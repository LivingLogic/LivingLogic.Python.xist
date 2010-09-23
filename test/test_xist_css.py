#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll import url
from ll.xist import xsc, css, parse
from ll.xist.ns import html, specials


def test_css():
	with xsc.build():
		with html.div(id=1) as e:
			with html.ul(id=2):
				+html.li(u"foo")
				+html.li()

	assert list(e.walknodes(css.selector(u"div"))) == [e]
	assert list(e.walknodes(css.selector(u"li"))) == [e[0][0], e[0][1]]
	assert list(e.walknodes(css.selector(u"div#1"))) == [e]
	assert list(e.walknodes(css.selector(u"#2"))) == [e[0]]
	assert list(e.walknodes(css.selector(u":empty"))) == [e[0][1]]
	assert list(e.walknodes(css.selector(u"li:empty"))) == [e[0][1]]
	assert list(e.walknodes(css.selector(u"div :empty"))) == [e[0][1]]
	assert list(e.walknodes(css.selector(u"div>*:empty"))) == []
	assert list(e.walknodes(css.selector(u"div>:empty"))) == []
	assert list(e.walknodes(css.selector(u"*|li"))) == [e[0][0], e[0][1]]
	assert list(e.walknodes(css.selector(u"h|li", prefixes={u"h": html}))) == [e[0][0], e[0][1]]
	assert list(e.walknodes(css.selector(u"h|li", prefixes={u"h": specials}))) == []

	with xsc.build():
		with xsc.Frag() as e:
			+html.div(u"foo")
			+xsc.Text(u"filler")
			+html.p(u"foo")
			+xsc.Text(u"filler")
			+html.ul(html.li(u"foo"))

	assert list(e.walknodes(css.selector(u"div + p"))) == [e[2]]
	assert list(e.walknodes(css.selector(u"div + ul"))) == []
	assert list(e.walknodes(css.selector(u"ul + p"))) == []
	assert list(e.walknodes(css.selector(u"div ~ p"))) == [e[2]]
	assert list(e.walknodes(css.selector(u"div ~ ul"))) == [e[4]]
	assert list(e.walknodes(css.selector(u"p ~ div"))) == []
	assert list(e.walknodes(css.selector(u"div:first-child + p"))) == [e[2]]
	assert list(e.walknodes(css.selector(u"*:first-child + p"))) == [e[2]]

	with xsc.build():
		with xsc.Frag() as e:
			+html.span(html.b(u"hurz"), u"gurk", html.em(u"hinz"), html.em(u"kunz"))
			+html.em(u"hurz")
			+html.em(u"hinz")
			+xsc.Text(u"nix")
			+html.i(u"kunz")

	assert list(e.walknodes(css.selector(u"*:only-of-type"))) == [e[0], e[0][0], e[4]]
	assert list(e.walknodes(css.selector(u"*:nth-child(1)"))) == [e[0], e[0][0]]
	assert list(e.walknodes(css.selector(u"*:nth-child(2)"))) == [e[0][2], e[1]]
	assert list(e.walknodes(css.selector(u"*:nth-last-child(1)"))) == [e[0][3], e[4]]
	assert list(e.walknodes(css.selector(u"*:nth-last-child(2)"))) == [e[0][2], e[2]]
	assert list(e.walknodes(css.selector(u"*:nth-of-type(1)"))) == [e[0], e[0][0], e[0][2], e[1], e[4]]
	assert list(e.walknodes(css.selector(u"*:nth-of-type(2)"))) == [e[0][3], e[2]]
	assert list(e.walknodes(css.selector(u"*:nth-last-of-type(1)"))) == [e[0], e[0][0], e[0][3], e[2], e[4]]
	assert list(e.walknodes(css.selector(u"*:nth-last-of-type(2)"))) == [e[0][2], e[1]]

	e = xsc.Frag(html.span(html.b(u"hurz"), u"gurk"))
	assert list(e.walknodes(css.selector(u"*:only-child"))) == [e[0], e[0][0]]

	with xsc.build():
		with xsc.Frag() as e:
			+html.em(class_=u"gurk", lang=u"en")
			+html.em(class_=u"gurk hurz", lang=u"en-us")
			+html.em(class_=u"hurz", lang=u"de")

	assert list(e.walknodes(css.selector(u"em[class='gurk']"))) == [e[0]]
	assert list(e.walknodes(css.selector(u"em[class~='gurk']"))) == [e[0], e[1]]
	assert list(e.walknodes(css.selector(u"em[lang|='en']"))) == [e[0], e[1]]


