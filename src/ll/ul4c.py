# -*- coding: utf-8 -*-

## Copyright 2009-2012 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2012 by Walter Dörwald
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



__docformat__ = "reStructuredText"


import re, datetime, io, locale, json, collections

from ll import spark, color, misc, ul4on


# Regular expression used for splitting dates in isoformat
datesplitter = re.compile("[-T:.]")


# Use internally by the UL4ON decoder to map names to classes
_names2classes = {}

###
### Location information
###

@ul4on.register("de.livinglogic.ul4.location")
class Location(object):
	"""
	A :class:`Location` object contains information about the location of a
	template tag.
	"""
	__slots__ = ("source", "type", "starttag", "endtag", "startcode", "endcode")

	def __init__(self, source=None, type=None, starttag=None, endtag=None, startcode=None, endcode=None):
		"""
		Create a new :class:`Location` object. The arguments have the following
		meaning:

			:var:`source`
				The complete source string

			:var:`type`
				The tag type (i.e. ``"for"``, ``"if"``, etc. or ``None`` for
				literal text)

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
		if key in {"source", "type", "starttag", "endtag", "startcode", "endcode"}:
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

	def ul4ondump(self, encoder):
		encoder.dump(self.source)
		encoder.dump(self.type)
		encoder.dump(self.starttag)
		encoder.dump(self.endtag)
		encoder.dump(self.startcode)
		encoder.dump(self.endcode)

	def ul4onload(self, decoder):
		self.source = decoder.load()
		self.type = decoder.load()
		self.starttag = decoder.load()
		self.endtag = decoder.load()
		self.startcode = decoder.load()
		self.endcode = decoder.load()


###
### Exceptions
###

class Error(Exception):
	"""
	Exception class that wraps another exception and provides a location.
	"""
	def __init__(self, location):
		self.location = location

	def __repr__(self):
		return "<{}.{} in {} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.location, id(self))

	def __str__(self):
		path = []

		return "in {}".format(self.location)


class LexicalError(Exception):
	def __init__(self, input):
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


###
### opcode class
###

class Opcode(object):
	"""
	An :class:`Opcode` stores an opcode. An :class:`Opcode` object has the
	following attributes:

	:attr:`code` : string or :const:`None`
		The opcode type (see below for a list).

	:attr:`r1`, :attr:`r2`, :attr:`r3`, :attr:`r4`, :attr:`r5` : integer or ``None``
		 Register specifications (for the sources or the target of the opcode)

	:attr:`arg` : string or :const:`None`
		Used if the opcode requires an additional argument (like a variable name
		or the value of a constant).

	:attr:`location` : :class:`Location` object
		The location of the tag to which this opcode belongs.

	The following opcode types are available:

	``None``:
		Print text. The text is available from ``location.code``.

	``"print"``:
		Print the content of register :attr:`r1`. (If the object in the register
		is not a string, it will be converted to a string first.)

	``"loadnone"``:

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
		register :attr:`r3` (which must be an ``int`` or ``None``) specifies
		the start index, the object in register :attr:`r4` specifies the end index.
		The result will be stored in register :attr:`r1`.

	``"getslice1"``:
		Similar to ``getslice12`` except that the end index is always the length
		of the object.

	``"getslice2"``:
		Similar to ``getslice12`` except that the start index is always 0 and the
		end index is in register :attr:`r3`.

	``"getslice"``:
		Similar to ``getslice12`` except that the start index is always 0 and the
		end index always the length of the object.

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
			"getslice": "r{op.r1!r} = r{op.r2!r}[:]",
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
			"def": "def {op.arg}(**vars)",
			"enddef": "endfor",
		}
		try:
			return formats[self.code].format(op=self)
		except KeyError:
			raise UnknownOpcodeError(self.code)


###
### Compiler stuff: Tokens and nodes for the AST
###

class Token(object):
	def __init__(self, location, type):
		self.location = location
		self.type = type

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.type)

	def __str__(self):
		return self.type


class AST(object):
	"""
	Baseclass for all syntax tree nodes.
	"""
	def __init__(self, location=None):
		self.location = location

	def ul4ondump(self, encoder):
		encoder.dump(self.location)

	def ul4onload(self, decoder):
		self.location = decoder.load()


@ul4on.register("de.livinglogic.ul4.text")
class Text(AST):
	def __init__(self, location=None):
		super().__init__(location)

	def formatpython(self, indent):
		return "{}yield {!r}\n".format(indent*"\t", self.location.code)


class Const(AST):
	"""
	Common baseclass for all constants (used for type testing in constant folding)
	"""

	def __repr__(self):
		return "{}()".format(self.__class__.__name__)


@ul4on.register("de.livinglogic.ul4.none")
class None_(Const):
	"""
	The constant ``None``.
	"""

	type = "none"
	value = None

	def formatpython(self, indent):
		return "None"


@ul4on.register("de.livinglogic.ul4.true")
class True_(Const):
	"""
	The boolean constant ``True``.
	"""

	type = "true"
	value = True

	def formatpython(self, indent):
		return "True"


@ul4on.register("de.livinglogic.ul4.false")
class False_(Const):
	"""
	The boolean constant ``False``.
	"""

	type = "false"
	value = False

	def formatpython(self, indent):
		return "False"


class Value(Const):
	def __init__(self, location=None, value=None):
		super().__init__(location)
		self.value = value

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.value)

	def formatpython(self, indent):
		return repr(self.value)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()


@ul4on.register("de.livinglogic.ul4.int")
class Int(Value):
	type = "int"


@ul4on.register("de.livinglogic.ul4.float")
class Float(Value):
	type = "float"


@ul4on.register("de.livinglogic.ul4.str")
class Str(Value):
	type = "str"


@ul4on.register("de.livinglogic.ul4.date")
class Date(Value):
	type = "date"


@ul4on.register("de.livinglogic.ul4.color")
class Color(Value):
	type = "color"

	def formatpython(self, indent):
		return "color.{!r}".format(self.value)


@ul4on.register("de.livinglogic.ul4.list")
class List(AST):
	def __init__(self, location=None, *items):
		super().__init__(location)
		self.items = list(items)

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, repr(self.items)[1:-1])

	def formatpython(self, indent):
		return "[{}]".format(", ".join(item.formatpython(indent) for item in self.items))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = decoder.load()


@ul4on.register("de.livinglogic.ul4.dict")
class Dict(AST):
	def __init__(self, location=None, *items):
		super().__init__(location)
		self.items = list(items)

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, repr(self.items)[1:-1])

	def formatpython(self, indent):
		return "ul4c._makedict({})".format(", ".join("({})".format(" ".join(v.formatpython(indent)+"," for v in item)) for item in self.items))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = map(tuple, decoder.load())


@ul4on.register("de.livinglogic.ul4.loadvar")
class Name(AST):
	type = "name"

	def __init__(self, location=None, name=None):
		super().__init__(location)
		self.name = name

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.name)

	def formatpython(self, indent):
		return "vars[{!r}]".format(self.name)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.name)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.name = decoder.load()


class Block(AST):
	def __init__(self, location=None):
		super().__init__(location)
		self.content = []

	def append(self, item):
		self.content.append(item)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.content = decoder.load()


@ul4on.register("de.livinglogic.ul4.ieie")
class IfElIfElse(Block):
	def __init__(self, location=None, condition=None):
		super().__init__(location)
		if condition is not None:
			self.newblock(If(condition))

	def append(self, item):
		self.content[-1].append(item)

	def newblock(self, block):
		self.content.append(block)

	def formatpython(self, indent):
		v = []
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)


@ul4on.register("de.livinglogic.ul4.if")
class If(Block):
	def __init__(self, location=None, condition=None):
		super().__init__(location)
		self.condition = condition

	def formatpython(self, indent):
		v = []
		v.append("{}if {}:\n".format(indent*"\t", self.condition.formatpython(indent)))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()


@ul4on.register("de.livinglogic.ul4.elif")
class ElIf(Block):
	def __init__(self, location=None, condition=None):
		super().__init__(location)
		self.condition = condition

	def formatpython(self, indent):
		v = []
		v.append("{}elif {}:\n".format(indent*"\t", self.condition.formatpython(indent)))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()


@ul4on.register("de.livinglogic.ul4.else")
class Else(Block):
	def python(self, indent=None):
		v = []
		v.append("{}else:\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)


@ul4on.register("de.livinglogic.ul4.for")
class For(Block):
	def __init__(self, location=None, cont=None, varname=None):
		super().__init__(location)
		self.cont = cont
		self.varname = varname

	def __repr__(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.cont, self.varname)

	def formatpython(self, indent):
		v = []
		v.append("{}for vars[{!r}] in {}:\n".format(indent*"\t", self.varname, self.cont.formatpython(indent)))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.cont)
		encoder.dump(self.varname)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.cont = decoder.load()
		self.varname = decoder.load()


@ul4on.register("de.livinglogic.ul4.foru")
class ForUnpack(Block):
	def __init__(self, location=None, cont=None, *varnames):
		super().__init__(location)
		self.cont = cont
		self.varnames = list(varnames)

	def __repr__(self):
		return "{}({!r}, {})".format(self.__class__.__name__, self.cont, repr(self.varnames)[1:-1])

	def formatpython(self, indent):
		v = []
		v.append("{}for ({}) in {}:\n".format(indent*"\t", " ".join("vars[{!r}],".format(varname) for varname in self.varnames), self.cont.formatpython(indent)))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.cont)
		encoder.dump(self.varnames)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.cont = decoder.load()
		self.varnames = decoder.load()


