#! /usr/bin/env python

"""
Module that helps to create XSC modules from DTDs
Needs xmlproc from the pyxml package
Usage: python dtd2xsc.py wml13.dtd
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xml.parsers.xmlproc import xmldtd_own
import sys

if __name__ == '__main__':
	# get name of dtd without extension
	mod_name = sys.argv[1]
	dot = mod_name.find('.')
	mod_name = mod_name[:dot]
	# create text for intro lines
	intro = '#! /usr/bin/env python\n\n"""\n\n"""\n\n'
	intro += '__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))\n'
	intro += '# $Source$\n\n' % (mod_name)
	intro += 'import string\nimport xsc\n\n'
	file = open(mod_name + '.py', 'w')
	file.write(intro)
	# parse dtd
	dtd = xmldtd_own.load_dtd(sys.argv[1])
	# write elements
	elements = dtd.get_elements()
	elements.sort()
	for elemname in elements:
		file.write('class %s(xsc.Element):\n    """\n\n    """\n' % (elemname))
		elem = dtd.get_elem(elemname)
		if elem.get_content_model() == 'empty':
			empty = 1
		else:
			empty = 0
		# write attributes
		file.write('    empty = %s\n    attrHandlers = {' % (empty))
		attrs = ''
		for attrname in elem.get_attr_list():
			attrs += '"%s": xsc.TextAttr, ' % (attrname)
		attrs = attrs[:-2]
		file.write(attrs)
		file.write('}\n\n')
	# write preparation for entities
	ents = dtd.get_general_entities()
	for entname in ents:
		ent=xsc.xsc.parseString(dtd.resolve_ge(entname).value)
		file.write('class %s(xsc.Entity): " "; codepoint = %d\n' % (entname, ord(ent[0][0])))
	file.write('\n')
	# write namespace registration
	file.write('# register all the classes we\'ve defined so far\n')
	file.write('namespace = xsc.Namespace(%r, "... insert URL of DTD ...", vars())' % (mod_name))
	file.close()
