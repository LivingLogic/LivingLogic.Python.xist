#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2000-2008 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2000-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See __init__.py for the license


r"""
<p><mod>ll.sisyphus</mod> simplifies running Python stuff as cron jobs.</p>

<p>There will be no more than one sisyphus job of a certain name
running at every given time. When the job is already running
and a second is started, the second one will quit immediately
if the first one hasn't exceeded its maximum allowed lifetime
yet. If it has exceeded the allowed lifetime the first job
will be killed and the second will start running.</p>

<p>In addition to that, logging features are provided.</p>

<p>To use this module, you must derive your own
class from <pyref class="Job"><class>Job</class></pyref> and implement
the <pyref class="Job" method="execute"><meth>execute</meth></pyref> method.</p>

<p>The job announces its presence (and its process id) in a file that
is stored in the <dirname>~/run</dirname> directory. Logs will be created in the
<dirname>~/log</dirname> directory (This can be changes by deriving new subclasses).</p>

<p>There are three log files:</p>
<dl>
<dt><filename>~/log/<rep>jobname</rep>_progress.log</filename></dt>
<dd>The progress of one job execution is logged here.
This log file will be truncated at the start of every execution,
so you can be rather verbose.
Use the <pyref class="Job" method="logProgress"><meth>logProgress</meth></pyref>
method for writing to this log file.</dd>
<dt><filename>~/log/<rep>jobname</rep>_loop.log</filename></dt>
<dd>One log line may be appended to the log after every job execution.
Use the <pyref class="Job" method="logLoop"><meth>logLoop</meth></pyref>
method for this.</dd>
<dt><filename>~/log/<rep>jobname</rep>_error.log</filename></dt>
<dd>Here exceptions happening during the execution of a job
will be logged. This is done via the <pyref class="Job" method="logError"><meth>logError</meth></pyref>
method with can be used for reporting other exception conditions apart
from exceptions.</dd>
</dl>

<p>To execute a job, use the function
<pyref function="execute"><func>execute</func></pyref>.</p>

<section><h>Example</h>
<p>The following example illustrates the use of this module:</p>
<example>
<h>Complete example showing the use of sisyphus</h>
<prog>
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
		self.logProgress("writing file %r (%d bytes)" %
			(self.tmpname, datasize))
		open(self.tmpname, "wb").write(data)
		self.logProgress("renaming file %r to %r" %
			(self.tmpname, self.officialname))
		os.rename(self.tmpname, self.officialname)
		self.logLoop("cached %r as %r (%d bytes)" %
			(self.url, self.officialname, datasize))

if __name__=="__main__":
	sisyphus.execute(Fetch())
</prog>
</example>
</section>
"""


import sys, os, traceback, errno, pprint, datetime

from ll import url


__docformat__ = "xist"


def _formattime(timestamp):
	"""
	format <arg>timestamp</arg> into a string.
	"""
	return timestamp.strftime("%d/%b/%Y %H:%M:%S")


def _formattimedelta(timedelta):
	"""
	format <arg>timedelta</arg> into a string.
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
		<p>create a new log file (which will be opened on the first write). Arguments are:</p>
		<ul>
		<li><arg>name</arg>: the filename (either as a string or a
		<pyref module="ll.url" class="URL"><class>ll.url.URL</class></pyref> instance).</li>
		<li><arg>mode</arg>: The mode for opening the file (should be <lit>"w"</lit> or <lit>"a"</lit>)</li>
		<li><arg>buffering</arg>: the buffering for the file (<lit>0</lit> is unbuffered, <lit>1</lit> is line buffered, any other integer specifies the buffersize)</li>
		<li><arg>encoding</arg>: the encoding to use for the strings written to the file</li>
		</ul>
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
		write <arg>texts</arg> to the log file.
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
	<p>A Job object executes a task once.</p>
	
	<p>The job announces its presence (and its process id) in a file that
	is stored in the <dirname>~/run</dirname> directory. Logs will be created in
	the <dirname>~/log</dirname> directory (This can be changes by deriving
	new subclasses).</p>

	<p>To use this class, derive your own class from it and overwrite
	the <pyref method="execute">execute method</pyref>.</p>
	"""

	pidfilenametemplate = "~/run/%s.pid"
	loopfilenametemplate = "~/log/%s_loop.log"
	errorfilenametemplate = "~/log/%s_error.log"
	progressfilenametemplate = "~/log/%s_progress.log"

	def __init__(self, maxruntime=0, name=None, raiseerrors=False, printkills=False):
		"""
		<p>create a new job. Arguments are:</p>

		<ul>
		<li><arg>maxruntime</arg>: the maximum allowed runtime in seconds for this job;</li>
		<li><arg>name</arg>: the name to be used for the log files. If <lit>None</lit>,
		the name of the class will be used;</li>
		<li><arg>raiseerrors</arg>: should exceptions that occur during the excution of the
		job be raised (which results in a output to the terminal, or an email
		from the cron daemon);</li>
		<li><arg>printkills</arg>: should the fact that a previous job was killed,
		be printed on stdout (resulting in a mail from the cron daemon)</li>
		</ul>
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
		creates the file containing the pid of the current process
		"""
		if not self.pidfilewritten:
			file = self.pidfilename.openwrite()
			file.write(str(os.getpid()))
			file.close()
			self.pidfilewritten = True

	def __killpid(self):
		"""
		deletes the pid file
		"""
		if self.pidfilewritten:
			self.pidfilename.remove()
			self.pidfilewritten = False

	def logLoop(self, *texts):
		"""
		log the message texts to the loop and progress log.
		(The call to <meth>logLoop</meth> should be the last statement
		in the <pyref method="execute"><meth>execute</meth></pyref> method.)
		"""
		self.loopLogfile.write(*texts)
		self.progressLogfile.write(*texts)

	def logProgress(self, *texts):
		"""
		log the message texts to the progress log
		"""
		self.progressLogfile.write(*texts)

	def logErrorOnly(self, *texts):
		"""
		log the error to the error log.
		error may be a string or an exception object.
		"""
		self.errorLogfile.write(*texts)

	def logError(self, error):
		"""
		log the error to the error log and the progress log.
		error may be a string or an exception object.
		"""
		self.progressLogfile.write(error)
		self.errorLogfile.write(error)

	def execute(self):
		"""
		Execute the job once.
		At the end of the job you should write one line to the loop log.
		Overwrite in subclasses.
		"""
		self.logLoop("done")

	def failed(self):
		"""
		Called when running the job generated an exception.
		Overwrite in subclasses, to e.g. rollback your database transactions.
		"""
		pass

	def handleexecution(self):
		"""
		handles executing the job including handling of duplicate or hanging jobs.
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
			pid = int(file.read())
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
					return # Return without calling execute()

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
	<p>Execute several jobs.</p>

	<p>Items in <arg>jobs</arg> are job objects, that will be executed sequentially.</p>
	"""
	for job in jobs:
		job.handleexecution()