@ul4on.register("de.livinglogic.ul4.break")
class Break(AST):
	def formatpython(self, indent):
		return "{}break\n".format(indent*"\t")


@ul4on.register("de.livinglogic.ul4.continue")
class Continue(AST):
	def formatpython(self, indent):
		return "{}continue\n".format(indent*"\t")


@ul4on.register("de.livinglogic.ul4.getattr")
class GetAttr(AST):
	def __init__(self, location=None, obj=None, attrname=None):
		super().__init__(location)
		self.obj = obj
		self.attrname = attrname

	def __repr__(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.obj, self.attrname)

	def formatpython(self, indent):
		return "{}[{!r}]".format(self.obj.formatpython(indent), self.attrname)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.attrname)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.attrname = decoder.load()


@ul4on.register("de.livinglogic.ul4.getslice")
class GetSlice(AST):
	def __init__(self, location=None, obj=None, index1=None, index2=None):
		super().__init__(location)
		self.obj = obj
		self.index1 = index1
		self.index2 = index2

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.obj, self.index1, self.index2)

	def formatpython(self, indent):
		return "{}[{}:{}]".format(self.obj.formatpython(indent), self.index1.formatpython(indent) if self.index1 is not None else "", self.index2.formatpython(indent) if self.index2 is not None else "")

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.index1)
		encoder.dump(self.index2)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.index1 = decoder.load()
		self.index2 = decoder.load()


class Unary(AST):
	def __init__(self, location=None, obj=None):
		super().__init__(location)
		self.obj = obj

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.obj)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()


@ul4on.register("de.livinglogic.ul4.not")
class Not(Unary):
	def formatpython(self, indent):
		return " not ({})".format(self.obj.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.neg")
class Neg(Unary):
	def formatpython(self, indent):
		return " -({})".format(self.obj.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.print")
class Print(Unary):
	def formatpython(self, indent):
		return "{}yield ul4c._str({})\n".format(indent*"\t", self.obj.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.printx")
class PrintX(Unary):
	def formatpython(self, indent):
		return "{}yield ul4c._xmlescape({})\n".format(indent*"\t", self.obj.formatpython(indent))


class Binary(AST):
	def __init__(self, location=None, obj1=None, obj2=None):
		super().__init__(location)
		self.obj1 = obj1
		self.obj2 = obj2

	def __repr__(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.obj1, self.obj2)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj1)
		encoder.dump(self.obj2)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj1 = decoder.load()
		self.obj2 = decoder.load()


@ul4on.register("de.livinglogic.ul4.getitem")
class GetItem(Binary):
	def formatpython(self, indent):
		return "{}[{}]".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.eq")
class EQ(Binary):
	def formatpython(self, indent):
		return "({}) == ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.ne")
class NE(Binary):
	def formatpython(self, indent):
		return "({}) != ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.lt")
class LT(Binary):
	def formatpython(self, indent):
		return "({}) < ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.le")
class LE(Binary):
	def formatpython(self, indent):
		return "({}) <= ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.gt")
class GT(Binary):
	def formatpython(self, indent):
		return "({}) > ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.ge")
class GE(Binary):
	def formatpython(self, indent):
		return "({}) >= ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.contains")
class Contains(Binary):
	def formatpython(self, indent):
		return "({}) in ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.notcontains")
class NotContains(Binary):
	def formatpython(self, indent):
		return "({}) not in ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.add")
class Add(Binary):
	def formatpython(self, indent):
		return "({}) + ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.sub")
class Sub(Binary):
	def formatpython(self, indent):
		return "({}) - ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.mul")
class Mul(Binary):
	def formatpython(self, indent):
		return "({}) * ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.floordiv")
class FloorDiv(Binary):
	def formatpython(self, indent):
		return "({}) // ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.truediv")
class TrueDiv(Binary):
	def formatpython(self, indent):
		return "({}) / ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.or")
class Or(Binary):
	def formatpython(self, indent):
		return "({}) or ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.and")
class And(Binary):
	def formatpython(self, indent):
		return "({}) and ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.mod")
class Mod(Binary):
	def formatpython(self, indent):
		return "({}) % ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


class ChangeVar(AST):
	def __init__(self, location=None, name=None, value=None):
		super().__init__(location)
		self.name = name
		self.value = value

	def __repr__(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.name, self.value)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.name)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.name = decoder.load()
		self.value = decoder.load()


@ul4on.register("de.livinglogic.ul4.storevar")
class StoreVar(ChangeVar):
	def formatpython(self, indent):
		return "{}vars[{!r}] = {}\n".format(indent*"\t", self.name, self.value.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.addvar")
class AddVar(ChangeVar):
	def formatpython(self, indent):
		return "{}vars[{!r}] += {}\n".format(indent*"\t", self.name, self.value.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.subvar")
class SubVar(ChangeVar):
	def formatpython(self, indent):
		return "{}vars[{!r}] -= {}\n".format(indent*"\t", self.name, self.value.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.mulvar")
class MulVar(ChangeVar):
	def formatpython(self, indent):
		return "{}vars[{!r}] *= {}\n".format(indent*"\t", self.name, self.value.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.floordivvar")
class FloorDivVar(ChangeVar):
	def formatpython(self, indent):
		return "{}vars[{!r}] //= {}\n".format(indent*"\t", self.name, self.value.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.truedivvar")
class TrueDivVar(ChangeVar):
	def formatpython(self, indent):
		return "{}vars[{!r}] /= {}\n".format(indent*"\t", self.name, self.value.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.modvar")
class ModVar(ChangeVar):
	def formatpython(self, indent):
		return "{}vars[{!r}] %= {}\n".format(indent*"\t", self.name, self.value.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.delvar")
class DelVar(AST):
	def __init__(self, location=None, name=None):
		super().__init__(location)
		self.name = name

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.name)

	def formatpython(self, indent):
		return "{}del vars[{!r}]\n".format(indent*"\t", self.name)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.name)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.name = decoder.load()


@ul4on.register("de.livinglogic.ul4.callfunc")
class CallFunc(AST):
	def __init__(self, location=None, funcname=None, *args):
		super().__init__(location)
		self.funcname = funcname
		self.args = list(args)

	def __repr__(self):
		if self.args:
			return "{}({!r}, {})".format(self.__class__.__name__, self.funcname, repr(self.args)[1:-1])
		else:
			return "{}({!r})".format(self.__class__.__name__, self.funcname)

	def formatpython(self, indent):
		functions = dict(
			now="datetime.datetime.now({})".format,
			utcnow="datetime.datetime.utcnow({})".format,
			vars="vars".format,
			random="random.random({})".format,
			xmlescape="ul4c._xmlescape({})".format,
			csv="ul4c._csv({})".format,
			json="ul4c._json({})".format,
			str="ul4c._str({})".format,
			int="int({})".format,
			float="float({})".format,
			bool="bool({})".format,
			len="len({})".format,
			abs="abs({})".format,
			enumerate="enumerate({})".format,
			enumfl="ul4c._enumfl({})".format,
			isfirstlast="ul4c._isfirstlast({})".format,
			isfirst="ul4c._isfirst({})".format,
			islast="ul4c._islast({})".format,
			isnone="{} is None".format,
			isstr="isinstance({}, str)".format,
			isint="ul4c._isint({})".format,
			isfloat="isinstance({}, float)".format,
			isbool="isinstance({}, bool)".format,
			isdate="isinstance({}, (datetime.datetime, datetime.date))".format,
			islist="ul4c._islist({})".format,
			isdict="isinstance({}, collections.Mapping)".format,
			istemplate="isinstance({}, ul4c.Template)".format,
			iscolor="isinstance({}, color.Color)".format,
			repr="ul4c._repr({})".format,
			get="vars.get({})".format,
			chr="chr({})".format,
			ord="ord({})".format,
			hex="hex({})".format,
			oct="oct({})".format,
			bin="bin({})".format,
			sorted="sorted({})".format,
			range="range({})".format,
			type="ul4c._type({})".format,
			reversed="reversed({})".format,
			randrange="random.randrange({})".format,
			randchoice="random.randchoice({})".format,
			format="format({})".format,
			zip="zip({})".format,
			rgb="color.Color.fromrgb({})".format,
			hls="color.Color.fromhls({})".format,
			hsv="color.Color.fromhsv({})".format,
		)
		try:
			formatter = functions[self.funcname]
		except KeyError:
			raise UnknownFunctionError(self.funcname)
		return formatter(", ".join(arg.formatpython(indent) for arg in self.args))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.funcname)
		encoder.dump(self.args)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.funcname = decoder.load()
		self.args = decoder.load()


@ul4on.register("de.livinglogic.ul4.callmeth")
class CallMeth(AST):
	def __init__(self, location=None, methname=None, obj=None, *args):
		super().__init__(location)
		self.methname = methname
		self.obj = obj
		self.args = list(args)

	def __repr__(self):
		if self.args:
			return "{}({!r}, {!r}, {})".format(self.__class__.__name__, self.methname, self.obj, repr(self.args)[1:-1])
		else:
			return "{}({!r}, {!r})".format(self.__class__.__name__, self.methname, self.obj)

	def formatpython(self, indent):
		methods = dict(
			split="({}).split({})".format,
			rsplit="({}).rsplit({})".format,
			strip="({}).strip({})".format,
			rstrip="({}).rstrip({})".format,
			find="({}).find({})".format,
			rfind="({}).rfind({})".format,
			startswith="({}).startswith({})".format,
			endswith="({}).endswith({})".format,
			upper="({}).upper({})".format,
			lower="({}).lower({})".format,
			capitalize="({}).capitalize({})".format,
			replace="({}).replace({})".format,
			r="({}).r({})".format,
			g="({}).g({})".format,
			b="({}).b({})".format,
			a="({}).a({})".format,
			hls="({}).hls({})".format,
			hlsa="({}).hlsa({})".format,
			hsv="({}).hsv({})".format,
			hsva="({}).hsva({})".format,
			lum="({}).lum({})".format,
			weekday="({}).weekday({})".format,
			items="({}).items({})".format,
			join="({}).join(ul4c._str(item) for item in {})".format,
			renders="({}).renders({})".format,
			mimeformat="ul4c._mimeformat({}, {})".format,
			isoformat="ul4c._isoformat({}, {})".format,
			yearday="ul4c._yearday({}, {})".format,
			get="({}).get({})".format,
			withlum="({}).withlum({})".format,
			witha="({}).witha({})".format,
			day="({}).day".format,
			month="({}).month".format,
			year="({}).year".format,
			hour="({}).hour".format,
			minute="({}).minute".format,
			second="({}).second".format,
			microsecond="({}).microsecond".format,
		)
		try:
			formatter = methods[self.methname]
		except KeyError:
			raise UnknownMethodError(self.methname)
		return formatter(self.obj.formatpython(indent), ", ".join(arg.formatpython(indent) for arg in self.args))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.methname)
		encoder.dump(self.obj)
		encoder.dump(self.args)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.methname = decoder.load()
		self.obj = decoder.load()
		self.args = decoder.load()


@ul4on.register("de.livinglogic.ul4.callmethkw")
class CallMethKeywords(AST):
	def __init__(self, location=None, methname=None, obj=None, *args):
		super().__init__(location)
		self.methname = methname
		self.obj = obj
		self.args = list(args)

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.methname, self.obj, self.args)

	def formatpython(self, indent):
		if self.methname == "renders":
			args = []
			for arg in self.args:
				if len(arg) == 1:
					args.append("({},)".format(arg[0].formatpython(indent)))
				else:
					args.append("({!r}, {})".format(arg[0], arg[1].formatpython(indent)))
			args = "ul4c._makedict({})".format(", ".join(args))
			return "({}).renders(**{})".format(self.obj.formatpython(indent), args)
		else:
			# The ``render`` method can only be used in the ``render`` tag, where it is handled separately
			raise UnknownMethodError(self.methname)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.methname)
		encoder.dump(self.obj)
		encoder.dump(self.args)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.methname = decoder.load()
		self.obj = decoder.load()
		self.args = map(tuple, decoder.load())


@ul4on.register("de.livinglogic.ul4.render")
class Render(Unary):
	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.obj)

	def formatpython(self, indent):
		if isinstance(self.obj, (CallMeth, CallMethKeywords)) and self.obj.methname == "render":
			v = []
			if self.obj.args:
				args = []
				for arg in self.obj.args:
					if len(arg) == 1:
						args.append(arg[0].formatpython(indent))
					else:
						args.append("({!r}, {})".format(arg[0], arg[1].formatpython(indent)))
				args = "**ul4c._makedict({})".format(", ".join(args))
			else:
				args = ""
			v.append("{}for part in ({})({}):\n".format(indent*"\t", self.obj.obj.formatpython(indent), args))
			v.append("{}\tyield part\n".format(indent*"\t"))
			return "".join(v)
		else:
			return "{}yield ul4c._str({})\n".format(indent*"\t", self.obj.formatpython(indent))


