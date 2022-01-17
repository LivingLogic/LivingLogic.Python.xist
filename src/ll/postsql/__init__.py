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


class SQLTypeUnknownError(TypeError):
	def __init__(self, type):
		super().__init__(f"Database type {type!r} unknown")


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

	def left_outer_join(self, *joins):
		self.leftjoins.extend(joins)
		return self

	def where(self, *wheres):
		self.wheres.extend(wheres)
		return self

	def order_by(self, *orderbys):
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
	sql.order_by(orderby or fieldname)


def _where_domain(sql, domain):
	if domain is not None:
		if isinstance(domain, str):
			sql.where("t.typname = %s").param(domain)
			return
		else:
			sql.where("t.typname = any(%s)").param(domain)
	sql.order_by("t.typname")


def _where_rel(sql, rel):
	if rel is not None:
		if isinstance(rel, str):
			sql.where("r.relname = %s").param(rel)
			return
		else:
			sql.where("r.relname = any(%s)").param(rel)
	sql.order_by("r.relname")


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
		join=(
			"pg_catalog.pg_constraint c on c.connamespace = n.oid",
			"pg_catalog.pg_class r on c.conrelid = r.oid",
		)
	)
	if contype is not None:
		sql.where(f"contype = '{contype}'")
	_where_nsp_internal(sql, internal)
	_where(sql, "n.nspname", nsp)
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
			relkind="r",
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
		done = set()
		for schema in self.schemas():
			yield schema
			yield from schema.referencedbyall()

	def object_from_identity(self, type, name, args, typtype, contype):
		if type == "schema":
			return Schema(".".join(name), self)
		elif type == "table":
			return Table(".".join(name), self)
		elif type == "table constraint" and contype in "pfuc":
			type = Constraint.types[contype]
			return type(".".join(name), self)
		elif type == "table column":
			return Table.Column(".".join(name), self)
		elif type == "view":
			return View(".".join(name), self)
		elif type == "view column":
			return View.Column(".".join(name), self)
		elif type == "trigger":
			return Trigger(".".join(name), self)
		elif type == "index":
			return Index(".".join(name), self)
		elif type == "sequence":
			return Sequence(".".join(name), self)
		elif type == "type" and typtype == "d":
			return Domain(".".join(name), self)
		else:
			print(type, name, args)
			raise SQLTypeUnknownError(type)

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

ID = collections.namedtuple("ID", ["type", "object", "index"], defaults=[None], module="ll.postsql")


class Object:
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

	def references(self, connection=None):
		"""
		Objects directly used by ``self``.

		If ``connection`` is not :const:`None` it will be used as the database
		connection from which to fetch data. If ``connection`` is :const:`None`
		the connection from which ``self`` has been extracted will be used. If
		there is not such connection, you'll get an exception.
		"""
		connection = self.getconnection(connection)
		id = self.identify(connection)
		if len(id) == 2:
			id = id + (0,)
		cursor = connection.cursor()
		cursor.execute("""
			select distinct
				(pg_identify_object_as_address(d.refclassid, d.refobjid, d.refobjsubid)).*,
				t.typtype,
				c.contype
			from
				pg_catalog.pg_depend d
			left outer join
				pg_catalog.pg_type t on d.refclassid = 'pg_type'::regclass and t.oid = d.refobjid and d.refobjsubid = 0
			left outer join
				pg_catalog.pg_constraint c on d.refclassid = 'pg_constraint'::regclass and c.oid = d.refobjid and d.refobjsubid = 0
			left outer join
				pg_catalog.pg_class r on d.refclassid = 'pg_class'::regclass and r.oid = d.refobjid and d.refobjsubid = 0
			where
				d.classid=%s and
				d.objid=%s and
				d.objsubid=%s and
				d.refclassid != 'pg_rewrite'::regclass and
				d.deptype = ANY('{n,a}') and
				(t.typtype is null or t.typtype = 'd') and
				(r.relkind is null or r.relkind != 't')
		""", id)
		for r in cursor:
			try:
				yield connection.object_from_identity(*r)
			except SQLTypeUnknownError as exc:
				pass # Ignore unknown types

	def referencesall(self, connection=None, done=None):
		"""
		All objects used by ``self`` (recursively).

		For the meaning of ``connection`` see :meth:`references`.

		``done`` is used internally and shouldn't be passed.
		"""
		if done is None:
			done = set()
		for obj in self.references(connection):
			if obj not in done:
				done.add(obj)
				yield obj
				yield from obj.referencesall(connection, done)

	def referencedby(self, connection=None):
		"""
		Objects using ``self``.

		For the meaning of ``connection`` see :meth:`references`.
		"""
		connection = self.getconnection(connection)
		id = self.identify(connection)
		if len(id) == 2:
			id = id + (0,)
		cursor = connection.cursor()
		cursor.execute("""
			select distinct
				(pg_identify_object_as_address(d.classid, d.objid, d.objsubid)).*,
				t.typtype,
				c.contype
			from
				pg_catalog.pg_depend d
			left outer join
				pg_catalog.pg_type t on d.classid = 'pg_type'::regclass and t.oid = d.objid and d.objsubid = 0
			left outer join
				pg_catalog.pg_constraint c on d.classid = 'pg_constraint'::regclass and c.oid = d.objid and d.objsubid = 0
			left outer join
				pg_catalog.pg_class r on d.classid = 'pg_class'::regclass and r.oid = d.objid and d.objsubid = 0
			where
				d.refclassid=%s and
				d.refobjid=%s and
				d.refobjsubid=%s and
				d.classid != 'pg_rewrite'::regclass and
				d.deptype = ANY('{n,a}') and
				(t.typtype is null or t.typtype = 'd') and
				(r.relkind is null or r.relkind != 't')
		""", id)
		for r in cursor:
			try:
				yield connection.object_from_identity(*r)
			except SQLTypeUnknownError as exc:
				pass # Ignore unknown types

	def referencedbyall(self, connection=None, done=None):
		if done is None:
			done = set()
		for obj in self.referencedby(connection):
			if obj not in done:
				done.add(obj)
				yield obj
				yield from obj.referencedbyall(connection, done)


