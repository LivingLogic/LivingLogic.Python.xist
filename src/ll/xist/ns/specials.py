# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
An XIST module that contains a collection of useful elements that can be used
for all conversion target, because they only generate text.
"""


import sys, types, datetime

from ll import url as url_
from ll.xist import xsc, parsers, sims


__docformat__ = "reStructuredText"


xmlns = "http://xmlns.livinglogic.de/xist/ns/specials"


class z(xsc.Element):
	"""
	Put the content into double quotes.
	"""
	xmlns = xmlns
	model = sims.Any()

	def convert(self, converter):
		e = xsc.Frag(u"\u201c", self.content, u"\u201d")
		return e.convert(converter)


class filesize(xsc.Element):
	"""
	The size (in bytes) of the file whose URL is the attribute href as a
	text node.
	"""
	xmlns = xmlns
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
	The time of the last modification of the file whose URL is in the attribute
	``href`` as a text node. This will always be an UTC timestamp.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr):
			"""
			The URL of the file.
			"""
			required = True

		class format(xsc.TextAttr):
			"""
			A :func:`strftime` compatible formatstring for formatting the timestamp.
			"""
			default = u"%d. %b. %Y, %H:%M"

	def convert(self, converter):
		format = str(self[u"format"].convert(converter))
		return xsc.Text(self[u"href"].convert(converter).lastmodified(root=converter.root).strftime(format))


class time(xsc.Element):
	"""
	the current time (i.e. the time when :meth:`convert` is called). You can
	specify the format of the string in the attribute ``format``, which is a
	:func:`strftime` compatible string.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class format(xsc.TextAttr):
			"""
			A :func:`strftime` compatible formatstring for formatting the timestamp.
			"""
			default = u"%d. %b. %Y, %H:%M"
		class utc(xsc.BoolAttr):
			"""
			Should UTC be used or local time?
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
	Element that will be ignored when converted.

	:class:`ignore` can be used to comment out stuff. The content of the
	element must of course still be wellformed.
	"""
	xmlns = xmlns
	model = sims.Any()

	def convert(self, converter):
		return xsc.Null


class include(xsc.Element):
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class src(xsc.URLAttr): pass

	def convert(self, converter):
		e = parsers.parseURL(self[u"src"].forInput())

		return e.convert(converter)


class loremipsum(xsc.Element):
	xmlns = xmlns
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
	A wrapper element that returns its content when converted.

	This is e.g. useful if you want to parse a file that starts with
	:mod:`ll.xist.ns.jsp` processing instructions.
	"""
	xmlns = xmlns
	model = sims.Any()

	def convert(self, converter):
		return self.content.convert(converter)


class AttrDecorator(xsc.Element):
	xmlns = xmlns
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
	:class:`literal` is a processing instruction that will output its content
	literally when published.
	"""
	def publish(self, publisher):
		yield publisher.encode(self.content)


class url(xsc.ProcInst):
	"""
	:class:`url` is a processing instruction containing an URL. On publishing
	it will be replaced by an URL that is relative to the base URL of the
	publisher.
	"""
	def parsed(self, parser, start=None):
		return self.__class__(unicode(parser.base/self.content))

	def publish(self, publisher):
		yield publisher.encodetext(unicode(url_.URL(self.content).relative(publisher.base)))


# Control characters (not part of HTML)
class lf(xsc.CharRef): "line feed"; codepoint = 10
class cr(xsc.CharRef): "carriage return"; codepoint = 13
class tab(xsc.CharRef): "horizontal tab"; codepoint = 9
class esc(xsc.CharRef): "escape"; codepoint = 27
