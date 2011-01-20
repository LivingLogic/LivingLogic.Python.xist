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
	p = argparse.ArgumentParser(description="Print (or execute) SQL for deleting all records from all tables in an Oracle database schema")
	p.add_argument("connectstring", help="Oracle connect string")
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-c", "--color", dest="color", help="Color output (default %(default)s)", default="auto", choices=("yes", "no", "auto"))
	p.add_argument("-s", "--sequences", dest="sequences", help="Reset sequences? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-x", "--execute", dest="execute", action=misc.FlagAction, help="immediately execute the commands instead of printing them? (default %(default)s)")
	p.add_argument("-i", "--ignore", dest="ignore", help="Ignore errors? (default %(default)s)", default=False, action=misc.FlagAction)
	p.add_argument("-e", "--encoding", dest="encoding", help="Encoding for output (default %(default)s)", default="utf-8")
	p.add_argument("-t", "--truncate", dest="truncate", help="Truncate tables (instead of deleting)? (default %(default)s)", default=False, action=misc.FlagAction)

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

	for (i, obj) in enumerate(connection.itertables(schema="user", mode="drop")):
		# Progress report
		if args.verbose:
			msg = "truncating" if args.truncate else "deleting from"
			msg = astyle.style_default("oradelete.py: ", cs, ": {} #{} ".format(msg, i+1), s4object(str(obj)))
			stderr.writeln(msg)

		# Print or execute SQL
		if args.execute:
			try:
				fmt = u"truncate table {}" if args.truncate else u"delete from {}"
				cursor.execute(fmt.format(obj.name))
			except orasql.DatabaseError, exc:
				if not args.ignore or "ORA-01013" in str(exc):
					raise
				stderr.writeln("oradelete.py: ", s4error("{}: {}".format(exc.__class__, str(exc).strip())))
		else:
			if args.truncate:
				sql = u"truncate table {};\n".format(obj.name)
			else:
				sql = u"delete from {};\n".format(obj.name)
			stdout.write(sql.encode(args.encoding))
	if not args.truncate:
		connection.commit()

	if args.sequences:
		for (i, obj) in enumerate(connection.itersequences(schema="user")):
			# Progress report
			if args.verbose:
				msg = astyle.style_default("oradelete.py: ", cs, ": recreating #{} ".format(i+1), s4object(str(obj)))
				stderr.writeln(msg)

			# Print or execute SQL
			if args.execute:
				try:
					sql = obj.createddl(term=False)
					cursor.execute(obj.dropddl(term=False))
					cursor.execute(sql)
				except orasql.DatabaseError, exc:
					if not args.ignore or "ORA-01013" in str(exc):
						raise
					stderr.writeln("oradelete.py: ", s4error("{}: {}".format(exc.__class__, str(exc).strip())))
			else:
				sql = obj.dropddl(term=True) + obj.createddl(term=True)
				stdout.write(sql.encode(args.encoding))

if __name__ == "__main__":
	sys.exit(main())
