#! /usr/bin/python

from xsc_specials import *

xsc = XSC()
try:
	xsc.root = plaintable(
		img(src="hurz.gif",width="%(width)d*2",height=2)+
		img(src="hurz.gif")+
		pixel(color="000000")+
		pixel(width=2,height=3)+
		filesize("hurz.gif")+
		nbsp()
	)
	print "XML:"
	print xsc.AsString()
	print "HTML:"
	print xsc.AsHTML().AsString()
except EHSCException,e:
	print str(e)

