#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, argparse

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
	return (name, xmlns)


def etree2xnd(model, node):
	ns = xnd.Module()
	elements = {} # maps (name, xmlns) to (xnd.Element, content set, attrname->xnd.Attr map)
	procinsts = {} # maps name to xnd.ProcInst

	# Iterate through the tree a collect: which elements are encountered and how they are nested
	for path in iterpath(node):
		node = path[-1]
		if "Element" in type(node).__name__:
			(name, xmlns) = getelementname(node)
			try:
				entry = elements[(name, xmlns)]
			except KeyError:
				xndnode = xnd.Element(name, xmlns=xmlns)
				entry = elements[(name, xmlns)] = (xndnode, set(), {})
				ns(xndnode)
			else:
				xndnode = entry[0]
			for attrname in node.keys():
				if not attrname.startswith("{") and attrname not in entry[2]:
					attr = xnd.Attr(attrname, type=xsc.TextAttr)
					entry[0](attr)
					entry[2][attrname] = attr
		elif "ProcessingInstruction" in type(node).__name__:
			name = node.target
			try:
				xndnode = procinsts[name]
			except KeyError:
				procinst = xnd.ProcInst(name)
				procinsts[name] = procinst
				xndnode = procinst
			ns(xndnode)
		elif "Comment" in type(node).__name__:
			xndnode = "#comment"
		elif isinstance(node, basestring):
			if node.isspace():
				xndnode = "#whitespace"
			else:
				xndnode = "#text"
		if len(path) >= 2:
			parent = path[-2]
			if "Element" in type(parent).__name__:
				parententry = elements[getelementname(parent)]
				parententry[1].add(xndnode)

	# Put sims info into the element definitions
	if model == "none":
		pass
	elif model == "simple":
		for entry in elements.itervalues():
			entry[0].modeltype = bool(entry[1])
	elif model == "full":
		for entry in elements.itervalues():
			if not entry[1]:
				entry[0].modeltype = "sims.Empty"
			else:
				elements = [el for el in entry[1] if isinstance(el, xnd.Element)]
				if not elements:
					if "#text" in entry[1]:
						entry[0].modeltype = "sims.NoElements"
					else:
						entry[0].modeltype = "sims.NoElementsOrText"
				else:
					if "#text" in entry[1]:
						entry[0].modeltype = "sims.ElementsOrText"
					else:
						entry[0].modeltype = "sims.Elements"
					entry[0].modelargs = elements
	else:
		raise ValueError("unknown sims mode {!r}".format(model))
	return ns


def stream2xnd(stream, model="simple", parser="etree"):
	if parser == "etree":
		from xml.etree import cElementTree
		node = cElementTree.parse(stream).getroot()
	elif parser == "lxml":
		from lxml import etree
		node = etree.parse(stream).getroot()
	else:
		raise ValueError("unknown parser {!r}".format(parser))

	return etree2xnd(model, node)


def main(args=None):
	p = argparse.ArgumentParser(description="Convert XML (on stdin) to XIST namespace (on stdout)")
	p.add_argument("-p", "--parser", dest="parser", help="parser module to use for XML parsing (etree or lxml)", choices=("etree", "lxml"), default="etree")
	p.add_argument("-m", "--model", dest="model", help="Create sims info?", choices=("none", "simple", "full"), default="simple")

	args = p.parse_args(args)
	print stream2xnd(sys.stdin, model=args.model, parser=args.parser).aspy()


if __name__ == "__main__":
	sys.exit(main())
