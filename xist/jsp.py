#! /usr/bin/env python

"""
A module that allows you to embed JSP content as processing instructions.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import xsc

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

# register all the classes we've defined so far
namespace = xsc.Namespace("jsp", "http://java.sun.com/procudts/jsp/dtd/jsp_1_0.dtd", vars())
