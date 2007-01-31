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
from ll.xist.ns import html, php, chars, abbr


def test_basics():
	# empty pool
	r = xsc.Pool()
	py.test.raises(xsc.IllegalElementError, r.elementclass, "a", html)
	py.test.raises(xsc.IllegalElementError, r.elementclass_xml, "a", html)

	# register one element
	r = xsc.Pool(html.a)
	assert r.elementclass("a", html) is html.a
	assert r.elementclass_xml("a", html) is html.a
	py.test.raises(xsc.IllegalElementError, r.elementclass, "b", html)
	py.test.raises(xsc.IllegalElementError, r.elementclass_xml, "b", html)

	# register a module
	r = xsc.Pool(html)
	assert r.elementclass("a", html) is html.a
	assert r.elementclass_xml("a", html) is html.a
	assert r.elementclass("b", html) is html.b
	assert r.elementclass_xml("b", html) is html.b
	py.test.raises(xsc.IllegalElementError, r.elementclass, "c", html)
	py.test.raises(xsc.IllegalElementError, r.elementclass_xml, "c", html)

	# procinsts
	r = xsc.Pool(php.php)
	assert r.procinstclass("php") is php.php
	assert r.procinstclass_xml("php") is php.php
	assert r.procinst("php", "foo") == php.php("foo")
	assert r.procinst_xml("php", "foo") == php.php("foo")
	py.test.raises(xsc.IllegalProcInstError, r.procinstclass, "nophp")
	py.test.raises(xsc.IllegalProcInstError, r.procinstclass_xml, "nophp")

	# entities
	r = xsc.Pool(abbr)
	assert r.entityclass("xist") is abbr.xist
	assert r.entityclass_xml("xist") is abbr.xist
	assert r.entity("xist") == abbr.xist()
	assert r.entity_xml("xist") == abbr.xist()
	py.test.raises(xsc.IllegalEntityError, r.entityclass, "dontxist")
	py.test.raises(xsc.IllegalEntityError, r.entityclass_xml, "dontxist")

	# charrefs
	r = xsc.Pool(chars)
	assert r.charrefclass("ouml") is chars.ouml
	assert r.charrefclass_xml("ouml") is chars.ouml
	assert r.charrefclass(ord(u"ö")) is chars.ouml
	assert r.charrefclass_xml(ord(u"ö")) is chars.ouml
	assert r.charref("ouml") == chars.ouml()
	assert r.charref_xml("ouml") == chars.ouml()
	assert r.charref(ord(u"ö")) == chars.ouml()
	assert r.charref_xml(ord(u"ö")) == chars.ouml()
	py.test.raises(xsc.IllegalEntityError, r.charrefclass, "nothing")
	py.test.raises(xsc.IllegalEntityError, r.charrefclass_xml, "nothing")


def test_textcomment():
	r = xsc.Pool()
	assert r.text("foo") == xsc.Text("foo")
	assert r.comment("foo") == xsc.Comment("foo")


def test_defaultpool():
	r = xsc.defaultpool
	assert r.elementclass("a", html) is html.a
	assert r.elementclass_xml("a", html) is html.a
	assert r.procinstclass("php") is php.php
	assert r.procinstclass_xml("php") is php.php
	assert r.entityclass("xist") is abbr.xist
	assert r.entityclass_xml("xist") is abbr.xist
	assert r.charrefclass("euro") is chars.euro
	assert r.charrefclass_xml("euro") is chars.euro
	assert r.charrefclass(ord(u"\N{EURO SIGN}")) is chars.euro
	assert r.charrefclass_xml(ord(u"\N{EURO SIGN}")) is chars.euro


