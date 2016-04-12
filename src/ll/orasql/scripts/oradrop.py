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

``oradrop`` prints the drop statements for all objects in an Oracle database
schema in the correct order (i.e. objects will be dropped so that no errors
happen during script execution). ``oradrop`` can also be used to actually
make the schema empty.


Options
-------

``oradrop`` supports the following options:

	``connectstring``
		An Oracle connectstring.

	``-v``, ``--verbose`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Produces output (on stderr) while the database is read or written.

	``-c``, ``--color`` : ``yes``, ``no`` or ``auto``
		Should the output (when the ``-v`` option is used) be colored? If ``auto``
		is specified (the default) then the output is colored if stderr is a
		terminal.

	``-f``, ``--fks`` : ``keep``, ``disable``, ``drop``
		Specifies how foreign keys from other schemas pointing to this schema
		should be treated: ``keep`` will not change the foreign keys in any way
		(this *will* lead to errors); ``disable`` will disable the foreign keys
		and ``drop`` will drop them completely.

	``-x``, ``--execute`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		When the ``-x`` argument is given the SQL script isn't printed on stdout,
		but is executed directly. Be careful with this: You *will* have an empty
		schema after ``oradrop -x``.

	``-k``, ``--keepjunk`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		If true (the default), database objects that have ``$`` or
		``SYS_EXPORT_SCHEMA_`` in their name will be skipped (otherwise these
		objects will be included in the output).

	``-i``, ``--ignore`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		If true, any exception that occurs while the database is read or written
		will be ignored.

	``--format`` : ``sql`` or ``pysql``
		If ``--execute`` is not given, this determines the output format: Plain
		SQL, or PySQL which can be piped into :mod:`ll.pysql`.

	``--include`` : regexp
		Only include objects in the output if their name contains the regular
		expression.

	``--exclude`` : regexp
		Exclude objects from the output if their name contains the regular
		expression.

"""


import sys, os, re, argparse

from ll import misc, astyle, orasql


__docformat__ = "reStructuredText"


s4warning = astyle.Style.fromenv("LL_ORASQL_REPRANSI_WARNING", "red:black")
s4error = astyle.Style.fromenv("LL_ORASQL_REPRANSI_ERROR", "red:black")
s4connectstring = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CONNECTSTRING", "yellow:black")
s4object = astyle.Style.fromenv("LL_ORASQL_REPRANSI_OBJECT", "green:black")


def main(args=None):
	p = argparse.ArgumentParser(description="Print (or execute) drop statements for all objects in an Oracle database schema", epilog="For more info see http://www.livinglogic.de/Python/orasql/scripts/oradrop.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-c", "--color", dest="color", help="Color output (default %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-f", "--fks", dest="fks", help="How should foreign keys from other schemas be treated? (default %(default)s)", default="disable", choices=("keep", "disable", "drop"))
	p.add_argument("-x", "--execute", dest="execute", help="immediately execute the commands instead of printing them? (default %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-k", "--keepjunk", dest="keepjunk", help="Output objects with '$' in their name? (default %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-i", "--ignore", dest="ignore", help="Ignore errors? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument(      "--format", dest="format", help="The output format (default %(default)s)", choices=("sql", "pysql"), default="sql")
	p.add_argument(      "--include", dest="include", metavar="REGEXP", help="Include only objects whose name contains PATTERN (default: %(default)s)", type=re.compile)
	p.add_argument(      "--exclude", dest="exclude", metavar="REGEXP", help="Exclude objects whose name contains PATTERN (default: %(default)s)", type=re.compile)

	args = p.parse_args(args)

	if args.color == "yes":
		color = True
	elif args.color == "no":
		color = False
	else:
		color = None

	stdout = astyle.Stream(sys.stdout, color)
	stderr = astyle.Stream(sys.stderr, color)

	connection = orasql.connect(args.connectstring)

	term = not args.execute

	cs = s4connectstring(connection.connectstring())

	def keep(obj):
		if obj.owner is not None and not isinstance(obj, orasql.ForeignKey):
			return False
		if ("$" in obj.name or obj.name.startswith("SYS_EXPORT_SCHEMA_")) and not args.keepjunk:
			return False
		if args.include is not None and args.include.search(obj.name) is None:
			return False
		if args.exclude is not None and args.exclude.search(obj.name) is not None:
			return False
		return True

	sqls = []
	for (i, obj) in enumerate(connection.objects(owner=None, mode="drop")):
		keepdef = keep(obj)
		# Get SQL
		sql = ""
		action = "skipped"
		if obj.owner is not None:
			if isinstance(obj, orasql.ForeignKey):
				if args.fks == "disable":
					sql = obj.disablesql(connection, term)
					action = "disabled"
				elif args.fks == "drop":
					sql = obj.dropsql(connection, term)
					action = None
		elif keepdef:
			sql = obj.dropsql(connection, term)
			action = None

		# Progress report
		if args.verbose:
			msg = astyle.style_default("oradrop.py: ", cs, ": fetching #{:,} ".format(i+1), s4object(str(obj)))
			if action is not None:
				msg = astyle.style_default(msg, " ", s4warning("({})".format(action)))
			stderr.writeln(msg)

		if sql:
			# Print or execute sql
			if args.execute:
				sqls.append((obj, sql))
			else:
				stdout.writeln(sql.strip())
				if args.format == "pysql":
					stdout.writeln()
					stdout.writeln("-- @@@")
					stdout.writeln()

	# Execute SQL
	if args.execute:
		cursor = connection.cursor()
		for (i, (obj, sql)) in enumerate(sqls):
			if args.verbose:
				stderr.writeln("oradrop.py: ", cs, ": dropping #{:,}/{:,} ".format(i+1, len(sqls)), s4object(str(obj)))
			try:
				cursor.execute(sql)
			except orasql.DatabaseError as exc:
				if not args.ignore or "ORA-01013" in str(exc):
					raise
				stderr.writeln("oradrop.py: ", s4error("{}: {}".format(exc.__class__, str(exc).strip())))


if __name__ == "__main__":
	sys.exit(main())
