import sys, unittest

from xist import xsc, parsers, presenters, converters, helpers
from xist.ns import wml, ihtml, html, css, specials

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
			xsc.XML10(),
			html.DocTypeHTML401transitional(),
			xsc.Comment("gurk"),
			"hurz",
			html.nbsp(),
			specials.xist(),
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
						xsc.XML10(),
						"hurz",
						html.nbsp(),
						specials.xist(),
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
		for showLocation in (0, 1):
			for showPath in (0, 1):
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
		self.assertEqual(node[0][0].startLoc.getSystemId(), "STRING")
		self.assertEqual(node[0][0].startLoc.getLineNumber(), 1)

	def test_parselocationexpat(self):
		node = parsers.parseString("<z>gurk&amp;hurz&#42;hinz&#x666;hunz</z>", parser=parsers.ExpatParser())
		self.assertEqual(len(node), 1)
		self.assertEqual(len(node[0]), 1)
		self.assertEqual(node[0][0].startLoc.getSystemId(), "STRING")
		self.assertEqual(node[0][0].startLoc.getLineNumber(), 1)
		self.assertEqual(node[0][0].startLoc.getColumnNumber(), 3)

	def check_namespace(self, module):
		for obj in module.__dict__.values():
			if issubclass(obj.__class__, type) and issubclass(obj, xsc.Node):
				obj().conv().asBytes()

	def test_html(self):
		self.check_namespace(html)

	def test_ihtml(self):
		self.check_namespace(ihtml)

	def test_wml(self):
		self.check_namespace(wml)

	def test_css(self):
		self.check_namespace(css)

	escapeInput = u"".join([unichr(i) for i in xrange(1000)] + [unichr(i) for i in xrange(sys.maxunicode-10, sys.maxunicode+1)])

	def test_helpersescapeText(self):
		escapeOutput = []
		for c in self.escapeInput:
			if c==u"&":
				escapeOutput.append("&amp;")
			elif c==u"<":
				escapeOutput.append("&lt;")
			elif c==u">":
				escapeOutput.append("&gt;")
			else:
				try:
					escapeOutput.append(c.encode("ascii"))
				except UnicodeError:
					escapeOutput.append("&#%d;" % ord(c))
		escapeOutput = "".join(escapeOutput)
		self.assertEqual(helpers.escapeText(self.escapeInput, "ascii"), escapeOutput)

	def test_helpersescapeAttr(self):
		escapeOutput = []
		for c in self.escapeInput:
			if c==u"&":
				escapeOutput.append("&amp;")
			elif c==u"<":
				escapeOutput.append("&lt;")
			elif c==u">":
				escapeOutput.append("&gt;")
			elif c==u'"':
				escapeOutput.append("&quot;")
			else:
				try:
					escapeOutput.append(c.encode("ascii"))
				except UnicodeError:
					escapeOutput.append("&#%d;" % ord(c))
		escapeOutput = "".join(escapeOutput)
		self.assertEqual(helpers.escapeAttr(self.escapeInput, "ascii"), escapeOutput)

	def test_helpersescapeCSS(self):
		escapeOutput = []
		for c in self.escapeInput:
			try:
				escapeOutput.append(c.encode("ascii"))
			except UnicodeError:
				escapeOutput.append(("\\%x" % ord(c)).upper())
		escapeOutput = "".join(escapeOutput)
		self.assertEqual(helpers.escapeCSS(self.escapeInput, "ascii"), escapeOutput)

	def test_attrsclone(self):
		class newa(html.a):
			def convert(self, converter):
				attrs = self.attrs.clone()
				attrs["href"].insert(0, "foo")
				e = html.a(self.content, attrs)
				return e.convert(converter)
		e = newa("gurk", href="hurz")
		e = e.conv().conv()
		self.assertEqual(e["href"], "foohurz")

if __name__ == "__main__":
	unittest.main()
