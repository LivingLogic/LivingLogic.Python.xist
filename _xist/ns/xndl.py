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

class xndl(xsc.Namespace):
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/xndl"

	def pyify(cls, name):
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
	pyify = classmethod(pyify)

	def simplify(cls, value):
		try:
			value = int(value)
		except ValueError:
			try:
				value = str(value)
			except UnicodeError:
				pass
		return value
	simplify = classmethod(simplify)

	class xndl(Base):
		empty = False
		class Attrs(Base.Attrs):
			class name(xsc.TextAttr): required = True
			class url(xsc.TextAttr): default = "... insert namespace name here ..."

		def _aspy(self, lines, encoding, level):
			lines.append([level, "#!/usr/bin/env python"])
			lines.append([level, "# -*- coding: %s -*-" % encoding])
			lines.append([0, ""])

			docs = self.find(type=xndl.doc)
			if len(docs):
				docs[0]._aspy(lines, encoding, level)
				lines.append([0, ""])

			lines.append([level, "__version__ = \"%sRevision%s\"[11:-2]" % ("$", "$")])
			lines.append([level, "# %sSource%s" % ("$", "$")])
			lines.append([0, ""])
			lines.append([level, "from ll.xist import xsc"])
			lines.append([0, ""])

			name = unicode(self["name"])
			pyname = self.xmlns.pyify(name)
			lines.append([level, "class %s(xsc.Namespace):" % pyname])
			if pyname != name:
				lines.append([level+1, "xmlname = %r" % self.xmlns.simplify(name)])
			lines.append([level+1, "xmlurl = %r" % self.xmlns.simplify(unicode(self["url"]))])
			for el in self.find(type=(xndl.element, xndl.procinst, xndl.entity, xndl.charref)):
				lines.append([0, ""])
				el._aspy(lines, encoding, level+1)

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
			pyname = self.xmlns.pyify(name)
			lines.append([level, "class %s(xsc.Element):" % pyname])
			newlines = []
			docs = self.find(type=xndl.doc)
			if len(docs):
				docs[0]._aspy(newlines, encoding, level+1)
			if pyname != name:
				newlines.append([level+1, "xmlname = %r" % self.xmlns.simplify(name)])
			if self.attrs.has("empty"):
				empty = "True"
			else:
				empty = "False"
			newlines.append([level+1, "empty = %s" % ["False", "True"][self.attrs.has("empty")]])
			attrs = self.find(type=xndl.attr)
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
			pyname = self.xmlns.pyify(name)
			type = str(self["type"])
			lines.append([level, "class %s(xsc.%s):" % (pyname, type)])
			newlines = []
			docs = self.find(type=xndl.doc)
			if len(docs):
				docs[0]._aspy(newlines, encoding, level+1)
			if pyname != name:
				newlines.append([level+1, "xmlname = %r" % self.xmlns.simplify(name)])
			values = self.find(type=xndl.value)
			if values:
				newvaluelines = []
				for v in values:
					v._aspy(newvaluelines, encoding, level+1)
				values = "(%s)" % ", ".join([ text for (sublevel, text) in newvaluelines ])
				newlines.append([level+1, "values = %s" % (values, )])
			default = unicode(self["default"])
			if default:
				newlines.append([level+1, "default = %r" % self.xmlns.simplify(default)])
			if self.attrs.has("required"):
				newlines.append([level+1, "required = True"])
			self._addlines(newlines, lines)

	class value(Base):
		empty = False

		def _aspy(self, lines, encoding, level):
			lines.append([level, repr(self.xmlns.simplify(unicode(self.content)))])

	class procinst(Base):
		empty = False
		class Attrs(Base.Attrs):
			class target(xsc.TextAttr): required = True

		def _aspy(self, lines, encoding, level):
			name = unicode(self["target"])
			pyname = self.xmlns.pyify(name)
			lines.append([level, "class %s(xsc.ProcInst):" % pyname])
			newlines = []
			docs = self.find(type=xndl.doc)
			if len(docs):
				docs[0]._aspy(newlines, encoding, level+1)
			if pyname != name:
				newlines.append([level+1, "xmlname = %r" % self.xmlns.simplify(name)])
			self._addlines(newlines, lines)

	class entity(Base):
		empty = False
		class Attrs(Base.Attrs):
			class name(xsc.TextAttr): required = True

		def _aspy(self, lines, encoding, level):
			name = unicode(self["name"])
			pyname = self.xmlns.pyify(name)
			lines.append([level, "class %s(xsc.Entity):" % pyname])
			newlines = []
			docs = self.find(type=xndl.doc)
			if len(docs):
				docs[0]._aspy(newlines, encoding, level+1)
			if pyname != name:
				newlines.append([level+1, "xmlname = %r" % self.xmlns.simplify(name)])
			self._addlines(newlines, lines)

	class charref(Base):
		empty = False
		class Attrs(Base.Attrs):
			class name(xsc.TextAttr): required = True
			class codepoint(xsc.IntAttr): required = True

		def _aspy(self, lines, encoding, level):
			name = unicode(self["name"])
			pyname = self.xmlns.pyify(name)
			lines.append([level, "class %s(xsc.CharRef):" % pyname])
			newlines = []
			docs = self.find(type=xndl.doc)
			if len(docs):
				docs[0]._aspy(newlines, encoding, level+1)
			if pyname != name:
				newlines.append([level+1, "xmlname = %r" % self.xmlns.simplify(name)])
			codepoint = int(self["codepoint"])
			newlines.append([level+1, "codepoint = 0x%04x" % codepoint])
			self._addlines(newlines, lines)

