#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

# import __builtin__ to use property, which is also defined here
import types, inspect, __builtin__

from ll.xist import xsc, parsers
from ll.xist.ns import html, text, docbook

class base(xsc.Element):
	"""
	The base of all element classes. Used for dispatching the
	to conversion targets.
	"""
	register = False
	empty = False

	def convert(self, converter):
		target = converter.target
		if issubclass(target, docbook):
			e = self.convert_docbook(converter)
		elif issubclass(target, html):
			e = self.convert_html(converter)
		else:
			raise ValueError("unknown conversion target %r" % target)
		return e.convert(converter)

class block(base):
	"""
	Base class for all block level elements
	"""
	register = False

class programlisting(block):
	"""
	A literal listing of all or part of a program
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.programlisting(self.content)

	def convert_html(self, converter):
		target = converter.target
		e = target.pre(class_="programlisting")
		for child in self.content:
			child = child.convert(converter)
			if isinstance(child, xsc.Text):
				for c in child.content:
					if c==u"\t":
						if issubclass(target, text):
							c = "   "
						else:
							c = target.span(u"···", class_="tab")
					e.append(c)
			else:
				e.append(child)
		if issubclass(target, text):
			e = target.blockquote(e)
		return e

class example(block):
	"""
	A formal example
	"""
	empty = False

	def convert(self, converter):
		target = converter.target
		ts = xsc.Frag()
		cs = xsc.Frag()
		for child in self:
			if isinstance(child, title):
				ts.append(child)
			else:
				cs.append(child)
		
		if issubclass(target, docbook):
			e = target.example(ts, cs)
		elif issubclass(target, html):
			e = cs
			if issubclass(target, text) and ts:
				e.append(target.div(ts, class_="example-title"))
		return e.convert(converter)

class option(base):
	"""
	An option for a software command
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.option(self.content)

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="option")

class lit(base):
	"""
	Inline text that is some literal value
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.literal(self.content)

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="literal")

class function(base):
	"""
	The name of a function or subroutine, as in a programming language
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.function(self.content)

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="function")

class method(base):
	"""
	The name of a method or memberfunction in a programming language
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.methodname(self.content)

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="method")

class property(base):
	"""
	The name of a property in a programming language
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.varname(self.content, role="property")

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="property")

class class_(base):
	"""
	The name of a class, in the object-oriented programming sense
	"""
	xmlname = "class"
	empty = False

	def convert_docbook(self, converter):
		return converter.target.classname(self.content)

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="class")

class rep(base):
	"""
	Content that may or must be replaced by the user
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.replaceable(self.content)

	def convert_html(self, converter):
		return converter.target.var(self.content, class_="rep")

class markup(base):
	"""
	A string of formatting markup in text that is to be represented literally
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.markup(self.content)

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="markup")

class arg(base):
	"""
	The name of a function or method argument.
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.parameter(self.content)

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="arg")

class module(base):
	"""
	The name of Python module.
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.classname(self.content, role="module")

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="module")

class parameter(base):
	"""
	A value or a symbolic reference to a value
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.parameter(self.content)

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="parameter")

class filename(base):
	"""
	The name of a file
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.filename(self.content)

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="filename")

class dirname(base):
	"""
	The name of directory
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.filename(self.content, class_="directory")

	def convert_html(self, converter):
		return converter.target.code(self.content, class_="dirname")

class app(base):
	"""
	The name of a software program
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.URLAttr): pass

	def convert_docbook(self, converter):
		return converter.target.application(self.content, moreinfo=self["moreinfo"])

	def convert_html(self, converter):
		return converter.target.span(self.content, class_="app")

