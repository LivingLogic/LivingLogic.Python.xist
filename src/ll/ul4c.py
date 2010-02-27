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


import re, datetime, StringIO, locale

from ll import spark, color


# Regular expression used for splitting dates
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

	@property
	def code(self):
		return self.source[self.startcode:self.endcode]

	@property
	def tag(self):
		return self.source[self.starttag:self.endtag]

	def __repr__(self):
		return "<%s.%s %s at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self, id(self))

	def pos(self):
		lastlinefeed = self.source.rfind("\n", 0, self.starttag)
		if lastlinefeed >= 0:
			return (self.source.count("\n", 0, self.starttag)+1, self.starttag-lastlinefeed)
		else:
			return (1, self.starttag + 1)

	def __str__(self):
		(line, col) = self.pos()
		return "%r at %d (line %d, col %d)" % (self.tag, self.starttag+1, line, col)


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
		return "<%s.%s in %s at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.location, id(self))

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
			name = "%s.%s" % (module, name)
		return "%s %s %s" % (name, " ".join("in %s:" % location for location in path), exc)


class LexicalError(Exception):
	def __init__(self, start, end, input):
		self.start = start
		self.end = end
		self.input = input

	def __str__(self):
		return "Unmatched input %r" % self.input


class SyntaxError(Exception):
	def __init__(self, token):
		self.token = token

	def __str__(self):
		return "Lexical error near %r" % str(self.token)


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
		return "function %r unknown" % self.funcname


class UnknownMethodError(Exception):
	"""
	Exception that is raised by the renderer if the method to be executed by the
	``callmeth0``, ``callmeth1``, ``callmeth2``  or ``callmeth3`` opcodes is
	unknown.
	"""

	def __init__(self, methname):
		self.methname = methname

	def __str__(self):
		return "method %r unknown" % self.methname


