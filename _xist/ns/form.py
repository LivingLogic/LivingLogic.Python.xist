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
<doc:par>An &xist; module that contains elements that are useful for
forms. These are just abbreviations for the various
<lit>&lt;input type=<rep>...</rep>&gt;</lit> elements.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc
import html

class checkbox(html.input):
	attrHandlers = html.input.attrHandlers.copy()
	del attrHandlers["type"]

	def convert(self, converter):
		e = html.input(self.attrs, type="checkbox")
		if self.hasAttr("value") and int(self["value"]) != 0:
			e["checked"] = None
		else:
			del e["checked"]
		return e.convert(converter)

class edit(html.input):
	attrHandlers = html.input.attrHandlers.copy()
	del attrHandlers["type"]

	def convert(self, converter):
		e = html.input(self.attrs, type="text")
		return e.convert(converter)

class radio(html.input):
	attrHandlers = html.input.attrHandlers.copy()
	del attrHandlers["type"]

	def convert(self, converter):
		e = html.input(self.attrs, type="radio")
		return e.convert(converter)

class submit(html.input):
	attrHandlers = html.input.attrHandlers.copy()
	del attrHandlers["type"]

	def convert(self, converter):
		e = html.input(self.attrs, type="submit")
		return e.convert(converter)

class memo(html.textarea):
	empty = 1
	attrHandlers = html.textarea.attrHandlers.copy()
	attrHandlers["value"] = xsc.TextAttr

	def convert(self, converter):
		e = html.textarea(self["value"], self.attr.without(["value"]))
		return e.convert(converter)

class hidden(html.input):
	attrHandlers = html.input.attrHandlers.copy()
	del attrHandlers["type"]

	def __unicode__(self):
		return u""

	def convert(self, converter):
		e = html.input(self.attrs(), type="hidden")
		return e.convert(converter)

namespace = xsc.Namespace("form", "http://xmlns.livinglogic.de/xist/ns/form", vars())
