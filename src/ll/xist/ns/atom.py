#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2006 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
This namespace module implements Atom 1.0 as specified by
<link href="http://www.atompub.org/rfc4287.html">RFC 4287</link>.
"""


__version__ = "$Revision ? $".split()[1]
# $Source$


from ll.xist import xsc, sims
from ll.xist.ns import html


class feed(xsc.Element):
	"""
	The <class>feed</class> element is the document (i.e., top-level) element of
	an Atom Feed Document, acting as a container for metadata and data associated
	with the feed.
	"""


class entry(xsc.Element):
	"""
	The <class>entry</class> element represents an individual entry, acting as a
	container for metadata and data associated with the entry.
	"""


class content(xsc.Element):
	"""
	The <class>content</class> element either contains or links to the content of
	the <pyref class="entry><class>entry</class></pyref>.
	"""
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass
		class src(xsc.URLAttr): pass


class author(xsc.Element):
	"""
	The <class>author</class> element indicates the author of the
	<pyref class="entry"><class>entry</class></pyref> or
	<pyref class="feed"><class>feed</class></pyref>.
	"""


class category(xsc.Element):
	"""
	The <class>category</class> element conveys information about a category
	associated with an <pyref class="entry"><class>entry</class></pyref> or
	<pyref class="feed"><class>feed</class></pyref>.
	"""
	class Attrs(xsc.Element.Attrs):
		class term(xsc.TextAttr): required = True
		class scheme(xsc.URLAttr): pass
		class label(xsc.TextAttr): pass


class contributor(xsc.Element):
	"""
	The <class>contributor</class> element indicates a person or other entity
	who contributed <pyref class="entry"><class>entry</class></pyref> or
	<pyref class="feed"><class>feed</class></pyref>.
	"""


class generator(xsc.Element):
	"""
	The <class>generator</class> element's content identifies the agent used to
	generate a feed, for debugging and other purposes.
	"""
	class Attrs(xsc.Element.Attrs):
		class uri(xsc.URLAttr): pass
		class version(xsc.TextAttr): pass


class icon(xsc.Element):
	"""
	The <class>icon</class> element's content is an IRI reference that identifies
	an image that provides iconic visual identification for a feed.
	"""



class id(xsc.Element):
	"""
	The <class>id</class> element conveys a permanent, universally unique identifier
	for an <pyref class="entry"><class>entry</class></pyref> or
	<pyref class="feed"><class>feed</class></pyref>.
	"""


class link(xsc.Element):
	"""
	The <class>link</class> element defines a reference from an
	<pyref class="entry"><class>entry</class></pyref> or
	<pyref class="feed"><class>feed</class></pyref> to a Web resource.
	"""
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): required = True
		class rel(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
		class hreflang(xsc.TextAttr): pass
		class title(xsc.TextAttr): pass
		class length(xsc.TextAttr): pass


class logo(xsc.Element):
	"""
	The <class>logo</class> element's content is an IRI reference that identifies
	an image that provides visual identification for a <pyref class="feed"><class>feed</class></pyref>.
	"""


class published(xsc.Element):
	"""
	The <class>published</class> element indicatesg an instant in time associated
	with an event early in the life cycle of the <pyref class="entry"><class>entry</class></pyref>.
	"""


class rights(xsc.Element):
	"""
	The <class>rights</class> element contains text that conveys information about
	rights held in and over an <pyref class="entry"><class>entry</class></pyref>
	or <pyref class="feed"><class>feed</class></pyref>.
	"""
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class source(xsc.Element):
	"""
	If an <pyref class="entry"><class>entry</class></pyref> is copied from one
	<pyref class="feed"><class>feed</class></pyref> into another <class>feed</class>,
	then the source <class>feed</class>'s metadata (all child elements of <class>feed</class>
	other than the <class>entry</class> elements) may be preserved within
	the copied entry by adding a <class>source</class> child element, if it is not
	already present in the <class>entry</class>, and including some or all of the
	source <class>feed</class>'s Metadata elements as the <class>source</class>
	element's children.
	"""


class subtitle(xsc.Element):
	"""
	The <class>subtitle</class> element contains text that conveys a human-readable
	description or subtitle for a <pyref class="feed"><class>feed</class></pyref>.
	"""
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class summary(xsc.Element):
	"""
	The <class>summary</class> element contains text that conveys a short summary,
	abstract, or excerpt of an entry.
	"""
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class title(xsc.Element):
	"""
	The <class>title</class> element contains text that conveys a human-readable
	title for an <pyref class="entry"><class>entry</class></pyref> or
	<pyref class="feed"><class>feed</class></pyref>.
	"""
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class updated(xsc.Element):
	"""
	The <class>updated</class> element contains a date indicating the most recent
	instant in time when an <pyref class="entry"><class>entry</class></pyref> or
	<pyref class="feed"><class>feed</class></pyref> was modified in a way the
	publisher considers significant.
	"""


class email(xsc.Element):
	"""
	The <class>email</class> element's content conveys an e-mail address associated with the person.
	"""


class uri(xsc.Element):
	"""
	The <class>uri</class> element's content conveys an IRI associated with the person.
	"""


class name(xsc.Element):
	"""
	The <class>name</class> element's content conveys a human-readable name for the person.
	"""


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


class __ns__(xsc.Namespace):
	xmlname = "atom"
	xmlurl = "http://www.w3.org/2005/Atom"
__ns__.makemod(vars())
