#! /usr/bin/python

import sys
import xsc

class html(xsc.XSCElement):
	close = 1
xsc.XSC.handlers["html"] = html

class head(xsc.XSCElement):
	close = 1
xsc.XSC.handlers["head"] = head

class title(xsc.XSCElement):
	close = 1
xsc.XSC.handlers["title"] = title

class link(xsc.XSCElement):
	close = 0

class body(xsc.XSCElement):
	close = 1
	permitted_attrs = [ "background","bgcolor","text","link","vlink","alink","leftmargin","topmargin","marginwidth","marginheight","style","onload"]

class h1(xsc.XSCElement):
	close = 1

class h2(xsc.XSCElement):
	close = 1

class h3(xsc.XSCElement):
	close = 1

class h4(xsc.XSCElement):
	close = 1

class h5(xsc.XSCElement):
	close = 1

class h6(xsc.XSCElement):
	close = 1

class p(xsc.XSCElement):
	close = 1

class div(xsc.XSCElement):
	close = 1

class table(xsc.XSCElement):
	close = 1

class tr(xsc.XSCElement):
	close = 1

class th(xsc.XSCElement):
	close = 1

class td(xsc.XSCElement):
	close = 1

class img(xsc.XSCElement):
	close = 0
	permitted_attrs = [ "src","alt","border","width","height" ]

	def AsHTML(self,mode = None):
		e = xsc.XSCElement.AsHTML(self,mode)

		e.AddImageSizeAttributes("src")

		return e
xsc.XSC.handlers["img"] = img

class br(xsc.XSCElement):
	close = 0

class hr(xsc.XSCElement):
	close = 0

class a(xsc.XSCElement):
	close = 1
	permitted_attrs = [ "href","name" ]

	def AsHTML(self,mode = None):	
		e = XSCElement.AsHTML(self,mode)

		e.ExpandLinkAttribute("href")

		return e
xsc.XSC.handlers["a"] = a

class b(xsc.XSCElement):
	close = 1
xsc.XSC.handlers["b"] = b

if __name__ == "__main__":
	h = xsc.XSC(sys.argv[1])
	print xsc.AsString(xsc.AsHTML(h.root))

