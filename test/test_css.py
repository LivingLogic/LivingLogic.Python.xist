#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


from __future__ import with_statement

from ll.xist import xsc, css
from ll.xist.ns import html, specials


def test_css():
	with html.div(id=1) as e:
		with html.ul(id=2):
			+html.li("foo")
			+html.li()

	assert list(e.walknode(css.selector("div"))) == [e]
	assert list(e.walknode(css.selector("li"))) == [e[0][0], e[0][1]]
	assert list(e.walknode(css.selector("div#1"))) == [e]
	assert list(e.walknode(css.selector("#2"))) == [e[0]]
	assert list(e.walknode(css.selector(":empty"))) == [e[0][1]]
	assert list(e.walknode(css.selector("li:empty"))) == [e[0][1]]
	assert list(e.walknode(css.selector("div :empty"))) == [e[0][1]]
	assert list(e.walknode(css.selector("div>*:empty"))) == []
	assert list(e.walknode(css.selector("div>:empty"))) == []
	assert list(e.walknode(css.selector("*|li"))) == [e[0][0], e[0][1]]
	assert list(e.walknode(css.selector("h|li", prefixes={"h": html}))) == [e[0][0], e[0][1]]
	assert list(e.walknode(css.selector("h|li", prefixes={"h": specials}))) == []

	with xsc.Frag() as e:
		+html.div("foo")
		+xsc.Text("filler")
		+html.p("foo")
		+xsc.Text("filler")
		+html.ul(html.li("foo"))

	assert list(e.walknode(css.selector("div + p"))) == [e[2]]
	assert list(e.walknode(css.selector("div + ul"))) == []
	assert list(e.walknode(css.selector("ul + p"))) == []
	assert list(e.walknode(css.selector("div ~ p"))) == [e[2]]
	assert list(e.walknode(css.selector("div ~ ul"))) == [e[4]]
	assert list(e.walknode(css.selector("p ~ div"))) == []
	assert list(e.walknode(css.selector("div:first-child + p"))) == [e[2]]
	assert list(e.walknode(css.selector("*:first-child + p"))) == [e[2]]

	with xsc.Frag() as e:
		+html.span(html.b("hurz"), "gurk", html.em("hinz"), html.em("kunz"))
		+html.em("hurz")
		+html.em("hinz")
		+xsc.Text("nix")
		+html.i("kunz")

	assert list(e.walknode(css.selector("*:only-of-type"))) == [e[0], e[0][0], e[4]]
	assert list(e.walknode(css.selector("*:nth-child(1)"))) == [e[0], e[0][0]]
	assert list(e.walknode(css.selector("*:nth-child(2)"))) == [e[0][2], e[1]]
	assert list(e.walknode(css.selector("*:nth-last-child(1)"))) == [e[0][3], e[4]]
	assert list(e.walknode(css.selector("*:nth-last-child(2)"))) == [e[0][2], e[2]]
	assert list(e.walknode(css.selector("*:nth-of-type(1)"))) == [e[0], e[0][0], e[0][2], e[1], e[4]]
	assert list(e.walknode(css.selector("*:nth-of-type(2)"))) == [e[0][3], e[2]]
	assert list(e.walknode(css.selector("*:nth-last-of-type(1)"))) == [e[0], e[0][0], e[0][3], e[2], e[4]]
	assert list(e.walknode(css.selector("*:nth-last-of-type(2)"))) == [e[0][2], e[1]]

	e = xsc.Frag(html.span(html.b("hurz"), "gurk"))
	assert list(e.walknode(css.selector("*:only-child"))) == [e[0], e[0][0]]

	with xsc.Frag() as e:
		+html.em(class_="gurk", lang="en")
		+html.em(class_="gurk hurz", lang="en-us")
		+html.em(class_="hurz", lang="de")

	assert list(e.walknode(css.selector("em[class='gurk']"))) == [e[0]]
	assert list(e.walknode(css.selector("em[class~='gurk']"))) == [e[0], e[1]]
	assert list(e.walknode(css.selector("em[lang|='en']"))) == [e[0], e[1]]


