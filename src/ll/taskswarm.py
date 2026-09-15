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
		task.log(t"Walking {dir}")
		for file in dir.iterdir():
			if file.is_dir():
				task.submit(walk, file.name, file)
			elif file.suffix == ".json":
				task.submit(prettyprint, file.name, file)
		task.log(t"Walked {dir}")


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

Log messages and task names can be strings or t-strings (i.e.
:class:`string.templatelib.Template` objects). A t-string is passed to the
swarm unchanged and formatted there by :meth:`Swarm.format`: Each
interpolated value is formatted (and colored) according to its type (again
by :meth:`Swarm.format`), so the task function doesn't have to do that
itself.
When the type isn't enough to decide how a value should be formatted (e.g.
a database schema name that is a plain :class:`str`), the format spec
selects the formatting: ``t"Exporting {name:schema}"`` calls the method
``format_schema`` of the swarm (which a subclass can add). Since the
t-string is sent to the main process via a :class:`multiprocessing.Queue`,
all interpolated values must be picklable. Values that aren't must be
preformatted by the task (e.g. ``t"Exporting {str(obj):sqlobject}"``).


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
:meth:`Swarm.format`), unless :attr:`Swarm.plain_output` is true, which is
the case on Windows or if ``stdout`` isn't a terminal. The formatting can be
customized by overwriting the methods :meth:`Swarm.format`,
:meth:`Swarm.format_sep` and :meth:`Swarm.format_task` in a subclass, or by
adding ``format_<spec>`` methods that can be selected via the format spec in
t-strings (see above).

