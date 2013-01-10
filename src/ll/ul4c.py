# -*- coding: utf-8 -*-

## Copyright 2009-2013 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2013 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`ll.ul4c` provides templating for XML/HTML as well as any other text-based
format. A template defines placeholders for data output and basic logic (like
loops and conditional blocks), that define how the final rendered output will
look.

:mod:`ll.ul4c` compiles a template to an internal format, which makes it
possible to implement template renderers in multiple programming languages.
"""


__docformat__ = "reStructuredText"


import re, datetime, urllib.parse as urlparse, json, collections, locale, itertools, random, datetime

import antlr3

from ll import color, misc


# Regular expression used for splitting dates in isoformat
datesplitter = re.compile("[-T:.]")


def register(name):
	from ll import ul4on
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
		return "{!r} at {}:{} (line {}, col {})".format(self.tag, self.starttag, self.endtag, line, col)

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
		return "in {}".format(self.location)


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
### Various versions of undefined objects
###

class Undefined(object):
	def __bool__(self):
		return False

	def __iter__(self):
		raise TypeError("{!r} doesn't support iteration".format(self))

	def __len__(self):
		raise AttributeError("{!r} has no len()".format(self))

	def __getattr__(self, key):
		raise AttributeError("{!r} has no attribute {!r}".format(self, key))

	def __getitem__(self, key):
		raise TypeError("{!r} doesn't support indexing (key={!r})".format(self, key))


class UndefinedKey(Undefined):
	def __init__(self, key):
		self.__key = key

	def __repr__(self):
		return "undefined object for key {!r}".format(self.__key)


class UndefinedIndex(Undefined):
	def __init__(self, index):
		self.__index = index

	def __repr__(self):
		return "undefined object at index {!r}".format(self.__index)




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
	Base class for all syntax tree nodes.
	"""
	# used in :meth:`format` to decide if we need brackets around an operator
	precedence = None
	associative = True

	# Set of attributes available via :meth:`getitem`.
	fields = {"type"}

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

	def _add2template(self, template):
		# Helper methods for adding all top level AST nodes to a map
		template._astsbyid[id(self)] = self

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


class Tag(AST):
	"""
	Base class for all syntax tree nodes that are the top level node in a
	template tag.
	"""
	# Set of attributes available via :meth:`getitem`.
	fields = AST.fields.union({"location"})

	def __init__(self, location=None):
		self.location = location

	def ul4ondump(self, encoder):
		encoder.dump(self.location)

	def ul4onload(self, decoder):
		self.location = decoder.load()


@register("text")
class Text(Tag):
	"""
	AST node for literal text.
	"""
	def format(self, indent):
		return "{}text {!r}\n".format(indent*"\t", self.location.code)

	def formatpython(self, indent):
		return "{i}# literal at position {l.starttag}:{l.endtag} ({id})\n{i}yield {l.code!r}\n".format(i=indent*"\t", id=id(self), l=self.location)


@register("const")
class Const(AST):
	"""
	Load a constant
	"""
	precedence = 11
	fields = AST.fields.union({"value"})

	def __init__(self, value=None):
		self.value = value

	def format(self, indent):
		return Template.function_repr(None, self.value)

	def formatpython(self, indent):
		if isinstance(self.value, color.Color):
			return "color.{!r}".format(self.value)
		return repr(self.value)

	def ul4ondump(self, encoder):
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		self.value = decoder.load()

	def __repr__(self):
		return "Const({!r})".format(self.value)


@register("list")
class List(AST):
	"""
	AST nodes for loading a list object.
	"""

	precedence = 11
	fields = AST.fields.union({"items"})

	def __init__(self, *items):
		self.items = list(items)

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, repr(self.items)[1:-1])

	def format(self, indent):
		return "[{}]".format(", ".join(item.format(indent) for item in self.items))

	def formatpython(self, indent):
		return "[{}]".format(", ".join(item.formatpython(indent) for item in self.items))

	def ul4ondump(self, encoder):
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		self.items = decoder.load()


@register("listcomp")
class ListComp(AST):
	"""
	AST node for list comprehension.
	"""

	precedence = 11
	fields = AST.fields.union({"item", "varname", "container", "condition"})

	def __init__(self, item=None, varname=None, container=None, condition=None):
		super().__init__()
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.item, self.varname, self.container, self.condition)

	def format(self, indent):
		s = "[{} for {} in".format(self.item.format(indent), _formatnestednameul4(self.varname), self.container.format(indent))
		if self.condition is not None:
			s += " if {}".format(self.condition.format(indent))
		s += "]"
		return s

	def formatpython(self, indent):
		s = "[{} for {} in {}".format(self.item.formatpython(indent), _formatnestednamepython(self.varname), self.container.formatpython(indent))
		if self.condition is not None:
			s += " if {}".format(self.condition.formatpython(indent))
		s += "]"
		return s

	def ul4ondump(self, encoder):
		encoder.dump(self.item)
		encoder.dump(self.varname)
		encoder.dump(self.container)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		self.item = decoder.load()
		self.varname = decoder.load()
		self.container = decoder.load()
		self.condition = decoder.load()


@register("dict")
class Dict(AST):
	"""
	AST node for loading a dict object.
	"""

	precedence = 11
	fields = AST.fields.union({"items"})

	def __init__(self, *items):
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
				v.append("({},)".format(item[0].formatpython(indent)))
			else:
				v.append("({}, {})".format(item[0].formatpython(indent), item[1].formatpython(indent)))
		return "ul4c._makedict({})".format(", ".join(v))

	def ul4ondump(self, encoder):
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		self.items = [tuple(item) for item in decoder.load()]


@register("dictcomp")
class DictComp(AST):
	"""
	AST node for dictionary comprehension.
	"""

	precedence = 11
	fields = AST.fields.union({"key", "value", "varname", "container", "condition"})

	def __init__(self, key=None, value=None, varname=None, container=None, condition=None):
		self.key = key
		self.value = value
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.key, self.value, self.varname, self.container, self.condition)

	def format(self, indent):
		s = "{{{} : {} for {} in {}".format(self.key.format(indent), self.value.format(indent), _formatnestednameul4(self.varname), self.container.format(indent))
		if self.condition is not None:
			s += " if {}".format(self.condition.format(indent))
		s += "}"
		return s

	def formatpython(self, indent):
		s = "{{{} : {} for {} in {}".format(self.key.formatpython(indent), self.value.formatpython(indent), _formatnestednamepython(self.varname), self.container.formatpython(indent))
		if self.condition is not None:
			s += " if {}".format(self.condition.formatpython(indent))
		s += "}"
		return s

	def ul4ondump(self, encoder):
		encoder.dump(self.key)
		encoder.dump(self.value)
		encoder.dump(self.varname)
		encoder.dump(self.container)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		self.key = decoder.load()
		self.value = decoder.load()
		self.varname = decoder.load()
		self.container = decoder.load()
		self.condition = decoder.load()


