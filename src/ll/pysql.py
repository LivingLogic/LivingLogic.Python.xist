# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2012-2022 by LivingLogic AG, Bayreuth/Germany
## Copyright 2012-2022 by Walter Dörwald
##
## All Rights Reserved
##
## See LICENSE for the license

"""
Overview
========
The module/script :mod:`!pysql` can be used to import data into one or more
Oracle or Postgres databases. It reads ``pysql`` files which are an extension
of normal Oracle or Postgres SQL files.

A PySQL file can contain different types of commands.


SQL commands
------------

A PySQL file may contain normal SQL commands. For the :mod:`!pysql` script
to be able to execute these commands they must be terminated with a comment
line ``-- @@@``. :mod:`!pysql` will prepare the command for execution and
execute it. Any exception that is raised as a result of executing the command
will stop the script and be reported. This is in contrast to how Oracle's
``sqlplus`` executes SQL commands. ``sqlplus`` would continue after an error
and exit with status code 0 even if there were errors. (For Oracle :mod:`!pysql`
can also explicitely ignore any exception raised by commands by specifying
a different exception handling mode.)

A PySQL file that only contains SQL commands is still a valid Oracle or Postgres
SQL file, so it still can be executed via ``sqlplus`` or ``psql``.


Literal Python blocks
---------------------

A literal Python block starts with a line that only contains ``#>>>`` and
ends with a line that only contains ``#<<<``. Python code within the block
gets executed when the block is encountered. The following objects are available
within the block as global variables:

``connection``
	The active database connection (or :const:`None` if there is no active
	database connection).

``DB_TYPE_CLOB``
	:data:`cx_Oracle.DB_TYPE_CLOB`, i.e. :mod:`cx_Oracle`\\s type
	for ``CLOB`` parameters;

``DB_TYPE_NCLOB``
	:data:`cx_Oracle.DB_TYPE_NCLOB`, i.e. :mod:`cx_Oracle`\\s type
	for ``NCLOB`` parameters;

``DB_TYPE_BLOB``
	:data:`cx_Oracle.DB_TYPE_BLOB`, i.e. :mod:`cx_Oracle`\\s type
	for ``BLOB`` parameters;

:class:`sqlexpr`
	Can be used to specify that an argument for a :class:`procedure` should be
	an SQL expression instead of a Python value or a :class:`var` object;

:mod:`datetime`
	Python's datetime module;

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
	Include another PySQL file;

:class:`connect`
	Connect to a database;

:class:`disconnect`
	Disconnect from the active database connection;

:class:`procedure`
	Call a procedure in the database (and handle OUT parameters via :class:`var`
	objects);

:class:`sql`
	Execute an SQL statement in the database (and handle OUT parameter via
	:class:`var` objects);

:class:`literalsql`
	Execute an SQL statement in the database (this is what SQL commands get
	converted to);

:class:`commit`
	Commit the transaction in the active database connection;

:class:`rollback`
	Roll back the transaction in the active database connection;

:class:`literalpy`
	Execute Python code (this is what literal Python blocks get converted to);

:class:`setvar`
	Set a variable;

:class:`unsetvar`
	Delete a variable;

:class:`raise_exceptions`
	Set the exception handling mode;

:class:`push_raise_exceptions`
	Temporarily modifies the exception handling mode;

:class:`pop_raise_exceptions`
	Reverts to the previously active exception handling mode;

:class:`check_errors`
	Checks whether there are invalid database objects;

:class:`scp`
	Create a file on a remote host via :program:`scp`;

:class:`file`
	Create a file on the local machine;

:class:`reset_sequence`
	Resets a database sequence to the maximum value of a field in a table;

:class:`user_exists`
	Test whether a database user exists;

:class:`schema_exists`
	Tests whether a database schema exists (which is the same as a user for
	Oracle);

:class:`object_exists`
	Test whether a database object (table, package, procedure, etc.) exists;

:class:`constraint_exists`
	Test whether a database constraint (primary key, foriegn key, unique or
	check constraint) exists;

:class:`drop_types`
	Drop all database objects of a certain type;

:class:`comment`
	A comment;

:class:`loadbytes`
	Load the binary content of a file;

:class:`loadstr`
	Load the text content of a file;

:class:`var`
	Mark an argument for a :class:`procedure` or :class:`sql` command as being
	an OUT parameter (or pass the value of the variable in subsequent
	:class:`procedure`/:class:`sql` commands);

:class:`env`
	Return the value of an environment variable.


Comments
--------

A line starting with ``#`` (outside of a SQL command or literal Python block)
is considered a comment and will be ignored.


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

	reset_sequence(
		'person_seq',
		table='person',
		field='per_id',
	}

	check_errors()

This file can then be imported into an Oracle database with the following
command::

	python -m ll.pysql -d user/pwd@database data.pysql

This will create two sequences, two tables and two procedures. Then it will
import two records, one by calling ``person_insert`` and one by calling
``contact_insert``. The PL/SQL equivalent of procedure calls is::

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
opened with the :class:`connect` command. This command opens a new database
connection. Subsequent commands that talk to the database will use this
connection until a :class:`disconnect` command disconnects from the database
and reverts to the previous connection (or ``None`` if this was the
outermost open database connection). An example looks like this::

	connect("oracle:user/pwd@db")
	procedure("test")
	disconnect()

for Oracle or like this::

	connect("postgres:host=localhost dbname=db user=me password=secret")
	procedure("test")
	disconnect()

for Postgres.


Variables
=========

Variable objects can be used to receive OUT parameters of procedure calls or
SQL statements. A variable object can be specified like this: ``var("foo")``.
``"foo"`` is the "name" of the variable. When a variable object is passed
to a procedure the first time (i.e. the variable object is uninitialized),
the resulting value after the call will be stored under the name of the
variable. When the variable is used in a later command the stored value will
be used instead. (Note that it's not possible to use the same variable twice
in the same procedure call, if it hasn't been used before, however in later
commands this is no problem).

The type of the variable defaults to :class:`int`, but a different type can be
passed when creating the object by passing the Python type like this:
``var("foo", str)``.

It is also possible to create variable objects via command line parameters.

As a PySQL command is a Python literal, it is possible to use Python expressions
inside a PySQL command.


External files
==============

Inside a PySQL command it is possible to load values from external files.
The :class:`loadbytes` command loads a :class:`bytes` object from an external
file like this::

	loadbytes("path/to/file.png")

A :class:`str` object can be loaded with the :class:`loadstr` command like
this::

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

``pysql.py`` has no external dependencies except for :mod:`cx_Oracle`
(for Oracle) or :mod:`psycopg` (for Postgres) and can be used as a script for
importing a PySQL file into the database (However some commands require
:mod:`ll.orasql` for an Oracle database). As a script it supports the following
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
		commands).

	``-d``, ``--database``
		The initial database connection that will be used before any additional
		:class:`connect` commands.

		For Postgres the value must start with ``postgres:`` the rest of the
		value will be passed to :meth:`psycopg.Connection.connect` as a positional
		argument. For example::

			postgres:host=localhost dbname=test user=me password=secret

		For Oracle the value may start with ``oracle:``. The rest can be a
		standard Oracle connectstring. For example::

			me/secret@database

	``-z``, ``--summary``
		Give a summary of the number of commands executed and procedures called.

	``-r``, ``--rollback``
		Specifies that transactions should be rolled back at the end of the script
		run, or when a :class:`disconnect` command disconnects from a database.
		The default is to commit at the end or on each disconnect. (But note that
		for Oracle when a DDL statement is in the script, Oracle will still
		implicitely commit everything up to the statement.)

	``-s``, ``--scpdirectory``
		The base directory for :class:`scp` file copy commands. As files are
		copied via :program:`scp` this can be a remote filename (like
		``root@www.example.org:~/uploads/``) and must include a trailing ``/``.

		If it is a local directory it should be absolute (otherwise PySQL
		scripts included from other directories won't work).

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

# We're importing :mod:`datetime` to make it available to :func:`exec`
import sys, os, os.path, argparse, collections, time, datetime, pathlib, tempfile, subprocess, contextlib

try:
	import pwd
except ImportError:
	pwd = None

try:
	import grp
except ImportError:
	grp = None

try:
	import cx_Oracle
except ImportError:
	cx_Oracle = None

try:
	from ll import orasql
except ImportError:
	orasql = None

try:
	import psycopg
except ImportError:
	psycopg = None

try:
	from psycopg import rows
except ImportError:
	rows = None

__docformat__ = "reStructuredText"


def format_class(obj):
	"""
	Return the name for the class ``obj``.
	"""
	if obj.__module__ not in ("builtins", "exceptions"):
		return f"{obj.__module__}.{obj.__qualname__}"
	else:
		return obj.__qualname__


reprthreshold = 100


def shortrepr(value):
	"""
	Return a short "repr" output for a :class:`str` or :class:`bytes` value.

	If the value ``value`` is sort enough, the normal :func:`repr` output will
	be returned, otherwise an abbreviated value will be returned, i.e. something
	like this::

		<'foobarbaz' ... (1234 characters)>
	"""
	if isinstance(value, bytes) and len(value) > reprthreshold:
		return f"<{bytes.__repr__(value[:reprthreshold])} ... ({len(value):,} bytes)>"
	elif isinstance(value, str) and len(value) > reprthreshold:
		return f"<{str.__repr__(value[:reprthreshold])} ... ({len(value):,} characters)>"
	else:
		return repr(value)


###
### Database handlers: Execute commands (and handle other stuff) for various databases
###


class Handler:
	"""
	A :class:`!Handler` object is responsible for executing PySQL commands.

	:class:`!Handler` can not execute commands that require a database connection.
	That is the job of the subclasses :class:`OracleHandler`,
	:class:`OraSQLHandler` and :class:`PostgresHandler`.
	"""

	@staticmethod
	def from_connectstring(connectstring, mode=None):
		"""
		Create an appropriate :class:`!Handler` from a connectstring.

		If ``connectstring`` is ``None``, a :class:`Handler` object will be
		returned.

		If ``connectstring`` starts with ``postgres:``, a :class:`PostgresHandler`
		will be returned.

		Otherwise on :class:`OracleHandler` will be returned.
		"""
		if connectstring is None:
			return Handler()
		elif connectstring.startswith("postgres:"):
			from psycopg import rows
			connection = psycopg.connect(connectstring[9:], row_factory=rows.dict_row)
			return PostgresHandler(connection)
		else:
			if connectstring.startswith("oracle:"):
				connectstring = connectstring[7:]
			mode = cx_Oracle.SYSDBA if mode == "sysdba" else 0
			if orasql is not None:
				connection = orasql.connect(connectstring, mode=mode, readlobs=True)
				return OraSQLHandler(connection)
			else:
				connection = cx_Oracle.connect(connectstring, mode=mode)
				return OracleHandler(connection)

	@staticmethod
	def from_command(command):
		"""
		Create an appropriate :class:`!Handler` from :class:`connect` command.
		"""
		return Handler.from_connectstring(command.connectstring, command.mode)

	def __init__(self):
		self.connection = None

	def connectstring(self):
		"""
		Return a string identifying the database connection for this handler.
		"""
		return ""

	def connect(self, context, command):
		"""
		Execute the :class:`connect` command ``command``.
		"""
		cs = command.connectstring
		if not command.cond:
			command.finish(f"Skipped connecting to {cs!r}")
			return None

		retry = command.retry if command.retry is not None else 1
		retrydelay = command.retrydelay if command.retrydelay is not None else 10

		for i in range(retry+1):
			if i == retry:
				handler = Handler.from_command(command)
			else:
				try:
					handler = Handler.from_command(command)
				except Exception as exc:
					if command.mode is not None:
						command.log(f"Connection #{i+1:,} to {cs!r} as {command.mode} failed:")
					else:
						command.log(f"Connection #{i+1:,} to {cs!r} failed:")
					exctext = str(exc).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
					command.log(f"{format_class(exc.__class__)}: {exctext}")
					if retrydelay > 0:
						command.log(f"Retrying after {retrydelay!r} seconds")
						time.sleep(retrydelay)
					else:
						command.log(f"Retrying immediately")
				else:
					break

		if command.mode is not None:
			command.finish(f"Connected to {cs!r} as {command.mode}")
		else:
			command.finish(f"Connected to {cs!r}")
		context.push_handler(handler)
		return handler.connection

	def include(self, context, command):
		"""
		Execute the :class:`include` command ``command``.
		"""
		filename = command.filename

		if not command.cond:
			command.finish(f"Skipped file {context.strfilename(filename)!r}")
		else:
			command.log(f"Including file {context.strfilename(filename)!r}")
			with context.changed_filename(filename) as fn:
				with fn.open("r", encoding="utf-8") as f:
					context._load(f)
			command.finish(f"Included file {context.strfilename(filename)!r}")

	def user_exists(self, context, command):
		"""
		Execute the :class:`user_exists` command ``command``.
		"""
		raise NoDatabaseError()

	def schema_exists(self, context, command):
		"""
		Execute the :class:`schema_exists` command ``command``.
		"""
		raise NoDatabaseError()

	def object_exists(self, context, command):
		"""
		Execute the :class:`object_exists` command ``command``.
		"""
		raise NoDatabaseError()

	def constraint_exists(self, context, command):
		"""
		Execute the :class:`constraint_exists` command ``command``.
		"""
		raise NoDatabaseError()

	def check_errors(self, context, command):
		"""
		Execute the :class:`check_errors` command ``command``.
		"""
		raise NoDatabaseError()

	def literalsql(self, context, command):
		"""
		Execute the :class:`literalsql` command ``command``.
		"""
		raise NoDatabaseError()

	def literalpy(self, context, command):
		"""
		Execute the :class:`literalpy` command ``command``.
		"""
		if not command.cond:
			self.finish(f"Skipped Python block")
			return None

		code = command.location.source() if command.location is not None else command.code
		code += "\n"
		code = compile(code, context.filename, "exec")
		exec(code, context._locals)

		command.finish(f"Executed Python block")
		command.count(self.connectstring())

	def procedure(self, context, command):
		"""
		Execute the :class:`procedure` command ``command``.
		"""
		raise NoDatabaseError()

	def sql(self, context, command):
		"""
		Execute the :class:`sql` command ``command``.
		"""
		raise NoDatabaseError()

	def reset_sequence(self, context, command):
		"""
		Execute the :class:`reset_sequence` command ``command``.
		"""
		raise NoDatabaseError()

	def drop_types(self, context, command):
		"""
		Execute the :class:`drop_types` command ``command``.
		"""
		raise NoDatabaseError()

	def rollback(self, context, command):
		"""
		Execute the :class:`rollback` command ``command``.
		"""
		raise NoDatabaseError()

	def commit(self, context, command):
		"""
		Execute the :class:`commit` command ``command``.
		"""
		raise NoDatabaseError()

	def disconnect(self, context, command):
		"""
		Execute the :class:`disconnect` command ``command``.
		"""
		raise NoDatabaseError()

	def setvar(self, context, command):
		"""
		Execute the :class:`setvar` command ``command``.
		"""
		if command.cond:
			context._locals[command.name] = command.value

	def unsetvar(self, context, command):
		"""
		Execute the :class:`unsetvar` command ``command``.
		"""
		if self.cond:
			context._locals.pop(command.name, None)

	def raise_exceptions(self, context, command):
		"""
		Execute the :class:`raise_exceptions` command ``command``.
		"""
		if not command.cond:
			command.finish(f"Skipped setting raise_exceptions")
			return None

		command.log(f"Setting raise_exceptions to {command.value}")
		context.raise_exceptions[-1] = command.value

	def push_raise_exceptions(self, context, command):
		"""
		Execute the :class:`push_raise_exceptions` command ``command``.
		"""
		if not command.cond:
			command.finish(f"Skipped pushing raise_exceptions")
			return None

		command.log(f"Pushing raise_exceptions value {command.value}")
		context.raise_exceptions.append(command.value)

	def pop_raise_exceptions(self, context, command):
		"""
		Execute the :class:`pop_raise_exceptions` command ``command``.
		"""
		if not command.cond:
			command.finish(f"Skipped popping raise_exceptions")
			return None

		if len(context.raise_exceptions) <= 1:
			raise ValueError("raiseexception stack empty")
		oldvalue = context.raise_exceptions.pop()
		command.finish(f"Popped raise_exceptions value {oldvalue}: returning to {context.raise_exceptions[-1]}")
		return oldvalue

	def scp(self, context, command):
		"""
		Execute the :class:`scp` command ``command``.
		"""
		if not command.cond:
			command.finish(f"Skipped copying file")
			return None

		filename = context.scpdirectory + command.name.format(**context._locals)
		command.log(f"Copying file to {filename!r}")

		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(command.content)
			tempname = f.name
		try:
			result = subprocess.run(["scp", "-q", tempname, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			if result.returncode:
				raise SCPError(result.returncode, (result.stdout or result.stderr).decode(errors="replace"))
		finally:
			os.remove(tempname)
		command.finish(f"Copied to {filename!r}")

	def file(self, context, command):
		"""
		Execute the :class:`file` command ``command``.
		"""
		if not command.cond:
			command.finish(f"Skipped saving file")
			return None

		filename = context.filedirectory / command.name.format(**context._locals)

		command.log(f"Saving file {context.strfilename(filename)!r}")
		try:
			filename.write_bytes(command.content)
		except FileNotFoundError: # probably the directory doesn't exist
			parent = filename.parent
			if parent != filename:
				parent.mkdir(parents=True)
				filename.write_bytes(command.content)
			else:
				raise # we don't have a directory to make so pass the error on

		if command.mode:
			os.chmod(filename, command.mode)
		if command.owner or command.group:
			if command.owner:
				uid = command.owner
				if isinstance(uid, str):
					uid = pwd.getpwnam(uid)[2]
			else:
				uid = -1
			if command.group:
				gid = command.group
				if isinstance(gid, str):
					gid = grp.getgrnam(gid)[2]
			else:
				gid = -1
			os.chown(filename, uid, gid)
		command.finish(f"Saved {len(command.content):,} bytes to {context.strfilename(filename)!r}")

	def comment(self, context, command):
		"""
		Execute the :class:`comment` command ``command``.
		"""
		pass

	def loadbytes(self, context, command):
		"""
		Execute the :class:`loadbytes` command ``command``.
		"""
		if command.cond:
			filename = pathlib.Path(command.filename)
			return filename.read_bytes()

	def loadstr(self, context, command):
		"""
		Execute the :class:`loadstr` command ``command``.
		"""
		if command.cond:
			filename = pathlib.Path(command.filename)
			return filename.read_text(encoding=command.encoding, errors=command.errors)

	def var(self, context, command):
		"""
		Execute the :class:`var` command ``command``.
		"""
		if command.key in context._locals:
			value = context._locals[command.key]
			if value is not None and not isinstance(value, command.type):
				raise TypeError(f"{value!r} is not of type {format_class(command.type)}")
		return command

	def env(self, context, command):
		"""
		Execute the :class:`env` command ``command``.
		"""
		return os.environ.get(command.name, command.default)

	def log(self, context, command):
		"""
		Execute the :class:`log` command ``command``.
		"""
		command.log(*command.objects)


class DBHandler(Handler):
	"""
	Subclass of :class:`Handler` that has a real database connection.
	"""

	def __init__(self, connection):
		self.connection = connection

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} connection={self.connection!r} at {id(self):#x}>"

	def commit(self, context, command):
		cs = self.connectstring()
		if not self.cond:
			self.finish(f"Skipped committing transaction in {cs!r}")
			return None

		command.log(f"Committing transaction in {cs!r}")
		self.connection.commit()
		command.finish(f"Committed transaction in {cs!r}")
		command.count(cs)

	def rollback(self, context, command):
		cs = self.connectstring()
		if not self.cond:
			self.finish(f"Skipped rolling back transaction in {cs!r}")
			return None

		command.log(f"Rolling back transaction in {cs!r}")
		self.connection.rollback()
		command.finish(f"Rolled back transaction in {cs!r}")
		command.count(cs)

	def disconnect(self, context, command):
		# Get the connectstring now, as Postgres will forget the info after a disconnect
		cs = self.connectstring()

		if not command.cond:
			command.finish(f"Skipped disconnecting from {cs!r}")
			return None

		commit = command.commit if command.commit is not None else context.commit

		if commit:
			self.connection.commit()
		else:
			self.connection.rollback()
		self.connection.close()

		context.pop_handler() # Pop ourselves off of the handler stack

		if commit:
			command.finish(f"Disconnected from {cs!r} (transaction committed)")
		else:
			command.finish(f"Disconnected from {cs!r} (transaction rolled back)")

		return self.connection

	def _touchup_sql(self, sql):
		return sql

	def literalsql(self, context, command):
		cs = self.connectstring()

		if not command.cond:
			self.finish(f"Skipped literal SQL in {cs!r}")
			return None

		sql = command._sql_for_execute()
		sql = self._touchup_sql(sql)
		self.connection.cursor().execute(sql)
		command.finish(f"Executed literal SQL in {cs!r}")
		command.count(cs)

	def procedure(self, context, command):
		cs = self.connectstring()

		if not command.cond:
			command.finish(f"Skipped procedure {command.name!r} in {cs!r}")
			return None

		query = self._create_query(command)
		result = self._executesql(context, query, command.args, command.argtypes)
		if result:
			command.log(f"Vars {result!r}")
		command.finish(f"Called procedure {command.name!r} in {cs!r}")
		command.count(cs, command.name)
		return result or None

	def sql(self, context, command):
		cs = self.connectstring()

		if not command.cond:
			command.finish(f"Skipped SQL in {cs!r}")
			return None

		result = self._executesql(context, command.sql, command.args, command.argtypes)
		if result:
			command.log(f"Vars {result!r}")
		command.finish(f"Executed SQL in {cs!r}")
		command.count(cs)
		return result or None

	def reset_sequence(self, context, command):
		cs = self.connectstring()

		if not command.cond:
			command.finish(f"Skipped resetting sequence {command.sequence!r} in {cs!r}")
			return None

		command.log(f"Resetting sequence {command.sequence} in {cs!r}")

		seqvalue = self._reset_sequence(context, command)
		if seqvalue is not None:
			command.finish(f"Reset sequence {command.sequence} to {seqvalue!r} in {cs!r}")
		else:
			command.finish(f"Can't reset sequence {command.sequence} in {cs!r}")
		command.count(cs)
		return seqvalue


class OracleHandler(DBHandler):
	"""
	Subclass of :class:`DBHandler` that executes database commands via :mod:`cx_Oracle`.

	However :class:`drop_types` is not supported, for this :class:`OraSQLHandler`
	is required, which requires that :mod:`ll.orasql` is available).
	"""

	def connectstring(self):
		return f"oracle:{self.connection.username}@{self.connection.dsn}"

	def _touchup_sql(self, sql):
		if sql.endswith((";", "/")):
			sql = sql[:-1]
		return sql

	def user_exists(self, context, command):
		cursor = self.connection.cursor()
		cursor.execute("select count(*) from all_users where username = :name", name=command.name)
		command.count(self.connectstring())
		return cursor.fetchone()[0] > 0

	schema_exists = user_exists

	def object_exists(self, context, command):
		cursor = self.connection.cursor()
		if command.owner is None:
			cursor.execute("select count(*) from user_objects where object_name = :name", name=command.name)
		else:
			cursor.execute("select count(*) from all_objects where owner = :owner and object_name = :name", owner=command.owner, name=command.name)
		command.count(self.connectstring())
		return cursor.fetchone()[0] > 0

	def constraint_exists(self, context, command):
		cursor = self.connection.cursor()
		if command.owner is None:
			cursor.execute("select count(*) from user_constraints where constraint_name = :name", name=command.name)
		else:
			cursor.execute("select count(*) from all_constraints where owner = :owner and constraint_name = :name", owner=command.owner, name=command.name)
		command.count(self.connectstring())
		return cursor.fetchone()[0] > 0

	def check_errors(self, context, command):
		cs = self.connectstring()

		if not command.cond:
			self.finish(f"Skipped error checking in {cs!r}")
			return None

		command.log(f"Checking errors in {cs!r}")
		cursor = self.connection.cursor()
		cursor.execute("select lower(type), name from user_errors group by lower(type), name")
		invalid_objects = [tuple(r) for r in cursor]

		if invalid_objects:
			raise CompilationError(invalid_objects)
		command.finish(f"No errors in {cs!r}")
		command.count(cs)
		return 0

	def _reset_sequence(self, context, command):
		cursor = self.connection.cursor()

		# Fetch information about the sequence
		cursor.execute("select min_value, increment_by from user_sequences where lower(sequence_name)=lower(:name)", name=command.sequence)
		oldvalues = cursor.fetchone()
		if oldvalues is None:
			raise ValueError(f"Sequence {command.sequence!r} unknown")
		(minvalue, increment) = oldvalues
		cursor.execute(f"select {command.sequence}.nextval from dual")
		seqvalue = cursor.fetchone()[0]

		# Fetch information about the table values
		cursor.execute(f"select nvl(max({command.field}), 0) from {command.table}")
		tabvalue = cursor.fetchone()[0]

		step = max(tabvalue, minvalue) - seqvalue
		if step:
			cursor.execute(f"alter sequence {command.sequence} increment by {step}")
			cursor.execute(f"select {command.sequence}.nextval from dual")
			seqvalue = cursor.fetchone()[0]
			cursor.execute(f"alter sequence {command.sequence} increment by {increment}")
			return seqvalue
		else:
			return None

	@staticmethod
	def _createvar(cursor, type, value):
		var = cursor.var(type)
		var.setvalue(0, value)
		return var

	def _executesql(self, context, query, args, argtypes):
		cursor = self.connection.cursor()

		queryargvars = {}
		varargs = {}
		for (argname, argvalue) in args.items():
			if isinstance(argvalue, sqlexpr):
				continue # no value
			if isinstance(argvalue, var):
				varargs[argname] = argvalue
				if argvalue.key is not None and argvalue.key in context._locals:
					argvalue = self._createvar(cursor, argvalue.type, context._locals[argvalue.key])
				else:
					argvalue = cursor.var(argvalue.type)
			elif isinstance(argvalue, str) and len(argvalue) >= 4000:
				argvalue = self._createvar(cursor, cx_Oracle.DB_TYPE_CLOB, argvalue)
			elif isinstance(argvalue, bytes) and len(argvalue) >= 4000:
				argvalue = self._createvar(cursor, cx_Oracle.DB_TYPE_BLOB, argvalue)
			queryargvars[argname] = argvalue

		cursor.execute(query, queryargvars)

		keys = {}
		for (argname, argvalue) in varargs.items():
			value = queryargvars[argname].getvalue(0)
			if argvalue.key is not None and (argvalue.key not in context._locals or context._locals[argvalue.key] != value):
				keys[argname] = value
				context._locals[argvalue.key] = value
		return keys

	def _create_query(self, command):
		argsql = ", ".join(f"{an}=>{av.expression}" if isinstance(av, sqlexpr) else f"{an}=>:{an}" for (an, av) in command.args.items())
		query = f"begin {command.name}({argsql}); end;"
		return query


class OraSQLHandler(OracleHandler):
	"""
	Subclass of :class:`DBHandler` that executes database commands via :mod:`ll.orasql`.
	"""

	def drop_types(self, context, command):
		cs = self.connectstring()

		if not command.cond:
			command.finish(f"Skipped dropping types in {cs!r}")
			return None

		if command.drop is not None:
			dropstr = " ".join(command.drop)
			command.log(f"Dropping {dropstr} in {cs!r}")
		elif command.keep is not None:
			keepstr = " ".join(command.keep)
			command.log(f"Dropping everything except {keepstr} in {cs!r}")
		else:
			command.log(f"Dropping everything in {cs!r}")

		cursor = self.connection.cursor()
		count = 0
		for (i, obj) in enumerate(self.connection.objects(owner=None, mode="drop")):
			if obj.owner is None:
				drop = False
				if command.drop is not None and obj.type in command.drop:
					drop = True
				if command.keep is not None and obj.type not in command.keep:
					drop = True
				if drop:
					ddl = obj.dropsql(self.connection, False)
					if ddl:
						cursor.execute(ddl)
						count += 1
		command.finish(f"Dropped {count:,} objects from {cs!r}")
		command.count(cs)
		return count


class PostgresHandler(DBHandler):
	"""
	Subclass of :class:`DBHandler` that executes database commands for Postgres.
	"""

	def connectstring(self):
		info = self.connection.info
		host = "localhost" if info.host.startswith("/") else info.host
		result = f"postgres:{info.user}@{host}"
		if info.port != 5432:
			result += f":{info.port}"
		if info.user != info.dbname:
			result += f"/{info.dbname}"
		return result

	def user_exists(self, context, command):
		cs = self.connectstring()
		cursor = self.connection.cursor(row_factory=rows.tuple_row)
		cursor.execute("select count(*) from pg_user where usename = %s", (command.name,))
		count = cursor.fetchone()[0]
		command.count(cs)
		return count > 0

	def schema_exists(self, context, command):
		cs = self.connectstring()
		cursor = self.connection.cursor(row_factory=rows.tuple_row)
		cursor.execute("select count(*) from pg_namespace where nspname = %s", (command.name,))
		count = cursor.fetchone()[0]
		command.count(cs)
		return count > 0

	def object_exists(self, context, command):
		cs = self.connectstring()
		cursor = self.connection.cursor(row_factory=rows.tuple_row)
		candidates = [
			("pg_class", "relname"),
			("pg_proc", "proname"),
		]
		for (table, column) in candidates:
			cursor.execute(f"select count(*) from pg_catalog.{table} where {column} = %s", (command.name,))
			count = cursor.fetchone()[0]
			if count:
				command.count(cs)
				return True
		command.count(cs)
		return False

	def constraint_exists(self, context, command):
		cs = self.connectstring()

		cursor = self.connection.cursor(row_factory=rows.tuple_row)

		cursor.execute(f"select count(*) from pg_catalog.pg_constraint where conname = %s", (command.name,))
		count = cursor.fetchone()[0]
		command.count(cs)
		return count > 0

	def check_errors(self, context, command):
		# We can't check for any errors in Postgres
		raise NotImplementedError()

	def _reset_sequence(self, context, command):
		cursor = self.connection.cursor(row_factory=rows.tuple_row)

		# Fetch information about the table values
		cursor.execute(f"select coalesce(max({command.field}), 0) from {command.table}")
		tabvalue = cursor.fetchone()[0]

		# Find min value
		cursor.execute("select seqmin from pg_catalog.pg_sequence where seqrelid = %s::regclass", (command.sequence,))
		minvalue = cursor.fetchone()[0]

		if tabvalue > minvalue:
			# Reset sequence
			cursor.execute(f"alter sequence {command.sequence} restart with {tabvalue}")
			# Increment sequence once so the next time we get a value hight that that
			cursor.execute(f"select nextval('{command.sequence}')")
			curvalue = cursor.fetchone()[0]
			return curvalue
		else:
			# We can't set the current value lower than the minimum value, so skip it
			return None

	def drop_types(self, context, command):
		# Currently no implemented
		raise NotImplementedError()

	def _executesql(self, context, sql, args, argtypes):
		queryargvars = {}
		varargs = {}
		for (argname, argvalue) in args.items():
			if isinstance(argvalue, sqlexpr):
				continue # no value
			elif isinstance(argvalue, var):
				varargs[argname] = argvalue
				if argvalue.key is not None and argvalue.key in context._locals:
					argvalue = context._locals[argvalue.key]
				else:
					argvalue = None
			queryargvars[argname] = argvalue

		cursor = self.connection.cursor(row_factory=rows.dict_row)
		cursor.execute(sql, queryargvars)
		keys = {}
		try:
			result = cursor.fetchone()
		except psycopg.ProgrammingError as exc:
			# The procedure call might not have had any out parameters
			if not exc.args or exc.args[0] not in {"no results to fetch", "no result available", "the last operation didn't produce a result"}:
				# some other problem -> report it
				raise
		else:
			for (column_name, value) in result.items():
				if column_name in varargs:
					# We have a ``var`` argument for that value
					key = varargs[column_name].key
				else:
					# This was probably a simple ``select``, so store the result directly
					key = column_name
				if key is not None and (key not in context._locals or context._locals[key] != value):
					keys[column_name] = value
					context._locals[key] = value
		return keys

	def _create_query(self, command):
		allargssql = []
		for (an, av) in command.args.items():
			if isinstance(av, sqlexpr):
				argsql = f"{an}=>{av.expression}"
			else:
				argsql = f"{an}=>%({an})s"
			if an in command.argtypes:
				argsql += f"::{command.argtypes[an]}"
			allargssql.append(argsql)
		allargssql = ", ".join(allargssql)
		query = f"call {command.name}({allargssql})"
		return query


###
### Command classes
###

class Command:
	"""
	The base class of all commands. A :class:`Command` object is created from a
	function call in a PySQL file and then immediatly the method :meth:`execute`
	will be called to execute the command.

	The only parameters in the call that is supported by all commands are the
	following:

	``raise_exceptions`` : bool (optional)
		Specifies whether exceptions that happen during the execution of the
		command should be reported and terminate the script (:const:`True`), or
		should be ignored (:const:`False`). :const:`None` (the default)
		uses the global configuration.

	``cond`` : bool (optional)
		Specifies whether this command should be executed or not.
		If ``cond`` is :const:`True` (the default), the command will be executed,
		else it won't.
	"""

	def __init__(self, *, raise_exceptions=None, cond=True):
		self.location = None
		self.raise_exceptions = raise_exceptions
		self.cond = cond
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
		if self.location.startline is not None and self.location.endline is not None:
			result += f" :: {self.location._lines()}"
		return result

	def finish(self, message):
		self._message = message

	def count(self, *keys):
		self._counter = keys

	def log(self, *objects):
		self._context.log(self, *objects)

	def execute(self, context):
		# Forward the call to the handler method with the same name as our class
		return getattr(context.handlers[-1], self.__class__.__name__)(context, self)

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

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, filename, *, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.filename = filename

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} filename={self.filename!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(self.filename, raise_exceptions=self.raise_exceptions)


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
		The connection mode: This can be either ``'sysdba'`` or :const:`None`
		(the default).

	``retry`` : int (optional)
		The number of times PySQL tries to get a database connection.

	``retrydelay`` : int (optional)
		The number of seconds to wait between connection tries.

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, connectstring, *, mode=None, retry=None, retrydelay=None, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		if not connectstring.startswith(("oracle:", "postgres:")):
			connectstring = "oracle:" + connectstring
		self.connectstring = connectstring
		self.mode = mode
		self.retry = retry
		self.retrydelay = retrydelay

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} connectstring={self.connectstring!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			connectstring=self.connectstring,
			mode=self.mode,
			retry=self.retry,
			retrydelay=self.retrydelay,
			raise_exceptions=self.raise_exceptions,
		)


@register
class disconnect(Command):
	"""
	The :class:`!disconnect` command disconnects from the active database
	connection and reverts back to the previously active database connection.

	``commit`` specifies whether the transaction should be committed. If
	``commit`` is :const:`None`, the default commit mode is used (which can be
	changed on the command line via the ``-r``/``--rollback`` option).

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, *, commit=None, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.commit = commit

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} commit={self.commit!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			commit=self.commit,
			raise_exceptions=self.raise_exceptions,
		)


