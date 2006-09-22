#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2006 by Walter Dörwald
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
	for cursor in node.walk((True, xsc.entercontent, True)):
		pass
	for cursor in node.walk(filter):
		pass


def test_walk_result():
	def check(node, filter, result):
		def node2str(node):
			if isinstance(node, xsc.Text):
				return "#"
			else:
				return node.xmlname
		def path2str(cursor):
			return ".".join(map(node2str, cursor.path))

		assert map(path2str, node.walk(filter)) == result

	node = html.div(
		html.tr(
			html.th("gurk"),
			html.td("hurz"),
			id=html.b(42)
		),
		class_=html.i("hinz")
	)

	def filtertopdown(cursor):
		return (isinstance(cursor.node, xsc.Element), xsc.entercontent)
	def filterbottomup(cursor):
		return (xsc.entercontent, isinstance(cursor.node, xsc.Element))
	def filtertopdownattrs(cursor):
		return (isinstance(cursor.node, xsc.Element), xsc.enterattrs, xsc.entercontent)
	def filterbottomupattrs(cursor):
		return (xsc.enterattrs, xsc.entercontent, isinstance(cursor.node, xsc.Element))
	def filtertopdowntextonlyinattr(cursor):
		for node in cursor.path:
			if isinstance(node, xsc.Attr):
				inattr = True
				break
		else:
			inattr = False
		node = cursor.path[-1]
		if isinstance(cursor.node, xsc.Element):
			return (True, xsc.enterattrs, xsc.entercontent)
		if inattr and isinstance(cursor.node, xsc.Text):
			return (True, )
		else:
			return (xsc.entercontent, )

	def filtertopdownattrwithoutcontent(cursor):
		if isinstance(cursor.node, xsc.Element):
			return (True, xsc.entercontent, xsc.enterattrs)
		elif isinstance(cursor.node, (xsc.Attr, xsc.Text)):
			return (True, )
		else:
			return (xsc.entercontent, )

	yield check, node, filtertopdown, ["div", "div.tr", "div.tr.th", "div.tr.td"]
	yield check, node, filterbottomup, ["div.tr.th", "div.tr.td", "div.tr", "div"]
	yield check, node, filtertopdownattrs, ["div", "div.class.i", "div.tr", "div.tr.id.b", "div.tr.th", "div.tr.td"]
	yield check, node, filterbottomupattrs, ["div.class.i", "div.tr.id.b", "div.tr.th", "div.tr.td", "div.tr", "div"]
	yield check, node, filtertopdowntextonlyinattr, ["div", "div.class.i", "div.class.i.#", "div.tr", "div.tr.id.b", "div.tr.id.b.#", "div.tr.th", "div.tr.td"]
	yield check, node, filtertopdownattrwithoutcontent, ["div", "div.tr", "div.tr.th", "div.tr.th.#", "div.tr.td", "div.tr.td.#", "div.tr.id", "div.class"]


def test_walkindex():
	e = html.div(
		"foo",
		html.a(
			"bar",
			xml.Attrs(lang="en"),
			href="baz",
		),
		"gurk",
	)
	res = list(e.walkindex(xsc.FindTypeAllAttrs(xsc.Text)))
	exp = [
		[0],
		[1, 0],
		[1, "href", 0],
		[1, (xml, "lang"), 0], # FIXME: This depends on dictionary iteration order
		[2]
	]
	assert res == exp


def test_cursor():
	# Check that all cursor attributes point to the same nodes
	def check(node):
		for cursor in node.walk(xsc.FindTypeAllAttrs(xsc.Text)):
			assert cursor.node is cursor.path[-1]
			assert cursor.node is cursor.root[cursor.index]

	for node in common.allnodes():
		yield check, node


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
	assert str(e.walk(isdiv)[0].node) == "123"
	assert str(e.walk(isdiv)[-1].node) == "3"
	py.test.raises(IndexError, e.walk(isdiv).__getitem__, 3)
	py.test.raises(IndexError, e.walk(isdiv).__getitem__, -4)