@register("genexpr")
class GenExpr(AST):
	"""
	AST node for a generator expression.
	"""

	precedence = 11
	fields = AST.fields.union({"item", "varname", "container", "condition"})

	def __init__(self, item=None, varname=None, container=None, condition=None):
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.item, self.varname, self.container, self.condition)

	def format(self, indent):
		s = "({} for {} in {}".format(self.item.format(indent), _formatnestednameul4(self.varname), self.container.format(indent))
		if self.condition is not None:
			s += " if {}".format(self.condition.format(indent))
		s += ")"
		return s

	def formatpython(self, indent):
		s = "({} for {} in {}".format(self.item.formatpython(indent), _formatnestednamepython(self.varname), self.container.formatpython(indent))
		if self.condition is not None:
			s += " if {}".format(self.condition.formatpython(indent))
		s += ")"
		return s

	def ul4ondump(self, encoder):
		encoder.dump(self.item)
		encoder.dump(self.varname)
		encoder.dump(self.container)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		self.item = decoder.load()
		self.varname = decoder.load()
		self.container = decoder.load()
		self.condition = decoder.load()


@register("var")
class Var(AST):
	"""
	AST nodes for loading a variable.
	"""

	precedence = 11
	fields = AST.fields.union({"name"})

	def __init__(self, name=None):
		self.name = name

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.name)

	def format(self, indent):
		return self.name

	def formatpython(self, indent):
		return "ul4c._getitem(vars, {!r})".format(self.name)

	def ul4ondump(self, encoder):
		encoder.dump(self.name)

	def ul4onload(self, decoder):
		self.name = decoder.load()


class Block(Tag):
	"""
	Base class for all AST nodes that are blocks.

	A block contains a sequence of tags that are executed sequencially.
	A block may execute its content zero (e.g. an ``<?if?>`` block) or more times
	(e.g. a ``<?for?>`` block).
	"""

	fields = Tag.fields.union({"endlocation", "content"})

	def __init__(self, location=None):
		super().__init__(location)
		self.endlocation = None
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

	def _add2template(self, template):
		super()._add2template(template)
		for node in self.content:
			node._add2template(template)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.endlocation)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.endlocation = decoder.load()
		self.content = decoder.load()


@register("ieie")
class IfElIfElse(Block):
	"""
	AST node for an conditional block.

	The content of the :class:`IfElIfElse` block is one :class:`If` block
	followed by zero or more :class:`ElIf` blocks followed by zero or one
	:class:`Else` block.
	"""
	def __init__(self, location=None, condition=None):
		super().__init__(location)
		if condition is not None:
			self.newblock(If(location, condition))

	def append(self, item):
		self.content[-1].append(item)

	def newblock(self, block):
		if self.content:
			self.content[-1].endlocation = block.location
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


@register("if")
class If(Block):
	"""
	AST node for an ``<?if?>`` block.
	"""

	fields = Block.fields.union({"condition"})

	def __init__(self, location=None, condition=None):
		super().__init__(location)
		self.condition = condition

	def format(self, indent):
		return "{}if {}\n{}".format(indent*"\t", self.condition.format(indent), super().format(indent))

	def formatpython(self, indent):
		v = ["{i}# <?if?> tag at position {l.starttag}:{l.endtag} ({id})\n".format(i=indent*"\t", id=id(self), l=self.location)]
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


@register("elif")
class ElIf(Block):
	"""
	AST node for an ``<?elif?>`` block.
	"""

	fields = Block.fields.union({"condition"})

	def __init__(self, location=None, condition=None):
		super().__init__(location)
		self.condition = condition

	def format(self, indent):
		return "{}elif {}\n{}".format(indent*"\t", self.condition.format(indent), super().format(indent))

	def formatpython(self, indent):
		v = ["{i}# <?elif?> tag at position {l.starttag}:{l.endtag} ({id})\n".format(i=indent*"\t", id=id(self), l=self.location)]
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


@register("else")
class Else(Block):
	"""
	AST node for an ``<?else?>`` block.
	"""

	def format(self, indent):
		return "{}else\n{}".format(indent*"\t", super().format(indent))

	def formatpython(self, indent):
		v = ["{i}# <?else?> tag at position {l.starttag}:{l.endtag} ({id})\n".format(i=indent*"\t", id=id(self), l=self.location)]
		v.append("{}else:\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)


@register("for")
class For(Block):
	"""
	AST node for a ``<?for?>`` loop variable.
	"""

	fields = Block.fields.union({"varname", "container"})

	def __init__(self, location=None, varname=None, container=None):
		super().__init__(location)
		self.varname = varname
		self.container = container

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.varname)
		encoder.dump(self.container)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.varname = decoder.load()
		self.container = decoder.load()

	def format(self, indent):
		return "{}for {} in {}\n{}".format(indent*"\t", _formatnestednameul4(self.varname), self.container.format(indent), super().format(indent))

	def formatpython(self, indent):
		v = ["{i}# <?for?> tag at position {l.starttag}:{l.endtag} ({id})\n".format(i=indent*"\t", id=id(self), l=self.location)]
		v.append("{}for {} in {}:\n".format(indent*"\t", _formatnestednamepython(self.varname), self.container.formatpython(indent)))
		indent += 1
		if self.content:
			for node in self.content:
				v.append(node.formatpython(indent))
		else:
			# Make sure we have a proper loop body
			v.append("{}pass\n".format(indent*"\t"))
		return "".join(v)


@register("break")
class Break(Tag):
	"""
	AST node for a ``<?break?>`` inside a ``<?for?>`` block.
	"""

	def format(self, indent):
		return "{}break\n".format(indent*"\t")

	def formatpython(self, indent):
		return "{i}# <?break?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}break\n".format(i=indent*"\t", id=id(self), l=self.location)


@register("continue")
class Continue(Tag):
	"""
	AST node for a ``<?continue?>`` inside a ``<?for?>`` block.
	"""

	def format(self, indent):
		return "{}continue\n".format(indent*"\t")

	def formatpython(self, indent):
		return "{i}# <?continue?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}continue\n".format(i=indent*"\t", id=id(self), l=self.location)


@register("getattr")
class GetAttr(AST):
	"""
	AST node for getting an attribute from an object.

	The object is loaded from the AST node :var:`obj` and the attribute name
	is stored in the string :var:`attrname`.
	"""
	precedence = 9
	associative = False
	fields = AST.fields.union({"obj", "attrname"})

	def __init__(self, obj=None, attrname=None):
		self.obj = obj
		self.attrname = attrname

	def __repr__(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.obj, self.attrname)

	def format(self, indent):
		return "{}.{}".format(self._formatop(self.obj), self.attrname)

	def formatpython(self, indent):
		return "ul4c._getitem({}, {!r})".format(self.obj.formatpython(indent), self.attrname)

	def ul4ondump(self, encoder):
		encoder.dump(self.obj)
		encoder.dump(self.attrname)

	def ul4onload(self, decoder):
		self.obj = decoder.load()
		self.attrname = decoder.load()


