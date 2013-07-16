# -*- coding: utf-8 -*-
# cython: language_level=3

## Copyright 2012-2013 by LivingLogic AG, Bayreuth/Germany
## Copyright 2012-2013 by Walter Dörwald
##
## All Rights Reserved
##
## See LICENSE for the license

"""
:mod:`oradd` can be used to import data into an Oracle database. The data is
imported by calling stored procedures.

Basic usage
-----------

Creating an ``oradd`` file can be done like this::

	from ll import oradd

	with open("data.oradd", "w", encoding="utf-8") as f:
		per_id = oradd.Key()
		oradd.dump_oradd(
			f,
			"person_insert",
			per_id=per_id,
			per_firstname=u"Max",
			per_lastname=u"Mustermann"
		)
		oradd.dump_oradd(
			f,
			"contact_insert",
			con_id=oradd.Key(),
			per_id=per_id,
			con_type=u"email",
			con_value=u"max@example.org"
		)

The content of the generated file ``data.oradd`` will look like this::

	{'name': 'person_insert', 'keys': ['per_id'], 'args': {'per_id': 'max', 'per_firstname': 'Max', 'per_lastname': 'Mustermann'}}
	{'name': 'contact_insert', 'keys': ['per_id', 'con_id'], 'args': {'per_id': 'max', 'con_id': 'max_mail', 'con_type': 'email', 'con_value': 'max@example.org'}}
	{'type': 'file', 'name': 'protrait_{max}.png', 'content': b'\x89PNG\r\n\x1a\n...'}

i.e. it's just one Python ``repr`` of a dictionary per line.

This file can then be imported into an Oracle database with the following
command::

	python oradd.py <data.pydd user/pwd@database

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


Data format
-----------

An oradd file (in its native format) contains one line for each procedure call.
Each line is the ``repr`` output of a Python dictionary. For example (pretty
printed for display purposes, the original format is on one line)::

	{
		'name': 'person_insert',
		'args': {
			'per_id': 'max',
			'per_firstname': 'Max',
			'per_lastname': 'Mustermann',
			per_created: 'sysdate'
		},
		'keys': ['per_id'],
		'sqls': ['per_created'],
	}

The keys in this dictionary have the following meaning:

	``type`` : string (optional)
		This is either ``"procedure"`` (the default) or ``"file"``.

	``name`` : string (required)
		The name of the procedure to be called or the name of the file to be
		created. In the case of a filename the filename may contain ``format()``
		style specifications containing any key that appeared in the
		``"procedure"`` record. These specifiers will be replaced be the correct
		key values.

For type ``"procedure"`` the following additional keys are used:

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
		optional, without it no parameter will be treated as a key.

	``sqls`` : list (optional)
		A list of parameter names that should be treated as SQL expressions.
		In the example above the parameter ``per_created`` will not be the string
		``"sysdate"``, but the result of the Oracle PL/SQL ``sysdate`` function.
		The ``sqls`` key is optional, without it no parameter will be treated as
		an SQL expression.

For type ``"file"`` the following additional key is used:

	``content``: bytes (required)
		The content of the file to be created.

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
"""

