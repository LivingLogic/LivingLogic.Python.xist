#! /usr/bin/env python

import sys
from xsc_html40 import *

class XSCplaintable(XSCtable):
	close = 1

	def __str__(self):
		e = XSCtable(self.content,self.attrs)
		if not e.has_attr("cellpadding"):
			e["cellpadding"] = 0
		if not e.has_attr("cellspacing"):
			e["cellspacing"] = 0
		if not e.has_attr("border"):
			e["border"] = 0

		return str(e)
RegisterElement("plaintable",XSCplaintable)

class XSCplainbody(XSCbody):
	close = 1

	def __str__(self):
		e = XSCbody(self.content,self.attrs)
		if not e.has_attr("leftmargin"):
			e["leftmargin"] = 0
		if not e.has_attr("topmargin"):
			e["topmargin"] = 0
		if not e.has_attr("marginheight"):
			e["marginheight"] = 0
		if not e.has_attr("marginwidth"):
			e["marginwidth"] = 0

		return str(e)
RegisterElement("plainbody",XSCplainbody)

class XSCz(XSCElement):
	close = 1

	def __str__(self):
		return str(XSCFrag(["«" , self.content , "»" ]))
RegisterElement("z",XSCz)

class XSCnbsp(XSCElement):
	close = 0

	def __str__(self):
		return "&nbsp;"
RegisterElement("nbsp",XSCnbsp)

class XSCfilesize(XSCElement):
	close = 0
	attr_handlers = { "href" : XSCurl }

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
	attr_handlers = AppendDict(XSCimg.attr_handlers,{ "color" : XSCFrag })
	del attr_handlers["src"]

	def __str__(self):
		e = XSCimg(self.content,self.attrs - [ "color" ])
		if self.has_attr("color"):
			color = self["color"]
		else:
			color = "dot_clear"
		e["src"] = XSCFrag([":Images/Pixels/" , color , ".gif" ])

		return str(e)
RegisterElement("pixel",XSCpixel)

class XSCcap(XSCElement):
	close = 1
	
	def __str__(self):
		e = str(self.content)
		if type(e) == types.ListType:
			e = e[0]
		e = e + "?"
		result = []
		collect = ""
		innini = 0
		for i in range(len(e)):
			if (i == len(e)) or ((e[i] in string.lowercase) and (innini==0)) or ((e[i] not in string.lowercase) and (innini==1)):
				if innini==0:
					result.append(collect)
				else:
					result.append(str(XSCspan([ string.upper(collect) ],Class="nini" )))
				if i != len(e):
					collect = e[i]
				innini = 1-innini
			else:
				collect = collect + e[i]
		return string.joinfields(result,"")
RegisterElement("cap",XSCcap)

if __name__ == "__main__":
	print str(xsc_parsefile(sys.argv[1]))

