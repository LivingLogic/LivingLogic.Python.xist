# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Contains the global attributes for the xlink namespace
(``http://www.w3.org/1999/xlink``).
"""


from ll.xist import xsc


__docformat__ = "reStructuredText"


xmlns = "http://www.w3.org/1999/xlink"


class Attrs(xsc.Attrs):
	xmlns = xmlns

	class type(xsc.TextAttr):
		xmlns = xmlns
		values = ("simple", "extended", "locator", "arc", "resource", "title")

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
		values = ("new", "replace", "embed", "other", "none")

	class label(xsc.TextAttr):
		xmlns = xmlns

	class actuate(xsc.TextAttr):
		xmlns = xmlns
		values = ("onLoad", "onRequest", "other", "none")

	class from_(xsc.TextAttr):
		xmlns = xmlns
		xmlname = "from"

	class to(xsc.TextAttr):
		xmlns = xmlns