When running in iTerm2, the title of the swarm and the current progress are
also shown in the iTerm2 session status (see
:func:`ll.iterm2.set_session_status`), so that the progress is visible in the
tab even when another tab is active.
"""

import sys, builtins, datetime, operator, pathlib, pickle, multiprocessing
from string import templatelib

from ll import iterm2


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

	All output of the swarm goes through the methods :meth:`format`,
	:meth:`format_sep` and :meth:`format_task`, so the formatting can be
	changed by overwriting them in a subclass.

	The following attributes influence the formatting and can be changed
	after the constructor call:

	``plain_output`` : bool
		If true, no ANSI escape sequences are output. Defaults to true on
		Windows or if ``stdout`` isn't a terminal.

	``currentdir`` : :class:`pathlib.Path`
		:meth:`format` prints paths relative to this directory (if possible).
		Defaults to the current directory when the swarm was created.
	"""

	def __init__(self, title, processes, continuous):
		self.title = title
		self.plain_output = (sys.platform == "win32" or not sys.stdout.isatty())
		self.currentdir = pathlib.Path.cwd()
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

	def format(self, obj, spec=""):
		"""
		Format ``obj`` (a log message, a task name or a value interpolated
		in one of them) for the output of the swarm (with ANSI colors).

		If ``obj`` is a t-string (i.e. a :class:`string.templatelib.Template`
		object) each interpolated value is converted according to its
		conversion (``!r``, ``!s`` or ``!a``) and then formatted with
		:meth:`format` (passing the format spec); ``spec`` itself is ignored
		in this case.

		Otherwise ``spec`` is the format spec from a t-string and is used as
		follows:

		*	If ``spec`` isn't empty and the swarm has a method named
			``format_<spec>``, this method is called with ``obj``. This is how
			a subclass can support formatting values whose type isn't enough
			to decide how they should be formatted (e.g. ``{name:schema}``
			calls ``self.format_schema(name)``).

		*	Otherwise the formatting depends on the type of ``obj``:
			:class:`pathlib.Path` objects are output relative to
			:attr:`currentdir` (if possible) in yellow, numbers and
			:class:`~datetime.datetime` objects in bold magenta (with ``spec``
			as the format spec, or ``,`` for :class:`int` and ``,.01f`` for
			:class:`float` if ``spec`` is empty), :class:`~datetime.timedelta`
			objects as ``HH:MM:SS`` with the leading zeros in normal magenta
			and the rest in bold magenta (``spec`` is ignored). Everything
			else is formatted with the builtin :func:`format` and ``spec`` (so
			an unknown ``spec`` raises a :exc:`ValueError`).

		If :attr:`plain_output` is true, no ANSI escape sequences are output.

		Overwrite this method in a subclass to change the formatting or to
		support additional types.
		"""

		if isinstance(obj, templatelib.Template):
			parts = []
			for part in obj:
				if isinstance(part, templatelib.Interpolation):
					value = part.value
					if part.conversion == "r":
						value = repr(value)
					elif part.conversion == "s":
						value = str(value)
					elif part.conversion == "a":
						value = ascii(value)
					parts.append(self.format(value, part.format_spec))
				else:
					parts.append(part)
			return "".join(parts)
		if spec:
			method = getattr(self, f"format_{spec}", None)
			if method is not None:
				return method(obj)
		if isinstance(obj, pathlib.Path):
			try:
				obj = obj.relative_to(self.currentdir)
			except ValueError:
				pass
			return str(obj) if self.plain_output else f"\033[33m{obj}\033[0m"
		elif isinstance(obj, int):
			return builtins.format(obj, spec or ",") if self.plain_output else f"\033[1;35m{obj:{spec or ','}}\033[0m"
		elif isinstance(obj, float):
			return builtins.format(obj, spec or ",.01f") if self.plain_output else f"\033[1;35m{obj:{spec or ',.01f'}}\033[0m"
		elif isinstance(obj, datetime.datetime):
			return builtins.format(obj, spec) if self.plain_output else f"\033[1;35m{obj:{spec}}\033[0m"
		elif isinstance(obj, datetime.timedelta):
			if self.plain_output:
				return str(obj)
			else:
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
			return builtins.format(obj, spec)

	def format_sep(self, text):
		"""
		Format the separator ``text`` for the output of the swarm (i.e. in
		dark grey).

		If :attr:`plain_output` is true, no ANSI escape sequences are output.
		"""

		if self.plain_output:
			return text
		else:
			return f"\033[30;1m{text}\033[0m"

	def format_task(self, task):
		"""
		Format the "full name" of ``task`` (i.e. the names of all tasks in
		:meth:`Task.path` joined with separators) for the output of the swarm.
		"""

		return f" {self.format_sep('::')} ".join(self.format(t.name) for t in task.path())

	def submit(self, func, name, *args, **kwargs):
		"""
		Submit a new task to the swarm and return the :class:`Task` object.

		``func`` is the callable that gets executed in a separate process. It
		will be called as ``func(task, *args, **kwargs)`` (where ``task`` is
		the :class:`Task` object). The task is finished when ``func`` returns
		or raises an exception. ``name`` is the name of the task used in the
		output. It can be a string or a t-string (see :meth:`format`).

		Tasks submitted before the ``with`` block is exited are started (in
		submission order, as far as free slots are available) when the block
		is exited. This method may only be called from the main process; a
		running task submits further tasks via :meth:`Task.submit`.
		"""

		task = Task(self.process_id, self.queue, name)
		process = multiprocessing.Process(target=_run_task, name=task.plain_name, args=(func, task) + args, kwargs=kwargs)
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
			self._print(datetime.datetime.now(), self.format_sep("Started"), task=task)
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
		output = f"{self.format(timestamp - self.started_at)}"

		if self.continuous:
			output += f" {self.format_sep('::')} ⏾ {self.format(len(self.pending_tasks))} {self.format_sep('→')} 🏃 {self.format(len(self.running_tasks))} {self.format_sep('→')} ✓ {self.format(self.count_done)}"
		if task is not None:
			output += f" {self.format_sep('::')} {self.format_task(task)}"
		output += f" {self.format_sep('>>')} {message}"

		if self.continuous:
			print(output)
		else:
			c = self.processes - slot + 1
			pre = f"\033[{c}A\033[K"
			post = f"\033[{c}B"
			print(f"{pre}{output}\n{post}", end="", flush=True)
			print(f"\033[1A\033[K{self.format(datetime.datetime.now() - self.started_at)} {self.format_sep('>>')} Tasks 😴 {self.format(len(self.pending_tasks))} wait {self.format_sep('\N{MIDDLE DOT}')} 🏃 {self.format(len(self.running_tasks))} run {self.format_sep('\N{MIDDLE DOT}')} ✅ {self.format(self.count_done)} done {self.format_sep('\N{EM DASH}')} Load {self.format(self.current_load)} now {self.format_sep('\N{MIDDLE DOT}')} {self.format(self.mean_load) if self.mean_load is not None else '-'} avg\n\033[1B", end="", flush=True)

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
				self._print(self.started_at, self.format_sep("Idle"), slot=i)

		while True:
			self._schedule_pending_tasks()
			(process_id, timestamp, type, data) = pickle.loads(self.queue.get())
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
					message = self.format_sep("Done")
				else:
					# The failure message might contain line feeds (e.g. from a
					# multi-line exception message), which would break the output.
					message = " ".join(self.format(data).splitlines())
				self._print(timestamp, message, task=task)
				slot = self.slots[process_id]
				if not self.continuous:
					self._print(timestamp, self.format_sep("Idle"), slot=slot)
				del self.slots[process_id]
				self.free_slots.add(slot)
				if not self.running_tasks:
					break
				self._schedule_pending_tasks()
			elif type == "log":
				self._print(timestamp, self.format(data), task=task)
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
		print(self.format(t"Executed {len(self.tasks)} tasks in {self.run_time}"))
		print(self.format(t"Total wait time {total_wait}, total run time {total_run}"))
		print(self.format(t"Mean wait time {total_wait/len(self.tasks)}, mean run time {total_run/len(self.tasks)}"))
		print(self.format(t"Longest wait time {max_wait.wait_time} ({max_wait:task}), longest run time {max_run.run_time} ({max_run:task})"))
		iterm2.clear_session_status()