class CommentObject(Object):
	def identify(self, connection=None):
		cursor = self.getcursor(connection)
		self.object()._identify(cursor)
		r = cursor.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return self.id(*r)

	def createsql(self, connection=None):
		cursor = self.getcursor(connection)
		self._query(cursor)
		r = cursor.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return self._sql(r, r.comment)

	def dropsql(self, connection=None):
		cursor = self.getcursor(connection)
		self._query(cursor)
		r = cursor.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return self._sql(r, None)

	def exists(self, connection=None):
		cursor = self.getcursor(connection)
		self._query(cursor)
		r = cursor.fetchone()
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

	def object(self, connection=None):
		return self.Object(self.name, self.getconnection(connection))

	def references(self, connection=None):
		yield self.object(connection)


class CommentedObject(Object):
	def comment(self, connection=None):
		return self.Comment(self.name, connection or self.connection)

	def identify(self, connection=None):
		cursor = self.getcursor(connection)
		self._identify(cursor)
		r = cursor.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return self.id(*r)

	def exists(self, connection=None):
		cursor = self.getcursor(connection)
		self._identify(cursor)
		r = cursor.fetchone()
		return r is not None

	def dropsql(self, connection=None, missing_ok=False):
		sql = f"drop {self.type}"
		if missing_ok:
			sql += " if exists"
		sql += f" {self.name};"
		return sql

	def referencedby(self, connection=None):
		connection = self.getconnection(connection)
		yield self.Comment(self.name, connection)
		yield from super().referencedby(connection)


class Schema(CommentedObject):
	type = "schema"
	names = collections.namedtuple("SchemaNames", ["schema"])
	id = collections.namedtuple("SchemaID", ["type", "object"])

	class Comment(CommentObject):
		type = "schema"
		names = collections.namedtuple("SchemaCommentNames", ["schema"])
		id = collections.namedtuple("SchemaCommentID", ["type", "object"])

		def _query(self, cursor):
			query = _schemaquery("obj_description(oid, 'pg_namespace') as comment", nsp=self.names[0])
			query.execute(cursor)

	def _identify(self, cursor):
		_schemaquery("'pg_namespace'::regclass::int", "oid", nsp=self.names[0]).execute(cursor)

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

	def ________________________referencedby(self, connection=None):
		yield from super().referencedby(connection)
		yield from self.domains(connection)
		yield from self.tables(connection)
		yield from self.views(connection)
		yield from self.sequences(connection)
		yield from self.procedures(connection)
		yield from self.functions(connection)


