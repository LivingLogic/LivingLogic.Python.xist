# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2009-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`!ll.ul4c` provides templating for XML/HTML as well as any other text-based
format. A template defines placeholders for data output and basic logic (like
loops and conditional blocks), that define how the final rendered output will
look.

:mod:`!ll.ul4c` compiles a template to an internal format, which makes it
possible to implement template renderers in multiple programming languages.
"""


__docformat__ = "reStructuredText"


import re, os.path, datetime, urllib.parse as urlparse, json, collections, locale, itertools, random, functools, math, inspect, contextlib
from collections import abc

import antlr3

from ll import misc


# Regular expression used for splitting dates in isoformat
_datesplitter = re.compile("[-T:.]")


_defaultitem = object()


def register(name):
	from ll import ul4on

	def registration(cls):
		ul4on.register("de.livinglogic.ul4." + name)(cls)
		cls.type = name
		return cls
	return registration


def withcontext(f):
	"""
	Normally when a function is exposed to UL4 this function will be called
	directly.

	However when the function needs access to the rendering context (i.e. the
	local variables or information about the call stack), the function must have
	an additional first parameter, and UL4 must be told that this parmeter is
	required.

	This can be done with this decorator.
	"""
	f.ul4context = True
	return f


error_underline = os.environ.get("LL_UL4_ERRORUNDERLINE", "~")[:1] or "~"


###
### Exceptions
###

class LocationError(Exception):
	"""
	Exception class that provides a location inside an UL4 template.

	If an exception happens inside an UL4 template, this exception will propagate
	outwards and will be decorated with :class:`LocationError` instances which
	will be chained via the ``__cause__`` attribute. Only the original exception
	will be reraised again and again, so these :class:`LocationError` will never
	have a traceback attached to them.

	The first ``__cause__`` attribute marks the location in the UL4 source where
	the exception happened and the last ``__cause__`` attribute at the end of the
	exception chain marks the outermost call.
	"""
	def __init__(self, location):
		self.location = location

	_condensewhitespace = re.compile("[\t\n\r\f\v]+")

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} in {self.location} offset {_offset(self.location.pos)} at {id(self):#x}>"

	def strtemplate(self):
		template = self.location.template
		prefix = "in local template" if template.parenttemplate is not None else "in template"
		out = []
		while template is not None:
			out.append(repr(template.name) if template.name is not None else "(unnamed)")
			template = template.parenttemplate
		return f"{prefix} {' in '.join(out)}"

	def strlocation(self):
		loc = self.location
		return f"offset {_offset(loc.startpos)}; line {loc.startline:,}; col {loc.startcol:,}"

	def __str__(self):
		prefix = repr(self._condensewhitespace.sub(" ", self.location.startsourceprefix))[1:-1]
		source = repr(self._condensewhitespace.sub(" ", self.location.startsource))[1:-1]
		suffix = repr(self._condensewhitespace.sub(" ", self.location.startsourcesuffix))[1:-1]
		indent = ' '*len(prefix)
		underline = error_underline*len(source)

		return f"{self.strtemplate()}: {self.strlocation()}\n{prefix}{source}{suffix}\n{indent}{underline}"

	def ul4getattr(self, name):
		if name == "context":
			if self.__context__ is not None and not self.__suppress_context__:
				return self.__context__
			elif self.__cause__ is not None:
				return self.__cause__
			return None
		elif name == "location":
			return self.location
		else:
			raise AttributeError(name)


class BlockError(Exception):
	"""
	Exception that is raised by the compiler when an illegal block structure is
	detected (e.g. an ``<?end if?>`` without a previous ``<?if?>``).
	"""

	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message


###
### Exceptions used by the interpreted code for flow control
###

class BreakException(Exception):
	pass


class ContinueException(Exception):
	pass


class ReturnException(Exception):
	def __init__(self, value):
		self.value = value


###
### Various versions of undefined objects
###

class Undefined:
	def __bool__(self):
		return False

	def __iter__(self):
		raise TypeError(f"{self!r} is not iterable")

	def __len__(self):
		raise AttributeError(f"{self!r} has no len()")

	def __call__(self, *args, **kwargs):
		raise TypeError(f"{self!r} is not callable")

	def __getattr__(self, key):
		raise AttributeError(f"{self!r} has no attribute {key!r}")

	def __getitem__(self, key):
		raise TypeError(f"{self!r} is not subscriptable (key={key!r})")


class UndefinedKey(Undefined):
	def __init__(self, key):
		self._key = key

	def __repr__(self):
		return f"UndefinedKey({self._key!r})"


class UndefinedVariable(Undefined):
	def __init__(self, name):
		self._name = name

	def __repr__(self):
		return f"UndefinedVariable({self._name!r})"


class Context:
	"""
	A :class:`Context` object stores the context of a call to a template. This
	consists of the local variables and the indent stack.
	"""
	# "Global" functions. Will be exposed to UL4 code
	functions = {}

	def __init__(self):
		self.vars = {}
		self.indents = [] # Stack of additional indentations for the ``<?render?>`` tag
		self.escapes = [] # Stack of functions for escaping the output
		self.asts = [] # Call stack (of :class:`AST` objects)

	@classmethod
	def makefunction(cls, f):
		name = f.__name__
		if name.startswith("function_"):
			name = name[9:]
		cls.functions[name] = f
		return f

	@contextlib.contextmanager
	def replacevars(self, vars):
		oldvars = self.vars
		try:
			self.vars = vars
			yield
		finally:
			self.vars = oldvars

	@contextlib.contextmanager
	def chainvars(self):
		oldvars = self.vars
		try:
			self.vars = collections.ChainMap({}, self.vars)
			yield
		finally:
			self.vars = oldvars

	def output(self, string):
		for escape in self.escapes:
			string = escape(string)
		return string


###
### Helper functions
###

def _decorateexception(exc, ast, obj=None):
	# Find the end of the exception chain
	while exc.__cause__:
		exc = exc.__cause__
	# Attach location to innermost exception
	if not isinstance(exc, LocationError) or (isinstance(ast, Call) and isinstance(obj, (Template, TemplateClosure))):
		exc.__cause__ = LocationError(ast)


def _handleexpressioneval(f):
	"""
	Decorator for an implementation of the :meth:`eval` method that does not
	do output (so it is a normal method).

	This decorator is responsible for exception handling. An exception that
	bubbles up the Python call stack will generate an exception chain that
	follows the UL4 call stack.
	"""
	@functools.wraps(f)
	def wrapped(self, context, *args, **kwargs):
		context.asts.append(self)
		try:
			return f(self, context, *args, **kwargs)
		except (BreakException, ContinueException, ReturnException):
			# Pass those exception through to the AST nodes that will handle them (:class:`ForBlock` or :class:`Template`)
			raise
		except Exception as exc:
			_decorateexception(exc, self)
			raise
		finally:
			context.asts.pop()
	return wrapped


def _handleoutputeval(f):
	"""
	Decorator for an implementation of the :meth:`eval` method that does output
	(so it is a generator).

	This decorator is responsible for exception handling. An exception that
	bubbles up the Python call stack will generate an exception chain that
	follows the UL4 call stack.
	"""
	@functools.wraps(f)
	def wrapped(self, context, *args, **kwargs):
		context.asts.append(self)
		try:
			yield from f(self, context, *args, **kwargs)
		except (BreakException, ContinueException, ReturnException):
			# Pass those exception through to the AST nodes that will handle them (:class:`ForBlock` or :class:`Template`)
			raise
		except Exception as exc:
			_decorateexception(exc, self)
			raise
		finally:
			context.asts.pop()
	return wrapped


def _unpackvar(lvalue, value):
	"""
	A generator used for recursively unpacking values for assignment.

	:obj:`lvalue` may be an :class:`AST` object (in which case the recursion ends)
	or a (possible nested) sequence of :class:`AST` objects.

	The values produced are (AST node, value) tuples.
	"""
	if isinstance(lvalue, AST):
		yield (lvalue, value)
	else:
		# Materialize iterators on the right hand side, but protect against infinite iterators
		if not isinstance(value, (tuple, list, str)):
			# If we get one item more than required, we have an error
			# Also :func:`islice` might fail if the right hand side isn't iterable (e.g. ``(a, b) = 42``)
			value = list(itertools.islice(value, len(lvalue)+1))
		if len(lvalue) != len(value):
			# The number of variables on the left hand side doesn't match the number of values on the right hand side
			raise TypeError(f"need {len(lvalue):,} value{'s' if len(lvalue) != 1 else ''} to unpack")
		for (lvalue, value) in zip(lvalue, value):
			yield from _unpackvar(lvalue, value)


def _makevars(signature, args, kwargs):
	"""
	Bind :obj:`args` and :obj:`kwargs` to the :class:`inspect.Signature` object
	:obj:`signature` and return the resulting argument dictionary. (This differs
	from :meth:`inspect.Signature.bind` in that it handles default values too.)

	:obj:`signature` may also be ``None`` in which case :obj:`args` must be empty
	and :obj:kwargs is returned, i.e. the signature is treated als accepting no
	positional argument and any keyword argument.
	"""
	if signature is None:
		if args:
			raise TypeError("positional arguments not supported")
		return kwargs
	else:
		vars = signature.bind(*args, **kwargs)
		# FIXME: use signature.apply_defaults in Python 3.6
		for param in signature.parameters.values():
			if param.name not in vars.arguments:
				if param.kind is inspect.Parameter.VAR_POSITIONAL:
					default = ()
				elif param.kind is inspect.Parameter.VAR_KEYWORD:
					default = {}
				else:
					default = param.default
				vars.arguments[param.name] = default
		return vars.arguments


class Proto:
	name = "?"

	# Attributes that are returned via a simple ``getattr`` call (either data attributes or as bound methods)
	plainattrs = set()

	# Attributes that should appear as data attributes, but are implemented as methods in the :class:`Proto` subclass
	wrappeddataattrs = set()

	# Attributes that should appear as methods and are implemented as methods in the :class:`Proto` subclass
	wrappedmethattrs = set()

	@classmethod
	def wrapmethod(cls, obj, name):
		func = getattr(cls, name)
		def wrapped(*args, **kwargs):
			return func(obj, *args, **kwargs)
		wrapped.__name__ = name
		wrapped.__module__ = cls.name
		wrapped.__qualname__ = name
		return wrapped

	@classmethod
	def missing(cls, obj, name, default=object):
		if default is object:
			raise AttributeError(name)
		else:
			return default

	@classmethod
	def getattr(cls, obj, name, default=object):
		"""
		Return the attribute :obj:`name` of the object :obj`obj` and honor
		``ul4getattr`` and ``ul4attrs``.
		"""
		ul4getattr = getattr(obj, "ul4getattr", None)
		if ul4getattr is not None:
			try:
				return ul4getattr(name)
			except AttributeError:
				return cls.missing(obj, name, default)
		else:
			ul4attrs = getattr(obj, "ul4attrs", None)
			if ul4attrs is not None and name in ul4attrs:
				return getattr(obj, name)
			elif name in cls.plainattrs:
				return getattr(obj, name)
			elif name in cls.wrappeddataattrs:
				return getattr(cls, name)(obj)
			elif name in cls.wrappedmethattrs:
				return cls.wrapmethod(obj, name)
			return cls.missing(obj, name, default)

	@classmethod
	def setattr(cls, obj, name, value):
		"""
		Set the attribute :obj:`name` of the object :obj`obj` to :obj:`value` and
		honor  ``ul4setattr`` and ``ul4attrs``.
		"""
		ul4setattr = getattr(obj, "ul4setattr", None)
		if ul4setattr is not None:
			ul4setattr(name, value)
		else:
			ul4attrs = getattr(obj, "ul4attrs", None)
			if ul4attrs is not None:
				# An ``ul4attrs`` attribute without ``ul4setattr`` will *not* make the attribute writable
				raise TypeError(f"attribute {misc.format_class(obj)}.{name!r} is readonly")
			else:
				obj[name] = value

	@classmethod
	def hasattr(cls, obj, name):
		"""
		Return whether the object :obj`obj`  has an attribute :obj:`name` and
		honor  ``ul4hasattr`` and ``ul4attrs``.
		"""
		ul4hasattr = getattr(obj, "ul4hasattr", None)
		if ul4hasattr is not None:
			return ul4hasattr(name)
		else:
			ul4attrs = getattr(obj, "ul4attrs", None)
			if ul4attrs is not None:
				return name in ul4attrs
			else:
				return name in cls.plainattrs or name in cls.wrappeddataattrs or name in cls.wrappedmethattrs

	@classmethod
	def dir(cls, obj):
		return frozenset({*cls.plainattrs, *cls.wrappeddataattrs, *cls.wrappedmethattrs})


class StrProto(Proto):
	name = "str"
	wrappedmethattrs = {"split", "rsplit", "splitlines", "strip", "lstrip", "rstrip", "upper", "lower", "capitalize", "startswith", "endswith", "replace", "count", "find", "rfind", "join"}

	@staticmethod
	def split(obj, sep=None, count=None):
		return obj.split(sep, count if count is not None else -1)

	@staticmethod
	def rsplit(obj, sep=None, count=None):
		return obj.rsplit(sep, count if count is not None else -1)

	@staticmethod
	def splitlines(obj, keepends=False):
		return obj.splitlines(keepends)

	@staticmethod
	def strip(obj, chars=None):
		return obj.strip(chars)

	@staticmethod
	def lstrip(obj, chars=None):
		return obj.lstrip(chars)

	@staticmethod
	def rstrip(obj, chars=None):
		return obj.rstrip(chars)

	@staticmethod
	def count(obj, sub, start=None, end=None):
		return obj.count(sub, start, end)

	@staticmethod
	def find(obj, sub, start=None, end=None):
		return obj.find(sub, start, end)

	@staticmethod
	def rfind(obj, sub, start=None, end=None):
		return obj.rfind(sub, start, end)

	@staticmethod
	def startswith(obj, prefix):
		if isinstance(prefix, list):
			prefix = tuple(prefix)
		return obj.startswith(prefix)

	@staticmethod
	def endswith(obj, suffix):
		if isinstance(suffix, list):
			suffix = tuple(suffix)
		return obj.endswith(suffix)

	@staticmethod
	def upper(obj):
		return obj.upper()

	@staticmethod
	def lower(obj):
		return obj.lower()

	@staticmethod
	def capitalize(obj):
		return obj.capitalize()

	@staticmethod
	def replace(obj, old, new, count=None):
		if count is None:
			return obj.replace(old, new)
		else:
			return obj.replace(old, new, count)

	@staticmethod
	def join(obj, iterable):
		return obj.join(iterable)


class ListProto(Proto):
	name = "list"
	wrappedmethattrs = {"append", "insert", "pop", "count", "find", "rfind"}

	@staticmethod
	def append(obj, *items):
		obj.extend(items)

	@staticmethod
	def insert(obj, pos, *items):
		obj[pos:pos] = items

	@staticmethod
	def pop(obj, pos=-1):
		return obj.pop(pos)

	@staticmethod
	def count(obj, sub, start=None, end=None):
		if start is None and end is None:
			return obj.count(sub)
		else:
			(start, stop, stride) = slice(start, end).indices(len(obj))
			count = 0
			for i in range(start, stop, stride):
				if obj[i] == sub:
					count += 1
			return count

	@staticmethod
	def find(obj, sub, start=None, end=None):
		try:
			if end is None:
				if start is None:
					return obj.index(sub)
				return obj.index(sub, start)
			return obj.index(sub, start, end)
		except ValueError:
			return -1

	@staticmethod
	def rfind(obj, sub, start=None, end=None):
		for i in reversed(range(*slice(start, end).indices(len(obj)))):
			if obj[i] == sub:
				return i
		return -1


class DictProto(Proto):
	name = "dict"
	plainattrs = {"items", "values", "clear"}
	wrappedmethattrs = {"get", "update"}

	@staticmethod
	def get(obj, key, default=None):
		return obj.get(key, default)

	@staticmethod
	def update(obj, *others, **kwargs):
		for other in others:
			obj.update(other)
		obj.update(**kwargs)

	@classmethod
	def missing(cls, obj, name, default=None):
		if name in obj:
			return obj[name]
		return super().missing(obj, name)


class SetProto(Proto):
	name = "set"
	plainattrs = {"clear"}
	wrappedmethattrs = {"add"}

	@staticmethod
	def add(obj, *items):
		obj.update(items)


class SliceProto(Proto):
	name = "slice"
	plainattrs = {"start", "stop"}


class DateProto(Proto):
	name = "date"
	wrappedmethattrs = {"weekday", "yearday", "week", "calendar", "day", "month", "year", "mimeformat", "isoformat"}

	@staticmethod
	def weekday(obj):
		return obj.weekday()

	@staticmethod
	def calendar(obj, firstweekday=0, mindaysinfirstweek=4):
		"""
		Return the calendar year the date :obj:`obj` belongs to, the calendar week
		number and the week dayy. (A day might belong to a different calender year,
		if it is in week 1 but before January 1, or if belongs to week 1 of the
		following year).

		:obj:`firstweekday` defines what a week is (i.e. which weekday is
		considered the start of the week, ``0`` is Monday and ``6`` is Sunday).
		:obj:`mindaysinfirstweek` defines how many days must be in a week to be
		considered the first week in the year.

		For example for the ISO week number (according to
		https://en.wikipedia.org/wiki/ISO_week_date) the week starts on Monday
		(i.e. ``firstweekday == 0``) and a week is considered the first week if
		it's the first week that contains a Thursday (which means that this week
		contains at least four days in January, so ``mindaysinfirstweek == 4``).
		This is also the default for both parameters.

		For the US ``firstweekday == 6`` and ``mindaysinfirstweek == 1``, i.e.
		the week starts on Sunday and January the first is always in week 1.

		There's also the convention that the week 1 is the first complete week
		in January. For this ``mindaysinfirstweek == 7``.

		For example ``<?print repr(@(2000-02-29).calendar()?>`` prints
		``[2000, 9, 1]``, i.e. this day is the Tuesday in week 9 of the year 2000.
		"""

		# Normalize parameters
		firstweekday %= 7
		mindaysinfirstweek = max(1, min(mindaysinfirstweek, 7))

		# :obj:`obj` might be in the first week of the next year, or last week of
		# the previous year, so we might have to try those too.
		for year in (obj.year+1, obj.year, obj.year-1):
			# :obj:`refdate` will always be in week 1
			refdate = obj.__class__(year, 1, mindaysinfirstweek)
			# Go back to the start of :obj:`refdate`\s week (i.e. day 1 of week 1)
			weekstartdate = refdate - datetime.timedelta((refdate.weekday() - firstweekday) % 7)
			# Is our date :obj:`obj` at or after day 1 of week 1?
			# (if not we have to recalculate based on the year before in the next loop iteration)
			if obj >= weekstartdate:
				# Add 1, because the first week is week 1, not week 0
				return (year, (obj - weekstartdate).days//7 + 1, obj.weekday())

	@staticmethod
	def week(obj, firstweekday=0, mindaysinfirstweek=4):
		"""
		Return the week number of the date :obj:`obj`. For more info see
		:meth:`calendar`.
		"""
		return DateProto.calendar(obj, firstweekday, mindaysinfirstweek)[1]

	@staticmethod
	def day(obj):
		return obj.day

	@staticmethod
	def month(obj):
		return obj.month

	@staticmethod
	def year(obj):
		return obj.year

	@staticmethod
	def mimeformat(obj):
		weekdayname = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
		monthname = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
		return f"{weekdayname[obj.weekday()]}, {obj.day:02d} {monthname[obj.month]:3} {obj.year:4}"

	@staticmethod
	def isoformat(obj):
		return obj.isoformat()

	@staticmethod
	def yearday(obj):
		return (obj - obj.__class__(obj.year, 1, 1)).days+1


class DatetimeProto(DateProto):
	name = "datetime"
	wrappedmethattrs = DateProto.wrappedmethattrs.union({"hour", "minute", "second", "microsecond"})

	@staticmethod
	def hour(obj):
		return obj.hour

	@staticmethod
	def minute(obj):
		return obj.minute

	@staticmethod
	def second(obj):
		return obj.second

	@staticmethod
	def microsecond(obj):
		return obj.microsecond

	@staticmethod
	def mimeformat(obj):
		weekdayname = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
		monthname = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
		return f"{weekdayname[obj.weekday()]}, {obj.day:02d} {monthname[obj.month]:3} {obj.year:4} {obj.hour:02}:{obj.minute:02}:{obj.second:02} GMT"


class TimeDeltaProto(Proto):
	name = "timedelta"
	wrappedmethattrs = {"days", "seconds", "microseconds"}

	@staticmethod
	def days(obj):
		return obj.days

	@staticmethod
	def seconds(obj):
		return obj.seconds

	@staticmethod
	def microseconds(obj):
		return obj.microseconds


class ExceptionProto(Proto):
	name = "exception"
	wrappeddataattrs = {"context"}

	@staticmethod
	def context(obj):
		if obj.__cause__ is not None:
			return obj.__cause__
		elif obj.__context__ is not None and not obj.__suppress_context__:
			return obj.__context__
		return None


@functools.singledispatch
def proto(obj):
	return Proto


@proto.register(str)
def proto_str(obj):
	return StrProto


@proto.register(list)
@proto.register(tuple)
@proto.register(abc.Sequence)
def proto_list(obj):
	return ListProto


@proto.register(dict)
@proto.register(abc.Mapping)
def proto_dict(obj):
	return DictProto


@proto.register(set)
@proto.register(frozenset)
@proto.register(abc.Set)
def proto_set(obj):
	return SetProto


@proto.register(slice)
def proto_slice(obj):
	return SliceProto


@proto.register(datetime.date)
def proto_date(obj):
	return DateProto


@proto.register(datetime.datetime)
def proto_datetime(obj):
	return DatetimeProto


@proto.register(datetime.timedelta)
def proto_timedelta(obj):
	return TimeDeltaProto


@proto.register(BaseException)
def proto_exception(obj):
	return ExceptionProto


def _linecol(source, index):
	index = index or 0
	lastlinefeed = source.rfind("\n", 0, index)
	if lastlinefeed >= 0:
		return (source.count("\n", 0, index)+1, index-lastlinefeed)
	else:
		return (1, index + 1)


def _offset(pos):
	offset = ["["]
	if pos.start is not None:
		offset.append(f"{pos.start:,}")
	offset.append(":")
	if pos.stop is not None:
		offset.append(f"{pos.stop:,}")
	offset.append("]")
	return "".join(offset)


def _sourceprefix(source, pos):
	outerstartpos = innerstartpos = pos

	preprefix = ""
	maxprefix = 40
	while maxprefix > 0:
		# We arrived at the start of the source
		if outerstartpos == 0:
			break
		# We arrived at the start of the line
		if source[outerstartpos-1] == "\n":
			break
		maxprefix -= 1
		outerstartpos -= 1
	else:
		# We've exhausted the length of the prefix
		preprefix = "\N{HORIZONTAL ELLIPSIS}"

	return preprefix + source[outerstartpos:innerstartpos]


def _sourcesuffix(source, pos):
	outerstoppos = innerstoppos = pos

	postsuffix = ""
	maxsuffix = 40
	while maxsuffix > 0:
		# We arrived at the end of the source
		if outerstoppos >= len(source):
			break
		# We arrived at the end of the line
		if source[outerstoppos] == "\n":
			break
		maxsuffix -= 1
		outerstoppos += 1
	else:
		# We've exhausted the length of the suffix
		postsuffix = "\N{HORIZONTAL ELLIPSIS}"

	return source[innerstoppos:outerstoppos] + postsuffix


###
### Helper functions for the various UL4 functions
###

def _str(obj=""):
	from ll import color
	if obj is None:
		return ""
	elif isinstance(obj, Undefined):
		return ""
	elif isinstance(obj, str):
		return obj
	elif isinstance(obj, datetime.datetime):
		if obj.microsecond or obj.second:
			return str(obj)
		else:
			return str(obj)[:-3]
	elif isinstance(obj, color.Color):
		return str(obj)
	elif isinstance(obj, (abc.Sequence, abc.Set, abc.Mapping)):
		return _repr(obj)
	elif isinstance(obj, inspect.Signature):
		v = []
		v.append("(")
		for (i, p) in enumerate(obj.parameters.values()):
			if i:
				v.append(", ")
			if p.kind == p.VAR_POSITIONAL:
				v.append("*")
			elif p.kind == p.VAR_KEYWORD:
				v.append("**")
			v.append(p.name)
			if p.default is not p.empty:
				v.append("=")
				v.append(_repr(p.default))
		v.append(")")
		return "".join(v)
	else:
		return str(obj)


def _repr_helper(obj, seen, forceascii):
	from ll import color
	if isinstance(obj, str):
		if forceascii:
			yield ascii(obj)
		else:
			yield repr(obj)
	elif isinstance(obj, datetime.datetime):
		s = obj.isoformat()
		if s.endswith("T00:00:00"):
			s = s[:-8]
		elif s.endswith(":00"):
			s = s[:-3]
		yield f"@({s})"
	elif isinstance(obj, datetime.date):
		yield f"@({obj.isoformat()})"
	elif isinstance(obj, datetime.timedelta):
		yield repr(obj).partition(".")[-1]
	elif isinstance(obj, color.Color):
		if obj[3] == 0xff:
			s = f"#{obj[0]:02x}{obj[1]:02x}{obj[2]:02x}"
			if s[1] == s[2] and s[3] == s[4] and s[5] == s[6]:
				s = f"#{s[1]}{s[3]}{s[5]}"
			yield s
		else:
			s = f"#{obj[0]:02x}{obj[1]:02x}{obj[2]:02x}{obj[3]:02x}"
			if s[1] == s[2] and s[3] == s[4] and s[5] == s[6] and s[7] == s[8]:
				s = f"#{s[1]}{s[3]}{s[5]}{s[7]}"
			yield s
	elif isinstance(obj, abc.Sequence):
		if id(obj) in seen:
			yield "..."
		else:
			seen.add(id(obj))
			yield "["
			for (i, item) in enumerate(obj):
				if i:
					yield ", "
				yield from _repr_helper(item, seen, forceascii)
			yield "]"
			seen.discard(id(obj))
	elif isinstance(obj, abc.Set):
		if id(obj) in seen:
			yield "..."
		else:
			if obj:
				seen.add(id(obj))
				yield "{"
				for (i, item) in enumerate(obj):
					if i:
						yield ", "
					yield from _repr_helper(item, seen, forceascii)
				yield "}"
				seen.discard(id(obj))
			else:
				yield "{/}"
	elif isinstance(obj, inspect.Signature):
		if id(obj) in seen:
			yield "..."
		else:
			seen.add(id(obj))
			yield "<Signature ("
			for (i, p) in enumerate(obj.parameters.values()):
				if i:
					yield ", "
				if p.kind == p.VAR_POSITIONAL:
					yield "*"
				elif p.kind == p.VAR_KEYWORD:
					yield "**"
				yield p.name
				if p.default is not p.empty:
					yield "="
					yield from _repr_helper(p.default, seen, forceascii)
			yield ")>"
			seen.discard(id(obj))
	elif isinstance(obj, abc.Mapping):
		if id(obj) in seen:
			yield "..."
		else:
			seen.add(id(obj))
			yield "{"
			for (i, (key, value)) in enumerate(obj.items()):
				if i:
					yield ", "
				yield from _repr_helper(key, seen, forceascii)
				yield ": "
				yield from _repr_helper(value, seen, forceascii)
			yield "}"
			seen.discard(id(obj))
	else:
		if forceascii:
			yield ascii(obj)
		else:
			yield repr(obj)


def _repr(obj):
	return "".join(_repr_helper(obj, set(), False))


def _ascii(obj):
	return "".join(_repr_helper(obj, set(), True))


def _asjson(obj):
	from ll import color
	if obj is None:
		return "null"
	elif isinstance(obj, Undefined):
		return "undefined"
	elif isinstance(obj, (bool, int, float)):
		return json.dumps(obj)
	elif isinstance(obj, str):
		return json.dumps(obj).replace("<", "\\u003c") # Prevent XSS (when the value is embedded literally in a ``<script>`` tag)
	elif isinstance(obj, datetime.datetime):
		return f"new Date({obj.year}, {obj.month-1}, {obj.day}, {obj.hour}, {obj.minute}, {obj.second}, {obj.microsecond//1000})"
	elif isinstance(obj, datetime.date):
		return f"new ul4.Date_({obj.year}, {obj.month}, {obj.day})"
	elif isinstance(obj, datetime.timedelta):
		return f"new ul4.TimeDelta({obj.days}, {obj.seconds}, {obj.microseconds})"
	elif isinstance(obj, misc.monthdelta):
		return f"new ul4.MonthDelta({obj.months()})"
	elif isinstance(obj, color.Color):
		return f"new ul4.Color({obj[0]}, {obj[1]}, {obj[2]}, {obj[3]})"
	elif isinstance(obj, abc.Mapping):
		items = ", ".join(f"{_asjson(key)}: {_asjson(value)}" for (key, value) in obj.items())
		return f"{{{items}}}"
	elif isinstance(obj, abc.Sequence):
		items = ", ".join(_asjson(item) for item in obj)
		return f"[{items}]"
	elif isinstance(obj, Template):
		return obj.jssource()
	else:
		raise TypeError(f"can't handle object of type {type(obj)}")


def _xmlescape(obj):
	if obj is None:
		return ""
	elif isinstance(obj, Undefined):
		return ""
	else:
		return misc.xmlescape(_str(obj))


###
### Node classes for the abstract syntax tree
###

class AST:
	"""
	Base class for all syntax tree nodes.
	"""

	# Set of attributes available to UL4 templates
	ul4attrs = {"type", "template", "pos", "startpos", "startline", "startcol", "source", "startsource", "fullsource", "sourceprefix", "sourcesuffix", "startsourceprefix", "startsourcesuffix"}

	# Specifies whether the node does output (so :meth:`eval` is a generator)
	# or not (so :meth:`eval` is a normal method).
	output = False

	def __init__(self, template=None, startpos=None):
		# ``template`` references the :class:`Template` object of which
		# ``self`` is a part. This mean that for a :class:`Template` object ``t``
		# (which is an :class:`AST` object) ``t.template is t`` is true.
		self.template = template
		self._startpos = startpos
		self._startline = None
		self._startcol = None
		self._stoppos = None
		self._stopline = None
		self._stopcol = None

	@property
	def startpos(self):
		return self._startpos

	@startpos.setter
	def startpos(self, pos):
		self._startpos = pos
		self._startline = None
		self._startcol = None

	@property
	def startline(self):
		if self._startline is None:
			(self._startline, self._startcol) = _linecol(self.template._fullsource, self._startpos.start)
		return self._startline

	@property
	def startcol(self):
		if self._startcol is None:
			(self._startline, self._startcol) = _linecol(self.template._fullsource, self._startpos.start)
		return self._startcol

	@property
	def startsource(self):
		return self.template._fullsource[self._startpos]

	@property
	def sourceprefix(self):
		return _sourceprefix(self.template._fullsource, self._startpos.start)

	@property
	def sourcesuffix(self):
		return _sourcesuffix(self.template._fullsource, self._stoppos.stop if self._stoppos is not None else self._startpos.stop)

	startsourceprefix = sourceprefix

	@property
	def startsourcesuffix(self):
		return _sourcesuffix(self.template._fullsource, self._startpos.stop)

	@property
	def stopsourceprefix(self):
		return _sourceprefix(self.template._fullsource, self._stoppos.start) if self._stoppos is not None else None

	@property
	def stopsourcesuffix(self):
		return _sourcesuffix(self.template._fullsource, self._stoppos.stop) if self._stoppos is not None else None

	@property
	def stoppos(self):
		return self._stoppos

	@stoppos.setter
	def stoppos(self, pos):
		self._stoppos = pos
		self._stopline = None
		self._stopcol = None

	@property
	def stopline(self):
		if self._stopline is None:
			(self._stopline, self._stopcol) = _linecol(self.template._fullsource, self._stoppos.stop)
		return self._stopline

	@property
	def stopcol(self):
		if self._stopcol is None:
			(self._stopline, self._stopcol) = _linecol(self.template._fullsource, self._stoppos.stop)
		return self._stopcol

	@property
	def stopsource(self):
		return self.template._fullsource[self._stoppos]

	@property
	def pos(self):
		return self._startpos if self._stoppos is None else slice(self._startpos.start, self._stoppos.stop)

	@property
	def source(self):
		return self.template._fullsource[self.pos]

	@property
	def fullsource(self):
		return self.template._fullsource

	def __repr__(self):
		parts = [f"<{self.__class__.__module__}.{self.__class__.__qualname__}"]
		pos = self.pos
		parts.append(f"(offset {_offset(pos)}; line {self.startline:,}; col {self.startcol:,})")
		parts.extend(self._repr())
		parts.append(f"at {id(self):#x}>")
		return " ".join(parts)

	def _repr(self):
		yield from ()

	def _repr_pretty_(self, p, cycle):
		prefix = f"<{self.__class__.__module__}.{self.__class__.__qualname__}"
		pos = self.pos
		prefix += f" (offset {_offset(pos)}; line {self.startline:,}; col {self.startcol:,})"
		suffix = f"at {id(self):#x}"

		if cycle:
			p.text(f"{prefix} ... {suffix}>")
		else:
			with p.group(4, prefix, ">"):
				self._repr_pretty(p)
				p.breakable()
				p.text(suffix)

	def _repr_pretty(self, p):
		pass

	def __str__(self):
		# This uses :meth:`_str`, which is a generator and may output:
		# ``None``, which means: "add a line feed and an indentation here"
		# an int, which means: add the int to the indentation level
		# a string, which means: add this string to the output
		v = []
		level = 0
		needlf = False
		for code in self._str():
			if code is None:
				needlf = True
			elif isinstance(code, int):
				level += code
			else:
				if needlf:
					v.append("\n")
					v.append(level*"\t")
					needlf = False
				v.append(code)
		if needlf:
			v.append("\n")
		return "".join(v)

	def eval(self, context):
		"""
		This evaluates the node.

		For most nodes this is a normal function that returns the result of
		evaluating the node. (For these nodes the class attribute :obj:`output`
		is false.). For nodes that produce output (like literal text,
		:class:`Print`, :class:`PrintX` or :class:`Render`) it is a generator
		which yields the text output of the node. For blocks (which might contain
		nodes which produce output) this is also a generator. (For these nodes
		the class attribute :obj:`output` is true.)
		"""
		pass

	def ul4ondump(self, encoder):
		encoder.dump(self.template)
		encoder.dump(self._startpos)

	def ul4onload(self, decoder):
		self.template = decoder.load()
		self.startpos = decoder.load()
		self.stoppos = None


@register("text")
class Text(AST):
	"""
	AST node for literal text.
	"""

	ul4attrs = AST.ul4attrs.union({"text"})

	output = True

	def _repr(self):
		yield repr(self.text)

	def _repr_pretty(self, p):
		p.breakable()
		p.text("text=")
		p.pretty(self.text)

	@property
	def text(self):
		return self.template._fullsource[self._startpos]

	def _str(self):
		yield f"text {self.text!r}"

	def eval(self, context):
		yield context.output(self.text)


@register("indent")
class Indent(Text):
	"""
	AST node for literal text that is an indentation at the start of the line.
	"""

	def __init__(self, template=None, startpos=None, text=None):
		super().__init__(template, startpos)
		self._text = text

	@property
	def text(self):
		if self._text is None:
			return self.template._fullsource[self._startpos]
		else:
			return self._text

	# We don't define a setter, because the template should *not* be able to
	# set this attribute. However the attribute *will* be set by the code
	# compiling the template
	def _settext(self, text):
		self._text = text if text != self.template._fullsource[self._startpos] else None

	def _str(self):
		yield f"indent {self.text!r}"

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self._text)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self._text = decoder.load()

	def eval(self, context):
		for indent in context.indents:
			yield context.output(indent)
		yield context.output(self.text)


@register("lineend")
class LineEnd(Text):
	"""
	AST node for literal text that is the end of a line.
	"""

	def _str(self):
		yield f"lineend {self.text!r}"


class Tag(AST):
	"""
	A :class:`Tag` object is the location of a template tag in a template.
	"""
	def __init__(self, template=None, tag=None, tagpos=None, codepos=None):
		super().__init__(template, tagpos)
		self.tag = tag
		self.codepos = codepos

	def _repr(self):
		yield repr(self.source)

	def _repr_pretty(self, p):
		p.breakable()
		p.text("source=")
		p.pretty(self.source)

	def __str__(self):
		return f"{self.source!r} (offset {_offset(self.startpos)}; line {self.startline:,}; col {self.startcol:,})"

	@property
	def code(self):
		return self.template._fullsource[self.codepos]


class Code(AST):
	"""
	The base class of all AST nodes that appear inside a :class:`Tag`.
	"""

	def _str(self):
		yield " ".join(self.source.splitlines(False))


@register("const")
class Const(Code):
	"""
	Load a constant
	"""
	ul4attrs = Code.ul4attrs.union({"value"})

	def __init__(self, template=None, startpos=None, value=None):
		super().__init__(template, startpos)
		self.value = value

	def eval(self, context):
		# We don't need a decorator, because this can't fail anyway.
		return self.value

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()

	def _repr(self):
		yield repr(self.value)

	def _repr_pretty(self, p):
		p.breakable()
		p.text("value=")
		p.pretty(self.value)


### AST nodes for items in list, set and dict "literals"

@register("seqitem")
class SeqItem(Code):
	"""
	AST node for an item in a list/set "literal"
	"""

	ul4attrs = Code.ul4attrs.union({"value"})

	def __init__(self, template=None, startpos=None, value=None):
		super().__init__(template, startpos)
		self.value = value

	def _repr(self):
		yield f"{self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("value=")
		p.pretty(self.value)

	@_handleexpressioneval
	def eval_list(self, context, result):
		result.append(self.value.eval(context))

	@_handleexpressioneval
	def eval_set(self, context, result):
		result.add(self.value.eval(context))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()


@register("unpackseqitem")
class UnpackSeqItem(Code):
	"""
	AST nodes for '*' unpacking expressions in a list/ set "literal".
	"""

	ul4attrs = Code.ul4attrs.union({"value"})

	def __init__(self, template=None, startpos=None, value=None):
		super().__init__(template, startpos)
		self.value = value

	def _repr(self):
		yield f"*{self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("value=")
		p.pretty(self.value)

	@_handleexpressioneval
	def eval_list(self, context, result):
		# We're updating the result list here to get a proper location when the ``*`` argument isn't iterable
		for item in self.value.eval(context):
			result.append(item)

	@_handleexpressioneval
	def eval_set(self, context, result):
		# We're updating the result set here to get a proper location when the ``*`` argument isn't iterable
		for item in self.value.eval(context):
			result.add(item)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()


@register("dictitem")
class DictItem(Code):
	"""
	AST node for a dictionary key
	"""

	ul4attrs = Code.ul4attrs.union({"key", "value"})

	def __init__(self, template=None, startpos=None, key=None, value=None):
		super().__init__(template, startpos)
		self.key = key
		self.value = value

	def _repr(self):
		yield f"{self.key!r}={self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("key=")
		p.pretty(self.key)
		p.breakable("")
		p.text("value=")
		p.pretty(self.value)

	@_handleexpressioneval
	def eval_dict(self, context, result):
		key = self.key.eval(context)
		value = self.value.eval(context)
		result[key] = value

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.key)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.key = decoder.load()
		self.value = decoder.load()


@register("unpackdictitem")
class UnpackDictItem(Code):
	"""
	AST nodes for '**' unpacking expressions in dict "literal".
	"""

	ul4attrs = Code.ul4attrs.union({"item"})

	def __init__(self, template=None, startpos=None, item=None):
		super().__init__(template, startpos)
		self.item = item

	def _repr(self):
		yield f"**{self.item!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("item=")
		p.pretty(self.item)

	@_handleexpressioneval
	def eval_dict(self, context, result):
		result.update(self.item.eval(context))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.item = decoder.load()


### AST nodes for call arguments

@register("posarg")
class PosArg(Code):
	"""
	AST node for a positional argument
	"""

	ul4attrs = Code.ul4attrs.union({"value"})

	def __init__(self, template=None, startpos=None, value=None):
		super().__init__(template, startpos)
		self.value = value

	def _repr(self):
		yield f"{self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("value=")
		p.pretty(self.value)

	def append(self, call):
		for arg in call.args:
			if isinstance(arg, KeywordArg):
				raise SyntaxError("positional argument follows keyword argument")
			elif isinstance(arg, UnpackDictArg):
				raise SyntaxError("positional argument follows keyword argument unpacking")
		call.args.append(self)

	@_handleexpressioneval
	def eval_call(self, context, args, kwargs):
		args.append(self.value.eval(context))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()


@register("keywordarg")
class KeywordArg(Code):
	"""
	AST node for a keyword argument
	"""

	ul4attrs = Code.ul4attrs.union({"name", "value"})

	def __init__(self, template=None, startpos=None, name=None, value=None):
		super().__init__(template, startpos)
		self.name = name
		self.value = value

	def _repr(self):
		yield f"{self.name}={self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("name=")
		p.pretty(self.name)
		p.breakable("")
		p.text("value=")
		p.pretty(self.value)

	def append(self, call):
		call.args.append(self)

	@_handleexpressioneval
	def eval_call(self, context, args, kwargs):
		if self.name in kwargs:
			raise SyntaxError(f"duplicate keyword argument {self.name!r}")
		kwargs[self.name] = self.value.eval(context)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.name)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.name = decoder.load()
		self.value = decoder.load()


@register("unpacklistarg")
class UnpackListArg(Code):
	"""
	AST nodes for '*' unpacking expressions in calls.
	"""

	ul4attrs = Code.ul4attrs.union({"item"})

	def __init__(self, template=None, startpos=None, item=None):
		super().__init__(template, startpos)
		self.item = item

	def _repr(self):
		yield f"*{self.item!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("item=")
		p.pretty(self.item)

	def append(self, call):
		for arg in call.args:
			if isinstance(arg, UnpackDictArg):
				raise SyntaxError("iterable argument unpacking follows keyword argument unpacking")
		call.args.append(self)

	@_handleexpressioneval
	def eval_call(self, context, args, kwargs):
		for item in self.item.eval(context):
			args.append(item)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.item = decoder.load()


@register("unpackdictarg")
class UnpackDictArg(Code):
	"""
	AST nodes for '**' unpacking expressions in calls.
	"""

	ul4attrs = Code.ul4attrs.union({"item"})

	def __init__(self, template=None, startpos=None, item=None):
		super().__init__(template, startpos)
		self.item = item

	def _repr(self):
		yield f"**{self.item!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("item=")
		p.pretty(self.item)

	def append(self, call):
		call.args.append(self)

	@_handleexpressioneval
	def eval_call(self, context, args, kwargs):
		item = self.item.eval(context)
		if hasattr(item, "keys"):
			for key in item:
				if key in kwargs:
					raise SyntaxError(f"duplicate keyword argument {key!r}")
				kwargs[key] = item[key]
		else:
			for (key, value) in item:
				if key in kwargs:
					raise SyntaxError(f"duplicate keyword argument {key!r}")
				kwargs[key] = value

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.item = decoder.load()


@register("list")
class List(Code):
	"""
	AST nodes for loading a list object.
	"""

	ul4attrs = Code.ul4attrs.union({"items"})

	def __init__(self, template=None, startpos=None, *items):
		super().__init__(template, startpos)
		self.items = list(items)

	def _repr(self):
		yield f"with {len(self.items):,} items"

	def _repr_pretty(self, p):
		for item in self.items:
			p.breakable()
			p.pretty(item)

	@_handleexpressioneval
	def eval(self, context):
		result = []
		for item in self.items:
			item.eval_list(context, result)
		return result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = decoder.load()


@register("listcomp")
class ListComp(Code):
	"""
	AST node for list comprehension.
	"""

	ul4attrs = Code.ul4attrs.union({"item", "varname", "container", "condition"})

	def __init__(self, template=None, startpos=None, item=None, varname=None, container=None, condition=None):
		super().__init__(template, startpos)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def _repr(self):
		yield f"item={self.item!r}"
		yield f"varname={self.varname!r}"
		yield f"container={self.container!r}"
		if self.container is not None:
			yield f"condition={self.condition!r}"

	def _repr_pretty(self, p):
		p.breakable("")
		p.text("item=")
		p.pretty(self.item)
		p.text(",")
		p.breakable()
		p.text("varname=")
		p.pretty(self.varname)
		p.text(",")
		p.breakable()
		p.text("container=")
		p.pretty(self.container)
		if self.condition is not None:
			p.text(",")
			p.breakable()
			p.text("condition=")
			p.pretty(self.condition)

	@_handleexpressioneval
	def eval(self, context):
		container = self.container.eval(context)
		with context.chainvars(): # Don't let loop variables leak into the surrounding scope
			result = []
			for item in container:
				for (lvalue, value) in _unpackvar(self.varname, item):
					lvalue.evalset(context, value)
				if self.condition is None or self.condition.eval(context):
					result.append(self.item.eval(context))
			return result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)
		encoder.dump(self.varname)
		encoder.dump(self.container)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.item = decoder.load()
		self.varname = decoder.load()
		self.container = decoder.load()
		self.condition = decoder.load()


@register("set")
class Set(Code):
	"""
	AST nodes for loading a set object.
	"""

	ul4attrs = Code.ul4attrs.union({"items"})

	def __init__(self, template=None, startpos=None, *items):
		super().__init__(template, startpos)
		self.items = list(items)

	def _repr(self):
		yield f"with {len(self.items):,} items"

	def _repr_pretty(self, p):
		for item in self.items:
			p.breakable()
			p.pretty(item)

	@_handleexpressioneval
	def eval(self, context):
		result = set()
		for item in self.items:
			item.eval_set(context, result)
		return result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = decoder.load()


@register("setcomp")
class SetComp(Code):
	"""
	AST node for set comprehension.
	"""

	ul4attrs = Code.ul4attrs.union({"item", "varname", "container", "condition"})

	def __init__(self, template=None, startpos=None, item=None, varname=None, container=None, condition=None):
		super().__init__(template, startpos)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def _repr(self):
		yield f"item={self.item!r}"
		yield f"varname={self.varname!r}"
		yield f"container={self.container!r}"
		if self.container is not None:
			yield f"condition={self.condition!r}"

	def _repr_pretty(self, p):
		p.breakable("")
		p.text("item=")
		p.pretty(self.item)
		p.text(",")
		p.breakable()
		p.text("varname=")
		p.pretty(self.varname)
		p.text(",")
		p.breakable()
		p.text("container=")
		p.pretty(self.container)
		if self.condition is not None:
			p.text(",")
			p.breakable()
			p.text("condition=")
			p.pretty(self.condition)

	@_handleexpressioneval
	def eval(self, context):
		container = self.container.eval(context)
		with context.chainvars(): # Don't let loop variables leak into the surrounding scope
			result = set()
			for item in container:
				for (lvalue, value) in _unpackvar(self.varname, item):
					lvalue.evalset(context, value)
				if self.condition is None or self.condition.eval(context):
					result.add(self.item.eval(context))
		return result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)
		encoder.dump(self.varname)
		encoder.dump(self.container)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.item = decoder.load()
		self.varname = decoder.load()
		self.container = decoder.load()
		self.condition = decoder.load()


@register("dict")
class Dict(Code):
	"""
	AST node for loading a dict object.
	"""

	ul4attrs = Code.ul4attrs.union({"items"})

	def __init__(self, template=None, startpos=None, *items):
		super().__init__(template, startpos)
		self.items = list(items)

	def _repr(self):
		yield f"with {len(self.items):,} items"

	def _repr_pretty(self, p):
		for item in self.items:
			p.breakable()
			p.pretty(item)

	@_handleexpressioneval
	def eval(self, context):
		result = {}
		for item in self.items:
			item.eval_dict(context, result)
		return result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = decoder.load()


@register("dictcomp")
class DictComp(Code):
	"""
	AST node for dictionary comprehension.
	"""

	ul4attrs = Code.ul4attrs.union({"key", "value", "varname", "container", "condition"})

	def __init__(self, template=None, startpos=None, key=None, value=None, varname=None, container=None, condition=None):
		super().__init__(template, startpos)
		self.key = key
		self.value = value
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		yield f"key={self.key!r}"
		yield f"value={self.value!r}"
		yield f"varname={self.varname!r}"
		yield f"container={self.container!r}"
		if self.container is not None:
			yield f"condition={self.condition!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("key=")
		p.pretty(self.key)
		p.breakable()
		p.text("value=")
		p.pretty(self.value)
		p.breakable()
		p.text("varname=")
		p.pretty(self.varname)
		p.breakable()
		p.text("container=")
		p.pretty(self.container)
		if self.condition is not None:
			p.breakable()
			p.text("condition=")
			p.pretty(self.condition)

	@_handleexpressioneval
	def eval(self, context):
		container = self.container.eval(context)
		with context.chainvars(): # Don't let loop variables leak into the surrounding scope
			result = {}
			for item in container:
				for (lvalue, value) in _unpackvar(self.varname, item):
					lvalue.evalset(context, value)
				if self.condition is None or self.condition.eval(context):
					result[self.key.eval(context)] = self.value.eval(context)
			return result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.key)
		encoder.dump(self.value)
		encoder.dump(self.varname)
		encoder.dump(self.container)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.key = decoder.load()
		self.value = decoder.load()
		self.varname = decoder.load()
		self.container = decoder.load()
		self.condition = decoder.load()


@register("genexpr")
class GenExpr(Code):
	"""
	AST node for a generator expression.
	"""

	ul4attrs = Code.ul4attrs.union({"item", "varname", "container", "condition"})

	def __init__(self, template=None, startpos=None, item=None, varname=None, container=None, condition=None):
		super().__init__(template, startpos)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def _repr(self):
		yield f"item={self.item!r}"
		yield f"varname={self.varname!r}"
		yield f"container={self.container!r}"
		if self.container is not None:
			yield f"condition={self.condition!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("item=")
		p.pretty(self.item)
		p.breakable()
		p.text("varname=")
		p.pretty(self.varname)
		p.breakable()
		p.text("container=")
		p.pretty(self.container)
		if self.condition is not None:
			p.breakable()
			p.text("condition=")
			p.pretty(self.condition)

	def eval(self, context):
		container = self.container.eval(context)

		try:
			with context.chainvars(): # Don't let loop variables leak into the surrounding scope
				for item in container:
					for (lvalue, value) in _unpackvar(self.varname, item):
						lvalue.evalset(context, value)
					if self.condition is None or self.condition.eval(context):
						yield self.item.eval(context)
		except LocationError:
			raise
		except Exception as exc:
			_decorateexception(exc, self)
			raise

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)
		encoder.dump(self.varname)
		encoder.dump(self.container)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.item = decoder.load()
		self.varname = decoder.load()
		self.container = decoder.load()
		self.condition = decoder.load()


@register("var")
class Var(Code):
	"""
	AST nodes for loading a variable.
	"""

	ul4attrs = Code.ul4attrs.union({"name"})

	def __init__(self, template=None, startpos=None, name=None):
		super().__init__(template, startpos)
		self.name = name

	def _repr(self):
		yield repr(self.name)

	def _repr_pretty(self, p):
		p.breakable()
		p.text("name=")
		p.pretty(self.name)

	@_handleexpressioneval
	def eval(self, context):
		try:
			return context.vars[self.name]
		except KeyError:
			try:
				return context.functions[self.name]
			except KeyError:
				return UndefinedVariable(self.name)

	@_handleexpressioneval
	def evalset(self, context, value):
		context.vars[self.name] = value

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		context.vars[self.name] = operator.evalfoldaug(context.vars[self.name], value)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.name)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.name = decoder.load()


class Block(Code):
	"""
	Base class for all AST nodes that are blocks.

	A block contains a sequence of AST nodes that are executed sequencially.
	A block may execute its content zero (e.g. an ``<?if?>`` block) or more times
	(e.g. a ``<?for?>`` block).
	"""

	output = True

	ul4attrs = Code.ul4attrs.union({"stoppos", "stopline", "stopcol", "stopsource", "content"})

	def __init__(self, template=None, startpos=None, stoppos=None):
		super().__init__(template, startpos)
		self._stoppos = stoppos	
		self._stopline = None
		self._stopcol = None
		self.content = []

	def append(self, item):
		self.content.append(item)

	def finish(self, endtag):
		self.stoppos = endtag.startpos

	def _str(self):
		if self.content:
			for node in self.content:
				yield from node._str()
				yield None
		else:
			yield "pass"
			yield None

	@_handleoutputeval
	def eval(self, context):
		for node in self.content:
			result = node.eval(context)
			if node.output:
				yield from result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.stoppos)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.stoppos = decoder.load()
		self.content = decoder.load()


@register("condblock")
class CondBlock(Block):
	r"""
	AST node for an conditional block.

	The content of the :class:`CondBlock` block is one :class:`IfBlock` followed
	by zero or more :class:`ElIfBlock`\s followed by zero or one
	:class:`ElseBlock`.
	"""

	def __init__(self, template=None, startpos=None, stoppos=None, condition=None):
		super().__init__(template, startpos, stoppos)
		if condition is not None:
			self.newblock(IfBlock(template, startpos, None, condition))

	def _repr_pretty(self, p):
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def append(self, item):
		self.content[-1].append(item)

	def finish(self, endtag):
		super().finish(endtag)
		if self.content:
			self.content[-1].stoppos = slice(endtag.startpos.start, endtag.startpos.start)

	def newblock(self, block):
		if self.content:
			self.content[-1].stoppos = slice(block.startpos.start, block.startpos.start)
		self.content.append(block)

	def _str(self):
		for node in self.content:
			yield from node._str()

	@_handleoutputeval
	def eval(self, context):
		for node in self.content:
			if isinstance(node, ElseBlock) or node.condition.eval(context):
				yield from node.eval(context)
				break


@register("ifblock")
class IfBlock(Block):
	"""
	AST node for an ``<?if?>`` block.
	"""

	ul4attrs = Block.ul4attrs.union({"condition"})

	def __init__(self, template=None, startpos=None, stoppos=None, condition=None):
		super().__init__(template, startpos, stoppos)
		self.condition = condition

	def _repr(self):
		yield f" condition={self.condition!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("condition=")
		p.pretty(self.condition)
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def _str(self):
		yield "if "
		yield from Code._str(self)
		yield ":"
		yield None
		yield +1
		yield from Block._str(self)
		yield -1

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()


@register("elifblock")
class ElIfBlock(Block):
	"""
	AST node for an ``<?elif?>`` block.
	"""

	ul4attrs = Block.ul4attrs.union({"condition"})

	def __init__(self, template=None, startpos=None, stoppos=None, condition=None):
		super().__init__(template, startpos, stoppos)
		self.condition = condition

	def _repr(self):
		yield f" condition={self.condition!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("condition=")
		p.pretty(self.condition)
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def _str(self):
		yield "elif "
		yield from Code._str(self)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()


@register("elseblock")
class ElseBlock(Block):
	"""
	AST node for an ``<?else?>`` block.
	"""

	def _repr_pretty(self, p):
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def _str(self):
		yield "else:"
		yield None
		yield +1
		yield from super()._str()
		yield -1


@register("forblock")
class ForBlock(Block):
	"""
	AST node for a ``<?for?>`` loop.
	"""

	ul4attrs = Block.ul4attrs.union({"varname", "container"})

	def __init__(self, template=None, startpos=None, stoppos=None, varname=None, container=None):
		super().__init__(template, startpos, stoppos)
		self.varname = varname
		self.container = container

	def _repr(self):
		yield f"varname={self.varname!r}"
		yield f"container={self.container!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("varname=")
		p.pretty(self.varname)
		p.breakable()
		p.text("container=")
		p.pretty(self.container)
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.varname)
		encoder.dump(self.container)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.varname = decoder.load()
		self.container = decoder.load()

	def _str(self):
		yield "for "
		yield from Code._str(self)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	@_handleoutputeval
	def eval(self, context):
		container = self.container.eval(context)
		for item in container:
			for (lvalue, value) in _unpackvar(self.varname, item):
				lvalue.evalset(context, value)
			try:
				yield from super().eval(context)
			except BreakException:
				break
			except ContinueException:
				pass


@register("whileblock")
class WhileBlock(Block):
	"""
	AST node for a ``<?while?>`` loop.
	"""

	ul4attrs = Block.ul4attrs.union({"condition"})

	def __init__(self, template=None, startpos=None, stoppos=None, condition=None):
		super().__init__(template, startpos, stoppos)
		self.condition = condition

	def _repr(self):
		yield f"condition={self.condition!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("condition=")
		p.pretty(self.condition)
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()

	def _str(self):
		yield "while "
		yield from Code._str(self)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	@_handleoutputeval
	def eval(self, context):
		while 1:
			condition = self.condition.eval(context)
			if not condition:
				break
			try:
				yield from super().eval(context)
			except BreakException:
				break
			except ContinueException:
				pass


@register("break")
class Break(Code):
	"""
	AST node for a ``<?break?>`` inside a ``<?for?>`` block.
	"""

	def _str(self):
		yield "break"

	@_handleexpressioneval
	def eval(self, context):
		raise BreakException()


@register("continue")
class Continue(Code):
	"""
	AST node for a ``<?continue?>`` inside a ``<?for?>`` block.
	"""

	def _str(self):
		yield "continue"

	@_handleexpressioneval
	def eval(self, context):
		raise ContinueException()


@register("attr")
class Attr(Code):
	"""
	AST node for getting and setting an attribute of an object.

	The object is loaded from the AST node :obj:`obj` and the attribute name
	is stored in the string :obj:`attrname`.
	"""
	ul4attrs = AST.ul4attrs.union({"obj", "attrname"})

	def __init__(self, template=None, startpos=None, obj=None, attrname=None):
		super().__init__(template, startpos)
		self.obj = obj
		self.attrname = attrname

	def _repr(self):
		yield f"obj={self.obj!r}"
		yield f"attrname={self.attrname!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		p.breakable()
		p.text("attrname=")
		p.pretty(self.attrname)

	@_handleexpressioneval
	def eval(self, context):
		obj = self.obj.eval(context)
		try:
			return proto(obj).getattr(obj, self.attrname)
		except AttributeError:
			return UndefinedKey(self.attrname)

	@_handleexpressioneval
	def evalset(self, context, value):
		obj = self.obj.eval(context)
		proto(obj).setattr(obj, self.attrname, value)

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		obj = self.obj.eval(context)

		p = proto(obj)
		oldvalue = p.getattr(obj, self.attrname)
		newvalue = operator.evalfoldaug(oldvalue, value)
		p.setattr(obj, self.attrname, newvalue)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.attrname)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.attrname = decoder.load()


@register("slice")
class Slice(Code):
	"""
	AST node for creating a slice object (used in ``obj[index1:index2]``).

	The start and stop indices are loaded from  the AST nodes :obj:`index1` and
	:obj:`index2`. :obj:`index1` and :obj:`index2` may also be :const:`None`
	(for missing slice indices, which default to the 0 for the start index and
	the length of the sequence for the end index).
	"""

	ul4attrs = Code.ul4attrs.union({"index1", "index2"})

	def __init__(self, template=None, startpos=None, index1=None, index2=None):
		super().__init__(template, startpos)
		self.index1 = index1
		self.index2 = index2

	def _repr(self):
		if self.index1 is not None:
			yield f"index1={self.index1!r}"
		if self.index2 is not None:
			yield f"index2={self.index2!r}"

	def _repr_pretty(self, p):
		if self.index1 is not None:
			p.breakable()
			p.text("index1=")
			p.pretty(self.index1)
		if self.index2 is not None:
			p.breakable()
			p.text("index2=")
			p.pretty(self.index2)

	@_handleexpressioneval
	def eval(self, context):
		index1 = None
		if self.index1 is not None:
			index1 = self.index1.eval(context)
		index2 = None
		if self.index2 is not None:
			index2 = self.index2.eval(context)
		return slice(index1, index2)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.index1)
		encoder.dump(self.index2)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.index1 = decoder.load()
		self.index2 = decoder.load()


class Unary(Code):
	"""
	Base class for all AST nodes implementing unary operators.
	"""

	ul4attrs = Code.ul4attrs.union({"obj"})

	def __init__(self, template=None, startpos=None, obj=None):
		super().__init__(template, startpos)
		self.obj = obj

	def _repr(self):
		yield repr(self.obj)

	def _repr_pretty(self, p):
		p.breakable()
		p.pretty(self.obj)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()

	@_handleexpressioneval
	def eval(self, context):
		obj = self.obj.eval(context)
		return self.evalfold(obj)

	@classmethod
	def make(cls, tag, pos, obj):
		if isinstance(obj, Const):
			try:
				result = cls.evalfold(obj.value)
				if not isinstance(result, Undefined):
					return Const(tag, pos, result)
			except Exception:
				pass # If constant folding doesn't work, return the original AST
		return cls(tag, pos, obj)


@register("not")
class Not(Unary):
	"""
	AST node for the unary ``not`` operator.
	"""

	@classmethod
	def evalfold(cls, obj):
		return not obj


@register("neg")
class Neg(Unary):
	"""
	AST node for the unary negation (i.e. "-") operator.
	"""

	@classmethod
	def evalfold(cls, obj):
		return -obj


@register("bitnot")
class BitNot(Unary):
	"""
	AST node for the bitwise not operator.
	"""

	@classmethod
	def evalfold(cls, obj):
		return ~obj


@register("print")
class Print(Unary):
	"""
	AST node for a ``<?print?>`` tag.
	"""

	output = True

	def _str(self):
		yield "print "
		yield from super()._str()

	@_handleoutputeval
	def eval(self, context):
		yield context.output(_str(self.obj.eval(context)))


@register("printx")
class PrintX(Unary):
	"""
	AST node for a ``<?printx?>`` tag.
	"""

	output = True

	def _str(self):
		yield "printx "
		yield from super()._str()

	@_handleoutputeval
	def eval(self, context):
		yield context.output(_xmlescape(self.obj.eval(context)))


@register("return")
class Return(Unary):
	"""
	AST node for a ``<?return?>`` tag.
	"""

	def _str(self):
		yield "return "
		yield from super()._str()

	@_handleexpressioneval
	def eval(self, context):
		value = self.obj.eval(context)
		raise ReturnException(value)


class Binary(Code):
	"""
	Base class for all AST nodes implementing binary operators.
	"""

	ul4attrs = Code.ul4attrs.union({"obj1", "obj2"})

	def __init__(self, template=None, startpos=None, obj1=None, obj2=None):
		super().__init__(template, startpos)
		self.obj1 = obj1
		self.obj2 = obj2

	def _repr(self):
		yield repr(self.obj1)
		yield repr(self.obj2)

	def _repr_pretty(self, p):
		p.breakable()
		p.pretty(self.obj1)
		p.breakable()
		p.pretty(self.obj2)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj1)
		encoder.dump(self.obj2)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj1 = decoder.load()
		self.obj2 = decoder.load()

	@_handleexpressioneval
	def eval(self, context):
		obj1 = self.obj1.eval(context)
		obj2 = self.obj2.eval(context)
		return self.evalfold(obj1, obj2)

	@classmethod
	def make(cls, tag, pos, obj1, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const):
			try:
				result = cls.evalfold(obj1.value, obj2.value)
				if not isinstance(result, Undefined):
					return Const(tag, pos, result)
			except Exception:
				pass # If constant folding doesn't work, return the original AST
		return cls(tag, pos, obj1, obj2)


@register("item")
class Item(Binary):
	"""
	AST node for subscripting operator.

	The object (which must be a list, string or dict) is loaded from the AST
	node :obj:`obj1` and the index/key is loaded from the AST node :obj:`obj2`.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		try:
			return obj1[obj2]
		except KeyError:
			return UndefinedKey(obj2)

	@_handleexpressioneval
	def evalset(self, context, value):
		obj1 = self.obj1.eval(context)
		obj2 = self.obj2.eval(context)
		obj1[obj2] = value

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		obj1 = self.obj1.eval(context)
		obj2 = self.obj2.eval(context)
		oldvalue = obj1[obj2]
		newvalue = operator.evalfoldaug(oldvalue, value)
		obj1[obj2] = newvalue


@register("is")
class Is(Binary):
	"""
	AST node for the binary ``is`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 is obj2


@register("isnot")
class IsNot(Binary):
	"""
	AST node for the binary ``is not`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 is not obj2


@register("eq")
class EQ(Binary):
	"""
	AST node for the binary ``==`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 == obj2


@register("ne")
class NE(Binary):
	"""
	AST node for the binary ``!=`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 != obj2


@register("lt")
class LT(Binary):
	"""
	AST node for the binary ``<`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 < obj2


@register("le")
class LE(Binary):
	"""
	AST node for the binary ``<=`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 <= obj2


@register("gt")
class GT(Binary):
	"""
	AST node for the binary ``>`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 > obj2


@register("ge")
class GE(Binary):
	"""
	AST node for the binary ``>=`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 >= obj2


@register("contains")
class Contains(Binary):
	"""
	AST node for the binary containment testing operator.

	The item/key object is loaded from the AST node :obj:`obj1` and the container
	object (which must be a list, string, dict or an object with a ``ul4attrs``
	attribute) is loaded from the AST node :obj:`obj2`.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 in obj2


@register("notcontains")
class NotContains(Binary):
	"""
	AST node for the inverted containment testing operator.

	The item/key object is loaded from the AST node :obj:`obj1` and the container
	object (which must be a list, string, dict or an object with a ``ul4attrs``
	attribute) is loaded from the AST node :obj:`obj2`.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 not in obj2


@register("add")
class Add(Binary):
	"""
	AST node for the binary addition operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 + obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 += obj2
		return obj1


@register("sub")
class Sub(Binary):
	"""
	AST node for the binary subtraction operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 - obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 -= obj2
		return obj1


@register("mul")
class Mul(Binary):
	"""
	AST node for the binary multiplication operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 * obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 *= obj2
		return obj1


@register("floordiv")
class FloorDiv(Binary):
	"""
	AST node for the binary truncating division operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 // obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 //= obj2
		return obj1


@register("truediv")
class TrueDiv(Binary):
	"""
	AST node for the binary true division operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 / obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 /= obj2
		return obj1


@register("mod")
class Mod(Binary):
	"""
	AST node for the binary modulo operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 % obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 %= obj2
		return obj1


@register("shiftleft")
class ShiftLeft(Binary):
	"""
	AST node for the bitwise left shift operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 << obj2 if obj2 >= 0 else obj1 >> -obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		if obj2 >= 0:
			obj1 <<= obj2
		else:
			obj1 >>= -obj2
		return obj1


@register("shiftright")
class ShiftRight(Binary):
	"""
	AST node for the bitwise right shift operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 >> obj2 if obj2 >= 0 else obj1 << -obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		if obj2 >= 0:
			obj1 >>= obj2
		else:
			obj1 <<= -obj2
		return obj1


@register("bitand")
class BitAnd(Binary):
	"""
	AST node for the binary bitwise and operator (``&``).
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		return obj1 & obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		obj1 &= obj2
		return obj1


@register("bitxor")
class BitXOr(Binary):
	"""
	AST node for the binary bitwise exclusive or operator (``^``).
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		return obj1 ^ obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		obj1 ^= obj2
		return obj1


@register("bitor")
class BitOr(Binary):
	"""
	AST node for the binary bitwise or operator (``|``).
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		return obj1 | obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		obj1 |= obj2
		return obj1


@register("and")
class And(Binary):
	"""
	AST node for the binary ``and`` operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		# This is not called from ``eval``, as it doesn't short-circuit
		return obj1 and obj2

	@_handleexpressioneval
	def eval(self, context):
		obj1 = self.obj1.eval(context)
		if not obj1:
			return obj1
		return self.obj2.eval(context)


@register("or")
class Or(Binary):
	"""
	AST node for the binary ``or`` operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		# This is not called from ``eval``, as it doesn't short-circuit
		return obj1 or obj2

	@_handleexpressioneval
	def eval(self, context):
		obj1 = self.obj1.eval(context)
		if obj1:
			return obj1
		return self.obj2.eval(context)


@register("if")
class If(Code):
	"""
	AST node for the ternary inline ``if/else`` operator.
	"""

	ul4attrs = Code.ul4attrs.union({"objif", "objcond", "objelse"})

	def __init__(self, template=None, startpos=None, objif=None, objcond=None, objelse=None):
		super().__init__(template, startpos)
		self.objif = objif
		self.objcond = objcond
		self.objelse = objelse

	def _repr(self):
		yield f"objif={self.objif!r}"
		yield f"objcond={self.objcond!r}"
		yield f"objelse={self.objelse!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.pretty(self.objif)
		p.breakable()
		p.pretty(self.objcond)
		p.breakable()
		p.pretty(self.objelse)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.objif)
		encoder.dump(self.objcond)
		encoder.dump(self.objelse)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.objif = decoder.load()
		self.objcond = decoder.load()
		self.objelse = decoder.load()

	@classmethod
	def make(cls, tag, pos, objif, objcond, objelse):
		if isinstance(objcond, Const) and not isinstance(objcond.value, Undefined):
			return objif if objcond.value else objelse
		return cls(tag, pos, objif, objcond, objelse)

	@_handleexpressioneval
	def eval(self, context):
		if self.objcond.eval(context):
			return self.objif.eval(context)
		else:
			return self.objelse.eval(context)


class ChangeVar(Code):
	"""
	Baseclass for all AST nodes that store or modify a variable.

	The left hand side is loaded from the AST node :obj:`label` and the value that
	will be stored or be used to modify the stored value is loaded from the
	AST node :obj:`value`.
	"""

	ul4attrs = Code.ul4attrs.union({"lvalue", "value"})

	def __init__(self, template=None, startpos=None, lvalue=None, value=None):
		super().__init__(template, startpos)
		self.lvalue = lvalue
		self.value = value

	def _repr(self):
		yield f"lvalue={self.lvalue!r}"
		yield f"value={self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("lvalue=")
		p.pretty(self.lvalue)
		p.breakable()
		p.text("value=")
		p.pretty(self.value)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.lvalue)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.lvalue = decoder.load()
		self.value = decoder.load()


@register("setvar")
class SetVar(ChangeVar):
	"""
	AST node that stores a value into a variable.
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalset(context, value)


@register("addvar")
class AddVar(ChangeVar):
	"""
	AST node that adds a value to a variable (i.e. the ``+=`` operator).
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, Add, value)


@register("subvar")
class SubVar(ChangeVar):
	"""
	AST node that subtracts a value from a variable (i.e. the ``-=`` operator).
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, Sub, value)


@register("mulvar")
class MulVar(ChangeVar):
	"""
	AST node that multiplies a variable by a value (i.e. the ``*=`` operator).
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, Mul, value)


@register("floordivvar")
class FloorDivVar(ChangeVar):
	"""
	AST node that divides a variable by a value (truncating to an integer value;
	i.e. the ``//=`` operator).
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, FloorDiv, value)


@register("truedivvar")
class TrueDivVar(ChangeVar):
	"""
	AST node that divides a variable by a value (i.e. the ``/=`` operator).
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, TrueDiv, value)


@register("modvar")
class ModVar(ChangeVar):
	"""
	AST node for the ``%=`` operator.
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, Mod, value)


@register("shiftleftvar")
class ShiftLeftVar(ChangeVar):
	"""
	AST node for the ``<<=`` operator.
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, ShiftLeft, value)


@register("shiftrightvar")
class ShiftRightVar(ChangeVar):
	"""
	AST node for the ``>>=`` operator.
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, ShiftRight, value)


@register("bitandvar")
class BitAndVar(ChangeVar):
	"""
	AST node for the ``&=`` operator.
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, BitAnd, value)


@register("bitxorvar")
class BitXOrVar(ChangeVar):
	"""
	AST node for the ``^=`` operator.
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, BitXOr, value)


@register("bitorvar")
class BitOrVar(ChangeVar):
	"""
	AST node for the ``|=`` operator.
	"""

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, BitOr, value)


@register("call")
class Call(Code):
	"""
	AST node for calling an object.

	The object to be called is stored in the attribute :obj:`obj`. The list of
	arguments is found in :obj:`args`.
	"""

	ul4attrs = Code.ul4attrs.union({"obj", "args"})

	def __init__(self, template=None, startpos=None, obj=None):
		super().__init__(template, startpos)
		self.obj = obj
		self.args = []

	def _repr(self):
		yield f"obj={self.obj!r}"
		for arg in self.args:
			yield from arg._repr()

	def _repr_pretty(self, p):
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		for arg in self.args:
			p.breakable()
			p.pretty(arg)

	@staticmethod
	def _call(context, obj, args, kwargs):
		ul4call = getattr(obj, "ul4call", None)
		if callable(ul4call):
			obj = ul4call

		needscontext = getattr(obj, "ul4context", False)

		if needscontext:
			return obj(context, *args, **kwargs)
		else:
			return obj(*args, **kwargs)

	def eval(self, context):
		obj = self.obj.eval(context)
		args = []
		kwargs = {}
		for arg in self.args:
			arg.eval_call(context, args, kwargs)

		try:
			return self._call(context, obj, args, kwargs)
		except Exception as exc:
			if inspect.ismethod(obj):
				_decorateexception(exc, self, obj.__self__)
			else:
				_decorateexception(exc, self, obj)
			raise

	@_handleexpressioneval
	def evalset(self, context, value):
		raise TypeError("can't use = on call result")

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		raise TypeError("augmented assigment not allowed for call result")

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.args)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.args = decoder.load()


@register("render")
class Render(Call):
	"""
	AST node for rendering a template.

	The template to be rendered is stored in the attribute :obj:`obj`. The list
	of arguments is found in :obj:`args`.
	"""

	ul4attrs = Call.ul4attrs.union({"indent"})

	def __init__(self, template=None, startpos=None, obj=None):
		super().__init__(template, startpos, obj)
		self.indent = None # The indentation before this ``<?render?>``/``<?renderx?>`` tag, i.e. the sibling AST node before ``self``

	output = True

	def _repr(self):
		yield f"indent={self.indent!r}"
		yield f"obj={self.obj!r}"
		for arg in self.args:
			yield from arg._repr()

	def _repr_pretty(self, p):
		p.breakable()
		p.text("indent=")
		p.pretty(self.indent)
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		for arg in self.args:
			p.breakable()
			p.pretty(arg)

	def _evalobjargs(self, context):
		obj = self.obj.eval(context)
		args = []
		kwargs = {}
		for arg in self.args:
			arg.eval_call(context, args, kwargs)
		return (obj, args, kwargs)

	def _renderobject(self, context, obj, args, kwargs):
		try:
			ul4render = getattr(obj, "ul4render", None)
			if callable(ul4render):
				if self.indent is not None:
					context.indents.append(self.indent.text)
				needscontext = getattr(ul4render, "ul4context", False)
				if needscontext:
					yield from ul4render(context, *args, **kwargs)
				else:
					yield from ul4render(*args, **kwargs)
				if self.indent is not None:
					context.indents.pop()
			else:
				raise TypeError(f"{misc.format_class(obj)} object can't be rendered")
		except Exception as exc:
			if inspect.ismethod(obj):
				_decorateexception(exc, self, obj.__self__)
			else:
				_decorateexception(exc, self, obj)
			raise

	def eval(self, context):
		(obj, args, kwargs) = self._evalobjargs(context)
		yield from self._renderobject(context, obj, args, kwargs)

	@_handleexpressioneval
	def evalset(self, context, value):
		raise TypeError("can't use = on call result")

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		raise TypeError("augmented assigment not allowed for call result")

	def _str(self):
		yield self.type
		yield " "
		yield from super()._str()
		if self.indent is not None:
			yield f" with indent {self.indent.text!r}"

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.indent)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.indent = decoder.load()


@register("renderx")
class RenderX(Render):
	def eval(self, context):
		context.escapes.append(_xmlescape)
		try:
			yield from Render.eval(self, context)
		finally:
			context.escapes.pop()


@register("renderblock")
class RenderBlock(Render):
	"""
	AST node for rendering a template and passing one additional argument that is
	the anonymous template that is defined in the block with will be passed as
	the keyword argument ``content``.

	The object to be called is stored in the attribute :obj:`obj`. The list of
	arguments is found in :obj:`args`.
	"""

	ul4attrs = Render.ul4attrs.union({"stoppos", "stopline", "stopcol", "stopsource", "stopsourceprefix", "stopsourcesuffix", "content"})

	def __init__(self, template=None, startpos=None, stoppos=None, obj=None):
		super().__init__(template, startpos, obj)
		self._stoppos = None
		self.content = None

	def append(self, item):
		self.content.content.append(item)

	def finish(self, endtag):
		self.stoppos = endtag.startpos
		self.content.startpos = slice(self.content.startpos.start, self.content.startpos.start)
		self.content.stoppos = slice(endtag.startpos.start, endtag.startpos.start)

	def eval(self, context):
		(obj, args, kwargs) = self._evalobjargs(context)

		# Check that the argument ``content`` hasn't been specified yet
		if "content" in kwargs:
			raise TypeError(f"multiple values for keyword argument 'content'")
		kwargs["content"] = TemplateClosure(self.content, context, None)

		yield from self._renderobject(context, obj, args, kwargs)

	def _str(self):
		yield self.type
		yield " "
		yield from Code._str(self)
		if self.indent is not None:
			yield f" with indent {self.indent.text!r}"
		yield ":"
		yield None
		yield +1
		yield from Block._str(self.content)
		yield -1

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self._stoppos)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.stoppos = decoder.load()
		self.content = decoder.load()


@register("renderblocks")
class RenderBlocks(Render):
	"""
	AST node for rendering a template and passing additional arguments via
	nested variable definitions.

	The object to be called is stored in the attribute :obj:`obj`. The list of
	arguments is found in :obj:`args`.
	"""

	ul4attrs = Render.ul4attrs.union({"stoppos", "stopline", "stopcol", "stopsource", "stopsourceprefix", "stopsourcesuffix", "content"})

	def __init__(self, template=None, startpos=None, stoppos=None, obj=None):
		super().__init__(template, startpos, obj)
		self._stoppos = stoppos
		self.content = []

	def append(self, item):
		self.content.append(item)

	def finish(self, endtag):
		self.stoppos = endtag.startpos

	def _str(self):
		yield self.type
		yield " "
		yield from Code._str(self) # Note that :class:`Block` is *not* one of our base classes, but as long as be have the proper attributes...
		if self.indent is not None:
			yield f" with indent {self.indent.text!r}"
		yield ":"
		yield None
		yield +1
		yield from Block._str(self)
		yield -1

	def _repr_pretty(self, p):
		p.breakable()
		p.text("indent=")
		p.pretty(self.indent)
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		for arg in self.args:
			p.breakable()
			p.pretty(arg)
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def _repr(self):
		yield f"indent={self.indent!r}"
		yield f"obj={self.obj!r}"
		for arg in self.args:
			yield from arg._repr()

	def eval(self, context):
		(obj, args, kwargs) = self._evalobjargs(context)

		# Open a new chained variable dict, so we can collect all variables defined inside the block
		with context.chainvars():
			# Evaluate the block content and ignore output
			# (Note that we're not a subclass of :class:`Block`, but have the correct attributes)
			for output in Block.eval(self, context):
				pass

			# Check that we have no duplicate arguments
			vars = context.vars.maps[0]
			for key in vars:
				if key in kwargs:
					raise TypeError(f"multiple values for keyword argument {key!r}")

			# Copy variables from the block into the keyword arguments (but only the outermost map from the chain)
			kwargs.update(vars)

		yield from self._renderobject(context, obj, args, kwargs)

	@_handleexpressioneval
	def evalset(self, context, value):
		raise TypeError("can't use = on call result")

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		raise TypeError("augmented assigment not allowed for call result")

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self._stoppos)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.stoppos = decoder.load()
		self.content = decoder.load()


@register("template")
class Template(Block):
	"""
	A template object is normally created by passing the template source to the
	constructor. It can also be loaded from the compiled format via the class
	methods :meth:`load` (from a stream) or :meth:`loads` (from a string).

	The compiled format can be generated with the methods :meth:`dump` (which
	dumps the format to a stream) or :meth:`dumps` (which returns a string with
	the compiled format).

	Rendering the template can be done with the methods :meth:`render` (which
	is a generator) or :meth:`renders` (which returns a string).

	A :class:`Template` can also be called as a function (returning the result
	of the first ``<?return?>`` tag encountered). In this case all output of the
	template will be ignored.

	A :class:`Template` object is itself an AST node. Evaluating it will store
	the template object under its name in the local variables.
	"""
	ul4attrs = Block.ul4attrs.union({"signature", "doc", "name", "whitespace", "startdelim", "enddelim", "parenttemplate", "fullsource", "renders"})

	version = "47"

	output = False # Evaluating a template doesn't produce output, but simply stores it in a local variable

	def __init__(self, source=None, name=None, whitespace="keep", startdelim="<?", enddelim="?>", signature=None):
		"""
		Create a :class:`Template` object.

		If :obj:`source` is ``None``, the :class:`Template` remains uninitialized,
		otherwise :obj:`source` will be compiled (using :obj:`startdelim` and
		:obj:`enddelim` as the tag delimiters).

		:obj:`name` is the name of the template. It will be used in exception
		messages and should be a valid Python identifier.

		:obj:`whitespace` specifies how whitespace is handled in the literal text
		in templates (i.e. the text between the tags):

		``"keep"``
			Whitespace is kept as it is.

		``"strip"``
			Strip linefeeds and the following indentation from the text.
			However trailing whitespace at the end of the line will still be
			honored.

		``"smart"``
			If a line contains only indentation and one tag that isn't a ``print``
			or ``printx`` tag, the indentation and the linefeed after the tag
			will be stripped from the text. Furthermore the additional indentation
			that might be introduced by a ``for``, ``if``, ``elif``, ``else`` or
			``def`` block will be ignored. So for example the output of::

				<?code langs = ["Python", "Java", "Javascript"]?>
				<?if langs?>
					<?for lang in langs?>
						<?print lang?>
					<?end for?>
				<?end if?>

			will simply be::

				Python
				Java
				Javascript

			without any additional empty lines or indentation.

		(Output will always be ignored when calling a template as a function.)

		:obj:`signature` is the signature of the template. For a top level
		template it can be:

		``None``
			The template will accept all keyword arguments.

		An :class:`inspect.Signature` object
			This signature will be used as the signature of the template.

		A callable
			The signature of the callable will be used.

		A string
			The signature as a string, i.e. something like
			``"x, y=42, *args, **kwargs"``. This string will be parsed and
			evaluated to create the signature for the template.

		If the template is a subtemplate (i.e. a template defined by another
		template via ``<?def t?>...<?end def?>``), :obj:`signature` can be:

		``None``
			The template will accept all arguments.

		A :class:`Signature` object
			This AST node will be evaluated at the point of definition of the
			subtemplate to create the final signature of the subtemplate.
		"""
		super().__init__(self, slice(0, 0), None)
		self.whitespace = whitespace
		self.startdelim = startdelim or "<?"
		self.enddelim = enddelim or "?>"
		self.name = name
		self._fullsource = None
		self.docpos = None
		self.parenttemplate = None
		if isinstance(signature, str):
			# The parser needs a tag, and each tag references its template which contains the source.
			# So to make the source of the signature available in the source, we prepend an ``<?ul4?>`` tag
			source = f"{self.startdelim}ul4 {name or ''}({signature}){self.enddelim}{source}"
			signature = None
		elif callable(signature):
			signature = inspect.signature(signature)
		self.signature = signature

		# If we have source code compile it
		if source is not None:
			stop = len(source)
			self.stoppos = slice(stop, stop)
			self._compile(source, startdelim, enddelim)
		else:
			self._fullsource = ""
			self.stoppos = self._startpos

	def _repr(self):
		yield f"name={self.name!r}"
		yield f"whitespace={self.whitespace!r}"
		if self.startdelim != "<?":
			yield f"startdelim={self.startdelim!r}"
		if self.enddelim != "?>":
			yield f"enddelim={self.enddelim!r}"
		if self.signature is not None:
			yield f"signature={self.signature}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("name=")
		p.pretty(self.name)
		p.breakable()
		p.text("whitespace=")
		p.pretty(self.whitespace)
		if self.startdelim != "<?":
			p.breakable()
			p.text("startdelim=")
			p.pretty(self.startdelim)
		if self.enddelim != "?>":
			p.breakable()
			p.text("enddelim=")
			p.pretty(self.enddelim)
		if self.signature is not None:
			p.breakable()
			if isinstance(self.signature, Signature):
				p.text("signature=")
				p.pretty(self.signature)
			else:
				p.text(f"signature={self.signature}")
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def _str(self):
		yield "def "
		yield self.name if self.name is not None else "unnamed"
		if self.signature is not None:
			if isinstance(self.signature, Signature):
				yield from self.signature._str()
			else:
				yield str(self.signature)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	@property
	def doc(self):
		return self._fullsource[self.docpos] if self.docpos is not None else None

	def ul4getattr(self, name):
		if name == "renders":
			return self.ul4renders
		else:
			return getattr(self, name)

	def ul4ondump(self, encoder):
		# Don't call ``super().ul4ondump()`` first, as we want the version to be first
		encoder.dump(self.version)
		encoder.dump(self.name)
		encoder.dump(self._fullsource)
		encoder.dump(self.whitespace)
		encoder.dump(self.startdelim)
		encoder.dump(self.enddelim)
		encoder.dump(self.docpos)
		encoder.dump(self.parenttemplate)

		# Signature can be ``None`` or an instance of :class:`inspect.Signature` or :class:`Signature`
		if self.signature is None or isinstance(self.signature, Signature):
			encoder.dump(self.signature)
		else:
			# Serialize an instance of :class:`inspect.Signature` as a flat list
			# e.g. ['x', 'y=', 42, '*args', '**kwargs'] for the signature ``(x, y=42, *args, **kwargs)``
			dump = []
			for param in self.signature.parameters.values():
				if param.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD:
					if param.default is inspect.Parameter.empty:
						dump.append(param.name)
					else:
						dump.append(param.name + "=")
						dump.append(param.default)
				elif param.kind is inspect.Parameter.VAR_POSITIONAL:
					dump.append("*" + param.name)
				elif param.kind is inspect.Parameter.VAR_KEYWORD:
					dump.append("**" + param.name)
				else:
					raise ValueError(f"can't dump parameter {param.name} of type {param.kind}")
			encoder.dump(dump)

		super().ul4ondump(encoder)

	def ul4onload(self, decoder):
		version = decoder.load()
		# If the loaded version is ``None``, this is not a "compiled" version of the template,
		# but a "source" version. It only contains the info required to compile the template.
		#
		# Not all implementations (i.e. the Javascript one) support this mode.
		#
		# This is implemented so that the PL/SQL version can put templates into UL4ON dumps.
		if version is None: # dump is in "source" form
			self.name = decoder.load()
			source = decoder.load()
			signature = decoder.load()
			self.whitespace = decoder.load()
			startdelim = decoder.load()
			if startdelim is None:
				startdelim = "<?"
			enddelim = decoder.load()
			if enddelim is None:
				enddelim = "?>"
			if signature is not None:
				source = f"{startdelim}ul4 {self.name or ''}({signature}){enddelim}{source}"
			# Remove old content, before compiling the source
			self.startpos = slice(0, 0)
			stop = len(source)
			self.stoppos = slice(stop, stop)
			del self.content[:]
			self._compile(source, startdelim, enddelim)
		else: # dump is in compiled form
			if version != self.version:
				raise ValueError(f"invalid version, expected {self.version!r}, got {version!r}")
			self.name = decoder.load()
			self._fullsource = decoder.load()
			self.whitespace = decoder.load()
			self.startdelim = decoder.load()
			self.enddelim = decoder.load()
			self.docpos = decoder.load()
			self.parenttemplate = decoder.load()

			dump = decoder.load()
			if dump is None or isinstance(dump, Signature):
				self.signature = dump
			else:
				params = []
				nextdefault = False
				paramname = None
				for param in dump:
					if nextdefault:
						params.append(inspect.Parameter(paramname, inspect.Parameter.POSITIONAL_OR_KEYWORD, default=param))
						nextdefault = False
					else:
						if param.endswith("="):
							paramname = param[:-1]
							nextdefault = True # The next item is the default value
						elif param.startswith("**"):
							params.append(inspect.Parameter(param[2:], inspect.Parameter.VAR_KEYWORD))
						elif param.startswith("*"):
							params.append(inspect.Parameter(param[1:], inspect.Parameter.VAR_POSITIONAL))
						else:
							params.append(inspect.Parameter(param, inspect.Parameter.POSITIONAL_OR_KEYWORD))
				self.signature = inspect.Signature(params)
			super().ul4onload(decoder)

	@classmethod
	def loads(cls, data):
		"""
		The class method :meth:`loads` loads the template from string :obj:`data`.
		:obj:`data` must contain the template in compiled UL4ON format.
		"""
		from ll import ul4on
		return ul4on.loads(data)

	@classmethod
	def load(cls, stream):
		"""
		The class method :meth:`load` loads the template from the stream
		:obj:`stream`. The stream must contain the template in compiled UL4ON
		format.
		"""
		from ll import ul4on
		return ul4on.load(stream)

	def dump(self, stream):
		"""
		:meth:`dump` dumps the template in compiled UL4ON format to the
		stream :obj:`stream`.
		"""
		from ll import ul4on
		ul4on.dump(self, stream)

	def dumps(self):
		"""
		:meth:`dumps` returns the template in compiled UL4ON format
		(as a string).
		"""
		from ll import ul4on
		return ul4on.dumps(self)

	def _renderbound(self, context):
		# Helper method used by :meth:`render` and :meth:`TemplateClosure.render` where arguments have already been bound
		try:
			# Bypass ``self.eval()`` which simply stores the object as a local variable
			# Also bypass ``super().eval()`` as this would add additional stackframe in exception messages
			for node in self.content:
				result = node.eval(context)
				if node.output:
					yield from result
		except ReturnException:
			pass

	@withcontext
	def ul4render(*args, **kwargs):
		self = args[0]
		context = args[1]
		args = args[2:]
		vars = _makevars(self.signature, args, kwargs)
		with context.replacevars(vars):
			yield from self._renderbound(context)

	def render(*args, **kwargs):
		"""
		Render the template iteratively (i.e. this is a generator).
		:obj:`args[1:]` and :obj:`kwargs` contain the top level variables available
		to the template code. (:obj:`args[0]` is the ``self`` parameter, but
		:meth:`render` is defined in this way, to allow a keyword argument named
		``self``).
		"""
		context = Context()
		yield from args[0].ul4render(context, *args[1:], **kwargs)

	def _rendersbound(self, context):
		# Helper method used by :meth:`renders` and :meth:`TemplateClosure.renders` where arguments have already been bound
		return "".join(self._renderbound(context))

	@withcontext
	def ul4renders(*args, **kwargs): # This will be exposed to UL4 as ``renders``
		self = args[0]
		context = args[1]
		args = args[2:]
		vars = _makevars(self.signature, args, kwargs)
		with context.replacevars(vars):
			return self._rendersbound(context)

	def renders(*args, **kwargs):
		"""
		Render the template as a string. :obj:`args[1:]` and :obj:`kwargs` contain
		the top level variables available to the template code. (:obj:`args[0]`
		is the ``self`` parameter, but :meth:`renders` is defined in this way,
		to allow a keyword argument named ``self``).
		"""
		context = Context()
		return args[0].ul4renders(context, *args[1:], **kwargs)

	def _callbound(self, context):
		# Helper method used by :meth:`__call__` and :meth:`TemplateClosure.__call__` where arguments have already been bound
		try:
			for output in super().eval(context): # Bypass ``self.eval()`` which simply stores the object as a local variable
				pass # Ignore all output
		except ReturnException as exc:
			return exc.value

	@withcontext
	def ul4call(*args, **kwargs):
		"""
		Call the template as a function and return the resulting value.
		:obj:`args[1:]` and :obj:`kwargs` contain the top level variables available
		to the template code. (:obj:`args[0]` is the ``self`` parameter, but
		:meth:`ul4call` is defined in this way, to allow a keyword argument named
		``self``).
		"""
		self = args[0]
		context = args[1]
		args = args[2:]
		vars = _makevars(self.signature, args, kwargs)
		with context.replacevars(vars):
			return self._callbound(context)

	def __call__(*args, **kwargs):
		"""
		Call the template as a function and return the resulting value.
		:obj:`args[1:]` and :obj:`kwargs` contain the top level variables available
		to the template code. (:obj:`args[0]` is the ``self`` parameter, but
		:meth:`__call__` is defined in this way, to allow a keyword argument named
		``self``).
		"""
		context = Context()
		return args[0].ul4call(context, *args[1:], **kwargs)

	def jssource(self):
		"""
		Return the template as the source code of a Javascript function.
		"""
		return f"ul4.loads({_asjson(self.dumps())})"

	def javasource(self):
		"""
		Return the template as Java source code.
		"""
		return f"com.livinglogic.ul4.InterpretedTemplate.loads({misc.javaexpr(self.dumps())})"

	def _tokenize(self, source, startdelim, enddelim):
		"""
		Tokenize the template source code in :obj:`source` into tags and non-tag
		text. :obj:`startdelim` and :obj:`enddelim` are used as the tag delimiters.

		This is a generator which produces :class:`Text`/:class:`Tag` objects
		for each tag or non-tag text. It will be called by :meth:`_compile`
		internally.
		"""
		pattern = fr"{re.escape(startdelim)}\s*(ul4|whitespace|printx|print|code|for|while|if|elif|else|end|break|continue|def|return|renderblocks|renderblock|renderx|render|note|doc)(\s*((.|\n)*?)\s*)?{re.escape(enddelim)}"
		pos = 0
		for match in re.finditer(pattern, source):
			if match.start() != pos:
				yield Text(self, slice(pos, match.start()))
			tagname = source[match.start(1):match.end(1)]
			yield Tag(self, tagname, slice(match.start(), match.end()), slice(match.start(3), match.end(3)))
			pos = match.end()
		end = len(source)
		if pos != end:
			yield Text(self, slice(pos, end))

	def _tags2lines(self, tags):
		"""
		Transforms an iterable of tags into an iterable of lines by splitting the
		literal text between the tags into lines.

		A line is a list of nodes and will start with an :class:`Indent` node
		(containing the indenting whitespace if the line is indented, or an empty
		indentation if it isn't) and might end with a :class:`LineEnd` node
		(containing the line feed if the line is terminated (which most lines
		(except maybe the last one) are)).
		"""
		# a list of tags that are all part of one line
		tagline = []

		def append(tag):
			# If this is a new line and it doesn't start with an indentation,
			# add an empty indentation at the start (We always add indentation,
			# as this is used by :class:`Render` to reindent the output of one
			# template when called from inside another template)
			if not tagline and not isinstance(tag, Indent):
				tagline.append(Indent(tag.template, slice(tag._startpos.start, tag._startpos.start)))
			tagline.append(tag)

		# Yield lines by splitting literal text into multiple chunks (normal text, indentation and lineends)
		wastag = False
		for tag in tags:
			if isinstance(tag, Text):
				pos = tag._startpos.start
				for line in tag.text.splitlines(True):
					# Find out if the line ends with a lineend
					linelen = len(line)
					for lineend in self._whitespace_lineends:
						if line.endswith(lineend):
							lineendlen = len(lineend)
							line = line[:-lineendlen]
							linelen -= lineendlen
							break
					else:
						lineendlen = 0

					# Find out how the line is indented
					if wastag:
						lineindentlen = 0
						wastag = False # Done inside the loop, because all lines after the first one must always be checked for indentation
					else:
						lineindentlen = len(line)-len(line.lstrip())
						linelen -= lineindentlen

					# Output the parts we found
					if lineindentlen:
						append(Indent(tag.template, slice(pos, pos+lineindentlen)))
						pos += lineindentlen
					if linelen:
						append(Text(tag.template, slice(pos, pos+linelen)))
						pos += linelen
					if lineendlen:
						append(LineEnd(tag.template, slice(pos, pos+lineendlen)))
						pos += lineendlen
						yield tagline
						tagline = []
			else:
				append(tag)
				wastag = True
		if tagline:
			yield tagline

	def _whitespace_keep(self, lines):
		for line in lines:
			yield from line

	def _whitespace_strip(self, lines):
		first = True
		for line in lines:
			for tag in line:
				if first or not isinstance(tag, (Indent, LineEnd)):
					yield tag
					first = False

	_whitespace_lineends = ("\r\n", "\n")

	def _whitespace_smart(self, lines):
		def indent(tagline):
			# Return the indentation of the line
			if tagline:
				return tagline[0].text
			return ""

		def isempty(tagline):
			return all(isinstance(tag, (Indent, LineEnd)) for tag in tagline)

		# Records the starting and ending line number of a block and its indentation
		class Block:
			def __init__(self, start):
				self.start = start
				self.stop = None
				self.indent = None

		# Return the length of the longest common prefix of all strings in :obj:`indents`
		def commonindentlen(indents):
			if not indents:
				return 0
			indent1 = min(indents)
			indent2 = max(indents)
			for (i, c) in enumerate(indent1):
				if c != indent2[i]:
					return i
			return len(indent1)

		# Step 1: Determine the block structure of the lines
		blocks = [] # List of all blocks
		stack = [] # Stack of currently "open" blocks

		newlines = []
		for (i, line) in enumerate(lines):
			linelen = len(line)
			if 2 <= linelen <= 3 and isinstance(line[0], Indent) and isinstance(line[1], Tag) and line[1].tag not in ("print", "printx", "render", "renderx") and (linelen == 2 or isinstance(line[2], LineEnd)):
				tag = line[1]
				# Tags closing a block
				if tag.tag in ("elif", "else", "end"):
					if stack:
						stack[-1].stop = i # Previous block ends before this line
						stack.pop()
				newlines.append((line, stack[:]))
				# Tags opening a block
				if tag.tag in ("for", "if", "def", "elif", "else", "renderblock", "renderblocks"):
					block = Block(i+1) # Block starts on the next line
					stack.append(block)
					blocks.append(block)
			else:
				newlines.append((line, stack[:]))
		# Close open blocks (shouldn't be necessary for properly nested templates)
		for block in stack:
			block.stop = len(lines)

		# Step 2: Find the outer and inner indentation of all blocks
		for block in blocks:
			block.indent = range(
				# outer indent, i.e. the indentation of the start tag of the block
				len(indent(lines[block.start-1])) if block.start else 0,
				# inner indentation (ignoring lines that only contain whitespace)
				commonindentlen([indent(line) for line in itertools.islice(lines, block.start, block.stop) if not isempty(line)]),
			)

		# Step 3: Fix the indentation
		allindents = {}
		for (line, blocks) in newlines:
			if line:
				# use all character for indentation that are not part of the "artificial" indentation introduced in each block
				newindent = "".join(c for (i, c) in enumerate(line[0].text) if not any(i in block.indent for block in blocks))
				# Reuse previous indent string if we already have it (minizes memory usage and UL4ON dump size)
				newindent = allindents.setdefault(newindent, newindent)
				line[0]._settext(newindent)

		# Step 4: Drop whitespace from empty lines or lines that only contain indentation and block tags
		for line in lines:
			if len(line) == 2 and isinstance(line[0], Indent) and isinstance(line[1], LineEnd):
				del line[0]
			elif len(line) == 2 and isinstance(line[0], Indent) and isinstance(line[1], Tag) and line[1].tag not in ("print", "printx", "render", "renderx"):
				del line[0]
			elif len(line) == 3 and isinstance(line[0], Indent) and isinstance(line[1], Tag) and line[1].tag not in ("print", "printx", "render", "renderx") and isinstance(line[2], LineEnd):
				del line[2]
				del line[0]
			elif len(line) == 3 and isinstance(line[0], Indent) and isinstance(line[1], Tag) and line[1].tag in ("render", "renderx") and isinstance(line[2], LineEnd):
				del line[2]

		# Step 5: Yield the individual :class:`Tag`/:class:`Text` objects
		for line in lines:
			yield from line

	def _parser(self, tag, error):
		from ll import UL4Lexer, UL4Parser
		source = tag.code
		if not source:
			raise ValueError(error)
		stream = antlr3.ANTLRStringStream(source)
		lexer = UL4Lexer.UL4Lexer(stream)
		lexer.tag = tag
		tokens = antlr3.CommonTokenStream(lexer)
		parser = UL4Parser.UL4Parser(tokens)
		parser.tag = tag
		return parser

	def _compile(self, source, startdelim, enddelim):
		"""
		Compile the template source code :obj:`source` into an AST.
		:obj:`startdelim` and :obj:`enddelim` are used as the tag delimiters.
		"""
		self._fullsource = source
		self.startdelim = startdelim
		self.enddelim = enddelim

		if source is None:
			return

		blockstack = [self] # This stack stores the nested for/if/elif/else/def blocks
		templatestack = [self] # This stack stores the nested templates

		def parsedeclaration(tag):
			try:
				return self._parser(tag, "declaration required").definition()
			except Exception as exc:
				_decorateexception(exc, template)
				raise

		def parseexpr(tag):
			return self._parser(tag, "expression required").expression()

		def parsestmt(tag):
			return self._parser(tag, "statement required").statement()

		def parsefor(tag):
			return self._parser(tag, "loop expression required").for_()

		def parsedef(tag):
			return self._parser(tag, "definition required").definition()

		def parserender(tag):
			call = self._parser(tag, "render call required").expression()
			if not isinstance(call, Call):
				raise TypeError("render call required")
			tags = dict(render=Render, renderx=RenderX, renderblock=RenderBlock, renderblocks=RenderBlocks)
			render = tags[tag.tag](template=tag.template, startpos=tag.startpos, obj=call.obj)
			render.args = call.args
			if tag.tag == "renderblock":
				# We create the sub template without source so there won't be any compilation done ...
				render.content = Template(None, name="content", whitespace=self.whitespace, startdelim=self.startdelim, enddelim=self.enddelim)
				# ... but then we have to fix the ``fullsource`` and ``startpos`` attributes ourselves
				render.content._fullsource = self._fullsource
				# The stop position will be updated by :meth:`RenderBlock.finish`.
				render.content.startpos = slice(tag.startpos.stop, tag.startpos.stop)
			return render

		tags = self._tokenize(source, startdelim, enddelim)
		lines = list(self._tags2lines(tags))

		# Find template declarations and whitespace specification
		for line in lines:
			for tag in line:
				if isinstance(tag, Tag):
					if tag.tag == "ul4":
						(name, signature) = parsedeclaration(tag)
						self.name = name
						if signature is not None:
							signature = signature.eval(Context())
						self.signature = signature
					elif tag.tag == "whitespace":
						whitespace = tag.code
						if whitespace in {"keep", "strip", "smart"}:
							self.whitespace = whitespace
						else:
							try:
								raise ValueError(f"whitespace mode {whitespace!r} unknown")
							except Exception as exc:
								_decorateexception(exc, tag)
								raise

		# Flatten lines and update whitespace according to the whitespace mode specified
		if self.whitespace == "keep":
			tags = self._whitespace_keep(lines)
		elif self.whitespace == "strip":
			tags = self._whitespace_strip(lines)
		elif self.whitespace == "smart":
			tags = self._whitespace_smart(lines)
		else:
			raise ValueError(f"whitespace mode {self.whitespace!r} unknown")

		for tag in tags:
			# Update ``tag.template`` to reference the innermost template
			# (Originally it referenced the outermost one)
			tag.template = templatestack[-1]
			try:
				if isinstance(tag, Text):
					blockstack[-1].append(tag)
				elif tag.tag == "doc":
					# Only use the first ``<?doc?>`` tag in each template, ignore all later ones
					if templatestack[-1].docpos is None:
						templatestack[-1].docpos = tag.codepos
				elif tag.tag == "print":
					blockstack[-1].append(Print(templatestack[-1], tag.startpos, parseexpr(tag)))
				elif tag.tag == "printx":
					blockstack[-1].append(PrintX(templatestack[-1], tag.startpos, parseexpr(tag)))
				elif tag.tag == "code":
					blockstack[-1].append(parsestmt(tag))
				elif tag.tag == "if":
					block = CondBlock(templatestack[-1], tag.startpos, None, parseexpr(tag))
					blockstack[-1].append(block)
					blockstack.append(block)
				elif tag.tag == "elif":
					if not isinstance(blockstack[-1], CondBlock):
						raise BlockError("elif doesn't match and if")
					elif isinstance(blockstack[-1].content[-1], ElseBlock):
						raise BlockError("else already seen in if")
					blockstack[-1].newblock(ElIfBlock(templatestack[-1], tag.startpos, None, parseexpr(tag)))
				elif tag.tag == "else":
					if not isinstance(blockstack[-1], CondBlock):
						raise BlockError("else doesn't match any if")
					elif isinstance(blockstack[-1].content[-1], ElseBlock):
						raise BlockError("else already seen in if")
					blockstack[-1].newblock(ElseBlock(templatestack[-1], tag.startpos, None))
				elif tag.tag == "end":
					if len(blockstack) <= 1:
						raise BlockError("not in any block")
					code = tag.code
					if code:
						if code == "if":
							if not isinstance(blockstack[-1], CondBlock):
								raise BlockError("endif doesn't match any if")
						elif code == "for":
							if not isinstance(blockstack[-1], ForBlock):
								raise BlockError("endfor doesn't match any for")
						elif code == "while":
							if not isinstance(blockstack[-1], WhileBlock):
								raise BlockError("endwhile doesn't match any while")
						elif code == "def":
							if not isinstance(blockstack[-1], Template):
								raise BlockError("enddef doesn't match any def")
							templatestack.pop()
						elif code == "renderblock":
							if not isinstance(blockstack[-1], RenderBlock):
								raise BlockError("endrenderblock doesn't match any renderblock")
						elif code == "renderblocks":
							if not isinstance(blockstack[-1], RenderBlocks):
								raise BlockError("endrenderblocks doesn't match any renderblocks")
						else:
							raise BlockError(f"illegal end value {code!r}")
					last = blockstack.pop()
					last.finish(tag) # Set end position of block
				elif tag.tag == "for":
					block = parsefor(tag)
					blockstack[-1].append(block)
					blockstack.append(block)
				elif tag.tag == "while":
					block = WhileBlock(templatestack[-1], tag.startpos, None, parseexpr(tag))
					blockstack[-1].append(block)
					blockstack.append(block)
				elif tag.tag == "break":
					for block in reversed(blockstack):
						if isinstance(block, (ForBlock, WhileBlock)):
							break
						elif isinstance(block, Template):
							raise BlockError("break outside of for loop")
					blockstack[-1].append(Break(templatestack[-1], tag.startpos))
				elif tag.tag == "continue":
					for block in reversed(blockstack):
						if isinstance(block, (ForBlock, WhileBlock)):
							break
						elif isinstance(block, Template):
							raise BlockError("continue outside of for loop")
					blockstack[-1].append(Continue(templatestack[-1], tag.startpos))
				elif tag.tag == "def":
					(name, signature) = parsedef(tag)
					block = Template(None, name=name, whitespace=self.whitespace, startdelim=self.startdelim, enddelim=self.enddelim, signature=signature)
					block.template = block
					block.parenttemplate = templatestack[-1]
					tag.template = block
					templatestack.append(block)
					# The source is always the complete source of the top level template
					# (so that the offsets in all :class:`AST` objects are correct)
					block._fullsource = self._fullsource
					block.startpos = tag.startpos
					blockstack[-1].append(block)
					blockstack.append(block)
				elif tag.tag == "return":
					blockstack[-1].append(Return(templatestack[-1], tag.startpos, parseexpr(tag)))
				elif tag.tag in {"render", "renderx", "renderblock", "renderblocks"}:
					render = parserender(tag)
					# Find innermost block
					innerblock = blockstack[-1]
					if isinstance(innerblock, CondBlock):
						innerblock = innerblock.content[-1]
					innerblock = innerblock.content
					# If we have an indentation before the ``<?render?>`` tag, move it
					# into the ``indent`` attribute of the :class`Render` object,
					# because this indentation must be added to every line that the
					# rendered template outputs.
					if innerblock and isinstance(innerblock[-1], Indent):
						render.indent = innerblock[-1]
						innerblock.pop()
					blockstack[-1].append(render)
					if tag.tag in {"renderblock", "renderblocks"}:
						blockstack.append(render)
				elif tag.tag in ("ul4", "whitespace", "note", "doc"):
					# Don't copy declarations, whitespace specification, comments or docstrings over into the syntax tree
					pass
				else: # Can't happen
					raise ValueError(f"unknown tag {tag.tag!r}")
			except Exception as exc:
				_decorateexception(exc, tag)
				raise
		if len(blockstack) > 1:
			exc = BlockError("block unclosed")
			_decorateexception(exc, blockstack[-1])
			raise exc

	# @_handleexpressioneval
	def eval(self, context):
		signature = self.signature
		# If our signature is an AST, we have to evaluate it to get the final :class:`inspect.Signature` object
		if isinstance(signature, Signature):
			signature = signature.eval(context)
		context.vars[self.name] = TemplateClosure(self, context, signature)


@register("signature")
class Signature(Code):
	"""
	AST node for the signature of a template.

	The list of arguments is found in :obj:`params`.
	"""

	ul4attrs = Code.ul4attrs.union({"params"})

	def __init__(self, template=None, startpos=None):
		super().__init__(template, startpos)
		self.params = []

	def __repr__(self):
		params = "".join(f" {paramname}" if default is None else f" {paramname}={default!r}" for (paramname, default) in self.params)
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} {_offset(self.pos)}{params} at {id(self):#x}>"

	def _repr_pretty(self, p):
		for (paramname, default) in self.params:
			p.breakable()
			if default is None:
				p.text(paramname)
			else:
				p.text(f"{paramname}=")
				p.pretty(default)

	def _str(self):
		yield "("
		for (i, (paramname, default)) in enumerate(self.params):
			if i:
				yield ", "
			yield paramname
			if default is not None:
				yield "="
				yield from default._str()
		yield ")"

	@_handleexpressioneval
	def eval(self, context):
		params = []
		for (paramname, default) in self.params:
			if default is None:
				if paramname.startswith("**"):
					paramname = paramname[2:]
					kind = inspect.Parameter.VAR_KEYWORD
				elif paramname.startswith("*"):
					paramname = paramname[1:]
					kind = inspect.Parameter.VAR_POSITIONAL
				else:
					kind = inspect.Parameter.POSITIONAL_OR_KEYWORD
				default = inspect.Parameter.empty
			else:
				kind = inspect.Parameter.POSITIONAL_OR_KEYWORD
				default = default.eval(context)
			params.append(inspect.Parameter(paramname, kind, default=default))
		return inspect.Signature(params)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		dump = []
		for (paramname, default) in self.params:
			if default is None:
				dump.append(paramname)
			else:
				dump.append([paramname, default])
		encoder.dump(dump)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		dump = decoder.load()
		for param in dump:
			if isinstance(param, str):
				self.params.append((param, None))
			else:
				self.params.append(param)


###
### Functions
###

@Context.makefunction
def function_str(obj=""):
	return _str(obj)


@Context.makefunction
def function_repr(obj):
	return _repr(obj)


@Context.makefunction
def function_ascii(obj):
	return _ascii(obj)


@Context.makefunction
def function_now():
	return datetime.datetime.now()


@Context.makefunction
def function_today():
	return datetime.date.today()


Context.makefunction(datetime.datetime.utcnow)


@Context.makefunction
def function_date(year, month, day):
	return datetime.date(year, month, day)


@Context.makefunction
def function_datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0):
	return datetime.datetime(year, month, day, hour, minute, second, microsecond)


@Context.makefunction
def function_timedelta(days=0, seconds=0, microseconds=0):
	return datetime.timedelta(days, seconds, microseconds)


@Context.makefunction
def function_monthdelta(months=0):
	return misc.monthdelta(months)


Context.makefunction(random.random)


@Context.makefunction
def function_xmlescape(obj):
	return _xmlescape(obj)


@Context.makefunction
def function_csv(obj):
	if obj is None:
		return ""
	elif isinstance(obj, Undefined):
		return ""
	elif not isinstance(obj, str):
		obj = _repr(obj)
	if any(c in obj for c in ',"\n'):
		text = obj.replace('"', '""')
		return f'"{text}"'
	return obj


@Context.makefunction
def function_asjson(obj):
	return _asjson(obj)


@Context.makefunction
def function_fromjson(string):
	return json.loads(string)


@Context.makefunction
def function_asul4on(obj):
	from ll import ul4on
	return ul4on.dumps(obj)


@Context.makefunction
def function_fromul4on(string):
	from ll import ul4on
	return ul4on.loads(string)


@Context.makefunction
def function_int(obj=0, base=None):
	if base is None:
		return int(obj)
	else:
		return int(obj, base)


@Context.makefunction
def function_float(obj=0.0):
	return float(obj)


@Context.makefunction
def function_bool(obj=False):
	return bool(obj)


@Context.makefunction
def function_list(iterable=()):
	return list(iterable)


@Context.makefunction
def function_set(iterable=()):
	return set(iterable)


@Context.makefunction
def function_len(sequence):
	return len(sequence)


@Context.makefunction
def function_abs(number):
	return abs(number)


@Context.makefunction
def function_any(iterable):
	return any(iterable)


@Context.makefunction
def function_all(iterable):
	return all(iterable)


Context.makefunction(enumerate)


@Context.makefunction
def function_enumfl(iterable, start=0):
	lastitem = None
	first = True
	i = start
	it = iter(iterable)
	try:
		item = next(it)
	except StopIteration:
		return
	while True:
		try:
			(lastitem, item) = (item, next(it))
		except StopIteration:
			yield (i, first, True, item) # Items haven't been swapped yet
			return
		else:
			yield (i, first, False, lastitem)
			first = False
		i += 1


@Context.makefunction
def function_isfirst(iterable):
	return misc.isfirst(iterable)


@Context.makefunction
def function_islast(iterable):
	return misc.islast(iterable)


@Context.makefunction
def function_isfirstlast(iterable):
	return misc.isfirstlast(iterable)


@Context.makefunction
def function_isundefined(obj):
	return isinstance(obj, Undefined)


@Context.makefunction
def function_isdefined(obj):
	return not isinstance(obj, Undefined)


@Context.makefunction
def function_isnone(obj):
	return obj is None


@Context.makefunction
def function_isstr(obj):
	return isinstance(obj, str)


@Context.makefunction
def function_isint(obj):
	return isinstance(obj, int) and not isinstance(obj, bool)


@Context.makefunction
def function_isfloat(obj):
	return isinstance(obj, float)


@Context.makefunction
def function_isbool(obj):
	return isinstance(obj, bool)


@Context.makefunction
def function_isdate(obj):
	return isinstance(obj, datetime.date) and not isinstance(obj, datetime.datetime)


@Context.makefunction
def function_isdatetime(obj):
	return isinstance(obj, datetime.datetime)


@Context.makefunction
def function_istimedelta(obj):
	return isinstance(obj, datetime.timedelta)


@Context.makefunction
def function_ismonthdelta(obj):
	return isinstance(obj, misc.monthdelta)


@Context.makefunction
def function_isexception(obj):
	return isinstance(obj, BaseException)


@Context.makefunction
def function_islist(obj):
	from ll import color
	return isinstance(obj, abc.Sequence) and not isinstance(obj, str) and not isinstance(obj, color.Color)


@Context.makefunction
def function_isset(obj):
	return isinstance(obj, (set, frozenset))


@Context.makefunction
def function_isdict(obj):
	return isinstance(obj, abc.Mapping) and not isinstance(obj, Template)


@Context.makefunction
def function_iscolor(obj):
	from ll import color
	return isinstance(obj, color.Color)


@Context.makefunction
def function_istemplate(obj):
	return isinstance(obj, (Template, TemplateClosure))


@Context.makefunction
def function_isfunction(obj):
	return (callable(obj) and not isinstance(obj, Undefined)) or callable(getattr(obj, "ul4call", None))


@Context.makefunction
def function_chr(i):
	return chr(i)


@Context.makefunction
def function_ord(c):
	return ord(c)


@Context.makefunction
def function_hex(number):
	return hex(number)


@Context.makefunction
def function_oct(number):
	return oct(number)


@Context.makefunction
def function_bin(number):
	return bin(number)


@Context.makefunction
def function_min(*args):
	return min(*args)


@Context.makefunction
def function_max(*args):
	return max(*args)


@Context.makefunction
def function_first(iterable, default=None):
	return misc.first(iterable, default)


@Context.makefunction
def function_last(iterable, default=None):
	return misc.last(iterable, default)


@Context.makefunction
def function_sum(iterable, start=0):
	return sum(iterable, start)


@Context.makefunction
@withcontext
def function_sorted(context, iterable, key=None, reverse=False):
	if key is not None:
		if callable(getattr(key, "ul4call", None)):
			key = key.ul4call
		elif callable(key):
			key = key.__call__
		if getattr(key, "ul4context", False):
			key = functools.partial(key, context)
	return sorted(iterable, key=key, reverse=reverse)


@Context.makefunction
def function_range(*args):
	return range(*args)


@Context.makefunction
def function_slice(*args):
	return itertools.islice(*args)


@Context.makefunction
def function_type(obj):
	from ll import color
	if obj is None:
		return "none"
	elif isinstance(obj, Undefined):
		return "undefined"
	elif isinstance(obj, abc.Mapping):
		return "dict"
	elif isinstance(obj, datetime.datetime):
		return "datetime"
	elif isinstance(obj, datetime.date):
		return "date"
	elif isinstance(obj, datetime.timedelta):
		return "timedelta"
	elif isinstance(obj, misc.monthdelta):
		return "monthdelta"
	elif isinstance(obj, abc.Sequence) and not isinstance(obj, (str, color.Color)):
		return "list"
	elif callable(obj) and not isinstance(obj, (Template, TemplateClosure)):
		return "function"
	else:
		return misc.format_class(obj)


@Context.makefunction
def function_reversed(sequence):
	return reversed(sequence)


@Context.makefunction
def function_randrange(*args):
	return random.randrange(*args)


@Context.makefunction
def function_randchoice(sequence):
	return random.choice(sequence)


@Context.makefunction
def function_format(obj, fmt, lang=None):
	if isinstance(obj, (datetime.date, datetime.time, datetime.timedelta)):
		if lang is None:
			lang = "en"
		oldlocale = locale.getlocale()
		try:
			for candidate in (locale.normalize(lang), locale.normalize("en"), ""):
				try:
					locale.setlocale(locale.LC_ALL, candidate)
					return format(obj, fmt)
				except locale.Error:
					if not candidate:
						return format(obj, fmt)
		finally:
			try:
				locale.setlocale(locale.LC_ALL, oldlocale)
			except locale.Error:
				pass
	else:
		return format(obj, fmt)


@Context.makefunction
def function_zip(*iterables):
	return zip(*iterables)


@Context.makefunction
def function_urlquote(string):
	return urlparse.quote_plus(string)


@Context.makefunction
def function_urlunquote(string):
	return urlparse.unquote_plus(string)


@Context.makefunction
def function_rgb(r, g, b, a=1.0):
	from ll import color
	return color.Color.fromrgb(r, g, b, a)


@Context.makefunction
def function_hls(h, l, s, a=1.0):
	from ll import color
	return color.Color.fromhls(h, l, s, a)


@Context.makefunction
def function_hsv(h, s, v, a=1.0):
	from ll import color
	return color.Color.fromhsv(h, s, v, a)


@Context.makefunction
def function_md5(string):
	import hashlib
	return hashlib.md5(string.encode("utf-8")).hexdigest()


@Context.makefunction
def function_round(x, digits=0):
	result = round(x, digits)
	if digits <= 0:
		result = int(result)
	return result


@Context.makefunction
def function_floor(x, digits=0):
	if digits:
		threshold = 10**digits
		result = math.floor(x*threshold)/threshold
		if digits < 0:
			return int(result)
		return result
	else:
		return math.floor(x)


@Context.makefunction
def function_ceil(x, digits=0):
	if digits:
		threshold = 10**digits
		result = math.ceil(x*threshold)/threshold
		if digits < 0:
			return int(result)
		return result
	else:
		return math.ceil(x)


Context.functions["pi"] = math.pi
Context.functions["tau"] = 2*math.pi


@Context.makefunction
def function_sqrt(x):
	return math.sqrt(x)


@Context.makefunction
def function_cos(x):
	return math.cos(x)


@Context.makefunction
def function_sin(x):
	return math.sin(x)


@Context.makefunction
def function_tan(x):
	return math.tan(x)


@Context.makefunction
def function_exp(x):
	return math.exp(x)


@Context.makefunction
def function_log(x, base=None):
	if base is None:
		return math.log(x)
	else:
		return math.log(x, base)


@Context.makefunction
def function_pow(x, y):
	return math.pow(x, y)


@Context.makefunction
def function_getattr(obj, attrname, default=None):
	return proto(obj).getattr(obj, attrname, default)


@Context.makefunction
def function_setattr(obj, attrname, value):
	return proto(obj).setattr(obj, attrname, value)


@Context.makefunction
def function_hasattr(obj, attrname):
	return proto(obj).hasattr(obj, attrname)


@Context.makefunction
def function_dir(obj):
	return proto(obj).dir(obj)


class TemplateClosure(Block):
	ul4attrs = Template.ul4attrs

	def __init__(self, template, context, signature):
		self.template = template
		self.vars = context.vars
		self.signature = signature

	@withcontext
	def ul4render(*args, **kwargs):
		self = args[0]
		context = args[1]
		args = args[2:]
		vars = _makevars(self.signature, args, kwargs)
		vars = collections.ChainMap(vars, self.vars)
		with context.replacevars(vars):
			# Call :meth:`_renderbound` to bypass binding the arguments again
			# (which wouldn't work anyway as ``self.template.signature`` is an :class:`AST` object)
			yield from self.template._renderbound(context)

	@withcontext
	def ul4renders(*args, **kwargs): # This will be exposed to UL4 as ``renders``
		self = args[0]
		context = args[1]
		args = args[2:]
		vars = _makevars(self.signature, args, kwargs)
		vars = collections.ChainMap(vars, self.vars)
		with context.replacevars(vars):
			# Call :meth:`_renderbound` to bypass binding the arguments again
			# (which wouldn't work anyway as ``self.template.signature`` is an :class:`AST` object)
			return self.template._rendersbound(context)

	@withcontext
	def ul4call(*args, **kwargs):
		self = args[0]
		context = args[1]
		args = args[2:]
		vars = _makevars(self.signature, args, kwargs)
		vars = collections.ChainMap(vars, self.vars)
		with context.replacevars(vars):
			# Call :meth:`_renderbound` to bypass binding the arguments again
			# (which wouldn't work anyway as ``self.template.signature`` is an :class:`AST` object)
			return self.template._callbound(context)

	def __getattr__(self, name):
		if name == "renders":
			return self.ul4renders
		else:
			return getattr(self.template, name)

	def ul4getattr(self, name):
		if name == "renders":
			return self.ul4renders
		else:
			return getattr(self, name)

	def _repr(self):
		yield f"name={self.name!r}"
		yield f"whitespace={self.whitespace!r}"
		if self.startdelim != "<?":
			yield f"startdelim={self.startdelim!r}"
		if self.enddelim != "?>":
			yield f"enddelim={self.enddelim!r}"
		if self.signature is not None:
			yield f"signature={self.signature}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("name=")
		p.pretty(self.name)
		p.breakable()
		p.text("whitespace=")
		p.pretty(self.whitespace)
		if self.startdelim != "<?":
			p.breakable()
			p.text("startdelim=")
			p.pretty(self.startdelim)
		if self.enddelim != "?>":
			p.breakable()
			p.text("enddelim=")
			p.pretty(self.enddelim)
		if self.signature is not None:
			p.breakable()
			p.text(f"signature={self.signature}")
		for node in self.content:
			p.breakable()
			p.pretty(node)
