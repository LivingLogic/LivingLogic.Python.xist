#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


from __future__ import with_statement

from ll.xist.ns import html


def test_applycss1():
	with html.html() as e:
		with html.head():
			+html.style("p {color: red;}", type="text/css")
		with html.body():
			+html.p("gurk")

	html.applycss(e)

	assert str(e.walknode(html.p)[0].attrs.style) == "color: red;"
	assert list(e.walknode(html.style)) == []


def test_applycss2():
	with html.html() as e:
		with html.head():
			+html.style("p.dont {color: red;}", type="text/css")
		with html.body():
			+html.p("gurk")

	html.applycss(e)

	assert str(e.walknode(html.p)[0].attrs.style) == ""
	assert list(e.walknode(html.style)) == []



def test_applycss3():
	with html.html() as e:
		with html.head():
			+html.style("p.do {color: red;}", type="text/css")
		with html.body():
			+html.p("gurk", class_="do")

	html.applycss(e)

	assert str(e.walknode(html.p)[0].attrs.style) == "color: red;"
	assert list(e.walknode(html.style)) == []
