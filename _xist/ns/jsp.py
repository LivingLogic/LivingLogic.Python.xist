#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter D�rwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>A module that allows you to embed &jsp; content as processing instructions.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import cgi # for parse_header

from ll.xist import xsc

class directive(xsc.Element):
	empty = True
	register = False # only serves as a base class

	def publish(self, publisher):
		publisher.publish(u"<%@ ")
		self._publishname(publisher)
		self.attrs.publish(publisher)
		publisher.publish(u"%>")

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
		if not self.attrs.has("contentType") or self["contentType"].isfancy():
			super(directive_page, self).publish(publisher)
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

class xmlns(xsc.Namespace):
	xmlname = "jsp"
	xmlurl = "http://java.sun.com/products/jsp/dtd/jsp_1_0.dtd"
xmlns.makemod(vars())

