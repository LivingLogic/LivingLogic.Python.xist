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
			sisyphus.Job.__init__(self, 180, name="Fetch")
			self.url = "http://www.python.org/"
			self.tmpname = "Fetch_Tmp_%d.html" % os.getpid()
			self.officialname = "Python.html"

		def execute(self):
			self.logProgress("fetching data from %r" % self.url)
			data = urllib.urlopen(self.url).read()
			datasize = len(data)
			self.logProgress("writing file %r (%d bytes)" % (self.tmpname, datasize))
			open(self.tmpname, "wb").write(data)
			self.logProgress("renaming file %r to %r" % (self.tmpname, self.officialname))
			os.rename(self.tmpname, self.officialname)
			self.logLoop("cached %r as %r (%d bytes)" % (self.url, self.officialname, datasize))

	if __name__=="__main__":
		sisyphus.execute(Fetch())
"""


import sys, os, traceback, errno, pprint, datetime

from ll import url


__docformat__ = "reStructuredText"


def _formattime(timestamp):
	"""
	Format :var:`timestamp` into a string.
	"""
	return timestamp.strftime("%d/%b/%Y %H:%M:%S")


def _formattimedelta(timedelta):
	"""
	Format :var:`timedelta` into a string.
	"""
	rest = timedelta.seconds
	(rest, secs) = divmod(rest, 60)
	(rest, mins) = divmod(rest, 60)
	rest += timedelta.days*24
	return "%d:%02d:%06.3f" % (rest, mins, secs+timedelta.microseconds/1000000.)


class LogFile:
	"""
	A log file. All lines written to the file will be prepended with a time stamp.
	"""
	def __init__(self, name, mode="a", buffering=True, encoding="iso-8859-1"):
		"""
		Create a new log file (which will be opened on the first write).
		Arguments are:

		:var:`name`
			The filename (either as a string or a :class:`ll.url.URL` instance).

		:var:`mode`
			The mode for opening the file (should be ``"w"`` or ``"a"``).

		:var:`buffering`
			The buffering for the file (``0`` is unbuffered, ``1`` is line
			buffered, any other integer specifies the buffersize).

		:var:`encoding`
			The encoding to use for the strings written to the file.
		"""
		self.starttime = datetime.datetime.now()
		if not isinstance(name, url.URL):
			name = url.File(name)
		self.name = name
		self.mode = mode
		self.buffering = buffering
		self.encoding = encoding
		self.file = None

	def __open(self):
		if self.file is None:
			self.file = open(self.name.local(), self.mode, self.buffering)

	def write(self, *texts):
		"""
		Write :var:`texts` to the log file.
		"""
		now = datetime.datetime.now()
		pid = os.getpid()
		prefix = "[pid=%d][%s]=[t+%s]" % (pid, _formattime(now), _formattimedelta(now-self.starttime))

		self.__open()
		for text in texts:
			if isinstance(text, str):
				pass
			elif isinstance(text, unicode):
				text = text.encode(self.encoding, "replace")
			elif isinstance(text, Exception):
				tb = "\n" + "".join(traceback.format_tb(sys.exc_info()[-1]))
				text = "%s%s: %s" % (tb, text.__class__.__name__, text)
			else:
				text = pprint.pformat(text)
			lines = text.splitlines()
			if lines and not len(lines[-1]):
				del lines[-1]
			for line in lines:
				self.file.write("%s %s\n" % (prefix, line))


class Job(object):
	"""
	A Job object executes a task once.
	
	The job announces its presence (and its process id) in a file that is stored
	in the :dir:`~/run` directory. Logs will be created in the :dir:`~/log`
	directory (This can be changes by deriving new subclasses).

	To use this class, derive your own class from it and overwrite the
	:meth:`execute` method.
	"""

	pidfilenametemplate = "~/run/%s.pid"
	loopfilenametemplate = "~/log/%s_loop.log"
	errorfilenametemplate = "~/log/%s_error.log"
	progressfilenametemplate = "~/log/%s_progress.log"

	def __init__(self, maxruntime=0, name=None, raiseerrors=False, printkills=False):
		"""
		Create a new job. Arguments are:

		:var:`maxruntime`: : integer
			The maximum allowed runtime in seconds for this job;

		:var:`name`: : string or ``None``
			The name to be used for the log files. If ``None``, the name of the
			class will be used;

		:var:`raiseerrors`: : bool
			should exceptions that occur during the excution of the job be raised
			(which results in a output to the terminal, or an email from the cron
			daemon);

		:var:`printkills`: : bool
			should the fact that a previous job was killed, be printed on stdout
			(resulting in a mail from the cron daemon)
		"""
		self.starttime = datetime.datetime.now()
		if not isinstance(maxruntime, datetime.timedelta):
			maxruntime = datetime.timedelta(seconds=maxruntime)
		self.maxruntime = maxruntime
		self.name = name or self.__class__.__name__
		self.raiseerrors = raiseerrors
		self.printkills = printkills
		self.pidfilewritten = False
		self.pidfilename = url.File(self.pidfilenametemplate % self.name)
		self.loopLogfile = LogFile(self.loopfilenametemplate % self.name)
		self.errorLogfile = LogFile(self.errorfilenametemplate % self.name)
		self.progressLogfile = LogFile(self.progressfilenametemplate % self.name, mode="w")

	def __writepid(self):
		"""
		Create the file containing the pid of the current process.
		"""
		if not self.pidfilewritten:
			file = self.pidfilename.openwrite()
			file.write(str(os.getpid()))
			file.close()
			self.pidfilewritten = True

	def __killpid(self):
		"""
		Delete the pid file.
		"""
		if self.pidfilewritten:
			self.pidfilename.remove()
			self.pidfilewritten = False

	def logLoop(self, *texts):
		"""
		Log the message texts to the loop and progress log. (The call to
		:meth:`logLoop` should be the last statement in the :meth:`execute`
		method.)
		"""
		self.loopLogfile.write(*texts)
		self.progressLogfile.write(*texts)

	def logProgress(self, *texts):
		"""
		Log the message texts to the progress log.
		"""
		self.progressLogfile.write(*texts)

	def logErrorOnly(self, *texts):
		"""
		Log the error to the error log. :var:`texts` may be strings or exception
		objects.
		"""
		self.errorLogfile.write(*texts)

	def logError(self, error):
		"""
		Log the error to the error log and the progress log. :var:`texts` may be
		strings or exception objects.
		"""
		self.progressLogfile.write(error)
		self.errorLogfile.write(error)

	def execute(self):
		"""
		Execute the job once. At the end of the job you should write one line to
		the loop log. Overwrite in subclasses.
		"""
		self.logLoop("done")

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
		try: # is there a pid file from a running job?
			file = open(self.pidfilename.local(), "r")
		except IOError, exc: # no pid file => the job has been finished without problems
			if exc[0] == errno.ENOENT: # file not found
				self.__writepid()
				self.logProgress("no previous job running; here we go")
			else:
				raise
		else:
			lastmodified = datetime.datetime.fromtimestamp(os.fstat(file.fileno()).st_mtime)
			try:
				pid = int(file.read())
			except ValueError:
				# disk may have been full
				file.close()
				self.__writepid()
				self.logProgress("ignoring bogus pid file %s (invalid content)" % self.pidfilename)
			else:
				file.close()
				# Check if this process really exists, if not continue as if the pid file wasn't there
				try:
					os.kill(pid, 0)
				except OSError, exc:
					if exc[0] != errno.ESRCH:
						raise
					self.__writepid()
					msg = "ignoring bogus pid file %s (process with pid %d doesn't exist)" % (self.pidfilename, pid)
					self.logError(msg)
				else:
					if self.maxruntime and self.starttime-lastmodified > self.maxruntime: # the job is to old, so it probably hangs => kill it
						try:
							os.kill(pid, 9)
						except OSError, exc:
							if exc[0] != errno.ESRCH: # there was no process
								raise
						self.__writepid()
						msg = "killed previous job running with pid %d (ran %s seconds; %s allowed); here we go" % (pid, _formattimedelta(self.starttime-lastmodified), _formattimedelta(self.maxruntime))
						self.logError(msg)
						if self.printkills:
							print msg
					else:
						msg = "Job still running (for %s; %s allowed; started on %s) with pid %d (according to %s)" % (_formattimedelta(self.starttime-lastmodified), _formattimedelta(self.maxruntime), _formattime(lastmodified), pid, self.pidfilename)
						self.logErrorOnly(msg)
						return # Return without calling :meth:`execute`

		try:
			self.execute()
		except (Exception, KeyboardInterrupt), exc:
			self.logError(exc) # log the error
			self.logLoop("failed with %s(%s)" % (exc.__class__.__name__, exc)) # log the error to the loop log too, because the job probably didn't have a chance to do it.
			self.failed()
			if self.raiseerrors or isinstance(exc, KeyboardInterrupt): # Really exit
				self.__killpid()
				raise
		self.__killpid() # finished => remove the pid file


def execute(*jobs):
	"""
	Execute several jobs.

	Items in :var:`jobs` are job objects, that will be executed sequentially.
	"""
	for job in jobs:
		job.handleexecution()
