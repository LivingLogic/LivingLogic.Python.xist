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


import sys, keyword, collections

from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


def simplify(value):
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
				value = u'u"{}"'.format(repr(value)[2:-1])
		else:
			if '"' in value:
				value = repr(value)
			else:
				value = u'"{}"'.format(repr(value)[1:-1])
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
				removed = [attr.name for attr in self.oldelement.attrs.itervalues() if attr.name not in self.newelement.attrs]
				if removed:
					msgs.append("attribute{} {} removed".format("s" if len(removed) > 1 else "", ", ".join(removed)))
				added = [attr.name for attr in self.newelement.attrs.itervalues() if attr.name not in self.oldelement.attrs]
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
		return "charref named {0.oldcharref.named} with codepoint {0.oldcharref.codepoint} redefined with codepoint {0.newcharref.codepoint}".format(self)


class Base(object):
	def __init__(self, name):
		self.name = name
		self.pyname = None

	def __ne__(self, other):
		return not self == other

	def assignpyname(self, names, name=None):
		"""
		Assign a modified version of :var:`name` to :attr:`pyname`, that is a
		valid Python identifier. This is done by replacing illegal characters
		with ``_`` and appending an ``_`` when the name collides with a Python
		keyword. Furthermore it is made sure that the new name is not in the list
		:var:`names`. (If :var:`name` is :const:`None` ``self.name`` is used.)
		"""
		if name is None:
			name = self.name
		name = "".join(c if "a" <= c <= "z" or "A" <= c <= "Z" or "0" <= c <= "9" or c == "_" else "_" for c in name)
		testname = name
		if keyword.iskeyword(name):
			testname += "_"
		suffix = 2
		while testname in names:
			testname = "{0}{1}".format(name, suffix)
			suffix += 1
		self.pyname = testname
		names.add(testname)

	def aspy(self, **options):
		options = Options(**options)
		lines = []
		self._aspy(lines, 0, set(), options)
		return u"".join(u"{}{}\n".format(level*options.indent, text) for (level, text) in lines)

	def _addlines(self, newlines, lines):
		l = len(newlines)
		if l==0:
			lines[-1][1] += u" pass"
		elif l==1:
			lines[-1][1] += u" {}".format(newlines[-1][1])
		else:
			lines.extend(newlines)

	def _adddoc(self, lines, level):
		if self.doc is not None:
			lines.append([level, u'"""'])
			for line in self.doc.splitlines():
				lines.append([level, line])
			lines.append([level, u'"""'])


