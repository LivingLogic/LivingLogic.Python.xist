#! /usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

from ll.xist import xsc, sims, parse
from ll.xist.ns import html, htmlspecials, meta, xml, chars


xmlns = "http://xmlns.livinglogic.de/xist/demo/media"


class name(xsc.Element):
	xmlns = xmlns
	model = sims.NoElements()

	def convert(self, converter):
		return self.content.convert(converter)


class rc(xsc.Element):
	xmlns = xmlns
	model = sims.NoElements()

	def convert(self, converter):
		return self.content.convert(converter)


class duration(xsc.Element):
	xmlns = xmlns
	model = sims.NoElements()

	def convert(self, converter):
		e = xsc.Frag(self.content.convert(converter), " min")
		return e.convert(converter)


class place(xsc.Element):
	xmlns = xmlns
	model = sims.NoElements()

	def convert(self, converter):
		return self.content.convert(converter)


class date(xsc.Element):
	xmlns = xmlns
	model = sims.NoElements()

	def convert(self, converter):
		return self.content.convert(converter)


class price(xsc.Element):
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(xsc.Element.Attrs):
		class currency(xsc.TextAttr): pass

	def convert(self, converter):
		e = xsc.Frag(self.content, " ", self.attrs.currency)
		return e.convert(converter)


class purchase(xsc.Element):
	xmlns = xmlns
	model = sims.Elements(place, date, price)

	def convert(self, converter):
		e = html.div(self[place], class_="purchase")
		for e2 in self[price]:
			e.append(": ", e2)
		e.append(" ")
		for e2 in self[date]:
			e.append("(", e2, ")")
		return e.convert(converter)


class ld(xsc.Element):
	xmlns = xmlns
	model = sims.Elements(name, duration, purchase)

	def convert(self, converter):
		e = html.li(
			html.span(self[name], class_="name")
		)
		for e2 in self[duration]:
			e.append(" (", e2, ")")
		e.append(self[purchase])
		return e.convert(converter)


class dvd(xsc.Element):
	xmlns = xmlns
	model = sims.Elements(name, rc, duration, purchase)

	def convert(self, converter):
		e = html.li(
			html.span(self[name], class_="name")
		)
		durations = xsc.Frag(self[duration])
		rcs = xsc.Frag(self[rc])
		if len(durations) or len(rcs):
			e.append(" (")
			if len(durations):
				e.append(durations[0])
				if len(rcs):
					e.append("; ")
			if len(rcs):
				e.append("RC ", rcs.withsep(", "))
			e.append(")")
		e.append(self[purchase])
		return e.convert(converter)


class media(xsc.Element):
	xmlns = xmlns
	model = sims.Elements(ld, dvd)

	def convert(self, converter):
		def namekey(node):
			return str(node[name][0].content)

		dvds = xsc.Frag(self[dvd]).sorted(key=namekey)
		lds = xsc.Frag(self[ld]).sorted(key=namekey)

		with xsc.build():
			with xsc.Frag() as e:
				+xml.XML()
				+html.DocTypeXHTML10transitional()
				with html.html():
					with html.head():
						+meta.contenttype()
						+html.title("Media")
						+meta.stylesheet(href="Media.css")
					with htmlspecials.plainbody():
						+html.h1("Media")
						if lds:
							+html.h2(len(lds), " LDs")
							+html.ol(lds)
						if dvds:
							+html.h2(len(dvds), " DVDs")
							+html.ol(dvds)
		return e.convert(converter)


if __name__ == "__main__":
	node = parse.tree(parse.File("Media.xml"), parse.Expat(ns=True), xsc.Pool(vars(), chars, xml))
	node = node[media][0]
	node = node.conv()
	print(node.bytes(encoding="us-ascii"))
