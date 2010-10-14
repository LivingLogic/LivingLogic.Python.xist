#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2000-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2000-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
:mod:`ll.sisyphus` simplifies running Python stuff as cron jobs.

There will be no more than one sisyphus job of a certain name running at every
given time. When the job is already running and a second is started, the second
one will quit immediately if the first one hasn't exceeded its maximum allowed
lifetime yet. If it has exceeded the allowed lifetime the first job
will be killed and the second will start running.

In addition to that, job execution can be logged.

To use this module, you must derive your own class from :class:`Job` and
implement the :meth:`execute` method.

The job announces its presence (and its process id) in a file that is stored in
the :dir:`~/run` directory. Logs will be created in the :dir:`~/log` directory
(This can be changes by deriving new subclasses and overwriting the appropriate
class attribute).

To execute a job, use the module level function :func:`execute` (or
:func:`executewithargs` when you want to support command line argument).

Example
-------

The following example illustrates the use of this module::

	#!/usr/bin/env python

	import os
	import urllib
	from ll import sisyphus

	class Fetch(sisyphus.Job):
		projectname = "ACME.FooBar"
		jobname = "Fetch"
		maxtime = 180
		argdescription = "savely fetches http://www.python.org/ and saves it to a local file"

		def __init__(self):
			self.url = "http://www.python.org/"
			self.tmpname = "Fetch_Tmp_{}.html".format(os.getpid())
			self.officialname = "Python.html"

		def execute(self):
			self.log("fetching data from {!r}".format(self.url))
			data = urllib.urlopen(self.url).read()
			datasize = len(data)
			self.log("writing file {!r} ({} bytes)".format(self.tmpname, datasize))
			open(self.tmpname, "wb").write(data)
			self.log("renaming file {!r} to {!r}".format(self.tmpname, self.officialname))
			os.rename(self.tmpname, self.officialname)
			return "cached {!r} as {!r} ({} bytes)".format(self.url, self.officialname, datasize)

	if __name__=="__main__":
		sisyphus.executewithargs(Fetch())
