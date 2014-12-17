# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2012-2014 by LivingLogic AG, Bayreuth/Germany
## Copyright 2012-2014 by Walter Dörwald
##
## All Rights Reserved
##
## See LICENSE for the license

"""
:mod:`oradd` can be used to import data into an Oracle database. The data is
imported by executing various "oradd commands" (like "execute a procedure",
"copy a file" etc.) that are specified in the ``oradd`` file.

Creating an ``oradd`` dump
--------------------------

Creating an ``oradd`` file can be done like this::

	from ll import oradd

	with open("data.oradd", "w", encoding="utf-8") as f:
		data = dict(
			type="procedure",
			name="person_insert",
			args=dict(
				per_id=oradd.var("per_id_max"),
				per_firstname="Max",
				per_lastname="Mustermann",
			),
		)
		print(repr(data), file=f)

		data = dict(
			type="procedure",
			name="contact_insert",
			args=dict(
				con_id=oradd.var("con_id_max"),
				per_id=oradd.var("per_id_max"),
				con_type="email",
				con_value="max@example.org",
			),
		)
		print(repr(data), file=f)

		data = dict(
			type="file",
			name="portrait_{per_id_max}.png",
			content=open("max.png", "rb".read()),
		)
		print(repr(data), file=f)

		data = dict(
			type="resetsequence",
			sequence="person_seq",
			table="person",
			field="per_id",
		)
		print(repr(data), file=f)

The content of the generated file ``data.oradd`` will look like this::

	{'name': 'person_insert', 'args': {'per_id': var('per_id_max'), 'per_firstname': 'Max', 'per_lastname': 'Mustermann'}}
	{'name': 'contact_insert', 'args': {'per_id': var('per_id_max'), 'con_id': var('con_id_max'), 'con_type': 'email', 'con_value': 'max@example.org'}}
	{'type': 'file', 'name': 'portrait_{per_id_max}.png', 'content': b'\\x89PNG\\r\\n\\x1a\\n...'}
	{'type': 'resetsequence', 'sequence': 'person_seq', 'table': 'person', 'field': 'per_id'}

i.e. it's just one Python ``repr`` of a dictionary per line.

This file can then be imported into an Oracle database with the following
command::

	python oradd.py user/pwd@database data.pydd

This will import two records, one by calling ``person_insert`` and one by
calling ``contact_insert``. The PL/SQL equivalent of the above is::

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


Data format
-----------

An oradd file contains one line for each "oradd command". Each line is the
``repr`` output of a Python dictionary. For example (pretty printed for display
purposes, the original format is on one line)::

	{
		'type': 'procedure',
		'name': 'person_insert',
		'args': {
			'per_id': var('per_id_max'),
			'per_firstname': 'Max',
			'per_lastname': 'Mustermann',
			'per_created': sql('sysdate')
		}
	}

The keys in the dictionary have the following meaning:

	``type`` : string (optional)
		This is either ``"procedure"`` (the default), ``"sql"``, ``"file"``,
		``"scp"`` or ``"resetsequence"``.

The type ``"procedure"`` calls on Oracle procedure in the database.
The following additional keys are used:

	``name`` : string (required)
		The name of the procedure to be called.

	``args`` : dictionary (optional)
		A dictionary with the names of the parameters as keys and the parameter
		values as values. ``oradd`` supports all types as values that
		:mod:`cx_Oracle` supports. In addition to those, two special classes are
		supported: :class:`sql` objects can be used to specify that the paramater
		should be literal SQL. So e.g. ``sql("sysdate")`` will be the date when
		the ``oradd`` script was executed. :class:`var` objects can be used to
		hold values that are ``OUT`` parameter of the procedure. For example
		on first use of ``var("foo_10")`` the value of the ``OUT`` parameter will
		be stored under the key ``"foo_10"``. The next time ``var("foo_10")`` is
		encountered the value stored under the key ``"foo_10"`` will be passed to
		the procedure. The type of the variable defaults to ``int``. If a
		different type is required it can be passed as the second argument to
		:class:`var`, e.g. ``var("foo_10", datetime.datetime)``.

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
		The file mode for the new file. If the mode is specified :func:`os.chmod`
		will be called on the file.

	``owner``: integer or string (optional)
		The owner of the file (as a user name or a uid).

	``group``: integer or string (optional)
		The owning group of the file (as a group name or a gid).
		If ``owner`` or ``group`` is given, :func:`os.chown` will be called on the
		file.

The type ``"resetsequence"`` resets a sequence in the Oracle database to the
maximum value of a field in a table. The following additional keys are used:

	``sequence``: string (required)
		The name of the sequence to reset.

	``table``: string (required)
		The name of the table that contains the field.

	``field``: string (required)
		The name of the field in the table ``table``. The sequence will be reset
		to a value, so that fetching the next value from the sequence will deliver
		a value that is larger than the maximum value of the field ``field`` in
		the table ``table``.

	``minvalue``: integer (optional, default taken from sequence)
		The minimum value for the sequence.

	``increment``: integer (optional, default taken from sequence)
		The increment (i.e. the stop size) for the sequence.

A line in an ``oradd`` dump that starts with a ``#`` will be ignored.


Importing an ``oradd`` dump
---------------------------

``oradd.py`` has no external dependencies (except for :mod:`cx_Oracle`) and can
be used as a script for importing an oradd dump into the database. As a script
it supports the following command line options:

	``connectstring``
		An Oracle connectstring.

	``file``
		The name of the file from which the oradd dump is read. If ``file`` isn't
		specified the dump is read from ``stdin``.

	``-v``, ``--verbose``
		Gives different levels of output while data is being imported to the database.
		Possible levels are: ``0`` (no output), ``1`` (a dot for each procedure
		call), ``2`` (like ``1``, plus a summary of which command has been executed
		how often and which procedure has been called how often), ``3`` (detailed
		output for each command/procedure call, plus summary)

	``-c``, ``--commit``
		Specifies when to commit database transactions. ``record`` commits after
		every command. ``once`` at the end of the script and ``never`` rolls back
		the transaction after all imports.

	``-s``, ``--scpdirectory``
		The base directory for ``scp`` file copy commands. As files are copied via
		``scp`` this can be a remote filename (like
		``ssh:root@www.example.org:uploads/``) and must include a trailing ``/``.

	``-f``, ``--filedirectory``
		The base directory for the ``file`` file save commands. It must include
		a trailing ``/``.
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


def load_oradd(iter):
	"""
	Load an oradd dump from :obj:`iter`. :obj:`iter` must be an iterable
	producing strings, that contain the ``repr`` output of ``oradd`` commands.

	This function is a generator. Its output are the ``oradd`` command
	dictionaries.
	"""
	for line in iter:
		if line != "\n" and not line.strip().startswith("#"):
			yield eval(line)


def loads_oradd(string):
	"""
	Load an oradd dump in oradd native format from the string ``string``.

	This function is a generator.
	"""
	return load_oradd(string.splitlines())


class Executor:
	def __init__(self, db, scpdirectory="", filedirectory="", commit="once", verbose=0):
		self.keys = {}
		self.db = db
		self.cursor = db.cursor()
		self.scpdirectory = scpdirectory
		self.filedirectory = filedirectory
		self.commit = commit
		self.verbose = verbose
		self.count = 0
		self.commandcounts = collections.Counter()
		self.procedurecounts = collections.Counter()

	def executeall(self, commands):
		try:
			for command in commands:
				self.execute(command)
			if self.commit == "once":
				self.db.commit()
			elif self.commit == "never":
				self.db.rollback()
		finally:
			if self.verbose >= 3:
				print()
		self._printsummary()

	def execute(self, command):
		self._fixargs(command)
		type = command.get("type", "procedure")
		result = None
		if type == "procedure":
			result = self.callprocedure(command)
		elif type == "sql":
			result = self.executesql(command)
		elif type == "scp":
			self.scpfile(command)
		elif type == "file":
			self.savefile(command)
		elif type == "resetsequence":
			self.resetsequence(command)
		else:
			raise ValueError("command type {!r} unknown".format(type))
		if type == "procedure":
			self.procedurecounts[command["name"]] += 1
		self.commandcounts[type] += 1
		self.count += 1
		return result

	def callprocedure(self, command):
		"""
		Import the ``procedure`` command :obj:`command` into the database.
		"""
		if self.verbose >= 1:
			if self.verbose >= 3:
				print("#{}: procedure {}".format(self.count+1, self._formatprocedurecall(command)), end="", flush=True)
			else:
				print(".", end="", flush=True)

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

	def executesql(self, command):
		"""
		Execute the SQL from the ``sql`` command :obj:`command`. ``cursor`` must
		be a :mod:`cx_Oracle` cursor.
		"""
		if self.verbose >= 1:
			if self.verbose >= 3:
				print("#{}: sql {}".format(self.count+1, self._formatsql(command)), end="", flush=True)
			else:
				print(".", end="", flush=True)

		result = self._executesql(command["sql"], command.get("args", {}))

		if self.commit == "record":
			self.db.commit()

		if self.verbose >= 3:
			if result:
				print(" -> {}".format(", ".join("{}={!r}".format(argname, argvalue) for (argname, argvalue) in result.items())), flush=True)
			else:
				print(flush=True)

		return result

	def scpfile(self, command):
		name = self.scpdirectory + command["name"].format(**self.keys)

		if self.verbose >= 1:
			if self.verbose >= 3:
				print("#{}: scp {}".format(self.count+1, name), end="", flush=True)
			else:
				print(".", end="", flush=True)

		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(command["content"])
			tempname = f.name
		try:
			return subprocess.call(["scp", "-q", tempname, name])
		finally:
			os.remove(tempname)

		if self.verbose >= 3:
			print(" -> {} bytes written".format(len(command["content"])), flush=True)

	def savefile(self, command):
		name = self.filedirectory + command["name"].format(**self.keys)

		if self.verbose >= 1:
			if self.verbose >= 3:
				print("#{}: file {}".format(self.count+1, name), end="", flush=True)
			else:
				print(".", end="", flush=True)

		try:
			with open(name, "wb") as f:
				f.write(command["content"])
		except FileNotFoundError: # probably the directory doesn't exist
			(splitpath, splitname) = os.path.split(name)
			if splitpath:
				os.makedirs(splitpath)
				with open(name, "wb") as f:
					f.write(command["content"])
			else:
				raise # we don't have a directory to make so pass the error on

		if "mode" in "command":
			os.chmod(name, command["mode"])
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
			os.chown(name, uid, gid)

		if self.verbose >= 3:
			msg = " -> {} bytes written".format(len(command["content"]))
			options = ("mode", "owner", "group")
			optionmsg = ", ".join("{} {}".format(option, oct(command[option]) if option == "mode" else repr(command[option])) for option in options if option in command)
			if optionmsg:
				msg = "{} ({})".format(msg, optionmsg)
			print(msg, flush=True)

	def resetsequence(self, command):
		sequence = command["sequence"]
		table = command["table"]
		field = command["field"]
		minvalue = command.get("minvalue", None)
		increment = command.get("increment", None)

		if self.verbose >= 1:
			if self.verbose >= 3:
				print("#{}: resetting sequence {} to maximum value from {}.{}".format(self.count+1, sequence, table, field), end="", flush=True)
			else:
				print(".", end="", flush=True)

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

	def _fixargs(self, command):
		if "args" in command:
			if "keys" in command:
				keys = command["keys"]
				if isinstance(keys, (list, tuple)):
					keys = dict.fromkeys(keys, int)
				else:
					keys = {key: eval(value) for (key, value) in keys.items()}
			else:
				keys = {}

			if "sqls" in command:
				sqls = set(command["sqls"])
			else:
				sqls = set()

			args = command["args"]
			for (argname, argvalue) in args.items():
				if argname in sqls:
					if isinstance(argvalue, sql):
						pass # Value already is an :class:`sql` instance
					elif isinstance(argvalue, var):
						raise TypeError("type mismatch: {!r}".format(argname))
					elif not isinstance(argvalue, str):
						raise TypeError("type mismatch: {!r}".format(argname))
					else:
						args[argname] = sql(argvalue)
				if argname in keys:
					if isinstance(argvalue, var):
						pass # Value already is a :class:`var` instance
					elif isinstance(argvalue, sql):
						raise TypeError("type mismatch: {!r}".format(argname))
					else:
						args[argname] = var(argvalue, keys[argname])

			if "keys" in command:
				del command["keys"]
			if "sqls" in command:
				del command["sqls"]

	def _printsummary(self):
		if self.verbose >= 2:
			commandcountvalues = self.commandcounts.values()
			l1 = len(str(max(commandcountvalues))) if commandcountvalues else 0
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
			for cmdtype in ("procedure", "sql", "file", "scp", "resetsequence"):
				if self.commandcounts[cmdtype]:
					anyoutput = True
					print("{:>{}} ({}s)".format(self.commandcounts[cmdtype], l1, cmdtype))
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
	p = argparse.ArgumentParser(description="Import an oradd dump to an Oracle database", epilog="For more info see http://www.livinglogic.de/Python/oradd/index.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("file", nargs="?", help="Name of dump file (default: read from stdin)", type=argparse.FileType("r"), default=sys.stdin)
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", type=int, default=2, choices=(0, 1, 2, 3))
	p.add_argument("-c", "--commit", dest="commit", help="When should database transactions be committed? (default %(default)s)", default="once", choices=("record", "once", "never"))
	p.add_argument("-s", "--scpdirectory", dest="scpdirectory", metavar="DIR", help="File name prefix for files to be copied via the 'scp' command (default: current directory)", default="")
	p.add_argument("-f", "--filedirectory", dest="filedirectory", metavar="DIR", help="File name prefix for files to be copied via the 'file' command (default: current directory)", default="")

	args = p.parse_args(args)

	db = cx_Oracle.connect(args.connectstring)

	executor = Executor(db=db, scpdirectory=args.scpdirectory, filedirectory=args.filedirectory, commit=args.commit, verbose=args.verbose)
	executor.executeall(load_oradd(args.file))


if __name__ == "__main__":
	sys.exit(main())
