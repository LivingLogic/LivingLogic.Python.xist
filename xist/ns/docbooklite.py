import sys, types

from xist import xsc, converters
from xist.ns import html, specials, abbr, meta

class itemizedlist(xsc.Element):
	"""
	A list in which each entry is marked with a bullet or other dingbat
	"""
	empty = 0

	def convert(self, converter=None):
		e = html.ul(self.content)
		return e.convert(converter)

class programlisting(xsc.Element):
	"""
	A literal listing of all or part of a program
	"""
	empty = 0

	def convert(self, converter=None):
		e = html.pre(class_="programlisting")
		for child in self.content:
			child = child.convert(converter)
			if isinstance(child, xsc.Text):
				for c in child:
					if c=="\t":
						e.append(html.span(u"···", class_="tab"))
					else:
						e.append(c)
			else:
				e.append(child)
		return e.convert(converter)

class example(xsc.Element):
	"""
	A formal example, with a title
	"""
	empty = 0
	attrHandlers = {"title": xsc.TextAttr}

	def convert(self, converter=None):
		e = xsc.Frag(self.content)
		if self.hasAttr("title"):
			e.append(html.div(self["title"], class_="example-title"))
		return e.convert(converter)

class option(xsc.Element):
	"""
	An option for a software command
	"""
	empty = 0

	def convert(self, converter=None):
		e = html.code(self.content, class_="option")
		return e.convert(converter)

class literal(xsc.Element):
	"""
	Inline text that is some literal value
	"""
	empty = 0

	def convert(self, converter=None):
		e = html.code(self.content, class_="literal")
		return e.convert(converter)

class function(xsc.Element):
	"""
	The name of a function or subroutine, as in a programming language
	"""
	empty = 0

	def convert(self, converter=None):
		e = html.code(self.content, class_="function")
		return e.convert(converter)

class classname(xsc.Element):
	"""
	The name of a class, in the object-oriented programming sense
	"""
	empty = 0

	def convert(self, converter=None):
		e = html.code(self.content, class_="classname")
		return e.convert(converter)

class replaceable(xsc.Element):
	"""
	Content that may or must be replaced by the user
	"""
	empty = 0

	def convert(self, converter=None):
		e = html.var(self.content, class_="replaceable")
		return e.convert(converter)

class markup(xsc.Element):
	"""
	A string of formatting markup in text that is to be represented literally
	"""
	empty = 0

	def convert(self, converter=None):
		e = html.code(self.content, class_="markup")
		return e.convert(converter)

class parameter(xsc.Element):
	"""
	A value or a symbolic reference to a value
	"""
	empty = 0

	def convert(self, converter=None):
		e = html.code(self.content, class_="parameter")
		return e.convert(converter)

class filename(xsc.Element):
	"""
	The name of a file
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr}

	def convert(self, converter=None):
		e = html.code(self.content, class_="filename")
		return e.convert(converter)

class para(xsc.Element):
	"""
	A paragraph
	"""
	empty = 0

	def convert(self, converter=None):
		e = html.p(self.content)
		return e.convert(converter)

class title(xsc.Element):
	"""
	The text of the title of a section of a document or of a formal block-level element
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr}

	def convert(self, converter=None):
		e = self.content
		return e.convert(converter)

class section(xsc.Element):
	"""
	A recursive section
	"""
	empty = 0

	def convert(self, converter=None):
		if converter is None:
			converter = converters.Converter()
		if not hasattr(converter, "depth"):
			converter.depth = 1
		ts = xsc.Frag()
		cs = xsc.Frag()
		for child in self:
			if isinstance(child, title):
				ts.append(child)
			else:
				cs.append(child)
		e = xsc.Frag()
		for t in ts:
			e.append(html.namespace.elementsByName["h%d" % converter.depth](t.content))
		for c in cs:
			e.append(c)
		converter.depth += 1
		e = e.convert(converter)
		converter.depth -= 1
		return e

namespace = xsc.Namespace("dbl", "http://www.livinglogic.de/DTDs/DocBookLite.dtd", vars())
