#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
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
<doc:par>This package contains all the modules that provide
<pyref module="xist.xsc" class="Namespace">namespace objects</pyref>
to &xist;. For example the definition of &html; can be found in the
module <pyref module="xist.ns.html"><module>xist.ns.html</module></pyref>.</doc:par>

<doc:par>Some of these namespaces can be considered target namespaces (e.g.
<pyref module="xist.ns.html"><module>html</module></pyref>,
<pyref module="xist.ns.chtml"><module>chtml</module></pyref>,
<pyref module="xist.ns.wml"><module>wml</module></pyref> and
<pyref module="xist.ns.docbook"><module>docbook</module></pyref>). The element and
entity classes in these namespaces don't implement a convert method, i.e. they inherit the
<pyref module="xist.xsc" class="Element" method="convert"><method>convert</method></pyref> method
from <pyref module="xist.xsc" class="Element"><class>Element</class></pyref>.</doc:par>

<doc:par>Other namespace modules provide additional functionality through
new element classes. Calling <pyref module="xist.xsc" class="Node" method="convert"><method>convert</method></pyref>
on these elements might convert them to one of these target namespaces
(depending on the <code>target</code> attribute of the
<pyref module="xist.converters" class="Converter"><class>Converter</class></pyref> object
passed around.) Some of these namespace modules completely ignore the target
and convert to one fixed target namespace (<pyref module="xist.ns.html"><module>html</module></pyref>
in most cases).</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

__all__ = [
	"html", "wml", "docbook", "ruby", "chtml",
	"jsp", "struts_html", "struts_config",
	"php",
	"specials", "abbr", "cond", "doc", "form", "meta"
]

