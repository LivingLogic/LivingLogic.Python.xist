#! /usr/bin/env python

## Copyright 2000 by Living Logic AG, Bayreuth, Germany.
## Copyright 2000 by Walter Dörwald
##
## See the file LICENSE for licensing details

"""
This modules contains stuff to be able to use XIST from
the command line as a compiler.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import sys
import getopt
import time
import xsc, html, publishers, url, utils

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

def make():
	"""
	use XSC as a compiler script, i.e. read an input file from args[1]
	and writes it to args[2]
	"""

	(options, args) = getopt.getopt(sys.argv[1:], "i:o:e:x:", ["import=", "output=", "encoding=", "xhtml="])

	globaloutname = url.URL("*/")
	encoding = None
	XHTML = None
	for (option, value) in options:
		if option=="-i" or option=="--import":
			__import__(value)
		elif option=="-o" or option=="--output":
			globaloutname = url.URL(value)
		elif option=="-e" or option=="--encoding":
			encoding = value
		elif option=="-x" or option=="--xhtml":
			XHTML = int(value)

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
			t1 = time.time()
			e_in = xsc.xsc.parse(inname)
			t2 = time.time()
			xsc.xsc.pushURL(inname)
			e_out = e_in.asHTML()
			t3 = time.time()
			p = publishers.FilePublisher(utils.forceopen(outname.asString(), "wb"), encoding=encoding, XHTML=XHTML)
			e_out.publish(p)
			t4 = time.time()
			size = p.tell()
			sys.stderr.write("XSC(encoding=%s, XHTML=%s): %s->%s: %s (parse %ss; transform %ss; save %ss)\n" % (xsc._stransi("1", encoding), xsc._stransi("1", str(XHTML)), xsc.strURL(str(inname)), xsc.strURL(str(outname)), xsc._stransi("1", str(size)), xsc._stransi("1", "%.02f" % (t2-t1)), xsc._stransi("1", "%.02f" % (t3-t2)), xsc._stransi("1", "%.02f" % (t4-t3))))
			xsc.xsc.popURL()
	else:
		sys.stderr.write("XSC: no files to convert.\n")

if __name__ == "__main__":
	make()