class _DatabaseCommand(Command):
	"""
	Base class of all commands that use a database connection.
	"""


class _SQLCommand(_DatabaseCommand):
	"""
	Common base class of :class:`procedure` and :class:`sql`.
	"""


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
			to the procedure. The type of the variable defaults to :class:`int`.
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

	``argtypes`` : dictionary (optional)
		A dictionary with the names of the parameters as keys and Postgres
		datatypes as the values. This is used for adding a cast to the parameter
		value in the call to guide Postgres to find the correct overloaded
		version of the procedure. For Oracle ``argtypes`` will be ignored.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, name, *, raise_exceptions=None, cond=True, args=None, argtypes=None):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.name = name
		self.args = args or {}
		self.argtypes = argtypes or {}

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.name,
			raise_exceptions=self.raise_exceptions,
			args=self.args if self.args else None,
			argtypes=self.argtypes if self.argtypes else None,
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

	``argtypes`` : dictionary (optional)
		A dictionary with the names of the parameters as keys and Postgres
		datatypes as the values. This is used for adding a cast to the parameter
		value in the call to try to convert the value to the proper Postgres
		datatype. For Oracle ``argtypes`` will be ignored.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.

	If you have arguments you can reference them in Oracle code like this::

		sql(
			"insert into foo (bar) values (:bar)",
			args=dict(
				bar="bar",
			)
		)

	or (if you want to use a variable) like this::

		sql(
			"insert into foo (bar) values (:bar)",
			args=dict(
				bar=var("bar", str),
			)
		)

	Or like this when you wnat to get a value out from an SQL command::

		sql(
			"begin; :now := to_char(sysdate); end;",
			args=dict(
				now=var("now", date),
			)
		)

	For Postgres you must reference parameters in the query like this::

		sql(
			"insert into foo (bar) values (%(bar)s)",
			args=dict(
				bar="bar",
			)
		)

	or (if you want to use a variable) like this::

		sql(
			"insert into foo (bar) values (%(bar)s)",
			args=dict(
				bar=var("bar", str),
			)
		)

	However to get variables out of a Postgres SQL statement you must use
	a ``select``::

		sql(
			"select baz as baz from foo where bar = %(bar)s",
			args=dict(
				bar=var("bar", str),
			)
		)

	Specify the target variable name via the output name of the field
	expressions.

	In the about example a variable ``baz`` will be set.
	"""

	def __init__(self, sql, *, raise_exceptions=None, cond=True, args=None, argtypes=None):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.sql = sql
		self.args = args or {}
		self.argtypes = argtypes or {}

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sql={self.sql!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.sql,
			raise_exceptions=self.raise_exceptions,
			args=self.args if self.args else None,
			argtypes=self.argtypes if self.argtypes else None,
		)


@register
class literalsql(_SQLCommand):
	"""
	A :class:`!literalsql` is used for SQL that appears literally in the
	PySQL file. Apart from the ``sql`` attribute it supports no further
	parameters.
	"""

	def __init__(self, sql):
		super().__init__()
		self.sql = sql

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sql={self.sql!r} location={self.location} at {id(self):#x}>"

	def _sql_for_execute(self):
		sql = self.sql
		if self.location is not None:
			# Prepend empty lines, so in case of an exception the
			# linenumbers from any database stacktrace match
			sql = (self.location.startline-1) * "\n" + self.sql
		return sql

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

	def __init__(self, *, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			raise_exceptions=self.raise_exceptions,
		)


@register
class rollback(_SQLCommand):
	"""
	A :class:`!rollback` command rolls back the current transaction in the
	activate database connection (or the one specified via the ``connection``
	parameter).

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, *, raiseexceptions=None, cond=True):
		super().__init__(raiseexceptions=raiseexceptions, cond=cond)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			raise_exceptions=self.raise_exceptions,
		)


