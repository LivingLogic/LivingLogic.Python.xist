# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
## THE SOFTWARE.


"""
<p>&xist; is an extensible &html; and &xml; generator written in Python.
&xist; is also a &dom; parser (built on top of &sax;2) with a very simple and
pythonesque tree &api;. Every &xml; element type corresponds to a Python class and these
Python classes provide a conversion method to transform the &xml; tree (e.g. into
&html;). &xist; can be considered <z>object oriented &xslt;</z>.</p>

<p>Some of the significant features of &xist; include:</p>
<ul>
<item>Easily extensible with new &xml; elements,</item>
<item>Can be used for offline or online page generation,</item>
<item>Allows embedding Python code in &xml; files,</item>
<item>Supports separation of layout and logic,</item>
<item>Can be used together with <a href="http://www.modpython.org/">mod_python</a>,
<a href="http://pywx.idyll.org/">PyWX</a> or <a href="http://webware.sf.net/">Webware</a>
to generate dynamic pages,</item>
<item>Fully supports Unicode and &xml; namespaces,</item>
<item>Provides features to use &xist; together with &jsp;/Struts (when replacing
Struts tag libraries with &xist; this speeds up pages by a factor of 5&ndash;10.)</item>
</ul>

<p>&xist; was written as a replacement for the
<a href="http://www.linguistik.uni-erlangen.de/~msbethke/software.html">&html; preprocessor &hsc;</a>,
and borrows some features and ideas from it.</p>

<p>It also borrows the basic ideas (&xml;/&html; elements as Python
objects) from
<a href="http://starship.python.net/crew/friedrich/HTMLgen/html/main.html">HTMLgen</a>
and <a href="http://dustman.net/andy/python/HyperText/">HyperText</a>.</p>
"""


__docformat__ = "xist"


__all__ = ["xsc", "publishers", "presenters", "parsers", "converters", "sims", "xnd", "ns"]

