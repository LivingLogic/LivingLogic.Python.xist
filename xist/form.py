#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of Living Logic AG or
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
A XSC module that contains elements that are useful for
forms. These are just abbreviations for the various
<code>&lt;input type=<var>...</var>&gt;</code> elements.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import xsc, html

class checkbox(xsc.Element):
	attrHandlers = {"name": xsc.TextAttr, "value": xsc.TextAttr}

	def transform(self, transformer=None):
		e = html.input(**self.attrs)
		e["type"] = "checkbox"
		if self.hasAttr("value") and int(self["value"].asPlainString()) != 0:
			e["checked"] = None
		else:
			del e["checked"]
		return e.transform(transformer)

class edit(xsc.Element):
	attrHandlers = {"name": xsc.TextAttr, "value": xsc.TextAttr, "size": xsc.TextAttr}

	def transform(self, transformer=None):
		e = html.input(**self.attrs)
		return e.transform(transformer)

class memo(xsc.Element):
	attrHandlers = {"name": xsc.TextAttr, "value": xsc.TextAttr}
	attrHandlers.update(html.textarea.attrHandlers)

	def transform(self, transformer=None):
		e = html.textarea()
		if self.hasAttr("value"):
			e.extend(self["value"])
		for attr in self.attrs.keys():
			if attr != "value":
				e[attr] = self[attr]
		return e.transform(transformer)

class hidden(xsc.Element):
	attrHandlers = {"name": xsc.TextAttr, "value": xsc.TextAttr}

	def asPlainString(self):
		return u""

	def transform(self, transformer=None):
		e = html.input(type="hidden", name=self["name"])
		if self.hasAttr("value"):
			e["value"] = self["value"]
		return e.transform(transformer)

namespace = xsc.Namespace("form", "http://www.livinglogic.de/DTDs/form.dtd", vars())
