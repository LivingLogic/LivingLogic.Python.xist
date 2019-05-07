# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2000-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2000-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
.. program:: sisyphus

:mod:`!ll.sisyphus` simplifies running Python stuff as jobs.

This can either be done under the direction of a cron daemon or a similar
process runner, then :mod:`!ll.sisyphus` makes sure that there will be no more
than one job of a certain name running at any given time.

Or :mod:`!ll.sisyphus` can be used as its own minimal cron daemon and can
execute the job repeatedly.

A job has a maximum allowed runtime. If this maximum is exceeded, the job will
kill itself. In addition to that, job execution can be logged and in case of
job failure an email can be sent.

To use this module, you must derive your own class from :class:`Job` and
implement the :meth:`execute` method.

Logs will (by default) be created in the :file:`~/ll.sisyphus` directory.
This can be changed by deriving a new subclass and overwriting the appropriate
class attributes.

To execute a job, use the module level function :func:`execute` (or
:func:`executewithargs` when you want to support command line arguments).


Example
-------

The following example illustrates the use of this module:

.. sourcecode:: python

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
			self.tmpname = f"Fetch_Tmp_{os.getpid()}.html"
			self.officialname = "Python.html"

		def execute(self):
			self.log(f"fetching data from {self.url!r}")
			data = urllib.request.urlopen(self.url).read()
			datasize = len(data)
			self.log(f"writing file {self.tmpname!r} ({datasize:,} bytes)")
			with open(self.tmpname, "wb") as f:
				f.write(data)
			self.log(f"renaming file {self.tmpname!r} to {self.officialname!r}")
			os.rename(self.tmpname, self.officialname)
			return f"cached {self.url!r} as {self.officialname!r} ({datasize:,} bytes)"

	if __name__ == "__main__":
		sisyphus.executewithargs(Fetch())

You will find the log files for this job in
:file:`~/ll.sisyphus/ACME.FooBar/Fetch/`.


Eventful und uneventful job runs
--------------------------------

The method :meth:`Job.execute` (which must be overwritten to implement the jobs
main functionality) should return a one-line summary of what the job did
(this is called an "eventful run"). It can also return :const:`None` to report
that the job had nothing to do (this is called an "uneventful run"). In case of
an uneventful run, the log file will be deleted immediately at the end of the
run.


Repeat mode
-----------

Normally sisyphus jobs run under the control of a cron daemon or similar process
runner. In this mode the method :meth:`Job.execute` is executed once and after
that execution of the Python script ends.

However it is possible to activate repeat mode with the class/instance attribute
:obj:`Job.repeat` (or the command line option :option:`--repeat`).
If :obj:`Job.repeat` is true, execution of the job will be repeated indefinitely.

By default the next job run starts immediately, but it is possible to delay the
next run. For this the class/instance attribute :obj:`Job.nextrun` (or the
command line option :option:`--nextrun`) can be used. In its simplest form this
is the number of seconds to wait until the next job run is started. It can
also be a :class:`datetime.timedelta` object that specifies the delay, or it
can be a :class:`datetime.datetime` object specifying the next job run.
Furthermore :obj:`Job.nextrun` can be callable (so it can be implemented as a
method) and can return any of the types :class:`int`, :class:`float`,
:class:`datetime.timedelta` or :class:`datetime.datetime`. And, if
:obj:`Job.nextrun` is :const:`None`, the job run will be repeated immediately.


Logging and tags
----------------

Logging itself is done by calling :meth:`~Job.log`:

.. sourcecode:: python

	self.log(f"can't parse XML file {filename}")

This logs the argument without tagging the line.

It is possible to add tags to the logging call. This is done by accessing
attributes of the ``log`` pseudo method. I.e. to add the tags ``xml`` and
``warning`` to a log call you can do the following:

.. sourcecode:: python

	self.log.xml.warning(f"can't parse XML file {filename}")

It's also possible to do this via ``__getitem__`` calls, i.e. the above can be
written like this:

.. sourcecode:: python

	self.log['xml']['warning'](f"can't parse XML file {filename}")

:mod:`!ll.sisyphus` itself uses the following tags:

``sisyphus``
	This tag will be added to all log lines produced by :mod:`!ll.sisyphus`
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

``info``
	This tag is used for all other informational log messages output by
	:mod:`!ll.sisyphus` itself (like log file cleanup etc.).


Exceptions
----------

When an exception object is passed to ``self.log`` the tag ``exc`` will be added
to the log call automatically.


Log files
---------

By default logging is done to the log file (whose name changes from run to run
as it includes the start time of the job).

However logging to ``stdout`` and ``stderr`` can also be activated.

Furthermore two links will be created that automatically point to the last log
file. The "current" link (by default named :file:`current.sisyphuslog`) will
always point to the log file of the currently running job. If no job is running,
but the last run was eventful, it will point the newest log file. If the last
run was uneventful the link will point to a nonexistent log file (whose name can
be used to determine the date of the last run). The "last eventful" link
(by default named :file:`last_eventful.sisyphuslog`) will always point to the
last eventful job run (but will only be created at the end of the job run).
This link will never point to a nonexistent file.


Email
-----

It is possible to send an email when a job fails. For this, the options
:option:`--fromemail`, :option:`--toemail` and :option:`--smtphost` have to be
set. If the job terminates because of an exception or exceeds its maximum
runtime (and the option :option:`--noisykills` is set) or any of the calls
to :meth:`~Job.log` include the tag ``email``, the email will be sent. This
email includes the last 10 logging calls and the final exception (if there is
any) in plain text and HTML format as well as as a JSON attachment.


