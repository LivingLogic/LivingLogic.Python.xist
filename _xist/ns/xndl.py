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
		name is not in the list <arg>names</arg>.</par>
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

	def aspy(self, encoding=None, indent="\t", asmod=True):
		if encoding is None:
			encoding = sys.getdefaultencoding()
		lines = []
		self._aspy(lines, encoding, 0, [], asmod)
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
		Base.__init__(self, None)
		self.content = content

	def _aspy(self, lines, encoding, level, names, asmod):
		lines.append([level, '"""'])
		for line in self.content.asBytes(encoding=encoding).split("\n"):
			lines.append([level, line])
		lines.append([level, '"""'])

class Namespace(Base):
	def __init__(self, name, doc, url, content):
		Base.__init__(self, name)
		self.doc = doc
		self.url = url
		self.content = content

	def _findgroups(self):
		"""
		<par>This methods find all attribute groups defined for any attribute.
		As an attribute group can be referenced multiple times (in fact that's
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

	def _aspy(self, lines, encoding, level, names, asmod):
		lines.append([level, "#!/usr/bin/env python"])
		lines.append([level, "# -*- coding: %s -*-" % encoding])
		lines.append([0, ""])

		if self.doc is not None:
			self.doc._aspy(lines, encoding, level, names, asmod)
			lines.append([0, ""])

		lines.append([level, "__version__ = \"%sRevision%s\"[11:-2]" % ("$", "$")])
		lines.append([level, "# %sSource%s" % ("$", "$")])
		lines.append([0, ""])
		lines.append([level, "from ll.xist import xsc"])

		attrgroups = self._findgroups()

		realname = self.name
		self.name = "xmlns"
		pyname = self.pyname(names)
		self.name = realname

		# output attribute groups
		for attrgroup in attrgroups:
			lines.append([0, ""])
			attrgroup._aspy(lines, encoding, level, names, asmod)

		# output elements
		for node in self.content:
			lines.append([0, ""])
			node._aspy(lines, encoding, level, names, asmod)

		lines.append([0, ""])
		lines.append([level, "class %s(xsc.Namespace):" % pyname])
		if pyname != self.name:
			lines.append([level+1, "xmlname = %s" % self.simplify(self.name)])
		if self.url is None:
			url = "... insert namespace name ..."
		else:
			url = self.url
		lines.append([level+1, "xmlurl = %s" % self.simplify(url)])
		if asmod:
			method = "makemod"
		else:
			method = "update"
		lines.append([level, "%s.%s(vars())" % (pyname, method)])

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
			# if the attribute appears more than once (or all attributes should be shared), define a group for it
			if all or len(attrs) > 1:
				group = AttrGroup(attrs[0].name, [attrs[0]])
				for attr in attrs:
					attr.share(group)

class Element(Base):
	def __init__(self, name, doc, empty, attrs):
		Base.__init__(self, name)
		self.doc = doc
		self.empty = empty
		self.attrs = attrs

	def _aspy(self, lines, encoding, level, names, asmod):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.Element):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, names, asmod)
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
					attr._aspy(newlines, encoding, level+2, localnames, asmod)
			else:
				newlines.append([level+2, "pass"])
		self._addlines(newlines, lines)

class AttrGroup(Base):
	id = 0
	def __init__(self, name, attrs):
		if name is None:
			name = "attrgroup_%d" % self.__class__.id
			self.__class__.id += 1
		Base.__init__(self, name)
		self.attrs = attrs

	def _aspy(self, lines, encoding, level, names, asmod):
		name = self.pyname(names)
		lines.append([level, "class %s(xsc.Element.Attrs):" % name])
		localnames = []
		for attr in self.attrs:
			attr._aspy(lines, encoding, level+1, localnames, asmod)

class Attr(Base):
	def __init__(self, name, doc, type, required, default, values):
		Base.__init__(self, name)
		self.doc = doc
		self.type = type
		self.required = required
		self.default = default
		self.values = values
		self.shared = None # if this attribute is part of a group shared will point to this group

	def _aspy(self, lines, encoding, level, names, asmod):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.%s):" % (pyname, self.type)])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, asmod)
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
		Base.__init__(self, name)
		self.doc = doc

	def _aspy(self, lines, encoding, level, names, asmod):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.ProcInst):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, names, asmod)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		self._addlines(newlines, lines)

class Entity(Base):
	def __init__(self, name, doc):
		Base.__init__(self, name)
		self.doc = doc

	def _aspy(self, lines, encoding, level, names, asmod):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.Entity):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, names, asmod)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		self._addlines(newlines, lines)

class CharRef(Entity):
	def __init__(self, name, doc, codepoint):
		Entity.__init__(self, name, doc)
		self.codepoint = codepoint

	def _aspy(self, lines, encoding, level, names, asmod):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.CharRef):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, asmod)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		newlines.append([level+1, "codepoint = 0x%04x" % self.codepoint])
		self._addlines(newlines, lines)

class base(xsc.Element):
	def finddoc(self):
		docs = self.content.find(xsc.FindType(doc))

		if len(docs):
			return Doc(docs[0].content)
		else:
			return None

class xndl(base):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr): required = True
		class url(xsc.TextAttr): pass

	def asdata(self):
		return Namespace(
			name=unicode(self["name"]),
			doc=self.finddoc(),
			url=unicode(self["url"]) or None,
			content=[ node.asdata() for node in self.content.find(xsc.FindType(element, procinst, entity, charref)) ]
		)

class doc(base):
	empty = False

	def asdata(self):
		return self.content

class element(base):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr): required = True
		class empty(xsc.BoolAttr): pass

	def asdata(self):
		return Element(
			name=unicode(self["name"]),
			doc=self.finddoc(),
			empty=self.attrs.has("empty"),
			attrs=[ a.asdata() for a in self.content.find(xsc.FindType(attr)) ]
		)

class attr(base):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr): required = True
		class type(xsc.TextAttr):
			default = "TextAttr"
			required = True
		class required(xsc.BoolAttr): pass
		class default(xsc.TextAttr): pass

	def asdata(self):
		return Attr(
			name=unicode(self["name"]),
			doc=self.finddoc(),
			type=str(self["type"]),
			required=self.attrs.has("required"),
			default=unicode(self["default"]) or None,
			values=[ unicode(v) for v in self.content.find(xsc.FindType(value)) ]
		)

class value(base):
	empty = False

class procinst(base):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class target(xsc.TextAttr): required = True

	def asdata(self):
		name = unicode(self["target"])
		return ProcInst(
			name=name,
			doc=self.finddoc()
		)

class entity(base):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr): required = True

	def asdata(self):
		name = unicode(self["name"])
		return Entity(
			name=unicode(self["name"]),
			doc=self.finddoc()
		)

class charref(base):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr): required = True
		class codepoint(xsc.IntAttr): required = True

	def asdata(self):
		return CharRef(
			name=unicode(self["name"]),
			doc=self.finddoc(),
			codepoint=int(self["codepoint"])
		)

class xmlns(xsc.Namespace):
	xmlname = "xndl"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/xndl"

	def fromdtd(cls, dtd, xmlname, xmlurl=None):
		"""
		Convert &dtd; information (in the format that is returned by <app>xmlproc</app>s
		<function>dtdparser.load_dtd</function> function) to an &xist; DOM using the
		<pyref module="ll.xist.ns.xndl"><module>xndl</module></pyref> namespace.
		"""

		node = xndl(name=xmlname, url=xmlurl)

		xmlns = {} # collects all the values of fixed xmlns attributes (as a set)

		# Add element info
		elements = dtd.get_elements()
		elements.sort()
		for elemname in elements:
			e = dtd.get_elem(elemname)
			if e.get_content_model() == ("", [], ""):
				empty = True
			else:
				empty = None
			node.append(element(name=elemname, empty=empty))

			# Add attribute info for this element
			attrs = e.get_attr_list()
			if len(attrs):
				attrs.sort()
				for attrname in attrs:
					a = e.get_attr(attrname)
					if attrname=="xmlns":
						if a.decl=="#FIXED":
							xmlns[a.default] = None
						continue # skip a namespace declaration
					elif u":" in attrname:
						continue # skip global attributes
					values = []
					if a.type == "ID":
						type = "IDAttr"
					else:
						type = "TextAttr"
						if isinstance(a.type, list):
							if len(a.type)>1:
								values = a.type
							else:
								type = "BoolAttr"
					default = a.default
					if a.decl=="#REQUIRED":
						required = True
					else:
						required = None
					node[-1].append(attr(name=attrname, type=type, default=default, required=required))
					for v in values:
						node[-1][-1].append(value(v))

		# Add entities
		ents = dtd.get_general_entities()
		ents.sort()
		for entname in ents:
			if entname not in ("quot", "apos", "gt", "lt", "amp"):
				ent = parsers.parseString(dtd.resolve_ge(entname).value)
				node.append(charref(name=entname, codepoint=ord(unicode(ent[0])[0])))

		# if the DTD has exactly one value for all fixed "xmlns" attributes and the user didn't specify an xmlurl, use this one
		if xmlurl is None and len(xmlns)==1:
			node["url"] = xmlns.popitem()[0]
		return node
	fromdtd = classmethod(fromdtd)

xmlns.makemod(vars())

