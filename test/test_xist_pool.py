#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2012 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import pytest

from ll.xist import xsc
from ll.xist.ns import html, php, chars, abbr


def test_basics():
	# empty pool
	r = xsc.Pool()
	with pytest.raises(xsc.IllegalElementError):
		r.elementclass("a", html)
	with pytest.raises(xsc.IllegalElementError):
		r.elementclass_xml("a", html)

	# register one element
	r = xsc.Pool(html.a)
	assert r.elementclass("a", html) is html.a
	assert r.elementclass_xml("a", html) is html.a
	with pytest.raises(xsc.IllegalElementError):
		r.elementclass("b", html)
	with pytest.raises(xsc.IllegalElementError):
		r.elementclass_xml("b", html)

	# register a module
	r = xsc.Pool(html)
	assert r.elementclass("a", html) is html.a
	assert r.elementclass_xml("a", html) is html.a
	assert r.elementclass("b", html) is html.b
	assert r.elementclass_xml("b", html) is html.b
	with pytest.raises(xsc.IllegalElementError):
		r.elementclass("c", html)
	with pytest.raises(xsc.IllegalElementError):
		r.elementclass_xml("c", html)

	# procinsts
	r = xsc.Pool(php.php)
	assert r.procinstclass("php") is php.php
	assert r.procinstclass_xml("php") is php.php
	assert r.procinst("php", "foo") == php.php("foo")
	assert r.procinst_xml("php", "foo") == php.php("foo")
	with pytest.raises(xsc.IllegalProcInstError):
		r.procinstclass("nophp")
	with pytest.raises(xsc.IllegalProcInstError):
		r.procinstclass_xml("nophp")

	# entities
	r = xsc.Pool(abbr)
	assert r.entityclass("xist") is abbr.xist
	assert r.entityclass_xml("xist") is abbr.xist
	assert r.entity("xist") == abbr.xist()
	assert r.entity_xml("xist") == abbr.xist()
	with pytest.raises(xsc.IllegalEntityError):
		r.entityclass("dontxist")
	with pytest.raises(xsc.IllegalEntityError):
		r.entityclass_xml("dontxist")

	# charrefs
	r = xsc.Pool(chars)
	assert r.charrefclass("ouml") is chars.ouml
	assert r.charrefclass_xml("ouml") is chars.ouml
	assert r.charrefclass(ord("ö")) is chars.ouml
	assert r.charrefclass_xml(ord("ö")) is chars.ouml
	assert r.charref("ouml") == chars.ouml()
	assert r.charref_xml("ouml") == chars.ouml()
	assert r.charref(ord("ö")) == chars.ouml()
	assert r.charref_xml(ord("ö")) == chars.ouml()
	with pytest.raises(xsc.IllegalEntityError):
		r.charrefclass("nothing")
	with pytest.raises(xsc.IllegalEntityError):
		r.charrefclass_xml("nothing")


def test_textcomment():
	r = xsc.Pool()
	assert r.text("foo") == xsc.Text("foo")
	assert r.comment("foo") == xsc.Comment("foo")


def test_defaultpool():
	r = xsc.threadlocalpool.pool
	assert r.elementclass("a", html) is html.a
	assert r.elementclass_xml("a", html) is html.a
	assert r.procinstclass("php") is php.php
	assert r.procinstclass_xml("php") is php.php
	assert r.entityclass("xist") is abbr.xist
	assert r.entityclass_xml("xist") is abbr.xist
	assert r.charrefclass("euro") is chars.euro
	assert r.charrefclass_xml("euro") is chars.euro
	assert r.charrefclass(ord("\N{EURO SIGN}")) is chars.euro
	assert r.charrefclass_xml(ord("\N{EURO SIGN}")) is chars.euro


