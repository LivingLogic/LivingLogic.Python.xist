#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
<par>An &xist; module that contains elements that simplify
handling meta data. All elements in this module will generate a
<pyref module="ll.xist.ns.html" class="meta"><class>html.meta</class></pyref>
element when converted.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc
import ihtml, html

class contenttype(html.meta):
	"""
	<par>can be used for a <markup>&lt;meta http-equiv="Content-Type" content="text/html"/&gt;</markup>, where
	the character set will be automatically inserted on a call to
	<pyref module="ll.xist.xsc" class="Node" method="publish"><method>publish</method></pyref>.</par>

	<par>Usage is simple: <markup>&lt;meta:contenttype/&gt;</markup></par>
	"""
	empty = True
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None

	def convert(self, converter):
		if converter.target=="ihtml":
			e = ihtml.meta(self.attrs)
		else:
			e = html.meta(self.attrs)
		e["http_equiv"] = "Content-Type"
		e["content"] = "text/html"
		return e.convert(converter)

class contentscripttype(html.meta):
	"""
	<par>can be used for a <markup>&lt;meta http-equiv="Content-Script-Type" content="..."/&gt;</markup>.</par>

	<par>Usage is simple: <markup>&lt;meta:contentscripttype type="text/javascript"/&gt;</markup></par>
	"""
	empty = True
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None
		class type(xsc.TextAttr): pass

	def convert(self, converter):
		attrs = self.attrs.copy()
		del attrs["type"]
		e = html.meta(attrs)
		e["http_equiv"] = "Content-Script-Type"
		e["content"] = self["type"]
		return e.convert(converter)

class keywords(html.meta):
	"""
	<par>can be used for a <markup>&lt;meta name="keywords" content="..."/&gt;</markup>.</par>

	<par>Usage is simple: <markup>&lt;meta:keywords&gt;foo, bar&lt;/meta:keywords&gt;</markup></par>
	"""
	empty = False
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None

	def convert(self, converter):
		e = html.meta(self.attrs)
		e["name"] = "keywords"
		e["content"] = self.content
		return e.convert(converter)

class description(html.meta):
	"""
	<par>can be used for a <markup>&lt;meta name="description" content="..."/&gt;</markup>.</par>

	<par>Usage is simple: <markup>&lt;meta:description&gt;This page describes the ...&lt;/meta:description&gt;</markup></par>
	"""
	empty = False
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None

	def convert(self, converter):
		e = html.meta(self.attrs)
		e["name"] = "description"
		e["content"] = self.content
		return e.convert(converter)

class stylesheet(html.link):
	"""
	<par>can be used for a <markup>&lt;link rel="stylesheet" type="text/css" href="..."/&gt;</markup>.</par>

	<par>Usage is simple: <markup>&lt;meta:stylesheet href="root:stylesheets/main.css"/&gt;</markup></par>
	"""
	empty = True
	class Attrs(html.link.Attrs):
		rel = None
		type = None

	def convert(self, converter):
		e = html.link(self.attrs, rel="stylesheet", type="text/css")
		return e.convert(converter)

class made(html.link):
	"""
	<par>can be used for a <markup>&lt;link rel="made" href="mailto:..."/&gt;</markup>.</par>

	<par>Usage is simple: <markup>&lt;meta:made href="foobert@bar.org"/&gt;</markup>.</par>
	"""
	empty = True
	class Attrs(html.link.Attrs):
		rel = None

	def convert(self, converter):
		e = html.link(self.attrs, rel="made", href=("mailto:", self["href"]))
		return e.convert(converter)

class author(xsc.Element):
	"""
	<par>can be used to embed author information in the header.
	It will generate <markup>&lt;link rel="made"/&gt;</markup> and
	<markup>&lt;meta name="author"/&gt;</markup> elements.</par>
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class lang(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class email(xsc.TextAttr): pass

	def convert(self, converter):
		e = xsc.Frag()
		if self.hasattr("name"):
			e.append(html.meta(name="author", content=self["name"]))
			if self.hasattr("lang"):
				e[-1]["lang"] = self["lang"]
		if self.hasattr("email"):
			e.append(html.link(rel="made", href=("mailto:", self["email"])))
		return e.convert(converter)

class refresh(xsc.Element):
	"""
	<par> a refresh header.</par>
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class secs(xsc.IntAttr):
			default = 0
		class href(xsc.URLAttr): pass

	def convert(self, converter):
		e = html.meta(http_equiv="Refresh", content=(self["secs"], "; url=", self["href"]))
		return e.convert(converter)

xmlns = xsc.Namespace("meta", "http://xmlns.livinglogic.de/xist/ns/meta", vars())
