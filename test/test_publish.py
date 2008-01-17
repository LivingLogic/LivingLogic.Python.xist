#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


import sys, re

from ll.xist import xsc, helpers, parsers
from ll.xist.ns import html, xml, php, abbr, xlink, specials, struts_html


# The following includes \x00 in addition to those characters defined in
# http://www.w3.org/TR/2004/REC-xml11-20040204/#NT-RestrictedChar
restrictedchars = re.compile(u"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]")


def test_publishelement():
	node = html.html()

	assert node.bytes(prefixdefault=False) == """<html></html>"""
	assert node.bytes(prefixdefault=None) == """<html xmlns="http://www.w3.org/1999/xhtml"></html>"""
	assert node.bytes(prefixdefault="h") == """<h:html xmlns:h="http://www.w3.org/1999/xhtml"></h:html>"""
	assert node.bytes(prefixdefault=True) == """<ns:html xmlns:ns="http://www.w3.org/1999/xhtml"></ns:html>"""
	assert node.bytes(prefixes={html: False}) == """<html></html>"""
	assert node.bytes(prefixes={html: None}) == """<html xmlns="http://www.w3.org/1999/xhtml"></html>"""
	assert node.bytes(prefixes={html: "h"}) == """<h:html xmlns:h="http://www.w3.org/1999/xhtml"></h:html>"""
	assert node.bytes(prefixes={html: True}) == """<ns:html xmlns:ns="http://www.w3.org/1999/xhtml"></ns:html>"""
	assert node.bytes(prefixdefault="h", hidexmlns=[html]) == """<h:html></h:html>"""


def test_publishentity():
	node = abbr.xml()

	assert node.bytes(prefixdefault=False) == """&xml;"""
	assert node.bytes(prefixdefault=None) == """&xml;"""
	assert node.bytes(prefixdefault="x") == """&xml;"""
	assert node.bytes(prefixdefault=True) == """&xml;"""
	assert node.bytes(prefixes={abbr: False}) == """&xml;"""
	assert node.bytes(prefixes={abbr: None}) == """&xml;"""
	assert node.bytes(prefixes={abbr: "x"}) == """&xml;"""
	assert node.bytes(prefixes={abbr: True}) == """&xml;"""


def test_publishprocinst():
	node = php.php("x")

	assert node.bytes(prefixdefault=False) == """<?php x?>"""
	assert node.bytes(prefixdefault=None) == """<?php x?>"""
	assert node.bytes(prefixdefault="p") == """<?php x?>"""
	assert node.bytes(prefixdefault=True) == """<?php x?>"""
	assert node.bytes(prefixes={php: False}) == """<?php x?>"""
	assert node.bytes(prefixes={php: None}) == """<?php x?>"""
	assert node.bytes(prefixes={php: "p"}) == """<?php x?>"""
	assert node.bytes(prefixes={php: True}) == """<?php x?>"""


