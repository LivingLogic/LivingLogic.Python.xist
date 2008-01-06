# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<par>This namespace module provides classes that can be used for generating
documentation (in &html;, DocBook and XSL-FO).</par>
"""


# import __builtin__ to use property, which is also defined here
import sys, types, inspect, textwrap, optparse, collections, warnings, operator, __builtin__

try:
	from docutils import nodes, utils, parsers as restparsers, frontend
	from docutils.parsers.rst import roles
	from docutils.parsers.rst.languages import en
except ImportError:
	pass
else:
	# FIXME: Do the right thing
	roles.register_generic_role("mod", nodes.literal)
	en.roles["mod"] = "mod"

	roles.register_generic_role("class", nodes.literal)
	en.roles["class"] = "class"

	roles.register_generic_role("func", nodes.literal)
	en.roles["func"] = "func"

	roles.register_generic_role("meth", nodes.literal)
	en.roles["meth"] = "meth"

	roles.register_generic_role("var", nodes.literal)
	en.roles["var"] = "var"

	roles.register_generic_role("exc", nodes.literal)
	en.roles["exc"] = "exc"

	roles.register_generic_role("attr", nodes.literal)
	en.roles["attr"] = "attr"

	roles.register_generic_role("prop", nodes.literal)
	en.roles["prop"] = "prop"

	roles.register_generic_role("option", nodes.literal)
	en.roles["option"] = "option"

	roles.register_generic_role("const", nodes.literal)
	en.roles["const"] = "const"

import ll
from ll.xist import xsc, parsers, sims, xfind
from ll.xist.ns import html, docbook, fo, specials, xml, abbr as abbr_


__docformat__ = "xist"


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

	if format.lower() == "plaintext":
		return xsc.Text(text)
	elif format.lower() == "restructuredtext":
		return rest2doc(text)
	elif format.lower() == "xist":
		if inspect.ismethod(thing):
			base = "METHOD-DOCSTRING(%s.%s.%s)" % (_getmodulename(thing), thing.im_class.__name__, thing.__name__)
		elif isinstance(thing, __builtin__.property):
			base = "PROPERTY-DOCSTRING(%s.%s)" % (_getmodulename(thing), "unknown")
		elif inspect.isfunction(thing):
			base = "FUNCTION-DOCSTRING(%s.%s)" % (_getmodulename(thing), thing.__name__)
		elif inspect.isclass(thing):
			base = "CLASS-DOCSTRING(%s.%s)" % (_getmodulename(thing), thing.__name__)
		elif inspect.ismodule(thing):
			base = "MODULE-DOCSTRING(%s)" % _getmodulename(thing)
		else:
			base = "DOCSTRING"
		node = parsers.parsestring(text, base=base, prefixes=xsc.docprefixes())
		if not node[par]: # optimization: one paragraph docstrings don't need a <par> element.
			node = par(node)

		if inspect.ismethod(thing):
			# Use the original method instead of the decorator
			realthing = thing
			while hasattr(realthing, "__wrapped__"):
				realthing = realthing.__wrapped__
			for ref in node.walknode(pyref):
				if u"module" not in ref.attrs:
					ref[u"module"] = _getmodulename(realthing)
					if u"class_" not in ref.attrs:
						ref[u"class_"] = thing.im_class.__name__
						if u"method" not in ref.attrs:
							ref[u"method"] = thing.__name__
		elif inspect.isfunction(thing):
			# Use the original method instead of the decorator
			while hasattr(thing, "__wrapped__"):
				thing = thing.__wrapped__
			for ref in node.walknode(pyref):
				if u"module" not in ref.attrs:
					ref[u"module"] = _getmodulename(thing)
		elif inspect.isclass(thing):
			for ref in node.walknode(pyref):
				if u"module" not in ref.attrs:
					ref[u"module"] = _getmodulename(thing)
					if u"class_" not in ref.attrs:
						ref[u"class_"] = thing.__name__
		elif inspect.ismodule(thing):
			for ref in node.walknode(pyref):
				if u"module" not in ref.attrs:
					ref[u"module"] = thing.__name__
		return node
	else:
		raise ValueError("unsupported __docformat__ %r" % format)


def getsourceline(obj):
	if isinstance(obj, __builtin__.property):
		pos = 999999999
		if obj.fget is not None:
			pos = min(pos, obj.fget.func_code.co_firstlineno)
		if obj.fset is not None:
			pos = min(pos, obj.fset.func_code.co_firstlineno)
		if obj.fdel is not None:
			pos = min(pos, obj.fdel.func_code.co_firstlineno)
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
	(args, varargs, varkw, defaults) = inspect.getargspec(thing)
	sig = xsc.Frag()
	offset = len(args)
	if defaults is not None:
		offset -= len(defaults)
	for i in xrange(len(args)):
		if i == 0:
			if issubclass(type, method):
				if args[i] == "self":
					sig.append(arg(self()))
				elif args[i] == "cls":
					sig.append(arg(cls()))
				else:
					sig.append(arg(args[i]))
			else:
				sig.append(arg(args[i]))
		else:
			if sig:
				sig.append(u", ")
			sig.append(arg(args[i]))
		if i >= offset:
			sig.append(u"=", lit(repr(defaults[i-offset])))
	if varargs:
		if sig:
			sig.append(u", ")
		sig.append(u"*", arg(varargs))
	if varkw:
		if sig:
			sig.append(u", ")
		sig.append(u"**", arg(varkw))
	sig.insert(0, type(name), u"\u200b(") # use "ZERO WIDTH SPACE" to allow linebreaks
	sig.append(u")")
	return sig


def explain(thing, name=None, format=None, context=[]):
	"""
	<par>Return a &xml; representation of the documentation of
	<arg>thing</arg>, which can be a function, method, class or module.</par>

	<par>If <arg>thing</arg> is not a module, you must pass the context
	in <arg>context</arg>, i.e. a list of names of objects into which <arg>thing</arg>
	is nested. This means the first entry will always be the module name, and
	the other entries will be class names.</par>
	"""

	def _append(all, obj, var):
		try:
			all.append((_namekey(obj, varname), obj, varname))
		except (IOError, TypeError):
			pass

	# Determine visibility
	visibility = u"public"
	testname = name or thing.__name__
	if testname.startswith("_"):
		visibility = u"protected"
		if testname.startswith("__"):
			visibility = u"private"
			if testname.endswith("__"):
				visibility = u"special"

	# Determine whether thing has a docstring
	if format is None and inspect.ismodule(thing):
		format = getattr(thing, "__docformat__", "plaintext").split()[0]
	doc = getdoc(thing, format)
	if doc is xsc.Null:
		hasdoc = u"nodoc"
	else:
		hasdoc = u"doc"

	# Determine type
	if inspect.ismethod(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		(args, varargs, varkw, defaults) = inspect.getargspec(thing.im_func)
		id = "-".join(info[1] for info in context[1:]) or None
		sig = xsc.Frag()
		if name != thing.__name__ and not (thing.__name__.startswith("__") and name=="_" + thing.im_class.__name__ + thing.__name__):
			sig.append(method(name), u" = ")
		sig.append(u"def ", _codeheader(thing.im_func, thing.__name__, method), u":")
		return section(title(sig), doc, role=(visibility, u" method ", hasdoc), id=id or None)
	elif inspect.isfunction(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		id = u"-".join(info[1] for info in context[1:]) or None
		sig = xsc.Frag(
			u"def ",
			_codeheader(thing, name, function),
			u":"
		)
		return section(title(sig), doc, role=(visibility, u" function ", hasdoc), id=id)
	elif isinstance(thing, __builtin__.property):
		context = context + [(thing, name)]
		id = u"-".join(info[1] for info in context[1:]) or None
		sig = xsc.Frag(
			u"property ", name, u":"
		)
		node = section(title(sig), doc, role=(visibility, u" property ", hasdoc), id=id)
		if thing.fget is not None:
			node.append(explain(thing.fget, u"__get__", format, context))
		if thing.fset is not None:
			node.append(explain(thing.fset, u"__set__", format, context))
		if thing.fdel is not None:
			node.append(explain(thing.fdel, u"__delete__", format, context))
		return node
	elif inspect.isclass(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		id = "-".join(info[1] for info in context[1:]) or None
		bases = xsc.Frag()
		if len(thing.__bases__):
			for baseclass in thing.__bases__:
				if baseclass.__module__ == "__builtin__":
					ref = class_(baseclass.__name__)
				else:
					try:
						baseclassname = baseclass.__fullname__
					except AttributeError:
						baseclassname = baseclass.__name__
					if thing.__module__ != baseclass.__module__:
						baseclassname4text = baseclass.__module__ + u"." + baseclassname
					else:
						baseclassname4text = baseclassname
					#baseclassname4text = u".\u200b".join(baseclassname4text.split("."))
					ref = pyref(class_(baseclassname4text), module=baseclass.__module__, class_=baseclassname)
				bases.append(ref)
			bases = bases.withsep(u", ")
			bases.insert(0, u"\u200b(") # use "ZERO WIDTH SPACE" to allow linebreaks
			bases.append(u")")
		node = section(
			title(
				u"class ",
				class_(name),
				bases,
				u":"
			),
			doc,
			role=(visibility, u" class ", hasdoc),
			id=id
		)

		# find methods, properties and classes, but filter out those methods that are attribute getters, setters or deleters
		all = []
		properties = []
		classes = []
		for varname in thing.__dict__.keys():
			obj = getattr(thing, varname)
			if isinstance(obj, __builtin__.property):
				properties.append((obj, varname))
				_append(all, obj, varname)
			elif inspect.isclass(obj):
				for (superclass, supername) in context:
					if obj is superclass: # avoid endless recursion for classes that reference a class further up in the context path.
						break
				else:
					classes.append((obj, varname))
					_append(all, obj, varname)
			elif inspect.ismethod(obj):
				# skip the method if it's a property getter, setter or deleter
				for (prop, name) in properties:
					if obj.im_func==prop.fget or obj.im_func==prop.fset or obj.im_func==prop.fdel:
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
	The base of all element classes. Used for dispatching
	to conversion targets.
	"""
	xmlns = xmlns
	register = False

	class Context(xsc.Element.Context):
		def __init__(self):
			xsc.Element.Context.__init__(self)
			self.sections = [0]
			self.lists = []

			self.llblue = u"#006499"
			self.llgreen = u"#9fc94d"

			self.ttfont = u"CourierNew, monospace"
			self.hdfont = u"ArialNarrow, Arial, sans-serif"
			self.font = u"PalatinoLinotype, serif"

			self.indentcount = 0

			self.vspaceattrs = dict(
				space_before=u"0pt",
				space_after_minimum=u"4pt",
				space_after_optimum=u"6pt",
				space_after_maximum=u"12pt",
				space_after_conditionality=u"discard",
			)

			self.linkattrs = dict(
				color=u"blue",
				text_decoration=u"underline",
			)

			self.codeattrs = dict(
				font_family=self.ttfont,
			)

			self.repattrs = dict(
				font_style=u"italic",
			)

			self.emattrs = dict(
				font_weight=u"bold",
			)

		def dedent(self):
			return u"-0.7cm"

		def indent(self):
			return u"%.1fcm" % (0.7*self.indentcount)

		def labelindent(self):
			return u"%.1fcm" % (0.7*self.indentcount-0.4)

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
			raise ValueError("unknown conversion target %r" % target)

	def convert_doc(self, converter):
		e = self.__class__(
			self.content.convert(converter),
			self.attrs.convert(converter)
		)
		return e


