#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>A module that allows you to embed PHP processing instructions.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc, sims


class php(xsc.ProcInst):
	"""
	<par>&php; processing instruction
	(must be used with an explicit target php to work with &xml;)</par>
	"""


class expression(php):
	def convert(self, converter):
		return php(u"print " + self.content + ";")


class If(php):
	xmlname = "if"

	def convert(self, converter):
		return php(u"if (" + self.content + "){")


class Else(php):
	xmlname = "else"

	def convert(self, converter):
		return php(u"}else{")


class ElIf(php):
	xmlname = "elif"

	def convert(self, converter):
		return php(u"}else if (" + self.content + "){")


class End(php):
	xmlname = "end"

	def convert(self, converter):
		return php(u"}")


class block(xsc.Element):
	model = sims.Any()

	def convert(self, converter):
		e = xsc.Frag(
			php(u"{"),
			self.content,
			php(u"}")
		)
		return e.convert(converter)


class xmlns(xsc.Namespace):
	xmlname = "php"
	xmlurl = "http://www.php.net/"
xmlns.makemod(vars())
