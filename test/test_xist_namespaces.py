#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


from ll.xist import xsc
from ll.xist.ns import html, xml, chars, abbr, ihtml, wml, specials, htmlspecials, form, meta, svg, fo, docbook, jsp, struts_html, struts_config, tld


def test_variousnamespaces():
	def check(ns, *skip):
		for obj in vars(ns).values():
			if isinstance(obj, type) and issubclass(obj, xsc.Element) and not issubclass(obj, skip):
				node = obj()
				for attrclass in node.Attrs.declaredattrs():
					if attrclass.required:
						if attrclass.values:
							node[attrclass] = attrclass.values[0]
						else:
							node[attrclass] = "foo"
				node.conv().bytes(prefixdefault=True)
		for obj in vars(ns).values():
			if isinstance(obj, type) and issubclass(obj, xsc.Entity) and not issubclass(obj, skip):
				node = obj()
				node.conv().bytes(prefixdefault=True)
		for obj in vars(ns).values():
			if isinstance(obj, type) and issubclass(obj, xsc.ProcInst) and not issubclass(obj, skip):
				node = obj()
				node.conv().bytes(prefixdefault=True)

	yield check, html
	yield check, ihtml
	yield check, wml
	yield check, specials, specials.include, specials.filetime, specials.filesize
	yield check, form
	yield check, meta
	yield check, htmlspecials, htmlspecials.autoimg, htmlspecials.autopixel
	yield check, svg
	yield check, fo
	yield check, docbook
	yield check, jsp
	yield check, struts_html, struts_html.taglib # taglib requires a custom prefix mapping for publishing
	yield check, struts_config
	yield check, tld


def test_attributeexamples():
	assert xsc.amp.__name__ == "amp"
	assert xsc.amp.xmlname == "amp"
	assert xsc.amp.xmlns is None

	assert chars.uuml.__name__ == "uuml"
	assert chars.uuml.xmlname == "uuml"
	assert chars.uuml.xmlns is None

	assert html.a.Attrs.class_.__name__ == "class_"
	assert html.a.Attrs.class_.xmlname == "class"
	assert html.a.Attrs.class_.xmlns is None

	assert xml.Attrs.lang.__name__ == "lang"
	assert xml.Attrs.lang.xmlname == "lang"
	assert xml.Attrs.lang.xmlns == xml.xmlns
