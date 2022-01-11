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
from collections import abc

import psycopg
from psycopg import rows, errors

from ll import misc, url as url_


__docformat__ = "reStructuredText"


bigbang = datetime.datetime(1970, 1, 1, 0, 0, 0) # timestamp for Postgres "directories"


###
### Typing stuff
###

from typing import *


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
	def __init__(self, select=None, from_=None, join=None, leftjoin=None, where=None, orderby=None):
		self.selects = []
		self.froms = []
		self.joins = []
		self.leftjoins = []
		self.wheres = []
		self.orderbys = []
		self.params = []
		if select is not None:
			if isinstance(select, str):
				self.selects.append(select)
			else:
				self.selects.extend(select)
		if from_ is not None:
			if isinstance(from_, str):
				self.froms.append(from_)
			else:
				self.froms.extend(from_)
		if join is not None:
			if isinstance(join, str):
				self.joins.append(join)
			else:
				self.joins.extend(join)
		if leftjoin is not None:
			if isinstance(leftjoin, str):
				self.leftjoins.append(leftjoin)
			else:
				self.leftjoins.extend(leftjoin)
		if where is not None:
			if isinstance(where, str):
				self.wheres.append(where)
			else:
				self.wheres.extend(where)
		if orderby is not None:
			if isinstance(orderby, str):
				self.orderbys.append(orderby)
			else:
				self.orderbys.extend(orderby)

	def __str__(self):
		selects = ", ".join(self.selects)
		froms = ", ".join(self.froms)
		joins = " ".join(f"join {j}" for j in self.joins)
		if joins:
			joins = f" {joins}"
		leftjoins = ", ".join(f"left outer join {j}" for j in self.leftjoins)
		if leftjoins:
			leftjoins = f" {leftjoins}"
		if self.wheres:
			if len(self.wheres) > 1:
				wheres = " and ".join(f"({w})" for w in self.wheres)
			else:
				wheres = self.wheres[0]
			wheres = f" where {wheres}"
		else:
			wheres = ""
		orderbys = ", ".join(self.orderbys)
		if orderbys:
			orderbys = f" order by {orderbys}"
		return f"select {selects} from {froms}{joins}{leftjoins}{wheres}{orderbys}"

	def execute(self, cursor):
		cursor.execute(str(self), tuple(self.params))
		return cursor

	def select(self, *expressions):
		self.selects.extend(expressions)
		return self

	def from_(self, *froms):
		self.froms.extend(froms)
		return self

	def join(self, *joins):
		self.joins.extend(joins)
		return self

	def leftjoin(self, *joins):
		self.leftjoins.extend(joins)
		return self

	def where(self, *wheres):
		self.wheres.extend(wheres)
		return self

	def orderby(self, *orderbys):
		self.orderbys.extend(orderbys)
		return self

	def param(self, *params):
		self.params.extend(params)
		return self


def _where_nsp_internal(sql, internal):
	if internal is not None:
		if internal:
			sql.where("n.nspname like 'pg_%%' or n.nspname = 'information_schema'")
		else:
			sql.where("n.nspname not like 'pg_%%'", "n.nspname != 'information_schema'")


def _where(sql, fieldname, fieldvalue, orderby=None):
	if fieldvalue is not None:
		if isinstance(fieldvalue, str):
			sql.where(f"{fieldname} = %s").param(fieldvalue)
			return
		else:
			sql.where(f"{fieldname} = any(%s)").param(fieldvalue)
	sql.orderby(orderby or fieldname)


def _where_domain(sql, domain):
	if domain is not None:
		if isinstance(domain, str):
			sql.where("t.typname = %s").param(domain)
			return
		else:
			sql.where("t.typname = any(%s)").param(domain)
	sql.orderby("t.typname")


def _where_rel(sql, rel):
	if rel is not None:
		if isinstance(rel, str):
			sql.where("r.relname = %s").param(rel)
			return
		else:
			sql.where("r.relname = any(%s)").param(rel)
	sql.orderby("r.relname")


def _schemaquery(*fields, nsp=None, internal=False):
	sql = _SQL(
		select=fields,
		from_="pg_catalog.pg_namespace n"
	)
	_where_nsp_internal(sql, internal)
	_where(sql, "n.nspname", nsp)
	return sql