class title(base):
	"""
	The text of the title of a section of a document or of a formal block-level element
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.title(self.content.convert(converter))

	def convert_html(self, converter):
		return self.content.convert(converter)

class section(block):
	"""
	A recursive section
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class role(xsc.TextAttr): pass

	class Context(xsc.Element.Context):
		def __init__(self):
			xsc.Element.Context.__init__(self)
			self.numbers = [0]

	def convert(self, converter):
		target = converter.target
		if issubclass(target, docbook):
			e = converter.target.section(self.content, role=self["role"])
			return e.convert(converter)
		elif issubclass(target, html):
			context = converter[section]
			context.numbers[-1] += 1
			context.numbers.append(0) # for numbering the subsections
			ts = xsc.Frag()
			cs = xsc.Frag()
			for child in self:
				if isinstance(child, title):
					ts.append(child)
				else:
					cs.append(child)
			e = xsc.Frag()
			for t in ts:
				try:
					hclass = target.element("h%d" % (len(context.numbers)-1))
				except LookupError: # ouch, we're nested to deep (a getter in a property in a class in a class)
					hclass = target.h6
				h = hclass(class_=self["role"])
				if issubclass(target, text):
					h.append(target.br(), t.content, target.br(), "="*len(unicode(t.content.convert(converter))))
				else:
					h.append(t.content)
				e.append(h)
			if self.attrs.has("role"):
				e.append(target.div(cs, class_=self["role"]))
			else:
				e.append(cs)
			# make sure to call the inner convert, because popping the number off of the stack
			e = e.convert(converter)
			del context.numbers[-1]
			return e
		else:
			raise ValueError("unknown conversion target %r" % target)

class par(block):
	"""
	A paragraph
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass

	def convert_docbook(self, converter):
		return converter.target.para(self.content, role=self["type"])

	def convert_html(self, converter):
		return converter.target.p(self.content, class_=self["type"])

class list(block):
	"""
	Common baseclass for <pyref class="ulist"><class>ulist</class></pyref>,
	<pyref class="olist"><class>olist</class></pyref> and
	<pyref class="dlist"><class>dlist</class></pyref>.
	"""
	register = False
	class Context(block.Context):
		def __init__(self):
			self._lists = []
		def get(self):
			return self._lists[-1]
		def push(self, type):
			self._lists.append(type)
		def pop(self):
			return self._lists.pop()

class ulist(list):
	"""
	A list in which each entry is marked with a bullet or other dingbat
	"""
	empty = False

	def convert(self, converter):
		context = converter[list]
		context.push(ulist)
		target = converter.target
		if issubclass(target, docbook):
			node = converter.target.itemizedlist(self.content)
		elif issubclass(target, html):
			node = converter.target.ul(self.content)
		else:
			raise ValueError("unknown conversion target %r" % target)
		return node.convert(converter)
		context.pop()
		return node

class olist(list):
	"""
	A list in which each entry is marked with a sequentially incremented label
	"""
	empty = False

	def convert(self, converter):
		context = converter[list]
		context.push(olist)
		target = converter.target
		if issubclass(target, docbook):
			node = converter.target.orderedlist(self.content)
		elif issubclass(target, html):
			node = converter.target.ol(self.content)
		else:
			raise ValueError("unknown conversion target %r" % target)
		return node.convert(converter)
		context.pop()
		return node

class dlist(list):
	"""
	A list in which each entry is marked with a label
	"""
	empty = False

	def convert(self, converter):
		context = converter[list]
		context.push(dlist)
		target = converter.target
		if issubclass(target, docbook):
			node = converter.target.variablelist()
			collect = converter.target.varlistentry()
			for child in self.content:
				collect.append(child)
				if isinstance(child, item):
					node.append(collect)
					collect = converter.target.varlistentry()
			if collect:
				node.append(collect)
		elif issubclass(target, html):
			node = converter.target.dl(self.content)
		else:
			raise ValueError("unknown conversion target %r" % target)
		return node.convert(converter)
		context.pop()
		return node

class term(base):
	"""
	A term inside a <pyref class="dlist"><class>dlist</class></pyref>
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.term(self.content)

	def convert_html(self, converter):
		return converter.target.dt(self.content)

class item(block):
	"""
	A wrapper for the elements of a list item
	"""
	empty = False

	def convert_docbook(self, converter):
		if self.content.find(type=(par, list, example, programlisting), subtype=True):
			content = self.content
		else:
			content = converter.target.para(self.content)
		return converter.target.listitem(content)

	def convert_html(self, converter):
		context = converter[list]
		if context.get() is dlist:
			return converter.target.dd(self.content)
		else:
			return converter.target.li(self.content)

class self(base):
	"""
	use this class when referring to the object for which a method has been
	called, e.g.:
	<example>
	<programlisting>
		this function fooifies the object &lt;self/&gt;.
	</programlisting>
	</example>
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.varname("self")

	def convert_html(self, converter):
		return converter.target.code("self", class_="self")

	def __unicode__(self):
		return u"self"

class link(base):
	"""
	A hypertext link.
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): pass

	def convert_docbook(self, converter):
		return converter.target.link(self.content, linkend=self["href"])

	def convert_html(self, converter):
		return converter.target.a(self.content, href=self["href"])

