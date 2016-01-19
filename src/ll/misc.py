# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2004-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2004-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`ll.misc` contains various utility functions and classes used by the other
LivingLogic modules and packages.
"""


import sys, os, types, datetime, collections, io, gzip as gzip_, argparse, functools, signal, contextlib, subprocess

from ll import ul4c, color


__docformat__ = "reStructuredText"


# get the current directory as early as possible to minimize the chance that someone has called ``os.chdir()``
_curdir = os.getcwd()


notifycmd = os.environ.get("LL_MISC_NOTIFY", "/usr/local/bin/terminal-notifier")


# Try to fetch ``xmlescape`` from C implementation
try:
	from ll._misc import *
except ImportError:
	def xmlescape(string):
		"""
		Return a copy of the argument string, where every occurrence of ``<``,
		``>``, ``&``, ``\"``, ``'`` and every restricted character has been
		replaced with their XML character entity or character reference.
		"""
		if isinstance(string, str):
			return string.translate({0x00: '&#0;', 0x01: '&#1;', 0x02: '&#2;', 0x03: '&#3;', 0x04: '&#4;', 0x05: '&#5;', 0x06: '&#6;', 0x07: '&#7;', 0x08: '&#8;', 0x0b: '&#11;', 0x0c: '&#12;', 0x0e: '&#14;', 0x0f: '&#15;', 0x10: '&#16;', 0x11: '&#17;', 0x12: '&#18;', 0x13: '&#19;', 0x14: '&#20;', 0x15: '&#21;', 0x16: '&#22;', 0x17: '&#23;', 0x18: '&#24;', 0x19: '&#25;', 0x1a: '&#26;', 0x1b: '&#27;', 0x1c: '&#28;', 0x1d: '&#29;', 0x1e: '&#30;', 0x1f: '&#31;', 0x22: '&quot;', 0x26: '&amp;', 0x27: '&#39;', 0x3c: '&lt;', 0x3e: '&gt;', 0x7f: '&#127;', 0x80: '&#128;', 0x81: '&#129;', 0x82: '&#130;', 0x83: '&#131;', 0x84: '&#132;', 0x86: '&#134;', 0x87: '&#135;', 0x88: '&#136;', 0x89: '&#137;', 0x8a: '&#138;', 0x8b: '&#139;', 0x8c: '&#140;', 0x8d: '&#141;', 0x8e: '&#142;', 0x8f: '&#143;', 0x90: '&#144;', 0x91: '&#145;', 0x92: '&#146;', 0x93: '&#147;', 0x94: '&#148;', 0x95: '&#149;', 0x96: '&#150;', 0x97: '&#151;', 0x98: '&#152;', 0x99: '&#153;', 0x9a: '&#154;', 0x9b: '&#155;', 0x9c: '&#156;', 0x9d: '&#157;', 0x9e: '&#158;', 0x9f: '&#159;'})
		else:
			string = string.replace("&", "&amp;")
			string = string.replace("<", "&lt;")
			string = string.replace(">", "&gt;")
			string = string.replace("'", "&#39;")
			string = string.replace('"', "&quot;")
			for c in "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1f\x7f\x80\x81\x82\x83\x84\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f":
				string = string.replace(c, "&#{};".format(ord(c)))
			return string

	def xmlescape_text(string):
		"""
		Return a copy of the argument string, where every occurrence of ``<``,
		``>``, ``&``, and every restricted character has been replaced with their
		XML character entity or character reference.
		"""
		if isinstance(string, str):
			return string.translate({0x00: '&#0;', 0x01: '&#1;', 0x02: '&#2;', 0x03: '&#3;', 0x04: '&#4;', 0x05: '&#5;', 0x06: '&#6;', 0x07: '&#7;', 0x08: '&#8;', 0x0b: '&#11;', 0x0c: '&#12;', 0x0e: '&#14;', 0x0f: '&#15;', 0x10: '&#16;', 0x11: '&#17;', 0x12: '&#18;', 0x13: '&#19;', 0x14: '&#20;', 0x15: '&#21;', 0x16: '&#22;', 0x17: '&#23;', 0x18: '&#24;', 0x19: '&#25;', 0x1a: '&#26;', 0x1b: '&#27;', 0x1c: '&#28;', 0x1d: '&#29;', 0x1e: '&#30;', 0x1f: '&#31;', 0x26: '&amp;', 0x3c: '&lt;', 0x3e: '&gt;', 0x7f: '&#127;', 0x80: '&#128;', 0x81: '&#129;', 0x82: '&#130;', 0x83: '&#131;', 0x84: '&#132;', 0x86: '&#134;', 0x87: '&#135;', 0x88: '&#136;', 0x89: '&#137;', 0x8a: '&#138;', 0x8b: '&#139;', 0x8c: '&#140;', 0x8d: '&#141;', 0x8e: '&#142;', 0x8f: '&#143;', 0x90: '&#144;', 0x91: '&#145;', 0x92: '&#146;', 0x93: '&#147;', 0x94: '&#148;', 0x95: '&#149;', 0x96: '&#150;', 0x97: '&#151;', 0x98: '&#152;', 0x99: '&#153;', 0x9a: '&#154;', 0x9b: '&#155;', 0x9c: '&#156;', 0x9d: '&#157;', 0x9e: '&#158;', 0x9f: '&#159;'})
		else:
			string = string.replace("&", "&amp;")
			string = string.replace("<", "&lt;")
			string = string.replace(">", "&gt;")
			for c in "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1f\x7f\x80\x81\x82\x83\x84\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f":
				string = string.replace(c, "&#{};".format(ord(c)))
			return string

	def xmlescape_attr(string):
		"""
		Return a copy of the argument string, where every occurrence of ``<``,
		``>``, ``&``, ``"`` and every restricted character has been replaced with
		their XML character entity or character reference.
		"""
		if isinstance(string, str):
			return string.translate({0x00: '&#0;', 0x01: '&#1;', 0x02: '&#2;', 0x03: '&#3;', 0x04: '&#4;', 0x05: '&#5;', 0x06: '&#6;', 0x07: '&#7;', 0x08: '&#8;', 0x0b: '&#11;', 0x0c: '&#12;', 0x0e: '&#14;', 0x0f: '&#15;', 0x10: '&#16;', 0x11: '&#17;', 0x12: '&#18;', 0x13: '&#19;', 0x14: '&#20;', 0x15: '&#21;', 0x16: '&#22;', 0x17: '&#23;', 0x18: '&#24;', 0x19: '&#25;', 0x1a: '&#26;', 0x1b: '&#27;', 0x1c: '&#28;', 0x1d: '&#29;', 0x1e: '&#30;', 0x1f: '&#31;', 0x22: '&quot;', 0x26: '&amp;', 0x3c: '&lt;', 0x3e: '&gt;', 0x7f: '&#127;', 0x80: '&#128;', 0x81: '&#129;', 0x82: '&#130;', 0x83: '&#131;', 0x84: '&#132;', 0x86: '&#134;', 0x87: '&#135;', 0x88: '&#136;', 0x89: '&#137;', 0x8a: '&#138;', 0x8b: '&#139;', 0x8c: '&#140;', 0x8d: '&#141;', 0x8e: '&#142;', 0x8f: '&#143;', 0x90: '&#144;', 0x91: '&#145;', 0x92: '&#146;', 0x93: '&#147;', 0x94: '&#148;', 0x95: '&#149;', 0x96: '&#150;', 0x97: '&#151;', 0x98: '&#152;', 0x99: '&#153;', 0x9a: '&#154;', 0x9b: '&#155;', 0x9c: '&#156;', 0x9d: '&#157;', 0x9e: '&#158;', 0x9f: '&#159;'})
		else:
			string = string.replace("&", "&amp;")
			string = string.replace("<", "&lt;")
			string = string.replace(">", "&gt;")
			string = string.replace('"', "&quot;")
			for c in "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1f\x7f\x80\x81\x82\x83\x84\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f":
				string = string.replace(c, "&#{};".format(ord(c)))
			return string


def item(iterable, index, default=None):
	"""
	Returns the :obj:`index`'th item from the iterable. :obj:`index` may be
	negative to count from the end. E.g. 0 returns the first item produced by
	the iterator, 1 the second, -1 the last one etc. If :obj:`index` is negative
	the iterator will be completely exhausted, if it's positive it will be
	exhausted up to the :obj:`index`'th item. If the iterator doesn't produce
	that many items :obj:`default` will be returned.

	:obj:`index` may also be an iterable of indexes, in which case :meth:`item`
	will be applied recursively, i.e. ``item(["foo", "bar"], (1, -1))`` returns
	``'r'``.
	"""
	if isinstance(index, int):
		index = (index,)
	for i in index:
		if i >= 0:
			for item in iterable:
				if not i:
					iterable = item
					break
				i -= 1
			else:
				return default
		else:
			i = -i
			cache = collections.deque()
			for item in iterable:
				cache.append(item)
				if len(cache) > i:
					cache.popleft()
			if len(cache) == i:
				iterable = cache.popleft()
			else:
				return default
	return iterable


def first(iterable, default=None):
	"""
	Return the first item from the iterable. If the iterator doesn't
	produce any items :obj:`default` will be returned.
	"""
	for item in iterable:
		return item
	return default


def last(iterable, default=None):
	"""
	Return the last item from the iterable. If the iterator doesn't produce any
	items :obj:`default` will be returned.
	"""
	item = default
	for item in iterable:
		pass
	return item


def count(iterable):
	"""
	Count the number of items produced by the iterable. Calling this function
	will exhaust the iterator.
	"""
	count = 0
	for node in iterable:
		count += 1
	return count


def notimplemented(function):
	"""
	A decorator that raises :exc:`NotImplementedError` when the method is called.
	This saves you the trouble of formatting the error message yourself for each
	implementation.
	"""
	@functools.wraps(function)
	def wrapper(self, *args, **kwargs):
		raise NotImplementedError("method {}() not implemented in {!r}".format(function.__name__, self.__class__))
	return wrapper


def withdoc(doc):
	"""
	A decorator that adds a docstring to the function it decorates. This can be
	useful if the docstring is not static, and adding it afterwards is not
	possible.
	"""
	def wrapper(function):
		function.__doc__ = doc
		return function
	return wrapper


class _propclass_Meta(type):
	def __new__(cls, name, bases, dict):
		if bases == (property,):
			# create propclass itself normally
			return super(_propclass_Meta, cls).__new__(cls, name, bases, dict)
		newdict = dict.copy()
		newdict.pop("__get__", None)
		newdict.pop("__set__", None)
		newdict.pop("__delete__", None)
		newdict.pop("__metaclass__", None)
		self = type.__new__(cls, name, bases, newdict)
		inst = self(
			dict.get("__get__", None),
			dict.get("__set__", None),
			dict.get("__delete__", None),
			dict.get("__doc__", None)
		)
		inst.__name__ = name
		return inst


class propclass(property, metaclass=_propclass_Meta):
	'''
	:class:`propclass` provides an alternate way to define properties.

	Subclassing :class:`propclass` and defining methods :meth:`__get__`,
	:meth:`__set__` and :meth:`__delete__` will automatically generate the
	appropriate property::

		class name(misc.propclass):
			"""
			The name property
			"""
			def __get__(self):
				return self._name
			def __set__(self, name):
				self._name = name.lower()
			def __delete__(self):
				self._name = None
	'''


def format_class(obj):
	"""
	Format the name of the class of obj:`obj`::

		>>> misc.format_class(42)
		'int'
		>>> misc.format_class(open('README.rst', 'rb'))
		'_io.BufferedReader'
	"""
	if obj.__class__.__module__ not in ("builtins", "exceptions"):
		fmt = "{0.__class__.__module__}.{0.__class__.__qualname__}"
	else:
		fmt = "{0.__class__.__qualname__}"
	return fmt.format(obj)


def format_exception(exc):
	"""
	Format an exception object::

		>>> misc.format_exception(ValueError("bad value"))
		'ValueError: bad value'
	"""
	try:
		strexc = str(exc).strip()
	except UnicodeError:
		strexc = "?"
	fmt = "{}"
	if strexc:
		fmt += ": {}"
	return fmt.format(format_class(exc), strexc)


def exception_chain(exc):
	"""
	Traverses the chain of exceptions. This is a generator.
	"""
	while True:
		yield exc
		if exc.__cause__ is not None:
			exc = exc.__cause__
		elif exc.__context__ is not None and not exc.__suppress_context__:
			exc = exc.__context__
		else:
			break


class Pool:
	"""
	A :class:`Pool` object can be used as an inheritable alternative to modules.
	The attributes of a module can be put into a pool and each pool can have
	base pools where lookup continues if an attribute can't be found.
	"""
	def __init__(self, *objects):
		self._attrs = {}
		self.bases = []
		for object in objects:
			self.register(object)

	def register(self, object):
		"""
		Register :obj:`object` in the pool. :obj:`object` can be a module, a
		dictionary or a :class:`Pool` objects (with registers the pool as a base
		pool). If :obj:`object` is a module and has an attribute :attr:`__bases__`
		(being a sequence of other modules) this attribute will be used to
		initialize :obj:`self`\s base pool.
		"""
		if isinstance(object, types.ModuleType):
			self.register(object.__dict__)
		elif isinstance(object, dict):
			for (key, value) in object.items():
				if key == "__bases__":
					for base in value:
						if not isinstance(base, Pool):
							base = self.__class__(base)
						self.bases.append(base)
				elif not isinstance(value, (types.ModuleType, dict)):
					try:
						self._attrs[key] = value
					except TypeError:
						pass
		elif isinstance(object, Pool):
			self.bases.append(object)
		elif isinstance(object, type):
			self._attrs[object.__name__] = object

	def __getitem__(self, key):
		try:
			return self._attrs[key]
		except KeyError:
			for base in self.bases:
				return base[key]
			raise

	def __getattr__(self, key):
		try:
			return self.__getitem__(key)
		except KeyError:
			raise AttributeError(key)

	def clear(self):
		"""
		Make :obj:`self` empty.
		"""
		self._attrs.clear()
		del self.bases[:]

	def clone(self):
		"""
		Return a copy of :obj:`self`.
		"""
		copy = self.__class__()
		copy._attrs = self._attrs.copy()
		copy.bases = self.bases[:]
		return copy

	def __repr__(self):
		return "<{}.{} object with {} items at {:#x}>".format(self.__class__.__module__, self.__class__.__qualname__, len(self._attrs), id(self))


def iterone(item):
	"""
	Return an iterator that will produce one item: :obj:`item`.
	"""
	yield item


class Iterator:
	"""
	:class:`Iterator` adds :meth:`__getitem__` support to an iterator. This is
	done by calling :func:`item` internally.
	"""
	__slots__ = ("iterator", )

	def __init__(self, iterator):
		self.iterator = iterator

	def __getitem__(self, index):
		if isinstance(index, slice):
			return list(self.iterator)[index]
		default = object()
		result = item(self, index, default)
		if result is default:
			raise IndexError(index)
		return result

	def __iter__(self):
		return self

	def __next__(self):
		return next(self.iterator)

	# We can't implement :meth:`__len__`, because if such an object is passed to
	# :class:`list`, :meth:`__len__` would be called, exhausting the iterator

	def __bool__(self):
		for node in self:
			return True
		return False

	def get(self, index, default=None):
		r"""
		Return the :obj:`index`'th item from the iterator (or :obj:`default` if
		there's no such item).
		"""
		return item(self, index, default)


class Queue:
	"""
	:class:`Queue` provides FIFO queues: The method :meth:`write` writes to the
	queue and the method :meth:`read` read from the other end of the queue and
	remove the characters read.
	"""
	def __init__(self):
		self._buffer = ""

	def write(self, chars):
		"""
		Write the string :obj:`chars` to the buffer.
		"""
		self._buffer += chars

	def read(self, size=-1):
		"""
		Read up to :obj:`size` character from the buffer (or all if :obj:`size`
		is negative). Those characters will be removed from the buffer.
		"""
		if size < 0:
			s = self._buffer
			self._buffer = ""
			return s
		else:
			s = self._buffer[:size]
			self._buffer = self._buffer[size:]
			return s


class Const:
	"""
	This class can be used for singleton constants.
	"""
	__slots__ = ("_name", "_module")

	def __init__(self, name, module=None):
		self._name = name
		self._module = module

	def __repr__(self):
		return "{}.{}".format(self._module or self.__module__, self._name)


class FlagAction(argparse.Action):
	"""
	:class:`FlagAction` can be use with :mod:`argparse` for options that
	represent flags. An options can have a value like ``yes`` or ``no`` for the
	correspending boolean value, or if the value is omitted it is the inverted
	default value (i.e. specifying the option toggles it).
	"""
	true_choices = ("1", "true", "yes", "on")
	false_choices = ("0", "false", "no", "off")

	def __init__(self, option_strings, dest, default=False, help=None):
		super().__init__(option_strings=option_strings, dest=dest, default="yes" if default else "no", help=help, metavar="yes|no", const="no" if default else "yes", type=self.str2bool, nargs="?")

	# implementing this prevents :meth:`__repr__` from generating an infinite recursion
	def _get_kwargs(self):
		return [(key, getattr(self, key)) for key in ("option_strings", "dest", "default", "help")]

	def str2bool(self, value):
		value = value.lower()
		if value in self.true_choices:
			return True
		elif value in self.false_choices:
			return False
		else:
			raise argparse.ArgumentTypeError("invalid flag value: {!r} (use any of {})".format(value, ", ".join(self.true_choices + self.false_choices)))

	def __call__(self, parser, namespace, values, option_string=None):
		setattr(namespace, self.dest, values)


def tokenizepi(string):
	"""
	Tokenize the string object :obj:`string` according to the processing
	instructions in the string. :func:`tokenize` will generate tuples with the
	first item being the processing instruction target and the second being the
	PI data. "Text" content (i.e. anything other than PIs) will be returned as
	``(None, data)``.
	"""

	pos = 0
	while True:
		pos1 = string.find("<?", pos)
		if pos1 < 0:
			part = string[pos:]
			if part:
				yield (None, part)
			return
		pos2 = string.find("?>", pos1)
		if pos2 < 0:
			part = string[pos:]
			if part:
				yield (None, part)
			return
		part = string[pos:pos1]
		if part:
			yield (None, part)
		part = string[pos1+2: pos2].strip()
		parts = part.split(None, 1)
		target = parts[0]
		if len(parts) > 1:
			data = parts[1]
		else:
			data = ""
		yield (target, data)
		pos = pos2+2


def itersplitat(string, positions):
	"""
	Split :obj:`string` at the positions specified in :obj:`positions`.

	For example::

		>>> from ll import misc
		>>> import datetime
		>>> datetime.datetime(*map(int, misc.itersplitat("20090609172345", (4, 6, 8, 10, 12))))
		datetime.datetime(2009, 6, 9, 17, 23, 45)

	This is a generator.
	"""
	curpos = 0
	for pos in positions:
		part = string[curpos:pos]
		if part:
			yield part
		curpos = pos
	part = string[curpos:]
	if part:
		yield part


def module(source, filename="unnamed.py", name=None):
	"""
	Create a module from the Python source code :obj:`source`. :obj:`filename`
	will be used as the filename for the module and :obj:`name` as the module
	name (defaulting to the filename part of :obj:`filename`).
	"""
	if name is None:
		name = os.path.splitext(os.path.basename(filename))[0]
	mod = types.ModuleType(name)
	mod.__file__ = filename
	code = compile(source, filename, "exec")
	exec(code, mod.__dict__)
	return mod


def javaexpr(obj):
	"""
	Return a Java expression for the object :obj:`obj`.
	"""

	if obj is None:
		return "null"
	elif obj is True:
		return "true"
	elif obj is False:
		return "false"
	elif isinstance(obj, str):
		if len(obj) > 10000: # Otherwise javac complains about ``constant string too long`` (the upper limit is 65535 UTF-8 bytes)
			return "new StringBuilder({}){}.toString()".format(len(obj), "".join(".append({})".format(javaexpr(obj[i:i+10000])) for i in range(0, len(obj), 10000)))
		else:
			v = []
			specialchars = {"\r": "\\r", "\n": "\\n", "\t": "\\t", "\f": "\\f", "\b": "\\b", '"': '\\"', "\\": "\\\\"}
			for c in obj:
				try:
					v.append(specialchars[c])
				except KeyError:
					oc = ord(c)
					v.append(c if 32 <= oc < 128 else "\\u{:04x}".format(oc))
			return '"{}"'.format("".join(v))
	elif isinstance(obj, datetime.datetime): # check ``datetime`` before ``date``, as ``datetime`` is a subclass of ``date``
		return "com.livinglogic.ul4.FunctionDate.call({0.year}, {0.month}, {0.day}, {0.hour}, {0.minute}, {0.second}, {0.microsecond})".format(obj)
	elif isinstance(obj, datetime.date):
		return "com.livinglogic.ul4.FunctionDate.call({0.year}, {0.month}, {0.day})".format(obj)
	elif isinstance(obj, datetime.timedelta):
		return "com.livinglogic.ul4.FunctionTimeDelta.call({0.days}, {0.seconds}, {0.microseconds})".format(obj)
	elif isinstance(obj, monthdelta):
		return "com.livinglogic.ul4.FunctionMonthDelta.call({0})".format(obj.months())
	elif isinstance(obj, color.Color):
		return "new com.livinglogic.ul4.Color({}, {}, {}, {})".format(*obj)
	elif isinstance(obj, float):
		return repr(obj)
	elif isinstance(obj, int):
		if -0x80000000 <= obj <= 0x7fffffff:
			return repr(obj)
		elif -0x8000000000000000 <= obj <= 0x7fffffffffffffff:
			return repr(obj) + "L"
		else:
			return 'new java.math.BigInteger("{}")'.format(obj)
		return repr(obj)
	elif isinstance(obj, collections.Sequence):
		return "java.util.Arrays.asList({})".format(", ".join(javaexpr(item) for item in obj))
	elif isinstance(obj, collections.Mapping):
		return "com.livinglogic.utils.MapUtils.makeMap({})".format(", ".join("{}, {}".format(javaexpr(key), javaexpr(value)) for (key, value) in obj.items()))
	elif isinstance(obj, collections.Set):
		return "com.livinglogic.utils.SetUtils.makeSet({})".format(", ".join(javaexpr(item) for item in obj))
	elif isinstance(obj, ul4c.UndefinedKey):
		return "new com.livinglogic.ul4.UndefinedKey({})".format(javaexpr(obj._key))
	elif isinstance(obj, ul4c.UndefinedVariable):
		return "new com.livinglogic.ul4.UndefinedVariable({})".format(javaexpr(obj._name))
	elif isinstance(obj, ul4c.UndefinedIndex):
		return "new com.livinglogic.ul4.UndefinedIndex({})".format(javaexpr(obj._index))
	elif isinstance(obj, ul4c.Template):
		return obj.javasource()
	else:
		raise TypeError("can't handle object of type {}".format(type(obj)))


class SysInfo:
	"""
	A :class:`SysInfo` object contains information about the host, user, python
	version and script. Available attributes are ``host_name``, ``host_fqdn``,
	``host_ip``, ``host_sysname``, ``host_nodename``, ``host_release``,
	``host_version``, ``host_machine``, ``user_name``, ``user_uid``, ``user_gid``,
	``user_gecos``, ``user_dir``, ``user_shell``, ``python_executable``,
	``python_version``, ``pid``, ``script_name``, ``short_script_name`` and
	``script_url``.

	:class:`SysInfo` object also support a mimimal dictionary interface (i.e.
	:meth:`__getitem__` and :meth:`__iter__`).

	One module global instance named :obj:`sysinfo` is created at module import
	time.
	"""

	_keys = {"host_name", "host_fqdn", "host_ip", "host_sysname", "host_nodename", "host_release", "host_version", "host_machine", "user_name", "user_uid", "user_gid", "user_gecos", "user_dir", "user_shell", "python_executable", "python_version", "pid", "script_name", "short_script_name", "script_url"}

	def __init__(self):
		# Use ``object`` as a marker for "not initialized"
		self._host_name = object
		self._host_fqdn = object
		self._host_ip = object
		self._host_sysname = object
		self._host_nodename = object
		self._host_release = object
		self._host_version = object
		self._host_machine = object
		self._user_name = object
		self._user_uid = object
		self._user_gid = object
		self._user_gecos = object
		self._user_dir = object
		self._user_shell = object
		self._pid = object
		self._script_name = object
		self._short_script_name = object
		self._script_url = object

	@property
	def host_name(self):
		if self._host_name is object:
			import socket
			self._host_name = socket.gethostname()
		return self._host_name

	@property
	def host_fqdn(self):
		return self.host_name

	@property
	def host_ip(self):
		if self._host_ip is object:
			import socket
			self._host_ip = socket.gethostbyname(self.host_name)
		return self._host_ip

	def _make_host_info(self):
		(self._host_sysname, self._host_nodename, self._host_release, self._host_version, self._host_machine) = os.uname()

	@property
	def host_sysname(self):
		if self._host_sysname is object:
			self._make_host_info()
		return self._host_sysname

	@property
	def host_nodename(self):
		if self._host_nodename is object:
			self._make_host_info()
		return self._host_nodename

	@property
	def host_release(self):
		if self._host_release is object:
			self._make_host_info()
		return self._host_release

	@property
	def host_version(self):
		if self._host_version is object:
			self._make_host_info()
		return self._host_version

	@property
	def host_machine(self):
		if self._host_machine is object:
			self._make_host_info()
		return self._host_machine

	def _make_user_info(self):
		import pwd
		(self._user_name, _, self._user_uid, self._user_gid, self._user_gecos, self._user_dir, self._user_shell) = pwd.getpwuid(os.getuid())

	@property
	def user_name(self):
		if self._user_name is object:
			self._make_user_info()
		return self._user_name

	@property
	def user_uid(self):
		if self._user_uid is object:
			self._make_user_info()
		return self._user_uid

	@property
	def user_gid(self):
		if self._user_gid is object:
			self._make_user_info()
		return self._user_gid

	@property
	def user_gecos(self):
		if self._user_gecos is object:
			self._make_user_info()
		return self._user_gecos

	@property
	def user_dir(self):
		if self._user_dir is object:
			self._make_user_info()
		return self._user_dir

	@property
	def user_shell(self):
		if self._user_shell is object:
			self._make_user_info()
		return self._user_shell

	@property
	def python_executable(self):
		return sys.executable

	@property
	def python_version(self):
		return ("{}.{}.{}" if sys.version_info.micro else "{}.{}").format(*sys.version_info)

	@property
	def pid(self):
		return os.getpid()

	@property
	def script_name(self):
		if self._script_name is object:
			main = sys.modules["__main__"]
			if hasattr(main, "__file__"):
				self._script_name = os.path.join(_curdir, main.__file__)
			else:
				self._script_name = "<shell>"
		return self._script_name

	@property
	def short_script_name(self):
		if self._short_script_name is object:
			script_name = self.script_name
			if script_name != "<shell>":
				userhome = os.path.expanduser("~")
				if script_name.startswith(userhome+"/"):
					script_name = "~" + script_name[len(userhome):]
			self._short_script_name = script_name
		return self._short_script_name

	@property
	def script_url(self):
		if self._script_url is object:
			from ll import url
			u = self.short_script_name
			if u != "<shell>":
				u = str(url.Ssh(self.user_name, self.host_fqdn or self.host_name, u))
			self._script_url = u
		return self._script_url

	def __getitem__(self, key):
		if key in self._keys:
			return getattr(self, key)
		raise KeyError(key)

	def __iter__(self):
		return iter(self._keys)


# Single instance
sysinfo = SysInfo()


class monthdelta:
	"""
	:class:`monthdelta` objects can be used to add months/years to a
	:class:`datetime.datetime` or :class:`datetime.date` object. If the resulting
	day falls out of the range of valid days for the target month, the last day
	for the target month will be used instead::

		>>> import datetime
		>>> from ll import misc
		>>> datetime.date(2000, 1, 31) + misc.monthdelta(1)
		datetime.date(2000, 2, 29)
	"""

	__slots__ = ("_months",)
	ul4attrs = {"months"}

	def __init__(self, months=0):
		self._months = months

	def __bool__(self):
		return self._months != 0

	def __hash__(self):
		return self._months

	def __eq__(self, other):
		return isinstance(other, monthdelta) and self._months == other._months

	def __ne__(self, other):
		return not isinstance(other, monthdelta) or self._months != other._months

	def __lt__(self, other):
		if not isinstance(other, monthdelta):
			raise TypeError("unorderable types: {0.__class__.__module__}.{0.__class__.__qualname__}() < {1.__class__.__module__}.{1.__class__.__qualname__}()".format(self, other))
		return self._months < other._months

	def __le__(self, other):
		if not isinstance(other, monthdelta):
			raise TypeError("unorderable types: {0.__class__.__module__}.{0.__class__.__qualname__}() <= {1.__class__.__module__}.{1.__class__.__qualname__}()".format(self, other))
		return self._months <= other._months

	def __gt__(self, other):
		if not isinstance(other, monthdelta):
			raise TypeError("unorderable types: {0.__class__.__module__}.{0.__class__.__qualname__}() > {1.__class__.__module__}.{1.__class__.__qualname__}()".format(self, other))
		return self._months > other._months

	def __ge__(self, other):
		if not isinstance(other, monthdelta):
			raise TypeError("unorderable types: {0.__class__.__module__}.{0.__class__.__qualname__}() >= {1.__class__.__module__}.{1.__class__.__qualname__}()".format(self, other))
		return self._months >= other._months

	def __add__(self, other):
		if isinstance(other, monthdelta):
			return monthdelta(self._months+other._months)
		elif isinstance(other, (datetime.datetime, datetime.date)):
			year = other.year
			month = other.month + self._months
			(years_add, month) = divmod(month-1, 12)
			month += 1
			year += years_add
			day = other.day
			while True:
				try:
					return other.replace(year=year, month=month, day=day)
				except ValueError:
					day -= 1
					if day == 1:
						raise
		else:
			return NotImplemented

	def __radd__(self, other):
		return self.__add__(other)

	def __sub__(self, other):
		if isinstance(other, monthdelta):
			return monthdelta(self._months-other._months)
		else:
			return NotImplemented

	def __rsub__(self, other):
		return other + (-self)

	def __neg__(self):
		return monthdelta(-self._months)

	def __abs__(self):
		return monthdelta(abs(self._months))

	def __mul__(self, other):
		if isinstance(other, int) and not isinstance(other, monthdelta):
			return monthdelta(self._months*other)
		else:
			return NotImplemented

	def __rmul__(self, other):
		return self.__mul__(other)

	def __floordiv__(self, other):
		if isinstance(other, int):
			return monthdelta(self._months//other)
		elif isinstance(other, monthdelta):
			return self._months//other._months
		else:
			return NotImplemented

	def __truediv__(self, other):
		if isinstance(other, monthdelta):
			return self._months/other._months
		else:
			return NotImplemented

	def __str__(self):
		m = self._months
		return "{} month{}".format(m, "s" if m != 1 and m != -1 else "")

	def __repr__(self):
		m = self._months
		if m:
			return "monthdelta({})".format(m)
		else:
			return "monthdelta()"

	def months(self):
		return self._months


class Timeout(Exception):
	"""
	Exception that is raised when a timeout in :func:`timeout` occurs.
	"""
	def __init__(self, seconds):
		self.seconds = seconds

	def __str__(self):
		return "timed out after {} seconds".format(self.seconds)


@contextlib.contextmanager
def timeout(seconds):
	"""
	A context manager that limits the runtime of the wrapped code.

	This doesn't work with threads and only on UNIX.
	"""

	def _timeouthandler(signum, frame):
		raise Timeout(seconds)

	oldsignal = signal.signal(signal.SIGALRM, _timeouthandler)
	signal.alarm(seconds)
	try:
		yield
	finally:
		signal.alarm(0)
		signal.signal(signal.SIGALRM, oldsignal)


def notifystart():
	"""
	Notify OS X of the start of a process by removing the previous notification.
	"""
	cmd = [notifycmd, "-remove", sysinfo.script_name]

	with open("/dev/null", "wb") as f:
		status = subprocess.call(cmd, stdout=f)


def notifyfinish(title, subtitle, message):
	"""
	Notify OS X of the end of a process.
	"""
	cmd = [notifycmd, "-title", title, "-subtitle", subtitle, "-message", message, "-group", sysinfo.script_name]

	with open("/dev/null", "wb") as f:
		status = subprocess.call(cmd, stdout=f)


def prettycsv(rows, padding="   "):
	"""
	Format table :obj:`rows`.

	:obj:`rows` must be a list of lists of strings (e.g. as produced by the
	:mod:`csv` module). :obj:`padding` is the padding between columns.

	:func:`prettycsv` is a generator.
	"""

	def width(row, i):
		try:
			return len(row[i])
		except IndexError:
			return 0

	maxlen = max(len(row) for row in rows)
	lengths = [max(width(row, i) for row in rows) for i in range(maxlen)]
	for row in rows:
		lasti = len(row)-1
		for (i, (w, f)) in enumerate(zip(lengths, row)):
			if i:
				yield padding
			if i == lasti:
				f = f.rstrip() # don't add padding to the last column
			else:
				f = "{0:<{1}}".format(f, w)
			yield f
		yield "\n"


class JSMinUnterminatedComment(Exception):
	pass


class JSMinUnterminatedStringLiteral(Exception):
	pass


class JSMinUnterminatedRegularExpression(Exception):
	pass


def jsmin(input):
	"""
	Minimizes the Javascript source :obj:`input`.
	"""
	indata = iter(input.replace("\r", "\n"))

	# Copy the input to the output, deleting the characters which are
	# insignificant to JavaScript. Comments will be removed. Tabs will be
	# replaced with spaces. Carriage returns will be replaced with linefeeds.
	# Most spaces and linefeeds will be removed.

	class var:
		a = "\n"
		b = None
		lookahead = None
	outdata = []

	def _get():
		# Return the next character from the input. Watch out for lookahead. If
		# the character is a control character, translate it to a space or linefeed.
		c = var.lookahead
		var.lookahead = None
		if c is None:
			try:
				c = next(indata)
			except StopIteration:
				return "" # EOF
		if c >= " " or c == "\n":
			return c
		return " "

	def _peek():
		var.lookahead = _get()
		return var.lookahead

	def isalphanum(c):
		# Return true if the character is a letter, digit, underscore, dollar sign, or non-ASCII character.
		return ('a' <= c <= 'z') or ('0' <= c <= '9') or ('A' <= c <= 'Z') or c in "_$\\" or (c is not None and ord(c) > 126)

	def _next():
		# Get the next character, excluding comments. peek() is used to see if an unescaped '/' is followed by a '/' or '*'.
		c = _get()
		if c == "/" and var.a != "\\":
			p = _peek()
			if p == "/":
				c = _get()
				while c > "\n":
					c = _get()
				return c
			if p == "*":
				c = _get()
				while 1:
					c = _get()
					if c == "*":
						if _peek() == "/":
							_get()
							return " "
					if not c:
						raise JSMinUnterminatedComment()
		return c

	def _action(action):
		"""
		Do something! What you do is determined by the argument:
		   1   Output A. Copy B to A. Get the next B.
		   2   Copy B to A. Get the next B. (Delete A).
		   3   Get the next B. (Delete B).
		action treats a string as a single character. Wow!
		action recognizes a regular expression if it is preceded by ( or , or =.
		"""
		if action <= 1:
			outdata.append(var.a)

		if action <= 2:
			var.a = var.b
			if var.a in "'\"":
				while True:
					outdata.append(var.a)
					var.a = _get()
					if var.a == var.b:
						break
					if var.a <= "\n":
						raise JSMinUnterminatedStringLiteral()
					if var.a == "\\":
						outdata.append(var.a)
						var.a = _get()

		if action <= 3:
			var.b = _next()
			if var.b == "/" and var.a in "(,=:[?!&|;{}\n":
				outdata.append(var.a)
				outdata.append(var.b)
				while True:
					var.a = _get()
					if var.a == "/":
						break
					elif var.a == "\\":
						outdata.append(var.a)
						var.a = _get()
					elif var.a <= "\n":
						raise JSMinUnterminatedRegularExpression()
					outdata.append(var.a)
				var.b = _next()

	_action(3)

	while var.a:
		if var.a == " ":
			_action(1 if isalphanum(var.b) else 2)
		elif var.a == "\n":
			if var.b in "{[(+-":
				_action(1)
			elif var.b == " ":
				_action(3)
			else:
				_action(1 if isalphanum(var.b) else 2)
		else:
			if var.b == " ":
				_action(1 if isalphanum(var.a) else 3)
			elif var.b == "\n":
				_action(1 if isalphanum(var.a) or var.a in "}])+-\"'" else 3)
			else:
				_action(1)
	return "".join(outdata).lstrip()
