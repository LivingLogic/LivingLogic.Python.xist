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
It is extensible to allow encoding/decoding arbitrary instances (i.e. it is
basically a reimplementation of :mod:`pickle`, but with string input/output
instead of bytes and with an eye towards cross-plattform support).

Example
-------

::

from ll import ul4on

@ul4on.register("com.example.person")
class Person:
	def __init__(self, firstname=None, lastname=None):
		self.firstname = firstname
		self.lastname = lastname

	def ul4ondump(self, encoder):
		encoder.dump(self.firstname)
		encoder.dump(self.lastname)

	def ul4onload(self, decoder)
		self.firstname = decoder.load()
		self.lastname = decoder.load()

otto = Person("Otto", "Normalverbraucher")


"""


import datetime, collections, io, contextlib

from ll import color, misc


_registry = {}


def register(name):
	"""
	This decorator can be used to register the decorated class with the
	:mod:`ll.ul4on` serialization machinery.

	:var:`name` must be a globally unique name for the class. To avoid
	name collisions Java's class naming system should be used (i.e. an
	inverted domain name like ``com.example.foo.bar``).

	:var:`name` will be stored in the class attribute ``ul4onname``.
	"""
	def registration(cls):
		cls.ul4onname = name
		_registry[name] = cls
		return cls
	return registration


class Encoder:
	def __init__(self, stream):
		"""
		Create an encoder for serializing objects to  :var:`self.stream`.

		:var:`stream` must provide a :meth:`write` method.
		"""
		self.stream = stream
		self._objects = []
		self._id2index = {}

	def _record(self, obj):
		# Record that we've written this object and in which position
		self._id2index[id(obj)] = len(self._objects)
		self._objects.append(obj)

	def dump(self, obj):
		"""
		Serialize :var:`obj` as an UL4ON formatted stream.
		"""
		# Have we written this object already?
		if id(obj) in self._id2index:
			# Yes: Store a backreference to the object
			self.stream.write("^{}|".format(self._id2index[id(obj)]))
		else:
			# No: Write the object itself
			# We're not using backreferences, if the object itself has a shorter dump
			if obj is None:
				self.stream.write("n")
			elif isinstance(obj, bool):
				self.stream.write("bT" if obj else "bF")
			elif isinstance(obj, int):
				self.stream.write("i{}|".format(obj))
			elif isinstance(obj, float):
				self.stream.write("f{!r}|".format(obj))
			elif isinstance(obj, str):
				self._record(obj)
				self.stream.write("S{}|".format(len(obj)))
				self.stream.write(obj)
			elif isinstance(obj, color.Color):
				self._record(obj)
				self.stream.write("C{:02x}{:02x}{:02x}{:02x}".format(obj.r(), obj.g(), obj.b(), obj.a()))
			elif isinstance(obj, datetime.datetime):
				self._record(obj)
				self.stream.write(obj.strftime("T%Y%m%d%H%M%S%f"))
			elif isinstance(obj, collections.Sequence):
				self._record(obj)
				self.stream.write("L")
				for item in obj:
					self.dump(item)
				self.stream.write(".")
			elif isinstance(obj, collections.Mapping):
				self._record(obj)
				self.stream.write("D")
				for (key, item) in obj.items():
					self.dump(key)
					self.dump(item)
				self.stream.write(".")
			else:
				self._record(obj)
				self.stream.write("O{}|".format(len(obj.ul4onname)))
				self.stream.write(obj.ul4onname)
				obj.ul4ondump(self)


class Decoder:
	def __init__(self, stream):
		"""
		Create a decoder for deserializing objects from  :var:`self.stream`.

		:var:`stream` must provide a :meth:`read` method.
		"""
		self.stream = stream
		self._objects = []
		self._keycache = {}

	def load(self):
		"""
		Deserialize the next object in the stream and return it.
		"""
		return self._load(None)

	def _readint(self):
		i = 0
		while True:
			c = self.stream.read(1)
			if c == "|":
				return i
			elif c.isdigit():
				i = 10*i+int(c)
			else:
				raise ValueError("broken stream: expected digit or '|', got {!r}".format(c))

	def _loading(self, obj):
		self._objects.append(obj)

	def _load(self, typecode):
		if typecode is None:
			typecode = self.stream.read(1)
		elif typecode == "^":
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
				raise ValueError("broken stream: expected 'T' or 'F' for bool; got {!r}".format(value))
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
				if c == "|":
					value = float("".join(chars))
					break
				else:
					chars.append(c)
			if typecode == "F":
				self._loading(value)
			return value
		elif typecode in "sS":
			size = self._readint()
			value = self.stream.read(size)
			if typecode == "S":
				self._loading(value)
			return value
		elif typecode in "cC":
			data = self.stream.read(8)
			value = color.Color(*(int(x, 16) for x in misc.itersplitat(data, (2, 4, 6))))
			if typecode == "C":
				self._loading(value)
			return value
		elif typecode in "tT":
			data = self.stream.read(20)
			value = datetime.datetime(*map(int, misc.itersplitat(data, (4, 6, 8, 10, 12, 14))))
			if typecode == "T":
				self._loading(value)
			return value
		elif typecode in "lL":
			value = []
			if typecode == "L":
				self._loading(value)
			while True:
				c = self.stream.read(1)
				if c == ".":
					return value
				else:
					item = self._load(c)
					value.append(item)
		elif typecode in "dD":
			value = {}
			if typecode == "D":
				self._loading(value)
			while True:
				c = self.stream.read(1)
				if c == ".":
					return value
				else:
					key = self._load(c)
					if key in keys:
						key = self._keycache[key]
					else:
						self._keycache[key] = key
					item = self._load(None)
					value[key] = item
		elif typecode in "oO":
			size = self._readint()
			name = self.stream.read(size)
			try:
				cls = _registry[name]
			except KeyError:
				raise TypeError("can't decode object of type {}".format(name))
			obj = cls()
			if typecode == "O":
				self._loading(obj)
			obj.ul4onload(self)
			return obj
		else:
			raise ValueError("broken stream: unknown typecode {!r}".format(typecode))


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


def dumps(obj):
	"""
	Serialize :var:`obj` as an UL4ON formatted string.
	"""
	stream = io.StringIO()
	Encoder(stream).dump(obj)
	return stream.getvalue()


def dump(obj, stream):
	"""
	Serialize :var:`obj` as an UL4ON formatted stream to :var:`stream`.

	:var:`stream` must provide a :meth:`write` method.
	"""
	Encoder(stream).dump(obj)


def loadclob(clob, bufsize=1024*1024):
	"""
	Deserialize :var:`clob` (which must be an :mod:`cx_Oracle` ``CLOB`` variable
	containing an UL4ON formatted object) to a Python object.

	:var:`bufsize` specifies the chunk size for reading the underlying ``CLOB``
	object.
	"""
	return Decoder(StreamBuffer(clob, bufsize)).load()


def loads(string):
	"""
	Deserialize :var:`string` (which must be a string containing an UL4ON
	formatted object) to a Python object.
	"""
	return Decoder(io.StringIO(string)).load()


def load(stream):
	"""
	Deserialize :var:`stream` (which must be file-like object with a :meth:`read`
	method containing an UL4ON formatted object) to a Python object.
	"""
	return Decoder(stream).load()
