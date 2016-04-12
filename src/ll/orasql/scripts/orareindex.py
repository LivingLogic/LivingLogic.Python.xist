#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2014-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2014-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
-------

``orareindex`` recreates/rebuilds all indexes and unique constraints in an
Oracle database schema.


Options
-------

``orareindex`` supports the following options:

	``connectstring``
		An Oracle connectstring.

	``-v``, ``--verbose`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Produces output (on stderr) while the database is read or written.

	``-c``, ``--color`` : ``yes``, ``no`` or ``auto``
		Should the output (when the ``-v`` option is used) be colored? If ``auto``
		is specified (the default) then the output is colored if stderr is a
		terminal.

	``-x``, ``--execute`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		When the ``-x`` argument is given the SQL script isn't printed on stdout,
		but is executed directly.

	``-r``, ``--rebuild`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		If given, the script uses ``ALTER INDEX ... REBUILD`` to rebuild indexes
		instead of dropping and recreating them.

	``--format`` : ``sql`` or ``pysql``
		If ``--execute`` is not given, this determines the output format: Plain
		SQL, or PySQL which can be piped into :mod:`ll.pysql`.
"""


import sys, argparse, itertools

from ll import misc, astyle, orasql


__docformat__ = "reStructuredText"


s4connectstring = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CONNECTSTRING", "yellow:black")
s4object = astyle.Style.fromenv("LL_ORASQL_REPRANSI_OBJECT", "green:black")


def main(args=None):
	p = argparse.ArgumentParser(description="Recreate/rebuild all indexes/unique constraints in an Oracle database schema", epilog="For more info see http://www.livinglogic.de/Python/orasql/scripts/orareindex.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-c", "--color", dest="color", help="Color output (default %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-r", "--rebuild", dest="rebuild", help="Rebuild indexes instead of recreating them? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-x", "--execute", dest="execute", action=misc.FlagAction, help="immediately execute the commands instead of printing them? (default %(default)s)")
	p.add_argument(      "--format", dest="format", help="The output format (default %(default)s)", choices=("sql", "pysql"), default="sql")

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
	cursor = connection.cursor()

	cs = s4connectstring(connection.connectstring())

	for (i, obj) in enumerate(itertools.chain(orasql.Index.objects(connection, owner=None), orasql.UniqueConstraint.objects(connection, owner=None))):
		rebuild = args.rebuild and isinstance(obj, orasql.Index)
		# Progress report
		if args.verbose:
			stderr.writeln("orareindex.py: ", cs, ": {} #{:,} ".format("Rebuilding" if rebuild else "Recreating", i+1), s4object(str(obj)))
		if rebuild:
			if args.execute:
				cursor.execute(obj.rebuildsql(term=False))
			else:
				stdout.writeln(obj.rebuildsql(term=True).strip())
				if args.format == "pysql":
					stdout.writeln()
					stdout.writeln("-- @@@")
					stdout.writeln()
		else:
			if args.execute:
				sql = obj.createsql(term=False)
				cursor.execute(obj.dropsql(term=False))
				cursor.execute(sql)
			else:
				stdout.writeln(obj.dropsql(term=True).strip())
				if args.format == "pysql":
					stdout.writeln()
					stdout.writeln("-- @@@")
					stdout.writeln()
				stdout.writeln(obj.createsql(term=True).strip())
				if args.format == "pysql":
					stdout.writeln()
					stdout.writeln("-- @@@")
					stdout.writeln()


if __name__ == "__main__":
	sys.exit(main())
