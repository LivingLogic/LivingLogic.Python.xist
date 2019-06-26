# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST namespace that contains definitions for all the elements in `HTML5`_ as
well as some (deprecated) elements that were in use in previous HTML versions.

This namespace also supports the elements and attributes from the `microdata
specification`_.

For all deprecated elements and attributes the class attribute :obj:`deprecated`
is set to :const:`True`.

The function :func:`astext` can be used to convert a HTML XIST tree into plain
text.

.. _HTML5: http://www.w3.org/TR/2012/CR-html5-20121217/

.. _microdata specification: http://www.w3.org/html/wg/drafts/microdata/master/

"""

import os, tempfile, subprocess, cgi, textwrap, collections

from ll.xist import xsc, sims


__docformat__ = "reStructuredText"

xmlns = "http://www.w3.org/1999/xhtml"


###
### Document types
###

class DocTypeHTML40transitional(xsc.DocType):
	"""
	document type for HTML 4.0 transitional
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd"')


class DocTypeHTML401transitional(xsc.DocType):
	"""
	document type for HTML 4.01 transitional
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"')


class DocTypeXHTML10strict(xsc.DocType):
	"""
	document type for XHTML 1.0 strict
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"')


class DocTypeXHTML10transitional(xsc.DocType):
	"""
	document type for XHTML 1.0 transitional
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"')


class DocTypeXHTML11(xsc.DocType):
	"""
	document type for XHTML 1.1
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"')


class DocTypeHTML5(xsc.DocType):
	"""
	document type for HTML5
	"""
	def __init__(self):
		xsc.DocType.__init__(self, "html")


###
### Attributes
###

class MediaAttr(xsc.TextAttr):
	def hasmedia(self, media):
		"""
		Return whether :obj:`self` contains the media type :obj:`media`. Returns
		``True`` if :obj:`media` is :const:`None` or :obj:`self` is empty.
		"""
		if media is not None and self:
			return media in {m.strip() for m in str(self).split(",")}
		return True


class GlobalAttrs(xsc.Attrs):
	"""
	Attributes that are common to and may be specified on all HTML elements
	"""
	def validateattr(self, path):
		node = path[-1]
		if node.xmlns is None and not self.isdeclared(node) and not node.xmlname.startswith(("data-", "aria-")):
			yield xsc.UndeclaredAttrWarning(self.__class__, node)

	class accesskey(xsc.TextAttr):
		"""
		This attribute's value is used by the user agent as a guide for creating a
		keyboard shortcut that activates or focuses the element.

		If specified, the value must be an ordered set of unique space-separated
		tokens that are case-sensitive, each of which must be exactly one Unicode
		code point in length.
		"""
	class class_(xsc.TextAttr):
		"""
		This attribute, if specified, must have a value that is a set of
		space-separated tokens representing the various classes that the element
		belongs to.
		"""
		xmlname = "class"
	class contenteditable(xsc.TextAttr):
		"""
		Indicates whether the element is editable.
		"""
		values = ("false", "true", "")
	class contextmenu(xsc.TextAttr):
		"""
		The element's context menu. The value must be the ID of a menu element in
		the DOM.
		"""
	class dir(xsc.TextAttr):
		"""
		The element's text directionality.
		"""
		values = ("ltr", "rtl", "auto")
	class draggable(xsc.TextAttr):
		"""
		Specifies whether the element is draggable.
		"""
		values = ("false", "true")
	class dropzone(xsc.TextAttr):
		"""
		Specifies which types of objects are allowed to be dropped on the element
		and how they are handled.
		"""
		# copy, move, link, string:*, file:*
	class hidden(xsc.BoolAttr):
		"""
		When specified, indicates that the element is not yet, or is no longer,
		directly relevant to the page's current state.

		User agents should not render elements that have the hidden attribute
		specified.
		"""
	class id(xsc.IDAttr):
		"""
		Specifies its element's unique identifier.
		"""
	class lang(xsc.TextAttr):
		"""
		Specifies the primary language for the element's contents and for any of
		the element's attributes that contain text.
		"""
	class spellcheck(xsc.TextAttr):
		"""
		Specifies whether the user agent should indicate spelling and/or grammar
		errors in content of the element.
		"""
		values = ("false", "true", "")
	class style(xsc.StyleAttr):
		"""
		A `CSS styling attribute`__

		__ http://dev.w3.org/csswg/css-style-attr/
		"""
	class tabindex(xsc.IntAttr):
		"""
		Specifies whether an element is supposed to be focusable and what is to
		be the relative order of the element for the purposes of sequential focus
		navigation.
		"""
	class title(xsc.TextAttr):
		"""
		Advisory information for the element, such as would be appropriate for a
		tooltip.
		"""
	class translate(xsc.TextAttr):
		"""
		An enumerated attribute that is used to specify whether an element's
		attribute values and the values of its text node children are to be
		translated when the page is localized, or whether to leave them unchanged.
		"""
		values = ("no", "yes", "")
	class role(xsc.TextAttr):
		"""
		If specified, must have a value that is a set of space-separated tokens
		representing the various WAI-ARIA roles that the element belongs to.
		"""
	class onabort(xsc.TextAttr):
		"""
		Event handler
		"""
	class onblur(xsc.TextAttr):
		"""
		Event handler
		"""
	class oncancel(xsc.TextAttr):
		"""
		Event handler
		"""
	class oncanplay(xsc.TextAttr):
		"""
		Event handler
		"""
	class oncanplaythrough(xsc.TextAttr):
		"""
		Event handler
		"""
	class onchange(xsc.TextAttr):
		"""
		Event handler
		"""
	class onclick(xsc.TextAttr):
		"""
		Event handler
		"""
	class onclose(xsc.TextAttr):
		"""
		Event handler
		"""
	class oncontextmenu(xsc.TextAttr):
		"""
		Event handler
		"""
	class oncuechange(xsc.TextAttr):
		"""
		Event handler
		"""
	class ondblclick(xsc.TextAttr):
		"""
		Event handler
		"""
	class ondrag(xsc.TextAttr):
		"""
		Event handler
		"""
	class ondragend(xsc.TextAttr):
		"""
		Event handler
		"""
	class ondragenter(xsc.TextAttr):
		"""
		Event handler
		"""
	class ondragleave(xsc.TextAttr):
		"""
		Event handler
		"""
	class ondragover(xsc.TextAttr):
		"""
		Event handler
		"""
	class ondragstart(xsc.TextAttr):
		"""
		Event handler
		"""
	class ondrop(xsc.TextAttr):
		"""
		Event handler
		"""
	class ondurationchange(xsc.TextAttr):
		"""
		Event handler
		"""
	class onemptied(xsc.TextAttr):
		"""
		Event handler
		"""
	class onended(xsc.TextAttr):
		"""
		Event handler
		"""
	class onerror(xsc.TextAttr):
		"""
		Event handler
		"""
	class onfocus(xsc.TextAttr):
		"""
		Event handler
		"""
	class oninput(xsc.TextAttr):
		"""
		Event handler
		"""
	class oninvalid(xsc.TextAttr):
		"""
		Event handler
		"""
	class onkeydown(xsc.TextAttr):
		"""
		Event handler
		"""
	class onkeypress(xsc.TextAttr):
		"""
		Event handler
		"""
	class onkeyup(xsc.TextAttr):
		"""
		Event handler
		"""
	class onload(xsc.TextAttr):
		"""
		Event handler
		"""
	class onloadeddata(xsc.TextAttr):
		"""
		Event handler
		"""
	class onloadedmetadata(xsc.TextAttr):
		"""
		Event handler
		"""
	class onloadstart(xsc.TextAttr):
		"""
		Event handler
		"""
	class onmousedown(xsc.TextAttr):
		"""
		Event handler
		"""
	class onmousemove(xsc.TextAttr):
		"""
		Event handler
		"""
	class onmouseout(xsc.TextAttr):
		"""
		Event handler
		"""
	class onmouseover(xsc.TextAttr):
		"""
		Event handler
		"""
	class onmouseup(xsc.TextAttr):
		"""
		Event handler
		"""
	class onmousewheel(xsc.TextAttr):
		"""
		Event handler
		"""
	class onpause(xsc.TextAttr):
		"""
		Event handler
		"""
	class onplay(xsc.TextAttr):
		"""
		Event handler
		"""
	class onplaying(xsc.TextAttr):
		"""
		Event handler
		"""
	class onprogress(xsc.TextAttr):
		"""
		Event handler
		"""
	class onratechange(xsc.TextAttr):
		"""
		Event handler
		"""
	class onreset(xsc.TextAttr):
		"""
		Event handler
		"""
	class onscroll(xsc.TextAttr):
		"""
		Event handler
		"""
	class onseeked(xsc.TextAttr):
		"""
		Event handler
		"""
	class onseeking(xsc.TextAttr):
		"""
		Event handler
		"""
	class onselect(xsc.TextAttr):
		"""
		Event handler
		"""
	class onshow(xsc.TextAttr):
		"""
		Event handler
		"""
	class onstalled(xsc.TextAttr):
		"""
		Event handler
		"""
	class onsubmit(xsc.TextAttr):
		"""
		Event handler
		"""
	class onsuspend(xsc.TextAttr):
		"""
		Event handler
		"""
	class ontimeupdate(xsc.TextAttr):
		"""
		Event handler
		"""
	class onvolumechange(xsc.TextAttr):
		"""
		Event handler
		"""
	class onwaiting(xsc.TextAttr):
		"""
		Event handler
		"""
	class itemscope(xsc.BoolAttr):
		"""
		Microdata attribute: Creates a new item, a group of name-value pairs.
		"""
	class itemtype(xsc.TextAttr):
		"""
		Microdata attribute: Space separated list of absolute URLs specifying the type of the item.
		"""
	class itemid(xsc.URLAttr):
		"""
		Microdata attribute: A global identifier for the item.
		"""
	class itemprop(xsc.TextAttr):
		"""
		Microdata attribute: The name of an item property.
		"""
	class itemref(xsc.TextAttr):
		"""
		Microdata attribute: List of additional element IDs to crawl to find the name-value pairs of the item.
		"""


class CommonFormAttrs(GlobalAttrs):
	class name(xsc.TextAttr):
		"""
		The name of the form control, as used in form submission and in the
		form element's elements object. If the attribute is specified, its
		value must not be the empty string.
		"""
	class disabled(xsc.BoolAttr):
		"""
		Makes the control non-interactive and prevents its value from being
		submitted.
		"""
	class autofocus(xsc.BoolAttr):
		"""
		Allows the author to indicate that a control is to be focused as soon
		as the page is loaded or as soon as the dialog within which it finds
		itself is shown, allowing the user to just start typing without having
		to manually focus the main control.
		"""
	class form(xsc.TextAttr):
		"""
		Used to explicitly associate the element with its form owner.
		"""


###
### Elements
###

class html(xsc.Element):
	"""
	The root of an HTML document.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class manifest(xsc.URLAttr):
			"""
			The address of the document's application cache manifest, if there is
			one.
			"""


###
### Document metadata
###

class head(xsc.Element):
	"""
	A collection of metadata for the document.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class profile(xsc.URLAttr):
			deprecated = True


class title(xsc.Element):
	"""
	The document's title or name.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(GlobalAttrs):
		pass


class base(xsc.Element):
	"""
	Allows authors to specify the document base URL for the purposes of resolving
	relative URLs, and the name of the default browsing context for the purposes
	of following hyperlinks.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class href(xsc.URLAttr):
			"""
			The document base URL.
			"""
		class target(xsc.TextAttr):
			"""
			The name of the default browsing context.
			"""

