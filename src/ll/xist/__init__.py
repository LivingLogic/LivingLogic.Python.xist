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
XIST is an extensible HTML and XML generator. XIST is also a XML parser with a
very simple and pythonesque tree API. Every XML element type corresponds to a
Python class and these Python classes provide a conversion method to transform
the XML tree (e.g. into HTML). XIST can be considered 'object oriented XSLT'.

XIST was written as a replacement for the HTML preprocessor HSC__, and borrows
some features and ideas from it.

__ http://www.linguistik.uni-erlangen.de/~msbethke/software.html

It also borrows the basic ideas (XML/HTML elements as Python objects) from
HTMLgen_ and HyperText_.

.. _HTMLgen: http://starship.python.net/crew/friedrich/HTMLgen/html/main.html
.. _HyperText: http://dustman.net/andy/python/HyperText
"""


__docformat__ = "reStructuredText"


__all__ = ["xsc", "publishers", "presenters", "parsers", "converters", "sims", "xnd", "ns"]

