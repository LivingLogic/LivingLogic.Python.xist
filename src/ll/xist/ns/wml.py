# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST namespace module that contains definitions for all the elements in
WML 1.3.
"""


from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://www.wapforum.org/DTD/wml13.dtd"


class coreattrs(xsc.Attrs):
	class id(xsc.TextAttr): pass
	class class_(xsc.TextAttr): xmlname = "class"


class cardevattrs(xsc.Attrs):
	class onenterforward(xsc.URLAttr): pass
	class onenterbackward(xsc.URLAttr): pass
	class ontimer(xsc.URLAttr): pass


class allattrs(coreattrs, cardevattrs):
	pass


class DocTypeWML13(xsc.DocType):
	"""
	document type for WML 1.3
	"""

	def __init__(self):
		xsc.DocType.__init__(self, 'wml PUBLIC "-//WAPFORUM//DTD WML 1.3 //EN" "http://www.wapforum.org/DTD/wml13.dtd"')


# The global structure of an WML document
class wml(xsc.Element):
	"""
	creates a WML deck consisting of one or more cards
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class card(xsc.Element):
	"""
	Defines and names a new card
	"""
	xmlns = xmlns
	class Attrs(allattrs):
		class title(xsc.TextAttr): pass
		class newcontext(xsc.TextAttr): pass
		class ordered(xsc.TextAttr): pass


class do(xsc.Element):
	"""
	Mechanism used to allow user actions within a card
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class type(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class optional(xsc.BoolAttr): pass


class onevent(xsc.Element):
	"""
	Specifies an action to be performed when specific events occur
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class type(xsc.TextAttr): pass


class head(xsc.Element):
	"""
	Provides information for an entire deck
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class template(xsc.Element):
	"""
	Specifies a template containing settings that will be used deck wide
	"""
	xmlns = xmlns
	class Attrs(allattrs):
		pass


class access(xsc.Element):
	"""
	Applies access-control rules to a deck effectively restricting referred access
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class domain(xsc.TextAttr): pass
		class path(xsc.TextAttr): pass


class meta(xsc.Element):
	"""
	Specifies deck-specific meta information within a :class:`head` block
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class http_equiv(xsc.TextAttr): xmlname = "http-equiv"
		class name(xsc.TextAttr): pass
		class forua(xsc.TextAttr): pass
		class content(xsc.TextAttr): pass
		class scheme(xsc.TextAttr): pass


class go(xsc.Element):
	"""
	Opens a specified URL using GET or POST methods
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class href(xsc.URLAttr): pass
		class sendreferer(xsc.TextAttr): pass
		class method(xsc.TextAttr): pass
		class enctype(xsc.TextAttr): pass
		class cache_control(xsc.TextAttr): xmlname = "cache-control"
		class accept_charset(xsc.TextAttr): xmlname = "accept-charset"


class prev(xsc.Element):
	"""
	Returns to the previous card
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class refresh(xsc.Element):
	"""
	Refreshes (or resets) variables to initial or updated values
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class noop(xsc.Element):
	"""
	Does nothing (as in no operation)
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class postfield(xsc.Element):
	"""
	Specifies a field and value to be sent to a URL
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass


class setvar(xsc.Element):
	"""
	Sets a variable to a specified value
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass


class select(xsc.Element):
	"""
	Displays a list of options for user selection
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass
		class iname(xsc.TextAttr): pass
		class ivalue(xsc.TextAttr): pass
		class multiple(xsc.TextAttr): pass
		class tabindex(xsc.IntAttr): pass


class optgroup(xsc.Element):
	"""
	Groups options together so that the browser can optimize the display
	appropriately
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass


class option(xsc.Element):
	"""
	Creates options within a :class:`select` list
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class value(xsc.TextAttr): pass
		class title(xsc.TextAttr): pass
		class onpick(xsc.URLAttr): pass


class input(xsc.Element):
	"""
	Prompts for user input which will be saved to a variable
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class name(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class emptyok(xsc.TextAttr): pass
		class size(xsc.IntAttr): pass
		class maxlength(xsc.IntAttr): pass
		class tabindex(xsc.IntAttr): pass
		class title(xsc.TextAttr): pass
		class accesskey(xsc.TextAttr): pass


class fieldset(xsc.Element):
	"""
	Groups input field together so that the browser can optimize the display
	appropriately
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass


