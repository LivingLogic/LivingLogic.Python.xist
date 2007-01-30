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
	# empty registry
	r = xsc.Registry()
	py.test.raises(xsc.IllegalElementError, r.element_py, "a", html)
	py.test.raises(xsc.IllegalElementError, r.element_xml, "a", html)

	# register one element
	r = xsc.Registry(html.a)
	assert r.element_py("a", html) is html.a
	assert r.element_xml("a", html) is html.a
	py.test.raises(xsc.IllegalElementError, r.element_py, "b", html)
	py.test.raises(xsc.IllegalElementError, r.element_xml, "b", html)

	# register a module
	r = xsc.Registry(html)
	assert r.element_py("a", html) is html.a
	assert r.element_xml("a", html) is html.a
	assert r.element_py("b", html) is html.b
	assert r.element_xml("b", html) is html.b
	py.test.raises(xsc.IllegalElementError, r.element_py, "c", html)
	py.test.raises(xsc.IllegalElementError, r.element_xml, "c", html)

	# procinsts
	r = xsc.Registry(php.php)
	assert r.procinst_py("php") is php.php
	assert r.procinst_xml("php") is php.php
	assert r.create_procinst_py("php", "foo") == php.php("foo")
	assert r.create_procinst_xml("php", "foo") == php.php("foo")
	py.test.raises(xsc.IllegalProcInstError, r.procinst_py, "nophp")
	py.test.raises(xsc.IllegalProcInstError, r.procinst_xml, "nophp")

	# entities
	r = xsc.Registry(abbr)
	assert r.entity_py("xist") is abbr.xist
	assert r.entity_xml("xist") is abbr.xist
	assert r.create_entity_py("xist") == abbr.xist()
	assert r.create_entity_xml("xist") == abbr.xist()
	py.test.raises(xsc.IllegalEntityError, r.entity_py, "dontxist")
	py.test.raises(xsc.IllegalEntityError, r.entity_xml, "dontxist")

	# charrefs
	r = xsc.Registry(chars)
	assert r.charref_py("ouml") is chars.ouml
	assert r.charref_xml("ouml") is chars.ouml
	assert r.charref_py(ord(u"ö")) is chars.ouml
	assert r.charref_xml(ord(u"ö")) is chars.ouml
	assert r.create_charref_py("ouml") == chars.ouml()
	assert r.create_charref_xml("ouml") == chars.ouml()
	assert r.create_charref_py(ord(u"ö")) == chars.ouml()
	assert r.create_charref_xml(ord(u"ö")) == chars.ouml()
	py.test.raises(xsc.IllegalEntityError, r.charref_py, "nothing")
	py.test.raises(xsc.IllegalEntityError, r.charref_xml, "nothing")


def test_textcomment():
	r = xsc.Registry()
	assert r.create_text("foo") == xsc.Text("foo")
	assert r.create_comment("foo") == xsc.Comment("foo")


def test_defaultregistry():
	r = xsc.defaultregistry
	assert r.element_py("a", html) is html.a
	assert r.element_xml("a", html) is html.a
	assert r.procinst_py("php") is php.php
	assert r.procinst_xml("php") is php.php
	assert r.entity_py("xist") is abbr.xist
	assert r.entity_xml("xist") is abbr.xist
	assert r.charref_py("euro") is chars.euro
	assert r.charref_xml("euro") is chars.euro
	assert r.charref_py(ord(u"\N{EURO SIGN}")) is chars.euro
	assert r.charref_xml(ord(u"\N{EURO SIGN}")) is chars.euro


