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
line that starts with ``-- @@@``. :mod:`pysql` will strip off a trailing
``;`` or ``/`` from the command and execute it. Any exception that is raised
as a result of executing the command will stop the script and be reported.
This is in contrast to how ``sqlplus`` executes SQL commands. ``sqlplus``
would continue after an error and exit with status code 0 even if there were
errors. It is also possible to explicitely ignore any exception raised by the
command by specifying a different exception handling mode.

A PySQL file that only contains SQL commands is still a valid SQL file from
the perspective of Oracle, so it still can be executed via ``sqlplus``.


PySQL commands
--------------

A PySQL file may also contain PySQL commands. A PySQL command looks like a
Python dictionary literal. This literal must either be contained in a single
line or it must start with a line that only contains ``{`` and end at a
line that only contains ``}``.

For further information about the different commands and which keys they support,
see the class :class:`Command` and its subclasses.


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

	-- @@@ import data

	{
		'type': 'procedure',
		'name': 'person_insert',
		'args': {
			'c_user': 'import',
			'p_per_id': var('per_id_max'),
			'p_per_firstname': 'Max',
			'p_per_lastname': 'Mustermann',
		}
	}

	{
		'type': 'procedure',
		'name': 'contact_insert',
		'args': {
			'c_user': 'import',
			'p_per_id': var('per_id_max'),
			'p_con_id': var('con_id_max'),
			'p_con_type': 'email',
			'p_con_value': 'max@example.org',
		}
	}

	{
		'type': 'file',
		'name': 'portrait_{per_id_max}.png',
		'content': b'\\x89PNG\\r\\n\\x1a\\n...',
	}

	{
		'type': 'resetsequence',
		'sequence': 'person_seq',
		'table': 'person',
		'field': 'per_id',
	}

	{"type": "compileall"}

	{"type": "checkerrors"}

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
``per_id`` in the table ``person``. Finally it will recompile all schema objects
and then make sure that no errors exist in the schema.


Multiple database connections
=============================

PySQL can handle multiple database connections. New database connections can be
opened with the ``pushconnnection`` command. This command opens a new database
connection and stores it under a name. Subsequent commands can refer to that
name to specify the database connection to use. The ``popconnection`` command
disconnects from the database and reverts to the previous connection for that
name (which might not exist). An example looks like this::

	{
		"type": "pushconnection",
		"connectstring": "user/pwd@db",
		"connectname": "db",
	}

	{
		"type": "procedure",
		"name": "test",
		"connectname": "db",
	}

	{
		"type": "popconnection",
		"connectname": "db",
	}

The connection with the name ``None`` is the "default connection". This
connection will be used for all normal SQL commands and all PySQL commands that
don't have a ``"connectname"`` key (or where the ``"connectname"`` key is
``None``).


Variables
=========