class block(base):
	"""
	Base class for all block level elements
	"""
	xmlns = xmlns
	register = False


class inline(base):
	"""
	Base class for all inline elements
	"""
	xmlns = xmlns
	register = False


class abbr(inline):
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(xsc.Element.Attrs):
		class title(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.abbrev(self.content, lang=self[u"lang"])
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.abbr(self.content, self.attrs)
		return e.convert(converter)

	def convert_fo(self, converter):
		return xsc.Text(unicode(self.content))

	def __unicode__(self):
		return unicode(self.content)


class tab(xsc.Element):
	"""
	Used for displaying a tab character in the &html; output.
	"""
	xmlns = xmlns
	register = False

	def convert(self, converter):
		e = converter.target.span(u"\xB7\xA0\xA0", class_=u"tab")
		return e.convert(converter)


class litblock(block):
	"""
	A literal text block (like source code or a shell dump)
	"""
	xmlns = xmlns
	register = False
	model = sims.ElementsOrText(inline)

	cssclass = None

	def convert_html(self, converter):
		target = converter.target
		e = target.pre(class_=self.cssclass)
		for child in self.content:
			child = child.convert(converter)
			if isinstance(child, xsc.Text):
				for c in child.content:
					if c==u"\t":
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
			text_align=u"left",
			line_height=u"130%",
			font_size=u"90%",
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
					if c==u" ":
						c = u"\xa0" # transform spaces into nbsps
					if c==u"\t":
						c = target.inline(u"\u25ab\xa0\xa0\xa0", color="rgb(50%, 50%, 50%)")
					if c==u"\n":
						if not collect and not first: # fix empty lines (but not the first one)
							collect.append(u"\ufeff")
							collect[u"line_height"] = u"60%" # reduce the line-height
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
	A literal listing of all or part of a program
	"""
	xmlns = xmlns
	cssclass = u"prog"

	def convert_docbook(self, converter):
		e = converter.target.programlisting(self.content)
		return e.convert(converter)


class tty(litblock):
	"""
	A dump of a shell session
	"""
	xmlns = xmlns
	cssclass = u"tty"

	def convert_docbook(self, converter):
		e = converter.target.screen(self.content)
		return e.convert(converter)


class prompt(inline):
	"""
	The prompt in a <pyref class="tty"><class>tty</class></pyref> dump.
	"""
	xmlns = xmlns

	def convert_docbook(self, converter):
		e = converter.target.prompt(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"prompt")
		return e.convert(converter)

	def convert_fo(self, converter):
		return xsc.Text(unicode(self.content))


class input(inline):
	"""
	Can be used inside a <pyref class="tty"><class>tty</class></pyref> to mark
	the parts typed by the user.
	"""
	xmlns = xmlns

	def convert_docbook(self, converter):
		e = converter.target.prompt(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"input")
		return e.convert(converter)

	def convert_fo(self, converter):
		return xsc.Text(unicode(self.content))


class programlisting(prog):
	xmlns = xmlns

	def convert(self, converter):
		warnings.warn(DeprecationWarning("programlisting is deprecated, use prog instead"))
		return prog.convert(self, converter)


class rep(inline):
	"""
	Content that may or must be replaced by the user
	"""
	xmlns = xmlns
	model = sims.NoElements()

	def convert_docbook(self, converter):
		e = converter.target.replaceable(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.var(self.content, class_=u"rep")
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
	An option for a software command
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.option(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"option")
		return e.convert(converter)


class lit(code):
	"""
	Inline text that is some literal value
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(code, rep)

	def convert_docbook(self, converter):
		e = converter.target.literal(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"literal")
		return e.convert(converter)


class function(code):
	"""
	The name of a function or subroutine, as in a programming language
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.function(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"function")
		return e.convert(converter)


class method(code):
	"""
	The name of a method or memberfunction in a programming language
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.methodname(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"method")
		return e.convert(converter)


class property(code):
	"""
	The name of a property in a programming language
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.varname(self.content, role=u"property")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"property")
		return e.convert(converter)


class class_(code):
	"""
	The name of a class, in the object-oriented programming sense
	"""
	xmlns = xmlns
	xmlname = "class"
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.classname(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"class")
		return e.convert(converter)


class markup(code):
	"""
	A string of formatting markup in text that is to be represented literally
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.markup(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"markup")
		return e.convert(converter)


class self(code):
	"""
	<par>use this class when referring to the object for which a method has been
	called, e.g.:</par>
	<example>
	<prog>
		this function fooifies the object &lt;self/&gt;.
	</prog>
	</example>
	"""
	xmlns = xmlns
	model = sims.Empty()

	def convert_docbook(self, converter):
		e = converter.target.varname(u"self")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(u"self", class_=u"self")
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.inline(u"self", converter[self].codeattrs)
		return e.convert(converter)

self_ = self


class cls(inline):
	"""
	<par>use this class when referring to the object for which a class method has been
	called, e.g.:</par>
	<example>
	<prog>
		this function fooifies the class &lt;cls/&gt;.
	</prog>
	</example>
	"""
	xmlns = xmlns
	model = sims.Empty()

	def convert_docbook(self, converter):
		e = converter.target.varname(u"cls")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(u"cls", class_=u"cls")
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.inline(u"cls", converter[self].codeattrs)
		return e.convert(converter)


class arg(code):
	"""
	The name of a function or method argument.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep, self, cls)

	def convert_docbook(self, converter):
		e = converter.target.parameter(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"arg")
		return e.convert(converter)


class module(code):
	"""
	The name of a Python module.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.classname(self.content, role=u"module")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"module")
		return e.convert(converter)


