#! /usr/bin/env python

"""
A XSC module that contains elements that simplify handling
meta data.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import xsc, html

class contenttype(html.meta):
	empty = 1
	attrHandlers = html.meta.attrHandlers.copy()
	del attrHandlers["http-equiv"]
	del attrHandlers["http_equiv"]
	del attrHandlers["name"]
	del attrHandlers["content"]

	def asHTML(self):
		e = html.meta(self.attrs)
		e["http-equiv"] = "Content-Type"
		e["content"] = "text/html"
		return e.asHTML()

class stylesheet(html.link):
	empty = 1
	attrHandlers = html.link.attrHandlers.copy()
	del attrHandlers["rel"]
	del attrHandlers["type"]

	def asHTML(self):
		e = html.link(self.attrs)
		e["rel"] = "stylesheet"
		e["type"] = "text/css"
		return e.asHTML()

namespace = xsc.Namespace("meta", "http://www.livinglogic.de/DTDs/meta.dtd", vars())

