# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2009-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


__docformat__ = "reStructuredText"

import os, collections, contextlib

from ll import url
from ll.xist import xsc, sims
from ll.xist.ns import doc


try:
	from docutils import core, nodes, utils, parsers, frontend
	from docutils.parsers.rst import roles
	from docutils.parsers.rst.languages import en
except ImportError:
	pass
else:
	class mod(nodes.literal):
		pass

	roles.register_generic_role("mod", mod)
	en.roles["mod"] = "mod"

	class class_(nodes.literal):
		pass

	roles.register_generic_role("class", class_)
	en.roles["class"] = "class"

	class func(nodes.literal):
		pass

	roles.register_generic_role("func", func)
	en.roles["func"] = "func"

	class meth(nodes.literal):
		pass

	roles.register_generic_role("meth", meth)
	en.roles["meth"] = "meth"

	class obj(nodes.literal):
		pass

	roles.register_generic_role("obj", obj)
	en.roles["obj"] = "obj"

	class exc(nodes.literal):
		pass

	roles.register_generic_role("exc", exc)
	en.roles["exc"] = "exc"

	class attr(nodes.literal):
		pass

	roles.register_generic_role("attr", attr)
	en.roles["attr"] = "attr"

	class prop(nodes.literal):
		pass

	roles.register_generic_role("prop", prop)
	en.roles["prop"] = "prop"

	class option(nodes.literal):
		pass

	roles.register_generic_role("option", option)
	en.roles["option"] = "option"

	class const(nodes.literal):
		pass

	roles.register_generic_role("const", const)
	en.roles["const"] = "const"

	class file(nodes.literal):
		pass

	roles.register_generic_role("file", file)
	en.roles["file"] = "file"

	class dir(nodes.literal):
		pass

	roles.register_generic_role("dir", dir)
	en.roles["dir"] = "dir"

	class data(nodes.literal):
		pass

	roles.register_generic_role("data", data)
	en.roles["data"] = "data"


