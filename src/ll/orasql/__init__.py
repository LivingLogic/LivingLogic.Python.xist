# -*- coding: utf-8 -*-
# cython: language_level=3

## Copyright 2004-2014 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2004-2014 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`ll.orasql` contains utilities for working with cx_Oracle__:

*	It allows calling procedures with keyword arguments (via the
	:class:`Procedure` class).

*	Query results will be put into :class:`Record` objects, where database
	fields are accessible as object attributes.

*	The :class:`Connection` class provides methods for iterating through the
	database metadata.

*	Importing this module adds support for URLs with the scheme ``oracle`` to
	:mod:`ll.url`. Examples of these URLs are::

		oracle://user:pwd@db/
		oracle://user:pwd@db/view/
		oracle://user:pwd@db/view/USER_TABLES.sql
		oracle://sys:pwd:sysdba@db/

__ http://cx-oracle.sourceforge.net/
"""


import urllib.request, urllib.parse, urllib.error, datetime, itertools, io, errno, re, fnmatch, unicodedata, collections

from cx_Oracle import *

from ll import misc, url as url_


__docformat__ = "reStructuredText"


bigbang = datetime.datetime(1970, 1, 1, 0, 0, 0) # timestamp for Oracle "directories"


ALL = object() # marker object for specifying a user


class SQLObjectNotFoundError(IOError):
	def __init__(self, obj):
		IOError.__init__(self, errno.ENOENT, "no such {}: {}".format(obj.type, obj.getfullname()))
		self.obj = obj


class SQLNoSuchObjectError(Exception):
	def __init__(self, name, owner):
		self.name = name
		self.owner = owner

	def __repr__(self):
		return "<{}.{} name={!r} owner={!r} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.name, self.owner, id(self))

	def __str__(self):
		if self.owner is None:
			return "no object named {!r}".format(self.name)
		else:
			return "no object named {!r} for owner {!r}".format(self.name, self.owner)


class UnknownModeError(ValueError):
	def __init__(self, mode):
		self.mode = mode

	def __repr__(self):
		return "<{}.{} mode={!r} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.mode, id(self))

	def __str__(self):
		return "unknown mode {!r}".format(self.mode)


class ConflictError(ValueError):
	def __init__(self, object, message):
		self.object = object
		self.message = message

	def __repr__(self):
		return "<{}.{} object={!r} message={!r} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.object, self.message, id(self))

	def __str__(self):
		return "conflict in {!r}: {}".format(self.object, self.message)


class Args(dict):
	"""
	An :class:`Args` object is a subclass of :class:`dict` that is used for
	passing arguments to procedures and functions. Both item and attribute access
	(i.e. :meth:`__getitem__` and :meth:`__getattr__`) are available. Names are
	case insensitive.
	"""
	def __init__(self, arg=None, **kwargs):
		dict.__init__(self)
		self.update(arg, **kwargs)

	def update(self, arg=None, **kwargs):
		if arg is not None:
			# if arg is a mapping use iteritems
			dict.update(self, ((key.lower(), value) for (key, value) in getattr(arg, "iteritems", arg)))
		dict.update(self, ((key.lower(), value) for (key, value) in kwargs.items()))

	def __getitem__(self, name):
		return dict.__getitem__(self, name.lower())

	def __setitem__(self, name, value):
		dict.__setitem__(self, name.lower(), value)

	def __delitem__(self, name):
		dict.__delitem__(self, name.lower())

	def __getattr__(self, name):
		try:
			return self.__getitem__(name)
		except KeyError:
			raise AttributeError(name)

	def __setattr__(self, name, value):
		self.__setitem__(name, value)

	def __delattr__(self, name):
		try:
			self.__delitem__(name)
		except KeyError:
			raise AttributeError(name)

	def __repr__(self):
		return "{}.{}({})".format(self.__class__.__module__, self.__class__.__name__, ", ".join("{}={!r}".format(*item) for item in self.items()))


class LOBStream(object):
	"""
	A :class:`LOBStream` object provides streamlike access to a ``BLOB`` or ``CLOB``.
	"""

	def __init__(self, value):
		self.value = value
		self.pos = 0

	def readall(self):
		"""
		Read all remaining data from the stream and return it.
		"""
		result = self.value.read(self.pos+1)
		self.pos = self.value.size()
		return result

	def readchunk(self):
		"""
		Read a chunk of data from the stream and return it. Reading is done in
		optimally sized chunks.
		"""
		size = self.value.getchunksize()
		bytes = self.value.read(self.pos+1, size)
		self.pos += size
		if self.pos >= self.value.size():
			self.pos = self.value.size()
		return bytes

	def read(self, size=None):
		"""
		Read :obj:`size` bytes/characters from to stream and return them.
		If :obj:`size` is :const:`None`, all remaining data will be read.
		"""
		if size is None:
			return self.readall()
		if size <= 0:
			return self.readchunk()
		data = self.value.read(self.pos+1, size)
		self.pos += size
		if self.pos >= self.value.size():
			self.pos = self.value.size()
		return data

	def reset(self):
		"""
		Reset the stream, so that the next :meth:`read` call starts at the
		beginning of the LOB.
		"""
		self.pos = 0

	def seek(self, offset, whence=0):
		"""
		Seek to the position :obj:`offset` in the LOB. The :obj:`whence` argument
		is optional and defaults to ``0`` (absolute file positioning);
		The other allowed value is ``1`` (seek relative to the current position).
		"""
		if whence == 0:
			self.pos = whence
		elif whence == 1:
			self.pos += whence
		else:
			raise ValueError("unkown whence: {!r}".format(whence))
		size = self.value.size()
		if self.pos >= size:
			self.pos = size
		elif self.pos < 0:
			self.pos = 0


def _decodelob(value, readlobs):
	if value is not None:
		if readlobs is True or (isinstance(readlobs, int) and value.size() <= readlobs):
			value = value.read()
		else:
			value = LOBStream(value)
	return value


class RecordMaker(object):
	def __init__(self, cursor):
		self._readlobs = cursor.readlobs
		self._index2name = tuple(d[0].lower() for d in cursor.description)
		self._index2conv = tuple(getattr(self, d[1].__name__, self.DEFAULT) for d in cursor.description)

	def __call__(self, *row):
		row = tuple(conv(value) for (conv, value) in zip(self._index2conv, row))
		name2index = dict(zip(self._index2name, itertools.count()))
		return Record(self._index2name, name2index, row)

	def CLOB(self, value):
		return _decodelob(value, self._readlobs)

	def NCLOB(self, value):
		return _decodelob(value, self._readlobs)

	def BLOB(self, value):
		return _decodelob(value, self._readlobs)

	def DEFAULT(self, value):
		return value


class Record(tuple, collections.Mapping):
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
			raise AttributeError("'{}' object has no attribute {!r}".format(self.__class__.__name__, name))
		return tuple.__getitem__(self, index)

	def get(self, name, default=None):
		"""
		Return the value for the field named :obj:`name`. If this field doesn't
		exist in :obj:`self`, return :obj:`default` instead.
		"""
		try:
			index = self._name2index[name.lower()]
		except KeyError:
			return default
		return tuple.__getitem__(self, index)

	def __contains__(self, name):
		return name.lower() in self._name2index

	def iterkeys(self):
		"""
		Return an iterator over field names
		"""
		return iter(self._index2name)

	def keys(self):
		"""
		Return a list of field names
		"""
		return self._index2name

	def items(self):
		"""
		Return a list of (field name, field value) tuples.
		"""
		return [(key, tuple.__getitem__(self, index)) for (index, key) in enumerate(self._index2name)]

	def iteritems(self):
		"""
		Return an iterator over (field name, field value) tuples.
		"""
		return ((key, tuple.__getitem__(self, index)) for (index, key) in enumerate(self._index2name))

	def __repr__(self):
		return "<{}.{} {} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, ", ".join("{}={!r}".format(*item) for item in self.items()), id(self))


class SessionPool(SessionPool):
	"""
	:class:`SessionPool` is a subclass of :class:`cx_Oracle.SessionPool`.
	"""

	def __init__(self, user, password, database, min, max, increment, connectiontype=None, threaded=False, getmode=SPOOL_ATTRVAL_NOWAIT, homogeneous=True):
		if connectiontype is None:
			connectiontype = Connection
		super().__init__(user, password, database, min, max, increment, connectiontype, threaded, getmode, homogeneous)

	def connectstring(self):
		return "{}@{}".format(self.username, self.tnsentry)

	def __repr__(self):
		return "<{}.{} object db={!r} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.connectstring(), id(self))


class Connection(Connection):
	"""
	:class:`Connection` is a subclass of :class:`cx_Oracle.Connection`.
	"""
	def __init__(self, *args, **kwargs):
		"""
		Create a new connection. In addition to the parameters supported by
		:func:`cx_Oracle.connect` the following keyword argument is supported.

		:obj:`readlobs` : bool or integer
			If :obj:`readlobs` is :const:`False` all cursor fetches return
			:class:`CLOBStream` or :class:`BLOBStream` objects for LOB object.
			If :obj:`readlobs` is an :class:`int` LOBs with a maximum size of
			:obj:`readlobs` will be returned as :class:`bytes`/:class:`str` objects.
			If :obj:`readlobs` is :const:`True` all LOB values will be
			returned as :class:`bytes`/:class:`str` objects.

		Furthermore the ``clientinfo`` will be automatically set to the name
		of the currently running script (except if the :obj:`clientinfo` keyword
		argument is given and :const:`None`).
		"""
		if "readlobs" in kwargs:
			kwargs = kwargs.copy()
			self.readlobs = kwargs.pop("readlobs", False)
		else:
			self.readlobs = False
		if "clientinfo" not in kwargs:
			kwargs = kwargs.copy()
			kwargs["clientinfo"] = misc.sysinfo.short_script_name[-64:]
		elif kwargs["clientinfo"] is None:
			kwargs = kwargs.copy()
			del kwargs["clientinfo"]
		super().__init__(*args, **kwargs)
		self.mode = kwargs.get("mode")
		self._ddprefix = None # Do we have access to the ``DBA_*`` views?
		self._ddprefixargs = None # Do we have access to the ``DBA_ARGUMENTS`` view (which doesn't exist in Oracle 10)?

	def connectstring(self):
		return "{}@{}".format(self.username, self.tnsentry)

	def cursor(self, readlobs=None):
		"""
		Return a new cursor for this connection. For the meaning of
		:obj:`readlobs` see :meth:`__init__`.
		"""
		return Cursor(self, readlobs=readlobs)

	def __repr__(self):
		return "<{}.{} object db={!r} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.connectstring(), id(self))

	def itertables(self, owner=ALL, mode="flat"):
		"""
		Generator that yields all table definitions in the current users schema
		(or all users schemas). :obj:`mode` specifies the order in which tables
		will be yielded:

		``"create"``
			Create order, deleting records from the table in this order will not
			violate foreign key constraints.

		``"drop"``
			Drop order, deleting records from the table in this order will not
			violate foreign key constraints.

		``"flat"``
			Unordered.

 		:obj:`schema` specifies from which user tables should be yielded:

		``"user"``
			Only tables belonging to the current user (and those objects these
			depend on) will be yielded (i.e. tables from the ``USER_TABLES`` view).

		``"all"``
			All tables accessible to the current user will be yielded (i.e. tables
			from the ``ALL_TABLES`` views).

		``"dba"``
			All tables from all users will be yielded (i.e. tables from the
			``DBA_TABLES`` view, this requires the appropriate privileges).

		Tables that are materialized views will be skipped in all cases.
		"""
		if mode not in ("create", "drop", "flat"):
			raise UnknownModeError(mode)

		cursor = self.cursor()

		tables = Table.iterobjects(self, owner)

		if mode == "flat":
			yield from tables
		else:
			done = set()

			tables = {(table.name, table.owner): table for table in tables}
			def do(table):
				if table not in done:
					done.add(table)
					cursor.execute("select ac1.table_name, decode(ac1.owner, user, null, ac1.owner) as owner from {0}_constraints ac1, {0}_constraints ac2 where ac1.constraint_type = 'R' and ac2.table_name=:name and ac2.owner = nvl(:owner, user) and ac1.r_constraint_name = ac2.constraint_name and ac1.r_owner = ac2.owner".format(cursor.ddprefix()), name=table.name, owner=table.owner)
					for rec in cursor.fetchall():
						try:
							t2 = tables[(rec.table_name, rec.owner)]
						except KeyError:
							pass
						else:
							yield from do(t2)
					yield table
			for table in tables.values():
				yield from do(table)

	def itersequences(self, owner=ALL):
		"""
		Generator that yields sequences. :obj:`owner` can be :const:`None`,
		:const:`ALL` (the default) or a user name.
		"""
		return Sequence.iterobjects(self, owner)

	def iterfks(self, owner=ALL):
		"""
		Generator that yields all foreign key constraints. :obj:`owner` can be
		:const:`None`, :const:`ALL` (the default) or a user name.
		"""
		return ForeignKey.iterobjects(self, owner)

	def iterprivileges(self, owner=ALL):
		"""
		Generator that yields object privileges. :obj:`owner` can be :const:`None`,
		:const:`ALL` (the default) or a user name.
		"""
		return Privilege.iterobjects(self, owner)

	def iterusers(self):
		"""
		Generator that yields all users.
		"""
		return User.iterobjects(self)

	def iterobjects(self, owner=ALL, mode="create"):
		"""
		Generator that yields the sequences, tables, primary keys, foreign keys,
		comments, unique constraints, indexes, views, functions, procedures,
		packages and types in the current users schema (or all users schemas)
		in a specified order.

		:obj:`mode` specifies the order in which objects will be yielded:

		``"create"``
			Create order, i.e. recreating the objects in this order will not lead
			to errors.

		``"drop"``
			Drop order, i.e. dropping the objects in this order will not lead to
			errors.

		``"flat"``
			Unordered.

		:obj:`owner` specifies from which schema objects should be yielded:

			:const:`None`
				All objects belonging to the current user (i.e. via the view
				``USER_OBJECTS``).

			:const:`ALL`
				All objects for all users (via the views ``ALL_OBJECTS`` or
				``DBA_OBJECTS``)

			username : string
				All objects belonging to the specified user
		"""
		if mode not in ("create", "drop", "flat"):
			raise UnknownModeError(mode)

		done = set()

		cursor = self.cursor()

		def do(obj):
			if mode == "create":
				yield from obj.iterreferencesall(self, done)
			elif mode == "drop":
				yield from obj.iterreferencedbyall(self, done)
			else:
				if obj not in done:
					done.add(obj)
					yield obj

		def dosequences():
			for sequence in Sequence.iterobjects(self, owner):
				yield from do(sequence)

		def dotables():
			for table in Table.iterobjects(self, owner):
				if mode == "create" or mode == "flat":
					yield from do(table)

				# Primary key
				pk = table.pk()
				if pk is not None:
					yield from do(pk)

				# Comments
				for comment in table.itercomments():
					# No dependency checks neccessary, but use ``do`` anyway
					yield from do(comment)

				if mode == "drop":
					yield from do(table)

		def dorest():
			for type in (UniqueConstraint, ForeignKey, Preference, Index, Synonym, View, MaterializedView, Function, Procedure, Package, PackageBody, Type, Trigger, JavaSource):
				for obj in type.iterobjects(self, owner):
					yield from do(obj)

		funcs = [dosequences, dotables, dorest]
		if mode == "drop":
			funcs = reversed(funcs)

		for func in funcs:
			yield from func()

	def _getobject(self, name, owner=None):
		cursor = self.cursor()
		cursor.execute("select object_name, decode(owner, user, null, owner) as owner, object_type from {0}_objects where object_name = :object_name and owner = nvl(:owner, user)".format(cursor.ddprefix()), object_name=name, owner=owner)
		rec = cursor.fetchone()
		if rec is not None:
			type = rec.object_type.lower()
			try:
				cls = Object.name2type[type]
			except KeyError:
				raise TypeError("type {} not supported".format(type))
			else:
				return cls(rec.object_name, rec.owner, self)
		raise SQLNoSuchObjectError(name, owner)

	def getobject(self, name, owner=None):
		"""
		Return the object named :obj:`name` from the schema. If :obj:`owner` is
		:const:`None` the current schema is queried, else the specified one is
		used. :obj:`name` and :obj:`owner` are treated case insensitively.
		"""
		if isinstance(name, str):
			name = str(name)
		if isinstance(owner, str):
			owner = str(owner)
		cursor = self.cursor()
		if "." in name:
			name = name.split(".")
			query = """
				select
					decode(owner, user, null, owner) as owner,
					object_name || '.' || procedure_name as object_name,
					decode((select count(*) from {0}_arguments where owner = nvl(:owner, user) and lower(object_name) = lower(:object_name) and lower(package_name) = lower(:package_name) and argument_name is null), 0, 'procedure', 'function') as object_type
				from
					{0}_procedures
				where
					lower(procedure_name) = lower(:object_name) and
					lower(owner) = lower(nvl(:owner, user)) and
					lower(object_name) = lower(:package_name)
			""".format(cursor.ddprefix())
			cursor.execute(query, object_name=name[1], package_name=name[0], owner=owner)
		else:
			query = """
				select
					object_name,
					decode(owner, user, null, owner) as owner,
					object_type
				from
					{}_objects
				where
					lower(object_name) = lower(:object_name) and
					lower(owner) = lower(nvl(:owner, user))
			""".format(cursor.ddprefix())
			cursor.execute(query, object_name=name, owner=owner)

		rec = cursor.fetchone()
		if rec is not None:
			type = rec.object_type.lower()
			try:
				cls = Object.name2type[type]
			except KeyError:
				raise TypeError("type {} not supported".format(type))
			else:
				return cls(rec.object_name, rec.owner, self)
		raise SQLNoSuchObjectError(name, owner)


def connect(*args, **kwargs):
	"""
	Create a connection to the database and return a :class:`Connection` object.
	"""
	return Connection(*args, **kwargs)


class Cursor(Cursor):
	"""
	A subclass of the cursor class in :mod:`cx_Oracle`. The "fetch" methods
	will return records as :class:`Record` objects and  ``LOB`` values will be
	returned as stream objects or :class:`str`/:class:`bytes` (depending of the
	the cursors :attr:`readlobs` attribute).
	"""
	def __init__(self, connection, readlobs=None):
		"""
		Return a new cursor for the connection :obj:`connection`. For the meaning
		of :obj:`readlobs` see :meth:`Connection.__init__`.
		"""
		super().__init__(connection)
		self.readlobs = (readlobs if readlobs is not None else connection.readlobs)

	def ddprefix(self):
		"""
		Return whether the user has access to the ``DBA_*`` views (``"dba"``) or
		not (``"all"``).
		"""
		if self.connection._ddprefix is None:
			try:
				self.execute("select /*+FIRST_ROWS(1)*/ table_name from dba_tables")
			except DatabaseError as exc:
				if exc.args[0].code == 942: # ORA-00942: table or view does not exist
					self.connection._ddprefix = "all"
				else:
					raise
			else:
				self.connection._ddprefix = "dba"
		return self.connection._ddprefix

	def ddprefixargs(self):
		"""
		Return whether the user has access to the ``DBA_ARGUMENTS`` view
		(``"dba"``) or not (``"all"``).
		"""
		# This method is separate from :meth:`ddprefix`, because Oracle 10 doesn't
		# have a ``DBA_ARGUMENTS`` view.
		if self.connection._ddprefixargs is None:
			try:
				self.execute("select /*+FIRST_ROWS(1)*/ object_name from dba_arguments")
			except DatabaseError as exc:
				if exc.args[0].code == 942: # ORA-00942: table or view does not exist
					self.connection._ddprefixargs = "all"
				else:
					raise
			else:
				self.connection._ddprefixargs = "dba"
		return self.connection._ddprefixargs

	def execute(self, statement, parameters=None, **kwargs):
		if parameters is not None:
			result = super().execute(statement, parameters, **kwargs)
		else:
			result = super().execute(statement, **kwargs)
		if self.description is not None:
			self.rowfactory = RecordMaker(self)
		return result

	def executemany(self, statement, parameters):
		result = super().executemany(statement, parameters)
		if self.description is not None:
			self.rowfactory = RecordMaker(self)
		return result

	def __repr__(self):
		return "<{}.{} statement={!r} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.statement, id(self))


def formatstring(value, latin1=False):
	result = []
	current = []

	if latin1:
		upper = 255
	else:
		upper = 127
	# Helper function: move the content of current to result

	def shipcurrent(force=False):
		if current and (force or (len(current) > 2000)):
			if result:
				result.append(" || ")
			result.append("'{}'".format("".join(current)))

	for c in value:
		if c == "'":
			current.append("''")
			shipcurrent()
		elif ord(c) < 32 or ord(c) > upper:
			shipcurrent(True)
			current = []
			if result:
				result.append(" || ")
			result.append("chr({})".format(ord(c)))
		else:
			current.append(c)
			shipcurrent()
	shipcurrent(True)
	return "".join(result)


def makeurl(name):
	return urllib.request.pathname2url(name.encode("utf-8")).replace("/", "%2f")


###
### Classes used for database meta data
###

class MixinNormalDates(object):
	"""
	Mixin class that provides methods for determining creation and modification
	dates for objects.
	"""
	def cdate(self, connection=None):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select created, to_number(to_char(systimestamp, 'TZH')), to_number(to_char(systimestamp, 'TZM')) from {}_objects where lower(object_type)=:type and object_name=:name and owner=nvl(:owner, user)".format(cursor.ddprefix()), type=self.__class__.type, name=self.name, owner=self.owner)
		row = cursor.fetchone()
		if row is None:
			raise SQLObjectNotFoundError(self)
		# FIXME: This is only correct 50% of the time, but Oracle doesn't provide anything better
		return row[0]-datetime.timedelta(seconds=60*(row[1]*60+row[2]))

	def udate(self, connection=None):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select last_ddl_time, to_number(to_char(systimestamp, 'TZH')), to_number(to_char(systimestamp, 'TZM')) from {}_objects where lower(object_type)=:type and object_name=:name and owner=nvl(:owner, user)".format(cursor.ddprefix()), type=self.__class__.type, name=self.name, owner=self.owner)
		row = cursor.fetchone()
		if row is None:
			raise SQLObjectNotFoundError(self)
		# FIXME: This is only correct 50% of the time, but Oracle doesn't provide anything better
		return row[0]-datetime.timedelta(seconds=60*(row[1]*60+row[2]))


class MixinCodeDDL(object):
	"""
	Mixin class that provides methods returning the create and drop statements
	for various objects.
	"""
	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select text from {}_source where lower(type)=lower(:type) and owner=nvl(:owner, user) and name=:name order by line".format(cursor.ddprefix()), type=self.__class__.type, owner=self.owner, name=self.name)
		code = "\n".join((rec.text or "").rstrip() for rec in cursor) # sqlplus strips trailing spaces when executing SQL scripts, so we do that too
		if not code:
			return ""
		code = " ".join(code.split(None, 1)) # compress "PROCEDURE          FOO"
		code = code.strip()
		type = self.__class__.type
		code = code[code.lower().find(type)+len(type):].strip() # drop "procedure" etc.
		# drop our own name (for triggers this includes the schema name)
		if code.startswith('"'):
			code = code[code.find('"', 1)+1:]
		else:
			while code and (code[0].isalnum() or code[0] in "_$."):
				code = code[1:]
		code = code.strip()
		code = "create or replace {} {}\n{}\n".format(type, self.getfullname(), code)
		if term:
			code += "\n/\n"
		else:
			code += "\n"
		return code

	def dropddl(self, connection=None, term=True):
		if self.owner is not None:
			name = "{}.{}".format(self.owner, self.name)
		else:
			name = self.name
		code = "drop {} {}".format(self.__class__.type, name)
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def fixname(self, code):
		if code:
			code = code.split(None, 5)
			code = "create or replace {} {}\n{}".format(code[3], self.getfullname(), code[5])
		return code


def getfullname(name, owner):
	parts = []
	if owner is not None:
		if owner != owner.upper() or not all(c.isalnum() or c == "_" for c in owner):
			part = '"{}"'.format(owner)
		parts.append(owner)
	for part in name.split("."):
		if part != part.upper() or not all(c.isalnum() or c == "_" for c in part):
			part = '"{}"'.format(part)
		parts.append(part)
	return ".".join(parts)


class _Object_meta(type):
	def __new__(mcl, name, bases, dict):
		typename = None
		if "type" in dict and name != "Object":
			typename = dict["type"]
		cls = type.__new__(mcl, name, bases, dict)
		if typename is not None:
			Object.name2type[typename] = cls
		return cls


class Object(object, metaclass=_Object_meta):
	"""
	The base class for all Python classes modelling schema objects in the
	database.

	Subclasses are: :class:`Sequence`, :class:`Table`, :class:`PrimaryKey`,
	:class:`Comment`, :class:`ForeignKey`, :class:`Index`, :class:`Unique`,
	:class:`Synonym`, :class:`View`, :class:`MaterializedView`, :class:`Library`,
	:class:`Function`, :class:`Package`, :class:`Type`, :class:`Trigger`,
	:class:`JavaSource` and :class:`Column`.
	"""
	name2type = {} # maps the Oracle type name to the Python class (populated by the metaclass)

	def __init__(self, name, owner=None, connection=None):
		self.name = name
		self.owner = owner
		self.connection = connection

	def __repr__(self):
		if self.owner is not None:
			return "{}.{}({!r}, {!r})".format(self.__class__.__module__, self.__class__.__name__, self.name, self.owner)
		else:
			return "{}.{}({!r})".format(self.__class__.__module__, self.__class__.__name__, self.name)

	def __str__(self):
		if self.owner is not None:
			return "{}({}, {})".format(self.__class__.__name__, self.name, self.owner)
		else:
			return "{}({})".format(self.__class__.__name__, self.name)

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.name == other.name and self.owner == other.owner

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.__class__.__name__) ^ hash(self.name) ^ hash(self.owner)

	def getfullname(self):
		return getfullname(self.name, self.owner)

	@misc.notimplemented
	def createddl(self, connection=None, term=True):
		"""
		Return SQL code to create this object.
		"""

	@misc.notimplemented
	def dropddl(self, connection=None, term=True):
		"""
		Return SQL code to drop this object
		"""

	@misc.notimplemented
	def fixname(self, code):
		"""
		Replace the name of the object in the SQL code :obj:`code` with
		the name of :obj:`self`.
		"""

	@misc.notimplemented
	def cdate(self, connection=None):
		"""
		Return a :class:`datetime.datetime` object with the creation date of
		:obj:`self` in the database specified by :obj:`connection` (or
		:const:`None` if such information is not available).
		"""

	@misc.notimplemented
	def udate(self, connection=None):
		"""
		Return a :class:`datetime.datetime` object with the last modification
		date of :obj:`self` in the database specified by :obj:`connection`
		(or :const:`None` if such information is not available).
		"""

	def iterreferences(self, connection=None):
		"""
		Objects directly used by :obj:`self`.

		If :obj:`connection` is not :const:`None` it will be used as the database
		connection from which to fetch data. If :obj:`connection` is :const:`None`
		the connection from which :obj:`self` has been extracted will be used. If
		there is not such connection, you'll get an exception.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select referenced_type, decode(referenced_owner, user, null, referenced_owner) as referenced_owner, referenced_name from {}_dependencies where type=upper(:type) and name=:name and owner=nvl(:owner, user) and type != 'NON-EXISTENT'".format(cursor.ddprefix()), type=self.type, name=self.name, owner=self.owner)
		for rec in cursor.fetchall():
			try:
				cls = Object.name2type[rec.referenced_type.lower()]
			except KeyError:
				pass # FIXME: Issue a warning?
			else:
				yield cls(rec.referenced_name, rec.referenced_owner, connection)

	def iterreferencesall(self, connection=None, done=None):
		"""
		All objects used by :obj:`self` (recursively).

		For the meaning of :obj:`connection` see :meth:`iterreferences`.

		:obj:`done` is used internally and shouldn't be passed.
		"""
		if done is None:
			done = set()
		if self not in done:
			done.add(self)
			for obj in self.iterreferences(connection):
				yield from obj.iterreferencesall(connection, done)
			yield self

	def iterreferencedby(self, connection=None):
		"""
		Objects using :obj:`self`.

		For the meaning of :obj:`connection` see :meth:`iterreferences`.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select type, decode(owner, user, null, owner) as owner, name from {}_dependencies where referenced_type=upper(:type) and referenced_name=:name and referenced_owner=nvl(:owner, user) and type != 'NON-EXISTENT'".format(cursor.ddprefix()), type=self.type, name=self.name, owner=self.owner)
		for rec in cursor.fetchall():
			try:
				type = Object.name2type[rec.type.lower()]
			except KeyError:
				pass # FIXME: Issue a warning?
			else:
				yield type(rec.name, rec.owner, connection)

	def iterreferencedbyall(self, connection=None, done=None):
		"""
		All objects depending on :obj:`self` (recursively).

		For the meaning of :obj:`connection` see :meth:`iterreferences`.

		:obj:`done` is used internally and shouldn't be passed.
		"""
		if done is None:
			done = set()
		if self not in done:
			done.add(self)
			for obj in self.iterreferencedby(connection):
				yield from obj.iterreferencedbyall(connection, done)
			yield self

	def getconnection(self, connection):
		if connection is None:
			connection = self.connection
		if connection is None:
			raise TypeError("no connection available")
		return connection

	def getcursor(self, connection):
		connection = self.getconnection(connection)
		return (connection, connection.cursor())

	def getconnectstring(self):
		if self.connection:
			return self.connection.connectstring()
		return None
	connectstring = property(getconnectstring)

	@classmethod
	def iternames(cls, connection, owner=ALL):
		"""
		Generator that yields the names of all objects of this type. The argument
		:obj:`owner` specifies whose objects are yielded:

			:const:`None`
				All objects belonging to the current user (i.e. via the view
				``USER_OBJECTS``).

			:const:`ALL`
				All objects for all users (via the views ``ALL_OBJECTS`` or
				``DBA_OBJECTS``)

			username : string
				All objects belonging to the specified user
		"""
		cursor = connection.cursor()
		if owner is None:
			cursor.execute("select null as owner, object_name from user_objects where lower(object_type) = :type and object_name not like 'BIN$%' and object_name not like 'DR$%' order by object_name", type=cls.type)
		elif owner is ALL:
			cursor.execute("select decode(owner, user, null, owner) as owner, object_name from {}_objects where lower(object_type) = :type and object_name not like 'BIN$%' and object_name not like 'DR$%' order by owner, object_name".format(cursor.ddprefix()), type=cls.type)
		else:
			cursor.execute("select decode(owner, user, null, owner) as owner, object_name from {}_objects where lower(object_type) = :type and object_name not like 'BIN$%' and object_name not like 'DR$%' and owner=:owner order by owner, object_name".format(cursor.ddprefix()), type=cls.type, owner=owner)
		return ((row.object_name, row.owner) for row in cursor)

	@classmethod
	def iterobjects(cls, connection, owner=ALL):
		"""
		Generator that yields all objects of this type in the current users schema.
		The argument :obj:`owner` specifies whose objects are yielded:

			:const:`None`
				All objects belonging to the current user (i.e. via the view
				``USER_OBJECTS``).

			:const:`ALL`
				All objects for all users (via the views ``ALL_OBJECTS`` or
				``DBA_OBJECTS``)

			username : string
				All objects belonging to the specified user
		"""
		return (cls(name[0], name[1], connection) for name in cls.iternames(connection, owner))


class Sequence(MixinNormalDates, Object):
	"""
	Models a sequence in the database.
	"""
	type = "sequence"

	def _createddl(self, connection, term, copyvalue):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select * from {}_sequences where sequence_owner=nvl(:owner, user) and sequence_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		code  = "create sequence {}\n".format(self.getfullname())
		code += "\tincrement by {}\n".format(rec.increment_by)
		if copyvalue:
			code += "\tstart with {}\n".format(rec.last_number + rec.increment_by)
		else:
			code += "\tstart with {}\n".format(rec.min_value)
		code += "\tmaxvalue {}\n".format(rec.max_value)
		code += "\tminvalue {}\n".format(rec.min_value)
		code += "\t{}cycle\n".format("" if rec.cycle_flag == "Y" else "no")
		if rec.cache_size:
			code += "\tcache {}\n".format(rec.cache_size)
		else:
			code += "\tnocache\n"
		code += "\t{}order".format("" if rec.cycle_flag == "Y" else "no")
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def createddl(self, connection=None, term=True):
		return self._createddl(connection, term, False)

	def createddlcopy(self, connection=None, term=True):
		"""
		Return SQL code to create an identical copy of this sequence.
		"""
		return self._createddl(connection, term, True)

	def dropddl(self, connection=None, term=True):
		code = "drop sequence {}".format(self.getfullname())
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def fixname(self, code):
		code = code.split(None, 3)
		code = "create sequence {}\n{}".format(self.getfullname(), code[3])
		return code

	def iterreferences(self, connection=None, done=None):
		# Shortcut: a sequence doesn't depend on anything
		if False:
			yield None


def _columntype(rec, data_precision=None, data_scale=None, char_length=None):
	ftype = rec.data_type.lower()
	if data_precision is None:
		data_precision = rec.data_precision
	if data_scale is None:
		data_scale = rec.data_scale
	if char_length is None:
		char_length = rec.char_length

	fsize = data_precision
	fprec = data_scale
	if ftype == "number" and fprec == 0 and fsize is None:
		ftype = "integer"
	elif ftype == "number" and fprec is None and fsize is None:
		ftype = "number"
	elif ftype == "number" and fprec == 0:
		ftype = "number({})".format(fsize)
	elif ftype == "number":
		ftype = "number({}, {})".format(fsize, fprec)
	elif ftype == "raw":
		ftype = "raw({})".format(rec.data_length)
	else:
		if char_length != 0:
			fsize = char_length
		if fsize is not None:
			ftype += "({}".format(fsize)
			if rec.char_used == "B":
				ftype += " byte"
			elif rec.char_used == "C":
				ftype += " char"
			if fprec is not None:
				ftype += ", {}".format(fprec)
			ftype += ")"
	return ftype


def _columndefault(rec):
	if rec.data_default is not None and rec.data_default != "null\n":
		return rec.data_default.rstrip("\n")
	return "null"


class Table(MixinNormalDates, Object):
	"""
	Models a table in the database.
	"""
	type = "table"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		if self.ismview(connection):
			return ""
		organization = self.organization(connection)
		cursor.execute("select * from {}_tab_columns where owner=nvl(:owner, user) and table_name=:name order by column_id asc".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		recs = cursor.fetchall()
		code = ["create table {}\n(\n".format(self.getfullname())]
		for (i, rec) in enumerate(recs):
			if i:
				code.append(",\n")
			code.append("\t{} {}".format(getfullname(rec.column_name, None), _columntype(rec)))
			default = _columndefault(rec)
			if default != "null":
				code.append(" default {}".format(default))
			if rec.nullable == "N":
				code.append(" not null")
		if term:
			code.append("\n);\n")
		else:
			code.append("\n)\n")
		return "".join(code)

	def dropddl(self, connection=None, term=True):
		if self.ismview(connection):
			return ""
		code = "drop table {}".format(self.getfullname())
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def fixname(self, code):
		code = code.split(None, 3)
		code = "create table {}\n{}".format(self.getfullname(), code[3])
		return code

	def mview(self, connection=None):
		"""
		The materialized view this table belongs to (or :const:`None` if it's a
		real table).
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select mview_name from {}_mviews where owner=nvl(:owner, user) and mview_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is not None:
			rec = MaterializedView(self.name, self.owner, connection)
		return rec

	def ismview(self, connection=None):
		"""
		Is this table a materialized view?
		"""
		return self.mview(connection) is not None

	def organization(self, connection=None):
		"""
		Return the organization of this table: either ``"heap"`` (for "normal"
		tables) or ``"index"`` (for index organized tables).
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select iot_type from {}_tables where owner=nvl(:owner, user) and table_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		return "heap" if rec.iot_type is None else "index"

	@classmethod
	def iternames(cls, connection, owner=ALL):
		# Skip tables that are materialized views
		cursor = connection.cursor()
		if owner is None:
			cursor.execute("select null as owner, table_name from user_tables where table_name not like 'BIN$%' and table_name not like 'DR$%' minus select null as owner, mview_name as table_name from user_mviews order by table_name")
		elif owner is ALL:
			cursor.execute("select decode(owner, user, null, owner) as owner, table_name from {0}_tables where table_name not like 'BIN$%' and table_name not like 'DR$%' minus select decode(owner, user, null, owner) as owner, mview_name as table_name from {0}_mviews order by owner, table_name".format(cursor.ddprefix()))
		else:
			cursor.execute("select decode(owner, user, null, owner) as owner, table_name from {0}_tables where table_name not like 'BIN$%' and table_name not like 'DR$%' and owner=:owner minus select decode(owner, user, null, owner) as owner, mview_name as table_name from {0}_mviews where owner=:owner order by table_name".format(cursor.ddprefix()), owner=owner)
		return ((row.table_name, row.owner) for row in cursor)

	def itercolumns(self, connection=None):
		"""
		Generator that yields all column objects of the :class:`Table` :obj:`self`.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select column_name from {}_tab_columns where owner=nvl(:owner, user) and table_name=:name order by column_id".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		return (Column("{}.{}".format(self.name, rec.column_name), self.owner, connection) for rec in cursor)

	def iterrecords(self, connection=None):
		"""
		Generator that yields all records of the table :obj:`self`.
		"""
		(connection, cursor) = self.getcursor(connection)
		query = "select * from {}".format(self.getfullname())
		cursor.execute(query)
		return iter(cursor)

	def itercomments(self, connection=None):
		"""
		Generator that yields all column comments of the table :obj:`self`.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select column_name from {}_tab_columns where owner=nvl(:owner, user) and table_name=:name order by column_id".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		return (Comment("{}.{}".format(self.name, rec.column_name), self.owner, connection) for rec in cursor)

	def _iterconstraints(self, connection, cond):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select decode(owner, user, null, owner) as owner, constraint_type, constraint_name from {}_constraints where constraint_type {} and owner=nvl(:owner, user) and table_name=:name".format(cursor.ddprefix(), cond), owner=self.owner, name=self.name)
		types = {"P": PrimaryKey, "U": UniqueConstraint, "R": ForeignKey}
		return (types[rec.constraint_type](rec.constraint_name, rec.owner, connection) for rec in cursor)

	def iterconstraints(self, connection=None):
		"""
		Generator that yields all constraints for this table.
		"""
		return self._iterconstraints(connection, "in ('P', 'U', 'R')")

	def pk(self, connection=None):
		"""
		Return the primary key constraint for this table (or :const:`None` if the
		table has no primary key constraint).
		"""
		return misc.first(self._iterconstraints(connection, "= 'P'"), None)

	def iterreferences(self, connection=None):
		connection = self.getconnection(connection)
		# A table doesn't depend on anything ...
		mview = self.mview(connection)
		if mview is not None:
			# ... unless it was created by a materialized view, in which case it depends on the view
			yield mview

	def iterreferencedby(self, connection=None):
		if not self.ismview(connection):
			yield from self.itercomments(connection)
			yield from self.iterconstraints(connection)
		for obj in super().iterreferencedby(connection):
			# skip the materialized view
			if not isinstance(obj, MaterializedView) or obj.name != self.name or obj.owner != self.owner:
				yield obj


class Constraint(Object):
	"""
	Base class of all constraints (primary key constraints, foreign key
	constraints and unique constraints).
	"""

	def cdate(self, connection=None):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select last_change, to_number(to_char(systimestamp, 'TZH')), to_number(to_char(systimestamp, 'TZM')) from {}_constraints where constraint_type=:type and constraint_name=:name and owner=nvl(:owner, user)".format(cursor.ddprefix()), type=self.constraint_type, name=self.name, owner=self.owner)
		row = cursor.fetchone()
		if row is None:
			raise SQLObjectNotFoundError(self)
		return None

	def udate(self, connection=None):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select last_change, to_number(to_char(systimestamp, 'TZH')), to_number(to_char(systimestamp, 'TZM')) from {}_constraints where constraint_type=:type and constraint_name=:name and owner=nvl(:owner, user)".format(cursor.ddprefix()), type=self.constraint_type, name=self.name, owner=self.owner)
		row = cursor.fetchone()
		if row is None:
			raise SQLObjectNotFoundError(self)
		# FIXME: This is only correct 50% of the time, but Oracle doesn't provide anything better
		return row[0]-datetime.timedelta(seconds=60*(row[1]*60+row[2]))

	@classmethod
	def iternames(cls, connection, owner=ALL):
		cursor = connection.cursor()
		if owner is None:
			cursor.execute("select null as owner, constraint_name from user_constraints where constraint_type=:type and constraint_name not like 'BIN$%' order by constraint_name", type=cls.constraint_type)
		elif owner is ALL:
			cursor.execute("select decode(owner, user, null, owner) as owner, constraint_name from {}_constraints where constraint_type=:type and constraint_name not like 'BIN$%' order by owner, constraint_name".format(cursor.ddprefix()), type=cls.constraint_type)
		else:
			cursor.execute("select decode(owner, user, null, owner) as owner, constraint_name from {}_constraints where constraint_type=:type and constraint_name not like 'BIN$%' and owner=:owner order by owner, constraint_name".format(cursor.ddprefix()), type=cls.constraint_type, owner=owner)
		return ((row.constraint_name, row.owner) for row in cursor)

	def fixname(self, code):
		code = code.split(None, 6)
		code = "alter table {} add constraint {} {}".format(code[2], self.getfullname(), code[6])
		return code


class PrimaryKey(Constraint):
	"""
	Models a primary key constraint in the database.
	"""
	type = "pk"
	constraint_type = "P"

	def itercolumns(self, connection=None):
		"""
		Return an iterator over the columns this primary key consists of.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select decode(owner, user, null, owner) as owner, constraint_name, table_name, r_owner, r_constraint_name from {}_constraints where constraint_type='P' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec2 = cursor.fetchone()
		if rec2 is None:
			raise SQLObjectNotFoundError(self)
		tablename = getfullname(rec2.table_name, rec2.owner)
		cursor.execute("select column_name from {}_cons_columns where owner=nvl(:owner, user) and constraint_name=:name order by position".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		return (Column("{}.{}".format(tablename, rec.column_name)) for rec in cursor)

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select decode(owner, user, null, owner) as owner, constraint_name, table_name, r_owner, r_constraint_name from {}_constraints where constraint_type='P' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec2 = cursor.fetchone()
		if rec2 is None:
			raise SQLObjectNotFoundError(self)
		cursor.execute("select column_name from {}_cons_columns where owner=nvl(:owner, user) and constraint_name=:name order by position".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		tablename = getfullname(rec2.table_name, rec2.owner)
		pkname = getfullname(self.name, None)
		code = "alter table {} add constraint {} primary key({})".format(tablename, pkname, ", ".join(r.column_name for r in cursor))
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def dropddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select decode(owner, user, null, owner) as owner, table_name from {}_constraints where owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		tablename = getfullname(rec.table_name, rec.owner)
		pkname = getfullname(self.name, None)
		code = "alter table {} drop constraint {}".format(tablename, pkname)
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def iterreferencedby(self, connection=None):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select decode(owner, user, null, owner) as owner, constraint_name from {}_constraints where constraint_type='R' and r_owner=nvl(:owner, user) and r_constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		for rec in cursor.fetchall():
			yield ForeignKey(rec.constraint_name, rec.owner, connection)
		# Normally there is an index for this primary key, but we ignore it, as for the purpose of :mod:`orasql` this index doesn't exist

	def iterreferences(self, connection=None):
		yield self.table(connection)

	def table(self, connection=None):
		"""
		Return the :class:`Table` :obj:`self` belongs to.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select decode(owner, user, null, owner) as owner, table_name from {}_constraints where constraint_type='P' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		return Table(rec.table_name, rec.owner, connection)


class Comment(Object):
	"""
	Models a column comment in the database.
	"""
	type = "comment"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		tcname = self.name.split(".")
		cursor.execute("select comments from {}_col_comments where owner=nvl(:owner, user) and table_name=:tname and column_name=:cname".format(cursor.ddprefix()), owner=self.owner, tname=tcname[0], cname=tcname[1])
		row = cursor.fetchone()
		if row is None:
			raise SQLObjectNotFoundError(self)

		name = self.getfullname()
		if row.comments:
			code = "comment on column {} is {}".format(name, formatstring(row.comments, latin1=True))
		else:
			code = "comment on column {} is ''".format(name)
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def dropddl(self, connection=None, term=True):
		# will be dropped with the table
		return ""

	def fixname(self, code):
		code = code.split(None, 5)
		code = "comment on column {} is {}".format(self.getfullname(), code[5])
		return code

	def cdate(self, connection=None):
		return None

	def udate(self, connection=None):
		return None

	def iterreferences(self, connection=None):
		connection = self.getconnection(connection)
		yield Table(self.name.split(".")[0], self.owner, connection)

	def iterreferencedby(self, connection=None):
		if False:
			yield None


class ForeignKey(Constraint):
	"""
	Models a foreign key constraint in the database.
	"""
	type = "fk"
	constraint_type = "R"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		# Add constraint_type to the query, so we don't pick up another constraint by accident
		cursor.execute("select decode(r_owner, user, null, r_owner) as r_owner, r_constraint_name, table_name from {}_constraints where constraint_type='R' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		cursor.execute("select column_name from {}_cons_columns where owner=nvl(:owner, user) and constraint_name=:name order by position".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		fields1 = ", ".join(r.column_name for r in cursor)
		cursor.execute("select table_name, column_name from {}_cons_columns where owner=nvl(:owner, user) and constraint_name=:name order by position".format(cursor.ddprefix()), owner=rec.r_owner, name=rec.r_constraint_name)
		fields2 = ", ".join("{}({})".format(getfullname(r.table_name, rec.r_owner), r.column_name) for r in cursor)
		tablename = getfullname(rec.table_name, self.owner)
		fkname = getfullname(self.name, None)
		code = "alter table {} add constraint {} foreign key ({}) references {}".format(tablename, fkname, fields1, fields2)
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def _ddl(self, connection, cmd, term):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select table_name from {}_constraints where owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		tablename = getfullname(rec.table_name, self.owner)
		fkname = getfullname(self.name, None)
		code = "alter table {} {} constraint {}".format(tablename, cmd, fkname)
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def dropddl(self, connection=None, term=True):
		return self._ddl(connection, "drop", term)

	def enableddl(self, connection=None, term=True):
		return self._ddl(connection, "enable", term)

	def disableddl(self, connection=None, term=True):
		return self._ddl(connection, "disable", term)

	def iterreferencedby(self, connection=None):
		# Shortcut: Nobody references a foreign key
		if False:
			yield None

	def iterreferences(self, connection=None):
		yield self.table(connection)
		yield self.pk(connection)

	def table(self, connection=None):
		"""
		Return the :class:`Table` :obj:`self` belongs to.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select table_name from {}_constraints where constraint_type='R' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		return Table(rec.table_name, self.owner, connection)

	def pk(self, connection=None):
		"""
		Return the primary key referenced by :obj:`self`.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select decode(r_owner, user, null, r_owner) as r_owner, r_constraint_name from {}_constraints where constraint_type='R' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		return PrimaryKey(rec.r_constraint_name, rec.r_owner, connection)

	def itercolumns(self, connection=None):
		"""
		Return an iterator over the columns this foreign key consists of.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select decode(owner, user, null, owner) as owner, table_name, column_name from {}_cons_columns where constraint_name=:name and owner=nvl(:owner, user) order by position".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		for r in cursor:
			yield Column("{}.{}".format(r.table_name, r.column_name), r.owner)

	def isenabled(self, connection=None):
		"""
		Return whether this constraint is enabled.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select status from {}_constraints where constraint_type='R' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		return rec[0] == "ENABLED"


class Index(MixinNormalDates, Object):
	"""
	Models an index in the database.
	"""
	type = "index"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		if self.isconstraint(connection):
			return ""
		cursor.execute("select index_name, table_name, uniqueness, index_type, ityp_owner, ityp_name, parameters from {}_indexes where owner=nvl(:owner, user) and index_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		tablename = getfullname(rec.table_name, self.owner)
		indexname = self.getfullname()
		if rec.uniqueness == "UNIQUE":
			unique = " unique"
		else:
			unique = ""
		cursor.execute("select aie.column_expression, aic.column_name from {0}_ind_columns aic, {0}_ind_expressions aie where aic.index_owner=aie.index_owner(+) and aic.index_name=aie.index_name(+) and aic.column_position=aie.column_position(+) and aic.index_owner=nvl(:owner, user) and aic.index_name=:name order by aic.column_position".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		code = "create{} index {} on {} ({})".format(unique, indexname, tablename, ", ".join(r.column_expression or r.column_name for r in cursor))
		if rec.index_type == "DOMAIN":
			if rec.parameters:
				parameters = " parameters ('{}')".format(rec.parameters.replace("'", "''"))
			else:
				parameters = ""
			code += " indextype is {}.{}{}".format(rec.ityp_owner, rec.ityp_name, parameters)
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def dropddl(self, connection=None, term=True):
		if self.isconstraint(connection):
			return ""
		code = "drop index {}".format(self.getfullname())
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	@classmethod
	def iternames(cls, connection, owner=ALL):
		# We skip those indexes that are generated by a constraint
		cursor = connection.cursor()
		if owner is None:
			cursor.execute("select null as owner, index_name from (select index_name from user_indexes where index_type not in ('LOB', 'IOT - TOP') minus select index_name from user_constraints where constraint_type in ('U', 'P') and owner=user) where index_name not like 'BIN$%' order by index_name")
		elif owner is ALL:
			cursor.execute("select decode(owner, user, null, owner) as owner, index_name from (select owner, index_name from {0}_indexes where index_type not in ('LOB', 'IOT - TOP') minus select index_owner, index_name from {0}_constraints where constraint_type in ('U', 'P')) where index_name not like 'BIN$%' order by owner, index_name".format(cursor.ddprefix()))
		else:
			cursor.execute("select decode(owner, user, null, owner) as owner, index_name from (select owner, index_name from {0}_indexes where index_type not in ('LOB', 'IOT - TOP') and owner = :owner minus select index_owner, index_name from {0}_constraints where constraint_type in ('U', 'P') and index_owner = :owner) where index_name not like 'BIN$%' order by owner, index_name".format(cursor.ddprefix()), owner=owner)
		return ((row.index_name, row.owner) for row in cursor)

	def fixname(self, code):
		if code.lower().startswith("create unique"):
			code = code.split(None, 5)
			code = "create unique index {} {}".format(self.getfullname(), code[5])
		else:
			code = code.split(None, 4)
			code = "create index {} {}".format(self.getfullname(), code[4])
		return code

	def constraint(self, connection=None):
		"""
		If this index is generated by a constraint, return the constraint
		otherwise return :const:`None`.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select constraint_type from {}_constraints where owner=nvl(:owner, user) and constraint_name=:name and constraint_type in ('U', 'P')".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is not None:
			rec = {"U": UniqueConstraint, "P": PrimaryKey}[rec.constraint_type](self.name, self.owner, connection)
		return rec

	def isconstraint(self, connection=None):
		"""
		Is this index generated by a constraint?
		"""
		return self.constraint(connection) is not None

	def iterreferences(self, connection=None):
		constraint = self.constraint(connection)
		# if self is generated by a constraint (i.e. ``constraint`` is not :const:`None`), we ignore all dependencies (such an index is never produced be :meth:`iterobjects`)
		if constraint is None:
			(connection, cursor) = self.getcursor(connection)
			# If this is a domain index, reference the preferences defined there
			cursor.execute("select index_type, parameters from {}_indexes where owner=nvl(:owner, user) and index_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
			rec = cursor.fetchone()
			if rec.index_type == "DOMAIN":
				parameters = re.split('\\b(datastore|memory|lexer|stoplist|wordlist)\\b', rec.parameters, flags=re.IGNORECASE)
				foundparameter = None
				for parameter in parameters:
					if foundparameter:
						if foundparameter.lower() in ("datastore", "lexer", "stoplist", "wordlist"):
							(prefowner, sep, prefname) = parameter.strip().partition(".")
							if sep:
								yield Preference(prefname.upper(), prefowner)
							else:
								yield Preference(prefowner.upper())
						foundparameter = None
					elif parameter.lower() in ("datastore", "lexer", "stoplist", "wordlist"):
						foundparameter = parameter

			yield from super().iterreferences(connection)

	def table(self, connection=None):
		"""
		Return the :class:`Table` :obj:`self` belongs to.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select table_name, decode(table_owner, user, null, table_owner) as table_owner from {}_indexes where owner=nvl(:owner, user) and index_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		return Table(rec.table_name, rec.table_owner, connection)


class UniqueConstraint(Constraint):
	"""
	Models a unique constraint in the database.
	"""
	type = "unique"
	constraint_type = "U"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		# Add constraint_type to the query, so we don't pick up another constraint by accident
		cursor.execute("select table_name from {}_constraints where constraint_type='U' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		tablename = getfullname(rec.table_name, self.owner)
		uniquename = getfullname(self.name, None)
		cursor.execute("select column_name from all_cons_columns where owner=nvl(:owner, user) and constraint_name=:name", owner=self.owner, name=self.name)
		code = "alter table {} add constraint {} unique({})".format(tablename, uniquename, ", ".join(r.column_name for r in cursor))
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def dropddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select table_name from {}_constraints where constraint_type='U' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		tablename = getfullname(rec.table_name, self.owner)
		uniquename = getfullname(self.name, None)
		code = "alter table {} drop constraint {}".format(tablename, uniquename)
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def iterreferencedby(self, connection=None):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select decode(owner, user, null, owner) as owner, constraint_name from {}_constraints where constraint_type='R' and r_owner=nvl(:owner, user) and r_constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		for rec in cursor.fetchall():
			yield ForeignKey(rec.constraint_name, rec.owner, connection)

		# Normally there is an index for this constraint, but we ignore it, as for the purpose of :mod:`orasql` this index doesn't exist

	def iterreferences(self, connection=None):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select decode(owner, user, null, owner) as owner, table_name from {}_constraints where constraint_type='U' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		for rec in cursor.fetchall():
			yield Table(rec.table_name, rec.owner, connection)

	def table(self, connection=None):
		"""
		Return the :class:`Table` :obj:`self` belongs to.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select table_name from {}_constraints where constraint_type='U' and owner=nvl(:owner, user) and constraint_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		return Table(rec.table_name, self.owner, connection)


class Synonym(Object):
	"""
	Models a synonym in the database.
	"""
	type = "synonym"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select table_owner, table_name, db_link from {}_synonyms where owner=nvl(:owner, user) and synonym_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		owner = self.owner
		if owner == "PUBLIC":
			public = "public "
			owner = None
		else:
			public = ""
		name = getfullname(self.name, owner)
		name2 = getfullname(rec.table_name, rec.table_owner)
		code = "create or replace {}synonym {} for {}".format(public, name, name2)
		if rec.db_link is not None:
			code += "@{}".format(rec.db_link)
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def dropddl(self, connection=None, term=True):
		owner = self.owner
		if owner == "PUBLIC":
			public = "public "
			owner = None
		else:
			public = ""
		name = getfullname(self.name, owner)
		code = "drop {}synonym {}".format(public, name)
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def fixname(self, code):
		if code.lower().startswith("create or replace public"):
			code = code.split(None, 6)
			code = "create or replace public synonym {} {}".format(self.getfullname(), code[6])
		else:
			code = code.split(None, 5)
			code = "create or replace synonym {} {}".format(self.getfullname(), code[5])
		return code

	def cdate(self, connection=None):
		return None

	def udate(self, connection=None):
		return None

	def iterreferences(self, connection=None, done=None):
		# Shortcut: a synonym doesn't depend on anything
		if False:
			yield None

	def getobject(self, connection=None):
		"""
		Get the object for which :obj:`self` is a synonym.
		"""
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select table_owner, table_name, db_link from {}_synonyms where owner=nvl(:owner, user) and synonym_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		return connection._getobject(rec.table_name, rec.table_owner)


class View(MixinNormalDates, Object):
	"""
	Models a view in the database.
	"""
	type = "view"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select text from {}_views where owner=nvl(:owner, user) and view_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		code = "\n".join(line.rstrip() for line in rec.text.strip().splitlines()) # Strip trailing whitespace
		code = "create or replace force view {} as\n\t{}".format(self.getfullname(), code)
		if term:
			code += "\n/\n"
		else:
			code += "\n"
		return code

	def dropddl(self, connection=None, term=True):
		code = "drop view {}".format(self.getfullname())
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def fixname(self, code):
		code = code.split(None, 6)
		code = "create or replace force view {} {}".format(self.getfullname(), code[6])
		return code

	def iterrecords(self, connection=None):
		(connection, cursor) = self.getcursor(connection)
		query = "select * from {}".format(self.getfullname())
		cursor.execute(query)
		return iter(cursor)


class MaterializedView(View):
	"""
	Models a meterialized view in the database.
	"""
	type = "materialized view"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select * from {}_mviews where owner=nvl(:owner, user) and mview_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		code = "\n".join(line.rstrip() for line in rec.query.strip().splitlines()) # Strip trailing whitespace
		code = "create materialized view {}\nrefresh {} on {} as\n\t{}".format(self.getfullname(), rec.refresh_method, rec.refresh_mode, code)
		if term:
			code += "\n/\n"
		else:
			code += "\n"
		return code

	def dropddl(self, connection=None, term=True):
		code = "drop materialized view {}".format(self.getfullname())
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def fixname(self, code):
		code = code.split(None, 4)
		code = "create materialized view {} {}".format(self.getfullname(), code[4])
		return code

	def iterreferences(self, connection=None):
		# skip the table
		for obj in super().iterreferences(connection):
			if not isinstance(obj, Table) or obj.name != self.name or obj.owner != self.owner:
				yield obj

	def iterreferencedby(self, connection=None):
		connection = self.getconnection(connection)
		yield Table(self.name, self.owner, connection)


class Library(Object):
	"""
	Models a library in the database.
	"""
	type = "library"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select file_spec from {}_libraries where owner=nvl(:owner, user) and library_name=:name".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		return "create or replace library {} as {!r}".format(self.getfullname(), rec.file_spec)
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def dropddl(self, connection=None, term=True):
		code = "drop library {}".format(self.getfullname())
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def fixname(self, code):
		code = code.split(None, 5)
		code = "create or replace library {} {}".format(self.getfullname(), code[5])
		return code


class Argument(object):
	"""
	:class:`Argument` objects hold information about the arguments of a
	stored procedure.
	"""
	def __init__(self, name, position, datatype, isin, isout):
		self.name = name
		self.position = position
		self.datatype = datatype
		self.isin = isin
		self.isout = isout

	def __repr__(self):
		return "<{}.{} name={!r} position={!r} datatype={!r} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.name, self.position, self.datatype, id(self))


class Callable(MixinNormalDates, MixinCodeDDL, Object):
	"""
	Models a callable object in the database, i.e. functions and procedures.
	"""

	_ora2cx = {
		"date": datetime.datetime,
		"timestamp": datetime.datetime,
		"timestamp with time zone": datetime.datetime,
		"number": float,
		"varchar2": str,
		"clob": CLOB,
		"blob": BLOB,
	}

	def __init__(self, name, owner=None, connection=None):
		Object.__init__(self, name, owner, connection)
		self._argsbypos = None
		self._argsbyname = None
		self._returnvalue = None

	def _calcargs(self, cursor):
		if self._argsbypos is None:
			if "." in self.name:
				(package_name, procedure_name) = self.name.split(".")
				cursor.execute("select object_name from {}_procedures where owner=nvl(:owner, user) and object_name=:package_name and procedure_name=:procedure_name".format(cursor.ddprefix()), owner=self.owner, package_name=package_name, procedure_name=procedure_name)
			else:
				package_name = None
				procedure_name = self.name
				cursor.execute("select object_name from {}_procedures where owner=nvl(:owner, user) and object_name=:name and procedure_name is null".format(cursor.ddprefix()), owner=self.owner, name=procedure_name)
			if cursor.fetchone() is None:
				raise SQLObjectNotFoundError(self)
			self._argsbypos = []
			self._argsbyname = {}
			if package_name is not None:
				cursor.execute("select lower(argument_name) as name, lower(in_out) as in_out, lower(data_type) as datatype from {}_arguments where owner=nvl(:owner, user) and package_name=:package_name and object_name=:procedure_name and data_level=0 order by sequence".format(cursor.ddprefixargs()), owner=self.owner, package_name=package_name, procedure_name=procedure_name)
			else:
				cursor.execute("select lower(argument_name) as name, lower(in_out) as in_out, lower(data_type) as datatype from {}_arguments where owner=nvl(:owner, user) and package_name is null and object_name=:procedure_name and data_level=0 order by sequence".format(cursor.ddprefixargs()), owner=self.owner, procedure_name=procedure_name)
			i = 0 # argument position (skip return value)
			for record in cursor:
				arginfo = Argument(record.name, i, record.datatype, "in" in record.in_out, "out" in record.in_out)
				if record.name is None: # this is the return value
					self._returnvalue = arginfo
				else:
					self._argsbypos.append(arginfo)
					self._argsbyname[arginfo.name] = arginfo
					i += 1

	def _getargs(self, cursor, *args, **kwargs):
		queryargs = {}

		if len(args) > len(self._argsbypos):
			raise TypeError("too many parameters for {!r}: {} given, {} expected".format(self, len(args), len(self._argsbypos)))

		# Handle positional arguments
		for (arg, arginfo) in zip(args, self._argsbypos):
			queryargs[arginfo.name] = self._wraparg(cursor, arginfo, arg)

		# Handle keyword arguments
		for (argname, arg) in kwargs.items():
			argname = argname.lower()
			if argname in queryargs:
				raise TypeError("duplicate argument for {!r}: {}".format(self, argname))
			try:
				arginfo = self._argsbyname[argname]
			except KeyError:
				raise TypeError("unknown parameter for {!r}: {}".format(self, argname))
			queryargs[arginfo.name] = self._wraparg(cursor, arginfo, arg)

		# Add out parameters for anything that hasn't been specified
		for arginfo in self._argsbypos:
			if arginfo.name not in queryargs and arginfo.isout:
				queryargs[arginfo.name] = self._wraparg(cursor, arginfo, None)

		return queryargs

	def _wraparg(self, cursor, arginfo, arg):
		try:
			if arg is None:
				t = self._ora2cx[arginfo.datatype]
			else:
				t = type(arg)
		except KeyError:
			raise TypeError("can't handle parameter {} of type {} with value {!r} in {!r}".format(arginfo.name, arginfo.datatype, arg, self))
		if isinstance(arg, bytes): # ``bytes`` is treated as binary data, always wrap it in a ``BLOB``
			t = BLOB
		elif isinstance(arg, str) and len(arg) >= 2000:
			t = CLOB
		var = cursor.var(t)
		var.setvalue(0, arg)
		return var

	def _unwraparg(self, arginfo, cursor, value):
		if isinstance(value, LOB):
			value = _decodelob(value, cursor.readlobs)
		return value

	def _makerecord(self, cursor, args):
		index2name = []
		values = []
		for arginfo in self._argsbypos:
			name = arginfo.name
			if name in args:
				index2name.append(name)
				values.append(self._unwraparg(arginfo, cursor, args[name].getvalue(0)))
		name2index = dict(zip(index2name, itertools.count()))
		return Record(index2name, name2index, values)

	def iterarguments(self, connection=None):
		"""
		Generator that yields all arguments of the function/procedure :obj:`self`.
		"""
		(connection, cursor) = self.getcursor(connection)
		self._calcargs(cursor)
		yield from self._argsbypos


class Procedure(Callable):
	"""
	Models a procedure in the database. A :class:`Procedure` object can be
	used as a wrapper for calling the procedure with keyword arguments.
	"""

	type = "procedure"

	def __call__(self, cursor, *args, **kwargs):
		"""
		Call the procedure with arguments :obj:`args` and keyword arguments
		:obj:`kwargs`. :obj:`cursor` must be a :mod:`ll.orasql` cursor. This will
		return a :class:`Record` object containing the result of the call (i.e.
		this record will contain all specified and all out parameters).
		"""
		self._calcargs(cursor)

		if self.owner is None:
			name = self.name
		else:
			name = "{}.{}".format(self.owner, self.name)

		queryargs = self._getargs(cursor, *args, **kwargs)

		query = "begin {}({}); end;".format(name, ", ".join("{0}=>:{0}".format(name) for name in queryargs))

		cursor.execute(query, queryargs)

		return self._makerecord(cursor, queryargs)


class Function(Callable):
	"""
	Models a function in the database. A :class:`Function` object can be
	used as a wrapper for calling the function with keyword arguments.
	"""
	type = "function"

	def __call__(self, cursor, *args, **kwargs):
		"""
		Call the function with arguments :obj:`args` and keyword arguments
		:obj:`kwargs`. :obj:`cursor` must be an :mod:`ll.orasql` cursor.
		This will return a tuple containing the result and a :class:`Record`
		object containing the modified parameters (i.e. this record will contain
		all specified and out parameters).
		"""
		self._calcargs(cursor)

		if self.owner is None:
			name = self.name
		else:
			name = "{}.{}".format(self.owner, self.name)

		queryargs = self._getargs(cursor, *args, **kwargs)

		returnvalue = "r"
		while returnvalue in queryargs:
			returnvalue += "_"
		queryargs[returnvalue] = self._wraparg(cursor, self._returnvalue, None)

		query = "begin :{} := {}({}); end;".format(returnvalue, name, ", ".join("{0}=>:{0}".format(name) for name in queryargs if name != returnvalue))

		cursor.execute(query, queryargs)

		returnvalue = self._unwraparg(self._returnvalue, cursor, queryargs.pop(returnvalue).getvalue(0))

		return (returnvalue, self._makerecord(cursor, queryargs))


class Package(MixinNormalDates, MixinCodeDDL, Object):
	"""
	Models a package in the database.
	"""
	type = "package"


class PackageBody(MixinNormalDates, MixinCodeDDL, Object):
	"""
	Models a package body in the database.
	"""
	type = "package body"


class Type(MixinNormalDates, MixinCodeDDL, Object):
	"""
	Models a type definition in the database.
	"""
	type = "type"


class Trigger(MixinNormalDates, MixinCodeDDL, Object):
	"""
	Models a trigger in the database.
	"""
	type = "trigger"


class JavaSource(MixinNormalDates, Object):
	"""
	Models Java source code in the database.
	"""
	type = "java source"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select text from {}_source where type='JAVA SOURCE' and owner=nvl(:owner, user) and name=:name order by line".format(cursor.ddprefix()), owner=self.owner, name=self.name)
		code = "\n".join((rec.text or "").rstrip() for rec in cursor)
		code = code.strip()

		code = "create or replace and compile java source named {} as\n{}\n".format(self.getfullname(), code)
		if term:
			code += "/\n"
		return code

	def dropddl(self, connection=None, term=True):
		code = "drop java source {}".format(self.getfullname())
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def fixname(self, code):
		code = code.split(None, 9)
		code = "create or replace and compile java source named {} {}".format(self.getfullname(), code[9])
		return code


class Privilege(object):
	"""
	Models a database object privilege (i.e. a grant).

	A :class:`Privilege` object has the following attributes:

		``privilege`` : string
			The type of the privilege (``EXECUTE`` etc.)

		``name`` : string
			The name of the object for which this privilege grants access

		``owner`` : string or :const:`None`
			the owner of the object

		``grantor`` : string or :const:`None`
			Who granted this privilege?

		``grantee`` : string or :const:`None`
			To whom has this privilege been granted?

		``connection`` : :class:`Connection` or :const:`None`
			The database connection
	"""

	type = "privilege"

	def __init__(self, privilege, name, grantor, grantee, owner=None, connection=None):
		self.privilege = privilege
		self.name = name
		self.grantor = grantor
		self.grantee = grantee
		self.owner = owner
		self.connection = connection

	def __repr__(self):
		if self.owner is not None:
			return "{}.{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__module__, self.__class__.__name__, self.privilege, self.name, self.grantee, self.owner)
		else:
			return "{}.{}({!r}, {!r}, {!r})".format(self.__class__.__module__, self.__class__.__name__, self.privilege, self.name, self.grantee)

	def __str__(self):
		if self.owner is not None:
			return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.privilege, self.name, self.grantee, self.owner)
		else:
			return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.privilege, self.name, self.grantee)

	def getconnection(self, connection):
		if connection is None:
			connection = self.connection
		if connection is None:
			raise TypeError("no connection available")
		return connection

	def getcursor(self, connection):
		connection = self.getconnection(connection)
		return (connection, connection.cursor())

	def getconnectstring(self):
		if self.connection:
			return self.connection.connectstring()
		return None
	connectstring = property(getconnectstring)

	@classmethod
	def iterobjects(cls, connection, owner=ALL):
		"""
		Generator that yields object privileges. For the meaning of :obj:`owner`
		see :meth:`Object.iternames`.
		"""
		cursor = connection.cursor() # can't use :meth:`getcursor` as we're in a classmethod

		if owner is None:
			cursor.execute("select null as owner, privilege, table_name as object, decode(grantor, user, null, grantor) as grantor, grantee from user_tab_privs where owner=user order by table_name, privilege")
		elif owner is ALL:
			ddprefix = cursor.ddprefix()
			# The column names in ``ALL_TAB_PRIVS`` and ``DBA_TAB_PRIVS`` are different, so we have to use two different queries
			if ddprefix == "all":
				cursor.execute("select decode(table_schema, user, null, table_schema) as owner, privilege, table_name as object, decode(grantor, user, null, grantor) as grantor, grantee from all_tab_privs order by table_name, privilege")
			else:
				cursor.execute("select decode(owner, user, null, owner) as owner, privilege, table_name as object, decode(grantor, user, null, grantor) as grantor, grantee from dba_tab_privs order by table_name, privilege")
		else:
			cursor.execute("select decode(table_schema, user, null, table_schema) as owner, privilege, table_name as object, decode(grantor, user, null, grantor) as grantor, grantee from {}_tab_privs where table_schema=:owner order by table_schema, table_name, privilege".format(cursor.ddprefix()), owner=owner)
		return (Privilege(rec.privilege, rec.object, rec.grantor, rec.grantee, rec.owner, connection) for rec in cursor)

	def grantddl(self, connection=None, term=True, mapgrantee=True):
		"""
		Return SQL code to grant this privilege. If :obj:`mapgrantee` is a list
		or a dictionary and ``self.grantee`` is not in this list (or dictionary)
		no command will be returned. If it's a dictionary and ``self.grantee`` is
		in it, the privilege will be granted to the user specified as the value
		instead of the original one. If :obj:`mapgrantee` is true (the default)
		the privilege will be granted to the original grantee.
		"""
		(connection, cursor) = self.getcursor(connection)
		if mapgrantee is True:
			grantee = self.grantee
		elif isinstance(mapgrantee, (list, tuple)):
			if self.grantee.lower() in (g.lower() for g in mapgrantee):
				grantee = self.grantee
			else:
				grantee = None
		else:
			mapgrantee = {key.lower(): value for (key, value) in mapgrantee.items()}
			grantee = mapgrantee.get(self.grantee.lower(), None)
		if grantee is None:
			return ""
		code = "grant {} on {} to {}".format(self.privilege, self.name, grantee)
		if term:
			code += ";\n"
		return code


class Column(Object):
	"""
	Models a single column of a table in the database. This is used to output
	``ALTER TABLE ...`` statements for adding, dropping and modifying columns.
	"""
	type = "column"

	def _getcolumnrecord(self, cursor):
		name = self.name.split(".")
		cursor.execute("select * from {}_tab_columns where owner=nvl(:owner, user) and table_name=:table_name and column_name=:column_name".format(cursor.ddprefix()), owner=self.owner, table_name=name[0], column_name=name[1])
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		return rec

	def addddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		rec = self._getcolumnrecord(cursor)
		name = self.name.split(".")
		code = ["alter table {} add {}".format(getfullname(name[0], self.owner), getfullname(name[1], None))]
		code.append(" {}".format(_columntype(rec)))
		default = _columndefault(rec)
		if default != "null":
			code.append(" default {}".format(default))
		if rec.nullable == "N":
			code.append(" not null")
		if term:
			code.append(";\n")
		else:
			code.append("\n")
		return "".join(code)

	def modifyddl(self, connection, cursorold, cursornew, term=True):
		(connection, cursor) = self.getcursor(connection)

		rec = self._getcolumnrecord(cursor)
		recold = self._getcolumnrecord(cursorold)
		recnew = self._getcolumnrecord(cursornew)

		name = self.name.split(".")

		code = ["alter table {} modify {}".format(getfullname(name[0], self.owner), getfullname(name[1], None))]
		# Has the type changed?
		if recold.data_precision != recnew.data_precision or recold.data_length != recnew.data_length or recold.data_scale != recnew.data_scale or recold.char_length != recnew.char_length or recold.data_type != recnew.data_type or recold.data_type_owner != recnew.data_type_owner:
			# Has only the size changed?
			if rec.data_type == recold.data_type == recnew.data_type and rec.data_type_owner == recold.data_type_owner == recnew.data_type_owner:
				try:
					data_precision = max(r.data_precision for r in (rec, recold, recnew) if r.data_precision is not None)
				except ValueError:
					data_precision = None
				try:
					data_scale = max(r.data_scale for r in (rec, recold, recnew) if r.data_scale is not None)
				except ValueError:
					data_scale = None
				try:
					char_length = max(r.char_length for r in (rec, recold, recnew) if r.char_length is not None)
				except ValueError:
					char_length = None
				code.append(" {}".format(_columntype(rec, data_precision=data_precision, data_scale=data_scale, char_length=char_length)))
			else: # The type has changed too
				if recnew.data_type != rec.data_type or recnew.data_type_owner != rec.data_type_owner:
					raise ConflictError(self, "data_type unmergeable")
				elif recnew.data_precision != rec.data_precision:
					raise ConflictError(self, "data_precision unmergeable")
				elif recnew.data_scale != rec.data_scale:
					raise ConflictError(self, "data_scale unmergeable")
				elif recnew.char_length != rec.char_length:
					raise ConflictError(self, "char_length unmergeable")
				code.append(" {}".format(_columntype(recnew)))

		# Has the default changed?
		default = _columndefault(rec)
		olddefault = _columndefault(recold)
		newdefault = _columndefault(recnew)
		if olddefault != newdefault:
			if newdefault != default:
				raise ConflictError(self, "default value unmergable")
			code.append(" default {}".format(newdefault))

		# Check nullability
		if recold.nullable != recnew.nullable:
			if recnew.nullable == "N":
				code.append(" not null")
			else:
				code.append(" null")

		if term:
			code.append(";\n")
		else:
			code.append("\n")

		return "".join(code)

	def dropddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		name = self.name.split(".")
		code = "alter table {} drop column {}".format(getfullname(name[0], self.owner), getfullname(name[1], None))
		if term:
			code += ";\n"
		else:
			code += "\n"
		return code

	def table(self):
		name = self.name.split(".")
		return Table(name[0], self.owner, self.connection)

	def cdate(self, connection=None):
		# The column creation date is the table creation date
		return self.table().cdate(connection)

	def udate(self, connection=None):
		# The column modification date is the table modification date
		return self.table().udate(connection)

	def iterreferences(self, connection=None):
		connection = self.getconnection(connection)
		name = self.name.split(".")
		yield Table(name[0], self.owner, connection)

	def iterreferencedby(self, connection=None):
		if False:
			yield None

	def datatype(self, connection=None):
		"""
		The SQL type of this column.
		"""
		(connection, cursor) = self.getcursor(connection)
		rec = self._getcolumnrecord(cursor)
		return _columntype(rec)

	def default(self, connection=None):
		"""
		The SQL default value for this column.
		"""
		(connection, cursor) = self.getcursor(connection)
		rec = self._getcolumnrecord(cursor)
		return _columndefault(rec)

	def nullable(self, connection=None):
		"""
		Is this column nullable?
		"""
		(connection, cursor) = self.getcursor(connection)
		rec = self._getcolumnrecord(cursor)
		return rec.nullable == "Y"

	def comment(self, connection=None):
		"""
		The comment for this column.
		"""
		name = self.name.split(".")
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select comments from {}_col_comments where owner=nvl(:owner, user) and table_name=:table_name and column_name=:column_name".format(cursor.ddprefix()), owner=self.owner, table_name=name[0], column_name=name[1])
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		return rec.comments or None


class User(object):
	"""
	Models a user in the database
	"""
	def __init__(self, name, connection=None):
		self.name = name
		self.connection = connection

	def __repr__(self):
		return "{}.{}({!r})".format(self.__class__.__module__, self.__class__.__name__, self.name)

	def __str__(self):
		return "{}({})".format(self.__class__.__name__, self.name)

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.name == other.name

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.__class__.__name__) ^ hash(self.name)

	@classmethod
	def iternames(cls, connection):
		"""
		Generator that yields the names of all users
		"""
		cursor = connection.cursor()
		cursor.execute("select username from {}_users order by username".format(cursor.ddprefix()))
		return (row.username for row in cursor)

	@classmethod
	def iterobjects(cls, connection):
		"""
		Generator that yields all user objects.
		"""
		return (cls(name[0], connection) for name in cls.iternames(connection))


