#! /usr/bin/python

from xsc_specials import *

try:
	a = plaintable(
		img(src="hurz.gif",width="%(width)d*2",height=2)+
		img(src="hurz.gif")+
		filesize("hurz.gif")+
		nbsp()
	)
	print "XML:"
	print AsString(a)
	print "HTML:"
	print AsString(AsHTML(a))
except EHSCException,e:
	print str(e)

