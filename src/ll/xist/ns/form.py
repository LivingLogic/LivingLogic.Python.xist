#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<par>An &xist; module that contains elements that are useful for
forms. These are just abbreviations for the various
<lit>&lt;input type=<rep>...</rep>&gt;</lit> elements.</par>
"""

__version__ = "$Revision$".split()[1]
# $Source$

from ll.xist import xsc
from ll.xist.ns import html


xmlns = "http://xmlns.livinglogic.de/xist/ns/form"


class checkbox(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type=u"checkbox")
		return e.convert(converter)


class edit(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type=u"text")
		return e.convert(converter)


class radio(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type=u"radio")
		return e.convert(converter)


class submit(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type=u"submit")
		return e.convert(converter)


class memo(html.textarea):
	xmlns = xmlns
	class Attrs(html.textarea.Attrs):
		class value(xsc.TextAttr): pass

	def convert(self, converter):
		e = html.textarea(self[u"value"], self.attrs.withoutnames(u"value"))
		return e.convert(converter)


class hidden(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def __unicode__(self):
		return u""

	def convert(self, converter):
		e = html.input(self.attrs, type=u"hidden")
		return e.convert(converter)
