#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; module that contains the global attributes from
<app>Zope</app>s <z>Template Attribute Language</z>.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc


class __ns__(xsc.Namespace):
	xmlname = "tal"
	xmlurl = "http://xml.zope.org/namespaces/tal"

	class Attrs(xsc.Namespace.Attrs):
		class define(xsc.TextAttr): pass
		class attributes(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class replace(xsc.TextAttr): pass
		class repeat(xsc.TextAttr): pass
		class on_error(xsc.TextAttr): xmlname = "on-error"
		class omit_tag(xsc.TextAttr): xmlname = "omit-tag"

__ns__.makemod(vars())
