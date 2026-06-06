#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2016-2026 by LivingLogic AG, Bayreuth/Germany
##
## All Rights Reserved

from __future__ import annotations
from urllib.request import install_opener

"""
Normally an object-relational mapper consist of:

1.	An infrastructure for specifying which records to fetch from the database.
	This can be as simple as specifying a primary key value, or as complex as
	a complete query language.
2. A way of mapping those records to objects and fields to attributes.

vSQL provides the first part only. vSQL does this by using a subset of
UL4 expressions retargeted for generating SQL expressions used in SQL queries.
So the end result of using vSQL always is a SQL query that you can execute
normally.

Currently only Oracle is supported.

The purpose of vSQL is not to abstract away differences between the relational
database and the object oriented world or to shield the developer from having
to deal with SQL or from handling the result of database queries.

Instead vSQL provides a safe query language that can be used to provided a
publicly accessible interface to database content. This eliminates the risky
parts of query construction, effectively preventing SQL injection attacks,
while offering the expressive power of an ORM without the overhead.


Example
-------

To create an SQL query via vSQL expressions in the simplest form we're using the
class :class:`Query` like this::

	from ll import vsql
	q = vsql.Query()

	# Define the expression we want
	q.select_vsql("('foo'.upper() + 'bar'.lower())[:3]")
	q.select_vsql("now() + years(3)")

	# Output the SQL query
	print(q.sqlsource())

this outputs:

.. sourcecode:: sql

	select
		vsqlimpl_pkg.slice_str((upper('foo') || lower('bar')), null, 3) /* ('foo'.upper() + 'bar'.lower())[:3] */,
		vsqlimpl_pkg.add_datetime_months(sysdate, (12 * 3)) /* now() + years(3) */
	from
		dual


Selecting from tables
---------------------

If you want to select records from a table, the :class:`Query` object needs to
know about the structure of the table, and needs a variable that can be used
to refer to records of that table. If the table looks like this:

.. sourcecode:: sql

	create table person
	(
		per_id integer,
		per_firstname varchar2(100),
		per_lastname varchar2(100),
		per_birthday date
	);

the table definition for vSQL can be defined like this::

	person_table = vsql.Group("person")
	person_table.add_field("id", vsql.DataType.INT, "{a}.per_id")
	person_table.add_field("firstname", vsql.DataType.STR, "{a}.per_firstname")
	person_table.add_field("lastname", vsql.DataType.STR, "{a}.per_lastname")
	person_table.add_field("birthday", vsql.DataType.DATE, "{a}.per_birthday")

Selecting from this table then works like this::

	from ll import vsql

	person_table = vsql.Group("person")
	person_table.add_field("id", vsql.DataType.INT, "{a}.per_id")
	person_table.add_field("firstname", vsql.DataType.STR, "{a}.per_firstname")
	person_table.add_field("lastname", vsql.DataType.STR, "{a}.per_lastname")
	person_table.add_field("birthday", vsql.DataType.DATE, "{a}.per_birthday")

	q = vsql.Query(
		p=vsql.Field("p", vsql.DataType.INT, refgroup=person_table)
	)

	# We want to force the query to select from `person`,
	# even if we don't select any fields
	q.from_vsql("p")

	# Specify which fields we want returned
	q.select_vsql("p.firstname + ' ' + p.lastname")
	q.select_vsql("p.birthday")

	# Return anly people born 1990 or later
	q.where_vsql("p.birthday > @(1990-01-01)")

	# Youngest first
	q.orderby_vsql("p.birthday", "desc")

	# Output the SQL query
	print(q.sqlsource())

this outputs:

.. sourcecode:: sql

	select
		((t1.per_firstname /* p.firstname */ || ' ') || t1.per_lastname /* p.lastname */) /* p.firstname + ' ' + p.lastname */,
		t1.per_birthday /* p.birthday */
	from
		person t1 /* p */
	where
		decode(vsqlimpl_pkg.cmp_datetime_datetime(t1.per_birthday /* p.birthday */, to_date('1990-01-01', 'YYYY-MM-DD')), 1, 1, null, null, 0) = 1 /* p.birthday > @(1990-01-01) */
	order by
		t1.per_birthday /* p.birthday */ desc


Using foreign key references
----------------------------

When you have foreign key fields that reference other tables,
you can use them too. When we assume that our table ``person``
looks like this:

.. sourcecode:: sql

	create table person
	(
		per_id integer,
		per_firstname varchar2(100),
		per_lastname varchar2(100),
		per_birthday date,
		com_id integer
	);

with the new field ``com_id`` referencing the table ``company``
that looks like this:

.. sourcecode:: sql

	create table company
	(
		com_id integer,
		com_name varchar2(100)
	);

then we can define the table structure and query connected fields,
as the following code demonstrates::

	from ll import vsql

	company_table = vsql.Group("company")
	company_table.add_field("id", vsql.DataType.INT, "{a}.com_id")
	company_table.add_field("name", vsql.DataType.STR, "{a}.com_name")

	person_table = vsql.Group("person")
	person_table.add_field("id", vsql.DataType.INT, "{a}.per_id")
	person_table.add_field("firstname", vsql.DataType.STR, "{a}.per_firstname")
	person_table.add_field("lastname", vsql.DataType.STR, "{a}.per_lastname")
	person_table.add_field("birthday", vsql.DataType.DATE, "{a}.per_birthday")
	person_table.add_field("company", vsql.DataType.INT, "{a}.com_id", "{m}.com_id = {d}.com_id", company_table)

	q = vsql.Query(
		p=vsql.Field("p", vsql.DataType.INT, refgroup=person_table)
	)

	# We want to force the query to select from `person`,
	# even if we don't select any fields
	q.from_vsql("p")

	# Specify which fields we want returned
	q.select_vsql("p.firstname + ' ' + p.lastname")
	q.select_vsql("p.birthday")
	q.select_vsql("p.company.name")

	# Return anly people born 1990 or later
	q.where_vsql("p.birthday > @(1990-01-01)")

	# Youngest first
	q.orderby_vsql("p.birthday", "desc")

	# Output the SQL query
	print(q.sqlsource())

This outputs:

.. sourcecode:: sql

	select
		((t1.per_firstname /* p.firstname */ || ' ') || t1.per_lastname /* p.lastname */) /* p.firstname + ' ' + p.lastname */,
		t1.per_birthday /* p.birthday */,
		t2.com_name /* p.company.name */
	from
		person t1 /* p */,
		company t2 /* p.company */
	where
		t1.com_id = t2.com_id /* p.company */ and
		decode(vsqlimpl_pkg.cmp_datetime_datetime(t1.per_birthday /* p.birthday */, to_date('1990-01-01', 'YYYY-MM-DD')), 1, 1, null, null, 0) = 1 /* p.birthday > @(1990-01-01) */
	order by
		t1.per_birthday /* p.birthday */ desc


vSQL standard library
---------------------

Many vSQL operations can not be converted to simple SQL expressions.
For these vSQL uses an Oracle package ``vsqlimpl_pkg`` that contains
the "vSQL standard library". This packages is available from Github at
https://github.com/LivingLogic/LivingLogic.Oracle.ul4


Module content
--------------
"""

import sys, datetime, itertools, re, pathlib, abc
from string import templatelib

from ll import color, misc, ul4c, ul4on

try:
	from ll import orasql
except ImportError:
	orasql = None

###
### Typing stuff
###

from typing import *

T_sql = str | templatelib.Template


###
### Global configurations
###

scriptname = misc.sysinfo.short_script_name


###
### Fields for the table ``VSQLRULE``
###

fields = dict(
	vr_nodetype=str,
	vr_value=str | None,
	vr_result=str,
	vr_signature=str | None,
	vr_arity=int,
	vr_literal1=str | None,
	vr_child2=int | None,
	vr_literal3=str | None,
	vr_child4=int | None,
	vr_literal5=str | None,
	vr_child6=int | None,
	vr_literal7=str | None,
	vr_child8=int | None,
	vr_literal9=str | None,
	vr_child10=int | None,
	vr_literal11=str | None,
	vr_child12=int | None,
	vr_literal13=str | None,
	vr_cname=str,
	vr_cdate=datetime.datetime,
)


###
### Helper functions and classes
###


class sqlliteral(str):
	"""
	Internal marker class that can be used to specify that its value should be
	treated as literal SQL.
	"""
	pass


def sql(value:Any) -> templatelib.Template:
	"""
	Return an SQL expression for the Python value ``value``.
	"""
	if value is None:
		return t"null"
	elif isinstance(value, sqlliteral):
		return templatelib.Template(str(value))
	elif isinstance(value, int):
		return templatelib.Template(str(value))
	elif isinstance(value, datetime.datetime):
		return templatelib.Template(f"to_date('{value:%Y-%m-%d %H:%M:%S}', 'YYYY-MM-DD HH24:MI:SS')")
	elif isinstance(value, str):
		if value:
			value = value.replace("'", "''")
			return templatelib.Template(f"'{value}'")
		else:
			return t"null"
	else:
		raise TypeError(f"unknown type {type(value)!r}")


def format_comment(comment:str | None) -> str:
	if comment is not None:
		comment = f"/* {comment.replace('/*', '/ *').replace('*/', '* /')} */"
	return comment


def add_comment(sqlsource: templatelib.Template, comment:str | None) -> templatelib.Template:
	"""
	Append the comment `comment` to the template `sqlsource`.

	If `sqlsource` already ends in the comment, it is not added again.

	I.e. ``add_comment(t"bar", "foo")`` returns ``t"bar /* foo */"``.
	"""
	if comment is not None:
		comment = format_comment(comment)

		if not sqlsource.strings[-1].endswith(comment):
			sqlsource = t"{sqlsource:l} {comment:l}"
	return sqlsource


def flatten_tstring(template: templatelib.Template) -> templatelib.Template:
	"""
	Recursively inline nested t-strings into a single flat t-string.

	For an interpolation that has no conversion and the format spec ``"l"``, its
	value is inlined into the result depending on its type:

	*	if the value is a :class:`!templatelib.Template`, its parts replace the
		interpolation in the result;

	*	if the value is :const:`None`, the interpolation is dropped (i.e. it
		contributes nothing);

	*	otherwise (a :class:`str` or any other value) the value is embedded
		directly as a literal string.

	All other parts (literal strings and non literal interpolations) are kept
	unchanged.

	I.e. ``flatten_tstring(t"a{t'b{c}d':l}e")`` returns ``t"ab{c}de"``.
	"""
	def parts(template):
		for part in template:
			if isinstance(part, str):
				yield part
			elif part.conversion is None and part.format_spec == "l":
				if isinstance(part.value, templatelib.Template):
					yield from parts(part.value)
				elif part.value is not None:
					yield str(part.value)
			else:
				yield part

	return templatelib.Template(*parts(template))


def to_tstring(obj: T_sql | None) -> templatelib.Template | None:
	"""
	Convert ``obj`` to a flattened t-string.

	``None`` is returned unchanged, a :class:`str` is wrapped in a
	:class:`!templatelib.Template`, and an existing t-string is flattened via
	:func:`flatten_tstring`.
	"""

	if obj is None:
		return None
	elif isinstance(obj, str):
		return templatelib.Template(obj)
	else:
		return flatten_tstring(obj)


def tstring_replace(obj: T_sql, search:str, replace:str):
	"""
	Replace all occurrences of ``search`` with ``replace`` in the literal string
	parts of the t-string ``obj``.

	Only the literal string parts are modified; interpolations are kept
	unchanged. A new :class:`!templatelib.Template` with the replaced parts is
	returned.

	I.e. ``tstring_replace(t"a{b}a", "a", "x")`` returns ``t"x{b}x"``.
	"""
	return templatelib.Template(*(p.replace(search, replace) if isinstance(p, str) else p for p in obj))


class TStringHasher:
	def __init__(self, template: templatelib.Template):
		self.template = flatten_tstring(template)

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False
		if self.template.strings != other.template.strings:
			return False
		for (selfi, otheri) in zip(self.template.interpolations, other.template.interpolations):
			if selfi.conversion != otheri.conversion:
				return False
			if selfi.format_spec != otheri.format_spec:
				return False
			if selfi.value != otheri.value:
				return False
		return True

	def __hash__(self):
		h = hash(self.template.strings)
		for i in self.template.interpolations:
			h ^= hash(i.conversion)
			h ^= hash(i.format_spec)
			h ^= hash(i.value)
		return h


class Repr:
	"""
	Base class that provides functionality for implementing :meth:`__repr__`
	and :meth:`_repr_pretty_` (used by IPython).
	"""

	_ll_repr_attrs_ = []

	def _ll_repr_prefix_(self) -> str:
		"""
		Return the initial part of the :meth:`__repr__` and :meth:`_repr_pretty_`
		output (without the initial ``"<"``).
		"""
		return f"{self.__class__.__module__}.{self.__class__.__qualname__}"

	def _ll_repr_suffix_(self) -> str:
		"""
		Return the final part of the :meth:`__repr__` and :meth:`_repr_pretty_`
		output (without the final ``">"``).
		"""
		return f"at {id(self):#x}"

	def __repr__(self) -> str:
		parts = itertools.chain(
			(f"<{self._ll_repr_prefix_()}",),
			self._ll_repr_(),
			(f"{self._ll_repr_suffix_()}>",),
		)
		return " ".join(parts)

	def _ll_repr_(self) -> Generator[str, None, None]:
		"""
		Each string produced by :meth:`!_ll_repr__` will be part of the
		:meth:`__repr__` output (joined by spaces).

		By default this outputs all non-``None`` attributes whose
		value is in the class attribute ``_ll_repr_attrs_``
		"""
		for cls in reversed(self.__class__.__mro__):
			for name in getattr(cls, "_ll_repr_attrs_", ()):
				value = getattr(self, name)
				if value is not None:
					yield f"{name}={value!r}"

	def _repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter", cycle:bool) -> None:
		if cycle:
			p.text(f"{self._ll_repr_prefix_()} ... {self._ll_repr_suffix_()}>")
		else:
			with p.group(3, f"<{self._ll_repr_prefix_()}", ">"):
				self._ll_repr_pretty_(p)
				p.breakable()
				p.text(self._ll_repr_suffix_())

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		"""
		Implement the body of the :meth:`_repr_pretty_` method.

		This means that the cycle detection and :meth:`group` call have already
		been done.

		By default this outputs all non-``None`` attributes whose
		value is in the class attribute ``_ll_repr_attrs_``
		"""
		for cls in reversed(self.__class__.__mro__):
			for name in getattr(cls, "_ll_repr_attrs_", {}):
				value = getattr(self, name)
				if value is not None:
					p.breakable()
					p.text(f"{name}=")
					p.pretty(value)


class Aggregate(misc.Enum):
	"""
	Aggregation methods.
	"""

	GROUP = "group"
	COUNT = "count"
	MIN = "min"
	MAX = "max"
	SUM = "sum"


class DataType(misc.Enum):
	"""
	The datatypes supported in vSQL expressions.
	"""

	NULL = ("null", )
	BOOL = ("bool", Aggregate.GROUP, Aggregate.MIN, Aggregate.MAX, Aggregate.SUM)
	INT = ("int", Aggregate.GROUP, Aggregate.MIN, Aggregate.MAX, Aggregate.SUM)
	NUMBER = ("number", Aggregate.GROUP, Aggregate.MIN, Aggregate.MAX, Aggregate.SUM)
	STR = ("str", Aggregate.GROUP, Aggregate.MIN, Aggregate.MAX)
	CLOB = ("clob", )
	COLOR = ("color", Aggregate.GROUP)
	GEO = ("geo", )
	DATE = ("date", Aggregate.GROUP, Aggregate.MIN, Aggregate.MAX)
	DATETIME = ("datetime", Aggregate.GROUP, Aggregate.MIN, Aggregate.MAX)
	DATEDELTA = ("datedelta", Aggregate.GROUP, Aggregate.MIN, Aggregate.MAX, Aggregate.SUM)
	DATETIMEDELTA = ("datetimedelta", Aggregate.GROUP, Aggregate.MIN, Aggregate.MAX, Aggregate.SUM)
	MONTHDELTA = ("monthdelta", Aggregate.GROUP, Aggregate.MIN, Aggregate.MAX, Aggregate.SUM)
	NULLLIST = ("nulllist", )
	INTLIST = ("intlist", )
	NUMBERLIST = ("numberlist", )
	STRLIST = ("strlist", )
	CLOBLIST = ("cloblist", )
	DATELIST = ("datelist", )
	DATETIMELIST = ("datetimelist", )
	NULLSET = ("nullset", )
	INTSET = ("intset", )
	NUMBERSET = ("numberset", )
	STRSET = ("strset", )
	DATESET = ("dateset", )
	DATETIMESET = ("datetimeset", )

	def __init__(self, value:str, *aggregates):
		misc.Enum.__init__(self)
		self._value_ = value
		self.aggregates = aggregates

	@classmethod
	def compatible_to(cls, given:DataType, required:DataType) -> Error | None:
		"""
		Check whether the type ``given`` is compatible to ``required``.

		If ``required`` is ``None`` every ``given`` type is accepted. Otherwise
		the types must be compatible (for example ``DataType.INT`` is compatible
		to ``DataType.NUMBER``, but not the other way around). Every type is
		compatible to itself.

		If ``given`` is not compatible to ``required`` the appropriate error value
		is returned, otherwise ``None`` is returned.
		"""
		# If we have no requirement for the datatype the given one is OK.
		if required is None:
			return None
		# ``NULL`` is compatible with everything
		elif given is DataType.NULL:
			return None
		# perfect match
		elif given is required:
			return None
		# some type of string
		elif required in {DataType.STR, DataType.CLOB} and given in {DataType.STR, DataType.CLOB}:
			return None
		# bool and int can be used for numbers
		elif required is DataType.NUMBER and given in {DataType.BOOL, DataType.INT, DataType.NUMBER}:
			return None
		# bool can be used for ints
		elif required is DataType.INT and given in {DataType.BOOL, DataType.INT}:
			return None
		# intlist can be used for numberlist
		elif required is DataType.NUMBERLIST and given in {DataType.INTLIST, DataType.NUMBERLIST}:
			return None
		# datelist can be used for datetimelist
		elif required is DataType.DATELIST and given in {DataType.INTLIST, DataType.DATETIMELIST}:
			return None
		# intset can be used for numberset
		elif required is DataType.NUMBERSET and given in {DataType.INTSET, DataType.NUMBERSET}:
			return None
		# dateset can be used for datetimeset
		elif required is DataType.DATESET and given in {DataType.INTSET, DataType.DATETIMESET}:
			return None
		# nulllist can be used as any list
		elif required in {DataType.INTLIST, DataType.NUMBERLIST, DataType.STRLIST, DataType.CLOBLIST, DataType.DATELIST, DataType.DATETIMELIST} and given is DataType.NULLLIST:
			return None
		# nullset can be used as any set
		elif required in {DataType.INTSET, DataType.NUMBERSET, DataType.STRSET, DataType.DATESET, DataType.DATETIMESET} and given is DataType.NULSET:
			return None
		else:
			return Error[f"DATATYPE_{required.name}"]

DataType.__doc__ += f"""
Possible values are:

{"".join(f"\t- ``{dt.name}``\n" for dt in DataType)}
"""

class NodeType(misc.Enum):
	"""
	The different types of vSQL abstract syntax tree nodes.

	This corresponds to the different subclasses of :class:`AST`.
	"""

	FIELD = "field"
	CONST_NONE = "const_none"
	CONST_BOOL = "const_bool"
	CONST_INT = "const_int"
	CONST_NUMBER = "const_number"
	CONST_STR = "const_str"
	CONST_CLOB = "const_clob"
	CONST_DATE = "const_date"
	CONST_DATETIME = "const_datetime"
	CONST_TIMESTAMP = "const_timestamp"
	CONST_COLOR = "const_color"
	LIST = "list"
	SET = "set"
	CMP_EQ = "cmp_eq"
	CMP_NE = "cmp_ne"
	CMP_LT = "cmp_lt"
	CMP_LE = "cmp_le"
	CMP_GT = "cmp_gt"
	CMP_GE = "cmp_ge"
	BINOP_ADD = "binop_add"
	BINOP_MUL = "binop_mul"
	BINOP_SUB = "binop_sub"
	BINOP_FLOORDIV = "binop_floordiv"
	BINOP_TRUEDIV = "binop_truediv"
	BINOP_MOD = "binop_mod"
	BINOP_AND = "binop_and"
	BINOP_OR = "binop_or"
	BINOP_CONTAINS = "binop_contains"
	BINOP_NOTCONTAINS = "binop_notcontains"
	BINOP_IS = "binop_is"
	BINOP_ISNOT = "binop_isnot"
	BINOP_ITEM = "binop_item"
	BINOP_SHIFTLEFT = "binop_shiftleft"
	BINOP_SHIFTRIGHT = "binop_shiftright"
	BINOP_BITAND = "binop_bitand"
	BINOP_BITOR = "binop_bitor"
	BINOP_BITXOR = "binop_bitxor"
	TERNOP_SLICE = "ternop_slice"
	UNOP_NOT = "unop_not"
	UNOP_NEG = "unop_neg"
	UNOP_BITNOT = "unop_bitnot"
	TERNOP_IF = "ternop_if"
	ATTR = "attr"
	FUNC = "func"
	METH = "meth"

NodeType.__doc__ += f"""
Possible values are:

{"".join(f"\t- ``{nt.name}``\n" for nt in NodeType)}
"""


class VSQLError(Exception):
	"""
	Base class of exceptions that can happend when compiling vSQL expressions.
	"""
	def __init__(self, root_ast:AST, cause_ast:AST, context:str | None=None):
		self.root_ast = root_ast
		self.cause_ast = cause_ast
		self.context = context

	def __str__(self) -> str:
		if self.root_ast is self.cause_ast:
			if self.context is None:
				return f"Error in vSQL expression `{self.root_ast!r}`: {self.detail()}"
			else:
				return f"Error in `{self.context}` expression `{self.root_ast.source()}`: {self.detail()}"
		else:
			if self.context is None:
				return f"Error in vSQL subexpression `{self.cause_ast.source()}` of `{self.root_ast.source()}`: {self.detail()}"
			else:
				return f"Error in `{self.context}` subexpression `{self.cause_ast.source()}` of `{self.root_ast.source()}`: {self.detail()}"

	def detail(self) -> str:
		return "..."


class VSQLSubnodeErrorError(VSQLError):
	def detail(self) -> str:
		return f"AST subnodes are invalid (Internal vSQL error)."


class VSQLUnknownNodeTypeError(VSQLError):
	def detail(self) -> str:
		return f"AST node has unknown type (Internal vSQL error)."


class VSQLArityError(VSQLError):
	def detail(self) -> str:
		return f"AST node has wrong arity (Internal vSQL error)."


class VSQLSubnodeTypesError(VSQLError):
	def detail(self) -> str:
		if any(child.datatype is None for child in self.cause_ast.children()):
			# This shouldn't happen, as :meth:`AST.check_valid` always return the most specific error
			return f"Expression contains invalid sub expression."
		else:
			types = ", ".join(f"`{child.datatype.name}`" for child in self.cause_ast.children())
			return f"Type combination {types} is not supported."


class VSQLUnknownFieldError(VSQLError):
	def detail(self) -> str:
		return f"Expression references the unknown field `{self.cause_ast.identifier}`."


class VSQLMalformedConstantError(VSQLError):
	def detail(self) -> str:
		return f"Constant `{self.cause_ast.nodevalue}` is malformed."


class VSQLAggregationtError(VSQLError):
	def detail(self) -> str:
		return f"Aggregation call is malformed."


class VSQLUnknownNameError(VSQLError):
	def detail(self) -> str:
		if isinstance(self.cause_ast, FuncAST):
			name = f"function name `{self.cause_ast.name}`"
		elif isinstance(self.cause_ast, MethAST):
			name = f"method name `{self.cause_ast.name}`"
		elif isinstance(self.cause_ast, AttrAST):
			name = f"attribute name `{self.cause_ast.attrname}`"
		else:
			name = "name"
		return f"The {name} is unknown."


class VSQLUnsupportedListTypesError(VSQLError):
	def detail(self) -> str:
		return f"List type can't be determined, since it contains unsupported or mixed types."


class VSQLMixedSetTypesError(VSQLError):
	def detail(self) -> str:
		return f"Set type can't be determined, since it contains mixed types."


class VSQLUnsupportedSetTypesError(VSQLError):
	def detail(self) -> str:
		return f"Set type can't be determined, since it contains unsupported or mixed types."


class VSQLWrongDatatypeError(VSQLError):
	def detail(self) -> str:
		return f"The expression should be of type `{self.cause_ast.error.name[9:]}` but is of type `{self.cause_ast.datatype.name}`."


