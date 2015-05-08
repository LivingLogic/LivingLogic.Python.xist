# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2012-2015 by LivingLogic AG, Bayreuth/Germany
## Copyright 2012-2015 by Walter Dörwald
##
## All Rights Reserved
##
## See LICENSE for the license

"""
The module/script :mod:`pysql` can be used to import data into an Oracle
database. It reads ``pysql`` files which are variant of normal Oracle SQL files.

There are two aspects to these files:

*	A pysql file may contains normal SQL commands. For the :mod:`pysql` script
	to be able to execute these commands they must be separated with a comment
	line that starts with ``-- @@@``. :mod:`pysql` will strip of a trailing ``;``
	or ``/`` from the command and execute it. Any exception that is raised as a
	result of executing the command will stop the script and be reported. This
	is in contrast to how ``sqlplus`` executes SQL command. ``sqlplus`` would
	continue after an error and exit with status code 0 even if there were
	errors. It is also possible to explicitely ignore any exception produced by
	executing an SQL command by separating the command with ``-- !!!`` from the
	command before (instead of ``-- @@@``).

	A ``pysql`` file that only contains SQL commands is still a valid SQL file
	from the perspective of Oracle, so it still can be executed via ``sqlplus``.

*	A pysql file may also contain PySQL commands. A PySQL command looks likes a
	Python dictionary literal. The keys in the dictionary have the following
	meaning:

	``type`` : string (optional)
		This is either ``"procedure"`` (the default), ``"sql"``, ``"file"``,
		``"scp"``, ``"resetsequence"``, ``"include"``, ``"compileall"`` or
		``"checkerrors"``.

	The type ``"procedure"`` calls on Oracle procedure in the database.
	The following additional keys are used:

		``name`` : string (required)
			The name of the procedure to be called.

		``args`` : dictionary (optional)
			A dictionary with the names of the parameters as keys and the parameter
			values as values. ``pysql`` supports all types as values that
			:mod:`cx_Oracle` supports. In addition to those, two special classes are
			supported: :class:`sql` objects can be used to specify that the paramater
			should be literal SQL. So e.g. ``sql("sysdate")`` will be the date when
			the ``pysql`` script was executed. :class:`var` objects can be used to
			hold values that are ``OUT`` parameter of the procedure. For example
			on first use of ``var("foo_10")`` the value of the ``OUT`` parameter
			will be stored under the key ``"foo_10"``. The next time
			``var("foo_10")`` is encountered the value stored under the key
			``"foo_10"`` will be passed to the procedure. The type of the variable
			defaults to ``int``. If a different type is required it can be passed
			as the second argument to :class:`var`, e.g.
			``var("foo_10", datetime.datetime)``.

	The type ``"sql"`` directly executes an SQL statement in the Oracle database.
	The following additional keys are used:

		``sql`` : string (required)
			The SQL to be executed. This may contain parameters in the form of
			``:paramname``. The values for those parameters will be taken from
			``args``.

		``args`` : dictionary (optional)
			A dictionary with the names of the parameters as keys and the parameter
			values as values. Similar to procedure calls :class:`var` objects are
			supported to. However :class:`sql` objects are not supported (they will
			be ignored).

	The type ``"scp"`` creates a file by copying it via the ``scp`` command.
	The following additional keys are used:

		``name`` : string (required)
			The name of the file to be created. It may contain ``format()`` style
			specifications containing any key that appeared in a ``"procedure"`` or
			``"sql"`` record. These specifiers will be replaced by the correct
			key values. As these files will be copied via the ``scp`` command, ssh
			file names can be used.

		``content``: bytes (required)
			The content of the file to be created.

	The type ``"file"`` creates a file by directly saving it from Python.
	The following additional keys are used:

		``name`` : string (required)
			The name of the file to be created. It may contain ``format()`` style
			specifications containing any key that appeared in a ``"procedure"`` or
			``"sql"`` record. These specifiers will be replaced by the correct
			key values.

		``content``: bytes (required)
			The content of the file to be created.

		``mode``: integer (optional)
			The file mode for the new file. If the mode is specified
			:func:`os.chmod` will be called on the file.

		``owner``: integer or string (optional)
			The owner of the file (as a user name or a uid).

		``group``: integer or string (optional)
			The owning group of the file (as a group name or a gid).
			If ``owner`` or ``group`` is given, :func:`os.chown` will be called on
			the file.

	The type ``"resetsequence"`` resets a sequence in the Oracle database to the
	maximum value of a field in a table. The following additional keys are used:

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

	The type ``"setvar"`` sets a variable to a fixed value. The following
	additional keys are used:

		``var``: string (required)
			The name of the variable to set.

		``value``: (required)
			The value of the variable.

	The type ``"include"`` includes another pysql file. The filename is read
	from the key ``"name"``. This name is interpreted as being relative to the
	directory with the file containing the ``include`` command.

	The type ``"checkerrors"`` checks that there are no compilation errors in the
	target schema. If there are an exception will be raised.

	The type ``"compileall"`` will recompile all objects in the schema.


Example
-------

The following is a complete pysql file that will create a sequence, table and
procedure and will call the procedure to insert data into the table:

	-- @@@

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

	-- @@@ recompile everything

	{
		'type': 'compileall'
	}

	-- @@@ check that everything compiled OK

	{
		'type': 'checkerrors'
	}

	-- @@@ person: insert a person

	{
		'type': 'procedure',
		'name': 'person_insert',
		'args': {
			'per_id': var('per_id_max'),
			'per_firstname': 'Max',
			'per_lastname': 'Mustermann',
		}
	}

	-- @@@ contact: insert a contact for the person

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

	-- @@@ save a file for the person

	{
		'type': 'file',
		'name': 'portrait_{per_id_max}.png',
		'content': b'\\x89PNG\\r\\n\\x1a\\n...',
	}

	-- @@@ reset the sequence

	{
		'type': 'resetsequence',
		'sequence': 'person_seq',
		'table': 'person',
		'field': 'per_id',
	}

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


Importing a ``pysql`` file
--------------------------

``pysql.py`` has no external dependencies (except for :mod:`cx_Oracle`) and can
be used as a script for importing a pysql file into the database. As a script
it supports the following command line options:

	``connectstring``
		An Oracle connectstring.

	``file``
		The name of the pysql file that will be read and imported. If ``file``
		isn't specified the commands are read from ``stdin``.

	``-v``, ``--verbose``
		Gives different levels of output while data is being imported to the
		database. Possible levels are: ``0`` (no output), ``1`` (one letter for
		each command), ``2`` (like ``1``, plus a summary of which command has been
		executed how often and which procedures have been called how often), ``3``
		(detailed output for each command/procedure call, plus summary)

	``-c``, ``--commit``
		Specifies when to commit database transactions. ``record`` commits after
		every command. ``once`` at the end of the script and ``never`` rolls back
		the transaction after all imports.

	``-s``, ``--scpdirectory``
		The base directory for ``scp`` file copy commands. As files are copied
		via ``scp`` this can be a remote filename (like
		``ssh:root@www.example.org:uploads/``) and must include a trailing ``/``.

	``-f``, ``--filedirectory``
		The base directory for the ``file`` file save commands. It must include
		a trailing ``/``.

	``-d``, ``--delimiter``
		The delimiter comment between each command (default ``-- @@@``).

	``-D``, ``--delimiterignored``
		The delimiter comment between each command where exceptions from
		executing the following command will be ignored (default ``-- !!!``).
"""

