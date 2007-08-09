#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
Module that uses the w3m browser to generate a text version
of a doc fragment.
Usage: python doc2txt.py spam.xml spam.txt
       to generate spam.txt from spam.xml
"""


import sys, getopt

from ll.xist import xsc, parsers, converters
from ll.xist.ns import html, doc, text


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

	e = e.conv(target=text)

	file = open(outfilename, "wb")
	file.write(html.astext(e, width=width))
	file.close()


def main():
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


if __name__ == "__main__":
	sys.exit(main())
