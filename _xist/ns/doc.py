#!/usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# __builtin__ to use property, which is also defined here
import types, inspect, __builtin__

from xist import xsc, parsers
from xist.ns import html, docbook

class programlisting(xsc.Element):
	"""
	A literal listing of all or part of a program
	"""
	empty = 0

	def convert(self, converter):
		e = html.pre(class_="programlisting")
		for child in self.content:
			child = child.convert(converter)
			if isinstance(child, xsc.Text):
				for c in child.content:
					if c==u"\t":
						if converter.target=="text":
							c = "   "
						else:
							c = html.span(u"···", class_="tab")
					e.append(c)
			else:
				e.append(child)
		if converter.target=="text":
			e = html.blockquote(e)
		return e.convert(converter)

class example(xsc.Element):
	"""
	A formal example, with a title
	"""
	empty = 0
	attrHandlers = {"title": xsc.TextAttr}

	def convert(self, converter):
		e = xsc.Frag(self.content)
		if converter.target!="text" and self.hasAttr("title"):
			e.append(html.div(self["title"], class_="example-title"))
		return e.convert(converter)

class option(xsc.Element):
	"""
	An option for a software command
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.option(self.content)
		else:
			e = html.code(self.content, class_="option")
		return e.convert(converter)

class lit(xsc.Element):
	"""
	Inline text that is some literal value
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.literal(self.content)
		else:
			e = html.code(self.content, class_="literal")
		return e.convert(converter)

class function(xsc.Element):
	"""
	The name of a function or subroutine, as in a programming language
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.function(self.content)
		else:
			e = html.code(self.content, class_="function")
		return e.convert(converter)

class method(xsc.Element):
	"""
	The name of a method or memberfunction in a programming language
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.methodname(self.content)
		else:
			e = html.code(self.content, class_="method")
		return e.convert(converter)

class property(xsc.Element):
	"""
	The name of a property in a programming language
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.varname(self.content, role="property")
		else:
			e = html.code(self.content, class_="property")
		return e.convert(converter)

class class_(xsc.Element):
	"""
	The name of a class, in the object-oriented programming sense
	"""
	name = "class"
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.classname(self.content)
		else:
			e = html.code(self.content, class_="class")
		return e.convert(converter)

class rep(xsc.Element):
	"""
	Content that may or must be replaced by the user
	"""
	empty = 0

	def convert(self, converter):
		e = html.var(self.content, class_="rep")
		return e.convert(converter)

class markup(xsc.Element):
	"""
	A string of formatting markup in text that is to be represented literally
	"""
	empty = 0

	def convert(self, converter):
		e = html.code(self.content, class_="markup")
		return e.convert(converter)

class arg(xsc.Element):
	"""
	The name of a function or method argument.
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.parameter(self.content)
		else:
			e = html.code(self.content, class_="arg")
		return e.convert(converter)

class module(xsc.Element):
	"""
	The name of Python module.
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.classname(self.content, role="module")
		else:
			e = html.code(self.content, class_="module")
		return e.convert(converter)

class parameter(xsc.Element):
	"""
	A value or a symbolic reference to a value
	"""
	empty = 0

	def convert(self, converter):
		e = html.code(self.content, class_="parameter")
		return e.convert(converter)

class filename(xsc.Element):
	"""
	The name of a file
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr}

	def convert(self, converter):
		e = html.code(self.content, class_="filename")
		return e.convert(converter)

class app(xsc.Element):
	"""
	The name of a software program
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.URLAttr}

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.application(self.content, moreinfo=self["moreinfo"])
		else:
			e = html.span(self.content, class_="app")
			if self.hasAttr("moreinfo"):
				e = html.a(e, href=self["moreinfo"])
		return e.convert(converter)

class title(xsc.Element):
	"""
	The text of the title of a section of a document or of a formal block-level element
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			return docbook.title(self.content.convert(converter))
		else:
			return self.content.convert(converter)

class section(xsc.Element):
	"""
	A recursive section
	"""
	empty = 0
	attrHandlers = {"role": xsc.TextAttr}

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.section(self.content, role=self["role"])
			return e.convert(converter)
		else:
			context = converter[self.__class__]
			if not hasattr(context, "depth"):
				context.depth = 1
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
					hclass = html.namespace.elementsByName["h%d" % context.depth]
				except KeyError: # ouch, we're nested to deep (a getter in a property in a class in a class)
					hclass = html.h6
				h = hclass(class_=self["role"])
				if converter.target=="text":
					h.append(html.br(), t.content, html.br(), "="*len(unicode(t.content.convert(converter))))
				else:
					h.append(t.content)
				e.append(h)
			if self.hasAttr("role"):
				e.append(html.div(cs, class_=self["role"]))
			else:
				e.append(cs)
			context.depth += 1
			e = e.convert(converter)
			context.depth -= 1
			return e

class par(xsc.Element):
	"""
	A paragraph
	"""
	empty = 0
	attrHandlers = {"type": xsc.TextAttr}

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.para(self.content, type=self["type"])
		else:
			e = html.p(self.content, class_=self["type"])
		return e.convert(converter)

