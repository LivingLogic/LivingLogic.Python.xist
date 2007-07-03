#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


from __future__ import with_statement

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
		assert res[2] is node[1][-1][0]

	yield check, list(node.walknode(xfind.isinstance(html.h1, html.h2)))
	yield check, list(node.walknode(xfind.isinstance(html.h1) | html.h2))
	yield check, list(node.walknode(html.h1 | xfind.isinstance(html.h2)))
	yield check, list(node.walknode(html.h1 | html.h2))
	yield check, list(node.walknode(xsc.Element & ~xfind.isinstance(xsc.Text, html.p, html.div, html.em)))


def test_hasname():
	node = xfindnode()

	def check(expr, res):
		assert [str(e) for e in node.walknode(expr)] == res
	yield check, xfind.hasname("em"), ["important", "first", "second", "important", "first", "important", "second", "important"]
	yield check, xfind.hasname_xml("em"), ["important", "first", "second", "important", "first", "important", "second", "important"]


def test_is():
	node = xfindnode()

	# Frags are invisible in the path
	res = list(node.walknode(node))
	assert len(res) == 0

	res = list(node[0].walknode(node[0]))
	assert len(res) == 1
	assert res[0] is node[0]


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


def test_hasattr():
	# hasattr
	node = xfindnode()
	res = list(node.walknode(node//xfind.hasattr("class_")))
	assert len(res) == 1
	assert res[0] is node[1]

	res = list(node.walknode(node//xfind.hasattr(html.div.Attrs.id, html.div.Attrs.align)))
	assert len(res) == 2
	assert res[0] is node[0]
	assert res[1] is node[1][-1]

	# hasattr_xml
	res = list(node.walknode(node//xfind.hasattr_xml("class")))
	assert len(res) == 1
	assert res[0] is node[1]

	res = list(node.walknode(node//xfind.hasattr_xml(html.div.Attrs.id, html.div.Attrs.align)))
	assert len(res) == 2
	assert res[0] is node[0]
	assert res[1] is node[1][-1]


def test_hasid():
	node = xfindnode()
	res = list(node.walknode(node//xfind.hasid("id42")))
	assert len(res) == 1
	assert res[0] is node[1][-1]


def test_hasclass():
	node = xfindnode()
	res = list(node.walknode(node//xfind.hasclass("foo")))
	assert len(res) == 1
	assert res[0] is node[1]


def test_frag():
	e = parsers.parseString("das ist <b>klaus</b>. das ist <b>erich</b>", prefixes={None: html})
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
		(ds[0]/(html.div & xfind.nthchild(0))/(html.div & xfind.nthchild(-1)), "5"),
		(ds[0]/html.div/(html.div & xfind.nthchild(-1)), "567"),
		(ds[0]/(html.div & xfind.nthchild(-1))/html.div, "67"),
		(ds[0]/(html.div/html.div), "455667"), # we get 5 and 6 twice
		(ds[0]/(html.div/html.div) & xfind.nthchild(2), "5"), # we get 5 and 6 twice
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
		yield check, node, got, exp


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


def test_css():
	with html.div(id=1) as e:
		with html.ul(id=2):
			+html.li("foo")
			+html.li()

	assert list(e.walknode(xfind.css("div"))) == [e]
	assert list(e.walknode(xfind.css("li"))) == [e[0][0], e[0][1]]
	assert list(e.walknode(xfind.css("div#1"))) == [e]
	assert list(e.walknode(xfind.css("#2"))) == [e[0]]
	assert list(e.walknode(xfind.css(":empty"))) == [e[0][1]]
	assert list(e.walknode(xfind.css("li:empty"))) == [e[0][1]]
	assert list(e.walknode(xfind.css("div :empty"))) == [e[0][1]]
	assert list(e.walknode(xfind.css("div>*:empty"))) == []
	assert list(e.walknode(xfind.css("div>:empty"))) == []
	assert list(e.walknode(xfind.css("li+li"))) == [e[0][1]]
