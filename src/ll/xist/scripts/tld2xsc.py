#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
Module that helps to create XIST namespace modules from TLD files (Java tag
library descriptors).

For usage information type::

	$ tld2xsc --help
"""

__docformat__ = "reStructuredText"


import sys, optparse

from ll import url
from ll.xist import xsc, xfind, parsers, converters
from ll.xist.ns import tld


__docformat__ = "reStructuredText"


def tld2xnd(stream, shareattrs=None):
	node = parsers.parsestream(stream, prefixes={None: tld})

	# get and convert the taglib object
	xnd = node.walknode(tld.taglib)[0].asxnd()

	if shareattrs=="dupes":
		xnd.shareattrs(False)
	elif shareattrs=="all":
		xnd.shareattrs(True)
	return xnd


def main(args=None):
	p = optparse.OptionParser(usage="usage: %prog [options] <input.tld >output_xmlns.py")
	p.add_option("-s", "--shareattrs", dest="shareattrs", help="Should identical attributes be shared among elements?", choices=("none", "dupes", "all"), default="dupes")
	p.add_option("-m", "--model", dest="model", default="once", help="Add sims information to the namespace", choices=("no", "all", "once"))
	p.add_option("-d", "--defaults", action="store_true", dest="defaults", help="Output default values for attributes")

	(options, args) = p.parse_args(args)
	if len(args) != 0:
		p.error("incorrect number of arguments")
		return 1
	print tld2xnd(sys.stdin, options.shareattrs).aspy(model=options.model, defaults=options.defaults)


if __name__ == "__main__":
	sys.exit(main())
