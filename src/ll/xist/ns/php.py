# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
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

	def convert(self, converter):
		return php(u"if (", self.content, u"){")


class Else(php):
	xmlname = "else"

	def convert(self, converter):
		return php(u"}else{")


class ElIf(php):
	xmlname = "elif"

	def convert(self, converter):
		return php(u"}else if (", self.content, u"){")


class End(php):
	xmlname = "end"

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
