#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


import py.test

from ll.xist import xsc
from ll.xist.ns import html, xml, chars, abbr, ihtml, wml, specials, htmlspecials, form, meta, svg, fo, docbook, jsp, struts_html, struts_config, tld


def test_mixedattrnames():
	class __ns__(xsc.Namespace):
		xmlname = "test"
		xmlurl = "test"

		class Attrs(xsc.Namespace.Attrs):
			class a(xsc.TextAttr): xmlname = "A"
			class A(xsc.TextAttr): xmlname = "a"
		class Test(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class a(xsc.TextAttr): xmlname = "A"
				class A(xsc.TextAttr): xmlname = "a"

	node = __ns__.Test(
		{
			(__ns__, "a"): "a2",
			(__ns__, "A"): "A2",
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
		((__ns__, "a"), "a2"),
		((__ns__, "A"), "A2")
	]
	for (name, value) in tests:
		yield check, name, value


def test_variousnamespaces():
	def check(ns, *skip):
		for obj in ns.iterelementvalues():
			if not issubclass(obj, skip):
				node = obj()
				for (attrname, attrvalue) in node.attrs.alloweditems():
					if attrvalue.required:
						if attrvalue.values:
							node[attrname] = attrvalue.values[0]
						else:
							node[attrname] = "foo"
			node.conv().asBytes()
		for obj in ns.iterentityvalues():
			node = obj()
			node.conv().asBytes()
		for obj in ns.iterprocinstvalues():
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


def test_nsupdate():
	def createns():
		class __ns__(xsc.Namespace):
			xmlname = "gurk"
			xmlurl = "http://www.gurk.com/"
			class foo(xsc.Element): pass
			class bar(xsc.Element): pass
		return __ns__
	
	class ns1:
		class foo(xsc.Element): pass
		class bar(xsc.Element): pass
		class foo2(xsc.Element): pass
		class bar2(xsc.Element): pass
	class ns2:
		class foo(xsc.Element): pass
		class bar(xsc.Element): pass
		class foo2(xsc.Element): pass
		class bar2(xsc.Element): pass
	a = [ {"foo": ns.foo, "bar": ns.bar, "foo2": ns.foo2, "bar2": ns.bar2} for ns in (ns1, ns2) ]

	ns = createns()
	ns.update(*a)
	assert ns.element("foo") is ns2.foo
	assert ns.element("bar") is ns2.bar
	assert ns.element("foo2") is ns2.foo2
	assert ns.element("bar2") is ns2.bar2

	ns = createns()
	ns.updatenew(*a)
	assert ns.element("foo") is ns.foo
	assert ns.element("bar") is ns.bar
	assert ns.element("foo2") is ns2.foo2
	assert ns.element("bar2") is ns2.bar2

	ns = createns()
	ns.updateexisting(*a)
	assert ns.element("foo") == ns2.foo
	assert ns.element("bar") == ns2.bar
	py.test.raises(xsc.IllegalElementError, ns.element, "foo2")
	py.test.raises(xsc.IllegalElementError, ns.element, "bar2")


def test_attributeexamples():
	assert xsc.amp.__name__ == "amp"
	assert xsc.amp.xmlname == u"amp"
	assert xsc.amp.__ns__ is None
	assert xsc.amp.xmlprefix() is None

	assert chars.uuml.__name__ == "uuml"
	assert chars.uuml.xmlname == u"uuml"
	assert chars.uuml.__ns__ is chars
	assert chars.uuml.xmlprefix() == "chars"

	assert html.a.Attrs.class_.__name__ == "class_"
	assert html.a.Attrs.class_.xmlname == u"class"
	assert html.a.Attrs.class_.__ns__ is None

	assert xml.Attrs.lang.__name__ == "lang"
	assert xml.Attrs.lang.xmlname == u"lang"
	assert xml.Attrs.lang.__ns__ is xml
	assert xml.Attrs.lang.xmlprefix() == "xml"


def test_autoinherit():
	class NS1(xsc.Namespace):
		xmlname = "test"
		xmlurl = "test"
		class foo(xsc.Element):
			model = False
			def convert(self, converter):
				e = self.__ns__.bar()
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


def check_nskeysvaluesitems(ns, method, resname, resclass):
	assert getattr(ns, method + "keys")(xml=False) == [resname]
	assert getattr(ns, method + "keys")(xml=True) == [resname[:-1]]

	assert getattr(ns, method + "values")() == [resclass]

	assert getattr(ns, method + "items")(xml=False) == [(resname, resclass)]
	assert getattr(ns, method + "items")(xml=True) == [(resname[:-1], resclass)]


def test_nskeysvaluesitems():
	class NS(xsc.Namespace):
		xmlname = "test"
		class el_(xsc.Element):
			xmlname = "el"
		class en_(xsc.Entity):
			xmlname = "en"
		class pi_(xsc.ProcInst):
			xmlname = "pi"
		class cr_(xsc.CharRef):
			xmlname = "cr"
			codepoint = 0x4242

	check_nskeysvaluesitems(NS, "element", "el_", NS.el_)

	keys = NS.entitykeys(xml=False)
	assert len(keys) == 2
	assert "en_" in keys
	assert "cr_" in keys
	keys = NS.entitykeys(xml=True)
	assert len(keys) == 2
	assert "en" in keys
	assert "cr" in keys

	values = NS.entityvalues()
	assert len(values) == 2
	assert NS.en_ in values
	assert NS.cr_ in values

	items = NS.entityitems(xml=False)
	assert len(items) == 2
	assert ("en_", NS.en_) in items
	assert ("cr_", NS.cr_) in items
	items = NS.entityitems(xml=True)
	assert len(items) == 2
	assert ("en", NS.en_) in items
	assert ("cr", NS.cr_) in items

	check_nskeysvaluesitems(NS, "procinst", "pi_", NS.pi_)

	check_nskeysvaluesitems(NS, "charref", "cr_", NS.cr_)


def test_prefixsubclasses():
	class NS1(xsc.Namespace):
		xmlname = "ns"
		xmlurl = "http://xmlns.ns.info/"

		class gurk(xsc.Element):
			model = False

	class NS2(NS1):
		xmlname = "ns"

	p = xsc.Prefixes(ns=NS1)

	assert \
		NS1.gurk().asBytes(xhtml=2, prefixmode=2, prefixes=p) == \
		'<ns:gurk xmlns:ns="http://xmlns.ns.info/"/>'

	# The sub namespace should pick up the prefix defined for the first one
	assert \
		NS2.gurk().asBytes(xhtml=2, prefixmode=2, prefixes=p) == \
		'<ns:gurk xmlns:ns="http://xmlns.ns.info/"/>'
