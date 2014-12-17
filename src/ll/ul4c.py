# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2009-2014 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2014 by Walter Dörwald
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


import re, types, datetime, urllib.parse as urlparse, json, collections, locale, itertools, random, functools, math, inspect

import antlr3


# Regular expression used for splitting dates in isoformat
_datesplitter = re.compile("[-T:.]")


_defaultitem = object()


def register(name):
	from ll import ul4on

	def registration(cls):
		ul4on.register("de.livinglogic.ul4." + name)(cls)
		cls.type = name
		return cls
	return registration


def generator(f):
	"""
	Decorating a function with :func:`generator` declares the decorated function
	to UL4 templates as a generator method (i.e. a method that can generate
	output and return a value).
	"""
	f.__ul4generator__ = True
	return f


###
### Location information
###

@register("location")
class Location:
	"""
	A :class:`Location` object contains information about the location of a
	template tag.
	"""
	ul4attrs = {"root", "source", "type", "starttag", "endtag", "startcode", "endcode", "tag", "code"}

	def __init__(self, root=None, source=None, type=None, starttag=None, endtag=None, startcode=None, endcode=None):
		"""
		Create a new :class:`Location` object. The arguments have the following
		meaning:

			:obj:`root`
				The :class:`Template` object

			:obj:`source`
				The complete source string

			:obj:`type`
				The tag type (i.e. ``"for"``, ``"if"``, etc. or ``None`` for
				literal text)

			:obj:`starttag`
				The start position of the start delimiter.

			:obj:`endtag`
				The end position of the end delimiter.

			:obj:`startcode`
				The start position of the tag code.

			:obj:`endcode`
				The end position of the tag code.
		"""
		self.root = root
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
		encoder.dump(self.root)
		encoder.dump(self.source)
		encoder.dump(self.type)
		encoder.dump(self.starttag)
		encoder.dump(self.endtag)
		encoder.dump(self.startcode)
		encoder.dump(self.endcode)

	def ul4onload(self, decoder):
		self.root = decoder.load()
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
	def __init__(self, node):
		self.node = node

	def __repr__(self):
		return "<{}.{} in {} at {:#x}>".format(self.__class__.__module__, self.__class__.__name__, self.node, id(self))

	def __str__(self):
		if isinstance(self.node, (Template, TemplateClosure)):
			if self.node.name is not None:
				return "in template named {}".format(self.node.name)
			else:
				return "in unnamed template"
		elif isinstance(self.node, Location):
			return "in tag {}".format(self.node)
		else:
			return "in tag {}".format(self.node.location)


class BlockError(Exception):
	"""
	Exception that is raised by the compiler when an illegal block structure is
	detected (e.g. an ``<?end if?>`` without a previous ``<?if?>``).
	"""

	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message


###
### Exceptions used by the interpreted code for flow control
###

class BreakException(Exception):
	pass


class ContinueException(Exception):
	pass


class ReturnException(Exception):
	def __init__(self, value):
		self.value = value


###
### Various versions of undefined objects
###

class Undefined:
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
		self._key = key

	def __repr__(self):
		return "UndefinedKey({!r})".format(self._key)


class UndefinedVariable(Undefined):
	def __init__(self, name):
		self._name = name

	def __repr__(self):
		return "UndefinedVariable({!r})".format(self._name)


class UndefinedIndex(Undefined):
	def __init__(self, index):
		self._index = index

	def __repr__(self):
		return "UndefinedIndex({!r})".format(self._index)


###
### Helper functions
###

def _handleeval(f):
	"""
	Decorator for each implementation of the :meth:`eval` method.

	This decorator is responsible for exception handling. An exception that
	bubbles up the Python call stack will generate an exception chain that
	follows the UL4 call stack.
	"""
	@functools.wraps(f)
	def wrapped(self, *args):
		try:
			return (yield from f(self, *args))
		except (BreakException, ContinueException, ReturnException) as ex:
			# Pass those exception through to the AST nodes that will handle them (:class:`ForBlock` or :class:`Template`)
			raise
		except Error as ex:
			# If the current AST node has a different location than the AST node where the exception came from
			if ex.node.location is not self.location:
				# ... wrap the exception in another exception that shows our location
				raise Error(self) from ex
			else:
				# Reraise original exception, as we're still in the same location
				raise
		except Exception as ex:
			# Wrap original exception in another exception that shows the location
			raise Error(self) from ex
	return wrapped


def _unpackvar(lvalue, value):
	"""
	A generator used for recursively unpacking values for assignment.

	:obj:`lvalue` may be an :class:`AST` object (in which case the recursion ends)
	or a (possible nested) sequence of :class:`AST` objects.

	The values produced are (AST node, value) tuples.
	"""
	if isinstance(lvalue, AST):
		yield (lvalue, value)
	else:
		# Materialize iterators on the right hand side, but protect against infinite iterators
		if not isinstance(value, (tuple, list, str)):
			# If we get one item more than required, we have an error
			# Also :func:`islice` might fail if the right hand side isn't iterable (e.g. ``(a, b) == 42``)
			value = list(itertools.islice(value, len(lvalue)+1))
		if len(lvalue) != len(value):
			# The number of variables on the left hand side doesn't match the number of values on the right hand side
			raise TypeError("need {} value{} to unpack".format(len(lvalue), "s" if len(lvalue) != 1 else ""))
		for (lvalue, value) in zip(lvalue, value):
			yield from _unpackvar(lvalue, value)


def _resultfromgenerator(iter):
	"""
	Exhaust a generator and return it return value
	"""
	try:
		while True:
			next(iter)
	except StopIteration as ex:
		return ex.value


def _makevars(signature, args, kwargs):
	"""
	Bind :obj:`args` and :obj:`kwargs` to the :class:`inspect.Signature` object
	:obj:`signature` and return the resulting argument dictionary.

	:obj:`signature` may also be ``None`` in which case :obj:`args` must be empty
	and :obj:kwargs is returned, i.e. the signature is treaded als accepting no
	positional argument and any keyword argument.
	"""
	if signature is None:
		if args:
			raise TypeError("positional arguments not supported")
		return kwargs
	else:
		vars = signature.bind(*args, **kwargs)

		for param in signature.parameters.values():
			if param.name not in vars.arguments:
				if param.kind is inspect.Parameter.VAR_POSITIONAL:
					default = ()
				elif param.kind is inspect.Parameter.VAR_KEYWORD:
					default = {}
				else:
					default = param.default
				vars.arguments[param.name] = default
		return vars.arguments


def _str(obj=""):
	if obj is None:
		return ""
	elif isinstance(obj, Undefined):
		return ""
	elif isinstance(obj, str):
		return obj
	elif isinstance(obj, (collections.Sequence, collections.Set, collections.Mapping)):
		return _repr(obj)
	else:
		return str(obj)


def _repr_helper(obj, seen):
	from ll import color
	if isinstance(obj, str):
		yield repr(obj)
	elif isinstance(obj, datetime.datetime):
		s = str(obj.isoformat())
		if s.endswith("T00:00:00"):
			s = s[:-9]
		yield "@({})".format(s)
	elif isinstance(obj, datetime.date):
		yield "@({})".format(obj.isoformat())
	elif isinstance(obj, datetime.timedelta):
		yield repr(obj).partition(".")[-1]
	elif isinstance(obj, color.Color):
		if obj[3] == 0xff:
			s = "#{:02x}{:02x}{:02x}".format(obj[0], obj[1], obj[2])
			if s[1] == s[2] and s[3] == s[4] and s[5] == s[6]:
				s = "#{}{}{}".format(s[1], s[3], s[5])
			yield s
		else:
			s = "#{:02x}{:02x}{:02x}{:02x}".format(*obj)
			if s[1] == s[2] and s[3] == s[4] and s[5] == s[6] and s[7] == s[8]:
				s = "#{}{}{}{}".format(s[1], s[3], s[5], s[7])
			yield s
	elif isinstance(obj, collections.Sequence):
		if id(obj) in seen:
			yield "..."
		else:
			seen.add(id(obj))
			yield "["
			for (i, item) in enumerate(obj):
				if i:
					yield ", "
				yield from _repr_helper(item, seen)
			yield "]"
			seen.discard(id(obj))
	elif isinstance(obj, collections.Set):
		if id(obj) in seen:
			yield "..."
		else:
			if obj:
				seen.add(id(obj))
				yield "{"
				for (i, item) in enumerate(obj):
					if i:
						yield ", "
					yield from _repr_helper(item, seen)
				yield "}"
				seen.discard(id(obj))
			else:
				yield "{/}"
	elif isinstance(obj, collections.Mapping):
		if id(obj) in seen:
			yield "..."
		else:
			seen.add(id(obj))
			yield "{"
			for (i, (key, value)) in enumerate(obj.items()):
				if i:
					yield ", "
				yield from _repr_helper(key, seen)
				yield ": "
				yield from _repr_helper(value, seen)
			yield "}"
			seen.discard(id(obj))
	else:
		yield repr(obj)


def _repr(obj):
	return "".join(_repr_helper(obj, set()))


def _asjson(obj):
	from ll import color, misc
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
		return "ul4.MonthDelta.create({})".format(obj.months())
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


def _xmlescape(obj):
	if obj is None:
		return ""
	elif isinstance(obj, Undefined):
		return ""
	else:
		from ll import misc
		return misc.xmlescape(str(obj))


###
### Compiler stuff: Nodes for the AST
###

