#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
(depending on the <code>target</code> attribute of the
<pyref module="ll.xist.converters" class="Converter"><class>Converter</class></pyref> object
passed around.) Some of these namespace modules completely ignore the target
and convert to one fixed target namespace (<pyref module="ll.xist.ns.html"><module>html</module></pyref>
in most cases).</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

__all__ = [
	"xml",
	"html", "wml", "docbook", "ruby", "ihtml",
	"jsp", "struts_html", "struts_config", "struts_config11",
	"php",
	"specials", "abbr", "cond", "code", "doc", "form", "meta",
	"css", "cssspecials"
]

