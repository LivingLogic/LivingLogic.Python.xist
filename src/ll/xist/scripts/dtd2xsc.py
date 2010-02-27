#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
Module that helps to create XIST namespace modules from DTDs. Needs xmlproc__

__http://www.garshol.priv.no/download/software/xmlproc/

For usage information type::

	$ dtd2xsc --help

"""


__docformat__ = "reStructuredText"


import sys, os.path, optparse

try:
	from xml.parsers.xmlproc import dtdparser
except ImportError:
	from xmlproc import dtdparser

from ll import url
from ll.xist import xsc, parsers, xnd


__docformat__ = "reStructuredText"


def getxmlns(dtd):
	"""
	Extract the value of all fixed ``xmlns`` attributes
	"""
	found = set()
	for elemname in dtd.get_elements():
		element = dtd.get_elem(elemname)
		for attrname in element.get_attr_list():
			attr = element.get_attr(attrname)
			if attrname=="xmlns" or u":" in attrname:
				if attr.decl=="#FIXED":
					found.add(attr.default)
					continue # skip a namespace declaration
	return found


def dtd2xnd(dtd, xmlns=None):
	"""
	Convert DTD information from the URL :var:`dtdurl` to an XIST DOM using the
	:mod:`ll.xist.xnd` functionality.
	"""

	dtd = dtdparser.load_dtd_string(dtd)

	ns = xnd.Module()

	if xmlns is None:
		# try to guess the namespace name from the dtd
		xmlns = getxmlns(dtd)
		if len(xmlns) == 1:
			xmlns = iter(xmlns).next()
		else:
			xmlns = None

	# Add element info
	elements = dtd.get_elements()
	elements.sort()
	for elemname in elements:
		dtd_e = dtd.get_elem(elemname)
		e = xnd.Element(elemname, xmlns=xmlns)

		# Add attribute info for this element
		attrs = dtd_e.get_attr_list()
		if len(attrs):
			attrs.sort()
			for attrname in attrs:
				dtd_a = dtd_e.get_attr(attrname)
				if attrname=="xmlns" or u":" in attrname:
					continue # skip namespace declarations and global attributes
				values = []
				if dtd_a.type == "ID":
					type = "xsc.IDAttr"
				else:
					type = "xsc.TextAttr"
					if isinstance(dtd_a.type, list):
						if len(dtd_a.type)>1:
							values = dtd_a.type
						else:
							type = "xsc.BoolAttr"
				default = dtd_a.default
				if dtd_a.decl=="#REQUIRED":
					required = True
				else:
					required = None
				a = xnd.Attr(name=attrname, type=type, default=default, required=required)
				for v in values:
					a.values.append(v)
				e.attrs.append(a)
		ns.content.append(e)

	# Iterate through the elements a second time and add model information
	for elemname in elements:
		e = dtd.get_elem(elemname)
		model = e.get_content_model()
		if model is None:
			modeltype = "sims.Any"
			modelargs = None
		elif model == ("", [], ""):
			modeltype = "sims.Empty"
			modelargs = None
		else:
			def extractcont(model):
				if len(model) == 3:
					result = {}
					for cont in model[1]:
						result.update(extractcont(cont))
					return result
				else:
					return {model[0]: None}
			model = extractcont(model)
			modeltype = "sims.Elements"
			modelargs = []
			for cont in model:
				if cont == "#PCDATA":
					modeltype = "sims.ElementsOrText"
				elif cont == "EMPTY":
					modeltype = "sims.Empty"
				else:
					modelargs.append(ns.element(cont))
			if not modelargs:
				if modeltype == "sims.ElementsOrText":
					modeltype = "sims.NoElements"
				else:
					modeltype = "sims.NoElementsOrText"
		e = ns.element(elemname)
		e.modeltype = modeltype
		e.modelargs = modelargs

	# Add entities
	ents = dtd.get_general_entities()
	ents.sort()
	for entname in ents:
		if entname not in ("quot", "apos", "gt", "lt", "amp"):
			ent = parsers.parsestring(dtd.resolve_ge(entname).value, parser=parsers.SGMLOPParser())
			ns.content.append(xnd.CharRef(entname, codepoint=ord(unicode(ent[0])[0])))

	return ns


def stream2xnd(stream, xmlns, shareattrs):
	xnd = dtd2xnd(stream.read(), xmlns)

	if shareattrs=="dupes":
		xnd.shareattrs(False)
	elif shareattrs=="all":
		xnd.shareattrs(True)
	return xnd


def main(args=None):
	p = optparse.OptionParser(usage="usage: %prog [options] <input.dtd >output_xmlns.py")
	p.add_option("-x", "--xmlns", dest="xmlns", help="the namespace name for this module")
	p.add_option("-s", "--shareattrs", dest="shareattrs", help="Should identical attributes be shared among elements?", choices=("none", "dupes", "all"), default="dupes")
	p.add_option("-m", "--model", dest="model", default="once", help="Add sims information to the namespace", choices=("no", "all", "once"))
	p.add_option("-d", "--defaults", action="store_true", dest="defaults", help="Output default values for attributes")

	(options, args) = p.parse_args(args)
	if len(args) != 0:
		p.error("incorrect number of arguments")
		return 1
	print stream2xnd(sys.stdin, options.xmlns, options.shareattrs).aspy(model=options.model, defaults=options.defaults)


if __name__ == "__main__":
	sys.exit(main())