def test_publishboolattr():
	node = html.td("?", nowrap=None)
	assert node.bytes(xhtml=0) == """<td>?</td>"""

	node = html.td("?", nowrap=True)
	assert node.bytes(xhtml=0) == """<td nowrap>?</td>"""
	assert node.bytes(xhtml=1) == """<td nowrap="nowrap">?</td>"""
	assert node.bytes(xhtml=2) == """<td nowrap="nowrap">?</td>"""

	class foo(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class bar(xsc.BoolAttr):
				xmlname = "baz"

	# Check that the XML name is used as the value
	assert foo("?", bar=True).bytes(xhtml=2) == """<foo baz="baz">?</foo>"""


def test_publishurlattr():
	node = html.link(href=None)
	assert node.bytes(xhtml=1) == """<link />"""

	node = html.link(href="root:gurk.html")
	assert node.bytes(xhtml=1) == """<link href="root:gurk.html" />"""
	assert node.bytes(xhtml=1, base="root:gurk.html") == """<link href="" />"""
	assert node.bytes(xhtml=1, base="root:hurz.html") == """<link href="gurk.html" />"""


def test_publishstyleattr():
	node = html.div(style=None)
	assert node.bytes(xhtml=1) == """<div></div>"""

	node = html.div(style="background-image: url(root:gurk.html)")
	assert node.bytes(xhtml=1) == """<div style="background-image: url(root:gurk.html)"></div>"""
	assert node.bytes(xhtml=1, base="root:gurk.html") == """<div style="background-image: url()"></div>"""
	assert node.bytes(xhtml=1, base="root:hurz.html") == """<div style="background-image: url(gurk.html)"></div>"""


def test_publishxmlattr():
	node = html.html(xml.Attrs(space="preserve"))
	assert node.bytes(prefixdefault=False) == """<html xml:space="preserve"></html>"""
	assert node.bytes(prefixdefault=True) == """<ns:html xmlns:ns="http://www.w3.org/1999/xhtml" xml:space="preserve"></ns:html>"""
	assert node.bytes(prefixdefault=None) == """<html xmlns="http://www.w3.org/1999/xhtml" xml:space="preserve"></html>"""
	assert node.bytes(prefixes={html: "h"}) == """<h:html xmlns:h="http://www.w3.org/1999/xhtml" xml:space="preserve"></h:html>"""
	# Prefix for XML namespace can't be overwritten
	assert node.bytes(prefixes={html: "h", xml: "spam"}) == """<h:html xmlns:h="http://www.w3.org/1999/xhtml" xml:space="preserve"></h:html>"""


def test_publishglobalattr():
	# FIXME: Some of those tests depend on dict iteration order
	node = html.html(xlink.Attrs(title="the foo bar"))
	assert node.bytes(prefixdefault=False) == """<html xmlns:ns="http://www.w3.org/1999/xlink" ns:title="the foo bar"></html>"""
	assert node.bytes(prefixdefault=None) == """<html xmlns="http://www.w3.org/1999/xhtml" xmlns:ns="http://www.w3.org/1999/xlink" ns:title="the foo bar"></html>"""
	assert node.bytes(prefixdefault=True) == """<ns:html xmlns:ns="http://www.w3.org/1999/xhtml" xmlns:ns2="http://www.w3.org/1999/xlink" ns2:title="the foo bar"></ns:html>"""
	assert node.bytes(prefixdefault="h") == """<h:html xmlns:h="http://www.w3.org/1999/xhtml" xmlns:ns="http://www.w3.org/1999/xlink" ns:title="the foo bar"></h:html>"""
	assert node.bytes(prefixes={html: "h", xlink: "xl"}) == """<h:html xmlns:h="http://www.w3.org/1999/xhtml" xmlns:xl="http://www.w3.org/1999/xlink" xl:title="the foo bar"></h:html>"""


def test_publishspecialsurl():
	node = specials.url("root:gurk.html")
	assert node.bytes() == """root:gurk.html"""
	assert node.bytes(base="root:gurk.html") == """"""
	assert node.bytes(base="root:hurz.html") == """gurk.html"""


def test_publishempty():
	node = xsc.Frag(html.br(), html.div())
	assert node.bytes(xhtml=0) == """<br><div></div>"""
	assert node.bytes(xhtml=1) == """<br /><div></div>"""
	assert node.bytes(xhtml=2) == """<br/><div/>"""


def test_publishescaped():
	s = u"""<&'"\xff>"""
	node = xsc.Text(s)
	assert node.bytes(encoding="ascii") == """&lt;&amp;'"&#255;&gt;"""
	node = html.span(class_=s)
	assert node.bytes(encoding="ascii", xhtml=2) == """<span class="&lt;&amp;'&quot;&#255;&gt;"/>"""


escape_input = u"".join([unichr(i) for i in xrange(1000)] + [unichr(i) for i in xrange(sys.maxunicode-10, sys.maxunicode+1)])


def test_helpersescapetext():
	escape_output = []
	for c in escape_input:
		if c==u"&":
			escape_output.append(u"&amp;")
		elif c==u"<":
			escape_output.append(u"&lt;")
		elif c==u">":
			escape_output.append(u"&gt;")
		elif restrictedchars.match(c) is not None:
			escape_output.append(u"&#%d;" % ord(c))
		else:
			escape_output.append(c)
	escape_output = "".join(escape_output)
	assert helpers.escapetext(escape_input) == escape_output


def test_helpersescapeattr():
	escape_output = []
	for c in escape_input:
		if c==u"&":
			escape_output.append(u"&amp;")
		elif c==u"<":
			escape_output.append(u"&lt;")
		elif c==u">":
			escape_output.append(u"&gt;")
		elif c==u'"':
			escape_output.append(u"&quot;")
		elif restrictedchars.match(c) is not None:
			escape_output.append(u"&#%d;" % ord(c))
		else:
			escape_output.append(c)
	escape_output = "".join(escape_output)
	assert helpers.escapeattr(escape_input) == escape_output


def test_helpercssescapereplace():
	escape_output = []
	for c in escape_input:
		try:
			c.encode("ascii")
			escape_output.append(c)
		except UnicodeError:
			escape_output.append((u"\\%x" % ord(c)).upper())
	escape_output = u"".join(escape_output)
	assert helpers.cssescapereplace(escape_input, "ascii") == escape_output


def test_encoding():
	def check(encoding):
		node = xsc.Frag(
			html.div(
				php.php("echo $foo"),
				abbr.html(),
				html.div("gurk", class_="hurz"),
				u"\u3042",
			)
		)
		s = node.bytes(encoding=encoding)
		node2 = parsers.parsestring(s, parser=parsers.ExpatParser(), prefixes={None: [html, php, abbr]})
		assert node == node2

	for encoding in ("utf-8", "utf-16", "utf-16-be", "utf-16-le", "latin-1", "ascii"):
		yield check, encoding


def test_xmlheader():
	assert xml.XML().bytes(encoding="utf-8") == '<?xml version="1.0" encoding="utf-8"?>'


def test_struts_html():
	assert 'prefix="xyzzx"' in struts_html.taglib().bytes(prefixdefault="xyzzx")
