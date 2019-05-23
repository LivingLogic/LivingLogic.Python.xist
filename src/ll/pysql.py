# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2012-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2012-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See LICENSE for the license

"""
Overview
========
The module/script :mod:`pysql` can be used to import data into an Oracle
database. It reads ``pysql`` files which are a variant of normal Oracle SQL
files.

A PySQL file can contain two different types of commands.


SQL commands
------------

A PySQL file may contain normal SQL commands. For the :mod:`pysql` script
to be able to execute these commands they must be terminated with a comment
line ``-- @@@``. :mod:`pysql` will strip off a trailing ``;`` or ``/`` from
the command and execute it. Any exception that is raised as a result of
executing the command will stop the script and be reported. This is in
contrast to how ``sqlplus`` executes SQL commands. ``sqlplus`` would continue
after an error and exit with status code 0 even if there were errors.
It is also possible to explicitely ignore any exception raised by the
command by specifying a different exception handling mode.

A PySQL file that only contains SQL commands is still a valid SQL file from
the perspective of Oracle, so it still can be executed via ``sqlplus``.


PySQL commands
--------------

A PySQL file may also contain PySQL commands. A PySQL command looks like a
Python function call. This function call must either be contained in a single
line or it must start with a line that only contains ``name(`` and end at a
line that only contains ``)``. (``name`` must be the name of a PySQL command).

For further information about the different commands and which arguments they
support, see the class :class:`Command` and its subclasses.


Example
=======

The following is a complete PySQL file that will create a sequence, table and
procedure and will call the procedure to insert data into the table::

	create sequence person_seq
		increment by 10
		start with 10
		maxvalue 1.0e28
		minvalue 10
		nocycle
		cache 20
		noorder
	;

	-- @@@

	create sequence contact_seq
		increment by 10
		start with 10
		maxvalue 1.0e28
		minvalue 10
		nocycle
		cache 20
		noorder
	;

	-- @@@ person: table

	create table person
	(
		per_id integer not null,
		per_firstname varchar2(200),
		per_lastname varchar2(200)
	);

	-- @@@ person: primary key

	alter table person add constraint person_pk primary key(per_id);

	-- @@@ contact: table

	create table contact
	(
		con_id integer not null,
		per_id integer not null,
		con_type varchar2(200),
		con_value varchar2(200)
	);

	-- @@@ contact: primary key

	alter table contact add constraint contact_pk primary key(con_id);

	-- @@@ person: insert procedure

	create or replace procedure person_insert
	(
		c_user in varchar2,
		p_per_id in out integer,
		p_per_firstname in varchar2 := null,
		p_per_lastname in varchar2 := null
	)
	as
	begin
		if p_per_id is null then
			select person_seq.nextval into p_per_id from dual;
		end if;

		insert into person
		(
			per_id,
			per_firstname,
			per_lastname
		)
		values
		(
			p_per_id,
			p_per_firstname,
			p_per_lastname
		);
	end;
	/

	-- @@@ contact: insert procedure

	create or replace procedure contact_insert
	(
		c_user in varchar2,
		p_con_id in out integer,
		p_per_id in integer := null,
		p_con_type in varchar2 := null,
		p_con_value in varchar2 := null
	)
	as
	begin
		if p_con_id is null then
			select contact_seq.nextval into p_con_id from dual;
		end if;

		insert into contact
		(
			con_id,
			per_id,
			con_type,
			con_value
		)
		values
		(
			p_con_id,
			p_per_id,
			p_con_type,
			p_con_value
		);
	end;
	/

	-- @@@

	# import data

	procedure(
		'person_insert',
		args=dict(
			c_user='import',
			p_per_id=var('per_id_max'),
			p_per_firstname='Max',
			p_per_lastname='Mustermann',
		)
	)

	procedure(
		'contact_insert',
		args=dict(
			c_user='import',
			p_per_id=var('per_id_max'),
			p_con_id=var('con_id_max'),
			p_con_type='email',
			p_con_value='max@example.org',
		)
	)

	file(
		'portrait_{per_id_max}.png',
		b'\\x89PNG\\r\\n\\x1a\\n...',
	)

	resetsequence(
		'person_seq',
		table='person',
		field='per_id',
	}

	checkerrors()

This file can then be imported into an Oracle database with the following
command::

	python pysql.py user/pwd@database data.pysql

This will create two sequences, two tables and two procedures. Then it will
import two records, one by calling ``person_insert`` and one by calling
``contact_insert``. The PL/SQL equivalent of the above is::

	declare
		v_per_id_max integer;
		v_con_id_max integer;
	begin
		person_insert(
			per_id=v_per_id_max,
			per_firstname='Max',
			per_lastname='Mustermann'
		);
		contact_insert(
			con_id=v_con_id_max,
			per_id=v_per_id_max,
			con_type='email',
			con_value='max@example.org'
		)
	end;

Furthermore it will create one file (named something like ``portrait_42.png``)
and reset the sequence ``person_seq`` to the maximum value of the field
``per_id`` in the table ``person``. Finally it will make sure that no errors
exist in the schema.


Multiple database connections
=============================

PySQL can handle multiple database connections. New database connections can be
opened with the ``pushconnnection`` command. This command opens a new database
connection and stores it under a name. Subsequent commands can refer to that
name to specify the database connection to use. The ``popconnection`` command
disconnects from the database and reverts to the previous connection for that
name (which might not exist). An example looks like this::

	pushconnection(connectstring="user/pwd@db", connectname=db")

	procedure("test", connectname="db")

	popconnection(connectname="db")

The connection with the name ``None`` is the "default connection". This
connection will be used for all normal SQL commands and all PySQL commands that
don't have a ``connectname`` parameter (or where the ``connectname`` parameter
is ``None``).


Variables
=========

Variable objects can be used to receive out parameters of procedure calls or
SQL statements. A variable object can be specified like this ``var("foo")``.
``"foo"`` is the "name" of the variable. When a variable object is passed
to a procedure the first time (i.e. the variable object is uninitialized),
a :mod:`cx_Oracle` ``var`` object will be passed and the resulting value after
the call will be stored under the name of the variable. When the variable is
used in a later command the stored value will be used instead. (Note that it's
not possible to use the same variable twice in the same procedure call,
if it hasn't been used before, however in later commands this is no problem).

The type of the variable defaults to :class:`int`, but a different type can be
passed when creating the object like this: ``var("foo", str)``.

It is also possible to create variable objects via command line parameters.

As a PySQL command is a Python literal, it is possible to use Python expressions
inside a PySQL command. A variable object that has a value will be replaced by
that value in such an expression, so stuff like ``2*var("foo")`` can be used.

An uninitialized variable object is considered "false", This makes it possible
to default to another value if a variable is uninitialized::

	var('foo', int) or 42


External files
==============

Inside a PySQL command it is possible to load values from external files.
The ``loadbytes`` command loads a ``bytes`` object from an external file
like this::

	loadbytes("path/to/file.png")

A string can be loaded with the ``loadstr`` function like this::

	loadstr("path/to/file.txt", "utf-8", "replace")

The second and third argument are the encoding and error handling name
respectively.

The filename is treated as being relative to the file containing the
``loadbytes`` or ``loadstr`` call.


Command line usage
==================

``pysql.py`` has no external dependencies except for :mod:`cx_Oracle` and can
be used as a script for importing a PySQL file into the database. As a script
it supports the following command line options:

	``connectstring``
		An Oracle connectstring.

	``file``
		The name of the PySQL file that will be read and imported. If ``file``
		isn't specified the commands are read from ``stdin``.

	``-v``, ``--verbose``
		Gives different levels of output while data is being imported to the
		database. The default is no output (unless an exception occurs). Possible
		modes are: ``dot`` (one dot for each command), ``type`` (each command type),
		``line`` (each top level command as a line), ``file`` (the file location
		of each command) or ``full`` (detailed output for each command)

	``-z``, ``--summary``
		Give a summary of the number of commands executed and procedures called.

	``-c``, ``--commit``
		Specifies when to commit database transactions. ``record`` commits after
		every command. ``once`` (the default) commits at the end of the script
		(or when a connection is popped) and ``never`` rolls back the transaction
		after all commands.

	``-s``, ``--scpdirectory``
		The base directory for :class:`scp` file copy commands. As files are
		copied via ``scp`` this can be a remote filename (like
		``root@www.example.org:~/uploads/``) and must include a trailing ``/``.

	``-f``, ``--filedirectory``
		The base directory for :class:`file` file save commands. It must include
		a trailing ``/``.

	``-t``, ``--terminator``
		The terminator after an SQL command (should be a valid SQL comment;
		default ``-- @@@``).

	``-D``, ``--define``
		Can be used multiple times to define variables. Supported formats are:

		``name``
			Defines a string variable named ``name`` and sets the value to the
			empty string.

		``name=value``
			Defines a string variable named ``name`` and sets the value to
			``value``.

		``name:type``
			Defines a variable named ``name`` of type ``type`` and sets the value
			to ``False``, ``0``, ``0.0`` or the empty string depending on the type.
			Supported types are ``str``, ``bool``, ``int`` and ``float``.

		``name:type=value``
			Defines a variable named ``name`` of type ``type`` and sets the value
			to ``value``. For type ``bool`` supported values are ``0``, ``no``,
			``false``, ``False``, ``1``, ``yes``, ``true`` and ``True``.
"""