Variable objects can be used to receive out parameters of procedure calls or
SQL statements. A variable object can be specified like this ``var("foo")``.
``"foo"`` is the "name" of the variable. When a variable object is passed
to a procedure the first time (i.e. the variable object is uninitialized),
a ``cx_Oracle`` ``var`` object will be passed and the resulting value after
the call will be stored under the name of the variable. When the variable is
used in a later command the stored value will be used instead. (Note that it's
not possible to use the same variable twice in the same procedure call,
if it hasn't been used before, however in later commands this is no problem).

The type of the variable defaults to ``int``, but a different type can be passed
when creating the object like this: ``var("foo", str)``.

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
The ``loadbytes`` function loads a ``bytes`` object from an external file
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
		modes are: ``dot`` (one dot for each command), ``type`` (each command type)
		or ``full`` (detailed output for each command/procedure call)

	``-z``, ``--summary``
		Give a summary of the number of commands executed and procedures called.

	``-c``, ``--commit``
		Specifies when to commit database transactions. ``record`` commits after
		every command. ``once`` (the default) commits at the end of the script
		(or when a connection is popped) and ``never`` rolls back the transaction
		after all commands.

	``-s``, ``--scpdirectory``
		The base directory for ``scp`` file copy commands. As files are copied
		via ``scp`` this can be a remote filename (like
		``root@www.example.org:~/uploads/``) and must include a trailing ``/``.

	``-f``, ``--filedirectory``
		The base directory for ``file`` file save commands. It must include
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

# We're importing ``datetime`` to make it available to ``eval()``
import sys, os, os.path, argparse, operator, collections, datetime, tempfile, subprocess

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


class Connection:
	def __init__(self, connectstring, commit):
		self.connection = cx_Oracle.connect(connectstring)
		self.cursor = self.connection.cursor()
		self.commit = commit

	def connectstring(self):
		return f"{self.connection.username}@{self.connection.tnsentry}"

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
		return f"connection {self.connectstring()}"

	def __repr__(self):
		return f"<Connection to {self.connectstring()}>"


class Context:
	"""
	A :class:`Context` objects contains the configuration and run time information
	required for importing a PySQL file.
	"""
	def __init__(self, connectstring=None, scpdirectory="", filedirectory="", commit="once", terminator="-- @@@", raiseexceptions=True, verbose=0, summary=False, vars=None):
		self.keys = {v.key: v for v in vars} if vars else {}
		self.connections = {}
		self.commit = commit
		self.scpdirectory = scpdirectory
		self.filedirectory = filedirectory
		self.terminator = terminator
		self.raiseexceptions = [raiseexceptions]
		self.verbose = verbose
		self.summary = summary
		self.commandcounts = collections.Counter()
		self.errorcount = 0
		self.totalcount = 0
		self._location = None
		if connectstring is not None:
			self.pushconnection(None, self.connect(connectstring, commit))

	def connect(self, connectstring, commit="once"):
		return Connection(connectstring, commit)

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

	def var(self, key, type=int):
		if key in self.keys:
			value = self.keys[key]
			if value is not None and not isinstance(value, type):
				raise TypeError(f"{value!r} is not of type {format_class(type)}")
			return value
		else:
			return var(key, type)

	def loadbytes(self, filename):
		return loadbytes(filename).execute(self._location.filename)

	def loadstr(self, filename, encoding=None, errors="strict"):
		return loadstr(filename, encoding, errors).execute(self._location.filename)

	def commandintro(self, command):
		if self.verbose == "dot":
			print(".", end="", flush=True)
		elif self.verbose == "type":
			print(" " + command.type, end="", flush=True)
		elif self.verbose == "full":
			print(f"pysql #{self.totalcount+1:,} :: {command.location}", end="", flush=True)

	def commandstart(self, *messages):
		if self.verbose == "full":
			output = []
			for (i, message) in enumerate(messages):
				if i == len(messages)-1 and i:
					output.append(" >> ")
				else:
					output.append(" :: ")
				output.append(message)
			print("".join(output), end="", flush=True)

	def commandend(self, message=None):
		if self.verbose == "full":
			if message is not None:
				print(f" -> {message}", flush=True)
			else:
				print(flush=True)

	def _load(self, stream):
		"""
		Load a PySQL file from :obj:`stream`. :obj:`stream` must be an iterable
		over lines that contain the PySQL commands.

		This function is a generator. Its output are the PySQL command objects
		(i.e. instances of :class:`Command`).
		"""
		lines = []

		globals = {
			"var": self.var,
			"sql": sql,
			"loadbytes": self.loadbytes,
			"loadstr": self.loadstr,
			"datetime": datetime,
		}

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
					if text:
						args = {}
						lines.clear()
						if text.startswith("{") and text.endswith("}"):
							block = eval(text, globals)
							args.update(block)
							if "type" not in args:
								args["type"] = "procedure"
						elif text.endswith((";", "/")):
							args["type"] = "sql"
							args["sql"] = text[:-1]
						else:
							raise ValueError(f"block terminator {text[-1:]!r} unknown")

						type = args.pop("type")
						if "raiseexceptions" not in args:
							args["raiseexceptions"] = self.raiseexceptions[-1]
						command = Command.fromdict(type, self._location, args)
						if isinstance(command, IncludeCommand):
							if not command.name:
								raise MissingKeyError("include", "name")
							filename = os.path.join(os.path.dirname(command.location.filename), command.name)
							with open(filename, "r", encoding="utf-8") as f:
								yield from self._load(f)
						else:
							yield command
			except Exception as exc:
				raise Error(self._location) from exc

		state = None # values ``"py"`` (inside PySQL block), ``"sql"`` (inside SQL block), ``None`` outside of any block
		for (i, line) in enumerate(stream, 1):
			line = line.rstrip()
			if state is None:
				if line.startswith("{"):
					lines.append((i, line))
					if line.endswith("}"):
						yield from makeblock()
					else:
						state = "py"
				elif line.startswith(self.terminator):
					pass # Still outside the block
				elif line.strip():
					lines.append((i, line))
					state = "sql"
			elif state == "py":
				lines.append((i, line))
				if line == "}": # A single unindented ``}``
					yield from makeblock()
					state = None
			elif state == "sql":
				if line.startswith(self.terminator):
					yield from makeblock()
					state = None
				else:
					lines.append((i, line))
		yield from makeblock()

	def executeall(self, stream):
		"""
		Execute all command in :obj:`stream`. :obj:`stream` must be an iterable
		over lines that contain the PySQL commands.
		"""
		try:
			if self.verbose == "type":
				print("commands:", end="", flush=True)
			for command in self._load(stream):
				try:
					self.commandintro(command)
					command.execute(self)
				except Exception as exc:
					if command.raiseexceptions:
						if self.verbose == "type":
							print("(error)", flush=True)
						elif self.verbose:
							print()
						raise Error(command) from exc
					else:
						self.errorcount += 1
						if self.verbose == "dot":
							print("!", end="", flush=True)
						elif self.verbose == "type":
							print("(error)", end="", flush=True)
						elif self.verbose == "full":
							exctext = str(exc).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
							print(f" -> ignored {format_class(exc.__class__)}: {exctext}")
			for connections in self.connections.values():
				for connection in connections:
					if connection.commit == "once":
						connection.connection.commit()
					elif connection.commit == "never":
						connection.connection.rollback()
		finally:
			if self.verbose in ("dot", "type"):
				print()
		self._printsummary()

	def _printsummary(self):
		if self.summary:
			if self.verbose:
				print()
			print("Command summary:")
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
					print()
					if connection:
						print(f"Connection {connection}:")
					else:
						print("Other commands:")
				lastconnection = connection
				anyoutput = True
				keys = " ".join(key[1:]) if len(key) > 1 else key[0]
				print(f"    {count:>{totallen},} {keys}")
			if self.errorcount:
				print("")
				print(f"Exceptions: {self.errorcount:,} exception{'s' if self.errorcount != 1 else ''} ignored")
			if anyoutput:
				print("")
				print(f"Total: {self.totalcount:,} command{'s' if self.totalcount != 1 else ''} executed")
			if not anyoutput:
				print("    no commands executed")

	def count(self, *args):
		self.commandcounts[args] += 1
		self.totalcount += 1


###
### Command classes
###

class Command:
	"""
	The base class of all commands. A :class:`Command` object is created from
	a command dictionary literal in a PySQL file. The keys in the command
	dictionary that are supported by all command types are the following:

	``type`` : string (optional)
		This is either ``"procedure"`` (the default), ``"sql"``, ``"file"``,
		``"scp"``, ``"resetsequence"``, ``"setvar"``, ``"include"``,
		``"compileall"``, ``"checkerrors"``, ``"pushconnection"``,
		``"popconnection"``, ``"raiseexceptions"``, ``"pushraiseexceptions"``
		or ``"popraiseexceptions"``  and specifies the type of the PySQL command.

	``raiseexceptions`` : bool (optional)
		Specifies whether exceptions that happen during the execution of the
		command should be reported and terminate the script (``True``), or
		should be ignored (``False``). ``None`` uses the global configuration.

	``comment`` : string (optional)
		This key will be ignored completely, but can be used to add a comment
		to a command.
	"""

	def __init__(self, location, *, raiseexceptions=None, comment=None):
		self.location = location
		self.raiseexceptions = raiseexceptions
		self.comment = comment

	commands = {}

	@classmethod
	def fromdict(cls, type, location, d):
		if type in cls.commands:
			return cls.commands[type](location, **d)
		raise ValueError(f"command type {type!r} unknown")

	def __str__(self):
		return f"{self.type} command {self.location}"


def register(cls):
	Command.commands[cls.type] = cls
	return cls


@register
class IncludeCommand(Command):
	"""
	The ``"include"`` command includes another PySQL file. The filename is read
	from the key ``"name"``. This name is interpreted as being relative to the
	directory with the file containing the ``include`` command.

	Additionally the keys ``"raiseexceptions"`` and ``"comment"`` from the base
	class are supported.
	"""

	type = "include"

	def __init__(self, location, *, name, raiseexceptions=None, comment=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)
		self.name = name

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"incluce command {self.location}"


@register
class PushConnectionCommand(Command):
	"""
	The ``"pushconnection"`` command connects to the database given in the
	connectstring in the key ``"connectstring"`` and pushes the connection under
	the name from the key ``"connectname"``. (If ``"connectname"`` is not given
	or is ``None``, the connection will be pushed as the default connection).
	``"commit"`` can be given to specify the commit mode for this connection
	(``"record"``, ``"once"`` or ``"never"``).

	Additionally the keys ``"raiseexceptions"`` and ``"comment"`` from the base
	class are supported.
	"""

	type = "pushconnection"

	def __init__(self, location, *, connectstring, raiseexceptions=None, comment=None, connectname=None, commit=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)
		self.connectstring = connectstring
		self.connectname = connectname
		self.commit = commit

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} connectname={self.connectname!r} connection={self.connection!r} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"pushconnection command {self.location}"

	def execute(self, context):
		connectname = "default connection" if self.connectname is None else f"connection {self.connectname!r}"
		context.commandstart(f"push {self.connectstring!r} as {connectname}")

		context.pushconnection(self.connectname, context.connect(self.connectstring, self.commit if self.commit is not None else context.commit))

		context.commandend("done")


