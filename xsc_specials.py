#! /usr/bin/env python

import sys
from xsc_html40 import *

class plaintable(table):
	close = 1

	def _doAsHTML(self):
		e = table(self.content.asHTML(),self.attrs.asHTML())
		if not e.has_attr("cellpadding"):
			e["cellpadding"] = "0"
		if not e.has_attr("cellspacing"):
			e["cellspacing"] = "0"
		if not e.has_attr("border"):
			e["border"] = "0"

		return e
RegisterElement("plaintable",plaintable)

class plainbody(body):
	close = 1

	def _doAsHTML(self):
		e = body(self.content.asHTML(),self.attrs.asHTML())
		if not e.has_attr("leftmargin"):
			e["leftmargin"] = "0"
		if not e.has_attr("topmargin"):
			e["topmargin"] = "0"
		if not e.has_attr("marginheight"):
			e["marginheight"] = "0"
		if not e.has_attr("marginwidth"):
			e["marginwidth"] = "0"

		return e
RegisterElement("plainbody",plainbody)

class z(XSCElement):
	close = 1

	def _doAsHTML(self):
		return XSCFrag(["«" , self.content , "»" ])
RegisterElement("z",z)

class nbsp(XSCElement):
	close = 0

	def __str__(self):
		return "&nbsp;"
RegisterElement("nbsp",nbsp)

class filesize(XSCElement):
	close = 0
	attr_handlers = { "href" : XSCurl }

	def _doAsHTML(self):
		return str(FileSize(str(self["href"].asHTML())))
RegisterElement("filesize",filesize)

class x(XSCElement):
	"""content will be ignored: can be used to comment out stuff (e.g. linefeeds)"""
	close=1

	def _doAsHTML(self):
		return ""
RegisterElement("x",x)

class pixel(img):
	close = 0
	attr_handlers = AppendDict(img.attr_handlers,{ "color" : XSCFrag })
	del attr_handlers["src"]

	def asHTML(self):
		e = img(self.content,self.attrs - [ "color" ])
		if self.has_attr("color"):
			color = self["color"]
		else:
			color = "dot_clear"
		e["src"] = XSCFrag([":Images/Pixels/" , color , ".gif" ])

		return e
RegisterElement("pixel",pixel)

class cap(XSCElement):
	close = 1
	
	def _doAsHTML(self):
		e = str(self.content.asHTML())
		if type(e) == types.ListType:
			e = e[0]
		e = e + "?"
		result = XSCFrag()
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
RegisterElement("cap",cap)

if __name__ == "__main__":
	print str(xsc.parsefile(sys.argv[1]).asHTML())

