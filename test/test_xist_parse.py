#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import warnings, cStringIO

from xml.etree import cElementTree

import py.test

from xml import sax
from xml.parsers import expat

from ll import url
from ll.xist import xsc, parsers
from ll.xist.ns import xml, chars, html, ihtml, specials, ruby


oldfilters = None


class a(xsc.Element):
	xmlns = "http://www.example.com/foo"
	class Attrs(xsc.Element.Attrs):
		class id(xsc.IDAttr): pass
		class title(xsc.TextAttr): pass


class foo(xsc.Entity):
	def __unicode__(self):
		return u"FOO"


class bar(xsc.CharRef):
	codepoint = 0x42


def check_parseentities(source, result, **parseargs):
	node = parsers.parsestring("""<a title="%s">%s</a>""" % (source, source), **parseargs)
	node = node.walknode(xsc.FindType(xsc.Element))[0]
	assert unicode(node) == result
	assert unicode(node["title"]) == result


def check_parsestrictentities(source, result, parserfactory):
	prefixes = {None: (a.xmlns, chars)}
	check_parseentities(source, result, prefixes=prefixes, parser=parserfactory())

	for bad in ("&", "&#x", "&&", "&#x;", "&#fg;", "&#999999999;", "&#;", "&#y;", "&#x;", "&#xy;"):
		py.test.raises(expat.ExpatError, check_parseentities, bad, u"", prefixes=prefixes, parser=parserfactory())
	py.test.raises(xsc.IllegalEntityError, check_parseentities, "&baz;", u"", prefixes=prefixes, parser=parserfactory())


def test_parsingmethods():
	t = u"abc\U00012345\u3042xyz"
	s = u'<?xml version="1.0" encoding="utf-8"?><a title="%s">%s</a>' % (t, t)
	b = s.encode("utf-8")

	def check(node):
		node = node.walknode(a)[0]
		assert unicode(node) == t
		assert unicode(node["title"]) == t

	yield check, parsers.parsestring(b, pool=xsc.Pool(a))
	yield check, parsers.parsestring(s, pool=xsc.Pool(a)) # parsestring can parse unicode directly
	yield check, parsers.parseiter(b, pool=xsc.Pool(a)) # parse byte by byte
	yield check, parsers.parsestream(cStringIO.StringIO(b), bufsize=1, pool=xsc.Pool(a))
	yield check, parsers.parseetree(cElementTree.fromstring(b), prefixes={None: [a.xmlns]}, pool=xsc.Pool(a))


