#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
This modules contains stuff to be able to use XIST from
the command line as a compiler.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys
import getopt
import time

from ll import ansistyle, url

from ll.xist import xsc, publishers, presenters, converters, parsers # don't do a subpackage import here, otherwise chaos will ensue, because XIST modules will be imported twice

exts = {
	"hsc": "html",
	"shsc": "shtml",
	"phsc": "phtml",
	"xsc": "html",
	"sxsc": "shtml",
	"pxsc": "phtml",
	"xsc.de": "html.de",
	"sxsc.de": "shtml.de",
	"pxsc.de": "phtml.de",
	"xsc.en": "html.en",
	"sxsc.en": "shtml.en",
	"pxsc.en": "phtml.en",
	"jxsc": "jsp",
	"jxscp": "jspp"
}

def make(args):
	"""
	use XSC as a compiler script
	"""
	(options, args) = getopt.getopt(args, "p:i:o:e:x:m:f:r:t:s:l:", ["path=", "import=", "output=", "encoding=", "xhtml=", "mode=", "files=", "parser=", "target=", "stage=", "lang="])

	globaloutname = url.root()
	encoding = None
	xhtml = None
	mode = None
	target = None
	stage = None
	lang = None
	files = {} # handle duplicate filenames by putting all filename in a dictionary
	parsername = "sgmlop"

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
			xhtml = int(value)
		elif option=="-m" or option=="--mode":
			mode = value
		elif option=="-t" or option=="--target":
			target = value
		elif option=="-s" or option=="--stage":
			stage = value
		elif option=="-l" or option=="--lang":
			lang = value
		elif option=="-f" or option=="--files":
			for filename in open(value, "r").read().splitlines():
				if filename != "":
					files[filename] = None
		elif option=="-r" or option=="--parser":
			parsername = value

	for filename in args:
		files[filename] = None
	files = files.keys()
	files.sort()

	if files:
		for file in files:
			converter = converters.Converter(mode=mode, target=target, stage=stage, lang=lang)
			if parsername=="sgmlop":
				parser = parsers.SGMLOPParser()
			elif parsername=="expat":
				parser = parsers.ExpatParser()
			else:
				raise ValueError("parser must be 'sgmlop' or 'expat', but not %r" % parsername)
			inname = url.URL(file)
			outname = globaloutname.clone()
			if not outname.file:
				outname /= inname
			try:
				outname.ext = exts[inname.ext]
			except KeyError:
				if inname.ext.endswith("xsc"):
					outname.ext = inname.ext[:-3]
				else:
					outname.ext = "html"
			t1 = time.time()
			e_in = parsers.parseURL(inname, parser=parser, base=outname)
			t2 = time.time()
			e_out = e_in.convert(converter)
			t3 = time.time()
			p = publishers.FilePublisher(outname.openwrite(), base=outname, encoding=encoding, xhtml=xhtml)
			e_out.publish(p)
			t4 = time.time()
			size = p.tell()
			sys.stderr.write(
				"XSC(encoding=%s; xhtml=%s; parse %ss; convert %ss; save %ss; size %s bytes): %s->%s\n" %
				(presenters.strString(p.encoding), presenters.strNumber(p.xhtml),
				 presenters.strNumber("%.02f" % (t2-t1)), presenters.strNumber("%.02f" % (t3-t2)), presenters.strNumber("%.02f" % (t4-t3)),
				 presenters.strNumber(size),
				 presenters.strURL(inname), presenters.strURL(outname))
			)
	else:
		sys.stderr.write("XSC: no files to convert.\n")

if __name__ == "__main__":
	make(sys.argv[1:])
