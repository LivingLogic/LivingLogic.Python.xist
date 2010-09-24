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

In addition to that, logging features are provided.

To use this module, you must derive your own class from :class:`Job` and
implement the :meth:`execute` method.

The job announces its presence (and its process id) in a file that is stored in
the :dir:`~/run` directory. Logs will be created in the :dir:`~/log` directory
(This can be changes by deriving new subclasses and overwriting the appropriate
class attribute).

There are three log files:

	:file:`~/log/jobname_progress.log`
		The progress of one job execution is logged here. This log file will be
		truncated at the start of every execution, so you can be rather verbose.
		Use the :meth:`logProgress` method for writing to this log file.

	:file:`~/log/jobname_loop.log`
		One log line may be appended to the log after every job execution.
		Call the method :meth:`logLoop` once at the end of :meth:`execute` for
		this.

	:file:`~/log/jobname_error.log`
		Here exceptions happening during the execution of a job will be logged.
		This is done via the :meth:`logError` method with can be used for
		reporting other exception conditions apart from exceptions.

To execute a job, use the module level function :func:`execute`.

Example
-------

The following example illustrates the use of this module::

	#!/usr/bin/env python

	import os
	import urllib
	from ll import sisyphus

	class Fetch(sisyphus.Job):
		"savely fetches an HTML file and saves it to a local file."

		def __init__(self):
			sisyphus.Job.__init__(self, "ACME.FooBar", "Fetch", "log/pwd@logging.acme.com", 180)
			self.url = "http://www.python.org/"
			self.tmpname = "Fetch_Tmp_{0}.html".format(os.getpid())
			self.officialname = "Python.html"

		def execute(self):
			self.log("fetching data from {0!r}".format(self.url))
			data = urllib.urlopen(self.url).read()
			datasize = len(data)
			self.log("writing file {0!r} ({1} bytes)".format(self.tmpname, datasize))
			open(self.tmpname, "wb").write(data)
			self.log("renaming file {0!r} to {1!r}".format(self.tmpname, self.officialname))
			os.rename(self.tmpname, self.officialname)
			return "cached {0!r} as {1!r} ({2} bytes)".format(self.url, self.officialname, datasize)

	if __name__=="__main__":
		sisyphus.execute(Fetch())
