#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of Living Logic AG or
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

import sys
from xml.parsers.xmlproc import dtdparser
from xist import xsc

def dtd2xsc(dtdfilename):
	# get name of dtd without extension
	dot = dtdfilename.find('.')
	modname = dtdfilename[:dot]
	xscfilename = modname + ".py"

	# parse dtd
	dtd = dtdparser.load_dtd(sys.argv[1])

	# write header
	file = open(xscfilename, 'w')
	file.write('#! /usr/bin/env python\n\n')
	file.write('"""\n')
	file.write('"""\n\n')
	file.write('__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))\n')
	file.write('# $Source$\n\n')
	file.write('from xist import xsc\n\n')

	# write elements
	elements = dtd.get_elements()
	elements.sort()
	for elemname in elements:
		file.write('class %s(xsc.Element):\n\t"""\n\t"""\n' % (elemname))
		elem = dtd.get_elem(elemname)
		if elem.get_content_model() == 'empty':
			empty = 1
		else:
			empty = 0

		# write empty and attributes
		file.write('\tempty = %d\n' % (empty))
		attrs = elem.get_attr_list()
		if len(attrs):
			file.write('\tattrHandlers = {')
			file.write(', '.join(['"%s": xsc.TextAttr' % attrname for attrname in attrs]))
			file.write('}\n')
		file.write('\n')

	# write entities
	ents = dtd.get_general_entities()
	for entname in ents:
		if entname not in ('quot', 'apos', 'gt', 'lt', 'amp'):
			ent = xsc.xsc.parseString(dtd.resolve_ge(entname).value)
			file.write('class %s(xsc.Entity): " "; codepoint = %d\n' % (entname, ord(ent[0][0])))
	file.write('\n')

	# write namespace registration
	file.write("# register all the classes we've defined so far\n")
	file.write('namespace = xsc.Namespace("%s", "... insert URL of DTD ...", vars())' % (modname))
	file.close()

if __name__ == "__main__":
	dtd2xsc(sys.argv[1])
