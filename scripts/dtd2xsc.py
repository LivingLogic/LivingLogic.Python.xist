#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
Module that helps to create XSC modules from DTDs.
Needs xmlproc from the PyXML package.
Usage: python dtd2xsc.py foo.dtd
       to generate foo.py
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import sys, os.path

from xml.parsers.xmlproc import dtdparser

from ll import url
from ll.xist import xsc, parsers
from ll.xist.ns import xndl

def dtd2xsc(dtdfilename, outfilename=None):
	# get name of dtd without extension
	modname = os.path.splitext(os.path.split(dtdfilename)[1])[0]
	if outfilename is None:
		outfilename = modname + ".py"

	# parse dtd
	dtd = dtdparser.load_dtd(sys.argv[1])

	# write header
	file = open(outfilename, 'w')

	e = xndl.xndl(name=modname, url="... insert namespace URI ...")

	# write elements
	elements = dtd.get_elements()
	elements.sort()
	for elemname in elements:
		elem = dtd.get_elem(elemname)
		if elem.get_content_model() == ("", [], ""):
			empty = True
		else:
			empty = None
		e.append(xndl.element(name=elemname, empty=empty))

		attrs = elem.get_attr_list()
		if len(attrs):
			attrs.sort()
			for attrname in attrs:
				if u":" in attrname:
					continue # skip global attributes
				attr = elem.get_attr(attrname)
				values = []
				if attr.type == "ID":
					type = "IDAttr"
				else:
					type = "TextAttr"
					if isinstance(attr.type, list):
						if len(attr.type)>1:
							values = attr.type
						else:
							type = "BoolAttr"
				if attr.default is not None:
					default = attr.default
				else:
					default = None
				if attr.decl=="#REQUIRED":
					required = True
				else:
					required = None
				e[-1].append(xndl.attr(name=attrname, type=type, default=default, required=required))
				for value in values:
					e[-1][-1].append(xndl.value(value))

	# write entities
	ents = dtd.get_general_entities()
	ents.sort()
	for entname in ents:
		if entname not in ("quot", "apos", "gt", "lt", "amp"):
			ent = parsers.parseString(dtd.resolve_ge(entname).value)
			e.append(xndl.charref(name=entname, codepoint=ord(unicode(ent[0])[0])))
	data = e.asdata()
	data.shareattrs(True)
	file.write(data.aspy())
	file.close()

if __name__ == "__main__":
	dtd2xsc(*sys.argv[1:3])
