#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll.xist import xsc
from ll.xist.ns import html


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


def test_texteq():
	assert xsc.Text() == xsc.Text()
	assert xsc.Text(1) == xsc.Text(1)
	assert xsc.Text("1") == xsc.Text(1)
	assert xsc.Text(u"1") == xsc.Text(1)
	assert xsc.Text("") != xsc.Text(1)


def test_commenteq():
	assert xsc.Comment() == xsc.Comment()
	assert xsc.Comment(1) == xsc.Comment(1)
	assert xsc.Comment("1") == xsc.Comment(1)
	assert xsc.Comment(u"1") == xsc.Comment(1)
	assert xsc.Comment("") != xsc.Comment(1)


def test_doctypeeq():
	assert xsc.DocType() == xsc.DocType()
	assert xsc.DocType(1) == xsc.DocType(1)
	assert xsc.DocType("1") == xsc.DocType(1)
	assert xsc.DocType(u"1") == xsc.DocType(1)
	assert xsc.DocType("") != xsc.DocType(1)


def test_mixeq():
	assert xsc.Comment(1) != xsc.Text(1)
	assert xsc.DocType(1) != xsc.Text(1)
