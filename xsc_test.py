#! /usr/bin/env python

from xsc_specials import *

print xsc_filename
xsc_filename = "test/gurk.xml"
print xsc_filename
x = XSCplaintable(
	XSCimg(src=":hurz.gif",width="%(width)d*2",height=2)+
	XSCimg(src="hurz.gif")+
#	XSCpixel(color="000000")+
#	XSCpixel(width=2,height=3)+
	XSCfilesize(href="hurz.gif")+
	XSCnbsp()
)
print str(x)

x = xsc_parsestring("<img src=':hurz.gif'/>")

print str(x)