# We're importing :mod:`datetime` to make it available to ``eval()``
import sys, os, os.path, argparse, collections, datetime, pathlib, tempfile, subprocess, contextlib

try:
	import pwd
except ImportError:
	pwd = None

try:
	import grp
except ImportError:
	grp = None

import cx_Oracle

__docformat__ = "reStructuredText"


def format_class(obj):
	if obj.__module__ not in ("builtins", "exceptions"):
		return f"{obj.__module__}.{obj.__qualname__}"
	else:
		return obj.__qualname__


reprthreshold = 100


def shortrepr(value):
	if isinstance(value, bytes) and len(value) > reprthreshold:
		return f"<{bytes.__repr__(value[:reprthreshold])} ... ({len(value):,} bytes)>"
	elif isinstance(value, str) and  len(value) > reprthreshold:
		return f"<{str.__repr__(value[:reprthreshold])} ... ({len(value):,} characters)>"
	else:
		return repr(value)


class Connection:
	def __init__(self, connectstring, mode, commit):
		self.mode = mode
		mode = cx_Oracle.SYSDBA if mode == "sysdba" else 0
		self.connection = cx_Oracle.connect(connectstring, mode=mode)
		self.connectstring = f"{self.connection.username}@{self.connection.tnsentry}"
		self.cursor = self.connection.cursor()
		self.commit = commit

	def close(self):
		if self.connection is not None:
			if self.commit == "once":
				self.connection.commit()
			elif self.commit == "never":
				self.connection.rollback()
			self.cursor.close()
			self.cursor = None
			self.connection.close()
			self.connection = None

	def __str__(self):
		state = "open" if self.connection is not None else "closed"
		return f"{state} connection {self.connectstring!r}"

	def __repr__(self):
		state = "open" if self.connection is not None else "closed"
		return f"<{state} connection to {self.connectstring!r}>"


class CommandStackEntry:
	def __init__(self, command):
		self.starttime = datetime.datetime.now()
		self.command = command
		self.output = False

	def sep(self, context):
		if self.output:
			if context.verbose == "full":
				print(", ", end="", flush=True)
			elif context.verbose == "type":
				print(" ", end="", flush=True)
		else:
			while self is not None:
				self.output = True
				self = self.preventry