class DocTypeHTML(xsc.DocType):
	"""
	document type for ReST
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'document PUBLIC "+//IDN docutils.sourceforge.net//DTD Docutils Generic//EN//XML" "http://docutils.sourceforge.net/docs/ref/docutils.dtd"')


class refuriattrs(xsc.Attrs):
	class refuri(xsc.URLAttr):
		"External reference to a URI/URL"


class refidattrs(xsc.Attrs):
	class refid(xsc.TextAttr):
		"Internal reference to the `id` attribute of an element."


class backrefsattrs(xsc.Attrs):
	class backrefs(xsc.TextAttr):
		"Space-separated list of id references, for backlinks."


class refnameattrs(xsc.Attrs):
	class refname(xsc.TextAttr):
		"""
		Internal reference to the ``name`` attribute of an element. On a
		'target' element, 'refname' indicates an indirect target which may
		resolve to either an internal or external reference.
		"""


class referenceattrs(refuriattrs, refidattrs, refnameattrs):
	"Collected hyperlink reference attributes."


class anonymousattrs(xsc.Attrs):
	class anonymous(xsc.TextAttr):
		"Unnamed hyperlink"


class autoattrs(xsc.Attrs):
	class auto(xsc.TextAttr):
		"Auto-numbered footnote or title."


class alignhattrs(xsc.Attrs):
	class align(xsc.TextAttr):
		values = ("left", "center", "right")


class alignhvattrs(xsc.Attrs):
	class align(xsc.TextAttr):
		values = ("top", "middle", "bottom", "left", "center", "right")


xmlns = "http://docutils.sourceforge.net/ns"


class BaseElement(xsc.Element):
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class ids(xsc.TextAttr):
			"``id`` is a unique identifier, typically assigned by the system."
		class names(xsc.TextAttr):
			"``name`` is an identifier assigned in the markup."
		class dupnames(xsc.TextAttr):
			"``dupname`` is the same as ``name``, used when it's a duplicate."
		class source(xsc.TextAttr):
			"``source`` is the name of the source of this document or fragment."
		class class_(xsc.TextAttr):
			"``class`` is used to transmit individuality information forward."
			xmlname = "class"


# Root Element
class document(BaseElement):
	class Attrs(BaseElement.Attrs):
		class title(xsc.TextAttr): pass

	def convert(self, converter):
		return self.content.convert(converter)


# Title Elements
class title(BaseElement):
	class Attrs(BaseElement.Attrs, refidattrs, autoattrs):
		pass

	def convert(self, converter):
		e = doc.h(self.content)
		return e.convert(converter)


class subtitle(BaseElement):
	pass


# Bibliographic Elements
class docinfo(BaseElement):
	pass


class info(BaseElement):
	pass


class author(BaseElement):
	pass


class authors(BaseElement):
	pass


class organization(BaseElement):
	pass


class address(BaseElement):
	pass


class contact(BaseElement):
	pass


class version(BaseElement):
	pass


class revision(BaseElement):
	pass


class status(BaseElement):
	pass


class date(BaseElement):
	pass


class copyright(BaseElement):
	pass


# Decoration Elements
class decoration(BaseElement):
	pass


class header(BaseElement):
	pass


class footer(BaseElement):
	pass


# Structural Elements
class section(BaseElement):
	def convert(self, converter):
		e = doc.section(self.content)
		return e.convert(converter)


class topic(BaseElement):
	pass


class sidebar(BaseElement):
	pass


class transition(BaseElement):
	model = sims.Empty()


# Body Elements
class paragraph(BaseElement):
	def convert(self, converter):
		e = doc.p(self.content)
		return e.convert(converter)


class compound(BaseElement):
	pass


class container(BaseElement):
	pass


class bullet_list(BaseElement):
	class Attrs(BaseElement.Attrs):
		class bullet(xsc.TextAttr): pass

	def convert(self, converter):
		e = doc.ul(self.content)
		return e.convert(converter)


class enumerated_list(BaseElement):
	class Attrs(BaseElement.Attrs):
		class enumtype(xsc.TextAttr):
			values = ("arabic", "loweraplha", "upperalpha", "lowerroman", "upperroman")
		class prefix(xsc.TextAttr): pass
		class suffix(xsc.TextAttr): pass
		class start(xsc.IntAttr): pass

	def convert(self, converter):
		e = doc.ol(self.content)
		return e.convert(converter)


class list_item(BaseElement):
	def convert(self, converter):
		e = doc.li(self.content)
		return e.convert(converter)


class definition_list(BaseElement):
	def convert(self, converter):
		e = doc.dl(self.content)
		return e.convert(converter)


class definition_list_item(BaseElement):
	def convert(self, converter):
		with xsc.build():
			with xsc.Frag() as e:
				if self[term] or self[classifier]:
					with doc.dt():
						+xsc.Frag(self[term])
						if self[classifier]:
							+xsc.Text(" (")
							+xsc.Frag(self[classifier]).withsep(", ")
							+xsc.Text(")")
				+xsc.Frag(self[definition])
		return e.convert(converter)


class term(BaseElement):
	def convert(self, converter):
		e = self.content
		return e.convert(converter)


class classifier(BaseElement):
	def convert(self, converter):
		e = self.content
		return e.convert(converter)


class definition(BaseElement):
	def convert(self, converter):
		e = doc.dd(self.content)
		return e.convert(converter)


class field_list(BaseElement):
	def convert(self, converter):
		e = doc.dl(self.content)
		return e.convert(converter)


class field(BaseElement):
	def convert(self, converter):
		e = self.content
		return e.convert(converter)


class field_name(BaseElement):
	def convert(self, converter):
		e = doc.dt(self.content)
		return e.convert(converter)


class field_body(BaseElement):
	def convert(self, converter):
		e = doc.dd(self.content)
		return e.convert(converter)


class option_list(BaseElement):
	def convert(self, converter):
		e = doc.dl(self.content)
		return e.convert(converter)


class option_list_item(BaseElement):
	def convert(self, converter):
		e = self.content
		return e.convert(converter)


class option_group(BaseElement):
	def convert(self, converter):
		e = doc.dt()
		for o in self[option]:
			if e:
				e.append(", ")
			e2 = doc.lit(doc.option(o[option_string][0].content))
			for oa in o[option_argument]:
				e2.append("=", oa.content)
			e.append(e2)
		return e.convert(converter)


class option_string(BaseElement):
	model = sims.NoElements()


class option_argument(BaseElement):
	model = sims.NoElements()
	class Attrs(BaseElement.Attrs):
		class delimiter(xsc.TextAttr): pass


class description(BaseElement):
	def convert(self, converter):
		e = doc.dd(self.content)
		return e.convert(converter)


class literal_block(BaseElement):
	def convert(self, converter):
		e = doc.litblock(self.content)
		return e.convert(converter)


class line_block(BaseElement):
	pass


class line(BaseElement):
	pass


class block_quote(BaseElement):
	pass


class attribution(BaseElement):
	pass


class doctest_block(BaseElement):
	pass


class attention(BaseElement):
	pass


class caution(BaseElement):
	pass


class danger(BaseElement):
	pass


class error(BaseElement):
	pass


class hint(BaseElement):
	pass


class important(BaseElement):
	pass


class note(BaseElement):
	pass


class tip(BaseElement):
	pass


class warning(BaseElement):
	pass


class admonition(BaseElement):
	pass


class footnote(BaseElement):
	class Attrs(BaseElement.Attrs, backrefsattrs, autoattrs):
		pass


class citation(BaseElement):
	class Attrs(BaseElement.Attrs, backrefsattrs):
		pass


class label(BaseElement):
	model = sims.NoElements()
	pass


class rubric(BaseElement):
	pass


class target(BaseElement):
	class Attrs(BaseElement.Attrs, referenceattrs, anonymousattrs):
		pass

	def convert(self, converter):
		return xsc.Null


class substitution_definition(BaseElement):
	class Attrs(BaseElement.Attrs):
		class ltrim(xsc.TextAttr): pass
		class rtrim(xsc.TextAttr): pass


class comment(BaseElement):
	model = sims.NoElements()
	pass


class pending(BaseElement):
	model = sims.Empty()
	pass


class figure(BaseElement):
	class Attrs(BaseElement.Attrs, alignhattrs):
		class width(xsc.TextAttr): pass


class image(BaseElement):
	model = sims.Empty()
	class Attrs(BaseElement.Attrs, alignhvattrs):
		class uri(xsc.URLAttr): required = True
		class alt(xsc.TextAttr): pass
		class height(xsc.TextAttr): pass
		class width(xsc.TextAttr): pass
		class scale(xsc.TextAttr): pass


class caption(BaseElement):
	pass


class legend(BaseElement):
	pass


# Table elements: table, tgroup, colspec, thead, tbody, row, entry.


class system_message(BaseElement):
	"Used to record processing information"
	class Attrs(BaseElement.Attrs, backrefsattrs):
		class level(xsc.TextAttr): pass
		class line(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass

	def convert(self, converter):
		# A warning has already been issued by docutils, we don't have to do anything
		return xsc.Null


class raw(BaseElement):
	class Attrs(BaseElement.Attrs):
		class format(xsc.TextAttr): pass


# Inline elements
class emphasis(BaseElement):
	def convert(self, converter):
		e = doc.em(self.content)
		return e.convert(converter)

class strong(BaseElement):
	def convert(self, converter):
		e = doc.em(self.content)
		return e.convert(converter)


class literal(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.lit(self.content)
		return e.convert(converter)


class meth(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.meth(self.content)
		return e.convert(converter)


class mod(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.mod(self.content)
		return e.convert(converter)


class class_(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.class_(self.content)
		return e.convert(converter)


class func(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.func(self.content)
		return e.convert(converter)


class meth(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.meth(self.content)
		return e.convert(converter)


class obj(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.obj(self.content)
		return e.convert(converter)


class exc(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.exc(self.content)
		return e.convert(converter)


class attr(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.attr(self.content)
		return e.convert(converter)


class prop(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.prop(self.content)
		return e.convert(converter)


class option(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.option(self.content)
		return e.convert(converter)


class const(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.const(self.content)
		return e.convert(converter)


class file(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.file(self.content)
		return e.convert(converter)


class dir(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.dir(self.content)
		return e.convert(converter)


class data(BaseElement):
	model = sims.NoElements()

	def convert(self, converter):
		e = doc.data(self.content)
		return e.convert(converter)


class reference(BaseElement):
	class Attrs(BaseElement.Attrs, referenceattrs, anonymousattrs):
		class name(xsc.TextAttr): pass

	def convert(self, converter):
		e = doc.a(self.content, href=self.attrs.refuri)
		return e.convert(converter)


class footnote_reference(BaseElement):
	model = sims.NoElements()
	class Attrs(BaseElement.Attrs, refidattrs, refnameattrs, autoattrs):
		pass


class citation_reference(BaseElement):
	model = sims.NoElements()
	class Attrs(BaseElement.Attrs, refidattrs, refnameattrs):
		pass


class substitution_reference(BaseElement):
	model = sims.NoElements()
	class Attrs(BaseElement.Attrs, refnameattrs):
		pass


class title_reference(BaseElement):
	pass


class abbreviation(BaseElement):
	pass


class acronym(BaseElement):
	pass


class superscript(BaseElement):
	pass


class subscript(BaseElement):
	pass


class inline(BaseElement):
	pass


class inline(BaseElement):
	class Attrs(BaseElement.Attrs, refidattrs):
		pass


class problematic(BaseElement):
	class Attrs(BaseElement.Attrs, refidattrs):
		pass


class generated(BaseElement):
	pass


PE_inline_elements = (
	emphasis,
	strong,
	literal,
	reference,
	footnote_reference,
	citation_reference,
	substitution_reference,
	title_reference,
	abbreviation,
	acronym,
	subscript,
	superscript,
	inline,
	problematic,
	generated,
	target,
	image,
	raw,
)

PE_body_elements = (
	paragraph,
	compound,
	container,
	literal_block,
	doctest_block,
	line_block,
	block_quote,
#	table,
	figure,
	image,
	footnote,
	citation,
	rubric,
	bullet_list,
	enumerated_list,
	definition_list,
	field_list,
	option_list,
	attention,
	caution,
	danger,
	error,
	hint,
	important,
	note,
	tip,
	warning,
	admonition,
	reference,
	target,
	substitution_definition,
	comment,
	pending,
	system_message,
	raw,
)

PE_section_elements = (section,)

PE_bibliographic_elements = (
	author,
	authors,
	organization,
	address,
	contact,
	version,
	revision,
	status,
	date,
	copyright,
	field,
)

PE_structure_model = (topic, sidebar, transition) + PE_section_elements

document.model = sims.Elements(*(title, subtitle, decoration, docinfo, transition) + PE_structure_model)
title.model = sims.ElementsOrText(*PE_inline_elements)
subtitle.model = sims.ElementsOrText(*PE_inline_elements)
docinfo.model = sims.Elements(*PE_bibliographic_elements)
author.model = sims.ElementsOrText(*PE_inline_elements)
authors.model = sims.Elements(author, organization, address, contact)
organization.model = sims.ElementsOrText(*PE_inline_elements)
address.model = sims.ElementsOrText(*PE_inline_elements)
contact.model = sims.ElementsOrText(*PE_inline_elements)
version.model = sims.ElementsOrText(*PE_inline_elements)
revision.model = sims.ElementsOrText(*PE_inline_elements)
status.model = sims.ElementsOrText(*PE_inline_elements)
date.model = sims.ElementsOrText(*PE_inline_elements)
copyright.model = sims.ElementsOrText(*PE_inline_elements)
decoration.model = sims.Elements(header, footer)
header.model = sims.Elements(*PE_body_elements)
footer.model = sims.Elements(*PE_body_elements)
section.model = sims.Elements(*((title, subtitle, info, decoration) + PE_structure_model))
topic.model = sims.Elements(*((title,) + PE_body_elements))
sidebar.model = sims.Elements(*((title, subtitle, topic) + PE_body_elements))
paragraph.model = sims.ElementsOrText(*PE_inline_elements)
compound.model = sims.Elements(*PE_body_elements)
container.model = sims.Elements(*PE_body_elements)
bullet_list.model = sims.Elements(list_item)
enumerated_list.model = sims.Elements(list_item)
list_item.model = sims.Elements(*PE_body_elements)
definition_list.model = sims.Elements(definition_list_item)
definition_list_item.model = sims.Elements(term, classifier, definition)
term.model = sims.ElementsOrText(*PE_inline_elements)
classifier.model = sims.ElementsOrText(*PE_inline_elements)
definition.model = sims.Elements(*PE_body_elements)
field_list.model = sims.Elements(field)
field.model = sims.Elements(field_name, field_body)
field_name.model = sims.ElementsOrText(*PE_inline_elements)
field_body.model = sims.Elements(*PE_body_elements)
option_list.model = sims.Elements(option_list_item)
option_list_item.model = sims.Elements(option_group, description)
option_group.model = sims.Elements(option)
option.model = sims.Elements(option_string, option_argument)
description.model = sims.Elements(*PE_body_elements)
literal_block.model = sims.ElementsOrText(*PE_inline_elements)
line_block.model = sims.Elements(line, line_block)
line.model = sims.ElementsOrText(*PE_inline_elements)
block_quote.model = sims.Elements(*(PE_body_elements + (attribution,)))
attribution.model = sims.ElementsOrText(*PE_inline_elements)
doctest_block.model = sims.ElementsOrText(*PE_inline_elements)
attention.model = sims.Elements(*PE_body_elements)
caution.model = sims.Elements(*PE_body_elements)
danger.model = sims.Elements(*PE_body_elements)
error.model = sims.Elements(*PE_body_elements)
hint.model = sims.Elements(*PE_body_elements)
important.model = sims.Elements(*PE_body_elements)
note.model = sims.Elements(*PE_body_elements)
tip.model = sims.Elements(*PE_body_elements)
warning.model = sims.Elements(*PE_body_elements)
admonition.model = sims.Elements(*(PE_body_elements + (title,)))
citation.model = sims.Elements(*(PE_body_elements + (label,)))
rubric.model = sims.ElementsOrText(*PE_inline_elements)
target.model = sims.ElementsOrText(*PE_inline_elements)
substitution_definition.model = sims.ElementsOrText(*PE_inline_elements)
figure.model = sims.Elements(image, caption, legend)
caption.model = sims.ElementsOrText(*PE_inline_elements)
legend.model = sims.Elements(*PE_body_elements)
system_message.model = sims.Elements(*PE_body_elements)
raw.model = sims.ElementsOrText(*PE_inline_elements)
emphasis.model = sims.ElementsOrText(*PE_inline_elements)
strong.model = sims.ElementsOrText(*PE_inline_elements)
reference.model = sims.ElementsOrText(*PE_inline_elements)
substitution_reference.model = sims.ElementsOrText(*PE_inline_elements)
title_reference.model = sims.ElementsOrText(*PE_inline_elements)
abbreviation.model = sims.ElementsOrText(*PE_inline_elements)
acronym.model = sims.ElementsOrText(*PE_inline_elements)
superscript.model = sims.ElementsOrText(*PE_inline_elements)
subscript.model = sims.ElementsOrText(*PE_inline_elements)
inline.model = sims.ElementsOrText(*PE_inline_elements)
problematic.model = sims.ElementsOrText(*PE_inline_elements)
generated.model = sims.ElementsOrText(*PE_inline_elements)


class ReSTConversionWarning(Warning):
	pass


class ReSTConverter:
	def __init__(self):
		from ll.xist.ns import doc, abbr
		self.namedrefs = collections.defaultdict(list)
		self.unnamedrefs = []
		self.doc = doc
		self.abbr = abbr

	def convert(self, node):
		if isinstance(node, nodes.document):
			return xsc.Frag(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.Text):
			return xsc.Text(node.astext())
		elif isinstance(node, nodes.problematic):
			# We don't do anything about this
			return xsc.Frag(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.section):
			return self.doc.section(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.title):
			return self.doc.h(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.paragraph):
			return self.doc.p(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.bullet_list):
			return self.doc.ul(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.list_item):
			return self.doc.li(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.definition_list):
			return self.doc.dl(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.definition_list_item):
			return xsc.Frag(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.term):
			return self.doc.dt(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.definition):
			return self.doc.dd(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.literal_block):
			return self.doc.prog(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.literal):
			return self.doc.lit(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.emphasis):
			return self.doc.em(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.substitution_reference):
			try:
				return getattr(self.abbr, node.attributes["refname"].lower())()
			except AttributeError:
				return xsc.Frag(self.convert(child) for child in node.children)
		elif isinstance(node, nodes.reference):
			e = self.doc.a(self.convert(child) for child in node.children)
			if "anonymous" in node.attributes:
				self.unnamedrefs.append(e)
			else:
				self.namedrefs[node.attributes["refname"]].append(e)
			return e
		elif isinstance(node, nodes.target):
			uri = node.attributes["refuri"]
			if "anonymous" in node.attributes:
				# Set the link on the first unnamed reference
				self.unnamedrefs[0].attrs.href = uri
				del self.unnamedrefs[0] # done => remove it
			else:
				for name in node.attributes["names"]:
					try:
						es = self.namedrefs[name]
					except KeyError:
						pass
					else:
						for e in es:
							e.attrs.href = uri
						del self.namedrefs[name]
			return xsc.Null
		elif isinstance(node, nodes.system_message):
			warnings.warn(ReSTConversionWarning(str(node)))
			return xsc.Null # ignore system messages
		else:
			raise TypeError("can't handle {!r}".format(node.__class__))


def fromstring(string, base=None, **options):
	realoptions = dict(tab_width=3)
	realoptions.update(options)
	doc = core.publish_doctree(string, source_path=base, settings_overrides=realoptions) # This requires docutils
	elements = globals()

	def toxist(node):
		if isinstance(node, nodes.Text):
			return xsc.Text(str(node.astext()))
		else:
			e = elements[node.__class__.__name__](toxist(child) for child in node.children)
			e.startloc = xsc.Location(node.source, node.line)
			for (attrkey, attrvalue) in node.attlist():
				if attrkey in e.Attrs:
					if isinstance(attrvalue, list):
						attrvalue = " ".join(attrvalue)
					e.attrs[attrkey] = attrvalue
			return e

	return toxist(doc)


def fromstream(stream, base=None, **options):
	return fromstring(stream.read(), base, **options)


def fromfile(filename, base=None, **options):
	filename = os.path.expanduser(filename)
	if base is None:
		base = filename
	with contextlib.closing(open(filename, "rb")) as stream:
		return fromstream(stream, base, **options)