"""


import sys, os, socket, pwd, codecs, traceback, errno, pprint, datetime, re, contextlib

from ll import url, ul4c


__docformat__ = "reStructuredText"


def literaldecode(exc):
	return (u"".join(u"[%02x]" % ord(c) for c in exc.object[exc.start:exc.end]), exc.end)

codecs.register_error("literaldecode", literaldecode)


encodingdeclaration = re.compile(r"coding[:=]\s*([-\w.]+)")


class DBInfo(object):
	"""
	This object handles all communcation with the database
	"""
	# Username for logging to the db
	user = u"ll.sisyphus"

	# The names of procedures to call for certain events
	procname_start = "DGRUN_START"
	procname_log = "DGRUN_LOG"
	procname_error = "DGRUN_ERROR"
	procname_failed = "DGRUN_FAILED"
	procname_end = "DGRUN_END"

	def __init__(self, job, connectstring):
		self.job = job
		self.connectstring = connectstring

	def start(self):
		"""
		Start logging. If :meth:`start` returns false, the job will not run.
		"""
		from ll import orasql
		self.db = orasql.connect(self.connectstring, threaded=True)
		self.dbrun_start = orasql.Procedure(self.procname_start)
		self.dbrun_log = orasql.Procedure(self.procname_log)
		self.dbrun_error = orasql.Procedure(self.procname_error)
		self.dbrun_failed = orasql.Procedure(self.procname_failed)
		self.dbrun_end = orasql.Procedure(self.procname_end)
		self.cursor = self.db.cursor()
		self.run = self.dbrun_start(
			self.cursor,
			c_user=self.user,
			p_pro_name=self.job.info.projectname,
			p_job_name=self.job.info.jobname,
			p_host_name=self.job.info.host_name,
			p_host_fqdn=self.job.info.host_fqdn,
			p_host_ip=self.job.info.host_ip,
			p_host_sysname=self.job.info.host_sysname,
			p_host_nodename=self.job.info.host_nodename,
			p_host_release=self.job.info.host_release,
			p_host_version=self.job.info.host_version,
			p_host_machine=self.job.info.host_machine,
			p_user_name=self.job.info.user_name,
			p_user_uid=self.job.info.user_uid,
			p_user_gid=self.job.info.user_gid,
			p_user_gecos=self.job.info.user_gecos,
			p_user_dir=self.job.info.user_dir,
			p_user_shell=self.job.info.user_shell,
			p_scr_filename=self.job.info.filename,
			p_scr_source=self.job.source,
			p_cron_tab=self.job.crontab,
			p_run_start=self.job.info.starttime,
			p_run_pid=self.job.info.pid,
			p_job_logfilename=self.job.logfilename,
			p_job_loglinkname=self.job.loglinkname,
			p_job_pidfilename=self.job.pidfilename,
			p_job_log2file=self.job.log2file,
			p_job_log2db=self.job.log2db,
			p_job_formatlogline=self.job.formatlogline,
			p_job_keepfilelogs=self.job.keepfilelogs,
			p_job_keepdblogs=self.job.keepdblogs,
			p_job_keepdbruns=self.job.keepdbruns,
		)
		self.db.commit()

		# Copy information from the database back to the job
		self.job.logfilename = self.run.p_job_logfilename
		self.job.loglinkname = self.run.p_job_loglinkname
		self.job.pidfilename = self.run.p_job_pidfilename
		self.job.log2file = self.run.p_job_log2file
		self.job.log2db = self.run.p_job_log2db
		self.job.formatlogline = self.run.p_job_formatlogline
		self.job.keepfilelogs = self.run.p_job_keepfilelogs
		self.job.keepdblogs = self.run.p_job_keepdblogs
		self.job.keepdbruns = self.run.p_job_keepdbruns
		return self.run.p_job_active != 0

	def end(self, result):
		"""
		Finish logging (without errors) and clean up.
		"""
		self.dbrun_end(
			self.cursor,
			c_user=self.user,
			p_run_id=self.run.p_run_id,
			p_run_end=datetime.datetime.now(),
			p_run_result=self.job._string(result),
			p_keepdblogs=self.job.keepdblogs,
			p_keepdbruns=self.job.keepdbruns,
		)
		self.db.commit()

	def failed(self, result):
		"""
		Finish logging (with errors) and clean up.
		"""
		self.dbrun_failed(
			self.cursor,
			c_user=self.user,
			p_run_id=self.run.p_run_id,
			p_run_end=datetime.datetime.now(),
			p_run_result=self.job._string(result),
			p_keepdblogs=self.job.keepdblogs,
			p_keepdbruns=self.job.keepdbruns,
		)
		self.db.commit()

	def log(self, timestamp, tags, line):
		"""
		Write a log line to the database.
		"""
		self.dbrun_log(
			self.cursor,
			c_user=self.user,
			p_run_id=self.run.p_run_id,
			p_log_lineno=self.job.lineno,
			p_log_date=timestamp,
			p_log_tags=u", ".join(tags),
			p_log_line=line
		)
		self.db.commit()

	def error(self):
		"""
		Record that this job has produced an error in the database.
		"""
		self.dbrun_error(
			self.cursor,
			c_user=self.user,
			p_run_id=self.run.p_run_id
		)
		self.db.commit()


class Log(object):
	def __init__(self, job, *tags):
		self.job = job
		self.tags = tags
		self._map = {}

	def __getattr__(self, tag):
		if tag not in self._map:
			newlog = Log(self.job, *(self.tags + (tag,)))
			self._map[tag] = newlog
			return newlog
		else:
			return self._map[tag]

	__getitem__ = __getattr__

	def __call__(self, *texts):
		self.job._log(self.tags, *texts)


class AttrDict(dict):
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

	# Default log/pidfile location/name as an UL4 template (can be overwritten in subclasses or by the db)
	logfilename = u"~<?print user_name?>/log/<?print projectname?>/<?print jobname?>/<?print starttime.format('%Y-%m-%d-%H-%M-%S-%f')?>.sisyphuslog"
	loglinkname = u"~<?print user_name?>/log/<?print projectname?>/<?print jobname?>/current.sisyphuslog"
	pidfilename = u"~<?print user_name?>/run/<?print projectname?>/<?print jobname?>.pid"

	# Should logging be done to files or to the database? (can be overwritten in subclasses or by the db)
	log2file = True
	log2db = True

	# Format string for logging (can be overwritten in subclasses or by the db)
	formatlogline = u"[<?print time?>]=[t+<?print time-starttime?>]<?if tags?>[<?print ', '.join(tags)?>]<?end if?>: <?print line?>\n"

	# How many days to keep logs (can be overwritten in subclasses or by the db)
	keepfilelogs = 30 # log files
	keepdblogs = 90 # database log (detailed line listing)
	keepdbruns = 300 # database log (summary of the run)

	# Encoding/errors to be used for all system data (host/user/network info etc.)
	inputencoding = u"utf-8"
	inputerrors = u"literaldecode"

	# Encoding/errors to be used for the logfile
	outputencoding = u"utf-8"
	outputerrors = u"strict"

	# Class to use for all communication with the database
	DBInfo = DBInfo

	def __init__(self, projectname, jobname, connectstring=None, maxruntime=0):
		"""
		Create a new :class:`Job` object. Parameters have the following meaning:

			:var:`projectname` : string
				The name of the project this job belongs to. This might be a
				dot-separated hierarchical project name (e.g. including customer
				names or similar stuff).

			:var:`jobname` : string
				The name of the job itself.

			:var:`connectstring` : string or :const:`None`
				A connect string for connecting to the database. This is passed to
				the constructor of the nested :class:`DBInfo` class (which can be
				overwritten in subclasses to support databases other than Oracle).
				If :var:`connectstring` is :const:`None` the job never talks to the
				database.

			:var:`maxruntime` : :class:`int` or :class:`datetime.timedelta`
				Maximum allowed runtime for the job (as a :class:`datetime.timedelta`
				instance or the number of seconds). If a job is started and the
				previous invocation has been running for more than :var:`maxruntime`
				the previous job will be killed.
		"""
		self.info = AttrDict()
		self.info.projectname = self._string(projectname)
		self.info.jobname = self._string(jobname)

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

		if not isinstance(maxruntime, datetime.timedelta):
			maxruntime = datetime.timedelta(seconds=maxruntime)
		self.info.maxruntime = maxruntime

		self.pidfilewritten = False

		self.__db = self.DBInfo(self, connectstring) if connectstring is not None else None

	def _string(self, s):
		if isinstance(s, str):
			s = s.decode(self.inputencoding, self.inputerrors)
		return s

	def _exc(self, exc):
		if exc.__class__.__module__ not in ("__builtin__", "exceptions"):
			fmt = u"{0.__class__.__module__}.{0.__class__.__name__}: {0}"
		else:
			fmt = u"{0.__class__.__name__}: {0}"
		return fmt.format(exc)

	def _log(self, tags, *texts):
		"""
		Log items in :var:`texts` to the log file and/or the database using
		:var:`tags` as the list of tags.
		"""
		if self.log2file or (self.__db is not None and self.log2db):
			timestamp = datetime.datetime.now()
			for text in texts:
				text = self._string(text)
				if isinstance(text, BaseException):
					tb = u"".join(traceback.format_tb(sys.exc_info()[-1]))
					text = u"{tb}\n{exc}".format(tb=tb, exc=self._exc(text))
				elif not isinstance(text, unicode):
					text = self._string(pprint.pformat(text))
				lines = text.splitlines()
				if lines and not len(lines[-1]):
					del lines[-1]
				for line in lines:
					if self.log2file:
						text = self._formatlogline.renders(line=line, time=timestamp, tags=tags, **self.info)
						self._logfile.write(text.encode(self.outputencoding, self.outputerrors))
						self._logfile.flush()
					if self.__db is not None and self.log2db:
						self.__db.log(timestamp, tags, line)
					self.lineno += 1
			if self.__db is not None and ("error" in tags or "exc" in tags):
				self.__db.error()

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

	def _createlog(self):
		"""
		Create the logfile and a link to this logfile (if requested).
		"""
		self._logfile = None
		if self.log2file:
			logfilename = ul4c.compile(self.logfilename).renders(**self.info)
			lf = url.File(logfilename)
			self._logfile = lf.openwrite()

			if self.loglinkname is not None:
				loglinkname = ul4c.compile(self.loglinkname).renders(**self.info)
				ll = url.File(loglinkname)
				try:
					lf.symlink(ll)
				except OSError, exc:
					if exc[0] == errno.EEXIST:
						ll.remove()
						lf.symlink(ll)
					else:
						raise
		self.log = Log(self)

	def _cleanupoldlogs(self):
		"""
		Remove old logfiles.
		"""
		if self._logfile and self.keepfilelogs is not None:
			removedany = False
			keepfilelogs = self.keepfilelogs
			if not isinstance(keepfilelogs, datetime.timedelta):
				keepfilelogs = datetime.timedelta(days=keepfilelogs)
			threshold = datetime.datetime.now() - keepfilelogs # Files older that this will be deleted
			logdir = self._logfile.url.withoutfile()
			for fileurl in logdir/logdir.files():
				if fileurl.mdate() < threshold:
					if not removedany: # Only log this line for the first logfile we remove
						self.log.sisyphus.info("Removing logfiles older than {0} days".format(keepfilelogs.days))
						removedany = True
					self.log.sisyphus.info("Removing logfile {0}".format(fileurl.local()))
					fileurl.remove()

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

	def handleexecution(self):
		"""
		Handle executing the job including handling of duplicate or hanging jobs.
		This is the method to be called from the outside world.
		"""
		self.info.starttime = datetime.datetime.now()

		if self.__db is not None:
			if not self.__db.start():
				self.__db.end(u"job is deactivated")
				return

		pidfilename = ul4c.compile(self.pidfilename).renders(**self.info)
		pidfilename = os.path.expanduser(pidfilename)

		self._formatlogline = ul4c.compile(self.formatlogline.replace("\n", "").replace("\r", "") + u"\n")

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
				# disk may have been full
				pidfile.close()
				self._writepid(pidfilename)
				self.log.sisyphus.warning(u"ignoring bogus pid file {0} (invalid content)".format(pidfilename))
			else:
				pidfile.close()
				# Check if this process really exists, if not continue as if the pid file wasn't there
				try:
					os.kill(pid, 0)
				except OSError, exc:
					if exc[0] != errno.ESRCH:
						raise
					self._writepid(pidfilename)
					msg = u"ignoring bogus pid file {0} (process with pid {1} doesn't exist)".format(pidfilename, pid)
					self.log.sisyphus.warning(msg)
				else:
					if self.info.maxruntime and self.info.starttime-lastmodified > self.info.maxruntime: # the job is to old, so it probably hangs => kill it
						try:
							os.kill(pid, 9)
						except OSError, exc:
							if exc[0] != errno.ESRCH: # there was no process
								raise
						self._writepid(pidfilename)
						msg = u"killed previous job running with pid {0} (ran {1} seconds; {2} allowed); here we go!".format(pid, self.info.starttime-lastmodified, self.info.maxruntime)
						self.log.sisyphus.warning(msg)
					else:
						msg = u"Job still running (for {0}; {1} allowed; started on {2}) with pid {3} (according to {4})".format(self.info.starttime-lastmodified, lastmodified, pid, pidfilename)
						self.log.sisyphus.warning(msg)
						return # Return without calling :meth:`execute`

		try:
			with url.Context():
				result = self.execute()
				self._cleanupoldlogs() # Clean up old logfiles
		except BaseException, exc:
			# log the error to the logfile, because the job probably didn't have a chance to do it
			self.log.sisyphus.exc(exc)
			result = u"failed with {0}".format(self._exc(exc))
			self.log.sisyphus.error(result)
			if self.__db is not None:
				self.__db.failed(result)
			self.failed()
			self._killpid(pidfilename)
			raise
		else:
			# log the result
			self.log.sisyphus.info(self._string(result))
			if self.__db is not None:
				self.__db.end(result)
		finally:
			self._logfile.close()
		self._killpid(pidfilename) # finished => remove the pid file


def execute(*jobs):
	"""
	Execute several jobs.

	Items in :var:`jobs` are job objects that will be executed sequentially.
	"""
	for job in jobs:
		job.handleexecution()
