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
given time. A job has a maximum allowed runtime. If this maximum is exceeded,
the job will kill itself.

In addition to that, job execution can be logged.

To use this module, you must derive your own class from :class:`Job` and
implement the :meth:`execute` method.

Logs will (by default) be created in the :dir:`~/ll.sisyphus` directory.
This can be changed by deriving a new subclass and overwriting the appropriate
class attribute.

To execute a job, use the module level function :func:`execute` (or
:func:`executewithargs` when you want to support command line arguments).

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
		argdescription = "fetch http://www.python.org/ and save it to a local file"
		maxtime = 180

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

You will find the log files for this job in ``~/ll.sisyphus/ACME.FooBar/Fetch/``.
"""


import sys, os, signal, fcntl, codecs, traceback, errno, pprint, datetime, re, contextlib, argparse

from ll import url, ul4c, misc


__docformat__ = "reStructuredText"


def literaldecode(exc):
	return (u"".join(u"[%02x]" % ord(c) for c in exc.object[exc.start:exc.end]), exc.end)

codecs.register_error("literaldecode", literaldecode)


encodingdeclaration = re.compile(r"coding[:=]\s*([-\w.]+)")


class MaximumRuntimeExceeded(Exception):
	def __init__(self, maxtime):
		self.maxtime = maxtime

	def __str__(self):
		return "maximum runtime of {} seconds exceeded".format(self.maxtime)


class Job(object):
	"""
	A Job object executes a task once.

	To use this class, derive your own class from it and overwrite the
	:meth:`execute` method.

	Logging itself is done by calling ``self.log``::

		self.log("can't parse XML file {}".format(filename))

	This logs the argument without tagging the line. To add tags to the logging
	call, simply access attributes of ``self.log``::

		self.log.xml.warning("can't parse XML file {}".format(filename))

	This adds the tags ``"xml"`` and ``"warning"`` to the log line.

	:mod:`ll.sisyphus` itself uses the following tags:

		``sisyphus``
			This tag will be added to all log lines produced by :mod:`ll.sisyphus`
			itself

		``init``
			This tag is used for the log lines output at the start of the job

		``result``
			This tag is used for final line it the log files that shows a summary
			of what the job did (or why it failed)

		``fail``
			This tag is used in the result line if the job failed with a exception.

		``kill``
			This tag is used in the result line if the job was killed because it
			exceeded the maximum allowed runtime.

	The job con be configured in three ways. By class attributes in the
	:class:`Job` subclass, by attributes of the :class:`Job` instance (e.g. set
	in :meth:`__init__`) and by command line arguments (if :func:`executewithargs`
	is used). The following attributes are supported:

	``projectname`` : :option:`-p` or :option:`--projectname`
		The name of the project this job belongs to. This might be a dot-separated
		hierarchical project name (e.g. including customer names or similar stuff).

	``jobname`` : :option:`-j` or :option:`--jobname`
		The name of the job itself (defaulting to the name of the class if
		:const:`None` is given).

	``argdescription`` : No command line equivalent
		Description for help message of the command line argument parser.

	``maxtime`` : :option:`-m` or :option:`--maxtime`
		Maximum allowed runtime for the job (as the number of seconds). If the job
		runs longer than that it will kill itself.

	``fork`` : :option:`--fork`
		Forks the process and does the work in the child process. The parent
		process is responsible for monitoring the maximum runtime (this is the
		default). In non-forking mode the single process does both the work and
		the runtime monitoring.

	``noisykills`` : :option:`--noisykills`
		Should a message be printed when the maximum runtime is exceeded?

	``logfilename`` : :option:`--logfilename`
		Path/name of the logfile for this job as an UL4 template. Variables
		available in the template include ``user_name``, ``projectname``,
		``jobname`` and ``starttime``.

	``loglinkname`` : :option:`--loglinkname`
		A link that points to the currently active logfile (as an UL4 template).
		If this is :const:`None` no link will be created.

	``log2file`` : :option:`-f` or :option:`--log2file`
		Should a logfile be written at all?

	``formatlogline`` : :option:`--formatlogline`
		An UL4 template for formatting each line in the logfile. Available
		variables are ``time`` (current time), ``starttime`` (start time of the
		job), ``tags`` (list of tags for the line) and ``line`` (the log line
		itself).

	``keepfilelogs`` : :option:`--keepfilelogs`
		The number of days the logfiles are kept. Old logfiles (i.e. any file in
		the same directory as the current logfile that's more than
		``keepfilelogs`` days old) will be removed at the end of the job.

	``inputencoding`` : :option:`--inputencoding`
		The encoding to be used for data that is supposed to be unicode, but isn't
		(e.g. host/user/network info, lines passed to ``self.log`` etc.)

	``inputerrors`` : :option:`--inputerrors`
		Decoding error handler name (goes with ``inputencoding``)

	``outputencoding`` : :option:`--outputencoding`
		The encoding to be used for the logfile.

	``outputerrors`` : :option:`--outputerrors`
		Encoding error handler name (goes with ``outputencoding``)

	Command line arguments take precedence over instance attributes (if
	:func:`executewithargs` is used) and those take precedence over class
	attributes.
	"""

	projectname = None
	jobname = None

	argdescription = "execute the job"

	maxtime = 5 * 60

	fork = True

	noisykills = False

	logfilename = u"~/ll.sisyphus/<?print projectname?>/<?print jobname?>/<?print starttime.format('%Y-%m-%d-%H-%M-%S-%f')?>.sisyphuslog"
	loglinkname = u"~/ll.sisyphus/<?print projectname?>/<?print jobname?>/current.sisyphuslog"

	log2file = True
	log2stdout = False
	log2stderr = False

	formatlogline = u"[<?print time?>]=[t+<?print time-starttime?>]<?for tag in tags?>[<?print tag?>]<?end for?>: <?print line?>"

	keepfilelogs = 30

	inputencoding = u"utf-8"
	inputerrors = u"literaldecode"

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
		p.add_argument("-p", "--projectname", dest="projectname", metavar="NAME", help="The name of the project this job belongs to (default: %(default)s)", type=self._string, default=self.projectname)
		p.add_argument("-j", "--jobname", dest="jobname", metavar="NAME", help="The name of the job (default: %(default)s)", type=self._string, default=self.jobname if self.jobname is not None else self.__class__.__name__)
		p.add_argument("-m", "--maxtime", dest="maxtime", metavar="SECONDS", help="Maximum number of seconds the job is allowed to run (default: %(default)s)", type=int, default=self.maxtime)
		p.add_argument(      "--fork", dest="fork", help="Fork the process and do the work in the child process? (default: %(default)s)", action=misc.FlagAction, default=self.fork)
		p.add_argument("-f", "--log2file", dest="log2file", help="Should the job log into a file? (default: %(default)s)", action=misc.FlagAction, default=self.log2file)
		p.add_argument("-o", "--log2stdout", dest="log2stdout", help="Should the job log to stdout? (default: %(default)s)", action=misc.FlagAction, default=self.log2stdout)
		p.add_argument("-e", "--log2stderr", dest="log2stderr", help="Should the job log to stderr? (default: %(default)s)", action=misc.FlagAction, default=self.log2stderr)
		p.add_argument(      "--keepfilelogs", dest="keepfilelogs", metavar="DAYS", help="Number of days log files are kept (default: %(default)s)", type=float, default=self.keepfilelogs)
		p.add_argument(      "--inputencoding", dest="inputencoding", metavar="ENCODING", help="Encoding for system data (i.e. crontab etc.) (default: %(default)s)", default=self.inputencoding)
		p.add_argument(      "--inputerrors", dest="inputerrors", metavar="METHOD", help="Error handling method for encoding errors in system data (default: %(default)s)", default=self.inputerrors)
		p.add_argument(      "--outputencoding", dest="outputencoding", metavar="ENCODING", help="Encoding for the log file (default: %(default)s)", default=self.outputencoding)
		p.add_argument(      "--outputerrors", dest="outputerrors", metavar="METHOD", help="Error handling method for encoding errors in log texts (default: %(default)s)", default=self.outputerrors)
		p.add_argument(      "--noisykills", dest="noisykills", help="Should a message be printed if the maximum runtime is exceeded? (default: %(default)s)", action=misc.FlagAction, default=self.noisykills)
		return p

	def parseargs(self, args=None):
		"""
		Use the parser returned by :meth:`argparser` to parse the argument
		sequence :var:`args`, modify :var:`self` accordingly and return
		the result of the parsers :meth:`parse_args` call.
		"""
		p = self.argparser()
		args = p.parse_args(args)
		self.projectname = args.projectname
		self.jobname = args.jobname
		self.maxtime = args.maxtime
		self.fork = args.fork
		self.noisykills = args.noisykills
		self.log2file = args.log2file
		self.log2stdout = args.log2stdout
		self.log2stderr = args.log2stderr
		self.keepfilelogs = datetime.timedelta(days=args.keepfilelogs)
		self.inputencoding = args.inputencoding
		self.inputerrors = args.inputerrors
		self.outputencoding = args.outputencoding
		self.outputerrors = args.outputerrors
		return args

	def _alarm_fork(self, signum, frame):
		os.kill(self.killpid, signal.SIGTERM) # Kill our child
		maxtime = datetime.timedelta(seconds=self.maxtime)
		if self._logfile is not None:
			self.log.sisyphus.result.kill(u"Terminated child after {}".format(maxtime))
			self._logfile.close()
		if self.noisykills:
			print "Terminated forked job {} (pid {}) after {}".format(self.info.sysinfo.scriptname, self.info.sysinfo.pid, maxtime)
		os._exit(1)

	def _alarm_nofork(self, signum, frame):
		self._prefix = ""
		maxtime = datetime.timedelta(seconds=self.maxtime)
		if self._logfile is not None:
			self.log.sisyphus.result.kill(u"Terminated after {}".format(maxtime))
			self._logfile.close()
		if self.noisykills:
			print "Terminated job {} (pid {}) after {}".format(self.info.sysinfo.scriptname, self.info.sysinfo.pid, maxtime)
		os._exit(1)

	def _handleexecution(self):
		"""
		Handle executing the job including handling of duplicate or hanging jobs.
		"""
		self.info = AttrDict()
		self.info.sysinfo = misc.SysInfo(self.inputencoding, self.inputerrors)
		self.info.projectname = self._string(self.projectname)
		self.info.jobname = self._string(self.jobname)
		self.info.maxtime = self.maxtime
		self._prefix = ""

		# Obtain a lock on the script file to make sure we're the only one running
		with open(self.info.sysinfo.scriptname, "rb") as f:
			try:
				fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError, exc:
				if exc[0] not in (errno.EACCES, errno.EAGAIN): # some other error
					raise
				# The previous invocation of the job is still running
				return # Return without calling :meth:`execute`

			# we were able to obtain the lock, so we are the only one running
			self.info.starttime = datetime.datetime.now()

			self._getscriptsource() # Get source code
			self._getcrontab() # Get crontab
			self.lineno = 1 # Current line number
			self.log = Tag(self._log) # Create tagged logger
			self._formatlogline = ul4c.compile(self.formatlogline.replace("\n", "").replace("\r", "") + u"\n") # Log line formatting template
			self._createlog() # Create log file and link

			self.log.sisyphus.init(u"{} (max time {}; pid {})".format(self.info.sysinfo.scriptname, datetime.timedelta(seconds=self.maxtime), self.info.sysinfo.pid))

			if self.fork: # Forking mode?
				# Fork the process; the child will do the work; the parent will monitor the maximum runtime
				self.killpid = pid = os.fork()
				if pid: # We are the parent process
					# set a signal to kill the child process after the maximum runtime
					signal.signal(signal.SIGALRM, self._alarm_fork)
					signal.alarm(self.maxtime)
					os.wait() # Wait for the child process to terminate
					return # Exit normally
				self.log.sisyphus.init(u"forked worker child (child pid {})".format(os.getpid()))
			else: # We didn't fork
				# set a signal to kill ourselves after the maximum runtime
				signal.signal(signal.SIGALRM, self._alarm_nofork)
				signal.alarm(self.maxtime)

			try:
				with url.Context():
					result = self.execute()
				self._cleanupoldlogs() # Clean up old logfiles
			except BaseException, exc:
				# log the error to the logfile, because the job probably didn't have a chance to do it
				self.log.sisyphus.exc(exc)
				result = u"failed with {}".format(self._exc(exc))
				self.log.sisyphus.result.fail(result)
				self.failed()
				raise
			else:
				# log the result
				self.log.sisyphus.result.ok(self._string(result))
			finally:
				if self._logfile is not None:
					self._logfile.close()
				fcntl.flock(f, fcntl.LOCK_UN | fcntl.LOCK_NB)
			if self.fork:
				os._exit(0)

	@contextlib.contextmanager
	def prefix(self, prefix):
		"""
		:meth:`prefix` is a context manager. For the duration of the ``with`` block
		:var:`prefix` will be prepended to all log lines. :meth:`prefix` calls can
		be nested.
		"""
		oldprefix = self._prefix
		self._prefix += prefix
		try:
			yield
		finally:
			self._prefix = oldprefix

	def _log(self, tags, *texts):
		"""
		Log items in :var:`texts` to the log file using :var:`tags` as the list
		of tags.
		"""
		if self.log2file or self.log2stdout or self.log2stderr:
			timestamp = datetime.datetime.now()
			for text in texts:
				text = self._string(text)
				if isinstance(text, BaseException):
					if "exc" not in tags:
						tags += ("exc",)
					tb = u"".join(map(self._string, traceback.format_tb(sys.exc_info()[-1])))
					text = u"{tb}\n{exc}".format(tb=tb, exc=self._exc(text))
				elif not isinstance(text, unicode):
					text = self._string(pprint.pformat(text))
				lines = text.splitlines()
				if lines and not lines[-1].strip():
					del lines[-1]
				for line in lines:
					text = self._formatlogline.renders(line=self._prefix+line, time=timestamp, tags=tags, **self.info)
					text = text.encode(self.outputencoding, self.outputerrors)
					if self.log2file:
						self._logfile.write(text)
						self._logfile.flush()
					if self.log2stdout:
						sys.stdout.write(text)
						sys.stdout.flush()
					if self.log2stderr:
						sys.stderr.write(text)
						sys.stderr.flush()
					self.lineno += 1

	def _getscriptsource(self):
		"""
		Reads the source code of the script into ``self.source``.
		"""
		try:
			with open(self.info.sysinfo.scriptname.rstrip("c"), "rb") as f:
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
		except IOError: # Script might have called ``os.chdir()`` before
			self.source = None

	def _getcrontab(self):
		"""
		Reads the current crontab into ``self.crontab``.
		"""
		self.crontab = self._string(os.popen("crontab -l 2>/dev/null").read())

	def _createlog(self):
		"""
		Create the logfile and the link to the logfile (if requested).
		"""
		self._logfile = None
		self._logfilename = None
		self._loglinkname = None
		if self.log2file:
			# Create the log file
			logfilename = ul4c.compile(self.logfilename).renders(**self.info)
			lf = self._logfilename = url.File(logfilename).abs()
			self._logfile = lf.openwrite()
			if self.loglinkname is not None:
				# Create the log link
				loglinkname = ul4c.compile(self.loglinkname).renders(**self.info)
				ll = self._loglinkname = url.File(loglinkname).abs()
				lf = self._logfilename
				try:
					lf.symlink(ll)
				except OSError, exc:
					if exc[0] == errno.EEXIST:
						ll.remove()
						lf.symlink(ll)
					else:
						raise

	def _cleanupoldlogs(self):
		"""
		Remove old logfiles.
		"""
		if self._logfile is not None and self.keepfilelogs is not None:
			removedany = False
			keepfilelogs = self.keepfilelogs
			if not isinstance(keepfilelogs, datetime.timedelta):
				keepfilelogs = datetime.timedelta(days=keepfilelogs)
			threshold = datetime.datetime.utcnow() - keepfilelogs # Files older that this will be deleted
			logdir = self._logfile.url.withoutfile()
			for fileurl in logdir/logdir.files():
				fileurl = logdir/fileurl
				# Never delete the current log file or link, even if keepfilelogs is 0
				if fileurl == self._logfilename or fileurl == self._loglinkname:
					continue
				# If the file is to old, delete it (note that this might delete files that were not produced by sisyphus)
				if fileurl.mdate() < threshold:
					if not removedany: # Only log this line for the first logfile we remove
						self.log.sisyphus.info("Removing logfiles older than {}".format(keepfilelogs))
						removedany = True
					self.log.sisyphus.info("Removing logfile {}".format(fileurl.local()))
					fileurl.remove()

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
			fmt = u"{0.__class__.__module__}.{0.__class__.__name__}: {1}"
		else:
			fmt = u"{0.__class__.__name__}: {1}"
		try:
			strexc = unicode(exc)
		except UnicodeError:
			try:
				strexc = str(exc)
			except UnicodeError:
				strexc = u"?"
		return fmt.format(exc, strexc)


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


def execute(job):
	"""
	Execute the job :var:`job` once.
	"""
	job._handleexecution()


def executewithargs(job, args=None):
	"""
	Execute the job :var:`job` once with command line arguments.

	:var:`args` are the command line arguments (:const:`None` results in
	``sys.argv`` being used)
	"""
	job.parseargs(args)
	job._handleexecution()
