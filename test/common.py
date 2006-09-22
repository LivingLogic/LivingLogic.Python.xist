#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2006 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


from ll import url
from ll.xist import xsc
from ll.xist.ns import html, xml, specials, abbr


def createattr():
	return html.span.Attrs.lang(
		True,
		False,
		url.URL("http://www.python.org/"),
		html.abbr(
			xml.XML10(),
			"hurz",
			specials.tab(),
			abbr.xist(),
			None,
			1,
			2.0,
			"3",
			u"4",
			(5, 6),
			[7, 8],
			html.span("gurk"),
			title="hurz"
		)
	)


def createattrs():
	return html.span.Attrs(
		lang=(
			True,
			False,
			url.URL("http://www.python.org/"),
			html.abbr(
				xml.XML10(),
				"hurz",
				specials.tab(),
				abbr.xist(),
				None,
				1,
				2.0,
				"3",
				u"4",
				(5, 6),
				[7, 8],
				html.span("gurk"),
				title="hurz"
			)
		)
	)


def createelement():
	return html.span(
		1,
		2,
		class_="gurk",
		id=(1, 2, (3, 4)),
		lang=(
			True,
			False,
			url.URL("http://www.python.org/"),
			html.abbr(
				xml.XML10(),
				"hurz",
				specials.tab(),
				abbr.xist(),
				None,
				1,
				2.0,
				"3",
				u"4",
				(5, 6),
				[7, 8],
				html.span("gurk"),
				title="hurz"
			)
		)
	)


def createfrag():
	return xsc.Frag(
		xml.XML10(),
		html.DocTypeHTML401transitional(),
		xsc.Comment("gurk"),
		"hurz",
		specials.tab(),
		abbr.xist(),
		None,
		True,
		False,
		1,
		2.0,
		"3",
		u"4",
		(5, 6),
		[7, 8],
		html.div(
			align="left"
		),
		url.URL("http://www.python.org/"),
		html.span(
			1,
			2,
			class_="gurk",
			id=(1, 2, (3, 4)),
			lang=(
				True,
				False,
				url.URL("http://www.python.org/"),
				html.abbr(
					xml.XML10(),
					"hurz",
					specials.tab(),
					abbr.xist(),
					None,
					1,
					2.0,
					"3",
					u"4",
					(5, 6),
					[7, 8],
					html.span("gurk"),
					title="hurz"
				)
			)
		)
	)


def allnodes():
	return (xsc.Null, createattr(), createattrs(), createelement(), createfrag())
