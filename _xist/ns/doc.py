#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

"""
This namespace module provides classes that can be used for generating
documentation (both &html; and XSL-FO).
"""

# import __builtin__ to use property, which is also defined here
import types, inspect, warnings, __builtin__

from ll.xist import xsc, parsers, sims, errors, xfind
from ll.xist.ns import html, text, docbook, fo, specials, xml


class base(xsc.Element):
	"""
	The base of all element classes. Used for dispatching
	to conversion targets.
	"""
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

			self.vspaceattrs = {
				u"space_before": u"0pt",
				u"space_after_minimum": u"4pt",
				u"space_after_optimum": u"6pt",
				u"space_after_maximum": u"12pt",
				u"space_after_conditionality": u"discard",
			}

			self.linkattrs = {
				u"color": u"blue",
				u"text_decoration": u"underline"
			}

			self.codeattrs = {
				u"font_family": self.ttfont
			}

			self.repattrs = {
				u"font_style": u"italic"
			}

			self.emattrs = {
				u"font_weight": u"bold"
			}

		def dedent(self):
			return u"-0.7cm"

		def indent(self):
			return u"%.1fcm" % (0.7*self.indentcount)

		def labelindent(self):
			return u"%.1fcm" % (0.7*self.indentcount-0.4)

	def convert(self, converter):
		target = converter.target
		if issubclass(target, docbook):
			return self.convert_docbook(converter)
		elif issubclass(target, text):
			return self.convert_text(converter)
		elif issubclass(target, html):
			return self.convert_html(converter)
		elif issubclass(target, __ns__): # our own namespace
			return self.convert_doc(converter)
		elif issubclass(target, fo): # our own namespace
			return self.convert_fo(converter)
		else:
			raise ValueError("unknown conversion target %r" % target)

	def convert_text(self, converter):
		# Forward to the HTML conversion
		return self.convert_html(converter)

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
	register = False


class inline(base):
	"""
	Base class for all inline elements
	"""
	register = False


class abbr(inline):
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
	register = False

	def convert(self, converter):
		e = converter.target.span(u"\xB7\xA0\xA0", class_=u"tab")
		return e.convert(converter)


class litblock(block):
	"""
	A literal text block (like source code or a shell dump)
	"""
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
						c = self.__ns__.tab()
					e.append(c)
			else:
				e.append(child)
		return e.convert(converter)

	def convert_text(self, converter):
		target = converter.target
		e = target.pre(class_=u"prog")
		for child in self.content:
			child = child.convert(converter)
			if isinstance(child, xsc.Text):
				for c in child.content:
					if c==u"\t":
						c = u"   "
					e.append(c)
			else:
				e.append(child)
		e = target.blockquote(e)
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
	cssclass = u"prog"

	def convert_docbook(self, converter):
		e = converter.target.programlisting(self.content)
		return e.convert(converter)


class tty(litblock):
	"""
	A dump of a shell session
	"""
	cssclass = u"tty"

	def convert_docbook(self, converter):
		e = converter.target.screen(self.content)
		return e.convert(converter)


class prompt(inline):
	"""
	The prompt in a <pyref class="tty"><class>tty</class></pyref> dump.
	"""

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

	def convert_docbook(self, converter):
		e = converter.target.prompt(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"input")
		return e.convert(converter)

	def convert_fo(self, converter):
		return xsc.Text(unicode(self.content))


class programlisting(prog):
	def convert(self, converter):
		warnings.warn(DeprecationWarning("programlisting is deprecated, use prog instead"))
		return prog.convert(self, converter)


class rep(inline):
	"""
	Content that may or must be replaced by the user
	"""
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
	register = False

	def convert_fo(self, converter):
		e = converter.target.inline(
			self.content,
			converter[self].codeattrs
		)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=self.xmlname[True])
		return e.convert(converter)


class option(code):
	"""
	An option for a software command
	"""
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
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.markup(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_=u"markup")
		return e.convert(converter)


class arg(code):
	"""
	The name of a function or method argument.
	"""
	model = sims.ElementsOrText(rep)

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
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.filename(self.content, class_=u"directory")
		return e.convert(converter)


class username(code):
	"""
	The name of a user account
	"""
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
		try:
			hclass = target.element(u"h%d" % level)
		except LookupError: # ouch, we're nested to deep (a getter in a property in a class in a class)
			hclass = target.h6
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


class term(base):
	"""
	A term inside a <pyref class="dlist"><class>dlist</class></pyref>
	"""
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


class item(base):
	"""
	A wrapper for the elements of a list item
	"""
	model = sims.ElementsOrText(block, inline) # if it contains no block elements, the content will be promoted to a paragraph

	def convert_docbook(self, converter):
		if xfind.count(self/block):
			content = self.content
		else:
			content = converter.target.para(self.content)
		e = converter.target.listitem(content)
		return e.convert(converter)

	def convert_html(self, converter):
		context = converter[self]
		if not context.lists:
			raise errors.NodeOutsideContextError(self, self.__ns__.list)
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
		if self.content.find(xsc.FindType(block)):
			content = self.content
		else:
			content = self.__ns__.par(self.content)
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
	register = False


