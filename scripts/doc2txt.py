#! /usr/bin/env python
# -*- coding: Latin-1 -*-

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
Module that uses the w3m browser to generate a text version
of a docbook fragment.
Usage: python docbooklite2text.py spam.xml spam.txt
       to generate spam.txt from spam.xml
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, getopt

from ll.xist import xsc, parsers, converters
from ll.xist.ns import html, doc

def xsc2txt(infilename, outfilename, title, width):
	e = parsers.parseFile(infilename, prefixes=xsc.DocPrefixes())

	if title is None:
		title = xsc.Null
	else:
		title = doc.title(title)
	e = html.html(
		html.body(
			doc.section(title, e)
		)
	)

	e = e.conv(target="text")

	file = open(outfilename, "wb")
	file.write(e.asText(width=width))
	file.close()

if __name__ == "__main__":
	title = None
	width = 72
	(options, args) = getopt.getopt(sys.argv[1:], "t:i:w:", ["title=", "import=", "width="])

	for (option, value) in options:
		if option=="-t" or option=="--title":
			title = value
		elif option=="-i" or option=="--import":
			__import__(value)
		if option=="-w" or option=="--width":
			width = int(value)

	xsc2txt(args[0], args[1], title, width)
