# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<p>An &xist; module that contains definitions for all the elements in Ruby 1.0.</p>
"""


from ll.xist import xsc, sims


__docformat__ = "xist"


xmlns = "http://www.w3.org/TR/ruby/xhtml-ruby-1.mod"


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
	xmlns = xmlns
	model = sims.NoElements()


class rbc(xsc.Element):
	"""
	The <class>rbc</class> (<z>ruby base component</z>) element is the container for <pyref class="rb"><class>rb</class></pyref> elements.
	"""
	xmlns = xmlns
	model = sims.Elements(rb)


class rp(xsc.Element):
	"""
	The <class>rp</class> element is intended to contain parenthesis characters in simple ruby.
	"""
	xmlns = xmlns
	model = sims.NoElements()


class rt(xsc.Element):
	"""
	The <class>rt</class> element is the container for the ruby text.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(xsc.Element.Attrs):
		class rbspan(xsc.TextAttr): pass


class rtc(xsc.Element):
	"""
	The <class>rtc</class> (<z>ruby text component</z>) element is the container for <pyref class="rt"><class>rt</class></pyref> elements.
	"""
	xmlns = xmlns
	model = sims.Elements(rt)


class ruby(xsc.Element):
	"""
	The <class>ruby</class> element is an inline (or text-level) element that serves as the
	container for either the <pyref class="rb"><class>rb</class></pyref>,
	<pyref class="rt"><class>rt</class></pyref> and optional
	<pyref class="rp><class>rp</class></pyref> elements or the
	<pyref class="rbc"><class>rbc</class></pyref> and <pyref class="irtc"><class>rtc</class></pyref> elements.
	"""
	xmlns = xmlns
	model = sims.Elements(rb, rt, rp, rbc, rtc)
