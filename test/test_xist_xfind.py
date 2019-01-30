#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import pytest

from ll import misc
from ll.xist import xsc, xfind, parse
from ll.xist.ns import html, php, abbr


node = xsc.Frag(
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
	php.php("echo $footer;"),
	abbr.xist(),
)


def test_levels():
	def check(node, expr, ids):
		assert "".join(str(e.attrs.id) for e in node.walknodes(expr)) == ids

	ds = [html.div(id=id) for id in range(8)]
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
		check(ds[0], got, exp)


def test_isinstance():
	res = list(node.walknodes(html.h1))
	assert len(res) == 2
	assert res[0] is node[0][0]
	assert res[1] is node[1][0]

	def check(res):
		assert len(res) == 3
		assert res[0] is node[0][0]
		assert res[1] is node[1][0]
		assert res[2] is node[1][2][0]

	check(list(node.walknodes(xfind.IsInstanceSelector(html.h1, html.h2))))
	check(list(node.walknodes(xfind.IsInstanceSelector(html.h1) | html.h2)))
	check(list(node.walknodes(html.h1 | xfind.IsInstanceSelector(html.h2))))
	check(list(node.walknodes(html.h1 | html.h2)))
	check(list(node.walknodes(html.h1, html.h2)))
	check(list(node.walknodes(html.h1, html.h2, ~xfind.any)))
	check(list(node.walknodes(xsc.Element & ~(xsc.Text | html.p | html.div | html.em | html.img))))


def test_element():
	def check(expr, res):
		assert [str(e) for e in node.walknodes(expr)] == res
	result = ["important", "first", "second", "important", "first", "important", "second", "important", "only"]
	check(xfind.element(None, "gurk"), [])
	check(xfind.element("nix", "gurk"), [])
	check(xfind.element(html, "em"), result)
	check(xfind.element(html.xmlns, "em"), result)


def test_procinst():
	def check(expr, res):
		assert [e for e in node.walknodes(expr)] == res
	check(xfind.procinst("foo"), [])
	check(xfind.procinst("php"), [node[-2]])


def test_entity():
	def check(expr, res):
		assert [e for e in node.walknodes(expr)] == res
	check(xfind.entity("foo"), [])
	check(xfind.entity("xist"), [node[-1]])


def test_is():
	# Frags will be put into the path (but only as the root of the path),
	# but the selector will not be called for the Frag, so when the first call
	# happens there are already two nodes in the path. This is done on purpose:
	# selectors should not have to special case Frags
	res = list(node.walknodes(node))
	assert len(res) == 0

	res = list(node.walknodes(node[0]))
	assert len(res) == 1
	assert res[0] is node[0]


def test_isroot():
	res = list(node.walknodes(xfind.isroot))
	assert len(res) == 0

	res = list(node[0].walknodes(xfind.isroot))
	assert len(res) == 1
	assert res[0] is node[0]


def test_empty():
	res = list(node.walknodes(xfind.empty))
	assert len(res) == 2
	assert res[0] is node[1][0][-1]
	assert res[1] is node[1][-1]


def test_onlychild():
	res = list(node.walknodes(xfind.onlychild & html.em))
	assert len(res) == 1
	assert res[0] is node[2][0]


def test_onlyoftype():
	res = list(node.walknodes(xfind.onlyoftype & html.h1))
	assert len(res) == 2
	assert res[0] is node[0][0]
	assert res[1] is node[1][0]

	res = list(node.walknodes(xfind.onlyoftype & html.div))
	assert len(res) == 0

	res = list(node.walknodes(xfind.onlyoftype & html.p))
	assert len(res) == 3
	assert res[0] is node[1][1]
	assert res[1] is node[1][2][1]
	assert res[2] is node[2]


def test_hasattr():
	# hasattr
	res = list(node.walknodes(xfind.hasattr("class")))
	assert len(res) == 1
	assert res[0] is node[1]

	res = list(node.walknodes(xfind.hasattr(html.div.Attrs.id, html.div.Attrs.align)))
	assert len(res) == 3
	assert res[0] is node[0]
	assert res[1] is node[1][2]
	assert res[2] is node[1][3]


def test_attrhasvalue():
	def check(expected, attrname, *attrvalues):
		got = list(node.walknodes(xfind.attrhasvalue(attrname, *attrvalues)))
		assert len(got) == len(expected)
		for (gotnode, expectednode) in zip(got, expected):
			assert gotnode is expectednode

	check([node[0]], "align", "left")
	check([node[0]], html.div.Attrs.align, "left")
	check([node[0]], "align", "right", "center", "left")
	check([], "align", "right", "center")
	check([], "align", "right")
	check([], "gurk", "hurz")