Requirements
------------

To reliably stop the job after the allowed maximum runtime, :mod:`sisyphus`
forks the process and kills the child process after the maximum runtime is
expired (via :func:`os.fork` and :func:`signal.signal`). This won't work on
Windows. So on Windows the job will always run to completion without being
killed after the maximum runtime.

To make sure that only one job instance runs concurrently, :mod:`!ll.sisyphus`
uses :mod:`fcntl` to create an exclusive lock on the file of the running script.
This won't work on Windows either. So on Windows you might have multiple
running instances of the job.

:mod:`!ll.sisyphus` uses the module :mod:`setproctitle` to change the process
title during various phases of running the job. If :mod:`setproctitle` is not
available the process title will not be changed.

If the module :mod:`psutil` is available it will be used to kill the child
process and any of its own child processes after the maximum runtime of the job
is exceeded. If :mod:`psutil` isn't available just the child process will be
killed (which is no problem as long as the child process doesn't spawn any
other processes).

For compressing the log files one of the modules :mod:`gzip`, :mod:`bz2` or
:mod:`lzma` is required (which might not be part of your Python installation).
"""


import sys, os, signal, traceback, errno, pprint, time, datetime, argparse, tokenize, json, smtplib

try:
	import fcntl
except ImportError:
	fcntl = None

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
	import psutil
except ImportError:
	psutil = None

try:
	import setproctitle
except ImportError:
	setproctitle = None

from ll import url, ul4c, misc


__docformat__ = "reStructuredText"


###
### Helper functions
###

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


def argdays(value):
	if isinstance(value, str):
		value = int(value)
	if not isinstance(value, datetime.timedelta):
		value = datetime.timedelta(days=value)
	return value


def argseconds(value):
	if isinstance(value, str):
		value = int(value)
	if not isinstance(value, datetime.timedelta):
		value = datetime.timedelta(seconds=value)
	return value


###
### The main class
###

class Job:
	"""
	A Job object executes a task (either once or repeatedly).

	To use this class, derive your own class from it and overwrite the
	:meth:`execute` method.

	The job can be configured in three ways: By class attributes in the
	:class:`Job` subclass, by attributes of the :class:`Job` instance (e.g. set
	in :meth:`__init__`) and by command line arguments (if :func:`executewithargs`
	is used). The following command line arguments are supported (the name of the
	attribute is the same as the long command line argument name):

	.. option:: -p <projectname>, --projectname <projectname>

		The name of the project this job belongs to. This might be a dot-separated
		hierarchical project name (e.g. including customer names or similar stuff).

	.. option:: -j <jobname>, --jobname <jobname>

		The name of the job itself (defaulting to the name of the class if none
		is given).

	.. option:: --identifier <identifier>

		An additional identifier that will be added to the failure report email.

	.. option:: --fromemail <emailadress>

		The sender email address for the failure report email.

		This email will only be sent if the options :option:`--fromemail`,
		:option:`--toemail` and :option:`--smtphost` are set (and any error
		or output to the email log occured).

	.. option:: --toemail <emailadress>

		An email address where an email will be sent in case of a failure.

	.. option:: --smtphost <servername>

		The SMTP server to be used for sending the failure report email.

	.. option:: --smtpport <integer>

		The port number used for the connection to the SMTP server.

	.. option:: --smtpuser <username>

		The user name used to log into the SMTP server. (Login will only be done
		if both :option:`--smtpuser` and :option:`--smtppassword` are given)

	.. option:: --smtppassword <password>

		The password used to log into the SMTP server.

	.. option:: -m <seconds>, --maxtime <seconds>

		Maximum allowed runtime for the job (as the number of seconds). If the job
		runs longer than that it will kill itself.

		(The instance attribute will always be converted to the type
		:class:`datetime.timedelta`)

	.. option:: --fork

		Forks the process and does the work in the child process. The parent
		process is responsible for monitoring the maximum runtime (this is the
		default). In non-forking mode the single process does both the work and
		the runtime monitoring.

	.. option:: --noisykills

		Should a message be printed/a failure email be sent when the maximum
		runtime is exceeded?

	.. option:: -n, --notify

		Should a notification be issued to the OS X Notification center?
		(done via terminal-notifier__).

		__ https://github.com/alloy/terminal-notifier

	.. option:: -r, --repeat

		Should job execution be repeated indefinitely?

		(This means that the job basically functions as its own cron daemon).

	.. option:: --nextrun <seconds>

		How many seconds should we wait after a job run before the next run gets
		started (only when :option:`--repeat` is set)?

		The class/instance attribute can also be a callable (i.e. it's possible
		to implement this as a method). Also :class:`datetime.datetime` is
		supported and specifies the start date for the next job run.

	.. option:: --logfilename <filename>

		Name of the logfile for this job as an UL4 template. Variables
		available in the template include ``user_name``, ``projectname``,
		``jobname`` and ``starttime``.

	.. option:: --currentloglinkname <filename>

		The filename of a link that points to the currently active logfile
		(as an UL4 template). If this is :const:`None` no link will be created.

	.. option:: --lasteventfulloglinkname <filename>

		The filename of a link that points to the logfile of the last eventful
		run of the job (as an UL4 template). If this is :const:`None` no
		link will be created.

	.. option:: -f, --log2file

		Should a logfile be written at all?

	.. option:: --formatlogline <format>

		An UL4 template for formatting each line in the logfile. Available
		variables are ``time`` (current time), ``starttime`` (start time of the
		job), ``tags`` (list of tags for the line) and ``line`` (the log line
		itself).

	.. option:: --keepfilelogs <days>

		The number of days the logfiles are kept. Old logfiles (i.e. all files in
		the same directory as the current logfile that are more than
		``keepfilelogs`` days old) will be removed at the end of the job.

		(The instance attribute will always be converted to the type
		:class:`datetime.timedelta`)

	.. option:: --compressfilelogs <days>

		The number of days after which log files are compressed (if they aren't
		deleted via :option:`--keepfilelogs`).

		(The instance attribute will always be converted to the type
		:class:`datetime.timedelta`)

	.. option:: --compressmode <mode>

		How to compress the logfiles. Possible values are: ``"gzip"``, ``"bzip2"``
		and ``"lzma"``. The default is ``"bzip2"``.

	.. option:: --encoding <encodingname>

		The encoding to be used for the logfile. The default is ``"utf-8"``.

	.. option:: --errors <errorhandlingname>

		Encoding error handler name (goes with :option:`--encoding`). The default is
		``"strict"``.

	.. option:: --maxemailerrors <integer>

		This options limits the number of exceptions and errors messages that
		will get attached to the failure email. The default is 10.

	.. option:: --proctitle

		When this options is specified, the process title will be modified during
		execution of the job, so that the :command:`ps` command shows what the
		processes are doing. (This requires :mod:`setproctitle`.)

	Command line arguments take precedence over instance attributes (if
	:func:`executewithargs` is used) and those take precedence over class
	attributes.

	Furthermore the following class attribute can be set to customize the
	help message:

	:attr:`argdescription`

		Description for the help message of the command line argument parser.
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

	maxtime = datetime.timedelta(minutes=5)

	fork = True

	noisykills = False
	notify = False

	repeat = False
	nextrun = None
	waitchildbreak = datetime.timedelta(seconds=0.5)

	logfilename = """
	~
	/ll.sisyphus
	/<?print job.projectname?>
	/<?print job.jobname?><?if job.identifier?>.<?print job.identifier?><?end if?>
	/<?print format(job.starttime, '%Y-%m-%d-%H-%M-%S-%f')?>.sisyphuslog
	"""

	currentloglinkname = """
	~
	/ll.sisyphus
	/<?print job.projectname?>
	/<?print job.jobname?><?if job.identifier?>.<?print job.identifier?><?end if?>
	/current.sisyphuslog
	"""

	lasteventfulloglinkname = """
	~
	/ll.sisyphus
	/<?print job.projectname?>
	/<?print job.jobname?><?if job.identifier?>.<?print job.identifier?><?end if?>
	/last_eventful.sisyphuslog
	"""

	# URL of final log file (``None`` if no logging is done to a file)
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
			<?if not isnone(task.index)?>
				[
					<?print task.index+1?>
					<?if not isnone(task.count)?>
						/<?print task.count?>
					<?end if?>
				]
				<?if desc?> <?end if?>
			<?elif not desc?>
				?
			<?end if?>
			<?print desc?>
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
				[
					<?print task.index+1?>
					<?if not isnone(task.count)?>
						/<?print task.count?>
					<?end if?>
				]
				<?if desc?> <?end if?>
			<?elif not desc?>
				?
			<?end if?>
			<?print desc?>
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

	keepfilelogs = datetime.timedelta(days=30)
	compressfilelogs = datetime.timedelta(days=7)
	compressmode = "bzip2"

	maxemailerrors = 10

	proctitle = True

	encoding = "utf-8"
	errors = "strict"

	ul4attrs = {"sysinfo", "projectname", "jobname", "identifier", "maxtime", "starttime", "endtime", "maxemailerrors", "logfileurl"}

	def execute(self):
		"""
		Execute the job once.

		Overwrite in subclasses to implement your job functionality.

		The return value is a one line summary of what the job did.

		When this method returns :const:`None` instead this tells the job
		machinery that the run of the job was uneventful and that the logfile
		can be deleted.
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
		p = argparse.ArgumentParser(description=self.argdescription, epilog="For more info see http://python.livinglogic.de/sisyphus.html")
		p.add_argument("-p", "--projectname", dest="projectname", metavar="NAME", help="The name of the project this job belongs to (default: %(default)s)", default=self.projectname)
		p.add_argument("-j", "--jobname", dest="jobname", metavar="NAME", help="The name of the job (default: %(default)s)", default=self.jobname if self.jobname is not None else self.__class__.__qualname__)
		p.add_argument(      "--fromemail", dest="fromemail", metavar="ADDRESS", help="The sender email address for the failure report email (default: %(default)s)", default=self.fromemail)
		p.add_argument(      "--toemail", dest="toemail", metavar="ADDRESS", help="An email address where failure reports will be sent (default: %(default)s)", default=self.toemail)
		p.add_argument(      "--smtphost", dest="smtphost", metavar="HOSTNAME", help="The SMTP server to use for sending the failure report email (default: %(default)s)", default=self.smtphost)
		p.add_argument(      "--smtpport", dest="smtpport", metavar="PORT", help="The port number used for the connection to the SMTP server (default: %(default)s)", type=int, default=self.smtpport)
		p.add_argument(      "--smtpuser", dest="smtpuser", metavar="USER", help="The user name used to log into the SMTP server. (default: %(default)s)", default=self.smtpuser)
		p.add_argument(      "--smtppassword", dest="smtppassword", metavar="PASSWORD", help="The password used to log into the SMTP server. (default: %(default)s)", default=self.smtppassword)
		p.add_argument(      "--identifier", dest="identifier", metavar="IDENTIFIER", help="Additional identifier that will be added to the failure report mail (default: %(default)s)", default=self.identifier)
		p.add_argument("-m", "--maxtime", dest="maxtime", metavar="SECONDS", help="Maximum number of seconds the job is allowed to run (default: %(default)s)", type=argseconds, default=self.maxtime)
		p.add_argument(      "--fork", dest="fork", help="Fork the process and do the work in the child process? (default: %(default)s)", action=misc.FlagAction, default=self.fork)
		p.add_argument("-f", "--log2file", dest="log2file", help="Should the job log into a file? (default: %(default)s)", action=misc.FlagAction, default=self.log2file)
		p.add_argument("-o", "--log2stdout", dest="log2stdout", help="Should the job log to stdout? (default: %(default)s)", action=misc.FlagAction, default=self.log2stdout)
		p.add_argument("-e", "--log2stderr", dest="log2stderr", help="Should the job log to stderr? (default: %(default)s)", action=misc.FlagAction, default=self.log2stderr)
		p.add_argument(      "--keepfilelogs", dest="keepfilelogs", metavar="DAYS", help="Number of days log files are kept (default: %(default)s)", type=argdays, default=self.keepfilelogs)
		p.add_argument(      "--compressfilelogs", dest="compressfilelogs", metavar="DAYS", help="Number of days log after which log files are gzipped (default: %(default)s)", type=argdays, default=self.compressfilelogs)
		p.add_argument(      "--compressmode", dest="compressmode", metavar="MODE", help="Method for compressing old log files (default: %(default)s)", choices=("gzip", "bzip2", "lzma"), default=self.compressmode)
		p.add_argument(      "--maxemailerrors", dest="maxemailerrors", metavar="INTEGER", help="Maximum number of errors or messages to report in the failure report (default: %(default)s)", default=self.maxemailerrors)
		p.add_argument(      "--proctitle", dest="proctitle", help="Set the process title (default: %(default)s)", action=misc.FlagAction, default=self.proctitle)
		p.add_argument(      "--encoding", dest="encoding", metavar="ENCODING", help="Encoding for the log file (default: %(default)s)", default=self.encoding)
		p.add_argument(      "--errors", dest="errors", metavar="METHOD", help="Error handling method for encoding errors in log texts (default: %(default)s)", default=self.errors)
		p.add_argument(      "--noisykills", dest="noisykills", help="Should a message be printed/failure email be sent if the maximum runtime is exceeded? (default: %(default)s)", action=misc.FlagAction, default=self.noisykills)
		p.add_argument("-n", "--notify", dest="notify", help="Should a notification be issued to the OS X notification center? (default: %(default)s)", action=misc.FlagAction, default=self.notify)
		p.add_argument("-r", "--repeat", dest="repeat", help="Repeat the job run indefinitely? (default: %(default)s)", action=misc.FlagAction, default=self.repeat)
		p.add_argument(      "--nextrun", dest="nextrun", metavar="SECONDS", help="How many seconds to wait after the run before repeating it? (default: %(default)s)", type=argseconds, default=self.nextrun)
		p.add_argument(      "--waitchildbreak", dest="waitchildbreak", metavar="SECONDS", help="How many seconds to wait to give the child process time to clean up after CTRL-C? (default: %(default)s)", type=float, default=self.waitchildbreak)

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
		self.keepfilelogs = args.keepfilelogs
		self.compressfilelogs = args.compressfilelogs
		self.compressmode = args.compressmode
		self.maxemailerrors = args.maxemailerrors
		self.proctitle = args.proctitle
		self.encoding = args.encoding
		self.errors = args.errors
		self.notify = args.notify
		self.repeat = args.repeat
		self.nextrun = args.nextrun
		self.waitchildbreak = args.waitchildbreak
		return args

	def _kill_children(self):
		if psutil is None:
			try:
				os.kill(self.killpid, signal.SIGTERM) # Kill our child
			except ProcessLookupError:
				pass # already gone
			return {self.killpid}
		else:
			pids = set()
			procs = psutil.Process().children(recursive=True)

			# Send SIGTERM
			for p in procs:
				pids.add(p.pid)
				p.terminate()
			(gone, alive) = psutil.wait_procs(procs, timeout=3)

			# Send SIGKILL
			if alive:
				for p in alive:
					print(f"Killing {p}")
					pids.add(p.pid)
					p.kill()
				(gone, alive) = psutil.wait_procs(alive, timeout=3)
				# Ignore whether any processes remain in the ``alive`` list
			return pids

	def _finished_timeout(self):
		self.setproctitle("parent", "Timeout")

		self.endtime = datetime.datetime.now()

		if self.fork:
			pids = self._kill_children()

			if len(pids) == 1:
				pidstr = f"child {misc.first(pids)}"
			else:
				pids = ", ".join(str(pid) for pid in pids)
				pidstr = f"children {pids}"

			exc = RuntimeError(f"maximum runtime {self.maxtime} exceeded in forked {pidstr}")
			msg = f"Terminated {pidstr} after {self.maxtime}"
		else:
			exc = RuntimeError(f"maximum runtime {self.maxtime} exceeded")
			msg = f"Terminated after {self.maxtime}"
		if self.noisykills:
			self.log.email(exc)
		else:
			self.log(exc)
		self.log.sisyphus.result.kill(msg)
		self._closelogs(True)
		return 4

	def _finished_break(self, exc):
		self.endtime = datetime.datetime.now()
		self.setproctitle("child", "Handling break")
		result = f"failed with {misc.format_exception(exc)}"
		self.log.sisyphus(exc)
		self.log.sisyphus.result.fail(result)
		self.failed()
		if not self.fork:
			self._closelogs(True)
		return 3

	def _finished_exception(self, exc):
		self.endtime = datetime.datetime.now()
		self.setproctitle("child", "Handling exception")
		result = f"failed with {misc.format_exception(exc)}"
		# log the error to the logfile, because :meth:`execute` probably didn't have a chance to do it
		self.log.sisyphus.email(exc)
		self.log.sisyphus.result.fail(result)
		self.failed()
		if not self.fork:
			self._closelogs(True)
		return 2

	def _finished_success(self, result):
		self.endtime = datetime.datetime.now()
		self.setproctitle("child", "Finishing")
		# log the result
		if self._exceptioncount:
			self.log.sisyphus.result.errors(result)
		else:
			self.log.sisyphus.result.ok(result)
		if not self.fork:
			self._closelogs(result is not None)
		return 1 if result is not None else 0

	def _signal_alarm(self, signum, frame):
		raise misc.Timeout(0)

	def _signal_int(self, signum, frame):
		signal.alarm(0) # Cancel maximum runtime alarm
		# Give the child process time to log the stacktrace
		time.sleep(self.waitchildbreak.total_seconds())
		raise KeyboardInterrupt

	def _logmessage(self):
		logmessage = []
		for logger in self._loggers:
			name = logger.name()
			if name is not None:
				logmessage.append(name)
		logmessage = ", ".join(logmessage)

		if logmessage:
			return f"logging to {logmessage}"
		else:
			return "no logging"

	def _handleoneexecution(self):
		self._tasks = []
		self._loggers = []
		self._exceptioncount = 0

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

		self._createlogs(True) # Create loggers

		if self.fork and hasattr(os, "fork"):
			self._tasks = [self.task("parent", os.getpid())]

		self.log.sisyphus.init(f"{misc.sysinfo.script_name} (max time {self.maxtime})")

		logmessage = self._logmessage()
		self.log.sisyphus.init(logmessage)

		# Check for support of various thing we'd like to use
		if fcntl is None:
			self.log.sisyphus.init.warning("Can't lock script file (module fcntl not available)")
		if self.fork and not hasattr(os, "fork"):
			self.log.sisyphus.init.warning("Can't fork (function os.fork not available)")
			self.fork = False
		if not hasattr(signal, "SIGALRM"):
			self.log.sisyphus.init.warning("Can't use signals (signal.SIGALRM not available)")
			self.fork = False
		if self.setproctitle and setproctitle is None:
			self.log.sisyphus.init.warning("Can't set process title (module setproctitle not available)")

		if self.fork: # Forking mode?
			# Fork the process; the child will do the work; the parent will monitor the maximum runtime
			self.killpid = pid = os.fork()
			if pid: # We are the parent process
				self.setproctitle("parent", f"{logmessage} (max time {self.maxtime})")
				# set a signal to delay CTRL-C handling until the child has cleaned up
				signal.signal(signal.SIGINT, self._signal_int)
				# set a signal to wake us up to kill the child process after the maximum runtime
				if self.maxtime is not None:
					signal.signal(signal.SIGALRM, self._signal_alarm)
					signal.alarm(int(self.maxtime.total_seconds()))
				try:
					(pid, status) = os.waitpid(pid, 0) # Wait for the child process to terminate
					if self.maxtime is not None:
						signal.alarm(0) # Cancel maximum runtime alarm
				except misc.Timeout as exc:
					self._finished_timeout()
					return # finish normally (or continue, if we're in repeat mode)
				else:
					status >>= 8
					if status == 0: # Uneventful run
						self._closelogs(False)
					elif status == 3: # KeyboardInterrupt
						# Don't close logfiles
						raise KeyboardInterrupt
					else: # Eventful run, exception, timeout
						self._closelogs(True)
					return # finish normally (or continue, if we're in repeat mode)
			# Here we are in the child process
			self.setproctitle("child")
			task = self.task("child", misc.sysinfo.pid, self._run if self.repeat else None)
			self._tasks = [task] # This replaces the task stack inherited from the parent
			self.log.sisyphus.init(f"forked worker child")
		else: # We didn't fork
			# set a signal to kill ourselves after the maximum runtime
			if self.maxtime is not None and hasattr(signal, "SIGALRM"):
				signal.signal(signal.SIGALRM, self._signal_alarm)
				signal.alarm(int(self.maxtime.total_seconds()))

		self.setproctitle("child", "Setting up")
		self.notifystart()
		result = None
		try:
			with url.Context():
				self.setproctitle("child", "Working")
				result = self.execute()
				signal.alarm(0) # Cancel alarm
		except misc.Timeout as exc:
			status = self._finished_timeout()
		except KeyboardInterrupt as exc:
			status = self._finished_break(exc)
			if not self.fork:
				raise
		except Exception as exc:
			status = self._finished_exception(exc)
		else:
			status = self._finished_success(result)
		self.notifyfinish(result)
		if self.fork:
			os._exit(status)

	def _handleexecution(self):
		"""
		Handle executing the job including handling of duplicate or hanging jobs.
		"""
		if self.jobname is None:
			self.jobname = self.__class__.__qualname__
		self._originalproctitle = setproctitle.getproctitle() if self.setproctitle and setproctitle else None
		self._run = 0
		self.maxtime = argseconds(self.maxtime)
		self.keepfilelogs = argdays(self.keepfilelogs)
		self.compressfilelogs = argdays(self.compressfilelogs)
		self.waitchildbreak = argseconds(self.waitchildbreak)

		# Obtain a lock on the script file to make sure we're the only one running
		with open(misc.sysinfo.script_name, "rb") as f:
			if fcntl is not None:
				try:
					fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
				except IOError as exc:
					if exc.errno != errno.EWOULDBLOCK: # some other error
						raise
					# The previous invocation of the job is still running
					return # Return without calling :meth:`execute`

			if self.repeat:
				while True:
					self._handleoneexecution()
					self._createlogs(False) # Recreate stdin/stdout loggers
					self._run += 1
					nextrun = self.nextrun
					if callable(nextrun):
						nextrun = nextrun()
					if nextrun is None:
						nextrun = datetime.timedelta(0)
					if isinstance(nextrun, (int, float)):
						nextrun = datetime.timedelta(seconds=nextrun)
					if isinstance(nextrun, datetime.timedelta):
						wait = nextrun
						nextrun = self.starttime + wait
					else:
						wait = nextrun - datetime.datetime.now()
					wait_seconds = wait.total_seconds()
					if wait_seconds > 0:
						self.setproctitle("parent", "Sleeping")
						self.log.sisyphus.info(f"Sleeping for {wait} until {nextrun}")
						time.sleep(wait_seconds)
					else:
						self.log.sisyphus.info(f"Restarting immediately")
			else:
				self._handleoneexecution()

			if fcntl is not None:
				fcntl.flock(f, fcntl.LOCK_UN | fcntl.LOCK_NB)

	def notifystart(self):
		if self.notify:
			misc.notifystart()

	def notifyfinish(self, result):
		if self.notify:
			misc.notifyfinish(
				f"{self.projectname} {self.jobname}",
				f"finished after {self.endtime-self.starttime}",
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

			items = list(sys.modules.items())
			for (name, module) in self.tasks(items, "module", operator.itemgetter(0)):
				self.log(f"module is {module}")

		The log output will look something like the following::

			[2019-05-06 18:52:31.366810]=[t+0:00:00.263849] :: parent 19448 :: {sisyphus}{init} >> /Users/walter/x/gurk.py (max time 0:01:40)
			[2019-05-06 18:52:31.367831]=[t+0:00:00.264870] :: parent 19448 :: {sisyphus}{init} >> logging to <stdout>, /Users/walter/ll.sisyphus/Test/Job/2019-05-06-18-52-31-102961.sisyphuslog
			[2019-05-06 18:52:31.371690]=[t+0:00:00.268729] :: [1] child 19451 :: {sisyphus}{init} >> forked worker child
			[2019-05-06 18:52:31.376598]=[t+0:00:00.273637] :: [1] child 19451 :: [1/226] module sys >> module is <module 'sys' (built-in)>
			[2019-05-06 18:52:31.378561]=[t+0:00:00.275600] :: [1] child 19451 :: [2/226] module builtins >> module is <module 'builtins' (built-in)>
			[2019-05-06 18:52:31.380381]=[t+0:00:00.277420] :: [1] child 19451 :: [3/226] module _frozen_importlib >> module is <module 'importlib._bootstrap' (frozen)>
			[2019-05-06 18:52:31.382248]=[t+0:00:00.279287] :: [1] child 19451 :: [4/226] module _imp >> module is <module '_imp' (built-in)>
			[2019-05-06 18:52:31.384064]=[t+0:00:00.281103] :: [1] child 19451 :: [5/226] module _thread >> module is <module '_thread' (built-in)>
			[2019-05-06 18:52:31.386047]=[t+0:00:00.283086] :: [1] child 19451 :: [6/226] module _warnings >> module is <module '_warnings' (built-in)>
			[2019-05-06 18:52:31.388009]=[t+0:00:00.285048] :: [1] child 19451 :: [7/226] module _weakref >> module is <module '_weakref' (built-in)>
			[...]
			[2019-05-06 18:52:31.847315]=[t+0:00:00.744354] :: [1] child 19451 :: {sisyphus}{result}{ok} >> done
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
		return f"{title} >> {detail}"

	def setproctitle(self, process, detail=None):
		if self.proctitle and setproctitle:
			title = self.makeproctitle(process, detail)
			setproctitle.setproctitle(f"{self._originalproctitle} :: {title}")

	def _log(self, tags, obj):
		"""
		Log :obj:`obj` to all loggers using :obj:`tags` as the list of tags.
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

	def _makelink(self, logfilename, linknametemplate):
		"""
		Make a symbolic link.

		The link goes from :obj:`loglinkname` to what the UL4 template
		:obj:`linknametemplate` returns.
		"""
		loglinkname = ul4c.Template(linknametemplate, "filename").renders(job=self)
		loglinkname = url.File(loglinkname).abs()
		logfilename = logfilename.relative(loglinkname)
		try:
			logfilename.symlink(loglinkname)
		except OSError as exc:
			if exc.errno == errno.EEXIST:
				loglinkname.remove()
				logfilename.symlink(loglinkname)
			else:
				raise
		return loglinkname

	def _createlogs(self, full):
		"""
		Create the logfile and the link to the logfile (if configured).

		If :obj:`full` is false, only the loggers for `stdout` and `stderr` will
		be generated (if configured).
		"""
		self._loggers = []
		if full and self.toemail and self.fromemail and self.smtphost:
			# Use the email logger as the first logger, so that when sending the email (in :meth:`EmailLogger.close`) fails, it will still be logged to the log file/stdout/stderr
			self._loggers.append(EmailLogger(self))
		if full and self.log2file:
			# Create the log file
			template = ul4c.Template(self.logfilename, "logfilename", whitespace="strip")
			logfilename = template.renders(job=self)
			logfilename = url.File(logfilename).abs()
			self.logfileurl = str(url.Ssh(misc.sysinfo.user_name, misc.sysinfo.host_fqdn or misc.sysinfo.host_name, logfilename.local()))
			skipurls = [logfilename]
			logfile = logfilename.open(mode="w", encoding=self.encoding, errors=self.errors)
			self._loggers.append(URLResourceLogger(self, logfilename, logfile, skipurls, self._formatlogline))
			if self.currentloglinkname is not None:
				# Create the link to the current log file
				template = ul4c.Template(self.currentloglinkname, "currentloglinkname", whitespace="strip")
				loglinkname = template.renders(job=self)
				loglinkname = url.File(loglinkname).abs()
				self._loggers.append(CurrentLinkLogger(self, logfilename, loglinkname))
				skipurls.append(loglinkname)
			if self.lasteventfulloglinkname is not None:
				# Create the link to the log file of the last eventful run
				# (deferred to the end of the run)
				template = ul4c.Template(self.lasteventfulloglinkname, "lasteventfulloglinkname", whitespace="strip")
				loglinkname = template.renders(job=self)
				loglinkname = url.File(loglinkname).abs()
				self._loggers.append(LastLinkLogger(self, logfilename, loglinkname))
				skipurls.append(loglinkname)
		if self.log2stdout:
			self._loggers.append(StreamLogger(self, sys.stdout, self._formatlogline))
		if self.log2stderr:
			self._loggers.append(StreamLogger(self, sys.stderr, self._formatlogline))

	def _closelogs(self, eventful):
		while self._loggers:
			# Don't remove the logger from the list immediately
			# In this way, log messages that the logger outputs during closing will
			# be logged by the logger itself (i.e. logfile cleanup will be logged
			# in the logfile)
			logger = self._loggers[0]
			logger.close(eventful)
			del self._loggers[0]


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
		v = ""
		if self.index is not None:
			v += f"[{self.index+1:,}"
			if self.count is not None:
				v += f"/{self.count:,}"
			v += "]"
		d = " ".join(str(d) for d in (self.type, self.name) if d)
		if d:
			if v:
				v += " "
			v += d
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
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} type={self.type!r} name={self.name!r} at {id(self):#x}"


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
	"""
	A :class:`Logger` is called by the :class:`Job` on any logging event.
	"""

	def name(self):
		"""
		A name for the logger (using in reporting)
		"""
		return None

	def log(self, timestamp, tags, tasks, text):
		"""
		Called by the :class:`Job` when a log entry has to be made.

		Arguments have the following meaning:

		``timestamp`` : ``datetime.datetime``
			The moment when the logging call was made.

		``tags`` : List of strings
			The tags that were part of the logging call. For example for the
			logging call::

				self.log.xml.warning("Skipping foobar")

			the list of tags is::

				["xml", "warning"]

		``tasks`` : List of :class:`Task` objects
			The currently active stack of :class:`Task` objects.

		``text`` : Any object
			The log text. This can be any object in which case is will be
			converted to a string via :func:`pprint.pformat` (or
			:func:`traceback.format_exception` if it's an exception)
		"""

	def taskstart(self, tasks):
		"""
		Called by the :class:`Job` when a new subtask has been started.

		:obj:`tasks` is the stack of currently active tasks (so ``tasks[-1]`` is
		the task that has been started).
		"""

	def taskend(self, tasks):
		"""
		Called by the :class:`Job` when a subtask is about to end.

		:obj:`tasks` is the stack of currently active tasks (so ``tasks[-1]`` is
		the task that's about to end).
		"""

	def close(self, eventful):
		"""
		Called by the :class:`Job` when job execution has finished.

		:obj:`eventful` specified whether the run was eventful (as returned by
		:meth:`Job.execute`).
		"""


class StreamLogger(Logger):
	"""
	Logger that writes logging events into an open file-like object. Is is used
	for logging to ``stdout`` and ``stderr``.
	"""

	def __init__(self, job, stream, linetemplate):
		self.job = job
		self.stream = stream
		self.linetemplate = linetemplate
		self.lineno = 1 # Current line number

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} stream={self.stream!r} at {id(self):#x}>"

	def name(self):
		return self.stream.name

	def log(self, timestamp, tags, tasks, text):
		for line in _formatlines(text):
			line = self.linetemplate.renders(line=line, time=timestamp, tags=tags, tasks=tasks, sysinfo=misc.sysinfo, job=self.job)
			self.stream.write(line)
			self.stream.write("\n")
			self.lineno += 1
		self.stream.flush()


class URLResourceLogger(StreamLogger):
	"""
	Logger that writes logging events into a file specified via an
	:class:`~ll.url.URL` object. This is used for logging to the standard log
	file.
	"""

	def __init__(self, job, fileurl, resource, skipurls, linetemplate):
		StreamLogger.__init__(self, job, resource, linetemplate)
		self.fileurl = fileurl
		self.skipurls = skipurls

	def name(self):
		return self.fileurl.local()

	def close(self, eventful):
		keepfilelogs = self.job.keepfilelogs
		compressfilelogs = self.job.compressfilelogs

		if keepfilelogs is not None or compressfilelogs is not None:
			now = datetime.datetime.utcnow()
			keepthreshold = now - keepfilelogs # Files older that this will be deleted
			compressthreshold = now - compressfilelogs # Files older that this will be compressed
			logdir = self.stream.url.withoutfile()
			removedany = False
			compressedany = False
			warnedcompressany = False
			for fileurl in logdir/logdir.files():
				fileurl = logdir/fileurl

				# Decide what to do with this file
				# (Note that this might delete/compress files that were not produced by sisyphus)
				if fileurl not in self.skipurls:
					mdate = fileurl.mdate()
					# If the file is not the logfile or a link to it ...
					if mdate < keepthreshold:
						# ... and it's to old to keep it, delete it
						if not removedany: # Only log this line for the first logfile we remove
							# This will still work, as the file isn't closed yet.
							self.job.log.sisyphus.info(f"Removing logfiles older than {keepfilelogs}")
							removedany = True
						self.remove(fileurl)
					elif mdate < compressthreshold:
						# ... and it's to old to keep it in uncompressed, compress it
						if not fileurl.file.endswith((".gz", ".bz2", ".xz")):
							if (self.job.compressmode == "gzip" and gzip is None) or (self.job.compressmode == "gzip2" and bz2 is None) or (self.job.compressmode == "lzma" and lzma is None):
								if not warnedcompressany:
									self.job.log.sisyphus.warning(f"{self.job.compressmode} compression not available, leaving log files uncompressed")
									warnedcompressany = True
							else:
								if not compressedany:
									self.job.log.sisyphus.info(f"Compressing logfiles older than {compressfilelogs} via {self.job.compressmode}")
									compressedany = True
								self.compress(fileurl)
			if not eventful:
				self.job.log.sisyphus.info("Going to delete current logfile")
			if removedany or compressedany or not eventful:
				self.job.log.sisyphus.info("Logfiles cleaned up")
			# Close the stream now, so that we're able to delete it (even on Windows)
			self.stream.close()
			if not eventful:
				# Remove current log file in case of a uneventful run
				self.fileurl.remove()

	def remove(self, fileurl):
		self.job.log.sisyphus.info(f"Removing logfile {fileurl.local()}")
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
			raise ValueError(f"unknown compressmode {self.job.compressmode!r}")

		filename = fileurl.local()
		self.job.log.sisyphus.info(f"Compressing logfile {fileurl.local()}")
		with open(filename, "rb") as logfile:
			with compressor(filename + ext, mode="wb") as compressedlogfile:
				while True:
					data = logfile.read(bufsize)
					if not data:
						break
					compressedlogfile.write(data)
		fileurl.remove()


class LinkLogger(Logger):
	"""
	Baseclass of all loggers that handle links to the log file.
	"""
	def __init__(self, job, fileurl, linkurl):
		self.job = job
		self.fileurl = fileurl
		self.linkurl = linkurl

	def _makelink(self):
		linkurl = self.linkurl.abs()
		fileurl = self.fileurl.relative(linkurl)
		try:
			fileurl.symlink(linkurl)
		except OSError as exc:
			if exc.errno == errno.EEXIST:
				linkurl.remove()
				fileurl.symlink(linkurl)
			else:
				raise


class CurrentLinkLogger(LinkLogger):
	"""
	Logger that handles the link to the current log file.
	"""
	def __init__(self, job, fileurl, linkurl):
		super().__init__(job, fileurl, linkurl)
		self._makelink()


class LastLinkLogger(LinkLogger):
	"""
	Logger that handles the link to the log file of the last eventful job run.
	"""

	def __init__(self, job, fileurl, linkurl):
		super().__init__(job, fileurl, linkurl)

	def close(self, eventful):
		if eventful:
			self._makelink()


class EmailLogger(Logger):
	"""
	Logger that handles sending an email report of the job run.
	"""

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

	def close(self, eventful):
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
			jsonpart.add_header('Content-Disposition', 'attachment', filename=f"{self.job.projectname}.{self.job.jobname}.json")

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
				self.job.log.sisyphus.report(f"Sent email report to {self.job.toemail}")
			except smtplib.SMTPException as exc:
				self.job.log.sisyphus.report(exc)


###
### High-level interface for starting jobs
###

def execute(job):
	"""
	Execute the job :obj:`job` once or repeatedly.
	"""
	job._handleexecution()


def executewithargs(job, args=None):
	"""
	Execute the job :obj:`job` once or repeatedly with command line arguments.

	:obj:`args` are the command line arguments (:const:`None` results in
	``sys.argv`` being used).
	"""
	job.parseargs(args)
	job._handleexecution()
