# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2011-2025 by LivingLogic AG, Bayreuth/Germany
## Copyright 2011-2025 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


r'''
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

:class:`~datetime.date`, :class:`~datetime.datetime` and
:class:`~datetime.timedelta` objects are supported too::

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

:mod:`!ll.ul4on` also supports :class:`~ll.color.Color` objects from
:mod:`ll.color`::

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


Recursive data structures
-------------------------

:mod:`!ll.ul4on` can also handle recursive data structures::

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

.. note::
	The ``^0`` part in the dump is a so called "back reference", it tells the
	decoder that in this spot an object is referenced that has already been part
	of the dump (The ``0`` indicates where in the dump the object can be found).


Extensibility
-------------

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

This script outputs:

.. sourcecode:: output

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

	For deserialization the class **must** be registered either in the local
	registry passed to the :class:`Decoder` or globally via :func:`register`.


Object content mismatch
-----------------------

In situations where an UL4ON API is updated frequently it is useful to be able
to update the writing side and the reading side independently. To support this,
:class:`Decoder` has a method :meth:`~Decoder.loadcontent` that is a generator
that reads the content items of an object from the input stream and yields those
items.

This allows to handle both situations:

*	When the writing side outputs more items that the reading side expects,
	exhausting the iterator returned by :meth:`~loadcontent` will read and
	ignore the unrecognized items and leave the input stream in a consistent
	state.

*	When the writing side outputs less items then the reading side expects,
	the remaining items can by initialized with default values.

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

This outputs:

.. sourcecode:: output

	Loaded: <Person firstname='John' lastname=None>


Chunked UL4ON
-------------

:mod:`!ll.ul4on` also provides access to the classes that implement UL4ON
encoding and decoding. This can be used to create multiple UL4ON dumps using the
same encoding context, or recreate multiple objects from those multiple UL4ON
dumps (using the same decoding context).

An example for encoding::

	encoder = ul4on.Encoder()
	obj = "spam"
	print(encoder.dumps(obj))
	print(encoder.dumps(obj))

This prints:

.. sourcecode:: output

	S'spam'
	^0

The second call outputs a back reference, since the encoder remembers that the
string ``"spam"`` has already been output.

An example for decoding::

	decoder = ul4on.Decoder()
	print(decoder.loads("S'spam'"))
	print(decoder.loads("^0"))

This prints:

.. sourcecode:: output

	spam
	spam

since the decoder remembers which object has been decoded as the first object
from the first dump.

One application of this is embedding multiple related UL4ON dumps as data
attributes in HTML and then deserializing those UL4ON chuncks back into the
appropriate Javascript objects. For example::

	from ll import ul4on
	from ll.misc import xmlencode as xe

	encoder = ul4on.Encoder()

	counter = 0

	def dump(obj):
		global counter
		counter += 1
		return f"{counter} {encoder.dumps(obj)}"

	data = ["gurk", "hurz", "hinz", "kunz"]

	def f(s):
		return f"<li data-ul4on='{xe(dump(s))}'>{xe(s.upper())}</li>"

	items = "\n".join(f(s) for s in data)
	html = f"<ul data-ul4on='{xe(dump(data))}'>\n{items}\n</ul>"
	print(html)

This outputs:

.. sourcecode:: xml

	<ul data-ul4on='5 L ^0 ^1 ^2 ^3 ]'>
	<li data-ul4on='1 S&#39;gurk&#39;'>GURK</li>
	<li data-ul4on='2 S&#39;hurz&#39;'>HURZ</li>
	<li data-ul4on='3 S&#39;hinz&#39;'>HINZ</li>
	<li data-ul4on='4 S&#39;kunz&#39;'>KUNZ</li>
	</ul>

By iterating through the ``data-ul4on`` attributes in the correct order and
feeding each UL4ON chunk to the same decoder, all objects can be recreated and
attached to their appropriate HTML elements.


Incremental UL4ON and persistent objects
----------------------------------------

Objects that have an attribute ``ul4onid`` are considered "persistent" objects.
The combination of ``ul4onname`` and ``ul4onid`` uniquely identifies each
persistent object (even across multiple unrelated UL4ON dumps).

An :class:`Encoder` will dump those objects differently than other objects
without an ``ul4onid`` attribute.

A :class:`Decoder` will remember all persistent objects it has loaded
(under their ``ul4onname`` and ``ul4onid``). If the decoder encounters the
``ul4onname`` and ``ul4onid`` of an object it has remembered, it will not create
a new object, instead :meth:`ul4onload` will be called for the existing object.
If the decoder encounters a persistent objects it hasn't remembered, it will
create a new object (passing the ``ul4onid`` as the only argument to the
constructor) and then call :meth:`ul4onload` on the new object.

This means that with this approach it's possible to use one :class:`Decoder`
object to load multiple unrelated UL4ON dumps "incrementally" one after the
other, but still merge the persistent objects in the subsequent dumps into the
those created by previous dumps.

.. note::
	For persistent objects :meth:`ul4onload` and :meth:`ul4ondump` don't have
	the dump/load the ``ul4onid`` attribute, as this is done by the
	:class:`Encoder`/:class:`Decoder`.

.. note::
	If the value of the attribute ``ul4onid`` is :const:`None` the object will
	be treated as an "ordinary" (i.e. non-persistent) object.

.. note::
	For this approach, the method :meth:`~Decoder.reset` must be called between
	calls to :meth:`~Decoder.load` or :meth:`~Decoder.loads` to reset the
	information about back references.


Module documentation
--------------------
'''

