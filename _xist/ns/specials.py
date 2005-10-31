#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
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

from ll.xist import xsc, parsers, sims


class z(xsc.Element):
	"""
	<par>Put the content into double quotes.</par>
	"""
	model = sims.Any()

	def convert(self, converter):
		e = xsc.Frag(u"\u201c", self.content, u"\u201d")
		return e.convert(converter)


class filesize(xsc.Element):
	"""
	<par>the size (in bytes) of the file whose URL is the attribute href
	as a text node.</par>
	"""
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): required = True

	def convert(self, converter):
		size = self[u"href"].convert(converter).contentlength(root=converter.root)
		if size is not None:
			return xsc.Text(size)
		else:
			return xsc.Text(u"?")


class filetime(xsc.Element):
	"""
	<par>the time of the last modification of the file whose &url; is in the attribute <lit>href</lit>
	as a text node. This will always be an &utc; timestamp.</par>
	"""
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr):
			"""
			<par>The &url; of the file.</par>
			"""
			required = True

		class format(xsc.TextAttr):
			"""
			<par>A <function>strftime</function> compatible formatstring for formatting the timestamp.</par>
			"""
			default = u"%d. %b. %Y, %H:%M"

	def convert(self, converter):
		format = str(self[u"format"].convert(converter))
		return xsc.Text(self[u"href"].convert(converter).lastmodified(root=converter.root).strftime(format))


class time(xsc.Element):
	"""
	<par>the current time (i.e. the time when <pyref method="convert"><method>convert</method></pyref>
	is called). You can specify the format of the string in the attribute <lit>format</lit>, which is a
	<function>strftime</function> compatible string.</par>
	"""
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class format(xsc.TextAttr):
			"""
			<par>A <function>strftime</function> compatible formatstring for formatting the timestamp.</par>
			"""
			default = u"%d. %b. %Y, %H:%M"
		class utc(xsc.BoolAttr):
			"""
			<par>Should &utc; be used or local time?</par>
			"""

	def convert(self, converter):
		format = str(self[u"format"].convert(converter))
		if u"utc" in self.attrs:
			f = datetime.datetime.utcnow
		else:
			f = datetime.datetime.now

		return xsc.Text(f().strftime(format))


class ignore(xsc.Element):
	"""
	<par>Element that will be ignored when converted.</par>

	<par><class>ignore</class> can be used to comment out stuff.
	The content of the element must of course still be wellformed.</par>
	"""
	model = sims.Any()

	def convert(self, converter):
		return xsc.Null


class include(xsc.Element):
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class src(xsc.URLAttr): pass

	def convert(self, converter):
		e = parsers.parseURL(self[u"src"].forInput())

		return e.convert(converter)


class loremipsum(xsc.Element):
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class len(xsc.IntAttr): pass

	text = u"Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diem nonummy nibh euismod tincidnut ut lacreet dolore magna aliguam erat volutpat. Ut wisis enim ad minim veniam, quis nostrud exerci tution ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis te feugifacilisi. Duis antem dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zril delinit au gue duis dolore te feugat nulla facilisi."

	def convert(self, converter):
		if u"len" in self.attrs:
			text = self.text[:int(self[u"len"].convert(converter))]
		else:
			text = self.text
		return xsc.Text(text)


class wrap(xsc.Element):
	"""
	<par>a wrapper element that returns its content when converted.</par>

	<par>This is e.g. useful if you want to parse a
	file that starts with <pyref module="ll.xist.ns.jsp"><module>&jsp;</module></pyref>
	processing instructions.</par>
	"""
	model = sims.Any()

	def convert(self, converter):
		return self.content.convert(converter)


class AttrDecorator(xsc.Element):
	model = sims.Any()
	register = False

	decoratable = ()

	def _mapper(self, node, converter):
		if isinstance(node, self.decoratable):
			node = node.__class__(
				node.content.mapped(self._mapper, converter),
				node.attrs.mapped(self._mapper, converter),
			)
			for (attrname, attrvalue) in self.attrs.iteritems():
				if attrname not in node.attrs:
					node[attrname] = attrvalue.convert(converter)
		return node

	def convert(self, converter):
		node = self.content.convert(converter)
		node = node.mapped(self._mapper, converter)
		return node


class literal(xsc.ProcInst):
	"""
	<class>literal</class> is a processing instruction that will output
	its content literally when published.
	"""
	def publish(self, publisher):
		yield publisher.encode(self.content)


# Control characters (not part of HTML)
class lf(xsc.CharRef): "line feed"; codepoint = 10
class cr(xsc.CharRef): "carriage return"; codepoint = 13
class tab(xsc.CharRef): "horizontal tab"; codepoint = 9
class esc(xsc.CharRef): "escape"; codepoint = 27


class __ns__(xsc.Namespace):
	xmlname = "specials"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/specials"
__ns__.makemod(vars())
