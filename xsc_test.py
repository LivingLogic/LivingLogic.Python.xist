#! /usr/bin/env python

from xsc_specials import *

print xsc.filename
xsc.filename = "test/gurk.xml"
print xsc.filename
x = plaintable(
	img(src=":hurz.gif",width="%(width)d*2",height=2)+
	img(src="hurz.gif")+
#	pixel(color="000000")+
#	pixel(width=2,height=3)+
	filesize(href="hurz.gif")+
	nbsp()
)
print str(x)

x = xsc.parsestring("<img src=':hurz.gif'/>")

print str(x)
