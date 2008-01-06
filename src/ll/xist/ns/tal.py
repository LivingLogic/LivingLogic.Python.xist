# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<p>An &xist; module that contains the global attributes from
<app>Zope</app>s <z>Template Attribute Language</z>.</p>
"""


from ll.xist import xsc


__docformat__ = "xist"


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
