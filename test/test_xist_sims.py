#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2012 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll.xist import xsc, sims
from ll.xist.ns import html, php


with xsc.Pool():
	class el1(xsc.Element):
		model = sims.Empty()


# The following tests are split into separate test functions, because ``pytest`` has problems otherwise
def test_empty1():
	e = el1()
	e.bytes()


def test_empty2(recwarn):
	e = el1("gurk")
	e.bytes()
	w = recwarn.pop(sims.EmptyElementWithContentWarning)


def test_empty3(recwarn):
	e = el1(php.php("gurk"))
	e.bytes()
	w = recwarn.pop(sims.EmptyElementWithContentWarning)


def test_empty4(recwarn):
	e = el1(xsc.Comment("gurk"))
	e.bytes()
	w = recwarn.pop(sims.EmptyElementWithContentWarning)


def test_empty5(recwarn):
	e = el1(el1())
	e.bytes()
	w = recwarn.pop(sims.EmptyElementWithContentWarning)


def test_elements(recwarn):
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
		e.bytes()
		w = recwarn.pop(sims.IllegalTextWarning)

		e = el11(php.php("gurk"))
		e.bytes()

		e = el11(xsc.Comment("gurk"))
		e.bytes()

		e = el11(el11())
		e.bytes()

		e = el11(el21())
		e.bytes()

		e = el11(el12())
		e.bytes()
		w = recwarn.pop(sims.WrongElementWarning)

		e = el11(el22())
		e.bytes()
		w = recwarn.pop(sims.WrongElementWarning)


def test_elementsortext(recwarn):
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
		e.bytes()
		w = recwarn.pop(sims.WrongElementWarning)

		e = el11(el22())
		e.bytes()
		w = recwarn.pop(sims.WrongElementWarning)


def test_noelements(recwarn):
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
		e.bytes()
		w = recwarn.pop(sims.ElementWarning)

		# Elements from a different namespace are OK
		e = el1(el2())
		e.bytes()


def test_noelementsortext(recwarn):
	with xsc.Pool():
		class el1(xsc.Element):
			xmlns = "ns1"
			model = sims.NoElementsOrText()
		class el2(xsc.Element):
			xmlns = "ns2"

		e = el1()
		e.bytes()

		e = el1("foo")
		e.bytes()
		w = recwarn.pop(sims.IllegalTextWarning)

		e = el1(php.php("gurk"))
		e.bytes()

		e = el1(xsc.Comment("gurk"))
		e.bytes()

		e = el1(el1())
		e.bytes()
		w = recwarn.pop(sims.ElementWarning)

		# Elements from a different namespace are OK
		e = el1(el2())
		e.bytes()