class email(base):
	"""
	An email address.
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.email(self.content)

	def convert_html(self, converter):
		return converter.target.a(self.content, href=("mailto:", self.content))

class em(base):
	"""
	Emphasized text:
	"""
	empty = False

	def convert_docbook(self, converter):
		return converter.target.emphasis(self.content)

	def convert_html(self, converter):
		return converter.target.em(self.content)

class pyref(base):
	"""
	reference to a Python object:
	module, class, method, property or function
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class module(xsc.TextAttr): pass
		class class_(xsc.TextAttr): xmlname = "class"
		class method(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class function(xsc.TextAttr): pass

	base = "http://localhost:7464/"

	def convert(self, converter):
		target = converter.target
		if self.attrs.has("function"):
			function = unicode(self["function"].convert(converter))
		else:
			function = None
		if self.attrs.has("method"):
			method = unicode(self["method"].convert(converter))
		else:
			method = None
		if self.attrs.has("property"):
			prop = unicode(self["property"].convert(converter))
		else:
			prop = None
		if self.attrs.has("class_"):
			class__ = unicode(self["class_"].convert(converter)).replace(u".", u"-")
		else:
			class__ = None
		if self.attrs.has("module"):
			module = unicode(self["module"].convert(converter))
			if module.startswith("ll."):
				module = module[3:].replace(u".", u"/")
			else:
				module = None
		else:
			module = None

		e = self.content
		if issubclass(target, html):
			if function is not None:
				if module is not None:
					e = target.a(e, href=(self.base, module, "/index.html#", function))
			elif method is not None:
				if class__ is not None and module is not None:
					e = target.a(e, href=(self.base, module, "/index.html#", class__, "-", method))
			elif prop is not None:
				if class__ is not None and module is not None:
					e = target.a(e, href=(self.base, module, "/index.html#", class__, "-", prop))
			elif class__ is not None:
				if module is not None:
					e = target.a(e, href=(self.base, module, "/index.html#", class__))
			elif module is not None:
				e = target.a(e, href=(self.base, module, "/index.html"))
		return e.convert(converter)

def _getmodulename(thing):
	module = inspect.getmodule(thing)
	if module is None:
		return "???"
	else:
		return module.__name__
_getmodulename = staticmethod(_getmodulename)

def getdoc(cls, thing):
	if thing.__doc__ is None:
		return xsc.Null
	lines = thing.__doc__.split("\n")

	# find first nonempty line
	for i in xrange(len(lines)):
		if lines[i] and not lines[i].isspace():
			if i:
				del lines[:i]
			break

	if len(lines):
		# find starting white space of this line
		startwhite = ""
		for c in lines[0]:
			if c.isspace():
				startwhite += c
			else:
				break

		# remove this whitespace from every line
		for i in xrange(len(lines)):
			if lines[i][:len(startwhite)] == startwhite:
				lines[i] = lines[i][len(startwhite):]

		# remove empty lines
		while len(lines) and lines[0] == "":
			del lines[0]
		while len(lines) and lines[-1] == "":
			del lines[-1]

	text = "\n".join(lines)

	if inspect.ismethod(thing):
		systemId = "METHOD-DOCSTRING(%s.%s.%s)" % (cls._getmodulename(thing), thing.__class__.__name__, thing.__name__)
	elif inspect.isfunction(thing):
		systemId = "FUNCTION-DOCSTRING(%s.%s)" % (cls._getmodulename(thing), thing.__name__)
	elif inspect.isclass(thing):
		systemId = "CLASS-DOCSTRING(%s.%s)" % (cls._getmodulename(thing), thing.__name__)
	elif inspect.ismodule(thing):
		systemId = "MODULE-DOCSTRING(%s)" % cls._getmodulename(thing)
	else:
		systemId = "DOCSTRING"
	node = parsers.parseString(text, systemId=systemId, prefixes=xsc.DocPrefixes())
	if not node.find(type=par): # optimization: one paragraph docstrings don't need a <par> element.
		node = cls.par(node)

	refs = node.find(type=pyref, subtype=1, searchchildren=1)
	if inspect.ismethod(thing):
		for ref in refs:
			if not ref.attrs.has("module"):
				ref["module"] = cls._getmodulename(thing)
				if not ref.attrs.has("class_"):
					ref["class_"] = thing.im_class.__name__
					if not ref.attrs.has("method"):
						ref["method"] = thing.__name__
	elif inspect.isfunction(thing):
		for ref in refs:
			if not ref.attrs.has("module"):
				ref["module"] = cls._getmodulename(thing)
	elif inspect.isclass(thing):
		for ref in refs:
			if not ref.attrs.has("module"):
				ref["module"] = cls._getmodulename(thing)
				if not ref.attrs.has("class_"):
					ref["class_"] = thing.__name__
	elif inspect.ismodule(thing):
		for ref in refs:
			if not ref.attrs.has("module"):
				ref["module"] = thing.__name__
	return node
getdoc = classmethod(getdoc)

canonicalOrder = [
	"__init__", "__del__",
	"__repr__", "__str__", "__unicode__",
	"__hash__",
	"__lt__", "__le__", "__eq__", "__ne__", "__gt__", "__ge__",
	"__cmp__", "__rcmp__", "__nonzero__",
	"__getattr__", "__setattr__", "__delattr__",
	"__call__",
	"__len__", "__getitem__", "__setitem__", "__delitem__", "__getslice__", "__setslice__", "__delslice__", "__contains__",
	"__add__", "__sub__", "__mul__", "__div__", "__mod__", "__divmod__", "__pow__", "__lshift__", "__rshift__", "__and__", "__xor__", "__or__",
	"__radd__", "__rsub__", "__rmul__", "__rdiv__", "__rmod__", "__rdivmod__", "__rpow__", "__rlshift__", "__rrshift__", "__rand__", "__rxor__", "__ror__",
	"__iadd__", "__isub__", "__imul__", "__idiv__", "__imod__", "__ipow__", "__ilshift__", "__irshift__", "__iand__", "__ixor__", "__ior__",
	"__neg__", "__pos__", "__abs__", "__invert__",
	"__complex__", "__int__", "__long__", "__float__", "__oct__", "__hex__", "__coerce__"
]

def _cmpname(cls, (obj1, name1), (obj2, name2)):
	names = [ name1 or obj1.__name__, name2 or obj2.__name__ ]
	sorts = []
	for name in names:
		try:
			pos = cls.canonicalOrder.index(name)
		except ValueError:
			if name.startswith("__"):
				pos = 3000
			elif name.startswith("_"):
				pos = 2000
			else:
				pos = 1000
		sorts.append((pos, name))
	return cmp(sorts[0], sorts[1])
_cmpname = classmethod(_cmpname)

def _codeheader(cls, thing, name, type):
	(args, varargs, varkw, defaults) = inspect.getargspec(thing)
	sig = xsc.Frag()
	sig.append(type(name), "(")
	offset = len(args)
	if defaults is not None:
		offset -= len(defaults)
	for i in xrange(len(args)):
		if i == 0:
			if issubclass(type, method):
				sig.append(cls.arg(cls.self()))
			else:
				sig.append(cls.arg(args[i]))
		else:
			sig.append(", ")
			sig.append(cls.arg(args[i]))
		if i >= offset:
			sig.append("=", repr(defaults[i-offset]))
	if varargs:
		sig.append(", *", cls.arg(varargs))
	if varkw:
		sig.append(", **", cls.arg(varkw))
	sig.append(")")
	return sig
_codeheader = classmethod(_codeheader)

def explain(cls, thing, name=None, context=[]):
	"""
	<par>returns a &xml; representation of the documentation of
	<arg>thing</arg>, which can be a function, method, class or module.</par>

	<par>If <arg>thing</arg> is not a module, you must pass the context
	in <arg>context</arg>, i.e. a list of names of objects into which <arg>thing</arg>
	is nested. This means the first entry will always be module name, and
	the other entries will be class names.</par>
	"""

	if inspect.ismethod(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		(args, varargs, varkw, defaults) = inspect.getargspec(thing.im_func)
		id = "-".join([info[1] for info in context[1:]])
		sig = xsc.Frag(
			html.a(name=id, id=id)
		)
		if name != thing.__name__ and not (thing.__name__.startswith("__") and name=="_" + thing.im_class.__name__ + thing.__name__):
			sig.append(name, " = ")
		sig.append("def ", cls._codeheader(thing.im_func, thing.__name__, cls.method), ":")
		return cls.section(cls.title(sig), cls.getdoc(thing), role="method")
	elif inspect.isfunction(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		id = "-".join([info[1] for info in context[1:]])
		sig = xsc.Frag(
			html.a(name=id, id=id),
			"def ",
			cls._codeheader(thing, name, cls.function),
			":"
		)
		return cls.section(cls.title(sig), cls.getdoc(thing), role="function")
	elif isinstance(thing, __builtin__.property):
		context = context + [(thing, name)]
		id = "-".join([info[1] for info in context[1:]])
		sig = xsc.Frag(
			html.a(name=id, id=id),
			"property ", name, ":"
		)
		node = cls.section(cls.title(sig), cls.getdoc(thing), role="property")
		if thing.fget is not None:
			node.append(cls.explain(thing.fget, "__get__", context))
		if thing.fset is not None:
			node.append(cls.explain(thing.fset, "__set__", context))
		if thing.fdel is not None:
			node.append(cls.explain(thing.fdel, "__delete__", context))
		return node
	elif inspect.isclass(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		id = "-".join([info[1] for info in context[1:]])
		bases = xsc.Frag()
		if len(thing.__bases__):
			for baseclass in thing.__bases__:
				if baseclass.__module__ == "__builtin__":
					ref = cls.class_(baseclass.__name__)
				else:
					try:
						baseclassname = baseclass.__fullname__()
					except AttributeError:
						baseclassname = baseclass.__name__
					if thing.__module__ != baseclass.__module__:
						baseclassname4text = baseclass.__module__ + "." + baseclassname
					else:
						baseclassname4text = baseclassname
					#baseclassname4text = u".\u200b".join(baseclassname4text.split("."))
					ref = cls.pyref(cls.class_(baseclassname4text), module=baseclass.__module__, class_=baseclassname)
				bases.append(ref)
			bases = bases.withsep(", ")
			bases.insert(0, "(")
			bases.append(")")
		node = cls.section(
			cls.title(
				html.a(name=id, id=id),
				"class ",
				cls.class_(name),
				bases,
				":"
			),
			cls.getdoc(thing),
			role="class"
		)
		# find methods, properties and classes, but filter out those methods that are attribute getters, setters or deleters
		methods = []
		properties = []
		classes = []
		for varname in thing.__dict__.keys():
			obj = getattr(thing, varname)
			if isinstance(obj, __builtin__.property):
				properties.append((obj, varname))
			elif inspect.isclass(obj):
				classes.append((obj, varname))
			elif inspect.ismethod(obj):
				# skip the method if it's a property getter, setter or deleter
				for (prop, name) in properties:
					if obj.im_func==prop.fget or obj.im_func==prop.fset or obj.im_func==prop.fdel:
						break
				else:
					methods.append((obj, varname))
		if len(methods):
			methods.sort(cls._cmpname)
			node.append([cls.explain(obj, varname, context) for (obj, varname) in methods])
		if len(properties):
			properties.sort(cls._cmpname)
			node.append([cls.explain(obj, varname, context) for (obj, varname) in properties])
		if len(classes):
			classes.sort(cls._cmpname)
			for (subclass, subname) in classes:
				for (superclass, supername) in context:
					if subclass is superclass: # avoid endless recursion for __outerclass__ which references a class further up in the context path.
						break
				else:
					node.append(cls.explain(subclass, subname, context))
		return node
	elif inspect.ismodule(thing):
		name = name or thing.__name__
		context = [(thing, name)]
		node = cls.section(
			cls.title("Module ", cls.module(name)),
			cls.getdoc(thing)
		)

		functions = []
		classes = []
		for varname in thing.__dict__.keys():
			obj = getattr(thing, varname)
			if inspect.isfunction(obj):
				functions.append((obj, varname))
			elif inspect.isclass(obj):
				classes.append((obj, varname))
		if len(classes):
			classes.sort(cls._cmpname)
			node.append(
				cls.section(
					cls.title("Classes"),
					[cls.explain(obj, name, context) for (obj, name) in classes],
					role="classes"
				)
			)
		if len(functions):
			functions.sort(cls._cmpname)
			node.append(
				cls.section(
					cls.title("Functions"),
					[cls.explain(obj, name, context) for (obj, name) in functions],
					role="functions"
				)
			)
		return node

	return xsc.Null
explain = classmethod(explain)

class xmlns(xsc.Namespace):
	xmlname = "doc"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/doc"
xmlns.makemod(vars())

