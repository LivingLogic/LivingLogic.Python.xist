#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
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

from ll.xist import xsc, parsers, sims


class Base(object):
	def __init__(self, name):
		self.name = name
		self._pyname = None

	def pyname(self, names=None):
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

	def aspy(self, encoding=None, indent="\t", asmod=True, defaults=False, schema=False):
		if encoding is None:
			encoding = sys.getdefaultencoding()
		lines = []
		self._aspy(lines, encoding, 0, [], asmod, defaults, schema)
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

	def _aspy(self, lines, encoding, level, names, asmod, defaults, schema):
		lines.append([level, '"""'])
		for line in self.content.asBytes(encoding=encoding).split("\n"):
			lines.append([level, line])
		lines.append([level, '"""'])


class Namespace(Base, list):
	def __init__(self, name, url=None, doc=None):
		Base.__init__(self, name)
		list.__init__(self)
		self.url = url
		self.doc = doc

	def __repr__(self):
		return "<%s.%s name=%r url=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, self.url, id(self))

	def __call__(self, *content):
		self.extend(content)
		return self

	def _findgroups(self):
		"""
		<par>This method finds all attribute groups defined for any attribute.
		As an attribute group can be referenced multiple times (in fact that's
		the reason for the attribute groups existence), we have to make sure
		to list an attribute group only once. Furthermore the attribute groups
		should appear in the order in which they are referenced.</par>
		"""
		# find all attribute groups defined for the attributes
		attrgroups = []
		attrgroupset = {}
		for node in self:
			if isinstance(node, Element):
				for attr in node:
					key = tuple(attr.shared)
					if attr.shared is not None and key not in attrgroupset:
						attrgroups.append(attr.shared)
						attrgroupset[key] = True
		return attrgroups

	def _aspy(self, lines, encoding, level, names, asmod, defaults, schema):
		lines.append([level, "#!/usr/bin/env python"])
		lines.append([level, "# -*- coding: %s -*-" % encoding])
		lines.append([0, ""])
		lines.append([0, ""])

		if self.doc is not None:
			self.doc._aspy(lines, encoding, level, names, asmod, defaults, schema)
			lines.append([0, ""])

		lines.append([level, "__version__ = \"%sRevision%s\"[11:-2]" % ("$", "$")])
		lines.append([level, "# %sSource%s" % ("$", "$")])
		lines.append([0, ""])
		lines.append([0, ""])
		lines.append([level, "from ll.xist import xsc, sims"])

		attrgroups = self._findgroups()

		realname = self.name
		self.name = "xmlns"
		pyname = self.pyname(names)
		self.name = realname

		# output attribute groups
		for attrgroup in attrgroups:
			lines.append([0, ""])
			lines.append([0, ""])
			attrgroup._aspy(lines, encoding, level, names, asmod, defaults, schema)

		# output elements, procinsts, entities and charref
		for node in self:
			lines.append([0, ""])
			lines.append([0, ""])
			node._aspy(lines, encoding, level, names, asmod, defaults, schema)

		# output schema information for the elements
		elswithschema = [node for node in self if isinstance(node, Element) and node.model is not None]
		if elswithschema:
			lines.append([0, ""])
			lines.append([0, ""])
			for node in elswithschema:
				lines.append([0, "%s.model = %s" % (node.pyname(), node.model)])

		lines.append([0, ""])
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
		for node in self:
			if isinstance(node, Element):
				for attr in node:
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
				group = AttrGroup(attrs[0].name)(attrs[0])
				for attr in attrs:
					attr.share(group)


class Element(Base, list):
	def __init__(self, name, model=None, doc=None):
		Base.__init__(self, name)
		list.__init__(self)
		self.model = model
		self.doc = doc

	def __repr__(self):
		return "<%s.%s name=%r model=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, self.model, id(self))

	def __call__(self, *content):
		self.extend(content)
		return self

	def _aspy(self, lines, encoding, level, names, asmod, defaults, schema):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.Element):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, names, asmod, defaults, schema)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		# don't output model, because this is done after all element classes have been defined

		if len(self):
			# find the attribute groups our elements are in
			# this means we don't have to define these attributes ourselves, but have to derive from the attribute group
			groups = []
			groupset = {}
			nogroup = []
			for attr in self:
				if attr.shared is not None:
					if tuple(attr.shared) not in groupset:
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
					attr._aspy(newlines, encoding, level+2, localnames, asmod, defaults, schema)
			else:
				newlines.append([level+2, "pass"])
		self._addlines(newlines, lines)


class AttrGroup(Base, list):
	id = 0
	def __init__(self, name):
		if name is None:
			name = "attrgroup_%d" % self.__class__.id
			self.__class__.id += 1
		Base.__init__(self, name)
		list.__init__(self)

	def __call__(self, *content):
		self.extend(content)
		return self

	def _aspy(self, lines, encoding, level, names, asmod, defaults, schema):
		name = self.pyname(names)
		lines.append([level, "class %s(xsc.Element.Attrs):" % name])
		localnames = []
		for attr in self:
			attr._aspy(lines, encoding, level+1, localnames, asmod, defaults, schema)


