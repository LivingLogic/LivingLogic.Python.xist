#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
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
<par>This modules contains elements for doing conditionals
on the &xml; level.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc, sandbox

class CodeAttr(xsc.Attr):
	"""
	used for attributes that contain Python code
	"""

class CondAttr(CodeAttr):
	"""
	used for Python conditions
	"""

class switch(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class var(xsc.TextAttr): pass

	def convert(self, converter):
		cases = self.find(type=case)

		return xsc.Null

class case(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class case(xsc.TextAttr): pass

	def convert(self, converter):
		return self.content.convert(converter)

class If(xsc.Element):
	empty = False
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
	empty = True
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
	empty = True
	xmlname = "else"

	def convert(self, converter):
		return xsc.Null

class xmlns(xsc.Namespace):
	xmlname = "cond"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/cond"
xmlns.makemod(vars())

