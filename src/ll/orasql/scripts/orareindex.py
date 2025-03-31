#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2014-2025 by LivingLogic AG, Bayreuth/Germany
## Copyright 2014-2025 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


r"""
Purpose
=======

:program:`orareindex` recreates/rebuilds all indexes and unique constraints in
an Oracle database schema.


Options
=======

:program:`orareindex` supports the following options:

.. program:: orareindex

.. option:: connectstring

	An Oracle connectstring.

.. option:: -v <flag>, --verbose <flag>

	Produces output (on stderr) while the database is read or written.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -c <mode>, --color <mode>

	Should the output (when the :option:`-v` option is used) be colored?
	If ``auto`` is specified (the default) then the output is colored if stderr
	is a terminal. Valid modes are ``yes``, ``no`` or ``auto``.

.. option:: -x <flag>, --execute <flag>

	When the :option:`-x` argument is given the SQL script isn't printed on
	stdout, but is executed directly in the schema specified via the
	:option:`connectstring` option.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: -r <flag>, --rebuild <flag>

	If given, the script uses ``ALTER INDEX ... REBUILD`` to rebuild indexes
	instead of dropping and recreating them.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: --format <format>

	If :option:`--execute` is not given, this determines the output format:
	Plain SQL (format ``sql``), or PySQL (format ``pysql``) which can be piped
	into :mod:`ll.pysql`.

.. option:: --thick <flag>

	If true, use :mod:`oracledb`\s thick mode.
	(Valid flag values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``)

.. option:: --config_dir <directory>

	In :mod:`oracledb`\s thin mode, specify the directory that contains the
	``tnsnames.ora`` file. This can be used if "Connect Descriptor Strings"
	from ``tnsnames.ora`` must be used but ``tnsnames.ora`` can't be found
	in its default location.
"""


import sys, argparse, itertools

from ll import misc, astyle, orasql


__docformat__ = "reStructuredText"


s4connectstring = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CONNECTSTRING", "yellow:black")
s4object = astyle.Style.fromenv("LL_ORASQL_REPRANSI_OBJECT", "green:black")


def main(args=None):
	p = argparse.ArgumentParser(description="Recreate/rebuild all indexes/unique constraints in an Oracle database schema", epilog="For more info see http://python.livinglogic.de/orasql_scripts_orareindex.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-c", "--color", dest="color", help="Color output (default %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-r", "--rebuild", dest="rebuild", help="Rebuild indexes instead of recreating them? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-x", "--execute", dest="execute", action=misc.FlagAction, help="immediately execute the commands instead of printing them? (default %(default)s)")
	p.add_argument(      "--format", dest="format", help="The output format (default %(default)s)", choices=("sql", "pysql"), default="sql")
	p.add_argument(      "--ignoreerrors", dest="ignoreerrors", help="Ignore errors? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument(      "--thick", dest="thick", help="Use oracledb's 'thick' mode for Oracle connections?", default=False, action=misc.FlagAction)
	p.add_argument(      "--config_dir", dest="config_dir", metavar="DIR", help="Directory that contains 'tnsnames.ora', if it should be used for Oracle connections.")

	args = p.parse_args(args)

	if args.color == "yes":
		color = True
	elif args.color == "no":
		color = False
	else:
		color = None

	stdout = astyle.Stream(sys.stdout, color)
	stderr = astyle.Stream(sys.stderr, color)

	if args.thick:
		orasql.init_oracle_client()
	connection = orasql.connect(args.connectstring, config_dir=args.config_dir)

	cursor = connection.cursor()

	cs = s4connectstring(connection.connectstring())

	for (i, obj) in enumerate(itertools.chain(orasql.Index.objects(connection, owner=None), orasql.UniqueConstraint.objects(connection, owner=None))):
		rebuild = args.rebuild and isinstance(obj, orasql.Index)
		# Progress report
		if args.verbose:
			stderr.writeln("orareindex.py: ", cs, f": {'Rebuilding' if rebuild else 'Recreating'} #{i+1:,} ", s4object(str(obj)))
		if rebuild:
			if args.execute:
				if args.ignoreerrors:
					try:
						cursor.execute(obj.rebuildsql(term=False))
					except Exception:
						pass
				else:
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
				if args.ignoreerrors:
					try:
						cursor.execute(obj.dropsql(term=False))
						cursor.execute(sql)
					except Exception:
						pass
				else:
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
