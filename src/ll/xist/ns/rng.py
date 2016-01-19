# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2005-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2005-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This module is an XIST namespace for `Relax NG`__ files.

__ http://relaxng.org/
"""


from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://relaxng.org/ns/structure/1.0"


class base(xsc.Element):
	"""
	"Abstract" basis class, providing common attributes.
	"""
	register = False

	class Attrs(xsc.Element.Attrs):
		class ns(xsc.TextAttr): pass
		# ns is inherited from the nearest ancestor, where a ns-attribute is defined, else it's ""
		class datatypeLibrary(xsc.URLAttr): pass


class anyName(base):
	"""
	Matches any name from any namespace.
	"""
	xmlns = xmlns
	# Restriction:
	# name classes of attributes can't overlap


class attribute(base):
	"""
	Specifies an XML attribute.
	"""
	xmlns = xmlns
	# Restriction:
	# after simplification: contain only text-node-relevent nodes
	# can't be duplicated
	# infinite name classes must be enclosed in oneOrMore/zeroOrMore
	# name and name class can't be both specified

	class Attrs(base.Attrs):
		class name(xsc.TextAttr): pass


class choice(base):
	"""
	nameclass: a name matches choice if, and only if, it matches at least one of
	the subname classes. pattern: it matches a node if, and only if, at least
	one of its subpatterns matches the node
	"""
	xmlns = xmlns


class data(base):
	"""
	Specifies data of a certain kind.
	"""
	xmlns = xmlns
	class Attrs(base.Attrs):
		class type(xsc.TextAttr): pass


class define(base):
	"""
	Defines a part of a grammar pattern (also a pattern), recursion possible
	only inside an element.
	"""
	xmlns = xmlns
	class Attrs(base.Attrs):
		class name(xsc.TextAttr): required = True
		class combine(xsc.TextAttr): values = ("interleave", "choice")


class div(base):
	"""
	Allows logical divisions, no effect on validation, annotations can be made
	here
	"""
	xmlns = xmlns
	class Attrs(base.Attrs):
		class name(xsc.TextAttr): pass


class element_(base):
	"""
	Specifies an XML element.
	"""
	xmlns = xmlns
	xmlname = "element"

	class Attrs(base.Attrs):
		class name(xsc.TextAttr): pass
		# alternative: namespace name


class empty(base):
	"""
	Specifies empty content.
	"""
	xmlns = xmlns
	model = sims.Empty()


class except_(base):
	"""
	An :class:`except_` element can remove a name class from another (this class
	has no attributes) (inside a :class:`name` element) or it is used to remove
	a set of values from a data pattern.
	"""
	xmlns = xmlns
	xmlname = "except"


class externalRef(base):
	"""
	Reference to an extern pattern stored in a file.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(base.Attrs):
		class href(xsc.URLAttr): required = True


class grammar(base):
	"""
	A :class:`grammar` element has a single :class:`start` child element, and
	zero or more :class:`define` child elements. The :class:`start` and
	:class:`define` elements contain patterns. These patterns can contain
	:class:`ref` elements that refer to patterns defined by any of the
	:class:`define` elements in that grammar element. A :class:`grammar` pattern
	is matched by matching the pattern contained in the :class:`start` element.
	"""
	xmlns = xmlns


class group(base):
	"""
	Is implied, can be also explicitly specified: the patterns have to appear
	in the specified order (except for the attributes, they are allowed to appear
	in any order in the start tag)
	"""
	xmlns = xmlns


class include(base):
	"""
	Includes an extern grammar pattern. Can contain define parts to overwrite
	that part (same name) in the extern pattern. A possible start element
	inside include overwrites the start element of the extern pattern.
	"""
	xmlns = xmlns
	class Attrs(base.Attrs):
		class href(xsc.URLAttr): required = True


class interleave(base):
	"""
	Child elements can appear in any order, if one is a group, the order must be
	kept, other direct childs can mix between.
	"""
	xmlns = xmlns


class list(base):
	"""
	Matches whitespace seperated values.
	"""
	xmlns = xmlns


class mixed(base):
	"""
	``<mixed> p </mixed>`` is short for ``<interleave> <text/> p </interleave>``
	"""
	xmlns = xmlns


class name(base):
	"""
	Defines a class with a single name.
	"""
	xmlns = xmlns
	model = sims.NoElements()


