#! /usr/bin/python

import sys
from xsc_html40 import *

class XSCplaintable(XSCtable):
	close = 1

	def AsHTML(self,xsc,mode = None):
		e = XSCtable(xsc.AsHTML(self.content,mode),xsc.AsHTML(self.attrs,mode))

		if not e.has_attr("cellpadding"):
			e["cellpadding"] = 0
		if not e.has_attr("cellspacing"):
			e["cellspacing"] = 0
		if not e.has_attr("border"):
			e["border"] = 0

		return e
RegisterElement("plaintable",XSCplaintable)

class XSCplainbody(XSCbody):
	close = 1

	def AsHTML(self,xsc,mode = None):
		e = XSCbody(xsc.AsHTML(self.content,mode),xsc.AsHTML(self.attrs,mode))

		if not e.has_attr("leftmargin"):
			e["leftmargin"] = 0
		if not e.has_attr("topmargin"):
			e["topmargin"] = 0
		if not e.has_attr("marginheight"):
			e["marginheight"] = 0
		if not e.has_attr("marginwidth"):
			e["marginwidth"] = 0

		return e
RegisterElement("plainbody",XSCplainbody)

class XSCz(XSCElement):
	close = 1

	def AsHTML(self,xsc,mode = None):
		return xsc.AsHTML(["«",xsc.AsHTML(self.content,mode),"»"],mode)
RegisterElement("z",XSCz)

class XSCnbsp(XSCElement):
	close = 0

	def AsHTML(self,xsc,mode = None):
		return xsc.AsHTML("\xA0",mode)
RegisterElement("nbsp",XSCnbsp)

class XSCfilesize(XSCElement):
	close=1

	def AsHTML(self,xsc,mode = None):
		return xsc.FileSize(xsc.ExpandedURL(xsc.AsString(self.content)))
RegisterElement("filesize",XSCfilesize)

class XSCx(XSCElement):
	"content will be ignored: can be used to comment out stuff (e.g. linefeeds)"
	close=1

	def AsHTML(self,xsc,mode = None):
		return ""
RegisterElement("x",XSCx)

class XSCpixel(XSCimg):
	close = 0
	attr_handlers = AppendDict(XSCimg.attr_handlers,{ "color" : XSCStringAttr })
	del attr_handlers["src"]

	def AsHTML(self,xsc,mode = None):
		if not self.has_attr("color"):
			self["color"] = "dot_clear"
		self["src"] = ":Images/Pixels/" + self["color"] + ".gif"
		del self["color"]
		e = XSCimg(xsc.AsHTML(self.content,mode),xsc.AsHTML(self.attrs,mode))

		return e
RegisterElement("pixel",XSCpixel)

if __name__ == "__main__":
	h = XSC(sys.argv[1])
	print str(h)

