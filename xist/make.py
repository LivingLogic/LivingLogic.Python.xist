#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of Living Logic AG or
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
This modules contains stuff to be able to use XIST from
the command line as a compiler.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys
import getopt
import time
from xist import xsc, html, publishers, url, utils, color # don't do a subpackage import here, otherwise chaos will ensue, because XIST modules will be imported twice

def extXSC2HTML(ext):
	try:
		return {"hsc": "html", "shsc": "shtml", "phsc": "phtml", "xsc": "html", "sxsc": "shtml", "pxsc": "phtml"}[ext]
	except KeyError:
		return ext

def extHTML2XSC(ext):
	try:
		return {"html": "hsc", "shtml": "shsc", "phtml": "phsc"}[ext]
	except KeyError:
		return ext

class ColoredString(color.Text):
	color = 0x2

class ColoredNumber(color.Text):
	color = 0x5

	def __init__(self, number):
		color.Text.__init__(self, str(number))

class ColoredURL(color.Text):
	color = 0x4

	def __init__(self, url):
		color.Text.__init__(self, url.asString())

def make():
	"""
	use XSC as a compiler script, i.e. read an input file from args[1]
	and writes it to args[2]
	"""
	(options, args) = getopt.getopt(sys.argv[1:], "p:i:o:e:x:m:", ["path=", "import=", "output=", "encoding=", "xhtml=", "mode="])

	globaloutname = url.URL("*/")
	encoding = None
	XHTML = None
	mode = None
	for (option, value) in options:
		if option=="-p" or option=="--path":
			sys.path.append(value)
		elif option=="-i" or option=="--import":
			__import__(value)
		elif option=="-o" or option=="--output":
			globaloutname = url.URL(value)
		elif option=="-e" or option=="--encoding":
			encoding = value
		elif option=="-x" or option=="--xhtml":
			XHTML = int(value)
		elif option=="-m" or option=="--mode":
			mode = value

	if args:
		for file in args:
			inname = url.URL(file)
			outname = globaloutname.clone()
			if not outname.file:
				outname += inname
			if not outname.file:
				outname.file = "noname"
			try:
				outname.ext = {"hsc": "html", "shsc": "shtml", "phsc": "phtml", "xsc": "html", "sxsc": "shtml", "pxsc": "phtml"}[inname.ext]
			except KeyError:
				outname.ext = "html"
			t1 = time.clock()
			e_in = xsc.xsc.parse(inname)
			t2 = time.clock()
			xsc.xsc.pushURL(inname)
			e_out = e_in.asHTML(mode)
			t3 = time.clock()
			p = publishers.FilePublisher(utils.forceopen(outname.asPlainString(), "wb", 65536), encoding=encoding, XHTML=XHTML)
			e_out.publish(p)
			t4 = time.clock()
			size = p.tell()
			sys.stderr.write("XSC(encoding=%s, XHTML=%s): %s->%s: %s (parse %ss; transform %ss; save %ss)\n" % (ColoredString(p.encoding), ColoredNumber(p.XHTML), ColoredURL(inname), ColoredURL(outname), ColoredNumber(size), ColoredNumber("%.02f" % (t2-t1)), ColoredNumber("%.02f" % (t3-t2)), ColoredNumber("%.02f" % (t4-t3))))
			xsc.xsc.popURL()
	else:
		sys.stderr.write("XSC: no files to convert.\n")

if __name__ == "__main__":
	make()
