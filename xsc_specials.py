#! /usr/bin/python

import sys
from xsc_html40 import *

class XSCplaintable(XSCtable):
	close = 1

	def __str__(self):
		if not self.has_attr("cellpadding"):
			self["cellpadding"] = 0
		if not self.has_attr("cellspacing"):
			self["cellspacing"] = 0
		if not self.has_attr("border"):
			self["border"] = 0

		return str(XSCtable(self.content,self.attrs))
RegisterElement("plaintable",XSCplaintable)

class XSCplainbody(XSCbody):
	close = 1

	def __str__(self):
		if not self.has_attr("leftmargin"):
			self["leftmargin"] = 0
		if not self.has_attr("topmargin"):
			self["topmargin"] = 0
		if not self.has_attr("marginheight"):
			self["marginheight"] = 0
		if not self.has_attr("marginwidth"):
			self["marginwidth"] = 0

		return str(XSCbody(self.content,self.attrs))
RegisterElement("plainbody",XSCplainbody)

class XSCz(XSCElement):
	close = 1

	def __str__(self,xsc,mode = None):
		return str("«" + self.content + "»")
RegisterElement("z",XSCz)

class XSCnbsp(XSCElement):
	close = 0

	def __str__(self):
		return "&nbsp;"
RegisterElement("nbsp",XSCnbsp)

class XSCfilesize(XSCElement):
	close = 0
	attr_handlers = { "href" : XSCURLAttr }

	def __str__(self):
		return str(FileSize(str(self["href"])))
RegisterElement("filesize",XSCfilesize)

class XSCx(XSCElement):
	"content will be ignored: can be used to comment out stuff (e.g. linefeeds)"
	close=1

	def __str__(self):
		return ""
RegisterElement("x",XSCx)

class XSCpixel(XSCimg):
	close = 0
	attr_handlers = AppendDict(XSCimg.attr_handlers,{ "color" : XSCStringAttr })
	del attr_handlers["src"]

	def __str__(self):
		if not self.has_attr("color"):
			self["color"] = "dot_clear"
		self["src"] = XSCURLAttr(":Images/Pixels/" + html(self["color"]) + ".gif")
		del self["color"]
		return str(XSCimg(self.content,self.attrs))
RegisterElement("pixel",XSCpixel)

if __name__ == "__main__":
	h = XSC(sys.argv[1])
	print str(h)