class Context:
	"""
	A :class:`Context` objects contains the configuration and run time information
	required for importing a PySQL file.
	"""
	def __init__(self, connectstring=None, scpdirectory="", filedirectory="", commit="once", terminator="-- @@@", tabsize=None, context=None, raiseexceptions=True, verbose=0, summary=False, vars=None):
		self.keys = {v.key: v for v in vars} if vars else {}
		self.connections = {}
		self.commit = commit
		self.scpdirectory = scpdirectory
		self.filedirectory = filedirectory
		self.terminator = terminator
		self.tabsize = tabsize
		self.context = context
		self.raiseexceptions = [raiseexceptions]
		self.verbose = verbose
		self.summary = summary
		self.commandcounts = collections.Counter()
		self.errorcount = 0
		self.totalcount = 0
		self._location = None
		self._runstarttime = None
		self.basedir = pathlib.Path()
		self._lastlocation = None
		self._lastcommand = None
		self._output = False
		for fd in range(3):
			try:
				self._width = os.get_terminal_size(fd)[0]
			except OSError:
				pass
			else:
				break
		else:
			self._width = 80
		if connectstring is not None:
			self.pushconnection(None, self.connect(connectstring, commit))

	def connect(self, connectstring, mode=None, commit="once"):
		return Connection(connectstring, mode, commit)

	def connection(self, connectname=None):
		if connectname not in self.connections:
			raise ValueError(f"no connection named {connectname!r}")
		return self.connections[connectname][-1]

	def pushconnection(self, connectname, connection):
		if connectname not in self.connections:
			self.connections[connectname] = []
		self.connections[connectname].append(connection)

	def popconnection(self, connectname):
		if connectname not in self.connections:
			raise ValueError(f"no connection named {connectname!r}")
		if not self.connections[connectname]:
			raise ValueError(f"connection stack for name {connectname!r} empty")
		return self.connections[connectname].pop()

	def logprefix(self, starttime, commandnumber, object):
		if object.location is not None:
			return f"[t+{starttime-self._runstarttime}] :: #{commandnumber:,} :: [{object.location}]"
		else:
			return f"[t+{starttime-self._runstarttime}] :: #{commandnumber:,}"

	def execute(self, label, default, object):
		if self._runstarttime is None:
			self._runstarttime = datetime.datetime.now()
			self._output = False

		if not isinstance(object, Command):
			return object

		if isinstance(object, comment):
			self.count("comment")
			return None

		commandnumber = self.totalcount + 1
		if object.raiseexceptions is not None:
			self.raiseexceptions.append(object.raiseexceptions)

		starttime = datetime.datetime.now()

		if self.verbose == "dot":
			print(".", end="", flush=True)
		elif self.verbose == "type":
			print(f"{object.__class__.__name__}(", end="", flush=True)
		elif self.verbose == "file":
			endfile = False
			if object.location is None:
				pass # A command inside another command
			elif self._lastlocation is None or object.location.filename != self._lastlocation.filename:
				print(f" [{object.location.filename} :: {object.location.lines()}", end="", flush=True)
				endfile = True
			elif object.location.startline != self._lastlocation.startline or object.location.endline != self._lastlocation.endline:
				print(f" [{object.location.lines()}", end="", flush=True)
				endfile = True
			else:
				pass # still the same location
		elif self.verbose == "line":
			print(f"[t+{starttime-self._runstarttime}] :: #{self.totalcount+1:,} :: [{object.location}] >> {object.__class__.__name__}(", end="", flush=True)
		elif self.verbose == "full":
			if object is not self._lastcommand:
				print("\u2501"*self._width, flush=True)
				self._lastcommand = object
			print(f"{self.logprefix(starttime, commandnumber, object)} >> {object.__class__.__name__}", flush=True)
			lines = object.source(self.tabsize).splitlines(False)
			if object.location and object.location.startline and object.location.endline:
				startline = object.location.startline
				endline = object.location.endline
				linenumberlen = len(f"{object.location.endline:,}")
				ruletop    = "\u2500" * (linenumberlen + 1) + "\u252c" + "\u2500" * (self._width - 2 - linenumberlen)
				rulebottom = "\u2500" * (linenumberlen + 1) + "\u2534" + "\u2500" * (self._width - 2 - linenumberlen)
				print(ruletop, flush=True)

				ellipsis = "\u22ee"
				for (linenumber, line) in enumerate(lines, startline):
					if self.context is not None and startline + self.context <= linenumber <= endline - self.context:
						if startline + self.context == linenumber:
							print(f"{ellipsis:>{linenumberlen}} \u2502 {ellipsis}", flush=True)
					else:
						print(f"{linenumber:{linenumberlen},} \u2502 {line}", flush=True)
				print(rulebottom, flush=True)
			else:
				endline = len(lines) - 1
				rule = "\u2500" * self._width
				print(rule, flush=True)
				for (linenumber, line) in enumerate(lines):
					if self.context is not None and self.context <= linenumber <= endline - self.context:
						if self.context == linenumber:
							print(ellipsis, flush=True)
					else:
						print(line, flush=True)
				print(rule, flush=True)

		if object.location is not None:
			self._lastlocation = object.location

		result = None
		try:
			result = object.execute(self)
		except Exception as exc:
			if self.raiseexceptions[-1]:
				if self.verbose:
					print(flush=True)
				raise CommandError(object) from exc
			else:
				self.errorcount += 1
				if self.verbose == "dot":
					print("!", end="", flush=True)
				elif self.verbose == "type":
					print(f")->failed", end="", flush=True)
				elif self.verbose == "file":
					if endfile:
						print(f"]->failed", end="", flush=True)
				elif self.verbose == "full":
					if object is not self._lastcommand:
						print("\u2501"*self._width, flush=True)
						self._lastcommand = object
					exctext = str(exc).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
					print(f"{self.logprefix(starttime, commandnumber, object)} >> ignored {format_class(exc.__class__)}: {exctext}", flush=True)
		else:
			now = datetime.datetime.now()
			if self.verbose == "full":
				if object is not self._lastcommand:
					print("\u2501"*self._width, flush=True)
					self._lastcommand = object
				if result is None:
					print(f"{self.logprefix(starttime, commandnumber, object)} >> {object.__class__.__name__} finished in {now-starttime}", flush=True)
				else:
					print(f"{self.logprefix(starttime, commandnumber, object)} >> {object.__class__.__name__} finished with {shortrepr(result)} (in {now-starttime})", flush=True)
			elif self.verbose == "file":
				if endfile:
					print(f"]", end="", flush=True)
			elif self.verbose == "type":
				print(f")", end="", flush=True)
		finally:
			if object.raiseexceptions is not None:
				self.raiseexceptions.pop()
		return result

	@contextlib.contextmanager
	def changed_basedir(self, dirpath):
		oldbasedir = self.basedir
		self.basedir = dirpath
		try:
			yield
		finally:
			self.basedir = oldbasedir

	def globals(self):
		vars = {command.__name__: command for command in Command.commands.values()}
		vars["sqlexpr"] = sqlexpr
		vars["datetime"] = datetime
		return vars

	def _load(self, stream):
		"""
		Load a PySQL file from :obj:`stream`. :obj:`stream` must be an iterable
		over lines that contain the PySQL commands.

		This function is a generator. Its output are the PySQL command objects
		(i.e. instances of :class:`Command`).
		"""
		lines = []

		vars = self.globals()

		constructor_prefixes = tuple(f"{cname}(" for cname in Command.commands)

		# ``state`` is the state of the "parser", values have the following meaning
		# ``None``: outside of any block
		# ``literalsql``: inside of literal SQL block
		# ``literalpy``: inside of literal Python block
		# ``comment``: inside of comment (lines starting with "#")
		# ``blockcomment``: inside of block comment (lines delimited by "######")
		# ``dict``: inside of Python dict literal
		# others: inside a PySQL command of that name
		state = None

		def makeblock():
			# Drop empty lines at the start
			while lines and not lines[0][1].strip():
				del lines[0]
			# Drop empty lines at the end
			while lines and not lines[-1][1].strip():
				del lines[-1]
			try:
				if lines:
					self._location = Location(stream.name, lines[0][0], lines[-1][0])
					text = "\n".join(line[1] for line in lines).strip()
					lines.clear()
					if text:
						if state == "literalsql":
							command = literalsql(text)
						elif state == "literalpy":
							command = literalpy(text)
						elif state == "comment":
							command = comment(text)
						elif state == "blockcomment":
							command = comment(text)
						elif state == "dict":
							args = eval(text, vars, vars)
							command = Command.fromdict(args)
						else:
							command = eval(text, vars, vars)
						command.location = self._location
						yield command
			except Exception as exc:
				raise LocationError(self._location) from exc


		for (i, line) in enumerate(stream, 1):
			line = line.rstrip()
			if state is None:
				if line.startswith("{"):
					lines.append((i, line))
					state = "dict"
					if line.endswith("}"):
						yield from makeblock()
						state = None
				elif line == "######":
					state = "blockcomment"
				elif line == "###>>>":
					lines.append((i, line))
					state = "literalpy"
				elif line.startswith("#"):
					state = "comment"
					lines.append((i, line[1:].strip()))
					yield from makeblock()
					state = None
				elif line == self.terminator:
					pass # Still outside the block
				elif line.startswith(constructor_prefixes): # PySQL command constructor?
					lines.append((i, line))
					state = line[:line.find("(")]
					if line.endswith(")"):
						yield from makeblock()
						state = None
				elif line:
					lines.append((i, line))
					state = "literalsql"
			elif state == "dict":
				lines.append((i, line))
				if line == "}": # A single unindented ``}``
					yield from makeblock()
					state = None
			elif state == "literalsql":
				if line.startswith(self.terminator):
					yield from makeblock()
					state = None
				else:
					lines.append((i, line))
			elif state == "literalpy":
				lines.append((i, line))
				if line == "###<<<":
					yield from makeblock()
					state = None
			elif state == "comment":
				raise ValueError("This can't happen")
			elif state == "blockcomment":
				if line == "######":
					yield from makeblock()
					state = None
				else:
					lines.append((i, line))
			else:
				lines.append((i, line))
				if line == ")": # A single unindented ``)``
					yield from makeblock()
					state = None
		yield from makeblock()

	def executeall(self, stream):
		"""
		Execute all command in :obj:`stream`. :obj:`stream` must be an iterable
		over lines that contain the PySQL commands.
		"""
		try:
			if self.verbose == "type":
				print("commands:", end="", flush=True)
			elif self.verbose == "file":
				print("files:", end="", flush=True)
			for command in self._load(stream):
				self.execute(None, None, command)
			for connections in self.connections.values():
				for connection in connections:
					if connection.commit == "once":
						connection.connection.commit()
					elif connection.commit == "never":
						connection.connection.rollback()
		finally:
			if self.verbose in {"dot", "type"}:
				print(flush=True)
		self._printsummary()

	def _printsummary(self):
		if self.summary:
			if self._runstarttime is None:
				self._runstarttime = datetime.datetime.now()
			now = datetime.datetime.now()
			if self.verbose == "full":
				print("\u2501"*self._width, flush=True)
				print(f"[t+{now-self._runstarttime}] >> Command summary", flush=True)
			else:
				print("Command summary", flush=True)
			anyoutput = False
			totallen = len(f"{self.totalcount:,}")

			def sortkey(keyvalue):
				(key, value) = keyvalue
				if len(key) > 1: # db command
					return (0, key[0], key[1] != "procedure", *key)
				else:
					return (1, *key)
			lastconnection = None
			for (key, count) in sorted(self.commandcounts.items(), key=sortkey):
				connection = key[0] if len(key) > 1 else None
				if not anyoutput or connection != lastconnection:
					print(flush=True)
					if connection:
						print(f"Connection {connection}:", flush=True)
					else:
						print("Other commands:", flush=True)
				lastconnection = connection
				anyoutput = True
				keys = " ".join(key[1:]) if len(key) > 1 else key[0]
				print(f"    {count:>{totallen},} {keys}", flush=True)
			if self.errorcount:
				print(flush=True)
				print(f"Exceptions: {self.errorcount:,} exception{'s' if self.errorcount != 1 else ''} ignored", flush=True)
			if anyoutput:
				print(flush=True)
				print(f"Total: {self.totalcount:,} command{'s' if self.totalcount != 1 else ''} executed", flush=True)
			if not anyoutput:
				print("    no commands executed", flush=True)

	def count(self, *args):
		self.commandcounts[args] += 1
		self.totalcount += 1


