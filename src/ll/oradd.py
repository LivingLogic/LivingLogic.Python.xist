# -*- coding: utf-8 -*-
# cython: language_level=3

## Copyright 2012-2014 by LivingLogic AG, Bayreuth/Germany
## Copyright 2012-2014 by Walter Dörwald
##
## All Rights Reserved
##
## See LICENSE for the license

r"""
:mod:`oradd` can be used to import data into an Oracle database. The data is
imported executing various "oradd commands" (like "execute a procedure",
"copy a file" etc.) that as specified in the ``oradd`` file.

Basic usage
-----------

Creating an ``oradd`` file can be done like this::

	with open("data.oradd", "w", encoding="utf-8") as f:
		data = dict(
			type="procedure",
			name="person_insert",
			keys=["per_id"],
			args=dict(
				per_id="per_id_max",
				per_firstname="Max",
				per_lastname="Mustermann",
			),
		)
		print(repr(data), file=f)

		data = dict(
			type="procedure",
			name="contact_insert",
			keys=["per_id", "con_id"],
			args=dict(
				con_id="con_id_max",
				per_id="per_id_max",
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

So the content of the generated file ``data.oradd`` will look like this::

	{'name': 'person_insert', 'keys': ['per_id'], 'args': {'per_id': 'per_id_max', 'per_firstname': 'Max', 'per_lastname': 'Mustermann'}}
	{'name': 'contact_insert', 'keys': ['per_id', 'con_id'], 'args': {'per_id': 'per_id_max', 'con_id': 'con_id_max', 'con_type': 'email', 'con_value': 'max@example.org'}}
	{'type': 'file', 'name': 'portrait_{per_id_max}.png', 'content': b'\x89PNG\r\n\x1a\n...'}
	{'type': 'resetsequence', 'sequence': 'person_seq', 'table': 'person', 'field': 'per_id'}

i.e. it's just one Python ``repr`` of a dictionary per line.

This file can then be imported into an Oracle database with the following
command::

	python oradd.py user/pwd@database data.pydd

This will import two records, one by calling ``person_insert`` and one by
calling ``contact_insert``. The PL/SQL equivalent of the above is::

	declare
		v_per_id integer;
		v_con_id integer;
	begin
		person_insert(
			per_id=v_per_id,
			per_firstname='Max',
			per_lastname='Mustermann'
		);
		contact_insert(
			con_id=v_con_id,
			per_id=v_per_id,
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
		'name': 'person_insert',
		'args': {
			'per_id': 'per_id_max',
			'per_firstname': 'Max',
			'per_lastname': 'Mustermann',
			'per_created': 'sysdate'
		},
		'keys': ['per_id'],
		'sqls': ['per_created'],
	}

The keys in the dictionary have the following meaning:

	``type`` : string (optional)
		This is either ``"procedure"`` (the default), ``"sql"``, ``"file"`` or
		``"resetsequence"``.

For type ``"procedure"`` the following additional keys are used:

	``name`` : string (required)
		The name of the procedure to be called.

	``args`` : dictionary (required)
		A dictionary with the names of the parameters as keys and the parameter
		values as values.

	``keys`` : list (optional)
		A list of parameter names that should be treated as keys. The value of the
		parameter is a integer or string identifer that is unique for each use of
		the key. On first use the parameter is used as an ``OUT`` parameter where
		the procedure will store the value of this key. On subsequent uses of this
		key (i.e. a key that has the same identifier) oradd will pass the value
		from the first use as a normal ``IN`` parameter. The ``keys`` key is
		optional, without it no parameter will be treated as a key. ``keys`` may
		also be a dictionary, with the identifiers as the keys and values the names
		of Python types. This can be used for out parameters that are not integers.

	``sqls`` : list (optional)
		A list of parameter names that should be treated as SQL expressions.
		In the example above the parameter ``per_created`` will not be the string
		``"sysdate"``, but the result of the Oracle PL/SQL ``sysdate`` function.
		The ``sqls`` key is optional, without it no parameter will be treated as
		an SQL expression.

For type ``"sql"`` the following additional keys are used:

	``sql`` : string (required)
		The SQL to be executed. This may contain parameters in the form
		``:paramname``. The values for those parameters will be taken from
		``args``.

	``args`` : dictionary (required)
		A dictionary with the names of the parameters as keys and the parameter
		values as values.

	``keys`` : list (optional)
		A list of parameter names that should be treated as keys. The value of the
		parameter is an integer or string identifer that is unique for each use of
		the key. On first use the parameter is used as an ``OUT`` parameter where
		the procedure will store the value of this key. On subsequent uses of this
		key (i.e. a key that has the same identifier) oradd will pass the value
		from the first use as a normal ``IN`` parameter. The ``keys`` key is
		optional, without it no parameter will be treated as a key. ``keys`` may
		also be a dictionary, with the identifiers as the keys and values the names
		of Python types. This can be used for out parameters that are not integers.

For type ``"file"`` the following additional keys are used:

	``name`` : string (required)
		The name of the file to be created. It may contain ``format()`` style
		specifications containing any key that appeared in a ``"procedure"`` or
		``"sql"`` record. These specifiers will be replaced by the correct
		key values. These files will be copied via ``ssh``, so ssh file names can
		be used.

	``content``: bytes (required)
		The content of the file to be created.

For type ``"resetsequence"`` the following additional keys are used:

	``sequence``: string (required)
		The name of the sequence to reset. The sequence will be reset to the
		maximum value of a field in a table.

	``table``: string (required)
		The name of the table that contains the field.

	``field``: string (required)
		The name of the field in the table ``table``. The sequence will be reset
		to a value, so that fetching the next value from the sequence will deliver
		a value that is larger than the maximum value of the field ``field`` in the
		table ``table``.

	``minvalue``: integer (optional, default 10)
		The minimum value for the sequence.

	``increment``: integer (optional, default 10)
		The increment (i.e. the stop size) for the sequence.

An oradd file in UL4ON format contains the same dictionaries, but not as a
Python repr output, but in UL4ON format. The UL4ON dump is *not* a list of
dictionaries, but simple concatenated dumps of each dictionary. When importing
this format ``oradd`` will simply read dumps from the file until the end of file
is reached. UL4ON format does not support files (because UL4ON can't represent
bytes).


Usage as a script
-----------------

``oradd.py`` has no external dependencies (except for :mod:`cx_Oracle`) and can
be used as a script for importing an oradd dump into the database. As a script
it supports the following command line options:

	``connectstring``
		An Oracle connectstring.

	``file``
		The name of the file from which the oradd dump is read. If ``file`` isn't
		specified the dump is read from ``stdin``.

	``-f``, ``--format``
		The format of the dump file: Either ``oradd`` (the default) or ``ul4on``.

	``-v``, ``--verbose``
		Gives different levels of output while data is imported to the database.
		Possible levels are: ``0`` (no output), ``1`` (a dot for each procedure
		call), ``2`` (like ``1``, plus a summary of which procedure has been
		called how often), ``3`` (detailed output for each procedure call, plus
		summary)

	``-c``, ``--commit``
		Specifies when to commit database transactions. ``record`` commit after
		every procedure call. ``once`` at the end of the script and ``never`` rolls
		back the transaction after all imports.
"""

