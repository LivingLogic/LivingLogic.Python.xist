#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, unittest, cStringIO, warnings

from xml.parsers import expat

import py.test

from ll import url
from ll.xist import xsc, parsers, css, presenters, converters, sims, xnd, xfind
from ll.xist.ns import wml, ihtml, html, chars, abbr, specials, htmlspecials, meta, form, php, xml, tld, docbook

import xist_common as common


# set to something ASCII, so presenters work, even if the system default encoding is ascii
presenters.reprtab = "  "


def check_lenunicode(node, _len, content):
	assert len(node) == _len
	assert unicode(node) == content


def test_fraglen():
	check_lenunicode(xsc.Frag(), 0, u"")
	check_lenunicode(xsc.Frag(1), 1, u"1")
	check_lenunicode(xsc.Frag(1, 2, 3), 3, u"123")
	check_lenunicode(xsc.Frag(None), 0, u"")
	check_lenunicode(xsc.Frag(None, None, None), 0, u"")
	check_lenunicode(xsc.Frag(1, None, 2, None, 3, None, 4), 4, u"1234")
	check_lenunicode(xsc.Frag(1, (2, 3)), 3, u"123")
	check_lenunicode(xsc.Frag(1, (None, None)), 1, u"1")


def test_append():
	for cls in (xsc.Frag, html.div):
		node = cls()
		node.append(1)
		check_lenunicode(node, 1, u"1")
		node.append(2)
		check_lenunicode(node, 2, u"12")
		node.append()
		check_lenunicode(node, 2, u"12")
		node.append(3, 4)
		check_lenunicode(node, 4, u"1234")
		node.append(None)
		check_lenunicode(node, 4, u"1234")
		node.append((5, 6))
		check_lenunicode(node, 6, u"123456")
		node.append(html.p.Attrs.id(7))
		check_lenunicode(node, 7, u"1234567")
		py.test.raises(TypeError, node.append, xml.Attrs(lang=8))


def test_extend():
	for cls in (xsc.Frag, html.div):
		node = cls()
		node.extend([1])
		check_lenunicode(node, 1, u"1")
		node.extend([2])
		check_lenunicode(node, 2, u"12")
		node.extend([])
		check_lenunicode(node, 2, u"12")
		node.extend([None])
		check_lenunicode(node, 2, u"12")
		node.extend([3, 4])
		check_lenunicode(node, 4, u"1234")
		node.extend([[], [[], [5], []]])
		check_lenunicode(node, 5, u"12345")


def test_insert():
	for cls in (xsc.Frag, html.div):
		node = cls()
		node.insert(0, 1)
		check_lenunicode(node, 1, u"1")
		node.insert(0, 2)
		check_lenunicode(node, 2, u"21")
		node.insert(0, 3, 4)
		check_lenunicode(node, 4, u"3421")
		node.insert(0, None)
		check_lenunicode(node, 4, u"3421")
		node.insert(0, (5, 6))
		check_lenunicode(node, 6, u"563421")


def test_iadd():
	for cls in (xsc.Frag, html.div):
		node = cls()
		node += [1]
		check_lenunicode(node, 1, u"1")
		node += [2]
		check_lenunicode(node, 2, u"12")
		node += []
		check_lenunicode(node, 2, u"12")
		node += [None]
		check_lenunicode(node, 2, u"12")
		node += [3, 4]
		check_lenunicode(node, 4, u"1234")
		node += [[], [[], [5], []]]
		check_lenunicode(node, 5, u"12345")


def test_len():
	for cls in (xsc.Frag, html.div):
		check_lenunicode(cls(), 0, u"")
		check_lenunicode(cls(1), 1, u"1")
		check_lenunicode(cls(1, 2, 3), 3, u"123")
		check_lenunicode(cls(None), 0, u"")
		check_lenunicode(cls(None, None, None), 0, u"")
		check_lenunicode(cls(1, None, 2, None, 3, None, 4), 4, u"1234")
		check_lenunicode(cls(1, (2, 3)), 3, u"123")
		check_lenunicode(cls(1, (None, None)), 1, u"1")


def test_standardmethods():
	for node in common.allnodes():
		node.compact()
		node.normalized()
		list(node.walk((True, xsc.enterattrs, xsc.entercontent)))
		list(node.walknode((True, xsc.enterattrs, xsc.entercontent)))
		list(node.walkpath((True, xsc.enterattrs, xsc.entercontent)))
		node.pretty()
		node.clone()
		node.conv()
		node.normalized().compact().pretty()


