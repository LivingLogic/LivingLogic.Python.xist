# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This namespace module provides classes that can be used for generating
documentation (in HTML, DocBook and XSL-FO).
"""


import sys, types, inspect, textwrap, warnings, operator

import ll
from ll.xist import xsc, parse, sims, xfind
from ll.xist.ns import html, docbook, fo, specials, xml


__docformat__ = "reStructuredText"


xmlns = "http://xmlns.livinglogic.de/xist/ns/doc"


def _getmodulename(thing):
	module = inspect.getmodule(thing)
	if module is None:
		return "???"
	else:
		return module.__name__


def getdoc(thing, format):
	if thing.__doc__ is None:
		return xsc.Null

	# Remove indentation
	lines = textwrap.dedent(thing.__doc__).split("\n")

	# remove empty lines
	while lines and not lines[0]:
		del lines[0]
	while lines and not lines[-1]:
		del lines[-1]

	text = "\n".join(lines)

	if inspect.ismethod(thing):
		fmt = "METHOD-DOCSTRING({0}.{1.__class__.__name__}.{1.__qualname__})"
	elif isinstance(thing, property):
		fmt = "PROPERTY-DOCSTRING({0}.{1})"
	elif inspect.isfunction(thing):
		fmt = "FUNCTION-DOCSTRING({0}.{1.__qualname__})"
	elif inspect.isclass(thing):
		fmt = "CLASS-DOCSTRING({0}.{1.__qualname__})"
	elif inspect.ismodule(thing):
		fmt = "MODULE-DOCSTRING({0})"
	else:
		fmt = "DOCSTRING"
	base = fmt.format(_getmodulename(thing), thing)

	lformat = format.lower()
	if lformat == "plaintext":
		return xsc.Text(text)
	elif lformat == "restructuredtext":
		from ll.xist.ns import rest, doc
		return rest.fromstring(text, base=base).conv(target=doc)
	elif lformat == "xist":
		from ll.xist.ns import doc
		node = parse.tree(parse.String(text), parse.SGMLOP(), parse.NS(doc), parse.Node(pool=xsc.docpool(), base=base))
		if not node[p]: # optimization: one paragraph docstrings don't need a <p> element.
			node = p(node)

		if inspect.ismethod(thing):
			# Use the original method instead of the decorator
			realthing = thing
			while hasattr(realthing, "__wrapped__"):
				realthing = realthing.__wrapped__
			for ref in node.walknodes(pyref):
				if "module" not in ref.attrs:
					ref["module"] = _getmodulename(realthing)
					if "class_" not in ref.attrs:
						ref["class_"] = thing.__self__.__class__.__name__
						if "method" not in ref.attrs:
							ref["method"] = thing.__name__
		elif inspect.isfunction(thing):
			# Use the original method instead of the decorator
			while hasattr(thing, "__wrapped__"):
				thing = thing.__wrapped__
			for ref in node.walknodes(pyref):
				if "module" not in ref.attrs:
					ref["module"] = _getmodulename(thing)
		elif inspect.isclass(thing):
			for ref in node.walknodes(pyref):
				if "module" not in ref.attrs:
					ref["module"] = _getmodulename(thing)
					if "class_" not in ref.attrs:
						ref["class_"] = thing.__name__
		elif inspect.ismodule(thing):
			for ref in node.walknodes(pyref):
				if "module" not in ref.attrs:
					ref["module"] = thing.__name__
		return node
	else:
		raise ValueError("unsupported __docformat__ {!r}".format(format))


def getsourceline(obj):
	if isinstance(obj, property):
		pos = 999999999
		if obj.fget is not None:
			pos = min(pos, obj.fget.__code__.co_firstlineno)
		if obj.fset is not None:
			pos = min(pos, obj.fset.__code__.co_firstlineno)
		if obj.fdel is not None:
			pos = min(pos, obj.fdel.__code__.co_firstlineno)
	else:
		while hasattr(obj, "__wrapped__"):
			obj = obj.__wrapped__
		try: # FIXME: Python SF bug #1224621
			pos = inspect.getsourcelines(obj)[-1]
		except IndentationError:
			pos = 42
	return pos


def _namekey(obj, name):
	return (getsourceline(obj), name or obj.__name__)


def _codeheader(thing, name, type):
	# FullArgSpec(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations)
	spec = inspect.getfullargspec(thing)
	# kwonlyargs, kwonlydefaults
	sig = xsc.Frag()
	offset = len(spec.args)
	if spec.defaults is not None:
		offset -= len(spec.defaults)
	for (i, arg) in enumerate(spec.args):
		if i == 0:
			if issubclass(type, meth):
				if arg == "self":
					sig.append(obj(self()))
				elif arg == "cls":
					sig.append(obj(cls()))
				else:
					sig.append(obj(arg))
			else:
				sig.append(obj(arg))
		else:
			if sig:
				sig.append(", ")
			sig.append(obj(arg))
		if i >= offset:
			sig.append("=", lit(repr(spec.defaults[i-offset])))
	if spec.varargs:
		if sig:
			sig.append(", ")
		sig.append("*", obj(spec.varargs))
	if spec.varkw:
		if sig:
			sig.append(", ")
		sig.append("**", obj(spec.varkw))
	for (i, arg) in enumerate(spec.kwonlyargs):
		if sig:
			sig.append(", ")
		sig.append(obj(arg))
		if arg in spec.kwonlydefaults:
			sig.append("=", lit(repr(spec.kwonlydefaults[arg])))
	sig.insert(0, type(name), "\u200b(") # use "ZERO WIDTH SPACE" to allow linebreaks
	sig.append(")")
	return sig


class _stack:
	def __init__(self, context, obj):
		self.context = context
		self.obj = obj

	def __enter__(self):
		self.context.stack.append(self.obj)

	def __exit__(self, type, value, traceback):
		self.context.stack.pop()


def explain(thing, name=None, format=None, context=[]):
	"""
	Return a XML representation of the doc string of :obj:`thing`, which can be
	a function, method, class or module.

	If :obj:`thing` is not a module, you must pass the context in :obj:`context`,
	i.e. a list of names of objects into which :obj:`thing` is nested. This
	means the first entry will always be the module name, and the other entries
	will be class names.
	"""

	def _append(all, obj, varname):
		try:
			all.append((_namekey(obj, varname), obj, varname))
		except (IOError, TypeError):
			pass

	# Determine visibility
	visibility = "public"
	testname = name or thing.__name__
	if testname.startswith("_"):
		visibility = "protected"
		if testname.startswith("__"):
			visibility = "private"
			if testname.endswith("__"):
				visibility = "special"

	# Determine whether ``thing`` has a docstring
	if format is None and inspect.ismodule(thing):
		format = getattr(thing, "__docformat__", "plaintext").split()[0]
	doc = getdoc(thing, format)
	if doc is xsc.Null:
		hasdoc = "nodoc"
	else:
		hasdoc = "doc"

	# Determine type
	if inspect.ismethod(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		(args, varargs, varkw, defaults) = inspect.getargspec(thing.__func__)
		id = "-".join(info[1] for info in context[1:]) or None
		sig = xsc.Frag()
		if name != thing.__name__ and not (thing.__name__.startswith("__") and name=="_" + thing.__self__.__class__.__name__ + thing.__name__):
			sig.append(meth(name), " = ")
		sig.append("def ", _codeheader(thing.__func__, thing.__name__, meth), ":")
		return section(h(sig), doc, role=(visibility, " method ", hasdoc), id=id)
	elif inspect.isfunction(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		id = "-".join(info[1] for info in context[1:]) or None
		sig = xsc.Frag(
			"def ",
			_codeheader(thing, name, func),
			":"
		)
		return section(h(sig), doc, role=(visibility, " function ", hasdoc), id=id)
	elif isinstance(thing, property):
		context = context + [(thing, name)]
		id = "-".join(info[1] for info in context[1:]) or None
		sig = xsc.Frag(
			"property ", name, ":"
		)
		node = section(h(sig), doc, role=(visibility, " property ", hasdoc), id=id)
		if thing.fget is not None:
			node.append(explain(thing.fget, "__get__", format, context))
		if thing.fset is not None:
			node.append(explain(thing.fset, "__set__", format, context))
		if thing.fdel is not None:
			node.append(explain(thing.fdel, "__delete__", format, context))
		return node
	elif inspect.isclass(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		id = "-".join(info[1] for info in context[1:]) or None
		bases = xsc.Frag()
		if len(thing.__bases__):
			for baseclass in thing.__bases__:
				if baseclass.__module__ in ("builtins", "exceptions"):
					ref = class_(baseclass.__name__)
				else:
					try:
						baseclassname = baseclass.__qualname__
					except AttributeError:
						baseclassname = baseclass.__name__
					if thing.__module__ != baseclass.__module__:
						baseclassname4text = baseclass.__module__ + "." + baseclassname
					else:
						baseclassname4text = baseclassname
					#baseclassname4text = u".\u200b".join(baseclassname4text.split("."))
					ref = pyref(class_(baseclassname4text), module=baseclass.__module__, class_=baseclassname)
				bases.append(ref)
			bases = bases.withsep(", ")
			bases.insert(0, "\u200b(") # use "ZERO WIDTH SPACE" to allow linebreaks
			bases.append(")")
		node = section(
			h(
				"class ",
				class_(name),
				bases,
				":"
			),
			doc,
			role=(visibility, " class ", hasdoc),
			id=id
		)

		# find methods, properties and classes, but filter out those methods that are attribute getters, setters or deleters
		all = []
		properties = []
		classes = []
		for varname in thing.__dict__:
			obj = getattr(thing, varname)
			if isinstance(obj, property):
				properties.append((obj, varname))
				_append(all, obj, varname)
			elif inspect.isclass(obj):
				for (superclass, supername) in context:
					if obj is superclass: # avoid endless recursion for classes that reference a class further up in the context path.
						break
				else:
					classes.append((obj, varname))
					_append(all, obj, varname)
			elif inspect.isfunction(obj):
				# skip the method if it's a property getter, setter or deleter
				for (prop, name) in properties:
					if obj==prop.fget or obj==prop.fset or obj==prop.fdel:
						break
				else:
					_append(all, obj, varname)
		if all:
			all.sort()
			for (key, subobj, subname) in all:
				node.append(explain(subobj, subname, format, context))
		return node
	elif inspect.ismodule(thing):
		name = name or thing.__name__
		context = [(thing, name)]
		node = xsc.Frag(doc)

		all = []

		for varname in thing.__dict__:
			obj = getattr(thing, varname)
			if inspect.isfunction(obj) or inspect.isclass(obj):
				_append(all, obj, varname)
		if all:
			all.sort()
			for (key, obj, name) in all:
				node.append(
					explain(obj, name, format, context),
				)
		return node

	return xsc.Null


class base(xsc.Element):
	"""
	The base of all element classes. Used for dispatching to conversion targets.
	"""
	xmlns = xmlns
	register = False

	class Context(xsc.Element.Context):
		def __init__(self):
			xsc.Element.Context.__init__(self)
			self.stack = []
			self.sections = [0]
			self.firstheaderlevel = None

			self.llblue = "#006499"
			self.llgreen = "#9fc94d"

			self.ttfont = "CourierNew, monospace"
			self.hdfont = "ArialNarrow, Arial, sans-serif"
			self.font = "PalatinoLinotype, serif"

			self.indentcount = 0

			self.vspaceattrs = dict(
				space_before="0pt",
				space_after_minimum="4pt",
				space_after_optimum="6pt",
				space_after_maximum="12pt",
				space_after_conditionality="discard",
			)

			self.linkattrs = dict(
				color="blue",
				text_decoration="underline",
			)

			self.codeattrs = dict(
				font_family=self.ttfont,
			)

			self.repattrs = dict(
				font_style="italic",
			)

			self.emattrs = dict(
				font_style="italic",
			)

			self.strongattrs = dict(
				font_weight="bold",
			)

		def dedent(self):
			return "-0.7cm"

		def indent(self):
			return "{:.1f}cm".format(0.7*self.indentcount)

		def labelindent(self):
			return "{:.1f}cm".format(0.7*self.indentcount-0.4)

	def convert(self, converter):
		target = converter.target
		if target.xmlns == docbook.xmlns:
			return self.convert_docbook(converter)
		elif target.xmlns == html.xmlns:
			return self.convert_html(converter)
		elif target.xmlns == xmlns: # our own namespace
			return self.convert_doc(converter)
		elif target.xmlns == fo.xmlns:
			return self.convert_fo(converter)
		else:
			raise ValueError("unknown conversion target {!r}".format(target))

	def convert_doc(self, converter):
		e = self.__class__(
			self.content.convert(converter),
			self.attrs.convert(converter)
		)
		return e


class block(base):
	"""
	Base class for all block level elements.
	"""
	xmlns = xmlns
	register = False

	def convert_html(self, converter):
		e = converter.target.div(self.content)
		return e.convert(converter)


class inline(base):
	"""
	Base class for all inline elements.
	"""
	xmlns = xmlns
	register = False

	def convert_html(self, converter):
		e = converter.target.span(self.content)
		return e.convert(converter)


class abbr(inline):
	"""
	Abbreviation.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(xsc.Element.Attrs):
		class title(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.abbrev(self.content, lang=self.attrs.lang)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.abbr(self.content, self.attrs)
		return e.convert(converter)

	def convert_fo(self, converter):
		return xsc.Text(str(self.content))

	def __str__(self):
		return str(self.content)


class tab(xsc.Element):
	"""
	Used for displaying a tab character in the HTML output.
	"""
	xmlns = xmlns
	register = False

	def convert(self, converter):
		e = converter.target.span("\xB7\xA0\xA0", class_="tab")
		return e.convert(converter)


class litblock(block):
	"""
	A literal text block (like source code or a shell session).
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)

	cssclass = "litblock"

	def convert_html(self, converter):
		target = converter.target
		e = target.pre(class_=self.cssclass)
		for child in self.content:
			child = child.convert(converter)
			if isinstance(child, xsc.Text):
				for c in child.content:
					if c=="\t":
						c = tab()
					e.append(c)
			else:
				e.append(child)
		return e.convert(converter)

	def convert_fo(self, converter):
		target = converter.target
		context = converter[self]
		context.indentcount += 1
		e = target.block(
			context.vspaceattrs,
			context.codeattrs,
			text_align="left",
			line_height="130%",
			font_size="90%",
			start_indent=context.indent(),
			end_indent=context.indent()
		)
		collect = target.block()
		first = True
		for child in self.content:
			child = child.convert(converter)
			if isinstance(child, xsc.Text):
				for c in child.content:
					# We have to do the following, because FOP doesn't support the white-space property yet
					if c==" ":
						c = "\xa0" # transform spaces into nbsps
					if c=="\t":
						c = target.inline("\u25ab\xa0\xa0\xa0", color="rgb(50%, 50%, 50%)")
					if c=="\n":
						if not collect and not first: # fix empty lines (but not the first one)
							collect.append("\ufeff")
							collect["line_height"] = "60%" # reduce the line-height
						e.append(collect)
						collect = target.block()
						first = False
					else:
						collect.append(c)
			else:
				collect.append(child)
		if collect:
			e.append(collect)
		context.indentcount -= 1
		return e.convert(converter)


class prog(litblock):
	"""
	A literal listing of all or part of a program.
	"""
	xmlns = xmlns
	cssclass = "prog"

	def convert_docbook(self, converter):
		e = converter.target.programlisting(self.content)
		return e.convert(converter)


class tty(litblock):
	"""
	A dump of a shell session.
	"""
	xmlns = xmlns
	cssclass = "tty"

	def convert_docbook(self, converter):
		e = converter.target.screen(self.content)
		return e.convert(converter)


class prompt(inline):
	"""
	The prompt in a :class:`tty` dump.
	"""
	xmlns = xmlns

	def convert_docbook(self, converter):
		e = converter.target.prompt(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_="prompt")
		return e.convert(converter)

	def convert_fo(self, converter):
		return xsc.Text(str(self.content))


class input(inline):
	"""
	Can be used inside a :class:`tty` to mark the parts typed by the user.
	"""
	xmlns = xmlns

	def convert_docbook(self, converter):
		e = converter.target.prompt(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_="input")
		return e.convert(converter)

	def convert_fo(self, converter):
		return xsc.Text(str(self.content))


class rep(inline):
	"""
	Content that may or must be replaced by the user.
	"""
	xmlns = xmlns
	model = sims.NoElements()

	def convert_docbook(self, converter):
		e = converter.target.replaceable(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.var(self.content, class_="rep")
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.inline(self.content, converter[self].repattrs)
		return e.convert(converter)


class code(inline):
	xmlns = xmlns
	register = False

	def convert_fo(self, converter):
		e = converter.target.inline(
			self.content,
			converter[self].codeattrs
		)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=self.xmlname)
		return e.convert(converter)


class option(code):
	"""
	An option for a software command.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.option(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_="option")
		return e.convert(converter)


class lit(code):
	"""
	Inline text that is some literal value.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(code, rep)

	def convert_docbook(self, converter):
		e = converter.target.literal(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_="lit")
		return e.convert(converter)


class func(code):
	"""
	The name of a function or subroutine, as in a programming language.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.function(self.content)
		return e.convert(converter)


class meth(code):
	"""
	The name of a method or memberfunction in a programming language.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.methodname(self.content)
		return e.convert(converter)


class attr(code):
	"""
	The name of an attribute of a class/object.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.methodname(self.content)
		return e.convert(converter)


class prop(code):
	"""
	The name of a property in a programming language.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.varname(self.content, role="property")
		return e.convert(converter)


class class_(code):
	"""
	The name of a class, in the object-oriented programming sense.
	"""
	xmlns = xmlns
	xmlname = "class"
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.classname(self.content)
		return e.convert(converter)


class exc(code):
	"""
	The name of an exception class.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.classname(self.content)
		return e.convert(converter)


class markup(code):
	"""
	A string of formatting markup in text that is to be represented literally.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.markup(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_="markup")
		return e.convert(converter)


class self(code):
	"""
	Use this class when referring to the object for which a method has been
	called, e.g.::

		this function fooifies the object <self/>;.
	"""
	xmlns = xmlns
	model = sims.Empty()

	def convert_docbook(self, converter):
		e = converter.target.varname("self")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code("self", class_="self")
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.inline("self", converter[self].codeattrs)
		return e.convert(converter)

self_ = self


class cls(inline):
	"""
	Use this class when referring to the object for which a class method has
	been called, e.g.::

		this function fooifies the class <cls/>.
	"""
	xmlns = xmlns
	model = sims.Empty()

	def convert_docbook(self, converter):
		e = converter.target.varname("cls")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code("cls", class_="cls")
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.inline("cls", converter[self].codeattrs)
		return e.convert(converter)


class obj(code):
	"""
	A object of unspecified type.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep, self, cls)

	def convert_docbook(self, converter):
		e = converter.target.varname(self.content)
		return e.convert(converter)


