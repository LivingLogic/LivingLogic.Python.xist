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

:mod:`ll.ul4c` compiles a template to an internal format, which makes it possible
to implement template renderers in multiple programming languages.
"""



__docformat__ = "reStructuredText"


import re, datetime, io, urllib.parse as urlparse, json, collections

from ll import spark, color, misc, ul4on


# Regular expression used for splitting dates in isoformat
datesplitter = re.compile("[-T:.]")


# Use internally by the UL4ON decoder to map names to classes
_names2classes = {}


def register(name):
	def registration(cls):
		ul4on.register("de.livinglogic.ul4." + name)(cls)
		cls.type = name
		return cls
	return registration


class Object:
	fields = {}

	def __getitem__(self, key):
		if key in self.fields:
			return getattr(self, key)
		raise KeyError(key)

###
### Location information
###

@register("location")
class Location(Object):
	"""
	A :class:`Location` object contains information about the location of a
	template tag.
	"""
	__slots__ = ("source", "type", "starttag", "endtag", "startcode", "endcode")
	fields = {"source", "type", "starttag", "endtag", "startcode", "endcode", "tag", "code"}

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
	Exception that is raised by the renderer if the function to be executed is unknown.
	"""

	def __init__(self, funcname):
		self.funcname = funcname

	def __str__(self):
		return "function {!r} unknown".format(self.funcname)


