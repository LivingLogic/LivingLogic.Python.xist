#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


from ll import url
from ll.xist import xsc, css, parse
from ll.xist.ns import html, specials


def test_css():
	with xsc.build():
		with html.div(id=1) as e:
			with html.ul(id=2):
				+html.li("foo")
				+html.li()

	assert list(e.walknodes(css.selector("div"))) == [e]
	assert list(e.walknodes(css.selector("li"))) == [e[0][0], e[0][1]]
	assert list(e.walknodes(css.selector("div#1"))) == [e]
	assert list(e.walknodes(css.selector("#2"))) == [e[0]]
	assert list(e.walknodes(css.selector(":empty"))) == [e[0][1]]
	assert list(e.walknodes(css.selector("li:empty"))) == [e[0][1]]
	assert list(e.walknodes(css.selector("div :empty"))) == [e[0][1]]
	assert list(e.walknodes(css.selector("div>*:empty"))) == []
	assert list(e.walknodes(css.selector("div>:empty"))) == []
	assert list(e.walknodes(css.selector("*|li"))) == [e[0][0], e[0][1]]
	assert list(e.walknodes(css.selector("h|li", prefixes={"h": html}))) == [e[0][0], e[0][1]]
	assert list(e.walknodes(css.selector("h|li", prefixes={"h": specials}))) == []

	with xsc.build():
		with xsc.Frag() as e:
			+html.div("foo")
			+xsc.Text("filler")
			+html.p("foo")
			+xsc.Text("filler")
			+html.ul(html.li("foo"))

	assert list(e.walknodes(css.selector("div + p"))) == [e[2]]
	assert list(e.walknodes(css.selector("div + ul"))) == []
	assert list(e.walknodes(css.selector("ul + p"))) == []
	assert list(e.walknodes(css.selector("div ~ p"))) == [e[2]]
	assert list(e.walknodes(css.selector("div ~ ul"))) == [e[4]]
	assert list(e.walknodes(css.selector("p ~ div"))) == []
	assert list(e.walknodes(css.selector("div:first-child + p"))) == [e[2]]
	assert list(e.walknodes(css.selector("*:first-child + p"))) == [e[2]]

	with xsc.build():
		with xsc.Frag() as e:
			+html.span(html.b("hurz"), "gurk", html.em("hinz"), html.em("kunz"))
			+html.em("hurz")
			+html.em("hinz")
			+xsc.Text("nix")
			+html.i("kunz")

	assert list(e.walknodes(css.selector("*:only-of-type"))) == [e[0], e[0][0], e[4]]
	assert list(e.walknodes(css.selector("*:nth-child(1)"))) == [e[0], e[0][0]]
	assert list(e.walknodes(css.selector("*:nth-child(2)"))) == [e[0][2], e[1]]
	assert list(e.walknodes(css.selector("*:nth-last-child(1)"))) == [e[0][3], e[4]]
	assert list(e.walknodes(css.selector("*:nth-last-child(2)"))) == [e[0][2], e[2]]
	assert list(e.walknodes(css.selector("*:nth-of-type(1)"))) == [e[0], e[0][0], e[0][2], e[1], e[4]]
	assert list(e.walknodes(css.selector("*:nth-of-type(2)"))) == [e[0][3], e[2]]
	assert list(e.walknodes(css.selector("*:nth-last-of-type(1)"))) == [e[0], e[0][0], e[0][3], e[2], e[4]]
	assert list(e.walknodes(css.selector("*:nth-last-of-type(2)"))) == [e[0][2], e[1]]

	e = xsc.Frag(html.span(html.b("hurz"), "gurk"))
	assert list(e.walknodes(css.selector("*:only-child"))) == [e[0], e[0][0]]

	with xsc.build():
		with xsc.Frag() as e:
			+html.em(class_="gurk", lang="en")
			+html.em(class_="gurk hurz", lang="en-us")
			+html.em(class_="hurz", lang="de")

	assert list(e.walknodes(css.selector("em[class='gurk']"))) == [e[0]]
	assert list(e.walknodes(css.selector("em[class~='gurk']"))) == [e[0], e[1]]
	assert list(e.walknodes(css.selector("em[lang|='en']"))) == [e[0], e[1]]


