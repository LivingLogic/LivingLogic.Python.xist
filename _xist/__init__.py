#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>&xist; is an &xml; based extensible &html; generator written in Python.
&xist; is also a &dom; parser (built on top of &sax;2) with a very simple and
pythonesque tree &api;. Every &xml; element type corresponds to a Python class and these
Python classes provide a conversion method to transform the &xml; tree (e.g. into
&html;). &xist; can be considered <z>object oriented &xsl;</z>.</par>

<par>Some of the significant features of &xist; include:</par>
<ulist>
<item>Easily extensible with new &xml; elements,</item>
<item>Can be used for offline or online page generation,</item>
<item>Allows embedding Python code in &xml; files,</item>
<item>Supports separation of layout and logic,</item>
<item>Can be used together with <link href="http://www.modpython.org/">mod_python</link>,
<link href="http://pywx.idyll.org/">PyWX</link> or <link href="http://webware.sf.net/">Webware</link>
to generate dynamic pages,</item>
<item>Fully supports Unicode and &xml; namespaces,</item>
<item>Provides features to use &xist; together with &jsp;/Struts (when replacing
Struts tag libraries with &xist; this speeds up pages by a factor of 5&ndash;10.)</item>
</ulist>

<par>&xist; was written as a replacement for the
<link href="http://www.giga.or.at/~agi/hsc/">&html; preprocessor &hsc;</link>,
and borrows some features and ideas from it.</par>

<par>It also borrows the basic ideas (&xml;/&html; elements as Python
objects) from
<link href="http://starship.python.net/crew/friedrich/HTMLgen/html/main.html">HTMLgen</link>
and <link href="http://dustman.net/andy/python/HyperText/">HyperText</link>.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

__all__ = ["xsc", "publishers", "presenters", "parsers", "converters", "ns"]