class Error(str, misc.Enum):
	"""
	The types of errors that can lead to invalid vSQL AST nodes.

	Note that some of those can not be produced by the Python implementation.
	"""

	def __new__(cls, value:str, exception:Type[VSQLError]):
		obj = str.__new__(cls, value)
		obj._value_ = value
		obj.exception = exception
		return obj

	SUBNODEERROR = ("subnodeerror", VSQLSubnodeErrorError) # Subnodes are invalid
	NODETYPE = ("nodetype", VSQLUnknownNodeTypeError) # Unknown node type (not any of the ``NODETYPE_...`` values from above
	ARITY = ("arity", VSQLArityError) # Node does not have the required number of children
	SUBNODETYPES = ("subnodetypes", VSQLSubnodeTypesError) # Subnodes have a combination of types that are not supported by the node
	FIELD = ("field", VSQLUnknownFieldError) # ``NODETYPE_FIELD`` nodes references an unknown field
	CONST_BOOL = ("const_bool", VSQLMalformedConstantError) # ``NODETYPE_CONST_BOOL`` value is ``null`` or malformed
	CONST_INT = ("const_int", VSQLMalformedConstantError) # ``NODETYPE_CONST_INT`` value is ``null`` or malformed
	CONST_NUMBER = ("const_number", VSQLMalformedConstantError) # ``NODETYPE_CONST_NUMBER`` value is ``null`` or malformed
	CONST_DATE = ("const_date", VSQLMalformedConstantError) # ``NODETYPE_CONST_DATE`` value is ``null`` or malformed
	CONST_DATETIME = ("const_datetime", VSQLMalformedConstantError) # ``NODETYPE_CONST_DATETIME`` value is ``null`` or malformed
	CONST_TIMESTAMP = ("const_timestamp", VSQLMalformedConstantError) # ``NODETYPE_CONST_DATETIME`` value is ``null`` or malformed
	CONST_COLOR = ("const_color", VSQLMalformedConstantError) # ``NODETYPE_CONST_COLOR`` value is ``null`` or malformed
	NAME = ("name", VSQLUnknownNameError) # Attribute/Function/Method is unknown
	LISTUNSUPPORTEDTYPES = ("listunsupportedtypes", VSQLUnsupportedListTypesError) # List items have unsupported or mixed types, so the type can't be determined
	SETMIXEDTYPES = ("setmixedtypes", VSQLMixedSetTypesError) # Set items have incompatible types, so the type can't be determined
	SETUNSUPPORTEDTYPES = ("setunsupportedtypes", VSQLUnsupportedSetTypesError) # Set items have unsupported types, so the type can't be determined
	DATATYPE_NULL = ("datatype_null", VSQLWrongDatatypeError) # The datatype of the node should be ``null`` but isn't
	DATATYPE_BOOL = ("datatype_bool", VSQLWrongDatatypeError) # The datatype of the node should be ``bool`` but isn't
	DATATYPE_INT = ("datatype_int", VSQLWrongDatatypeError) # The datatype of the node should be ``int`` but isn't
	DATATYPE_NUMBER = ("datatype_number", VSQLWrongDatatypeError) # The datatype of the node should be ``number`` but isn't
	DATATYPE_STR = ("datatype_str", VSQLWrongDatatypeError) # The datatype of the node should be ``str`` but isn't
	DATATYPE_CLOB = ("datatype_clob", VSQLWrongDatatypeError) # The datatype of the node should be ``clob`` but isn't
	DATATYPE_COLOR = ("datatype_color", VSQLWrongDatatypeError) # The datatype of the node should be ``color`` but isn't
	DATATYPE_DATE = ("datatype_date", VSQLWrongDatatypeError) # The datatype of the node should be ``date`` but isn't
	DATATYPE_DATETIME = ("datatype_datetime", VSQLWrongDatatypeError) # The datatype of the node should be ``datetime`` but isn't
	DATATYPE_DATEDELTA = ("datatype_datedelta", VSQLWrongDatatypeError) # The datatype of the node should be ``datedelta`` but isn't
	DATATYPE_DATETIMEDELTA = ("datatype_datetimedelta", VSQLWrongDatatypeError) # The datatype of the node should be ``datetimedelta`` but isn't
	DATATYPE_MONTHDELTA = ("datatype_monthdelta", VSQLWrongDatatypeError) # The datatype of the node should be ``monthdelta`` but isn't
	DATATYPE_NULLLIST = ("datatype_nulllist", VSQLWrongDatatypeError) # The datatype of the node should be ``nulllist`` but isn't
	DATATYPE_INTLIST = ("datatype_intlist", VSQLWrongDatatypeError) # The datatype of the node should be ``intlist`` but isn't
	DATATYPE_NUMBERLIST = ("datatype_numberlist", VSQLWrongDatatypeError) # The datatype of the node should be ``numberlist`` but isn't
	DATATYPE_STRLIST = ("datatype_strlist", VSQLWrongDatatypeError) # The datatype of the node should be ``strlist`` but isn't
	DATATYPE_CLOBLIST = ("datatype_cloblist", VSQLWrongDatatypeError) # The datatype of the node should be ``cloblist`` but isn't
	DATATYPE_DATELIST = ("datatype_datelist", VSQLWrongDatatypeError) # The datatype of the node should be ``datelist`` but isn't
	DATATYPE_DATETIMELIST = ("datatype_datetimelist", VSQLWrongDatatypeError) # The datatype of the node should be ``datetimelist`` but isn't
	DATATYPE_NULLSET = ("datatype_nullset", VSQLWrongDatatypeError) # The datatype of the node should be ``nullset`` but isn't
	DATATYPE_INTSET = ("datatype_intset", VSQLWrongDatatypeError) # The datatype of the node should be ``intset`` but isn't
	DATATYPE_NUMBERSET = ("datatype_numberset", VSQLWrongDatatypeError) # The datatype of the node should be ``numberset`` but isn't
	DATATYPE_STRSET = ("datatype_strset", VSQLWrongDatatypeError) # The datatype of the node should be ``strset`` but isn't
	DATATYPE_DATESET = ("datatype_dateset", VSQLWrongDatatypeError) # The datatype of the node should be ``dateset`` but isn't
	DATATYPE_DATETIMESET = ("datatype_datetimeset", VSQLWrongDatatypeError) # The datatype of the node should be ``datetimeset`` but isn't

Error.__doc__ += f"""
Possible values are:

{"".join(f"\t- ``{e.name}``\n" for e in Error)}
"""


@ul4on.register("de.livinglogic.vsql.field")
class Field(Repr):
	"""
	A :class:`!Field` object describes a database field.

	This field is either in a database table or view or a global variable.

	As a table or view field it belongs to a :class:`Group` object.
	"""

	identifier : str
	datatype : DataType | None
	fieldsql : templatelib.Template
	joinsql : templatelib.Template | None
	refgroup : Group | None

	def __init__(self, identifier:str | None=None, datatype:DataType=DataType.NULL, fieldsql:T_sql | None=None, joinsql:T_sql | None=None, refgroup:Group | None=None):
		"""
		Create a :class:`Field` instance.

		Argument are:

		``identifier``
			The UL4 identifier of the field

		``datatype``
			The vSQL datatype of the field

		``fieldsql``
			The SQL expression for that fields. This should include ``{a}`` as a
			placeholder for the table alias.

		``joinsql``
			If this field is a foreign key to another table, ``joinsql`` is the
			join condition. This should include ``{m}`` and ``{d}`` placeholder
			for the table aliases of the master table (i.e. the one where this
			field is in) and the detail table (i.e. the one that will be joined).

		``refgroup``
			The :class:`Group` object that represents the target table.
		"""
		self.identifier = identifier
		self.datatype = datatype
		self.fieldsql = to_tstring(fieldsql)
		self.joinsql = to_tstring(joinsql)
		self.refgroup = refgroup

	def _ll_repr_(self) -> Generator[str, None, None]:
		yield f"identifier={self.identifier!r}"
		if self.datatype is not None:
			yield f"datatype={self.datatype.name}"
		if self.fieldsql is not None:
			yield f"fieldsql={self.fieldsql!r}"
		if self.joinsql is not None:
			yield f"joinsql={self.joinsql!r}"
		if self.refgroup is not None:
			yield f"refgroup.tablesql={self.refgroup.tablesql!r}"

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		p.breakable()
		p.text("identifier=")
		p.pretty(self.identifier)
		if self.datatype is not None:
			p.breakable()
			p.text(f"datatype={self.datatype.name}")
		if self.fieldsql is not None:
			p.breakable()
			p.text("fieldsql=")
			p.pretty(self.fieldsql)
		if self.joinsql is not None:
			p.breakable()
			p.text("joinsql=")
			p.pretty(self.joinsql)
		if self.refgroup is not None:
			p.breakable()
			p.text("refgroup.tablesql=")
			p.pretty(self.refgroup.tablesql)

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		encoder.dump(self.identifier)
		encoder.dump(self.datatype.value if self.datatype is not None else None)
		encoder.dump(self.fieldsql)
		encoder.dump(self.joinsql)
		encoder.dump(self.refgroup)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		self.identifier = decoder.load()
		datatype = decoder.load()
		self.datatype = DataType(datatype) if datatype is not None else None
		self.fieldsql = decoder.load()
		self.joinsql = decoder.load()
		self.refgroup = decoder.load()


@ul4on.register("de.livinglogic.vsql.group")
class Group(Repr):
	"""
	A :class:`!Group` object describes a group of database fields.

	These fields are part of a database table or view and are instances of
	:class:`Field`.
	"""

	tablesql : str
	fields : dict[str, Field]

	def __init__(self, tablesql:T_sql | None=None, **fields:Field | tuple[DataType, T_sql] | tuple[DataType, T_sql, T_sql, Group]):
		self.tablesql = to_tstring(tablesql)
		self.fields = {}
		for (fieldname, fielddata) in fields.items():
			if not isinstance(fielddata, Field):
				fielddata = Field(fieldname, *fielddata)
			self.fields[fieldname] = fielddata

	def _ll_repr_(self) -> Generator[str, None, None]:
		yield f"tablesql={self.tablesql!r}"
		yield f"with {len(self.fields):,} fields"

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		p.breakable()
		p.text("tablesql=")
		p.pretty(self.tablesql)

	def __getitem__(self, key:str) -> Field:
		if key in self.fields:
			return self.fields[key]
		elif "*" in self.fields:
			return self.fields["*"]
		else:
			raise KeyError(key)

	def add_field(self, identifier:str, datatype:DataType, fieldsql:T_sql, joinsql:T_sql | None=None, refgroup:Group | None=None) -> None:
		"""
		Create a :class:`Field` object from the arguments and add it to the fields of the group.
		"""
		field = Field(identifier, datatype, fieldsql, joinsql, refgroup)
		self.fields[identifier] = field

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		encoder.dump(self.tablesql)
		encoder.dump(self.fields)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		self.tablesql = decoder.load()
		self.fields = decoder.load()


class Query(Repr):
	"""
	A :class:`!Query` object can be used to build an SQL query using vSQL expressions.
	"""

	class SQLExpr(Repr):
		_ll_repr_attrs_ = ["expr", "comment"]
		context = None
		query : Query
		expr : templatelib.Template
		comment : str | None

		def __init__(self, query, expr : T_sql, comment : str | None = None):
			self.query = query
			self.expr = to_tstring(expr)
			self.comment = comment

		def sqlsource(self) -> templatelib.Template:
			return add_comment(self.expr, self.comment)

	class VSQLExpr(Repr):
		_ll_repr_attrs_ = ["expr", "comment"]
		context = None
		query : Query
		expr : AST
		comment : str | None

		def __init__(self, query, expr : str, comment : str | None = None):
			self.query = query
			self.expr = query._vsql(expr, self.context)
			self.comment = comment

		def sqlsource(self) -> templatelib.Template:
			sqlsource = self.expr.sqlsource(self.query)
			return add_comment(sqlsource, self.comment)

		def conform(self, value):
			"""
			Converts the value ``value`` to the form expected by this vSQL expression.

			This is used to convert :class:`datetime.dateime` values from Oracle
			to :class:`datetime.date` for expressions of the ``DataType.DATE``.

			If this is not a vSQL expression ``value`` will be returned unmodified.
			"""
			if self.expr is not None and self.expr.datatype is DataType.DATE and isinstance(value, datetime.datetime):
				value = value.date()
			return value

	class SQLSelectExpr(SQLExpr):
		_ll_repr_attrs_ = ["alias"]
		context = "select"
		alias : templatelib.Template | None

		def __init__(self, query, expr, comment=None, alias=None):
			super().__init__(query, expr, comment)
			self.alias = to_tstring(alias)

		def sqlsource(self) -> templatelib.Template:
			sqlsource = super().sqlsource()
			if self.alias is not None:
				sqlsource = t"{sqlsource:l} as {self.alias:l}"
			return sqlsource

	class VSQLSelectExpr(VSQLExpr):
		_ll_repr_attrs_ = ["alias"]
		context = "select"
		alias : templatelib.Template | None

		def __init__(self, query, expr, comment=None, alias=None):
			super().__init__(query, expr, comment)
			self.alias = to_tstring(alias)

		def sqlsource(self) -> templatelib.Template:
			sqlsource = super().sqlsource()
			if self.alias is not None:
				sqlsource = t"{sqlsource:l} as {self.alias:l}"
			return sqlsource

	class SQLAggregatedSelectExpr(SQLSelectExpr):
		context = "aggregate"

	class VSQLAggregatedSelectExpr(VSQLSelectExpr):
		_ll_repr_attrs_ = ["aggregate"]
		context = "aggregate"
		aggregate : Aggregate

		def __init__(self, query, expr, comment=None, alias=None):
			self.query = query
			expr = AST.fromsource(expr, **query.vars)
			if not isinstance(expr, FuncAST):
				raise VSQLAggregationtError(expr, expr, self.context)
			if expr.name == "count" and not expr.args:
				self.aggregate = Aggregate.COUNT
				self.expr = None
			elif expr.name in {"min", "max", "sum", "group"} and len(expr.args) == 1:
				self.aggregate = Aggregate(expr.name)
				self.expr = expr.args[0]
				self.expr.check_valid(self.context)
				for fieldref in expr.fieldrefs():
					query._register(fieldref)
			else:
				raise VSQLAggregationtError(expr, expr, self.context)
			self.comment = comment
			self.alias = to_tstring(alias)

		def sqlsource(self) -> templatelib.Template:
			if self.expr is None:
				sqlsource = t"count(*)"
			else:
				sqlsource = Query.VSQLExpr.sqlsource(self) # We don't want the alias

			if self.aggregate is Aggregate.COUNT:
				sqlsource = t"count(*)"
			elif self.aggregate is not Aggregate.GROUP:
				name = templatelib.Template(self.aggregate.value)
				sqlsource = t"{name:l}({sqlsource:l})"
			if self.alias is not None:
				sqlsource = t"{sqlsource:l} as {self.alias:l}"
			return sqlsource

	class SQLFromExpr(SQLExpr):
		_ll_repr_attrs_ = ["alias"]
		context = "from"
		alias : templatelib.Template | None

		def __init__(self, query, expr=None, comment=None, alias=None):
			super().__init__(query, expr, comment)
			self.alias = to_tstring(alias)

		def sqlsource(self) -> templatelib.Template:
			sqlsource = super().sqlsource()
			if self.alias is not None:
				sqlsource = t"{sqlsource:l} {self.alias:l}"
			return sqlsource

	class SQLWhereExpr(SQLExpr):
		context = "where"

	class VSQLWhereExpr(VSQLExpr):
		context = "where"

		def __init__(self, query, expr, comment=None):
			super().__init__(query, expr, comment)

			if self.expr.datatype is not DataType.BOOL:
				self.expr = FuncAST.make("bool", self.expr)

		def sqlsource(self) -> templatelib.Template:
			return t"{super().sqlsource():l} = 1"

	class SQLGroupByExpr(SQLExpr):
		context = "groupby"

	class VSQLGroupByExpr(VSQLExpr):
		context = "groupby"

	class SQLOrderByExpr(SQLExpr):
		_ll_repr_attrs_ = ["dir", "nulls"]
		context = "orderby"

		dir : str | None
		nulls : str | None

		def __init__(self, query, expr, comment, dir, nulls):
			super().__init__(query, expr, comment)
			self.dir = dir
			self.nulls = nulls

		def sqlsource(self) -> templatelib.Template:
			sqlsource = super().sqlsource()
			if self.dir is not None:
				sqlsource = t"{sqlsource:l} {self.dir:l}"
			if self.nulls is not None:
				sqlsource = t"{sqlsource:l} nulls {self.nulls:l}"
			return sqlsource

	class VSQLOrderByExpr(VSQLExpr):
		_ll_repr_attrs_ = ["dir", "nulls"]
		context = "orderby"

		dir : str | None
		nulls : str | None

		def __init__(self, query, expr, comment, dir, nulls):
			super().__init__(query, expr, comment)
			self.dir = dir
			self.nulls = nulls

		def sqlsource(self) -> templatelib.Template:
			sqlsource = super().sqlsource()
			if self.dir is not None:
				sqlsource = t"{sqlsource:l} {self.dir:l}"
			if self.nulls is not None:
				sqlsource = t"{sqlsource:l} nulls {self.nulls:l}"
			return sqlsource

	comment : str | None
	vars : dict[str, Field]
	fields : dict[TStringHasher, SQLSelectExpr | VSQLSelectExpr] # Key is the SQL source
	aggregated_fields : dict[TStringHasher, SQLAggregatedSelectExpr | VSQLAggregatedSelectExpr] # Key is the SQL source
	_from : dict[TStringHasher, SQLFromExpr] # Key is the SQL source + the alias
	_where : dict[TStringHasher, SQLWhereExpr | VSQLWhereExpr]
	_orderby : list[SQLOrderByExpr | VSQLOrderByExpr]
	_groupby : dict[TStringHasher, SQLGroupByExpr | VSQLGroupByExpr]
	_offset : int | None
	_limit = int | None
	_identifier_aliases : dict[str, str]

	def __init__(self, comment:str | None=None, **vars:Field):
		"""
		Create a new empty :class:`!Query` object.

		Arguments are:

		``comment`` : :class:`str` or ``None``
			A comment that will be included in the generated SQL.

		``vars`` : :class:`Field`
			These are the top level variables that will be availabe for vSQL
			expressions added to this query. The argument name is the name of
			the variable. The argument value is a :class:`Field` object that
			describes this variable.

			In most cases this :class:`Field` object is a foreign key to another
			table, so it has a ``joinsql`` and a ``refgroup``.
		"""
		self.comment = comment
		self.vars = {name: field for (name, field) in vars.items() if field is not None}
		self.fields = {}
		self.aggregated_fields = {}
		self._from = {}
		self._where = {}
		self._orderby = []
		self._groupby = {}
		self._offset = None
		self._limit = None
		self._identifier_aliases = {}

	def _register(self, fieldref:FieldRefAST) -> str | None:
		"""
		Registers the :class:`FieldRefAST` object `fieldref`.

		This means that all the tables and join conditions that are required to
		access the field will be added to the "from" and "where" clauses.
		"""
		if fieldref.error is not None:
			return # Don't register broken expressions
		if fieldref.parent is None:
			# No need to register anything as this is a "global variable".
			# Also we don't need a table alias to access this field.
			return None

		identifier = fieldref.parent.full_identifier
		if identifier in self._identifier_aliases:
			alias = self._identifier_aliases[identifier]
			return alias

		alias = self._register(fieldref.parent)

		newalias = f"t{len(self._from)+1}"
		joincond = fieldref.parent.field.joinsql
		if joincond is not None:
			# Only add to "where" if the join condition is not empty
			if alias is not None:
				joincond = tstring_replace(joincond, "{m}", alias)
			joincond = tstring_replace(joincond, "{d}", newalias)
			hasher = TStringHasher(joincond)
			self._where[hasher] = self.SQLWhereExpr(self, joincond, fieldref.parent.source())

		if fieldref.parent.field.refgroup.tablesql is None:
			# If this field is not part of a table (which can happen e.g. for
			# the request parameters, which we get from function calls),
			# we don't add the table aliases to the list of table aliases
			# and we don't add a table to the "from" list.
			return None

		self._identifier_aliases[identifier] = newalias
		sql = fieldref.parent.field.refgroup.tablesql
		hasher = TStringHasher(t"{sql:l} {newalias:l}")
		self._from[hasher] = self.SQLFromExpr(self, sql, comment=fieldref.parent.source(), alias=newalias)
		return newalias

	def from_vsql(self, identifier:str) -> str | None:
		"""
		Registers the field identifier ``identifier`` as a table to select from.

		``identifier`` must belong to one of the fields passed to the constructor
		and it should reference a table.

		:func:`from_vsql` will then make sure that this referenced table will
		be added to the "from" list, even if it is never referenced explicitely
		in any of the "from" and "where" clauses.
		"""
		if identifier not in self.vars:
			raise ValueError(f"Unknown field {identifier!r}!")
		field = self.vars[identifier]
		newalias = f"t{len(self._from)+1}"
		joincond = field.joinsql
		if joincond is not None:
			# Only add to "where" if the join condition is not empty
			joincond = tstring_replace(joincond, "{d}", newalias)
			hasher = TStringHasher(joincond)
			self._where[hasher] = self.SQLWhereExpr(self, joincond, identifier)

		if field.refgroup.tablesql is None:
			# If this field is not part of a table (which can happen e.g. for
			# the request parameters, which we get from function calls),
			# we don't add the table aliases to the list of table aliases
			# and we don't add a table to the "from" list.
			return None

		self._identifier_aliases[identifier] = newalias
		sql = field.refgroup.tablesql
		hasher = TStringHasher(t"{sql:l} {newalias:l}")
		self._from[hasher] = self.SQLFromExpr(self, sql, identifier, newalias)
		return newalias

	def _vsql(self, expr:str, context:str) -> None:
		"""
		Compiles ``expr`` to a vSQL :class:`AST` and register all field references in it.

		Does type inference and checks for valid type combinations.

		``context`` is the query context in which this expression is used and
		can be ``"select"``, ``"from"``, ``"where"`` and ``"orderby``".
		(This is used as additional information in exceptions)
		"""
		vsqlexpr = AST.fromsource(expr, **self.vars)
		vsqlexpr.check_valid(context)
		for fieldref in vsqlexpr.fieldrefs():
			self._register(fieldref)
		return vsqlexpr

	def select_vsql(self, expr:str, comment : str | None = None, alias : str | None = None) -> Query.VSQLSelectExpr:
		"""
		Add the vSQL expression ``expr`` to the list of expression to select.

		``comment`` will be added as a comment after the column expression.

		``alias`` can be used to give the expression a column alias.

		This compiles ``expr`` and adds the resulting SQL. To add an
		SQL expression directly use :meth:`select_sql` instead.
		"""
		if self.aggregated_fields:
			raise TypeError("Can't mix non-aggregated and aggregated select expressions")
		if self._groupby:
			raise TypeError("Can't mix non-aggregated select expressions and groupby expressions")

		vsqlexpr = self.VSQLSelectExpr(self, expr, comment, alias)
		sqlsource = vsqlexpr.sqlsource()
		hasher = TStringHasher(sqlsource)
		if hasher in self.fields:
			return self.fields[hasher]
		self.fields[hasher] = vsqlexpr
		return vsqlexpr

	def select_sql(self, expr:T_sql, comment=None, alias=None) -> Query.SQLSelectExpr:
		"""
		Add the SQL expression ``expr`` to the list of expression to select.

		``comment`` can be used to give the column a comment in the select list.

		``alias`` can be used to give the expression a column alias.

		Note that that adds ``expr`` directly as "raw" SQL. To add a vSQL
		expression use :meth:`select_vsql` instead.
		"""
		if self.aggregated_fields:
			raise TypeError("Can't mix non-aggregated and aggregated select expressions")
		if self._groupby:
			raise TypeError("Can't mix non-aggregated select expressions and groupby expressions")

		sqlexpr = self.SQLSelectExpr(self, expr, comment, alias)
		sqlsource = sqlexpr.sqlsource()
		hasher = TStringHasher(sqlsource)
		if hasher in self.fields:
			return self.fields[hasher]
		self.fields[hasher] = sqlexpr
		return sqlexpr

	def aggregate_vsql(self, expr:str, comment : str | None = None, alias : str | None = None) -> Query.VSQLAggregatedSelectExpr:
		"""
		Add the aggregating vSQL expression ``expr`` to the list of expression to select.

		``comment`` will be added as a comment after the column expression.

		``alias`` can be used to give the expression a column alias.

		Note that it's not possible to mix aggregated and non-aggregated
		fields. For a vSQL expression to be an aggregating expression it
		must either be the function call ``count()`` (without arguments),
		or call one of the functions ``group()``, ``min()``, `max()`` or
		``sum()`` with one argument. These function do the following:

		``count()``
			Return number of records in this group;

		``min(expr)``
			Return the minimum value of the expressions ``expr`` for all
			records in this group;

		``max(expr)``
			Return the maximum value of the expressions ``expr`` for all
			records in this group;

		``sum(expr)``
			Return the sum of the values for the expressions ``expr`` for
			all records in this group.

		``group(expr)``
			Use the grouping value ``expr`` (which is the same for all records
			in this group).
		"""
		if self.fields:
			raise TypeError("Can't mix aggregated and non-aggregated select expressions")
		vsqlexpr = self.VSQLAggregatedSelectExpr(self, expr, comment, alias)
		sqlsource = vsqlexpr.sqlsource()
		hasher = TStringHasher(sqlsource)
		if hasher in self.aggregated_fields:
			vsqlexpr = self.aggregated_fields[hasher]
		else:
			self.aggregated_fields[hasher] = vsqlexpr
		if vsqlexpr.aggregate is Aggregate.GROUP and hasher not in self._groupby:
			self.groupby_vsql(vsqlexpr.expr.source())
		return vsqlexpr

	def aggregate_sql(self, expr:T_sql, comment : str | None, alias : T_sql | None = None) -> Query.SQLAggregatedSelectExpr:
		"""
		Add the aggregating SQL expression ``expr`` to the list of expression to select.

		``comment`` will be added as a comment after the column expression.

		``alias`` can be used to give the expression a column alias.

		Note that it's not possible to mix aggregated and non-aggregated
		fields.

	 	Make sure that ``expr`` is an aggregating expression like
		``count(*)`` or ``max(tbl.value)``
		"""
		if self.fields:
			raise TypeError("Can't mix aggregated and non-aggregated select expressions")
		sqlexpr = self.SQLAggregatedSelectExpr(self, expr, comment, alias)
		sqlsource = sqlexpr.sqlsource()
		hasher = TStringHasher(sqlsource)
		if hasher in self.aggregated_fields:
			return self.aggregated_fields[hasher]
		self.aggregated_fields[hasher] = sqlexpr
		return sqlexpr

	def from_sql(self, tablename, comment=None, alias=None) -> Query.SQLFromExpr:
		"""
		Add a table to the list of tables to select from.

		This adds the table in "raw" SQL form.

		There's no need to add to the "from" list in vSQL form, since this
		is done automatically in :meth:`select_vsql`, :meth:`where_vsql` or
		:meth:`orderby_vsql`.
		"""
		for f in self._from:
			(n, a) = f.strings[-1].rsplit(" ", 1)
			if a == alias:
				raise ValueError(f"duplicate table alias {alias!r}")
		sqlexpr = self.SQLFromExpr(self, tablename, comment, alias)
		hasher = TStringHasher(t"{tablename:l} {alias:l}")
		self._from[hasher] = sqlexpr
		return sqlexpr

	def where_vsql(self, expr:str) -> Query.VSQLWhereExpr:
		"""
		Add vSQL condition ``expr`` to the ``where`` clause.

		Note that this compiles ``expr`` and add the resulting SQL. To add an
		SQL expression directly use :meth:`where_sql` instead.

		If ``expr`` doesn't have the datatype ``BOOL`` it will be automatically
		converted to ``BOOL``.
		"""
		vsqlexpr = self.VSQLWhereExpr(self, expr)
		sqlsource = vsqlexpr.sqlsource()
		hasher = TStringHasher(sqlsource)
		if hasher in self._where:
			return self._where[hasher]
		self._where[hasher] = vsqlexpr
		return vsqlexpr

	def where_sql(self, expr:T_sql, comment:str|None=None) -> Query.SQLWhereExpr:
		"""
		Add vSQL condition ``expr`` to the ``where`` clause.

		Note that that adds ``expr`` directly as "raw" SQL. To add a vSQL
		expression use :meth:`where_vsql` instead.
		"""
		sqlexpr = self.SQLWhereExpr(self, expr, comment)
		sqlsource = sqlexpr.sqlsource()
		hasher = TStringHasher(sqlsource)
		if hasher in self._where:
			return self._where[hasher]
		self._where[hasher] = sqlexpr
		return sqlexpr

	def groupby_vsql(self, expr:T_sql, comment : str | None = None) -> Query.VSQLGroupByExpr:
		"""
		Add the grouping vSQL expression ``expr`` to the list of expression to group by.

		``comment`` will be added as a comment after the column expression.
		"""
		if self.fields:
			raise TypeError("Can't mix groupby and non-aggregated select expressions")
		vsqlexpr = self.VSQLGroupByExpr(self, expr, comment)
		sqlsource = vsqlexpr.sqlsource()
		hasher = TStringHasher(sqlsource)
		if hasher in self._groupby:
			return self._groupby[hasher]
		self._groupby[hasher] = vsqlexpr
		return vsqlexpr

	def groupby_sql(self, expr:T_sql, comment : str | None = None) -> Query.SQLGroupByExpr:
		"""
		Add the grouping SQL expression ``expr`` to the list of expression to group by.

		``comment`` will be added as a comment after the column expression.
		"""
		if self.fields:
			raise TypeError("Can't mix groupby and non-aggregated select expressions")

		sqlexpr = self.SQLGroupByExpr(self, expr, comment)
		sqlsource = sqlexpr.sqlsource()
		hasher = TStringHasher(sqlsource)
		if hasher in self._groupby:
			return self._groupby[hasher]
		self._groupby[hasher] = sqlexpr
		return sqlexpr

	def _extract_orderby(self, expr:str) -> tuple[str, str | None, str | None]:
		expr = to_tstring(expr)
		if expr.strings[-1].endswith(" nulls last"):
			nulls = "last"
			expr = templatelib.Template(*(p.removesuffix(" nulls last") if l else p for (l, p) in misc.islast(expr)))
		elif expr.strings[-1].endswith(" nulls first"):
			nulls = "first"
			expr = templatelib.Template(*(p.removesuffix(" nulls first") if l else p for (l, p) in misc.islast(expr)))
		else:
			nulls = None
		if expr.strings[-1].endswith(" asc"):
			dir = "asc"
			expr = templatelib.Template(*(p.removesuffix(" asc") if l else p for (l, p) in misc.islast(expr)))
		elif expr.strings[-1].endswith(" desc"):
			dir = "desc"
			expr = templatelib.Template(*(p.removesuffix(" desc") if l else p for (l, p) in misc.islast(expr)))
		else:
			dir = None
		return (expr, dir, nulls)

	def orderby_vsql(self, expr:T_sql, comment : str | None = None) -> Query.VSQLOrderByExpr:
		r"""
		Add the "order by" vSQL expression ``expr`` to this query.

		"order by" specifications will be output in the query in the order they
		have been added.

		The format must be a vSQL expression optionally followed by ``asc`` or
		``desc`` optionally followed by ``nulls first`` or ``nulls last``

		``asc`` sorts in ascending order and ``desc`` sorts descending order.
		If neither is specified neither ``asc`` nor ``desc`` will be added to
		the query (which is equivalent to ``asc``).

		``nulls first`` outputs ``null`` values first, ``nulls last`` outputs
		them last.

		Example::

			>>> from ll import vsql
			>>> q = vsql.Query("Example query", user=la.User.vsqlfield())
			>>> q.select_vsql("user.email")
			>>> q.orderby_vsql("user.firstname asc nulls first")
			>>> q.orderby_vsql("user.surname desc nulls last")
			>>> print(q.sqlsource())
			/* Example query */
			select
				t1.ide_account /* user.email */
			from
				identity t1 /* user */
			where
				livingapi_pkg.global_user = t1.ide_id(+) /* user */
			order by
				t1.ide_firstname /* user.firstname */ asc nulls first,
				t1.ide_surname /* user.surname */ desc nulls last
		"""
		(expr, dir, nulls) = self._extract_orderby(expr)
		vsqlexpr = self.VSQLOrderByExpr(self, expr, None, dir, nulls)
		self._orderby.append(vsqlexpr)
		return vsqlexpr

	def orderby_sql(self, expr:str, comment : str | None = None) -> Query.SQLOrderByExpr:
		"""
		Add the "order by" SQL expression ``expr`` to this query.

		"order by" specifications will be output in the query in the order they
		have been added.

		Note that that adds ``expr`` directly as "raw" SQL. To add a vSQL
		expression use :meth:`select_vsql` instead.

		The format must be an SQL expression optionally followed by ``asc`` or
		``desc`` optionally followed by ``nulls first`` or ``nulls last``

		``asc`` sorts in ascending order and ``desc`` sorts descending order.
		If neither is specified neither ``asc`` nor ``desc`` will be added to
		the query (which is equivalent to ``asc``).

		``nulls first`` outputs ``null`` values first, ``nulls last`` outputs
		them last.
		"""
		(expr, dir, nulls) = self._extract_orderby(expr)
		sqlexpr = self.SQLOrderByExpr(self, expr, comment, dir, nulls)
		self._orderby.append(sqlexpr)
		return sqlexpr

	def offset(self, offset: int | None) -> None:
		"""
		Use ``offset`` as the offset value.

		This offset specifies how mnay records to skip before returing
		the first one. The default `0` or `None` doesn't skip any records.
		"""
		self._offset = offset

	def limit(self, limit: int | None) -> None:
		"""
		Use ``limit`` to limit the number of records returned.

		After ``limit`` records no further records will be returned even if there
		are more than ``limit`` records that match the filter condition.
		"""
		self._limit = limit

	def sqlsource(self, indent="\t") -> str:
		"""
		Return the SQL source code for this query.

		For example::

			>>> from ll import vsql
			>>> print(vsql.Query().select_vsql("now()").sqlsource()))
			select
				sysdate /* now() */
			from
				dual
		"""
		tokens = []

		def a(*parts):
			tokens.extend(parts)

		if self.comment:
			a(templatelib.Template(format_comment(self.comment)), None)

		a(t"select", None, +1)
		first = True
		for expr in self.fields.values():
			if first:
				first = False
			else:
				a(t",", None)
			a(expr.sqlsource())
		for expr in self.aggregated_fields.values():
			if first:
				first = False
			else:
				a(t",", None)
			a(expr.sqlsource())
		if first:
			a(t"42")
		a(None, -1)

		a(t"from", None, +1)
		first = True
		for expr in self._from.values():
			if first:
				first = False
			else:
				a(t",", None)
			a(expr.sqlsource())
		if first:
			a(t"dual")
		a(None, -1)

		if self._where:
			a(t"where", None, +1)
			for (i, expr) in enumerate(self._where.values()):
				if i:
					a(t" and", None)
				a(expr.sqlsource())
			a(None, -1)

		if self._groupby:
			a(t"group by", None, +1)
			first = True
			for expr in self._groupby.values():
				if first:
					first = False
				else:
					a(t",", None)
				a(expr.sqlsource())
			a(None, -1)

		if self._orderby:
			a(t"order by", None, +1)
			for (i, expr) in enumerate(self._orderby):
				if i:
					a(t",", None)
				a(expr.sqlsource())
			a(None, -1)

		if self._offset is not None:
			a(templatelib.Template(f"offset {self._offset} rows"), None)
		if self._limit is not None:
			a(templatelib.Template(f"fetch next {self._limit} rows only"), None)

		source = t""
		first = True
		level = 0
		for part in tokens:
			if part is None:
				if indent:
					source += t"\n"
					first = True
			elif isinstance(part, int):
				level += part
			else:
				if first:
					if indent:
						source += templatelib.Template(level*indent)
					else:
						source += t" "
				source += part
				first = False

		return flatten_tstring(source)