@register("getslice")
class GetSlice(AST):
	"""
	AST node for getting a slice from a list or string object.

	The object is loaded from the AST node :var:`obj` and the start and stop
	indices from the AST node :var:`index1` and :var:`index2`. :var:`index1`
	and :var:`index2` may also be :const:`None` (for missing slice indices,
	which default to the 0 for the start index and the length of the sequence
	for the end index).
	"""

	precedence = 8
	associative = False
	fields = AST.fields.union({"obj", "index1", "index2"})

	def __init__(self, obj=None, index1=None, index2=None):
		self.obj = obj
		self.index1 = index1
		self.index2 = index2

	def __repr__(self):
		return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.obj, self.index1, self.index2)

	@classmethod
	def make(cls, obj, index1, index2):
		# We don't have to check for undefined results here, because this can't happen with slices
		if isinstance(obj, Const):
			if index1 is None:
				if index2 is None:
					return Const(obj[:])
				elif isinstance(index2, Const):
					return Const(obj[:index2.value])
			elif isinstance(index1, Const):
				if index2 is None:
					return Const(obj[index1.value:])
				elif isinstance(index2, Const):
					return Const(obj[index1.value:index2.value])
		return cls(obj, index1, index2)

	def format(self, indent):
		return "{}[{}:{}]".format(self._formatop(self.obj), self.index1.format(indent) if self.index1 is not None else "", self.index2.format(indent) if self.index2 is not None else "")

	def formatpython(self, indent):
		return "({})[{}:{}]".format(self.obj.formatpython(indent), self.index1.formatpython(indent) if self.index1 is not None else "", self.index2.formatpython(indent) if self.index2 is not None else "")

	def ul4ondump(self, encoder):
		encoder.dump(self.obj)
		encoder.dump(self.index1)
		encoder.dump(self.index2)

	def ul4onload(self, decoder):
		self.obj = decoder.load()
		self.index1 = decoder.load()
		self.index2 = decoder.load()


class Unary(AST):
	"""
	Base class for all AST nodes implementing unary operators.
	"""

	fields = AST.fields.union({"obj"})

	def __init__(self, obj=None):
		self.obj = obj

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.obj)

	def ul4ondump(self, encoder):
		encoder.dump(self.obj)

	def ul4onload(self, decoder):
		self.obj = decoder.load()

	@classmethod
	def make(cls, obj):
		if isinstance(obj, Const):
			result = cls.evaluate(obj.value)
			if not isinstance(result, Undefined):
				return Const(result)
		return cls(obj)


@register("not")
class Not(Unary):
	"""
	AST node for the unary ``not`` operator.
	"""

	precedence = 2

	@classmethod
	def evaluate(cls, obj):
		return not obj

	def format(self, indent):
		return "not {}".format(self._formatop(self.obj))

	def formatpython(self, indent):
		return "not ({})".format(self.obj.formatpython(indent))


@register("neg")
class Neg(Unary):
	"""
	AST node for the unary negation (i.e. "-") operator.
	"""

	precedence = 7

	@classmethod
	def evaluate(cls, obj):
		return -obj

	def format(self, indent):
		return "-{}".format(self._formatop(self.obj))

	def formatpython(self, indent):
		return "-({})".format(self.obj.formatpython(indent))


class UnaryTag(Tag):
	fields = Tag.fields.union({"obj"})

	def __init__(self, location=None, obj=None):
		super().__init__(location)
		self.obj = obj

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()


@register("print")
class Print(UnaryTag):
	"""
	AST node for a ``<?print?>`` tag.
	"""

	def format(self, indent):
		return "{}print {}\n".format(indent*"\t", self.obj.format(indent))

	def formatpython(self, indent):
		return "{i}# <?print?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}yield self.function_str(vars, {o})\n".format(i=indent*"\t", id=id(self), o=self.obj.formatpython(indent), l=self.location)


@register("printx")
class PrintX(UnaryTag):
	"""
	AST node for a ``<?printx?>`` tag.
	"""

	def format(self, indent):
		return "{}printx {}\n".format(indent*"\t", self.obj.format(indent))

	def formatpython(self, indent):
		return "{i}# <?printx?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}yield ul4c._xmlescape({o})\n".format(i=indent*"\t", id=id(self), o=self.obj.formatpython(indent), l=self.location)


class Binary(AST):
	"""
	Base class for all AST nodes implementing binary operators.
	"""

	fields = AST.fields.union({"obj1", "obj2"})

	def __init__(self, obj1=None, obj2=None):
		self.obj1 = obj1
		self.obj2 = obj2

	def __repr__(self):
		return "{}({!r}, {!r})".format(self.__class__.__name__, self.obj1, self.obj2)

	def ul4ondump(self, encoder):
		encoder.dump(self.obj1)
		encoder.dump(self.obj2)

	def ul4onload(self, decoder):
		self.obj1 = decoder.load()
		self.obj2 = decoder.load()

	@classmethod
	def make(cls, obj1, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const):
			result = cls.evaluate(obj1.value, obj2.value)
			if not isinstance(result, Undefined):
				return Const(result)
		return cls(obj1, obj2)


@register("getitem")
class GetItem(Binary):
	"""
	AST node for subscripting operator.

	The object (which must be a list, string or dict) is loaded from the AST
	node :var:`obj1` and the index/key is loaded from the AST node :var:`obj2`.
	"""

	precedence = 9
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1[obj2]

	def format(self, indent):
		return "{}[{}]".format(self._formatop(self.obj1), self.obj2.format(indent))

	def formatpython(self, indent):
		return "ul4c._getitem({}, {})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("eq")
class EQ(Binary):
	"""
	AST node for the binary ``==`` comparison operator.
	"""

	precedence = 4
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 == obj2

	def format(self, indent):
		return "{} == {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) == ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("ne")
class NE(Binary):
	"""
	AST node for the binary ``!=`` comparison operator.
	"""

	precedence = 4
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 != obj2

	def format(self, indent):
		return "{} != {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) != ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("lt")
class LT(Binary):
	"""
	AST node for the binary ``<`` comparison operator.
	"""

	precedence = 4
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 < obj2

	def format(self, indent):
		return "{} < {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) < ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("le")
class LE(Binary):
	"""
	AST node for the binary ``<=`` comparison operator.
	"""

	precedence = 4
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 <= obj2

	def format(self, indent):
		return "{} <= {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) <= ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("gt")
class GT(Binary):
	"""
	AST node for the binary ``>`` comparison operator.
	"""

	precedence = 4
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 > obj2

	def format(self, indent):
		return "{} > {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) > ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("ge")
class GE(Binary):
	"""
	AST node for the binary ``>=`` comparison operator.
	"""

	precedence = 4
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 >= obj2

	def format(self, indent):
		return "{} >= {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) >= ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("contains")
class Contains(Binary):
	"""
	AST node for the binary containment testing operator.

	The item/key object is loaded from the AST node :var:`obj1` and the container
	object (which must be a list, string or dict) is loaded from the AST node
	:var:`obj2`.
	"""

	precedence = 3
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 in obj2

	def format(self, indent):
		return "{} in {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) in ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("notcontains")
class NotContains(Binary):
	"""
	AST node for the inverted containment testing operator.

	The item/key object is loaded from the AST node :var:`obj1` and the container
	object (which must be a list, string or dict) is loaded from the AST node
	:var:`obj2`.
	"""

	precedence = 3
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 not in obj2

	def format(self, indent):
		return "{} not in {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) not in ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("add")
class Add(Binary):
	"""
	AST node for the binary addition operator.
	"""

	precedence = 5

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 + obj2

	def format(self, indent):
		return "{}+{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) + ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("sub")
class Sub(Binary):
	"""
	AST node for the binary substraction operator.
	"""

	precedence = 5
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 - obj2

	def format(self, indent):
		return "{}-{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) - ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("mul")
