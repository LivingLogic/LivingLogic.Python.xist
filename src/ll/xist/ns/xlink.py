# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
Contains the global attributes for the xlink namespace
(``http://www.w3.org/1999/xlink``).
"""


from ll.xist import xsc


__docformat__ = "reStructuredText"


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
