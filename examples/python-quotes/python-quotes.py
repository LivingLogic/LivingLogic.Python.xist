#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from ll.xist import xsc, parsers
from ll.xist.ns import html, meta

url = "python-quotes.xml"

class quotations(xsc.Element):
	empty = False

	def convert(self, converter):
		header = html.head(
			meta.contenttype(),
			html.title("Python quotes"),
			meta.stylesheet(href="python-quotes.css")
		)

		description = html.div("(Generated from ", html.a(url, href=url), ")")

		# We want to get rid of the excessive whitespace
		quotations = self.content.find(xsc.FindType(quotation))

		e = xsc.Frag(
			html.DocTypeHTML401transitional(),
			html.html(
				header,
				html.body(
					html.h1("Python quotes"),
					description,
					quotations
				)
			)
		)

		return e.convert(converter)

class quotation(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class date(xsc.TextAttr): pass

	def convert(self, converter):
		e = html.div(self.content, class_="quotation")

		return e.convert(converter)

class source(xsc.Element):
	empty = False

	def convert(self, converter):
		e = html.div(self.content, class_="source")

		return e.convert(converter)

class note(xsc.Element):
	empty = False

	def convert(self, converter):
		e = html.div(self.content, class_="note")

		return e.convert(converter)

class author(xsc.Element):
	empty = False

	def convert(self, converter):
		e = self.content

		return e.convert(converter)

class foreign(xsc.Element):
	empty = False

	def convert(self, converter):
		e = html.em(self.content)

		return e.convert(converter)

class xmlns(xsc.Namespace):
	xmlname = "quotations"
	xmlurl = "http://xmlns.livinglogic.de/xist/examples/python-quotes"
xmlns.update(vars())

if __name__ == "__main__":
	e = parsers.parseURL(url, parser=parsers.ExpatParser())
	e = e.findfirst(xsc.FindType(quotations))
	e = e.compact().conv()
	print e.asBytes(encoding="iso-8859-1")

