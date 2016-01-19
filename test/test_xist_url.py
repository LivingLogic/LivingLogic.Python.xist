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
from ll.xist import xsc, parse
from ll.xist.ns import specials, html, jsp


def test_url(recwarn):
	# The ``recwarn`` argument silences the ``RequiredAttrMissingWarning``
	node = parse.tree(b"<?url root:images/gurk.gif?>", parse.SGMLOP(), parse.NS(html), parse.Node())
	assert node.bytes(base="root:about/us.html") == b"../images/gurk.gif"

	node = parse.tree(b'<img src="root:images/gurk.gif"/>', parse.Expat(), parse.NS(html), parse.Node())
	assert node.bytes(base="root:about/us.html") == b'<img src="../images/gurk.gif" />'


def test_fancyurl():
	node = html.a("gurk", href=("http://", jsp.expression("server")))
	assert node.bytes(base="root:about/us.html") == b'<a href="http://<%= server %>">gurk</a>'


def test_replaceurls():
	node = html.div("gurk", style="background-image: url(gurk.gif);")
	node.attrs.style.replaceurls(lambda u: url.URL("http://www.example.org")/u)
	assert str(node.attrs.style) == "background-image: url(http://www.example.org/gurk.gif)"