def _domainquery(*fields, nsp=None, domain=None, internal=False):
	sql = _SQL(
		select=fields,
		from_="pg_catalog.pg_namespace n",
		join="pg_catalog.pg_type t on n.oid = t.typnamespace",
		where="t.typtype = 'd'",
	)
	_where_nsp_internal(sql, internal)
	_where(sql, "n.nspname", nsp)
	_where(sql, "t.typname", domain)
	return sql


def _relquery(*fields, relkind, nsp=None, rel=None, internal=None):
	sql = _SQL(
		select=fields,
		from_="pg_catalog.pg_namespace n",
		join="pg_catalog.pg_class r on n.oid = r.relnamespace",
		where=(f"r.relkind = '{relkind}'", ),
	)
	_where_nsp_internal(sql, internal)
	_where(sql, "n.nspname", nsp)
	_where(sql, "r.relname", rel)
	return sql


def _proquery(*fields, prokind, nsp=None, pro=None, lan=False, internal=None):
	sql = _SQL(
		select=fields,
		from_="pg_catalog.pg_namespace n",
		join="pg_catalog.pg_proc p on n.oid = p.pronamespace",
	)
	if lan:
		sql.join("pg_catalog.pg_language l on p.prolang = l.oid")
	if prokind is not None:
		sql.where(f"p.prokind {prokind}")
	_where_nsp_internal(sql, internal)
	_where(sql, "n.nspname", nsp)
	_where(sql, "p.proname", pro)
	return sql


def _indquery(*fields, nsp=None, rel=None, ind=None, internal=None):
	sql = _SQL(
		select=fields,
		from_="pg_catalog.pg_namespace n",
		join=(
			"pg_catalog.pg_class c on n.oid = c.relnamespace",
			"pg_catalog.pg_index i on c.oid = i.indexrelid",
		),
		where="not i.indisprimary",
	)
	_where_nsp_internal(sql, internal)
	_where(sql, "n.nspname", nsp)
	if rel is not None:
		sql.join("pg_catalog.pg_class ct on i.indrelid = ct.oid")
		_where(sql, "ct.relname", rel)
	_where(sql, "c.relname", ind)
	return sql


def _attquery(*fields, relkind, nsp=None, rel=None, att=None, internal=None):
	sql = _SQL(
		select=fields,
		from_="pg_catalog.pg_namespace n",
		join=(
			"pg_catalog.pg_class c on n.oid = c.relnamespace",
			"pg_catalog.pg_attribute a on c.oid = a.attrelid",
		),
		where=(
			"a.attnum > 0",
			"not a.attisdropped",
			f"c.relkind = '{relkind}'"
		)
	)
	_where_nsp_internal(sql, internal)
	_where(sql, "n.nspname", nsp)
	_where(sql, "c.relname", rel)
	_where(sql, "a.attname", att, "a.attnum")
	return sql


def _tgquery(*fields, nsp=False, rel=False, tg=False, internal=None):
	sql = _SQL(
		select=fields,
		from_="pg_catalog.pg_namespace n",
		join=(
			"pg_catalog.pg_class c on n.oid = c.relnamespace",
			"pg_catalog.pg_trigger t on c.oid = t.tgrelid",
		),
		where="not t.tgisinternal"
	)
	_where_nsp_internal(sql, internal)
	_where(sql, "n.nspname", nsp)
	_where(sql, "c.relname", rel)
	_where(sql, "t.tgname", tg)
	return sql


def _conquery(*fields, contype=None, nsp=None, rel=None, con=None, internal=None):
	sql = _SQL(
		select=fields,
		from_="pg_catalog.pg_namespace n",
		join="pg_catalog.pg_constraint c on c.connamespace = n.oid"
	)
	if contype is not None:
		sql.where(f"contype = '{contype}'")
	_where_nsp_internal(sql, internal)
	_where(sql, "n.nspname", nsp)
	if rel is not None:
		sql.join("pg_catalog.pg_class r on c.conrelid = r.oid")
		_where(sql, "r.relname", rel)
	_where(sql, "c.conname", con)
	return sql


###
### :mod:ll.postsql` version of connections and cursors
###

