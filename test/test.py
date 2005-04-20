#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

import sys, unittest, cStringIO, warnings, re, cPickle

from xml.sax import saxlib
from xml.parsers import expat

from ll import url
from ll.xist import xsc, parsers, cssparsers, presenters, converters, helpers, options, sims, xnd, xfind
from ll.xist.ns import wml, ihtml, html, chars, css, abbr, specials, htmlspecials, php, xml, tld


# set to something ASCII, so presenters work, even if the system default encoding is ascii
options.reprtab = "  "


# The following includes \x00 in addition to those characters defined in
# http://www.w3.org/TR/2004/REC-xml11-20040204/#NT-RestrictedChar
restrictedchars = re.compile(u"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]")


def createattr():
	return html.span.Attrs.lang(
		True,
		False,
		url.URL("http://www.python.org/"),
		html.abbr(
			xml.XML10(),
			"hurz",
			specials.tab(),
			abbr.xist(),
			None,
			1,
			2.0,
			"3",
			u"4",
			(5, 6),
			[7, 8],
			html.span("gurk"),
			title="hurz"
		)
	)


def createattrs():
	return html.span.Attrs(
		lang=(
			True,
			False,
			url.URL("http://www.python.org/"),
			html.abbr(
				xml.XML10(),
				"hurz",
				specials.tab(),
				abbr.xist(),
				None,
				1,
				2.0,
				"3",
				u"4",
				(5, 6),
				[7, 8],
				html.span("gurk"),
				title="hurz"
			)
		)
	)


def createelement():
	return html.span(
		1,
		2,
		class_="gurk",
		id=(1, 2, (3, 4)),
		lang=(
			True,
			False,
			url.URL("http://www.python.org/"),
			html.abbr(
				xml.XML10(),
				"hurz",
				specials.tab(),
				abbr.xist(),
				None,
				1,
				2.0,
				"3",
				u"4",
				(5, 6),
				[7, 8],
				html.span("gurk"),
				title="hurz"
			)
		)
	)


def createfrag():
	return xsc.Frag(
		xml.XML10(),
		html.DocTypeHTML401transitional(),
		xsc.Comment("gurk"),
		"hurz",
		specials.tab(),
		abbr.xist(),
		None,
		True,
		False,
		1,
		2.0,
		"3",
		u"4",
		(5, 6),
		[7, 8],
		html.div(
			align="left"
		),
		url.URL("http://www.python.org/"),
		html.span(
			1,
			2,
			class_="gurk",
			id=(1, 2, (3, 4)),
			lang=(
				True,
				False,
				url.URL("http://www.python.org/"),
				html.abbr(
					xml.XML10(),
					"hurz",
					specials.tab(),
					abbr.xist(),
					None,
					1,
					2.0,
					"3",
					u"4",
					(5, 6),
					[7, 8],
					html.span("gurk"),
					title="hurz"
				)
			)
		)
	)


def allnodes():
	return (xsc.Null, createattr(), createattrs(), createelement(), createfrag())


