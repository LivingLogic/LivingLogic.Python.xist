# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`!ll.postsql` contains utilities for working with Postgres__:

*	It allows calling procedures and functions with keyword arguments (via the
	classes :class:`Procedure` and :class:`Function`).

*	The default cursor class will return results a named tuples.

*	The :class:`Connection` class provides methods for iterating through the
	database metadata.

*	Importing this module adds support for URLs with the scheme ``postgres`` to
	:mod:`ll.url`. Examples of these URLs are::

		postgres://user:pwd@db/
		postgres://user:pwd@db/view/
		postgres://user:pwd@db/view/USER_TABLES.sql
		postgres://sys:pwd:sysdba@db/

__ https://www.postgresql.org/
"""

import datetime, collections, errno

import psycopg2
from psycopg2 import extras, extensions, errors

from ll import misc, url as url_


__docformat__ = "reStructuredText"


bigbang = datetime.datetime(1970, 1, 1, 0, 0, 0) # timestamp for Postgres "directories"


###
### Exceptions
###

class SQLObjectNotFoundError(IOError):
	def __init__(self, obj):
		super().__init__(errno.ENOENT, f"no such {obj.type}: {obj.name}")
		self.obj = obj


###
### Helper classes and functions
###


def split_comma(sql):
	result = []
	instring = 0
	inparens = 0

	startpos = 0
	for (pos, c) in enumerate(sql):
		if c == "," and not instring and not inparens:
			if pos != startpos:
				result.append(sql[startpos:pos].strip())
			startpos = pos+1
		elif instring == 1:
			if c == "'":
				instring = 2
		elif instring == 2:
			instring = 1 if c == "'" else 0
		elif c == "(":
			inparens += 1
		elif c == ")":
			inparens -= 1
	if startpos < len(sql):
		result.append(sql[startpos:].strip())
	return result


def sqlstr(s):
	s = s.replace("'", "''")
	return f"'{s}'"


class _SQL:
	"""
	Helper class for constructing SQL queries.
	"""
	def __init__(self, s=None, f=None, j=None, lj=None, w=None, o=None):
		self.selects = []
		self.froms = []
		self.joins = []
		self.leftjoins = []
		self.wheres = []
		self.orderbys = []
		if s is not None:
			if isinstance(s, str):
				self.selects.append(s)
			else:
				self.selects.extend(s)
		if f is not None:
			if isinstance(f, str):
				self.froms.append(f)
			else:
				self.froms.extend(f)
		if j is not None:
			if isinstance(j, str):
				self.joins.append(j)
			else:
				self.joins.extend(j)
		if lj is not None:
			if isinstance(lj, str):
				self.leftjoins.append(lj)
			else:
				self.leftjoins.extend(lj)
		if w is not None:
			if isinstance(w, str):
				self.wheres.append(w)
			else:
				self.wheres.extend(w)
		if o is not None:
			if isinstance(o, str):
				self.orderbys.append(o)
			else:
				self.orderbys.extend(o)

	def __str__(self):
		selects = ", ".join(self.selects)
		froms = ", ".join(self.froms)
		joins = " ".join(f"join {j}" for j in self.joins)
		if joins:
			joins = f" {joins}"
		leftjoins = ", ".join(f"left outer join {j}" for j in self.leftjoins)
		if leftjoins:
			leftjoins = f" {leftjoins}"
		wheres = " and ".join(self.wheres)
		if wheres:
			wheres = f" where {wheres}"
		orderbys = ", ".join(self.orderbys)
		if orderbys:
			orderbys = f" order by {orderbys}"
		return f"select {selects} from {froms}{joins}{leftjoins}{wheres}{orderbys}"

	def s(self, *expressions):
		self.selects.extend(expressions)
		return self

	def f(self, *froms):
		self.froms.extend(froms)
		return self

	def j(self, *joins):
		self.joins.extend(joins)
		return self

	def lj(self, *joins):
		self.leftjoins.extend(joins)
		return self

	def w(self, *wheres):
		self.wheres.extend(wheres)
		return self

	def o(self, *orderbys):
		self.orderbys.extend(orderbys)
		return self


def _schemaquery(*fields, nsp=False):
	sql = _SQL(
		s=fields,
		f="pg_catalog.pg_namespace n"
	)
	if nsp:
		sql.w("n.nspname = %s")
	else:
		sql.w("n.nspname not like 'pg_%'", "n.nspname != 'information_schema'").o("n.nspname")
	return str(sql)


def _domainquery(*fields, nsp=False, domain=False):
	sql = _SQL(
		s=fields,
		f="pg_catalog.pg_namespace n",
		j="pg_catalog.pg_type t on n.oid = t.typnamespace",
		w="t.typtype = 'd'",
	)
	if nsp:
		sql.w("n.nspname = %s")
		if domain:
			sql.w("t.typname = %s")
		else:
			sql.o("t.typname")
	else:
		sql.w("n.nspname not like 'pg_%'", "n.nspname != 'information_schema'").o("n.nspname", "t.typname")
	return str(sql)


def _relquery(*fields, relkind, nsp=False, rel=False):
	sql = _SQL(
		s=fields,
		f="pg_catalog.pg_namespace n",
		j="pg_catalog.pg_class r on n.oid = r.relnamespace",
		w=(f"r.relkind = '{relkind}'", ),
	)
	if nsp:
		sql.w("n.nspname = %s")
		if rel:
			sql.w("r.relname = %s")
		else:
			sql.o("r.relname")
	else:
		sql.w("n.nspname not like 'pg_%'", "n.nspname != 'information_schema'").o("n.nspname", "r.relname")
	return str(sql)


def _proquery(*fields, prokind, nsp=False, pro=False, lan=False):
	sql = _SQL(
		s=fields,
		f="pg_catalog.pg_namespace n",
		j="pg_catalog.pg_proc p on n.oid = p.pronamespace",
	)
	if lan:
		sql.j("pg_catalog.pg_language l on p.prolang = l.oid")
	if prokind is not None:
		sql.w(f"p.prokind {prokind}")
	if nsp:
		sql.w("n.nspname = %s")
		if pro:
			sql.w("p.proname = %s")
		else:
			sql.o("p.proname")
	else:
		sql.w("n.nspname not like 'pg_%'", "n.nspname != 'information_schema'").o("n.nspname", "p.proname")
	return str(sql)


def _indquery(*fields, nsp=False, rel=False, ind=False):
	sql = _SQL(
		s=fields,
		f="pg_catalog.pg_namespace n",
		j=(
			"pg_catalog.pg_class c on n.oid = c.relnamespace",
			"pg_catalog.pg_index i on c.oid = i.indexrelid",
		),
		w="not i.indisprimary",
	)
	if nsp:
		sql.w("n.nspname = %s")
		if rel:
			sql.j("pg_catalog.pg_class ct on i.indrelid = ct.oid").w("ct.relname = %s").o("c.relname")
		elif ind:
			sql.w("c.relname = %s")
		else:
			sql.o("c.relname")
	else:
		sql.w("n.nspname not like 'pg_%'", "n.nspname != 'information_schema'").o("n.nspname", "c.relname")
	return str(sql)


def _attquery(*fields, relkind, nsp=False, rel=False, att=False):
	sql = _SQL(
		s=fields,
		f="pg_catalog.pg_namespace n",
		j=(
			"pg_catalog.pg_class c on n.oid = c.relnamespace",
			"pg_catalog.pg_attribute a on c.oid = a.attrelid",
		),
		w=(
			"a.attnum > 0",
			"not a.attisdropped",
			f"c.relkind = '{relkind}'"
		)
	)
	if nsp:
		sql.w("n.nspname = %s")
		if rel:
			sql.w("c.relname = %s")
			if att:
				sql.w("a.attname = %s")
			else:
				sql.o("a.attnum")
		else:
			sql.o("c.relname", "a.attnum")
	else:
		sql.w("n.nspname not like 'pg_%'", "n.nspname != 'information_schema'").o("n.nspname", "c.relname", "a.attnum")
	return str(sql)

def _tgquery(*fields, nsp=False, rel=False, tg=False):
	sql = _SQL(
		s=fields,
		f="pg_catalog.pg_namespace n",
		j=(
			"pg_catalog.pg_class c on n.oid = c.relnamespace",
			"pg_catalog.pg_trigger t on c.oid = t.tgrelid",
		),
		w="not t.tgisinternal"
	)
	if nsp:
		sql.w("n.nspname = %s")
		if rel:
			sql.w("c.relname = %s")
			if tg:
				sql.w("t.tgname = %s")
			else:
				sql.o("t.tgname")
		else:
			sql.o("c.relname", "t.tgname")
	else:
		sql.w("n.nspname not like 'pg_%'", "n.nspname != 'information_schema'").o("n.nspname", "c.relname", "t.tgname")
	return str(sql)


def _conquery(*fields, contype=None, nsp=False, rel=False, con=False):
	sql = _SQL(
		s=fields,
		f="pg_catalog.pg_namespace n",
		j="pg_catalog.pg_constraint c on c.connamespace = n.oid"
	)
	if contype is not None:
		sql.w(f"contype = '{contype}'")
	if nsp:
		sql.w("n.nspname = %s")
		if rel:
			sql.w("c.relname = %s")
		elif con:
			sql.w("c.conname = %s")
		else:
			sql.o("c.conname")
	else:
		sql.w("n.nspname not like 'pg_%'", "n.nspname != 'information_schema'").o("n.nspname", "c.conname")
	return str(sql)


###
### :mod:ll.postsql` version of connections and cursors
###

class Connection(extensions.connection):
	def __repr__(self):
		status = "closed" if self.closed else "open"
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} dsn={self.dsn!r} {status} at {id(self):#x}>"

	def __str__(self):
		return repr(self)

	def schemas(self):
		c = self.cursor()
		c.execute(_schemaquery("nspname"))
		for r in c:
			yield Schema(r.nspname, self)

	def domains(self):
		c = self.cursor()
		c.execute(_domainquery("n.nspname || '.' || t.typname as name"))
		for r in c:
			yield Domain(r.name, c.connection)

	def tables(self):
		c = self.cursor()
		c.execute(_relquery("n.nspname || '.' || r.relname as name", relkind="r"))
		for r in c:
			yield Table(r.name, self)

	def table_columns(self):
		c = self.cursor()
		c.execute(_attquery("n.nspname || '.' || c.relname || '.' || a.attname as name", relkind='r'))
		for r in c:
			yield Table.Column(r.name, c.connection)

	def indexes(self):
		c = self.cursor()
		c.execute(_indquery("n.nspname || '.' || c.relname as name"))
		for r in c:
			yield Index(r.name, self)

	def triggers(self):
		c = self.cursor()
		c.execute(_tgquery("n.nspname || '.' || c.relname || '.' || t.tgname as name"))
		for r in c:
			yield Trigger(r.name, c.connection)

	def pks(self):
		c = self.cursor()
		c.execute(_conquery("n.nspname || '.' || c.conname as name", contype="p"))
		for r in c:
			yield PrimaryKey(r.name, c.connection)

	def fks(self):
		c = self.cursor()
		c.execute(_conquery("n.nspname || '.' || c.conname as name", contype="f"))
		for r in c:
			yield ForeignKey(r.name, c.connection)

	def unique_constraints(self):
		c = self.cursor()
		c.execute(_conquery("n.nspname || '.' || c.conname as name", contype="u"))
		for r in c:
			yield ForeignKey(r.name, c.connection)

	def check_constraints(self):
		c = self.cursor()
		c.execute(_conquery("n.nspname || '.' || c.conname as name", contype="c"))
		for r in c:
			yield CheckConstraint(r.name, c.connection)

	def constraints(self):
		c = self.cursor()
		c.execute(_conquery("c.contype", "n.nspname || '.' || c.conname as name"))
		for r in c:
			type = Constraint.types[r.contype]
			yield type(r.name, c.connection)

	def views(self):
		c = self.cursor()
		c.execute(_relquery("n.nspname || '.' || r.relname as name", relkind="v"))
		for r in c:
			yield View(r.name, self)

	def view_columns(self):
		c = self.cursor()
		c.execute(_attquery("n.nspname || '.' || c.relname || '.' || a.attname as name", relkind='v'))
		for r in c:
			yield View.Column(r.name, c.connection)

	def sequences(self):
		c = self.cursor()
		c.execute(_relquery("n.nspname || '.' || r.relname as name", relkind="S"))
		for r in c:
			yield Sequence(r.name, self)

	def callables(self):
		c = self.cursor()
		c.execute(_proquery("p.prokind", "n.nspname || '.' || p.proname as name", prokind="in ('f', 'p')"))
		for r in c:
			if r.prokind == "f":
				yield Function(r.name, self)
			else:
				yield Procedure(r.name, self)

	def procedures(self):
		c = self.cursor()
		c.execute(_proquery("n.nspname || '.' || p.proname as name", prokind="= 'p'"))
		for r in c:
			yield Procedure(r.name, self)

	def functions(self):
		c = self.cursor()
		c.execute(_proquery("n.nspname || '.' || p.proname as name", prokind="= 'f'"))
		for r in c:
			yield Function(r.name, self)

	def objects(self):
		raise NotImplementedError

	def getobject(self, name):
		raise NotImplementedError


class Cursor(extras.NamedTupleCursor):
	def __repr__(self):
		status = "closed" if self.closed else "open"
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} dsn={self.connection.dsn!r} query={self.query!r} {status} at {id(self):#x}>"


def connect(dsn=None, connection_factory=Connection, cursor_factory=Cursor, **kwargs):
	return psycopg2.connect(dsn=dsn, connection_factory=connection_factory, cursor_factory=cursor_factory, **kwargs)


###
### Classes for all types of objects in a Postgres database
###

class ObjectMeta(type):
	def __new__(mcl, name, bases, dict):
		cls = type.__new__(mcl, name, bases, dict)
		if "names" in dict:
			names = cls.__qualname__.replace(".", "")
			cls.names = collections.namedtuple(f"{names}Names", dict["names"].split("."))
		return cls


class Object(metaclass=ObjectMeta):
	def __init__(self, name, connection=None):
		self.name = name
		self.names = self.__class__.names._make(name.split("."))
		self.connection = connection

	def __repr__(self):
		if self.connection is None:
			return f"<{self.__class__.__module__}.{self.__class__.__qualname__} {self.name} at {id(self):#x}>"
		else:
			return f"<{self.__class__.__module__}.{self.__class__.__qualname__} {self.name} dsn={self.connection.dsn!r} at {id(self):#x}>"

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.name == other.name

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.__class__.__module__) ^ hash(self.__class__.__qualname__) ^ hash(self.name)

	def getconnection(self, connection):
		if connection is None:
			connection = self.connection
		if connection is None:
			raise TypeError("no connection available")
		return connection

	def getcursor(self, connection):
		return self.getconnection(connection).cursor()

	def exists(self, connection=None):
		raise NotImplementedError

	def references(self, connection=None, done=None):
		"""
		Objects directly used by ``self``.

		If ``connection`` is not :const:`None` it will be used as the database
		connection from which to fetch data. If ``connection`` is :const:`None`
		the connection from which ``self`` has been extracted will be used. If
		there is not such connection, you'll get an exception.
		"""
		raise NotImplementedError

	def referencesall(self, connection=None, done=None):
		"""
		All objects used by ``self`` (recursively).

		For the meaning of ``connection`` see :meth:`references`.

		``done`` is used internally and shouldn't be passed.
		"""
		if done is None:
			done = set()
		if self not in done:
			done.add(self)
			for obj in self.references(connection):
				yield from obj.referencesall(connection, done)
			yield self

	def referencedby(self, connection=None):
		"""
		Objects using ``self``.

		For the meaning of ``connection`` see :meth:`references`.
		"""
		raise NotImplementedError

	def referencedbyall(self, connection=None, done=None):
		raise NotImplementedError


class CommentObject(Object):
	def createsql(self, connection=None):
		c = self.getcursor(connection)
		r = self._query(c)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return self._sql(r, r.comment)

	def dropsql(self, connection=None):
		c = self.getcursor(connection)
		r = self._query(c)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return self._sql(r, None)

	def exists(self, connection=None):
		c = self.getcursor(connection)
		r = self._query(c)
		r = c.fetchone()
		return r is not None

	def _sql(self, record, comment):
		type = self.type.rsplit(None, 1)[0]
		return self._makesql(f"{type} {self.name}", comment)

	def _makesql(self, basesql, comment):
		sql = f"comment on {basesql} is"
		if comment is None:
			sql += " null;"
		elif "\n" in comment:
			sql += f"\n{sqlstr(comment)};"
		else:
			sql += f" {sqlstr(comment)};"
		return sql

	def referencedby(self, connection=None, done=None):
		if False:
			yield None


class CommentedObject(Object):
	def comment(self, connection=None):
		return self.Comment(self.name, connection or self.connection)

	def dropsql(self, connection=None, missing_ok=False):
		sql = f"drop {self.type}"
		if missing_ok:
			sql += " if exists"
		sql += f" {self.name};"
		return sql


class Schema(CommentedObject):
	type = "schema"
	names = "schema"

	class Comment(CommentObject):
		type = "schema"
		names = "schema"

		def _query(self, cursor):
			cursor.execute(_schemaquery("obj_description(oid, 'pg_namespace') as comment", nsp=True), self.names)

	def oid(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_schemaquery("oid", nsp=True), self.names)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return r.oid

	def domains(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_domainquery("n.nspname || '.' || t.typname as name", nsp=True), self.names)
		for r in c:
			yield Domain(r.name, c.connection)

	def tables(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_relquery("n.nspname || '.' || r.relname as name", relkind="r", nsp=True), self.names)
		for r in c:
			yield Table(r.name, c.connection)

	def table_columns(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_attquery("n.nspname || '.' || c.relname || '.' || a.attname as name", relkind='r', nsp=True), self.names)
		for r in c:
			yield Table.Column(r.name, c.connection)

	def indexes(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_indquery("n.nspname || '.' || c.relname as name", nsp=True), self.names)
		for r in c:
			yield Index(r.name, c.connection)

	def triggers(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_tgquery("n.nspname || '.' || c.relname || '.' || t.tgname as name", nsp=True), self.names)
		for r in c:
			yield Trigger(r.name, c.connection)

	def pks(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_conquery("n.nspname || '.' || c.conname as name", contype="p", nsp=True), self.names)
		for r in c:
			yield PrimaryKey(r.name, c.connection)

	def fks(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_conquery("n.nspname || '.' || c.conname as name", contype="f", nsp=True), self.names)
		for r in c:
			yield ForeignKey(r.name, c.connection)

	def unique_constraints(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_conquery("n.nspname || '.' || c.conname as name", contype="u", nsp=True), self.names)
		for r in c:
			yield UniqueConstraint(r.name, c.connection)

	def check_constraints(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_conquery("n.nspname || '.' || c.conname as name", contype="c", nsp=True), self.names)
		for r in c:
			yield CheckConstraint(r.name, c.connection)

	def constraints(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_conquery("c.contype", "n.nspname || '.' || c.conname as name", nsp=True), self.names)
		for r in c:
			type = Constraint.types[r.contype]
			yield type(r.name, c.connection)

	def views(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_relquery("n.nspname || '.' || r.relname as name", relkind="v", nsp=True), self.names)
		for r in c:
			yield View(r.name, c.connection)

	def view_columns(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_attquery("n.nspname || '.' || c.relname || '.' || a.attname as name", relkind='v', nsp=True), self.names)
		for r in c:
			yield View.Column(r.name, c.connection)

	def sequences(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_relquery("n.nspname || '.' || r.relname as name", relkind="S", nsp=True), self.names)
		for r in c:
			yield Sequence(r.name, c.connection)

	def callables(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_proquery("p.prokind", "n.nspname || '.' || p.proname as name", prokind="in ('f', 'p')", nsp=True), self.names)
		for r in c:
			if r.prokind == "f":
				yield Function(r.name, c.connection)
			else:
				yield Procedure(r.name, c.connection)

	def procedures(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_proquery("n.nspname || '.' || p.proname as name", prokind="= 'p'", nsp=True), self.names)
		for r in c:
			yield Procedure(r.name, c.connection)

	def functions(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_proquery("n.nspname || '.' || p.proname as name", prokind="= 'f'", nsp=True), self.names)
		for r in c:
			yield Function(r.name, c.connection)

	def createsql(self, connection=None, exists_ok=False):
		if self.name != "public":
			sql = "create schema"
			if exists_ok:
				sql += " if not exists"
			sql += f" {self.name};"
			return sql
		else:
			return None

	def dropsql(self, connection=None, missing_ok=False, cascade=False):
		if self.name != "public":
			sql = "drop schema"
			if missing_ok:
				sql += " if exists"
			sql += f" {self.name}"
			if cascade:
				sql += " cascade"
			sql += ";"
			return sql
		else:
			return None


class Domain(CommentedObject):
	type = "domain"
	names = "schema.domain"

	class Comment(CommentObject):
		type = "domain"
		names = "schema.domain"

		def _query(self, cursor):
			cursor.execute(_domainquery("obj_description(t.oid, 'pg_type') as comment", nsp=True, domain=True), self.names)

	def oid(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_domainquery("t.oid", nsp=True, domain=True), self.names)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return r.oid

	def createsql(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_domainquery("typnotnull", "pg_catalog.format_type(typbasetype, typtypmod) as domain_def", nsp=True, domain=True), self.names)

		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		notnull = " not null" if r.typnotnull else ""
		return f"create domain {self.name} {r.domain_def}{notnull};"


class ColumnObject(CommentedObject):
	class Comment(CommentObject):
		def _query(self, cursor):
			cursor.execute(_attquery("col_description(c.oid, a.attnum) as comment", relkind=self.relkind, nsp=True, rel=True, att=True), self.names)

	def datatype(self, connection=None):
		raise NotImplementedError

	def default(self, connection=None):
		raise NotImplementedError

	def nullable(self, connection=None):
		raise NotImplementedError


class Table(CommentedObject):
	type = "table"
	names = "schema.table"

	class Comment(CommentObject):
		type = "table comment"
		names = "schema.table"

		def _query(self, cursor):
			cursor.execute(_relquery("obj_description(r.oid, 'pg_class') as comment", relkind="r", nsp=True, rel=True), self.names)

	class Column(ColumnObject):
		type = "table column"
		names = "schema.table.column"
		relkind = "r"

		class Comment(ColumnObject.Comment):
			type = "table column comment"
			names = "schema.table.column"
			relkind = "r"

		def table(self, connection=None):
			raise NotImplementedError

		def addsql(self, connection=None, exists_ok=False):
			c = self.getcursor(connection)
			c.execute("""
				select
					a.attnotnull,
					pg_catalog.format_type(a.atttypid, a.atttypmod) as column_type,
					case
						when d.adrelid is not null then pg_catalog.pg_get_expr(d.adbin, d.adrelid)
						else null
					end as default_value
				from
					pg_catalog.pg_namespace n,
					pg_catalog.pg_class c
				join
					pg_catalog.pg_attribute a on c.oid = a.attrelid and a.attnum > 0 and not a.attisdropped
				left outer join
					pg_catalog.pg_attrdef d on d.adrelid = a.attrelid and d.adnum = a.attnum and a.atthasdef
				where
					n.oid = c.relnamespace and
					c.relkind = 'r' and
					n.nspname = %s and 
					c.relname = %s and
					a.attname = %s
				order by
					attnum
			""", self.names)
			r = c.fetchone()
			if r is None:
				raise SQLObjectNotFoundError(self)
			sql = f"alter table {self.names[0]}.{self.names[1]} add column"
			if exists_ok:
				sql += " if not exists"
			sql += f" {self.names[2]} {r.column_type}"
			if r.attnotnull:
				sql += " not null"
			sql += ";"
			return sql

		def dropsql(self, connection=None, missing_ok=False, cascade=False):
			sql = f"alter table {self.names.schema}.{self.names.table} drop column"
			if missing_ok:
				sql += " if exists"
			sql += f" {self.names[2]}"
			if cascade:
				sql += " cascade"
			sql += ";"
			return sql

	def oid(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_relquery("r.oid", relkind="r", nsp=True, rel=True), self.names)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return r.oid

	def columns(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_attquery("n.nspname || '.' || c.relname || '.' || a.attname as name", relkind='r', nsp=True, rel=True), self.names)
		for r in c:
			yield self.Column(r.name, c.connection)

	def indexes(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_indquery("n.nspname || '.' || c.relname as name", nsp=True, rel=True), self.names)
		for r in c:
			yield Index(r.name, c.connection)

	def triggers(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_tgquery("n.nspname || '.' || c.relname || '.' || t.tgname as name", nsp=True, rel=True), self.names)
		for r in c:
			yield Trigger(r.name, c.connection)

	def pk(self, connection=None):
		c = self.getcursor(connection)
		oid = self.oid(c.connection)
		c.execute("""
			select
				c.conname
			from
				pg_catalog.pg_constraint c
			where
				conrelid = %s and
				contype = 'p'
		""", [oid])
		r = c.fetchone()
		if r is None:
			return None
		else:
			return PrimaryKey(f"{self.names.schema}.{r.conname}", c.connection)

	def fks(self, connection=None):
		c = self.getcursor(connection)
		oid = self.oid(c.connection)

		c.execute("""
			select
				c.conname
			from
				pg_catalog.pg_constraint c
			where
				conrelid=%s and
				contype = 'f'
		""", [oid])
		for r in c:
			yield ForeignKey(f"{self.names.schema}.{r.conname}", c.connection)

	def unique_constraints(self, connection=None):
		c = self.getcursor(connection)
		oid = self.oid(c.connection)

		c.execute("""
			select
				c.conname
			from
				pg_catalog.pg_constraint c
			where
				conrelid=%s and
				contype = 'u'
		""", [oid])
		for r in c:
			yield UniqueConstraint(f"{self.names.schema}.{r.conname}", c.connection)

	def check_constraints(self, connection=None):
		c = self.getcursor(connection)
		oid = self.oid(c.connection)

		c.execute("""
			select
				c.conname
			from
				pg_catalog.pg_constraint c
			where
				conrelid=%s and
				contype = 'c'
		""", [oid])
		for r in c:
			yield CheckConstraint(f"{self.names.schema}.{r.conname}", c.connection)

	def constraints(self, connection=None):
		c = self.getcursor(connection)
		oid = self.oid(c.connection)

		c.execute("""
			select
				c.contype,
				c.conname
			from
				pg_catalog.pg_constraint c
			where
				conrelid=%s
		""", [oid])
		for r in c:
			type = Constraint.types[r.contype]
			yield type(f"{self.names.schema}.{r.conname}", c.connection)

	def records(self, connection=None):
		c = self.getcursor(connection)
		c.execute(f"select * from {self.name};")
		for r in c:
			yield r

	def createsql(self, connection=None):
		c = self.getcursor(connection)

		oid = self.oid(c.connection)
		c.execute("""
			select
				a.attname,
				a.attnum,
				a.attnotnull,
				pg_catalog.format_type(a.atttypid, a.atttypmod) as column_type,
				case
					when d.adrelid is not null then pg_catalog.pg_get_expr(d.adbin, d.adrelid)
					else null
				end as default_value
			from
				pg_catalog.pg_class c
			join
				pg_catalog.pg_attribute a on c.oid = a.attrelid and a.attnum > 0 and not a.attisdropped
			left outer join
				pg_catalog.pg_attrdef d on d.adrelid = a.attrelid and d.adnum = a.attnum and a.atthasdef
			where
				c.oid = %s
			order by
				attnum
		""", [oid])

		sql = f"create table {self.name}\n"
		sql += f"(\n"
		for (last, column) in misc.islast(c):
			column_term = "" if last else ","
			notnull = " not null" if column.attnotnull else ""
			default = f" default {column.default_value}" if column.default_value is not None else ""
			sql += f"\t{column.attname} {column.column_type}{default}{notnull}{column_term}\n"
		sql += f");"
		return sql

	def mview(self, connection=None):
		raise NotImplementedError

	def ismview(self, connection=None):
		raise NotImplementedError


class Index(CommentedObject):
	type = "index"
	names = "schema.index"

	class Comment(CommentObject):
		type = "index comment"
		names = "schema.index"

		def _query(self, cursor):
			cursor.execute(_indquery("obj_description(c.oid, 'pg_class') as comment", nsp=True, ind=True), self.names)

	def oid(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_indquery("c.oid", nsp=True, ind=True), self.names)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return r.oid

	def createsql(self, connection=None, exists_ok=False):
		c = self.getcursor(connection)
		c.execute("""
			select
				pg_catalog.pg_get_indexdef(i.indexrelid) as index_def
			from
				pg_catalog.pg_namespace n,
				pg_catalog.pg_class c,
				pg_catalog.pg_index i
			where
				n.oid = c.relnamespace and
				c.oid = i.indexrelid and
				n.nspname = %s and
				c.relname = %s and
				not i.indisprimary
		""", self.names)
		sql = c.fetchone().index_def
		(prefix, sql) = sql.split(None, 1)
		if prefix.lower() != "create":
			raise ValueError(f"Can't parse index {self.name}")
		(prefix, sql) = sql.split(None, 1)
		if prefix.lower() == "unique":
			(prefix, sql) = sql.split(None, 1)
			unique = " unique"
		else:
			unique = ""
		if prefix.lower() != "index":
			raise ValueError(f"Can't parse index {self.name}")
		exists_ok = " if not exists" if exists_ok else ""
		return f"create{unique} index{exists_ok} {sql};"

	def dropsql(self, connection=None, missing_ok=False, cascade=False):
		sql = "drop index"
		if missing_ok:
			sql += " if exists"
		sql = f" {self.name}"
		if cascade:
			sql += " cascade"
		sql += ";"
		return sql

	def rebuildsql(self, connection=None):
		raise NotImplementedError

	def constraint(self, connection=None):
		raise NotImplementedError

	def isconstraint(self, connection=None):
		raise NotImplementedError

	def table(self, connection=None):
		raise NotImplementedError

	def columns(self, connection=None):
		raise NotImplementedError


class Trigger(CommentedObject):
	type = "trigger"
	names = "schema.table.trigger"

	class Comment(CommentObject):
		type = "trigger comment"
		names = "schema.table.trigger"

		def _sql(self, record, comment):
			return self._makesql(f"trigger {self.names.trigger} on {self.names.schema}.{self.names.table}", comment)

		def _query(self, cursor):
			cursor.execute(_tgquery("obj_description(t.oid) as comment", nsp=True, rel=True, tg=True), self.names)

	def createsql(self, connection=None):
		c = self.getcursor(connection)
		c.execute("""
			select
				pg_get_triggerdef(t.oid, true) as trigger_def
			from
				pg_catalog.pg_namespace n,
				pg_catalog.pg_class c,
				pg_catalog.pg_trigger t
			where
				n.oid = c.relnamespace and
				c.oid = t.tgrelid and
				n.nspname = %s and
				c.relname = %s and
				t.tgname = %s and
				not t.tgisinternal
		""", self.names)

		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return f"{r.trigger_def};"


	def dropsql(self, connection=None, missing_ok=False, cascade=False):
		sql = "drop trigger"
		if missing_ok:
			sql += " if exists"
		sql += f" {self.names.trigger} on {self.names.table}.{self.names.schema}"
		if cascade:
			sql += " cascade"
		sql += ";"
		return sql


class Constraint(CommentedObject):
	class Comment(CommentObject):
		def _query(self, cursor):
			cursor.execute(f"""
			select
				r.relname,
				obj_description(c.oid) as comment
			from
				pg_catalog.pg_namespace n,
				pg_catalog.pg_constraint c,
				pg_catalog.pg_class r
			where
				n.oid = c.connamespace and
				c.conrelid = r.oid and
				n.nspname = %s and
				c.conname = %s and
				c.contype = '{self.contype}'
			""", self.names)

		def _sql(self, record, comment):
			return self._makesql(f"constraint {self.names[1]} on {self.names[0]}.{record.relname}", comment)

	def oid(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_conquery("c.oid", contype=self.contype, nsp=True, con=True), self.names)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return r.oid

	def createsql(self, connection=None):
		c = self.getcursor(connection)
		c.execute(f"""
			select
				r.relname,
				pg_catalog.pg_get_constraintdef(c.oid, true) as constraint_def
			from
				pg_catalog.pg_namespace n,
				pg_catalog.pg_constraint c,
				pg_catalog.pg_class r
			where
				n.oid = c.connamespace and
				c.conrelid = r.oid and
				n.nspname = %s and
				c.conname = %s and
				c.contype = '{self.contype}'
		""", self.names)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return f"alter table {self.names[0]}.{r.relname} add constraint {self.names[1]} {r.constraint_def};"

	def dropsql(self, connection=None, missing_ok=False):
		c = self.getcursor(connection)
		c.execute(f"""
			select
				r.relname
			from
				pg_catalog.pg_namespace n,
				pg_catalog.pg_constraint c,
				pg_catalog.pg_class r
			where
				n.oid = c.connamespace and
				c.conrelid = r.oid and
				n.nspname = %s and
				c.conname = %s and
				c.contype = '{self.contype}'
		""", self.names)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		sql = f"alter table {self.names[0]}.{r.relname} drop constraint"
		if missing_ok:
			sql += " if exists"
		sql += f" {self.names[1]};"
		return sql

	def enablesql(self, connection=None):
		c = self.getcursor(connection)
		raise NotImplementedError

	def disablesql(self, connection=None):
		c = self.getcursor(connection)
		raise NotImplementedError

	def isenabled(self, connection=None):
		c = self.getcursor(connection)
		raise NotImplementedError

	def table(self, connection=None):
		c = self.getcursor(connection)
		raise NotImplementedError

class PrimaryKey(Constraint):
	type = "primary key"
	names = "schema.pk"
	contype = "p"

	class Comment(Constraint.Comment):
		type = "primary key comment"
		names = "schema.pk"
		contype = "p"

	def columns(self, connection=None):
		raise NotImplementedError


class ForeignKey(Constraint):
	type = "foreign key"
	names = "schema.fk"
	contype = "f"

	class Comment(Constraint.Comment):
		type = "foreign key comment"
		names = "schema.fk"
		contype = "f"

	def columns(self, connection=None):
		raise NotImplementedError

	def refconstraint(self, connection=None):
		raise NotImplementedError


class UniqueConstraint(Constraint):
	type = "unique constraint"
	names = "schema.constraint"
	contype = "u"

	class Comment(Constraint.Comment):
		type = "unique constraint comment"
		names = "schema.constraint"
		contype = "u"

	def columns(self, connection=None):
		raise NotImplementedError


class CheckConstraint(Constraint):
	type = "check constraint"
	names = "schema.constraint"
	contype = "c"

	class Comment(Constraint.Comment):
		type = "check constraint comment"
		names = "schema.constraint"
		contype = "c"


Constraint.types = dict(
	p=PrimaryKey,
	f=ForeignKey,
	u=UniqueConstraint,
	c=CheckConstraint,
)


class View(CommentedObject):
	type = "view"
	names = "schema.view"

	class Comment(CommentObject):
		type = "view comment"
		names = "schema.view"

		def _query(self, cursor):
			cursor.execute(_relquery("obj_description(r.oid, 'pg_class') as comment", relkind="v", nsp=True, rel=True), self.names)

	class Column(ColumnObject):
		type = "view column"
		names = "schema.view.column"
		relkind = "v"

		class Comment(ColumnObject.Comment):
			type = "view column comment"
			names = "schema.view.column"
			relkind = "v"

		def view(self, connection=None):
			raise NotImplementedError

	def oid(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_relquery("r.oid", relkind="v", nsp=True, rel=True), self.names)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return r.oid

	def columns(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_attquery("n.nspname || '.' || c.relname || '.' || a.attname as name", relkind='v', nsp=True, rel=True), self.names)
		for r in c:
			yield self.Column(r.name, c.connection)

	def records(self, connection=None):
		c = self.getcursor(connection)
		c.execute(f"select * from {self.name};")
		for r in c:
			yield r

	def createsql(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_relquery("pg_catalog.pg_get_viewdef(r.oid) as view_def", relkind="v", nsp=True, rel=True), self.names)
		r = c.fetchone()
		return f"create or replace view {self.name}\nas\n{r.view_def};"


class MaterializedView(View):
	type = "materialized view"
	names = "schema.materializedview"

	class Comment(CommentObject):
		type = "materialized view comment"
		names = "schema.materializedview"


class Sequence(CommentedObject):
	type = "sequence"
	names = "schema.sequence"

	seqtypes = dict(
		int2=(-(1<<15), (1<<15)-1, "smallint"),
		int4=(-(1<<31), (1<<31)-1, "integer"),
		int8=(-(1<<63), (1<<63)-1, "bigint"),
		default=(0.5, 0.5, "bigint"),
	)

	class Comment(CommentObject):
		type = "sequence comment"
		names = "schema.sequence"

		def _query(self, cursor):
			cursor.execute(_relquery("obj_description(r.oid, 'pg_class') as comment", relkind="S", nsp=True, rel=True), self.names)

	def createsql(self, connection=None, exists_ok=False):
		c = self.getcursor(connection)
		c.execute("""
			select
				s.*,
				t.typname
			from
				pg_catalog.pg_namespace n,
				pg_catalog.pg_class c,
				pg_catalog.pg_sequence s,
				pg_catalog.pg_type t
			where
				n.oid = c.relnamespace and
				c.oid = s.seqrelid and
				s.seqtypid = t.oid and
				c.relkind = 'S' and
				n.nspname = %s and
				c.relname = %s
		""", self.names)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		sql = f"create sequence"
		if exists_ok:
			sql += " if not exists"
		sql += f" {self.name}"
		type = self.seqtypes.get(r.typname, "default")
		if r.typname != "int8":
			sql += f" as {type[2]}"
		if r.seqincrement != 1:
			sql += f" increment by {r.seqincrement}"
		minvalue = 1 if r.seqincrement > 0 else type[0]
		if r.seqmin is None:
			sql += f" no minvalue"
		elif r.seqmin != minvalue:
			sql += f" minvalue {r.seqmin}"
		maxvalue = (type[1] if r.seqincrement > 0 else -1)
		if r.seqmax is None:
			sql += f" no maxvalue"
		elif r.seqmax != maxvalue:
			sql += f" maxvalue {r.seqmax}"
		if r.seqmin is not None:
			minvalue = r.seqmin
		if r.seqmax is not None:
			maxvalue = r.seqmax
		if r.seqstart != (minvalue if r.seqincrement > 0 else maxvalue):
			sql += f" start with {r.seqstart}"
		if r.seqcache != 1:
			sql += f" cache {r.seqcache}"
		if r.seqcycle:
			sql += f" cycle"
		sql += ";"
		return sql


class CallableObject(CommentedObject):
	class Comment(CommentObject):
		def _query(self, cursor):
			cursor.execute(_proquery("obj_description(p.oid, 'pg_proc') as comment", prokind=f"= '{self.prokind}'", nsp=True, pro=True), self.names)

	def arguments(self, connection=None):
		raise NotImplementedError

	def __call__(self, cursor, *args, **kwargs):
		raise NotImplementedError

	def createsql(self, connection=None):
		c = self.getcursor(connection)
		sql = _proquery(
			"p.prokind",
			"p.proname",
			"l.lanname",
			"p.provolatile",
			"p.prosrc",
			"pg_catalog.pg_get_function_arguments(p.oid) as args_def",
			"pg_catalog.pg_get_function_result(p.oid) as return_def",
			prokind=f"= '{self.prokind}'",
			nsp=True,
			pro=True,
			lan=True,
		)
		c.execute(sql, self.names)
		r = c.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)

		sql = f"create or replace {self.type} {self.names.schema}.{self.names[-1]}({r.args_def})\n"
		if len(sql) > 80 or r.args_def:
			args = split_comma(r.args_def)
			sql = f"create or replace {self.type} {self.names.schema}.{self.names[-1]}(\n"
			for (last, arg) in misc.islast(args):
				comma = "" if last else ","
				sql += f"\t{arg}{comma}\n"
			sql += ")\n"
		sql += f"{r.return_def}\n"
		sql += f"language {r.lanname}\n"
		if r.provolatile == "i":
			sql += f"immutable\n"
		elif r.provolatile == "s":
			sql += f"stable\n"
		sql += f"as ${self.type}$\n"
		sql += f"{r.prosrc.strip()}\n"
		sql += f"${self.type}$\n"
		sql += ";"
		return sql


class Procedure(CallableObject):
	type = "procedure"
	names = "schema.procedure"
	prokind = "p"

	class Comment(CallableObject.Comment):
		type = "procedure comment"
		names = "schema.procedure"
		prokind = "p"


class Function(CallableObject):
	type = "function"
	names = "schema.function"
	prokind = "f"

	class Comment(CallableObject.Comment):
		type = "function comment"
		names = "schema.function"
		prokind = "f"