class Rule(Repr):
	"""
	:class:`!Rule` is used to store a type specific vSQL grammar rule.

	I.e. one rule object stores the information that:

	- there's and addition operator;
	- that adds two ``INT`` values;
	- with a result of type ``INT``;
	- and the SQL code to generate for that operation.

	For more information see :meth:`AST.add_rules`.
	"""
	_re_specials = re.compile(r"{([st])(\d)}")
	_re_sep = re.compile(r"\W+")
	_re_tokenize = re.compile(r"\b[A-Z_0-9]+\b")

	# Mappings of vSQL datatypes to other datatypes for creating the SQL source
	source_aliases = {
		"bool":         "int",
		"date":         "datetime",
		"datelist":     "datetimelist",
		"intset":       "intlist",
		"numberset":    "numberlist",
		"strset":       "strlist",
		"dateset":      "datetimelist",
		"datetimeset":  "datetimelist",
	}

	def __init__(self, astcls, spectemplate, spec, source, vsqltokens):
		# The interpolations in ``spectemplate`` are the types and a function/method/attribute name,
		# e.g. for the method call ``INT <- STR.find(STR)`` the interpolations are
		# ``DataType.INT`` - the result type
		# ``DataType.STR`` - The type the method is called on
		# ``find`` - The name of the method
		# ``DataType.STR`` - the type of the argument
		# On the right hand side types might be a single type or multiple ones

		# What we need is:
		# - The result type: ``INT`` (i.e. the first interpolation)
		# - The name of the function/method/attribute (i.e. the only interpolation of type string)
		# - The key that uniquely identifies this operator (ie. all interpolations except the result type)
		# - The type signature (i.e. all ``DataType`` interpolations except the result type)
		self.astcls = astcls
		self.result = spec[0]
		self.name = misc.first(p for p in spec if isinstance(p, str))
		self.key = spec[1:]
		self.signature = tuple(p for p in spec if isinstance(p, DataType))[1:]
		self.source = self._make_source(self.signature, source)
		self.vsqlsource = self._make_vsqlsource(self.signature, spectemplate)

	def _key(self) -> str:
		key = ", ".join(p.name if isinstance(p, DataType) else repr(p) for p in self.key)
		return f"({key})"

	def str_signature(self):
		signature = ", ".join(p.name for p in self.signature)
		return f"({signature})"

	def str_vsqlsource(self):
		return "".join(p if isinstance(p, str) else p.name for p in self.vsqlsource)

	def _ll_repr_(self) -> Generator[str, None, None]:
		yield f"nodetype={self.astcls.nodetype.name}"
		yield f"result={self.result.name}"
		if self.name is not None:
			yield f"name={self.name!r}"
		yield f"key={self._key()}"
		yield f"signature={self.str_signature()}"
		yield f"source={self.source}"
		yield f"vsqlsource={self.str_vsqlsource()}"

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		p.breakable()
		p.text("result=")
		p.text(self.result.name)
		if self.name is not None:
			p.breakable()
			p.text("name=")
			p.pretty(self.name)
		p.breakable()
		p.text("signature=")
		p.text(self.str_signature())
		p.breakable()
		p.text("key=")
		p.text(self._key())
		p.breakable()
		p.text("source=")
		p.pretty(self.source)
		p.breakable()
		p.text("vsqlsource=")
		p.pretty(self.str_vsqlsource())

	@classmethod
	def _make_source(cls, signature:tuple[DataType, ...], source:templatelib.Template) -> tuple[int | str, ...]:
		final_source = []

		def append(text):
			if final_source and isinstance(text, str) and isinstance(final_source[-1], str):
				final_source[-1] += text
			else:
				final_source.append(text)

		for p in source:
			if isinstance(p, str):
				append(p)
			else:
				pos = int(p.value[1:])
				if p.value[0] == "s":
					append(pos)
				else:
					type = signature[pos-1].name.lower()
					type = cls.source_aliases.get(type, type)
					append(type)
		return tuple(final_source)

	@classmethod
	def _make_vsqlsource(cls, signature:tuple[DataType, ...], spectemplate:templatelib.Template) -> tuple[DataType | str, ...]:
		final_source = []

		def append(text):
			if final_source and isinstance(text, str) and isinstance(final_source[-1], str):
				final_source[-1] += text
			else:
				final_source.append(text)

		parts = list(spectemplate)
		while parts and isinstance(parts[0], str):
			parts.pop(0)
		if parts:
			parts.pop(0)
		if parts:
			first = parts[0].lstrip().split(None, 1)
			if len(first) > 1:
				append(first[1])
			parts.pop(0)
		i = 0
		for p in parts:
			if isinstance(p, str):
				append(p)
			elif isinstance(p.value, str):
				append(p.value)
			else:
				append(signature[i])
				i += 1
		return tuple(final_source)

	def java_source(self) -> str:
		key = ", ".join(
			f"VSQLDataType.{p.name}" if isinstance(p, DataType) else misc.javaexpr(p)
			for p in self.key
		)

		source = ", ".join(misc.javaexpr(s) for s in self.source)

		return f"addRule(rules, VSQLDataType.{self.result.name}, List.of({key}), List.of({source}));"

	def oracle_fields(self) -> dict[str, int | str | sqlliteral]:
		fields = {}

		fields["vr_nodetype"] = self.astcls.nodetype.value
		fields["vr_value"] = self.name
		fields["vr_result"] = self.result.value
		fields["vr_signature"] = " ".join(p.value for p in self.signature)
		fields["vr_arity"] = len(self.signature)

		wantlit = True
		index = 1

		for part in self.source:
			if wantlit:
				if isinstance(part, int):
					index += 1 # skip this field
					fields[f"vr_child{index}"] = part
				else:
					fields[f"vr_literal{index}"] = part
				wantlit = False
			else:
				if isinstance(part, int):
					fields[f"vr_child{index}"] = part
				else:
					raise ValueError("two children")
				wantlit = True
			index += 1

		fields["vr_cdate"] = sqlliteral("sysdate")
		fields["vr_cname"] = sqlliteral("c_user")

		return fields

	def oracle_source(self) -> str:
		fieldnames = []
		fieldvalues = []
		for (fieldname, fieldvalue) in self.oracle_fields().items():
			fieldvalue = sql(fieldvalue)
			if fieldvalue != "null":
				fieldnames.append(fieldname)
				fieldvalues.append(fieldvalue)
		fieldnames = ", ".join(fieldnames)
		fieldvalues = ", ".join(fieldvalues)

		return f"insert into vsqlrule ({fieldnames}) values ({fieldvalues});"


###
### Classes for all vSQL abstract syntax tree node types
###

class AST(Repr):
	"""
	Base class of all vSQL abstract syntax tree node types.

	The following class attribute is used:

	.. attribute:: title
		:type: str

		Contains a human readable name for the AST type.

	Instance attributes are:

	.. attribute:: nodetype
		:type: NodeType

		Type of the node. There's a one-to-one correspondence between :class:`AST`
		subclasses and :class:`NodeType` values (except for intermediate classes
		like :class:`BinaryAST`)

	.. attribute:: nodevalue
		:type: str

		The node value is an instance attribute that represents a string that
		isn't represented by any child node. E.g. the values of constants or
		the names of functions, methods and attributes. Will be overwritten by
		properties in subclasses.

	.. attribute:: datatype
		:type: DataType | None

		The datatype is an instance attribute that represents the datatype of the
		expression.

		If the datatype can't be determined because of errors `datatype` will be `None`.
	"""

	nodetype = None

	nodevalue = None

	datatype = None

	title = None

	rules = None

	def __init__(self, *content: AST | str):
		"""
		Create a new :class:`!AST` node from its content.

		``content`` is a mix of :class:`str` objects containing the UL4 source
		and child :class:`!AST` nodes.

		Normally the user doesn't call :meth:`!__init__` directly, but uses
		:meth:`make` to create the appropriate :class:`!AST` node from child
		nodes.

		For example a function call to the function ``date`` could be created
		like this::

			FuncAST(
				"date",
				"(",
				IntAST("2000", 2000),
				", ",
				IntAST("2", 2),
				", ",
				IntAST("29", 29),
				")",
			)

		but more conveniently like this::

			FuncAST.make(
				"date",
				ConstAST.make(2000),
				ConstAST.make(2),
				ConstAST.make(29),
			)
		"""
		final_content = []
		for item in content:
			if isinstance(item, str):
				if item: # Ignore empty strings
					if final_content and isinstance(final_content[-1], str):
						# Merge string with previous string
						final_content[-1] += item
					else:
						final_content.append(item)
			elif isinstance(item, AST):
				final_content.append(item)
			elif item is not None:
				raise TypeError(item)
		self.error = None
		self.content = final_content

	@classmethod
	@abc.abstractmethod
	def make(cls) -> AST:
		"""
		Create an instance of this AST class from its child AST nodes.

		This method is abstract and is overwritten in each subclass.

		This is a very low level way of creating vSQL expressions.

		For example a vSQL expression for
		``"foo".lower() + "bar".upper()`` can be constructed like this::

			vsql.AddAST.make(
				vsql.MethAST.make(
					vsql.StrAST.make("foo"),
					"lower",
				),
				vsql.MethAST.make(
					vsql.StrAST.make("bar"),
					"upper",
				),
			)
		"""

	@classmethod
	def fromul4(cls, node:ul4c.AST, **vars: Field) -> AST:
		try:
			vsqltype = _ul42vsql[type(node)]
		except KeyError:
			pass
		else:
			return vsqltype.fromul4(node, **vars)

		if isinstance(node, ul4c.VarAST):
			field = vars.get(node.name, None)
			return FieldRefAST(None, node.name, field, *cls._make_content_from_ul4(node))
		elif isinstance(node, ul4c.AttrAST):
			obj = cls.fromul4(node.obj, **vars)
			if isinstance(obj, FieldRefAST) and isinstance(obj.field, Field) and obj.field.refgroup:
				try:
					field = obj.field.refgroup[node.attrname]
				except KeyError:
					pass # Fall through to return a generic :class:`AttrAST` node
				else:
					return FieldRefAST(
						obj,
						node.attrname,
						field,
						*cls._make_content_from_ul4(node, node.obj, obj)
					)
			return AttrAST(
				obj,
				node.attrname,
				*cls._make_content_from_ul4(node, node.obj, obj),
			)
		elif isinstance(node, ul4c.CallAST):
			obj = cls.fromul4(node.obj, **vars)

			content = [*obj.content]
			callargs = []

			if isinstance(obj, FieldRefAST):
				if obj.parent is not None:
					asttype = MethAST
					args = (obj.parent, obj.identifier)
				else:
					asttype = FuncAST
					args = (obj.identifier,)
			elif isinstance(obj, AttrAST):
				asttype = MethAST
				args = (obj.obj, obj.attrname)

			for arg in node.args:
				if not isinstance(arg, ul4c.PositionalArgumentAST):
					raise TypeError(f"Can't compile UL4 expression of type {misc.format_class(arg)}!")
				content.append(arg.value)
				arg = AST.fromul4(arg.value, **vars)
				content.append(arg)
				callargs.append(arg)

			return asttype(
				*args,
				callargs,
				*cls._make_content_from_ul4(node, *content),
			)
		raise TypeError(f"Can't compile UL4 expression of type {misc.format_class(node)}!")

	@classmethod
	def fromsource(cls, source:str, **vars: Field) -> AST:
		"""
		Create a vSQL expression from it source code.

		For example ``"foo".lower() + "bar".upper()`` can be compiled like this::

			vsql.AST.fromsource("'foo'.lower() + 'bar'.upper()")

		``vars`` contains the "root" variables that can be referenced in
		the vSQL expression.
		"""
		template = ul4c.Template(f"<?return {source}?>")
		expr = template.content[-1].obj
		return cls.fromul4(expr, **vars)

	def sqlsource(self, query:Query) -> templatelib.Template:
		sqlsource = self._sqlsource(query)
		return flatten_tstring(sqlsource)

	def fieldrefs(self) -> Generator[FieldRefAST, None, None]:
		"""
		Return all :class:`FieldRefAST` objects in this :class:`!AST`.

		This is a generator.
		"""
		for child in self.children():
			yield from child.fieldrefs()

	@classmethod
	def all_types(cls) -> Generator[Type[AST], None, None]:
		"""
		Return this class and all subclasses.

		This is a generator.
		"""
		yield cls
		for subcls in cls.__subclasses__():
			yield from subcls.all_types()

	@classmethod
	def all_rules(cls) -> Generator[Rule, None, None]:
		"""
		Return all grammar rules of this class and all its subclasses.

		This is a generator.
		"""
		for subcls in cls.all_types():
			if subcls.rules is not None:
				yield from subcls.rules.values()

	@classmethod
	def _add_rule(cls, rule:Rule) -> None:
		cls.rules[rule.key] = rule

	@classmethod
	def typeref(cls, s:str | DataType) -> int | None:
		if isinstance(s, str) and s.startswith("T") and s[1:].isdigit():
			return int(s[1:])
		return None

	@classmethod
	def _specs(cls, spectemplate:templatelib.Template) -> Generator[tuple[DataType | str, ...], None, None]:
		# Find position of potential name in the spec, so we can correct
		# the typeref offsets later.
		for (i, v) in enumerate(spectemplate.values):
			if isinstance(v, str) and not v[0].isupper():
				namepos = i
				name = v
				break
		else:
			namepos = len(spectemplate.values)
			name = None

		specs = tuple(v if isinstance(v, set | list | tuple) else (v,) for v in spectemplate.values)

		for spec in itertools.product(*specs):
			newspec = list(spec)
			for (i, type) in enumerate(spec):
				typeref = cls.typeref(type)
				if typeref:
					# Fetch reference type (and correct offset if there's a name in ``spec`` before)
					type = spec[typeref+1 if typeref >= namepos else typeref]
					if cls.typeref(type):
						raise ValueError("typeref to typeref")
				newspec[i] = type

			yield tuple(newspec)

	@classmethod
	def add_rules(cls, spectemplate:templatelib.Template, source:templatelib.Template) -> None:
		"""
		Register new syntax rules for this AST class.

		These rules are used for type checking and type inference and for
		converting the vSQL AST into SQL source code.

		Both arguments are template strings (t-strings). The arguments
		``spectemplate`` and ``source`` have the following meaning:

		``spectemplate``
			``spectemplate`` specifies the allowed combinations of operand types and
			the resulting type. Only the interpolations are used; the literal text is
			ignored (but can be used to make the rule clearer). Each interpolation
			is one of the following:

			Datatypes
				A datatype is given by interpolating the appropriate :class:`DataType`
				member directly (e.g. ``{dt.INT}`` or ``{dt.STR}``, where ``dt`` is an
				alias for :class:`DataType`). A string like ``{'T1'}`` refers to
				another type in the spec.

			Union types
				A set, list or tuple of :class:`DataType` members (e.g.
				``{(dt.BOOL, dt.INT)}``) specifies a union type, i.e. any of the
				types in the collection is allowed. Some predefined unions are
				available as module level variables (e.g. ``{INTLIKE}`` or
				``{NUMBERLIKE}``).

			Names
				The name of a function, method or attribute is given as a (lowercase)
				string constant (e.g. ``{'year'}``).

			The first interpolation in the rule always is the result type.

			Examples:

			``t"{dt.INT} <- {dt.BOOL} + {dt.BOOL}"``
				Adding this rule to :class:`AddAST` specifies that the types ``BOOL``
				and ``BOOL`` can be added and the resulting type is ``INT``. Note
				that using ``+`` is only syntactic sugar. This rule could also have
				been written as ``t"{dt.INT} {dt.BOOL} {dt.BOOL}"`` or even as
				``t"{dt.INT}?????{dt.BOOL}#$%^&*{dt.BOOL}"``.

			``t"{dt.INT} <- {(dt.BOOL, dt.INT)} + {(dt.BOOL, dt.INT)}"``
				This is equivalent to the four rules:
				``t"{dt.INT} <- {dt.BOOL} + {dt.BOOL}"``,
				``t"{dt.INT} <- {dt.INT} + {dt.BOOL}"``,
				``t"{dt.INT} <- {dt.BOOL} + {dt.INT}"`` and
				``t"{dt.INT} <- {dt.INT} + {dt.INT}"``.

			``t"{'T1'} <- {(dt.BOOL, dt.INT)} + {'T1'}"``
				This is equivalent to the two rules
				``t"{dt.BOOL} <- {dt.BOOL} + {dt.BOOL}"`` and
				``t"{dt.INT} <- {dt.INT} + {dt.INT}"``.

			Note that each rule will only be registered once. So the following
			code::

				AddAST.add_rules(
					t"{dt.INT} <- {(dt.BOOL, dt.INT)} + {(dt.BOOL, dt.INT)}",
					t"..."
				)
				AddAST.add_rules(
					t"{dt.NUMBER} <- {(dt.BOOL, dt.INT, dt.NUMBER)} + {(dt.BOOL, dt.INT, dt.NUMBER)}",
					t"..."
				)

			will register the rule ``t"{dt.INT} <- {dt.BOOL} + {dt.BOOL}"``, but not
			``t"{dt.NUMBER} <- {dt.BOOL} + {dt.BOOL}"`` since the first call already
			registered a rule for the signature ``BOOL BOOL``.

		``source``
			``source`` specifies the SQL source that will be generated for this
			expression. Two types of interpolations are supported: ``{'s1'}`` means
			"embed the source code of the first operand in this spot" (and ``{'s2'}``
			etc. accordingly) and ``{'t1'}`` embeds the type name (in lowercase) in
			this spot (and ``{'t2'}`` etc. accordingly).

			Example 1::

				AttrAST.add_rules(
					t"{dt.INT} <- {dt.DATE}.{'year'}",
					t"extract(year from {'s1'})"
				)

			This specifies that a ``DATE`` value has an attribute ``year`` and that
			for such a value ``value`` the generated SQL source code will be:

			.. sourcecode:: sql

				extract(year from value)

			Example 2::

				EQAST.add_rules(
					t"{dt.BOOL} <- {(dt.STR, dt.CLOB)} == {(dt.STR, dt.CLOB)}",
					t"vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'})"
				)

			This registers four rules for equality comparison between ``STR`` and
			``CLOB`` objects. The generated SQL source code for comparisons
			between ``STR`` and ``STR`` will be

			.. sourcecode:: sql

				vsqlimpl_pkg.eq_str_str(value1, value2)

			and for ``CLOB``/``CLOB`` comparison it will be

			.. sourcecode:: sql

				vsqlimpl_pkg.eq_clob_clob(value1, value2)
		"""

		for spec in cls._specs(spectemplate):
			key = spec[1:]
			if cls.rules is None:
				cls.rules = {}
			if key not in cls.rules:
				cls._add_rule(Rule(cls, spectemplate, spec, source, None))

	def validate(self) -> None:
		"""
		Validate the content of this AST node.

		If this node turns out to be invalid :meth:`!validate` will set the
		attribute ``datatype`` to ``None`` and ``error`` to the appropriate
		:class:`Error` value.

		If this node turns out to be valid, :meth:`!validate` will set the
		attribute ``error`` to ``None`` and ``datatype`` to the resulting data
		type of this node.
		"""
		pass

	def check_valid(self, context:str | None=None) -> None:
		"""
		Makes sure that ``self`` is valid.

		If ``self`` is invalid an appropriate exception will be raised.

		``context`` should describe the context in which the expression is used.
		E.g. ``"select"`` when used in :meth:`Query.select_vsql` or ``"where"``
		when used in :meth:`Query.where_vsql`.
		"""
		if self.error is not None:
			# Find first child node with a "real" error
			for child in self.walknodes():
				if child.error is not None and child.error is not Error.SUBNODEERROR:
					raise child.error.exception(self, child, context)
			# No child has a "real" error, so raise one for ``self``
			raise self.error.exception(self, self, context)

	def source(self) -> str:
		"""
		Return the UL4/vSQL source code of the AST.
		"""
		return "".join(s for s in self._source())

	def _source(self) -> Generator[str, None, None]:
		for item in self.content:
			if isinstance(item, str):
				yield item
			else:
				yield from item._source()

	def __str__(self) -> str:
		parts = [f"{self.__class__.__module__}.{self.__class__.__qualname__}"]
		if self.datatype is not None:
			parts.append(f"(datatype {self.datatype.name})")
		if self.error is not None:
			parts.append(f"(error {self.error.name})")
		parts.append(f": {self.source()}")
		return "".join(parts)

	def _ll_repr_(self) -> Generator[str, None, None]:
		if self.datatype is not None:
			yield f"datatype={self.datatype.name}"
		if self.error is not None:
			yield f"error={self.error.name}"
		yield f"source={self.source()!r}"

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		if self.datatype is not None:
			p.breakable()
			p.text(f"datatype={self.datatype.name}")
		if self.error is not None:
			p.breakable()
			p.text(f"error={self.error.name}")
		p.breakable()
		p.text("source=")
		p.pretty(self.source())

	@classmethod
	def _wrap(cls, obj:AST | str, cond:bool) -> Generator[AST | str, None, None]:
		if cond:
			yield "("
		yield obj
		if cond:
			yield ")"

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		encoder.dump(self._source)
		encoder.dump(self.pos)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		self._source = decoder.load()
		self.pos = decoder.load()

	@classmethod
	def _make_content_from_ul4(cls, node:ul4c.AST, *args:ul4c.AST | AST | str | None) -> tuple[AST | str, ...]:
		content = []
		lastpos = node.pos.start
		for subnode in args:
			if isinstance(subnode, AST):
				content.append(subnode)
				lastpos += len(subnode.source())
			elif isinstance(subnode, ul4c.AST):
				if lastpos != subnode.pos.start:
					content.append(node.fullsource[lastpos:subnode.pos.start])
					lastpos = subnode.pos.start
			elif isinstance(subnode, str):
				content.append(subnode)
				lastpos += len(subnode)
		if lastpos != node.pos.stop:
			content.append(node.fullsource[lastpos:node.pos.stop])
		return content

	def children(self) -> Generator[AST, None, None]:
		"""
		Return the child AST nodes of this node.
		"""
		yield from ()

	def walknodes(self) -> Generator[AST, None, None]:
		"""
		Return the all child AST nodes of this node (recursively).
		"""
		for child in self.children():
			yield child
			yield from child.walknodes()

	def walkpaths(self) -> Generator[list[AST], None, None]:
		"""
		Return an iterator for traversing the syntax tree rooted at ``self``.

		Items produced by the iterator paths are lists containing the path
		from the root :class:`AST` object to ``self``.

		Note that the iterator will always produce the same list object that will
		be changed during the iteration. If you want to keep the value produced
		during the iteration, you have to make copies.
		"""
		yield from self._walkpaths([])

	def _walkpaths(self, path:list[AST]) -> Generator[list[AST], None, None]:
		path.append(self)
		yield path
		for child in self.children():
			yield from child._walkpaths(path)
		path.pop()