# We're importing ``datetime``, so that it's available to ``eval()``
import sys, os, os.path, pwd, grp, argparse, operator, collections, datetime, tempfile, subprocess

import cx_Oracle


__docformat__ = "reStructuredText"


class var:
	"""
	:class:`var` instances are used to mark procedure values that are ``OUT``
	parameters. On first use the parameter is used as an ``OUT`` parameter and
	the procedure stores the value of the newly created primary key under the
	unique key specified in the constructor. When a :class:`var` object is used
	a second time its value will be passed to the procedure as a normal ``IN``
	parameters.
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


class Error(Exception):
	def __init__(self, executor, pos, command):
		self.filenames = executor.filenames()
		self.pos = pos
		self.command = command

	def __str__(self):
		if isinstance(self.command, str):
			return "{}: in literal @ lines {:,}-{:,}".format(self.filenames, self.pos[0], self.pos[1])
		elif self.command is None:
			return "{}: in lines {:,}-{:,}".format(self.filenames, self.pos[0], self.pos[1])
		else:
			return "{}: in {} command @ lines {:,}-{:,}".format(self.filenames, self.command.get("type", "procedure"), self.pos[0], self.pos[1])


class CompilationError(Exception):
	def __init__(self, count):
		self.count = count

	def __str__(self):
		if self.count == 1:
			return "1 invalid object in the database"
		else:
			return "{:,} invalid objects in the database".format(self.count)


class Executor:
	def __init__(self, db, scpdirectory="", filedirectory="", commit="once", delimiter="-- @@@", delimiterignore="-- !!!", verbose=0):
		self.keys = {}
		self.db = db
		self.cursor = db.cursor()
		self.scpdirectory = scpdirectory
		self.filedirectory = filedirectory
		self.commit = commit
		self.delimiter = delimiter
		self.delimiterignore = delimiterignore
		self.verbose = verbose
		self.count = 0
		self.commandcounts = collections.Counter()
		self.procedurecounts = collections.Counter()
		self.errorcount = 0
		self.streams = []

	def load(self, stream):
		"""
		Load a pysql file from :obj:`stream`. :obj:`stream` must be an iterable
		producing strings, that contain the ``pysql`` commands.

		This function is a generator. Its output are the ``pysql`` command
		dictionaries/literal strings.
		"""
		ignoreerrors = False
		lines = []

		def makeblock():
			# Drop empty lines at the start
			while lines and not lines[0][1].strip():
				del lines[0]
			# Drop empty lines at the end
			while lines and not lines[-1][1].strip():
				del lines[-1]
			block = "".join(line[1] for line in lines).strip()
			if block:
				pos = (lines[0][0], lines[-1][0])
				lines.clear()
				if block.endswith((";", "/")):
					yield (pos, ignoreerrors, block[:-1])
				elif block.endswith("}"):
					try:
						block = eval(block)
					except Exception as exc:
						raise Error(self, pos, block) from exc
					if block.get("type", "procedure") == "include":
						filename = block.get("name")
						if filename:
							if self.verbose in (1, 2):
								print("(", end="", flush=True)
							with open(self.relativefilename(filename), "r", encoding="utf-8") as f:
								yield from self.load(f)
							if self.verbose in (1, 2):
								print(")", end="", flush=True)
					else:
						yield (pos, ignoreerrors, block)
				else:
					raise Error(self, pos, None) from ValueError("block terminator {!r} unknown".format(block[-1:]))

		try:
			self.streams.append(stream)
			for (i, line) in enumerate(stream, 1):
				if line.startswith(self.delimiter):
					yield from makeblock()
					ignoreerrors = False
				elif line.startswith(self.delimiterignore):
					yield from makeblock()
					ignoreerrors = True
				else:
					# Collection line number and line
					lines.append((i, line))
			yield from makeblock()
		finally:
			self.streams.pop()

	def filenames(self):
		return " -> ".join(stream.name for stream in self.streams)

	def relativefilename(self, filename):
		return os.path.join(os.path.dirname(self.streams[-1].name), filename)

	def executeall(self, commands):
		try:
			for (pos, ignoreerrors, command) in commands:
				try:
					self.execute(pos, command)
				except Exception as exc:
					if ignoreerrors:
						self.errorcount += 1
						if self.verbose >= 1:
							if self.verbose >= 3:
								exctext = str(exc).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
								print(" -> ignored {}.{}: {}".format(exc.__class__.__module__, exc.__class__.__qualname__, exctext))
							elif self.verbose >= 2:
								print("!", end="", flush=True)
					else:
						raise Error(self, pos, command) from exc
				else:
					if self.verbose in (1, 2):
						print(".", end="", flush=True)
			if self.commit == "once":
				self.db.commit()
			elif self.commit == "never":
				self.db.rollback()
		finally:
			if self.verbose >= 3:
				print()
		self._printsummary()

	def execute(self, pos, command):
		result = None
		if isinstance(command, str):
			type = "literal"
			self.literal(pos, command)
		else:
			type = command.get("type", "procedure")
			if type == "procedure":
				result = self.callprocedure(pos, command)
			elif type == "sql":
				result = self.executesql(pos, command)
			elif type == "scp":
				self.scpfile(pos, command)
			elif type == "file":
				self.savefile(pos, command)
			elif type == "resetsequence":
				self.resetsequence(pos, command)
			elif type == "setvar":
				self.setvar(pos, command)
			elif type == "compileall":
				self.compileall(pos, command)
			elif type == "checkerrors":
				self.checkerrors(pos, command)
			else:
				raise ValueError("command type {!r} unknown".format(type))
			if type == "procedure":
				self.procedurecounts[command["name"]] += 1
		self.commandcounts[type] += 1
		self.count += 1
		return result

	def literal(self, pos, command):
		"""
		Execute the SQL in :obj:`command`. ``cursor`` must
		be a :mod:`cx_Oracle` cursor.
		"""
		if self.verbose >= 3:
			if len(command) > 72:
				text = "{!r}...".format(command[:72])
			else:
				text = repr(command)
			print("#{:,} in {} @ lines {:,}-{:,}: literal {}".format(self.count+1, self.filenames(), pos[0], pos[1], text), end="", flush=True)

		self.cursor.execute(command)

		if self.commit == "record":
			self.db.commit()

		if self.verbose >= 3:
			print(" -> done", flush=True)

	def callprocedure(self, pos, command):
		"""
		Import the ``procedure`` command :obj:`command` into the database.
		"""
		if self.verbose >= 3:
			print("#{:,} in {} @ lines {:,}-{:,}: procedure {}".format(self.count+1, self.filenames(), pos[0], pos[1], self._formatprocedurecall(command)), end="", flush=True)

		name = command["name"]
		args = command.get("args", {})
		queryargvalues = {}
		for (argname, argvalue) in args.items():
			if isinstance(argvalue, var):
				queryargvalues[argname] = ":{}".format(argname)
			elif isinstance(argvalue, sql):
				queryargvalues[argname] = argvalue.expression
				# no value
			elif isinstance(argvalue, str) and len(argvalue) >= 4000:
				queryargvalues[argname] = ":{}".format(argname)
			else:
				queryargvalues[argname] = ":{}".format(argname)

		query = "begin {}({}); end;".format(name, ", ".join("{}=>{}".format(*argitem) for argitem in queryargvalues.items()))
		result = self._executesql(query, args)

		if self.commit == "record":
			self.db.commit()

		if self.verbose >= 3:
			if result:
				print(" -> {}".format(", ".join("{}={!r}".format(argname, argvalue) for (argname, argvalue) in result.items())), flush=True)
			else:
				print(flush=True)
		return result

	def setvar(self, pos, command):
		"""
		Set a variable.
		"""
		var = command.get("var")
		value = command.get("value")
		if self.verbose >= 3:
			print("#{:,} in {} @ lines {:,}-{:,}: set var {!r} to {!r}".format(self.count+1, self.filenames(), pos[0], pos[1], var, value), end="", flush=True)

		self.keys[var] = value

		if self.verbose >= 3:
			print(" -> done", flush=True)

	def checkerrors(self, pos, command):
		"""
		Check that we have no compilation errors in the target schema.
		"""
		if self.verbose >= 3:
			print("#{:,} in {} @ lines {:,}-{:,}: check errors".format(self.count+1, self.filenames(), pos[0], pos[1]), end="", flush=True)

		self.cursor.execute("select count(*) from (select name from user_errors group by name, type)")
		count = self.cursor.fetchone()[0]

		if count:
			raise CompilationError(count)

		if self.verbose >= 3:
			print(" -> done", flush=True)

	def compileall(self, pos, command):
		"""
		Recompile everything in the target schema.
		"""
		if self.verbose >= 3:
			print("#{:,} in {} @ lines {:,}-{:,}: compile all".format(self.count+1, self.filenames(), pos[0], pos[1]), end="", flush=True)

		self.cursor.execute("begin dbms_utility.compile_schema(user); end;")

		if self.verbose >= 3:
			print(" -> done", flush=True)

	def executesql(self, pos, command):
		"""
		Execute the SQL from the ``sql`` command :obj:`command`
		"""
		if self.verbose >= 3:
			print("#{:,} in {} @ lines {:,}-{:,}: sql {}".format(self.count+1, self.filenames(), pos[0], pos[1], self._formatsql(command)), end="", flush=True)

		result = self._executesql(command["sql"], command.get("args", {}))

		if self.commit == "record":
			self.db.commit()

		if self.verbose >= 3:
			if result:
				print(" -> {}".format(", ".join("{}={!r}".format(argname, argvalue) for (argname, argvalue) in result.items())), flush=True)
			else:
				print(flush=True)

		return result

	def scpfile(self, pos, command):
		filename = self.scpdirectory + command["name"].format(**self.keys)

		if self.verbose >= 3:
			print("#{:,} in {} @ lines {:,}-{:,}: scp {}".format(self.count+1, self.filenames(), pos[0], pos[1], filename), end="", flush=True)

		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(command["content"])
			tempname = f.name
		try:
			return subprocess.call(["scp", "-q", tempname, filename])
		finally:
			os.remove(tempname)

		if self.verbose >= 3:
			print(" -> {} bytes written".format(len(command["content"])), flush=True)

	def savefile(self, pos, command):
		filename = self.filedirectory + command["name"].format(**self.keys)

		if self.verbose >= 3:
			print("#{:,} in {} @ lines {:,}-{:,}: file {}".format(self.count+1, self.filenames(), pos[0], pos[1], filename), end="", flush=True)

		try:
			with open(filename, "wb") as f:
				f.write(command["content"])
		except FileNotFoundError: # probably the directory doesn't exist
			(splitpath, splitname) = os.path.split(filename)
			if splitpath:
				os.makedirs(splitpath)
				with open(filename, "wb") as f:
					f.write(command["content"])
			else:
				raise # we don't have a directory to make so pass the error on

		if "mode" in "command":
			os.chmod(filename, command["mode"])
		if "owner" in "command" or "group" in command:
			if "owner" in command:
				uid = command["owner"]
				if isinstance(uid, str):
					uid = pwd.getpwnam(uid)[2]
			else:
				uid = -1
			if "group" in command:
				gid = command["group"]
				if isinstance(gid, str):
					gid = grp.getgrnam(gid)[2]
			else:
				gid = -1
			os.chown(filename, uid, gid)

		if self.verbose >= 3:
			msg = " -> {} bytes written".format(len(command["content"]))
			options = ("mode", "owner", "group")
			optionmsg = ", ".join("{} {}".format(option, oct(command[option]) if option == "mode" else repr(command[option])) for option in options if option in command)
			if optionmsg:
				msg = "{} ({})".format(msg, optionmsg)
			print(msg, flush=True)

	def resetsequence(self, pos, command):
		sequence = command["sequence"]
		table = command["table"]
		field = command["field"]
		minvalue = command.get("minvalue", None)
		increment = command.get("increment", None)

		if self.verbose >= 3:
			print("#{:,} in {} @ lines {:,}-{:,}: resetting sequence {} to maximum value from {}.{}".format(self.count+1, self.filenames(), pos[0], pos[1], sequence, table, field), end="", flush=True)

		# Fetch information about the sequence
		self.cursor.execute("select min_value, increment_by, last_number from user_sequences where lower(sequence_name)=lower(:name)", name=sequence)
		oldvalues = self.cursor.fetchone()
		if oldvalues is None:
			raise ValueError("sequence {!r} unknown".format(sequence))
		if increment is None:
			increment = oldvalues[1]
		if minvalue is None:
			minvalue = oldvalues[0]
		self.cursor.execute("select {}.nextval from dual".format(sequence))
		seqvalue = self.cursor.fetchone()[0]

		# Fetch information about the table values
		self.cursor.execute("select nvl(max({}), 0) from {}".format(field, table))
		tabvalue = self.cursor.fetchone()[0]

		step = max(tabvalue, minvalue) - seqvalue
		if step:
			self.cursor.execute("alter sequence {} increment by {}".format(sequence, step))
			self.cursor.execute("select {}.nextval from dual".format(sequence))
			seqvalue = self.cursor.fetchone()[0]
			self.cursor.execute("alter sequence {} increment by {}".format(sequence, increment))
			if self.verbose >= 3:
				print(" -> reset to {}".format(seqvalue), flush=True)
			return seqvalue
		else:
			if self.verbose >= 3:
				print(" -> no reset required", flush=True)
			return None

	def _executesql(self, query, args):
		queryargvars = {}
		for (argname, argvalue) in args.items():
			if isinstance(argvalue, var):
				if argvalue.key is None:
					queryargvars[argname] = None
				elif argvalue.key in self.keys:
					queryargvars[argname] = self.keys[argvalue.key]
				else:
					queryargvars[argname] = self.cursor.var(argvalue.type)
			elif isinstance(argvalue, sql):
				pass # no value
			elif isinstance(argvalue, str) and len(argvalue) >= 4000:
				var_ = self.cursor.var(cx_Oracle.CLOB)
				var_.setvalue(0, argvalue)
				queryargvars[argname] = var_
			else:
				queryargvars[argname] = argvalue

		self.cursor.execute(query, queryargvars)

		newkeys = {}
		for (argname, argvalue) in args.items():
			if isinstance(argvalue, var) and argvalue.key is not None and argvalue.key not in self.keys:
				newkeys[argname] = self.keys[argvalue.key] = queryargvars[argname].getvalue(0)
		return newkeys

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
			for cmdtype in ("literal", "procedure", "sql", "resetsequence", "setvar", "file", "scp"):
				if self.commandcounts[cmdtype]:
					anyoutput = True
					print("{:>{}} ({}s)".format(self.commandcounts[cmdtype], l1, cmdtype))
			if self.errorcount:
				print("{:>{}} ignored errors".format(self.errorcount, l1))
			if not anyoutput:
				print("no commands executed")

	def _formatargs(self, command):
		args = []
		if "args" in command:
			for (argname, argvalue) in command["args"].items():
				if isinstance(argvalue, var) and argvalue.key in self.keys:
					arg = "{}={!r}={!r}".format(argname, argvalue, self.keys[argvalue.key])
				else:
					arg = "{}={!r}".format(argname, argvalue)
				args.append(arg)
		return ", ".join(args)

	def _formatprocedurecall(self, command):
		return "{}({})".format(command["name"], self._formatargs(command))

	def _formatsql(self, command):
		if "args" in command and command["args"]:
			return "{!r} with args {}".format(command["sql"], self._formatargs(command))
		else:
			return repr(command["sql"])


def main(args=None):
	p = argparse.ArgumentParser(description="Import a pysql file into an Oracle database", epilog="For more info see http://www.livinglogic.de/Python/pysql/index.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("file", nargs="?", help="Name of the pysql file (default: read from stdin)", type=argparse.FileType("r"), default=sys.stdin)
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", type=int, default=2, choices=(0, 1, 2, 3))
	p.add_argument("-c", "--commit", dest="commit", help="When should database transactions be committed? (default %(default)s)", default="once", choices=("record", "once", "never"))
	p.add_argument("-s", "--scpdirectory", dest="scpdirectory", metavar="DIR", help="File name prefix for files to be copied via the 'scp' command (default: current directory)", default="")
	p.add_argument("-f", "--filedirectory", dest="filedirectory", metavar="DIR", help="File name prefix for files to be copied via the 'file' command (default: current directory)", default="")
	p.add_argument("-d", "--delimiter", dest="delimiter", metavar="STRING", help="Delimiter between each command (should be a valid SQL comment; default %(default)r)", default="-- @@@")
	p.add_argument("-D", "--delimiterignore", dest="delimiterignore", metavar="STRING", help="Delimiter between each command that ignores errors (should be a valid SQL comment; default %(default)r)", default="-- !!!")

	args = p.parse_args(args)

	db = cx_Oracle.connect(args.connectstring)

	executor = Executor(
		db=db,
		scpdirectory=args.scpdirectory,
		filedirectory=args.filedirectory,
		commit=args.commit,
		delimiter=args.delimiter,
		delimiterignore=args.delimiterignore,
		verbose=args.verbose,
	)
	executor.executeall(executor.load(args.file))


if __name__ == "__main__":
	sys.exit(main())
