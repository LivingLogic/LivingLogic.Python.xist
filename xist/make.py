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
from xist import xsc, html, publishers, url, utils # don't do a subpackage import here, otherwise chaos will ensue, because XIST modules will be imported twice

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

def formatstring(string):
	return xsc._stransi(["1", "32"], string)

def formatnumber(number):
	return xsc._stransi(["1", "35"], str(number))

def make():
	"""
	use XSC as a compiler script, i.e. read an input file from args[1]
	and writes it to args[2]
	"""
	(options, args) = getopt.getopt(sys.argv[1:], "p:i:o:e:x:", ["path=", "import=", "output=", "encoding=", "xhtml="])

	globaloutname = url.URL("*/")
	encoding = None
	XHTML = None
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
			p = publishers.FilePublisher(utils.forceopen(outname.asPlainString(), "wb"), encoding=encoding, XHTML=XHTML)
			e_out.publish(p)
			t4 = time.time()
			size = p.tell()
			sys.stderr.write("XSC(encoding=%s, XHTML=%s): %s->%s: %s (parse %ss; transform %ss; save %ss)\n" % (formatstring(p.encoding), formatnumber(p.XHTML), xsc.strURL(inname.asString()), xsc.strURL(outname.asString()), formatnumber(size), formatnumber("%.02f" % (t2-t1)), formatnumber("%.02f" % (t3-t2)), formatnumber("%.02f" % (t4-t3))))
			xsc.xsc.popURL()
	else:
		sys.stderr.write("XSC: no files to convert.\n")

if __name__ == "__main__":
	make()