@register
class PopConnectionCommand(Command):
	"""
	The ``"popconnection"`` command disconnects from the database connection with
	the name in the key ``"connectname"`` and reverts to the previous connection
	registered for that name. (If ``"connectname"`` is ``None`` the default
	connection will be used). If the commit mode for the connection is ``"once"``
	the transaction will be committed before closing the connection.

	Additionally the keys ``"raiseexceptions"`` and ``"comment"`` from the base
	class are supported.
	"""

	type = "popconnection"

	def __init__(self, location, *, connectname=None, raiseexceptions=None, comment=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)
		self.connectname = connectname

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} connectname={self.connectname!r} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"popconnection command {self.location}"

	def execute(self, context):
		connectname = "default connection" if self.connectname is None else f"connection {self.connectname!r}"
		context.commandstart(f"pop {connectname}")

		connection = context.popconnection(self.connectname)
		connectstring = connection.connectstring()
		connection.close()

		context.commandend(f"popped {connectstring}")


class _DatabaseCommand(Command):
	"""
	Base class of all commands that use a database connection.

	All database commands support the following keys:

	``"connectname"`` : string (optional)
		The name of the connection to use for this command. (This connection must
		have been pushed by a :class:`PushConnectionCommand` previously). Also
		``None`` can be specified explicitely to use the default connection.

	``"connectstring"`` : string (optional)
		If a ``"connectstring"`` is given a new connection to this database will
		be created  just for this one command.

	If neither of these keys is given, the default connection is used (and
	giving both is an error).

	Additionally the keys ``"raiseexceptions"`` and ``"comment"`` from the base
	class are supported.
	"""

	def __init__(self, location, *, raiseexceptions=None, comment=None, connectstring=None, connectname=None):
		if connectstring is not None and connectname is not None:
			raise ValueError("connectstring and connectname can't be specified simultaneously")
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)
		self.connectstring = connectstring
		self.connectname = connectname

	def beginconnection(self, context):
		if self.connectstring is not None:
			return context.connect(self.connectstring, context.commit)
		else:
			return context.connection(self.connectname)

	def endconnection(self, context, connection):
		if connection.commit == "record":
			connection.connect.commit()
		if self.connectstring is not None: # This was a connection just for this one command
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

	def _executesql(self, context, query, connection):
		cursor = connection.cursor
		queryargvars = {}
		for (argname, argvalue) in self.args.items():
			if isinstance(argvalue, sql):
				continue # no value
			if isinstance(argvalue, var):
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
		for (argname, argvalue) in self.args.items():
			if isinstance(argvalue, var) and argvalue.key not in context.keys:
				value = _makevalue(argname, queryargvars[argname].getvalue(0))
				newkeys[argname] = value
				if argvalue.key is not None:
					context.keys[argvalue.key] = value
		return newkeys

	def _formatargs(self, context):
		args = []
		if self.args:
			for (argname, argvalue) in self.args.items():
				if isinstance(argvalue, str):
					argvalue = _reprstr(argvalue)
				elif isinstance(argvalue, bytes):
					argvalue = _reprbytes(argvalue)
				else:
					argvalue = repr(argvalue)
				arg = f"{argname}={argvalue}"
				args.append(arg)
		return ", ".join(args)