@ul4on.register("de.livinglogic.ul4.template")
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
	"""
	version = "17"

	def __init__(self, source=None, name=None, startdelim="<?", enddelim="?>"):
		"""
		Create a :class:`Template` object. If :var:`source` is ``None``, the
		:class:`Template` remains uninitialized, otherwise :var:`source` will be
		compiled (using :var:`startdelim` and :var:`enddelim` as the tag
		delimiters). :var:`name` is the name of the template. It will be used in
		exception messages and should be a valid Python identifier.

		"""
		super().__init__(None)
		self.startdelim = startdelim
		self.enddelim = enddelim
		self.name = name
		self.source = None
		# The following is used for converting the AST back to executable Python code
		self._pythonfunction = None
		if source is not None:
			self._compile(source, name, startdelim, enddelim)

	def ul4ondump(self, encoder):
		encoder.dump(self.version)
		encoder.dump(self.source)
		encoder.dump(self.name)
		encoder.dump(self.startdelim)
		encoder.dump(self.enddelim)
		super().ul4ondump(encoder)

	def ul4onload(self, decoder):
		version = decoder.load()
		if version != self.version:
			raise ValueError("invalid version, expected {!r}, got {!r}".format(self.version, version))
		self.source = decoder.load()
		self.name = decoder.load()
		self.startdelim = decoder.load()
		self.enddelim = decoder.load()
		super().ul4onload(decoder)

	def __getitem__(self, key):
		if key in {"source", "name", "content", "startdelim", "enddelim"}:
			return getattr(self, key)
		raise KeyError(key)

	@classmethod
	def loads(cls, data):
		"""
		The class method :meth:`loads` loads the template from string :var:`data`.
		:var:`data` must contain the template in compiled format.
		"""

		return ul4on.loads(data)

	@classmethod
	def load(cls, stream):
		"""
		The class method :meth:`load` loads the template from the stream
		:var:`stream`. The stream must contain the template in compiled format.
		"""
		return ul4on.load(stream)

	def dump(self, stream):
		"""
		:meth:`dump` dumps the template in compiled format to the stream
		:var:`stream`.
		"""
		ul4on.dump(self, stream)

	def dumps(self):
		"""
		:meth:`dumps` returns the template in compiled format (as a string).
		"""
		return ul4on.dumps(self)

	def formatpython(self, indent):
		v = []
		v.append("{}def template(**vars):\n".format(indent*"\t"))
		indent += 1
		v.append("{}import datetime, random\n".format(indent*"\t"))
		v.append("{}from ll import ul4c, misc, color\n".format(indent*"\t"))
		v.append("{}if 0:\n".format(indent*"\t"))
		v.append("{}\tyield\n".format(indent*"\t"))
		for node in self.content:
			v.append(node.formatpython(indent))
		indent -= 1
		name = self.name if self.name is not None else "unnamed"
		v.append("{}template.__name__ = {!r}\n".format(indent*"\t", name))
		v.append("{}vars[{!r}] = template\n".format(indent*"\t", name))
		return "".join(v)

	def render(self, **vars):
		"""
		Render the template iteratively (i.e. this is a generator).
		:var:`vars` contains the top level variables available to the
		template code.
		"""
		return self.pythonfunction()(**vars)

	def renders(self, **vars):
		"""
		Render the template as a string. :var:`vars` contains the top level
		variables available to the template code.
		"""
		return "".join(self.pythonfunction()(**vars))

	def pythonfunction(self):
		"""
		Return a Python generator that can be called to render the template. The
		argument signature of the function will be ``**vars``.
		"""
		if self._pythonfunction is None:
			code = self.pythonsource()
			ns = {}
			exec(code, ns)
			self._pythonfunction = ns[self.name if self.name is not None else "unnamed"]
			self._pythonfunction.source = self.source
		return self._pythonfunction

	def __call__(self, **vars):
		return self.pythonfunction()(**vars)

	def pythonsource(self, *args, **kwargs):
		"""
		Return the template as Python source code. All arguments in :var:`args`
		and :var:`kwargs` will be passed on to the :class:`PythonSource` object
		which creates the sourcecode. See its constructor for more info.
		"""
		v = []
		v.append("def {}(**vars):\n".format(self.name if self.name is not None else "unnamed"))
		v.append("\timport datetime, random\n")
		v.append("\tfrom ll import ul4c, misc, color\n")
		v.append("\tif 0:\n")
		v.append("\t\tyield\n")
		for node in self.content:
			v.append(node.formatpython(1))
		return "".join(v)

	def jssource(self):
		"""
		Return the template as the source code of a Javascript function. A
		:class:`JavascriptSource` object will be used to generated the sourcecode.
		"""
		return str(JavascriptSource(self))

	def javasource(self, *args, **kwargs):
		"""
		Return the template as Java source code. All arguments in :var:`args`
		and :var:`kwargs` will be passed on to the :class:`JavaSource` object
		which creates the sourcecode. See its constructor for more info.
		"""
		return str(JavaSource(self, *args, **kwargs))

	def format(self, indent="\t"):
		"""
		Format the list of opcodes. This is a generator yielding lines to be output
		(but without trailing newlines). :var:`indent` can be used to specify how
		to indent blocks (defaulting to ``"\\t"``).
		"""
		name = self.name if self.name is not None else "unnamed"
		yield "def {}(**vars) {{".format(name)
		i = 1
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
		yield "}"

	def _tokenize(self, source, startdelim, enddelim):
		"""
		Tokenize the template source code :var:`source` into tags and non-tag
		text. :var:`startdelim` and :var:`enddelim` are used as the tag delimiters.

		This is a generator which produces :class:`Location` objects for each tag
		or non-tag text. It will be called by :meth:`_compile` internally.
		"""
		pattern = "{}(printx|print|code|for|if|elif|else|end|break|continue|render|def|note)(\s*((.|\\n)*?)\s*)?{}".format(re.escape(startdelim), re.escape(enddelim))
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

	def opcode(self, code, r1=None, r2=None, r3=None, r4=None, r5=None, arg=None):
		"""
		Creates an :class:`Opcode` object and appends it to :var:`self`\s list of
		opcodes.
		"""
		self.opcodes.append(Opcode(code, r1, r2, r3, r4, r5, arg, self.location))

	def _compile(self, source, name, startdelim, enddelim):
		"""
		Compile the template source code :var:`source` into opcodes.
		:var:`startdelim` and :var:`enddelim` are used as the tag delimiters.
		"""
		self.name = name
		self.startdelim = startdelim
		self.enddelim = enddelim
		scanner = Scanner()
		parseexpr = ExprParser(scanner).compile
		parsestmt = StmtParser(scanner).compile
		parsefor = ForParser(scanner).compile

		# This stack stores for each nested for/if/elif/else/def the following information:
		# 1) Which construct we're in (i.e. "if" or "for")
		# 2) The start location of the construct
		# For ifs:
		# 3) How many if's or elif's we have seen (this is used for simulating elif's via nested if's, for each additional elif, we have one more endif to add)
		# 4) Whether we've already seen the else
		stack = [self]

		self.source = source

		if source is None:
			return

		for location in self._tokenize(source, startdelim, enddelim):
			try:
				if location.type is None:
					stack[-1].append(Text(location))
				elif location.type == "print":
					stack[-1].append(Print(location, parseexpr(location)))
				elif location.type == "printx":
					stack[-1].append(PrintX(location, parseexpr(location)))
				elif location.type == "code":
					stack[-1].append(parsestmt(location))
				elif location.type == "if":
					block = IfElIfElse(location, parseexpr(location))
					stack[-1].append(block)
					stack.append(block)
				elif location.type == "elif":
					if not isinstance(stack[-1], IfElIfElse):
						raise BlockError("elif doesn't match and if")
					elif isinstance(stack[-1].content[-1], Else):
						raise BlockError("else already seen in if")
					stack[-1].newblock(ElIf(location, parseexpr(location)))
				elif location.type == "else":
					if not isinstance(stack[-1], IfElIfElse):
						raise BlockError("else doesn't match and if")
					elif isinstance(stack[-1].content[-1], Else):
						raise BlockError("else already seen in if")
					stack[-1].newblock(Else(location))
				elif location.type == "end":
					if len(stack) <= 1:
						raise BlockError("not in any block")
					code = location.code
					if code:
						if code == "if":
							if not isinstance(stack[-1], IfElIfElse):
								raise BlockError("endif doesn't match any if")
						elif code == "for":
							if not isinstance(stack[-1], (For, ForUnpack)):
								raise BlockError("endfor doesn't match any for")
						elif code == "def":
							if not isinstance(stack[-1], Template):
								raise BlockError("enddef doesn't match any def")
						else:
							raise BlockError("illegal end value {!r}".format(code))
					stack.pop()
				elif location.type == "for":
					block = parsefor(location)
					stack[-1].append(block)
					stack.append(block)
				elif location.type == "break":
					for block in reversed(stack):
						if isinstance(block, (For, ForUnpack)):
							break
						elif isinstance(block, Template):
							raise BlockError("break outside of for loop")
					stack[-1].append(Break(location))
				elif location.type == "continue":
					for block in reversed(stack):
						if isinstance(block, (For, ForUnpack)):
							break
						elif isinstance(block, Template):
							raise BlockError("continue outside of for loop")
					stack[-1].append(Continue(location))
				elif location.type == "render":
					stack[-1].append(Render(location, parseexpr(location)))
				elif location.type == "def":
					block = Template(None, location.code, self.startdelim, self.enddelim)
					block.location = location
					stack[-1].append(block)
					stack.append(block)
				else: # Can't happen
					raise ValueError("unknown tag {!r}".format(location.type))
			except Exception as exc:
				raise Error(location) from exc
		if len(stack) > 1:
			raise Error(stack[-1].location) from BlockError("block unclosed")

	def __str__(self):
		return "\n".join(self.format())

	def __repr__(self):
		return "<{}.{} object with {} opcodes at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, len(self.opcodes), id(self))


###
### Code generators for various languages
###

class PythonSource(object):
	"""
	A :class:`PythonSource` object generates Python sourcecode from a UL4
	template.
	"""

	def __init__(self, template):
		"""
		Create a :class:`PythonSource` object. :var:`template` is the
		:class:`Template` object.
		"""
		self.template = template

	def __str__(self):
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

		self._line(self.lastlocation, "def {}(**variables):".format(self.template.name))
		self.indent += 1
		self.lines2locs = [] # We initialize startline one line below, which restarts the counter
		self._line(self.lastlocation, "import sys, datetime, itertools, json, random, collections; from ll.misc import xmlescape; from ll import ul4c, color; startline = sys._getframe().f_lineno") # The line number of this line
		self._line(self.lastlocation, "__1__")
		self._line(self.lastlocation, "__2__")
		self._line(self.lastlocation, "source = {!r}".format(self.template.source))
		self._line(self.lastlocation, "name = {!r}".format(self.template.name))
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
		except Exception as exc:
			raise Error(opcode.location) from exc
		self.indent -= 1
		self._line(self.lastlocation, "except Exception as exc:")
		self.indent += 1
		self._line(self.lastlocation, "raise ul4c.Error(ul4c.Location(source, name, *locations[lines2locs[sys.exc_info()[2].tb_lineno-startline]])) from exc")
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
	def _dispatch_getslice(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}[:]".format(op=opcode))
	def _dispatch_print(self, opcode):
		self._line(opcode.location, "if r{op.r1:d} is not None: yield str(r{op.r1:d})".format(op=opcode))
	def _dispatch_printx(self, opcode):
		self._line(opcode.location, "if r{op.r1:d} is not None: yield xmlescape(str(r{op.r1:d}))".format(op=opcode))
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
			self._line(opcode.location, "r{op.r1:d} = list(r{op.r2:d}.items())".format(op=opcode))
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
			self._line(opcode.location, "r{op.r1:d} = r{op.r2:d}.join(str(x) for x in r{op.r3:d})".format(op=opcode))
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
			self._line(opcode.location, 'r{op.r1:d} = "".join(r{op.r2:d}(**r{op.r3:d}))'.format(op=opcode))
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
			self.lines[-1] += " pass"
		self.indent -= 1
	def _dispatch_def(self, opcode):
		self._line(opcode.location, "def _template_{}(**variables):".format(opcode.arg))
		self.defs.append(opcode)
		self.indent += 1
		self._line(opcode.location, "name = {!r}".format(opcode.arg))
		self._line(opcode.location, "r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = r8 = r9 = None")
		self._line(opcode.location, "try:")
		self.indent += 1
		# Make sure that the resulting code is a generator even if the byte codes produce no yield statement
		self._line(opcode.location, "if 0: yield ''")
	def _dispatch_enddef(self, opcode):
		defopcode = self.defs.pop()
		self.indent -= 1
		self._line(opcode.location, "except Exception as exc:")
		self.indent += 1
		self._line(opcode.location, "raise ul4c.Error(ul4c.Location(source, name, *locations[lines2locs[sys.exc_info()[2].tb_lineno-startline]])) from exc")
		self.indent -= 2
		self._line(opcode.location, "variables[{op.arg!r}] = _template_{op.arg}".format(op=defopcode))
	def _dispatch_render(self, opcode):
		self._line(opcode.location, 'for chunk in r{op.r1:d}(**r{op.r2:d}): yield chunk'.format(op=opcode))
	def _dispatch_callfunc0_now(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = datetime.datetime.now()".format(op=opcode))
	def _dispatch_callfunc0_utcnow(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = datetime.datetime.utcnow()".format(op=opcode))
	def _dispatch_callfunc0_vars(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = variables".format(op=opcode))
	def _dispatch_callfunc0_random(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = random.random()".format(op=opcode))
	def _dispatch_callfunc1_xmlescape(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = xmlescape(str(r{op.r2:d})) if r{op.r2:d} is not None else ''".format(op=opcode))
	def _dispatch_callfunc1_csv(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._csv(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_json(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._json(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_str(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = str(r{op.r2:d}) if r{op.r2:d} is not None else ''".format(op=opcode))
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
	def _dispatch_callfunc1_enumfl(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._enumfl(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_isfirstlast(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._isfirstlast(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_isfirst(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._isfirst(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_islast(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._islast(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_isnone(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = r{op.r2:d} is None".format(op=opcode))
	def _dispatch_callfunc1_isstr(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, str)".format(op=opcode))
	def _dispatch_callfunc1_isint(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, int) and not isinstance(r{op.r2:d}, bool)".format(op=opcode))
	def _dispatch_callfunc1_isfloat(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, float)".format(op=opcode))
	def _dispatch_callfunc1_isbool(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, bool)".format(op=opcode))
	def _dispatch_callfunc1_isdate(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, datetime.datetime)".format(op=opcode))
	def _dispatch_callfunc1_islist(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, collections.Sequence) and not isinstance(r{op.r2:d}, (str, color.Color))".format(op=opcode))
	def _dispatch_callfunc1_isdict(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, collections.Mapping)".format(op=opcode))
	def _dispatch_callfunc1_istemplate(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, ul4c.Template)".format(op=opcode))
	def _dispatch_callfunc1_iscolor(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = isinstance(r{op.r2:d}, color.Color)".format(op=opcode))
	def _dispatch_callfunc1_repr(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ul4c._repr(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_get(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = variables.get(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_chr(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = chr(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_ord(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = ord(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_hex(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = hex(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_oct(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = oct(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_bin(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = bin(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_sorted(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = sorted(r{op.r2:d})".format(op=opcode))
	def _dispatch_callfunc1_range(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = range(r{op.r2:d})".format(op=opcode))
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
		self._line(opcode.location, "r{op.r1:d} = range(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc2_get(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = variables.get(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc2_zip(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = zip(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc2_int(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = int(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc2_randrange(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = random.randrange(r{op.r2:d}, r{op.r3:d})".format(op=opcode))
	def _dispatch_callfunc3_range(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = range(r{op.r2:d}, r{op.r3:d}, r{op.r4:d})".format(op=opcode))
	def _dispatch_callfunc3_zip(self, opcode):
		self._line(opcode.location, "r{op.r1:d} = zip(r{op.r2:d}, r{op.r3:d}, r{op.r4:d})".format(op=opcode))
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

	Note that the generated code will require the ``ul4`` Javascript support
	library.
	"""
	def __init__(self, template):
		"""
		Create a :class:`JavascriptSource` object. :var:`template` is the
		:class:`Template` object.
		"""
		self.template = template

	def __str__(self):
		"""
		Return the Javascript sourcecode for the :class:`Template` object passed
		to the constructor.
		"""
		return "ul4.Template.loads({})".format(_json(self.template.dumps()))


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

	def __str__(self):
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
				self._do("/* <?{}?> tag at position {} (line {}, col {}, template {}): {} */".format(lastloc.type, lastloc.starttag+1, line, col, lastloc.name, repr(tag)[1:-1]))
			try:
				getattr(self, "_dispatch_{}".format(opcode.code))(opcode)
			except AttributeError:
				raise UnknownOpcodeError(opcode.code)

		# Add source and register declaration at the beginning
		lines.append("/*@@@ BEGIN template source */")
		sourcelines = self.template.source.splitlines(False)
		width = len(str(len(sourcelines)))
		for (i, line) in enumerate(sourcelines):
			lines.append("/* {1:{0}} {2} */".format(width, i+1, line.replace("/*", "*").replace("*/", "*")))
		lines.append("/*@@@ BEGIN template code */")
		
		for i in sorted(self._stack[-1].regsused):
			lines.append("Object r{} = null;".format(i))

		# copy over generated source code
		lines.extend(self._stack[-1].lines)

		lines.append("/*@@@ END template code */")

		v = []
		indent = self.indent
		for line in lines:
			if isinstance(line, int):
				indent += line
			else:
				v.append("\t"*indent + line)
		return "\n".join(v)

	def output(self, expression):
		"""
		Return a statement for outputting the Java expression :var:`expression`.
		This uses ``out.write()`` (for JSP etc.) but can be overwritten in
		subclasses.
		"""
		return "out.write({});".format(expression)

	def _usereg(self, r):
		self._stack[-1].regsused.add(r)

	def _do(self, line):
		# :var:`line` is either an ``int`` (which is added to the current indentation) or a line of source code.
		self._stack[-1].lines.append(line)

	def _dispatch_None(self, opcode):
		(line, col) = opcode.location.pos()
		self._do("/* Literal at {} (line {}, col {}) */".format(opcode.location.starttag+1, line, col))
		self._do(self.output(misc.javaexpr(opcode.location.code)))
	def _dispatch_loadstr(self, opcode):
		self._do("r{op.r1} = {arg};".format(op=opcode, arg=misc.javaexpr(opcode.arg)))
		self._usereg(opcode.r1)
	def _dispatch_loadint(self, opcode):
		self._do("r{op.r1} = new Integer({op.arg});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loadfloat(self, opcode):
		self._do("r{op.r1} = new Double({op.arg});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loadnone(self, opcode):
		self._do("r{op.r1} = null;".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loadfalse(self, opcode):
		self._do("r{op.r1} = false;".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loadtrue(self, opcode):
		self._do("r{op.r1} = true;".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loaddate(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.makeDate({date});".format(op=opcode, date=", ".join(str(int(p)) for p in datesplitter.split(opcode.arg))))
		self._usereg(opcode.r1)
	def _dispatch_loadcolor(self, opcode):
		self._do("r{op.r1} = new de.livinglogic.ul4.Color(0x{r}, 0x{g}, 0x{b}, 0x{a});".format(op=opcode, r=opcode.arg[:2], g=opcode.arg[2:4], b=opcode.arg[4:6], a=opcode.arg[6:]))
		self._usereg(opcode.r1)
	def _dispatch_buildlist(self, opcode):
		self._do("r{op.r1} = new java.util.ArrayList();".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_builddict(self, opcode):
		self._do("r{op.r1} = new java.util.HashMap();".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_addlist(self, opcode):
		self._do("((java.util.List)r{op.r1}).add(r{op.r2});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_adddict(self, opcode):
		self._do("((java.util.Map)r{op.r1}).put(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_updatedict(self, opcode):
		self._do("((java.util.Map)r{op.r1}).putAll((java.util.Map)r{op.r2});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_loadvar(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.getItem({var}, {arg});".format(op=opcode, var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg)))
		self._usereg(opcode.r1)
	def _dispatch_storevar(self, opcode):
		self._do("{var}.put({arg}, r{op.r1});".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_addvar(self, opcode):
		self._do("{var}.put({arg}, de.livinglogic.ul4.Utils.add({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_subvar(self, opcode):
		self._do("{var}.put({arg}, de.livinglogic.ul4.Utils.sub({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_mulvar(self, opcode):
		self._do("{var}.put({arg}, de.livinglogic.ul4.Utils.mul({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_truedivvar(self, opcode):
		self._do("{var}.put({arg}, de.livinglogic.ul4.Utils.truediv({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_floordivvar(self, opcode):
		self._do("{var}.put({arg}, de.livinglogic.ul4.Utils.floordiv({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_modvar(self, opcode):
		self._do("{var}.put({arg}, de.livinglogic.ul4.Utils.mod({var}.get({arg}), r{op.r1}));".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg), op=opcode))
	def _dispatch_delvar(self, opcode):
		self._do("{var}.remove({arg});".format(var=self._stack[-1].variables, arg=misc.javaexpr(opcode.arg)))
	def _dispatch_getattr(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.getItem(r{op.r2}, {arg});".format(op=opcode, arg=misc.javaexpr(opcode.arg)))
		self._usereg(opcode.r1)
	def _dispatch_getitem(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.getItem(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_getslice12(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.getSlice(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_getslice1(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.getSlice(r{op.r2}, r{op.r3}, null);".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_getslice2(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.getSlice(r{op.r2}, null, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_getslice(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.getSlice(r{op.r2}, null, null);".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_print(self, opcode):
		self._do(self.output("de.livinglogic.ul4.Utils.str(r{op.r1})".format(op=opcode)))
	def _dispatch_printx(self, opcode):
		self._do(self.output("de.livinglogic.ul4.Utils.xmlescape(r{op.r1})".format(op=opcode)))
	def _dispatch_for(self, opcode):
		varcounter = self._stack[-1].varcounter
		self._do("for (java.util.Iterator iterator{count} = de.livinglogic.ul4.Utils.iterator(r{op.r2}); iterator{count}.hasNext();)".format(op=opcode, count=varcounter))
		self._do("{")
		self._do(1)
		self._do("r{op.r1} = iterator{count}.next();".format(op=opcode, count=varcounter))
		self._usereg(opcode.r1)
		self._stack[-1].varcounter += 1
	def _dispatch_endfor(self, opcode):
		self._do(-1)
		self._do("}")
	def _dispatch_def(self, opcode):
		self._stack.append(_JavaTemplateLevel("variables", opcode.arg))
	def _dispatch_enddef(self, opcode):
		level = self._stack.pop()
		# define new template object
		self._do('{var}.put({arg}, new de.livinglogic.ul4.JSPTemplate()'.format(var=self._stack[-1].variables, arg=misc.javaexpr(level.name)))
		self._do("{")
		self._do(1)
		self._do("public String getName()")
		self._do("{")
		self._do(1)
		self._do('return {};'.format(misc.javaexpr(level.name)))
		self._do(-1)
		self._do("}")
		self._do("public void render(java.io.Writer out, java.util.Map<String, Object> variables) throws java.io.IOException")
		self._do("{")
		self._do(1)
		# registers
		for i in sorted(level.regsused):
			self._do("Object r{} = null;".format(i))
		# copy over source from the nested template
		self._stack[-1].lines.extend(level.lines)
		# end object and put it into variables
		self._do(-1)
		self._do("}")
		self._do(-1)
		self._do("});")
	def _dispatch_break(self, opcode):
		self._do("break;")
	def _dispatch_continue(self, opcode):
		self._do("continue;")
	def _dispatch_not(self, opcode):
		self._do("r{op.r1} = !de.livinglogic.ul4.Utils.getBool(r{op.r2});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_neg(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.neg(r{op.r2});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_contains(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.contains(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_notcontains(self, opcode):
		self._do("r{op.r1} = !de.livinglogic.ul4.Utils.contains(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_eq(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.eq(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_ne(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.ne(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_lt(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.lt(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_le(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.le(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_gt(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.gt(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_ge(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.ge(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_add(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.add(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_sub(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.sub(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_mul(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.mul(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_floordiv(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.floordiv(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_truediv(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.truediv(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_and(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.getBool(r{op.r3}) ? r{op.r2} : r{op.r3};".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_or(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.getBool(r{op.r2}) ? r{op.r2} : r{op.r3};".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_mod(self, opcode):
		self._do("r{op.r1} = de.livinglogic.ul4.Utils.mod(r{op.r2}, r{op.r3});".format(op=opcode))
		self._usereg(opcode.r1)
	def _dispatch_callfunc0(self, opcode):
		if opcode.arg == "now":
			self._do("r{op.r1} = new java.util.Date();".format(op=opcode))
		elif opcode.arg in {"utcnow", "random"}:
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.{op.arg}();".format(op=opcode))
		elif opcode.arg == "vars":
			self._do("r{op.r1} = {var};".format(op=opcode, var=self._stack[-1].variables))
		else:
			raise UnknownFunctionError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callfunc1(self, opcode):
		if opcode.arg in {"xmlescape", "csv", "repr", "enumerate", "isfirstlast", "isfirst", "islast", "enumfl", "chr", "ord", "hex", "oct", "bin", "sorted", "range", "type", "json", "reversed", "randrange", "randchoice", "abs", "str"}:
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.{op.arg}(r{op.r2});".format(op=opcode))
		elif opcode.arg == "int":
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.toInteger(r{op.r2});".format(op=opcode))
		elif opcode.arg == "float":
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.toFloat(r{op.r2});".format(op=opcode))
		elif opcode.arg == "bool":
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.getBool(r{op.r2});".format(op=opcode))
		elif opcode.arg == "len":
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.length(r{op.r2});".format(op=opcode))
		elif opcode.arg == "isnone":
			self._do("r{op.r1} = (r{op.r2} == null);".format(op=opcode))
		elif opcode.arg == "isstr":
			self._do("r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof String));".format(op=opcode))
		elif opcode.arg == "isint":
			self._do("r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof Integer));".format(op=opcode))
		elif opcode.arg == "isfloat":
			self._do("r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof Double));".format(op=opcode))
		elif opcode.arg == "isbool":
			self._do("r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof Boolean));".format(op=opcode))
		elif opcode.arg == "isdate":
			self._do("r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof java.util.Date));".format(op=opcode))
		elif opcode.arg == "islist":
			self._do("r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof java.util.List));".format(op=opcode))
		elif opcode.arg == "isdict":
			self._do("r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof java.util.Map) && !(r{op.r2} instanceof de.livinglogic.ul4.Template));".format(op=opcode))
		elif opcode.arg == "istemplate":
			self._do("r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof de.livinglogic.ul4.Template));".format(op=opcode))
		elif opcode.arg == "iscolor":
			self._do("r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof de.livinglogic.ul4.Color));".format(op=opcode))
		elif opcode.arg == "get":
			self._do("r{op.r1} = {var}.get(r{op.r2});".format(op=opcode, var=self._stack[-1].variables))
		else:
			raise UnknownFunctionError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callfunc2(self, opcode):
		if opcode.arg in {"format", "range", "zip", "randrange"}:
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.arg == "int":
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.toInteger(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.arg == "get":
			self._do("r{op.r1} = {var}.containsKey(r{op.r2}) ? {var}.get(r{op.r2}) : r{op.r3};".format(op=opcode, var=self._stack[-1].variables))
		else:
			raise UnknownFunctionError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callfunc3(self, opcode):
		if opcode.arg in {"range", "zip", "rgb", "hls", "hsv", "randrange"}:
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
		else:
			raise UnknownFunctionError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callfunc4(self, opcode):
		if opcode.arg in {"rgb", "hls", "hsv"}:
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4}, r{op.r5});".format(op=opcode))
		else:
			raise UnknownFunctionError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callmeth0(self, opcode):
		if opcode.arg in {"split", "rsplit", "strip", "lstrip", "rstrip", "upper", "lower", "capitalize", "items", "isoformat", "mimeformat", "day", "month", "year", "hour", "minute", "second", "microsecond", "weekday", "yearday"}:
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.{op.arg}(r{op.r2});".format(op=opcode))
		elif opcode.arg in {"r", "g", "b", "a"}:
			self._do("r{op.r1} = ((de.livinglogic.ul4.Color)r{op.r2}).get{arg}();".format(op=opcode, arg=opcode.arg.upper()))
		elif opcode.arg in {"hls", "hlsa", "hsv", "hsva"}:
			self._do("r{op.r1} = ((de.livinglogic.ul4.Color)r{op.r2}).{op.arg}();".format(op=opcode))
		elif opcode.arg == "lum":
			self._do("r{op.r1} = ((de.livinglogic.ul4.Color)r{op.r2}).lum();".format(op=opcode))
		elif opcode.arg == "render":
			self._do("r{op.r1} = ((de.livinglogic.ul4.Template)r{op.r2}).renders(null);".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callmeth1(self, opcode):
		if opcode.arg in {"join", "split", "rsplit", "strip", "lstrip", "rstrip", "startswith", "endswith", "find", "rfind", "withlum", "witha"}:
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.arg == "get":
			self._do("r{op.r1} = ((java.util.Map)r{op.r2}).get(r{op.r3});".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callmeth2(self, opcode):
		if opcode.arg in {"split", "rsplit", "find", "rfind", "replace"}:
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
		elif opcode.arg == "get":
			self._do("r{op.r1} = ((java.util.Map)r{op.r2}).containsKey(r{op.r3}) ? ((java.util.Map)r{op.r2}).get(r{op.r3}) : r{op.r4};".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callmeth3(self, opcode):
		if opcode.arg in {"find", "rfind"}:
			self._do("r{op.r1} = de.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4}, r{op.r5});".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_callmethkw(self, opcode):
		if opcode.arg == "render":
			self._do("r{op.r1} = ((de.livinglogic.ul4.Template)r{op.r2}).renders((java.util.Map)r{op.r3});".format(op=opcode))
		else:
			raise UnknownMethodError(opcode.arg)
		self._usereg(opcode.r1)
	def _dispatch_if(self, opcode):
		self._do("if (de.livinglogic.ul4.Utils.getBool(r{op.r1}))".format(op=opcode))
		self._do("{")
		self._do(1)
	def _dispatch_else(self, opcode):
		self._do(-1)
		self._do("}")
		self._do("else")
		self._do("{")
		self._do(1)
	def _dispatch_endif(self, opcode):
		self._do(-1)
		self._do("}")
	def _dispatch_render(self, opcode):
		self._do("((de.livinglogic.ul4.Template)r{op.r1}).render(out, (java.util.Map)r{op.r2});".format(op=opcode))


###
### Tokenizer
###

class Scanner(spark.Scanner):
	reflags = re.UNICODE

	def tokenize(self, location):
		self.location = location
		self.collectstr = []
		self.rv = []
		self.start = 0
		try:
			spark.Scanner.tokenize(self, location.code)
			if self.mode != "default":
				raise UnterminatedStringError()
		except Exception as exc:
			raise Error(location) from exc
		return self.rv

	# Color tokens must be in the order of decreasing length
	@spark.token("\\#[0-9a-fA-F]{8}", "default")
	def color8(self, start, end, s):
		self.rv.append(Color(self.location, color.Color(int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), int(s[7:], 16))))

	@spark.token("\\#[0-9a-fA-F]{6}", "default")
	def color6(self, start, end, s):
		self.rv.append(Color(self.location, color.Color(int(s[1:3], 16), int(s[3:5], 16), int(s[5:], 16))))

	@spark.token("\\#[0-9a-fA-F]{4}", "default")
	def color4(self, start, end, s):
		self.rv.append(Color(self.location, color.Color(17*int(s[1], 16), 17*int(s[2], 16), 17*int(s[3], 16), 17*int(s[4], 16))))

	@spark.token("\\#[0-9a-fA-F]{3}", "default")
	def color3(self, start, end, s):
		self.rv.append(Color(self.location, color.Color(17*int(s[1], 16), 17*int(s[2], 16), 17*int(s[3], 16))))

	@spark.token("@\\(\\d{4}-\\d{2}-\\d{2}(T(\\d{2}:\\d{2}(:\\d{2}(\\.\\d{6})?)?)?)?\\)", "default")
	def date(self, start, end, s):
		self.rv.append(Date(self.location, datetime.datetime(*map(int, [_f for _f in datesplitter.split(s[2:-1]) if _f]))))

	@spark.token("\\(|\\)|\\[|\\]|\\{|\\}|\\.|,|==|\\!=|<=|<|>=|>|=|\\+=|\\-=|\\*=|//=|/=|%=|%|:|\\+|-|\\*\\*|\\*|//|/", "default")
	def token(self, start, end, s):
		self.rv.append(Token(self.location, s))

	@spark.token("[a-zA-Z_][\\w]*", "default")
	def name(self, start, end, s):
		if s in ("in", "not", "or", "and", "del"):
			self.rv.append(Token(self.location, s))
		elif s == "None":
			self.rv.append(None_(self.location))
		elif s == "True":
			self.rv.append(True_(self.location))
		elif s == "False":
			self.rv.append(False_(self.location))
		else:
			self.rv.append(Name(self.location, s))

	# We don't have negatve numbers, this is handled by constant folding in the AST for unary minus
	@spark.token("\\d+\\.\\d*([eE][+-]?\\d+)?", "default")
	@spark.token("\\d+(\\.\\d*)?[eE][+-]?\\d+", "default")
	def float(self, start, end, s):
		self.rv.append(Float(self.location, float(s)))

	@spark.token("0[xX][\\da-fA-F]+", "default")
	def hexint(self, start, end, s):
		self.rv.append(Int(self.location, int(s[2:], 16)))

	@spark.token("0[oO][0-7]+", "default")
	def octint(self, start, end, s):
		self.rv.append(Int(self.location, int(s[2:], 8)))

	@spark.token("0[bB][01]+", "default")
	def binint(self, start, end, s):
		self.rv.append(Int(self.location, int(s[2:], 2)))

	@spark.token("\\d+", "default")
	def int(self, start, end, s):
		self.rv.append(Int(self.location, int(s)))

	@spark.token("'", "default")
	def beginstr1(self, start, end, s):
		self.mode = "str1"

	@spark.token('"', "default")
	def beginstr2(self, start, end, s):
		self.mode = "str2"

	@spark.token("'", "str1")
	@spark.token('"', "str2")
	def endstr(self, start, end, s):
		self.rv.append(Str(self.location, "".join(self.collectstr)))
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
		self.collectstr.append(chr(int(s[2:], 16)))

	@spark.token("\\\\u[0-9a-fA-F]{4}", "str1", "str2")
	def escaped16bitchar(self, start, end, s):
		self.collectstr.append(chr(int(s[2:], 16)))

	@spark.token(".|\\n", "str1", "str2")
	def text(self, start, end, s):
		self.collectstr.append(s)

	@spark.token("(.|\\n)+", "default", "str1", "str2")
	def default(self, start, end, s):
		raise LexicalError(s)

	def error(self, start, end, s):
		raise LexicalError(s)


###
### Parsers for different types of code
###

class ExprParser(spark.Parser):
	emptyerror = "expression required"
	start = "expr0"

	def __init__(self, scanner):
		spark.Parser.__init__(self)
		self.scanner = scanner

	def compile(self, location):
		self.location = location
		if not location.code:
			raise ValueError(self.emptyerror)
		try:
			return self.parse(self.scanner.tokenize(location))
		except Exception as exc:
			raise Error(location) from exc

	def typestring(self, token):
		return token.type

	def makeconst(self, value):
		if value is None:
			return None_(self.location)
		elif value is True:
			return True_(self.location)
		elif value is False:
			return False_(self.location)
		elif isinstance(value, int):
			return Int(self.location, value)
		elif isinstance(value, float):
			return Float(self.location, value)
		elif isinstance(value, str):
			return Str(self.location, value)
		elif isinstance(value, color.Color):
			return Color(self.location, value)
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
		return List(self.location)

	@spark.production('buildlist ::= [ expr0')
	def expr_buildlist(self, _0, expr):
		return List(self.location, expr)

	@spark.production('buildlist ::= buildlist , expr0')
	def expr_addlist(self, list, _0, expr):
		list.items.append(expr)
		return list

	@spark.production('expr11 ::= buildlist ]')
	def expr_finishlist(self, list, _0):
		return list

	@spark.production('expr11 ::= buildlist , ]')
	def expr_finishlist1(self, list, _0, _1):
		return list

	@spark.production('expr11 ::= { }')
	def expr_emptydict(self, _0, _1):
		return Dict(self.location)

	@spark.production('builddict ::= { expr0 : expr0')
	def expr_builddict(self, _0, exprkey, _1, exprvalue):
		return Dict(self.location, (exprkey, exprvalue))

	@spark.production('builddict ::= { ** expr0')
	def expr_builddictupdate(self, _0, _1, expr):
		return Dict(self.location, (expr,))

	@spark.production('builddict ::= builddict , expr0 : expr0')
	def expr_adddict(self, dict, _0, exprkey, _1, exprvalue):
		dict.items.append((exprkey, exprvalue))
		return dict

	@spark.production('builddict ::= builddict , ** expr0')
	def expr_updatedict(self, dict, _0, _1, expr):
		dict.items.append((expr,))
		return dict

	@spark.production('expr11 ::= builddict }')
	def expr_finishdict(self, dict, _0):
		return dict

	@spark.production('expr11 ::= builddict , }')
	def expr_finishdict1(self, dict, _0, _1):
		return dict

	@spark.production('expr11 ::= ( expr0 )')
	def expr_bracket(self, _0, expr, _1):
		return expr

	@spark.production('expr10 ::= name ( )')
	def expr_callfunc0(self, name, _0, _1):
		return CallFunc(self.location, name.name)

	@spark.production('expr10 ::= name ( expr0 )')
	def expr_callfunc1(self, name, _0, arg0, _1):
		return CallFunc(self.location, name.name, arg0)

	@spark.production('expr10 ::= name ( expr0 , expr0 )')
	def expr_callfunc2(self, name, _0, arg0, _1, arg1, _2):
		return CallFunc(self.location, name.name, arg0, arg1)

	@spark.production('expr10 ::= name ( expr0 , expr0 , expr0 )')
	def expr_callfunc3(self, name, _0, arg0, _1, arg1, _2, arg2, _3):
		return CallFunc(self.location, name.name, arg0, arg1, arg2)

	@spark.production('expr10 ::= name ( expr0 , expr0 , expr0 , expr0 )')
	def expr_callfunc4(self, name, _0, arg0, _1, arg1, _2, arg2, _3, arg3, _4):
		return CallFunc(self.location, name.name, arg0, arg1, arg2, arg3)

	@spark.production('expr9 ::= expr9 . name')
	def expr_getattr(self, expr, _0, name):
		return GetAttr(self.location, expr, name.name)

	@spark.production('expr9 ::= expr9 . name ( )')
	def expr_callmeth0(self, expr, _0, name, _1, _2):
		return CallMeth(self.location, name.name, expr)

	@spark.production('expr9 ::= expr9 . name ( expr0 )')
	def expr_callmeth1(self, expr, _0, name, _1, arg1, _2):
		return CallMeth(self.location, name.name, expr, arg1)

	@spark.production('expr9 ::= expr9 . name ( expr0 , expr0 )')
	def expr_callmeth2(self, expr, _0, name, _1, arg1, _2, arg2, _3):
		return CallMeth(self.location, name.name, expr, arg1, arg2)

	@spark.production('expr9 ::= expr9 . name ( expr0 , expr0 , expr0 )')
	def expr_callmeth3(self, expr, _0, name, _1, arg1, _2, arg2, _3, arg3, _4):
		return CallMeth(self.location, name.name, expr, arg1, arg2, arg3)

	@spark.production('callmethkw ::= expr9 . name ( name = expr0')
	def methkw_startname(self, expr, _0, methname, _1, argname, _2, argvalue):
		return CallMethKeywords(self.location, methname.name, expr, (argname.name, argvalue))

	@spark.production('callmethkw ::= expr9 . name ( ** expr0')
	def methkw_startdict(self, expr, _0, methname, _1, _2, argvalue):
		return CallMethKeywords(self.location, methname.name, expr, (argvalue,))

	@spark.production('callmethkw ::= callmethkw , name = expr0')
	def methkw_buildname(self, call, _0, argname, _1, argvalue):
		call.args.append((argname.name, argvalue))
		return call

	@spark.production('callmethkw ::= callmethkw , ** expr0')
	def methkw_builddict(self, call, _0, _1, argvalue):
		call.args.append((argvalue,))
		return call

	@spark.production('expr9 ::= callmethkw )')
	def methkw_finish(self, call, _0):
		return call

	@spark.production('expr9 ::= expr9 [ expr0 ]')
	def expr_getitem(self, expr, _0, key, _1):
		if isinstance(expr, Const) and isinstance(key, Const): # Constant folding
			return self.makeconst(expr.value[key.value])
		return GetItem(self.location, expr, key)

	@spark.production('expr8 ::= expr8 [ expr0 : expr0 ]')
	def expr_getslice12(self, expr, _0, index1, _1, index2, _2):
		if isinstance(expr, Const) and isinstance(index1, Const) and isinstance(index2, Const): # Constant folding
			return self.makeconst(expr.value[index1.value:index2.value])
		return GetSlice(self.location, expr, index1, index2)

	@spark.production('expr8 ::= expr8 [ expr0 : ]')
	def expr_getslice1(self, expr, _0, index1, _1, _2):
		if isinstance(expr, Const) and isinstance(index1, Const): # Constant folding
			return self.makeconst(expr.value[index1.value:])
		return GetSlice(self.location, expr, index1, None)

	@spark.production('expr8 ::= expr8 [ : expr0 ]')
	def expr_getslice2(self, expr, _0, _1, index2, _2):
		if isinstance(expr, Const) and isinstance(index2, Const): # Constant folding
			return self.makeconst(expr.value[:index2.value])
		return GetSlice(self.location, expr, None, index2)

	@spark.production('expr8 ::= expr8 [ : ]')
	def expr_getslice(self, expr, _0, _1, _2):
		if isinstance(expr, Const): # Constant folding
			return self.makeconst(expr.value[:])
		return GetSlice(self.location, expr, None, None)

	@spark.production('expr7 ::= - expr7')
	def expr_neg(self, _0, expr):
		if isinstance(expr, Const): # Constant folding
			return self.makeconst(-expr.value)
		return Neg(self.location, expr)

	@spark.production('expr6 ::= expr6 * expr6')
	def expr_mul(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value * obj2.value)
		return Mul(self.location, obj1, obj2)

	@spark.production('expr6 ::= expr6 // expr6')
	def expr_floordiv(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value // obj2.value)
		return FloorDiv(self.location, obj1, obj2)

	@spark.production('expr6 ::= expr6 / expr6')
	def expr_truediv(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value / obj2.value)
		return TrueDiv(self.location, obj1, obj2)

	@spark.production('expr6 ::= expr6 % expr6')
	def expr_mod(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value % obj2.value)
		return Mod(self.location, obj1, obj2)

	@spark.production('expr5 ::= expr5 + expr5')
	def expr_add(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value + obj2.value)
		return Add(self.location, obj1, obj2)

	@spark.production('expr5 ::= expr5 - expr5')
	def expr_sub(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value - obj2.value)
		return Sub(self.location, obj1, obj2)

	@spark.production('expr4 ::= expr4 == expr4')
	def expr_eq(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value == obj2.value)
		return EQ(self.location, obj1, obj2)

	@spark.production('expr4 ::= expr4 != expr4')
	def expr_ne(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value != obj2.value)
		return NE(self.location, obj1, obj2)

	@spark.production('expr4 ::= expr4 < expr4')
	def expr_lt(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value < obj2.value)
		return LT(self.location, obj1, obj2)

	@spark.production('expr4 ::= expr4 <= expr4')
	def expr_le(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value <= obj2.value)
		return LE(self.location, obj1, obj2)

	@spark.production('expr4 ::= expr4 > expr4')
	def expr_gt(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value > obj2.value)
		return GT(self.location, obj1, obj2)

	@spark.production('expr4 ::= expr4 >= expr4')
	def expr_ge(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value >= obj2.value)
		return GE(self.location, obj1, obj2)

	@spark.production('expr3 ::= expr3 in expr3')
	def expr_contains(self, obj, _0, container):
		if isinstance(obj, Const) and isinstance(container, Const): # Constant folding
			return self.makeconst(obj.value in container.value)
		return Contains(self.location, obj, container)

	@spark.production('expr3 ::= expr3 not in expr3')
	def expr_notcontains(self, obj, _0, _1, container):
		if isinstance(obj, Const) and isinstance(container, Const): # Constant folding
			return self.makeconst(obj.value not in container.value)
		return NotContains(self.location, obj, container)

	@spark.production('expr2 ::= not expr2')
	def expr_not(self, _0, expr):
		if isinstance(expr, Const): # Constant folding
			return self.makeconst(not expr.value)
		return Notself.location, (expr)

	@spark.production('expr1 ::= expr1 and expr1')
	def expr_and(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value and obj2.value)
		return And(self.location, obj1, obj2)

	@spark.production('expr0 ::= expr0 or expr0')
	def expr_or(self, obj1, _0, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const): # Constant folding
			return self.makeconst(obj1.value or obj2.value)
		return Or(self.location, obj1, obj2)

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
		return For(self.location, cont, iter.name)

	@spark.production('for ::= ( name , ) in expr0')
	def for1(self, _0, varname, _1, _2, _3, cont):
		return ForUnpack(self.location, cont, varname.name)

	@spark.production('buildfor ::= ( name , name')
	def buildfor(self, _0, varname1, _1, varname2):
		return ForUnpack(self.location, None, varname1.name, varname2.name)

	@spark.production('buildfor ::= buildfor , name')
	def addfor(self, for_, _0, varname3):
		for_.varnames.append(varname3.name)
		return for_

	@spark.production('for ::= buildfor ) in expr0')
	def finishfor(self, for_, _0, _1, cont):
		for_.cont = cont
		return for_

	@spark.production('for ::= buildfor , ) in expr0')
	def finishfor1(self, for_, _0, _1, _2, cont):
		for_.cont = cont
		return for_


class StmtParser(ExprParser):
	emptyerror = "statement required"
	start = "stmt"

	@spark.production('stmt ::= name = expr0')
	def stmt_assign(self, name, _0, value):
		return StoreVar(self.location, name.name, value)

	@spark.production('stmt ::= name += expr0')
	def stmt_iadd(self, name, _0, value):
		return AddVar(self.location, name.name, value)

	@spark.production('stmt ::= name -= expr0')
	def stmt_isub(self, name, _0, value):
		return SubVar(self.location, name.name, value)

	@spark.production('stmt ::= name *= expr0')
	def stmt_imul(self, name, _0, value):
		return MulVar(self.location, name.name, value)

	@spark.production('stmt ::= name /= expr0')
	def stmt_itruediv(self, name, _0, value):
		return TrueDivVar(self.location, name.name, value)

	@spark.production('stmt ::= name //= expr0')
	def stmt_ifloordiv(self, name, _0, value):
		return FloorDivVar(self.location, name.name, value)

	@spark.production('stmt ::= name %= expr0')
	def stmt_imod(self, name, _0, value):
		return ModVar(self.location, name.name, value)

	@spark.production('stmt ::= del name')
	def stmt_del(self, _0, name):
		return DelVar(self.location, name.name)


###
### Helper functions used at template runtime
###

def _makedict(*items):
	result = {}
	for item in items:
		if len(item) == 1:
			result.update(item[0])
		else:
			result[item[0]] = item[1]
	return result

def _str(obj):
	"""
	Helper for the ``str`` function.
	"""
	if obj is None:
		return ""
	else:
		return str(obj)


def _repr(obj):
	"""
	Helper for the ``repr`` function.
	"""
	if isinstance(obj, str):
		return repr(obj)
	elif isinstance(obj, datetime.datetime):
		s = str(obj.isoformat())
		if s.endswith("T00:00:00"):
			s = s[:-9]
		return "@({})".format(s)
	elif isinstance(obj, datetime.date):
		return "@({})".format(obj.isoformat())
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
		return "[{}]".format(", ".join(_repr(item) for item in obj))
	elif isinstance(obj, collections.Mapping):
		return "{{{}}}".format(", ".join("{}: {}".format(_repr(key), _repr(value)) for (key, value) in obj.items()))
	else:
		return repr(obj)


def _xmlescape(obj):
	"""
	Helper for the ``xmlescape`` function.
	"""
	if obj is None:
		return ""
	else:
		return misc.xmlescape(str(obj))


def _json(obj):
	"""
	Helper for the ``json`` function.
	"""
	if obj is None:
		return "null"
	if isinstance(obj, (bool, int, float, str)):
		return json.dumps(obj)
	elif isinstance(obj, datetime.datetime):
		return format(obj, "new Date({}, {}, {}, {}, {}, {}, {})".format(obj.year, obj.month-1, obj.day, obj.hour, obj.minute, obj.second, obj.microsecond//1000))
	elif isinstance(obj, datetime.date):
		return format(obj, "new Date({}, {}, {})".format(obj.year, obj.month-1, obj.day))
	elif isinstance(obj, color.Color):
		return "ul4.Color.create({}, {}, {}, {})".format(*obj)
	elif isinstance(obj, collections.Mapping):
		return "{{{}}}".format(", ".join("{}: {}".format(_json(key), _json(value)) for (key, value) in obj.items()))
	elif isinstance(obj, collections.Sequence):
		return "[{}]".format(", ".join(_json(item) for item in obj))
	elif isinstance(obj, Template):
		return obj.jssource()
	else:
		raise TypeError("can't handle object of type {}".format(type(obj)))


def _isint(obj):
	"""
	Helper for the ``isint`` function.
	"""
	return isinstance(obj, int) and not isinstance(obj, bool)


def _islist(obj):
	"""
	Helper for the ``islist`` function.
	"""
	return isinstance(obj, mapping.Sequence) and not isinstance(obj, color.Color)


def _enumfl(obj):
	"""
	Helper for the ``enumfl`` function.
	"""
	lastitem = None
	first = True
	i = 0
	it = iter(obj)
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


def _isfirstlast(obj):
	"""
	Helper for the ``isfirstlast`` function.
	"""
	lastitem = None
	first = True
	it = iter(obj)
	try:
		item = next(it)
	except StopIteration:
		return
	while True:
		try:
			(lastitem, item) = (item, next(it))
		except StopIteration:
			yield (first, True, item) # Items haven't been swapped yet
			return
		else:
			yield (first, False, lastitem)
			first = False


def _isfirst(obj):
	"""
	Helper for the ``isfirst`` function.
	"""
	first = True
	for item in obj:
		yield (first, item)
		first = False


def _islast(obj):
	"""
	Helper for the ``islast`` function.
	"""
	lastitem = None
	it = iter(obj)
	try:
		item = next(it)
	except StopIteration:
		return
	while True:
		try:
			(lastitem, item) = (item, next(it))
		except StopIteration:
			yield (True, item) # Items haven't been swapped yet
			return
		else:
			yield (False, lastitem)


def _csv(obj):
	"""
	Helper for the ``csv`` function.
	"""
	if obj is None:
		return ""
	elif not isinstance(obj, str):
		obj = _repr(obj)
	if any(c in obj for c in ',"\n'):
		return '"{}"'.format(obj.replace('"', '""'))
	return obj


def _type(obj):
	"""
	Helper for the ``type`` function.
	"""
	if obj is None:
		return "none"
	elif isinstance(obj, str):
		return "str"
	elif isinstance(obj, bool):
		return "bool"
	elif isinstance(obj, int):
		return "int"
	elif isinstance(obj, float):
		return "float"
	elif isinstance(obj, (datetime.datetime, datetime.date)):
		return "date"
	elif isinstance(obj, color.Color):
		return "color"
	elif isinstance(obj, Template):
		return "template"
	elif isinstance(obj, collections.Mapping):
		return "dict"
	elif isinstance(obj, color.Color):
		return "color"
	elif isinstance(obj, collections.Sequence):
		return "list"
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