def test_attrcontains():
	def check(expected, attrname, *attrvalues):
		got = list(node.walknodes(xfind.attrcontains(attrname, *attrvalues)))
		assert len(got) == len(expected)
		for (gotnode, expectednode) in zip(got, expected):
			assert gotnode is expectednode

	check([node[0]], "align", "ef")
	check([node[0]], html.div.Attrs.align, "ef")
	check([node[0]], "align", "ri", "ef")
	check([], "align", "ri", "en")
	check([], "align", "x")
	check([], "gurk", "nix")


def test_attrstartswith():
	def check(expected, attrname, *attrvalues):
		got = list(node.walknodes(xfind.attrstartswith(attrname, *attrvalues)))
		assert len(got) == len(expected)
		for (gotnode, expectednode) in zip(got, expected):
			assert gotnode is expectednode

	check([node[0]], "align", "le")
	check([node[0]], html.div.Attrs.align, "le")
	check([node[0]], "align", "ri", "ce", "le")
	check([], "align", "ri", "ce")
	check([], "align", "eft")
	check([], "gurk", "nix")
	check([node[1][0][1]], "src", "root:")


def test_attrendswith():
	def check(expected, attrname, *attrvalues):
		got = list(node.walknodes(xfind.attrendswith(attrname, *attrvalues)))
		assert len(got) == len(expected)
		for (gotnode, expectednode) in zip(got, expected):
			assert gotnode is expectednode

	check([node[0]], "align", "ft")
	check([node[0]], html.div.Attrs.align, "ft")
	check([node[0]], "align", "ht", "er", "ft")
	check([], "align", "ht", "er")
	check([], "align", "lef")
	check([], "gurk", "nix")
	check([node[1][0][1]], "src", ".gif")


def test_hasid():
	res = list(node.walknodes(xfind.hasid("id42")))
	assert len(res) == 1
	assert res[0] is node[1][2]


def test_hasclass():
	res = list(node.walknodes(xfind.hasclass("foo")))
	assert len(res) == 1
	assert res[0] is node[1]


def test_frag():
	e = parse.tree(b"das ist <b>klaus</b>. das ist <b>erich</b>", parse.SGMLOP(), parse.NS(html), parse.Node())
	assert "".join(map(str, e.walknodes(e//html.b))) == "klauserich"


def test_multiall():
	def check(node, expr, ids):
		assert "".join(str(e.attrs.id) for e in node.walknodes(expr)) == ids

	#        ____0____
	#       /         \
	#     _1_         _2_
	#    /   \       /   \
	#   3     4     5     6
	#  / \   / \   / \   / \
	# 7   8 9   a b   c d   e
	ds = [html.div(id=hex(id).lower()[2:]) for id in range(15)]
	for i in range(7):
		ds[i].append(ds[2*i+1:2*i+3])
	check(ds[0], ds[0]//html.div//html.div, "37849a5bc6de")


def test_itemsslices():
	def check(node, expr, ids):
		assert "".join(str(e.attrs.id) for e in node.walknodes(expr)) == ids

	#        ____0____
	#       /    |    \
	#     _1_   _2_   _3_
	#    /   \ /   \ /   \
	#   4     5     6     7
	ds = [html.div(id=id) for id in range(8)]
	ds[0].append(ds[1], ds[2], ds[3])
	ds[1].append(ds[4], ds[5])
	ds[2].append(ds[5], ds[6])
	ds[3].append(ds[6], ds[7])

	tests = [
		(ds[0]/html.div[0]/html.div[-1], "5"),
		(ds[0]/html.div/html.div[-1], "567"),
		(ds[0]/html.div[-1]/html.div, "67"),
		(ds[0]/html.div/html.div, "455667"), # we get 5 and 6 twice
		#(ds[0]/(html.div/html.div) & xfind.nthchild(2), u"5"), # we get 5 and 6 twice
		#(ds[0]/html.div[:]/html.div[:], u"455667"),
		(ds[0]/html.div/html.p[0], ""),
		(ds[0]/html.p[0]/html.p[0], ""),
		(ds[0]//html.div, "145256367"),
	]
	for (got, exp) in tests:
		check(ds[0], got, exp)


def test_item():
	e = html.div(range(10))
	assert str(misc.item(e[xsc.Text], 0)) == "0"
	assert str(misc.item(e[xsc.Text], 9)) == "9"
	assert str(misc.item(e[xsc.Text], -1)) == "9"
	assert str(misc.item(e[xsc.Text], -10)) == "0"
	misc.item(e[xsc.Text], 10) is None
	misc.item(e[xsc.Text], -11) is None
	assert str(misc.item(e[xsc.Text], 10, "x")) == "x"
	assert str(misc.item(e[xsc.Text], -11, "x")) == "x"