class mod(code):
	"""
	The name of a Python module.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.classname(self.content, role="module")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_="module")
		return e.convert(converter)


class file(code):
	"""
	The name of a file.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.filename(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_="filename")
		return e.convert(converter)


class dir(code):
	"""
	The name of a directory.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.filename(self.content, class_="directory")
		return e.convert(converter)


class user(code):
	"""
	The name of a user account.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.literal(self.content, role="username")
		return e.convert(converter)


class host(code):
	"""
	The name of a computer.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.literal(self.content, role="hostname")
		return e.convert(converter)


class const(code):
	"""
	The name of a constant.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.literal(self.content, role="constant")
		return e.convert(converter)


class data(code):
	"""
	The name of a data object.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.literal(self.content, role="data")
		return e.convert(converter)


class app(inline):
	"""
	The name of a software program.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.URLAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.application(self.content, moreinfo=self.attrs.moreinfo)
		return e.convert(converter)

	def convert_html(self, converter):
		if "moreinfo" in self.attrs:
			e = converter.target.a(self.content, class_="app", href=self.attrs.moreinfo)
		else:
			e = converter.target.span(self.content, class_="app")
		return e.convert(converter)

	def convert_fo(self, converter):
		if "moreinfo" in self.attrs:
			e = converter.target.basic_link(
				self.content,
				converter[self].linkattrs,
				external_destination=self.attrs.moreinfo
			)
		else:
			e = self.content
		return e.convert(converter)


