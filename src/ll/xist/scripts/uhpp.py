#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2007-2014 by LivingLogic AG, Bayreuth/Germany
## Copyright 2007-2014 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
-------

``uhpp`` is a script for pretty printing HTML files. It is URL-enabled, so you
can specify local file names and URLs (and remote files via ``ssh`` URLs).


Options
-------

``uhpp`` supports the following options:

	``urls``
		Zero or more URLs to be printed. If no URL is given, stdin is read.

	``-v``, ``--verbose`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Output parse warnings?

	``-c``, ``--compact`` : ``false``, ``no``, ``0``, ``true``, ``yes`` or ``1``
		Compact HTML before printing (i.e. remove whitespace nodes)?


Examples
--------

Pretty print stdin::

	$ cat foo.html | uhpp

Pretty print a local HTML file::

	$ uhpp foo.html

Pretty print a remote HTML file::

	$ uhpp ssh://user@www.example.org/~/foo.html
"""


import sys, argparse

from ll import misc, url
from ll.xist import xsc, parse
from ll.xist.ns import xml, html

__docformat__ = "reStructuredText"


def main(args=None):
	def printone(u):
		source = parse.URL(u) if isinstance(u, url.URL) else parse.Stream(u)
		node = parse.tree(source, parse.Tidy(), parse.NS(html), parse.Node(base="", pool=xsc.Pool(html, xml)))
		if args.compact:
			node = node.normalized().compacted()
		node = node.pretty()
		print(node.string(encoding=sys.stdout.encoding))

	p = argparse.ArgumentParser(description="pretty print HTML files", epilog="For more info see http://www.livinglogic.de/Python/xist/scripts/uhpp.html")
	p.add_argument("urls", metavar="url", help="URLs to be pretty printed", nargs="*", type=url.URL)
	p.add_argument("-v", "--verbose", dest="verbose", help="Ouput parse warnings?", action=misc.FlagAction, default=False)
	p.add_argument("-c", "--compact", dest="compact", help="Compact HTML before pretty printing (default: %(default)s)", action=misc.FlagAction, default=False)

	args = p.parse_args(args)
	if not args.verbose:
		import warnings
		warnings.simplefilter("ignore", category=xsc.Warning)
	with url.Context():
		if args.urls:
			for u in args.urls:
				printone(u)
		else:
			printone(sys.stdin.buffer)


if __name__ == "__main__":
	sys.exit(main())