class link(xsc.Element):
	"""
	Allows authors to link their document to other resources.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class href(xsc.URLAttr):
			"""
			Destination of the link.
			"""
		class rel(xsc.TextAttr):
			"""
			The type relationship the link has to the document.
			"""
		class media(MediaAttr):
			"""
			The media the resource applies to.
			"""
		class hreflang(xsc.TextAttr):
			"""
			The language of the linked resource.
			"""
		class type(xsc.TextAttr):
			"""
			The MIME type of the linked resource.
			"""
		class sizes(xsc.TextAttr):
			"""
			The sizes of icons for visual media.
			"""
		class rev(xsc.TextAttr):
			deprecated = True
		class charset(xsc.TextAttr):
			deprecated = True
		class target(xsc.TextAttr):
			deprecated = True


class meta(xsc.Element):
	"""
	Various kinds of metadata that cannot be expressed using the ``title``,
	``base``, ``link``, ``style``, and ``script`` elements.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class id(GlobalAttrs.id):
			pass
		class http_equiv(xsc.TextAttr):
			"""
			The name of the pragma directive.
			"""
			xmlname = "http-equiv"
		class name(xsc.TextAttr):
			"""
			The name of the metadata element.
			"""
		class content(xsc.TextAttr):
			"""
			The value of the document metadata or pragma directive.
			"""
		class charset(xsc.TextAttr):
			"""
			The character encoding used by the document.
			"""
		class scheme(xsc.TextAttr):
			deprecated = True

	def publish(self, publisher):
		if "http-equiv" in self.attrs and not self.attrs.http_equiv.isfancy():
			ctype = str(self.attrs.http_equiv).lower()
			if ctype == "content-type" and "content" in self.attrs:
				(contenttype, options) = cgi.parse_header(str(self.attrs.content))
				encoding = publisher.getencoding()
				if "charset" not in options or options["charset"] != encoding:
					options["charset"] = encoding
					node = self.__class__(
						self.attrs,
						http_equiv="Content-Type",
						content=(contenttype, "; ", "; ".join(f"{name}={value}" for (name, value) in options.items())),
					)
					return node.publish(publisher) # return a generator-iterator
		return super().publish(publisher) # return a generator-iterator


class style(xsc.Element):
	"""
	Allows authors to embed style information in their documents.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(GlobalAttrs):
		class media(MediaAttr):
			"""
			Specifies which media the styles apply to.
			"""
		class type(xsc.TextAttr):
			"""
			The styling language as a valid MIME type.
			"""
		class scoped(xsc.BoolAttr):
			"""
			Indicates that the styles are intended just for the subtree rooted at
			the style element's parent element.
			"""


###
### Scripting
###

class script(xsc.Element):
	"""
	Allows authors to include dynamic script and data blocks in their documents.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(GlobalAttrs):
		class src(xsc.URLAttr):
			"""
			If specified, gives the address of the external script resource to use.
			"""
		class async_(xsc.BoolAttr):
			"""
			If present, the script will be executed asynchronously.
			"""
			xmlname = "async"

		class defer(xsc.BoolAttr):
			"""
			If present, the script is executed when the page has finished parsing.
			"""
		class type(xsc.TextAttr):
			"""
			The language of the script or format of the data. If the attribute is
			present, its value must be a valid MIME type.
			"""
		class charset(xsc.TextAttr):
			"""
			The character encoding of the external script resource.
			"""
		class language(xsc.TextAttr):
			"""
			Only used if there's no ``type`` attribute. The MIME subtype (the main
			type being ``text`` automatically)
			"""
			deprecated = True
		class event(xsc.TextAttr):
			"""
			Must be ``onload`` or ``onload()``.
			"""
			deprecated = True
		class for_(xsc.TextAttr):
			"""
			Must be ``window``.
			"""
			xmlname = "for"
			deprecated = True


class noscript(xsc.Element):
	"""
	Represents nothing if scripting is enabled, and represents its children if
	scripting is disabled.
	"""
	xmlns = xmlns
	model = sims.Transparent()
	class Attrs(GlobalAttrs):
		pass


###
### Sections
###


class body(xsc.Element):
	"""
	The main content of the document.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class onafterprint(xsc.TextAttr):
			"""
			Event handler
			"""
		class onbeforeprint(xsc.TextAttr):
			"""
			Event handler
			"""
		class onbeforeunload(xsc.TextAttr):
			"""
			Event handler
			"""
		class onhashchange(xsc.TextAttr):
			"""
			Event handler
			"""
		class onmessage(xsc.TextAttr):
			"""
			Event handler
			"""
		class onoffline(xsc.TextAttr):
			"""
			Event handler
			"""
		class ononline(xsc.TextAttr):
			"""
			Event handler
			"""
		class onpagehide(xsc.TextAttr):
			"""
			Event handler
			"""
		class onpageshow(xsc.TextAttr):
			"""
			Event handler
			"""
		class onpopstate(xsc.TextAttr):
			"""
			Event handler
			"""
		class onresize(xsc.TextAttr):
			"""
			Event handler
			"""
		class onstorage(xsc.TextAttr):
			"""
			Event handler
			"""
		class onunload(xsc.TextAttr):
			"""
			Event handler
			"""
		class background(xsc.URLAttr):
			deprecated = True
		class bgcolor(xsc.ColorAttr):
			deprecated = True
		class text(xsc.ColorAttr):
			deprecated = True
		class link(xsc.ColorAttr):
			deprecated = True
		class vlink(xsc.ColorAttr):
			deprecated = True
		class alink(xsc.ColorAttr):
			deprecated = True
		class leftmargin(xsc.IntAttr):
			deprecated = True
		class topmargin(xsc.IntAttr):
			deprecated = True
		class marginwidth(xsc.IntAttr):
			deprecated = True
		class marginheight(xsc.IntAttr):
			deprecated = True


class article(xsc.Element):
	"""
	A self-contained composition in a document, page, application, or site and
	that is, in principle, independently distributable or reusable, e.g. in
	syndication.

	This could be a forum post, a magazine or newspaper article, a blog entry,
	a user-submitted comment, an interactive widget or gadget, or any other
	independent item of content.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class section(xsc.Element):
	"""
	A generic section of a document or application. A section, in this context,
	is a thematic grouping of content, typically with a heading.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class nav(xsc.Element):
	"""
	A section of a page that links to other pages or to parts within the page:
	a section with navigation links.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class aside(xsc.Element):
	"""
	A section of a page that consists of content that is tangentially related to
	the content around the aside element, and which could be considered separate
	from that content. Such sections are often represented as sidebars in printed
	typography.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class h(xsc.Element):
	"""
	Base class of :class:`h1`, :class:`h2`, :class:`h3`, :class:`h4`, :class:`h5`
	and :class:`h6`, which represent headings for their sections.
	"""
	xmlns = xmlns
	register = False
	class Attrs(GlobalAttrs):
		class align(xsc.TextAttr):
			deprecated = True
			values = ("left", "right", "center", "justify")


class h1(h):
	pass


class h2(h):
	pass


class h3(h):
	pass


class h4(h):
	pass


class h5(h):
	pass


class h6(h):
	pass


class hgroup(xsc.Element):
	"""
	The heading of a section. The element is used to group a set of ``h1``–``h6``
	elements when the heading has multiple levels, such as subheadings,
	alternative titles, or taglines.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class header(xsc.Element):
	"""
	A group of introductory or navigational aids.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class footer(xsc.Element):
	"""
	A footer for its nearest ancestor sectioning content or sectioning root
	element. A footer typically contains information about its section such as
	who wrote it, links to related documents, copyright data, and the like.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class address(xsc.Element):
	"""
	The contact information for its nearest ``article`` or ``body`` element
	ancestor.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


###
### Grouping content
###

class p(xsc.Element):
	"""
	A paragraph.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class align(xsc.TextAttr):
			deprecated = True
			values = ("left", "right", "center", "justify")


class hr(xsc.Element):
	"""
	A paragraph-level thematic break, e.g. a scene change in a story, or a
	transition to another topic within a section of a reference book.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class align(xsc.TextAttr):
			deprecated = True
			values = ("left", "right", "center")
		class noshade(xsc.BoolAttr):
			deprecated = True
		class size(xsc.IntAttr):
			deprecated = True
		class width(xsc.TextAttr):
			deprecated = True
		class color(xsc.ColorAttr):
			deprecated = True


class pre(xsc.Element):
	"""
	A block of preformatted text, in which structure is represented by
	typographic conventions rather than by elements.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class width(xsc.IntAttr):
			deprecated = True


class blockquote(xsc.Element):
	"""
	A section that is quoted from another source.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class cite(xsc.URLAttr):
			"""
			The source address of the quote.
			"""


class ol(xsc.Element):
	"""
	A list of items, where the items have been intentionally ordered, such that
	changing the order would change the meaning of the document.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class reversed(xsc.BoolAttr):
			"""
			If present, it indicates that the list is a descending list
			(..., 3, 2, 1). If the attribute is omitted, the list is an ascending
			list (1, 2, 3, ...).
			"""
		class start(xsc.TextAttr):
			"""
			The ordinal value of the first list item.
			"""
		class type(xsc.TextAttr):
			"""
			The kind of marker to use in the list.
			"""
			values = ("1", "a", "A", "i", "I")
		class compact(xsc.BoolAttr):
			deprecated = True


class ul(xsc.Element):
	"""
	A list of items, where the order of the items is not important — that is,
	where changing the order would not materially change the meaning of the
	document.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class type(xsc.TextAttr):
			deprecated = True
			values = ("disc", "square", "circle")
		class compact(xsc.BoolAttr):
			deprecated = True


class li(xsc.Element):
	"""
	A list item.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class value(xsc.IntAttr):
			"""
			The ordinal value of the list item if the element is a child of an
			``ol`` element.
			"""
		class type(xsc.TextAttr):
			deprecated = True


class dl(xsc.Element):
	"""
	An association list consisting of zero or more name-value groups (a
	description list). Each group must consist of one or more names
	(``dt`` elements) followed by one or more values (``dd`` elements).
	Within a single dl element, there should not be more than one ``dt`` element
	for each name.

	Name-value groups may be terms and definitions, metadata topics and values,
	questions and answers, or any other groups of name-value data.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class compact(xsc.BoolAttr):
			deprecated = True


class dt(xsc.Element):
	"""
	The term, or name, part of a term-description group in a description list
	(``dl`` element).
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class dd(xsc.Element):
	"""
	The description, definition, or value, part of a term-description group in a
	description list (``dl`` element).
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class figure(xsc.Element):
	"""
	Some flow content, optionally with a caption, that is self-contained and is
	typically referenced as a single unit from the main flow of the document.

	The element can thus be used to annotate illustrations, diagrams, photos,
	code listings, etc, that are referred to from the main content of the
	document, but that could, without affecting the flow of the document, be
	moved away from that primary content, e.g. to the side of the page, to
	dedicated pages, or to an appendix.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class figcaption(xsc.Element):
	"""
	A caption or legend for the rest of the contents of the ``figcaption``
	element's parent ``figure`` element, if any.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class div(xsc.Element):
	"""
	The ``div`` element has no special meaning at all. It represents its
	children. It can be used with the ``class``, ``lang``, and ``title``
	attributes to mark up semantics common to a group of consecutive elements.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class align(xsc.TextAttr):
			deprecated = True
			values = ("left", "right", "center", "justify")


