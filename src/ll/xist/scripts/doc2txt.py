#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
Module that uses the w3m browser to generate a text version
of a doc fragment.
Usage: python doc2txt.py spam.xml spam.txt
       to generate spam.txt from spam.xml
"""


__docformat__ = "reStructuredText"


import sys, getopt

from ll.xist import xsc, parsers, converters
from ll.xist.ns import html, doc, text


__docformat__ = "plaintext"


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


def main(args=None):
	if args is None:
		args = sys.argv[1:]
	title = None
	width = 72
	(options, args) = getopt.getopt(args, "t:i:w:", ["title=", "import=", "width="])

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
