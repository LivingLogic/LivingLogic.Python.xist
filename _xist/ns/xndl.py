#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; module that contains elements that describe &xist; namespace
module and generate a skeleton implementation of this module.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, keyword

from ll.xist import xsc, utils

class Base(object):
	def __init__(self, name):
		self.name = name
		self._pyname = None

	def pyname(self, names=[]):
		"""
		<par>Return a modified version of <arg>name</arg>, that is a valid
		Python identifier. This is done by replacing illegal characters with
		<lit>_</lit> and appending an <lit>_</lit> when the name collides
		with a Python keyword. Furthermore it is made sure that the new
		name is not already part of the list <arg>names</arg>.</par>
		"""
		if self._pyname is None:
			newname = []
			name = self.name
			for c in name:
				if "a" <= c <= "z" or "A" <= c <= "Z" or "0" <= c <= "9" or c == "_":
					newname.append(c)
				else:
					newname.append("_")
			name = "".join(newname)
			testname = name
			if keyword.iskeyword(name):
				testname += "_"
			suffix = 2
			while testname in names:
				testname = "%s%d" % (name, suffix)
				suffix += 1
			name = testname
			self._pyname = name
			names.append(name)
		else:
			name = self._pyname
		return name

	def simplify(cls, value):
		"""
		<par>Return a string, whose value can be used as an intializer for an attribute values.
		If the value is an <class>int</class> strip the quotes, if it fits into ASCII drop
		the <lit>u</lit> prefix.</par>
		"""
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
		self._aspy(lines, encoding, 0, [])
		return "\n".join(["%s%s" % (level*indent, text) for (level, text) in lines])

	def _addlines(self, newlines, lines):
		l = len(newlines)
		if l==0:
			lines[-1][1] += " pass"
		elif l==1:
			lines[-1][1] += " %s" % newlines[-1][1]
		else:
			lines.extend(newlines)

class Doc(Base):
	def __init__(self, content):
		super(Doc, self).__init__(None)
		self.content = content

	def _aspy(self, lines, encoding, level, names):
		lines.append([level, '"""'])
		for line in self.content.asBytes(encoding=encoding).split("\n"):
			lines.append([level, line])
		lines.append([level, '"""'])

class Namespace(Base):
	def __init__(self, name, doc, url, content):
		super(Namespace, self).__init__(name)
		self.doc = doc
		self.url = url
		self.content = content

	def _findgroups(self):
		"""
		<par>This methods find all attribute groups defined for any attribute.
		As an attribute group can be reference multiple times (in fact that's
		the reason for the attribute groups existence), we have to make sure
		to list an attribute group only once. Furthermore the attribute groups
		should appear in the order in which they are referenced.</par>
		"""
		# find all attribute groups defined for the attributes
		attrgroups = []
		attrgroupset = {}
		for node in self.content:
			if isinstance(node, Element):
				for attr in node.attrs:
					if attr.shared is not None and attr.shared not in attrgroupset:
						attrgroups.append(attr.shared)
						attrgroupset[attr.shared] = True
		return attrgroups


	def _aspy(self, lines, encoding, level, names):
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

		attrgroups = self._findgroups()

		name = self.name
		pyname = self.pyname(names)

		# output attribute groups
		for attrgroup in attrgroups:
			lines.append([0, ""])
			attrgroup._aspy(lines, encoding, level, names)

		lines.append([0, ""])
		lines.append([level, "class %s(xsc.Namespace):" % pyname])
		if pyname != name:
			lines.append([level+1, "xmlname = %s" % self.simplify(name)])
		lines.append([level+1, "xmlurl = %s" % self.simplify(self.url)])

		for node in self.content:
			lines.append([0, ""])
			node._aspy(lines, encoding, level+1, names)

	def shareattrs(self, all):
		# collect all identical attributes into lists
		identicalattrs = []
		identicalattrset = {}
		for node in self.content:
			if isinstance(node, Element):
				for attr in node.attrs:
					if attr.shared is None: # skip attributes that are already shared
						ident = attr.ident()
						try:
							attrs = identicalattrset[ident]
						except KeyError:
							attrs = []
							identicalattrs.append(attrs)
							identicalattrset[ident] = attrs
						attrs.append(attr)
		for attrs in identicalattrs:
			# if the attribute appears more than once, define a group for it
			if all or len(attrs) > 1:
				group = AttrGroup(attrs[0].name, [attrs[0]])
				for attr in attrs:
					attr.share(group)

