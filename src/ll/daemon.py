# -*- coding: utf-8 -*-

## Copyright 2007-2012 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


r"""
This module can be used on UNIX to fork a daemon process. It is based on
`Jürgen Hermann's Cookbook recipe`__.

__ http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012

An example script might look like this::

	from ll import daemon

	counter = daemon.Daemon(
		stdin="/dev/null",
		stdout="/tmp/daemon.log",
		stderr="/tmp/daemon.log",
		pidfile="/var/run/counter/counter.pid",
		user="nobody"
	)

	if __name__ == "__main__":
		if counter.service():
			import sys, os, time
			sys.stdout.write("Daemon started with pid {}\n".format(os.getpid()))
			sys.stdout.write("Daemon stdout output\n")
			sys.stderr.write("Daemon stderr output\n")
			c = 0
			while True:
				sys.stdout.write('{}: {}\n'.format(c, time.ctime(time.time())))
				sys.stdout.flush()
				c += 1
				time.sleep(1)
"""


import sys, os, signal, pwd, grp, argparse


__docformat__ = "reStructuredText"


class Options(object):
	def __init__(self, **values):
		self.__dict__.update(values)


class Daemon(object):
	"""
	The :class:`Daemon` class provides methods for starting and stopping a
	daemon process as well as handling command line arguments.
	"""
	def __init__(self, stdin="/dev/null", stdout="/dev/null", stderr="/dev/null", pidfile=None, user=None, group=None):
		"""
		The :var:`stdin`, :var:`stdout`, and :var:`stderr` arguments are file
		names that will be opened and be used to replace the standard file
		descriptors in ``sys.stdin``, ``sys.stdout``, and ``sys.stderr``.
		These arguments are optional and default to ``"/dev/null"``. Note that
		stderr is opened unbuffered, so if it shares a file with stdout then
		interleaved output may not appear in the order that you expect.

		:var:`pidfile` must be the name of a file. :meth:`start` will write
		the pid of the newly forked daemon to this file. :meth:`stop` uses this
		file to kill the daemon.

		:var:`user` can be the name or uid of a user. :meth:`start` will switch
		to this user for running the service. If :var:`user` is ``None`` no
		user switching will be done.

		In the same way :var:`group` can be the name or gid of a group.
		:meth:`start` will switch to this group.
		"""
		self.options = Options(
			stdin=stdin,
			stdout=stdout,
			stderr=stderr,
			pidfile=pidfile,
			user=user,
			group=group,
		)

	def openstreams(self):
		"""
		Open the standard file descriptors stdin, stdout and stderr as specified
		in the constructor.
		"""
		si = open(self.options.stdin, "r")
		so = open(self.options.stdout, "a+")
		se = open(self.options.stderr, "a+", 0)
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())

	def handlesighup(self, signum, frame):
		"""
		Handle a ``SIG_HUP`` signal: Reopen standard file descriptors.
		"""
		self.openstreams()

	def handlesigterm(self, signum, frame):
		"""
		Handle a ``SIG_TERM`` signal: Remove the pid file and exit.
		"""
		if self.options.pidfile is not None:
			try:
				os.remove(self.options.pidfile)
			except Exception:
				pass
		sys.exit(0)

	def switchuser(self, user, group):
		"""
		Switch the effective user and group. If :var:`user` and :var:`group` are
		both :const:`None` nothing will be done. :var:`user` and :var:`group`
		can be an :class:`int` (i.e. a user/group id) or :class:`str`
		(a user/group name).
		"""
		if group is not None:
			if isinstance(group, str):
				group = grp.getgrnam(group).gr_gid
			os.setegid(group)
		if user is not None:
			if isinstance(user, str):
				user = pwd.getpwnam(user).pw_uid
			os.seteuid(user)
			if "HOME" in os.environ:
				os.environ["HOME"] = pwd.getpwuid(user).pw_dir

	def start(self):
		"""
		Daemonize the running script. When this method returns the process is
		completely decoupled from the parent environment.
		"""
		# Finish up with the current stdout/stderr
		sys.stdout.flush()
		sys.stderr.flush()

		# Do first fork
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0) # Exit first parent
		except OSError as exc:
			sys.exit("{}: fork #1 failed: ({}) {}\n".format(sys.argv[0], exc.errno, exc.strerror))

		# Decouple from parent environment
		os.chdir("/")
		os.umask(0)
		os.setsid()

		# Do second fork
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0) # Exit second parent
		except OSError as exc:
			sys.exit("{}: fork #2 failed: ({}) {}\n".format(sys.argv[0], exc.errno, exc.strerror))

		# Now I am a daemon!

		# Switch user
		self.switchuser(self.options.user, self.options.group)

		# Redirect standard file descriptors (will belong to the new user)
		self.openstreams()

		# Write pid file (will belong to the new user)
		if self.options.pidfile is not None:
			open(self.options.pidfile, "wb").write(str(os.getpid()))

		# Reopen file descriptors on SIGHUP
		signal.signal(signal.SIGHUP, self.handlesighup)

		# Remove pid file and exit on SIGTERM
		signal.signal(signal.SIGTERM, self.handlesigterm)

	def stop(self):
		"""
		Send a ``SIGTERM`` signal to a running daemon. The pid of the daemon
		will be read from the pidfile specified in the constructor.
		"""
		if self.options.pidfile is None:
			sys.exit("no pidfile specified")
		try:
			pidfile = open(self.options.pidfile, "rb")
		except IOError as exc:
			sys.exit("can't open pidfile {}: {}".format(self.options.pidfile, str(exc)))
		data = pidfile.read()
		try:
			pid = int(data)
		except ValueError:
			sys.exit("mangled pidfile {}: {}".format(self.options.pidfile, data))
		os.kill(pid, signal.SIGTERM)

	def argparser(self):
		"""
		Return an :mod:`argparse` parser for parsing the command line arguments.
		This can be overwritten in subclasses to add more arguments.
		"""
		p = argparse.ArgumentParser(description="Start, stop or restart a daemon process")
		p.add_argument("action", help="Action to execute", choices=("start", "stop", "restart", "run"))
		p.add_argument("--pidfile", dest="pidfile", help="PID filename (default %(default)s)", default=self.options.pidfile)
		p.add_argument("--stdin", dest="stdin", help="stdin filename (default %(default)s)", default=self.options.stdin)
		p.add_argument("--stdout", dest="stdout", help="stdout filename (default %(default)s)", default=self.options.stdout)
		p.add_argument("--stderr", dest="stderr", help="stderr filename (default %(default)s)", default=self.options.stderr)
		p.add_argument("--user", dest="user", help="user name or id (default %(default)s)", default=self.options.user)
		p.add_argument("--group", dest="group", help="group name or id (default %(default)s)", default=self.options.group)
		return p

	def service(self, args=None):
		"""
		Handle command line arguments and start or stop the daemon accordingly.

		:var:`args` must be a list of command line arguments (including the
		program name in ``args[0]``). If :var:`args` is :const`None` or
		unspecified ``sys.argv`` is used.

		The return value is true when a starting option has been specified as the
		command line argument, i.e. if the daemon should be started.

		The :mod:`argparse` arguments are available afterwards as ``self.args``.
		"""
		p = self.argparser()
		self.args = p.parse_args(args)
		if self.args.action == "run":
			return True
		elif self.args.action == "restart":
			self.stop()
			self.start()
			return True
		elif self.args.action == "start":
			self.start()
			return True
		elif self.args.action == "stop":
			self.stop()
			return False