class Mul(Binary):
	"""
	AST node for the binary multiplication operator.
	"""

	precedence = 6

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 * obj2

	def format(self, indent):
		return "{}*{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) * ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("floordiv")
class FloorDiv(Binary):
	"""
	AST node for the binary truncating division operator.
	"""

	precedence = 6
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 // obj2

	def format(self, indent):
		return "{}//{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) // ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("truediv")
class TrueDiv(Binary):
	"""
	AST node for the binary true division operator.
	"""

	precedence = 6
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 / obj2

	def format(self, indent):
		return "{}/{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) / ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("and")
class And(Binary):
	"""
	AST node for the binary ``and`` operator.
	"""

	precedence = 1

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 and obj2

	def format(self, indent):
		return "{} and {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) and ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("or")
class Or(Binary):
	"""
	AST node for the binary ``or`` operator.
	"""

	precedence = 0

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 or obj2

	def format(self, indent):
		return "{} or {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) or ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


@register("mod")
class Mod(Binary):
	"""
	AST node for the binary modulo operator.
	"""

	precedence = 6
	associative = False

	@classmethod
	def evaluate(cls, obj1, obj2):
		return obj1 % obj2

	def format(self, indent):
		return "{}%{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) % ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))


class ChangeVar(Tag):
	"""
	Baseclass for all AST nodes that store or modify a variable.

	The variable name is stored in the string :var:`varname` and the value that
	will be stored or be used to modify the stored value is loaded from the
	AST node :var:`value`.
	"""

	fields = Tag.fields.union({"varname", "value"})

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
	"""
	AST node that stores a value into a variable.
	"""

	def format(self, indent):
		return "{}{} = {}\n".format(indent*"\t", _formatnestednameul4(self.varname), self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}{n} = {v}\n".format(i=indent*"\t", id=id(self), n=_formatnestednamepython(self.varname), v=self.value.formatpython(indent), l=self.location)


@register("addvar")
class AddVar(ChangeVar):
	"""
	AST node that adds a value to a variable (i.e. the ``+=`` operator).
	"""

	def format(self, indent):
		return "{}{} += {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] += {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)


@register("subvar")
class SubVar(ChangeVar):
	"""
	AST node that substracts a value from a variable (i.e. the ``-=`` operator).
	"""

	def format(self, indent):
		return "{}{} -= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] -= {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)


@register("mulvar")
class MulVar(ChangeVar):
	"""
	AST node that multiplies a variable by a value (i.e. the ``*=`` operator).
	"""

	def format(self, indent):
		return "{}{} *= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] *= {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)


@register("floordivvar")
class FloorDivVar(ChangeVar):
	"""
	AST node that divides a variable by a value (truncating to an integer value;
	i.e. the ``//=`` operator).
	"""

	def format(self, indent):
		return "{}{} //= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] //= {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)


@register("truedivvar")
class TrueDivVar(ChangeVar):
	"""
	AST node that divides a variable by a value (i.e. the ``/=`` operator).
	"""

	def format(self, indent):
		return "{}{} /= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] /= {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)


@register("modvar")
class ModVar(ChangeVar):
	"""
	AST node for the ``%=`` operator.
	"""

	def format(self, indent):
		return "{}{} %= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] %= {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)


@register("callfunc")
class CallFunc(AST):
	"""
	AST node for calling a function.

	The function name is stored in the string :var:`funcname`. The list of
	positional arguments is loaded from the list of AST nodes :var:`args`.
	Keyword arguments are in :var:`kwargs`. `var`:remargs` is the AST node
	for the ``*`` argument (and may by ``None`` if there is no ``*`` argument).
	`var`:remkwargs` is the AST node for the ``**`` argument (and may by ``None``
	if there is no ``**`` argument)
	"""

	precedence = 10
	associative = False
	fields = AST.fields.union({"funcname", "args", "kwargs", "remargs", "remkwargs"})

	def __init__(self, funcname=None):
		self.funcname = funcname
		self.args = []
		self.kwargs = []
		self.remargs = None
		self.remkwargs = None

	def __repr__(self):
		args = [
			(repr(self.funcname),),
			(repr(arg) for arg in self.args),
			("{}={!r}".format(argname, argvalue) for (argname, argvalue) in self.kwargs)
		]
		if self.remargs is not None:
			args.append(("*{}".format(repr(self.remargs)),))
		if self.remkwargs is not None:
			args.append(("**{}".format(repr(self.remkwargs)),))
		return "{}({})".format(self.__class__.__name__, ", ".join(itertools.chain(args)))

	def format(self, indent):
		args = []
		for arg in self.args:
			s = arg.format(indent)
			if isinstance(arg, GenExpr):
				s = s[1:-1]
			args.append(s)
		for (argname, argvalue) in self.kwargs:
			s = argvalue.format(indent)
			if isinstance(arg, GenExpr):
				s = s[1:-1]
			args.append("{}={}".format(argname, s))
		if self.remargs is not None:
			args.append("*{}".format(self.remargs.format(indent)))
		if self.remkwargs is not None:
			args.append("**{}".format(self.remkwargs.format(indent)))
		return "{}({})".format(self.funcname, ", ".join(args))

	def formatpython(self, indent):
		args = []
		for arg in self.args:
			args.append(arg.formatpython(indent))
		for (argname, argvalue) in self.kwargs:
			args.append("{}={}".format(argname, argvalue.formatpython(indent)))
		if self.remargs is not None:
			args.append("*{}".format(self.remargs.formatpython(indent)))
		if self.remkwargs is not None:
			args.append("**{}".format(self.remkwargs.formatpython(indent)))
		return "stack[0].function_{}(vars, {})".format(self.funcname, ", ".join(args))

	def ul4ondump(self, encoder):
		encoder.dump(self.funcname)
		encoder.dump(self.args)
		encoder.dump(self.kwargs)
		encoder.dump(self.remargs)
		encoder.dump(self.remkwargs)

	def ul4onload(self, decoder):
		self.funcname = decoder.load()
		self.args = decoder.load()
		self.kwargs = [tuple(arg) for arg in decoder.load()]
		self.remargs = decoder.load()
		self.remkwargs = decoder.load()