# We're importing ``datetime``, so that it's available to ``eval()``
import sys, os, io, argparse, operator, collections, datetime, tempfile, subprocess

import cx_Oracle


__docformat__ = "reStructuredText"


class Key(object):
	"""
	:class:`Key` instances are used to mark procedure values that are
	primary/foreign keys. On first use the parameter is used as an ``OUT``
	parameter and the procedure stores the value of the newly created primary key
	in this parameter. When a :class:`Key` object is used a second time its value
	will be passed to the procedure as normal ``IN`` parameters.
	"""

	seq = 0

	def __init__(self):
		self._value = self.__class__.seq
		self.__class__.seq += 1

	def value(self):
		return self._value


class SQL(object):
	"""
	An :class:`SQL` object can be used to specify an SQL expression as a
	procedure parameter instead of a fixed value (e.g. passing the current
	date (i.e. the date of the import) can be done with ``SQL("sysdate")``).
	"""

	def __init__(self, expression):
		self.expression = expression

	def value(self):
		return self.expression


def dump(name, **kwargs):
	"""
	Return the dump format for calling the procedure ``name`` with the parameters
	``kwargs``.

	``kwargs`` may contain :class:`Key` and :class`SQL` instances.
	"""
	keys = [key for (key, value) in kwargs.items() if isinstance(value, Key)]
	sqls = [key for (key, value) in kwargs.items() if isinstance(value, SQL)]
	for (key, value) in kwargs.items():
		if isinstance(value, (Key, SQL)):
			kwargs[key] = value.value()
	result = dict(name=name, args=kwargs)
	if keys:
		result["keys"] = keys
	if sqls:
		result["sqls"] = sqls
	return result