class UnknownMethodError(Exception):
	"""
	Exception that is raised by the renderer if the method to be executed is unknown.
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


class AST(Object):
	"""
	Baseclass for all syntax tree nodes.
	"""
	# used in :meth:`format` to decide if we need brackets around an operator
	precedence = None
	associative = True

	# Set of attributes available via :meth:`getitem`.
	fields = {"location", "type"}

	def __init__(self, location=None):
		self.location = location

	def __str__(self):
		return self.format(0)

	def __getitem__(self, key):
		if key in self.fields:
			return getattr(self, key)
		raise KeyError(key)

	def _formatop(self, op):
		if op.precedence < self.precedence:
			return "({})".format(op.format(0))
		elif op.precedence == self.precedence and (not isinstance(op, self.__class__) or not self.associative):
			return "({})".format(op.format(0))
		else:
			return op.format(0)

	@misc.notimplemented
	def format(self, indent):
		"""
		Format :var:`self` (with the indentation level :var:`indent`).

		This is used by :meth:`__str__.
		"""

	@misc.notimplemented
	def formatpython(self, indent):
		"""
		Format :var:`self` into valid Python source code.
		"""

	@misc.notimplemented
	def formatjava(self, indent):
		"""
		Format :var:`self` into valid Java source code.
		"""

	def ul4ondump(self, encoder):
		encoder.dump(self.location)

	def ul4onload(self, decoder):
		self.location = decoder.load()


@register("text")
class Text(AST):
	def __init__(self, location=None):
		super().__init__(location)

	def format(self, indent):
		return "{}text {!r}\n".format(indent*"\t", self.location.code)

	def formatpython(self, indent):
		return "{i}# literal at position {l.starttag}:{l.endtag}\n{i}yield {l.code!r}\n".format(i=indent*"\t", l=self.location)

	def formatjava(self, indent):
		return "{}context.write({});\n".format(indent*"\t", misc.javaexpr(self.location.code))


class Const(AST):
	"""
	Common baseclass for all constants (used for type testing in constant folding)
	"""
	precedence = 11

	def __repr__(self):
		return "{}()".format(self.__class__.__name__)


@register("none")
class None_(Const):
	"""
	The constant ``None``.
	"""

	value = None

	def format(self, indent):
		return "None"

	def formatpython(self, indent):
		return "None"

	def formatjava(self, indent):
		return "null"


@register("true")
class True_(Const):
	"""
	The boolean constant ``True``.
	"""

	value = True

	def format(self, indent):
		return "True"

	def formatpython(self, indent):
		return "True"

	def formatjava(self, indent):
		return "true"


@register("false")
class False_(Const):
	"""
	The boolean constant ``False``.
	"""

	value = False

	def format(self, indent):
		return "False"

	def formatpython(self, indent):
		return "False"

	def formatjava(self, indent):
		return "false"


class Value(Const):
	fields = Const.fields.union({"value"})

	def __init__(self, location=None, value=None):
		super().__init__(location)
		self.value = value

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.value)

	def format(self, indent):
		return _repr(self.value)

	def formatpython(self, indent):
		return repr(self.value)

	def formatjava(self, indent):
		return misc.javaexpr(self.value)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()


@register("int")
class Int(Value):
	pass


@register("float")
class Float(Value):
	pass


@register("str")
class Str(Value):
	pass


@register("date")
class Date(Value):
	pass


@register("color")
class Color(Value):
	# No need to overwrite :meth:`format` or :meth:`formatjava`

	def formatpython(self, indent):
		return "color.{!r}".format(self.value)


@register("list")
class List(AST):
	precedence = 11
	fields = AST.fields.union({"items"})

	def __init__(self, location=None, *items):
		super().__init__(location)
		self.items = list(items)

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, repr(self.items)[1:-1])

	def format(self, indent):
		return "[{}]".format(", ".join(item.format(indent) for item in self.items))

	def formatpython(self, indent):
		return "[{}]".format(", ".join(item.formatpython(indent) for item in self.items))

	def formatjava(self, indent):
		return "java.util.Arrays.asList({})".format(", ".join(item.formatjava(indent) for item in self.items))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = decoder.load()


@register("dict")
class Dict(AST):
	precedence = 11
	fields = AST.fields.union({"items"})

	def __init__(self, location=None, *items):
		super().__init__(location)
		self.items = list(items)

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, repr(self.items)[1:-1])

	def format(self, indent):
		v = []
		for item in self.items:
			if len(item) == 2:
				v.append("{}: {}".format(item[0], item[1].format(indent)))
			else:
				v.append("**{}".format(item[0].format(indent)))
		return "{{{}}}".format(", ".join(v))

	def formatpython(self, indent):
		v = []
		for item in self.items:
			if len(item) == 1:
				v.append("({},)".format(item[0].format(indent)))
			else:
				v.append("({}, {})".format(item[0].format(indent), item[1].format(indent)))
		return "ul4c._makedict({})".format(", ".join(v))

	def formatjava(self, indent):
		v = ["new com.livinglogic.ul4.MapMaker()"]
		for item in self.items:
			v.append(".add({})".format(", ".join(arg.format(indent) for arg in item)))
		v.append(".getMap()")
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = [tuple(item) for item in decoder.load()]


@register("var")
class Var(AST):
	precedence = 11
	fields = AST.fields.union({"name"})

	def __init__(self, location=None, name=None):
		super().__init__(location)
		self.name = name

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.name)

	def format(self, indent):
		return self.name

	def formatpython(self, indent):
		return "vars[{!r}]".format(self.name)

	def formatjava(self, indent):
		return "context.get({})".format(misc.javaexpr(self.name))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.name)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.name = decoder.load()


class Block(AST):
	fields = AST.fields.union({"content"})

	def __init__(self, location=None):
		super().__init__(location)
		self.content = []

	def append(self, item):
		self.content.append(item)

	def format(self, indent):
		v = []
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.format(indent))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.content = decoder.load()


@register("ieie")
class IfElIfElse(Block):
	def __init__(self, location=None, condition=None):
		super().__init__(location)
		if condition is not None:
			self.newblock(If(location, condition))

	def append(self, item):
		self.content[-1].append(item)

	def newblock(self, block):
		self.content.append(block)

	def format(self, indent):
		v = []
		for node in self.content:
			v.append(node.format(indent))
		return "".join(v)

	def formatpython(self, indent):
		v = []
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)

	def formatjava(self, indent):
		v = []
		for node in self.content:
			v.append(node.formatjava(indent))
		return "".join(v)


@register("if")
class If(Block):
	fields = Block.fields.union({"condition"})

	def __init__(self, location=None, condition=None):
		super().__init__(location)
		self.condition = condition

	def format(self, indent):
		return "{}if {}\n{}".format(indent*"\t", self.condition.format(indent), super().format(indent))

	def formatpython(self, indent):
		v = ["{i}# <?if?> tag at position {l.starttag}:{l.endtag}\n".format(i=indent*"\t", l=self.location)]
		v.append("{}if {}:\n".format(indent*"\t", self.condition.formatpython(indent)))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)

	def formatjava(self, indent):
		v = []
		v.append("{}if ({})\n".format(indent*"\t", self.condition.formatjava(indent)))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()


@register("elif")
class ElIf(Block):
	fields = Block.fields.union({"condition"})

	def __init__(self, location=None, condition=None):
		super().__init__(location)
		self.condition = condition

	def format(self, indent):
		return "{}elif {}\n{}".format(indent*"\t", self.condition.format(indent), super().format(indent))

	def formatpython(self, indent):
		v = ["{i}# <?elif?> tag at position {l.starttag}:{l.endtag}\n".format(i=indent*"\t", l=self.location)]
		v.append("{}elif {}:\n".format(indent*"\t", self.condition.formatpython(indent)))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)

	def formatjava(self, indent):
		v = []
		v.append("{}else if ({})\n".format(indent*"\t", self.condition.formatjava(indent)))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()


@register("else")
class Else(Block):
	def format(self, indent):
		return "{}else\n{}".format(indent*"\t", super().format(indent))

	def formatpython(self, indent):
		v = ["{i}# <?else?> tag at position {l.starttag}:{l.endtag}\n".format(i=indent*"\t", l=self.location)]
		v.append("{}else:\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)

	def formatjava(self, indent):
		v = []
		v.append("{}else\n".format(indent*"\t"))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		return "".join(v)


@register("for")
class For(Block):
	fields = Block.fields.union({"container", "varname"})

	def __init__(self, location=None, container=None, varname=None):
		super().__init__(location)
		self.container = container
		self.varname = varname

	def __repr__(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.container, self.varname)

	def format(self, indent):
		return "{}for {} in {}\n{}".format(indent*"\t", self.varname, self.container.format(indent), super().format(indent))

	def formatpython(self, indent):
		v = ["{i}# <?for?> tag at position {l.starttag}:{l.endtag}\n".format(i=indent*"\t", l=self.location)]
		v.append("{}for vars[{!r}] in {}:\n".format(indent*"\t", self.varname, self.container.formatpython(indent)))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)

	def formatjava(self, indent):
		v = []
		v.append("{indent}for (Iterator iter{id:x} = com.livinglogic.ul4.Utils.iterator({container}); iter{id:x}.hasNext();)\n".format(indent=indent*"\t", id=id(self), container=self.container.formatjava(indent)))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		v.append("{}com.livinglogic.ul4.ForNormal.unpackLoopVariable(context, iter{:x}.next(), {});\n".format(indent*"\t", id(self), misc.javaexpr(self.varname)))
		for node in self.content:
			v.append(node.formatjava(indent))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.container)
		encoder.dump(self.varname)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.container = decoder.load()
		self.varname = decoder.load()


@register("foru")
class ForUnpack(Block):
	fields = Block.fields.union({"container", "varnames"})

	def __init__(self, location=None, container=None, *varnames):
		super().__init__(location)
		self.container = container
		self.varnames = list(varnames)

	def __repr__(self):
		return "{}({!r}, {})".format(self.__class__.__name__, self.container, repr(self.varnames)[1:-1])

	def format(self, indent):
		return "{}for ({}) in {}\n{}".format(indent*"\t", ", ".join(self.varnames), self.container.format(indent), super().format(indent))

	def formatpython(self, indent):
		v = ["{i}# <?for?> tag at position {l.starttag}:{l.endtag}\n".format(i=indent*"\t", l=self.location)]
		v.append("{}for ({}) in {}:\n".format(indent*"\t", " ".join("vars[{!r}],".format(varname) for varname in self.varnames), self.container.formatpython(indent)))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)

	def formatjava(self, indent):
		v = []
		v.append("{indent}for (Iterator iter{id:x} = com.livinglogic.ul4.Utils.iterator({container}); iter{id:x}.hasNext();)\n".format(indent=indent*"\t", id=id(self), container=self.container.formatjava(indent)))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		varnames = "java.util.Arrays.asList({})".format(", ".join(misc.javaexpr(varname) for varname in self.varnames))
		v.append("{}com.livinglogic.ul4.ForUnpack.unpackLoopVariable(context, iter{:x}.next(), {});\n".format(indent*"\t", id(self), varnames))
		for node in self.content:
			v.append(node.formatjava(indent))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.container)
		encoder.dump(self.varnames)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.container = decoder.load()
		self.varnames = decoder.load()


@register("break")
class Break(AST):
	def format(self, indent):
		return "{}break\n".format(indent*"\t")

	def formatpython(self, indent):
		return "{i}# <?break?> tag at position {l.starttag}:{l.endtag}\n{i}continue\n".format(i=indent*"\t", l=self.location)

	def formatjava(self, indent):
		return "{}break;\n".format(indent*"\t")


@register("continue")
class Continue(AST):
	def format(self, indent):
		return "{}continue\n".format(indent*"\t")

	def formatpython(self, indent):
		return "{i}# <?continue?> tag at position {l.starttag}:{l.endtag}\n{i}continue\n".format(i=indent*"\t", l=self.location)

	def formatjava(self, indent):
		return "{}continue;\n".format(indent*"\t")


@register("getattr")
class GetAttr(AST):
	precedence = 9
	associative = False
	fields = AST.fields.union({"obj", "attrname"})

	def __init__(self, location=None, obj=None, attrname=None):
		super().__init__(location)
		self.obj = obj
		self.attrname = attrname

	def __repr__(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.obj, self.attrname)

	def format(self, indent):
		return "{}.{}".format(self._formatop(self.obj), self.attrname)

	def formatpython(self, indent):
		return "{}[{!r}]".format(self.obj.formatpython(indent), self.attrname)

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.getItem({}, {})".format(self.obj.formatjava(indent), misc.javaexpr(self.attrname))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.attrname)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.attrname = decoder.load()


@register("getslice")
class GetSlice(AST):
	precedence = 8
	associative = False
	fields = AST.fields.union({"obj", "index1", "index2"})

	def __init__(self, location=None, obj=None, index1=None, index2=None):
		super().__init__(location)
		self.obj = obj
		self.index1 = index1
		self.index2 = index2

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.obj, self.index1, self.index2)

	def format(self, indent):
		return "{}[{}:{}]".format(self._formatop(self.obj), self.index1.format(indent) if self.index1 is not None else "", self.index2.format(indent) if self.index2 is not None else "")

	def formatpython(self, indent):
		return "{}[{}:{}]".format(self.obj.formatpython(indent), self.index1.formatpython(indent) if self.index1 is not None else "", self.index2.formatpython(indent) if self.index2 is not None else "")

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.getSlice({}, {}, {})".format(self.obj.formatjava(indent), self.index1.formatjava(indent) if self.index1 is not None else "null", self.index2.formatjava(indent) if self.index2 is not None else "null")

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
	fields = AST.fields.union({"obj"})

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


@register("not")
class Not(Unary):
	precedence = 2

	def format(self, indent):
		return "not {}".format(self._formatop(self.obj))

	def formatpython(self, indent):
		return "not ({})".format(self.obj.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.not({})".format(self.obj.formatjava(indent))


@register("neg")
class Neg(Unary):
	precedence = 7

	def format(self, indent):
		return "-{}".format(self._formatop(self.obj))

	def formatpython(self, indent):
		return "-({})".format(self.obj.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.neg({})".format(self.obj.formatjava(indent))


@register("print")
class Print(Unary):
	def format(self, indent):
		return "{}print {}\n".format(indent*"\t", self.obj.format(indent))

	def formatpython(self, indent):
		return "{i}# <?print?> tag at position {l.starttag}:{l.endtag}\n{i}yield ul4c._str({o})\n".format(i=indent*"\t", o=self.obj.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{}context.write(com.livinglogic.ul4.Utils.str({});\n".format(indent*"\t", self.obj.formatjava(indent))


@register("printx")
class PrintX(Unary):
	def format(self, indent):
		return "{}printx {}\n".format(indent*"\t", self.obj.format(indent))

	def formatpython(self, indent):
		return "{i}# <?printx?> tag at position {l.starttag}:{l.endtag}\n{i}yield ul4c._xmlescape({o})\n".format(i=indent*"\t", o=self.obj.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{}context.write(com.livinglogic.ul4.Utils.xmlescape({});\n".format(indent*"\t", self.obj.formatjava(indent))


class Binary(AST):
	fields = AST.fields.union({"obj1", "obj2"})

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


@register("getitem")
class GetItem(Binary):
	precedence = 9
	associative = False

	def format(self, indent):
		return "{}[{}]".format(self._formatop(self.obj1), self.obj2.format(indent))

	def formatpython(self, indent):
		return "({})[{}]".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.getItem({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("eq")
class EQ(Binary):
	precedence = 4
	associative = False

	def format(self, indent):
		return "{} == {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) == ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.eq({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("ne")
class NE(Binary):
	precedence = 4
	associative = False

	def format(self, indent):
		return "{} != {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) != ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.ne({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("lt")
class LT(Binary):
	precedence = 4
	associative = False

	def format(self, indent):
		return "{} < {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) < ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.lt({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("le")
class LE(Binary):
	precedence = 4
	associative = False

	def format(self, indent):
		return "{} <= {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) <= ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.le({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("gt")
class GT(Binary):
	precedence = 4
	associative = False

	def format(self, indent):
		return "{} > {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) > ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.gt({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("ge")
class GE(Binary):
	precedence = 4
	associative = False

	def format(self, indent):
		return "{} >= {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) >= ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.ge({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("contains")
class Contains(Binary):
	precedence = 3
	associative = False

	def format(self, indent):
		return "{} in {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) in ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.contains({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("notcontains")
class NotContains(Binary):
	precedence = 3
	associative = False

	def format(self, indent):
		return "{} not in {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) not in ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.notcontains({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("add")
class Add(Binary):
	precedence = 5

	def format(self, indent):
		return "{}+{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) + ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.add({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("sub")
class Sub(Binary):
	precedence = 5
	associative = False

	def format(self, indent):
		return "{}-{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) - ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.sub({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("mul")
class Mul(Binary):
	precedence = 6

	def format(self, indent):
		return "{}*{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) * ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.mul({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("floordiv")
class FloorDiv(Binary):
	precedence = 6
	associative = False

	def format(self, indent):
		return "{}//{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) // ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.floordiv({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("truediv")
class TrueDiv(Binary):
	precedence = 6
	associative = False

	def format(self, indent):
		return "{}/{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) / ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.truediv({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("and")
class And(Binary):
	precedence = 1

	def format(self, indent):
		return "{} and {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) and ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.getBool(context.push({})) ? context.pop({}) : context.pop()".format(self.obj2.formatjava(indent), self.obj1.formatjava(indent))


@register("or")
class Or(Binary):
	precedence = 0

	def format(self, indent):
		return "{} or {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) or ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.getBool(context.push({})) ? context.pop() : context.pop({})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("mod")
class Mod(Binary):
	precedence = 6
	associative = False

	def format(self, indent):
		return "{}%{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) % ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Utils.mod({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


class ChangeVar(AST):
	fields = AST.fields.union({"varname", "value"})

	def __init__(self, location=None, varname=None, value=None):
		super().__init__(location)
		self.varname = varname
		self.value = value

	def __repr__(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.varname, self.value)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.varname)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.varname = decoder.load()
		self.value = decoder.load()


@register("storevar")
class StoreVar(ChangeVar):
	def format(self, indent):
		return "{}{} = {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag}\n{i}vars[{n!r}] = {v}\n".format(i=indent*"\t", n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "context.set({}, {});".format(misc.javaexpr(self.varname), self.value.formatjava(indent))


@register("addvar")
class AddVar(ChangeVar):
	def format(self, indent):
		return "{}{} += {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag}\n{i}vars[{n!r}] += {v}\n".format(i=indent*"\t", n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		varname = misc.javaexpr(self.varname)
		return "context.set({}, com.livinglogic.ul4.Utils.add(context.get({}), {}));".format(varname, varname, self.value.formatjava(indent))


@register("subvar")
class SubVar(ChangeVar):
	def format(self, indent):
		return "{}{} -= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag}\n{i}vars[{n!r}] -= {v}\n".format(i=indent*"\t", n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		varname = misc.javaexpr(self.varname)
		return "context.set({}, com.livinglogic.ul4.Utils.sub(context.get({}), {}));".format(varname, varname, self.value.formatjava(indent))


@register("mulvar")
class MulVar(ChangeVar):
	def format(self, indent):
		return "{}{} *= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag}\n{i}vars[{n!r}] *= {v}\n".format(i=indent*"\t", n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		varname = misc.javaexpr(self.varname)
		return "context.set({}, com.livinglogic.ul4.Utils.mul(context.get({}), {}));".format(varname, varname, self.value.formatjava(indent))


@register("floordivvar")
class FloorDivVar(ChangeVar):
	def format(self, indent):
		return "{}{} //= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag}\n{i}vars[{n!r}] //= {v}\n".format(i=indent*"\t", n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		varname = misc.javaexpr(self.varname)
		return "context.set({}, com.livinglogic.ul4.Utils.floordiv(context.get({}), {}));".format(varname, varname, self.value.formatjava(indent))


@register("truedivvar")
class TrueDivVar(ChangeVar):
	def format(self, indent):
		return "{}{} /= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag}\n{i}vars[{n!r}] /= {v}\n".format(i=indent*"\t", n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		varname = misc.javaexpr(self.varname)
		return "context.set({}, com.livinglogic.ul4.Utils.truediv(context.get({}), {}));".format(varname, varname, self.value.formatjava(indent))


@register("modvar")
class ModVar(ChangeVar):
	def format(self, indent):
		return "{}{} %= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag}\n{i}vars[{n!r}] %= {v}\n".format(i=indent*"\t", n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		varname = misc.javaexpr(self.varname)
		return "context.set({}, com.livinglogic.ul4.Utils.mod(context.get({}), {}));".format(varname, varname, self.value.formatjava(indent))


@register("delvar")
class DelVar(AST):
	fields = AST.fields.union({"varname"})

	def __init__(self, location=None, varname=None):
		super().__init__(location)
		self.varname = varname

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.varname)

	def format(self, indent):
		return "{}del {}\n".format(indent*"\t", self.varname)

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag}\n{i}del vars[{n!r}]\n".format(i=indent*"\t", n=self.varname, l=self.location)

	def formatjava(self, indent):
		return "context.remove({});".format(misc.javaexpr(self.varname))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.varname)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.varname = decoder.load()


@register("callfunc")
class CallFunc(AST):
	precedence = 10
	associative = False
	fields = AST.fields.union({"funcname", "args"})

	def __init__(self, location=None, funcname=None, *args):
		super().__init__(location)
		self.funcname = funcname
		self.args = list(args)

	def __repr__(self):
		if self.args:
			return "{}({!r}, {})".format(self.__class__.__name__, self.funcname, repr(self.args)[1:-1])
		else:
			return "{}({!r})".format(self.__class__.__name__, self.funcname)

	def format(self, indent):
		return "{}({})".format(self.funcname, ", ".join(arg.format(indent) for arg in self.args))

	def formatpython(self, indent):
		functions = dict(
			now="datetime.datetime.now({})".format,
			utcnow="datetime.datetime.utcnow({})".format,
			vars="ul4c._vars(vars, {})".format,
			random="random.random({})".format,
			xmlescape="ul4c._xmlescape({})".format,
			csv="ul4c._csv({})".format,
			asjson="ul4c._asjson({})".format,
			fromjson="ul4c._fromjson({})".format,
			asul4on="ul4c._asul4on({})".format,
			fromul4on="ul4c._fromul4on({})".format,
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
			isnone="ul4c._isnone({})".format,
			isstr="ul4c._isstr({})".format,
			isint="ul4c._isint({})".format,
			isfloat="ul4c._isfloat({})".format,
			isbool="ul4c._isbool({})".format,
			isdate="ul4c._isdate({})".format,
			islist="ul4c._islist({})".format,
			isdict="ul4c._isdict({})".format,
			iscolor="ul4c._iscolor({})".format,
			istemplate="ul4c._istemplate({})".format,
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
			randchoice="random.choice({})".format,
			format="format({})".format,
			zip="zip({})".format,
			urlquote="ul4c._urlquote({})".format,
			urlunquote="ul4c._urlunquote({})".format,
			rgb="color.Color.fromrgb({})".format,
			hls="color.Color.fromhls({})".format,
			hsv="color.Color.fromhsv({})".format,
		)
		try:
			formatter = functions[self.funcname]
		except KeyError:
			raise UnknownFunctionError(self.funcname)
		return formatter(", ".join(arg.formatpython(indent) for arg in self.args))

	def formatjava(self, indent):
		functions = dict(
			now="com.livinglogic.ul4.Utils.now({})".format,
			utcnow="com.livinglogic.ul4.Utils.now({})".format,
			vars="variables".format,
			random="com.livinglogic.ul4.Utils.random({})".format,
			xmlescape="com.livinglogic.ul4.Utils.xmlescape({})".format,
			csv="com.livinglogic.ul4.Utils.csv({})".format,
			asjson="com.livinglogic.ul4.Utils.asjson({})".format,
			fromjson="com.livinglogic.ul4.Utils.fromjson({})".format,
			str="com.livinglogic.ul4.Utils.str({})".format,
			int="com.livinglogic.ul4.Utils.int({})".format,
			float="com.livinglogic.ul4.Utils.float({})".format,
			bool="com.livinglogic.ul4.Utils.getBool({})".format,
			len="com.livinglogic.ul4.Utils.len({})".format,
			abs="com.livinglogic.ul4.Utils.abs({})".format,
			enumerate="com.livinglogic.ul4.Utils.enumerate({})".format,
			enumfl="com.livinglogic.ul4.Utils.enumfl({})".format,
			isfirstlast="com.livinglogic.ul4.Utils.isfirstlast({})".format,
			isfirst="com.livinglogic.ul4.Utils.isfirst({})".format,
			islast="com.livinglogic.ul4.Utils.islast({})".format,
			isnone="com.livinglogic.ul4.Utils.isnone({})".format,
			isstr="com.livinglogic.ul4.Utils.isstr({})".format,
			isint="com.livinglogic.ul4.Utils.isint({})".format,
			isfloat="com.livinglogic.ul4.Utils.isfloat({})".format,
			isbool="com.livinglogic.ul4.Utils.isbool({})".format,
			isdate="com.livinglogic.ul4.Utils.isdate({})".format,
			islist="com.livinglogic.ul4.Utils.islist({})".format,
			isdict="com.livinglogic.ul4.Utils.isdict({})".format,
			iscolor="com.livinglogic.ul4.Utils.iscolor({})".format,
			istemplate="com.livinglogic.ul4.Utils.istemplate({})".format,
			repr="com.livinglogic.ul4.Utils.repr({})".format,
			get="variables.get({})".format,
			chr="com.livinglogic.ul4.Utils.chr({})".format,
			ord="com.livinglogic.ul4.Utils.ord({})".format,
			hex="com.livinglogic.ul4.Utils.hex({})".format,
			oct="com.livinglogic.ul4.Utils.oct({})".format,
			bin="com.livinglogic.ul4.Utils.bin({})".format,
			sorted="com.livinglogic.ul4.Utils.sorted({})".format,
			range="com.livinglogic.ul4.Utils.range({})".format,
			type="com.livinglogic.ul4.Utils.type({})".format,
			reversed="com.livinglogic.ul4.Utils.reversed({})".format,
			randrange="com.livinglogic.ul4.Utils.randrange({})".format,
			randchoice="com.livinglogic.ul4.Utils.randchoice({})".format,
			format="com.livinglogic.ul4.Utils.format({})".format,
			zip="com.livinglogic.ul4.Utils.zip({})".format,
			urlquote="com.livinglogic.ul4.Utils.urlquote({})".format,
			urlunquote="com.livinglogic.ul4.Utils.urlunquote({})".format,
			rgb="com.livinglogic.ul4.Color.fromrgb({})".format,
			hls="com.livinglogic.ul4.Color.fromhls({})".format,
			hsv="com.livinglogic.ul4.Color.fromhsv({})".format,
		)
		try:
			formatter = functions[self.funcname]
		except KeyError:
			raise UnknownFunctionError(self.funcname)
		return formatter(", ".join(arg.formatjava(indent) for arg in self.args))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.funcname)
		encoder.dump(self.args)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.funcname = decoder.load()
		self.args = decoder.load()


@register("callmeth")
class CallMeth(AST):
	precedence = 9
	associative = False
	fields = AST.fields.union({"methname", "obj", "args"})

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

	def format(self, indent):
		return "({}).{}({})".format(self._formatop(self.obj), self.methname, ", ".join(arg.format(indent) for arg in self.args))

	def formatpython(self, indent):
		methods = dict(
			split="({}).split({})".format,
			rsplit="({}).rsplit({})".format,
			strip="({}).strip({})".format,
			lstrip="({}).lstrip({})".format,
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
			renders="''.join(({})({}))".format,
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

	def formatjava(self, indent):
		functions = dict(
			now="com.livinglogic.ul4.Utils.now({})".format,
		)
		try:
			formatter = functions[self.methname]
		except KeyError:
			raise UnknownFunctionError(self.methname)
		return formatter(self.obj.formatjava(indent), ", ".join(arg.formatjava(indent) for arg in self.args))

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


@register("callmethkw")
class CallMethKeywords(AST):
	precedence = 9
	associative = False
	fields = AST.fields.union({"methname", "obj", "args"})

	def __init__(self, location=None, methname=None, obj=None, *args):
		super().__init__(location)
		self.methname = methname
		self.obj = obj
		self.args = list(args)

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.methname, self.obj, self.args)

	def format(self, indent):
		args = []
		for arg in self.args:
			if len(arg) == 1:
				args.append("**{}".format(arg[0].format(indent)))
			else:
				args.append("{}={}".format(arg[0], arg[1].format(indent)))
		return "{}.{}({})".format(self._formatop(self.obj), self.methname, ", ".join(args))

	def formatpython(self, indent):
		if self.methname == "renders":
			args = []
			for arg in self.args:
				if len(arg) == 1:
					args.append("({},)".format(arg[0].formatpython(indent)))
				else:
					args.append("({!r}, {})".format(arg[0], arg[1].formatpython(indent)))
			args = "ul4c._makedict({})".format(", ".join(args))
			return "''.join(({})(**{}))".format(self.obj.formatpython(indent), args)
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
		self.args = [tuple(arg) for arg in decoder.load()]


@register("render")
class Render(Unary):
	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.obj)

	def format(self, indent):
		return "{}render {}\n".format(indent*"\t", self.obj.format(indent))

	def formatpython(self, indent):
		if isinstance(self.obj, (CallMeth, CallMethKeywords)) and self.obj.methname == "render":
			v = ["{i}# <?render?> tag at position {l.starttag}:{l.endtag}\n".format(i=indent*"\t", l=self.location)]
			if self.obj.args:
				args = []
				for arg in self.obj.args:
					if len(arg) == 1:
						args.append("({},)".format(arg[0].formatpython(indent)))
					else:
						args.append("({!r}, {})".format(arg[0], arg[1].formatpython(indent)))
				args = "**ul4c._makedict({})".format(", ".join(args))
			else:
				args = ""
			v.append("{}for part in ({})({}):\n".format(indent*"\t", self.obj.obj.formatpython(indent), args))
			v.append("{}\tyield part\n".format(indent*"\t"))
			return "".join(v)
		else:
			return "{i}# <?render?> tag at position {l.starttag}:{l.endtag}\n{i}yield ul4c._str({o})\n".format(i=indent*"\t", o=self.obj.formatpython(indent), l=self.location)


@register("template")
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
	fields = Block.fields.union({"source", "name", "startdelim", "enddelim"})

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
		self._subtemplatesbyid = None
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

	def format(self, indent):
		v = []
		name = self.name if self.name is not None else "unnamed"
		v.append("{}def {}()\n".format(indent*"\t", name))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.format(indent))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		return "".join(v)

	def formatpython(self, indent):
		return "{i}# <?def?> tag at position {l.starttag}:{l.endtag}\n{i}vars[{n!r}] = self._getsubtemplate({id!r})\n".format(i=indent*"\t", n=self.name if self.name is not None else "unnamed", id=id(self), l=self.location)

	def _getsubtemplate(self, tid):
		if self._subtemplatesbyid is None:
			self._subtemplatesbyid = {}
			def add(block):
				for child in block.content:
					if isinstance(child, Template):
						self._subtemplatesbyid[id(child)] = child
					elif isinstance(child, Block):
						add(child)
			add(self)
		return self._subtemplatesbyid[tid]

	def _java(self, indent):
		v = []
		v.append("new com.livinglogic.ul4.CompiledTemplate()\n")
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		v.append("{}public String getName()\n".format(indent*"\t"))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		v.append("{}return {};\n".format(indent*"\t", misc.javaexpr(self.name if self.name is not None else "unnamed")))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		v.append("\n")
		v.append("{}public void render(EvaluationContext context) throws java.io.IOException\n".format(indent*"\t"))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatjava(indent))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		indent -= 1
		v.append("{}}}".format(indent*"\t"))
		return "".join(v)

	def formatjava(self, indent):
		return "{}variables.put({}, {});\n".format(indent*"\t", misc.javaexpr(self.name if self.name is not None else "unnamed"), self._java(indent))

	def render(self, **vars):
		"""
		Render the template iteratively (i.e. this is a generator).
		:var:`vars` contains the top level variables available to the
		template code.
		"""
		return self.pythonfunction()(self, vars)

	def renders(self, **vars):
		"""
		Render the template as a string. :var:`vars` contains the top level
		variables available to the template code.
		"""
		return "".join(self.pythonfunction()(self, vars))

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
		return self.pythonfunction()(self, vars)

	def pythonsource(self):
		"""
		Return the template as Python source code.
		"""
		v = []
		v.append("def {}(self, vars):\n".format(self.name if self.name is not None else "unnamed"))
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
		return "ul4.Template.loads({})".format(_asjson(self.dumps()))

	def javasource(self, indent=0, interpreted=True):
		"""
		Return the template as Java source code.

		:var:`indent` is the indentation level.

		:var:`interpreted` can be used the specify whether a ``CompiledTemplate``
		or an ``InterpretedTemplate`` will be used.
		"""
		if interpreted:
			return "com.livinglogic.ul4.InterpretedTemplate.loads({})\n".format(misc.javaexpr(self.dumps()))
		else:
			return self._java(indent)

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
						raise BlockError("else doesn't match any if")
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
					last = stack.pop()
					# Fix source attribute of sub template
					if isinstance(last, Template):
						# ``source`` does not include the ``<?def?>``/``<?end def?>`` tags
						last.source = last.location.source[last.location.endtag:location.starttag]
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

	def __repr__(self):
		return "<{}.{} object at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, id(self))


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
			self.rv.append(Var(self.location, s))

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
	@spark.production('expr11 ::= var')
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

	@spark.production('expr10 ::= var ( )')
	def expr_callfunc0(self, var, _0, _1):
		return CallFunc(self.location, var.name)

	@spark.production('expr10 ::= var ( expr0 )')
	def expr_callfunc1(self, var, _0, arg0, _1):
		return CallFunc(self.location, var.name, arg0)

	@spark.production('expr10 ::= var ( expr0 , expr0 )')
	def expr_callfunc2(self, var, _0, arg0, _1, arg1, _2):
		return CallFunc(self.location, var.name, arg0, arg1)

	@spark.production('expr10 ::= var ( expr0 , expr0 , expr0 )')
	def expr_callfunc3(self, var, _0, arg0, _1, arg1, _2, arg2, _3):
		return CallFunc(self.location, var.name, arg0, arg1, arg2)

	@spark.production('expr10 ::= var ( expr0 , expr0 , expr0 , expr0 )')
	def expr_callfunc4(self, var, _0, arg0, _1, arg1, _2, arg2, _3, arg3, _4):
		return CallFunc(self.location, var.name, arg0, arg1, arg2, arg3)

	@spark.production('expr9 ::= expr9 . var')
	def expr_getattr(self, expr, _0, var):
		return GetAttr(self.location, expr, var.name)

	@spark.production('expr9 ::= expr9 . var ( )')
	def expr_callmeth0(self, expr, _0, var, _1, _2):
		return CallMeth(self.location, var.name, expr)

	@spark.production('expr9 ::= expr9 . var ( expr0 )')
	def expr_callmeth1(self, expr, _0, var, _1, arg1, _2):
		return CallMeth(self.location, var.name, expr, arg1)

	@spark.production('expr9 ::= expr9 . var ( expr0 , expr0 )')
	def expr_callmeth2(self, expr, _0, var, _1, arg1, _2, arg2, _3):
		return CallMeth(self.location, var.name, expr, arg1, arg2)

	@spark.production('expr9 ::= expr9 . var ( expr0 , expr0 , expr0 )')
	def expr_callmeth3(self, expr, _0, var, _1, arg1, _2, arg2, _3, arg3, _4):
		return CallMeth(self.location, var.name, expr, arg1, arg2, arg3)

	@spark.production('callmethkw ::= expr9 . var ( var = expr0')
	def methkw_startname(self, expr, _0, methname, _1, argname, _2, argvalue):
		return CallMethKeywords(self.location, methname.name, expr, (argname.name, argvalue))

	@spark.production('callmethkw ::= expr9 . var ( ** expr0')
	def methkw_startdict(self, expr, _0, methname, _1, _2, argvalue):
		return CallMethKeywords(self.location, methname.name, expr, (argvalue,))

	@spark.production('callmethkw ::= callmethkw , var = expr0')
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
		return Not(self.location, expr)

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

	@spark.production('for ::= var in expr0')
	def for0(self, iter, _0, cont):
		return For(self.location, cont, iter.name)

	@spark.production('for ::= ( var , ) in expr0')
	def for1(self, _0, varname, _1, _2, _3, cont):
		return ForUnpack(self.location, cont, varname.name)

	@spark.production('buildfor ::= ( var , var')
	def buildfor(self, _0, varname1, _1, varname2):
		return ForUnpack(self.location, None, varname1.name, varname2.name)

	@spark.production('buildfor ::= buildfor , var')
	def addfor(self, for_, _0, varname3):
		for_.varnames.append(varname3.name)
		return for_

	@spark.production('for ::= buildfor ) in expr0')
	def finishfor(self, for_, _0, _1, cont):
		for_.container = cont
		return for_

	@spark.production('for ::= buildfor , ) in expr0')
	def finishfor1(self, for_, _0, _1, _2, cont):
		for_.container = cont
		return for_


class StmtParser(ExprParser):
	emptyerror = "statement required"
	start = "stmt"

	@spark.production('stmt ::= var = expr0')
	def stmt_assign(self, var, _0, value):
		return StoreVar(self.location, var.name, value)

	@spark.production('stmt ::= var += expr0')
	def stmt_iadd(self, var, _0, value):
		return AddVar(self.location, var.name, value)

	@spark.production('stmt ::= var -= expr0')
	def stmt_isub(self, var, _0, value):
		return SubVar(self.location, var.name, value)

	@spark.production('stmt ::= var *= expr0')
	def stmt_imul(self, var, _0, value):
		return MulVar(self.location, var.name, value)

	@spark.production('stmt ::= var /= expr0')
	def stmt_itruediv(self, var, _0, value):
		return TrueDivVar(self.location, var.name, value)

	@spark.production('stmt ::= var //= expr0')
	def stmt_ifloordiv(self, var, _0, value):
		return FloorDivVar(self.location, var.name, value)

	@spark.production('stmt ::= var %= expr0')
	def stmt_imod(self, var, _0, value):
		return ModVar(self.location, var.name, value)

	@spark.production('stmt ::= del var')
	def stmt_del(self, _0, var):
		return DelVar(self.location, var.name)


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


def _vars(vars):
	"""
	Helper for the ``vars`` function.
	"""
	return vars


def _str(obj=None):
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


def _asjson(obj):
	"""
	Helper for the ``asjson`` function.
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
		return "{{{}}}".format(", ".join("{}: {}".format(_asjson(key), _asjson(value)) for (key, value) in obj.items()))
	elif isinstance(obj, collections.Sequence):
		return "[{}]".format(", ".join(_asjson(item) for item in obj))
	elif isinstance(obj, Template):
		return obj.jssource()
	else:
		raise TypeError("can't handle object of type {}".format(type(obj)))


def _fromjson(obj):
	"""
	Helper for the ``fromjson`` function.
	"""
	return json.loads(obj)


def _asul4on(obj):
	"""
	Helper for the ``asul4on`` function.
	"""
	return ul4on.dumps(obj)


def _fromul4on(obj):
	"""
	Helper for the ``fromul4on`` function.
	"""
	return ul4on.loads(obj)


def _isnone(obj):
	"""
	Helper for the ``isnone`` function.
	"""
	return obj is None


def _isbool(obj):
	"""
	Helper for the ``isbool`` function.
	"""
	return isinstance(obj, bool)


def _isint(obj):
	"""
	Helper for the ``isint`` function.
	"""
	return isinstance(obj, int) and not isinstance(obj, bool)


def _isfloat(obj):
	"""
	Helper for the ``isfloat`` function.
	"""
	return isinstance(obj, float)


def _isstr(obj):
	"""
	Helper for the ``isstr`` function.
	"""
	return isinstance(obj, str)


def _isdate(obj):
	"""
	Helper for the ``isdate`` function.
	"""
	return isinstance(obj, (datetime.datetime, datetime.date))


def _islist(obj):
	"""
	Helper for the ``islist`` function.
	"""
	return isinstance(obj, collections.Sequence) and not isinstance(obj, str) and not isinstance(obj, color.Color)


def _isdict(obj):
	"""
	Helper for the ``isdict`` function.
	"""
	return isinstance(obj, collections.Mapping) and not isinstance(obj, Template)


def _iscolor(obj):
	"""
	Helper for the ``iscolor`` function.
	"""
	return isinstance(obj, color.Color)


def _istemplate(obj):
	"""
	Helper for the ``istemplate`` function.
	"""
	return isinstance(obj, Template)


def _enumfl(obj, start=0):
	"""
	Helper for the ``enumfl`` function.
	"""
	lastitem = None
	first = True
	i = start
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


def _urlquote(obj):
	"""
	Helper for the ``urlquote`` function.
	"""
	return urlparse.quote_plus(obj)


def _urlunquote(obj):
	"""
	Helper for the ``urlunquote`` function.
	"""
	return urlparse.unquote_plus(obj)


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
