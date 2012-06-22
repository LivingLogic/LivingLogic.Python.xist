#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2012 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license

import pytest

from ll.xist import xsc, xfind
from ll.xist.ns import html, xml

import xist_common as common


def test_walk_coverage():
	node = common.createfrag()
	class Filter(xfind.WalkFilter):
		def filternode(self, node):
			return (True, xfind.enterattrs, xfind.entercontent, True)

	# call only for code coverage
	for path in node.walk(Filter()):
		pass


def test_walk_result():
	def check(node, filter, result):
		filter = filter()
		def path2str(path):
			return ".".join("#" if isinstance(node, xsc.Text) else node.xmlname for node in path)

		assert [path2str(s) for s in node.walkpaths(filter)] == result

	node = html.div(
		html.tr(
			html.th("gurk"),
			html.td("hurz"),
			id=html.b(42)
		),
		class_=html.i("hinz")
	)

	class filtertopdown(xfind.WalkFilter):
		def filternode(self, node):
			return (isinstance(node, xsc.Element), xfind.entercontent)

	class filterbottomup(xfind.WalkFilter):
		def filternode(self, node):
			return (xfind.entercontent, isinstance(node, xsc.Element))

	class filtertopdownattrs(xfind.WalkFilter):
		def filternode(self, node):
			return (isinstance(node, xsc.Element), xfind.enterattrs, xfind.entercontent)

	class filterbottomupattrs(xfind.WalkFilter):
		def filternode(self, node):
			return (xfind.enterattrs, xfind.entercontent, isinstance(node, xsc.Element))

	class filtertopdowntextonlyinattr(xfind.WalkFilter):
		def filterpath(self, path):
			for node in path:
				if isinstance(node, xsc.Attr):
					inattr = True
					break
			else:
				inattr = False
			node = path[-1]
			if isinstance(node, xsc.Element):
				return (True, xfind.enterattrs, xfind.entercontent)
			if inattr and isinstance(node, xsc.Text):
				return (True, )
			else:
				return (xfind.entercontent, )

	class filtertopdownattrwithoutcontent(xfind.WalkFilter):
		def filternode(self, node):
			if isinstance(node, xsc.Element):
				return (True, xfind.entercontent, xfind.enterattrs)
			elif isinstance(node, (xsc.Attr, xsc.Text)):
				return (True, )
			else:
				return (xfind.entercontent, )

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
	isdiv = xfind.FindTypeAll(html.div)
	assert str(e.walknodes(isdiv)[0]) == "123"
	assert str(e.walknodes(isdiv)[-1]) == "3"
	with pytest.raises(IndexError):
		e.walknodes(isdiv)[3]
	with pytest.raises(IndexError):
		e.walknodes(isdiv)[-4]
	assert str(e.walkpaths(isdiv)[0][-1]) == "123"
	assert str(e.walkpaths(isdiv)[-1][-1]) == "3"
	with pytest.raises(IndexError):
		e.walkpaths(isdiv)[3]
	with pytest.raises(IndexError):
		e.walkpaths(isdiv)[-4]