class h(base):
	"""
	The text of the title of a :class:`section` or an :class:`example`.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)

	def convert_docbook(self, converter):
		e = converter.target.title(self.content.convert(converter))
		return e.convert(converter)

	def convert_html(self, converter):
		context = converter[self]
		if context.stack:
			if isinstance(context.stack[-1], example):
				e = self.content
			elif isinstance(context.stack[-1], section):
				level = len(context.sections)
				if context.firstheaderlevel is None:
					context.firstheaderlevel = level
				e = getattr(converter.target, "h{}".format(context.firstheaderlevel+level), converter.target.h6)(self.content)
			else:
				raise ValueError("unknown node {!r} on the stack".format(context.stack[-1]))
		else:
			context.firstheaderlevel = 0
			e = converter.target.h1(self.content)
		return e.convert(converter)

	def convert_fo(self, converter):
		e = self.content
		return e.convert(converter)


class section(block):
	"""
	A recursive section.
	"""
	xmlns = xmlns
	model = sims.Elements(h, block)
	class Attrs(xsc.Element.Attrs):
		class role(xsc.TextAttr): pass
		class id(xsc.IDAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.section(self.content, role=self.attrs.role, id=self.attrs.id)
		return e.convert(converter)

	def convert_html(self, converter):
		target = converter.target
		context = converter[self]
		context.sections[-1] += 1
		level = len(context.sections)
		context.sections.append(0) # for numbering the subsections
		ts = xsc.Frag()
		cs = html.div(class_="content")
		for child in self:
			if isinstance(child, h):
				ts.append(child)
			else:
				cs.append(child)
		e = target.div(class_=("section level", level), id=self.attrs.id)
		if "role" in self.attrs:
			e.attrs.class_.append(" ", self.attrs.role)
		#if "id" in self.attrs:
		#	e.append(target.a(name=self.attrs.id, id=self.attrs.id))
		hclass = getattr(target, "h{}".format(level), target.h6)
		for t in ts:
			e.append(hclass(t.content))
		e.append(cs)
		with _stack(context, self):
			# make sure to call the inner convert() before popping the number off of the stack
			e = e.convert(converter)
			del context.sections[-1]
			return e

	def convert_fo(self, converter):
		context = converter[self]
		context.sections[-1] += 1
		context.sections.append(0)
		ts = xsc.Frag()
		cs = xsc.Frag()
		props = [
			# size,    before,  after
			("30pt", "30pt", "2pt"),
			("22pt", "20pt", "2pt"),
			("16pt", "15pt", "2pt"),
			("12pt", "15pt", "2pt")
		]
		for child in self.content:
			if isinstance(child, h):
				ts.append(child.content)
			else:
				cs.append(child)
		p = props[min(len(context.sections)-1, len(props)-1)]
		isref = str(self.attrs.role.convert(converter)) in ("class", "method", "property", "function", "module")

		number = None
		if isref:
			context.indentcount += 1
			text_indent = context.dedent()
		else:
			if len(context.sections)>1:
				number = (
					".".join(str(s) for s in context.sections[:-1]),
					". "
				)
			text_indent = None

		tattrs = fo.block.Attrs(
			font_size=p[0],
			color=context.llblue,
			space_before=p[1],
			space_after=p[2],
			text_align="left",
			font_family=context.hdfont,
			keep_with_next_within_page="always",
			text_indent=text_indent
		)
		e = fo.block(
			fo.block(number, ts, tattrs),
			cs,
			start_indent=context.indent()
		)
		e = e.convert(converter)
		del context.sections[-1]
		if isref:
			context.indentcount -= 1
		return e


class p(block):
	"""
	A paragraph.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.para(self.content, role=self.attrs.type)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.p(self.content, class_=self.attrs.type)
		return e.convert(converter)

	def convert_fo(self, converter):
		e = fo.block(
			self.content,
			converter[self].vspaceattrs,
			line_height="130%"
		)
		return e.convert(converter)