def test_standardmethods2():
	for node in (common.createelement(), common.createfrag()):
		node.sorted()
		node.shuffled()
		node.reversed()


def test_stringify():
	for node in common.allnodes():
		unicode(node)
		str(node)
		node.string()
		node.bytes()
		list(node.iterstring())
		list(node.iterbytes())


def test_astext():
	for node in common.allnodes():
		html.astext(node)
		html.astext(node, width=120)


def test_number():
	node = html.div(class_=1234)
	assert int(node["class_"]) == 1234
	assert long(node["class_"]) == 1234L
	assert abs(float(node["class_"]) - 1234.) < 1e-2
	node = html.div(class_="1+1j")
	compl = complex(node["class_"])
	assert abs(compl.real - 1.) < 1e-2
	assert abs(compl.imag - 1.) < 1e-2


def test_write():
	node = html.div()
	io = cStringIO.StringIO()
	node.write(io, xhtml=2)
	assert io.getvalue() == "<div/>"


def test_mul():
	node = xsc.Frag("a")
	assert 3*node == xsc.Frag(list("aaa"))
	assert node*3 == xsc.Frag(list("aaa"))

	node = html.div()
	assert 3*node == xsc.Frag(html.div(), html.div(), html.div())
	assert node*3 == xsc.Frag(html.div(), html.div(), html.div())


def test_text():
	s = "test"
	node = xsc.Text(s)
	hash(node)
	assert len(node), 4
	assert node[1] == xsc.Text("e")
	assert 3*node == xsc.Text(3*s)
	assert node*3 == xsc.Text(s*3)
	assert node[1:3] == xsc.Text("es")
	assert node.capitalize() == xsc.Text("Test")
	assert node.center(8) == xsc.Text("  test  ")
	assert node.count("t") == 2
	assert node.endswith("st") is True
	assert node.index("s") == 2
	assert node.isalpha() is True
	assert node.isalnum() is True
	assert node.isdecimal() is False
	assert node.isdigit() is False
	assert node.islower() is True
	assert node.isnumeric() is False
	assert node.isspace() is False
	assert node.istitle() is False
	assert node.isupper() is False
	assert node.join(xsc.Frag(list("abc"))) == xsc.Frag("a", "test", "b", "test", "c")
	assert node.ljust(6) == xsc.Text("test  ")
	assert node.ljust(6, ".") == xsc.Text("test..")
	assert node.lower() == xsc.Text("test")
	assert xsc.Text("  test").lstrip() == xsc.Text("test")
	assert node.replace("s", "x") == xsc.Text("text")
	assert node.rjust(6) == xsc.Text("  test")
	assert node.rjust(6, ".") == xsc.Text("..test")
	assert xsc.Text("test  ").rstrip() == xsc.Text("test")
	assert node.rfind("s") == 2
	assert node.rindex("s") == 2
	assert node.split("e") == xsc.Frag("t", "st")
	assert xsc.Text("a\nb\n").splitlines() == xsc.Frag("a", "b")
	assert node.startswith("te") is True
	assert xsc.Text("  test  ").strip() == xsc.Text("test")
	assert node.swapcase() == xsc.Text("TEST")
	assert node.title() == xsc.Text("Test")
	assert node.upper() == xsc.Text("TEST")


def test_charref():
	node = chars.ouml()
	hash(node)
	assert len(node) == 1
	assert node[0] == xsc.Text(u"ö")
	assert 3*node == xsc.Text(u"ööö")
	assert node*3 == xsc.Text(u"ööö")
	assert node[1:-2] == xsc.Text()
	assert node.capitalize() == xsc.Text(u"Ö")
	assert node.center(5) == xsc.Text(u"  ö  ")
	assert node.count(u"t") == 0
	assert node.endswith(u"ö") is True
	assert node.index(u"ö") == 0
	assert node.isalpha() is True
	assert node.isalnum() is True
	assert node.isdecimal() is False
	assert node.isdigit() is False
	assert node.islower() is True
	assert node.isnumeric() is False
	assert node.isspace() is False
	assert node.istitle() is False
	assert node.isupper() is False
	assert node.ljust(3) == xsc.Text(u"ö  ")
	assert node.ljust(3, ".") == xsc.Text(u"ö..")
	assert node.lower() == xsc.Text(u"ö")
	assert node.replace(u"ö", "x") == xsc.Text("x")
	assert node.rjust(3) == xsc.Text(u"  ö")
	assert node.rjust(3, ".") == xsc.Text(u"..ö")
	assert node.rfind(u"ö") == 0
	assert node.rindex(u"ö") == 0
	assert node.startswith(u"ö") is True
	assert node.swapcase() == xsc.Text(u"Ö")
	assert node.title() == xsc.Text(u"Ö")
	assert node.upper() == xsc.Text(u"Ö")


