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

class Base(object):
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
				if '"' in value:
					value = repr(value)
				else:
					value = 'u"%s"' % repr(value)[2:-1]
			else:
				if '"' in value:
					value = repr(value)
				else:
					value = '"%s"' % repr(value)[1:-1]
		return value
	simplify = classmethod(simplify)

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

class Doc(Base):
	def __init__(self, content):
		self.content = content

	def _aspy(self, lines, encoding, level):
		lines.append([level, '"""'])
		for line in self.content.asBytes(encoding=encoding).split("\n"):
			lines.append([level, line])
		lines.append([level, '"""'])

class Namespace(Base):
	def __init__(self, name, doc, url, content):
		self.name = name
		self.doc = doc
		self.url = url
		self.content = content

	def _aspy(self, lines, encoding, level):
		lines.append([level, "#!/usr/bin/env python"])
		lines.append([level, "# -*- coding: %s -*-" % encoding])
		lines.append([0, ""])

		if self.doc is not None:
			self.doc._aspy(lines, encoding, level)
			lines.append([0, ""])

		lines.append([level, "__version__ = \"%sRevision%s\"[11:-2]" % ("$", "$")])
		lines.append([level, "# %sSource%s" % ("$", "$")])
		lines.append([0, ""])
		lines.append([level, "from ll.xist import xsc"])
		lines.append([0, ""])

		name = self.name
		pyname = self.pyify(name)
		lines.append([level, "class %s(xsc.Namespace):" % pyname])
		if pyname != name:
			lines.append([level+1, "xmlname = %s" % self.simplify(name)])
		lines.append([level+1, "xmlurl = %s" % self.simplify(self.url)])
		for node in self.content:
			lines.append([0, ""])
			node._aspy(lines, encoding, level+1)

