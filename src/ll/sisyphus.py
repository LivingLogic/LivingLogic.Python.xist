# -*- coding: utf-8 -*-
# cython: language_level=3

## Copyright 2000-2013 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2000-2013 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`ll.sisyphus` simplifies running Python stuff as cron jobs.

There will be no more than one sisyphus job of a certain name running at any
given time. A job has a maximum allowed runtime. If this maximum is exceeded,
the job will kill itself. In addition to that, job execution can be logged and
in case of job failure an email can be sent.

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
			self.log("writing file {!r} ({:,} bytes)".format(self.tmpname, datasize))
			open(self.tmpname, "wb").write(data)
			self.log("renaming file {!r} to {!r}".format(self.tmpname, self.officialname))
			os.rename(self.tmpname, self.officialname)
			return "cached {!r} as {!r} ({:,} bytes)".format(self.url, self.officialname, datasize)

	if __name__=="__main__":
		sisyphus.executewithargs(Fetch())

You will find the log files for this job in ``~/ll.sisyphus/ACME.FooBar/Fetch/``.
"""


import sys, os, signal, fcntl, codecs, traceback, errno, pprint, datetime, re, contextlib, argparse, tokenize, json, smtplib
from email.mime import text, application, multipart
from email import encoders

from ll import url, ul4c, misc


__docformat__ = "reStructuredText"


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

		``email``
			This tag will be added for all log messages related to sending the
			failure report email.

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
		The name of the job itself (defaulting to the name of the class if none
		is given).

	``identifier`` : :option:`--identifier`
		An additional identifier that will be added to the failure report email.

	``argdescription`` : No command line equivalent
		Description for help message of the command line argument parser.

	``fromemail`` : :option:`--fromemail`
		The sender email address for the failure report email.

		This email will only be sent if the options :option:`--fromemail`,
		:option:`--toemail` and :option:`--smtphost` are set (and any errors
		occured).

	``toemail`` : :option:`--toemail`
		An email address where an email will be sent in case of a failure.

	``smtphost`` : :option:`--smtphost`
		The SMTP server to be used for sending the failure report email.

	``smtpport`` : :option:`--smtpport`
		The port number used for the connection to the SMTP server.

	``maxtime`` : :option:`-m` or :option:`--maxtime`
		Maximum allowed runtime for the job (as the number of seconds). If the job
		runs longer than that it will kill itself.

	``fork`` : :option:`--fork`
		Forks the process and does the work in the child process. The parent
		process is responsible for monitoring the maximum runtime (this is the
		default). In non-forking mode the single process does both the work and
		the runtime monitoring.

	``noisykills`` : :option:`--noisykills`
		Should a message be printed/a failure email be sent when the maximum
		runtime is exceeded?

	``notify`` : :option:`-n` or :option:`--notify`
		Should a notification be issued to the OS X Notification center?
		(done via terminal-notifier__).

		__ https://github.com/alloy/terminal-notifier

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

	``encoding`` : :option:`--encoding`
		The encoding to be used for the logfile.

	``errors`` : :option:`--errors`
		Encoding error handler name (goes with ``encoding``)

	Command line arguments take precedence over instance attributes (if
	:func:`executewithargs` is used) and those take precedence over class
	attributes.
	"""

	projectname = None
	jobname = None

	argdescription = "execute the job"

	fromemail = None
	toemail = None
	smtphost = None
	smtpport = 0

	identifier = None

	maxtime = 5 * 60

	fork = True

	noisykills = False
	notify = False

	logfilename = "~/ll.sisyphus/<?print job.projectname?>/<?print job.jobname?>/<?print format(job.starttime, '%Y-%m-%d-%H-%M-%S-%f')?>.sisyphuslog"
	loglinkname = "~/ll.sisyphus/<?print job.projectname?>/<?print job.jobname?>/current.sisyphuslog"

	log2file = True
	log2stdout = False
	log2stderr = False

	formatlogline = r"""
		[<?print time?>]
		=
		[t+<?print time-job.starttime?>]
		<?for task in tasks?>
			<?print " :: "?>
			<?code desc = [task.type, task.name]?>
			<?code desc = [d for d in desc if d]?>
			<?if desc?>
				<?print " ".join(desc)?>
			<?end if?>
			<?if not isnone(task.index)?>
				<?if desc?> <?end if?>
				(
				<?print task.index+1?>
				<?if not isnone(task.count)?>
					/<?print task.count?>
				<?end if?>
				)
			<?elif not desc?>
				?
			<?end if?>
		<?end for?>
		<?if tags?>
			<?print " :: "?>
			<?for tag in tags?>
				{<?print tag?>}
			<?end for?>
		<?end if?>
		<?print " >> "?>
		<?print line?>
	"""

	formatemailsubject = r"""
		<?print job.projectname?>/<?print job.jobname?> failed for <?print sysinfo.user_name?>@<?print sysinfo.host_fqdn?> (<?print sysinfo.host_ip?>)<?if errors?> with <?print len(errors)?> errors<?end if?>
	"""

	formatemailbodytext = r"""
		Project:    <?print job.projectname?><?print "\n"?>
		Job:        <?print job.jobname?><?print "\n"?>
		Identifier: <?print job.identifier or "n/a"?><?print "\n"?>
		Script:     <?print sysinfo.script_name?><?print "\n"?>
		User:       <?print sysinfo.user_name?><?print "\n"?>
		Python:     <?print sysinfo.python_executable?><?print "\n"?>
		Version:    <?print sysinfo.python_version?><?print "\n"?>
		Host:       <?print sysinfo.host_fqdn?><?print "\n"?>
		IP:         <?print sysinfo.host_ip?><?print "\n"?>
		PID:        <?print sysinfo.pid?><?print "\n"?>
		Start:      <?print job.starttime?><?print "\n"?>
		End:        <?print job.endtime?><?print "\n"?>
		Duration:   <?print job.endtime-job.starttime?><?print "\n"?>
		Errors:     <?print len(errors)?><?print "\n"?>

		<?for (i, error) in enumerate(errors, 1)?>
			<?print "-"*80?><?print "\n"?>
			Error:     #<?print i?><?print "\n"?>
			<?for task in error.tasks?>
				Task:      <?code desc = [task.type, task.name]?>
				<?code desc = [d for d in desc if d]?>
				<?if desc?>
					<?print " ".join(desc)?>
				<?end if?>
				<?if not isnone(task.index)?>
					<?if desc?> <?end if?>
					(
					<?print task.index+1?>
					<?if not isnone(task.count)?>
						/<?print task.count?>
					<?end if?>
					)
				<?elif not desc?>
					?
				<?end if?>
				<?print "\n"?>
			<?end for?>
			<?if error.tasks?>
				<?code starttime = error.tasks[-1].starttime?>
				<?code endtime = error.tasks[-1].endtime?>
				Start:     <?print starttime?><?print "\n"?>
				End:       <?print endtime?><?print "\n"?>
				Duration:  <?print endtime-starttime?><?print "\n"?>
			<?end if?>
			Type:      <?print error.error?><?print "\n"?>
			<?if error.message?>
				Message:   <?print error.message?><?print "\n"?>
			<?end if?>
			Traceback:<?print "\n"?>
			<?print error.traceback.strip("\n")?><?print "\n"?>
		<?end for?>
	"""

	formatemailbodyhtml = r"""
		<?note Subtemplates?>
		<?def table?>
			<table>
				<?for (label, value) in data?>
					<tr><th style="text-align:right;"><?print label?></th><td style="padding-left: 1em;"><?printx value?></td></tr>
				<?end for?>
			</table>
		<?end def?>
		<?def tasklabel?>
			<?code desc = [task.type, task.name]?>
			<?code desc = [d for d in desc if d]?>
			<?if desc?>
				<?print " ".join(desc)?>
			<?end if?>
			<?if not isnone(task.index)?>
				<?if desc?> <?end if?>
				(
				<?print task.index+1?>
				<?if not isnone(task.count)?>
					/<?print task.count?>
				<?end if?>
				)
			<?elif not desc?>
				?
			<?end if?>
		<?end def?>


		<?xml version='1.0' encoding='utf-8'?>
		<html>
			<head>
				<title><?printx job.projectname?>/<?printx job.jobname?> on <?printx sysinfo.user_name?>@<?printx sysinfo.host_fqdn?> (<?printx sysinfo.host_ip?>) failed</title>
			</head>
			<body style="font-family: monospace;">
				<h1><?printx job.projectname?>/<?printx job.jobname?> on <?printx sysinfo.user_name?>@<?printx sysinfo.host_fqdn?> (<?printx sysinfo.host_ip?>) failed</h1>
				<?code data = [
					["Project", job.projectname],
					["Job", job.jobname],
					["Identifier", job.identifier or 'n/a'],
					["Script", sysinfo.script_name],
					["User", sysinfo.user_name],
					["Python", sysinfo.python_executable],
					["Version", sysinfo.python_version],
					["Host", sysinfo.host_fqdn],
					["IP", sysinfo.host_ip],
					["PID", sysinfo.pid],
					["Start", job.starttime],
					["End", job.endtime],
					["Duration", job.endtime-job.starttime],
					["Errors", len(errors)],
				]?>
				<?code table.render(data=data)?>
				<?for (i, error) in enumerate(errors, 1)?>
					<hr/>
					<h2>Error #<?print i?></h2>
					<?code data = [["Task", tasklabel.renders(task=task)] for task in error.tasks]?>
					<?if error.tasks?>
						<?code starttime = error.tasks[-1].starttime?>
						<?code endtime = error.tasks[-1].endtime?>
						<?code data.append(["Start", starttime])?>
						<?code data.append(["End", endtime])?>
						<?code data.append(["Duration", endtime-starttime])?>
					<?end if?>
					<?code data.append(["Type", error.error])?>
					<?if error.message?>
						<?code data.append(["Message", error.message])?>
					<?end if?>
					<?code table.render(data=data)?>
					<h3>Traceback<h3>
					<pre style="font-weight:normal;">
						<?printx error.traceback.strip("\n")?>
					</pre>
				<?end for?>
			</pre>
		</body>
	</head>
	"""

	keepfilelogs = 30

	encoding = "utf-8"
	errors = "strict"

	ul4attrs = {"sysinfo", "projectname", "jobname", "tasksep", "maxtime", "starttime", "endtime"}

	def execute(self):
		"""
		Execute the job once. The return value is a one line summary of what the
		job did. Overwrite in subclasses.
		"""
		return "done"

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
		p = argparse.ArgumentParser(description=self.argdescription, epilog="For more info see http://www.livinglogic.de/Python/sisyphus/")
		p.add_argument("-p", "--projectname", dest="projectname", metavar="NAME", help="The name of the project this job belongs to (default: %(default)s)", default=self.projectname)
		p.add_argument("-j", "--jobname", dest="jobname", metavar="NAME", help="The name of the job (default: %(default)s)", default=self.jobname if self.jobname is not None else self.__class__.__name__)
		p.add_argument(      "--fromemail", dest="fromemail", metavar="ADDRESS", help="The sender email address for the failure report email (default: %(default)s)", default=self.fromemail)
		p.add_argument(      "--toemail", dest="toemail", metavar="ADDRESS", help="An email address where failure reports will be sent (default: %(default)s)", default=self.toemail)
		p.add_argument(      "--smtphost", dest="smtphost", metavar="HOSTNAME", help="The SMTP server to use for sending the failure report email (default: %(default)s)", default=self.smtphost)
		p.add_argument(      "--smtpport", dest="smtpport", metavar="PORT", help="The port number used for the connection to the SMTP server (default: %(default)s)", type=int, default=self.smtpport)
		p.add_argument(      "--identifier", dest="identifier", metavar="IDENTIFIER", help="Additional identifier that will be added to the failure report mail (default: %(default)s)", default=self.identifier)
		p.add_argument("-m", "--maxtime", dest="maxtime", metavar="SECONDS", help="Maximum number of seconds the job is allowed to run (default: %(default)s)", type=int, default=self.getmaxtime_seconds())
		p.add_argument(      "--fork", dest="fork", help="Fork the process and do the work in the child process? (default: %(default)s)", action=misc.FlagAction, default=self.fork)
		p.add_argument("-f", "--log2file", dest="log2file", help="Should the job log into a file? (default: %(default)s)", action=misc.FlagAction, default=self.log2file)
		p.add_argument("-o", "--log2stdout", dest="log2stdout", help="Should the job log to stdout? (default: %(default)s)", action=misc.FlagAction, default=self.log2stdout)
		p.add_argument("-e", "--log2stderr", dest="log2stderr", help="Should the job log to stderr? (default: %(default)s)", action=misc.FlagAction, default=self.log2stderr)
		p.add_argument(      "--keepfilelogs", dest="keepfilelogs", metavar="DAYS", help="Number of days log files are kept (default: %(default)s)", type=float, default=self.keepfilelogs)
		p.add_argument(      "--encoding", dest="encoding", metavar="ENCODING", help="Encoding for the log file (default: %(default)s)", default=self.encoding)
		p.add_argument(      "--errors", dest="errors", metavar="METHOD", help="Error handling method for encoding errors in log texts (default: %(default)s)", default=self.errors)
		p.add_argument(      "--noisykills", dest="noisykills", help="Should a message be printed/failure email be sent if the maximum runtime is exceeded? (default: %(default)s)", action=misc.FlagAction, default=self.noisykills)
		p.add_argument("-n", "--notify", dest="notify", help="Should a notification be issued to the OS X notification center? (default: %(default)s)", action=misc.FlagAction, default=self.notify)
		return p

	def parseargs(self, args=None):
		"""
		Use the parser returned by :meth:`argparser` to parse the argument
		sequence :obj:`args`, modify :obj:`self` accordingly and return
		the result of the parsers :meth:`parse_args` call.
		"""
		p = self.argparser()
		args = p.parse_args(args)
		self.projectname = args.projectname
		self.jobname = args.jobname
		self.fromemail = args.fromemail
		self.toemail = args.toemail
		self.smtphost = args.smtphost
		self.smtpport = args.smtpport
		self.identifier = args.identifier
		self.maxtime = args.maxtime
		self.fork = args.fork
		self.noisykills = args.noisykills
		self.log2file = args.log2file
		self.log2stdout = args.log2stdout
		self.log2stderr = args.log2stderr
		self.keepfilelogs = datetime.timedelta(days=args.keepfilelogs)
		self.encoding = args.encoding
		self.errors = args.errors
		self.notify = args.notify
		return args

	def getmaxtime(self):
		if isinstance(self.maxtime, datetime.timedelta):
			return self.maxtime
		else:
			return datetime.timedelta(seconds=self.maxtime)

	def getmaxtime_seconds(self):
		if isinstance(self.maxtime, datetime.timedelta):
			return int(self.maxtime.total_seconds())
		else:
			return self.maxtime

	def _alarm_fork(self, signum, frame):
		os.kill(self.killpid, signal.SIGTERM) # Kill our child
		maxtime = self.getmaxtime()
		self.endtime = datetime.datetime.now()
		if self.noisykills:
			try:
				raise RuntimeError("maximum runtime {} exceeded in forked child (pid {})".format(maxtime, misc.sysinfo.pid))
			except Exception as exc:
				self._exceptions.append((self._tasks[:], exc))
			self._reporterrors()
		if self._logfile is not None:
			self.log.sisyphus.result.kill("Terminated child after {}".format(maxtime))
			self._logfile.close()
		os._exit(1)

	def _alarm_nofork(self, signum, frame):
		self._prefix = ""
		maxtime = self.getmaxtime()
		self.endtime = datetime.datetime.now()
		if self.noisykills:
			try:
				raise RuntimeError("maximum runtime {} exceeded (pid {})".format(maxtime, misc.sysinfo.pid))
			except Exception as exc:
				self._exceptions.append((self._tasks[:], exc))
			self._reporterrors()
		if self._logfile is not None:
			self.log.sisyphus.result.kill("Terminated after {}".format(maxtime))
			self._logfile.close()
		os._exit(1)

	def _handleexecution(self):
		"""
		Handle executing the job including handling of duplicate or hanging jobs.
		"""
		self._prefix = ""
		self._tasks = []
		self._exceptions = []

		# Obtain a lock on the script file to make sure we're the only one running
		with open(misc.sysinfo.script_name, "rb") as f:
			try:
				fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError as exc:
				if exc.errno != errno.EWOULDBLOCK: # some other error
					raise
				# The previous invocation of the job is still running
				return # Return without calling :meth:`execute`

			# we were able to obtain the lock, so we are the only one running
			self.starttime = datetime.datetime.now()
			self.endtime = None

			self._getscriptsource() # Get source code
			self._getcrontab() # Get crontab
			self.lineno = 1 # Current line number
			self.log = Tag(self._log) # Create tagged logger
			self._formatlogline = ul4c.Template(self.formatlogline, "formatlogline", keepws=False) # Log line formatting template
			self._formatemailsubject = ul4c.Template(self.formatemailsubject, "formatemailsubject", keepws=False) # Email subject formatting template
			self._formatemailbodytext = ul4c.Template(self.formatemailbodytext, "formatemailbodytext", keepws=False) # Email body formatting template (plain text)
			self._formatemailbodyhtml = ul4c.Template(self.formatemailbodyhtml, "formatemailbodyhtml", keepws=False) # Email body formatting template (HTML)
			self._createlog() # Create log file and link

			self.log.sisyphus.init("{} (max time {}; pid {})".format(misc.sysinfo.script_name, self.getmaxtime(), misc.sysinfo.pid))

			if self.fork: # Forking mode?
				# Fork the process; the child will do the work; the parent will monitor the maximum runtime
				self.killpid = pid = os.fork()
				if pid: # We are the parent process
					# set a signal to kill the child process after the maximum runtime
					signal.signal(signal.SIGALRM, self._alarm_fork)
					signal.alarm(self.getmaxtime_seconds())
					os.waitpid(pid, 0) # Wait for the child process to terminate
					return # Exit normally
				self.log.sisyphus.init("forked worker child (child pid {})".format(os.getpid()))
			else: # We didn't fork
				# set a signal to kill ourselves after the maximum runtime
				signal.signal(signal.SIGALRM, self._alarm_nofork)
				signal.alarm(self.getmaxtime_seconds())

			self.notifystart()
			try:
				with url.Context():
					result = self.execute()
				self._cleanupoldlogs() # Clean up old logfiles
			except BaseException as exc:
				self.endtime = datetime.datetime.now()
				# log the error to the logfile, because the job probably didn't have a chance to do it
				self._exceptions.append(([], exc))
				self.log.sisyphus.exc(exc)
				result = "failed with {}".format(self._exc(exc))
				self.log.sisyphus.result.fail(result)
				self.failed()
				# Make sure that exceptions at the top level get propagated (this mean that they might be reported twice)
				raise
			else:
				self.endtime = datetime.datetime.now()
				# log the result
				if self._exceptions:
					self.log.sisyphus.result.errors(result)
				else:
					self.log.sisyphus.result.ok(result)
			finally:
				# Send the email before closing the logfile, so that if sending the email fails, it will be logged to the file
				self._reporterrors()
				self.notifyfinish(result)
				if self._logfile is not None:
					self._logfile.close()
				fcntl.flock(f, fcntl.LOCK_UN | fcntl.LOCK_NB)
			if self.fork:
				os._exit(0)

	def strtimedelta(self, delta):
		"""
		Return a nicely formatted string for the :class:`datetime.timedelta`
		value :obj:`delta`. :obj:`delta` may also be :const:`None` in with case
		``"0"`` will be returned.
		"""
		if delta is None:
			return "0"
		rest = delta.seconds

		(rest, secs) = divmod(rest, 60)
		(rest, mins) = divmod(rest, 60)
		rest += delta.days*24

		secs += delta.microseconds/1000000.
		if rest:
			return "{:d}:{:02d}:{:06.3f}h".format(rest, mins, secs)
		elif mins:
			return "{:02d}:{:06.3f}m".format(mins, secs)
		else:
			return "{:.3f}s".format(secs)

	def notifystart(self):
		if self.notify:
			cmd = [
				"/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier",
				"-remove",
				misc.sysinfo.script_name,
			]

			import subprocess
			with open("/dev/null", "wb") as f:
				status = subprocess.call(cmd, stdout=f)

	def notifyfinish(self, result):
		if self.notify:
			cmd = [
				"/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier",
				"-title",
				"{} {}".format(self.projectname, self.jobname),
				"-subtitle",
				"finished after {}".format(self.strtimedelta(self.endtime-self.starttime)),
				"-message",
				result,
				"-group",
				misc.sysinfo.script_name,
			]

			import subprocess
			with open("/dev/null", "wb") as f:
				status = subprocess.call(cmd, stdout=f)

	@contextlib.contextmanager
	def prefix(self, prefix):
		"""
		:meth:`prefix` is a context manager. For the duration of the ``with`` block
		:obj:`prefix` will be prepended to all log lines. :meth:`prefix` calls can
		be nested.
		"""
		oldprefix = self._prefix
		self._prefix += prefix
		try:
			yield
		finally:
			self._prefix = oldprefix

	@contextlib.contextmanager
	def task(self, type=None, name=None, index=None, count=None, errors="raise", logbegin=False, logend=False):
		"""
		:meth:`task` is a context manager and can be used to specify subtasks.

		Arguments have the following meaning:

		``type`` : string or ``None``
			The type of the task.

		``name`` : string or ``None``
			The name of the task.

		``index`` : integer or ``None``
			If this task is one in a sequence of similar tasks, ``index`` should
			be the index of this task, i.e. the first task of this type has
			``index==0``, the second one ``index==1`` etc.

		``count`` : integer or ``None``
			If this task is one in a sequence of similar tasks and the total number
			of tasks is known, ``count`` should be the total number of tasks.

		``errors`` : string
			Specifies how exceptions occuring in the subtask will be handled:

			``raise``
				Raise the exception (which normally aborts the job, excepti when
				an outer task swallows it)

			``ignore``
				Ignore the exception (but of course the rest of the subtask wills
				*not* be executed)

			``log``
				Log the exception.

			``logemail``
				Log the exception and add it to the failure report email.

			``email``
				Add the exception to the failure report email.

		``logbegin`` : bool
			Should a line be logged at the start of the task?

		``logend`` : bool
			Should a line be logged at the end of the task?
		"""
		task = Task(type=type, name=name, index=index, count=count)
		self._tasks.append(task)
		if logbegin:
			self.log("begin")
		try:
			yield
		except BaseException as exc:
			task.fail()
			if errors == "raise":
				raise
			elif errors == "ignore":
				pass
			elif errors == "log":
				self.log(exc)
			elif errors == "logemail":
				self._exceptions.append((self._tasks[:], exc))
				self.log(exc)
			elif errors == "email":
				self._exceptions.append((self._tasks[:], exc))
			else:
				raise ValueError("unknown value for errors parameter: {!r}".format(errors))
			if logend:
				self.log("failed after {}".format(task.endtime-task.starttime))
		else:
			task.end()
			if logend:
				fmt = "done after {}" if logbegin else "done in {}"
				self.log(fmt.format(task.endtime-task.starttime))
		finally:
			self._tasks.pop()

	def _log(self, tags, *texts):
		"""
		Log items in :obj:`texts` to the log file using :obj:`tags` as the list
		of tags.
		"""
		if self.log2file or self.log2stdout or self.log2stderr:
			timestamp = datetime.datetime.now()
			for text in texts:
				if isinstance(text, BaseException):
					if "exc" not in tags:
						tags += ("exc",)
					tb = "".join(traceback.format_tb(text.__traceback__))
					text = "{}\n{}".format(tb, self._exc(text))
				elif not isinstance(text, str):
					text = pprint.pformat(text)
				lines = text.splitlines()
				if lines and not lines[-1].strip():
					del lines[-1]
				for line in lines:
					text = self._formatlogline.renders(line=self._prefix+line, time=timestamp, tags=tags, tasks=self._tasks, sysinfo=misc.sysinfo, job=self)
					if self.log2file:
						self._logfile.write(text)
						self._logfile.write("\n")
						self._logfile.flush()
					if self.log2stdout:
						sys.stdout.write(text)
						sys.stdout.write("\n")
						sys.stdout.flush()
					if self.log2stderr:
						sys.stderr.write(text)
						sys.stderr.write("\n")
						sys.stderr.flush()
					self.lineno += 1

	def _getscriptsource(self):
		"""
		Reads the source code of the script into ``self.source``.
		"""
		scriptname = misc.sysinfo.script_name.rstrip("c")
		try:
			encoding = tokenize.detect_encoding(open(scriptname, "rb").readline)[0]
			with open(scriptname, "r", encoding=encoding, errors="replace") as f:
				self.source = f.read()
		except IOError: # Script might have called ``os.chdir()`` before
			self.source = None

	def _getcrontab(self):
		"""
		Reads the current crontab into ``self.crontab``.
		"""
		with os.popen("crontab -l 2>/dev/null") as f:
			self.crontab = f.read()

	def _createlog(self):
		"""
		Create the logfile and the link to the logfile (if requested).
		"""
		self._logfile = None
		self._logfilename = None
		self._loglinkname = None
		if self.log2file:
			# Create the log file
			logfilename = ul4c.Template(self.logfilename, "logfilename").renders(job=self)
			lf = self._logfilename = url.File(logfilename).abs()
			self._logfile = lf.open(mode="w", encoding=self.encoding, errors=self.errors)
			if self.loglinkname is not None:
				# Create the log link
				loglinkname = ul4c.Template(self.loglinkname, "loglinkname").renders(job=self)
				ll = self._loglinkname = url.File(loglinkname).abs()
				lf = self._logfilename.relative(ll)
				try:
					lf.symlink(ll)
				except OSError as exc:
					if exc.errno == errno.EEXIST:
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
				# If the file is too old, delete it (note that this might delete files that were not produced by sisyphus)
				if fileurl.mdate() < threshold:
					if not removedany: # Only log this line for the first logfile we remove
						self.log.sisyphus.info("Removing logfiles older than {}".format(keepfilelogs))
						removedany = True
					self.log.sisyphus.info("Removing logfile {}".format(fileurl.local()))
					fileurl.remove()

	def _reporterrors(self):
		if self._exceptions:
			ul4errors = []
			jsonerrors = []
			for (tasks, exc) in self._exceptions:
				error = "{}.{}".format(exc.__class__.__module__, exc.__class__.__qualname__)
				message = str(exc) or None
				tb = "".join(traceback.format_tb(exc.__traceback__))
				tb += self._exc(exc)
				ul4errors.append(dict(tasks=tasks, error=error, message=message, traceback=tb))
				jsonerrors.append(dict(tasks=[task.asjson() for task in tasks], error=error, message=message, traceback=tb))

			jsondata = dict(
				projectname=self.projectname,
				jobname=self.jobname,
				identifier=self.identifier,
				errors=jsonerrors,
				host_name=misc.sysinfo.host_name,
				host_fqdn=misc.sysinfo.host_fqdn,
				host_ip=misc.sysinfo.host_ip,
				host_sysname=misc.sysinfo.host_sysname,
				host_nodename=misc.sysinfo.host_nodename,
				host_release=misc.sysinfo.host_release,
				host_version=misc.sysinfo.host_version,
				host_machine=misc.sysinfo.host_machine,
				user_name=misc.sysinfo.user_name,
				user_uid=misc.sysinfo.user_uid,
				user_gid=misc.sysinfo.user_gid,
				user_gecos=misc.sysinfo.user_gecos,
				user_dir=misc.sysinfo.user_dir,
				user_shell=misc.sysinfo.user_shell,
				pid=misc.sysinfo.pid,
				script_name=misc.sysinfo.script_name,
				short_script_name=misc.sysinfo.short_script_name,
			)
			emailsubject = self._formatemailsubject.renders(job=self, sysinfo=misc.sysinfo, errors=ul4errors)
			emailbodytext = self._formatemailbodytext.renders(job=self, sysinfo=misc.sysinfo, errors=ul4errors)
			emailbodyhtml = self._formatemailbodyhtml.renders(job=self, sysinfo=misc.sysinfo, errors=ul4errors)

			if self.toemail and self.fromemail and self.smtphost:
				textpart = text.MIMEText(emailbodytext)
				htmlpart = text.MIMEText(emailbodyhtml, _subtype="html")
				jsonpart = application.MIMEApplication(json.dumps(jsondata).encode("utf-8"), _subtype="json", _encoder=encoders.encode_7or8bit)
				jsonpart.add_header('Content-Disposition', 'attachment', filename="{}.{}.json".format(self.projectname, self.jobname))

				msg = multipart.MIMEMultipart(
					_subparts=[
						multipart.MIMEMultipart(_subtype="alternative", _subparts=[textpart, htmlpart]),
						jsonpart,
					]
				)

				msg["To"] = self.toemail
				msg["From"] = self.fromemail
				msg["Subject"] = emailsubject
				try:
					server = smtplib.SMTP(self.smtphost, self.smtpport)
					server.sendmail(self.fromemail, self.toemail, msg.as_string())
					server.quit()
					self.log.sisyphus.email("Sent email report to {}".format(self.toemail))
				except smtplib.SMTPException as exc:
					self.log.sisyphus.email.exc(exc)
			else:
				print(emailbodytext)
				print("-"*80)

	def _exc(self, exc):
		"""
		Format an exception object for logging.
		"""
		try:
			strexc = str(exc)
		except UnicodeError:
			strexc = "?"
		if exc.__class__.__module__ not in ("builtins", "exceptions"):
			fmt = "{0.__class__.__module__}.{0.__class__.__name__}"
		else:
			fmt = "{0.__class__.__name__}"
		if strexc:
			fmt += ": {1}"
		return fmt.format(exc, strexc)