class ConstAST(AST):
	"""
	Base class for all vSQL expressions that are constants.
	"""

	title = "Constant"
	precedence = 20

	@staticmethod
	def make(value:Any) -> ConstAST:
		cls = _consts.get(type(value))
		if cls is None:
			raise TypeError(value)
		elif cls is NoneAST:
			return cls.make()
		else:
			return cls.make(value)

	@classmethod
	def fromul4(cls, node, **vars: Field) -> AST:
		try:
			vsqltype = _consts[type(node.value)]
		except KeyError:
			raise TypeError(f"constant of type {misc.format_class(node.value)} not supported!") from None
		return vsqltype.fromul4(node, **vars)


@ul4on.register("de.livinglogic.vsql.none")
class NoneAST(ConstAST):
	"""
	The constant ``None``.
	"""

	title = "Constant `None`"
	nodetype = NodeType.CONST_NONE
	datatype = DataType.NULL

	@classmethod
	def make(cls) -> NoneAST:
		return cls("None")

	def _sqlsource(self, query:Query) -> templatelib.Template:
		return t"null"

	@classmethod
	def fromul4(cls, node:ul4c.ConstAST, **vars: Field) -> AST:
		return cls(node.source)


class _ConstWithValueAST(ConstAST):
	"""
	Base class for all vSQL constants taht may have different values.

	(i.e. anything except ``None``).
	"""

	def __init__(self, value, *content):
		super().__init__(*content)
		self.value = value

	@classmethod
	def make(cls, value:Any) -> ConstAST:
		return cls(value, ul4c._repr(value))

	@classmethod
	def fromul4(cls, node:ul4c.ConstAST, **vars: Field) -> ConstAST:
		return cls(node.value, node.source)

	@property
	def nodevalue(self) -> str:
		return self.value

	def _ll_repr_(self) -> Generator[str, None, None]:
		yield from super()._ll_repr_()
		yield f"value={self.value!r}"

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		super()._ll_repr_pretty_(p)
		p.breakable()
		p.text("value=")
		p.pretty(self.value)

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		super().ul4onload(decoder)
		self.value = decoder.load()


@ul4on.register("de.livinglogic.vsql.bool")
class BoolAST(_ConstWithValueAST):
	"""
	A boolean constant (i.e. ``True`` or ``False``).
	"""

	title = "Boolean constant"
	nodetype = NodeType.CONST_BOOL
	datatype = DataType.BOOL

	@classmethod
	def make(cls, value:Any) -> BoolAST:
		return cls(value, "True" if value else "False")

	def _sqlsource(self, query:Query) -> templatelib.Template:
		return t"1" if self.value else t"0"

	@property
	def nodevalue(self) -> str:
		return "True" if self.value else "False"


@ul4on.register("de.livinglogic.vsql.int")
class IntAST(_ConstWithValueAST):
	"""
	An integer constant.
	"""

	title = "Integer constant"
	nodetype = NodeType.CONST_INT
	datatype = DataType.INT

	def _sqlsource(self, query:Query) -> templatelib.Template:
		return t"{self.value:l}"

	@property
	def nodevalue(self) -> str:
		return str(self.value)


@ul4on.register("de.livinglogic.vsql.number")
class NumberAST(_ConstWithValueAST):
	"""
	A number constant (containing a decimal point).
	"""

	title = "Number constant"
	nodetype = NodeType.CONST_NUMBER
	datatype = DataType.NUMBER

	def _sqlsource(self, query:Query) -> templatelib.Template:
		return t"{repr(self.value):l}"

	@property
	def nodevalue(self) -> str:
		return repr(self.value)


@ul4on.register("de.livinglogic.vsql.str")
class StrAST(_ConstWithValueAST):
	"""
	A string constant.
	"""

	title = "String constant"
	nodetype = NodeType.CONST_STR
	datatype = DataType.STR

	def _sqlsource(self, query:Query) -> templatelib.Template:
		s = self.value.replace("'", "''")
		return t"'{s:l}'"


@ul4on.register("de.livinglogic.vsql.clob")
class CLOBAST(_ConstWithValueAST):
	"""
	A CLOB constant.

	This normally will not be created by the Python implementation
	"""

	title = "CLOB constant"
	nodetype = NodeType.CONST_CLOB
	datatype = DataType.CLOB

	def _sqlsource(self, query:Query) -> templatelib.Template:
		s = self.value.replace("'", "''")
		return t"'{s}'"


@ul4on.register("de.livinglogic.vsql.color")
class ColorAST(_ConstWithValueAST):
	"""
	A color constant (e.g. ``#fff``).
	"""

	title = "Color constant"
	nodetype = NodeType.CONST_COLOR
	datatype = DataType.COLOR

	def _sqlsource(self, query:Query) -> templatelib.Template:
		c = self.value
		c = str((c.r() << 24) + (c.g() << 16) + (c.b() << 8) + c.a())
		return t"{c:l}"

	@property
	def nodevalue(self) -> str:
		c = self.value
		return f"{c.r():02x}{c.g():02x}{c.b():02x}{c.a():02x}"


@ul4on.register("de.livinglogic.vsql.date")
class DateAST(_ConstWithValueAST):
	"""
	A date constant (e.g. ``@(2000-02-29)``).
	"""

	title = "Date constant"
	nodetype = NodeType.CONST_DATE
	datatype = DataType.DATE

	def _sqlsource(self, query:Query) -> templatelib.Template:
		s = f"to_date('{self.value:%Y-%m-%d}', 'YYYY-MM-DD')"
		return t"{s:l}"

	@property
	def nodevalue(self) -> str:
		return f"{self.value:%Y-%m-%d}"


@ul4on.register("de.livinglogic.vsql.datetime")
class DateTimeAST(_ConstWithValueAST):
	"""
	A datetime constant (e.g. ``@(2000-02-29T12:34:56)``).
	"""

	title = "Datetime constant"
	nodetype = NodeType.CONST_DATETIME
	datatype = DataType.DATETIME

	@classmethod
	def make(cls, value:datetime.datetime) -> DateTimeAST:
		value = value.replace(microsecond=0)
		return cls(value, ul4c._repr(value))

	def _sqlsource(self, query:Query) -> templatelib.Template:
		s = f"to_date('{self.value:%Y-%m-%d %H:%M:%S}', 'YYYY-MM-DD HH24:MI:SS')";
		return t"{s:l}"

	@property
	def nodevalue(self) -> str:
		return f"{self.value:%Y-%m-%dT%H:%M:%S}"


class _SeqAST(AST):
	"""
	Base class of :class:`ListAST` and :class:`SetAST`.
	"""

	def __init__(self, *content:AST | str):
		super().__init__(*content)
		self.items = [item for item in content if isinstance(item, AST)]
		self.datatype = None
		self.validate()

	@classmethod
	def fromul4(cls, node:ul4c.AST, **vars: Field) -> AST:
		content = []

		lastpos = None # This value is never used
		for item in node.items:
			if not isinstance(item, ul4c.SeqItemAST):
				raise TypeError(f"Can't compile UL4 expression of type {misc.format_class(item)}!")
			content.append(item.value)
			content.append(AST.fromul4(item.value, **vars))
		return cls(*cls._make_content_from_ul4(node, *content))

	def _sqlsource(self, query:Query) -> templatelib.Template:
		if self.datatype is self.nulltype:
			return t"{self.nodevalue:l}"
		else:
			(prefix, suffix) = self.sqltypes[self.datatype]
			result = t"{prefix:l}"
			for (i, item) in enumerate(self.items):
				if i:
					result += t", "
				result += item._sqlsource(query)
			result += t"{suffix:l}"
			return result

	def _ll_repr_(self) -> Generator[str, None, None]:
		yield from super()._ll_repr_()
		yield f"with {len(self.items):,} items"

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		super()._ll_repr_pretty_(p)
		for item in self.items:
			p.breakable()
			p.pretty(item)

	def children(self) -> Generator[AST, None, None]:
		yield from self.items

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		super().ul4onload(decoder)
		self.items = decoder.load()


@ul4on.register("de.livinglogic.vsql.list")
class ListAST(_SeqAST):
	"""
	A list constant.

	For this to work the list may only contain items of "compatible" types, i.e.
	types that con be converted to a common type without losing information.
	"""

	title = "List"
	nodetype = NodeType.LIST
	nulltype = DataType.NULLLIST
	precedence = 20

	sqltypes = {
		DataType.INTLIST: ("integers(", ")"),
		DataType.NUMBERLIST: ("numbers(", ")"),
		DataType.STRLIST: ("varchars(", ")"),
		DataType.CLOBLIST: ("clobs(", ")"),
		DataType.DATELIST: ("dates(", ")"),
		DataType.DATETIMELIST: ("dates(", ")"),
	}

	def __init__(self, *content:AST | str):
		super().__init__(*content)
		self.validate()

	@classmethod
	def make(cls, *items:AST) -> ListAST:
		if items:
			content = []
			for (i, item) in enumerate(items):
				content.append(", " if i else "[")
				content.append(item)
			content.append("]")
			return cls(*content)
		else:
			return cls("[]")

	valid_item_types = {
		frozenset(): DataType.NULLLIST,
		frozenset({DataType.INT}): DataType.INTLIST,
		frozenset({DataType.NUMBER}): DataType.NUMBERLIST,
		frozenset({DataType.STR}): DataType.STRLIST,
		frozenset({DataType.CLOB}): DataType.CLOBLIST,
		frozenset({DataType.DATE}): DataType.DATELIST,
		frozenset({DataType.DATETIME}): DataType.DATETIMELIST,
		frozenset({DataType.INT, DataType.NUMBER}): DataType.NUMBERLIST,
		frozenset({DataType.STR, DataType.CLOB}): DataType.CLOBLIST,
	}

	def validate(self) -> None:
		if any(item.error for item in self.items):
			self.error = Error.SUBNODEERROR
			self.datatype = None
		else:
			types = {item.datatype for item in self.items}
			if DataType.NULL in types:
				types.remove(DataType.NULL)
			try:
				self.datatype = self.valid_item_types[frozenset(types)]
			except KeyError:
				self.datatype = None
				self.error = Error.LISTUNSUPPORTEDTYPES
			else:
				self.error = None

	@property
	def nodevalue(self) -> str:
		return str(len(self.items)) if self.datatype is DataType.NULLLIST else None


@ul4on.register("de.livinglogic.vsql.set")
class SetAST(_SeqAST):
	"""
	A set constant.

	For this to work the set may only contain items of "compatible" types, i.e.
	types that can be converted to a common type without losing information.
	"""

	title = "Set"
	nodetype = NodeType.SET
	nulltype = DataType.NULLSET
	precedence = 20

	sqltypes = {
		DataType.INTSET: ("vsqlimpl_pkg.set_intlist(integers(", "))"),
		DataType.NUMBERSET: ("vsqlimpl_pkg.set_numberlist(numbers(", "))"),
		DataType.STRSET: ("vsqlimpl_pkg.set_strlist(varchars(", "))"),
		DataType.DATESET: ("vsqlimpl_pkg.set_datetimelist(dates(", "))"),
		DataType.DATETIMESET: ("vsqlimpl_pkg.set_datetimelist(dates(", "))"),
	}

	def __init__(self, *content:AST | str):
		super().__init__(*content)
		self.validate()

	@classmethod
	def make(cls, *items:AST) -> SetAST:
		if items:
			content = []
			for (i, item) in enumerate(items):
				content.append(", " if i else "{")
				content.append(item)
			content.append("}")
			return cls(*content)
		else:
			return cls("{/}")

	def validate(self) -> None:
		if any(item.error for item in self.items):
			self.error = Error.SUBNODEERROR
			self.datatype = None
		else:
			types = {item.datatype for item in self.items}
			if DataType.NULL in types:
				types.remove(DataType.NULL)
			if not types:
				self.error = None
				self.datatype = DataType.NULLSET
			elif len(types) == 1:
				self.error = None
				datatype = misc.first(types)
				if datatype is DataType.INT:
					datatype = DataType.INTSET
				elif datatype is DataType.NUMBER:
					datatype = DataType.NUMBERSET
				elif datatype is DataType.STR:
					datatype = DataType.STRSET
				elif datatype is DataType.DATE:
					datatype = DataType.DATESET
				elif datatype is DataType.DATETIME:
					datatype = DataType.DATETIMESET
				else:
					datatype = None
				self.datatype = datatype
				self.error = None if datatype else Error.SETUNSUPPORTEDTYPES
			else:
				self.error = Error.SETMIXEDTYPES
				self.datatype = None

	@property
	def nodevalue(self) -> str:
		return str(len(self.items)) if self.datatype is DataType.NULLSET else None


@ul4on.register("de.livinglogic.vsql.fieldref")
class FieldRefAST(AST):
	"""
	Reference to a field defined in the database.
	"""

	title = "Field reference"
	nodetype = NodeType.FIELD
	precedence = 19

	def __init__(self, parent:FieldRefAST | None, identifier:str, field:Field | None, *content:AST | str):
		"""
		Create a :class:`FieldRef` object.

		There are three possible scenarios with respect to ``identifier`` and
		``field``:

		``field is not None and field.identifier == identifier``
			In this case we have a valid :class:`Field` that describes a real
			field.

		``field is not None and field.identifier != identifier and field.identifier == "*"``
			In this case :obj:`field` is the :class:`Field` object for the generic
			typed request parameters. E.g. when the vSQL expression is
			``params.str.foo`` then :obj:`field` references the :class:`Field` for
			``params.str.*``, so ``field.identifier == "*" and
			identifier == "foo"``.

		``field is None``
			In this case the field is unknown.
		"""
		super().__init__(*content)
		self.parent = parent
		# Note that ``identifier`` might be different from ``field.identifier``
		# if ``field.identifier == "*"``.
		self.identifier = identifier
		# Note that ``field`` might be ``None`` when the field can't be found.
		self.field = field
		self.validate()

	@classmethod
	def make_root(cls, field:str | Field) -> FieldRefAST:
		if isinstance(field, str):
			# This is an invalid field reference
			return FieldRefAST(None, field, None, field)
		else:
			return FieldRefAST(None, field.identifier, field, field.identifier)

	@classmethod
	def make(cls, parent:FieldRefAST, identifier:str) -> FieldRefAST:
		result_field = None
		parent_field = parent.field
		if parent_field is not None:
			group = parent_field.refgroup
			if group is not None:
				try:
					result_field = group[identifier]
				except KeyError:
					pass

		return FieldRefAST(parent, identifier, result_field, parent, ".", identifier)

	def _sqlsource(self, query:Query) -> templatelib.Template:
		# FIXME
		alias = query._register(self)
		full_identifier = self.full_identifier
		if full_identifier.startswith("params."):
			# If the innermost field is "params" we need special treatment
			s = f"livingapi_pkg.reqparam_{self.parent.identifier}('{self.identifier}') /* {self.source()} */"
			return t"{s:l}"
		elif alias is None:
			return t"{self.field.fieldsql:l} {format_comment(self.source()):l}"
		else:
			fieldsql = tstring_replace(self.field.fieldsql, "{a}", alias)
			return t"{fieldsql:l} {format_comment(self.source()):l}"

	def validate(self) -> None:
		self.error = Error.FIELD if self.field is None else None

	@property
	def datatype(self) -> DataType | None:
		return self.field.datatype if self.field is not None else None

	@property
	def nodevalue(self) -> str:
		identifierpath = []
		node = self
		while node is not None:
			identifierpath.insert(0, node.identifier)
			node = node.parent
		return ".".join(identifierpath)

	def fieldrefs(self) -> Generator[FieldRefAST, None, None]:
		yield self
		yield from super().fieldrefs()

	@property
	def full_identifier(self) -> str:
		if self.parent is None:
			return self.identifier
		else:
			return f"{self.parent.full_identifier}.{self.identifier}"

	def _ll_repr_(self) -> Generator[str, None, None]:
		yield from super()._ll_repr_()
		if self.field is None or self.field.identifier != self.identifier:
			yield f"identifier={self.identifier!r}"
		if self.field is not None:
			yield f"field={self.field!r}"

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		super()._ll_repr_pretty_(p)
		p.breakable()
		p.text("identifier=")
		p.pretty(self.identifier)
		if self.field is None or self.field.identifier != self.identifier:
			p.breakable()
			p.text("identifier=")
			p.pretty(self.identifier)
		if self.field is not None:
			p.breakable()
			p.text("field=")
			p.pretty(self.field)

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		super().ul4ondump(encoder)
		encoder.dump(self.parent)
		encoder.dump(self.identifier)
		encoder.dump(self.field)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		super().ul4onload(decoder)
		self.parent = decoder.load()
		self.identifier = decoder.load()
		self.field = decoder.load()


class BinaryAST(AST):
	"""
	Base class of all binary expressions (i.e. expressions with two operands).
	"""

	title = "Binary operation"

	def __init__(self, obj1:AST, obj2:AST, *content:AST | str):
		super().__init__(*content)
		self.obj1 = obj1
		self.obj2 = obj2
		self.datatype = None
		self.validate()

	@classmethod
	def make(cls, obj1:AST, obj2:AST) -> BinaryAST:
		return cls(
			obj1,
			obj2,
			*cls._wrap(obj1, obj1.precedence < cls.precedence),
			f" {cls.operator} ",
			*cls._wrap(obj2, obj2.precedence <= cls.precedence),
		)

	def validate(self) -> None:
		if self.obj1.error or self.obj2.error:
			self.error = Error.SUBNODEERROR
		signature = (self.obj1.datatype, self.obj2.datatype)
		try:
			rule = self.rules[signature]
		except KeyError:
			self.error = Error.SUBNODETYPES
			self.datatype = None
		else:
			self.error = None
			self.datatype = rule.result

	@classmethod
	def fromul4(cls, node:ul4c.BinaryAST, **vars: Field) -> AST:
		obj1 = AST.fromul4(node.obj1, **vars)
		obj2 = AST.fromul4(node.obj2, **vars)
		return cls(
			obj1,
			obj2,
			*cls._make_content_from_ul4(node, node.obj1, obj1, node.obj2, obj2),
		)

	def _sqlsource(self, query:Query) -> templatelib.Template:
		rule = self.rules[(self.obj1.datatype, self.obj2.datatype)]
		result = t""
		for child in rule.source:
			if child == 1:
				result += self.obj1._sqlsource(query)
			elif child == 2:
				result += self.obj2._sqlsource(query)
			else:
				result += to_tstring(child)
		return result

	def children(self) -> Generator[AST, None, None]:
		yield self.obj1
		yield self.obj2

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		super()._ll_repr_pretty_(p)
		p.breakable()
		p.text("obj1=")
		p.pretty(self.obj1)
		p.breakable()
		p.text("obj2=")
		p.pretty(self.obj2)

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		super().ul4ondump(encoder)
		encoder.dump(self.obj1)
		encoder.dump(self.obj2)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		super().ul4onload(decoder)
		self.obj1 = decoder.load()
		self.obj2 = decoder.load()


@ul4on.register("de.livinglogic.vsql.eq")
class EQAST(BinaryAST):
	"""
	Equality comparison (``A == B``).
	"""

	title = "Equality comparison (`A == B`)"
	nodetype = NodeType.CMP_EQ
	precedence = 6
	operator = "=="


@ul4on.register("de.livinglogic.vsql.ne")
class NEAST(BinaryAST):
	"""
	Inequality comparison (``A != B``).
	"""

	title = "Inequality comparison (`A != B`)"
	nodetype = NodeType.CMP_NE
	precedence = 6
	operator = "!="


@ul4on.register("de.livinglogic.vsql.lt")
class LTAST(BinaryAST):
	"""
	Less-than comparison (``A < B``).
	"""

	title = "Less-than comparison (`A < B`)"
	nodetype = NodeType.CMP_LT
	precedence = 6
	operator = "<"


@ul4on.register("de.livinglogic.vsql.le")
class LEAST(BinaryAST):
	"""
	Less-than or equal comparison (``A <= B``).
	"""

	title = "Less-than or equal comparison (`A <= B`)"
	nodetype = NodeType.CMP_LE
	precedence = 6
	operator = "<="


@ul4on.register("de.livinglogic.vsql.gt")
class GTAST(BinaryAST):
	"""
	Greater-than comparison (``A > B``).
	"""

	title = "Greater-than comparison (`A > B`)"
	nodetype = NodeType.CMP_GT
	precedence = 6
	operator = ">"


@ul4on.register("de.livinglogic.vsql.ge")
class GEAST(BinaryAST):
	"""
	Greater-than-or equal comparison (``A >= B``).
	"""

	title = "Greater-than or equal comparison (`A >= B`)"
	nodetype = NodeType.CMP_GE
	precedence = 6
	operator = ">="


@ul4on.register("de.livinglogic.vsql.add")
class AddAST(BinaryAST):
	"""
	Addition (``A + B``).
	"""

	title = "Addition (`A + B`)"
	nodetype = NodeType.BINOP_ADD
	precedence = 11
	operator = "+"


@ul4on.register("de.livinglogic.vsql.sub")
class SubAST(BinaryAST):
	"""
	Subtraction (``A - B``).
	"""

	title = "Subtraction (`A - B`)"
	nodetype = NodeType.BINOP_SUB
	precedence = 11
	operator = "-"


@ul4on.register("de.livinglogic.vsql.mul")
class MulAST(BinaryAST):
	"""
	Multiplication (``A * B``).
	"""

	title = "Multiplication (`A * B`)"
	nodetype = NodeType.BINOP_MUL
	precedence = 12
	operator = "*"


@ul4on.register("de.livinglogic.vsql.truediv")
class TrueDivAST(BinaryAST):
	"""
	True division (``A / B``).
	"""

	title = "True division (`A / B`)"
	nodetype = NodeType.BINOP_TRUEDIV
	precedence = 12
	operator = "/"


@ul4on.register("de.livinglogic.vsql.floordiv")
class FloorDivAST(BinaryAST):
	"""
	Floor division (``A // B``).
	"""

	title = "Floor division (`A // B`)"
	nodetype = NodeType.BINOP_FLOORDIV
	precedence = 12
	operator = "//"


