# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2011-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2011-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


'''
This module provides functions for encoding and decoding a lightweight
text-based format for serializing the object types supported by UL4.

It is extensible to allow encoding/decoding arbitrary instances (i.e. it is
basically a reimplementation of :mod:`pickle`, but with string input/output
instead of bytes and with an eye towards cross-plattform support).

There are implementations for Python (this module), Java_ and Javascript_
(as part of the UL4 packages for those languages).

.. _Java: https://github.com/LivingLogic/LivingLogic.Java.ul4
.. _Javascript: https://github.com/LivingLogic/LivingLogic.Javascript.ul4

Furthermore there's an `Oracle package`_ that can be used for generating
UL4ON encoded data.

.. _Oracle package: https://github.com/LivingLogic/LivingLogic.Oracle.ul4

Basic usage follows the API design of :mod:`pickle`, :mod:`json`, etc. and
supports most builtin Python types::

	>>> from ll import ul4on
	>>> ul4on.dumps(None)
	'n'
	>>> ul4on.loads('n')
	>>> ul4on.dumps(False)
	'bF'
	>>> ul4on.loads('bF')
	False
	>>> ul4on.dumps(42)
	'i42'
	>>> ul4on.loads('i42')
	42
	>>> ul4on.dumps(42.5)
	'f42.5'
	>>> ul4on.loads('f42.5')
	42.5
	>>> ul4on.dumps('foo')
	"S'foo'"
	>>> ul4on.loads("S'foo'")
	'foo'

:class:`date`, :class:`datetime` and :class:`timedelta` objects are supported too::

	>>> import datetime
	>>> ul4on.dumps(datetime.date.today())
	'X i2014 i11 i3'
	>>> ul4on.dumps(datetime.datetime.now())
	'Z i2014 i11 i3 i18 i16 i45 i314157'
	>>> ul4on.loads('X i2014 i11 i3')
	datetime.date(2014, 11, 3)
	>>> ul4on.loads('Z i2014 i11 i3 i18 i16 i45 i314157')
	datetime.datetime(2014, 11, 3, 18, 16, 45, 314157)
	>>> ul4on.dumps(datetime.timedelta(days=1))
	'T i1 i0 i0'
	>>> ul4on.loads('T i1 i0 i0')
	datetime.timedelta(1)

:mod:`ll.ul4on` also supports :class:`Color` objects from :mod:`ll.color`::

	>>> from ll import color
	>>> ul4on.dumps(color.red)
	'C i255 i0 i0 i255'
	>>> ul4on.loads('C i255 i0 i0 i255')
	Color(0xff, 0x00, 0x00)

Lists, dictionaries and sets are also supported::

	>>> ul4on.dumps([1, 2, 3])
	'L i1 i2 i3 ]'
	>>> ul4on.loads('L i1 i2 i3 ]')
	[1, 2, 3]
	>>> ul4on.dumps(dict(one=1, two=2))
	"D S'two' i2 S'one' i1 }"
	>>> ul4on.loads("D S'two' i2 S'one' i1 }")
	{'one': 1, 'two': 2}
	>>> ul4on.dumps({1, 2, 3})
	'Y i1 i2 i3 }'
	>>> ul4on.loads('Y i1 i2 i3 }')
	{1, 2, 3}

:mod:`ll.ul4on` can also handle recursive data structures::

	>>> r = []
	>>> r.append(r)
	>>> ul4on.dumps(r)
	'L ^0 ]'
	>>> r2 = ul4on.loads('L ^0 ]')
	>>> r2
	[[...]]
	>>> r2 is r2[0]
	True
	>>> r = {}
	>>> r['recursive'] = r
	>>> ul4on.dumps(r)
	"D S'recursive' ^0 }"
	>>> r2 = ul4on.loads("D S'recursive' ^0 }")
	>>> r2
	{'recursive': {...}}
	>>> r2['recursive'] is r2
	True

UL4ON is extensible. It supports serializing arbitrary instances by registering
the class with the UL4ON serialization machinery::

	from ll import ul4on

	@ul4on.register("com.example.person")
	class Person:
		def __init__(self, firstname=None, lastname=None):
			self.firstname = firstname
			self.lastname = lastname

		def __repr__(self):
			return f"<Person firstname={self.firstname!r} lastname={self.lastname!r}>"

		def ul4ondump(self, encoder):
			encoder.dump(self.firstname)
			encoder.dump(self.lastname)

		def ul4onload(self, decoder):
			self.firstname = decoder.load()
			self.lastname = decoder.load()

	jd = Person("John", "Doe")
	output = ul4on.dumps(jd)
	print("Dump:", output)
	jd2 = ul4on.loads(output)
	print("Loaded:", jd2)

This script outputs::

	Dump: O S'com.example.person' S'John' S'Doe' )
	Loaded: <Person firstname='John' lastname='Doe'>

It is also possible to pass a custom registry to :func:`load` and
:func:`loads`::

	from ll import ul4on

	class Person:
		ul4onname = "com.example.person"

		def __init__(self, firstname=None, lastname=None):
			self.firstname = firstname
			self.lastname = lastname

		def __repr__(self):
			return f"<Person firstname={self.firstname!r} lastname={self.lastname!r}>"

		def ul4ondump(self, encoder):
			encoder.dump(self.firstname)
			encoder.dump(self.lastname)

		def ul4onload(self, decoder):
			self.firstname = decoder.load()
			self.lastname = decoder.load()

	jd = Person("John", "Doe")
	output = ul4on.dumps(jd)
	print("Dump:", output)
	jd2 = ul4on.loads(output, {"com.example.person": Person})
	print("Loaded:", jd2)

Any type name not found in the registry dict passed in will be looked up in the
global registry.

.. note::
	If a class isn't registered with the UL4ON serialization machinery, you have
	to set the class attribute ``ul4onname`` yourself for serialization to work.

In situations where an UL4ON API is updated frequently it makes sense to be able
to update the writing side and the reading side independently. To support this
:class:`Decoder` has a method :meth:`~Decoder.loadcontent` that is an generator
that reads the content of an object from the input and yields those items.
For our example class it could be used like this::

	from ll import ul4on

	class Person:
		ul4onname = "com.example.person"

		def __init__(self, firstname=None, lastname=None):
			self.firstname = firstname
			self.lastname = lastname

		def __repr__(self):
			return f"<Person firstname={self.firstname!r} lastname={self.lastname!r}>"

		def ul4ondump(self, encoder):
			encoder.dump(self.firstname)
			encoder.dump(self.lastname)

		def ul4onload(self, decoder):
			index = -1
			for (index, item) in enumerate(decoder.loadcontent()):
				if index == 0:
					self.firstname = item
				elif index == 1:
					self.lastname = item
			# Initialize attributes that were not loaded by ``loadcontent``
			if index < 1:
				self.lastname = None
				if index < 0:
					self.firstname = None

	output = """o s'com.example.person' s'John' )"""
	j = ul4on.loads(output, {"com.example.person": Person})
	print("Loaded:", j)
'''

