#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>Contains the global attributes for the xlink namespace
(<lit>http://www.w3.org/1999/xlink</lit>).</par>
"""

__version__ = "$Revision$".split()[1]
# $Source$

from ll.xist import xsc, utils


xmlns  = "http://www.w3.org/1999/xlink"


class Attrs(xsc.Attrs):
	class type(xsc.TextAttr):
		xmlns = xmlns
		values = (u"simple", u"extended", u"locator", u"arc", u"resource", u"title")

	class href(xsc.URLAttr):
		xmlns = xmlns

	class role(xsc.URLAttr):
		xmlns = xmlns

	class arcrole(xsc.URLAttr):
		xmlns = xmlns

	class title(xsc.TextAttr):
		xmlns = xmlns

	class show(xsc.TextAttr):
		xmlns = xmlns
		values = (u"new", u"replace", u"embed", u"other", u"none")

	class label(xsc.TextAttr):
		xmlns = xmlns

	class actuate(xsc.TextAttr):
		xmlns = xmlns
		values = (u"onLoad", u"onRequest", u"other", u"none")

	class from_(xsc.TextAttr):
		xmlns = xmlns
		xmlname = "from"

	class to(xsc.TextAttr):
		xmlns = xmlns
