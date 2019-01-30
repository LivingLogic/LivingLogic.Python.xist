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
from ll.xist import xsc, xfind
from ll.xist.ns import html, xml

import xist_common as common


node = html.div(
	html.tr(
		html.th("gurk"),
		html.td("hurz"),
		id=html.b(42)
	),
	class_=html.i("hinz")
)


def path2str(path):
	return ".".join("#" if isinstance(node, xsc.Text) else node.xmlname for node in path)


def iterpath2str(iter):
	return [path2str(s) for s in iter]


def test_walk_coverage():
	node = common.createfrag()

	# call only for code coverage
	for c in node.walk(entercontent=True, enterattrs=True, enterattr=True, enterelementnode=True, leaveelementnode=True, enterattrnode=True, leaveattrnode=True):
		pass


def test_walkpaths_topdown():
	# Elements top down
	assert ["div", "div.tr", "div.tr.th", "div.tr.td"] == iterpath2str(node.walkpaths(xsc.Element))


def test_walkpaths_bottomup():
	# Elements bottom up
	assert ["div.tr.th", "div.tr.td", "div.tr", "div"] == iterpath2str(node.walkpaths(xsc.Element, enterelementnode=False, leaveelementnode=True))


def test_walkpaths_topdown_attributes():
	# Elements top down (including elements in attributes)
	assert ["div", "div.class.i", "div.tr", "div.tr.id.b", "div.tr.th", "div.tr.td"] == iterpath2str(node.walkpaths(xsc.Element, enterattrs=True, enterattr=True))


def test_walkpaths_bottomup_attributes():
	# Elements bottom up (including elements in attributes)
	assert ["div.class.i", "div.tr.id.b", "div.tr.th", "div.tr.td", "div.tr", "div"] == iterpath2str(node.walkpaths(xsc.Element, enterattrs=True, enterattr=True, enterelementnode=False, leaveelementnode=True))


def test_walkpaths_topdown_all():
	# Elements, attributes and texts top down (including elements in attributes)
	assert ["div", "div.class", "div.tr", "div.tr.id", "div.tr.th", "div.tr.th.#", "div.tr.td", "div.tr.td.#"] == iterpath2str(node.walkpaths(xsc.Element, xsc.Attr, xsc.Text, enterattrs=True))


def test_walkpaths_topdown_textonlyinattr():
	# Elements, attributes and texts top down (including elements in attributes, but text only if it is inside attributes)
	def textonlyinattr(path):
		node = path[-1]
		if isinstance(node, xsc.Element):
			return True
		if isinstance(node, xsc.Text) and any(isinstance(node, xsc.Attr) for node in path):
			return True
		else:
			return False

	assert ["div", "div.class.i", "div.class.i.#", "div.tr", "div.tr.id.b", "div.tr.id.b.#", "div.tr.th", "div.tr.td"] == iterpath2str(node.walkpaths(textonlyinattr, enterattrs=True, enterattr=True))


def test_walk_cursor():
	nodes = []
	for c in node.walk(xsc.Element):
		if isinstance(c.node, html.tr):
			c.entercontent = False # Don't enter the ``tr`` element
		nodes.append(c.path[:])
	assert ["div", "div.tr"] == iterpath2str(nodes)


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
	isdiv = xfind.selector(html.div)

	# Test ``walknodes``
	assert str(misc.first(e.walknodes(isdiv))) == "123"
	assert str(misc.last(e.walknodes(isdiv))) == "3"
	misc.item(e.walknodes(isdiv), 3) is None
	misc.item(e.walknodes(isdiv), -4) is None

	# Test ``walkpaths``
	assert str(misc.item(e.walkpaths(isdiv), (0, -1))) == "123"
	assert str(misc.item(e.walkpaths(isdiv), (-1, -1))) == "3"
	misc.item(e.walkpaths(isdiv), 3) is None
	misc.item(e.walkpaths(isdiv), -4) is None