class parameter(code):
	"""
	A value or a symbolic reference to a value
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.parameter(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"parameter")
		return e.convert(converter)


class filename(code):
	"""
	The name of a file
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.filename(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"filename")
		return e.convert(converter)


class dirname(code):
	"""
	The name of directory
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.filename(self.content, class_=u"directory")
		return e.convert(converter)


class username(code):
	"""
	The name of a user account
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.literal(self.content, role=u"username")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"username")
		return e.convert(converter)


class hostname(code):
	"""
	The name of a computer
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.literal(self.content, role=u"hostname")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"hostname")
		return e.convert(converter)


class app(inline):
	"""
	The name of a software program
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(rep)
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.URLAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.application(self.content, moreinfo=self[u"moreinfo"])
		return e.convert(converter)

	def convert_html(self, converter):
		if u"moreinfo" in self.attrs:
			e = converter.target.a(self.content, class_=u"app", href=self[u"moreinfo"])
		else:
			e = converter.target.span(self.content, class_=u"app")
		return e.convert(converter)

	def convert_fo(self, converter):
		if u"moreinfo" in self.attrs:
			e = converter.target.basic_link(
				self.content,
				converter[self].linkattrs,
				external_destination=self[u"moreinfo"]
			)
		else:
			e = self.content
		return e.convert(converter)