###
### Command classes
###

class Command:
	"""
	The base class of all commands. A :class:`Command` object is created from
	function call in a PySQL file. The only parameter in the call that is
	supported by all commands is the following:

	``raiseexceptions`` : bool (optional)
		Specifies whether exceptions that happen during the execution of the
		command should be reported and terminate the script (``True``), or
		should be ignored (``False``). ``None`` uses the global configuration.
	"""

	def __init__(self, *, raiseexceptions=None):
		self.location = None
		self.raiseexceptions = raiseexceptions

	commands = {}

	@classmethod
	def fromdict(cls, d):
		type = d.pop("type", "procedure")
		if type in cls.commands:
			return cls.commands[type](**d)
		raise ValueError(f"command type {type!r} unknown")

	def __str__(self):
		if self.location is None:
			return f"{self.__class__.__name__} command"
		else:
			return f"{self.__class__.__name__} command in {self.location}"

	def _value(self, output, key, value):
		if key is not None:
			output.append(f"{key}=")
		if isinstance(value, str):
			value = value.replace("\r\n", "\n").replace("\r", "\n")
		if isinstance(value, str) and "\n" in value:
			if key is not None:
				output.append(1)
				output.append(None)
			lines = value.splitlines(True)
			for (i, line) in enumerate(lines):
				last = i == len(lines)-1
				if last:
					output.append(f"{line!r},")
				else:
					output.append(repr(line))
				output.append(None)
			output.append(-1)
			return
		elif isinstance(value, dict):
			output.append("dict(")
			output.append(1)
			output.append(None)
			for (dictkey, dictvalue) in value.items():
				self._value(output, dictkey, dictvalue)
			output.append(-1)
			output.append("),")
			output.append(None)
			return
		output.append(f"{value!r},")
		output.append("")
		output.append(None)

	def _source_format(self, *args, **kwargs):
		yield f"{self.__class__.__name__}("
		yield 1
		yield None
		parts = []
		for argvalue in args:
			# We assume that all positional arguments are mandatory
			parts.append((None, argvalue))
		for (argname, argvalue) in kwargs.items():
			if argvalue is not None:
				parts.append((argname, argvalue))
		lastindex = len(parts)-1
		for (i, (argname, argvalue)) in enumerate(parts):
			if argname is not None:
				yield f"{argname}="
				if isinstance(argvalue, str) and "\n" in argvalue:
					yield 1
					yield None
			yield from source_format(argvalue)
			if i == lastindex:
				yield (",", "")
			else:
				yield (",", ", ")
			if argname is not None and isinstance(argvalue, str) and "\n" in argvalue:
				yield 1
			yield None
		yield -1
		yield ")"

	def source(self, tabsize=None):
		return source(self, tabsize)


def register(cls):
	Command.commands[cls.__name__] = cls
	return cls


