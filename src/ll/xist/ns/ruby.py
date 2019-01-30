# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST module that contains definitions for all the elements in Ruby 1.0.
"""


from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://www.w3.org/TR/ruby/xhtml-ruby-1.mod"


class DocTypeRuby10(xsc.DocType):
	"""
	document type for Ruby 1.0
	"""

	def __init__(self):
		xsc.DocType.__init__(self, 'ruby PUBLIC "-//W3C//ELEMENTS XHTML 1.1 Ruby 1.0//EN" "http://www.w3.org/TR/ruby/xhtml11-ruby-1.mod"')


class rb(xsc.Element):
	"""
	The :class:`rb` element is the container for the text of the ruby base.
	"""
	xmlns = xmlns
	model = sims.NoElements()


class rbc(xsc.Element):
	"""
	The :class:`rbc` (ruby base component) element is the container for
	:class:`rb` elements.
	"""
	xmlns = xmlns
	model = sims.Elements(rb)


class rp(xsc.Element):
	"""
	The :class:`rp` element is intended to contain parenthesis characters in
	simple ruby.
	"""
	xmlns = xmlns
	model = sims.NoElements()


class rt(xsc.Element):
	"""
	The :class:`rt` element is the container for the ruby text.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(xsc.Element.Attrs):
		class rbspan(xsc.TextAttr): pass


class rtc(xsc.Element):
	"""
	The :class:`rtc` ("ruby text component") element is the container for
	:class:`rt` elements.
	"""
	xmlns = xmlns
	model = sims.Elements(rt)


class ruby(xsc.Element):
	"""
	The :class:`ruby` element is an inline (or text-level) element that serves
	as the container for either the :class:`rb`, :class:`rt` and optional
	:class:`rp` elements or the :class:`rbc` and :class:`rtc` elements.
	"""
	xmlns = xmlns
	model = sims.Elements(rb, rt, rp, rbc, rtc)