Schema.Comment.Object = Schema


class CommentedSchemaObject(CommentedObject):
	def schema(self, connection=None):
		return Schema(self.names.schema, connection or self.connection)

	def ______references(self, connection=None):
		yield self.schema(connection)


class Domain(CommentedSchemaObject):
	type = "domain"
	names = collections.namedtuple("DomainNames", ["schema", "domain"])
	id = collections.namedtuple("DomainID", ["type", "object"])

	class Comment(CommentObject):
		type = "domain"
		names = collections.namedtuple("DomainCommentNames", ["schema", "domain"])
		id = collections.namedtuple("DomainCommentID", ["type", "object"])

		def _query(self, cursor):
			query = _domainquery(
				"obj_description(t.oid, 'pg_type') as comment",
				nsp=self.names.schema,
				domain=self.names.domain
			)
			query.execute(cursor)

	def _identify(self, cursor):
		query = _domainquery(
			"'pg_type'::regclass::int",
			"t.oid",
			nsp=self.names.schema,
			domain=self.names.domain,
		)
		query.execute(cursor)

	def createsql(self, connection=None):
		cursor = self.getcursor(connection)
		query = _domainquery(
			"typnotnull",
			"pg_catalog.format_type(typbasetype, typtypmod) as domain_def",
			nsp=self.names.schema,
			domain=self.names.domain,
		)
		query.execute(cursor)

		r = cursor.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		notnull = " not null" if r.typnotnull else ""
		return f"create domain {self.name} {r.domain_def}{notnull};"

Domain.Comment.Object = Domain


