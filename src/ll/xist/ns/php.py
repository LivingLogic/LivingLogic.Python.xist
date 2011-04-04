# -*- coding: utf-8 -*-

## Copyright 1999-2011 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2011 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
A module that allows you to embed PHP processing instructions.
"""


from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://www.php.net/"


class php(xsc.ProcInst):
	"""
	PHP processing instruction (must be used with an explicit target php to work
	with XML)
	"""


class expression(php):
	def convert(self, converter):
		return php(u"print ", self.content, u";")


class If(php):
	xmlname = "if"
	prettyindentbefore = 0
	prettyindentafter = 1

	def convert(self, converter):
		return php(u"if (", self.content, u"){")


class Else(php):
	xmlname = "else"
	prettyindentbefore = -1
	prettyindentafter = 1

	def convert(self, converter):
		return php(u"}else{")


class ElIf(php):
	xmlname = "elif"
	prettyindentbefore = -1
	prettyindentafter = 1

	def convert(self, converter):
		return php(u"}else if (", self.content, u"){")


class End(php):
	xmlname = "end"
	prettyindentbefore = -1
	prettyindentafter = 0

	def convert(self, converter):
		return php(u"}")


class block(xsc.Element):
	xmlns = xmlns
	model = sims.Any()

	def convert(self, converter):
		e = xsc.Frag(
			php(u"{"),
			self.content,
			php(u"}")
		)
		return e.convert(converter)