class UnknownOpcodeError(Exception):
	"""
	Exception that is raised when an unknown opcode is encountered by the renderer.
	"""

	def __init__(self, opcode):
		self.opcode = opcode

	def __str__(self):
		return "opcode %r unknown" % self.opcode


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

	def __repr__(self):
		v = ["<", self.__class__.__name__, " code=%r" % self.code]
		for attrname in ("r1", "r2", "r3", "r4", "r5", "arg"):
			attr = getattr(self, attrname)
			if attr is not None:
				v.append(" %s=%r" % (attrname, attr))
		if self.code is None:
			v.append(" text=%r" % self.location.code)
		v.append(" at 0x%x>" % id(self))
		return "".join(v)

	def __str__(self):
		if self.code is None:
			return "print %r" % self.location.code
		elif self.code == "print":
			return "print r%r" % self.r1
		elif self.code == "printx":
			return "print xmlescape(r%r)" % self.r1
		elif self.code == "loadnone":
			return "r%r = None" % self.r1
		elif self.code == "loadfalse":
			return "r%r = False" % self.r1
		elif self.code == "loadtrue":
			return "r%r = True" % self.r1
		elif self.code == "loadstr":
			return "r%r = %r" % (self.r1, self.arg)
		elif self.code == "loadint":
			return "r%r = %s" % (self.r1, self.arg)
		elif self.code == "loadfloat":
			return "r%r = %s" % (self.r1, self.arg)
		elif self.code == "loaddate":
			return "r%r = %s" % (self.r1, self.arg)
		elif self.code == "loadcolor":
			return "r%r = #%s" % (self.r1, self.arg)
		elif self.code == "buildlist":
			return "r%r = []" % (self.r1)
		elif self.code == "builddict":
			return "r%r = {}" % (self.r1)
		elif self.code == "addlist":
			return "r%r.append(r%r)" % (self.r1, self.r2)
		elif self.code == "adddict":
			return "r%r[r%r] = r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "updatedict":
			return "r%r.update(r%r)" % (self.r1, self.r2)
		elif self.code == "loadvar":
			return "r%r = vars[%r]" % (self.r1, self.arg)
		elif self.code == "storevar":
			return "vars[%r] = r%r" % (self.arg, self.r1)
		elif self.code == "addvar":
			return "vars[%r] += r%r" % (self.arg, self.r1)
		elif self.code == "subvar":
			return "vars[%r] -= r%r" % (self.arg, self.r1)
		elif self.code == "mulvar":
			return "vars[%r] *= r%r" % (self.arg, self.r1)
		elif self.code == "truedivvar":
			return "vars[%r] /= r%r" % (self.arg, self.r1)
		elif self.code == "floordivvar":
			return "vars[%r] //= r%r" % (self.arg, self.r1)
		elif self.code == "modvar":
			return "vars[%r] %%= r%r" % (self.arg, self.r1)
		elif self.code == "delvar":
			return "del vars[%r]" % self.arg
		elif self.code == "for":
			return "for r%r in r%r" % (self.r1, self.r2)
		elif self.code == "endfor":
			return "endfor"
		elif self.code == "break":
			return "break"
		elif self.code == "continue":
			return "continue"
		elif self.code == "if":
			return "if r%r" % self.r1
		elif self.code == "else":
			return "else"
		elif self.code == "endif":
			return "endif"
		elif self.code == "getattr":
			return "r%r = getattr(r%r, %r)" % (self.r1, self.r2, self.arg)
		elif self.code == "getitem":
			return "r%r = r%r[r%r]" % (self.r1, self.r2, self.r3)
		elif self.code == "getslice1":
			return "r%r = r%r[r%r:]" % (self.r1, self.r2, self.r3)
		elif self.code == "getslice2":
			return "r%r = r%r[:r%r]" % (self.r1, self.r2, self.r3)
		elif self.code == "getslice12":
			return "r%r = r%r[r%r:r%r]" % (self.r1, self.r2, self.r3, self.r4)
		elif self.code == "not":
			return "r%r = not r%r" % (self.r1, self.r2)
		elif self.code == "eq":
			return "r%r = r%r == r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "ne":
			return "r%r = r%r != r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "lt":
			return "r%r = r%r < r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "le":
			return "r%r = r%r <= r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "gt":
			return "r%r = r%r > r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "ge":
			return "r%r = r%r >= r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "contains":
			return "r%r = r%r in r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "notcontains":
			return "r%r = r%r not in r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "add":
			return "r%r = r%r + r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "sub":
			return "r%r = r%r - r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "mul":
			return "r%r = r%r * r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "floordiv":
			return "r%r = r%r // r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "truediv":
			return "r%r = r%r / r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "and":
			return "r%r = r%r and r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "or":
			return "r%r = r%r or r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "mod":
			return "r%r = r%r %% r%r" % (self.r1, self.r2, self.r3)
		elif self.code == "neg":
			return "r%r = -r%r" % (self.r1, self.r2)
		elif self.code == "callfunc0":
			return "r%r = %s()" % (self.r1, self.arg)
		elif self.code == "callfunc1":
			return "r%r = %s(r%r)" % (self.r1, self.arg, self.r2)
		elif self.code == "callfunc2":
			return "r%r = %s(r%r, r%r)" % (self.r1, self.arg, self.r2, self.r3)
		elif self.code == "callfunc3":
			return "r%r = %s(r%r, r%r, r%r)" % (self.r1, self.arg, self.r2, self.r3, self.r4)
		elif self.code == "callfunc4":
			return "r%r = %s(r%r, r%r, r%r, r%r)" % (self.r1, self.arg, self.r2, self.r3, self.r4, self.r5)
		elif self.code == "callmeth0":
			return "r%r = r%r.%s()" % (self.r1, self.r2, self.arg)
		elif self.code == "callmeth1":
			return "r%r = r%r.%s(r%r)" % (self.r1, self.r2, self.arg, self.r3)
		elif self.code == "callmeth2":
			return "r%r = r%r.%s(r%r, r%r)" % (self.r1, self.r2, self.arg, self.r3, self.r4)
		elif self.code == "callmeth3":
			return "r%r = r%r.%s(r%r, r%r, r%r)" % (self.r1, self.r2, self.arg, self.r3, self.r4, self.r5)
		elif self.code == "callmethkw":
			return "r%r = r%r.%s(**r%r)" % (self.r1, self.r2, self.arg, self.r3)
		elif self.code == "render":
			return "render r%r(r%r)" % (self.r1, self.r2)
		elif self.code == "def":
			return "def %s(vars)" % self.arg
		elif self.code == "enddef":
			return "endfor"
		else:
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
	version = "11"

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
		# Stack for currently open def opcodes
		self.defs = []
		if source is not None:
			self._compile(source, startdelim, enddelim)

	@classmethod
	def loads(cls, data):
		"""
		The class method :meth:`loads` loads the template from string :var:`data`.
		:var:`data` must contain the template in compiled format.
		"""
		def _readint(term):
			i = 0
			while True:
				c = stream.read(1)
				if c.isdigit():
					i = 10*i+int(c)
				elif c == term:
					return i
				else:
					raise ValueError("invalid terminator, expected %r, got %r" % (term, c))

		def _readstr(term):
			i = 0
			digit = False
			while True:
				c = stream.read(1)
				if c.isdigit():
					i = 10*i+int(c)
					digit = True
				elif c == term:
					if digit:
						break
					return None
				else:
					raise ValueError("invalid terminator, expected %r, got %r" % (term, c))
			s = stream.read(i)
			if len(s) != i:
				raise ValueError("short read")
			return s

		def _readspec():
			c = stream.read(1)
			if c == "-":
				return None
			elif c.isdigit():
				return int(c)
			else:
				raise ValueError("invalid register spec %r" % c)

		def _readcr():
			c = stream.read(1)
			if c != "\n":
				raise ValueError("invalid linefeed %r" % c)

		self = cls()
		stream = StringIO.StringIO(data)
		header = stream.readline()
		header = header.rstrip()
		if header != "ul4":
			raise ValueError("invalid header, expected 'ul4', got %r" % header)
		version = stream.readline()
		version = version.rstrip()
		if version != self.version:
			raise ValueError("invalid version, expected %r got, %r" % (self.version, version))
		self.startdelim = _readstr(u"<")
		_readcr()
		self.enddelim = _readstr(u">")
		_readcr()
		self.source = _readstr('"')
		self.opcodes = []
		_readcr()
		count = _readint(u"#")
		_readcr()
		location = None
		while count:
			r1 = _readspec()
			r2 = _readspec()
			r3 = _readspec()
			r4 = _readspec()
			r5 = _readspec()
			code = _readstr(":")
			arg = _readstr(".")
			locspec = stream.read(1)
			if locspec == u"^":
				if location is None:
					raise ValueError("no previous location")
			elif locspec == u"*":
				location = Location(self.source, _readstr("="), _readint("("), _readint(")"), _readint("{"), _readint("}"))
			else:
				raise ValueError("invalid location spec %r" % locspec)
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
		def _writeint(term, number):
			yield unicode(number)
			yield term

		def _writestr(term, string):
			if string is None:
				yield term
			else:
				yield str(len(string))
				yield term
				yield string

		yield "ul4\n%s\n" % self.version
		for p in _writestr("<", self.startdelim): yield p
		yield "\n"
		for p in _writestr(">", self.enddelim): yield p
		yield "\n"
		for p in _writestr('"', self.source): yield p
		yield "\n"
		for p in _writeint("#", len(self.opcodes)): yield p
		yield "\n"
		lastlocation = None
		for opcode in self.opcodes:
			yield str(opcode.r1) if opcode.r1 is not None else u"-"
			yield str(opcode.r2) if opcode.r2 is not None else u"-"
			yield str(opcode.r3) if opcode.r3 is not None else u"-"
			yield str(opcode.r4) if opcode.r4 is not None else u"-"
			yield str(opcode.r5) if opcode.r5 is not None else u"-"
			for p in _writestr(":", opcode.code): yield p
			for p in _writestr(".", opcode.arg): yield p
			if opcode.location is not lastlocation:
				lastlocation = opcode.location
				yield u"*"
				for p in _writestr("=", lastlocation.type): yield p
				for p in _writeint("(", lastlocation.starttag): yield p
				for p in _writeint(")", lastlocation.endtag): yield p
				for p in _writeint("{", lastlocation.startcode): yield p
				for p in _writeint("}", lastlocation.endcode): yield p
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

	def _pythonsource_line(self, location, line):
		self.lines.append("%s%s" % ("\t"*self.indent, line))
		if self.lastlocation is not location or not self.locations:
			self.locations.append((location.type, location.starttag, location.endtag, location.startcode, location.endcode))
			self.lastlocation = location
		self.lines2locs.append(len(self.locations)-1)

	def _pythonsource_dispatch_None(self, opcode):
		self._pythonsource_line(opcode.location, "yield %r" % opcode.location.code)
	def _pythonsource_dispatch_loadstr(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = %r" % (opcode.r1, opcode.arg))
	def _pythonsource_dispatch_loadint(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = %s" % (opcode.r1, opcode.arg))
	def _pythonsource_dispatch_loadfloat(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = %s" % (opcode.r1, opcode.arg))
	def _pythonsource_dispatch_loadnone(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = None" % opcode.r1)
	def _pythonsource_dispatch_loadfalse(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = False" % opcode.r1)
	def _pythonsource_dispatch_loadtrue(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = True" % opcode.r1)
	def _pythonsource_dispatch_loaddate(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = datetime.datetime(%s)" % (opcode.r1, ", ".join(str(int(p)) for p in datesplitter.split(opcode.arg))))
	def _pythonsource_dispatch_loadcolor(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = color.Color(0x%s, 0x%s, 0x%s, 0x%s)" % (opcode.r1, opcode.arg[:2], opcode.arg[2:4], opcode.arg[4:6], opcode.arg[6:]))
	def _pythonsource_dispatch_buildlist(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = []" % opcode.r1)
	def _pythonsource_dispatch_builddict(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = {}" % opcode.r1)
	def _pythonsource_dispatch_addlist(self, opcode):
		self._pythonsource_line(opcode.location, "r%d.append(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_adddict(self, opcode):
		self._pythonsource_line(opcode.location, "r%d[r%d] = r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_updatedict(self, opcode):
		self._pythonsource_line(opcode.location, "r%d.update(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_loadvar(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = variables[%r]" % (opcode.r1, opcode.arg))
	def _pythonsource_dispatch_storevar(self, opcode):
		self._pythonsource_line(opcode.location, "variables[%r] = r%d" % (opcode.arg, opcode.r1))
	def _pythonsource_dispatch_addvar(self, opcode):
		self._pythonsource_line(opcode.location, "variables[%r] += r%d" % (opcode.arg, opcode.r1))
	def _pythonsource_dispatch_subvar(self, opcode):
		self._pythonsource_line(opcode.location, "variables[%r] -= r%d" % (opcode.arg, opcode.r1))
	def _pythonsource_dispatch_mulvar(self, opcode):
		self._pythonsource_line(opcode.location, "variables[%r] *= r%d" % (opcode.arg, opcode.r1))
	def _pythonsource_dispatch_truedivvar(self, opcode):
		self._pythonsource_line(opcode.location, "variables[%r] /= r%d" % (opcode.arg, opcode.r1))
	def _pythonsource_dispatch_floordivvar(self, opcode):
		self._pythonsource_line(opcode.location, "variables[%r] //= r%d" % (opcode.arg, opcode.r1))
	def _pythonsource_dispatch_modvar(self, opcode):
		self._pythonsource_line(opcode.location, "variables[%r] %%= r%d" % (opcode.arg, opcode.r1))
	def _pythonsource_dispatch_delvar(self, opcode):
		self._pythonsource_line(opcode.location, "del variables[%r]" % opcode.arg)
	def _pythonsource_dispatch_getattr(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d[%r]" % (opcode.r1, opcode.r2, opcode.arg))
	def _pythonsource_dispatch_getitem(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d[r%d]" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_getslice12(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d[r%d:r%d]" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
	def _pythonsource_dispatch_getslice1(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d[r%d:]" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_getslice2(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d[:r%d]" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_print(self, opcode):
		self._pythonsource_line(opcode.location, "if r%d is not None: yield unicode(r%d)" % (opcode.r1, opcode.r1))
	def _pythonsource_dispatch_printx(self, opcode):
		self._pythonsource_line(opcode.location, "if r%d is not None: yield xmlescape(unicode(r%d))" % (opcode.r1, opcode.r1))
	def _pythonsource_dispatch_for(self, opcode):
		self._pythonsource_line(opcode.location, "for r%d in r%d:" % (opcode.r1, opcode.r2))
		self.indent += 1
	def _pythonsource_dispatch_endfor(self, opcode):
		# we don't have to check for empty loops here, as a ``<?for?>`` tag always generates at least one ``storevar`` opcode inside the loop
		self.indent -= 1
	def _pythonsource_dispatch_break(self, opcode):
		self._pythonsource_line(opcode.location, "break")
	def _pythonsource_dispatch_continue(self, opcode):
		self._pythonsource_line(opcode.location, "continue")
	def _pythonsource_dispatch_not(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = not r%d" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_neg(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = -r%d" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_contains(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d in r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_notcontains(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d not in r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_eq(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d == r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_ne(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d != r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_lt(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d < r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_le(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d <= r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_gt(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d > r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_ge(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d >= r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_add(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d + r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_sub(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d - r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_mul(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d * r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_floordiv(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d // r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_truediv(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d / r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_and(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d and r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_or(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d or r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_mod(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d %% r%d" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_callfunc0(self, opcode):
		try:
			getattr(self, "_pythonsource_dispatch_callfunc0_%s" % opcode.arg)(opcode)
		except AttributeError:
			raise UnknownFunctionError(opcode.arg)
	def _pythonsource_dispatch_callfunc1(self, opcode):
		try:
			getattr(self, "_pythonsource_dispatch_callfunc1_%s" % opcode.arg)(opcode)
		except AttributeError:
			raise UnknownFunctionError(opcode.arg)
	def _pythonsource_dispatch_callfunc2(self, opcode):
		try:
			getattr(self, "_pythonsource_dispatch_callfunc2_%s" % opcode.arg)(opcode)
		except AttributeError:
			raise UnknownFunctionError(opcode.arg)
	def _pythonsource_dispatch_callfunc3(self, opcode):
		try:
			getattr(self, "_pythonsource_dispatch_callfunc3_%s" % opcode.arg)(opcode)
		except AttributeError:
			raise UnknownFunctionError(opcode.arg)
	def _pythonsource_dispatch_callfunc4(self, opcode):
		try:
			getattr(self, "_pythonsource_dispatch_callfunc4_%s" % opcode.arg)(opcode)
		except AttributeError:
			raise UnknownFunctionError(opcode.arg)
	def _pythonsource_dispatch_callmeth0(self, opcode):
		if opcode.arg in ("split", "rsplit", "strip", "lstrip", "rstrip", "upper", "lower", "capitalize", "isoformat", "r", "g", "b", "a", "hls", "hlsa", "hsv", "hsva", "lum"):
			self._pythonsource_line(opcode.location, "r%d = r%d.%s()" % (opcode.r1, opcode.r2, opcode.arg))
		elif opcode.arg == "items":
			self._pythonsource_line(opcode.location, "r%d = r%d.iteritems()" % (opcode.r1, opcode.r2))
		elif opcode.arg == "render":
			self._pythonsource_line(opcode.location, 'r%d = "".join(r%d())' % (opcode.r1, opcode.r2))
		else:
			raise UnknownMethodError(opcode.arg)
	def _pythonsource_dispatch_callmeth1(self, opcode):
		if opcode.arg in ("split", "rsplit", "strip", "lstrip", "rstrip", "startswith", "endswith", "find", "get", "withlum", "witha"):
			self._pythonsource_line(opcode.location, "r%d = r%d.%s(r%d)" % (opcode.r1, opcode.r2, opcode.arg, opcode.r3))
		elif opcode.arg == "join":
			self._pythonsource_line(opcode.location, "r%d = r%d.join(unicode(x) for x in r%d)" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.arg == "format":
			self._pythonsource_line(opcode.location, "r%d = r%d.__format__(r%d)" % (opcode.r1, opcode.r2, opcode.r3))
		else:
			raise UnknownMethodError(opcode.arg)
	def _pythonsource_dispatch_callmeth2(self, opcode):
		if opcode.arg in ("split", "rsplit", "find", "replace", "get"):
			self._pythonsource_line(opcode.location, "r%d = r%d.%s(r%d, r%d)" % (opcode.r1, opcode.r2, opcode.arg, opcode.r3, opcode.r4))
		else:
			raise UnknownMethodError(opcode.arg)
	def _pythonsource_dispatch_callmeth3(self, opcode):
		if opcode.arg == "find":
			self._pythonsource_line(opcode.location, "r%d = r%d.%s(r%d, r%d, r%d)" % (opcode.r1, opcode.r2, opcode.arg, opcode.r3, opcode.r4, opcode.r5))
		else:
			raise UnknownMethodError(opcode.arg)
	def _pythonsource_dispatch_callmethkw(self, opcode):
		if opcode.arg == "render":
			self._pythonsource_line(opcode.location, 'r%d = "".join(r%d(**dict((key.encode("utf-8"), value) for (key, value) in r%d.iteritems())))' % (opcode.r1, opcode.r2, opcode.r3))
		else:
			raise UnknownMethodError(opcode.arg)
	def _pythonsource_dispatch_if(self, opcode):
		self._pythonsource_line(opcode.location, "if r%d:" % (opcode.r1))
		self.indent += 1
	def _pythonsource_dispatch_else(self, opcode):
		if self.lastopcode == "if":
			self.lines[-1] += " pass"
		self.indent -= 1
		self._pythonsource_line(opcode.location, "else:")
		self.indent += 1
	def _pythonsource_dispatch_endif(self, opcode):
		if self.lastopcode in ("if", "else"):
			lines[-1] += " pass"
		self.indent -= 1
	def _pythonsource_dispatch_def(self, opcode):
		self._pythonsource_line(opcode.location, "def _(**variables):")
		self.defs.append(opcode)
		self.indent += 1
		self._pythonsource_line(opcode.location, 'variables = dict((key.decode("utf-8"), value) for (key, value) in variables.iteritems())') # FIXME: This can be dropped in Python 3.0 where strings are unicode
		self._pythonsource_line(opcode.location, "r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = r8 = r9 = None")
		self._pythonsource_line(opcode.location, "try:")
		self.indent += 1
		# Make sure that the resulting code is a generator even if the byte codes produce no yield statement
		self._pythonsource_line(opcode.location, "if 0: yield ''")
	def _pythonsource_dispatch_enddef(self, opcode):
		defopcode = self.defs.pop()
		self.indent -= 1
		self._pythonsource_line(opcode.location, "except Exception, exc:")
		self.indent += 1
		self._pythonsource_line(opcode.location, "newexc = ul4c.Error(ul4c.Location(source, *locations[lines2locs[sys.exc_info()[2].tb_lineno-startline]]))") # FIXME: Use ``raise ... from`` in Python 3.0
		self._pythonsource_line(opcode.location, "newexc.__cause__ = exc")
		self._pythonsource_line(opcode.location, "raise newexc")
		self.indent -= 2
		self._pythonsource_line(opcode.location, "variables[%r] = _" % defopcode.arg)
	def _pythonsource_dispatch_render(self, opcode):
		self._pythonsource_line(opcode.location, 'for chunk in r%d(**dict((key.encode("utf-8"), value) for (key, value) in r%d.iteritems())): yield chunk' % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc0_now(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = datetime.datetime.now()" % opcode.r1)
	def _pythonsource_dispatch_callfunc0_vars(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = variables" % opcode.r1)
	def _pythonsource_dispatch_callfunc1_xmlescape(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = xmlescape(unicode(r%d)) if r%d is not None else u''" % (opcode.r1, opcode.r2, opcode.r2))
	def _pythonsource_dispatch_callfunc1_csv(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = ul4c._csv(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_json(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = json.dumps(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_str(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = unicode(r%d) if r%d is not None else u''" % (opcode.r1, opcode.r2, opcode.r2))
	def _pythonsource_dispatch_callfunc1_int(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = int(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_float(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = float(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_bool(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = bool(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_len(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = len(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_enumerate(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = enumerate(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_isnone(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = r%d is None" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_isstr(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = isinstance(r%d, basestring)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_isint(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = isinstance(r%d, (int, long)) and not isinstance(r%d, bool)" % (opcode.r1, opcode.r2, opcode.r2))
	def _pythonsource_dispatch_callfunc1_isfloat(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = isinstance(r%d, float)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_isbool(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = isinstance(r%d, bool)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_isdate(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = isinstance(r%d, datetime.datetime)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_islist(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = isinstance(r%d, (list, tuple)) and not isinstance(r%d, color.Color)" % (opcode.r1, opcode.r2, opcode.r2))
	def _pythonsource_dispatch_callfunc1_isdict(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = isinstance(r%d, dict)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_istemplate(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = hasattr(r%d, '__call__')" % (opcode.r1, opcode.r2)) # this supports normal generators too
	def _pythonsource_dispatch_callfunc1_iscolor(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = isinstance(r%d, color.Color)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_repr(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = ul4c._repr(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_get(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = variables.get(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_chr(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = unichr(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_ord(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = ord(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_hex(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = hex(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_oct(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = ul4c._oct(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_bin(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = bin(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_sorted(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = sorted(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_range(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = xrange(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_type(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = ul4c._type(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc1_reversed(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = reversed(r%d)" % (opcode.r1, opcode.r2))
	def _pythonsource_dispatch_callfunc2_range(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = xrange(r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_callfunc2_get(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = variables.get(r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_callfunc2_zip(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = itertools.izip(r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_callfunc2_int(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = int(r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3))
	def _pythonsource_dispatch_callfunc3_range(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = xrange(r%d, r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
	def _pythonsource_dispatch_callfunc3_zip(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = itertools.izip(r%d, r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
	def _pythonsource_dispatch_callfunc3_rgb(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = color.Color.fromrgb(r%d, r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
	def _pythonsource_dispatch_callfunc3_hls(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = color.Color.fromhls(r%d, r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
	def _pythonsource_dispatch_callfunc3_hsv(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = color.Color.fromhsv(r%d, r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
	def _pythonsource_dispatch_callfunc4_rgb(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = color.Color.fromrgb(r%d, r%d, r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4, opcode.r5))
	def _pythonsource_dispatch_callfunc4_hls(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = color.Color.fromhls(r%d, r%d, r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4, opcode.r5))
	def _pythonsource_dispatch_callfunc4_hsv(self, opcode):
		self._pythonsource_line(opcode.location, "r%d = color.Color.fromhsv(r%d, r%d, r%d, r%d)" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4, opcode.r5))

	def pythonsource(self, function=None):
		"""
		Return the template as Python source code. If :var:`function` is specified
		the code will be wrapped in a function with this name.
		"""

		self.indent = 0
		self.lines = []
		self.locations = []
		self.lines2locs = []
		self.lastopcode = None
		self.lastlocation = Location(self.source, None, 0, 0, 0, 0)

		if function is not None:
			self._pythonsource_line(self.lastlocation, "def %s(**variables):" % function)
			self.indent += 1
			self.lines2locs = [] # We initialize startline one line below, which restarts the counter
		self._pythonsource_line(self.lastlocation, "import sys, datetime, itertools, json; from ll.misc import xmlescape; from ll import ul4c, color; startline = sys._getframe().f_lineno") # The line number of this line
		self._pythonsource_line(self.lastlocation, "__1__")
		self._pythonsource_line(self.lastlocation, "__2__")
		self._pythonsource_line(self.lastlocation, "source = %r" % self.source)
		self._pythonsource_line(self.lastlocation, 'variables = dict((key.decode("utf-8"), value) for (key, value) in variables.iteritems())') # FIXME: This can be dropped in Python 3.0 where strings are unicode
		self._pythonsource_line(self.lastlocation, "r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = r8 = r9 = None")
		self._pythonsource_line(self.lastlocation, "try:")
		self.indent += 1
		# Make sure that the resulting code is a generator even if the byte codes produce no yield statement
		self._pythonsource_line(self.lastlocation, "if 0: yield ''")
		try:
			for opcode in self.opcodes:
				try:
					getattr(self, "_pythonsource_dispatch_%s" % opcode.code)(opcode)
				except AttributeError:
					raise UnknownOpcodeError(opcode.code)
				self.lastopcode = opcode.code
		except Exception, exc:
			newexc = Error(opcode.location) # FIXME: Use ``raise ... from`` in Python 3.0
			newexc.__cause__ = exc
			raise newexc
		self.indent -= 1
		self._pythonsource_line(self.lastlocation, "except Exception, exc:")
		self.indent += 1
		self._pythonsource_line(self.lastlocation, "newexc = ul4c.Error(ul4c.Location(source, *locations[lines2locs[sys.exc_info()[2].tb_lineno-startline]]))") # FIXME: Use ``raise ... from`` in Python 3.0
		self._pythonsource_line(self.lastlocation, "newexc.__cause__ = exc")
		self._pythonsource_line(self.lastlocation, "raise newexc")
		locoffset = 1+int(self.lines[0].strip() != "__1__")
		self.lines[locoffset] = self.lines[locoffset].replace("__1__", "locations = %r" % (tuple(self.locations),))
		self.lines[locoffset+1] = self.lines[locoffset+1].replace("__2__", "lines2locs = %r" % (tuple(self.lines2locs),))
		result = "\n".join(self.lines)
		del self.lastopcode
		del self.indent
		del self.lines
		del self.locations
		del self.lines2locs
		return result

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
		return "".join(self.render(**variables))

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
				yield "%s}" % (i*indent)
			elif opcode.code in ("for", "if", "def"):
				yield "%s%s {" % (i*indent, opcode)
			elif opcode.code == "else":
				yield "%s} else {" % (i*indent)
			else:
				yield "%s%s" % (i*indent, opcode)
			if opcode.code in ("for", "if", "else", "def"):
				i += 1

	def _tokenize(self, source, startdelim, enddelim):
		"""
		Tokenize the template source code :var:`source` into tags and non-tag
		text. :var:`startdelim` and :var:`enddelim` are used as the tag delimiters.

		This is a generator which produces :class:`Location` objects for each tag
		or non-tag text. It will be called by :meth:`_compile` internally.
		"""
		pattern = u"%s(printx|print|code|for|if|elif|else|end|break|continue|render|def|note)(\s*((.|\\n)*?)\s*)?%s" % (re.escape(startdelim), re.escape(enddelim))
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
							raise BlockError("illegal end value %r" % code)
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
					raise ValueError("unknown tag %r" % location.type)
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
		return "<%s.%s object with %d opcodes at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, len(self.opcodes), id(self))


def compile(source, startdelim="<?", enddelim="?>"):
	return Template(source, startdelim, enddelim)

load = Template.load
loads = Template.loads


###
### Tokens and nodes for the AST
###

class Token(object):
	def __init__(self, start, end, type):
		self.start = start
		self.end = end
		self.type = type

	def __repr__(self):
		return "%s(%r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.type)

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
		return "%s(%r, %r)" % (self.__class__.__name__, self.start, self.end)

	def compile(self, template):
		r = template._allocreg()
		template.opcode("load%s" % self.type, r1=r)
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
		return "%s(%r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.value)

	def compile(self, template):
		r = template._allocreg()
		template.opcode("load%s" % self.type, r1=r, arg=unicode(self.value))
		return r


class Int(Value):
	type = "int"


class Float(Value):
	type = "float"

	def compile(self, template):
		r = template._allocreg()
		template.opcode("load%s" % self.type, r1=r, arg=repr(self.value))
		return r


class Str(Value):
	type = "str"


class Date(Value):
	type = "date"

	def compile(self, template):
		r = template._allocreg()
		template.opcode("load%s" % self.type, r1=r, arg=self.value.isoformat())
		return r


class Color(Value):
	type = "color"

	def compile(self, template):
		r = template._allocreg()
		template.opcode("load%s" % self.type, r1=r, arg="%02x%02x%02x%02x" % self.value)
		return r


class List(AST):
	def __init__(self, start, end, *items):
		AST.__init__(self, start, end)
		self.items = list(items)

	def __repr__(self):
		return "%s(%r, %r, %s)" % (self.__class__.__name__, self.start, self.end, repr(self.items)[1:-1])

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
		return "%s(%r, %r, %s)" % (self.__class__.__name__, self.start, self.end, repr(self.items)[1:-1])

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
		return "%s(%r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.name)

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
		return "%s(%r, %r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.iter, self.cont)

	def compile(self, template):
		rc = self.cont.compile(template)
		ri = template._allocreg()
		template.opcode("for", r1=ri, r2=rc)
		if isinstance(self.iter, list):
			for (i, iter) in enumerate(self.iter):
				rii = template._allocreg()
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
		return "%s(%r, %r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.obj, self.attr)

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
		return "%s(%r, %r, %r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.obj, self.index1, self.index2)

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
		return "%s(%r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.obj)

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
		return "%s(%r, %r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.obj1, self.obj2)

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
		return "%s(%r, %r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.name, self.value)

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
		return "%s(%r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.name)

	def compile(self, template):
		template.opcode("delvar", arg=self.name.name)


class CallFunc(AST):
	def __init__(self, start, end, name, args):
		AST.__init__(self, start, end)
		self.name = name
		self.args = args

	def __repr__(self):
		if self.args:
			return "%s(%r, %r, %r, %s)" % (self.__class__.__name__, self.start, self.end, self.name, repr(self.args)[1:-1])
		else:
			return "%s(%r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.name)

	def compile(self, template):
		if len(self.args) == 0:
			r = template._allocreg()
			template.opcode("callfunc0", r1=r, arg=self.name.name)
			return r
		elif len(self.args) > 4:
			raise ValueError("%d function arguments not supported" % len(self.args))
		else:
			rs = [arg.compile(template) for arg in self.args]
			template.opcode("callfunc%d" % len(self.args), rs[0], *rs, **dict(arg=self.name.name)) # FIXME: Replace **dict(arg=) with arg= in Python 2.6?
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
			return "%s(%r, %r, %r, %r, %s)" % (self.__class__.__name__, self.start, self.end, self.name, self.obj, repr(self.args)[1:-1])
		else:
			return "%s(%r, %r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.name, self.obj)

	def compile(self, template):
		if len(self.args) > 3:
			raise ValueError("%d method arguments not supported" % len(self.args))
		ro = self.obj.compile(template)
		rs = [arg.compile(template) for arg in self.args]
		template.opcode("callmeth%d" % len(self.args), ro, ro, *rs, **dict(arg=self.name.name))
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
		return "%s(%r, %r, %r, %r, %r)" % (self.__class__.__name__, self.start, self.end, self.name, self.obj, self.args)

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
		return "%s(%r, %r, %r, %s)" % (self.__class__.__name__, self.start, self.end, self.template, repr(self.variables)[1:-1])

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

	# Must be before the int and float constants
	@spark.token("\\d{4}-\\d{2}-\\d{2}T(\\d{2}:\\d{2}(:\\d{2}(\\.\\d{6})?)?)?", "default")
	def date(self, start, end, s):
		self.rv.append(Date(start, end, datetime.datetime(*map(int, filter(None, datesplitter.split(s))))))

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
		elif isinstance(value, int):
			return Int(start, end, value)
		elif isinstance(value, float):
			return Float(start, end, value)
		elif isinstance(value, basestring):
			return Str(start, end, value)
		elif isinstance(value, color.Color):
			return Color(start, end, value)
		else:
			raise TypeError("can't convert %r" % value)

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
		return unicode(obj.isoformat())
	elif isinstance(obj, color.Color):
		if obj[3] == 0xff:
			s = "#%02x%02x%02x" % (obj[0], obj[1], obj[2])
			if s[1]==s[2] and s[3]==s[4] and s[5]==s[6]:
				return "#%s%s%s" % (s[1], s[3], s[5])
			return s
		else:
			s = "#%02x%02x%02x%02x" % obj
			if s[1]==s[2] and s[3]==s[4] and s[5]==s[6] and s[7]==s[8]:
				return "#%s%s%s%s" % (s[1], s[3], s[5], s[7])
			return s
	elif isinstance(obj, list):
		return u"[%s]" % u", ".join(_repr(item) for item in obj)
	elif isinstance(obj, dict):
		return u"{%s}" % u", ".join(u"%s: %s" % (_repr(key), _repr(value)) for (key, value) in obj.iteritems())
	else:
		return unicode(repr(obj))


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
		return u'"%s"' % obj.replace('"', '""')
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
	elif isinstance(obj, (list, tuple)):
		return u"list"
	elif isinstance(obj, dict):
		return u"dict"
	elif hasattr(obj, "__call__"):
		return u"template"
	elif isinstance(obj, color.Color):
		return u"color"
	return None