class dt(block):
	"""
	A term inside a :class:`dl`.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)

	def convert_docbook(self, converter):
		e = converter.target.term(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.dt(self.content)
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.block(
			self.content,
			font_style="italic"
		)
		return e.convert(converter)


class li(block):
	"""
	A wrapper for the elements of a list item in :class:`ul` or :class:`ol`.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(block, inline) # if it contains no block elements, the content will be promoted to a paragraph

	def convert_docbook(self, converter):
		if self[block]:
			content = self.content
		else:
			content = converter.target.para(self.content)
		e = converter.target.listitem(content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.li(self.content)
		return e.convert(converter)

	def convert_fo(self, converter):
		target = converter.target
		context = converter[self]
		context.lists[-1][1] += 1
		type = context.lists[-1][0]
		if type=="ul":
			label = "\u2022"
		elif type=="ol":
			label = "{}.".format(context.lists[-1][1])
		context.indentcount += 1
		if self[block]: # Do we have a block in our content?
			content = self.content # yes => use the content as is
		else:
			content = p(self.content) # no => wrap it in a paragraph
		e = target.list_item(
			target.list_item_label(
				target.block(label),
				start_indent=context.labelindent()
			),
			target.list_item_body(
				content,
				start_indent=context.indent()
			)
		)
		context.indentcount -= 1
		return e.convert(converter)


class dd(block):
	"""
	A wrapper for the elements of a list item :class:`dl`.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(block, inline) # if it contains no block elements, the content will be promoted to a paragraph

	def convert_docbook(self, converter):
		if self[block]:
			content = self.content
		else:
			content = converter.target.para(self.content)
		e = converter.target.listitem(content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.dd(self.content)
		return e.convert(converter)

	def convert_fo(self, converter):
		target = converter.target
		context = converter[self]
		context.lists[-1][1] += 1
		type = context.lists[-1][0]
		context.indentcount += 1
		if self[block]: # Do we have a block in our content?
			content = self.content # yes => use the content as is
		else:
			content = p(self.content) # no => wrap it in a paragraph
		e = target.block(
			content,
			start_indent=context.indent()
		)
		context.indentcount -= 1
		return e.convert(converter)


class list(block):
	"""
	Common baseclass for :class:`ul`, :class:`ol` and :class:`dl`.
	"""
	xmlns = xmlns
	register = False


class ul(list):
	"""
	A list in which each entry is marked with a bullet or other dingbat.
	"""
	xmlns = xmlns
	model = sims.Elements(li)

	def convert_docbook(self, converter):
		e = converter.target.itemizedlist(self.content.convert(converter))
		return e.convert(converter)

	def convert_html(self, converter):
		with _stack(converter[self], self):
			return converter.target.ul(self.content.convert(converter))

	def convert_fo(self, converter):
		context = converter[self]
		context.lists.append(["ul", 0])
		e = converter.target.list_block(self.content, line_height="130%")
		e = e.convert(converter)
		del context.lists[-1]
		return e


class ol(list):
	"""
	A list in which each entry is marked with a sequentially incremented label.
	"""
	xmlns = xmlns
	model = sims.Elements(li)

	def convert_docbook(self, converter):
		e = converter.target.orderedlist(self.content.convert(converter))
		return e.convert(converter)

	def convert_html(self, converter):
		with _stack(converter[self], self):
			return converter.target.ol(self.content.convert(converter))

	def convert_fo(self, converter):
		context = converter[self]
		context.lists.append(["ol", 0])
		e = converter.target.list_block(self.content, line_height="130%")
		e = e.convert(converter)
		del context.lists[-1]
		return e


class dl(list):
	"""
	A list in which each entry is marked with a label.
	"""
	xmlns = xmlns
	model = sims.Elements(dt, dd)

	def convert_docbook(self, converter):
		e = converter.target.variablelist()
		collect = converter.target.varlistentry()
		for child in self.content:
			collect.append(child)
			if isinstance(child, dd):
				e.append(collect)
				collect = converter.target.varlistentry()
		if collect:
			e.append(collect)
		return e.convert(converter)

	def convert_html(self, converter):
		with _stack(converter[self], self):
			return converter.target.dl(self.content.convert(converter))

	def convert_fo(self, converter):
		context = converter[self]
		context.lists.append(["dl", 0])
		e = self.content.convert(converter)
		del context.lists[-1]
		return e


class example(block):
	"""
	A formal example.
	"""
	xmlns = xmlns
	model = sims.Elements(h, block)

	def convert_docbook(self, converter):
		e = converter.target.example(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		target = converter.target
		ts = xsc.Frag()
		e = xsc.Frag()
		for child in self:
			if isinstance(child, h):
				ts.append(child)
			else:
				e.append(child)
		if ts:
			e.append(target.div(ts, class_="example-title"))
		with _stack(converter[self], self):
			return e.convert(converter)

	def convert_fo(self, converter):
		# FIXME: handle title
		e = xsc.Frag()
		for child in self.content:
			if not isinstance(child, h):
				e.append(child)
		return e.convert(converter)


class a(inline):
	"""
	A hypertext link.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): pass
		class hreflang(xsc.TextAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.link(self.content, linkend=self.attrs.href)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.a(self.content, href=self.attrs.href, hreflang=self.attrs.hreflang)
		return e.convert(converter)

	def convert_fo(self, converter):
		if "href" in self.attrs:
			e = converter.target.basic_link(
				self.content,
				converter[self].linkattrs,
				external_destination=self.attrs.href
			)
		else:
			e = self.content
		return e.convert(converter)


class xref(inline):
	"""
	An internal cross reference.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)
	class Attrs(xsc.Element.Attrs):
		class ref(xsc.TextAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.link(self.content, linkend=self.attrs.ref)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.a(self.content, href=("#", self.attrs.ref))
		return e.convert(convertert)

	def convert_fo(self, converter):
		if "href" in self.attrs:
			e = converter.target.basic_link(
				self.content,
				converter[self].linkattrs,
				internal_destination=self.attrs.ref
			)
		else:
			e = self.content
		return e.convert(converter)


class email(inline):
	"""
	An email address.
	"""
	xmlns = xmlns
	model = sims.NoElements()

	def convert_docbook(self, converter):
		e = converter.target.email(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.a(self.content, href=("mailto:", self.content))
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.basic_link(
			self.content,
			converter[self].linkattrs,
			external_destination=("mailto:", self.content)
		)
		return e.convert(converter)


class em(inline):
	"""
	Emphasized text.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)

	def convert_docbook(self, converter):
		e = converter.target.emphasis(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.em(self.content)
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.inline(
			self.content,
			converter[self].emattrs
		)
		return e.convert(converter)


class strong(inline):
	"""
	Emphasized text.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)

	def convert_docbook(self, converter):
		e = converter.target.emphasis(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.strong(self.content)
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.inline(
			self.content,
			converter[self].strongattrs
		)
		return e.convert(converter)


class z(inline):
	"""
	Put the content into double quotes.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)

	def convert(self, converter):
		e = xsc.Frag("\u201c", self.content, "\u201d")
		return e.convert(converter)


