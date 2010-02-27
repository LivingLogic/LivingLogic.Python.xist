# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


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

