# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
An XIST module that contains the global attributes from Zopes "Macro Expansion
Template Attribute Language".
"""


from ll.xist import xsc


__docformat__ = "reStructuredText"


xmlns = "http://xml.zope.org/namespaces/metal"


class Attrs(xsc.Attrs):
	class define_macro(xsc.TextAttr):
		xmlns = xmlns
		xmlname = "define-macro"

	class use_macro(xsc.TextAttr):
		xmlns = xmlns
		xmlname = "use-macro"

	class define_slot(xsc.TextAttr):
		xmlns = xmlns
		xmlname = "define-slot"

	class use_slot(xsc.TextAttr):
		xmlns = xmlns
		xmlname = "use-slot"
