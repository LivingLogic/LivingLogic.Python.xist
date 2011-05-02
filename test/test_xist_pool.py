#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2011 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2011 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import py.test

from ll.xist import xsc
from ll.xist.ns import html, php, chars, abbr


def test_basics():
	# empty pool
	r = xsc.Pool()
	with py.test.raises(xsc.IllegalElementError):
		r.elementclass(u"a", html)
	with py.test.raises(xsc.IllegalElementError):
		r.elementclass_xml(u"a", html)

	# register one element
	r = xsc.Pool(html.a)
	assert r.elementclass(u"a", html) is html.a
	assert r.elementclass_xml(u"a", html) is html.a
	with py.test.raises(xsc.IllegalElementError):
		r.elementclass(u"b", html)
	with py.test.raises(xsc.IllegalElementError):
		r.elementclass_xml(u"b", html)

	# register a module
	r = xsc.Pool(html)
	assert r.elementclass(u"a", html) is html.a
	assert r.elementclass_xml(u"a", html) is html.a
	assert r.elementclass(u"b", html) is html.b
	assert r.elementclass_xml(u"b", html) is html.b
	with py.test.raises(xsc.IllegalElementError):
		r.elementclass(u"c", html)
	with py.test.raises(xsc.IllegalElementError):
		r.elementclass_xml(u"c", html)

	# procinsts
	r = xsc.Pool(php.php)
	assert r.procinstclass(u"php") is php.php
	assert r.procinstclass_xml(u"php") is php.php
	assert r.procinst(u"php", u"foo") == php.php(u"foo")
	assert r.procinst_xml(u"php", u"foo") == php.php(u"foo")
	with py.test.raises(xsc.IllegalProcInstError):
		r.procinstclass(u"nophp")
	with py.test.raises(xsc.IllegalProcInstError):
		r.procinstclass_xml(u"nophp")

	# entities
	r = xsc.Pool(abbr)
	assert r.entityclass(u"xist") is abbr.xist
	assert r.entityclass_xml(u"xist") is abbr.xist
	assert r.entity(u"xist") == abbr.xist()
	assert r.entity_xml(u"xist") == abbr.xist()
	with py.test.raises(xsc.IllegalEntityError):
		r.entityclass(u"dontxist")
	with py.test.raises(xsc.IllegalEntityError):
		r.entityclass_xml(u"dontxist")

	# charrefs
	r = xsc.Pool(chars)
	assert r.charrefclass(u"ouml") is chars.ouml
	assert r.charrefclass_xml(u"ouml") is chars.ouml
	assert r.charrefclass(ord(u"ö")) is chars.ouml
	assert r.charrefclass_xml(ord(u"ö")) is chars.ouml
	assert r.charref(u"ouml") == chars.ouml()
	assert r.charref_xml(u"ouml") == chars.ouml()
	assert r.charref(ord(u"ö")) == chars.ouml()
	assert r.charref_xml(ord(u"ö")) == chars.ouml()
	with py.test.raises(xsc.IllegalEntityError):
		r.charrefclass(u"nothing")
	with py.test.raises(xsc.IllegalEntityError):
		r.charrefclass_xml(u"nothing")


def test_textcomment():
	r = xsc.Pool()
	assert r.text(u"foo") == xsc.Text(u"foo")
	assert r.comment(u"foo") == xsc.Comment(u"foo")


