#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>Contains the global attributes for the xlink namespace
(<lit>http://www.w3.org/1999/xlink</lit>).</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc, utils

class xmlns(xsc.Namespace):
	xmlname = "xlink"
	xmlurl  = "http://www.w3.org/1999/xlink"

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
xmlns.makemod(vars())
