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
from xist import xsc, html, publishers
from xist.URL import URL

def __forceopen(name, mode):
	try:
		return open(name, mode)
	except IOError, e:
		if e[0] != 2: # didn't work for some other reason
			raise
		found = name.rfind("/")
		if found == -1:
			raise
		os.makedirs(name[:found])
		return open(name, mode)

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

	globaloutname = URL("*/")
	encoding = None
	XHTML = None
	for (option, value) in options:
		if option=="-i" or option=="--import":
			__import__(value)
		elif option=="-o" or option=="--output":
			globaloutname = URL(value)
		elif option=="-e" or option=="--encoding":
			encoding = value
		elif option=="-x" or option=="--xhtml":
			XHTML = int(value)

	if args:
		for file in args:
			inname = URL(file)
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
			p = publishers.BytePublisher(encoding=encoding, XHTML=XHTML)
			e_out.publish(p)
			s_out = p.asBytes()
			__forceopen(outname.asString(), "wb").write(s_out)
			t4 = time.time()
			sys.stderr.write("XSC(encoding=%r, XHTML=%r): %r->%r: %s (parse %.02fs; transform %.02fs; save %.02fs)\n" % (encoding, XHTML, str(inname), str(outname), xsc._stransi("1", str(len(s_out))), t2-t1, t3-t2, t4-t3))
			xsc.xsc.popURL()
	else:
		sys.stderr.write("XSC: no files to convert.\n")

if __name__ == "__main__":
	make()
