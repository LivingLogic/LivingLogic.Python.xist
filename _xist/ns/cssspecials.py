#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; module that contains a collection of useful elements for use
with &css;.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc
import css


class opacity(css.prop):
	"""
	<par>Creates both an <pyref module="ll.xist.ns.css" class="filter"><class>filter</class></pyref>
	and a <pyref module="ll.xist.ns.css" class="_moz_opacity"><class>_moz_opacity</class></pyref>
	element for setting the opacity.</par>
	"""

	def convert(self, converter):
		e = xsc.Frag(
			css.filter(u"alpha(opacity=", self.content, u")"),
			css._moz_opacity(self.content, u"%")
		)
		return e.convert(converter)


class verdana(css.prop):
	"""
	<par>Creates a <pyref module="ll.xist.ns.css" class="font_family"><class>font_family</class></pyref>
	element which specifies <lit>Verdana</lit> as the font and uses several fall back fonts.</par>
	"""

	def convert(self, converter):
		e = css.font_family(u'"Verdana", "Tahoma", "Arial", "XHelvetica", "Helvetica", sans-serif')
		return e.convert(converter)


class arialnarrow(css.prop):
	"""
	<par>Creates a <pyref module="ll.xist.ns.css" class="font_family"><class>font_family</class></pyref>
	element which specifies <lit>Arial Narrow</lit> as the font and uses several fall back fonts.</par>
	"""

	def convert(self, converter):
		e = css.font_family(u'"Arial Narrow", "Tahoma", "Arial", "Verdana", "XHelvetica", "Helvetica", sans-serif')
		return e.convert(converter)


class border_leftright(css.prop):
	"""
	<par>Creates both an <pyref module="ll.xist.ns.css" class="border_left"><class>border_left</class></pyref>
	and a <pyref module="ll.xist.ns.css" class="border_right"><class>border_right</class></pyref>
	element.</par>
	"""
	xmlname = "border-leftright"

	def convert(self, converter):
		e = xsc.Frag(
			css.border_left(self.content),
			css.border_right(self.content)
		)
		return e.convert(converter)


class border_topbottom(css.prop):
	"""
	<par>Creates both an <pyref module="ll.xist.ns.css" class="border_top"><class>border_top</class></pyref>
	and a <pyref module="ll.xist.ns.css" class="border_bottom"><class>border_bottom</class></pyref>
	element.</par>
	"""
	xmlname = "border-topbottom"

	def convert(self, converter):
		e = xsc.Frag(
			css.border_top(self.content),
			css.border_bottom(self.content)
		)
		return e.convert(converter)


class padding_leftright(css.prop):
	"""
	<par>Creates both an <pyref module="ll.xist.ns.css" class="padding_left"><class>padding_left</class></pyref>
	and a <pyref module="ll.xist.ns.css" class="padding_right"><class>padding_right</class></pyref>
	element.</par>
	"""
	xmlname = "padding-leftright"

	def convert(self, converter):
		e = xsc.Frag(
			css.padding_left(self.content),
			css.padding_right(self.content)
		)
		return e.convert(converter)


class padding_topbottom(css.prop):
	"""
	<par>Creates both an <pyref module="ll.xist.ns.css" class="padding_top"><class>padding_top</class></pyref>
	and a <pyref module="ll.xist.ns.css" class="padding_bottom"><class>padding_bottom</class></pyref>
	element.</par>
	"""
	xmlname = "padding-topbottom"

	def convert(self, converter):
		e = xsc.Frag(
			css.padding_top(self.content),
			css.padding_bottom(self.content)
		)
		return e.convert(converter)


class margin_leftright(css.prop):
	"""
	<par>Creates both an <pyref module="ll.xist.ns.css" class="margin_left"><class>margin_left</class></pyref>
	and a <pyref module="ll.xist.ns.css" class="margin_right"><class>margin_right</class></pyref>
	element.</par>
	"""
	xmlname = "margin-leftright"

	def convert(self, converter):
		e = xsc.Frag(
			css.margin_left(self.content),
			css.margin_right(self.content)
		)
		return e.convert(converter)


class margin_topbottom(css.prop):
	"""
	<par>Creates both an <pyref module="ll.xist.ns.css" class="margin_top"><class>margin_top</class></pyref>
	and a <pyref module="ll.xist.ns.css" class="margin_bottom"><class>margin_bottom</class></pyref>
	element.</par>
	"""
	xmlname = "margin-topbottom"

	def convert(self, converter):
		e = xsc.Frag(
			css.margin_top(self.content),
			css.margin_bottom(self.content)
		)
		return e.convert(converter)


class xmlns(xsc.Namespace):
	xmlname = "cssspecials"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/cssspecials"
xmlns.makemod(vars())

