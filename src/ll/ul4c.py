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

:mod:`ll.ul4c` compiles a template to an internal format, which makes it
possible to implement template renderers in multiple programming languages.
"""


__docformat__ = "reStructuredText"


import re, datetime, urllib.parse as urlparse, json, collections, locale

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


class LexicalError(Exception):
	def __init__(self, input):
		self.input = input

	def __str__(self):
		return "Unmatched input {!r}".format(self.input)


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
	"""
	AST node for literal text.
	"""
	def __init__(self, location=None):
		super().__init__(location)

	def format(self, indent):
		return "{}text {!r}\n".format(indent*"\t", self.location.code)

	def formatpython(self, indent):
		return "{i}# literal at position {l.starttag}:{l.endtag} ({id})\n{i}yield {l.code!r}\n".format(i=indent*"\t", id=id(self), l=self.location)

	def formatjava(self, indent):
		return "{i}// literal at position {l.starttag}:{l.endtag}\n{i}context.write({t});\n".format(i=indent*"\t", t=misc.javaexpr(self.location.code), l=self.location)


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
	AST node for loading the constant ``None``.
	"""

	value = None

	def format(self, indent):
		return "None"

	def formatpython(self, indent):
		return "None"

	def formatjava(self, indent):
		return "((Object)null)" # Make sure that call always dispatch to the most generic version


@register("true")
class True_(Const):
	"""
	AST node for loading the boolean constant ``True``.
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
	AST node for loading the boolean constant ``False``.
	"""

	value = False

	def format(self, indent):
		return "False"

	def formatpython(self, indent):
		return "False"

	def formatjava(self, indent):
		return "false"


class Value(Const):
	"""
	Base class for all AST nodes that load a constant value.
	"""
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
	"""
	AST node for loading an integer constant.
	"""


@register("float")
class Float(Value):
	"""
	AST node for loading a float constant.
	"""


@register("str")
class Str(Value):
	"""
	AST node for loading a string constant.
	"""


@register("date")
class Date(Value):
	"""
	AST node for loading a date constant.
	"""


@register("color")
class Color(Value):
	"""
	AST node for loading a color constant.
	"""

	# No need to overwrite :meth:`format` or :meth:`formatjava`

	def formatpython(self, indent):
		return "color.{!r}".format(self.value)


@register("list")
class List(AST):
	"""
	AST nodes for loading a list object.
	"""

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


@register("listcomp")
class ListComp(AST):
	"""
	AST node for list comprehension.
	"""

	precedence = 11
	fields = AST.fields.union({"item", "varname", "container", "condition"})

	def __init__(self, location=None, item=None, varname=None, container=None, condition=None):
		super().__init__(location)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.item, self.varname, self.container, self.condition)

	def format(self, indent):
		v = []
		v.append("[ ")
		v.append(self.item.format(indent))
		v.append(" for ")
		v.append(_formatnestednameul4(self.varname))
		v.append(" in ")
		v.append(self.container.format(indent))
		if self.condition is not None:
			v.append(" if ")
			v.append(self.condition.format(indent))
		v.append(" ]")
		return "".join(v)

	def formatpython(self, indent):
		v = []
		v.append("[ ")
		v.append(self.item.formatpython(indent))
		v.append(" for ")
		v.append(_formatnestednamepython(self.varname))
		v.append(" in ")
		v.append(self.container.formatpython(indent))
		if self.condition is not None:
			v.append(" if ")
			v.append(self.condition.formatpython(indent))
		v.append(" ]")
		return "".join(v)

	def formatjava(self, indent):
		v = []
		v.append("(new com.livinglogic.ul4.Execution()")
		v.append("{public Object execute(com.livinglogic.ul4.EvaluationContext context){")
		v.append("java.util.List result = new java.util.ArrayList();")
		v.append("java.util.Iterator iter = com.livinglogic.ul4.Utils.iterator({});".format(self.container.formatjava(indent)))
		v.append("while (iter.hasNext()){")
		v.append("com.livinglogic.ul4.Utils.unpackVariable(context.getVariables(), {}, iter.next());".format(misc.javaexpr(self.varname)))
		if self.condition is not None:
			v.append("if (com.livinglogic.ul4.FunctionBool.call({}))".format(self.condition.formatjava(indent)))
		v.append("result.add({});".format(self.item.formatjava(indent)))
		v.append("}return result;}}).execute(context)")
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)
		encoder.dump(self.varname)
		encoder.dump(self.container)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
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
				v.append("({},)".format(item[0].formatpython(indent)))
			else:
				v.append("({}, {})".format(item[0].formatpython(indent), item[1].formatpython(indent)))
		return "ul4c._makedict({})".format(", ".join(v))

	def formatjava(self, indent):
		v = ["new com.livinglogic.ul4.MapMaker()"]
		for item in self.items:
			if len(item) == 1:
				v.append(".add((java.util.Map){})".format(item[0].formatjava(indent)))
			else:
				v.append(".add({}, {})".format(item[0].formatjava(indent), item[1].formatjava(indent)))
		v.append(".getMap()")
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = [tuple(item) for item in decoder.load()]