@register
class ProcedureCommand(_SQLCommand):
	"""
	A ``"procedure"`` command calls an Oracle procedure in the database.
	The following keys are supported in the command dictionary:

	``"name"`` : string (required)
		The name of the procedure to be called (This may include ``.`` for
		calling a procedure in a package or one owned by a different user).

	``"args"`` : dictionary (optional)
		A dictionary with the names of the parameters as keys and the parameter
		values as values. PySQL supports all types as values that
		:mod:`cx_Oracle` supports. In addition to those, three special classes
		are supported:

		*	:class:`sql` objects can be used to specify that the paramater
			should be literal SQL. So e.g. ``sql("sysdate")`` will be the date
			when the PySQL script was executed.

		*	:class:`var` objects can be used to hold values that are ``OUT``
			parameters of the procedure. For example on first use of
			``var("foo_10")`` the value of the ``OUT`` parameter will be stored
			under the key ``"foo_10"``. The next time ``var("foo_10")`` is
			encountered the value stored under the key ``"foo_10"`` will be passed
			to the procedure. The type of the variable defaults to ``int``.
			If a different type is required it can be passed as the second
			argument to :class:`var`, e.g. ``var("foo_10", str)``.

		*	Finally :func:`loadbytes`  and :func:`loadstr` objects can be used
			to load values from external files (as long as they are of type
			:class:`bytes` or :class:`str`). ``loadbytes("foo/bar.txt")`` will
			be replaced with the content of the external file ``foo/bar.txt``
			(as a :class:`bytes` object). If a :class:`str` object is required,
			:func:`loadstr` can be used. Encoding info can be passed like this::

				loadstr("foo/bar.txt", "utf-8", "replace")

	Additionally the keys ``"raiseexceptions"``, ``"comment"``, ``"connectname"``
	and ``"connectstring"`` from the base classes are supported.
	"""

	type = "procedure"

	def __init__(self, location, *, name, raiseexceptions=None, comment=None, connectstring=None, connectname=None, args=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment, connectstring=connectstring, connectname=connectname)
		self.name = name
		self.args = args or {}

	def __repr__(self):
		if self.args:
			return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} args={self.args!r} {self.location} at {id(self):#x}>"
		else:
			return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"procedure command {self.location}"

	def _formatprocedurecall(self, context):
		return f"{self.name}({self._formatargs(context)})"

	def execute(self, context):
		connection = self.beginconnection(context)

		context.commandstart(str(connection), f"procedure {self._formatprocedurecall(context)}")

		queryargvalues = {}
		for (argname, argvalue) in self.args.items():
			if isinstance(argvalue, sql):
				argvalue = argvalue.expression
			else:
				argvalue = f":{argname}"
			queryargvalues[argname] = argvalue

		args = ", ".join(f"{argname}=>{argvalue}" for (argname, argvalue) in queryargvalues.items())
		query = f"begin {self.name}({args}); end;"
		result = self._executesql(context, query, connection)

		context.count(connection.connectstring(), self.type, self.name)

		self.endconnection(context, connection)

		if result:
			message = ", ".join(f"{argname}={argvalue!r}" for (argname, argvalue) in result.items())
		else:
			message = "done"

		context.commandend(message)

		return result


@register
class SQLCommand(_SQLCommand):
	"""
	An ``"sql"`` command directly executes an SQL statement in the Oracle database.
	The following keys are supported in the command dictionary:

	``"sql"`` : string (required)
		The SQL to be executed. This may contain parameters in the form of
		``:paramname``. The values for those parameters will be taken from
		``args``.

	``"args"`` : dictionary (optional)
		A dictionary with the names of the parameters as keys and the parameter
		values as values. Similar to procedure calls :class:`var`,
		:class:`loadbytes` and :class:`loadstr` objects are supported. However
		:class:`sql` objects are not supported (they will be ignored).

	Additionally the keys ``"raiseexceptions"``, ``"comment"``, ``"connectname"``
	and ``"connectstring"`` from the base classes are supported.
	"""

	type = "sql"

	def __init__(self, location, *, sql, raiseexceptions=None, comment=None, connectstring=None, connectname=None, args=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment, connectstring=connectstring, connectname=connectname)
		self.sql = sql
		self.args = args or {}

	def __repr__(self):
		if self.args:
			return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sql={self.sql!r} args={self.args!r} {self.location} at {id(self):#x}>"
		else:
			return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sql={self.sql!r} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"sql command {self.location}"

	def _formatsql(self, context):
		if self.args:
			return f"{self.sql!r} with args {self._formatargs(context)}"
		else:
			return repr(self.sql)

	def execute(self, context):
		connection = self.beginconnection(context)

		context.commandstart(str(connection), f"sql {self._formatsql(context)}")

		result = self._executesql(context, self.sql, connection)

		context.count(connection.connectstring(), self.type)

		self.endconnection(context, connection)

		if result:
			message = ", ".join(f"{argname}={argvalue!r}" for (argname, argvalue) in result.items())
		else:
			message = "done"
		context.commandend(message)

		return result


@register
class SetVarCommand(Command):
	"""
	The ``"setvar"`` command sets a variable to a fixed value. The following
	keys are supported in the command dictionary:

	``"name"``: string (required)
		The name of the variable to set.

	``"value"``: object (required)
		The value of the variable.

	Additionally the keys ``"raiseexceptions"`` and ``"comment"`` from the base
	class are supported.
	"""

	type = "setvar"

	def __init__(self, location, *, name, value, raiseexceptions=None, comment=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)
		self.name = name
		self.value = value

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} value={self.value!r} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"setvar command {self.location}"

	def execute(self, context):
		context.commandstart(f"set var {self.name!r} to {self.value!r}")

		context.keys[self.name] = self.value

		context.count(self.type)

		context.commandend("done")


@register
class UnsetVarCommand(Command):
	"""
	The ``"unsetvar"`` command deletes a variable. The key ``"name"`` must be
	given and must contain the name of the variable.

	Additionally the keys ``"raiseexceptions"`` and ``"comment"`` from the base
	class are supported.
	"""

	type = "unsetvar"

	def __init__(self, location, *, name, raiseexceptions=None, comment=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)
		self.name = name

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"unsetvar command {self.location}"

	def execute(self, context):
		context.commandstart(f"unset var {self.name!r}")

		context.keys.pop(self.name, None)

		context.count(self.type)

		context.commandend("done")


@register
class RaiseExceptionsCommand(Command):
	"""
	The ``"raiseexceptions"`` command changes the global error reporting mode
	for all subsequent commands. After::

		{"type": "raiseexceptions", "value": False}

	for all subsequent commands any exception will be reported and command
	execution will continue with the next command. ::

		{"type": "raiseexceptions", "value": True}

	will switch back to aborting the execution of the PySQL script once an
	exception is encountered.

	Note that the global configuration will only be relevant for commands that
	don't specify the ``"raiseexceptions"`` key themselves.

	Additionally the keys ``"raiseexceptions"`` and ``"comment"`` from the base
	class are supported.
	"""

	type = "raiseexceptions"

	def __init__(self, location, *, value, raiseexceptions=None, comment=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)
		self.value = bool(value)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} value={self.value!r} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"raiseexceptions command {self.location}"

	def execute(self, context):
		context.commandstart(f"raiseexceptions {self.value!r}")

		context.raiseexceptions[-1] = self.value

		context.count(self.type)

		context.commandend("done")


