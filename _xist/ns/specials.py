#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
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
<par>An &xist; module that contains a collection of useful elements that
can be used for all conversion target, because they only generate text.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, types, time as time_, string

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
	<par>the time of the last modification of the file whose URL is in the attibute href
	as a text node.</par>
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): pass
		class format(xsc.TextAttr): pass

	def convert(self, converter):
		format = str(self.getAttr("format", "%d. %b. %Y, %H:%M").convert(converter))
		return xsc.Text(self["href"].convert(converter).lastmodified(root=converter.root).Format(format))

class time(xsc.Element):
	"""
	<par>the current time (i.e. the time when <pyref method="convert"><method>convert</method></pyref>
	is called). You can specify the format of the string in the attribute format, which is a
	<function>strftime</function> compatible string.</par>
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class format(xsc.TextAttr): pass

	def convert(self, converter):
		format = str(self.getAttr("format", "%d. %b. %Y, %H:%M").convert(converter))

		return xsc.Text(time_.strftime(format, time_.gmtime(time_.time())))

class x(xsc.Element):
	"""
	<par>element whose content will be ignored when converted:
	this can be used to comment out stuff. The content of the element must
	of course still be wellformed.</par>
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
		if self.hasattr("len"):
			text = self.text[:int(self["len"].convert(converter))]
		else:
			text = self.text
		return xsc.Text(text)

class wrap(xsc.Element):
	"""
	<par>a wrapper element that returns its content.
	This is e.g. useful if you want to parse a
	file that starts with <pyref module="ll.xist.ns.jsp"><module>&jsp;</module></pyref>
	processing instructions.</par>
	<par>This is also used for publishing, when <lit>xmlns</lit> attributes
	are required, but the root is not an element.</par>
	"""
	empty = False

	def convert(self, converter):
		return self.content.convert(converter)

# Control characters (not part of HTML)
class lf(xsc.CharRef): "line feed"; codepoint = 10
class cr(xsc.CharRef): "carriage return"; codepoint = 13
class tab(xsc.CharRef): "horizontal tab"; codepoint = 9
class esc(xsc.CharRef): "escape"; codepoint = 27

xmlns = xsc.Namespace("specials", "http://xmlns.livinglogic.de/xist/ns/specials", vars())