import sys, datetime, collections, io, ast
from collections import abc


__docformat__ = "reStructuredText"


_registry = {}


def register(name):
	"""
	This decorator can be used to register the decorated class with the
	:mod:`ll.ul4on` serialization machinery.

	:obj:`name` must be a globally unique name for the class. To avoid
	name collisions Java's class naming system should be used (i.e. an
	inverted domain name like ``com.example.foo.bar``).

	:obj:`name` will be stored in the class attribute ``ul4onname``.
	"""
	def registration(cls):
		cls.ul4onname = name
		_registry[name] = cls
		return cls
	return registration


class Encoder:
	"""
	A :class:`Encoder` is used for serializing an object into an UL4ON dump.

	It manages the internal state required for handling backreferences and other
	stuff.
	"""
	def __init__(self, stream, indent=None):
		"""
		Create an encoder for serializing objects to  :obj:`self.stream`.

		:obj:`stream` must provide a :meth:`write` method.
		"""
		self.stream = stream
		self._level = 0
		self.indent = indent
		self._lastwaslf = False
		self._first = True # Remember whether we have dumped something into the stream (so we have to write separator whitespace/indentation) or not
		self._objects = []
		self._id2index = {}

	def _record(self, obj):
		# Record that we've written this object and in which position
		self._id2index[id(obj)] = len(self._objects)
		self._objects.append(obj)

	def _line(self, line, *items):
		if self.indent:
			self.stream.write(self.indent*self._level)
		else:
			if not self._first:
				self.stream.write(" ")
		self._first = False
		self.stream.write(line)
		if items:
			oldindent = self.indent
			try:
				self.indent = ""
				for item in items:
					self.dump(item)
			finally:
				self.indent = oldindent
		if self.indent:
			self.stream.write("\n")

	def dump(self, obj):
		"""
		Serialize :obj:`obj` into the stream as an UL4ON formatted dump.
		"""
		# Have we written this object already?
		if id(obj) in self._id2index:
			# Yes: Store a backreference to the object
			self._line(f"^{self._id2index[id(obj)]}")
		else:
			from ll import color, misc
			# No: Write the object itself
			# We're not using backreferences if the object itself has a shorter dump
			if obj is None:
				self._line("n")
			elif isinstance(obj, bool):
				self._line("bT" if obj else "bF")
			elif isinstance(obj, int):
				self._line(f"i{obj}")
			elif isinstance(obj, float):
				self._line(f"f{obj!r}")
			elif isinstance(obj, str):
				self._record(obj)
				dump = repr(obj).replace("<", "\\x3c") # Prevent XSS (when the value is embedded literally in a ``<script>`` tag)
				self._line(f"S{dump}")
			elif isinstance(obj, slice):
				self._record(obj)
				self._line("R", obj.start, obj.stop)
			elif isinstance(obj, color.Color):
				self._record(obj)
				self._line("C", obj.r(), obj.g(), obj.b(), obj.a())
			elif isinstance(obj, datetime.datetime):
				self._record(obj)
				self._line("Z", obj.year, obj.month, obj.day, obj.hour, obj.minute, obj.second, obj.microsecond)
			elif isinstance(obj, datetime.date):
				self._record(obj)
				self._line("X", obj.year, obj.month, obj.day)
			elif isinstance(obj, datetime.timedelta):
				self._record(obj)
				self._line("T", obj.days, obj.seconds, obj.microseconds)
			elif isinstance(obj, misc.monthdelta):
				self._record(obj)
				self._line("M", obj.months())
			elif isinstance(obj, abc.Sequence):
				self._record(obj)
				self._line("L")
				self._level += 1
				for item in obj:
					self.dump(item)
				self._level -= 1
				self._line("]")
			elif isinstance(obj, (dict, collections.OrderedDict)):
				self._record(obj)
				self._line("E")
				self._level += 1
				for (key, item) in obj.items():
					self.dump(key)
					self.dump(item)
				self._level -= 1
				self._line("}")
			elif isinstance(obj, abc.Mapping):
				self._record(obj)
				self._line("D")
				self._level += 1
				for (key, item) in obj.items():
					self.dump(key)
					self.dump(item)
				self._level -= 1
				self._line("}")
			elif isinstance(obj, abc.Set):
				self._record(obj)
				self._line("Y")
				self._level += 1
				for item in obj:
					self.dump(item)
				self._level -= 1
				self._line("}")
			else:
				self._record(obj)
				self._line("O", obj.ul4onname)
				self._level += 1
				obj.ul4ondump(self)
				self._level -= 1
				self._line(")")


