#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
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


import sys, os.path, optparse

from xml.parsers.xmlproc import dtdparser

from ll import url
from ll.xist import xsc, parsers, xnd


def dtd2xnd(dtd, xmlns=None):
	"""
	Convert &dtd; information from the &url; <arg>dtdurl</arg> to an &xist; &dom;
	using the <pyref module="ll.xist.xnd"><module>xnd</module></pyref> functionality.
	"""

	dtd = dtdparser.load_dtd_string(dtd)

	ns = xnd.Module()

	foundxmlns = set() # collects all the values of fixed xmlns attributes

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
				if attrname=="xmlns":
					if dtd_a.decl=="#FIXED":
						foundxmlns.add(dtd_a.default)
					continue # skip a namespace declaration
				elif u":" in attrname:
					continue # skip global attributes
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
			ent = parsers.parsestring(dtd.resolve_ge(entname).value)
			ns.content.append(xnd.CharRef(entname, codepoint=ord(unicode(ent[0])[0])))

	# if the DTD has exactly one value for all fixed "xmlns" attributes and the user didn't specify xmlns, use this one
	if xmlns is None and len(foundxmlns)==1:
		ns.xmlns = foundxmlns.pop()
	return ns


def stream2xnd(stream, xmlns, shareattrs):
	xnd = dtd2xnd(stream.read(), xmlns)

	if shareattrs=="dupes":
		xnd.shareattrs(False)
	elif shareattrs=="all":
		xnd.shareattrs(True)
	return xnd


def main():
	p = optparse.OptionParser(usage="usage: %prog [options] <input.dtd >output_xmlns.py")
	p.add_option("-x", "--xmlns", dest="xmlns", help="the namespace name for this module")
	p.add_option("-s", "--shareattrs", dest="shareattrs", help="Should identical attributes be shared among elements?", choices=("none", "dupes", "all"), default="dupes")
	p.add_option("-m", "--model", dest="model", default="once", help="Add sims information to the namespace", choices=("no", "all", "once"))
	p.add_option("-d", "--defaults", action="store_true", dest="defaults", help="Output default values for attributes")

	(options, args) = p.parse_args()
	if len(args) != 0:
		p.error("incorrect number of arguments")
		return 1
	print stream2xnd(sys.stdin, options.xmlns, options.shareattrs).aspy(model=options.model, defaults=options.defaults)


if __name__ == "__main__":
	sys.exit(main())
