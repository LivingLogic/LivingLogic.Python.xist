#! /usr/bin/env python

"""
A XSC module that contains definitions for all the elements in Ruby 1.0.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc

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
	empty = 0

class rbc(xsc.Element):
	"""
	The rbc (ruby base component) element is the container for rb elements.
	"""
	empty = 0

class rp(xsc.Element):
	"""
	The rp element is intended to contain parenthesis characters in simple ruby.
	"""
	empty = 0

class rt(xsc.Element):
	"""
	The rt element is the container for the ruby text.
	"""
	empty = 0
	attrHandlers = {"rbspan": xsc.TextAttr}

class rtc(xsc.Element):
	"""
	The rtc (ruby text component) element is the container for rt elements.
	"""
	empty = 0

class ruby(xsc.Element):
	"""
	The ruby element is an inline (or text-level) element that serves as the
	container for either the rb, rt and optional rp elements or the rbc and
	rtc elements.
	"""
	empty = 0

# register all the classes we've defined so far
namespace = xsc.Namespace("ruby", "http://www.w3.org/TR/ruby/xhtml11-ruby-1.mod", vars())