@ul4on.register("de.livinglogic.vsql.mod")
class ModAST(BinaryAST):
	"""
	Modulo operator (``A % B``).
	"""

	title = "Modulo operation (`A % B`)"
	nodetype = NodeType.BINOP_MOD
	precedence = 12
	operator = "%"


@ul4on.register("de.livinglogic.vsql.shiftleft")
class ShiftLeftAST(BinaryAST):
	"""
	Left shift operator (``A << B``).
	"""

	title = "Left shift operation (`A << B`)"
	nodetype = NodeType.BINOP_SHIFTLEFT
	precedence = 10
	operator = "<<"


@ul4on.register("de.livinglogic.vsql.shiftright")
class ShiftRightAST(BinaryAST):
	"""
	Right shift operator (``A >> B``).
	"""

	title = "Right shift operation (`A >> B`)"
	nodetype = NodeType.BINOP_SHIFTRIGHT
	precedence = 10
	operator = ">>"


@ul4on.register("de.livinglogic.vsql.and")
class AndAST(BinaryAST):
	"""
	Logical "and" (``A and B``).
	"""

	title = 'Logical "and" operation (`A and B`)'
	nodetype = NodeType.BINOP_AND
	precedence = 4
	operator = "and"


@ul4on.register("de.livinglogic.vsql.or")
class OrAST(BinaryAST):
	"""
	Logical "or" (``A or B``).
	"""

	title = 'Logical "or" operation (`A or B`)'
	nodetype = NodeType.BINOP_OR
	precedence = 4
	operator = "or"


@ul4on.register("de.livinglogic.vsql.contains")
class ContainsAST(BinaryAST):
	"""
	Containment test (``A in B``).
	"""

	title = "Containment test (`A in B`)"
	nodetype = NodeType.BINOP_CONTAINS
	precedence = 6
	operator = "in"


@ul4on.register("de.livinglogic.vsql.notcontains")
class NotContainsAST(BinaryAST):
	"""
	Inverted containment test (``A not in B``).
	"""

	title = "Inverted containment test (`A not in B`)"
	nodetype = NodeType.BINOP_NOTCONTAINS
	precedence = 6
	operator = "not in"


@ul4on.register("de.livinglogic.vsql.is")
class IsAST(BinaryAST):
	"""
	Identity test (``A is B``).
	"""

	title = "Identity test (`A is B`)"
	nodetype = NodeType.BINOP_IS
	precedence = 6
	operator = "is"


@ul4on.register("de.livinglogic.vsql.isnot")
class IsNotAST(BinaryAST):
	"""
	Inverted identity test (``A is not B``).
	"""

	title = "Inverted identity test (`A is not B`)"
	nodetype = NodeType.BINOP_ISNOT
	precedence = 6
	operator = "is not"


@ul4on.register("de.livinglogic.vsql.item")
class ItemAST(BinaryAST):
	"""
	Item access operator (``A[B]``).
	"""

	title = "Item access operation (`A[B]`)"
	nodetype = NodeType.BINOP_ITEM
	precedence = 16

	@classmethod
	def make(self, obj1:AST, obj2:AST) -> ItemAST:
		if obj1.precedence >= self.precedence:
			return cls(obj1, obj2, obj1, "[", obj2, "]")
		else:
			return cls(obj1, obj2, "(", obj1, ")[", obj2, "]")

	@classmethod
	def fromul4(cls, node:ul4c.ItemAST, **vars: Field) -> AST:
		if isinstance(node.obj2, ul4c.SliceAST):
			return SliceAST.fromul4(node, **vars)
		return super().fromul4(node, **vars)


@ul4on.register("de.livinglogic.vsql.bitand")
class BitAndAST(BinaryAST):
	"""
	Bitwise "and" (``A & B``).
	"""

	title = 'Bitwise "and" operation (`A & B`)'
	nodetype = NodeType.BINOP_BITAND
	precedence = 9
	operator = "&"


@ul4on.register("de.livinglogic.vsql.bitor")
class BitOrAST(BinaryAST):
	"""
	Bitwise "or" (``A | B``).
	"""

	title = 'Bitwise "or" operation (`A | B`)'
	nodetype = NodeType.BINOP_BITOR
	precedence = 7
	operator = "|"


@ul4on.register("de.livinglogic.vsql.bitxor")
class BitXOrAST(BinaryAST):
	"""
	Bitwise "exclusive or" (``A ^ B``).
	"""

	title = 'Bitwise "exclusive or" operation (`A ^ B`)'
	nodetype = NodeType.BINOP_BITXOR
	precedence = 8
	operator = "^"


class UnaryAST(AST):
	"""
	Base class of all unary expressions (i.e. expressions with one operand).
	"""

	title = "Unary operation"

	def __init__(self, obj:AST, *content:AST | str):
		super().__init__(*content)
		self.obj = obj
		self.datatype = None
		self.validate()

	@classmethod
	def make(cls, obj:AST) -> UnaryAST:
		return cls(
			obj,
			cls.operator,
			*cls._wrap(obj, obj.precedence <= cls.precedence),
		)

	@classmethod
	def fromul4(cls, node:ul4c.UnaryAST, **vars: Field) -> AST:
		obj = AST.fromul4(node.obj, **vars)
		return cls(
			obj,
			*cls._make_content_from_ul4(node, node.obj, obj),
		)

	def validate(self) -> None:
		if self.obj.error:
			self.error = Error.SUBNODEERROR
		signature = (self.obj.datatype,)
		try:
			rule = self.rules[signature]
		except KeyError:
			self.error = Error.SUBNODETYPES
			self.datatype = None
		else:
			self.error = None
			self.datatype = rule.result

	def _sqlsource(self, query:Query) -> templatelib.Template:
		rule = self.rules[(self.obj.datatype, )]
		result = t""
		for child in rule.source:
			if child == 1:
				result += self.obj._sqlsource(query)
			else:
				result += to_tstring(child)
		return result

	def children(self) -> Generator[AST, None, None]:
		yield self.obj

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		super()._ll_repr_pretty_(p)
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		super().ul4ondump(encoder)
		encoder.dump(self.obj)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		super().ul4onload(decoder)
		self.obj = decoder.load()


@ul4on.register("de.livinglogic.vsql.not")
class NotAST(UnaryAST):
	"""
	Logical negation (``not A``).
	"""

	title = "Logical negation operation (`not A`)"
	nodetype = NodeType.UNOP_NOT
	precedence = 5
	operator = "not "


@ul4on.register("de.livinglogic.vsql.neg")
class NegAST(UnaryAST):
	"""
	Arithmetic negation (``-A``).
	"""

	title = "Arithmetic negation operation (`-A`)"
	nodetype = NodeType.UNOP_NEG
	precedence = 14
	operator = "-"


@ul4on.register("de.livinglogic.vsql.bitnot")
class BitNotAST(UnaryAST):
	"""
	Bitwise "not" (``~A``).
	"""

	title = 'Bitwise "not" operation (`~A`)'
	nodetype = NodeType.UNOP_BITNOT
	precedence = 14
	operator = "~"


@ul4on.register("de.livinglogic.vsql.if")
class IfAST(AST):
	"""
	Ternary "if"/"else" (``A if COND else B``).
	"""

	title = "if/else operation (`A if COND else B`)"
	nodetype = NodeType.TERNOP_IF
	precedence = 3

	def __init__(self, objif:AST, objcond:AST, objelse:AST, *content:AST | str):
		super().__init__(*content)
		self.objif = objif
		self.objcond = objcond
		self.objelse = objelse
		self.datatype = None
		self.validate()

	@classmethod
	def make(cls, objif:AST, objcond:AST, objelse:AST) -> IfAST:
		return cls(
			objif,
			objcond,
			objelse,
			*cls._wrap(objif, objif.precedence <= cls.precedence),
			" if ",
			*cls._wrap(objcond, objcond.precedence <= cls.precedence),
			" else ",
			*cls._wrap(objelse, objcond.precedence <= cls.precedence),
		)

	def validate(self) -> None:
		if self.objif.error or self.objcond.error or self.objelse.error:
			self.error = Error.SUBNODEERROR
		signature = (self.objif.datatype, self.objcond.datatype, self.objelse.datatype)
		try:
			rule = self.rules[signature]
		except KeyError:
			self.error = Error.SUBNODETYPES
			self.datatype = None
		else:
			self.error = None
			self.datatype = rule.result

	@classmethod
	def fromul4(cls, node:ul4c.IfAST, **vars: Field) -> IfAST:
		objif = AST.fromul4(node.objif, **vars)
		objcond = AST.fromul4(node.objcond, **vars)
		objelse = AST.fromul4(node.objelse, **vars)

		return cls(
			objif,
			objcond,
			objelse,
			*cls._make_content_from_ul4(node, node.objif, objif, node.objcond, objcond, node.objelse, objelse),
		)

	def _sqlsource(self, query:Query) -> templatelib.Template:
		rule = self.rules[(self.objif.datatype, self.objcond.datatype, self.objelse.datatype)]
		result = t""
		for child in rule.source:
			if child == 1:
				result += self.objif._sqlsource(query)
			elif child == 2:
				result += self.objcond._sqlsource(query)
			elif child == 3:
				result += self.objelse._sqlsource(query)
			else:
				result += to_tstring(child)
		return result

	def children(self) -> Generator[AST, None, None]:
		yield self.objif
		yield self.objcond
		yield self.objelse

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		super()._ll_repr_pretty_(p)
		p.breakable()
		p.text("objif=")
		p.pretty(self.objif)
		p.breakable()
		p.text("objcond=")
		p.pretty(self.objcond)
		p.breakable()
		p.text("objelse=")
		p.pretty(self.objelse)

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		super().ul4ondump(encoder)
		encoder.dump(self.objif)
		encoder.dump(self.objcond)
		encoder.dump(self.objelse)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		super().ul4onload(decoder)
		self.objif = decoder.load()
		self.objcond = decoder.load()
		self.objelse = decoder.load()


@ul4on.register("de.livinglogic.vsql.if")
class SliceAST(AST):
	"""
	Slice operator (``A[B:C]``).
	"""

	title = "Slice operation (`A[B:C]`)"
	nodetype = NodeType.TERNOP_SLICE
	precedence = 16

	def __init__(self, obj:AST, index1:AST | None, index2:AST | None, *content:AST | str):
		super().__init__(*content)
		self.obj = obj
		self.index1 = index1
		self.index2 = index2
		self.datatype = None
		self.validate()

	@classmethod
	def make(cls, obj:AST, index1:AST | None, index2:AST | None) -> SliceAST:
		if index1 is None:
			index1 = NoneAST(None)
		if index2 is None:
			index2 = NoneAST(None)

		return cls(
			obj,
			index1,
			index2,
			*cls._wrap(obj, obj.precedence < cls.precedence),
			"[",
			index1,
			":",
			index2,
			"]",
		)

	def validate(self) -> None:
		if self.obj.error or self.index1.error or self.index2.error:
			self.error = Error.SUBNODEERROR
		signature = (self.obj.datatype, self.index1.datatype, self.index2.datatype)
		try:
			rule = self.rules[signature]
		except KeyError:
			self.error = Error.SUBNODETYPES
			self.datatype = None
		else:
			self.error = None
			self.datatype = rule.result

	@classmethod
	def fromul4(cls, node:ul4c.ItemAST, **vars: Field) -> AST:
		obj = AST.fromul4(node.obj1, **vars)
		index1 = AST.fromul4(node.obj2.index1, **vars) if node.obj2.index1 is not None else NoneAST("")
		index2 = AST.fromul4(node.obj2.index2, **vars) if node.obj2.index2 is not None else NoneAST("")

		return cls(
			obj,
			index1,
			index2,
			*cls._make_content_from_ul4(node, node.obj1, obj, node.obj2.index1, index1, node.obj2.index2, index2)
		)

	def _sqlsource(self, query:Query) -> templatelib.Template:
		rule = self.rules[(self.obj.datatype, self.index1.datatype, self.index2.datatype)]
		result = t""
		for child in rule.source:
			if child == 1:
				result += self.obj._sqlsource(query)
			elif child == 2:
				result += self.index1._sqlsource(query)
			elif child == 3:
				result += self.index2._sqlsource(query)
			else:
				result += to_tstring(child)
		return result

	def children(self) -> Generator[AST, None, None]:
		yield self.obj
		yield self.index1 if self.index1 is None else NoneAST("")
		yield self.index2 if self.index2 is None else NoneAST("")

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		super()._ll_repr_pretty_(p)
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		if self.index1 is not None:
			p.breakable()
			p.text("index1=")
			p.pretty(self.index1)
		if self.index2 is not None:
			p.breakable()
			p.text("index2=")
			p.pretty(self.index2)

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.index1)
		encoder.dump(self.index1)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.index1 = decoder.load()
		self.index2 = decoder.load()


@ul4on.register("de.livinglogic.vsql.attr")
class AttrAST(AST):
	"""
	Attribute access (``A.name``).
	"""

	title = "Attribute access operation (`A.name`)"
	nodetype = NodeType.ATTR
	precedence = 19

	def __init__(self, obj:AST, attrname:str, *content:AST | str):
		super().__init__(*content)
		self.obj = obj
		self.attrname = attrname
		self.datatype = None
		self.validate()

	@classmethod
	def make(cls, obj:AST, attrname:str) -> AttrAST:
		return cls(
			obj,
			attrname,
			*cls._wrap(obj, obj.precedence < cls.precedence),
			".",
			attrname,
		)

	def validate(self) -> None:
		if self.obj.error:
			self.error = Error.SUBNODEERROR
		signature = (self.obj.datatype, self.attrname)
		try:
			rule = self.rules[signature]
		except KeyError:
			self.error = Error.NAME
			self.datatype = None
		else:
			self.error = None
			self.datatype = rule.result

	def _sqlsource(self, query:Query) -> templatelib.Template:
		rule = self.rules[(self.obj.datatype, self.attrname)]
		result = t""
		for child in rule.source:
			if child == 1:
				result += self.obj._sqlsource(query)
			else:
				result += to_tstring(child)
		return result

	@property
	def nodevalue(self) -> str:
		return self.attrname

	def children(self) -> Generator[AST, None, None]:
		yield self.obj

	def _ll_repr_(self) -> Generator[str, None, None]:
		yield from super()._ll_repr_()
		yield f"attrname={self.attrname!r}"

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		super()._ll_repr_pretty_(p)
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		p.breakable()
		p.text("attrname=")
		p.pretty(self.attrname)

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.attrname)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.attrname = decoder.load()


@ul4on.register("de.livinglogic.vsql.func")
class FuncAST(AST):
	"""
	Function call (``name(A, ...)``).
	"""

	title = "Function call (`name(A, ...)`)"
	nodetype = NodeType.FUNC
	precedence = 18
	names = {} # Maps function names to set of supported arities

	def __init__(self, name:str, args:tuple[AST, ...], *content:AST | str):
		super().__init__(*content)
		self.name = name
		self.args = args
		self.datatype = None
		self.validate()

	@classmethod
	def make(cls, name:str, *args:AST) -> FuncAST:
		content = [name, "("]
		for (i, arg) in enumerate(args):
			if i:
				content.append(", ")
			content.append(arg)
		content.append(")")

		return cls(name, args, *content)

	def _sqlsource(self, query:Query) -> templatelib.Template:
		rule = self.rules[(self.name,) + tuple(c.datatype for c in self.args)]
		result = t""
		for child in rule.source:
			if isinstance(child, int):
				result += self.args[child-1]._sqlsource(query)
			else:
				result += to_tstring(child)
		return result

	@classmethod
	def _add_rule(cls, rule:Rule) -> None:
		super()._add_rule(rule)
		if rule.name not in cls.names:
			cls.names[rule.name] = set()
		cls.names[rule.name].add(len(rule.signature))

	def validate(self) -> None:
		if any(arg.error is not None for arg in self.args):
			self.error = Error.SUBNODEERROR
		else:
			signature = (self.name, *(arg.datatype for arg in self.args))
			try:
				rule = self.rules[signature]
			except KeyError:
				if self.name not in self.names:
					self.error = Error.NAME
				elif len(self.args) not in self.names[self.name]:
					self.error = Error.ARITY
				else:
					self.error = Error.SUBNODETYPES
				self.datatype = None
			else:
				self.error = None
				self.datatype = rule.result

	@property
	def nodevalue(self) -> str:
		return self.name

	def children(self) -> Generator[AST, None, None]:
		yield from self.args

	def _ll_repr_(self) -> Generator[str, None, None]:
		yield from super()._ll_repr_()
		yield f"name={self.name!r}"
		yield f"with {len(self.args):,} arguments"

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		super()._ll_repr_pretty_(p)
		for (i, arg) in enumerate(self.args):
			p.breakable()
			p.text(f"args[{i}]=")
			p.pretty(arg)

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		super().ul4ondump(encoder)
		encoder.dump(self.name)
		encoder.dump(self.args)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		super().ul4onload(decoder)
		self.name = decoder.load()
		self.args = decoder.load()


@ul4on.register("de.livinglogic.vsql.meth")
class MethAST(AST):
	"""
	Method call (``A.name(B, ...)``).
	"""

	title = "Method call (`A.name(B, ...)`)"
	nodetype = NodeType.METH
	precedence = 17
	names = {} # Maps (type, meth name) to set of supported arities

	def __init__(self, obj:AST, name:str, args:tuple[AST, ...], *content:AST | str):
		super().__init__(*content)
		self.obj = obj
		self.name = name
		self.args = args or ()
		self.datatype = None
		self.validate()

	@classmethod
	def make(cls, obj:AST, name:str, *args:AST) -> MethAST:
		content = [*cls._wrap(obj, obj.precedence < cls.precedence), ".", name, "("]
		for (i, arg) in enumerate(args):
			if i:
				content.append(", ")
			content.append(arg)
		content.append(")")

		return cls(obj, name, args, *content)

	def _sqlsource(self, query:Query) -> templatelib.Template:
		rule = self.rules[(self.obj.datatype, self.name) + tuple(c.datatype for c in self.args)]
		result = t""
		for child in rule.source:
			if isinstance(child, int):
				if child == 1:
					result += self.obj._sqlsource(query)
				else:
					result += self.args[child-2]._sqlsource(query)
			else:
				result += to_tstring(child)
		return result

	@classmethod
	def _add_rule(cls, rule:Rule) -> None:
		super()._add_rule(rule)
		key = (rule.signature[0], rule.name)
		if key not in cls.names:
			cls.names[key] = set()
		cls.names[key].add(len(rule.signature)-1)

	def validate(self) -> None:
		if self.obj.error is not None or any(arg.error is not None for arg in self.args):
			self.error = Error.SUBNODEERROR
		signature = (self.obj.datatype, self.name, *(arg.datatype for arg in self.args))
		try:
			rule = self.rules[signature]
		except KeyError:
			key = (self.obj.datatype, self.name)
			if key not in self.names:
				self.error = Error.NAME
			elif len(self.args) not in self.names[key]:
				self.error = Error.ARITY
			else:
				self.error = Error.SUBNODETYPES
			self.datatype = None
		else:
			self.error = None
			self.datatype = rule.result

	@property
	def nodevalue(self) -> str:
		return self.name

	def children(self) -> Generator[AST, None, None]:
		yield self.obj
		yield from self.args

	def _ll_repr_(self) -> Generator[str, None, None]:
		yield from super()._ll_repr_()
		yield f"name={self.name!r}"
		yield f"with {len(self.args):,} arguments"

	def _ll_repr_pretty_(self, p:"IPython.lib.pretty.PrettyPrinter") -> None:
		super()._ll_repr_pretty_(p)
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		p.breakable()
		p.text("name=")
		p.pretty(self.name)
		for (i, arg) in enumerate(self.args):
			p.breakable()
			p.text(f"args[{i}]=")
			p.pretty(arg)

	def ul4ondump(self, encoder:ul4on.Encoder) -> None:
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.name)
		encoder.dump(self.args)

	def ul4onload(self, decoder:ul4on.Decoder) -> None:
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.name = decoder.load()
		self.args = decoder.load()


_consts = {
	type(None): NoneAST,
	bool: BoolAST,
	int: IntAST,
	float: NumberAST,
	str: StrAST,
	color.Color: ColorAST,
	datetime.date: DateAST,
	datetime.datetime: DateTimeAST,
}

# Set of UL4 AST nodes that directly map to their equivalent vSQL version
_ops = {
	ul4c.ConstAST,
	ul4c.NotAST,
	ul4c.NegAST,
	ul4c.BitNotAST,
	*ul4c.BinaryAST.__subclasses__(),
	ul4c.IfAST,
	ul4c.SliceAST,
	ul4c.ListAST,
	ul4c.SetAST
}

# Create the mapping that maps the UL4 AST type to the vSQL AST type
v = vars()
_ul42vsql = {cls: v[cls.__name__] for cls in _ops}

# Remove temporary variables
del _ops, v


###
### Create vSQL rules for all AST classes for validating datatypes and type inference
###

# Subsets of datatypes (used as union types in the t-strings for the AST signature)

dt = DataType

INTLIKE = (dt.BOOL, dt.INT)
NUMBERLIKE = (*INTLIKE, dt.NUMBER)
NUMBERSTORED = (dt.BOOL, dt.INT, dt.NUMBER, dt.COLOR, dt.DATEDELTA, dt.DATETIMEDELTA, dt.MONTHDELTA)

TEXT = (dt.STR, dt.CLOB)
LIST = (dt.INTLIST, dt.NUMBERLIST, dt.STRLIST, dt.CLOBLIST, dt.DATELIST, dt.DATETIMELIST)
SET = (dt.INTSET, dt.NUMBERSET, dt.STRSET, dt.DATESET, dt.DATETIMESET)
SEQ = (*TEXT, *LIST, *SET)
ANY = (dt.NULL, dt.BOOL, dt.INT, dt.NUMBER, dt.COLOR, dt.GEO, dt.DATE, dt.DATETIME, dt.DATEDELTA, dt.DATETIMEDELTA, dt.MONTHDELTA, dt.NULLLIST, *SEQ)

# Field references and constants (will not be used for generating source,
# but for checking that the node type is valid and that they have no child nodes)
FieldRefAST.add_rules(t"{dt.NULL}", t"")
NoneAST.add_rules(t"{dt.NULL}", t"")
BoolAST.add_rules(t"{dt.BOOL}", t"")
IntAST.add_rules(t"{dt.INT}", t"")
NumberAST.add_rules(t"{dt.NUMBER}", t"")
StrAST.add_rules(t"{dt.STR}", t"")
CLOBAST.add_rules(t"{dt.CLOB}", t"")
ColorAST.add_rules(t"{dt.COLOR}", t"")
DateAST.add_rules(t"{dt.DATE}", t"")
DateTimeAST.add_rules(t"{dt.DATETIME}", t"")

# Function ``today()``
FuncAST.add_rules(t"{dt.DATE} <- {'today'}()", t"trunc(sysdate)")

# Function ``now()``
FuncAST.add_rules(t"{dt.DATETIME} <- {'now'}()", t"sysdate")

# Function ``bool()``
FuncAST.add_rules(t"{dt.BOOL} <- {'bool'}()", t"0")
FuncAST.add_rules(t"{dt.BOOL} <- {'bool'}({dt.NULL})", t"0")
FuncAST.add_rules(t"{dt.BOOL} <- {'bool'}({dt.BOOL})", t"nvl({'s1'}, 0)")
FuncAST.add_rules(t"{dt.BOOL} <- {'bool'}({(dt.INT, dt.NUMBER, dt.DATEDELTA, dt.DATETIMEDELTA, dt.MONTHDELTA, dt.NULLLIST, dt.NULLSET)})", t"(case when nvl({'s1'}, 0) = 0 then 0 else 1 end)")
FuncAST.add_rules(t"{dt.BOOL} <- {'bool'}({(dt.DATE, dt.DATETIME, dt.STR, dt.COLOR, dt.GEO)})", t"(case when {'s1'} is null then 0 else 1 end)")
FuncAST.add_rules(t"{dt.BOOL} <- {'bool'}({ANY})", t"vsqlimpl_pkg.bool_{'t1'}({'s1'})")

# Function ``int()``
FuncAST.add_rules(t"{dt.INT} <- {'int'}()", t"0")
FuncAST.add_rules(t"{dt.INT} <- {'int'}({INTLIKE})", t"{'s1'}")
FuncAST.add_rules(t"{dt.INT} <- {'int'}({(dt.NUMBER, dt.STR, dt.CLOB)})", t"vsqlimpl_pkg.int_{'t1'}({'s1'})")

# Function ``float()``
FuncAST.add_rules(t"{dt.NUMBER} <- {'float'}()", t"0.0")
FuncAST.add_rules(t"{dt.NUMBER} <- {'float'}({NUMBERLIKE})", t"{'s1'}")
FuncAST.add_rules(t"{dt.NUMBER} <- {'float'}({TEXT})", t"vsqlimpl_pkg.float_{'t1'}({'s1'})")

# Function ``geo()``
FuncAST.add_rules(t"{dt.GEO} <- {'geo'}({NUMBERLIKE}, {NUMBERLIKE})", t"vsqlimpl_pkg.geo_number_number_str({'s1'}, {'s2'}, null)")
FuncAST.add_rules(t"{dt.GEO} <- {'geo'}({NUMBERLIKE}, {NUMBERLIKE}, {dt.STR})", t"vsqlimpl_pkg.geo_number_number_str({'s1'}, {'s2'}, {'s3'})")

# Function ``str()``
FuncAST.add_rules(t"{dt.STR} <- {'str'}()", t"null")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.NULL})", t"null")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.STR})", t"{'s1'}")
FuncAST.add_rules(t"{dt.CLOB} <- {'str'}({dt.CLOB})", t"{'s1'}")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.BOOL})", t"(case {'s1'} when 0 then 'False' when null then 'None' else 'True' end)")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.INT})", t"to_char({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.NUMBER})", t"vsqlimpl_pkg.str_number({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.GEO})", t"vsqlimpl_pkg.repr_geo({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.DATE})", t"to_char({'s1'}, 'YYYY-MM-DD')")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.DATETIME})", t"to_char({'s1'}, 'YYYY-MM-DD HH24:MI:SS')")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.NULLLIST})", t"vsqlimpl_pkg.repr_nulllist({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.DATELIST})", t"vsqlimpl_pkg.repr_datelist({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({LIST})", t"vsqlimpl_pkg.repr_{'t1'}({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.NULLSET})", t"vsqlimpl_pkg.repr_nullset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.INTSET})", t"vsqlimpl_pkg.repr_intset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.NUMBERSET})", t"vsqlimpl_pkg.repr_numberset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.STRSET})", t"vsqlimpl_pkg.repr_strset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.DATESET})", t"vsqlimpl_pkg.repr_dateset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({dt.DATETIMESET})", t"vsqlimpl_pkg.repr_datetimeset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'str'}({ANY})", t"vsqlimpl_pkg.str_{'t1'}({'s1'})")