###
### Text-level semantics
###

class a(xsc.Element):
	"""
	If the ``a`` element has an ``href`` attribute, then it represents a
	hyperlink (a hypertext anchor) labeled by its contents.

	If the ``a`` element has no ``href`` attribute, then the element represents
	a placeholder for where a link might otherwise have been placed, if it had
	been relevant, consisting of just the element's contents.
	"""
	xmlns = xmlns
	model = sims.Transparent()
	class Attrs(GlobalAttrs):
		class href(xsc.URLAttr):
			"""
			Destination of the link.
			"""
		class target(xsc.TextAttr):
			"""
			The name of the browsing context for this link.
			"""
		class rel(xsc.TextAttr):
			"""
			The type of relationship the link has to the document.
			"""
		class media(MediaAttr):
			"""
			The media the resource applies to.
			"""
		class hreflang(xsc.TextAttr):
			"""
			The language of the linked resource.
			"""
		class type(xsc.TextAttr):
			"""
			The MIME type of the linked resource.
			"""
		class name(xsc.TextAttr):
			deprecated = True
		class coords(xsc.TextAttr):
			deprecated = True
		class charset(xsc.TextAttr):
			deprecated = True
		class shape(xsc.TextAttr):
			deprecated = True
			values = ("rect", "circle", "poly", "default")
		class rev(xsc.TextAttr):
			deprecated = True


class em(xsc.Element):
	"""
	Stress emphasis.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class strong(xsc.Element):
	"""
	Strong importance.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class small(xsc.Element):
	"""
	Side comments such as small print.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class s(xsc.Element):
	"""
	Contents that are no longer accurate or no longer relevant.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class cite(xsc.Element):
	"""
	The title of a work (e.g. a book, a paper, an essay, a poem, a score, a song,
	a script, a film, a TV show, a game, a sculpture, a painting, a theatre
	production, a play, an opera, a musical, an exhibition, a legal case report,
	etc). This can be a work that is being quoted or referenced in detail (i.e.
	a citation), or it can just be a work that is mentioned in passing.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class q(xsc.Element):
	"""
	Some phrasing content quoted from another source.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class cite(xsc.URLAttr):
			"""
			The source address of the quote.
			"""


class dfn(xsc.Element):
	"""
	The defining instance of a term. The paragraph, description list group, or
	section that is the nearest ancestor of the ``dfn`` element must also contain
	the definition(s) for the term given by the ``dfn`` element.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class abbr(xsc.Element):
	"""
	An abbreviation or acronym, optionally with its expansion. The ``title``
	attribute may be used to provide an expansion of the abbreviation. The
	attribute, if specified, must contain an expansion of the abbreviation,
	and nothing else.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class time(xsc.Element):
	"""
	Represents its contents, along with a machine-readable form of those contents
	in the ``datetime`` attribute.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class datetime(xsc.TextAttr):
			"""
			The element's contents in a machine-readable format.
			"""


class code(xsc.Element):
	"""
	A fragment of computer code. This could be an XML element name, a filename,
	a computer program, or any other string that a computer would recognize.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class var(xsc.Element):
	"""
	A variable. This could be an actual variable in a mathematical expression or
	programming context, an identifier representing a constant, a symbol
	identifying a physical quantity, a function parameter, or just be a term used
	as a placeholder in prose.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class samp(xsc.Element):
	"""
	A (sample) output from a program or computing system.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class kbd(xsc.Element):
	"""
	User input (typically keyboard input, although it may also be used to
	represent other input, such as voice commands).
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class sub(xsc.Element):
	"""
	A subscript.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class sup(xsc.Element):
	"""
	A superscript.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class i(xsc.Element):
	"""
	A span of text in an alternate voice or mood, or otherwise offset from the
	normal prose in a manner indicating a different quality of text, such as a
	taxonomic designation, a technical term, an idiomatic phrase or short span of
	transliterated prose from another language, a thought, or a ship name in
	Western texts.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class b(xsc.Element):
	"""
	A span of text to which attention is being drawn for utilitarian purposes
	without conveying any extra importance and with no implication of an
	alternate voice or mood, such as key words in a document abstract, product
	names in a review, actionable words in interactive text-driven software,
	or an article lede.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class u(xsc.Element):
	"""
	A span of text with an unarticulated, though explicitly rendered, non-textual
	annotation, such as labeling the text as being a proper name in Chinese text
	(a Chinese proper name mark), or labeling the text as being misspelt.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class mark(xsc.Element):
	"""
	A run of text in one document marked or highlighted for reference purposes,
	due to its relevance in another context. When used in a quotation or other
	block of text referred to from the prose, it indicates a highlight that was
	not originally present but which has been added to bring the reader's
	attention to a part of the text that might not have been considered
	important by the original author when the block was originally written,
	but which is now under previously unexpected scrutiny. When used in the main
	prose of a document, it indicates a part of the document that has been
	highlighted due to its likely relevance to the user's current activity.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class ruby(xsc.Element):
	"""
	Allows one or more spans of phrasing content to be marked with ruby
	annotations. Ruby annotations are short runs of text presented alongside base
	text, primarily used in East Asian typography as a guide for pronunciation or
	to include other annotations. In Japanese, this form of typography is also
	known as "furigana".
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class rt(xsc.Element):
	"""
	The ruby text component of a ruby annotation.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class rp(xsc.Element):
	"""
	Can be used to provide parentheses around a ruby text component of a ruby
	annotation, to be shown by user agents that don't support ruby annotations.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class bdi(xsc.Element):
	"""
	A span of text that is to be isolated from its surroundings for the purposes
	of bidirectional text formatting.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class bdo(xsc.Element):
	"""
	Explicit text directionality formatting control for its children. It allows
	authors to override the Unicode bidirectional algorithm by explicitly
	specifying a direction override.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class dir(xsc.TextAttr):
			"""
			The element's text directionality.
			"""
			required = True
			values = ("ltr", "rtl")


class span(xsc.Element):
	"""
	Doesn't mean anything on its own, but can be useful when used together with
	the global attributes, e.g. ``class``, ``lang``, or ``dir``. It represents
	its children.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class br(xsc.Element):
	"""
	A line break.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class clear(xsc.TextAttr):
			deprecated = True
			values = ("left", "all", "right", "none")


class wbr(xsc.Element):
	"""
	A line break opportunity.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		pass


###
### Edits
###

class ins(xsc.Element):
	"""
	An addition to the document.
	"""
	xmlns = xmlns
	model = sims.Transparent()
	class Attrs(GlobalAttrs):
		class cite(xsc.URLAttr):
			"""
			The address of a document that explains the change.
			"""
		class datetime(xsc.TextAttr):
			"""
			The time and date of the change.
			"""


class del_(xsc.Element):
	"""
	A removal from the document.
	"""
	xmlns = xmlns
	xmlname = "del"
	model = sims.Transparent()
	class Attrs(GlobalAttrs):
		class cite(xsc.URLAttr):
			"""
			The address of a document that explains the change.
			"""
		class datetime(xsc.TextAttr):
			"""
			The time and date of the change.
			"""


###
### Embedded content
###

class img(xsc.Element):
	"""
	An image.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class alt(xsc.TextAttr):
			"""
			Provides equivalent content for those who cannot process images or who
			have image loading disabled.
			"""
		class src(xsc.URLAttr):
			"""
			A non-interactive, optionally animated, image resource that is neither
			paged nor scripted.
			"""
		class crossorigin(xsc.TextAttr):
			"""
			Allows images from third-party sites that allow cross-origin access to
			be used with canvas.
			"""
		class usemap(xsc.TextAttr):
			"""
			A valid hash-name reference to a ``map`` element that makes the image a
			clickable image map.
			"""
		class ismap(xsc.BoolAttr):
			"""
			When used on an element that is a descendant of an ``a`` element with
			an ``href`` attribute, indicates by its presence that the element
			provides access to a server-side image map.
			"""
		class width(xsc.IntAttr):
			"""
			The width of the image.
			"""
		class height(xsc.IntAttr):
			"""
			The height of the image.
			"""
		class name(xsc.TextAttr):
			deprecated = True
		class longdesc(xsc.URLAttr):
			deprecated = True
		class align(xsc.TextAttr):
			deprecated = True
			values = ("top", "middle", "bottom", "left", "right", "absmiddle")
		class border(xsc.TextAttr):
			deprecated = True
		class hspace(xsc.IntAttr):
			deprecated = True
		class vspace(xsc.IntAttr):
			deprecated = True
		class lowsrc(xsc.URLAttr):
			deprecated = True


class iframe(xsc.Element):
	"""
	A nested browsing context.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(GlobalAttrs):
		class src(xsc.URLAttr):
			"""
			The address of a page that the nested browsing context is to contain.
			"""
		class srcdoc(xsc.TextAttr):
			"""
			The content of the page that the nested browsing context is to contain.
			"""
		class name(xsc.TextAttr):
			"""
			A valid browsing context name. The given value is used to name the
			nested browsing context.
			"""
		class sandbox(xsc.TextAttr):
			"""
			Enables a set of extra restrictions on any content hosted by the
			``iframe``. Its value must be an unordered set of unique
			space-separated tokens that are ASCII case-insensitive. The allowed
			values are ``allow-forms``, ``allow-popups``, ``allow-same-origin``,
			``allow-scripts``, and ``allow-top-navigation``.
			"""
		class seamless(xsc.BoolAttr):
			"""
			Indicates that the iframe element's browsing context is to be rendered
			in a manner that makes it appear to be part of the containing document
			(seamlessly included in the parent document).
			"""
		class width(xsc.IntAttr):
			"""
			The width of the ``iframe``.
			"""
		class height(xsc.IntAttr):
			"""
			The height of the ``iframe``.
			"""
		class longdesc(xsc.URLAttr):
			deprecated = True
		class frameborder(xsc.TextAttr):
			deprecated = True
			values = (1, 0)
		class marginwidth(xsc.IntAttr):
			deprecated = True
		class marginheight(xsc.IntAttr):
			deprecated = True
		class noresize(xsc.BoolAttr):
			deprecated = True
		class scrolling(xsc.TextAttr):
			deprecated = True
			values = ("yes", "no", "auto")
		class align(xsc.TextAttr):
			deprecated = True
			values = ("top", "middle", "bottom", "left", "right", "absmiddle")
		class hspace(xsc.IntAttr):
			deprecated = True
		class vspace(xsc.IntAttr):
			deprecated = True
		class bordercolor(xsc.ColorAttr):
			deprecated = True
		class allowfullscreen(xsc.TextAttr):
			deprecated = True


class embed(xsc.Element):
	"""
	An integration point for an external (typically non-HTML) application or
	interactive content.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class src(xsc.URLAttr):
			"""
			The address of the resource being embedded.
			"""
		class type(xsc.TextAttr):
			"""
			The MIME type by which the plugin to instantiate is selected.
			"""
		class width(xsc.IntAttr):
			"""
			The width of the embedded resource.
			"""
		class height(xsc.IntAttr):
			"""
			The height of the embedded resource.
			"""
		class controller(xsc.TextAttr):
			deprecated = True
		class href(xsc.URLAttr):
			deprecated = True
		class target(xsc.TextAttr):
			deprecated = True
		class border(xsc.IntAttr):
			deprecated = True
		class pluginspage(xsc.URLAttr):
			deprecated = True
		class quality(xsc.TextAttr):
			deprecated = True
		class bgcolor(xsc.ColorAttr):
			deprecated = True
		class menu(xsc.TextAttr):
			deprecated = True
		class allowfullscreen(xsc.TextAttr):
			deprecated = True
		class flashvars(xsc.TextAttr):
			deprecated = True



