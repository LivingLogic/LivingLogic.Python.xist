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
<doc:par>&xist; is an &xml; based extensible &html; generator written in Python.
&xist; is also a &dom; parser (built on top of &sax;2) with a very simple and
pythonesque tree &api;. Every &xml; element type corresponds to a Python class and these
Python classes provide a conversion method to transform the &xml; tree (e.g. into
&html;). &xist; can be considered <z>object oriented &xsl;</z>.</doc:par>

<doc:par>Some of the significant features of &xist; include:
<ulist>
<item>Easily extensible with new &xml; elements,</item>
<item>Can be used for offline or online page generation,</item>
<item>Allows embedding Python code in &xml; files,</item>
<item>Supports separation of layout and logic,</item>
<item>Can be used together with <a href="http://www.modpython.org/">mod_python</a>,
<a href="http://pywx.idyll.org/">PyWX</a> or <a href="http://webware.sourceforge.net/">Webware</a> to generate dynamic pages,</item>
<item>Fully supports Unicode,</item>
<item>Provides features to use &xist; together with &jsp;/struts,</item>
<item>Simplifies handling of deeply nested directory trees,</item>
<item>Automatically generates <code>HEIGHT</code> and <code>WIDTH</code> attributes for images.</item>
</ulist>
</doc:par>

<doc:par>&xist; was written as a replacement for the
<a href="http://www.giga.or.at/~agi/hsc/">&html; preprocessor HSC</a>,
and borrows some features and ideas from it.</doc:par>

<doc:par>It also borrows the basic ideas (&xml;/&html; elements as Python
objects) from
<a href="http://starship.python.net/crew/friedrich/HTMLgen/html/main.html">HTMLgen</a>
and <a href="http://dustman.net/andy/python/HyperText/">HyperText</a>.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

__all__ = ["xsc", "publishers", "presenters", "parsers", "converters", "ns"]