class XISTTest(unittest.TestCase):
	def check_lenunicode(self, node, _len, content):
		self.assertEqual(len(node), _len)
		self.assertEqual(unicode(node), content)

	def test_frageq(self):
		self.assertEqual(xsc.Frag(), xsc.Frag())
		self.assertEqual(xsc.Frag(1), xsc.Frag(1))
		self.assertEqual(xsc.Frag(1, 2), xsc.Frag(1, 2, None))
		self.assertNotEqual(xsc.Frag(1, 2), xsc.Frag(12))
		self.assertNotEqual(xsc.Frag(), xsc.Frag(""))
		self.assertNotEqual(xsc.Frag(""), xsc.Frag("", ""))

	def test_elementeq(self):
		self.assertEqual(html.div(), html.div())
		self.assertEqual(html.div(1), html.div(1))
		self.assertEqual(html.div(1, 2), html.div(1, 2, None))
		self.assertNotEqual(html.div(1, 2), html.div(12))
		self.assertNotEqual(html.div(), html.div(""))
		self.assertNotEqual(html.div(""), html.div("", ""))
		self.assertEqual(html.div(1, html.div(2, html.div(3))), html.div(1, html.div(2, html.div(3))))

	def test_texteq(self):
		self.assertEqual(xsc.Text(), xsc.Text())
		self.assertEqual(xsc.Text(1), xsc.Text(1))
		self.assertEqual(xsc.Text("1"), xsc.Text(1))
		self.assertEqual(xsc.Text(u"1"), xsc.Text(1))

	def test_commenteq(self):
		self.assertEqual(xsc.Comment(), xsc.Comment())
		self.assertEqual(xsc.Comment(1), xsc.Comment(1))
		self.assertEqual(xsc.Comment("1"), xsc.Comment(1))
		self.assertEqual(xsc.Comment(u"1"), xsc.Comment(1))

	def test_doctypeeq(self):
		self.assertEqual(xsc.DocType(), xsc.DocType())
		self.assertEqual(xsc.DocType(1), xsc.DocType(1))
		self.assertEqual(xsc.DocType("1"), xsc.DocType(1))
		self.assertEqual(xsc.DocType(u"1"), xsc.DocType(1))

	def test_mixeq(self):
		self.assertNotEqual(xsc.Comment(1), xsc.Text(1))
		self.assertNotEqual(xsc.DocType(1), xsc.Text(1))
		self.assertNotEqual(xsc.DocType(1), xsc.Text(1))

	def test_fraglen(self):
		self.check_lenunicode(xsc.Frag(), 0, u"")
		self.check_lenunicode(xsc.Frag(1), 1, u"1")
		self.check_lenunicode(xsc.Frag(1, 2, 3), 3, u"123")
		self.check_lenunicode(xsc.Frag(None), 0, u"")
		self.check_lenunicode(xsc.Frag(None, None, None), 0, u"")
		self.check_lenunicode(xsc.Frag(1, None, 2, None, 3, None, 4), 4, u"1234")
		self.check_lenunicode(xsc.Frag(1, (2, 3)), 3, u"123")
		self.check_lenunicode(xsc.Frag(1, (None, None)), 1, u"1")

	def test_append(self):
		for cls in (xsc.Frag, html.div):
			node = cls()
			node.append(1)
			self.check_lenunicode(node, 1, u"1")
			node.append(2)
			self.check_lenunicode(node, 2, u"12")
			node.append()
			self.check_lenunicode(node, 2, u"12")
			node.append(3, 4)
			self.check_lenunicode(node, 4, u"1234")
			node.append(None)
			self.check_lenunicode(node, 4, u"1234")
			node.append((5, 6))
			self.check_lenunicode(node, 6, u"123456")

	def test_extend(self):
		for cls in (xsc.Frag, html.div):
			node = cls()
			node.extend([1])
			self.check_lenunicode(node, 1, u"1")
			node.extend([2])
			self.check_lenunicode(node, 2, u"12")
			node.extend([])
			self.check_lenunicode(node, 2, u"12")
			node.extend([None])
			self.check_lenunicode(node, 2, u"12")
			node.extend([3, 4])
			self.check_lenunicode(node, 4, u"1234")
			node.extend([[], [[], [5], []]])
			self.check_lenunicode(node, 5, u"12345")

	def test_insert(self):
		for cls in (xsc.Frag, html.div):
			node = cls()
			node.insert(0, 1)
			self.check_lenunicode(node, 1, u"1")
			node.insert(0, 2)
			self.check_lenunicode(node, 2, u"21")
			node.insert(0, 3, 4)
			self.check_lenunicode(node, 4, u"3421")
			node.insert(0, None)
			self.check_lenunicode(node, 4, u"3421")
			node.insert(0, (5, 6))
			self.check_lenunicode(node, 6, u"563421")

	def test_iadd(self):
		for cls in (xsc.Frag, html.div):
			node = cls()
			node += [1]
			self.check_lenunicode(node, 1, u"1")
			node += [2]
			self.check_lenunicode(node, 2, u"12")
			node += []
			self.check_lenunicode(node, 2, u"12")
			node += [None]
			self.check_lenunicode(node, 2, u"12")
			node += [3, 4]
			self.check_lenunicode(node, 4, u"1234")
			node += [[], [[], [5], []]]
			self.check_lenunicode(node, 5, u"12345")

	def test_len(self):
		for cls in (xsc.Frag, html.div):
			self.check_lenunicode(cls(), 0, u"")
			self.check_lenunicode(cls(1), 1, u"1")
			self.check_lenunicode(cls(1, 2, 3), 3, u"123")
			self.check_lenunicode(cls(None), 0, u"")
			self.check_lenunicode(cls(None, None, None), 0, u"")
			self.check_lenunicode(cls(1, None, 2, None, 3, None, 4), 4, u"1234")
			self.check_lenunicode(cls(1, (2, 3)), 3, u"123")
			self.check_lenunicode(cls(1, (None, None)), 1, u"1")

	def test_standardmethods(self):
		for node in allnodes():
			node.compact()
			node.normalized()
			list(node.walk((True, xsc.enterattrs, xsc.entercontent)))
			node.find((True, xsc.enterattrs, xsc.entercontent))
			node.pretty()
			node.clone()
			node.conv()
			node.normalized().compact().pretty()

	def test_standardmethods2(self):
		for node in (createelement(), createfrag()):
			node.sorted()
			node.shuffled()
			node.reversed()

	def test_stringify(self):
		for node in allnodes():
			unicode(node)
			str(node)
			node.asString()
			node.asBytes()

	def test_asText(self):
		for node in allnodes():
			node.asText()
			node.asText(monochrome=True)
			node.asText(squeezeBlankLines=True)
			node.asText(lineNumbers=True)
			node.asText(width=120)

	def test_number(self):
		node = html.div(class_=1234)
		self.assertEqual(int(node["class_"]), 1234)
		self.assertEqual(long(node["class_"]), 1234L)
		self.assertAlmostEqual(float(node["class_"]), 1234.)
		node = html.div(class_="1+1j")
		compl = complex(node["class_"])
		self.assertAlmostEqual(compl.real, 1.)
		self.assertAlmostEqual(compl.imag, 1.)

	def test_prefix(self):
		node = html.div()
		self.assertEqual(node.xmlprefix(), "html")

	def test_write(self):
		node = html.div()
		io = cStringIO.StringIO()
		node.write(io, xhtml=2)
		self.assertEqual(io.getvalue(), "<div/>")

	def test_mul(self):
		node = xsc.Frag("a")
		self.assertEqual(3*node, xsc.Frag(list("aaa")))
		self.assertEqual(node*3, xsc.Frag(list("aaa")))

		node = html.div()
		self.assertEqual(3*node, xsc.Frag(html.div(), html.div(), html.div()))
		self.assertEqual(node*3, xsc.Frag(html.div(), html.div(), html.div()))

	def test_text(self):
		s = "test"
		node = xsc.Text(s)
		hash(node)
		self.assertEqual(len(node), 4)
		self.assertEqual(node[1], xsc.Text("e"))
		self.assertEqual(3*node, xsc.Text(3*s))
		self.assertEqual(node*3, xsc.Text(s*3))
		self.assertEqual(node[1:3], xsc.Text("es"))
		self.assertEqual(node.capitalize(), xsc.Text("Test"))
		self.assertEqual(node.center(8), xsc.Text("  test  "))
		self.assertEqual(node.count("t"), 2)
		self.assertEqual(node.endswith("st"), True)
		self.assertEqual(node.index("s"), 2)
		self.assertEqual(node.isalpha(), True)
		self.assertEqual(node.isalnum(), True)
		self.assertEqual(node.isdecimal(), False)
		self.assertEqual(node.isdigit(), False)
		self.assertEqual(node.islower(), True)
		self.assertEqual(node.isnumeric(), False)
		self.assertEqual(node.isspace(), False)
		self.assertEqual(node.istitle(), False)
		self.assertEqual(node.isupper(), False)
		self.assertEqual(node.join(xsc.Frag(list("abc"))), xsc.Frag("a", "test", "b", "test", "c"))
		self.assertEqual(node.ljust(6), xsc.Text("test  "))
		self.assertEqual(node.ljust(6, "."), xsc.Text("test.."))
		self.assertEqual(node.lower(), xsc.Text("test"))
		self.assertEqual(xsc.Text("  test").lstrip(), xsc.Text("test"))
		self.assertEqual(node.replace("s", "x"), xsc.Text("text"))
		self.assertEqual(node.rjust(6), xsc.Text("  test"))
		self.assertEqual(node.rjust(6, "."), xsc.Text("..test"))
		self.assertEqual(xsc.Text("test  ").rstrip(), xsc.Text("test"))
		self.assertEqual(node.rfind("s"), 2)
		self.assertEqual(node.rindex("s"), 2)
		self.assertEqual(node.split("e"), xsc.Frag("t", "st"))
		self.assertEqual(xsc.Text("a\nb\n").splitlines(), xsc.Frag("a", "b"))
		self.assertEqual(node.startswith("te"), True)
		self.assertEqual(xsc.Text("  test  ").strip(), xsc.Text("test"))
		self.assertEqual(node.swapcase(), xsc.Text("TEST"))
		self.assertEqual(node.title(), xsc.Text("Test"))
		self.assertEqual(node.upper(), xsc.Text("TEST"))

	def test_charref(self):
		node = chars.ouml()
		hash(node)
		self.assertEqual(len(node), 1)
		self.assertEqual(node[0], xsc.Text(u"ö"))
		self.assertEqual(3*node, xsc.Text(u"ööö"))
		self.assertEqual(node*3, xsc.Text(u"ööö"))
		self.assertEqual(node[1:-2], xsc.Text())
		self.assertEqual(node.capitalize(), xsc.Text(u"Ö"))
		self.assertEqual(node.center(5), xsc.Text(u"  ö  "))
		self.assertEqual(node.count(u"t"), 0)
		self.assertEqual(node.endswith(u"ö"), True)
		self.assertEqual(node.index(u"ö"), 0)
		self.assertEqual(node.isalpha(), True)
		self.assertEqual(node.isalnum(), True)
		self.assertEqual(node.isdecimal(), False)
		self.assertEqual(node.isdigit(), False)
		self.assertEqual(node.islower(), True)
		self.assertEqual(node.isnumeric(), False)
		self.assertEqual(node.isspace(), False)
		self.assertEqual(node.istitle(), False)
		self.assertEqual(node.isupper(), False)
		self.assertEqual(node.ljust(3), xsc.Text(u"ö  "))
		self.assertEqual(node.ljust(3, "."), xsc.Text(u"ö.."))
		self.assertEqual(node.lower(), xsc.Text(u"ö"))
		self.assertEqual(node.replace(u"ö", "x"), xsc.Text("x"))
		self.assertEqual(node.rjust(3), xsc.Text(u"  ö"))
		self.assertEqual(node.rjust(3, "."), xsc.Text(u"..ö"))
		self.assertEqual(node.rfind(u"ö"), 0)
		self.assertEqual(node.rindex(u"ö"), 0)
		self.assertEqual(node.startswith(u"ö"), True)
		self.assertEqual(node.swapcase(), xsc.Text(u"Ö"))
		self.assertEqual(node.title(), xsc.Text(u"Ö"))
		self.assertEqual(node.upper(), xsc.Text(u"Ö"))

	def test_getsetitem(self):
		for cls in (xsc.Frag, html.div):
			for attr in ("class_", (xml, "lang")):
				node = cls(html.div("foo", html.div({attr: "gurk"}), "bar"))
				self.assert_(node[[]] is node)
				self.assertEqual(str(node[[0, 1, attr]]), "gurk")
				node[[0, 1, attr]] = "hurz"
				self.assertEqual(str(node[[0, 1, attr]]), "hurz")
				i = node[0][xsc.Text]
				self.assertEqual(str(i.next()), "foo")
				self.assertEqual(str(i.next()), "bar")
				self.assertRaises(StopIteration, i.next)
				self.assertRaises(ValueError, node.__setitem__, [], None)
				self.assertRaises(ValueError, node.__delitem__, [])

	def mappedmapper(self, node, converter):
		if isinstance(node, xsc.Text):
			node = node.replace("gurk", "hurz")
		return node

	def test_conv(self):
		node = createfrag()
		node.conv()
		node.conv(converters.Converter())
		node.mapped(self.mappedmapper, converters.Converter())

	def test_repr(self):
		tests = allnodes()
		allpresenters = [c for c in presenters.__dict__.itervalues() if isinstance(c, type) and c is not presenters.Presenter and issubclass(c, presenters.Presenter)]
		for node in tests:
			repr(node)
			for class_ in allpresenters:
				presenter = class_()
				# do it multiple time, to make sure the presenter gets properly reset
				for i in xrange(3):
					node.repr(presenter)
			for showlocation in (False, True):
				for showpath in (False, True):
					presenter = presenters.TreePresenter(showlocation=showlocation, showpath=showpath)
					# do it multiple time, to make sure the presenter gets properly reset
					for i in xrange(3):
						node.repr(presenter)

	def test_locationeq(self):
		l1 = xsc.Location(sysid="gurk", pubid="http://gurk.com", line=42, col=666)
		l2 = xsc.Location(sysid="gurk", pubid="http://gurk.com", line=42, col=666)
		l3 = xsc.Location(sysid="hurz", pubid="http://gurk.com", line=42, col=666)
		l4 = xsc.Location(sysid="gurk", pubid="http://hurz.com", line=42, col=666)
		l5 = xsc.Location(sysid="gurk", pubid="http://gurk.com", line=43, col=666)
		l6 = xsc.Location(sysid="gurk", pubid="http://gurk.com", line=43, col=667)
		l7 = xsc.Location(sysid="gurk", pubid="http://gurk.com")
		self.assertEqual(l1, l2)
		self.assertNotEqual(l1, l3)
		self.assertNotEqual(l1, l4)
		self.assertNotEqual(l1, l5)
		self.assertNotEqual(l1, l6)
		self.assertNotEqual(l1, l7)

	def test_locationoffset(self):
		l1 = xsc.Location(sysid="gurk", pubid="http://gurk.com", line=42, col=666)
		self.assertEqual(l1, l1.offset(0))
		l2 = l1.offset(1)
		self.assertEqual(l1.getSystemId(), l2.getSystemId())
		self.assertEqual(l1.getPublicId(), l2.getPublicId())
		self.assertEqual(l1.getLineNumber()+1, l2.getLineNumber())

	def test_attrsclone(self):
		class newa(html.a):
			def convert(self, converter):
				attrs = self.attrs.clone()
				attrs["href"].insert(0, "foo")
				e = html.a(self.content, attrs)
				return e.convert(converter)
		e = newa("gurk", href="hurz")
		e = e.conv().conv()
		self.assertEqual(unicode(e["href"]), "foohurz")
		self.assertEqual(str(e["href"]), "foohurz")

	def test_attributes(self):
		node = html.h1("gurk", {(xml, "lang"): "de"}, lang="de")
		self.assert_(node.attrs.has("lang"))
		self.assert_(node.attrs.has((xml, "lang")))

	def check_attributekeysvaluesitems(self, node, xml, attrname, attrvalue):
		self.assertEquals(node.attrs.allowedkeys(xml=xml), [attrname])
		iter = node.attrs.iterallowedkeys(xml=xml)
		self.assertEquals(iter.next(), attrname)
		self.assertRaises(StopIteration, iter.next)

		self.assertEquals(node.attrs.allowedvalues(), [node.Attrs.attr_])
		iter = node.attrs.iterallowedvalues()
		self.assertEquals(iter.next(), node.Attrs.attr_)
		self.assertRaises(StopIteration, iter.next)

		self.assertEquals(node.attrs.alloweditems(xml=xml), [(attrname, node.Attrs.attr_)])
		iter = node.attrs.iteralloweditems(xml=xml)
		self.assertEquals(iter.next(), (attrname, node.Attrs.attr_))
		self.assertRaises(StopIteration, iter.next)

		if attrvalue:
			self.assertEquals(node.attrs.keys(xml=xml), [attrname])
			iter = node.attrs.iterkeys(xml=xml)
			self.assertEquals(iter.next(), attrname)
			self.assertRaises(StopIteration, iter.next)
		else:
			self.assertEquals(node.attrs.keys(xml=xml), [])
			iter = node.attrs.iterkeys(xml=xml)
			self.assertRaises(StopIteration, iter.next)

		if attrvalue:
			res = node.attrs.values()
			self.assertEquals(len(res), 1)
			self.assertEquals(res[0].__class__, node.Attrs.attr_)
			self.assertEquals(unicode(res[0]), attrvalue)
			iter = node.attrs.itervalues()
			res = iter.next()
			self.assertEquals(res.__class__, node.Attrs.attr_)
			self.assertEquals(unicode(res), attrvalue)
			self.assertRaises(StopIteration, iter.next)
		else:
			res = node.attrs.values()
			self.assertEquals(len(res), 0)
			iter = node.attrs.itervalues()
			self.assertRaises(StopIteration, iter.next)

		if attrvalue:
			res = node.attrs.items(xml=xml)
			self.assertEquals(len(res), 1)
			self.assertEquals(res[0][0], attrname)
			self.assertEquals(res[0][1].__class__, node.Attrs.attr_)
			self.assertEquals(unicode(res[0][1]), attrvalue)
			iter = node.attrs.iteritems(xml=xml)
			res = iter.next()
			self.assertEquals(res[0], attrname)
			self.assertEquals(res[1].__class__, node.Attrs.attr_)
			self.assertEquals(unicode(res[1]), attrvalue)
			self.assertRaises(StopIteration, iter.next)
		else:
			res = node.attrs.items(xml=xml)
			self.assertEquals(len(res), 0)
			iter = node.attrs.iteritems(xml=xml)
			self.assertRaises(StopIteration, iter.next)

	def test_attributekeysvaluesitems(self):
		class Test1(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class attr_(xsc.TextAttr):
					xmlname = "attr"
					default = 42
		class Test2(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class attr_(xsc.TextAttr):
					xmlname = "attr"

		for (xml, attrname) in ((False, u"attr_"), (True, u"attr")):
			self.check_attributekeysvaluesitems(Test1(), xml, attrname, u"42")
			self.check_attributekeysvaluesitems(Test1(attr_=17), xml, attrname, u"17")
			self.check_attributekeysvaluesitems(Test1(attr_=None), xml, attrname, None)

			self.check_attributekeysvaluesitems(Test2(), xml, attrname, None)
			self.check_attributekeysvaluesitems(Test2(attr_=17), xml, attrname, u"17")
			self.check_attributekeysvaluesitems(Test2(attr_=None), xml, attrname, None)

	def test_attributeswithout(self):
		# Use a sub namespace of xml to test the issubclass checks
		class xml2(xml):
			class Attrs(xml.Attrs):
				class lang(xml.Attrs.lang):
					default = 42

		node = html.h1("gurk",
			{(xml2, "space"): 1, (xml2, "lang"): "de", (xml2, "base"): "http://www.livinglogic.de/"},
			lang="de",
			style="color: #fff",
			align="right",
			title="gurk",
			class_="important",
			id=42,
			dir="ltr"
		)
		keys = node.attrs.keys()
		keys.sort()
		keys.remove("class_")

		keys1 = node.attrs.without(["class_"]).keys()
		keys1.sort()
		self.assertEqual(keys, keys1)

		keys.remove((xml2, "space"))
		keys2 = node.attrs.without(["class_", (xml, "space")]).keys()
		keys2.sort()
		self.assertEqual(keys, keys2)

		keys.remove((xml2, "lang"))
		keys.remove((xml2, "base"))
		keys3 = node.attrs.without(["class_"], [xml]).keys()
		keys3.sort()
		self.assertEqual(keys, keys3)

		# Check that non existing attrs are handled correctly
		keys4 = node.attrs.without(["class_", "src"], keepglobals=False).keys()
		keys4.sort()
		self.assertEqual(keys, keys4)

	def test_attributeswith(self):
		# Use a sub namespace of xml to test the issubclass checks
		class xml2(xml):
			class Attrs(xml.Attrs):
				class lang(xml.Attrs.lang):
					default = 42

		node = html.h1("gurk",
			{(xml2, "space"): 1, (xml2, "lang"): "de"},
			lang="de",
			align="right"
		)
		keys = node.attrs.keys()
		keys.sort()
		keys.remove("lang")

		self.assertEquals(node.attrs.with(["lang"]).keys(), ["lang"])

		keys1 = node.attrs.with(["lang", "align"]).keys()
		keys1.sort()
		self.assertEqual(keys1, ["align", "lang"])

		keys = ["lang", (xml2, "lang")]
		keys.sort()
		keys2 = node.attrs.with(keys).keys()
		keys2.sort()
		self.assertEqual(keys2, keys)

		keys = ["lang", (xml2, "lang"), (xml2, "space")]
		keys.sort()
		keys3 = node.attrs.with(["lang"], [xml]).keys()
		keys3.sort()
		self.assertEqual(keys3, keys)

	def test_defaultattributes(self):
		class Test(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class withdef(xsc.TextAttr):
					default = 42
				class withoutdef(xsc.TextAttr):
					pass
		node = Test()
		self.assert_(node.attrs.has("withdef"))
		self.assert_(not node.attrs.has("withoutdef"))
		self.assertRaises(xsc.IllegalAttrError, node.attrs.has, "illegal")
		node = Test(withdef=None)
		self.assert_(not node.attrs.has("withdef"))

	def check_listiter(self, listexp, *lists):
		for l in lists:
			count = 0
			for item in l:
				self.assert_(item in listexp)
				count += 1
			self.assertEqual(count, len(listexp))

	def test_attributedictmethods(self):
		class Test(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class withdef(xsc.TextAttr):
					default = 42
				class withoutdef(xsc.TextAttr):
					pass
				class another(xsc.URLAttr):
					pass

		node = Test(withoutdef=42)

		self.check_listiter(
			[ "withdef", "withoutdef" ],
			node.attrs.keys(),
			node.attrs.iterkeys()
		)
		self.check_listiter(
			[ Test.Attrs.withdef(42), Test.Attrs.withoutdef(42)],
			node.attrs.values(),
			node.attrs.itervalues()
		)
		self.check_listiter(
			[ ("withdef", Test.Attrs.withdef(42)), ("withoutdef", Test.Attrs.withoutdef(42)) ],
			node.attrs.items(),
			node.attrs.iteritems()
		)

		self.check_listiter(
			[ "another", "withdef", "withoutdef" ],
			node.attrs.allowedkeys(),
			node.attrs.iterallowedkeys()
		)
		self.check_listiter(
			[ Test.Attrs.another, Test.Attrs.withdef, Test.Attrs.withoutdef ],
			node.attrs.allowedvalues(),
			node.attrs.iterallowedvalues()
		)
		self.check_listiter(
			[ ("another", Test.Attrs.another), ("withdef", Test.Attrs.withdef), ("withoutdef", Test.Attrs.withoutdef) ],
			node.attrs.alloweditems(),
			node.attrs.iteralloweditems()
		)

	def test_fragattrdefault(self):
		class testelem(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class testattr(xsc.TextAttr):
					default = 42

		node = testelem()
		self.assertEquals(unicode(node["testattr"]), "42")
		self.assertEquals(unicode(node.conv()["testattr"]), "42")

		node["testattr"].clear()
		self.assert_(not node.attrs.has("testattr"))
		self.assert_(not node.conv().attrs.has("testattr"))

		node = testelem(testattr=23)
		self.assertEquals(unicode(node["testattr"]), "23")
		self.assertEquals(unicode(node.conv()["testattr"]), "23")

		del node["testattr"]
		self.assertEquals(unicode(node["testattr"]), "")
		self.assertEquals(unicode(node.conv()["testattr"]), "")

		node["testattr"] = 23
		node["testattr"] = None
		self.assert_("testattr" not in node.attrs)
		self.assert_("testattr" not in node.conv().attrs)

		node = testelem(testattr=None)
		self.assert_("testattr" not in node.attrs)
		self.assert_("testattr" not in node.conv().attrs)

	def test_checkisallowed(self):
		class testelem(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class testattr(xsc.TextAttr):
					pass

		class testelem2(testelem):
			pass

		class testelem3(testelem2):
			class Attrs(testelem2.Attrs):
				class testattr3(xsc.TextAttr):
					pass

		class testelem4(testelem3):
			class Attrs(testelem3.Attrs):
				testattr = None

		node = testelem()
		self.assertEquals(node.attrs.isallowed("testattr"), True)
		self.assertEquals(node.attrs.isallowed("notestattr"), False)

		node = testelem2()
		self.assertEquals(node.attrs.isallowed("testattr"), True)
		self.assertEquals(node.attrs.isallowed("notestattr"), False)

		node = testelem3()
		self.assertEquals(node.attrs.isallowed("testattr"), True)
		self.assertEquals(node.attrs.isallowed("testattr3"), True)

		node = testelem4()
		self.assertEquals(node.attrs.isallowed("testattr"), False)
		self.assertEquals(node.attrs.isallowed("testattr3"), True)

	def test_withsep(self):
		for class_ in (xsc.Frag, html.div):
			node = class_(1,2,3)
			self.assertEquals(unicode(node.withsep(",")), u"1,2,3")
			node = class_(1)
			self.assertEquals(unicode(node.withsep(",")), u"1")
			node = class_()
			self.assertEquals(unicode(node.withsep(",")), u"")

	def test_allowedattr(self):
		self.assertEquals(html.a.Attrs.allowedattr("href"), html.a.Attrs.href)
		self.assertRaises(xsc.IllegalAttrError, html.a.Attrs.allowedattr, "gurk")
		self.assertEquals(html.a.Attrs.allowedattr((xml, "lang")), xml.Attrs.lang)

	def test_plaintableattrs(self):
		e = htmlspecials.plaintable(border=3)
		self.assert_(isinstance(e["border"], html.table.Attrs.border))
		self.assert_(isinstance(e["cellpadding"], html.table.Attrs.cellpadding))
		e = e.conv()
		self.assert_(isinstance(e["border"], html.table.Attrs.border))
		self.assert_(isinstance(e["cellpadding"], html.table.Attrs.cellpadding))

	def test_attrupdate(self):
		node = html.a(href="gurk", class_="hurz")
		node.attrs.update(xml.Attrs(lang="de"), {"href": "gurk2", "id": 42})
		self.assertEquals(unicode(node["href"]), u"gurk2")
		self.assertEquals(unicode(node["id"]), u"42")
		self.assertEquals(unicode(node[(xml, "lang")]), u"de")

		node = html.a(href="gurk", class_="hurz")
		node.attrs.updatenew(xml.Attrs(lang="de"), {"href": "gurk2", "id": 42})
		self.assertEquals(unicode(node["href"]), u"gurk")
		self.assertEquals(unicode(node["id"]), u"42")
		self.assertEquals(unicode(node[(xml, "lang")]), u"de")

		node = html.a(href="gurk", class_="hurz")
		node.attrs.updateexisting({"href": "gurk2", "id": 42})
		self.assertEquals(unicode(node["href"]), u"gurk2")
		self.assertEquals("id" in node.attrs, False)
		self.assertEquals((xml, "lang") in node.attrs, False)

		node = html.a({(xml, "lang"): "de"}, href="gurk", class_="hurz")
		self.assertEquals(unicode(node[(xml, "lang")]), u"de")

		node = html.a(xml.Attrs(lang="de"), href="gurk", class_="hurz")
		self.assertEquals(unicode(node[(xml, "lang")]), u"de")

		class Gurk(xsc.Element):
			model = False
			class Attrs(xsc.Element.Attrs):
				class gurk(xsc.TextAttr): pass
				class hurz(xsc.TextAttr): default = "hinz+kunz"

		node1 = Gurk()
		node2 = Gurk(hurz=None)
		node1.attrs.update(node2.attrs)
		self.assert_("hurz" not in node1.attrs)

		node1 = Gurk(hurz=None)
		node2 = Gurk()
		node1.attrs.update(node2.attrs)
		self.assert_("hurz" in node1.attrs)

		node = Gurk(Gurk(hurz=None).attrs)
		self.assert_("hurz" not in node.attrs)

		attrs = Gurk.Attrs(Gurk.Attrs(hurz=None))
		self.assert_("hurz" not in attrs)

		# No global attributes inside global attributes
		self.assertRaises(xsc.IllegalAttrError, xml.Attrs, xml.Attrs(lang="de"))

	def test_classrepr(self):
		repr(xsc.Base)
		repr(xsc.Node)
		repr(xsc.Null.__class__)
		repr(xsc.Element)
		repr(xsc.ProcInst)
		repr(xsc.Entity)
		repr(xsc.CharRef)
		repr(xsc.Element.Attrs)
		repr(xml.Attrs)
		repr(xml.Attrs.lang)

	def test_itemslice(self):
		for cls in (xsc.Frag, html.div):
			# __get(item|slice)__
			e = cls(range(6))
			self.assertEqual(e[2], xsc.Text(2))
			self.assertEqual(e[-1], xsc.Text(5))
			self.assertEqual(e[:], e)
			self.assertEqual(e[:2], cls(0, 1))
			self.assertEqual(e[-2:], cls(4, 5))
			self.assertEqual(e[::2], cls(0, 2, 4))
			self.assertEqual(e[1::2], cls(1, 3, 5))
			self.assertEqual(e[::-1], cls(range(5, -1, -1)))
			e[1] = 10
			self.assertEqual(e, cls(0, 10, 2, 3, 4, 5))
			e[1] = None
			self.assertEqual(e, cls(0, 2, 3, 4, 5))
			e[1] = ()
			self.assertEqual(e, cls(0, 3, 4, 5))

			# __set(item|slice)__
			e = cls(range(6))
			e[-1] = None
			self.assertEqual(e, cls(0, 1, 2, 3, 4))

			e = cls(range(6))
			e[1:5] = (100, 200)
			self.assertEqual(e, cls(0, 100, 200, 5))

			e = cls(range(6))
			e[:] = (100, 200)
			self.assertEqual(e, cls(100, 200))

			e = cls(range(6))
			e[::2] = (100, 120, 140)
			self.assertEqual(e, cls(100, 1, 120, 3, 140, 5))

			e = cls(range(6))
			e[1::2] = (110, 130, 150)
			self.assertEqual(e, cls(0, 110, 2, 130, 4, 150))

			e = cls(range(6))
			e[::-1] = range(6)
			self.assertEqual(e, cls(range(5, -1, -1)))

			# __del(item|slice)__
			e = cls(range(6))
			del e[0]
			self.assertEqual(e, cls(1, 2, 3, 4, 5))
			del e[-1]
			self.assertEqual(e, cls(1, 2, 3, 4))

			e = cls(range(6))
			del e[1:5]
			self.assertEqual(e, cls(0, 5))

			e = cls(range(6))
			del e[2:]
			self.assertEqual(e, cls(0, 1))

			e = cls(range(6))
			del e[-2:]
			self.assertEqual(e, cls(0, 1, 2, 3))

			e = cls(range(6))
			del e[:2]
			self.assertEqual(e, cls(2, 3, 4, 5))

			e = cls(range(6))
			del e[:-2]
			self.assertEqual(e, cls(4, 5))

			e = cls(range(6))
			del e[:]
			self.assertEqual(e, cls())

			e = cls(range(6))
			del e[::2]
			self.assertEqual(e, cls(1, 3, 5))

			e = cls(range(6))
			del e[1::2]
			self.assertEqual(e, cls(0, 2, 4))

		e = html.div(range(6), id=42)
		self.assertEqual(e[2], xsc.Text(2))
		self.assertEqual(e[-1], xsc.Text(5))
		self.assertEqual(e[:], e)
		self.assertEqual(e[:2], cls(0, 1, id=42))
		self.assertEqual(e[-2:], cls(4, 5, id=42))
		self.assertEqual(e[::2], cls(0, 2, 4, id=42))
		self.assertEqual(e[1::2], cls(1, 3, 5, id=42))
		self.assertEqual(e[::-1], cls(range(5, -1, -1), id=42))

	def test_clone(self):
		for cls in (xsc.Frag, html.div):
			e = html.div(1)

			src = cls(1, e, e)

			dst = src.clone()
			self.assert_(src is not dst)
			self.assert_(src[0] is dst[0])
			self.assert_(src[1] is not dst[1])
			self.assert_(dst[1] is not dst[2])

			e.append(e) # create a cycle

			dst = src.copy()
			self.assert_(src is not dst)
			self.assert_(src[0] is dst[0])
			self.assert_(src[1] is dst[1])
			self.assert_(dst[1] is dst[2])

			dst = src.deepcopy()
			self.assert_(src is not dst)
			self.assert_(src[0] is dst[0])
			self.assert_(src[1] is not dst[1])
			self.assert_(dst[1] is dst[2])

		e = html.div(id=(17, html.div(23), 42))
		for src in (e, e.attrs):
			dst = src.clone()
			self.assert_(src["id"] is not dst["id"])
			self.assert_(src["id"][0] is dst["id"][0])
			self.assert_(src["id"][1] is not dst["id"][1])

		e["id"][1] = e # create a cycle
		e["id"][2] = e # create a cycle
		for src in (e, e.attrs):
			dst = src.copy()
			self.assert_(src["id"] is dst["id"])
			self.assert_(src["id"][0] is dst["id"][0])
			self.assert_(src["id"][1] is dst["id"][1])
			self.assert_(dst["id"][1] is dst["id"][2])
			dst = src.deepcopy()
			self.assert_(src["id"] is not dst["id"])
			self.assert_(src["id"][0] is dst["id"][0])
			self.assert_(src["id"][1] is not dst["id"][1])
			self.assert_(dst["id"][1] is dst["id"][2])

	def check_sortreverse(self, method):
		for class_ in (xsc.Frag, html.div):
			node = class_(3, 2, 1)
			node2 = getattr(node, method)()
			self.assertEqual(node, class_(3, 2, 1))
			self.assertEqual(node2, class_(1, 2, 3))

	def test_sorted(self):
		self.check_sortreverse("sorted")

	def test_reversed(self):
		self.check_sortreverse("reversed")


class NamespaceTest(unittest.TestCase):
	def test_mixedattrnames(self):
		class __ns__(xsc.Namespace):
			xmlname = "test"
			xmlurl = "test"

			class Attrs(xsc.Namespace.Attrs):
				class a(xsc.TextAttr): xmlname = "A"
				class A(xsc.TextAttr): xmlname = "a"
			class Test(xsc.Element):
				class Attrs(xsc.Element.Attrs):
					class a(xsc.TextAttr): xmlname = "A"
					class A(xsc.TextAttr): xmlname = "a"

		node = __ns__.Test(
			{
				(__ns__, "a"): "a2",
				(__ns__, "A"): "A2",
			},
			a="a",
			A="A"
		)
		for (name, value) in (
				("a", "a"),
				("A", "A"),
				((__ns__, "a"), "a2"),
				((__ns__, "A"), "A2")
			):
			self.assertEqual(unicode(node[name]), value)
			self.assertEqual(unicode(node.attrs[name]), value)
			self.assertEqual(unicode(node.attrs.get(name, xml=False)), value)
			if isinstance(name, tuple):
				name = (name[0], name[1].swapcase())
			else:
				name = name.swapcase()
			self.assertEqual(unicode(node.attrs.get(name, xml=True)), value)

	def check_namespace(self, module):
		for obj in module.__dict__.values():
			if isinstance(obj, type) and issubclass(obj, xsc.Node):
				node = obj()
				if isinstance(node, xsc.Element):
					for (attrname, attrvalue) in node.attrs.alloweditems():
						if attrvalue.required:
							if attrvalue.values:
								node[attrname] = attrvalue.values[0]
							else:
								node[attrname] = "foo"
				node.conv().asBytes()

	def test_html(self):
		self.check_namespace(html)

	def test_ihtml(self):
		self.check_namespace(ihtml)

	def test_wml(self):
		self.check_namespace(wml)

	def test_css(self):
		self.check_namespace(css)

	def test_specials(self):
		self.check_namespace(css)

	def test_form(self):
		self.check_namespace(css)

	def test_meta(self):
		self.check_namespace(css)

	def test_htmlspecials(self):
		self.check_namespace(css)

	def test_cssspecials(self):
		self.check_namespace(css)

	def test_docbook(self):
		self.check_namespace(css)

	def createns(self):
		class __ns__(xsc.Namespace):
			xmlname = "gurk"
			xmlurl = "http://www.gurk.com/"
			class foo(xsc.Element):
				pass
			class bar(xsc.Element):
				pass
		return __ns__

	def test_nsupdate(self):
		class ns1:
			class foo(xsc.Element):
				pass
			class bar(xsc.Element):
				pass
			class foo2(xsc.Element):
				pass
			class bar2(xsc.Element):
				pass
		class ns2:
			class foo(xsc.Element):
				pass
			class bar(xsc.Element):
				pass
			class foo2(xsc.Element):
				pass
			class bar2(xsc.Element):
				pass
		a = [ {"foo": ns.foo, "bar": ns.bar, "foo2": ns.foo2, "bar2": ns.bar2} for ns in (ns1, ns2) ]

		ns = self.createns()
		ns.update(*a)
		self.assertEquals(ns.element("foo"), ns2.foo)
		self.assertEquals(ns.element("bar"), ns2.bar)
		self.assertEquals(ns.element("foo2"), ns2.foo2)
		self.assertEquals(ns.element("bar2"), ns2.bar2)

		ns = self.createns()
		ns.updatenew(*a)
		self.assertEquals(ns.element("foo"), ns.foo)
		self.assertEquals(ns.element("bar"), ns.bar)
		self.assertEquals(ns.element("foo2"), ns2.foo2)
		self.assertEquals(ns.element("bar2"), ns2.bar2)

		ns = self.createns()
		ns.updateexisting(*a)
		self.assertEquals(ns.element("foo"), ns2.foo)
		self.assertEquals(ns.element("bar"), ns2.bar)
		self.assertRaises(xsc.IllegalElementError, ns.element, "foo2")
		self.assertRaises(xsc.IllegalElementError, ns.element, "bar2")

	def test_attributeexamples(self):
		self.assertEqual(xsc.amp.__name__, "amp")
		self.assertEqual(xsc.amp.xmlname, u"amp")
		self.assert_(xsc.amp.__ns__ is None)
		self.assertEqual(xsc.amp.xmlprefix(), None)

		self.assertEqual(chars.uuml.__name__, "uuml")
		self.assertEqual(chars.uuml.xmlname, u"uuml")
		self.assert_(chars.uuml.__ns__ is chars)
		self.assertEqual(chars.uuml.xmlprefix(), "chars")

		self.assertEqual(html.a.Attrs.class_.__name__, "class_")
		self.assertEqual(html.a.Attrs.class_.xmlname, u"class")
		self.assert_(html.a.Attrs.class_.__ns__ is None)

		self.assertEqual(xml.Attrs.lang.__name__, "lang")
		self.assertEqual(xml.Attrs.lang.xmlname, u"lang")
		self.assert_(xml.Attrs.lang.__ns__ is xml)
		self.assertEqual(xml.Attrs.lang.xmlprefix(), "xml")

	def test_autoinherit(self):
		class NS1(xsc.Namespace):
			xmlname = "test"
			xmlurl = "test"
			class foo(xsc.Element):
				model = False
				def convert(self, converter):
					e = self.__ns__.bar()
					return e.convert(converter)
			class bar(xsc.Entity):
				def convert(self, converter):
					return xsc.Text(17)

		class NS2(NS1):
			xmlname = "test"
			class bar(xsc.Entity):
				def convert(self, converter):
					return xsc.Text(23)

		self.assertEquals(unicode(NS1.foo().conv()), u"17")
		self.assertEquals(unicode(NS2.foo().conv()), u"23")

	def check_nskeysvaluesitems(self, ns, method, resname, resclass):
		self.assertEquals(getattr(ns, method + "keys")(xml=False), [resname])
		self.assertEquals(getattr(ns, method + "keys")(xml=True), [resname[:-1]])

		self.assertEquals(getattr(ns, method + "values")(), [resclass])

		self.assertEquals(getattr(ns, method + "items")(xml=False), [(resname, resclass)])
		self.assertEquals(getattr(ns, method + "items")(xml=True), [(resname[:-1], resclass)])

	def test_nskeysvaluesitems(self):
		class NS(xsc.Namespace):
			xmlname = "test"
			class el_(xsc.Element):
				xmlname = "el"
			class en_(xsc.Entity):
				xmlname = "en"
			class pi_(xsc.ProcInst):
				xmlname = "pi"
			class cr_(xsc.CharRef):
				xmlname = "cr"
				codepoint = 0x4242

		self.check_nskeysvaluesitems(NS, "element", "el_", NS.el_)

		keys = NS.entitykeys(xml=False)
		self.assertEqual(len(keys), 2)
		self.assert_("en_" in keys)
		self.assert_("cr_" in keys)
		keys = NS.entitykeys(xml=True)
		self.assertEqual(len(keys), 2)
		self.assert_("en" in keys)
		self.assert_("cr" in keys)

		values = NS.entityvalues()
		self.assertEqual(len(values), 2)
		self.assert_(NS.en_ in values)
		self.assert_(NS.cr_ in values)

		items = NS.entityitems(xml=False)
		self.assertEqual(len(items), 2)
		self.assert_(("en_", NS.en_) in items)
		self.assert_(("cr_", NS.cr_) in items)
		items = NS.entityitems(xml=True)
		self.assertEqual(len(items), 2)
		self.assert_(("en", NS.en_) in items)
		self.assert_(("cr", NS.cr_) in items)

		self.check_nskeysvaluesitems(NS, "procinst", "pi_", NS.pi_)

		self.check_nskeysvaluesitems(NS, "charref", "cr_", NS.cr_)

	def test_prefixsubclasses(self):
		class NS1(xsc.Namespace):
			xmlname = "ns"
			xmlurl = "http://xmlns.ns.info/"

			class gurk(xsc.Element):
				model = False

		class NS2(NS1):
			xmlname = "ns"

		p = xsc.Prefixes(ns=NS1)

		self.assertEqual(
			NS1.gurk().asBytes(xhtml=2, prefixmode=2, prefixes=p),
			'<ns:gurk xmlns:ns="http://xmlns.ns.info/"/>'
		)
		# The sub namespace should pick up the prefix defined for the first one
		self.assertEqual(
			NS2.gurk().asBytes(xhtml=2, prefixmode=2, prefixes=p),
			'<ns:gurk xmlns:ns="http://xmlns.ns.info/"/>'
		)


class PublishTest(unittest.TestCase):
	def test_publishelement(self):
		node = html.html()

		prefixes = xsc.Prefixes(h=html)
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=0), """<html></html>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=1), """<h:html></h:html>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=2), """<h:html xmlns:h="http://www.w3.org/1999/xhtml"></h:html>""")

		prefixes = xsc.Prefixes(html)
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=0), """<html></html>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=1), """<html></html>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=2), """<html xmlns="http://www.w3.org/1999/xhtml"></html>""")

	def test_publishentity(self):
		node = abbr.xml()

		prefixes = xsc.Prefixes(a=abbr, s=specials)
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=0), """&xml;""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=1), """&xml;""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=2), """&xml;""")

		prefixes = xsc.Prefixes(abbr, s=specials)
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=0), """&xml;""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=1), """&xml;""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=2), """&xml;""")

	def test_publishprocinst(self):
		node = php.php("x")

		prefixes = xsc.Prefixes(p=php, s=specials)
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=0), """<?php x?>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=1), """<?php x?>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=2), """<?php x?>""")

		prefixes = xsc.Prefixes(php, s=specials)
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=0), """<?php x?>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=1), """<?php x?>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=2), """<?php x?>""")

	def test_publishboolattr(self):
		node = html.td("?", nowrap=None)
		self.assertEquals(node.asBytes(xhtml=0), """<td>?</td>""")
		node = html.td("?", nowrap=True)
		self.assertEquals(node.asBytes(xhtml=0), """<td nowrap>?</td>""")
		self.assertEquals(node.asBytes(xhtml=1), """<td nowrap="nowrap">?</td>""")
		self.assertEquals(node.asBytes(xhtml=2), """<td nowrap="nowrap">?</td>""")

	def test_publishurlattr(self):
		node = html.link(href=None)
		self.assertEquals(node.asBytes(xhtml=1), """<link />""")
		node = html.link(href="root:gurk.html")
		self.assertEquals(node.asBytes(xhtml=1), """<link href="root:gurk.html" />""")
		self.assertEquals(node.asBytes(xhtml=1, base="root:gurk.html"), """<link href="" />""")
		self.assertEquals(node.asBytes(xhtml=1, base="root:hurz.html"), """<link href="gurk.html" />""")

	def test_publishstyleattr(self):
		node = html.div(style=None)
		self.assertEquals(node.asBytes(xhtml=1), """<div></div>""")
		node = html.div(style="background-image: url(root:gurk.html)")
		self.assertEquals(node.asBytes(xhtml=1), """<div style="background-image: url(root:gurk.html)"></div>""")
		self.assertEquals(node.asBytes(xhtml=1, base="root:gurk.html"), """<div style="background-image: url()"></div>""")
		self.assertEquals(node.asBytes(xhtml=1, base="root:hurz.html"), """<div style="background-image: url(gurk.html)"></div>""")

	def test_publishxmlattr(self):
		from ll.xist.ns import xml
		node = html.html({(xml, "space"): "preserve"})
		prefixes = xsc.Prefixes(h=html)
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=0), """<html xml:space="preserve"></html>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=1), """<h:html xml:space="preserve"></h:html>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=2), """<h:html xmlns:h="http://www.w3.org/1999/xhtml" xml:space="preserve"></h:html>""")

	def test_publishglobalattr(self):
		from ll.xist.ns import xlink
		node = html.html({(xlink, "title"): "the foo bar"})
		prefixes = xsc.Prefixes(h=html, xl=xlink)
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=0), """<html xmlns:xl="http://www.w3.org/1999/xlink" xl:title="the foo bar"></html>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=1), """<h:html xmlns:xl="http://www.w3.org/1999/xlink" xl:title="the foo bar"></h:html>""")
		# FIXME: this depends on dict iteration order
		self.assertEquals(node.asBytes(prefixes=prefixes, prefixmode=2), """<h:html xmlns:xl="http://www.w3.org/1999/xlink" xmlns:h="http://www.w3.org/1999/xhtml" xl:title="the foo bar"></h:html>""")

	def test_publishempty(self):
		node = xsc.Frag(html.br(), html.div())
		self.assertEquals(node.asBytes(xhtml=0), """<br><div></div>""")
		self.assertEquals(node.asBytes(xhtml=1), """<br /><div></div>""")
		self.assertEquals(node.asBytes(xhtml=2), """<br/><div/>""")

	def test_publishescaped(self):
		s = u"""<&'"\xff>"""
		node = xsc.Text(s)
		self.assertEquals(node.asBytes(encoding="ascii"), """&lt;&amp;'"&#255;&gt;""")
		node = html.span(class_=s)
		self.assertEquals(node.asBytes(encoding="ascii", xhtml=2), """<span class="&lt;&amp;'&quot;&#255;&gt;"/>""")

	escapeInput = u"".join([unichr(i) for i in xrange(1000)] + [unichr(i) for i in xrange(sys.maxunicode-10, sys.maxunicode+1)])

	def test_helpersescapetext(self):
		escapeOutput = []
		for c in self.escapeInput:
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
		self.assertEqual(helpers.escapetext(self.escapeInput), escapeOutput)

	def test_helpersescapeattr(self):
		escapeOutput = []
		for c in self.escapeInput:
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
		self.assertEqual(helpers.escapeattr(self.escapeInput), escapeOutput)

	def test_helpercssescapereplace(self):
		escapeOutput = []
		for c in self.escapeInput:
			try:
				c.encode("ascii")
				escapeOutput.append(c)
			except UnicodeError:
				escapeOutput.append((u"\\%x" % ord(c)).upper())
		escapeOutput = u"".join(escapeOutput)
		self.assertEqual(helpers.cssescapereplace(self.escapeInput, "ascii"), escapeOutput)

	def test_csspublish(self):
		e = css.css(
			css.atimport("http://www.gurk.org/gurk.css"),
			css.atimport("http://www.gurk.org/print.css", media="print"),
			css.atimport("http://www.gurk.org/screen.css", media="screen"),
			css.rule(
				css.sel("body"),
				css.font_family("Verdana, sans-serif"),
				css.font_size("10pt"),
				css.background_color("#000"),
				css.color("#fff")
			),
			css.atmedia(
				css.rule(
					css.sel("div, p"),
					css.font_family("Verdana, sans-serif"),
					css.font_size("10pt"),
					css.background_color("#000"),
					css.color("#fff")
				),
				media="print"
			)
		)
		e.asBytes()


