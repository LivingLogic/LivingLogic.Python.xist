#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVING LOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVING LOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Module that helps to create XSC modules from TLDs.
Usage: python tld2xsc.py foo.tld
       to generate foo.py
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, os
from ll.xist import parsers, converters
from ll.xist.ns.tld import tld

def tld2xsc(tldfilename, outfilename=None):
	# get name of tld without extension
	modname = os.path.splitext(os.path.split(tldfilename)[1])[0]
	if outfilename is None:
		outfilename = modname + ".py"

	# parse tld file
	doc = parsers.parseFile(sys.argv[1])

	# get and convert the tablib object
	taglib = doc.find(type=tld.taglib)[0]
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
