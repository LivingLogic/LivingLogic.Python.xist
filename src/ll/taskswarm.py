# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2025-2026 by LivingLogic AG, Bayreuth/Germany
## Copyright 2025-2026 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Overview
========

:mod:`ll.taskswarm` provides an easy way to execute multiple Python functions in
parallel using the :mod:`multiprocessing` module. It is designed to improve
performance by utilizing multiple CPU cores efficiently.


Features
========

-	Parallel execution of multiple functions or other callables;

-	Automatic process management;

-	Supports passing arguments to functions;

-	Configurable number of parallel processes;

-	Tasks can dynamically add new tasks during execution;

-	Live progress output on the terminal (and in the iTerm2 session status
	via :mod:`ll.iterm2`).


Limitations
===========

-	Functions/callables, their arguments (and the object in case of bound
	methods) must be picklable (depending on the start method used by
	:mod:`multiprocessing`).

-	No return values are collected; tasks are executed for their side effects
	(like created files, executed HTTP or database requests).

-	Overhead from creating processes may outweigh benefits of parallelization.


Usage
=====

A task is a function (or other callable) that gets a :class:`Task` object as
its first argument. It may report its progress via :meth:`Task.log` and
submit further tasks via :meth:`Task.submit`. The task is finished when the
function returns (or raises an exception).

Tasks are submitted to a :class:`Swarm` object inside a ``with`` block.
The tasks are started when the ``with`` block is exited, so the ``with``
block itself only collects the initial tasks::

	import sys, json, pathlib

	from ll import taskswarm


	def walk(task, dir):
		task.log(f"Walking {dir}")
		for file in dir.iterdir():
			if file.is_dir():
				task.submit(walk, file.name, file)
			elif file.suffix == ".json":
				task.submit(prettyprint, file.name, file)
		task.log(f"Walked {dir}")


	def prettyprint(task, file):
		data = json.loads(file.read_text())
		file.write_text(json.dumps(data, indent="\t"))
		task.log("Pretty printed")


	if __name__ == "__main__":
		with taskswarm.Swarm("Pretty printing JSON files", 20, False) as swarm:
			dir = pathlib.Path(sys.argv[1])
			swarm.submit(walk, str(dir), dir)

Each task runs in its own :class:`multiprocessing.Process`. At most
``processes`` (20 in the example) tasks run at the same time, additional tasks
are queued until a slot becomes free. The swarm is finished when all tasks
(including those submitted by other tasks) have finished.
Then a summary of the total, mean and longest wait and run times is printed.


Output
======

While the swarm is running, its progress is printed to ``stdout``. There are
two output modes (selected via the ``continuous`` argument of
:class:`Swarm`):

Continuous output (``continuous=True``)
	Every event (a task being started, logging a message or finishing) is
	printed as a new line, prefixed with the elapsed time and the number of
	waiting, running and finished tasks. This mode is appropriate when the
	output is redirected to a file or a CI log.

In-place output (``continuous=False``)
	One line per process slot is reserved on the terminal and updated in
	place (via ANSI cursor movement) with the current state of the task
	running in that slot. Below these lines a status line shows the numbers
	of waiting, running and finished tasks and the current and mean load
	(i.e. the number of running processes). This mode requires a terminal
	that understands ANSI escape sequences.

In both modes values are colored via ANSI escape sequences (see
:func:`format`), unless :data:`plain_output` is true, which is the case on
Windows or if ``stdout`` isn't a terminal.