class title(base):
	"""
	The text of the title of a <pyref class="section"><class>section</class></pyref>
	or an <pyref class="example"><class>example</class></pyref>
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)

	def convert_docbook(self, converter):
		e = converter.target.title(self.content.convert(converter))
		return e.convert(converter)

	def convert_html(self, converter):
		e = self.content
		return e.convert(converter)

	def convert_fo(self, converter):
		e = self.content
		return e.convert(converter)


class section(block):
	"""
	A recursive section
	"""
	xmlns = xmlns
	model = sims.Elements(title, block)
	class Attrs(xsc.Element.Attrs):
		class role(xsc.TextAttr): pass
		class id(xsc.IDAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.section(self.content, role=self[u"role"], id=self[u"id"])
		return e.convert(converter)

	def convert_html(self, converter):
		target = converter.target
		context = converter[self]
		context.sections[-1] += 1
		level = len(context.sections)
		context.sections.append(0) # for numbering the subsections
		ts = xsc.Frag()
		cs = html.div(class_=u"content")
		for child in self:
			if isinstance(child, title):
				ts.append(child)
			else:
				cs.append(child)
		e = target.div(class_=(u"section level", level), id=self[u"id"])
		if u"role" in self.attrs:
			e[u"class_"].append(u" ", self.attrs[u"role"])
		#if u"id" in self.attrs:
		#	e.append(target.a(name=self[u"id"], id=self[u"id"]))
		hclass = getattr(target, u"h%d" % level, target.h6)
		for t in ts:
			h = hclass(t.content)
			e.append(h)
		e.append(cs)
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
			(u"30pt", u"30pt", u"2pt"),
			(u"22pt", u"20pt", u"2pt"),
			(u"16pt", u"15pt", u"2pt"),
			(u"12pt", u"15pt", u"2pt")
		]
		for child in self.content:
			if isinstance(child, title):
				ts.append(child.content)
			else:
				cs.append(child)
		p = props[min(len(context.sections)-1, len(props)-1)]
		isref = unicode(self[u"role"].convert(converter)) in (u"class", u"method", u"property", u"function", u"module")

		number = None
		if isref:
			context.indentcount += 1
			text_indent = context.dedent()
		else:
			if len(context.sections)>1:
				number = (
					u".".join(unicode(s) for s in context.sections[:-1]),
					u". "
				)
			text_indent = None

		tattrs = fo.block.Attrs(
			font_size=p[0],
			color=context.llblue,
			space_before=p[1],
			space_after=p[2],
			text_align=u"left",
			font_family=context.hdfont,
			keep_with_next_within_page=u"always",
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


class par(block):
	"""
	A paragraph
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.para(self.content, role=self[u"type"])
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.p(self.content, class_=self[u"type"])
		return e.convert(converter)

	def convert_fo(self, converter):
		e = fo.block(
			self.content,
			converter[self].vspaceattrs,
			line_height=u"130%"
		)
		return e.convert(converter)


