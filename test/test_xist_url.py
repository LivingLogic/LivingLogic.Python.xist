#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import py.test

from ll import url
from ll.xist import xsc, parsers
from ll.xist.ns import specials, html, jsp


def test_url():
	node = parsers.parsestring("<?url root:images/gurk.gif?>", parser=parsers.SGMLOPParser())
	assert node.bytes(base="root:about/us.html") == "../images/gurk.gif"

	node = parsers.parsestring('<img src="root:images/gurk.gif"/>')
	assert node.bytes(base="root:about/us.html") == '<img src="../images/gurk.gif" />'


def test_fancyurl():	
	node = html.a("gurk", href=("http://", jsp.expression("server")))
	assert node.bytes(base="root:about/us.html") == '<a href="http://<%= server %>">gurk</a>'


def test_replaceurls():	
	node = html.div("gurk", style="background-image: url(gurk.gif);")
	node.attrs.style.replaceurls(lambda u: url.URL("http://www.example.org")/u)
	assert str(node.attrs.style) == "background-image: url(http://www.example.org/gurk.gif)"