class ulist(xsc.Element):
	"""
	A list in which each entry is marked with a bullet or other dingbat
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.itemizedlist(self.content)
		else:
			e = html.ul(self.content)
		return e.convert(converter)

class olist(xsc.Element):
	"""
	A list in which each entry is marked with a sequentially incremented label
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.orderedlist(self.content)
		else:
			e = html.ol(self.content)
		return e.convert(converter)

class item(xsc.Element):
	"""
	A wrapper for the elements of a list item
	"""
	empty = 0

	def convert(self, converter):
		if converter.target=="docbook":
			e = docbook.listitem(self.content)
		else:
			e = html.li(self.content)
		return e.convert(converter)

class self(xsc.Element):
	"""
	use this class when referring to the object for which a method has been
	called, e.g.:
	<doc:example>
	<doc:programlisting>
		this function fooifies the object &lt;self/&gt;.
	</doc:programlisting>
	</doc:example>
	"""
	empty = 0

	def convert(self, converter):
		return html.code("self", class_="self")

class pyref(xsc.Element):
	"""
	reference to a Python object:
	module, class, method, property or function
	"""
	empty = 0
	attrHandlers = {"module": xsc.TextAttr, "class": xsc.TextAttr, "method": xsc.TextAttr, "property": xsc.TextAttr, "function": xsc.TextAttr}

	base = "http://localhost:7464/"

	def convert(self, converter):
		if self.hasAttr("var"):
			var = unicode(self["var"].convert(converter))
		else:
			var = None
		if self.hasAttr("arg"):
			arg = unicode(self["arg"].convert(converter))
		else:
			arg = None
		if self.hasAttr("function"):
			function = unicode(self["function"].convert(converter))
		else:
			function = None
		if self.hasAttr("method"):
			method = unicode(self["method"].convert(converter))
		else:
			method = None
		if self.hasAttr("property"):
			prop = unicode(self["property"].convert(converter))
		else:
			prop = None
		if self.hasAttr("class"):
			class__ = unicode(self["class"].convert(converter)).replace(u".", u"-")
		else:
			class__ = None
		if self.hasAttr("module"):
			module = unicode(self["module"].convert(converter)).replace(u".", u"/")
		else:
			module = None

		e = self.content
		if converter is not None and converter.target=="html":
			if function is not None:
				if module is not None:
					e = html.a(e, href=(self.base, module, "/index.html#", function))
			elif method is not None:
				if class__ is not None and module is not None:
					e = html.a(e, href=(self.base, module, "/index.html#", class__, "-", method))
			elif prop is not None:
				if class__ is not None and module is not None:
					e = html.a(e, href=(self.base, module, "/index.html#", class__, "-", prop))
			elif class__ is not None:
				if module is not None:
					e = html.a(e, href=(self.base, module, "/index.html#", class__))
			elif module is not None:
				e = html.a(e, href=(self.base, module, "/index.html"))
		return e.convert(converter)

def getDoc(thing):
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

	doc = "\n".join(lines)

	if inspect.ismethod(thing):
		systemId = "METHOD-DOCSTRING(%s.%s.%s)" % (inspect.getmodule(thing).__name__, thing.__class__.__name__, thing.__name__)
	elif inspect.isfunction(thing):
		systemId = "FUNCTION-DOCSTRING(%s.%s)" % (inspect.getmodule(thing).__name__, thing.__name__)
	elif inspect.isclass(thing):
		systemId = "CLASS-DOCSTRING(%s.%s)" % (inspect.getmodule(thing).__name__, thing.__name__)
	elif inspect.ismodule(thing):
		systemId = "MODULE-DOCSTRING(%s)" % inspect.getmodule(thing).__name__
	else:
		systemId = "DOCSTRING"
	node = parsers.parseString(doc, systemId=systemId)
	if not node.find(type=par): # optimization: one paragraph docstrings don't need a <doc:par> element.
		node = par(node)

	refs = node.find(type=pyref, subtype=1, searchchildren=1)
	if inspect.ismethod(thing):
		for ref in refs:
			if not ref.hasAttr("module"):
				ref["module"] = inspect.getmodule(thing).__name__
				if not ref.hasAttr("class"):
					ref["class"] = thing.im_class.__name__
					if not ref.hasAttr("method"):
						ref["method"] = thing.__name__
	elif inspect.isfunction(thing):
		for ref in refs:
			if not ref.hasAttr("module"):
				ref["module"] = inspect.getmodule(thing).__name__
	elif inspect.isclass(thing):
		for ref in refs:
			if not ref.hasAttr("module"):
				ref["module"] = inspect.getmodule(thing).__name__
				if not ref.hasAttr("class"):
					ref["class"] = thing.__name__
	elif inspect.ismodule(thing):
		for ref in refs:
			if not ref.hasAttr("module"):
				ref["module"] = thing.__name__
	return node

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