class notAllowed(base):
	"""
	Used to make extension points in patterns.
	"""
	xmlns = xmlns
	model = sims.Empty()


class nsName(base):
	"""
	Allows any name in a specific namespace.
	"""
	xmlns = xmlns
	model = sims.Elements(except_)
	class Attrs(base.Attrs):
		class ns(xsc.URLAttr): pass


class oneOrMore(base):
	"""
	There can be one or more recurrence of the enclosed pattern.
	"""
	xmlns = xmlns


class optional(base):
	"""
	The enclosed tags can be left out.
	"""
	xmlns = xmlns


class param(base):
	"""
	Specifies parameters passed to the datatype library to determine whether a
	value is valid per a datatype.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(base.Attrs):
		class name(xsc.TextAttr): pass


class parentRef(base):
	"""
	Escapes out of the current grammar and references a definition from the
	parent of the current grammar.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(base.Attrs):
		class name(xsc.TextAttr): required = True


class ref(base):
	"""
	A :class:`ref` pattern refers to a definition from the nearest grammar
	ancestor.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(base.Attrs):
		class name(xsc.TextAttr): required = True


class start(base):
	"""
	Required start tag inside a :class:`grammar` tag.
	"""
	xmlns = xmlns
	class Attrs(base.Attrs):
		class combine(xsc.TextAttr): values = ("combine", "interleave")


class text(base):
	"""
	Matches arbitrary text (one or more text nodes), including empty text.
	"""
	xmlns = xmlns
	model = sims.Empty()


class value(base):
	"""
	By default, the :class:`value` pattern will consider the string in the
	pattern to match the string in the document if the two strings are the same
	after the whitespace in both strings is normalized. Whitespace normalization
	strips leading and trailing whitespace characters, and collapses sequences
	of one or more whitespace characters to a single space character. This
	corresponds to the behaviour of an XML parser for an attribute that is
	declared as other than CDATA.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(base.Attrs):
		class type(xsc.TextAttr): pass


class zeroOrMore(base):
	"""
	There can be zero or more recurrence of the enclosed pattern.
	"""
	xmlns = xmlns


# modeltype definitions
anyName.model = sims.Elements(except_)
attribute.model = sims.ElementsOrText(choice, data, empty, externalRef, grammar, group, interleave, list, mixed, name, notAllowed, nsName, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
choice.model = sims.Elements(anyName, attribute, choice, data, element_, empty, externalRef, grammar, group, interleave, list, mixed, name, notAllowed, nsName, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
data.model = sims.Elements(except_, param)
define.model = sims.Elements(attribute, choice, data, element_, empty, externalRef, grammar, group, interleave, list, mixed, notAllowed, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
div.model = sims.Elements(define, div, include, start)
element_.model = \
except_.model = sims.Elements(anyName, attribute, choice, data, element_, empty, externalRef, grammar, group, interleave, list, mixed, name, notAllowed, nsName, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
grammar.model = sims.Elements(start, define, div, include)
group.model = sims.Elements(attribute, choice, data, element_, externalRef, grammar, group, interleave, list, mixed, notAllowed, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
include.model = sims.Elements(start, define, div)
interleave.model = sims.Elements(attribute, choice, data, element_, externalRef, grammar, group, interleave, list, mixed, notAllowed, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
list.model = sims.Elements(choice, data, empty, externalRef, grammar, group, notAllowed, oneOrMore, optional, parentRef, ref, value, zeroOrMore)
mixed.model = sims.Elements(attribute, choice, data, element_, empty, externalRef, grammar, group, interleave, list, mixed, notAllowed, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
oneOrMore.model = sims.Elements(choice, data, element_, empty, externalRef, grammar, group, interleave, list, mixed, notAllowed, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
optional.model = sims.Elements(attribute, choice, data, element_, empty, externalRef, grammar, group, interleave, list, mixed, notAllowed, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
start.model = sims.Elements(attribute, choice, data, element_, empty, externalRef, grammar, group, interleave, list, mixed, notAllowed, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
zeroOrMore.model = sims.Elements(choice, data, element_, empty, externalRef, grammar, group, interleave, list, mixed, notAllowed, oneOrMore, optional, parentRef, ref, text, value, zeroOrMore)