def dumps_oradd(name, **kwargs):
	"""
	Return the dump of a procedure call to the procedure named ``name`` with the
	parameters ``kwargs`` in oradd native format as a string.
	"""
	return "{!r}\n".format(dump(name, **kwargs))


def dump_oradd(stream, name, **kwargs):
	"""
	Dump a procedure call to the procedure named ``name`` with the parameters
	``kwargs`` into the output stream ``stream`` in oradd native format.
	"""
	stream.write(repr(dump(name, **kwargs)))
	stream.write("\n")


def dumps_ul4on(name, **kwargs):
	"""
	Return the dump of a procedure call to the procedure named ``name`` with the
	parameters ``kwargs`` in UL4ON format as a string.
	"""
	from ll import ul4on
	return ul4on.dumps(dump(name, **kwargs))


def dump_ul4on(stream, name, **kwargs):
	"""
	Dump a procedure call to the procedure named ``name`` with the parameters
	``kwargs`` into the output stream ``stream`` in UL4ON format.
	"""
	from ll import ul4on
	ul4on.dump(dump(name, **kwargs), stream)


def loads_oradd(string):
	"""
	Load an oradd dump in oradd native format from the string ``string``.

	This function is a generator. It's output can be passed to :func:`importdata`.
	"""
	for line in string.splitlines():
		if line != "\n":
			yield eval(line)


def load_oradd(stream):
	"""
	Load an oradd dump in oradd native format from the stream ``stream``.

	This function is a generator. It's output can be passed to :func:`importdata`.
	"""
	for line in stream:
		if line != "\n":
			yield eval(line)


def loads_ul4on(string):
	"""
	Load an oradd dump in UL4ON format from the string ``string``.

	This function is a generator. It's output can be passed to :func:`importdata`.
	"""
	from ll import ul4on
	stream = io.StringIO(string)
	while True:
		try:
			yield ul4on.load(stream)
		except EOFError:
			break


def load_ul4on(stream):
	"""
	Load an oradd dump in UL4ON format from the stream ``stream``.

	This function is a generator. It's output can be passed to :func:`importdata`.
	"""
	from ll import ul4on
	while True:
		try:
			yield ul4on.load(stream)
		except EOFError:
			break


def _formatprocedurecall(record, allkeys):
	args = []
	keys = set(record.get("keys", []))
	sqls = set(record.get("sqls", []))
	for (argname, argvalue) in record["args"].items():
		if argname in keys:
			if argvalue is None:
				args.append("{}=None".format(argname))
			elif argvalue in allkeys:
				args.append("{}={}=<{}>".format(argname, allkeys[argvalue], argvalue))
			else:
				args.append("{}=<{}>".format(argname, argvalue))
		elif argname in sqls:
			args.append("{}={}".format(argname, argvalue))
		else:
			args.append("{}={!r}".format(argname, argvalue))
	return "{}({})".format(record["name"], ", ".join(args))


def _formatsql(record, allkeys):
	args = []
	keys = set(record.get("keys", []))
	sqls = set(record.get("sqls", []))
	for (argname, argvalue) in record["args"].items():
		if argname in keys:
			if argvalue is None:
				args.append("{}=None".format(argname))
			elif argvalue in allkeys:
				args.append("{}={}=<{}>".format(argname, allkeys[argvalue], argvalue))
			else:
				args.append("{}=<{}>".format(argname, argvalue))
		elif argname in sqls:
			args.append("{}={}".format(argname, argvalue))
		else:
			args.append("{}={!r}".format(argname, argvalue))
	return "{!r} with args {}".format(record["sql"], ", ".join(args))