class AST:
	"""
	Base class for all syntax tree nodes.
	"""

	# Set of attributes available via :meth:`getitem`.
	ul4attrs = {"type", "location", "start", "end"}

	# "Global" functions. Will be exposed to UL4 code
	functions = {}

	def __init__(self, location=None, start=None, end=None):
		self.location = location
		self.start = start
		self.end = end

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		p.text(repr(self))

	def __str__(self):
		v = []
		level = 0
		needlf = False
		for code in self._str():
			if code is None:
				needlf = True
			elif isinstance(code, int):
				level += code
			else:
				if needlf:
					v.append("\n")
					v.append(level*"\t")
					needlf = False
				v.append(code)
		if needlf:
			v.append("\n")
		return "".join(v)

	def _str(self):
		# Format :obj:`self`.
		# This is used by :meth:`__str__.
		# ``_str`` is a generator and may output:
		# ``None``, which means: "add a line feed and an indentation here"
		# an int, which means: add the int to the indentation level
		# a string, which means: add this string to the output
		yield self.location.source[self.start:self.end].replace("\r\n", " ").replace("\n", " ")

	def eval(self, vars):
		"""
		This evaluates the node.

		This is a generator, which yields the text output of the node. If the
		node returns a value (as most nodes do), this is done as the value of a
		:exc:`StopIteration` exception.
		"""
		yield from ()

	def ul4ondump(self, encoder):
		encoder.dump(self.location)
		encoder.dump(self.start)
		encoder.dump(self.end)

	def ul4onload(self, decoder):
		self.location = decoder.load()
		self.start = decoder.load()
		self.end = decoder.load()

	@classmethod
	def makefunction(cls, f):
		name = f.__name__
		if name.startswith("function_"):
			name = name[9:]
		cls.functions[name] = f
		return f


