#! /usr/bin/env python

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
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
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

import ansistyle

from xist import xsc, publishers, presenters, url, utils, converters, parsers # don't do a subpackage import here, otherwise chaos will ensue, because XIST modules will be imported twice

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
	(options, args) = getopt.getopt(sys.argv[1:], "p:i:o:e:x:m:f:", ["path=", "import=", "output=", "encoding=", "xhtml=", "mode=", "files="])

	globaloutname = url.URL("*/")
	encoding = None
	XHTML = None
	mode = None
	filesname = None
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
		elif option=="-f" or option=="--files":
			filesname = value

	files = []
	if filesname is not None:
		for filename in open(filesname,"r").readlines():
			filename = filename.strip()
			if filename != "":
				files.append(filename)
	files.extend(args)

	if files:
		converter = converters.Converter(mode)
		for file in files:
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
			e_in = parsers.parseFile(inname.asString())
			t2 = time.clock()
			e_out = e_in.convert(converter)
			t3 = time.clock()
			p = publishers.FilePublisher(utils.forceopen(outname.asPlainString(), "wb", 65536), base=outname, encoding=encoding, XHTML=XHTML)
			e_out.publish(p)
			t4 = time.clock()
			size = p.tell()
			sys.stderr.write(
				"XSC(encoding=%s; XHTML=%s; parse %ss; convert %ss; save %ss; size %s bytes): %s->%s\n" %
				(presenters.strString(p.encoding), presenters.strNumber(p.XHTML),
				 presenters.strNumber("%.02f" % (t2-t1)), presenters.strNumber("%.02f" % (t3-t2)), presenters.strNumber("%.02f" % (t4-t3)),
				 presenters.strNumber(size),
				 presenters.strURL(inname), presenters.strURL(outname))
			)
	else:
		sys.stderr.write("XSC: no files to convert.\n")

if __name__ == "__main__":
	make()
