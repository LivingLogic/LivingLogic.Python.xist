#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


import py.test

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


def test_levels():
	def check(expr, ids):
		assert "".join(str(e["id"]) for e in expr) == ids

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
		(ds[0]//html.div, "1234567"),
		(ds[0]/html.div, "123"),
		(ds[0]/html.div/html.div, "4567"),
		(ds[0]/html.div/html.div/html.div, ""),
		(ds[0]//xfind.contains(html.div), "012"),
	]
	for (got, exp) in tests:
		yield check, got, exp


def test_hasattr():
	node = xfindnode()
	res = list(node//xfind.hasattr(html.div.Attrs.id, html.div.Attrs.align))
	assert len(res) == 2
	assert res[0] is node[0]
	assert res[1] is node[1][-1]


def test_hasattrnamed():
	node = xfindnode()
	res = list(node//xfind.hasattrnamed("class_"))
	assert len(res) == 1
	assert res[0] is node[1]

	res = list(node//xfind.hasattrnamed("class", xml=True))
	assert len(res) == 1
	assert res[0] is node[1]


def test_is():
	node = xfindnode()
	res = list(node//xfind.is_(html.h1, html.h2))
	assert len(res) == 3
	assert res[0] is node[0][0]
	assert res[1] is node[1][0]
	assert res[2] is node[1][-1][0]

	res = list(node//html.h1/xfind.is_(html.h1, html.h2))
	assert len(res) == 2
	assert res[0] is node[0][0]
	assert res[1] is node[1][0]


def test_isnot():
	node = xfindnode()
	res = list(node//xfind.isnot(xsc.Text, html.p, html.div, html.em))
	assert len(res) == 3
	assert res[0] is node[0][0]
	assert res[1] is node[1][0]
	assert res[2] is node[1][-1][0]


def test_contains():
	node = xfindnode()
	res = list(node//xfind.is_(html.h1, html.h2)/xfind.contains(html.em))
	assert len(res) == 2
	assert res[0] is node[0][0]
	assert res[1] is node[1][-1][0]


def test_child():
	node = xfindnode()
	res = list(node//html.h1/xfind.child(html.em))
	assert len(res) == 1
	assert res[0] is node[0][0][1]


def test_attr():
	node = xfindnode()
	res = list(node//xfind.attr(html.div.Attrs.id, html.div.Attrs.align))
	assert len(res) == 2
	assert res[0] is node[0]["align"]
	assert res[1] is node[1][-1]["id"]


def test_attrnamed():
	node = xfindnode()
	res = list(node//xfind.attrnamed("class_"))
	assert len(res) == 1
	assert res[0] is node[1]["class_"]

	res = list(node//xfind.attrnamed("class", xml=True))
	assert len(res) == 1
	assert res[0] is node[1]["class_"]


def test_frag():
	e = parsers.parseString("das ist <b>klaus</b>. das ist <b>erich</b>", prefixes=xsc.Prefixes(html))
	# The following won't generate any nodes, because e/xfind.all iterates all
	# nodes in the tree (but not the Frag root) and ../html.b filters the bold
	# *children*, but there are none.
	assert u"".join(map(unicode, e//html.b)) == u""
	# The following *will* produce these nodes
	assert u"".join(map(unicode, e//xfind.is_(html.b))) == u"klauserich"


def test_multiall():
	def check(expr, ids):
		assert "".join(str(e["id"]) for e in expr) == ids

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
	check(ds[0]//html.div//html.div, "34789a56bcde789abcde")


def test_itemsslices():
	def check(expr, ids):
		assert "".join(str(e["id"]) for e in expr) == ids

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
		(ds[0]/(html.div/html.div), "455667"), # we get 5 and 6 twice
		(ds[0]/(html.div/html.div)[2], "5"), # we get 5 and 6 twice
		(ds[0]/html.div[:]/html.div[:], "455667"),
		(ds[0]/html.div/html.p[0], ""),
		(ds[0]/html.p[0]/html.p[0], ""),
	
		# The following might be a surprise, but is perfectly normal:
		# each node is visited and the div children are yielded.
		# div(id=0) does have div children and those will be yielded.
		# This is why the sequence starts with "12" and not "14"
		(ds[0]//html.div, "123455667"),
	
		(ds[0]/html.div[1:2], "2"),
		(ds[0]/html.div[1:-1]/html.div[1:-1], ""),
		(ds[0]/html.div[1:-1]/html.div[-1:], "6"),
	]
	for (got, exp) in tests:
		yield check, got, exp


def test_item():
	e = html.div(xrange(10))
	assert str(e[xsc.Text][0]) == "0"
	assert str(e[xsc.Text][9]) == "9"
	assert str(e[xsc.Text][-1]) == "9"
	assert str(e[xsc.Text][-10]) == "0"
	py.test.raises(IndexError, e[xsc.Text].__getitem__, 10)
	py.test.raises(IndexError, e[xsc.Text].__getitem__, -11)
	assert str(xfind.item(e[xsc.Text], 10, "x")) == "x"
	assert str(xfind.item(e[xsc.Text], -11, "x")) == "x"
