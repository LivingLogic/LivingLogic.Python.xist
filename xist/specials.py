#! /usr/bin/env python

"""
A XSC module that contains a collection of useful elements.
"""

__version__ = "$Revision$"
# $Source$

import sys
import types
import string
import xsc
import html

class plaintable(html.table):
	empty = 0

	def asHTML(self):
		e = html.table(self.content,self.attrs)
		if not e.has_attr("cellpadding"):
			e["cellpadding"] = "0"
		if not e.has_attr("cellspacing"):
			e["cellspacing"] = "0"
		if not e.has_attr("border"):
			e["border"] = "0"

		return e.asHTML()
xsc.registerElement(plaintable)

class plainbody(html.body):
	empty = 0

	def asHTML(self):
		e = html.body(self.content,self.attrs)
		if not e.has_attr("leftmargin"):
			e["leftmargin"] = "0"
		if not e.has_attr("topmargin"):
			e["topmargin"] = "0"
		if not e.has_attr("marginheight"):
			e["marginheight"] = "0"
		if not e.has_attr("marginwidth"):
			e["marginwidth"] = "0"

		return e.asHTML()
xsc.registerElement(plainbody)

class z(xsc.Element):
	empty = 0

	def asHTML(self):
		e = xsc.Frag(["«" , self.content , "»" ])

		return e.asHTML()
xsc.registerElement(z)

class nbsp(xsc.Element):
	empty = 1

	def asHTML(self):
		return xsc.CharRef(160)
xsc.registerElement(nbsp)

class filesize(xsc.Element):
	empty = 1
	attr_handlers = { "href" : xsc.URLAttr }

	def asHTML(self):
		return xsc.Text(self["href"].FileSize())
xsc.registerElement(filesize)

class x(xsc.Element):
	"""content will be ignored: can be used to comment out stuff (e.g. linefeeds)"""
	close=1

	def asHTML(self):
		return None
xsc.registerElement(x)

class pixel(html.img):
	empty = 1
	attr_handlers = xsc.appendDict(html.img.attr_handlers,{ "color" : xsc.ColorAttr })
	del attr_handlers["src"]

	def asHTML(self):
		e = html.img(self.content)
		color = "dot_clear"
		for attr in self.attrs.keys():
			if attr == "color":
				color = self["color"]
			else:
				e[attr] = self[attr]
		e["src"] = [ ":images/pixels/" , color , ".gif" ]

		return e.asHTML()
xsc.registerElement(pixel)

class cap(xsc.Element):
	empty = 0
	
	def asHTML(self):
		e = str(self.content.asHTML())
		if type(e) == types.ListType:
			e = e[0]
		e = e + "?"
		result = xsc.Frag()
		collect = ""
		innini = 0
		for i in range(len(e)):
			if (i == len(e)) or ((e[i] in string.lowercase) and (innini==0)) or ((e[i] not in string.lowercase) and (innini==1)):
				if innini==0:
					result.append(collect)
				else:
					result.append(span([ string.upper(collect) ],Class="nini" ))
				if i != len(e):
					collect = e[i]
				innini = 1-innini
			else:
				collect = collect + e[i]
		return result
xsc.registerElement(cap)

class endash(xsc.Element):
	empty = 1

	def asHTML(self):
		return xsc.Text("-")
xsc.registerElement(endash)

class emdash(xsc.Element):
	empty = 1

	def asHTML(self):
		return xsc.Text("-")
xsc.registerElement(emdash)

class include(xsc.Element):
	empty = 1
	attr_handlers = { "src" : xsc.URLAttr }

	def asHTML(self):
		e = xsc.xsc.parseFile(self["src"].forInput())

		return e.asHTML()
xsc.registerElement(include)

if __name__ == "__main__":
	xsc.make()