class Preference(Object):
	"""
	Models a preference in the database.
	"""
	type = "preference"

	def createddl(self, connection=None, term=True):
		(connection, cursor) = self.getcursor(connection)
		cursor.execute("select pre_object from ctx_preferences where pre_owner=nvl(:owner, user) and pre_name=:name", owner=self.owner, name=self.name)
		rec = cursor.fetchone()
		if rec is None:
			raise SQLObjectNotFoundError(self)
		name = self.getfullname()
		code = ["begin\n"]
		code.append("\tctx_ddl.create_preference('{}', '{}');\n".format(name.replace("'", "''"), rec.pre_object.replace("'", "''")))
		cursor.execute("select prv_attribute, prv_value from ctx_preference_values where prv_owner=nvl(:owner, user) and prv_preference=:name", owner=self.owner, name=self.name)
		name = self.getfullname().replace("'", "''")
		for rec in cursor:
			code.append("\tctx_ddl.set_attribute('{}', '{}', '{}');\n".format(name, rec.prv_attribute.replace("'", "''"), rec.prv_value.replace("'", "''")))
		code.append("end;\n")
		code = "".join(code)
		if term:
			code += "/\n"
		return code

	def dropddl(self, connection=None, term=True):
		name = self.getfullname()
		code = "begin\n\tctx_ddl.drop_preference('{}');\nend;\n".format(name.replace("'", "''"))
		if term:
			code += "/\n"
		return code

	def cdate(self, connection=None):
		return None

	def udate(self, connection=None):
		return None

	def iterreferencedby(self, connection=None):
		# FIXME: Parse the parameters of all domain indexes and output those indexes here that reference us in any of their parameters
		if False:
			yield None

	def iterreferences(self, connection=None, done=None):
		if False:
			yield None

	@classmethod
	def iternames(cls, connection, owner=ALL):
		"""
		Generator that yields the names of all preferences.
		"""
		cursor = connection.cursor()
		try:
			if owner is None:
				cursor.execute("select null as owner, pre_name from ctx_preferences where pre_owner=user order by pre_name")
			elif owner is ALL:
				cursor.execute("select pre_owner as owner, pre_name from ctx_preferences order by pre_owner, pre_name")
			else:
				cursor.execute("select decode(pre_owner, user, null, pre_owner) as owner, pre_name from ctx_preferences where pre_owner=:owner order by pre_name", owner=owner)
		except DatabaseError as exc:
			if exc.args[0].code == 942: # ORA-00942: table or view does not exist
				return iter(())
			else:
				raise
		else:
			return ((row.pre_name, row.owner) for row in cursor)

	@classmethod
	def iterobjects(cls, connection, owner=ALL):
		"""
		Generator that yields all preferences.
		"""
		return (cls(name[0], name[1], connection) for name in cls.iternames(connection, owner=owner))