from typing import *
from typing import TextIO

import datetime, collections, io
from collections import abc


__docformat__ = "reStructuredText"


_registry = {}


def register(name : str):
	"""
	This decorator can be used to register the decorated class with the
	:mod:`!ll.ul4on` serialization machinery.

	``name`` must be a globally unique name for the class. To avoid
	name collisions Java's class naming system should be used (i.e. an
	inverted domain name like ``com.example.foo.bar``).

	``name`` will be stored in the class attribute ``ul4onname``.
	"""
	def registration(cls):
		cls.ul4onname = name
		_registry[name] = cls
		return cls
	return registration


from ll import ul4c


class Encoder:
	"""
	An :class:`Encoder` is used for serializing an object into an UL4ON dump.

	It manages the internal state required for handling backreferences and other
	stuff.
	"""
	ul4_type = ul4c.InstantiableType("ul4on", "Encoder", "An Encoder is used for serializing an object into an UL4ON dump.")
	ul4_attrs = {"dumps"}

	def __init__(self, indent:str=None):
		"""
		Create an encoder for serializing objects.

		When ``indent`` is not :const:`None`, it is used as an indentation string
		for pretty printing the output.
		"""
		self.stream = None # type: Optional[TextIO]
		self._level = 0
		self.indent = indent
		self._lastwaslf = False
		# Remember whether we have dumped something into the stream (so we have to write separator whitespace/indentation) or not
		self._first = True
		# Objects that are available for back references (using the position in the list)
		self._objects = [] # type: List[Any]
		# Maps object ids to their position in ``_objects``
		self._id2index = {} # type: Dict[int, int]

	def _record(self, obj:Any) -> None:
		# Record that we've written this object and in which position
		self._id2index[id(obj)] = len(self._objects)
		self._objects.append(obj)

	def _line(self, line:str, *items:Any):
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

	def dumps(self, obj:Any) -> str:
		"""
		Serialize ``obj`` and return the resulting dump as a string.
		"""

		self.stream = io.StringIO()
		self._level = 0
		self._lastwaslf = False
		self._first = True
		self.dump(obj)
		result = self.stream.getvalue()
		self.stream = None
		return result

	def dump(self, obj:Any, stream:Optional[TextIO]=None) -> None:
		"""
		Serialize ``obj`` into the stream ``stream`` as an UL4ON formatted dump.

		``stream`` must provide a :meth:`!write` method.

		Passing :const:`None` for ``stream`` may only be done by objects that
		call :meth:`!dump` to implement UL4ON serialization in their
		own :meth:`ul4ondump` method.
		"""
		if stream is not None:
			self.stream = stream
			self._level = 0
			self._lastwaslf = False
			self._first = True

		# Have we written this object already?
		if id(obj) in self._id2index:
			# Yes: Store a backreference to the object
			index = self._id2index[id(obj)]
			self._line(f"^{index}")
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
				ul4onid = getattr(obj , "ul4onid", None)
				self._record(obj)
				if ul4onid is not None:
					self._line("P", obj.ul4onname, obj.ul4onid)
				else:
					self._line("O", obj.ul4onname)
				self._level += 1
				obj.ul4ondump(self)
				self._level -= 1
				self._line(")")
		if stream is not None:
			self.stream = None


