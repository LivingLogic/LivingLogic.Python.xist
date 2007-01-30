#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; namespace that contains definitions for all the elements and
entities in <link href="http://www.w3.org/TR/html4/loose.dtd">&html; 4.0 transitional</link>
(and a few additional ones).</par>
"""

__version__ = "$Revision$".split()[1]
# $Source$

import cgi # for parse_header

from ll.xist import xsc
from ll.xist.ns import html as html_, chars


xmlns = "http://xmlns.livinglogic.de/xist/ns/text"


class html(html_.html):
	xmlns = xmlns
	def fixcharacters(self, node, converter):
		if isinstance(node, xsc.Text):
			node = node.replace(unichr(chars.mdash.codepoint), u"--")
			node = node.replace(unichr(chars.ndash.codepoint), u"-")
			node = node.replace(u"\u200b", u"")
			node = node.replace(unichr(chars.Alpha.codepoint), u"Alpha")
			node = node.replace(unichr(chars.Beta.codepoint), u"Beta")
			node = node.replace(unichr(chars.Gamma.codepoint), u"Gamma")
			node = node.replace(unichr(chars.alpha.codepoint), u"alpha")
			node = node.replace(unichr(chars.beta.codepoint), u"beta")
			node = node.replace(unichr(chars.gamma.codepoint), u"gamma")
		return node

	def convert(self, converter):
		e = html_.html(self.content.convert(converter), self.attrs.convert(converter))
		e = e.mapped(self.fixcharacters, converter)
		return e


class HeaderFormattingMixin(object):
	underline = None

	def convert(self, converter):
		target = converter.target
		content = unicode(self.content.convert(converter))
		l = len(content)
		if self.underline:
			underline = ((self.underline*l)[:l], target.br())
		else:
			underline = None
		e = self.base(
			target.br(),
			self.content, target.br(),
			underline
		)
		return e.convert(converter)


class h1(HeaderFormattingMixin, html_.h1):
	xmlns = xmlns
	underline = u"="
	base = html_.h1


class h2(HeaderFormattingMixin, html_.h2):
	xmlns = xmlns
	underline = u"="
	base = html_.h2


class h3(HeaderFormattingMixin, html_.h3):
	xmlns = xmlns
	underline = u"-"
	base = html_.h3


class h4(HeaderFormattingMixin, html_.h4):
	xmlns = xmlns
	underline = u"-"
	base = html_.h4


class h5(HeaderFormattingMixin, html_.h5):
	xmlns = xmlns
	underline = u"-"
	base = html_.h5


class h6(HeaderFormattingMixin, html_.h6):
	xmlns = xmlns
	underline = u"-"
	base = html_.h6
