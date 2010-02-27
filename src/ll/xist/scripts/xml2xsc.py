#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, optparse

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


def etree2xnd(sims, node):
	ns = xnd.Module()
	elements = {} # maps (name, xmlns) to (xnd.Element, content set, attrname->xnd.Attr map)
	procinsts = {} # maps name to xnd.ProcInst

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
	if sims == "none":
		pass
	elif sims == "simple":
		for entry in elements.itervalues():
			entry[0].modeltype = bool(entry[1])
	elif sims == "full":
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
		raise ValueError("unknown sims mode %r" % sims)
	return ns


def stream2xnd(stream, sims="simple", parser="etree"):
	if parser == "etree":
		from xml.etree import cElementTree
		node = cElementTree.parse(stream).getroot()
	elif parser == "lxml":
		from lxml import etree
		node = etree.parse(stream).getroot()
	else:
		raise ValueError("unknown parser %r" % parser)
	
	return etree2xnd(sims, node)


def main(args=None):
	p = optparse.OptionParser(usage="usage: %prog [options] <input.xml >output.py")
	p.add_option("-p", "--parser", dest="parser", help="parser module to use for XML parsing (etree or lxml)", choices=("etree", "lxml"), default="etree")
	choices = ["none", "simple", "full"]
	p.add_option("-s", "--sims", dest="sims", help="Create sims info? (%s)" % ", ".join(choices), metavar="MODE", default="simple")

	(options, args) = p.parse_args(args)
	if len(args) != 0:
		p.error("incorrect number of arguments")
		return 1
	print stream2xnd(sys.stdin, sims=options.sims, parser=options.parser).aspy()


if __name__ == "__main__":
	sys.exit(main())
