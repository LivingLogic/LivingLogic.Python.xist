#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

import sys, unittest, cStringIO, warnings

from xml.sax import saxlib

from ll import url
from ll.xist import xsc, parsers, presenters, converters, helpers, errors, options
from ll.xist.ns import wml, ihtml, html, css, abbr, specials, htmlspecials, php, xml

# set to something ASCII, so presenters work, even if the system default encoding is ascii
options.reprtab = "  "

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

	def test_fragappend(self):
		node = xsc.Frag()
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

	def test_fragextend(self):
		node = xsc.Frag()
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

	def test_fraginsert(self):
		node = xsc.Frag()
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

	def test_fragiadd(self):
		node = xsc.Frag()
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

	def test_elementlen(self):
		self.check_lenunicode(html.div(), 0, u"")
		self.check_lenunicode(html.div(1), 1, u"1")
		self.check_lenunicode(html.div(1, 2, 3), 3, u"123")
		self.check_lenunicode(html.div(None), 0, u"")
		self.check_lenunicode(html.div(None, None, None), 0, u"")
		self.check_lenunicode(html.div(1, None, 2, None, 3, None, 4), 4, u"1234")
		self.check_lenunicode(html.div(1, (2, 3)), 3, u"123")
		self.check_lenunicode(html.div(1, (None, None)), 1, u"1")

	def createattr(self):
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

	def createattrs(self):
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

	def createelement(self):
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

	def createfrag(self):
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

	def allnodes(self):
		return (xsc.Null, self.createattr(), self.createattrs(), self.createelement(), self.createfrag())

	def test_standardmethods(self):
		for node in self.allnodes():
			node.compact()
			node.normalized()
			node.find()
			node.pretty()
			node.clone()
			node.conv()
			node.normalized().compact().pretty()

	def test_standardmethods2(self):
		for node in (self.createelement(), self.createfrag()):
			node.sorted()
			node.shuffled()
			node.reversed()

	def test_stringify(self):
		for node in self.allnodes():
			unicode(node)
			str(node)
			node.asString()
			node.asBytes()

	def test_asText(self):
		for node in self.allnodes():
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
		node = xsc.Text("test")
		hash(node)
		self.assertEqual(len(node), 4)
		self.assertEqual(node[1], xsc.Text("e"))
		self.assertEqual(3*node, xsc.Text(3*node.content))
		self.assertEqual(node*3, xsc.Text(node.content*3))
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
		self.assertEqual(node.lower(), xsc.Text("test"))
		self.assertEqual(xsc.Text("  test").lstrip(), xsc.Text("test"))
		self.assertEqual(node.replace("s", "x"), xsc.Text("text"))
		self.assertEqual(node.rjust(6), xsc.Text("  test"))
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

	def test_getsetitem(self):
		for cls in (xsc.Frag, html.div):
			for attr in ("class_", (xml, "lang")):
				node = cls(html.div(html.div({attr: "gurk"})))
				self.assertEqual(str(node[[0, 0, attr]]), "gurk")
				node[[0, 0, attr]] = "hurz"
				self.assertEqual(str(node[[0, 0, attr]]), "hurz")

	def test_mixedattrnames(self):
		class xmlns(xsc.Namespace):
			xmlname = "test"
			xmlurl = "test"

			class Attrs(xsc.Namespace.Attrs):
				class a(xsc.TextAttr, xsc.NamespaceAttrMixIn): xmlname = "A"
				class A(xsc.TextAttr, xsc.NamespaceAttrMixIn): xmlname = "a"
			class Test(xsc.Element):
				class Attrs(xsc.Element.Attrs):
					class a(xsc.TextAttr): xmlname = "A"
					class A(xsc.TextAttr): xmlname = "a"

		node = xmlns.Test(
			{
				(xmlns, "a"): "a2",
				(xmlns, "A"): "A2",
			},
			a="a",
			A="A"
		)
		for (name, value) in (
				("a", "a"),
				("A", "A"),
				((xmlns, "a"), "a2"),
				((xmlns, "A"), "A2")
			):
			self.assertEqual(unicode(node[name]), value)
			self.assertEqual(unicode(node.attrs[name]), value)
			self.assertEqual(unicode(node.attrs.get(name, xml=False)), value)
			if isinstance(name, tuple):
				name = (name[0], name[1].swapcase())
			else:
				name = name.swapcase()
			self.assertEqual(unicode(node.attrs.get(name, xml=True)), value)

	def mappedmapper(self, node, converter):
		if isinstance(node, xsc.Text):
			node = node.replace("gurk", "hurz")
		return node

	def test_conv(self):
		node = self.createfrag()
		node.conv()
		node.conv(converters.Converter())
		node.conv(function=self.mappedmapper)

	def test_repr(self):
		for node in self.allnodes():
			repr(node)
			for class_ in presenters.__dict__.itervalues():
				if isinstance(class_, type) and issubclass(class_, presenters.Presenter):
					node.repr(class_())
			for showLocation in (False, True):
				for showPath in (False, True):
					node.repr(presenters.TreePresenter(showLocation=showLocation, showPath=showPath))

	def test_walk(self):
		node = self.createfrag()
		def filter1(node):
			return xsc.Found(foundstart=True, foundend=True, enter=True)
		def filter2(path):
			return xsc.Found(foundstart=True, foundend=True, enter=True)

		list(node.walk(xsc.Found(foundstart=True, foundend=True, enter=True)))
		list(node.walk(xsc.Found(foundstart=True, foundend=True, enter=True), walkpath=True))
		list(node.walk(filter1))
		list(node.walk(filter1, walkpath=True))
		list(node.walk(filter2, filterpath=True))
		list(node.walk(filter2, filterpath=True, walkpath=True))

	def test_visit(self):
		node = self.createfrag()
		def dummy1(node, start):
			pass
		def dummy2(path, start):
			pass
		def filter1(node):
			return xsc.Found(foundstart=dummy1, foundend=dummy1, enter=True)
		def filter2(path):
			return xsc.Found(foundstart=dummy1, foundend=dummy1, enter=True)

		node.visit(xsc.Found(foundstart=dummy1, foundend=dummy1, enter=True))
		node.visit(xsc.Found(foundstart=dummy1, foundend=dummy1, entercontent=True, enterattrs=True))
		node.visit(xsc.Found(foundstart=dummy2, foundend=dummy2, enter=True), visitpath=True)
		node.visit(filter1)
		node.visit(filter1, visitpath=True)
		node.visit(filter2, filterpath=True)
		node.visit(filter2, filterpath=True, visitpath=True)

	def test_locationeq(self):
		l1 = xsc.Location(sysID="gurk", pubID="http://gurk.com", lineNumber=42, columnNumber=666)
		l2 = xsc.Location(sysID="gurk", pubID="http://gurk.com", lineNumber=42, columnNumber=666)
		l3 = xsc.Location(sysID="hurz", pubID="http://gurk.com", lineNumber=42, columnNumber=666)
		l4 = xsc.Location(sysID="gurk", pubID="http://hurz.com", lineNumber=42, columnNumber=666)
		l5 = xsc.Location(sysID="gurk", pubID="http://gurk.com", lineNumber=43, columnNumber=666)
		l6 = xsc.Location(sysID="gurk", pubID="http://gurk.com", lineNumber=43, columnNumber=667)
		l7 = xsc.Location(sysID="gurk", pubID="http://gurk.com")
		self.assertEqual(l1, l2)
		self.assertNotEqual(l1, l3)
		self.assertNotEqual(l1, l4)
		self.assertNotEqual(l1, l5)
		self.assertNotEqual(l1, l6)
		self.assertNotEqual(l1, l7)

	def test_locationoffset(self):
		l1 = xsc.Location(sysID="gurk", pubID="http://gurk.com", lineNumber=42, columnNumber=666)
		self.assertEqual(l1, l1.offset(0))
		l2 = l1.offset(1)
		self.assertEqual(l1.getSystemId(), l2.getSystemId())
		self.assertEqual(l1.getPublicId(), l2.getPublicId())
		self.assertEqual(l1.getLineNumber()+1, l2.getLineNumber())

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
			else:
				escapeOutput.append(c)
		escapeOutput = "".join(escapeOutput)
		self.assertEqual(helpers.escapeattr(self.escapeInput), escapeOutput)

	def test_helperxmlcharrefreplace(self):
		escapeOutput = []
		for c in self.escapeInput:
			try:
				c.encode("ascii")
				escapeOutput.append(c)
			except UnicodeError:
				escapeOutput.append(u"&#%d;" % ord(c))
		escapeOutput = u"".join(escapeOutput)
		self.assertEqual(helpers.xmlcharrefreplace(self.escapeInput, "ascii"), escapeOutput)

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

	def test_namespace(self):
		self.assertEqual(xsc.amp.xmlname, (u"amp", u"amp"))
		self.assert_(xsc.amp.xmlns is xsc.xmlns)
		self.assertEqual(xsc.amp.xmlprefix(), None)

		self.assertEqual(html.uuml.xmlname, (u"uuml", u"uuml"))
		self.assert_(html.uuml.xmlns is html)
		self.assertEqual(html.uuml.xmlprefix(), "html")

		self.assertEqual(html.a.Attrs.class_.xmlname, (u"class_", u"class"))
		self.assert_(html.a.Attrs.class_.xmlns is None)

		self.assertEqual(xml.Attrs.lang.xmlname, (u"lang", u"lang"))
		self.assert_(xml.Attrs.lang.xmlns is xml)
		self.assertEqual(xml.Attrs.lang.xmlprefix(), "xml")

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
		keys.remove("lang")

		keys1 = node.attrs.without(["lang"]).keys()
		keys1.sort()
		self.assertEqual(keys, keys1)

		keys.remove((xml2, "space"))
		keys2 = node.attrs.without(["lang", (xml, "space")]).keys()
		keys2.sort()
		self.assertEqual(keys, keys2)

		keys.remove((xml2, "lang"))
		keys.remove((xml2, "base"))
		keys3 = node.attrs.without(["lang"], [xml]).keys()
		keys3.sort()
		self.assertEqual(keys, keys3)

		# Check that non existing attrs are handled correctly
		keys4 = node.attrs.without(["lang", "src"], keepglobals=False).keys()
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

		self.assertEquals(node.attrs.with([u"lang"]).keys(), [u"lang"])

		keys1 = node.attrs.with([u"lang", u"align"]).keys()
		keys1.sort()
		self.assertEqual(keys1, [u"align", u"lang"])

		keys = [u"lang", (xml2, u"lang")]
		keys.sort()
		keys2 = node.attrs.with(keys).keys()
		keys2.sort()
		self.assertEqual(keys2, keys)

		keys = [u"lang", (xml2, u"lang"), (xml2, u"space")]
		keys.sort()
		keys3 = node.attrs.with([u"lang"], [xml]).keys()
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
		self.assertRaises(errors.IllegalAttrError, node.attrs.has, "illegal")
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
		self.assertEquals(unicode(node["testattr"]), "42")
		self.assertEquals(unicode(node.conv()["testattr"]), "42")

		node["testattr"] = None
		self.assert_(not node.attrs.has("testattr"))
		self.assert_(not node.conv().attrs.has("testattr"))

		node = testelem(testattr=None)
		self.assert_(not node.attrs.has("testattr"))
		self.assert_(not node.conv().attrs.has("testattr"))

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

	def test_autoinherit(self):
		class NS1(xsc.Namespace):
			xmlname = "test"
			xmlurl = "test"
			class foo(xsc.Element):
				empty = True
				def convert(self, converter):
					e = self.xmlns.bar()
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

	def test_allowedattr(self):
		self.assertEquals(html.a.Attrs.allowedattr("href"), html.a.Attrs.href)
		self.assertRaises(errors.IllegalAttrError, html.a.Attrs.allowedattr, "gurk")
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
		node.attrs.update({"href": "gurk2", "id": 42})
		self.assertEquals(unicode(node["href"]), u"gurk2")
		self.assertEquals(unicode(node["id"]), u"42")

		node = html.a(href="gurk", class_="hurz")
		node.attrs.updatenew({"href": "gurk2", "id": 42})
		self.assertEquals(unicode(node["href"]), u"gurk")
		self.assertEquals(unicode(node["id"]), u"42")

		node = html.a(href="gurk", class_="hurz")
		node.attrs.updateexisting({"href": "gurk2", "id": 42})
		self.assertEquals(unicode(node["href"]), u"gurk2")
		self.assertEquals(node.attrs.has("id"), False)

	def test_classrepr(self):
		repr(xsc.Base)
		repr(xsc.Node)
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

