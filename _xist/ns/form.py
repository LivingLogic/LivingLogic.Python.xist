#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; module that contains elements that are useful for
forms. These are just abbreviations for the various
<lit>&lt;input type=<rep>...</rep>&gt;</lit> elements.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc
from ll.xist.ns import html


class checkbox(html.input):
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type="checkbox")
		return e.convert(converter)


class edit(html.input):
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type="text")
		return e.convert(converter)


class radio(html.input):
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type="radio")
		return e.convert(converter)


class submit(html.input):
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type="submit")
		return e.convert(converter)


class memo(html.textarea):
	class Attrs(html.textarea.Attrs):
		class value(xsc.TextAttr): pass

	def convert(self, converter):
		e = html.textarea(self["value"], self.attr.without(["value"]))
		return e.convert(converter)


class hidden(html.input):
	class Attrs(html.input.Attrs):
		type = None

	def __unicode__(self):
		return u""

	def convert(self, converter):
		e = html.input(self.attrs, type="hidden")
		return e.convert(converter)


class xmlns(xsc.Namespace):
	xmlname = "form"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/form"
xmlns.makemod(vars())
