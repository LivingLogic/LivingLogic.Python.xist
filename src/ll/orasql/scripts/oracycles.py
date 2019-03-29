#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
=======

:program:`oracycles` checks the foreign key references in an Oracle database
for cyclic references, either direct ones (i.e. foreign keys that reference
the same table) or indirect ones.


Options
=======

:program:`oracycles` supports the following options:

.. program:: oracycles

.. option:: connectstring

	An Oracle connectstring.

.. option:: -v <flag>, --verbose <flag>

	Produces output (on stderr) while the database is read or foreign keys are
	checked for cycles. (Valid flag values are ``false``, ``no``, ``0``,
	``true``, ``yes`` or ``1``)

.. option:: -c <mode>, --color <mode>

	Should the output (when the :option:`-v` option is used) be colored? If
	``auto`` is specified (the default) then the output is colored if it goes to
	a terminal. Valid modes are ``yes``, ``no`` or ``auto``.
"""


import sys, os, re, argparse

from ll import misc, astyle, orasql


__docformat__ = "reStructuredText"


s4connectstring = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CONNECTSTRING", "yellow:black")
s4object = astyle.Style.fromenv("LL_ORASQL_REPRANSI_OBJECT", "green:black")


def main(args=None):
	p = argparse.ArgumentParser(description="Check Oracle database schema for cyclic foreign key references", epilog="For more info see http://python.livinglogic.de/orasql_scripts_oracycles.html")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-c", "--color", dest="color", help="Color output (default %(default)s)", default="auto", choices=("yes", "no", "auto"))

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

	cs = s4connectstring(connection.connectstring())

	refs = {} # type: Dict[Table, Tuple[ForeignKey, Table]]

	# Collect tables
	tables = list(connection.tables())

	# Collect foreign keys from tables
	for (i, table) in enumerate(tables, 1):
		if args.verbose:
			stderr.writeln("oracycles.py: ", cs, f": Collecting fks from table #{i:,}/{len(tables):,} ", s4object(table.name), f" -> {len(refs):,} found")
		for constraint in list(table.constraints()):
			if isinstance(constraint, orasql.ForeignKey):
				pk = constraint.refconstraint()
				if isinstance(pk, orasql.PrimaryKey):
					if table not in refs:
						refs[table] = []
					reftable = pk.table()
					refs[table].append((constraint, reftable))

	# Find cycles in foreign keys
	cycles = {}

	def collect(path):
		for i in range(len(path)-2, 0, -1):
			if path[i] == path[-1]:
				cyclepath  = path[i:]
				pathkey = frozenset(cyclepath)
				if pathkey not in cycles:
					cycles[pathkey] = cyclepath
				return

	def findcycles(path):
		table = path[-1]
		if table in refs:
			for (constraint, reftable) in refs[table]:
				path.append(constraint)
				cycle = reftable in path
				path.append(reftable)
				if cycle:
					collect(path)
				else:
					findcycles(path)
				path.pop()
				path.pop()

	for (i, table) in enumerate(tables, 1):
		if args.verbose:
			stderr.writeln("oracycles.py: ", cs, f": Testing table #{i:,}/{len(tables):,} ", s4object(table.name), f" for cycles -> {len(cycles):,} found")
		findcycles([table])

	# Sort and output result
	def pathstr(path):
		v = []
		for obj in path:
			if isinstance(obj, orasql.ForeignKey):
				v.append(f"{misc.first(obj.columns()).name}({obj.name})")
			else:
				v.append(obj.name)
		return " -> ".join(v)

	cycles = sorted(cycles.values(), key=pathstr)

	for path in cycles:
		for (i, obj) in enumerate(path):
			if i:
				stdout.write(" -> ")
			if isinstance(obj, orasql.ForeignKey):
				stdout.write(s4object(misc.first(obj.columns()).name), "(", s4object(obj.name), ")")
			else:
				stdout.write(s4object(obj.name))
		stdout.writeln()


if __name__ == "__main__":
	sys.exit(main())
