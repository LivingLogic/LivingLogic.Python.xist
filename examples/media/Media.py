#!/usr/bin/env python

from xist import xsc, html, specials, meta

class media(xsc.Element):
	empty = 0

	def convert(self, converter=None):
		dvds = self.content.find(type=dvd)
		lds = self.content.find(type=ld)

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

	def convert(self, converter=None):
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

	def convert(self, converter=None):
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
				e.append("RC ", rcs.withSeparator(", "))
			e.append(")")
		e.extend(self.content.find(type=purchase))
		return e.convert(converter)

class name(xsc.Element):
	empty = 0

	def convert(self, converter=None):
		return self.content.convert(converter)

class rc(xsc.Element):
	empty = 0

	def convert(self, converter=None):
		return self.content.convert(converter)

class duration(xsc.Element):
	empty = 0

	def convert(self, converter=None):
		return xsc.Frag(self.content.convert(converter), " min")

class purchase(xsc.Element):
	empty = 0

	def convert(self, converter=None):
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

	def convert(self, converter=None):
		return self.content.convert(converter)

class date(xsc.Element):
	empty = 0

	def convert(self, converter=None):
		return self.content.convert(converter)

class price(xsc.Element):
	empty = 0
	attrHandlers = {"currency": xsc.TextAttr}

	def convert(self, converter=None):
		return xsc.Frag(self.content, " ", self["currency"]).convert(converter)

namespace = xsc.Namespace("media", "http://www.livinglogic.de/DTDs/Media.dtd", vars())

if __name__=="__main__":
	import time
	t1 = time.clock()
	xsc.xsc.parse("Media.xml").find(type=media).convert().write(open("Media.html","wb"))
	t2 = time.clock()
	print "%.02f sec" % (t2-t1)