# Function ``repr()``
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({dt.NULL})", t"'None'")
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({dt.BOOL})", t"(case {'s1'} when 0 then 'False' when null then 'None' else 'True' end)")
FuncAST.add_rules(t"{dt.CLOB} <- {'repr'}({[dt.CLOB, dt.CLOBLIST]})", t"vsqlimpl_pkg.repr_{'t1'}({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({dt.DATE})", t"vsqlimpl_pkg.repr_date({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({dt.DATELIST})", t"vsqlimpl_pkg.repr_datelist({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({dt.NULLSET})", t"vsqlimpl_pkg.repr_nullset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({dt.INTSET})", t"vsqlimpl_pkg.repr_intset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({dt.NUMBERSET})", t"vsqlimpl_pkg.repr_numberset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({dt.STRSET})", t"vsqlimpl_pkg.repr_strset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({dt.DATESET})", t"vsqlimpl_pkg.repr_dateset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({dt.DATETIMESET})", t"vsqlimpl_pkg.repr_datetimeset({'s1'})")
FuncAST.add_rules(t"{dt.STR} <- {'repr'}({ANY})", t"vsqlimpl_pkg.repr_{'t1'}({'s1'})")

# Function ``date()``
FuncAST.add_rules(t"{dt.DATE} <- {'date'}({dt.INT}, {dt.INT}, {dt.INT})", t"vsqlimpl_pkg.date_int({'s1'}, {'s2'}, {'s3'})")
FuncAST.add_rules(t"{dt.DATE} <- {'date'}({dt.DATETIME})", t"trunc({'s1'})")

# Function ``datetime()``
FuncAST.add_rules(t"{dt.DATETIME} <- {'datetime'}({dt.INT}, {dt.INT}, {dt.INT})", t"vsqlimpl_pkg.datetime_int({'s1'}, {'s2'}, {'s3'})")
FuncAST.add_rules(t"{dt.DATETIME} <- {'datetime'}({dt.INT}, {dt.INT}, {dt.INT}, {dt.INT})", t"vsqlimpl_pkg.datetime_int({'s1'}, {'s2'}, {'s3'}, {'s4'})")
FuncAST.add_rules(t"{dt.DATETIME} <- {'datetime'}({dt.INT}, {dt.INT}, {dt.INT}, {dt.INT}, {dt.INT})", t"vsqlimpl_pkg.datetime_int({'s1'}, {'s2'}, {'s3'}, {'s4'}, {'s5'})")
FuncAST.add_rules(t"{dt.DATETIME} <- {'datetime'}({dt.INT}, {dt.INT}, {dt.INT}, {dt.INT}, {dt.INT}, {dt.INT})", t"vsqlimpl_pkg.datetime_int({'s1'}, {'s2'}, {'s3'}, {'s4'}, {'s5'}, {'s6'})")
FuncAST.add_rules(t"{dt.DATETIME} <- {'datetime'}({dt.DATE})", t"{'s1'}")
FuncAST.add_rules(t"{dt.DATETIME} <- {'datetime'}({dt.DATE}, {dt.INT})", t"({'s1'} + {'s2'}/24)")
FuncAST.add_rules(t"{dt.DATETIME} <- {'datetime'}({dt.DATE}, {dt.INT}, {dt.INT})", t"({'s1'} + {'s2'}/24 + {'s3'}/24/60)")
FuncAST.add_rules(t"{dt.DATETIME} <- {'datetime'}({dt.DATE}, {dt.INT}, {dt.INT}, {dt.INT})", t"({'s1'} + {'s2'}/24 + {'s3'}/24/60 + {'s4'}/24/60/60)")

# Function ``len()``
FuncAST.add_rules(t"{dt.INT} <- {'len'}({TEXT})", t"nvl(length({'s1'}), 0)")
FuncAST.add_rules(t"{dt.INT} <- {'len'}({dt.NULLLIST})", t"{'s1'}")
FuncAST.add_rules(t"{dt.INT} <- {'len'}({LIST})", t"vsqlimpl_pkg.len_{'t1'}({'s1'})")
FuncAST.add_rules(t"{dt.INT} <- {'len'}({dt.NULLSET})", t"case when {'s1'} > 0 then 1 else {'s1'} end")
FuncAST.add_rules(t"{dt.INT} <- {'len'}({SET})", t"vsqlimpl_pkg.len_{'t1'}({'s1'})")

# Function ``timedelta()``
FuncAST.add_rules(t"{dt.DATEDELTA} <- {'timedelta'}()", t"0")
FuncAST.add_rules(t"{dt.DATEDELTA} <- {'timedelta'}({dt.INT})", t"{'s1'}")
FuncAST.add_rules(t"{dt.DATETIMEDELTA} <- {'timedelta'}({dt.INT}, {dt.INT})", t"({'s1'} + {'s2'}/86400)")

# Function ``monthdelta()``
FuncAST.add_rules(t"{dt.MONTHDELTA} <- {'monthdelta'}()", t"0")
FuncAST.add_rules(t"{dt.MONTHDELTA} <- {'monthdelta'}({dt.INT})", t"{'s1'}")

# Function ``years()``
FuncAST.add_rules(t"{dt.MONTHDELTA} <- {'years'}({dt.INT})", t"(12 * {'s1'})")

# Function ``months()``
FuncAST.add_rules(t"{dt.MONTHDELTA} <- {'months'}({dt.INT})", t"{'s1'}")

# Function ``weeks()``
FuncAST.add_rules(t"{dt.DATEDELTA} <- {'weeks'}({dt.INT})", t"(7 * {'s1'})")

# Function ``days()``
FuncAST.add_rules(t"{dt.DATEDELTA} <- {'days'}({dt.INT})", t"{'s1'}")

# Function ``hours()``
FuncAST.add_rules(t"{dt.DATETIMEDELTA} <- {'hours'}({dt.INT})", t"({'s1'} / 24)")

# Function ``minutes()``
FuncAST.add_rules(t"{dt.DATETIMEDELTA} <- {'minutes'}({dt.INT})", t"({'s1'} / 1440)")

# Function ``seconds()``
FuncAST.add_rules(t"{dt.DATETIMEDELTA} <- {'seconds'}({dt.INT})", t"({'s1'} / 86400)")

# Function `md5()``
FuncAST.add_rules(t"{dt.STR} <- {'md5'}({dt.STR})", t"lower(rawtohex(dbms_crypto.hash(utl_raw.cast_to_raw({'s1'}), 2)))")

# Function `random()``
FuncAST.add_rules(t"{dt.NUMBER} <- {'random'}()", t"dbms_random.value")

# Function `randrange()``
FuncAST.add_rules(t"{dt.INT} <- {'randrange'}({dt.INT}, {dt.INT})", t"floor(dbms_random.value({'s1'}, {'s2'}))")

# Function `seq()``
FuncAST.add_rules(t"{dt.INT} <- {'seq'}()", t"vsqlimpl_pkg.seq()")

# Function `rgb()``
FuncAST.add_rules(t"{dt.COLOR} <- {'rgb'}({NUMBERLIKE}, {NUMBERLIKE}, {NUMBERLIKE})", t"vsqlimpl_pkg.rgb({'s1'}, {'s2'}, {'s3'})")
FuncAST.add_rules(t"{dt.COLOR} <- {'rgb'}({NUMBERLIKE}, {NUMBERLIKE}, {NUMBERLIKE}, {NUMBERLIKE})", t"vsqlimpl_pkg.rgb({'s1'}, {'s2'}, {'s3'}, {'s4'})")

# Function `list()``
FuncAST.add_rules(t"{dt.STRLIST} <- {'list'}({TEXT})", t"vsqlimpl_pkg.list_{'t1'}({'s1'})")
FuncAST.add_rules(t"{'T1'} <- {'list'}({[dt.NULLLIST, *LIST]})", t"{'s1'}")
FuncAST.add_rules(t"{dt.NULLLIST} <- {'list'}({dt.NULLSET})", t"{'s1'}")
FuncAST.add_rules(t"{dt.INTLIST} <- {'list'}({dt.INTSET})", t"{'s1'}")
FuncAST.add_rules(t"{dt.NUMBERLIST} <- {'list'}({dt.NUMBERSET})", t"{'s1'}")
FuncAST.add_rules(t"{dt.STRLIST} <- {'list'}({dt.STRSET})", t"{'s1'}")
FuncAST.add_rules(t"{dt.DATELIST} <- {'list'}({dt.DATESET})", t"{'s1'}")
FuncAST.add_rules(t"{dt.DATETIMELIST} <- {'list'}({dt.DATETIMESET})", t"{'s1'}")

# Function `set()``
FuncAST.add_rules(t"{dt.STRSET} <- {'set'}({TEXT})", t"vsqlimpl_pkg.set_{'t1'}({'s1'})")
FuncAST.add_rules(t"{'T1'} <- {'set'}({SET})", t"{'s1'}")
FuncAST.add_rules(t"{dt.NULLSET} <- {'set'}({dt.NULLLIST})", t"case when {'s1'} > 0 then 1 else {'s1'} end")
FuncAST.add_rules(t"{dt.INTSET} <- {'set'}({dt.INTLIST})", t"vsqlimpl_pkg.set_{'t1'}({'s1'})")
FuncAST.add_rules(t"{dt.NUMBERSET} <- {'set'}({dt.NUMBERLIST})", t"vsqlimpl_pkg.set_{'t1'}({'s1'})")
FuncAST.add_rules(t"{dt.STRSET} <- {'set'}({dt.STRLIST})", t"vsqlimpl_pkg.set_{'t1'}({'s1'})")
FuncAST.add_rules(t"{dt.DATESET} <- {'set'}({dt.DATELIST})", t"vsqlimpl_pkg.set_{'t1'}({'s1'})")
FuncAST.add_rules(t"{dt.DATETIMESET} <- {'set'}({dt.DATETIMELIST})", t"vsqlimpl_pkg.set_{'t1'}({'s1'})")

# Function ``dist()``
FuncAST.add_rules(t"{dt.NUMBER} <- {'dist'}({dt.GEO}, {dt.GEO})", t"vsqlimpl_pkg.dist_geo_geo({'s1'}, {'s2'})")

# Function ``abs()``
FuncAST.add_rules(t"{dt.INT} <- {'abs'}({dt.BOOL})", t"{'s1'}")
FuncAST.add_rules(t"{dt.INT} <- {'abs'}({dt.INT})", t"abs({'s1'})")
FuncAST.add_rules(t"{dt.NUMBER} <- {'abs'}({dt.NUMBER})", t"abs({'s1'})")

# Function ``cos()``
FuncAST.add_rules(t"{dt.NUMBER} <- {'cos'}({NUMBERLIKE})", t"cos({'s1'})")

# Function ``sin()``
FuncAST.add_rules(t"{dt.NUMBER} <- {'sin'}({NUMBERLIKE})", t"sin({'s1'})")

# Function ``tan()``
FuncAST.add_rules(t"{dt.NUMBER} <- {'tan'}({NUMBERLIKE})", t"tan({'s1'})")

# Function ``sqrt()``
FuncAST.add_rules(t"{dt.NUMBER} <- {'sqrt'}({NUMBERLIKE})", t"sqrt(case when {'s1'} >= 0 then {'s1'} else null end)")

# Function ``request_id()``
FuncAST.add_rules(t"{dt.STR} <- {'request_id'}()", t"livingapi_pkg.reqid")

# Function ``request_method()``
FuncAST.add_rules(t"{dt.STR} <- {'request_method'}()", t"livingapi_pkg.reqmethod")

# Function ``request_url()``
FuncAST.add_rules(t"{dt.STR} <- {'request_url'}()", t"livingapi_pkg.requrl")

# Function ``request_header_str()``
FuncAST.add_rules(t"{dt.STR} <- {'request_header_str'}({dt.STR})", t"livingapi_pkg.reqheader_str({'s1'})")

# Function ``request_header_strlist()``
FuncAST.add_rules(t"{dt.STRLIST} <- {'request_header_strlist'}({dt.STR})", t"livingapi_pkg.reqheader_str({'s1'})")

# Function ``request_cookie()``
FuncAST.add_rules(t"{dt.STR} <- {'request_cookie'}({dt.STR})", t"livingapi_pkg.reqcookie_str({'s1'})")

# Function ``request_param_str()``
FuncAST.add_rules(t"{dt.STR} <- {'request_param_str'}({dt.STR})", t"livingapi_pkg.reqparam_str({'s1'})")

# Function ``request_param_strlist()``
FuncAST.add_rules(t"{dt.STRLIST} <- {'request_param_strlist'}({dt.STR})", t"livingapi_pkg.reqparam_strlist({'s1'})")

# Function ``request_param_int()``
FuncAST.add_rules(t"{dt.INT} <- {'request_param_int'}({dt.STR})", t"livingapi_pkg.reqparam_int({'s1'})")

# Function ``request_param_intlist()``
FuncAST.add_rules(t"{dt.INTLIST} <- {'request_param_intlist'}({dt.STR})", t"livingapi_pkg.reqparam_intlist({'s1'})")

# Function ``request_param_float()``
FuncAST.add_rules(t"{dt.NUMBER} <- {'request_param_float'}({dt.STR})", t"livingapi_pkg.reqparam_float({'s1'})")

# Function ``request_param_floatlist()``
FuncAST.add_rules(t"{dt.NUMBERLIST} <- {'request_param_floatlist'}({dt.STR})", t"livingapi_pkg.reqparam_floatlist({'s1'})")

# Function ``request_param_date()``
FuncAST.add_rules(t"{dt.DATE} <- {'request_param_date'}({dt.STR})", t"livingapi_pkg.reqparam_date({'s1'})")

# Function ``request_param_datelist()``
FuncAST.add_rules(t"{dt.DATELIST} <- {'request_param_datelist'}({dt.STR})", t"livingapi_pkg.reqparam_datelist({'s1'})")

# Function ``request_param_datetime()``
FuncAST.add_rules(t"{dt.DATETIME} <- {'request_param_datetime'}({dt.STR})", t"livingapi_pkg.reqparam_datetime({'s1'})")

# Function ``request_param_datetimelist()``
FuncAST.add_rules(t"{dt.DATETIMELIST} <- {'request_param_datetimelist'}({dt.STR})", t"livingapi_pkg.reqparam_datetimelist({'s1'})")

# Function ``search()``
FuncAST.add_rules(t"{dt.STR} <- {'search'}()", t"livingapi_pkg.global_search")

# Function ``lang()``
FuncAST.add_rules(t"{dt.STR} <- {'lang'}()", t"livingapi_pkg.global_lang")

# Function ``mode()``
FuncAST.add_rules(t"{dt.STR} <- {'mode'}()", t"livingapi_pkg.global_mode")

# Method ``lower()``
MethAST.add_rules(t"{'T1'} <- {TEXT}.{'lower'}()", t"lower({'s1'})")

# Method ``upper()``
MethAST.add_rules(t"{'T1'} <- {TEXT}.{'upper'}()", t"upper({'s1'})")

# Method ``startswith()``
MethAST.add_rules(t"{dt.BOOL} <- {TEXT}.{'startswith'}({[dt.STR, dt.STRLIST]})", t"vsqlimpl_pkg.startswith_{'t1'}_{'t2'}({'s1'}, {'s2'})")

# Method ``endswith()``
MethAST.add_rules(t"{dt.BOOL} <- {TEXT}.{'endswith'}({[dt.STR, dt.STRLIST]})", t"vsqlimpl_pkg.endswith_{'t1'}_{'t2'}({'s1'}, {'s2'})")

# Method ``strip()``
MethAST.add_rules(t"{'T1'} <- {TEXT}.{'strip'}()", t"vsqlimpl_pkg.strip_{'t1'}({'s1'}, null, 1, 1)")
MethAST.add_rules(t"{'T1'} <- {TEXT}.{'strip'}({dt.STR}) ", t"vsqlimpl_pkg.strip_{'t1'}({'s1'}, {'s2'}, 1, 1)")

# Method ``lstrip()``
MethAST.add_rules(t"{'T1'} <- {TEXT}.{'lstrip'}()", t"vsqlimpl_pkg.strip_{'t1'}({'s1'}, null, 1, 0)")
MethAST.add_rules(t"{'T1'} <- {TEXT}.{'lstrip'}({dt.STR}) ", t"vsqlimpl_pkg.strip_{'t1'}({'s1'}, {'s2'}, 1, 0)")

# Method ``rstrip()``
MethAST.add_rules(t"{'T1'} <- {TEXT}.{'rstrip'}()", t"vsqlimpl_pkg.strip_{'t1'}({'s1'}, null, 0, 1)")
MethAST.add_rules(t"{'T1'} <- {TEXT}.{'rstrip'}({dt.STR}) ", t"vsqlimpl_pkg.strip_{'t1'}({'s1'}, {'s2'}, 0, 1)")

# Method ``find()``
MethAST.add_rules(t"{dt.INT} <- {TEXT}.{'find'}({TEXT})", t"(instr({'s1'}, {'s2'}) - 1)")
MethAST.add_rules(t"{dt.INT} <- {TEXT}.{'find'}({TEXT}, {dt.NULL})", t"(instr({'s1'}, {'s2'}) - 1)")
MethAST.add_rules(t"{dt.INT} <- {TEXT}.{'find'}({TEXT}, {dt.NULL}, {dt.NULL})", t"(instr({'s1'}, {'s2'}) - 1)")
MethAST.add_rules(t"{dt.INT} <- {TEXT}.{'find'}({TEXT}, {[dt.NULL, dt.INT]})", t"vsqlimpl_pkg.find_{'t1'}_{'t2'}({'s1'}, {'s2'}, {'s3'}, null)")
MethAST.add_rules(t"{dt.INT} <- {TEXT}.{'find'}({TEXT}, {[dt.NULL, dt.INT]}, {[dt.NULL, dt.INT]})", t"vsqlimpl_pkg.find_{'t1'}_{'t2'}({'s1'}, {'s2'}, {'s3'}, {'s4'})")

# Method ``replace()``
MethAST.add_rules(t"{'T1'} <- {TEXT}.{'replace'}({dt.STR}, {dt.STR})", t"replace({'s1'}, {'s2'}, {'s3'})")

# Method ``split()``
MethAST.add_rules(t"{dt.STRLIST} <- {dt.STR}.{'split'}()", t"vsqlimpl_pkg.split_{'t1'}_str({'s1'}, null)")
MethAST.add_rules(t"{dt.CLOBLIST} <- {dt.CLOB}.{'split'}()", t"vsqlimpl_pkg.split_{'t1'}_str({'s1'}, null)")
MethAST.add_rules(t"{dt.STRLIST} <- {dt.STR}.{'split'}({dt.NULL})", t"vsqlimpl_pkg.split_{'t1'}_str(null, null)")
MethAST.add_rules(t"{dt.CLOBLIST} <- {dt.CLOB}.{'split'}({dt.NULL})", t"vsqlimpl_pkg.split_{'t1'}_str(null, null)")
MethAST.add_rules(t"{dt.STRLIST} <- {dt.STR}.{'split'}({dt.STR})", t"vsqlimpl_pkg.split_{'t1'}_str({'s1'}, {'s2'})")
MethAST.add_rules(t"{dt.CLOBLIST} <- {dt.CLOB}.{'split'}({dt.STR})", t"vsqlimpl_pkg.split_{'t1'}_str({'s1'}, {'s2'})")
MethAST.add_rules(t"{dt.STRLIST} <- {dt.STR}.{'split'}({dt.STR}, {dt.NULL})", t"vsqlimpl_pkg.split_{'t1'}_str({'s1'}, {'s2'})")
MethAST.add_rules(t"{dt.CLOBLIST} <- {dt.CLOB}.{'split'}({dt.STR}, {dt.NULL})", t"vsqlimpl_pkg.split_{'t1'}_str({'s1'}, {'s2'})")
MethAST.add_rules(t"{dt.STRLIST} <- {dt.STR}.{'split'}({dt.NULL}, {[dt.BOOL, dt.INT]})", t"vsqlimpl_pkg.split_{'t1'}_str({'s1'}, null, {'s3'})")
MethAST.add_rules(t"{dt.CLOBLIST} <- {dt.CLOB}.{'split'}({dt.NULL}, {[dt.BOOL, dt.INT]})", t"vsqlimpl_pkg.split_{'t1'}_str({'s1'}, null, {'s3'})")
MethAST.add_rules(t"{dt.STRLIST} <- {dt.STR}.{'split'}({dt.STR}, {[dt.BOOL, dt.INT]})", t"vsqlimpl_pkg.split_{'t1'}_str({'s1'}, {'s2'}, {'s3'})")
MethAST.add_rules(t"{dt.CLOBLIST} <- {dt.CLOB}.{'split'}({dt.STR}, {[dt.BOOL, dt.INT]})", t"vsqlimpl_pkg.split_{'t1'}_str({'s1'}, {'s2'}, {'s3'})")

# Method ``join()``
MethAST.add_rules(t"{dt.STR} <- {dt.STR}.{'join'}({[dt.STR, dt.STRLIST]})", t"vsqlimpl_pkg.join_str_{'t2'}({'s1'}, {'s2'})")
MethAST.add_rules(t"{dt.CLOB} <- {dt.STR}.{'join'}({[dt.CLOB, dt.CLOBLIST]})", t"vsqlimpl_pkg.join_str_{'t2'}({'s1'}, {'s2'})")

# Method ``lum()``
MethAST.add_rules(t"{dt.NUMBER} <- {dt.COLOR}.{'lum'}()", t"vsqlimpl_pkg.lum({'s1'})")

# Method ``week()``
MethAST.add_rules(t"{dt.INT} <- {[dt.DATE, dt.DATETIME]}.{'week'}()", t"to_number(to_char({'s1'}, 'IW'))")

# Attributes
AttrAST.add_rules(t"{dt.INT} <- {[dt.DATE, dt.DATETIME]}.{'year'}", t"extract(year from {'s1'})")
AttrAST.add_rules(t"{dt.INT} <- {[dt.DATE, dt.DATETIME]}.{'month'}", t"extract(month from {'s1'})")
AttrAST.add_rules(t"{dt.INT} <- {[dt.DATE, dt.DATETIME]}.{'day'}", t"extract(day from {'s1'})")
AttrAST.add_rules(t"{dt.INT} <- {dt.DATETIME}.{'hour'}", t"to_number(to_char({'s1'}, 'HH24'))")
AttrAST.add_rules(t"{dt.INT} <- {dt.DATETIME}.{'minute'}", t"to_number(to_char({'s1'}, 'MI'))")
AttrAST.add_rules(t"{dt.INT} <- {dt.DATETIME}.{'second'}", t"to_number(to_char({'s1'}, 'SS'))")
AttrAST.add_rules(t"{dt.INT} <- {[dt.DATE, dt.DATETIME]}.{'weekday'}", t"vsqlimpl_pkg.attr_date_weekday({'s1'})")
AttrAST.add_rules(t"{dt.INT} <- {[dt.DATE, dt.DATETIME]}.{'yearday'}", t"to_number(to_char({'s1'}, 'DDD'))")
AttrAST.add_rules(t"{dt.INT} <- {dt.DATEDELTA}.{'days'}", t"{'s1'}")
AttrAST.add_rules(t"{dt.INT} <- {dt.DATETIMEDELTA}.{'days'}", t"trunc({'s1'})")
AttrAST.add_rules(t"{dt.INT} <- {dt.DATETIMEDELTA}.{'seconds'}", t"trunc(mod({'s1'}, 1) * 86400 + 0.5)")
AttrAST.add_rules(t"{dt.NUMBER} <- {dt.DATETIMEDELTA}.{'total_days'}", t"{'s1'}")
AttrAST.add_rules(t"{dt.NUMBER} <- {dt.DATETIMEDELTA}.{'total_hours'}", t"({'s1'} * 24)")
AttrAST.add_rules(t"{dt.NUMBER} <- {dt.DATETIMEDELTA}.{'total_minutes'}", t"({'s1'} * 1440)")
AttrAST.add_rules(t"{dt.NUMBER} <- {dt.DATETIMEDELTA}.{'total_seconds'}", t"({'s1'} * 86400)")
AttrAST.add_rules(t"{dt.INT} <- {dt.COLOR}.{'r'}", t"vsqlimpl_pkg.attr_color_r({'s1'})")
AttrAST.add_rules(t"{dt.INT} <- {dt.COLOR}.{'g'}", t"vsqlimpl_pkg.attr_color_g({'s1'})")
AttrAST.add_rules(t"{dt.INT} <- {dt.COLOR}.{'b'}", t"vsqlimpl_pkg.attr_color_b({'s1'})")
AttrAST.add_rules(t"{dt.INT} <- {dt.COLOR}.{'a'}", t"vsqlimpl_pkg.attr_color_a({'s1'})")
AttrAST.add_rules(t"{dt.NUMBER} <- {dt.GEO}.{'lat'}", t"vsqlimpl_pkg.attr_geo_lat({'s1'})")
AttrAST.add_rules(t"{dt.NUMBER} <- {dt.GEO}.{'long'}", t"vsqlimpl_pkg.attr_geo_long({'s1'})")
AttrAST.add_rules(t"{dt.STR} <- {dt.GEO}.{'info'}", t"vsqlimpl_pkg.attr_geo_info({'s1'})")