def cmpName((obj1, name1), (obj2, name2)):
	names = [ name1 or obj1.__name__, name2 or obj2.__name__ ]
	sorts = []
	for name in names:
		try:
			pos = canonicalOrder.index(name)
		except ValueError:
			if name.startswith("__"):
				pos = 3000
			elif name.startswith("_"):
				pos = 2000
			else:
				pos = 1000
		sorts.append((pos, name))
	return cmp(sorts[0], sorts[1])

def __codeHeader(thing, name, type):
	(args, varargs, varkw, defaults) = inspect.getargspec(thing)
	sig = xsc.Frag()
	sig.append(type(name), "(")
	offset = len(args)
	if defaults is not None:
		offset -= len(defaults)
	for i in xrange(len(args)):
		if i == 0:
			if type==method:
				sig.append(arg(self()))
			else:
				sig.append(arg(args[i]))
		else:
			sig.append(", ")
			sig.append(arg(args[i]))
		if i >= offset:
			sig.append("=", repr(defaults[i-offset]))
	if varargs:
		sig.append(", *", arg(varargs))
	if varkw:
		sig.append(", **", arg(varkw))
	sig.append(")")
	return sig

def explain(thing, name=None, context=[]):
	"""
	<doc:par>returns a &xml; representation of the documentation of
	<arg>thing</arg>, which can be a function, method, class or module.</doc:par>

	<doc:par>If <arg>thing</arg> is not a module, you must pass the context
	in <arg>context</arg>, i.e. a list of names of objects into which <arg>thing</arg>
	is nested. This means the first entry will always be module name, and
	the other entries will be class names.</doc:par>
	"""

	if inspect.ismethod(thing):
		name = name or thing.__name__
		context = context + [name]
		(args, varargs, varkw, defaults) = inspect.getargspec(thing.im_func)
		id = "-".join(context)
		sig = xsc.Frag(
			html.a(name=id, id=id)
		)
		if name != thing.__name__ and not (thing.__name__.startswith("__") and name=="_" + thing.im_class.__name__ + thing.__name__):
			sig.append(name, " = ")
		sig.append("def ", __codeHeader(thing.im_func, thing.__name__, method), ":")
		return section(title(sig), getDoc(thing), role="method")
	elif inspect.isfunction(thing):
		name = name or thing.im_func.__name__
		context = context + [name]
		id = "-".join(context)
		sig = xsc.Frag(
			html.a(name=id, id=id),
			"def ",
			__codeHeader(thing, name, function),
			":"
		)
		return section(title(sig), getDoc(thing), role="function")
	elif isinstance(thing, __builtin__.property):
		context = context + [name]
		id = "-".join(context)
		sig = xsc.Frag(
			html.a(name=id, id=id),
			"property ", name, ":"
		)
		node = section(title(sig), getDoc(thing), role="property")
		if thing.fget is not None:
			node.append(explain(thing.fget, "__get__", context))
		if thing.fset is not None:
			node.append(explain(thing.fset, "__set__", context))
		if thing.fdel is not None:
			node.append(explain(thing.fdel, "__delete__", context))
		return node
	elif inspect.isclass(thing):
		name = name or thing.__name__
		context = context + [name]
		id = "-".join(context)
		bases = xsc.Frag()
		if len(thing.__bases__):
			for baseclass in thing.__bases__:
				if baseclass.__module__ == "__builtin__":
					ref = class_(baseclass.__name__)
				else:
					ref = pyref(class_(baseclass.__name__), module=baseclass.__module__, class_=baseclass.__name__)
					if thing.__module__ != baseclass.__module__:
						ref.insert(0, baseclass.__module__, ".")
				bases.append(ref)
			bases = bases.withSep(", ")
			bases.insert(0, "(")
			bases.append(")")
		node = section(
			title(
				html.a(name=id, id=id),
				"class ",
				class_(name),
				bases,
				":"
			),
			getDoc(thing),
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
		for varname in thing.__dict__.keys():
			obj = getattr(thing, varname)
			if inspect.ismethod(obj):
				# skip the method if it's a property getter, setter or deleter
				for (prop, name) in properties:
					if obj.im_func==prop.fget or obj.im_func==prop.fset or obj.im_func==prop.fdel:
						break
				else:
					methods.append((obj, varname))
		if len(methods):
			methods.sort(cmpName)
			node.append([explain(obj, varname, context) for (obj, varname) in methods])
		if len(properties):
			properties.sort(cmpName)
			node.append([explain(obj, varname, context) for (obj, varname) in properties])
		if len(classes):
			classes.sort(cmpName)
			node.append([explain(obj, varname, context) for (obj, varname) in classes])
		return node
	elif inspect.ismodule(thing):
		context = [name or thing.__name__]
		node = section(
			title("Module ", module(name)),
			getDoc(thing)
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
			classes.sort(cmpName)
			node.append(
				section(
					title("Classes"),
					[explain(obj, name, context) for (obj, name) in classes],
					role="classes"
				)
			)
		if len(functions):
			functions.sort(cmpName)
			node.append(
				section(
					title("Functions"),
					[explain(obj, name, context) for (obj, name) in functions],
					role="functions"
				)
			)
		return node

	return xsc.Null

namespace = xsc.Namespace("doc", "http://xmlns.livinglogic.de/xist/ns/doc", vars())
