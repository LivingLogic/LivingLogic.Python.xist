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


import sys, argparse

from ll import url
from ll.xist import xsc, xfind, parse
from ll.xist.ns import tld


__docformat__ = "reStructuredText"


def tld2xnd(stream, shareattrs=None):
	node = parse.tree(parse.Stream(stream), parse.Expat(), parse.NS(tld), parse.Node())

	# get and convert the taglib object
	xnd = node.walknodes(tld.taglib)[0].asxnd()

	if shareattrs=="dupes":
		xnd.shareattrs(False)
	elif shareattrs=="all":
		xnd.shareattrs(True)
	return xnd


def main(args=None):
	p = argparse.ArgumentParser(description="Convert JSP Tag Library Descriptor XML file (on stdin) to XIST namespace (on stdout)")
	p.add_argument("-s", "--shareattrs", dest="shareattrs", help="Should identical attributes be shared among elements?", choices=("none", "dupes", "all"), default="dupes")
	p.add_argument("-m", "--model", dest="model", help="Add sims information to the namespace", choices=("no", "all", "once"), default="once")
	p.add_argument("-d", "--defaults", dest="defaults", action="store_true", help="Output default values for attributes?")

	args = p.parse_args(args)
	print tld2xnd(sys.stdin, args.shareattrs).aspy(model=args.model, defaults=args.defaults)


if __name__ == "__main__":
	sys.exit(main())