When running in iTerm2, the title of the swarm and the current progress are
also shown in the iTerm2 session status (see
:func:`ll.iterm2.set_session_status`), so that the progress is visible in the
tab even when another tab is active.
"""

import sys, datetime, operator, pathlib, multiprocessing

from ll import iterm2


#: The current directory at import time. :func:`format` prints paths relative
#: to this directory (if possible).
currentdir = pathlib.Path.cwd()

#: If true, :func:`format` and :func:`format_sep` don't emit ANSI escape
#: sequences. This is the case on Windows or if ``stdout`` isn't a terminal.
plain_output = (sys.platform == "win32" or not sys.stdout.isatty())


def format(obj):
	"""
	Format ``obj`` for terminal output with ANSI colors.

	The formatting depends on the type of ``obj``: :class:`pathlib.Path`
	objects are output relative to :data:`currentdir` (if possible) in
	yellow, numbers and :class:`~datetime.datetime` objects in bold magenta,
	:class:`~datetime.timedelta` objects as ``HH:MM:SS`` with the leading
	zeros in normal magenta and the rest in bold magenta. Everything else is
	simply converted with :class:`str`.

	If :data:`plain_output` is true, no ANSI escape sequences are output.
	"""

	if plain_output:
		return str(obj)
	else:
		if isinstance(obj, pathlib.Path):
			try:
				obj = obj.relative_to(currentdir)
			except ValueError:
				pass
			return f"\033[33m{obj}\033[0m"
		if isinstance(obj, int):
			return f"\033[1;35m{obj:,}\033[0m"
		elif isinstance(obj, float):
			return f"\033[1;35m{obj:,.01f}\033[0m"
		elif isinstance(obj, datetime.datetime):
			return f"\033[1;35m{obj}\033[0m"
		elif isinstance(obj, datetime.timedelta):
			value = str(obj).split('.')[0]
			value = value.rjust(8, "0")
			if not value.startswith("0"):
				value = f"\033[35m{value}\033[0m"
			else:
				for (i, c) in enumerate(value):
					if c not in "0:":
						value = f"\033[35m{value[:i]}\033[1;35m{value[i:]}\033[0m"
						break
				else:
					value = f"\033[35m{value}\033[0m"
			return value
		else:
			return str(obj)


def format_sep(text):
	"""
	Format the separator ``text`` for terminal output (i.e. in dark grey).

	If :data:`plain_output` is true, no ANSI escape sequences are output.
	"""

	if plain_output:
		return text
	else:
		return f"\033[30;1m{text}\033[0m"


def _run_task(func, task, *args, **kwargs):
	"""
	Run the task function ``func`` in the task process and report to the
	swarm when it's finished.

	This is the target of the :class:`multiprocessing.Process` created for
	each task. If ``func`` raises an exception, the swarm is informed about
	the failure (so that it doesn't wait for the task forever) and the
	exception is reraised (so that :mod:`multiprocessing` prints the
	traceback).
	"""

	try:
		func(task, *args, **kwargs)
	except BaseException as exc:
		task._done(f"Failed with {exc.__class__.__qualname__}: {exc}")
		raise
	else:
		task._done(None)


class Swarm:
	"""
	A :class:`!Swarm` executes tasks in parallel processes.

	A :class:`!Swarm` is used as a context manager: Inside the ``with`` block
	tasks are submitted via :meth:`submit`, when the block is exited the tasks
	are executed (and further tasks submitted by running tasks via
	:meth:`Task.submit` are executed too). The ``with`` block ends when all
	tasks are done. If an exception is raised inside the ``with`` block, no
	tasks are started.

	The constructor arguments are:

	``title`` : string
		The title of the swarm. It is shown in the iTerm2 session status while
		the swarm is running.

	``processes`` : int
		The maximum number of tasks that run in parallel.

	``continuous`` : bool
		Selects the output mode: continuous output (one line per event) if
		true, in-place output (one line per process slot) if false. See the
		module documentation for details.

	After the ``with`` block the attributes :attr:`tasks`, :attr:`run_time`
	and :attr:`mean_load` can be used to inspect the result.
	"""

	def __init__(self, title, processes, continuous):
		self.title = title
		self.process_id = 0
		self.count_done = 0
		self.started_at = None
		self.finished_at = None
		self.total_load = 0
		self.count_events = 0
		self.tasks = {} # All tasks (by `process_id`)
		self.running_tasks = {} # Task that are currently running (by `process_id`)
		self.pending_tasks = {} # Task that have been submitted, but are still waiting for on open slot (by `process_id`)
		self.slots = {} # Output line (by `process_id`)
		self.free_slots = set(range(processes))
		self.queue = multiprocessing.Queue()
		self.processes = processes
		self.continuous = continuous

	@property
	def current_load(self):
		"""
		The number of tasks currently running.
		"""

		return len(self.running_tasks)

	@property
	def mean_load(self):
		"""
		The mean number of running tasks over the runtime of the swarm (or
		``None`` if the swarm hasn't run yet).

		The load is sampled whenever a task event (start, log message or
		done) is processed, so this is an average over events, not over time.
		"""

		return self.total_load/self.count_events if self.count_events else None

	@property
	def run_time(self):
		"""
		The total run time of the swarm as a :class:`~datetime.timedelta`
		(or ``None`` if the swarm hasn't finished yet).
		"""

		return self.finished_at - self.started_at if self.finished_at is not None and self.started_at is not None else None

	def submit(self, func, name, *args, **kwargs):
		"""
		Submit a new task to the swarm and return the :class:`Task` object.

		``func`` is the callable that gets executed in a separate process. It
		will be called as ``func(task, *args, **kwargs)`` (where ``task`` is
		the :class:`Task` object). The task is finished when ``func`` returns
		or raises an exception. ``name`` is the name of the task used in the
		output.

		Tasks submitted before the ``with`` block is exited are started (in
		submission order, as far as free slots are available) when the block
		is exited. This method may only be called from the main process; a
		running task submits further tasks via :meth:`Task.submit`.
		"""

		task = Task(self.process_id, self.queue, name)
		process = multiprocessing.Process(target=_run_task, name=name, args=(func, task) + args, kwargs=kwargs)
		self.pending_tasks[task.process_id] = (process, task)
		self.tasks[task.process_id] = (process, task)
		self.process_id += 1
		return task

	def _schedule_pending_tasks(self):
		"""
		Start pending tasks (in submission order) as long as there are free
		slots.
		"""

		while len(self.running_tasks) < self.processes and self.pending_tasks:
			for (process, task) in self.pending_tasks.values():
				break
			self.running_tasks[task.process_id] = (process, task)
			del self.pending_tasks[task.process_id]
			task.started_at = datetime.datetime.now()
			slot = min(self.free_slots)
			self.free_slots.remove(slot)
			self.slots[task.process_id] = slot
			self._print(datetime.datetime.now(), format_sep("Started"), task=task)
			process.start()

	def _print(self, timestamp, message, task=None, slot=None):
		"""
		Output ``message`` for ``task`` (or for the process slot ``slot``,
		if ``task`` is ``None``).

		In continuous mode a new line is printed. In in-place mode the line
		of the slot and the status line below the slots are updated.
		"""

		if task is not None:
			slot = self.slots[task.process_id]
		output = f"{format(timestamp - self.started_at)}"

		if self.continuous:
			output += f" {format_sep('::')} ⏾ {format(len(self.pending_tasks))} {format_sep('→')} 🏃 {format(len(self.running_tasks))} {format_sep('→')} ✓ {format(self.count_done)}"
		if task is not None:
			output += f" {format_sep('::')} {task}"
		output += f" {format_sep('>>')} {message}"

		if self.continuous:
			print(output)
		else:
			c = self.processes - slot + 1
			pre = f"\033[{c}A\033[K"
			post = f"\033[{c}B"
			print(f"{pre}{output}\n{post}", end="", flush=True)
			print(f"\033[1A\033[K{format(datetime.datetime.now() - self.started_at)} {format_sep('>>')} Tasks 😴 {format(len(self.pending_tasks))} wait {format_sep('\N{MIDDLE DOT}')} 🏃 {format(len(self.running_tasks))} run {format_sep('\N{MIDDLE DOT}')} ✅ {format(self.count_done)} done {format_sep('\N{EM DASH}')} Load {format(self.current_load)} now {format_sep('\N{MIDDLE DOT}')} {format(self.mean_load) if self.mean_load is not None else '-'} avg\n\033[1B", end="", flush=True)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		"""
		Run all submitted tasks (and the tasks they submit) until all of them
		are done, then print a summary.

		Events from the tasks (log messages, done messages and submissions of
		new tasks) arrive via a :class:`multiprocessing.Queue` and are
		processed in the main process.

		If an exception was raised inside the ``with`` block, no tasks are
		started and the exception propagates.
		"""

		if exc_type is not None:
			return False

		self.started_at = datetime.datetime.now()

		iterm2.set_session_status(status=self.title, status_color="#ffcc33", indicator="#ffcc33")
		if not self.continuous:
			for i in range(self.processes):
				print()
			print()
			for i in range(self.processes):
				self._print(self.started_at, format_sep("Idle"), slot=i)

		while True:
			self._schedule_pending_tasks()
			(process_id, timestamp, type, data) = self.queue.get()
			self.count_events += 1
			self.total_load += self.current_load
			(process, task) = self.tasks[process_id]
			if type == "done":
				process.join()
				process.close()
				task.finished_at = datetime.datetime.now()
				del self.running_tasks[process_id]
				self.count_done += 1
				if data is None:
					message = format_sep("Done")
				else:
					# The failure message might contain line feeds (e.g. from a
					# multi-line exception message), which would break the output.
					message = " ".join(data.splitlines())
				self._print(timestamp, message, task=task)
				slot = self.slots[process_id]
				if not self.continuous:
					self._print(timestamp, format_sep("Idle"), slot=slot)
				del self.slots[process_id]
				self.free_slots.add(slot)
				if not self.running_tasks:
					break
				self._schedule_pending_tasks()
			elif type == "log":
				self._print(timestamp, data, task=task)
			elif type == "submit":
				(func, name, args, kwargs) = data
				new_task = self.submit(func, name, *args, **kwargs)
				new_task.parent = task
				self._schedule_pending_tasks()
			runtime = datetime.datetime.now() - self.started_at
			runtime = datetime.timedelta(runtime.days, runtime.seconds)
			iterm2.set_session_status(
				detail=
					f"Time  {runtime}\n"
					"Tasks "
						f"😴\N{THIN SPACE}{len(self.pending_tasks):,} wait"
						" \N{MIDDLE DOT} "
						f"🏃\N{THIN SPACE}{len(self.running_tasks):,} run"
						" \N{MIDDLE DOT} "
						f"✅\N{THIN SPACE}{self.count_done:,} done"
					"\n"
					"Load  "
						f"{self.current_load:,} now"
						" \N{MIDDLE DOT} "
						f"{self.mean_load:.01f} avg"
			)
		self.finished_at = datetime.datetime.now()
		total_wait = sum((task.wait_time for (process, task) in self.tasks.values()), start=datetime.timedelta(0))
		total_run = sum((task.run_time for (process, task) in self.tasks.values()), start=datetime.timedelta(0))
		max_wait = max((task for (process, task) in self.tasks.values()), key=operator.attrgetter("wait_time"))
		max_run =  max((task for (process, task) in self.tasks.values()), key=operator.attrgetter("run_time"))
		print(f"Executed {format(len(self.tasks))} tasks in {format(self.run_time)}")
		print(f"Total wait time {format(total_wait)}, total run time {format(total_run)}")
		print(f"Mean wait time {format(total_wait/len(self.tasks))}, mean run time {format(total_run/len(self.tasks))}")
		print(f"Longest wait time {format(max_wait.wait_time)} ({max_wait}), longest run time {format(max_run.run_time)} ({max_run})")
		iterm2.clear_session_status()


class Task:
	"""
	A :class:`!Task` object represents one task submitted to a :class:`Swarm`.

	It is created by :meth:`Swarm.submit` (or :meth:`Task.submit`) and passed
	as the first argument to the task function. The task function uses it to
	communicate with the swarm (which runs in the main process): :meth:`log`
	outputs a progress message and :meth:`submit` submits further tasks. The
	task is finished when the task function returns.

	The following attributes are available:

	``process_id`` : int
		The unique id of the task inside the swarm.

	``name`` : string
		The name of the task (used in the output).

	``parent`` : :class:`Task` or ``None``
		The task that submitted this task (or ``None`` for tasks submitted
		via :meth:`Swarm.submit`).

	``submitted_at``, ``started_at``, ``finished_at`` : :class:`~datetime.datetime` or ``None``
		When the task was submitted, started and finished. Note that these
		are only maintained in the main process, so they are not available
		inside the task function.
	"""

	def __init__(self, process_id, queue, name):
		self.process_id = process_id
		self.queue = queue
		self.name = name
		self.submitted_at = datetime.datetime.now()
		self.started_at = None
		self.finished_at = None
		self.parent = None

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} process_id={self.process_id!r} name={self.name!r} at {id(self):#x}>"

	def __str__(self):
		"""
		The names of all tasks in :meth:`path` joined with ``::``, i.e. the
		"full name" of the task including its ancestors.
		"""

		return f" {format_sep('::')} ".join(t.name for t in self.path())

	@property
	def wait_time(self):
		"""
		How long the task waited for a free slot as a
		:class:`~datetime.timedelta` (or ``None`` if it hasn't started yet).
		"""

		return self.started_at - self.submitted_at if self.started_at is not None else None

	@property
	def run_time(self):
		"""
		How long the task ran as a :class:`~datetime.timedelta` (or ``None``
		if it hasn't finished yet).
		"""

		return self.finished_at - self.started_at if self.finished_at is not None and self.started_at is not None else None

	def path(self):
		"""
		Yield the chain of tasks from the root task down to this task (i.e.
		all ancestors via :attr:`parent` followed by the task itself).
		"""

		if self.parent is not None:
			yield from self.parent.path()
		yield self

	def log(self, message):
		"""
		Output the progress message ``message`` for this task.
		"""

		self.queue.put((self.process_id, datetime.datetime.now(), "log", message))

	def _done(self, message):
		"""
		Signal to the swarm that this task is finished. ``message`` is an
		error message if the task failed, or ``None`` if it succeeded.

		This is called by the swarm itself when the task function returns
		(see :func:`_run_task`), not by the task function.
		"""

		self.queue.put((self.process_id, datetime.datetime.now(), "done", message))

	def submit(self, func, name, *args, **kwargs):
		"""
		Submit a new task to the swarm from inside a running task.

		The arguments have the same meaning as for :meth:`Swarm.submit`. The
		new task will have this task as its :attr:`parent`. ``func``,
		``args`` and ``kwargs`` are sent to the main process via a
		:class:`multiprocessing.Queue`, so they must be picklable.
		"""

		self.queue.put((self.process_id, datetime.datetime.now(), "submit", (func, name, args, kwargs)))
