#!/usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
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

import sys, os, getopt

from xist import xsc, parsers
from xist.ns import html, docbooklite as dbl

def dookbooklite2text(infilename, outfilename, title):
	e = parsers.parseFile(infilename, namespaces=xsc.Namespaces(dbl))

	if title is None:
		title = xsc.Null
	else:
		title = dbl.title(title)
	e = html.html(
		html.body(
			dbl.section(title, e)
		)
	)

	e = e.convert()

	(stdin, stdout) = os.popen2("w3m -T text/html -dump >%s" % outfilename)

	stdin.write(e.asBytes())
	stdin.close()
	stdout.close()

if __name__ == "__main__":
	title = None
	(options, args) = getopt.getopt(sys.argv[1:], "t:", ["title="])

	for (option, value) in options:
		if option=="-t" or option=="--title":
			title = value

	dookbooklite2text(args[0], args[1], title)
