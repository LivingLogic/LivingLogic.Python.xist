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
<par>An &xist; module that contains elements that describe &xist; namespace
module and generate a skeleton implementation of this module.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, keyword

from ll.xist import xsc, utils

def pyify(name):
	if keyword.iskeyword(name):
		return name + "_"
	else:
		newname = []
		for c in name:
			if "a" <= c <= "z" or "A" <= c <= "Z" or "0" <= c <= "9" or c == "_":
				newname.append(c)
			else:
				newname.append("_")
		return "".join(newname)

def simplify(value):
	try:
		value = int(value)
	except ValueError:
		try:
			value = str(value)
		except UnicodeError:
			pass
	return value

class Base(xsc.Element):
	def aspy(self, encoding=None, indent="\t"):
		if encoding is None:
			encoding = sys.getdefaultencoding()
		lines = []
		self._aspy(lines, encoding, 0)
		return "\n".join(["%s%s" % (level*indent, text) for (level, text) in lines])

	def _addlines(self, newlines, lines):
		if len(newlines)==0:
			lines[-1][1] += " pass"
		elif len(newlines)==1:
			lines[-1][1] += " %s" % newlines[-1][1]
		else:
			lines.extend(newlines)

class xndl(Base):
	empty = False
	class Attrs(Base.Attrs):
		class prefix(xsc.TextAttr): required = True
		class name(xsc.TextAttr): default = "... insert namespace name here ..."

	def _aspy(self, lines, encoding, level):
		lines.append([level, "#!/usr/bin/env python"])
		lines.append([level, "# -*- coding: %s -*-" % encoding])
		lines.append([level, ""])

		docs = self.find(type=doc)
		if len(docs):
			docs[0]._aspy(lines, encoding, level)
			lines.append([level, ""])

		lines.append([level, "__version__ = \"%sRevision%s\"[11:-2]" % ("$", "$")])
		lines.append([level, "# %sSource%s" % ("$", "$")])
		lines.append([level, ""])
		lines.append([level, "from ll.xist import xsc"])

		for el in self.find(type=(element, procinst, entity, charref)):
			lines.append([level, ""])
			el._aspy(lines, encoding, level)
		lines.append([level, ""])
		lines.append([level, "xmlns = xsc.Namespace(%r, %r, vars())" % (str(self["prefix"]), str(self["name"]))])
		lines.append([level, ""])

class doc(Base):
	empty = False

	def _aspy(self, lines, encoding, level):
		lines.append([level, '"""'])
		for line in self.content.asBytes(encoding=encoding).split("\n"):
			lines.append([level, line])
		lines.append([level, '"""'])

class element(Base):
	empty = False
	class Attrs(Base.Attrs):
		class name(xsc.TextAttr): required = True
		class empty(xsc.BoolAttr): pass

	def _aspy(self, lines, encoding, level):
		name = unicode(self["name"])
		pyname = pyify(name)
		lines.append([level, "class %s(xsc.Element):" % pyname])
		newlines = []
		docs = self.find(type=doc)
		if len(docs):
			docs[0]._aspy(newlines, encoding, level+1)
		if pyname != name:
			newlines.append([level+1, "xmlname = %r" % simplify(name)])
		if self.hasattr("empty"):
			empty = "True"
		else:
			empty = "False"
		newlines.append([level+1, "empty = %s" % ["False", "True"][self.hasattr("empty")]])
		attrs = self.find(type=attr)
		if len(attrs):
			newlines.append([level+1, "class Attrs(xsc.Element.Attrs):"])
			for a in attrs:
				a._aspy(newlines, encoding, level+2)
		self._addlines(newlines, lines)

class attr(Base):
	empty = False
	class Attrs(Base.Attrs):
		class name(xsc.TextAttr): required = True
		class type(xsc.TextAttr):
			default = "TextAttr"
			required = True
		class required(xsc.BoolAttr): pass
		class default(xsc.TextAttr): pass

	def _aspy(self, lines, encoding, level):
		name = unicode(self["name"])
		pyname = pyify(name)
		type = str(self["type"])
		lines.append([level, "class %s(xsc.%s):" % (pyname, type)])
		newlines = []
		docs = self.find(type=doc)
		if len(docs):
			docs[0]._aspy(newlines, encoding, level+1)
		if pyname != name:
			newlines.append([level+1, "xmlname = %r" % simplify(name)])
		values = self.find(type=value)
		if values:
			newvaluelines = []
			for v in values:
				v._aspy(newvaluelines, encoding, level+1)
			values = "(%s)" % ", ".join([ text for (sublevel, text) in newvaluelines ])
			newlines.append([level+1, "values = %s" % (values, )])
		default = unicode(self["default"])
		if default:
			newlines.append([level+1, "default = %r" % simplify(default)])
		if self.hasattr("required"):
			newlines.append([level+1, "required = True"])
		self._addlines(newlines, lines)

class value(Base):
	empty = False

	def _aspy(self, lines, encoding, level):
		lines.append([level, repr(simplify(unicode(self.content)))])

class procinst(Base):
	empty = False
	class Attrs(Base.Attrs):
		class target(xsc.TextAttr): required = True

	def _aspy(self, lines, encoding, level):
		name = unicode(self["target"])
		pyname = pyify(name)
		lines.append([level, "class %s(xsc.ProcInst):" % pyname])
		newlines = []
		docs = self.find(type=doc)
		if len(docs):
			docs[0]._aspy(newlines, encoding, level+1)
		if pyname != name:
			newlines.append([level+1, "xmlname = %r" % simplify(name)])
		self._addlines(newlines, lines)

class entity(Base):
	empty = False
	class Attrs(Base.Attrs):
		class name(xsc.TextAttr): required = True

	def _aspy(self, lines, encoding, level):
		name = unicode(self["name"])
		pyname = pyify(name)
		lines.append([level, "class %s(xsc.Entity):" % pyname])
		newlines = []
		docs = self.find(type=doc)
		if len(docs):
			docs[0]._aspy(newlines, encoding, level+1)
		if pyname != name:
			newlines.append([level+1, "xmlname = %r" % simplify(name)])
		self._addlines(newlines, lines)

class charref(Base):
	empty = False
	class Attrs(Base.Attrs):
		class name(xsc.TextAttr): required = True
		class codepoint(xsc.IntAttr): required = True

	def _aspy(self, lines, encoding, level):
		name = unicode(self["name"])
		pyname = pyify(name)
		lines.append([level, "class %s(xsc.CharRef):" % pyname])
		newlines = []
		docs = self.find(type=doc)
		if len(docs):
			docs[0]._aspy(newlines, encoding, level+1)
		if pyname != name:
			newlines.append([level+1, "xmlname = %r" % simplify(name)])
		codepoint = int(self["codepoint"])
		newlines.append([level+1, "codepoint = 0x%04x" % codepoint])
		self._addlines(newlines, lines)

# register all the classes we've defined so far
xmlns = xsc.Namespace("xndl", "http://xmlns.livinglogic.de/xist/ns/xndl", vars())