class ParseTest(unittest.TestCase):
	def assertSAXRaises(self, exception, func, *args, **kwargs):
		# assert that func(*args, **kwargs) raises exception either directly or wrapped in a SAXParseException
		try:
			func(*args, **kwargs)
		except exception:
			pass
		except saxlib.SAXParseException, exc:
			realexc = exc.getException()
			self.assert_(isinstance(realexc, exception))
		else:
			self.fail()

	def test_parselocationsgmlop(self):
		# Check that SGMLOP gets the location info right (at least the line numbers)
		node = parsers.parseString("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", saxparser=parsers.SGMLOPParser)
		self.assertEqual(len(node), 1)
		self.assertEqual(len(node[0]), 1)
		self.assertEqual(node[0][0].startloc.getSystemId(), "STRING")
		self.assertEqual(node[0][0].startloc.getLineNumber(), 1)

	def test_parselocationexpat(self):
		# Check that expat gets the location info right
		node = parsers.parseString("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", saxparser=parsers.ExpatParser)
		self.assertEqual(len(node), 1)
		self.assertEqual(len(node[0]), 1)
		self.assertEqual(node[0][0].startloc.getSystemId(), "STRING")
		self.assertEqual(node[0][0].startloc.getLineNumber(), 1)
		self.assertEqual(node[0][0].startloc.getColumnNumber(), 3)

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
		node = node.findfirst(xsc.FindType(xsc.Element)).compact() # get rid of the Frag and whitespace
		self.assertEquals(node, check)

	def test_parseurls(self):
		# Check proper URL handling when parsing URLAttr or StyleAttr attributes
		prefixes = xsc.Prefixes(html)
		node = parsers.parseString('<a href="4.html" style="background-image: url(3.gif);"/>', base="root:1/2.html", prefixes=prefixes)
		self.assertEqual(str(node[0]["style"]), "background-image: url(root:1/3.gif);")
		self.assertEqual(node[0]["style"].urls(), [url.URL("root:1/3.gif")])
		self.assertEqual(str(node[0]["href"]), "root:1/4.html")
		self.assertEqual(node[0]["href"].forInput(root="gurk/hurz.html"), url.URL("gurk/1/4.html"))

	def test_parserequiredattrs(self):
		# Parser should complain about required attributes that are missing
		class __ns__(xsc.Namespace):
			class Test(xsc.Element):
				class Attrs(xsc.Element.Attrs):
					class required(xsc.TextAttr): required = True

		prefixes = xsc.Prefixes(__ns__)
		node = parsers.parseString('<Test required="foo"/>', prefixes=prefixes)
		self.assertEqual(str(node[0]["required"]), "foo")

		warnings.filterwarnings("error", category=xsc.RequiredAttrMissingWarning)
		self.assertSAXRaises(xsc.RequiredAttrMissingWarning, parsers.parseString, '<Test/>', prefixes=prefixes)

	def test_parsevalueattrs(self):
		# Parser should complain about attributes with illegal values, when a set of values is specified
		class __ns__(xsc.Namespace):
			class Test(xsc.Element):
				class Attrs(xsc.Element.Attrs):
					class withvalues(xsc.TextAttr): values = ("foo", "bar")

		prefixes = xsc.Prefixes(__ns__)

		warnings.filterwarnings("error", category=xsc.IllegalAttrValueWarning)
		node = parsers.parseString('<Test withvalues="bar"/>', prefixes=prefixes)
		self.assertEqual(str(node[0]["withvalues"]), "bar")
		self.assertSAXRaises(xsc.IllegalAttrValueWarning, parsers.parseString, '<Test withvalues="baz"/>', prefixes=prefixes)

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

	def check_parseentities(self, source, result, **parseargs):
		node = parsers.parseString("""<a title="%s">%s</a>""" % (source, source), **parseargs)
		node = node.findfirst(xsc.FindType(xsc.Element))
		self.assertEqual(unicode(node), result)
		self.assertEqual(unicode(node["title"]), result)

	def check_parsestrictentities(self, source, result, parserfactory):
		# in the strict parser the errors will always be raised, so change them into errors to verify that
		warnings.filterwarnings("error", category=xsc.MalformedCharRefWarning)

		prefixes = xsc.Prefixes([self.__class__.__ns__, chars])
		self.check_parseentities(source, result, prefixes=prefixes, saxparser=parserfactory)
		for bad in ("&", "&#x", "&&", "&#x;", "&#fg;", "&#999999999;", "&#;", "&#y;", "&#x;", "&#xy;"):
			self.assertSAXRaises((xsc.MalformedCharRefWarning, expat.ExpatError), self.check_parseentities, bad, u"", prefixes=prefixes, saxparser=parserfactory)
		self.assertSAXRaises(xsc.IllegalEntityError, self.check_parseentities, "&baz;", u"", prefixes=prefixes, saxparser=parserfactory)

	def test_parsestrictentities_sgmlop(self):
		self.check_parsestrictentities(
			"a&amp;b&foo;&bar;c&#32;d&#x20;&#30000;;&lt;&gt;&quot;&apos;",
			u"""a&bFOO\x42c d %c;<>"'""" % 30000,
			parsers.SGMLOPParser
		)

	def test_parsestrictentities_expat(self):
		self.check_parsestrictentities(
			"a&amp;bc&#32;d&#x20;&#30000;;&lt;&gt;&quot;&apos;",
			u"""a&bc d %c;<>"'""" % 30000,
			parsers.ExpatParser
		)

	def check_parsebadentities(self, parserfactory):
		warnings.filterwarnings("ignore", category=xsc.MalformedCharRefWarning)

		prefixes = xsc.Prefixes([self.__class__.__ns__, chars])
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
			self.check_parseentities(source, result, prefixes=prefixes, saxparser=parserfactory)

	def test_parsebadentities_badentity(self):
		self.check_parsebadentities(parsers.BadEntityParser)

	def test_parsebadentities_html(self):
		self.check_parsebadentities(parsers.HTMLParser)

	def test_multipleparsecalls(self):
		# A Parser instance should be able to parse multiple XML sources, even when some of the parse calls fail
		for saxparser in (parsers.SGMLOPParser, parsers.BadEntityParser, parsers.HTMLParser, parsers.ExpatParser):
			p = parsers.Parser(saxparser=saxparser)
			for i in xrange(3):
				try:
					p.parseString("<>gurk")
				except Exception:
					pass
				for j in xrange(3):
					self.assertEqual(p.parseString("<a>gurk</a>").asBytes(), "<a>gurk</a>")

	def test_sysid(self):
		# Default system ids and explicitely specified system ids should end up in the location info of the resulting XML tree
		node = parsers.parseString("gurk")
		self.assertEqual(node[0].startloc.sysid, "STRING")

		node = parsers.parseString("gurk", base="root:gurk.xmlxsc")
		self.assertEqual(node[0].startloc.sysid, "root:gurk.xmlxsc")

		node = parsers.parseString("gurk", base="root:gurk.xmlxsc", sysid="hurz")
		self.assertEqual(node[0].startloc.sysid, "hurz")


