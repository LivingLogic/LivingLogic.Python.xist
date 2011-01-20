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
	p = argparse.ArgumentParser(description="Print (or execute) drop statements for all objects in an Oracle database schema")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-c", "--color", dest="color", help="Color output (default %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-f", "--fks", dest="fks", help="How should foreign keys from other schemas be treated? (default %(default)s)", default="disable", choices=("keep", "disable", "drop"))
	p.add_argument("-x", "--execute", dest="execute", help="immediately execute the commands instead of printing them? (default %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-k", "--keepjunk", dest="keepjunk", help="Output objects with '$' in their name? (default %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument("-i", "--ignore", dest="ignore", help="Ignore errors? (default %(default)s)", default=False, action=misc.FlagAction)
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

	term = not args.execute

	cs = s4connectstring(connection.connectstring())

	def keep(obj):
		if obj.owner is not None and not isinstance(obj, orasql.ForeignKey):
			return False
		if args.keepjunk:
			return True
		if "$" in obj.name:
			return False
		return True

	ddls = []
	for (i, obj) in enumerate(connection.iterobjects(mode="drop", schema="user")):
		keepdef = keep(obj)
		# Get DDL
		ddl = ""
		action = "skipped"
		if obj.owner is not None:
			if isinstance(obj, orasql.ForeignKey):
				if args.fks == "disable":
					ddl = obj.disableddl(cursor, term)
					action = "disabled"
				elif args.fks == "drop":
					ddl = obj.dropddl(cursor, term)
					action = None
		elif keepdef:
			ddl = obj.dropddl(connection, term)
			action = None

		# Progress report
		if args.verbose:
			msg = astyle.style_default("oradrop.py: ", cs, ": fetching #{} ".format(i+1), s4object(str(obj)))
			if action is not None:
				msg = astyle.style_default(msg, " ", s4warning("({})".format(action)))
			stderr.writeln(msg)

		if ddl:
			# Print or execute DDL
			if args.execute:
				ddls.append((obj, ddl))
			else:
				stdout.write(ddl.encode(args.encoding))

	# Execute DDL
	if args.execute:
		cursor = connection.cursor()
		for (i, (obj, ddl)) in enumerate(ddls):
			if args.verbose:
				stderr.writeln("oradrop.py: ", cs, ": dropping #{}/{} ".format(i+1, len(ddls)), s4object(str(obj)))
			try:
				cursor.execute(ddl)
			except orasql.DatabaseError, exc:
				if not args.ignore or "ORA-01013" in str(exc):
					raise
				stderr.writeln("oradrop.py: ", s4error("{}: {}".format(exc.__class__, str(exc).strip())))


if __name__ == "__main__":
	sys.exit(main())
