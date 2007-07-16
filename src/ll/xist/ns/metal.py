#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<par>An &xist; module that contains the global attributes from
<app>Zope</app>s <z>Macro Expansion Template Attribute Language</z>.</par>
"""

__version__ = "$Revision$".split()[1]
# $Source$

from ll.xist import xsc


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
