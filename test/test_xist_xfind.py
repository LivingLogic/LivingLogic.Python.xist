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
from ll.xist import xsc, xfind, parse
from ll.xist.ns import html


def xfindnode():
	return xsc.Frag(
		html.div(
			html.h1(u"The ", html.em(u"important"), u" headline"),
			html.p(u"The ", html.em(u"first"), u" paragraph."),
			html.p(u"The ", html.em(u"second"), u" ", html.em(u"important"), u" paragraph."),
			align=u"left",
		),
		html.div(
			html.h1(u"The headline", html.img(src=u"root:gurk.gif")),
			html.p(u"The ", html.em(u"first"), u" paragraph."),
			html.div(
				html.h2(u"The ", html.em(u"important"), u" headline"),
				html.p(u"The ", html.em(u"second"), u" ", html.em(u"important"), u" paragraph."),
				id=u"id42",
			),
			html.div(id=u"id23"),
			class_=u"foo",
		),
		html.p(html.em(u"only")),
	)


def test_levels():
	def check(node, expr, ids):
		assert u"".join(unicode(e.attrs.id) for e in node.walknodes(expr)) == ids

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
		(ds[0]//html.div, u"1456273"),
		(ds[0]/html.div, u"123"),
		(ds[0]/html.div/html.div, u"4567"),
		(ds[0]/html.div/html.div/html.div, u""),
	]
	for (got, exp) in tests:
		yield check, ds[0], got, exp


def test_isinstance():
	node = xfindnode()
	res = list(node.walknodes(html.h1))
	assert len(res) == 2
	assert res[0] is node[0][0]
	assert res[1] is node[1][0]

	def check(res):
		assert len(res) == 3
		assert res[0] is node[0][0]
		assert res[1] is node[1][0]
		assert res[2] is node[1][2][0]

	yield check, list(node.walknodes(xfind.IsInstanceSelector(html.h1, html.h2)))
	yield check, list(node.walknodes(xfind.IsInstanceSelector(html.h1) | html.h2))
	yield check, list(node.walknodes(html.h1 | xfind.IsInstanceSelector(html.h2)))
	yield check, list(node.walknodes(html.h1 | html.h2))
	yield check, list(node.walknodes(xsc.Element & ~(xsc.Text | html.p | html.div | html.em | html.img)))


def test_hasname():
	node = xfindnode()

	def check(expr, res):
		assert [unicode(e) for e in node.walknodes(expr)] == res
	result = [u"important", u"first", u"second", u"important", u"first", u"important", u"second", u"important", u"only"]
	yield check, xfind.hasname(u"em"), result
	yield check, xfind.hasname(u"em", html), result
	yield check, xfind.hasname(u"em", html.xmlns), result
	yield check, xfind.hasname(u"em", u"gurk"), []
	yield check, xfind.hasname_xml(u"em"), result
	yield check, xfind.hasname_xml(u"em", html), result
	yield check, xfind.hasname_xml(u"em", html.xmlns), result
	yield check, xfind.hasname_xml(u"em", u"gurk"), []


def test_is():
	node = xfindnode()

	# Frags will be put into the path, but the walk filter will not be called for the Frag,
	# so when the first call happens there are already two nodes in the path
	# This is done on purpose: filters should not have to special case Frags
	res = list(node.walknodes(node))
	assert len(res) == 0

	res = list(node.walknodes(node[0]))
	assert len(res) == 1
	assert res[0] is node[0]


def test_isroot():
	node = xfindnode()
	res = list(node.walknodes(xfind.isroot))
	assert len(res) == 0

	res = list(node[0].walknodes(xfind.isroot))
	assert len(res) == 1
	assert res[0] is node[0]


def test_empty():
	node = xfindnode()
	res = list(node.walknodes(xfind.empty))
	assert len(res) == 2
	assert res[0] is node[1][0][-1]
	assert res[1] is node[1][-1]


def test_onlychild():
	node = xfindnode()
	res = list(node.walknodes(xfind.onlychild & html.em))
	assert len(res) == 1
	assert res[0] is node[2][0]


def test_onlyoftype():
	node = xfindnode()
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
	node = xfindnode()

	# hasattr
	res = list(node.walknodes(xfind.hasattr("class_")))
	assert len(res) == 1
	assert res[0] is node[1]

	res = list(node.walknodes(xfind.hasattr(html.div.Attrs.id, html.div.Attrs.align)))
	assert len(res) == 3
	assert res[0] is node[0]
	assert res[1] is node[1][2]
	assert res[2] is node[1][3]

	# hasattr_xml
	res = list(node.walknodes(xfind.hasattr_xml("class")))
	assert len(res) == 1
	assert res[0] is node[1]

	res = list(node.walknodes(xfind.hasattr_xml(html.div.Attrs.id, html.div.Attrs.align)))
	assert len(res) == 3
	assert res[0] is node[0]
	assert res[1] is node[1][2]
	assert res[2] is node[1][3]


