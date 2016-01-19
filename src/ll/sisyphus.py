# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2000-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2000-2016 by Walter Dörwald
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
	import urllib.request
	from ll import sisyphus

	class Fetch(sisyphus.Job):
		projectname = "ACME.FooBar"
		jobname = "Fetch"
		argdescription = "fetch http://www.python.org/ and save it to a local file"
		maxtime = 3 * 60

		def __init__(self):
			self.url = "http://www.python.org/"
			self.tmpname = "Fetch_Tmp_{}.html".format(os.getpid())
			self.officialname = "Python.html"

		def execute(self):
			self.log("fetching data from {!r}".format(self.url))
			data = urllib.request.urlopen(self.url).read()
			datasize = len(data)
			self.log("writing file {!r} ({:,} bytes)".format(self.tmpname, datasize))
			open(self.tmpname, "wb").write(data)
			self.log("renaming file {!r} to {!r}".format(self.tmpname, self.officialname))
			os.rename(self.tmpname, self.officialname)
			return "cached {!r} as {!r} ({:,} bytes)".format(self.url, self.officialname, datasize)

	if __name__=="__main__":
		sisyphus.executewithargs(Fetch())

You will find the log files for this job in ``~/ll.sisyphus/ACME.FooBar/Fetch/``.


Logging and tags
----------------

Logging itself is done by calling ``self.log``::

	self.log("can't parse XML file {}".format(filename))

This logs the argument without tagging the line.

It is possible to add tags to the logging call. This is done by accessing
attributes of the ``log`` pseudo method. I.e. to add the tags ``xml`` and
``warning`` to a log call you can do the following::

	self.log.xml.warning("can't parse XML file {}".format(filename))

It's also possible to do this via ``__getitem__`` calls, i.e. the above can be
written like this::

	self.log['xml']['warning']("can't parse XML file {}".format(filename))

:mod:`ll.sisyphus` itself uses the following tags:

	``sisyphus``
		This tag will be added to all log lines produced by :mod:`ll.sisyphus`
		itself.

	``init``
		This tag is used for the log lines output at the start of the job.

	``report``
		This tag will be added for all log messages related to sending the
		failure report email.

	``result``
		This tag is used for the final line written to the log files that shows a
		summary of what the job did (or why it failed).

	``fail``
		This tag is used in the result line if the job failed with an exception.

	``errors``
		This tag is used in the result line if the job ran to completion, but some
		exceptions where logged.

	``ok``
		This tag is used in the result line if the job ran to completion without
		any exceptions.

	``kill``
		This tag is used in the result line if the job was killed because it
		exceeded the maximum allowed runtime.


Exceptions
----------

When an exception object is passed to ``self.log`` the tag ``exc`` will be added
to the log call automatically.


Email
-----

