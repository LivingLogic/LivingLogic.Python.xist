#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
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
<doc:par>This modules contains elements for doing conditionals
on the &xml; level.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc, sandbox

class CodeAttr(xsc.Attr):
	"""
	used for attributes that contain Python code
	"""

class CondAttr(CodeAttr):
	"""
	used for Python conditions
	"""

class switch(xsc.Element):
	empty = 0
	attrHandlers = {"var": xsc.TextAttr}

	def convert(self, converter):
		cases = self.find(type=case)

		return xsc.Null

class case(xsc.Element):
	empty = 0
	attrHandlers = {"case": xsc.TextAttr}

	def convert(self, converter):
		return self.content.convert(converter)

class If(xsc.Element):
	empty = 0
	attrHandlers = {"cond": CondAttr, "mode": xsc.TextAttr, "target": xsc.TextAttr, "stage": xsc.TextAttr, "lang": xsc.TextAttr}
	name = "if"

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
					intruecondition = 1
			else:
				if intruecondition:
					truecondition.append(child)
		return truecondition.convert(converter)

	def __testCond(self, node, converter):
		result = 1
		if node.hasAttr("cond"):
			cond = node["cond"].convert(converter).asPlainString()
			result = eval(str(cond), sandbox.__dict__)
		if result and node.hasAttr("mode"):
			result = node["mode"].convert(converter).asPlainString() == converter.mode
		if result and node.hasAttr("target"):
			result = node["target"].convert(converter).asPlainString() == converter.target
		if result and node.hasAttr("stage"):
			result = node["stage"].convert(converter).asPlainString() == converter.stage
		if result and node.hasAttr("lang"):
			result = node["lang"].convert(converter).asPlainString() == converter.lang
		return result

class ElIf(xsc.Element):
	empty = 1
	attrHandlers = {"cond": CondAttr, "mode": xsc.TextAttr, "target": xsc.TextAttr, "stage": xsc.TextAttr, "lang": xsc.TextAttr}
	name = "elif"

	def convert(self, converter):
		return xsc.Null

class Else(xsc.Element):
	empty = 1
	name = "else"

	def convert(self, converter):
		return xsc.Null

namespace = xsc.Namespace("cond", "http://xmlns.livinglogic.de/xist/cond.dtd", vars())