@register("dictcomp")
class DictComp(AST):
	"""
	AST node for dictionary comprehension.
	"""

	precedence = 11
	fields = AST.fields.union({"key", "value", "varname", "container", "condition"})

	def __init__(self, location=None, key=None, value=None, varname=None, container=None, condition=None):
		super().__init__(location)
		self.key = key
		self.value = value
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.key, self.value, self.varname, self.container, self.condition)

	def format(self, indent):
		v = []
		v.append("{ ")
		v.append(self.key.format(indent))
		v.append(" : ")
		v.append(self.value.format(indent))
		v.append(" for ")
		v.append(_formatnestednameul4(self.varname))
		v.append(" in ")
		v.append(self.container.format(indent))
		if self.condition is not None:
			v.append(" if ")
			v.append(self.condition.format(indent))
		v.append(" }")
		return "".join(v)

	def formatpython(self, indent):
		v = []
		v.append("{ ")
		v.append(self.key.formatpython(indent))
		v.append(" : ")
		v.append(self.value.formatpython(indent))
		v.append(" for ")
		v.append(_formatnestednamepython(self.varname))
		v.append(" in ")
		v.append(self.container.formatpython(indent))
		if self.condition is not None:
			v.append(" if ")
			v.append(self.condition.formatpython(indent))
		v.append(" }")
		return "".join(v)

	def formatjava(self, indent):
		v = []
		v.append("(new com.livinglogic.ul4.Execution()")
		v.append("{public Object execute(com.livinglogic.ul4.EvaluationContext context){")
		v.append("java.util.Map result = new java.util.HashMap();")
		v.append("java.util.Iterator iter = com.livinglogic.ul4.Utils.iterator({});".format(self.container.formatjava(indent)))
		v.append("while (iter.hasNext()){")
		v.append("com.livinglogic.ul4.Utils.unpackVariable(context.getVariables(), {}, iter.next());\n".format(misc.javaexpr(self.varname)))
		if self.condition is not None:
			v.append("if (com.livinglogic.ul4.FunctionBool.call({}))".format(self.condition.formatjava(indent)))
		v.append("result.put({}, {});".format(self.key.formatjava(indent), self.value.formatjava(indent)))
		v.append("}return result;}}).execute(context)")
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.key)
		encoder.dump(self.value)
		encoder.dump(self.varname)
		encoder.dump(self.container)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
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

	def __init__(self, location=None, item=None, varname=None, container=None, condition=None):
		super().__init__(location)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.item, self.varname, self.container, self.condition)

	def format(self, indent):
		v = []
		v.append("( ")
		v.append(self.item.format(indent))
		v.append(" for ")
		v.append(_formatnestednameul4(self.varname))
		v.append(" in ")
		v.append(self.container.format(indent))
		if self.condition is not None:
			v.append(" if ")
			v.append(self.condition.format(indent))
		v.append(" )")
		return "".join(v)

	def formatpython(self, indent):
		v = []
		v.append("( ")
		v.append(self.item.formatpython(indent))
		v.append(" for ")
		v.append(_formatnestednamepython(self.varname))
		v.append(" in ")
		v.append(self.container.formatpython(indent))
		if self.condition is not None:
			v.append(" if ")
			v.append(self.condition.formatpython(indent))
		v.append(" )")
		return "".join(v)

	def formatjava(self, indent):
		v = []
		v.append("(")
		v.append("new com.livinglogic.ul4.Execution()")
		v.append("{")
		v.append("public Object execute(final com.livinglogic.ul4.EvaluationContext context)")
		v.append("{")
		v.append("final java.util.Iterator baseIterator = com.livinglogic.ul4.Utils.iterator({});".format(self.container.formatjava(indent)))
		v.append("return new com.livinglogic.ul4.FilteredIterator(){")
		v.append("protected void fetchNext()")
		v.append("{")
		v.append("while (baseIterator.hasNext())")
		v.append("{")
		v.append("com.livinglogic.ul4.Utils.unpackVariable(context.getVariables(), {}, baseIterator.next());".format(misc.javaexpr(self.varname)))
		if self.condition is not None:
			v.append("if (com.livinglogic.ul4.FunctionBool.call({}))".format(self.condition.formatjava(indent)))
			v.append("{")
		v.append("haveNextItem({});".format(self.item.formatjava(indent)))
		v.append("return;")
		if self.condition is not None:
			v.append("}")
		v.append("}")
		v.append("noNextItem();")
		v.append("}")
		v.append("};")
		v.append("}")
		v.append("}")
		v.append(").execute(context)")
		return "".join(v)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)
		encoder.dump(self.varname)
		encoder.dump(self.container)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
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
	"""
	Base class for all AST nodes that are blocks.

	A block contains a sequence of AST nodes that are executed sequencially.
	A block may execute its content zero (e.g. an ``<?if?>`` block) or more times
	(e.g. a ``<?for?>`` block).
	"""

	fields = AST.fields.union({"endlocation", "content"})

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

	def formatjava(self, indent):
		v = []
		for node in self.content:
			v.append(node.formatjava(indent))
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

	def formatjava(self, indent):
		v = []
		v.append("{}// {}\n".format(indent*"\t", repr(self.location.tag)[1:-1]))
		v.append("{}if (com.livinglogic.ul4.FunctionBool.call({}))\n".format(indent*"\t", self.condition.formatjava(indent)))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatjava(indent))
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

	def formatjava(self, indent):
		v = []
		v.append("{}// {}\n".format(indent*"\t", repr(self.location.tag)[1:-1]))
		v.append("{}else if (com.livinglogic.ul4.FunctionBool.call({}))\n".format(indent*"\t", self.condition.formatjava(indent)))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatjava(indent))
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

	def formatjava(self, indent):
		v = []
		v.append("{}// {}\n".format(indent*"\t", repr(self.location.tag)[1:-1]))
		v.append("{}else\n".format(indent*"\t"))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatjava(indent))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
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

	def formatjava(self, indent):
		v = []
		v.append("{}// {}\n".format(indent*"\t", repr(self.location.tag)[1:-1]))
		v.append("{indent}for (java.util.Iterator iter{id:x} = com.livinglogic.ul4.Utils.iterator({container}); iter{id:x}.hasNext();)\n".format(indent=indent*"\t", id=id(self), container=self.container.formatjava(indent)))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		v.append("{}com.livinglogic.ul4.Utils.unpackVariable(context.getVariables(), {}, iter{:x}.next());\n".format(indent*"\t", misc.javaexpr(self.varname), id(self)))
		v.append("{}try\n".format(indent*"\t"))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		for node in self.content:
			v.append(node.formatjava(indent))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		v.append("{}catch (com.livinglogic.ul4.BreakException ex)\n".format(indent*"\t"))
		v.append("{}{{\n".format(indent*"\t"))
		indent += 1
		v.append("{}break;\n".format(indent*"\t"))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		v.append("{}catch (com.livinglogic.ul4.ContinueException ex)\n".format(indent*"\t"))
		v.append("{}{{\n".format(indent*"\t"))
		v.append("{}}}\n".format(indent*"\t"))
		indent -= 1
		v.append("{}}}\n".format(indent*"\t"))
		return "".join(v)

	def format(self, indent):
		return "{}for {} in {}\n{}".format(indent*"\t", _formatnestednameul4(self.varname), self.container.format(indent), super().format(indent))

	def formatpython(self, indent):
		v = ["{i}# <?for?> tag at position {l.starttag}:{l.endtag} ({id})\n".format(i=indent*"\t", id=id(self), l=self.location)]
		v.append("{}for {} in {}:\n".format(indent*"\t", _formatnestednamepython(self.varname), self.container.formatpython(indent)))
		indent += 1
		for node in self.content:
			v.append(node.formatpython(indent))
		return "".join(v)


