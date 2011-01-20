#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
Module that uses :func:`html.astext` to generate a text version of a doc fragment.
Usage: doc2txt spam.xml spam.txt
       to generate spam.txt from spam.xml
"""


__docformat__ = "reStructuredText"


import sys, argparse

from ll.xist import xsc, parse
from ll.xist.ns import html, doc


__docformat__ = "plaintext"


def xsc2txt(infilename, outfilename, title, width):
	e = parse.tree(parse.File(infilename), parse.SGMLOP(), parse.NS(doc), parse.Node(pool=xsc.docpool()))

	if title is None:
		title = xsc.Null
	else:
		title = doc.title(title)
	e = html.html(
		html.body(
			doc.section(title, e)
		)
	)

	e = e.conv()

	with open(outfilename, "wb") as f:
		f.write(html.astext(e, width=width))


def main(args=None):
	p = argparse.ArgumentParser(description="Convert an XML file using the ll.xist.ns.doc namespace into plain text")
	p.add_argument("source", help="input XML file")
	p.add_argument("target", help="output plain text file")
	p.add_argument("-t", "--title", dest="title", help="Title for the document")
	p.add_argument("-w", "--width", dest="width", help="Width of the plain text output (default %(default)s)", type=int, default=72)

	args = p.parse_args()

	xsc2txt(args.source, args.target, args.title, args.width)


if __name__ == "__main__":
	sys.exit(main())
