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
	fks = ("keep", "disable", "drop")
	p = optparse.OptionParser(usage="usage: %prog [options] connectstring >output.sql")
	p.add_option("-v", "--verbose", dest="verbose", help="Give a progress report?", default=False, action="store_true")
	p.add_option("-c", "--color", dest="color", help="Color output (%s)" % ", ".join(colors), default="auto", choices=colors)
	p.add_option("-f", "--fks", dest="fks", help="How should foreign keys from other schemas be treated (%s)?" % ", ".join(fks), default="disable", choices=fks)
	p.add_option("-x", "--execute", dest="execute", action="store_true", help="immediately execute the commands instead of printing them?")
	p.add_option("-k", "--keepjunk", dest="keepjunk", help="Output objects with '$' in their name?", default=False, action="store_true")
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

	term = not options.execute
	
	cs = s4connectstring(connection.connectstring())

	def keep(obj):
		if obj.owner is not None and not isinstance(obj, orasql.ForeignKey):
			return False
		if options.keepjunk:
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
				if options.fks == "disable":
					ddl = obj.disableddl(cursor, term)
					action = "disabled"
				elif options.fks == "drop":
					ddl = obj.dropddl(cursor, term)
					action = None
		elif keepdef:
			ddl = obj.dropddl(connection, term)
			action = None

		# Progress report
		if options.verbose:
			msg = astyle.style_default("oradrop.py: ", cs, ": fetching #%d " % (i+1), s4object(str(obj)))
			if action is not None:
				msg = astyle.style_default(msg, " ", s4warning("(%s)" % action))
			stderr.writeln(msg)

		if ddl:
			# Print or execute DDL
			if options.execute:
				ddls.append((obj, ddl))
			else:
				stdout.write(ddl.encode(options.encoding))

	# Execute DDL
	if options.execute:
		cursor = connection.cursor()
		for (i, (obj, ddl)) in enumerate(ddls):
			if options.verbose:
				stderr.writeln("oradrop.py: ", cs, ": dropping #%d/%d " % (i+1, len(ddls)), s4object(str(obj)))
			try:
				cursor.execute(ddl)
			except orasql.DatabaseError, exc:
				if not options.ignore or "ORA-01013" in str(exc):
					raise
				stderr.writeln("oradrop.py: ", s4error("%s: %s" % (exc.__class__, str(exc).strip())))


if __name__ == "__main__":
	sys.exit(main())
