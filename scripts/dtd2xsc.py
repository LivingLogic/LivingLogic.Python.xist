#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>Module that helps to create &xist; namespace modules from &dtd;s.
Needs <app>xmlproc</app> from the <app>PyXML</app> package.
For usage information type:</par>
<prog>
dtd2xsc --help
</prog>
"""


__version__ = "$Revision$"[11:-2]
# $Source$


import sys, os.path, optparse

from xml.parsers.xmlproc import dtdparser

from ll import url
from ll.xist import xsc, parsers, xnd


def dtd2xsc(dtdurl, outurl, verbose, xmlname, xmlurl, shareattrs, asmod, defaults):
	if verbose:
		print "Parsing DTD %s ..." % dtdurl
	d = dtdparser.load_dtd(dtdurl.url)

	if verbose:
		print "Converting ..."
	data = xnd.fromdtd(d, xmlname, xmlurl)

	if shareattrs=="dupes":
		data.shareattrs(False)
	elif shareattrs=="all":
		data.shareattrs(True)

	if verbose:
		print "Writing to %s ..." % outurl
	file = outurl.openwrite()
	file.write(data.aspy(asmod=asmod, defaults=defaults))
	file.close()


if __name__ == "__main__":
	p = optparse.OptionParser(usage="usage: %prog [options] inputurl.dtd")
	p.add_option("-o", "--output", dest="output", metavar="FILE", help="write output to FILE")
	p.add_option("-v", "--verbose", action="store_true", dest="verbose")
	p.add_option("-p", "--prefix", dest="xmlname", help="the XML prefix for this namespace", default="prefix", metavar="PREFIX")
	p.add_option("-u", "--url", dest="xmlurl", help="the XML namespace name", metavar="URL")
	p.add_option("-a", "--shareattrs", dest="shareattrs", help="Should identical attributes be shared among elements?", choices=("none", "dupes", "all"), default="dupes")
	p.add_option("-m", "--model", dest="model", default="once", help="Add sims information to the namespace", choices=("no", "all", "once"))
	p.add_option("-d", "--defaults", action="store_true", dest="defaults", help="Output default values for attributes")

	(options, args) = p.parse_args()
	if len(args) != 1:
		p.error("incorrect number of arguments")
		sys.exit(1)
	input = url.URL(args[0])
	if options.output is None:
		output = url.File(input.withExt("py").file)
	else:
		output = url.URL(options.output)
	dtd2xsc(input, output, options.verbose, options.xmlname, options.xmlurl, options.shareattrs, options.model, options.defaults)
