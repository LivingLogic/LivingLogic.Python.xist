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

import ansistyle, url

from xist import xsc, publishers, presenters, converters, parsers # don't do a subpackage import here, otherwise chaos will ensue, because XIST modules will be imported twice

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
	(options, args) = getopt.getopt(args, "p:i:o:e:x:m:f:r:n:t:s:l:", ["path=", "import=", "output=", "encoding=", "xhtml=", "mode=", "files=", "parser=", "namespace=", "target=", "stage=", "lang="])

	globaloutname = url.root()
	encoding = None
	xhtml = None
	mode = None
	target = None
	stage = None
	lang = None
	files = {} # handle duplicate filenames by putting all filename in a dictionary
	parsername = "sgmlop"
	namespaces = xsc.Namespaces()

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
		elif option=="-n" or option=="--namespace":
			namespaces.pushNamespace(xsc.namespaceRegistry.byPrefix[value.strip()])

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
			outname.ext = exts.get(inname.ext, "html")
			t1 = time.time()
			e_in = parsers.parseURL(inname, parser=parser, namespaces=namespaces, base=outname)
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