@register("text")
class Text(AST):
	"""
	AST node for literal text.
	"""

	_re_removewhitespace = re.compile(r"\r?\n\s*")

	def text(self):
		# If ``keepws`` is true, we output the literal text from the location info.
		# Otherwise we have to strip linefeeds and indentation
		text = self.location.code
		if not self.location.root.keepws:
			text = self._re_removewhitespace.sub("", text)
		return text

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {1!r} at {2:#x}>".format(self, self.text(), id(self))

	def _str(self):
		yield "text {!r}".format(self.text())

	def eval(self, vars):
		yield self.text()


@register("const")
class Const(AST):
	"""
	Load a constant
	"""
	ul4attrs = AST.ul4attrs.union({"value"})

	def __init__(self, location=None, start=None, end=None, value=None):
		super().__init__(location, start, end)
		self.value = value

	def eval(self, vars):
		yield from ()
		return self.value

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {0.value!r} at {1:#x}>".format(self, id(self))


@register("list")
class List(AST):
	"""
	AST nodes for loading a list object.
	"""

	ul4attrs = AST.ul4attrs.union({"items"})

	def __init__(self, location=None, start=None, end=None, *items):
		super().__init__(location, start, end)
		self.items = list(items)

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {0.items!r} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				for item in self.items:
					p.breakable()
					p.pretty(item)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		result = []
		for item in self.items:
			item = (yield from item.eval(vars))
			result.append(item)
		return result

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

	ul4attrs = AST.ul4attrs.union({"item", "varname", "container", "condition"})

	def __init__(self, location=None, start=None, end=None, item=None, varname=None, container=None, condition=None):
		super().__init__(location, start, end)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		s = "<{0.__class__.__module__}.{0.__class__.__qualname__} item={0.item!r} varname={0.varname!r} container={0.container!r}".format(self)
		if self.condition is not None:
			s += " condition={0.condition!r}".format(self)
		return s + " at {:#x}>".format(id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("{0.__class__.__module__}.{0.__class__.__qualname__}(...)".format(self))
		else:
			with p.group(4, "{0.__class__.__module__}.{0.__class__.__qualname__}(".format(self), ")"):
				p.breakable("")
				p.text("item=")
				p.pretty(self.item)
				p.text(",")
				p.breakable()
				p.text("varname=")
				p.pretty(self.varname)
				p.text(",")
				p.breakable()
				p.text("container=")
				p.pretty(self.container)
				if self.condition is not None:
					p.text(",")
					p.breakable()
					p.text("condition=")
					p.pretty(self.condition)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		container = (yield from self.container.eval(vars))
		vars = collections.ChainMap({}, vars) # Don't let loop variables leak into the surrounding scope
		result = []
		for item in container:
			for (lvalue, value) in _unpackvar(self.varname, item):
				yield from lvalue.evalsetvar(vars, value)
			if self.condition is None or (yield from self.condition.eval(vars)):
				item = (yield from self.item.eval(vars))
				result.append(item)
		return result

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


@register("set")
class Set(AST):
	"""
	AST nodes for loading a set object.
	"""

	ul4attrs = AST.ul4attrs.union({"items"})

	def __init__(self, location=None, start=None, end=None, *items):
		super().__init__(location, start, end)
		self.items = list(items)

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {0.items!r} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				for item in self.items:
					p.breakable()
					p.pretty(item)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		result = set()
		for item in self.items:
			item = (yield from item.eval(vars))
			result.add(item)
		return result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = decoder.load()


@register("setcomp")
class SetComp(AST):
	"""
	AST node for set comprehension.
	"""

	ul4attrs = AST.ul4attrs.union({"item", "varname", "container", "condition"})

	def __init__(self, location=None, start=None, end=None, item=None, varname=None, container=None, condition=None):
		super().__init__(location, start, end)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		s = "<{0.__class__.__module__}.{0.__class__.__qualname__} item={0.item!r} varname={0.varname!r} container={0.container!r}".format(self)
		if self.condition is not None:
			s += " condition={0.condition!r}".format(self)
		return s + " at {:#x}>".format(id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("{0.__class__.__module__}.{0.__class__.__qualname__}(...)".format(self))
		else:
			with p.group(4, "{0.__class__.__module__}.{0.__class__.__qualname__}(".format(self), ")"):
				p.breakable("")
				p.text("item=")
				p.pretty(self.item)
				p.text(",")
				p.breakable()
				p.text("varname=")
				p.pretty(self.varname)
				p.text(",")
				p.breakable()
				p.text("container=")
				p.pretty(self.container)
				if self.condition is not None:
					p.text(",")
					p.breakable()
					p.text("condition=")
					p.pretty(self.condition)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		container = (yield from self.container.eval(vars))
		vars = collections.ChainMap({}, vars) # Don't let loop variables leak into the surrounding scope
		result = set()
		for item in container:
			for (lvalue, value) in _unpackvar(self.varname, item):
				yield from lvalue.evalsetvar(vars, value)
			if self.condition is None or (yield from self.condition.eval(vars)):
				item = (yield from self.item.eval(vars))
				result.add(item)
		return result

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

	ul4attrs = AST.ul4attrs.union({"items"})

	def __init__(self, location=None, start=None, end=None, *items):
		super().__init__(location, start, end)
		self.items = list(items)

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {0.items!r} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				for item in self.items:
					p.breakable()
					p.pretty(item[0])
					p.text("=")
					p.pretty(item[1])
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		result = {}
		for item in self.items:
			key = (yield from item[0].eval(vars))
			value = (yield from item[1].eval(vars))
			result[key] = value
		return result

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

	ul4attrs = AST.ul4attrs.union({"key", "value", "varname", "container", "condition"})

	def __init__(self, location=None, start=None, end=None, key=None, value=None, varname=None, container=None, condition=None):
		super().__init__(location, start, end)
		self.key = key
		self.value = value
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		s = "<{0.__class__.__module__}.{0.__class__.__qualname__} key={0.key!r} value={0.value!r} varname={0.varname!r} container={0.container!r}".format(self)
		if self.condition is not None:
			s += " {0.condition!r}".format(self)
		return s + " at {:#x}>".format(id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("key=")
				p.pretty(self.key)
				p.breakable()
				p.text("value=")
				p.pretty(self.value)
				p.breakable()
				p.text("varname=")
				p.pretty(self.varname)
				p.breakable()
				p.text("container=")
				p.pretty(self.container)
				if self.condition is not None:
					p.breakable()
					p.text("condition=")
					p.pretty(self.condition)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		container = (yield from self.container.eval(vars))
		vars = collections.ChainMap({}, vars) # Don't let loop variables leak into the surrounding scope
		result = {}
		for item in container:
			for (lvalue, value) in _unpackvar(self.varname, item):
				yield from lvalue.evalsetvar(vars, value)
			if self.condition is None or (yield from self.condition.eval(vars)):
				key = (yield from self.key.eval(vars))
				value = (yield from self.value.eval(vars))
				result[key] = value
		return result

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

	ul4attrs = AST.ul4attrs.union({"item", "varname", "container", "condition"})

	def __init__(self, location=None, start=None, end=None, item=None, varname=None, container=None, condition=None):
		super().__init__(location, start, end)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def __repr__(self):
		s = "<{0.__class__.__module__}.{0.__class__.__qualname__} item={0.item!r} varname={0.varname!r} container={0.container!r}".format(self)
		if self.condition is not None:
			s += " condition={0.condition!r}".format(self)
		return s + " at {:#x}>".format(id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("item=")
				p.pretty(self.item)
				p.breakable()
				p.text("varname=")
				p.pretty(self.varname)
				p.breakable()
				p.text("container=")
				p.pretty(self.container)
				if self.condition is not None:
					p.breakable()
					p.text("condition=")
					p.pretty(self.condition)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		container = (yield from self.container.eval(vars))
		vars = collections.ChainMap({}, vars) # Don't let loop variables leak into the surrounding scope

		def result():
			for item in container:
				for (lvalue, value) in _unpackvar(self.varname, item):
					yield from lvalue.evalsetvar(vars, value)
				if self.condition is None or (yield from self.condition.eval(vars)):
					item = (yield from self.item.eval(vars))
					yield item
		return result()

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

	ul4attrs = AST.ul4attrs.union({"name"})

	def __init__(self, location=None, start=None, end=None, name=None):
		super().__init__(location, start, end)
		self.name = name

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {0.name!r} at {1:#x}>".format(self, id(self))

	@_handleeval
	def eval(self, vars):
		yield from ()
		try:
			return vars[self.name]
		except KeyError:
			try:
				return self.functions[self.name]
			except KeyError:
				return UndefinedVariable(self.name)

	@_handleeval
	def evalsetvar(self, vars, value):
		yield from ()
		vars[self.name] = value

	@_handleeval
	def evalmodifyvar(self, operator, vars, value):
		yield from ()
		vars[self.name] = operator.evalfoldaug(vars[self.name], value)

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

	ul4attrs = AST.ul4attrs.union({"endlocation", "content"})

	def __init__(self, location=None, start=None, end=None):
		super().__init__(location, start, end)
		self.endlocation = None
		self.content = []

	def append(self, item):
		self.content.append(item)

	def _str(self):
		if self.content:
			for node in self.content:
				yield from node._str()
				yield None
		else:
			yield "pass"
			yield None

	@_handleeval
	def eval(self, vars):
		for node in self.content:
			yield from node.eval(vars)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.endlocation)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.endlocation = decoder.load()
		self.content = decoder.load()


@register("condblock")
class CondBlock(Block):
	"""
	AST node for an conditional block.

	The content of the :class:`CondBlock` block is one :class:`IfBlock` block
	followed by zero or more :class:`ElIfBlock` blocks followed by zero or one
	:class:`ElseBlock` block.
	"""
	def __init__(self, location=None, start=None, end=None, condition=None):
		super().__init__(location, start, end)
		if condition is not None:
			self.newblock(IfBlock(location, start, end, condition))

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {1} at {2:#x}>".format(self, repr(self.content)[1:-1], id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				for node in self.content:
					p.breakable()
					p.pretty(node)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	def append(self, item):
		self.content[-1].append(item)

	def newblock(self, block):
		if self.content:
			self.content[-1].endlocation = block.location
		self.content.append(block)

	def _str(self):
		for node in self.content:
			yield from node._str()

	@_handleeval
	def eval(self, vars):
		for node in self.content:
			if isinstance(node, ElseBlock) or (yield from node.condition.eval(vars)):
				yield from node.eval(vars)
				break


@register("ifblock")
class IfBlock(Block):
	"""
	AST node for an ``<?if?>`` block.
	"""

	ul4attrs = Block.ul4attrs.union({"condition"})

	def __init__(self, location=None, start=None, end=None, condition=None):
		super().__init__(location, start, end)
		self.condition = condition

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} condition={0.condition!r} {1} at {2:#x}>".format(self, " ..." if self.content else "", id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("condition=")
				p.pretty(self.condition)
				for node in self.content:
					p.breakable()
					p.pretty(node)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	def _str(self):
		yield "if "
		yield from AST._str(self)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()


@register("elifblock")
class ElIfBlock(Block):
	"""
	AST node for an ``<?elif?>`` block.
	"""

	ul4attrs = Block.ul4attrs.union({"condition"})

	def __init__(self, location=None, start=None, end=None, condition=None):
		super().__init__(location, start, end)
		self.condition = condition

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} condition={0.condition!r} {1} at {2:#x}>".format(self, " ..." if self.content else "", id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("condition=")
				p.pretty(self.condition)
				for node in self.content:
					p.breakable()
					p.pretty(node)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	def _str(self):
		yield "elif "
		yield from AST._str(self)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()


@register("elseblock")
class ElseBlock(Block):
	"""
	AST node for an ``<?else?>`` block.
	"""

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				for node in self.content:
					p.breakable()
					p.pretty(node)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	def _str(self):
		yield "else:"
		yield None
		yield +1
		yield from super()._str()
		yield -1


@register("forblock")
class ForBlock(Block):
	"""
	AST node for a ``<?for?>`` loop.
	"""

	ul4attrs = Block.ul4attrs.union({"varname", "container"})

	def __init__(self, location=None, start=None, end=None, varname=None, container=None):
		super().__init__(location, start, end)
		self.varname = varname
		self.container = container

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} varname={0.varname!r} container={0.container!r} {1} at {2:#x}>".format(self, " ..." if self.content else "", id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("varname=")
				p.pretty(self.varname)
				p.breakable()
				p.text("container=")
				p.pretty(self.container)
				for node in self.content:
					p.breakable()
					p.pretty(node)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.varname)
		encoder.dump(self.container)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.varname = decoder.load()
		self.container = decoder.load()

	def _str(self):
		yield "for "
		yield from AST._str(self)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	@_handleeval
	def eval(self, vars):
		container = (yield from self.container.eval(vars))
		if hasattr(container, "ul4attrs"):
			container = (attrname.lstrip("+") for attrname in container.ul4attrs)
		for item in container:
			for (lvalue, value) in _unpackvar(self.varname, item):
				yield from lvalue.evalsetvar(vars, value)
			try:
				yield from super().eval(vars)
			except BreakException:
				break
			except ContinueException:
				pass


@register("whileblock")
class WhileBlock(Block):
	"""
	AST node for a ``<?while?>`` loop.
	"""

	ul4attrs = Block.ul4attrs.union({"condition"})

	def __init__(self, location=None, start=None, end=None, condition=None):
		super().__init__(location, start, end)
		self.condition = condition

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} condition={0.condition!r} {1} at {2:#x}>".format(self, " ..." if self.content else "", id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("condition=")
				p.pretty(self.condition)
				for node in self.content:
					p.breakable()
					p.pretty(node)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()

	def _str(self):
		yield "while "
		yield from AST._str(self)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	@_handleeval
	def eval(self, vars):
		while 1:
			condition = (yield from self.condition.eval(vars))
			if not condition:
				break
			try:
				yield from super().eval(vars)
			except BreakException:
				break
			except ContinueException:
				pass


@register("break")
class Break(AST):
	"""
	AST node for a ``<?break?>`` inside a ``<?for?>`` block.
	"""

	def _str(self):
		yield "break"

	def eval(self, vars):
		yield from ()
		raise BreakException()


@register("continue")
class Continue(AST):
	"""
	AST node for a ``<?continue?>`` inside a ``<?for?>`` block.
	"""

	def _str(self):
		yield "continue"

	def eval(self, vars):
		yield from ()
		raise ContinueException()


@register("attr")
class Attr(AST):
	"""
	AST node for getting and setting an attribute of an object.

	The object is loaded from the AST node :obj:`obj` and the attribute name
	is stored in the string :obj:`attrname`.
	"""
	ul4attrs = AST.ul4attrs.union({"obj", "attrname"})

	def __init__(self, location=None, start=None, end=None, obj=None, attrname=None):
		super().__init__(location, start, end)
		self.obj = obj
		self.attrname = attrname

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} obj={0.obj!r}, attrname={0.attrname!r} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("obj=")
				p.pretty(self.obj)
				p.breakable()
				p.text("attrname=")
				p.pretty(self.attrname)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		obj = (yield from self.obj.eval(vars))
		if hasattr(obj, "ul4attrs"):
			if self.attrname in {"items", "values"}:
				return self.method_dict(obj, self.attrname)
			elif self.attrname in obj.ul4attrs or "+" + self.attrname in obj.ul4attrs:
				return getattr(obj, self.attrname)
			return UndefinedKey(self.attrname)
		elif isinstance(obj, str):
			return self.method_str(obj, self.attrname)
		elif isinstance(obj, collections.Mapping):
			return self.method_dict(obj, self.attrname)
		elif isinstance(obj, collections.Set):
			return self.method_set(obj, self.attrname)
		elif isinstance(obj, collections.Sequence):
			return self.method_list(obj, self.attrname)
		elif isinstance(obj, (datetime.datetime, datetime.date)):
			return self.method_date(obj, self.attrname)
		elif isinstance(obj, datetime.timedelta):
			return self.method_timedelta(obj, self.attrname)
		else:
			try:
				return obj[self.attrname]
			except KeyError:
				return UndefinedKey(self.attrname)

	def method_str(self, obj, methname):
		if methname == "split":
			def split(sep=None, count=None):
				return obj.split(sep, count if count is not None else -1)
			result = split
		elif methname == "rsplit":
			def rsplit(sep=None, count=None):
				return obj.rsplit(sep, count if count is not None else -1)
			result = rsplit
		elif methname == "strip":
			def strip(chars=None):
				return obj.strip(chars)
			result = strip
		elif methname == "lstrip":
			def lstrip(chars=None):
				return obj.lstrip(chars)
			result = lstrip
		elif methname == "rstrip":
			def rstrip(chars=None):
				return obj.rstrip(chars)
			result = rstrip
		elif methname == "find":
			def find(sub, start=None, end=None):
				return obj.find(sub, start, end)
			result = find
		elif methname == "rfind":
			def rfind(sub, start=None, end=None):
				return obj.rfind(sub, start, end)
			result = rfind
		elif methname == "startswith":
			def startswith(prefix):
				return obj.startswith(prefix)
			result = startswith
		elif methname == "endswith":
			def endswith(suffix):
				return obj.endswith(suffix)
			result = endswith
		elif methname == "upper":
			def upper():
				return obj.upper()
			result = upper
		elif methname == "lower":
			def lower():
				return obj.lower()
			result = lower
		elif methname == "capitalize":
			def capitalize():
				return obj.capitalize()
			result = capitalize
		elif methname == "replace":
			def replace(old, new, count=None):
				if count is None:
					return obj.replace(old, new)
				else:
					return obj.replace(old, new, count)
			result = replace
		elif methname == "join":
			def join(iterable):
				return obj.join(iterable)
			result = join
		else:
			result = UndefinedKey(methname)
		return result

	def method_list(self, obj, methname):
		if methname == "append":
			def append(*items):
				obj.extend(items)
			result = append
		elif methname == "insert":
			def insert(pos, *items):
				obj[pos:pos] = items
			result = insert
		elif methname == "pop":
			def pop(pos=-1):
				return obj.pop(pos)
			result = pop
		elif methname == "find":
			def find(sub, start=None, end=None):
				try:
					if end is None:
						if start is None:
							return obj.index(sub)
						return obj.index(sub, start)
					return obj.index(sub, start, end)
				except ValueError:
					return -1
			result = find
		elif methname == "rfind":
			def rfind(sub, start=None, end=None):
				for i in reversed(range(*slice(start, end).indices(len(obj)))):
					if obj[i] == sub:
						return i
				return -1
			result = rfind
		else:
			result = UndefinedKey(methname)
		return result

	def method_set(self, obj, methname):
		if methname == "add":
			def add(*items):
				obj.update(items)
			result = add
		else:
			result = UndefinedKey(methname)
		return result

	def method_dict(self, obj, methname):
		if methname == "items":
			def items():
				try:
					attrs = obj.ul4attrs
				except AttributeError:
					return obj.items()
				else:
					def iterate(obj):
						for attrname in attrs:
							attrname = attrname.lstrip("+")
							yield (attrname, getattr(obj, attrname, UndefinedKey(attrname)))
					return iterate(obj)
			result = items
		elif methname == "values":
			def values():
				try:
					attrs = obj.ul4attrs
				except AttributeError:
					return obj.values()
				else:
					def iterate(obj):
						for attrname in attrs:
							attrname = attrname.lstrip("+")
							yield getattr(obj, attrname, UndefinedKey(attrname))
					return iterate(obj)
			result = values
		elif methname == "update":
			def update(*others, **kwargs):
				for other in others:
					obj.update(other)
				obj.update(**kwargs)
			result = update
		elif methname == "get":
			def get(key, default=None):
				return obj.get(key, default)
			result = get
		else:
			try:
				result = obj[methname]
			except KeyError:
				result = UndefinedKey(methname)
		return result

	def method_date(self, obj, methname):
		if methname == "weekday":
			def weekday():
				return obj.weekday()
			result = weekday
		elif methname == "week":
			def week(firstweekday=None):
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
			result = week
		elif methname == "day":
			def day():
				return obj.day
			result = day
		elif methname == "month":
			def month():
				return obj.month
			result = month
		elif methname == "year":
			def year():
				return obj.year
			result = year
		elif methname == "hour":
			def hour():
				return obj.hour
			result = hour
		elif methname == "minute":
			def minute():
				return obj.minute
			result = minute
		elif methname == "second":
			def second():
				return obj.second
			result = second
		elif methname == "microsecond":
			def microsecond():
				return obj.microsecond
			result = microsecond
		elif methname == "mimeformat":
			def mimeformat():
				weekdayname = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
				monthname = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
				return "{1}, {0.day:02d} {2:3} {0.year:4} {0.hour:02}:{0.minute:02}:{0.second:02} GMT".format(obj, weekdayname[obj.weekday()], monthname[obj.month])
			result = mimeformat
		elif methname == "isoformat":
			def isoformat():
				result = obj.isoformat()
				suffix = "T00:00:00"
				if result.endswith(suffix):
					return result[:-len(suffix)]
				return result
			result = isoformat
		elif methname == "yearday":
			def yearday():
				return (obj - obj.__class__(obj.year, 1, 1)).days+1
			result = yearday
		else:
			result = UndefinedKey(methname)
		return result

	def method_timedelta(self, obj, methname):
		if methname == "days":
			def days():
				return obj.days
			result = days
		elif methname == "seconds":
			def seconds():
				return obj.seconds
			result = seconds
		elif methname == "microseconds":
			def microseconds():
				return obj.microseconds
			result = microseconds
		else:
			result = UndefinedKey(methname)
		return result

	@_handleeval
	def evalsetvar(self, vars, value):
		obj = (yield from self.obj.eval(vars))
		if hasattr(obj, "ul4attrs"):
			if "+" + self.attrname in obj.ul4attrs:
				setattr(obj, self.attrname, value)
			else:
				raise AttributeError("attribute {!r} is readonly".format(self.attrname))
		else:
			obj[self.attrname] = value

	@_handleeval
	def evalmodifyvar(self, operator, vars, value):
		obj = (yield from self.obj.eval(vars))
		if hasattr(obj, "ul4attrs"):
			if "+" + self.attrname in obj.ul4attrs:
				attr = getattr(obj, self.attrname)
				attr = operator.evalfoldaug(attr, value)
				setattr(obj, self.attrname, attr)
			else:
				raise AttributeError("attribute {!r} is readonly".format(self.attrname))
		else:
			obj[self.attrname] = operator.evalfoldaug(obj[self.attrname], value)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.attrname)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.attrname = decoder.load()


@register("slice")
class Slice(AST):
	"""
	AST node for creating a slice object (used in ``obj[index1:index2]``).

	The start and stop indices are loaded from  the AST nodes :obj:`index1` and
	:obj:`index2`. :obj:`index1` and :obj:`index2` may also be :const:`None`
	(for missing slice indices, which default to the 0 for the start index and
	the length of the sequence for the end index).
	"""

	ul4attrs = AST.ul4attrs.union({"index1", "index2"})

	def __init__(self, location=None, start=None, end=None, index1=None, index2=None):
		super().__init__(location, start, end)
		self.index1 = index1
		self.index2 = index2

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} index1={0.index1!r} index2={0.index2!r} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("index1=")
				p.pretty(self.index1)
				p.breakable()
				p.text("index2=")
				p.pretty(self.index2)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		index1 = None
		if self.index1 is not None:
			index1 = (yield from self.index1.eval(vars))
		index2 = None
		if self.index2 is not None:
			index2 = (yield from self.index2.eval(vars))
		return slice(index1, index2)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.index1)
		encoder.dump(self.index2)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.index1 = decoder.load()
		self.index2 = decoder.load()


class Unary(AST):
	"""
	Base class for all AST nodes implementing unary operators.
	"""

	ul4attrs = AST.ul4attrs.union({"obj"})

	def __init__(self, location=None, start=None, end=None, obj=None):
		super().__init__(location, start, end)
		self.obj = obj

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {0.obj!r} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.pretty(self.obj)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()

	@_handleeval
	def eval(self, vars):
		obj = (yield from self.obj.eval(vars))
		return self.evalfold(obj)

	@classmethod
	def make(cls, location, start, end, obj):
		if isinstance(obj, Const):
			result = cls.evalfold(obj.value)
			if not isinstance(result, Undefined):
				return Const(location, start, end, result)
		return cls(location, start, end, obj)


@register("not")
class Not(Unary):
	"""
	AST node for the unary ``not`` operator.
	"""

	@classmethod
	def evalfold(cls, obj):
		return not obj


@register("neg")
class Neg(Unary):
	"""
	AST node for the unary negation (i.e. "-") operator.
	"""

	@classmethod
	def evalfold(cls, obj):
		return -obj


@register("bitnot")
class BitNot(Unary):
	"""
	AST node for the bitwise not operator.
	"""

	@classmethod
	def evalfold(cls, obj):
		return ~obj


@register("print")
class Print(Unary):
	"""
	AST node for a ``<?print?>`` tag.
	"""

	def _str(self):
		yield "print "
		yield from super()._str()

	@_handleeval
	def eval(self, vars):
		yield _str((yield from self.obj.eval(vars)))


@register("printx")
class PrintX(Unary):
	"""
	AST node for a ``<?printx?>`` tag.
	"""

	def _str(self):
		yield "printx "
		yield from super()._str()

	@_handleeval
	def eval(self, vars):
		yield _xmlescape((yield from self.obj.eval(vars)))


@register("return")
class Return(Unary):
	"""
	AST node for a ``<?return?>`` tag.
	"""

	def _str(self):
		yield "return "
		yield from super()._str()

	@_handleeval
	def eval(self, vars):
		value = (yield from self.obj.eval(vars))
		raise ReturnException(value)


class Binary(AST):
	"""
	Base class for all AST nodes implementing binary operators.
	"""

	ul4attrs = AST.ul4attrs.union({"obj1", "obj2"})

	def __init__(self, location=None, start=None, end=None, obj1=None, obj2=None):
		super().__init__(location, start, end)
		self.obj1 = obj1
		self.obj2 = obj2

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {0.obj1!r} {0.obj2!r} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.pretty(self.obj1)
				p.breakable()
				p.pretty(self.obj2)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj1)
		encoder.dump(self.obj2)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj1 = decoder.load()
		self.obj2 = decoder.load()

	@_handleeval
	def eval(self, vars):
		obj1 = (yield from self.obj1.eval(vars))
		obj2 = (yield from self.obj2.eval(vars))
		return self.evalfold(obj1, obj2)

	@classmethod
	def make(cls, location, start, end, obj1, obj2):
		if isinstance(obj1, Const) and isinstance(obj2, Const):
			result = cls.evalfold(obj1.value, obj2.value)
			if not isinstance(result, Undefined):
				return Const(location, start, end, result)
		return cls(location, start, end, obj1, obj2)


@register("item")
class Item(Binary):
	"""
	AST node for subscripting operator.

	The object (which must be a list, string or dict) is loaded from the AST
	node :obj:`obj1` and the index/key is loaded from the AST node :obj:`obj2`.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		if isinstance(obj2, str) and hasattr(obj1, "ul4attrs"):
			if obj2 in obj1.ul4attrs or "+" + obj2 in obj1.ul4attrs:
				return getattr(obj1, obj2)
			return UndefinedKey(obj2)
		try:
			return obj1[obj2]
		except KeyError:
			return UndefinedKey(obj2)
		except IndexError:
			return UndefinedIndex(obj2)

	@_handleeval
	def evalsetvar(self, vars, value):
		obj1 = (yield from self.obj1.eval(vars))
		obj2 = (yield from self.obj2.eval(vars))
		if isinstance(obj2, str) and hasattr(obj1, "ul4attrs"):
			if "+" + obj2 in obj1.ul4attrs:
				setattr(obj1, obj2, value)
			else:
				raise AttributeError("attribute {!r} is readonly".format(obj2))
		else:
			obj1[obj2] = value

	@_handleeval
	def evalmodifyvar(self, operator, vars, value):
		obj1 = (yield from self.obj1.eval(vars))
		obj2 = (yield from self.obj2.eval(vars))
		if isinstance(obj2, str) and hasattr(obj1, "ul4attrs"):
			if "+" + obj2 in obj1.ul4attrs:
				attr = getattr(obj1, obj2)
				attr = operator.evalfoldaug(attr, value)
				setattr(obj1, obj2, attr)
			else:
				raise AttributeError("attribute {!r} is readonly".format(obj2))
		else:
			obj1[obj2] = operator.evalfoldaug(obj1[obj2], value)


@register("eq")
class EQ(Binary):
	"""
	AST node for the binary ``==`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 == obj2


@register("ne")
class NE(Binary):
	"""
	AST node for the binary ``!=`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 != obj2


@register("lt")
class LT(Binary):
	"""
	AST node for the binary ``<`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 < obj2


@register("le")
class LE(Binary):
	"""
	AST node for the binary ``<=`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 <= obj2


@register("gt")
class GT(Binary):
	"""
	AST node for the binary ``>`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 > obj2


@register("ge")
class GE(Binary):
	"""
	AST node for the binary ``>=`` comparison operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 >= obj2


@register("contains")
class Contains(Binary):
	"""
	AST node for the binary containment testing operator.

	The item/key object is loaded from the AST node :obj:`obj1` and the container
	object (which must be a list, string, dict or an object with a ``ul4attrs``
	attribute) is loaded from the AST node :obj:`obj2`.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		if isinstance(obj1, str) and hasattr(obj2, "ul4attrs"):
			return obj1 in obj2.ul4attrs or "+" + obj1 in obj2.ul4attrs
		else:
			return obj1 in obj2


@register("notcontains")
class NotContains(Binary):
	"""
	AST node for the inverted containment testing operator.

	The item/key object is loaded from the AST node :obj:`obj1` and the container
	object (which must be a list, string, dict or an object with a ``ul4attrs``
	attribute) is loaded from the AST node :obj:`obj2`.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		if isinstance(obj1, str) and hasattr(obj2, "ul4attrs"):
			return obj1 not in obj2.ul4attrs and "+" + obj1 not in obj2.ul4attrs
		else:
			return obj1 not in obj2


@register("add")
class Add(Binary):
	"""
	AST node for the binary addition operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 + obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 += obj2
		return obj1


@register("sub")
class Sub(Binary):
	"""
	AST node for the binary substraction operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 - obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 -= obj2
		return obj1


@register("mul")
class Mul(Binary):
	"""
	AST node for the binary multiplication operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 * obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 *= obj2
		return obj1


@register("floordiv")
class FloorDiv(Binary):
	"""
	AST node for the binary truncating division operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 // obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 //= obj2
		return obj1


@register("truediv")
class TrueDiv(Binary):
	"""
	AST node for the binary true division operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 / obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 /= obj2
		return obj1


@register("mod")
class Mod(Binary):
	"""
	AST node for the binary modulo operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 % obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 %= obj2
		return obj1


@register("shiftleft")
class ShiftLeft(Binary):
	"""
	AST node for the bitwise left shift operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 << obj2 if obj2 >= 0 else obj1 >> -obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		if obj2 >= 0:
			obj1 <<= obj2
		else:
			obj1 >>= -obj2
		return obj1


@register("shiftright")
class ShiftRight(Binary):
	"""
	AST node for the bitwise right shift operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 >> obj2 if obj2 >= 0 else obj1 << -obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		if obj2 >= 0:
			obj1 >>= obj2
		else:
			obj1 <<= -obj2
		return obj1


@register("bitand")
class BitAnd(Binary):
	"""
	AST node for the binary bitwise and operator (``&``).
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		return obj1 & obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		obj1 &= obj2
		return obj1


@register("bitxor")
class BitXOr(Binary):
	"""
	AST node for the binary bitwise exclusive or operator (``^``).
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		return obj1 ^ obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		obj1 ^= obj2
		return obj1


@register("bitor")
class BitOr(Binary):
	"""
	AST node for the binary bitwise or operator (``|``).
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		return obj1 | obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		if isinstance(obj1, bool):
			obj1 = int(obj1)
		if isinstance(obj2, bool):
			obj2 = int(obj2)
		obj1 |= obj2
		return obj1


@register("and")
class And(Binary):
	"""
	AST node for the binary ``and`` operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		# This is not called from ``eval``, as it doesn't short-circuit
		return obj1 and obj2

	@_handleeval
	def eval(self, vars):
		obj1 = (yield from self.obj1.eval(vars))
		if not obj1:
			return obj1
		return (yield from self.obj2.eval(vars))


@register("or")
class Or(Binary):
	"""
	AST node for the binary ``or`` operator.
	"""

	@classmethod
	def evalfold(cls, obj1, obj2):
		# This is not called from ``eval``, as it doesn't short-circuit
		return obj1 or obj2

	@_handleeval
	def eval(self, vars):
		obj1 = (yield from self.obj1.eval(vars))
		if obj1:
			return obj1
		return (yield from self.obj2.eval(vars))


@register("if")
class If(AST):
	"""
	AST node for the ternary inline ``if/else`` operator.
	"""

	def __init__(self, location=None, start=None, end=None, objif=None, objcond=None, objelse=None):
		super().__init__(location, start, end)
		self.objif = objif
		self.objcond = objcond
		self.objelse = objelse

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} {0.objif!r} {0.objcond!r} {0.objelse!r} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.pretty(self.objif)
				p.breakable()
				p.pretty(self.objcond)
				p.breakable()
				p.pretty(self.objelse)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.objif)
		encoder.dump(self.objcond)
		encoder.dump(self.objelse)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.objif = decoder.load()
		self.objcond = decoder.load()
		self.objelse = decoder.load()

	@classmethod
	def make(cls, location, start, end, objif, objcond, objelse):
		if isinstance(objcond, Const) and not isinstance(objcond.value, Undefined):
			return objif if objcond.value else objelse
		return cls(location, start, end, objif, objcond, objelse)

	@_handleeval
	def eval(self, vars):
		objcond = (yield from self.objcond.eval(vars))
		if objcond:
			return (yield from self.objif.eval(vars))
		else:
			return (yield from self.objelse.eval(vars))


class ChangeVar(AST):
	"""
	Baseclass for all AST nodes that store or modify a variable.

	The variable name is stored in the string :obj:`varname` and the value that
	will be stored or be used to modify the stored value is loaded from the
	AST node :obj:`value`.
	"""

	ul4attrs = AST.ul4attrs.union({"varname", "value"})

	def __init__(self, location=None, start=None, end=None, lvalue=None, value=None):
		super().__init__(location, start, end)
		self.lvalue = lvalue
		self.value = value

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} lvalue={0.lvalue!r} value={0.value!r} at {1:#x}>".format(self, id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("lvalue=")
				p.pretty(self.lvalue)
				p.breakable()
				p.text("value=")
				p.pretty(self.value)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.lvalue)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.lvalue = decoder.load()
		self.value = decoder.load()


@register("setvar")
class SetVar(ChangeVar):
	"""
	AST node that stores a value into a variable.
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalsetvar(vars, value)


@register("addvar")
class AddVar(ChangeVar):
	"""
	AST node that adds a value to a variable (i.e. the ``+=`` operator).
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(Add, vars, value)


@register("subvar")
class SubVar(ChangeVar):
	"""
	AST node that substracts a value from a variable (i.e. the ``-=`` operator).
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(Sub, vars, value)


@register("mulvar")
class MulVar(ChangeVar):
	"""
	AST node that multiplies a variable by a value (i.e. the ``*=`` operator).
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(Mul, vars, value)


@register("floordivvar")
class FloorDivVar(ChangeVar):
	"""
	AST node that divides a variable by a value (truncating to an integer value;
	i.e. the ``//=`` operator).
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(FloorDiv, vars, value)


@register("truedivvar")
class TrueDivVar(ChangeVar):
	"""
	AST node that divides a variable by a value (i.e. the ``/=`` operator).
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(TrueDiv, vars, value)


@register("modvar")
class ModVar(ChangeVar):
	"""
	AST node for the ``%=`` operator.
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(Mod, vars, value)


@register("shiftleftvar")
class ShiftLeftVar(ChangeVar):
	"""
	AST node for the ``<<=`` operator.
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(ShiftLeft, vars, value)


@register("shiftrightvar")
class ShiftRightVar(ChangeVar):
	"""
	AST node for the ``>>=`` operator.
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(ShiftRight, vars, value)


@register("bitandvar")
class BitAndVar(ChangeVar):
	"""
	AST node for the ``&=`` operator.
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(BitAnd, vars, value)


@register("bitxorvar")
class BitXOrVar(ChangeVar):
	"""
	AST node for the ``^=`` operator.
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(BitXOr, vars, value)


@register("bitorvar")
class BitOrVar(ChangeVar):
	"""
	AST node for the ``|=`` operator.
	"""

	@_handleeval
	def eval(self, vars):
		value = (yield from self.value.eval(vars))
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			yield from lvalue.evalmodifyvar(BitOr, vars, value)


@register("call")
class Call(AST):
	"""
	AST node for calling an object.

	The object to be called is stored in the attribute :obj:`obj`. The list of
	arguments is found in :obj:`args`.
	"""

	ul4attrs = AST.ul4attrs.union({"obj", "args"})

	def __init__(self, location=None, start=None, end=None, obj=None):
		super().__init__(location, start, end)
		self.obj = obj
		self.args = []

	def __repr__(self):
		args = []
		for (name, arg) in self.args:
			if name is None:
				fmt = " {arg!r}"
			elif argname == "*":
				fmt = " *{arg!r}"
			elif argname == "**":
				fmt = " **{arg!r}"
			else:
				fmt = " {name}={arg!r}"
			args.append(fmt.format(name=name, arg=arg))

		return "<{0.__class__.__module__}.{0.__class__.__qualname__} obj={0.obj!r}{1} at {2:#x}>".format(self, "".join(args), id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("obj=")
				p.pretty(self.obj)
				for (name, arg) in self.args:
					p.breakable()
					if name is None:
						p.pretty(arg)
					elif name in ("*", "**"):
						p.text(name)
						p.pretty(arg)
					else:
						p.text("{}=".format(name))
						p.pretty(arg)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		obj = (yield from self.obj.eval(vars))
		args = []
		kwargs = {}
		for (name, arg) in self.args:
			arg = yield from arg.eval(vars)
			if name is None:
				args.append(arg)
			elif name == "*":
				args.extend(arg)
			elif name == "**":
				kwargs.update(arg)
			else:
				kwargs[name] = arg

		if isinstance(obj, types.MethodType):
			generator = getattr(obj.__func__, "__ul4generator__", False)
		else:
			generator = getattr(obj, "__ul4generator__", False)
		if generator:
			return (yield from obj(*args, **kwargs))
		else:
			return obj(*args, **kwargs)

	@_handleeval
	def evalsetvar(self, vars, value):
		raise TypeError("can't use = on call result")

	@_handleeval
	def evalmodifyvar(self, operator, vars, value):
		raise TypeError("augmented assigment not allowed for call result")

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.args)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.args = [tuple(arg) for arg in decoder.load()]


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

	A :class:`Template` can also be called as a function (returning the result
	of the first ``<?return?>`` tag encountered). In this case all output of the
	template will be ignored.

	A :class:`Template` object is itself an AST node. Evaluating it will store
	the template object under its name in the local variables.
	"""
	ul4attrs = Block.ul4attrs.union({"source", "name", "keepws", "startdelim", "enddelim", "render", "renders"})

	version = "32"

	def __init__(self, source=None, name=None, keepws=True, startdelim="<?", enddelim="?>", signature=None):
		"""
		Create a :class:`Template` object.

		If :obj:`source` is ``None``, the :class:`Template` remains uninitialized,
		otherwise :obj:`source` will be compiled (using :obj:`startdelim` and
		:obj:`enddelim` as the tag delimiters).

		:obj:`name` is the name of the template. It will be used in exception
		messages and should be a valid Python identifier.

		If :obj:`keepws` is false linefeeds and indentation will be ignored in the
		literal text in templates (i.e. the text between the tags). However
		trailing whitespace at the end of the line will be honored regardless of
		the value of :obj:`keepws`. Output will always be ignored when calling
		a template as a function.

		:obj:`signature` is the signature of the template. For a top level
		template it can be:

			``None``
				The template will accept all keyword arguments.

			An :class:`inspect.Signature` object
				This signature will be used as the signature of the template.

			A callable
				The signature of the callable will be used.

			A string
				The signature as a string, i.e. something like
				``"x, y=[42], *args, **kwargs"``. This string will be parsed and
				evaluated to create the signature for the template.

		If the template is a subtemplate (i.e. a template defined by another
		template via ``<?def t?>...<?end def?>``), :obj:`signature` can be:

			``None``
				The template will accept all arguments.

			A :class:`Signature` object
				This AST node will be evaluated at the point of definition of the
				subtemplate to create to final signature of the subtemplate.
		"""
		# ``location``/``endlocation`` will remain ``None`` for a top level template
		# For a subtemplate/subfunction ``location`` will be set to the location of the ``<?def?>`` tag in :meth:`_compile`
		# and ``endlocation`` will be the location of the ``<?end def?>`` tag
		super().__init__(None, 0, 0)
		self.keepws = keepws
		self.startdelim = startdelim or "<?"
		self.enddelim = enddelim or "?>"
		self.name = name
		self.source = None
		if callable(signature):
			signature = inspect.signature(signature)
		elif isinstance(signature, str):
			signature = "({})".format(signature)
			location = Location(self, signature, None, 0, len(signature), 0, len(signature))
			ast = self._parsesignature(location)
			signature = _resultfromgenerator(ast.eval({}))
		self.signature = signature

		# If we have source code compile it
		if source is not None:
			self._compile(source, name, startdelim, enddelim)

	def __repr__(self):
		s = "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} keepws={0.keepws!r}".format(self)
		if self.startdelim != "<?":
			s += " startdelim={0.startdelim!r}".format(self)
		if self.enddelim != "?>":
			s += " enddelim={0.enddelim!r}".format(self)
		if self.signature is not None:
			s += " {}".format(self.signature)
		if self.content:
			s + " ..."
		return s + " at {:#x}>".format(id(self))

	def _str(self):
		yield "def "
		yield self.name if self.name is not None else "unnamed"
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("name=")
				p.pretty(self.name)
				p.breakable()
				p.text("keepws=")
				p.pretty(self.keepws)
				if self.startdelim != "<?":
					p.breakable()
					p.text("startdelim=")
					p.pretty(self.startdelim)
				if self.enddelim != "?>":
					p.breakable()
					p.text("enddelim=")
					p.pretty(self.enddelim)
				if self.signature is not None:
					p.breakable()
					if isinstance(self.signature, Signature):
						p.text("signature=")
						p.pretty(self.signature)
					else:
						p.text("signature={}".format(self.signature))
				for node in self.content:
					p.breakable()
					p.pretty(node)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

				# for item in self.items:
				# 	p.breakable()
				# 	p.pretty(item)
				# p.breakable()

	def ul4ondump(self, encoder):
		# Don't call ``super().ul4ondump()`` first, as we want the version to be first
		encoder.dump(self.version)
		encoder.dump(self.source)
		encoder.dump(self.name)
		encoder.dump(self.keepws)
		encoder.dump(self.startdelim)
		encoder.dump(self.enddelim)

		# Signature can be ``None`` or an instance of :class:`inspect.Signature` or :class:`Signature`
		if self.signature is None or isinstance(self.signature, Signature):
			encoder.dump(self.signature)
		else:
			# Serialize an instance of :class:`inspect.Signature` as a flat list
			# e.g. ['x', 'y=', 42, '*args', '**kwargs'] for the signature ``(x, y=42, *args, **kwargs)``
			dump = []
			for param in self.signature.parameters.values():
				if param.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD:
					if param.default is inspect.Parameter.empty:
						dump.append(param.name)
					else:
						dump.append(param.name + "=")
						dump.append(param.default)
				elif param.kind is inspect.Parameter.VAR_POSITIONAL:
					dump.append("*" + param.name)
				elif param.kind is inspect.Parameter.VAR_KEYWORD:
					dump.append("**" + param.name)
				else:
					raise ValueError("can dump parameter {} of type {}".format(param.name, param.kind))
			encoder.dump(dump)

		super().ul4ondump(encoder)

	def ul4onload(self, decoder):
		version = decoder.load()
		if version != self.version:
			raise ValueError("invalid version, expected {!r}, got {!r}".format(self.version, version))
		self.source = decoder.load()
		self.name = decoder.load()
		self.keepws = decoder.load()
		self.startdelim = decoder.load()
		self.enddelim = decoder.load()

		dump = decoder.load()
		if dump is None or isinstance(dump, Signature):
			self.signature = dump
		else:
			params = []
			nextdefault = False
			paramname = None
			for param in dump:
				if nextdefault:
					params.append(inspect.Parameter(paramname, inspect.Parameter.POSITIONAL_OR_KEYWORD, default=param))
					nextdefault = False
				else:
					if param.endswith("="):
						paramname = param[:-1]
						nextdefault = True # The next item is the default value
					elif param.startswith("**"):
						params.append(inspect.Parameter(param[2:], inspect.Parameter.VAR_KEYWORD))
					elif param.startswith("*"):
						params.append(inspect.Parameter(param[1:], inspect.Parameter.VAR_POSITIONAL))
					else:
						params.append(inspect.Parameter(param, inspect.Parameter.POSITIONAL_OR_KEYWORD))
			self.signature = inspect.Signature(params)
		super().ul4onload(decoder)

	@classmethod
	def loads(cls, data):
		"""
		The class method :meth:`loads` loads the template/function from string
		:obj:`data`. :obj:`data` must contain the template/function in compiled
		UL4ON format.
		"""
		from ll import ul4on
		return ul4on.loads(data)

	@classmethod
	def load(cls, stream):
		"""
		The class method :meth:`load` loads the template/function from the stream
		:obj:`stream`. The stream must contain the template/function in compiled
		UL4ON format.
		"""
		from ll import ul4on
		return ul4on.load(stream)

	def dump(self, stream):
		"""
		:meth:`dump` dumps the template/function in compiled UL4ON format to the
		stream :obj:`stream`.
		"""
		from ll import ul4on
		ul4on.dump(self, stream)

	def dumps(self):
		"""
		:meth:`dumps` returns the template/function in compiled UL4ON format
		(as a string).
		"""
		from ll import ul4on
		return ul4on.dumps(self)

	def _renderbound(self, vars):
		# Helper method used by :meth:`render` and :meth:`TemplateClosure.render` where arguments have already been bound
		try:
			yield from super().eval(vars) # Bypass ``self.eval()`` which simply stores the object as a local variable
		except ReturnException:
			pass

	@generator
	def render(self, *args, **kwargs):
		"""
		Render the template iteratively (i.e. this is a generator).
		:obj:`args` and :obj:`kwargs` contain the top level variables available
		to the template code.
		"""
		vars = _makevars(self.signature, args, kwargs)
		return self._renderbound(vars)

	def _rendersbound(self, vars):
		# Helper method used by :meth:`renders` and :meth:`TemplateClosure.renders` where arguments have already been bound
		try:
			return "".join(self._renderbound(vars))
		except ReturnException:
			pass

	def renders(self, *args, **kwargs):
		"""
		Render the template as a string. :obj:`vars` contains the top level
		variables available to the template code.
		"""
		vars = _makevars(self.signature, args, kwargs)
		return self._rendersbound(vars)

	def _callbound(self, vars):
		# Helper method used by :meth:`__call__` and :meth:`TemplateClosure.__call__` where arguments have already been bound
		try:
			for output in super().eval(vars): # Bypass ``self.eval()`` which simply stores the object as a local variable
				pass # Ignore all output
		except ReturnException as ex:
			return ex.value

	def __call__(self, *args, **kwargs):
		"""
		Call the template as a function and return the resulting value.
		:obj:`vars` contains the top level variables available to the template code.
		"""
		vars = _makevars(self.signature, args, kwargs)
		return self._callbound(vars)

	def jssource(self):
		"""
		Return the template as the source code of a Javascript function.
		"""
		return "ul4.Template.loads({})".format(_asjson(self.dumps()))

	def javasource(self):
		"""
		Return the template as Java source code.
		"""
		from ll import misc
		return "com.livinglogic.ul4.InterpretedTemplate.loads({})".format(misc.javaexpr(self.dumps()))

	def _tokenize(self, source, startdelim, enddelim):
		"""
		Tokenize the template/function source code :obj:`source` into tags and
		non-tag text. :obj:`startdelim` and :obj:`enddelim` are used as the tag
		delimiters.

		This is a generator which produces :class:`Location` objects for each tag
		or non-tag text. It will be called by :meth:`_compile` internally.
		"""
		pattern = "{}(printx|print|code|for|while|if|elif|else|end|break|continue|def|return|note)(\s*((.|\\n)*?)\s*)?{}".format(re.escape(startdelim), re.escape(enddelim))
		pos = 0
		for match in re.finditer(pattern, source):
			if match.start() != pos:
				yield Location(self, source, None, pos, match.start(), pos, match.start())
			type = source[match.start(1):match.end(1)]
			if type != "note":
				yield Location(self, source, type, match.start(), match.end(), match.start(3), match.end(3))
			pos = match.end()
		end = len(source)
		if pos != end:
			yield Location(self, source, None, pos, end, pos, end)

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

	def _parsesignature(self, location):
		return self._parser(location, "unused").signature()

	def _compile(self, source, name, startdelim, enddelim):
		"""
		Compile the template source code :obj:`source` into an AST.
		:obj:`startdelim` and :obj:`enddelim` are used as the tag delimiters.
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

		def parsedef(location):
			return self._parser(location, "definition required").definition()

		for location in self._tokenize(source, startdelim, enddelim):
			try:
				if location.type is None:
					stack[-1].append(Text(location, location.startcode, location.endcode))
				elif location.type == "print":
					stack[-1].append(Print(location, location.startcode, location.endcode, parseexpr(location)))
				elif location.type == "printx":
					stack[-1].append(PrintX(location, location.startcode, location.endcode, parseexpr(location)))
				elif location.type == "code":
					stack[-1].append(parsestmt(location))
				elif location.type == "if":
					block = CondBlock(location, location.startcode, location.endcode, parseexpr(location))
					stack[-1].append(block)
					stack.append(block)
				elif location.type == "elif":
					if not isinstance(stack[-1], CondBlock):
						raise BlockError("elif doesn't match and if")
					elif isinstance(stack[-1].content[-1], ElseBlock):
						raise BlockError("else already seen in if")
					stack[-1].newblock(ElIfBlock(location, location.startcode, location.endcode, parseexpr(location)))
				elif location.type == "else":
					if not isinstance(stack[-1], CondBlock):
						raise BlockError("else doesn't match any if")
					elif isinstance(stack[-1].content[-1], ElseBlock):
						raise BlockError("else already seen in if")
					stack[-1].newblock(ElseBlock(location, location.startcode, location.endcode))
				elif location.type == "end":
					if len(stack) <= 1:
						raise BlockError("not in any block")
					code = location.code
					if code:
						if code == "if":
							if not isinstance(stack[-1], CondBlock):
								raise BlockError("endif doesn't match any if")
						elif code == "for":
							if not isinstance(stack[-1], ForBlock):
								raise BlockError("endfor doesn't match any for")
						elif code == "while":
							if not isinstance(stack[-1], WhileBlock):
								raise BlockError("endwhile doesn't match any while")
						elif code == "def":
							if not isinstance(stack[-1], Template):
								raise BlockError("enddef doesn't match any def")
						else:
							raise BlockError("illegal end value {!r}".format(code))
					last = stack.pop()
					# Set ``endlocation`` of block
					last.endlocation = location
					if isinstance(last, CondBlock):
						last.content[-1].endlocation = location
				elif location.type == "for":
					block = parsefor(location)
					stack[-1].append(block)
					stack.append(block)
				elif location.type == "while":
					block = WhileBlock(location, location.startcode, location.endcode, parseexpr(location))
					stack[-1].append(block)
					stack.append(block)
				elif location.type == "break":
					for block in reversed(stack):
						if isinstance(block, (ForBlock, WhileBlock)):
							break
						elif isinstance(block, Template):
							raise BlockError("break outside of for loop")
					stack[-1].append(Break(location, location.startcode, location.endcode))
				elif location.type == "continue":
					for block in reversed(stack):
						if isinstance(block, (ForBlock, WhileBlock)):
							break
						elif isinstance(block, Template):
							raise BlockError("continue outside of for loop")
					stack[-1].append(Continue(location, location.startcode, location.endcode))
				elif location.type == "def":
					(name, signature) = parsedef(location)
					block = Template(None, name, keepws=self.keepws, startdelim=self.startdelim, enddelim=self.enddelim, signature=signature)
					block.location = location # Set start ``location`` of sub template
					block.source = self.source # The source of the top level template (so that the offsets in :class:`Location` are correct)
					block.start = location.startcode
					block.end = location.endcode
					stack[-1].append(block)
					stack.append(block)
				elif location.type == "return":
					stack[-1].append(Return(location, location.startcode, location.endcode, parseexpr(location)))
				else: # Can't happen
					raise ValueError("unknown tag {!r}".format(location.type))
			except Exception as exc:
				try:
					raise Error(location) from exc
				except Error as exc:
					raise Error(self) from exc
		if len(stack) > 1:
			raise Error(stack[-1]) from BlockError("block unclosed")

	@_handleeval
	def eval(self, vars):
		signature = self.signature
		# If our signature is an AST, we have the evaluate it to get the final :class:`inspect.Signature` object
		if isinstance(signature, Signature):
			signature = yield from signature.eval(vars)
		vars[self.name] = TemplateClosure(self, vars, signature)


###
### Functions
###

@register("signature")
class Signature(AST):
	"""
	AST node for the signature of a template.

	The list of arguments is found in :obj:`params`.
	"""

	ul4attrs = AST.ul4attrs.union({"params"})

	def __init__(self, location=None, start=None, end=None):
		super().__init__(location, start, end)
		self.params = []

	def __repr__(self):
		params = []
		for (paramname, default) in self.params:
			if default is None:
				fmt = " {paramname}"
			else:
				fmt = " {paramname}={default!r}"
			params.append(fmt.format(paramname=paramname, default=default))

		return "<{0.__class__.__module__}.{0.__class__.__qualname__}{1} at {2:#x}>".format(self, "".join(params), id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				for (paramname, default) in self.params:
					p.breakable()
					if default is None:
						p.text(paramname)
					else:
						p.text("{}=".format(paramname))
						p.pretty(default)
				p.breakable()
				p.text("at {:#x}".format(id(self)))

	@_handleeval
	def eval(self, vars):
		params = []
		for (paramname, default) in self.params:
			if default is None:
				if paramname.startswith("**"):
					paramname = paramname[2:]
					kind = inspect.Parameter.VAR_KEYWORD
				elif paramname.startswith("*"):
					paramname = paramname[1:]
					kind = inspect.Parameter.VAR_POSITIONAL
				else:
					kind = inspect.Parameter.POSITIONAL_OR_KEYWORD
				default = inspect.Parameter.empty
			else:
				kind = inspect.Parameter.POSITIONAL_OR_KEYWORD
				default = yield from default.eval(vars)
			params.append(inspect.Parameter(paramname, kind, default=default))
		return inspect.Signature(params)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		dump = []
		for (paramname, default) in self.params:
			if default is None:
				dump.append(paramname)
			else:
				dump.append([paramname, default])
		encoder.dump(dump)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		dump = decoder.load()
		for param in dump:
			if isinstance(param, str):
				self.params.append((param, None))
			else:
				self.params.append(param)


###
### Functions
###

@AST.makefunction
@generator
def function_print(*values):
	for (i, value) in enumerate(values):
		if i:
			yield " "
		yield _str(value)


@AST.makefunction
@generator
def function_printx(*values):
	for (i, value) in enumerate(values):
		if i:
			yield " "
		yield _xmlescape(value)


@AST.makefunction
def function_str(obj=""):
	return _str(obj)


@AST.makefunction
def function_repr(obj):
	return _repr(obj)


@AST.makefunction
def function_now():
	return datetime.datetime.now()


AST.makefunction(datetime.datetime.utcnow)


@AST.makefunction
def function_date(year, month, day, hour=0, minute=0, second=0, microsecond=0):
	return datetime.datetime(year, month, day, hour, minute, second, microsecond)


@AST.makefunction
def function_timedelta(days=0, seconds=0, microseconds=0):
	return datetime.timedelta(days, seconds, microseconds)


@AST.makefunction
def function_monthdelta(months=0):
	from ll import misc
	return misc.monthdelta(months)


AST.makefunction(random.random)


@AST.makefunction
def function_xmlescape(obj):
	return _xmlescape(obj)


@AST.makefunction
def function_csv(obj):
	if obj is None:
		return ""
	elif isinstance(obj, Undefined):
		return ""
	elif not isinstance(obj, str):
		obj = _repr(obj)
	if any(c in obj for c in ',"\n'):
		return '"{}"'.format(obj.replace('"', '""'))
	return obj


@AST.makefunction
def function_asjson(obj):
	return _asjson(obj)


@AST.makefunction
def function_fromjson(string):
	return json.loads(string)


@AST.makefunction
def function_asul4on(obj):
	from ll import ul4on
	return ul4on.dumps(obj)


@AST.makefunction
def function_fromul4on(string):
	from ll import ul4on
	return ul4on.loads(string)


@AST.makefunction
def function_int(obj=0, base=None):
	if base is None:
		return int(obj)
	else:
		return int(obj, base)


@AST.makefunction
def function_float(obj=0.0):
	return float(obj)


@AST.makefunction
def function_bool(obj=False):
	return bool(obj)


@AST.makefunction
def function_list(iterable=()):
	return list(iterable)


@AST.makefunction
def function_set(iterable=()):
	return set(iterable)


@AST.makefunction
def function_len(sequence):
	return len(sequence)


@AST.makefunction
def function_abs(number):
	return abs(number)


@AST.makefunction
def function_any(iterable):
	return any(iterable)


@AST.makefunction
def function_all(iterable):
	return all(iterable)


AST.makefunction(enumerate)


@AST.makefunction
def function_enumfl(iterable, start=0):
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


@AST.makefunction
def function_isfirstlast(iterable):
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


@AST.makefunction
def function_isfirst(iterable):
	first = True
	for item in iterable:
		yield (first, item)
		first = False


@AST.makefunction
def function_islast(iterable):
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


@AST.makefunction
def function_isundefined(obj):
	return isinstance(obj, Undefined)


@AST.makefunction
def function_isdefined(obj):
	return not isinstance(obj, Undefined)


@AST.makefunction
def function_isnone(obj):
	return obj is None


@AST.makefunction
def function_isstr(obj):
	return isinstance(obj, str)


@AST.makefunction
def function_isint(obj):
	return isinstance(obj, int) and not isinstance(obj, bool)


@AST.makefunction
def function_isfloat(obj):
	return isinstance(obj, float)


@AST.makefunction
def function_isbool(obj):
	return isinstance(obj, bool)


@AST.makefunction
def function_isdate(obj):
	return isinstance(obj, (datetime.datetime, datetime.date))


@AST.makefunction
def function_istimedelta(obj):
	return isinstance(obj, datetime.timedelta)


@AST.makefunction
def function_ismonthdelta(obj):
	from ll import misc
	return isinstance(obj, misc.monthdelta)


@AST.makefunction
def function_islist(obj):
	from ll import color
	return isinstance(obj, collections.Sequence) and not isinstance(obj, str) and not isinstance(obj, color.Color)


@AST.makefunction
def function_isset(obj):
	from ll import color
	return isinstance(obj, (set, frozenset))


@AST.makefunction
def function_isdict(obj):
	return isinstance(obj, collections.Mapping) and not isinstance(obj, Template)


@AST.makefunction
def function_iscolor(obj):
	from ll import color
	return isinstance(obj, color.Color)


@AST.makefunction
def function_istemplate(obj):
	return isinstance(obj, (Template, TemplateClosure))


@AST.makefunction
def function_isfunction(obj):
	return callable(obj)


@AST.makefunction
def function_chr(i):
	return chr(i)


@AST.makefunction
def function_ord(c):
	return ord(c)


@AST.makefunction
def function_hex(number):
	return hex(number)


@AST.makefunction
def function_oct(number):
	return oct(number)


@AST.makefunction
def function_bin(number):
	return bin(number)


@AST.makefunction
def function_min(*args):
	return min(*args)


@AST.makefunction
def function_max(*args):
	return max(*args)


@AST.makefunction
def function_first(iterable, default=None):
	from ll import misc
	return misc.first(iterable, default)


@AST.makefunction
def function_last(iterable, default=None):
	from ll import misc
	return misc.last(iterable, default)


@AST.makefunction
def function_sum(iterable, start=0):
	return sum(iterable, start)


@AST.makefunction
def function_sorted(iterable):
	return sorted(iterable)


@AST.makefunction
def function_range(*args):
	return range(*args)


@AST.makefunction
def function_slice(*args):
	return itertools.islice(*args)


@AST.makefunction
def function_type(obj):
	from ll import color, misc
	if obj is None:
		return "none"
	elif isinstance(obj, Undefined):
		return "undefined"
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
	elif isinstance(obj, (Template, TemplateClosure)):
		return "template"
	elif isinstance(obj, collections.Mapping):
		return "dict"
	elif isinstance(obj, color.Color):
		return "color"
	elif isinstance(obj, collections.Sequence):
		return "list"
	elif callable(obj):
		return "function"
	return None


@AST.makefunction
def function_reversed(sequence):
	return reversed(sequence)


@AST.makefunction
def function_randrange(*args):
	return random.randrange(*args)


@AST.makefunction
def function_randchoice(sequence):
	return random.choice(sequence)


@AST.makefunction
def function_format(obj, fmt, lang=None):
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


@AST.makefunction
def function_zip(*iterables):
	return zip(*iterables)


@AST.makefunction
def function_urlquote(string):
	return urlparse.quote_plus(string)


@AST.makefunction
def function_urlunquote(string):
	return urlparse.unquote_plus(string)


@AST.makefunction
def function_rgb(r, g, b, a=1.0):
	from ll import color
	return color.Color.fromrgb(r, g, b, a)


@AST.makefunction
def function_hls(h, l, s, a=1.0):
	from ll import color
	return color.Color.fromhls(h, l, s, a)


@AST.makefunction
def function_hsv(h, s, v, a=1.0):
	from ll import color
	return color.Color.fromhsv(h, s, v, a)


@AST.makefunction
def function_round(x, digits=0):
	result = round(x, digits)
	if digits <= 0:
		result = int(result)
	return result


@AST.makefunction
def function_floor(x, digits=0):
	if digits:
		threshhold = 10**digits
		result = math.floor(x*threshhold)/threshhold
		if digits < 0:
			return int(result)
		return result
	else:
		return math.floor(x)


@AST.makefunction
def function_ceil(x, digits=0):
	if digits:
		threshhold = 10**digits
		result = math.ceil(x*threshhold)/threshhold
		if digits < 0:
			return int(result)
		return result
	else:
		return math.ceil(x)


AST.functions["pi"] = math.pi
AST.functions["tau"] = 2*math.pi


@AST.makefunction
def function_sqrt(x):
	return math.sqrt(x)


@AST.makefunction
def function_cos(x):
	return math.cos(x)


@AST.makefunction
def function_sin(x):
	return math.sin(x)


@AST.makefunction
def function_tan(x):
	return math.tan(x)


@AST.makefunction
def function_exp(x):
	return math.exp(x)


@AST.makefunction
def function_log(x, base=None):
	if base is None:
		return math.log(x)
	else:
		return math.log(x, base)


@AST.makefunction
def function_pow(x, y):
	return math.pow(x, y)


class TemplateClosure:
	ul4attrs = {"location", "endlocation", "name", "source", "startdelim", "enddelim", "signature", "content", "render", "renders"}

	def __init__(self, template, vars, signature):
		self.template = template
		# Freeze variables of the currently running templates/functions
		self.vars = vars.copy()
		self.signature = signature

	@generator
	def render(self, *args, **kwargs):
		vars = _makevars(self.signature, args, kwargs)
		# Call :meth:`_renderbound` to bypass binding the arguments again
		# (which wouldn't work anyway as ``self.template.signature`` is an :class:`AST` object)
		yield from self.template._renderbound(collections.ChainMap(vars, self.vars))

	def renders(self, *args, **kwargs):
		vars = _makevars(self.signature, args, kwargs)
		# Call :meth:`_rendersbound` to bypass binding the arguments again
		# (which wouldn't work anyway as ``self.template.signature`` is an :class:`AST` object)
		return self.template._rendersbound(collections.ChainMap(vars, self.vars))

	def __call__(self, *args, **kwargs):
		vars = _makevars(self.signature, args, kwargs)
		# Call :meth:`_callbound` to bypass binding the arguments again
		# (which wouldn't work anyway as ``self.template.signature`` is an :class:`AST` object)
		return self.template._callbound(collections.ChainMap(vars, self.vars))

	def __getattr__(self, name):
		return getattr(self.template, name)

	def __repr__(self):
		s = "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} keepws={0.keepws!r}".format(self)
		if self.startdelim != "<?":
			s += " startdelim={0.startdelim!r}".format(self)
		if self.enddelim != "?>":
			s += " enddelim={0.enddelim!r}".format(self)
		if self.signature is not None:
			s += " {}".format(self.signature)
		if self.content:
			s + " ..."
		return s + " at {:#x}>".format(id(self))

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("<{0.__class__.__module__}.{0.__class__.__qualname__} ... at {1:#x}>".format(self, id(self)))
		else:
			with p.group(4, "<{0.__class__.__module__}.{0.__class__.__qualname__}".format(self), ">"):
				p.breakable()
				p.text("name=")
				p.pretty(self.name)
				p.breakable()
				p.text("keepws=")
				p.pretty(self.keepws)
				if self.startdelim != "<?":
					p.breakable()
					p.text("startdelim=")
					p.pretty(self.startdelim)
				if self.enddelim != "?>":
					p.breakable()
					p.text("enddelim=")
					p.pretty(self.enddelim)
				if self.signature is not None:
					p.breakable()
					p.text("signature={}".format(self.signature))
				for node in self.content:
					p.breakable()
					p.pretty(node)
				p.breakable()
				p.text("at {:#x}".format(id(self)))