class CSSParseTest(unittest.TestCase):
	def test_parse(self):
		csshandler = cssparsers.ParseHandler()
		s = "div {border: 0px;}"
		self.assertEqual(csshandler.parseString(s), s)
		s = "div {background-image: url(gurk.gif);}"
		self.assertEqual(csshandler.parseString(s), s)
		s = "div {background-image: url(gurk.gif);}"
		self.assertEqual(
			csshandler.parseString(s, base="root:hurz/index.css"),
			"div {background-image: url(root:hurz/gurk.gif);}"
		)

	def test_publish(self):
		csshandler = cssparsers.PublishHandler()
		s = "div {border: 0px;}"
		self.assertEqual(csshandler.parseString(s), s)
		s = "div {background-image: url(gurk.gif);}"
		self.assertEqual(csshandler.parseString(s), s)
		s = "div {background-image: url(root:hurz/gurk.gif);}"
		self.assertEqual(
			csshandler.parseString(s, base="root:hurz/index.css"),
			"div {background-image: url(gurk.gif);}"
		)

	def test_collect(self):
		csshandler = cssparsers.CollectHandler()
		s = """
			div.c1 {background-image: url(root:hurz/hinz.gif);}
			div.c1 {background-image: url(root:hurz/kunz.gif);}
		"""
		csshandler.parseString(s)
		self.assertEqual(len(csshandler.urls), 2)
		self.assertEqual(csshandler.urls[0], url.URL("root:hurz/hinz.gif"))
		self.assertEqual(csshandler.urls[1], url.URL("root:hurz/kunz.gif"))


