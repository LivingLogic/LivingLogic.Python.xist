#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
<doc:par>An &xist; module that contains a collection of useful elements for use
with &css;.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc
import css

class opacity(css.prop):
	"""
	<doc:par>Creates both an <pyref module="xist.ns.css" class="filter"><class>filter</class></pyref>
	and a <pyref module="xist.ns.css" class="_moz_opacity"><class>_moz_opacity</class></pyref>
	element for setting the opacity.</doc:par>
	"""

	def convert(self, converter):
		e = xsc.Frag(
			css.filter("alpha(opacity=", self.content, ")"),
			css._moz_opacity(self.content, "%")
		)
		return e.convert(converter)

class verdana(css.prop):
	"""
	<doc:par>Creates a <pyref module="xist.ns.css" class="font_family"><class>font_family</class></pyref>
	element which specifies <lit>Verdana</lit> as the font and uses several fall back fonts.</doc:par>
	"""

	def convert(self, converter):
		e = css.font_family('"Verdana", "Tahoma", "Arial", "XHelvetica", "Helvetica", sans-serif')
		return e.convert(converter)

class arialnarrow(css.prop):
	"""
	<doc:par>Creates a <pyref module="xist.ns.css" class="font_family"><class>font_family</class></pyref>
	element which specifies <lit>Arial Narrow</lit> as the font and uses several fall back fonts.</doc:par>
	"""

	def convert(self, converter):
		e = css.font_family('"Arial Narrow", "Tahoma", "Arial", "Verdana", "XHelvetica", "Helvetica", sans-serif;')
		return e.convert(converter)

class border_leftright(css.prop):
	"""
	<doc:par>Creates both an <pyref module="xist.ns.css" class="border_left"><class>border_left</class></pyref>
	and a <pyref module="xist.ns.css" class="border_right"><class>border_right</class></pyref>
	element.</doc:par>
	"""
	name = "border-leftright"

	def convert(self, converter):
		e = xsc.Frag(
			css.border_left(self.content),
			css.border_right(self.content)
		)
		return e.convert(converter)

class border_topbottom(css.prop):
	"""
	<doc:par>Creates both an <pyref module="xist.ns.css" class="border_top"><class>border_top</class></pyref>
	and a <pyref module="xist.ns.css" class="border_bottom"><class>border_bottom</class></pyref>
	element.</doc:par>
	"""
	name = "border-topbottom"

	def convert(self, converter):
		e = xsc.Frag(
			css.border_top(self.content),
			css.border_bottom(self.content)
		)
		return e.convert(converter)

class padding_leftright(css.prop):
	"""
	<doc:par>Creates both an <pyref module="xist.ns.css" class="padding_left"><class>padding_left</class></pyref>
	and a <pyref module="xist.ns.css" class="padding_right"><class>padding_right</class></pyref>
	element.</doc:par>
	"""
	name = "padding-leftright"

	def convert(self, converter):
		e = xsc.Frag(
			css.padding_left(self.content),
			css.padding_right(self.content)
		)
		return e.convert(converter)

class padding_topbottom(css.prop):
	"""
	<doc:par>Creates both an <pyref module="xist.ns.css" class="padding_top"><class>padding_top</class></pyref>
	and a <pyref module="xist.ns.css" class="padding_bottom"><class>padding_bottom</class></pyref>
	element.</doc:par>
	"""
	name = "padding-topbottom"

	def convert(self, converter):
		e = xsc.Frag(
			css.padding_top(self.content),
			css.padding_bottom(self.content)
		)
		return e.convert(converter)

class margin_leftright(css.prop):
	"""
	<doc:par>Creates both an <pyref module="xist.ns.css" class="margin_left"><class>margin_left</class></pyref>
	and a <pyref module="xist.ns.css" class="margin_right"><class>margin_right</class></pyref>
	element.</doc:par>
	"""
	name = "margin-leftright"

	def convert(self, converter):
		e = xsc.Frag(
			css.margin_left(self.content),
			css.margin_right(self.content)
		)
		return e.convert(converter)

class margin_topbottom(css.prop):
	"""
	<doc:par>Creates both an <pyref module="xist.ns.css" class="margin_top"><class>margin_top</class></pyref>
	and a <pyref module="xist.ns.css" class="margin_bottom"><class>margin_bottom</class></pyref>
	element.</doc:par>
	"""
	name = "margin-topbottom"

	def convert(self, converter):
		e = xsc.Frag(
			css.margin_top(self.content),
			css.margin_bottom(self.content)
		)
		return e.convert(converter)

namespace = xsc.Namespace("cssspecials", "http://xmlns.livinglogic.de/xist/cssspecials.dtd", vars())