class literalpy(_DatabaseCommand):
	"""
	A :class:`!literalpy` is used for Python code that appears literally in the
	PySQL file. Apart from the ``code`` attribute it supports the no further
	parameters.
	"""

	def __init__(self, code):
		super().__init__()
		prefix = f"{Context.literalpy_begin}\n"
		suffix = f"\n{Context.literalpy_end}"
		testcode = code.strip()
		if not testcode.startswith(prefix) or not testcode.endswith(suffix):
			raise ValueError(f"{self.__class__.__qualname__} code must start with {prefix!r} and end with {suffix!r}")
		self.code = code

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} code={self.code!r} location={self.location} at {id(self):#x}>"

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

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, name, value, *, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.name = name
		self.value = value

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} value={self.value!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.name,
			self.value,
			raise_exceptions=self.raise_exceptions,
		)


@register
class unsetvar(Command):
	"""
	The :class:`!unsetvar` command deletes a variable. The parameter ``name``
	must be given and must contain the name of the variable.

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, name, *, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.name = name

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.name,
			raise_exceptions=self.raise_exceptions,
		)


@register
class raise_exceptions(Command):
	"""
	The :class:`!raise_exceptions` command changes the global error reporting mode
	for all subsequent commands. After::

		raise_exceptions(False)

	for all subsequent commands any exception will be ignored and reported and
	command execution will continue with the next command. ::

		raise_exceptions(True)

	will switch back to aborting the execution of the PySQL script once an
	exception is encountered.

	Note that the global configuration will only be relevant for commands that
	don't specify the ``raise_exceptions`` parameter themselves.

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, value, *, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.value = value

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} value={self.value!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.value,
			raise_exceptions=self.raise_exceptions,
		)


