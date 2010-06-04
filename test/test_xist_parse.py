#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import cStringIO

from xml.etree import cElementTree

import py.test

from xml import sax
from xml.parsers import expat

from ll import url
from ll.xist import xsc, parsers, xfind
from ll.xist.ns import xml, chars, html, ihtml, specials, ruby, doc


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


def test_parsingmethods():
	t = u"abc\U00012345\u3042xyz"
	s = u'<?xml version="1.0" encoding="utf-8"?><a title="{0}">{0}</a>'.format(t)
	b = s.encode("utf-8")

	def check(*pipeline):
		node = parsers.tree(*pipeline)
		node = node.walknodes(a)[0]
		assert unicode(node) == t
		assert unicode(node["title"]) == t

	prefixes = {None: a.xmlns}
	pool = xsc.Pool(a)

	yield check, b, parsers.Expat(), parsers.NS(a.xmlns), parsers.Instantiate(pool)
	yield check, s, parsers.Encoder(encoding="utf-8"), parsers.Expat(), parsers.NS(a.xmlns), parsers.Instantiate(pool)
	yield check, parsers.IterSource(b), parsers.Expat(), parsers.NS(a.xmlns), parsers.Instantiate(pool) # parse byte by byte
	yield check, parsers.StreamSource(cStringIO.StringIO(b), bufsize=1), parsers.Expat(), parsers.NS(a.xmlns), parsers.Instantiate(pool)
	yield check, parsers.ETreeSource(cElementTree.fromstring(b), defaultxmlns=a.xmlns), parsers.Instantiate(pool)


