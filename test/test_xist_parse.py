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
from xml import sax
from xml.parsers import expat

import py.test

from ll import url
from ll.xist import xsc, parse, xfind
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
		node = parse.tree(*pipeline)
		node = node.walknodes(a)[0]
		assert unicode(node) == t
		assert unicode(node["title"]) == t

	prefixes = {None: a.xmlns}
	pool = xsc.Pool(a)

	yield check, b, parse.Expat(), parse.NS(a.xmlns), parse.Node(pool)
	yield check, s, parse.Encoder(encoding="utf-8"), parse.Expat(), parse.NS(a.xmlns), parse.Node(pool)
	yield check, parse.Iter(b), parse.Expat(), parse.NS(a.xmlns), parse.Node(pool) # parse byte by byte
	yield check, parse.Stream(cStringIO.StringIO(b), bufsize=1), parse.Expat(), parse.NS(a.xmlns), parse.Node(pool)
	yield check, parse.ETree(cElementTree.fromstring(b), defaultxmlns=a.xmlns), parse.Node(pool)


def test_parselocationsgmlop():
	# sgmlop doesn't provide any location info, so check only the URL
	node = parse.tree(b"<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parse.SGMLOP(), parse.NS(doc), parse.Node())
	assert len(node) == 1
	assert len(node[0]) == 1
	assert str(node[0][0].startloc.url) == "STRING"
	assert node[0][0].startloc.line is None
	assert node[0][0].startloc.col is None


def test_parselocationexpat():
	# Check that expat gets the location info right
	node = parse.tree(b"<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parse.Expat(), parse.NS(doc), parse.Node())
	assert len(node) == 1
	assert len(node[0]) == 1
	assert str(node[0][0].startloc.url) == "STRING"
	assert node[0][0].startloc.line == 0
	assert node[0][0].startloc.col == 36 # expat reports the *end* of the text


def test_nsparse():
	# A prepopulated prefix mapping and xmlns attributes should work together
	xml = b"""
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
	node = parse.tree(xml, parse.Expat(), parse.NS(x=ihtml), parse.Node())
	node = node.walknodes(xsc.Element)[0].compact() # get rid of the Frag and whitespace
	assert node == check


def test_parseurls():
	# Check proper URL handling when parsing ``URLAttr`` or ``StyleAttr`` attributes
	node = parse.tree(b'<a href="4.html" style="background-image: url(3.gif);"/>', parse.Expat(), parse.NS(html), parse.Node(base="root:1/2.html"))
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

		node = parse.tree(b'<Test required="foo"/>', parse.Expat(), parse.NS(xmlns), parse.Node())
		assert str(node[0]["required"]) == "foo"

		parse.tree(b'<Test/>', parse.Expat(), parse.NS(xmlns), parse.Node())
		w = recwarn.pop(xsc.RequiredAttrMissingWarning)

	with py.test.raises(xsc.IllegalElementError):
		parse.tree(b'<Test required="foo"/>', parse.Expat(), parse.NS(xmlns), parse.Node())


def test_parsevalueattrs(recwarn):
	xmlns = "http://www.example.com/required2"

	# Parser should complain about attributes with illegal values, when a set of values is specified
	with xsc.Pool():
		class Test(xsc.Element):
			xmlns = "http://www.example.com/required2"
			class Attrs(xsc.Element.Attrs):
				class withvalues(xsc.TextAttr):
					values = ("foo", "bar")

		node = parse.tree(b'<Test withvalues="bar"/>', parse.Expat(), parse.NS(xmlns), parse.Node())
		assert str(node[0]["withvalues"]) == "bar"

		parse.tree(b'<Test withvalues="baz"/>', parse.Expat(), parse.NS(xmlns), parse.Node())
		w = recwarn.pop(xsc.IllegalAttrValueWarning)


def test_multipleparsecalls():
	def check(parser):
		for i in xrange(3):
			try:
				parse.tree(b"<>gurk", parser, parse.NS(html), parse.Node())
			except Exception:
				pass
			for j in xrange(3):
				assert parse.tree(b"<a>gurk</a>", parser, parse.NS(html), parse.Node()).bytes() == "<a>gurk</a>"

	# A Parser instance should be able to parse multiple XML sources, even when some of the parse calls fail
	for parser in (parse.SGMLOP, parse.Expat):
		yield check, parser()


def test_parseentities_sgmlop():
	def check(input, output):
		node = parse.tree(b"""<a title="{0}">{0}</a>""".format(input), parse.SGMLOP(), parse.NS(a.xmlns), parse.Node(pool=xsc.Pool(a, bar, foo, chars)))
		node = node.walknodes(a)[0]
		assert unicode(node) == output
		assert unicode(node.attrs.title) == output

	yield check, b"a", "a"
	yield check, b";a;", ";a;"
	yield check, b"&lt;", "<"
	yield check, b"&lt;&gt;", "<>"
	yield check, b"&gt;", ">"
	yield check, b"&apos;", "'"
	yield check, b"&quot;", '"'
	yield check, b"&amp;", "&"
	yield check, b"&amp;", "&"
	yield check, b"a&amp;b", "a&b"
	yield check, b"&foo;", "FOO"
	yield check, b"&bar;", "\x42"
	yield check, b"&#32;", " "
	yield check, b"&#x20;", " "
	yield check, b"&#x3042;", u"\u3042"


def test_parseattr_sgmlop():
	def check(input, output):
		node = parse.tree(input, parse.SGMLOP(), parse.NS(a), parse.Node())
		node = node.walknodes(a)[0]
		assert unicode(node.attrs.title) == output

	yield check, b"""<a title=x></a>""", "x"
	yield check, b"""<a title=x/>""", "x"
	yield check, b"""<a title=x id=42/>""", "x"
	yield check, b"""<a title="x" id=42/>""", "x"
	yield check, b"""<a title='x' id=42/>""", "x"
	yield check, b"""<a title='x"y' id=42/>""", 'x"y'
	yield check, b"""<a title="x'y" id=42/>""", "x'y"


def test_parsestringurl():
	# Base URLs should end up in the location info of the resulting XML tree
	node = parse.tree(b"gurk", parse.SGMLOP(), parse.NS(), parse.Node())
	assert str(node[0].startloc.url) == "STRING"

	node = parse.tree(parse.String(b"gurk", url="root:gurk.xmlxsc"), parse.SGMLOP(), parse.NS(), parse.Node())
	assert str(node[0].startloc.url) == "root:gurk.xmlxsc"


def test_xmlns():
	s = b"<z xmlns={!r}><rb xmlns={!r}/><z/></z>".format(doc.xmlns, ruby.xmlns)
	e = parse.tree(s, parse.Expat(ns=True), parse.Node(pool=xsc.Pool(doc, ruby)))

	assert e[0].xmlns == doc.xmlns
	assert e[0][0].xmlns == ruby.xmlns

	s = b"<a xmlns={!r}><a xmlns={!r}/></a>".format(html.xmlns, ihtml.xmlns)
	e = parse.tree(s, parse.Expat(ns=True), parse.Node(pool=xsc.Pool(html, ihtml)))
	assert isinstance(e[0], html.a)
	assert isinstance(e[0][0], ihtml.a)

	s = b"<a><a xmlns={!r}/></a>".format(ihtml.xmlns)
	with py.test.raises(xsc.IllegalElementError):
		parse.tree(s, parse.Expat(), parse.NS(html), parse.Node(pool=xsc.Pool(ihtml)))
	e = parse.tree(s, parse.Expat(), parse.NS(html), parse.Node(pool=xsc.Pool(html, ihtml)))
	assert isinstance(e[0], html.a)
	assert isinstance(e[0][0], ihtml.a)

	s = b"<z xmlns={!r}/>".format(doc.xmlns)
	e = parse.tree(s, parse.Expat(ns=True), parse.Node(pool=xsc.Pool(doc.z)))
	assert isinstance(e[0], doc.z)
	with py.test.raises(xsc.IllegalElementError):
		parse.tree(s, parse.Expat(ns=True), parse.Node(pool=xsc.Pool()))


def test_parseemptyattribute():
	e = parse.tree(b"<a target=''/>", parse.Expat(), parse.NS(html), parse.Node(pool=xsc.Pool(html)))
	assert "target" in e[0].attrs


def test_expat_xmldecl():
	e = parse.tree(b"<?xml version='1.0' encoding='utf-8' standalone='yes'?><a/>", parse.Expat(), parse.NS(html), parse.Node())
	assert not isinstance(e[0], xml.XML)

	e = parse.tree(b"<a/>", parse.Expat(xmldecl=True), parse.NS(html), parse.Node())
	assert not isinstance(e[0], xml.XML)

	e = parse.tree(b"<?xml version='1.0'?><a/>", parse.Expat(xmldecl=True), parse.NS(html), parse.Node())
	assert isinstance(e[0], xml.XML)
	assert e[0].content == u'version="1.0"'

	e = parse.tree(b"<?xml version='1.0' encoding='utf-8'?><a/>", parse.Expat(xmldecl=True), parse.NS(html), parse.Node())
	assert isinstance(e[0], xml.XML)
	assert e[0].content == u'version="1.0" encoding="utf-8"'

	e = parse.tree(b"<?xml version='1.0' encoding='utf-8' standalone='yes'?><a/>", parse.Expat(xmldecl=True), parse.NS(html), parse.Node())
	assert isinstance(e[0], xml.XML)
	assert e[0].content == u'version="1.0" encoding="utf-8" standalone="yes"'


def test_expat_doctype():
	e = parse.tree(b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parse.Expat(), parse.NS(html), parse.Node())
	assert not isinstance(e[0], xsc.DocType)

	e = parse.tree(b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parse.Expat(doctype=True), parse.NS(html), parse.Node())
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == html.DocTypeXHTML11().content

	e = parse.tree(b'<!DOCTYPE html><a/>', parse.Expat(doctype=True), parse.NS(html), parse.Node())
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == "html"

	e = parse.tree(b'<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parse.Expat(doctype=True), parse.NS(html), parse.Node())
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == u'html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"'

	e = parse.tree(b'<!DOCTYPE a [<!ELEMENT a EMPTY><!--gurk-->]><a/>', parse.Expat(doctype=True), parse.NS(html), parse.Node())
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == u'a' # Internal subset gets dropped


def test_htmlparse_base():
	e = parse.tree(b"<a href='gurk.gif'/>", parse.Tidy(), parse.NS(html), parse.Node(base="hurz/index.html"))
	e = e.walknodes(html.a)[0]
	assert unicode(e.attrs.href) == "hurz/gurk.gif"


def test_parse_tidy_empty():
	e = parse.tree(b"", parse.Tidy(), parse.NS(), parse.Node())
	assert not e


def test_base():
	e = parse.tree(parse.String(b'<a xmlns="http://www.w3.org/1999/xhtml" href="gurk.html"/>', 'http://www.gurk.de/'), parse.Expat(ns=True), parse.Node(pool=xsc.Pool(html)))
	assert unicode(e[0].attrs.href) == "http://www.gurk.de/gurk.html"


def test_stringsource():
	expect = b"hinz & kunz"
	source = parse.String(expect)
	for i in xrange(3):
		parsed = b"".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_itersource():
	expect = b"hinz & kunz"
	source = parse.Iter([b"hinz", b" & ", b"kunz"])
	for i in xrange(3):
		parsed = b"".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_filesource():
	expect = open("setup.py", "rb").read()
	source = parse.File("setup.py", bufsize=32)
	for i in xrange(3):
		parsed = "".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_streamsource():
	# Stream objects are not reusable
	expect = open("setup.py", "rb").read()
	parsed = "".join(event[1] for event in parse.Stream(open("setup.py", "rb"), bufsize=32) if event[0] == "bytes")
	assert parsed == expect


@py.test.mark.net
def test_urlsource():
	expect = url.URL("http://www.python.org/").openread().read()
	source = parse.URL("http://www.python.org/", bufsize=32)
	for i in xrange(3):
		parsed = b"".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_itertree_large():
	def xml():
		yield b"<ul xmlns='{}'>".format(html.xmlns)
		for i in xrange(1000):
			yield b"<li>{}</li>".format(i)
		yield b"</ul>"

	for (i, (evtype, path)) in enumerate(parse.itertree(parse.Iter(xml()), parse.Expat(ns=True), parse.Node(), filter=html.li)):
		assert int(str(path[-1])) == i
		path[-2].content.clear()


def test_expat_events_on_exception():
	# Test that all collected events are output before an exception is thrown
	i = parse.events(b"<x/>schrott", parse.Expat())
	assert i.next() == (u"url", url.URL("STRING"))
	assert i.next() == (u"position", (0, 0))
	assert i.next() == (u"enterstarttag", u"x")
	assert i.next() == (u"leavestarttag", u"x")
	assert i.next() == (u"position", (0, 4))
	assert i.next() == (u"endtag", u"x")
	with py.test.raises(expat.ExpatError):
		i.next()


def test_expat_no_multiple_text_events():
	# Test that we don't get consecutive text events with expat
	i = parse.events(parse.Iter(b"<a>gurk &amp; hurz &amp; hinz &amp; kunz</a>"), parse.Expat())
	assert i.next() == (u"url", url.URL("ITER"))
	assert i.next() == (u"position", (0, 0))
	assert i.next() == (u"enterstarttag", u"a")
	assert i.next() == (u"leavestarttag", u"a")
	assert i.next() == (u"position", (0, 4))
	assert i.next() == (u"text", u"gurk & hurz & hinz & kunz")
	assert i.next() == (u"position", (0, 40))
	assert i.next() == (u"endtag", u"a")
	with py.test.raises(StopIteration):
		i.next()


def test_sgmlop_no_multiple_text_events():
	# Test that we don't get consecutive text events with sgmlop
	i = parse.events(parse.Iter(b"<a>gurk &amp; hurz &amp; hinz &amp; kunz</a>"), parse.SGMLOP())
	assert i.next() == (u"url", url.URL("ITER"))
	assert i.next() == (u"enterstarttag", u"a")
	assert i.next() == (u"leavestarttag", u"a")
	assert i.next() == (u"text", u"gurk & hurz & hinz & kunz")
	assert i.next() == (u"endtag", u"a")
	with py.test.raises(StopIteration):
		i.next()

