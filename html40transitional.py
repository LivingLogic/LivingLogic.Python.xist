#! /usr/bin/python

import sys
import xsc.xsc

class html(xsc.xsc.xsc.xsc.XSCElement):
	close = 1
xsc.xsc.XSC.handlers["html"] = html

class head(xsc.xsc.XSCElement):
	close = 1
xsc.xsc.XSC.handlers["head"] = head

class title(xsc.xsc.XSCElement):
	close = 1
xsc.xsc.XSC.handlers["title"] = title

class link(xsc.xsc.XSCElement):
	close = 0

class body(xsc.xsc.XSCElement):
	close = 1
	permitted_attrs = [ "background","bgcolor","text","link","vlink","alink","leftmargin","topmargin","marginwidth","marginheight","style","onload"]

class h1(xsc.xsc.XSCElement):
	close = 1

class h2(xsc.xsc.XSCElement):
	close = 1

class h3(xsc.xsc.XSCElement):
	close = 1

class h4(xsc.xsc.XSCElement):
	close = 1

class h5(xsc.xsc.XSCElement):
	close = 1

class h6(xsc.xsc.XSCElement):
	close = 1

class p(xsc.xsc.XSCElement):
	close = 1

class div(xsc.xsc.XSCElement):
	close = 1

class table(xsc.xsc.XSCElement):
	close = 1

class tr(xsc.xsc.XSCElement):
	close = 1

class th(xsc.xsc.XSCElement):
	close = 1

class td(xsc.xsc.XSCElement):
	close = 1

class img(xsc.xsc.XSCElement):
	close = 0
	permitted_attrs = [ "src","alt","border","width","height" ]

	def AsHTML(self,mode = None):
		e = xsc.xsc.XSCElement.AsHTML(self,mode)

		e.AddImageSizeAttributes("src")

		return e
xsc.xsc.XSC.handlers["img"] = img

class br(xsc.xsc.XSCElement):
	close = 0

class hr(xsc.xsc.XSCElement):
	close = 0

class a(xsc.xsc.XSCElement):
	close = 1
	permitted_attrs = [ "href","name" ]

	def AsHTML(self,mode = None):	
		e = xsc.xsc.XSCElement.AsHTML(self,mode)

		e.ExpandLinkAttribute("href")

		return e
xsc.xsc.XSC.handlers["a"] = a

class b(xsc.xsc.XSCElement):
	close = 1
xsc.xsc.XSC.handlers["b"] = b

if __name__ == "__main__":
	h = xsc.xsc.XSC(sys.argv[1])
	print xsc.xsc.AsString(xsc.xsc.AsHTML(h.root))