class Element(Base):
	def __init__(self, name, doc, empty, attrs):
		super(Element, self).__init__(name)
		self.doc = doc
		self.empty = empty
		self.attrs = attrs

	def _aspy(self, lines, encoding, level, names):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.Element):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, names)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		if self.empty:
			empty = "True"
		else:
			empty = "False"
		newlines.append([level+1, "empty = %s" % empty])

		if self.attrs:
			# find the attribute groups our elements are in
			# this means we don't have to define these attributes ourselves, but have to derive from the attribute group
			groups = []
			groupset = {}
			nogroup = []
			for attr in self.attrs:
				if attr.shared is not None:
					if attr.shared not in groupset:
						groups.append(attr.shared)
				else:
					nogroup.append(attr)
			if groups:
				base = ", ".join([group.pyname() for group in groups])
			else:
				base = "xsc.Element.Attrs"
			newlines.append([level+1, "class Attrs(%s):" % base])
			if nogroup:
				localnames = []
				for attr in nogroup:
					attr._aspy(newlines, encoding, level+2, localnames)
			else:
				newlines.append([level+2, "pass"])
		self._addlines(newlines, lines)

class AttrGroup(Base):
	id = 0
	def __init__(self, name, attrs):
		if name is None:
			name = "attrgroup_%d" % self.__class__.id
			self.__class__.id += 1
		super(AttrGroup, self).__init__(name)
		self.attrs = attrs

	def _aspy(self, lines, encoding, level, names):
		name = self.pyname(names)
		lines.append([level, "class %s(xsc.Element.Attrs):" % name])
		localnames = []
		for attr in self.attrs:
			attr._aspy(lines, encoding, level+1, localnames)

class Attr(Base):
	def __init__(self, name, doc, type, required, default, values):
		super(Attr, self).__init__(name)
		self.doc = doc
		self.type = type
		self.required = required
		self.default = default
		self.values = values
		self.shared = None

	def _aspy(self, lines, encoding, level, names):
		name = self.name
		pyname = self.pyname(names)
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

	def share(self, group):
		assert self.shared is None, "cannot share attr %r twice" % self
		self.shared = group

	def ident(self):
		return (self.name, self.type, self.required, self.default, tuple(self.values))

class ProcInst(Base):
	def __init__(self, name, doc):
		super(ProcInst, self).__init__(name)
		self.doc = doc

	def _aspy(self, lines, encoding, level, names):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.ProcInst):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1)
		if pytarget != target:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		self._addlines(newlines, lines)

class Entity(Base):
	def __init__(self, name, doc):
		super(Entity, self).__init__(name)
		self.doc = doc

	def _aspy(self, lines, encoding, level, names):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.Entity):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, names)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		self._addlines(newlines, lines)

class CharRef(Entity):
	def __init__(self, name, doc, codepoint):
		super(CharRef, self).__init__(name, doc)
		self.codepoint = codepoint

	def _aspy(self, lines, encoding, level, names):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.CharRef):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		newlines.append([level+1, "codepoint = 0x%04x" % self.codepoint])
		self._addlines(newlines, lines)

class xndl(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr): required = True
		class url(xsc.TextAttr): default = "... insert namespace name here ..."

	def asdata(self):
		docs = self.content.find(xsc.FindType(doc))
		if len(docs):
			docs = Doc(docs[0])
		else:
			docs = None

		return Namespace(
			name=unicode(self["name"]),
			doc=docs,
			url=unicode(self["url"]) or None,
			content=[ node.asdata() for node in self.content.find(xsc.FindType(element, procinst, entity, charref)) ]
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
		docs = self.content.find(xsc.FindType(doc))
		if len(docs):
			docs = Doc(docs[0])
		else:
			docs = None

		return Element(
			name=unicode(self["name"]),
			doc=docs,
			empty=self.attrs.has("empty"),
			attrs=[ a.asdata() for a in self.content.find(xsc.FindType(attr)) ]
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
		docs = self.content.find(xsc.FindType(doc))
		if len(docs):
			docs = Doc(docs[0])
		else:
			docs = None
		return Attr(
			name=unicode(self["name"]),
			doc=docs,
			type=str(self["type"]),
			required=self.attrs.has("required"),
			default=unicode(self["default"]) or None,
			values=[ unicode(v) for v in self.content.find(xsc.FindType(value)) ]
		)

class value(xsc.Element):
	empty = False

class procinst(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class target(xsc.TextAttr): required = True

	def asdata(self):
		name = unicode(self["target"])
		docs = self.content.find(xsc.FindType(doc))
		if len(docs):
			docs = docs[0]
		else:
			docs = None
		return ProcInst(
			name=name,
			doc=docs
		)

class entity(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr): required = True

	def asdata(self):
		name = unicode(self["name"])
		docs = self.content.find(xsc.FindType(doc))
		if len(docs):
			docs = docs[0]
		else:
			docs = None
		return Entity(
			name=unicode(self["name"]),
			doc=docs
		)

class charref(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr): required = True
		class codepoint(xsc.IntAttr): required = True

	def asdata(self):
		docs = self.content.find(xsc.FindType(doc))
		if len(docs):
			docs = docs[0]
		else:
			docs = None
		return CharRef(
			name=unicode(self["name"]),
			doc=docs,
			codepoint=int(self["codepoint"])
		)

class xmlns(xsc.Namespace):
	xmlname = "xndl"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/xndl"
xmlns.makemod(vars())