class Module(Base):
	def __init__(self, doc=None):
		Base.__init__(self, "____")
		self.doc = doc
		self.elements = collections.OrderedDict() # Maps (element name, namespace name) to ``xnd.Element``
		self.procinsts = collections.OrderedDict() # Maps pi target to ``xnd.ProcInst``
		self.entities = collections.OrderedDict() # Maps entity name to ``xnd.Entity``
		self.charrefs = collections.OrderedDict() # Maps charref name to ``xnd.CharRef``

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} name={0.name!r} url={0.url!r} at {1:#x}>".format(self, id(self))

	def __call__(self, *content):
		for thing in content:
			thing.add(self)
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
		for node in self.elements.itervalues():
			for attr in node.attrs.itervalues():
				if attr.shared is not None and attr.shared not in attrgroupset:
					attrgroups.append(attr.shared)
					attrgroupset[attr.shared] = True
		return attrgroups

	def _aspy(self, lines, level, names, options):
		# used as a variable name for the namespace name (must always work, i.e. be the original name)
		self.assignpyname(names, "xmlns")

		# assign names to all elements
		for child in self.elements.itervalues():
			child.assignpyname(names)
			attrnames = set()
			for attr in child.attrs.itervalues():
				attr.assignpyname(attrnames)

		# assign names to all processing instructions
		for child in self.procinsts.itervalues():
			child.assignpyname(names)

		# assign names to all entitites
		for child in self.entities.itervalues():
			child.assignpyname(names)

		# assign names to all character references
		for child in self.charrefs.itervalues():
			child.assignpyname(names)

		# Assign names to attribute groups
		attrgroups = self._findgroups()
		for attrgroup in attrgroups:
			attrgroup.assignpyname(names)

		lines.append([level, "# -*- coding: {} -*-".format(options.encoding)])
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
		for nodetype in ("elements", "procinsts", "entities", "charrefs"):
			for node in getattr(self, nodetype).itervalues():
				lines.append([0, ""])
				lines.append([0, ""])
				node._aspy(lines, level, names, options)

		# output schema information for the elements
		if options.model != "none":
			elswithschema = [node for node in self.elements.itervalues() if not isinstance(node.modeltype, (bool, type(None)))]
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
				if options.model in ("simple", "fullall"):
					for line in newlines:
						lines.append([0, "{} = {}".format(*line)])
				elif options.model == "fullonce":
					newlines.sort(key=lambda l: l[1])
					for (i, line) in enumerate(newlines):
						(var, code) = line
						if i != len(newlines)-1 and code == newlines[i+1][1]:
							code = "\\"
						lines.append([0, "{} = {}".format(var, code)])
				else:
					raise ValueError("unknown sims mode {!r}".format(options.model))

	def shareattrs(self, all):
		# collect all identical attributes into lists
		identicalattrs = collections.OrderedDict()
		for node in self.elements.itervalues():
			for attr in node.attrs.itervalues():
				if attr.shared is None: # skip attributes that are already shared
					ident = attr.ident()
					try:
						attrs = identicalattrs[ident]
					except KeyError:
						attrs = []
						identicalattrs[ident] = attrs
					attrs.append(attr)
		for (ident, attrs) in identicalattrs.iteritems():
			# if the attribute appears more than once (or all attributes should be shared), define a group for it
			if all or len(attrs) > 1:
				group = AttrGroup(attrs[0].name)(attrs[0])
				for attr in attrs:
					attr.share(group)


class Element(Base):
	def __init__(self, name, xmlns=None, modeltype=None, modelargs=None, doc=None):
		Base.__init__(self, name)
		self.xmlns = xmlns
		self.attrs = collections.OrderedDict()
		self.modeltype = modeltype
		self.modelargs = modelargs
		self.doc = doc

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} name={0.name!r} xmlns={0.xmlns!r} attrs={0.attrs!r} at {1:#x}>".format(self, id(self))

	def __eq__(self, other):
		# Don't compare the models
		return type(other) is Element and self.name == other.name and self.xmlns == other.xmlns and self.attrs == other.attrs

	def __call__(self, *attrs):
		for attr in attrs:
			self.attrs[attr.name] = attr
		return self

	def add(self, module, duplicates="reject"):
		key = (self.name, self.xmlns)
		if key in module.elements:
			oldelement = module.elements[key]
			if duplicates == "reject":
				raise RedefinedElementError(oldelement, self, duplicates=duplicates)
			elif duplicates == "allow":
				if module.elements[self.name] != self:
					raise RedefinedElementError(oldelement, self, duplicates=duplicates)
			else: # if duplicates == "merge"
				for attr in self.attrs.itervalues():
					if attr.name in self.attrs:
						if attr != self.attrs[attr.name]:
							raise RedefinedElementError(oldelement, self, duplicates=duplicates)
					else:
						self.attrs[attr.name] = attr
		else:
			module.elements[key] = self

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class {}(xsc.Element):".format(self.pyname)])
		newlines = []
		self._adddoc(newlines, level+1)
		if self.xmlns is not None:
			newlines.append([level+1, "xmlns = {}".format(simplify(self.xmlns))])
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = {}".format(simplify(self.name))])
		# only output model, if it is a bool, otherwise it might reference other element,
		# in which case this is done after all element classes have been defined
		if isinstance(self.modeltype, bool):
			newlines.append([level+1, "model = {!r}".format(self.modeltype)])

		if self.attrs:
			# find the attribute groups our elements are in
			# this means we don't have to define these attributes ourselves, but have to derive from the attribute group
			groups = []
			groupset = {}
			nogroup = []
			for attr in self.attrs.itervalues():
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
					attr._aspy(newlines, level+2, localnames, options)
			else:
				newlines.append([level+2, "pass"])
		self._addlines(newlines, lines)


class AttrGroup(Base):
	id = 0
	def __init__(self, name):
		if name is None:
			name = "attrgroup_{}".format(self.__class__.id)
			self.__class__.id += 1
		Base.__init__(self, name)
		self.attrs = []

	def __call__(self, *content):
		self.attrs.extend(content)
		return self

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class {}(xsc.Element.Attrs):".format(self.pyname)])
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
		self.values = tuple(values) if values is not None else ()
		self.shared = None # if this attribute is part of a group ``shared`` will point to the group

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} name={0.name!r} type={0.type!r} at {1:#x}>".format(self, id(self))

	def __eq__(self, other):
		return type(other) is Attr and self.name == other.name and self.type == other.type and self.required == other.required and self.default == other.default and self.values == other.values

	def __hash__(self):
		return hash(self.name) ^ hash(self.type) ^ hash(self.required) ^ hash(self.default) ^ hash(self.values)

	def _aspy(self, lines, level, names, options):
		name = self.name
		if isinstance(self.type, type):
			basename = "{0.type.__module__}.{0.type.__name__}".format(self)
		else:
			basename = self.type
		if basename.startswith("ll.xist.xsc."):
			basename = basename[8:]
		lines.append([level, "class {}({}):".format(self.pyname, basename)])
		newlines = []
		self._adddoc(newlines, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = {}".format(simplify(self.name))])
		if self.values:
			values = "({})".format(", ".join(str(simplify(value)) for value in self.values))
			newlines.append([level+1, "values = {}".format(values)])
		if self.default and options.defaults:
			newlines.append([level+1, "default = {}".format(simplify(self.default))])
		if self.required:
			newlines.append([level+1, "required = True"])
		self._addlines(newlines, lines)

	def share(self, group):
		assert self.shared is None, "cannot share attr {!r} twice".format(self)
		self.shared = group

	def ident(self):
		return (self.name, self.type, self.required, self.default, tuple(self.values))


class ProcInst(Base):
	def __init__(self, name, doc=None):
		Base.__init__(self, name)
		self.doc = doc

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} name={0.name!r} at {1:#x}>".format(self, id(self))

	def add(self, module, duplicates="reject"):
		if self.name in module.procinsts:
			if duplicates == "reject":
				raise RedefinedProcInstError(module.procinsts[self.name], self, duplicates)
		else:
			module.procinsts[self.name] = self

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class {}(xsc.ProcInst):".format(self.pyname)])
		newlines = []
		self._adddoc(newlines, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = {}".format(simplify(self.name))])
		self._addlines(newlines, lines)


class Entity(Base):
	def __init__(self, name, doc=None):
		Base.__init__(self, name)
		self.doc = doc

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} name={0.name!r} at {1:#x}>".format(self, id(self))

	def __eq__(self, other):
		return type(other) is CharRef and self.name == other.name

	def add(self, module, duplicates="reject"):
		if self.name in module.entities:
			if duplicates == "reject":
				raise RedefinedEntityError(module.entities[self.name], self, duplicates)
		else:
			module.entities[self.name] = self

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class {}(xsc.Entity):".format(self.pyname)])
		newlines = []
		self._adddoc(newlines, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = {}".format(simplify(self.name))])
		self._addlines(newlines, lines)


class CharRef(Entity):
	def __init__(self, name, codepoint, doc=None):
		Entity.__init__(self, name, doc)
		self.codepoint = codepoint

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} name={0.name!r} codepoint={0.codepoint:#x} at {1:#x}>".format(self, id(self))

	def __eq__(self, other):
		return type(other) is CharRef and self.name == other.name and self.codepoint == other.codepoint

	def add(self, module, duplicates="reject"):
		if self.name in module.charrefs:
			if duplicates == "reject":
				raise RedefinedCharRefError(oldcharref, self, duplicates)
			else: # duplicates in ("allow", "merge"):
				oldcharref = module.charrefs[self.name]
				if oldcharref != self:
					raise RedefinedCharRefError(oldcharref, self, duplicates)
		else:
			module.charrefs[self.name] = self

	def _aspy(self, lines, level, names, options):
		lines.append([level, "class {}(xsc.CharRef):".format(self.pyname)])
		newlines = []
		self._adddoc(newlines, level+1)
		if self.pyname != self.name:
			newlines.append([level+1, "xmlname = {}".format(simplify(self.name))])
		if self.codepoint > 0xffff:
			fmt = "#010x"
		elif self.codepoint > 0xff:
			fmt = "#06x"
		else:
			fmt = "#02x"
		newlines.append([level+1, "codepoint = {0:{1}}".format(self.codepoint, fmt)])
		self._addlines(newlines, lines)


class Options(object):
	def __init__(self, indent="\t", encoding=None, defaults=False, model="fullonce"):
		self.indent = indent
		if encoding is None:
			encoding = sys.getdefaultencoding()
		self.encoding = encoding
		self.defaults = defaults
		self.model = model
