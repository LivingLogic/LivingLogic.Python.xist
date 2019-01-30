#! /usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Purpose
-------

:program:`tld2xsc` is a script that converts a JSP Tag Library Descriptor XML
file into a skeleton XIST namespace module. The tld file is read from stdin and
the namespace module is printed to stdout.


Options
-------

:program:`tld2xsc` supports the following options:

.. program:: tld2xsc

.. option:: -s <value>, --shareattrs <value

	Should attributes be shared among the elements? ``none`` means that each
	element will have its own standalone :class:`Attrs` class directly derived
	from :class:`ll.xist.xsc.Elements.Attrs`. For ``dupes`` each attribute that
	is used by more than one element will be moved into its own :class:`Attrs`
	class. For ``all`` this will be done for all attributes.

.. option:: -m <model>, --model <model>

	Add model information to the namespace. ``no`` doesn't add any model
	information. ``simple`` only adds ``model = False`` or ``model = True``
	(i.e. only the information whether the element must be empty or not).
	``fullall`` adds a :mod:`ll.xist.sims` model object to each element class.
	``fullonce`` adds full model information to, but reuses model objects for
	elements which have the same model.
"""

__docformat__ = "reStructuredText"


import sys, argparse

from ll import misc, url
from ll.xist import xsc, xfind, parse
from ll.xist.ns import tld


__docformat__ = "reStructuredText"


def makexnd(stream, encoding=None, shareattrs="dupes", model="simple"):
	# :obj:`stream` can be a stream, an :class:`URL` or ``str``/``bytes``
	encoding = None
	if isinstance(stream, str):
		encoding = "utf-8"
		stream = stream.encode(encoding)
	node = parse.tree(stream, parse.Expat(encoding=encoding), parse.NS(tld), parse.Node())

	# get and convert the taglib object
	xnd = misc.first(node.walknodes(tld.taglib)).asxnd(model=model)

	if shareattrs=="dupes":
		xnd.shareattrs(False)
	elif shareattrs=="all":
		xnd.shareattrs(True)
	return xnd


def main(args=None):
	p = argparse.ArgumentParser(description="Convert JSP Tag Library Descriptor XML file (on stdin) to XIST namespace (on stdout)", epilog="For more info see http://python.livinglogic.de/XIST_scripts_tld2xsc.html")
	p.add_argument("-s", "--shareattrs", dest="shareattrs", help="Should identical attributes be shared among elements? (default %(default)s)", choices=("none", "dupes", "all"), default="dupes")
	p.add_argument("-m", "--model", dest="model", help="Add sims information to the namespace (default %(default)s)", choices=("none", "simple", "fullall", "fullonce"), default="simple")

	args = p.parse_args(args)
	print(makexnd(sys.stdin, args.shareattrs, model=args.model))


if __name__ == "__main__":
	sys.exit(main())
