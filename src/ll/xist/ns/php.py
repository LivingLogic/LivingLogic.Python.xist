# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


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
		return php("print ", self.content, ";")


class If(php):
	xmlname = "if"
	prettyindentbefore = 0
	prettyindentafter = 1

	def convert(self, converter):
		return php("if (", self.content, "){")


class Else(php):
	xmlname = "else"
	prettyindentbefore = -1
	prettyindentafter = 1

	def convert(self, converter):
		return php("}else{")


class ElIf(php):
	xmlname = "elif"
	prettyindentbefore = -1
	prettyindentafter = 1

	def convert(self, converter):
		return php("}else if (", self.content, "){")


class End(php):
	xmlname = "end"
	prettyindentbefore = -1
	prettyindentafter = 0

	def convert(self, converter):
		return php("}")


class block(xsc.Element):
	xmlns = xmlns
	model = sims.Any()

	def convert(self, converter):
		e = xsc.Frag(
			php("{"),
			self.content,
			php("}")
		)
		return e.convert(converter)
