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

:program:`oradelete` prints the delete statements for all tables in an Oracle
database schema in the correct order (i.e. records will be deleted so that no
errors happen during script execution). :program:`oradelete` can also be used
to actually make all tables empty.


Options
=======

:program:`oradelete` supports the following options:

.. program:: oradelete

.. option:: connectstring

	An Oracle connectstring.

.. option:: -v <flag>, --verbose <flag>

	Produces output (on stderr) while the database is read or written.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -c <flag>, --color <flag>

	Should the output (when the ``-v`` option is used) be colored? If ``auto``
	is specified (the default) then the output is colored if stderr is a
	terminal. Valid modes are ``yes``, ``no`` or ``auto``.

.. option:: -s <flag>, --sequences <flag>

	Should sequences be reset to their initial values?
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -x <flag>, --execute <flag>

	When the :option:`-x` argument is given the SQL script isn't printed on
	stdout, but is executed directly in the schema specified via the
	:option:`connectstring` option. Be careful with this: You *will* have empty
	tables after ``oradelete -x``.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -k <flag>, --keepjunk <flag>

	If false (the default), database objects that have ``$`` or
	``SYS_EXPORT_SCHEMA_`` in their name will be skipped (otherwise these
	objects will be included in the output).
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -i <flag>, --ignore <flag>

	If true, any exception that occurs while the database is read or written
	will be ignored.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -t <flag>, --truncate <flag>

	If given the script uses the ``TRUNCATE`` command instead of the ``DELETE``
	command.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: --format <format>

	If ``--execute`` is not given, this determines the output format: Plain
	SQL (format ``sql``), or PySQL (format ``pysql``) which can be piped into
	:mod:`ll.pysql`.

.. option:: --include <regexp>

	Only include objects in the output if their name contains the regular
	expression.

.. option:: --exclude <regexp>

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
	p = argparse.ArgumentParser(description="Print (or execute) SQL for deleting all records from all tables in an Oracle database schema", epilog="For more info see http://python.livinglogic.de/orasql_scripts_oradelete.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-c", "--color", dest="color", help="Color output (default %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-s", "--sequences", dest="sequences", help="Reset sequences? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-x", "--execute", dest="execute", action=misc.FlagAction, help="immediately execute the commands instead of printing them? (default %(default)s)")
	p.add_argument("-k", "--keepjunk", dest="keepjunk", help="Output objects with '$' or 'SYS_EXPORT_SCHEMA_' in their name? (default %(default)s)", default=False, action="store_true")
	p.add_argument("-i", "--ignore", dest="ignore", help="Ignore errors? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-t", "--truncate", dest="truncate", help="Truncate tables (instead of deleting)? (default %(default)s)", default=False, action=misc.FlagAction)
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
	cursor = connection.cursor()

	cs = s4connectstring(connection.connectstring())

	def keep(obj):
		if ("$" in obj.name or "/" in obj.name or obj.name.startswith("SYS_EXPORT_SCHEMA_")) and not args.keepjunk:
			return False
		if args.include is not None and args.include.search(obj.name) is None:
			return False
		if args.exclude is not None and args.exclude.search(obj.name) is not None:
			return False
		return True

	for (i, obj) in enumerate(connection.tables(owner=None, mode="drop")):
		keepobj = keep(obj)
		# Progress report
		if args.verbose:
			msg = "truncating" if args.truncate else "deleting from"
			msg = astyle.style_default("oradelete.py: ", cs, f": {msg} #{i+1:,} ", s4object(str(obj)))
			if not keepobj:
				msg = astyle.style_default(msg, " ", s4warning("(skipped)"))
			stderr.writeln(msg)

		if keepobj:
			# Print or execute SQL
			if args.execute:
				try:
					if args.truncate:
						query = f"truncate table {obj.name}"
					else:
						query = f"delete from {obj.name}"
					cursor.execute(query)
				except orasql.DatabaseError as exc:
					if not args.ignore or "ORA-01013" in str(exc):
						raise
					stderr.writeln("oradelete.py: ", s4error(f"{exc.__class__}: {str(exc).strip()}"))
			else:
				if args.truncate:
					sql = f"truncate table {obj.name};"
				else:
					sql = f"delete from {obj.name};"
				stdout.writeln(sql)
				stdout.writeln()
				if args.format == "pysql":
					stdout.writeln("-- @@@")
					stdout.writeln()
	if not args.truncate:
		connection.commit()

	if args.sequences:
		for (i, obj) in enumerate(connection.sequences(owner=None)):
			keepobj = keep(obj)
			# Progress report
			if args.verbose:
				msg = astyle.style_default("oradelete.py: ", cs, f": recreating #{i+1:,} ", s4object(str(obj)))
				if not keepobj:
					msg = astyle.style_default(msg, " ", s4warning("(skipped)"))
				stderr.writeln(msg)

			if keepobj:
				# Print or execute SQL
				if args.execute:
					try:
						sql = obj.createsql(term=False)
						cursor.execute(obj.dropsql(term=False))
						cursor.execute(sql)
					except orasql.DatabaseError as exc:
						if not args.ignore or "ORA-01013" in str(exc):
							raise
						stderr.writeln("oradelete.py: ", s4error(f"{exc.__class__}: {str(exc).strip()}"))
				else:
					stdout.writeln(obj.dropsql(term=True).strip())
					stdout.writeln()
					if args.format == "pysql":
						stdout.writeln("-- @@@")
						stdout.writeln()
					stdout.writeln(obj.createsql(term=True).strip())
					stdout.writeln()
					if args.format == "pysql":
						stdout.writeln("-- @@@")
						stdout.writeln()


if __name__ == "__main__":
	sys.exit(main())
