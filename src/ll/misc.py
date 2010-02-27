#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2004-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2004-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
:mod:`ll.misc` contains various utility functions and classes used by the other
LivingLogic modules and packages.
"""


import sys, types, collections, weakref, cStringIO, gzip as gzip_


__docformat__ = "reStructuredText"


# fetch item, first, last, count and xmlescape
try:
	from ll._misc import *
except ImportError:
	# Use Python implementations of those functions
	_defaultitem = object()

	def item(iterator, index, default=_defaultitem):
		"""
		Returns the :var:`index`'th element from the iterable. :var:`index` may be
		negative to count from the end. E.g. 0 returns the first element produced
		by the iterator, 1 the second, -1 the last one etc. If :var:`index` is
		negative the iterator will be completely exhausted, if it's positive it
		will be exhausted up to the :var:`index`'th element. If the iterator
		doesn't produce that many elements :exc:`IndexError` will be raised,
		except when :var:`default` is given, in which case :var:`default` will be
		returned.
		"""
		i = index
		if i>=0:
			for item in iterator:
				if not i:
					return item
				i -= 1
		else:
			i = -index
			cache = collections.deque()
			for item in iterator:
				cache.append(item)
				if len(cache)>i:
					cache.popleft()
			if len(cache)==i:
				return cache.popleft()
		if default is _defaultitem:
			raise IndexError(index)
		else:
			return default


	def first(iterator, default=_defaultitem):
		"""
		Return the first element from the iterable. If the iterator doesn't
		produce any elements :exc:`IndexError` will be raised, except when
		:var:`default` is given, in which case :var:`default` will be returned.
		"""
		return item(iterator, 0, default)


	def last(iterator, default=_defaultitem):
		"""
		Return the last element from the iterable. If the iterator doesn't produce
		any elements :exc:`IndexError` will be raised, except when :var:`default`
		is given, in which case :var:`default` will be returned.
		"""
		return item(iterator, -1, default)


	def count(iterator):
		"""
		Count the number of elements produced by the iterable. Calling this
		function will exhaust the iterator.
		"""
		count = 0
		for node in iterator:
			count += 1
		return count

	def xmlescape(string):
		"""
		Return a copy of the argument string, where every occurrence of ``<``,
		``>``, ``&``, ``\"``, ``'`` and every restricted character has been
		replaced with their XML character entity or character reference.
		"""
		if isinstance(string, unicode):
			return string.translate({0x00: u'&#0;', 0x01: u'&#1;', 0x02: u'&#2;', 0x03: u'&#3;', 0x04: u'&#4;', 0x05: u'&#5;', 0x06: u'&#6;', 0x07: u'&#7;', 0x08: u'&#8;', 0x0b: u'&#11;', 0x0c: u'&#12;', 0x0e: u'&#14;', 0x0f: u'&#15;', 0x10: u'&#16;', 0x11: u'&#17;', 0x12: u'&#18;', 0x13: u'&#19;', 0x14: u'&#20;', 0x15: u'&#21;', 0x16: u'&#22;', 0x17: u'&#23;', 0x18: u'&#24;', 0x19: u'&#25;', 0x1a: u'&#26;', 0x1b: u'&#27;', 0x1c: u'&#28;', 0x1d: u'&#29;', 0x1e: u'&#30;', 0x1f: u'&#31;', 0x22: u'&quot;', 0x26: u'&amp;', 0x27: u'&#39;', 0x3c: u'&lt;', 0x3e: u'&gt;', 0x7f: u'&#127;', 0x80: u'&#128;', 0x81: u'&#129;', 0x82: u'&#130;', 0x83: u'&#131;', 0x84: u'&#132;', 0x86: u'&#134;', 0x87: u'&#135;', 0x88: u'&#136;', 0x89: u'&#137;', 0x8a: u'&#138;', 0x8b: u'&#139;', 0x8c: u'&#140;', 0x8d: u'&#141;', 0x8e: u'&#142;', 0x8f: u'&#143;', 0x90: u'&#144;', 0x91: u'&#145;', 0x92: u'&#146;', 0x93: u'&#147;', 0x94: u'&#148;', 0x95: u'&#149;', 0x96: u'&#150;', 0x97: u'&#151;', 0x98: u'&#152;', 0x99: u'&#153;', 0x9a: u'&#154;', 0x9b: u'&#155;', 0x9c: u'&#156;', 0x9d: u'&#157;', 0x9e: u'&#158;', 0x9f: u'&#159;'})
		else:
			string = string.replace("&", "&amp;")
			string = string.replace("<", "&lt;")
			string = string.replace(">", "&gt;")
			string = string.replace("'", "&#39;")
			string = string.replace('"', "&quot;")
			for c in "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1f\x7f\x80\x81\x82\x83\x84\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f":
				string = string.replace(c, "&#%d;" % ord(c))
			return string

	def xmlescape_text(string):
		"""
		Return a copy of the argument string, where every occurrence of ``<``,
		``>``, ``&``, and every restricted character has been replaced with their
		XML character entity or character reference.
		"""
		if isinstance(string, unicode):
			return string.translate({0x00: u'&#0;', 0x01: u'&#1;', 0x02: u'&#2;', 0x03: u'&#3;', 0x04: u'&#4;', 0x05: u'&#5;', 0x06: u'&#6;', 0x07: u'&#7;', 0x08: u'&#8;', 0x0b: u'&#11;', 0x0c: u'&#12;', 0x0e: u'&#14;', 0x0f: u'&#15;', 0x10: u'&#16;', 0x11: u'&#17;', 0x12: u'&#18;', 0x13: u'&#19;', 0x14: u'&#20;', 0x15: u'&#21;', 0x16: u'&#22;', 0x17: u'&#23;', 0x18: u'&#24;', 0x19: u'&#25;', 0x1a: u'&#26;', 0x1b: u'&#27;', 0x1c: u'&#28;', 0x1d: u'&#29;', 0x1e: u'&#30;', 0x1f: u'&#31;', 0x26: u'&amp;', 0x3c: u'&lt;', 0x3e: u'&gt;', 0x7f: u'&#127;', 0x80: u'&#128;', 0x81: u'&#129;', 0x82: u'&#130;', 0x83: u'&#131;', 0x84: u'&#132;', 0x86: u'&#134;', 0x87: u'&#135;', 0x88: u'&#136;', 0x89: u'&#137;', 0x8a: u'&#138;', 0x8b: u'&#139;', 0x8c: u'&#140;', 0x8d: u'&#141;', 0x8e: u'&#142;', 0x8f: u'&#143;', 0x90: u'&#144;', 0x91: u'&#145;', 0x92: u'&#146;', 0x93: u'&#147;', 0x94: u'&#148;', 0x95: u'&#149;', 0x96: u'&#150;', 0x97: u'&#151;', 0x98: u'&#152;', 0x99: u'&#153;', 0x9a: u'&#154;', 0x9b: u'&#155;', 0x9c: u'&#156;', 0x9d: u'&#157;', 0x9e: u'&#158;', 0x9f: u'&#159;'})
		else:
			string = string.replace("&", "&amp;")
			string = string.replace("<", "&lt;")
			string = string.replace(">", "&gt;")
			for c in "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1f\x7f\x80\x81\x82\x83\x84\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f":
				string = string.replace(c, "&#%d;" % ord(c))
			return string

	def xmlescape_attr(string):
		"""
		Return a copy of the argument string, where every occurrence of ``<``,
		``>``, ``&``, ``"`` and every restricted character has been replaced with
		their XML character entity or character reference.
		"""
		if isinstance(string, unicode):
			return string.translate({0x00: u'&#0;', 0x01: u'&#1;', 0x02: u'&#2;', 0x03: u'&#3;', 0x04: u'&#4;', 0x05: u'&#5;', 0x06: u'&#6;', 0x07: u'&#7;', 0x08: u'&#8;', 0x0b: u'&#11;', 0x0c: u'&#12;', 0x0e: u'&#14;', 0x0f: u'&#15;', 0x10: u'&#16;', 0x11: u'&#17;', 0x12: u'&#18;', 0x13: u'&#19;', 0x14: u'&#20;', 0x15: u'&#21;', 0x16: u'&#22;', 0x17: u'&#23;', 0x18: u'&#24;', 0x19: u'&#25;', 0x1a: u'&#26;', 0x1b: u'&#27;', 0x1c: u'&#28;', 0x1d: u'&#29;', 0x1e: u'&#30;', 0x1f: u'&#31;', 0x22: u'&quot;', 0x26: u'&amp;', 0x3c: u'&lt;', 0x3e: u'&gt;', 0x7f: u'&#127;', 0x80: u'&#128;', 0x81: u'&#129;', 0x82: u'&#130;', 0x83: u'&#131;', 0x84: u'&#132;', 0x86: u'&#134;', 0x87: u'&#135;', 0x88: u'&#136;', 0x89: u'&#137;', 0x8a: u'&#138;', 0x8b: u'&#139;', 0x8c: u'&#140;', 0x8d: u'&#141;', 0x8e: u'&#142;', 0x8f: u'&#143;', 0x90: u'&#144;', 0x91: u'&#145;', 0x92: u'&#146;', 0x93: u'&#147;', 0x94: u'&#148;', 0x95: u'&#149;', 0x96: u'&#150;', 0x97: u'&#151;', 0x98: u'&#152;', 0x99: u'&#153;', 0x9a: u'&#154;', 0x9b: u'&#155;', 0x9c: u'&#156;', 0x9d: u'&#157;', 0x9e: u'&#158;', 0x9f: u'&#159;'})
		else:
			string = string.replace("&", "&amp;")
			string = string.replace("<", "&lt;")
			string = string.replace(">", "&gt;")
			string = string.replace('"', "&quot;")
			for c in "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1f\x7f\x80\x81\x82\x83\x84\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f":
				string = string.replace(c, "&#%d;" % ord(c))
			return string


def notimplemented(function):
	"""
	A decorator that raises :exc:`NotImplementedError` when the method is called.
	This saves you the trouble of formatting the error message yourself for each
	implementation.
	"""
	def wrapper(self, *args, **kwargs):
		raise NotImplementedError("method %s() not implemented in %r" % (function.__name__, self.__class__))
	wrapper.__dict__.update(function.__dict__)
	wrapper.__doc__ = function.__doc__
	wrapper.__name__ = function.__name__
	wrapper.__wrapped__ = function
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


class propclass(property):
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
	__metaclass__ = _propclass_Meta


class Pool(object):
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
		Register :var:`object` in the pool. :var:`object` can be a module, a
		dictionary or a :class:`Pool` objects (with registers the pool as a base
		pool. If :var:`object` is a module and has an attribute :attr:`__bases__`
		(being a sequence of other modules) this attribute will be used to
		initialize :var:`self` base pool.
		"""
		if isinstance(object, types.ModuleType):
			self._attrs.update(object.__dict__)
			if hasattr(object, "__bases__"):
				for base in object.__bases__:
					if not isinstance(base, Pool):
						base = self.__class__(base)
					self.register(base)
		elif isinstance(object, dict):
			for (key, value) in object.iteritems():
				try:
					self._attrs[key] = value
				except TypeError:
					pass
		elif isinstance(object, Pool):
			self.bases.append(object)

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
		Make :var:`self` empty.
		"""
		self._attrs.clear()
		del self.bases[:]

	def clone(self):
		"""
		Return a copy of :var:`self`.
		"""
		copy = self.__class__()
		copy._attrs = self._attrs.copy()
		copy.bases = self.bases[:]
		return copy

	def __repr__(self):
		return "<%s.%s object with %d items at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, len(self._attrs), id(self))


def iterone(item):
	"""
	Return an iterator that will produce one item: :var:`item`.
	"""
	yield item


class Iterator(object):
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
		return item(self, index)

	def __iter__(self):
		return self

	def next(self):
		return self.iterator.next()

	# We can't implement :meth:`__len__`, because if such an object is passed to
	# :class:`list`, :meth:`__len__` would be called, exhausting the iterator

	def __nonzero__(self):
		for node in self:
			return True
		return False

	def get(self, index, default=None):
		"""
		Return the :var:`index`\th item from the iterator (or :var:`default` if
		there's no such item).
		"""
		return item(self, index, default)


class Queue(object):
	"""
	:class:`Queue` provides FIFO queues: The method :meth:`write` writes to the
	queue and the method :meth:`read` read from the other end of the queue and
	remove the characters read.
	"""
	def __init__(self):
		self._buffer = ""

	def write(self, chars):
		"""
		Write the string :var:`chars` to the buffer.
		"""
		self._buffer += chars

	def read(self, size=-1):
		"""
		Read up to :var:`size` character from the buffer (or all if :var:`size`
		is negative). Those characters will be removed from the buffer.
		"""
		if size<0:
			s = self._buffer
			self._buffer = ""
			return s
		else:
			s = self._buffer[:size]
			self._buffer = self._buffer[size:]
			return s


class Const(object):
	"""
	This class can be used for singleton constants.
	"""
	__slots__ = ("_name")

	def __init__(self, name):
		self._name = name

	def __repr__(self):
		return "%s.%s" % (self.__module__, self._name)


def tokenizepi(string):
	"""
	Tokenize the string object :var:`string` according to the processing
	instructions in the string. :func:`tokenize` will generate tuples with the
	first item being the processing instruction target and the second being the
	PI data. "Text" content (i.e. anything other than PIs) will be returned as
	``(None, data)``.
	"""

	pos = 0
	while True:
		pos1 = string.find("<?", pos)
		if pos1<0:
			part = string[pos:]
			if part:
				yield (None, part)
			return
		pos2 = string.find("?>", pos1)
		if pos2<0:
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


def gzip(data, compresslevel=9):
	"""
	Compresses the byte string :var:`data` with gzip using the compression level
	:var:`compresslevel`.
	"""
	stream = cStringIO.StringIO()
	compressor = gzip_.GzipFile(filename="", mode="wb", fileobj=stream, compresslevel=compresslevel)
	compressor.write(data)
	compressor.close()
	return stream.getvalue()


def gunzip(data):
	"""
	Uncompresses the byte string :var:`data` with gzip.
	"""
	stream = cStringIO.StringIO(data)
	compressor = gzip_.GzipFile(filename="", mode="rb", fileobj=stream)
	return compressor.read()


def itersplitat(string, positions):
	"""
	Split :var:`string` at the positions specified in :var:`positions`.

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


class JSMinUnterminatedComment(Exception):
	pass

class JSMinUnterminatedStringLiteral(Exception):
	pass

class JSMinUnterminatedRegularExpression(Exception):
	pass


def jsmin(input):
	"""
	Minimizes the Javascript source :var:`input`.
	"""

	indata = iter(input.replace("\r", "\n"))

	# Copy the input to the output, deleting the characters which are
	# insignificant to JavaScript. Comments will be removed. Tabs will be
	# replaced with spaces. Carriage returns will be replaced with linefeeds.
	# Most spaces and linefeeds will be removed.

	class var(object):
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
				c = indata.next()
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
