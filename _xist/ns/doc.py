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

# import __builtin__ to use property, which is also defined here
import types, inspect, warnings, __builtin__

from ll.xist import xsc, parsers, converters, sims
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

			self.llblue = "#006499"
			self.llgreen = "#9fc94d"

			self.ttfont = "CourierNew, monospace"
			self.hdfont = "ArialNarrow, Arial, sans-serif"
			self.font = "PalatinoLinotype, serif"

			self.indentcount = 0

			self.vspaceattrs = {
				"space_before": "0pt",
				"space_after_minimum": "4pt",
				"space_after_optimum": "6pt",
				"space_after_maximum": "12pt",
				"space_after_conditionality": "discard",
			}

			self.linkattrs = {
				"color": "blue",
				"text_decoration": "underline"
			}

			self.codeattrs = {
				"font_family": self.ttfont
			}

			self.repattrs = {
				"font_style": "italic"
			}

			self.emattrs = {
				"font_weight": "bold"
			}

		def dedent(self):
			return "-0.7cm"

		def indent(self):
			return "%.1fcm" % (0.7*self.indentcount)

		def labelindent(self):
			return "%.1fcm" % (0.7*self.indentcount-0.4)

	def convert(self, converter):
		target = converter.target
		if issubclass(target, docbook):
			return self.convert_docbook(converter)
		elif issubclass(target, text):
			return self.convert_text(converter)
		elif issubclass(target, html):
			return self.convert_html(converter)
		elif issubclass(target, xmlns): # our own namespace
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
		e = converter.target.abbrev(self.content, lang=self["lang"])
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.abbr(self.content, self.attrs)
		return e.convert(converter)

	def convert_fo(self, converter):
		return xsc.Text(unicode(self.content))

	def __unicode__(self):
		return unicode(self.content)


class prog(block):
	"""
	A literal listing of all or part of a program
	"""
	model = sims.ElementsOrText(inline)

	def convert_docbook(self, converter):
		e = converter.target.programlisting(self.content)
		return e.convert(converter)

	def convert_html(self, converter):
		target = converter.target
		e = target.pre(class_="prog")
		for child in self.content:
			child = child.convert(converter)
			if isinstance(child, xsc.Text):
				for c in child.content:
					if c==u"\t":
						c = target.span(u"···", class_="tab")
					e.append(c)
			else:
				e.append(child)
		return e.convert(converter)

	def convert_text(self, converter):
		target = converter.target
		e = target.pre(class_="prog")
		for child in self.content:
			child = child.convert(converter)
			if isinstance(child, xsc.Text):
				for c in child.content:
					if c==u"\t":
						c = "   "
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
					if c==u" ":
						c = u"\xa0" # transform spaces into nbsps
					if c==u"\t":
						c = target.inline(u"\u25ab", 3*u"\xa0", color="rgb(50%, 50%, 50%)")
					if c==u"\n":
						if not collect and not first: # fix empty lines (but not the first one)
							collect.append(u"\ufeff")
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
		e = converter.target.var(self.content, class_="rep")
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
		e = converter.target.code(self.content, class_="option")
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
		e = converter.target.code(self.content, class_="literal")
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
		e = converter.target.code(self.content, class_="function")
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
		e = converter.target.code(self.content, class_="method")
		return e.convert(converter)


class property(code):
	"""
	The name of a property in a programming language
	"""
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.varname(self.content, role="property")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_="property")
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
		e = converter.target.code(self.content, class_="class")
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
		e = converter.target.code(self.content, class_="markup")
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
		e = converter.target.code(self.content, class_="arg")
		return e.convert(converter)


class module(code):
	"""
	The name of a Python module.
	"""
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.classname(self.content, role="module")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_="module")
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
		e = converter.target.code(self.content, class_="parameter")
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
		e = converter.target.code(self.content, class_="filename")
		return e.convert(converter)


class dirname(code):
	"""
	The name of directory
	"""
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.filename(self.content, class_="directory")
		return e.convert(converter)


class username(code):
	"""
	The name of a user account
	"""
	model = sims.ElementsOrText(rep)

	def convert_docbook(self, converter):
		e = converter.target.literal(self.content, role="username")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code(self.content, class_="username")
		return e.convert(converter)


