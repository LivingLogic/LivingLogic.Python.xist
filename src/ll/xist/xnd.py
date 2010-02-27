# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
An XIST module that contains classes for describing XIST namespace modules.
From that info a skeleton implementation of the namespace module can be
generated.
"""


import sys, keyword

from ll.xist import xsc, parsers, sims


__docformat__ = "reStructuredText"


class Base(object):
	def __init__(self, name):
		self.name = name
		self.pyname = None

	def assignname(self, names, name=None):
		"""
		Assign a modified version of :var:`name` to :attr:`pyname`, that is a
		valid Python identifier. This is done by replacing illegal characters
		with ``_`` and appending an ``_`` when the name collides with a Python
		keyword. Furthermore it is made sure that the new name is not in the list
		:var:`names`. (If :var:`name` is :const:`None` ``self.name`` is used.)
		"""
		newname = []
		if name is None:
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
		self.pyname = testname
		names.append(testname)

	@classmethod
	def simplify(cls, value):
		"""
		Return a string whose value can be used as an intializer for an attribute
		value. (If the value is an :class:`int` strip the quotes, if it fits into
		ASCII drop the ``u`` prefix.)
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

	def aspy(self, **options):
		options = Options(**options)
		lines = []
		self._aspy(lines, 0, [], options)
		return "".join("%s%s\n" % (level*options.indent, text) for (level, text) in lines)

	def _addlines(self, newlines, lines):
		l = len(newlines)
		if l==0:
			lines[-1][1] += " pass"
		elif l==1:
			lines[-1][1] += " %s" % newlines[-1][1]
		else:
			lines.extend(newlines)

	def _adddoc(self, lines, level):
		if self.doc is not None:
			lines.append([level, '"""'])
			for line in self.doc.splitlines():
				lines.append([level, line])
			lines.append([level, '"""'])


