# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This XIST module contains convenience classes for form elements. These are
just abbreviations for the various ``<input type="...">`` elements.
"""


from ll.xist import xsc
from ll.xist.ns import html


__docformat__ = "reStructuredText"


xmlns = "http://xmlns.livinglogic.de/xist/ns/form"


class text(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type="text")
		return e.convert(converter)


class checkbox(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type="checkbox")
		return e.convert(converter)


class radio(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type="radio")
		return e.convert(converter)


class file(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type="file")
		return e.convert(converter)


class submit(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type="submit")
		return e.convert(converter)


class button(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def convert(self, converter):
		e = html.input(self.attrs, type="button")
		return e.convert(converter)


class textarea(html.textarea):
	xmlns = xmlns
	class Attrs(html.textarea.Attrs):
		class value(xsc.TextAttr): pass

	def convert(self, converter):
		e = html.textarea(self.attrs.value, self.attrs.withoutnames("value"))
		return e.convert(converter)


class hidden(html.input):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		type = None

	def __str__(self):
		return ""

	def convert(self, converter):
		e = html.input(self.attrs, type="hidden")
		return e.convert(converter)
