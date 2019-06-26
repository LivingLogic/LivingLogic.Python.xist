#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

"""
Purpose
=======

:program:`rul4` is a script that can be used to render an UL4 template.


The ``globals`` object
======================

Inside the template the object ``globals`` (an instance of the class
:class:`Globals`) will be available to make database connections, load and save
files, compile templates, access environment variables and parameters etc.
However access to those features can be switched off via command line
options.


Options
=======

:program:`rul4` supports the following options:

.. program:: rul4

.. option:: templates

	One or more template files. A file named ``-`` will be treated as
	standard input. The first file in the list is the main template, i.e. the
	one that gets rendered. All templates will be available in the main
	template as the ``globals.templates`` dictionary. The keys are the base names
	of the files (i.e. ``foo.ul4`` will be ``globals.templates.foo``; stdin will
	be ``globals.templates.stdin``).

.. option:: --oracle <flag>

	Provide the method :meth:`Globals.oracle` (as ``globals.oracle``) to the
	template? If switched off ``globals.oracle`` will be :const:`None`.

	(Allowed values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``;
	the default is ``true``)

.. option:: --sqlite <flag>

	Provide the method :meth:`Globals.sqlite` (as ``globals.sqlite``) to the
	template? If switched off ``globals.sqlite`` will be :const:`None`.

	(Allowed values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``;
	the default is ``true``)

.. option:: --mysql <flag>

	Provide the method :meth:`Globals.mysql` (as ``globals.mysql``) to the
	template? If switched off ``globals.mysql`` will be :const:`None`.

	(Allowed values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``;
	the default is ``true``)

.. option:: --redis <flag>

	Provide the method :meth:`Globals.redis` (as ``globals.redis``) to the
	template? If switched off ``globals.redis`` will be :const:`None`.

	(Allowed values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``;
	the default is ``true``)

.. option:: --system <flag>

	Provide the method :meth:`Globals.system` (as ``globals.system``) to the
	template? If switched off ``globals.system`` will be :const:`None`.

	(Allowed values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``;
	the default is ``true``)

.. option:: --load <flag>

	Provide the method :meth:`Globals.load` (as ``globals.load``) to the
	template? If switched off ``globals.load`` will be :const:`None`.

	(Allowed values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``;
	the default is ``true``)

.. option:: --save <flag>

	Provide the method :meth:`Globals.save` (as ``globals.save``) to the
	template? If switched off ``globals.save`` will be :const:`None`.

	(Allowed values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``;
	the default is ``true``)

.. option:: --compile <flag>

	Provide the method :meth:`Globals.compile` (as ``globals.compile``) to the
	template? If switched off ``globals.compile`` will be :const:`None`.

	(Allowed values are ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``;
	the default is ``true``)

.. option::  -e <encoding> , --encoding <encoding>

	The encoding of the templates files (default ``utf-8``)

.. option::  -w <value>, --whitespace <value>

	Specifies how to handle whitespace in the template (Allowed values are
	``keep``, ``strip``, or ``smart``). This can of course be overwritten with
	the template tag ``<?whitespace ...?>`` in the template files.

.. option:: -D, --define

	Defines an additional variable that will be available inside the template
	(e.g. the variable ``foo`` will be available as ``globals.vars.foo``).
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

			-Ddb:oracle=user/password@database

	``sqlite``
		``value`` is a connection to an SQLite database.

	``mysql``
		``value`` is a connection to a MySQL database.

	``redis``
		``value`` will be a connection to an Redis database, e.g.::

			-Ddb:redis=192.168.123.1:6379/42

		The port (i.e. the ``6379`` in the above value) is optional and
		defaults to 6379. The database number (i.e. the ``42`` in the above
		value) is also optional and defaults to 0.


Example
=======

This example shows how to connect to an Oracle database and output the content
of a ``person`` table into an XML file.

Suppose we have a database table that looks like this:

.. sourcecode:: sql

	create table person
	(
		id integer not null,
		firstname varchar2(200),
		lastname varchar2(200)
	);

Then we can use the following template to output the table into an XML file:

.. sourcecode:: xml

	<?xml version='1.0' encoding='utf-8'?>
	<?code db = globals.oracle("user/password@database')?>
	<persons>
		<?for p in db.query("select id, firstname, lastname from person order by 3, 2")?>
			<person id="<?printx p.id?>">
				<firstname><?printx p.firstname?></firstname>
				<lastname><?printx p.lastname?></lastname>
			</person>
		<?end for?>
	</persons>

If we put the template into the file :file:`person.ul4` we can call
:program:`rul4` like this:

.. sourcecode:: bash

	rul4 person.ul4 >person.xml

We could also pass the connection to our database via the :option:`-D` option
and disallow the script to make any database connections itself or execute any
system commands:

.. sourcecode:: bash

	rul4 person.ul4 -Ddb:oracle=user/password@database --oracle=0 --sqlite=0 --mysql=0 --redis=0 --system=0 >person.xml

Then the template can use the Oracle connection object :obj:`db` directly.


API
===
"""


