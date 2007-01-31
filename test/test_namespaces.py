#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


from __future__ import with_statement

import py.test

from ll.xist import xsc
from ll.xist.ns import html, xml, chars, abbr, ihtml, wml, specials, htmlspecials, form, meta, svg, fo, docbook, jsp, struts_html, struts_config, tld


def test_mixedattrnames():
	with xsc.Pool() as r:
		xmlns = "test"

		class Attrs(xsc.Attrs):
			class a(xsc.TextAttr):
				xmlns = "test"
				xmlname = "A"
			class A(xsc.TextAttr):
				xmlns = "test"
				xmlname = "a"
	
		class Test(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class a(xsc.TextAttr):
					xmlname = "A"
				class A(xsc.TextAttr):
					xmlname = "a"

	node = Test(
		{
			("a", xmlns): "a2",
			("A", xmlns): "A2",
		},
		a="a",
		A="A"
	)

	def check(name, value):
		assert unicode(node[name]) == value
		assert unicode(node.attrs[name]) == value
		if not isinstance(name, tuple):
			assert unicode(getattr(node.attrs, name)) == value
		assert unicode(node.attrs.get(name, xml=False)) == value
		if isinstance(name, tuple):
			name = (name[0], name[1].swapcase())
		else:
			name = name.swapcase()
		assert unicode(node.attrs.get(name, xml=True)) == value

	tests = [
		("a", "a"),
		("A", "A"),
		(("a", xmlns), "a2"),
		(("A", xmlns), "A2")
	]
	for (name, value) in tests:
		yield check, name, value


def test_variousnamespaces():
	def check(ns, *skip):
		for obj in vars(ns).itervalues():
			if isinstance(obj, type) and issubclass(obj, xsc.Element) and not issubclass(obj, skip):
				node = obj()
				for (attrname, attrvalue) in node.attrs.alloweditems():
					if attrvalue.required:
						if attrvalue.values:
							node[attrname] = attrvalue.values[0]
						else:
							node[attrname] = "foo"
				node.conv().asBytes()
		for obj in vars(ns).itervalues():
			if isinstance(obj, type) and issubclass(obj, xsc.Entity):
				node = obj()
				node.conv().asBytes()
		for obj in vars(ns).itervalues():
			if isinstance(obj, type) and issubclass(obj, xsc.ProcInst):
				node = obj()
				node.conv().asBytes()

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
	yield check, struts_html
	yield check, struts_config
	yield check, tld


def test_attributeexamples():
	assert xsc.amp.__name__ == "amp"
	assert xsc.amp.xmlname == u"amp"
	assert xsc.amp.xmlns is None

	assert chars.uuml.__name__ == "uuml"
	assert chars.uuml.xmlname == u"uuml"
	assert chars.uuml.xmlns is None

	assert html.a.Attrs.class_.__name__ == "class_"
	assert html.a.Attrs.class_.xmlname == u"class"
	assert html.a.Attrs.class_.xmlns is None

	assert xml.Attrs.lang.__name__ == "lang"
	assert xml.Attrs.lang.xmlname == u"lang"
	assert xml.Attrs.lang.xmlns == xml.xmlns


def test_subclassing():
	class NS1(xsc.Namespace):
		xmlname = "test"

		class foo(xsc.Element):
			model = False
			def convert(self, converter):
				e = self.xmlns().bar()
				return e.convert(converter)

		class bar(xsc.Entity):
			def convert(self, converter):
				return xsc.Text(17)

	class NS2(NS1):
		xmlname = "test"

		class bar(xsc.Entity):
			def convert(self, converter):
				return xsc.Text(23)

	assert unicode(NS1.foo().conv()) == u"17"
	assert unicode(NS2.foo().conv()) == u"23"


def test_poolkeysvaluesitems():
	with xsc.Pool() as r:
		class el_(xsc.Element):
			xmlname = "el"
		class en_(xsc.Entity):
			xmlname = "en"
		class pi_(xsc.ProcInst):
			xmlname = "pi"
		class cr_(xsc.CharRef):
			xmlname = "cr"
			codepoint = 0x4242

	# Test elements
	keys = list(r.element_keys_py())
	assert keys == [("el_", None)]
	keys = list(r.element_keys_xml())
	assert keys == [("el", None)]
	values = list(r.element_values())
	assert values == [el_]
	items = list(r.element_items_py())
	assert items == [(("el_", None), el_)]
	items = list(r.element_items_xml())
	assert items == [(("el", None), el_)]
	
	# Test entities
	keys = list(r.entity_keys_py())
	assert len(keys) == 2
	assert "en_" in keys
	assert "cr_" in keys
	keys = list(r.entity_keys_xml())
	assert len(keys) == 2
	assert "en" in keys
	assert "cr" in keys
	values = list(r.entity_values())
	assert len(values) == 2
	assert en_ in values
	assert cr_ in values
	items = list(r.entity_items_py())
	assert len(items) == 2
	assert ("en_", en_) in items
	assert ("cr_", cr_) in items
	items = list(r.entity_items_xml())
	assert len(items) == 2
	assert ("en", en_) in items
	assert ("cr", cr_) in items

	# Test procinsts
	keys = list(r.procinst_keys_py())
	assert keys == ["pi_"]
	keys = list(r.procinst_keys_xml())
	assert keys == ["pi"]
	values = list(r.procinst_values())
	assert values == [pi_]
	items = list(r.procinst_items_py())
	assert items == [("pi_", pi_)]
	items = list(r.procinst_items_xml())
	assert items == [("pi", pi_)]

	# Test charrefs
	keys = list(r.charref_keys_py())
	assert keys == ["cr_"]
	keys = list(r.charref_keys_xml())
	assert keys == ["cr"]
	values = list(r.charref_values())
	assert values == [cr_]
	items = list(r.charref_items_py())
	assert items == [("cr_", cr_)]
	items = list(r.charref_items_xml())
	assert items == [("cr", cr_)]