def test_conv():
	def mappedmapper(node, converter):
		if isinstance(node, xsc.Text):
			node = node.replace("gurk", "hurz")
		return node

	node = common.createfrag()
	node.conv()
	node.conv(converters.Converter())
	node.mapped(mappedmapper, converters.Converter())


def test_repr():
	tests = common.allnodes()
	allpresenters = [c for c in presenters.__dict__.itervalues() if isinstance(c, type) and c is not presenters.Presenter and issubclass(c, presenters.Presenter)]
	for node in tests:
		repr(node)
		for class_ in allpresenters:
			presenter = class_(node)
			# do it multiple time, to make sure the presenter gets properly reset
			for i in xrange(3):
				list(presenter)
				str(presenter)


def test_attrsclone():
	class newa(html.a):
		def convert(self, converter):
			attrs = self.attrs.clone()
			attrs["href"].insert(0, "foo")
			e = html.a(self.content, attrs)
			return e.convert(converter)
	e = newa("gurk", href="hurz")
	e = e.conv().conv()
	assert unicode(e["href"]) == "foohurz"
	assert str(e["href"]) == "foohurz"


def test_attributes():
	node = html.h1("gurk", {xml.Attrs.lang: "de"}, lang="de")
	assert node.attrs.has("lang")
	assert node.attrs.has_xml("lang")

	assert node.attrs.has(html.h1.Attrs.lang)
	assert node.attrs.has_xml(html.h1.Attrs.lang)

	assert node.attrs.has(xml.Attrs.lang)
	assert node.attrs.has_xml(xml.Attrs.lang)

	assert "lang" in node.attrs
	assert html.h1.Attrs.lang in node.attrs
	assert xml.Attrs.lang in node.attrs


