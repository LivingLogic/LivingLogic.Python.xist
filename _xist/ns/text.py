#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; namespace that contains definitions for all the elements and
entities in <link href="http://www.w3.org/TR/html4/loose.dtd">&html; 4.0 transitional</link>
(and a few additional ones).</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import cgi # for parse_header

from ll.xist.ns import html

class xmlns(html):
	pass
xmlns.makemod(vars())
