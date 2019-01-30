#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import io, warnings

from xml.etree import cElementTree
from xml.parsers import expat

import pytest

from ll import url
from ll.xist import xsc, parse, xfind
from ll.xist.ns import xml, chars, html, xlink, ihtml, specials, ruby, doc


class a(xsc.Element):
	xmlns = "http://www.example.com/foo"
	class Attrs(xsc.Element.Attrs):
		class id(xsc.IDAttr): pass
		class title(xsc.TextAttr): pass


class foo(xsc.Entity):
	def __str__(self):
		return "FOO"


class bar(xsc.CharRef):
	codepoint = 0x42


def test_parsingmethods():
	t = "abc\U00012345\u3042xyz"
	s = f'<?xml version="1.0" encoding="utf-8"?><a title="{t}">{t}</a>'
	b = s.encode("utf-8")

	def check(*pipeline):
		node = parse.tree(*pipeline, validate=True)
		node = node.walknodes(a)[0]
		assert str(node) == t
		assert str(node["title"]) == t

	prefixes = {None: a.xmlns}
	pool = xsc.Pool(a)

	check(b, parse.Expat(), parse.NS(a.xmlns), parse.Node(pool))
	check(s, parse.Encoder(encoding="utf-8"), parse.Expat(), parse.NS(a.xmlns), parse.Node(pool))
	check(parse.Iter(b), parse.Expat(), parse.NS(a.xmlns), parse.Node(pool)) # parse byte by byte
	check(parse.Stream(io.BytesIO(b), bufsize=1), parse.Expat(), parse.NS(a.xmlns), parse.Node(pool))
	check(parse.ETree(cElementTree.fromstring(b), defaultxmlns=a.xmlns), parse.Node(pool))