class Module(Base):
	def __init__(self, doc=None):
		Base.__init__(self, "____")
		self.doc = doc
		self.content = []

	def __repr__(self):
		return "<%s.%s name=%r url=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, self.url, id(self))

	def __call__(self, *content):
		self.content.extend(content)
		return self

	def _findgroups(self):
		"""
		This method finds all attribute groups defined for any attribute. As an
		attribute group can be referenced multiple times (in fact that's the
		reason for the attribute groups existence), we have to make sure to list
		an attribute group only once. Furthermore the attribute groups should
		appear in the order in which they are referenced.
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

	def _aspy(self, lines, level, names, options):
		# used as a variable name for the namespace name (must always work, i.e. be the original name)
		self.assignname(names, "xmlns")

		# assign names to all elements
		for child in self.content:
			if isinstance(child, Element):
				child.assignname(names)
				attrnames = []
				for attr in child.attrs:
					attr.assignname(attrnames)

		# assign names to all processing instructions
		for child in self.content:
			if isinstance(child, ProcInst):
				child.assignname(names)

		# assign names to all entitites
		for child in self.content:
			if isinstance(child, Entity) and not isinstance(child, CharRef):
				child.assignname(names)

		# assign names to all character references
		for child in self.content:
			if isinstance(child, CharRef):
				child.assignname(names)

		# Assign names to attribute groups
		attrgroups = self._findgroups()
		for attrgroup in attrgroups:
			attrgroup.assignname(names)

		lines.append([level, "# -*- coding: %s -*-" % options.encoding])
		lines.append([0, ""])
		lines.append([0, ""])

		self._adddoc(lines, level)

		lines.append([level, "from ll.xist import xsc, sims"])

		# output attribute groups
		for attrgroup in attrgroups:
			lines.append([0, ""])
			lines.append([0, ""])
			attrgroup._aspy(lines, level, names, options)

		# output elements, procinsts, entities and charref
		for node in self.content:
			lines.append([0, ""])
			lines.append([0, ""])
			node._aspy(lines, level, names, options)

		# output schema information for the elements
		if options.model != "no":
			elswithschema = [node for node in self.content if isinstance(node, Element) and not isinstance(node.modeltype, (bool, type(None)))]
			if elswithschema:
				lines.append([0, ""])
				lines.append([0, ""])
				newlines = []
				for node in elswithschema:
					modelargs = []
					if node.modelargs:
						for arg in node.modelargs:
							if isinstance(arg, Element):
								arg = arg.pyname
							modelargs.append(arg)
					newlines.append(("%s.model" % node.pyname, "%s(%s)" % (node.modeltype, ", ".join(modelargs))))
				if options.model == "all":
					for line in newlines:
						lines.append([0, "%s = %s" % line])
				elif options.model == "once":
					newlines.sort(key=lambda l: l[1])
					for (i, line) in enumerate(newlines):
						(var, code) = line
						if i != len(newlines)-1 and code == newlines[i+1][1]:
							code = "\\"
						lines.append([0, "%s = %s" % (var, code)])

	def element(self, name):
		for node in self.content:
			if isinstance(node, Element) and node.name==name:
				return node
		raise ValueError("no element named %r" % name)

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
				group = AttrGroup(attrs[0].name)(attrs[0])
				for attr in attrs:
					attr.share(group)


class Element(Base):
	def __init__(self, name, xmlns=None, modeltype=None, modelargs=None, doc=None):
		Base.__init__(self, name)
		self.xmlns = xmlns
		self.attrs = []
		self.modeltype = modeltype
		self.modelargs = modelargs
		self.doc = doc

	def __repr__(self):
		return "<%s.%s name=%r xmlns=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, self.xmlns, id(self))

	def __call__(self, *content):
		self.attrs.extend(content)
		return self

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class %s(xsc.Element):" % self.pyname])
		newlines = []
		self._adddoc(newlines, level+1)
		if self.xmlns is not None:
			newlines.append([level+1, "xmlns = %s" % self.simplify(self.xmlns)])
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(self.name)])
		# only output model, if it is a bool, otherwise it might reference other element,
		# in which case this is done after all element classes have been defined
		if isinstance(self.modeltype, bool):
			newlines.append([level+1, "model = %r" % self.modeltype])

		if len(self.attrs):
			# find the attribute groups our elements are in
			# this means we don't have to define these attributes ourselves, but have to derive from the attribute group
			groups = []
			groupset = {}
			nogroup = []
			for attr in self.attrs:
				if attr.shared is not None:
					if tuple(attr.shared.attrs) not in groupset:
						groups.append(attr.shared)
				else:
					nogroup.append(attr)
			if groups:
				base = ", ".join(group.pyname for group in groups)
			else:
				base = "xsc.Element.Attrs"
			newlines.append([level+1, "class Attrs(%s):" % base])
			if nogroup:
				localnames = []
				for attr in nogroup:
					attr._aspy(newlines, level+2, localnames, options)
			else:
				newlines.append([level+2, "pass"])
		self._addlines(newlines, lines)


class AttrGroup(Base):
	id = 0
	def __init__(self, name):
		if name is None:
			name = "attrgroup_%d" % self.__class__.id
			self.__class__.id += 1
		Base.__init__(self, name)
		self.attrs = []

	def __call__(self, *content):
		self.attrs.extend(content)
		return self

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class %s(xsc.Element.Attrs):" % self.pyname])
		localnames = []
		for attr in self.attrs:
			attr._aspy(lines, level+1, localnames, options)


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
		self.shared = None # if this attribute is part of a group ``shared`` will point to the group

	def __repr__(self):
		return "<%s.%s name=%r type=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, self.type, id(self))

	def _aspy(self, lines, level, names, options):
		name = self.name
		if isinstance(self.type, type):
			basename = "%s.%s" % (self.type.__module__, self.type.__name__)
		else:
			basename = self.type
		if basename.startswith("ll.xist.xsc."):
			basename = basename[8:]
		lines.append([level, "class %s(%s):" % (self.pyname, basename)])
		newlines = []
		self._adddoc(newlines, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(self.name)])
		if self.values:
			values = "(%s)" % ", ".join(str(self.simplify(value)) for value in self.values)
			newlines.append([level+1, "values = %s" % (values, )])
		if self.default and options.defaults:
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

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class %s(xsc.ProcInst):" % self.pyname])
		newlines = []
		self._adddoc(newlines, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(self.name)])
		self._addlines(newlines, lines)


class Entity(Base):
	def __init__(self, name, doc=None):
		Base.__init__(self, name)
		self.doc = doc

	def __repr__(self):
		return "<%s.%s name=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, id(self))

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class %s(xsc.Entity):" % self.pyname])
		newlines = []
		self._adddoc(newlines, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(self.name)])
		self._addlines(newlines, lines)


class CharRef(Entity):
	def __init__(self, name, codepoint, doc=None):
		Entity.__init__(self, name, doc)
		self.codepoint = codepoint

	def __repr__(self):
		return "<%s.%s name=%r codepoint=0x%x at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, self.codepoint, id(self))

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class %s(xsc.CharRef):" % self.pyname])
		newlines = []
		self._adddoc(newlines, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = %s" % self.simplify(self.name)])
		if self.codepoint > 0xffff:
			codepoint = "0x%08x" % self.codepoint
		else:
			codepoint = "0x%04x" % self.codepoint
		newlines.append([level+1, "codepoint = %s" % codepoint])
		self._addlines(newlines, lines)


class Options(object):
	def __init__(self, indent="\t", encoding=None, defaults=False, model="once"):
		self.indent = indent
		if encoding is None:
			encoding = sys.getdefaultencoding()
		self.encoding = encoding
		self.defaults = defaults
		self.model = model