def test_names():
	# Test classes where the Python and the XML name differ
	with xsc.Pool() as r:
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
			class attr(xsc.TextAttr):
				xmlname = "-attr"
				xmlns = "nix"

	# elements
	assert r.element1 is element1
	assert r.elementclass("element1", "nix") is element1
	assert r.elementclass_xml("-element", "nix") is element1
	assert r.element("element1", "nix") == element1()
	assert r.element_xml("-element", "nix") == element1()
	with pytest.raises(xsc.IllegalElementError):
		r.elementclass("-element", "nix")
	with pytest.raises(xsc.IllegalElementError):
		r.elementclass_xml("element1", "nix")
	# make sure that the default pool didn't pick up the new class
	with pytest.raises(xsc.IllegalElementError):
		xsc.threadlocalpool.pool.elementclass("element1", "nix")
	with pytest.raises(xsc.IllegalElementError):
		xsc.threadlocalpool.pool.elementclass_xml("-element", "nix")

	# procinsts
	assert r.procinst1 is procinst1
	assert r.procinstclass("procinst1") is procinst1
	assert r.procinstclass_xml("-procinst") is procinst1
	assert r.procinst("procinst1", "spam") == procinst1("spam")
	assert r.procinst_xml("-procinst", "spam") == procinst1("spam")
	with pytest.raises(xsc.IllegalProcInstError):
		r.procinstclass("-procinst")
	with pytest.raises(xsc.IllegalProcInstError):
		r.procinstclass_xml("procinst1")
	# make sure that the default pool didn't pick up the new class
	with pytest.raises(xsc.IllegalProcInstError):
		xsc.threadlocalpool.pool.procinstclass("procinst1")
	with pytest.raises(xsc.IllegalProcInstError):
		xsc.threadlocalpool.pool.procinstclass_xml("-procinst")

	# entities
	r.entity1 is entity1
	assert r.entityclass("entity1") is entity1
	assert r.entityclass_xml("-entity") is entity1
	assert r.entity("entity1") == entity1()
	assert r.entity_xml("-entity") == entity1()
	with pytest.raises(xsc.IllegalEntityError):
		r.entityclass("-entity")
	with pytest.raises(xsc.IllegalEntityError):
		r.entityclass_xml("entity1")
	# make sure that the default pool didn't pick up the new class
	with pytest.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.entityclass("entity1")
	with pytest.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.entityclass_xml("-entity")
	# the charref is an entity too
	assert r.entityclass("charref1") is charref1
	assert r.entityclass_xml("-charref") is charref1
	assert r.entity("charref1") == charref1()
	assert r.entity_xml("-charref") == charref1()
	with pytest.raises(xsc.IllegalEntityError):
		r.entityclass("-charref")
	with pytest.raises(xsc.IllegalEntityError):
		r.entityclass_xml("charref1")
	# make sure that the default pool didn't pick up the new class
	with pytest.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.entityclass("charref1")
	with pytest.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.entityclass_xml("-charref")

	# charrefs
	r.charref1 is charref1
	assert r.charrefclass("charref1") is charref1
	assert r.charrefclass_xml("-charref") is charref1
	assert r.charrefclass(42) is charref1
	assert r.charrefclass_xml(42) is charref1
	assert r.charref("charref1") == charref1()
	assert r.charref_xml("-charref") == charref1()
	assert r.charref(42) == charref1()
	assert r.charref_xml(42) == charref1()
	with pytest.raises(xsc.IllegalEntityError):
		r.charrefclass("-charref")
	with pytest.raises(xsc.IllegalEntityError):
		r.charrefclass_xml("charref1")
	# make sure that the default pool didn't pick up the new class
	with pytest.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.charrefclass("charref1")
	with pytest.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.charrefclass_xml("-charref")
	# make sure that entity has not been register as a charref
	with pytest.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.charrefclass("entity1")
	with pytest.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.charrefclass_xml("-entity")

	# attributes
	assert r.attrclass("attr", "nix") is Attrs.attr
	assert r.attrclass_xml("-attr", "nix") is Attrs.attr
	with pytest.raises(xsc.IllegalAttrError):
		r.attrclass("-attr", "nix")
	with pytest.raises(xsc.IllegalAttrError):
		r.attrclass_xml("attr", "nix")
	# make sure that the default pool didn't pick up the new class
	with pytest.raises(xsc.IllegalAttrError):
		xsc.threadlocalpool.pool.attrclass("attr", "nix")
	with pytest.raises(xsc.IllegalAttrError):
		xsc.threadlocalpool.pool.attrclass_xml("-attr", "nix")


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

	# Test charrefs
	assert set(r.charrefs()) == {cr_}


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

	assert p1.elementclass_xml("foo", "nix") is foo1
	with pytest.raises(xsc.IllegalElementError):
		p1.elementclass("bar", "nix")
	assert p1.elementclass_xml("baz", "nix") is baz

	assert p2.elementclass_xml("foo", "nix") is foo2
	assert p2.elementclass_xml("bar", "nix") is bar
	assert p2.elementclass_xml("baz", "nix") is baz


def test_chain2():
	with xsc.Pool() as p1:
		class foo1(xsc.Element):
			xmlns = "nix"

	with xsc.Pool() as p2:
		class foo2(xsc.Element):
			xmlns = "nix"

	p = xsc.Pool(p1, p2)
	assert p.elementclass_xml("foo2", "nix") is foo2


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
			assert str(getattr(node.attrs, name)) == value
		assert str(node.attrs.get(name)) == value
		if isinstance(name, str):
			assert str(node.attrs.get_xml(name.swapcase())) == value

	tests = [
		("a", "a"),
		("A", "A"),
		(Test.Attrs.a, "a"),
		(Test.Attrs.A, "A"),
		(Attrs.a, "a2"),
		(Attrs.A, "A2")
	]
	for (name, value) in tests:
		yield check, name, value

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
	assert cr in list(p2.charrefs())
