#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
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

	check(html)
	check(ihtml)
	check(wml)
	check(specials, specials.include, specials.filetime, specials.filesize)
	check(form)
	check(meta)
	check(htmlspecials, htmlspecials.autoimg, htmlspecials.autopixel)
	check(svg)
	check(fo)
	check(docbook)
	check(jsp)
	check(struts_html, struts_html.taglib) # taglib requires a custom prefix mapping for publishing
	check(struts_config)
	check(tld)


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
