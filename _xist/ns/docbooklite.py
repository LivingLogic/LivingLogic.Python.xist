from xist import xsc, converters
from xist.ns import html, docbook

class itemizedlist(xsc.Element):
	"""
	A list in which each entry is marked with a bullet or other dingbat
	"""
	empty = 0

	def convert(self, converter):
		e = html.ul(self.content)
		return e.convert(converter)

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
				for c in child:
					if c=="\t":
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
		e = html.code(self.content, class_="option")
		return e.convert(converter)

class literal(xsc.Element):
	"""
	Inline text that is some literal value
	"""
	empty = 0

	def convert(self, converter):
		e = html.code(self.content, class_="literal")
		return e.convert(converter)

class function(xsc.Element):
	"""
	The name of a function or subroutine, as in a programming language
	"""
	empty = 0

	def convert(self, converter):
		e = html.code(self.content, class_="function")
		return e.convert(converter)

class classname(xsc.Element):
	"""
	The name of a class, in the object-oriented programming sense
	"""
	empty = 0

	def convert(self, converter):
		e = html.code(self.content, class_="classname")
		return e.convert(converter)

class replaceable(xsc.Element):
	"""
	Content that may or must be replaced by the user
	"""
	empty = 0

	def convert(self, converter):
		e = html.var(self.content, class_="replaceable")
		return e.convert(converter)

class markup(xsc.Element):
	"""
	A string of formatting markup in text that is to be represented literally
	"""
	empty = 0

	def convert(self, converter):
		e = html.code(self.content, class_="markup")
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

class application(xsc.Element):
	"""
	The name of a software program
	"""
	empty = 0

	def convert(self, converter):
		e = html.span(self.content, class_="application")
		return e.convert(converter)

class para(xsc.Element):
	"""
	A paragraph
	"""
	empty = 0

	def convert(self, converter):
		e = html.p(self.content)
		return e.convert(converter)

class title(xsc.Element):
	"""
	The text of the title of a section of a document or of a formal block-level element
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr}

	def convert(self, converter):
		e = self.content
		return e.convert(converter)

class section(xsc.Element):
	"""
	A recursive section
	"""
	empty = 0

	def convert(self, converter):
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
			h = html.namespace.elementsByName["h%d" % context.depth]()
			if converter.target=="text":
				h.append(html.br(), t.content, html.br(), "="*len(t.content.convert(converter).asPlainString()))
			else:
				h.append(t.content)
			e.append(h)
		for c in cs:
			e.append(c)
		context.depth += 1
		e = e.convert(converter)
		context.depth -= 1
		return e

class para(xsc.Element):
	"""
	"""
	empty = 0

	def convert(self, converter):
		e = html.p(*self.content)
		return e.convert(converter)

class pyref(xsc.Element):
	"""
	reference to a Python object:
	module, class, method, function, variable or argument
	"""
	empty = 0
	attrHandlers = {"module": xsc.TextAttr, "class": xsc.TextAttr, "method": xsc.TextAttr, "function": xsc.TextAttr, "var": xsc.TextAttr, "arg": xsc.TextAttr}

	base = "http://localhost:7464/"

	def convert(self, converter):
		if self.hasAttr("var"):
			var = self["var"].convert(converter).asPlainString()
		else:
			var = None
		if self.hasAttr("arg"):
			arg = self["arg"].convert(converter).asPlainString()
		else:
			arg = None
		if self.hasAttr("function"):
			function = self["function"].convert(converter).asPlainString()
		else:
			function = None
		if self.hasAttr("method"):
			method = self["method"].convert(converter).asPlainString()
		else:
			method = None
		if self.hasAttr("class"):
			class_ = self["class"].convert(converter).asPlainString()
		else:
			class_ = None
		if self.hasAttr("module"):
			module = self["module"].convert(converter).asPlainString()
		else:
			module = None

		e = self.content
		if converter is not None and converter.target=="docbook":
			if var is not None:
				e = e # FIXME
			elif arg is not None:
				e = docbook.parameter(e)
			elif function is not None:
				e = docbook.function(e)
			elif method is not None:
				e = docbook.function(e, type="method")
			elif class_ is not None:
				e = docbook.classname(e)
			elif module is not None:
				e = e # FIXME
		else:
			if var is not None:
				e = html.code(e, class_="pyvar")
			elif arg is not None:
				e = html.code(e, class_="pyarg")
			elif function is not None:
				e = html.code(e, class_="pyfunction")
				if module is not None:
					e = html.a(e, href=(self.base, module, ".html#", function))
			elif method is not None:
				e = html.code(e, class_="pymethod")
				if class_ is not None and module is not None:
					e = html.a(e, href=(self.base, module, ".html#", class_, "-", method))
			elif class_ is not None:
				e = html.code(e, class_="pyclass")
				if module is not None:
					e = html.a(e, href=(self.base, ".html#", class_))
			elif module is not None:
				e = html.code(e, class_="pymodule")
				e = html.a(e, href=(self.base, module, ".html"))
			else:
				e = html.code(e)
		return e.convert(converter)

namespace = xsc.Namespace("dbl", "http://www.livinglogic.de/DTDs/DocBookLite.dtd", vars())
