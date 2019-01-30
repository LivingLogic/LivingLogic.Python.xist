#!/usr/bin/env python
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

:program:`xml2xsc` is a script that generates an XIST namespace module from one
or more XML files. :program:`xml2xsc` will output an XIST element class for each
element it encounters in any of the XML files. The attributes and model
information :program:`xml2xsc` assigns to an element will be collected from each
occurrence of the element in the XML files, so the XML files should cover as
many different cases as possible.


Options
-------

:program:`xml2xsc` supports the following options:

.. program:: xml2xsc

.. option:: urls

	Zero or more URLs (or filenames) of XML files to be parsed. If no URL is
	given stdin will be read.

.. option:: -p <parser>, --parser <parser>

	Which XML parser should be used from parsing the XML files? (``etree`` is
	the default, ``lxml`` requires that lxml_ is installed)

.. option:: -s <mode>, --shareattrs <mode>

	Should attributes be shared among the elements? ``none`` means that each
	element will have its own standalone :class:`Attrs` class directly derived
	from :class:`ll.xist.xsc.Elements.Attrs`. For ``dupes`` each attribute that
	is used by more than one element will be moved into its own :class:`Attrs`
	class. For ``all`` this will be done for all attributes.

.. option:: -m <mode>, --model <mode>

	Add model information to the namespace. ``no`` doesn't add any model
	information. ``simple`` only adds ``model = False`` or ``model = True``
	(i.e. only the information whether the element must be empty or not).
	``fullall`` adds a :mod:`ll.xist.sims` model object to each element class.
	``fullonce`` adds full model information to, but reuses model objects for
	elements which have the same model.

.. option:: -x <name>, --defaultxmlns <name>

	The default namespace name. All elements that don't belong to any
	namespace will be assigned to this namespace.

.. _lxml: http://lxml.de/


Example
-------

Suppose we have the following XML file (named :file:`foo.xml`):

.. sourcecode:: xml

	<x a="0"><x b="1"/><y/></x>

Then we can generate a skeleton XIST namespace from it with the following command:

.. sourcecode:: bash

	xml2xsc foo.xml -xhttp://xmlns.example.org/ -mfullonce

The output will be:

.. sourcecode:: python

	# -*- coding: ascii -*-

	from ll.xist import xsc, sims

	xmlns = 'http://xmlns.example.org/'

	class x(xsc.Element):
		xmlns = xmlns
		class Attrs(xsc.Element.Attrs):
			class a(xsc.TextAttr): pass
			class b(xsc.TextAttr): pass

	class y(xsc.Element): xmlns = xmlns

	x.model = sims.Elements(y, x)
	y.model = sims.Empty()
"""


import sys, argparse, io

from ll import misc, url
from ll.xist import xsc, xnd, sims


__docformat__ = "reStructuredText"


def iterpath(node):
	yield [node]
	if hasattr(node, "text") and node.text:
		yield [node, node.text]
	if hasattr(node, "getchildren"):
		for child in node:
			for path in iterpath(child):
				yield [node] + path
	if hasattr(node, "tail") and node.tail:
		yield [node, node.tail]


def getelementname(node):
	xmlns = None
	name = node.tag
	if name.startswith("{"):
		(xmlns, sep, name) = name[1:].partition("}")
	return (xmlns, name)


def addetree2xnd(ns, node, elements):
	# Iterate through the tree and collect which elements are encountered and how they are nested
	for path in iterpath(node):
		node = path[-1]
		if "Element" in type(node).__name__:
			(xmlns, name) = getelementname(node)
			if (xmlns, name) in ns.elements:
				xndnode = ns.elements[(xmlns, name)]
			else:
				xndnode = xnd.Element(xmlns, name)
				ns += xndnode
				elements[(xmlns, name)] = set()
			for attrname in node.keys():
				if not attrname.startswith("{") and attrname not in xndnode.attrs:
					xndnode += xnd.Attr(attrname, type=xsc.TextAttr)
		elif "ProcessingInstruction" in type(node).__name__:
			name = node.target
			if name not in ns.procinsts:
				ns += xnd.ProcInst(name)
		elif "Comment" in type(node).__name__:
			xndnode = "#comment"
		elif isinstance(node, str):
			if node.isspace():
				xndnode = "#whitespace"
			else:
				xndnode = "#text"
		if len(path) >= 2:
			parent = path[-2]
			if "Element" in type(parent).__name__:
				parententry = elements[getelementname(parent)]
				parententry.add(xndnode)


def makexnd(urls, parser="etree", shareattrs="dupes", model="simple", defaultxmlns=None):
	elements = {} # maps (name, xmlns) to content set
	ns = xnd.Module(defaultxmlns=defaultxmlns, model=model)
	with url.Context():
		if not urls:
			urls = [sys.stdin]
		for u in urls:
			if isinstance(u, url.URL):
				u = u.openread()
			elif isinstance(u, str):
				u = io.BytesIO(u.encode("utf-8"))
			elif isinstance(u, bytes):
				u = io.BytesIO(u)
			if parser == "etree":
				from xml.etree import cElementTree
				node = cElementTree.parse(u).getroot()
			elif parser == "lxml":
				from lxml import etree
				node = etree.parse(u).getroot()
			else:
				raise ValueError(f"unknown parser {parser!r}")
			addetree2xnd(ns, node, elements)

	# Put sims info into the element definitions
	if model == "none":
		pass
	elif model == "simple":
		for (fullname, modelset) in elements.items():
			ns.elements[fullname].modeltype = bool(modelset)
	elif model in ("fullall", "fullonce"):
		for (fullname, modelset) in elements.items():
			element = ns.elements[fullname]
			if not modelset:
				element.modeltype = "sims.Empty"
			else:
				elements = [el for el in modelset if isinstance(el, xnd.Element)]
				if not elements:
					if "#text" in modelset:
						element.modeltype = "sims.NoElements"
					else:
						element.modeltype = "sims.NoElementsOrText"
				else:
					if "#text" in modelset:
						element.modeltype = "sims.ElementsOrText"
					else:
						element.modeltype = "sims.Elements"
					element.modelargs = elements
	else:
		raise ValueError(f"unknown sims mode {model!r}")

	if shareattrs=="dupes":
		ns.shareattrs(False)
	elif shareattrs=="all":
		ns.shareattrs(True)
	return ns


def main(args=None):
	p = argparse.ArgumentParser(description="Convert XML files to XIST namespace (on stdout)", epilog="For more info see http://python.livinglogic.de/XIST_scripts_xml2xsc.html")
	p.add_argument("urls", metavar="urls", type=url.URL, help="URLs of XML files to be parsed (default stdin)", nargs="*")
	p.add_argument("-p", "--parser", dest="parser", help="parser module to use for XML parsing (default: %(default)s)", choices=("etree", "lxml"), default="etree")
	p.add_argument("-s", "--shareattrs", dest="shareattrs", help="Should identical attributes be shared among elements? (default: %(default)s)", choices=("none", "dupes", "all"), default="dupes")
	p.add_argument("-m", "--model", dest="model", help="Create sims info? (default: %(default)s)", choices=("none", "simple", "fullall", "fullonce"), default="simple")
	p.add_argument("-x", "--defaultxmlns", dest="defaultxmlns", metavar="NAME", help="Force elements without a namespace into this namespace")

	args = p.parse_args(args)
	print(makexnd(**args.__dict__))


if __name__ == "__main__":
	sys.exit(main())
