#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; namespace that contains definitions for all the elements and
entities in <link href="http://www.w3.org/TR/html4/loose.dtd">&html; 4.0 transitional</link>
(and a few additional ones).</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import cgi # for parse_header

from ll.xist import xsc
from ll.xist.ns import html as html_

class html(html_.html):
	def fixcharacters(self, node, converter):
		if isinstance(node, xsc.Text):
			node = node.replace(unichr(html_.mdash.codepoint), u"--")
			node = node.replace(unichr(html_.ndash.codepoint), u"-")
			node = node.replace(u"\u200b", u"")
			node = node.replace(unichr(html_.Alpha.codepoint), u"Alpha")
			node = node.replace(unichr(html_.Beta.codepoint), u"Beta")
			node = node.replace(unichr(html_.Gamma.codepoint), u"Gamma")
			node = node.replace(unichr(html_.alpha.codepoint), u"alpha")
			node = node.replace(unichr(html_.beta.codepoint), u"beta")
			node = node.replace(unichr(html_.gamma.codepoint), u"gamma")
		return node

	def convert(self, converter):
		e = html_.html(self.content.convert(converter), self.attrs.convert(converter))
		e = e.mapped(self.fixcharacters, converter)
		return e

class HeaderFormattingMixin(object):
	abovetext = None
	belowtext = None

	def convert(self, converter):
		target = converter.target
		content = unicode(self.content.convert(converter))
		l = len(content)
		if self.abovetext:
			abovetext = ((self.abovetext*l)[:l], target.br())
		else:
			abovetext = None
		if self.belowtext:
			belowtext = ((self.belowtext*l)[:l], target.br())
		else:
			belowtext = None
		e = self.base(
			target.br(),
			abovetext,
			self.content, target.br(),
			belowtext
		)
		return e.convert(converter)

class h1(HeaderFormattingMixin, html_.h1):
	abovetext = "#"
	belowtext = "#"
	base = html_.h1

class h2(HeaderFormattingMixin, html_.h2):
	abovetext = "="
	belowtext = "="
	base = html_.h2

class h3(HeaderFormattingMixin, html_.h3):
	abovetext = "-"
	belowtext = "-"
	base = html_.h3

class h4(HeaderFormattingMixin, html_.h4):
	belowtext = "#"
	base = html_.h4

class h5(HeaderFormattingMixin, html_.h5):
	belowtext = "="
	base = html_.h5

class h6(HeaderFormattingMixin, html_.h6):
	belowtext = "-"
	base = html_.h6

class xmlns(html_):
	xmlname = "text"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/text"
xmlns.makemod(vars())