def test_names():
	# Test classes where the Python and the XML name differ
	with xsc.Pool() as r:
		class element(xsc.Element):
			xmlname = "-element"
			xmlns = "nix"
		class procinst(xsc.ProcInst):
			xmlname = "-procinst"
		class entity(xsc.Entity):
			xmlname = "-entity"
		class charref(xsc.CharRef):
			xmlname = "-charref"
			codepoint = 42

	# elements
	assert r.elementclass("element", "nix") is element
	assert r.elementclass_xml("-element", "nix") is element
	assert r.element("element", "nix") == element()
	assert r.element_xml("-element", "nix") == element()
	py.test.raises(xsc.IllegalElementError, r.elementclass, "-element", "nix")
	py.test.raises(xsc.IllegalElementError, r.elementclass_xml, "element", "nix")
	# make sure that the default pool didn't pick up the new class
	py.test.raises(xsc.IllegalElementError, xsc.defaultpool.elementclass, "element", "nix")
	py.test.raises(xsc.IllegalElementError, xsc.defaultpool.elementclass_xml, "-element", "nix")

	# procinsts
	assert r.procinstclass("procinst") is procinst
	assert r.procinstclass_xml("-procinst") is procinst
	assert r.procinst("procinst", "spam") == procinst("spam")
	assert r.procinst_xml("-procinst", "spam") == procinst("spam")
	py.test.raises(xsc.IllegalProcInstError, r.procinstclass, "-procinst")
	py.test.raises(xsc.IllegalProcInstError, r.procinstclass_xml, "procinst")
	# make sure that the default pool didn't pick up the new class
	py.test.raises(xsc.IllegalProcInstError, xsc.defaultpool.procinstclass, "procinst")
	py.test.raises(xsc.IllegalProcInstError, xsc.defaultpool.procinstclass_xml, "-procinst")

	# entities
	assert r.entityclass("entity") is entity
	assert r.entityclass_xml("-entity") is entity
	assert r.entity("entity") == entity()
	assert r.entity_xml("-entity") == entity()
	py.test.raises(xsc.IllegalEntityError, r.entityclass, "-entity")
	py.test.raises(xsc.IllegalEntityError, r.entityclass_xml, "entity")
	# make sure that the default pool didn't pick up the new class
	py.test.raises(xsc.IllegalEntityError, xsc.defaultpool.entityclass, "entity")
	py.test.raises(xsc.IllegalEntityError, xsc.defaultpool.entityclass_xml, "-entity")
	# the charref is an entity too
	assert r.entityclass("charref") is charref
	assert r.entityclass_xml("-charref") is charref
	assert r.entity("charref") == charref()
	assert r.entity_xml("-charref") == charref()
	py.test.raises(xsc.IllegalEntityError, r.entityclass, "-charref")
	py.test.raises(xsc.IllegalEntityError, r.entityclass_xml, "charref")
	# make sure that the default pool didn't pick up the new class
	py.test.raises(xsc.IllegalEntityError, xsc.defaultpool.entityclass, "charref")
	py.test.raises(xsc.IllegalEntityError, xsc.defaultpool.entityclass_xml, "-charref")

	# charrefs
	assert r.charrefclass("charref") is charref
	assert r.charrefclass_xml("-charref") is charref
	assert r.charrefclass(42) is charref
	assert r.charrefclass_xml(42) is charref
	assert r.charref("charref") == charref()
	assert r.charref_xml("-charref") == charref()
	assert r.charref(42) == charref()
	assert r.charref_xml(42) == charref()
	py.test.raises(xsc.IllegalEntityError, r.charrefclass, "-charref")
	py.test.raises(xsc.IllegalEntityError, r.charrefclass_xml, "charref")
	# make sure that the default pool didn't pick up the new class
	py.test.raises(xsc.IllegalEntityError, xsc.defaultpool.charrefclass, "charref")
	py.test.raises(xsc.IllegalEntityError, xsc.defaultpool.charrefclass_xml, "-charref")
	# make sure that entity has not been register as a charref
	py.test.raises(xsc.IllegalEntityError, xsc.defaultpool.charrefclass, "entity")
	py.test.raises(xsc.IllegalEntityError, xsc.defaultpool.charrefclass_xml, "-entity")


