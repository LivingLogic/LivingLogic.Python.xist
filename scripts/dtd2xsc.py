#! /usr/bin/env python
# -*- coding: Latin-1 -*-

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

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, keyword, os.path

from xml.parsers.xmlproc import dtdparser

from ll import url
from ll.xist import xsc, parsers

def pyify(name):
	if keyword.iskeyword(name):
		return name + "_"
	else:
		newname = []
		for c in name:
			if "a" <= c <= "z" or "A" <= c <= "Z" or "0" <= c <= "9" or c == "_":
				newname.append(c)
			else:
				newname.append("_")
		return "".join(newname)

def simplify(value):
	try:
		value = int(value)
	except ValueError:
		try:
			value = str(value)
		except UnicodeError:
			pass
	return value

def dtd2xsc(dtdfilename, outfilename=None):
	# get name of dtd without extension
	modname = os.path.splitext(os.path.split(dtdfilename)[1])[0]
	if outfilename is None:
		outfilename = modname + ".py"

	# parse dtd
	dtd = dtdparser.load_dtd(sys.argv[1])

	# write header
	file = open(outfilename, 'w')
	file.write('#! /usr/bin/env python\n\n')
	file.write('"""\n')
	file.write('"""\n\n')
	file.write('__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))\n')
	file.write('# $Source$\n\n')
	file.write('from ll.xist import xsc\n\n')

	# write elements
	elements = dtd.get_elements()
	elements.sort()
	for elemname in elements:
		pyelemname = pyify(elemname)
		file.write('class %s(xsc.Element):\n\t"""\n\t"""\n' % (pyelemname))
		if pyelemname != elemname:
			file.write('\txmlname = "%s"\n' % elemname)
		elem = dtd.get_elem(elemname)
		if elem.get_content_model() == 'empty':
			empty = "True"
		else:
			empty = "False"

		# write empty and attribute class
		file.write('\tempty = %s\n' % empty)
		attrs = elem.get_attr_list()
		if len(attrs):
			attrs.sort()
			file.write('\tclass Attrs(xsc.Element.Attrs):\n')
			for attrname in attrs:
				if u":" in attrname:
					continue # skip global attributes
				pyattrname = pyify(attrname) # get a version of the name that can be used as a Python identifier.
				attr = elem.get_attr(attrname)
				values = None
				if attr.type == "ID":
					type = "IDAttr"
				else:
					type = "TextAttr"
					if isinstance(attr.type, list):
						if len(attr.type)>1:
							values = repr(tuple([ simplify(value) for value in attr.type]))
						else:
							type = "BoolAttr"
				if attr.default is not None:
					default = repr(simplify(attr.default))
				else:
					default = None
				if attr.decl=="#REQUIRED":
					required = True
				else:
					required = None
				file.write('\t\tclass %s(xsc.%s):' % (pyattrname, type))
				if values is not None or default is not None or required is not None:
					if pyattrname != attrname:
						file.write('\n\t\t\txmlname = "%s"' % attrname)
					if values is not None:
						file.write('\n\t\t\tvalues = %s' % values)
					if default is not None:
						file.write('\n\t\t\tdefault = %s' % default)
					if required is not None:
						file.write('\n\t\t\trequired = True')
				else:
					if pyattrname != attrname:
						file.write(' xmlname = "%s"' % attrname)
					else:
						file.write(' pass')
				file.write('\n')
		file.write('\n')

	# write entities
	ents = dtd.get_general_entities()
	for entname in ents:
		if entname not in ('quot', 'apos', 'gt', 'lt', 'amp'):
			ent = parsers.parseString(dtd.resolve_ge(entname).value)
			file.write('class %s(xsc.CharRef): " "; codepoint = %d\n' % (entname, ord(unicode(ent[0])[0])))
	file.write('\n')

	# write namespace registration
	file.write("# register all the classes we've defined so far\n")
	file.write('xmlns = xsc.Namespace("%s", "... insert namespace URI ...", vars())' % (modname))
	file.close()

if __name__ == "__main__":
	dtd2xsc(*sys.argv[1:3])