@register("callmeth")
class CallMeth(AST):
	"""
	AST node for calling a method.

	The method name is stored in the string :var:`methname`. The object for which
	the method will be called is loaded from the AST node :var:`obj` and the list
	of arguments is loaded from the list of AST nodes :var:`args`. Keyword
	arguments are in :var:`kwargs`. `var`:remargs` is the AST node for the ``*``
	argument (and may by ``None`` if there is no ``*`` argument).
	`var`:remkwargs` is the AST node for the ``**`` argument (and may by ``None``
	if there is no ``**`` argument)

	"""

	precedence = 9
	associative = False
	fields = AST.fields.union({"methname", "obj", "args"})

	def __init__(self, methname=None, obj=None):
		self.methname = methname
		self.obj = obj
		self.args = []
		self.kwargs = []
		self.remargs = None
		self.remkwargs = None

	def __repr__(self):
		args = [
			(repr(self.methname), repr(self.obj)),
			(repr(arg) for arg in self.args),
			("{}={!r}".format(argname, argvalue) for (argname, argvalue) in self.kwargs)
		]
		if self.remargs is not None:
			args.append(("*{}".format(repr(self.remargs)),))
		if self.remkwargs is not None:
			args.append(("**{}".format(repr(self.remkwargs)),))
		return "{}({})".format(self.__class__.__name__, ", ".join(itertools.chain(args)))

	def format(self, indent):
		args = []
		if len(self.args) == 1 and isinstance(self.args[0], GenExpr) and not self.kwargs and self.remargs is None and self.remkwargs is None:
			args.append(self.args[0].format(indent)[1:-1])
		else:
			for arg in self.args:
				args.append(arg.format(indent))
			for (argname, argvalue) in self.kwargs:
				args.append("{}={}".format(argname, argvalue.format(indent)))
			if self.remargs is not None:
				args.append("*{}".format(self.remargs.format(indent)))
			if self.remkwargs is not None:
				args.append("**{}".format(self.remkwargs.format(indent)))
		return "({}).{}({})".format(self._formatop(self.obj), self.methname, ", ".join(args))

	def formatpython(self, indent):
		args = []
		for arg in self.args:
			args.append(arg.formatpython(indent))
		for (argname, argvalue) in self.kwargs:
			args.append("{}={}".format(argname, argvalue.formatpython(indent)))
		if self.remargs is not None:
			args.append("*{}".format(self.remargs.formatpython(indent)))
		if self.remkwargs is not None:
			args.append("**{}".format(self.remkwargs.formatpython(indent)))
		return "stack[0].method_{}(stack, {}, {})".format(self.methname, self.obj.formatpython(indent), ", ".join(args))

	def ul4ondump(self, encoder):
		encoder.dump(self.methname)
		encoder.dump(self.obj)
		encoder.dump(self.args)
		encoder.dump(self.kwargs)
		encoder.dump(self.remargs)
		encoder.dump(self.remkwargs)

	def ul4onload(self, decoder):
		self.methname = decoder.load()
		self.obj = decoder.load()
		self.args = decoder.load()
		self.kwargs = [tuple(arg) for arg in decoder.load()]
		self.remargs = decoder.load()
		self.remkwargs = decoder.load()


@register("render")
class Render(UnaryTag):
	"""
	AST node for the ``<?render?>`` tag.
	"""

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.obj)

	def format(self, indent):
		return "{}render {}\n".format(indent*"\t", self.obj.format(indent))

	def formatpython(self, indent):
		if isinstance(self.obj, CallMeth) and self.obj.methname == "render":
			code = "yield from {}".format(self.obj.formatpython(indent))
		else:
			code = "yield self.function_str(vars, {})".format(self.obj.formatpython(indent))
		return "{i}# <?render?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}{c}\n".format(i=indent*"\t", id=id(self), c=code, l=self.location)


