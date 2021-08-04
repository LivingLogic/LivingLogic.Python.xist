# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2009-2021 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2021 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`!ll.ul4c` provides templating for XML/HTML as well as any other text-based
format. A template defines placeholders for data output and basic logic (like
loops and conditional blocks), that define how the final rendered output will
look.

:mod:`!ll.ul4c` compiles a template to an internal format, which makes it
possible to implement template renderers in multiple programming languages.
"""


__docformat__ = "reStructuredText"


import re, os.path, datetime, urllib.parse as urlparse, json, collections
import locale, itertools, random, functools, math, inspect, contextlib
import types, textwrap

from collections import abc

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


def withcontext(f):
	"""
	Normally when a function is exposed to UL4 this function will be called
	directly.

	However when the function needs access to the rendering context (i.e. the
	local variables or information about the call stack), the function must have
	an additional first parameter, and UL4 must be told that this parmeter is
	required.

	This can be done with this decorator.
	"""
	f.ul4_context = True
	return f


def _create_module(name, doc, **attrs):
	module = types.ModuleType(name, doc)
	module.ul4_attrs = {"__name__", "__doc__"}
	for (attrname, attrvalue) in attrs.items():
		setattr(module, attrname, attrvalue)
		module.ul4_attrs.add(attrname)
	return module


error_underline = os.environ.get("LL_UL4_ERRORUNDERLINE", "~")[:1] or "~"


###
### Exceptions
###

class LocationError(Exception):
	"""
	Exception class that provides a location inside an UL4 template.

	If an exception happens inside an UL4 template, this exception will propagate
	outwards and will be decorated with :class:`LocationError` instances which
	will be chained via the ``__cause__`` attribute. Only the original exception
	will be reraised again and again, so these :class:`LocationError` will never
	have a traceback attached to them.

	The first ``__cause__`` attribute marks the location in the UL4 source where
	the exception happened and the last ``__cause__`` attribute at the end of the
	exception chain marks the outermost call.
	"""
	def __init__(self, location):
		self.location = location

	_condensewhitespace = re.compile("[\t\n\r\f\v]+")

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} in {self.location} offset {_offset(self.location.pos)} at {id(self):#x}>"

	def strtemplate(self):
		template = self.location.template
		prefix = "in local template" if template.parenttemplate is not None else "in template"
		out = []
		while template is not None:
			out.append(repr(template.name) if template.name is not None else "(unnamed)")
			template = template.parenttemplate
		return f"{prefix} {' in '.join(out)}"

	def strlocation(self):
		loc = self.location
		return f"offset {_offset(loc.startpos)}; line {loc.startline:,}; col {loc.startcol:,}"

	def __str__(self):
		prefix = repr(self._condensewhitespace.sub(" ", self.location.startsourceprefix))[1:-1]
		source = repr(self._condensewhitespace.sub(" ", self.location.startsource))[1:-1]
		suffix = repr(self._condensewhitespace.sub(" ", self.location.startsourcesuffix))[1:-1]
		indent = ' '*len(prefix)
		underline = error_underline*len(source)

		return f"{self.strtemplate()}: {self.strlocation()}\n{prefix}{source}{suffix}\n{indent}{underline}"

	def ul4_getattr(self, name):
		if name == "context":
			if self.__context__ is not None and not self.__suppress_context__:
				return self.__context__
			elif self.__cause__ is not None:
				return self.__cause__
			return None
		elif name == "location":
			return self.location
		else:
			raise AttributeError(name)


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


class Context:
	"""
	A :class:`Context` object stores the context of a call to a template. This
	consists of local, global and builtin variables and the indent stack.
	"""

	# "Builtin" functions, types and modules. Will be exposed to UL4 code
	builtins = {}

	def __init__(self, globals=None):
		self._globals = globals if globals is not None else {}
		if not self.builtins:
			self.add_builtins()
		self.vars = collections.ChainMap({}, self.globals, self.builtins)
		self.indents = [] # Stack of additional indentations for the ``<?render?>`` tag
		self.escapes = [] # Stack of functions for escaping the output
		self.asts = [] # Call stack (of :class:`AST` objects)

	@property
	def globals(self):
		return self._globals

	@globals.setter
	def globals(self, vars):
		self.vars.maps[-2] = self._globals = vars

	@classmethod
	def add_builtins(cls):
		from ll import misc, color, ul4on

		b = cls.builtins

		if not b:
			b["repr"] = _repr
			b["ascii"] = _ascii
			b["now"] = _now
			b["today"] = datetime.date.today
			b["utcnow"] = datetime.datetime.utcnow
			b["random"] = random.random
			b["xmlescape"] = _xmlescape
			b["csv"] = _csv
			b["asjson"] = _asjson
			b["fromjson"] = _fromjson
			b["asul4on"] = ul4on.dumps
			b["fromul4on"] = _fromul4on
			b["len"] = len
			b["abs"] = abs
			b["any"] = any
			b["all"] = all
			b["enumerate"] = enumerate
			b["enumfl"] = _enumfl
			b["isfirst"] = misc.isfirst
			b["islast"] = misc.islast
			b["isfirstlast"] = misc.isfirstlast
			b["isundefined"] = _isundefined
			b["isdefined"] = _isdefined
			b["isnone"] = _isnone
			b["isstr"] = _isstr
			b["isint"] = _isint
			b["isfloat"] = _isfloat
			b["isbool"] = _isbool
			b["isdate"] = _isdate
			b["isdatetime"] = _isdatetime
			b["istimedelta"] = _istimedelta
			b["ismonthdelta"] = _ismonthdelta
			b["isexception"] = _isexception
			b["isinstance"] = _isinstance
			b["islist"] = _islist
			b["isset"] = _isset
			b["isdict"] = _isdict
			b["iscolor"] = _iscolor
			b["istemplate"] = _istemplate
			b["isfunction"] = _isfunction
			b["chr"] = chr
			b["ord"] = ord
			b["hex"] = hex
			b["oct"] = oct
			b["bin"] = bin
			b["min"] = _min
			b["max"] = _max
			b["first"] = misc.first
			b["last"] = misc.last
			b["sum"] = sum
			b["sorted"] = _sorted
			b["range"] = range
			b["slice"] = itertools.islice
			b["type"] = _type
			b["reversed"] = reversed
			b["randrange"] = _randrange
			b["randchoice"] = random.choice
			b["format"] = _format
			b["zip"] = zip
			b["urlquote"] = _urlquote
			b["urlunquote"] = _urlunquote
			b["rgb"] = color.Color.fromrgb
			b["hls"] = color.Color.fromhls
			b["hsv"] = color.Color.fromhsv
			b["md5"] = _md5
			b["scrypt"] = _scrypt
			b["round"] = _round
			b["floor"] = _floor
			b["ceil"] = _ceil
			b["exp"] = math.exp
			b["log"] = math.log
			b["pow"] = math.pow
			b["getattr"] = _getattr
			b["setattr"] = _setattr
			b["hasattr"] = _hasattr
			b["dir"] = _dir
			b["bool"] = BoolType
			b["int"] = IntType
			b["float"] = FloatType
			b["str"] = StrType
			b["date"] = DateType
			b["datetime"] = DateTimeType
			b["timedelta"] = TimeDeltaType
			b["monthdelta"] = misc.monthdelta.ul4_type
			b["list"] = ListType
			b["set"] = SetType
			b["dict"] = DictType
			b["color"] = _create_module(
				"color",
				"Types and functions for handling RGBA colors",
				Color=color.Color.ul4_type,
				css=color.css,
				mix=color.mix,
			)
			b["ul4"] = _create_module(
				"ul4",
				"UL4 - A templating language",
				AST=AST.ul4_type,
				TextAST=TextAST.ul4_type,
				IndentAST=IndentAST.ul4_type,
				LineEndAST=LineEndAST.ul4_type,
				CodeAST=CodeAST.ul4_type,
				ConstAST=ConstAST.ul4_type,
				SeqItemAST=SeqItemAST.ul4_type,
				UnpackSeqItemAST=UnpackSeqItemAST.ul4_type,
				ListAST=ListAST.ul4_type,
				ListComprehensionAST=ListComprehensionAST.ul4_type,
				SetAST=SetAST.ul4_type,
				SetComprehensionAST=SetComprehensionAST.ul4_type,
				DictItemAST=DictItemAST.ul4_type,
				UnpackDictItemAST=UnpackDictItemAST.ul4_type,
				DictAST=DictAST.ul4_type,
				DictComprehensionAST=DictComprehensionAST.ul4_type,
				GeneratorExpressionAST=GeneratorExpressionAST.ul4_type,
				VarAST=VarAST.ul4_type,
				BlockAST=BlockAST.ul4_type,
				ConditionalBlocksAST=ConditionalBlocksAST.ul4_type,
				IfBlockAST=IfBlockAST.ul4_type,
				ElIfBlockAST=ElIfBlockAST.ul4_type,
				ElseBlockAST=ElseBlockAST.ul4_type,
				ForBlockAST=ForBlockAST.ul4_type,
				WhileBlockAST=WhileBlockAST.ul4_type,
				BreakAST=BreakAST.ul4_type,
				ContinueAST=ContinueAST.ul4_type,
				AttrAST=AttrAST.ul4_type,
				SliceAST=SliceAST.ul4_type,
				UnaryAST=UnaryAST.ul4_type,
				NotAST=NotAST.ul4_type,
				IfAST=IfAST.ul4_type,
				NegAST=NegAST.ul4_type,
				BitNotAST=BitNotAST.ul4_type,
				PrintAST=PrintAST.ul4_type,
				PrintXAST=PrintXAST.ul4_type,
				ReturnAST=ReturnAST.ul4_type,
				BinaryAST=BinaryAST.ul4_type,
				ItemAST=ItemAST.ul4_type,
				ShiftLeftAST=ShiftLeftAST.ul4_type,
				ShiftRightAST=ShiftRightAST.ul4_type,
				BitAndAST=BitAndAST.ul4_type,
				BitXOrAST=BitXOrAST.ul4_type,
				BitOrAST=BitOrAST.ul4_type,
				IsAST=IsAST.ul4_type,
				IsNotAST=IsNotAST.ul4_type,
				EQAST=EQAST.ul4_type,
				NEAST=NEAST.ul4_type,
				LTAST=LTAST.ul4_type,
				LEAST=LEAST.ul4_type,
				GTAST=GTAST.ul4_type,
				GEAST=GEAST.ul4_type,
				ContainsAST=ContainsAST.ul4_type,
				NotContainsAST=NotContainsAST.ul4_type,
				AddAST=AddAST.ul4_type,
				SubAST=SubAST.ul4_type,
				MulAST=MulAST.ul4_type,
				FloorDivAST=FloorDivAST.ul4_type,
				TrueDivAST=TrueDivAST.ul4_type,
				OrAST=OrAST.ul4_type,
				AndAST=AndAST.ul4_type,
				ModAST=ModAST.ul4_type,
				ChangeVarAST=ChangeVarAST.ul4_type,
				SetVarAST=SetVarAST.ul4_type,
				AddVarAST=AddVarAST.ul4_type,
				SubVarAST=SubVarAST.ul4_type,
				MulVarAST=MulVarAST.ul4_type,
				FloorDivVarAST=FloorDivVarAST.ul4_type,
				TrueDivVarAST=TrueDivVarAST.ul4_type,
				ModVarAST=ModVarAST.ul4_type,
				ShiftLeftVarAST=ShiftLeftVarAST.ul4_type,
				ShiftRightVarAST=ShiftRightVarAST.ul4_type,
				BitAndVarAST=BitAndVarAST.ul4_type,
				BitXOrVarAST=BitXOrVarAST.ul4_type,
				BitOrVarAST=BitOrVarAST.ul4_type,
				PositionalArgumentAST=PositionalArgumentAST.ul4_type,
				KeywordArgumentAST=KeywordArgumentAST.ul4_type,
				UnpackListArgumentAST=UnpackListArgumentAST.ul4_type,
				UnpackDictArgumentAST=UnpackDictArgumentAST.ul4_type,
				CallAST=CallAST.ul4_type,
				RenderAST=RenderAST.ul4_type,
				RenderXAST=RenderXAST.ul4_type,
				RenderBlockAST=RenderBlockAST.ul4_type,
				RenderBlocksAST=RenderBlocksAST.ul4_type,
				SignatureAST=SignatureAST.ul4_type,
				Template=Template.ul4_type,
				TemplateClosure=TemplateClosure.ul4_type,
			)
			b["ul4on"] = _create_module(
				"ul4on",
				"Object serialization",
				loads=ul4on.loads,
				dumps=ul4on.dumps,
				Encoder=ul4on.Encoder.ul4_type,
				Decoder=ul4on.Decoder.ul4_type,
			)
			b["operator"] = _create_module(
				"operator",
				"Various operators as functions",
				attrgetter=AttrGetter.ul4_type,
			)
			b["math"] = _create_module(
				"math",
				"Math related functions and constants",
				cos=math.cos,
				sin=math.sin,
				tan=math.tan,
				sqrt=math.sqrt,
				isclose=math.isclose,
				pi=math.pi,
				e=math.e,
				tau=math.tau,
			)

	@contextlib.contextmanager
	def replacevars(self, vars):
		oldvars = self.vars.maps[0]
		try:
			self.vars.maps[0] = vars
			yield
		finally:
			self.vars.maps[0] = oldvars

	@contextlib.contextmanager
	def chainvars(self):
		try:
			self.vars.maps.insert(0, {})
			yield
		finally:
			del self.vars.maps[0]

	def output(self, string):
		for escape in self.escapes:
			string = escape(string)
		return string


###
### Helper functions
###

def _decorateexception(exc, ast, obj=None):
	# Find the end of the exception chain
	while exc.__cause__:
		exc = exc.__cause__
	# Attach location to innermost exception
	if not isinstance(exc, LocationError) or (isinstance(ast, CallAST) and isinstance(obj, (Template, TemplateClosure))):
		exc.__cause__ = LocationError(ast)


def _handleexpressioneval(f):
	"""
	Decorator for an implementation of the :meth:`eval` method that does not
	do output (so it is a normal method).

	This decorator is responsible for exception handling. An exception that
	bubbles up the Python call stack will generate an exception chain that
	follows the UL4 call stack.
	"""
	@functools.wraps(f)
	def wrapped(self, context, /, *args, **kwargs):
		context.asts.append(self)
		try:
			return f(self, context, *args, **kwargs)
		except (BreakException, ContinueException, ReturnException):
			# Pass those exception through to the AST nodes that will handle them (:class:`ForBlockAST` or :class:`Template`)
			raise
		except Exception as exc:
			_decorateexception(exc, self)
			raise
		finally:
			context.asts.pop()
	return wrapped


def _handleoutputeval(f):
	"""
	Decorator for an implementation of the :meth:`eval` method that does output
	(so it is a generator).

	This decorator is responsible for exception handling. An exception that
	bubbles up the Python call stack will generate an exception chain that
	follows the UL4 call stack.
	"""
	@functools.wraps(f)
	def wrapped(self, context, /, *args, **kwargs):
		context.asts.append(self)
		try:
			yield from f(self, context, *args, **kwargs)
		except (BreakException, ContinueException, ReturnException):
			# Pass those exception through to the AST nodes that will handle them (:class:`ForBlockAST` or :class:`Template`)
			raise
		except Exception as exc:
			_decorateexception(exc, self)
			raise
		finally:
			context.asts.pop()
	return wrapped


def _unpackvar(lvalue, value):
	"""
	A generator used for recursively unpacking values for assignment.

	``lvalue`` may be an :class:`AST` object (in which case the recursion ends)
	or a (possible nested) sequence of :class:`AST` objects.

	The values produced are (AST node, value) tuples.
	"""
	if isinstance(lvalue, AST):
		yield (lvalue, value)
	else:
		# Materialize iterators on the right hand side, but protect against infinite iterators
		if not isinstance(value, (tuple, list, str)):
			# If we get one item more than required, we have an error
			# Also :func:`islice` might fail if the right hand side isn't iterable (e.g. ``(a, b) = 42``)
			value = list(itertools.islice(value, len(lvalue)+1))
		if len(lvalue) != len(value):
			# The number of variables on the left hand side doesn't match the number of values on the right hand side
			raise TypeError(f"need {len(lvalue):,} value{'s' if len(lvalue) != 1 else ''} to unpack")
		for (lvalue, value) in zip(lvalue, value):
			yield from _unpackvar(lvalue, value)


def _makevars(signature, args, kwargs):
	"""
	Bind ``args`` and ``kwargs`` to the :class:`inspect.Signature` object
	``signature`` and return the resulting argument dictionary. (This differs
	from :meth:`inspect.Signature.bind` in that it handles default values too.)

	``signature`` may also be :const:`None` in which case ``args`` must be empty
	and `kwargs` is returned, i.e. the signature is treated as accepting no
	positional argument and any keyword argument.
	"""
	if signature is None:
		if args:
			raise TypeError("positional arguments not supported")
		return kwargs
	else:
		vars = signature.bind(*args, **kwargs)
		vars.apply_defaults()
		return vars.arguments


def _linecol(source, index):
	index = index or 0
	lastlinefeed = source.rfind("\n", 0, index)
	if lastlinefeed >= 0:
		return (source.count("\n", 0, index)+1, index-lastlinefeed)
	else:
		return (1, index + 1)


def _offset(pos):
	offset = ["["]
	if pos.start is not None:
		offset.append(f"{pos.start:,}")
	offset.append(":")
	if pos.stop is not None:
		offset.append(f"{pos.stop:,}")
	offset.append("]")
	return "".join(offset)


def _sourceprefix(source, pos):
	outerstartpos = innerstartpos = pos

	preprefix = ""
	maxprefix = 40
	while maxprefix > 0:
		# We arrived at the start of the source
		if outerstartpos == 0:
			break
		# We arrived at the start of the line
		if source[outerstartpos-1] == "\n":
			break
		maxprefix -= 1
		outerstartpos -= 1
	else:
		# We've exhausted the length of the prefix
		preprefix = "\N{HORIZONTAL ELLIPSIS}"

	return preprefix + source[outerstartpos:innerstartpos]


def _sourcesuffix(source, pos):
	outerstoppos = innerstoppos = pos

	postsuffix = ""
	maxsuffix = 40
	while maxsuffix > 0:
		# We arrived at the end of the source
		if outerstoppos >= len(source):
			break
		# We arrived at the end of the line
		if source[outerstoppos] == "\n":
			break
		maxsuffix -= 1
		outerstoppos += 1
	else:
		# We've exhausted the length of the suffix
		postsuffix = "\N{HORIZONTAL ELLIPSIS}"

	return source[innerstoppos:outerstoppos] + postsuffix


###
### Helper functions for the various UL4 functions
###

def _str(obj="", /):
	from ll import color
	if obj is None:
		return ""
	elif isinstance(obj, Undefined):
		return ""
	elif isinstance(obj, str):
		return obj
	elif isinstance(obj, datetime.datetime):
		if obj.microsecond or obj.second:
			return str(obj)
		else:
			return str(obj)[:-3]
	elif isinstance(obj, color.Color):
		return str(obj)
	elif isinstance(obj, (abc.Sequence, abc.Set, abc.Mapping)):
		return _repr(obj)
	elif isinstance(obj, inspect.Signature):
		v = []
		v.append("(")
		for (i, p) in enumerate(obj.parameters.values()):
			if i:
				v.append(", ")
			if p.kind == p.VAR_POSITIONAL:
				v.append("*")
			elif p.kind == p.VAR_KEYWORD:
				v.append("**")
			v.append(p.name)
			if p.default is not p.empty:
				v.append("=")
				v.append(_repr(p.default))
		v.append(")")
		return "".join(v)
	else:
		return str(obj)


def _repr_helper(obj, seen, forceascii):
	from ll import color
	if isinstance(obj, str):
		if forceascii:
			yield ascii(obj)
		else:
			yield repr(obj)
	elif isinstance(obj, datetime.datetime):
		s = obj.isoformat()
		if s.endswith("T00:00:00"):
			s = s[:-8]
		elif s.endswith(":00"):
			s = s[:-3]
		yield f"@({s})"
	elif isinstance(obj, datetime.date):
		yield f"@({obj.isoformat()})"
	elif isinstance(obj, datetime.timedelta):
		yield repr(obj).partition(".")[-1]
	elif isinstance(obj, color.Color):
		if obj[3] == 0xff:
			s = f"#{obj[0]:02x}{obj[1]:02x}{obj[2]:02x}"
			if s[1] == s[2] and s[3] == s[4] and s[5] == s[6]:
				s = f"#{s[1]}{s[3]}{s[5]}"
			yield s
		else:
			s = f"#{obj[0]:02x}{obj[1]:02x}{obj[2]:02x}{obj[3]:02x}"
			if s[1] == s[2] and s[3] == s[4] and s[5] == s[6] and s[7] == s[8]:
				s = f"#{s[1]}{s[3]}{s[5]}{s[7]}"
			yield s
	elif isinstance(obj, abc.Sequence):
		if id(obj) in seen:
			yield "..."
		else:
			seen.add(id(obj))
			yield "["
			for (i, item) in enumerate(obj):
				if i:
					yield ", "
				yield from _repr_helper(item, seen, forceascii)
			yield "]"
			seen.discard(id(obj))
	elif isinstance(obj, abc.Set):
		if id(obj) in seen:
			yield "..."
		else:
			if obj:
				seen.add(id(obj))
				yield "{"
				for (i, item) in enumerate(obj):
					if i:
						yield ", "
					yield from _repr_helper(item, seen, forceascii)
				yield "}"
				seen.discard(id(obj))
			else:
				yield "{/}"
	elif isinstance(obj, inspect.Signature):
		if id(obj) in seen:
			yield "..."
		else:
			seen.add(id(obj))
			yield "<Signature ("
			for (i, p) in enumerate(obj.parameters.values()):
				if i:
					yield ", "
				if p.kind == p.VAR_POSITIONAL:
					yield "*"
				elif p.kind == p.VAR_KEYWORD:
					yield "**"
				yield p.name
				if p.default is not p.empty:
					yield "="
					yield from _repr_helper(p.default, seen, forceascii)
			yield ")>"
			seen.discard(id(obj))
	elif isinstance(obj, abc.Mapping):
		if id(obj) in seen:
			yield "..."
		else:
			seen.add(id(obj))
			yield "{"
			for (i, (key, value)) in enumerate(obj.items()):
				if i:
					yield ", "
				yield from _repr_helper(key, seen, forceascii)
				yield ": "
				yield from _repr_helper(value, seen, forceascii)
			yield "}"
			seen.discard(id(obj))
	else:
		if forceascii:
			yield ascii(obj)
		else:
			yield repr(obj)


def _repr(obj, /):
	return "".join(_repr_helper(obj, set(), False))


def _ascii(obj, /):
	return "".join(_repr_helper(obj, set(), True))


def _asjson(obj, /):
	from ll import misc, color
	if obj is None:
		return "null"
	elif isinstance(obj, Undefined):
		return "undefined"
	elif isinstance(obj, (bool, int, float)):
		return json.dumps(obj)
	elif isinstance(obj, str):
		return json.dumps(obj).replace("<", "\\u003c") # Prevent XSS (when the value is embedded literally in a ``<script>`` tag)
	elif isinstance(obj, datetime.datetime):
		return f"new Date({obj.year}, {obj.month-1}, {obj.day}, {obj.hour}, {obj.minute}, {obj.second}, {obj.microsecond//1000})"
	elif isinstance(obj, datetime.date):
		return f"new ul4.Date_({obj.year}, {obj.month}, {obj.day})"
	elif isinstance(obj, datetime.timedelta):
		return f"new ul4.TimeDelta({obj.days}, {obj.seconds}, {obj.microseconds})"
	elif isinstance(obj, misc.monthdelta):
		return f"new ul4.MonthDelta({obj.months()})"
	elif isinstance(obj, color.Color):
		return f"new ul4.Color({obj[0]}, {obj[1]}, {obj[2]}, {obj[3]})"
	elif isinstance(obj, abc.Mapping):
		items = ", ".join(f"{_asjson(key)}: {_asjson(value)}" for (key, value) in obj.items())
		return f"{{{items}}}"
	elif isinstance(obj, abc.Sequence):
		items = ", ".join(_asjson(item) for item in obj)
		return f"[{items}]"
	elif isinstance(obj, Template):
		return obj.jssource()
	else:
		raise TypeError(f"can't handle object of type {type(obj)}")


def _xmlescape(obj, /):
	if obj is None:
		return ""
	elif isinstance(obj, Undefined):
		return ""
	else:
		from ll import misc
		return misc.xmlescape(_str(obj))


###
### Type objects for UL4 types
###

class Type:
	ul4_attrs = {"__module__", "__name__", "__doc__"}

	# Attributes that are returned via a simple ``getattr`` call (either data attributes or as bound methods)
	plainattrs = frozenset()

	# Attributes that should appear as data attributes, but are implemented as methods in the :class:`Type` subclass
	wrappeddataattrs = frozenset()

	# Attributes that should appear as methods and are implemented as methods in the :class:`Type` subclass
	wrappedmethattrs = frozenset()

	def __init__(self, module=None, name=None, doc=None, type=None):
		self.type = type
		self.__module__ = module
		self.__name__ = name
		if doc is not None:
			doc = textwrap.dedent(doc).strip()
		self.__doc__ = doc

	def __repr__(self):
		if self.__module__ is None:
			return f"<type {self.__name__}>"
		else:
			return f"<type {self.__module__}.{self.__name__}>"

	def __set_name__(self, type, name):
		self.type = type
		if self.__name__ is None and type.__name__ is not None:
			self.__name__ = type.__name__
		if self.__doc__ is None and type.__doc__ is not None:
			self.__doc__ = textwrap.dedent(type.__doc__).strip().split("\n\n")[0]

	def instancecheck(self, obj):
		return isinstance(obj, self.type)

	def _wrapmethod(self, obj, name):
		func = getattr(self, name)
		def wrapped(*args, **kwargs):
			return func(obj, *args, **kwargs)
		wrapped.__name__ = name
		wrapped.__module__ = self.__module__
		wrapped.__qualname__ = name
		return wrapped

	def getattr(self, obj, name, default=object):
		"""
		Return the attribute ``name`` of the object :obj`obj` and honor
		``ul4_getattr`` and ``ul4_attrs``.
		"""
		ul4_getattr = getattr(obj, "ul4_getattr", None)
		ul4_attrs = getattr(obj, "ul4_attrs", None)

		if ul4_getattr is not None:
			try:
				return ul4_getattr(name)
			except AttributeError:
				return self.missing(obj, name, default)
		else:
			if ul4_attrs is not None and name in ul4_attrs:
				return getattr(obj, name)
			elif name in self.plainattrs:
				return getattr(obj, name)
			elif name in self.wrappeddataattrs:
				return getattr(self, name)(obj)
			elif name in self.wrappedmethattrs:
				return self._wrapmethod(obj, name)
			return self.missing(obj, name, default)

	def missing(self, obj, name, default=object):
		if default is object:
			raise AttributeError(name)
		return default

	def setattr(self, obj, name, value):
		"""
		Set the attribute ``name`` of the object :obj`obj` to ``value`` and
		honors ``ul4_setattr`` and ``ul4_attrs``.
		"""
		ul4_setattr = getattr(obj, "ul4_setattr", None)
		if ul4_setattr is not None:
			ul4_setattr(name, value)
		else:
			ul4_attrs = getattr(obj, "ul4_attrs", None)
			if ul4_attrs is not None:
				# An ``ul4_attrs`` attribute without ``ul4_setattr`` will *not* make the attribute writable
				from ll import misc
				raise TypeError(f"attribute {misc.format_class(obj)}.{name!r} is readonly")
			else:
				obj[name] = value

	def hasattr(self, obj, name):
		"""
		Return whether the object :obj`obj`  has an attribute ``name`` and
		honors ``ul4_hasattr`` and ``ul4_attrs``.
		"""
		ul4_hasattr = getattr(obj, "ul4_hasattr", None)
		if ul4_hasattr is not None:
			return ul4_hasattr(name)
		else:
			ul4_attrs = getattr(obj, "ul4_attrs", None)
			if ul4_attrs is not None:
				return name in ul4_attrs
			else:
				return name in self.plainattrs or name in self.wrappeddataattrs or name in self.wrappedmethattrs

	def dir(self, obj):
		ul4_attrs = getattr(obj, "ul4_attrs", None)
		if ul4_attrs is not None:
			return ul4_attrs
		return frozenset({*self.plainattrs, *self.wrappeddataattrs, *self.wrappedmethattrs})


class InstantiableType(Type):
	def __call__(self, /, *args, **kwargs):
		return self.type(*args, **kwargs)


class GenericType(Type):
	def __init__(self, cls):
		super().__init__(cls.__module__ if cls.__module__ != "builtins" else None, cls.__name__, cls.__doc__)
		self.type = cls


class GenericExceptionType(GenericType):
	wrappeddataattrs = {"context"}

	@staticmethod
	def context(obj):
		if obj.__cause__ is not None:
			return obj.__cause__
		elif obj.__context__ is not None and not obj.__suppress_context__:
			return obj.__context__
		return None


class NoneType(Type):
	def instancecheck(self, obj):
		return obj is None

NoneType = NoneType(None, "None", "Nothing")


BoolType = InstantiableType(None, "bool", "A boolean value (True or False)", type=bool)


class IntType(Type):
	def __call__(self, obj=0, /, base=None):
		if base is None:
			return int(obj)
		else:
			return int(obj, base)

	def instancecheck(self, obj):
		return isinstance(obj, int) and not isinstance(obj, bool)

IntType = IntType(None, "int", "An integer value")


class FloatType(Type):
	def __call__(self, x=0.0, /):
		return float(x)

	def instancecheck(self, obj):
		return isinstance(obj, float)

FloatType = FloatType(None, "float", "An floating point value")


class StrType(Type):
	wrappedmethattrs = {"split", "rsplit", "splitlines", "strip", "lstrip", "rstrip", "upper", "lower", "capitalize", "startswith", "endswith", "replace", "count", "find", "rfind", "join"}

	def __call__(self, obj="", /):
		return _str(obj)

	def instancecheck(self, obj):
		return isinstance(obj, str)

	@staticmethod
	def split(obj, sep=None, maxsplit=None):
		return obj.split(sep, maxsplit if maxsplit is not None else -1)

	@staticmethod
	def rsplit(obj, sep=None, maxsplit=None):
		return obj.rsplit(sep, maxsplit if maxsplit is not None else -1)

	@staticmethod
	def splitlines(obj, keepends=False):
		return obj.splitlines(keepends)

	@staticmethod
	def strip(obj, chars=None, /):
		return obj.strip(chars)

	@staticmethod
	def lstrip(obj, chars=None, /):
		return obj.lstrip(chars)

	@staticmethod
	def rstrip(obj, chars=None, /):
		return obj.rstrip(chars)

	@staticmethod
	def count(obj, sub, start=None, end=None, /):
		return obj.count(sub, start, end)

	@staticmethod
	def find(obj, sub, start=None, end=None, /):
		return obj.find(sub, start, end)

	@staticmethod
	def rfind(obj, sub, start=None, end=None, /):
		return obj.rfind(sub, start, end)

	@staticmethod
	def startswith(obj, prefix, /):
		if isinstance(prefix, list):
			prefix = tuple(prefix)
		return obj.startswith(prefix)

	@staticmethod
	def endswith(obj, suffix, /):
		if isinstance(suffix, list):
			suffix = tuple(suffix)
		return obj.endswith(suffix)

	@staticmethod
	def upper(obj):
		return obj.upper()

	@staticmethod
	def lower(obj):
		return obj.lower()

	@staticmethod
	def capitalize(obj):
		return obj.capitalize()

	@staticmethod
	def replace(obj, old, new, count=-1, /):
		return obj.replace(old, new, count if count is not None else -1)

	@staticmethod
	def join(obj, iterable, /):
		return obj.join(iterable)

StrType = StrType(None, "str", "A string")


class ListType(Type):
	wrappedmethattrs = {"append", "insert", "pop", "count", "find", "rfind"}

	def __call__(self, iterable=(), /):
		return list(iterable)

	def instancecheck(self, obj):
		from ll import color
		return isinstance(obj, (list, tuple, abc.Sequence)) and not isinstance(obj, (str, color.Color))

	@staticmethod
	def append(obj, *items):
		obj.extend(items)

	@staticmethod
	def insert(obj, pos, *items):
		obj[pos:pos] = items

	@staticmethod
	def pop(obj, pos=-1):
		return obj.pop(pos)

	@staticmethod
	def count(obj, sub, start=None, end=None, /):
		if start is None and end is None:
			return obj.count(sub)
		else:
			(start, stop, stride) = slice(start, end).indices(len(obj))
			count = 0
			for i in range(start, stop, stride):
				if obj[i] == sub:
					count += 1
			return count

	@staticmethod
	def find(obj, sub, start=None, end=None, /):
		try:
			if end is None:
				if start is None:
					return obj.index(sub)
				return obj.index(sub, start)
			return obj.index(sub, start, end)
		except ValueError:
			return -1

	@staticmethod
	def rfind(obj, sub, start=None, end=None, /):
		for i in reversed(range(*slice(start, end).indices(len(obj)))):
			if obj[i] == sub:
				return i
		return -1

ListType = ListType(None, "list", "A list")


class DateType(Type):
	wrappedmethattrs = {"weekday", "yearday", "week", "calendar", "day", "month", "year", "date", "mimeformat", "isoformat"}

	def __call__(self, year, month, day):
		return datetime.date(year, month, day)

	def instancecheck(self, obj):
		return isinstance(obj, datetime.date) and not isinstance(obj, datetime.datetime)

	@staticmethod
	def weekday(obj):
		return obj.weekday()

	@staticmethod
	def calendar(obj, firstweekday=0, mindaysinfirstweek=4):
		"""
		Return the calendar year the date ``obj`` belongs to, the calendar week
		number and the week day. (A day might belong to a different calender year,
		if it is in week 1 but before January 1, or if belongs to week 1 of the
		following year).

		``firstweekday`` defines what a week is (i.e. which weekday is
		considered the start of the week, ``0`` is Monday and ``6`` is Sunday).
		``mindaysinfirstweek`` defines how many days must be in a week to be
		considered the first week in the year.

		For example for the ISO week number (according to
		https://en.wikipedia.org/wiki/ISO_week_date) the week starts on Monday
		(i.e. ``firstweekday == 0``) and a week is considered the first week if
		it's the first week that contains a Thursday (which means that this week
		contains at least four days in January, so ``mindaysinfirstweek == 4``).
		This is also the default for both parameters.

		For the US ``firstweekday == 6`` and ``mindaysinfirstweek == 1``, i.e.
		the week starts on Sunday and January the first is always in week 1.

		There's also the convention that the week 1 is the first complete week
		in January. For this ``mindaysinfirstweek == 7``.

		For example ``<?print repr(@(2000-02-29).calendar()?>`` prints
		``[2000, 9, 1]``, i.e. this day is the Tuesday in week 9 of the year 2000.
		"""

		# Normalize parameters
		firstweekday %= 7
		mindaysinfirstweek = max(1, min(mindaysinfirstweek, 7))

		# ``obj`` might be in the first week of the next year, or last week of
		# the previous year, so we might have to try those too.
		for year in (obj.year+1, obj.year, obj.year-1):
			# ``refdate`` will always be in week 1
			refdate = obj.__class__(year, 1, mindaysinfirstweek)
			# Go back to the start of ``refdate``\s week (i.e. day 1 of week 1)
			weekstartdate = refdate - datetime.timedelta((refdate.weekday() - firstweekday) % 7)
			# Is our date ``obj`` at or after day 1 of week 1?
			# (if not we have to recalculate based on the year before in the next loop iteration)
			if obj >= weekstartdate:
				# Add 1, because the first week is week 1, not week 0
				return (year, (obj - weekstartdate).days//7 + 1, obj.weekday())

	@staticmethod
	def week(obj, firstweekday=0, mindaysinfirstweek=4):
		"""
		Return the week number of the date ``obj``. For more info see
		:meth:`calendar`.
		"""
		return DateType.calendar(obj, firstweekday, mindaysinfirstweek)[1]

	@staticmethod
	def day(obj):
		return obj.day

	@staticmethod
	def month(obj):
		return obj.month

	@staticmethod
	def year(obj):
		return obj.year

	@staticmethod
	def date(obj):
		return obj

	@staticmethod
	def mimeformat(obj):
		weekdayname = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
		monthname = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
		return f"{weekdayname[obj.weekday()]}, {obj.day:02d} {monthname[obj.month]:3} {obj.year:4}"

	@staticmethod
	def isoformat(obj):
		return obj.isoformat()

	@staticmethod
	def yearday(obj):
		return (obj - obj.__class__(obj.year, 1, 1)).days+1

DateType = DateType(None, "date", "A date")


class DateTimeType(DateType.__class__):
	wrappedmethattrs = DateType.wrappedmethattrs.union({"hour", "minute", "second", "microsecond"})

	def __call__(self, year, month, day, hour=0, minute=0, second=0, microsecond=0):
		return datetime.datetime(year, month, day, hour, minute, second, microsecond)

	def instancecheck(self, obj):
		return isinstance(obj, datetime.datetime)

	@staticmethod
	def hour(obj):
		return obj.hour

	@staticmethod
	def minute(obj):
		return obj.minute

	@staticmethod
	def second(obj):
		return obj.second

	@staticmethod
	def microsecond(obj):
		return obj.microsecond

	@staticmethod
	def date(obj):
		return obj.date()

	@staticmethod
	def mimeformat(obj):
		weekdayname = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
		monthname = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
		return f"{weekdayname[obj.weekday()]}, {obj.day:02d} {monthname[obj.month]:3} {obj.year:4} {obj.hour:02}:{obj.minute:02}:{obj.second:02} GMT"

DateTimeType = DateTimeType(None, "datetime", "A date and time value")


class TimeDeltaType(Type):
	wrappedmethattrs = {"days", "seconds", "microseconds"}

	def __call__(self, days=0, seconds=0, microseconds=0):
		return datetime.timedelta(days, seconds, microseconds)

	def instancecheck(self, obj):
		return isinstance(obj, datetime.timedelta)

	@staticmethod
	def days(obj):
		return obj.days

	@staticmethod
	def seconds(obj):
		return obj.seconds

	@staticmethod
	def microseconds(obj):
		return obj.microseconds

TimeDeltaType = TimeDeltaType(None, "timedelta", "A time span")


class DictType(Type):
	plainattrs = {"items", "values", "clear", "pop"}
	wrappedmethattrs = {"get", "update"}

	def __call__(self, *args, **kwargs):
		return dict(*args, **kwargs)

	def instancecheck(self, obj):
		return isinstance(obj, (dict, abc.Mapping))

	@staticmethod
	def get(obj, key, default=None, /):
		return obj.get(key, default)

	@staticmethod
	def update(obj, *others, **kwargs):
		for other in others:
			obj.update(other)
		obj.update(**kwargs)

	def missing(self, obj, name, default=None):
		if name in obj:
			return obj[name]
		return super().missing(obj, name)

DictType = DictType(None, "dict", "A dictionary")


class SetType(Type):
	plainattrs = {"clear"}
	wrappedmethattrs = {"add"}

	def __call__(self, iterable=(), /):
		return set(iterable)

	def instancecheck(self, obj):
		return isinstance(obj, (set, frozenset, abc.Set))

	@staticmethod
	def add(obj, *items):
		obj.update(items)


SetType = SetType(None, "set", "A set")


class SliceType(Type):
	plainattrs = {"start", "stop"}

	def instancecheck(self, obj):
		return isinstance(obj, slice)


SliceType = SliceType(None, "slice", "A slice")


class AttrGetter:
	ul4_type = InstantiableType("operator", "attrgetter", "Return a callable object that fetches the given attribute(s) from its operand.")

	def __init__(self, *attrs):
		self.attrs = [a.split(".") for a in attrs]

	def _fetchattr(self, obj, attrnames):
		for name in attrnames:
			obj = _type(obj).getattr(obj, name)
		return obj

	def __call__(self, obj):
		if len(self.attrs) == 1:
			return self._fetchattr(obj, self.attrs[0])
		return [self._fetchattr(obj, a) for a in self.attrs]


###
### Node classes for the abstract syntax tree
###

class AST:
	"""
	Base class for all UL4 syntax tree nodes.
	"""

	ul4_type = Type("ul4")

	# Set of attributes available to UL4 templates
	ul4_attrs = {"type", "template", "pos", "startpos", "startline", "startcol", "source", "startsource", "fullsource", "sourceprefix", "sourcesuffix", "startsourceprefix", "startsourcesuffix", "stopsourceprefix", "stopsourcesuffix"}

	# Specifies whether the node does output (so :meth:`eval` is a generator)
	# or not (so :meth:`eval` is a normal method).
	output = False

	def __init__(self, template=None, startpos=None):
		# ``template`` references the :class:`Template` object of which
		# ``self`` is a part. This mean that for a :class:`Template` object ``t``
		# (which is an :class:`AST` object) ``t.template is t`` is true.
		self.template = template
		self._startpos = startpos
		self._startline = None
		self._startcol = None
		self._stoppos = None
		self._stopline = None
		self._stopcol = None

	@property
	def startpos(self):
		return self._startpos

	@startpos.setter
	def startpos(self, pos):
		self._startpos = pos
		self._startline = None
		self._startcol = None

	@property
	def startline(self):
		if self._startline is None:
			(self._startline, self._startcol) = _linecol(self.template._fullsource, self._startpos.start)
		return self._startline

	@property
	def startcol(self):
		if self._startcol is None:
			(self._startline, self._startcol) = _linecol(self.template._fullsource, self._startpos.start)
		return self._startcol

	@property
	def startsource(self):
		return self.template._fullsource[self._startpos]

	@property
	def sourceprefix(self):
		return _sourceprefix(self.template._fullsource, self._startpos.start)

	@property
	def sourcesuffix(self):
		return _sourcesuffix(self.template._fullsource, self._stoppos.stop if self._stoppos is not None else self._startpos.stop)

	startsourceprefix = sourceprefix

	@property
	def startsourcesuffix(self):
		return _sourcesuffix(self.template._fullsource, self._startpos.stop)

	@property
	def stopsourceprefix(self):
		return _sourceprefix(self.template._fullsource, self._stoppos.start) if self._stoppos is not None else None

	@property
	def stopsourcesuffix(self):
		return _sourcesuffix(self.template._fullsource, self._stoppos.stop) if self._stoppos is not None else None

	@property
	def stoppos(self):
		return self._stoppos

	@stoppos.setter
	def stoppos(self, pos):
		self._stoppos = pos
		self._stopline = None
		self._stopcol = None

	@property
	def stopline(self):
		if self._stopline is None:
			(self._stopline, self._stopcol) = _linecol(self.template._fullsource, self._stoppos.stop)
		return self._stopline

	@property
	def stopcol(self):
		if self._stopcol is None:
			(self._stopline, self._stopcol) = _linecol(self.template._fullsource, self._stoppos.stop)
		return self._stopcol

	@property
	def stopsource(self):
		return self.template._fullsource[self._stoppos]

	@property
	def pos(self):
		return self._startpos if self._stoppos is None else slice(self._startpos.start, self._stoppos.stop)

	@property
	def source(self):
		return self.template._fullsource[self.pos]

	@property
	def fullsource(self):
		return self.template._fullsource

	def __repr__(self):
		parts = [f"<{self.__class__.__module__}.{self.__class__.__qualname__}"]
		pos = self.pos
		parts.append(f"(offset {_offset(pos)}; line {self.startline:,}; col {self.startcol:,})")
		parts.extend(self._repr())
		parts.append(f"at {id(self):#x}>")
		return " ".join(parts)

	def _repr(self):
		yield from ()

	def _repr_pretty_(self, p, cycle):
		prefix = f"<{self.__class__.__module__}.{self.__class__.__qualname__}"
		pos = self.pos
		prefix += f" (offset {_offset(pos)}; line {self.startline:,}; col {self.startcol:,})"
		suffix = f"at {id(self):#x}"

		if cycle:
			p.text(f"{prefix} ... {suffix}>")
		else:
			with p.group(4, prefix, ">"):
				self._repr_pretty(p)
				p.breakable()
				p.text(suffix)

	def _repr_pretty(self, p):
		pass

	def __str__(self):
		# This uses :meth:`_str`, which is a generator and may output:
		# :const:`None`, which means: "add a line feed and an indentation here"
		# an int, which means: add the int to the indentation level
		# a string, which means: add this string to the output
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

	def eval(self, context):
		"""
		This evaluates the node.

		For most nodes this is a normal function that returns the result of
		evaluating the node. (For these nodes the class attribute ``output``
		is false.). For nodes that produce output (like literal text,
		:class:`PrintAST`, :class:`PrintXAST` or :class:`RenderAST`) it is a
		generator which yields the text output of the node. For blocks (which
		might contain nodes which produce output) this is also a generator.
		(For these nodes the class attribute ``output`` is true.)
		"""
		pass

	def ul4ondump(self, encoder):
		encoder.dump(self.template)
		encoder.dump(self._startpos)

	def ul4onload(self, decoder):
		self.template = decoder.load()
		self.startpos = decoder.load()
		self.stoppos = None


@register("text")
class TextAST(AST):
	"""
	AST node for literal text (i.e. the stuff between tags).

	Attributes are:

	``text`` : :class:`str`
		The text
	"""

	ul4_type = Type("ul4")

	ul4_attrs = AST.ul4_attrs.union({"text"})

	output = True

	def _repr(self):
		yield repr(self.text)

	def _repr_pretty(self, p):
		p.breakable()
		p.text("text=")
		p.pretty(self.text)

	@property
	def text(self):
		return self.template._fullsource[self._startpos]

	def _str(self):
		yield f"text {self.text!r}"

	def eval(self, context):
		yield context.output(self.text)


@register("indent")
class IndentAST(TextAST):
	"""
	AST node for literal text that is an indentation at the start of the line.

	Attributes are:

	``text`` : :class:`str`
		The indentation text (i.e. a string that consists solely of whitespace).
	"""

	ul4_type = Type("ul4")

	def __init__(self, template=None, startpos=None, text=None):
		super().__init__(template, startpos)
		self._text = text

	@property
	def text(self):
		if self._text is None:
			return self.template._fullsource[self._startpos]
		else:
			return self._text

	# We don't define a setter, because the template should *not* be able to
	# set this attribute. However the attribute *will* be set by the code
	# compiling the template
	def _settext(self, text):
		self._text = text if text != self.template._fullsource[self._startpos] else None

	def _str(self):
		yield f"indent {self.text!r}"

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self._text)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self._text = decoder.load()

	def eval(self, context):
		for indent in context.indents:
			yield context.output(indent)
		yield context.output(self.text)


@register("lineend")
class LineEndAST(TextAST):
	r"""
	AST node for literal text that is the end of a line.

	Attributes are:

	``text`` : :class:`str`
		The text of the linefeed (i.e. ``"\n"`` or ``"\r\n"``).
	"""

	ul4_type = Type("ul4")

	def _str(self):
		yield f"lineend {self.text!r}"


class Tag(AST):
	"""
	A :class:`Tag` object is the location of a template tag in a template.
	"""

	ul4_type = Type("ul4")

	def __init__(self, template=None, tag=None, tagpos=None, codepos=None):
		super().__init__(template, tagpos)
		self.tag = tag
		self.codepos = codepos

	def _repr(self):
		yield repr(self.source)

	def _repr_pretty(self, p):
		p.breakable()
		p.text("source=")
		p.pretty(self.source)

	def __str__(self):
		return f"{self.source!r} (offset {_offset(self.startpos)}; line {self.startline:,}; col {self.startcol:,})"

	@property
	def code(self):
		return self.template._fullsource[self.codepos]


class CodeAST(AST):
	"""
	The base class of all AST nodes that are not literal text.

	These nodes appear inside a :class:`Tag`.
	"""

	ul4_type = Type("ul4")

	def _str(self):
		yield " ".join(self.source.splitlines(False))


@register("const")
class ConstAST(CodeAST):
	"""
	AST node for load a constant value.

	Attributes are:

	``value``
		The constant to be loaded.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"value"})

	def __init__(self, template=None, startpos=None, value=None):
		super().__init__(template, startpos)
		self.value = value

	def eval(self, context):
		# We don't need a decorator, because this can't fail anyway.
		return self.value

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()

	def _repr(self):
		yield repr(self.value)

	def _repr_pretty(self, p):
		p.breakable()
		p.text("value=")
		p.pretty(self.value)


