# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST module that contains the global attributes from Zopes
"Template Attribute Language".
"""


from ll.xist import xsc


__docformat__ = "reStructuredText"


xmlns = "http://xml.zope.org/namespaces/tal"


class Attrs(xsc.Attrs):
	class define(xsc.TextAttr):
		xmlns = xmlns

	class attributes(xsc.TextAttr):
		xmlns = xmlns

	class condition(xsc.TextAttr):
		xmlns = xmlns

	class replace(xsc.TextAttr):
		xmlns = xmlns

	class repeat(xsc.TextAttr):
		xmlns = xmlns

	class on_error(xsc.TextAttr):
		xmlns = xmlns
		xmlname = "on-error"

	class omit_tag(xsc.TextAttr):
		xmlns = xmlns
		xmlname = "omit-tag"
