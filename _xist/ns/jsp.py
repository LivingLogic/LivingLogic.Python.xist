#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter D�rwald
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
<doc:par>A module that allows you to embed JSP content as processing instructions.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import cgi # for parse_header

from xist import xsc

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
	name = "if"

	def convert(self, converter):
		return scriptlet(u"if(" + self.content + u"){")

class Else(scriptlet):
	name = "else"

	def convert(self, converter):
		return scriptlet(u"}else{")

class ElIf(scriptlet):
	name = "elif"

	def convert(self, converter):
		return scriptlet(u"}else if (" + self.content + "){")

class End(scriptlet):
	name = "end"

	def convert(self, converter):
		return scriptlet(u"}")

class block(xsc.Element):
	"""
	<doc:par>This element embeds its content in <lit>{}</lit> brackets.</doc:par>
	<doc:par>Note that the content itself will not be turned into a scriptlet
	automatically but will be used as-is.</doc:par>
	"""
	empty = 0

	def convert(self, converter):
		e = xsc.Frag(
			scriptlet(u"{"),
			self.content,
			scriptlet(u"}")
		)
		return e.convert(converter)

class directive(xsc.Element):
	empty = 1
	register = 0 # only serves as a base class

	def publish(self, publisher):
		if self.publishPrefix is not None:
			publishPrefix = self.publishPrefix
		else:
			publishPrefix = publisher.publishPrefix
		publisher.publish(u"<%@ ")
		if publishPrefix:
			publisher.publish(self.prefix())
			publisher.publish(u":")
		name = self.name
		pos = name.find(".")
		if pos != -1:
			name = name[pos+1:]
		publisher.publish(name)
		self.attrs.publish(publisher)
		publisher.publish(u"%>")

class directive_include(directive):
	name = "directive.include"
	attrHandlers = {"file": xsc.TextAttr}

class directive_taglib(directive):
	name = "directive.taglib"
	attrHandlers = {"uri": xsc.TextAttr, "prefix": xsc.TextAttr}

class directive_page(directive):
	name = "directive.page"
	attrHandlers = {"import": xsc.TextAttr, "buffer": xsc.TextAttr, "errorPage": xsc.URLAttr, "session": xsc.TextAttr, "contentType": xsc.TextAttr}

	def publish(self, publisher):
		if not self.hasAttr("contentType"):
			node = self.__class__(self.attrs, contentType="text/html; charset=%s" % publisher.encoding)
			node.publish(publisher)
		else:
			(contenttype, options) = cgi.parse_header(unicode(self["contentType"]))
			if options.has_key(u"charset") and options[u"charset"] == publisher.encoding:
				super(directive_page, self).publish(publisher)
			else:
				options[u"charset"] = publisher.encoding
				node = self.__class__(
					self.attrs,
					contentType=(contenttype, u"; ", u"; ".join([ "%s=%s" % option for option in options.items()]))
				)
				node.publish(publisher)
# register all the classes we've defined so far
namespace = xsc.Namespace("jsp", "http://java.sun.com/products/jsp/dtd/jsp_1_0.dtd", vars())