class Callable(object):
	"""
	Base class that implements all UL4 functions as methods.
	"""

	def __getattr__(self, name):
		if name.startswith("function_"):
			raise UnknownFunctionError(name[9:])
		elif name.startswith("method_"):
			raise UnknownMethodError(name[7:])
		else:
			raise AttributeError(name)

	@classmethod
	def function_vars(cls, vars):
		return vars

	@classmethod
	def function_get(cls, vars, name, default=None):
		return vars.get(name, default)

	@classmethod
	def function_now(cls, vars):
		return datetime.datetime.now()

	@classmethod
	def function_utcnow(cls, vars):
		return datetime.datetime.utcnow()

	@classmethod
	def function_date(cls, vars, year, month, day, hour=0, minute=0, second=0, microsecond=0):
		return datetime.datetime(year, month, day, hour, minute, second, microsecond)

	@classmethod
	def function_timedelta(cls, vars, days=0, seconds=0, microseconds=0):
		return datetime.timedelta(days, seconds, microseconds)

	@classmethod
	def function_monthdelta(cls, vars, months=0):
		return misc.monthdelta(months)

	@classmethod
	def function_random(cls, vars, ):
		return random.random()

	@classmethod
	def function_xmlescape(cls, vars, obj):
		if obj is None:
			return ""
		elif isinstance(obj, Undefined):
			return ""
		else:
			return misc.xmlescape(str(obj))

	@classmethod
	def function_csv(cls, vars, obj):
		if obj is None:
			return ""
		elif isinstance(obj, Undefined):
			return ""
		elif not isinstance(obj, str):
			obj = cls.function_repr(vars, obj)
		if any(c in obj for c in ',"\n'):
			return '"{}"'.format(obj.replace('"', '""'))
		return obj

	@classmethod
	def function_asjson(cls, vars, obj):
		if obj is None:
			return "null"
		elif isinstance(obj, Undefined):
			return "{}.undefined"
		if isinstance(obj, (bool, int, float, str)):
			return json.dumps(obj)
		elif isinstance(obj, datetime.datetime):
			return "new Date({}, {}, {}, {}, {}, {}, {})".format(obj.year, obj.month-1, obj.day, obj.hour, obj.minute, obj.second, obj.microsecond//1000)
		elif isinstance(obj, datetime.date):
			return "new Date({}, {}, {})".format(obj.year, obj.month-1, obj.day)
		elif isinstance(obj, datetime.timedelta):
			return "ul4.TimeDelta.create({}, {}, {})".format(obj.days, obj.seconds, obj.microseconds)
		elif isinstance(obj, misc.monthdelta):
			return "ul4.MonthDelta.create({})".format(obj.months)
		elif isinstance(obj, color.Color):
			return "ul4.Color.create({}, {}, {}, {})".format(*obj)
		elif isinstance(obj, collections.Mapping):
			return "{{{}}}".format(", ".join("{}: {}".format(cls.function_asjson(vars, key), cls.function_asjson(vars, value)) for (key, value) in obj.items()))
		elif isinstance(obj, collections.Sequence):
			return "[{}]".format(", ".join(cls.function_asjson(vars, item) for item in obj))
		elif isinstance(obj, Template):
			return obj.jssource()
		else:
			raise TypeError("can't handle object of type {}".format(type(obj)))

	@classmethod
	def function_fromjson(cls, vars, string):
		return json.loads(string)

	@classmethod
	def function_asul4on(cls, vars, obj):
		from ll import ul4on
		return ul4on.dumps(obj)

	@classmethod
	def function_fromul4on(cls, vars, string):
		from ll import ul4on
		return ul4on.loads(string)

	@classmethod
	def function_str(cls, vars, obj=""):
		if obj is None:
			return ""
		elif isinstance(obj, Undefined):
			return ""
		else:
			return str(obj)

	@classmethod
	def function_int(cls, vars, obj=0, base=None):
		if base is None:
			return int(obj)
		else:
			return int(obj, base)

	@classmethod
	def function_float(cls, vars, obj=0.0):
		return float(obj)

	@classmethod
	def function_bool(cls, vars, obj=False):
		return bool(obj)

	@classmethod
	def function_len(cls, vars, sequence):
		return len(sequence)

	@classmethod
	def function_abs(cls, vars, number):
		return abs(number)

	@classmethod
	def function_any(cls, vars, iterable):
		return any(iterable)

	@classmethod
	def function_all(cls, vars, iterable):
		return all(iterable)

	@classmethod
	def function_enumerate(cls, vars, iterable, start=0):
		return enumerate(iterable, start)

	@classmethod
	def function_enumfl(cls, vars, iterable, start=0):
		lastitem = None
		first = True
		i = start
		it = iter(iterable)
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

	@classmethod
	def function_isfirstlast(cls, vars, iterable):
		lastitem = None
		first = True
		it = iter(iterable)
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

	@classmethod
	def function_isfirst(cls, vars, iterable):
		first = True
		for item in iterable:
			yield (first, item)
			first = False

	@classmethod
	def function_islast(cls, vars, iterable):
		lastitem = None
		it = iter(iterable)
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

	@classmethod
	def function_isundefined(cls, vars, obj):
		return isinstance(obj, Undefined)

	@classmethod
	def function_isdefined(cls, vars, obj):
		return not isinstance(obj, Undefined)

	@classmethod
	def function_isnone(cls, vars, obj):
		return obj is None

	@classmethod
	def function_isstr(cls, vars, obj):
		return isinstance(obj, str)

	@classmethod
	def function_isint(cls, vars, obj):
		return isinstance(obj, int) and not isinstance(obj, bool)

	@classmethod
	def function_isfloat(cls, vars, obj):
		return isinstance(obj, float)

	@classmethod
	def function_isbool(cls, vars, obj):
		return isinstance(obj, bool)

	@classmethod
	def function_isdate(cls, vars, obj):
		return isinstance(obj, (datetime.datetime, datetime.date))

	@classmethod
	def function_istimedelta(cls, vars, obj):
		return isinstance(obj, datetime.timedelta)

	@classmethod
	def function_ismonthdelta(cls, vars, obj):
		return isinstance(obj, misc.monthdelta)

	@classmethod
	def function_islist(cls, vars, obj):
		return isinstance(obj, collections.Sequence) and not isinstance(obj, str) and not isinstance(obj, color.Color)

	@classmethod
	def function_isdict(cls, vars, obj):
		return isinstance(obj, collections.Mapping) and not isinstance(obj, Template)

	@classmethod
	def function_iscolor(cls, vars, obj):
		return isinstance(obj, color.Color)

	@classmethod
	def function_istemplate(cls, vars, obj):
		return isinstance(obj, (Template, TemplateClosure))

	@classmethod
	def function_repr(cls, vars, obj):
		if isinstance(obj, str):
			return repr(obj)
		elif isinstance(obj, datetime.datetime):
			s = str(obj.isoformat())
			if s.endswith("T00:00:00"):
				s = s[:-9]
			return "@({})".format(s)
		elif isinstance(obj, datetime.date):
			return "@({})".format(obj.isoformat())
		elif isinstance(obj, datetime.timedelta):
			return repr(obj).partition(".")[-1]
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
			return "[{}]".format(", ".join(cls.function_repr(vars, item) for item in obj))
		elif isinstance(obj, collections.Mapping):
			return "{{{}}}".format(", ".join("{}: {}".format(cls.function_repr(vars, key), cls.function_repr(vars, value)) for (key, value) in obj.items()))
		else:
			return repr(obj)


	@classmethod
	def function_chr(cls, vars, i):
		return chr(i)

	@classmethod
	def function_ord(cls, vars, c):
		return ord(c)

	@classmethod
	def function_hex(cls, vars, number):
		return hex(number)

	@classmethod
	def function_oct(cls, vars, number):
		return oct(number)

	@classmethod
	def function_bin(cls, vars, number):
		return bin(number)

	@classmethod
	def function_min(cls, vars, *args):
		return min(*args)

	@classmethod
	def function_max(cls, vars, *args):
		return max(*args)

	@classmethod
	def function_sorted(cls, vars, iterable):
		return sorted(iterable)

	@classmethod
	def function_range(cls, vars, *args):
		return range(*args)

	@classmethod
	def function_type(cls, vars, obj):
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
		elif isinstance(obj, datetime.timedelta):
			return "timedelta"
		elif isinstance(obj, misc.monthdelta):
			return "monthdelta"
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


	@classmethod
	def function_reversed(cls, vars, sequence):
		return reversed(sequence)

	@classmethod
	def function_randrange(cls, vars, *args):
		return random.randrange(*args)

	@classmethod
	def function_randchoice(cls, vars, sequence):
		return random.choice(sequence)

	@classmethod
	def function_format(cls, vars, obj, fmt, lang=None):
		if isinstance(obj, (datetime.date, datetime.time, datetime.timedelta)):
			if lang is None:
				lang = "en"
			oldlocale = locale.getlocale()
			try:
				for candidate in (locale.normalize(lang), locale.normalize("en"), ""):
					try:
						locale.setlocale(locale.LC_ALL, candidate)
						return format(obj, fmt)
					except locale.Error:
						if not candidate:
							return format(obj, fmt)
			finally:
				try:
					locale.setlocale(locale.LC_ALL, oldlocale)
				except locale.Error:
					pass
		else:
			return format(obj, fmt)


	@classmethod
	def function_zip(cls, vars, *iterables):
		return zip(*iterables)

	@classmethod
	def function_urlquote(cls, vars, string):
		return urlparse.quote_plus(string)

	@classmethod
	def function_urlunquote(cls, vars, string):
		return urlparse.unquote_plus(string)

	@classmethod
	def function_rgb(cls, vars, r, g, b, a=1.0):
		return color.Color.fromrgb(r, g, b, a)

	@classmethod
	def function_hls(cls, vars, h, l, s, a=1.0):
		return color.Color.fromhls(h, l, s, a)

	@classmethod
	def function_hsv(cls, vars, h, s, v, a=1.0):
		return color.Color.fromhsv(h, s, v, a)

	@classmethod
	def method_split(cls, stack, obj, sep=None, count=None):
		return obj.split(sep, count if count is not None else -1)

	@classmethod
	def method_rsplit(cls, stack, obj, sep=None, count=None):
		return obj.rsplit(sep, count if count is not None else -1)

	@classmethod
	def method_strip(cls, stack, obj, chars=None):
		return obj.strip(chars)

	@classmethod
	def method_lstrip(cls, stack, obj, chars=None):
		return obj.lstrip(chars)

	@classmethod
	def method_rstrip(cls, stack, obj, chars=None):
		return obj.rstrip(chars)

	@classmethod
	def method_find(cls, stack, obj, sub, start=None, end=None):
		if isinstance(obj, str):
			return obj.find(sub, start, end)
		else:
			try:
				if end is None:
					if start is None:
						return obj.index(sub)
					return obj.index(sub, start)
				return obj.index(sub, start, end)
			except ValueError:
				return -1

	@classmethod
	def method_rfind(cls, stack, obj, sub, start=None, end=None):
		if isinstance(obj, str):
			return obj.rfind(sub, start, end)
		else:
			for i in reversed(range(*slice(start, end).indices(len(obj)))):
				if obj[i] == sub:
					return i
			return -1

	@classmethod
	def method_startswith(cls, stack, obj, prefix):
		return obj.startswith(prefix)

	@classmethod
	def method_endswith(cls, stack, obj, suffix):
		return obj.endswith(suffix)

	@classmethod
	def method_upper(cls, stack, obj):
		return obj.upper()

	@classmethod
	def method_lower(cls, stack, obj):
		return obj.lower()

	@classmethod
	def method_capitalize(cls, stack, obj):
		return obj.capitalize()

	@classmethod
	def method_replace(cls, stack, obj, old, new, count=None):
		if count is None:
			return obj.replace(old, new)
		else:
			return obj.replace(old, new, count)

	@classmethod
	def method_r(cls, stack, obj):
		return obj.r()

	@classmethod
	def method_g(cls, stack, obj):
		return obj.g()

	@classmethod
	def method_b(cls, stack, obj):
		return obj.b()

	@classmethod
	def method_a(cls, stack, obj):
		return obj.a()

	@classmethod
	def method_hls(cls, stack, obj):
		return obj.hls()

	@classmethod
	def method_hlsa(cls, stack, obj):
		return obj.hlsa()

	@classmethod
	def method_hsv(cls, stack, obj):
		return obj.hsv()

	@classmethod
	def method_hsva(cls, stack, obj):
		return obj.hsva()

	@classmethod
	def method_lum(cls, stack, obj):
		return obj.lum()

	@classmethod
	def method_weekday(cls, stack, obj):
		return obj.weekday()

	@classmethod
	def method_week(cls, stack, obj, firstweekday=None):
		if firstweekday is None:
			firstweekday = 0
		else:
			firstweekday %= 7
		jan1 = obj.__class__(obj.year, 1, 1)
		yearday = (obj - jan1).days+7
		jan1weekday = jan1.weekday()
		while jan1weekday != firstweekday:
			yearday -= 1
			jan1weekday += 1
			if jan1weekday == 7:
				jan1weekday = 0
		return yearday//7

	@classmethod
	def method_items(cls, stack, obj):
		return obj.items()

	@classmethod
	def method_values(cls, stack, obj):
		return obj.values()

	@classmethod
	def method_join(cls, stack, obj, iterable):
		return obj.join(iterable)

	@classmethod
	def method_render(cls, stack, obj, **vars):
		return obj._render(stack, vars)

	@classmethod
	def method_renders(cls, stack, obj, **vars):
		return "".join(obj._render(stack, vars))

	@classmethod
	def method_mimeformat(cls, stack, obj):
		weekdayname = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
		monthname = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
		return "{1}, {0.day:02d} {2:3} {0.year:4} {0.hour:02}:{0.minute:02}:{0.second:02} GMT".format(obj, weekdayname[obj.weekday()], monthname[obj.month])

	@classmethod
	def method_isoformat(cls, stack, obj):
		result = obj.isoformat()
		suffix = "T00:00:00"
		if result.endswith(suffix):
			return result[:-len(suffix)]
		return result

	@classmethod
	def method_yearday(cls, stack, obj):
		return (obj - obj.__class__(obj.year, 1, 1)).days+1

	@classmethod
	def method_get(cls, stack, obj, key, default=None):
		return obj.get(key, default)

	@classmethod
	def method_withlum(cls, stack, obj, lum):
		return obj.withlum(lum)

	@classmethod
	def method_witha(cls, stack, obj, a):
		return obj.witha(a)

	@classmethod
	def method_day(cls, stack, obj):
		return obj.day

	@classmethod
	def method_month(cls, stack, obj):
		return obj.month

	@classmethod
	def method_year(cls, stack, obj):
		return obj.year

	@classmethod
	def method_hour(cls, stack, obj):
		return obj.hour

	@classmethod
	def method_minute(cls, stack, obj):
		return obj.minute

	@classmethod
	def method_second(cls, stack, obj):
		return obj.second

	@classmethod
	def method_microsecond(cls, stack, obj):
		return obj.microsecond


@register("template")
class Template(Block, Callable):
	"""
	A template object is normally created by passing the template source to the
	constructor. It can also be loaded from the compiled format via the class
	methods :meth:`load` (from a stream) or :meth:`loads` (from a string).

	The compiled format can be generated with the methods :meth:`dump` (which
	dumps the format to a stream) or :meth:`dumps` (which returns a string with
	the compiled format).

	Rendering the template can be done with the methods :meth:`render` (which
	is a generator) or :meth:`renders` (which returns a string).

	A :class:`Template` object is itself an AST node. Evaluating it will store
	the template object under its name in the local variables.
	"""
	version = "22"
	fields = Block.fields.union({"source", "name", "startdelim", "enddelim", "endlocation"})

	def __init__(self, source=None, name=None, startdelim="<?", enddelim="?>"):
		"""
		Create a :class:`Template` object. If :var:`source` is ``None``, the
		:class:`Template` remains uninitialized, otherwise :var:`source` will be
		compiled (using :var:`startdelim` and :var:`enddelim` as the tag
		delimiters). :var:`name` is the name of the template. It will be used in
		exception messages and should be a valid Python identifier.

		"""
		# ``location``/``endlocation`` will remain ``None`` for a top level template
		# For a subtemplate ``location`` will be set to the location of the ``<?def?>`` tag in :meth:`_compile` and ``endlocation`` will be the location of the ``<?end def?>`` tag
		super().__init__(None)
		self.startdelim = startdelim
		self.enddelim = enddelim
		self.name = name
		self.source = None

		# The following attributes (``_astsbyid``, ``_pythonsource`` and ``_pythonfunction``)
		# are used for converting the AST back to executable Python code
		# They will be initialized when required

		# ``_astsbyid`` maps the id of the AST node to the ast node itself
		# It is used in :meth:`Template.format` (to give the generated Python source code access to the subtemplate)
		# and for proper exception chaining (when an exception occurs in the template, comments in the
		# generated source code allow finding the offending AST node)
		self._astsbyid = None
		# Python source code generated for the template
		self._pythonsource = None
		# A compiled Python function implementing the template logic
		self._pythonfunction = None

		# If we have source code compile it
		if source is not None:
			self._compile(source, name, startdelim, enddelim)

	def ul4ondump(self, encoder):
		encoder.dump(self.version)
		encoder.dump(self.source)
		encoder.dump(self.name)
		encoder.dump(self.startdelim)
		encoder.dump(self.enddelim)
		encoder.dump(self.location)
		encoder.dump(self.endlocation)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		version = decoder.load()
		if version != self.version:
			raise ValueError("invalid version, expected {!r}, got {!r}".format(self.version, version))
		self.source = decoder.load()
		self.name = decoder.load()
		self.startdelim = decoder.load()
		self.enddelim = decoder.load()
		self.location = decoder.load()
		self.endlocation = decoder.load()
		self.content = decoder.load()

	@classmethod
	def loads(cls, data):
		"""
		The class method :meth:`loads` loads the template from string :var:`data`.
		:var:`data` must contain the template in compiled format.
		"""
		from ll import ul4on
		return ul4on.loads(data)

	@classmethod
	def load(cls, stream):
		"""
		The class method :meth:`load` loads the template from the stream
		:var:`stream`. The stream must contain the template in compiled format.
		"""
		from ll import ul4on
		return ul4on.load(stream)

	def dump(self, stream):
		"""
		:meth:`dump` dumps the template in compiled format to the stream
		:var:`stream`.
		"""
		from ll import ul4on
		ul4on.dump(self, stream)

	def dumps(self):
		"""
		:meth:`dumps` returns the template in compiled format (as a string).
		"""
		from ll import ul4on
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
		return "{i}# <?def?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] = ul4c.TemplateClosure(stack[-1]._getast({id}), vars)\n".format(i=indent*"\t", n=self.name if self.name is not None else "unnamed", id=id(self), l=self.location)

	def _getast(self, astid):
		if self._astsbyid is None:
			self._astsbyid = {}
			self._add2template(self)
		return self._astsbyid[astid]

	def _handleexc(self, exc):
		source = [line.strip() for line in self._pythonsource.splitlines()]
		lineno = exc.__traceback__.tb_lineno-1
		for line in reversed(source[:lineno]):
			if line.startswith("#"):
				ast = self._getast(int(line.rpartition(" ")[2][1:-1])) # extract the id from the comment and fetch the appropriate node
				break
		else:
			raise # shouldn't happen -> reraise original
		if ast.location is None:
			raise # shouldn't happen, as a ``<?def?>`` tag itself can't result in any exceptions -> reraise original
		else:
			raise Error(ast.location) from exc

	def _render(self, stack, vars):
		return self.pythonfunction()(self, stack, vars)

	def render(self, **vars):
		"""
		Render the template iteratively (i.e. this is a generator).
		:var:`vars` contains the top level variables available to the
		template code.
		"""
		stack = []
		vars = collections.ChainMap(vars, {'stack': stack})
		return self._render(stack, vars)

	def renders(self, **vars):
		"""
		Render the template as a string. :var:`vars` contains the top level
		variables available to the template code.
		"""
		return "".join(self.render(**vars))

	def pythonfunction(self):
		"""
		Return a Python generator that can be called to render the template. The
		argument signature of the function will be ``**vars``.
		"""
		if self._pythonfunction is None:
			name = self.name if self.name is not None else "unnamed"
			source = self.pythonsource()
			ns = {}
			exec(source, ns)
			self._pythonfunction = ns[name]
		return self._pythonfunction

	def __call__(self, **vars):
		return self.pythonfunction()(self, [], vars)

	def pythonsource(self):
		"""
		Return the template as Python source code.
		"""
		if self._pythonsource is None:
			v = []
			v.append("def {}(self, stack, vars):\n".format(self.name if self.name is not None else "unnamed"))
			v.append("\timport datetime\n")
			v.append("\tfrom ll import ul4c, misc, color\n")
			v.append("\tif 0:\n")
			v.append("\t\tyield\n")
			v.append("\ttry:\n")
			v.append("\t\tstack.append(self)\n")
			for node in self.content:
				v.append(node.formatpython(2))
			v.append("\texcept Exception as exc:\n")
			v.append("\t\tstack[-1]._handleexc(exc)\n")
			v.append("\tfinally:\n")
			v.append("\t\tstack.pop()\n")
			self._pythonsource = "".join(v)
		return self._pythonsource

	def jssource(self):
		"""
		Return the template as the source code of a Javascript function. A
		:class:`JavascriptSource` object will be used to generated the sourcecode.
		"""
		return "ul4.Template.loads({})".format(self.function_asjson(None, self.dumps()))

	def javasource(self):
		"""
		Return the template as Java source code.
		"""
		return "com.livinglogic.ul4.InterpretedTemplate.loads({})".format(misc.javaexpr(self.dumps()))

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

	def _parser(self, location, error):
		from ll import UL4Lexer, UL4Parser
		source = location.code
		if not source:
			raise ValueError(error)
		stream = antlr3.ANTLRStringStream(source)
		lexer = UL4Lexer.UL4Lexer(stream)
		lexer.location = location
		tokens = antlr3.CommonTokenStream(lexer)
		parser = UL4Parser.UL4Parser(tokens)
		parser.location = location
		return parser

	def _compile(self, source, name, startdelim, enddelim):
		"""
		Compile the template source code :var:`source` into opcodes.
		:var:`startdelim` and :var:`enddelim` are used as the tag delimiters.
		"""
		self.name = name
		self.startdelim = startdelim
		self.enddelim = enddelim

		# This stack stores the nested for/if/elif/else/def blocks
		stack = [self]

		self.source = source

		if source is None:
			return

		def parseexpr(location):
			return self._parser(location, "expression required").expression()

		def parsestmt(location):
			return self._parser(location, "statement required").statement()

		def parsefor(location):
			return self._parser(location, "loop expression required").for_()

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
							if not isinstance(stack[-1], For):
								raise BlockError("endfor doesn't match any for")
						elif code == "def":
							if not isinstance(stack[-1], Template):
								raise BlockError("enddef doesn't match any def")
						else:
							raise BlockError("illegal end value {!r}".format(code))
					last = stack.pop()
					# Set ``endlocation`` of block
					last.endlocation = location
					if isinstance(last, IfElIfElse):
						last.content[-1].endlocation = location
				elif location.type == "for":
					block = parsefor(location)
					stack[-1].append(block)
					stack.append(block)
				elif location.type == "break":
					for block in reversed(stack):
						if isinstance(block, For):
							break
						elif isinstance(block, Template):
							raise BlockError("break outside of for loop")
					stack[-1].append(Break(location))
				elif location.type == "continue":
					for block in reversed(stack):
						if isinstance(block, For):
							break
						elif isinstance(block, Template):
							raise BlockError("continue outside of for loop")
					stack[-1].append(Continue(location))
				elif location.type == "render":
					stack[-1].append(Render(location, parseexpr(location)))
				elif location.type == "def":
					block = Template(None, location.code, self.startdelim, self.enddelim)
					block.location = location # Set start ``location`` of sub template
					block.source = self.source # The source of the top level template (so that the offsets in :class:`Location` are correct)
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


class TemplateClosure(Object):
	fields = {"location", "endlocation", "name", "source", "startdelim", "enddelim", "content"}

	def __init__(self, template, vars):
		self.template = template
		# Freeze variable of the currently running template
		self.vars = collections.ChainMap(vars.maps[0].copy(), *vars.maps[1:])

	def _render(self, stack, vars):
		return self.template._render(stack, collections.ChainMap(vars, self.vars))

	@property
	def location(self):
		return self.template.location

	@property
	def endlocation(self):
		return self.template.endlocation

	@property
	def name(self):
		return self.template.name

	@property
	def source(self):
		return self.template.source

	@property
	def startdelim(self):
		return self.template.startdelim

	@property
	def enddelim(self):
		return self.template.enddelim

	@property
	def content(self):
		return self.template.content


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


def _formatnestednameul4(name):
	if isinstance(name, str):
		return name
	elif len(name) == 1:
		return "({},)".format(_formatnestednameul4(name[0]))
	else:
		return "({})".format(", ".join(_formatnestednameul4(name) for name in name))


def _formatnestednamepython(name):
	if isinstance(name, str):
		return "vars[{!r}]".format(name)
	elif len(name) == 1:
		return "({},)".format(_formatnestednamepython(name[0]))
	else:
		return "({})".format(", ".join(_formatnestednamepython(name) for name in name))


def _getitem(container, key):
	"""
	Helper for the ``getitem`` operator.
	"""
	try:
		return container[key]
	except KeyError:
		return UndefinedKey(key)
	except IndexError:
		return UndefinedIndex(key)
