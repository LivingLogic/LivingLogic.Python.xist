# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST module that contains classes for describing XIST namespace modules.
From that info a skeleton implementation of the namespace module can be
generated.
"""


import sys, keyword, collections


__docformat__ = "reStructuredText"


def _simplify(value):
	"""
	Return a string whose value can be used as an intializer for an attribute
	value. (If the value is an :class:`int` strip the quotes)
	"""
	try:
		value = int(value)
	except ValueError:
		if '"' in value:
			value = repr(value)
		else:
			value = '"{}"'.format(repr(value)[1:-1])
	return value


class Error(Exception):
	pass


class RedefinedElementError(Error):
	def __init__(self, oldelement, newelement, duplicates):
		self.oldelement = oldelement
		self.newelement = newelement
		self.duplicates = duplicates

	def __str__(self):
		msg = "element named {0.oldelement.name} redefined".format(self)
		if self.duplicates == "allow":
			msgs = []
			if self.oldelement.attrs != self.newelement.attrs:
				# New element has different attributes
				removed = [attr.name for attr in self.oldelement.attrs.values() if attr.name not in self.newelement.attrs]
				if removed:
					msgs.append("attribute{} {} removed".format("s" if len(removed) > 1 else "", ", ".join(removed)))
				added = [attr.name for attr in self.newelement.attrs.values() if attr.name not in self.oldelement.attrs]
				if added:
					msgs.append("attribute{} {} added".format("s" if len(added) > 1 else "", ", ".join(added)))
			if msgs:
				msg += " ({})".format("; ".join(msgs))
		elif self.duplicates == "merge":
			incompatible = [attr.name for attr in self.oldelement.attrs if attr != self.newelement.attrs[attr.name]]
			msg += " (attribute{} {} incompatible)".format("s" if len(added) > 1 else "", ", ".join(incompatible))
		# else self.duplicates == "reject"
		return msg


class RedefinedProcInstError(Error):
	def __init__(self, oldprocinst, newprocinst, duplicates):
		self.oldprocinst = oldprocinst
		self.newprocinst = newprocinst
		self.duplicates = duplicates

	def __str__(self):
		return "procinst named {0.oldprocinst.named} redefined".format(self)


class RedefinedEntityError(Error):
	def __init__(self, oldentity, newentity, duplicates):
		self.oldentity = oldentity
		self.newentity = newentity
		self.duplicates = duplicates

	def __str__(self):
		return "entity named {0.oldentity.named} redefined".format(self)


class RedefinedCharRefError(Error):
	def __init__(self, oldcharref, newcharref, duplicates):
		self.oldcharref = oldcharref
		self.newcharref = newcharref
		self.duplicates = duplicates

	def __str__(self):
		return "charref named {0.oldcharref.named} with code point {0.oldcharref.codepoint} redefined with codepoint {0.newcharref.codepoint}".format(self)


def findname(basename, names):
	"""
	Return a new valid Python identifier based on :obj:`basename`, i.e. a name
	that is based on :obj:`basename`, a valid Python identifier and not in
	:obj:`names. Illegal characters in :obj:`basename` are replaced with ``_``
	and an ``_`` appendedwhen the name collides with a Python keyword.
	"""
	basename = "".join(c if "a" <= c <= "z" or "A" <= c <= "Z" or "0" <= c <= "9" or c == "_" else "_" for c in basename)
	testname = basename
	if keyword.iskeyword(basename):
		testname += "_"
	suffix = 2
	while testname in names:
		testname = "{0}{1}".format(basename, suffix)
		suffix += 1
	return testname


def _addlines(lines, newlines):
	l = len(newlines)
	if l == 0:
		lines[-1][1] += " pass"
	elif l == 1:
		lines[-1][1] += " {}".format(newlines[-1][1])
	else:
		lines.extend(newlines)


def _adddoc(lines, doc, level):
	if doc is not None:
		lines.append([level, '"""'])
		for line in doc.splitlines():
			lines.append([level, line])
		lines.append([level, '"""'])


class Module:
	def __init__(self, doc=None, defaultxmlns=None, indent="\t", encoding=None, defaults=False, model="fullonce", duplicates="reject"):
		self.doc = doc
		self.defaultxmlns = defaultxmlns
		self.indent = indent
		self.encoding = encoding if encoding is not None else sys.getdefaultencoding()
		self.defaults = defaults
		self.model = model
		self.duplicates = duplicates
		self.elements = collections.OrderedDict() # Maps (namespace name, element name) to ``xnd.Element``
		self.procinsts = collections.OrderedDict() # Maps pi target to ``xnd.ProcInst``
		self.entities = collections.OrderedDict() # Maps entity name to ``xnd.Entity``
		self.charrefs = collections.OrderedDict() # Maps charref name to ``xnd.CharRef``

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} url={0.url!r} at {1:#x}>".format(self, id(self))

	def __iadd__(self, node):
		node._add(self)
		return self

	def __str__(self):
		lines = []
		self._aspy(lines, 0, set(), self)
		return "".join("{}{}\n".format(level*self.indent, text) for (level, text) in lines)

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
		for node in self.elements.values():
			for attr in node.attrs.values():
				if attr.shared is not None and attr.shared not in attrgroupset:
					attrgroups.append(attr.shared)
					attrgroupset[attr.shared] = True
		return attrgroups

	def _aspy(self, lines, level, names, module):
		# Find all namespaces
		self._xmlnames = dict.fromkeys(e.xmlns for e in self.elements.values() if e.xmlns is not None)
		# Assign names to namespaces
		for xmlns in self._xmlnames:
			varname = findname("xmlns", names)
			self._xmlnames[xmlns] = varname
			names.add(varname)

		# assign names to all elements
		for child in self.elements.values():
			child.assignpyname(names)
			attrnames = set()
			for attr in child.attrs.values():
				attr.assignpyname(attrnames)

		# assign names to all processing instructions
		for child in self.procinsts.values():
			child.assignpyname(names)

		# assign names to all entitites
		for child in self.entities.values():
			child.assignpyname(names)

		# assign names to all character references
		for child in self.charrefs.values():
			child.assignpyname(names)

		# Assign names to attribute groups
		attrgroups = self._findgroups()
		for attrgroup in attrgroups:
			attrgroup.assignpyname(names)

		lines.append([level, "# -*- coding: {} -*-".format(module.encoding)])
		lines.append([0, ""])
		lines.append([0, ""])

		_adddoc(lines, self.doc, level)

		lines.append([level, "from ll.xist import xsc, sims"])

		# output namespace names
		if self._xmlnames:
			lines.append([0, ""])
			lines.append([0, ""])
			for (xmlns, varname) in self._xmlnames.items():
				lines.append([level, "{} = {!r}".format(varname, xmlns)])

		# output attribute groups
		for attrgroup in attrgroups:
			lines.append([0, ""])
			lines.append([0, ""])
			attrgroup._aspy(lines, level, names, module)

		# output elements, procinsts, entities and charref
		for nodetype in ("elements", "procinsts", "entities", "charrefs"):
			for node in getattr(self, nodetype).values():
				lines.append([0, ""])
				lines.append([0, ""])
				node._aspy(lines, level, names, module)

		# output schema information for the elements
		if module.model != "none":
			elswithschema = [node for node in self.elements.values() if not isinstance(node.modeltype, (bool, type(None)))]
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
					newlines.append(("{}.model".format(node.pyname), "{}({})".format(node.modeltype, ", ".join(modelargs))))
				if self.model in ("simple", "fullall"):
					for line in newlines:
						lines.append([0, "{} = {}".format(*line)])
				elif self.model == "fullonce":
					newlines.sort(key=lambda l: l[1])
					for (i, line) in enumerate(newlines):
						(var, code) = line
						if i != len(newlines)-1 and code == newlines[i+1][1]:
							code = "\\"
						lines.append([0, "{} = {}".format(var, code)])
				else:
					raise ValueError("unknown sims mode {!r}".format(self.model))

	def shareattrs(self, all):
		# collect all identical attributes into lists
		identicalattrs = collections.OrderedDict()
		for node in self.elements.values():
			for attr in node.attrs.values():
				if attr.shared is None: # skip attributes that are already shared
					ident = attr.ident()
					try:
						attrs = identicalattrs[ident]
					except KeyError:
						attrs = identicalattrs[ident] = []
					attrs.append(attr)
		for (ident, attrs) in identicalattrs.items():
			# if the attribute appears more than once (or all attributes should be shared), define a group for it
			if all or len(attrs) > 1:
				group = AttrGroup(attrs[0].name)(attrs[0])
				for attr in attrs:
					attr.share(group)


class Named:
	def __init__(self, name):
		self.name = name
		self.pyname = None

	def __ne__(self, other):
		return not self == other

	def assignpyname(self, names, name=None):
		"""
		Assign a Python identifier to :obj:`self` (using either :obj:`name` or
		:obj:`self.name`). This uses :func:`findname` to create a valid Python
		identifier that is not in :obj:`names`.
		"""
		if name is None:
			name = self.name
		name = findname(name, names)
		self.pyname = name
		names.add(name)


class Element(Named):
	def __init__(self, xmlns, name, modeltype=None, modelargs=None, doc=None):
		Named.__init__(self, name)
		self.xmlns = xmlns
		self.attrs = collections.OrderedDict()
		self.modeltype = modeltype
		self.modelargs = modelargs
		self.doc = doc

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} xmlns={0.xmlns!r} attrs={0.attrs!r} at {1:#x}>".format(self, id(self))

	def __eq__(self, other):
		# Don't compare the models
		return type(other) is Element and self.name == other.name and self.xmlns == other.xmlns and self.attrs == other.attrs

	def __hash__(self):
		return hash(self.name) ^ hash(self.xmlns) # don't include the attributes in the hash value, as they're unhashable

	def __iadd__(self, attr):
		self.attrs[attr.name] = attr
		return self

	def _add(self, module):
		key = (self.xmlns, self.name)
		if key in module.elements:
			oldelement = module.elements[key]
			if module.duplicates == "reject":
				raise RedefinedElementError(oldelement, self, duplicates=module.duplicates)
			elif module.duplicates == "allow":
				if module.elements[self.name] != self:
					raise RedefinedElementError(oldelement, self, duplicates=module.duplicates)
			else: # if duplicates == "merge"
				for attr in self.attrs.values():
					if attr.name in self.attrs:
						if attr != self.attrs[attr.name]:
							raise RedefinedElementError(oldelement, self, duplicates=module.duplicates)
					else:
						self.attrs[attr.name] = attr
		else:
			module.elements[key] = self
		if self.xmlns is None:
			self.xmlns = module.defaultxmlns

	def _aspy(self, lines, level, names, module):
		lines.append([level, "class {}(xsc.Element):".format(self.pyname)])
		newlines = []
		_adddoc(newlines, self.doc, level+1)
		if self.xmlns is not None:
			try:
				xmlns = module._xmlnames[self.xmlns] # Use variable name
			except KeyError:
				xmlns = _simplify(self.xmlns) # Use literal
			newlines.append([level+1, "xmlns = {}".format(xmlns)])
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = {}".format(_simplify(self.name))])
		# only output model if it is a bool, otherwise it might reference other element,
		# in which case this is done after all element classes have been defined
		if isinstance(self.modeltype, bool):
			newlines.append([level+1, "model = {!r}".format(self.modeltype)])

		if self.attrs:
			# find the attribute groups our elements are in
			# this means we don't have to define these attributes ourselves, but have to derive from the attribute group
			groups = []
			groupset = {}
			nogroup = []
			for attr in self.attrs.values():
				if attr.shared is not None:
					if tuple(attr.shared.attrs) not in groupset:
						groups.append(attr.shared)
				else:
					nogroup.append(attr)
			if groups:
				base = ", ".join(group.pyname for group in groups)
			else:
				base = "xsc.Element.Attrs"
			newlines.append([level+1, "class Attrs({}):".format(base)])
			if nogroup:
				localnames = []
				for attr in nogroup:
					attr._aspy(newlines, level+2, localnames, module)
			else:
				newlines.append([level+2, "pass"])
		_addlines(lines, newlines)


class AttrGroup(Named):
	id = 0

	def __init__(self, name):
		if name is None:
			name = "attrgroup_{}".format(self.__class__.id)
			self.__class__.id += 1
		Named.__init__(self, name)
		self.attrs = []

	def __call__(self, *content):
		self.attrs.extend(content)
		return self

	def _aspy(self, lines, level, names, module):
		lines.append([level, "class {}(xsc.Element.Attrs):".format(self.pyname)])
		localnames = []
		for attr in self.attrs:
			attr._aspy(lines, level+1, localnames, module)


class Attr(Named):
	def __init__(self, name, type, required=False, default=None, values=None, doc=None):
		Named.__init__(self, name)
		self.doc = doc
		self.type = type
		self.required = required
		self.default = default
		self.values = tuple(values) if values is not None else ()
		self.shared = None # if this attribute is part of a group ``shared`` will point to the group

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} type={0.type!r} at {1:#x}>".format(self, id(self))

	def __eq__(self, other):
		return type(other) is Attr and self.name == other.name and self.type == other.type and self.required == other.required and self.default == other.default and self.values == other.values

	def __hash__(self):
		return hash(self.name) ^ hash(self.type) ^ hash(self.required) ^ hash(self.default) ^ hash(self.values)

	def _aspy(self, lines, level, names, module):
		name = self.name
		if isinstance(self.type, type):
			basename = "{0.type.__module__}.{0.type.__name__}".format(self)
		else:
			basename = self.type
		if basename.startswith("ll.xist.xsc."):
			basename = basename[8:]
		lines.append([level, "class {}({}):".format(self.pyname, basename)])
		newlines = []
		_adddoc(newlines, self.doc, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = {}".format(_simplify(self.name))])
		if self.values:
			values = "({})".format(", ".join(str(_simplify(value)) for value in self.values))
			newlines.append([level+1, "values = {}".format(values)])
		if self.default and module.defaults:
			newlines.append([level+1, "default = {}".format(_simplify(self.default))])
		if self.required:
			newlines.append([level+1, "required = True"])
		_addlines(lines, newlines)

	def share(self, group):
		assert self.shared is None, "cannot share attr {!r} twice".format(self)
		self.shared = group

	def ident(self):
		return (self.name, self.type, self.required, self.default, tuple(self.values))


class ProcInst(Named):
	def __init__(self, name, doc=None):
		Named.__init__(self, name)
		self.doc = doc

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} at {1:#x}>".format(self, id(self))

	def _add(self, module):
		if self.name in module.procinsts:
			if module.duplicates == "reject":
				raise RedefinedProcInstError(module.procinsts[self.name], self, module.duplicates)
		else:
			module.procinsts[self.name] = self

	def _aspy(self, lines, level, names, module):
		lines.append([level, "class {}(xsc.ProcInst):".format(self.pyname)])
		newlines = []
		_adddoc(newlines, self.doc, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = {}".format(_simplify(self.name))])
		_addlines(lines, newlines)


class Entity(Named):
	def __init__(self, name, doc=None):
		Named.__init__(self, name)
		self.doc = doc

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} at {1:#x}>".format(self, id(self))

	def __eq__(self, other):
		return type(other) is CharRef and self.name == other.name

	def _add(self, module):
		if self.name in module.entities:
			if module.duplicates == "reject":
				raise RedefinedEntityError(module.entities[self.name], self, module.duplicates)
		else:
			module.entities[self.name] = self

	def _aspy(self, lines, level, names, module):
		lines.append([level, "class {}(xsc.Entity):".format(self.pyname)])
		newlines = []
		_adddoc(newlines, self.doc, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = {}".format(_simplify(self.name))])
		_addlines(lines, newlines)


class CharRef(Entity):
	def __init__(self, name, codepoint, doc=None):
		Entity.__init__(self, name, doc)
		self.codepoint = codepoint

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__qualname__} name={0.name!r} codepoint={0.codepoint:#x} at {1:#x}>".format(self, id(self))

	def __eq__(self, other):
		return type(other) is CharRef and self.name == other.name and self.codepoint == other.codepoint

	def _add(self, module):
		if self.name in module.charrefs:
			if module.duplicates == "reject":
				oldcharref = module.charrefs[self.name]
				raise RedefinedCharRefError(oldcharref, self, module.duplicates)
			else: # duplicates in ("allow", "merge"):
				oldcharref = module.charrefs[self.name]
				if oldcharref != self:
					raise RedefinedCharRefError(oldcharref, self, module.duplicates)
		else:
			module.charrefs[self.name] = self

	def _aspy(self, lines, level, names, module):
		lines.append([level, "class {}(xsc.CharRef):".format(self.pyname)])
		newlines = []
		_adddoc(newlines, self.doc, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = {}".format(_simplify(self.name))])
		if self.codepoint > 0xffff:
			fmt = "#010x"
		elif self.codepoint > 0xff:
			fmt = "#06x"
		else:
			fmt = "#02x"
		newlines.append([level+1, "codepoint = {0:{1}}".format(self.codepoint, fmt)])
		_addlines(lines, newlines)