class DTD2XSCTest(unittest.TestCase):
	def dtd2ns(self, s, xmlname, xmlurl=None, shareattrs=None):
		from xml.parsers.xmlproc import dtdparser

		dtd = dtdparser.load_dtd_string(s)
		data = xnd.fromdtd(dtd, xmlname=xmlname, xmlurl=xmlurl)

		if shareattrs is not None:
			data.shareattrs(shareattrs)

		mod = {"__name__": xmlname}
		encoding = "iso-8859-1"
		code = data.aspy(encoding=encoding, asmod=False).encode(encoding)
		exec code in mod

		return mod["__ns__"]

	def test_convert(self):
		dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
		<!ELEMENT foo (bar+)>
		<!ATTLIST foo
			id    ID    #IMPLIED
			xmlns CDATA #FIXED "http://xmlns.foo.com/foo"
		>
		<!ELEMENT bar EMPTY>
		<!ATTLIST bar
			bar1 CDATA               #REQUIRED
			bar2 (bar2)              #IMPLIED
			bar3 (bar3a|bar3b|bar3c) #IMPLIED
			bar-4 (bar-4a|bar-4b)    #IMPLIED
			bar_4 (bar_4a|bar_4b)    #IMPLIED
			bar_42 (bar_42a|bar_42b) #IMPLIED
			class CDATA              #IMPLIED
			foo:bar CDATA            #IMPLIED
		>
		"""
		ns = self.dtd2ns(dtdstring, "foo")

		self.assert_(issubclass(ns, xsc.Namespace))
		self.assertEqual(ns.xmlname, "foo")
		self.assertEqual(ns.xmlurl, "http://xmlns.foo.com/foo")
		self.assert_(isinstance(ns.foo.model, sims.Elements))
		self.assertEqual(len(ns.foo.model.elements), 1)
		self.assertEqual(ns.foo.model.elements[0], ns.bar)
		self.assert_(issubclass(ns.foo.Attrs.id, xsc.IDAttr))
		self.assert_("xmlns" not in ns.foo.Attrs)
		self.assert_(isinstance(ns.bar.model, sims.Empty))

		self.assert_("bar" not in ns.bar.Attrs)

		self.assert_(issubclass(ns.bar.Attrs.bar1, xsc.TextAttr))
		self.assertEqual(ns.bar.Attrs.bar1.required, True)

		self.assert_(issubclass(ns.bar.Attrs.bar2, xsc.BoolAttr))
		self.assertEqual(ns.bar.Attrs.bar2.required, False)

		self.assert_(issubclass(ns.bar.Attrs.bar3, xsc.TextAttr))
		self.assertEqual(ns.bar.Attrs.bar3.required, False)
		self.assertEqual(ns.bar.Attrs.bar3.values, ("bar3a", "bar3b", "bar3c"))

		# Attributes are alphabetically sorted
		self.assert_(issubclass(ns.bar.Attrs.bar_4, xsc.TextAttr))
		self.assertEqual(ns.bar.Attrs.bar_4.xmlname, "bar-4")
		self.assertEqual(ns.bar.Attrs.bar_4.values, ("bar-4a", "bar-4b"))

		self.assert_(issubclass(ns.bar.Attrs.bar_42, xsc.TextAttr))
		self.assertEqual(ns.bar.Attrs.bar_42.xmlname, "bar_4")
		self.assertEqual(ns.bar.Attrs.bar_42.values, ("bar_4a", "bar_4b"))

		self.assert_(issubclass(ns.bar.Attrs.bar_422, xsc.TextAttr))
		self.assertEqual(ns.bar.Attrs.bar_422.xmlname, "bar_42")
		self.assertEqual(ns.bar.Attrs.bar_422.values, ("bar_42a", "bar_42b"))

	def test_charref(self):
		dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
		<!ELEMENT foo (EMPTY)>
		<!ENTITY bar "&#xff;">
		"""
		ns = self.dtd2ns(dtdstring, "foo")

		self.assertEqual(ns.bar.codepoint, 0xff)

	def test_keyword(self):
		dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
		<!ELEMENT foo EMPTY>
		<!ATTLIST foo
			class CDATA              #IMPLIED
		>
		"""
		ns = self.dtd2ns(dtdstring, "foo")
		self.assert_(issubclass(ns.foo.Attrs.class_, xsc.TextAttr))
		self.assertEqual(ns.foo.Attrs.class_.__name__, "class_")
		self.assertEqual(ns.foo.Attrs.class_.xmlname, u"class")

	def test_quotes(self):
		dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
		<!ELEMENT foo EMPTY>
		"""
		ns = self.dtd2ns(dtdstring, "foo", xmlurl='"')
		self.assertEqual(ns.xmlurl, '"')

	def test_unicode(self):
		dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
		<!ELEMENT foo EMPTY>
		"""
		ns = self.dtd2ns(dtdstring, "foo", xmlurl=u'\u3042')
		self.assertEqual(ns.xmlurl, u'\u3042')

	def test_unicodequotes(self):
		dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
		<!ELEMENT foo EMPTY>
		"""
		ns = self.dtd2ns(dtdstring, "foo", xmlurl=u'"\u3042"')
		self.assertEqual(ns.xmlurl, u'"\u3042"')

	def test_badelementname(self):
		dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
		<!ELEMENT class EMPTY>
		"""
		ns = self.dtd2ns(dtdstring, "foo")
		self.assert_(issubclass(ns.class_, xsc.Element))

	def test_shareattrsnone(self):
		dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
		<!ELEMENT foo (bar)>
		<!ATTLIST foo
			baz CDATA              #IMPLIED
		>
		<!ELEMENT bar EMPTY>
		<!ATTLIST bar
			baz CDATA              #IMPLIED
		>
		"""
		ns = self.dtd2ns(dtdstring, "foo", shareattrs=None)
		self.assert_(not hasattr(ns, "baz"))

	def test_shareattrsdupes(self):
		dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
		<!ELEMENT foo (bar)>
		<!ATTLIST foo
			baz  CDATA             #IMPLIED
			baz2 CDATA             #IMPLIED
		>
		<!ELEMENT bar EMPTY>
		<!ATTLIST bar
			baz  CDATA             #IMPLIED
			baz2 CDATA             #REQUIRED
		>
		"""
		ns = self.dtd2ns(dtdstring, "foo", shareattrs=False)
		self.assert_(issubclass(ns.foo.Attrs.baz, ns.baz.baz))
		self.assert_(issubclass(ns.bar.Attrs.baz, ns.baz.baz))
		self.assert_(not hasattr(ns, "baz2"))
		self.assert_(not ns.foo.Attrs.baz2.required)
		self.assert_(ns.bar.Attrs.baz2.required)

	def test_shareattrsall(self):
		dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
		<!ELEMENT foo (bar)>
		<!ATTLIST foo
			baz  CDATA             #IMPLIED
			bazz CDATA             #IMPLIED
		>
		<!ELEMENT bar EMPTY>
		<!ATTLIST bar
			baz  CDATA             #IMPLIED
			bazz CDATA             #REQUIRED
		>
		"""
		ns = self.dtd2ns(dtdstring, "foo", shareattrs=True)
		self.assert_(issubclass(ns.foo.Attrs.baz, ns.baz.baz))
		self.assert_(issubclass(ns.bar.Attrs.baz, ns.baz.baz))

		self.assertNotEqual(ns.foo.Attrs.bazz.__bases__[0], xsc.TextAttr)
		self.assertNotEqual(ns.bar.Attrs.bazz.__bases__[0], xsc.TextAttr)
		self.assertNotEqual(ns.foo.Attrs.bazz.__bases__, ns.bar.Attrs.bazz.__bases__)

		self.assert_(not ns.foo.Attrs.bazz.required)
		self.assert_(ns.bar.Attrs.bazz.required)