class object(xsc.Element):
	"""
	This element can represent an external resource, which, depending on the type
	of the resource, will either be treated as an image, as a nested browsing
	context, or as an external resource to be processed by a plugin.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class data(xsc.URLAttr):
			"""
			The address of the resource.
			"""
		class type(xsc.TextAttr):
			"""
			The MIME type of the resource.
			"""
		class typemustmatch(xsc.BoolAttr):
			"""
			Indicates that the resource specified by the data attribute is only to
			be used if the value of the type attribute and the ``Content-Type`` of
			the aforementioned resource match.
			"""
		class name(xsc.TextAttr):
			"""
			A valid browsing context name. The given value is used to name the
			nested browsing context, if applicable.
			"""
		class usemap(xsc.TextAttr):
			"""
			A valid hash-name reference to a ``map`` element that makes the object
			a clickable map.
			"""
		class form(xsc.TextAttr):
			"""
			The id of the ``form`` element this object is associated with.
			"""
		class width(xsc.IntAttr):
			"""
			The width of the object.
			"""
		class height(xsc.IntAttr):
			"""
			The height of the object.
			"""
		class declare(xsc.BoolAttr):
			deprecated = True
		class classid(xsc.URLAttr):
			deprecated = True
		class codebase(xsc.URLAttr):
			deprecated = True
		class codetype(xsc.TextAttr):
			deprecated = True
		class archive(xsc.TextAttr):
			deprecated = True
		class standby(xsc.TextAttr):
			deprecated = True
		class align(xsc.TextAttr):
			deprecated = True
			values = ("top", "middle", "bottom", "left", "right", "absmiddle")
		class border(xsc.IntAttr):
			deprecated = True
		class hspace(xsc.IntAttr):
			deprecated = True
		class vspace(xsc.IntAttr):
			deprecated = True


class param(xsc.Element):
	"""
	Defines parameters for plugins invoked by ``object`` elements. It does not
	represent anything on its own.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class name(xsc.TextAttr):
			"""
			The name of the parameter.
			"""
			required = True
		class value(xsc.TextAttr):
			"""
			The value of the parameter.
			"""
			required = True
		class valuetype(xsc.TextAttr):
			deprecated = True
			values = ("data", "ref", "object")
		class type(xsc.TextAttr):
			deprecated = True


class video(xsc.Element):
	"""
	Used for playing videos or movies, and audio files with captions.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class src(xsc.URLAttr):
			"""
			The address of the media resource (video, audio) to show.
			"""
		class crossorigin(xsc.TextAttr):
			"""
			Specifies the origin behaviour for fetching the media resource.
			"""
			values = ("anonymous", "use-credentials", "")
		class poster(xsc.URLAttr):
			"""
			The address of an image file that the user agent can show while no
			video data is available.
			"""
		class preload(xsc.TextAttr):
			"""
			A hint to the user agent about what the author thinks will lead to the
			best user experience.
			"""
			values = ("none", "metadata", "auto", "")
		class autoplay(xsc.BoolAttr):
			"""
			When present, the user agent will automatically begin playback of the
			media resource as soon as it can do so without stopping.
			"""
		class mediagroup(xsc.TextAttr):
			"""
			Links multiple media elements together by implicitly creating a
			MediaController. The value is text; media elements with the same value
			are automatically linked by the user agent.
			"""
		class loop(xsc.BoolAttr):
			"""
			Indicates that the media element is to seek back to the start of the
			media resource upon reaching the end.
			"""
		class muted(xsc.BoolAttr):
			"""
			Controls the default state of the audio output of the media resource,
			potentially overriding user preferences.
			"""
		class controls(xsc.BoolAttr):
			"""
			Indicates that the author has not provided a scripted controller and
			would like the user agent to provide its own set of controls.
			"""
		class width(xsc.IntAttr):
			"""
			The width of the ``video`` element.
			"""
		class height(xsc.IntAttr):
			"""
			The height of the ``video`` element.
			"""


class audio(xsc.Element):
	"""
	A sound or audio stream.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class src(xsc.URLAttr):
			"""
			The address of the media resource (video, audio) to show.
			"""
		class crossorigin(xsc.TextAttr):
			"""
			Specifies the origin behaviour for fetching the media resource.
			"""
			values = ("anonymous", "use-credentials", "")
		class preload(xsc.TextAttr):
			"""
			A hint to the user agent about what the author thinks will lead to the
			best user experience.
			"""
			values = ("none", "metadata", "auto", "")
		class autoplay(xsc.BoolAttr):
			"""
			When present, the user agent will automatically begin playback of the
			media resource as soon as it can do so without stopping.
			"""
		class mediagroup(xsc.TextAttr):
			"""
			Links multiple media elements together by implicitly creating a
			MediaController. The value is text; media elements with the same value
			are automatically linked by the user agent.
			"""
		class loop(xsc.BoolAttr):
			"""
			Indicates that the media element is to seek back to the start of the
			media resource upon reaching the end.
			"""
		class muted(xsc.BoolAttr):
			"""
			Controls the default state of the audio output of the media resource,
			potentially overriding user preferences.
			"""
		class controls(xsc.BoolAttr):
			"""
			Indicates that the author has not provided a scripted controller and
			would like the user agent to provide its own set of controls.
			"""


class source(xsc.Element):
	"""
	Allows authors to specify multiple alternative media resources for media
	elements. It does not represent anything on its own.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class src(xsc.URLAttr):
			"""
			The address of the media resource.
			"""
			required = True
		class type(xsc.TextAttr):
			"""
			Helps the user agent determine if it can play this media resource
			before fetching it. If specified, its value must be a valid MIME type.
			"""
		class media(MediaAttr):
			"""
			The intended media type of the media resource, to help the user agent
			determine if this media resource is useful to the user before fetching
			it.
			"""


class track(xsc.Element):
	"""
	Allows authors to specify explicit external timed text tracks for media
	elements. It does not represent anything on its own.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class kind(xsc.TextAttr):
			"""
			The type of the track.
			"""
			values = ("subtitles", "captions", "descriptions", "chapters", "metadata")
		class src(xsc.URLAttr):
			"""
			The address of the text track data.
			"""
			required = True
		class srclang(xsc.TextAttr):
			"""
			The language of the text track data.
			"""
		class label(xsc.TextAttr):
			"""
			A user-readable title for the track. This title is used by user agents
			when listing subtitle, caption, and audio description tracks in their
			user interface.
			"""
		class default(xsc.BoolAttr):
			"""
			Indicates that the track is to be enabled if the user's preferences do
			not indicate that another track would be more appropriate.
			"""


class canvas(xsc.Element):
	"""
	Provides scripts with a resolution-dependent bitmap canvas, which can be used
	for rendering graphs, game graphics, art, or other visual images on the fly.
	"""
	xmlns = xmlns
	model = sims.Transparent()
	class Attrs(GlobalAttrs):
		class width(xsc.IntAttr):
			"""
			The width of the ``canvas`` element.
			"""
		class height(xsc.IntAttr):
			"""
			The height of the ``canvas`` element.
			"""


class map(xsc.Element):
	"""
	Defines an image map in conjunction with any ``area`` element descendants.
	The element represents its children.
	"""
	xmlns = xmlns
	model = sims.Transparent()
	class Attrs(GlobalAttrs):
		class name(xsc.TextAttr):
			"""
			Gives the map a name so that it can be referenced. The attribute must
			be present and must have a non-empty value with no space characters.
			"""
			required = True
		class class_(xsc.TextAttr):
			deprecated = True
			xmlname = "class"


class area(xsc.Element):
	"""
	Represents either a hyperlink with some text and a corresponding area on an
	image map, or a dead area on an image map.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class alt(xsc.TextAttr):
			"""
			Specifies the text of the hyperlink. Required if the ``href`` attribute
			is present.
			"""
		class coords(xsc.TextAttr):
			"""
			Gives the coordinates for the shape described by the shape attribute
			as a list of integers.
			"""
		class shape(xsc.TextAttr):
			"""
			The shape of the area.
			"""
			values = ("circle", "default", "poly", "rect")
		class href(xsc.TextAttr):
			"""
			Destination of the link.
			"""
		class target(xsc.TextAttr):
			"""
			The name of the browsing context for this link.
			"""
		class rel(xsc.TextAttr):
			"""
			The type of relationship the link has to the document.
			"""
		class media(MediaAttr):
			"""
			The media the resource applies to.
			"""
		class hreflang(xsc.TextAttr):
			"""
			The language of the linked resource.
			"""
		class type(xsc.TextAttr):
			"""
			The MIME type of the linked resource.
			"""
		class nohref(xsc.BoolAttr):
			deprecated = True


###
### Tabular data
###

class table(xsc.Element):
	"""
	Data with more than one dimension, in the form of a table.

	The ``table`` element takes part in the table model. Tables have rows,
	columns, and cells given by their descendants. The rows and columns form a
	grid; a table's cells must completely cover that grid without overlap.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class border(xsc.TextAttr):
			"""
			Indicate that the table element is not being used for layout purposes.
			"""
			values = ("1", "")
			values += ("0",) # deprecated

		class summary(xsc.TextAttr):
			deprecated = True
		class width(xsc.TextAttr):
			deprecated = True
		class frame(xsc.TextAttr):
			deprecated = True
			values = ("void", "above", "below", "hsides", "lhs", "rhs", "vsides", "box", "border")
		class rules(xsc.TextAttr):
			deprecated = True
			values = ("none", "groups", "rows", "cols", "all")
		class cellspacing(xsc.IntAttr):
			deprecated = True
		class cellpadding(xsc.IntAttr):
			deprecated = True
		class align(xsc.TextAttr):
			deprecated = True
			values = ("left", "right", "center")
		class bgcolor(xsc.ColorAttr):
			deprecated = True
		class height(xsc.TextAttr):
			deprecated = True
		class background(xsc.URLAttr):
			deprecated = True
		class bordercolor(xsc.ColorAttr):
			deprecated = True
		class hspace(xsc.IntAttr):
			deprecated = True
		class vspace(xsc.IntAttr):
			deprecated = True


class caption(xsc.Element):
	"""
	The title of the ``table`` that is its parent.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class align(xsc.TextAttr):
			deprecated = True
			values = ("top", "bottom", "left", "right")


class colgroup(xsc.Element):
	"""
	A group of one or more columns in the ``table`` that is its parent.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class span(xsc.IntAttr):
			pass
		class align(xsc.TextAttr):
			deprecated = True
			values = ("left", "center", "right", "justify", "char")
		class valign(xsc.TextAttr):
			deprecated = True
			values = ("top", "middle", "bottom", "baseline")
		class char(xsc.TextAttr):
			deprecated = True
		class charoff(xsc.TextAttr):
			deprecated = True
		class width(xsc.TextAttr):
			deprecated = True


class col(xsc.Element):
	"""
	One or more columns in the column group represented by the ``colgroup`` that
	is its parent.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class span(xsc.IntAttr):
			pass
		class align(xsc.TextAttr):
			deprecated = True
			values = ("left", "center", "right", "justify", "char")
		class valign(xsc.TextAttr):
			deprecated = True
			values = ("top", "middle", "bottom", "baseline")
		class char(xsc.TextAttr):
			deprecated = True
		class charoff(xsc.TextAttr):
			deprecated = True
		class width(xsc.TextAttr):
			deprecated = True


class tbody(xsc.Element):
	"""
	A block of rows that consist of a body of data for the parent ``table``
	element.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class charoff(xsc.TextAttr):
			deprecated = True
		class char(xsc.TextAttr):
			deprecated = True
		class valign(xsc.TextAttr):
			deprecated = True
		class align(xsc.TextAttr):
			deprecated = True