# Equality comparison (A == B)
EQAST.add_rules(t"{dt.BOOL} <- {dt.NULL} == {dt.NULL}", t"1")
EQAST.add_rules(t"{dt.BOOL} <- {ANY} == {dt.NULL}", t"(case when {'s1'} is null then 1 else 0 end)")
EQAST.add_rules(t"{dt.BOOL} <- {dt.NULL} == {ANY}", t"(case when {'s2'} is null then 1 else 0 end)")
EQAST.add_rules(t"{dt.BOOL} <- {INTLIKE} == {INTLIKE}", t"vsqlimpl_pkg.eq_int_int({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {NUMBERLIKE} == {NUMBERLIKE}", t"vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.GEO} == {dt.GEO}", t"vsqlimpl_pkg.eq_str_str({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.COLOR} == {dt.COLOR}", t"vsqlimpl_pkg.eq_int_int({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {TEXT} == {TEXT}", t"vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {[dt.DATE, dt.DATETIME]} == {'T1'}", t"vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {[dt.DATEDELTA, dt.MONTHDELTA, dt.COLOR]} == {'T1'}", t"vsqlimpl_pkg.eq_int_int({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.DATETIMEDELTA} == {dt.DATETIMEDELTA}", t"vsqlimpl_pkg.eq_datetimedelta_datetimedelta({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.NULLLIST} == {[dt.NULLLIST, *LIST]}", t"vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {[dt.NULLLIST, *LIST]} == {dt.NULLLIST}", t"vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {[dt.INTLIST, dt.NUMBERLIST]} == {[dt.INTLIST, dt.NUMBERLIST]}", t"vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {[dt.STRLIST, dt.CLOBLIST]} == {[dt.STRLIST, dt.CLOBLIST]}", t"vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {[dt.DATELIST, dt.DATETIMELIST]} == {[dt.DATELIST, dt.DATETIMELIST]}", t"vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} == {dt.NULLSET}", t"vsqlimpl_pkg.eq_nullset_nullset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} == {dt.INTSET}", t"vsqlimpl_pkg.eq_nullset_intset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} == {dt.NUMBERSET}", t"vsqlimpl_pkg.eq_nullset_numberset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} == {dt.STRSET}", t"vsqlimpl_pkg.eq_nullset_strset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} == {dt.DATESET}", t"vsqlimpl_pkg.eq_nullset_datetimeset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} == {dt.DATETIMESET}", t"vsqlimpl_pkg.eq_nullset_datetimeset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.INTSET} == {dt.NULLSET}", t"vsqlimpl_pkg.eq_intset_nullset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.NUMBERSET} == {dt.NULLSET}", t"vsqlimpl_pkg.eq_numberset_nullset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.STRSET} == {dt.NULLSET}", t"vsqlimpl_pkg.eq_strset_nullset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.DATESET} == {dt.NULLSET}", t"vsqlimpl_pkg.eq_datetimeset_nullset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.DATETIMESET} == {dt.NULLSET}", t"vsqlimpl_pkg.eq_datetimeset_nullset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.INTSET} == {dt.INTSET}", t"vsqlimpl_pkg.eq_intset_intset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.NUMBERSET} == {dt.NUMBERSET}", t"vsqlimpl_pkg.eq_numberset_numberset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {dt.STRSET} == {dt.STRSET}", t"vsqlimpl_pkg.eq_strset_strset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {[dt.DATESET, dt.DATETIMESET]} == {[dt.DATESET, dt.DATETIMESET]}", t"vsqlimpl_pkg.eq_datetimeset_datetimeset({'s1'}, {'s2'})")
EQAST.add_rules(t"{dt.BOOL} <- {ANY} == {ANY}", t"(case when {'s1'} is null and {'s2'} is null then 1 else 0 end)")

# Inequality comparison (A != B)
NEAST.add_rules(t"{dt.BOOL} <- {dt.NULL} != {dt.NULL}", t"0")
NEAST.add_rules(t"{dt.BOOL} <- {ANY} != {dt.NULL}", t"(case when {'s1'} is null then 0 else 1 end)")
NEAST.add_rules(t"{dt.BOOL} <- {dt.NULL} != {ANY}", t"(case when {'s2'} is null then 0 else 1 end)")
NEAST.add_rules(t"{dt.BOOL} <- {INTLIKE} != {INTLIKE}", t"(1 - vsqlimpl_pkg.eq_int_int({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {NUMBERLIKE} != {NUMBERLIKE}", t"(1 - vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.GEO} != {dt.GEO}", t"(1 - vsqlimpl_pkg.eq_str_str({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.COLOR} != {dt.COLOR}", t"(1 - vsqlimpl_pkg.eq_int_int({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {TEXT} != {TEXT}", t"(1 - vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {[dt.DATE, dt.DATETIME]} != {'T1'}", t"(1 - vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {[dt.DATEDELTA, dt.MONTHDELTA, dt.COLOR]} != {'T1'}", t"(1 - vsqlimpl_pkg.eq_int_int({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.DATETIMEDELTA} != {dt.DATETIMEDELTA}", t"(1 - vsqlimpl_pkg.eq_datetimedelta_datetimedelta({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.NULLLIST} != {[dt.NULLLIST, *LIST]}", t"(1 - vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {[dt.NULLLIST, *LIST]} != {dt.NULLLIST}", t"(1 - vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {[dt.INTLIST, dt.NUMBERLIST]} != {[dt.INTLIST, dt.NUMBERLIST]}", t"(1 - vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {[dt.STRLIST, dt.CLOBLIST]} != {[dt.STRLIST, dt.CLOBLIST]}", t"(1 - vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {[dt.DATELIST, dt.DATETIMELIST]} != {[dt.DATELIST, dt.DATETIMELIST]}", t"(1 - vsqlimpl_pkg.eq_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} != {dt.NULLSET}", t"(1 - vsqlimpl_pkg.eq_nullset_nullset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} != {dt.INTSET}", t"(1 - vsqlimpl_pkg.eq_nullset_intset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} != {dt.NUMBERSET}", t"(1 - vsqlimpl_pkg.eq_nullset_numberset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} != {dt.STRSET}", t"(1 - vsqlimpl_pkg.eq_nullset_strset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} != {dt.DATESET}", t"(1 - vsqlimpl_pkg.eq_nullset_datetimeset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.NULLSET} != {dt.DATETIMESET}", t"(1 - vsqlimpl_pkg.eq_nullset_datetimeset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.INTSET} != {dt.NULLSET}", t"(1 - vsqlimpl_pkg.eq_intset_nullset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.NUMBERSET} != {dt.NULLSET}", t"(1 - vsqlimpl_pkg.eq_numberset_nullset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.STRSET} != {dt.NULLSET}", t"(1 - vsqlimpl_pkg.eq_strset_nullset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.DATESET} != {dt.NULLSET}", t"(1 - vsqlimpl_pkg.eq_datetimeset_nullset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.DATETIMESET} != {dt.NULLSET}", t"(1 - vsqlimpl_pkg.eq_datetimeset_nullset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.INTSET} != {dt.INTSET}", t"(1 - vsqlimpl_pkg.eq_intset_intset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.NUMBERSET} != {dt.NUMBERSET}", t"(1 - vsqlimpl_pkg.eq_numberset_numberset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {dt.STRSET} != {dt.STRSET}", t"(1 - vsqlimpl_pkg.eq_strset_strset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {[dt.DATESET, dt.DATETIMESET]} != {[dt.DATESET, dt.DATETIMESET]}", t"(1 - vsqlimpl_pkg.eq_datetimeset_datetimeset({'s1'}, {'s2'}))")
NEAST.add_rules(t"{dt.BOOL} <- {ANY} != {ANY}", t"(case when {'s1'} is null and {'s2'} is null then 0 else 1 end)")

# The following comparisons always treat ``None`` as uncomparable (expect when comparing with another ``None``)

# Greater-than comparison (A > B)
GTAST.add_rules(t"{dt.BOOL} <- {dt.NULL} > {dt.NULL}", t"0")
GTAST.add_rules(t"{dt.BOOL} <- {ANY} > {dt.NULL}", t"(case when {'s1'} is null then 0 else null end)")
GTAST.add_rules(t"{dt.BOOL} <- {dt.NULL} > {ANY}", t"(case when {'s2'} is null then 0 else null end)")
GTAST.add_rules(t"{dt.BOOL} <- {INTLIKE} > {INTLIKE}", t"case vsqlimpl_pkg.cmp_int_int({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")
GTAST.add_rules(t"{dt.BOOL} <- {NUMBERLIKE} > {NUMBERLIKE}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")
GTAST.add_rules(t"{dt.BOOL} <- {TEXT} > {TEXT}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")
GTAST.add_rules(t"{dt.BOOL} <- {[dt.DATE, dt.DATETIME]} > {'T1'}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")
GTAST.add_rules(t"{dt.BOOL} <- {dt.DATEDELTA} > {dt.DATEDELTA}", t"case vsqlimpl_pkg.cmp_int_int({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")
GTAST.add_rules(t"{dt.BOOL} <- {dt.DATETIMEDELTA} > {dt.DATETIMEDELTA}", t"case vsqlimpl_pkg.cmp_number_number({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")
GTAST.add_rules(t"{dt.BOOL} <- {[dt.INTLIST, dt.NUMBERLIST]} > {[dt.INTLIST, dt.NUMBERLIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")
GTAST.add_rules(t"{dt.BOOL} <- {[dt.STRLIST, dt.CLOBLIST]} > {[dt.STRLIST, dt.CLOBLIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")
GTAST.add_rules(t"{dt.BOOL} <- {[dt.DATELIST, dt.DATETIMELIST]} > {'T1'}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")
GTAST.add_rules(t"{dt.BOOL} <- {dt.NULLLIST} > {[dt.NULLLIST, *LIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")
GTAST.add_rules(t"{dt.BOOL} <- {[dt.NULLLIST, *LIST]} > {dt.NULLLIST}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 0 when 1 then 1 end")

# Greater-than-or equal comparison (A >= B)
GEAST.add_rules(t"{dt.BOOL} <- {dt.NULL} >= {dt.NULL}", t"1")
GEAST.add_rules(t"{dt.BOOL} <- {ANY} >= {dt.NULL}", t"(case when {'s1'} is null then 1 else null end)")
GEAST.add_rules(t"{dt.BOOL} <- {dt.NULL} >= {ANY}", t"(case when {'s2'} is null then 1 else null end)")
GEAST.add_rules(t"{dt.BOOL} <- {INTLIKE} >= {INTLIKE}", t"case vsqlimpl_pkg.cmp_int_int({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")
GEAST.add_rules(t"{dt.BOOL} <- {NUMBERLIKE} >= {NUMBERLIKE}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")
GEAST.add_rules(t"{dt.BOOL} <- {TEXT} >= {TEXT}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")
GEAST.add_rules(t"{dt.BOOL} <- {[dt.DATE, dt.DATETIME]} >= {'T1'}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")
GEAST.add_rules(t"{dt.BOOL} <- {dt.DATEDELTA} >= {dt.DATEDELTA}", t"case vsqlimpl_pkg.cmp_int_int({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")
GEAST.add_rules(t"{dt.BOOL} <- {dt.DATETIMEDELTA} >= {dt.DATETIMEDELTA}", t"case vsqlimpl_pkg.cmp_number_number({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")
GEAST.add_rules(t"{dt.BOOL} <- {[dt.INTLIST, dt.NUMBERLIST]} >= {[dt.INTLIST, dt.NUMBERLIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")
GEAST.add_rules(t"{dt.BOOL} <- {[dt.STRLIST, dt.CLOBLIST]} >= {[dt.STRLIST, dt.CLOBLIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")
GEAST.add_rules(t"{dt.BOOL} <- {[dt.DATELIST, dt.DATETIMELIST]} >= {'T1'}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")
GEAST.add_rules(t"{dt.BOOL} <- {dt.NULLLIST} >= {[dt.NULLLIST, *LIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")
GEAST.add_rules(t"{dt.BOOL} <- {[dt.NULLLIST, *LIST]} >= {dt.NULLLIST}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 0 when 0 then 1 when 1 then 1 end")

# Less-than comparison (A < B)
LTAST.add_rules(t"{dt.BOOL} <- {dt.NULL} < {dt.NULL}", t"0")
LTAST.add_rules(t"{dt.BOOL} <- {ANY} < {dt.NULL}", t"(case when {'s1'} is null then 0 else null end)")
LTAST.add_rules(t"{dt.BOOL} <- {dt.NULL} < {ANY}", t"(case when {'s2'} is null then 0 else null end)")
LTAST.add_rules(t"{dt.BOOL} <- {INTLIKE} < {INTLIKE}", t"case vsqlimpl_pkg.cmp_int_int({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")
LTAST.add_rules(t"{dt.BOOL} <- {NUMBERLIKE} < {NUMBERLIKE}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")
LTAST.add_rules(t"{dt.BOOL} <- {TEXT} < {TEXT}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")
LTAST.add_rules(t"{dt.BOOL} <- {[dt.DATE, dt.DATETIME]} < {'T1'}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")
LTAST.add_rules(t"{dt.BOOL} <- {dt.DATEDELTA} < {dt.DATEDELTA}", t"case vsqlimpl_pkg.cmp_int_int({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")
LTAST.add_rules(t"{dt.BOOL} <- {dt.DATETIMEDELTA} < {dt.DATETIMEDELTA}", t"case vsqlimpl_pkg.cmp_number_number({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")
LTAST.add_rules(t"{dt.BOOL} <- {[dt.INTLIST, dt.NUMBERLIST]} < {[dt.INTLIST, dt.NUMBERLIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")
LTAST.add_rules(t"{dt.BOOL} <- {[dt.STRLIST, dt.CLOBLIST]} < {[dt.STRLIST, dt.CLOBLIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")
LTAST.add_rules(t"{dt.BOOL} <- {[dt.DATELIST, dt.DATETIMELIST]} < {'T1'}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")
LTAST.add_rules(t"{dt.BOOL} <- {dt.NULLLIST} < {[dt.NULLLIST, *LIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")
LTAST.add_rules(t"{dt.BOOL} <- {[dt.NULLLIST, *LIST]} < {dt.NULLLIST}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 0 when 1 then 0 end")

# Less-than-or equal comparison (A <= B)
LEAST.add_rules(t"{dt.BOOL} <- {dt.NULL} <= {dt.NULL}", t"1")
LEAST.add_rules(t"{dt.BOOL} <- {ANY} <= {dt.NULL}", t"(case when {'s1'} is null then 1 else null end)")
LEAST.add_rules(t"{dt.BOOL} <- {dt.NULL} <= {ANY}", t"(case when {'s2'} is null then 1 else null end)")
LEAST.add_rules(t"{dt.BOOL} <- {INTLIKE} <= {INTLIKE}", t"case vsqlimpl_pkg.cmp_int_int({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")
LEAST.add_rules(t"{dt.BOOL} <- {NUMBERLIKE} <= {NUMBERLIKE}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")
LEAST.add_rules(t"{dt.BOOL} <- {TEXT} <= {TEXT}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")
LEAST.add_rules(t"{dt.BOOL} <- {[dt.DATE, dt.DATETIME]} <= {'T1'}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")
LEAST.add_rules(t"{dt.BOOL} <- {dt.DATEDELTA} <= {dt.DATEDELTA}", t"case vsqlimpl_pkg.cmp_int_int({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")
LEAST.add_rules(t"{dt.BOOL} <- {dt.DATETIMEDELTA} <= {dt.DATETIMEDELTA}", t"case vsqlimpl_pkg.cmp_number_number({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")
LEAST.add_rules(t"{dt.BOOL} <- {[dt.INTLIST, dt.NUMBERLIST]} <= {[dt.INTLIST, dt.NUMBERLIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")
LEAST.add_rules(t"{dt.BOOL} <- {[dt.STRLIST, dt.CLOBLIST]} <= {[dt.STRLIST, dt.CLOBLIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")
LEAST.add_rules(t"{dt.BOOL} <- {[dt.DATELIST, dt.DATETIMELIST]} <= {'T1'}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")
LEAST.add_rules(t"{dt.BOOL} <- {dt.NULLLIST} <= {[dt.NULLLIST, *LIST]}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")
LEAST.add_rules(t"{dt.BOOL} <- {[dt.NULLLIST, *LIST]} <= {dt.NULLLIST}", t"case vsqlimpl_pkg.cmp_{'t1'}_{'t2'}({'s1'}, {'s2'}) when -1 then 1 when 0 then 1 when 1 then 0 end")

# Addition (A + B)
AddAST.add_rules(t"{dt.INT} <- {INTLIKE} + {INTLIKE}", t"({'s1'} + {'s2'})")
AddAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} + {NUMBERLIKE}", t"({'s1'} + {'s2'})")
AddAST.add_rules(t"{dt.STR} <- {dt.STR} + {dt.STR}", t"({'s1'} || {'s2'})")
AddAST.add_rules(t"{dt.CLOB} <- {TEXT} + {TEXT}", t"({'s1'} || {'s2'})")
AddAST.add_rules(t"{dt.INTLIST} <- {dt.INTLIST} + {dt.INTLIST}", t"vsqlimpl_pkg.add_intlist_intlist({'s1'}, {'s2'})")
AddAST.add_rules(t"{dt.NUMBERLIST} <- {[dt.INTLIST, dt.NUMBERLIST]} + {[dt.INTLIST, dt.NUMBERLIST]}", t"vsqlimpl_pkg.add_{'t1'}_{'t2'}({'s1'}, {'s2'})")
AddAST.add_rules(t"{dt.STRLIST} <- {dt.STRLIST} + {dt.STRLIST}", t"vsqlimpl_pkg.add_strlist_strlist({'s1'}, {'s2'})")
AddAST.add_rules(t"{dt.CLOBLIST} <- {[dt.STRLIST, dt.CLOBLIST]} + {[dt.STRLIST, dt.CLOBLIST]}", t"vsqlimpl_pkg.add_{'t1'}_{'t2'}({'s1'}, {'s2'})")
AddAST.add_rules(t"{'T1'} <- {[dt.DATELIST, dt.DATETIMELIST]} + {'T1'}", t"vsqlimpl_pkg.add_{'t1'}_{'t2'}({'s1'}, {'s2'})")
AddAST.add_rules(t"{dt.NULLLIST} <- {dt.NULLLIST} + {dt.NULLLIST}", t"({'s1'} + {'s2'})")
AddAST.add_rules(t"{'T2'} <- {dt.NULLLIST} + {[dt.NULLLIST, *LIST]}", t"vsqlimpl_pkg.add_{'t1'}_{'t2'}({'s1'}, {'s2'})")
AddAST.add_rules(t"{'T1'} <- {[dt.NULLLIST, *LIST]} + {dt.NULLLIST}", t"vsqlimpl_pkg.add_{'t1'}_{'t2'}({'s1'}, {'s2'})")
AddAST.add_rules(t"{dt.DATE} <- {dt.DATE} + {dt.DATEDELTA}", t"({'s1'} + {'s2'})")
AddAST.add_rules(t"{dt.DATETIME} <- {dt.DATETIME} + {[dt.DATEDELTA, dt.DATETIMEDELTA]}", t"({'s1'} + {'s2'})")
AddAST.add_rules(t"{'T1'} <- {[dt.DATE, dt.DATETIME]} + {dt.MONTHDELTA}", t"vsqlimpl_pkg.add_{'t1'}_months({'s1'}, {'s2'})")
AddAST.add_rules(t"{'T2'} <- {dt.MONTHDELTA} + {[dt.DATE, dt.DATETIME]}", t"vsqlimpl_pkg.add_months_{'t2'}({'s1'}, {'s2'})")
AddAST.add_rules(t"{dt.DATEDELTA} <- {dt.DATEDELTA} + {dt.DATEDELTA}", t"({'s1'} + {'s2'})")
AddAST.add_rules(t"{dt.DATETIMEDELTA} <- {[dt.DATEDELTA, dt.DATETIMEDELTA]} + {[dt.DATEDELTA, dt.DATETIMEDELTA]}", t"({'s1'} + {'s2'})")
AddAST.add_rules(t"{dt.MONTHDELTA} <- {dt.MONTHDELTA} + {dt.MONTHDELTA}", t"({'s1'} + {'s2'})")

# Subtraction (A - B)
SubAST.add_rules(t"{dt.INT} <- {INTLIKE} - {INTLIKE}", t"({'s1'} - {'s2'})")
SubAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} - {NUMBERLIKE}", t"({'s1'} - {'s2'})")
SubAST.add_rules(t"{dt.DATE} <- {dt.DATE} - {dt.DATEDELTA}", t"({'s1'} - {'s2'})")
SubAST.add_rules(t"{dt.DATEDELTA} <- {dt.DATE} - {dt.DATE}", t"({'s1'} - {'s2'})")
SubAST.add_rules(t"{dt.DATETIMEDELTA} <- {dt.DATETIME} - {dt.DATETIME}", t"({'s1'} - {'s2'})")
SubAST.add_rules(t"{'T1'} <- {[dt.DATE, dt.DATETIME]} - {dt.MONTHDELTA}", t"vsqlimpl_pkg.add_{'t1'}_months({'s1'}, -{'s2'})")
SubAST.add_rules(t"{dt.DATETIME} <- {dt.DATETIME} - {[dt.DATEDELTA, dt.DATETIMEDELTA]}", t"({'s1'} - {'s2'})")
SubAST.add_rules(t"{'T1'} <- {[dt.DATEDELTA, dt.MONTHDELTA]} - {'T1'}", t"({'s1'} - {'s2'})")
SubAST.add_rules(t"{dt.DATETIMEDELTA} <- {[dt.DATEDELTA, dt.DATETIMEDELTA]} - {[dt.DATEDELTA, dt.DATETIMEDELTA]}", t"({'s1'} - {'s2'})")

# Multiplication (A * B)
MulAST.add_rules(t"{dt.INT} <- {INTLIKE} * {INTLIKE}", t"({'s1'} * {'s2'})")
MulAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} * {NUMBERLIKE}", t"({'s1'} * {'s2'})")
MulAST.add_rules(t"{'T2'} <- {INTLIKE} * {[dt.DATEDELTA, dt.DATETIMEDELTA, dt.MONTHDELTA]}", t"({'s1'} * {'s2'})")
MulAST.add_rules(t"{dt.DATETIMEDELTA} <- {dt.NUMBER} * {dt.DATETIMEDELTA}", t"({'s1'} * {'s2'})")
MulAST.add_rules(t"{'T2'} <- {INTLIKE} * {TEXT}", t"vsqlimpl_pkg.mul_int_{'t2'}({'s1'}, {'s2'})")
MulAST.add_rules(t"{'T1'} <- {TEXT} * {INTLIKE}", t"vsqlimpl_pkg.mul_{'t1'}_int({'s1'}, {'s2'})")
MulAST.add_rules(t"{'T2'} <- {INTLIKE} * {LIST}", t"vsqlimpl_pkg.mul_int_{'t2'}({'s1'}, {'s2'})")
MulAST.add_rules(t"{'T1'} <- {LIST} * {INTLIKE}", t"vsqlimpl_pkg.mul_{'t1'}_int({'s1'}, {'s2'})")
MulAST.add_rules(t"{dt.NULLLIST} <- {INTLIKE} * {dt.NULLLIST}", t"({'s1'} * {'s2'})")
MulAST.add_rules(t"{dt.NULLLIST} <- {dt.NULLLIST} * {INTLIKE}", t"({'s1'} * {'s2'})")

# True division (A / B)
TrueDivAST.add_rules(t"{dt.INT} <- {dt.BOOL} / {dt.BOOL}", t"({'s1'} / {'s2'})")
TrueDivAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} / {NUMBERLIKE}", t"({'s1'} / {'s2'})")
TrueDivAST.add_rules(t"{dt.DATETIMEDELTA} <- {dt.DATETIMEDELTA} / {NUMBERLIKE}", t"({'s1'} / {'s2'})")

# Floor division (A // B)
FloorDivAST.add_rules(t"{dt.INT} <- {NUMBERLIKE} // {NUMBERLIKE}", t"vsqlimpl_pkg.floordiv_{'t1'}_{'t2'}({'s1'}, {'s2'})")
FloorDivAST.add_rules(t"{'T1'} <- {[dt.DATEDELTA, dt.MONTHDELTA]} // {INTLIKE}", t"vsqlimpl_pkg.floordiv_int_int({'s1'}, {'s2'})")
FloorDivAST.add_rules(t"{dt.DATEDELTA} <- {dt.DATETIMEDELTA} // {NUMBERLIKE}", t"vsqlimpl_pkg.floordiv_number_int({'s1'}, {'s2'})")

# Modulo operator (A % B)
ModAST.add_rules(t"{dt.INT} <- {INTLIKE} % {INTLIKE}", t"vsqlimpl_pkg.mod_int_int({'s1'}, {'s2'})")
ModAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} % {NUMBERLIKE}", t"vsqlimpl_pkg.mod_{'t1'}_{'t2'}({'s1'}, {'s2'})")
ModAST.add_rules(t"{dt.COLOR} <- {dt.COLOR} % {dt.COLOR}", t"vsqlimpl_pkg.mod_color_color({'s1'}, {'s2'})")

# Left shift operator (A << B)
ShiftLeftAST.add_rules(t"{dt.INT} <- {INTLIKE} << {INTLIKE}", t"trunc({'s1'} * power(2, {'s2'}))")

# Right shift operator (A >> B)
ShiftRightAST.add_rules(t"{dt.INT} <- {INTLIKE} >> {INTLIKE}", t"trunc({'s1'} / power(2, {'s2'}))")

