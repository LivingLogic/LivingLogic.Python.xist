#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; module that contains elements that simplify
handling meta data. All elements in this module will generate a
<pyref module="ll.xist.ns.html" class="meta"><class>html.meta</class></pyref>
element when converted.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc, sims
from ll.xist.ns import ihtml, html


class contenttype(html.meta):
	"""
	<par>can be used for a <markup>&lt;meta http-equiv="Content-Type" content="text/html"/&gt;</markup>, where
	the character set will be automatically inserted on a call to
	<pyref module="ll.xist.xsc" class="Node" method="publish"><method>publish</method></pyref>.</par>

	<par>Usage is simple: <markup>&lt;meta:contenttype/&gt;</markup></par>
	"""
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None
		class mimetype(xsc.TextAttr): default = u"text/html"

	def convert(self, converter):
		target = converter.target
		if issubclass(target, ihtml) or issubclass(target, html):
			e = target.meta(
				self.attrs.without([u"mimetype"]),
				http_equiv=u"Content-Type",
				content=self[u"mimetype"],
			)
		else:
			raise ValueError("unknown conversion target %r" % target)
		return e.convert(converter)

	def publish(self, publisher):
		# fall back to the Element method
		xsc.Element.publish(self, publisher)


class contentscripttype(html.meta):
	"""
	<par>can be used for a <markup>&lt;meta http-equiv="Content-Script-Type" content="..."/&gt;</markup>.</par>

	<par>Usage is simple: <markup>&lt;meta:contentscripttype type="text/javascript"/&gt;</markup></par>
	"""
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None
		class type(xsc.TextAttr): pass

	def convert(self, converter):
		attrs = self.attrs.copy()
		del attrs[u"type"]
		e = html.meta(attrs)
		e[u"http_equiv"] = u"Content-Script-Type"
		e[u"content"] = self[u"type"]
		return e.convert(converter)


class keywords(html.meta):
	"""
	<par>can be used for a <markup>&lt;meta name="keywords" content="..."/&gt;</markup>.</par>

	<par>Usage is simple: <markup>&lt;meta:keywords&gt;foo, bar&lt;/meta:keywords&gt;</markup></par>
	"""
	model = sims.NoElements()
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None

	def convert(self, converter):
		e = html.meta(self.attrs)
		e[u"name"] = u"keywords"
		e[u"content"] = self.content
		return e.convert(converter)


class description(html.meta):
	"""
	<par>can be used for a <markup>&lt;meta name="description" content="..."/&gt;</markup>.</par>

	<par>Usage is simple: <markup>&lt;meta:description&gt;This page describes the ...&lt;/meta:description&gt;</markup></par>
	"""
	model = sims.NoElements()
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None

	def convert(self, converter):
		e = html.meta(self.attrs)
		e[u"name"] = u"description"
		e[u"content"] = self.content
		return e.convert(converter)


class stylesheet(html.link):
	"""
	<par>can be used for a <markup>&lt;link rel="stylesheet" type="text/css" href="..."/&gt;</markup>.</par>

	<par>Usage is simple: <markup>&lt;meta:stylesheet href="root:stylesheets/main.css"/&gt;</markup></par>
	"""
	class Attrs(html.link.Attrs):
		rel = None
		type = None

	def convert(self, converter):
		e = html.link(self.attrs, rel=u"stylesheet", type=u"text/css")
		return e.convert(converter)


class made(html.link):
	"""
	<par>can be used for a <markup>&lt;link rel="made" href="mailto:..."/&gt;</markup>.</par>

	<par>Usage is simple: <markup>&lt;meta:made href="foobert@bar.org"/&gt;</markup>.</par>
	"""
	class Attrs(html.link.Attrs):
		rel = None

	def convert(self, converter):
		e = html.link(self.attrs, rel=u"made", href=(u"mailto:", self[u"href"]))
		return e.convert(converter)


class author(xsc.Element):
	"""
	<par>can be used to embed author information in the header.
	It will generate <markup>&lt;link rel="made"/&gt;</markup> and
	<markup>&lt;meta name="author"/&gt;</markup> elements.</par>
	"""
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class lang(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class email(xsc.TextAttr): pass

	def convert(self, converter):
		e = xsc.Frag()
		if u"name" in self.attrs:
			e.append(html.meta(name=u"author", content=self[u"name"]))
			if u"lang" in self.attrs:
				e[-1][u"lang"] = self[u"lang"]
		if u"email" in self.attrs:
			e.append(html.link(rel=u"made", href=(u"mailto:", self[u"email"])))
		return e.convert(converter)


class refresh(xsc.Element):
	"""
	<par> a refresh header.</par>
	"""
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class secs(xsc.IntAttr):
			default = 0
		class href(xsc.URLAttr): pass

	def convert(self, converter):
		e = html.meta(http_equiv=u"Refresh", content=(self[u"secs"], u"; url=", self[u"href"]))
		return e.convert(converter)


class xmlns(xsc.Namespace):
	xmlname = "meta"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/meta"
xmlns.makemod(vars())