class thead(xsc.Element):
	"""
	The block of rows that consist of the column labels (headers) for the
	parent ``table`` element.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class charoff(xsc.TextAttr):
			deprecated = True
		class char(xsc.TextAttr):
			deprecated = True
		class valign(xsc.TextAttr):
			deprecated = True
		class align(xsc.TextAttr):
			deprecated = True


class tfoot(xsc.Element):
	"""
	The block of rows that consist of the column summaries (footers) for the
	parent ``table`` element
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class charoff(xsc.TextAttr):
			deprecated = True
		class char(xsc.TextAttr):
			deprecated = True
		class valign(xsc.TextAttr):
			deprecated = True
		class align(xsc.TextAttr):
			deprecated = True


class tr(xsc.Element):
	"""
	A row of cells in a table.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class align(xsc.TextAttr):
			deprecated = True
			values = ("left", "center", "right", "justify", "char")
		class char(xsc.TextAttr):
			deprecated = True
		class charoff(xsc.IntAttr):
			deprecated = True
		class valign(xsc.TextAttr):
			deprecated = True
			values = ("top", "middle", "bottom", "baseline")
		class bgcolor(xsc.ColorAttr):
			deprecated = True
		class nowrap(xsc.BoolAttr):
			deprecated = True
		class width(xsc.IntAttr):
			deprecated = True
		class background(xsc.URLAttr):
			deprecated = True


class td(xsc.Element):
	"""
	A data cell in a table.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class colspan(xsc.IntAttr):
			"""
			The number of columns that the cell is to span.
			"""
		class rowspan(xsc.IntAttr):
			"""
			The number of rows that the cell is to span.
			"""
		class headers(xsc.TextAttr):
			"""
			A space separated list of ids of ``th`` elements that this cell targets.
			"""
		class align(xsc.TextAttr):
			deprecated = True
			values = ("left", "center", "right", "justify", "char")
		class char(xsc.TextAttr):
			deprecated = True
		class charoff(xsc.IntAttr):
			deprecated = True
		class valign(xsc.TextAttr):
			deprecated = True
			values = ("top", "middle", "bottom", "baseline")
		class abbr(xsc.TextAttr):
			deprecated = True
		class axis(xsc.TextAttr):
			deprecated = True
		class scope(xsc.TextAttr):
			deprecated = True
			values = ("row", "col", "rowgroup", "colgroup")
		class nowrap(xsc.BoolAttr):
			deprecated = True
		class bgcolor(xsc.ColorAttr):
			deprecated = True
		class width(xsc.IntAttr):
			deprecated = True
		class height(xsc.IntAttr):
			deprecated = True
		class background(xsc.URLAttr):
			deprecated = True
		class bordercolor(xsc.ColorAttr):
			deprecated = True


class th(xsc.Element):
	"""
	A header cell in a table.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class colspan(xsc.IntAttr):
			"""
			The number of columns that the cell is to span.
			"""
		class rowspan(xsc.IntAttr):
			"""
			The number of rows that the cell is to span.
			"""
		class headers(xsc.TextAttr):
			"""
			A space separated list of ids of ``th`` elements that this cell targets.
			"""
		class scope(xsc.TextAttr):
			"""
			Specifies to which cells the header applies.
			"""
			values = ("row", "col", "rowgroup", "colgroup")
		class abbr(xsc.TextAttr):
			"""
			An alternative label for the header cell, to be used when referencing
			the cell in other contexts (e.g. when describing the header cells that
			apply to a data cell). It is typically an abbreviated form of the full
			header cell, but can also be an expansion, or merely a different
			phrasing.
			"""
		class align(xsc.TextAttr):
			deprecated = True
			values = ("left", "center", "right", "justify", "char")
		class char(xsc.TextAttr):
			deprecated = True
		class charoff(xsc.IntAttr):
			deprecated = True
		class valign(xsc.TextAttr):
			deprecated = True
			values = ("top", "middle", "bottom", "baseline")
		class axis(xsc.TextAttr):
			deprecated = True
		class nowrap(xsc.BoolAttr):
			deprecated = True
		class bgcolor(xsc.ColorAttr):
			deprecated = True
		class width(xsc.IntAttr):
			deprecated = True
		class height(xsc.IntAttr):
			deprecated = True
		class background(xsc.URLAttr):
			deprecated = True
		class bordercolor(xsc.ColorAttr):
			deprecated = True


###
### Forms
###


class form(xsc.Element):
	"""
	A collection of form-associated elements, some of which can represent
	editable values that can be submitted to a server for processing.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class accept_charset(xsc.TextAttr):
			"""
			The character encodings that are to be used for the submission.
			"""
			xmlname = "accept-charset"
		class action(xsc.URLAttr):
			"""
			The address to which this form will be submitted.
			"""
		class autocomplete(xsc.TextAttr):
			"""
			Specifies whether autocompletion should be done for this form.
			"""
			values = ("off", "on")
		class enctype(xsc.TextAttr):
			"""
			The encoding algorithm to use for encoding the form data.
			"""
			values = ("application/x-www-form-urlencoded", "multipart/form-data", "text/plain")
		class method(xsc.TextAttr):
			"""
			The HTTP method for submitting the form.
			"""
			values = ("get", "post")
		class name(xsc.TextAttr):
			"""
			The form's name within the forms collection.
			"""
		class novalidate(xsc.BoolAttr):
			"""
			Indicate that the form is not to be validated during submission.
			"""
		class target(xsc.TextAttr):
			"""
			The name of the browsing context for the response.
			"""


class fieldset(xsc.Element):
	"""
	A set of form controls optionally grouped under a common name.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class disabled(xsc.BoolAttr):
			"""
			Causes all the form control descendants of the ``fieldset`` element,
			excluding those that are descendants of the ``fieldset`` element's
			first legend element child, if any, to be disabled.
			"""
		class form(xsc.TextAttr):
			"""
			Used to explicitly associate the ``fieldset`` element with its form owner.
			"""
		class name(xsc.TextAttr):
			"""
			The element's name.
			"""


class legend(xsc.Element):
	"""
	A caption for the rest of the contents of the legend element's parent
	fieldset element, if any.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class align(xsc.TextAttr):
			deprecated = True
			values = ("top", "bottom", "left", "right")


class label(xsc.Element):
	"""
	A caption in a user interface. The caption can be associated with a specific
	form control, known as the label element's labeled control, either using
	``for`` attribute, or by putting the form control inside the label element
	itself.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class form(xsc.TextAttr):
			"""
			Used to explicitly associate the ``label`` element with its form owner.
			"""
		class for_(xsc.TextAttr):
			"""
			Indicate the id of a form control with which the caption is to be
			associated.
			"""
			xmlname = "for"


class input(xsc.Element):
	"""
	A caption in a user interface. The caption can be associated with a specific
	form control, known as the label element's labeled control, either using
	``for`` attribute, or by putting the form control inside the label element
	itself.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(CommonFormAttrs):
		class accept(xsc.TextAttr):
			"""
			Provides user agents with a hint of what file types will be accepted.
			A valid MIME type, or ``audio/*``, ``video/*``, ``image/*`` or a string
			starting with ``.`` the specify an allowed file extension.
			"""
		class alt(xsc.TextAttr):
			"""
			For ``type="button"``: provides the textual label for the button for
			users and user agents who cannot use the image.
			"""
		class autocomplete(xsc.TextAttr):
			"""
			The ``off`` state indicates either that the control's input data is
			particularly sensitive (for example the activation code for a nuclear
			weapon); or that it is a value that will never be reused (for example
			a one-time-key for a bank login) and the user will therefore have to
			explicitly enter the data each time, instead of being able to rely on
			the UA to prefill the value for him; or that the document provides its
			own autocomplete mechanism and does not want the user agent to provide
			autocompletion values.

			Conversely, the on state indicates that the value is not particularly
			sensitive and the user can expect to be able to rely on his user agent
			to remember values he has entered for that control.
			"""
			values = ("off", "on")
		class checked(xsc.BoolAttr):
			"""
			Gives the default checkedness of the input element.
			"""
		class dirname(xsc.TextAttr):
			"""
			Adds an additional name/value pair to the submitted data with this
			name that provides the writing direction of the submitted data.
			"""
		class formaction(xsc.TextAttr):
			"""
			Can be used on submit buttons to overwrite the ``action`` attribute
			of the form.
			"""
		class formenctype(xsc.TextAttr):
			"""
			Can be used on submit buttons to overwrite the ``enctype`` attribute
			of the form.
			"""
			values = ("application/x-www-form-urlencoded", "multipart/form-data", "text/plain")
		class formmethod(xsc.TextAttr):
			"""
			Can be used on submit buttons to overwrite the ``method`` attribute
			of the form.
			"""
			values = ("got", "post")
		class formnovalidate(xsc.BoolAttr):
			"""
			Can be used on submit buttons to overwrite the ``novalidate`` attribute
			of the form.
			"""
		class formtarget(xsc.TextAttr):
			"""
			Can be used on submit buttons to overwrite the ``target`` attribute
			of the form.
			"""
		class list(xsc.TextAttr):
			"""
			Identify an element that lists predefined options suggested to the user.

			If present, its value must be the ID of a datalist element in the same
			document.
			"""
		class max(xsc.TextAttr):
			"""
			Indicates the allowed maximum value for the element.
			"""
		class maxlength(xsc.IntAttr):
			"""
			The maximum length of the value.
			"""
		class min(xsc.TextAttr):
			"""
			Indicates the allowed minimum value for the element.
			"""
		class multiple(xsc.TextAttr):
			"""
			Indicates whether the user is to be allowed to specify more than one
			value.
			"""
		class pattern(xsc.TextAttr):
			"""
			A regular expression against which the control's value, or, when the
			multiple attribute applies and is set, the control's values, are to be
			checked.
			"""
		class placeholder(xsc.TextAttr):
			"""
			A short hint (a word or short phrase) intended to aid the user with
			data entry when the control has no value. A hint could be a sample
			value or a brief description of the expected format. The attribute,
			if specified, must have a value that contains no "LF" (U+000A) or
			"CR" (U+000D) characters.

			The ``placeholder`` attribute should not be used as an alternative to a
			label. For a longer hint or other advisory text, the ``title``
			attribute is more appropriate.
			"""
		class readonly(xsc.BoolAttr):
			"""
			Controls whether or not the user can edit the form control. When
			specified, the element is immutable.
			"""
		class required(xsc.BoolAttr):
			"""
			When specified, the element is required.
			"""
		class size(xsc.IntAttr):
			"""
			The number of characters that, in a visual rendering, the user agent
			is to allow the user to see while editing the element's value.
			"""
		class src(xsc.TextAttr):
			"""
			The address of the image for ``type="image"``.
			"""
		class step(xsc.TextAttr):
			"""
			The granularity that is expected (and required) of the value, by
			limiting the allowed values.
			"""
		class type(xsc.TextAttr):
			"""
			The data type (and associated control) of the element.
			"""
			values = ("hidden", "text", "search", "tel", "url", "email", "password", "datetime", "date", "month", "week", "time", "datetime", "number", "range", "color", "checkbox", "radio", "file", "submit", "image", "button")
		class value(xsc.TextAttr):
			"""
			The default value of the input element.
			"""
		class width(xsc.TextAttr):
			"""
			The width of the button image (for ``type="image"``)
			"""
		class height(xsc.TextAttr):
			"""
			The height of the button image (for ``type="image"``)
			"""
		class usemap(xsc.URLAttr):
			deprecated = True
		class align(xsc.TextAttr):
			deprecated = True
			values = ("top", "middle", "bottom", "left", "right", "absmiddle")
		class border(xsc.IntAttr):
			deprecated = True


