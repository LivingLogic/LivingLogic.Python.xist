#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>A XSC module that contains definitions for all the elements in Ruby 1.0.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc


class DocTypeRuby10(xsc.DocType):
	"""
	document type for Ruby 1.0
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'ruby PUBLIC "-//W3C//ELEMENTS XHTML 1.1 Ruby 1.0//EN" "http://www.w3.org/TR/ruby/xhtml11-ruby-1.mod"')


class rb(xsc.Element):
	"""
	The <class>rb</class> element is the container for the text of the ruby base.
	"""
	empty = False


class rbc(xsc.Element):
	"""
	The <class>rbc</class> (<z>ruby base component</z>) element is the container for <pyref class="rb"><class>rb</class></pyref> elements.
	"""
	empty = False


class rp(xsc.Element):
	"""
	The <class>rp</class> element is intended to contain parenthesis characters in simple ruby.
	"""
	empty = False


class rt(xsc.Element):
	"""
	The <class>rt</class> element is the container for the ruby text.
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class rbspan(xsc.TextAttr): pass


class rtc(xsc.Element):
	"""
	The <class>rtc</class> (<z>ruby text component</z>) element is the container for <pyref class="rt"><class>rt</class></pyref> elements.
	"""
	empty = False


class ruby(xsc.Element):
	"""
	The <class>ruby</class> element is an inline (or text-level) element that serves as the
	container for either the <pyref class="rb"><class>rb</class></pyref>,
	<pyref class="rt"><class>rt</class></pyref> and optional
	<pyref class="rp><class>rp</class></pyref> elements or the
	<pyref class="rbc"><class>rbc</class></pyref> and <pyref class="irtc"><class>rtc</class></pyref> elements.
	"""
	empty = False


class xmlns(xsc.Namespace):
	xmlname = "ruby"
	xmlurl = "http://www.w3.org/TR/ruby/xhtml11-ruby-1.mod"

