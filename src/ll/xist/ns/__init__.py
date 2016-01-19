# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This package contains all the modules that provide namespaces to to XIST.
For example the definition of HTML can be found in the module
:mod:`ll.xist.ns.html`.

Some of these namespaces can be considered target namespaces (e.g.
:mod:`ll.xist.ns.html`, :mod:`ll.xist.ns.ihtml`,:mod:`ll.xist.ns.wml` and
:mod:`ll.xist.ns.docbook`). The element and entity classes in these namespaces
don't implement a convert method, i.e. they inherit the :meth:`convert` method
from :class:`ll.xist.xsc.Element.convert`.

Other namespace modules provide additional functionality through new element
classes. Calling :meth:`ll.xist.xsc.Node.convert` on these elements might
convert them to one of these target namespaces (depending on the :attr:`target`
attribute of the :class:`ll.xist.xsc.Converter` object passed around.) Some of
these namespace modules completely ignore the target and convert to one
fixed target namespace (:mod:`ll.xist.ns.html` in most cases).
"""


__docformat__ = "reStructuredText"


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
