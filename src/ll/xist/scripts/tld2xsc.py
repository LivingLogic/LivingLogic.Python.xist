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

from ll import misc, url
from ll.xist import xsc, xfind, parse
from ll.xist.ns import tld


__docformat__ = "reStructuredText"


def makexnd(stream, encoding=None, shareattrs="dupes", model="simple"):
	# :var:`stream` can be a stream, an :class:`URL` or a string
	node = parse.tree(stream, parse.Expat(), parse.NS(tld), parse.Node())

	# get and convert the taglib object
	xnd = node.walknodes(tld.taglib)[0].asxnd(model=model)

	if shareattrs=="dupes":
		xnd.shareattrs(False)
	elif shareattrs=="all":
		xnd.shareattrs(True)
	return xnd


def main(args=None):
	p = argparse.ArgumentParser(description="Convert JSP Tag Library Descriptor XML file (on stdin) to XIST namespace (on stdout)")
	p.add_argument("-s", "--shareattrs", dest="shareattrs", help="Should identical attributes be shared among elements? (default %(default)s)", choices=("none", "dupes", "all"), default="dupes")
	p.add_argument("-m", "--model", dest="model", help="Add sims information to the namespace (default %(default)s)", choices=("none", "simple", "fullall", "fullonce"), default="simple")
	p.add_argument("-d", "--defaults", dest="defaults", help="Output default values for attributes? (default %(default)s)", action=misc.FlagAction, default=False)

	args = p.parse_args(args)
	print makexnd(sys.stdin, args.shareattrs, model=args.model, defaults=args.defaults)


if __name__ == "__main__":
	sys.exit(main())
