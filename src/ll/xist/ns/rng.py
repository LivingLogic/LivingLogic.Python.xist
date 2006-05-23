#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 2005-2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2006 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
This module is an &xist; namespace for
<link href="http://relaxng.org/">Relax NG</link> files.
"""

__version__ = "$Revision$".split()[1]
# $Source$


from ll.xist import xsc, sims


class base(xsc.Element):
	""" 
	<z>Abstract</z> basis class, providing common attributes.
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
	# Restriction:
	# name classes of attributes can't overlap


class attribute(base):
	"""
	Specifies an &xml; attribute.
	"""
	# Restriction:
	# after simplification: contain only text-node-relevent nodes
	# can't be duplicated
	# infinite name classes must be enclosed in oneOrMore/zeroOrMore
	# name and name class can't be both specified

	class Attrs(base.Attrs):
		class name(xsc.TextAttr): pass


class choice(base):
	"""
	nameclass: a name matches choice if, and only if, it matches at least one of the subname classes
	pattern: it matches a node if, and only if, at least one of its subpatterns matches the node
	"""


class data(base):
	"""
	Specifies data of a certain kind.
	"""
	# Restriction
	# cant' be used in mixed content models

	class Attrs(base.Attrs):
		class type(xsc.TextAttr): pass


class define(base):
	"""
	Defines a part of a grammar pattern (also a pattern), recursion possible only inside an element.
	"""
	# Restriction:
	# is not possible to define and make reference to nonpatterns such as class names/datatype parameters
	
	class Attrs(base.Attrs):
		class name(xsc.TextAttr): required = True
		class combine(xsc.TextAttr): values = (u"interleave", u"choice")


class div(base):
	"""
	Allows logical divisions, no effect on validation, annotations can be made here
	"""
	
	class Attrs(base.Attrs):
		class name(xsc.TextAttr): pass


class element_(base):
	"""
	Specifies an &xml; element.
	"""
	xmlname = "element"
	
	class Attrs(base.Attrs):
		class name(xsc.TextAttr): pass
		# alternative: namespace name


class empty(base):
	"""
	Specifies empty content.
	"""
	model = sims.Empty()


class except_(base):
	"""
	An <class>except_</class> element can remove a name class from another
	(this class has no attributes) (inside a <class>name</class> element) or
	it is used to remove a set of values from a data pattern.
	"""
	xmlname = "except"


class externalRef(base):
	"""
	Reference to an extern pattern stored in a file.
	"""
	model = sims.Empty()

	class Attrs(base.Attrs):
		class href(xsc.URLAttr): required = True


class grammar(base):
	"""
	A <class>grammar</class> element has a single <class>start</class> child element,
	and zero or more <class>define</class> child elements. The <class>start</class>
	and <class>define</class> elements contain patterns. These patterns can
	contain <class>ref</class> elements that refer to patterns defined by any of
	the <class>define</class> elements in that grammar element. A <class>grammar</class>
	pattern is matched by matching the pattern contained in the <class>start</class> element.
	"""


class group(base):
	"""
	Is implied, can be also explicitly specified: the patterns have to appear
	in the specified order (except for the attributes, they are allowed to appear
	in any order in the start tag)
	"""


class include(base):
	"""
	Includes an extern grammar pattern.
	Can contain define parts to overwrite that part (same name) in the extern pattern.
	A possible start element inside include overwrites the start element of the extern pattern.
	"""

	class Attrs(base.Attrs):
		class href(xsc.URLAttr): required = True


class interleave(base):
	"""
	Child elements can appear in any order, if one is a group, the order must be
	kept, other direct childs can mix between.
	"""
	# Restriction:
	# interleave can't be used within a list,
	# elements within can't have overlapping name classes,
	# there can be at most one text pattern in each set of patterns combined by interleave


class list(base):
	"""
	Matches whitespace seperated values.
	"""
	# Restriction:
	# list can't be used within list
	# no list in list
	# content: only about data: no element, attribut, text


class mixed(base):
	"""
	<markup>&lt;mixed&gt; p &lt;/mixed&gt;</markup> is short for
	<markup>&lt;interleave&gt; &lt;text/&gt; p &lt;/interleave&gt;</markup>
	Restr.: can't be used within a list, elements within can't have overlapping name classes, there must no other text pattern in each set of patterns combined by mixed
	"""


class name(base):
	"""
	Defines a class with a single name.
	"""
	model = sims.NoElements()


class notAllowed(base):
	"""
	Used to make extension points in patterns.
	"""
	model = sims.Empty()


class nsName(base):
	"""
	Allows any name in a specific namespace.
	"""
	model = sims.Elements(except_)
	# Restriction:
	# within the scope of an element, the attributes can't overlap, same as when elements are combined by interleave

	class Attrs(base.Attrs):
		class ns(xsc.URLAttr): pass


class oneOrMore(base):
	"""
	There can be one or more recurrence of the enclosed pattern.
	"""
	# Restriction
	# can't contain attribute definitions
	


class optional(base):
	"""
	The enclosed tags can be left out.
	"""


class param(base):
	"""
	Specifies parameters passed to the datatype library to determine whether a value is valid per a datatype.
	"""
	model = sims.NoElements()

	class Attrs(base.Attrs):
		class name(xsc.TextAttr): pass


class parentRef(base):
	"""
	Escapes out of the current grammar and references a definition from the parent of the current grammar.
	"""
	model = sims.Empty()

	class Attrs(base.Attrs):
		class name(xsc.TextAttr): required = True


class ref(base):
	"""
	A <class>ref</class> pattern refers to a definition from the nearest grammar ancestor.
	"""
	model = sims.Empty()

	class Attrs(base.Attrs):
		class name(xsc.TextAttr): required = True


class start(base):
	"""
	Required start tag inside a <class>grammar</class> tag.
	"""

	class Attrs(base.Attrs):
		class combine(xsc.TextAttr): values = (u"combine", u"interleave")


class text(base):
	"""
	Matches arbitrary text (one or more text nodes), including empty text.
	"""
	model = sims.Empty()
	# Restriction:
	# No more than one text pattern in an interleave pattern


class value(base):
	"""
	By default, the <class>value</class> pattern will consider the string in the pattern
	to match the string in the document if the two strings are the same after
	the whitespace in both strings is normalized. Whitespace normalization
	strips leading and trailing whitespace characters, and collapses sequences
	of one or more whitespace characters to a single space character.
	This corresponds to the behaviour of an &xml; parser for an attribute
	that is declared as other than CDATA.
	"""
	# Restriction:
	# meant for data-oriented applicated, can't be used in mixed-content
	model = sims.NoElements()

	class Attrs(base.Attrs):
		class type(xsc.TextAttr): pass
#@TODO: evtl. kein TextAttr		


class zeroOrMore(base):
	"""
	There can be zero or more recurrence of the enclosed pattern.
	"""
	# Restriction
	# can't contain attribute definitions


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


class __ns__(xsc.Namespace):
	xmlname = "rng"
	xmlurl = "http://relaxng.org/ns/structure/1.0"
__ns__.makemod(vars())