def test_defaultpool():
	r = xsc.threadlocalpool.pool
	assert r.elementclass(u"a", html) is html.a
	assert r.elementclass_xml(u"a", html) is html.a
	assert r.procinstclass(u"php") is php.php
	assert r.procinstclass_xml(u"php") is php.php
	assert r.entityclass(u"xist") is abbr.xist
	assert r.entityclass_xml(u"xist") is abbr.xist
	assert r.charrefclass(u"euro") is chars.euro
	assert r.charrefclass_xml(u"euro") is chars.euro
	assert r.charrefclass(ord(u"\N{EURO SIGN}")) is chars.euro
	assert r.charrefclass_xml(ord(u"\N{EURO SIGN}")) is chars.euro


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
	assert r.elementclass(u"element1", u"nix") is element1
	assert r.elementclass_xml(u"-element", u"nix") is element1
	assert r.element(u"element1", u"nix") == element1()
	assert r.element_xml(u"-element", u"nix") == element1()
	with py.test.raises(xsc.IllegalElementError):
		r.elementclass(u"-element", u"nix")
	with py.test.raises(xsc.IllegalElementError):
		r.elementclass_xml(u"element1", u"nix")
	# make sure that the default pool didn't pick up the new class
	with py.test.raises(xsc.IllegalElementError):
		xsc.threadlocalpool.pool.elementclass(u"element1", u"nix")
	with py.test.raises(xsc.IllegalElementError):
		xsc.threadlocalpool.pool.elementclass_xml(u"-element", u"nix")

	# procinsts
	assert r.procinst1 is procinst1
	assert r.procinstclass(u"procinst1") is procinst1
	assert r.procinstclass_xml(u"-procinst") is procinst1
	assert r.procinst(u"procinst1", u"spam") == procinst1(u"spam")
	assert r.procinst_xml(u"-procinst", u"spam") == procinst1(u"spam")
	with py.test.raises(xsc.IllegalProcInstError):
		r.procinstclass(u"-procinst")
	with py.test.raises(xsc.IllegalProcInstError):
		r.procinstclass_xml(u"procinst1")
	# make sure that the default pool didn't pick up the new class
	with py.test.raises(xsc.IllegalProcInstError):
		xsc.threadlocalpool.pool.procinstclass(u"procinst1")
	with py.test.raises(xsc.IllegalProcInstError):
		xsc.threadlocalpool.pool.procinstclass_xml(u"-procinst")

	# entities
	r.entity1 is entity1
	assert r.entityclass(u"entity1") is entity1
	assert r.entityclass_xml(u"-entity") is entity1
	assert r.entity(u"entity1") == entity1()
	assert r.entity_xml(u"-entity") == entity1()
	with py.test.raises(xsc.IllegalEntityError):
		r.entityclass(u"-entity")
	with py.test.raises(xsc.IllegalEntityError):
		r.entityclass_xml(u"entity1")
	# make sure that the default pool didn't pick up the new class
	with py.test.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.entityclass(u"entity1")
	with py.test.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.entityclass_xml(u"-entity")
	# the charref is an entity too
	assert r.entityclass(u"charref1") is charref1
	assert r.entityclass_xml(u"-charref") is charref1
	assert r.entity(u"charref1") == charref1()
	assert r.entity_xml(u"-charref") == charref1()
	with py.test.raises(xsc.IllegalEntityError):
		r.entityclass(u"-charref")
	with py.test.raises(xsc.IllegalEntityError):
		r.entityclass_xml(u"charref1")
	# make sure that the default pool didn't pick up the new class
	with py.test.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.entityclass(u"charref1")
	with py.test.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.entityclass_xml(u"-charref")

	# charrefs
	r.charref1 is charref1
	assert r.charrefclass(u"charref1") is charref1
	assert r.charrefclass_xml(u"-charref") is charref1
	assert r.charrefclass(42) is charref1
	assert r.charrefclass_xml(42) is charref1
	assert r.charref(u"charref1") == charref1()
	assert r.charref_xml(u"-charref") == charref1()
	assert r.charref(42) == charref1()
	assert r.charref_xml(42) == charref1()
	with py.test.raises(xsc.IllegalEntityError):
		r.charrefclass(u"-charref")
	with py.test.raises(xsc.IllegalEntityError):
		r.charrefclass_xml(u"charref1")
	# make sure that the default pool didn't pick up the new class
	with py.test.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.charrefclass(u"charref1")
	with py.test.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.charrefclass_xml(u"-charref")
	# make sure that entity has not been register as a charref
	with py.test.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.charrefclass(u"entity1")
	with py.test.raises(xsc.IllegalEntityError):
		xsc.threadlocalpool.pool.charrefclass_xml(u"-entity")

	# attributes
	assert r.attrclass(u"attr", u"nix") is Attrs.attr
	assert r.attrclass_xml(u"-attr", u"nix") is Attrs.attr
	with py.test.raises(xsc.IllegalAttrError):
		r.attrclass(u"-attr", u"nix")
	with py.test.raises(xsc.IllegalAttrError):
		r.attrclass_xml(u"attr", u"nix")
	# make sure that the default pool didn't pick up the new class
	with py.test.raises(xsc.IllegalAttrError):
		xsc.threadlocalpool.pool.attrclass(u"attr", u"nix")
	with py.test.raises(xsc.IllegalAttrError):
		xsc.threadlocalpool.pool.attrclass_xml(u"-attr", u"nix")


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

	assert r1.elementclass_xml(u"foo", u"nix") is foo1
	assert r2.elementclass_xml(u"foo", u"nix") is foo2


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

	assert p1.elementclass_xml(u"foo", u"nix") is foo1
	with py.test.raises(xsc.IllegalElementError):
		p1.elementclass(u"bar", u"nix")
	assert p1.elementclass_xml(u"baz", u"nix") is baz

	assert p2.elementclass_xml(u"foo", u"nix") is foo2
	assert p2.elementclass_xml(u"bar", u"nix") is bar
	assert p2.elementclass_xml(u"baz", u"nix") is baz


def test_chain2():
	with xsc.Pool() as p1:
		class foo1(xsc.Element):
			xmlns = "nix"

	with xsc.Pool() as p2:
		class foo2(xsc.Element):
			xmlns = "nix"

	p = xsc.Pool(p1, p2)
	assert p.elementclass_xml(u"foo2", u"nix") is foo2


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
		assert unicode(node[name]) == value
		assert unicode(node.attrs[name]) == value
		if isinstance(name, basestring):
			assert unicode(getattr(node.attrs, name)) == value
		assert unicode(node.attrs.get(name)) == value
		if isinstance(name, basestring):
			assert unicode(node.attrs.get_xml(name.swapcase())) == value

	tests = [
		(u"a", u"a"),
		(u"A", u"A"),
		(Test.Attrs.a, u"a"),
		(Test.Attrs.A, u"A"),
		(Attrs.a, u"a2"),
		(Attrs.A, u"A2")
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
