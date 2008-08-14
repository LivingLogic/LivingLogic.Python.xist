#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
	class Row(sqlite3.Row):
		def __getitem__(self, key):
			if isinstance(key, unicode):
				key = key.encode("ascii")
			return sqlite3.Row.__getitem__(self, key)
	db.row_factory = Row
	return db


def main(args=None):
	p = optparse.OptionParser(usage="usage: %prog [options] connectstring maintemplate [subtemplate1 subtemplate2 ...]")
	dbs = dict(oracle=oracle, sqlite=sqlite)
	p.add_option("-d", "--database", dest="database", help="Database type (%s)" % ", ".join(dbs), choices=dbs.keys(), default="sqlite")
	p.add_option("-i", "--inputencoding", dest="inputencoding", help="Encoding for template sources", default="utf-8", metavar="ENCODING")
	p.add_option("-o", "--outputencoding", dest="outputencoding", help="Encoding for output", default="utf-8", metavar="ENCODING")

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
		template = ul4c.compile(templatestream.read().decode(options.inputencoding))
		if maintemplate is None:
			maintemplate = template
		templates[templatename] = template

	vars = dict(iters=QueryIter(db), lists=QueryList(db), encoding=options.outputencoding, templates=templates)
	for part in codecs.iterencode(maintemplate.render(**vars), options.outputencoding):
		sys.stdout.write(part)


if __name__ == "__main__":
	sys.exit(main())
