# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2000-2021 by LivingLogic AG, Bayreuth/Germany
## Copyright 2000-2021 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


r"""
.. program:: sisyphus

:mod:`sisyphus` simplifies running Python stuff as jobs.

This can either be done under the direction of a cron daemon or a similar
process runner, then :mod:`sisyphus` makes sure that there will be no more
than one job of a certain name running at any given time.

Or :mod:`sisyphus` can be used as its own minimal cron daemon and can
execute the job repeatedly.

A job has a maximum allowed runtime. If this maximum is exceeded, the job will
kill itself. In addition to that, job execution can be logged and in case of
job failure an email can be sent, a message can be posted to a `Mattermost
chat channel`__ or an event can be emitted to a `Sentry server`__.

To use this module, you must derive your own class from :class:`Job`,
implement the :meth:`~Job.execute` method and then call the module level
function :func:`execute` or :func:`executewithargs` with your job object
(preferably in an ``if __name__ == "__main__"`` block).

Logs will (by default) be created in the :file:`~/ll.sisyphus` directory.
This can be changed by overwriting the appropriate methods in the subclass.

To execute a job, use the module level function :func:`execute` (or
:func:`executewithargs` when you want to support command line arguments).

__ https://mattermost.com/
__ https://sentry.io/


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


Result status of a job run
--------------------------

The method :meth:`Job.execute` (which must be overwritten to implement the jobs
main functionality) should return a one-line summary of what the job did
(this is called a "successful run"). It can also return :const:`None` to report
that the job had nothing to do (this is called an "uneventful run").

Apart from "uneventful" and "successful" runs, the following results are
possible:

"interrupted"
	The job failed with an :exc:`KeyboardInterrupt`.

"failed"
	The job failed with an exception (other than :exc:`KeyboardInterrupt`).

"timeout"
	The job ran longer than that the allowed maximum runtime.


Repeat mode
-----------

Normally sisyphus jobs run under the control of a cron daemon or similar process
runner. In this mode the method :meth:`Job.execute` is executed once and after
that, execution of the Python script ends.

However it is possible to activate repeat mode with the class/instance attribute
``repeat`` (or the command line option :option:`--repeat`).
If ``repeat`` is true, execution of the job will be repeated indefinitely.

By default the next job run starts immediately after the end of the previous
run, but it is possible to delay the next run. For this the class/instance
attribute ``nextrun`` (or the command line option :option:`--nextrun`) can be
used. In its simplest form this is the number of seconds to wait until the next
job run is started. It can also be a :class:`datetime.timedelta` object that
specifies the delay, or it can be a :class:`datetime.datetime` object specifying
the next job run. Furthermore ``nextrun`` can be callable (so it can be
implemented as a method) and can return any of the types :class:`int`,
:class:`float`, :class:`datetime.timedelta` or :class:`datetime.datetime`.
And, if ``Job.nextrun`` is :const:`None`, the job run will be repeated
immediately.


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

:mod:`sisyphus` itself uses the following tags:

``sisyphus``
	This tag will be added to all log lines produced by :mod:`sisyphus`
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
	:mod:`sisyphus` itself (like log file cleanup etc.).


Exceptions
----------

When an exception object is passed to ``self.log`` the tag ``exc`` will be added
to the log call automatically.


Delayed logs
------------

If a log message has the tag ``delay`` it is considered a delayed message.
Delayed messages will be buffered up until the first log message that isn't
delayed is encountered (:mod:`sisyphus`\s messages all are delayed).
Then all buffered messages will be output. If only delayed messages are output
during the complete job run, only the result of the job run will be output.
If this output is ``None`` nothing will be output. This means that you will get
no log entries until something "interesting" happens.


Log files
---------

By default logging is done to the log file (whose name changes from run to run
as it includes the start time of the job).

However logging to ``stdout`` and ``stderr`` can also be activated.

Logfiles for uneventful runs wil be deleted after the run.

Multiple links will be created that automatically point to the last log file.
The "current" link (by default named :file:`current.sisyphuslog`) will always
point to the log file of the currently running job. If no job is running,
but the last run was eventful, it will point to the newest log file. If the last
run was uneventful the link will point to a nonexistent log file (whose name can
be used to determine the date of the last run).

The following links will be created at the end of the job run and will only
start to point to non-existent files when the log files they point to get
cleaned up:

*	The "last successful" link (by default named
	:file:`last_successful.sisyphuslog`) will always point to the last
	successful job run,
*	:file:`last_failed.sisyphuslog` points to the last failed run,
*	:file:`last_interrupted.sisyphuslog` points to the last interrupted run and
*	:file:`last_timeout.sisyphuslog` points to the last run that timed out.


Email
-----

It is possible to send an email when a job fails. For this, the options
:option:`--fromemail`, :option:`--toemail` and :option:`--smtphost` (or the
appropriate class attributes) have to be set. If the job terminates because of
an exception or exceeds its maximum runtime (and the option
:option:`--noisykills` is set) or any of the calls to :meth:`~Job.log` include
the tag ``email``, an email will be sent. This email includes the last 10
logging calls and the final exception (if there is any) in plain text and HTML
format as well as as a JSON attachment.


Mattermost
----------

It is possible to send log entries to a Mattermost_ chat channel. For this the
options :option:`--mattermost_url`, :option:`--mattermost_channel` and
:option:`--mattermost_token` (or the appropriate class attributes) must be
specified. All log entries including the tag ``mattermost``, as well as
all exceptions that abort the job will be sent to the Mattermost channel.

.. _Mattermost: https://mattermost.com/


Sentry
------

It is possible to send log entries to a Sentry_ server. For this the
option :option:`--sentry_dsn` (or the appropriate class attribute) must be
specified. All log entries including the tag ``sentry``, as well as
all exceptions that abort the job will be sent to the Sentry server.

.. _Sentry: https://sentry.io/

If the logging call includes any of the tags ``fatal``, ``error``, ``warning``,
``info``, ``debug`` this will be used as the event level. If the log argument
is an exception the event level will be ``fatal``. Otherwise it wil default to
``info``.

All tags will be converted to Sentry tags like this: A sisyphus tag ``foo``
will be converted into a Sentry tag ``sisypus.tag.foo`` with a value of ``true``.

Active tasks will be converted into Sentry breadcrumbs (See the methods
:meth:`~Job.task` and :meth:`~Job.tasks` for more info).


Health checks
-------------

When a job is started with the option :option:`--healthcheck`, instead of
running the job normally a health check is done. This bypasses the normal
mechanism that prevents multiple instances of the job from running (i.e. you can
have a normal job execution and a health check running in parallel).

If the job is healthy this will exit with an exit status of 0, otherwise it will
exit with an exit status of 1 and an error message on ``stdout`` stating the
reason why the job is considered unhealthy. There are three possible scenarios
for this:

1.	The job has never been run.

2.	The last run has ended with an error.

3.	The last run was too long ago.

To configure how scenario 3 is handled the class/instance attribute
``maxhealthcheckage`` (or the command line option
:option:`--maxhealthcheckage`) can be used. In its simplest form this is a
number of seconds or a :class:`datetime.timedelta` object. A job run that is
older that this value triggers scenario 3. ``maxhealthcheckage`` can be also be
a :class:`datetime.datetime` object specifying the cut-off date.

Furthermore ``maxhealthcheckage`` can be callable (so it can be implemented
as a method) and can return any of the types :class:`int`, :class:`float`,
:class:`datetime.timedelta` or :class:`datetime.datetime`.

And if ``Job.maxhealthcheckage`` is :const:`None`, scenario 3 will never trigger.


Requirements
------------

To reliably stop the job after the allowed maximum runtime, :mod:`sisyphus`
forks the process and kills the child process after the maximum runtime is
expired (via :func:`os.fork` and :func:`signal.signal`). This won't work on
Windows. So on Windows the job will always run to completion without being
killed after the maximum runtime.

To make sure that only one job instance runs concurrently, :mod:`sisyphus`
uses :mod:`fcntl` to create an exclusive lock on the file of the running script.
This won't work on Windows either. So on Windows you might have multiple
running instances of the job.

:mod:`sisyphus` uses the module :mod:`setproctitle` to change the process
title during various phases of running the job. If :mod:`setproctitle` is not
available the process title will not be changed.

If the module :mod:`psutil` is available it will be used to kill the child
process and any of its own child processes after the maximum runtime of the job
is exceeded. If :mod:`psutil` isn't available just the child process will be
killed (which is no problem as long as the child process doesn't spawn any
other processes).

If logging to Mattermost is used, :mod:`requests` has to be installed.

If logging to Sentry is used, :mod:`sentry_sdk` has to be installed.

For compressing the log files one of the modules :mod:`gzip`, :mod:`bz2` or
:mod:`lzma` is required (which might not be part of your Python installation).


Module documentation
--------------------
"""


import sys, os, argparse, time, datetime, pathlib, enum, types
import signal, traceback, pprint, tokenize, json, smtplib, operator, itertools

from typing import *
from typing import TextIO

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


from ll import url, ul4c, ul4on, misc


__docformat__ = "reStructuredText"