def _executesql(sql, args, keys, sqls, cursor, allkeys):
	queryargvars = {}
	for (argname, argvalue) in args.items():
		if argname in keys:
			if argvalue is None:
				queryargvars[argname] = None
			elif argvalue in allkeys:
				queryargvars[argname] = allkeys[argvalue]
			else:
				queryargvars[argname] = cursor.var(keys[argname])
		elif argname in sqls:
			pass # no value
		elif isinstance(argvalue, str) and len(argvalue) >= 4000:
			var = cursor.var(cx_Oracle.CLOB)
			var.setvalue(0, argvalue)
			queryargvars[argname] = var
		else:
			queryargvars[argname] = argvalue

	cursor.execute(sql, queryargvars)

	newkeys = {}
	for (argname, argvalue) in args.items():
		if argname in keys and argvalue is not None and argvalue not in allkeys:
			newkeys[argname] = allkeys[argvalue] = queryargvars[argname].getvalue(0)
	return newkeys


def importrecord(record, cursor, allkeys):
	"""
	Import the ``procedure`` record :var:`record` into the database. ``cursor``
	must be a :mod:`cx_Oracle` cursor.
	"""
	name = record["name"]
	args = record["args"]
	if "keys" in record:
		keys = record["keys"]
		if isinstance(keys, list):
			keys = dict.fromkeys(keys, int)
		else:
			keys = {key: eval(value) for (key, value) in keys.items()}
	else:
		keys = {}
	sqls = set(record.get("sqls", []))
	queryargvalues = {}
	for (argname, argvalue) in args.items():
		if argname in keys:
			queryargvalues[argname] = ":{}".format(argname)
		elif argname in sqls:
			queryargvalues[argname] = argvalue
			# no value
		elif isinstance(argvalue, str) and len(argvalue) >= 4000:
			queryargvalues[argname] = ":{}".format(argname)
		else:
			queryargvalues[argname] = ":{}".format(argname)

	sql = "begin {}({}); end;".format(name, ", ".join("{}=>{}".format(*argitem) for argitem in queryargvalues.items()))
	return _executesql(sql, args, keys, sqls, cursor, allkeys)


def copyfile(name, content, allkeys, directory):
	with tempfile.NamedTemporaryFile(delete=False) as f:
		f.write(content)
		tempname = f.name
	try:
		name = directory + name.format(**allkeys)
		return subprocess.call(["scp", "-q", tempname, name])
	finally:
		os.remove(tempname)


def resetsequence(cursor, sequence, table, field, minvalue, increment):
	cursor.execute("select nvl(max({}), {}) from {}".format(field, minvalue, table))
	tabvalue = cursor.fetchone()[0]
	cursor.execute("select {}.nextval from dual".format(sequence))
	seqvalue = cursor.fetchone()[0]
	cursor.execute("alter sequence {} increment by {}".format(sequence, max(minvalue, tabvalue-seqvalue)))
	cursor.execute("select {}.nextval from dual".format(sequence))
	seqvalue = cursor.fetchone()[0]
	cursor.execute("alter sequence {} increment by {}".format(sequence, increment))
	return seqvalue


def importsql(record, cursor, allkeys):
	"""
	Execute the SQL from the ``sql`` record :var:`record`. ``cursor`` must
	be a :mod:`cx_Oracle` cursor.
	"""
	sql = record["sql"]
	args = record.get("args", {})
	if "keys" in record:
		keys = record["keys"]
		if isinstance(keys, list):
			keys = dict.fromkeys(keys, int)
		else:
			keys = {key: eval(value) for (key, value) in keys.items()}
	else:
		keys = {}
	sqls = set(record.get("sqls", []))
	return _executesql(sql, args, keys, sqls, cursor, allkeys)