class button(xsc.Element):
	"""
	A button labeled by its contents. The ``type`` attribute controls the
	behavior of the button when it is activated.
	"""
	xmlns = xmlns
	class Attrs(CommonFormAttrs):
		class formaction(xsc.TextAttr):
			"""
			Can be used on submit buttons to overwrite the ``action`` attribute
			of the form.
			"""
		class formenctype(xsc.TextAttr):
			"""
			Can be used on submit buttons to overwrite the ``enctype`` attribute
			of the form.
			"""
			values = ("application/x-www-form-urlencoded", "multipart/form-data", "text/plain")
		class formmethod(xsc.TextAttr):
			"""
			Can be used on submit buttons to overwrite the ``method`` attribute
			of the form.
			"""
			values = ("got", "post")
		class formnovalidate(xsc.BoolAttr):
			"""
			Can be used on submit buttons to overwrite the ``novalidate`` attribute
			of the form.
			"""
		class formtarget(xsc.TextAttr):
			"""
			Can be used on submit buttons to overwrite the ``target`` attribute
			of the form.
			"""
		class type(xsc.TextAttr):
			"""
			The type of the button. ``submit`` submits the form. ``reset`` resets
			the form and ``button`` does nothing.
			"""
			values = ("submit", "reset", "button")
		class value(xsc.TextAttr):
			"""
			The button's value for the purposes of form submission.

			A button (and its value) is only included in the form submission if the
			button itself was used to initiate the form submission.
			"""


class select(xsc.Element):
	"""
	A control for selecting amongst a set of options.
	"""
	xmlns = xmlns
	class Attrs(CommonFormAttrs):
		class multiple(xsc.TextAttr):
			"""
			Indicates whether the user is to be allowed to specify more than one
			value.
			"""
		class required(xsc.BoolAttr):
			"""
			When specified, the user will be required to select a value before
			submitting the form.
			"""
		class size(xsc.IntAttr):
			"""
			The number of options to show to the user.
			"""
		class rows(xsc.TextAttr):
			deprecated = True


class datalist(xsc.Element):
	"""
	A set of option elements that represent predefined options for other
	controls. The contents of the element represents fallback content for
	legacy user agents, intermixed with ``option`` elements that represent the
	predefined options. In the rendering, the ``datalist`` element represents
	nothing and it, along with its children, should be hidden.

	The datalist element is hooked up to an ``input`` element using the ``list``
	attribute on the ``input`` element.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class optgroup(xsc.Element):
	"""
	A group of ``option`` elements with a common label.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class disabled(xsc.BoolAttr):
			"""
			Can be used to disable a group of ``option`` elements together.
			"""
		class label(xsc.TextAttr):
			"""
			The name of the group, for the purposes of the user interface. User
			agents should use this attribute's value when labelling the group of
			``option`` elements in a ``select`` element.
			"""
			required = True


class option(xsc.Element):
	"""
	An option in a ``select`` element or as part of a list of suggestions in a
	``datalist`` element.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(GlobalAttrs):
		class disabled(xsc.BoolAttr):
			"""
			Specifies that the option should be disabled.
			"""
		class label(xsc.TextAttr):
			"""
			A label for the ``option`` element.
			"""
		class selected(xsc.BoolAttr):
			"""
			The default selectedness of the ``option`` element.
			"""
		class value(xsc.TextAttr):
			"""
			The value of the ``option`` element for the purposes of form submission
			when the ``option`` is selected.
			"""


class textarea(xsc.Element):
	"""
	A multiline plain text edit control for the element's raw value.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(CommonFormAttrs):
		class cols(xsc.IntAttr):
			"""
			The expected maximum number of characters per line.
			"""
		class dirname(xsc.TextAttr):
			"""
			Adds an additional name/value pair to the submitted data with this
			name that provides the writing direction of the submitted data.
			"""
		class maxlength(xsc.IntAttr):
			"""
			The maximum length of the value.
			"""
		class placeholder(xsc.TextAttr):
			"""
			A short hint (a word or short phrase) intended to aid the user with
			data entry when the control has no value. A hint could be a sample
			value or a brief description of the expected format. The attribute,
			if specified, must have a value that contains no "LF" (U+000A) or
			"CR" (U+000D) characters.

			The ``placeholder`` attribute should not be used as an alternative to a
			label. For a longer hint or other advisory text, the ``title``
			attribute is more appropriate.
			"""
		class readonly(xsc.BoolAttr):
			"""
			Controls whether the text can be edited by the user or not.
			"""
		class required(xsc.BoolAttr):
			"""
			When specified, the user will be required to enter a value before
			submitting the form.
			"""
		class rows(xsc.IntAttr):
			"""
			The number of lines to show.
			"""
		class wrap(xsc.TextAttr):
			"""
			Specifies how linefeeds in the controls value are to be handled.
			``soft`` indicates that the text in the ``textarea`` is not to be
			wrapped when it is submitted (though it can still be wrapped in the
			rendering). ``hard`` indicates that the text in the textarea is to have
			newlines added by the user agent so that the text is wrapped when it is
			submitted.
			"""
			values = ("soft", "hard")
			values += ("virtual", "physical", "off") # deprecated


class keygen(xsc.Element):
	"""
	A key pair generator control. When the control's form is submitted, the
	private key is stored in the local keystore, and the public key is packaged
	and sent to the server.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(CommonFormAttrs):
		class challenge(xsc.TextAttr):
			"""
			Its value will be packaged with the submitted key.
			"""
		class keytype(xsc.TextAttr):
			"""
			The type of key to be used. Only ``rsa`` is officially supported.
			"""


class output(xsc.Element):
	"""
	The result of a calculation.

	Allows an explicit relationship to be made between the result of a
	calculation and the elements that represent the values that went into
	the calculation or that otherwise influenced the calculation.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class for_(xsc.TextAttr):
			"""
			If specified, must be a list of space-separated ids of the elements
			that influenced the output.
			"""
			xmlname = "for"
		class form(xsc.TextAttr):
			"""
			Used to explicitly associate the ``output`` element with its form
			owner.
			"""
		class name(xsc.TextAttr):
			"""
			The element's name.
			"""


class progress(xsc.Element):
	"""
	The completion progress of a task.

	The progress is either indeterminate, indicating that progress is being made
	but that it is not clear how much more work remains to be done before the
	task is complete (e.g. because the task is waiting for a remote host to
	respond), or the progress is a number in the range zero to a maximum,
	giving the fraction of work that has so far been completed.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class value(xsc.FloatAttr):
			"""
			Specifies how much of the task has been completed. If ``value`` is not
			specified the progress is indeterminate.
			"""
		class max(xsc.FloatAttr):
			"""
			Specifies how much work the task requires in total.
			The units are arbitrary and not specified.
			"""


class meter(xsc.Element):
	"""
	A scalar measurement within a known range, or a fractional value; for example
	disk usage, the relevance of a query result, or the fraction of a voting
	population to have selected a particular candidate.

	This is also known as a gauge.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class value(xsc.FloatAttr):
			"""
			The value to have the gauge indicate as the "measured" value.
			"""
		class min(xsc.FloatAttr):
			"""
			The lower bound of the range.
			"""
		class max(xsc.FloatAttr):
			"""
			The lower bound of the range.
			"""
		class low(xsc.FloatAttr):
			"""
			The range that is considered to be the "low" part.
			"""
		class high(xsc.FloatAttr):
			"""
			The range that is considered to be the "high" part.
			"""
		class optimum(xsc.FloatAttr):
			"""
			The position that is "optimum".
			"""


###
### Interactive elements
###

class details(xsc.Element):
	"""
	A disclosure widget from which the user can obtain additional information or
	controls.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class open(xsc.BoolAttr):
			"""
			Indicates that both the summary and the additional information is to be
			shown to the user. If the attribute is absent, only the summary is to
			be shown.
			"""


class summary(xsc.Element):
	"""
	A summary, caption, or legend for the rest of the contents of the ``summary``
	element's parent ``details`` element, if any.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		pass


class command(xsc.Element):
	"""
	A summary, caption, or legend for the rest of the contents of the ``summary``
	element's parent ``details`` element, if any.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class type(xsc.TextAttr):
			"""
			Indicates the kind of command: either a normal command with an
			associated action, or a state or option that can be toggled, or a
			selection of one item from a list of items.
			"""
			values = ("command", "checkbox", "radio")
		class label(xsc.TextAttr):
			"""
			The name of the command, as shown to the user.
			"""
			required = True
		class icon(xsc.URLAttr):
			"""
			A picture that represents the command.
			"""
		class disabled(xsc.BoolAttr):
			"""
			Indicates that the command is not available in the current state.
			"""
		class checked(xsc.BoolAttr):
			"""
			Indicates that the command is selected (for ``type="checkbox"`` or
			``type="radio"``)
			"""
		class radiogroup(xsc.TextAttr):
			"""
			The name of the group of commands that will be toggled when the
			command itself is toggled (for ``type="radio"``).
			"""
		class command(xsc.TextAttr):
			"""
			The ID of the master command.
			"""


class menu(xsc.Element):
	"""
	A list of commands.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class type(xsc.TextAttr):
			"""
			The type of the menu.
			"""
			values = ("context", "toolbar")
		class label(xsc.TextAttr):
			"""
			The label of the menu. It is used by user agents to display nested
			menus in the UI.
			"""
		class compact(xsc.BoolAttr):
			deprecated = True


class dialog(xsc.Element):
	"""
 	A part of an application that a user interacts with to perform a task,
 	for example a dialog box, inspector, or window.
	"""
	xmlns = xmlns
	class Attrs(GlobalAttrs):
		class open(xsc.BoolAttr):
			"""
			Indicates that the ``dialog`` element is active and that the user can
			interact with it.
			"""


class data(xsc.Element):
	"""
	Microdata element: Contains the name and value of an item property.
	"""
	xmlns = xmlns
	model = sims.Transparent()
	class Attrs(xsc.Attrs):
		class itemprop(xsc.TextAttr):
			"""
			Microdata attribute: The name of an item property.
			"""
		class value(xsc.TextAttr):
			"""
			Microdata attribute: The value of an item property.
			"""


###
### Deprecated elements
###

