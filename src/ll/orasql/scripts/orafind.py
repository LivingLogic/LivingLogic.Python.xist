#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2005-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2005-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
-------

``orafind`` can be used to search all tables in an Oracle database schema for
a string.


Options
-------

``orafind`` supports the following options:

	``connectstring``
		An Oracle connectstring.

	``searchstring``
		The text to be searched for.

	``tables``
		Zero or more tables names. If any table name is specified the search will
		be limited to those tables. Otherwise all tables will be searched.

	``-v``, ``--verbose`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Produces output (on stderr) while the database is read or written.

	``-c``, ``--color`` : ``yes``, ``no`` or ``auto``
		Should the output (when the ``-v`` option is used) be colored? If ``auto``
		is specified (the default) then the output is colored if stderr is a
		terminal.

	``-i``, ``--ignore-case`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		If given, the search will be case insensitve.

	``-r``, ``--read-lobs`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		If given, ``CLOB``\s will be read when printing search results.

Example
-------

Search for ``spam`` in all tables in the schema ``user@db``. The search is case
insensitive and ``CLOB``\s will be printed::

	$ orafind user/pwd@db spam -i -r
"""


import sys, os, argparse

from ll import misc, orasql, astyle


__docformat__ = "reStructuredText"


s4warning = astyle.Style.fromenv("LL_ORASQL_REPRANSI_WARNING", "red:black")
s4error = astyle.Style.fromenv("LL_ORASQL_REPRANSI_ERROR", "red:black")
s4comment = astyle.Style.fromenv("LL_ORASQL_REPRANSI_COMMENT", "black:black:bold")
s4addedfile = astyle.Style.fromenv("LL_ORASQL_REPRANSI_ADDEDFILE", "black:green")
s4addedline = astyle.Style.fromenv("LL_ORASQL_REPRANSI_ADDEDLINE", "green:black")
s4removedfile = astyle.Style.fromenv("LL_ORASQL_REPRANSI_REMOVEDFILE", "black:red")
s4removedline = astyle.Style.fromenv("LL_ORASQL_REPRANSI_REMOVEDLINE", "red:black")
s4changedfile = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CHANGEDFILE", "black:blue")
s4changedline = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CHANGEDLINE", "blue:black")
s4pos = astyle.Style.fromenv("LL_ORASQL_REPRANSI_POS", "black:black:bold")
s4connectstring = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CONNECTSTRING", "yellow:black")
s4connid = astyle.Style.fromenv("LL_ORASQL_REPRANSI_NOTE", "yellow:black:bold")
s4action = astyle.Style.fromenv("LL_ORASQL_REPRANSI_NOTE", "magenta:black")
s4object = astyle.Style.fromenv("LL_ORASQL_REPRANSI_OBJECT", "green:black")



def cs(connection):
	return s4connectstring(connection.connectstring())


def df(obj):
	return s4object(str(obj))


def connid(name):
	return s4connid("[{}]".format(name))


def showcomment(out, *texts):
	out.writeln(s4comment("-- ", *texts))


def conflictmarker(prefix, *text):
	return astyle.style_default(s4error(prefix), " ", *text)


def showreport(out, type, countcreate, countdrop, countcollision, countmerge, countmergeconflict):
	first = True
	data = (("added", countcreate), ("dropped", countdrop), ("collided", countcollision), ("merged", countmerge), ("mergeconflict", countmergeconflict))
	for (name, count) in data:
		if count:
			if first:
				out.write(" => ")
				first = False
			else:
				out.write("; ")
			if name in ("collided", "mergeconflict"):
				cls = s4error
			else:
				cls = s4action
			if count > 1:
				msg = "{} {}s {}".format(count, type, name)
			else:
				msg = "1 {} {}".format(type, name)
			out.write(cls(msg))
	if first:
		out.write(" => identical")
	out.writeln()


def gettimestamp(obj, cursor, format):
	try:
		timestamp = obj.udate(cursor)
	except orasql.SQLObjectNotFoundError:
		return "doesn't exist"
	if timestamp is not None:
		timestamp = timestamp.strftime(format)
	else:
		timestamp = "without timestamp"
	return timestamp


def main(args=None):
	p = argparse.ArgumentParser(description="Search for a string in all fields of all tables in an Oracle database schema", epilog="For more info see http://www.livinglogic.de/Python/orasql/scripts/orafind.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("searchstring", help="String to search for")
	p.add_argument("tables", metavar="table", nargs="*", help="Limit search to those tables")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-c", "--color", dest="color", help="Color output (default: %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-i", "--ignore-case", dest="ignorecase", help="Ignore case distinctions? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-r", "--read-lobs", dest="readlobs", help="Read CLOBs when printing records? (default: %(default)s)", action=misc.FlagAction, default=False)

	args = p.parse_args(args)

	if args.color == "yes":
		color = True
	elif args.color == "no":
		color = False
	else:
		color = None
	stdout = astyle.Stream(sys.stdout, color)
	stderr = astyle.Stream(sys.stderr, color)

	searchstring = args.searchstring
	if args.ignorecase:
		searchstring = searchstring.lower()
	searchstring = "%{}%".format(searchstring.replace("%", "%%"))
	tablenames = [name.lower() for name in args.tables]

	connection = orasql.connect(args.connectstring, readlobs=args.readlobs)
	c = connection.cursor()

	tables = list(connection.tables(None))
	for (i, table) in enumerate(tables):
		skip = tablenames and table.name.lower() not in tablenames
		if args.verbose:
			msg = "skipped" if skip else "searching"
			stderr.writeln("orafind.py: ", df(table), " #", str(i+1), "/", str(len(tables)), ": ", msg)
		if not skip:
			where = []
			for col in table.columns():
				datatype = col.datatype()
				if datatype == "clob" or datatype.startswith("varchar2"):
					if args.ignorecase:
						where.append("lower({}) like :searchstring".format(col.name))
					else:
						where.append("{} like :searchstring".format(col.name))
			if not where:
				continue # no string columns
			query = "select * from {} where {}".format(table.name, " or ".join(where))
			c.execute(query, searchstring=searchstring)
			for r in c:
				stdout.writeln("orafind.py: in ", df(table), ": ", repr(r))
	return 0


if __name__ == "__main__":
	sys.exit(main())