###
### Classes that add an ``oracle`` scheme to the urls supported by :mod:`ll.url`.
###

class OracleConnection(url_.Connection):
	def __init__(self, context, connection, mode):
		self.dbconnection = connect(connection, mode=mode) if mode is not None else connect(connection)

	def open(self, url, mode="rb"):
		return OracleFileResource(self, url, mode)

	def close(self):
		self.dbconnection.close()

	def _type(self, url):
		path = url.path
		if path and not path[-1]:
			path = path[:-1]
		lp = len(path)
		if lp == 0:
			return "root"
		elif lp == 1:
			if path[0] == "user":
				return "allusers"
			else:
				return "type"
		elif lp == 2:
			if path[0] == "user":
				return "user"
			else:
				return "object"
		elif lp == 3:
			if path[0] == "user":
				return "usertype"
			else:
				raise ValueError("can't happen")
		elif lp == 4:
			if path[0] == "user":
				return "userobject"
			else:
				raise ValueError("can't happen")

	def _infofromurl(self, url):
		type = self._type(url)
		if type == "root":
			owner = None
			objectype = None
			name = None
		elif type == "allusers":
			owner = None
			objectype = None
			name = None
		elif type == "type":
			owner = None
			objectype = None
			name = None
		elif type == "user":
			owner = url.path[1]
			objectype = None
			name = None
		elif type == "object":
			owner = None
			objectype = url.path[0]
			name = url.path[1]
		elif type == "usertype":
			owner = url.path[1]
			objectype = url.path[2]
			name = None
		else:
			owner = url.path[1]
			objectype = url.path[2]
			name = url.path[3]
		if name is not None:
			if name.lower().endswith(".sql"):
				name = name[:-4]
			name = unicodedata.normalize('NFC', name)
		return (type, owner, objectype, name)

	def _objectfromurl(self, url):
		(type, owner, objecttype, name) = self._infofromurl(url)
		if objecttype not in Object.name2type:
			raise ValueError("don't know how to handle {0!r}".format(url))
		return Object.name2type[objecttype](name, owner)

	def isdir(self, url):
		return not self._type(url).endswith("object")

	def isfile(self, url):
		return self._type(url).endswith("object")

	def mimetype(self, url):
		if self.isdir(url):
			return "application/octet-stream"
		return "text/x-oracle-{}".format(url.path[0 if url.path[0] != "user" else 2])

	def owner(self, url):
		if len(url.path) >= 2 and url.path[0] == "user" and url.path[1]:
			return url.path[1]
		else:
			c = self.dbconnection.cursor()
			c.execute("select user from dual")
			return c.fetchone()[0]

	def cdate(self, url):
		if self.isdir(url):
			return bigbang
		try:
			obj = self._objectfromurl(url)
		except SQLNoSuchObjectError:
			raise IOError(errno.ENOENT, "no such file: {}".format(type, url))
		return obj.cdate(self.dbconnection)

	def mdate(self, url):
		if self.isdir(url):
			return bigbang
		try:
			obj = self._objectfromurl(url)
		except SQLNoSuchObjectError:
			raise IOError(errno.ENOENT, "no such file: {}".format(type, url))
		return obj.udate(self.dbconnection)

	def _listdir(self, url, pattern=None, files=True, dirs=True):
		result = []
		type = self._type(url)
		if type == "root": # directory of types for the current user
			if dirs:
				result = [url_.URL(name + "/") for name in Object.name2type]
		elif type == "type": # directory of objects of the specified type for current user
			if files:
				path = url.path
				type = path[0]
				names = (name[0] for name in Object.name2type[type].iternames(self.dbconnection, None))
				if len(path) == 1:
					result = [url_.URL("{}/{}.sql".format(type, makeurl(name))) for name in names]
				else:
					result = [url_.URL("{}.sql".format(makeurl(name))) for name in names]
		elif type == "allusers": # directory of all users
			if dirs:
				path = url.path
				names = User.iternames(self.dbconnection)
				if len(path) == 1:
					result = [url_.URL("user/{}/".format(makeurl(name))) for name in names]
				else:
					result = [url_.URL("{}/".format(makeurl(name))) for name in names]
		elif type == "user": # directory of types for a specific user
			if dirs:
				path = url.path
				if len(path) == 2:
					result = [url_.URL("{}/{}/".format(path[1], name)) for name in Object.name2type]
				else:
					result = [url_.URL("{}/".format(name)) for name in Object.name2type]
		elif type == "usertype": # directory of objects of the specified type for a specific user
			if files:
				path = url.path
				type = path[2]
				names = (name[0] for name in Object.name2type[type].iternames(self.dbconnection, path[1]))
				if len(path) == 3:
					result = [url_.URL("{}/{}.sql".format(type, makeurl(name))) for name in names]
				else:
					result = [url_.URL("{}.sql".format(makeurl(name))) for name in names]
		else:
			raise IOError(errno.ENOTDIR, "Not a directory: {}".format(url))
		if pattern is not None:
			pattern = pattern.lower()
			result = [u for u in result if fnmatch.fnmatch(str(u).lower(), pattern)]
		return result

	def listdir(self, url, pattern=None):
		return self._listdir(url, pattern, True, True)

	def files(self, url, pattern=None):
		return self._listdir(url, pattern, True, False)

	def dirs(self, url, pattern=None):
		return self._listdir(url, pattern, False, True)

	def __repr__(self):
		return "<{}.{} to {!r} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.connection.connectstring(), id(self))


