#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license

import py.test

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
			return u".".join(u"#" if isinstance(node, xsc.Text) else node.xmlname for node in path)

		assert map(path2str, node.walkpaths(filter)) == result

	node = html.div(
		html.tr(
			html.th(u"gurk"),
			html.td(u"hurz"),
			id=html.b(42)
		),
		class_=html.i(u"hinz")
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

	yield check, node, filtertopdown, [u"div", u"div.tr", u"div.tr.th", u"div.tr.td"]
	yield check, node, filterbottomup, [u"div.tr.th", u"div.tr.td", u"div.tr", u"div"]
	yield check, node, filtertopdownattrs, [u"div", u"div.class.i", u"div.tr", u"div.tr.id.b", u"div.tr.th", u"div.tr.td"]
	yield check, node, filterbottomupattrs, [u"div.class.i", u"div.tr.id.b", u"div.tr.th", u"div.tr.td", u"div.tr", u"div"]
	yield check, node, filtertopdowntextonlyinattr, [u"div", u"div.class.i", u"div.class.i.#", u"div.tr", u"div.tr.id.b", u"div.tr.id.b.#", u"div.tr.th", u"div.tr.td"]
	yield check, node, filtertopdownattrwithoutcontent, [u"div", u"div.tr", u"div.tr.th", u"div.tr.th.#", u"div.tr.td", u"div.tr.td.#", u"div.tr.id", u"div.class"]


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
	assert unicode(e.walknodes(isdiv)[0]) == u"123"
	assert unicode(e.walknodes(isdiv)[-1]) == u"3"
	with py.test.raises(IndexError):
		e.walknodes(isdiv)[3]
	with py.test.raises(IndexError):
		e.walknodes(isdiv)[-4]
	assert unicode(e.walkpaths(isdiv)[0][-1]) == u"123"
	assert unicode(e.walkpaths(isdiv)[-1][-1]) == u"3"
	with py.test.raises(IndexError):
		e.walkpaths(isdiv)[3]
	with py.test.raises(IndexError):
		e.walkpaths(isdiv)[-4]
