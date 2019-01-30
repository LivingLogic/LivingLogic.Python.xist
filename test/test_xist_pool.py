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
from ll.xist.ns import html, php, chars, abbr


def test_basics_element():
	def check(pool, xmlns, xmlname, cls):
		assert pool.elementclass(xmlns, xmlname) is cls
		e = pool.element(xmlns, xmlname)
		assert (e.xmlns, e.xmlname) == (xsc.nsname(xmlns), xmlname)

	# empty pool
	pool = xsc.Pool()
	check(pool, html, "a", xsc.Element)

	# register one element
	pool = xsc.Pool(html.a)
	check(pool, html, "a", html.a)
	check(pool, html, "b", xsc.Element)

	# register a module
	pool = xsc.Pool(html)
	check(pool, html, "a", html.a)
	check(pool, html, "b", html.b)
	check(pool, html, "c", xsc.Element)


def test_basics_procinst():
	def check(pool, xmlname, content, cls):
		assert pool.procinstclass(xmlname) is cls
		procinst = pool.procinst(xmlname, content)
		assert procinst.xmlname == xmlname
		assert procinst.content == content

	pool = xsc.Pool(php.php)
	check(pool, "php", "foo", php.php)
	check(pool, "nophp", "foo", xsc.ProcInst)


def test_basics_entity():
	def check(pool, xmlname, cls):
		assert pool.entityclass(xmlname) is cls
		assert pool.entity(xmlname).xmlname == xmlname

	pool = xsc.Pool(abbr)
	check(pool, "xist", abbr.xist)
	check(pool, "dontxist", xsc.Entity)


def test_textcomment():
	pool = xsc.Pool()
	assert pool.text("foo") == xsc.Text("foo")
	assert pool.comment("foo") == xsc.Comment("foo")


def test_defaultpool():
	pool = xsc.threadlocalpool.pool
	assert pool.elementclass(html, "a") is html.a
	assert pool.procinstclass("php") is php.php
	assert pool.entityclass("xist") is abbr.xist
	assert pool.entityclass("euro") is chars.euro


def test_names():
	# Test classes where the Python and the XML name differ
	with xsc.Pool() as pool:
		class element1(xsc.Element):
			xmlname = "-element"
			xmlns = "nix"
		class procinst1(xsc.ProcInst):
			xmlname = "-procinst"
		class entity1(xsc.Entity):
			xmlname = "-entity"
		class charref1(xsc.CharRef):
			xmlname = "-charref"
			codepoint = 42
		class Attrs(xsc.Attrs):
			xmlns = "nix"
			class attr(xsc.TextAttr):
				xmlname = "-attr"
				xmlns = "nix"

	# elements
	assert pool.element1 is element1
	assert pool.elementclass("nix", "-element") is element1
	assert pool.element("nix", "-element") == element1()
	assert pool.elementclass("nix", "element1") is xsc.Element
	# make sure that the default pool didn't pick up the new class
	assert xsc.threadlocalpool.pool.elementclass("nix", "-element") is xsc.Element

	# procinsts
	assert pool.procinst1 is procinst1
	assert pool.procinstclass("-procinst") is procinst1
	assert pool.procinst("-procinst", "spam") == procinst1("spam")
	assert pool.procinstclass("procinst1") is xsc.ProcInst
	# make sure that the default pool didn't pick up the new class
	assert xsc.threadlocalpool.pool.procinstclass("-procinst") is xsc.ProcInst

	# entities
	assert pool.entity1 is entity1
	assert pool.entityclass("-entity") is entity1
	assert pool.entity("-entity") == entity1()
	assert pool.entityclass("entity1") is xsc.Entity
	# make sure that the default pool didn't pick up the new class
	assert xsc.threadlocalpool.pool.entityclass("-entity") is xsc.Entity
	# the charref is an entity too
	assert pool.entityclass("-charref") is charref1
	assert pool.entity("-charref") == charref1()
	assert pool.entityclass("charref1") is xsc.Entity
	# make sure that the default pool didn't pick up the new class
	assert xsc.threadlocalpool.pool.entityclass("-charref") is xsc.Entity

	# attributes
	assert pool.attrkey("nix", "-attr") is Attrs.attr
	assert pool.attrkey("nix", "attr") == ("nix", "attr")
	# make sure that the default pool didn't pick up the new class
	assert xsc.threadlocalpool.pool.attrkey("nix", "-attr") == ("nix", "-attr")


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
	assert set(r.elements()) == {el_}

	# Test entities
	assert set(r.entities()) == {cr_, en_}

	# Test procinsts
	assert set(r.procinsts()) == {pi_}


def test_stack():
	with xsc.Pool() as r1:
		class foo1(xsc.Element):
			xmlname = "foo"
			xmlns = "nix"
		with xsc.Pool() as r2:
			class foo2(xsc.Element):
				xmlname = "foo"
				xmlns = "nix"

	assert r1.elementclass("nix", "foo") is foo1
	assert r2.elementclass("nix", "foo") is foo2


def test_chain():
	with xsc.Pool() as p1:
		class foo1(xsc.Element):
			xmlname = "foo"
			xmlns = "nix"
		class baz(xsc.Element):
			xmlns = "nix"

	with xsc.Pool(p1) as p2:
		class foo2(xsc.Element):
			xmlname = "foo"
			xmlns = "nix"
		class bar(xsc.Element):
			xmlns = "nix"

	assert p1.elementclass("nix", "foo") is foo1
	assert p1.elementclass("nix", "bar") is xsc.Element
	assert p1.elementclass("nix", "baz") is baz

	assert p2.elementclass("nix", "foo") is foo2
	assert p2.elementclass("nix", "bar") is bar
	assert p2.elementclass("nix", "baz") is baz


def test_chain2():
	with xsc.Pool() as p1:
		class foo1(xsc.Element):
			xmlns = "nix"

	with xsc.Pool() as p2:
		class foo2(xsc.Element):
			xmlns = "nix"

	p = xsc.Pool(p1, p2)
	assert p.elementclass("nix", "foo2") is foo2


def test_mixedattrnames():
	with xsc.Pool() as r:
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

	xmlns = "test"

	node = Test(
		{
			Attrs.a: "a2",
			Attrs.A: "A2",
		},
		a="a",
		A="A"
	)

	def check(name, value):
		assert str(node[name]) == value
		assert str(node.attrs[name]) == value
		if isinstance(name, str):
			assert str(getattr(node.attrs, name)).swapcase() == value

	check("A", "a")
	check("a", "A")
	check(Test.Attrs.a, "a")
	check(Test.Attrs.A, "A")
	check(Attrs.a, "a2")
	check(Attrs.A, "A2")


def test_xmlns():
	p = xsc.Pool(html)
	assert p.xmlns == html.xmlns


def test_itermethods():
	class pi(xsc.ProcInst):
		pass
	class en(xsc.Entity):
		pass
	class cr(xsc.CharRef):
		codepoint = 0x42

	p1 = xsc.Pool(html.a, pi, en, cr)
	p2 = xsc.Pool(html.b, p1)

	assert html.a in list(p2.elements())
	assert html.b in list(p2.elements())
	assert pi in list(p2.procinsts())
	assert en in list(p2.entities())
	assert cr in list(p2.entities())