class TLD2XSCTest(unittest.TestCase):
	def tld2ns(self, s, xmlname, shareattrs=None):
		node = parsers.parseString(s, prefixes=xsc.Prefixes(tld))
		node = node.findfirst(xsc.FindType(tld.taglib))

		data = node.asxnd()

		if shareattrs is not None:
			data.shareattrs(shareattrs)

		mod = {"__name__": xmlname}
		encoding = "iso-8859-1"
		code = data.aspy(encoding=encoding, asmod=False).encode(encoding)
		exec code in mod

		return mod["__ns__"]

	def test_convert(self):
		tldstring = """<?xml version="1.0" encoding="ISO-8859-1"?>
		<!DOCTYPE taglib PUBLIC "-//Sun Microsystems, Inc.//DTD JSP Tag Library 1.1//EN" "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd">
		<taglib>
			<tlibversion>1.0</tlibversion>
			<jspversion>1.1</jspversion>
			<shortname>foo</shortname>
			<tag>
				<name>bar</name>
				<tagclass>com.foo.bar</tagclass>
				<bodycontent>empty</bodycontent>
				<info>info</info>
				<attribute>
					<name>name</name>
					<required>true</required>
					<rtexprvalue>true</rtexprvalue>
				</attribute>
				<attribute>
					<name>response</name>
					<required>false</required>
					<rtexprvalue>true</rtexprvalue>
				</attribute>
				<attribute>
					<name>controllerElement</name>
					<required>false</required>
					<rtexprvalue>true</rtexprvalue>
				</attribute>
				<attribute>
					<name>type</name>
					<required>false</required>
					<rtexprvalue>true</rtexprvalue>
				</attribute>
			</tag>
		</taglib>
		"""
		ns = self.tld2ns(tldstring, "foo")
		self.assertEqual(ns.xmlname, u"foo")
		self.assertEqual(ns.bar.xmlname, u"bar")
		self.assert_(isinstance(ns.bar.model, sims.Empty))
		self.assertEqual(ns.bar.__doc__.strip(), "info")

		self.assert_(issubclass(ns.bar.Attrs.name, xsc.TextAttr))
		self.assertEqual(ns.bar.Attrs.name.required, True)

		self.assert_(issubclass(ns.bar.Attrs.response, xsc.TextAttr))
		self.assertEqual(ns.bar.Attrs.response.required, False)