###
### Typing stuff
###

T = TypeVar("T")
OptStr = Optional[str]
OptInt = Optional[int]
OptStrFromCall = Union[str, None, Callable[..., Union[str, None]]]
OptDictFromCall = Union[dict, None, Callable[..., Union[dict, None]]]
Tags = Tuple[str, ...]
LogList  = List[Tuple[datetime.datetime, Tags, List["Task"], Any]]


###
### Helper functions and classes
###

def _formattraceback(exc: BaseException) -> str:
	return "".join(traceback.format_exception(exc.__class__, exc, exc.__traceback__))


def _formatlines(obj: Any) -> List[str]:
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


def argdays(value: Union[str, int, datetime.timedelta]) -> datetime.timedelta:
	if isinstance(value, str):
		value = int(value)
	if not isinstance(value, datetime.timedelta):
		value = datetime.timedelta(days=value)
	return value


def argseconds(value: Union[str, int, datetime.timedelta]) -> datetime.timedelta:
	if isinstance(value, str):
		value = int(value)
	if not isinstance(value, datetime.timedelta):
		value = datetime.timedelta(seconds=value)
	return value


def env(varname: str) -> OptStr:
	return os.environ.get(varname, None)


def get_mtime(filename: pathlib.Path) -> datetime.datetime:
	return datetime.datetime.fromtimestamp(filename.stat().st_mtime)


def get_utime(filename: pathlib.Path) -> Tuple[datetime.datetime, datetime.datetime]:
	stat = filename.stat()
	return (datetime.datetime.fromtimestamp(stat.st_atime), datetime.datetime.fromtimestamp(stat.st_mtime))


def set_utime(filename: pathlib.Path, atime: datetime.datetime, mtime: datetime.datetime) -> None:
	os.utime(str(filename), times=(atime.timestamp(), mtime.timestamp()))


class DatetimeEncoder(json.JSONEncoder):
	def default(self, obj: Any) -> str:
		if isinstance(obj, datetime.datetime):
			return obj.isoformat()
		return super().default(obj)


class Status(enum.IntEnum):
	"""
	The result status of a job run.

	Possible values are:

	*	``UNEVENTFUL``,
	*	``SUCCESSFUL``,
	*	``FAILED``,
	*	``INTERRUPTED``,
	*	``TIMEOUT``.
	"""
	UNEVENTFUL = 0
	SUCCESSFUL = 1
	FAILED = 2
	INTERRUPTED = 3
	TIMEOUT = 4


class Process(enum.Enum):
	"""
	The type of a running :mod:`!sisyphus` process.

	Possible values are:

	*	``SOLO`` (when in non-forking mode),
	*	``PARENT`` (the parent process in forking mode),
	*	``CHILD`` (the child process in forking mode).
	"""
	SOLO = 0
	PARENT = 1
	CHILD = 2


###
### The main class
###

