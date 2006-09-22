#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2006 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


import warnings

import py.test

from xml import sax
from xml.parsers import expat

from ll import url
from ll.xist import xsc, parsers
from ll.xist.ns import chars, html, ihtml, specials, ruby


oldfilters = None


def raisesSAX(exception, func, *args, **kwargs):
	# assert that func(*args, **kwargs) raises exception either directly or wrapped in a SAXParseException
	try:
		func(*args, **kwargs)
	except exception:
		pass
	except sax.SAXParseException, exc:
		realexc = exc.getException()
		assert isinstance(realexc, exception)
	else:
		raise py.test.fail("exception not raised")


class __ns__(xsc.Namespace):
	xmlname = "foo"
	xmlurl = "http://www.foo.com/foo"
	class a(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class title(xsc.TextAttr): pass
	class foo(xsc.Entity):
		def __unicode__(self):
			return u"FOO"
	class bar(xsc.CharRef):
		codepoint = 0x42


def check_parseentities(source, result, **parseargs):
	node = parsers.parseString("""<a title="%s">%s</a>""" % (source, source), **parseargs)
	node = node.walknode(xsc.FindType(xsc.Element))[0]
	assert unicode(node) == result
	assert unicode(node["title"]) == result


def check_parsestrictentities(source, result, parserfactory):
	prefixes = xsc.Prefixes([__ns__, chars])
	check_parseentities(source, result, prefixes=prefixes, saxparser=parserfactory)

	warnings.filterwarnings("error", category=xsc.MalformedCharRefWarning)
	for bad in ("&", "&#x", "&&", "&#x;", "&#fg;", "&#999999999;", "&#;", "&#y;", "&#x;", "&#xy;"):
		raisesSAX((xsc.MalformedCharRefWarning, expat.ExpatError), check_parseentities, bad, u"", prefixes=prefixes, saxparser=parserfactory)
	raisesSAX(xsc.IllegalEntityError, check_parseentities, "&baz;", u"", prefixes=prefixes, saxparser=parserfactory)


def check_parsebadentities(parserfactory):
	prefixes = xsc.Prefixes([__ns__, chars])
	tests = [
		("&amp;", u"&"),
		("&amp;amp;", u"&amp;"),
		("x&foo;&bar;y", u"xFOO\x42y"),
		("x&foobar;y", u"x&foobar;y"),
		("&uuml;", u"ü"),
		("x&x", u"x&x"),
		("x&x;", u"x&x;"),
		("a&amp;b&lt;c&gt;d&quot;e&apos;f", u"a&b<c>d\"e'f"),
		("x&#;y", u"x&#;y"),
		("x&#32;y", u"x y"),
		("x&#x20;y", u"x y"),
		("x&#-32;y", u"x&#-32;y"),
		("x&#999999999;y", "x&#999999999;y"),
		("x&#xffffffff;y", "x&#xffffffff;y"),
		("x&#xffffffff;y", "x&#xffffffff;y"),
		("x&#xffffffff;y&#", "x&#xffffffff;y&#")
	]
	for (source, result) in tests:
		check_parseentities(source, result, prefixes=prefixes, saxparser=parserfactory)


class Test:
	def setup_method(self, method):
		global oldfilters
		oldfilters = warnings.filters[:]

	def teardown_method(self, method):
		warnings.filters = oldfilters

	def test_parselocationsgmlop(self):
		# Check that SGMLOP gets the location info right (at least the line numbers)
		node = parsers.parseString("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", saxparser=parsers.SGMLOPParser)
		assert len(node) == 1
		assert len(node[0]) == 1
		assert node[0][0].startloc.getSystemId() == "STRING"
		assert node[0][0].startloc.getLineNumber() == 1

	def test_parselocationexpat(self):
		# Check that expat gets the location info right
		node = parsers.parseString("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", saxparser=parsers.ExpatParser)
		assert len(node) == 1
		assert len(node[0]) == 1
		assert node[0][0].startloc.getSystemId() == "STRING"
		assert node[0][0].startloc.getLineNumber() == 1
		assert node[0][0].startloc.getColumnNumber() == 3

	def test_nsparse(self):
		# A prepopulated prefix mapping and xmlns attributes should work together
		xml = """
			<x:a>
				<x:a xmlns:x='http://www.w3.org/1999/xhtml'>
					<x:a xmlns:x='http://www.nttdocomo.co.jp/imode'>gurk</x:a>
				</x:a>
			</x:a>
		"""
		check = ihtml.a(
			html.a(
				ihtml.a(
					"gurk"
				)
			)
		)
		prefixes = xsc.Prefixes(x=ihtml)
		node = parsers.parseString(xml, prefixes=prefixes)
		node = node.walknode(xsc.FindType(xsc.Element))[0].compact() # get rid of the Frag and whitespace
		assert node == check

	def test_parseurls(self):
		# Check proper URL handling when parsing URLAttr or StyleAttr attributes
		prefixes = xsc.Prefixes(html)
		node = parsers.parseString('<a href="4.html" style="background-image: url(3.gif);"/>', base="root:1/2.html", prefixes=prefixes)
		assert str(node[0]["style"]) == "background-image: url(root:1/3.gif);"
		assert node[0]["style"].urls() == [url.URL("root:1/3.gif")]
		assert str(node[0]["href"]) == "root:1/4.html"
		assert node[0]["href"].forInput(root="gurk/hurz.html") == url.URL("gurk/1/4.html")

	def test_parserequiredattrs(self):
		# Parser should complain about required attributes that are missing
		class __ns__(xsc.Namespace):
			class Test(xsc.Element):
				class Attrs(xsc.Element.Attrs):
					class required(xsc.TextAttr): required = True

		prefixes = xsc.Prefixes(__ns__)
		node = parsers.parseString('<Test required="foo"/>', prefixes=prefixes)
		assert str(node[0]["required"]) == "foo"

		warnings.filterwarnings("error", category=xsc.RequiredAttrMissingWarning)
		raisesSAX(xsc.RequiredAttrMissingWarning, parsers.parseString, '<Test/>', prefixes=prefixes)

	def test_parsevalueattrs(self):
		# Parser should complain about attributes with illegal values, when a set of values is specified
		class __ns__(xsc.Namespace):
			class Test(xsc.Element):
				class Attrs(xsc.Element.Attrs):
					class withvalues(xsc.TextAttr): values = ("foo", "bar")

		prefixes = xsc.Prefixes(__ns__)

		node = parsers.parseString('<Test withvalues="bar"/>', prefixes=prefixes)
		assert str(node[0]["withvalues"]) == "bar"

		warnings.filterwarnings("error", category=xsc.IllegalAttrValueWarning)
		raisesSAX(xsc.IllegalAttrValueWarning, parsers.parseString, '<Test withvalues="baz"/>', prefixes=prefixes)

	def test_parsestrictentities_sgmlop(self):
		check_parsestrictentities(
			"a&amp;b&foo;&bar;c&#32;d&#x20;&#30000;;&lt;&gt;&quot;&apos;",
			u"""a&bFOO\x42c d %c;<>"'""" % 30000,
			parsers.SGMLOPParser
		)

	def test_parsestrictentities_expat(self):
		check_parsestrictentities(
			"a&amp;bc&#32;d&#x20;&#30000;;&lt;&gt;&quot;&apos;",
			u"""a&bc d %c;<>"'""" % 30000,
			parsers.ExpatParser
		)

	def test_parsebadentities_badentity(self):
		check_parsebadentities(parsers.BadEntityParser)

	def test_parsebadentities_html(self):
		check_parsebadentities(parsers.HTMLParser)

	def test_multipleparsecalls(self):
		def check(saxparser):
			p = parsers.Parser(saxparser=saxparser)
			for i in xrange(3):
				try:
					p.parseString("<>gurk")
				except Exception:
					pass
				for j in xrange(3):
					assert p.parseString("<a>gurk</a>").asBytes() == "<a>gurk</a>"

		# A Parser instance should be able to parse multiple XML sources, even when some of the parse calls fail
		for saxparser in (parsers.SGMLOPParser, parsers.BadEntityParser, parsers.HTMLParser, parsers.ExpatParser):
			yield check, saxparser

	def test_sysid(self):
		# Default system ids and explicitely specified system ids should end up in the location info of the resulting XML tree
		node = parsers.parseString("gurk")
		assert node[0].startloc.sysid == "STRING"

		node = parsers.parseString("gurk", base="root:gurk.xmlxsc")
		assert node[0].startloc.sysid == "root:gurk.xmlxsc"

		node = parsers.parseString("gurk", base="root:gurk.xmlxsc", sysid="hurz")
		assert node[0].startloc.sysid == "hurz"


def test_xmlns():
	s = '''
	<z xmlns="http://xmlns.livinglogic.de/xist/ns/specials">
	<rb xmlns="http://www.w3.org/TR/ruby/xhtml-ruby-1.mod"/>
	<z/>
	</z>
	'''
	# After the <rb/> element is left the parser must return to the proper previous mapping
	parsers.parseString(s, nspool=xsc.NSPool(specials, ruby))
