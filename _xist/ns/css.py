#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
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
<doc:par>An &xist; module that contains elements that can be used to generate
CSS files.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc

class css(xsc.Element):
	"""
	The root element
	"""
	empty = 0

	def publish(self, publisher):
		# publish the imports first
		imports = self.find(type=import_)
		for i in imports:
			publisher.publish(u"\n")
			i.publish(publisher)
		# FIXME: publish global and media specific rules in their given order
		rules = self.find(type=rule)
		for r in rules:
			publisher.publish(u"\n")
			r.publish(publisher)

class import_(xsc.Element):
	"""
	<doc:par>A CSS import rule.</doc:par>
	"""
	empty = 0
	name = "import"

	def publish(self, publisher):
		publisher.publish(u'@import url("')
		self.content.publish(publisher)
		publisher.publish(u'");')

class rule(xsc.Element):
	"""
	<doc:par>One CSS rule (with potentially multiple <pyref class="sel">selectors</pyref>).</doc:par>
	"""
	empty = 0

	def publish(self, publisher):
		sels = self.find(type=sel)
		props = self.find(type=prop, subtype=1)

		for i in xrange(len(sels)):
			if i != 0:
				publisher.publish(u", ")
			sels[i].publish(publisher)
		publisher.publish(u" { ")
		for i in xrange(len(props)):
			if i != 0:
				publisher.publish(u" ")
			props[i].publish(publisher)
		publisher.publish(u" }")

class sel(xsc.Element):
	"""
	<doc:par>A CSS selector.</doc:par>
	"""
	empty = 0

	def publish(self, publisher):
		self.content.publish(publisher)

class prop(xsc.Element):
	"""
	<doc:par>A CSS property.</doc:par>
	"""
	empty = 0
	attrHandlers = {"important": xsc.BoolAttr}

	def publish(self, publisher):
		publisher.publish(u"%s: " % self.name)
		self.content.publish(publisher)
		if self.hasAttr("important"):
			publisher.publish(u" !important")
		publisher.publish(u";")

class margin_top(prop):
	name = "margin-top"

class margin_right(prop):
	name = "margin-right"

class margin_bottom(prop):
	name = "margin-bottom"

class margin_left(prop):
	name = "margin-left"

# register all the classes we've defined so far
namespace = xsc.Namespace("css", "http://www.w3.org/TR/REC-CSS2", vars())