class ulist(list):
	"""
	A list in which each entry is marked with a bullet or other dingbat
	"""
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

	def convert_text(self, converter):
		target = converter.target
		e = xsc.Frag()
		for child in self.content:
			if not isinstance(child, title):
				e.append(child)

		return e.convert(converter)

	def convert_fo(self, converter):
		# FIXME: handle title
		e = xsc.Frag()
		for child in self.content:
			if not isinstance(child, title):
				e.append(child)
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


class link(inline):
	"""
	A hypertext link.
	"""
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
		if issubclass(target, __ns__): # our own namespace
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
		if issubclass(target, html):
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


@staticmethod
def _getmodulename(thing):
	module = inspect.getmodule(thing)
	if module is None:
		return "???"
	else:
		return module.__name__


@classmethod
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

	if lines:
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
		while lines and not lines[0]:
			del lines[0]
		while lines and not lines[-1]:
			del lines[-1]

	text = "\n".join(lines)

	if inspect.ismethod(thing):
		sysid = "METHOD-DOCSTRING(%s.%s.%s)" % (cls._getmodulename(thing), thing.im_class.__name__, thing.__name__)
	elif isinstance(thing, __builtin__.property):
		sysid = "PROPERTY-DOCSTRING(%s.%s)" % (cls._getmodulename(thing), "unknown")
	elif inspect.isfunction(thing):
		sysid = "FUNCTION-DOCSTRING(%s.%s)" % (cls._getmodulename(thing), thing.__name__)
	elif inspect.isclass(thing):
		sysid = "CLASS-DOCSTRING(%s.%s)" % (cls._getmodulename(thing), thing.__name__)
	elif inspect.ismodule(thing):
		sysid = "MODULE-DOCSTRING(%s)" % cls._getmodulename(thing)
	else:
		sysid = "DOCSTRING"
	node = parsers.parseString(text, sysid=sysid, prefixes=xsc.DocPrefixes())
	if not list(node/par): # optimization: one paragraph docstrings don't need a <par> element.
		node = cls.par(node)

	if inspect.ismethod(thing):
		for ref in node//pyref:
			if u"module" not in ref.attrs:
				ref[u"module"] = cls._getmodulename(thing)
				if u"class_" not in ref.attrs:
					ref[u"class_"] = thing.im_class.__name__
					if u"method" not in ref.attrs:
						ref[u"method"] = thing.__name__
	elif inspect.isfunction(thing):
		for ref in node//pyref:
			if u"module" not in ref.attrs:
				ref[u"module"] = cls._getmodulename(thing)
	elif inspect.isclass(thing):
		for ref in node//pyref:
			if u"module" not in ref.attrs:
				ref[u"module"] = cls._getmodulename(thing)
				if u"class_" not in ref.attrs:
					ref[u"class_"] = thing.__name__
	elif inspect.ismodule(thing):
		for ref in node//pyref:
			if u"module" not in ref.attrs:
				ref[u"module"] = thing.__name__
	return node


