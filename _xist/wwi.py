#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>A XSC module can be used with WebWare</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import HTTPServlet

import xsc

class Servlet(HTTPServlet.HTTPServlet):
	encoding = "utf-8"

	def respondToGet(self, trans):
		trans._response.write(self.content(trans).convert().asBytes(encoding=self.encoding))

	def content(self, trans):
		return xsc.Null
