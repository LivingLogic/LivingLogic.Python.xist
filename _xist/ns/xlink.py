#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
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
<doc:par>Contains the global attributes for the xlink namespace
(<lit>http://www.w3.org/1999/xlink</lit>).</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc, utils

class Namespace(xsc.Namespace):
	class Attrs(xsc.Namespace.Attrs):
		class type(xsc.NamespaceAttrMixIn, xsc.TextAttr):
			values = ("simple", "extended", "locator", "arc", "resource", "title")
		class href(xsc.NamespaceAttrMixIn, xsc.URLAttr):
			pass
		class role(xsc.NamespaceAttrMixIn, xsc.URLAttr):
			pass
		class arcrole(xsc.NamespaceAttrMixIn, xsc.URLAttr):
			pass
		class title(xsc.NamespaceAttrMixIn, xsc.TextAttr):
			pass
		class show(xsc.NamespaceAttrMixIn, xsc.TextAttr):
			values = ("new", "replace", "embed", "other", "none")
		class label(xsc.NamespaceAttrMixIn, xsc.TextAttr):
			pass
		class actuate(xsc.NamespaceAttrMixIn, xsc.TextAttr):
			values = ("onLoad", "onRequest", "other", "none")
		class from_(xsc.NamespaceAttrMixIn, xsc.TextAttr):
			xmlname = "from"
		class to(xsc.NamespaceAttrMixIn, xsc.TextAttr):
			pass

	def __init__(self, vars):
		xsc.Namespace.__init__(self, "xlink", "http://www.w3.org/1999/xlink", vars)

xmlns = Namespace(vars())

