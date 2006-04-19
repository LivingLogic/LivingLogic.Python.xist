#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


import sys, re

from ll.xist import xsc, helpers, parsers
from ll.xist.ns import html, xml, php, abbr, xlink, specials


# The following includes \x00 in addition to those characters defined in
# http://www.w3.org/TR/2004/REC-xml11-20040204/#NT-RestrictedChar
restrictedchars = re.compile(u"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]")


def test_publishelement():
	node = html.html()

	prefixes = xsc.Prefixes(h=html)
	assert node.asBytes(prefixes=prefixes, prefixmode=0) == """<html></html>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=1) == """<h:html></h:html>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=2) == """<h:html xmlns:h="http://www.w3.org/1999/xhtml"></h:html>"""

	prefixes = xsc.Prefixes(html)
	assert node.asBytes(prefixes=prefixes, prefixmode=0) == """<html></html>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=1) == """<html></html>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=2) == """<html xmlns="http://www.w3.org/1999/xhtml"></html>"""


def test_publishentity():
	node = abbr.xml()

	prefixes = xsc.Prefixes(a=abbr, s=specials)
	assert node.asBytes(prefixes=prefixes, prefixmode=0) == """&xml;"""
	assert node.asBytes(prefixes=prefixes, prefixmode=1) == """&xml;"""
	assert node.asBytes(prefixes=prefixes, prefixmode=2) == """&xml;"""

	prefixes = xsc.Prefixes(abbr, s=specials)
	assert node.asBytes(prefixes=prefixes, prefixmode=0) == """&xml;"""
	assert node.asBytes(prefixes=prefixes, prefixmode=1) == """&xml;"""
	assert node.asBytes(prefixes=prefixes, prefixmode=2) == """&xml;"""


def test_publishprocinst():
	node = php.php("x")

	prefixes = xsc.Prefixes(p=php, s=specials)
	assert node.asBytes(prefixes=prefixes, prefixmode=0) == """<?php x?>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=1) == """<?php x?>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=2) == """<?php x?>"""

	prefixes = xsc.Prefixes(php, s=specials)
	assert node.asBytes(prefixes=prefixes, prefixmode=0) == """<?php x?>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=1) == """<?php x?>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=2) == """<?php x?>"""


def test_publishboolattr():
	node = html.td("?", nowrap=None)
	assert node.asBytes(xhtml=0) == """<td>?</td>"""

	node = html.td("?", nowrap=True)
	assert node.asBytes(xhtml=0) == """<td nowrap>?</td>"""
	assert node.asBytes(xhtml=1) == """<td nowrap="nowrap">?</td>"""
	assert node.asBytes(xhtml=2) == """<td nowrap="nowrap">?</td>"""

	class foo(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class bar(xsc.BoolAttr):
				xmlname = "baz"

	assert foo("?", bar=True).asBytes(xhtml=2) == """<foo baz="baz">?</foo>"""


def test_publishurlattr():
	node = html.link(href=None)
	assert node.asBytes(xhtml=1) == """<link />"""

	node = html.link(href="root:gurk.html")
	assert node.asBytes(xhtml=1) == """<link href="root:gurk.html" />"""
	assert node.asBytes(xhtml=1, base="root:gurk.html") == """<link href="" />"""
	assert node.asBytes(xhtml=1, base="root:hurz.html") == """<link href="gurk.html" />"""


def test_publishstyleattr():
	node = html.div(style=None)
	assert node.asBytes(xhtml=1) == """<div></div>"""

	node = html.div(style="background-image: url(root:gurk.html)")
	assert node.asBytes(xhtml=1) == """<div style="background-image: url(root:gurk.html)"></div>"""
	assert node.asBytes(xhtml=1, base="root:gurk.html") == """<div style="background-image: url()"></div>"""
	assert node.asBytes(xhtml=1, base="root:hurz.html") == """<div style="background-image: url(gurk.html)"></div>"""


def test_publishxmlattr():
	node = html.html(xml.Attrs(space="preserve"))
	prefixes = xsc.Prefixes(h=html)
	assert node.asBytes(prefixes=prefixes, prefixmode=0) == """<html xml:space="preserve"></html>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=1) == """<h:html xml:space="preserve"></h:html>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=2) == """<h:html xmlns:h="http://www.w3.org/1999/xhtml" xml:space="preserve"></h:html>"""


