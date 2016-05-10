# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2011-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2011-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
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
UL4on encoded data.

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

:class:`datetime` and :class:`timedelta` objects are supported too::

	>>> import datetime
	>>> ul4on.dumps(datetime.datetime.now())
	'Z i2014 i11 i3 i18 i16 i45 i314157'
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
			return "<Person firstname={!r} lastname={!r}>".format(self.firstname, self.lastname)

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
"""

import datetime, collections, io, ast


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
		Serialize :obj:`obj` as an UL4ON formatted stream.
		"""
		# Have we written this object already?
		if id(obj) in self._id2index:
			# Yes: Store a backreference to the object
			self._line("^{}".format(self._id2index[id(obj)]))
		else:
			from ll import ul4c, color, misc
			# No: Write the object itself
			# We're not using backreferences if the object itself has a shorter dump
			if obj is None:
				self._line("n")
			elif isinstance(obj, bool):
				self._line("bT" if obj else "bF")
			elif isinstance(obj, int):
				self._line("i{}".format(obj))
			elif isinstance(obj, float):
				self._line("f{!r}".format(obj))
			elif isinstance(obj, str):
				self._record(obj)
				self._line("S{!r}".format(obj))
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
				self._line("Z", obj.year, obj.month, obj.day, 0, 0, 0, 0)
			elif isinstance(obj, datetime.timedelta):
				self._record(obj)
				self._line("T", obj.days, obj.seconds, obj.microseconds)
			elif isinstance(obj, misc.monthdelta):
				self._record(obj)
				self._line("M", obj.months())
			elif isinstance(obj, collections.Sequence):
				self._record(obj)
				self._line("L")
				self._level += 1
				for item in obj:
					self.dump(item)
				self._level -= 1
				self._line("]")
			elif isinstance(obj, collections.Mapping):
				self._record(obj)
				self._line("D")
				self._level += 1
				for (key, item) in obj.items():
					self.dump(key)
					self.dump(item)
				self._level -= 1
				self._line("}")
			elif isinstance(obj, collections.Set):
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
	def __init__(self, stream):
		"""
		Create a decoder for deserializing objects from  :obj:`self.stream`.

		:obj:`stream` must provide a :meth:`read` method.
		"""
		self.stream = stream
		self._objects = []
		self._keycache = {} # Used for "interning" dictionary keys

	def load(self):
		"""
		Deserialize the next object in the stream and return it.
		"""
		return self._load(None)

	def _readint(self):
		buffer = []
		while True:
			c = self.stream.read(1)
			if c and not c.isspace():
				buffer.append(c)
			else:
				return int("".join(buffer))

	def _loading(self, obj):
		self._objects.append(obj)

	def _nextchar(self, nextchar=None):
		while True:
			nextchar = self.stream.read(1)
			if nextchar:
				if not nextchar.isspace():
					return nextchar
			else:
				raise EOFError()

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

	def _load(self, typecode):
		from ll import misc
		if typecode is None:
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
				raise ValueError("broken UL4ON stream at position {}: expected 'T' or 'F' for bool; got {!r}".format(self.stream.tell(), value))
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
			buffer = [delimiter]
			while True:
				c = self.stream.read(1)
				if not c:
					raise EOFError()
				buffer.append(c)
				if c == delimiter:
					value = ast.literal_eval("".join(buffer))
					break
				elif c == "\\":
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
			r = self._load(None)
			g = self._load(None)
			b = self._load(None)
			a = self._load(None)
			value = color.Color(r, g, b, a)
			if typecode == "C":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "zZ":
			if typecode == "Z":
				oldpos = self._beginfakeloading()
			year = self._load(None)
			month = self._load(None)
			day = self._load(None)
			hour = self._load(None)
			minute = self._load(None)
			second = self._load(None)
			microsecond = self._load(None)
			value = datetime.datetime(year, month, day, hour, minute, second, microsecond)
			if typecode == "Z":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "rR":
			if typecode == "R":
				oldpos = self._beginfakeloading()
			start = self._load(None)
			stop = self._load(None)
			value = slice(start, stop)
			if typecode == "R":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "tT":
			if typecode == "T":
				oldpos = self._beginfakeloading()
			days = self._load(None)
			seconds = self._load(None)
			microseconds = self._load(None)
			value = datetime.timedelta(days, seconds, microseconds)
			if typecode == "T":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "mM":
			from ll import misc
			if typecode == "M":
				oldpos = self._beginfakeloading()
			months = self._load(None)
			value = misc.monthdelta(months)
			if typecode == "M":
				self._endfakeloading(oldpos, value)
			return value
		elif typecode in "lL":
			value = []
			if typecode == "L":
				self._loading(value)
			while True:
				typecode = self._nextchar()
				if typecode == "]":
					return value
				else:
					item = self._load(typecode)
					value.append(item)
		elif typecode in "dD":
			value = {}
			if typecode == "D":
				self._loading(value)
			while True:
				typecode = self._nextchar()
				if typecode == "}":
					return value
				else:
					key = self._load(typecode)
					if isinstance(key, str):
						if key in self._keycache:
							key = self._keycache[key]
						else:
							self._keycache[key] = key
					item = self._load(None)
					value[key] = item
		elif typecode in "yY":
			value = set()
			if typecode == "Y":
				self._loading(value)
			while True:
				typecode = self._nextchar()
				if typecode == "}":
					return value
				else:
					item = self._load(typecode)
					value.add(item)
		elif typecode in "oO":
			if typecode == "O":
				oldpos = self._beginfakeloading()
			name = self._load(None)
			try:
				cls = _registry[name]
			except KeyError:
				raise TypeError("can't decode object of type {}".format(name))
			value = cls()
			if typecode == "O":
				self._endfakeloading(oldpos, value)
			value.ul4onload(self)
			typecode = self._nextchar()
			if typecode != ")":
				raise ValueError("broken UL4ON stream at position {}: object terminator ')' expected, got {!r}".format(self.stream.tell(), typecode))
			return value
		else:
			raise ValueError("broken UL4ON stream at position {}: unknown typecode {!r}".format(self.stream.tell(), typecode))


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


def loadclob(clob, bufsize=1024*1024):
	"""
	Deserialize :obj:`clob` (which must be an :mod:`cx_Oracle` ``CLOB`` variable
	containing an UL4ON formatted object) to a Python object.

	:obj:`bufsize` specifies the chunk size for reading the underlying ``CLOB``
	object.
	"""
	return Decoder(StreamBuffer(clob, bufsize)).load()


def loads(string):
	"""
	Deserialize :obj:`string` (which must be a string containing an UL4ON
	formatted object) to a Python object.
	"""
	return Decoder(io.StringIO(string)).load()


def load(stream):
	"""
	Deserialize :obj:`stream` (which must be file-like object with a :meth:`read`
	method containing an UL4ON formatted object) to a Python object.
	"""
	return Decoder(stream).load()
