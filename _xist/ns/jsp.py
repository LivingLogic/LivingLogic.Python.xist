#! /usr/bin/env python

"""
A module that allows you to embed JSP content as processing instructions.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc

class scriptlet(xsc.ProcInst):
	"""
	will be published as <% data %>
	"""
	def publish(self, publisher):
		publisher.publish(u"<% ")
		publisher.publish(self.content)
		publisher.publish(u" %>")

class expression(xsc.ProcInst):
	"""
	will be published as <%= data %>
	"""

	def publish(self, publisher):
		publisher.publish(u"<%= ")
		publisher.publish(self.content)
		publisher.publish(u" %>")

class declaration(xsc.ProcInst):
	"""
	will be published as <%! data %>
	"""

	def publish(self, publisher):
		publisher.publish(u"<%! ")
		publisher.publish(self.content)
		publisher.publish(u" %>")

class If(scriptlet):
	name = "if"

	def publish(self, publisher):
		publisher.publish(u"<% if(")
		publisher.publish(self.content)
		publisher.publish(u"){ %>")

class Else(scriptlet):
	name = "else"
	def publish(self, publisher):
		publisher.publish(u"<% }else{ %>")

class ElIf(scriptlet):
	name = "elif"

	def publish(self, publisher):
		publisher.publish(u"<% }else if(")
		publisher.publish(self.content)
		publisher.publish(u"){ %>")

class End(scriptlet):
	name = "end"
	def publish(self, publisher):
		publisher.publish(u"<% } %>")

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
		self._publishAttrs(publisher)
		publisher.publish(u"%>")

class directive_include(directive):
	register = 1
	name = "directive.include"
	attrHandlers = {"file": xsc.TextAttr}

class directive_taglib(directive):
	register = 1
	name = "directive.taglib"
	attrHandlers = {"uri": xsc.TextAttr, "prefix": xsc.TextAttr}

class directive_page(directive):
	register = 1
	name = "directive.page"
	attrHandlers = {"import": xsc.TextAttr, "buffer": xsc.TextAttr, "errorPage": xsc.URLAttr}

# register all the classes we've defined so far
namespace = xsc.Namespace("jsp", "http://java.sun.com/products/jsp/dtd/jsp_1_0.dtd", vars())