class term(block):
	"""
	A term inside a <pyref class="dlist"><class>dlist</class></pyref>
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
			font_style=u"italic"
		)
		return e.convert(converter)


class item(block):
	"""
	A wrapper for the elements of a list item
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
		context = converter[self]
		if not context.lists:
			raise xsc.NodeOutsideContextError(self, list)
		if context.lists[-1][0] == "dlist":
			e = converter.target.dd(self.content)
		else:
			e = converter.target.li(self.content)
		return e.convert(converter)

	def convert_fo(self, converter):
		target = converter.target
		context = converter[self]
		context.lists[-1][1] += 1
		type = context.lists[-1][0]
		if type=="ulist":
			label = u"\u2022"
		elif type=="olist":
			label = "%d." % context.lists[-1][1]
		context.indentcount += 1
		if self[block]: # Do we have a block in our content?
			content = self.content # yes => use the content as is
		else:
			content = par(self.content) # no => wrap it in a paragraph
		if type=="dlist":
			e = target.block(
				content,
				start_indent=context.indent()
			)
		else:
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


class list(block):
	"""
	Common baseclass for <pyref class="ulist"><class>ulist</class></pyref>,
	<pyref class="olist"><class>olist</class></pyref> and
	<pyref class="dlist"><class>dlist</class></pyref>.
	"""
	xmlns = xmlns
	register = False