class Task(object):
	"""
	A subtask of a :class:`Job`.
	"""

	ul4attrs = {"index", "count", "type", "name", "starttime", "endtime"}

	def __init__(self, type=None, name=None, index=None, count=None, errors="raise"):
		"""
		Create a :class:`Task` object. For the meaning of the parameters see
		:meth:`Job.task`.
		"""
		self.type = type
		self.name = name
		self.index = index
		self.count = count
		self.errors = errors
		self.starttime = datetime.datetime.now()
		self.endtime = None
		self.success = None

	def end(self):
		self.endtime = datetime.datetime.now()
		self.success = True

	def fail(self):
		self.endtime = datetime.datetime.now()
		self.success = False

	def asjson(self):
		return dict(
			type=self.type,
			name=self.name,
			index=self.index,
			count=self.count,
			starttime=self.starttime.isoformat(),
			endtime=self.endtime.isoformat() if self.endtime else None,
			success=self.success
		)

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} type={0.type!r} name={0.name!r} at {1:#x}".format(self, id(self))


class Tag(object):
	"""
	A :class:`Tag` object can be used to call a function with an additional list
	of tags. Tags can be added via :meth:`__getattr__` or :meth:`__getitem__` calls.
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


def execute(job):
	"""
	Execute the job :obj:`job` once.
	"""
	job._handleexecution()


def executewithargs(job, args=None):
	"""
	Execute the job :obj:`job` once with command line arguments.

	:obj:`args` are the command line arguments (:const:`None` results in
	``sys.argv`` being used)
	"""
	job.parseargs(args)
	job._handleexecution()