"""


import sys, os, socket, pwd, codecs, traceback, errno, pprint, datetime, re, contextlib, argparse

from ll import url, ul4c


__docformat__ = "reStructuredText"


def literaldecode(exc):
	return (u"".join(u"[%02x]" % ord(c) for c in exc.object[exc.start:exc.end]), exc.end)

codecs.register_error("literaldecode", literaldecode)


encodingdeclaration = re.compile(r"coding[:=]\s*([-\w.]+)")


class Tag(object):
	"""
	A :class:`Tag` object can be used to call a function with an additional list
	of tags. Tags ca be added via :meth:`__getattr__` or :meth:`__getitem__` calls.
	"""
	def __init__(self, log, *tags):
		self.log = log
		self.tags = tags
		self._map = {}

	def __getattr__(self, tag):
		if tag in self.tags: # Avoid duplicate tags
			return self
		if tag not in self._map:
			newtag = Tag(self.log, *(self.tags + (tag,)))
			self._map[tag] = newtag
			return newtag
		else:
			return self._map[tag]

	__getitem__ = __getattr__

	def __call__(self, *texts, **kwargs):
		self.log(self.tags, *texts, **kwargs)


class AttrDict(dict):
	"""
	:class:`dict` subclass that makes keys available as attributes.
	"""
	def __getattr__(self, name):
		try:
			return self[name]
		except KeyError:
			raise AttributeError

	def __setattr__(self, name, value):
		self[name] = value


class Job(object):
	"""
	A Job object executes a task once.
	
	The job announces its presence (and its process id) in a file that is stored
	in the :dir:`~/run/` directory. Logs will be created in the :dir:`~/log/`
	directory (This can be changes by deriving new subclasses).

	To use this class, derive your own class from it and overwrite the
	:meth:`execute` method.
	"""

	# The name of the project this job belongs to. This might be a dot-separated hierarchical project name (e.g. including customer names or similar stuff).
	projectname = None

	# The name of the job itself (defaulting to the name of the class)
	jobname = None

	# Description for help message of the command line argument parser
	argdescription = "execute the job"

	# Maximum allowed runtime for the job (as a :class:`datetime.timedelta` instance or the number of seconds). If a job is started and the
	# previous invocation has been running for more than :var:`maxtime` the previous job will be killed.
	maxtime = 5 * 60

	# Default log/pidfile location/name as an UL4 template (can be overwritten in subclasses)
	logfilename = u"~<?print user_name?>/log/<?print projectname?>/<?print jobname?>/<?print starttime.format('%Y-%m-%d-%H-%M-%S-%f')?>.sisyphuslog"
	loglinkname = u"~<?print user_name?>/log/<?print projectname?>/<?print jobname?>/current.sisyphuslog"
	pidfilename = u"~<?print user_name?>/run/<?print projectname?>/<?print jobname?>.pid"

	# Should logging be done? (can be overwritten in subclasses)
	log2file = True

	# Format string for logging (can be overwritten in subclasses)
	formatlogline = u"[<?print time?>]=[t+<?print time-starttime?>]<?if tags?>[<?print ', '.join(tags)?>]<?end if?>: <?print line?>"

	# How many days to keep logs (can be overwritten in subclasses)
	keepfilelogs = 30 # log files

	# Encoding/errors to be used for all system data (host/user/network info etc.)
	inputencoding = u"utf-8"
	inputerrors = u"literaldecode"

	# Encoding/errors to be used for the logfile
	outputencoding = u"utf-8"
	outputerrors = u"strict"

	def execute(self):
		"""
		Execute the job once. The return value is a one line summary of what the
		job did. Overwrite in subclasses.
		"""
		return u"done"

	def failed(self):
		"""
		Called when running the job generated an exception. Overwrite in
		subclasses, to e.g. rollback your database transactions.
		"""
		pass

	def argparser(self):
		"""
		Return an :mod:`argparse` parser for parsing the command line arguments.
		This can be overwritten in subclasses to add more arguments.
		"""
		p = argparse.ArgumentParser(description=self.argdescription)
		p.add_argument("-p", "--projectname", dest="projectname", metavar="NAME", help="The name of the project this job belongs to", type=self._string, default=self.projectname)
		p.add_argument("-j", "--jobname", dest="jobname", metavar="NAME", help="The name of the job", type=self._string, default=self.jobname if self.jobname is not None else self.__class__.__name__)
		p.add_argument("-m", "--maxtime", dest="maxtime", metavar="SECONDS", help="Maximum number of seconds the job is allowed to run", type=int, default=self.info.maxtime.total_seconds())
		p.add_argument(      "--keepfilelogs", dest="keepfilelogs", metavar="DAYS", help="Number of days log files are kept", type=float, default=self.keepfilelogs)
		p.add_argument(      "--inputencoding", dest="inputencoding", metavar="ENCODING", help="Encoding for system data (i.e. crontab etc.)", default=self.inputencoding)
		p.add_argument(      "--inputerrors", dest="inputerrors", metavar="METHOD", help="Error handling method for encoding errors in system data", default=self.inputerrors)
		p.add_argument(      "--outputencoding", dest="outputencoding", metavar="ENCODING", help="Encoding for the log file", default=self.outputencoding)
		p.add_argument(      "--outputerrors", dest="outputerrors", metavar="METHOD", help="Error handling method for encoding errors in log texts", default=self.outputerrors)
		return p

	def parseargs(self, args=None):
		"""
		Use the parser returned by :meth:`argparser` to parse the argument
		sequence :var:`args`, modify :var:`self` accordingly and return
		the result of the parsers :meth:`parse_args` call.
		"""
		p = self.argparser()
		args = p.parse_args(args)
		self.info.projectname = args.projectname
		self.info.jobname = args.jobname
		self.info.maxtime = datetime.timedelta(seconds=args.maxtime)
		self.keepfilelogs = datetime.timedelta(days=args.keepfilelogs)
		self.inputencoding = args.inputencoding
		self.inputerrors = args.inputerrors
		self.outputencoding = args.outputencoding
		self.outputerrors = args.outputerrors
		return args

	def _setup(self):
		self.info = AttrDict()
		self.info.connectstring = self._string(self.connectstring)
		self.info.projectname = self._string(self.projectname)
		self.info.jobname = self._string(self.jobname)

		maxtime = self.maxtime
		if not isinstance(maxtime, datetime.timedelta):
			maxtime = datetime.timedelta(seconds=maxtime)
		self.info.maxtime = maxtime

		# Get PID
		self.info.pid = os.getpid()

		# Get host info
		host_name = socket.gethostname()
		self.info.host_name = self._string(socket.gethostname())
		self.info.host_fqdn = self._string(socket.getfqdn(host_name))
		self.info.host_ip = self._string(socket.gethostbyname(host_name))

		# Get uname info
		(self.info.host_sysname, self.info.host_nodename, self.info.host_release, self.info.host_version, self.info.host_machine) = map(self._string, os.uname())

		# Get user info
		(self.info.user_name, _, self.info.user_uid, self.info.user_gid, self.info.user_gecos, self.info.user_dir, self.info.user_shell) = map(self._string, pwd.getpwuid(os.getuid()))

		# Get filename
		filename = sys.modules["__main__"].__file__
		self.info.filename = self._string(os.path.abspath(filename))

		# Get source code
		with open(filename.rstrip("c"), "rb") as f:
			source = f.read()
			lines = source.splitlines()
			# find encoding in the first two lines
			encoding = self.inputencoding
			if lines and lines[0].startswith(codecs.BOM_UTF8):
				encoding = "utf-8"
			else:
				for line in lines[:2]:
					match = encodingdeclaration.search(line)
					if match is not None:
						encoding = match.group(1)
			self.source = source.decode(encoding, self.inputerrors)

		# Get crontab
		self.crontab = self._string(os.popen("crontab -l 2>/dev/null").read())

		# Current line number
		self.lineno = 1

		self.pidfilewritten = False

	def _handleexecution(self):
		"""
		Handle executing the job including handling of duplicate or hanging jobs.
		"""
		self.info.starttime = datetime.datetime.now()

		pidfilename = ul4c.compile(self.pidfilename).renders(**self.info)
		pidfilename = os.path.expanduser(pidfilename)

		formatlogline = self.formatlogline.replace("\n", "").replace("\r", "") + u"\n"
		self._formatlogline = ul4c.compile(formatlogline)

		self._createlog()

		self.log.sisyphus.info(u"{info.filename} (pid {info.pid})".format(info=self.info))
		try: # is there a pid file from a running job?
			pidfile = open(pidfilename, "r")
		except IOError, exc: # no pid file => the job has finished without problems
			if exc[0] == errno.ENOENT: # file not found
				self._writepid(pidfilename)
				self.log.sisyphus.info(u"no previous job running; here we go!")
			else:
				raise
		else:
			lastmodified = datetime.datetime.fromtimestamp(os.fstat(pidfile.fileno()).st_mtime)
			try:
				pid = int(pidfile.read())
			except ValueError:
				# file is empty or otherwise broken (disk may have been full)
				pidfile.close()
				self._writepid(pidfilename)
				self.log.sisyphus.warning(u"ignoring bogus pid file {} (invalid content)".format(pidfilename))
			else:
				pidfile.close()
				# Check if this process really exists, if not continue as if the pid file wasn't there
				try:
					os.kill(pid, 0)
				except OSError, exc:
					if exc[0] != errno.ESRCH:
						raise
					self._writepid(pidfilename)
					msg = u"ignoring bogus pid file {} (process with pid {} doesn't exist)".format(pidfilename, pid)
					self.log.sisyphus.warning(msg)
				else:
					if self.info.maxtime and self.info.starttime-lastmodified > self.info.maxtime: # the job is to old, so it probably hangs => kill it
						try:
							os.kill(pid, 9)
						except OSError, exc:
							if exc[0] != errno.ESRCH: # there was no process
								raise
						self._writepid(pidfilename)
						msg = u"killed previous job running with pid {} (ran {} seconds; {} allowed); here we go!".format(pid, self.info.starttime-lastmodified, self.info.maxtime)
						self.log.sisyphus.warning(msg)
					else:
						msg = u"Job still running (for {}; {} allowed; started on {}) with pid {} (according to {})".format(self.info.starttime-lastmodified, lastmodified, pid, pidfilename)
						self.log.sisyphus.warning(msg)
						return # Return without calling :meth:`execute`

		try:
			with url.Context():
				result = self.execute()
				self._cleanupoldlogs() # Clean up old logfiles
		except BaseException, exc:
			# log the error to the logfile, because the job probably didn't have a chance to do it
			self.log.sisyphus.exc(exc)
			result = u"failed with {}".format(self._exc(exc))
			self.log.sisyphus.result.error(result)
			self.failed()
			self._killpid(pidfilename)
			raise
		else:
			# log the result
			self.log.sisyphus.result(self._string(result))
		finally:
			self._logfile.close()
		self._killpid(pidfilename) # finished => remove the pid file

	def _log(self, tags, *texts):
		"""
		Log items in :var:`texts` to the log file using :var:`tags` as the list
		of tags.
		"""
		if self.log2file:
			timestamp = datetime.datetime.now()
			for text in texts:
				text = self._string(text)
				if isinstance(text, BaseException):
					tb = u"".join(traceback.format_tb(sys.exc_info()[-1]))
					text = u"{tb}\n{exc}".format(tb=tb, exc=self._exc(text))
				elif not isinstance(text, unicode):
					text = self._string(pprint.pformat(text))
				lines = text.splitlines()
				if lines and not lines[-1].strip():
					del lines[-1]
				for line in lines:
					text = self._formatlogline.renders(line=line, time=timestamp, tags=tags, **self.info)
					self._logfile.write(text.encode(self.outputencoding, self.outputerrors))
					self._logfile.flush()
					self.lineno += 1

	def _createlog(self):
		"""
		Create the logfile and a link to this logfile (if requested).
		"""
		self._logfile = None
		self._logfilename = None
		self._loglinename = None
		if self.log2file:
			logfilename = ul4c.compile(self.logfilename).renders(**self.info)
			lf = self._logfilename = url.File(logfilename).abs()
			self._logfile = lf.openwrite()

			if self.loglinkname is not None:
				loglinkname = ul4c.compile(self.loglinkname).renders(**self.info)
				ll = self._loglinkname = url.File(loglinkname).abs()
				try:
					lf.symlink(ll)
				except OSError, exc:
					if exc[0] == errno.EEXIST:
						ll.remove()
						lf.symlink(ll)
					else:
						raise
		self.log = Tag(self._log)

	def _cleanupoldlogs(self):
		"""
		Remove old logfiles.
		"""
		if self._logfile and self.keepfilelogs is not None:
			removedany = False
			keepfilelogs = self.keepfilelogs
			if not isinstance(keepfilelogs, datetime.timedelta):
				keepfilelogs = datetime.timedelta(days=keepfilelogs)
			threshold = datetime.datetime.utcnow() - keepfilelogs # Files older that this will be deleted
			logdir = self._logfile.url.withoutfile()
			for fileurl in logdir/logdir.files():
				fileurl = logdir/fileurl
				# Never delete the current log file or the link to it, even if keepfilelogs is 0
				if fileurl == self._logfile.url or fileurl == self._loglinkname:
					continue
				# If the file is to old, delete it (not that this might delete files that were not produced by sisyphus)
				if fileurl.mdate() < threshold:
					if not removedany: # Only log this line for the first logfile we remove
						self.log.sisyphus.info("Removing logfiles older than {}".format(keepfilelogs))
						removedany = True
					self.log.sisyphus.info("Removing logfile {}".format(fileurl.local()))
					fileurl.remove()

	def _writepid(self, pidfilename):
		"""
		Create the file containing the pid of the current process.
		"""
		if not self.pidfilewritten:
			with contextlib.closing(url.File(pidfilename).openwrite()) as file:
				file.write(str(self.info.pid))
			self.pidfilewritten = True

	def _killpid(self, pidfilename):
		"""
		Delete the pid file.
		"""
		if self.pidfilewritten:
			url.File(pidfilename).remove()
			self.pidfilewritten = False

	def _string(self, s):
		"""
		Convert :var:`s` to unicode if it's a :class:`str`.
		"""
		if isinstance(s, str):
			s = s.decode(self.inputencoding, self.inputerrors)
		return s

	def _exc(self, exc):
		"""
		Format an exception object for logging.
		"""
		if exc.__class__.__module__ not in ("__builtin__", "exceptions"):
			fmt = u"{0.__class__.__module__}.{0.__class__.__name__}: {0}"
		else:
			fmt = u"{0.__class__.__name__}: {0}"
		return fmt.format(exc)


def execute(job):
	"""
	Execute the job :var:`job` once.
	"""
	job._setup()
	job._handleexecution()


def executewithargs(job, args=None):
	"""
	Execute the job :var:`job` once with command line arguments.

	:var:`args` are the command line arguments (:const:`None` results in
	``sys.argv`` being used)
	"""
	job._setup()
	job.parseargs(args)
	job._handleexecution()