class OracleFileResource(url_.Resource):
	"""
	An :class:`OracleFileResource` wraps an Oracle database object (like a
	table, view, function, procedure etc.) in a file-like API.
	"""
	def __init__(self, connection, url, mode="r"):
		self.connection = connection
		self.url = url
		self.mode = mode
		self.closed = False
		self.name = str(self.url)

		if "w" in self.mode:
			if "b" in self.mode:
				self.stream = io.BytesIO()
			else:
				self.stream = io.StringIO()
		else:
			code = self.connection._objectfromurl(url).createddl(self.connection.dbconnection, term=False)
			if "b" in self.mode:
				code = code.encode("utf-8")
				self.stream = io.BytesIO(code)
			else:
				self.stream = io.StringIO(code)

	def read(self, size=-1):
		if self.closed:
			raise ValueError("I/O operation on closed file")
		return self.stream.read(size)

	def write(self, data):
		if self.closed:
			raise ValueError("I/O operation on closed file")
		return self.stream.write(data)

	def mimetype(self):
		return self.connection.mimetype(self.url)

	def cdate(self):
		return self.connection.cdate(self.url)

	def mdate(self):
		return self.connection.mdate(self.url)

	def close(self):
		if not self.closed:
			if "w" in self.mode:
				obj = self.connection._objectfromurl(self.url)
				code = self.stream.getvalue()
				if isinstance(code, bytes):
					code = code.decode("utf-8")
				code = obj.fixname(code)
				cursor = self.connection.dbconnection.cursor()
				cursor.execute(code)
			self.stream = None
			self.closed = True


