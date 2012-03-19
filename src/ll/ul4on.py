#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2011-2012 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2011-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
This module provides functions for encoding and decoding a lightweight
machine-readable format for serializing the object types supported by UL4.

It provides an API similar to that of the modules :mod:`pickle` and :mod:`json`
from the standard library.
"""


import datetime, collections, io, contextlib

from ll import color, misc, ul4c


def iterdump(obj):
	"""
	Return an iterator that provides a piecewise serialization of :var:`obj`
	into the UL4ON format.
	"""
	if obj is None:
		yield "n"
	elif isinstance(obj, bool):
		yield "bT" if obj else "bF"
	elif isinstance(obj, int):
		yield "i{}|".format(obj)
	elif isinstance(obj, float):
		yield "f{!r}|".format(obj)
	elif isinstance(obj, str):
		yield "s{}|".format(len(obj))
		yield obj
	elif isinstance(obj, color.Color):
		yield "c{:02x}{:02x}{:02x}{:02x}".format(obj.r(), obj.g(), obj.b(), obj.a())
	elif isinstance(obj, datetime.datetime):
		yield obj.strftime("d%Y%m%d%H%M%S%f")
	elif isinstance(obj, ul4c.Template):
		output = obj.dumps()
		yield "t{}|".format(len(output))
		yield output
	elif isinstance(obj, collections.Sequence):
		yield "["
		for item in obj:
			for output in iterdump(item):
				yield output
		yield "]"
	elif isinstance(obj, collections.Mapping):
		yield "{"
		for (key, item) in obj.items():
			for output in iterdump(key):
				yield output
			for output in iterdump(item):
				yield output
		yield "}"


def dumps(obj):
	"""
	Serialize :var:`obj` as an UL4ON formatted string.
	"""
	return "".join(iterdump(obj))


def dump(obj, stream):
	"""
	Serialize :var:`obj` as an UL4ON formatted stream to :var:`stream`.

	:var:`stream` must provide a :meth:`write` method.
	"""
	for part in iterdump(obj):
		stream.write(part)


def _readint(stream):
	i = 0
	while True:
		c = stream.read(1)
		if c == "|":
			return i
		elif c.isdigit():
			i = 10*i+int(c)
		else:
			raise ValueError("broken stream: expected digit or '|', got {!r}".format(c))


def _load(stream, typecode, keys):
	if typecode is None:
		typecode = stream.read(1)
	if typecode == "n":
		return None
	elif typecode == "b":
		value = stream.read(1)
		if value == "T":
			return True
		elif value == "F":
			return False
		else:
			raise ValueError("broken stream: expected 'T' or 'F' for bool; got {!r}".format(value))
	elif typecode == "i":
		return _readint(stream)
	elif typecode == "f":
		chars = []
		while True:
			c = stream.read(1)
			if c == "|":
				return float("".join(chars))
			else:
				chars.append(c)
	elif typecode == "s":
		size = _readint(stream)
		return stream.read(size)
	elif typecode == "c":
		data = stream.read(8)
		return color.Color(*(int(x, 16) for x in misc.itersplitat(data, (2, 4, 6))))
	elif typecode == "d":
		data = stream.read(20)
		return datetime.datetime(*map(int, misc.itersplitat(data, (4, 6, 8, 10, 12, 14))))
	elif typecode == "t":
		size = _readint(stream)
		data = stream.read(size)
		return ul4c.Template.loads(data)
	elif typecode == "[":
		data = []
		while True:
			c = stream.read(1)
			if c == "]":
				return data
			else:
				item = _load(stream, c, keys)
				data.append(item)
	elif typecode == "{":
		data = {}
		while True:
			c = stream.read(1)
			if c == "}":
				return data
			else:
				key = _load(stream, c, keys)
				if key in keys:
					key = keys[key]
				else:
					keys[key] = key
				item = _load(stream, None, keys)
				data[key] = item
	else:
		raise ValueError("broken stream: unknown typecode {!r}".format(typecode))


class Encoder(object):
	"""
	An :class:`Encoder` object can be used to write list or dictionaries to a
	stream incrementally.
	"""
	def __init__(self, stream):
		"""
		Create an :class:`Encoder` object for writing to the file-like object
		:var:`stream` incrementally. :var:`stream` will be available as the
		instance attribute with the same name.
		"""
		self.stream = stream

	def write(self, obj):
		"""
		Write the object :var:`obj` to the stream
		"""
		dump(obj, self.stream)

	@contextlib.contextmanager
	def list(self):
		"""
		This methods is a context manager and can be used for outputting a list incrementally
		like this::

			enc = ul4on.Encoder(io.StringIO())

			with enc.list():
				for i in range(10):
					enc.write(i)

		This is equivalent to::

			enc.write(range(10))
		"""
		self.stream.write("[")
		yield
		self.stream.write("]")

	@contextlib.contextmanager
	def dict(self):
		"""
		This methods is a context manager and can be used for outputting a dict incrementally
		like this::

			enc = ul4on.Encoder(io.StringIO())

			with enc.dict():
				enc.write("eins")
				enc.write(1)
				enc.write("zwei")
				enc.write(2)
				enc.write("drei")
				enc.write(3)

		This is equivalent to::

			enc.write(dict(eins=1, zwei=2, drei=3))
		"""
		self.stream.write("{")
		yield
		self.stream.write("}")

	def getvalue(self):
		"""
		If the wrapped stream is a :class:`StringIO` stream :meth:`getvalue` can be used
		to get the content of the stream.
		"""
		return self.stream.getvalue()


class StreamBuffer(object):
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


def loadclob(clob, bufsize=1024*1024):
	"""
	Deserialize :var:`clob` (which must be an :mod:`cx_Oracle` ``CLOB`` variable
	containing an UL4ON formatted object) to a Python object.

	:var:`bufsize` specifies the chunk size for reading the underlying ``CLOB``
	object.
	"""
	return _load(StreamBuffer(clob, bufsize), None, {})


def loads(string):
	"""
	Deserialize :var:`string` (which must be a string containing an UL4ON
	formatted object) to a Python object.
	"""
	return _load(io.StringIO(string), None, {})


def load(stream):
	"""
	Deserialize :var:`stream` (which must be file-like object with a :meth:`read`
	method containing an UL4ON formatted object) to a Python object.
	"""
	return _load(stream, None, {})