import sys, os, argparse, datetime, keyword

from ll import ul4c, misc


__docformat__ = "reStructuredText"


class System:
	ul4attrs = {"execute"}

	def execute(self, cmd):
		return os.popen(cmd).read()


class Var:
	ul4attrs = {"value"}

	def __init__(self, value=None):
		self.value = value

	def ul4setattr(self, name, value):
		# As ``ul4attrs`` only contains ``"value"``, we will never be called with any other name
		self.value = value

	@misc.notimplemented
	def makevar(c, cursor):
		pass


class Connection:
	"""
	A :class:`Connection` object provides a database connection to an UL4
	template.

	To execute SQL the two methods :meth:`query` and :meth:`execute` are provided.

	Calling functions or procedures with out parameters can be done with variable
	objects that can be created with the methods :meth:`int`, :meth:`number`,
	:meth:`str`, :meth:`clob` and :meth:`date`. The resulting value of the out
	parameter is available from the :attr:`value` attribute of the variable
	object. The following example creates a function, calls it to get at the
	result and drops it again:

	.. sourcecode:: xml

		<?code db = oracle.connect('user/password@database')?>
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

	A :class:`Connection` object can be created with the methods
	:meth:`Globals.mysql` or :meth:`Globals.sqlite`.
	"""

	ul4attrs = {"query", "queryone", "execute", "int", "number", "str", "clob", "date"}

	def __init__(self, connection):
		self.connection = connection

	def _execute(self, cursor, queryparts):
		query = []
		params = {}
		vars = {}
		for (i, part) in enumerate(queryparts):
			if i % 2:
				name = f"value{(i+1)//2}"
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
		"""
		Execute the query passed in and return an iterator over the resulting
		records.

		At least one positional argument is required. Arguments alternate between
		fragments of the SQL query and parameters that will be embedded in the
		query. For example:

		.. sourcecode:: xml

			<?code db = globals.oracle("user/pwd@db")?>
			<?code name = "Bob"?>
			<ul>
				<?for p in db.query("select * from person where firstname=", name, " or lastname=", name)?>
					<li><?print p.firstname?> <?print p.lastname?></li>
				<?end for?>
			</ul>

		The records returned from :meth:`query` are dict-like objects mapping
		field names to field values.
		"""

		cursor = self.connection.cursor()
		self._execute(cursor, queryparts)
		return cursor

	def queryone(self, *queryparts):
		"""
		Execute the query passed in and return the first result record (or
		:const:`None` if the query didn't output any record). ``queryparts``
		is handled the same way as :meth:`query` does.
		"""

		cursor = self.connection.cursor()
		self._execute(cursor, queryparts)
		return cursor.fetchone()

	def execute(self, *queryparts):
		"""
		Similar to :meth:`query` and :meth:`queryone`, but doesn't doesn't return
		a result. This can be used to call functions or procedures.
		"""
		cursor = self.connection.cursor()
		self._execute(cursor, queryparts)

	@misc.notimplemented
	def str(self, value=None):
		"""
		Create a variable that can be used for OUT parameters of type ``varchar``.
		"""

	@misc.notimplemented
	def clob(self, value=None):
		"""
		Create a variable that can be used for OUT parameters of type ``clob``.
		"""

	@misc.notimplemented
	def int(self, value=None):
		"""
		Create a variable that can be used for OUT parameters of type ``integer``.
		"""

	@misc.notimplemented
	def number(self, value=None):
		"""
		Create a variable that can be used for OUT parameters of type ``number``.
		"""

	@misc.notimplemented
	def date(self, value=None):
		"""
		Create a variable that can be used for OUT parameters of type ``date``.
		"""


