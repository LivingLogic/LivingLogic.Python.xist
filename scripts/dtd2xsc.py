#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVING LOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVING LOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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

import optik

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

	e = xndl.xndl(prefix=modname, name="... insert namespace URI ...")
	
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
	file.write(e.aspy())
	file.close()

if __name__ == "__main__":
	dtd2xsc(*sys.argv[1:3])