class ulist(list):
	"""
	A list in which each entry is marked with a bullet or other dingbat
	"""
	xmlns = xmlns
	model = sims.Elements(item)

	def convert_docbook(self, converter):
		e = converter.target.itemizedlist(self.content.convert(converter))
		return e.convert(converter)

	def convert_html(self, converter):
		context = converter[self]
		context.lists.append(["ulist", 0])
		e = converter.target.ul(self.content.convert(converter))
		del context.lists[-1]
		return e

	def convert_fo(self, converter):
		context = converter[self]
		context.lists.append(["ulist", 0])
		e = converter.target.list_block(self.content, line_height=u"130%")
		e = e.convert(converter)
		del context.lists[-1]
		return e


class olist(list):
	"""
	A list in which each entry is marked with a sequentially incremented label
	"""
	xmlns = xmlns
	model = sims.Elements(item)

	def convert_docbook(self, converter):
		e = converter.target.orderedlist(self.content.convert(converter))
		return e.convert(converter)

	def convert_html(self, converter):
		context = converter[self]
		context.lists.append(["olist", 0])
		e = converter.target.ol(self.content.convert(converter))
		del context.lists[-1]
		return e

	def convert_fo(self, converter):
		context = converter[self]
		context.lists.append(["olist", 0])
		e = converter.target.list_block(self.content, line_height=u"130%")
		e = e.convert(converter)
		del context.lists[-1]
		return e