def test_applystylesheets1():
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style(u"p {color: red;}", type=u"text/css")
			with html.body():
				+html.p(u"gurk")

	css.applystylesheets(e)

	assert unicode(e.walknodes(html.p)[0].attrs.style) == u"color: red;"
	assert list(e.walknodes(html.style)) == []


def test_applystylesheets2():
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style(u"p.dont {color: red;}", type=u"text/css")
			with html.body():
				+html.p(u"gurk")

	css.applystylesheets(e)

	assert unicode(e.walknodes(html.p)[0].attrs.style) == u""
	assert list(e.walknodes(html.style)) == []


def test_applystylesheets3():
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style(u"p.do {color: red;}", type=u"text/css")
			with html.body():
				+html.p(u"gurk", class_=u"do")

	css.applystylesheets(e)

	assert unicode(e.walknodes(html.p)[0].attrs.style) == u"color: red;"
	assert list(e.walknodes(html.style)) == []


def test_applystylesheets4():
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style(u"#id42 {color: red;}", type=u"text/css")
			with html.body():
				+html.p(u"gurk", id=u"id42", style=u"color: blue;")

	css.applystylesheets(e)

	# style attribute wins
	assert unicode(e.walknodes(html.p)[0].attrs.style) == u"color: blue;"
	assert list(e.walknodes(html.style)) == []


def test_applystylesheets5():
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style(u"p#id42 {color: red;}", type=u"text/css")
			with html.body():
				+html.p(u"gurk", id=u"id42", style=u"color: blue;")

	css.applystylesheets(e)

	# stylesheet always wins (at least in CSS 2.1 and 3)
	assert unicode(e.walknodes(html.p)[0].attrs.style) == u"color: blue;"
	assert list(e.walknodes(html.style)) == []


def test_applystylesheets_media():
	# Check that media="screen" picks up the media stylesheet
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style(u"p {color: red;}", type=u"text/css", media=u"screen")
			with html.body():
				+html.p(u"gurk")

	css.applystylesheets(e, media=u"screen")

	assert unicode(e.walknodes(html.p)[0].attrs.style) == u"color: red;"

	# Check that media="screen" doesn't pick up the print stylesheet
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style(u"p {color: red;}", type=u"text/css", media=u"screen")
			with html.body():
				+html.p(u"gurk")

	css.applystylesheets(e, media=u"print")

	assert unicode(e.walknodes(html.p)[0].attrs.style) == u""

	# Check that @media rules are treated properly
	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style(u"@media screen { p {color: red;}}", type=u"text/css")
			with html.body():
				+html.p(u"gurk")

	css.applystylesheets(e, media=u"screen")

	assert unicode(e.walknodes(html.p)[0].attrs.style) == u"color: red;"

	with xsc.build():
		with html.html() as e:
			with html.head():
				+html.style(u"@media screen { p {color: red;}}", type=u"text/css")
			with html.body():
				+html.p(u"gurk")

	css.applystylesheets(e, media=u"print")

	assert unicode(e.walknodes(html.p)[0].attrs.style) == u""


def test_applystylesheets_title():
	def makenode():
		with xsc.build():
			with html.html() as e:
				with html.head():
					+html.style(u"p {color: red;}", type=u"text/css")
					+html.style(u"p {color: blue;}", type=u"text/css", title=u"blue")
				with html.body():
					+html.p(u"gurk")
		return e

	# Check that title=None uses only the titleless stylesheets
	e = makenode()
	css.applystylesheets(e, title=None)
	assert unicode(e.walknodes(html.p)[0].attrs.style) == u"color: red;"

	# Check that title="blue" uses only the stylesheet with the specified title
	e = makenode()
	css.applystylesheets(e, title=u"blue")
	assert str(e.walknodes(html.p)[0].attrs.style) == u"color: blue;"


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
	assert unicode(node.walknodes(html.p)[0].attrs.style) == u"color: red;"
