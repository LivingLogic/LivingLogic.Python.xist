#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from ll.xist import xsc, sims, parsers, xfind
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
		e = xsc.Frag(
			html.DocTypeHTML401transitional(),
			html.html(
				html.head(
					meta.contenttype(),
					html.title("Python quotes"),
					meta.stylesheet(href="root:python-quotes.css")
				),
				html.body(
					html.h1("Python quotes"),
					html.div("(Generated from ", html.a(url, href=url), ")"),
					self/quotation # We want to get rid of the excessive whitespace
				)
			)
		)

		return e.convert(converter)


class __ns__(xsc.Namespace):
	xmlname = "quotations"
	xmlurl = "http://xmlns.livinglogic.de/xist/examples/python-quotes"
__ns__.update(vars())


if __name__ == "__main__":
	prefixes = xsc.Prefixes([__ns__, html, xml])
	base = "root:python-quotes.html"
	# We don't validate, because the XML contains broken HTML (<pre> inside <p>)
	e = parsers.parseURL(url, base=base, saxparser=parsers.ExpatParser, prefixes=prefixes, validate=False)
	e = xfind.first(e/quotations)
	e = e.compact().conv()
	e.write(open("python-quotes.html", "wb"), base=base, encoding="iso-8859-1", validate=False)