def test_names2():
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
	assert list(r.elementkeys()) == [("el_", None)]
	assert list(r.elementkeys_xml()) == [("el", None)]
	assert list(r.elementvalues()) == [el_]
	assert list(r.elementitems()) == [(("el_", None), el_)]
	assert list(r.elementitems_xml()) == [(("el", None), el_)]
	
	# Test entities
	keys = list(r.entitykeys())
	assert len(keys) == 2
	assert "en_" in keys
	assert "cr_" in keys
	keys = list(r.entitykeys_xml())
	assert len(keys) == 2
	assert "en" in keys
	assert "cr" in keys
	values = list(r.entityvalues())
	assert len(values) == 2
	assert en_ in values
	assert cr_ in values
	items = list(r.entityitems())
	assert len(items) == 2
	assert ("en_", en_) in items
	assert ("cr_", cr_) in items
	items = list(r.entityitems_xml())
	assert len(items) == 2
	assert ("en", en_) in items
	assert ("cr", cr_) in items

	# Test procinsts
	assert list(r.procinstkeys()) == ["pi_"]
	assert list(r.procinstkeys_xml()) == ["pi"]
	assert list(r.procinstvalues()) == [pi_]
	assert list(r.procinstitems()) == [("pi_", pi_)]
	assert list(r.procinstitems_xml()) == [("pi", pi_)]

	# Test charrefs
	assert list(r.charrefkeys()) == ["cr_"]
	assert list(r.charrefkeys_xml()) == ["cr"]
	assert list(r.charrefvalues()) == [cr_]
	assert list(r.charrefitems()) == [("cr_", cr_)]
	assert list(r.charrefitems_xml()) == [("cr", cr_)]


def test_stack():
	with xsc.Pool() as r1:
		class foo1(xsc.Element):
			xmlname = "foo"
			xmlns = "nix"
		with xsc.Pool() as r2:
			class foo2(xsc.Element):
				xmlname = "foo"
				xmlns = "nix"

	assert r1.elementclass_xml("foo", "nix") is foo1
	assert r2.elementclass_xml("foo", "nix") is foo2


def test_base():
	with xsc.Pool() as r1:
		class foo1(xsc.Element):
			xmlname = "foo"
			xmlns = "nix"
		class baz(xsc.Element):
			xmlns = "nix"

	with xsc.Pool(r1) as r2:
		class foo2(xsc.Element):
			xmlname = "foo"
			xmlns = "nix"
		class bar(xsc.Element):
			xmlns = "nix"

	assert r1.elementclass_xml("foo", "nix") is foo1
	py.test.raises(xsc.IllegalElementError, r1.elementclass, "bar", "nix")
	assert r1.elementclass_xml("baz", "nix") is baz

	assert r2.elementclass_xml("foo", "nix") is foo2
	assert r2.elementclass_xml("bar", "nix") is bar
	assert r2.elementclass_xml("baz", "nix") is baz


def test_defaultbase():
	with xsc.Pool() as r1:
		class foo(xsc.Element):
			xmlns = "nix"

		with xsc.Pool(True) as r2:
			class bar(xsc.Element):
				xmlns = "nix"

	assert r1.elementclass_xml("foo", "nix") is foo
	py.test.raises(xsc.IllegalElementError, r1.elementclass, "bar", "nix")

	assert r2.elementclass_xml("foo", "nix") is foo
	assert r2.elementclass_xml("bar", "nix") is bar


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
			xmlns = "test"
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
		assert unicode(node.attrs.get(name)) == value
		if isinstance(name, tuple):
			name = (name[0], name[1].swapcase())
		else:
			name = name.swapcase()
		assert unicode(node.attrs.get_xml(name)) == value

	tests = [
		("a", "a"),
		("A", "A"),
		(("a", xmlns), "a2"),
		(("A", xmlns), "A2")
	]
	for (name, value) in tests:
		yield check, name, value
