#! /usr/bin/env python

"""
A XSC module that contains a collection of useful elements.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import sys
import types
import time
time_ = time
import string
import xsc
import html

class plaintable(html.table):
	"""
	a HTML table where the values of the attributes cellpadding, cellspacing and
	border default to 0.
	"""
	empty = 0

	def asHTML(self):
		e = html.table(self.content,self.attrs)
		if not e.has_attr("cellpadding"):
			e["cellpadding"] = 0
		if not e.has_attr("cellspacing"):
			e["cellspacing"] = 0
		if not e.has_attr("border"):
			e["border"] = 0

		return e.asHTML()

class plainbody(html.body):
	"""
	a HTML body where the attributes leftmaring, topmargin, marginheight and
	marginwidth default to 0.
	"""
	empty = 0

	def asHTML(self):
		e = html.body(self.content,self.attrs)
		if not e.has_attr("leftmargin"):
			e["leftmargin"] = 0
		if not e.has_attr("topmargin"):
			e["topmargin"] = 0
		if not e.has_attr("marginheight"):
			e["marginheight"] = 0
		if not e.has_attr("marginwidth"):
			e["marginwidth"] = 0

		return e.asHTML()

class z(xsc.Element):
	"""
	puts it's content into french quotes
	"""
	empty = 0

	def asHTML(self):
		e = xsc.Frag("«",self.content,"»")

		return e.asHTML()

	def asPlainString(self):
		return '«' + self.content.asPlainString() + '»'

xsc.registerElement(z)

class nbsp(xsc.Element):
	"""
	a nonbreakable space as an element
	"""
	empty = 1

	def asHTML(self):
		return xsc.CharRef(160)

class filesize(xsc.Element):
	"""
	the size (in bytes) of the file whose URL is the attribute href
	as a text node.
	"""
	empty = 1
	attrHandlers = { "href" : xsc.URLAttr }

	def asHTML(self):
		return xsc.Text(self["href"].FileSize())

class filetime(xsc.Element):
	"""
	the time of the last modification of the file whose URL is in the attibute href
	as a text node.
	"""
	empty = 1
	attrHandlers = { "href" : xsc.URLAttr , "format" : xsc.TextAttr }

	def asHTML(self):
		return xsc.Text(self["href"].FileTime())

class time(xsc.Element):
	"""
	the current time (i.e. the time when asHTML() is called). You can specify the
	format of the string in the attribute format, which is a strftime() compatible
	string.
	"""
	empty = 1
	attrHandlers = { "format" : xsc.TextAttr }

	def asHTML(self):
		if self.has_attr("format"):
			format = self["format"].asPlainString()
		else:
			format = "%d. %b. %Y, %H:%M"

		return xsc.Text(time_.strftime(format,time_.gmtime(time_.time())))

class x(xsc.Element):
	"""
	element whose content will be ignored when converted to HTML:
	this can be used to comment out stuff.
	"""
	close=1

	def asHTML(self):
		return xsc.Null()

class pixel(html.img):
	"""
	element for single pixel images, the default is the image
	":images/pixels/dot_clear.gif", but you can specify the color
	as a six digit hex string, which will be used as the filename,
	i.e. <pixel color="000000"/> results in
	<img src=":images/pixels/000000.gif">.

	In addition to that you can specify width and height attributes
	(and every other allowed attribute for the img element) as usual.
	"""

	empty = 1
	attrHandlers = xsc.appendDict(html.img.attrHandlers,{ "color" : xsc.ColorAttr })
	del attrHandlers["src"]

	def asHTML(self):
		e = html.img(self.content)
		color = "dot_clear"
		for attr in self.attrs.keys():
			if attr == "color":
				color = self["color"]
			else:
				e[attr] = self[attr]
		e["src"] = (":images/pixels/",color,".gif")

		return e.asHTML()

class caps(xsc.Element):
	"""
	returns a fragment that contains the content string converted to caps and small caps.
	This is done by converting all lowercase letters to uppercase and packing them into a
	<span class="nini">...</span>. This element is meant to be a workaround until all
	browsers support the CSS feature "font-variant: small-caps".
	"""
	empty = 0

	def asHTML(self):
		e = self.content.asPlainString() + "?"
		result = xsc.Frag()
		collect = ""
		innini = 0
		for i in range(len(e)):
			if (i == len(e)) or ((e[i] in string.lowercase) and (innini==0)) or ((e[i] not in string.lowercase) and (innini==1)):
				if innini==0:
					result.append(collect)
				else:
					result.append(html.span([ string.upper(collect) ],Class="nini" ))
				if i != len(e):
					collect = e[i]
				innini = 1-innini
			else:
				collect = collect + e[i]
		return result

	def asPlainString(self):
			return string.upper(self.content.asPlainString())

class endash(xsc.Element):
	empty = 1

	def asHTML(self):
		return xsc.Text("-")

class emdash(xsc.Element):
	empty = 1

	def asHTML(self):
		return xsc.Text("-")

class include(xsc.Element):
	empty = 1
	attrHandlers = { "src" : xsc.URLAttr }

	def asHTML(self):
		e = xsc.xsc.parse(self["src"].forInput())

		return e.asHTML()

xsc.registerAllElements(vars(),"specials")

# Control characters (not part of HTML)
xsc.registerEntity("lf",xsc.CharRef(10))  # line feed
xsc.registerEntity("cr",xsc.CharRef(13))  # carriage return
xsc.registerEntity("tab",xsc.CharRef(9))  # horizontal tab
xsc.registerEntity("esc",xsc.CharRef(27)) # escape

if __name__ == "__main__":
	xsc.make()