It is possible to send an email when a job fails. For this the options
:option:`--fromemail`, :option:`--toemail` and :option:`--smtphost` have to be
set. If the job terminates because of an exception, or exceeds its maximum
runtime (and the option :option:`--noisykills` is set) or any of the calls to
``self.log`` include the tag ``email``, the email will be sent. This email
includes all logging calls and the final exception (if there is any) in plain
text and HTML format as well as as a JSON attachment.
"""


import sys, os, signal, fcntl, traceback, errno, pprint, datetime, argparse, tokenize, json, smtplib

try:
	import gzip
except ImportError:
	gzip = None

try:
	import bz2
except ImportError:
	bz2 = None

try:
	import lzma
except ImportError:
	lzma = None

from email.mime import text, application, multipart
from email import encoders

try:
	import setproctitle
except ImportError:
	setproctitle = None

from ll import url, ul4c, misc


__docformat__ = "reStructuredText"


def _formattraceback(exc):
	return "".join(traceback.format_exception(exc.__class__, exc, exc.__traceback__))


def _formatlines(obj):
	if isinstance(obj, BaseException):
		obj = _formattraceback(obj)
	elif not isinstance(obj, str):
		obj = pprint.pformat(obj)
	lines = obj.splitlines()
	while lines and not lines[0].strip():
		del lines[0]
	while lines and not lines[-1].strip():
		del lines[-1]
	return lines


class Job:
	"""
	A Job object executes a task once.

	To use this class, derive your own class from it and overwrite the
	:meth:`execute` method.

	The job can be configured in three ways: By class attributes in the
	:class:`Job` subclass, by attributes of the :class:`Job` instance (e.g. set
	in :meth:`__init__`) and by command line arguments (if :func:`executewithargs`
	is used). The following attributes/arguments are supported:

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
		:option:`--toemail` and :option:`--smtphost` are set (and any error
		or output to the email log occured).

	``toemail`` : :option:`--toemail`
		An email address where an email will be sent in case of a failure.

	``smtphost`` : :option:`--smtphost`
		The SMTP server to be used for sending the failure report email.

	``smtpport`` : :option:`--smtpport`
		The port number used for the connection to the SMTP server.

	``smtpuser`` : :option:`--smtpuser`
		The user name used to log into the SMTP server. (Login will only be done
		if both :option:`--smtpuser` and :option:`--smtppassword` are given)

	``smtppassword`` : :option:`--smtppassword`
		The password used to log into the SMTP server.

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
		The filename of a link that points to the currently active logfile
		(as an UL4 template). If this is :const:`None` no link will be created.

	``log2file`` : :option:`-f` or :option:`--log2file`
		Should a logfile be written at all?

	``formatlogline`` : :option:`--formatlogline`
		An UL4 template for formatting each line in the logfile. Available
		variables are ``time`` (current time), ``starttime`` (start time of the
		job), ``tags`` (list of tags for the line) and ``line`` (the log line
		itself).

	``keepfilelogs`` : :option:`--keepfilelogs`
		The number of days the logfiles are kept. Old logfiles (i.e. all files in
		the same directory as the current logfile that are more than
		``keepfilelogs`` days old) will be removed at the end of the job.

	``compressfilelogs`` : :option:`--compressfilelogs`
		The number of days after which log files are compressed (if they aren't
		deleted via ``keepfilelogs``).

	``compressmode`` : :option:`--compressmode`
		How to compress the logfiles. Possible values are: ``"gzip"``, ``"bzip2"``
		and ``"lzma"``. The default is ``"bzip2"``.

	``encoding`` : :option:`--encoding`
		The encoding to be used for the logfile. The default is ``"utf-8"``.

	``errors`` : :option:`--errors`
		Encoding error handler name (goes with ``encoding``). The default is
		``"strict"``.

	``maxemailerrors`` : :option:`--maxemailerrors`
		This options limits the number of exceptions and errors messages that
		will get attached to the failure email. The default is 10.

	``proctitle`` : :option:`--proctitle`
		When this options is specified, the process title will be modified during
		execution of the job, so that the ``ps`` command shows what the processes
		are doing. (This requires :mod:`setproctitle`.)

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
	smtpuser = None
	smtppassword = None

	identifier = None

	maxtime = 5 * 60

	fork = True

	noisykills = False
	notify = False

	logfilename = "~/ll.sisyphus/<?print job.projectname?>/<?print job.jobname?><?if job.identifier?>.<?print job.identifier?><?end if?>/<?print format(job.starttime, '%Y-%m-%d-%H-%M-%S-%f')?>.sisyphuslog"
	loglinkname = "~/ll.sisyphus/<?print job.projectname?>/<?print job.jobname?><?if job.identifier?>.<?print job.identifier?><?end if?>/current.sisyphuslog"

	# URL of final log file (``None`` if no logging is done to a fiole)
	logfileurl = None

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
			<?code desc = " ".join(str(d) for d in desc if d)?>
			<?print desc?>
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
		<?print job.projectname?>/<?print job.jobname?> for <?print sysinfo.user_name?>@<?print sysinfo.host_fqdn?> (<?print sysinfo.host_ip?>)<?if log?> failed with <?print len(log)?> exceptions/messages<?end if?>
	"""

	formatemailbodytext = r"""
		<?def line?>
			<?if value?>
				<?code value = str(value).split("\n")?>
				<?for line in value?>
					<?print format(label, "11")?>: <?print line?><?print "\n"?>
					<?code label = ""?>
				<?end for?>
			<?end if?>
		<?end def?>
		<?def tasklabel?>
			<?code desc = " ".join(str(part) for part in [task.type, task.name] if part)?>
			<?print desc?>
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
			<?print "\n@"?>
			<?print task.starttime?>
		<?end def?>
		<?render line(label="Project", value=job.projectname)?>
		<?render line(label="Job", value=job.jobname)?>
		<?render line(label="Identifier", value=job.identifier)?>
		<?render line(label="Script", value=sysinfo.script_name)?>
		<?render line(label="User", value=sysinfo.user_name)?>
		<?render line(label="Python", value=sysinfo.python_executable)?>
		<?render line(label="Version", value=sysinfo.python_version)?>
		<?render line(label="Host", value=sysinfo.host_fqdn)?>
		<?render line(label="IP", value=sysinfo.host_ip)?>
		<?render line(label="PID", value=sysinfo.pid)?>
		<?render line(label="Start", value=job.starttime)?>
		<?render line(label="End", value=job.endtime)?>
		<?if job.starttime and job.endtime?>
			<?render line(label="Duration", value=job.endtime-job.starttime)?>
		<?end if?>
		<?render line(label="Exceptions", value=countexceptions)?>
		<?render line(label="Messages", value=countmessages)?>
		<?render line(label="Logfile", value=job.logfileurl)?>

		<?code reportedexceptions = 0?>
		<?code reportedmessages = 0?>
		<?for (i, entry) in enumerate(log, 1)?>
			<?print "\n"?>
			<?print "-"*80?><?print "\n"?>
			<?print "\n"?>
			<?if entry.type == "exception"?>
				<?code reportedexceptions += 1?>
				#<?print i?>: Exception<?print "\n"?>
				<?print "\n"?>
				<?for task in entry.tasks?>
					<?render line(label="Task", value=tasklabel.renders(task=task))?>
				<?end for?>
				<?render line(label="Class", value=entry.class)?>
				<?render line(label="Value", value=entry.value)?>
				<?if entry.traceback?>
					<?print "\n"?>
					<?print entry.traceback?>
				<?end if?>
			<?elif entry.type == "message"?>
				<?code reportedmessages += 1?>
				#<?print i?>: Message<?print "\n"?>
				<?print "\n"?>
				<?for task in entry.tasks?>
					<?render line(label="Task", value=tasklabel.renders(task=task))?>
				<?end for?>
				<?render line(label="Message", value=entry.message)?>
			<?end if?>
		<?end for?>
		<?if countexceptions + countmessages > reportedexceptions + reportedmessages?>
			<?print "\n"?>
			<?print "-"*80?><?print "\n"?>
			<?if countexceptions > reportedexceptions?><?print countexceptions - reportedexceptions?> more exceptions<?end if?>
			<?if countexceptions > reportedexceptions and countmessages > reportedmessages?> and<?end if?>
			<?if countmessages > reportedmessages?><?print countmessages - reportedmessages?> more messages<?end if?>
			...<?print "\n"?>
		<?end if?>
	"""

	formatemailbodyhtml = r"""
		<?note Subtemplates?>
		<?def line?>
			<?if value?>
				<tr style="vertical-align: baseline;"><th style="text-align:right;"><?printx label?></th><td style="padding-left: 1em;<?if whitespace?>white-space: <?printx whitespace?>;<?end if?>"><?printx value?></td></tr>
			<?end if?>
		<?end def?>
		<?def tasklabel?>
			<?code desc = [task.type, task.name]?>
			<?code desc = " ".join(str(d) for d in desc if d)?>
			<?printx desc?>
			<?if not isnone(task.index)?>
				<?if desc?> <?end if?>
				(
				<?printx task.index+1?>
				<?if not isnone(task.count)?>
					/<?printx task.count?>
				<?end if?>
				)
			<?elif not desc?>
				?
			<?end if?>
			<?print "\n@"?>
			<?printx task.starttime?>
		<?end def?>

		<?xml version='1.0' encoding='utf-8'?>
		<html>
			<head>
				<title><?printx job.projectname?>/<?printx job.jobname?> for <?printx sysinfo.user_name?>@<?printx sysinfo.host_fqdn?> (<?printx sysinfo.host_ip?>) failed</title>
			</head>
			<body style="font-family: monospace;">
				<h1><?printx job.projectname?>/<?printx job.jobname?> for <?printx sysinfo.user_name?>@<?printx sysinfo.host_fqdn?> (<?printx sysinfo.host_ip?>) failed</h1>
				<table>
					<?render line(label="Project", value=job.projectname)?>
					<?render line(label="Job", value=job.jobname)?>
					<?render line(label="Identifier", value=job.identifier)?>
					<?render line(label="Script", value=sysinfo.script_name)?>
					<?render line(label="User", value=sysinfo.user_name)?>
					<?render line(label="Python", value=sysinfo.python_executable)?>
					<?render line(label="Version", value=sysinfo.python_version)?>
					<?render line(label="Host", value=sysinfo.host_fqdn)?>
					<?render line(label="IP", value=sysinfo.host_ip)?>
					<?render line(label="PID", value=sysinfo.pid)?>
					<?render line(label="Start", value=job.starttime)?>
					<?render line(label="End", value=job.endtime)?>
					<?if job.starttime and job.endtime?>
						<?render line(label="Duration", value=job.endtime-job.starttime)?>
					<?end if?>
					<?render line(label="Exceptions", value=countexceptions)?>
					<?render line(label="Messages", value=countmessages)?>
					<?render line(label="Logfile", value=job.logfileurl)?>
				</table>
				<?code reportedexceptions = 0?>
				<?code reportedmessages = 0?>
				<?for (i, entry) in enumerate(log, 1)?>
					<hr/>
					<?if entry.type == "exception"?>
						<?code reportedexceptions += 1?>
						<h2>#<?printx i?>: Exception</h2>
						<table>
							<?for task in entry.tasks?>
								<?render line(label="Task", value=tasklabel.renders(task=task), whitespace="pre")?>
							<?end for?>
							<?render line(label="Timestamp", value=entry.timestamp)?>
							<?render line(label="Class", value=entry.class)?>
							<?render line(label="Value", value=entry.value)?>
						</table>
						<?if entry.traceback?>
							<h3>Traceback<h3>
							<pre style="font-weight:normal;">
								<?printx entry.traceback?>
							</pre>
						<?end if?>
					<?else?>
						<?code reportedmessages += 1?>
						<h2>#<?printx i?>: Message</h2>
						<table>
							<?for task in entry.tasks?>
								<?render line(label="Task", value=tasklabel.renders(task=task), whitespace="pre")?>
							<?end for?>
							<?render line(label="Timestamp", value=entry.timestamp)?>
							<?render line(label="Message", value=entry.message, whitespace="pre")?>
						</table>
					<?end if?>
				<?end for?>
				<?if countexceptions + countmessages > reportedexceptions + reportedmessages?>
					<hr/>
					<p>
						<?if countexceptions > reportedexceptions?><?print countexceptions - reportedexceptions?> more exceptions<?end if?>
						<?if countexceptions > reportedexceptions and countmessages > reportedmessages?> and<?end if?>
						<?if countmessages > reportedmessages?><?print countmessages - reportedmessages?> more messages<?end if?>
						...
					</p>
				<?end if?>
			</body>
		</html>
	"""

	keepfilelogs = 30
	compressfilelogs = 7
	compressmode = "bzip2"

	maxemailerrors = 10

	proctitle = True

	encoding = "utf-8"
	errors = "strict"

	ul4attrs = {"sysinfo", "projectname", "jobname", "identifier", "maxtime", "starttime", "endtime", "maxemailerrors", "logfileurl"}

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
		p.add_argument("-j", "--jobname", dest="jobname", metavar="NAME", help="The name of the job (default: %(default)s)", default=self.jobname if self.jobname is not None else self.__class__.__qualname__)
		p.add_argument(      "--fromemail", dest="fromemail", metavar="ADDRESS", help="The sender email address for the failure report email (default: %(default)s)", default=self.fromemail)
		p.add_argument(      "--toemail", dest="toemail", metavar="ADDRESS", help="An email address where failure reports will be sent (default: %(default)s)", default=self.toemail)
		p.add_argument(      "--smtphost", dest="smtphost", metavar="HOSTNAME", help="The SMTP server to use for sending the failure report email (default: %(default)s)", default=self.smtphost)
		p.add_argument(      "--smtpport", dest="smtpport", metavar="PORT", help="The port number used for the connection to the SMTP server (default: %(default)s)", type=int, default=self.smtpport)
		p.add_argument(      "--smtpuser", dest="smtpuser", metavar="USER", help="The user name used to log into the SMTP server. (default: %(default)s)", default=self.smtpuser)
		p.add_argument(      "--smtppassword", dest="smtppassword", metavar="PASSWORD", help="The password used to log into the SMTP server. (default: %(default)s)", default=self.smtppassword)
		p.add_argument(      "--identifier", dest="identifier", metavar="IDENTIFIER", help="Additional identifier that will be added to the failure report mail (default: %(default)s)", default=self.identifier)
		p.add_argument("-m", "--maxtime", dest="maxtime", metavar="SECONDS", help="Maximum number of seconds the job is allowed to run (default: %(default)s)", type=int, default=self.getmaxtime_seconds())
		p.add_argument(      "--fork", dest="fork", help="Fork the process and do the work in the child process? (default: %(default)s)", action=misc.FlagAction, default=self.fork)
		p.add_argument("-f", "--log2file", dest="log2file", help="Should the job log into a file? (default: %(default)s)", action=misc.FlagAction, default=self.log2file)
		p.add_argument("-o", "--log2stdout", dest="log2stdout", help="Should the job log to stdout? (default: %(default)s)", action=misc.FlagAction, default=self.log2stdout)
		p.add_argument("-e", "--log2stderr", dest="log2stderr", help="Should the job log to stderr? (default: %(default)s)", action=misc.FlagAction, default=self.log2stderr)
		p.add_argument(      "--keepfilelogs", dest="keepfilelogs", metavar="DAYS", help="Number of days log files are kept (default: %(default)s)", type=float, default=self.keepfilelogs)
		p.add_argument(      "--compressfilelogs", dest="compressfilelogs", metavar="DAYS", help="Number of days log after which log files are gzipped (default: %(default)s)", type=float, default=self.compressfilelogs)
		p.add_argument(      "--compressmode", dest="compressmode", metavar="MODE", help="Method for compressing old log files (default: %(default)s)", choices=("gzip", "bzip2", "lzma"), default=self.compressmode)
		p.add_argument(      "--maxemailerrors", dest="maxemailerrors", metavar="INTEGER", help="Maximum number of errors or messages to report in the failure report (default: %(default)s)", default=self.maxemailerrors)
		p.add_argument(      "--proctitle", dest="proctitle", help="Set the process title (default: %(default)s)", action=misc.FlagAction, default=self.proctitle)
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
		self.smtpuser = args.smtpuser
		self.smtppassword = args.smtppassword
		self.identifier = args.identifier
		self.maxtime = args.maxtime
		self.fork = args.fork
		self.noisykills = args.noisykills
		self.log2file = args.log2file
		self.log2stdout = args.log2stdout
		self.log2stderr = args.log2stderr
		self.keepfilelogs = datetime.timedelta(days=args.keepfilelogs)
		self.compressfilelogs = datetime.timedelta(days=args.compressfilelogs)
		self.compressmode = args.compressmode
		self.maxemailerrors = args.maxemailerrors
		self.proctitle = args.proctitle
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
		exc = RuntimeError("maximum runtime {} exceeded in forked child (pid {})".format(maxtime, misc.sysinfo.pid))
		if self.noisykills:
			self.log.email(exc)
		else:
			self.log(exc)
		self.log.sisyphus.result.kill("Terminated child after {}".format(maxtime))
		for logger in self._loggers:
			logger.close()
		os._exit(1)

	def _alarm_nofork(self, signum, frame):
		maxtime = self.getmaxtime()
		self.endtime = datetime.datetime.now()
		exc = RuntimeError("maximum runtime {} exceeded (pid {})".format(maxtime, misc.sysinfo.pid))
		if self.noisykills:
			self.log.email(exc)
		else:
			self.log(exc)
		self.log.sisyphus.result.kill("Terminated after {}".format(maxtime))
		for logger in self._loggers:
			logger.close()
		os._exit(1)

	def _handleexecution(self):
		"""
		Handle executing the job including handling of duplicate or hanging jobs.
		"""
		self._tasks = []
		self._loggers = []
		self._exceptioncount = 0
		self._originalproctitle = setproctitle.getproctitle() if self.setproctitle and setproctitle else None

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
			self.log = Tag(self._log) # Create tagged logger for files
			self._formatlogline = ul4c.Template(self.formatlogline, "formatlogline", whitespace="strip") # Log line formatting template
			self._formatemailsubject = ul4c.Template(self.formatemailsubject, "formatemailsubject", whitespace="strip") # Email subject formatting template
			self._formatemailbodytext = ul4c.Template(self.formatemailbodytext, "formatemailbodytext", whitespace="strip") # Email body formatting template (plain text)
			self._formatemailbodyhtml = ul4c.Template(self.formatemailbodyhtml, "formatemailbodyhtml", whitespace="strip") # Email body formatting template (HTML)

			self._createlog() # Create loggers

			maxtime = self.getmaxtime()
			self.log.sisyphus.init("{} (max time {}; pid {})".format(misc.sysinfo.script_name, maxtime, misc.sysinfo.pid))
			if self.setproctitle and setproctitle is None:
				self.log.sisyphus.init.warning("Can't set process title (module setproctitle not available)")

			if self.fork: # Forking mode?
				# Fork the process; the child will do the work; the parent will monitor the maximum runtime
				self.killpid = pid = os.fork()
				if pid: # We are the parent process
					self.setproctitle("parent", "{} (max time {})".format("logging to {}".format(self.logfileurl) if self.logfileurl else "no logging", maxtime))
					# set a signal to kill the child process after the maximum runtime
					signal.signal(signal.SIGALRM, self._alarm_fork)
					signal.alarm(self.getmaxtime_seconds())
					try:
						os.waitpid(pid, 0) # Wait for the child process to terminate
					except BaseException as exc:
						pass
					return # Exit normally
				self.setproctitle("child")
				self.log.sisyphus.init("forked worker child (child pid {})".format(os.getpid()))
			else: # We didn't fork
				# set a signal to kill ourselves after the maximum runtime
				signal.signal(signal.SIGALRM, self._alarm_nofork)
				signal.alarm(self.getmaxtime_seconds())

			self.setproctitle("child", "Setting up")
			self.notifystart()
			result = None
			try:
				with url.Context():
					self.setproctitle("child", "Working")
					result = self.execute()
			except Exception as exc:
				self.endtime = datetime.datetime.now()
				self.setproctitle("child", "Handling exception")
				result = "failed with {}".format(misc.format_exception(exc))
				# log the error to the logfile, because the job probably didn't have a chance to do it
				self.log.sisyphus.email(exc)
				self.log.sisyphus.result.fail(result)
				self.failed()
				# Make sure that exceptions at the top level get propagated if they are not reported by email
				if not (self.toemail and self.fromemail and self.smtphost):
					raise
			else:
				self.endtime = datetime.datetime.now()
				self.setproctitle("child", "Finishing")
				# log the result
				if self._exceptioncount:
					self.log.sisyphus.result.errors(result)
				else:
					self.log.sisyphus.result.ok(result)
			finally:
				self.setproctitle("child", "Cleaning up logs")
				for logger in self._loggers:
					logger.close()
				self.notifyfinish(result)
				fcntl.flock(f, fcntl.LOCK_UN | fcntl.LOCK_NB)
			if self.fork:
				os._exit(0)

	def notifystart(self):
		if self.notify:
			misc.notifystart()

	def notifyfinish(self, result):
		if self.notify:
			misc.notifyfinish(
				"{} {}".format(self.projectname, self.jobname),
				"finished after {}".format(self.endtime-self.starttime),
				result,
			)

	def task(self, type=None, name=None, index=None, count=None):
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
		"""
		return Task(self, type=type, name=name, index=index, count=count)

	def tasks(self, iterable, type=None, name=None):
		"""
		:meth:`tasks` iterates through :obj:`iterable` and calls :meth:`task` for
		each item. :obj:`index` and :obj:`count` will be passed to :meth:`task`
		automatically. :obj:`type` and :obj:`name` will be used for the type and
		name of the task. They can either be constants (in which case they will
		be passed as is) or callables (in which case they will be called with the
		item to get the type/name).

		Example::

			import sys, operator

			items = sys.modules.items()
			for (name, module) in self.tasks(items, "module", operator.itemgetter(0)):
				self.log("module is {}".format(module))

		The log output will look something like the following::

			[2014-11-14 11:17:01.319291]=[t+0:00:00.342013] :: {sisyphus}{init} >> /Users/walter/test.py (max time 0:05:00; pid 33482)
			[2014-11-14 11:17:01.321860]=[t+0:00:00.344582] :: {sisyphus}{init} >> forked worker child (child pid 33485)
			[2014-11-14 11:17:01.324067]=[t+0:00:00.346789] :: module tokenize (1/212) :: {email} >> module is <module 'tokenize' from '/Users/walter/.local/lib/python3.4/tokenize.py'>
			[2014-11-14 11:17:01.327711]=[t+0:00:03.350433] :: module heapq (2/212) :: {email} >> module is <module 'heapq' from '/Users/walter/.local/lib/python3.4/heapq.py'>
			[2014-11-14 11:17:01.333471]=[t+0:00:09.356193] :: module marshal (3/212) :: {email} >> module is <module 'marshal' (built-in)>
			[2014-11-14 11:17:01.340733]=[t+0:00:15.363455] :: module math (4/212) :: {email} >> module is <module 'math' from '/Users/walter/.local/lib/python3.4/lib-dynload/math.so'>
			[2014-11-14 11:17:01.354177]=[t+0:00:18.366899] :: module urllib.parse (5/212) :: {email} >> module is <module 'urllib.parse' from '/Users/walter/.local/lib/python3.4/urllib/parse.py'>
			[2014-11-14 11:17:01.368187]=[t+0:00:21.370909] :: module _posixsubprocess (6/212) :: {email} >> module is <module '_posixsubprocess' from '/Users/walter/.local/lib/python3.4/lib-dynload/_posixsubprocess.so'>
			[2014-11-14 11:17:01.372633]=[t+0:00:33.385355] :: module pickle (7/212) :: {email} >> module is <module 'pickle' from '/Users/walter/.local/lib/python3.4/pickle.py'>
			[...]
			[2014-11-14 11:17:03.768065]=[t+0:00:39.790787] :: {sisyphus}{info} >> Compressing logfiles older than 7 days, 0:00:00 via bzip2
			[2014-11-14 11:17:03.768588]=[t+0:00:39.791310] :: {sisyphus}{info} >> Compressing logfile /Users/walter/ll.sisyphus/ACME.FooBar/Test/2014-11-06-16-44-22-416878.sisyphuslog
			[2014-11-14 11:17:03.772348]=[t+0:00:39.795070] :: {sisyphus}{info} >> Compressing logfile /Users/walter/ll.sisyphus/ACME.FooBar/Test/2014-11-06-16-44-37-839632.sisyphuslog
			[2014-11-14 11:17:03.774178]=[t+0:00:39.796900] :: {sisyphus}{info} >> Cleanup done

		"""
		try:
			count = len(iterable)
		except TypeError:
			count = None
		for (i, item) in enumerate(iterable):
			with self.task(type(item) if callable(type) else type, name(item) if callable(name) else name, i, count):
				yield item

	def makeproctitle(self, process, detail=None):
		v = []
		if self.fork:
			v.append(process)
		for task in self._tasks:
			v.append(str(task))
		title = " :: ".join(v)
		if not detail:
			return title
		if not title:
			return detail
		return "{} >> {}".format(title, detail)

	def setproctitle(self, process, detail=None):
		if self.proctitle and setproctitle:
			title = self.makeproctitle(process, detail)
			setproctitle.setproctitle("{} :: {}".format(self._originalproctitle, title))

	def _log(self, tags, obj):
		"""
		Log :obj:`obj` to the log file using :obj:`tags` as the list of tags.
		"""
		timestamp = datetime.datetime.now()
		if isinstance(obj, BaseException) and "exc" not in tags:
			tags += ("exc",)
			self._exceptioncount += 1
		for logger in self._loggers:
			logger.log(timestamp, tags, self._tasks, obj)

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
		if self.toemail and self.fromemail and self.smtphost:
			# Use the email logger as the first logger, so that when sending the email (in :meth:`EmailLogger.close`) fails, it will still be logged to the log file/stdout/stderr
			self._loggers.append(EmailLogger(self))
		if self.log2stderr:
			self._loggers.append(StreamLogger(self, sys.stderr, self._formatlogline))
		if self.log2stdout:
			self._loggers.append(StreamLogger(self, sys.stdout, self._formatlogline))
		if self.log2file:
			# Create the log file
			logfilename = ul4c.Template(self.logfilename, "logfilename").renders(job=self)
			logfilename = url.File(logfilename).abs()
			self.logfileurl = str(url.Ssh(misc.sysinfo.user_name, misc.sysinfo.host_fqdn or misc.sysinfo.host_name, logfilename.local()))
			skipurls = [logfilename]
			logfile = logfilename.open(mode="w", encoding=self.encoding, errors=self.errors)
			if self.loglinkname is not None:
				# Create the log link
				loglinkname = ul4c.Template(self.loglinkname, "loglinkname").renders(job=self)
				loglinkname = url.File(loglinkname).abs()
				skipurls.append(loglinkname)
				logfilename = logfilename.relative(loglinkname)
				try:
					logfilename.symlink(loglinkname)
				except OSError as exc:
					if exc.errno == errno.EEXIST:
						loglinkname.remove()
						logfilename.symlink(loglinkname)
					else:
						raise
			self._loggers.append(URLResourceLogger(self, logfile, skipurls, self._formatlogline))


