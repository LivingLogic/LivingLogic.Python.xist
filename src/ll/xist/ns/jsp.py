# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


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
		yield publisher.encode("<%@ ")
		yield publisher.encode(self._publishname(publisher))
		yield from self.attrs.publish(publisher)
		yield publisher.encode("%>")


class scriptlet(xsc.ProcInst):
	"""
	Will be published as ``<% content %>``.
	"""

	def publish(self, publisher):
		yield publisher.encode("<% ")
		yield publisher.encode(self.content)
		yield publisher.encode(" %>")


class expression(xsc.ProcInst):
	"""
	Will be published as ``<%= content %>``.
	"""

	def publish(self, publisher):
		yield publisher.encode("<%= ")
		yield publisher.encode(self.content)
		yield publisher.encode(" %>")


class declaration(xsc.ProcInst):
	"""
	Will be published as ``<%! content %>``.
	"""

	def publish(self, publisher):
		yield publisher.encode("<%! ")
		yield publisher.encode(self.content)
		yield publisher.encode(" %>")


class If(scriptlet):
	xmlname = "if"
	prettyindentbefore = 0
	prettyindentafter = 1

	def convert(self, converter):
		return scriptlet("if(", self.content, "){")


class Else(scriptlet):
	xmlname = "else"
	prettyindentbefore = -1
	prettyindentafter = 1

	def convert(self, converter):
		return scriptlet("}else{")


class ElIf(scriptlet):
	xmlname = "elif"
	prettyindentbefore = -1
	prettyindentafter = 1

	def convert(self, converter):
		return scriptlet("}else if (", self.content, "){")


class End(scriptlet):
	xmlname = "end"
	prettyindentbefore = -1
	prettyindentafter = 0

	def convert(self, converter):
		return scriptlet("}")


class block(xsc.Element):
	"""
	This element embeds its content in ``{}`` brackets. Note that the content
	itself will not be turned into a scriptlet automatically but will be used
	as-is.
	"""
	model = sims.Any()

	def convert(self, converter):
		e = xsc.Frag(
			scriptlet("{"),
			self.content,
			scriptlet("}")
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
		class session(xsc.TextAttr): values = ("true", "false")
		class buffer(xsc.TextAttr): pass
		class autoFlush(xsc.TextAttr): values = ("true", "false")
		class isThreadSafe(xsc.TextAttr): values = ("true", "false")
		class info(xsc.TextAttr): pass
		class errorPage(xsc.URLAttr): pass
		class contentType(xsc.TextAttr): pass
		class isErrorPage(xsc.TextAttr): values = ("true", "false")
		class pageEncoding(xsc.TextAttr): pass

	def publish(self, publisher):
		# Only a contentType attribute triggers the special code
		if "contentType" in self.attrs and not self.attrs.contentType.isfancy() and not self.attrs.pageEncoding.isfancy():
			(contenttype, options) = cgi.parse_header(str(self.attrs.contentType))
			pageencoding = str(self.attrs.pageEncoding)
			encoding = publisher.encoding
			if encoding is None:
				encoding = "utf-8"
			if "charset" not in options or not (options["charset"] == pageencoding == encoding):
				options["charset"] = encoding
				node = self.__class__(
					self.attrs,
					contentType=(contenttype, "; ", "; ".join(f"{name}={value}" for (name, value) in options.items())),
					pageEncoding=encoding
				)
				return node.publish(publisher) # return a generator-iterator
		return super().publish(publisher) # return a generator-iterator


def fromul4(template, variables="variables", indent=0):
	"""
	Return the UL4 template :obj:`template` as JSP source code. :obj:`variables`
	is the variable name of the map object containing the top level variables.
	:obj:`indent` is the initial indentation of the source code.

	The code produced requires the `UL4 Java package`__.

	__ https://github.com/LivingLogic/LivingLogic.Java.ul4
	"""
	return scriptlet(template.javasource(variables=variables, indent=indent))
