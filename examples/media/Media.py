#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from ll.xist import xsc, parsers
from ll.xist.ns import html, htmlspecials, meta, xml

def nameCompare(node1, node2):
	name1 = unicode(node1.content.findfirst(xsc.FindType(name)).content)
	name2 = unicode(node2.content.findfirst(xsc.FindType(name)).content)
	return cmp(name1, name2)

class media(xsc.Element):
	empty = False

	def convert(self, converter):
		dvds = self.content.find(xsc.FindType(dvd)).sorted(nameCompare)
		lds = self.content.find(xsc.FindType(ld)).sorted(nameCompare)

		e = xsc.Frag(
			html.DocTypeHTML401transitional(),
			html.html(
				html.head(
					meta.contenttype(),
					html.title("Media"),
					meta.stylesheet(href="Media.css")
				),
				htmlspecials.plainbody(
					html.h1("Media")
				)
			)
		)
		if lds:
			e[-1][-1].append(html.h2(len(lds), " LDs"), html.ol(lds))
		if dvds:
			e[-1][-1].append(html.h2(len(dvds), " DVDs"), html.ol(dvds))
		return e.convert(converter)

class ld(xsc.Element):
	empty = False

	def convert(self, converter):
		e = html.li(
			html.span(self.content.findfirst(xsc.FindType(name)), class_="name")
		)
		durations = self.content.find(xsc.FindType(duration))
		if len(durations):
			e.append(" (", durations[0], ")")
		e.append(self.content.find(xsc.FindType(purchase)))
		return e.convert(converter)

class dvd(xsc.Element):
	empty = False

	def convert(self, converter):
		e = html.li(
			html.span(self.content.findfirst(xsc.FindType(name)), class_="name")
		)
		durations = self.content.find(xsc.FindType(duration))
		rcs = self.content.find(xsc.FindType(rc))
		if len(durations) or len(rcs):
			e.append(" (")
			if len(durations):
				e.append(durations[0])
				if len(rcs):
					e.append("; ")
			if len(rcs):
				e.append("RC ", rcs.withsep(", "))
			e.append(")")
		e.append(self.content.find(xsc.FindType(purchase)))
		return e.convert(converter)

class name(xsc.Element):
	empty = False

	def convert(self, converter):
		return self.content.convert(converter)

class rc(xsc.Element):
	empty = False

	def convert(self, converter):
		return self.content.convert(converter)

class duration(xsc.Element):
	empty = False

	def convert(self, converter):
		return xsc.Frag(self.content.convert(converter), " min")

class purchase(xsc.Element):
	empty = False

	def convert(self, converter):
		places = self.content.find(xsc.FindType(place))
		dates = self.content.find(xsc.FindType(date))
		prices = self.content.find(xsc.FindType(price))

		e = html.div(places[0], class_="purchase")
		if len(prices):
			e.append(": ", prices[0])
		e.append(" ")
		if len(dates):
			e.append("(", dates[0], ")")
		return e.convert(converter)

class place(xsc.Element):
	empty = False

	def convert(self, converter):
		return self.content.convert(converter)

class date(xsc.Element):
	empty = False

	def convert(self, converter):
		return self.content.convert(converter)

class price(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class currency(xsc.TextAttr): pass

	def convert(self, converter):
		return xsc.Frag(self.content, " ", self["currency"]).convert(converter)

class xmlns(xsc.Namespace):
	xmlname = "media"
	xmlurl = "http://xmlns.livinglogic.de/xist/example/media"
xmlns.update(vars())

if __name__ == "__main__":
	prefixes = xsc.Prefixes(xmlns, xml=xml)
	node = parsers.parseFile("Media.xml", prefixes=prefixes)
	node = node.findfirst(xsc.FindType(media))
	node = node.conv()
	node.write(open("Media.html","wb"))

