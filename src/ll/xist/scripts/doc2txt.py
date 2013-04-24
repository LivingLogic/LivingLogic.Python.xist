#! /usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3

## Copyright 1999-2013 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2013 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
``doc2txt`` is a script that converts an XML files using XIST doc vocabulary
(i.e. the :mod:`ll.xist.ns.doc` namespace module) into plain text (by using
:func:`ll.xist.ns.html.astext`.

``doc2txt`` supports the following options:

	``-t``, ``--title``
		The title for the document

	``-w``, ``--width``
		The width of the formatted text output (default 72)

The input is read from stdin and printed to stdout.

Note that ``doc2txt`` needs an installed elinks_ browser.

	.. _elinks: http://elinks.or.cz/

Example
-------

The following generates ``spam.txt`` from ``spam.xml`` formatted to 80 columns::

	$ doc2txt <spam.xml >spam.txt -w80
"""


import sys, argparse

from ll.xist import xsc, parse
from ll.xist.ns import html, doc


__docformat__ = "reStructuredText"


def xsc2txt(instream, outstream, title, width):
	e = parse.tree(parse.Stream(instream), parse.SGMLOP(), parse.NS(doc), parse.Node(pool=xsc.docpool()))

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

	outstream.write(html.astext(e, width=width))


def main(args=None):
	p = argparse.ArgumentParser(description="Convert an XML file (on stdin) using the ll.xist.ns.doc namespace into plain text and print it (on stdout)", epilog="For more info see http://www.livinglogic.de/Python/xist/scripts/doc2txt.html")
	p.add_argument("-t", "--title", dest="title", help="Title for the document")
	p.add_argument("-w", "--width", dest="width", help="Width of the plain text output (default %(default)s)", type=int, default=72)

	args = p.parse_args()

	xsc2txt(sys.stdin, sys.stdout, args.title, args.width)


if __name__ == "__main__":
	sys.exit(main())
