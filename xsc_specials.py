#! /usr/bin/python

import sys
import xsc
import xsc_html40transitional

class plaintable(xsc_html40transitional.table):
	close = 1

	def AsHTML(self,mode = None):
		e = xsc_html40transitional.table(xsc.AsHTML(self.content,mode),xsc.AsHTML(self.attrs,mode))

		if not e.has_attr("cellpadding"):
			e["cellpadding"] = 0
		if not e.has_attr("cellspacing"):
			e["cellspacing"] = 0
		if not e.has_attr("border"):
			e["border"] = 0

		return e
xsc.XSC.handlers["plaintable"] = plaintable

class plainbody(xsc_html40transitional.body):
	close = 1

	def AsHTML(self,mode = None):
		e = xsc_html40transitional.body(xsc.AsHTML(self.content,mode),xsc.AsHTML(self.attrs,mode))

		if not e.has_attr("leftmargin"):
			e["leftmargin"] = 0
		if not e.has_attr("topmargin"):
			e["topmargin"] = 0
		if not e.has_attr("marginheight"):
			e["marginheight"] = 0
		if not e.has_attr("marginwidth"):
			e["marginwidth"] = 0

		return e
xsc.XSC.handlers["plainbody"] = plainbody

class z(xsc.XSCElement):
	close = 1

	def AsHTML(self,mode = None):
		return xsc.AsHTML(["«",xsc.AsHTML(self.content,mode),"»"],mode)
xsc.XSC.handlers["z"] = z

class nbsp(xsc.XSCElement):
	close = 0

	def AsHTML(self,mode = None):
		return xsc.AsHTML("\xA0",mode)

class filesize(xsc.XSCElement):
	close=1

	def AsHTML(self,mode = None):
		return xsc.FileSize(xsc.ExpandedURL(xsc.AsString(self.content)))

if __name__ == "__main__":
	h = xsc.XSC(sys.argv[1])
	print xsc.AsString(xsc.AsHTML(h.root))

