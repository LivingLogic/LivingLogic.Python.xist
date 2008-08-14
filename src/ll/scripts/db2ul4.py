#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, optparse, codecs

from ll import ul4c


class System(object):
	def __getitem__(self, cmd):
		return os.popen(cmd).read()


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


class DB(object):
	def __getitem__(self, key):
		if key == "iter":
			return QueryIter(self.connection)
		elif key == "list":
			return QueryList(self.connection)
		else:
			raise KeyError(key)


class Oracle(DB):
	def __init__(self, connectstring):
		from ll import orasql
		self.connection = orasql.connect(connectstring, readlobs=True)


class SQLite(DB):
	def __init__(self, connectstring):
		import sqlite3
		connection = sqlite3.connect(connectstring)
		class Row(sqlite3.Row):
			def __getitem__(self, key):
				if isinstance(key, unicode):
					key = key.encode("ascii")
				return sqlite3.Row.__getitem__(self, key)
		connection.row_factory = Row
		self.connection = connection


class MySQL(DB):
	def __init__(self, connectstring):
		import MySQLdb
		from MySQLdb import cursors
		(user, host) = connectstring.split("@")
		(user, passwd) = user.split("/")
		(host, db) = host.split("/")
		self.connection = MySQLdb.connect(user=user, passwd=passwd, host=host, db=db, use_unicode=True, cursorclass=cursors.DictCursor)


class Connect(object):
	def __getitem__(self, connectstring):
		(type, sep, connectstring) = connectstring.partition(":")
		if type == "oracle":
			return Oracle(connectstring)
		elif type == "sqlite":
			return SQLite(connectstring)
		elif type == "mysql":
			return MySQL(connectstring)
		else:
			return KeyError(connectstring)


def main(args=None):
	p = optparse.OptionParser(usage="usage: %prog [options] maintemplate [subtemplate1 subtemplate2 ...]")
	p.add_option("-i", "--inputencoding", dest="inputencoding", help="Encoding for template sources", default="utf-8", metavar="ENCODING")
	p.add_option("-o", "--outputencoding", dest="outputencoding", help="Encoding for output", default="utf-8", metavar="ENCODING")

	(options, args) = p.parse_args(args)
	if len(args) < 1:
		p.error("incorrect number of arguments")
		return 1

	templates = {}
	maintemplate = None
	for templatename in args:
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

	vars = dict(connect=Connect(), system=System(), encoding=options.outputencoding, templates=templates)
	for part in codecs.iterencode(maintemplate.render(**vars), options.outputencoding):
		sys.stdout.write(part)


if __name__ == "__main__":
	sys.exit(main())
