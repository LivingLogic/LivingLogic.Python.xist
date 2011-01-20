#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2005-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See orasql/__init__.py for the license


import sys, os, argparse

from ll import misc, astyle, orasql


s4warning = astyle.Style.fromenv("LL_ORASQL_REPRANSI_WARNING", "red:black")
s4error = astyle.Style.fromenv("LL_ORASQL_REPRANSI_ERROR", "red:black")
s4connectstring = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CONNECTSTRING", "yellow:black")
s4object = astyle.Style.fromenv("LL_ORASQL_REPRANSI_OBJECT", "green:black")


def main(args=None):
	p = argparse.ArgumentParser(description="Print (and execute) grants statements from an Oracle database schema")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-c", "--color", dest="color", help="Color output (default %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-x", "--execute", metavar="CONNECTSTRING2", dest="execute", help="Execute in target database")
	p.add_argument("-k", "--keepjunk", dest="keepjunk", help="Output objects with '$' or 'SYS_EXPORT_SCHEMA_' in their name? (default %(default)s)", default=False, action="store_true")
	p.add_argument("-i", "--ignore", dest="ignore", help="Ignore errors? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-m", "--mapgrantee", dest="mapgrantee", help="Map grantees (Python expression: list or dict)", default="True")
	p.add_argument("-e", "--encoding", dest="encoding", help="Encoding for output (default %(default)s)", default="utf-8")

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
		if args.keepjunk:
			return True
		if "$" in obj.name or "/" in obj.name or obj.name.startswith("SYS_EXPORT_SCHEMA_"):
			return False
		return True

	for (i, obj) in enumerate(connection.iterprivileges(schema="user")):
		keepobj = keep(obj)
		if args.verbose:
			if args.execute:
				msg = astyle.style_default("oragrant.py: ", cs1, " -> ", cs2, ": fetching/granting #{}".format(i+1))
			else:
				msg = astyle.style_default("oragrant.py: ", cs1, " fetching #{}".format(i+1))
			msg = astyle.style_default(msg, " ", s4object(str(obj)))
			if not keepobj:
				msg = astyle.style_default(msg, " ", s4warning("(skipped)"))
			stderr.writeln(msg)

		if keepobj:
			ddl = obj.grantddl(connection, term, mapgrantee=mapgrantee)
			if ddl:
				if args.execute:
					try:
						cursor2.execute(ddl)
					except orasql.DatabaseError, exc:
						if not args.ignore or "ORA-01013" in str(exc):
							raise
						stderr.writeln("oragrant.py: ", s4error("{}: {}".format(exc.__class__.__name__, str(exc).strip())))
				else:
					stdout.writeln(ddl.encode(args.encoding))
					stdout.writeln()


if __name__ == "__main__":
	sys.exit(main())