def main(args=None):
	p = argparse.ArgumentParser(description="Import an oradd dump to an Oracle database", epilog="For more info see http://www.livinglogic.de/Python/oradd/index.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("file", nargs="?", help="Name of dump file (default: read from stdin)", type=argparse.FileType("r"), default=sys.stdin)
	p.add_argument("-f", "--format", dest="format", help="Format of the dumpfile ('oradd' or 'ul4on') (default %(default)s)", default="oradd", choices=("oradd", "ul4on"))
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", type=int, default=2, choices=(0, 1, 2, 3))
	p.add_argument("-c", "--commit", dest="commit", help="When should database transactions be committed? (default %(default)s)", default="once", choices=("record", "once", "never"))
	p.add_argument("-d", "--directory", dest="directory", metavar="DIR", help="Base directory for files to be copied via scp (default current directory)", default="")

	args = p.parse_args(args)

	db = cx_Oracle.connect(args.connectstring)

	try:
		allkeys = {}
		counts = collections.Counter()
		countfiles = 0
		countsequences = 0
		countsqls = 0
		loader = dict(oradd=load_oradd, ul4on=load_ul4on)[args.format]
		cursor = db.cursor()
		for (i, record) in enumerate(loader(args.file), 1):
			type = record.get("type", "procedure")
			if args.verbose >= 1:
				if args.verbose >= 3:
					if type == "procedure":
						sys.stdout.write("#{}: procedure {}".format(i, _formatprocedurecall(record, allkeys)))
					elif type == "sql":
						sys.stdout.write("#{}: sql {}".format(i, _formatsql(record, allkeys)))
					elif type == "file":
						sys.stdout.write("#{}: file {}".format(i, record["name"].format(**allkeys)))
					elif type == "resetsequence":
						sys.stdout.write("#{}: resetting sequence {} to maximum value from {}.{}".format(i, record["sequence"], record["table"], record["field"]))
					else:
						raise ValueError("unknown command type {!r}".format(type))
				else:
					sys.stdout.write(".")
				sys.stdout.flush()
			if type == "procedure":
				newkeys = importrecord(record, cursor, allkeys)
				if args.commit == "record":
					db.commit()
				if args.verbose >= 3:
					if newkeys:
						sys.stdout.write(" -> {}\n".format(", ".join("{}={!r}".format(argname, argvalue) for (argname, argvalue) in newkeys.items())))
					else:
						sys.stdout.write("\n")
				sys.stdout.flush()
				counts[record["name"]] += 1
			elif type == "sql":
				newkeys = importsql(record, cursor, allkeys)
				if args.commit == "record":
					db.commit()
				if args.verbose >= 3:
					if newkeys:
						sys.stdout.write(" -> {}\n".format(", ".join("{}={!r}".format(argname, argvalue) for (argname, argvalue) in newkeys.items())))
					else:
						sys.stdout.write("\n")
				sys.stdout.flush()
				countsqls += 1
			elif type == "file":
				copyfile(record["name"], record["content"], allkeys, args.directory)
				if args.verbose >= 3:
					sys.stdout.write(" -> {} bytes written\n".format(len(record["content"])))
					sys.stdout.flush()
				countfiles += 1
			elif type == "resetsequence":
				newvalue = resetsequence(cursor, sequence=record["sequence"], table=record["table"], field=record["field"], minvalue=record.get("minvalue", 10), increment=record.get("increment", 10))
				if args.verbose >= 3:
					sys.stdout.write(" -> reset to {}\n".format(newvalue))
					sys.stdout.flush()
				countsequences += 1
		if args.commit == "once":
			db.commit()
		elif args.commit == "never":
			db.rollback()
	finally:
		if args.verbose >= 3:
			print()

	if args.verbose >= 2:
		totalcount = sum(counts.values())
		l1 = len(str(max(totalcount, countfiles, countsequences, countsqls)))
		l2 = max(len(procname) for procname in counts) if counts else 0
		print()
		print("Summary")
		print("=======")
		if totalcount:
			print("{:>{}} procedure".format("#", l1))
			print("{} {}".format("-"*l1, "-"*l2))
			for (procname, count) in sorted(counts.items(), key=operator.itemgetter(1)):
				print("{:>{}} {}".format(count, l1, procname))
			print("{} {}".format("-"*l1, "-"*l2))
			print("{:>{}} (total calls)".format(totalcount, l1))
		if countfiles:
			print("{:>{}} (files)".format(countfiles, l1))
		if countsequences:
			print("{:>{}} (sequences)".format(countsequences, l1))
		if countsqls:
			print("{:>{}} (sqls)".format(countsqls, l1))


if __name__ == "__main__":
	sys.exit(main())