def test_applystylesheets1():
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style("p {color: red;}", type="text/css")
			with html.body():
				+html.p("gurk")

	css.applystylesheets(e)

	assert str(e.walknodes(html.p)[0].attrs.style) == "color: red;"
	assert list(e.walknodes(html.style)) == []


def test_applystylesheets2():
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style("p.dont {color: red;}", type="text/css")
			with html.body():
				+html.p("gurk")

	css.applystylesheets(e)

	assert str(e.walknodes(html.p)[0].attrs.style) == ""
	assert list(e.walknodes(html.style)) == []


def test_applystylesheets3():
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style("p.do {color: red;}", type="text/css")
			with html.body():
				+html.p("gurk", class_="do")

	css.applystylesheets(e)

	assert str(e.walknodes(html.p)[0].attrs.style) == "color: red;"
	assert list(e.walknodes(html.style)) == []


def test_applystylesheets4():
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style("#id42 {color: red;}", type="text/css")
			with html.body():
				+html.p("gurk", id="id42", style="color: blue;")

	css.applystylesheets(e)

	# style attribute wins
	assert str(e.walknodes(html.p)[0].attrs.style) == "color: blue;"
	assert list(e.walknodes(html.style)) == []


def test_applystylesheets5():
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style("p#id42 {color: red;}", type="text/css")
			with html.body():
				+html.p("gurk", id="id42", style="color: blue;")

	css.applystylesheets(e)

	# stylesheet always wins (at least in CSS 2.1 and 3)
	assert str(e.walknodes(html.p)[0].attrs.style) == "color: blue;"
	assert list(e.walknodes(html.style)) == []


def test_applystylesheets_media():
	# Check that media="screen" picks up the media stylesheet
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style("p {color: red;}", type="text/css", media="screen")
			with html.body():
				+html.p("gurk")

	css.applystylesheets(e, media="screen")

	assert str(e.walknodes(html.p)[0].attrs.style) == "color: red;"

	# Check that media="screen" doesn't pick up the print stylesheet
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style("p {color: red;}", type="text/css", media="screen")
			with html.body():
				+html.p("gurk")

	css.applystylesheets(e, media="print")

	assert str(e.walknodes(html.p)[0].attrs.style) == ""

	# Check that @media rules are treated properly
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style("@media screen { p {color: red;}}", type="text/css")
			with html.body():
				+html.p("gurk")

	css.applystylesheets(e, media="screen")

	assert str(e.walknodes(html.p)[0].attrs.style) == "color: red;"

	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style("@media screen { p {color: red;}}", type="text/css")
			with html.body():
				+html.p("gurk")

	css.applystylesheets(e, media="print")

	assert str(e.walknodes(html.p)[0].attrs.style) == ""


def test_applystylesheets_title():
	def makenode():
		with xsc.build():
			with html.html() as e:
				with html.head():
					+html.style("p {color: red;}", type="text/css")
					+html.style("p {color: blue;}", type="text/css", title="blue")
				with html.body():
					+html.p("gurk")
		return e

	# Check that title=None uses only the titleless stylesheets
	e = makenode()
	css.applystylesheets(e, title=None)
	assert str(e.walknodes(html.p)[0].attrs.style) == "color: red;"

	# Check that title="blue" uses only the stylesheet with the specified title
	e = makenode()
	css.applystylesheets(e, title="blue")
	assert str(e.walknodes(html.p)[0].attrs.style) == "color: blue;"


def test_parse():
	s = css.parsestring(b"@charset 'utf-8'; div{background-image: url(gurk.gif);}")
	urls = set(css.geturls(s))
	assert urls == {url.URL("gurk.gif")}

	s = css.parsestring(b"@charset 'utf-8'; div{background-image: url(gurk.gif);}", base="root:")
	urls = set(css.geturls(s))
	assert urls == {url.URL("root:gurk.gif")}


def test_comments():
	d = b'<html><head><style type="text/css">/*nix*/ p{/*nix*/ color: red;}</style></head><body><p>gurk</p></body></html>'
	node = parse.tree(d, parse.Expat(), parse.NS(html), parse.Node())
	css.applystylesheets(node)
	assert str(node.walknodes(html.p)[0].attrs.style) == "color: red;"