class dlist(list):
	"""
	A list in which each entry is marked with a label
	"""
	xmlns = xmlns
	model = sims.Elements(term, item)

	def convert_docbook(self, converter):
		e = converter.target.variablelist()
		collect = converter.target.varlistentry()
		for child in self.content:
			collect.append(child)
			if isinstance(child, item):
				e.append(collect)
				collect = converter.target.varlistentry()
		if collect:
			e.append(collect)
		return e.convert(converter)

	def convert_html(self, converter):
		context = converter[self]
		context.lists.append(["dlist", 0])
		e = converter.target.dl(self.content.convert(converter))
		del context.lists[-1]
		return e

	def convert_fo(self, converter):
		context = converter[self]
		context.lists.append(["dlist", 0])
		e = self.content.convert(converter)
		del context.lists[-1]
		return e


class example(block):
	"""
	A formal example
	"""
	xmlns = xmlns
	model = sims.Elements(title, block)

	def convert_docbook(self, converter):
		e = converter.target.example(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		target = converter.target
		ts = xsc.Frag()
		e = xsc.Frag()
		for child in self:
			if isinstance(child, title):
				ts.append(child)
			else:
				e.append(child)
		if ts:
			e.append(target.div(ts, class_=u"example-title"))
		return e.convert(converter)

	def convert_fo(self, converter):
		# FIXME: handle title
		e = xsc.Frag()
		for child in self.content:
			if not isinstance(child, title):
				e.append(child)
		return e.convert(converter)


class link(inline):
	"""
	A hypertext link.
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): pass
		class hreflang(xsc.TextAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.link(self.content, linkend=self[u"href"])
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.a(self.content, href=self[u"href"], hreflang=self[u"hreflang"])
		return e.convert(converter)

	def convert_fo(self, converter):
		if u"href" in self.attrs:
			e = converter.target.basic_link(
				self.content,
				converter[self].linkattrs,
				external_destination=self[u"href"]
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
		e = converter.target.link(self.content, linkend=self[u"ref"])
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.a(self.content, href=(u"#", self[u"ref"]))
		return e.convert(convertert)

	def convert_fo(self, converter):
		if u"href" in self.attrs:
			e = converter.target.basic_link(
				self.content,
				converter[self].linkattrs,
				internal_destination=self[u"ref"]
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
		e = converter.target.a(self.content, href=(u"mailto:", self.content))
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.basic_link(
			self.content,
			converter[self].linkattrs,
			external_destination=(u"mailto:", self.content)
		)
		return e.convert(converter)


class em(inline):
	"""
	Emphasized text
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


class pyref(inline):
	"""
	reference to a Python object:
	module, class, method, property or function
	"""
	xmlns = xmlns
	model = sims.ElementsOrText(inline)
	class Attrs(xsc.Element.Attrs):
		class module(xsc.TextAttr): pass
		class class_(xsc.TextAttr): xmlname = u"class"
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
		if u"function" in self.attrs:
			function = unicode(self[u"function"].convert(converter))
		else:
			function = None
		if u"method" in self.attrs:
			method = unicode(self[u"method"].convert(converter))
		else:
			method = None
		if u"property" in self.attrs:
			prop = unicode(self[u"property"].convert(converter))
		else:
			prop = None
		if u"class_" in self.attrs:
			class__ = unicode(self[u"class_"].convert(converter)).replace(u".", u"-")
		else:
			class__ = None
		if u"module" in self.attrs:
			module = unicode(self[u"module"].convert(converter))
			if module.startswith(u"ll."):
				module = module[3:].replace(u".", u"/")
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
					e = target.a(e, href=(context.base, module, u"/index.html#", function))
			elif method is not None:
				if class__ is not None and module is not None:
					e = target.a(e, href=(context.base, module, u"/index.html#", class__, "-", method))
			elif prop is not None:
				if class__ is not None and module is not None:
					e = target.a(e, href=(context.base, module, u"/index.html#", class__, "-", prop))
			elif class__ is not None:
				if module is not None:
					e = target.a(e, href=(context.base, module, u"/index.html#", class__))
			elif module is not None:
				e = target.a(e, href=(context.base, module, u"/index.html"))
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
			xml.XML(), u"\n",
			fo.root(
				fo.layout_master_set(
					fo.simple_page_master(
						fo.region_body(
							region_name=u"xsl-region-body",
							margin_bottom=u"3cm"
						),
						fo.region_after(
							region_name=u"xsl-region-after",
							extent=u"2cm"
						),
						master_name=u"default",
						page_height=u"29.7cm",
						page_width=u"21cm",
						margin_top=u"1cm",
						margin_bottom=u"1cm",
						margin_left=u"2.5cm",
						margin_right=u"1cm"
					)
				),
				fo.page_sequence(
					fo.static_content(
						fo.block(
							fo.page_number(),
							border_before_width=u"0.1pt",
							border_before_color=u"#000",
							border_before_style=u"solid",
							padding_before=u"4pt",
							text_align=u"center"
						),
						flow_name=u"xsl-region-after"
					),
					fo.flow(
						e,
						flow_name=u"xsl-region-body"
					),
					master_reference=u"default"
				),
				font_family=context.font,
				font_size=u"10pt",
				text_align=u"justify",
				line_height=u"normal",
				language=u"en",
				orphans=2,
				widows=3
			)
		)
		return e


