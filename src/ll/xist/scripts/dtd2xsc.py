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


import sys, os.path, argparse, cStringIO

try:
	from xml.parsers.xmlproc import dtdparser
except ImportError:
	from xmlproc import dtdparser

from ll import misc, url
from ll.xist import xsc, parse, xnd


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


def adddtd2xnd(ns, dtd):
	"""
	Append DTD information from :var:`dtd` to the :class:`xnd.Module` object
	:var:`ns`.
	"""

	dtd = dtdparser.load_dtd_string(dtd)

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
						if len(dtd_a.type) > 1:
							values = dtd_a.type
						else:
							type = "xsc.BoolAttr"
				default = dtd_a.default
				if dtd_a.decl=="#REQUIRED":
					required = True
				else:
					required = None
				e += xnd.Attr(name=attrname, type=type, default=default, required=required, values=values)
		ns += e

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
					modelargs.append(ns.elements[(cont, xmlns)])
			if not modelargs:
				if modeltype == "sims.ElementsOrText":
					modeltype = "sims.NoElements"
				else:
					modeltype = "sims.NoElementsOrText"
		e = ns.elements[(elemname, xmlns)]
		if ns.model == "simple":
			modeltype = modeltype == "sims.Empty"
			modelargs = None
		e.modeltype = modeltype
		e.modelargs = modelargs

	# Add entities
	ents = dtd.get_general_entities()
	ents.sort()
	for entname in ents:
		if entname not in ("quot", "apos", "gt", "lt", "amp"):
			try:
				ent = parse.tree(dtd.resolve_ge(entname).value, parse.Encoder("utf-8"), parse.SGMLOP(encoding="utf-8"), parse.NS(), parse.Node())
			except xsc.IllegalEntityError:
				pass
			else:
				ns += xnd.CharRef(entname, codepoint=ord(unicode(ent[0])[0]))


def urls2xnd(urls, shareattrs=None, **kwargs):
	ns = xnd.Module(**kwargs)
	with url.Context():
		for u in urls:
			if isinstance(u, url.URL):
				u = u.openread()
			elif isinstance(u, str):
				u = cStringIO.StringIO(u)
			adddtd2xnd(ns, u.read())

	if shareattrs=="dupes":
		ns.shareattrs(False)
	elif shareattrs=="all":
		ns.shareattrs(True)
	return ns


def main(args=None):
	p = argparse.ArgumentParser(description="Convert DTDs to XIST namespace (on stdout)")
	p.add_argument("urls", metavar="urls", type=url.URL, help="ULRs of DTDs to be parsed", nargs="+")
	p.add_argument("-x", "--xmlns", dest="defaultxmlns", metavar="NAME", help="the namespace name for this module")
	p.add_argument("-s", "--shareattrs", dest="shareattrs", help="Should identical attributes be shared among elements? (default: %(default)s)", choices=("none", "dupes", "all"), default="dupes")
	p.add_argument("-m", "--model", dest="model", default="once", help="Add sims information to the namespace (default: %(default)s)", choices=("no", "simple", "fullall", "fullonce"))
	p.add_argument("-d", "--defaults", dest="defaults", help="Output default values for attributes? (default: %(default)s)", action=misc.FlagAction, default=False)
	p.add_argument(      "--duplicates", dest="duplicates", help="How to handle duplicate elements from multiple DTDs (default: %(default)s)", choices=("reject", "allow", "merge"), default="reject")

	args = p.parse_args(args)
	print urls2xnd(args.urls, **args.__dict__)


if __name__ == "__main__":
	sys.exit(main())
