#! /usr/bin/python

from xsc_specials import *

xsc = XSC("gurk.xml",0)
xsc.root = XSCplaintable(
	XSCimg(src="hurz.gif",width="%(width)d*2",height=2)+
	XSCimg(src="hurz.gif")+
#	XSCpixel(color="000000")+
#	XSCpixel(width=2,height=3)+
	XSCfilesize(href="hurz.gif")+
	XSCnbsp()
)
print html(xsc)

