#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import warnings

import py.test

from ll.xist import xsc, sims
from ll.xist.ns import html, php


oldfilters = None


def setup_module(module):
	global oldfilters
	oldfilters = warnings.filters[:]

	warnings.filterwarnings("error", category=sims.EmptyElementWithContentWarning)
	warnings.filterwarnings("error", category=sims.WrongElementWarning)
	warnings.filterwarnings("error", category=sims.ElementWarning)
	warnings.filterwarnings("error", category=sims.IllegalTextWarning)


def teardown_module(module):
	warnings.filters = oldfilters


def test_empty():
	with xsc.Pool():
		class el1(xsc.Element):
			model = sims.Empty()

		e = el1()
		e.bytes()
	
		e = el1("gurk")
		py.test.raises(sims.EmptyElementWithContentWarning, e.bytes)
	
		e = el1(php.php("gurk"))
		py.test.raises(sims.EmptyElementWithContentWarning, e.bytes)
	
		e = el1(xsc.Comment("gurk"))
		py.test.raises(sims.EmptyElementWithContentWarning, e.bytes)
	
		e = el1(el1())
		py.test.raises(sims.EmptyElementWithContentWarning, e.bytes)


def test_elements():
	with xsc.Pool():
		class el11(xsc.Element):
			xmlname = "el1"
			xmlns = "ns1"
		class el12(xsc.Element):
			xmlname = "el2"
			xmlns = "ns1"
		class el21(xsc.Element):
			xmlname = "el1"
			xmlns = "ns2"
		class el22(xsc.Element):
			xmlname = "el2"
			xmlns = "ns2"

		el11.model = sims.Elements(el11, el21)
	
		e = el11()
		e.bytes()
	
		e = el11("foo")
		py.test.raises(sims.IllegalTextWarning, e.bytes)
	
		e = el11(php.php("gurk"))
		e.bytes()
	
		e = el11(xsc.Comment("gurk"))
		e.bytes()
	
		e = el11(el11())
		e.bytes()
	
		e = el11(el21())
		e.bytes()
	
		e = el11(el12())
		py.test.raises(sims.WrongElementWarning, e.bytes)
	
		e = el11(el22())
		py.test.raises(sims.WrongElementWarning, e.bytes)


def test_elementsortext():
	with xsc.Pool():
		class el11(xsc.Element):
			xmlname = "el1"
			xmlns = "ns1"
		class el12(xsc.Element):
			xmlname = "el2"
			xmlns = "ns1"
		class el21(xsc.Element):
			xmlname = "el1"
			xmlns = "ns2"
		class el22(xsc.Element):
			xmlname = "el2"
			xmlns = "ns2"

		el11.model = sims.ElementsOrText(el11, el21)
	
		e = el11()
		e.bytes()
	
		e = el11("foo")
		e.bytes()
	
		e = el11(php.php("gurk"))
		e.bytes()
	
		e = el11(xsc.Comment("gurk"))
		e.bytes()
	
		e = el11(el11())
		e.bytes()
	
		e = el11(el21())
		e.bytes()
	
		e = el11(el12())
		py.test.raises(sims.WrongElementWarning, e.bytes)
	
		e = el11(el22())
		py.test.raises(sims.WrongElementWarning, e.bytes)


def test_noelements():
	with xsc.Pool():
		class el1(xsc.Element):
			xmlns = "ns1"
			model = sims.NoElements()
		class el2(xsc.Element):
			xmlns = "ns2"

		e = el1()
		e.bytes()
	
		e = el1("foo")
		e.bytes()
	
		e = el1(php.php("gurk"))
		e.bytes()
	
		e = el1(xsc.Comment("gurk"))
		e.bytes()
	
		e = el1(el1())
		py.test.raises(sims.ElementWarning, e.bytes)

		# Elements from a different namespace are OK
		e = el1(el2())
		e.bytes()


def test_noelementsortext():
	with xsc.Pool():
		class el1(xsc.Element):
			xmlns = "ns1"
			model = sims.NoElementsOrText()
		class el2(xsc.Element):
			xmlns = "ns2"

		e = el1()
		e.bytes()
	
		e = el1("foo")
		py.test.raises(sims.IllegalTextWarning, e.bytes)
	
		e = el1(php.php("gurk"))
		e.bytes()
	
		e = el1(xsc.Comment("gurk"))
		e.bytes()
	
		e = el1(el1())
		py.test.raises(sims.ElementWarning, e.bytes)
	
		# Elements from a different namespace are OK
		e = el1(el2())
		e.bytes()
