# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<par>An &xist; module that contains classes for describing &xist; namespace
modules. From that info a skeleton implementation of the namespace module
can be generated.</par>
"""


import sys, keyword

from ll.xist import xsc, parsers, sims


class Base(object):
	def __init__(self, name):
		self.name = name
		self.pyname = None

	def assignname(self, names, name=None):
		"""
		<par>Assign a modified version of <arg>name</arg> to <lit>pyname</lit>,
		that is a valid Python identifier. This is done by replacing illegal
		characters with <lit>_</lit> and appending an <lit>_</lit> when the name
		collides with a Python keyword. Furthermore it is made sure that the new
		name is not in the list <arg>names</arg>. (If <arg>name</arg> is <lit>None</lit>
		<lit><self/>.name</lit> is used.)</par>
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
		<par>Return a string, whose value can be used as an intializer for an attribute values.
		(If the value is an <class>int</class> strip the quotes, if it fits into ASCII drop
		the <lit>u</lit> prefix.)</par>
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
	def __init__(self, xmlns=None, doc=None):
		Base.__init__(self, "xmlns")
		self.xmlns = xmlns
		self.doc = doc
		self.content = []

	def __repr__(self):
		return "<%s.%s name=%r url=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, self.url, id(self))

	def __call__(self, *content):
		self.content.extend(content)
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

		lines.append([0, ""])
		lines.append([0, ""])
		lines.append([level, "%s = %s" % (self.pyname, self.simplify(self.xmlns if self.xmlns is not None else "... insert namespace name ..."))])

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
	def __init__(self, name, modeltype=None, modelargs=None, doc=None):
		Base.__init__(self, name)
		self.attrs = []
		self.modeltype = modeltype
		self.modelargs = modelargs
		self.doc = doc

	def __repr__(self):
		return "<%s.%s name=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.name, id(self))

	def __call__(self, *content):
		self.attrs.extend(content)
		return self

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class %s(xsc.Element):" % self.pyname])
		newlines = []
		self._adddoc(newlines, level+1)
		newlines.append([level+1, "xmlns = xmlns"])
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
		self.shared = None # if this attribute is part of a group <lit>shared</lit> will point to the group

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
		newlines.append([level+1, "xmlns = xmlns"])
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
		newlines.append([level+1, "xmlns = xmlns"])
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
		newlines.append([level+1, "xmlns = xmlns"])
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


def fromdtd(dtd, xmlns=None):
	"""
	Convert &dtd; information (in the format that is returned by <app>xmlproc</app>s
	<function>dtdparser.load_dtd</function> function) to an &xist; &dom; using the
	<pyref module="ll.xist.xnd"><module>xnd</module></pyref> namespace.
	"""

	ns = Module(xmlns)

	foundxmlns = set() # collects all the values of fixed xmlns attributes

	# Add element info
	elements = dtd.get_elements()
	elements.sort()
	for elemname in elements:
		dtd_e = dtd.get_elem(elemname)
		e = Element(name=elemname)

		# Add attribute info for this element
		attrs = dtd_e.get_attr_list()
		if len(attrs):
			attrs.sort()
			for attrname in attrs:
				dtd_a = dtd_e.get_attr(attrname)
				if attrname=="xmlns":
					if dtd_a.decl=="#FIXED":
						foundxmlns.add(dtd_a.default)
					continue # skip a namespace declaration
				elif u":" in attrname:
					continue # skip global attributes
				values = []
				if dtd_a.type == "ID":
					type = "xsc.IDAttr"
				else:
					type = "xsc.TextAttr"
					if isinstance(dtd_a.type, list):
						if len(dtd_a.type)>1:
							values = dtd_a.type
						else:
							type = "xsc.BoolAttr"
				default = dtd_a.default
				if dtd_a.decl=="#REQUIRED":
					required = True
				else:
					required = None
				a = Attr(name=attrname, type=type, default=default, required=required)
				for v in values:
					a.values.append(v)
				e.attrs.append(a)
		ns.content.append(e)

	# Iterate through the elements a second time and add model information
	for elemname in elements:
		e = dtd.get_elem(elemname)
		model = e.get_content_model()
		if model is None:
			modeltype = "sims.Any"
			modelargs = None
		elif model == ("", [], ""):
			modeltype = "sims.Empty"
			modelargs = None
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
			modeltype = "sims.Elements"
			modelargs = []
			for cont in model:
				if cont == "#PCDATA":
					modeltype = "sims.ElementsOrText"
				elif cont == "EMPTY":
					modeltype = "sims.Empty"
				else:
					modelargs.append(ns.element(cont))
			if not modelargs:
				if modeltype == "sims.ElementsOrText":
					modeltype = "sims.NoElements"
				else:
					modeltype = "sims.NoElementsOrText"
		e = ns.element(elemname)
		e.modeltype = modeltype
		e.modelargs = modelargs

	# Add entities
	ents = dtd.get_general_entities()
	ents.sort()
	for entname in ents:
		if entname not in ("quot", "apos", "gt", "lt", "amp"):
			ent = parsers.parseString(dtd.resolve_ge(entname).value)
			ns.content.append(CharRef(entname, codepoint=ord(unicode(ent[0])[0])))

	# if the DTD has exactly one value for all fixed "xmlns" attributes and the user didn't specify xmlns, use this one
	if xmlns is None and len(foundxmlns)==1:
		ns.xmlns = foundxmlns.pop()
	return ns