def test_names():
	# Test classes where the Python and the XML name differ
	with xsc.Registry() as r:
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
	assert r.element_py("element", "nix") is element
	assert r.element_xml("-element", "nix") is element
	assert r.create_element_py("element", "nix") == element()
	assert r.create_element_xml("-element", "nix") == element()
	py.test.raises(xsc.IllegalElementError, r.element_py, "-element", "nix")
	py.test.raises(xsc.IllegalElementError, r.element_xml, "element", "nix")
	# make sure that the default registry didn't pick up the new class
	py.test.raises(xsc.IllegalElementError, xsc.defaultregistry.element_py, "element", "nix")
	py.test.raises(xsc.IllegalElementError, xsc.defaultregistry.element_xml, "-element", "nix")

	# procinsts
	assert r.procinst_py("procinst") is procinst
	assert r.procinst_xml("-procinst") is procinst
	assert r.create_procinst_py("procinst", "spam") == procinst("spam")
	assert r.create_procinst_xml("-procinst", "spam") == procinst("spam")
	py.test.raises(xsc.IllegalProcInstError, r.procinst_py, "-procinst")
	py.test.raises(xsc.IllegalProcInstError, r.procinst_xml, "procinst")
	# make sure that the default registry didn't pick up the new class
	py.test.raises(xsc.IllegalProcInstError, xsc.defaultregistry.procinst_py, "procinst")
	py.test.raises(xsc.IllegalProcInstError, xsc.defaultregistry.procinst_xml, "-procinst")

	# entities
	assert r.entity_py("entity") is entity
	assert r.entity_xml("-entity") is entity
	assert r.create_entity_py("entity") == entity()
	assert r.create_entity_xml("-entity") == entity()
	py.test.raises(xsc.IllegalEntityError, r.entity_py, "-entity")
	py.test.raises(xsc.IllegalEntityError, r.entity_xml, "entity")
	# make sure that the default registry didn't pick up the new class
	py.test.raises(xsc.IllegalEntityError, xsc.defaultregistry.entity_py, "entity")
	py.test.raises(xsc.IllegalEntityError, xsc.defaultregistry.entity_xml, "-entity")
	# the charref is an entity too
	assert r.entity_py("charref") is charref
	assert r.entity_xml("-charref") is charref
	assert r.create_entity_py("charref") == charref()
	assert r.create_entity_xml("-charref") == charref()
	py.test.raises(xsc.IllegalEntityError, r.entity_py, "-charref")
	py.test.raises(xsc.IllegalEntityError, r.entity_xml, "charref")
	# make sure that the default registry didn't pick up the new class
	py.test.raises(xsc.IllegalEntityError, xsc.defaultregistry.entity_py, "charref")
	py.test.raises(xsc.IllegalEntityError, xsc.defaultregistry.entity_xml, "-charref")

	# charrefs
	assert r.charref_py("charref") is charref
	assert r.charref_xml("-charref") is charref
	assert r.charref_py(42) is charref
	assert r.charref_xml(42) is charref
	assert r.create_charref_py("charref") == charref()
	assert r.create_charref_xml("-charref") == charref()
	assert r.create_charref_py(42) == charref()
	assert r.create_charref_xml(42) == charref()
	py.test.raises(xsc.IllegalEntityError, r.charref_py, "-charref")
	py.test.raises(xsc.IllegalEntityError, r.charref_xml, "charref")
	# make sure that the default registry didn't pick up the new class
	py.test.raises(xsc.IllegalEntityError, xsc.defaultregistry.charref_py, "charref")
	py.test.raises(xsc.IllegalEntityError, xsc.defaultregistry.charref_xml, "-charref")
	# make sure that entity has not been register as a charref
	py.test.raises(xsc.IllegalEntityError, xsc.defaultregistry.charref_py, "entity")
	py.test.raises(xsc.IllegalEntityError, xsc.defaultregistry.charref_xml, "-entity")


def test_stack():
	with xsc.Registry() as r1:
		class foo1(xsc.Element):
			xmlname = "foo"
			xmlns = "nix"
		with xsc.Registry() as r2:
			class foo2(xsc.Element):
				xmlname = "foo"
				xmlns = "nix"

	assert r1.element_xml("foo", "nix") is foo1
	assert r2.element_xml("foo", "nix") is foo2


def test_base():
	with xsc.Registry() as r1:
		class foo1(xsc.Element):
			xmlname = "foo"
			xmlns = "nix"
		class baz(xsc.Element):
			xmlns = "nix"

	with xsc.Registry(r1) as r2:
		class foo2(xsc.Element):
			xmlname = "foo"
			xmlns = "nix"
		class bar(xsc.Element):
			xmlns = "nix"

	assert r1.element_xml("foo", "nix") is foo1
	py.test.raises(xsc.IllegalElementError, r1.element_py, "bar", "nix")
	assert r1.element_xml("baz", "nix") is baz

	assert r2.element_xml("foo", "nix") is foo2
	assert r2.element_xml("bar", "nix") is bar
	assert r2.element_xml("baz", "nix") is baz


def test_defaultbase():
	with xsc.Registry() as r1:
		class foo(xsc.Element):
			xmlns = "nix"

		with xsc.Registry(True) as r2:
			class bar(xsc.Element):
				xmlns = "nix"

	assert r1.element_xml("foo", "nix") is foo
	py.test.raises(xsc.IllegalElementError, r1.element_py, "bar", "nix")

	assert r2.element_xml("foo", "nix") is foo
	assert r2.element_xml("bar", "nix") is bar