class Job:
	"""
	A Job object executes a task (either once or repeatedly).

	To use this class, derive your own class from it and overwrite the
	:meth:`~Job.execute` method.

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

	.. option:: --mattermost_url <url>

		The URL where log entries can be posted to a Mattermost chat. For
		example:

		.. sourcecode:: text

			https://mattermost.example.org/api/v4/posts

		A log entry will only be posted to the Mattermost chat channel if the
		options :option:`--mattermost_url`, :option:`--mattermost_channel` and
		:option:`--mattermost_token` are set (and the log entry has the tag
		``mattermost``).

		Note that using this feature requires :mod:`requests`.

	.. option:: --mattermost_channel <id>

		The channel id of the Mattermost chat channel where log entries should be
		posted. For example:

		.. sourcecode:: text

			4cnszmopr3ntjexi4qmx499inc

	.. option:: --mattermost_token <auth>

		The "Personal Access Token" used for authorizing the post with the
		Mattermost server. For example:

		.. sourcecode:: text

			9xuqwrwgstrb3mzrxb83nb357a

	.. option:: --sentry_dsn <dsn>

		Sentry DSN for logging to a Sentry server. Something like:

		.. sourcecode:: text

			https://examplePublicKey@o0.ingest.sentry.io/0

	.. option:: --sentry_environment <environment>

		Environment reported to Sentry.

	.. option:: --sentry_release <release>

		Release reported to Sentry.

	.. option:: --sentry_debug <flag>

		Activates/deactivates Sentry debug mode.

		(Allowed ``<flag>`` values are ``false``, ``no``, ``0``, ``true``,
		``yes`` or ``1``)

	.. option:: -m <seconds>, --maxtime <seconds>

		Maximum allowed runtime for the job (as the number of seconds). If the job
		runs longer than that it will kill itself.

		(The instance attribute will always be converted to the type
		:class:`datetime.timedelta`)

	.. option:: --fork <flag>

		Forks the process and does the work in the child process. The parent
		process is responsible for monitoring the maximum runtime (this is the
		default). In non-forking mode the single process does both the work and
		the runtime monitoring.

		(Allowed ``<flag>`` values are ``false``, ``no``, ``0``, ``true``,
		``yes`` or ``1``)

	.. option:: --noisykills <flag>

		Should a message be printed/a failure email be sent when the maximum
		runtime is exceeded?

		(Allowed ``<flag>`` values are ``false``, ``no``, ``0``, ``true``,
		``yes`` or ``1``)

	.. option:: --exit_on_error <flag>

		End job execution even in repeat mode when an exception is thrown?

		(Allowed ``<flag>`` values are ``false``, ``no``, ``0``, ``true``,
		``yes`` or ``1``)

	.. option:: -n <flag>, --notify <flag>

		Should a notification be issued to the OS X Notification center?
		(done via terminal-notifier__).

		(Allowed ``<flag>`` values are ``false``, ``no``, ``0``, ``true``,
		``yes`` or ``1``)

		__ https://github.com/alloy/terminal-notifier

	.. option:: -r <flag>, --repeat <flag>

		Should job execution be repeated indefinitely?

		(This means that the job basically functions as its own cron daemon).

		(Allowed ``<flag>`` values are ``false``, ``no``, ``0``, ``true``,
		``yes`` or ``1``)

	.. option:: --nextrun <seconds>

		How many seconds should we wait after a job run before the next run gets
		started (only when :option:`--repeat` is set)?

		The class/instance attribute can also be a callable (i.e. it's possible
		to implement this as a method). Also :class:`datetime.datetime` is
		supported and specifies the start date for the next job run.

	.. option:: --healthcheck <flag>

		Instead of normally executing the job, run a health check instead.

		(Allowed ``<flag>`` values are ``false``, ``no``, ``0``, ``true``,
		``yes`` or ``1``)

	.. option:: --maxhealthcheckage <seconds>

		If the last uneventful or successful job run is older then this number
		of seconds, consider the job to be unhealthy.

	.. option:: -f <flag>, --log2file <flag>

		Should a logfile be written at all?

		(Allowed ``<flag>`` values are ``false``, ``no``, ``0``, ``true``,
		``yes`` or ``1``)

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

	.. option:: --proctitle <flag>

		When this options is specified, the process title will be modified during
		execution of the job, so that the :command:`ps` command shows what the
		processes are doing. The default is ``True``. (This
		requires :mod:`setproctitle`.)

		(Allowed ``<flag>`` values are ``false``, ``no``, ``0``, ``true``,
		``yes`` or ``1``)


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

	mattermost_url = None
	mattermost_channel = None
	mattermost_token = None

	sentry_dsn = None
	sentry_release = None
	sentry_environment = None
	sentry_debug = False

	identifier = None

	maxtime = datetime.timedelta(minutes=5)

	fork = True

	noisykills = False
	exit_on_error = False

	notify = False

	repeat = False
	nextrun = None
	waitchildbreak = datetime.timedelta(seconds=0.5)
	runhealthcheck = False
	maxhealthcheckage = None

	def basedir(self) -> pathlib.Path:
		"""
		Return the base directory where all log files will be kept.

		The path must be absolute.
		"""
		path = pathlib.Path(
			"~",
			"ll.sisyphus",
			self.projectname,
			self.jobname if self.identifier is None else f"{self.jobname}.{self.identifier}",
		)
		return path.expanduser().absolute()

	def logfilename(self) -> Optional[pathlib.Path]:
		"""
		Return the filename of the logfile for this job.

		The value must by an absolute :class:`pathlib.Path` object (or ``None``
		to disable creating the logfile).
		"""
		return self.basedir() / f"{self.starttime:%Y-%m-%d %H-%M-%S_%f}.sisyphuslog"

	def currentloglinkname(self) -> Optional[pathlib.Path]:
		"""
		Return the filename of the link to the currently active logfile.

		The value must by an absolute :class:`pathlib.Path` object (or ``None``
		to disable creating the link).
		"""
		return self.basedir() / f"current.sisyphuslog"

	def lastsuccessfulloglinkname(self) -> Optional[pathlib.Path]:
		"""
		Return the filename of the link that points to the logfile of the last
		successful run of the job.

		The value must by an absolute :class:`pathlib.Path` object (or ``None``
		to disable creating the link).
		"""
		return self.basedir() / f"last_successful.sisyphuslog"

	def lastfailedloglinkname(self) -> Optional[pathlib.Path]:
		"""
		Return the filename of the link that points to the logfile of the last
		failed run of the job.

		The value must by an absolute :class:`pathlib.Path` object (or ``None``
		to disable creating the link).
		"""
		return self.basedir() / f"last_failed.sisyphuslog"

	def lastinterruptedloglinkname(self) -> Optional[pathlib.Path]:
		"""
		Return the filename of the link that points to the logfile of the last
		interrupted run of the job.

		The value must by an absolute :class:`pathlib.Path` object (or ``None``
		to disable creating the link).
		"""
		return self.basedir() / f"last_interrupted.sisyphuslog"

	def lasttimeoutloglinkname(self) -> Optional[pathlib.Path]:
		"""
		Return the filename of the link that points to the logfile of the last
		run of the job with a timeout.

		The value must by an absolute :class:`pathlib.Path` object (or ``None``
		to disable creating the link).
		"""
		return self.basedir() / f"last_timeout.sisyphuslog"

	def healthfilename(self) -> pathlib.Path:
		"""
		Return the filename where the health of the last job run is stored.

		The value must by an absolute :class:`pathlib.Path` object and may not be
		``None``.
		"""
		return self.basedir() / f"current.sisyphushealth"

	def emailfilename(self, process: Optional[Process]=None) -> pathlib.Path:
		"""
		Return the filename where the parent and child process can log message
		that should be part of the email report.

		The value must by an absolute :class:`pathlib.Path` object and may not be
		``None``.
		"""
		if process is None:
			process = self.process
		return self.basedir() / f"email.{process.name.lower()}.ul4on"

	# URL of final log file (:const:`None` if no logging is done to a file)
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
			<?if task.index is not None?>
				[
					<?print task.index+1?>
					<?if task.count is not None?>
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
		<?def line(label, value)?>
			<?if value?>
				<?code value = str(value).split("\n")?>
				<?for line in value?>
					<?print format(label, "11")?>: <?print line?><?print "\n"?>
					<?code label = ""?>
				<?end for?>
			<?end if?>
		<?end def?>
		<?def tasklabel(task)?>
			<?code desc = " ".join(str(part) for part in [task.type, task.name] if part)?>
			<?if task.index is not None?>
				[
					<?print task.index+1?>
					<?if task.count is not None?>
						/<?print task.count?>
					<?end if?>
				]
				<?if desc?>
					<?print " "?>
				<?end if?>
			<?elif not desc?>
				?
			<?end if?>
			<?print desc?>
			<?if task.starttime?>
				<?print " "?>
				@
				<?print " "?>
				<?print task.starttime?>
			<?end if?>
		<?end def?>
		<?render line("Project", job.projectname)?>
		<?render line("Job", job.jobname)?>
		<?render line("Identifier", job.identifier)?>
		<?render line("Script", sysinfo.script_name)?>
		<?render line("User", sysinfo.user_name)?>
		<?render line("Python", sysinfo.python_executable)?>
		<?render line("Version", sysinfo.python_version)?>
		<?render line("Host", sysinfo.host_fqdn)?>
		<?render line("IP", sysinfo.host_ip)?>
		<?render line("PID", sysinfo.pid)?>
		<?render line("Start", job.starttime)?>
		<?render line("End", job.endtime)?>
		<?if job.starttime and job.endtime?>
			<?render line("Duration", job.endtime-job.starttime)?>
		<?end if?>
		<?render line("Exceptions", countexceptions)?>
		<?render line("Messages", countmessages)?>
		<?render line("Logfile", job.logfileurl)?>

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
					<?render line("Task", tasklabel.renders(task))?>
				<?end for?>
				<?render line("Class", entry.class)?>
				<?render line("Value", entry.value)?>
				<?if entry.traceback?>
					<?print "\n"?>
					<?print entry.traceback?>
				<?end if?>
			<?elif entry.type == "message"?>
				<?code reportedmessages += 1?>
				#<?print i?>: Message<?print "\n"?>
				<?print "\n"?>
				<?for task in entry.tasks?>
					<?render line("Task", tasklabel.renders(task))?>
				<?end for?>
				<?render line("Message", entry.message)?>
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
		<?def line(label, value, whitespace=None)?>
			<?if value?>
				<tr style="vertical-align: baseline;"><th style="text-align:right;"><?printx label?></th><td style="padding-left: 1em;<?if whitespace?>white-space: <?printx whitespace?>;<?end if?>"><?printx value?></td></tr>
			<?end if?>
		<?end def?>
		<?def tasklabel(task)?>
			<?code desc = [task.type, task.name]?>
			<?code desc = " ".join(str(d) for d in desc if d)?>
			<?if task.index is not None?>
				[
				<?printx task.index+1?>
				<?if task.count is not None?>
					/<?printx task.count?>
				<?end if?>
				]
				<?if desc?>
					<?printx " "?>
				<?end if?>
			<?elif not desc?>
				?
			<?end if?>
			<?printx desc?>
			<?if task.starttime?>
				<?printx " "?>
				@
				<?printx " "?>
				<?printx task.starttime?>
			<?end if?>
		<?end def?>

		<?xml version='1.0' encoding='utf-8'?>
		<html>
			<head>
				<title><?printx job.projectname?>/<?printx job.jobname?> for <?printx sysinfo.user_name?>@<?printx sysinfo.host_fqdn?> (<?printx sysinfo.host_ip?>) failed</title>
			</head>
			<body style="font-family: monospace;">
				<h1><?printx job.projectname?>/<?printx job.jobname?> for <?printx sysinfo.user_name?>@<?printx sysinfo.host_fqdn?> (<?printx sysinfo.host_ip?>) failed</h1>
				<table>
					<?render line("Project", job.projectname)?>
					<?render line("Job", job.jobname)?>
					<?render line("Identifier", job.identifier)?>
					<?render line("Script", sysinfo.script_name)?>
					<?render line("User", sysinfo.user_name)?>
					<?render line("Python", sysinfo.python_executable)?>
					<?render line("Version", sysinfo.python_version)?>
					<?render line("Host", sysinfo.host_fqdn)?>
					<?render line("IP", sysinfo.host_ip)?>
					<?render line("PID", sysinfo.pid)?>
					<?render line("Start", job.starttime)?>
					<?render line("End", job.endtime)?>
					<?if job.starttime and job.endtime?>
						<?render line("Duration", job.endtime-job.starttime)?>
					<?end if?>
					<?render line("Exceptions", countexceptions)?>
					<?render line("Messages", countmessages)?>
					<?render line("Logfile", job.logfileurl)?>
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
								<?render line("Task", tasklabel.renders(task), whitespace="pre")?>
							<?end for?>
							<?render line("Timestamp", entry.timestamp)?>
							<?render line("Class", entry.class)?>
							<?render line("Value", entry.value)?>
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
								<?render line("Task", tasklabel.renders(task), whitespace="pre")?>
							<?end for?>
							<?render line("Timestamp", entry.timestamp)?>
							<?render line("Message", entry.message, whitespace="pre")?>
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

	formatmattermosttitle = r"""
		<?if "error" in tags?>
			<?if type == "exc"?>
				<?code header = "Exception"?>
			<?elif type == "obj"?>
				<?code header = "Error object"?>
			<?else?>
				<?code header = "Error message"?>
			<?end if?>
		<?else?>
			<?if type == "exc"?>
				<?code header = "Exception"?>
			<?elif type == "obj"?>
				<?code header = "Object"?>
			<?else?>
				<?code header = "Message"?>
			<?end if?>
		<?end if?>
		<?print header?> in sisyphus job `<?print job.projectname?>`/`<?print job.jobname?>` from `<?print sysinfo.user_name?>@<?print sysinfo.host_fqdn?>` (<?print sysinfo.host_ip?>)
	"""

	formatmattermostmessage = r"""
		<?if type == "exc"?>
			```
			<?print "\n"?>
			<?print message?>
			<?print "\n"?>
			```
		<?elif type == "obj"?>
			```py
			<?print "\n"?>
			<?print message?>
			<?print "\n"?>
			```
		<?else?>
			<?print message?>
		<?end if?>
		<?print "\n"?>
		<?if tags?>
			**Tags**: <?for (f, t) in isfirst(tags)?><?if not f?>, <?end if?>`<?print t?>`<?end for?>
			<?print "\n"?>
		<?end if?>
		<?if len(tasks) > 1?>
			**Task**:<?print " "?>
			<?print " "?>
			<?for (f, task) in isfirst(tasks[1:])?>
				<?if not f?>
					<?print " ⟶ "?>
				<?end if?>
				<?code output = False?>
				<?if task.type is not None?>
					<?if output?> <?end if?>
					`<?print task.type?>`
					<?code output = True?>
				<?end if?>
				<?if task.name is not None?>
					<?if output?> <?end if?>
					`<?print task.name?>`
					<?code output = True?>
				<?end if?>
				<?if task.index is not None?>
					<?if output?> <?end if?>
					[
						<?print task.index+1?>
						<?if task.count is not None?>
							/<?print task.count?>
						<?end if?>
					]
					<?code output = True?>
				<?end if?>
				<?if not output?>
					?
				<?end if?>
			<?end for?>
			<?print "\n"?>
		<?end if?>
		**Timestamp**: <?print time?> — t+<?print time-job.starttime?>
		<?print "\n"?>
	"""

	keepfilelogs = datetime.timedelta(days=30)
	compressfilelogs = datetime.timedelta(days=7)
	compressmode = "bzip2"

	maxemailerrors = 10

	proctitle = True

	encoding = "utf-8"
	errors = "strict"

	ul4_attrs = {"sysinfo", "projectname", "jobname", "identifier", "maxtime", "starttime", "endtime", "maxemailerrors", "logfileurl"}

	process = Process.SOLO

	def execute(self) -> OptStr:
		"""
		Execute the job once.

		Overwrite in subclasses to implement your job functionality.

		The return value is a one line summary of what the job did.

		When this method returns :const:`None` instead this tells the job
		machinery that the run of the job was uneventful and that the logfile
		can be deleted.
		"""
		return "done"

	def healthcheck(self) -> OptStr:
		"""
		Called in parallel to a running job to check whether the job is healthy.

		Returns ``None`` if everything is ok, or an error message otherwise.
		"""
		healthfilename = self.healthfilename()
		try:
			lastwrite = get_mtime(healthfilename)
			cutoff = self._calc_maxhealthcheckage()
			if lastwrite < cutoff:
				return f"Not running since {cutoff} (last run at {lastwrite}; {datetime.datetime.now()-lastwrite} ago)"
			error = healthfilename.read_text(encoding=self.encoding, errors=self.errors)
			return error.strip() or None
		except FileNotFoundError:
			return f"Healthfile {healthfilename} missing"
		except ValueError:
			return f"Healthfile {healthfilename} malformed"

		return None

	def argparser(self) -> argparse.ArgumentParser:
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
		p.add_argument(      "--mattermost_url", dest="mattermost_url", metavar="URL", help="URL for logging to mattermost chat channel. (default: %(default)s)", default=self.mattermost_url)
		p.add_argument(      "--mattermost_channel", dest="mattermost_channel", metavar="ID", help="Channel id for logging to mattermost chat. (default: %(default)s)", default=self.mattermost_channel)
		p.add_argument(      "--mattermost_token", dest="mattermost_token", metavar="AUTH", help="Channel id for logging to mattermost chat. (default: %(default)s)", default=self.mattermost_token)
		p.add_argument(      "--sentry_dsn", dest="sentry_dsn", metavar="DSN", help="Sentry DSN for logging to a Sentry server. (default: %(default)s)", default=self.sentry_dsn)
		p.add_argument(      "--sentry_environment", dest="sentry_environment", metavar="ENVIRONMENT", help="Environment reported to Sentry. (default: %(default)s)", default=self.sentry_environment)
		p.add_argument(      "--sentry_release", dest="sentry_release", metavar="RELEASE", help="Release reported to Sentry. (default: %(default)s)", default=self.sentry_release)
		p.add_argument(      "--sentry_debug", dest="sentry_debug", help="Activate Sentry debug mode. (default: %(default)s)", action=misc.FlagAction, default=self.sentry_debug)
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
		p.add_argument(      "--exit_on_error", dest="exit_on_error", help="Stop the job when an error happens in repeat mode? (default: %(default)s)", action=misc.FlagAction, default=self.exit_on_error)
		p.add_argument("-n", "--notify", dest="notify", help="Should a notification be issued to the OS X notification center? (default: %(default)s)", action=misc.FlagAction, default=self.notify)
		p.add_argument("-r", "--repeat", dest="repeat", help="Repeat the job run indefinitely? (default: %(default)s)", action=misc.FlagAction, default=self.repeat)
		p.add_argument(      "--nextrun", dest="nextrun", metavar="SECONDS", help="How many seconds to wait after the run before repeating it? (default: %(default)s)", type=argseconds, default=self.nextrun)
		p.add_argument(      "--waitchildbreak", dest="waitchildbreak", metavar="SECONDS", help="How many seconds to wait to give the child process time to clean up? (default: %(default)s)", type=float, default=self.waitchildbreak)
		p.add_argument(      "--maxhealthcheckage", dest="maxhealthcheckage", metavar="SECONDS", help="How old may a healthcheckfile be before the health check complains about it? (default: %(default)s)", type=float, default=self.maxhealthcheckage)
		p.add_argument(      "--healthcheck", dest="runhealthcheck", help="Run a heathcheck instead of the normal job? (default: %(default)s)", action=misc.FlagAction, default=self.runhealthcheck)

		return p

	def parseargs(self, args: Optional[List[str]]) -> argparse.Namespace:
		"""
		Use the parser returned by :meth:`argparser` to parse the argument
		sequence ``args``, modify ``self`` accordingly and return
		the result of the parsers :meth:`parse_args` call.
		"""
		p = self.argparser()
		ns = p.parse_args(args)
		self.projectname = ns.projectname
		self.jobname = ns.jobname
		self.fromemail = ns.fromemail
		self.toemail = ns.toemail
		self.smtphost = ns.smtphost
		self.smtpport = ns.smtpport
		self.smtpuser = ns.smtpuser
		self.smtppassword = ns.smtppassword
		self.mattermost_url = ns.mattermost_url
		self.mattermost_channel = ns.mattermost_channel
		self.mattermost_token = ns.mattermost_token
		self.sentry_dsn = ns.sentry_dsn
		self.sentry_environment = ns.sentry_environment
		self.sentry_release = ns.sentry_release
		self.sentry_debug = ns.sentry_debug
		self.identifier = ns.identifier
		self.maxtime = ns.maxtime
		self.fork = ns.fork
		self.noisykills = ns.noisykills
		self.exit_on_error = ns.exit_on_error
		self.log2file = ns.log2file
		self.log2stdout = ns.log2stdout
		self.log2stderr = ns.log2stderr
		self.keepfilelogs = ns.keepfilelogs
		self.compressfilelogs = ns.compressfilelogs
		self.compressmode = ns.compressmode
		self.maxemailerrors = ns.maxemailerrors
		self.proctitle = ns.proctitle
		self.encoding = ns.encoding
		self.errors = ns.errors
		self.notify = ns.notify
		self.repeat = ns.repeat
		self.nextrun = ns.nextrun
		self.waitchildbreak = ns.waitchildbreak
		self.runhealthcheck = ns.runhealthcheck
		return ns

	def _handleexecution(self) -> None:
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
		self.sentry_sdk = None

		self._healthfilename = self.healthfilename()
		if self.runhealthcheck:
			result = self.healthcheck()
			raise SystemExit(result)

		self._formatlogline = ul4c.Template(self.formatlogline, "formatlogline", whitespace="strip") # Log line formatting template
		self._formatemailsubject = ul4c.Template(self.formatemailsubject, "formatemailsubject", whitespace="strip") # Email subject formatting template
		self._formatemailbodytext = ul4c.Template(self.formatemailbodytext, "formatemailbodytext", whitespace="strip") # Email body formatting template (plain text)
		self._formatemailbodyhtml = ul4c.Template(self.formatemailbodyhtml, "formatemailbodyhtml", whitespace="strip") # Email body formatting template (HTML)
		self._formatmattermosttitle = ul4c.Template(self.formatmattermosttitle, "formatmattermosttitle", whitespace="strip") # Mattermost chat title formatting template
		self._formatmattermostmessage = ul4c.Template(self.formatmattermostmessage, "formatmattermostmessage", whitespace="strip") # Mattermost chat message formatting template

		# Obtain a lock on the script file to make sure we're the only one running
		with open(misc.sysinfo.script_name, "rb") as f:
			if fcntl is not None:
				try:
					fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
				except BlockingIOError:
					# The previous invocation of the job is still running
					return # Return without calling :meth:`execute`

			if self.repeat:
				while True:
					status = self._handleoneexecution()
					self._run += 1
					nextrun = self._calc_nextrun()
					wait = nextrun - datetime.datetime.now()
					wait_seconds = wait.total_seconds()
					self._closelogs(status)
					if wait_seconds > 0:
						self.setproctitle("Sleeping")
						self.log.sisyphus.delay.info(f"Sleeping for {wait} until {nextrun}")
						time.sleep(wait_seconds)
					else:
						self.log.sisyphus.delay.info(f"Restarting immediately")
			else:
				status = self._handleoneexecution()
				self._closelogs(status)

			if fcntl is not None:
				fcntl.flock(f, fcntl.LOCK_UN | fcntl.LOCK_NB)

	def _handleoneexecution(self) -> Status:
		self._tasks = [] # type: List[Task]
		self._loggers = [] # type: List[Logger]
		self._exceptioncount = 0

		self.process = Process.SOLO

		# we were able to obtain the lock, so we are the only one running
		self.starttime = datetime.datetime.now()
		self.starttime_utc = datetime.datetime.utcnow()
		self.endtime = None # type: Optional[datetime.datetime]

		self._getscriptsource() # Get source code
		self._getcrontab() # Get crontab
		self.log = Tag(self._log) # Create tagged logger for files
		self._delayed_logs = [] # type: Optional[LogList]
		self._createlogs() # Create loggers

		if self.fork and hasattr(os, "fork"):
			self._tasks = [self.task("parent", str(os.getpid()))]

		self.log.sisyphus.delay.init(f"{misc.sysinfo.script_name} (max time {self.maxtime})")

		logmessage = self._logmessage()
		self.log.sisyphus.delay.init(logmessage)

		# Check for support of various thing we'd like to use
		if fcntl is None:
			self.log.sisyphus.init.delay.warning("Can't lock script file (module fcntl not available)")
		if self.fork and not hasattr(os, "fork"):
			self.log.sisyphus.init.delay.warning("Can't fork (function os.fork not available)")
			self.fork = False
		if not hasattr(signal, "SIGALRM"):
			self.log.sisyphus.init.delay.warning("Can't use signals (signal.SIGALRM not available)")
			self.fork = False
		if self.setproctitle and setproctitle is None:
			self.log.sisyphus.init.delay.warning("Can't set process title (module setproctitle not available)")

		if self.fork: # Forking mode?
			# Fork the process; the child will do the work; the parent will monitor the maximum runtime
			self.killpid = pid = os.fork()
			if pid: # We are the parent process
				self.process = Process.PARENT
				self.setproctitle(f"{logmessage} (max time {self.maxtime})")
				# set a signal to delay CTRL-C handling until the child has cleaned up
				signal.signal(signal.SIGINT, self._signal_interupt)
				# set a signal to wake us up to kill the child process after the maximum runtime
				if self.maxtime is not None:
					signal.signal(signal.SIGALRM, self._signal_timeout)
					signal.alarm(int(self.maxtime.total_seconds()))
				try:
					(pid, status) = os.waitpid(pid, 0) # Wait for the child process to terminate
					if self.maxtime is not None:
						signal.alarm(0) # Cancel maximum runtime alarm
				except misc.Timeout as exc:
					self._finished_timeout(exc)
					if self.exit_on_error:
						raise
					else:
						return # finish normally (or continue, if we're in repeat mode)
				except KeyboardInterrupt as exc:
					self._finished_break(exc)
					raise
				else:
					status = Status(status >> 8)
					if status is Status.UNEVENTFUL:
						self._finished_uneventful()
					elif status is Status.INTERRUPTED:
						exc = KeyboardInterrupt()
						self._finished_break(exc)
						raise exc
					elif status is Status.TIMEOUT:
						exc = misc.Timeout(self.maxtime)
						self._finished_timeout(exc)
						if self.exit_on_error:
							raise exc
					elif status is Status.FAILED:
						exc = RuntimeError("failed")
						self._finished_exception(exc)
						if self.exit_on_error:
							raise exc
					elif status is Status.SUCCESSFUL:
						self._finished_successful(None)
					return status # finish normally (or continue, if we're in repeat mode)
			# Here we are in the child process

			self.process = Process.CHILD
			self.setproctitle()
			task = self.task("child", misc.sysinfo.pid, self._run if self.repeat else None)
			self._tasks = [task] # This replaces the task stack inherited from the parent
			self.log.sisyphus.init.delay(f"forked worker child")
			self._init_sentry()
		else: # We didn't fork
			# set a signal to kill ourselves after the maximum runtime
			self._init_sentry()
			if self.maxtime is not None and hasattr(signal, "SIGALRM"):
				signal.signal(signal.SIGALRM, self._signal_timeout)
				signal.alarm(int(self.maxtime.total_seconds()))

		self.setproctitle("Setting up")
		self.notifystart()
		result = None
		try:
			with url.Context():
				self.setproctitle("Working")
				result = self.execute()
				signal.alarm(0) # Cancel alarm
		except misc.Timeout as exc:
			status = self._finished_timeout(exc)
			if not self.fork:
				raise
			result = str(exc)
		except KeyboardInterrupt as exc:
			status = self._finished_break(exc)
			if not self.fork:
				raise
			result = "interrupted"
		except Exception as exc:
			status = self._finished_exception(exc)
			result = f"failed with {misc.format_exception(exc)}"
			if not self.fork and self.exit_on_error:
				raise
		else:
			if result is None:
				status = self._finished_uneventful()
			else:
				status = self._finished_successful(result)
		self.notifyfinish(result)
		if self.fork:
			os._exit(status)
		return status

	def _kill_children(self) -> Set[int]:
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

			seconds = self.waitchildbreak.total_seconds()
			(gone, alive) = psutil.wait_procs(procs, timeout=seconds)

			# Send SIGKILL
			if alive:
				for p in alive:
					pids.add(p.pid)
					p.kill()
				(gone, alive) = psutil.wait_procs(alive, timeout=seconds)
				# Ignore whether any processes remain in the ``alive`` list
			return pids

	def _termination_message(self, exc, pids):
		if not pids:
			return f"Terminated: {exc}"
		elif len(pids) == 1:
			return f"Terminated child {misc.first(pids)}: {exc}"
		else:
			pidstr = ", ".join(str(pid) for pid in pids)
			return f"Ternminated children {pidstr}: {exc}"

	def _init_sentry(self) -> None:
		if self.sentry_dsn is not None:
			self.log.sisyphus.delay.init(f"Setting up sentry")
			try:
				import sentry_sdk
			except ImportError:
				self.log.sisyphus.delay.warning("Can't log to Sentry (module sentry_sdk not available)")
				return
			self.sentry_sdk = sentry_sdk
			self.sentry_sdk.init(
				self.sentry_dsn,
				traces_sample_rate=1.0,
				release=self.sentry_release,
				environment=self.sentry_environment,
				debug=self.sentry_debug,
			)
			if self.identifier:
				app_name = f"{self.projectname} {self.jobname} ({self.identifier})"
			else:
				app_name = f"{self.projectname} {self.jobname}"
			self.sentry_sdk.set_context(
				"app",
				{
					"app_identifier": f"{self.projectname}.{self.jobname}",
					"app_name": app_name,
					"app_start_time": self.starttime_utc,
				}
			)
			self.sentry_sdk.set_context(
				"os",
				{
					"name": misc.sysinfo.host_sysname,
					"version": misc.sysinfo.host_release,
					"kernel_version": misc.sysinfo.host_version,
				}
			)
			self.sentry_sdk.set_context(
				"Sisyphus",
				{
					"Script": misc.sysinfo.script_name,
					"PID": misc.sysinfo.pid,
					"Python": misc.sysinfo.python_executable,
				}
			)
			self.sentry_sdk.set_context(
				"User",
				{
					"Name": misc.sysinfo.user_name,
					"UID": misc.sysinfo.user_uid,
					"GID": misc.sysinfo.user_gid,
					"Home": misc.sysinfo.user_dir,
				}
			)

	def _finished_uneventful(self) -> Status:
		self.endtime = datetime.datetime.now()
		self.setproctitle("Finishing")
		if self.process is not Process.PARENT:
			self._write_healthfile(None)
			# log the result
			if self._exceptioncount:
				self.log.sisyphus.result.errors(None)
			else:
				self.log.sisyphus.result.delay.ok(None)
		return Status.UNEVENTFUL

	def _finished_successful(self, result: OptStr) -> Status:
		self.endtime = datetime.datetime.now()
		self.setproctitle("Finishing")
		# log the result
		if self.process is not Process.PARENT:
			self._write_healthfile(None)
			if self._exceptioncount:
				self.log.sisyphus.result.errors(result)
			else:
				# Throw away delayed logs.
				if self._delayed_logs is not None:
					self._delayed_logs = []
				self.log.sisyphus.result.ok(result)
		return Status.SUCCESSFUL

	def _finished_exception(self, exc: BaseException) -> Status:
		self.endtime = datetime.datetime.now()
		self.setproctitle("Handling exception")
		if self.process is not Process.PARENT:
			strexc = misc.format_exception(exc)
			self._write_healthfile(f"Failed with {strexc}")
			# log the error to the logfile, as we assume that :meth:`execute` didn't do it
			self.log.sisyphus.external(exc)
			self.log.sisyphus.result.fail(f"failed with {strexc}")
		return Status.FAILED

	def _finished_break(self, exc: KeyboardInterrupt) -> Status:
		self.endtime = datetime.datetime.now()
		self.setproctitle("Handling break")
		self._write_healthfile("Interrupted")
		if self.process is not Process.CHILD:
			# Don't log to email or mattermost
			self.log.sisyphus(exc)
			self.log.sisyphus.result.fail(f"failed with {misc.format_exception(exc)}")
		return Status.INTERRUPTED

	def _finished_timeout(self, exc: misc.Timeout) -> Status:
		self.endtime = datetime.datetime.now()
		self.setproctitle("Timeout")
		if self.process is not Process.CHILD:
			self._write_healthfile(f"Timeout after {self.maxtime}")

		if self.process is Process.PARENT:
			pids = self._kill_children()
		elif self.process is Process.SOLO:
			pids = set()

		if self.process is not Process.CHILD:
			if self.noisykills:
				self.log.email.mattermost(exc)
			else:
				self.log(exc)
			self.log.sisyphus.result.kill(self._termination_message(exc, pids))
		return Status.TIMEOUT

	def _signal_timeout(self, signum: int, frame: Optional[types.FrameType]) -> NoReturn:
		raise misc.Timeout(self.maxtime)

	def _signal_interupt(self, signum: int, frame: Optional[types.FrameType]) -> NoReturn:
		signal.alarm(0) # Cancel maximum runtime alarm
		# Give the child process time to log the stacktrace
		time.sleep(self.waitchildbreak.total_seconds())
		raise KeyboardInterrupt

	def _logmessage(self) -> str:
		logmessage = []
		for logger in self._loggers:
			name = logger.name()
			if name is not None:
				logmessage.append(name)
		logstr = ", ".join(logmessage)

		if logstr:
			return f"logging to {logstr}"
		else:
			return "no logging"

	def notifystart(self) -> None:
		if self.notify:
			misc.notifystart()

	def notifyfinish(self, result: OptStr) -> None:
		if self.notify:
			misc.notifyfinish(
				f"{self.projectname} {self.jobname}",
				f"finished after {self.endtime-self.starttime}",
				result or "uneventful",
			)

	def task(self, type:OptStr=None, name:OptStr=None, index:OptInt=None, count:OptInt=None, **data) -> "Task":
		"""
		:meth:`!task` is a context manager and can be used to specify subtasks.

		Arguments have the following meaning:

		``type`` : :class:`str` or :const:`None`
			The type of the task.

		``name`` : :class:`str` or :const:`None`
			The name of the task.

		``index`` : :class:`int` or :const:`None`
			If this task is one in a sequence of similar tasks, ``index`` should
			be the index of this task, i.e. the first task of this type has
			``index==0``, the second one ``index==1`` etc.

		``count`` : :class:`int` or :const:`None`
			If this task is one in a sequence of similar tasks and the total number
			of tasks is known, ``count`` should be the total number of tasks.

		``**data``
			Additional information about the task. This will be added to the
			Sentry breadcrumbs when logging to Sentry. Otherwise this is ignored.
		"""
		return Task(self, type=type, name=name, index=index, count=count, **data)

	def tasks(self, iterable: Iterable[T], type: OptStrFromCall=None, name: OptStrFromCall=None, data: OptDictFromCall=None) -> Generator[T, None, None]:
		"""
		:meth:`!tasks` iterates through ``iterable`` and calls :meth:`task` for
		each item. ``index`` and ``count`` will be passed to :meth:`task`
		automatically. ``type``, ``name`` and ``data`` will be used for the type,
		name and additional data of the task. They can either be constants
		(in which case they will be passed as is) or callables (in which case
		they will be called with the item to get the type/name/data).

		Example::

			import sys, operator

			items = list(sys.modules.items())
			for (name, module) in self.tasks(items, "module", operator.itemgetter(0)):
				self.log(f"module is {module}")

		The log output will look something like the following:

		.. sourcecode:: output

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
			realtype = type(item) if callable(type) else type
			realname = name(item) if callable(name) else name
			realdata = data(item) if callable(data) else data
			with self.task(realtype, realname, i, count, **(realdata or {})):
				yield item

	def makeproctitle(self, detail: OptStr=None) -> str:
		v = []
		if self.process is not Process.SOLO:
			v.append(self.process.name.lower())
		for task in self._tasks:
			v.append(str(task))
		title = " :: ".join(v)
		if not detail:
			return title
		if not title:
			return detail
		return f"{title} >> {detail}"

	def setproctitle(self, detail:OptStr=None) -> None:
		if self.proctitle and setproctitle:
			title = self.makeproctitle(detail)
			setproctitle.setproctitle(f"{self._originalproctitle} :: {title}")

	def _log(self, tags:Tags, obj:Any) -> None:
		"""
		Log ``obj`` to all loggers using ``tags`` as the list of tags.

		If we're in "delayed logs" mode, buffer up messages instead.
		"""
		timestamp = datetime.datetime.now()
		if isinstance(obj, BaseException) and "exc" not in tags:
			tags += ("exc",)
			self._exceptioncount += 1

		delayed = "delay" in tags
		if delayed:
			tags = tuple(tag for tag in tags if tag != "delay")
		if delayed and self._delayed_logs is not None:
			self._delayed_logs.append((timestamp, tags, self._tasks[:], obj))
		else:
			self._flush_logs()
			for logger in self._loggers:
				logger.log(timestamp, tags, self._tasks, obj)

	def _flush_logs(self) -> None:
		"""
		Flush delayed logs and switch of "delayed logs" mode.
		"""
		if self._delayed_logs is not None:
			for (timestamp, tags, tasks, obj) in self._delayed_logs:
				for logger in self._loggers:
					logger.log(timestamp, tags, tasks, obj)
			self._delayed_logs = None # No more delayed logs

	def _getscriptsource(self) -> None:
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

	def _getcrontab(self) -> None:
		"""
		Reads the current crontab into ``self.crontab``.
		"""
		with os.popen("crontab -l 2>/dev/null") as f:
			self.crontab = f.read()

	def _calc_nextrun(self) -> datetime.datetime:
		"""
		Calculate when the job should run next (in repeat mode).
		"""
		nextrun = self.nextrun
		if callable(nextrun):
			nextrun = nextrun()
		if nextrun is None:
			nextrun = datetime.timedelta(0)
		if isinstance(nextrun, (int, float)):
			nextrun = datetime.timedelta(seconds=nextrun)
		if isinstance(nextrun, datetime.timedelta):
			return datetime.datetime.now() + nextrun
		else:
			return nextrun

	def _calc_maxhealthcheckage(self) -> datetime.datetime:
		"""
		Calculate cut-off date for the health check.

		A health check file with a timestamp before that date will indicate an
		unhealthy job.
		"""
		cutoff = self.maxhealthcheckage
		if callable(cutoff):
			cutoff = cutoff()
		if cutoff is None:
			cutoff = datetime.datetime(datetime.MINYEAR, 1, 1)
		if isinstance(cutoff, (int, float)):
			cutoff = datetime.timedelta(seconds=cutoff)
		if isinstance(cutoff, datetime.timedelta):
			cutoff = datetime.datetime.now() - cutoff
		return cutoff

	def _createlogs(self) -> None:
		"""
		Create the logfile and the link to the logfile (if configured).
		"""
		self._loggers = []
		skipfilenames = [] # type: List[pathlib.Path]
		if self.toemail and self.fromemail and self.smtphost:
			# Use the email logger as the first logger, so that when sending the email (in :meth:`EmailLogger.close`) fails,
			# it will still be logged to the log file/stdout/stderr
			self._loggers.append(EmailLogger(self))
		if self.log2file:
			logfilename = self.logfilename()
			if logfilename is not None:
				# Create the logger for the log file
				self.logfileurl = str(url.Ssh(misc.sysinfo.user_name, misc.sysinfo.host_fqdn or misc.sysinfo.host_name, str(logfilename)))
				self._loggers.append(FileLogger(self, logfilename, self.encoding, self.errors, skipfilenames, self._formatlogline))
				skipfilenames.append(logfilename) # Note that we can still append URLs after the logger has been created, as the list object is shared
				# Create logger for links
				links = [
					(self.currentloglinkname, CurrentLinkLogger),
					(self.lastsuccessfulloglinkname, LastStatusLinkLogger, Status.SUCCESSFUL),
					(self.lastfailedloglinkname, LastStatusLinkLogger, Status.FAILED),
					(self.lastinterruptedloglinkname, LastStatusLinkLogger, Status.INTERRUPTED),
					(self.lasttimeoutloglinkname, LastStatusLinkLogger, Status.TIMEOUT),
				] # type: List[Union[Tuple[Callable[[], pathlib.Path], Type[Logger]], Tuple[Callable[[], pathlib.Path], Type[Logger], Status]]]
				for (makelinkfilename, logger, *additionalargs) in links:
					linkfilename = makelinkfilename()
					if linkfilename is not None:
						self._loggers.append(logger(self, logfilename, linkfilename, *additionalargs))
						skipfilenames.append(linkfilename)
				if self._healthfilename is not None:
					skipfilenames.append(self._healthfilename)
		if self.log2stdout:
			self._loggers.append(StreamLogger(self, sys.stdout, self._formatlogline))
		if self.log2stderr:
			self._loggers.append(StreamLogger(self, sys.stderr, self._formatlogline))
		if self.mattermost_url is not None and self.mattermost_channel is not None and self.mattermost_token is not None:
			self._loggers.append(MattermostLogger(self))
		if self.sentry_dsn is not None:
			self._loggers.append(SentryLogger(self))

	def _closelogs(self, status:Status) -> None:
		# Note that in forking mode the child process inherits the delayed log
		# messages of the parent process. If both processes would log a
		# non-delayed message, the inherited messages would be output twice.
		# To avoid this problem, we clear the delayed log queue in the parent
		# before continuing.
		if self._delayed_logs:
			self._delayed_logs = []
		index = 0
		while index < len(self._loggers):
			# Don't remove the logger from the list immediately
			# In this way, log messages that the logger outputs during closing will
			# be logged by the logger itself (i.e. logfile cleanup will be logged
			# in the logfile)
			logger = self._loggers[index]
			if logger.close(status):
				# Logger has closed, so remove it
				del self._loggers[index]
			else:
				# Logger didn't close, keep it and go to the next one
				index += 1

	def _write_healthfile(self, error:OptStr) -> None:
		# Write the file that is used for the healthcheck
		if self._healthfilename:
			error = "" if error is None else error + "\n"
			try:
				self._healthfilename.write_text(error, encoding=self.encoding, errors=self.errors)
			except FileNotFoundError:
				self._healthfilename.parent.mkdir(parents=True)
				self._healthfilename.write_text(error, encoding=self.encoding, errors=self.errors)


