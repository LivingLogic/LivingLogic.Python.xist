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
<par>A module that allows you to embed &jsp; content as processing instructions.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import cgi # for parse_header

from ll.xist import xsc

class scriptlet(xsc.ProcInst):
	"""
	will be published as <markup>&lt;% <rep>content</rep> %&gt;</markup>
	"""
	def publish(self, publisher):
		publisher.publish(u"<% ")
		publisher.publish(self.content)
		publisher.publish(u" %>")

class expression(xsc.ProcInst):
	"""
	will be published as <markup>&lt;%= <rep>content</rep> %&gt;</markup>
	"""

	def publish(self, publisher):
		publisher.publish(u"<%= ")
		publisher.publish(self.content)
		publisher.publish(u" %>")

class declaration(xsc.ProcInst):
	"""
	will be published as <markup>&lt;%! <rep>content</rep> %&gt;</markup>
	"""

	def publish(self, publisher):
		publisher.publish(u"<%! ")
		publisher.publish(self.content)
		publisher.publish(u" %>")

class If(scriptlet):
	xmlname = "if"

	def convert(self, converter):
		return scriptlet(u"if(" + self.content + u"){")

class Else(scriptlet):
	xmlname = "else"

	def convert(self, converter):
		return scriptlet(u"}else{")

class ElIf(scriptlet):
	xmlname = "elif"

	def convert(self, converter):
		return scriptlet(u"}else if (" + self.content + "){")

class End(scriptlet):
	xmlname = "end"

	def convert(self, converter):
		return scriptlet(u"}")

class block(xsc.Element):
	"""
	<par>This element embeds its content in <lit>{}</lit> brackets.</par>
	<par>Note that the content itself will not be turned into a scriptlet
	automatically but will be used as-is.</par>
	"""
	empty = False

	def convert(self, converter):
		e = xsc.Frag(
			scriptlet(u"{"),
			self.content,
			scriptlet(u"}")
		)
		return e.convert(converter)

class directive(xsc.Element):
	empty = True
	register = False # only serves as a base class

	def publish(self, publisher):
		publisher.publish(u"<%@ ")
		self._publishname(publisher)
		self.attrs.publish(publisher)
		publisher.publish(u"%>")

class directive_include(directive):
	xmlname = "include"
	class Attrs(directive.Attrs):
		class file(xsc.TextAttr): pass

class directive_taglib(directive):
	xmlname = "taglib"
	class Attrs(directive.Attrs):
		class uri(xsc.TextAttr): pass
		class prefix(xsc.TextAttr): pass

class directive_page(directive):
	xmlname = "page"
	class Attrs(directive.Attrs):
		class import_(xsc.TextAttr): xmlname = "import"
		class buffer(xsc.TextAttr): pass
		class errorPage(xsc.URLAttr): pass
		class session(xsc.TextAttr): pass
		class contentType(xsc.TextAttr): pass

	def publish(self, publisher):
		if not self.hasattr("contentType"):
			node = self.__class__(self.attrs, contentType="text/html; charset=%s" % publisher.encoding)
			node.publish(publisher)
		else:
			(contenttype, options) = cgi.parse_header(unicode(self["contentType"]))
			if u"charset" in options and options[u"charset"] == publisher.encoding:
				super(directive_page, self).publish(publisher)
			else:
				options[u"charset"] = publisher.encoding
				node = self.__class__(
					self.attrs,
					contentType=(contenttype, u"; ", u"; ".join([ "%s=%s" % option for option in options.items()]))
				)
				node.publish(publisher)

# register all the classes we've defined so far
xmlns = xsc.Namespace("jsp", "http://java.sun.com/products/jsp/dtd/jsp_1_0.dtd", vars())
