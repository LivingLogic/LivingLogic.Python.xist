#!/usr/bin/env python

from xist import xsc, parsers
from xist.ns import html, specials, meta

def nameCompare(node1, node2):
	name1 = unicode(node1.find(type=name)[0].content)
	name2 = unicode(node2.find(type=name)[0].content)
	return cmp(name1, name2)

class media(xsc.Element):
	empty = 0

	def convert(self, converter):
		dvds = self.content.find(type=dvd).sorted(nameCompare)
		lds = self.content.find(type=ld).sorted(nameCompare)

		e = xsc.Frag(
			html.DocTypeHTML401transitional(),
			html.html(
				html.head(
					meta.contenttype(),
					html.title("Media"),
					meta.stylesheet(href="Media.css")
				),
				specials.plainbody(
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
	empty = 0

	def convert(self, converter):
		e = html.li(
			html.span(self.content.find(type=name)[0], class_="name")
		)
		durations = self.content.find(type=duration)
		if len(durations):
			e.append(" (", durations[0], ")")
		e.extend(self.content.find(type=purchase))
		return e.convert(converter)

class dvd(xsc.Element):
	empty = 0

	def convert(self, converter):
		e = html.li(
			html.span(self.content.find(type=name)[0], class_="name")
		)
		durations = self.content.find(type=duration)
		rcs = self.content.find(type=rc)
		if len(durations) or len(rcs):
			e.append(" (")
			if len(durations):
				e.append(durations[0])
				if len(rcs):
					e.append("; ")
			if len(rcs):
				e.append("RC ", rcs.withSep(", "))
			e.append(")")
		e.extend(self.content.find(type=purchase))
		return e.convert(converter)

class name(xsc.Element):
	empty = 0

	def convert(self, converter):
		return self.content.convert(converter)

class rc(xsc.Element):
	empty = 0

	def convert(self, converter):
		return self.content.convert(converter)

class duration(xsc.Element):
	empty = 0

	def convert(self, converter):
		return xsc.Frag(self.content.convert(converter), " min")

class purchase(xsc.Element):
	empty = 0

	def convert(self, converter):
		places = self.find(type=place)
		dates = self.find(type=date)
		prices = self.find(type=price)

		e = html.div(places[0], class_="purchase")
		if len(prices):
			e.append(": ", prices[0])
		e.append(" ")
		if len(dates):
			e.append("(", dates[0], ")")
		return e.convert(converter)

class place(xsc.Element):
	empty = 0

	def convert(self, converter):
		return self.content.convert(converter)

class date(xsc.Element):
	empty = 0

	def convert(self, converter):
		return self.content.convert(converter)

class price(xsc.Element):
	empty = 0
	attrHandlers = {"currency": xsc.TextAttr}

	def convert(self, converter):
		return xsc.Frag(self.content, " ", self["currency"]).convert(converter)

namespace = xsc.Namespace("media", "http://www.livinglogic.de/DTDs/Media.dtd", vars())

if __name__ == "__main__":
	parsers.parseFile("Media.xml").find(type=media).conv().write(open("Media.html","wb"))