class Task:
	"""
	A subtask of a :class:`Job`.
	"""

	ul4_attrs = {"index", "count", "type", "name", "starttime", "endtime", "success", "data"}

	def __init__(self, job:Job, type:OptStr=None, name:OptStr=None, index:OptInt=None, count:OptInt=None, **data):
		"""
		Create a :class:`!Task` object. For the meaning of the parameters see
		:meth:`Job.task`.
		"""
		self.job = job
		self.type = type
		self.name = name
		self.index = index
		self.count = count
		self.data = data
		self.starttime = None # type: Optional[datetime.datetime]
		self.endtime = None # type: Optional[datetime.datetime]
		self.success = None # type: Optional[bool]

	def __enter__(self) -> "Task":
		self.starttime = datetime.datetime.now()
		self.job._tasks.append(self)
		self.job.setproctitle()
		for logger in self.job._loggers:
			logger.taskstart(self.job._tasks)
		return self

	def __exit__(self, type:Optional[Type[BaseException]], value:Optional[BaseException], traceback:Optional[types.TracebackType]) -> None:
		self.endtime = datetime.datetime.now()
		self.success = type is None
		for logger in self.job._loggers:
			logger.taskend(self.job._tasks)
		self.job._tasks.pop()
		self.job.setproctitle()

	def __str__(self) -> str:
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

	def asdict(self) -> Dict[str, Any]:
		return dict(
			type=self.type,
			name=str(self.name) or None,
			index=self.index,
			count=self.count,
			starttime=self.starttime,
			endtime=self.endtime,
		)

	def __repr__(self) -> str:
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} type={self.type!r} name={self.name!r} at {id(self):#x}"


class Tag:
	"""
	A :class:`!Tag` object can be used to call a function with an additional list
	of tags. Tags can be added via :meth:`__getattr__` or :meth:`__getitem__` calls.
	"""
	def __init__(self, func:Callable, *tags:str):
		self.func = func
		self.tags = tags
		self._map = {} # type: Dict[str, Tag]

	def __getattr__(self, tag:str) -> "Tag":
		if tag in self.tags: # Avoid duplicate tags
			return self
		if tag not in self._map:
			newtag = Tag(self.func, *(self.tags + (tag,)))
			self._map[tag] = newtag
			return newtag
		else:
			return self._map[tag]

	__getitem__ = __getattr__

	def __call__(self, *args, **kwargs) -> "Tag":
		return self.func(self.tags, *args, **kwargs)


class Logger:
	"""
	A :class:`Logger` is called by the :class:`Job` for each logging event.
	"""

	def name(self) -> OptStr:
		"""
		A name for the logger (using in reporting)
		"""
		return None

	def log(self, timestamp:datetime.datetime, tags:Tags, tasks:List[Task], text:str) -> None:
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
			The log text. This can be any object. If it's not a string it will be
			converted to a string via :func:`pprint.pformat` (or
			:func:`traceback.format_exception` if it's an exception)
		"""

	def taskstart(self, tasks:List[Task]) -> None:
		"""
		Called by the :class:`Job` when a new subtask has been started.

		``tasks`` is the stack of currently active tasks (so ``tasks[-1]`` is
		the task that has been started).
		"""

	def taskend(self, tasks:List[Task]) -> None:
		"""
		Called by the :class:`Job` when a subtask is about to end.

		``tasks`` is the stack of currently active tasks (so ``tasks[-1]`` is
		the task that's about to end).
		"""

	def close(self, status:Status) -> bool:
		"""
		Called by the :class:`Job` when job execution has finished.

		``status`` (a :class:`Status`) is the result status of the job run.

		Return whether the logfile has been closed. (All normal loggers
		will close except ``stdout`` and ``stderr`` loggers).
		"""


class StreamLogger(Logger):
	"""
	Logger that writes logging events into an open file-like object. Is is used
	for logging to ``stdout`` and ``stderr``.
	"""

	def __init__(self, job:Job, stream:TextIO, linetemplate:ul4c.Template) -> None:
		self.job = job
		self.stream = stream
		self.linetemplate = linetemplate
		self.lineno = 1 # Current line number

	def __repr__(self) -> str:
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} stream={self.stream!r} at {id(self):#x}>"

	def name(self) -> str:
		return self.stream.name

	def log(self, timestamp:datetime.datetime, tags:Tags, tasks:List[Task], text:str) -> None:
		for line in _formatlines(text):
			line = self.linetemplate.renders(line=line, time=timestamp, tags=tags, tasks=tasks, sysinfo=misc.sysinfo, job=self.job, env=env)
			self.stream.write(line)
			self.stream.write("\n")
			self.lineno += 1
		self.stream.flush()

	def close(self, status:Status) -> bool:
		return False


class FileLogger(StreamLogger):
	"""
	Logger that writes logging events into a file specified via an
	:class:`~ll.url.URL` object. This is used for logging to the standard log
	file.
	"""

	def __init__(self, job:Job, filename:pathlib.Path, encoding:str, errors:str, skipfilenames:List[pathlib.Path], linetemplate:ul4c.Template) -> None:
		self.filename = filename
		try:
			file = filename.open("w", encoding=encoding, errors=errors)
		except FileNotFoundError:
			filename.parent.mkdir(parents=True)
			file = filename.open("w", encoding=encoding, errors=errors)
		StreamLogger.__init__(self, job, file, linetemplate)
		self.skipfilenames = skipfilenames

	def __repr__(self) -> str:
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} filename={str(self.filename)!r} at {id(self):#x}>"

	def close(self, status:Status) -> None:
		keepfilelogs = self.job.keepfilelogs
		compressfilelogs = self.job.compressfilelogs

		if self.job.process is not Process.CHILD and (keepfilelogs is not None or compressfilelogs is not None):
			now = datetime.datetime.now()
			keepthreshold = now - keepfilelogs # Files older that this will be deleted
			compressthreshold = now - compressfilelogs # Files older that this will be compressed
			logdir = pathlib.Path(self.stream.name).parent
			removedany = False
			compressedany = False
			warnedcompressany = False
			for filename in sorted(list(logdir.iterdir())):
				# Decide what to do with this file
				# (Note that this might delete/compress files that were not produced by sisyphus)
				if filename not in self.skipfilenames:
					# If the file is not the logfile or a link to it ...
					mdate = get_mtime(filename)
					if mdate < keepthreshold:
						# ... and it's to old to keep it, delete it
						if not removedany: # Only log this line for the first logfile we remove
							# This will still work, as the file isn't closed yet.
							self.job.log.sisyphus.delay.info(f"Removing logfiles older than {keepfilelogs}")
							removedany = True
						self.remove(filename)
					elif mdate < compressthreshold:
						# ... and it's to old to keep it in uncompressed, compress it
						if filename.suffix not in {".gz", ".bz2", ".xz"}:
							if (self.job.compressmode == "gzip" and gzip is None) or (self.job.compressmode == "gzip2" and bz2 is None) or (self.job.compressmode == "lzma" and lzma is None):
								if not warnedcompressany:
									self.job.log.sisyphus.delay.warning(f"{self.job.compressmode} compression not available, leaving log files uncompressed")
									warnedcompressany = True
							else:
								if not compressedany:
									self.job.log.sisyphus.delay.info(f"Compressing logfiles older than {compressfilelogs} via {self.job.compressmode}")
									compressedany = True
								self.compress(filename)
			if removedany or compressedany:
				self.job.log.sisyphus.delay.info("Old logfiles cleaned up")
		if self.job.process is not Process.CHILD and status is Status.UNEVENTFUL:
			self.job.log.sisyphus.delay.info("Going to delete current logfile")
		# Close the stream now, so that we're able to delete it (even on Windows)
		self.stream.close()
		if self.job.process is not Process.CHILD:
			if status is Status.UNEVENTFUL:
				# Remove current log file in case of a uneventful run
				self.filename.unlink()
		return True

	def remove(self, filename:pathlib.Path) -> None:
		self.job.log.sisyphus.delay.info(f"Removing logfile {filename}")
		filename.unlink()

	def compress(self, filename:pathlib.Path, bufsize:int=65536) -> None:
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

		self.job.log.sisyphus.delay.info(f"Compressing logfile {filename}")
		compressedfilename = pathlib.Path(str(filename) + ext)
		with filename.open("rb") as logfile:
			with compressor(compressedfilename, mode="wb") as compressedlogfile:
				while True:
					data = logfile.read(bufsize)
					if not data:
						break
					compressedlogfile.write(data)
		# Copy timestamp of original file to the compressed file
		# (otherwise removal of the compressed log file would be delayed)
		times = get_utime(filename)
		set_utime(compressedfilename, *times)
		# Remove uncompressed log file
		filename.unlink()


class LinkLogger(Logger):
	"""
	Baseclass of all loggers that handle links to the log file.
	"""
	def __init__(self, job:Job, filename:pathlib.Path, linkname:pathlib.Path):
		self.job = job
		self.filename = filename
		self.linkname = linkname

	def __repr__(self) -> str:
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} linkname={str(self.linkname)!r} at {id(self):#x}>"

	def _makelink(self) -> None:
		linkname = self.linkname.absolute()
		filename = self.filename
		try:
			filename = filename.absolute().relative_to(linkname.parent)
		except ValueError:
			pass
		try:
			linkname.symlink_to(filename)
		except FileExistsError:
			linkname.unlink()
			linkname.symlink_to(filename)

	def close(self, status:Status) -> bool:
		return True


class CurrentLinkLogger(LinkLogger):
	"""
	Logger that handles the link to the current log file.
	"""
	def __init__(self, job:Job, filename:pathlib.Path, linkname:pathlib.Path):
		super().__init__(job, filename, linkname)
		self._makelink()


class LastStatusLinkLogger(LinkLogger):
	"""
	Logger that handles the link to the log file for a specific job status.
	"""

	def __init__(self, job:Job, filename:pathlib.Path, linkname:pathlib.Path, status:Status):
		super().__init__(job, filename, linkname)
		self.status = status

	def __repr__(self) -> str:
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} linkname={str(self.linkname)!r} status={self.status.name} at {id(self):#x}>"

	def close(self, status:Status) -> bool:
		if self.job.process is not Process.CHILD and status is self.status:
			self._makelink()
		return True


class EmailLogger(Logger):
	"""
	Logger that handles sending an email report of the job run.
	"""

	def __init__(self, job:Job):
		self.job = job
		self.filename = None
		self.file = None
		self.encoder = None

	def name(self) -> str:
		return "<email>"

	def log(self, timestamp:datetime.datetime, tags:Tags, tasks:List[Task], text:str) -> None:
		if "email" in tags or "external" in tags:
			if self.file is None:
				filename = self.job.emailfilename()
				try:
					file = filename.open("w", encoding="utf-8", buffering=1)
				except FileNotFoundError:
					filename.parent.mkdir(parents=True)
					file = filename.open("w", encoding="utf-8", buffering=1)
				self.file = file
				self.encoder = ul4on.Encoder()
			data = {"timestamp": timestamp, "tags": tags, "tasks": [t.asdict() for t in tasks]}
			if isinstance(text, BaseException):
				data["type"] = "exception"
				data["class"] = misc.format_class(text)
				data["value"] = str(text) or None
				data["traceback"] = _formattraceback(text)
			else:
				data["type"] = "message"
				data["message"] = "\n".join(_formatlines(text))
			self.file.write(self.encoder.dumps(data))
			self.file.write("\n")
			self.file.flush()

	def _load_dump(self, process:Process) -> Generator[Any, None, None]:
		decoder = ul4on.Decoder()
		filename = self.job.emailfilename(process)
		try:
			with filename.open("r", encoding="utf-8") as f:
				while True:
					try:
						yield decoder.load(f)
					except EOFError:
						break
		except FileNotFoundError:
			pass

	def close(self, status:Status) -> bool:
		if self.file is not None:
			self.file.close()
		else:
			# If we never wrote any logs, remove the log file (shoudn't exist anyway)
			try:
				self.job.emailfilename().unlink()
			except FileNotFoundError:
				pass
		if self.job.process is not Process.CHILD:
			if self.job.process is Process.SOLO:
				processes = (Process.SOLO,)
			else:
				processes = (Process.CHILD, Process.PARENT)

			log = sorted(
				itertools.chain.from_iterable(self._load_dump(p) for p in processes),
				key=operator.itemgetter("timestamp"),
			)

			# Without log messages, we have nothing to do
			if log:
				countexceptions = 0
				countmessages = 0
				for data in log:
					if data["type"] == "exception":
						countexceptions += 1
					else:
						countmessages += 1

				# Limit size of email
				log = log[:self.job.maxemailerrors]

				jsondata = dict(
					projectname=self.job.projectname,
					jobname=self.job.jobname,
					identifier=self.job.identifier,
					log=log,
					countexceptions=countexceptions,
					countmessages=countmessages,
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
					starttime=self.job.starttime,
					endtime=self.job.endtime,
					logfileurl=self.job.logfileurl,
				)
				variables = dict(
					job=self.job,
					env=env,
					sysinfo=misc.sysinfo,
					log=log,
					countexceptions=countexceptions,
					countmessages=countmessages,
				)
				emailsubject = self.job._formatemailsubject.renders(**variables)
				emailbodytext = self.job._formatemailbodytext.renders(**variables)
				emailbodyhtml = self.job._formatemailbodyhtml.renders(**variables)

				textpart = text.MIMEText(emailbodytext)
				htmlpart = text.MIMEText(emailbodyhtml, _subtype="html")
				jsonpart = application.MIMEApplication(json.dumps(jsondata, cls=DatetimeEncoder).encode("utf-8"), _subtype="json", _encoder=encoders.encode_base64)
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

			# Remove files
			for p in processes:
				try:
					self.job.emailfilename(p).unlink()
				except FileNotFoundError:
					pass
		return True


class MattermostLogger(Logger):
	"""
	Logger that logs messages to a Mattermost chat channel.
	"""

	def __init__(self, job:Job):
		self.job = job

	def name(self) -> str:
		return "<mattermost>"

	def log(self, timestamp:datetime.datetime, tags:Tags, tasks:List[Task], text:str) -> None:
		if "mattermost" in tags or "external" in tags:
			import requests
			if isinstance(text, BaseException):
				message = _formattraceback(text)
				type = "exc"
			elif not isinstance(text, str):
				message = pprint.pformat(text)
				type = "obj"
			else:
				message = text
				type = "str"
			message = message.strip("\n")
			if len(message) > 14000:
				message = message[:14000] + "..."
			vars = dict(
				job=self.job,
				env=env,
				sysinfo=misc.sysinfo,
				type=type,
				message=message,
				time=timestamp,
				tags=tags,
				tasks=tasks,
			)
			title = self.job._formatmattermosttitle.renders(**vars)
			message = self.job._formatmattermostmessage.renders(**vars)

			message = f"# {title}\n{message}"

			requests.post(
				self.job.mattermost_url,
				headers={
					"Authorization": f"Bearer {self.job.mattermost_token}",
				},
				json={
					"channel_id": self.job.mattermost_channel,
					"message": message[:15000],
				}
			)

	def close(self, status:Status) -> bool:
		return True


class SentryLogger(Logger):
	"""
	Logger that logs messages and exceptions to Sentry.
	"""

	def __init__(self, job:Job):
		self.job = job
		
	def name(self) -> str:
		return "<sentry>"

	def _task_description(self, task:Task) -> str:
		v = ""
		if task.type is not None and task.name is not None:
			v = str(task.name)
		if task.index is not None:
			v += f" [{task.index+1:,}"
			if task.count is not None:
				v += f"/{task.count:,}"
			v += "]"
		return v or "?"

	def log(self, timestamp:datetime.datetime, tags:Tags, tasks:List[Task], text:str) -> None:
		if "sentry" in tags or "external" in tags:
			sentry = self.job.sentry_sdk
			if sentry is not None:
				with sentry.push_scope() as scope:
					if isinstance(text, BaseException):
						scope.level = "fatal"
					else:
						for level in ("fatal", "error", "warning", "info", "debug"):
							if level in tags:
								scope.level = level
								break
						else:
							scope.level = "info"
					for tag in tags:
						scope.set_tag(f"sisphus.tag.{tag}", "true")
					for task in tasks:
						sentry.add_breadcrumb(
							type="debug",
							category=task.type or task.name,
							message=self._task_description(task),
							data={k: str(v) for (k, v) in task.data.items()},
						)
					if isinstance(text, BaseException):
						sentry.capture_exception(text)
					else:
						if not isinstance(text, str):
							text = pprint.pformat(text)
						sentry.capture_message(text, level="warning")
					sentry.flush()

	def close(self, status:Status) -> bool:
		return True


###
### High-level interface for starting jobs
###

def execute(job:Job) -> None:
	"""
	Execute the job ``job`` once or repeatedly.
	"""
	job._handleexecution()


def executewithargs(job:Job, args:Optional[List[str]]=None) -> None:
	"""
	Execute the job ``job`` once or repeatedly with command line arguments.

	``args`` are the command line arguments (:const:`None` results in
	``sys.argv`` being used).
	"""
	job.parseargs(args)
	job._handleexecution()