class timer(xsc.Element):
	"""
	Invokes a timer after a specified amount of inactivity
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass


class img(xsc.Element):
	"""
	Displays an image in the browser
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class alt(xsc.TextAttr): pass
		class src(xsc.URLAttr): pass
		class localsrc(xsc.TextAttr): pass
		class vspace(xsc.TextAttr): pass
		class hspace(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class height(xsc.TextAttr): pass
		class width(xsc.TextAttr): pass


class anchor(xsc.Element):
	"""
	Creates an anchor (also called a link) associated with :class:`go`,
	:class:`prev` or :class:`refresh` tasks.
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass
		class accesskey(xsc.TextAttr): pass


class a(xsc.Element):
	"""
	Creates an anchor (also called a link)
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class href(xsc.URLAttr): pass
		class title(xsc.TextAttr): pass
		class accesskey(xsc.TextAttr): pass


class table(xsc.Element):
	"""
	Creates a columnar table providing control over table alignment
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class columns(xsc.IntAttr): pass


class tr(xsc.Element):
	"""
	Creates rows within a table
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class td(xsc.Element):
	"""
	Creates cells within table rows
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class em(xsc.Element):
	"""
	Displays all text between ``<em>`` and ``</em>`` formatted with emphasis
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class strong(xsc.Element):
	"""
	Displays all text between ``<strong>`` and ``</strong>`` formatted with
	strong emphasis
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class b(xsc.Element):
	"""
	Displays all text between ``<b>`` and ``</b>`` in bold text
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class i(xsc.Element):
	"""
	``Displays all text between ``<i>`` and ``</i>`` in italic text
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class u(xsc.Element):
	"""
	Displays all text between ``<u>`` and ``</u>`` as underlined text
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class big(xsc.Element):
	"""
	Displays all text between ``<big>`` and ``</big>`` in a large font
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class small(xsc.Element):
	"""
	Displays all text between ``<small>`` and ``</small>`` in a small font
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


class p(xsc.Element):
	"""
	Creates a paragraph, establishing alignment and wrapping for all text
	within it
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class align(xsc.TextAttr): pass
		class mode(xsc.TextAttr): pass


class br(xsc.Element):
	"""
	Forces a line break
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		class type(xsc.TextAttr): pass


class pre(xsc.Element):
	"""
	Preformatted text
	"""
	xmlns = xmlns
	class Attrs(coreattrs):
		pass


head.model = sims.Elements(access, meta)
template.model = sims.Elements(do, onevent)
do.model = \
onevent.model = sims.Elements(go, prev, noop, refresh)
wml.model = sims.Elements(head, card, template)
optgroup.model = \
select.model = sims.Elements(optgroup, option)
go.model = sims.Elements(postfield, setvar)
card.model = sims.Elements(pre, do, timer, onevent, p)
prev.model = \
refresh.model = sims.Elements(setvar)
tr.model = sims.Elements(td)
table.model = sims.Elements(tr)
pre.model = sims.ElementsOrText(a, do, b, i, u, br, input, em, strong, anchor, select)
anchor.model = sims.ElementsOrText(br, img, go, prev, refresh)
td.model = sims.ElementsOrText(em, a, b, img, i, big, u, br, small, strong, anchor)
b.model = \
big.model = \
em.model = \
i.model = \
small.model = \
strong.model = \
u.model = sims.ElementsOrText(em, a, b, img, i, big, u, br, small, table, strong, anchor)
fieldset.model = \
p.model = sims.ElementsOrText(em, a, do, b, fieldset, img, i, big, u, br, input, small, table, strong, anchor, select)
a.model = sims.ElementsOrText(img, br)
option.model = sims.ElementsOrText(onevent)
access.model = \
br.model = \
img.model = \
input.model = \
meta.model = \
noop.model = \
postfield.model = \
setvar.model = \
timer.model = sims.Empty()