# Logical "and" (A and B)
AndAST.add_rules(t"{'T1'} <- {ANY} and {dt.NULL}", t"null")
AndAST.add_rules(t"{'T2'} <- {dt.NULL} and {ANY}", t"null")
AndAST.add_rules(t"{dt.BOOL} <- {dt.BOOL} and {dt.BOOL}", t"(case when {'s1'} = 1 then {'s2'} else 0 end)")
AndAST.add_rules(t"{dt.INT} <- {INTLIKE} and {INTLIKE}", t"(case when nvl({'s1'}, 0) != 0 then {'s2'} else {'s1'} end)")
AndAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} and {NUMBERLIKE}", t"(case when nvl({'s1'}, 0) != 0 then {'s2'} else {'s1'} end)")
AndAST.add_rules(t"{dt.STR} <- {dt.STR} and {dt.STR}", t"nvl2({'s1'}, {'s2'}, {'s1'})")
AndAST.add_rules(t"{dt.CLOB} <- {dt.STR} and {dt.CLOB}", t"(case when {'s1'} is not null then {'s2'} else to_clob({'s1'}) end)")
AndAST.add_rules(t"{dt.CLOB} <- {dt.CLOB} and {dt.CLOB}", t"(case when {'s1'} is not null and length({'s1'}) != 0 then {'s2'} else {'s1'} end)")
AndAST.add_rules(t"{dt.CLOB} <- {dt.CLOB} and {dt.STR}", t"(case when {'s1'} is not null and length({'s1'}) != 0 then to_clob({'s2'}) else {'s1'} end)")
AndAST.add_rules(t"{'T1'} <- {[dt.DATE, dt.DATETIME]} and {'T1'}", t"nvl2({'s1'}, {'s2'}, {'s1'})")
AndAST.add_rules(t"{'T1'} <- {[dt.DATEDELTA, dt.DATETIMEDELTA, dt.MONTHDELTA]} and {'T1'}", t"(case when nvl({'s1'}, 0) != 0 then {'s2'} else {'s1'} end)")
AndAST.add_rules(t"{'T1'} <- {LIST} and {'T1'}", t"(case when nvl(vsqlimpl_pkg.len_{'t1'}({'s1'}), 0) != 0 then {'s2'} else {'s1'} end)")
AndAST.add_rules(t"{dt.DATETIMELIST} <- {[dt.DATELIST, dt.DATETIMELIST]} and {[dt.DATELIST, dt.DATETIMELIST]}", t"(case when nvl(vsqlimpl_pkg.len_{'t1'}({'s1'}), 0) != 0 then {'s2'} else {'s1'} end)")
AndAST.add_rules(t"{dt.NULLLIST} <- {dt.NULLLIST} and {dt.NULLLIST}", t"(case when nvl({'s1'}, 0) != 0 then {'s2'} else {'s1'} end)")
AndAST.add_rules(t"{'T2'} <- {dt.NULLLIST} and {LIST}", t"(case when nvl({'s1'}, 0) != 0 then {'s2'} else vsqlimpl_pkg.{'t2'}_fromlen({'s1'}) end)")
AndAST.add_rules(t"{'T1'} <- {LIST} and {dt.NULLLIST}", t"(case when nvl(vsqlimpl_pkg.len_{'t1'}({'s1'}), 0) != 0 then vsqlimpl_pkg.{'t1'}_fromlen({'s2'}) else {'s1'} end)")

# Logical "or" (A or B)
OrAST.add_rules(t"{'T1'} <- {ANY} or {dt.NULL}", t"{'s1'}")
OrAST.add_rules(t"{'T2'} <- {dt.NULL} or {ANY}", t"{'s2'}")
OrAST.add_rules(t"{dt.BOOL} <- {dt.BOOL} or {dt.BOOL}", t"(case when {'s1'} = 1 then 1 else {'s2'} end)")
OrAST.add_rules(t"{dt.INT} <- {INTLIKE} or {INTLIKE}", t"(case when nvl({'s1'}, 0) != 0 then {'s1'} else {'s2'} end)")
OrAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} or {NUMBERLIKE}", t"(case when nvl({'s1'}, 0) != 0 then {'s1'} else {'s2'} end)")
OrAST.add_rules(t"{dt.STR} <- {dt.STR} or {dt.STR}", t"nvl({'s1'}, {'s2'})")
OrAST.add_rules(t"{dt.CLOB} <- {dt.STR} or {dt.CLOB}", t"(case when {'s1'} is not null then to_clob({'s1'}) else {'s2'} end)")
OrAST.add_rules(t"{dt.CLOB} <- {dt.CLOB} or {dt.CLOB}", t"(case when {'s1'} is not null and length({'s1'}) != 0 then {'s1'} else {'s2'} end)")
OrAST.add_rules(t"{dt.CLOB} <- {dt.CLOB} or {dt.STR}", t"(case when {'s1'} is not null and length({'s1'}) != 0 then {'s1'} else to_clob({'s2'}) end)")
OrAST.add_rules(t"{'T1'} <- {[dt.DATE, dt.DATETIME]} or {'T1'}", t"nvl({'s1'}, {'s2'})")
OrAST.add_rules(t"{'T1'} <- {[dt.DATEDELTA, dt.DATETIMEDELTA, dt.MONTHDELTA]} or {'T1'}", t"(case when nvl({'s1'}, 0) != 0 then {'s1'} else {'s2'} end)")
OrAST.add_rules(t"{'T1'} <- {LIST} or {'T1'}", t"(case when nvl(vsqlimpl_pkg.len_{'t1'}({'s1'}), 0) != 0 then {'s1'} else {'s2'} end)")
OrAST.add_rules(t"{dt.DATETIMELIST} <- {[dt.DATELIST, dt.DATETIMELIST]} or {[dt.DATELIST, dt.DATETIMELIST]}", t"(case when nvl(vsqlimpl_pkg.len_{'t1'}({'s1'}), 0) != 0 then {'s1'} else {'s2'} end)")
OrAST.add_rules(t"{dt.NULLLIST} <- {dt.NULLLIST} or {dt.NULLLIST}", t"(case when nvl({'s1'}, 0) != 0 then {'s1'} else {'s2'} end)")
OrAST.add_rules(t"{'T2'} <- {dt.NULLLIST} or {LIST}", t"(case when nvl({'s1'}, 0) != 0 then vsqlimpl_pkg.{'t2'}_fromlen({'s1'}) else {'s2'} end)")
OrAST.add_rules(t"{'T1'} <- {LIST} or {dt.NULLLIST}", t"(case when nvl(vsqlimpl_pkg.len_{'t1'}({'s1'}), 0) != 0 then {'s1'} else vsqlimpl_pkg.{'t1'}_fromlen({'s2'}) end)")

# Containment test (A in B)
ContainsAST.add_rules(t"{dt.BOOL} <- {dt.NULL} in {[*LIST, dt.NULLLIST]}", t"vsqlimpl_pkg.contains_null_{'t2'}({'s2'})")
ContainsAST.add_rules(t"{dt.BOOL} <- {[dt.STR, dt.CLOB]} in {[dt.STR, dt.CLOB, dt.STRLIST, dt.CLOBLIST, dt.STRSET]}", t"vsqlimpl_pkg.contains_{'t1'}_{'t2'}({'s1'}, {'s2'})")
ContainsAST.add_rules(t"{dt.BOOL} <- {[dt.INT, dt.NUMBER]} in {[dt.INTLIST, dt.NUMBERLIST, dt.INTSET, dt.NUMBERSET]}", t"vsqlimpl_pkg.contains_{'t1'}_{'t2'}({'s1'}, {'s2'})")
ContainsAST.add_rules(t"{dt.BOOL} <- {dt.DATE} in {[dt.DATELIST, dt.DATESET]}", t"vsqlimpl_pkg.contains_{'t1'}_{'t2'}({'s1'}, {'s2'})")
ContainsAST.add_rules(t"{dt.BOOL} <- {dt.DATETIME} in {[dt.DATETIMELIST, dt.DATETIMESET]}", t"vsqlimpl_pkg.contains_{'t1'}_{'t2'}({'s1'}, {'s2'})")
ContainsAST.add_rules(t"{dt.BOOL} <- {ANY} in {dt.NULLLIST}", t"case when {'s1'} is null then vsqlimpl_pkg.contains_null_nulllist({'s2'}) else 0 end")

# Inverted containment test (A not in B)
NotContainsAST.add_rules(t"{dt.BOOL} <- {dt.NULL} not in {[*LIST, dt.NULLLIST]}", t"(1 - vsqlimpl_pkg.contains_null_{'t2'}({'s2'}))")
NotContainsAST.add_rules(t"{dt.BOOL} <- {[dt.STR, dt.CLOB]} not in {[dt.STR, dt.CLOB, dt.STRLIST, dt.CLOBLIST, dt.STRSET]}", t"(1 - vsqlimpl_pkg.contains_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NotContainsAST.add_rules(t"{dt.BOOL} <- {[dt.INT, dt.NUMBER]} not in {[dt.INTLIST, dt.NUMBERLIST, dt.INTSET, dt.NUMBERSET]}", t"(1 - vsqlimpl_pkg.contains_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NotContainsAST.add_rules(t"{dt.BOOL} <- {dt.DATE} not in {[dt.DATELIST, dt.DATESET]}", t"(1 - vsqlimpl_pkg.contains_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NotContainsAST.add_rules(t"{dt.BOOL} <- {dt.DATETIME} not in {[dt.DATETIMELIST, dt.DATETIMESET]}", t"(1 - vsqlimpl_pkg.contains_{'t1'}_{'t2'}({'s1'}, {'s2'}))")
NotContainsAST.add_rules(t"{dt.BOOL} <- {ANY} not in {dt.NULLLIST}", t"case when {'s1'} is null then 1 - vsqlimpl_pkg.contains_null_nulllist({'s2'}) else 1 end")

# Identity test (A is B)
IsAST.add_rules(t"{dt.BOOL} <- {dt.NULL} is {dt.NULL}", t"1")
IsAST.add_rules(t"{dt.BOOL} <- {ANY} is {dt.NULL}", t"(case when {'s1'} is null then 1 else 0 end)")
IsAST.add_rules(t"{dt.BOOL} <- {dt.NULL} is {ANY}", t"(case when {'s2'} is null then 1 else 0 end)")

# Inverted identity test (A is not B)
IsNotAST.add_rules(t"{dt.BOOL} <- {dt.NULL} is not {dt.NULL}", t"0")
IsNotAST.add_rules(t"{dt.BOOL} <- {ANY} is not {dt.NULL}", t"(case when {'s1'} is not null then 1 else 0 end)")
IsNotAST.add_rules(t"{dt.BOOL} <- {dt.NULL} is not {ANY}", t"(case when {'s2'} is not null then 1 else 0 end)")

# Item access operator (A[B])
ItemAST.add_rules(t"{dt.NULL} <- {dt.NULLLIST}[{INTLIKE}]", t"null")
ItemAST.add_rules(t"{dt.STR} <- {[dt.STR, dt.CLOB, dt.STRLIST]}[{INTLIKE}]", t"vsqlimpl_pkg.item_{'t1'}({'s1'}, {'s2'})")
ItemAST.add_rules(t"{dt.CLOB} <- {dt.CLOBLIST}[{INTLIKE}]", t"vsqlimpl_pkg.item_{'t1'}({'s1'}, {'s2'})")
ItemAST.add_rules(t"{dt.INT} <- {dt.INTLIST}[{INTLIKE}]", t"vsqlimpl_pkg.item_{'t1'}({'s1'}, {'s2'})")
ItemAST.add_rules(t"{dt.NUMBER} <- {dt.NUMBERLIST}[{INTLIKE}]", t"vsqlimpl_pkg.item_{'t1'}({'s1'}, {'s2'})")
ItemAST.add_rules(t"{dt.DATE} <- {dt.DATELIST}[{INTLIKE}]", t"vsqlimpl_pkg.item_{'t1'}({'s1'}, {'s2'})")
ItemAST.add_rules(t"{dt.DATETIME} <- {dt.DATETIMELIST}[{INTLIKE}]", t"vsqlimpl_pkg.item_{'t1'}({'s1'}, {'s2'})")

# Bitwise "and" (A & B)
BitAndAST.add_rules(t"{dt.INT} <- {INTLIKE} & {INTLIKE}", t"bitand({'s1'}, {'s2'})")
BitAndAST.add_rules(t"{'T1'} <- {dt.INTSET} & {dt.INTSET}", t"vsqlimpl_pkg.bitand_intset({'s1'}, {'s2'})")
BitAndAST.add_rules(t"{'T1'} <- {dt.NUMBERSET} & {dt.NUMBERSET}", t"vsqlimpl_pkg.bitand_numberset({'s1'}, {'s2'})")
BitAndAST.add_rules(t"{'T1'} <- {dt.STRSET} & {dt.STRSET}", t"vsqlimpl_pkg.bitand_strset({'s1'}, {'s2'})")
BitAndAST.add_rules(t"{'T1'} <- {[dt.DATESET, dt.DATETIMESET]} & {'T1'}", t"vsqlimpl_pkg.bitand_datetimeset({'s1'}, {'s2'})")

# Bitwise "or" (A | B)
BitOrAST.add_rules(t"{dt.INT} <- {INTLIKE} | {INTLIKE}", t"vsqlimpl_pkg.bitor_int({'s1'}, {'s2'})")
BitOrAST.add_rules(t"{'T1'} <- {dt.INTSET} | {dt.INTSET}", t"vsqlimpl_pkg.bitor_intset({'s1'}, {'s2'})")
BitOrAST.add_rules(t"{'T1'} <- {dt.NUMBERSET} | {dt.NUMBERSET}", t"vsqlimpl_pkg.bitor_numberset({'s1'}, {'s2'})")
BitOrAST.add_rules(t"{'T1'} <- {dt.STRSET} | {dt.STRSET}", t"vsqlimpl_pkg.bitor_strset({'s1'}, {'s2'})")
BitOrAST.add_rules(t"{'T1'} <- {[dt.DATESET, dt.DATETIMESET]} | {'T1'}", t"vsqlimpl_pkg.bitor_datetimeset({'s1'}, {'s2'})")

# Bitwise "exclusive or" (A ^ B)
BitXOrAST.add_rules(t"{dt.INT} <- {INTLIKE} ^ {INTLIKE}", t"vsqlimpl_pkg.bitxor_int({'s1'}, {'s2'})")

# Logical negation (not A)
NotAST.add_rules(t"{dt.BOOL} <- not {dt.NULL}", t"1")
NotAST.add_rules(t"{dt.BOOL} <- not {dt.BOOL}", t"(case {'s1'} when 1 then 0 else 1 end)")
NotAST.add_rules(t"{dt.BOOL} <- not {[dt.INT, dt.NUMBER, dt.DATEDELTA, dt.DATETIMEDELTA, dt.MONTHDELTA]}", t"(case nvl({'s1'}, 0) when 0 then 1 else 0 end)")
NotAST.add_rules(t"{dt.BOOL} <- not {[dt.DATE, dt.DATETIME, dt.STR, dt.COLOR, dt.GEO]}", t"(case when {'s1'} is null then 1 else 0 end)")
NotAST.add_rules(t"{dt.BOOL} <- not {ANY}", t"(1 - vsqlimpl_pkg.bool_{'t1'}({'s1'}))")

# Arithmetic negation (-A)
NegAST.add_rules(t"{dt.INT} <- {dt.BOOL}", t"(-{'s1'})")
NegAST.add_rules(t"{'T1'} <- {[dt.INT, dt.NUMBER, dt.DATEDELTA, dt.DATETIMEDELTA, dt.MONTHDELTA]}", t"(-{'s1'})")

# Bitwise "not" (~A)
BitNotAST.add_rules(t"{dt.INT} <- {INTLIKE}", t"(-{'s1'} - 1)")

# Ternary "if"/"else" (A if COND else B)
IfAST.add_rules(t"{'T1'} <- {ANY} if {dt.NULL} else {'T1'}", t"{'s3'}")
IfAST.add_rules(t"{dt.INT} <- {INTLIKE} if {dt.NULL} else {INTLIKE}", t"{'s3'}")
IfAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} if {dt.NULL} else {NUMBERLIKE}", t"{'s3'}")
IfAST.add_rules(t"{'T1'} <- {ANY} if {dt.NULL} else {dt.NULL}", t"{'s3'}")
IfAST.add_rules(t"{'T3'} <- {dt.NULL} if {dt.NULL} else {ANY}", t"{'s3'}")
IfAST.add_rules(t"{'T1'} <- {ANY} if {NUMBERSTORED} else {'T1'}", t"(case when nvl({'s2'}, 0) != 0 then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{dt.INT} <- {INTLIKE} if {NUMBERSTORED} else {INTLIKE}", t"(case when nvl({'s2'}, 0) != 0 then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} if {NUMBERSTORED} else {NUMBERLIKE}", t"(case when nvl({'s2'}, 0) != 0 then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{'T1'} <- {ANY} if {NUMBERSTORED} else {dt.NULL}", t"(case when nvl({'s2'}, 0) != 0 then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{'T3'} <- {dt.NULL} if {NUMBERSTORED} else {ANY}", t"(case when nvl({'s2'}, 0) != 0 then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{'T1'} <- {ANY} if {[dt.DATE, dt.DATETIME, dt.STR, dt.GEO]} else {'T1'}", t"(case when {'s2'} is not null then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{dt.INT} <- {INTLIKE} if {[dt.DATE, dt.DATETIME, dt.STR, dt.GEO]} else {INTLIKE}", t"(case when {'s2'} is not null then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} if {[dt.DATE, dt.DATETIME, dt.STR, dt.GEO]} else {NUMBERLIKE}", t"(case when {'s2'} is not null then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{'T1'} <- {ANY} if {[dt.DATE, dt.DATETIME, dt.STR, dt.GEO]} else {dt.NULL}", t"(case when {'s2'} is not null then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{'T3'} <- {dt.NULL} if {[dt.DATE, dt.DATETIME, dt.STR, dt.GEO]} else {ANY}", t"(case when {'s2'} is not null then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{'T1'} <- {ANY} if {ANY} else {'T1'}", t"(case when vsqlimpl_pkg.bool_{'t2'}({'s2'}) = 1 then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{dt.INT} <- {INTLIKE} if {ANY} else {INTLIKE}", t"(case when vsqlimpl_pkg.bool_{'t2'}({'s2'}) = 1 then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{dt.NUMBER} <- {NUMBERLIKE} if {ANY} else {NUMBERLIKE}", t"(case when vsqlimpl_pkg.bool_{'t2'}({'s2'}) = 1 then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{'T1'} <- {ANY} if {ANY} else {dt.NULL}", t"(case when vsqlimpl_pkg.bool_{'t2'}({'s2'}) = 1 then {'s1'} else {'s3'} end)")
IfAST.add_rules(t"{'T3'} <- {dt.NULL} if {ANY} else {ANY}", t"(case when vsqlimpl_pkg.bool_{'t2'}({'s2'}) = 1 then {'s1'} else {'s3'} end)")

# Slice operator (A[B:C])
SliceAST.add_rules(t"{'T1'} <- {[*TEXT, *LIST]}[{[dt.NULL, *INTLIKE]}:{[dt.NULL, *INTLIKE]}]", t"vsqlimpl_pkg.slice_{'t1'}({'s1'}, {'s2'}, {'s3'})")
SliceAST.add_rules(t"{dt.NULLLIST} <- {dt.NULLLIST}[{[dt.NULL, *INTLIKE]}:{[dt.NULL, *INTLIKE]}]", t"vsqlimpl_pkg.slice_{'t1'}({'s1'}, {'s2'}, {'s3'})")


###
### Class for regenerating the Java type information.
###

class JavaSource:
	"""
	A :class:`JavaSource` object combines the source code of a Java class that
	implements a vSQL AST type with the Python class that implements that AST
	type.

	It is used to update the vSQL syntax rules in the Java implemenation of vSQL.
	"""

	_start_line = "//BEGIN RULES (don't remove this comment)"
	_end_line = "//END RULES (don't remove this comment)"

	def __init__(self, astcls:Type[AST], path:pathlib.Path):
		self.astcls = astcls
		self.path = path
		self.lines = path.read_text(encoding="utf-8").splitlines(False)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} cls={self.astcls!r} path={str(self.path)!r} at {id(self):#x}>"

	def new_lines(self) -> Generator[str, None, None]:
		"""
		Return an iterator over the new Java source code lines that should
		replace the static initialization block inside the Java source file.
		"""

		# How many ``addRule()`` calls to pack in one static method.
		# This avoids the ``code too large`` error from the Java compiler.
		bunch = 100

		number = 0

		yield f"\t{self._start_line}"
		for (i, rule) in enumerate(self.astcls.rules.values()):
			if i % bunch == 0:
				number += 1
				yield f"\tprivate static void addRulesPart{number}()"
				yield "\t{"
			yield f"\t\t{rule.java_source()}"
			if i % bunch == bunch-1:
				yield "\t}"
				yield ""

		if i % bunch != bunch-1:
			yield "\t}"
			yield ""

		yield f"\tstatic"
		yield "\t{"
		for i in range(1, number+1):
			yield f"\t\taddRulesPart{i}();"
		yield "\t}"

		yield f"\t{self._end_line}"

	def save(self) -> None:
		"""
		Resave the Java source code incorporating the new vSQL type info from the
		Python AST class.
		"""
		inrules = False

		with self.path.open("w", encoding="utf-8") as f:
			for line in self.lines:
				if inrules:
					if line.strip() == self._end_line:
						inrules = False
				else:
					if line.strip() == self._start_line:
						inrules = True
						for new_line in self.new_lines():
							f.write(f"{new_line}\n")
					else:
						f.write(f"{line}\n")

	@classmethod
	def all_java_source_files(cls, path: pathlib.Path) -> Generator[JavaSource, None, None]:
		"""
		Return an iterator over all :class:`!JavaSource` objects for vSQL AST nodes
		that can be found in the directory ``path``. ``path`` should point to the
		directory containing the Java vSQL AST classes.
		"""

		# Find all AST classes that have rules
		classes = {"vsql" + cls.__name__.lower(): cls for cls in AST.all_types() if hasattr(cls, "rules")}

		for filename in path.glob("**/*.java"):
			try:
				# Do we have a Python class for this Java source?
				cls = classes[filename.stem.lower()]
			except KeyError:
				pass
			else:
				yield JavaSource(cls, filename)

	@classmethod
	def rewrite_all_java_source_files(cls, path:pathlib.Path, verbose:bool=False) -> None:
		"""
		Rewrite all Java source code files implementing Java vSQL AST classes
		in the directory ``path``. ``path`` should point to the directory
		containing the Java vSQL AST classes.
		"""
		if verbose:
			print(f"Rewriting Java source files in {str(path)!r}")
		for javasource in cls.all_java_source_files(path):
			javasource.save()


###
### Functions for regenerating the Oracle type information.
###

def oracle_sql_table() -> str:
	"""
	Return the SQL statement for creating the table ``VSQLRULE``.
	"""

	recordfields = [rule.oracle_fields() for rule in AST.all_rules()]

	sql = []
	sql.append("create table vsqlrule")
	sql.append("(")
	for (i, (fieldname, fieldtype)) in enumerate(fields.items()):
		term = "" if i == len(fields)-1 else ","
		if fieldname == "vr_cname":
			sql.append(f"\t{fieldname} varchar2(200) not null{term}")
		elif fieldtype is int:
			sql.append(f"\t{fieldname} integer not null{term}")
		elif fieldtype == int | None:
			sql.append(f"\t{fieldname} integer{term}")
		elif fieldtype is datetime.datetime:
			sql.append(f"\t{fieldname} date not null{term}")
		elif fieldtype is str:
			size = max(len(r[fieldname]) for r in recordfields if fieldname in r and r[fieldname])
			sql.append(f"\t{fieldname} varchar2({size}) not null{term}")
		elif fieldtype == str | None:
			size = max(len(r[fieldname]) for r in recordfields if fieldname in r and r[fieldname])
			sql.append(f"\t{fieldname} varchar2({size}){term}")
		else:
			raise ValueError(f"unknown field type {fieldtype!r}")
	sql.append(")")
	return "\n".join(sql)


def oracle_sql_procedure() -> str:
	"""
	Return the SQL statement for creating the procedure ``VSQLGRAMMAR_MAKE``.
	"""

	sql = []
	sql.append("create or replace procedure vsqlgrammar_make(c_user varchar2)")
	sql.append("as")
	sql.append("begin")
	sql.append("\tdelete from vsqlrule;")
	for rule in AST.all_rules():
		sql.append(f"\t{rule.oracle_source()}")
	sql.append("end;")
	return "\n".join(sql)


def oracle_sql_index() -> str:
	"""
	Return the SQL statement for creating the index ``VSQLRULE_I1``.
	"""

	return "create unique index vsqlrule_i1 on vsqlrule(vr_nodetype, vr_value, vr_signature, vr_arity)"


def oracle_sql_tablecomment() -> str:
	"""
	Return the SQL statement for creating a comment on the table ``VSQLRULE``.
	"""

	return "comment on table vsqlrule is 'Syntax rules for vSQL expressions.'"


def recreate_oracle(connectstring:str, verbose:bool=False) -> None:
	"""
	Recreate the vSQL syntax rules in the database.

	This recreates the procedure ``VSQLGRAMMAR_MAKE`` and the table ``VSQLRULE``
	and its content.
	"""

	from ll import orasql

	orasql.init_oracle_client()

	db = orasql.connect(connectstring, readlobs=True)
	cursor = db.cursor()

	oldtable = orasql.Table("VSQLRULE", connection=db)
	try:
		oldsql = oldtable.createsql(term=False).strip().lower().replace(" byte)", ")")
	except orasql.SQLObjectNotFoundError:
		oldsql = None

	newsql = oracle_sql_table()

	if oldsql is not None and oldsql != newsql:
		if verbose:
			print(f"Dropping old table VSQLRULE in {db.connectstring()!r}", file=sys.stderr)
		cursor.execute("drop table vsqlrule")
	if oldsql != newsql:
		if verbose:
			print(f"Creating new table VSQLRULE in {db.connectstring()!r}", file=sys.stderr)
		cursor.execute(newsql)
		if verbose:
			print(f"Creating index VSQLRULE_I1 in {db.connectstring()!r}", file=sys.stderr)
		cursor.execute(oracle_sql_index())
		if verbose:
			print(f"Creating table comment for VSQLRULE in {db.connectstring()!r}", file=sys.stderr)
		cursor.execute(oracle_sql_tablecomment())
	if verbose:
		print(f"Creating procedure VSQLGRAMMAR_MAKE in {db.connectstring()!r}", file=sys.stderr)
	cursor.execute(oracle_sql_procedure())
	if verbose:
		print(f"Calling procedure VSQLGRAMMAR_MAKE in {db.connectstring()!r}", file=sys.stderr)
	cursor.execute(f"begin vsqlgrammar_make('{scriptname}'); end;")
	if verbose:
		print(f"Committing transaction in {db.connectstring()!r}", file=sys.stderr)
	db.commit()


def main(args:tuple[str, ...] | None=None) -> None:
	import argparse
	p = argparse.ArgumentParser(description="Recreate vSQL type info for the Java and Oracle implementations")
	p.add_argument("-c", "--connectstring", help="Oracle database where the table VSQLRULE and the procedure VSQLGRAMMAR_MAKE will be created")
	p.add_argument("-j", "--javapath", dest="javapath", help="Path to the Java implementation of vSQL", type=pathlib.Path)
	p.add_argument("-v", "--verbose", dest="verbose", help="Give a progress report? (default %(default)s)", default=False, action="store_true")

	args = p.parse_args(args)

	if args.connectstring:
		recreate_oracle(args.connectstring, verbose=args.verbose)
	if args.javapath:
		JavaSource.rewrite_all_java_source_files(args.javapath, verbose=args.verbose)


if __name__ == "__main__":
	sys.exit(main())
