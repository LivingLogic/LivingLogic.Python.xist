#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; module that contains a collection of useful elements that
can be used for all conversion target, because they only generate text.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, types, datetime

from ll.xist import xsc, parsers

class z(xsc.Element):
	"""
	<par>puts it's content into french quotes</par>
	"""
	empty = False

	def convert(self, converter):
		e = xsc.Frag(u"»", self.content.convert(converter), u"«")

		return e

	def __unicode__(self):
		return u"»" + unicode(self.content) + u"«"

class filesize(xsc.Element):
	"""
	<par>the size (in bytes) of the file whose URL is the attribute href
	as a text node.</par>
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): pass

	def convert(self, converter):
		size = self["href"].convert(converter).contentlength(root=converter.root)
		if size is not None:
			return xsc.Text(size)
		else:
			return xsc.Text("?")

class filetime(xsc.Element):
	"""
	<par>the time of the last modification of the file whose &url; is in the attribute <lit>href</lit>
	as a text node. This will always be an &utc; timestamp.</par>
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): pass
			"""
			<par>The &url; of the file.</par>
			"""
		class format(xsc.TextAttr):
			"""
			<par>A <function>strftime</function> compatible formatstring for formatting the timestamp.</par>
			"""
			default = "%d. %b. %Y, %H:%M"

	def convert(self, converter):
		format = str(self["format"].convert(converter))
		return xsc.Text(self["href"].convert(converter).lastmodified(root=converter.root).Format(format))

class time(xsc.Element):
	"""
	<par>the current time (i.e. the time when <pyref method="convert"><method>convert</method></pyref>
	is called). You can specify the format of the string in the attribute format, which is a
	<function>strftime</function> compatible string.</par>
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class format(xsc.TextAttr):
			"""
			<par>A <function>strftime</function> compatible formatstring for formatting the timestamp.</par>
			"""
			default = "%d. %b. %Y, %H:%M"
		class utc(xsc.BoolAttr):
			"""
			<par>Should &utc; be used or local time?</par>
			"""

	def convert(self, converter):
		format = str(self["format"].convert(converter))
		if "utc" in self.attrs:
			f = datetime.datetime.utcnow
		else:
			f = datetime.datetime.now

		return xsc.Text(f().strftime(format))

class x(xsc.Element):
	"""
	<par>Element that will be ignored when converted.</par>

	<par><class>x</class> can be used to comment out stuff.
	The content of the element must of course still be wellformed.</par>
	"""
	empty = False

	def convert(self, converter):
		return xsc.Null

class include(xsc.Element):
	empty = True
	class Attrs(xsc.Element.Attrs):
		class src(xsc.URLAttr): pass

	def convert(self, converter):
		e = parsers.parseURL(self["src"].forInput())

		return e.convert(converter)

class loremipsum(xsc.Element):
	empty = True
	class Attrs(xsc.Element.Attrs):
		class len(xsc.IntAttr): pass

	text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diem nonummy nibh euismod tincidnut ut lacreet dolore magna aliguam erat volutpat. Ut wisis enim ad minim veniam, quis nostrud exerci tution ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis te feugifacilisi. Duis antem dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zril delinit au gue duis dolore te feugat nulla facilisi."

	def convert(self, converter):
		if self.attrs.has("len"):
			text = self.text[:int(self["len"].convert(converter))]
		else:
			text = self.text
		return xsc.Text(text)

class wrap(xsc.Element):
	"""
	<par>a wrapper element that returns its content when converted.</par>

	<par>This is e.g. useful if you want to parse a
	file that starts with <pyref module="ll.xist.ns.jsp"><module>&jsp;</module></pyref>
	processing instructions.</par>

	<par>This is also used for publishing, when <lit>xmlns</lit> attributes
	are required, but the root is not an element.</par>
	"""
	empty = False

	def convert(self, converter):
		return self.content.convert(converter)

class AttrDecorator(xsc.Element):
	empty = False
	register = False

	decoratable = ()

	class Visitor(object):

		def __init__(self, decorator, converter):
			self.decorator = decorator
			self.converter = converter

		def isdecoratable(self, node):
			return isinstance(node, self.decorator.decoratable)

		def visit(self, node):
			found = xsc.Found(enter=True)
			if self.isdecoratable(node):
				found.foundstart = self.decorate
			return found

		def decorate(self, node, start):
			for (attrname, attrvalue) in self.decorator.attrs.iteritems():
				if attrname not in node.attrs:
					node[attrname] = attrvalue.convert(self.converter)

	def convert(self, converter):
		node = self.content.convert(converter)
		visitor = self.Visitor(self, converter)
		node.visit(visitor.visit)
		return node

# Control characters (not part of HTML)
class lf(xsc.CharRef): "line feed"; codepoint = 10
class cr(xsc.CharRef): "carriage return"; codepoint = 13
class tab(xsc.CharRef): "horizontal tab"; codepoint = 9
class esc(xsc.CharRef): "escape"; codepoint = 27

class xmlns(xsc.Namespace):
	xmlname = "specials"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/specials"
xmlns.makemod(vars())

