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
	def __init__(self, content=u""):
		xsc.ProcInst.__init__(self, u"scriptlet", content)

	def publish(self, publisher):
		publisher.publish(u"<% ")
		publisher.publish(self._content)
		publisher.publish(u"%>")

class expression(xsc.ProcInst):
	"""
	will be published as <%= data %>
	"""

	def __init__(self, content=u""):
		xsc.ProcInst.__init__(self, u"expression", content)

	def publish(self, publisher):
		publisher.publish(u"<%= ")
		publisher.publish(self._content)
		publisher.publish(u"%>")

class declaration(xsc.ProcInst):
	"""
	will be published as <%! data %>
	"""

	def __init__(self, content=u""):
		xsc.ProcInst.__init__(self, u"declaration", content)

	def publish(self, publisher):
		publisher.publish(u"<%! ")
		publisher.publish(self._content)
		publisher.publish(u"%>")

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
			publisher.publish(self.namespace.prefix) # requires that the element is registered via registerElement()
			publisher.publish(u":")
		name = self.name
		pos = name.find(".")
		if pos != -1:
			name = name[pos+1:]
		publisher.publish(name)
		self._publishAttrs(publisher)
		publisher.publish(u"%>")

class directive_import(directive):
	register = 1
	name = "directive.import"
	attrHandlers = {"buffer": xsc.TextAttr}

# register all the classes we've defined so far
namespace = xsc.Namespace("jsp", "http://java.sun.com/procudts/jsp/dtd/jsp_1_0.dtd", vars())