class pyref(inline):
	"""
	Reference to a Python object: module, class, method, property or function.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)
	class Attrs(xsc.Element.Attrs):
		class module(xsc.TextAttr): pass
		class class_(xsc.TextAttr): xmlname = "class"
		class method(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class function(xsc.TextAttr): pass

	class Context(xsc.Element.Context):
		def __init__(self):
			xsc.Element.Context.__init__(self)
			self.base = "http://127.0.0.1:7464/"

	def convert(self, converter):
		target = converter.target
		context = converter[self]
		if target.xmlns == xmlns: # our own namespace
			return self.convert_doc(converter)
		if "function" in self.attrs:
			function = str(self.attrs.function.convert(converter))
		else:
			function = None
		if "method" in self.attrs:
			method = str(self.attrs.method.convert(converter))
		else:
			method = None
		if "property" in self.attrs:
			prop = str(self.attrs.property.convert(converter))
		else:
			prop = None
		if "class" in self.attrs:
			class_ = str(self.attrs.class_.convert(converter)).replace(".", "-")
		else:
			class_ = None
		if "module" in self.attrs:
			module = str(self.attrs.module.convert(converter))
			if module.startswith("ll."):
				module = module[3:].replace(".", "/")
			elif module == "ll":
				module = "core"
			else:
				module = None
		else:
			module = None

		e = self.content
		if target.xmlns == html.xmlns:
			if function is not None:
				if module is not None:
					e = target.a(e, href=(context.base, module, "/index.html#", function))
			elif method is not None:
				if class_ is not None and module is not None:
					e = target.a(e, href=(context.base, module, "/index.html#", class_, "-", method))
			elif prop is not None:
				if class_ is not None and module is not None:
					e = target.a(e, href=(context.base, module, "/index.html#", class_, "-", prop))
			elif class_ is not None:
				if module is not None:
					e = target.a(e, href=(context.base, module, "/index.html#", class_))
			elif module is not None:
				e = target.a(e, href=(context.base, module, "/index.html"))
		return e.convert(converter)


class fodoc(base):
	xmlns = xmlns
	model = sims.Elements(block)

	def convert(self, converter):
		context = converter[self]
		e = self.content
		converter.push(target=sys.modules[__name__]) # our own module
		e = e.convert(converter)
		converter.pop()
		converter.push(target=fo)
		e = e.convert(converter)
		converter.pop()

		e = xsc.Frag(
			xml.XML(), "\n",
			fo.root(
				fo.layout_master_set(
					fo.simple_page_master(
						fo.region_body(
							region_name="xsl-region-body",
							margin_bottom="3cm"
						),
						fo.region_after(
							region_name="xsl-region-after",
							extent="2cm"
						),
						master_name="default",
						page_height="29.7cm",
						page_width="21cm",
						margin_top="1cm",
						margin_bottom="1cm",
						margin_left="2.5cm",
						margin_right="1cm"
					)
				),
				fo.page_sequence(
					fo.static_content(
						fo.block(
							fo.page_number(),
							border_before_width="0.1pt",
							border_before_color="#000",
							border_before_style="solid",
							padding_before="4pt",
							text_align="center"
						),
						flow_name="xsl-region-after"
					),
					fo.flow(
						e,
						flow_name="xsl-region-body"
					),
					master_reference="default"
				),
				font_family=context.font,
				font_size="10pt",
				text_align="justify",
				line_height="normal",
				language="en",
				orphans=2,
				widows=3
			)
		)
		return e