@register
class include(Command):
	"""
	The :class:`!include` command includes another PySQL file. The filename is
	passed in the first parameter ``name``. This name is interpreted as being
	relative to the directory with the file containing the :class:`!include`
	command.

	The parameter ``cond`` specifies whether this :class:`!include` command
	should be executed or not. If ``cond`` is ``None`` or true, the
	:class:`!include` command will be executed, else it won't.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, name, *, cond=None, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.name = name
		self.cond = cond

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		name = context.execute("name", None, self.name)
		cond = context.execute("cond", None, self.cond)

		filename = context.basedir/name

		if cond is None or cond:
			with context.changed_basedir(filename.parent):
				with filename.open("r", encoding="utf-8") as f:
					for command in context._load(f):
						context.execute(None, None, command)
		context.count(self.__class__.__name__)

	def source_format(self):
		yield from self._source_format(self.name, raiseexceptions=self.raiseexceptions)


@register
class pushconnection(Command):
	"""
	The :class:`!pushconnection` command connects to the database given in the
	connectstring in the parameter ``connectstring`` and pushes the connection
	under the name from the parameter ``connectname``. (If ``connectname`` is
	not given or is ``None``, the connection will be pushed as the default
	connection). ``commit`` can be given to specify the commit mode for this
	connection (``"record"``, ``"once"`` or ``"never"``).

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, connectstring, *, mode=None, raiseexceptions=None, connectname=None, commit=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.connectstring = connectstring
		self.mode = mode
		self.connectname = connectname
		self.commit = commit

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} connectname={self.connectname!r} connectstring={self.connectstring!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connectname = context.execute("connectname", None, self.connectname)
		connectstring = context.execute("connectstring", None, self.connectstring)
		mode = context.execute("mode", None, self.mode)
		commit = context.execute("commit", None, self.commit)

		connection = context.connect(connectstring, mode=mode, commit=commit if commit is not None else context.commit)
		context.pushconnection(connectname, connection)
		context.count(self.__class__.__name__)
		return connection

	def source_format(self):
		yield from self._source_format(
			connectname=self.connectname,
			connectstring=self.connectstring,
			raiseexceptions=self.raiseexceptions,
			commit=self.commit,
		)


@register
class popconnection(Command):
	"""
	The :class:`!popconnection` command disconnects from the database connection
	with the name ``connectname`` and reverts to the previous connection
	registered for that name. (If ``connectname`` is ``None`` the default
	connection will be used). If the commit mode for the connection is ``"once"``
	the transaction will be committed before closing the connection.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, *, connectname=None, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.connectname = connectname

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} connectname={self.connectname!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connectname = context.execute("connectname", None, self.connectname)
		connection = context.popconnection(connectname)
		connection.close()
		context.count(self.__class__.__name__)
		return connection

	def source_format(self):
		yield from self._source_format(
			connectname=self.connectname,
			raiseexceptions=self.raiseexceptions,
		)


class _DatabaseCommand(Command):
	"""
	Base class of all commands that use a database connection.

	All database commands support the following parameters:

	``connectname`` : string (optional)
		The name of the connection to use for this command. (This connection must
		have been pushed by a :class:`pushconnection` command previously). Also
		``None`` can be specified explicitely to use the default connection.

	``connectstring`` : string (optional)
		If a ``connectstring`` is given a new connection to this database will
		be created just for this one command.

	If neither of these parameters is given, the default connection is used (and
	giving both is an error).

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, *, raiseexceptions=None, connectstring=None, connectname=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.connectstring = connectstring
		self.connectname = connectname
		self._single = False

	def beginconnection(self, context, connectstring, connectname):
		if connectstring is not None:
			self._single = True
			return context.connect(connectstring, context.commit)
		else:
			self._single = False
			return context.connection(connectname)

	def endconnection(self, context, connection):
		if connection.commit == "record":
			connection.connection.commit()
		if self._single: # This was a connection just for this one command
			self.connection.close()


class _SQLCommand(_DatabaseCommand):
	"""
	Common base class of :class:`ProcedureCommand` and :class:`SQLCommand`.
	"""

	@staticmethod
	def _createvar(cursor, type, value):
		var = cursor.var(type)
		var.setvalue(0, value)
		return var

	def _executesql(self, context, connection, query):
		cursor = connection.cursor

		queryargvars = {}
		varargs = {}
		for (argname, argvalue) in self.args.items():
			argvalue = context.execute(f"args.{argname}", None, argvalue)
			if isinstance(argvalue, sqlexpr):
				continue # no value
			if isinstance(argvalue, var):
				varargs[argname] = argvalue
				if argvalue.key is not None and argvalue.key in context.keys:
					argvalue = context.keys[argvalue.key]
				else:
					argvalue = cursor.var(argvalue.type)
			elif isinstance(argvalue, str) and len(argvalue) >= 4000:
				argvalue = self._createvar(cursor, cx_Oracle.CLOB, argvalue)
			elif isinstance(argvalue, bytes) and len(argvalue) >= 4000:
				argvalue = self._createvar(cursor, cx_Oracle.BLOB, argvalue)
			queryargvars[argname] = argvalue

		cursor.execute(query, queryargvars)

		newkeys = {}
		for (argname, argvalue) in varargs.items():
			if argvalue.key not in context.keys:
				value = queryargvars[argname].getvalue(0)
				newkeys[argname] = value
				if argvalue.key is not None:
					context.keys[argvalue.key] = value
		return newkeys


@register
class procedure(_SQLCommand):
	"""
	A :class:`!procedure` command calls an Oracle procedure in the database.
	The following parameters are supported:

	``name`` : string (required)
		The name of the procedure to be called (This may include ``.`` for
		calling a procedure in a package or one owned by a different user).

	``args`` : dictionary (optional)
		A dictionary with the names of the parameters as keys and the parameter
		values as values. PySQL supports all types as values that
		:mod:`cx_Oracle` supports. In addition to those, three special classes
		are supported:

		*	:class:`sqlexpr` objects can be used to specify that the paramater
			should be literal SQL. So e.g. ``sqlexpr("sysdate")`` will be the date
			when the PySQL script was executed.

		*	:class:`var` objects can be used to hold values that are ``OUT``
			parameters of the procedure. For example on first use of
			``var("foo_10")`` the value of the ``OUT`` parameter will be stored
			under the key ``"foo_10"``. The next time ``var("foo_10")`` is
			encountered the value stored under the key ``"foo_10"`` will be passed
			to the procedure. The type of the variable defaults to ``int``.
			If a different type is required it can be passed as the second
			argument to :class:`var`, e.g. ``var("foo_10", str)``.

		*	Finally all other commands can be called to get a value (for example
			the two commands :class:`loadbytes`  and :class:`loadstr` to load
			values from external files (as long as they are of type :class:`bytes`
			or :class:`str`). ``loadbytes("foo/bar.txt")`` will return with the
			content of the external file ``foo/bar.txt`` (as a :class:`bytes`
			object). If a :class:`str` object is required, :class:`loadstr` can
			be used. Encoding info can be passed like this::

				loadstr("foo/bar.txt", "utf-8", "replace")

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, name, *, raiseexceptions=None, connectstring=None, connectname=None, args=None):
		super().__init__(raiseexceptions=raiseexceptions, connectstring=connectstring, connectname=connectname)
		self.name = name
		self.args = args or {}

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		name = context.execute(None, None, self.name)
		connectstring = context.execute("connectstring", None, self.connectstring)
		connectname = context.execute("connectname", None, self.connectname)

		connection = self.beginconnection(context, connectstring, connectname)

		argsql = ", ".join(f"{an}=>{av}" if isinstance(av, sqlexpr) else f"{an}=>:{an}" for (an, av) in self.args.items())
		query = f"begin {name}({argsql}); end;"
		result = self._executesql(context, connection, query)

		context.count(connection.connectstring, self.__class__.__name__, name)

		self.endconnection(context, connection)

		return result or None

	def source_format(self):
		yield from self._source_format(
			self.name,
			raiseexceptions=self.raiseexceptions,
			connectstring=self.connectstring,
			connectname=self.connectname,
			args=self.args,
		)


@register
class sql(_SQLCommand):
	"""
	An :class:`!sql` command directly executes an SQL statement in the Oracle
	database. The following parameters are supported:

	``sql`` : string (required)
		The SQL to be executed. This may contain parameters in the form of
		``:paramname``. The values for those parameters will be taken from
		``args``.

	``args`` : dictionary (optional)
		A dictionary with the names of the parameters as keys and the parameter
		values as values. Similar to procedure calls :class:`var`,
		:class:`loadbytes` and :class:`loadstr` objects are supported. However
		:class:`sqlexpr` objects are not supported (they will be ignored).

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, sql, *, raiseexceptions=None, connectstring=None, connectname=None, args=None):
		super().__init__(raiseexceptions=raiseexceptions, connectstring=connectstring, connectname=connectname)
		self.sql = sql
		self.args = args or {}

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sql={self.sql!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		sql = context.execute(None, None, self.sql)
		connectstring = context.execute("connectstring", None, self.connectstring)
		connectname = context.execute("connectname", None, self.connectname)

		connection = self.beginconnection(context, connectstring, connectname)
		result = self._executesql(context, connection, sql)
		context.count(connection.connectstring, self.__class__.__name__)
		self.endconnection(context, connection)
		return result or None

	def source_format(self):
		yield from self._source_format(
			self.sql,
			raiseexceptions=self.raiseexceptions,
			connectstring=self.connectstring,
			connectname=self.connectname,
			args=self.args,
		)


class literalsql(_SQLCommand):
	"""
	A :class:`!sql` is used for SQL that appears literally in the
	PySQL file. So apart from the ``sql`` attribute is has no further usable
	attributes (i.e. ``raiseexceptions``, ``connectname`` and ``connectstring``
	from the base classes are all ``None``).
	"""

	def __init__(self, sql):
		super().__init__()
		self.sql = sql

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sql={self.sql!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		sql = context.execute(None, None, self.sql)
		if sql.endswith((";", "/")):
			sql = sql[:-1]
		connection = self.beginconnection(context, None, None)
		connection.cursor.execute(sql)
		context.count(connection.connectstring, self.__class__.__name__)
		self.endconnection(context, connection)

	def source(self, tabsize=None):
		sql = (self.sql or "").strip()
		if tabsize is not None:
			sql = sql.expandtabs(tabsize)
		return sql


class literalpy(_DatabaseCommand):
	"""
	A :class:`!literalpy` is used for Python code that appears literally in the
	PySQL file. So apart from the ``code`` attribute is has no further usable
	attributes (i.e. ``raiseexceptions``, ``connectname`` and ``connectstring``
	from the base classes are all ``None``).
	"""

	def __init__(self, code):
		super().__init__()
		self.code = code

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} code={self.code!r} location={self.location} at {id(self):#x}>"

	def globals(self, context, connection):
		vars = {command.__name__: CommandExecutor(command, context) for command in Command.commands.values()}
		vars["sqlexpr"] = sqlexpr
		vars["datetime"] = datetime
		vars["vars"] = context.keys
		vars["connection"] = connection.connection
		return vars

	def execute(self, context):
		code = context.execute(None, None, self.code)
		connection = self.beginconnection(context, None, None)

		vars = self.globals(context, connection)
		exec(code + "\n", vars, vars)

		context.count(connection.connectstring, self.__class__.__name__)
		self.endconnection(context, connection)

	def source(self, tabsize=None):
		return self.code.expandtabs(tabsize)


@register
class setvar(Command):
	"""
	The :class:`!setvar` command sets a variable to a fixed value. The following
	parameters are supported:

	``name``: string (required)
		The name of the variable to set.

	``value``: object (required)
		The value of the variable.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, name, value, *, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.name = name
		self.value = value

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} value={self.value!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		name = context.execute(None, None, self.name)
		value = context.execute(None, None, self.value)

		context.keys[name] = value
		context.count(self.__class__.__name__)

	def source_format(self):
		yield from self._source_format(
			self.name,
			self.value,
			raiseexceptions=self.raiseexceptions,
		)


@register
class unsetvar(Command):
	"""
	The :class:`!unsetvar` command deletes a variable. The parameter ``name``
	must be given and must contain the name of the variable.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, name, *, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.name = name

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		name = context.execute(None, None, self.name)

		context.keys.pop(name, None)
		context.count(self.__class__.__name__)

	def source_format(self):
		yield from self._source_format(
			self.name,
			raiseexceptions=self.raiseexceptions,
		)


@register
class raiseexceptions(Command):
	"""
	The :class:`!raiseexceptions` command changes the global error reporting mode
	for all subsequent commands. After::

		raiseexceptions(False)

	for all subsequent commands any exception will be reported and command
	execution will continue with the next command. ::

		raiseexceptions(True)

	will switch back to aborting the execution of the PySQL script once an
	exception is encountered.

	Note that the global configuration will only be relevant for commands that
	don't specify the ``raiseexceptions`` paramter themselves.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, *, value, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.value = value

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} value={self.value!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		value = context.execute(None, None, self.value)
		context.raiseexceptions[-1] = value
		context.count(self.__class__.__name__)

	def source_format(self):
		yield from self._source_format(
			self.value,
			raiseexceptions=self.raiseexceptions,
		)


@register
class pushraiseexceptions(Command):
	"""
	The :class:`!pushraiseexceptions` command changes the global error reporting
	mode for all subsequent commands, but remembers the previous exception
	handling mode. After::

		pushraiseexceptions(False)

	for all subsequent commands any exception will be ignored and command
	execution will continue with the next command. It is possible to switch back
	to the previous exception handling mode via::

		popraiseexceptions()

	Note that this global configuration will only be relevant for commands that
	don't specify the ``raiseexceptions`` parameter themselves.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, value, *, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.value = value

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} value={self.value!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		value = context.execute(None, None, self.value)
		context.raiseexceptions.append(value)
		context.count(self.__class__.__name__)

	def source_format(self):
		yield from self._source_format(
			self.value,
			raiseexceptions=self.raiseexceptions,
		)


@register
class popraiseexceptions(Command):
	"""
	The :class:`popraiseexceptions` command restores the previously active
	exception handling mode (i.e. the one active before the last
	:class:`pushraiseexceptions` command).

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, *, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		if len(context.raiseexceptions) <= 1:
			raise ValueError("raiseexception stack empty")
		oldvalue = context.raiseexceptions.pop()
		context.count(self.__class__.__name__)
		return oldvalue

	def source_format(self):
		yield from self._source_format(
			raiseexceptions=self.raiseexceptions,
		)


@register
class checkerrors(_DatabaseCommand):
	"""
	The :class:`!checkerrors` command checks that there are no compilation errors
	in the target schema. If there are, an exception will be raised.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`
	(but the value of the ``raiseexceptions`` key will be ignored).
	"""

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connectstring = context.execute("connectstring", None, self.connectstring)
		connectname = context.execute("connectname", None, self.connectname)

		connection = self.beginconnection(context, connectstring, connectname)
		connectstring = connection.connectstring
		connection.cursor.execute("select lower(type), name from user_errors group by lower(type), name")
		invalid_objects = [tuple(r) for r in connection.cursor]
		self.endconnection(context, connection)
		context.count(connectstring, self.__class__.__name__)

		if invalid_objects:
			raise CompilationError(invalid_objects)

		return pyexpr(f"no errors in {connectstring}")

	def source_format(self):
		yield from self._source_format()


@register
class scp(Command):
	"""
	The :class:`!scp` command creates a file by copying it via the ``scp``
	command. The following parameters are supported:

	``name`` : string (required)
		The name of the file to be created. It may contain ``format()`` style
		specifications containing any key that appeared in a :class:`procedure`
		or :class:`sql` command. These specifiers will be replaced by the correct
		key values. As these files will be copied via the ``scp`` command,
		ssh file names can be used.

	``content``: bytes (required)
		The content of the file to be created. This can also be a
		:class:`loadbytes` command, to load the content from an external file.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, *, name, content, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.name = name
		self.content = content

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} content={shortrepr(self.content)} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		name = context.execute(None, None, self.name)
		content = context.execute(None, None, self.content)

		filename = context.scpdirectory + name.format(**context.keys)

		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(self.content)
			tempname = f.name
		try:
			result = subprocess.run(["scp", "-q", tempname, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			if result.returncode:
				raise SCPError(result.returncode, (result.stdout or result.stderr).decode(errors="replace"))
		finally:
			os.remove(tempname)

		context.count(self.__class__.__name__)
		return content

	def source_format(self):
		yield from self._source_format(
			self.name,
			self.content,
			raiseexceptions=self.raiseexceptions,
		)


@register
class file(Command):
	"""
	The :class:`!file` command creates a file by directly saving it from Python.
	The following parameters are supported:

	``name`` : string (required)
		The name of the file to be created. It may contain ``format()`` style
		specifications containing any key that appeared in a :class:`procedure` or
		:class:`sql` command. These specifiers will be replaced by the correct
		key values.

	``content``: bytes (required)
		The content of the file to be created. This can also be a
		:class:`loadbytes` command, to load the content from an external file.

	``mode``: integer (optional)
		The file mode for the new file. If the mode is specified :func:`os.chmod`
		will be called on the file.

	``owner``: integer or string (optional)
		The owner of the file (as a user name or a uid).

	``group``: integer or string (optional)
		The owning group of the file (as a group name or a gid).
		If ``owner`` or ``group`` is given, :func:`os.chown` will be called on
		the file.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, name, content, *, mode=None, owner=None, group=None, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.name = name
		self.content = content
		self.mode = mode
		self.owner = owner
		self.group = group

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} content={shortrepr(self.content)} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		name = context.execute(None, None, self.name)
		content = context.execute(None, None, self.content)
		mode = context.execute("mode", None, self.mode)
		owner = context.execute("owner", None, self.owner)
		group = context.execute("group", None, self.group)

		filename = pathlib.Path(context.filedirectory + name.format(**context.keys))

		try:
			filename.write_bytes(content)
		except FileNotFoundError: # probably the directory doesn't exist
			parent = filename.parent
			if parent != filename:
				parent.mkdir(parents=True)
				filename.write_bytes(content)
			else:
				raise # we don't have a directory to make so pass the error on

		if mode:
			os.chmod(filename, mode)
		if owner or group:
			if owner:
				uid = owner
				if isinstance(uid, str):
					uid = pwd.getpwnam(uid)[2]
			else:
				uid = -1
			if group:
				gid = group
				if isinstance(gid, str):
					gid = grp.getgrnam(gid)[2]
			else:
				gid = -1
			os.chown(filename, uid, gid)

		context.count(self.__class__.__name__)
		return content

	def source_format(self):
		yield from self._source_format(
			self.name,
			self.content,
			mode=self.mode,
			owner=self.owner,
			group=self.group,
			raiseexceptions=self.raiseexceptions,
		)


@register
class resetsequence(_DatabaseCommand):
	"""
	The :class:`!resetsequence` command resets a sequence in the Oracle database
	to the maximum value of a field in a table. The following parameters are
	supported:

	``sequence``: string (required)
		The name of the sequence to reset.

	``table``: string (required)
		The name of the table that contains the field.

	``field``: string (required)
		The name of the field in the table ``table``. The sequence will be
		reset to a value so that fetching the next value from the sequence
		will deliver a value that is larger than the maximum value of the field
		``field`` in the table ``table``.

	``minvalue``: integer (optional, default taken from sequence)
		The minimum value for the sequence.

	``increment``: integer (optional, default taken from sequence)
		The increment (i.e. the step size) for the sequence.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, sequence, table, field, *, minvalue=None, increment=None, connectstring=None, connectname=None, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions, connectstring=connectstring, connectname=connectname)
		self.sequence = sequence
		self.table = table
		self.field = field
		self.minvalue = minvalue
		self.increment = increment

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sequence={self.sequence!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		sequence = context.execute(None, None, self.sequence)
		table = context.execute(None, None, self.table)
		field = context.execute(None, None, self.field)
		minvalue = context.execute("minvalue", None, self.minvalue)
		increment = context.execute("increment", None, self.increment)
		connectstring = context.execute("connectstring", None, self.connectstring)
		connectname = context.execute("connectname", None, self.connectname)

		connection = self.beginconnection(context, connectstring, connectname)

		cursor = connection.cursor

		# Fetch information about the sequence
		cursor.execute("select min_value, increment_by, last_number from user_sequences where lower(sequence_name)=lower(:name)", name=sequence)
		oldvalues = cursor.fetchone()
		if oldvalues is None:
			raise ValueError(f"sequence {sequence!r} unknown")
		increment = self.increment
		if increment is None:
			increment = oldvalues[1]
		minvalue = self.minvalue
		if minvalue is None:
			minvalue = oldvalues[0]
		cursor.execute(f"select {sequence}.nextval from dual")
		seqvalue = cursor.fetchone()[0]

		# Fetch information about the table values
		cursor.execute(f"select nvl(max({field}), 0) from {table}")
		tabvalue = cursor.fetchone()[0]

		step = max(tabvalue, minvalue) - seqvalue
		if step:
			cursor.execute(f"alter sequence {sequence} increment by {step}")
			cursor.execute(f"select {sequence}.nextval from dual")
			seqvalue = cursor.fetchone()[0]
			cursor.execute(f"alter sequence {sequence} increment by {increment}")
		else:
			seqvalue = None

		context.count(connection.connectstring, self.__class__.__name__)

		self.endconnection(context, connection)

		return seqvalue

	def source_format(self):
		yield from self._source_format(
			self.sequence,
			self.table,
			self.field,
			mode=self.mode,
			owner=self.owner,
			group=self.group,
			minvalue=self.minvalue,
			increment=self.increment,
			connectstring=self.connectstring,
			connectname=self.connectname,
			raiseexceptions=self.raiseexceptions,
		)


@register
class comment(Command):
	"""
	The :class:`!comment` command does nothing.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, comment=None):
		super().__init__()
		self.comment = comment

	def __str__(self):
		return f"comment {self.location}"

	def execute(self, context):
		context.count(self.__class__.__name__)

	def source(self, tabsize=None):
		comment = self.comment
		if tabsize is not None:
			comment = comment.expandtabs(tabsize)
		return comment


@register
class loadbytes(Command):
	"""
	The :class:`!loadbytes` command can be used to load a :class:`bytes` object
	from an external file. The following parameters are supported:

	:obj:`filename` : string (required)
		The name of the file to be loaded. The filename is treated as being
		relative to the directory containing the pysql file that contains 
		:class:`loadbytes` command.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, filename, *, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.filename = filename

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} filename={self.name!r} {self.location} at {id(self):#x}>"

	def execute(self, context):
		"""
		Read the file and return the file content as a :class:`bytes` object.
		"""
		filename = context.execute(None, None, self.filename)
		filename = context.basedir/filename
		data = filename.read_bytes()
		context.count(self.__class__.__name__)
		return data

	def source_format(self):
		yield from self._source_format(
			self.filename,
			raiseexceptions=self.raiseexceptions,
		)


@register
class loadstr(Command):
	"""
	The :class:`!loadstr` command can be used to load a :class:`str` object
	from an external file. The following parameters are supported:

	:obj:`filename` : string (required)
		The name of the file to be loaded. The filename is treated as being
		relative to the directory containing the PySQL file that contains the
		the :class:`!loadstr` command.

	:obj:`encoding` : string (optional)
		The encoding used for decoding the bytes in the file to text.

	:obj:`errors` : string (optional)
		The error handling mode for decoding.
	"""

	def __init__(self, filename, *, encoding=None, errors="strict", raiseexceptions=None):
		"""
		Create a new :class:`loadbytes` object. 
		"""
		super().__init__(raiseexceptions=raiseexceptions)
		self.filename = filename
		self.encoding = encoding
		self.errors = errors

	def __repr__(self):
		result = f"<{self.__class__.__module__}.{self.__class__.__qualname__} filename={self.filename!r}"
		if self.encoding is not None:
			result += f", encoding={self.encoding!r}"
		if self.errors is not None:
			result += f", errors={self.errors!r}"
		result += f"{self.location} at {id(self):#x}>"
		return result

	def execute(self, context):
		"""
		Read the file and return the file content as a :class:`str` object.
		"""
		filename = context.execute(None, None, self.filename)
		encoding = context.execute("encoding", None, self.encoding)
		errors = context.execute("errors", "strict", self.errors)

		filename = context.basedir/filename
		data = filename.read_text(encoding=encoding, errors=errors)
		context.count(self.__class__.__name__)
		return data

	def source_format(self):
		yield from self._source_format(
			self.filename,
			encoding=self.encoding,
			errors=self.errors,
			raiseexceptions=self.raiseexceptions,
		)


@register
class var(Command):
	"""
	:class:`var` commands are used to mark procedure values that are ``OUT``
	parameters. On first use the parameter is used as an ``OUT`` parameter and
	PySQL will remembers the OUT value under the unique key specified in the
	constructor. When a :class:`var` object is used a second time its value
	will be passed to the procedure as a normal ``IN`` parameter instead.
	The following parameters are supported:

	:obj:`key` : string (required)
		A unique name for the value.

	:obj:`type` : class )optional)
		The type of the value (defaulting to :class:`int`).

	Note that when the :obj:`key` is :const:`None`, PySQL will *not* remember
	the value, instead each use of ``var(None)`` will create a new OUT
	parameter. This can be used for OUT parameters whose values is not
	required by subsequent commands.
	"""

	def __init__(self, key=None, type=int):
		super().__init__(raiseexceptions=None)
		self.key = key
		self.type = type

	def __repr__(self):
		if self.type is int:
			return f"var({self.key!r})"
		else:
			return f"var({self.key!r}, {format_class(self.type)})"

	def __bool__(self):
		return False

	def execute(self, context):
		key = context.execute(None, None, self.key)
		type = context.execute(None, str, self.type)

		context.count(self.__class__.__name__)

		if key in context.keys:
			value = context.keys[key]
			if value is not None and not isinstance(value, type):
				raise TypeError(f"{value!r} is not of type {format_class(type)}")
			return value
		else:
			return self

	def source_format(self):
		yield repr(self)


@register
class env(Command):
	"""
	:class:`env` commands return an environment variable:
	The following parameters are supported:

	:obj:`name` : string (required)
		The name of the environment variable.
	"""

	def __init__(self, name):
		super().__init__(raiseexceptions=None)
		self.name = name

	def __repr__(self):
		return f"env({self.name!r})"

	def execute(self, context):
		name = context.execute(None, None, self.name)
		return os.environ.get(name, None)

	def source_format(self):
		yield repr(self)


class CommandExecutor:
	"""
	A :class:`!CommandExecutor` object wraps a :class:`Command` object in a
	callable. Calling the :class:`!CommandExecutor` object executes the command
	using the specified context and returns the command result.

	This is used to allow calling commands in the Python source code of
	by :class:`literalpy` commands.
	"""
	def __init__(self, command, context):
		self.command = command
		self.context = context

	def __call__(self, *args, **kwargs):
		return self.command(*args, **kwargs).execute(self.context)


###
### Classes to be used by the PySQL commands
###


class sqlexpr:
	"""
	An :class:`sqlexpr` object can be used to specify an SQL expression as a
	procedure parameter instead of a fixed value. For example passing the current
	date (i.e. the date of the import) can be done with ``sqlexpr("sysdate")``.
	"""

	def __init__(self, expression):
		self.expression = expression

	def __repr__(self):
		return f"sqlexpr({self.expression!r})"


class pyexpr:
	"""
	A :class:`pyexpr` object can be used to embed literal Python source code
	in a PySQL file.

	.. note::
		As PySQL source code is evaluated via :func:`eval` anyway, it it always
		possible to embed Python expressions in PySQL source code. However this
		doesn't roundtrip, i.e. printing the PySQL command via
		:meth:`~Command.source` outputs the value of a "literal" Python expression.
	"""

	def __init__(self, expression):
		self.expression = expression

	def __repr__(self):
		return self.expression


###
### Exception classes and location information
###

class LocationError(Exception):
	def __init__(self, location):
		self.location = location

	def __str__(self):
		return f"in {self.location}"


class CommandError(Exception):
	def __init__(self, command):
		self.command = command

	def __str__(self):
		return str(self.command)


class CompilationError(Exception):
	"""
	Exception raised by :class:`checkerrors` when invalid database
	objects are encountered.
	"""
	def __init__(self, objects):
		self.objects = objects

	def __str__(self):
		if len(self.objects) == 1:
			return f"one invalid db object: {self.objects[0][0]} {self.objects[0][1]}"
		else:
			objects = ", ".join(f"{object[0]} {object[1]}" for object in self.objects)
			return f"{len(self.objects):,} invalid db objects: {objects}"


class SCPError(Exception):
	"""
	Exception raised by :class:`scp` when a call to the ``scp`` command
	fails.
	"""

	def __init__(self, status, msg):
		self.status = status
		self.msg = msg

	def __str__(self):
		return f"scp failed with code {self.status}: {self.msg}"


class Location:
	"""
	The location of a PySQL/SQL command in a pysql file.
	"""

	def __init__(self, filename, startline, endline):
		self.filename = filename
		self.startline = startline
		self.endline = endline

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} filename={self.filename!r} startline={self.startline!r} endline={self.endline!r} at {id(self):#x}>"

	def __str__(self):
		if self.startline is None and self.endline is None:
			return str(self.filename)
		else:
			return f"{self.filename} :: {self.lines()}"

	def lines(self):
		if self.startline is None and self.endline is None:
			return "?"
		elif self.startline == self.endline:
			return f"{self.startline:,}"
		else:
			return f"{self.startline:,}-{self.endline:,}"


def define(arg):
	(name, _, value) = arg.partition("=")
	(name, _, type) = name.partition(":")

	if type == "int":
		if not value:
			return 0
		try:
			return int(value)
		except ValueError:
			raise argparse.ArgumentTypeError(f"{value!r} is not a legal integer value")
	elif type == "float":
		if not value:
			return 0.
		try:
			return float(value)
		except ValueError:
			raise argparse.ArgumentTypeError(f"{value!r} is not a legal float value")
	elif type == "bool":
		if value in ("", "0", "no", "false", "False"):
			return False
		elif value in ("1", "yes", "true", "True"):
			return True
		else:
			raise argparse.ArgumentTypeError(f"{value!r} is not a legal bool value")
	elif type and type != "str":
		raise argparse.ArgumentTypeError(f"{type!r} is not a legal type")
	return value


def source_format(object):
	if isinstance(object, Command):
		yield from object.source_format()
	elif isinstance(object, str):
		if "\n" in object:
			lines = object.splitlines(True)
			for (i, line) in enumerate(lines):
				yield repr(line)
				if i != len(lines)-1:
					yield None
		else:
			yield repr(object)
	elif isinstance(object, dict):
		yield "dict("
		yield 1
		yield None
		for (i, (key, value)) in enumerate(object.items()):
			# Keys must always be strings
			yield f"{key}="
			if isinstance(value, str) and "\n" in value:
				yield 1
				yield None
			yield from source_format(value)
			if i == len(object)-1:
				yield (",", "")
			else:
				yield (",", ", ")
			if isinstance(value, str) and "\n" in value:
				yield -1
			yield None
		yield -1
		yield ")"
	elif isinstance(object, list):
		yield "["
		yield 1
		yield None
		for value in object:
			yield from source_format(value)
			if i == len(object)-1:
				yield (",", "")
			else:
				yield (",", ", ")
			yield None
		yield -1
		yield "]"
	else:
		yield repr(object)


def source(object, tabsize=None):
	parts = list(source_format(object))

	if sum(len(part if isinstance(part, str) else part[1]) for part in parts if isinstance(part, (str, tuple))) <= 80:
		return "".join(part if isinstance(part, str) else part[1] for part in parts if isinstance(part, (str, tuple)))
	else:
		indent = 0
		needindent = True
		output = []
		for part in parts:
			if isinstance(part, str):
				if needindent:
					output.append("\t"*indent)
					needindent = False
				output.append(part)
			elif isinstance(part, int):
				indent += part
			elif part is None:
				output.append("\n")
				needindent = True
			else: # tuple
				output.append(part[0])
		output = "".join(output)
		if tabsize is not None:
			output = output.expandtabs(tabsize)
		return output


###
### Main script function
###

def main(args=None):
	p = argparse.ArgumentParser(description="Import a pysql file into an Oracle database", epilog="For more info see http://python.livinglogic.de/pysql.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("file", nargs="?", help="Name of the pysql file (default: read from stdin)", type=argparse.FileType("r"), default=sys.stdin)
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", choices=("dot", "type", "file", "line", "full"))
	p.add_argument("-c", "--commit", dest="commit", help="When should database transactions be committed? (default %(default)s)", default="once", choices=("record", "once", "never"))
	p.add_argument("-s", "--scpdirectory", dest="scpdirectory", metavar="DIR", help="File name prefix for files to be copied via the 'scp' command (default: current directory)", default="")
	p.add_argument("-f", "--filedirectory", dest="filedirectory", metavar="DIR", help="File name prefix for files to be copied via the 'file' command (default: current directory)", default="")
	p.add_argument("-t", "--terminator", dest="terminator", metavar="STRING", help="Terminator after an SQL command (should be a valid SQL comment; default %(default)r)", default="-- @@@")
	p.add_argument(      "--tabsize", dest="tabsize", metavar="INTEGER", help="Number of spaces a tab expands to when printing source (default %(default)r)", type=int, default=8)
	p.add_argument(      "--context", dest="context", metavar="INTEGER", help="Maximum number of lines when printing source code (default %(default)r)", type=int, default=None)
	p.add_argument("-z", "--summary", dest="summary", help="Output a summary after executing all commands", default=False, action="store_true")
	p.add_argument("-D", "--define", dest="defines", metavar="VARSPEC", help="Set variables before executing the script (can be specified multiple times). The format for VARSPEC is: 'name' or 'name=value' or 'name:type' or 'name:type=value'. Type may be 'str', 'bool', 'int' or 'float'.", default=[], action="append", type=define)

	args = p.parse_args(args)

	context = Context(
		connectstring=args.connectstring,
		scpdirectory=args.scpdirectory,
		filedirectory=args.filedirectory,
		commit=args.commit,
		terminator=args.terminator,
		tabsize=args.tabsize,
		context=args.context,
		verbose=args.verbose,
		summary=args.summary,
		vars=args.defines
	)
	context.executeall(args.file)


if __name__ == "__main__":
	sys.exit(main())
