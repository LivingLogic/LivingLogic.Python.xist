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
	The rb element is the container for the text of the ruby base.
	"""
	empty = False

class rbc(xsc.Element):
	"""
	The rbc (ruby base component) element is the container for rb elements.
	"""
	empty = False

class rp(xsc.Element):
	"""
	The rp element is intended to contain parenthesis characters in simple ruby.
	"""
	empty = False

class rt(xsc.Element):
	"""
	The rt element is the container for the ruby text.
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class rbspan(xsc.TextAttr): pass

class rtc(xsc.Element):
	"""
	The rtc (ruby text component) element is the container for rt elements.
	"""
	empty = False

class ruby(xsc.Element):
	"""
	The ruby element is an inline (or text-level) element that serves as the
	container for either the rb, rt and optional rp elements or the rbc and
	rtc elements.
	"""
	empty = False

class xmlns(xsc.Namespace):
	xmlname = "ruby"
	xmlurl = "http://www.w3.org/TR/ruby/xhtml11-ruby-1.mod"

