#!/usr/bin/env python

import sys, os, optparse, codecs

from ll import ul4c


class QueryList(object):
	def __init__(self, connection):
		self.connection = connection

	def __getitem__(self, query):
		c = self.connection.cursor()
		c.execute(query)
		return list(c)


class QueryIter(object):
	def __init__(self, connection):
		self.connection = connection

	def __getitem__(self, query):
		c = self.connection.cursor()
		c.execute(query)
		return c


def oracle(connectstring):
	"""
	Return an Oracle connection for the connectstring :var:`connectstring`.
	"""
	from ll import orasql
	return orasql.connect(connectstring, readlobs=True)


def sqlite(connectstring):
	"""
	Return a SQLite connection for the connectstring :var:`connectstring`.
	"""
	import sqlite3
	db = sqlite3.connect(connectstring)
	db.row_factory = sqlite3.Row
	return db


def main(args=None):
	p = optparse.OptionParser(usage="usage: %prog [options] connectstring maintemplate [subtemplate1 subtemplate2 ...]")
	dbs = dict(oracle=oracle, sqlite=sqlite)
	p.add_option("-d", "--database", dest="database", help="Database type (%s)" % ", ".join(dbs), choices=dbs.keys(), default="sqlite")
	p.add_option("-i", "--inputencoding", dest="inputencoding", help="Encoding for template sources", metavar="ENCODING")
	p.add_option("-o", "--outputencoding", dest="outputencoding", help="Encoding for output", metavar="ENCODING")

	(options, args) = p.parse_args(args)
	if len(args) < 2:
		p.error("incorrect number of arguments")
		return 1

	db = dbs[options.database](args[0])

	templates = {}
	maintemplate = None
	for templatename in args[1:]:
		if templatename == "-":
			templatestream = sys.stdin
			templatename = "stdin"
		else:
			templatestream = open(templatename, "rb")
			templatename = os.path.basename(templatename)
			if os.path.extsep in templatename:
				templatename = templatename.rpartition(os.extsep)[0]
		template = ul4c.compile(templatestream.read())
		if options.inputencoding is not None:
			template = template.decode(options.inputencoding)
		if maintemplate is None:
			maintemplate = template
		templates[templatename] = template

	vars = dict(iters=QueryIter(db), lists=QueryList(db), encoding=options.outputencoding, templates=templates)
	
	output = maintemplate.render(**vars)
	if options.outputencoding is not None:
		output = codecs.iterencode(output, options.outputencoding)
	for part in output:
		sys.stdout.write(part)


if __name__ == "__main__":
	sys.exit(main())
