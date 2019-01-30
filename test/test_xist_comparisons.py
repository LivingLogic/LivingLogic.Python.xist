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
from ll.xist.ns import html, abbr, ul4


def test_frageq():
	assert xsc.Frag() == xsc.Frag()
	assert xsc.Frag(1) == xsc.Frag(1)
	assert xsc.Frag(1, 2) == xsc.Frag(1, 2, None)
	assert xsc.Frag(1, 2) != xsc.Frag(12)
	assert xsc.Frag() != xsc.Frag("")
	assert xsc.Frag("") != xsc.Frag("", "")


def test_elementeq():
	assert html.div() == html.div()
	assert html.div(1) == html.div(1)
	assert html.div(1, 2) == html.div(1, 2, None)
	assert html.div(1, 2) != html.div(12)
	assert html.div() != html.div("")
	assert html.div("") != html.div("", "")
	assert html.div(1, html.div(2, html.div(3))) == html.div(1, html.div(2, html.div(3)))

	# Test plain element instances
	plainelement = xsc.element(html, "div")
	assert plainelement.__class__ is xsc.Element
	assert plainelement.xmlns == html.div.xmlns
	assert plainelement.xmlname == html.div.xmlname
	assert html.div() == plainelement


def test_texteq():
	assert xsc.Text() == xsc.Text()
	assert xsc.Text(1) == xsc.Text(1)
	assert xsc.Text("1") == xsc.Text(1)
	assert xsc.Text("1") == xsc.Text(1)
	assert xsc.Text("") != xsc.Text(1)


def test_commenteq():
	assert xsc.Comment() == xsc.Comment()
	assert xsc.Comment(1) == xsc.Comment(1)
	assert xsc.Comment("1") == xsc.Comment(1)
	assert xsc.Comment("1") == xsc.Comment(1)
	assert xsc.Comment("") != xsc.Comment(1)


def test_doctypeeq():
	assert xsc.DocType() == xsc.DocType()
	assert xsc.DocType(1) == xsc.DocType(1)
	assert xsc.DocType("1") == xsc.DocType(1)
	assert xsc.DocType("1") == xsc.DocType(1)
	assert xsc.DocType("") != xsc.DocType(1)


def test_entityeq():
	assert abbr.html() == abbr.html()
	assert abbr.sgml() != abbr.html()

	# Test plain entity instances
	plainentity = xsc.entity("html")
	assert plainentity.__class__ is xsc.Entity
	assert abbr.html() == plainentity


def test_procinsteq():
	assert ul4.code() == ul4.code()
	assert ul4.code("x = 1") == ul4.code("x = 1")
	assert ul4.code("x = 1") != ul4.code("x = 2")
	assert ul4.code("x") != ul4.return_("x")

	# Test plain processing instruction instances
	plainprocinst = xsc.procinst("code", "x = 1")
	assert plainprocinst.__class__ is xsc.ProcInst
	assert ul4.code("x = 1") == plainprocinst


def test_mixeq():
	assert xsc.Comment(1) != xsc.Text(1)
	assert xsc.DocType(1) != xsc.Text(1)