@register
class PushRaiseExceptionsCommand(Command):
	"""
	The ``"pushraiseexceptions"`` command changes the global error reporting mode
	for all subsequent commands, but remembers the previous exception handling
	mode. After::

		{"type": "pushraiseexceptions", "value": False}

	for all subsequent commands any exception will be ignored and command
	execution will continue with the next command. It is possible to switch back
	to the previous exception handling mode via::

		{"type": "popraiseexceptions"}

	Note that this global configuration will only be relavant for commands that
	don't specify the ``"raiseexceptions"`` key themselves.

	Additionally the keys ``"raiseexceptions"`` and ``"comment"`` from the base
	class are supported.
	"""

	type = "pushraiseexceptions"

	def __init__(self, location, *, value, raiseexceptions=None, comment=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)
		self.value = bool(value)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} value={self.value!r} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"pushraiseexceptions command {self.location}"

	def execute(self, context):
		context.commandstart(f"pushraiseexceptions {self.value!r}")

		context.raiseexceptions.append(self.value)

		context.count(self.type)

		context.commandend("done")


@register
class PopRaiseExceptionsCommand(Command):
	"""
	The ``"popraiseexceptions"`` command restores the previously active exception
	handling mode (i.e. the one active before the last ``"pushraiseexceptions"``
	command).

	The keys ``"raiseexceptions"`` and ``"comment"`` from the base class are
	supported in the command dictionary.
	"""

	type = "popraiseexceptions"

	def __init__(self, location, *, raiseexceptions=None, comment=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"popraiseexceptions command {self.location}"

	def execute(self, context):
		context.commandstart("popraiseexceptions")

		if len(context.raiseexceptions) <= 1:
			raise ValueError("raiseexception stack empty")

		context.raiseexceptions.pop()

		context.count(self.type)

		context.commandend(f"reverting to {context.raiseexceptions[-1]!r}")


@register
class CheckErrorsCommand(_DatabaseCommand):
	"""
	The ``"checkerrors"`` command checks that there are no compilation errors in
	the target schema. If there are, an exception will be raised.

	The keys ``"raiseexceptions"``, ``"comment"``, ``"connectname"``
	and ``"connectstring"`` from the base classes are supported, but the value
	of the ``"raiseexceptions"`` key will be ignored.
	"""

	type = "checkerrors"

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"checkerrors command {self.location}"

	def execute(self, context):
		connection = self.beginconnection(context)

		context.commandstart(str(connection), "check errors")

		connection.cursor.execute("select lower(type), name from user_errors group by lower(type), name")
		invalid_objects = [tuple(r) for r in connection.cursor]

		self.endconnection(context, connection)

		context.count(connection.connectstring(), self.type)

		if invalid_objects:
			raise CompilationError(invalid_objects)

		context.commandend("done")


@register
class CompileAllCommand(_DatabaseCommand):
	"""
	The ``"compileall"`` command will recompile all objects in the schema.

	The keys ``"raiseexceptions"``, ``"comment"``, ``"connectname"``
	and ``"connectstring"`` from the base classes are supported.
	"""

	type = "compileall"

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"compileall command {self.location}"

	def execute(self, context):
		connection = self.beginconnection(context)

		context.commandstart(str(connection), "compile all")

		connection.cursor.execute("begin dbms_utility.compile_schema(user); end;")

		self.endconnection(context, connection)

		context.count(connection.connectstring(), self.type)

		context.commandend("done")


@register
class SCPCommand(Command):
	"""
	The ``"scp"`` command creates a file by copying it via the ``scp`` command.
	The following keys are supported in the command dictionary:

	``"name"`` : string (required)
		The name of the file to be created. It may contain ``format()`` style
		specifications containing any key that appeared in a ``"procedure"``
		or ``"sql"`` command. These specifiers will be replaced by the correct
		key values. As these files will be copied via the ``scp`` command,
		ssh file names can be used.

	``"content"``: bytes (required)
		The content of the file to be created. This can also be a
		:class:`loadbytes` object, to load the content from an external file.

	Additionally the keys ``"raiseexceptions"`` and ``"comment"`` from the base
	class are supported.
	"""

	type = "scp"

	def __init__(self, location, *, name, content, raiseexceptions=None, comment=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)
		self.name = name
		self.content = content

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} content={self.formatload(self.content)} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"scp command {self.location}"

	def execute(self, context):
		filename = context.scpdirectory + self.name.format(**context.keys)

		context.commandstart(f"scp {filename}")

		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(self.content)
			tempname = f.name
		try:
			result = subprocess.run(["scp", "-q", tempname, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			if result.returncode:
				raise SCPError(result.returncode, (result.stdout or result.stderr).decode(errors="replace"))
		finally:
			os.remove(tempname)

		context.count(self.type)

		context.commandend(f"{_reprbytes(self.content)} written")


@register
class FileCommand(Command):
	"""
	The ``"file"`` command creates a file by directly saving it from Python.
	The following keys are supported in the command dictionary:

	``"name"`` : string (required)
		The name of the file to be created. It may contain ``format()`` style
		specifications containing any key that appeared in a ``"procedure"`` or
		``"sql"`` command. These specifiers will be replaced by the correct
		key values.

	``"content"``: bytes (required)
		The content of the file to be created. This can also be a
		:class:`loadbytes` object, to load the content from an external file.

	``"mode"``: integer (optional)
		The file mode for the new file. If the mode is specified :func:`os.chmod`
		will be called on the file.

	``"owner"``: integer or string (optional)
		The owner of the file (as a user name or a uid).

	``"group"``: integer or string (optional)
		The owning group of the file (as a group name or a gid).
		If ``owner`` or ``group`` is given, :func:`os.chown` will be called on
		the file.

	Additionally the keys ``"raiseexceptions"`` and ``"comment"`` from the base
	class are supported.
	"""

	type = "file"

	def __init__(self, location, *, name, content, raiseexceptions, comment=None, mode=None, owner=None, group=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, comment=comment)
		self.name = name
		self.content = content
		self.mode = mode
		self.owner = owner
		self.group = group

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} content={self.formatload(self.content)} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"file command {self.location}"

	def execute(self, context):
		filename = context.filedirectory + self.name.format(**context.keys)

		context.commandstart(f"file {filename}")

		try:
			with open(filename, "wb") as f:
				f.write(self.content)
		except FileNotFoundError: # probably the directory doesn't exist
			(splitpath, splitname) = os.path.split(filename)
			if splitpath:
				os.makedirs(splitpath)
				with open(filename, "wb") as f:
					f.write(self.content)
			else:
				raise # we don't have a directory to make so pass the error on

		if self.mode:
			os.chmod(filename, self.mode)
		if self.owner or self.group:
			if self.owner:
				uid = self.owner
				if isinstance(uid, str):
					uid = pwd.getpwnam(uid)[2]
			else:
				uid = -1
			if self.group:
				gid = self.group
				if isinstance(gid, str):
					gid = grp.getgrnam(gid)[2]
			else:
				gid = -1
			os.chown(filename, uid, gid)

		context.count(self.type)

		message = f"{_reprbytes(self.content)} written"
		messageoptions = []
		if self.mode:
			messageoptions.append(f"mode {self.mode:#o}")
		if self.owner:
			messageoptions.append(f"owner {self.owner!r}")
		if self.group:
			messageoptions.append(f"group {self.group!r}")
		if messageoptions:
			message = "{message} ({', '.join(messageoptions)})"
		context.commandend(message)


@register
class ResetSequenceCommand(_DatabaseCommand):
	"""
	The ``"resetsequence"`` command resets a sequence in the Oracle database to
	the maximum value of a field in a table. The following keys are supported
	in the command dictionary:

	``"sequence"``: string (required)
		The name of the sequence to reset.

	``"table"``: string (required)
		The name of the table that contains the field.

	``"field"``: string (required)
		The name of the field in the table ``table``. The sequence will be
		reset to a value, so that fetching the next value from the sequence
		will deliver a value that is larger than the maximum value of the field
		``field`` in the table ``table``.

	``"minvalue"``: integer (optional, default taken from sequence)
		The minimum value for the sequence.

	``"increment"``: integer (optional, default taken from sequence)
		The increment (i.e. the step size) for the sequence.

	Additionally the keys ``"raiseexceptions"``, ``"comment"``, ``"connectname"``
	and ``"connectstring"`` from the base classes are supported.
	"""

	type = "resetsequence"

	def __init__(self, location, *, sequence, table, field, raiseexceptions=None, comment=None, minvalue=None, increment=None, connectstring=None, connectname=None):
		super().__init__(location=location, raiseexceptions=raiseexceptions, connectstring=connectstring, connectname=connectname)
		self.sequence = sequence
		self.table = table
		self.field = field
		self.minvalue = minvalue
		self.increment = increment

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sequence={self.sequence!r} {self.location} at {id(self):#x}>"

	def __str__(self):
		return f"resetsequence command {self.location}"

	def execute(self, context):
		connection = self.beginconnection(context)

		context.commandstart(str(connection), f"resetting sequence {self.sequence} to maximum value from {self.table}.{self.field}")

		cursor = connection.cursor

		# Fetch information about the sequence
		cursor.execute("select min_value, increment_by, last_number from user_sequences where lower(sequence_name)=lower(:name)", name=self.sequence)
		oldvalues = cursor.fetchone()
		if oldvalues is None:
			raise ValueError(f"sequence {self.sequence!r} unknown")
		increment = self.increment
		if increment is None:
			increment = oldvalues[1]
		minvalue = self.minvalue
		if minvalue is None:
			minvalue = oldvalues[0]
		cursor.execute(f"select {self.sequence}.nextval from dual")
		seqvalue = cursor.fetchone()[0]

		# Fetch information about the table values
		cursor.execute(f"select nvl(max({self.field}), 0) from {self.table}")
		tabvalue = cursor.fetchone()[0]

		step = max(tabvalue, minvalue) - seqvalue
		if step:
			cursor.execute(f"alter sequence {self.sequence} increment by {step}")
			cursor.execute(f"select {self.sequence}.nextval from dual")
			seqvalue = cursor.fetchone()[0]
			cursor.execute(f"alter sequence {self.sequence} increment by {increment}")
			message = f"reset to {seqvalue}"
			result = seqvalue
		else:
			message = "no reset required"
			result = None

		context.count(connection.connectstring(), self.type)
		self.endconnection(context, connection)
		context.commandend(message)
		return result


@register
class CommentCommand(Command):
	"""
	The ``"comment"`` command does nothing.

	The keys ``"raiseexceptions"`` and ``"comment"`` from the base class are
	supported.
	"""

	type = "comment"

	def __str__(self):
		return f"comment {self.location}"

	def execute(self, context):
		context.commandstart("comment")
		context.commandend()


###
### Classes to be used by the PySQL commands
###

class var:
	"""
	:class:`var` objects are used to mark procedure values that are ``OUT``
	parameters. On first use the parameter is used as an ``OUT`` parameter and
	PySQL will remembers the OUT value under the unique key specified in the
	constructor. When a :class:`var` object is used a second time its value will
	be passed to the procedure as a normal ``IN`` parameter instead. This also
	means that it is possible to have Python expressions as parameter values that
	transform the variable value.
	"""

	def __init__(self, key=None, type=int):
		"""
		Create a :class:`var` instance. :obj:`key` is a unique name for the value.
		:obj:`type` is the type of the value (defaulting to :class:`int`).

		Note that when the :obj:`key` is :const:`None`, PySQL will *not* remember
		the value, instead each use of ``var(None)`` will create a new OUT
		parameter. This can be used for OUT parameters whose values is not
		required by subsequent commands.
		"""
		self.key = key
		self.type = type

	def __repr__(self):
		if self.type is int:
			return f"var({self.key!r})"
		else:
			return f"var({self.key!r}, {format_class(self.type)})"

	def __bool__(self):
		"""
		Variables without values are always false.
		"""
		return False


reprthreshold = 100


def _reprbytes(value):
	if len(value) > reprthreshold:
		return f"({len(value):,} bytes starting with {bytes.__repr__(value[:reprthreshold])})"
	else:
		return bytes.__repr__(value) # Because ``value`` might be an instance of a subclass of :class:`bytes`


def _reprstr(value):
	if len(value) > reprthreshold:
		return f"({len(value):,} characters starting with {str.__repr__(value[:reprthreshold])})"
	else:
		return str.__repr__(value) # Because ``value`` might be an instance of a subclass of :class:`str`


class strvalue(str):
	def __new__(cls, key, value=""):
		self = super().__new__(cls, value)
		self.key = key
		return self

	def __repr__(self):
		return f"{self.__class__.__qualname__}({self.key!r}, {_reprstr(self)})"


class bytesvalue(bytes):
	def __new__(cls, key, value=b""):
		self = super().__new__(cls, value)
		self.key = key
		return self

	def __repr__(self):
		return f"{self.__class__.__qualname__}({self.key!r}, {_reprbytes(self)})"


class intvalue(int):
	def __new__(cls, key, value=0):
		self = super().__new__(cls, value)
		self.key = key
		return self

	def __repr__(self):
		return f"{self.__class__.__qualname__}({self.key!r}, {int.__repr__(self)})"


class floatvalue(float):
	def __new__(cls, key, value=0.0):
		self = super().__new__(cls, value)
		self.key = key
		return self

	def __repr__(self):
		return f"{self.__class__.__qualname__}({self.key!r}, {float.__repr__(self)})"


def _makevalue(name, value):
	if isinstance(value, int) and not isinstance(value, bool):
		return intvalue(name, value)
	elif isinstance(value, float):
		return floatvalue(name, value)
	elif isinstance(value, str):
		return strvalue(name, value)
	elif isinstance(value, bytes):
		return bytesvalue(name, value)
	else:
		return value


class sql:
	"""
	An :class:`sql` object can be used to specify an SQL expression as a
	procedure parameter instead of a fixed value. For example passing the current
	date (i.e. the date of the import) can be done with ``sql("sysdate")``.
	"""

	def __init__(self, expression):
		self.expression = expression

	def __repr__(self):
		return f"sql({self.expression!r})"


class loadbytes:
	"""
	A :class:`loadbytes` object can be used to load a :class:`bytes` object
	from an external file.
	"""

	def __init__(self, filename):
		"""
		Create a new :class:`loadbytes` object. :obj:`filename` is the name of the
		file to be loaded. The filename is treated as being relative to the
		directory containing the pysql file that contains the PySQL command with
		the :class:`loadbytes` object.
		"""
		self.filename = filename

	def __repr__(self):
		return f"{self.__class__.__qualname__}({self.filename!r})"

	def execute(self, basefilename):
		"""
		Read the file and return the file content as a :class:`bytes` object.
		:obj:`basefilename` is the filename containing the PySQL command with the
		:class:`load` object (i.e. this determines the base directory).
		"""
		filename = os.path.join(os.path.dirname(basefilename), self.filename)
		with open(filename, "rb") as f:
			return loadedbytes(filename, f.read())


class loadstr:
	"""
	A :class:`loadstr` object can be used to load a :class:`str` object
	from an external file.
	"""

	def __init__(self, filename, encoding=None, errors="strict"):
		"""
		Create a new :class:`loadbytes` object. :obj:`filename` is the name of the
		file to be loaded. The filename is treated as being relative to the
		directory containing the pysql file that contains the PySQL command with
		the :class:`loadstr` object. :obj:`encoding` and :obj:`errors` will be
		used for the file content into a string.
		"""
		self.filename = filename
		self.encoding = encoding
		self.errors = errors

	def __repr__(self):
		result = f"{self.__class__.__qualname__}({self.filename!r}"
		if self.encoding is not None:
			result += f", encoding={self.encoding!r}"
		if self.errors is not None:
			result += f", errors={self.errors!r}"
		return result + ")"

	def execute(self, basefilename):
		"""
		Read the file and return the file content as a :class:`str` object.
		:obj:`basefilename` is the filename containing the PySQL command with the
		:class:`load` object (i.e. this determines the base directory).
		"""
		filename = os.path.join(os.path.dirname(basefilename), self.filename)
		with open(filename, "r", encoding=self.encoding, errors=self.errors) as f:
			return loadedstr(filename, f.read())


class loadedbytes(bytes):
	def __new__(cls, filename, value):
		self = super().__new__(cls, value)
		self.filename = filename
		return self

	def __repr__(self):
		return f"{self.__class__.__qualname__}({self.filename!r}, {_reprbytes(self)})"


class loadedstr(str):
	def __new__(cls, filename, value):
		self = super().__new__(cls, value)
		self.filename = filename
		return self

	def __repr__(self):
		return f"{self.__class__.__qualname__}({self.filename!r}, {_reprstr(self)})"


###
### Exception classes and location information
###

class Error(Exception):
	def __init__(self, location):
		self.location = location

	def __str__(self):
		return str(self.location)


class CompilationError(Exception):
	"""
	Exception raised by :class:`CheckErrorsCommand` when invalid database
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
	Exception raised by :class:`SCPCommand` when a call to the ``scp`` command
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
			return self.filename
		elif self.startline == self.endline:
			return f"{self.filename} :: line {self.startline:,}"
		else:
			return f"{self.filename} :: lines {self.startline:,}-{self.endline:,}"


def define(arg):
	(name, _, value) = arg.partition("=")
	(name, _, type) = name.partition(":")

	if type == "int":
		if not value:
			return intvalue(name, 0)
		try:
			return intvalue(name, int(value))
		except ValueError:
			raise argparse.ArgumentTypeError(f"{value!r} is not a legal integer value")
	elif type == "float":
		if not value:
			return floatvalue(name, 0.)
		try:
			return floatvalue(name, float(value))
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
	return strvalue(name, value)


def main(args=None):
	p = argparse.ArgumentParser(description="Import a pysql file into an Oracle database", epilog="For more info see http://python.livinglogic.de/pysql.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("file", nargs="?", help="Name of the pysql file (default: read from stdin)", type=argparse.FileType("r"), default=sys.stdin)
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", choices=("dot", "type", "full"))
	p.add_argument("-c", "--commit", dest="commit", help="When should database transactions be committed? (default %(default)s)", default="once", choices=("record", "once", "never"))
	p.add_argument("-s", "--scpdirectory", dest="scpdirectory", metavar="DIR", help="File name prefix for files to be copied via the 'scp' command (default: current directory)", default="")
	p.add_argument("-f", "--filedirectory", dest="filedirectory", metavar="DIR", help="File name prefix for files to be copied via the 'file' command (default: current directory)", default="")
	p.add_argument("-t", "--terminator", dest="terminator", metavar="STRING", help="Terminator after an SQL command (should be a valid SQL comment; default %(default)r)", default="-- @@@")
	p.add_argument("-z", "--summary", dest="summary", help="Output a summary after executing all commands", default=False, action="store_true")
	p.add_argument("-D", "--define", dest="defines", metavar="VARSPEC", help="Set variables before executing the script (can be specified multiple times). The format for VARSPEC is: 'name' or 'name=value' or 'name:type' or 'name:type=value'. Type may be 'str', 'bool', 'int' or 'float'.", default=[], action="append", type=define)

	args = p.parse_args(args)

	context = Context(
		connectstring=args.connectstring,
		scpdirectory=args.scpdirectory,
		filedirectory=args.filedirectory,
		commit=args.commit,
		terminator=args.terminator,
		verbose=args.verbose,
		summary=args.summary,
		vars=args.defines
	)
	context.executeall(args.file)


if __name__ == "__main__":
	sys.exit(main())