### AST nodes for items in list, set and dict "literals"

@register("seqitem")
class SeqItemAST(CodeAST):
	"""
	AST node for an item in a list/set "literal" (e.g. ``{x, y}`` or ``[x, y]``)

	Attributes are:

	``value`` : :class:`AST`
		The list/set item (``x`` and ``y`` in the above examples).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"value"})

	def __init__(self, template=None, startpos=None, value=None):
		super().__init__(template, startpos)
		self.value = value

	def _repr(self):
		yield f"{self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("value=")
		p.pretty(self.value)

	@_handleexpressioneval
	def eval_list(self, context, result):
		result.append(self.value.eval(context))

	@_handleexpressioneval
	def eval_set(self, context, result):
		result.add(self.value.eval(context))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()


@register("unpackseqitem")
class UnpackSeqItemAST(CodeAST):
	"""
	AST node for an ``*`` unpacking expression in a list/set "literal"
	(e.g. the ``y`` in ``{x, *y}`` or ``[x, *y]``)

	Attributes are:

	``value`` : :class:`AST`
		The item to be unpacked into list/set items (``y`` in the above
		examples).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"value"})

	def __init__(self, template=None, startpos=None, value=None):
		super().__init__(template, startpos)
		self.value = value

	def _repr(self):
		yield f"*{self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("value=")
		p.pretty(self.value)

	@_handleexpressioneval
	def eval_list(self, context, result):
		# We're updating the result list here to get a proper location when the ``*`` argument isn't iterable
		for item in self.value.eval(context):
			result.append(item)

	@_handleexpressioneval
	def eval_set(self, context, result):
		# We're updating the result set here to get a proper location when the ``*`` argument isn't iterable
		for item in self.value.eval(context):
			result.add(item)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()


