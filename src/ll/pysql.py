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
database. It reads ``pysql`` files which are an extension of normal Oracle SQL
files.

A PySQL file can contain different types of commands.


SQL commands
------------

A PySQL file may contain normal SQL commands. For the :mod:`!pysql` script
to be able to execute these commands they must be terminated with a comment
line ``-- @@@``. :mod:`pysql` will strip off a trailing ``;`` or ``/`` from
the command and execute it. Any exception that is raised as a result of
executing the command will stop the script and be reported. This is in
contrast to how ``sqlplus`` executes SQL commands. ``sqlplus`` would continue
after an error and exit with status code 0 even if there were errors.
(It is also possible to explicitely ignore any exception raised by the
command by specifying a different exception handling mode.)

A PySQL file that only contains SQL commands is still a valid SQL file from
the perspective of Oracle, so it still can be executed via ``sqlplus``.


Literal Python blocks
---------------------

A literal Python block starts with a line that only contains ``#>>>`` and
ends with a line that only contains ``#<<<``. Python code within the block
gets executed when the block is encountered. The following objects are available
within the block as global variables:

:class:`sqlexpr`
	Can be used to specify that an argument for a :class:`procedure` should be
	an SQL expression instead of a Python value or a :class:`var` object;

:mod:`datetime`
	Python's datetime module;

:obj:`connection`
	The active database connection (or :const:`None` if there is no active
	database connection).

Furthermore all PySQL commands (see below) are available.

Variables that get set within a literal Python block will be available (and
retain their value) in subsequent literal Python blocks or other PySQL commands.


PySQL commands
--------------

