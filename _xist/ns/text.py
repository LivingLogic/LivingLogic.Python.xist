#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 2002 by Walter Dörwald
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
<par>An &xist; namespace that contains definitions for all the elements and
entities in <link href="http://www.w3.org/TR/html4/loose.dtd">&html; 4.0 transitional</link>
(and a few additional ones).</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import cgi # for parse_header

from ll.xist.ns.html import html

class text(html):
	pass