def test_parselocationsgmlop():
	# sgmlop doesn't provide any location info, so check only the URL
	node = parsers.parsestring("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parser=parsers.SGMLOPParser())
	assert len(node) == 1
	assert len(node[0]) == 1
	assert str(node[0][0].startloc.url) == "STRING"
	assert node[0][0].startloc.line is None
	assert node[0][0].startloc.col is None


def test_parselocationexpat():
	# Check that expat gets the location info right
	node = parsers.parsestring("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parser=parsers.ExpatParser())
	assert len(node) == 1
	assert len(node[0]) == 1
	assert str(node[0][0].startloc.url) == "STRING"
	assert node[0][0].startloc.line == 0
	assert node[0][0].startloc.col == 36 # expat reports the *end* of the text


class Test:
	def setup_method(self, method):
		global oldfilters
		oldfilters = warnings.filters[:]

	def teardown_method(self, method):
		warnings.filters = oldfilters

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
		node = parsers.parsestring(xml, prefixes=dict(x=ihtml))
		node = node.walknode(xsc.FindType(xsc.Element))[0].compact() # get rid of the Frag and whitespace
		assert node == check

	def test_parseurls(self):
		# Check proper URL handling when parsing URLAttr or StyleAttr attributes
		node = parsers.parsestring('<a href="4.html" style="background-image: url(3.gif);"/>', base="root:1/2.html", prefixes={None: html})
		assert str(node[0]["style"]) == "background-image: url(root:1/3.gif)"
		assert node[0]["style"].urls() == [url.URL("root:1/3.gif")]
		assert str(node[0]["href"]) == "root:1/4.html"
		assert node[0]["href"].forInput(root="gurk/hurz.html") == url.URL("gurk/1/4.html")

	def test_parserequiredattrs(self):
		xmlns = "http://www.example.com/required"

		prefixes = {None: xmlns}

		# Parser should complain about required attributes that are missing
		with xsc.Pool():
			class Test(xsc.Element):
				xmlns = "http://www.example.com/required"
				class Attrs(xsc.Element.Attrs):
					class required(xsc.TextAttr):
						required = True

			node = parsers.parsestring('<Test required="foo"/>', prefixes=prefixes)
			assert str(node[0]["required"]) == "foo"
	
			warnings.filterwarnings("error", category=xsc.RequiredAttrMissingWarning)
			py.test.raises(xsc.RequiredAttrMissingWarning, parsers.parsestring, '<Test/>', prefixes=prefixes)

		py.test.raises(xsc.IllegalElementError, parsers.parsestring, '<Test required="foo"/>', prefixes=prefixes)

	def test_parsevalueattrs(self):
		xmlns = "http://www.example.com/required2"

		prefixes = {None: xmlns}

		# Parser should complain about attributes with illegal values, when a set of values is specified
		with xsc.Pool():
			class Test(xsc.Element):
				xmlns = "http://www.example.com/required2"
				class Attrs(xsc.Element.Attrs):
					class withvalues(xsc.TextAttr):
						values = ("foo", "bar")

			node = parsers.parsestring('<Test withvalues="bar"/>', prefixes=prefixes)
			assert str(node[0]["withvalues"]) == "bar"
	
			warnings.filterwarnings("error", category=xsc.IllegalAttrValueWarning)
			py.test.raises(xsc.IllegalAttrValueWarning, parsers.parsestring, '<Test withvalues="baz"/>', prefixes=prefixes)

	def test_parsestrictentities_expat(self):
		check_parsestrictentities(
			"a&amp;bc&#32;d&#x20;&#30000;;&lt;&gt;&quot;&apos;",
			u"""a&bc d %c;<>"'""" % 30000,
			parsers.ExpatParser
		)


def test_multipleparsecalls():
	def check(parser):
		b = parsers.Builder(parser=parser)
		for i in xrange(3):
			try:
				b.parsestring("<>gurk")
			except Exception:
				pass
			for j in xrange(3):
				assert b.parsestring("<a>gurk</a>").bytes() == "<a>gurk</a>"

	# A Parser instance should be able to parse multiple XML sources, even when some of the parse calls fail
	for parser in (parsers.SGMLOPParser, parsers.ExpatParser):
		yield check, parser()


def test_parseentities_sgmlop():
	def check(input, output):
		prefixes = {None: (a.xmlns, chars)}
		node = parsers.parsestring("""<a title="%s">%s</a>""" % (input, input), parser=parsers.SGMLOPParser(), prefixes=prefixes)
		node = node.walknode(a)[0]
		assert unicode(node) == output
		assert unicode(node.attrs.title) == output

	yield check, "a", "a"
	yield check, ";a;", ";a;"
	yield check, "&lt;", "<"
	yield check, "&lt;&gt;", "<>"
	yield check, "&gt;", ">"
	yield check, "&apos;", "'"
	yield check, "&quot;", '"'
	yield check, "&amp;", "&"
	yield check, "&amp;", "&"
	yield check, "a&amp;b", "a&b"
	yield check, "&foo;", "FOO"
	yield check, "&bar;", "\x42"
	yield check, "&#32;", " "
	yield check, "&#x20;", " "
	yield check, "&#x3042;", u"\u3042"


def test_parseattr_sgmlop():
	def check(input, output):
		prefixes = {None: (a.xmlns, chars)}
		node = parsers.parsestring(input, parser=parsers.SGMLOPParser(), prefixes=prefixes)
		node = node.walknode(a)[0]
		assert unicode(node.attrs.title) == output

	yield check, """<a title=x></a>""", "x"
	yield check, """<a title=x/>""", "x"
	yield check, """<a title=x id=42/>""", "x"
	yield check, """<a title="x" id=42/>""", "x"
	yield check, """<a title='x' id=42/>""", "x"
	yield check, """<a title='x"y' id=42/>""", 'x"y'
	yield check, """<a title="x'y" id=42/>""", "x'y"


def test_parsestringurl():
	# Base URLs should end up in the location info of the resulting XML tree
	node = parsers.parsestring("gurk", parser=parsers.SGMLOPParser())
	assert str(node[0].startloc.url) == "STRING"

	node = parsers.parsestring("gurk", base="root:gurk.xmlxsc", parser=parsers.SGMLOPParser())
	assert str(node[0].startloc.url) == "root:gurk.xmlxsc"


def test_xmlns():
	s = "<z xmlns=%r><rb xmlns=%r/><z/></z>" % (specials.xmlns, ruby.xmlns)
	e = parsers.parsestring(s)

	assert e[0].xmlns == specials.xmlns
	assert e[0][0].xmlns == ruby.xmlns

	s = "<a xmlns=%r><a xmlns=%r/></a>" % (html.xmlns, ihtml.xmlns)
	e = parsers.parsestring(s, pool=xsc.Pool(html, ihtml))
	assert isinstance(e[0], html.a)
	assert isinstance(e[0][0], ihtml.a)

	s = "<a><a xmlns=%r/></a>" % ihtml.xmlns
	py.test.raises(xsc.IllegalElementError, parsers.parsestring, s, prefixes={None: html}, pool=xsc.Pool(ihtml))
	e = parsers.parsestring(s, prefixes={None: html}, pool=xsc.Pool(html, ihtml))
	assert isinstance(e[0], html.a)
	assert isinstance(e[0][0], ihtml.a)

	s = "<z xmlns=%r/>" % specials.xmlns
	e = parsers.parsestring(s, pool=xsc.Pool(specials.z))
	assert isinstance(e[0], specials.z)
	py.test.raises(xsc.IllegalElementError, parsers.parsestring, s, pool=xsc.Pool())


def test_parseemptyattribute():
	e = parsers.parsestring("<a target=''/>", pool=xsc.Pool(html))
	assert "target" in e[0].attrs


def test_expat_xmldecl():
	e = parsers.parsestring("<?xml version='1.0' encoding='utf-8' standalone='yes'?><a/>", parser=parsers.ExpatParser())
	assert not isinstance(e[0], xml.XML)

	e = parsers.parsestring("<a/>", parser=parsers.ExpatParser(xmldecl=True))
	assert not isinstance(e[0], xml.XML)

	e = parsers.parsestring("<?xml version='1.0'?><a/>", parser=parsers.ExpatParser(xmldecl=True))
	assert isinstance(e[0], xml.XML)
	assert e[0].content == u'version="1.0"'

	e = parsers.parsestring("<?xml version='1.0' encoding='utf-8'?><a/>", parser=parsers.ExpatParser(xmldecl=True))
	assert isinstance(e[0], xml.XML)
	assert e[0].content == u'version="1.0" encoding="utf-8"'

	e = parsers.parsestring("<?xml version='1.0' encoding='utf-8' standalone='yes'?><a/>", parser=parsers.ExpatParser(xmldecl=True))
	assert isinstance(e[0], xml.XML)
	assert e[0].content == u'version="1.0" encoding="utf-8" standalone="yes"'


def test_expat_doctype():
	e = parsers.parsestring('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parser=parsers.ExpatParser())
	assert not isinstance(e[0], xsc.DocType)

	e = parsers.parsestring('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parser=parsers.ExpatParser(doctype=True))
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == html.DocTypeXHTML11().content

	e = parsers.parsestring('<!DOCTYPE html><a/>', parser=parsers.ExpatParser(doctype=True))
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == "html"

	e = parsers.parsestring('<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parser=parsers.ExpatParser(doctype=True))
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == u'html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"'

	e = parsers.parsestring('<!DOCTYPE a [<!ELEMENT a EMPTY><!--gurk-->]><a/>', parser=parsers.ExpatParser(doctype=True))
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == u'a' # Internal subset gets dropped


def test_htmlparse_base():
	e = parsers.parsestring("<a href='gurk.gif'/>", base="hurz/index.html", tidy=True)
	e = e.walknode(html.a)[0]
	assert unicode(e.attrs.href) == "hurz/gurk.gif"


def test_parse_tidy_empty():
	e = parsers.parsestring("", tidy=True)
	assert not e