#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
Module that helps to create XSC modules from TLDs.
Usage: python tld2xsc.py foo.tld
       to generate foo.py
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, os

from ll.xist import xsc, parsers, converters
from ll.xist.ns import tld

def tld2xsc(tldfilename, outfilename=None):
	# get name of tld without extension
	modname = os.path.splitext(os.path.split(tldfilename)[1])[0]
	if outfilename is None:
		outfilename = modname + ".py"

	# parse tld file
	doc = parsers.parseFile(sys.argv[1])

	# get and convert the tablib object
	taglib = doc.findfirst(xsc.FindType(tld.taglib))
	e = taglib.conv()
	s = e.asdata().aspy()

	file = open(outfilename, 'w')
	file.write(s)
	file.close()

if __name__ == "__main__":
	if len(sys.argv)<2 or len(sys.argv)>3:
		print "Usage: tld2xsc.py file.tld [file.py]"
		sys.exit(0)
	tld2xsc(*sys.argv[1:3])
