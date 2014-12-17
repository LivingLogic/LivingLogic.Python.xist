#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

"""
Purpose
=======

``rul4`` is a script that can be used for rendering UL4 templates. Templates
have access to Oracle, MySQL and SQLite databases and can execute system
commands.


Options
=======

``rul4`` supports the following options:

	``templates``
		One or more template files. A file named ``-`` will be treated as
		standard input. The first file in the list is the main template, i.e. the
		one that gets rendered. All templates will be available in the main
		template as the ``templates`` dictionary. The keys are the base names
		of the files (i.e. ``foo.ul4`` will be ``templates.foo``; stdin will be
		``templates.stdin``).

	``--oracle`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Provide the object ``oracle`` to the template or not (see below)?

	``--sqlite`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Provide the object ``sqlite`` to the template or not (see below)?

	``--mysql`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Provide the object ``mysql`` to the template or not (see below)?

	``--system`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Provide the object ``system`` to the template or not (see below)?

	``-e``, ``--encoding``
		The encoding of the templates files (default ``utf-8``)

	``-w``, ``--keepws`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Should line feeds and indentation be kept in the templates or not?

	``-D``, ``--define``
		Defines an additional value that will be available inside the template.
		``-D`` can be specified multiple times. The following formats are supported:

			``var``
				Defines ``var`` as an empty string;

			``var=value``
				Defines ``var`` as the string ``value``;

			``var:type``
				Defines ``var`` as an empty variable of the type ``type``;

			``var:type=value``
				Defines ``var`` as a variable of the type ``type`` with the value
				``value``.

		``type`` can be any of the following:

			``int``
				``value`` is an integer value.

			``float``
				``value`` is a float value.

			``bool``
				``value`` is a boolean value. ``0``, ``no``, ``false``, ``False`` or
				the empty string will be recognized as false and ``1``, ``yes``,
				``true`` or ``True`` will be recognized as true.

			``str``
				``value`` is a string.

			``oracle``
				``value`` will be a connection to an Oracle database, e.g.::

					-Ddb:oracle=user/pwd@database

			``sqlite``
				``value`` is a connection to an SQLite database.

			``mysql``
				``value`` is a connection to a MySQL database.


Template variables
==================

Inside the template the following variables are available (if enabled via
the matching options):

	``templates``
		A dictionary containing all the templates specified on the command line.

	``encoding``
		The output encoding.

	``system``
		An object with an ``execute`` method that executes system commands and
		returns their output, e.g. the template::

			<?print system.execute("whoami")?>

		will output the user name.

	``oracle``
		An object with a ``connect`` method that returns a connection to an oracle
		database.

	``mysql``
		An object with a ``connect`` method that return a MySQL connection for
		the MySQL connect strings passed in. A MySQL connect string is a string
		of the form ``user/pwd@host/db``.

	``sqlite``
		An object with a ``connect`` method that return a SQLite connection for
		the connect strings passed in. The connect string will be passed directly
		to :func:`sqlite3.connect`.

All variables defined via the :option:`-D`/:option:`--define` option will also
be available. (Note that you can't overwrite any of the predefined variables).


Database connections
--------------------

All connection objects have a ``query`` method that executes the query passed in
and returns an iterator over the resulting records. This ``query`` method
requires at least one positional argument. Arguments alternate between fragments
of the SQL query and parameters that will be embedded in the query. For example::

	<?code db = oracle.connect("user/pwd@db")?>
	<?code name = "Bob"?>
	<?for p in db.query("select * from person where firstname=", name, " or lastname=", name)?>
		...

The records returned from ``query`` are dict-like objects mapping field names to
field values.

Connection objects also have an ``execute`` method that supports the same
parameters as ``query`` but doesn't return an iterable result. This can be used
to call functions or procedures.

Calling functions or procedures with out parameters can be done with variable
objects that can be created with the methods :meth:`int`, :meth:`number`,
:meth:`str`, :meth:`clob` and :meth:`date`. The resulting value of the out
parameter is available from the ``value`` attribute of the variable object.
The following example creates a function, calls it to get at the result and
drops it again::

	<?code db = oracle.connect('user/pwd@database')?>
	<?code db.execute('''
		create or replace function ul4test(p_arg integer)
		return integer
		as
		begin
			return 2*p_arg;
		end;
	''')?>
	<?code vout = db.int()?>
	<?code db.execute('begin ', vout, ' := ul4test(42); end;')?>
	<?print vout.value?>
	<?code db.execute('drop function ul4test')?>


Example
=======

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

	<?xml version='1.0' encoding='utf-8'?>
	<?code db = oracle.connect("user/pwd@database')?>
	<persons>
		<?for p in db.query("select id, firstname, lastname from person order by 2, 1")?>
			<person id="<?printx p.id?>">
				<firstname><?printx p.firstname?></firstname>
				<lastname><?printx p.lastname?></lastname>
			</person>
		<?end for?>
	</persons>

If we put the template into the file ``person.ul4`` we can call ``rul4`` like
this::

	rul4 person.ul4 >person.xml

We could also pass the connection to our database via the ``-D`` option and
disallow the script to make any database connections or execute any system
commands::

	rul4 person.ul4 -Ddb:oracle=user/pwd@database --oracle=0 --sqlite=0 --mysql=0 --system=0 >person.xml

Then the template could use the Oracle connection object ``db`` directly.
"""


