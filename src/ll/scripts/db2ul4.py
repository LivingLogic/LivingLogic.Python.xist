#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
``db2ul4`` is a script that can be used for rendering database content into
a UL4 template. An example template that connects to an Oracle database and
outputs the content of a ``person`` table into an XML file looks like this::

	<?xml version='1.0' encoding='<?print encoding?>'?>
	<?code db = oracle["user/pwd@db"]?>
	<persons>
		<?for p in db.iter["select id, firstname, lastname from person"]?>
			<person id="<?printx p.id?>">
				<firstname><?printx p.firstname?></firstname>
				<lastname><?printx p.lastname?></lastname>
			</person>
		<?end for?>
	</persons>
"""


import sys, os, argparse, codecs

from ll import ul4c


__docformat__ = "reStructuredText"


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


class Connection(object):
	def __init__(self, connection):
		self.connection = connection

	def __getitem__(self, key):
		if key == "iter":
			return QueryIter(self.connection)
		elif key == "list":
			return QueryList(self.connection)
		else:
			raise KeyError(key)


class Oracle(object):
	def __getitem__(self, connectstring):
		from ll import orasql
		return Connection(orasql.connect(connectstring, readlobs=True))


class SQLite(object):
	def __getitem__(self, connectstring):
		import sqlite3
		connection = sqlite3.connect(connectstring)
		class Row(sqlite3.Row):
			def __getitem__(self, key):
				if isinstance(key, unicode):
					key = key.encode("ascii")
				return sqlite3.Row.__getitem__(self, key)
		connection.row_factory = Row
		return Connection(connection)


class MySQL(object):
	def __getitem__(self, connectstring):
		import MySQLdb
		from MySQLdb import cursors
		(user, host) = connectstring.split("@")
		(user, passwd) = user.split("/")
		(host, db) = host.split("/")
		return Connection(MySQLdb.connect(user=user, passwd=passwd, host=host, db=db, use_unicode=True, cursorclass=cursors.DictCursor))


def main(args=None):
	p = argparse.ArgumentParser(description="render UL4 templates containing SQL statements")
	p.add_argument("templates", metavar="template", help="templates to be used", nargs="+")
	p.add_argument("-i", "--inputencoding", dest="inputencoding", help="Encoding for template sources (default %(default)s)", default="utf-8", metavar="ENCODING")
	p.add_argument("-o", "--outputencoding", dest="outputencoding", help="Encoding for output (default %(default)s)", default="utf-8", metavar="ENCODING")

	args = p.parse_args(args)

	templates = {}
	maintemplate = None
	for templatename in args.templates:
		if templatename == "-":
			templatestream = sys.stdin
			templatename = "stdin"
		else:
			templatestream = open(templatename, "rb")
			templatename = os.path.basename(templatename)
			if os.path.extsep in templatename:
				templatename = templatename.rpartition(os.extsep)[0]
		template = ul4c.compile(templatestream.read().decode(args.inputencoding))
		# The first template is the main template
		if maintemplate is None:
			maintemplate = template
		templates[templatename] = template

	vars = dict(
		oracle=Oracle(),
		sqlite=SQLite(),
		mysql=MySQL(),
		system=System(),
		encoding=args.outputencoding,
		templates=templates,
	)
	for part in codecs.iterencode(maintemplate.render(**vars), args.outputencoding):
		sys.stdout.write(part)


if __name__ == "__main__":
	sys.exit(main())
