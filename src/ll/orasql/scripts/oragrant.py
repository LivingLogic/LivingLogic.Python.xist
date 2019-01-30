#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2005-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2005-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
=======

:program:`oragrant` prints all existing grants in an Oracle database schema.
It can also be used to execute these grant statements directly.


Options
=======

:program:`oragrant` supports the following options:

.. program:: oragrant


.. option:: connectstring

	An Oracle connectstring.

.. option:: -v <flag>, --verbose <flag>

	Produces output (on stderr) while the database is read or written.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -c <mode>, --color <mode>

	Should the output (when the :option:`-v` option is used) be colored?
	If ``auto`` is specified (the default) then the output is colored if stderr
	is a terminal. Valid modes are ``yes``, ``no`` or ``auto``.

.. option:: -x <connectstring>, --execute <connectstring>

	When the :option:`-x` argument is given the SQL script isn't printed on
	stdout, but executed in the database specfied as the :option:`-x` argument.

.. option:: -k <flag>, --keepjunk <flag>

	If false (the default), database objects that have ``$`` or
	``SYS_EXPORT_SCHEMA_`` in their name will be skipped (otherwise these
	objects will be included in the output).
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -i <flag>, --ignore <flag>

	If true, any exception that occurs while the database is read or written
	will be ignored.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -m <expr>, --mapgrantee <expr>

	A Python ``dict`` or ``list`` literal which will be evaluated. If the
	grantee is not in this list (or dictionary) no grant statement will be
	returned. If it's a dictionary and the grantee exists as a key, the
	privilege will be granted to the user specified as the value instead of
	the original one. The default is to grant all privileges to the original
	grantee.

.. option:: --format <format>

	If :option:`--execute` is not given, this determines the output format:
	Plain SQL (format ``sql``), or PySQL (format ``pysql``) which can be piped
	into :mod:`ll.pysql`.

.. option:: --include <regexp>

	Only include objects in the output if their name contains the regular
	expression.

.. option:: --exclude <regexp>

	Exclude objects from the output if their name contains the regular
	expression.


Example
=======

Grant all privileges that ``alice`` has in the schema ``user@db`` to ``bob`` in
``user2@db2``:

.. sourcecode:: bash

	$ oragrant user/pwd@db -x user2/pwd2@db2 -m '{"alice": "bob"}' -v
"""


import sys, os, re, argparse

from ll import misc, astyle, orasql


__docformat__ = "reStructuredText"


s4warning = astyle.Style.fromenv("LL_ORASQL_REPRANSI_WARNING", "red:black")
s4error = astyle.Style.fromenv("LL_ORASQL_REPRANSI_ERROR", "red:black")
s4connectstring = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CONNECTSTRING", "yellow:black")
s4object = astyle.Style.fromenv("LL_ORASQL_REPRANSI_OBJECT", "green:black")


def main(args=None):
	p = argparse.ArgumentParser(description="Print (and execute) grants statements from an Oracle database schema", epilog="For more info see http://python.livinglogic.de/orasql_scripts_oragrant.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-c", "--color", dest="color", help="Color output (default %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-x", "--execute", metavar="CONNECTSTRING2", dest="execute", help="Execute in target database")
	p.add_argument("-k", "--keepjunk", dest="keepjunk", help="Output objects with '$' or 'SYS_EXPORT_SCHEMA_' in their name? (default %(default)s)", default=False, action="store_true")
	p.add_argument("-i", "--ignore", dest="ignore", help="Ignore errors? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-m", "--mapgrantee", dest="mapgrantee", help="Map grantees (Python expression: list or dict)", default="True")
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

	if args.execute:
		connection2 = orasql.connect(args.execute)
		cursor2 = connection2.cursor()
		term = False
	else:
		term = True

	cs1 = s4connectstring(connection.connectstring())
	if args.execute:
		cs2 = s4connectstring(connection2.connectstring())

	mapgrantee = eval(args.mapgrantee)

	def keep(obj):
		if ("$" in obj.name or "/" in obj.name or obj.name.startswith("SYS_EXPORT_SCHEMA_")) and not args.keepjunk:
			return False
		if args.include is not None and args.include.search(obj.name) is None:
			return False
		if args.exclude is not None and args.exclude.search(obj.name) is not None:
			return False
		return True

	for (i, obj) in enumerate(connection.privileges(None)):
		keepobj = keep(obj)
		if args.verbose:
			if args.execute:
				msg = astyle.style_default("oragrant.py: ", cs1, " -> ", cs2, f": fetching/granting #{i+1:,}")
			else:
				msg = astyle.style_default("oragrant.py: ", cs1, f" fetching #{i+1:,}")
			msg = astyle.style_default(msg, " ", s4object(str(obj)))
			if not keepobj:
				msg = astyle.style_default(msg, " ", s4warning("(skipped)"))
			stderr.writeln(msg)

		if keepobj:
			sql = obj.grantsql(connection, term, mapgrantee=mapgrantee)
			if sql:
				if args.execute:
					try:
						cursor2.execute(sql)
					except orasql.DatabaseError as exc:
						if not args.ignore or "ORA-01013" in str(exc):
							raise
						stderr.writeln("oragrant.py: ", s4error(misc.format_exception(exc)))
				else:
					stdout.writeln(sql.strip())
					if args.format == "pysql":
						stdout.writeln()
						stdout.writeln("-- @@@")
						stdout.writeln()


if __name__ == "__main__":
	sys.exit(main())
