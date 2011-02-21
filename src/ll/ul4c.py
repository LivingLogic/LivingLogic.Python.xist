# -*- coding: utf-8 -*-

## Copyright 2009-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
:mod:`ll.ul4c` provides templating for XML/HTML as well as any other text-based
format. A template defines placeholders for data output and basic logic (like
loops and conditional blocks), that define how the final rendered output will
look.

:mod:`ll.ul4c` compiles a template to a bytecode format, which makes it possible
to implement template renderers in multiple programming languages.
"""

from __future__ import division

__docformat__ = "reStructuredText"


import re, datetime, StringIO, locale, json, collections

from ll import spark, color, misc


# Regular expression used for splitting dates in isoformat
datesplitter = re.compile("[-T:.]")


###
### Location information
###

class Location(object):
	"""
	A :class:`Location` object contains information about the location of a
	template tag.
	"""
	__slots__ = ("source", "type", "starttag", "endtag", "startcode", "endcode")

	def __init__(self, source, type, starttag, endtag, startcode, endcode):
		"""
		Create a new :class:`Location` object. The arguments have the following
		meaning:

		:var:`source`
			The complete source string

		:var:`type`
			The tag type (i.e. ``"for"``, ``"if"``, etc. or ``None`` for literal
			text)

		:var:`starttag`
			The start position of the start delimiter.

		:var:`endtag`
			The end position of the end delimiter.

		:var:`startcode`
			The start position of the tag code.

		:var:`endcode`
			The end position of the tag code.
		"""
		self.source = source
		self.type = type
		self.starttag = starttag
		self.endtag = endtag
		self.startcode = startcode
		self.endcode = endcode

	def __getitem__(self, key):
		if key in {"type", "starttag", "endtag", "startcode", "endcode"}:
			return getattr(self, key)
		raise KeyError(key)

	@property
	def code(self):
		return self.source[self.startcode:self.endcode]

	@property
	def tag(self):
		return self.source[self.starttag:self.endtag]

	def __repr__(self):
		return "<{}.{} {} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self, id(self))

	def pos(self):
		lastlinefeed = self.source.rfind("\n", 0, self.starttag)
		if lastlinefeed >= 0:
			return (self.source.count("\n", 0, self.starttag)+1, self.starttag-lastlinefeed)
		else:
			return (1, self.starttag + 1)

	def __str__(self):
		(line, col) = self.pos()
		return "{!r} at {} (line {}, col {})".format(self.tag, self.starttag+1, line, col)


###
### Exceptions
###

class Error(Exception):
	"""
	Exception class that wraps another exception and provides a location.
	"""
	def __init__(self, location):
		self.location = location
		self.__cause__ = None

	def __repr__(self):
		return "<{}.{} in {} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.location, id(self))

	def __str__(self):
		path = []

		exc = self
		while isinstance(exc, Error):
			if not path or path[-1] is not exc.location:
				path.append(exc.location)
			exc = exc.__cause__
		name = exc.__class__.__name__
		module = exc.__class__.__module__
		if module != "exceptions":
			name = "{}.{}".format(module, name)
		return "{} {} {}".format(name, " ".join("in {}:".format(location) for location in path), exc)


class LexicalError(Exception):
	def __init__(self, start, end, input):
		self.start = start
		self.end = end
		self.input = input

	def __str__(self):
		return "Unmatched input {!r}".format(self.input)


class SyntaxError(Exception):
	def __init__(self, token):
		self.token = token

	def __str__(self):
		return "Lexical error near {!r}".format(str(self.token))


class UnterminatedStringError(Exception):
	"""
	Exception that is raised by the parser when a string constant is not
	terminated.
	"""
	def __str__(self):
		return "Unterminated string"


class BlockError(Exception):
	"""
	Exception that is raised by the compiler when an illegal block structure is
	detected (e.g. an ``endif`` without a previous ``if``).
	"""

	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message


class UnknownFunctionError(Exception):
	"""
	Exception that is raised by the renderer if the function to be executed by
	the ``callfunc0``, ``callfunc1``, ``callfunc2``, ``callfunc3`` or
	``callfunc4`` opcodes is unknown.
	"""

	def __init__(self, funcname):
		self.funcname = funcname

	def __str__(self):
		return "function {!r} unknown".format(self.funcname)


class UnknownMethodError(Exception):
	"""
	Exception that is raised by the renderer if the method to be executed by the
	``callmeth0``, ``callmeth1``, ``callmeth2``  or ``callmeth3`` opcodes is
	unknown.
	"""

	def __init__(self, methname):
		self.methname = methname

	def __str__(self):
		return "method {!r} unknown".format(self.methname)


class UnknownOpcodeError(Exception):
	"""
	Exception that is raised when an unknown opcode is encountered by the renderer.
	"""

	def __init__(self, opcode):
		self.opcode = opcode

	def __str__(self):
		return "opcode {!r} unknown".format(self.opcode)


class OutOfRegistersError(Exception):
	"""
	Exception that is raised by the compiler when there are no more free
	registers. This might happen with complex expressions in tag code.
	"""

	def __str__(self):
		return "out of registers"


###
### opcode class
###

class Opcode(object):
	"""
	An :class:`Opcode` stores an opcode. An :class:`Opcode` object has the
	following attributes:

	:attr:`code` : string or :const:`None`
		The opcode type (see below for a list).

	:attr:`r1`, :attr:`r2`, :attr:`r3`, :attr:`r4`, :attr:`r5` : integer or :const:`None`
		 Register specifications (for the sources or the target of the opcode)

	:attr:`arg` : string or :const:`None`
		Used if the opcode requires an additional argument (like a variable name
		or the value of a constant).

	:attr:`location` : :class:`Location` object
		The location of the tag to which this opcode belongs.

	The following opcode types are available:

	:const:`None`:
		Print text. The text is available from ``location.code``.

	``"print"``:
		Print the content of register :attr:`r1`. (If the object in the register
		is not a string, it will be converted to a string first.)

	``"loadnone"``:
		Load the constant :const:`None` into register :attr:`r1`.

	``"loadfalse"``:
		Load the constant :const:`False` into register :attr:`r1`.

	``"loadtrue"``:
		Load the constant :const:`True` into register :attr:`r1`.

	``"loadstr"``:
		Load the string :attr:`arg` into register :attr:`r1`.

	``"loadint"``:
		Load the integer value :attr:`arg` into register :attr:`r1`.

	``"loadfloat"``:
		Load the float value :attr:`arg` into register :attr:`r1`.

	``"loaddate"``:
		Load the date value :attr:`arg` into register :attr:`r1`. :attr:`arg` must
		be in ISO format (e.g. ``2008-07-02T11:05:55.460464``).

	``"loadcolor"``:
		Load the color value :attr:`arg` into register :attr:`r1`. :attr:`arg` must
		be in the format ``rrggbbaa``).

	``"buildlist"``:
		Load an empty list into register :attr:`r1`.

	``"builddict"``:
		Load an empty dictionary into register :attr:`r1`.

	``"addlist"``
		Append the object in register :attr:`r2` to the list in register :attr:`r1`.

	``"adddict"``
		Add a new entry to the dictionary in register :attr:`r1`. The object in
		:attr:`r2` is the key and the object in register :attr:`r3` is the value.

	``"updatedict"``
		Update the dictionary in register :attr:`r1` with the items from the
		dictionary in :attr:`r2`.

	``"loadvar"``:
		Load the variable named :attr:`arg` into the register :attr:`r1`.

	``"storevar"``:
		Store the content of register :attr:`r1` in the variable named :attr:`arg`.

	``"addvar"``:
		Add the content of register :attr:`r1` to the variable named :attr:`arg`.

	``"for"``:
		Start a loop over the object in the register :attr:`r2` and store the
		object from each loop iteration in the register :attr:`r1`.

	``"endfor"``:
		End the innermost running ``for`` loop.

	``"break"``:
		Breaks the innermost running ``for`` loop.

	``"continue"``:
		Continues the innermost running ``for`` loop (i.e. jumps back to the
		start of the loop body).

	``"if"``:
		Start a conditional block. If the objects in the register :attr:`r1` is
		true the block will be executed. The "block" consists of all opcodes after
		the ``if`` upto the matching ``else`` or ``endif`` opcode.

	``"else"``:
		Start the else branch of the previous ``if``.

	``"endif"``:
		End a conditional block.

	``"getattr"``:
		Get the attribute named :attr:`arg` from the object in register :attr:`r2`
		and store it in register :attr:`r1`.

	``"getitem"``:
		Get an item from the object in register :attr:`r2`. If this object is a
		list or string the object in register :attr:`r3` will be used as the
		index. If it is a dictionary :attr:`r3` will be used as the key. The
		result will be stored in register :attr:`r1`.

	``"getslice12"``:
		Get an slice from the object in register :attr:`r2`. The object in
		register :attr:`r3` (which must be an ``int`` or :const:`None`) specifies
		the start index, the object in register :attr:`r4` specifies the end index.
		The result will be stored in register :attr:`r1`.

	``"getslice1"``:
		Similar to ``getslice12`` except that the end index is always the length
		of the object.

	``"getslice2"``:
		Similar to ``getslice12`` except that the start index is always 0 and the
		end index is in register :attr:`r3`.

	``"not"``:
		Invert the truth value of the object in register :attr:`r2` and stores the
		resulting bool in the register :attr:`r1`.

	``"eq"``:
		Compare the objects in register :attr:`r2` and :attr:`r3` and store
		``True`` in the register :attr:`r1` if they are equal, ``False`` otherwise.

	``"ne"``:
		Compare the objects in register :attr:`r2` and :attr:`r3` and store
		``False`` in the register :attr:`r1` if they are equal, ``True`` otherwise.

	``"lt"``:
		Does a "<" comparison of the objects in register :attr:`r2` and :attr:`r3`
		and stores the result in register :attr:`r1`.

	``"le"``:
		Does a "<=" comparison of the objects in register :attr:`r2` and :attr:`r3`
		and stores the result in register :attr:`r1`.

	``"gt"``:
		Does a ">" comparison of the objects in register :attr:`r2` and :attr:`r3`
		and stores the result in register :attr:`r1`.

	``"ge"``:
		Does a ">=" comparison of the objects in register :attr:`r2` and :attr:`r3`
		and stores the result in register :attr:`r1`.

	``"contains"``:
		Test whether the object in register :attr:`r3` contains the object in
		register :attr:`r2` (either as a key if :attr:`r3` is a dictionary or as
		an item if it's a list or as a substring if it's a string) and store
		``True`` into the register :attr:`r1` if it does, ``False`` otherwise.

	``"notcontains"``:
		Test whether the object in register :attr:`r3` contains the object in
		register :attr:`r2` (either as a key if :attr:`r3` is a dictionary or as
		an item if it's a list or as a substring if it's a string) and store
		``False`` into the register :attr:`r1` if it does, ``True`` otherwise.

	``"or"``:
		Check the truth value of the two objects in registers :attr:`r2` and
		:attr:`r3` and store :attr:`r2` in the register :attr:`r1` if it is true,
		:attr:`r3` otherwise).

	``"and"``:
		Check the truth value of the two objects in registers :attr:`r2` and
		:attr:`r3` and store :attr:`r3` in the register :attr:`r1` if :attr:`r2`
		is true, :attr:`r3` otherwise).

	``"mod"``:
		Does a modulo operation: Calculates :attr:`r2` modulo :attr:`r3` and stores
		the result in register :attr:`r1`.

	``"callfunc0"``:
		Call the function named :attr:`arg` without any arguments and store the
		return value in register :attr:`r1`.

	``"callfunc1"``:
		Call the function named :attr:`arg` with the content of register :attr:`r2`
		as an argument and store the return value in register :attr:`r1`.

	``"callfunc2"``:
		Call the function named :attr:`arg` with the contents of register
		:attr:`r2` and :attr:`r3` as the two arguments and store the return value
		in register :attr:`r1`.

	``"callfunc3"``:
		Call the function named :attr:`arg` with the contents of register
		:attr:`r2`, :attr:`r3` and :attr:`r4` as the three arguments and store
		the return value in register :attr:`r1`.

	``"callfunc4"``:
		Call the function named :attr:`arg` with the contents of register
		:attr:`r2`, :attr:`r3`, :attr:`r4` and :attr:`r5` as the four arguments
		and store the return value in register :attr:`r1`.

	``"callmeth0"``:
		Call the method named :attr:`arg` on the object in register :attr:`r2`
		and store the return value in register :attr:`r1`.

	``"callmeth1"``:
		Call the method named :attr:`arg` on the object in register :attr:`r2`
		using the object in register :attr:`r3` as the only argument and store the
		return value in register :attr:`r1`.

	``"callmeth2"``:
		Call the method named :attr:`arg` on the object in register :attr:`r2`
		using the objects in register :attr:`r3` and :attr:`r4` as arguments and
		store the return value in register :attr:`r1`.

	``"callmeth3"``:
		Call the method named :attr:`arg` on the object in register :attr:`r2`
		using the objects in register :attr:`r3`, :attr:`r4` and :attr:`r5` as
		arguments and store the return value in register :attr:`r1`.

	``"render"``:
		Render the template in the attribute :attr:`r1`. The content of register
		:attr:`r2` (which must be a dictionary) will be passed to the template as
		the variable dictionary.

	``"def"``
		Begin the definition of a local template. The template will be stored in
		the variable named :attr:`arg`.

	``"enddef"``
		End the definition of a local template.

	"""
	__slots__ = ("code", "r1", "r2", "r3", "r4", "r5", "arg", "location")

	def __init__(self, code, r1=None, r2=None, r3=None, r4=None, r5=None, arg=None, location=None):
		self.code = code
		self.r1 = r1
		self.r2 = r2
		self.r3 = r3
		self.r4 = r4
		self.r5 = r5
		self.arg = arg
		self.location = location

	def __getitem__(self, key):
		if key in {"code", "r1", "r2", "r3", "r4", "r5", "arg", "location"}:
			return getattr(self, key)
		raise KeyError(key)

	def __repr__(self):
		v = ["<", self.__class__.__name__, " code={!r}".format(self.code)]
		for attrname in ("r1", "r2", "r3", "r4", "r5", "arg"):
			attr = getattr(self, attrname)
			if attr is not None:
				v.append(" {}={!r}".format(attrname, attr))
		if self.code is None:
			v.append(" text={!r}".format(self.location.code))
		v.append(" at {:#x}>".format(id(self)))
		return "".join(v)

	def __str__(self):
		formats = {
			None: "print {op.location.code!r}",
			"print": "print r{op.r1!r}",
			"printx": "print xmlescape(r{op.r1!r})",
			"loadnone": "r{op.r1!r} = None",
			"loadfalse": "r{op.r1!r} = False",
			"loadtrue": "r{op.r1!r} = True",
			"loadstr": "r{op.r1!r} = {op.arg!r}",
			"loadint": "r{op.r1!r} = {op.arg}",
			"loadfloat": "r{op.r1!r} = {op.arg}",
			"loaddate": "r{op.r1!r} = {op.arg}",
			"loadcolor": "r{op.r1!r} = #{op.arg}",
			"buildlist": "r{op.r1!r} = []",
			"builddict": "r{op.r1!r} = {{}}",
			"addlist": "r{op.r1!r}.append(r{op.r2!r})",
			"adddict": "r{op.r1!r}[r{op.r2!r}] = r{op.r3!r}",
			"updatedict": "r{op.r1!r}.update(r{op.r2!r})",
			"loadvar": "r{op.r1!r} = vars[{op.arg!r}]",
			"storevar": "vars[{op.arg!r}] = r{op.r1!r}",
			"addvar": "vars[{op.arg!r}] += r{op.r1!r}",
			"subvar": "vars[{op.arg!r}] -= r{op.r1!r}",
			"mulvar": "vars[{op.arg!r}] *= r{op.r1!r}",
			"truedivvar": "vars[{op.arg!r}] /= r{op.r1!r}",
			"floordivvar": "vars[{op.arg!r}] //= r{op.r1!r}",
			"modvar": "vars[{op.arg!r}] %= r{op.r1!r}",
			"delvar": "del vars[{op.arg!r}]",
			"for": "for r{op.r1!r} in r{op.r2!r}",
			"endfor": "endfor",
			"break": "break",
			"continue": "continue",
			"if": "if r{op.r1!r}",
			"else": "else",
			"endif": "endif",
			"getattr": "r{op.r1!r} = getattr(r{op.r2!r}, {op.arg!r})",
			"getitem": "r{op.r1!r} = r{op.r2!r}[r{op.r3!r}]",
			"getslice1": "r{op.r1!r} = r{op.r2!r}[r{op.r3!r}:]",
			"getslice2": "r{op.r1!r} = r{op.r2!r}[:r{op.r3!r}]",
			"getslice12": "r{op.r1!r} = r{op.r2!r}[r{op.r3!r}:r{op.r4!r}]",
			"not": "r{op.r1!r} = not r{op.r2!r}",
			"eq": "r{op.r1!r} = r{op.r2!r} == r{op.r3!r}",
			"ne": "r{op.r1!r} = r{op.r2!r} != r{op.r3!r}",
			"lt": "r{op.r1!r} = r{op.r2!r} < r{op.r3!r}",
			"le": "r{op.r1!r} = r{op.r2!r} <= r{op.r3!r}",
			"gt": "r{op.r1!r} = r{op.r2!r} > r{op.r3!r}",
			"ge": "r{op.r1!r} = r{op.r2!r} >= r{op.r3!r}",
			"contains": "r{op.r1!r} = r{op.r2!r} in r{op.r3!r}",
			"notcontains": "r{op.r1!r} = r{op.r2!r} not in r{op.r3!r}",
			"add": "r{op.r1!r} = r{op.r2!r} + r{op.r3!r}",
			"sub": "r{op.r1!r} = r{op.r2!r} - r{op.r3!r}",
			"mul": "r{op.r1!r} = r{op.r2!r} * r{op.r3!r}",
			"floordiv": "r{op.r1!r} = r{op.r2!r} // r{op.r3!r}",
			"truediv": "r{op.r1!r} = r{op.r2!r} / r{op.r3!r}",
			"and": "r{op.r1!r} = r{op.r2!r} and r{op.r3!r}",
			"or": "r{op.r1!r} = r{op.r2!r} or r{op.r3!r}",
			"mod": "r{op.r1!r} = r{op.r2!r} % r{op.r3!r}",
			"neg":"r{op.r1!r} = -r{op.r2!r}",
			"callfunc0": "r{op.r1!r} = {op.arg}()",
			"callfunc1": "r{op.r1!r} = {op.arg}(r{op.r2!r})",
			"callfunc2": "r{op.r1!r} = {op.arg}(r{op.r2!r}, r{op.r3!r})",
			"callfunc3": "r{op.r1!r} = {op.arg}(r{op.r2!r}, r{op.r3!r}, r{op.r4!r})",
			"callfunc4": "r{op.r1!r} = {op.arg}(r{op.r2!r}, r{op.r3!r}, r{op.r4!r}, r{op.r5!r})",
			"callmeth0": "r{op.r1!r} = r{op.r2!r}.{op.arg}()",
			"callmeth1": "r{op.r1!r} = r{op.r2!r}.{op.arg}(r{op.r3!r})",
			"callmeth2": "r{op.r1!r} = r{op.r2!r}.{op.arg}(r{op.r3!r}, r{op.r4!r})",
			"callmeth3": "r{op.r1!r} = r{op.r3!r}.{op.arg}(r{op.r3!r}, r{op.r4!r}, r{op.r5!r})",
			"callmethkw": "r{op.r1!r} = r{op.r2!r}.{op.arg}(**r{op.r3!r})",
			"render": "render r{op.r1!r}(r{op.r2!r})",
			"def": "def {op.arg}(vars)",
			"enddef": "endfor",
		}
		try:
			return formats[self.code].format(op=self)
		except KeyError:
			raise UnknownOpcodeError(self.code)


class Template(object):
	"""
	A template object can be compiled via the class method :meth:`compile` from
	source. It can be loaded from the compiled format via :meth:`load` (from a
	stream) or :meth:`loads` (from a string).

	The compiled format can be generated with the methods :meth:`dump` (which
	dumps the format to a stream) or :meth:`dumps` (which returns a string with
	the compiled format).

	Rendering the template can be done with the methods :meth:`render` (which
	is a generator) or :meth:`renders` (which returns a string).
	"""
	version = "15"

	def __init__(self, source=None, startdelim="<?", enddelim="?>"):
		"""
		Create a :class:`Template` object. If :var:`source` is :const:`None`, the
		:class:`Template` remains uninitialized, otherwise :var:`source` will be
		compiled (using :var:`startdelim` and :var:`enddelim` as the tag
		delimiters).

		"""
		self.startdelim = startdelim
		self.enddelim = enddelim
		self.source = None
		self.opcodes = None
		# The following is used for converting the opcodes back to executable Python code
		self._pythonfunction = None
		if source is not None:
			self._compile(source, startdelim, enddelim)

	def __getitem__(self, key):
		if key in {"startdelim", "enddelim", "source", "opcodes"}:
			return getattr(self, key)
		raise KeyError(key)

	@classmethod
	def loads(cls, data):
		"""
		The class method :meth:`loads` loads the template from string :var:`data`.
		:var:`data` must contain the template in compiled format.
		"""
		def _readint(prefix):
			if prefix is not None:
				c = stream.read(len(prefix))
				if c != prefix:
					raise ValueError("invalid prefix, expected {!r}, got {!r}".format(prefix, c))
			i = None
			while True:
				c = stream.read(1)
				if c.isdigit():
					if i is None:
						i = 0
					i = 10*i+int(c)
				elif c == "|":
					return i
				else:
					raise ValueError("invalid separator, expected '|', got {!r}".format(c))

		def _readstr(prefix):
			if prefix is not None:
				c = stream.read(len(prefix))
				if c != prefix:
					raise ValueError("invalid prefix, expected {!r}, got {!r}".format(prefix, c))
			i = None
			while True:
				c = stream.read(1)
				if c.isdigit():
					if i is None:
						i = 0
					i = 10*i+int(c)
				elif c == "|":
					if i is None:
						return None
					break
				else:
					raise ValueError("invalid separator, expected '|', got {!r}".format(c))
			s = stream.read(i)
			if len(s) != i:
				raise ValueError("short read")
			c = stream.read(1)
			if c != "|":
				raise ValueError("invalid separator, expected '|', got {!r}".format(c))
			return s

		def _readcr():
			c = stream.read(1)
			if c != "\n":
				raise ValueError("invalid linefeed {!r}".format(c))

		self = cls()
		stream = StringIO.StringIO(data)
		header = stream.readline()
		header = header.rstrip()
		if header != "ul4":
			raise ValueError("invalid header, expected 'ul4', got {!r}".format(header))
		version = stream.readline()
		version = version.rstrip()
		if version != self.version:
			raise ValueError("invalid version, expected {!r}, got {!r}".format(self.version, version))
		self.startdelim = _readstr(u"SD")
		_readcr()
		self.enddelim = _readstr(u"ED")
		_readcr()
		self.source = _readstr("SRC")
		self.opcodes = []
		_readcr()
		count = _readint(u"n")
		_readcr()
		location = None
		while count:
			r1 = _readint(None)
			r2 = _readint(None)
			r3 = _readint(None)
			r4 = _readint(None)
			r5 = _readint(None)
			code = _readstr("C")
			arg = _readstr("A")
			locspec = stream.read(1)
			if locspec == u"^":
				if location is None:
					raise ValueError("no previous location")
			elif locspec == u"*":
				locspec2 = stream.read(1)
				if locspec2 != "|":
					raise ValueError("invalid location spec {!r}".format(locspec + locspec2))
				location = Location(self.source, _readstr("T"), _readint("st"), _readint("et"), _readint("sc"), _readint("ec"))
			else:
				raise ValueError("invalid location spec {!r}".format(locspec))
			_readcr()
			count -= 1
			self.opcodes.append(Opcode(code, r1, r2, r3, r4, r5, arg, location))
		return self

	@classmethod
	def load(cls, stream):
		"""
		The class method :meth:`load` loads the template from the stream
		:var:`stream`. The stream must contain the template in compiled format.
		"""
		return cls.loads(stream.read())

	def iterdump(self):
		"""
		This generator outputs the template in compiled format.
		"""
		def _writeint(prefix, number):
			if prefix is not None:
				yield prefix
			if number is not None:
				yield unicode(number)
			yield u"|"

		def _writestr(prefix, string):
			yield prefix
			if string is not None:
				yield str(len(string))
				yield u"|"
				yield string
			yield u"|"

		yield "ul4\n{}\n".format(self.version)
		for p in _writestr("SD", self.startdelim): yield p
		yield "\n"
		for p in _writestr("ED", self.enddelim): yield p
		yield "\n"
		for p in _writestr("SRC", self.source): yield p
		yield "\n"
		for p in _writeint("n", len(self.opcodes)): yield p
		yield "\n"
		lastlocation = None
		for opcode in self.opcodes:
			for p in _writeint(None, opcode.r1): yield p
			for p in _writeint(None, opcode.r2): yield p
			for p in _writeint(None, opcode.r3): yield p
			for p in _writeint(None, opcode.r4): yield p
			for p in _writeint(None, opcode.r5): yield p
			for p in _writestr("C", opcode.code): yield p
			for p in _writestr("A", opcode.arg): yield p
			if opcode.location is not lastlocation:
				lastlocation = opcode.location
				yield u"*|"
				for p in _writestr("T", lastlocation.type): yield p
				for p in _writeint("st", lastlocation.starttag): yield p
				for p in _writeint("et", lastlocation.endtag): yield p
				for p in _writeint("sc", lastlocation.startcode): yield p
				for p in _writeint("ec", lastlocation.endcode): yield p
			else:
				yield "^"
			yield "\n"

	def dump(self, stream):
		"""
		:meth:`dump` dumps the template in compiled format to the stream
		:var:`stream`.
		"""
		for part in self.iterdump():
			stream.write(part)

	def dumps(self):
		"""
		:meth:`dumps` returns the template in compiled format (as a string).
		"""
		return "".join(self.iterdump())

	def render(self, **variables):
		"""
		Render the template iteratively (i.e. this is a generator).
		:var:`variables` contains the top level variables available to the
		template code.
		"""
		return self.pythonfunction()(**variables)

	def renders(self, **variables):
		"""
		Render the template as a string. :var:`variables` contains the top level
		variables available to the template code.
		"""
		return "".join(self.pythonfunction()(**variables))

	def pythonfunction(self):
		"""
		Return a Python generator that can be called to render the template. The
		argument signature of the function will be ``**variables``.
		"""
		if self._pythonfunction is None:
			code = self.pythonsource("render")
			ns = {}
			exec code.encode("utf-8") in ns # FIXME: no need to encode in Python 3.0
			self._pythonfunction = ns["render"]
		return self._pythonfunction

	def __call__(self, **variables):
		return self.pythonfunction()(**variables)

	def pythonsource(self, *args, **kwargs):
		"""
		Return the template as Python source code. All arguments in :var:`args`
		and :var:`kwargs` will be passed on to the :class:`PythonSource` object
		which creates the sourcecode. See its constructor for more info.
		"""
		return unicode(PythonSource(self, *args, **kwargs))

	def jssource(self):
		"""
		Return the template as the source code of a Javascript function. A
		:class:`JavascriptSource` object will be used to generated the sourcecode.
		"""
		return unicode(JavascriptSource(self))

	def javasource(self, *args, **kwargs):
		"""
		Return the template as Java source code. All arguments in :var:`args`
		and :var:`kwargs` will be passed on to the :class:`JavaSource` object
		which creates the sourcecode. See its constructor for more info.
		"""
		return unicode(JavaSource(self, *args, **kwargs))

	def format(self, indent="\t"):
		"""
		Format the list of opcodes. This is a generator yielding lines to be output
		(but without trailing newlines). :var:`indent` can be used to specify how
		to indent blocks (defaulting to ``"\\t"``).
		"""
		i = 0
		for opcode in self.opcodes:
			if opcode.code in ("else", "endif", "endfor", "enddef"):
				i -= 1
			if opcode.code in ("endif", "endfor", "enddef"):
				yield "{}}}".format(i*indent)
			elif opcode.code in ("for", "if", "def"):
				yield "{}{} {{".format(i*indent, opcode)
			elif opcode.code == "else":
				yield "{}}} else {{".format(i*indent)
			else:
				yield "{}{}".format(i*indent, opcode)
			if opcode.code in ("for", "if", "else", "def"):
				i += 1

	def _tokenize(self, source, startdelim, enddelim):
		"""
		Tokenize the template source code :var:`source` into tags and non-tag
		text. :var:`startdelim` and :var:`enddelim` are used as the tag delimiters.

		This is a generator which produces :class:`Location` objects for each tag
		or non-tag text. It will be called by :meth:`_compile` internally.
		"""
		pattern = u"{}(printx|print|code|for|if|elif|else|end|break|continue|render|def|note)(\s*((.|\\n)*?)\s*)?{}".format(re.escape(startdelim), re.escape(enddelim))
		pos = 0
		for match in re.finditer(pattern, source):
			if match.start() != pos:
				yield Location(source, None, pos, match.start(), pos, match.start())
			type = source[match.start(1):match.end(1)]
			if type != "note":
				yield Location(source, type, match.start(), match.end(), match.start(3), match.end(3))
			pos = match.end()
		end = len(source)
		if pos != end:
			yield Location(source, None, pos, end, pos, end)

	def _allocreg(self):
		"""
		Allocates a free register from the pool of available registers.
		"""
		try:
			return self.registers.pop()
		except KeyError:
			raise OutOfRegistersError()

	def _freereg(self, register):
		"""
		Returns the register :var:`register` to the pool of available registers.
		"""
		self.registers.add(register)

	def opcode(self, code, r1=None, r2=None, r3=None, r4=None, r5=None, arg=None):
		"""
		Creates an :class:`Opcode` object and appends it to :var:`self`\s list of
		opcodes.
		"""
		self.opcodes.append(Opcode(code, r1, r2, r3, r4, r5, arg, self.location))

	def _compile(self, source, startdelim, enddelim):
		"""
		Compile the template source code :var:`source` into opcodes.
		:var:`startdelim` and :var:`enddelim` are used as the tag delimiters.
		"""
		self.startdelim = startdelim
		self.enddelim = enddelim
		scanner = Scanner()
		parseexpr = ExprParser(scanner).compile
		parsestmt = StmtParser(scanner).compile
		parsefor = ForParser(scanner).compile
		parserender = RenderParser(scanner).compile

		# This stack stores for each nested for/foritem/if/elif/else the following information:
		# 1) Which construct we're in (i.e. "if" or "for")
		# 2) The start location of the construct
		# For ifs:
		# 3) How many if's or elif's we have seen (this is used for simulating elif's via nested if's, for each additional elif, we have one more endif to add)
		# 4) Whether we've already seen the else
		stack = []

		self.source = source
		self.opcodes = []

		for location in self._tokenize(source, startdelim, enddelim):
			self.location = location
			try:
				if location.type is None:
					self.opcode(None)
				elif location.type == "print":
					r = parseexpr(self)
					self.opcode("print", r1=r)
				elif location.type == "printx":
					r = parseexpr(self)
					self.opcode("printx", r1=r)
				elif location.type == "code":
					parsestmt(self)
				elif location.type == "if":
					r = parseexpr(self)
					self.opcode("if", r1=r)
					stack.append(("if", location, 1, False))
				elif location.type == "elif":
					if not stack or stack[-1][0] != "if":
						raise BlockError("elif doesn't match any if")
					elif stack[-1][3]:
						raise BlockError("else already seen in elif")
					self.opcode("else")
					r = parseexpr(self)
					self.opcode("if", r1=r)
					stack[-1] = ("if", stack[-1][1], stack[-1][2]+1, False)
				elif location.type == "else":
					if not stack or stack[-1][0] != "if":
						raise BlockError("else doesn't match any if")
					elif stack[-1][3]:
						raise BlockError("duplicate else")
					self.opcode("else")
					stack[-1] = ("if", stack[-1][1], stack[-1][2], True)
				elif location.type == "end":
					if not stack:
						raise BlockError("not in any block")
					code = location.code
					if code:
						if code == "if":
							if stack[-1][0] != "if":
								raise BlockError("endif doesn't match any if")
						elif code == "for":
							if stack[-1][0] != "for":
								raise BlockError("endfor doesn't match any for")
						elif code == "def":
							if stack[-1][0] != "def":
								raise BlockError("enddef doesn't match any def")
						else:
							raise BlockError("illegal end value {!r}".format(code))
					last = stack.pop()
					if last[0] == "if":
						for i in xrange(last[2]):
							self.opcode("endif")
					elif last[0] == "for":
						self.opcode("endfor")
					else: # last[0] == "def":
						self.opcode("enddef")
				elif location.type == "for":
					parsefor(self)
					stack.append(("for", location))
				elif location.type == "break":
					if not any(entry[0] == "for" for entry in stack):
						raise BlockError("break outside of for loop")
					self.opcode("break")
				elif location.type == "continue":
					if not any(entry[0] == "for" for entry in stack):
						raise BlockError("continue outside of for loop")
					self.opcode("continue")
				elif location.type == "render":
					parserender(self)
				elif location.type == "def":
					self.opcode("def", arg=location.code)
					stack.append(("def", location))
				else: # Can't happen
					raise ValueError("unknown tag {!r}".format(location.type))
			except Exception, exc:
				newexc = Error(location) # FIXME: use ``raise ... from`` in Python 3.0
				newexc.__cause__ = exc
				raise newexc
			finally:
				del self.location
		if stack:
			newexc = Error(stack[-1][1]) # FIXME: use ``raise ... from`` in Python 3.0
			newexc.__cause__ = BlockError("block unclosed")
			raise newexc

	def __str__(self):
		return "\n".join(self.format())

	def __unicode__(self):
		return u"\n".join(self.format())

	def __repr__(self):
		return "<{}.{} object with {} opcodes at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, len(self.opcodes), id(self))


def compile(source, startdelim="<?", enddelim="?>"):
	return Template(source, startdelim, enddelim)


load = Template.load
loads = Template.loads


###
### Code generators for various languages
###

class PythonSource(object):
	"""
	A :class:`PythonSource` object generates Python sourcecode from a UL4
	template.
	"""

	def __init__(self, template, function=None):
		"""
		Create a :class:`PythonSource` object. :var:`template` is the
		:class:`Template` object. If :var:`function` is specified the code will be
		wrapped in a function with this name.
		"""
		self.template = template
		self.function = function

	def __unicode__(self):
		"""
		Return the Python sourcecode for the :class:`Template` object passed to
		the constructor.
		"""
		self.indent = 0
		self.lines = []
		self.locations = []
		self.lines2locs = []
		self.defs = [] # Stack for currently open def opcodes
		self.lastopcode = None
		self.lastlocation = Location(self.template.source, None, 0, 0, 0, 0)

		if self.function is not None:
			self._line(self.lastlocation, "def {}(**variables):".format(self.function))
			self.indent += 1
			self.lines2locs = [] # We initialize startline one line below, which restarts the counter
		self._line(self.lastlocation, "import sys, datetime, itertools, json, random, collections; from ll.misc import xmlescape; from ll import ul4c, color; startline = sys._getframe().f_lineno") # The line number of this line
		self._line(self.lastlocation, "__1__")
		self._line(self.lastlocation, "__2__")
		self._line(self.lastlocation, "source = {!r}".format(self.template.source))
		self._line(self.lastlocation, 'variables = {key.decode("utf-8"): value for (key, value) in variables.iteritems()}') # FIXME: This can be dropped in Python 3.0 where strings are unicode
		self._line(self.lastlocation, "r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = r8 = r9 = None")
		self._line(self.lastlocation, "try:")
		self.indent += 1
		# Make sure that the resulting code is a generator even if the byte codes produce no yield statement
		self._line(self.lastlocation, "if 0: yield ''")
		try:
			for opcode in self.template.opcodes:
				try:
					getattr(self, "_dispatch_{}".format(opcode.code))(opcode)
				except AttributeError:
					raise UnknownOpcodeError(opcode.code)
				self.lastopcode = opcode.code
		except Exception, exc:
			newexc = Error(opcode.location) # FIXME: Use ``raise ... from`` in Python 3.0
			newexc.__cause__ = exc
			raise newexc
		self.indent -= 1
		self._line(self.lastlocation, "except Exception, exc:")
		self.indent += 1
		self._line(self.lastlocation, "newexc = ul4c.Error(ul4c.Location(source, *locations[lines2locs[sys.exc_info()[2].tb_lineno-startline]]))") # FIXME: Use ``raise ... from`` in Python 3.0
		self._line(self.lastlocation, "newexc.__cause__ = exc")
		self._line(self.lastlocation, "raise newexc")
		locoffset = 1+int(self.lines[0].strip() != "__1__")
		self.lines[locoffset] = self.lines[locoffset].replace("__1__", "locations = {!r}".format(tuple(self.locations)))
		self.lines[locoffset+1] = self.lines[locoffset+1].replace("__2__", "lines2locs = {!r}".format(tuple(self.lines2locs)))
		return "\n".join(self.lines)

	def _line(self, location, line):
		self.lines.append("\t"*self.indent + line)
		if self.lastlocation is not location or not self.locations:
			self.locations.append((location.type, location.starttag, location.endtag, location.startcode, location.endcode))
			self.lastlocation = location
		self.lines2locs.append(len(self.locations)-1)

	def _dispatch_None(self, opcode):
		self._line(opcode.location, "yield {op.location.code!r}".format(op=opcode))
	def _dispatch_loadstr(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = {op.arg!r}".format(op=opcode))
	def _dispatch_loadint(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = {op.arg}".format(op=opcode))
	def _dispatch_loadfloat(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = {op.arg}".format(op=opcode))
	def _dispatch_loadnone(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = None".format(op=opcode))
	def _dispatch_loadfalse(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = False".format(op=opcode))
	def _dispatch_loadtrue(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = True".format(op=opcode))
	def _dispatch_loaddate(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = datetime.datetime({date})".format(op=opcode, date=", ".join(str(int(p)) for p in datesplitter.split(opcode.arg))))
	def _dispatch_loadcolor(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = color.Color({r}, {g}, {b}, {a})".format(op=opcode, r=int(opcode.arg[:2], 16), g=int(opcode.arg[2:4], 16), b=int(opcode.arg[4:6], 16), a=int(opcode.arg[6:], 16)))
	def _dispatch_buildlist(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = []".format(op=opcode))
	def _dispatch_builddict(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = {{}}".format(op=opcode))
	def _dispatch_addlist(self, opcode):
		self._line(opcode.location, "r{op.r1:d}.append(r{op.r2:d})".format(op=opcode))
	def _dispatch_adddict(self, opcode):
		self._line(opcode.location, "r{op.r1:d}[r{op.r2:d}] = r{op.r3:d}".format(op=opcode))
	def _dispatch_updatedict(self, opcode):
		self._line(opcode.location, "r{op.r1:d}.update(r{op.r2:d})".format(op=opcode))
	def _dispatch_loadvar(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = variables[{op.arg!r}]".format(op=opcode))
	def _dispatch_storevar(self, opcode):
		self._line(opcode.location, "variables[{op.arg!r}] = r{op.r1:d}".format(op=opcode))
	def _dispatch_addvar(self, opcode):
		self._line(opcode.location, "variables[{op.arg!r}] += r{op.r1:d}".format(op=opcode))
	def _dispatch_subvar(self, opcode):
		self._line(opcode.location, "variables[{op.arg!r}] -= r{op.r1:d}".format(op=opcode))
	def _dispatch_mulvar(self, opcode):
		self._line(opcode.location, "variables[{op.arg!r}] *= r{op.r1:d}".format(op=opcode))
	def _dispatch_truedivvar(self, opcode):
		self._line(opcode.location, "variables[{op.arg!r}] /= r{op.r1:d}".format(op=opcode))
	def _dispatch_floordivvar(self, opcode):
		self._line(opcode.location, "variables[{op.arg!r}] //= r{op.r1:d}".format(op=opcode))
	def _dispatch_modvar(self, opcode):
		self._line(opcode.location, "variables[{op.arg!r}] %= r{op.r1:d}".format(op=opcode))
	def _dispatch_delvar(self, opcode):
		self._line(opcode.location, "del variables[{op.arg!r}]".format(op=opcode))
	def _dispatch_getattr(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}[{op.arg!r}]".format(op=opcode))
	def _dispatch_getitem(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}[r{op.r3:d}]".format(op=opcode))
	def _dispatch_getslice12(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}[r{op.r3:d}:r{op.r4:d}]".format(op=opcode))
	def _dispatch_getslice1(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}[r{op.r3:d}:]".format(op=opcode))
	def _dispatch_getslice2(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}[:r{op.r3:d}]".format(op=opcode))
	def _dispatch_print(self, opcode):
		self._line(opcode.location, "if r{op.r1:d} is not None: yield unicode(r{op.r1:d})".format(op=opcode))
	def _dispatch_printx(self, opcode):
		self._line(opcode.location, "if r{op.r1:d} is not None: yield xmlescape(unicode(r{op.r1:d}))".format(op=opcode))
	def _dispatch_for(self, opcode):
		self._line(opcode.location, "for r{op.r1:d} in r{op.r2:d}:".format(op=opcode))
		self.indent += 1
	def _dispatch_endfor(self, opcode):
		# we don't have to check for empty loops here, as a ``<?for?>`` tag always generates at least one ``storevar`` opcode inside the loop
		self.indent -= 1
	def _dispatch_break(self, opcode):
		self._line(opcode.location, "break")
	def _dispatch_continue(self, opcode):
		self._line(opcode.location, "continue")
	def _dispatch_not(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = not r{op.r2:d}".format(op=opcode))
	def _dispatch_neg(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = -r{op.r2:d}".format(op=opcode))
	def _dispatch_contains(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} in r{op.r3:d}".format(op=opcode))
	def _dispatch_notcontains(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} not in r{op.r3:d}".format(op=opcode))
	def _dispatch_eq(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} == r{op.r3:d}".format(op=opcode))
	def _dispatch_ne(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} != r{op.r3:d}".format(op=opcode))
	def _dispatch_lt(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} < r{op.r3:d}".format(op=opcode))
	def _dispatch_le(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} <= r{op.r3:d}".format(op=opcode))
	def _dispatch_gt(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} > r{op.r3:d}".format(op=opcode))
	def _dispatch_ge(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} >= r{op.r3:d}".format(op=opcode))
	def _dispatch_add(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} + r{op.r3:d}".format(op=opcode))
	def _dispatch_sub(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} - r{op.r3:d}".format(op=opcode))
	def _dispatch_mul(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} * r{op.r3:d}".format(op=opcode))
	def _dispatch_floordiv(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} // r{op.r3:d}".format(op=opcode))
	def _dispatch_truediv(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} / r{op.r3:d}".format(op=opcode))
	def _dispatch_and(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} and r{op.r3:d}".format(op=opcode))
	def _dispatch_or(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} or r{op.r3:d}".format(op=opcode))
	def _dispatch_mod(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} % r{op.r3:d}".format(op=opcode))
	def _dispatch_callfunc0(self, opcode):
		try:
			getattr(self, "_dispatch_callfunc0_{op.arg}".format(op=opcode))(opcode)
		except AttributeError:
			raise UnknownFunctionError(opcode.arg)
	def _dispatch_callfunc1(self, opcode):
		try:
			getattr(self, "_dispatch_callfunc1_{op.arg}".format(op=opcode))(opcode)
		except AttributeError:
			raise UnknownFunctionError(opcode.arg)
	def _dispatch_callfunc2(self, opcode):
		try:
			getattr(self, "_dispatch_callfunc2_{op.arg}".format(op=opcode))(opcode)
		except AttributeError:
			raise UnknownFunctionError(opcode.arg)
	def _dispatch_callfunc3(self, opcode):
		try:
			getattr(self, "_dispatch_callfunc3_{op.arg}".format(op=opcode))(opcode)
		except AttributeError:
			raise UnknownFunctionError(opcode.arg)
	def _dispatch_callfunc4(self, opcode):
		try:
			getattr(self, "_dispatch_callfunc4_{op.arg}".format(op=opcode))(opcode)
		except AttributeError:
			raise UnknownFunctionError(opcode.arg)
	def _dispatch_callmeth0(self, opcode):
		if opcode.arg in ("split", "rsplit", "strip", "lstrip", "rstrip", "upper", "lower", "capitalize", "r", "g", "b", "a", "hls", "hlsa", "hsv", "hsva", "lum", "weekday"):
			self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}.{op.arg}()".format(op=opcode))
		elif opcode.arg == "items":
			self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}.iteritems()".format(op=opcode))
		elif opcode.arg == "render":
			self._line(opcode.location, 'r{op.r1:d} = "".join(r{op.r2:d}())'.format(op=opcode))
		elif opcode.arg in ("mimeformat", "yearday", "isoformat"):
			self._line(opcode.location, 'r{op.r1:d} = ul4c._{op.arg}(r{op.r2:d})'.format(op=opcode))
		elif opcode.arg in ("day", "month", "year", "hour", "minute", "second", "microsecond"):
			self._line(opcode.location, 'r{op.r1:d} = r{op.r2:d}.{op.arg}'.format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
	def _dispatch_callmeth1(self, opcode):
		if opcode.arg in ("split", "rsplit", "strip", "lstrip", "rstrip", "startswith", "endswith", "find", "rfind", "get", "withlum", "witha"):
			self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}.{op.arg}(r{op.r3:d})".format(op=opcode))
		elif opcode.arg == "join":
			self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}.join(unicode(x) for x in r{op.r3:d})".format(op=opcode))
		elif opcode.arg == "format":
			self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}.__format__(r{op.r3:d})".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
	def _dispatch_callmeth2(self, opcode):
		if opcode.arg in ("split", "rsplit", "find", "rfind", "replace", "get"):
			self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}.{op.arg}(r{op.r3:d}, r{op.r4:d})".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
	def _dispatch_callmeth3(self, opcode):
		if opcode.arg in {"find", "rfind"}:
			self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}.{op.arg}(r{op.r3:d}, r{op.r4:d}, r{op.r5:d})".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
	def _dispatch_callmethkw(self, opcode):
		if opcode.arg == "render":
			self._line(opcode.location, 'r{op.r1:d} = "".join(r{op.r2:d}(**{{key.encode("utf-8"): value for (key, value) in r{op.r3:d}.iteritems()}}))'.format(op=opcode)) # FIXME: This can be simplified in Python 3.0 where strings are unicode
		else:
			raise UnknownMethodError(opcode.arg)
	def _dispatch_if(self, opcode):
		self._line(opcode.location, "if r{op.r1:d}:".format(op=opcode))
		self.indent += 1
	def _dispatch_else(self, opcode):
		if self.lastopcode == "if":
			self.lines[-1] += " pass"
		self.indent -= 1
		self._line(opcode.location, "else:")
		self.indent += 1
	def _dispatch_endif(self, opcode):
		if self.lastopcode in ("if", "else"):
			lines[-1] += " pass"
		self.indent -= 1
	def _dispatch_def(self, opcode):
		self._line(opcode.location, "def _(**variables):")
		self.defs.append(opcode)
		self.indent += 1
		self._line(opcode.location, 'variables = {key.decode("utf-8"): value for (key, value) in variables.iteritems()}') # FIXME: This can be dropped in Python 3.0 where strings are unicode
		self._line(opcode.location, "r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = r8 = r9 = None")
		self._line(opcode.location, "try:")
		self.indent += 1
		# Make sure that the resulting code is a generator even if the byte codes produce no yield statement
		self._line(opcode.location, "if 0: yield ''")
	def _dispatch_enddef(self, opcode):
		defopcode = self.defs.pop()
		self.indent -= 1
		self._line(opcode.location, "except Exception, exc:")
		self.indent += 1
		self._line(opcode.location, "newexc = ul4c.Error(ul4c.Location(source, *locations[lines2locs[sys.exc_info()[2].tb_lineno-startline]]))") # FIXME: Use ``raise ... from`` in Python 3.0
		self._line(opcode.location, "newexc.__cause__ = exc")
		self._line(opcode.location, "raise newexc")
		self.indent -= 2
		self._line(opcode.location, "variables[{op.arg!r}] = _".format(op=defopcode))
	def _dispatch_render(self, opcode):
		self._line(opcode.location, 'for chunk in r{op.r1:d}(**{{key.encode("utf-8"): value for (key, value) in r{op.r2:d}.iteritems()}}): yield chunk'.format(op=opcode))
	def _dispatch_callfunc0_now(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = datetime.datetime.now()".format(op=opcode))
	def _dispatch_callfunc0_utcnow(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = datetime.datetime.utcnow()".format(op=opcode))
	def _dispatch_callfunc0_vars(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = variables".format(op=opcode))
	def _dispatch_callfunc0_random(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = random.random()".format(op=opcode))
	def _dispatch_callfunc1_xmlescape(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = xmlescape(unicode(r{op.r2:d})) if r{op.r2:d} is not None else u''".format(op=opcode))
	def _dispatch_callfunc1_csv(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._csv(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_json(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._json(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_str(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = unicode(r{op.r2:d}) if r{op.r2:d} is not None else u''".format(op=opcode))
	def _dispatch_callfunc1_int(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = int(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_float(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = float(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_bool(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = bool(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_len(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = len(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_abs(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = abs(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_enumerate(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = enumerate(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_isnone(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} is None".format(op=opcode))
	def _dispatch_callfunc1_isstr(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, basestring)".format(op=opcode))
	def _dispatch_callfunc1_isint(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, (int, long)) and not isinstance(r{op.r2:d}, bool)".format(op=opcode))
	def _dispatch_callfunc1_isfloat(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, float)".format(op=opcode))
	def _dispatch_callfunc1_isbool(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, bool)".format(op=opcode))
	def _dispatch_callfunc1_isdate(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, datetime.datetime)".format(op=opcode))
	def _dispatch_callfunc1_islist(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, collections.Sequence) and not isinstance(r{op.r2:d}, (str, unicode, color.Color))".format(op=opcode))
	def _dispatch_callfunc1_isdict(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, collections.Mapping)".format(op=opcode))
	def _dispatch_callfunc1_istemplate(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = hasattr(r{op.r2:d}, '__call__')".format(op=opcode)) # this supports normal generators too
	def _dispatch_callfunc1_iscolor(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, color.Color)".format(op=opcode))
	def _dispatch_callfunc1_repr(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._repr(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_get(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = variables.get(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_chr(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = unichr(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_ord(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ord(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_hex(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = hex(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_oct(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._oct(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_bin(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = bin(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_sorted(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = sorted(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_range(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = xrange(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_type(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._type(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_reversed(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = reversed(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_randrange(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = random.randrange(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_randchoice(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = random.choice(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc2_format(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = format(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc2_range(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = xrange(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc2_get(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = variables.get(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc2_zip(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = itertools.izip(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc2_int(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = int(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc2_randrange(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = random.randrange(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc3_range(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = xrange(r{op.r2:d}, r{op.r3:d}, r{op.r4:d})".format(op=opcode))
	def _dispatch_callfunc3_zip(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = itertools.izip(r{op.r2:d}, r{op.r3:d}, r{op.r4:d})".format(op=opcode))
	def _dispatch_callfunc3_rgb(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = color.Color.fromrgb(r{op.r2:d}, r{op.r3:d}, r{op.r4:d})".format(op=opcode))
	def _dispatch_callfunc3_hls(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = color.Color.fromhls(r{op.r2:d}, r{op.r3:d}, r{op.r4:d})".format(op=opcode))
	def _dispatch_callfunc3_hsv(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = color.Color.fromhsv(r{op.r2:d}, r{op.r3:d}, r{op.r4:d})".format(op=opcode))
	def _dispatch_callfunc3_randrange(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = random.randrange(r{op.r2:d}, r{op.r3:d}, r{op.r4:d})".format(op=opcode))
	def _dispatch_callfunc4_rgb(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = color.Color.fromrgb(r{op.r2:d}, r{op.r3:d}, r{op.r4:d}, r{op.r5:d})".format(op=opcode))
	def _dispatch_callfunc4_hls(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = color.Color.fromhls(r{op.r2:d}, r{op.r3:d}, r{op.r4:d}, r{op.r5:d})".format(op=opcode))
	def _dispatch_callfunc4_hsv(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = color.Color.fromhsv(r{op.r2:d}, r{op.r3:d}, r{op.r4:d}, r{op.r5:d})".format(op=opcode))


class JavascriptSource(object):
	"""
	A :class:`JavascriptSource` object generates javascript sourcecode from a UL4
	template.

	The signature of the generated Javascript function will be ``function(vars)``,
	i.e. all template variables will be attributes of the object ``vars``.

	Note that the generated code will require the ``ul4`` Javascript support
	library.
	"""
	def __init__(self, template):
		"""
		Create a :class:`JavascriptSource` object. :var:`template` is the
		:class:`Template` object.
		"""
		self.template = template

	def __unicode__(self):
		"""
		Return the Javascript sourcecode for the :class:`Template` object passed
		to the constructor.
		"""
		self._indent = 0
		self._lines = []
		self._varcounter = 0

		self._line("ul4.Template.create(function(vars){")
		self._indent += 1

		self._line(u"//@@@ BEGIN template source")
		lines = self.template.source.splitlines(False)
		width = len(str(len(lines)+1))
		for (i, line) in enumerate(lines):
			self._line(u"// {1:{0}} {2}".format(width, i+1, line))
		self._line(u"//@@@ BEGIN template code")

		self._line(u"var out = [], {};".format(", ".join("r{} = null".format(i) for i in xrange(10))))

		lastloc = None
		for opcode in self.template.opcodes:
			if opcode.code is not None and opcode.location is not lastloc:
				lastloc = opcode.location
				(line, col) = lastloc.pos()
				tag = lastloc.tag
				self._line(u"// <?{}?< tag at {} (line {}, col {}): {}".format(lastloc.type, lastloc.starttag+1, line, col, repr(tag)[1+isinstance(tag, unicode):-1]))
			try:
				getattr(self, "_dispatch_{}".format(opcode.code))(opcode)
			except AttributeError:
				raise UnknownOpcodeError(opcode.code)

		self._line(u'return out;')
		self._line(u"//@@@ END template code")

		self._indent -= 1
		self._line("})")

		return "\n".join(self._lines)

	def _line(self, line):
		self._lines.append(u"\t"*self._indent + line)

	def _dispatch_None(self, opcode):
		self._line("out.push({});".format(json.dumps(opcode.location.code)))
	def _dispatch_loadstr(self, opcode):
		self._line(u'r{op.r1} = {arg};'.format(op=opcode, arg=json.dumps(opcode.arg)))
	def _dispatch_loadint(self, opcode):
		self._line(u"r{op.r1} = {op.arg};".format(op=opcode))
	def _dispatch_loadfloat(self, opcode):
		self._line(u"r{op.r1} = {op.arg};".format(op=opcode))
	def _dispatch_loadnone(self, opcode):
		self._line(u"r{op.r1} = null;".format(op=opcode))
	def _dispatch_loadfalse(self, opcode):
		self._line(u"r{op.r1} = false;".format(op=opcode))
	def _dispatch_loadtrue(self, opcode):
		self._line(u"r{op.r1} = true;".format(op=opcode))
	def _dispatch_loaddate(self, opcode):
		args = map(int, datesplitter.split(opcode.arg))
		args[1] -= 1
		if len(args) == 7:
			args[6] //= 1000
		self._line(u"r{op.r1} = new Date({date});".format(op=opcode, date=", ".join(map(str, args))))
	def _dispatch_loadcolor(self, opcode):
		self._line(u"r{op.r1} = ul4.Color.create({r}, {g}, {b}, {a});".format(op=opcode, r=int(opcode.arg[:2], 16), g=int(opcode.arg[2:4], 16), b=int(opcode.arg[4:6], 16), a=int(opcode.arg[6:], 16)))
	def _dispatch_buildlist(self, opcode):
		self._line(u"r{op.r1} = [];".format(op=opcode))
	def _dispatch_builddict(self, opcode):
		self._line(u"r{op.r1} = {{}};".format(op=opcode))
	def _dispatch_addlist(self, opcode):
		self._line(u"r{op.r1}.push(r{op.r2});".format(op=opcode))
	def _dispatch_adddict(self, opcode):
		self._line(u"r{op.r1}[r{op.r2}] = r{op.r3};".format(op=opcode))
	def _dispatch_updatedict(self, opcode):
		self._line(u"for (var key in r{op.r2})".format(op=opcode))
		self._indent += 1
		self._line(u"r{op.r1}[key] = r{op.r2}[key];".format(op=opcode))
		self._indent -= 1
	def _dispatch_loadvar(self, opcode):
		self._line(u"r{op.r1} = ul4._op_getitem(vars, {arg});".format(op=opcode, arg=json.dumps(opcode.arg)))
	def _dispatch_storevar(self, opcode):
		self._line(u"vars[{arg}] = r{op.r1};".format(op=opcode, arg=json.dumps(opcode.arg)))
	def _dispatch_addvar(self, opcode):
		self._line(u"vars[{arg}] = ul4._op_add(vars[{arg}], r{op.r1});".format(op=opcode, arg=json.dumps(opcode.arg)))
	def _dispatch_subvar(self, opcode):
		self._line(u"vars[{arg}] = ul4._op_sub(vars[{arg}], r{op.r1});".format(op=opcode, arg=json.dumps(opcode.arg)))
	def _dispatch_mulvar(self, opcode):
		self._line(u"vars[{arg}] = ul4._op_mul(vars[{arg}], r{op.r1});".format(op=opcode, arg=json.dumps(opcode.arg)))
	def _dispatch_truedivvar(self, opcode):
		self._line(u"vars[{arg}] = ul4._op_truediv(vars[{arg}], r{op.r1});".format(op=opcode, arg=json.dumps(opcode.arg)))
	def _dispatch_floordivvar(self, opcode):
		self._line(u"vars[{arg}] = ul4._op_floordiv(vars[{arg}], r{op.r1});".format(op=opcode, arg=json.dumps(opcode.arg)))
	def _dispatch_modvar(self, opcode):
		self._line(u"vars[{arg}] = ul4._op_mod(vars[{arg}], r{op.r1});".format(op=opcode, arg=json.dumps(opcode.arg)))
	def _dispatch_delvar(self, opcode):
		self._line(u"vars[{arg}] = undefined;".format(arg=json.dumps(opcode.arg)))
	def _dispatch_getattr(self, opcode):
		self._line(u"r{op.r1} = ul4._op_getitem(r{op.r2}, {arg});".format(op=opcode, arg=json.dumps(opcode.arg)))
	def _dispatch_getitem(self, opcode):
		self._line(u"r{op.r1} = ul4._op_getitem(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_getslice12(self, opcode):
		self._line(u"r{op.r1} = ul4._op_getslice(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
	def _dispatch_getslice1(self, opcode):
		self._line(u"r{op.r1} = ul4._op_getslice(r{op.r2}, r{op.r3}, null);".format(op=opcode))
	def _dispatch_getslice2(self, opcode):
		self._line(u"r{op.r1} = ul4._op_getslice(r{op.r2}, null, r{op.r3});".format(op=opcode))
	def _dispatch_print(self, opcode):
		self._line(u"out.push(ul4._fu_str(r{op.r1}));".format(op=opcode))
	def _dispatch_printx(self, opcode):
		self._line(u"out.push(ul4._fu_xmlescape(r{op.r1}));".format(op=opcode))
	def _dispatch_for(self, opcode):
		self._varcounter += 1
		self._line(u"for (var iter{counter} = ul4._iter(r{op.r2});;)".format(op=opcode, counter=self._varcounter))
		self._line(u"{")
		self._indent += 1
		self._line(u"r{op.r1} = iter{counter}();".format(op=opcode, counter=self._varcounter))
		self._line(u"if (r{op.r1} === null)".format(op=opcode))
		self._indent += 1
		self._line(u"break;")
		self._indent -= 1
		self._line(u"r{op.r1} = r{op.r1}[0];".format(op=opcode))
	def _dispatch_endfor(self, opcode):
		self._indent -= 1
		self._line(u"}")
	def _dispatch_def(self, opcode):
		self._line(u"vars[{arg}] = ul4.Template.create(function(vars){{".format(arg=json.dumps(opcode.arg)))
		self._indent += 1
		self._line(u"var out = [], {};".format(", ".join("r{} = null".format(i) for i in xrange(10))))
	def _dispatch_enddef(self, opcode):
		self._line(u'return out;')
		self._indent -= 1
		self._line(u"});")
	def _dispatch_break(self, opcode):
		self._line(u"break;")
	def _dispatch_continue(self, opcode):
		self._line(u"continue;")
	def _dispatch_not(self, opcode):
		self._line(u"r{op.r1} = !ul4._fu_bool(r{op.r2});".format(op=opcode))
	def _dispatch_neg(self, opcode):
		self._line(u"r{op.r1} = ul4._op_neg(r{op.r2});".format(op=opcode))
	def _dispatch_contains(self, opcode):
		self._line(u"r{op.r1} = ul4._op_contains(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_notcontains(self, opcode):
		self._line(u"r{op.r1} = !ul4._op_contains(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_eq(self, opcode):
		self._line(u"r{op.r1} = ul4._op_eq(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_ne(self, opcode):
		self._line(u"r{op.r1} = !ul4._op_eq(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_lt(self, opcode):
		self._line(u"r{op.r1} = ul4._op_lt(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_le(self, opcode):
		self._line(u"r{op.r1} = ul4._op_le(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_gt(self, opcode):
		self._line(u"r{op.r1} = !ul4._op_le(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_ge(self, opcode):
		self._line(u"r{op.r1} = !ul4._op_lt(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_add(self, opcode):
		self._line(u"r{op.r1} = ul4._op_add(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_sub(self, opcode):
		self._line(u"r{op.r1} = ul4._op_sub(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_mul(self, opcode):
		self._line(u"r{op.r1} = ul4._op_mul(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_floordiv(self, opcode):
		self._line(u"r{op.r1} = ul4._op_floordiv(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_truediv(self, opcode):
		self._line(u"r{op.r1} = ul4._op_truediv(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_and(self, opcode):
		self._line(u"r{op.r1} = ul4._fu_bool(r{op.r3}) ? r{op.r2} : r{op.r3};".format(op=opcode))
	def _dispatch_or(self, opcode):
		self._line(u"r{op.r1} = ul4._fu_bool(r{op.r2}) ? r{op.r2} : r{op.r3};".format(op=opcode))
	def _dispatch_mod(self, opcode):
		self._line(u"r{op.r1} = ul4._op_mod(r{op.r2}, r{op.r3});".format(op=opcode))
	def _dispatch_callfunc0(self, opcode):
		if opcode.arg == "now":
			self._line(u"r{op.r1} = new Date();".format(op=opcode))
		elif opcode.arg == "utcnow":
			self._line(u"r{op.r1} = ul4._fu_utcnow();".format(op=opcode))
		elif opcode.arg == "random":
			self._line(u"r{op.r1} = Math.random();".format(op=opcode))
		elif opcode.arg == "vars":
			self._line(u"r{op.r1} = vars;".format(op=opcode))
		else:
			raise UnknownFunctionError(opcode.arg)
	def _dispatch_callfunc1(self, opcode):
		if opcode.arg in {"xmlescape", "csv", "repr", "enumerate", "chr", "ord", "hex", "oct", "bin", "sorted", "type", "json", "reversed", "randchoice", "str", "int", "float", "bool", "len", "isstr", "isint", "isfloat", "isbool", "isdate", "islist", "isdict", "istemplate", "iscolor", "abs"}:
			self._line(u"r{op.r1} = ul4._fu_{op.arg}(r{op.r2});".format(op=opcode))
		elif opcode.arg in {"range", "randrange"}:
			self._line(u"r{op.r1} = ul4._fu_{op.arg}(0, r{op.r2}, 1);".format(op=opcode))
		elif opcode.arg == "isnone":
			self._line(u"r{op.r1} = (r{op.r2} === null);".format(op=opcode))
		elif opcode.arg == "get":
			self._line(u"r{op.r1} = ul4._me_get(vars, r{op.r2});".format(op=opcode))
		else:
			raise UnknownFunctionError(opcode.arg)
	def _dispatch_callfunc2(self, opcode):
		if opcode.arg in {"format", "zip", "int"}:
			self._line(u"r{op.r1} = ul4._fu_{op.arg}(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.arg in {"range", "randrange"}:
			self._line(u"r{op.r1} = ul4._fu_{op.arg}(r{op.r2}, r{op.r3}, 1);".format(op=opcode))
		elif opcode.arg == "get":
			self._line(u"r{op.r1} = ul4._me_get(vars, r{op.r2}, r{op.r3});".format(op=opcode))
		else:
			raise UnknownFunctionError(opcode.arg)
	def _dispatch_callfunc3(self, opcode):
		if opcode.arg in {"range", "zip", "randrange"}:
			self._line(u"r{op.r1} = ul4._fu_{op.arg}(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
		elif opcode.arg in {"rgb", "hls", "hsv"}:
			self._line(u"r{op.r1} = ul4._fu_{op.arg}(r{op.r2}, r{op.r3}, r{op.r4}, 1.0);".format(op=opcode))
		else:
			raise UnknownFunctionError(opcode.arg)
	def _dispatch_callfunc4(self, opcode):
		if opcode.arg in {"rgb", "hls", "hsv"}:
			self._line(u"r{op.r1} = ul4._fu_{op.arg}(r{op.r2}, r{op.r3}, r{op.r4}, r{op.r5});".format(op=opcode))
		else:
			raise UnknownFunctionError(opcode.arg)
	def _dispatch_callmeth0(self, opcode):
		if opcode.arg in {"strip", "lstrip", "rstrip", "upper", "lower", "capitalize", "items", "isoformat", "mimeformat", "day", "month", "year", "hour", "minute", "second", "microsecond", "weekday", "yearday", "r", "g", "b", "a", "lum", "hls", "hlsa", "hsv", "hsva"}:
			self._line(u"r{op.r1} = ul4._me_{op.arg}(r{op.r2});".format(op=opcode))
		elif opcode.arg in {"split", "rsplit"}:
			self._line(u"r{op.r1} = ul4._me_{op.arg}(r{op.r2}, null, null);".format(op=opcode))
		elif opcode.arg == "render":
			self._line(u"r{op.r1} = r{op.r2}.renders({{}});".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
	def _dispatch_callmeth1(self, opcode):
		if opcode.arg in {"join", "strip", "lstrip", "rstrip", "startswith", "endswith", "withlum", "witha"}:
			self._line(u"r{op.r1} = ul4._me_{op.arg}(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.arg in {"split", "rsplit", "get"}:
			self._line(u"r{op.r1} = ul4._me_{op.arg}(r{op.r2}, r{op.r3}, null);".format(op=opcode))
		elif opcode.arg in {"find", "rfind"}:
			self._line(u"r{op.r1} = ul4._me_{op.arg}(r{op.r2}, r{op.r3}, null, null);".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
	def _dispatch_callmeth2(self, opcode):
		if opcode.arg in {"split", "rsplit", "replace", "get"}:
			self._line(u"r{op.r1} = ul4._me_{op.arg}(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
		elif opcode.arg in {"find", "rfind"}:
			self._line(u"r{op.r1} = ul4._me_{op.arg}(r{op.r2}, r{op.r3}, r{op.r4}, null);".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
	def _dispatch_callmeth3(self, opcode):
		if opcode.arg in {"find", "rfind"}:
			self._line(u"r{op.r1} = ul4._me_{op.arg}(r{op.r2}, r{op.r3}, r{op.r4}, r{op.r5});".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
	def _dispatch_callmethkw(self, opcode):
		if opcode.arg == "render":
			self._line(u"r{op.r1} = r{op.r2}.renders(r{op.r3});".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
	def _dispatch_if(self, opcode):
		self._line(u"if (ul4._fu_bool(r{op.r1}))".format(op=opcode))
		self._line(u"{")
		self._indent += 1
	def _dispatch_else(self, opcode):
		self._indent -= 1
		self._line(u"}")
		self._line(u"else")
		self._line(u"{")
		self._indent += 1
	def _dispatch_endif(self, opcode):
		self._indent -= 1
		self._line(u"}")
	def _dispatch_render(self, opcode):
		self._line(u"out = out.concat(r{op.r1}.render(r{op.r2}));".format(op=opcode))


class _JavaTemplateLevel(object):
	def __init__(self, variables, name=None):
		self.variables = variables # Name of the variables dict
		self.name = name
		self.lines = [] # contains source code lines and indentation info
		self.varcounter = 0 # Counter for variables names (loop variable etc.)
		self.regsused = set() # Which registers have been used?


class JavaSource(object):
	"""
	A :class:`JavaSource` object generates Java sourcecode from a UL4
	template.

	The code produced requires the `UL4 Java package`__.

	__ http://hg.livinglogic.de/LivingLogic.Java.ul4
	"""

	def __init__(self, template, indent=2, variables="variables"):
		"""
		Create a :class:`JavaSource` object. :var:`template` is the
		:class:`Template` object.

		:var:`indent` is the current indent level (defaulting to 2 for normal
		method source code).

		:var:`variables` is the variable name of a ``Map`` object containing the
		template variables.
		"""
		self.template = template
		self.indent = indent
		self.variables = variables

	def __unicode__(self):
		"""
		Return the Java sourcecode for the :class:`Template` object passed to
		the constructor.
		"""

		self._stack = [_JavaTemplateLevel(self.variables)] # Stack for info about nested def opcodes

		lines = []

		lastloc = None
		for opcode in self.template.opcodes:
			if opcode.code is not None and opcode.location is not lastloc:
				lastloc = opcode.location
				(line, col) = lastloc.pos()
				tag = lastloc.tag
				self._do(u"/* <?{}?> tag at {} (line {}, col {}): {} */".format(lastloc.type, lastloc.starttag+1, line, col, repr(tag)[1+isinstance(tag, unicode):-1]))
			try:
				getattr(self, "_dispatch_{}".format(opcode.code))(opcode)
			except AttributeError:
				raise UnknownOpcodeError(opcode.code)

		# Add source and register declaration at the beginning
		lines.append(u"/*@@@ BEGIN template source */")
		sourcelines = self.template.source.splitlines(False)
		width = len(str(len(sourcelines)))
		for (i, line) in enumerate(sourcelines):
			lines.append(u"/* {1:{0}} {2} */".format(width, i+1, line))
		lines.append(u"/*@@@ BEGIN template code */")
		
		for i in sorted(self._stack[-1].regsused):
			lines.append(u"Object r{} = null;".format(i))

		# copy over generated source code
		lines.extend(self._stack[-1].lines)

		lines.append(u"/*@@@ END template code */")

		v = []
		indent = self.indent
		for line in lines:
			if isinstance(line, int):
				indent += line
			else:
				v.append("\t"*indent + line)
		return u"\n".join(v)

	def output(self, expression):
		"""
		Return a statement for outputting the Java expression :var:`expression`.
		This uses ``out.write()`` (for JSP etc.) but can be overwritten in
		subclasses.
		"""
		return u"out.write({});".format(expression)

	def _usereg(self, r):
		self._stack[-1].regsused.add(r)

	def _do(self, line):
		# :var:`line` is either an ``int`` (which is added to the current indentation) or a line of source code.
		self._stack[-1].lines.append(line)

	def _dispatch_None(self, opcode):
		(line, col) = opcode.location.pos()
		self._do(u"/* Literal at {} (line {}, col {}) */".format(opcode.location.starttag+1, line, col))
		self._do(self.output(misc.javaexpr(opcode.location.code)))
	def _dispatch_loadstr(self, opcode):
		self._do(u"r{op.r1} = {arg};".format(op=opcode, arg=misc.javaexpr(opcode.arg)))
		self._usereg(opcode.r1)
	def _dispatch_loadint(self, opcode):
		self._do(u"r{op.r1} = new Integer({op.arg});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loadfloat(self, opcode):
		self._do(u"r{op.r1} = new Double({op.arg});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loadnone(self, opcode):
		self._do(u"r{op.r1} = null;".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loadfalse(self, opcode):
		self._do(u"r{op.r1} = false;".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loadtrue(self, opcode):
		self._do(u"r{op.r1} = true;".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loaddate(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.makeDate({date});".format(op=opcode, date=", ".join(str(int(p)) for p in datesplitter.split(opcode.arg))))
		self._usereg(opcode.r1)
	def _dispatch_loadcolor(self, opcode):
		self._do(u"r{op.r1} = new com.livinglogic.ul4.Color(0x{r}, 0x{g}, 0x{b}, 0x{a});".format(op=opcode, r=opcode.arg[:2], g=opcode.arg[2:4], b=opcode.arg[4:6], a=opcode.arg[6:]))
		self._usereg(opcode.r1)
	def _dispatch_buildlist(self, opcode):
		self._do(u"r{op.r1} = new java.util.ArrayList();".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_builddict(self, opcode):
		self._do(u"r{op.r1} = new java.util.HashMap();".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_addlist(self, opcode):
		self._do(u"((java.util.List)r{op.r1}).add(r{op.r2});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_adddict(self, opcode):
		self._do(u"((java.util.Map)r{op.r1}).put(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_updatedict(self, opcode):
		self._do(u"((java.util.Map)r{op.r1}).putAll((java.util.Map)r{op.r2});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loadvar(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.getItem({var}, {arg});".format(op=opcode, var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg)))
		self._usereg(opcode.r1)
	def _dispatch_storevar(self, opcode):
		self._do(u"{var}.put({arg}, r{op.r1});".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_addvar(self, opcode):
		self._do(u"{var}.put({arg}, com.livinglogic.ul4.Utils.add({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_subvar(self, opcode):
		self._do(u"{var}.put({arg}, com.livinglogic.ul4.Utils.sub({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_mulvar(self, opcode):
		self._do(u"{var}.put({arg}, com.livinglogic.ul4.Utils.mul({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_truedivvar(self, opcode):
		self._do(u"{var}.put({arg}, com.livinglogic.ul4.Utils.truediv({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_floordivvar(self, opcode):
		self._do(u"{var}.put({arg}, com.livinglogic.ul4.Utils.floordiv({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_modvar(self, opcode):
		self._do(u"{var}.put({arg}, com.livinglogic.ul4.Utils.mod({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_delvar(self, opcode):
		self._do(u"{var}.remove({arg});".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg)))
	def _dispatch_getattr(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.getItem(r{op.r2}, {arg});".format(op=opcode, arg=misc.javaexpr(opcode.arg)))
		self._usereg(opcode.r1)
	def _dispatch_getitem(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.getItem(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_getslice12(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.getSlice(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_getslice1(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.getSlice(r{op.r2}, r{op.r3}, null);".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_getslice2(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.getSlice(r{op.r2}, null, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_print(self, opcode):
		self._do(self.output(u"com.livinglogic.ul4.Utils.str(r{op.r1})".format(op=opcode)))
	def _dispatch_printx(self, opcode):
		self._do(self.output(u"com.livinglogic.ul4.Utils.xmlescape(r{op.r1})".format(op=opcode)))
	def _dispatch_for(self, opcode):
		varcounter = self._stack[-1].varcounter
		self._do(u"for (java.util.Iterator iterator{count} = com.livinglogic.ul4.Utils.iterator(r{op.r2}); iterator{count}.hasNext();)".format(op=opcode, count=varcounter))
		self._do(u"{")
		self._do(1)
		self._do(u"r{op.r1} = iterator{count}.next();".format(op=opcode, count=varcounter))
		self._usereg(opcode.r1)
		self._stack[-1].varcounter += 1
	def _dispatch_endfor(self, opcode):
		self._do(-1)
		self._do(u"}")
	def _dispatch_def(self, opcode):
		self._stack.append(_JavaTemplateLevel("variables", opcode.arg))
	def _dispatch_enddef(self, opcode):
		level = self._stack.pop()
		varcounter = self._stack[-1].varcounter
		# define new template object
		self._do(u"com.livinglogic.ul4.JSPTemplate template{count} = new com.livinglogic.ul4.JSPTemplate()".format(count=varcounter))
		self._do(u"{")
		self._do(1)
		self._do(u"public void render(java.io.Writer out, java.util.Map<String, Object> variables) throws java.io.IOException")
		self._do(u"{")
		self._do(1)
		# registers
		for i in sorted(level.regsused):
			self._do(u"Object r{} = null;".format(i))
		# copy over source from the nested template
		self._stack[-1].lines.extend(level.lines)
		# end object and put it into variables
		self._do(-1)
		self._do(u"}")
		self._do(-1)
		self._do(u"};")
		self._do(u"{var}.put({arg}, template{count});".format(var=self._stack[-1].variables, arg=misc.javaexpr(level.name), count=varcounter))
		self._stack[-1].varcounter += 1
	def _dispatch_break(self, opcode):
		self._do(u"break;")
	def _dispatch_continue(self, opcode):
		self._do(u"continue;")
	def _dispatch_not(self, opcode):
		self._do(u"r{op.r1} = !com.livinglogic.ul4.Utils.getBool(r{op.r2});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_neg(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.neg(r{op.r2});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_contains(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.contains(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_notcontains(self, opcode):
		self._do(u"r{op.r1} = !com.livinglogic.ul4.Utils.contains(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_eq(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.eq(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_ne(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.ne(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_lt(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.lt(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_le(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.le(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_gt(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.gt(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_ge(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.ge(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_add(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.add(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_sub(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.sub(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_mul(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.mul(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_floordiv(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.floordiv(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_truediv(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.truediv(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_and(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.getBool(r{op.r3}) ? r{op.r2} : r{op.r3};".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_or(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.getBool(r{op.r2}) ? r{op.r2} : r{op.r3};".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_mod(self, opcode):
		self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.mod(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_callfunc0(self, opcode):
		if opcode.arg == "now":
			self._do(u"r{op.r1} = new java.util.Date();".format(op=opcode))
		elif opcode.arg in {"utcnow", "random"}:
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}();".format(op=opcode))
		elif opcode.arg == "vars":
			self._do(u"r{op.r1} = {var};".format(op=opcode, var=self._stack[-1].variables))
		else:
			raise UnknownFunctionError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callfunc1(self, opcode):
		if opcode.arg in {"xmlescape", "csv", "repr", "enumerate", "chr", "ord", "hex", "oct", "bin", "sorted", "range", "type", "json", "reversed", "randrange", "randchoice", "abs", "str"}:
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2});".format(op=opcode))
		elif opcode.arg == "int":
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.toInteger(r{op.r2});".format(op=opcode))
		elif opcode.arg == "float":
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.toFloat(r{op.r2});".format(op=opcode))
		elif opcode.arg == "bool":
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.getBool(r{op.r2});".format(op=opcode))
		elif opcode.arg == "len":
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.length(r{op.r2});".format(op=opcode))
		elif opcode.arg == "isnone":
			self._do(u"r{op.r1} = (r{op.r2} == null);".format(op=opcode))
		elif opcode.arg == "isstr":
			self._do(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof String));".format(op=opcode))
		elif opcode.arg == "isint":
			self._do(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof Integer));".format(op=opcode))
		elif opcode.arg == "isfloat":
			self._do(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof Double));".format(op=opcode))
		elif opcode.arg == "isbool":
			self._do(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof Boolean));".format(op=opcode))
		elif opcode.arg == "isdate":
			self._do(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof java.util.Date));".format(op=opcode))
		elif opcode.arg == "islist":
			self._do(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof java.util.List));".format(op=opcode))
		elif opcode.arg == "isdict":
			self._do(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof java.util.Map));".format(op=opcode))
		elif opcode.arg == "istemplate":
			self._do(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof com.livinglogic.ul4.Template));".format(op=opcode))
		elif opcode.arg == "iscolor":
			self._do(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof com.livinglogic.ul4.Color));".format(op=opcode))
		elif opcode.arg == "get":
			self._do(u"r{op.r1} = {var}.get(r{op.r2});".format(op=opcode, var=self._stack[-1].variables))
		else:
			raise UnknownFunctionError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callfunc2(self, opcode):
		if opcode.arg in {"format", "range", "zip", "randrange"}:
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.arg == "int":
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.toInteger(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.arg == "get":
			self._do(u"r{op.r1} = {var}.containsKey(r{op.r2}) ? {var}.get(r{op.r2}) : r{op.r3};".format(op=opcode, var=self._stack[-1].variables))
		else:
			raise UnknownFunctionError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callfunc3(self, opcode):
		if opcode.arg in {"range", "zip", "rgb", "hls", "hsv", "randrange"}:
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
		else:
			raise UnknownFunctionError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callfunc4(self, opcode):
		if opcode.arg in {"rgb", "hls", "hsv"}:
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4}, r{op.r5});".format(op=opcode))
		else:
			raise UnknownFunctionError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callmeth0(self, opcode):
		if opcode.arg in {"split", "rsplit", "strip", "lstrip", "rstrip", "upper", "lower", "capitalize", "items", "isoformat", "mimeformat", "day", "month", "year", "hour", "minute", "second", "microsecond", "weekday", "yearday"}:
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2});".format(op=opcode))
		elif opcode.arg in {"r", "g", "b", "a"}:
			self._do(u"r{op.r1} = ((com.livinglogic.ul4.Color)r{op.r2}).get{arg}();".format(op=opcode, arg=opcode.arg.upper()))
		elif opcode.arg in {"hls", "hlsa", "hsv", "hsva"}:
			self._do(u"r{op.r1} = ((com.livinglogic.ul4.Color)r{op.r2}).{op.arg}();".format(op=opcode))
		elif opcode.arg == "lum":
			self._do(u"r{op.r1} = ((com.livinglogic.ul4.Color)r{op.r2}).lum();".format(op=opcode))
		elif opcode.arg == "render":
			self._do(u"r{op.r1} = ((com.livinglogic.ul4.Template)r{op.r2}).renders(null);".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callmeth1(self, opcode):
		if opcode.arg in {"join", "split", "rsplit", "strip", "lstrip", "rstrip", "startswith", "endswith", "find", "rfind", "withlum", "witha"}:
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.arg == "get":
			self._do(u"r{op.r1} = ((java.util.Map)r{op.r2}).get(r{op.r3});".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callmeth2(self, opcode):
		if opcode.arg in {"split", "rsplit", "find", "rfind", "replace"}:
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
		elif opcode.arg == "get":
			self._do(u"r{op.r1} = ((java.util.Map)r{op.r2}).containsKey(r{op.r3}) ? ((java.util.Map)r{op.r2}).get(r{op.r3}) : r{op.r4};".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callmeth3(self, opcode):
		if opcode.arg in {"find", "rfind"}:
			self._do(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4}, r{op.r5});".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callmethkw(self, opcode):
		if opcode.arg == "render":
			self._do(u"r{op.r1} = ((com.livinglogic.ul4.Template)r{op.r2}).renders((java.util.Map)r{op.r3});".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_if(self, opcode):
		self._do(u"if (com.livinglogic.ul4.Utils.getBool(r{op.r1}))".format(op=opcode))
		self._do(u"{")
		self._do(1)
	def _dispatch_else(self, opcode):
		self._do(-1)
		self._do(u"}")
		self._do(u"else")
		self._do(u"{")
		self._do(1)
	def _dispatch_endif(self, opcode):
		self._do(-1)
		self._do(u"}")
	def _dispatch_render(self, opcode):
		self._do(u"((com.livinglogic.ul4.Template)r{op.r1}).render(out, (java.util.Map)r{op.r2});".format(op=opcode))


###
### Compiler stuff: Tokens and nodes for the AST
###

class Token(object):
	def __init__(self, start, end, type):
		self.start = start
		self.end = end
		self.type = type

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.type)

	def __str__(self):
		return self.type


class AST(object):
	"""
	Baseclass for all syntax tree nodes.
	"""

	def __init__(self, start, end):
		self.start = start
		self.end = end


class Const(AST):
	"""
	Common baseclass for all constants (used for type testing in constant folding)
	"""

	def __repr__(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.start, self.end)

	def compile(self, template):
		r = template._allocreg()
		template.opcode("load{}".format(self.type), r1=r)
		return r


class None_(Const):
	type = "none"
	value = None


class True_(Const):
	type = "true"
	value = True


class False_(Const):
	type = "false"
	value = False


class Value(Const):
	def __init__(self, start, end, value):
		Const.__init__(self, start, end)
		self.value = value

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.value)

	def compile(self, template):
		r = template._allocreg()
		template.opcode("load{}".format(self.type), r1=r, arg=unicode(self.value))
		return r


class Int(Value):
	type = "int"


class Float(Value):
	type = "float"

	def compile(self, template):
		r = template._allocreg()
		template.opcode("load{}".format(self.type), r1=r, arg=repr(self.value))
		return r


class Str(Value):
	type = "str"


class Date(Value):
	type = "date"

	def compile(self, template):
		r = template._allocreg()
		template.opcode("load{}".format(self.type), r1=r, arg=self.value.isoformat())
		return r


class Color(Value):
	type = "color"

	def compile(self, template):
		r = template._allocreg()
		template.opcode("load{}".format(self.type), r1=r, arg="{:02x}{:02x}{:02x}{:02x}".format(*self.value))
		return r


class List(AST):
	def __init__(self, start, end, *items):
		AST.__init__(self, start, end)
		self.items = list(items)

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, repr(self.items)[1:-1])

	def compile(self, template):
		r = template._allocreg()
		template.opcode("buildlist", r1=r)
		for item in self.items:
			ri = item.compile(template)
			template.opcode("addlist", r1=r, r2=ri)
			template._freereg(ri)
		return r


class Dict(AST):
	def __init__(self, start, end, *items):
		AST.__init__(self, start, end)
		self.items = list(items)

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, repr(self.items)[1:-1])

	def compile(self, template):
		r = template._allocreg()
		template.opcode("builddict", r1=r)
		for item in self.items:
			if len(item) == 1:
				rd = item[0].compile(template)
				template.opcode("updatedict", r1=r, r2=rd)
				template._freereg(rd)
			else:
				(key, value) = item
				rk = key.compile(template)
				rv = value.compile(template)
				template.opcode("adddict", r1=r, r2=rk, r3=rv)
				template._freereg(rk)
				template._freereg(rv)
		return r


class Name(AST):
	type = "name"

	def __init__(self, start, end, name):
		AST.__init__(self, start, end)
		self.name = name

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.name)

	def compile(self, template):
		r = template._allocreg()
		template.opcode("loadvar", r1=r, arg=self.name)
		return r


class For(AST):
	def __init__(self, start, end, iter, cont):
		AST.__init__(self, start, end)
		self.iter = iter
		self.cont = cont

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.iter, self.cont)

	def compile(self, template):
		rc = self.cont.compile(template)
		ri = template._allocreg()
		template.opcode("for", r1=ri, r2=rc)
		if isinstance(self.iter, list):
			rii = template._allocreg()
			for (i, iter) in enumerate(self.iter):
				template.opcode("loadint", r1=rii, arg=str(i))
				template.opcode("getitem", r1=rii, r2=ri, r3=rii)
				template.opcode("storevar", r1=rii, arg=iter.name)
			template._freereg(rii)
		else:
			template.opcode("storevar", r1=ri, arg=self.iter.name)
		template._freereg(ri)
		template._freereg(rc)


class GetAttr(AST):
	def __init__(self, start, end, obj, attr):
		AST.__init__(self, start, end)
		self.obj = obj
		self.attr = attr

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.obj, self.attr)

	def compile(self, template):
		r = self.obj.compile(template)
		template.opcode("getattr", r1=r, r2=r, arg=self.attr.name)
		return r


class GetSlice12(AST):
	def __init__(self, start, end, obj, index1, index2):
		AST.__init__(self, start, end)
		self.obj = obj
		self.index1 = index1
		self.index2 = index2

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.obj, self.index1, self.index2)

	def compile(self, template):
		r1 = self.obj.compile(template)
		r2 = self.index1.compile(template)
		r3 = self.index2.compile(template)
		template.opcode("getslice12", r1=r1, r2=r1, r3=r2, r4=r3)
		template._freereg(r2)
		template._freereg(r3)
		return r1


class Unary(AST):
	opcode = None

	def __init__(self, start, end, obj):
		AST.__init__(self, start, end)
		self.obj = obj

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.obj)

	def compile(self, template):
		r = self.obj.compile(template)
		template.opcode(self.opcode, r1=r, r2=r)
		return r


class Not(Unary):
	opcode = "not"


class Neg(Unary):
	opcode = "neg"


class Binary(AST):
	opcode = None

	def __init__(self, start, end, obj1, obj2):
		AST.__init__(self, start, end)
		self.obj1 = obj1
		self.obj2 = obj2

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.obj1, self.obj2)

	def compile(self, template):
		r1 = self.obj1.compile(template)
		r2 = self.obj2.compile(template)
		template.opcode(self.opcode, r1=r1, r2=r1, r3=r2)
		template._freereg(r2)
		return r1


class GetItem(Binary):
	opcode = "getitem"


class GetSlice1(Binary):
	opcode = "getslice1"


class GetSlice2(Binary):
	opcode = "getslice2"


class EQ(Binary):
	opcode = "eq"


class NE(Binary):
	opcode = "ne"


class LT(Binary):
	opcode = "lt"


class LE(Binary):
	opcode = "le"


class GT(Binary):
	opcode = "gt"


class GE(Binary):
	opcode = "ge"


class Contains(Binary):
	opcode = "contains"


class NotContains(Binary):
	opcode = "notcontains"


class Add(Binary):
	opcode = "add"


class Sub(Binary):
	opcode = "sub"


class Mul(Binary):
	opcode = "mul"


class FloorDiv(Binary):
	opcode = "floordiv"


class TrueDiv(Binary):
	opcode = "truediv"


class Or(Binary):
	opcode = "or"


class And(Binary):
	opcode = "and"


class Mod(Binary):
	opcode = "mod"


class ChangeVar(AST):
	opcode = None

	def __init__(self, start, end, name, value):
		AST.__init__(self, start, end)
		self.name = name
		self.value = value

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.name, self.value)

	def compile(self, template):
		r = self.value.compile(template)
		template.opcode(self.opcode, r1=r, arg=self.name.name)
		template._freereg(r)


class StoreVar(ChangeVar):
	opcode = "storevar"


class AddVar(ChangeVar):
	opcode = "addvar"


class SubVar(ChangeVar):
	opcode = "subvar"


class MulVar(ChangeVar):
	opcode = "mulvar"


class TrueDivVar(ChangeVar):
	opcode = "truedivvar"


class FloorDivVar(ChangeVar):
	opcode = "floordivvar"


class ModVar(ChangeVar):
	opcode = "modvar"


class DelVar(AST):
	def __init__(self, start, end, name):
		AST.__init__(self, start, end)
		self.name = name

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.name)

	def compile(self, template):
		template.opcode("delvar", arg=self.name.name)


class CallFunc(AST):
	def __init__(self, start, end, name, args):
		AST.__init__(self, start, end)
		self.name = name
		self.args = args

	def __repr__(self):
		if self.args:
			return "{}({!r}, {!r}, {!r}, {})".format(self.__class__.__name__, self.start, self.end, self.name, repr(self.args)[1:-1])
		else:
			return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.name)

	def compile(self, template):
		if len(self.args) == 0:
			r = template._allocreg()
			template.opcode("callfunc0", r1=r, arg=self.name.name)
			return r
		elif len(self.args) > 4:
			raise ValueError("{} function arguments not supported".format(len(self.args)))
		else:
			rs = [arg.compile(template) for arg in self.args]
			template.opcode("callfunc{}".format(len(self.args)), rs[0], *rs, **dict(arg=self.name.name)) # FIXME: Replace **dict(arg=) with arg= in Python 2.6?
			for i in xrange(1, len(self.args)):
				template._freereg(rs[i])
			return rs[0]


class CallMeth(AST):
	def __init__(self, start, end, name, obj, args):
		AST.__init__(self, start, end)
		self.name = name
		self.obj = obj
		self.args = args

	def __repr__(self):
		if self.args:
			return "{}({!r}, {!r}, {!r}, {!r}, {})".format(self.__class__.__name__, self.start, self.end, self.name, self.obj, repr(self.args)[1:-1])
		else:
			return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.name, self.obj)

	def compile(self, template):
		if len(self.args) > 3:
			raise ValueError("{} method arguments not supported".format(len(self.args)))
		ro = self.obj.compile(template)
		rs = [arg.compile(template) for arg in self.args]
		template.opcode("callmeth{}".format(len(self.args)), ro, ro, *rs, **dict(arg=self.name.name))
		for r in rs:
			template._freereg(r)
		return ro


class CallMethKeywords(AST):
	def __init__(self, start, end, name, obj, args):
		AST.__init__(self, start, end)
		self.name = name
		self.obj = obj
		self.args = args

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.start, self.end, self.name, self.obj, self.args)

	def compile(self, template):
		ra = template._allocreg()
		template.opcode("builddict", r1=ra)
		for item in self.args:
			if len(item) == 1:
				rd = item[0].compile(template)
				template.opcode("updatedict", r1=ra, r2=rd)
				template._freereg(rd)
			else:
				(key, value) = item
				rv = value.compile(template)
				rk = template._allocreg()
				template.opcode("loadstr", r1=rk, arg=key.name)
				template.opcode("adddict", r1=ra, r2=rk, r3=rv)
				template._freereg(rk)
				template._freereg(rv)
		ro = self.obj.compile(template)
		template.opcode("callmethkw", r1=ro, r2=ro, r3=ra, arg=self.name.name)
		template._freereg(ra)
		return ro


class Render(AST):
	def __init__(self, start, end, template, *variables):
		AST.__init__(self, start, end)
		self.template = template
		self.variables = list(variables)

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {})".format(self.__class__.__name__, self.start, self.end, self.template, repr(self.variables)[1:-1])

	def compile(self, template):
		ra = template._allocreg()
		template.opcode("builddict", r1=ra)
		for item in self.variables:
			if len(item) == 1:
				rd = item[0].compile(template)
				template.opcode("updatedict", r1=ra, r2=rd)
				template._freereg(rd)
			else:
				(key, value) = item
				rv = value.compile(template)
				rk = template._allocreg()
				template.opcode("loadstr", r1=rk, arg=key.name)
				template.opcode("adddict", r1=ra, r2=rk, r3=rv)
				template._freereg(rk)
				template._freereg(rv)
		rt = self.template.compile(template)
		template.opcode("render", r1=rt, r2=ra)
		template._freereg(rt)
		template._freereg(ra)


###
### Tokenizer
###

class Scanner(spark.Scanner):
	reflags = re.UNICODE

	def tokenize(self, location):
		self.collectstr = []
		self.rv = []
		self.start = 0
		try:
			spark.Scanner.tokenize(self, location.code)
			if self.mode != "default":
				raise UnterminatedStringError()
		except Exception, exc:
			newexc = Error(location) # FIXME: use ``raise ... from`` in Python 3.0
			newexc.__cause__ = exc
			raise newexc
		return self.rv

	# Color tokens must be in the order of decreasing length
	@spark.token("\\#[0-9a-fA-F]{8}", "default")
	def color8(self, start, end, s):
		self.rv.append(Color(start, end, color.Color(int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), int(s[7:], 16))))

	@spark.token("\\#[0-9a-fA-F]{6}", "default")
	def color6(self, start, end, s):
		self.rv.append(Color(start, end, color.Color(int(s[1:3], 16), int(s[3:5], 16), int(s[5:], 16))))

	@spark.token("\\#[0-9a-fA-F]{4}", "default")
	def color4(self, start, end, s):
		self.rv.append(Color(start, end, color.Color(17*int(s[1], 16), 17*int(s[2], 16), 17*int(s[3], 16), 17*int(s[4], 16))))

	@spark.token("\\#[0-9a-fA-F]{3}", "default")
	def color3(self, start, end, s):
		self.rv.append(Color(start, end, color.Color(17*int(s[1], 16), 17*int(s[2], 16), 17*int(s[3], 16))))

	@spark.token("@\\d{4}-\\d{2}-\\d{2}T(\\d{2}:\\d{2}(:\\d{2}(\\.\\d{6})?)?)?", "default")
	def date(self, start, end, s):
		self.rv.append(Date(start, end, datetime.datetime(*map(int, filter(None, datesplitter.split(s[1:]))))))

	@spark.token("\\(|\\)|\\[|\\]|\\{|\\}|\\.|,|==|\\!=|<=|<|>=|>|=|\\+=|\\-=|\\*=|//=|/=|%=|%|:|\\+|-|\\*\\*|\\*|//|/", "default")
	def token(self, start, end, s):
		self.rv.append(Token(start, end, s))

	@spark.token("[a-zA-Z_][\\w]*", "default")
	def name(self, start, end, s):
		if s in ("in", "not", "or", "and", "del"):
			self.rv.append(Token(start, end, s))
		elif s == "None":
			self.rv.append(None_(start, end))
		elif s == "True":
			self.rv.append(True_(start, end))
		elif s == "False":
			self.rv.append(False_(start, end))
		else:
			self.rv.append(Name(start, end, s))

	# We don't have negatve numbers, this is handled by constant folding in the AST for unary minus
	@spark.token("\\d+\\.\\d*([eE][+-]?\\d+)?", "default")
	@spark.token("\\d+(\\.\\d*)?[eE][+-]?\\d+", "default")
	def float(self, start, end, s):
		self.rv.append(Float(start, end, float(s)))

	@spark.token("0[xX][\\da-fA-F]+", "default")
	def hexint(self, start, end, s):
		self.rv.append(Int(start, end, int(s[2:], 16)))

	@spark.token("0[oO][0-7]+", "default")
	def octint(self, start, end, s):
		self.rv.append(Int(start, end, int(s[2:], 8)))

	@spark.token("0[bB][01]+", "default")
	def binint(self, start, end, s):
		self.rv.append(Int(start, end, int(s[2:], 2)))

	@spark.token("\\d+", "default")
	def int(self, start, end, s):
		self.rv.append(Int(start, end, int(s)))

	@spark.token("'", "default")
	def beginstr1(self, start, end, s):
		self.mode = "str1"
		self.start = start

	@spark.token('"', "default")
	def beginstr2(self, start, end, s):
		self.mode = "str2"
		self.start = start

	@spark.token("'", "str1")
	@spark.token('"', "str2")
	def endstr(self, start, end, s):
		self.rv.append(Str(self.start, end, "".join(self.collectstr)))
		self.collectstr = []
		self.mode = "default"

	@spark.token("\\s+", "default")
	def whitespace(self, start, end, s):
		pass

	@spark.token("\\\\\\\\", "str1", "str2")
	def escapedbackslash(self, start, end, s):
		self.collectstr.append("\\")

	@spark.token("\\\\'", "str1", "str2")
	def escapedapos(self, start, end, s):
		self.collectstr.append("'")

	@spark.token('\\\\"', "str1", "str2")
	def escapedquot(self, start, end, s):
		self.collectstr.append('"')

	@spark.token("\\\\a", "str1", "str2")
	def escapedbell(self, start, end, s):
		self.collectstr.append("\a")

	@spark.token("\\\\b", "str1", "str2")
	def escapedbackspace(self, start, end, s):
		self.collectstr.append("\b")

	@spark.token("\\\\f", "str1", "str2")
	def escapedformfeed(self, start, end, s):
		self.collectstr.append("\f")

	@spark.token("\\\\n", "str1", "str2")
	def escapedlinefeed(self, start, end, s):
		self.collectstr.append("\n")

	@spark.token("\\\\r", "str1", "str2")
	def escapedcarriagereturn(self, start, end, s):
		self.collectstr.append("\r")

	@spark.token("\\\\t", "str1", "str2")
	def escapedtab(self, start, end, s):
		self.collectstr.append("\t")

	@spark.token("\\\\v", "str1", "str2")
	def escapedverticaltab(self, start, end, s):
		self.collectstr.append("\v")

	@spark.token("\\\\e", "str1", "str2")
	def escapedescape(self, start, end, s):
		self.collectstr.append("\x1b")

	@spark.token("\\\\x[0-9a-fA-F]{2}", "str1", "str2")
	def escaped8bitchar(self, start, end, s):
		self.collectstr.append(unichr(int(s[2:], 16)))

	@spark.token("\\\\u[0-9a-fA-F]{4}", "str1", "str2")
	def escaped16bitchar(self, start, end, s):
		self.collectstr.append(unichr(int(s[2:], 16)))

	@spark.token(".|\\n", "str1", "str2")
	def text(self, start, end, s):
		self.collectstr.append(s)

	@spark.token("(.|\\n)+", "default", "str1", "str2")
	def default(self, start, end, s):
		raise LexicalError(start, end, s)

	def error(self, start, end, s):
		raise LexicalError(start, end, s)


###
### Parsers for different types of code
###

class ExprParser(spark.Parser):
	emptyerror = "expression required"
	start = "expr0"

	def __init__(self, scanner):
		spark.Parser.__init__(self)
		self.scanner = scanner

	def compile(self, template):
		location = template.location
		if not location.code:
			raise ValueError(self.emptyerror)
		template.registers = set(xrange(10))
		try:
			ast = self.parse(self.scanner.tokenize(location))
			return ast.compile(template)
		except Exception, exc:
			newexc = Error(location) # FIXME: Use ``raise ... from`` in Python 3.0
			newexc.__cause__ = exc
			raise newexc
		finally:
			del template.registers

	def typestring(self, token):
		return token.type

	def error(self, token):
		raise SyntaxError(token)

	def makeconst(self, start, end, value):
		if value is None:
			return None_(start, end)
		elif value is True:
			return True_(start, end)
		elif value is False:
			return False_(start, end)
		elif isinstance(value, (int, long)):
			return Int(start, end, value)
		elif isinstance(value, float):
			return Float(start, end, value)
		elif isinstance(value, basestring):
			return Str(start, end, value)
		elif isinstance(value, color.Color):
			return Color(start, end, value)
		else:
			raise TypeError("can't convert {!r}".format(value))

	# To implement operator precedence, each expression rule has the precedence in its name. The highest precedence is 11 for atomic expressions.
	# Each expression can have only expressions as parts which have the some or a higher precedence with two exceptions:
	#    1. Expressions where there's no ambiguity, like the index for a getitem/getslice or function/method arguments;
	#    2. Brackets, which can be used to boost the precedence of an expression to the level of an atomic expression.

	@spark.production('expr11 ::= none')
	@spark.production('expr11 ::= true')
	@spark.production('expr11 ::= false')
	@spark.production('expr11 ::= str')
	@spark.production('expr11 ::= int')
	@spark.production('expr11 ::= float')
	@spark.production('expr11 ::= date')
	@spark.production('expr11 ::= color')
	@spark.production('expr11 ::= name')
	def expr_atom(self, atom):
		return atom

	@spark.production('expr11 ::= [ ]')
	def expr_emptylist(self, _0, _1):
		return List(_0.start, _1.end)

	@spark.production('buildlist ::= [ expr0')
	def expr_buildlist(self, _0, expr):
		return List(_0.start, expr.end, expr)

	@spark.production('buildlist ::= buildlist , expr0')
	def expr_addlist(self, list, _0, expr):
		list.items.append(expr)
		list.end = expr.end
		return list

	@spark.production('expr11 ::= buildlist ]')
	def expr_finishlist(self, list, _0):
		list.end = _0.end
		return list

	@spark.production('expr11 ::= buildlist , ]')
	def expr_finishlist1(self, list, _0, _1):
		list.end = _1.end
		return list

	@spark.production('expr11 ::= { }')
	def expr_emptydict(self, _0, _1):
		return Dict(_0.start, _1.end)

	@spark.production('builddict ::= { expr0 : expr0')
	def expr_builddict(self, _0, exprkey, _1, exprvalue):
		return Dict(_0.start, exprvalue.end, (exprkey, exprvalue))

	@spark.production('builddict ::= { ** expr0')
	def expr_builddictupdate(self, _0, _1, expr):
		return Dict(_0.start, expr.end, (expr,))

	@spark.production('builddict ::= builddict , expr0 : expr0')
	def expr_adddict(self, dict, _0, exprkey, _1, exprvalue):
		dict.items.append((exprkey, exprvalue))
		dict.end = exprvalue.end
		return dict

	@spark.production('builddict ::= builddict , ** expr0')
	def expr_updatedict(self, dict, _0, _1, expr):
		dict.items.append((expr,))
		dict.end = expr.end
		return dict

	@spark.production('expr11 ::= builddict }')
	def expr_finishdict(self, dict, _0):
		dict.end = _0.end
		return dict

	@spark.production('expr11 ::= builddict , }')
	def expr_finishdict1(self, dict, _0, _1):
		dict.end = _1.end
		return dict

	@spark.production('expr11 ::= ( expr0 )')
	def expr_bracket(self, _0, expr, _1):
		return expr

	@spark.production('expr10 ::= name ( )')
	def expr_callfunc0(self, name, _0, _1):
		return CallFunc(name.start, _1.end, name, [])

	@spark.production('expr10 ::= name ( expr0 )')
	def expr_callfunc1(self, name, _0, arg0, _1):
		return CallFunc(name.start, _1.end, name, [arg0])

	@spark.production('expr10 ::= name ( expr0 , expr0 )')
	def expr_callfunc2(self, name, _0, arg0, _1, arg1, _2):
		return CallFunc(name.start, _2.end, name, [arg0, arg1])

	@spark.production('expr10 ::= name ( expr0 , expr0 , expr0 )')
	def expr_callfunc3(self, name, _0, arg0, _1, arg1, _2, arg2, _3):
		return CallFunc(name.start, _3.end, name, [arg0, arg1, arg2])

	@spark.production('expr10 ::= name ( expr0 , expr0 , expr0 , expr0 )')
	def expr_callfunc4(self, name, _0, arg0, _1, arg1, _2, arg2, _3, arg3, _4):
		return CallFunc(name.start, _4.end, name, [arg0, arg1, arg2, arg3])

	@spark.production('expr9 ::= expr9 . name')
	def expr_getattr(self, expr, _0, name):
		return GetAttr(expr.start, name.end, expr, name)

	@spark.production('expr9 ::= expr9 . name ( )')
	def expr_callmeth0(self, expr, _0, name, _1, _2):
		return CallMeth(expr.start, _2.end, name, expr, [])

	@spark.production('expr9 ::= expr9 . name ( expr0 )')
	def expr_callmeth1(self, expr, _0, name, _1, arg1, _2):
		return CallMeth(expr.start, _2.end, name, expr, [arg1])

	@spark.production('expr9 ::= expr9 . name ( expr0 , expr0 )')
	def expr_callmeth2(self, expr, _0, name, _1, arg1, _2, arg2, _3):
		return CallMeth(expr.start, _3.end, name, expr, [arg1, arg2])

	@spark.production('expr9 ::= expr9 . name ( expr0 , expr0 , expr0 )')
	def expr_callmeth3(self, expr, _0, name, _1, arg1, _2, arg2, _3, arg3, _4):
		return CallMeth(expr.start, _4.end, name, expr, [arg1, arg2, arg3])

	@spark.production('callmethkw ::= expr9 . name ( name = expr0')
	def methkw_startname(self, expr, _0, methname, _1, argname, _2, argvalue):
		return CallMethKeywords(expr.start, argvalue.end, methname, expr, [(argname, argvalue)])

	@spark.production('callmethkw ::= expr9 . name ( ** expr0')
	def methkw_startdict(self, expr, _0, methname, _1, _2, argvalue):
		return CallMethKeywords(expr.start, argvalue.end, methname, expr, [(argvalue,)])

	@spark.production('callmethkw ::= callmethkw , name = expr0')
	def methkw_buildname(self, call, _0, argname, _1, argvalue):
		call.args.append((argname, argvalue))
		call.end = argvalue.end
		return call

	@spark.production('callmethkw ::= callmethkw , ** expr0')
	def methkw_builddict(self, call, _0, _1, argvalue):
		call.args.append((argvalue,))
		call.end = argvalue.end
		return call

	@spark.production('expr9 ::= callmethkw )')
	def methkw_finish(self, call, _0):
		call.end = _0.end
		return call

	@spark.production('expr9 ::= expr9 [ expr0 ]')
	def expr_getitem(self, expr, _0, key, _1):
		if isinstance(expr, Const) and isinstance(key, Const): # Constant folding
			return self.makeconst(expr.start, _1.end, expr.value[key.value])
		return GetItem(expr.start, _1.end, expr, key)

	@spark.production('expr8 ::= expr8 [ expr0 : expr0 ]')
	def expr_getslice12(self, expr, _0, index1, _1, index2, _2):
		if isinstance(expr, Const) and isinstance(index1, Const) and isinstance(index2, Const): # Constant folding
			return self.makeconst(expr.start, _2.end, expr.value[index1.value:index2.value])
		return GetSlice12(expr.start, _2.end, expr, index1, index2)

	@spark.production('expr8 ::= expr8 [ expr0 : ]')
	def expr_getslice1(self, expr, _0, index1, _1, _2):
		if isinstance(expr, Const) and isinstance(index1, Const): # Constant folding
			return self.makeconst(expr.start, _2.end, expr.value[index1.value:])
		return GetSlice1(expr.start, _2.end, expr, index1)

	@spark.production('expr8 ::= expr8 [ : expr0 ]')
	def expr_getslice2(self, expr, _0, _1, index2, _2):
		if isinstance(expr, Const) and isinstance(index2, Const): # Constant folding
			return self.makeconst(expr.start, _2.end, expr.value[:index2.value])
		return GetSlice2(expr.start, _2.end, expr, index2)

	@spark.production('expr7 ::= - expr7')
	def expr_neg(self, _0, expr):
		if isinstance(expr, Const): # Constant folding
			return self.makeconst(_0.start, expr.end, -expr.value)
		return Neg(_0.start, expr.end, expr)

	@spark.production('expr6 ::= expr6 * expr6')
	def expr_mul(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value * obj2.value)
		return Mul(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr6 ::= expr6 // expr6')
	def expr_floordiv(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value // obj2.value)
		return FloorDiv(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr6 ::= expr6 / expr6')
	def expr_truediv(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value / obj2.value)
		return TrueDiv(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr6 ::= expr6 % expr6')
	def expr_mod(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value % obj2.value)
		return Mod(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr5 ::= expr5 + expr5')
	def expr_add(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value + obj2.value)
		return Add(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr5 ::= expr5 - expr5')
	def expr_sub(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value - obj2.value)
		return Sub(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr4 ::= expr4 == expr4')
	def expr_eq(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value == obj2.value)
		return EQ(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr4 ::= expr4 != expr4')
	def expr_ne(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value != obj2.value)
		return NE(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr4 ::= expr4 < expr4')
	def expr_lt(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value < obj2.value)
		return LT(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr4 ::= expr4 <= expr4')
	def expr_le(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value <= obj2.value)
		return LE(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr4 ::= expr4 > expr4')
	def expr_gt(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value > obj2.value)
		return GT(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr4 ::= expr4 >= expr4')
	def expr_ge(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, obj1.value >= obj2.value)
		return GE(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr3 ::= expr3 in expr3')
	def expr_contains(self, obj, _0, container):
		if isinstance(obj, Const) and isinstance(container, Const): # Constant folding
			return self.makeconst(obj.start, container.end, obj.value in container.value)
		return Contains(obj.start, container.end, obj, container)

	@spark.production('expr3 ::= expr3 not in expr3')
	def expr_notcontains(self, obj, _0, _1, container):
		if isinstance(obj, Const) and isinstance(container, Const): # Constant folding
			return self.makeconst(obj.start, container.end, obj.value not in container.value)
		return NotContains(obj.start, container.end, obj, container)

	@spark.production('expr2 ::= not expr2')
	def expr_not(self, _0, expr):
		if isinstance(expr, Const): # Constant folding
			return self.makeconst(_0.start, expr.end, not expr.value)
		return Not(_0.start, expr.end, expr)

	@spark.production('expr1 ::= expr1 and expr1')
	def expr_and(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, bool(obj1.value and obj2.value))
		return And(obj1.start, obj2.end, obj1, obj2)

	@spark.production('expr0 ::= expr0 or expr0')
	def expr_or(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.start, obj2.end, bool(obj1.value or obj2.value))
		return Or(obj1.start, obj2.end, obj1, obj2)

	# These rules make operators of different precedences interoperable, by allowing an expression to "drop" its precedence.
	@spark.production('expr10 ::= expr11')
	@spark.production('expr9 ::= expr10')
	@spark.production('expr8 ::= expr9')
	@spark.production('expr7 ::= expr8')
	@spark.production('expr6 ::= expr7')
	@spark.production('expr5 ::= expr6')
	@spark.production('expr4 ::= expr5')
	@spark.production('expr3 ::= expr4')
	@spark.production('expr2 ::= expr3')
	@spark.production('expr1 ::= expr2')
	@spark.production('expr0 ::= expr1')
	def expr_dropprecedence(self, expr):
		return expr


class ForParser(ExprParser):
	emptyerror = "loop expression required"
	start = "for"

	@spark.production('for ::= name in expr0')
	def for0(self, iter, _0, cont):
		return For(iter.start, cont.end, iter, cont)

	@spark.production('for ::= ( name , ) in expr0')
	def for1(self, _0, iter, _1, _2, _3, cont):
		return For(_0.start, cont.end, [iter], cont)

	@spark.production('for ::= ( name , name ) in expr0')
	def for2a(self, _0, iter1, _1, iter2, _2, _3, cont):
		return For(_0.start, cont.end, [iter1, iter2], cont)

	@spark.production('for ::= ( name , name , ) in expr0')
	def for2b(self, _0, iter1, _1, iter2, _2, _3, _4, cont):
		return For(_0.start, cont.end, [iter1, iter2], cont)

	@spark.production('for ::= ( name , name , name ) in expr0')
	def for3a(self, _0, iter1, _1, iter2, _2, iter3, _3, _4, cont):
		return For(_0.start, cont.end, [iter1, iter2, iter3], cont)

	@spark.production('for ::= ( name , name , name , ) in expr0')
	def for3b(self, _0, iter1, _1, iter2, _2, iter3, _3, _4, _5, cont):
		return For(_0.start, cont.end, [iter1, iter2, iter3], cont)


class StmtParser(ExprParser):
	emptyerror = "statement required"
	start = "stmt"

	@spark.production('stmt ::= name = expr0')
	def stmt_assign(self, name, _0, value):
		return StoreVar(name.start, value.end, name, value)

	@spark.production('stmt ::= name += expr0')
	def stmt_iadd(self, name, _0, value):
		return AddVar(name.start, value.end, name, value)

	@spark.production('stmt ::= name -= expr0')
	def stmt_isub(self, name, _0, value):
		return SubVar(name.start, value.end, name, value)

	@spark.production('stmt ::= name *= expr0')
	def stmt_imul(self, name, _0, value):
		return MulVar(name.start, value.end, name, value)

	@spark.production('stmt ::= name /= expr0')
	def stmt_itruediv(self, name, _0, value):
		return TrueDivVar(name.start, value.end, name, value)

	@spark.production('stmt ::= name //= expr0')
	def stmt_ifloordiv(self, name, _0, value):
		return FloorDivVar(name.start, value.end, name, value)

	@spark.production('stmt ::= name %= expr0')
	def stmt_imod(self, name, _0, value):
		return ModVar(name.start, value.end, name, value)

	@spark.production('stmt ::= del name')
	def stmt_del(self, _0, name):
		return DelVar(_0.start, name.end, name)


class RenderParser(ExprParser):
	emptyerror = "render statement required"
	start = "render"

	@spark.production('render ::= expr0 ( )')
	def emptyrender(self, template, _0, _1):
		return Render(template.start, _1.end, template)

	@spark.production('buildrender ::= expr0 ( name = expr0')
	def startrender(self, template, _0, argname, _1, argvalue):
		return Render(template.start, argvalue.end, template, (argname, argvalue))

	@spark.production('buildrender ::= expr0 ( ** expr0')
	def startrenderupdate(self, template, _0, _1, arg):
		return Render(template.start, arg.end, template, (arg, ))

	@spark.production('buildrender ::= buildrender , name = expr0')
	def buildrender(self, render, _0, argname, _1, argvalue):
		render.variables.append((argname, argvalue))
		render.end = argvalue.end
		return render

	@spark.production('buildrender ::= buildrender , ** expr0')
	def buildrenderupdate(self, render, _0, _1, arg):
		render.variables.append((arg,))
		render.end = arg.end
		return render

	@spark.production('render ::= buildrender )')
	def finishrender(self, render, _0):
		render.end = _0.end
		return render

	@spark.production('render ::= buildrender , )')
	def finishrender1(self, render, _0, _1):
		render.end = _1.end
		return render


###
### Helper functions used at template runtime
###

def _repr(obj):
	"""
	Helper for the ``repr`` function.
	"""
	if isinstance(obj, unicode):
		return unicode(repr(obj)[1:])
	elif isinstance(obj, str):
		return unicode(repr(obj))
	elif isinstance(obj, datetime.datetime):
		s = unicode(obj.isoformat())
		if s.endswith(u"T00:00:00"):
			return u"@{}T".format(s[:-9])
		else:
			return u"@" + s
	elif isinstance(obj, datetime.date):
		return u"@{}T".format(obj.isoformat())
	elif isinstance(obj, color.Color):
		if obj[3] == 0xff:
			s = "#{:02x}{:02x}{:02x}".format(obj[0], obj[1], obj[2])
			if s[1]==s[2] and s[3]==s[4] and s[5]==s[6]:
				return "#{}{}{}".format(s[1], s[3], s[5])
			return s
		else:
			s = "#{:02x}{:02x}{:02x}{:02x}".format(*obj)
			if s[1]==s[2] and s[3]==s[4] and s[5]==s[6] and s[7]==s[8]:
				return "#{}{}{}{}".format(s[1], s[3], s[5], s[7])
			return s
	elif isinstance(obj, collections.Sequence):
		return u"[{}]".format(u", ".join(_repr(item) for item in obj))
	elif isinstance(obj, collections.Mapping):
		return u"{{{}}}".format(u", ".join(u"{}: {}".format(_repr(key), _repr(value)) for (key, value) in obj.iteritems()))
	else:
		return unicode(repr(obj))


def _json(obj):
	"""
	Helper for the ``json`` function.
	"""
	if obj is None:
		return u"null"
	if isinstance(obj, (bool, int, long, float, basestring)):
		return json.dumps(obj)
	elif isinstance(obj, datetime.datetime):
		return format(obj, u"new Date({}, {}, {}, {}, {}, {}, {})".format(obj.year, obj.month-1, obj.day, obj.hour, obj.minute, obj.second, obj.microsecond//1000))
	elif isinstance(obj, datetime.date):
		return format(obj, u"new Date({}, {}, {})".format(obj.year, obj.month-1, obj.day))
	elif isinstance(obj, color.Color):
		return u"ul4.Color.create({}, {}, {}, {})".format(*obj)
	elif isinstance(obj, collections.Mapping):
		return u"{{{}}}".format(u", ".join(u"{}: {}".format(_json(key), _json(value)) for (key, value) in obj.iteritems()))
	elif isinstance(obj, collections.Sequence):
		return u"[{}]".format(u", ".join(_json(item) for item in obj))
	elif isinstance(obj, Template):
		return obj.jssource()
	else:
		raise TypeError("can't handle object of type {}".format(type(obj)))


def _oct(value):
		"""
		Helper for the ``oct`` function.
		"""
		if value == 0:
			return "0o0"
		elif value < 0:
			return "-0o" + oct(value)[2:]
		else:
			return "0o" + oct(value)[1:]


def _csv(obj):
	"""
	Helper for the ``csv`` function.
	"""
	if obj is None:
		return u""
	elif not isinstance(obj, basestring):
		obj = _repr(obj)
	if any(c in obj for c in ',"\n'):
		return u'"{}"'.format(obj.replace('"', '""'))
	return obj


def _type(obj):
	"""
	Helper for the ``type`` function.
	"""
	if obj is None:
		return u"none"
	elif isinstance(obj, basestring):
		return u"str"
	elif isinstance(obj, bool):
		return u"bool"
	elif isinstance(obj, (int, long)):
		return u"int"
	elif isinstance(obj, float):
		return u"float"
	elif isinstance(obj, (datetime.datetime, datetime.date)):
		return u"date"
	elif isinstance(obj, color.Color):
		return u"color"
	elif isinstance(obj, collections.Mapping):
		return u"dict"
	elif isinstance(obj, collections.Sequence):
		return u"list"
	elif hasattr(obj, "__call__"):
		return u"template"
	elif isinstance(obj, color.Color):
		return u"color"
	return None


def _mimeformat(obj):
	"""
	Helper for the ``mimeformat`` method.
	"""
	weekdayname = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
	monthname = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
	return "{1}, {0.day:02d} {2:3} {0.year:4} {0.hour:02}:{0.minute:02}:{0.second:02} GMT".format(obj, weekdayname[obj.weekday()], monthname[obj.month])


def _yearday(obj):
	"""
	Helper for the ``yearday`` method.
	"""
	return (obj - obj.__class__(obj.year, 1, 1)).days+1


def _isoformat(obj):
	"""
	Helper for the ``isoformat`` method.
	"""
	result = obj.isoformat()
	suffix = "T00:00:00"
	if result.endswith(suffix):
		return result[:-len(suffix)]
	return result
