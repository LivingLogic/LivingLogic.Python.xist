#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; module that contains the global attributes from
<app>Zope</app>s <z>Macro Expansion Template Attribute Language</z>.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc


class xmlns(xsc.Namespace):
	xmlname = "metal"
	xmlurl = "http://xml.zope.org/namespaces/metal"

	class Attrs(xsc.Namespace.Attrs):
		class define_macro(xsc.TextAttr): xmlname = "define-macro"
		class use_macro(xsc.TextAttr): xmlname = "use-macro"
		class define_slot(xsc.TextAttr): xmlname = "define-slot"
		class use_slot(xsc.TextAttr): xmlname = "use-slot"

xmlns.makemod(vars())