class Element(Base):
	def __init__(self, name, doc, empty, attrs):
		self.name = name
		self.doc = doc
		self.empty = empty
		self.attrs = attrs

	def _aspy(self, lines, encoding, level):
		name = self.name
		pyname = self.pyify(name)
		lines.append([level, "class %s(xsc.Element):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		if self.empty:
			empty = "True"
		else:
			empty = "False"
		newlines.append([level+1, "empty = %s" % empty])
		if self.attrs:
			newlines.append([level+1, "class Attrs(xsc.Element.Attrs):"])
			for a in self.attrs:
				a._aspy(newlines, encoding, level+2)
		self._addlines(newlines, lines)

class Attr(Base):
	def __init__(self, name, doc, type, required, default, values):
		self.name = name
		self.doc = doc
		self.type = type
		self.required = required
		self.default = default
		self.values = values

	def _aspy(self, lines, encoding, level):
		name = self.name
		pyname = self.pyify(name)
		lines.append([level, "class %s(xsc.%s):" % (pyname, self.type)])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		if self.values:
			values = "(%s)" % ", ".join([ str(self.simplify(value)) for value in self.values ])
			newlines.append([level+1, "values = %s" % (values, )])
		if self.default:
			newlines.append([level+1, "default = %s" % self.simplify(self.default)])
		if self.required:
			newlines.append([level+1, "required = True"])
		self._addlines(newlines, lines)

class ProcInst(Base):
	def __init__(self, target, doc):
		self.target = target
		self.doc = doc

	def _aspy(self, lines, encoding, level):
		target = self.target
		pytarget = self.pyify(target)
		lines.append([level, "class %s(xsc.ProcInst):" % pytarget])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1)
		if pytarget != target:
			newlines.append([level+1, "xmlname = %s" % self.simplify(target)])
		self._addlines(newlines, lines)

class Entity(Base):
	def __init__(self, name, doc):
		self.name = name
		self.doc = doc

	def _aspy(self, lines, encoding, level):
		name = self.name
		pyname = self.pyify(name)
		lines.append([level, "class %s(xsc.Entity):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1)
		if pyname != name:
			newlines.append([level+1, "xmlname = %r" % self.simplify(name)])
		self._addlines(newlines, lines)

class CharRef(Entity):
	def __init__(self, name, doc, codepoint):
		super(CharRef, self).__init__(name, doc)
		self.codepoint = codepoint

	def _aspy(self, lines, encoding, level):
		name = self.name
		pyname = self.pyify(name)
		lines.append([level, "class %s(xsc.CharRef):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1)
		if pyname != name:
			newlines.append([level+1, "xmlname = %r" % self.simplify(name)])
		newlines.append([level+1, "codepoint = 0x%04x" % self.codepoint])
		self._addlines(newlines, lines)

class xndl(xsc.Namespace):
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/xndl"

	class xndl(xsc.Element):
		empty = False
		class Attrs(xsc.Element.Attrs):
			class name(xsc.TextAttr): required = True
			class url(xsc.TextAttr): default = "... insert namespace name here ..."

		def asdata(self):
			docs = self.find(type=xndl.doc)
			if len(docs):
				doc = Doc(docs[0])
			else:
				doc = None

			return Namespace(
				name=unicode(self["name"]),
				doc=doc,
				url=unicode(self["url"]) or None,
				content=[ node.asdata() for node in self.find(type=(xndl.element, xndl.procinst, xndl.entity, xndl.charref)) ]
			)

	class doc(xsc.Element):
		empty = False

		def asdata(self):
			return self.content

	class element(xsc.Element):
		empty = False
		class Attrs(xsc.Element.Attrs):
			class name(xsc.TextAttr): required = True
			class empty(xsc.BoolAttr): pass

		def asdata(self):
			docs = self.find(type=xndl.doc)
			if len(docs):
				doc = Doc(docs[0])
			else:
				doc = None

			return Element(
				name=unicode(self["name"]),
				doc=doc,
				empty=self.attrs.has("empty"),
				attrs=[ attr.asdata() for attr in self.find(type=xndl.attr) ]
			)

	class attr(xsc.Element):
		empty = False
		class Attrs(xsc.Element.Attrs):
			class name(xsc.TextAttr): required = True
			class type(xsc.TextAttr):
				default = "TextAttr"
				required = True
			class required(xsc.BoolAttr): pass
			class default(xsc.TextAttr): pass

		def asdata(self):
			docs = self.find(type=xndl.doc)
			if len(docs):
				doc = Doc(docs[0])
			else:
				doc = None
			return Attr(
				name=unicode(self["name"]),
				doc=doc,
				type=str(self["type"]),
				required=self.attrs.has("required"),
				default=unicode(self["default"]) or None,
				values=[ unicode(value) for value in self.find(type=xndl.value) ]
			)

	class value(xsc.Element):
		empty = False

	class procinst(xsc.Element):
		empty = False
		class Attrs(xsc.Element.Attrs):
			class target(xsc.TextAttr): required = True

		def asdata(self):
			name = unicode(self["target"])
			docs = self.find(type=xndl.doc)
			if len(docs):
				doc = docs[0]
			else:
				doc = None
			return ProcInst(
				target=unicode(self["target"]),
				doc=doc
			)

	class entity(xsc.Element):
		empty = False
		class Attrs(xsc.Element.Attrs):
			class name(xsc.TextAttr): required = True

		def asdata(self):
			name = unicode(self["name"])
			docs = self.find(type=xndl.doc)
			if len(docs):
				doc = docs[0]
			else:
				doc = None
			return Entity(
				name=unicode(self["name"]),
				doc=doc
			)

	class charref(xsc.Element):
		empty = False
		class Attrs(xsc.Element.Attrs):
			class name(xsc.TextAttr): required = True
			class codepoint(xsc.IntAttr): required = True

		def asdata(self):
			docs = self.find(type=xndl.doc)
			if len(docs):
				doc = docs[0]
			else:
				doc = None
			return CharRef(
				name=unicode(self["name"]),
				doc=doc,
				codepoint=int(self["codepoint"])
			)