def test_attributekeysvaluesitems():
	def check(node, attrclass, attrvalue):
		assert list(node.attrs.allowedattrs()) == [attrclass]

		if attrvalue:
			assert list(node.attrs.keys()) == [attrclass]
		else:
			assert list(node.attrs.keys()) == []

		if attrvalue:
			res = list(node.attrs.values())
			assert len(res) == 1
			assert res[0].__class__ is node.Attrs.attr_
			assert unicode(res[0]) == attrvalue
		else:
			res = list(node.attrs.values())
			assert len(res) == 0

		if attrvalue:
			res = list(node.attrs.items())
			assert len(res) == 1
			assert res[0][0] is attrclass
			assert res[0][1].__class__ is attrclass
			assert unicode(res[0][1]) == attrvalue
		else:
			res = list(node.attrs.items())
			assert len(res) == 0

	class Test1(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class attr_(xsc.TextAttr):
				xmlname = "attr"
				default = 42
	class Test2(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class attr_(xsc.TextAttr):
				xmlname = "attr"

	yield check, Test1(), Test1.Attrs.attr_, u"42"
	yield check, Test1(attr_=17), Test1.Attrs.attr_, u"17"
	yield check, Test1(attr_=None), Test1.Attrs.attr_, None

	yield check, Test2(), Test2.Attrs.attr_, None
	yield check, Test2(attr_=17), Test2.Attrs.attr_, u"17"
	yield check, Test2(attr_=None), Test2.Attrs.attr_, None


def test_attributeswithoutnames():
	node = html.h1("gurk",
		{xml.Attrs.lang: "de", xml.Attrs.base: "http://www.livinglogic.de/"},
		lang="de",
		style="color: #fff",
		align="right",
		title="gurk",
		class_="important",
		id=42,
		dir="ltr"
	)
	keys = set(node.attrs.keys())
	keys.remove(html.h1.Attrs.class_)

	keys1 = set(node.attrs.withoutnames("class_").keys())
	assert keys == keys1

	keys.remove(xml.Attrs.lang)
	keys.remove(xml.Attrs.base)
	keys2 = set(node.attrs.withoutnames("class_", xml.Attrs.lang, xml.Attrs.base).keys())
	assert keys == keys2

	# Check that non existing attrs are handled correctly
	keys3 = set(node.attrs.withoutnames("class_", "src", xml.Attrs.lang, xml.Attrs.base).keys())
	assert keys == keys3


def test_attributeswithoutnames_xml():
	node = html.h1("gurk",
		title="gurk",
		class_="important",
		id=42,
	)
	keys = set(node.attrs.keys())
	keys.remove(html.h1.Attrs.class_)

	keys1 = set(node.attrs.withoutnames_xml("class").keys())
	assert keys == keys1


def test_attributeswithnames():
	class h1(html.h1):
		class Attrs(html.h1.Attrs):
			class lang(html.h1.Attrs.lang):
				default = 42

	node = h1("gurk",
		{xml.Attrs.space: 1, xml.Attrs.lang: "de"},
		class_="gurk",
		align="right"
	)

	assert set(node.attrs.withnames("id").keys()) == set()

	assert set(node.attrs.withnames("class_").keys()) == set([html.h1.Attrs.class_])

	assert set(node.attrs.withnames("lang", "align").keys()) == set([h1.Attrs.lang, html.h1.Attrs.align])

	assert set(node.attrs.withnames(h1.Attrs.lang, "align").keys()) == set([h1.Attrs.lang, html.h1.Attrs.align])

	assert set(node.attrs.withnames(html.h1.Attrs.lang, "align").keys()) == set([h1.Attrs.lang, html.h1.Attrs.align])

	node = html.h1("gurk",
		{xml.Attrs.space: 1, xml.Attrs.lang: "de"},
		lang="de",
		class_="gurk",
		align="right"
	)

	assert set(node.attrs.withnames("id").keys()) == set()

	assert set(node.attrs.withnames("class_").keys()) == set([html.h1.Attrs.class_])

	assert set(node.attrs.withnames("lang", "align").keys()) == set([html.h1.Attrs.lang, html.h1.Attrs.align])

	# no h1.Attrs.lang
	assert set(node.attrs.withnames(h1.Attrs.lang, "align").keys()) == set([html.h1.Attrs.align])

	assert set(node.attrs.withnames(html.h1.Attrs.lang, "align").keys()) == set([html.h1.Attrs.lang, html.h1.Attrs.align])


def test_attributeswithnames_xml():
	node = html.h1("gurk",
		{xml.Attrs.space: 1},
		lang="de",
		class_="gurk",
		align="right"
	)
	assert set(node.attrs.withnames_xml("class").keys()) == set([html.h1.Attrs.class_])
	assert set(node.attrs.withnames_xml(xml.Attrs.space).keys()) == set([xml.Attrs.space])



def test_defaultattributes():
	class Test(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class withdef(xsc.TextAttr): default = 42
			class withoutdef(xsc.TextAttr): pass
	node = Test()
	assert "withdef" in node.attrs
	assert "withoutdef" not in node.attrs
	py.test.raises(xsc.IllegalAttrError, node.attrs.__contains__, "illegal")
	node = Test(withdef=None)
	assert "withdef" not in node.attrs


def test_attributedictmethods():
	def check(listexp, iter):
		count = 0
		for item in iter:
			assert item in listexp
			count += 1
		assert count == len(listexp)

	class Test(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class withdef(xsc.TextAttr):
				default = 42
			class withoutdef(xsc.TextAttr):
				pass
			class another(xsc.URLAttr):
				pass

	node = Test(withoutdef=42)

	check(
		[ Test.Attrs.withdef, Test.Attrs.withoutdef ],
		node.attrs.keys(),
	)
	check(
		[ Test.Attrs.withdef(42), Test.Attrs.withoutdef(42)],
		node.attrs.values(),
	)
	check(
		[ (Test.Attrs.withdef, Test.Attrs.withdef(42)), (Test.Attrs.withoutdef, Test.Attrs.withoutdef(42)) ],
		node.attrs.items(),
	)

	check(
		[ Test.Attrs.another, Test.Attrs.withdef, Test.Attrs.withoutdef ],
		node.attrs.allowedattrs(),
	)


def test_fragattrdefault():
	class testelem(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class testattr(xsc.TextAttr):
				default = 42

	node = testelem()
	assert unicode(node["testattr"]) == "42"
	assert unicode(node.conv()["testattr"]) == "42"

	node["testattr"].clear()
	assert "testattr" not in node.attrs
	assert "testattr" not in node.conv().attrs

	node = testelem(testattr=23)
	assert unicode(node["testattr"]) == "23"
	assert unicode(node.conv()["testattr"]) == "23"

	del node["testattr"]
	assert unicode(node["testattr"]) == ""
	assert unicode(node.conv()["testattr"]) == ""

	node["testattr"] = 23
	node["testattr"] = None
	assert "testattr" not in node.attrs
	assert "testattr" not in node.conv().attrs

	node = testelem(testattr=None)
	assert "testattr" not in node.attrs
	assert "testattr" not in node.conv().attrs


def test_checkisallowed():
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
	assert node.attrs.isallowed("testattr") is True
	assert node.attrs.isallowed("notestattr") is False

	node = testelem2()
	assert node.attrs.isallowed("testattr") is True
	assert node.attrs.isallowed("notestattr") is False

	node = testelem3()
	assert node.attrs.isallowed("testattr") is True
	assert node.attrs.isallowed("testattr3") is True

	node = testelem4()
	assert node.attrs.isallowed("testattr") is False
	assert node.attrs.isallowed("testattr3") is True


def test_withsep():
	for class_ in (xsc.Frag, html.div):
		node = class_(1,2,3)
		assert unicode(node.withsep(",")) == u"1,2,3"
		node = class_(1)
		assert unicode(node.withsep(",")) == u"1"
		node = class_()
		assert unicode(node.withsep(",")) == u""


def test_allowedattr():
	assert html.a.Attrs.allowedattr("href") is html.a.Attrs.href
	py.test.raises(xsc.IllegalAttrError, html.a.Attrs.allowedattr, "gurk")
	assert html.a.Attrs.allowedattr(xml.Attrs.lang) is xml.Attrs.lang

	# Check inherited attributes
	assert htmlspecials.plaintable.Attrs.allowedattr("border") is htmlspecials.plaintable.Attrs.border
	assert htmlspecials.plaintable.Attrs.allowedattr(htmlspecials.plaintable.Attrs.border) is htmlspecials.plaintable.Attrs.border
	assert html.table.Attrs.allowedattr(htmlspecials.plaintable.Attrs.border) is html.table.Attrs.border


def test_plaintableattrs():
	e = htmlspecials.plaintable(border=3)
	assert isinstance(e["border"], html.table.Attrs.border)
	assert isinstance(e["cellpadding"], html.table.Attrs.cellpadding)
	e = e.conv()
	assert isinstance(e["border"], html.table.Attrs.border)
	assert isinstance(e["cellpadding"], html.table.Attrs.cellpadding)


def test_attrupdate():
	node = html.a(href="gurk", class_="hurz")
	node.attrs.update(xml.Attrs(lang="de"), {"href": "gurk2", html.a.Attrs.id: 42})
	assert unicode(node["href"]) == u"gurk2"
	assert unicode(node["id"]) == u"42"
	assert unicode(node[xml.Attrs.lang]) == u"de"

	node = html.a({xml.Attrs.lang: "de"}, href="gurk", class_="hurz")
	assert unicode(node[xml.Attrs.lang]) == u"de"

	node = html.a(xml.Attrs(lang="de"), href="gurk", class_="hurz")
	assert unicode(node[xml.Attrs.lang]) == u"de"

	class Gurk(xsc.Element):
		model = False
		class Attrs(xsc.Element.Attrs):
			class gurk(xsc.TextAttr): pass
			class hurz(xsc.TextAttr): default = "hinz+kunz"

	node1 = Gurk()
	node2 = Gurk(hurz=None)
	node1.attrs.update(node2.attrs)
	assert "hurz" not in node1.attrs

	node1 = Gurk(hurz=None)
	node2 = Gurk()
	node1.attrs.update(node2.attrs)
	assert "hurz" in node1.attrs

	node = Gurk(Gurk(hurz=None).attrs)
	assert "hurz" not in node.attrs

	attrs = Gurk.Attrs(Gurk.Attrs(hurz=None))
	assert "hurz" not in attrs


def test_classrepr():
	repr(xsc.Node)
	repr(xsc.Null.__class__)
	repr(xsc.Element)
	repr(xsc.ProcInst)
	repr(xsc.Entity)
	repr(xsc.CharRef)
	repr(xsc.Element.Attrs)
	repr(xml.Attrs)
	repr(xml.Attrs.lang)


def test_getitem():
	for cls in (xsc.Frag, html.div):
		e = cls(xrange(6))
		# int
		assert e[2] == xsc.Text(2)
		assert e[-1] == xsc.Text(5)

		# slice
		assert e[:] == xsc.Frag(xrange(6))
		assert e[:2] == xsc.Frag(0, 1)
		assert e[-2:] == xsc.Frag(4, 5)
		assert e[::2] == xsc.Frag(0, 2, 4)
		assert e[1::2] == xsc.Frag(1, 3, 5)
		assert e[::-1] == xsc.Frag(xrange(5, -1, -1))

		# selector
		e = cls((html.dt(i), html.dd(2*i)) for i in xrange(3))
		assert xsc.Frag(e[html.dt]) == xsc.Frag(html.dt(0), html.dt(1), html.dt(2))
		assert xsc.Frag(e[html.dt[1]]) == xsc.Frag(html.dt(1))
		assert e[e[0]][0] is e[0] # selector for a single node (returns an iterator nevertheless)
		def isgt1(p):
			return int(str(p[-1]))>1
		assert xsc.Frag(e[html.dt & isgt1]) == xsc.Frag(html.dt(2))
		assert xsc.Frag(e[e/html.dt]) == xsc.Frag(html.dt(0), html.dt(1), html.dt(2))
		assert xsc.Frag(e[e.__class__/html.dt]) == xsc.Frag(html.dt(0), html.dt(1), html.dt(2))

		for attr in ("class_", xml.Attrs.lang):
			e = cls("foo", html.div("bar", {attr: "gurk"}), "baz")
			i = e[xsc.Text]
			assert str(i.next()) == "foo"
			assert str(i.next()) == "baz"
			py.test.raises(StopIteration, i.next)

		# list
		for attr in ("class_", xml.Attrs.lang):
			node = cls(html.div("foo", html.div("bar", {attr: "gurk"}), "baz"))
			assert node[[]] == node[:]
			assert str(node[[0, 1]]) == "bar"
			assert str(node[[0, 1, attr]]) == "gurk"


def test_setitem():
	for cls in (xsc.Frag, html.div):
		e = cls(range(6))
		e[1] = 10
		assert e == cls(0, 10, 2, 3, 4, 5)
		e[1] = None
		assert e == cls(0, 2, 3, 4, 5)
		e[1] = ()
		assert e == cls(0, 3, 4, 5)

		e = cls(range(6))
		e[-1] = None
		assert e == cls(0, 1, 2, 3, 4)

		e = cls(range(6))
		e[1:5] = (100, 200)
		assert e == cls(0, 100, 200, 5)

		e = cls(range(6))
		e[:] = (100, 200)
		assert e == cls(100, 200)

		e = cls(range(6))
		e[::2] = (100, 120, 140)
		assert e == cls(100, 1, 120, 3, 140, 5)

		e = cls(range(6))
		e[1::2] = (110, 130, 150)
		assert e == cls(0, 110, 2, 130, 4, 150)

		e = cls(range(6))
		e[::-1] = range(6)
		assert e == cls(range(5, -1, -1))

		for attr in ("class_", xml.Attrs.lang):
			node = cls(html.div("foo", html.div({attr: "gurk"}), "bar"))
			node[[0, 1, attr]] = "hurz"
			assert str(node[[0, 1, attr]]) == "hurz"
			py.test.raises(ValueError, node.__setitem__, [], None)
			py.test.raises(ValueError, node.__delitem__, [])


def test_delitem():
	for cls in (xsc.Frag, html.div):
		e = cls(range(6))
		del e[0]
		assert e == cls(1, 2, 3, 4, 5)
		del e[-1]
		assert e == cls(1, 2, 3, 4)

		e = cls(range(6))
		del e[1:5]
		assert e == cls(0, 5)

		e = cls(range(6))
		del e[2:]
		assert e == cls(0, 1)

		e = cls(range(6))
		del e[-2:]
		assert e == cls(0, 1, 2, 3)

		e = cls(range(6))
		del e[:2]
		assert e == cls(2, 3, 4, 5)

		e = cls(range(6))
		del e[:-2]
		assert e == cls(4, 5)

		e = cls(range(6))
		del e[:]
		assert e == cls()

		e = cls(range(6))
		del e[::2]
		assert e == cls(1, 3, 5)

		e = cls(range(6))
		del e[1::2]
		assert e == cls(0, 2, 4)


def test_clone():
	for cls in (xsc.Frag, html.div):
		e = html.div(1)

		src = cls(1, e, e)

		dst = src.clone()
		assert src is not dst
		assert src[0] is dst[0] # Text nodes are immutable and shared
		assert src[1] is not dst[1]
		assert dst[1] is not dst[2]

		e.append(e) # create a cycle

		dst = src.copy()
		assert src is not dst
		assert src[0] is dst[0]
		assert src[1] is dst[1]
		assert dst[1] is dst[2]

		dst = src.deepcopy()
		assert src is not dst
		assert src[0] is dst[0]
		assert src[1] is not dst[1]
		assert dst[1] is dst[2]

	e = html.div(id=(17, html.div(23), 42))
	for src in (e, e.attrs):
		dst = src.clone()
		assert src["id"] is not dst["id"]
		assert src["id"][0] is dst["id"][0]
		assert src["id"][1] is not dst["id"][1]

	e["id"][1] = e # create a cycle
	e["id"][2] = e # create a cycle
	for src in (e, e.attrs):
		dst = src.copy()
		assert src["id"] is dst["id"]
		assert src["id"][0] is dst["id"][0]
		assert src["id"][1] is dst["id"][1]
		assert dst["id"][1] is dst["id"][2]
		dst = src.deepcopy()
		assert src["id"] is not dst["id"]
		assert src["id"][0] is dst["id"][0]
		assert src["id"][1] is not dst["id"][1]
		assert dst["id"][1] is dst["id"][2]


def test_sortedreversed():
	for class_ in (xsc.Frag, html.div):
		node = class_(3, 2, 1)
		node2 = node.sorted(key=str)
		assert node == class_(3, 2, 1)
		assert node2 == class_(1, 2, 3)

	for class_ in (xsc.Frag, html.div):
		node = class_(3, 2, 1)
		node2 = node.reversed()
		assert node == class_(3, 2, 1)
		assert node2 == class_(1, 2, 3)


def test_with():
	with xsc.build():
		with html.ul() as e:
			+html.li(1)
			+html.li(2)
	assert e == html.ul(html.li(1), html.li(2))

	with xsc.build():
		with html.p() as e:
			+html.span(1)
			with html.b():
				+html.span(2)
			+html.span(3)
	assert e == html.p(html.span(1), html.b(html.span(2)), html.span(3))

	with xsc.build():
		with html.p() as e:
			+xsc.Text(1)
	assert e == html.p(1)

	with xsc.build():
		with html.p() as e:
			+xml.Attrs(lang="de")
	assert e == html.p(xml.Attrs(lang="de"))
	assert e.bytes() == '<p xml:lang="de"></p>'

	with xsc.build():
		with xsc.Frag() as e:
			+xsc.Text(1)
	assert e == xsc.Frag(1)

	# Test add()
	with xsc.build():
		with html.p() as e:
			xsc.add(1)
	assert e == html.p(1)

	with xsc.build():
		with html.p() as e:
			xsc.add(class_="foo")
	assert e == html.p(class_="foo")

	with xsc.build():
		with html.p() as e:
			xsc.add(dict(class_="foo"))
	assert e == html.p(class_="foo")

	with xsc.build():
		with html.p() as e:
			xsc.add(xml.Attrs(lang="en"))
	assert e == html.p(xml.Attrs(lang="en"))


def test_with_addattr():
	with xsc.build():
		with html.ul() as e:
			with xsc.addattr("id"):
				+xsc.Text("gurk")
	assert e == html.ul(id="gurk")

	with xsc.build():
		with html.ul() as e:
			with xsc.addattr(html.ul.Attrs.id):
				+xsc.Text("gurk")
	assert e == html.ul(id="gurk")
