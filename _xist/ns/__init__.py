#! /usr/bin/env python

"""
<doc:par>This package contains all the modules that provide 
<pyref module="xist.xsc" class="Namespace">namespace objects</pyref>
to &xist;. For example the definition of &html; can 
be found in the module <pyref module="xist.ns.html">xist.ns.html</pyref>.</doc:par>

<doc:par>Some of these namespaces can be considered target namespaces (e.g.
<pyref module="xist.ns.html">html</pyref>, <pyref module="xist.ns.wml">wml</pyref> and
<pyref module="xist.ns.docbook">docbook</pyref>). The element and entity classes
in these namespaces don't implement a convert method, i.e. they inherit the
<pyref module="xist.xsc" class="Element" method="convert">convert</pyref> method
from <pyref module="xist.xsc" class="Element">Element</pyref>.</doc:par>

<doc:par>Other namespace modules provide additional functionality through
new element classes. Calling <pyref module="xist.xsc" class="Node" method="convert">convert</pyref>
on these elements might convert them to one of these target namespaces
(probably dependent on the <pyref module="xist.converters" class="Converter" method="__init__" arg="target">target</pyref>
element of the <pyref module="xist.converters" class="Converter">Converter</pyref> object
passed around.) Some of these namespace modules completely ignore the target
and convert to one fixed target namespace (<pyref module="xist.ns.html">html</pyref> in
most cases).</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

__all__ = [
	"html", "wml", "docbook", "ruby",
	"jsp", "struts_html", "struts_config",
	"php",
	"specials", "abbr", "cond", "doc", "form", "meta"
]

