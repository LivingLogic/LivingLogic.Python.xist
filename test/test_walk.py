#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

import py.test

from ll.xist import xsc
from ll.xist.ns import html, xml

import common


def test_walk_coverage():
	node = common.createfrag()
	def filter(*args):
		return (True, xsc.enterattrs, xsc.entercontent, True)

	# call only for code coverage
	for path in node.walk((True, xsc.entercontent, True)):
		pass
	for path in node.walk(filter):
		pass


def test_walk_result():
	def check(node, filter, result):
		def node2str(node):
			if isinstance(node, xsc.Text):
				return "#"
			else:
				return node.xmlname
		def path2str(path):
			return ".".join(map(node2str, path))

		assert map(path2str, node.walk(filter)) == result

	node = html.div(
		html.tr(
			html.th("gurk"),
			html.td("hurz"),
			id=html.b(42)
		),
		class_=html.i("hinz")
	)

	def filtertopdown(path):
		return (isinstance(path[-1], xsc.Element), xsc.entercontent)
	def filterbottomup(path):
		return (xsc.entercontent, isinstance(path[-1], xsc.Element))
	def filtertopdownattrs(path):
		return (isinstance(path[-1], xsc.Element), xsc.enterattrs, xsc.entercontent)
	def filterbottomupattrs(path):
		return (xsc.enterattrs, xsc.entercontent, isinstance(path[-1], xsc.Element))
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

	def filtertopdownattrwithoutcontent(path):
		if isinstance(path[-1], xsc.Element):
			return (True, xsc.entercontent, xsc.enterattrs)
		elif isinstance(path[-1], (xsc.Attr, xsc.Text)):
			return (True, )
		else:
			return (xsc.entercontent, )

	yield check, node, filtertopdown, ["div", "div.tr", "div.tr.th", "div.tr.td"]
	yield check, node, filterbottomup, ["div.tr.th", "div.tr.td", "div.tr", "div"]
	yield check, node, filtertopdownattrs, ["div", "div.class.i", "div.tr", "div.tr.id.b", "div.tr.th", "div.tr.td"]
	yield check, node, filterbottomupattrs, ["div.class.i", "div.tr.id.b", "div.tr.th", "div.tr.td", "div.tr", "div"]
	yield check, node, filtertopdowntextonlyinattr, ["div", "div.class.i", "div.class.i.#", "div.tr", "div.tr.id.b", "div.tr.id.b.#", "div.tr.th", "div.tr.td"]
	yield check, node, filtertopdownattrwithoutcontent, ["div", "div.tr", "div.tr.th", "div.tr.th.#", "div.tr.td", "div.tr.td.#", "div.tr.id", "div.class"]


def test_walkgetitem():
	e = html.div(
		1,
		html.div(
			2,
			html.div(
				3
			)
		)
	)
	isdiv = xsc.FindTypeAll(html.div)
	assert str(e.walknode(isdiv)[0]) == "123"
	assert str(e.walknode(isdiv)[-1]) == "3"
	py.test.raises(IndexError, e.walknode(isdiv).__getitem__, 3)
	py.test.raises(IndexError, e.walknode(isdiv).__getitem__, -4)
	assert str(e.walkpath(isdiv)[0][-1]) == "123"
	assert str(e.walkpath(isdiv)[-1][-1]) == "3"
	py.test.raises(IndexError, e.walkpath(isdiv).__getitem__, 3)
	py.test.raises(IndexError, e.walkpath(isdiv).__getitem__, -4)