class Task:
	"""
	A :class:`!Task` object represents one task submitted to a :class:`Swarm`.

	It is created by :meth:`Swarm.submit` (or :meth:`Task.submit`) and passed
	as the first argument to the task function. The task function uses it to
	communicate with the swarm (which runs in the main process): :meth:`log`
	outputs a progress message and :meth:`submit` submits further tasks. The
	task is finished when the task function returns.

	Everything sent to the swarm (log messages, names and arguments of new
	tasks) is pickled by the task itself before it's put into the
	:class:`multiprocessing.Queue`, so that unpicklable values raise an
	exception in the task function (instead of silently losing the message
	in the feeder thread of the queue).

	The following attributes are available:

	``process_id`` : int
		The unique id of the task inside the swarm.

	``name`` : string or t-string
		The name of the task (used in the output, see
		:meth:`Swarm.format`).

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
		"full name" of the task including its ancestors (without any
		formatting, see :meth:`Swarm.format_task` for that).
		"""

		return " :: ".join(t.plain_name for t in self.path())

	@property
	def plain_name(self):
		"""
		The :attr:`name` of the task as a plain string.

		If the name is a t-string, the interpolated values are simply
		converted with :class:`str` (format specs are ignored).
		"""

		if isinstance(self.name, templatelib.Template):
			return "".join(str(part.value) if isinstance(part, templatelib.Interpolation) else part for part in self.name)
		else:
			return str(self.name)

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

	def _put(self, type, data):
		"""
		Send the event ``type`` with the payload ``data`` to the swarm.

		The event is pickled here (i.e. in the task process) so that
		unpicklable values in ``data`` raise the exception in the task
		function.
		"""

		self.queue.put(pickle.dumps((self.process_id, datetime.datetime.now(), type, data)))

	def log(self, message):
		"""
		Output the progress message ``message`` for this task.

		``message`` can be a string or a t-string (see
		:meth:`Swarm.format`). All interpolated values of a t-string
		must be picklable; preformat those that aren't (e.g.
		``t"{str(obj):sqlobject}"``).
		"""

		self._put("log", message)

	def _done(self, message):
		"""
		Signal to the swarm that this task is finished. ``message`` is an
		error message if the task failed, or ``None`` if it succeeded.

		This is called by the swarm itself when the task function returns
		(see :func:`_run_task`), not by the task function.
		"""

		self._put("done", message)

	def submit(self, func, name, *args, **kwargs):
		"""
		Submit a new task to the swarm from inside a running task.

		The arguments have the same meaning as for :meth:`Swarm.submit`. The
		new task will have this task as its :attr:`parent`. ``func``,
		``name``, ``args`` and ``kwargs`` are sent to the main process via a
		:class:`multiprocessing.Queue`, so they must be picklable.
		"""

		self._put("submit", (func, name, args, kwargs))
