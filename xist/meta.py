#! /usr/bin/env python

"""
A XSC module that contains elements that simplify handling
meta data.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import xsc, html

class contenttype(html.meta):
	"""
	<par noindent>can be used for a <code>&lt;meta http-equiv="Content-Type" content="text/html"/&gt;</code>, where
	the character set will be automatically inserted on a call to <code>publish()</code>.</par>

	<par>Usage is simple: <code>&lt;meta:contenttype/&gt;</code></par>
	"""
	empty = 1
	attrHandlers = html.meta.attrHandlers.copy()
	del attrHandlers["http-equiv"]
	del attrHandlers["http_equiv"]
	del attrHandlers["name"]
	del attrHandlers["content"]

	def asHTML(self):
		e = html.meta(**self.attrs)
		e["http-equiv"] = "Content-Type"
		e["content"] = "text/html"
		return e.asHTML()

class keywords(html.meta):
	"""
	<par noindent>can be used for a <code>&lt;meta name="keywords" content="..."/&gt;</code>.</par>

	<par>Usage is simple: <code>&lt;meta:keywords&gt;foo, bar&lt;/meta:keywords&gt;</code></par>
	"""
	empty = 0
	attrHandlers = html.meta.attrHandlers.copy()
	del attrHandlers["http-equiv"]
	del attrHandlers["http_equiv"]
	del attrHandlers["name"]
	del attrHandlers["content"]

	def asHTML(self):
		e = html.meta(**self.attrs)
		e["name"] = "keywords"
		e["content"] = self.content.asHTML().asPlainString()
		return e.asHTML()

class description(html.meta):
	"""
	<par noindent>can be used for a <code>&lt;meta name="description" content="..."/&gt;</code>.</par>

	<par>Usage is simple: <code>&lt;meta:description&gt;foo, bar&lt;/meta:description&gt;</code></par>
	"""
	empty = 0
	attrHandlers = html.meta.attrHandlers.copy()
	del attrHandlers["http-equiv"]
	del attrHandlers["http_equiv"]
	del attrHandlers["name"]
	del attrHandlers["content"]

	def asHTML(self):
		e = html.meta(**self.attrs)
		e["name"] = "description"
		e["content"] = self.content.asHTML().asPlainString()
		return e.asHTML()

class stylesheet(html.link):
	"""
	<par noindent>can be used for a <code>&lt;link rel="stylesheet" type="text/css" href="..."/&gt;</code>.</par>

	<par>Usage is simple: <code>&lt;meta:stylesheet href="*/stylesheets/main.css"/&gt;</code></par>
	"""
	empty = 1
	attrHandlers = html.link.attrHandlers.copy()
	del attrHandlers["rel"]
	del attrHandlers["type"]

	def asHTML(self):
		e = html.link(**self.attrs)
		e["rel"] = "stylesheet"
		e["type"] = "text/css"
		return e.asHTML()

class made(html.link):
	"""
	<par noindent>can be used for a <code>&lt;link rel="made" href="mailto:..."/&gt;</code>.</par>

	<par>Usage is simple: <code>&lt;meta:made href="foobert@bar.org"/&gt;</code>.</par>
	"""
	empty = 1
	attrHandlers = html.link.attrHandlers.copy()
	del attrHandlers["rel"]

	def asHTML(self):
		e = html.link(**self.attrs)
		e["rel"] = "made"
		e["href"] = ("mailto:", e["href"])
		return e.asHTML()

namespace = xsc.Namespace("meta", "http://www.livinglogic.de/DTDs/meta.dtd", vars())