class Connection(psycopg.Connection):
	def __repr__(self):
		parts = []
		parts.append(f"dsn={self.dsn!r}")
		parts.append(f"state={self.state}")
		parts.append(f"status={self.info.status.name}")
		parts.append(f"transaction_status={self.info.transaction_status.name}")
		parts.append(f"server_version={self.server_version}")
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} {' '.join(parts)} at {id(self):#x}>"

	def __str__(self):
		return repr(self)

	def _repr_pretty_(self, p, cycle):
		prefix = f"<{self.__class__.__module__}.{self.__class__.__qualname__}"
		suffix = ">"

		if cycle:
			p.text(f"{prefix} ... {suffix}")
		else:
			with p.group(4, prefix, suffix):
				p.breakable()
				p.text(f"dsn={self.dsn!r}")

				p.breakable()
				p.text(f"state={self.state}")

				p.breakable()
				p.text(f"status={self.info.status.name}")

				p.breakable()
				p.text(f"transaction_status={self.info.transaction_status.name}")

				p.breakable()
				p.text(f"server_version={self.server_version!r}")

				p.breakable()
				p.text(f"encoding={self.info.encoding!r}")

				if self.info.error_message:
					p.breakable()
					p.text(f"error_message={self.info.error_message!r}")

				p.breakable()
				p.text(f"at {id(self):#x}")

	@property
	def dsn(self):
		return self.info.dsn

	@property
	def state(self):
		if self.broken:
			return "BROKEN"
		elif self.closed:
			return "CLOSED"
		else:
			return "OPEN"

	@property
	def server_version(self):
		sv = self.info.server_version
		if sv >= 100000:
			sv = str(sv)
			return f"{sv[:2]}.{sv[-2:].lstrip('0')}"
		else:
			sv = str(sv)
			return f"{sv[:2]}.{sv[2:-2].lstrip('0')}.{sv[-2:].lstrip('0')}"

	def schemas(self, cursor=None, schema=None, internal=False):
		query = _schemaquery(
			"nspname",
			nsp=schema,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield Schema(r.nspname, self)

	def domains(self, cursor=None, schema=None, name=None, internal=False):
		query = _domainquery(
			"n.nspname || '.' || t.typname as name",
			nsp=schema,
			domain=name,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield Domain(r.name, self)

	def tables(self, cursor=None, schema=None, name=None, internal=False):
		query = _relquery(
			"n.nspname || '.' || r.relname as name",
			relkind="r",
			nsp=schema,
			rel=name,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield Table(r.name, self)

	def table_columns(self, cursor=None, schema=None, tablename=None, columnname=None, internal=False):
		query = _attquery(
			"n.nspname || '.' || c.relname || '.' || a.attname as name",
			relkind='r',
			nsp=schema,
			rel=tablename,
			att=columnname,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield Table.Column(r.name, self)

	def indexes(self, cursor=None, schema=None, tablename=None, indexname=None, internal=False):
		query = _indquery(
			"n.nspname || '.' || c.relname as name",
			nsp=schema,
			rel=tablename,
			ind=indexname,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield Index(r.name, self)

	def triggers(self, cursor=None, schema=None, tablename=None, triggername=None, internal=False):
		query = _tgquery(
			"n.nspname || '.' || c.relname || '.' || t.tgname as name",
			nsp=schema,
			rel=tablename,
			tg=triggername,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield Trigger(r.name, self)

	def pks(self, cursor=None, schema=None, tablename=None, conname=None, internal=False):
		query = _conquery(
			"n.nspname || '.' || c.conname as name",
			contype="p",
			nsp=schema,
			rel=tablename,
			con=conname,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield PrimaryKey(r.name, self)

	def fks(self, cursor=None, schema=None, tablename=None, conname=None, internal=False):
		query = _conquery(
			"n.nspname || '.' || c.conname as name",
			contype="f",
			nsp=schema,
			rel=tablename,
			con=conname,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield ForeignKey(r.name, self)

	def unique_constraints(self, cursor=None, schema=None, tablename=None, conname=None, internal=False):
		query = _conquery(
			"n.nspname || '.' || c.conname as name",
			contype="u",
			nsp=schema,
			rel=tablename,
			con=conname,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield ForeignKey(r.name, self)

	def check_constraints(self, cursor=None, schema=None, tablename=None, conname=None, internal=False):
		query = _conquery(
			"n.nspname || '.' || c.conname as name",
			contype="c",
			nsp=schema,
			rel=tablename,
			con=conname,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield CheckConstraint(r.name, self)

	def constraints(self, cursor=None, schema=None, tablename=None, conname=None, internal=False):
		query = _conquery(
			"c.contype",
			"n.nspname || '.' || c.conname as name",
			nsp=schema,
			rel=tablename,
			con=conname,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			type = Constraint.types[r.contype]
			yield type(r.name, self)

	def views(self, cursor=None, schema=None, name=None, internal=False):
		query = _relquery(
			"n.nspname || '.' || r.relname as name",
			relkind="v",
			nsp=schema,
			rel=name,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield View(r.name, self)

	def view_columns(self, cursor=None, schema=None, viewname=None, columnname=None, internal=False):
		query = _attquery(
			"n.nspname || '.' || c.relname || '.' || a.attname as name",
			relkind="v",
			nsp=schema,
			rel=viewname,
			att=columnname,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield View.Column(r.name, self)

	def sequences(self, cursor=None, schema=None, name=None, internal=False):
		query = _relquery(
			"n.nspname || '.' || r.relname as name",
			relkind="S",
			nsp=schema,
			rel=name,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield Sequence(r.name, self)

	def callables(self, cursor=None, schema=None, name=None, internal=False):
		query = _proquery(
			"p.prokind", "n.nspname || '.' || p.proname as name",
			prokind="in ('f', 'p')",
			nsp=schema,
			pro=name,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			type = CallableObject.types[r.prokind]
			yield type(r.name, self)

	def procedures(self, cursor=None, schema=None, name=None, internal=False):
		query = _proquery(
			"n.nspname || '.' || p.proname as name",
			prokind="= 'p'",
			nsp=schema,
			pro=name,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield Procedure(r.name, self)

	def functions(self, cursor=None, schema=None, name=None, internal=False):
		query = _proquery(
			"n.nspname || '.' || p.proname as name",
			prokind="= 'f'",
			nsp=schema,
			pro=name,
			internal=internal,
		)
		for r in query.execute(cursor or self.cursor()):
			yield Function(r.name, self)

	def objects(self):
		raise NotImplementedError

	def object_named(self, name):
		raise NotImplementedError


class Record(tuple, abc.Mapping):
	"""
	A :class:`Record` is a subclass of :class:`tuple` that is used for storing
	results of database fetches and procedure and function calls. Both item and
	attribute access (i.e. :meth:`__getitem__` and :meth:`__getattr__`) are
	available. Field names are case insensitive.
	"""

	def __new__(cls, index2name, name2index, values):
		record = tuple.__new__(cls, values)
		record._index2name = index2name
		record._name2index = name2index
		return record

	def __getitem__(self, arg):
		if isinstance(arg, str):
			arg = self._name2index[arg.lower()]
		return tuple.__getitem__(self, arg)

	def __getattr__(self, name):
		try:
			index = self._name2index[name.lower()]
		except KeyError:
			raise AttributeError(f"{self.__class__.__module__}.{self.__class__.__qualname__} object has no attribute {name!r}")
		return tuple.__getitem__(self, index)

	def ul4_getattr(self, name):
		return getattr(self, name)

	def ul4_hasattr(self, name):
		return name.lower() in self._name2index

	def get(self, name, default=None):
		"""
		Return the value for the field named ``name``. If this field doesn't
		exist in ``self``, return ``default`` instead.
		"""
		try:
			index = self._name2index[name.lower()]
		except KeyError:
			return default
		return tuple.__getitem__(self, index)

	def __contains__(self, name):
		return name.lower() in self._name2index

	def keys(self):
		"""
		Return an iterator over field names.
		"""
		return iter(self._index2name)

	def items(self):
		"""
		Return an iterator over (field name, field value) tuples.
		"""
		for (index, key) in enumerate(self._index2name):
			yield (key, tuple.__getitem__(self, index))

	def replace(self, **kwargs):
		"""
		Return a new :class:`Record` with the same fields as ``self``, except
		for those fields given new values by whichever keyword arguments are
		specified.
		"""
		values = list(self)
		for (key, value) in kwargs.items():
			values[self._name2index[key.lower()]] = value
		return self.__class__(self._index2name, self._name2index, values)

	def __repr__(self):
		items = ", ".join(f"{key}={value!r}" for (key, value) in self.items())
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} {items} at {id(self):#x}>"

	def _repr_pretty_(self, p, cycle):
		prefix = f"<{self.__class__.__module__}.{self.__class__.__qualname__}"
		suffix = f"at {id(self):#x}"

		if cycle:
			p.text(f"{prefix} ... {suffix}>")
		else:
			with p.group(4, prefix, ">"):
				for (key, value) in self.items():
					p.breakable()
					p.text(f"{key}=")
					p.pretty(value)
				p.breakable()
				p.text(suffix)


class RecordFactory:
	def __init__(self, cursor: psycopg.Cursor[Dict[str, Any]]):
		if cursor.description is None:
			self.index2name = None
			self.name2index = None
		else:
			self.index2name = []
			self.name2index = {}
			for (i, col) in enumerate(cursor.description):
				colname = col.name.lower()
				self.index2name.append(colname)
				self.name2index[colname] = i

	def __call__(self, values: Sequence[Any]) -> Record:
		return Record(self.index2name, self.name2index, values)


def connect(conninfo, **kwargs):
	return Connection.connect(conninfo, row_factory=RecordFactory, **kwargs)


###
### Classes for all types of objects in a Postgres database
###

class Object:
	def __init__(self, name, connection=None):
		self.name = name
		self.names = self.__class__.names._make(name.split("."))
		self.connection = connection

	def oid(self, connection=None):
		r = self._oid(connection)
		if r is None:
			raise SQLObjectNotFoundError(self)
		return r.oid

	def exists(self, connection=None):
		return self._oid(connection) is not None

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
	names = collections.namedtuple("SchemaNames", ["schema"])

	class Comment(CommentObject):
		type = "schema"
		names = collections.namedtuple("SchemaCommentNames", ["schema"])

		def _query(self, cursor):
			query = _schemaquery("obj_description(oid, 'pg_namespace') as comment", nsp=self.names[0])
			query.execute(cursor)

	def _oid(self, connection=None):
		cursor = self.getcursor(connection)
		_schemaquery("oid", nsp=self.names[0]).execute(cursor)
		r = cursor.fetchone()
		return r

	def domains(self, connection=None):
		return self.getconnection(connection).domains(schema=self.names.schema)

	def tables(self, connection=None):
		return self.getconnection(connection).tables(schema=self.names.schema)

	def table_columns(self, connection=None):
		return self.getconnection(connection).table_columns(schema=self.names.schema)

	def indexes(self, connection=None):
		return self.getconnection(connection).indexes(schema=self.names.schema)

	def triggers(self, connection=None):
		return self.getconnection(connection).triggers(schema=self.names.schema)

	def pks(self, connection=None):
		return self.getconnection(connection).pks(schema=self.names.schema)

	def fks(self, connection=None):
		return self.getconnection(connection).fks(schema=self.names.schema)

	def unique_constraints(self, connection=None):
		return self.getconnection(connection).unique_constraints(schema=self.names.schema)

	def check_constraints(self, connection=None):
		return self.getconnection(connection).check_constraints(schema=self.names.schema)

	def constraints(self, connection=None):
		return self.getconnection(connection).constraints(schema=self.names.schema)

	def views(self, connection=None):
		return self.getconnection(connection).views(schema=self.names.schema)

	def view_columns(self, connection=None):
		return self.getconnection(connection).view_columns(schema=self.names.schema)

	def sequences(self, connection=None):
		return self.getconnection(connection).sequences(schema=self.names.schema)

	def callables(self, connection=None):
		return self.getconnection(connection).callables(schema=self.names.schema)

	def procedures(self, connection=None):
		return self.getconnection(connection).procedures(schema=self.names.schema)

	def functions(self, connection=None):
		return self.getconnection(connection).functions(schema=self.names.schema)

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
	names = collections.namedtuple("DomainNames", ["schema", "domain"])

	class Comment(CommentObject):
		type = "domain"
		names = collections.namedtuple("DomainCommentNames", ["schema", "domain"])

		def _query(self, cursor):
			query = _domainquery(
				"obj_description(t.oid, 'pg_type') as comment",
				nsp=self.names.schema,
				domain=self.names.domain
			)
			query.execute(cursor)

	def _oid(self, connection=None):
		cursor = self.getcursor(connection)
		query = _domainquery("t.oid", nsp=self.names.schema, domain=self.names.domain)
		query.execute(cursor)
		r = cursor.fetchone()
		return r

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

	def _info(self, connection):
		c = self.getcursor(connection)
		c.execute(f"""
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
				c.relkind = '{self.relkind}' and
				n.nspname = %s and 
				c.relname = %s and
				a.attname = %s
			order by
				attnum
		""", self.names)
		return c.fetchone()

	def datatype(self, connection=None):
		r = self._info(connection)
		if r is None:
			raise SQLObjectNotFoundError(self)
		return r.column_type

	def default(self, connection=None):
		r = self._info(connection)
		if r is None:
			raise SQLObjectNotFoundError(self)
		return r.default_value

	def nullable(self, connection=None):
		r = self._info(connection)
		if r is None:
			raise SQLObjectNotFoundError(self)
		return not r.attnotnull


class Table(CommentedObject):
	type = "table"
	names = collections.namedtuple("TableNames", ["schema", "table"])

	class Comment(CommentObject):
		type = "table comment"
		names = collections.namedtuple("TableCommentNames", ["schema", "table"])

		def _query(self, cursor):
			query = _relquery(
				"obj_description(r.oid, 'pg_class') as comment",
				relkind="r",
				nsp=self.names.schema,
				rel=self.names.table,
			)
			query.execute(cursor)

	class Column(ColumnObject):
		type = "table column"
		names = collections.namedtuple("TableColumnNames", ["schema", "table", "column"])
		relkind = "r"

		class Comment(ColumnObject.Comment):
			type = "table column comment"
			names = collections.namedtuple("TableColumnCommentNames", ["schema", "table", "column"])
			relkind = "r"

		def table(self, connection=None):
			return Table(self.name.rpartition(".")[0], self.getconnection(connection))

		def addsql(self, connection=None, exists_ok=False):
			r = self._info(connection)
			sql = f"alter table {self.names.schema}.{self.names.table} add column"
			if exists_ok:
				sql += " if not exists"
			sql += f" {self.names.column} {r.column_type}"
			if r.attnotnull:
				sql += " not null"
			sql += ";"
			return sql

		def dropsql(self, connection=None, missing_ok=False, cascade=False):
			sql = f"alter table {self.names.schema}.{self.names.table} drop column"
			if missing_ok:
				sql += " if exists"
			sql += f" {self.names.column}"
			if cascade:
				sql += " cascade"
			sql += ";"
			return sql

	def _oid(self, connection=None):
		cursor = self.getcursor(connection)
		query = _relquery(
			"r.oid",
			relkind="r",
			nsp=self.names.schema,
			rel=self.names.table,
		)
		query.execute(cursor)
		r = cursor.fetchone()
		return r

	def columns(self, connection=None):
		connection = self.getconnection(connection)
		return connection.table_columns(schema=self.names.schema, tablename=self.names.table)

	def indexes(self, connection=None):
		connection = self.getconnection(connection)
		return connection.indexes(schema=self.names.schema, tablename=self.names.table)

	def triggers(self, connection=None):
		connection = self.getconnection(connection)
		return connection.triggers(schema=self.names.schema, tablename=self.names.table)

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
		connection = self.getconnection(connection)
		return connection.fks(schema=self.names.schema, tablename=self.names.table)

	def unique_constraints(self, connection=None):
		connection = self.getconnection(connection)
		return connection.unique_constraints(schema=self.names.schema, tablename=self.names.table)

	def check_constraints(self, connection=None):
		connection = self.getconnection(connection)
		return connection.check_constraints(schema=self.names.schema, tablename=self.names.table)

	def constraints(self, connection=None):
		connection = self.getconnection(connection)
		return connection.constraints(schema=self.names.schema, tablename=self.names.table)

	def records(self, connection=None):
		cursor = self.getcursor(connection)
		cursor.execute(f"select * from {self.name};")
		yield from cursor

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
	names = collections.namedtuple("IndexNames", ["schema", "index"])

	class Comment(CommentObject):
		type = "index comment"
		names = collections.namedtuple("IndexCommentNames", ["schema", "index"])

		def _query(self, cursor):
			cursor.execute(_indquery("obj_description(c.oid, 'pg_class') as comment", nsp=True, ind=True), self.names)

	def _oid(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_indquery("c.oid", nsp=True, ind=True), self.names)
		r = c.fetchone()
		return r

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
	names = collections.namedtuple("TriggerNames", ["schema", "table", "trigger"])

	class Comment(CommentObject):
		type = "trigger comment"
		names = collections.namedtuple("TriggerCommentNames", ["schema", "table", "trigger"])

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

	def _oid(self, connection=None):
		cursor = self.getcursor(connection)
		query = _conquery("c.oid", contype=self.contype, nsp=self.names[0], con=self.names[1])
		r = cursor.execute(cursor).fetchone()
		return r

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
	names = collections.namedtuple("PrimaryKeyNames", ["schema", "pk"])
	contype = "p"

	class Comment(Constraint.Comment):
		type = "primary key comment"
		names = collections.namedtuple("PrimaryKeyCommentNames", ["schema", "pk"])
		contype = "p"

	def columns(self, connection=None):
		raise NotImplementedError


class ForeignKey(Constraint):
	type = "foreign key"
	names = collections.namedtuple("ForeignKeyNames", ["schema", "fk"])
	contype = "f"

	class Comment(Constraint.Comment):
		type = "foreign key comment"
		names = collections.namedtuple("ForeignKeyCommentNames", ["schema", "fk"])
		contype = "f"

	def columns(self, connection=None):
		raise NotImplementedError

	def refconstraint(self, connection=None):
		raise NotImplementedError


class UniqueConstraint(Constraint):
	type = "unique constraint"
	names = collections.namedtuple("UniqueConstraintNames", ["schema", "constraint"])
	contype = "u"

	class Comment(Constraint.Comment):
		type = "unique constraint comment"
		names = collections.namedtuple("UniqueConstraintCommentNames", ["schema", "constraint"])
		contype = "u"

	def columns(self, connection=None):
		raise NotImplementedError


class CheckConstraint(Constraint):
	type = "check constraint"
	names = collections.namedtuple("CheckConstraintNames", ["schema", "constraint"])
	contype = "c"

	class Comment(Constraint.Comment):
		type = "check constraint comment"
		names = collections.namedtuple("CheckConstraintCommentNames", ["schema", "constraint"])
		contype = "c"


Constraint.types = dict(
	p=PrimaryKey,
	f=ForeignKey,
	u=UniqueConstraint,
	c=CheckConstraint,
)


class View(CommentedObject):
	type = "view"
	names = collections.namedtuple("ViewNames", ["schema", "view"])

	class Comment(CommentObject):
		type = "view comment"
		names = collections.namedtuple("ViewCommentNames", ["schema", "view"])

		def _query(self, cursor):
			cursor.execute(_relquery("obj_description(r.oid, 'pg_class') as comment", relkind="v", nsp=True, rel=True), self.names)

	class Column(ColumnObject):
		type = "view column"
		names = collections.namedtuple("ViewColumnNames", ["schema", "view", "column"])
		relkind = "v"

		class Comment(ColumnObject.Comment):
			type = "view column comment"
			names = collections.namedtuple("ViewColumnCommentNames", ["schema", "view", "column"])
			relkind = "v"

		def view(self, connection=None):
			return View(self.name.rpartition(".")[0], self.getconnection(connection))

	def _oid(self, connection=None):
		c = self.getcursor(connection)
		c.execute(_relquery("r.oid", relkind="v", nsp=True, rel=True), self.names)
		r = c.fetchone()
		return r

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
	names = collections.namedtuple("MaterializedViewNames", ["schema", "materializedview"])

	class Comment(CommentObject):
		type = "materialized view comment"
		names = collections.namedtuple("MaterializedViewCommentNames", ["schema", "materializedview"])


class Sequence(CommentedObject):
	type = "sequence"
	names = collections.namedtuple("SequenceNames", ["schema", "sequence"])

	seqtypes = dict(
		int2=(-(1<<15), (1<<15)-1, "smallint"),
		int4=(-(1<<31), (1<<31)-1, "integer"),
		int8=(-(1<<63), (1<<63)-1, "bigint"),
		default=(0.5, 0.5, "bigint"),
	)

	class Comment(CommentObject):
		type = "sequence comment"
		names = collections.namedtuple("SequenceCommentNames", ["schema", "sequence"])

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
	names = collections.namedtuple("ProcedureNames", ["schema", "procedure"])
	prokind = "p"

	class Comment(CallableObject.Comment):
		type = "procedure comment"
		names = collections.namedtuple("ProcedureCommentNames", ["schema", "procedure"])
		prokind = "p"


class Function(CallableObject):
	type = "function"
	names = collections.namedtuple("FunctionNames", ["schema", "function"])
	prokind = "f"

	class Comment(CallableObject.Comment):
		type = "function comment"
		names = collections.namedtuple("FunctionCommentNames", ["schema", "function"])
		prokind = "f"


CallableObject.types = dict(
	f=Function,
	p=Procedure,
)