class ReSTConversionWarning(Warning):
	pass


class ReSTConverter(object):
	def __init__(self):
		self.namedrefs = collections.defaultdict()
		self.namedrefs.default_factory = list
		self.unnamedrefs = []

	def convert(self, node):
		if isinstance(node, nodes.document):
			return xsc.Frag(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.Text):
			return xsc.Text(node.astext())
		elif isinstance(node, nodes.problematic):
			# We don't do anything about this
			return xsc.Frag(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.section):
			return section(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.title):
			return title(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.paragraph):
			return par(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.bullet_list):
			return ulist(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.list_item):
			return item(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.definition_list):
			return dlist(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.definition_list_item):
			return xsc.Frag(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.term):
			return term(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.definition):
			return item(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.literal_block):
			return prog(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.literal):
			return lit(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.emphasis):
			return em(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.substitution_reference):
			try:
				return getattr(abbr_, node.attributes["refname"].lower())()
			except AttributeError:
				return xsc.Frag(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.reference):
			e = link(self.convert(child) for child in node.children)
			if "anonymous" in node.attributes:
				self.unnamedrefs.append(e)
			else:
				self.namedrefs[node.attributes["refname"]].append(e)
			return e
		elif isinstance(node, nodes.target):
			uri = node.attributes["refuri"]
			if "anonymous" in node.attributes:
				# Set the link on the first unnamed reference
				self.unnamedrefs[0].attrs.href = uri
				del self.unnamedrefs[0] # done => remove it
			else:
				for name in node.attributes["names"]:
					try:
						es = self.namedrefs[name]
					except KeyError:
						pass
					else:
						for e in es:
							e.attrs.href = uri
						del self.namedrefs[name]
			return xsc.Null
		elif isinstance(node, nodes.system_message):
			warnings.warn(ReSTConversionWarning(str(node)))
			return xsc.Null # ignore system messages
		else:
			raise TypeError("can't handle %r" % node.__class__)


def rest2doc(string):
	parser = restparsers.get_parser_class("rst")()
	defaults = frontend.OptionParser().defaults.copy()
	defaults["tab_width"] = 3
	defaults["pep_references"] = 1
	defaults["rfc_references"] = 1

	doc = utils.new_document("?", optparse.Values(defaults))
	parser.parse(string, doc)

	conv = ReSTConverter()
	return conv.convert(doc)