import sys, os, argparse, datetime, keyword

from ll import ul4c, misc


__docformat__ = "reStructuredText"


class System:
	ul4attrs = {"execute"}

	def execute(self, cmd):
		return os.popen(cmd).read()


class Var:
	ul4attrs = {"+value"}

	def __init__(self, value=None):
		self.value = value

	@misc.notimplemented
	def makevar(c, cursor):
		pass


class Connection:
	ul4attrs = {"query", "execute", "int", "number", "str", "clob", "date"}

	def __init__(self, connection):
		self.connection = connection

	def _execute(self, cursor, queryparts):
		query = []
		params = {}
		vars = {}
		for (i, part) in enumerate(queryparts):
			if i % 2:
				name = "value{}".format((i+1)//2)
				if isinstance(part, Var):
					params[name] = part.makevar(cursor)
					vars[name] = part
				else:
					params[name] = part
				query.append(":" + name)
			else:
				query.append(part)
		cursor.execute("".join(query), **params)
		for (name, var) in vars.items():
			var.value = params[name].getvalue(0)

	def query(self, *queryparts):
		cursor = self.connection.cursor()
		self._execute(cursor, queryparts)
		return cursor

	def execute(self, *queryparts):
		cursor = self.connection.cursor()
		self._execute(cursor, queryparts)

	@misc.notimplemented
	def str(self, value=None):
		pass

	@misc.notimplemented
	def clob(self, value=None):
		pass

	@misc.notimplemented
	def int(self, value=None):
		pass

	@misc.notimplemented
	def number(self, value=None):
		pass

	@misc.notimplemented
	def date(self, value=None):
		pass


class OracleConnection(Connection):
	class IntVar(Var):
		def makevar(self, c):
			var = c.var(int)
			var.setvalue(0, self.value)
			return var

	class NumberVar(Var):
		def makevar(self, c):
			var = c.var(float)
			var.setvalue(0, self.value)
			return var

	class StrVar(Var):
		def makevar(self, c):
			var = c.var(str)
			var.setvalue(0, self.value)
			return var

	class CLOBVar(Var):
		def makevar(self, c):
			from ll import orasql
			var = c.var(orasql.CLOB)
			var.setvalue(0, self.value)
			return var

	class DateVar(Var):
		def makevar(self, c):
			var = c.var(datetime.datetime)
			var.setvalue(0, self.value)
			return var

	def str(self, value=None):
		return self.StrVar(value)

	def clob(self, value=None):
		return self.CLOBVar(value)

	def int(self, value=None):
		return self.IntVar(value)

	def number(self, value=None):
		return self.NumberVar(value)

	def date(self, value=None):
		return self.DateVar(value)


class Oracle:
	ul4attrs = {"connect"}

	def connect(self, connectstring):
		from ll import orasql
		return OracleConnection(orasql.connect(connectstring, readlobs=True))


class SQLite:
	ul4attrs = {"connect"}

	def connect(self, connectstring):
		import sqlite3
		connection = sqlite3.connect(connectstring)
		class Row(sqlite3.Row):
			def __getitem__(self, key):
				if isinstance(key, str):
					key = key.encode("ascii")
				return sqlite3.Row.__getitem__(self, key)
		connection.row_factory = Row
		return Connection(connection)


class MySQL:
	ul4attrs = {"connect"}

	def connect(self, connectstring):
		import MySQLdb
		from MySQLdb import cursors
		(user, host) = connectstring.split("@")
		(user, passwd) = user.split("/")
		(host, db) = host.split("/")
		return Connection(MySQLdb.connect(user=user, passwd=passwd, host=host, db=db, use_unicode=True, cursorclass=cursors.DictCursor))


# Instantiate all "handlers"
system = System()
oracle = Oracle()
sqlite = SQLite()
mysql = MySQL()


def fixname(name):
	newname = "".join(c for (i, c) in enumerate(name) if (c.isalnum() if i else c.isalpha()) or c == "_")
	while keyword.iskeyword(newname):
		newname += "_"
	return newname


def define(arg):
	(name, _, value) = arg.partition("=")
	(name, _, type) = name.partition(":")
	if any(c != "_" and not (c.isalnum() if i else c.isalpha()) for (i, c) in enumerate(name)):
		raise argparse.ArgumentTypeError("{!r} is not a legal variable name".format(name))

	if type == "int":
		if not value:
			return (name, 0)
		try:
			return (name,  int(value))
		except ValueError:
			raise argparse.ArgumentTypeError("{!r} is not a legal integer value".format(value))
	elif type == "float":
		if not value:
			return (name, 0.)
		try:
			return (name, float(value))
		except ValueError:
			raise argparse.ArgumentTypeError("{!r} is not a legal float value".format(value))
	elif type == "bool":
		if value in ("", "0", "no", "false", "False"):
			return (name, False)
		if value in ("1", "yes", "true", "True"):
			return (name, True)
		raise argparse.ArgumentTypeError("{!r} is not a legal bool value".format(value))
	elif type == "oracle":
		return (name, oracle.connect(value))
	elif type == "sqlite":
		return (name, sqlite.connect(value))
	elif type == "mysql":
		return (name, mysql.connect(value))
	elif type and type != "str":
		raise argparse.ArgumentTypeError("{!r} is not a legal type".format(type))
	return (name, value)


def main(args=None):
	p = argparse.ArgumentParser(description="render UL4 templates with access to Oracle, MySQL or SQLite databases", epilog="For more info see http://www.livinglogic.de/Python/scripts/rul4.html")
	p.add_argument("templates", metavar="template", help="templates to be used", nargs="+")
	p.add_argument("-e", "--encoding", dest="encoding", help="Encoding for template sources (default %(default)s)", default="utf-8", metavar="ENCODING")
	p.add_argument("-w", "--keepws", dest="keepws", help="Keep linefeeds and indentation in template sources? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--oracle", dest="oracle", help="Allow the templates to connect to Oracle databases? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--sqlite", dest="sqlite", help="Allow the templates to connect to SQLite databases? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--mysql", dest="mysql", help="Allow the templates to connect to MySQL databases? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--system", dest="system", help="Allow the templates to execute system commands? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument("-D", "--define", dest="defines", metavar="var=value", help="Pass additional parameters to the template (can be specified multiple times).", action="append", type=define)

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
		template = ul4c.Template(templatestream.read(), fixname(templatename), keepws=args.keepws)
		# The first template is the main template
		if maintemplate is None:
			maintemplate = template
		templates[templatename] = template

	vars = dict(templates=templates, encoding=sys.stdout.encoding)
	if args.defines:
		vars.update(args.defines)
	if args.oracle:
		vars["oracle"] = oracle
	if args.mysql:
		vars["mysql"] = mysql
	if args.sqlite:
		vars["sqlite"] = sqlite
	if args.system:
		vars["system"] = system
	for part in maintemplate.render(**vars):
		sys.stdout.write(part)


if __name__ == "__main__":
	sys.exit(main())