class ColumnObject(CommentedSchemaObject):
	class Comment(CommentObject):
		def _query(self, cursor):
			query = _attquery(
				"col_description(c.oid, a.attnum) as comment",
				relkind=self.relkind,
				nsp=self.names.schema,
				rel=self.names[1], # Might be "table" or "view"
				att=self.names.column,
			)
			query.execute(cursor)

	def _identify(self, cursor):
		query = _attquery(
			"'pg_class'::regclass::int",
			"c.oid",
			"a.attnum",
			relkind=self.relkind,
			nsp=self.names.schema,
			rel=self.names[1], # Might be "table" or "view"
			att=self.names.column,
		)
		query.execute(cursor)

	def _info(self, connection):
		cursor = self.getcursor(connection)
		cursor.execute(f"""
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
		return cursor.fetchone()

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


class Table(CommentedSchemaObject):
	type = "table"
	names = collections.namedtuple("TableNames", ["schema", "table"])
	id = collections.namedtuple("TableID", ["type", "object"])

	class Comment(CommentObject):
		type = "table comment"
		names = collections.namedtuple("TableCommentNames", ["schema", "table"])
		id = collections.namedtuple("TableCommentID", ["type", "object"])

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
		id = collections.namedtuple("TableColumnID", ["type", "object", "index"])
		relkind = "r"

		class Comment(ColumnObject.Comment):
			type = "table column comment"
			names = collections.namedtuple("TableColumnCommentNames", ["schema", "table", "column"])
			id = collections.namedtuple("TableColumnCommentID", ["type", "object", "index"])
			relkind = "r"

		def table(self, connection=None):
			return Table(self.name.rpartition(".")[0], self.getconnection(connection))

		def ____________references(self, connection=None):
			yield self.table(connection)

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

	def _identify(self, cursor):
		query = _relquery(
			"'pg_class'::regclass::int",
			"r.oid",
			relkind="r",
			nsp=self.names.schema,
			rel=self.names.table,
		)
		query.execute(cursor)

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
		cursor = self.getcursor(connection)
		oid = self.identify(cursor.connection)[1]
		cursor.execute("""
			select
				c.conname
			from
				pg_catalog.pg_constraint c
			where
				conrelid = %s and
				contype = 'p'
		""", [oid])
		r = cursor.fetchone()
		if r is None:
			return None
		else:
			return PrimaryKey(f"{self.names.schema}.{r.conname}", cursor.connection)

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
		cursor = self.getcursor(connection)

		oid = self.identify(cursor.connection)[1]
		query = (_SQL()
			.select("a.attname")
			.select("a.attnum")
			.select("a.attnotnull")
			.select("pg_catalog.format_type(a.atttypid, a.atttypmod) as column_type")
			.select("""
				case
					when d.adrelid is not null then pg_catalog.pg_get_expr(d.adbin, d.adrelid)
					else null
				end as default_value
			""")
			.from_("pg_catalog.pg_class c")
			.join("pg_catalog.pg_attribute a on c.oid = a.attrelid and a.attnum > 0 and not a.attisdropped")
			.left_outer_join("pg_catalog.pg_attrdef d on d.adrelid = a.attrelid and d.adnum = a.attnum and a.atthasdef")
			.order_by("attnum")
			.where("c.oid = %s").param(oid)
		)

		query.execute(cursor)

		sql = f"create table {self.name}\n"
		sql += f"(\n"
		for (last, column) in misc.islast(cursor):
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

	def _____referencedby(self, connection=None):
		yield from super().referencedby(connection)
		yield from self.indexes(connection)
		yield from self.triggers(connection)
		pk = self.pk(connection)
		if pk is not None:
			yield pk
		yield from self.fks(connection)
		yield from self.unique_constraints(connection)
		yield from self.check_constraints(connection)

Table.Comment.Object = Table
Table.Column.Comment.Object = Table.Column


class Index(CommentedSchemaObject):
	type = "index"
	names = collections.namedtuple("IndexNames", ["schema", "index"])
	id = collections.namedtuple("IndexID", ["type", "object"])

	class Comment(CommentObject):
		type = "index comment"
		names = collections.namedtuple("IndexCommentNames", ["schema", "index"])
		id = collections.namedtuple("IndexCommentID", ["type", "object"])

		def _query(self, cursor):
			query = _indquery(
				"obj_description(c.oid, 'pg_class') as comment",
				nsp=self.names.schema,
				ind=self.names.index,
			)
			query.execute(cursor)

	def _identify(self, cursor):
		query = _indquery(
			"'pg_class'::regclass::int",
			"c.oid",
			nsp=self.names.schema,
			ind=self.names.index,
		)
		query.execute(cursor)

	def createsql(self, connection=None, exists_ok=False):
		cursor = self.getcursor(connection)
		query = (_SQL()
			.select("pg_catalog.pg_get_indexdef(i.indexrelid) as index_def")
			.from_("pg_catalog.pg_namespace n")
			.join("pg_catalog.pg_class c on n.oid = c.relnamespace")
			.join("pg_catalog.pg_index i on c.oid = i.indexrelid")
			.where("n.nspname = %s").param(self.names.schema)
			.where("c.relname = %s").param(self.names.index)
			.where("not i.indisprimary")
		)
		sql = query.execute(cursor).fetchone().index_def
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

Index.Comment.Object = Index


class Trigger(CommentedSchemaObject):
	type = "trigger"
	names = collections.namedtuple("TriggerNames", ["schema", "table", "trigger"])
	id = collections.namedtuple("TriggerID", ["type", "object"])

	class Comment(CommentObject):
		type = "trigger comment"
		names = collections.namedtuple("TriggerCommentNames", ["schema", "table", "trigger"])
		id = collections.namedtuple("TriggerCommentID", ["type", "object"])

		def _sql(self, record, comment):
			return self._makesql(f"trigger {self.names.trigger} on {self.names.schema}.{self.names.table}", comment)

		def _query(self, cursor):
			query = _tgquery(
				"obj_description(t.oid) as comment",
				nsp=self.names.schema,
				rel=self.names.table,
				tg=self.names.trigger,
			)
			query.execute(cursor)

	def _identify(self, cursor):
		query = _tgquery(
			"'pg_trigger'::regclass::int",
			"t.oid",
			nsp=self.names.schema,
			rel=self.names.table,
			tg=self.names.trigger,
		)
		query.execute(cursor)

	def createsql(self, connection=None):
		cursor = self.getcursor(connection)
		cursor.execute("""
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

		r = cursor.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return f"{r.trigger_def};"

	def dropsql(self, connection=None, missing_ok=False, cascade=False):
		sql = "drop trigger"
		if missing_ok:
			sql += " if exists"
		sql += f" {self.names.trigger} on {self.names.schema}.{self.names.table}"
		if cascade:
			sql += " cascade"
		sql += ";"
		return sql

	def table(self, connection=None):
		return Table(self.name.rpartition(".")[0], self.getconnection(connection))

	def ____________references(self, connection=None):
		yield self.table(connection)

Trigger.Comment.Object = Trigger


class Constraint(CommentedSchemaObject):
	class Comment(CommentObject):
		def _query(self, cursor):
			cursor.execute(f"""
			select
				obj_description(c.oid) as comment
			from
				pg_catalog.pg_namespace n,
				pg_catalog.pg_constraint c,
				pg_catalog.pg_class r
			where
				n.oid = c.connamespace and
				c.conrelid = r.oid and
				n.nspname = %s and
				r.relname = %s and
				c.conname = %s and
				c.contype = '{self.contype}'
			""", self.names)

		def _sql(self, record, comment):
			return self._makesql(f"constraint {self.names[2]} on {self.names.schema}.{self.names.table}", comment)

	def _identify(self, cursor):
		query = _conquery(
			"'pg_constraint'::regclass::int",
			"c.oid",
			contype=self.contype,
			nsp=self.names.schema,
			rel=self.names.table,
			con=self.names[2],
		)
		query.execute(cursor)

	def createsql(self, connection=None):
		cursor = self.getcursor(connection)
		cursor.execute(f"""
			select
				pg_catalog.pg_get_constraintdef(c.oid, true) as constraint_def
			from
				pg_catalog.pg_namespace n,
				pg_catalog.pg_constraint c,
				pg_catalog.pg_class r
			where
				n.oid = c.connamespace and
				c.conrelid = r.oid and
				n.nspname = %s and
				r.relname = %s and
				c.conname = %s and
				c.contype = '{self.contype}'
		""", self.names)
		r = cursor.fetchone()
		if r is None:
			raise SQLObjectNotFoundError(self)
		return f"alter table {self.names.schema}.{self.names.table} add constraint {self.names[2]} {r.constraint_def};"

	def dropsql(self, connection=None, missing_ok=False):
		sql = f"alter table {self.names.schema}.{self.names.table} drop constraint"
		if missing_ok:
			sql += " if exists"
		sql += f" {self.names[2]};"
		return sql

	def enablesql(self, connection=None):
		cursor = self.getcursor(connection)
		raise NotImplementedError

	def disablesql(self, connection=None):
		cursor = self.getcursor(connection)
		raise NotImplementedError

	def isenabled(self, connection=None):
		cursor = self.getcursor(connection)
		raise NotImplementedError

	def table(self, connection=None):
		return Table(f"{self.names.schema}.{self.names.table}", connection)

	def _________________references(self, connection=None):
		yield self.table(connection)


class PrimaryKey(Constraint):
	type = "primary key"
	names = collections.namedtuple("PrimaryKeyNames", ["schema", "table", "pk"])
	id = collections.namedtuple("PrimaryKeyID", ["type", "object"])
	contype = "p"

	class Comment(Constraint.Comment):
		type = "primary key comment"
		names = collections.namedtuple("PrimaryKeyCommentNames", ["schema", "table", "pk"])
		id = collections.namedtuple("PrimaryKeyCommentID", ["type", "object"])
		contype = "p"

	def columns(self, connection=None):
		raise NotImplementedError

PrimaryKey.Comment.Object = PrimaryKey


class ForeignKey(Constraint):
	type = "foreign key"
	names = collections.namedtuple("ForeignKeyNames", ["schema", "table", "fk"])
	id = collections.namedtuple("ForeignKeyID", ["type", "object"])
	contype = "f"

	class Comment(Constraint.Comment):
		type = "foreign key comment"
		names = collections.namedtuple("ForeignKeyCommentNames", ["schema", "table", "fk"])
		id = collections.namedtuple("ForeignKeyCommentID", ["type", "object"])
		contype = "f"

	def columns(self, connection=None):
		raise NotImplementedError

	def refconstraint(self, connection=None):
		raise NotImplementedError

ForeignKey.Comment.Object = ForeignKey


class UniqueConstraint(Constraint):
	type = "unique constraint"
	names = collections.namedtuple("UniqueConstraintNames", ["schema", "table", "constraint"])
	id = collections.namedtuple("UniqueConstraintID", ["type", "object"])
	contype = "u"

	class Comment(Constraint.Comment):
		type = "unique constraint comment"
		names = collections.namedtuple("UniqueConstraintCommentNames", ["schema", "table", "constraint"])
		id = collections.namedtuple("UniqueConstraintCommentID", ["type", "object"])
		contype = "u"

	def columns(self, connection=None):
		raise NotImplementedError

UniqueConstraint.Comment.Object = UniqueConstraint


class CheckConstraint(Constraint):
	type = "check constraint"
	names = collections.namedtuple("CheckConstraintNames", ["schema", "table", "constraint"])
	id = collections.namedtuple("CheckConstraintID", ["type", "object"])
	contype = "c"

	class Comment(Constraint.Comment):
		type = "check constraint comment"
		names = collections.namedtuple("CheckConstraintCommentNames", ["schema", "table", "constraint"])
		id = collections.namedtuple("CheckConstraintCommentID", ["type", "object"])
		contype = "c"

CheckConstraint.Comment.Object = CheckConstraint


Constraint.types = dict(
	p=PrimaryKey,
	f=ForeignKey,
	u=UniqueConstraint,
	c=CheckConstraint,
)


class View(CommentedSchemaObject):
	type = "view"
	names = collections.namedtuple("ViewNames", ["schema", "view"])
	id = collections.namedtuple("ViewID", ["type", "object"])

	class Comment(CommentObject):
		type = "view comment"
		names = collections.namedtuple("ViewCommentNames", ["schema", "view"])
		id = collections.namedtuple("ViewCommentID", ["type", "object"])

		def _query(self, cursor):
			query = _relquery(
				"obj_description(r.oid, 'pg_class') as comment",
				relkind="v",
				nsp=self.names.schema,
				rel=self.names.view,
			)
			query.execute(cursor)

	class Column(ColumnObject):
		type = "view column"
		names = collections.namedtuple("ViewColumnNames", ["schema", "view", "column"])
		id = collections.namedtuple("ViewColumnID", ["type", "object", "index"])
		relkind = "v"

		class Comment(ColumnObject.Comment):
			type = "view column comment"
			names = collections.namedtuple("ViewColumnCommentNames", ["schema", "view", "column"])
			id = collections.namedtuple("ViewColumnCommentID", ["type", "object", "index"])
			relkind = "v"

		def view(self, connection=None):
			return View(self.name.rpartition(".")[0], self.getconnection(connection))

		def ________________references(self, connection=None):
			yield self.view(connection)

	def _identify(self, cursor):
		query = _relquery(
			"'pg_class'::regclass::int",
			"r.oid",
			relkind="v",
			nsp=self.names.schema,
			rel=self.names.view,
		)
		query.execute(cursor)

	def columns(self, connection=None):
		query = _attquery(
			"n.nspname || '.' || c.relname || '.' || a.attname as name",
			relkind="v",
			nsp=self.names.schema,
			rel=self.names.view,
		)
		for r in query.execute(self.getcursor(connection)):
			yield self.Column(r.name, c.connection)

	def records(self, connection=None):
		cursor = self.getcursor(connection)
		cursor.execute(f"select * from {self.name};")
		yield from cursor

	def createsql(self, connection=None):
		cursor = self.getcursor(connection)
		query = _relquery(
			"pg_catalog.pg_get_viewdef(r.oid) as view_def",
			relkind="v",
			nsp=self.names.schema,
			rel=self.names.view,
		)
		query.execute(cursor)
		r = cursor.fetchone()
		return f"create or replace view {self.name}\nas\n{r.view_def};"

View.Comment.Object = View
View.Column.Comment.Object = View.Column


class MaterializedView(View):
	type = "materialized view"
	names = collections.namedtuple("MaterializedViewNames", ["schema", "materializedview"])
	id = collections.namedtuple("MaterializedViewID", ["type", "object"])

	class Comment(CommentObject):
		type = "materialized view comment"
		names = collections.namedtuple("MaterializedViewCommentNames", ["schema", "materializedview"])
		id = collections.namedtuple("MaterializedViewCommentID", ["type", "object"])

	def _identify(self, cursor):
		query = _relquery(
			"'pg_class'::relclass::int",
			"r.oid",
			relkind="m",
			nsp=self.names.schema,
			rel=self.names.view,
		)
		query.execute(cursor)


MaterializedView.Comment.Object = MaterializedView


class Sequence(CommentedSchemaObject):
	type = "sequence"
	names = collections.namedtuple("SequenceNames", ["schema", "sequence"])
	id = collections.namedtuple("SequenceID", ["type", "object"])

	seqtypes = dict(
		int2=(-(1<<15), (1<<15)-1, "smallint"),
		int4=(-(1<<31), (1<<31)-1, "integer"),
		int8=(-(1<<63), (1<<63)-1, "bigint"),
		default=(0.5, 0.5, "bigint"),
	)

	class Comment(CommentObject):
		type = "sequence comment"
		names = collections.namedtuple("SequenceCommentNames", ["schema", "sequence"])
		id = collections.namedtuple("SequenceCommentID", ["type", "object"])

		def _query(self, cursor):
			query = _relquery(
				"obj_description(r.oid, 'pg_class') as comment",
				relkind="S",
				nsp=self.names.schema,
				rel=self.names.sequence,
			)
			query.execute(cursor)

	def _identify(self, cursor):
		query = (_SQL()
			.select("'pg_class'::regclass::int")
			.select("t.oid")
			.from_("pg_catalog.pg_namespace n")
			.join("pg_catalog.pg_class c on n.oid = c.relnamespace")
			.join("pg_catalog.pg_sequence s on c.oid = s.seqrelid")
			.join("pg_catalog.pg_type t on c.oid = s.seqrelid and s.seqtypid = t.oid")
			.where("c.relkind = 'S'")
			.where("n.nspname = %s").param(self.names.schema)
			.where("c.relname = %s").param(self.names.sequence)
		)
		query.execute(cursor)

	def createsql(self, connection=None, exists_ok=False):
		cursor = self.getcursor(connection)
		query = (_SQL()
			.select("s.*")
			.select("t.typname")
			.from_("pg_catalog.pg_namespace n")
			.join("pg_catalog.pg_class c on n.oid = c.relnamespace")
			.join("pg_catalog.pg_sequence s on c.oid = s.seqrelid")
			.join("pg_catalog.pg_type t on c.oid = s.seqrelid and s.seqtypid = t.oid")
			.where("c.relkind = 'S'")
			.where("n.nspname = %s").param(self.names.schema)
			.where("c.relname = %s").param(self.names.sequence)
		)
		r = query.execute(cursor).fetchone()
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

Sequence.Comment.Object = Sequence


class CallableObject(CommentedSchemaObject):
	class Comment(CommentObject):
		def _query(self, cursor):
			query = _proquery(
				"obj_description(p.oid, 'pg_proc') as comment",
				prokind=f"= '{self.prokind}'",
				nsp=self.names.schema,
				pro=self.names[-1], # might be "procedure" or "function"
			)
			query.execute(cursor)

	def arguments(self, connection=None):
		raise NotImplementedError

	def __call__(self, cursor, *args, **kwargs):
		raise NotImplementedError

	def _identify(self, cursor):
		query = _proquery(
			"'pg_proc'::regclass::int",
			"p.oid",
			prokind=f"= '{self.prokind}'",
			nsp=self.names.schema,
			pro=self.names[-1], # might be "procedure" or "function"
		)
		query.execute(cursor)

	def createsql(self, connection=None):
		cursor = self.getcursor(connection)
		query = _proquery(
			"p.prokind",
			"p.proname",
			"l.lanname",
			"p.provolatile",
			"p.prosrc",
			"pg_catalog.pg_get_function_arguments(p.oid) as args_def",
			"pg_catalog.pg_get_function_result(p.oid) as return_def",
			prokind=f"= '{self.prokind}'",
			nsp=self.names.schema,
			pro=self.names[-1], # might be "procedure" or "function"
			lan=True,
		)
		r = query.execute(cursor).fetchone()
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
	id = collections.namedtuple("ProcedureID", ["type", "object"])
	prokind = "p"

	class Comment(CallableObject.Comment):
		type = "procedure comment"
		names = collections.namedtuple("ProcedureCommentNames", ["schema", "procedure"])
		id = collections.namedtuple("ProcedureCommentID", ["type", "object"])
		prokind = "p"

Procedure.Comment.Object = Procedure


class Function(CallableObject):
	type = "function"
	names = collections.namedtuple("FunctionNames", ["schema", "function"])
	id = collections.namedtuple("FunctionID", ["type", "object"])
	prokind = "f"

	class Comment(CallableObject.Comment):
		type = "function comment"
		names = collections.namedtuple("FunctionCommentNames", ["schema", "function"])
		id = collections.namedtuple("FunctionCommentID", ["type", "object"])
		prokind = "f"

Function.Comment.Object = Function


CallableObject.types = dict(
	f=Function,
	p=Procedure,
)
