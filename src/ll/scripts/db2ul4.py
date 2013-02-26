#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
``db2ul4`` is a script that can be used for rendering database content into
a UL4 template.


Options
-------

``db2ul4`` supports the following options:

	``templates``
		One or more template files. A file named ``-`` will be treated as
		standard input. The first file in the list is the main template, i.e. the
		one that gets rendered. All templates will be available in the main
		template as the ``templates`` dictionary. The keys are the base names
		of the files (i.e. ``foo.ul4`` will be ``templates.foo``; stdin will be
		``templates.stdin``).

	``-i``, ``--inputencoding``
		The encoding of the templates files (default ``utf-8``)


Template variables
------------------

Inside the template the following variables are available:

	``templates``
		A dictionary containing all the templates specified on the command line.

	``encoding``
		The output encoding.

	``system``
		A dict-like object that maps system commands to their output, e.g. the
		template::

			<?print system["whoami"]?>

		will output the user name.

	``oracle``
		A dict-like object that maps Oracle connect strings to connection objects.

	``mysql``
		A dict-like object that maps MySQL connect strings to connection objects.
		A MySQL connect string is a string of the form ``user/pwd@host/db``.

	``sqlite``
		A dict-like object that maps SQLite connect strings to connection objects.
		The connect string will be passed directly to :func:`sqlite3.connect`.

All connection objects are itself dict-like objects providing two keys:

	``iter``
		A dict-like object that maps SQL queries to iterators over the
		result records.

	``list``
		A dict-like object that maps SQL queries to a list of result records.

A record in turn is a dict-like object mapping field names to field values.


Example
-------

This example shows how to connect to an Oracle database and output the content
of a ``person`` table into an XML file.

Suppose we have a database table that looks like this::

	create table person
	(
		id integer not null,
		firstname varchar2(200),
		lastname varchar2(200)
	);

Then we can use the following template to output the table into an XML file::

	<?xml version='1.0' encoding='<?print encoding?>'?>
	<?code db = oracle["user/pwd@db"]?>
	<persons>
		<?for p in db.iter["select id, firstname, lastname from person order by 2, 1"]?>
			<person id="<?printx p.id?>">
				<firstname><?printx p.firstname?></firstname>
				<lastname><?printx p.lastname?></lastname>
			</person>
		<?end for?>
	</persons>

If we put the template into the file ``person.ul4`` we can call ``db2ul4`` like
this::

	db2ul4 -o=utf-8 person.ul4 >person.xml
"""


import sys, os, argparse, codecs, keyword

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
				if isinstance(key, str):
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


def fixname(name):
	newname = "".join(c for (i, c) in enumerate(name) if (c.isalnum() if i else c.isalpha()))
	while keyword.iskeyword(newname):
		newname += "_"
	return newname


def main(args=None):
	p = argparse.ArgumentParser(description="render UL4 templates containing SQL statements", epilog="For more info see http://www.livinglogic.de/Python/scripts/db2ul4.html")
	p.add_argument("templates", metavar="template", help="templates to be used", nargs="+")
	p.add_argument("-e", "--encoding", dest="encoding", help="Encoding for template sources (default %(default)s)", default="utf-8", metavar="ENCODING")

	args = p.parse_args(args)

	templates = {}
	maintemplate = None
	for templatename in args.templates:
		if templatename == "-":
			templatestream = sys.stdin
			templatename = "stdin"
		else:
			templatestream = open(templatename, "r", encoding=args.encoding)
			templatename = os.path.basename(templatename)
			if os.path.extsep in templatename:
				templatename = templatename.rpartition(os.extsep)[0]
		template = ul4c.Template(templatestream.read(), fixname(templatename))
		# The first template is the main template
		if maintemplate is None:
			maintemplate = template
		templates[templatename] = template

	vars = dict(
		oracle=Oracle(),
		sqlite=SQLite(),
		mysql=MySQL(),
		system=System(),
		templates=templates,
		encoding=sys.stdout.encoding,
	)
	for part in maintemplate.render(**vars):
		sys.stdout.write(part)


if __name__ == "__main__":
	sys.exit(main())
