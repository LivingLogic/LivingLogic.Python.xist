#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>This modules contains elements for doing conditionals
on the &xml; level.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc, sandbox, sims


class CodeAttr(xsc.Attr):
	"""
	used for attributes that contain Python code
	"""


class CondAttr(CodeAttr):
	"""
	used for Python conditions
	"""


class case(xsc.Element):
	model = sims.Any()
	class Attrs(xsc.Element.Attrs):
		class case(xsc.TextAttr): pass

	def convert(self, converter):
		return self.content.convert(converter)


class switch(xsc.Element):
	model = sims.Elements(case)
	class Attrs(xsc.Element.Attrs):
		class var(xsc.TextAttr): pass

	def convert(self, converter):
		cases = self.find(xsc.FindType(case))

		return xsc.Null


class If(xsc.Element):
	model = sims.Any()
	class Attrs(xsc.Element.Attrs):
		class cond(xsc.TextAttr): pass
		class mode(xsc.TextAttr): pass
		class target(xsc.TextAttr): pass
		class stage(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
	xmlname = "if"

	def convert(self, converter):
		intruecondition = self.__testCond(self, converter)
		truecondition = xsc.Frag()
		for child in self.content:
			if isinstance(child, ElIf):
				if intruecondition:
					break
				else:
					intruecondition = self.__testCond(child, converter)
			elif isinstance(child, Else):
				if intruecondition:
					break
				else:
					intruecondition = True
			else:
				if intruecondition:
					truecondition.append(child)
		return truecondition.convert(converter)

	def __testCond(self, node, converter):
		result = True
		if node.attrs.has("cond"):
			cond = unicode(node["cond"].convert(converter))
			result = eval(cond, sandbox.__dict__)
		if result and node.attrs.has("mode"):
			result = unicode(node["mode"].convert(converter)) == converter.mode
		if result and node.attrs.has("target"):
			result = unicode(node["target"].convert(converter)) == converter.target
		if result and node.attrs.has("stage"):
			result = unicode(node["stage"].convert(converter)) == converter.stage
		if result and node.attrs.has("lang"):
			result = unicode(node["lang"].convert(converter)) == converter.lang
		return result


class ElIf(xsc.Element):
	model = sims.Empty()
	xmlname = "elif"
	class Attrs(xsc.Element.Attrs):
		class cond(xsc.TextAttr): pass
		class mode(xsc.TextAttr): pass
		class target(xsc.TextAttr): pass
		class stage(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass

	def convert(self, converter):
		return xsc.Null


class Else(xsc.Element):
	model = sims.Empty()
	xmlname = "else"

	def convert(self, converter):
		return xsc.Null


class xmlns(xsc.Namespace):
	xmlname = "cond"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/cond"
xmlns.makemod(vars())
