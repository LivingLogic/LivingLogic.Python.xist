#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
This module contains functions that help converting &dtd;s to
<pyref module="ll.xist.ns.xndl"><module>xndl</module></pyref>
information or &xist; namespaces
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import sys, os.path

from ll import url
from ll.xist import xsc, parsers
from ll.xist.ns import xndl

def dtd2xndl(dtd, xmlname, xmlurl=None, skipxmlns=True):
	"""
	Convert &dtd; information (in the format that is returned by <app>xmlproc</app>s
	<function>dtdparser.load_dtd</function> function) to an &xist; DOM using the
	<pyref module="ll.xist.ns.xndl"><module>xndl</module></pyref> namespace.
	"""

	node = xndl.xndl(name=xmlname, url=xmlurl)

	xmlns = {}

	# Add element info
	elements = dtd.get_elements()
	elements.sort()
	for elemname in elements:
		elem = dtd.get_elem(elemname)
		if elem.get_content_model() == ("", [], ""):
			empty = True
		else:
			empty = None
		node.append(xndl.element(name=elemname, empty=empty))

		# Add attribute info for this element
		attrs = elem.get_attr_list()
		if len(attrs):
			attrs.sort()
			for attrname in attrs:
				attr = elem.get_attr(attrname)
				if attrname=="xmlns":
					if attr.decl=="#FIXED":
						xmlns[attr.default] = None
					if skipxmlns:
						continue # skip a namespace declaration
				elif u":" in attrname:
					continue # skip global attributes
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
				node[-1].append(xndl.attr(name=attrname, type=type, default=default, required=required))
				for value in values:
					node[-1][-1].append(xndl.value(value))

	# Add entities
	ents = dtd.get_general_entities()
	ents.sort()
	for entname in ents:
		if entname not in ("quot", "apos", "gt", "lt", "amp"):
			ent = parsers.parseString(dtd.resolve_ge(entname).value)
			node.append(xndl.charref(name=entname, codepoint=ord(unicode(ent[0])[0])))

	# if the DTD has exactly one value for all fixed "xmlns" attributes and the user didn't specify an xmlurl, use this one
	if xmlurl is None:
		if len(xmlns)==1:
			node["url"] = xmlns.popitem()[0]
		else:
			node["url"] = "... insert namespace name ..."
	return node

def dtd2data(dtd, xmlname, xmlurl=None, skipxmlns=True):
	return dtd2xndl(dtd, xmlname, xmlurl, skipxmlns).asdata()

