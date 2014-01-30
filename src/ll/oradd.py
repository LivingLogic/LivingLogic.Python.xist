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
		the procedure. They type of the variable defaults to ``int``. If a
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
		values as values. Similar to procedure call :class:`var` objects are
		supported to. However :class:`sql` objects are not supported (they will
		be ignored).

The type ``"scp"`` creates a file by copying it via the ``scp`` command.
The following additional keys are used:

	``name`` : string (required)
		The name of the file to be created. It may contain ``format()`` style
		specifications containing any key that appeared in a ``"procedure"`` or
		``"sql"`` record. These specifiers will be replaced by the correct
		key values. As these files will be copied via the ``scp`` command, so ssh
		file names can be used.

	``content``: bytes (required)
		The content of the file to be created.

The type ``"file"`` creates a file by directly saving it from Python.
The following additional keys are used:

	``name`` : string (required)
		The name of the file to be created. It may contain ``format()`` style
		specifications containing any key that appeared in a ``"procedure"`` or
		``"sql"`` record. These specifiers will be replaced by the correct
		key values. The file will be created by scopied via ``ssh``, so ssh file names can
		be used.

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

The type ``"resetsequence"`` creset a sequence in the Oracle database to the
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

	``minvalue``: integer (optional, default 10)
		The minimum value for the sequence.

	``increment``: integer (optional, default 10)
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
		call), ``2`` (like ``1``, plus a summary of which procedure has been
		called how often), ``3`` (detailed output for each procedure call, plus
		summary)

	``-c``, ``--commit``
		Specifies when to commit database transactions. ``record`` commit after
		every procedure call. ``once`` at the end of the script and ``never`` rolls
		back the transaction after all imports.

	``-s``, ``--scpdirectory``
		The base directory for ``scp`` file copy commands. As files are copied via
		``scp`` this can be a remote filename (like
		``ssh:root@www.example.org:uploads/``) and must include a trailing ``/``.

	``-f``, ``--filedirectory``
		The base directory for ``file`` file save commands. It must include
		a trailing ``/``.
