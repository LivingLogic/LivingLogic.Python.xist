#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from ll.xist import xsc, sims, parsers
from ll.xist.ns import xml, html, meta


url = "python-quotes.xml"


class note(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = html.div(self.content, class_="note")

		return e.convert(converter)


class foreign(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = html.em(self.content)

		return e.convert(converter)


class author(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = self.content

		return e.convert(converter)


class source(xsc.Element):
	model = sims.NoElements()

	def convert(self, converter):
		e = html.div(self.content, class_="source")

		return e.convert(converter)


class quotation(xsc.Element):
	model = sims.Elements(author, source, note)

	class Attrs(xsc.Element.Attrs):
		class date(xsc.TextAttr): pass

	def convert(self, converter):
		e = html.div(self.content, class_="quotation")

		return e.convert(converter)


class quotations(xsc.Element):
	model = sims.Elements(quotation)

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


class xmlns(xsc.Namespace):
	xmlname = "quotations"
	xmlurl = "http://xmlns.livinglogic.de/xist/examples/python-quotes"
xmlns.update(vars())


if __name__ == "__main__":
	prefixes = xsc.Prefixes([xmlns, html, xml])
	e = parsers.parseURL(url, saxparser=parsers.ExpatParser, prefixes=prefixes)
	e = e.findfirst(xsc.FindType(quotations))
	e = e.compact().conv()
	e.write(open("python-quotes.html", "wb"), encoding="iso-8859-1")