@register
class push_raise_exceptions(Command):
	"""
	The :class:`!push_raise_exceptions` command changes the global error
	reporting mode for all subsequent commands, but remembers the previous
	exception handling mode. After::

		push_raise_exceptions(False)

	for all subsequent commands any exception will be ignored and reported and
	command execution will continue with the next command. It is possible to
	switch back to the previous exception handling mode via::

		pop_raise_exceptions()

	Note that this global configuration will only be relevant for commands that
	don't specify the ``raise_exceptions`` parameter themselves.

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, value, *, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.value = value

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} value={self.value!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.value,
			raise_exceptions=self.raise_exceptions,
		)


@register
class pop_raise_exceptions(Command):
	"""
	The :class:`pop_raise_exceptions` command restores the previously
	active exception handling mode (i.e. the one active before the last
	:class:`push_raise_exceptions` command).

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, *, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			raise_exceptions=self.raise_exceptions,
		)


@register
class check_errors(_DatabaseCommand):
	"""
	The :class:`!check_errors` command checks that there are no compilation errors
	in the active database schema. If there are, an exception will be raised.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`
	(but the value of the ``raise_exceptions`` key will be ignored).
	"""

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

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

	``content`` : bytes (required)
		The content of the file to be created. This can also be a
		:class:`loadbytes` command to load the content from an external file.

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, *, name, content, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.name = name
		self.content = content

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} content={shortrepr(self.content)} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.name,
			self.content,
			raise_exceptions=self.raise_exceptions,
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

	``content`` : bytes (required)
		The content of the file to be created. This can also be a
		:class:`loadbytes` command to load the content from an external file.

	``mode`` : integer (optional)
		The file mode for the new file. If the mode is specified, :func:`os.chmod`
		will be called on the file.

	``owner`` : integer or string (optional)
		The owner of the file (as a user name or a uid).

	``group`` : integer or string (optional)
		The owning group of the file (as a group name or a gid).
		If ``owner`` or ``group`` is given, :func:`os.chown` will be called on
		the file.

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, name, content, *, mode=None, owner=None, group=None, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.name = name
		self.content = content
		self.mode = mode
		self.owner = owner
		self.group = group

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} content={shortrepr(self.content)} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.name,
			self.content,
			mode=self.mode,
			owner=self.owner,
			group=self.group,
			raise_exceptions=self.raise_exceptions,
		)