A PySQL file may also contain PySQL commands. A PySQL command looks and behaves
like a Python function call. This function call must either be contained in a
single line (i.e. start with ``name(`` and end with ``)`` or it must start with
a line that only contains ``name(`` and end at a line that only contains ``)``.
(``name`` must be the name of a PySQL command).

The following commands are available:

:class:`include`
	Includes another PySQL file;

:class:`connect`
	Connects to a database;

:class:`disconnect`
	Disconnects from the active database connection;

:class:`procedure`
	Call a procedure in the database (and handles OUT parameter via :class:`var`
	objects);

:class:`sql`
	Executes an SQL statement in the database (and handles OUT parameter via
	:class:`var` objects);

:class:`literalsql`
	Executes an SQL statement in the database (this is what SQL commands get
	converted to);

:class:`commit`
	Commits the transaction in the active database connection;

:class:`rollback`
	Rolls back the transaction in the active database connection;

:class:`literalpy`
	Executes Python code (this is what literal Python blocks get converted to);

:class:`setvar`
	Sets a variable;

:class:`unsetvar`
	Deletes a variable;

:class:`raiseexceptions`
	Set the exception handling mode;

:class:`pushraiseexceptions`
	Temporarily modifies the exception handling mode;

:class:`popraiseexceptions`
	Reverts to the previously active exception handling mode;

:class:`checkerrors`
	Checks whether there are invalid database objects;

:class:`scp`
	Creates a file on a remote host via :program:`scp`;

:class:`file`
	Creates a file on the local machine;

:class:`resetsequence`
	Resets a database sequence to the maximum value of a field in a table;

:class:`user_exists`
	Tests whether a database user exists;

:class:`object_exists`
	Tests whether a database object (table, package, procedure, etc.) exists;

:class:`drop_types`
	Drops all database objects of a certain type;

:class:`comment`
	A comment

:class:`loadbytes`
	Loads the binary content of a file;

:class:`loadstr`
	Loads the text content of a file;

:class:`var`
	Marks an argument for a :class:`procedure` or :class:`sql` command as being
	an OUT parameter (or passes the value of the variable in subsequent
	:class:`procedure`/:class:`sql` commands);

:class:`env`
	Returns the value of an environment variable.


Comments
--------

A line starting with '#' (outside of a SQL command or literal Python block) is
considered a comment and will be ignored.


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

	-- @@@

	create table person
	(
		per_id integer not null,
		per_firstname varchar2(200),
		per_lastname varchar2(200)
	);

	-- @@@

	alter table person add constraint person_pk primary key(per_id);

	-- @@@

	create table contact
	(
		con_id integer not null,
		per_id integer not null,
		con_type varchar2(200),
		con_value varchar2(200)
	);

	-- @@@

	alter table contact add constraint contact_pk primary key(con_id);

	-- @@@

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

	-- @@@

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

	python -m ll.pysql data.pysql -d user/pwd@database

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
opened with the ``connect`` command. This command opens a new database
connection. Subsequent commands that talk to the database will use this
connection until a ``disconnect`` command disconnects from the database and
reverts to the previous connection (which might not exist). An example looks
like this::

	connect("user/pwd@db")

	procedure("test")

	disconnect()


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
inside a PySQL command.


External files
==============

Inside a PySQL command it is possible to load values from external files.
The :class:`loadbytes` command loads a :class:`bytes` object from an external
file like this::

	loadbytes("path/to/file.png")

A string can be loaded with the :class:`loadstr` command like this::

	loadstr("path/to/file.txt", encoding="utf-8", errors="replace")

The second and third argument are the encoding and error handling name
respectively.

The filename is treated as being relative to the file containing the
:class:`loadbytes` or :class:`loadstr` call.

This file content can then be used in other PySQL commands (e.g. as parameters
in :class:`procedure` commands, or as file content in :class:`scp` or
:class:`file` commands).


Command line usage
==================

``pysql.py`` has no external dependencies except for :mod:`cx_Oracle` and can
be used as a script for importing a PySQL file into the database (However some
commands require :mod:`ll.orasql`). As a script it supports the following
command line options:

	``file``
		The name of one or more PySQL files that will be read and imported.
		If no filename is given, commands are read from ``stdin``.

	``-v``, ``--verbose``
		Gives different levels of output while data is being imported to the
		database. The default is no output (unless an exception occurs). Possible
		modes are: ``dot`` (one dot for each command), ``type`` (each command type),
		``file`` (the file names and line numbers from which code gets executed),
		``log`` (the log messages output by the commands) or ``full``
		(source code that will be executed and the log messages output by the
		commands)

	``-d``, ``--database``
		The value is an Oracle connectstring to specify the initial database
		connection that will be used before any additional :class:`connect`
		commands.

	``-z``, ``--summary``
		Give a summary of the number of commands executed and procedures called.

	``-r``, ``--rollback``
		Specifies that transactions should be rolled back at the end of the script
		run, or when a :class:`disconnect` command disconnects from the database.
		The default is to commit at the end or on each disconnect. (But note that
		DDL in the script will still commit everything up to the DDL statement.)

	``-s``, ``--scpdirectory``
		The base directory for :class:`scp` file copy commands. As files are
		copied via :program:`scp` this can be a remote filename (like
		``root@www.example.org:~/uploads/``) and must include a trailing ``/``.

	``-f``, ``--filedirectory``
		The base directory for :class:`file` file save commands. It must include
		a trailing ``/``.

	``--tabsize``
		The tab size when PySQL source is printed in ``full`` mode.

	``--context``
		The number of lines at the start and end of the source code of a block to
		print in ``full`` mode. The default is to print the complete source code.

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

# We're importing :mod:`datetime` to make it available to :func:`eval` and :func:`exec`
import sys, os, os.path, argparse, collections, time, datetime, pathlib, tempfile, subprocess, contextlib

try:
	import pwd
except ImportError:
	pwd = None

try:
	import grp
except ImportError:
	grp = None

import cx_Oracle

try:
	from ll import orasql
except ImportError:
	orasql = None

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
	elif isinstance(value, str) and len(value) > reprthreshold:
		return f"<{str.__repr__(value[:reprthreshold])} ... ({len(value):,} characters)>"
	else:
		return repr(value)


def connectstring(connection):
	if connection is None:
		return ""
	else:
		return f"{connection.username}@{connection.tnsentry}"


###
### Command classes
###

class Command:
	"""
	The base class of all commands. A :class:`Command` object is created from a
	function call in a PySQL file and then immediatetel the method
	:meth:`execute` will be called to execute the command.

	The only parameter in the call that is supported by all commands is the
	following:

	``raiseexceptions`` : bool (optional)
		Specifies whether exceptions that happen during the execution of the
		command should be reported and terminate the script (``True``), or
		should be ignored (``False``). ``None`` uses the global configuration.
	"""

	def __init__(self, *, raiseexceptions=None):
		self.location = None
		self.raiseexceptions = raiseexceptions
		self._context = None
		self._startime = None
		self._stoptime = None
		self._nr = None
		self._message = None # Final message of the command
		self._counter = () # Additional keys for counting

	commands = {} # Maps command names to command classes.

	def __str__(self):
		if self.location is None:
			return f"{self.__class__.__name__} command"
		else:
			return f"{self.__class__.__name__} command in {self.location}"

	def strlocation(self, context):
		result = context.strfilename(self.location.filename)
		if self.location.startline is None and self.location.endline is None:
			result += f" :: {self._lines()}"
		return result

	def finish(self, message):
		self._message = message

	def count(self, *keys):
		self._counter = keys

	def log(self, *objects):
		self._context.log(self, *objects)

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
	"""
	Register a :class:`Command` subclass as a PySQL command.

	This is used as a class decorator.
	"""
	Command.commands[cls.__name__] = cls
	return cls


@register
class include(Command):
	"""
	The :class:`!include` command includes another PySQL file. The filename is
	passed in the first parameter ``filename``. This filename is interpreted as
	being relative to the directory with the file containing the
	:class:`!include` command.

	The parameter ``cond`` specifies whether this :class:`!include` command
	should be executed or not. If ``cond`` is ``None`` or true, the
	:class:`!include` command will be executed, else it won't.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, filename, *, cond=None, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.filename = filename
		self.cond = cond

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} filename={self.filename!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		filename = self.filename

		if self.cond is None or self.cond:
			self.log(f"Including file {context.strfilename(filename)!r}")
			with context.changed_filename(filename) as fn:
				with fn.open("r", encoding="utf-8") as f:
					context._load(f)
			self.finish(f"Included file {context.strfilename(filename)!r}")
		else:
			self.finish(f"Skipped file {context.strfilename(filename)!r}")

	def source_format(self):
		yield from self._source_format(self.filename, raiseexceptions=self.raiseexceptions)


@register
class connect(Command):
	"""
	The :class:`!connect` command connects to the database given in the
	connectstring in the parameter ``connectstring``. After the :class:`!connect`
	command until the matching :class:`disconnect` command, all commands that
	talk to the database will use this connection. After a :class:`disconnect`
	command :mod:`!pysql` will revert back to the previously active database
	connection. Parameter have the following meaning:

	``mode`` : string or :const:`None` (optional)
		The connection mode: This can be either ``'sysdba'`` or :const:`None`.

	``retry`` : int (optional)
		The number of times PySQL tries to get a database connection.

	``retrydelay`` : int (optional)
		The number of seconds to wait between connection tries.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, connectstring, *, mode=None, retry=None, retrydelay=None, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.connectstring = connectstring
		self.mode = mode
		self.retry = retry
		self.retrydelay = retrydelay

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} connectstring={self.connectstring!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		retry = self.retry if self.retry is not None else 1
		retrydelay = self.retrydelay if self.retrydelay is not None else 10

		for i in range(retry):
			if i == retry-1:
				connection = context.connect(self.connectstring, mode=self.mode)
			else:
				try:
					connection = context.connect(self.connectstring, mode=self.mode)
				except cx_Oracle.DatabaseError as exc:
					if self.mode is not None:
						self.log(f"Connection #{i+1:,} to {self.connectstring!r} as {self.mode} failed:")
					else:
						self.log(f"Connection #{i+1:,} to {self.connectstring!r} failed:")
					exctext = str(exc).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
					self.log(f"{format_class(exc.__class__)}: {exctext}")
					if retrydelay > 0:
						self.log(f"Retrying after {retrydelay!r} seconds")
						time.sleep(retrydelay)
					else:
						self.log(f"Retrying immediately")
				else:
					break

		if self.mode is not None:
			self.finish(f"Connected to {self.connectstring!r} as {self.mode}")
		else:
			self.finish(f"Connected to {self.connectstring!r}")

		return connection

	def source_format(self):
		yield from self._source_format(
			connectstring=self.connectstring,
			mode=self.mode,
			retry=self.retry,
			retrydelay=self.retrydelay,
			raiseexceptions=self.raiseexceptions,
		)


@register
class disconnect(Command):
	"""
	The :class:`!disconnect` command disconnects from the active database
	connection and reverts back to the previously active database connection.

	``commit`` specifies whether the transaction should be committed. If
	``commit`` is :const:`None`, the default commit mode is used (which can be
	changed on the command line via the ``-r``/``--rollback`` option).

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, *, commit=None, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.commit = commit

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} commit={self.commit!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		if not context.connections:
			raise ValueError(f"no connection available")

		commit = self.commit if self.commit is not None else context.commit
		connection = context.connections[-1]
		context.disconnect(commit)
		if commit:
			self.finish(f"Disconnected from {connectstring(connection)!r} (transaction committed)")
		else:
			self.finish(f"Disconnected from {connectstring(connection)!r} (transaction rolled back)")

		return connection

	def source_format(self):
		yield from self._source_format(
			commit=self.commit,
			raiseexceptions=self.raiseexceptions,
		)


class _DatabaseCommand(Command):
	"""
	Base class of all commands that use a database connection.

	All database commands support the following parameter:

	``connection`` : database connection (optional)
		The database connection the use for the database command. If :const:`None`
		the currently active database connection will be used.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, *, connection=None, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.connection = connection


class _SQLCommand(_DatabaseCommand):
	"""
	Common base class of :class:`procedure` and :class:`sql`.
	"""

	@staticmethod
	def _createvar(cursor, type, value):
		var = cursor.var(type)
		var.setvalue(0, value)
		return var

	def _executesql(self, context, connection, query):
		cursor = connection.cursor()

		queryargvars = {}
		varargs = {}
		for (argname, argvalue) in self.args.items():
			if isinstance(argvalue, sqlexpr):
				continue # no value
			if isinstance(argvalue, var):
				varargs[argname] = argvalue
				if argvalue.key is not None and argvalue.key in context._locals:
					argvalue = context._locals[argvalue.key]
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
			if argvalue.key not in context._locals:
				value = queryargvars[argname].getvalue(0)
				newkeys[argname] = value
				if argvalue.key is not None:
					context._locals[argvalue.key] = value
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

				loadstr("foo/bar.txt", encoding="utf-8", errors="replace")

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, name, *, connection=None, raiseexceptions=None, args=None):
		super().__init__(connection=connection, raiseexceptions=raiseexceptions)
		self.name = name
		self.args = args or {}

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connection = context.getconnection(self.connection)

		argsql = ", ".join(f"{an}=>{av.expression}" if isinstance(av, sqlexpr) else f"{an}=>:{an}" for (an, av) in self.args.items())
		query = f"begin {self.name}({argsql}); end;"
		result = self._executesql(context, connection, query)
		self.finish(f"Called procedure {self.name!r} in {connection.connectstring()!r}")
		self.count(connectstring(connection), self.name)
		if result:
			self.log(f"New vars {result!r}")
		return result or None

	def source_format(self):
		yield from self._source_format(
			self.name,
			connection=self.connection,
			raiseexceptions=self.raiseexceptions,
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

	def __init__(self, sql, *, connection=None, raiseexceptions=None, args=None):
		super().__init__(connection=connection, raiseexceptions=raiseexceptions)
		self.sql = sql
		self.args = args or {}

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sql={self.sql!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connection = context.getconnection(self.connection)

		result = self._executesql(context, connection, self.sql)
		self.finish(f"Executed SQL")
		self.count(connectstring(connection))
		if result:
			self.log(f"New vars {result!r}")
		return result or None

	def source_format(self):
		yield from self._source_format(
			self.sql,
			connection=self.connection,
			raiseexceptions=self.raiseexceptions,
			args=self.args if self.args else None,
		)


@register
class literalsql(_SQLCommand):
	"""
	A :class:`!sql` is used for SQL that appears literally in the
	PySQL file. So apart from the ``sql`` attribute is has no further usable
	attributes (i.e. ``raiseexceptions`` and ``connectionname``).
	"""

	def __init__(self, sql):
		super().__init__()
		self.sql = sql

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sql={self.sql!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		sql = self.sql

		if sql.endswith((";", "/")):
			sql = sql[:-1]
		connection = context.getconnection(None)
		connection.cursor().execute(sql)
		self.finish(f"Executed literal SQL")
		self.count(connectstring(connection))

	def source(self, tabsize=None):
		sql = (self.sql or "").strip()
		if tabsize is not None:
			sql = sql.expandtabs(tabsize)
		return sql


@register
class commit(_SQLCommand):
	"""
	A :class:`!commit` command commits the current transaction in the activate
	database connection (or the one specified via the ``connection`` parameter).

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, sql, *, connection=None):
		super().__init__(connection=connection, raiseexceptions=raiseexceptions)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connection = context.getconnection(self.connection)

		self.log(f"Committing transaction in {connectstring(connection)!r}")
		connection.commit()
		self.finish(f"Committed transaction in {connectstring(connection)!r}")
		self.count(connectstring(connection))

	def source_format(self):
		yield from self._source_format(
			self.connection,
			raiseexceptions=self.raiseexceptions,
		)


@register
class rollback(_SQLCommand):
	"""
	A :class:`!rollback` command rolls back the current transaction in the
	activate database connection (or the one specified via the ``connection``
	parameter).

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, sql, *, connection=None):
		super().__init__(connection=connection, raiseexceptions=raiseexceptions)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connection = context.getconnection(self.connection)

		context.log(f"Rolling back transaction in {connectstring(connection)!r}")
		connection.rollback()
		self.finish(f"Rolled back transaction in {connectstring(connection)!r}")
		self.count(connectstring(connection))

	def source_format(self):
		yield from self._source_format(
			self.connection,
			raiseexceptions=self.raiseexceptions,
		)


class literalpy(_DatabaseCommand):
	"""
	A :class:`!literalpy` is used for Python code that appears literally in the
	PySQL file. So apart from the ``code`` attribute is has no further usable
	attributes (i.e. ``connection`` and ``raiseexceptions`` from the base class
	are all ``None``).
	"""

	def __init__(self, code):
		super().__init__()
		prefix = f"{Context.literalpy_begin}\n"
		suffix = f"\n{Context.literalpy_end}"
		if not code.startswith(prefix) or not code.endswith(suffix):
			raise ValueError(f"{self.__class__.__qualname__} code must start with {prefix!r} and end with {suffix!r}")
		self.code = code

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} code={self.code!r} location={self.location} at {id(self):#x}>"

	def globals(self, context, connection):
		vars = {command.__name__: CommandExecutor(command, context) for command in Command.commands.values()}
		vars["sqlexpr"] = sqlexpr
		vars["datetime"] = datetime
		vars["connection"] = connection
		return vars

	def execute(self, context):
		connection = context.connections[-1] if context.connections else None
		vars = self.globals(context, connection)

		code = self.location.source(True) if self.location is not None else self.code
		code += "\n"
		code = compile(code, context.filename, "exec")
		exec(code, vars, context._locals)

		self.finish(f"Executed Python block")
		self.count(connectstring(connection))

	def source(self, tabsize=None):
		code = self.code
		if tabsize is not None:
			code = code.expandtabs(tabsize)
		return code


@register
class setvar(Command):
	"""
	The :class:`!setvar` command sets a variable to a fixed value. The following
	parameters are supported:

	``name`` : string (required)
		The name of the variable to set.

	``value`` : object (required)
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
		context._locals[self.name] = self.value

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
		context._locals.pop(self.name, None)

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

	for all subsequent commands any exception will be ignored and reported and
	command execution will continue with the next command. ::

		raiseexceptions(True)

	will switch back to aborting the execution of the PySQL script once an
	exception is encountered.

	Note that the global configuration will only be relevant for commands that
	don't specify the ``raiseexceptions`` parameter themselves.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, *, value, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.value = value

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} value={self.value!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		self.log(f"Setting raiseexceptions to {self.value}")
		context.raiseexceptions[-1] = self.value

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

	for all subsequent commands any exception will be ignored and reported and
	command execution will continue with the next command. It is possible to
	switch back to the previous exception handling mode via::

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
		self.log(f"Pushing raiseexceptions value {self.value}")
		context.raiseexceptions.append(self.value)

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
		self.finish(f"Popped raiseexceptions value {oldvalue}: returning to {context.raiseexceptions[-1]}")
		return oldvalue

	def source_format(self):
		yield from self._source_format(
			raiseexceptions=self.raiseexceptions,
		)


@register
class checkerrors(_DatabaseCommand):
	"""
	The :class:`!checkerrors` command checks that there are no compilation errors
	in the active database schema. If there are, an exception will be raised.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`
	(but the value of the ``raiseexceptions`` key will be ignored).
	"""

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connection = context.getconnection(None)

		self.log(f"Checking errors in {connectstring(connection)!r}")

		cursor = connection.cursor()
		cursor.execute("select lower(type), name from user_errors group by lower(type), name")
		invalid_objects = [tuple(r) for r in cursor]

		if invalid_objects:
			raise CompilationError(invalid_objects)

		self.finish(f"No errors in {connectstring(connection)!r}")
		self.count(connectstring(connection))

	def source_format(self):
		yield from self._source_format()


@register
class scp(Command):
	"""
	The :class:`!scp` command creates a file by copying it via the :program:`scp`
	program. The following parameters are supported:

	``name`` : string (required)
		The name of the file to be created. It may contain ``format()`` style
		specifications containing any variable (for example those that appeared
		in a :class:`procedure` or :class:`sql` command). These specifiers will be
		replaced by the correct variable values. As these files will be copied via
		the :program:`scp` program, ssh file names can be used.

	``content``: bytes (required)
		The content of the file to be created. This can also be a
		:class:`loadbytes` command to load the content from an external file.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, *, name, content, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.name = name
		self.content = content

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} content={shortrepr(self.content)} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		filename = context.scpdirectory + self.name.format(**context._locals)
		self.log("Copying file to {filename!r}")

		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(self.content)
			tempname = f.name
		try:
			result = subprocess.run(["scp", "-q", tempname, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			if result.returncode:
				raise SCPError(result.returncode, (result.stdout or result.stderr).decode(errors="replace"))
		finally:
			os.remove(tempname)
		self.finish(f"Copied to {filename!r}")

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
		specifications containing any variable (for example those that appeared
		in a :class:`procedure` or :class:`sql` command). These specifiers will
		be replaced by the correct variable values.

	``content``: bytes (required)
		The content of the file to be created. This can also be a
		:class:`loadbytes` command to load the content from an external file.

	``mode``: integer (optional)
		The file mode for the new file. If the mode is specified, :func:`os.chmod`
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
		filename = context.filedirectory / self.name.format(**context._locals)

		self.log(f"Saving file {context.strfilename(filename)!r}")
		try:
			filename.write_bytes(self.content)
		except FileNotFoundError: # probably the directory doesn't exist
			parent = filename.parent
			if parent != filename:
				parent.mkdir(parents=True)
				filename.write_bytes(self.content)
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
		self.finish(f"Saved {len(self.content):,} bytes to {context.strfilename(filename)!r}")

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
	The :class:`!resetsequence` command resets a sequence in the database to
	the maximum value of a field in a table. The following parameters are
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

	def __init__(self, sequence, table, field, *, minvalue=None, increment=None, connection=None, raiseexceptions=None):
		super().__init__(connection=connection, raiseexceptions=raiseexceptions)
		self.sequence = sequence
		self.table = table
		self.field = field
		self.minvalue = minvalue
		self.increment = increment

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sequence={self.sequence!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connection = context.getconnection(self.connection)

		cursor = connection.cursor()

		self.log(f"Resetting sequence {self.sequence}")
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
			cursor.execute(f"alter sequence {self.sequence} increment by {self.step}")
			cursor.execute(f"select {self.sequence}.nextval from dual")
			seqvalue = cursor.fetchone()[0]
			cursor.execute(f"alter sequence {self.sequence} increment by {self.increment}")
			self.finish(f"Reset sequence {self.sequence} to {seqvalue}")
		else:
			seqvalue = None
			self.finish(f"Resetting sequence {self.sequence} skipped")

		self.count(connectstring(connection))

		return seqvalue

	def source_format(self):
		yield from self._source_format(
			self.sequence,
			self.table,
			self.field,
			minvalue=self.minvalue,
			increment=self.increment,
			connection=self.connection,
			raiseexceptions=self.raiseexceptions,
		)


@register
class user_exists(_DatabaseCommand):
	"""
	The :class:`!user_exists` command returns whether a user with a specified
	name exists in the database. It supports the following parameters:

	``name``: string (required)
		The name of the user to be checked for existence.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, name, *, connection=None, raiseexceptions=None):
		super().__init__(connection=connection, raiseexceptions=raiseexceptions)
		self.name = name

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connection = context.getconnection(self.connection)

		cursor = connection.cursor()
		cursor.execute("select count(*) from all_users where username = :name", name=self.name)
		result = cursor.fetchone()[0] > 0
		self.count(connectstring(connection))

		return result

	def source_format(self):
		yield from self._source_format(
			self.name,
			connection=self.connection,
			raiseexceptions=self.raiseexceptions,
		)


@register
class object_exists(_DatabaseCommand):
	"""
	The :class:`!object_exists` command return whether an object with a
	specified name exists in the database. It supports the following parameters:

	``name``: string (required)
		The name of the object to be checked for existence.

	``owner``: string (optional)
		The owner of the object (defaults to the current user if not specified
		or :const:`None`).

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, name, *, owner=None, connection=None, raiseexceptions=None):
		super().__init__(connection=connection, raiseexceptions=raiseexceptions)
		self.name = name
		self.owner = owner

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connection = context.getconnection(self.connection)

		cursor = connection.cursor()

		if self.owner is None:
			cursor.execute("select count(*) from user_objects where object_name = :name", name=self.name)
		else:
			cursor.execute("select count(*) from all_objects where owner = :owner and object_name = :name", owner=self.owner, name=self.name)
		result = cursor.fetchone()[0] > 0
		self.count(connectstring(connection))

		return result

	def source_format(self):
		yield from self._source_format(
			self.name,
			owner=self.owner,
			connection=self.connection,
			raiseexceptions=self.raiseexceptions,
		)


@register
class drop_types(_DatabaseCommand):
	"""
	The :class:`!drop_types` command drops database objects.

	Unlike all other commands this command requires the :mod:`ll.orasql` module.

	:class:`!drop_types` supports the following parameters:

	``drop``: list of strings (optional)
		The types of objects to drop (value must be names for :mod:`ll.orasql`
		object types.

	``keep``: list string (required)
		The types of objects to keep (value must be names for :mod:`ll.orasql`
		object types.

	``drop`` and ``keep`` are mutually exclusive. When neither of them
	is specified *all* database objects will be dropped.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, *, drop=None, keep=None, connection=None, raiseexceptions=None):
		super().__init__(connection=connection, raiseexceptions=raiseexceptions)
		self.drop = drop
		self.keep = keep

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

	def execute(self, context):
		connection = context.getconnection(self.connection)

		if self.drop is not None and self.keep is not None:
			raise ValueError("The parameters 'drop' and 'keep' are mutually exclusive")

		if self.drop is not None:
			dropstr = " ".join(self.drop)
			self.log(f"Dropping {dropstr} from {connectstring(connection)!r}")
		elif self.keep is not None:
			keepstr = " ".join(self.keep)
			self.log(f"Dropping everything except {keepstr} from {connectstring(connection)!r}")
		else:
			self.log(f"Dropping everything from {connectstring(connection)!r}")

		cursor = connection.cursor()

		def drop_obj(obj):
			if self.drop is not None:
				return obj.type in self.drop
			elif self.keep is not None:
				return obj.type not in self.keep
			else:
				return True

		count = 0
		for (i, obj) in enumerate(connection.objects(owner=None, mode="drop")):
			if obj.owner is None:
				if drop_obj(obj):
					ddl = obj.dropsql(connection, False)
					if ddl:
						cursor.execute(ddl)
						count += 1

		self.finish(f"Dropped {count:,} objects from {connectstring(connection)!r}")
		self.count(connectstring(connection))

		return count

	def source_format(self):
		yield from self._source_format(
			drop=self.drop,
			keep=self.keep,
			connection=self.connection,
			raiseexceptions=self.raiseexceptions,
		)


@register
class comment(Command):
	"""
	The :class:`!comment` command does nothing.
	"""

	def __init__(self, comment):
		super().__init__()
		if not all(line.startswith("#") for line in comment.splitlines()):
			raise ValueError("All lines in comment must start with '#")
		self.comment = comment

	def __str__(self):
		return f"comment {self.location}"

	def execute(self, context):
		pass

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
		relative to the directory containing the PySQL file that contains
		:class:`loadbytes` command.

	For the parameter ``raiseexceptions`` see the base class :class:`Command`.
	"""

	def __init__(self, filename, *, raiseexceptions=None):
		super().__init__(raiseexceptions=raiseexceptions)
		self.filename = filename

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} filename={self.filename!r} {self.location} at {id(self):#x}>"

	def execute(self, context):
		"""
		Read the file and return the file content as a :class:`bytes` object.
		"""
		filename = pathlib.Path(self.filename)
		return filename.read_bytes()

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
		if self.errors != "strict":
			result += f", errors={self.errors!r}"
		result += f"{self.location} at {id(self):#x}>"
		return result

	def execute(self, context):
		"""
		Read the file and return the file content as a :class:`str` object.
		"""
		filename = pathlib.Path(self.filename)
		return filename.read_text(encoding=self.encoding, errors=self.errors)

	def source_format(self):
		yield from self._source_format(
			self.filename,
			encoding=self.encoding,
			errors=self.errors if self.errors != "strict" else None,
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

	:obj:`type` : class (optional)
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
		if self.key in context._locals:
			value = context._locals[self.key]
			if value is not None and not isinstance(value, self.type):
				raise TypeError(f"{value!r} is not of type {format_class(self.type)}")
			return value
		else:
			return self

	def source_format(self):
		yield repr(self)


@register
class env(Command):
	"""
	A :class:`env` command returns the value of an environment variable.

	The following parameters are supported:

	:obj:`name` : string (required)
		The name of the environment variable.

	:obj:`default` : string (optional)
		The default to use, if the environment variable isn't set.
		This defaults to :const:`None`.
	"""

	def __init__(self, name, default=None):
		super().__init__(raiseexceptions=None)
		self.name = name
		self.default = default

	def __repr__(self):
		return f"env({self.name!r})"

	def execute(self, context):
		return os.environ.get(self.name, self.default)

	def source_format(self):
		yield repr(self)


@register
class log(Command):
	"""
	:class:`log` commands generate logging output.

	The following parameters are supported:

	:obj:`objects` : Any
		The objects to log. String will be logged directly. For all other
		objects :func:`repr` will be called.
	"""

	def __init__(self, *objects):
		super().__init__(raiseexceptions=None)
		self.objects = objects

	def execute(self, context):
		self.log(*self.objects)

	def source_format(self):
		yield from self._source_format(*self.objects)


class CommandExecutor:
	"""
	A :class:`!CommandExecutor` object wraps a :class:`Command` object in a
	callable. Calling the :class:`!CommandExecutor` object executes the command
	using the specified context and returns the command result.

	This class exists because :class:`Command` objects serve two purposes:

	1.	They can be created to print them to a file (via the method
		:meth:`Command.source`);

	2.	They can be put into a PySQL file which will then be read and executed,
		with must then create the :class:`Command` object and execute it
		immediately. This is the job of :class:`!CommandExecutor` objects.
	"""
	def __init__(self, command, context):
		self.command = command
		self.context = context

	def __call__(self, *args, **kwargs):
		command = self.command(*args, **kwargs)
		context = self.context
		command._context = context
		command.location = context._location
		command._starttime = datetime.datetime.now()
		if context._runstarttime is None:
			context._runstarttime = command._starttime
			first = True
		else:
			first = False
		context.totalcount += 1
		command._nr = context.totalcount
		if command.raiseexceptions is not None:
			context.raiseexceptions.append(command.raiseexceptions)

		if context.verbose == "type":
			if isinstance(command, procedure):
				print(f" {command.__class__.__qualname__}({command.name})", end="", flush=True)
			else:
				print(f" {command.__class__.__qualname__}", end="", flush=True)
		elif context.verbose == "file":
			endfile = False
			if context._lastlocation is not command.location:
				if context._lastlocation is None or command.location.filename != context._lastlocation.filename:
					print(f" [{command.location.filename} :: {command.location._lines()}", end="", flush=True)
				else:
					print(f" [{command.location._lines()}", end="", flush=True)
				endfile = True
			else:
				pass # still the same location
		elif context.verbose == "log":
			pass
		elif context.verbose == "full":
			if command.location is not context._lastlocation:
				if not first:
					print(flush=True)
				command.location.print_source(context)
		# Update ``_lastlocation`` *now*, so that other commands called during :meth:`execute` don't print the location/source twice
		context._lastlocation = command.location

		try:
			result = command.execute(context)
		except Exception as exc:
			command._stoptime = datetime.datetime.now()
			if context.raiseexceptions[-1]:
				if context.verbose:
					print(flush=True)
				raise CommandError(command) from exc
			else:
				context.errorcount += 1
				if context.verbose == "dot":
					print("!", end="", flush=True)
				elif context.verbose == "type":
					print(f"->failed", end="", flush=True)
				elif context.verbose == "file":
					if endfile:
						print(f"]->failed", end="", flush=True)
				elif context.verbose == "full":
					exctext = str(exc).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
					command.log(f"ignored {format_class(exc.__class__)}: {exctext}")
				result = None
		else:
			command._stoptime = datetime.datetime.now()
			if context.verbose == "dot":
				print(".", end="", flush=True)
			elif context.verbose == "file":
				if endfile:
					print(f"]", end="", flush=True)
			elif context.verbose in {"log", "full"}:
				if command._message is not None:
					command.log(command._message, f"(in {command._stoptime-command._starttime})")
		finally:
			command._stoptime = datetime.datetime.now()
			if command.raiseexceptions is not None:
				context.raiseexceptions.pop()
		context.count(command.__class__.__qualname__, *command._counter)

		return result


###
###
###

class Context:
	"""
	A :class:`Context` objects contains the configuration and run time
	information required for importing a PySQL file.
	"""

	terminator = "-- @@@"
	literalpy_begin = "#>>>"
	literalpy_end = "#<<<"
	command_begin = tuple(f"{cname}(" for cname in Command.commands)
	command_end = ")"

	def __init__(self, connectstring=None, scpdirectory="", filedirectory="", commit=True, tabsize=None, context=None, raiseexceptions=True, verbose=0, summary=False, vars=None):
		self.connections = []
		self.commit = commit
		self.scpdirectory = scpdirectory
		self.filedirectory = pathlib.Path(filedirectory).resolve()
		self.basedirectory = pathlib.Path.cwd().resolve()
		self.homedirectory = pathlib.Path.home().resolve()
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
		self.filename = None
		self._lastlocation = None
		self._lastcommand = None
		self._locals = {v.key: v for v in vars} if vars else {}
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
			self.connect(connectstring, None)

	def connect(self, connectstring, mode=None):
		mode = cx_Oracle.SYSDBA if mode == "sysdba" else 0
		if orasql is not None:
			connection = orasql.connect(connectstring, mode=mode, readlobs=True)
		else:
			connection = cx_Oracle.connect(connectstring, mode=mode)
		self.connections.append(connection)
		return connection

	def disconnect(self, commit=None):
		if commit is None:
			commit = self.commit
		if not self.connections:
			raise ValueError(f"no connection available")
		connection = self.connections.pop()
		if commit:
			connection.commit()
		else:
			connection.rollback()
		connection.close()
		return connection

	def getconnection(self, connection):
		if connection is not None:
			return connection
		if not self.connections:
			raise ValueError(f"no connection available")
		return self.connections[-1]

	def log(self, command, *objects):
		if self.verbose in {"log", "full"}:
			now = datetime.datetime.now()
			print(f"[t+{now-self._runstarttime}] :: #{command._nr:,} :: [{command.strlocation(self)}] >>", end="", flush=True)
			for (i, obj) in enumerate(objects):
				print(" ", end="", flush=True)
				if isinstance(obj, str):
					print(obj, end="", flush=True)
				elif isinstance(obj, int):
					print(f"{obj:,}", end="", flush=True)
				else:
					print(repr(obj), end="", flush=True)
			print(flush=True)

	@contextlib.contextmanager
	def changed_filename(self, filename):
		filename = pathlib.Path(filename)
		oldfilename = self.filename
		self.filename = filename
		oldcwd = pathlib.Path.cwd()
		os.chdir(filename.parent)
		try:
			yield pathlib.Path(filename.name)
		finally:
			self.filename = oldfilename
			os.chdir(oldcwd)

	def globals(self):
		vars = {command.__name__: CommandExecutor(command, self) for command in Command.commands.values()}
		vars["sqlexpr"] = sqlexpr
		vars["datetime"] = datetime
		vars["connection"] = self.connections[-1] if self.connections else None
		return vars

	def _load(self, stream):
		"""
		Load a PySQL file from :obj:`stream` and executes the commands in the file.
		:obj:`stream` must be an iterable over lines that contain the PySQL
		commands.
		"""
		lines = []

		vars = self.globals()

		# ``state`` is the state of the "parser", values have the following meaning
		# ``None``: outside of any block
		# ``literalsql``: inside of literal SQL block
		# ``literalpy``: inside of literal Python block
		# ``dict``: inside of Python dict literal
		# others: inside a PySQL command of that name
		state = None

		def executeblock():
			# Drop empty lines at the start
			while lines and not lines[0][1].strip():
				del lines[0]
			# Drop empty lines at the end
			while lines and not lines[-1][1].strip():
				del lines[-1]
			try:
				if lines:
					self._location = Location(stream.name, lines)
					lines.clear()
					source = self._location.source(False)
					if state == "literalsql":
						CommandExecutor(literalsql, self)(source)
					elif state == "literalpy":
						CommandExecutor(literalpy, self)(source)
					elif state == "dict":
						code = compile(source, self._location.filename, "eval")
						args = eval(code, vars, self._locals)
						type = args.pop("type", "procedure")
						if type not in Command.commands:
							raise ValueError(f"command type {type!r} unknown")
						CommandExecutor(Command.commands[type], self)(**args)
					else:
						code = compile(source, self._location.filename, "exec")
						exec(code, vars, self._locals)
			except Exception as exc:
				raise LocationError(self._location) from exc

		for (i, line) in enumerate(stream, 1):
			line = line.rstrip()
			if state is None:
				if line.startswith("{"):
					lines.append((i, line))
					state = "dict"
					if line.endswith("}"):
						executeblock()
						state = None
				elif line == self.literalpy_begin:
					lines.append((i, line))
					state = "literalpy"
				elif line.startswith("#"):
					pass # Ignore comments
				elif line == self.terminator:
					pass # Still outside the block
				elif line.startswith(self.command_begin): # PySQL command constructor?
					lines.append((i, line))
					state = line[:line.find("(")]
					if line.endswith(self.command_end):
						executeblock()
						state = None
				elif line:
					lines.append((i, line))
					state = "literalsql"
			elif state == "dict":
				lines.append((i, line))
				if line == "}": # A single unindented ``}``
					executeblock()
					state = None
			elif state == "literalsql":
				if line.startswith(self.terminator):
					executeblock()
					state = None
				else:
					lines.append((i, line))
			elif state == "literalpy":
				lines.append((i, line))
				if line == self.literalpy_end:
					executeblock()
					state = None
			else:
				# Inside any of the PySQL commands as a function call
				lines.append((i, line))
				if line == self.command_end: # A single unindented ``)``
					executeblock()
					state = None
		executeblock()

	def executeall(self, *filenames):
		"""
		Execute all commands in the PySQL files specified by :obj:`filenames`.
		If :obj:`filenames` is empty :obj:`sys.stdin` is read.
		"""
		try:
			if self.verbose == "type":
				print("commands:", end="", flush=True)
			elif self.verbose == "file":
				print("files:", end="", flush=True)
			if filenames:
				for filename in filenames:
					filename = pathlib.Path(filename)
					with self.changed_filename(filename) as absfilenname:
						with absfilenname.open("r") as f:
							self._load(f)
			else:
				self._load(sys.stdin)
			for connection in self.connections:
				if self.commit:
					connection.commit()
				else:
					connection.rollback()
		finally:
			if self.verbose in {"dot", "type", "file"}:
				print(flush=True)
		self.print_summary()

	def print_summary(self):
		if self.summary:
			if self._runstarttime is None:
				self._runstarttime = datetime.datetime.now()
			now = datetime.datetime.now()
			if self.verbose:
				print(flush=True)
				print("\u2501"*self._width, flush=True)
				print(f"[t+{now-self._runstarttime}] >> Command summary:", flush=True)
			else:
				print("Command summary:", flush=True)
			anyoutput = False
			totallen = len(f"{self.totalcount:,}")

			def sortkey(keyvalue):
				(key, value) = keyvalue
				if len(key) > 1: # db command
					return (0, key[1], key[0] != "procedure", *key)
				else:
					return (1, *key)
			lastconnection = None
			for (key, count) in sorted(self.commandcounts.items(), key=sortkey):
				connection = key[1] if len(key) > 1 else None
				if not anyoutput or connection != lastconnection:
					print(flush=True)
					if connection:
						print(f"Connection {connection}:", flush=True)
					elif connection is not None:
						print(f"Without connection:", flush=True)
					else:
						print("Other commands:", flush=True)
				lastconnection = connection
				anyoutput = True
				keys = " ".join((key[0], *key[2:])) if len(key) > 1 else key[0]
				print(f"   {count:>{totallen},} {keys}", flush=True)
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

	def strfilename(self, filename):
		filename = pathlib.Path(filename).resolve()
		try:
			filename = filename.relative_to(self.basedirectory)
		except ValueError:
			try:
				filename = filename.relative_to(self.homedirectory)
			except ValueError:
				return str(filename)
			else:
				return f"~/{filename}"
		else:
			return str(filename)

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
		As PySQL source code is evaluated via :func:`eval`/:func:`exec` anyway,
		it it always possible to embed Python expressions in PySQL source code.
		However this doesn't roundtrip, i.e. printing the PySQL command via
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
	The location of a PySQL/SQL command in a PySQL file.
	"""

	def __init__(self, filename, lines):
		self.filename = filename
		self.startline = lines[0][0]
		self.endline = lines[-1][0]
		self.lines = lines[:]

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} filename={self.filename!r} startline={self.startline!r} endline={self.endline!r} at {id(self):#x}>"

	def __str__(self):
		if self.startline is None and self.endline is None:
			return str(self.filename)
		else:
			return f"{self.filename} :: {self._lines()}"

	def _lines(self):
		if self.startline is None and self.endline is None:
			return "?"
		elif self.startline == self.endline:
			return f"{self.startline:,}"
		else:
			return f"{self.startline:,}-{self.endline:,}"

	def source(self, offset):
		source = "\n".join(line for (linenumber, line) in self.lines)
		if offset and self.startline is not None:
			# Prepend empty lines, so in case of an exception the
			# linenumbers in the stacktrace match
			source = (self.startline-1) * "\n" + source
		return source

	def print_source(self, context):
		ellipsis = "\u22ee"
		if self.startline and self.endline:
			startline = self.startline
			endline = self.endline
			linenumberlen = len(f"{self.endline:,}")
			filename = context.strfilename(self.filename)
			filenamelen = len(filename)
			ruletop    = "\u2500" * (linenumberlen + 1) + "\u252c[ " + filename + " ]" + "\u2500" * (context._width - 2 - linenumberlen - 4 - filenamelen)
			rulebottom = "\u2500" * (linenumberlen + 1) + "\u2534" + "\u2500" * (context._width - 2 - linenumberlen)
			print(ruletop, flush=True)

			for (linenumber, line) in self.lines:
				if context.context is not None and startline + context.context <= linenumber <= endline - context.context:
					if startline + context.context == linenumber:
						print(f"{ellipsis:>{linenumberlen}} \u2502 {ellipsis}", flush=True)
				else:
					if context.tabsize is not None:
						line = line.expandtabs(context.tabsize)
					print(f"{linenumber:{linenumberlen},} \u2502 {line}", flush=True)
			print(rulebottom, flush=True)
		else:
			endline = len(self.lines) - 1
			rule = "\u2500" * self._width
			print(rule, flush=True)
			for (linenumber, line) in self.lines:
				if context.context is not None and context.context <= linenumber <= endline - context.context:
					if context.context == linenumber:
						print(ellipsis, flush=True)
				else:
					if context.tabsize is not None:
						line = line.expandtabs(context.tabsize)
					print(line, flush=True)
			print(rule, flush=True)


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
	p = argparse.ArgumentParser(description="Import a PySQL file into an Oracle database", epilog="For more info see http://python.livinglogic.de/pysql.html")
	p.add_argument("files", nargs="*", help="PySQL files (none: read from stdin)")
	p.add_argument("-d", "--database", dest="connectstring", metavar="CONNECTSTRING", help="Oracle connect string specifying the default database connection (default %(default)s)", default=None)
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", choices=("dot", "type", "file", "log", "full"))
	p.add_argument("-r", "--rollback", dest="rollback", help="Should database transactions be rolled back? (default: commit on disconnect/after run)", default=False, action="store_true")
	p.add_argument("-s", "--scpdirectory", dest="scpdirectory", metavar="DIR", help="File name prefix for files to be copied via the 'scp' command (default: current directory)", default="")
	p.add_argument("-f", "--filedirectory", dest="filedirectory", metavar="DIR", help="File name prefix for files to be copied via the 'file' command (default: current directory)", default="")
	p.add_argument(      "--tabsize", dest="tabsize", metavar="INTEGER", help="Number of spaces a tab expands to when printing source (default %(default)r)", type=int, default=8)
	p.add_argument(      "--context", dest="context", metavar="INTEGER", help="Maximum number of context lines when printing source code (default %(default)r)", type=int, default=None)
	p.add_argument("-z", "--summary", dest="summary", help="Output a summary after executing all commands", default=False, action="store_true")
	p.add_argument("-D", "--define", dest="defines", metavar="VARSPEC", help="Set variables before executing the script (can be specified multiple times). The format for VARSPEC is: 'name' or 'name=value' or 'name:type' or 'name:type=value'. Type may be 'str', 'bool', 'int' or 'float'.", default=[], action="append", type=define)

	args = p.parse_args(args)

	context = Context(
		connectstring=args.connectstring,
		scpdirectory=args.scpdirectory,
		filedirectory=args.filedirectory,
		commit=not args.rollback,
		tabsize=args.tabsize,
		context=args.context,
		verbose=args.verbose,
		summary=args.summary,
		vars=args.defines
	)
	context.executeall(*args.files)


if __name__ == "__main__":
	sys.exit(main())
