#! /usr/bin/env python

from xist import xsc, parsers
from xist.ns import html, specials, meta

url = "http://amk.ca/quotations/python-quotes.xml"
#url = "python-quotes.xml"

class quotations(xsc.Element):
	empty = 0

	def convert(self, converter):
		header = html.head(
			meta.contenttype(),
			html.title("Python quotes"),
			meta.stylesheet(href="python-quotes.css")
		)

		description = html.div("(Generated from ", html.a(url, href=url), ")")

		# We want to get rid of the excessive whitespace
		quotations = self.find(type=quotation)

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
	empty = 0

	def convert(self, converter):
		e = html.div(self.content, class_="quotation")

		return e.convert(converter)

class source(xsc.Element):
	empty = 0

	def convert(self, converter):
		e = html.div(self.content, class_="source")

		return e.convert(converter)

class note(xsc.Element):
	empty = 0

	def convert(self, converter):
		e = html.div(self.content, class_="note")

		return e.convert(converter)

class author(xsc.Element):
	empty = 0

	def convert(self, converter):
		e = self.content

		return e.convert(converter)

class foreign(xsc.Element):
	empty = 0

	def convert(self, converter):
		e = html.em(self.content)

		return e.convert(converter)

namespace = xsc.Namespace("pq","http://www.python.org/topics/xml/dtds/qel-2.0.dtd",vars())

if __name__ == "__main__":
	e = parsers.parseURL(url, parser=parsers.ExpatParser())
	e = e.find(type=quotations)[0]
	e = e.compact().convert()
	print e.asBytes(encoding="iso-8859-1")