class XNDTest(unittest.TestCase):
	def xnd2ns(self, data):

		mod = {"__name__": str(data.name)}
		encoding = "iso-8859-1"
		code = data.aspy(encoding=encoding, asmod=False).encode(encoding)
		exec code in mod

		return mod["__ns__"]

	def test_procinst(self):
		e = xnd.Namespace("ns")(
			xnd.ProcInst("foo", doc="gurk")
		)
		ns = self.xnd2ns(e)
		self.assert_(issubclass(ns.foo, xsc.ProcInst))
		self.assertEqual(ns.foo.__doc__.strip(), "gurk")

		e = xnd.Namespace("ns")(
			xnd.ProcInst("f-o-o")
		)
		ns = self.xnd2ns(e)
		self.assert_(issubclass(ns.f_o_o, xsc.ProcInst))
		self.assert_(ns.f_o_o.xmlname, ("f_o_o", "f-o-o"))

	def test_entity(self):
		e = xnd.Namespace("ns")(
			xnd.Entity("foo", doc="gurk")
		)
		ns = self.xnd2ns(e)
		self.assert_(issubclass(ns.foo, xsc.Entity))
		self.assertEqual(ns.foo.__doc__.strip(), "gurk")

		e = xnd.Namespace("ns")(
			xnd.Entity("f-o-o")
		)
		ns = self.xnd2ns(e)
		self.assert_(issubclass(ns.f_o_o, xsc.Entity))
		self.assert_(ns.f_o_o.xmlname, ("f_o_o", "f-o-o"))

	def test_charref(self):
		e = xnd.Namespace("ns")(
			xnd.CharRef("foo", doc="gurk", codepoint=0x3042)
		)
		ns = self.xnd2ns(e)
		self.assert_(issubclass(ns.foo, xsc.CharRef))
		self.assertEqual(ns.foo.__doc__.strip(), "gurk")
		self.assertEqual(ns.foo.codepoint, 0x3042)

		e = xnd.Namespace("ns")(
			xnd.CharRef("f-o-o", codepoint=0x3042)
		)
		ns = self.xnd2ns(e)
		self.assert_(issubclass(ns.f_o_o, xsc.CharRef))
		self.assert_(ns.f_o_o.xmlname, ("f_o_o", "f-o-o"))

	def test_model(self):
		e = xnd.Namespace("ns")(
			xnd.Element("foo", modeltype=True)
		)
		ns = self.xnd2ns(e)
		self.assert_(isinstance(ns.foo.model, sims.Any))

		e = xnd.Namespace("ns")(
			xnd.Element("foo", modeltype=False)
		)
		ns = self.xnd2ns(e)
		self.assert_(isinstance(ns.foo.model, sims.Empty))


class SIMSTest(unittest.TestCase):
	def setUp(self):
		self.oldfilters = warnings.filters[:]

	def tearDown(self):
		warnings.filters = self.oldfilters

	def test_empty(self):
		class ns1(xsc.Namespace):
			class el1(xsc.Element):
				model = sims.Empty()

		warnings.filterwarnings("error", category=sims.EmptyElementWithContentWarning)

		e = ns1.el1()
		e.asBytes()

		e = ns1.el1("gurk")
		self.assertRaises(sims.EmptyElementWithContentWarning, e.asBytes)

		e = ns1.el1(php.php("gurk"))
		self.assertRaises(sims.EmptyElementWithContentWarning, e.asBytes)

		e = ns1.el1(xsc.Comment("gurk"))
		self.assertRaises(sims.EmptyElementWithContentWarning, e.asBytes)

		e = ns1.el1(ns1.el1())
		self.assertRaises(sims.EmptyElementWithContentWarning, e.asBytes)

	def test_elements(self):
		class ns1(xsc.Namespace):
			class el1(xsc.Element):
				pass
			class el2(xsc.Element):
				pass

		class ns2(xsc.Namespace):
			class el1(xsc.Element):
				pass
			class el2(xsc.Element):
				pass

		warnings.filterwarnings("error", category=sims.WrongElementWarning)
		warnings.filterwarnings("error", category=sims.ElementWarning)
		warnings.filterwarnings("error", category=sims.IllegalTextWarning)

		ns1.el1.model = sims.Elements(ns1.el1, ns2.el1)

		e = ns1.el1()
		e.asBytes()

		e = ns1.el1("foo")
		self.assertRaises(sims.IllegalTextWarning, e.asBytes)

		e = ns1.el1(php.php("gurk"))
		e.asBytes()

		e = ns1.el1(xsc.Comment("gurk"))
		e.asBytes()

		e = ns1.el1(ns1.el1())
		e.asBytes()

		e = ns1.el1(ns2.el1())
		e.asBytes()

		e = ns1.el1(ns1.el2())
		self.assertRaises(sims.WrongElementWarning, e.asBytes)

		e = ns1.el1(ns2.el2())
		self.assertRaises(sims.WrongElementWarning, e.asBytes)

	def test_elementsortext(self):
		class ns1(xsc.Namespace):
			class el1(xsc.Element):
				pass
			class el2(xsc.Element):
				pass

		class ns2(xsc.Namespace):
			class el1(xsc.Element):
				pass
			class el2(xsc.Element):
				pass

		warnings.filterwarnings("error", category=sims.WrongElementWarning)
		warnings.filterwarnings("error", category=sims.ElementWarning)
		warnings.filterwarnings("error", category=sims.IllegalTextWarning)

		ns1.el1.model = sims.ElementsOrText(ns1.el1, ns2.el1)

		e = ns1.el1()
		e.asBytes()

		e = ns1.el1("foo")
		e.asBytes()

		e = ns1.el1(php.php("gurk"))
		e.asBytes()

		e = ns1.el1(xsc.Comment("gurk"))
		e.asBytes()

		e = ns1.el1(ns1.el1())
		e.asBytes()

		e = ns1.el1(ns2.el1())
		e.asBytes()

		e = ns1.el1(ns1.el2())
		self.assertRaises(sims.WrongElementWarning, e.asBytes)

		e = ns1.el1(ns2.el2())
		self.assertRaises(sims.WrongElementWarning, e.asBytes)

	def test_noelements(self):
		class ns1(xsc.Namespace):
			class el1(xsc.Element):
				model = sims.NoElements()

		class ns2(xsc.Namespace):
			class el1(xsc.Element):
				pass

		warnings.filterwarnings("error", category=sims.WrongElementWarning)
		warnings.filterwarnings("error", category=sims.ElementWarning)
		warnings.filterwarnings("error", category=sims.IllegalTextWarning)

		e = ns1.el1()
		e.asBytes()

		e = ns1.el1("foo")
		e.asBytes()

		e = ns1.el1(php.php("gurk"))
		e.asBytes()

		e = ns1.el1(xsc.Comment("gurk"))
		e.asBytes()

		e = ns1.el1(ns1.el1())
		self.assertRaises(sims.ElementWarning, e.asBytes)

		e = ns1.el1(ns2.el1())
		e.asBytes()

	def test_noelementsortext(self):
		class ns1(xsc.Namespace):
			class el1(xsc.Element):
				model = sims.NoElementsOrText()

		class ns2(xsc.Namespace):
			class el1(xsc.Element):
				pass

		warnings.filterwarnings("error", category=sims.WrongElementWarning)
		warnings.filterwarnings("error", category=sims.ElementWarning)
		warnings.filterwarnings("error", category=sims.IllegalTextWarning)

		e = ns1.el1()
		e.asBytes()

		e = ns1.el1("foo")
		self.assertRaises(sims.IllegalTextWarning, e.asBytes)

		e = ns1.el1(php.php("gurk"))
		e.asBytes()

		e = ns1.el1(xsc.Comment("gurk"))
		e.asBytes()

		e = ns1.el1(ns1.el1())
		self.assertRaises(sims.ElementWarning, e.asBytes)

		e = ns1.el1(ns2.el1())
		e.asBytes()


class PrettyTest(unittest.TestCase):
	def check(self, node, result):
		self.assertEqual(node.pretty().asBytes(), result)

	def test_pretty(self):
		self.check(html.p("apple", "tree"), "<p>appletree</p>")
		self.check(html.p("apple", html.br(), "tree"), "<p>apple<br />tree</p>")
		self.check(html.p(php.php("apple")), "<p>\n\t<?php apple?>\n</p>")
		self.check(html.p(php.php("apple"), "tree"), "<p><?php apple?>tree</p>")
		self.check(
			html.div(2*html.p("apple", "tree"), html.br()),
			"<div>\n\t<p>appletree</p>\n\t<p>appletree</p>\n\t<br />\n</div>"
		)
		self.check(
			html.div(
				php.php("apple"),
				html.p("apple", "tree"),
				html.div(
					html.p("apple"),
					html.p("tree"),
				),
				html.br()
			),
			"<div>\n\t<?php apple?>\n\t<p>appletree</p>\n\t<div>\n\t\t<p>apple</p>\n\t\t<p>tree</p>\n\t</div>\n\t<br />\n</div>"
		)