@register("break")
class Break(AST):
	"""
	AST node for a ``<?break?>`` inside a ``<?for?>`` block.
	"""

	def format(self, indent):
		return "{}break\n".format(indent*"\t")

	def formatpython(self, indent):
		return "{i}# <?break?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}break\n".format(i=indent*"\t", id=id(self), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}break;\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1])


@register("continue")
class Continue(AST):
	"""
	AST node for a ``<?continue?>`` inside a ``<?for?>`` block.
	"""

	def format(self, indent):
		return "{}continue\n".format(indent*"\t")

	def formatpython(self, indent):
		return "{i}# <?continue?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}continue\n".format(i=indent*"\t", id=id(self), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}continue;\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1])


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
		return "com.livinglogic.ul4.GetAttr.call({}, {})".format(self.obj.formatjava(indent), misc.javaexpr(self.attrname))

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
		return "({})[{}:{}]".format(self.obj.formatpython(indent), self.index1.formatpython(indent) if self.index1 is not None else "", self.index2.formatpython(indent) if self.index2 is not None else "")

	def formatjava(self, indent):
		return "com.livinglogic.ul4.GetSlice.call({}, {}, {})".format(self.obj.formatjava(indent), self.index1.formatjava(indent) if self.index1 is not None else "null", self.index2.formatjava(indent) if self.index2 is not None else "null")

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
	"""
	Base class for all AST nodes implementing unary operators.
	"""

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
	"""
	AST node for the unary ``not`` operator.
	"""

	precedence = 2

	def format(self, indent):
		return "not {}".format(self._formatop(self.obj))

	def formatpython(self, indent):
		return "not ({})".format(self.obj.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Not.call({})".format(self.obj.formatjava(indent))


@register("neg")
class Neg(Unary):
	"""
	AST node for the unary negation (i.e. "-") operator.
	"""

	precedence = 7

	def format(self, indent):
		return "-{}".format(self._formatop(self.obj))

	def formatpython(self, indent):
		return "-({})".format(self.obj.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Neg.call({})".format(self.obj.formatjava(indent))


@register("print")
class Print(Unary):
	"""
	AST node for a ``<?print?>`` tag.
	"""

	def format(self, indent):
		return "{}print {}\n".format(indent*"\t", self.obj.format(indent))

	def formatpython(self, indent):
		return "{i}# <?print?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}yield ul4c._str({o})\n".format(i=indent*"\t", id=id(self), o=self.obj.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}context.write(com.livinglogic.ul4.FunctionStr.call({v}));\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], v=self.obj.formatjava(indent))


@register("printx")
class PrintX(Unary):
	"""
	AST node for a ``<?printx?>`` tag.
	"""

	def format(self, indent):
		return "{}printx {}\n".format(indent*"\t", self.obj.format(indent))

	def formatpython(self, indent):
		return "{i}# <?printx?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}yield ul4c._xmlescape({o})\n".format(i=indent*"\t", id=id(self), o=self.obj.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}context.write(com.livinglogic.ul4.FunctionXMLEscape.call({v}));\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], v=self.obj.formatjava(indent))


class Binary(AST):
	"""
	Base class for all AST nodes implementing binary operators.
	"""

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
	"""
	AST node for subscripting operator.

	The object (which must be a list, string or dict) is loaded from the AST
	node :var:`obj1` and the index/key is loaded from the AST node :var:`obj2`.
	"""

	precedence = 9
	associative = False

	def format(self, indent):
		return "{}[{}]".format(self._formatop(self.obj1), self.obj2.format(indent))

	def formatpython(self, indent):
		return "({})[{}]".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.GetItem.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("eq")
class EQ(Binary):
	"""
	AST node for the binary ``==`` comparison operator.
	"""

	precedence = 4
	associative = False

	def format(self, indent):
		return "{} == {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) == ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.EQ.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("ne")
class NE(Binary):
	"""
	AST node for the binary ``!=`` comparison operator.
	"""

	precedence = 4
	associative = False

	def format(self, indent):
		return "{} != {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) != ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.NE.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("lt")
class LT(Binary):
	"""
	AST node for the binary ``<`` comparison operator.
	"""

	precedence = 4
	associative = False

	def format(self, indent):
		return "{} < {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) < ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.LT.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("le")