class Decoder:
	"""
	A :class:`Decoder` is used for deserializing an UL4ON dump.

	It manages the internal state required for handling backreferences and other
	stuff.
	"""
	def __init__(self, stream, registry=None):
		"""
		Create a decoder for deserializing objects from  :obj:`self.stream`.

		:obj:`stream` must provide a :meth:`read` method.

		:obj:`registry` is used as a "custom type registry". It must map UL4ON
		type names to callables that create new empty instances of those types.
		Any type not found in :obj:`registry` will be looked up in the global
		registry (see :func:`register`).
		"""
		self.stream = stream
		self._bufferedchar = None # Next character to be read by :meth:`_nextchar`
		self._objects = []
		self._keycache = {} # Used for "interning" dictionary keys
		self.registry = registry
		self._stack = [] # A stack of types that are currently in the process of being decoded (used in exception messages)

	def _readint(self):
		buffer = io.StringIO()
		while True:
			c = self.stream.read(1)
			if c and not c.isspace():
				buffer.write(c)
			else:
				return int(buffer.getvalue())

	def _loading(self, obj):
		self._objects.append(obj)

	def _nextchar(self):
		if self._bufferedchar is not None:
			result = self._bufferedchar
			self._bufferedchar = None
			return result
		else:
			while True:
				nextchar = self.stream.read(1)
				if nextchar:
					if not nextchar.isspace():
						return nextchar
				else:
					raise EOFError()

	def _path(self):
		return "/".join(self._stack)

	def _beginfakeloading(self):
		# For loading custom object or immutable objects that have attributes we have a problem:
		# We have to record the object we're loading *now*, so that it is available for backreferences.
		# However until we've read the UL4ON name of the class (for custom object) or the attributes
		# of the object (for immutable objects with attributes), we can't create the object.
		# So we push ``None`` to the backreference list for now and put the right object in this spot,
		# once we've created it (via :meth:`_endfakeloading`). This shouldn't lead to problems,
		# because during the time the backreference is wrong, only the class name is read,
		# so our object won't be referenced. For immutable objects the attributes normally
		# don't reference the object itself.
		oldpos = len(self._objects)
		self._loading(None)
		return oldpos

	def _endfakeloading(self, oldpos, value):
		# Fix backreference in object list
		self._objects[oldpos] = value

	def load(self):
		"""
		Deserialize the next object in the stream and return it.
		"""
		from ll import misc
		typecode = self._nextchar()
		if typecode == "^":
			position = self._readint()
			return self._objects[position]
		elif typecode in "nN":
			if typecode == "N":
				self._loading(None)
			return None
		elif typecode in "bB":
			value = self.stream.read(1)
			if value == "T":
				value = True
			elif value == "F":
				value = False
			else:
				raise ValueError(f"broken UL4ON stream at position {self.stream.tell():,}: expected 'T' or 'F' for bool; got {value!r}")
			if typecode == "B":
				self._loading(value)
			return value
		elif typecode in "iI":
			value = self._readint()
			if typecode == "I":
				self._loading(value)
			return value
		elif typecode in "fF":
			chars = []
			while True:
				c = self.stream.read(1)
				if c and not c.isspace():
					chars.append(c)
				else:
					value = float("".join(chars))
					break
			if typecode == "F":
				self._loading(value)
			return value
		elif typecode in "sS":
			delimiter = self.stream.read(1)
			if not delimiter:
				raise EOFError()
			buffer = []
			while True:
				c = self.stream.read(1)
				if not c:
					raise EOFError()
				if c == delimiter:
					value = "".join(buffer).encode("ascii", "backslashreplace").decode("unicode_escape")
					break
				buffer.append(c)
				if c == "\\":
					c2 = self.stream.read(1)
					if not c2:
						raise EOFError()
					buffer.append(c2)
			if typecode == "S":
				self._loading(value)
			return value
		elif typecode in "cC":
			from ll import color
			if typecode == "C":
				oldpos = self._beginfakeloading()
			r = self.load()
			g = self.load()
			b = self.load()
			a = self.load()
			value = color.Color(r, g, b, a)
			if typecode == "C":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "zZ":
			if typecode == "Z":
				oldpos = self._beginfakeloading()
			year = self.load()
			month = self.load()
			day = self.load()
			hour = self.load()
			minute = self.load()
			second = self.load()
			microsecond = self.load()
			value = datetime.datetime(year, month, day, hour, minute, second, microsecond)
			if typecode == "Z":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "xX":
			if typecode == "X":
				oldpos = self._beginfakeloading()
			year = self.load()
			month = self.load()
			day = self.load()
			value = datetime.date(year, month, day)
			if typecode == "X":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "rR":
			if typecode == "R":
				oldpos = self._beginfakeloading()
			start = self.load()
			stop = self.load()
			value = slice(start, stop)
			if typecode == "R":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "tT":
			if typecode == "T":
				oldpos = self._beginfakeloading()
			days = self.load()
			seconds = self.load()
			microseconds = self.load()
			value = datetime.timedelta(days, seconds, microseconds)
			if typecode == "T":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "mM":
			from ll import misc
			if typecode == "M":
				oldpos = self._beginfakeloading()
			months = self.load()
			value = misc.monthdelta(months)
			if typecode == "M":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "lL":
			self._stack.append("list")
			value = []
			if typecode == "L":
				self._loading(value)
			while True:
				typecode = self._nextchar()
				if typecode == "]":
					self._stack.pop()
					return value
				else:
					self._bufferedchar = typecode
					item = self.load()
					value.append(item)
		elif typecode in "dDeE":
			self._stack.append("dict" if typecode in "dD" else "odict")
			value = {} # Load all dicts as a standard Python 3.6 ordered dict
			if typecode in "DE":
				self._loading(value)
			while True:
				typecode = self._nextchar()
				if typecode == "}":
					self._stack.pop()
					return value
				else:
					self._bufferedchar = typecode
					key = self.load()
					if isinstance(key, str):
						if key in self._keycache:
							key = self._keycache[key]
						else:
							self._keycache[key] = key
					item = self.load()
					value[key] = item
		elif typecode in "yY":
			self._stack.append("set")
			value = set()
			if typecode == "Y":
				self._loading(value)
			while True:
				typecode = self._nextchar()
				if typecode == "}":
					self._stack.pop()
					return value
				else:
					self._bufferedchar = typecode
					item = self.load()
					value.add(item)
		elif typecode in "oO":
			if typecode == "O":
				oldpos = self._beginfakeloading()
			name = self.load()
			self._stack.append(name)
			cls = None
			if self.registry is not None:
				cls = self.registry.get(name)
			if cls is None:
				cls = _registry.get(name)
			if cls is None:
				raise TypeError(f"broken UL4ON stream at position {self.stream.tell():,} (path {self._path()}): can't decode object of type {name!r}")
			value = cls()
			if typecode == "O":
				self._endfakeloading(oldpos, value)
			value.ul4onload(self)
			typecode = self._nextchar()
			if typecode != ")":
				raise ValueError(f"broken UL4ON stream at position {self.stream.tell():,} (path {self._path()}): object terminator ')' expected, got {typecode!r}")
			self._stack.pop()
			return value
		else:
			raise ValueError(f"broken UL4ON stream at position {self.stream.tell():,} (path {self._path()}): unknown typecode {typecode!r}")

	def loadcontent(self):
		"""
		Load the content of an object until the "object terminator" is encountered.

		This is a generator and might produce fewer or more items than expected.
		The caller must be able to handle both cases (e.g. by ignoring additional
		items or initializing missing items with a default value).

		The iterator should always be exhausted when it is read, otherwise the
		stream will be in an undefined state.
		"""

		while True:
			typecode = self._nextchar()
			# We always "push back" the typecode we've read so that :meth:`load`
			# can treat both cases (i.e. whether :meth:`ul4onload` uses
			# :meth:`load` or :meth:`loadcontent`) the same way.
			self._bufferedchar = typecode
			if typecode == ")":
				break
			yield self.load()