class noframes(xsc.Element):
	"""
	Alternate content container for non frame-based rendering (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		pass


class dir(xsc.Element):
	"""
	Multiple column list (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		class compact(xsc.BoolAttr):
			pass


class center(xsc.Element):
	"""
	Centered block level element (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		pass


class acronym(xsc.Element):
	"""
	Indicates an acronym (e.g., WAC, radar, etc.) (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		pass


class tt(xsc.Element):
	"""
	Teletype or monospaced text style (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		pass


class big(xsc.Element):
	"""
	Large text style (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		pass


class strike(xsc.Element):
	"""
	Strike-through text style (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		pass


class basefont(xsc.Element):
	"""
	Base font size (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class face(xsc.TextAttr):
			pass
		class size(xsc.TextAttr):
			pass
		class color(xsc.ColorAttr):
			pass


class font(xsc.Element):
	"""
	Local change to font (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		class face(xsc.TextAttr):
			pass
		class size(xsc.TextAttr):
			pass
		class color(xsc.ColorAttr):
			pass


class applet(xsc.Element):
	"""
	Java applet (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		class codebase(xsc.URLAttr):
			pass
		class archive(xsc.TextAttr):
			pass
		class code(xsc.TextAttr):
			pass
		class object(xsc.TextAttr):
			pass
		class alt(xsc.TextAttr):
			pass
		class name(xsc.TextAttr):
			pass
		class width(xsc.TextAttr):
			required = True
		class height(xsc.TextAttr):
			required = True
		class align(xsc.TextAttr):
			values = ("top", "middle", "bottom", "left", "right", "absmiddle")
		class hspace(xsc.IntAttr):
			pass
		class vspace(xsc.IntAttr):
			pass


class isindex(xsc.Element):
	"""
	(deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class prompt(xsc.TextAttr):
			pass


class frameset(xsc.Element):
	"""
	Window subdivision (deprecated)
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		class rows(xsc.TextAttr):
			deprecated = True
		class cols(xsc.TextAttr):
			deprecated = True
		class onload(xsc.TextAttr):
			deprecated = True
		class onunload(xsc.TextAttr):
			deprecated = True
		class framespacing(xsc.TextAttr):
			deprecated = True
		class border(xsc.IntAttr):
			deprecated = True
		class marginwidth(xsc.IntAttr):
			deprecated = True
		class marginheight(xsc.IntAttr):
			deprecated = True
		class frameborder(xsc.IntAttr):
			deprecated = True
		class noresize(xsc.BoolAttr):
			deprecated = True
		class scrolling(xsc.TextAttr):
			deprecated = True


class frame(xsc.Element):
	"""
	Subwindow (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	model = sims.Empty()
	class Attrs(GlobalAttrs):
		class longdesc(xsc.TextAttr):
			deprecated = True
		class name(xsc.TextAttr):
			deprecated = True
		class src(xsc.URLAttr):
			deprecated = True
		class frameborder(xsc.TextAttr):
			deprecated = True
		class marginwidth(xsc.IntAttr):
			deprecated = True
		class marginheight(xsc.IntAttr):
			deprecated = True
		class noresize(xsc.BoolAttr):
			deprecated = True
		class scrolling(xsc.TextAttr):
			deprecated = True
		class framespacing(xsc.TextAttr):
			deprecated = True
		class border(xsc.IntAttr):
			deprecated = True
		class frameborder(xsc.IntAttr):
			deprecated = True
		class noresize(xsc.BoolAttr):
			deprecated = True
		class scrolling(xsc.TextAttr):
			deprecated = True


class nobr(xsc.Element):
	"""
	Prevents line breaks (deprecated).
	"""
	xmlns = xmlns
	deprecated = True
	class Attrs(GlobalAttrs):
		pass


###
### Content models
###

content_metadata = (base, command, link, meta, noscript, script, style, title)

content_sectioning = (article, aside, nav, section)

content_heading = (h1, h2, h3, h4, h5, h6, hgroup)

content_phrasing = (
	a, abbr, acronym, applet, area, audio, b, bdi, bdo, big, br, button, canvas,
	center, cite, code, command, data, datalist, del_, dfn, em, embed, font, i, iframe,
	img, input, ins, kbd, keygen, label, map, mark, meter, nobr, noframes,
	noscript, object, output, progress, q, ruby, s, samp, script, select, small,
	span, strike, strong, sub, sup, textarea, time, tt, u, var, video, wbr,
)

content_flow = content_phrasing + (
	address, article, aside, blockquote, details, dialog, dir, div, dl, fieldset,
	figure, footer, form, h1, h2, h3, h4, h5, h6, header, hgroup, hr, menu, nav,
	noframes, ol, p, pre, section, style, table, ul,
)

# We don't include ``audio``, ``img``, ``input``, ``menu``, ``object`` and ``video``
# here because they're only interactive under certain conditions.
content_interactive = (
	a, button, details, embed, iframe, keygen, label, select, textarea,
)

html.model = sims.Elements(head, body, frameset)
head.model = sims.Elements(*content_metadata)
body.model = sims.ElementsOrText(*content_flow)
article.model = sims.ElementsOrText(*content_flow)
section.model = sims.ElementsOrText(*content_flow)
nav.model = sims.ElementsOrText(*content_flow)
aside.model = sims.ElementsOrText(*content_flow)
h.model = sims.ElementsOrText(*content_phrasing)
hgroup.model = sims.Elements(h1, h2, h3, h4, h5, h6)
header.model = sims.ElementsOrText(*tuple(e for e in content_flow if e not in (header, footer)))
footer.model = sims.ElementsOrText(*tuple(e for e in content_flow if e not in (header, footer)))
address.model = sims.ElementsOrText(*tuple(e for e in content_flow if e not in content_heading + content_sectioning + (header, footer, address)))
p.model = sims.ElementsOrText(*content_phrasing)
pre.model = sims.ElementsOrText(*content_phrasing)
blockquote.model = sims.ElementsOrText(*content_flow)
ol.model = sims.Elements(li)
ul.model = sims.Elements(li)
li.model = sims.ElementsOrText(*content_flow)
dl.model = sims.Elements(dt, dd)
dt.model = sims.ElementsOrText(*tuple(e for e in content_flow if e not in content_heading + content_sectioning + (header, footer)))
dd.model = sims.ElementsOrText(*content_flow)
figure.model = sims.ElementsOrText(figcaption, *content_flow)
figcaption.model = sims.ElementsOrText(*content_flow)
div.model = sims.ElementsOrText(*content_flow)
em.model = sims.ElementsOrText(*content_phrasing)
strong.model = sims.ElementsOrText(*content_phrasing)
small.model = sims.ElementsOrText(*content_phrasing)
s.model = sims.ElementsOrText(*content_phrasing)
cite.model = sims.ElementsOrText(*content_phrasing)
q.model = sims.ElementsOrText(*content_phrasing)
dfn.model = sims.ElementsOrText(*tuple(e for e in content_phrasing if e is not dfn))
abbr.model = sims.ElementsOrText(*content_phrasing)
time.model = sims.ElementsOrText(*content_phrasing)
code.model = sims.ElementsOrText(*content_phrasing)
var.model = sims.ElementsOrText(*content_phrasing)
samp.model = sims.ElementsOrText(*content_phrasing)
kbd.model = sims.ElementsOrText(*content_phrasing)
sub.model = sims.ElementsOrText(*content_phrasing)
sup.model = sims.ElementsOrText(*content_phrasing)
i.model = sims.ElementsOrText(*content_phrasing)
b.model = sims.ElementsOrText(*content_phrasing)
u.model = sims.ElementsOrText(*content_phrasing)
mark.model = sims.ElementsOrText(*content_phrasing)
ruby.model = sims.ElementsOrText(rt, rp, *content_phrasing)
rt.model = sims.ElementsOrText(*content_phrasing)
rp.model = sims.ElementsOrText(*content_phrasing)
bdi.model = sims.ElementsOrText(*content_phrasing)
bdo.model = sims.ElementsOrText(*content_phrasing)
span.model = sims.ElementsOrText(*content_phrasing)
object.model = sims.ElementsOrText(*((param,) + content_flow + content_interactive))
video.model = sims.All(sims.Any(sims.ElementsOrText(source, track), sims.Transparent()), sims.NotElements(video, audio))
audio.model = sims.All(sims.Any(sims.ElementsOrText(source, track), sims.Transparent()), sims.NotElements(video, audio))
table.model = sims.Elements(caption, colgroup, thead, tfoot, tbody, tr)
caption.model = sims.ElementsOrText(*tuple(e for e in content_flow if e is not table))
colgroup.model = sims.Elements(col)
tbody.model = sims.Elements(tr)
thead.model = sims.Elements(tr)
tfoot.model = sims.Elements(tr)
tr.model = sims.Elements(td, th)
td.model = sims.ElementsOrText(*content_flow)
th.model = sims.ElementsOrText(*tuple(e for e in content_flow if e not in content_heading + content_sectioning + (header, footer)))
form.model = sims.ElementsOrText(*tuple(e for e in content_flow if e is not form))
fieldset.model = sims.ElementsOrText(legend, *content_flow)
legend.model = sims.ElementsOrText(*content_phrasing)
label.model = sims.ElementsOrText(*tuple(e for e in content_phrasing if e is not label))
button.model = sims.ElementsOrText(*tuple(e for e in content_phrasing if e not in content_interactive))
select.model = sims.ElementsOrText(option, optgroup)
datalist.model = sims.ElementsOrText(option, *content_phrasing)
optgroup.model = sims.Elements(option)
output.model = sims.ElementsOrText(*content_phrasing)
progress.model = sims.ElementsOrText(*tuple(e for e in content_phrasing if e is not progress))
meter.model = sims.ElementsOrText(*tuple(e for e in content_phrasing if e is not meter))
details.model = sims.ElementsOrText(summary, *content_flow)
summary.model = sims.ElementsOrText(*content_phrasing)
menu.model = sims.ElementsOrText(li, *content_flow)
dialog.model = sims.ElementsOrText(*content_flow)

# Content models for deprectated elements

noframes.model = sims.Elements(body)
dir.model = sims.Elements(li)
center.model = sims.ElementsOrText(*content_flow)
acronym.model = sims.ElementsOrText(*content_phrasing)
tt.model = sims.ElementsOrText(*content_phrasing)
big.model = sims.ElementsOrText(*content_phrasing)
strike.model = sims.ElementsOrText(*content_phrasing)
font.model = sims.ElementsOrText(*content_phrasing)
applet.model = sims.ElementsOrText(*((param,) + content_flow + content_interactive))
frameset.model = sims.Elements(frameset, frame, noframes)
nobr.model = sims.ElementsOrText(*content_flow)


###
### HTML to plain text conversion
###

class _PlainTextFormatter:
	class Style:
		def __init__(self, display="inline", top=0, bottom=0, left=("",), right=("",), whitespace="normal", overline=None, underline=None, prefix="", suffix=""):
			self.display = display
			self.top = top
			self.bottom = bottom
			self.left = (left,) if isinstance(left, str) else left
			self.right = (right,) if isinstance(right, str) else right
			self.whitespace = whitespace
			self.overline = overline
			self.underline = underline
			self.prefix = prefix
			self.suffix = suffix

		def margins(self, node, name, level, pos=None, last=None):
			return _PlainTextFormatter.Margins(self, node, name, level, pos, last)

	class Margins:
		def __init__(self, style, node, name, level, pos, last):
			self.style = style
			self.node = node
			self.name = name
			left = style.left[level if level < len(style.left) else -1]
			right = style.right[level if level < len(style.right) else -1]
			if pos is not None:
				width = len(str(last))
				left = left.format(pos=pos, width=width)
				right = right.format(pos=pos, width=width)
			left = left.split("\n")
			right = right.split("\n")
			self.leftwidth = max(len(line) for line in left)
			self.rightwidth = max(len(line) for line in right)
			self.lefts = self.repeatlast([line.rjust(self.leftwidth) for line in left])
			self.rights = self.repeatlast([line.ljust(self.rightwidth) for line in right])

		def repeatlast(self, items):
			yield from items
			while True:
				yield items[-1]

	def __init__(self, node, width=80, **styles):
		self.node = node
		self.width = width
		self.styles = {key: self.Style(**value) for (key, value) in styles.items()}
		self.stack = []
		self.blockspacing = 0
		self.texts = []
		self.levels = collections.Counter()

	def push(self, node, name=None, pos=None, last=None):
		r"""
		Add an additional box around any further text.

		:obj:`node` is the HTML element itself for which the box gets added.

		:obj:`name` is the name of the box (normally the name of the HTML element
		itself (``"ul"``, ``"dd"``, ``"pre"``, ``"blockquote"`` etc.) For
		``li`` element inside ``ul`` elements the name is ``ul_li`` and for
		``li`` elements inside ``ol`` elements it is ``ol_li``.

		For a ``li`` element inside an ``ol`` element :obj:`pos` specifies the
		index of the ``li`` element among its siblings (starting at 1) and
		:obj:`last` specifies the index of the last ``li`` (i.e. the total number
		of ``li``\s inside the ``ol``).

		This additional box might also specify an additional number of blank
		lines before and after its content and it might also introduce a new
		line wrapping mode and it might specify underlining (for ``h1``-``h6``
		elements.)

		Consecutive blank lines (e.g. from the bottom of the previous box and
		the top of this one), will not add up, instead the largest of the values
		will be used.
		"""
		if name is None:
			name = node.__class__.__name__
		style = self.styles.get(name, self.styles["default"])
		level = self.levels[name]
		margins = style.margins(node, name, level, pos=pos, last=last)
		self.stack.append(margins)
		if style.display == "block":
			# we flush any previous text as a block (this should handle ``<ul><li>foo<ul><li>bar</li></ul></li></ul>``)
			yield from self.flush()
			self.blockspacing = max(self.blockspacing, margins.style.top)
		self.levels[name] += 1
		prefix = margins.style.prefix
		if prefix:
			if callable(prefix):
				prefix = prefix(margins.node)
			self.texts.append(prefix)

	def pop(self):
		"""
		Remove the innermost box created by a previous :meth:`push` call. All
		text collected so far will be output taking the current margins, block
		spacing and whitespace mode into account. After the text is output the
		block spacing is reset to 0. If there's no collected text nothing will
		be output and the block spacing will not be reset.
		"""
		margins = self.stack[-1]
		suffix = margins.style.suffix
		if suffix:
			if callable(suffix):
				suffix = suffix(margins.node)
			self.texts.append(suffix)
		if margins.style.display == "block":
			yield from self.flush()
			self.blockspacing = max(self.blockspacing, margins.style.bottom)
		self.levels[margins.name] -= 1
		self.stack.pop()

	def text(self, text):
		"""
		Add the text :obj:`text` to the output. All text will be collected
		until a call to :meth:`push` or :meth:`pop` is done.
		"""
		self.texts.append(text)

	def flush(self):
		text = "".join(self.texts)

		# Find innermost block
		for margins in reversed(self.stack):
			if margins.style.display == "block":
				block = margins
				break
		else:
			block = None

		whitespace = block.style.whitespace if block else "normal"

		leftmarginwidth = self.leftmarginwidth()
		rightmarginwidth = self.rightmarginwidth()

		# Perform line wrapping
		if whitespace == "pre":
			lines = text.strip("\n").splitlines(False)
		elif whitespace == "normal":
			text = " ".join(text.strip().split()).strip()
			if text:
				if self.width is not None:
					lines = textwrap.wrap(text, max(self.width-leftmarginwidth-rightmarginwidth, 20))
				else:
					lines = [text]
			else:
				lines = []
		elif whitespace == "nowrap":
			text = " ".join(text.strip().split()).strip()
			if text:
				lines = [text]
			else:
				lines = []
		else:
			raise ValueError(f"unknown whitepace mode {whitespace!r}")

		if lines:
			for i in range(self.blockspacing):
				yield "\n"
			self.blockspacing = 0

			borderlinewidth = contentwidth = max(len(line) for line in lines)
			if self.width is not None:
				contentwidth = max(self.width-leftmarginwidth-rightmarginwidth, contentwidth)

			if block and block.style.overline:
				yield " "*leftmarginwidth + borderlinewidth*block.style.overline + "\n"

			for line in lines:
				left = "".join(next(margins.lefts) for margins in self.stack if margins.style.display == "block")
				right = "".join(next(margins.rights) for margins in self.stack if margins.style.display == "block")
				line = left + line.ljust(contentwidth) + right
				yield line.rstrip() + "\n"

			if block and block.style.underline:
				yield " "*leftmarginwidth + borderlinewidth*block.style.underline + "\n"
		self.texts = []

	def leftmarginwidth(self):
		return sum(margins.leftwidth for margins in self.stack if margins.style.display == "block")

	def rightmarginwidth(self):
		return sum(margins.rightwidth for margins in self.stack if margins.style.display == "block")

	def __iter__(self):
		lists = []

		for cursor in self.node.walk(xsc.Element | xsc.Text, enterelementnode=True, leaveelementnode=True):
			node = cursor.node
			if isinstance(node, xsc.Text):
				self.text(str(node))
			elif isinstance(node, ul):
				if cursor.event == "enterelementnode":
					lists.append(["ul", 0])
					yield from self.push(node)
				else:
					yield from self.pop()
					lists.pop()
			elif isinstance(node, ol):
				if cursor.event == "enterelementnode":
					from ll import misc
					lists.append(["ol", 0, misc.count(node[li])])
					yield from self.push(node)
				else:
					yield from self.pop()
					lists.pop()
			elif isinstance(node, li):
				if lists:
					if cursor.event == "enterelementnode":
						lists[-1][1] += 1
						if lists[-1][0] == "ol":
							yield from self.push(node, "ol_li", lists[-1][1], lists[-1][2])
						elif lists[-1][0] == "ul":
							yield from self.push(node, "ul_li")
						else:
							yield from self.push(node)
					else:
						yield from self.pop()
			elif isinstance(node, dl):
				if cursor.event == "enterelementnode":
					lists.append(["dl", 0])
					yield from self.push(node)
				else:
					yield from self.pop()
					lists.pop()
			elif isinstance(node, xsc.Element) and node.xmlname in self.styles:
				if cursor.event == "enterelementnode":
					yield from self.push(node)
				else:
					yield from self.pop()
			elif isinstance(node, script):
				cursor.entercontent = False
		yield from self.flush()


def astext(
	node,
	width=None,
	default=dict(display="inline"),
	h1=dict(display="block", top=2, bottom=1, whitespace="nowrap", overline="=", underline="="),
	h2=dict(display="block", top=2, bottom=1, whitespace="nowrap", underline="-"),
	h3=dict(display="block", top=2, bottom=1, whitespace="nowrap", underline='"'),
	h4=dict(display="block", top=2, bottom=1, whitespace="nowrap", underline="'"),
	h5=dict(display="block", top=2, bottom=1, whitespace="nowrap", underline="'"),
	h6=dict(display="block", top=2, bottom=1, whitespace="nowrap", underline="'"),
	dl=dict(display="block", top=1, bottom=1),
	dt=dict(display="block", top=1),
	dd=dict(display="block", bottom=1, left="   "),
	ol=dict(display="block", top=1, bottom=1),
	ol_li=dict(display="block", top=1, bottom=1, left="{pos:{width}}. \n"),
	ul=dict(display="block", top=1, bottom=1),
	ul_li=dict(display="block", top=1, bottom=1, left=("*  \n", "-  \n")),
	li=dict(display="block", top=1, bottom=1),
	pre=dict(display="block", top=1, bottom=1, left="   ", whitespace="pre"),
	blockquote=dict(display="block", top=1, bottom=1, left="   "),
	div=dict(display="block", bottom=1),
	p=dict(display="block", bottom=1),
	hr=dict(display="block", bottom=1),
	address=dict(display="block", bottom=1),
	th=dict(display="block", bottom=1),
	td=dict(display="block", bottom=1),
	b=dict(display="inline", prefix="*", suffix="*"),
	em=dict(display="inline", prefix="*", suffix="*"),
	strong=dict(display="inline", prefix="**", suffix="**"),
	i=dict(display="inline", prefix="*", suffix="*"),
	u=dict(display="inline", prefix="_", suffix="_"),
	code=dict(display="inline", prefix="``", suffix="``"),
	**kwargs
	):
	r"""
	Return the node :obj:`node` formatted as plain text. :obj:`node` must contain
	an HTML tree.

	:obj:`width` is the maximum line length. If :obj:`width` is :const:`None`
	line length is unlimited (i.e. no line wrapping will be done).

	The rest of the parameters specify the formatting styles for HTML elements.
	The parameter names are the names of the HTML elements, except for ``ol_li``
	which is used for ``li`` elements inside ``ol`` elements and ``ul_li`` which
	is used for ``li`` elements inside ``ul`` elements. ``default`` is used if
	the parameter for the HTML element is not passed.

	The parameter value must be a dictionary which might contain any of the
	following keys (if the key is missing a default value is used):

	``display``
		This is either ``"block"`` for a block level element or ``"inline"`` for
		an inline element.

	``prefix``
		A string that should be output before any of the content of the block.

	``suffix``
		A string that should be output after any of the content of the block.

	The following keys will only be used for ``display == "block"``:

	``top``
		The minimum number of empty lines before the block. (The default is ``0``)

	``bottom``
		The minimum number of empty lines after the block. (The default is ``0``)

	``left``
		The left margin for the block. This margin can be different for different
		nesting levels (e. g. different "bullets" can be used for nested
		``ul``\s). If the value is a string it will be used as the indentation on
		the left side for all levels, otherwise it must be a list of strings.
		If the nesting of this element is deeper than the list, the last item in
		the list will be used.

		If a margin contains multiple lines, the first indentation line will be
		used for the first content line, the second indentation line for the
		second content line etc. If the content has more lines than the
		indentation the last indentation line will be repeated. All indentation
		lines will be padded to the longest line. For example the indentation for
		a ``li`` element inside an ``ul`` element on level 1 is ``"*  \n"``, i.e.
		the first line will be indented with ``"*  "``, all subsequent lines with
		three spaces.

	``right``
		The right margin for the block. This supports the same semantics regarding
		levels and multiple lines as the ``left`` argument.

	``whitespace``
		Specifies how lines in the block should be wrapped. ``"normal"`` collapses
		consecutive whitespace and wraps the lines at the specified width.
		``"nowrap"`` collapses consecutive whitespace but doesn't wrap and
		``"pre"`` uses the lines as given.

	``overline``
		A character that is repeated for the width of the content as a rule before
		the content. If ``None`` is used, no rule will be output. (Note that this
		will only work on the innermost block level element.)

	``underline``
		A rule after the content of the block. (Note that this will only work on
		the innermost block level element.)
	"""
	kwargs = {
		"width": width,
		"default": default,
		"h1": h1,
		"h2": h2,
		"h3": h3,
		"h4": h4,
		"h5": h5,
		"h6": h6,
		"dl": dl,
		"dt": dt,
		"dd": dd,
		"ol": ol,
		"ol_li": ol_li,
		"ul": ul,
		"ul_li": ul_li,
		"li": li,
		"pre": pre,
		"blockquote": blockquote,
		"div": div,
		"p": p,
		"hr": hr,
		"address": address,
		"th": th,
		"td": td,
		"b": b,
		"em": em,
		"strong": strong,
		"i": i,
		"u": u,
		"code": code,
		**kwargs	
	}
	formatter = _PlainTextFormatter(node, **kwargs)
	return "".join(formatter).strip("\n")
