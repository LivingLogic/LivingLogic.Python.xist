#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

import sys, unittest

from ll.xist import xsc, parsers, presenters, converters, helpers, errors
from ll.xist.ns import wml, ihtml, html, css, abbr, specials, php, xml

class XISTTestCase(unittest.TestCase):
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

	def test_elementlen(self):
		self.check_lenunicode(html.div(), 0, u"")
		self.check_lenunicode(html.div(1), 1, u"1")
		self.check_lenunicode(html.div(1, 2, 3), 3, u"123")
		self.check_lenunicode(html.div(None), 0, u"")
		self.check_lenunicode(html.div(None, None, None), 0, u"")
		self.check_lenunicode(html.div(1, None, 2, None, 3, None, 4), 4, u"1234")
		self.check_lenunicode(html.div(1, (2, 3)), 3, u"123")
		self.check_lenunicode(html.div(1, (None, None)), 1, u"1")

	def mappedmapper(self, node):
		if isinstance(node, xsc.Text):
			node = node.replace("gurk", "hurz")
		return node

	def test_standardmethods(self):
		node = xsc.Frag(
			xml.XML10(),
			html.DocTypeHTML401transitional(),
			xsc.Comment("gurk"),
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
			html.div(
				align="left"
			),
			html.span(
				1,
				2,
				class_="gurk",
				id=(1, 2, (3, 4)),
				lang=(
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
		unicode(node)
		str(node)
		node.repr()
		node.repr(presenters.PlainPresenter())
		node.repr(presenters.NormalPresenter())
		for showLocation in (False, True):
			for showPath in (False, True):
				node.repr(presenters.TreePresenter(showLocation=showLocation, showPath=showPath))
		node.repr(presenters.CodePresenter())
		node.conv()
		node.compact()
		node.normalized()
		node.asString()
		node.asBytes()
		node.find()
		node.sorted()
		node.mapped(self.mappedmapper)
		node.shuffled()
		node.pretty()
		node.normalized().compact().pretty()

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

	def check_namespace(self, module):
		for obj in module.__dict__.values():
			if isinstance(obj, type) and issubclass(obj, xsc.Node):
				node = obj()
				if isinstance(node, xsc.Element):
					for (attrname, attrvalue) in node.allowedattritems():
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
		self.assertEqual(xsc.amp.xmlname, "amp")
		self.assert_(xsc.amp.xmlns is xsc.xmlns)
		self.assertEqual(xsc.amp.xmlprefix(), "xsc")

	def test_attributes(self):
		node = html.h1("gurk",
			{(xml, "space"): 1, (xml, "lang"): "de", (xml, "base"): "http://www.livinglogic.de/"},
			lang="de",
			style="color: #fff",
			align="right",
			title="gurk",
			class_="important",
			id=42,
			dir="ltr"
		)
		self.assert_(node.hasattr("lang"))
		self.assert_(node.hasattr((xml, "lang")))
		self.assert_(node.hasattr((xml.xmlns, "lang")))
		self.assert_(node.hasattr((xml.xmlns.xmlname, "lang")))

		keys = node.attrs.keys()
		keys.sort()
		keys.remove("lang")

		keys1 = node.attrs.without(["lang"]).keys()
		keys1.sort()
		self.assertEqual(keys, keys1)

		keys.remove((xml.xmlns, "space"))
		keys2 = node.attrs.without(["lang", (xml, "space")]).keys()
		keys2.sort()
		self.assertEqual(keys, keys2)

		keys.remove((xml.xmlns, "lang"))
		keys.remove((xml.xmlns, "base"))
		keys3 = node.attrs.without(["lang", xml]).keys()
		keys3.sort()
		self.assertEqual(keys, keys3)

		# Check that non existing attrs are handled correctly
		keys4 = node.attrs.without(["lang", "src", None]).keys()
		keys4.sort()
		self.assertEqual(keys, keys4)

	def test_defaultattributes(self):
		class Test(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class withdef(xsc.TextAttr):
					default = 42
				class withoutdef(xsc.TextAttr):
					pass
		node = Test()
		self.assert_(node.hasattr("withdef"))
		self.assert_(not node.hasattr("withoutdef"))
		self.assertRaises(errors.IllegalAttrError, node.hasattr, "illegal")
		node = Test(withdef=None)
		self.assert_(not node.hasattr("withdef"))

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
			node.attrkeys(),
			node.iterattrkeys(),
			node.attrs.keys(),
			node.attrs.iterkeys()
		)
		self.check_listiter(
			[ Test.Attrs.withdef(42), Test.Attrs.withoutdef(42)],
			node.attrvalues(),
			node.iterattrvalues(),
			node.attrs.values(),
			node.attrs.itervalues()
		)
		self.check_listiter(
			[ ("withdef", Test.Attrs.withdef(42)), ("withoutdef", Test.Attrs.withoutdef(42)) ],
			node.attritems(),
			node.iterattritems(),
			node.attrs.items(),
			node.attrs.iteritems()
		)

		self.check_listiter(
			[ "another", "withdef", "withoutdef" ],
			node.allowedattrkeys(),
			node.iterallowedattrkeys(),
			node.attrs.allowedkeys(),
			node.attrs.iterallowedkeys()
		)
		self.check_listiter(
			[ Test.Attrs.another, Test.Attrs.withdef, Test.Attrs.withoutdef ],
			node.allowedattrvalues(),
			node.iterallowedattrvalues(),
			node.attrs.allowedvalues(),
			node.attrs.iterallowedvalues()
		)
		self.check_listiter(
			[ ("another", Test.Attrs.another), ("withdef", Test.Attrs.withdef), ("withoutdef", Test.Attrs.withoutdef) ],
			node.allowedattritems(),
			node.iterallowedattritems(),
			node.attrs.alloweditems(),
			node.attrs.iteralloweditems()
		)

	def test_nsparse(self):
		xml = """
			<x:a>
				<x:a xmlns:x='http://www.w3.org/1999/xhtml'>
					<x:a xmlns:x='http://www.nttdocomo.co.jp/imode'>gurk</x:a>
				</x:a>
			</x:a>
		"""
		from ll.xist.ns import html, ihtml
		from ll.xist import presenters
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

	def test_fragattrdefault(self):
		class testelem(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class testattr(xsc.TextAttr):
					default = 42

		node = testelem()
		self.assertEquals(unicode(node["testattr"]), "42")
		self.assertEquals(unicode(node.conv()["testattr"]), "42")

		node["testattr"].clear()
		self.assert_(not node.hasattr("testattr"))
		self.assert_(not node.conv().hasattr("testattr"))

		node = testelem(testattr=23)
		self.assertEquals(unicode(node["testattr"]), "23")
		self.assertEquals(unicode(node.conv()["testattr"]), "23")

		del node["testattr"]
		self.assertEquals(unicode(node["testattr"]), "42")
		self.assertEquals(unicode(node.conv()["testattr"]), "42")

		node["testattr"] = None
		self.assert_(not node.hasattr("testattr"))
		self.assert_(not node.conv().hasattr("testattr"))

		node = testelem(testattr=None)
		self.assert_(not node.hasattr("testattr"))
		self.assert_(not node.conv().hasattr("testattr"))

	def test_checkisallowed(self):
		class testelem(xsc.Element):
			class Attrs(xsc.Element.Attrs):
				class testattr(xsc.TextAttr):
					pass

		node = testelem()
		self.assertEquals(node.isallowedattr("testattr"), True)
		self.assertEquals(node.attrs.isallowed("testattr"), True)

		self.assertEquals(node.isallowedattr("notestattr"), False)
		self.assertEquals(node.attrs.isallowed("notestattr"), False)

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

if __name__ == "__main__":
	unittest.main()
