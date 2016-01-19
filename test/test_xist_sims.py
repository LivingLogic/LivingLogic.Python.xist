#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import warnings

from ll.xist import xsc, sims
from ll.xist.ns import html, php


with xsc.Pool():
	class el1(xsc.Element):
		model = sims.Empty()


# The following tests are split into separate test functions, because ``pytest`` has problems otherwise
def test_empty1():
	e = el1()
	e.bytes(validate=True)


def test_empty2():
	e = el1("gurk")
	with warnings.catch_warnings(record=True) as w:
		e.bytes(validate=True)
	assert len(w) == 1
	assert issubclass(w[-1].category, sims.EmptyElementWithContentWarning)


def test_empty3():
	e = el1(php.php("gurk"))
	with warnings.catch_warnings(record=True) as w:
		e.bytes(validate=True)
	assert len(w) == 1
	assert issubclass(w[-1].category, sims.EmptyElementWithContentWarning)


def test_empty4():
	e = el1(xsc.Comment("gurk"))
	with warnings.catch_warnings(record=True) as w:
		e.bytes(validate=True)
	assert len(w) == 1
	assert issubclass(w[-1].category, sims.EmptyElementWithContentWarning)


def test_empty5():
	e = el1(el1())
	with warnings.catch_warnings(record=True) as w:
		e.bytes(validate=True)
	assert len(w) == 1
	assert issubclass(w[-1].category, sims.EmptyElementWithContentWarning)


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
		e.bytes(validate=True)

		e = el11("foo")
		with warnings.catch_warnings(record=True) as w:
			e.bytes(validate=True)
		assert len(w) == 1
		assert issubclass(w[-1].category, sims.IllegalTextWarning)

		e = el11(php.php("gurk"))
		e.bytes(validate=True)

		e = el11(xsc.Comment("gurk"))
		e.bytes(validate=True)

		e = el11(el11())
		e.bytes(validate=True)

		e = el11(el21())
		e.bytes(validate=True)

		e = el11(el12())
		with warnings.catch_warnings(record=True) as w:
			e.bytes(validate=True)
		assert len(w) == 1
		assert issubclass(w[-1].category, sims.WrongElementWarning)

		e = el11(el22())
		with warnings.catch_warnings(record=True) as w:
			e.bytes(validate=True)
		assert len(w) == 1
		assert issubclass(w[-1].category, sims.WrongElementWarning)


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
		e.bytes(validate=True)

		e = el11("foo")
		e.bytes(validate=True)

		e = el11(php.php("gurk"))
		e.bytes(validate=True)

		e = el11(xsc.Comment("gurk"))
		e.bytes(validate=True)

		e = el11(el11())
		e.bytes(validate=True)

		e = el11(el21())
		e.bytes(validate=True)

		e = el11(el12())
		with warnings.catch_warnings(record=True) as w:
			e.bytes(validate=True)
		assert len(w) == 1
		assert issubclass(w[-1].category, sims.WrongElementWarning)

		e = el11(el22())
		with warnings.catch_warnings(record=True) as w:
			e.bytes(validate=True)
		assert len(w) == 1
		assert issubclass(w[-1].category, sims.WrongElementWarning)


def test_noelements():
	with xsc.Pool():
		class el1(xsc.Element):
			xmlns = "ns1"
			model = sims.NoElements()
		class el2(xsc.Element):
			xmlns = "ns2"

		e = el1()
		e.bytes(validate=True)

		e = el1("foo")
		e.bytes(validate=True)

		e = el1(php.php("gurk"))
		e.bytes(validate=True)

		e = el1(xsc.Comment("gurk"))
		e.bytes(validate=True)

		e = el1(el1())
		with warnings.catch_warnings(record=True) as w:
			e.bytes(validate=True)
		assert len(w) == 1
		assert issubclass(w[-1].category, sims.ElementWarning)

		# Elements from a different namespace are OK
		e = el1(el2())
		e.bytes(validate=True)


def test_noelementsortext():
	with xsc.Pool():
		class el1(xsc.Element):
			xmlns = "ns1"
			model = sims.NoElementsOrText()
		class el2(xsc.Element):
			xmlns = "ns2"

		e = el1()
		e.bytes(validate=True)

		e = el1("foo")
		with warnings.catch_warnings(record=True) as w:
			e.bytes(validate=True)
		assert len(w) == 1
		assert issubclass(w[-1].category, sims.IllegalTextWarning)

		e = el1(php.php("gurk"))
		e.bytes(validate=True)

		e = el1(xsc.Comment("gurk"))
		e.bytes(validate=True)

		e = el1(el1())
		with warnings.catch_warnings(record=True) as w:
			e.bytes(validate=True)
		assert len(w) == 1
		assert issubclass(w[-1].category, sims.ElementWarning)

		# Elements from a different namespace are OK
		e = el1(el2())
		e.bytes(validate=True)
