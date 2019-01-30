#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


from ll.xist import xsc, parse
from ll.xist.ns import html, xml, php, abbr, xlink, specials, struts_html


def test_publishelement():
	node = html.html()

	assert node.bytes(prefixdefault=False) == b"""<html></html>"""
	assert node.bytes(prefixdefault=None) == b"""<html xmlns="http://www.w3.org/1999/xhtml"></html>"""
	assert node.bytes(prefixdefault="h") == b"""<h:html xmlns:h="http://www.w3.org/1999/xhtml"></h:html>"""
	assert node.bytes(prefixdefault=True) == b"""<ns:html xmlns:ns="http://www.w3.org/1999/xhtml"></ns:html>"""
	assert node.bytes(prefixes={html: False}) == b"""<html></html>"""
	assert node.bytes(prefixes={html: None}) == b"""<html xmlns="http://www.w3.org/1999/xhtml"></html>"""
	assert node.bytes(prefixes={html: "h"}) == b"""<h:html xmlns:h="http://www.w3.org/1999/xhtml"></h:html>"""
	assert node.bytes(prefixes={html: True}) == b"""<ns:html xmlns:ns="http://www.w3.org/1999/xhtml"></ns:html>"""
	assert node.bytes(prefixdefault="h", hidexmlns=[html]) == b"""<h:html></h:html>"""


def test_publishentity():
	node = abbr.xml()

	assert node.bytes(prefixdefault=False) == b"""&xml;"""
	assert node.bytes(prefixdefault=None) == b"""&xml;"""
	assert node.bytes(prefixdefault="x") == b"""&xml;"""
	assert node.bytes(prefixdefault=True) == b"""&xml;"""
	assert node.bytes(prefixes={abbr: False}) == b"""&xml;"""
	assert node.bytes(prefixes={abbr: None}) == b"""&xml;"""
	assert node.bytes(prefixes={abbr: "x"}) == b"""&xml;"""
	assert node.bytes(prefixes={abbr: True}) == b"""&xml;"""


def test_publishprocinst():
	node = php.php("x")

	assert node.bytes(prefixdefault=False) == b"""<?php x?>"""
	assert node.bytes(prefixdefault=None) == b"""<?php x?>"""
	assert node.bytes(prefixdefault="p") == b"""<?php x?>"""
	assert node.bytes(prefixdefault=True) == b"""<?php x?>"""
	assert node.bytes(prefixes={php: False}) == b"""<?php x?>"""
	assert node.bytes(prefixes={php: None}) == b"""<?php x?>"""
	assert node.bytes(prefixes={php: "p"}) == b"""<?php x?>"""
	assert node.bytes(prefixes={php: True}) == b"""<?php x?>"""