class Attr(Base):
	def __init__(self, name, type, required=False, default=None, values=None, doc=None):
		Base.__init__(self, name)
		self.doc = doc
		self.type = type
		self.required = required
		self.default = default
		if values is None:
			values = []
		self.values = values
		self.shared = None # if this attribute is part of a group <lit>shared</lit> will point to the group

	def __repr__(self):
		return "<%s.%s name=%r type=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, self.type, id(self))

	def _aspy(self, lines, encoding, level, names, asmod, defaults, schema):
		name = self.name
		pyname = self.pyname(names)
		basename = "%s.%s" % (self.type.__module__, self.type.__name__)
		if basename.startswith("ll.xist.xsc."):
			basename = basename[8:]
		lines.append([level, "class %s(%s):" % (pyname, basename)])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, asmod, defaults, schema)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		if self.values:
			values = "(%s)" % ", ".join([ str(self.simplify(value)) for value in self.values ])
			newlines.append([level+1, "values = %s" % (values, )])
		if self.default and defaults:
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
	def __init__(self, name, doc=None):
		Base.__init__(self, name)
		self.doc = doc

	def __repr__(self):
		return "<%s.%s name=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, id(self))

	def _aspy(self, lines, encoding, level, names, asmod, defaults, schema):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.ProcInst):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, names, asmod, defaults, schema)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		self._addlines(newlines, lines)


class Entity(Base):
	def __init__(self, name, doc=None):
		Base.__init__(self, name)
		self.doc = doc

	def __repr__(self):
		return "<%s.%s name=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, id(self))

	def _aspy(self, lines, encoding, level, names, asmod, defaults, schema):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.Entity):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, names, asmod, defaults, schema)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		self._addlines(newlines, lines)


class CharRef(Entity):
	def __init__(self, name, codepoint, doc=None):
		Entity.__init__(self, name, doc)
		self.codepoint = codepoint

	def __repr__(self):
		return "<%s.%s name=%r codepoint=0x%x at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, self.codepoint, id(self))

	def _aspy(self, lines, encoding, level, names, asmod, defaults, schema):
		name = self.name
		pyname = self.pyname(names)
		lines.append([level, "class %s(xsc.CharRef):" % pyname])
		newlines = []
		if self.doc is not None:
			self.doc._aspy(newlines, encoding, level+1, names, asmod, defaults, schema)
		if pyname != name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(name)])
		if self.codepoint > 0xffff:
			codepoint = "0x%08x" % self.codepoint
		else:
			codepoint = "0x%04x" % self.codepoint
		newlines.append([level+1, "codepoint = %s" % codepoint])
		self._addlines(newlines, lines)


def fromdtd(dtd, xmlname, xmlurl=None):
	"""
	Convert &dtd; information (in the format that is returned by <app>xmlproc</app>s
	<function>dtdparser.load_dtd</function> function) to an &xist; &dom; using the
	<pyref module="ll.xist.ns.xndl"><module>xndl</module></pyref> namespace.
	"""

	node = Namespace(name=xmlname, url=xmlurl)

	xmlns = {} # collects all the values of fixed xmlns attributes (as a set)

	# Add element info
	elements = dtd.get_elements()
	elements.sort()
	for elemname in elements:
		e = dtd.get_elem(elemname)
		model = e.get_content_model()
		if model is None:
			model = "sims.Any()"
		elif model == ("", [], ""):
			model = "sims.Empty()"
		else:
			def extractcont(model):
				if len(model) == 3:
					result = {}
					for cont in model[1]:
						result.update(extractcont(cont))
					return result
				else:
					return {model[0]: None}
			model = extractcont(model)
			newmodel = []
			cls = "Elements"
			for cont in model:
				if cont == "#PCDATA":
					cls = "ElementsOrText"
				else:
					newmodel.append(cont)
			if not newmodel:
				if cls == "ElementsOrText":
					cls = "NoElements"
				else:
					cls = "NoElementsOrText"
			model = "sims.%s(%s)" % (cls, ", ".join(newmodel))
		node.append(Element(name=elemname, model=model))

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
					type = "xsc.IDAttr"
				else:
					type = "xsc.TextAttr"
					if isinstance(a.type, list):
						if len(a.type)>1:
							values = a.type
						else:
							type = "xsc.BoolAttr"
				default = a.default
				if a.decl=="#REQUIRED":
					required = True
				else:
					required = None
				node[-1].append(Attr(name=attrname, type=type, default=default, required=required))
				for v in values:
					node[-1][-1].values.append(v)

	# Add entities
	ents = dtd.get_general_entities()
	ents.sort()
	for entname in ents:
		if entname not in ("quot", "apos", "gt", "lt", "amp"):
			ent = parsers.parseString(dtd.resolve_ge(entname).value)
			node.append(charref(name=entname, codepoint=ord(unicode(ent[0])[0])))

	# if the DTD has exactly one value for all fixed "xmlns" attributes and the user didn't specify an xmlurl, use this one
	if xmlurl is None and len(xmlns)==1:
		node.url = xmlns.popitem()[0]
	return node