@register("dictitem")
class DictItemAST(CodeAST):
	"""
	AST node for a dictionary entry in a dict expression (:class:`DictAST`).

	Attributes are:

	``key`` : :class:`AST`
		The key of the entry.

	``value`` : :class:`AST`
		The value of the entry.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"key", "value"})

	def __init__(self, template=None, startpos=None, key=None, value=None):
		super().__init__(template, startpos)
		self.key = key
		self.value = value

	def _repr(self):
		yield f"{self.key!r}={self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("key=")
		p.pretty(self.key)
		p.breakable("")
		p.text("value=")
		p.pretty(self.value)

	@_handleexpressioneval
	def eval_dict(self, context, result):
		key = self.key.eval(context)
		value = self.value.eval(context)
		result[key] = value

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.key)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.key = decoder.load()
		self.value = decoder.load()


@register("unpackdictitem")
class UnpackDictItemAST(CodeAST):
	"""
	AST node for ``**`` unpacking expressions in dict "literal"
	(e.g. the ``**u`` in ``{k: v, **u}``).

	Attributes are:

	``item`` : :class:`AST`
		The argument that must evaluate to a dictionary or an iterable of
		(key, value) pairs.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"item"})

	def __init__(self, template=None, startpos=None, item=None):
		super().__init__(template, startpos)
		self.item = item

	def _repr(self):
		yield f"**{self.item!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("item=")
		p.pretty(self.item)

	@_handleexpressioneval
	def eval_dict(self, context, result):
		result.update(self.item.eval(context))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.item = decoder.load()


### AST nodes for call arguments

@register("posarg")
class PositionalArgumentAST(CodeAST):
	"""
	AST node for a positional argument. (e.g. the ``x`` in ``f(x)``).

	Attributes are:

	``value`` : :class:`AST`
		The value of the argument (``x`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"value"})

	def __init__(self, template=None, startpos=None, value=None):
		super().__init__(template, startpos)
		self.value = value

	def _repr(self):
		yield f"{self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("value=")
		p.pretty(self.value)

	def append(self, call):
		for arg in call.args:
			if isinstance(arg, KeywordArgumentAST):
				raise SyntaxError("positional argument follows keyword argument")
			elif isinstance(arg, UnpackDictArgumentAST):
				raise SyntaxError("positional argument follows keyword argument unpacking")
		call.args.append(self)

	@_handleexpressioneval
	def eval_call(self, context, args, kwargs):
		args.append(self.value.eval(context))

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.value = decoder.load()


@register("keywordarg")
class KeywordArgumentAST(CodeAST):
	"""
	AST node for a keyword argument in a :class:`CallAST` (e.g. the ``x=y``
	in the function call``f(x=y)``).

	Attributes are:

	``name`` : :class:`str`
		The keyword argument name (``"x"`` in the above example).

	``value`` : :class:`AST`
		The keyword argument value (``y`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"name", "value"})

	def __init__(self, template=None, startpos=None, name=None, value=None):
		super().__init__(template, startpos)
		self.name = name
		self.value = value

	def _repr(self):
		yield f"{self.name}={self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("name=")
		p.pretty(self.name)
		p.breakable("")
		p.text("value=")
		p.pretty(self.value)

	def append(self, call):
		call.args.append(self)

	@_handleexpressioneval
	def eval_call(self, context, args, kwargs):
		if self.name in kwargs:
			raise SyntaxError(f"duplicate keyword argument {self.name!r}")
		kwargs[self.name] = self.value.eval(context)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.name)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.name = decoder.load()
		self.value = decoder.load()


@register("unpacklistarg")
class UnpackListArgumentAST(CodeAST):
	"""
	AST node for an ``*`` unpacking expressions in a :class:`CallAST`
	(e.g. the ``*x`` in ``f(*x)``).

	Attributes are:

	``item`` : :class:`AST`
		The argument that must evaluate an iterable.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"item"})

	def __init__(self, template=None, startpos=None, item=None):
		super().__init__(template, startpos)
		self.item = item

	def _repr(self):
		yield f"*{self.item!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("item=")
		p.pretty(self.item)

	def append(self, call):
		for arg in call.args:
			if isinstance(arg, UnpackDictArgumentAST):
				raise SyntaxError("iterable argument unpacking follows keyword argument unpacking")
		call.args.append(self)

	@_handleexpressioneval
	def eval_call(self, context, args, kwargs):
		for item in self.item.eval(context):
			args.append(item)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.item = decoder.load()


@register("unpackdictarg")
class UnpackDictArgumentAST(CodeAST):
	"""
	AST node for an ``**`` unpacking expressions in a :class:`CallAST`
	(e.g. the ``**x`` in ``f(**x)``).

	Attributes are:

	``item`` : :class:`AST`
		The argument that must evaluate to a dictionary or an iterable of
		(key, value) pairs.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"item"})

	def __init__(self, template=None, startpos=None, item=None):
		super().__init__(template, startpos)
		self.item = item

	def _repr(self):
		yield f"**{self.item!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("item=")
		p.pretty(self.item)

	def append(self, call):
		call.args.append(self)

	@_handleexpressioneval
	def eval_call(self, context, args, kwargs):
		item = self.item.eval(context)
		if hasattr(item, "keys"):
			for key in item:
				if key in kwargs:
					raise SyntaxError(f"duplicate keyword argument {key!r}")
				kwargs[key] = item[key]
		else:
			for (key, value) in item:
				if key in kwargs:
					raise SyntaxError(f"duplicate keyword argument {key!r}")
				kwargs[key] = value

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.item)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.item = decoder.load()


@register("list")
class ListAST(CodeAST):
	"""
	AST node for creating a list object (e.g. ``[x, y, *z]``).

	Attributes are:

	``items`` : :class:`list`
		The items that will be put into the newly created list as a list of
		:class:`SeqItemAST` (``x`` and ``y`` in the above example) and
		:class:`UnpackSeqItemAST` objects (``z`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"items"})

	def __init__(self, template=None, startpos=None, *items):
		super().__init__(template, startpos)
		self.items = list(items)

	def _repr(self):
		yield f"with {len(self.items):,} items"

	def _repr_pretty(self, p):
		for item in self.items:
			p.breakable()
			p.pretty(item)

	@_handleexpressioneval
	def eval(self, context):
		result = []
		for item in self.items:
			item.eval_list(context, result)
		return result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = decoder.load()


