# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2007-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2007-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This namespace module implements Atom 1.0 as specified by :rfc:`4287`.
"""


from ll.xist import xsc, sims
from ll.xist.ns import html


__docformat__ = "reStructuredText"


xmlns = "http://www.w3.org/2005/Atom"


class feed(xsc.Element):
	"""
	The :class:`feed` element is the document (i.e., top-level) element of an
	Atom Feed Document, acting as a container for metadata and data associated
	with the feed.
	"""
	xmlns = xmlns


class entry(xsc.Element):
	"""
	The :class:`entry` element represents an individual entry, acting as a
	container for metadata and data associated with the entry.
	"""
	xmlns = xmlns


class content(xsc.Element):
	"""
	The :class:`content` element either contains or links to the content of
	the :class:`entry`.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass
		class src(xsc.URLAttr): pass


class author(xsc.Element):
	"""
	The :class:`author` element indicates the author of the
	:class:`entry` or :class:`feed`.
	"""
	xmlns = xmlns


class category(xsc.Element):
	"""
	The :class:`category` element conveys information about a category
	associated with an :class:`entry` or :class:`feed`.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class term(xsc.TextAttr): required = True
		class scheme(xsc.URLAttr): pass
		class label(xsc.TextAttr): pass


class contributor(xsc.Element):
	"""
	The :class:`contributor` element indicates a person or other entity
	who contributed :class:`entry` or :class:`feed`.
	"""
	xmlns = xmlns


class generator(xsc.Element):
	"""
	The :class:`generator` element's content identifies the agent used to
	generate a feed, for debugging and other purposes.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class uri(xsc.URLAttr): pass
		class version(xsc.TextAttr): pass


class icon(xsc.Element):
	"""
	The :class:`icon` element's content is an IRI reference that identifies
	an image that provides iconic visual identification for a feed.
	"""
	xmlns = xmlns


class id(xsc.Element):
	"""
	The :class:`id` element conveys a permanent, universally unique identifier
	for an :class:`entry` or :class:`feed`.
	"""
	xmlns = xmlns


class link(xsc.Element):
	"""
	The :class:`link` element defines a reference from an
	:class:`entry` or :class:`feed` to a Web resource.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): required = True
		class rel(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
		class hreflang(xsc.TextAttr): pass
		class title(xsc.TextAttr): pass
		class length(xsc.TextAttr): pass


class logo(xsc.Element):
	"""
	The :class:`logo` element's content is an IRI reference that identifies
	an image that provides visual identification for a :class:`feed`.
	"""
	xmlns = xmlns


class published(xsc.Element):
	"""
	The :class:`published` element indicatesg an instant in time associated
	with an event early in the life cycle of the :class:`entry`.
	"""
	xmlns = xmlns


class rights(xsc.Element):
	"""
	The :class:`rights` element contains text that conveys information about
	rights held in and over an :class:`entry` or :class:`feed`.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class source(xsc.Element):
	"""
	If an :class:`entry` is copied from one :class:`feed` into another
	:class:`feed`, then the source :class:`feed`'s metadata (all child elements
	of :class:`feed` other than the :class:`entry` elements) may be preserved
	within the copied entry by adding a :class:`source` child element, if it is
	not already present in the :class:`entry`, and including some or all of the
	source :class:`feed`'s Metadata elements as the :class:`source` element's
	children.
	"""
	xmlns = xmlns


class subtitle(xsc.Element):
	"""
	The :class:`subtitle` element contains text that conveys a human-readable
	description or subtitle for a :class:`feed`.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class summary(xsc.Element):
	"""
	The :class:`summary` element contains text that conveys a short summary,
	abstract, or excerpt of an entry.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class title(xsc.Element):
	"""
	The :class:`title` element contains text that conveys a human-readable
	title for an :class:`entry` or :class:`feed`.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class updated(xsc.Element):
	"""
	The :class:`updated` element contains a date indicating the most recent
	instant in time when an :class:`entry` or :class:`feed` was modified in a
	way the publisher considers significant.
	"""
	xmlns = xmlns


class email(xsc.Element):
	"""
	The :class:`email` element's content conveys an e-mail address associated
	with the person.
	"""
	xmlns = xmlns


class uri(xsc.Element):
	"""
	The :class:`uri` element's content conveys an IRI associated with the person.
	"""
	xmlns = xmlns


class name(xsc.Element):
	"""
	The :class:`name` element's content conveys a human-readable name for the
	person.
	"""
	xmlns = xmlns


link.model = \
category.model = sims.Empty()
content.model = sims.ElementsOrText(html.div)
source.model = sims.ElementsOrText(author, category, contributor, generator, icon, id, link, logo, rights, subtitle, title, updated)
feed.model = sims.Elements(author, category, contributor, generator, icon, logo, id, link, rights, subtitle, title, updated, entry)
entry.model = sims.Elements(author, category, content, contributor, id, link, published, rights, source, summary, title, updated)
contributor.model = \
author.model = sims.Elements(name, uri, email)
title.model = \
summary.model = \
subtitle.model = \
rights.model = sims.ElementsOrText(html.div)
updated.model = \
published.model = \
logo.model = \
id.model = \
icon.model = \
generator.model = \
email.model = \
uri.model = \
name.model = sims.NoElements()
