#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
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


class __ns__(xsc.Namespace):
	xmlname = "xlink"
	xmlurl  = "http://www.w3.org/1999/xlink"

	class Attrs(xsc.Namespace.Attrs):
		class type(xsc.TextAttr): values = (u"simple", u"extended", u"locator", u"arc", u"resource", u"title")
		class href(xsc.URLAttr): pass
		class role(xsc.URLAttr): pass
		class arcrole(xsc.URLAttr): pass
		class title(xsc.TextAttr): pass
		class show(xsc.TextAttr): values = (u"new", u"replace", u"embed", u"other", u"none")
		class label(xsc.TextAttr): pass
		class actuate(xsc.TextAttr): values = (u"onLoad", u"onRequest", u"other", u"none")
		class from_(xsc.TextAttr): xmlname = "from"
		class to(xsc.TextAttr): pass
__ns__.makemod(vars())