class XFindTestLevels(unittest.TestCase):
	def setUp(self):
		ds = [html.div(id=id) for id in xrange(8)]
		ds[1].append(ds[4:7])
		ds[2].append(ds[7])
		ds[0].append(ds[1:4])
		self.divs = ds
		#      ____0____
		#     /    |    \
		#   _1_    2     3
		#  / | \   |
		# 4  5  6  7

	def tearDown(self):
		del self.divs

	def checkids(self, expr, ids):
		self.assertEqual("".join(str(e["id"]) for e in expr), ids)

	def test_all(self):
		self.checkids(self.divs[0]//html.div, "1234567")

	def test_level1(self):
		self.checkids(self.divs[0]/html.div, "123")

	def test_level2(self):
		self.checkids(self.divs[0]/html.div/html.div, "4567")

	def test_level3(self):
		self.checkids(self.divs[0]/html.div/html.div/html.div, "")

	def test_contains(self):
		self.checkids(self.divs[0]//xfind.contains(html.div), "012")


class XFindTestOperators(unittest.TestCase):
	def setUp(self):
		self.node = xsc.Frag(
			html.div(
				html.h1("The ", html.em("important"), " headline"),
				html.p("The ", html.em("first"), " paragraph."),
				html.p("The ", html.em("second"), " ", html.em("important"), " paragraph."),
				align="left",
			),
			html.div(
				html.h1("The headline"),
				html.p("The ", html.em("first"), " paragraph."),
				html.div(
					html.h2("The ", html.em("important"), " headline"),
					html.p("The ", html.em("second"), " ", html.em("important"), " paragraph."),
					id="id42",
				),
				class_="foo",
			),
		)

	def tearDown(self):
		del self.node

	def test_hasattr(self):
		res = list(self.node//xfind.hasattr(html.div.Attrs.id, html.div.Attrs.align))
		self.assertEqual(len(res), 2)
		self.assert_(res[0] is self.node[0])
		self.assert_(res[1] is self.node[1][-1])

	def test_hasattrnamed(self):
		res = list(self.node//xfind.hasattrnamed("class_"))
		self.assertEqual(len(res), 1)
		self.assert_(res[0] is self.node[1])

		res = list(self.node//xfind.hasattrnamed("class", xml=True))
		self.assertEqual(len(res), 1)
		self.assert_(res[0] is self.node[1])

	def test_is(self):
		res = list(self.node//xfind.is_(html.h1, html.h2))
		self.assertEqual(len(res), 3)
		self.assert_(res[0] is self.node[0][0])
		self.assert_(res[1] is self.node[1][0])
		self.assert_(res[2] is self.node[1][-1][0])

		res = list(self.node//html.h1/xfind.is_(html.h1, html.h2))
		self.assertEqual(len(res), 2)
		self.assert_(res[0] is self.node[0][0])
		self.assert_(res[1] is self.node[1][0])

	def test_isnot(self):
		res = list(self.node//xfind.isnot(xsc.Text, html.p, html.div, html.em))
		self.assertEqual(len(res), 3)
		self.assert_(res[0] is self.node[0][0])
		self.assert_(res[1] is self.node[1][0])
		self.assert_(res[2] is self.node[1][-1][0])

	def test_contains(self):
		res = list(self.node//xfind.is_(html.h1, html.h2)/xfind.contains(html.em))
		self.assertEqual(len(res), 2)
		self.assert_(res[0] is self.node[0][0])
		self.assert_(res[1] is self.node[1][-1][0])

	def test_child(self):
		res = list(self.node//html.h1/xfind.child(html.em))
		self.assertEqual(len(res), 1)
		self.assert_(res[0] is self.node[0][0][1])

	def test_attr(self):
		res = list(self.node//xfind.attr(html.div.Attrs.id, html.div.Attrs.align))
		self.assertEqual(len(res), 2)
		self.assert_(res[0] is self.node[0]["align"])
		self.assert_(res[1] is self.node[1][-1]["id"])

	def test_attrnamed(self):
		res = list(self.node//xfind.attrnamed("class_"))
		self.assertEqual(len(res), 1)
		self.assert_(res[0] is self.node[1]["class_"])

		res = list(self.node//xfind.attrnamed("class", xml=True))
		self.assertEqual(len(res), 1)
		self.assert_(res[0] is self.node[1]["class_"])


class XFindTestMisc(unittest.TestCase):
	def checkids(self, expr, ids):
		self.assertEqual("".join(str(e["id"]) for e in expr), ids)

	def test_frag(self):
		e = parsers.parseString("das ist <b>klaus</b>. das ist <b>erich</b>", prefixes=xsc.Prefixes(html))
		# The following won't generate any nodes, because e/xfind.all iterates all
		# nodes in the tree (but not the Frag root) and ../html.b filters the bold
		# *children*, but there are none.
		self.assertEqual(u"".join(map(unicode, e//html.b)), u"")
		# The following *will* produce these nodes
		self.assertEqual(u"".join(map(unicode, e//xfind.is_(html.b))), u"klauserich")

	def test_multiall(self):
		#        ____0____
		#       /         \
		#     _1_         _2_
		#    /   \       /   \
		#   3     4     5     6
		#  / \   / \   / \   / \
		# 7   8 9   a b   c d   e
		ds = [html.div(id=hex(id).lower()[2:]) for id in xrange(15)]
		for i in xrange(7):
			ds[i].append(ds[2*i+1:2*i+3])
		# Using // multiple times might produce certain nodes twice
		self.checkids(ds[0]//html.div//html.div, "34789a56bcde789abcde")


class XFindTestItemSlice(unittest.TestCase):
	def checkids(self, expr, ids):
		self.assertEqual("".join(str(e["id"]) for e in expr), ids)

	def test_itemsslices(self):
		#        ____0____
		#       /    |    \
		#     _1_   _2_   _3_
		#    /   \ /   \ /   \
		#   4     5     6     7
		ds = [html.div(id=id) for id in xrange(8)]
		ds[0].append(ds[1], ds[2], ds[3])
		ds[1].append(ds[4], ds[5])
		ds[2].append(ds[5], ds[6])
		ds[3].append(ds[6], ds[7])

		self.checkids(ds[0]/html.div[0]/html.div[-1], "5")
		self.checkids(ds[0]/html.div/html.div[-1], "567")
		self.checkids(ds[0]/html.div[-1]/html.div, "67")
		self.checkids(ds[0]/(html.div/html.div), "455667") # we get 5 and 6 twice
		self.checkids(ds[0]/(html.div/html.div)[2], "5") # we get 5 and 6 twice
		self.checkids(ds[0]/html.div[:]/html.div[:], "455667")
		self.checkids(ds[0]/html.div/html.p[0], "")
		self.checkids(ds[0]/html.p[0]/html.p[0], "")

		# The following might be a surprise, but is perfectly normal:
		# each node is visited and the div children are yielded.
		# div(id=0) does have div children and those will be yielded.
		# This is why the sequence starts with "12" and not "14"
		self.checkids(ds[0]//html.div, "123455667")

		self.checkids(ds[0]/html.div[1:2], "2")
		self.checkids(ds[0]/html.div[1:-1]/html.div[1:-1], "")
		self.checkids(ds[0]/html.div[1:-1]/html.div[-1:], "6")


class PickleTest(unittest.TestCase):
	def test_pickle(self):
		e = xsc.Frag(
			xml.XML10(),
			html.DocTypeXHTML10transitional(),
			xsc.Comment("foo"),
			html.html(xml.Attrs(lang="de"), lang="de"),
			php.expression("$foo"),
			chars.nbsp(),
			abbr.xml(),
		)
		e.append(e[3])
		e2 = cPickle.loads(cPickle.dumps(e))
		self.assertEqual(e, e2)
		self.assert_(e2[3] is e2[-1])


class WalkTest(unittest.TestCase):
	def node2str(self, node):
		if isinstance(node, xsc.Node):
			if isinstance(node, xsc.Text):
				return "#"
			else:
				return node.xmlname
		else:
			return ".".join(map(self.node2str, node))

	def check_walk(self, node, filter, result, inmode=xsc.walknode, outmode=xsc.walknode):
		self.assertEqual(map(self.node2str, node.walk(filter, inmode=inmode, outmode=outmode)), result)

	def test_walk1(self):
		node = createfrag()
		def filter(*args):
			return (True, xsc.enterattrs, xsc.entercontent, True)

		modes = (xsc.walknode, xsc.walkpath, xsc.walkindex, xsc.walkrootindex)
		for inmode in modes:
			for outmode in modes:
				list(node.walk((True, xsc.entercontent, True), inmode=inmode, outmode=outmode))
				list(node.walk(filter, inmode=inmode, outmode=outmode))

	def test_walk2(self):
		node = html.div(html.tr(html.th("gurk"), html.td("hurz"), id=html.b(42)), class_=html.i("hinz"))

		def filtertopdown(node):
			return (isinstance(node, xsc.Element), xsc.entercontent)
		def filterbottomup(node):
			return (xsc.entercontent, isinstance(node, xsc.Element))
		def filtertopdownattrs(node):
			return (isinstance(node, xsc.Element), xsc.enterattrs, xsc.entercontent)
		def filterbottomupattrs(node):
			return (xsc.enterattrs, xsc.entercontent, isinstance(node, xsc.Element))
		def filtertopdowntextonlyinattr(path):
			for node in path:
				if isinstance(node, xsc.Attr):
					inattr = True
					break
			else:
				inattr = False
			node = path[-1]
			if isinstance(node, xsc.Element):
				return (True, xsc.enterattrs, xsc.entercontent)
			if inattr and isinstance(node, xsc.Text):
				return (True, )
			else:
				return (xsc.entercontent, )

		def filtertopdownattrwithoutcontent(node):
			if isinstance(node, xsc.Element):
				return (True, xsc.entercontent, xsc.enterattrs)
			elif isinstance(node, (xsc.Attr, xsc.Text)):
				return (True, )
			else:
				return (xsc.entercontent, )

		self.check_walk(node, filtertopdown, ["div", "tr", "th", "td"])
		self.check_walk(node, filterbottomup, ["th", "td", "tr", "div"])
		self.check_walk(node, filtertopdownattrs, ["div", "i", "tr", "b", "th", "td"])
		self.check_walk(node, filtertopdownattrs, ["div", "div.class.i", "div.tr", "div.tr.id.b", "div.tr.th", "div.tr.td"], outmode=xsc.walkpath)
		self.check_walk(node, filterbottomupattrs, ["div.class.i", "div.tr.id.b", "div.tr.th", "div.tr.td", "div.tr", "div"], outmode=xsc.walkpath)
		self.check_walk(node, filtertopdowntextonlyinattr, ["div", "div.class.i", "div.class.i.#", "div.tr", "div.tr.id.b", "div.tr.id.b.#", "div.tr.th", "div.tr.td"], inmode=xsc.walkpath, outmode=xsc.walkpath)
		self.check_walk(node, filtertopdownattrwithoutcontent, ["div", "div.tr", "div.tr.th", "div.tr.th.#", "div.tr.td", "div.tr.td.#", "div.tr.id", "div.class"], outmode=xsc.walkpath)

	def test_walkindex(self):
		e = html.div(
			"foo",
			html.a(
				"bar",
				xml.Attrs(lang="en"),
				href="baz",
			),
			"gurk",
		)
		res = list(e.walk(xsc.FindTypeAllAttrs(xsc.Text), outmode=xsc.walkindex))
		exp = [
			[0],
			[1, 0],
			[1, "href", 0],
			[1, (xml, "lang"), 0], # FIXME: This depends on dictionary iteration order
			[2]
		]
		self.assertEqual(res, exp)

	def test_walkindexisnode(self):
		# Check that all walk modes return the same data
		for node in allnodes():
			l1 = list(node.walk(xsc.FindTypeAllAttrs(xsc.Text), outmode=xsc.walknode))
			l2 = list(node.walk(xsc.FindTypeAllAttrs(xsc.Text), outmode=xsc.walkpath))
			l3 = list(node.walk(xsc.FindTypeAllAttrs(xsc.Text), outmode=xsc.walkindex))
			l4 = list(node.walk(xsc.FindTypeAllAttrs(xsc.Text), outmode=xsc.walkrootindex))
			self.assert_(len(l1) == len(l2) == len(l3) == len(l4))
			for (subnode, path, index, (root, rindex)) in zip(l1, l2, l3, l4):
				self.assert_(subnode is path[-1])
				self.assert_(subnode is node[index])
				self.assert_(subnode is root[rindex])


def test_main():
	unittest.main()


if __name__ == "__main__":
	test_main()