# We're importing ``datetime``, so that it's available to ``eval()``
import sys, io, argparse, operator, collections, contextlib, datetime, tempfile, subprocess

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

	This function is generator. It's output can be passed to :func:`importdata`.
	"""
	for line in string.splitlines():
		yield eval(line)


def load_oradd(stream):
	"""
	Load an oradd dump in oradd native format from the stream ``stream``.

	This function is generator. It's output can be passed to :func:`importdata`.
	"""
	for line in stream:
		yield eval(line)


def loads_ul4on(string):
	"""
	Load an oradd dump in UL4ON format from the string ``string``.

	This function is generator. It's output can be passed to :func:`importdata`.
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

	This function is generator. It's output can be passed to :func:`importdata`.
	"""
	from ll import ul4on
	while True:
		try:
			yield ul4on.load(stream)
		except EOFError:
			break


def _formatcall(record, allkeys):
	args = []
	keys = set(record.get("keys", []))
	sqls = set(record.get("sqls", []))
	for (argname, argvalue) in record["args"].items():
		if argname in keys:
			if argvalue is None:
				args.append("{}=None".format(argname))
			elif argvalue in allkeys:
				args.append("{}={}".format(argname, allkeys[argvalue]))
			else:
				args.append("{}=?".format(argname))
		elif argname in sqls:
			args.append("{}={}".format(argname, argvalue))
		else:
			args.append("{}={!r}".format(argname, argvalue))
	return "{}({})".format(record["name"], ", ".join(args))


def importrecord(record, cursor, allkeys):
	"""
	Import the data ``data`` produced by :func:`loads_oradd`, :func:`load_oradd`,
	:func:`loads_ulon` or :func:`load_ul4on` into the database. ``cursor`` must
	be a :mod:`cx_Oracle` cursor.
	"""
	name = record["name"]
	args = record["args"]
	keys = set(record.get("keys", []))
	sqls = set(record.get("sqls", []))
	queryargvalues = {}
	queryargvars = {}
	for (argname, argvalue) in args.items():
		if argname in keys:
			queryargvalues[argname] = ":{}".format(argname)
			if argvalue is None:
				queryargvars[argname] = None
			elif argvalue in allkeys:
				queryargvars[argname] = allkeys[argvalue]
			else:
				queryargvars[argname] = cursor.var(int)
		elif argname in sqls:
			queryargvalues[argname] = argvalue
			# no value
		elif isinstance(argvalue, str) and len(argvalue) >= 4000:
			queryargvalues[argname] = ":{}".format(argname)
			var = cursor.var(cx_Oracle.CLOB)
			var.setvalue(0, argvalue)
			queryargvars[argname] = var
		else:
			queryargvalues[argname] = ":{}".format(argname)
			queryargvars[argname] = argvalue

	query = "begin {}({}); end;".format(name, ", ".join("{}=>{}".format(*argitem) for argitem in queryargvalues.items()))
	cursor.execute(query, queryargvars)

	newkeys = {}
	for (argname, argvalue) in args.items():
		if argname in keys and argvalue is not None and argvalue not in allkeys:
			newkeys[argname] = allkeys[argvalue] = queryargvars[argname].getvalue(0)
	return newkeys


def copyfile(name, content, allkeys):
	with tempfile.NamedTemporaryFile(delete=True) as f:
		f.write(content)
		name = name.format(**allkeys)
		return subprocess.call("scp {} {}".format(f.name, name, shell=True)


def main(args=None):
	p = argparse.ArgumentParser(description="Import an oradd dump to an Oracle database", epilog="For more info see http://www.livinglogic.de/Python/oradd/index.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("file", nargs="?", help="Name of dump file (default: read from stdin)", type=argparse.FileType("r"), default=sys.stdin)
	p.add_argument("-f", "--format", dest="format", help="Format of the dumpfile ('oradd' or 'ul4on') (default %(default)s)", default="oradd", choices=("oradd", "ul4on"))
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", type=int, default=2, choices=(0, 1, 2, 3))
	p.add_argument("-c", "--commit", dest="commit", help="Do a rollback after all imports instead of a commit? (default %(default)s)", default=False, action=misc.FlagAction)

	args = p.parse_args(args)

	db = cx_Oracle.connect(args.connectstring)

	try:
		allkeys = {}
		counts = collections.Counter()
		countfiles = 0
		loader = dict(oradd=load_oradd, ul4on=load_ul4on)[args.format]
		cursor = db.cursor()
		for (i, record) in enumerate(loader(args.file), 1):
			type = record.get("type", "procedure")
			if args.verbose >= 1:
				if args.verbose >= 3:
					if type == "procedure":
						sys.stdout.write("#{}: procedure {}".format(i, _formatcall(record, allkeys)))
					else:
						sys.stdout.write("#{}: file {} ({} bytes)".format(i, record["name"].format(**allkeys), len(record["content"])))
				else:
					sys.stdout.write(".")
				sys.stdout.flush()
			if type == "procedure":
				newkeys = importrecord(record, cursor, allkeys)
				if args.verbose >= 3:
					if newkeys:
						sys.stdout.write(" -> {}\n".format(", ".join("{}={!r}".format(argname, argvalue) for (argname, argvalue) in newkeys.items())))
					else:
						sys.stdout.write("\n")
				sys.stdout.flush()
				counts[record["name"]] += 1
			else:
				copyfile(record["filename"], record["content"], allkeys)
				if args.verbose >= 3:
					sys.stdout.write(" -> done\n")
					sys.stdout.flush()
				countfiles += 1
		if args.dryrun:
			db.rollback()
		else:
			db.commit()
	finally:
		if args.verbose >= 3:
			print()

	if args.verbose >= 2:
		totalcount = sum(counts.values())
		l1 = len(str(max(totalcount, countfiles)))
		l2 = max(len(procname) for procname in counts)
		print()
		print("Summary")
		print("="*(l1+1+l2))
		print("{:>{}} procedure".format("#", l1))
		print("{} {}".format("-"*l1, "-"*l2))
		for (procname, count) in sorted(counts.items(), key=operator.itemgetter(1)):
			print("{:>{}} {}".format(count, l1, procname))
		print("{} {}".format("-"*l1, "-"*l2))
		print("{:>{}} (total calls)".format(totalcount, l1))
		print("{:>{}} (files)".format(countfiles, l1))


if __name__ == "__main__":
	sys.exit(main())