class LE(Binary):
	"""
	AST node for the binary ``<=`` comparison operator.
	"""

	precedence = 4
	associative = False

	def format(self, indent):
		return "{} <= {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) <= ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.LE.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("gt")
class GT(Binary):
	"""
	AST node for the binary ``>`` comparison operator.
	"""

	precedence = 4
	associative = False

	def format(self, indent):
		return "{} > {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) > ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.GT.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("ge")
class GE(Binary):
	"""
	AST node for the binary ``>=`` comparison operator.
	"""

	precedence = 4
	associative = False

	def format(self, indent):
		return "{} >= {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) >= ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.GE.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


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

	def format(self, indent):
		return "{} in {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) in ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Contains.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


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

	def format(self, indent):
		return "{} not in {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) not in ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.NotContains.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("add")
class Add(Binary):
	"""
	AST node for the binary addition operator.
	"""

	precedence = 5

	def format(self, indent):
		return "{}+{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) + ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Add.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("sub")
class Sub(Binary):
	"""
	AST node for the binary substraction operator.
	"""

	precedence = 5
	associative = False

	def format(self, indent):
		return "{}-{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) - ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Sub.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("mul")
class Mul(Binary):
	"""
	AST node for the binary multiplication operator.
	"""

	precedence = 6

	def format(self, indent):
		return "{}*{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) * ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Mul.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("floordiv")
class FloorDiv(Binary):
	"""
	AST node for the binary truncating division operator.
	"""

	precedence = 6
	associative = False

	def format(self, indent):
		return "{}//{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) // ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.FloorDiv.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("truediv")
class TrueDiv(Binary):
	"""
	AST node for the binary true division operator.
	"""

	precedence = 6
	associative = False

	def format(self, indent):
		return "{}/{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) / ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.TrueDiv.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("and")
class And(Binary):
	"""
	AST node for the binary ``and`` operator.
	"""

	precedence = 1

	def format(self, indent):
		return "{} and {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) and ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "new com.livinglogic.ul4.Execution(){{public Object execute(com.livinglogic.ul4.EvaluationContext context){{Object obj1 = {}; return (!com.livinglogic.ul4.FunctionBool.call(obj1)) ? obj1  : {};}}}}.execute(context)".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("or")
class Or(Binary):
	"""
	AST node for the binary ``or`` operator.
	"""

	precedence = 0

	def format(self, indent):
		return "{} or {}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) or ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "new com.livinglogic.ul4.Execution(){{public Object execute(com.livinglogic.ul4.EvaluationContext context){{Object obj1 = {}; return com.livinglogic.ul4.FunctionBool.call(obj1) ? obj1  : {};}}}}.execute(context)".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


@register("mod")
class Mod(Binary):
	"""
	AST node for the binary modulo operator.
	"""

	precedence = 6
	associative = False

	def format(self, indent):
		return "{}%{}".format(self._formatop(self.obj1), self._formatop(self.obj2))

	def formatpython(self, indent):
		return "({}) % ({})".format(self.obj1.formatpython(indent), self.obj2.formatpython(indent))

	def formatjava(self, indent):
		return "com.livinglogic.ul4.Mod.call({}, {})".format(self.obj1.formatjava(indent), self.obj2.formatjava(indent))


class ChangeVar(AST):
	"""
	Baseclass for all AST nodes that store or modify a variable.

	The variable name is stored in the string :var:`varname` and the value that
	will be stored or be used to modify the stored value is loaded from the
	AST node :var:`value`.
	"""

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
	"""
	AST node that stores a value into a variable.
	"""

	def format(self, indent):
		return "{}{} = {}\n".format(indent*"\t", _formatnestednameul4(self.varname), self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}{n} = {v}\n".format(i=indent*"\t", id=id(self), n=_formatnestednamepython(self.varname), v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}com.livinglogic.ul4.Utils.unpackVariable(context.getVariables(), {n}, {v});\n".format(i=indent*"\t", n=misc.javaexpr(self.varname), s=repr(self.location.tag)[1:-1], v=self.value.formatjava(indent))


@register("addvar")
class AddVar(ChangeVar):
	"""
	AST node that adds a value to a variable (i.e. the ``+=`` operator).
	"""

	def format(self, indent):
		return "{}{} += {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] += {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}context.put({n}, com.livinglogic.ul4.Add.call(context.get({n}), {v}));\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], n=misc.javaexpr(self.varname), v=self.value.formatjava(indent))


@register("subvar")
class SubVar(ChangeVar):
	"""
	AST node that substracts a value from a variable (i.e. the ``-=`` operator).
	"""

	def format(self, indent):
		return "{}{} -= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] -= {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}context.put({n}, com.livinglogic.ul4.Sub.call(context.get({n}), {v}));\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], n=misc.javaexpr(self.varname), v=self.value.formatjava(indent))


@register("mulvar")
class MulVar(ChangeVar):
	"""
	AST node that multiplies a variable by a value (i.e. the ``*=`` operator).
	"""

	def format(self, indent):
		return "{}{} *= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] *= {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}context.put({n}, com.livinglogic.ul4.Mul.call(context.get({n}), {v}));\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], n=misc.javaexpr(self.varname), v=self.value.formatjava(indent))


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

	def formatjava(self, indent):
		return "{i}// {s}\n{i}context.put({n}, com.livinglogic.ul4.FloorDiv.call(context.get({n}), {v}));\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], n=misc.javaexpr(self.varname), v=self.value.formatjava(indent))


@register("truedivvar")
class TrueDivVar(ChangeVar):
	"""
	AST node that divides a variable by a value (i.e. the ``/=`` operator).
	"""

	def format(self, indent):
		return "{}{} /= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] /= {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}context.put({n}, com.livinglogic.ul4.TrueDiv.call(context.get({n}), {v}));\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], n=misc.javaexpr(self.varname), v=self.value.formatjava(indent))


