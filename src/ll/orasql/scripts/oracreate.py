#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2005-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See orasql/__init__.py for the license


import sys, os, optparse

from ll import astyle, orasql


s4warning = astyle.Style.fromenv("LL_ORASQL_REPRANSI_WARNING", "red:black")
s4error = astyle.Style.fromenv("LL_ORASQL_REPRANSI_ERROR", "red:black")
s4connectstring = astyle.Style.fromenv("LL_ORASQL_REPRANSI_CONNECTSTRING", "yellow:black")
s4object = astyle.Style.fromenv("LL_ORASQL_REPRANSI_OBJECT", "green:black")


def main(args=None):
	colors = ("yes", "no", "auto")
	p = optparse.OptionParser(usage="usage: %prog [options] connectstring >output.sql")
	p.add_option("-v", "--verbose", dest="verbose", help="Give a progress report?", default=False, action="store_true")
	p.add_option("-c", "--color", dest="color", help="Color output (%s)" % ", ".join(colors), default="auto", choices=colors)
	p.add_option("-s", "--seqcopy", dest="seqcopy", help="copy sequence values?", default=False, action="store_true")
	p.add_option("-x", "--execute", metavar="CONNECTSTRING2", dest="execute", help="Execute in target database", type="str")
	p.add_option("-k", "--keepjunk", dest="keepjunk", help="Output objects with '$' or 'SYS_EXPORT_SCHEMA_' in their name?", default=False, action="store_true")
	p.add_option("-i", "--ignore", dest="ignore", help="Ignore errors?", default=False, action="store_true")
	p.add_option("-e", "--encoding", dest="encoding", help="Encoding for output", default="utf-8")

	(options, args) = p.parse_args(args)
	if len(args) != 1:
		p.error("incorrect number of arguments")
		return 1

	if options.color == "yes":
		color = True
	elif options.color == "no":
		color = False
	else:
		color = None
	stdout = astyle.Stream(sys.stdout, color)
	stderr = astyle.Stream(sys.stderr, color)

	connection = orasql.connect(args[0])

	if options.execute:
		connection2 = orasql.connect(options.execute)
		cursor2 = connection2.cursor()
		term = False
	else:
		term = True

	cs1 = s4connectstring(connection.connectstring())
	if options.execute:
		cs2 = s4connectstring(connection2.connectstring())

	def keep(obj):
		if obj.owner is not None:
			return False
		if options.keepjunk:
			return True
		# output pk, fks etc. only when they belong to table we do output
		if isinstance(obj, (orasql.Constraint, orasql.Index)):
			obj = obj.table()
		if "$" in obj.name or obj.name.startswith("SYS_EXPORT_SCHEMA_"):
			return False
		return True

	for (i, obj) in enumerate(connection.iterobjects(mode="create", schema="user")):
		keepobj = keep(obj)
		if options.verbose:
			if options.execute:
				msg = astyle.style_default("oracreate.py: ", cs1, " -> ", cs2, ": fetching/creating #%d" % (i+1))
			else:
				msg = astyle.style_default("oracreate.py: ", cs1, " fetching #%d" % (i+1))
			msg = astyle.style_default(msg, " ", s4object(str(obj)))
			if not keepobj:
				msg = astyle.style_default(msg, " ", s4warning("(skipped)"))
			stderr.writeln(msg)

		if keepobj:
			if isinstance(obj, orasql.Sequence) and options.seqcopy:
				ddl = obj.createddlcopy(connection, term)
			else:
				ddl = obj.createddl(connection, term)
			if ddl:
				if options.execute:
					try:
						cursor2.execute(ddl)
					except orasql.DatabaseError, exc:
						if not options.ignore or "ORA-01013" in str(exc):
							raise
						stderr.writeln("oracreate.py: ", s4error("%s: %s" % (exc.__class__.__name__, str(exc).strip())))
				else:
					stdout.writeln(ddl.encode(options.encoding))
					stdout.writeln()


if __name__ == "__main__":
	sys.exit(main())
