#! /usr/bin/env python

## Copyright 2000 by Living Logic AG, Bayreuth, Germany.
## Copyright 2000 by Walter Dörwald
##
## See the file LICENSE for licensing details

"""
This modules contains elements for doing conditional
on the XML level.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

from xist import xsc, html

class switch(xsc.Element):
	empty = 0
	attrHandlers = {"var": xsc.TextAttr}

	def asHTML(self):
		cases = self.find(type=case)

class case(xsc.Element):
	empty = 0
	attrHandlers = {"case": xsc.TextAttr}

	def asHTML(self):
		return self.content.asHTML()

