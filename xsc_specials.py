#! /usr/bin/python

import sys
from xsc_html40 import *

class plaintable(table):
	close = 1

	def AsHTML(self,mode = None):
		e = table(AsHTML(self.content,mode),AsHTML(self.attrs,mode))

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

	def AsHTML(self,mode = None):
		e = body(AsHTML(self.content,mode),AsHTML(self.attrs,mode))

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

	def AsHTML(self,mode = None):
		return AsHTML(["«",AsHTML(self.content,mode),"»"],mode)
handlers["z"] = z

class nbsp(XSCElement):
	close = 0

	def AsHTML(self,mode = None):
		return AsHTML("\xA0",mode)

class filesize(XSCElement):
	close=1

	def AsHTML(self,mode = None):
		return FileSize(ExpandedURL(AsString(self.content)))
handlers["filesize"] = filesize

if __name__ == "__main__":
	h = XSC(sys.argv[1])
	print str(h)

