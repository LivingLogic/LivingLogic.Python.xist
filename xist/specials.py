#! /usr/bin/python

import sys
import xsc.xsc
import xsc.html40transitional

class plaintable(xsc.html40transitional.table):
	close = 1

	def AsHTML(self,mode = None):
		e = xsc.html40transitional.table(xsc.AsHTML(self.content,mode),xsc.AsHTML(self.attrs,mode))

		if not e.has_attr("cellpadding"):
			e["cellpadding"] = 0
		if not e.has_attr("cellspacing"):
			e["cellspacing"] = 0
		if not e.has_attr("border"):
			e["border"] = 0

		return e
xsc.xsc.XSC.handlers["plaintable"] = plaintable

class plainbody(xsc.html40transitional.body):
	close = 1

	def AsHTML(self,mode = None):
		e = xsc.html40transitional.body(xsc.AsHTML(self.content,mode),xsc.AsHTML(self.attrs,mode))

		if not e.has_attr("leftmargin"):
			e["leftmargin"] = 0
		if not e.has_attr("topmargin"):
			e["topmargin"] = 0
		if not e.has_attr("marginheight"):
			e["marginheight"] = 0
		if not e.has_attr("marginwidth"):
			e["marginwidth"] = 0

		return e
xsc.xsc.XSC.handlers["plainbody"] = plainbody

class z(xsc.xsc.XSCElement):
	close = 1

	def AsHTML(self,mode = None):
		return xsc.xsc.AsHTML(["«",xsc.xsc.AsHTML(self.content,mode),"»"],mode)
xsc.xsc.XSC.handlers["z"] = z

class nbsp(xsc.xsc.XSCElement):
	close = 0

	def AsHTML(self,mode = None):
		return xsc.AsHTML("\xA0",mode)

class filesize(xsc.xsc.XSCElement):
	close=1

	def AsHTML(self,mode = None):
		return xsc.xsc.FileSize(xsc.xsc.ExpandedURL(xsc.xsc.AsString(self.content)))
xsc.xsc.XSC.handlers["filesize"] = filesize

if __name__ == "__main__":
	h = xsc.xsc.XSC(sys.argv[1])
	print xsc.xsc.AsString(xsc.xsc.AsHTML(h.root))