def test_publishglobalattr():
	node = html.html(xlink.Attrs(title="the foo bar"))
	prefixes = xsc.Prefixes(h=html, xl=xlink)
	assert node.asBytes(prefixes=prefixes, prefixmode=0) == """<html xmlns:xl="http://www.w3.org/1999/xlink" xl:title="the foo bar"></html>"""
	assert node.asBytes(prefixes=prefixes, prefixmode=1) == """<h:html xmlns:xl="http://www.w3.org/1999/xlink" xl:title="the foo bar"></h:html>"""
	# FIXME: this depends on dict iteration order
	assert node.asBytes(prefixes=prefixes, prefixmode=2) == """<h:html xmlns:xl="http://www.w3.org/1999/xlink" xmlns:h="http://www.w3.org/1999/xhtml" xl:title="the foo bar"></h:html>"""


def test_publishempty():
	node = xsc.Frag(html.br(), html.div())
	assert node.asBytes(xhtml=0) == """<br><div></div>"""
	assert node.asBytes(xhtml=1) == """<br /><div></div>"""
	assert node.asBytes(xhtml=2) == """<br/><div/>"""


def test_publishescaped():
	s = u"""<&'"\xff>"""
	node = xsc.Text(s)
	assert node.asBytes(encoding="ascii") == """&lt;&amp;'"&#255;&gt;"""
	node = html.span(class_=s)
	assert node.asBytes(encoding="ascii", xhtml=2) == """<span class="&lt;&amp;'&quot;&#255;&gt;"/>"""


escapeInput = u"".join([unichr(i) for i in xrange(1000)] + [unichr(i) for i in xrange(sys.maxunicode-10, sys.maxunicode+1)])


def test_helpersescapetext():
	escapeOutput = []
	for c in escapeInput:
		if c==u"&":
			escapeOutput.append(u"&amp;")
		elif c==u"<":
			escapeOutput.append(u"&lt;")
		elif c==u">":
			escapeOutput.append(u"&gt;")
		elif restrictedchars.match(c) is not None:
			escapeOutput.append(u"&#%d;" % ord(c))
		else:
			escapeOutput.append(c)
	escapeOutput = "".join(escapeOutput)
	assert helpers.escapetext(escapeInput) == escapeOutput


def test_helpersescapeattr():
	escapeOutput = []
	for c in escapeInput:
		if c==u"&":
			escapeOutput.append(u"&amp;")
		elif c==u"<":
			escapeOutput.append(u"&lt;")
		elif c==u">":
			escapeOutput.append(u"&gt;")
		elif c==u'"':
			escapeOutput.append(u"&quot;")
		elif restrictedchars.match(c) is not None:
			escapeOutput.append(u"&#%d;" % ord(c))
		else:
			escapeOutput.append(c)
	escapeOutput = "".join(escapeOutput)
	assert helpers.escapeattr(escapeInput) == escapeOutput


def test_helpercssescapereplace():
	escapeOutput = []
	for c in escapeInput:
		try:
			c.encode("ascii")
			escapeOutput.append(c)
		except UnicodeError:
			escapeOutput.append((u"\\%x" % ord(c)).upper())
	escapeOutput = u"".join(escapeOutput)
	assert helpers.cssescapereplace(escapeInput, "ascii") == escapeOutput


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
		s = node.asBytes(encoding=encoding)
		node2 = parsers.parseString(
			s,
			saxparser=parsers.ExpatParser,
			prefixes=xsc.Prefixes([html, php, abbr]),
		)
		assert node == node2

	for encoding in ("utf-8", "utf-16", "utf-16-be", "utf-16-le", "latin-1", "ascii"):
		yield check, encoding