@register
class reset_sequence(_DatabaseCommand):
	"""
	The :class:`!reset_sequence` command resets a sequence in the database to
	the maximum value of a field in a table. The following parameters are
	supported:

	``sequence`` : string (required)
		The name of the sequence to reset.

	``table`` : string (required)
		The name of the table that contains the field.

	``field`` : string (required)
		The name of the field in the table ``table``. The sequence will be
		reset to a value so that fetching the next value from the sequence
		will deliver a value that is larger than the maximum value of the field
		``field`` in the table ``table``.

	``minvalue`` : integer (optional, default taken from sequence)
		The minimum value for the sequence.

	``increment`` : integer (optional, default taken from sequence)
		The increment (i.e. the step size) for the sequence.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, sequence, table, field, *, minvalue=None, increment=None, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.sequence = sequence
		self.table = table
		self.field = field

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} sequence={self.sequence!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.sequence,
			self.table,
			self.field,
			minvalue=self.minvalue,
			increment=self.increment,
			connection=self.connection,
			raise_exceptions=self.raise_exceptions,
		)


@register
class user_exists(_DatabaseCommand):
	"""
	The :class:`!user_exists` command returns whether a user with a specified
	name exists in the database. It supports the following parameters:

	``name`` : string (required)
		The name of the user to be checked for existence.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, name, *, raise_exceptions=None):
		super().__init__(raise_exceptions=raise_exceptions)
		self.name = name

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.name,
			raise_exceptions=self.raise_exceptions,
		)


