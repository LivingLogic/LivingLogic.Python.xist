#! /usr/bin/python

import sys
from xsc_html40 import *

class plaintable(table):
	close = 1

	def AsHTML(self,xsc,mode = None):
		e = table(xsc.AsHTML(self.content,mode),xsc.AsHTML(self.attrs,mode))

		if not e.has_attr("cellpadding"):
			e["cellpadding"] = 0
		if not e.has_attr("cellspacing"):
			e["cellspacing"] = 0
		if not e.has_attr("border"):
			e["border"] = 0

		return e
handlers["plaintable"] = plaintable

class plainbody(body):
	close = 1

	def AsHTML(self,xsc,mode = None):
		e = body(xsc.AsHTML(self.content,mode),xsc.AsHTML(self.attrs,mode))

		if not e.has_attr("leftmargin"):
			e["leftmargin"] = 0
		if not e.has_attr("topmargin"):
			e["topmargin"] = 0
		if not e.has_attr("marginheight"):
			e["marginheight"] = 0
		if not e.has_attr("marginwidth"):
			e["marginwidth"] = 0

		return e
handlers["plainbody"] = plainbody

class z(XSCElement):
	close = 1

	def AsHTML(self,xsc,mode = None):
		return xsc.AsHTML(["«",xsc.AsHTML(self.content,mode),"»"],mode)
handlers["z"] = z

class nbsp(XSCElement):
	close = 0

	def AsHTML(self,xsc,mode = None):
		return xsc.AsHTML("\xA0",mode)

class filesize(XSCElement):
	close=1

	def AsHTML(self,xsc,mode = None):
		return xsc.FileSize(xsc.ExpandedURL(xsc.AsString(self.content)))
handlers["filesize"] = filesize

class x(XSCElement):
	"content will be ignored: can be used to comment out stuff (e.g. linefeeds)"
	close=1

	def AsHTML(self,xsc,mode = None):
		return ""
handlers["x"] = x

class pixel(img):
	close = 0
	attr_handlers = AppendDict(img.attr_handlers,{ "color" : XSCStringAttr })
	del attr_handlers["src"]

	def AsHTML(self,xsc,mode = None):
		if not self.has_attr("color"):
			self["color"] = "dot_clear"
		self["src"] = ":Images/Pixels/" + self["color"] + ".gif"
		del self["color"]
		e = img(xsc.AsHTML(self.content,mode),xsc.AsHTML(self.attrs,mode))

		return e
handlers["pixel"] = pixel

if __name__ == "__main__":
	h = XSC(sys.argv[1])
	print str(h)