class Task:
	"""
	A subtask of a :class:`Job`.
	"""

	ul4attrs = {"index", "count", "type", "name", "starttime", "endtime", "success"}

	def __init__(self, job, type=None, name=None, index=None, count=None):
		"""
		Create a :class:`Task` object. For the meaning of the parameters see
		:meth:`Job.task`.
		"""
		self.job = job
		self.type = type
		self.name = name
		self.index = index
		self.count = count
		self.starttime = None
		self.endtime = None
		self.success = None
		self.exc = None

	def __enter__(self):
		self.starttime = datetime.datetime.now()
		self.job._tasks.append(self)
		self.job.setproctitle("child")
		for logger in self.job._loggers:
			logger.taskstart(self.job._tasks)
		return self

	def __exit__(self, type, value, traceback):
		self.endtime = datetime.datetime.now()
		if type is None:
			self.success = True
		else:
			self.success = False
			self.exc = value
		for logger in self.job._loggers:
			logger.taskend(self.job._tasks)
		self.job._tasks.pop()
		self.job.setproctitle("child")

	def __str__(self):
		v = " ".join(str(d) for d in (self.type, self.name) if d)
		if self.index is not None:
			if v:
				v += " "
			v += "({}".format(self.index+1)
			if self.count is not None:
				v += "/{}".format(self.count)
			v += ")"
		return v or "?"

	def asjson(self):
		return dict(
			type=self.type,
			name=self.name,
			index=self.index,
			count=self.count,
			starttime=self.starttime.isoformat() if self.starttime else None,
			endtime=self.endtime.isoformat() if self.endtime else None,
			success=self.success
		)

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} type={0.type!r} name={0.name!r} at {1:#x}".format(self, id(self))


class Tag:
	"""
	A :class:`Tag` object can be used to call a function with an additional list
	of tags. Tags can be added via :meth:`__getattr__` or :meth:`__getitem__` calls.
	"""
	def __init__(self, func, *tags):
		self.func = func
		self.tags = tags
		self._map = {}

	def __getattr__(self, tag):
		if tag in self.tags: # Avoid duplicate tags
			return self
		if tag not in self._map:
			newtag = Tag(self.func, *(self.tags + (tag,)))
			self._map[tag] = newtag
			return newtag
		else:
			return self._map[tag]

	__getitem__ = __getattr__

	def __call__(self, *args, **kwargs):
		return self.func(self.tags, *args, **kwargs)


class Logger:
	def log(self, timestamp, tags, tasks, text):
		pass

	def taskstart(self, tasks):
		pass

	def taskend(self, tasks):
		pass

	def close(self):
		pass


class StreamLogger(Logger):
	def __init__(self, job, stream, linetemplate):
		self.job = job
		self.stream = stream
		self.linetemplate = linetemplate
		self.lineno = 1 # Current line number

	def log(self, timestamp, tags, tasks, text):
		for line in _formatlines(text):
			line = self.linetemplate.renders(line=line, time=timestamp, tags=tags, tasks=tasks, sysinfo=misc.sysinfo, job=self.job)
			self.stream.write(line)
			self.stream.write("\n")
			self.lineno += 1
		self.stream.flush()

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} stream={0.stream!r} at {1:#x}>".format(self, id(self))


class URLResourceLogger(StreamLogger):
	def __init__(self, job, resource, skipurls, linetemplate):
		StreamLogger.__init__(self, job, resource, linetemplate)
		self.skipurls = skipurls

	def close(self):
		keepfilelogs = self.job.keepfilelogs
		compressfilelogs = self.job.compressfilelogs

		if keepfilelogs is not None or compressfilelogs is not None:
			if not isinstance(keepfilelogs, datetime.timedelta):
				keepfilelogs = datetime.timedelta(days=keepfilelogs)
			if not isinstance(compressfilelogs, datetime.timedelta):
				compressfilelogs = datetime.timedelta(days=compressfilelogs)
			now = datetime.datetime.utcnow()
			keepthreshold = now - keepfilelogs # Files older that this will be deleted
			compressthreshold = now - compressfilelogs # Files older that this will be gzipped
			logdir = self.stream.url.withoutfile()
			removedany = False
			compressedany = False
			warnedcompressany = False
			for fileurl in logdir/logdir.files():
				fileurl = logdir/fileurl
				# Never delete/compress the current log file or link, even if keepfilelogs/compressfilelogs is 0
				if fileurl in self.skipurls:
					continue
				# If the file is too old, delete/compress it (note that this might touch files that were not produced by sisyphus)
				mdate = fileurl.mdate()
				if mdate < keepthreshold:
					if not removedany: # Only log this line for the first logfile we remove
						# This will still work, as the file isn't closed yet.
						self.job.log.sisyphus.info("Removing logfiles older than {}".format(keepfilelogs))
						removedany = True
					self.remove(fileurl)
				elif mdate < compressthreshold:
					if not fileurl.file.endswith((".gz", ".bz2", ".xz")):
						if (self.job.compressmode == "gzip" and gzip is None) or (self.job.compressmode == "gzip2" and bz2 is None) or (self.job.compressmode == "lzma" and lzma is None):
							if not warnedcompressany:
								self.job.log.sisyphus.warning("{} compression not available, leaving log files uncompressed".format(self.job.compressmode))
								warnedcompressany = True
						else:
							if not compressedany:
								self.job.log.sisyphus.info("Compressing logfiles older than {} via {}".format(compressfilelogs, self.job.compressmode))
								compressedany = True
							self.compress(fileurl)
			if removedany or compressedany:
				self.job.log.sisyphus.info("Logfiles cleaned up")

	def remove(self, fileurl):
		self.job.log.sisyphus.info("Removing logfile {}".format(fileurl.local()))
		fileurl.remove()

	def compress(self, fileurl, bufsize=65536):
		if self.job.compressmode == "gzip":
			compressor = gzip.GzipFile
			ext = ".gz"
		elif self.job.compressmode == "bzip2":
			compressor = bz2.BZ2File
			ext = ".bz2"
		elif self.job.compressmode == "lzma":
			compressor = lzma.LZMAFile
			ext = ".xz"
		else:
			raise ValueError("unknown compressmode {!r}".format(self.job.compressmode))

		filename = fileurl.local()
		self.job.log.sisyphus.info("Compressing logfile {}".format(fileurl.local()))
		with open(filename, "rb") as logfile:
			with compressor(filename + ext, mode="wb") as compressedlogfile:
				while True:
					data = logfile.read(bufsize)
					if not data:
						break
					compressedlogfile.write(data)
		fileurl.remove()


class EmailLogger(Logger):
	def __init__(self, job):
		self.job = job
		self._log = []
		self._countexceptions = 0
		self._countmessages = 0

	def log(self, timestamp, tags, tasks, text):
		if "email" in tags:
			if len(self._log) < self.job.maxemailerrors:
				self._log.append((timestamp, tags, tasks[:], text))
			if isinstance(text, BaseException):
				self._countexceptions += 1
			else:
				self._countmessages += 1

	def close(self):
		if self._log:
			ul4log = []
			jsonlog = []
			for (timestamp, tags, tasks, obj) in self._log:
				if isinstance(obj, BaseException):
					excclass = misc.format_class(obj)
					value = str(obj) or None
					tb = _formattraceback(obj)
					ul4log.append({"type": "exception", "timestamp": timestamp, "class": excclass, "value": value, "traceback": tb, "tasks": tasks})
					jsonlog.append({"type": "exception", "timestamp": timestamp.isoformat(), "class": excclass, "value": value, "traceback": tb, "tasks": [task.asjson() for task in tasks]})
				else:
					message = "\n".join(_formatlines(obj))
					ul4log.append({"type": "message", "timestamp": timestamp, "message": message, "tasks": tasks})
					jsonlog.append({"type": "message", "timestamp": timestamp.isoformat(), "message": message, "tasks": [task.asjson() for task in tasks]})

			jsondata = dict(
				projectname=self.job.projectname,
				jobname=self.job.jobname,
				identifier=self.job.identifier,
				log=jsonlog,
				countexceptions=self._countexceptions,
				countmessages=self._countmessages,
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
				python_executable=misc.sysinfo.python_executable,
				python_version=misc.sysinfo.python_version,
				pid=misc.sysinfo.pid,
				script_name=misc.sysinfo.script_name,
				short_script_name=misc.sysinfo.short_script_name,
				starttime=self.job.starttime.isoformat() if self.job.starttime else None,
				endtime=self.job.endtime.isoformat() if self.job.endtime else None,
				logfileurl=self.job.logfileurl,
			)
			variables = dict(
				job=self.job,
				sysinfo=misc.sysinfo,
				log=ul4log,
				countexceptions=self._countexceptions,
				countmessages=self._countmessages,
			)
			emailsubject = self.job._formatemailsubject.renders(**variables)
			emailbodytext = self.job._formatemailbodytext.renders(**variables)
			emailbodyhtml = self.job._formatemailbodyhtml.renders(**variables)

			textpart = text.MIMEText(emailbodytext)
			htmlpart = text.MIMEText(emailbodyhtml, _subtype="html")
			jsonpart = application.MIMEApplication(json.dumps(jsondata).encode("utf-8"), _subtype="json", _encoder=encoders.encode_base64)
			jsonpart.add_header('Content-Disposition', 'attachment', filename="{}.{}.json".format(self.job.projectname, self.job.jobname))

			msg = multipart.MIMEMultipart(
				_subparts=[
					multipart.MIMEMultipart(_subtype="alternative", _subparts=[textpart, htmlpart]),
					jsonpart,
				]
			)

			msg["To"] = self.job.toemail
			msg["From"] = self.job.fromemail
			msg["Subject"] = emailsubject
			try:
				server = smtplib.SMTP(self.job.smtphost, self.job.smtpport)
				if self.job.smtpuser and self.job.smtppassword:
					server.login(self.job.smtpuser, self.job.smtppassword)
				server.send_message(msg)
				server.quit()
				self.job.log.sisyphus.report("Sent email report to {}".format(self.job.toemail))
			except smtplib.SMTPException as exc:
				self.job.log.sisyphus.report(exc)


def execute(job):
	"""
	Execute the job :obj:`job` once.
	"""
	job._handleexecution()


def executewithargs(job, args=None):
	"""
	Execute the job :obj:`job` once with command line arguments.

	:obj:`args` are the command line arguments (:const:`None` results in
	``sys.argv`` being used).
	"""
	job.parseargs(args)
	job._handleexecution()
