#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
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
<doc:par>An &xist; module that contains elements that simplify handling
meta data. All elements in this module will generate a <pyref module="xist.ns.html" class="meta">html.meta</pyref>
element when converted.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc
import html

class contenttype(html.meta):
	"""
	<doc:par>can be used for a <markup>&lt;meta http-equiv="Content-Type" content="text/html"/&gt;</markup>, where
	the character set will be automatically inserted on a call to <pyref module="xist.xsc" class="Node" method="publish">publish</pyref>.</doc:par>

	<doc:par>Usage is simple: <code>&lt;meta:contenttype/&gt;</code></doc:par>
	"""
	empty = 1
	attrHandlers = html.meta.attrHandlers.copy()
	del attrHandlers["http-equiv"]
	del attrHandlers["http_equiv"]
	del attrHandlers["name"]
	del attrHandlers["content"]

	def convert(self, converter):
		e = html.meta(self.attrs)
		e["http-equiv"] = "Content-Type"
		e["content"] = "text/html"
		return e.convert(converter)

class keywords(html.meta):
	"""
	<doc:par>can be used for a <markup>&lt;meta name="keywords" content="..."/&gt;</markup>.</doc:par>

	<doc:par>Usage is simple: <markup>&lt;meta:keywords&gt;foo, bar&lt;/meta:keywords&gt;</markup></doc:par>
	"""
	empty = 0
	attrHandlers = html.meta.attrHandlers.copy()
	del attrHandlers["http-equiv"]
	del attrHandlers["http_equiv"]
	del attrHandlers["name"]
	del attrHandlers["content"]

	def convert(self, converter):
		e = html.meta(self.attrs)
		e["name"] = "keywords"
		e["content"] = self.content
		return e.convert(converter)

class description(html.meta):
	"""
	<doc:par>can be used for a <markup>&lt;meta name="description" content="..."/&gt;</markup>.</doc:par>

	<doc:par>Usage is simple: <markup>&lt;meta:description&gt;foo, bar&lt;/meta:description&gt;</markup></doc:par>
	"""
	empty = 0
	attrHandlers = html.meta.attrHandlers.copy()
	del attrHandlers["http-equiv"]
	del attrHandlers["http_equiv"]
	del attrHandlers["name"]
	del attrHandlers["content"]

	def convert(self, converter):
		e = html.meta(self.attrs)
		e["name"] = "description"
		e["content"] = self.content
		return e.convert(converter)

class stylesheet(html.link):
	"""
	<doc:par>can be used for a <markup>&lt;link rel="stylesheet" type="text/css" href="..."/&gt;</markup>.</doc:par>

	<doc:par>Usage is simple: <markup>&lt;meta:stylesheet href="root:stylesheets/main.css"/&gt;</markup></doc:par>
	"""
	empty = 1
	attrHandlers = html.link.attrHandlers.copy()
	del attrHandlers["rel"]
	del attrHandlers["type"]

	def convert(self, converter):
		e = html.link(self.attrs)
		e["rel"] = "stylesheet"
		e["type"] = "text/css"
		return e.convert(converter)

class made(html.link):
	"""
	<doc:par>can be used for a <markup>&lt;link rel="made" href="mailto:..."/&gt;</markup>.</doc:par>

	<doc:par>Usage is simple: <markup>&lt;meta:made href="foobert@bar.org"/&gt;</markup>.</doc:par>
	"""
	empty = 1
	attrHandlers = html.link.attrHandlers.copy()
	del attrHandlers["rel"]

	def convert(self, converter):
		e = html.link(self.attrs)
		e["rel"] = "made"
		e["href"] = ("mailto:", self["href"])
		return e.convert(converter)

class author(xsc.Element):
	"""
	<doc:par>can be used to embed author information in the header.
	It will generate <markup>&lt;link rel="made"/&gt;</markup> and
	<markup>&lt;meta name="author"/&gt;</markup> elements.</doc:par>
	"""
	empty = 1
	attrHandlers = {"lang": xsc.TextAttr, "name": xsc.TextAttr, "email": xsc.TextAttr}

	def convert(self, converter):
		e = xsc.Frag()
		if self.hasAttr("name"):
			e.append(html.meta(name="author", content=self["name"]))
			if self.hasAttr("lang"):
				e[-1]["lang"] = self["lang"]
		if self.hasAttr("email"):
			e.append(html.link(rel="made", href=("mailto:", self["email"])))
		return e.convert(converter)

class refresh(xsc.Element):
	"""
	<doc:par> a refresh header.</doc:par>
	"""
	empty = 0
	attrHandlers = {"secs": xsc.IntAttr, "href": xsc.URLAttr}

	def convert(self, converter):
		e = html.meta(http_equiv="Refresh", content=(self.getAttr("secs", 0), "; url=", self["href"]))
		return e.convert(converter)

namespace = xsc.Namespace("meta", "http://www.livinglogic.de/DTDs/meta.dtd", vars())
