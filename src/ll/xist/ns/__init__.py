# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<p>This package contains all the modules that provide namespaces to
to &xist;. For example the definition of &html; can be found in the
module <pyref module="ll.xist.ns.html"><mod>xist.ns.html</mod></pyref>.</p>

<p>Some of these namespaces can be considered target namespaces (e.g.
<pyref module="ll.xist.ns.html"><mod>html</mod></pyref>,
<pyref module="ll.xist.ns.ihtml"><mod>ihtml</mod></pyref>,
<pyref module="ll.xist.ns.wml"><mod>wml</mod></pyref> and
<pyref module="ll.xist.ns.docbook"><mod>docbook</mod></pyref>). The element and
entity classes in these namespaces don't implement a convert method, i.e. they inherit the
<pyref module="ll.xist.xsc" class="Element" method="convert"><meth>convert</meth></pyref> method
from <pyref module="ll.xist.xsc" class="Element"><class>Element</class></pyref>.</p>

<p>Other namespace modules provide additional functionality through
new element classes. Calling <pyref module="ll.xist.xsc" class="Node" method="convert"><meth>convert</meth></pyref>
on these elements might convert them to one of these target namespaces
(depending on the <lit>target</lit> attribute of the
<pyref module="ll.xist.converters" class="Converter"><class>Converter</class></pyref> object
passed around.) Some of these namespace modules completely ignore the target
and convert to one fixed target namespace (<pyref module="ll.xist.ns.html"><mod>html</mod></pyref>
in most cases).</p>
"""


__docformat__ = "xist"


__all__ = [
	"abbr",
	"chars",
	"code",
	"cond",
	"css",
	"cssspecials",
	"docbook",
	"doc",
	"fo",
	"form",
	"html",
	"htmlspecials",
	"ihtml",
	"jsp",
	"metal",
	"meta",
	"php",
	"rng",
	"ruby",
	"specials",
	"struts_config",
	"struts_html",
	"svg",
	"tal",
	"text",
	"tld",
	"wml",
	"xlink",
	"xml"
]