def test_publishboolattr():
	node = html.td("?", nowrap=None)
	assert node.bytes(xhtml=0) == b"""<td>?</td>"""

	node = html.td("?", nowrap=True)
	assert node.bytes(xhtml=0) == b"""<td nowrap>?</td>"""
	assert node.bytes(xhtml=1) == b"""<td nowrap="nowrap">?</td>"""
	assert node.bytes(xhtml=2) == b"""<td nowrap="nowrap">?</td>"""

	class foo(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class bar(xsc.BoolAttr):
				xmlname = "baz"

	# Check that the XML name is used as the value
	assert foo("?", bar=True).bytes(xhtml=2) == b"""<foo baz="baz">?</foo>"""


def test_publishurlattr():
	node = html.link(href=None)
	assert node.bytes(xhtml=1) == b"""<link />"""

	node = html.link(href="root:gurk.html")
	assert node.bytes(xhtml=1) == b"""<link href="root:gurk.html" />"""
	assert node.bytes(xhtml=1, base="root:gurk.html") == b"""<link href="" />"""
	assert node.bytes(xhtml=1, base="root:hurz.html") == b"""<link href="gurk.html" />"""


def test_publishstyleattr():
	node = html.div(style=None)
	assert node.bytes(xhtml=1) == b"""<div></div>"""

	node = html.div(style="background-image: url(root:gurk.html)")
	assert node.bytes(xhtml=1) == b"""<div style="background-image: url(root:gurk.html)"></div>"""
	assert node.bytes(xhtml=1, base="root:gurk.html") == b"""<div style="background-image: url()"></div>"""
	assert node.bytes(xhtml=1, base="root:hurz.html") == b"""<div style="background-image: url(gurk.html)"></div>"""


def test_publishxmlattr():
	node = html.html(xml.Attrs(space="preserve"))
	assert node.bytes(prefixdefault=False) == b"""<html xml:space="preserve"></html>"""
	assert node.bytes(prefixdefault=True) == b"""<ns:html xmlns:ns="http://www.w3.org/1999/xhtml" xml:space="preserve"></ns:html>"""
	assert node.bytes(prefixdefault=None) == b"""<html xmlns="http://www.w3.org/1999/xhtml" xml:space="preserve"></html>"""
	assert node.bytes(prefixes={html: "h"}) == b"""<h:html xmlns:h="http://www.w3.org/1999/xhtml" xml:space="preserve"></h:html>"""
	# Prefix for XML namespace can't be overwritten
	assert node.bytes(prefixes={html: "h", xml: "spam"}) == b"""<h:html xmlns:h="http://www.w3.org/1999/xhtml" xml:space="preserve"></h:html>"""


def test_publishglobalattr():
	# FIXME: Some of those tests depend on dict iteration order
	node = html.html(xlink.Attrs(title="the foo bar"))
	assert node.bytes(prefixdefault=False) == b"""<html xmlns:ns="http://www.w3.org/1999/xlink" ns:title="the foo bar"></html>"""
	assert node.bytes(prefixdefault=None) == b"""<html xmlns="http://www.w3.org/1999/xhtml" xmlns:ns="http://www.w3.org/1999/xlink" ns:title="the foo bar"></html>"""
	assert node.bytes(prefixdefault=True) == b"""<ns:html xmlns:ns="http://www.w3.org/1999/xhtml" xmlns:ns2="http://www.w3.org/1999/xlink" ns2:title="the foo bar"></ns:html>"""
	assert node.bytes(prefixdefault="h") == b"""<h:html xmlns:h="http://www.w3.org/1999/xhtml" xmlns:ns="http://www.w3.org/1999/xlink" ns:title="the foo bar"></h:html>"""
	assert node.bytes(prefixes={html: "h", xlink: "xl"}) == b"""<h:html xmlns:h="http://www.w3.org/1999/xhtml" xmlns:xl="http://www.w3.org/1999/xlink" xl:title="the foo bar"></h:html>"""


def test_publishspecialsurl():
	node = specials.url("root:gurk.html")
	assert node.bytes() == b"""root:gurk.html"""
	assert node.bytes(base="root:gurk.html") == b""""""
	assert node.bytes(base="root:hurz.html") == b"""gurk.html"""


def test_publishempty():
	node = xsc.Frag(html.br(), html.div())
	assert node.bytes(xhtml=0) == b"""<br><div></div>"""
	assert node.bytes(xhtml=1) == b"""<br /><div></div>"""
	assert node.bytes(xhtml=2) == b"""<br/><div/>"""


def test_publishescaped():
	s = """\x04<&'"\xff>"""
	node = xsc.Text(s)
	assert node.bytes(encoding="ascii") == b"""&#4;&lt;&amp;'"&#255;&gt;"""
	node = html.span(class_=s)
	assert node.bytes(encoding="ascii", xhtml=2) == b"""<span class="&#4;&lt;&amp;'&quot;&#255;&gt;"/>"""


def test_encoding():
	def check(encoding):
		node = xsc.Frag(
			html.div(
				php.php("echo $foo"),
				abbr.html(),
				html.div("gurk", class_="hurz"),
				"\u3042",
			)
		)
		s = node.bytes(encoding=encoding)
		node2 = parse.tree(s, parse.Expat(), parse.NS(html), xsc.Pool(html, php, abbr))
		assert node == node2

	for encoding in ("utf-8", "utf-16", "utf-16-be", "utf-16-le", "latin-1", "ascii"):
		check(encoding)


def test_xmlheader():
	assert xml.XML().bytes(encoding="utf-8") == b'<?xml version="1.0" encoding="utf-8"?>'
	assert xml.XML().bytes(encoding="latin-1") == b'<?xml version="1.0" encoding="latin-1"?>'
	assert html.div(xml.XML()).bytes(encoding="latin-1") == b'<div><?xml version="1.0" encoding="latin-1"?></div>'


def test_struts_html():
	assert b'prefix="xyzzx"' in struts_html.taglib().bytes(prefixdefault="xyzzx")


def test_publish_forcexmlns():
	e = html.html()
	s = e.string(prefixes={html: "h", specials: "s"}, showxmlns=[specials])
	assert f'xmlns:s="{specials.xmlns}"' in s


def test_comment_in_attr():
	node = html.div(class_=xsc.Comment("gurk"))
	assert node.bytes() == b"""<div class=""></div>"""


def test_doctype_in_attr():
	node = html.div(class_=html.DocTypeXHTML11())
	assert node.bytes() == b"""<div class=""></div>"""


def test_attribute_order():
	node = html.div(xml.Attrs(lang="de"), id="id42", align="right", class_="foo")
	assert node.bytes() == b"""<div xml:lang="de" id="id42" align="right" class="foo"></div>"""


def test_allowschemerelurls():
	node = html.a(href="http://www.example.org/index.html")
	assert node.bytes() == b'<a href="http://www.example.org/index.html"></a>'
	assert node.bytes(base="http://www.example.org") == b'<a href="index.html"></a>'
	assert node.bytes(base="http://www.example.com") == b'<a href="http://www.example.org/index.html"></a>'
	assert node.bytes(base="http://www.example.com", allowschemerelurls=True) == b'<a href="//www.example.org/index.html"></a>'

	node = specials.url("http://www.example.org/index.html")
	assert node.bytes() == b'http://www.example.org/index.html'
	assert node.bytes(base="http://www.example.org") == b'index.html'
	assert node.bytes(base="http://www.example.com") == b'http://www.example.org/index.html'
	assert node.bytes(base="http://www.example.com", allowschemerelurls=True) == b'//www.example.org/index.html'

	node = html.span(style="background: url(http://www.example.org/index.html)")
	assert node.bytes() == b'<span style="background: url(http://www.example.org/index.html)"></span>'
	assert node.bytes(base="http://www.example.org") == b'<span style="background: url(index.html)"></span>'
	assert node.bytes(base="http://www.example.com") == b'<span style="background: url(http://www.example.org/index.html)"></span>'
	assert node.bytes(base="http://www.example.com", allowschemerelurls=True) == b'<span style="background: url(//www.example.org/index.html)"></span>'
