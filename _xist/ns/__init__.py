#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>This package contains all the modules that provide
<pyref module="ll.xist.xsc" class="Namespace">namespace objects</pyref>
to &xist;. For example the definition of &html; can be found in the
module <pyref module="ll.xist.ns.html"><module>xist.ns.html</module></pyref>.</par>

<par>Some of these namespaces can be considered target namespaces (e.g.
<pyref module="ll.xist.ns.html"><module>html</module></pyref>,
<pyref module="ll.xist.ns.ihtml"><module>ihtml</module></pyref>,
<pyref module="ll.xist.ns.wml"><module>wml</module></pyref> and
<pyref module="ll.xist.ns.docbook"><module>docbook</module></pyref>). The element and
entity classes in these namespaces don't implement a convert method, i.e. they inherit the
<pyref module="ll.xist.xsc" class="Element" method="convert"><method>convert</method></pyref> method
from <pyref module="ll.xist.xsc" class="Element"><class>Element</class></pyref>.</par>

<par>Other namespace modules provide additional functionality through
new element classes. Calling <pyref module="ll.xist.xsc" class="Node" method="convert"><method>convert</method></pyref>
on these elements might convert them to one of these target namespaces
(depending on the <lit>target</lit> attribute of the
<pyref module="ll.xist.converters" class="Converter"><class>Converter</class></pyref> object
passed around.) Some of these namespace modules completely ignore the target
and convert to one fixed target namespace (<pyref module="ll.xist.ns.html"><module>html</module></pyref>
in most cases).</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

__all__ = [
	"xml",
	"html", "wml", "docbook", "ruby", "ihtml", "svg",
	"jsp", "struts_html", "struts_config",
	"php",
	"specials", "abbr", "cond", "code", "doc", "form", "meta",
	"css", "cssspecials"
]