"""

# We're importing ``datetime``, so that it's available to ``eval()``
import sys, os, pwd, grp, argparse, operator, collections, datetime, tempfile, subprocess

import cx_Oracle


__docformat__ = "reStructuredText"


class var(object):
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


class sql(object):
	"""
	An :class:`sql` object can be used to specify an SQL expression as a
	procedure parameter instead of a fixed value (e.g. passing the current
	date (i.e. the date of the import) can be done with ``sql("sysdate")``).
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

	This function is a generator. It's output can be passed to :func:`importdata`.
	"""
	return load_oradd(string.splitlines())


def _formatargs(record, allkeys):
	args = []
	if "args" in record:
		for (argname, argvalue) in record["args"].items():
			if isinstance(argvalue, var) and argvalue.key in allkeys:
				arg = "{}={!r}={!r}".format(argname, argvalue, allkeys[argvalue.key])
			else:
				arg = "{}={!r}".format(argname, argvalue)
			args.append(arg)
	return ", ".join(args)


def _formatprocedurecall(record, allkeys):
	return "{}({})".format(record["name"], _formatargs(record, allkeys))


def _formatsql(record, allkeys):
	return "{!r} with args {}".format(record["sql"], _formatargs(record, allkeys))


class Executor:
	def __init__(self, db, scpdirectory="", filedirectory="", commit="once", verbose=0):
		self.keys = {}
		self.db = db
		self.cursor = db.cursor()
		self.scpdirectory = scpdirectory
		self.filedirectory = filedirectory
		self.commit = commit
		self.verbose = verbose
		self.commandcounts = collections.Counter()
		self.procedurecounts = collections.Counter()

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
		return result

	def callprocedure(self, command):
		"""
		Import the ``procedure`` command :obj:`command` into the database.
		"""
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
		return self._executesql(query, args)

	def executesql(self, command):
		"""
		Execute the SQL from the ``sql`` command :obj:`command`. ``cursor`` must
		be a :mod:`cx_Oracle` cursor.
		"""
		result = self._executesql(command["sql"], command.get("args", {}))
		if self.commit == "record":
			self.db.commit()
		return result

	def scpfile(self, command):
		name = command["name"]
		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(command["content"])
			tempname = f.name
		try:
			name = self.scpdirectory + name.format(**self.keys)
			return subprocess.call(["scp", "-q", tempname, name])
		finally:
			os.remove(tempname)

	def savefile(self, command):
		name = self.filedirectory + command["name"].format(**self.keys)
		with open(name, "wb") as f:
			f.write(command["content"])
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

	def resetsequence(self, command):
		sequence = command["sequence"]
		table = command["table"]
		field = command["field"]
		minvalue = command.get("minvalue", 10)
		increment = command.get("increment", 10)
		self.cursor.execute("select nvl(max({}), {}) from {}".format(field, minvalue, table))
		tabvalue = self.cursor.fetchone()[0]
		self.cursor.execute("select {}.nextval from dual".format(sequence))
		seqvalue = self.cursor.fetchone()[0]
		self.cursor.execute("alter sequence {} increment by {}".format(sequence, max(minvalue, tabvalue-seqvalue)))
		self.cursor.execute("select {}.nextval from dual".format(sequence))
		seqvalue = self.cursor.fetchone()[0]
		self.cursor.execute("alter sequence {} increment by {}".format(sequence, increment))
		return seqvalue

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
			l1 = len(str(max(self.commandcounts.values())))
			l2 = max(len(procname) for procname in self.procedurecounts) if self.procedurecounts else 0
			print()
			print("Summary")
			print("=======")
			if self.commandcounts["procedure"]:
				print("{:>{}} type".format("#", l1))
				print("{} {}".format("-"*l1, "-"*l2))
				for (procname, count) in sorted(self.procedurecounts.items(), key=operator.itemgetter(1)):
					print("{:>{}} {}".format(count, l1, procname))
				print("{} {}".format("-"*l1, "-"*l2))
			for cmdtype in ("procedure", "sql", "file", "scp", "resetsequence"):
				if self.commandcounts[cmdtype]:
					print("{:>{}} ({}s)".format(self.commandcounts[cmdtype], l1, cmdtype))


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

	try:
		executor = Executor(db=db, scpdirectory=args.scpdirectory, filedirectory=args.filedirectory, commit=args.commit, verbose=args.verbose)
		for (i, command) in enumerate(load_oradd(args.file), 1):
			type = command.get("type", "procedure")
			if args.verbose >= 1:
				if args.verbose >= 3:
					if type == "procedure":
						sys.stdout.write("#{}: procedure {}".format(i, _formatprocedurecall(command, executor.keys)))
					elif type == "sql":
						sys.stdout.write("#{}: sql {}".format(i, _formatsql(command, executor.keys)))
					elif type == "file":
						sys.stdout.write("#{}: file {}".format(i, command["name"].format(**executor.keys)))
					elif type == "scp":
						sys.stdout.write("#{}: scp {}".format(i, command["name"].format(**executor.keys)))
					elif type == "resetsequence":
						sys.stdout.write("#{}: resetting sequence {} to maximum value from {}.{}".format(i, command["sequence"], command["table"], command["field"]))
					else:
						raise ValueError("unknown command type {!r}".format(type))
				else:
					sys.stdout.write(".")
				sys.stdout.flush()
			result = executor.execute(command)
			if type == "procedure":
				if args.verbose >= 3:
					if result:
						sys.stdout.write(" -> {}\n".format(", ".join("{}={!r}".format(argname, argvalue) for (argname, argvalue) in result.items())))
					else:
						sys.stdout.write("\n")
				sys.stdout.flush()
			elif type == "sql":
				if args.verbose >= 3:
					if result:
						sys.stdout.write(" -> {}\n".format(", ".join("{}={!r}".format(argname, argvalue) for (argname, argvalue) in result.items())))
					else:
						sys.stdout.write("\n")
				sys.stdout.flush()
			elif type == "file":
				if args.verbose >= 3:
					sys.stdout.write(" -> {} bytes written\n".format(len(command["content"])))
					sys.stdout.flush()
			elif type == "scp":
				if args.verbose >= 3:
					sys.stdout.write(" -> {} bytes written\n".format(len(command["content"])))
					sys.stdout.flush()
			elif type == "resetsequence":
				if args.verbose >= 3:
					sys.stdout.write(" -> reset to {}\n".format(result))
					sys.stdout.flush()
		if args.commit == "once":
			db.commit()
		elif args.commit == "never":
			db.rollback()
	finally:
		if args.verbose >= 3:
			print()
	executor._printsummary()


if __name__ == "__main__":
	sys.exit(main())