@register("listcomp")
class ListComprehensionAST(CodeAST):
	"""
	AST node for a list comprehension (e.g. ``[v for (a, b) in w if c]``.

	Attributes are:

	``item`` : :class:`AST`
		The expression for the item in the newly created list (``v`` in the
		above example).

	``varname`` : nested :class:`tuple` of :class:`VarAST` objects
		The loop variable (or variables) (``a`` and ``b`` in the above example).

	``container`` : :class:`AST`
		The container or iterable object over which to loop (``w`` in the above
		example).

	``condition`` : :class:`AST` or ``None``
		The condition (as an :class:`AST` object if there is one, or ``None`` if
		there is not) (``c`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"item", "varname", "container", "condition"})

	def __init__(self, template=None, startpos=None, item=None, varname=None, container=None, condition=None):
		super().__init__(template, startpos)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def _repr(self):
		yield f"item={self.item!r}"
		yield f"varname={self.varname!r}"
		yield f"container={self.container!r}"
		if self.container is not None:
			yield f"condition={self.condition!r}"

	def _repr_pretty(self, p):
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

	@_handleexpressioneval
	def eval(self, context):
		container = self.container.eval(context)
		with context.chainvars(): # Don't let loop variables leak into the surrounding scope
			result = []
			for item in container:
				for (lvalue, value) in _unpackvar(self.varname, item):
					lvalue.evalset(context, value)
				if self.condition is None or self.condition.eval(context):
					result.append(self.item.eval(context))
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
class SetAST(CodeAST):
	"""
	AST node for creating a set object (e.g. ``{x, y, *z}``.

	Attributes are:

	``items`` : :class:`list`
		The items that will be put into the newly created set as a list of
		:class:`SeqItemAST` (``x`` and ``y`` in the above example) and
		:class:`UnpackSeqItemAST` objects (``z`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"items"})

	def __init__(self, template=None, startpos=None, *items):
		super().__init__(template, startpos)
		self.items = list(items)

	def _repr(self):
		yield f"with {len(self.items):,} items"

	def _repr_pretty(self, p):
		for item in self.items:
			p.breakable()
			p.pretty(item)

	@_handleexpressioneval
	def eval(self, context):
		result = set()
		for item in self.items:
			item.eval_set(context, result)
		return result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = decoder.load()


@register("setcomp")
class SetComprehensionAST(CodeAST):
	"""
	AST node for a set comprehension (e.g. ``{v for (a, b) in w if c}``.

	Attributes are:

	``item`` : :class:`AST`
		The expression for the item in the newly created set (``v`` in the
		above example).

	``varname`` : nested :class:`tuple` of :class:`VarAST` objects
		The loop variable (or variables) (``a`` and ``b`` in the above example).

	``container`` : :class:`AST`
		The container or iterable object over which to loop (``w`` in the above
		example).

	``condition`` : :class:`AST` or ``None``
		The condition (as an :class:`AST` object if there is one, or ``None`` if
		there is not) (``c`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"item", "varname", "container", "condition"})

	def __init__(self, template=None, startpos=None, item=None, varname=None, container=None, condition=None):
		super().__init__(template, startpos)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def _repr(self):
		yield f"item={self.item!r}"
		yield f"varname={self.varname!r}"
		yield f"container={self.container!r}"
		if self.container is not None:
			yield f"condition={self.condition!r}"

	def _repr_pretty(self, p):
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

	@_handleexpressioneval
	def eval(self, context):
		container = self.container.eval(context)
		with context.chainvars(): # Don't let loop variables leak into the surrounding scope
			result = set()
			for item in container:
				for (lvalue, value) in _unpackvar(self.varname, item):
					lvalue.evalset(context, value)
				if self.condition is None or self.condition.eval(context):
					result.add(self.item.eval(context))
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
class DictAST(CodeAST):
	"""
	AST node for creating a dict object (e.g. `{k: v, **u}`.

	Attributes are:

	``items`` : :class:`list`
		The items that will be put into the newly created dictionary as a list of
		:class:`DictItemAST` (for ``k`` and ``v`` in the above example) and
		:class:`UnpackDictItemAST` objects (for ``u`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"items"})

	def __init__(self, template=None, startpos=None, *items):
		super().__init__(template, startpos)
		self.items = list(items)

	def _repr(self):
		yield f"with {len(self.items):,} items"

	def _repr_pretty(self, p):
		for item in self.items:
			p.breakable()
			p.pretty(item)

	@_handleexpressioneval
	def eval(self, context):
		result = {}
		for item in self.items:
			item.eval_dict(context, result)
		return result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.items)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.items = decoder.load()


@register("dictcomp")
class DictComprehensionAST(CodeAST):
	"""
	AST node for a dictionary comprehension (e.g. ``{k: v for (a, b) in w if c}``.

	Attributes are:

	``key`` : :class:`AST`
		The expression for the keys in the newly created dictionary (``k`` in the
		above example).

	``value`` : :class:`AST`
		The expression for the values in the newly created dictionary (``v`` in
		the above example).

	``varname`` : nested :class:`tuple` of :class:`VarAST` objects
		The loop variable (or variables) (``a`` and ``b`` in the above example).

	``container`` : :class:`AST`
		The container or iterable object over which to loop (``w`` in the above
		example).

	``condition`` : :class:`AST` or ``None``
		The condition (as an :class:`AST` object if there is one, or ``None`` if
		there is not) (``c`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"key", "value", "varname", "container", "condition"})

	def __init__(self, template=None, startpos=None, key=None, value=None, varname=None, container=None, condition=None):
		super().__init__(template, startpos)
		self.key = key
		self.value = value
		self.varname = varname
		self.container = container
		self.condition = condition

	def _repr(self):
		yield f"key={self.key!r}"
		yield f"value={self.value!r}"
		yield f"varname={self.varname!r}"
		yield f"container={self.container!r}"
		if self.container is not None:
			yield f"condition={self.condition!r}"

	def _repr_pretty(self, p):
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

	@_handleexpressioneval
	def eval(self, context):
		container = self.container.eval(context)
		with context.chainvars(): # Don't let loop variables leak into the surrounding scope
			result = {}
			for item in container:
				for (lvalue, value) in _unpackvar(self.varname, item):
					lvalue.evalset(context, value)
				if self.condition is None or self.condition.eval(context):
					result[self.key.eval(context)] = self.value.eval(context)
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
class GeneratorExpressionAST(CodeAST):
	"""
	AST node for a generator expression (e.g. ``(x for (a, b) in w if c)``).

	Attributes are:

	``item`` : :class:`AST`
		An expression for the item that looping over the generator expression will
		produce (``x`` in the above example).

	``varname`` : nested :class:`tuple` of :class:`VarAST` objects
		The loop variable (or variables) (``a`` and ``b`` in the above example).

	``container`` : :class:`AST`
		The container or iterable object over which to loop (``w`` in the above
		example).

	``condition`` : :class:`AST` or ``None``
		The condition (as an :class:`AST` object if there is one, or ``None`` if
		there is not) (``c`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"item", "varname", "container", "condition"})

	def __init__(self, template=None, startpos=None, item=None, varname=None, container=None, condition=None):
		super().__init__(template, startpos)
		self.item = item
		self.varname = varname
		self.container = container
		self.condition = condition

	def _repr(self):
		yield f"item={self.item!r}"
		yield f"varname={self.varname!r}"
		yield f"container={self.container!r}"
		if self.container is not None:
			yield f"condition={self.condition!r}"

	def _repr_pretty(self, p):
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

	def eval(self, context):
		container = self.container.eval(context)

		try:
			with context.chainvars(): # Don't let loop variables leak into the surrounding scope
				for item in container:
					for (lvalue, value) in _unpackvar(self.varname, item):
						lvalue.evalset(context, value)
					if self.condition is None or self.condition.eval(context):
						yield self.item.eval(context)
		except LocationError:
			raise
		except Exception as exc:
			_decorateexception(exc, self)
			raise

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
class VarAST(CodeAST):
	"""
	AST node for getting a variable.

	Attributes are:

	``name`` : :class:`str`
		The name of the variable.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"name"})

	def __init__(self, template=None, startpos=None, name=None):
		super().__init__(template, startpos)
		self.name = name

	def _repr(self):
		yield repr(self.name)

	def _repr_pretty(self, p):
		p.breakable()
		p.text("name=")
		p.pretty(self.name)

	@_handleexpressioneval
	def eval(self, context):
		try:
			return context.vars[self.name]
		except KeyError:
			return UndefinedVariable(self.name)

	@_handleexpressioneval
	def evalset(self, context, value):
		context.vars[self.name] = value

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		context.vars[self.name] = operator.evalfoldaug(context.vars[self.name], value)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.name)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.name = decoder.load()


class BlockAST(CodeAST):
	"""
	Base class for all AST nodes that are blocks.

	A block contains a sequence of AST nodes that are executed sequencially.
	A block may execute its content zero (e.g. an ``<?if?>`` block) or more times
	(e.g. a ``<?for?>`` block).

	Attributes are:

	``content`` : :class:`list` of :class:`AST` objects
		The content of the block.
	"""

	output = True

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"stoppos", "stopline", "stopcol", "stopsource", "content"})

	def __init__(self, template=None, startpos=None, stoppos=None):
		super().__init__(template, startpos)
		self._stoppos = stoppos	
		self._stopline = None
		self._stopcol = None
		self.content = []

	def append(self, item):
		self.content.append(item)

	def _pop_trailing_indent(self):
		if self.content and isinstance(self.content[-1], IndentAST):
			return self.content.pop()
		else:
			return None

	def finish(self, endtag):
		self.stoppos = endtag.startpos

	def _str(self):
		if self.content:
			for node in self.content:
				yield from node._str()
				yield None
		else:
			yield "pass"
			yield None

	@_handleoutputeval
	def eval(self, context):
		for node in self.content:
			result = node.eval(context)
			if node.output:
				yield from result

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.stoppos)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.stoppos = decoder.load()
		self.content = decoder.load()


@register("condblock")
class ConditionalBlocksAST(BlockAST):
	r"""
	AST node for a conditional ``<?if?>/<?elif?>/<?else?>`` block.

	Attributes are:

	``content`` : :class:`list`
		The content of the :class:`ConditionalBlocksAST` block is one
		:class:`IfBlockAST` followed by zero or more :class:`ElIfBlockAST`\s followed
		by zero or one :class:`ElseBlockAST`.
	"""

	ul4_type = Type("ul4")

	def __init__(self, template=None, startpos=None, stoppos=None, condition=None):
		super().__init__(template, startpos, stoppos)
		if condition is not None:
			self.newblock(IfBlockAST(template, startpos, None, condition))

	def _repr_pretty(self, p):
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def append(self, item):
		self.content[-1].append(item)

	def finish(self, endtag):
		super().finish(endtag)
		if self.content:
			self.content[-1].stoppos = slice(endtag.startpos.start, endtag.startpos.start)

	def _pop_trailing_indent(self):
		if self.content:
			return self.content[-1]._pop_trailing_indent()
		else:
			return None

	def newblock(self, block):
		if self.content:
			self.content[-1].stoppos = slice(block.startpos.start, block.startpos.start)
		self.content.append(block)

	def _str(self):
		for node in self.content:
			yield from node._str()

	@_handleoutputeval
	def eval(self, context):
		for node in self.content:
			if isinstance(node, ElseBlockAST) or node.condition.eval(context):
				yield from node.eval(context)
				break


@register("ifblock")
class IfBlockAST(BlockAST):
	"""
	AST node for an ``<?if?>`` block in an ``<?if?>/<?elif?>/<?else?>`` block.

	Attributes are:

	``condition`` : class:`AST`
		The condition in the ``<?if?>`` block.

	``content`` : :class:`list` of `:class:`AST` objects
		The content of the ``<?if?>`` block.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = BlockAST.ul4_attrs.union({"condition"})

	def __init__(self, template=None, startpos=None, stoppos=None, condition=None):
		super().__init__(template, startpos, stoppos)
		self.condition = condition

	def _repr(self):
		yield f" condition={self.condition!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("condition=")
		p.pretty(self.condition)
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def _str(self):
		yield "if "
		yield from CodeAST._str(self)
		yield ":"
		yield None
		yield +1
		yield from BlockAST._str(self)
		yield -1

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()


@register("elifblock")
class ElIfBlockAST(BlockAST):
	"""
	AST node for an ``<?elif?>`` block.

	Attributes are:

	``condition`` : class:`AST`
		The condition in the ``<?elif?>`` block.

	``content`` : :class:`list` of `:class:`AST` objects
		The content of the ``<?elif?>`` block.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = BlockAST.ul4_attrs.union({"condition"})

	def __init__(self, template=None, startpos=None, stoppos=None, condition=None):
		super().__init__(template, startpos, stoppos)
		self.condition = condition

	def _repr(self):
		yield f" condition={self.condition!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("condition=")
		p.pretty(self.condition)
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def _str(self):
		yield "elif "
		yield from CodeAST._str(self)
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
class ElseBlockAST(BlockAST):
	"""
	AST node for an ``<?else?>`` block.

	Attributes are:

	``content`` : :class:`list` of `:class:`AST` objects
		The content of the ``<?else?>`` block.
	"""

	ul4_type = Type("ul4")

	def _repr_pretty(self, p):
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def _str(self):
		yield "else:"
		yield None
		yield +1
		yield from super()._str()
		yield -1


@register("forblock")
class ForBlockAST(BlockAST):
	"""
	AST node for a ``<?for?>`` loop.

	For example ::

		<?for (a, b) in w?>
			body
		<?end for?>

	Attributes are:

	``varname`` : nested :class:`tuple` of :class:`VarAST` objects
		The loop variable (or variables) (``a`` and ``b`` in the above example).

	``container`` : :class:`AST`
		The container or iterable object over which to loop (``w`` in the above
		example).

	``content`` : :class:`list` of :class:`AST` objects
		The loop body (``body`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = BlockAST.ul4_attrs.union({"varname", "container"})

	def __init__(self, template=None, startpos=None, stoppos=None, varname=None, container=None):
		super().__init__(template, startpos, stoppos)
		self.varname = varname
		self.container = container

	def _repr(self):
		yield f"varname={self.varname!r}"
		yield f"container={self.container!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("varname=")
		p.pretty(self.varname)
		p.breakable()
		p.text("container=")
		p.pretty(self.container)
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

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
		yield from CodeAST._str(self)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	@_handleoutputeval
	def eval(self, context):
		container = self.container.eval(context)
		for item in container:
			for (lvalue, value) in _unpackvar(self.varname, item):
				lvalue.evalset(context, value)
			try:
				yield from super().eval(context)
			except BreakException:
				break
			except ContinueException:
				pass


@register("whileblock")
class WhileBlockAST(BlockAST):
	"""
	AST node for a ``<?while?>`` loop.

	For example ::

		<?while c?>
			body
		<?end for?>

	Attributes are:

	``condition`` : :class:`AST`
		The condition which must be true to continue executing the loops booy
		(``c`` in the above example).

	``content`` : :class:`list` of :class:`AST` objects
		The loop body (``body`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = BlockAST.ul4_attrs.union({"condition"})

	def __init__(self, template=None, startpos=None, stoppos=None, condition=None):
		super().__init__(template, startpos, stoppos)
		self.condition = condition

	def _repr(self):
		yield f"condition={self.condition!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("condition=")
		p.pretty(self.condition)
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.condition)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.condition = decoder.load()

	def _str(self):
		yield "while "
		yield from CodeAST._str(self)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	@_handleoutputeval
	def eval(self, context):
		while 1:
			condition = self.condition.eval(context)
			if not condition:
				break
			try:
				yield from super().eval(context)
			except BreakException:
				break
			except ContinueException:
				pass


@register("break")
class BreakAST(CodeAST):
	"""
	AST node for a ``<?break?>`` tag inside a ``<?for?>`` loop.
	"""

	ul4_type = Type("ul4")

	def _str(self):
		yield "break"

	@_handleexpressioneval
	def eval(self, context):
		raise BreakException()


@register("continue")
class ContinueAST(CodeAST):
	"""
	AST node for a ``<?continue?>`` tag inside a ``<?for?>`` block.
	"""

	ul4_type = Type("ul4")

	def _str(self):
		yield "continue"

	@_handleexpressioneval
	def eval(self, context):
		raise ContinueException()


@register("attr")
class AttrAST(CodeAST):
	"""
	AST node for an expression that gets or sets an attribute of an object.
	(e.g. ``x.y``).

	Attributes are:

	``obj`` : :class:`AST`
		The object from which to get the attribute (``x`` in the above example);

	``attrname`` : :class:`str`
		The name of the attribute (``"y"`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = AST.ul4_attrs.union({"obj", "attrname"})

	def __init__(self, template=None, startpos=None, obj=None, attrname=None):
		super().__init__(template, startpos)
		self.obj = obj
		self.attrname = attrname

	def _repr(self):
		yield f"obj={self.obj!r}"
		yield f"attrname={self.attrname!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		p.breakable()
		p.text("attrname=")
		p.pretty(self.attrname)

	@_handleexpressioneval
	def eval(self, context):
		obj = self.obj.eval(context)
		try:
			return _type(obj).getattr(obj, self.attrname)
		except AttributeError:
			return UndefinedKey(self.attrname)

	@_handleexpressioneval
	def evalset(self, context, value):
		obj = self.obj.eval(context)
		_type(obj).setattr(obj, self.attrname, value)

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		obj = self.obj.eval(context)

		t = _type(obj)
		oldvalue = t.getattr(obj, self.attrname)
		newvalue = operator.evalfoldaug(oldvalue, value)
		t.setattr(obj, self.attrname, newvalue)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.attrname)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.attrname = decoder.load()