@register
class schema_exists(_DatabaseCommand):
	"""
	The :class:`!schema_exists` command returns whether a schema with a specified
	name exists in the database. It supports the following parameters:

	``name``: string (required)
		The name of the schema to be checked for existence.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, name, *, raise_exceptions=None):
		super().__init__(raise_exceptions=raise_exceptions)
		self.name = name

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.name,
			raise_exceptions=self.raise_exceptions,
		)


@register
class object_exists(_DatabaseCommand):
	"""
	The :class:`!object_exists` command returns whether an object with a
	specified name exists in the database. It supports the following parameters:

	``name`` : string (required)
		The name of the object to be checked for existence.

	``owner`` : string (optional)
		The owner of the object (defaults to the current user if not specified
		or :const:`None`).

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.

	Note that :class:`!object_exists` won't test for constraints. For this use
	:class:`constraint_exists`.
	"""

	def __init__(self, name, *, owner=None, raise_exceptions=None):
		super().__init__(raise_exceptions=raise_exceptions)
		self.name = name
		self.owner = owner

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.name,
			owner=self.owner,
			raise_exceptions=self.raise_exceptions,
		)


@register
class constraint_exists(_DatabaseCommand):
	"""
	The :class:`!constraint_exists` command returns whether a constraint (i.e.
	a primary key, foreign key, unique or check constraint) with a specified name
	exists in the database. It supports the following parameters:

	``name`` : string (required)
		The name of the object to be checked for existence.

	``owner`` : string (optional)
		The owner of the constraint (defaults to the current user if not specified
		or :const:`None`).

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, name, *, owner=None, raise_exceptions=None):
		super().__init__(raise_exceptions=raise_exceptions)
		self.name = name
		self.owner = owner

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} name={self.name!r} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.name,
			owner=self.owner,
			raise_exceptions=self.raise_exceptions,
		)