canonicalOrder = [
	"__init__", "__del__",
	"__repr__", "__str__", "__unicode__",
	"__hash__",
	"__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__",
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


@classmethod
def _namekey(cls, (obj, name)):
	name = name or obj.__name__
	try:
		pos = cls.canonicalOrder.index(name)
	except ValueError:
		if name.startswith("__"):
			if name.endswith("__"):
				pos = 1000
			else:
				pos = 4000
		elif name.startswith("_"):
			pos = 3000
		else:
			pos = 2000
	return (pos, name)


@classmethod
def _codeheader(cls, thing, name, type):
	(args, varargs, varkw, defaults) = inspect.getargspec(thing)
	sig = xsc.Frag()
	offset = len(args)
	if defaults is not None:
		offset -= len(defaults)
	for i in xrange(len(args)):
		if i == 0:
			if issubclass(type, method):
				if args[i] == "self":
					sig.append(cls.arg(cls.self()))
				elif args[i] == "cls":
					sig.append(cls.arg(cls.cls()))
				else:
					sig.append(cls.arg(args[i]))
			else:
				sig.append(cls.arg(args[i]))
		else:
			if sig:
				sig.append(u", ")
			sig.append(cls.arg(args[i]))
		if i >= offset:
			sig.append(u"=", cls.lit(repr(defaults[i-offset])))
	if varargs:
		if sig:
			sig.append(u", ")
		sig.append(u"*", cls.arg(varargs))
	if varkw:
		if sig:
			sig.append(u", ")
		sig.append(u"**", cls.arg(varkw))
	sig.insert(0, type(name), u"\u200b(") # use "ZERO WIDTH SPACE" to allow linebreaks
	sig.append(u")")
	return sig


@classmethod
def explain(cls, thing, name=None, context=[]):
	"""
	<par>Return a &xml; representation of the documentation of
	<arg>thing</arg>, which can be a function, method, class or module.</par>

	<par>If <arg>thing</arg> is not a module, you must pass the context
	in <arg>context</arg>, i.e. a list of names of objects into which <arg>thing</arg>
	is nested. This means the first entry will always be module name, and
	the other entries will be class names.</par>
	"""

	visibility = u"public"
	testname = name or thing.__name__
	if testname.startswith("_"):
		visibility = u"protected"
		if testname.startswith("__"):
			visibility = u"private"
			if testname.endswith("__"):
				visibility = u"special"

	doc = cls.getdoc(thing)
	if doc is xsc.Null:
		hasdoc = u"nodoc"
	else:
		hasdoc = u"doc"

	if inspect.ismethod(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		(args, varargs, varkw, defaults) = inspect.getargspec(thing.im_func)
		id = "-".join(info[1] for info in context[1:]) or None
		sig = xsc.Frag()
		if name != thing.__name__ and not (thing.__name__.startswith("__") and name=="_" + thing.im_class.__name__ + thing.__name__):
			sig.append(cls.method(name), u" = ")
		sig.append(u"def ", cls._codeheader(thing.im_func, thing.__name__, cls.method), u":")
		return cls.section(cls.title(sig), doc, role=(visibility, u" method ", hasdoc), id=id or None)
	elif inspect.isfunction(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		id = u"-".join(info[1] for info in context[1:]) or None
		sig = xsc.Frag(
			u"def ",
			cls._codeheader(thing, name, cls.function),
			u":"
		)
		return cls.section(cls.title(sig), doc, role=(visibility, u" function ", hasdoc), id=id)
	elif isinstance(thing, __builtin__.property):
		context = context + [(thing, name)]
		id = u"-".join(info[1] for info in context[1:]) or None
		sig = xsc.Frag(
			u"property ", name, u":"
		)
		node = cls.section(cls.title(sig), doc, role=(visibility, u" property ", hasdoc), id=id)
		if thing.fget is not None:
			node.append(cls.explain(thing.fget, u"__get__", context))
		if thing.fset is not None:
			node.append(cls.explain(thing.fset, u"__set__", context))
		if thing.fdel is not None:
			node.append(cls.explain(thing.fdel, u"__delete__", context))
		return node
	elif inspect.isclass(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		id = "-".join(info[1] for info in context[1:]) or None
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
						baseclassname4text = baseclass.__module__ + u"." + baseclassname
					else:
						baseclassname4text = baseclassname
					#baseclassname4text = u".\u200b".join(baseclassname4text.split("."))
					ref = cls.pyref(cls.class_(baseclassname4text), module=baseclass.__module__, class_=baseclassname)
				bases.append(ref)
			bases = bases.withsep(u", ")
			bases.insert(0, u"\u200b(") # use "ZERO WIDTH SPACE" to allow linebreaks
			bases.append(u")")
		node = cls.section(
			cls.title(
				u"class ",
				cls.class_(name),
				bases,
				u":"
			),
			doc,
			role=(visibility, u" class ", hasdoc),
			id=id
		)
		# find methods, properties and classes, but filter out those methods that are attribute getters, setters or deleters
		methods = []
		properties = []
		classes = []
		for varname in thing.__dict__.keys():
			obj = getattr(thing, varname)
			if isinstance(obj, __builtin__.property):
				properties.append((obj, varname))
			elif inspect.isclass(obj) and not (issubclass(obj, xsc.Namespace) and hasattr(obj, "__file__")):
				classes.append((obj, varname))
			elif inspect.ismethod(obj):
				# skip the method if it's a property getter, setter or deleter
				for (prop, name) in properties:
					if obj.im_func==prop.fget or obj.im_func==prop.fset or obj.im_func==prop.fdel:
						break
				else:
					methods.append((obj, varname))
		if len(methods):
			methods.sort(key=cls._namekey)
			node.append([cls.explain(obj, varname, context) for (obj, varname) in methods])
		if len(properties):
			properties.sort(key=cls._namekey)
			node.append([cls.explain(obj, varname, context) for (obj, varname) in properties])
		if len(classes):
			classes.sort(key=cls._namekey)
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
		node = xsc.Frag(doc)

		functions = []
		classes = []
		for varname in thing.__dict__.keys():
			obj = getattr(thing, varname)
			if inspect.isfunction(obj):
				functions.append((obj, varname))
			elif inspect.isclass(obj) and not (issubclass(obj, xsc.Namespace) and hasattr(obj, "__file__")):
				classes.append((obj, varname))
		if len(classes):
			classes.sort(key=cls._namekey)
			node.append(
				[cls.explain(obj, name, context) for (obj, name) in classes],
			)
		if len(functions):
			functions.sort(key=cls._namekey)
			node.append(
				[cls.explain(obj, name, context) for (obj, name) in functions],
			)
		return node

	return xsc.Null


class fodoc(base):
	model = sims.Elements(block)

	def convert(self, converter):
		context = converter[self]
		e = self.content
		converter.push(target=__ns__)
		e = e.convert(converter)
		converter.pop()
		converter.push(target=fo)
		e = e.convert(converter)
		converter.pop()

		e = xsc.Frag(
			xml.XML10(), u"\n",
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


class __ns__(xsc.Namespace):
	xmlname = "doc"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/doc"
__ns__.makemod(vars())