@register("slice")
class SliceAST(CodeAST):
	"""
	AST node for creating a slice object (used in ``obj[index1:index2]``).

	Attributes are:

	``index1`` : :class:`AST` or ``None``
		The start index (``index1`` in the above example).

	``index2`` : :class:`AST` or ``None``
		The stop hand side (``y`` in the above example).

	``index1`` and ``index2`` may also be :const:`None` (for missing slice indices,
	which default to the 0 for the start index and the length of the sequence for
	the end index).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"index1", "index2"})

	def __init__(self, template=None, startpos=None, index1=None, index2=None):
		super().__init__(template, startpos)
		self.index1 = index1
		self.index2 = index2

	def _repr(self):
		if self.index1 is not None:
			yield f"index1={self.index1!r}"
		if self.index2 is not None:
			yield f"index2={self.index2!r}"

	def _repr_pretty(self, p):
		if self.index1 is not None:
			p.breakable()
			p.text("index1=")
			p.pretty(self.index1)
		if self.index2 is not None:
			p.breakable()
			p.text("index2=")
			p.pretty(self.index2)

	@_handleexpressioneval
	def eval(self, context):
		index1 = None
		if self.index1 is not None:
			index1 = self.index1.eval(context)
		index2 = None
		if self.index2 is not None:
			index2 = self.index2.eval(context)
		return slice(index1, index2)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.index1)
		encoder.dump(self.index2)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.index1 = decoder.load()
		self.index2 = decoder.load()


class UnaryAST(CodeAST):
	"""
	Base class for all AST nodes implementing unary expressions
	(i.e. operators with one operand).

	Atttributes are:

	``obj`` : :class:`AST`
		The operand of the unary operator.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"obj"})

	def __init__(self, template=None, startpos=None, obj=None):
		super().__init__(template, startpos)
		self.obj = obj

	def _repr(self):
		yield repr(self.obj)

	def _repr_pretty(self, p):
		p.breakable()
		p.pretty(self.obj)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()

	@_handleexpressioneval
	def eval(self, context):
		obj = self.obj.eval(context)
		return self.evalfold(obj)

	@classmethod
	def make(cls, tag, pos, obj):
		if isinstance(obj, ConstAST):
			try:
				result = cls.evalfold(obj.value)
				if not isinstance(result, Undefined):
					return ConstAST(tag, pos, result)
			except Exception:
				pass # If constant folding doesn't work, return the original AST
		return cls(tag, pos, obj)


@register("not")
class NotAST(UnaryAST):
	"""
	AST node for a unary "not" expression (e.g. ``not x``).

	Attributes are:

	``obj`` : :class:`AST`
		The operand (``x`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj):
		return not obj


@register("neg")
class NegAST(UnaryAST):
	"""
	AST node for a unary negation expression (e.g. ``-x``).

	Attributes are:

	``obj`` : :class:`AST`
		The operand (``x`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj):
		return -obj


@register("bitnot")
class BitNotAST(UnaryAST):
	"""
	AST node for a bitwise unary "not" expression that returns its operand
	with its bits inverted (e.g. ``~x``).

	Attributes are:

	``obj`` : :class:`AST`
		The operand (``x`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj):
		return ~obj


@register("print")
class PrintAST(UnaryAST):
	"""
	AST node for a ``<?print?>`` tag (e.g. ``<?print x?>``).

	Attributes are:

	``obj`` : :class:`AST`
		The object to be printed (``x`` in the above example).
	"""

	ul4_type = Type("ul4")

	output = True

	def _str(self):
		yield "print "
		yield from super()._str()

	@_handleoutputeval
	def eval(self, context):
		yield context.output(_str(self.obj.eval(context)))


@register("printx")
class PrintXAST(UnaryAST):
	"""
	AST node for a ``<?printx?>`` tag (e.g. ``<?printx x?>``).

	Attributes are:

	``obj`` : :class:`AST`
		The object to be printed (``x`` in the above example).
	"""

	ul4_type = Type("ul4")

	output = True

	def _str(self):
		yield "printx "
		yield from super()._str()

	@_handleoutputeval
	def eval(self, context):
		yield context.output(_xmlescape(self.obj.eval(context)))


@register("return")
class ReturnAST(UnaryAST):
	"""
	AST node for a ``<?return?>`` tag (e.g. ``<?return x?>``).

	Attributes are:

	``obj`` : :class:`AST`
		The operand (``x`` in the above example).
	"""

	ul4_type = Type("ul4")

	def _str(self):
		yield "return "
		yield from super()._str()

	@_handleexpressioneval
	def eval(self, context):
		value = self.obj.eval(context)
		raise ReturnException(value)


