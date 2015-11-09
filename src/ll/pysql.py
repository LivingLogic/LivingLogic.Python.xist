# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2012-2015 by LivingLogic AG, Bayreuth/Germany
## Copyright 2012-2015 by Walter Dörwald
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

A PySQL file may contains normal SQL commands. For the :mod:`pysql` script
to be able to execute these commands they must be terminated with a comment
line that starts with ``-- @@@``. :mod:`pysql` will strip off a trailing
``;`` or ``/`` from the command and execute it. Any exception that is raised
as a result of executing the command will stop the script and be reported.
This is in contrast to how ``sqlplus`` executes SQL command. ``sqlplus``
would continue after an error and exit with status code 0 even if there were
errors. It is also possible to explicitely ignore any exception raised by the
command by terminating the command with ``-- !!!`` (instead of ``-- @@@``).

A PySQL file that only contains SQL commands is still a valid SQL file from
the perspective of Oracle, so it still can be executed via ``sqlplus``.


PySQL commands
--------------

A pysql file may also contain PySQL commands. A PySQL command looks like a
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
		per_firstnane varchar2(200),
		per_lastnane varchar2(200)
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
		p_per_firstnane in varchar2 := null,
		p_per_lastnane in varchar2 := null
	)
	as
	begin
		if p_per_id is null then
			select person_seq.nextval into p_per_id from dual;
		end if;

		insert into person
		(
			per_id,
			per_firstnane,
			per_lastnane
		)
		values
		(
			p_per_id,
			p_per_firstnane,
			p_per_lastnane
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
			'per_id': var('per_id_max'),
			'per_firstname': 'Max',
			'per_lastname': 'Mustermann',
		}
	}

	{
		'type': 'procedure',
		'name': 'contact_insert',
		'args': {
			'per_id': var('per_id_max'),
			'con_id': var('con_id_max'),
			'con_type': 'email',
			'con_value': 'max@example.org',
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
``per_id`` in the table ``person``.


Importing a PySQL file
======================

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
		database. Possible levels are: ``0`` (no output), ``1`` (one letter for
		each command), ``2`` (like ``1``, plus a summary of which command has been
		executed how often and which procedure has been called how often), ``3``
		(detailed output for each command/procedure call, plus summary)

	``-c``, ``--commit``
		Specifies when to commit database transactions. ``record`` commits after
		every command. ``once`` (the default) at the end of the script and
		``never`` rolls back the transaction after all imports.

	``-s``, ``--scpdirectory``
		The base directory for ``scp`` file copy commands. As files are copied
		via ``scp`` this can be a remote filename (like
		``root@www.example.org:~/uploads/``) and must include a trailing ``/``.

	``-f``, ``--filedirectory``
		The base directory for the ``file`` file save commands. It must include
		a trailing ``/``.

	``-t``, ``--terminator``
		The terminator after an SQL command (should be a valid SQL comment;
		default ``-- @@@``).

	``-T``, ``--terminatorignored``
		The error ignoring terminator after an SQL command (should be a valid
		SQL comment; default ``-- !!!``).
"""

# We're importing ``datetime``, so that it's available to ``eval()``
import sys, os, os.path, pwd, grp, argparse, operator, collections, datetime, tempfile, subprocess

import cx_Oracle


__docformat__ = "reStructuredText"


class Context:
	"""
	A :class:`Context` objects contains the configuration and run time information
	required for importing a PySQL file.
	"""
	def __init__(self, db=None, scpdirectory="", filedirectory="", commit="once", terminator="-- @@@", terminatorignore="-- !!!", verbose=0):
		self.keys = {}
		self.db = db
		self.cursor = db.cursor() if db is not None else None
		self.scpdirectory = scpdirectory
		self.filedirectory = filedirectory
		self.commit = commit
		self.terminator = terminator
		self.terminatorignore = terminatorignore
		self.verbose = verbose
		self.count = 0
		self.commandcounts = collections.Counter()
		self.procedurecounts = collections.Counter()
		self.errorcount = 0

	def load(self, stream):
		"""
		Load a PySQL file from :obj:`stream`. :obj:`stream` must be an iterable
		over lines that contain the PySQL commands.

		This function is a generator. Its output are the PySQL command objects
		(i.e. instances of :class:`Command`).
		"""
		reporterrors = True
		lines = []

		def makeblock():
			# Drop empty lines at the start
			while lines and not lines[0][1].strip():
				del lines[0]
			# Drop empty lines at the end
			while lines and not lines[-1][1].strip():
				del lines[-1]
			try:
				if lines:
					location = Location(stream.name, lines[0][0], lines[-1][0])
					text = "\n".join(line[1] for line in lines).strip()
					if text:
						args = {}
						lines.clear()
						if text.startswith("{") and text.endswith("}"):
							try:
								block = eval(text)
							except Exception as exc:
								raise Error(args) from exc
							args.update(block)
							if "type" not in args:
								args["type"] = "procedure"
						elif text.endswith((";", "/")):
							args["type"] = "sql"
							args["sql"] = text[:-1]
						else:
							raise ValueError("block terminator {!r} unknown".format(text[-1:]))

						type = args.pop("type")
						command = Command.fromdict(type, location, reporterrors, args)
						if isinstance(command, IncludeCommand):
							if not command.name:
								raise MissingKeyError("include", "name")
							filename = os.path.join(os.path.dirname(command.location.filename), command.name)
							with open(filename, "r", encoding="utf-8") as f:
								yield from self.load(f)
						else:
							yield command
			except Exception as exc:
				raise Error(location) from exc

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
				elif line.startswith(self.terminator) or line.startswith(self.terminatorignore):
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
					reporterrors = True
					yield from makeblock()
					state = None
				elif line.startswith(self.terminatorignore):
					reporterrors = False
					yield from makeblock()
					state = None
				else:
					lines.append((i, line))
		yield from makeblock()

	def executeall(self, commands):
		"""
		Execute all command in :obj:`commands`, which must be an iterable of
		:class:`Command` objects.
		"""
		try:
			if self.verbose == 2:
				print("commands:", end="", flush=True)
			for command in commands:
				try:
					command.execute(self)
				except Exception as exc:
					if command.reporterrors:
						if self.verbose == 2:
							print("(error)", flush=True)
						raise Error(command) from exc
					else:
						self.errorcount += 1
						if self.verbose >= 1:
							if self.verbose >= 3:
								exctext = str(exc).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
								print(" -> ignored {}.{}: {}".format(exc.__class__.__module__, exc.__class__.__qualname__, exctext))
							elif self.verbose >= 2:
								print("(error)", end="", flush=True)
				else:
					if isinstance(command, ProcedureCommand):
						self.procedurecounts[command.name] += 1
					self.commandcounts[command.type] += 1
					self.count += 1
			if self.commit == "once":
				self.db.commit()
			elif self.commit == "never":
				self.db.rollback()
		finally:
			if self.verbose >= 3:
				print()
		self._printsummary()

	def _printsummary(self):
		if self.verbose >= 2:
			commandcountvalues = self.commandcounts.values()
			l1 = len(str(max(commandcountvalues))) if commandcountvalues else 0
			l1 = max(l1, len(str(self.errorcount)))
			l2 = max(len(procname) for procname in self.procedurecounts) if self.procedurecounts else 0
			print()
			print("Summary")
			print("=======")
			anyoutput = False
			if self.commandcounts["procedure"]:
				anyoutput = True
				print("{:>{}} type".format("#", l1))
				print("{} {}".format("-"*l1, "-"*l2))
				for (procname, count) in sorted(self.procedurecounts.items(), key=operator.itemgetter(1)):
					print("{:>{}} {}".format(count, l1, procname))
				print("{} {}".format("-"*l1, "-"*l2))
			for cmdtype in ("procedure", "sql", "resetsequence", "setvar", "file", "scp", "compileall", "checkerrors"):
				if self.commandcounts[cmdtype]:
					anyoutput = True
					print("{:>{}} ({})".format(self.commandcounts[cmdtype], l1, cmdtype))
			if self.errorcount:
				print("{:>{}} error{} ignored".format(self.errorcount, l1, "s" if self.errorcount != 1 else ""))
			if not anyoutput:
				print("no commands executed")


###
### Command classes
###

class Command:
	"""
	The base class of all commands. A :class:`Command` object is created from
	a command dictionary literal in a PySQL file. The keys in the command
	dictorionary that are supported by all command types are the following:

		``type`` : string (optional)
			This is either ``"procedure"`` (the default), ``"sql"``, ``"file"``,
			``"scp"``, ``"resetsequence"``, ``"setvar"``, ``"include"``,
			``"compileall"`` or ``"checkerrors"`` and specifies the type of the
			PySQL command.

		``reporterrors`` : bool (optional)
			Specifies whether exceptions that happen during the execution of the
			command should be reported and terminate the script (``True``,
			the default), or should be ignored (``False``).
	"""
	def __init__(self, location, reporterrors):
		self.location = location
		self.reporterrors = reporterrors

	commands = {}

	@classmethod
	def fromdict(cls, type, location, reporterrors, d):
		if type in cls.commands:
			return cls.commands[type](location, reporterrors, **d)
		raise ValueError("command type {!r} unknown".format(type))

	def __str__(self):
		return "{} command {}".format(self.type, self.location)

	def executeload(self, value):
		if isinstance(value, load):
			value = value.execute(self.location.filename)
		return value

	def formatload(self, value):
		if isinstance(value, str):
			return "({:,} chars)".format(len(value))
		elif isinstance(value, bytes):
			return "({:,} bytes)".format(len(value))
		else:
			return repr(value)


def register(cls):
	Command.commands[cls.type] = cls
	return cls


@register
class IncludeCommand(Command):
	"""
	The ``"include"`` command includes another PySQL file. The filename is read
	from the key ``"name"``. This name is interpreted as being relative to the
	directory with the file containing the ``include`` command.
	"""
	type = "include"

	def __init__(self, location, reporterrors, name):
		super().__init__(location=location, reporterrors=reporterrors)
		self.name = name

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} {0.location} at {1:#x}>".format(self, id(self))

	def __str__(self):
		return "incluce command {}".format(self.location)


class _SQLCommand(Command):
	"""
	Common base class of :class:`ProcedureCommand` and :class:`SQLCommand`.
	"""
	def _executesql(self, context, query):
		queryargvars = {}
		for (argname, argvalue) in self.args.items():
			if isinstance(argvalue, var):
				if argvalue.key is None:
					queryargvars[argname] = None
				elif argvalue.key in context.keys:
					queryargvars[argname] = context.keys[argvalue.key]
				else:
					queryargvars[argname] = context.cursor.var(argvalue.type)
			elif isinstance(argvalue, sql):
				pass # no value
			elif isinstance(argvalue, load):
				queryargvars[argname] = self.executeload(argvalue)
			elif isinstance(argvalue, str) and len(argvalue) >= 4000:
				var_ = context.cursor.var(cx_Oracle.CLOB)
				var_.setvalue(0, argvalue)
				queryargvars[argname] = var_
			else:
				queryargvars[argname] = argvalue

		context.cursor.execute(query, queryargvars)

		newkeys = {}
		for (argname, argvalue) in self.args.items():
			if isinstance(argvalue, var) and argvalue.key is not None and argvalue.key not in context.keys:
				newkeys[argname] = context.keys[argvalue.key] = queryargvars[argname].getvalue(0)
		return newkeys

	def _formatargs(self, context):
		args = []
		if self.args:
			for (argname, argvalue) in self.args.items():
				if isinstance(argvalue, var) and argvalue.key in context.keys:
					arg = "{}={!r}={!r}".format(argname, argvalue, context.keys[argvalue.key])
				else:
					arg = "{}={!r}".format(argname, argvalue)
				args.append(arg)
		return ", ".join(args)


@register
class ProcedureCommand(_SQLCommand):
	"""
	A ``"procedure"`` command calls an Oracle procedure in the database.
	In addition to ``"type"`` and ``"reporterrors"`` the following keys are
	supported in the command dictionary:

		``name`` : string (required)
			The name of the procedure to be called (This may include ``.`` for
			calling a procedure in a package or one owned by a different user).

		``args`` : dictionary (optional)
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

			*	Finally :class:`load` objects can be used to load values from
				external files (as long as they are of type :class:`str` or
				:class:`bytes`). ``load("foo/bar.txt")`` will be replaced with the
				content of the external file ``foo/bar.txt`` (as a :class:`bytes`
				object). If a :class:`str` object is required, the encoding and
				error handler name can be passed to :class:`load` like this::

					load("foo/bar.txt", "utf-8", "replace")
	"""

	type = "procedure"

	def __init__(self, location, reporterrors, name, args=None):
		super().__init__(location=location, reporterrors=reporterrors)
		self.name = name
		self.args = args or {}

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} args={0.args!r} {0.location} at {1:#x}>".format(self, id(self))

	def __str__(self):
		return "procedure command {}".format(self.location)

	def _formatprocedurecall(self, context):
		return "{}({})".format(self.name, self._formatargs(context))

	def execute(self, context):
		if context.verbose >= 1:
			if context.verbose >= 3:
				print("#{:,} {}: procedure {}".format(context.count+1, self.location, self._formatprocedurecall(context)), end="", flush=True)
			else:
				print(" " + self.type, end="", flush=True)

		queryargvalues = {}
		for (argname, argvalue) in self.args.items():
			if isinstance(argvalue, var):
				queryargvalues[argname] = ":{}".format(argname)
			elif isinstance(argvalue, sql):
				queryargvalues[argname] = argvalue.expression
				# no value
			elif isinstance(argvalue, str) and len(argvalue) >= 4000:
				queryargvalues[argname] = ":{}".format(argname)
			else:
				queryargvalues[argname] = ":{}".format(argname)

		query = "begin {}({}); end;".format(self.name, ", ".join("{}=>{}".format(*argitem) for argitem in queryargvalues.items()))
		result = self._executesql(context, query)

		if context.commit == "record":
			context.db.commit()

		if context.verbose >= 3:
			if result:
				print(" -> {}".format(", ".join("{}={!r}".format(argname, argvalue) for (argname, argvalue) in result.items())), flush=True)
			else:
				print(flush=True)
		return result


@register
class SQLCommand(_SQLCommand):
	"""
	An ``"sql"`` command directly executes an SQL statement in the Oracle database.
	In addition to ``"type"`` and ``"reporterrors"`` the following keys are
	supported in the command dictionary:

		``sql`` : string (required)
			The SQL to be executed. This may contain parameters in the form of
			``:paramname``. The values for those parameters will be taken from
			``args``.

		``args`` : dictionary (optional)
			A dictionary with the names of the parameters as keys and the parameter
			values as values. Similar to procedure calls :class:`var` and
			:class:`load` objects are supported. However :class:`sql` objects
			are not supported (they will be ignored).


	"""
	type = "sql"

	def __init__(self, location, reporterrors, sql, args=None):
		super().__init__(location=location, reporterrors=reporterrors)
		self.sql = sql
		self.args = args or {}

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} sql={0.sql!r} args={0.args!r} {0.location} at {1:#x}>".format(self, id(self))

	def __str__(self):
		return "sql command {}".format(self.location)

	def _formatsql(self, context):
		if self.args:
			return "{!r} with args {}".format(self.sql, self._formatargs(context))
		else:
			return repr(self.sql)

	def execute(self, context):
		if context.verbose >= 1:
			if context.verbose >= 3:
				print("#{:,} {}: sql {}".format(context.count+1, self.location, self._formatsql(context)), end="", flush=True)
			else:
				print(" " + self.type, end="", flush=True)

		result = self._executesql(context, self.sql)

		if context.commit == "record":
			context.db.commit()

		if context.verbose >= 3:
			if result:
				print(" -> {}".format(", ".join("{}={!r}".format(argname, argvalue) for (argname, argvalue) in result.items())), flush=True)
			else:
				print(flush=True)

		return result


@register
class SetVarCommand(Command):
	"""
	The ``"setvar"`` command sets a variable to a fixed value. In addition to
	``"type"`` and ``"reporterrors"`` the following keys are supported in the
	command dictionary:

		``var``: string (required)
			The name of the variable to set.

		``value``: (required)
			The value of the variable.
	"""
	type = "setvar"

	def __init__(self, location, reporterrors, var, value):
		super().__init__(location=location, reporterrors=reporterrors)
		self.var = var
		self.value = value

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} var={0.var!r} value={0.value!r} {0.location} at {1:#x}>".format(self, id(self))

	def __str__(self):
		return "setvar command {}".format(self.location)

	def execute(self, context):
		if context.verbose >= 1:
			if context.verbose >= 3:
				print("#{:,} {}: set var {!r} to {!r}".format(context.count+1, self.location, self.var, self.value), end="", flush=True)
			else:
				print(" " + self.type, end="", flush=True)

		context.keys[self.var] = self.value

		if context.verbose >= 3:
			print(" -> done", flush=True)


@register
class CheckErrorsCommand(Command):
	"""
	The ``"checkerrors"`` command checks that there are no compilation errors in
	the target schema. If there are, an exception will be raised. (The
	``reporterrors`` key is supported, but its value will be ignored).
	"""
	type = "checkerrors"

	def __init__(self, location, reporterrors):
		super().__init__(location=location, reporterrors=reporterrors)

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {0.location} at {1:#x}>".format(self, id(self))

	def __str__(self):
		return "checkerrors command {}".format(self.location)

	def execute(self, context):
		if context.verbose >= 1:
			if context.verbose >= 3:
				print("#{:,} {}: check errors".format(context.count+1, self.location), end="", flush=True)
			else:
				print(" " + self.type, end="", flush=True)

		context.cursor.execute("select lower(type), name from user_errors group by lower(type), name")
		invalid_objects = [tuple(r) for r in context.cursor]

		if invalid_objects:
			raise CompilationError(invalid_objects)

		if context.verbose >= 3:
			print(" -> done", flush=True)


@register
class CompileAllCommand(Command):
	"""
	The ``"compileall"`` command will recompile all objects in the schema.
	"""
	type = "compileall"

	def __init__(self, location, reporterrors):
		super().__init__(location=location, reporterrors=reporterrors)

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {0.location} at {1:#x}>".format(self, id(self))

	def __str__(self):
		return "compileall command {}".format(self.location)

	def execute(self, context):
		if context.verbose >= 1:
			if context.verbose >= 3:
				print("#{:,} {}: compile all".format(context.count+1, self.location), end="", flush=True)
			else:
				print(" " + self.type, end="", flush=True)

		context.cursor.execute("begin dbms_utility.compile_schema(user); end;")

		if context.verbose >= 3:
			print(" -> done", flush=True)


@register
class SCPCommand(Command):
	"""
	The ``"scp"`` command creates a file by copying it via the ``scp`` command.
	In addition to ``"type"`` and ``"reporterrors"`` the following keys are
	supported in the command dictionary:

		``name`` : string (required)
			The name of the file to be created. It may contain ``format()`` style
			specifications containing any key that appeared in a ``"procedure"``
			or ``"sql"`` command. These specifiers will be replaced by the correct
			key values. As these files will be copied via the ``scp`` command,
			ssh file names can be used.

		``content``: bytes (required)
			The content of the file to be created. This can also be a
			:class:`load` object, to load the content from an external file.
	"""
	type = "scp"

	def __init__(self, location, reporterrors, name, content):
		super().__init__(location=location, reporterrors=reporterrors)
		self.name = name
		self.content = content

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} content={1} {0.location} at {2:#x}>".format(self, self.formatload(self.content), id(self))

	def __str__(self):
		return "scp command {}".format(self.location)

	def execute(self, context):
		filename = context.scpdirectory + self.name.format(**context.keys)

		if context.verbose >= 1:
			if context.verbose >= 3:
				print("#{:,} {}: scp {}".format(context.count+1, self.location, filename), end="", flush=True)
			else:
				print(" " + self.type, end="", flush=True)

		content = self.executeload(self.content)
		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(content)
			tempname = f.name
		try:
			result = subprocess.run(["scp", "-q", tempname, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			if result.returncode:
				raise SCPError(result.returncode, (result.stdout or result.stderr).decode(errors="replace"))
		finally:
			os.remove(tempname)

		if context.verbose >= 3:
			print(" -> {} bytes written".format(len(self.content)), flush=True)


@register
class FileCommand(Command):
	"""
	The ``"file"`` command creates a file by directly saving it from Python.
	In addition to ``"type"`` and ``"reporterrors"`` the following keys are
	supported in the command dictionary:

		``name`` : string (required)
			The name of the file to be created. It may contain ``format()`` style
			specifications containing any key that appeared in a ``"procedure"`` or
			``"sql"`` command. These specifiers will be replaced by the correct
			key values.

		``content``: bytes (required)
			The content of the file to be created. This can also be a
			:class:`load` object, to load the content from an external file.

		``mode``: integer (optional)
			The file mode for the new file. If the mode is specified :func:`os.chmod`
			will be called on the file.

		``owner``: integer or string (optional)
			The owner of the file (as a user name or a uid).

		``group``: integer or string (optional)
			The owning group of the file (as a group name or a gid).
			If ``owner`` or ``group`` is given, :func:`os.chown` will be called on
			the file.
	"""
	type = "file"

	def __init__(self, location, reporterrors, name, content, mode=None, owner=None, group=None):
		super().__init__(location=location, reporterrors=reporterrors)
		self.name = name
		self.content = content
		self.mode = mode
		self.owner = owner
		self.group = group

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} content={1} {0.location} at {2:#x}>".format(self, self.formatload(self.content), id(self))

	def __str__(self):
		return "file command {}".format(self.location)

	def execute(self, context):
		filename = context.filedirectory + self.name.format(**context.keys)

		if context.verbose >= 1:
			if context.verbose >= 3:
				print("#{:,} {}: file {}".format(context.count+1, self.location, filename), end="", flush=True)
			else:
				print(" " + self.type, end="", flush=True)

		content = self.executeload(self.content)

		try:
			with open(filename, "wb") as f:
				f.write(content)
		except FileNotFoundError: # probably the directory doesn't exist
			(splitpath, splitname) = os.path.split(filename)
			if splitpath:
				os.makedirs(splitpath)
				with open(filename, "wb") as f:
					f.write(content)
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

		if context.verbose >= 3:
			msg = " -> {:,} bytes written".format(len(content))
			optionmsg = []
			if self.mode:
				optionmsg.append("mode {:#o}".format(self.mode))
			if self.owner:
				optionmsg.append("owner {!r}".format(self.owner))
			if self.group:
				optionmsg.append("group {!r}".format(self.group))
			if optionmsg:
				msg = "{} ({})".format(msg, ", ".join(optionmsg))
			print(msg, flush=True)


@register
class ResetSequenceCommand(Command):
	"""
	The ``"resetsequence"`` command resets a sequence in the Oracle database to the
	maximum value of a field in a table. In addition to ``"type"`` and
	``"reporterrors`` the following keys are supported in the command dictionary:

		``sequence``: string (required)
			The name of the sequence to reset.

		``table``: string (required)
			The name of the table that contains the field.

		``field``: string (required)
			The name of the field in the table ``table``. The sequence will be
			reset to a value, so that fetching the next value from the sequence
			will deliver a value that is larger than the maximum value of the field
			``field`` in the table ``table``.

		``minvalue``: integer (optional, default taken from sequence)
			The minimum value for the sequence.

		``increment``: integer (optional, default taken from sequence)
			The increment (i.e. the stop size) for the sequence.
	"""
	type = "resetsequence"

	def __init__(self, location, reporterrors, sequence, table, field, minvalue=None, increment=None):
		super().__init__(location=location, reporterrors=reporterrors)
		self.sequence = sequence
		self.table = table
		self.field = field
		self.minvalue = minvalue
		self.increment = increment

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} sequence={0.sequence!r} {0.location} at {1:#x}>".format(self, id(self))

	def __str__(self):
		return "resetsequence command {}".format(self.location)

	def execute(self, context):
		if context.verbose >= 1:
			if context.verbose >= 3:
				print("#{:,} {}: resetting sequence {} to maximum value from {}.{}".format(context.count+1, self.location, self.sequence, self.table, self.field), end="", flush=True)
			else:
				print(" " + self.type, end="", flush=True)

		# Fetch information about the sequence
		context.cursor.execute("select min_value, increment_by, last_number from user_sequences where lower(sequence_name)=lower(:name)", name=self.sequence)
		oldvalues = context.cursor.fetchone()
		if oldvalues is None:
			raise ValueError("sequence {!r} unknown".format(self.sequence))
		increment = self.increment
		if increment is None:
			increment = oldvalues[1]
		minvalue = self.minvalue
		if minvalue is None:
			minvalue = oldvalues[0]
		context.cursor.execute("select {}.nextval from dual".format(self.sequence))
		seqvalue = context.cursor.fetchone()[0]

		# Fetch information about the table values
		context.cursor.execute("select nvl(max({}), 0) from {}".format(self.field, self.table))
		tabvalue = context.cursor.fetchone()[0]

		step = max(tabvalue, minvalue) - seqvalue
		if step:
			context.cursor.execute("alter sequence {} increment by {}".format(self.sequence, step))
			context.cursor.execute("select {}.nextval from dual".format(self.sequence))
			seqvalue = context.cursor.fetchone()[0]
			context.cursor.execute("alter sequence {} increment by {}".format(self.sequence, increment))
			if context.verbose >= 3:
				print(" -> reset to {}".format(seqvalue), flush=True)
			return seqvalue
		else:
			if context.verbose >= 3:
				print(" -> no reset required", flush=True)
			return None


###
### Classes to be used by the PySQL commands
###

class var:
	"""
	:class:`var` instances are used to mark procedure values that are ``OUT``
	parameters. On first use the parameter is used as an ``OUT`` parameter and
	PySQL will remembers the OUT value under the unique key specified in the
	constructor. When a :class:`var` object is used a second time its value will
	be passed to the procedure as a normal ``IN`` parameter.
	"""

	def __init__(self, key, type=int):
		"""
		Create a :class:`var` instance. :obj:`key` is a unique name for the value.
		:obj:`type` is the type of the value (defaulting to :class:`int`).
		"""
		self.key = key
		self.type = type

	def __repr__(self):
		if self.type is int:
			fmt = "var({0.key!r})"
		elif self.type.__module__ == "builtins":
			fmt = "var({0.key!r}, {0.type.__qualname__})"
		else:
			fmt = "var({0.key!r}, {0.type.__module__}.{0.type.__qualname__})"
		return fmt.format(self)


class sql:
	"""
	An :class:`sql` object can be used to specify an SQL expression as a
	procedure parameter instead of a fixed value. For example passing the current
	date (i.e. the date of the import) can be done with ``sql("sysdate")``.
	"""

	def __init__(self, expression):
		self.expression = expression

	def __repr__(self):
		return "sql({!r})".format(self.expression)


class load:
	"""
	A :class:`load` object can be used to load a :class:`str` or :class:`bytes`
	object from an external file.
	"""

	def __init__(self, filename, encoding=None, errors=None):
		"""
		Create a new :class:`load` object. :obj:`filename` is the name of the file
		to be loaded. The filename is treated as being relative to the directory
		containing the pysql file that contains the PySQL command with the
		:class:`load` object. If :obj:`encoding` is ``None`` the content of the
		file will be returned as a :class:`bytes` object, otherwise :obj:`encoding`
		and :obj:`errors` will be used for decoding the file content into a string.
		"""
		self.filename = filename
		self.encoding = encoding
		self.errors = errors

	def __repr__(self):
		fmt = "load({0.filename!r}"
		if self.encoding is not None:
			fmt += ", encoding={0.encoding!r}"
		if self.errors is not None:
			fmt += ", errors={0.errors!r}"
		fmt += ")"
		return fmt.format(self)

	def execute(self, basefilename):
		"""
		Read the file and return the file content as a :class:`bytes` or
		:class:`str` object. :obj:`basefilename` is the filename containing the
		PySQL command with the :class:`load` object (i.e. this determines the
		base directory).
		"""
		filename = os.path.join(os.path.dirname(basefilename), self.filename)
		if self.encoding is None: # load bytes
			with open(filename, "rb") as f:
				return f.read()
		else: # load string
			with open(filename, "r", encoding=self.encoding, errors=self.errors) as f:
				return f.read()


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
			return "one invalid db object: {} {}".format(*self.objects[0])
		else:
			return "{:,} invalid db objects: {}".format(len(self.objects), ", ".join("{} {}".format(*object) for object in self.objects))


class SCPError(Exception):
	"""
	Exception raised by :class:`SCPCommand` when a call to the ``scp`` comamnd
	fails.
	"""
	def __init__(self, status, msg):
		self.status = status
		self.msg = msg

	def __str__(self):
		return "scp failed with code {}: {}".format(self.status, self.msg)


class Location:
	"""
	The location of a PySQL/SQL command in a pysql file.
	"""
	def __init__(self, filename, startline, endline):
		self.filename = filename
		self.startline = startline
		self.endline = endline

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} filename={0.filename!r} startline={0.startline!r} endline={0.endline!r} at {1:#x}>".format(self, id(self))

	def __str__(self):
		if self.startline is None and self.endline is None:
			return "in {!r}".format(self.filename)
		elif self.startline == self.endline:
			return "in {!r} at line {:,}".format(self.filename, self.startline)
		else:
			return "in {!r} at lines {:,}-{:,}".format(self.filename, self.startline, self.endline)


def main(args=None):
	p = argparse.ArgumentParser(description="Import a pysql file into an Oracle database", epilog="For more info see http://www.livinglogic.de/Python/pysql/index.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("file", nargs="?", help="Name of the pysql file (default: read from stdin)", type=argparse.FileType("r"), default=sys.stdin)
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", type=int, default=2, choices=(0, 1, 2, 3))
	p.add_argument("-c", "--commit", dest="commit", help="When should database transactions be committed? (default %(default)s)", default="once", choices=("record", "once", "never"))
	p.add_argument("-s", "--scpdirectory", dest="scpdirectory", metavar="DIR", help="File name prefix for files to be copied via the 'scp' command (default: current directory)", default="")
	p.add_argument("-f", "--filedirectory", dest="filedirectory", metavar="DIR", help="File name prefix for files to be copied via the 'file' command (default: current directory)", default="")
	p.add_argument("-t", "--terminator", dest="terminator", metavar="STRING", help="Terminator after an SQL command (should be a valid SQL comment; default %(default)r)", default="-- @@@")
	p.add_argument("-T", "--terminatorignore", dest="terminatorignore", metavar="STRING", help="Terminator after an SQL command that ignores errors (should be a valid SQL comment; default %(default)r)", default="-- !!!")

	args = p.parse_args(args)

	context = Context(
		db=cx_Oracle.connect(args.connectstring),
		scpdirectory=args.scpdirectory,
		filedirectory=args.filedirectory,
		commit=args.commit,
		terminator=args.terminator,
		terminatorignore=args.terminatorignore,
		verbose=args.verbose,
	)
	context.executeall(context.load(args.file))


if __name__ == "__main__":
	sys.exit(main())