class OracleConnection(Connection):
	"""
	:class:`OracleConnection` is a subclass of :class:`Connection` that
	implements functionality that is specific to Oracle databases (e.g.
	support for variables). The inferface is the same as :class:`Connection`\s.

	An :class:`OracleConnection` object can be created with the method
	:meth:`Globals.oracle`.
	"""

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

	def __repr__(self):
		connectstring = f"{self.connection.username}@{self.connection.tnsentry}"
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} schema={connectstring!r} at {id(self):#x}>"

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


class RedisConnection:
	"""
	A connection to a Redis database. A :class:`RedisConnection` object provides
	the methods :meth:`get` to read data from the database and :meth:`set` to
	write data to the database.

	Example::

		<?code db = redis.connect("192.168.123.42/1")?>
		<?code value = db.get("key")?>
		<?if isnone(value)?>
			<?code value = "foobar"?>
			<?code db.put("key", value, timedelta(seconds=10*60))?>
		<?end if?>
	"""

	ul4attrs = {"get", "put"}

	def __init__(self, host, port, db):
		import redis
		self.connection = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

	def get(self, key):
		"""
		Return the value for the key ``key`` or ``None`` if the key doesn't exist.
		"""
		return self.connection.get(key)

	def set(self, key, data, timeout=None):
		"""
		Store the string value ``data`` under the key ``key``.

		If ``timeout`` is :const:`None` the value will be stored indefinitely.
		Otherwise it specifies when the value will expire. ``timeout`` can be
		an integer (the number of seconds) or a :class:`timedelta` object.
		"""
		if timeout is None:
			self.connection.set(key, data)
		else:
			self.connection.setex(key, timeout, data)


def fixname(name):
	newname = "".join(c for (i, c) in enumerate(name) if (c.isalnum() if i else c.isalpha()) or c == "_")
	while keyword.iskeyword(newname):
		newname += "_"
	return newname


def print_exception_chain(exc):
	print("UL4 traceback (most recent call last):", file=sys.stderr)
	for exc in reversed(list(misc.exception_chain(exc))):
		print()
		print(misc.format_exception(exc), file=sys.stderr)


class Globals:
	"""
	An instance of the :class:`Globals` class will be passed to the main template
	as the ``globals`` variable. The following attributes will be accessible to
	UL4 templates:

	``templates`` : dictionary
		A dictionary containing the templates specified on the command line. This
		will include the main template.

	``vars`` : dictionary
		A dictionary containing the variables that have been specified via the
		:option:`-D`/:option:`--define` option.

	``encoding`` : string
		The encoding that will be used for output (this is the same as
		``sys.stdout.encoding``, so it can be set with the environment variable
		:envvar:`PYTHONIOENCODING`).

	``env`` : dictionary
		A reference to :obj:`os.environ`.

	Furthermore the following methods can be called from UL4 templates:
	:meth:`error`, :meth:`log`, :meth:`oracle`, :meth:`mysql`, :meth:`sqlite`,
	:meth:`redis`, :meth:`system`, :meth:`load`, :meth:`save` and :meth:`compile`.
	"""

	ul4attrs = {"templates", "vars", "encoding", "env", "oracle", "mysql", "sqlite", "redis", "error", "log", "system", "load", "save", "compile"}
	def __init__(self, templates=None, vars=None, encoding=None, oracle=True, mysql=True, sqlite=True, redis=True, system=True, load=True, save=True, compile=True):
		self.templates = templates if templates is not None else {}
		self.encoding = encoding if encoding is not None else sys.stdout.encoding
		self.vars = vars if vars is not None else {}
		self.env = os.environ
		# Deactivate features if requested by overwriting the method with an instance attribute.
		if not oracle:
			self.oracle = None
		if not mysql:
			self.mysql = None
		if not sqlite:
			self.sqlite = None
		if not redis:
			self.redis = None
		if not system:
			self.system = None
		if not load:
			self.load = None
		if not save:
			self.save = None
		if not compile:
			self.compile = None

	def from_args(self, args):
		"""
		Sets the attributes of :obj:`self` from the object :obj:`args` (which
		must be an instance of :class:`argparse.Namespace`).

		Returns the main template.
		"""
		templates = {}
		maintemplate = None
		for templatename in args.templates:
			if templatename == "-":
				templatesource = sys.stdin.read()
				templatename = "stdin"
			else:
				with open(templatename, "r", encoding=args.encoding) as f:
					templatesource = f.read()
				templatename = os.path.basename(templatename)
				if os.path.extsep in templatename:
					templatename = templatename.rpartition(os.extsep)[0]
			templatename = fixname(templatename)
			if args.stacktrace == "short":
				try:
					template = ul4c.Template(templatesource, name=templatename, whitespace=args.whitespace)
				except Exception as exc:
					print_exception_chain(exc)
					raise SystemExit(1)
			else:
				template = ul4c.Template(templatesource, name=templatename, whitespace=args.whitespace)
			# The first template is the main template
			if maintemplate is None:
				maintemplate = template
			templates[template.name] = template
		self.templates = templates

		self.vars = dict(args.vars) if args.vars is not None else {}

		def option(name):
			if getattr(args, name):
				if getattr(self, name) is None:
					delattr(self, name)
			else:
				if getattr(self, name) is not None:
					setattr(self, name, None)

		option("oracle")
		option("mysql")
		option("sqlite")
		option("redis")
		option("system")
		option("load")
		option("save")
		option("compile")

		return maintemplate

	def error(self, message, ast=None):
		"""
		Can be called to output an error message and abort template execution.
		The signature is:

		.. sourcecode:: python

			globals.error(message, ast=None)

		``message`` is the error message and ``ast`` can be an AST node from an
		UL4 template syntax tree to print an error message that originates from
		that node.
		"""
		exc = Exception(message)
		if ast is not None:
			exc.__cause__ = ul4c.LocationError(ast)
		raise exc

	def log(self, *args, sep=" ", end="\n", flush=False):
		"""
		Logs ``args`` to ``sys.stderr``.

		The parameters ``sep``, ``end`` and ``flush`` have the same meaning as
		for :func:`print`.
		"""
		print(*args, sep=sep, end=end, file=sys.stderr, flush=flush)

	def oracle(self, connectstring):
		"""
		Return an :class:`OracleConnection` object for the Oracle connect string
		passed in::

			<?code db = globals.oracle("user/password@database")?>
			<?for row in db.query("select sysdate as sd from dual")?>
				<?print row.sd?>
			<?end for?>
		"""
		from ll import orasql
		return OracleConnection(orasql.connect(connectstring, readlobs=True))

	def mysql(self, connectstring):
		"""
		Return a :class:`Connection` object to a MySQL database for the
		connectstring passed in. The format of the connect string is::

			user/password@host/database
		"""
		import MySQLdb
		from MySQLdb import cursors
		(user, host) = connectstring.split("@")
		(user, passwd) = user.split("/")
		(host, db) = host.split("/")
		return Connection(MySQLdb.connect(user=user, passwd=passwd, host=host, db=db, use_unicode=True, cursorclass=cursors.DictCursor))

	def sqlite(self, connectstring):
		"""
		Return a :class:`Connection` object to an SQLite database for the
		connectstring passed in. The connectstring will be passed directly
		to :func:`sqlite3.connect`.
		"""
		import sqlite3
		connection = sqlite3.connect(connectstring)
		class Row(sqlite3.Row):
			def __getitem__(self, key):
				if isinstance(key, str):
					key = key.encode("ascii")
				return sqlite3.Row.__getitem__(self, key)
		connection.row_factory = Row
		return Connection(connection)

	def redis(self, connectstring):
		"""
		Return a :class:`RedisConnection` object, which provides a connection to a
		Redis database. The connectstring has the format::

			host:port/db

		``port`` is optional and defaults to 6379. ``db`` is optional too and
		defaults to 0.
		"""
		(hostport, _, db) = connectstring.partition("/")
		if not db:
			db = 0
		(host, _, port) = hostport.partition(":")
		if not port:
			port = 6379
		return RedisConnection(host=host, port=port, db=db)

	def system(self, cmd):
		"""
		Execute the system command :obj:`cmd` and returns its output, e.g.
		the template:

		.. sourcecode:: xml

			<?print globals.system("whoami")?>

		will output the user name.
		"""
		return os.popen(cmd).read()

	def load(self, filename, encoding="utf-8"):
		"""
		Read a file from disk and returns the content. :obj:`filename` is the
		filename and :obj:`encoding` is the encoding of the file. The encoding
		parameter is optional and defaults to ``"utf-8"``:

		.. sourcecode:: xml

			<?code data = globals.load("/home/user/data.txt", "iso-8859-1")?>
		"""
		with open(filename, "r", encoding=encoding) as f:
			return f.read()

	def save(self, filename, data, encoding="utf-8"):
		r"""
		Save the string :obj:`data` to a file on disk. :obj:`filename` is the
		filename and :obj:`encoding` is the encoding of the file. The encoding
		parameter is optional and defaults to ``"utf-8"``:

		.. sourcecode:: xml

			<?code globals.save("/home/user/data.txt", "foo\nbar\n", "iso-8859-1")?>
		"""
		with open(filename, "w", encoding=encoding) as f:
			f.write(data)

	def compile(self, source, name=None, whitespace="keep", signature=None, startdelim="<?", enddelim="?>"):
		"""
		Compile the UL4 source ``source`` into a :class:`~ll.ul4c.Template` object
		and return it. All other parameters are passed to the
		:class:`~ll.ul4c.Template` constructor too.
		"""
		return ul4c.Template(source, name=name, whitespace=whitespace, signature=signature, startdelim=startdelim, enddelim=enddelim)

	def define(self, arg):
		(name, _, value) = arg.partition("=")
		(name, _, type) = name.partition(":")
		if any(c != "_" and not (c.isalnum() if i else c.isalpha()) for (i, c) in enumerate(name)):
			raise argparse.ArgumentTypeError(f"{name!r} is not a legal variable name")

		if type == "int":
			if not value:
				return (name, 0)
			try:
				return (name,  int(value))
			except ValueError:
				raise argparse.ArgumentTypeError(f"{value!r} is not a legal integer value")
		elif type == "float":
			if not value:
				return (name, 0.)
			try:
				return (name, float(value))
			except ValueError:
				raise argparse.ArgumentTypeError(f"{value!r} is not a legal float value")
		elif type == "bool":
			if value in ("", "0", "no", "false", "False"):
				return (name, False)
			if value in ("1", "yes", "true", "True"):
				return (name, True)
			raise argparse.ArgumentTypeError(f"{value!r} is not a legal bool value")
		elif type == "oracle":
			return (name, self.oracle(value))
		elif type == "sqlite":
			return (name, self.sqlite(value))
		elif type == "mysql":
			return (name, self.mysql(value))
		elif type == "redis":
			return (name, self.redis(value))
		elif type and type != "str":
			raise argparse.ArgumentTypeError(f"{type!r} is not a legal type")
		return (name, value)


def main(args=None):
	globals = Globals()

	define = globals.define

	p = argparse.ArgumentParser(description="render UL4 templates with access to Oracle, MySQL, SQLite or Redis databases", epilog="For more info see http://python.livinglogic.de/scripts_rul4.html")
	p.add_argument("templates", metavar="template", help="templates to be used (first template gets rendered)", nargs="+")
	p.add_argument("-e", "--encoding", dest="encoding", help="Encoding for template sources (default %(default)s)", default="utf-8", metavar="ENCODING")
	p.add_argument("-w", "--whitespace", dest="whitespace", help="How to treat whitespace in template sources? (default %(default)s)", choices=("keep", "strip", "smart"), default="smart")
	p.add_argument("-t", "--stacktrace", dest="stacktrace", help="How to display stack traces in case of an error? (default %(default)s)", choices=("full", "short"), default="short")
	p.add_argument(      "--oracle", dest="oracle", help="Allow the templates to connect to Oracle databases? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--sqlite", dest="sqlite", help="Allow the templates to connect to SQLite databases? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--mysql", dest="mysql", help="Allow the templates to connect to MySQL databases? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--redis", dest="redis", help="Allow the templates to connect to Redis databases? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--system", dest="system", help="Allow the templates to execute system commands? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--load", dest="load", help="Allow the templates to load data from arbitrary paths? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--save", dest="save", help="Allow the templates to save data to arbitrary paths? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument(      "--compile", dest="compile", help="Allow the templates access to the compile function? (default %(default)s)", action=misc.FlagAction, default=True)
	p.add_argument("-D", "--define", dest="vars", metavar="var=value", help="Pass additional parameters to the template (can be specified multiple times).", action="append", type=define)

	args = p.parse_args(args)

	maintemplate = globals.from_args(args)

	if args.stacktrace == "short":
		try:
			for part in maintemplate.render(globals=globals):
				sys.stdout.write(part)
		except Exception as exc:
			print_exception_chain(exc)
			return 1
	else:
		for part in maintemplate.render(globals=globals):
			sys.stdout.write(part)


if __name__ == "__main__":
	sys.exit(main())