def test_attrhasvalue():
	node = xfindnode()

	def check(expected, attrname, *attrvalues):
		for selector in (xfind.attrhasvalue, xfind.attrhasvalue_xml):
			got = list(node.walknodes(selector(attrname, *attrvalues)))
			assert len(got) == len(expected)
			for (gotnode, expectednode) in zip(got, expected):
				assert gotnode is expectednode

	yield check, [node[0]], u"align", u"left"
	yield check, [node[0]], html.div.Attrs.align, u"left"
	yield check, [node[0]], u"align", u"right", u"center", u"left"
	yield check, [], u"align", u"right", u"center"
	yield check, [], u"align", u"right"
	yield check, [], u"gurk", u"hurz"


def test_attrcontains():
	node = xfindnode()

	def check(expected, attrname, *attrvalues):
		for selector in (xfind.attrcontains, xfind.attrcontains_xml):
			got = list(node.walknodes(selector(attrname, *attrvalues)))
			assert len(got) == len(expected)
			for (gotnode, expectednode) in zip(got, expected):
				assert gotnode is expectednode

	yield check, [node[0]], u"align", u"ef"
	yield check, [node[0]], html.div.Attrs.align, u"ef"
	yield check, [node[0]], u"align", u"ri", u"ef"
	yield check, [], u"align", u"ri", u"en"
	yield check, [], u"align", u"x"
	yield check, [], u"gurk", u"",


def test_attrstartswith():
	node = xfindnode()

	def check(expected, attrname, *attrvalues):
		for selector in (xfind.attrstartswith, xfind.attrstartswith_xml):
			got = list(node.walknodes(selector(attrname, *attrvalues)))
			assert len(got) == len(expected)
			for (gotnode, expectednode) in zip(got, expected):
				assert gotnode is expectednode

	yield check, [node[0]], u"align", u"le"
	yield check, [node[0]], html.div.Attrs.align, u"le"
	yield check, [node[0]], u"align", u"ri", u"ce", u"le"
	yield check, [], u"align", u"ri", u"ce"
	yield check, [], u"align", u"eft"
	yield check, [], u"gurk", u""
	yield check, [node[1][0][1]], u"src", u"root:"


def test_attrendswith():
	node = xfindnode()

	def check(expected, attrname, *attrvalues):
		for selector in (xfind.attrendswith, xfind.attrendswith_xml):
			got = list(node.walknodes(selector(attrname, *attrvalues)))
			assert len(got) == len(expected)
			for (gotnode, expectednode) in zip(got, expected):
				assert gotnode is expectednode

	yield check, [node[0]], u"align", u"ft"
	yield check, [node[0]], html.div.Attrs.align, u"ft"
	yield check, [node[0]], u"align", u"ht", u"er", u"ft"
	yield check, [], u"align", u"ht", u"er"
	yield check, [], u"align", u"lef"
	yield check, [], u"gurk", u""
	yield check, [node[1][0][1]], u"src", u".gif"


def test_hasid():
	node = xfindnode()
	res = list(node.walknodes(xfind.hasid("id42")))
	assert len(res) == 1
	assert res[0] is node[1][2]


def test_hasclass():
	node = xfindnode()
	res = list(node.walknodes(xfind.hasclass("foo")))
	assert len(res) == 1
	assert res[0] is node[1]


def test_frag():
	e = parse.tree(b"das ist <b>klaus</b>. das ist <b>erich</b>", parse.SGMLOP(), parse.NS(html), parse.Node())
	assert u"".join(map(unicode, e.walknodes(e//html.b))) == u"klauserich"


def test_multiall():
	def check(node, expr, ids):
		assert u"".join(unicode(e.attrs.id) for e in node.walknodes(expr)) == ids

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
	check(ds[0], ds[0]//html.div//html.div, u"37849a5bc6de")


def test_itemsslices():
	def check(node, expr, ids):
		assert u"".join(unicode(e.attrs.id) for e in node.walknodes(expr)) == ids

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
		(ds[0]/html.div[0]/html.div[-1], u"5"),
		(ds[0]/html.div/html.div[-1], u"567"),
		(ds[0]/html.div[-1]/html.div, u"67"),
		(ds[0]/html.div/html.div, u"455667"), # we get 5 and 6 twice
		#(ds[0]/(html.div/html.div) & xfind.nthchild(2), u"5"), # we get 5 and 6 twice
		#(ds[0]/html.div[:]/html.div[:], u"455667"),
		(ds[0]/html.div/html.p[0], u""),
		(ds[0]/html.p[0]/html.p[0], u""),
		(ds[0]//html.div, u"145256367"),
	]
	for (got, exp) in tests:
		yield check, ds[0], got, exp


def test_item():
	e = html.div(xrange(10))
	assert unicode(e[xsc.Text][0]) == u"0"
	assert unicode(e[xsc.Text][9]) == u"9"
	assert unicode(e[xsc.Text][-1]) == u"9"
	assert unicode(e[xsc.Text][-10]) == u"0"
	with py.test.raises(IndexError):
		e[xsc.Text][10]
	with py.test.raises(IndexError):
		e[xsc.Text][-11]
	assert unicode(misc.item(e[xsc.Text], 10, u"x")) == u"x"
	assert unicode(misc.item(e[xsc.Text], -11, u"x")) == u"x"