def test_parselocationsgmlop():
	# sgmlop doesn't provide any location info, so check only the URL
	node = parsers.tree("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parsers.SGMLOP(), parsers.NS(doc), parsers.Instantiate())
	assert len(node) == 1
	assert len(node[0]) == 1
	assert str(node[0][0].startloc.url) == "STRING"
	assert node[0][0].startloc.line is None
	assert node[0][0].startloc.col is None


def test_parselocationexpat():
	# Check that expat gets the location info right
	node = parsers.tree("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parsers.Expat(), parsers.NS(doc), parsers.Instantiate())
	assert len(node) == 1
	assert len(node[0]) == 1
	assert str(node[0][0].startloc.url) == "STRING"
	assert node[0][0].startloc.line == 0
	assert node[0][0].startloc.col == 36 # expat reports the *end* of the text


def test_nsparse():
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
	node = parsers.tree(xml, parsers.Expat(), parsers.NS(x=ihtml), parsers.Instantiate())
	node = node.walknodes(xsc.Element)[0].compact() # get rid of the Frag and whitespace
	assert node == check


def test_parseurls():
	# Check proper URL handling when parsing URLAttr or StyleAttr attributes
	node = parsers.tree('<a href="4.html" style="background-image: url(3.gif);"/>', parsers.Expat(), parsers.NS(html), parsers.Instantiate(base="root:1/2.html"))
	assert str(node[0]["style"]) == "background-image: url(root:1/3.gif)"
	assert node[0]["style"].urls() == [url.URL("root:1/3.gif")]
	assert str(node[0]["href"]) == "root:1/4.html"
	assert node[0]["href"].forInput(root="gurk/hurz.html") == url.URL("gurk/1/4.html")


def test_parserequiredattrs(recwarn):
	xmlns = "http://www.example.com/required"

	# Parser should complain about required attributes that are missing
	with xsc.Pool():
		class Test(xsc.Element):
			xmlns = "http://www.example.com/required"
			class Attrs(xsc.Element.Attrs):
				class required(xsc.TextAttr):
					required = True

		node = parsers.tree('<Test required="foo"/>', parsers.Expat(), parsers.NS(xmlns), parsers.Instantiate())
		assert str(node[0]["required"]) == "foo"

		parsers.tree('<Test/>', parsers.Expat(), parsers.NS(xmlns), parsers.Instantiate())
		w = recwarn.pop(xsc.RequiredAttrMissingWarning)

	py.test.raises(xsc.IllegalElementError, parsers.tree, '<Test required="foo"/>', parsers.Expat(), parsers.NS(xmlns), parsers.Instantiate())


def test_parsevalueattrs(recwarn):
	xmlns = "http://www.example.com/required2"

	# Parser should complain about attributes with illegal values, when a set of values is specified
	with xsc.Pool():
		class Test(xsc.Element):
			xmlns = "http://www.example.com/required2"
			class Attrs(xsc.Element.Attrs):
				class withvalues(xsc.TextAttr):
					values = ("foo", "bar")

		node = parsers.tree('<Test withvalues="bar"/>', parsers.Expat(), parsers.NS(xmlns), parsers.Instantiate())
		assert str(node[0]["withvalues"]) == "bar"

		parsers.tree('<Test withvalues="baz"/>', parsers.Expat(), parsers.NS(xmlns), parsers.Instantiate())
		w = recwarn.pop(xsc.IllegalAttrValueWarning)


def test_multipleparsecalls():
	def check(parser):
		for i in xrange(3):
			try:
				parsers.tree("<>gurk", parser, parsers.NS(html), parsers.Instantiate())
			except Exception:
				pass
			for j in xrange(3):
				assert parsers.tree("<a>gurk</a>", parser, parsers.NS(html), parsers.Instantiate()).bytes() == "<a>gurk</a>"

	# A Parser instance should be able to parse multiple XML sources, even when some of the parse calls fail
	for parser in (parsers.SGMLOP, parsers.Expat):
		yield check, parser()


def test_parseentities_sgmlop():
	def check(input, output):
		node = parsers.tree("""<a title="{0}">{0}</a>""".format(input), parsers.SGMLOP(), parsers.NS(a.xmlns), parsers.Instantiate(pool=xsc.Pool(a, bar, foo, chars)))
		node = node.walknodes(a)[0]
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
		node = parsers.tree(input, parsers.SGMLOP(), parsers.NS(a), parsers.Instantiate())
		node = node.walknodes(a)[0]
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
	node = parsers.tree("gurk", parsers.SGMLOP(), parsers.NS(), parsers.Instantiate())
	assert str(node[0].startloc.url) == "STRING"

	node = parsers.tree(parsers.StringSource("gurk", url="root:gurk.xmlxsc"), parsers.SGMLOP(), parsers.NS(), parsers.Instantiate())
	assert str(node[0].startloc.url) == "root:gurk.xmlxsc"


def test_xmlns():
	s = "<z xmlns={0!r}><rb xmlns={1!r}/><z/></z>".format(doc.xmlns, ruby.xmlns)
	e = parsers.tree(s, parsers.Expat(ns=True), parsers.Instantiate(pool=xsc.Pool(doc, ruby)))

	assert e[0].xmlns == doc.xmlns
	assert e[0][0].xmlns == ruby.xmlns

	s = "<a xmlns={0!r}><a xmlns={1!r}/></a>".format(html.xmlns, ihtml.xmlns)
	e = parsers.tree(s, parsers.Expat(ns=True), parsers.Instantiate(pool=xsc.Pool(html, ihtml)))
	assert isinstance(e[0], html.a)
	assert isinstance(e[0][0], ihtml.a)

	s = "<a><a xmlns={0!r}/></a>".format(ihtml.xmlns)
	py.test.raises(xsc.IllegalElementError, parsers.tree, s, parsers.Expat(), parsers.NS(html), parsers.Instantiate(pool=xsc.Pool(ihtml)))
	e = parsers.tree(s, parsers.Expat(), parsers.NS(html), parsers.Instantiate(pool=xsc.Pool(html, ihtml)))
	assert isinstance(e[0], html.a)
	assert isinstance(e[0][0], ihtml.a)

	s = "<z xmlns={0!r}/>".format(doc.xmlns)
	e = parsers.tree(s, parsers.Expat(ns=True), parsers.Instantiate(pool=xsc.Pool(doc.z)))
	assert isinstance(e[0], doc.z)
	py.test.raises(xsc.IllegalElementError, parsers.tree, s, parsers.Expat(ns=True), parsers.Instantiate(pool=xsc.Pool()))


def test_parseemptyattribute():
	e = parsers.tree("<a target=''/>", parsers.Expat(), parsers.NS(html), parsers.Instantiate(pool=xsc.Pool(html)))
	assert "target" in e[0].attrs


def test_expat_xmldecl():
	e = parsers.tree("<?xml version='1.0' encoding='utf-8' standalone='yes'?><a/>", parsers.Expat(), parsers.NS(html), parsers.Instantiate())
	assert not isinstance(e[0], xml.XML)

	e = parsers.tree("<a/>", parsers.Expat(xmldecl=True), parsers.NS(html), parsers.Instantiate())
	assert not isinstance(e[0], xml.XML)

	e = parsers.tree("<?xml version='1.0'?><a/>", parsers.Expat(xmldecl=True), parsers.NS(html), parsers.Instantiate())
	assert isinstance(e[0], xml.XML)
	assert e[0].content == u'version="1.0"'

	e = parsers.tree("<?xml version='1.0' encoding='utf-8'?><a/>", parsers.Expat(xmldecl=True), parsers.NS(html), parsers.Instantiate())
	assert isinstance(e[0], xml.XML)
	assert e[0].content == u'version="1.0" encoding="utf-8"'

	e = parsers.tree("<?xml version='1.0' encoding='utf-8' standalone='yes'?><a/>", parsers.Expat(xmldecl=True), parsers.NS(html), parsers.Instantiate())
	assert isinstance(e[0], xml.XML)
	assert e[0].content == u'version="1.0" encoding="utf-8" standalone="yes"'


def test_expat_doctype():
	e = parsers.tree('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parsers.Expat(), parsers.NS(html), parsers.Instantiate())
	assert not isinstance(e[0], xsc.DocType)

	e = parsers.tree('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parsers.Expat(doctype=True), parsers.NS(html), parsers.Instantiate())
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == html.DocTypeXHTML11().content

	e = parsers.tree('<!DOCTYPE html><a/>', parsers.Expat(doctype=True), parsers.NS(html), parsers.Instantiate())
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == "html"

	e = parsers.tree('<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parsers.Expat(doctype=True), parsers.NS(html), parsers.Instantiate())
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == u'html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"'

	e = parsers.tree('<!DOCTYPE a [<!ELEMENT a EMPTY><!--gurk-->]><a/>', parsers.Expat(doctype=True), parsers.NS(html), parsers.Instantiate())
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == u'a' # Internal subset gets dropped


def test_htmlparse_base():
	e = parsers.tree("<a href='gurk.gif'/>", parsers.Tidy(), parsers.NS(html), parsers.Instantiate(base="hurz/index.html"))
	e = e.walknodes(html.a)[0]
	assert unicode(e.attrs.href) == "hurz/gurk.gif"


def test_parse_tidy_empty():
	e = parsers.tree("", parsers.Tidy(), parsers.NS(), parsers.Instantiate())
	assert not e


def test_base():
	e = parsers.tree(parsers.StringSource('<a xmlns="http://www.w3.org/1999/xhtml" href="gurk.html"/>', 'http://www.gurk.de/'), parsers.Expat(ns=True), parsers.Instantiate(pool=xsc.Pool(html)))
	assert unicode(e[0].attrs.href) == "http://www.gurk.de/gurk.html"


def test_stringsource():
	expect = "hinz & kunz"
	source = parsers.StringSource(expect)
	for i in xrange(3):
		parsed = "".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_itersource():
	expect = "hinz & kunz"
	source = parsers.IterSource(["hinz", " & ", "kunz"])
	for i in xrange(3):
		parsed = "".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_filesource():
	expect = open("setup.py", "rb").read()
	source = parsers.FileSource("setup.py", bufsize=32)
	for i in xrange(3):
		parsed = "".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_streamsource():
	# StreamSource objects are not reusable
	expect = open("setup.py", "rb").read()
	parsed = "".join(event[1] for event in parsers.StreamSource(open("setup.py", "rb"), bufsize=32) if event[0] == "bytes")
	assert parsed == expect


def test_urlsource():
	expect = url.URL("http://www.python.org/").openread().read()
	source = parsers.URLSource("http://www.python.org/", bufsize=32)
	for i in xrange(3):
		parsed = "".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_itertree_large():
	def xml():
		yield "<ul xmlns='%s'>" % html.xmlns
		for i in xrange(1000):
			yield "<li>%d</li>" % i
		yield "</ul>"

	for (i, (evtype, path)) in enumerate(parsers.itertree(parsers.IterSource(xml()), parsers.Expat(ns=True), parsers.Instantiate(), filter=html.li)):
		assert int(str(path[-1])) == i
		path[-2].content.clear()