class StreamBuffer:
	# Internal helper class that wraps a file-like object and provides buffering
	def __init__(self, stream, bufsize=1024*1024):
		self.stream = stream
		self.bufsize = bufsize
		self.buffer = ""

	def read(self, size):
		havesize = len(self.buffer)
		if havesize >= size:
			result = self.buffer[:size]
			self.buffer = self.buffer[size:]
			return result
		else:
			needsize = size-havesize
			newdata = self.stream.read(max(self.bufsize, needsize))
			result = self.buffer + newdata[:needsize]
			self.buffer = newdata[needsize:]
			return result


def dumps(obj, indent=None):
	"""
	Serialize :obj:`obj` as an UL4ON formatted string.
	"""
	stream = io.StringIO()
	Encoder(stream, indent=indent).dump(obj)
	return stream.getvalue()


def dump(obj, stream, indent=None):
	"""
	Serialize :obj:`obj` as an UL4ON formatted stream to :obj:`stream`.

	:obj:`stream` must provide a :meth:`write` method.
	"""
	Encoder(stream, indent=indent).dump(obj)


def loadclob(clob, bufsize=1024*1024, registry=None):
	"""
	Deserialize :obj:`clob` (which must be an :mod:`cx_Oracle` ``CLOB`` variable
	containing an UL4ON formatted object) to a Python object.

	:obj:`bufsize` specifies the chunk size for reading the underlying ``CLOB``
	object.

	For the meaning of :obj:`registry` see :meth:`Decoder.__init__`.
	"""
	return Decoder(StreamBuffer(clob, bufsize), registry).load()


def loads(string, registry=None):
	"""
	Deserialize :obj:`string` (which must be a string containing an UL4ON
	formatted object) to a Python object.

	For the meaning of :obj:`registry` see :meth:`Decoder.__init__`.
	"""
	return Decoder(io.StringIO(string), registry).load()


def load(stream, registry=None):
	"""
	Deserialize :obj:`stream` (which must be file-like object with a :meth:`read`
	method containing an UL4ON formatted object) to a Python object.

	For the meaning of :obj:`registry` see :meth:`Decoder.__init__`.
	"""
	return Decoder(stream, registry).load()