class Decoder:
	"""
	A :class:`Decoder` is used for deserializing an UL4ON dump.

	It manages the internal state required for handling backreferences,
	persistent objects and other stuff.
	"""
	ul4_type = ul4c.InstantiableType("ul4on", "Decoder", "A Decoder is used for deserializing an UL4ON dump.")
	ul4_attrs = {"loads", "reset"}

	def __init__(self, registry:Optional[Dict[str, Callable[..., Any]]]=None):
		"""
		Create a decoder for deserializing objects from an UL4ON dump.

		``registry`` is used as a "custom type registry". It must map UL4ON
		type names to callables that create new empty instances of those types.
		Any type not found in ``registry`` will be looked up in the global
		registry (see :func:`register`).
		"""
		self.stream = None # type: Optional[TextIO]
		# Next character to be read by :meth:`_nextchar`
		self._bufferedchar = None # type: Optional[str]
		self._objects = [] # type: List[Any]
		self._persistent_objects = {} # type: Dict[Tuple[str, str], Any]
		# Used for "interning" dictionary keys
		self._keycache = {} # type: Dict[str, str]
		self.registry = registry
		# A stack of types that are currently in the process of being decoded (used in exception messages)
		self._stack = None # type: Optional[List[Any]]

	def loads(self, dump:str) -> Any:
		"""
		Deserialize the object in the string ``dump`` and return it.
		"""

		return self.load(io.StringIO(dump))

	def load(self, stream:Optional[TextIO]=None) -> Any:
		"""
		Deserialize the next object from the stream ``stream`` and return it.

		``stream`` must provide a :meth:`!read` method.

		Passing :const:`None` for ``stream`` may only be done by objects that
		call :meth:`!load` to implement UL4ON deserialization in their
		own :meth:`ul4onload` method.
		"""
		if stream is not None:
			self.stream = stream
			self._stack = []
			self._bufferedchar = None

		typecode = self._nextchar()
		if typecode == "^":
			position = self._readint()
			value = self._objects[position]
		elif typecode in "nN":
			if typecode == "N":
				self._loading(None)
			value = None
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
		elif typecode in "iI":
			value = self._readint()
			if typecode == "I":
				self._loading(value)
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
		elif typecode in "sS":
			delimiter = self.stream.read(1)
			if not delimiter:
				raise EOFError()
			buffer = io.StringIO()
			while True:
				c = self.stream.read(1)
				if not c:
					raise EOFError()
				if c == delimiter:
					value = buffer.getvalue().encode("ascii", "backslashreplace").decode("unicode_escape")
					break
				buffer.write(c)
				if c == "\\":
					c2 = self.stream.read(1)
					if not c2:
						raise EOFError()
					buffer.write(c2)
			if typecode == "S":
				self._loading(value)
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
		elif typecode in "xX":
			if typecode == "X":
				oldpos = self._beginfakeloading()
			year = self.load()
			month = self.load()
			day = self.load()
			value = datetime.date(year, month, day)
			if typecode == "X":
				self._endfakeloading(oldpos, value)
		elif typecode in "rR":
			if typecode == "R":
				oldpos = self._beginfakeloading()
			start = self.load()
			stop = self.load()
			value = slice(start, stop)
			if typecode == "R":
				self._endfakeloading(oldpos, value)
		elif typecode in "tT":
			if typecode == "T":
				oldpos = self._beginfakeloading()
			days = self.load()
			seconds = self.load()
			microseconds = self.load()
			value = datetime.timedelta(days, seconds, microseconds)
			if typecode == "T":
				self._endfakeloading(oldpos, value)
		elif typecode in "mM":
			from ll import misc
			if typecode == "M":
				oldpos = self._beginfakeloading()
			months = self.load()
			value = misc.monthdelta(months)
			if typecode == "M":
				self._endfakeloading(oldpos, value)
		elif typecode in "lL":
			self._stack.append("list")
			value = []
			if typecode == "L":
				self._loading(value)
			while True:
				typecode = self._nextchar()
				if typecode == "]":
					self._stack.pop()
					break
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
					break
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
					break
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
		elif typecode in "pP":
			if typecode == "P":
				oldpos = self._beginfakeloading()
			name = self.load()
			id = self.load()
			self._stack.append(f"{name}={id}")
			try:
				value = self._persistent_objects[(name, id)]
			except KeyError:
				cls = None
				if self.registry is not None:
					cls = self.registry.get(name)
				if cls is None:
					cls = _registry.get(name)
				if cls is None:
					raise TypeError(f"broken UL4ON stream at position {self.stream.tell():,} (path {self._path()}): can't decode object of type {name!r} with id {id!r}") from None
				value = cls(id)
				self._persistent_objects[(name, id)] = value
			if typecode == "P":
				self._endfakeloading(oldpos, value)
			value.ul4onload(self)
			typecode = self._nextchar()
			if typecode != ")":
				raise ValueError(f"broken UL4ON stream at position {self.stream.tell():,} (path {self._path()}): object terminator ')' expected, got {typecode!r}")
			self._stack.pop()
		else:
			raise ValueError(f"broken UL4ON stream at position {self.stream.tell():,} (path {self._path()}): unknown typecode {typecode!r}")

		if stream is not None:
			self.stream = None
			self._stack = None
		return value

	def loadcontent(self) -> Generator[Any, None, None]:
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
			# can treat all cases (i.e. whether :meth:`ul4onload` uses :meth:`load`
			# :meth:`loadcontent` or  :meth:`loadcontentitems`) the same way.
			self._bufferedchar = typecode
			if typecode == ")":
				break
			yield self.load()

	def loadcontentitems(self) -> Generator[Tuple[str, Any], None, None]:
		"""
		Similar to :meth:`loadcontent`, but will load the content of an object as
		(key, value) pairs.

		For further info see :meth:`loadcontent`.
		"""

		while True:
			typecode = self._nextchar()
			# We always "push back" the typecode we've read so that :meth:`load`
			# can treat all cases (i.e. whether :meth:`ul4onload` uses :meth:`load`
			# :meth:`loadcontent` or  :meth:`loadcontentitems`) the same way.
			self._bufferedchar = typecode
			if typecode == ")":
				break
			key = self.load()
			value = self.load()
			yield (key, value)

	def reset(self) -> None:
		"""
		Clear the internal cache for backreferences so that a new unrelated
		UL4ON dump can be loaded.

		However the cache for persistent objects will not be cleared.
		"""
		self._objects.clear()

	def store_persistent_object(self, object) -> None:
		"""
		Add a persistent object to the cache of persistent objects.
		"""
		self._persistent_objects[(object.ul4onname, object.ul4onid)] = object

	def forget_persistent_object(self, object) -> None:
		"""
		Remove a persistent object from the cache of persistent objects.
		"""
		try:
			del self._persistent_objects[(object.ul4onname, object.ul4onid)]
		except KeyError:
			pass

	def persistent_object(self, name:str, id:str) -> Any:
		"""
		Return the persistent object with the type ``name`` and the id ``id``,
		or :const:`None`, when the decoder hasn't encountered that object yet.
		"""
		return self._persistent_objects.get((name, id), None)

	def persistent_objects(self) -> ValuesView[Any]:
		"""
		Return an iterator over all persistent objects the decoder has encountered
		so far.
		"""
		return self._persistent_objects.values()

	def _readint(self) -> int:
		buffer = io.StringIO()
		while True:
			c = self.stream.read(1)
			if c and not c.isspace():
				buffer.write(c)
			else:
				return int(buffer.getvalue())

	def _loading(self, obj) -> None:
		self._objects.append(obj)

	def _nextchar(self) -> str:
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

	def _path(self) -> str:
		return "/".join(self._stack)

	def _beginfakeloading(self) -> int:
		# For loading custom object or immutable objects that have attributes we have a problem:
		# We have to record the object we're loading *now*, so that it is available for backreferences.
		# However until we've read the UL4ON name of the class (for custom object) or the attributes
		# of the object (for immutable objects with attributes), we can't create the object.
		# So we push :const:`None` to the backreference list for now and put the right object in this spot,
		# once we've created it (via :meth:`_endfakeloading`). This shouldn't lead to problems,
		# because during the time the backreference is wrong, only the class name is read,
		# so our object won't be referenced. For immutable objects the attributes normally
		# don't reference the object itself.
		oldpos = len(self._objects)
		self._loading(None)
		return oldpos

	def _endfakeloading(self, oldpos, value) -> None:
		# Fix backreference in object list
		self._objects[oldpos] = value