def test_cssweight():
	# from http://www.w3.org/TR/css3-selectors/#specificity
	assert css.selector("*").cssweight() == (0, 0, 0)
	assert css.selector("LI").cssweight() == (0, 0, 1)
	assert css.selector("UL LI").cssweight() == (0, 0, 2)
	assert css.selector("UL OL+LI").cssweight() == (0, 0, 3)
	assert css.selector("UL OL LI.red").cssweight() == (0, 1, 3)
	assert css.selector("LI.red.level").cssweight() == (0, 2, 1)
	assert css.selector("#x34y").cssweight() == (1, 0, 0)
	# The following is not supported
	# assert css.selector("#s12:not(FOO)").cssweight() == (1, 0, 1)


def test_applystylesheets1():
	with html.html() as e:
		with html.head():
			+html.style("p {color: red;}", type="text/css")
		with html.body():
			+html.p("gurk")

	css.applystylesheets(e)

	assert str(e.walknode(html.p)[0].attrs.style) == "color: red;"
	assert list(e.walknode(html.style)) == []


def test_applystylesheets2():
	with html.html() as e:
		with html.head():
			+html.style("p.dont {color: red;}", type="text/css")
		with html.body():
			+html.p("gurk")

	css.applystylesheets(e)

	assert str(e.walknode(html.p)[0].attrs.style) == ""
	assert list(e.walknode(html.style)) == []


def test_applystylesheets3():
	with html.html() as e:
		with html.head():
			+html.style("p.do {color: red;}", type="text/css")
		with html.body():
			+html.p("gurk", class_="do")

	css.applystylesheets(e)

	assert str(e.walknode(html.p)[0].attrs.style) == "color: red;"
	assert list(e.walknode(html.style)) == []


def test_applystylesheets4():
	with html.html() as e:
		with html.head():
			+html.style("#id42 {color: red;}", type="text/css")
		with html.body():
			+html.p("gurk", id="id42", style="color: blue;")

	css.applystylesheets(e)

	# style attribute wins (same specificity, but it is considered to come last)
	assert str(e.walknode(html.p)[0].attrs.style) == "color: blue;"
	assert list(e.walknode(html.style)) == []


def test_applystylesheets5():
	with html.html() as e:
		with html.head():
			+html.style("p#id42 {color: red;}", type="text/css")
		with html.body():
			+html.p("gurk", id="id42", style="color: blue;")

	css.applystylesheets(e)

	# stylesheet wins (because element name + id has a greater specificity)
	assert str(e.walknode(html.p)[0].attrs.style) == "color: red;"
	assert list(e.walknode(html.style)) == []


def test_applystylesheets_media():
	# Check that media="screen" picks up the media stylesheet
	with html.html() as e:
		with html.head():
			+html.style("p {color: red;}", type="text/css", media="screen")
		with html.body():
			+html.p("gurk")

	css.applystylesheets(e, media="screen")

	assert str(e.walknode(html.p)[0].attrs.style) == "color: red;"

	# Check that media="screen" doesn't pick up the print stylesheet
	with html.html() as e:
		with html.head():
			+html.style("p {color: red;}", type="text/css", media="screen")
		with html.body():
			+html.p("gurk")

	css.applystylesheets(e, media="print")

	assert str(e.walknode(html.p)[0].attrs.style) == ""

	# Check that @media rules are treated properly
	with html.html() as e:
		with html.head():
			+html.style("@media screen { p {color: red;}}", type="text/css")
		with html.body():
			+html.p("gurk")

	css.applystylesheets(e, media="screen")

	assert str(e.walknode(html.p)[0].attrs.style) == "color: red;"

	with html.html() as e:
		with html.head():
			+html.style("@media screen { p {color: red;}}", type="text/css")
		with html.body():
			+html.p("gurk")

	css.applystylesheets(e, media="print")

	assert str(e.walknode(html.p)[0].attrs.style) == ""