class BinaryAST(CodeAST):
	"""
	Base class for all UL4 AST nodes implementing binary expressions
	(i.e. operators with two operands).

	``obj1`` : :class:`AST`
		The first operand.

	``obj2`` : :class:`AST`
		The second operand.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"obj1", "obj2"})

	def __init__(self, template=None, startpos=None, obj1=None, obj2=None):
		super().__init__(template, startpos)
		self.obj1 = obj1
		self.obj2 = obj2

	def _repr(self):
		yield repr(self.obj1)
		yield repr(self.obj2)

	def _repr_pretty(self, p):
		p.breakable()
		p.pretty(self.obj1)
		p.breakable()
		p.pretty(self.obj2)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj1)
		encoder.dump(self.obj2)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj1 = decoder.load()
		self.obj2 = decoder.load()

	@_handleexpressioneval
	def eval(self, context):
		obj1 = self.obj1.eval(context)
		obj2 = self.obj2.eval(context)
		return self.evalfold(obj1, obj2)

	@classmethod
	def make(cls, tag, pos, obj1, obj2):
		if isinstance(obj1, ConstAST) and isinstance(obj2, ConstAST):
			try:
				result = cls.evalfold(obj1.value, obj2.value)
				if not isinstance(result, Undefined):
					return ConstAST(tag, pos, result)
			except Exception:
				pass # If constant folding doesn't work, return the original AST
		return cls(tag, pos, obj1, obj2)


@register("item")
class ItemAST(BinaryAST):
	"""
	AST node for subscripting expression (e.g. ``x[y]``).

	Attributes are:

	``obj1`` : :class:`AST`
		The container object, which must be a list, string or dict
		(``x`` in the above example).

	``obj2`` : :class:`AST`
		The index/key object (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		try:
			return obj1[obj2]
		except KeyError:
			return UndefinedKey(obj2)

	@_handleexpressioneval
	def evalset(self, context, value):
		obj1 = self.obj1.eval(context)
		obj2 = self.obj2.eval(context)
		obj1[obj2] = value

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		obj1 = self.obj1.eval(context)
		obj2 = self.obj2.eval(context)
		oldvalue = obj1[obj2]
		newvalue = operator.evalfoldaug(oldvalue, value)
		obj1[obj2] = newvalue


@register("is")
class IsAST(BinaryAST):
	"""
	AST node for a binary ``is`` comparison expression (e.g. ``x is y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 is obj2


@register("isnot")
class IsNotAST(BinaryAST):
	"""
	AST node for a binary ``is not`` comparison expression (e.g. ``x is not y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 is not obj2


@register("eq")
class EQAST(BinaryAST):
	"""
	AST node for the binary equality comparison (e.g. ``x == y``.

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 == obj2


@register("ne")
class NEAST(BinaryAST):
	"""
	AST node for a binary inequalitiy comparison (e.g. ``x != y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 != obj2


@register("lt")
class LTAST(BinaryAST):
	"""
	AST node for the binary "less than" comparison (e.g. ``x < y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 < obj2


@register("le")
class LEAST(BinaryAST):
	"""
	AST node for the binary "less than or equal" comparison (e.g. ``x <= y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 <= obj2


@register("gt")
class GTAST(BinaryAST):
	"""
	AST node for the binary "greater than" comparison (e.g. ``x > y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 > obj2


@register("ge")
class GEAST(BinaryAST):
	"""
	AST node for the binary "greater than or equal" comparison (e.g. ``x >= y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 >= obj2


@register("contains")
class ContainsAST(BinaryAST):
	"""
	AST node for the binary containment testing operator (e.g. ``x in y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The item/key object (``x`` in the above example).

	``obj2`` : :class:`AST`
		The container object (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 in obj2


@register("notcontains")
class NotContainsAST(BinaryAST):
	"""
	AST node for an inverted containment testing expression (e.g. ``x not in y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The item/key object (``x`` in the above example).

	``obj2`` : :class:`AST`
		The container object (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 not in obj2


@register("add")
class AddAST(BinaryAST):
	"""
	AST node for a binary addition expression that adds its two operands and
	returns the result  (e.g. ``x + y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left summand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right summand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 + obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 += obj2
		return obj1


@register("sub")
class SubAST(BinaryAST):
	"""
	AST node for the binary subtraction operator.
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 - obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 -= obj2
		return obj1


@register("mul")
class MulAST(BinaryAST):
	"""
	AST node for the binary multiplication expression (e.g. ``x * y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left factor (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right factor (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 * obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 *= obj2
		return obj1


@register("floordiv")
class FloorDivAST(BinaryAST):
	"""
	AST node for a binary truncating division expression (e.g. ``x // y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The dividend (``x`` in the above example).

	``obj2`` : :class:`AST`
		The divisor (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 // obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 //= obj2
		return obj1


@register("truediv")
class TrueDivAST(BinaryAST):
	"""
	AST node for a binary true division expression (e.g. ``x / y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The dividend (``x`` in the above example).

	``obj2`` : :class:`AST`
		The divisor (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 / obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 /= obj2
		return obj1


@register("mod")
class ModAST(BinaryAST):
	"""
	AST node for a binary modulo expression (e.g. ``x % y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		return obj1 % obj2

	@classmethod
	def evalfoldaug(cls, obj1, obj2):
		obj1 %= obj2
		return obj1


@register("shiftleft")
class ShiftLeftAST(BinaryAST):
	"""
	AST node for a bitwise left shift expression (e.g. ``x << y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

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
class ShiftRightAST(BinaryAST):
	"""
	AST node for a bitwise right shift expression (e.g. ``x >> y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

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
class BitAndAST(BinaryAST):
	"""
	AST node for a binary bitwise "and" expression (e.g ``x & y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

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
class BitXOrAST(BinaryAST):
	"""
	AST node for the binary bitwise "exclusive or" expression (e.g. ``x ^ y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

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
class BitOrAST(BinaryAST):
	"""
	AST node for a binary bitwise "or" expression (e.g. ``x | y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

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
class AndAST(BinaryAST):
	"""
	AST node for the binary "and" expression (i.e. ``x and y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		# This is not called from ``eval``, as it doesn't short-circuit
		return obj1 and obj2

	@_handleexpressioneval
	def eval(self, context):
		obj1 = self.obj1.eval(context)
		if not obj1:
			return obj1
		return self.obj2.eval(context)


@register("or")
class OrAST(BinaryAST):
	"""
	AST node for a binary "or" expression (e.g. ``x or y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The item/key object (``x`` in the above example).

	``obj2`` : :class:`AST`
		The container object (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@classmethod
	def evalfold(cls, obj1, obj2):
		# This is not called from ``eval``, as it doesn't short-circuit
		return obj1 or obj2

	@_handleexpressioneval
	def eval(self, context):
		obj1 = self.obj1.eval(context)
		if obj1:
			return obj1
		return self.obj2.eval(context)


@register("if")
class IfAST(CodeAST):
	"""
	AST node for the ternary inline ``if/else`` operator (e.g. ``x if y else z``).

	Attributes are:

	``objif`` : :class:`AST`
		The value of the ``if/else`` expression when the condition is true
		(``x`` in the above example).

	``objcond`` : :class:`AST`
		The condition (``y`` in the above example).

	``objelse`` : :class:`AST`
		The value of the ``if/else`` expression when the condition is false
		(``z`` in the above example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"objif", "objcond", "objelse"})

	def __init__(self, template=None, startpos=None, objif=None, objcond=None, objelse=None):
		super().__init__(template, startpos)
		self.objif = objif
		self.objcond = objcond
		self.objelse = objelse

	def _repr(self):
		yield f"objif={self.objif!r}"
		yield f"objcond={self.objcond!r}"
		yield f"objelse={self.objelse!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.pretty(self.objif)
		p.breakable()
		p.pretty(self.objcond)
		p.breakable()
		p.pretty(self.objelse)

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
	def make(cls, tag, pos, objif, objcond, objelse):
		if isinstance(objcond, ConstAST) and not isinstance(objcond.value, Undefined):
			return objif if objcond.value else objelse
		return cls(tag, pos, objif, objcond, objelse)

	@_handleexpressioneval
	def eval(self, context):
		if self.objcond.eval(context):
			return self.objif.eval(context)
		else:
			return self.objelse.eval(context)


class ChangeVarAST(CodeAST):
	"""
	Base class for all AST nodes that are assignment operators, i.e. that
	set or modify a variable/attribute or item.

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side, i.e. the value that will be modified.

	``value`` : :class:`AST`
		The right hand side, the value that will be assigned or be used to modify
		the intial value.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"lvalue", "value"})

	def __init__(self, template=None, startpos=None, lvalue=None, value=None):
		super().__init__(template, startpos)
		self.lvalue = lvalue
		self.value = value

	def _repr(self):
		yield f"lvalue={self.lvalue!r}"
		yield f"value={self.value!r}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("lvalue=")
		p.pretty(self.lvalue)
		p.breakable()
		p.text("value=")
		p.pretty(self.value)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.lvalue)
		encoder.dump(self.value)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.lvalue = decoder.load()
		self.value = decoder.load()


@register("setvar")
class SetVarAST(ChangeVarAST):
	"""
	AST node for setting a variable, attribute or item to a value (e.g.
	``x = y``).

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalset(context, value)


@register("addvar")
class AddVarAST(ChangeVarAST):
	"""
	AST node for an augmented assignment expression that adds a value to a
	variable (e.g. ``x += y``).

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, AddAST, value)


@register("subvar")
class SubVarAST(ChangeVarAST):
	"""
	AST node for an augmented assignment expression that subtracts a value from
	a variable/attribute/item. (e.g. ``x -= y``).

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, SubAST, value)


@register("mulvar")
class MulVarAST(ChangeVarAST):
	"""
	AST node for an augmented assignment expression that assigns the result
	of a multiplication to its left operand. (e.g. ``x *= y``).

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, MulAST, value)


@register("floordivvar")
class FloorDivVarAST(ChangeVarAST):
	"""
	AST node for augmented assignment expression that divides a variable by a
	value, truncating to an integer value (e.g. ``x //= y``).

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, FloorDivAST, value)


@register("truedivvar")
class TrueDivVarAST(ChangeVarAST):
	"""
	AST node for an augmented assignment expression that assigns the result
	of a truncation division to its left operand. (e.g. ``x //= y``).

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, TrueDivAST, value)


@register("modvar")
class ModVarAST(ChangeVarAST):
	"""
	AST node for an augmented assignment expression that assigns the result
	of a modulo expression to its left operand. (e.g. ``x %= y``).

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, ModAST, value)


@register("shiftleftvar")
class ShiftLeftVarAST(ChangeVarAST):
	"""
	AST node for an augmented assignment expression that assigns the result
	of a "shift left" expression to its left operand. (e.g. ``x <<= y``).

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, ShiftLeftAST, value)


@register("shiftrightvar")
class ShiftRightVarAST(ChangeVarAST):
	"""
	AST node for an augmented assignment expression that assigns the result
	of a "shift right" expression to its left operand. (e.g. ``x >>= y``).

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, ShiftRightAST, value)


@register("bitandvar")
class BitAndVarAST(ChangeVarAST):
	"""
	AST node for an augmented assignment expression that assigns the result
	of a binary bitwise "and" expression to its left operand.
	(e.g. ``x &= y``).

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, BitAndAST, value)


@register("bitxorvar")
class BitXOrVarAST(ChangeVarAST):
	"""
	AST node for an augmented assignment expression that assigns the result
	of a binary bitwise "exclusive or" expression to its left operand.
	(e.g. ``x ^= y``).

	Attributes are:

	``obj1`` : :class:`AST`
		The left operand (``x`` in the above example).

	``obj2`` : :class:`AST`
		The right operand (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, BitXOrAST, value)


@register("bitorvar")
class BitOrVarAST(ChangeVarAST):
	"""
	AST node for an augmented assignment expression that assigns the result
	of a binary bitwise "or" expression to its left operand.
	(e.g. ``x |= y``).

	Attributes are:

	``lvalue`` : :class:`AST`
		The left hand side (``x`` in the above example).

	``value`` : :class:`AST`
		The right hand side (``y`` in the above example).
	"""

	ul4_type = Type("ul4")

	@_handleexpressioneval
	def eval(self, context):
		value = self.value.eval(context)
		for (lvalue, value) in _unpackvar(self.lvalue, value):
			lvalue.evalmodify(context, BitOrAST, value)


@register("call")
class CallAST(CodeAST):
	"""
	AST node for calling an object (e.g. ``f(x, y)``).

	Attributes are:

	``obj`` : :class:`AST`
		The object to be called (``f`` in the above example);

	``args`` : :class:`list`
		The arguments to the call as a :class:`list` of :class:`PositionalArgumentAST`,
		:class:`KeywordArgumentAST`, :class:`UnpackListArgumentAST` or
		:class:`UnpackDictArgumentAST` objects (``x`` and ``y`` in the above
		example).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"obj", "args"})

	def __init__(self, template=None, startpos=None, obj=None):
		super().__init__(template, startpos)
		self.obj = obj
		self.args = []

	def _repr(self):
		yield f"obj={self.obj!r}"
		for arg in self.args:
			yield from arg._repr()

	def _repr_pretty(self, p):
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		for arg in self.args:
			p.breakable()
			p.pretty(arg)

	@staticmethod
	def _call(context, obj, args, kwargs):
		ul4_call = getattr(obj, "ul4_call", None)
		if callable(ul4_call):
			obj = ul4_call

		needscontext = getattr(obj, "ul4_context", False)

		if needscontext:
			return obj(context, *args, **kwargs)
		else:
			return obj(*args, **kwargs)

	def eval(self, context):
		obj = self.obj.eval(context)
		args = []
		kwargs = {}
		for arg in self.args:
			arg.eval_call(context, args, kwargs)

		try:
			return self._call(context, obj, args, kwargs)
		except Exception as exc:
			if inspect.ismethod(obj):
				_decorateexception(exc, self, obj.__self__)
			else:
				_decorateexception(exc, self, obj)
			raise

	@_handleexpressioneval
	def evalset(self, context, value):
		raise TypeError("can't use = on call result")

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		raise TypeError("augmented assigment not allowed for call result")

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.obj)
		encoder.dump(self.args)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.obj = decoder.load()
		self.args = decoder.load()


@register("render")
class RenderAST(CallAST):
	"""
	AST node for rendering a template (e.g. ``<?render t(x)?>``.

	Attributes are:

	``obj`` : :class:`AST`
		The object to be rendered (``t`` in the above example);

	``args`` : :class:`list`
		The arguments to the call as a :class:`list` of
		:class:`PositionalArgumentAST`, :class:`KeywordArgumentAST`,
		:class:`UnpackListArgumentAST` or :class:`UnpackDictArgumentAST` objects.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CallAST.ul4_attrs.union({"indent"})

	def __init__(self, template=None, startpos=None, obj=None):
		super().__init__(template, startpos, obj)
		self.indent = None # The indentation before this ``<?render?>``/``<?renderx?>`` tag, i.e. the sibling AST node before ``self``

	output = True

	def _repr(self):
		yield f"indent={self.indent!r}"
		yield f"obj={self.obj!r}"
		for arg in self.args:
			yield from arg._repr()

	def _repr_pretty(self, p):
		p.breakable()
		p.text("indent=")
		p.pretty(self.indent)
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		for arg in self.args:
			p.breakable()
			p.pretty(arg)

	def _evalobjargs(self, context):
		obj = self.obj.eval(context)
		args = []
		kwargs = {}
		for arg in self.args:
			arg.eval_call(context, args, kwargs)
		return (obj, args, kwargs)

	def _renderobject(self, context, obj, args, kwargs):
		try:
			ul4_render = getattr(obj, "ul4_render", None)
			if callable(ul4_render):
				if self.indent is not None:
					context.indents.append(self.indent.text)
				needscontext = getattr(ul4_render, "ul4_context", False)
				if needscontext:
					yield from ul4_render(context, *args, **kwargs)
				else:
					yield from ul4_render(*args, **kwargs)
				if self.indent is not None:
					context.indents.pop()
			else:
				from ll import misc
				raise TypeError(f"{misc.format_class(obj)} object can't be rendered")
		except Exception as exc:
			if inspect.ismethod(obj):
				_decorateexception(exc, self, obj.__self__)
			else:
				_decorateexception(exc, self, obj)
			raise

	def eval(self, context):
		(obj, args, kwargs) = self._evalobjargs(context)
		yield from self._renderobject(context, obj, args, kwargs)

	@_handleexpressioneval
	def evalset(self, context, value):
		raise TypeError("can't use = on call result")

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		raise TypeError("augmented assigment not allowed for call result")

	def _str(self):
		yield self.type
		yield " "
		yield from super()._str()
		if self.indent is not None:
			yield f" with indent {self.indent.text!r}"

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self.indent)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.indent = decoder.load()


@register("renderx")
class RenderXAST(RenderAST):
	"""
	AST node for rendering a template and XML-escaping the output
	(e.g. ``<?renderx t(x)?>``.

	Attributes are:

	``obj`` : :class:`AST`
		The object to be rendered (``t`` in the above example);

	``args`` : :class:`list`
		The arguments to the call as a :class:`list` of
		:class:`PositionalArgumentAST`, :class:`KeywordArgumentAST`,
		:class:`UnpackListArgumentAST` or :class:`UnpackDictArgumentAST` objects.
	"""

	ul4_type = Type("ul4")

	def eval(self, context):
		context.escapes.append(_xmlescape)
		try:
			yield from RenderAST.eval(self, context)
		finally:
			context.escapes.pop()


@register("renderblock")
class RenderBlockAST(RenderAST):
	"""
	AST node for rendering a template via a ``<?renderblock?>`` block and
	passing the content of the block as one additional keyword argument named
	``content``.

	For example ::

		<?renderblock t(a, b)?>
			content
		<?end renderblock?>

	Attributes are:

	``obj`` : :class:`AST`
		The object to be rendered (``t`` in the above example);

	``args`` : :class:`list`
		The arguments to the call as a :class:`list` of
		:class:`PositionalArgumentAST`, :class:`KeywordArgumentAST`,
		:class:`UnpackListArgumentAST` or :class:`UnpackDictArgumentAST` objects
		(``a`` and ``b`` in the above example).

	``content`` : :class:`list` of :class:`AST` objects
		The content of the ``<?renderblock?>`` tag (``content`` in the above
		example) that will be passed as a signatureless template as the keyword
		argument ``content`` to the object.
	"""

	ul4_type = Type("ul4")
	ul4_attrs = RenderAST.ul4_attrs.union({"stoppos", "stopline", "stopcol", "stopsource", "stopsourceprefix", "stopsourcesuffix", "content"})

	def __init__(self, template=None, startpos=None, stoppos=None, obj=None):
		super().__init__(template, startpos, obj)
		self._stoppos = None
		self.content = None

	def append(self, item):
		self.content.content.append(item)

	def finish(self, endtag):
		self.stoppos = endtag.startpos
		self.content.startpos = slice(self.content.startpos.start, self.content.startpos.start)
		self.content.stoppos = slice(endtag.startpos.start, endtag.startpos.start)

	def _pop_trailing_indent(self):
		if self.content is not None:
			return self.content._pop_trailing_indent()
		else:
			return None

	def eval(self, context):
		(obj, args, kwargs) = self._evalobjargs(context)

		# Check that the argument ``content`` hasn't been specified yet
		if "content" in kwargs:
			raise TypeError(f"multiple values for keyword argument 'content'")
		kwargs["content"] = TemplateClosure(self.content, context, None)

		yield from self._renderobject(context, obj, args, kwargs)

	def _str(self):
		yield self.type
		yield " "
		yield from CodeAST._str(self)
		if self.indent is not None:
			yield f" with indent {self.indent.text!r}"
		yield ":"
		yield None
		yield +1
		yield from BlockAST._str(self.content)
		yield -1

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self._stoppos)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.stoppos = decoder.load()
		self.content = decoder.load()


@register("renderblocks")
class RenderBlocksAST(RenderAST):
	"""
	AST node for rendering a template and passing additional arguments via
	nested variable definitions, e.g.::

		<?renderblocks t(a, b)?>
			<?code x = 42?>
			<?def n?>
				...
			<?end def?>
		<?end renderblocks?>

	Attributes are:

	``obj`` : :class:`AST`
		The object to be rendered (``t`` in the above example);

	``args`` : :class:`list`
		The arguments to the call as a :class:`list` of
		:class:`PositionalArgumentAST`, :class:`KeywordArgumentAST`,
		:class:`UnpackListArgumentAST` or :class:`UnpackDictArgumentAST` objects
		(``a`` and ``b`` in the above example).

	``content`` : :class:`list` of :class:`AST` objects
		The content of the ``<?renderblocks?>`` tag. These must be :class:`AST`
		nodes that define variables (e.g. :class:`SetVarAST` (the
		``<?code x = 42?>`` in the above example), or :class:`Template`
		(the ``<?def n?>...<?end def?>`` in the above example)).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = RenderAST.ul4_attrs.union({"stoppos", "stopline", "stopcol", "stopsource", "stopsourceprefix", "stopsourcesuffix", "content"})

	def __init__(self, template=None, startpos=None, stoppos=None, obj=None):
		super().__init__(template, startpos, obj)
		self._stoppos = stoppos
		self.content = []

	def append(self, item):
		self.content.append(item)

	def finish(self, endtag):
		self.stoppos = endtag.startpos

	def _pop_trailing_indent(self):
		if self.content and isinstance(self.content[-1], IndentAST):
			return self.content.pop()
		else:
			return None

	def _str(self):
		yield self.type
		yield " "
		yield from CodeAST._str(self) # Note that :class:`BlockAST` is *not* one of our base classes, but as long as be have the proper attributes...
		if self.indent is not None:
			yield f" with indent {self.indent.text!r}"
		yield ":"
		yield None
		yield +1
		yield from BlockAST._str(self)
		yield -1

	def _repr_pretty(self, p):
		p.breakable()
		p.text("indent=")
		p.pretty(self.indent)
		p.breakable()
		p.text("obj=")
		p.pretty(self.obj)
		for arg in self.args:
			p.breakable()
			p.pretty(arg)
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def _repr(self):
		yield f"indent={self.indent!r}"
		yield f"obj={self.obj!r}"
		for arg in self.args:
			yield from arg._repr()

	def eval(self, context):
		(obj, args, kwargs) = self._evalobjargs(context)

		# Open a new chained variable dict, so we can collect all variables defined inside the block
		with context.chainvars():
			# Evaluate the block content and ignore output
			# (Note that we're not a subclass of :class:`Block`, but have the correct attributes)
			for output in BlockAST.eval(self, context):
				pass

			# Check that we have no duplicate arguments
			vars = context.vars.maps[0]
			for key in vars:
				if key in kwargs:
					raise TypeError(f"multiple values for keyword argument {key!r}")

			# Copy variables from the block into the keyword arguments (but only the outermost map from the chain)
			kwargs.update(vars)

		yield from self._renderobject(context, obj, args, kwargs)

	@_handleexpressioneval
	def evalset(self, context, value):
		raise TypeError("can't use = on call result")

	@_handleexpressioneval
	def evalmodify(self, context, operator, value):
		raise TypeError("augmented assigment not allowed for call result")

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		encoder.dump(self._stoppos)
		encoder.dump(self.content)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		self.stoppos = decoder.load()
		self.content = decoder.load()


@register("template")
class Template(BlockAST):
	"""
	A UL4 template.

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

	For rendering and calling a template with global variables the following
	methods are available: :meth:`render_with_globals`,
	:meth:`renders_with_globals` and :meth:`call_with_globals`.

	A :class:`Template` object is itself an AST node. Evaluating it will store
	a :class:`TemplateClosure` object for this template under the template's name
	in the local variables.
	"""

	ul4_type = InstantiableType("ul4", "Template", "An UL4 template")
	ul4_attrs = BlockAST.ul4_attrs.union({"signature", "doc", "name", "whitespace", "parenttemplate", "fullsource", "renders"})

	version = "51"

	output = False # Evaluating a template doesn't produce output, but simply stores it in a local variable

	def __init__(self, source=None, name=None, *, whitespace="keep", signature=None):
		"""
		Create a :class:`Template` object.

		If ``source`` is :const:`None`, the :class:`Template` remains uninitialized,
		otherwise ``source`` will be compiled.

		``name`` is the name of the template. It will be used in exception
		messages and should be a valid Python identifier.

		``whitespace`` specifies how whitespace is handled in the literal text
		in templates (i.e. the text between the tags):

		``"keep"``
			Whitespace is kept as it is.

		``"strip"``
			Strip linefeeds and the following indentation from the text.
			However trailing whitespace at the end of the line will still be
			honored.

		``"smart"``
			If a line contains only indentation and one tag that isn't a ``print``
			or ``printx`` tag, the indentation and the linefeed after the tag
			will be stripped from the text. Furthermore the additional indentation
			that might be introduced by a ``for``, ``if``, ``elif``, ``else`` or
			``def`` block will be ignored. So for example the output of::

				<?code langs = ["Python", "Java", "Javascript"]?>
				<?if langs?>
					<?for lang in langs?>
						<?print lang?>
					<?end for?>
				<?end if?>

			will simply be::

				Python
				Java
				Javascript

			without any additional empty lines or indentation.

		(Output will always be ignored when calling a template as a function.)

		``signature`` is the signature of the template. For a top level
		template it can be:

		:const:`None`
			The template will accept all keyword arguments.

		An :class:`inspect.Signature` object
			This signature will be used as the signature of the template.

		A callable
			The signature of the callable will be used.

		A string
			The signature as a string, i.e. something like
			``"x, y=42, *args, **kwargs"``. This string will be parsed and
			evaluated to create the signature for the template.

		If the template is a locally defined subtemplate (i.e. a template defined
		by another template via ``<?def t?>...<?end def?>``), ``signature``
		can be:

		:const:`None`
			The template will accept all arguments.

		A :class:`SignatureAST` object
			This AST node will be evaluated at the point of definition of the
			subtemplate to create the final signature of the subtemplate.
		"""
		super().__init__(self, slice(0, 0), None)
		self.whitespace = whitespace
		self.name = name
		self._fullsource = None
		self.docpos = None
		self.parenttemplate = None
		if isinstance(signature, str):
			# The parser needs a tag, and each tag references its template which contains the source.
			# So to make the source of the signature available in the source, we prepend an ``<?ul4?>`` tag
			source = f"<?ul4 {name or ''}({signature})?>{source}"
			signature = None
		elif callable(signature):
			signature = inspect.signature(signature)
		self.signature = signature

		# If we have source code compile it
		if source is not None:
			stop = len(source)
			self.stoppos = slice(stop, stop)
			self._compile(source)
		else:
			self._fullsource = ""
			self.stoppos = self._startpos

	def _repr(self):
		yield f"name={self.name!r}"
		yield f"whitespace={self.whitespace!r}"
		if self.signature is not None:
			yield f"signature={self.signature}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("name=")
		p.pretty(self.name)
		p.breakable()
		p.text("whitespace=")
		p.pretty(self.whitespace)
		if self.signature is not None:
			p.breakable()
			if isinstance(self.signature, SignatureAST):
				p.text("signature=")
				p.pretty(self.signature)
			else:
				p.text(f"signature={self.signature}")
		p.breakable()
		with p.group(4, "content=[", "]"):
			for node in self.content:
				p.breakable()
				p.pretty(node)

	def _str(self):
		yield "def "
		yield self.name if self.name is not None else "unnamed"
		if self.signature is not None:
			if isinstance(self.signature, SignatureAST):
				yield from self.signature._str()
			else:
				yield str(self.signature)
		yield ":"
		yield None
		yield +1
		yield from super()._str()
		yield -1

	@property
	def doc(self):
		return self._fullsource[self.docpos] if self.docpos is not None else None

	def ul4_getattr(self, name):
		if name == "renders":
			return self.ul4_renders
		else:
			return getattr(self, name)

	def ul4ondump(self, encoder):
		# Don't call ``super().ul4ondump()`` first, as we want the version to be first
		encoder.dump(self.version)
		encoder.dump(self.name)
		encoder.dump(self._fullsource)
		encoder.dump(self.whitespace)
		encoder.dump(self.docpos)
		encoder.dump(self.parenttemplate)

		# Signature can be :const:`None` or an instance of :class:`inspect.Signature` or :class:`SignatureAST`
		if self.signature is None or isinstance(self.signature, SignatureAST):
			encoder.dump(self.signature)
		else:
			# Serialize an instance of :class:`inspect.Signature` as a flat list
			# e.g. ['x', 'pk', 'y', 'pk=', 42, args', '*', kwargs', '**'] for the signature ``(x, y=42, *args, **kwargs)``
			dump = []
			for param in self.signature.parameters.values():
				dump.append(param.name)
				if param.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD:
					if param.default is inspect.Parameter.empty:
						dump.append("pk")
					else:
						dump.append( "pk=")
						dump.append(param.default)
				elif param.kind is inspect.Parameter.POSITIONAL_ONLY:
					if param.default is inspect.Parameter.empty:
						dump.append("p")
					else:
						dump.append("p=")
						dump.append(param.default)
				elif param.kind is inspect.Parameter.KEYWORD_ONLY:
					if param.default is inspect.Parameter.empty:
						dump.append("k")
					else:
						dump.append("k=")
					dump.append(param.default)
				elif param.kind is inspect.Parameter.VAR_POSITIONAL:
					dump.append("*")
				elif param.kind is inspect.Parameter.VAR_KEYWORD:
					dump.append("**")
				else:
					raise ValueError(f"can't dump parameter {param.name} of type {param.kind}")
			encoder.dump(dump)

		super().ul4ondump(encoder)

	ul42signature = {
		"pk": inspect.Parameter.POSITIONAL_OR_KEYWORD,
		"pk=": inspect.Parameter.POSITIONAL_OR_KEYWORD,
		"p": inspect.Parameter.POSITIONAL_ONLY,
		"p=": inspect.Parameter.POSITIONAL_ONLY,
		"k": inspect.Parameter.KEYWORD_ONLY,
		"k=": inspect.Parameter.KEYWORD_ONLY,
		"*": inspect.Parameter.VAR_POSITIONAL,
		"**": inspect.Parameter.VAR_KEYWORD,
	}

	def ul4onload(self, decoder):
		version = decoder.load()
		# If the loaded version is :const:`None`, this is not a "compiled" version of the template,
		# but a "source" version. It only contains the info required to compile the template.
		#
		# Not all implementations (i.e. the Javascript one) support this mode.
		#
		# This is implemented so that the PL/SQL version can put templates into UL4ON dumps.
		if version is None: # dump is in "source" form
			self.name = decoder.load()
			source = decoder.load()
			signature = decoder.load()
			self.whitespace = decoder.load()
			if signature is not None:
				source = f"<?ul4 {self.name or ''}({signature})?>{source}"
			# Remove old content, before compiling the source
			self.startpos = slice(0, 0)
			stop = len(source)
			self.stoppos = slice(stop, stop)
			del self.content[:]
			self._compile(source)
		else: # dump is in compiled form
			if version != self.version:
				raise ValueError(f"invalid version, expected {self.version!r}, got {version!r}")
			self.name = decoder.load()
			self._fullsource = decoder.load()
			self.whitespace = decoder.load()
			self.docpos = decoder.load()
			self.parenttemplate = decoder.load()

			dump = decoder.load()
			if dump is None or isinstance(dump, SignatureAST):
				self.signature = dump
			else:
				params = []
				paramname = None
				paramtype = None
				state = 0
				for value in dump:
					if state == 0:
						paramname = value
						state = 1
					elif state == 1:
						paramtype = value
						if paramtype.endswith("="):
							state = 2
						else:
							params.append(inspect.Parameter(paramname, self.ul42signature[paramtype]))
							state = 0
					else:
						params.append(inspect.Parameter(paramname, self.ul42signature[paramtype], default=value))
						state = 0
				self.signature = inspect.Signature(params)
			super().ul4onload(decoder)

	@classmethod
	def loads(cls, data):
		"""
		Loads a template as an UL4ON dump from the string ``data``.
		"""
		from ll import ul4on
		return ul4on.loads(data)

	@classmethod
	def load(cls, stream):
		"""
		Loads the template as an UL4ON dump from the stream ``stream``.
		format.
		"""
		from ll import ul4on
		return ul4on.load(stream)

	def dump(self, stream):
		"""
		Dump the template in compiled UL4ON format to the stream ``stream``.
		"""
		from ll import ul4on
		ul4on.dump(self, stream)

	def dumps(self):
		"""
		Return the template in compiled UL4ON format (as a string).
		"""
		from ll import ul4on
		return ul4on.dumps(self)

	def _renderbound(self, context):
		# Helper method used by :meth:`render` and :meth:`TemplateClosure.render`
		# where arguments have already been bound
		try:
			# Bypass ``self.eval()`` which simply stores the object as a local variable
			# Also bypass ``super().eval()`` as this would add additional stackframe in exception messages
			for node in self.content:
				result = node.eval(context)
				if node.output:
					yield from result
		except ReturnException:
			pass

	@withcontext
	def ul4_render(self, context, /, *args, **kwargs):
		vars = _makevars(self.signature, args, kwargs)
		with context.replacevars(vars):
			yield from self._renderbound(context)

	def render(self, /, *args, **kwargs):
		"""
		Render the template iteratively (i.e. this is a generator).

		``args`` and ``kwargs`` contain the top level positional and keyword
		arguments available to the template code. Positional arguments will
		only be supported if the template has a signature.
		"""
		context = Context()
		yield from self.ul4_render(context, *args, **kwargs)

	def render_with_globals(self, args, kwargs, globals):
		"""
		Render the template iteratively (i.e. this is a generator).

		``args`` and ``kwargs`` contain the top level positional and keyword
		arguments available to the template code. ``globals`` contains global
		variables. Positional arguments will only be supported if the template
		has a signature.
		"""
		context = Context(globals)
		yield from self.ul4_render(context, *args, **kwargs)

	def _rendersbound(self, context):
		# Helper method used by :meth:`renders` and :meth:`TemplateClosure.renders`
		# where arguments have already been bound
		return "".join(self._renderbound(context))

	# This will be exposed to UL4 as ``renders``
	@withcontext
	def ul4_renders(self, context, /, *args, **kwargs):
		vars = _makevars(self.signature, args, kwargs)
		with context.replacevars(vars):
			return self._rendersbound(context)

	def renders(self, /, *args, **kwargs):
		"""
		Render the template as a string.

		``args`` and ``kwargs`` contain the top level positional and keyword
		arguments available to the template code. Positional arguments will only
		be supported if the template has a signature.
		"""
		context = Context()
		return self.ul4_renders(context, *args, **kwargs)

	def renders_with_globals(self, args, kwargs, globals):
		"""
		Render the template as a string.

		``args`` and ``kwargs`` contain the top level positional and keyword
		arguments available to the template code. ``globals`` contains global
		variables. Positional arguments will only be supported if the template
		has a signature.
		"""
		context = Context(globals)
		return self.ul4_renders(context, *args, **kwargs)

	def _callbound(self, context):
		# Helper method used by :meth:`__call__` and :meth:`TemplateClosure.__call__`
		# where arguments have already been bound
		try:
			for output in super().eval(context): # Bypass ``self.eval()`` which simply stores the object as a local variable
				pass # Ignore all output
		except ReturnException as exc:
			return exc.value

	@withcontext
	def ul4_call(self, context, /, *args, **kwargs):
		"""
		Call the template as a function and return the resulting value.

		``args`` and ``kwargs`` contain the top level positional and keyword
		arguments available to the template code. Positional arguments will
		only be supported if the template has a signature.
		"""
		vars = _makevars(self.signature, args, kwargs)
		with context.replacevars(vars):
			return self._callbound(context)

	def __call__(self, /, *args, **kwargs):
		"""
		Call the template as a function and return the resulting value.

		``args`` and ``kwargs`` contain the top level positional and keyword
		arguments available to the template code. Positional arguments will
		only be supported if the template has a signature.
		"""
		context = Context()
		return self.ul4_call(context, *args, **kwargs)

	def call_with_globals(self, args, kwargs, globals):
		"""
		Call the template as a function and return the resulting value.

		``args`` and ``kwargs`` contain the top level positional and keyword
		arguments available to the template code. ``globals`` contains global
		variables. Positional arguments will only be supported if the template
		has a signature.
		"""
		context = Context(globals)
		return self.ul4_call(context, *args, **kwargs)

	def jssource(self):
		"""
		Return the template as the source code of a Javascript function.
		"""
		return f"ul4.loads({_asjson(self.dumps())})"

	def javasource(self):
		"""
		Return the template as Java source code.
		"""
		from ll import misc
		return f"com.livinglogic.ul4.Template.loads({misc.javaexpr(self.dumps())})"

	def _tokenize(self, source):
		"""
		Tokenize the template source code in ``source`` into tags and non-tag
		text.

		This is a generator which produces :class:`Text`/:class:`Tag` objects
		for each tag or non-tag text. It will be called by :meth:`_compile`
		internally.
		"""
		pattern = r"<\?\s*(ul4|whitespace|printx|print|code|for|while|if|elif|else|end|break|continue|def|return|renderblocks|renderblock|renderx|render|note|doc|ignore)(\s*((.|\n)*?)\s*)?\?>"
		# Last position
		pos = 0
		# Nesting level of ``<?ignore?>``/``<?end ignore?>``
		ignore = 0
		# Location of the last active outermost ``<?ignore?>`` block
		last_ignore_tag_pos = None
		last_ignore_code_pos = None
		for match in re.finditer(pattern, source):
			if not ignore and match.start() != pos:
				yield TextAST(self, slice(pos, match.start()))
			tagname = source[slice(*match.span(1))]
			if tagname == "ignore":
				if not ignore:
					# Remember the initial ignore block so we can complain about it
					# if it remains unclosed
					last_ignore_tag_pos = slice(*match.span())
					last_ignore_code_pos = slice(*match.span(3))
				ignore += 1
			elif ignore and tagname == "end" and match.group(3) == "ignore":
				ignore -= 1
			elif not ignore and tagname != "note":
				yield Tag(self, tagname, slice(*match.span()), slice(*match.span(3)))
			pos = match.end()
		end = len(source)
		if not ignore and pos != end:
			yield TextAST(self, slice(pos, end))
		if ignore:
			exc = BlockError("<?ignore?> block unclosed")
			_decorateexception(exc, Tag(self, "ignore", last_ignore_tag_pos, last_ignore_code_pos))
			raise exc

	def _tags2lines(self, tags):
		"""
		Transforms an iterable of tags into an iterable of lines by splitting the
		literal text between the tags into lines.

		A line is a list of nodes and will start with an :class:`Indent` node
		(containing the indenting whitespace if the line is indented, or an empty
		indentation if it isn't) and might end with a :class:`LineEnd` node
		(containing the line feed if the line is terminated (which most lines
		(except maybe the last one) are)).
		"""
		# a list of tags that are all part of one line
		tagline = []

		def append(tag):
			# If this is a new line and it doesn't start with an indentation,
			# add an empty indentation at the start (We always add indentation,
			# as this is used by :class:`RenderAST` to reindent the output of one
			# template when called from inside another template)
			if not tagline and not isinstance(tag, IndentAST):
				tagline.append(IndentAST(tag.template, slice(tag._startpos.start, tag._startpos.start)))
			tagline.append(tag)

		# Yield lines by splitting literal text into multiple chunks (normal text, indentation and lineends)
		wastag = False
		for tag in tags:
			if isinstance(tag, TextAST):
				pos = tag._startpos.start
				for line in tag.text.splitlines(True):
					# Find out if the line ends with a lineend
					linelen = len(line)
					for lineend in self._whitespace_lineends:
						if line.endswith(lineend):
							lineendlen = len(lineend)
							line = line[:-lineendlen]
							linelen -= lineendlen
							break
					else:
						lineendlen = 0

					# Find out how the line is indented
					if wastag:
						lineindentlen = 0
						wastag = False # Done inside the loop, because all lines after the first one must always be checked for indentation
					else:
						lineindentlen = len(line)-len(line.lstrip())
						linelen -= lineindentlen

					# Output the parts we found
					if lineindentlen:
						append(IndentAST(tag.template, slice(pos, pos+lineindentlen)))
						pos += lineindentlen
					if linelen:
						append(TextAST(tag.template, slice(pos, pos+linelen)))
						pos += linelen
					if lineendlen:
						append(LineEndAST(tag.template, slice(pos, pos+lineendlen)))
						pos += lineendlen
						yield tagline
						tagline = []
			else:
				append(tag)
				wastag = True
		if tagline:
			yield tagline

	def _whitespace_keep(self, lines):
		for line in lines:
			yield from line

	def _whitespace_strip(self, lines):
		first = True
		for line in lines:
			for tag in line:
				if first or not isinstance(tag, (IndentAST, LineEndAST)):
					yield tag
					first = False

	_whitespace_lineends = ("\r\n", "\n")

	def _whitespace_smart(self, lines):
		def indent(tagline):
			# Return the indentation of the line
			if tagline:
				return tagline[0].text
			return ""

		def isempty(tagline):
			return all(isinstance(tag, (IndentAST, LineEndAST)) for tag in tagline)

		# Records the starting and ending line number of a block and its indentation
		class Block:
			def __init__(self, start):
				self.start = start
				self.stop = None
				self.indent = None

		# Return the length of the longest common prefix of all strings in ``indents``
		def commonindentlen(indents):
			if not indents:
				return 0
			indent1 = min(indents)
			indent2 = max(indents)
			for (i, c) in enumerate(indent1):
				if c != indent2[i]:
					return i
			return len(indent1)

		# Step 1: Determine the block structure of the lines
		blocks = [] # List of all blocks
		stack = [] # Stack of currently "open" blocks

		newlines = []
		for (i, line) in enumerate(lines):
			linelen = len(line)
			if 2 <= linelen <= 3 and isinstance(line[0], IndentAST) and isinstance(line[1], Tag) and line[1].tag not in ("print", "printx", "render", "renderx") and (linelen == 2 or isinstance(line[2], LineEndAST)):
				tag = line[1]
				# Tags closing a block
				if tag.tag in ("elif", "else", "end"):
					if stack:
						stack[-1].stop = i # Previous block ends before this line
						stack.pop()
				newlines.append((line, stack[:]))
				# Tags opening a block
				if tag.tag in ("for", "if", "def", "elif", "else", "renderblock", "renderblocks"):
					block = Block(i+1) # Block starts on the next line
					stack.append(block)
					blocks.append(block)
			else:
				newlines.append((line, stack[:]))
		# Close open blocks (shouldn't be necessary for properly nested templates)
		for block in stack:
			block.stop = len(lines)

		# Step 2: Find the outer and inner indentation of all blocks
		for block in blocks:
			block.indent = range(
				# outer indent, i.e. the indentation of the start tag of the block
				len(indent(lines[block.start-1])) if block.start else 0,
				# inner indentation (ignoring lines that only contain whitespace)
				commonindentlen([indent(line) for line in itertools.islice(lines, block.start, block.stop) if not isempty(line)]),
			)

		# Step 3: Fix the indentation
		allindents = {}
		for (line, blocks) in newlines:
			if line:
				# use all character for indentation that are not part of the "artificial" indentation introduced in each block
				newindent = "".join(c for (i, c) in enumerate(line[0].text) if not any(i in block.indent for block in blocks))
				# Reuse previous indent string if we already have it (minizes memory usage and UL4ON dump size)
				newindent = allindents.setdefault(newindent, newindent)
				line[0]._settext(newindent)

		# Step 4: Drop whitespace from empty lines or lines that only contain indentation and block tags
		for line in lines:
			if len(line) == 2 and isinstance(line[0], IndentAST) and isinstance(line[1], LineEndAST):
				del line[0]
			elif len(line) == 2 and isinstance(line[0], IndentAST) and isinstance(line[1], Tag) and line[1].tag not in ("print", "printx", "render", "renderx"):
				del line[0]
			elif len(line) == 3 and isinstance(line[0], IndentAST) and isinstance(line[1], Tag) and line[1].tag not in ("print", "printx", "render", "renderx") and isinstance(line[2], LineEndAST):
				del line[2]
				del line[0]
			elif len(line) == 3 and isinstance(line[0], IndentAST) and isinstance(line[1], Tag) and line[1].tag in ("render", "renderx") and isinstance(line[2], LineEndAST):
				del line[2]

		# Step 5: Yield the individual :class:`Tag`/:class:`TextAST` objects
		for line in lines:
			yield from line

	def _parser(self, tag, error):
		from ll import UL4Lexer, UL4Parser
		source = tag.code
		if not source:
			raise ValueError(error)
		stream = antlr3.ANTLRStringStream(source)
		lexer = UL4Lexer.UL4Lexer(stream)
		lexer.tag = tag
		tokens = antlr3.CommonTokenStream(lexer)
		parser = UL4Parser.UL4Parser(tokens)
		parser.tag = tag
		return parser

	def _compile(self, source):
		"""
		Compile the template source code ``source`` into an AST.
		"""
		self._fullsource = source

		if source is None:
			return

		blockstack = [self] # This stack stores the nested for/if/elif/else/def blocks
		templatestack = [self] # This stack stores the nested templates

		def parsedeclaration(tag):
			try:
				return self._parser(tag, "declaration required").definition()
			except Exception as exc:
				_decorateexception(exc, self)
				raise

		def parseexpr(tag):
			return self._parser(tag, "expression required").expression()

		def parsestmt(tag):
			return self._parser(tag, "statement required").statement()

		def parsefor(tag):
			return self._parser(tag, "loop expression required").for_()

		def parsedef(tag):
			return self._parser(tag, "definition required").definition()

		def parserender(tag):
			call = self._parser(tag, "render call required").expression()
			if not isinstance(call, CallAST):
				raise TypeError("render call required")
			tags = dict(render=RenderAST, renderx=RenderXAST, renderblock=RenderBlockAST, renderblocks=RenderBlocksAST)
			render = tags[tag.tag](template=tag.template, startpos=tag.startpos, obj=call.obj)
			render.args = call.args
			if tag.tag == "renderblock":
				# We create the sub template without source so there won't be any compilation done ...
				render.content = Template(None, name="content", whitespace=self.whitespace)
				# ... but then we have to fix the ``fullsource`` and ``startpos`` attributes ourselves
				render.content._fullsource = self._fullsource
				# The stop position will be updated by :meth:`RenderBlock.finish`.
				render.content.startpos = slice(tag.startpos.stop, tag.startpos.stop)
			return render

		tags = self._tokenize(source)
		lines = list(self._tags2lines(tags))

		# Find template declarations and whitespace specification
		for line in lines:
			for tag in line:
				if isinstance(tag, Tag):
					if tag.tag == "ul4":
						(name, signature) = parsedeclaration(tag)
						self.name = name
						if signature is not None:
							signature = signature.eval(Context())
						self.signature = signature
					elif tag.tag == "whitespace":
						whitespace = tag.code
						if whitespace in {"keep", "strip", "smart"}:
							self.whitespace = whitespace
						else:
							try:
								raise ValueError(f"whitespace mode {whitespace!r} unknown")
							except Exception as exc:
								_decorateexception(exc, tag)
								raise

		# Flatten lines and update whitespace according to the whitespace mode specified
		if self.whitespace == "keep":
			tags = self._whitespace_keep(lines)
		elif self.whitespace == "strip":
			tags = self._whitespace_strip(lines)
		elif self.whitespace == "smart":
			tags = self._whitespace_smart(lines)
		else:
			raise ValueError(f"whitespace mode {self.whitespace!r} unknown")

		for tag in tags:
			# Update ``tag.template`` to reference the innermost template
			# (Originally it referenced the outermost one)
			tag.template = templatestack[-1]
			try:
				if isinstance(tag, TextAST):
					blockstack[-1].append(tag)
				elif tag.tag == "doc":
					# Only use the first ``<?doc?>`` tag in each template, ignore all later ones
					if templatestack[-1].docpos is None:
						templatestack[-1].docpos = tag.codepos
				elif tag.tag == "print":
					blockstack[-1].append(PrintAST(templatestack[-1], tag.startpos, parseexpr(tag)))
				elif tag.tag == "printx":
					blockstack[-1].append(PrintXAST(templatestack[-1], tag.startpos, parseexpr(tag)))
				elif tag.tag == "code":
					blockstack[-1].append(parsestmt(tag))
				elif tag.tag == "if":
					block = ConditionalBlocksAST(templatestack[-1], tag.startpos, None, parseexpr(tag))
					blockstack[-1].append(block)
					blockstack.append(block)
				elif tag.tag == "elif":
					if not isinstance(blockstack[-1], ConditionalBlocksAST):
						raise BlockError("<?elif?> doesn't match any <?if?>")
					elif isinstance(blockstack[-1].content[-1], ElseBlockAST):
						raise BlockError("<?else?> already seen in <?if?>")
					blockstack[-1].newblock(ElIfBlockAST(templatestack[-1], tag.startpos, None, parseexpr(tag)))
				elif tag.tag == "else":
					if not isinstance(blockstack[-1], ConditionalBlocksAST):
						raise BlockError("<?else?> doesn't match any <?if?>")
					elif isinstance(blockstack[-1].content[-1], ElseBlockAST):
						raise BlockError("<?else?> already seen in <?if?>")
					blockstack[-1].newblock(ElseBlockAST(templatestack[-1], tag.startpos, None))
				elif tag.tag == "end":
					if len(blockstack) <= 1:
						raise BlockError("not in any block")
					code = tag.code
					if code:
						if code == "if":
							if not isinstance(blockstack[-1], ConditionalBlocksAST):
								raise BlockError("<?end if?> doesn't match any <?if?>")
						elif code == "for":
							if not isinstance(blockstack[-1], ForBlockAST):
								raise BlockError("<?end for?> doesn't match any <?for?>")
						elif code == "while":
							if not isinstance(blockstack[-1], WhileBlockAST):
								raise BlockError("<?end while?> doesn't match any <?while?>")
						elif code == "def":
							if not isinstance(blockstack[-1], Template):
								raise BlockError("<?end def?> doesn't match any <?def?>")
							templatestack.pop()
						elif code == "renderblock":
							if not isinstance(blockstack[-1], RenderBlockAST):
								raise BlockError("<?end renderblock?> doesn't match any <?renderblock?>")
						elif code == "renderblocks":
							if not isinstance(blockstack[-1], RenderBlocksAST):
								raise BlockError("<?end renderblocks?> doesn't match any <?renderblocks?>")
						elif code == "ignore":
							raise BlockError("not in any <?ignore?> block")
						else:
							raise BlockError(f"illegal end value {code!r}")
					last = blockstack.pop()
					last.finish(tag) # Set end position of block
				elif tag.tag == "for":
					block = parsefor(tag)
					blockstack[-1].append(block)
					blockstack.append(block)
				elif tag.tag == "while":
					block = WhileBlockAST(templatestack[-1], tag.startpos, None, parseexpr(tag))
					blockstack[-1].append(block)
					blockstack.append(block)
				elif tag.tag == "break":
					for block in reversed(blockstack):
						if isinstance(block, (ForBlockAST, WhileBlockAST)):
							break
						elif isinstance(block, Template):
							raise BlockError("<?break?> outside of <?for?> loop")
					blockstack[-1].append(BreakAST(templatestack[-1], tag.startpos))
				elif tag.tag == "continue":
					for block in reversed(blockstack):
						if isinstance(block, (ForBlockAST, WhileBlockAST)):
							break
						elif isinstance(block, Template):
							raise BlockError("<?continue?> outside of <?for?> loop")
					blockstack[-1].append(ContinueAST(templatestack[-1], tag.startpos))
				elif tag.tag == "def":
					(name, signature) = parsedef(tag)
					block = Template(None, name=name, whitespace=self.whitespace, signature=signature)
					block.template = block
					block.parenttemplate = templatestack[-1]
					tag.template = block
					templatestack.append(block)
					# The source is always the complete source of the top level template
					# (so that the offsets in all :class:`AST` objects are correct)
					block._fullsource = self._fullsource
					block.startpos = tag.startpos
					blockstack[-1].append(block)
					blockstack.append(block)
				elif tag.tag == "return":
					blockstack[-1].append(ReturnAST(templatestack[-1], tag.startpos, parseexpr(tag)))
				elif tag.tag in {"render", "renderx", "renderblock", "renderblocks"}:
					render = parserender(tag)
					# Find innermost block
					innerblock = blockstack[-1]
					# If we have an indentation before the ``<?render?>`` tag, move it
					# into the ``indent`` attribute of the :class`Render` object,
					# because this indentation must be added to every line that the
					# rendered template outputs.
					render.indent = innerblock._pop_trailing_indent()
					blockstack[-1].append(render)
					if tag.tag in {"renderblock", "renderblocks"}:
						blockstack.append(render)
				elif tag.tag in ("ul4", "whitespace", "note", "doc"):
					# Don't copy declarations, whitespace specification, comments or docstrings over into the syntax tree
					pass
				else: # Can't happen
					raise ValueError(f"unknown tag {tag.tag!r}")
			except Exception as exc:
				_decorateexception(exc, tag)
				raise
		if len(blockstack) > 1:
			exc = BlockError("block unclosed")
			_decorateexception(exc, blockstack[-1])
			raise exc

	# @_handleexpressioneval
	def eval(self, context):
		signature = self.signature
		# If our signature is an AST, we have to evaluate it to get the final :class:`inspect.Signature` object
		if isinstance(signature, SignatureAST):
			signature = signature.eval(context)
		context.vars[self.name] = TemplateClosure(self, context, signature)


@register("signature")
class SignatureAST(CodeAST):
	"""
	AST node for the signature of a locally defined subtemplate.

	Attributes are:

	``params`` : :class:`list`
		The parameter. Each list item is a :class:`tuple` with three items:

		``name`` : :class:`str`
			The name of the argument.

		``type`` : :class:`str`
			The type of the argument. One of:

			-	``pk`` (positional or keyword argument without default)
			-	``pk=`` (positional or keyword argument with default)
			-	``p`` (positional-only argument without default)
			-	``p=`` (positional-only argument with default)
			-	``k`` (keyword-only argument without default)
			-	``k=`` (keyword-only argument with default)
			-	``*`` (argument that collects addition positional arguments)
			-	``**`` (argument that collects addition keyword arguments)

		``default`` : :class:`AST` or ``None``
			The default value for the argument (or ``None`` if the argument
			has no default value).
	"""

	ul4_type = Type("ul4")
	ul4_attrs = CodeAST.ul4_attrs.union({"params"})

	def __init__(self, template=None, startpos=None):
		super().__init__(template, startpos)
		self.params = []

	def __repr__(self):
		params = []
		lastparamtype = None
		for (paramname, paramtype, default) in self.params:
			sep = self._sep(lastparamtype, paramtype)
			lastparamtype = paramtype
			params.append(sep)
			if paramtype in {"*", "**"}:
				params.append(paramtype)
			params.append(paramname)
			if paramtype.endswith("="):
				params.append(f"={default!r}")
		params = "".join(params)
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} {_offset(self.pos)} ({params}) at {id(self):#x}>"

	def _repr_pretty(self, p):
		for (paramname, default) in self.params:
			p.breakable()
			if default is None:
				p.text(paramname)
			else:
				p.text(f"{paramname}=")
				p.pretty(default)

	def _str(self):
		yield "("
		lastparamtype = None
		for (i, (paramname, paramtype, default)) in enumerate(self.params):
			sep = self._sep(lastparamtype, paramtype)
			lastparamtype = paramtype
			if sep:
				yield sep
			yield paramname
			if paramtype.endswith("="):
				yield "="
				yield from default._str()
		yield ")"

	def _sep(self, lastparamtype, paramtype):
		if lastparamtype is None:
			return "*, " if paramtype in {"k", "k="} else ""
		elif lastparamtype in {"pk", "pk="}:
			return ", *, " if paramtype in {"k", "k="} else ", "
		elif lastparamtype in {"p", "p="}:
			if paramtype in {"pk", "pk="}:
				return ", /, "
			elif paramtype in {"k", "k="}:
				return ", /, *, "
			else:
				return ", "
		else:
			return ", "

	@_handleexpressioneval
	def eval(self, context):
		params = []
		for (paramname, paramtype, default) in self.params:
			if paramtype == "*":
				kind = inspect.Parameter.VAR_POSITIONAL
				default = inspect.Parameter.empty
			elif paramtype	 == "**":
				kind = inspect.Parameter.VAR_KEYWORD
				default = inspect.Parameter.empty
			elif paramtype == "pk":
				kind = inspect.Parameter.POSITIONAL_OR_KEYWORD
				default = inspect.Parameter.empty
			elif paramtype == "pk=":
				kind = inspect.Parameter.POSITIONAL_OR_KEYWORD
				default = default.eval(context)
			elif paramtype == "p":
				kind = inspect.Parameter.POSITIONAL_ONLY
				default = inspect.Parameter.empty
			elif paramtype == "p=":
				kind = inspect.Parameter.POSITIONAL_ONLY
				default = default.eval(context)
			elif paramtype == "k":
				kind = inspect.Parameter.KEYWORD_ONLY
				default = inspect.Parameter.empty
			elif paramtype == "k=":
				kind = inspect.Parameter.KEYWORD_ONLY
				default = default.eval(context)
			params.append(inspect.Parameter(paramname, kind, default=default))
		return inspect.Signature(params)

	def ul4ondump(self, encoder):
		super().ul4ondump(encoder)
		dump = []
		for (paramname, paramtype, default) in self.params:
			dump.append(paramname)
			dump.append(paramtype)
			if paramtype.endswith("="):
				dump.append(default)
		encoder.dump(dump)

	def ul4onload(self, decoder):
		super().ul4onload(decoder)
		dump = decoder.load()
		state = 0
		for value in dump:
			if state == 0:
				paramname = value
				state = 1
			elif state == 1:
				paramtype = value
				if paramtype.endswith("="):
					state = 2
				else:
					self.params.append((paramname, paramtype, None))
					state = 0
			else:
				self.params.append((paramname, paramtype, value))
				state = 0


###
### Various versions of undefined objects
###

class Undefined:
	ul4_type = Type(None, "undefined")

	def __bool__(self):
		return False

	def __iter__(self):
		raise TypeError(f"{self!r} is not iterable")

	def __len__(self):
		raise AttributeError(f"{self!r} has no len()")

	def __call__(self, *args, **kwargs):
		raise TypeError(f"{self!r} is not callable")

	def __getattr__(self, key):
		raise AttributeError(f"{self!r} has no attribute {key!r}")

	def __getitem__(self, key):
		raise TypeError(f"{self!r} is not subscriptable (key={key!r})")


class UndefinedKey(Undefined):
	ul4_type = Type(None, "undefinedkey")

	def __init__(self, key):
		self._key = key

	def __repr__(self):
		return f"UndefinedKey({self._key!r})"


class UndefinedVariable(Undefined):
	ul4_type = Type(None, "undefinedvariable")

	def __init__(self, name):
		self._name = name

	def __repr__(self):
		return f"UndefinedVariable({self._name!r})"


###
### Functions
###

def _now():
	# Wrap this in our own function, because :meth:`datateimt.datetime.now` supports a ``tz`` argument.
	return datetime.datetime.now()


def _csv(obj, /):
	if obj is None:
		return ""
	elif isinstance(obj, Undefined):
		return ""
	elif not isinstance(obj, str):
		obj = _repr(obj)
	if any(c in obj for c in ',"\n'):
		text = obj.replace('"', '""')
		return f'"{text}"'
	return obj


def _fromjson(string, /):
	# Wrap this in our own function, because :func:`json.loads` supports a many more arguments.
	return json.loads(string)


def _fromul4on(dump, /):
	# Wrap this in our own function, because we don't want to support the ``registry`` argument
	from ll import ul4on
	return ul4on.loads(dump)


def _enumfl(iterable, /, start=0):
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


def _isundefined(obj, /):
	return isinstance(obj, Undefined)


def _isdefined(obj, /):
	return not isinstance(obj, Undefined)


def _isnone(obj, /):
	return obj is None


def _isstr(obj, /):
	return isinstance(obj, str)


def _isint(obj, /):
	return isinstance(obj, int) and not isinstance(obj, bool)


def _isfloat(obj, /):
	return isinstance(obj, float)


def _isbool(obj, /):
	return isinstance(obj, bool)


def _isdate(obj, /):
	return isinstance(obj, datetime.date) and not isinstance(obj, datetime.datetime)


def _isdatetime(obj, /):
	return isinstance(obj, datetime.datetime)


def _istimedelta(obj, /):
	return isinstance(obj, datetime.timedelta)


def _ismonthdelta(obj, /):
	from ll import misc
	return isinstance(obj, misc.monthdelta)


def _isexception(obj, /):
	return isinstance(obj, BaseException)


def _islist(obj, /):
	from ll import color
	return isinstance(obj, abc.Sequence) and not isinstance(obj, (str, color.Color))


def _isset(obj, /):
	return isinstance(obj, (set, frozenset))


def _isdict(obj, /):
	return isinstance(obj, abc.Mapping) and not isinstance(obj, Template)


def _iscolor(obj, /):
	from ll import color
	return isinstance(obj, color.Color)


def _istemplate(obj, /):
	return isinstance(obj, (Template, TemplateClosure))


def _isfunction(obj, /):
	return (callable(obj) and not isinstance(obj, Undefined)) or callable(getattr(obj, "ul4_call", None))


def _isinstance(obj, type, /):
	return type.instancecheck(obj)


def _makekeyfunction(context, key):
	if key is not None:
		if callable(getattr(key, "ul4_call", None)):
			key = key.ul4_call
		elif callable(key):
			key = key.__call__
		if getattr(key, "ul4_context", False):
			key = functools.partial(key, context)
	return key


@withcontext
def _min(context, *args, default=_defaultitem, key=None):
	if default is _defaultitem:
		return min(*args, key=_makekeyfunction(context, key))
	else:
		return min(*args, default=default, key=_makekeyfunction(context, key))


@withcontext
def _max(context, *args, default=_defaultitem, key=None):
	if default is _defaultitem:
		return max(*args, key=_makekeyfunction(context, key))
	else:
		return max(*args, default=default, key=_makekeyfunction(context, key))


@withcontext
def _sorted(context, iterable, /, key=None, reverse=False):
	return sorted(iterable, key=_makekeyfunction(context, key), reverse=reverse)


_py_classes_2_ul4_types = {}

def _type(obj, /):
	ul4type = getattr(obj, "ul4_type", None)
	if ul4type is not None:
		return ul4type
	elif obj is None:
		return NoneType
	elif isinstance(obj, bool):
		return BoolType
	elif isinstance(obj, int):
		return IntType
	elif isinstance(obj, float):
		return FloatType
	elif isinstance(obj, str):
		return StrType
	elif isinstance(obj, (set, frozenset, abc.Set)):
		return SetType
	elif isinstance(obj, (list, tuple, abc.Sequence)):
		return ListType
	elif isinstance(obj, (dict, abc.Mapping)):
		return DictType
	elif isinstance(obj, slice):
		return SliceType
	elif isinstance(obj, datetime.datetime):
		return DateTimeType
	elif isinstance(obj, datetime.date):
		return DateType
	elif isinstance(obj, datetime.timedelta):
		return TimeDeltaType
	else:
		cls = type(obj)
		try:
			return _py_classes_2_ul4_types[cls]
		except KeyError:
			ul4cls = GenericExceptionType if issubclass(cls, BaseException) else GenericType
			result = _py_classes_2_ul4_types[cls] = ul4cls(cls)
			return result


def _randrange(*args):
	return random.randrange(*args)


def _format(obj, fmt, lang=None):
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


def _urlquote(string):
	return urlparse.quote_plus(string)


def _urlunquote(string):
	return urlparse.unquote_plus(string)


def _md5(string, /):
	import hashlib
	return hashlib.md5(string.encode("utf-8")).hexdigest()


def _scrypt(string, /, salt):
	import scrypt
	return scrypt.hash(string, salt, N=16384, r=8, p=1, buflen=128).hex()


def _round(number, /, digits=0):
	result = round(number, digits)
	if digits <= 0:
		result = int(result)
	return result


def _floor(number, /, digits=0):
	if digits:
		if isinstance(number, int):
			if digits > 0:
				return number
			base = 10 ** -digits
			return (number // base) * base
		else:
			base = 10**digits
			result = math.floor(number*base)/base
			if digits < 0:
				return int(result)
		return result
	else:
		return math.floor(number)


def _ceil(number, /, digits=0):
	if digits:
		if isinstance(number, int):
			if digits > 0:
				return number
			base = 10 ** -digits
			return (number + base - 1) // base * base
		else:
			base = 10**digits
			result = math.ceil(number*base)/base
			if digits < 0:
				return int(result)
		return result
	else:
		return math.ceil(number)


def _getattr(obj, attrname, default=None):
	return _type(obj).getattr(obj, attrname, default)


def _setattr(obj, attrname, value):
	return _type(obj).setattr(obj, attrname, value)


def _hasattr(obj, attrname):
	return _type(obj).hasattr(obj, attrname)


def _dir(obj, /):
	return _type(obj).dir(obj)


class TemplateClosure(BlockAST):
	"""
	A locally defined subtemplate.

	A :class:`!TemplateClosure` is a closure, i.e. it can use the local variables
	of the template it is defined in.
	"""
	ul4_type = Type("ul4", "TemplateClosure", "A locally defined UL4 template")
	ul4_attrs = Template.ul4_attrs

	def __init__(self, template, context, signature):
		self.template = template
		self.vars = context.vars.maps[0]
		self.signature = signature

	@withcontext
	def ul4_render(self, context, /, *args, **kwargs):
		vars = _makevars(self.signature, args, kwargs)
		vars = collections.ChainMap(vars, self.vars)
		with context.replacevars(vars):
			# Call :meth:`_renderbound` to bypass binding the arguments again
			# (which wouldn't work anyway as ``self.template.signature`` is an :class:`AST` object)
			yield from self.template._renderbound(context)

	# This will be exposed to UL4 as ``renders``
	@withcontext
	def ul4_renders(self, context, /, *args, **kwargs):
		vars = _makevars(self.signature, args, kwargs)
		vars = collections.ChainMap(vars, self.vars)
		with context.replacevars(vars):
			# Call :meth:`_renderbound` to bypass binding the arguments again
			# (which wouldn't work anyway as ``self.template.signature`` is an :class:`AST` object)
			return self.template._rendersbound(context)

	@withcontext
	def ul4_call(self, context, /, *args, **kwargs):
		vars = _makevars(self.signature, args, kwargs)
		vars = collections.ChainMap(vars, self.vars)
		with context.replacevars(vars):
			# Call :meth:`_renderbound` to bypass binding the arguments again
			# (which wouldn't work anyway as ``self.template.signature`` is an :class:`AST` object)
			return self.template._callbound(context)

	def __getattr__(self, name):
		if name == "renders":
			return self.ul4_renders
		else:
			return getattr(self.template, name)

	def ul4_getattr(self, name):
		if name == "renders":
			return self.ul4_renders
		else:
			return getattr(self, name)

	def _repr(self):
		yield f"name={self.name!r}"
		yield f"whitespace={self.whitespace!r}"
		if self.signature is not None:
			yield f"signature={self.signature}"

	def _repr_pretty(self, p):
		p.breakable()
		p.text("name=")
		p.pretty(self.name)
		p.breakable()
		p.text("whitespace=")
		p.pretty(self.whitespace)
		if self.signature is not None:
			p.breakable()
			p.text(f"signature={self.signature}")
		for node in self.content:
			p.breakable()
			p.pretty(node)