class app(inline):
	"""
	The name of a software program
	"""
	model = sims.ElementsOrText(rep)
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.URLAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.application(self.content, moreinfo=self["moreinfo"])
		return e.convert(converter)

	def convert_html(self, converter):
		if "moreinfo" in self.attrs:
			e = converter.target.a(self.content, class_="app", href=self["moreinfo"])
		else:
			e = converter.target.span(self.content, class_="app")
		return e.convert(converter)

	def convert_fo(self, converter):
		if "moreinfo" in self.attrs:
			e = converter.target.basic_link(
				self.content,
				converter[self].linkattrs,
				external_destination=self["moreinfo"]
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
		e = converter.target.section(self.content, role=self["role"], id=self["id"])
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
			if isinstance(child, title):
				ts.append(child)
			else:
				cs.append(child)
		e = target.div(class_=("section level", level), id=self["id"])
		if "role" in self.attrs:
			e["class_"].append(" ", self.attrs["role"])
		#if "id" in self.attrs:
		#	e.append(target.a(name=self["id"], id=self["id"]))
		try:
			hclass = target.element("h%d" % level)
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
			# size,   before, after
			("30pt", "30pt", "2pt"),
			("22pt", "20pt", "2pt"),
			("16pt", "15pt", "2pt"),
			("12pt", "15pt", "2pt")
		]
		for child in self.content:
			if isinstance(child, title):
				ts.append(child.content)
			else:
				cs.append(child)
		p = props[min(len(context.sections)-1, len(props)-1)]
		isref = unicode(self["role"].convert(converter)) in ("class", "method", "property", "function", "module")

		number = None
		if isref:
			context.indentcount += 1
			text_indent = context.dedent()
		else:
			if len(context.sections)>2:
				number = (
					".".join([str(x) for x in context.sections[1:-1]]),
					". "
				)
			text_indent = None

		if len(context.sections)==2:
			if context.sections[0]==1:
				break_before = None
			else:
				break_before = "page"
			tattrs = fo.block.Attrs(
				font_family=context.hdfont,
				color=context.llblue,
				text_align="center",
				font_size="36pt",
				space_after="30pt",
				break_before=break_before,
				keep_with_next_within_page="always",
			)
		else:
			tattrs = fo.block.Attrs(
				font_size=p[0],
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


class par(block):
	"""
	A paragraph
	"""
	model = sims.ElementsOrText(inline)
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.para(self.content, role=self["type"])
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.p(self.content, class_=self["type"])
		return e.convert(converter)

	def convert_fo(self, converter):
		e = fo.block(
			self.content,
			converter[self].vspaceattrs,
			line_height="130%"
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
			font_style="italic"
		)
		return e.convert(converter)


class item(base):
	"""
	A wrapper for the elements of a list item
	"""
	model = sims.ElementsOrText(block, inline) # if it contains no block elements, the content will be promoted to a paragraph

	def convert_docbook(self, converter):
		if self.content.find(xsc.FindType(block)):
			content = self.content
		else:
			content = converter.target.para(self.content)
		e = converter.target.listitem(content)
		return e.convert(converter)

	def convert_html(self, converter):
		context = converter[self]
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
			content = self.xmlns.par(self.content)
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
		e = converter.target.list_block(self.content, line_height="130%")
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
		e = converter.target.list_block(self.content, line_height="130%")
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
			e.append(target.div(ts, class_="example-title"))

		return e.convert(converter)

	def convert_text(self, converter):
		target = converter.target
		e = xsc.Frag()
		for child in self.content:
			if not isinstance(child, title):
				e.append(child)

		return e.convert(converter)

	def convert_fo(self, converter):
		# FIXME handle title
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
		e = converter.target.varname("self")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code("self", class_="self")
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.inline("self", converter[self].codeattrs)
		return e.convert(converter)

	def __unicode__(self):
		return u"self"

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
		e = converter.target.varname("cls")
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.code("cls", class_="cls")
		return e.convert(converter)

	def convert_fo(self, converter):
		e = converter.target.inline("cls", converter[self].codeattrs)
		return e.convert(converter)

	def __unicode__(self):
		return u"cls"


class link(inline):
	"""
	A hypertext link.
	"""
	model = sims.ElementsOrText(inline)
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): pass
		class hreflang(xsc.TextAttr): pass

	def convert_docbook(self, converter):
		e = converter.target.link(self.content, linkend=self["href"])
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.a(self.content, href=self["href"], hreflang=self["href"])
		return e.convert(converter)

	def convert_fo(self, converter):
		if "href" in self.attrs:
			e = converter.target.basic_link(
				self.content,
				converter[self].linkattrs,
				external_destination=self["href"]
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
		e = converter.target.link(self.content, linkend=self["ref"])
		return e.convert(converter)

	def convert_html(self, converter):
		e = converter.target.a(self.content, href=("#", self["ref"]))
		return e.convert(convertert)

	def convert_fo(self, converter):
		if "href" in self.attrs:
			e = converter.target.basic_link(
				self.content,
				converter[self].linkattrs,
				internal_destination=self["ref"]
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
		class class_(xsc.TextAttr): xmlname = "class"
		class method(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class function(xsc.TextAttr): pass

	class Context(xsc.Element.Context):
		def __init__(self):
			xsc.Element.Context.__init__(self)
			self.base = "http://localhost:7464/"

	def convert(self, converter):
		target = converter.target
		context = converter[self]
		if issubclass(target, xmlns): # our own namespace
			return self.convert_doc(converter)
		if "function" in self.attrs:
			function = unicode(self["function"].convert(converter))
		else:
			function = None
		if "method" in self.attrs:
			method = unicode(self["method"].convert(converter))
		else:
			method = None
		if "property" in self.attrs:
			prop = unicode(self["property"].convert(converter))
		else:
			prop = None
		if "class_" in self.attrs:
			class__ = unicode(self["class_"].convert(converter)).replace(u".", u"-")
		else:
			class__ = None
		if "module" in self.attrs:
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
					e = target.a(e, href=(context.base, module, "/index.html#", function))
			elif method is not None:
				if class__ is not None and module is not None:
					e = target.a(e, href=(context.base, module, "/index.html#", class__, "-", method))
			elif prop is not None:
				if class__ is not None and module is not None:
					e = target.a(e, href=(context.base, module, "/index.html#", class__, "-", prop))
			elif class__ is not None:
				if module is not None:
					e = target.a(e, href=(context.base, module, "/index.html#", class__))
			elif module is not None:
				e = target.a(e, href=(context.base, module, "/index.html"))
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
	if not node.find(xsc.FindType(par)): # optimization: one paragraph docstrings don't need a <par> element.
		node = cls.par(node)

	refs = node.find(xsc.FindTypeAll(pyref))
	if inspect.ismethod(thing):
		for ref in refs:
			if "module" not in ref.attrs:
				ref["module"] = cls._getmodulename(thing)
				if "class_" not in ref.attrs:
					ref["class_"] = thing.im_class.__name__
					if "method" not in ref.attrs:
						ref["method"] = thing.__name__
	elif inspect.isfunction(thing):
		for ref in refs:
			if "module" not in ref.attrs:
				ref["module"] = cls._getmodulename(thing)
	elif inspect.isclass(thing):
		for ref in refs:
			if "module" not in ref.attrs:
				ref["module"] = cls._getmodulename(thing)
				if "class_" not in ref.attrs:
					ref["class_"] = thing.__name__
	elif inspect.ismodule(thing):
		for ref in refs:
			if "module" not in ref.attrs:
				ref["module"] = thing.__name__
	return node
getdoc = classmethod(getdoc)


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


def _cmpname(cls, (obj1, name1), (obj2, name2)):
	names = [ name1 or obj1.__name__, name2 or obj2.__name__ ]
	sorts = []
	for name in names:
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
		sorts.append((pos, name))
	return cmp(sorts[0], sorts[1])
_cmpname = classmethod(_cmpname)


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
				sig.append(", ")
			sig.append(cls.arg(args[i]))
		if i >= offset:
			sig.append("=", cls.lit(repr(defaults[i-offset])))
	if varargs:
		if sig:
			sig.append(", ")
		sig.append("*", cls.arg(varargs))
	if varkw:
		if sig:
			sig.append(", ")
		sig.append("**", cls.arg(varkw))
	sig.insert(0, type(name), u"\u200b(") # use "ZERO WIDTH SPACE" to allow linebreaks
	sig.append(")")
	return sig
_codeheader = classmethod(_codeheader)


def explain(cls, thing, name=None, context=[]):
	"""
	<par>Return a &xml; representation of the documentation of
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
		sig = xsc.Frag()
		if name != thing.__name__ and not (thing.__name__.startswith("__") and name=="_" + thing.im_class.__name__ + thing.__name__):
			sig.append(cls.method(name), " = ")
		sig.append("def ", cls._codeheader(thing.im_func, thing.__name__, cls.method), ":")
		return cls.section(cls.title(sig), cls.getdoc(thing), role="method", id=id)
	elif inspect.isfunction(thing):
		name = name or thing.__name__
		context = context + [(thing, name)]
		id = "-".join([info[1] for info in context[1:]])
		sig = xsc.Frag(
			"def ",
			cls._codeheader(thing, name, cls.function),
			":"
		)
		return cls.section(cls.title(sig), cls.getdoc(thing), role="function", id=id)
	elif isinstance(thing, __builtin__.property):
		context = context + [(thing, name)]
		id = "-".join([info[1] for info in context[1:]])
		sig = xsc.Frag(
			"property ", name, ":"
		)
		node = cls.section(cls.title(sig), cls.getdoc(thing), role="property", id=id)
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
			bases.insert(0, u"\u200b(") # use "ZERO WIDTH SPACE" to allow linebreaks
			bases.append(")")
		node = cls.section(
			cls.title(
				"class ",
				cls.class_(name),
				bases,
				":"
			),
			cls.getdoc(thing),
			role="class",
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
			elif inspect.isclass(obj) and not (issubclass(obj, xsc.Namespace) and hasattr(obj, "__file__")):
				classes.append((obj, varname))
		if len(classes):
			classes.sort(cls._cmpname)
			node.append(
				[cls.explain(obj, name, context) for (obj, name) in classes],
			)
		if len(functions):
			functions.sort(cls._cmpname)
			node.append(
				[cls.explain(obj, name, context) for (obj, name) in functions],
			)
		return node

	return xsc.Null
explain = classmethod(explain)


class fodoc(base):
	model = sims.Elements(block)

	def convert(self, converter):
		context = converter[self]
		e = self.content
		converter.push(target=xmlns)
		e = e.convert(converter)
		converter.pop()
		converter.push(target=fo)
		e = e.convert(converter)
		converter.pop()

		e = xsc.Frag(
			xml.XML10(), "\n",
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


class xmlns(xsc.Namespace):
	xmlname = "doc"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/doc"
xmlns.makemod(vars())
