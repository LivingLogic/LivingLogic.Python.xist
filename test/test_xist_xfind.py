#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import py.test

from ll import misc
from ll.xist import xsc, xfind, parsers
from ll.xist.ns import html


def xfindnode():
	return xsc.Frag(
		html.div(
			html.h1("The ", html.em("important"), " headline"),
			html.p("The ", html.em("first"), " paragraph."),
			html.p("The ", html.em("second"), " ", html.em("important"), " paragraph."),
			align="left",
		),
		html.div(
			html.h1("The headline", html.img(src="root:gurk.gif")),
			html.p("The ", html.em("first"), " paragraph."),
			html.div(
				html.h2("The ", html.em("important"), " headline"),
				html.p("The ", html.em("second"), " ", html.em("important"), " paragraph."),
				id="id42",
			),
			html.div(id="id23"),
			class_="foo",
		),
		html.p(html.em("only")),
	)


def test_levels():
	def check(node, expr, ids):
		assert "".join(str(e.attrs.id) for e in node.walknode(expr)) == ids

	ds = [html.div(id=id) for id in xrange(8)]
	ds[1].append(ds[4:7])
	ds[2].append(ds[7])
	ds[0].append(ds[1:4])
	#      ____0____
	#     /    |    \
	#   _1_    2     3
	#  / | \   |
	# 4  5  6  7

	tests = [
		(ds[0]//html.div, "1456273"),
		(ds[0]/html.div, "123"),
		(ds[0]/html.div/html.div, "4567"),
		(ds[0]/html.div/html.div/html.div, ""),
	]
	for (got, exp) in tests:
		yield check, ds[0], got, exp


def test_isinstance():
	node = xfindnode()
	res = list(node.walknode(html.h1))
	assert len(res) == 2
	assert res[0] is node[0][0]
	assert res[1] is node[1][0]

	def check(res):
		assert len(res) == 3
		assert res[0] is node[0][0]
		assert res[1] is node[1][0]
		assert res[2] is node[1][2][0]

	yield check, list(node.walknode(xfind.IsInstanceSelector(html.h1, html.h2)))
	yield check, list(node.walknode(xfind.IsInstanceSelector(html.h1) | html.h2))
	yield check, list(node.walknode(html.h1 | xfind.IsInstanceSelector(html.h2)))
	yield check, list(node.walknode(html.h1 | html.h2))
	yield check, list(node.walknode(xsc.Element & ~(xsc.Text | html.p | html.div | html.em | html.img)))


def test_hasname():
	node = xfindnode()

	def check(expr, res):
		assert [str(e) for e in node.walknode(expr)] == res
	result = ["important", "first", "second", "important", "first", "important", "second", "important", "only"]
	yield check, xfind.hasname("em"), result
	yield check, xfind.hasname("em", html), result
	yield check, xfind.hasname("em", html.xmlns), result
	yield check, xfind.hasname("em", "gurk"), []
	yield check, xfind.hasname_xml("em"), result
	yield check, xfind.hasname_xml("em", html), result
	yield check, xfind.hasname_xml("em", html.xmlns), result
	yield check, xfind.hasname_xml("em", "gurk"), []


def test_is():
	node = xfindnode()

	# Frags will be put into the path, but the walk filter will not be called for the Frag,
	# so when the first call happens there are already two nodes in the path
	# This is done on purpose: filters should not have to special case Frags
	res = list(node.walknode(node))
	assert len(res) == 0

	res = list(node.walknode(node[0]))
	assert len(res) == 1
	assert res[0] is node[0]


def test_isroot():
	node = xfindnode()
	res = list(node.walknode(xfind.isroot))
	assert len(res) == 0

	res = list(node[0].walknode(xfind.isroot))
	assert len(res) == 1
	assert res[0] is node[0]


def test_empty():
	node = xfindnode()
	res = list(node.walknode(xfind.empty))
	assert len(res) == 2
	assert res[0] is node[1][0][-1]
	assert res[1] is node[1][-1]


def test_onlychild():
	node = xfindnode()
	res = list(node.walknode(xfind.onlychild & html.em))
	assert len(res) == 1
	assert res[0] is node[2][0]


def test_onlyoftype():
	node = xfindnode()
	res = list(node.walknode(xfind.onlyoftype & html.h1))
	assert len(res) == 2
	assert res[0] is node[0][0]
	assert res[1] is node[1][0]

	res = list(node.walknode(xfind.onlyoftype & html.div))
	assert len(res) == 0

	res = list(node.walknode(xfind.onlyoftype & html.p))
	assert len(res) == 3
	assert res[0] is node[1][1]
	assert res[1] is node[1][2][1]
	assert res[2] is node[2]


def test_hasattr():
	node = xfindnode()

	# hasattr
	res = list(node.walknode(xfind.hasattr("class_")))
	assert len(res) == 1
	assert res[0] is node[1]

	res = list(node.walknode(xfind.hasattr(html.div.Attrs.id, html.div.Attrs.align)))
	assert len(res) == 3
	assert res[0] is node[0]
	assert res[1] is node[1][2]
	assert res[2] is node[1][3]

	# hasattr_xml
	res = list(node.walknode(xfind.hasattr_xml("class")))
	assert len(res) == 1
	assert res[0] is node[1]

	res = list(node.walknode(xfind.hasattr_xml(html.div.Attrs.id, html.div.Attrs.align)))
	assert len(res) == 3
	assert res[0] is node[0]
	assert res[1] is node[1][2]
	assert res[2] is node[1][3]


def test_attrhasvalue():
	node = xfindnode()

	def check(expected, attrname, *attrvalues):
		for selector in (xfind.attrhasvalue, xfind.attrhasvalue_xml):
			got = list(node.walknode(selector(attrname, *attrvalues)))
			assert len(got) == len(expected)
			for (gotnode, expectednode) in zip(got, expected):
				assert gotnode is expectednode

	yield check, [node[0]], "align", "left"
	yield check, [node[0]], html.div.Attrs.align, "left"
	yield check, [node[0]], "align", "right", "center", "left"
	yield check, [], "align", "right", "center"
	yield check, [], "align", "right"
	yield check, [], "gurk", "hurz"


def test_attrcontains():
	node = xfindnode()

	def check(expected, attrname, *attrvalues):
		for selector in (xfind.attrcontains, xfind.attrcontains_xml):
			got = list(node.walknode(selector(attrname, *attrvalues)))
			assert len(got) == len(expected)
			for (gotnode, expectednode) in zip(got, expected):
				assert gotnode is expectednode

	yield check, [node[0]], "align", "ef"
	yield check, [node[0]], html.div.Attrs.align, "ef"
	yield check, [node[0]], "align", "ri", "ef"
	yield check, [], "align", "ri", "en"
	yield check, [], "align", "x"
	yield check, [], "gurk", "", 


def test_attrstartswith():
	node = xfindnode()

	def check(expected, attrname, *attrvalues):
		for selector in (xfind.attrstartswith, xfind.attrstartswith_xml):
			got = list(node.walknode(selector(attrname, *attrvalues)))
			assert len(got) == len(expected)
			for (gotnode, expectednode) in zip(got, expected):
				assert gotnode is expectednode

	yield check, [node[0]], "align", "le"
	yield check, [node[0]], html.div.Attrs.align, "le"
	yield check, [node[0]], "align", "ri", "ce", "le"
	yield check, [], "align", "ri", "ce"
	yield check, [], "align", "eft"
	yield check, [], "gurk", ""
	yield check, [node[1][0][1]], "src", "root:"


def test_attrendswith():
	node = xfindnode()

	def check(expected, attrname, *attrvalues):
		for selector in (xfind.attrendswith, xfind.attrendswith_xml):
			got = list(node.walknode(selector(attrname, *attrvalues)))
			assert len(got) == len(expected)
			for (gotnode, expectednode) in zip(got, expected):
				assert gotnode is expectednode

	yield check, [node[0]], "align", "ft"
	yield check, [node[0]], html.div.Attrs.align, "ft"
	yield check, [node[0]], "align", "ht", "er", "ft"
	yield check, [], "align", "ht", "er"
	yield check, [], "align", "lef"
	yield check, [], "gurk", ""
	yield check, [node[1][0][1]], "src", ".gif"


def test_hasid():
	node = xfindnode()
	res = list(node.walknode(xfind.hasid("id42")))
	assert len(res) == 1
	assert res[0] is node[1][2]


def test_hasclass():
	node = xfindnode()
	res = list(node.walknode(xfind.hasclass("foo")))
	assert len(res) == 1
	assert res[0] is node[1]


def test_frag():
	e = parsers.parsestring("das ist <b>klaus</b>. das ist <b>erich</b>", parser=parsers.SGMLOPParser(), prefixes={None: html})
	assert u"".join(map(unicode, e.walknode(e//html.b))) == u"klauserich"


def test_multiall():
	def check(node, expr, ids):
		assert "".join(str(e.attrs.id) for e in node.walknode(expr)) == ids

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
	check(ds[0], ds[0]//html.div//html.div, "37849a5bc6de")


def test_itemsslices():
	def check(node, expr, ids):
		assert "".join(str(e.attrs.id) for e in node.walknode(expr)) == ids

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

	tests = [
		(ds[0]/html.div[0]/html.div[-1], "5"),
		(ds[0]/html.div/html.div[-1], "567"),
		(ds[0]/html.div[-1]/html.div, "67"),
		(ds[0]/html.div/html.div, "455667"), # we get 5 and 6 twice
		#(ds[0]/(html.div/html.div) & xfind.nthchild(2), "5"), # we get 5 and 6 twice
		#(ds[0]/html.div[:]/html.div[:], "455667"),
		(ds[0]/html.div/html.p[0], ""),
		(ds[0]/html.p[0]/html.p[0], ""),
		(ds[0]//html.div, "145256367"),
	]
	for (got, exp) in tests:
		yield check, ds[0], got, exp


def test_item():
	e = html.div(xrange(10))
	assert str(e[xsc.Text][0]) == "0"
	assert str(e[xsc.Text][9]) == "9"
	assert str(e[xsc.Text][-1]) == "9"
	assert str(e[xsc.Text][-10]) == "0"
	py.test.raises(IndexError, e[xsc.Text].__getitem__, 10)
	py.test.raises(IndexError, e[xsc.Text].__getitem__, -11)
	assert str(misc.item(e[xsc.Text], 10, "x")) == "x"
	assert str(misc.item(e[xsc.Text], -11, "x")) == "x"
