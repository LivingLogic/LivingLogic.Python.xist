# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
A module that allows you to embed JSP content as processing instructions.
"""


import cgi # for parse_header

from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://java.sun.com/JSP/Page"


class directive(xsc.Element):
	model = sims.Empty()
	register = False # only serves as a base class

	def publish(self, publisher):
		yield publisher.encode(u"<%@ ")
		yield publisher.encode(self._publishname(publisher))
		for part in self.attrs.publish(publisher):
			yield part
		yield publisher.encode(u"%>")


class scriptlet(xsc.ProcInst):
	"""
	Will be published as ``<% content %>``.
	"""

	def publish(self, publisher):
		yield publisher.encode(u"<% ")
		yield publisher.encode(self.content)
		yield publisher.encode(u" %>")


class expression(xsc.ProcInst):
	"""
	Will be published as ``<%= content %>``.
	"""

	def publish(self, publisher):
		yield publisher.encode(u"<%= ")
		yield publisher.encode(self.content)
		yield publisher.encode(u" %>")


class declaration(xsc.ProcInst):
	"""
	Will be published as ``<%! content %>``.
	"""

	def publish(self, publisher):
		yield publisher.encode(u"<%! ")
		yield publisher.encode(self.content)
		yield publisher.encode(u" %>")


class If(scriptlet):
	xmlname = "if"

	def convert(self, converter):
		return scriptlet(u"if(", self.content, u"){")


class Else(scriptlet):
	xmlname = "else"

	def convert(self, converter):
		return scriptlet(u"}else{")


class ElIf(scriptlet):
	xmlname = "elif"

	def convert(self, converter):
		return scriptlet(u"}else if (", self.content, u"){")


class End(scriptlet):
	xmlname = "end"

	def convert(self, converter):
		return scriptlet(u"}")


class block(xsc.Element):
	"""
	This element embeds its content in ``{}`` brackets. Note that the content
	itself will not be turned into a scriptlet automatically but will be used
	as-is.
	"""
	model = sims.Any()

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
		class language(xsc.TextAttr):
			values = ("java",)
		class extends(xsc.TextAttr): pass
		class import_(xsc.TextAttr): xmlname = "import"
		class session(xsc.TextAttr): values = (u"true", u"false")
		class buffer(xsc.TextAttr): pass
		class autoFlush(xsc.TextAttr): values = (u"true", u"false")
		class isThreadSafe(xsc.TextAttr): values = (u"true", u"false")
		class info(xsc.TextAttr): pass
		class errorPage(xsc.URLAttr): pass
		class contentType(xsc.TextAttr): pass
		class isErrorPage(xsc.TextAttr): values = (u"true", u"false")
		class pageEncoding(xsc.TextAttr): pass

	def publish(self, publisher):
		# Only a contentType attribute triggers the special code
		if u"contentType" in self.attrs and not self.attrs.contentType.isfancy() and not self.attrs.pageEncoding.isfancy():
			(contenttype, options) = cgi.parse_header(unicode(self.attrs.contentType))
			pageencoding = unicode(self.attrs.pageEncoding)
			encoding = publisher.encoding
			if encoding is None:
				encoding = "utf-8"
			if u"charset" not in options or not (options[u"charset"] == pageencoding == encoding):
				options[u"charset"] = encoding
				node = self.__class__(
					self.attrs,
					contentType=(contenttype, u"; ", u"; ".join("{}={}".format(*option) for option in options.items())),
					pageEncoding=encoding
				)
				return node.publish(publisher) # return a generator-iterator
		return super(directive_page, self).publish(publisher) # return a generator-iterator


def fromul4(template, variables="variables", indent=0):
	"""
	Return the UL4 template :var:`template` as JSP source code. :var:`variables`
	is the variable name of the map object containing the top level variables.
	:var:`indent` is the initial indentation of the source code.

	The code produced requires the `UL4 Java package`__.

	__ http://hg.livinglogic.de/LivingLogic.Java.ul4
	"""
	return scriptlet(template.javasource(variables=variables, indent=indent))
