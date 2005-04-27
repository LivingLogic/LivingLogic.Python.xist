#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


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
	class ns1(xsc.Namespace):
		class el1(xsc.Element):
			model = sims.Empty()

	e = ns1.el1()
	e.asBytes()

	e = ns1.el1("gurk")
	py.test.raises(sims.EmptyElementWithContentWarning, e.asBytes)

	e = ns1.el1(php.php("gurk"))
	py.test.raises(sims.EmptyElementWithContentWarning, e.asBytes)

	e = ns1.el1(xsc.Comment("gurk"))
	py.test.raises(sims.EmptyElementWithContentWarning, e.asBytes)

	e = ns1.el1(ns1.el1())
	py.test.raises(sims.EmptyElementWithContentWarning, e.asBytes)


def test_elements():
	class ns1(xsc.Namespace):
		class el1(xsc.Element):
			pass
		class el2(xsc.Element):
			pass

	class ns2(xsc.Namespace):
		class el1(xsc.Element):
			pass
		class el2(xsc.Element):
			pass

	ns1.el1.model = sims.Elements(ns1.el1, ns2.el1)

	e = ns1.el1()
	e.asBytes()

	e = ns1.el1("foo")
	py.test.raises(sims.IllegalTextWarning, e.asBytes)

	e = ns1.el1(php.php("gurk"))
	e.asBytes()

	e = ns1.el1(xsc.Comment("gurk"))
	e.asBytes()

	e = ns1.el1(ns1.el1())
	e.asBytes()

	e = ns1.el1(ns2.el1())
	e.asBytes()

	e = ns1.el1(ns1.el2())
	py.test.raises(sims.WrongElementWarning, e.asBytes)

	e = ns1.el1(ns2.el2())
	py.test.raises(sims.WrongElementWarning, e.asBytes)


def test_elementsortext():
	class ns1(xsc.Namespace):
		class el1(xsc.Element):
			pass
		class el2(xsc.Element):
			pass

	class ns2(xsc.Namespace):
		class el1(xsc.Element):
			pass
		class el2(xsc.Element):
			pass

	ns1.el1.model = sims.ElementsOrText(ns1.el1, ns2.el1)

	e = ns1.el1()
	e.asBytes()

	e = ns1.el1("foo")
	e.asBytes()

	e = ns1.el1(php.php("gurk"))
	e.asBytes()

	e = ns1.el1(xsc.Comment("gurk"))
	e.asBytes()

	e = ns1.el1(ns1.el1())
	e.asBytes()

	e = ns1.el1(ns2.el1())
	e.asBytes()

	e = ns1.el1(ns1.el2())
	py.test.raises(sims.WrongElementWarning, e.asBytes)

	e = ns1.el1(ns2.el2())
	py.test.raises(sims.WrongElementWarning, e.asBytes)


def test_noelements():
	class ns1(xsc.Namespace):
		class el1(xsc.Element):
			model = sims.NoElements()

	class ns2(xsc.Namespace):
		class el1(xsc.Element):
			pass

	e = ns1.el1()
	e.asBytes()

	e = ns1.el1("foo")
	e.asBytes()

	e = ns1.el1(php.php("gurk"))
	e.asBytes()

	e = ns1.el1(xsc.Comment("gurk"))
	e.asBytes()

	e = ns1.el1(ns1.el1())
	py.test.raises(sims.ElementWarning, e.asBytes)

	e = ns1.el1(ns2.el1())
	e.asBytes()


def test_noelementsortext():
	class ns1(xsc.Namespace):
		class el1(xsc.Element):
			model = sims.NoElementsOrText()

	class ns2(xsc.Namespace):
		class el1(xsc.Element):
			pass

	e = ns1.el1()
	e.asBytes()

	e = ns1.el1("foo")
	py.test.raises(sims.IllegalTextWarning, e.asBytes)

	e = ns1.el1(php.php("gurk"))
	e.asBytes()

	e = ns1.el1(xsc.Comment("gurk"))
	e.asBytes()

	e = ns1.el1(ns1.el1())
	py.test.raises(sims.ElementWarning, e.asBytes)

	e = ns1.el1(ns2.el1())
	e.asBytes()