class OracleSchemeDefinition(url_.SchemeDefinition):
	def _connect(self, url, context=None, **kwargs):
		context = url_.getcontext(context)
		# Use one :class:`OracleConnection` for each ``user@host`` combination
		server = url.server
		try:
			connections = context.schemes["oracle"]
		except KeyError:
			connections = context.schemes["oracle"] = {}
		try:
			connection = connections[server]
		except KeyError:
			userinfo = url.userinfo.split(":")
			lui = len(userinfo)
			if lui == 2:
				mode = None
			elif lui == 3:
				try:
					mode = dict(sysoper=SYSOPER, sysdba=SYSDBA, normal=None)[userinfo[2]]
				except KeyError:
					raise ValueError("unknown connect mode {!r}".format(userinfo[2]))
			else:
				raise ValueError("illegal userinfo {!r}".format(url.userinfo))
			connection = connections[server] = OracleConnection(context, "{}/{}@{}".format(userinfo[0], userinfo[1], url.host), mode)
		return (connection, kwargs)

	def open(self, url, mode="rb", context=None):
		(connection, kwargs) = self._connect(url, context)
		return OracleFileResource(connection, url, mode, **kwargs)

	def closeall(self, context):
		for connection in context.schemes["oracle"].values():
			connection.close()


url_.schemereg["oracle"] = OracleSchemeDefinition("oracle", usehierarchy=True, useserver=True, usefrag=False, islocal=False, isremote=True)