def test_parselocationsgmlop():
	# sgmlop doesn't provide any location info, so check only the URL
	node = parse.tree(b"<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parse.SGMLOP(), parse.NS(doc), parse.Node(), validate=True)
	assert len(node) == 1
	assert len(node[0]) == 1
	assert str(node[0][0].startloc.url) == "STRING"
	assert node[0][0].startloc.line is None
	assert node[0][0].startloc.col is None


def test_parselocationexpat():
	# Check that expat gets the location info right
	node = parse.tree(b"<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parse.Expat(), parse.NS(doc), parse.Node(), validate=True)
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
				<x:a xmlns:x='http://xmlns.livinglogic.de/xist/ns/doc'>gurk</x:a>
			</x:a>
		</x:a>
	"""
	check = doc.a(
		html.a(
			doc.a(
				"gurk"
			)
		)
	)
	node = parse.tree(xml, parse.Expat(), parse.NS(x=doc), parse.Node(), validate=True)
	node = node.walknodes(xsc.Element)[0].compacted() # get rid of the Frag and whitespace
	assert node == check


def test_parseurls():
	# Check proper URL handling when parsing ``URLAttr`` or ``StyleAttr`` attributes
	node = parse.tree(b'<a href="4.html" style="background-image: url(3.gif);"/>', parse.Expat(), parse.NS(html), parse.Node(base="root:1/2.html"), validate=True)
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

		node = parse.tree(b'<Test required="foo"/>', parse.Expat(), parse.NS(xmlns), parse.Node(), validate=True)
		assert str(node[0]["required"]) == "foo"

		parse.tree(b'<Test/>', parse.Expat(), parse.NS(xmlns), parse.Node(), validate=True)
		w = recwarn.pop(xsc.RequiredAttrMissingWarning)

	node = parse.tree(b'<Test required="foo"/>', parse.Expat(), parse.NS(xmlns), parse.Node(), validate=True)
	assert node[0].__class__ is xsc.Element
	assert node[0].xmlname == "Test"
	assert node[0].xmlns == xmlns


def test_parsevalueattrs(recwarn):
	xmlns = "http://www.example.com/required2"

	# Parser should complain about attributes with illegal values, when a set of values is specified
	with xsc.Pool():
		class Test(xsc.Element):
			xmlns = "http://www.example.com/required2"
			class Attrs(xsc.Element.Attrs):
				class withvalues(xsc.TextAttr):
					values = ("foo", "bar")

		node = parse.tree(b'<Test withvalues="bar"/>', parse.Expat(), parse.NS(xmlns), parse.Node(), validate=True)
		assert str(node[0]["withvalues"]) == "bar"

		parse.tree(b'<Test withvalues="baz"/>', parse.Expat(), parse.NS(xmlns), parse.Node(), validate=True)
		w = recwarn.pop(xsc.IllegalAttrValueWarning)


def test_multipleparsecalls():
	def check(parser):
		for i in range(3):
			try:
				parse.tree(b"<>gurk", parser, parse.NS(html), parse.Node(), validate=True)
			except Exception:
				pass
			for j in range(3):
				assert parse.tree(b"<a>gurk</a>", parser, parse.NS(html), parse.Node()).string() == "<a>gurk</a>"

	# A Parser instance should be able to parse multiple XML sources, even when some of the parse calls fail
	check(parse.SGMLOP())
	check(parse.Expat())


def test_parseentities_sgmlop():
	def check(input, output):
		node = parse.tree(f'<a title="{input}">{input}</a>'.encode("utf-8"), parse.SGMLOP(), parse.NS(a.xmlns), parse.Node(pool=xsc.Pool(a, bar, foo, chars)), validate=True)
		node = node.walknodes(a)[0]
		assert str(node) == output
		assert str(node.attrs.title) == output

	check("a", "a")
	check(";a;", ";a;")
	check("&lt;", "<")
	check("&lt;&gt;", "<>")
	check("&gt;", ">")
	check("&apos;", "'")
	check("&quot;", '"')
	check("&amp;", "&")
	check("&amp;", "&")
	check("a&amp;b", "a&b")
	check("&foo;", "FOO")
	check("&bar;", "\x42")
	check("&#32;", " ")
	check("&#x20;", " ")
	check("&#x3042;", "\u3042")


def test_parseattr_sgmlop():
	def check(input, output):
		node = parse.tree(input, parse.SGMLOP(), parse.NS(a), parse.Node(), validate=True)
		node = node.walknodes(a)[0]
		assert str(node.attrs.title) == output

	check(b"""<a title=x></a>""", "x")
	check(b"""<a title=x/>""", "x")
	check(b"""<a title=x id=42/>""", "x")
	check(b"""<a title="x" id=42/>""", "x")
	check(b"""<a title='x' id=42/>""", "x")
	check(b"""<a title='x"y' id=42/>""", 'x"y')
	check(b"""<a title="x'y" id=42/>""", "x'y")


def test_parsestringurl():
	# Base URLs should end up in the location info of the resulting XML tree
	node = parse.tree(b"gurk", parse.SGMLOP(), parse.NS(), parse.Node(), validate=True)
	assert str(node[0].startloc.url) == "STRING"

	node = parse.tree(parse.String(b"gurk", url="root:gurk.xmlxsc"), parse.SGMLOP(), parse.NS(), parse.Node())
	assert str(node[0].startloc.url) == "root:gurk.xmlxsc"


def test_xmlns():
	s = f"<z xmlns={doc.xmlns!r}><rb xmlns={ruby.xmlns!r}/><z/></z>".encode("utf-8")
	e = parse.tree(s, parse.Expat(ns=True), parse.Node(pool=xsc.Pool(doc, ruby)), validate=True)

	assert e[0].xmlns == doc.xmlns
	assert e[0][0].xmlns == ruby.xmlns

	s = f"<a xmlns={html.xmlns!r}><a xmlns={ihtml.xmlns!r}/></a>".encode("utf-8")
	e = parse.tree(s, parse.Expat(ns=True), parse.Node(pool=xsc.Pool(html, ihtml)), validate=True)
	assert isinstance(e[0], html.a)
	assert isinstance(e[0][0], ihtml.a)

	s = f"<a><a xmlns={ihtml.xmlns!r}/></a>".encode("utf-8")
	with warnings.catch_warnings(record=True) as ws:
		e  = parse.tree(s, parse.Expat(), parse.NS(html), parse.Node(pool=xsc.Pool(ihtml)), validate=True)
	assert e[0].__class__ is xsc.Element
	assert e[0].xmlname == "a"
	assert e[0].xmlns == html.xmlns
	assert isinstance(e[0][0], ihtml.a)
	assert len(ws) == 1
	assert issubclass(ws[0].category, xsc.UndeclaredNodeWarning)

	e = parse.tree(s, parse.Expat(), parse.NS(html), parse.Node(pool=xsc.Pool(html, ihtml)), validate=True)
	assert isinstance(e[0], html.a)
	assert isinstance(e[0][0], ihtml.a)

	s = f"<z xmlns={doc.xmlns!r}/>".encode("utf-8")
	e = parse.tree(s, parse.Expat(ns=True), parse.Node(pool=xsc.Pool(doc.z)), validate=True)
	assert isinstance(e[0], doc.z)

	with warnings.catch_warnings(record=True) as ws:
		e = parse.tree(s, parse.Expat(ns=True), parse.Node(pool=xsc.Pool()), validate=True)
	assert e[0].__class__ is xsc.Element
	assert e[0].xmlname == "z"
	assert e[0].xmlns == doc.xmlns
	assert len(ws) == 1
	assert issubclass(ws[0].category, xsc.UndeclaredNodeWarning)


def test_parseemptyattribute():
	e = parse.tree(b"<a target=''/>", parse.Expat(), parse.NS(html), parse.Node(pool=xsc.Pool(html)), validate=True)
	assert "target" in e[0].attrs


def test_expat_xmldecl():
	e = parse.tree(b"<?xml version='1.0' encoding='utf-8' standalone='yes'?><a/>", parse.Expat(), parse.NS(html), parse.Node(), validate=True)
	assert not isinstance(e[0], xml.XML)

	e = parse.tree(b"<a/>", parse.Expat(xmldecl=True), parse.NS(html), parse.Node(), validate=True)
	assert not isinstance(e[0], xml.XML)

	e = parse.tree(b"<?xml version='1.0'?><a/>", parse.Expat(xmldecl=True), parse.NS(html), parse.Node(), validate=True)
	assert isinstance(e[0], xml.XML)
	assert e[0].content == 'version="1.0"'

	e = parse.tree(b"<?xml version='1.0' encoding='utf-8'?><a/>", parse.Expat(xmldecl=True), parse.NS(html), parse.Node(), validate=True)
	assert isinstance(e[0], xml.XML)
	assert e[0].content == 'version="1.0" encoding="utf-8"'

	e = parse.tree(b"<?xml version='1.0' encoding='utf-8' standalone='yes'?><a/>", parse.Expat(xmldecl=True), parse.NS(html), parse.Node(), validate=True)
	assert isinstance(e[0], xml.XML)
	assert e[0].content == 'version="1.0" encoding="utf-8" standalone="yes"'


def test_expat_doctype():
	e = parse.tree(b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parse.Expat(), parse.NS(html), parse.Node(), validate=True)
	assert not isinstance(e[0], xsc.DocType)

	e = parse.tree(b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parse.Expat(doctype=True), parse.NS(html), parse.Node(), validate=True)
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == html.DocTypeXHTML11().content

	e = parse.tree(b'<!DOCTYPE html><a/>', parse.Expat(doctype=True), parse.NS(html), parse.Node(), validate=True)
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == "html"

	e = parse.tree(b'<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><a/>', parse.Expat(doctype=True), parse.NS(html), parse.Node(), validate=True)
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == 'html SYSTEM "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"'

	e = parse.tree(b'<!DOCTYPE a [<!ELEMENT a EMPTY><!--gurk-->]><a/>', parse.Expat(doctype=True), parse.NS(html), parse.Node(), validate=True)
	assert isinstance(e[0], xsc.DocType)
	assert e[0].content == 'a' # Internal subset gets dropped


@pytest.mark.lxml
def test_htmlparse_base():
	e = parse.tree(b"<a href='gurk.gif'/>", parse.Tidy(), parse.NS(html), parse.Node(base="hurz/index.html"), validate=True)
	e = e.walknodes(html.a)[0]
	assert str(e.attrs.href) == "hurz/gurk.gif"


@pytest.mark.lxml
def test_parse_tidy_attrs():
	e = parse.tree(b"<a xmlns:xl='http://www.w3.org/1999/xlink' xml:lang='de' xl:href='gurk.gif' href='gurk.gif'/>", parse.Tidy(), parse.NS(html), parse.Node(pool=xsc.Pool(html, xml, xlink)), validate=True)
	a = e.walknodes(html.a)[0]
	assert str(a.attrs["href"]) == "gurk.gif"
	assert str(a.attrs[xml.Attrs.lang]) == "de"
	assert str(a.attrs[xlink.Attrs.href]) == "gurk.gif"


@pytest.mark.lxml
def test_parse_tidy_empty():
	e = parse.tree(b"", parse.Tidy(), parse.NS(), parse.Node(), validate=True)
	assert not e


def test_base():
	e = parse.tree(parse.String(b'<a xmlns="http://www.w3.org/1999/xhtml" href="gurk.html"/>', 'http://www.gurk.de/'), parse.Expat(ns=True), parse.Node(pool=xsc.Pool(html)), validate=True)
	assert str(e[0].attrs.href) == "http://www.gurk.de/gurk.html"


def test_stringsource():
	expect = b"hinz & kunz"
	source = parse.String(expect)
	for i in range(3):
		parsed = b"".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_itersource():
	expect = b"hinz & kunz"
	source = parse.Iter([b"hinz", b" & ", b"kunz"])
	for i in range(3):
		parsed = b"".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_filesource():
	expect = open("setup.py", "rb").read()
	source = parse.File("setup.py", bufsize=32)
	for i in range(3):
		parsed = b"".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_streamsource():
	# Stream objects are not reusable
	expect = open("setup.py", "rb").read()
	parsed = b"".join(event[1] for event in parse.Stream(open("setup.py", "rb"), bufsize=32) if event[0] == "bytes")
	assert parsed == expect


@pytest.mark.net
def test_urlsource():
	expect = url.URL("http://www.python.org/").openread().read()
	source = parse.URL("http://www.python.org/", bufsize=32)
	for i in range(3):
		parsed = b"".join(data for (evtype, data) in source if evtype == "bytes")
		assert parsed == expect


def test_itertree_large():
	def xml():
		yield f"<ul xmlns='{html.xmlns}'>".encode("utf-8")
		for i in range(1000):
			yield f"<li>{i}</li>".encode("utf-8")
		yield "</ul>".encode("utf-8")

	for (i, c) in enumerate(parse.itertree(parse.Iter(xml()), parse.Expat(ns=True), parse.Node(), selector=html.li, validate=True)):
		assert int(str(c.node)) == i
		c.path[-2].content.clear()


def test_itertree_skip():
	def xml():
		yield f"<ul xmlns='{html.xmlns}'>".encode("utf-8")
		for i in range(10):
			yield f"<li>{i}</li>".encode("utf-8")
		yield "</ul>".encode("utf-8")

	for c in parse.itertree(parse.Iter(xml()), parse.Expat(ns=True), parse.Node(), enterelementnode=True, validate=True):
		if isinstance(c.node, html.ul):
			c.entercontent = False
		assert not isinstance(c.node, html.li)


def test_expat_events_on_exception():
	# Test that all collected events are output before an exception is thrown
	i = parse.events(b"<x/>schrott", parse.Expat())
	assert next(i) == ("url", url.URL("STRING"))
	assert next(i) == ("position", (0, 0))
	assert next(i) == ("enterstarttag", "x")
	assert next(i) == ("leavestarttag", "x")
	assert next(i) == ("position", (0, 4))
	assert next(i) == ("endtag", "x")
	with pytest.raises(expat.ExpatError):
		next(i)


def test_expat_no_multiple_text_events():
	# Test that we don't get consecutive text events with expat
	i = parse.events(parse.Iter(b"<a>gurk &amp; hurz &amp; hinz &amp; kunz</a>"), parse.Expat())
	assert next(i) == ("url", url.URL("ITER"))
	assert next(i) == ("position", (0, 0))
	assert next(i) == ("enterstarttag", "a")
	assert next(i) == ("leavestarttag", "a")
	assert next(i) == ("position", (0, 4))
	assert next(i) == ("text", "gurk & hurz & hinz & kunz")
	assert next(i) == ("position", (0, 40))
	assert next(i) == ("endtag", "a")
	with pytest.raises(StopIteration):
		next(i)


def test_sgmlop_no_multiple_text_events():
	# Test that we don't get consecutive text events with sgmlop
	i = parse.events(parse.Iter(b"<a>gurk &amp; hurz &amp; hinz &amp; kunz</a>"), parse.SGMLOP())
	assert next(i) == ("url", url.URL("ITER"))
	assert next(i) == ("enterstarttag", "a")
	assert next(i) == ("leavestarttag", "a")
	assert next(i) == ("text", "gurk & hurz & hinz & kunz")
	assert next(i) == ("endtag", "a")
	with pytest.raises(StopIteration):
		next(i)


def test_plain_element():
	with warnings.catch_warnings(record=True) as ws:
		node = parse.tree(b"<a xmlns='gurk'/>", parse.Expat(ns=True), parse.Node(pool=xsc.Pool()), validate=True)[0]

	assert node.__class__ is xsc.Element
	assert node.xmlns == "gurk"
	assert node.xmlname == "a"

	assert len(ws) == 1
	assert issubclass(ws[0].category, xsc.UndeclaredNodeWarning)


def test_plain_entity():
	with warnings.catch_warnings(record=True) as ws:
		node = parse.tree(b"<a xmlns='gurk'>&hurz;</a>", parse.Expat(ns=True), parse.Node(pool=xsc.Pool()), validate=True)[0][0]

	assert node.__class__ is xsc.Entity
	assert node.xmlname == "hurz"

	assert len(ws) == 2
	assert all(issubclass(w.category, xsc.UndeclaredNodeWarning) for w in ws)


def test_plain_procinst():
	with warnings.catch_warnings(record=True) as ws:
		node = parse.tree(b"<a xmlns='gurk'><?hurz text?></a>", parse.Expat(ns=True), parse.Node(pool=xsc.Pool()), validate=True)[0][0]

	assert node.__class__ is xsc.ProcInst
	assert node.xmlname == "hurz"
	assert node.content == "text"

	assert len(ws) == 2
	assert all(issubclass(w.category, xsc.UndeclaredNodeWarning) for w in ws)