@register("modvar")
class ModVar(ChangeVar):
	"""
	AST node for the ``%=`` operator.
	"""

	def format(self, indent):
		return "{}{} %= {}\n".format(indent*"\t", self.varname, self.value.format(indent))

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] %= {v}\n".format(i=indent*"\t", id=id(self), n=self.varname, v=self.value.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}context.put({n}, com.livinglogic.ul4.Mod.call(context.get({n}), {v}));\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], n=misc.javaexpr(self.varname), v=self.value.formatjava(indent))


@register("delvar")
class DelVar(AST):
	"""
	AST node for deleting a variable.

	The name of the variable is stored in the string :var:`varname`.
	"""

	fields = AST.fields.union({"varname"})

	def __init__(self, location=None, varname=None):
		super().__init__(location)
		self.varname = varname

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.varname)

	def format(self, indent):
		return "{}del {}\n".format(indent*"\t", self.varname)

	def formatpython(self, indent):
		return "{i}# <?code?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}del vars[{n!r}]\n".format(i=indent*"\t", id=id(self), n=self.varname, l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}context.remove({n});\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], n=misc.javaexpr(self.varname))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.varname)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.varname = decoder.load()


@register("callfunc")
class CallFunc(AST):
	"""
	AST node for calling a function.

	The function name is stored in the string :var:`funcname`. The list of
	arguments is loaded from the list of AST nodes :var:`args`.
	"""

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
			now="ul4c._now({})".format,
			utcnow="ul4c._utcnow({})".format,
			date="datetime.datetime({})".format,
			timedelta="ul4c._timedelta({})".format,
			monthdelta="misc.monthdelta({})".format,
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
			istimedelta="ul4c._istimedelta({})".format,
			ismonthdelta="ul4c._ismonthdelta({})".format,
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
			min="min({})".format,
			max="max({})".format,
			sorted="sorted({})".format,
			range="range({})".format,
			type="ul4c._type({})".format,
			reversed="reversed({})".format,
			randrange="random.randrange({})".format,
			randchoice="random.choice({})".format,
			format="ul4c._format({})".format,
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
			now="com.livinglogic.ul4.FunctionNow.call({})".format,
			utcnow="com.livinglogic.ul4.FunctionUTCNow.call({})".format,
			date="com.livinglogic.ul4.FunctionDate.call({})".format,
			timedelta="com.livinglogic.ul4.FunctionTimeDelta.call({})".format,
			monthdelta="com.livinglogic.ul4.FunctionMonthDelta.call({})".format,
			vars="com.livinglogic.ul4.FunctionVars.call(context.getVariables(){})".format,
			random="com.livinglogic.ul4.FunctionRandom.call({})".format,
			xmlescape="com.livinglogic.ul4.FunctionXMLEscape.call({})".format,
			csv="com.livinglogic.ul4.FunctionCSV.call({})".format,
			asjson="com.livinglogic.ul4.FunctionAsJSON.call({})".format,
			fromjson="com.livinglogic.ul4.FunctionFromJSON.call({})".format,
			asul4on="com.livinglogic.ul4.FunctionAsUL4ON.call({})".format,
			fromul4on="com.livinglogic.ul4.FunctionFromUL4ON.call({})".format,
			str="com.livinglogic.ul4.FunctionStr.call({})".format,
			int="com.livinglogic.ul4.FunctionInt.call({})".format,
			float="com.livinglogic.ul4.FunctionFloat.call({})".format,
			bool="com.livinglogic.ul4.FunctionBool.call({})".format,
			len="com.livinglogic.ul4.FunctionLen.call({})".format,
			abs="com.livinglogic.ul4.FunctionAbs.call({})".format,
			enumerate="com.livinglogic.ul4.FunctionEnumerate.call({})".format,
			enumfl="com.livinglogic.ul4.FunctionEnumFL.call({})".format,
			isfirstlast="com.livinglogic.ul4.FunctionIsFirstLast.call({})".format,
			isfirst="com.livinglogic.ul4.FunctionIsFirst.call({})".format,
			islast="com.livinglogic.ul4.FunctionIsLast.call({})".format,
			isnone="com.livinglogic.ul4.FunctionIsNone.call({})".format,
			isstr="com.livinglogic.ul4.FunctionIsStr.call({})".format,
			isint="com.livinglogic.ul4.FunctionIsInt.call({})".format,
			isfloat="com.livinglogic.ul4.FunctionIsFloat.call({})".format,
			isbool="com.livinglogic.ul4.FunctionIsBool.call({})".format,
			isdate="com.livinglogic.ul4.FunctionIsDate.call({})".format,
			istimedelta="com.livinglogic.ul4.FunctionIsTimeDelta.call({})".format,
			ismonthdelta="com.livinglogic.ul4.FunctionIsMonthDelta.call({})".format,
			islist="com.livinglogic.ul4.FunctionIsList.call({})".format,
			isdict="com.livinglogic.ul4.FunctionIsDict.call({})".format,
			iscolor="com.livinglogic.ul4.FunctionIsColor.call({})".format,
			istemplate="com.livinglogic.ul4.FunctionIsTemplate.call({})".format,
			repr="com.livinglogic.ul4.FunctionRepr.call({})".format,
			get="com.livinglogic.ul4.FunctionGet.call(context.getVariables(){})".format,
			chr="com.livinglogic.ul4.FunctionChr.call({})".format,
			ord="com.livinglogic.ul4.FunctionOrd.call({})".format,
			hex="com.livinglogic.ul4.FunctionHex.call({})".format,
			oct="com.livinglogic.ul4.FunctionOct.call({})".format,
			bin="com.livinglogic.ul4.FunctionBin.call({})".format,
			min="com.livinglogic.ul4.FunctionMin.call({})".format,
			max="com.livinglogic.ul4.FunctionMax.call({})".format,
			sorted="com.livinglogic.ul4.FunctionSorted.call({})".format,
			range="com.livinglogic.ul4.FunctionRange.call({})".format,
			type="com.livinglogic.ul4.FunctionType.call({})".format,
			reversed="com.livinglogic.ul4.FunctionReversed.call({})".format,
			randrange="com.livinglogic.ul4.FunctionRandRange.call({})".format,
			randchoice="com.livinglogic.ul4.FunctionRandChoice.call({})".format,
			format="com.livinglogic.ul4.FunctionFormat.call({})".format,
			zip="com.livinglogic.ul4.FunctionZip.call({})".format,
			urlquote="com.livinglogic.ul4.FunctionURLQuote.call({})".format,
			urlunquote="com.livinglogic.ul4.FunctionURLUnquote.call({})".format,
			rgb="com.livinglogic.ul4.FunctionRGB.call({})".format,
			hls="com.livinglogic.ul4.FunctionHLS.call({})".format,
			hsv="com.livinglogic.ul4.FunctionHSV.call({})".format,
		)
		try:
			formatter = functions[self.funcname]
		except KeyError:
			raise UnknownFunctionError(self.funcname)
		if self.funcname in ("get", "vars"):
			return formatter("".join(", " + arg.formatjava(indent) for arg in self.args))
		else:
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
	"""
	AST node for calling a method.

	The method name is stored in the string :var:`methname`. The object for which
	the method will be called is loaded from the AST node :var:`obj` and the list
	of arguments is loaded from the list of AST nodes :var:`args`.
	"""

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
			find="ul4c._find({}, {})".format,
			rfind="ul4c._rfind({}, {})".format,
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
			week="ul4c._week({}, {})".format,
			items="({}).items({})".format,
			join="({}).join({})".format,
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
		methods = dict(
			split="com.livinglogic.ul4.MethodSplit.call({})".format,
			rsplit="com.livinglogic.ul4.MethodRSplit.call({})".format,
			strip="com.livinglogic.ul4.MethodStrip.call({})".format,
			lstrip="com.livinglogic.ul4.MethodLStrip.call({})".format,
			rstrip="com.livinglogic.ul4.MethodRStrip.call({})".format,
			find="com.livinglogic.ul4.MethodFind.call({})".format,
			rfind="com.livinglogic.ul4.MethodRFind.call({})".format,
			startswith="com.livinglogic.ul4.MethodStartsWith.call({})".format,
			endswith="com.livinglogic.ul4.MethodEndsWith.call({})".format,
			upper="com.livinglogic.ul4.MethodUpper.call({})".format,
			lower="com.livinglogic.ul4.MethodLower.call({})".format,
			capitalize="com.livinglogic.ul4.MethodCapitalize.call({})".format,
			replace="com.livinglogic.ul4.MethodReplace.call({})".format,
			r="com.livinglogic.ul4.MethodR.call({})".format,
			g="com.livinglogic.ul4.MethodG.call({})".format,
			b="com.livinglogic.ul4.MethodB.call({})".format,
			a="com.livinglogic.ul4.MethodA.call({})".format,
			hls="com.livinglogic.ul4.MethodHLS.call({})".format,
			hlsa="com.livinglogic.ul4.MethodHLSA.call({})".format,
			hsv="com.livinglogic.ul4.MethodHSV.call({})".format,
			hsva="com.livinglogic.ul4.MethodHSVA.call({})".format,
			lum="com.livinglogic.ul4.MethodLum.call({})".format,
			week="com.livinglogic.ul4.MethodWeek.call({})".format,
			weekday="com.livinglogic.ul4.MethodWeekday.call({})".format,
			items="com.livinglogic.ul4.MethodItems.call({})".format,
			join="com.livinglogic.ul4.MethodJoin.call({})".format,
			render="com.livinglogic.ul4.MethodRender.call(context.getWriter(), {})".format,
			renders="com.livinglogic.ul4.MethodRenderS.call({})".format,
			mimeformat="com.livinglogic.ul4.MethodMIMEFormat.call({})".format,
			isoformat="com.livinglogic.ul4.MethodISOFormat.call({})".format,
			yearday="com.livinglogic.ul4.MethodYearday.call({})".format,
			get="com.livinglogic.ul4.MethodGet.call({})".format,
			withlum="com.livinglogic.ul4.MethodWithLum.call({})".format,
			witha="com.livinglogic.ul4.MethodWithA.call({})".format,
			day="com.livinglogic.ul4.MethodDay.call({})".format,
			month="com.livinglogic.ul4.MethodMonth.call({})".format,
			year="com.livinglogic.ul4.MethodYear.call({})".format,
			hour="com.livinglogic.ul4.MethodHour.call({})".format,
			minute="com.livinglogic.ul4.MethodMinute.call({})".format,
			second="com.livinglogic.ul4.MethodSecond.call({})".format,
			microsecond="com.livinglogic.ul4.MethodMicrosecond.call({})".format,
		)
		try:
			formatter = methods[self.methname]
		except KeyError:
			raise UnknownMethodError(self.methname)
		return formatter(", ".join(arg.formatjava(indent) for arg in [self.obj] + self.args))

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
	"""
	AST node for calling a method with keyword arguments.

	The method name is stored in the string :var:`methname`. The object for which
	the method will be called is loaded from the AST node :var:`obj` and the list
	of arguments is loaded :var:`args`. :var:`args` is a list of either:

	*	1-item tuples containing an AST node: this is used for the ``**arg``
		argument variant;
	*	2-item tuples containing an argument name and an AST node: this is used
		for the ``name=arg`` variant.
	"""

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

	def formatjava(self, indent):
		v = []
		for arg in self.args:
			if len(arg) == 1:
				v.append(".add((java.util.Map){})".format(arg[0].formatjava(indent)))
			else:
				v.append(".add({}, {})".format(misc.javaexpr(arg[0]), arg[1].formatjava(indent)))
		args = "new com.livinglogic.ul4.MapMaker(){}.getMap()".format("".join(v))
		if self.methname == "renders":
			return "com.livinglogic.ul4.KeywordMethodRenderS.call({}, {})".format(self.obj.formatjava(indent), args)
		elif self.methname == "render":
			return "com.livinglogic.ul4.KeywordMethodRender.call(context.getWriter(), {}, {})".format(self.obj.formatjava(indent), args)
		else:
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
	"""
	AST node for the ``<?render?>`` tag.
	"""

	def __repr__(self):
		return "{}({!r})".format(self.__class__.__name__, self.obj)

	def format(self, indent):
		return "{}render {}\n".format(indent*"\t", self.obj.format(indent))

	def formatpython(self, indent):
		if isinstance(self.obj, (CallMeth, CallMethKeywords)) and self.obj.methname == "render":
			v = ["{i}# <?render?> tag at position {l.starttag}:{l.endtag} ({id})\n".format(i=indent*"\t", id=id(self), l=self.location)]
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
			return "{i}# <?render?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}yield ul4c._str({o})\n".format(i=indent*"\t", id=id(self), o=self.obj.formatpython(indent), l=self.location)

	def formatjava(self, indent):
		return "{i}// {s}\n{i}{o};\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], o=self.obj.formatjava(indent))


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

	A :class:`Template` object is itself an AST node. Evaluating it will store
	the template object under its name in the local variables.
	"""
	version = "19"
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
		return "{i}# <?def?> tag at position {l.starttag}:{l.endtag} ({id})\n{i}vars[{n!r}] = self._getast({id})\n".format(i=indent*"\t", n=self.name if self.name is not None else "unnamed", id=id(self), l=self.location)

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
		v.append("{}public void render(com.livinglogic.ul4.EvaluationContext context) throws java.io.IOException\n".format(indent*"\t"))
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
		return "{i}// {s}\n{i}context.put(\n{i}\t{n},\n{i}\t{c}\n{i});\n".format(i=indent*"\t", s=repr(self.location.tag)[1:-1], n=misc.javaexpr(self.name if self.name is not None else "unnamed"), c=self._java(indent))

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
			name = self.name if self.name is not None else "unnamed"
			source = self.pythonsource()
			ns = {}
			exec(source, ns)
			self._pythonfunction = ns[name]
		return self._pythonfunction

	def __call__(self, **vars):
		return self.pythonfunction()(self, vars)

	def pythonsource(self):
		"""
		Return the template as Python source code.
		"""
		if self._pythonsource is None:
			v = []
			v.append("def {}(self, vars):\n".format(self.name if self.name is not None else "unnamed"))
			v.append("\timport datetime, random\n")
			v.append("\tfrom ll import ul4c, misc, color\n")
			v.append("\tif 0:\n")
			v.append("\t\tyield\n")
			v.append("\ttry:\n")
			for node in self.content:
				v.append(node.formatpython(2))
			v.append("\texcept Exception as exc:\n")
			v.append("\t\tself._handleexc(exc)\n")
			self._pythonsource = "".join(v)
		return self._pythonsource

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
			return "com.livinglogic.ul4.InterpretedTemplate.loads({})".format(misc.javaexpr(self.dumps()))
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
		if s in ("for", "if", "in", "not", "or", "and", "del"):
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

	@spark.production('nestedname ::= var')
	def nestedname(self, var):
		return var.name

	@spark.production('nestedname ::= ( nestedname , )')
	def nestedname1(self, _0, name, _1, _2):
		return (name,)

	@spark.production('buildnestedname ::= ( nestedname , nestedname')
	def buildnestedname(self, _0, name1, _1, name2):
		return (name1, name2)

	@spark.production('buildnestedname ::= buildnestedname , nestedname')
	def addnestedname(self, buildname, _0, name):
		return buildname + (name,)

	@spark.production('nestedname ::= buildnestedname )')
	def finishnestedname0(self, buildname, _0):
		return buildname

	@spark.production('nestedname ::= buildnestedname , )')
	def finishnestedname1(self, buildname, _0, _1):
		return buildname

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

	@spark.production('expr11 ::= [ expr0 for nestedname in expr0 ]')
	def expr_listcomp0(self, _0, item, _1, varname, _2, container, _3):
		return ListComp(self.location, item, varname, container)

	@spark.production('expr11 ::= [ expr0 for nestedname in expr0 if expr0 ]')
	def expr_listcomp1(self, _0, item, _1, varname, _2, container, _3, condition, _4):
		return ListComp(self.location, item, varname, container, condition)

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

	@spark.production('expr11 ::= { expr0 : expr0 for nestedname in expr0 }')
	def expr_dictcomp0(self, _0, key, _1, value, _2, varname, _3, container, _4):
		return DictComp(self.location, key, value, varname, container)

	@spark.production('expr11 ::= { expr0 : expr0 for nestedname in expr0 if expr0 }')
	def expr_dictcomp1(self, _0, key, _1, value, _2, varname, _3, container, _4, condition, _5):
		return DictComp(self.location, key, value, varname, container, condition)

	@spark.production('expr11 ::= ( expr0 for nestedname in expr0 )')
	def expr_genexp0(self, _0, item, _1, varname, _2, container, _3):
		return GenExpr(self.location, item, varname, container)

	@spark.production('expr11 ::= ( expr0 for nestedname in expr0 if expr0 )')
	def expr_genexp1(self, _0, item, _1, varname, _2, container, _3, condition, _4):
		return GenExpr(self.location, item, varname, container, condition)

	@spark.production('exprarg ::= expr0')
	def expr_arg(self, expr):
		return expr

	@spark.production('exprarg ::= expr0 for nestedname in expr0')
	def expr_arg_genexp0(self, item, _0, varname, _1, container):
		return GenExpr(self.location, item, varname, container)

	@spark.production('exprarg ::= expr0 for nestedname in expr0 if expr0')
	def expr_arg_genexp1(self, item, _0, varname, _1, container, _2, condition):
		return GenExpr(self.location, item, varname, container, condition)

	@spark.production('expr11 ::= ( expr0 )')
	def expr_bracket(self, _0, expr, _1):
		return expr

	@spark.production('expr10 ::= var ( )')
	def expr_callfunc0(self, var, _0, _1):
		return CallFunc(self.location, var.name)

	@spark.production('buildfunccall ::= var ( exprarg')
	def expr_buildcallfunc(self, var, _0, arg):
		return CallFunc(self.location, var.name, arg)

	@spark.production('buildfunccall ::= buildfunccall , exprarg')
	def expr_addcallfunc(self, funccall, _0, arg):
		funccall.args.append(arg)
		return funccall

	@spark.production('expr10 ::= buildfunccall )')
	def expr_finishcallfunc0(self, funccall, _0):
		return funccall

	@spark.production('expr10 ::= buildfunccall , )')
	def expr_finishcallfunc1(self, funccall, _0, _1):
		return funccall

	@spark.production('expr9 ::= expr9 . var')
	def expr_getattr(self, expr, _0, var):
		return GetAttr(self.location, expr, var.name)

	@spark.production('expr9 ::= expr9 . var ( )')
	def expr_callmeth0(self, expr, _0, var, _1, _2):
		return CallMeth(self.location, var.name, expr)

	@spark.production('expr9 ::= expr9 . var ( exprarg )')
	def expr_callmeth1(self, expr, _0, var, _1, arg1, _2):
		return CallMeth(self.location, var.name, expr, arg1)

	@spark.production('expr9 ::= expr9 . var ( exprarg , exprarg )')
	def expr_callmeth2(self, expr, _0, var, _1, arg1, _2, arg2, _3):
		return CallMeth(self.location, var.name, expr, arg1, arg2)

	@spark.production('expr9 ::= expr9 . var ( exprarg , exprarg , exprarg )')
	def expr_callmeth3(self, expr, _0, var, _1, arg1, _2, arg2, _3, arg3, _4):
		return CallMeth(self.location, var.name, expr, arg1, arg2, arg3)

	@spark.production('callmethkw ::= expr9 . var ( var = exprarg')
	def methkw_startname(self, expr, _0, methname, _1, argname, _2, argvalue):
		return CallMethKeywords(self.location, methname.name, expr, (argname.name, argvalue))

	@spark.production('callmethkw ::= expr9 . var ( ** exprarg')
	def methkw_startdict(self, expr, _0, methname, _1, _2, argvalue):
		return CallMethKeywords(self.location, methname.name, expr, (argvalue,))

	@spark.production('callmethkw ::= callmethkw , var = exprarg')
	def methkw_buildname(self, call, _0, argname, _1, argvalue):
		call.args.append((argname.name, argvalue))
		return call

	@spark.production('callmethkw ::= callmethkw , ** exprarg')
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

	@spark.production('for ::= nestedname in expr0')
	def for_(self, name, _0, cont):
		return For(self.location, name, cont)


class StmtParser(ExprParser):
	emptyerror = "statement required"
	start = "stmt"

	@spark.production('stmt ::= nestedname = expr0')
	def stmt_assign(self, name, _0, value):
		return StoreVar(self.location, name, value)

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


def _vars(vars):
	"""
	Helper for the ``vars`` function.
	"""
	return vars


def _now():
	"""
	Helper for the ``now`` function.
	"""
	return datetime.datetime.now()


def _utcnow():
	"""
	Helper for the ``utcnow`` function.
	"""
	return datetime.datetime.utcnow()


def _str(obj=None):
	"""
	Helper for the ``str`` function.
	"""
	if obj is None:
		return ""
	else:
		return str(obj)


def _format(obj, fmt, lang=None):
	"""
	Helper for the ``format`` function.
	"""
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
						raise
		finally:
			locale.setlocale(locale.LC_ALL, oldlocale)
	else:
		return format(obj, fmt)


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


def _istimedelta(obj):
	"""
	Helper for the ``istimedelta`` function.
	"""
	return isinstance(obj, datetime.timedelta)


def _ismonthdelta(obj):
	"""
	Helper for the ``ismonthdelta`` function.
	"""
	return isinstance(obj, misc.monthdelta)


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


def _find(obj, sub, start=None, end=None):
	"""
	Helper for the ``find`` method.
	"""
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


def _rfind(obj, sub, start=None, end=None):
	"""
	Helper for the ``rfind`` method.
	"""
	if isinstance(obj, str):
		return obj.rfind(sub, start, end)
	else:
		for i in reversed(range(*slice(start, end).indices(len(obj)))):
			if obj[i] == sub:
				return i
		return -1


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


def _week(obj, firstweekday=None):
	"""
	Helper for the ``week`` method.
	"""
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


def _isoformat(obj):
	"""
	Helper for the ``isoformat`` method.
	"""
	result = obj.isoformat()
	suffix = "T00:00:00"
	if result.endswith(suffix):
		return result[:-len(suffix)]
	return result


def _timedelta(days=0, seconds=0, microseconds=0):
	"""
	Helper for the ``timedelta`` method.
	"""
	return datetime.timedelta(days, seconds, microseconds)