@register
class drop_types(_DatabaseCommand):
	"""
	The :class:`!drop_types` command drops database objects.

	Unlike all other commands this command requires the :mod:`ll.orasql` module.

	:class:`!drop_types` supports the following parameters:

	``drop`` : list of strings (optional)
		The types of objects to drop (value must be names for :mod:`ll.orasql`
		object types.

	``keep`` : list of strings (optional)
		The types of objects to keep (value must be names for :mod:`ll.orasql`
		object types.

	``drop`` and ``keep`` are mutually exclusive. When neither of them
	is specified *all* database objects will be dropped.

	For the rest of the parameters see the base class :class:`_DatabaseCommand`.
	"""

	def __init__(self, *, drop=None, keep=None, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.drop = drop
		self.keep = keep

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} location={self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			drop=self.drop,
			keep=self.keep,
			raise_exceptions=self.raise_exceptions,
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

	``filename`` : string (required)
		The name of the file to be loaded. The filename is treated as being
		relative to the directory containing the PySQL file that contains
		:class:`loadbytes` command.

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, filename, *, raise_exceptions=None, cond=True):
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
		self.filename = filename

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} filename={self.filename!r} {self.location} at {id(self):#x}>"

	def source_format(self):
		yield from self._source_format(
			self.filename,
			raise_exceptions=self.raise_exceptions,
		)


@register
class loadstr(Command):
	"""
	The :class:`!loadstr` command can be used to load a :class:`str` object
	from an external file. The following parameters are supported:

	``filename`` : string (required)
		The name of the file to be loaded. The filename is treated as being
		relative to the directory containing the PySQL file that contains the
		:class:`!loadstr` command.

	``encoding`` : string (optional)
		The encoding used for decoding the bytes in the file to text.

	``errors`` : string (optional)
		The error handling mode for decoding.

	For the parameters ``raise_exceptions`` and ``cond`` see the base class
	:class:`Command`.
	"""

	def __init__(self, filename, *, encoding=None, errors="strict", raise_exceptions=None, cond=True):
		"""
		Create a new :class:`loadstr` object. 
		"""
		super().__init__(raise_exceptions=raise_exceptions, cond=cond)
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

	def source_format(self):
		yield from self._source_format(
			self.filename,
			encoding=self.encoding,
			errors=self.errors if self.errors != "strict" else None,
			raise_exceptions=self.raise_exceptions,
		)


@register
class var(Command):
	"""
	:class:`var` commands are used to mark procedure values that are ``OUT``
	parameters. On first use the parameter is used as an ``OUT`` parameter and
	PySQL will remembers the OUT value as a local variable under the unique name
	specified in the constructor. When a :class:`var` object is used a second
	time a variable object will be passed to the procedure with it's value set
	to the value of the local variable. The following parameters are supported:

	``key`` : string (required)
		A unique name for the value.

	``type`` : class (optional)
		The type of the value (defaulting to :class:`int`).

	Note that when the ``key`` is :const:`None`, PySQL will *not* remember
	the value, instead each use of ``var(None)`` will create a new OUT
	parameter. This can be used for OUT parameters whose values is not
	required by subsequent commands.
	"""

	def __init__(self, key=None, type=int):
		super().__init__(raise_exceptions=None)
		self.key = key
		self.type = type

	def __repr__(self):
		if self.type is int:
			return f"var({self.key!r})"
		else:
			return f"var({self.key!r}, {format_class(self.type)})"

	def __bool__(self):
		return False

	def source_format(self):
		yield repr(self)


@register
class env(Command):
	"""
	A :class:`env` command returns the value of an environment variable.

	The following parameters are supported:

	``name`` : string (required)
		The name of the environment variable.

	``default`` : string (optional)
		The default to use, if the environment variable isn't set.
		This defaults to :const:`None`.
	"""

	def __init__(self, name, default=None):
		super().__init__()
		self.name = name
		self.default = default

	def __repr__(self):
		return f"env({self.name!r})"

	def source_format(self):
		yield repr(self)


@register
class log(Command):
	"""
	:class:`log` commands generate logging output.

	The following parameters are supported:

	``objects`` : Any
		The objects to log. Strings will be logged directly. For all other
		objects :func:`repr` will be called.
	"""

	def __init__(self, *objects):
		super().__init__()
		self.objects = objects

	def source_format(self):
		yield from self._source_format(*self.objects)


class CommandExecutor:
	"""
	A :class:`!CommandExecutor` object wraps executing a :class:`Command` object
	in a callable. Calling the :class:`!CommandExecutor` object executes the
	command using the specified context and returns the command result.

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
		command = self.command(*args, **kwargs) # Create the :class:`Command` object
		context = self.context
		command._context = context
		command.location = context._location
		command._starttime = datetime.datetime.now()
		if context._runstarttime is None:
			context._runstarttime = command._starttime
		context.totalcount += 1
		command._nr = context.totalcount
		if command.raise_exceptions is not None:
			context.raise_exceptions.append(command.raise_exceptions)

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
		# Update ``_lastlocation`` *now*, so that other commands called during :meth:`execute` don't print the location/source twice
		context._lastlocation = command.location

		try:
			result = command.execute(context)
		except Exception as exc:
			command._stoptime = datetime.datetime.now()
			if context.raise_exceptions[-1]:
				if context.verbose:
					print(flush=True)
				raise
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
			if command.raise_exceptions is not None:
				context.raise_exceptions.pop()
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

	def __init__(self, connectstring=None, scpdirectory="", filedirectory="", commit=True, tabsize=None, context=None, ascii=False, raise_exceptions=True, verbose=0, summary=False, vars=None):
		self.handlers = [Handler.from_connectstring(None)]
		self.commit = commit
		self.scpdirectory = scpdirectory
		self.filedirectory = pathlib.Path(filedirectory).resolve()
		self.basedirectory = pathlib.Path.cwd().resolve()
		self.homedirectory = pathlib.Path.home().resolve()
		self.tabsize = tabsize
		self.context = context
		self.ascii = ascii
		if ascii:
			self.char_vrule = "|"
			self.char_fathrule = "="
			self.char_hrule = "-"
			self.char_hruledown = "-"
			self.char_hruleup = "-"
			self.char_vellipsis = "..."
		else:
			self.char_vrule = "\u2502"
			self.char_fathrule = "\u2501"
			self.char_hrule = "\u2500"
			self.char_hruledown = "\u252c"
			self.char_hruleup = "\u2534"
			self.char_vellipsis = "\u22ee"
		self.raise_exceptions = [raise_exceptions]
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

		for fd in range(3):
			try:
				self._width = os.get_terminal_size(fd)[0]
			except OSError:
				pass
			else:
				break
		else:
			self._width = 80

		self._locals = dict(vars) if vars else {}
		self._locals["sqlexpr"] = sqlexpr
		self._locals["datetime"] = datetime
		self._locals["connection"] = None
		self._locals["DB_TYPE_CLOB"] = cx_Oracle.DB_TYPE_CLOB
		self._locals["DB_TYPE_NCLOB"] = cx_Oracle.DB_TYPE_NCLOB
		self._locals["DB_TYPE_BLOB"] = cx_Oracle.DB_TYPE_BLOB
		for command in Command.commands.values():
			self._locals[command.__name__] = CommandExecutor(command, self)

		if connectstring is not None:
			self.push_handler(Handler.from_connectstring(connectstring))

	def push_handler(self, handler):
		self.handlers.append(handler)
		self._locals["connection"] = handler.connection

	def pop_handler(self):
		if self.handlers:
			self.handlers.pop()
		self._locals["connection"] = self.handlers[-1].connection if self.handlers else None

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

	def hrule(self, width):
		return self.char_hrule * width

	@contextlib.contextmanager
	def changed_filename(self, filename):
		filename = pathlib.Path(filename).resolve()
		oldfilename = self.filename
		self.filename = filename
		oldcwd = pathlib.Path.cwd()
		os.chdir(filename.parent)
		try:
			yield pathlib.Path(filename.name)
		finally:
			self.filename = oldfilename
			os.chdir(oldcwd)

	def _load(self, stream):
		"""
		Load a PySQL file from ``stream`` and executes the commands in the file.
		``stream`` must be an iterable over lines that contain the PySQL
		commands.
		"""
		self._locals["connection"] = self.handlers[-1].connection if self.handlers else None

		def blocks():
			# ``state`` is the state of the "parser", values have the following meaning
			# :const:`None`: outside of any block
			# ``literalsql``: inside of literal SQL block
			# ``literalpy``: inside of literal Python block
			# ``dict``: inside of Python dict literal
			# others: inside a PySQL command of that name
			state = None
			lines = []
			for (i, line) in enumerate(stream, 1):
				line = line.rstrip()
				if state is None:
					if line.startswith("{"):
						lines.append((i, line))
						state = "dict"
						if line.endswith("}"):
							yield (state, lines)
							lines  = []
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
							yield (state, lines)
							lines  = []
							state = None
					elif line:
						lines.append((i, line))
						state = "literalsql"
				elif state == "dict":
					lines.append((i, line))
					if line == "}": # A single unindented ``}``
						yield (state, lines)
						lines  = []
						state = None
				elif state == "literalsql":
					if line.startswith(self.terminator):
						yield (state, lines)
						lines  = []
						state = None
					else:
						lines.append((i, line))
				elif state == "literalpy":
					lines.append((i, line))
					if line == self.literalpy_end:
						yield (state, lines)
						lines  = []
						state = None
				else:
					# Inside any of the PySQL commands as a function call
					lines.append((i, line))
					if line == self.command_end: # A single unindented ``)``
						yield (state, lines)
						lines  = []
						state = None
			if lines:
				yield (state, lines)

		for (state, lines) in blocks():
			# Drop empty lines at the start
			while lines and not lines[0][1].strip():
				del lines[0]
			# Drop empty lines at the end
			while lines and not lines[-1][1].strip():
				del lines[-1]
			if lines:
				self._location = Location(stream.name, lines)
				if self.verbose == "full":
					# Print the source code here, before the command gets instantiated,
					# so that we'll see the source even when an exception happens
					# on instantiation
					self._location.print_source(self)
				source = self._location.source()
				if state == "literalsql":
					CommandExecutor(literalsql, self)(source)
				elif state == "literalpy":
					CommandExecutor(literalpy, self)(source)
				elif state == "dict":
					code = compile(source, str(self._location.filename), "eval")
					args = eval(code, self._locals)
					type = args.pop("type", "procedure")
					if type not in Command.commands:
						raise ValueError(f"command type {type!r} unknown")
					CommandExecutor(Command.commands[type], self)(**args)
				else:
					code = compile(source, str(self._location.filename), "exec")
					exec(code, self._locals)

	def executeall(self, *filenames):
		"""
		Execute all commands in the PySQL files specified by ``filenames``.
		If ``filenames`` is empty ``sys.stdin`` is read.
		"""
		try:
			if self.verbose == "type":
				print("commands:", end="", flush=True)
			elif self.verbose == "file":
				print("files:", end="", flush=True)
			if filenames:
				for filename in filenames:
					with self.changed_filename(filename) as fn:
						with fn.open("r") as f:
							self._load(f)
			else:
				self._load(sys.stdin)
			for handler in self.handlers:
				if handler.connection is not None:
					if self.commit:
						handler.connection.commit()
					else:
						handler.connection.rollback()
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
				print(self.char_fathrule*self._width, flush=True)
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
			else:
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

class NoDatabaseError(Exception):
	def __str__(self):
		return f"no database connection"


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
	Exception raised by :class:`check_errors` when invalid database
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
		self.filename = pathlib.Path(filename).resolve()
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

	def source(self):
		source = "\n".join(line for (linenumber, line) in self.lines)
		if self.startline is not None:
			# Prepend empty lines, so in case of an exception the
			# linenumbers in the stacktrace match
			source = (self.startline-1) * "\n" + source
		return source

	def print_source(self, context):
		if self.startline and self.endline:
			startline = self.startline
			endline = self.endline
			linenumberlen = len(f"{self.endline:,}")
			filename = context.strfilename(self.filename)
			filenamelen = len(filename)
			ruletop    = f"{context.hrule(linenumberlen + 1)}{context.char_hruledown}[ {filename} ]{context.hrule(context._width - 2 - linenumberlen - 4 - filenamelen)}"
			rulebottom = f"{context.hrule(linenumberlen + 1)}{context.char_hruleup}{context.hrule(context._width - 2 - linenumberlen)}"
			print(ruletop, flush=True)

			linenumberellipsis = context.char_vellipsis[:linenumberlen]
			for (linenumber, line) in self.lines:
				if context.context is not None and startline + context.context <= linenumber <= endline - context.context:
					if startline + context.context == linenumber:
						print(f"{linenumberellipsis:>{linenumberlen}} {context.char_vrule} {context.char_vellipsis}", flush=True)
				else:
					if context.tabsize is not None:
						line = line.expandtabs(context.tabsize)
					print(f"{linenumber:{linenumberlen},} {context.char_vrule} {line}", flush=True)
			print(rulebottom, flush=True)
		else:
			endline = len(self.lines) - 1
			rule = context.hrule(context._width)
			print(rule, flush=True)
			for (linenumber, line) in self.lines:
				if context.context is not None and context.context <= linenumber <= endline - context.context:
					if context.context == linenumber:
						print(context.char_vellipsis, flush=True)
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
			return (name, None)
		try:
			return (name, int(value))
		except ValueError:
			raise argparse.ArgumentTypeError(f"{value!r} is not a legal integer value")
	elif type == "float":
		if not value:
			return (name, 0.)
		try:
			return (name, float(value))
		except ValueError:
			raise argparse.ArgumentTypeError(f"{value!r} is not a legal float value")
	elif type == "bool":
		if value in ("", "0", "no", "false", "False"):
			return (name, False)
		elif value in ("1", "yes", "true", "True"):
			return (name, True)
		else:
			raise argparse.ArgumentTypeError(f"{value!r} is not a legal bool value")
	elif type and type != "str":
		raise argparse.ArgumentTypeError(f"{type!r} is not a legal type")
	return (name, value)


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
		for (i, value) in enumerate(object):
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

class SetDictEntryAction(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		getattr(namespace, self.dest)[values[0]] = values[1]


def main(args=None):
	p = argparse.ArgumentParser(description="Import a PySQL file into an Oracle and/or Postgres database", epilog="For more info see http://python.livinglogic.de/pysql.html")
	p.add_argument("files", nargs="*", help="PySQL files (none: read from stdin)")
	p.add_argument("-d", "--database", dest="connectstring", metavar="CONNECTSTRING", help="Oracle or Postgres connect string specifying the default database connection (default %(default)s)", default=None)
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", choices=("dot", "type", "file", "log", "full"))
	p.add_argument("-r", "--rollback", dest="rollback", help="Should database transactions be rolled back? (default: commit on disconnect/after run)", default=False, action="store_true")
	p.add_argument("-s", "--scpdirectory", dest="scpdirectory", metavar="DIR", help="File name prefix for files to be copied via the 'scp' command (default: current directory)", default="")
	p.add_argument("-f", "--filedirectory", dest="filedirectory", metavar="DIR", help="File name prefix for files to be copied via the 'file' command (default: current directory)", default="")
	p.add_argument(      "--tabsize", dest="tabsize", metavar="INTEGER", help="Number of spaces a tab expands to when printing source (default %(default)r)", type=int, default=8)
	p.add_argument(      "--context", dest="context", metavar="INTEGER", help="Maximum number of context lines when printing source code (default %(default)r)", type=int, default=None)
	p.add_argument("-a", "--ascii", dest="ascii", help="Don't use fancy unicode characters?", default=False, action="store_true")
	p.add_argument("-z", "--summary", dest="summary", help="Output a summary after executing all commands", default=False, action="store_true")
	p.add_argument("-D", "--define", dest="defines", metavar="VARSPEC", help="Set variables before executing the script (can be specified multiple times). The format for VARSPEC is: 'name' or 'name=value' or 'name:type' or 'name:type=value'. Type may be 'str', 'bool', 'int' or 'float'.", default={}, action=SetDictEntryAction, type=define)

	args = p.parse_args(args)

	context = Context(
		connectstring=args.connectstring,
		scpdirectory=args.scpdirectory,
		filedirectory=args.filedirectory,
		commit=not args.rollback,
		tabsize=args.tabsize,
		context=args.context,
		ascii=args.ascii,
		verbose=args.verbose,
		summary=args.summary,
		vars=args.defines
	)
	context.executeall(*args.files)


if __name__ == "__main__":
	sys.exit(main())
