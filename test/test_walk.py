#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

import py.test

from ll.xist import xsc
from ll.xist.ns import html, xml

import common


def test_walk_1():
	node = common.createfrag()
	def filter(*args):
		return (True, xsc.enterattrs, xsc.entercontent, True)

	def check(inmode, outmode):
		# call only for code coverage
		list(node.walk((True, xsc.entercontent, True), inmode=inmode, outmode=outmode))
		list(node.walk(filter, inmode=inmode, outmode=outmode))

	modes = (xsc.walknode, xsc.walkpath, xsc.walkindex, xsc.walkrootindex)
	for inmode in modes:
		for outmode in modes:
			yield check, inmode, outmode


def test_walk_2():
	def check(node, filter, result, inmode=xsc.walknode, outmode=xsc.walknode):
		def node2str(node):
			if isinstance(node, xsc.Node):
				if isinstance(node, xsc.Text):
					return "#"
				else:
					return node.xmlname
			else:
				return ".".join(map(node2str, node))
	
		assert map(node2str, node.walk(filter, inmode=inmode, outmode=outmode)) == result

	node = html.div(
		html.tr(
			html.th("gurk"),
			html.td("hurz"),
			id=html.b(42)
		),
		class_=html.i("hinz")
	)

	def filtertopdown(node):
		return (isinstance(node, xsc.Element), xsc.entercontent)
	def filterbottomup(node):
		return (xsc.entercontent, isinstance(node, xsc.Element))
	def filtertopdownattrs(node):
		return (isinstance(node, xsc.Element), xsc.enterattrs, xsc.entercontent)
	def filterbottomupattrs(node):
		return (xsc.enterattrs, xsc.entercontent, isinstance(node, xsc.Element))
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

	def filtertopdownattrwithoutcontent(node):
		if isinstance(node, xsc.Element):
			return (True, xsc.entercontent, xsc.enterattrs)
		elif isinstance(node, (xsc.Attr, xsc.Text)):
			return (True, )
		else:
			return (xsc.entercontent, )

	yield check, node, filtertopdown, ["div", "tr", "th", "td"]
	yield check, node, filterbottomup, ["th", "td", "tr", "div"]
	yield check, node, filtertopdownattrs, ["div", "i", "tr", "b", "th", "td"]
	yield check, node, filtertopdownattrs, ["div", "div.class.i", "div.tr", "div.tr.id.b", "div.tr.th", "div.tr.td"], xsc.walknode, xsc.walkpath
	yield check, node, filterbottomupattrs, ["div.class.i", "div.tr.id.b", "div.tr.th", "div.tr.td", "div.tr", "div"], xsc.walknode, xsc.walkpath
	yield check, node, filtertopdowntextonlyinattr, ["div", "div.class.i", "div.class.i.#", "div.tr", "div.tr.id.b", "div.tr.id.b.#", "div.tr.th", "div.tr.td"], xsc.walkpath, xsc.walkpath
	yield check, node, filtertopdownattrwithoutcontent, ["div", "div.tr", "div.tr.th", "div.tr.th.#", "div.tr.td", "div.tr.td.#", "div.tr.id", "div.class"], xsc.walknode, xsc.walkpath


def test_walk_walkindex():
	e = html.div(
		"foo",
		html.a(
			"bar",
			xml.Attrs(lang="en"),
			href="baz",
		),
		"gurk",
	)
	res = list(e.walk(xsc.FindTypeAllAttrs(xsc.Text), outmode=xsc.walkindex))
	exp = [
		[0],
		[1, 0],
		[1, "href", 0],
		[1, (xml, "lang"), 0], # FIXME: This depends on dictionary iteration order
		[2]
	]
	assert res == exp


def test_walk_walkindexisnode():
	# Check that all walk modes return the same data
	def check(node):
		l1 = list(node.walk(xsc.FindTypeAllAttrs(xsc.Text), outmode=xsc.walknode))
		l2 = list(node.walk(xsc.FindTypeAllAttrs(xsc.Text), outmode=xsc.walkpath))
		l3 = list(node.walk(xsc.FindTypeAllAttrs(xsc.Text), outmode=xsc.walkindex))
		l4 = list(node.walk(xsc.FindTypeAllAttrs(xsc.Text), outmode=xsc.walkrootindex))
		assert len(l1) == len(l2) == len(l3) == len(l4)
		for (subnode, path, index, (root, rindex)) in zip(l1, l2, l3, l4):
			assert subnode is path[-1]
			assert subnode is node[index]
			assert subnode is root[rindex]

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
	assert str(e.walk(isdiv)[0]) == "123"
	assert str(e.walk(isdiv)[-1]) == "3"
	py.test.raises(IndexError, e.walk(isdiv).__getitem__, 3)
	py.test.raises(IndexError, e.walk(isdiv).__getitem__, -4)