class PublishTest(unittest.TestCase):
	def test_publishelement(self):
		node = html.html()

		prefixes = xsc.Prefixes()
		prefixes.addPrefixMapping("h", html)

		self.assertEquals(node.asBytes(), "<html></html>")
		self.assertEquals(node.asBytes(prefixes=prefixes, elementmode=1), "<h:html></h:html>")
		self.assertEquals(node.asBytes(prefixes=prefixes, elementmode=2), """<h:html xmlns:h="http://www.w3.org/1999/xhtml"></h:html>""")

		prefixes = xsc.Prefixes()
		prefixes.addPrefixMapping(None, html)

		self.assertEquals(node.asBytes(prefixes=prefixes, elementmode=2), """<html xmlns="http://www.w3.org/1999/xhtml"></html>""")

	def test_publishentity(self):
		node = abbr.xml()

		prefixes = xsc.Prefixes()
		prefixes.addPrefixMapping("a", abbr)
		prefixes.addPrefixMapping("s", specials)

		self.assertEquals(node.asBytes(), "&xml;")
		self.assertEquals(node.asBytes(prefixes=prefixes, entitymode=1), "&a:xml;")
		self.assertEquals(node.asBytes(prefixes=prefixes, entitymode=2), """<wrap entityns:a="http://xmlns.livinglogic.de/xist/ns/abbr">&a:xml;</wrap>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, elementmode=2, entitymode=2), """<s:wrap entityns:a="http://xmlns.livinglogic.de/xist/ns/abbr" xmlns:s="http://xmlns.livinglogic.de/xist/ns/specials">&a:xml;</s:wrap>""")

		prefixes = xsc.Prefixes()
		prefixes.addPrefixMapping(None, abbr)
		prefixes.addPrefixMapping("s", specials)

		self.assertEquals(node.asBytes(prefixes=prefixes, entitymode=2), """<wrap entityns="http://xmlns.livinglogic.de/xist/ns/abbr">&xml;</wrap>""")
		self.assertEquals(node.asBytes(prefixes=prefixes, elementmode=2, entitymode=2), """<s:wrap entityns="http://xmlns.livinglogic.de/xist/ns/abbr" xmlns:s="http://xmlns.livinglogic.de/xist/ns/specials">&xml;</s:wrap>""")

	def test_publishprocinst(self):
		node = php.php("x")

		prefixes = xsc.Prefixes()
		prefixes.addPrefixMapping("p", php)
		prefixes.addPrefixMapping("s", specials)

		self.assertEquals(node.asBytes(), "<?php x?>")
		self.assertEquals(node.asBytes(prefixes=prefixes, procinstmode=1), "<?p:php x?>")
		self.assertEquals(node.asBytes(prefixes=prefixes, procinstmode=2), """<wrap procinstns:p="http://www.php.net/"><?p:php x?></wrap>""")
		# FIXME this depends on dict iteration order
		self.assertEquals(node.asBytes(prefixes=prefixes, elementmode=2, procinstmode=2), """<s:wrap procinstns:p="http://www.php.net/" xmlns:s="http://xmlns.livinglogic.de/xist/ns/specials"><?p:php x?></s:wrap>""")

		prefixes = xsc.Prefixes()
		prefixes.addPrefixMapping(None, php)
		prefixes.addPrefixMapping("s", specials)

		self.assertEquals(node.asBytes(prefixes=prefixes, procinstmode=2), """<wrap procinstns="http://www.php.net/"><?php x?></wrap>""")
		# FIXME this depends on dict iteration order
		self.assertEquals(node.asBytes(prefixes=prefixes, elementmode=2, procinstmode=2), """<s:wrap procinstns="http://www.php.net/" xmlns:s="http://xmlns.livinglogic.de/xist/ns/specials"><?php x?></s:wrap>""")

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

class ParseTest(unittest.TestCase):
	def test_parselocationsgmlop(self):
		node = parsers.parseString("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parser=parsers.SGMLOPParser())
		self.assertEqual(len(node), 1)
		self.assertEqual(len(node[0]), 1)
		self.assertEqual(node[0][0].startloc.getSystemId(), "STRING")
		self.assertEqual(node[0][0].startloc.getLineNumber(), 1)

	def test_parselocationexpat(self):
		node = parsers.parseString("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parser=parsers.ExpatParser())
		self.assertEqual(len(node), 1)
		self.assertEqual(len(node[0]), 1)
		self.assertEqual(node[0][0].startloc.getSystemId(), "STRING")
		self.assertEqual(node[0][0].startloc.getLineNumber(), 1)
		self.assertEqual(node[0][0].startloc.getColumnNumber(), 3)

	def test_nsparse(self):
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
		prefixes = xsc.Prefixes().addElementPrefixMapping("x", ihtml)
		node = parsers.parseString(xml, prefixes=prefixes)
		node = node.find(type=xsc.Element, subtype=True)[0].compact() # get rid of the Frag and whitespace
		self.assertEquals(node, check)

	def test_parseurls(self):
		prefixes = xsc.Prefixes()
		prefixes.addElementPrefixMapping(None, html)
		node = parsers.parseString('<a href="4.html" style="background-image: url(3.gif);"/>', base="root:1/2.html", prefixes=prefixes)
		self.assertEqual(str(node[0]["style"]), "background-image: url(root:1/3.gif);")
		self.assertEqual(node[0]["style"].urls(), [url.URL("root:1/3.gif")])
		self.assertEqual(str(node[0]["href"]), "root:1/4.html")
		self.assertEqual(node[0]["href"].forInput(root="gurk/hurz.html"), url.URL("gurk/1/4.html"))

	def test_parserequiredattrs(self):
		class xmlns(xsc.Namespace):
			class Test(xsc.Element):
				class Attrs(xsc.Element.Attrs):
					class required(xsc.TextAttr): required = True

		prefixes = xsc.Prefixes()
		prefixes.addElementPrefixMapping(None, xmlns)
		node = parsers.parseString('<Test required="foo"/>', prefixes=prefixes)
		self.assertEqual(str(node[0]["required"]), "foo")

		warnings.filterwarnings("error", category=errors.RequiredAttrMissingWarning)
		try:
			node = parsers.parseString('<Test/>', prefixes=prefixes)
		except saxlib.SAXParseException, exc:
			self.assert_(isinstance(exc.getException(), errors.RequiredAttrMissingWarning))
			pass
		else:
			self.fail()

	def test_parsevalueattrs(self):
		class xmlns(xsc.Namespace):
			class Test(xsc.Element):
				class Attrs(xsc.Element.Attrs):
					class withvalues(xsc.TextAttr): values = ("foo", "bar")

		prefixes = xsc.Prefixes()
		prefixes.addElementPrefixMapping(None, xmlns)

		warnings.filterwarnings("error", category=errors.IllegalAttrValueWarning)
		node = parsers.parseString('<Test withvalues="bar"/>', prefixes=prefixes)
		self.assertEqual(str(node[0]["withvalues"]), "bar")
		try:
			node = parsers.parseString('<Test withvalues="baz"/>', prefixes=prefixes)
		except saxlib.SAXParseException, exc:
			self.assert_(isinstance(exc.getException(), errors.IllegalAttrValueWarning))
			pass
		else:
			self.fail()

def test_main():
	unittest.main()

if __name__ == "__main__":
	test_main()