def dumps(obj:Any, /, indent:Optional[str]=None) -> str:
	"""
	Serialize ``obj`` as an UL4ON formatted string.
	"""
	stream = io.StringIO()
	Encoder(indent=indent).dump(obj, stream)
	return stream.getvalue()


def dump(obj:Any, /, stream:TextIO, indent:Optional[str]=None) -> None:
	"""
	Serialize ``obj`` as an UL4ON formatted stream to ``stream``.

	``stream`` must provide a :meth:`write` method.
	"""
	Encoder(indent=indent).dump(obj, stream)


def load(stream:TextIO, /, registry:Optional[Dict[str, Callable[..., Any]]]=None) -> Any:
	"""
	Deserialize ``stream`` (which must be file-like object with a :meth:`read`
	method containing an UL4ON formatted object) to a Python object.

	For the meaning of ``registry`` see :meth:`Decoder.__init__`.
	"""
	return Decoder(registry).load(stream)


def loads(dump:str, /, registry:Optional[Dict[str, Callable[..., Any]]]=None) -> Any:
	"""
	Deserialize ``dump`` (which must be a string containing an UL4ON
	formatted object) to a Python object.

	For the meaning of ``registry`` see :meth:`Decoder.__init__`.
	"""
	return Decoder(registry).loads(dump)


def loadclob(clob, /, bufsize:int=1024*1024, registry:Optional[Dict[str, Callable[..., Any]]]=None) -> Any:
	"""
	Deserialize ``clob`` (which must be an :mod:`cx_Oracle` ``CLOB`` variable
	containing an UL4ON formatted object) to a Python object.

	``bufsize`` specifies the chunk size for reading the underlying ``CLOB``
	object.

	For the meaning of ``registry`` see :meth:`Decoder.__init__`.
	"""
	return Decoder(registry).load(StreamBuffer(clob, bufsize))


class StreamBuffer:
	# Internal helper class that wraps a file-like object and provides buffering
	def __init__(self, stream, bufsize:int=1024*1024):
		self.stream = stream
		self.bufsize = bufsize
		self.buffer = ""

	def read(self, size:int) -> AnyStr:
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
