#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; namespace module that contains definitions for all the elements in &wml; 1.3.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import string

from ll.xist import xsc, sims


class coreattrs(xsc.Element.Attrs):
	class id(xsc.TextAttr): pass
	class class_(xsc.TextAttr): xmlname = "class"


class cardevattrs(xsc.Element.Attrs):
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
	class Attrs(coreattrs):
		pass


class card(xsc.Element):
	"""
	defines and names a new card
	"""
	class Attrs(allattrs):
		class title(xsc.TextAttr): pass
		class newcontext(xsc.TextAttr): pass
		class ordered(xsc.TextAttr): pass


class do(xsc.Element):
	"""
	mechanism used to allow user actions within a card
	"""
	class Attrs(coreattrs):
		class type(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class optional(xsc.BoolAttr): pass


class onevent(xsc.Element):
	"""
	specifies an action to be performed when specific events occur
	"""
	class Attrs(coreattrs):
		class type(xsc.TextAttr): pass


class head(xsc.Element):
	"""
	provides information for an entire deck
	"""
	class Attrs(coreattrs):
		pass


class template(xsc.Element):
	"""
	specifies a template containing settings that will be used deck wide
	"""
	class Attrs(allattrs):
		pass


class access(xsc.Element):
	"""
	applies access-control rules to a deck effectively restricting referred access
	"""
	class Attrs(coreattrs):
		class domain(xsc.TextAttr): pass
		class path(xsc.TextAttr): pass


class meta(xsc.Element):
	"""
	specifies deck-specific meta information within a <pyref class="head"><class>head</class></pyref> block
	"""
	class Attrs(coreattrs):
		class http_equiv(xsc.TextAttr): xmlname = "http-equiv"
		class name(xsc.TextAttr): pass
		class forua(xsc.TextAttr): pass
		class content(xsc.TextAttr): pass
		class scheme(xsc.TextAttr): pass


class go(xsc.Element):
	"""
	opens a specified URL using GET or POST methods
	"""
	class Attrs(coreattrs):
		class href(xsc.URLAttr): pass
		class sendreferer(xsc.TextAttr): pass
		class method(xsc.TextAttr): pass
		class enctype(xsc.TextAttr): pass
		class cache_control(xsc.TextAttr): xmlname = "cache-control"
		class accept_charset(xsc.TextAttr): xmlname = "accept-charset"


class prev(xsc.Element):
	"""
	returns to the previous card
	"""
	class Attrs(coreattrs):
		pass


class refresh(xsc.Element):
	"""
	refreshes (or resets) variables to initial or updated values
	"""
	class Attrs(coreattrs):
		pass


class noop(xsc.Element):
	"""
	does nothing (as in no operation)
	"""
	class Attrs(coreattrs):
		pass


class postfield(xsc.Element):
	"""
	specifies a field and value to be sent to a URL
	"""
	class Attrs(coreattrs):
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass


class setvar(xsc.Element):
	"""
	sets a variable to a specified value
	"""
	class Attrs(coreattrs):
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass


class select(xsc.Element):
	"""
	displays a list of options for user selection
	"""
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
	groups options together so that the browser can optimize the display appropriately
	"""
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass


class option(xsc.Element):
	"""
	creates options within a <pyref class="select"><class>select</class></pyref> list
	"""
	class Attrs(coreattrs):
		class value(xsc.TextAttr): pass
		class title(xsc.TextAttr): pass
		class onpick(xsc.URLAttr): pass


class input(xsc.Element):
	"""
	prompts for user input which will be saved to a variable
	"""
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
	groups input field together so that the browser can optimize the display appropriately
	"""
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass


class timer(xsc.Element):
	"""
	invokes a timer after a specified amount of inactivity
	"""
	class Attrs(coreattrs):
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass


class img(xsc.Element):
	"""
	displays an image in the browser
	"""
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
	creates an anchor (also called a link) associated with <pyref class="go"><class>go</class></pyref>,
	<pyref class="prev"><class>prev</class></pyref> or <pyref class="refresh"><class>refresh</class></pyref> tasks.
	"""
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass
		class accesskey(xsc.TextAttr): pass


class a(xsc.Element):
	"""
	creates an anchor (also called a link)
	"""
	class Attrs(coreattrs):
		class href(xsc.URLAttr): pass
		class title(xsc.TextAttr): pass
		class accesskey(xsc.TextAttr): pass


class table(xsc.Element):
	"""
	creates a columnar table providing control over table alignment
	"""
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class columns(xsc.IntAttr): pass


class tr(xsc.Element):
	"""
	creates rows within a table
	"""
	class Attrs(coreattrs):
		pass


class td(xsc.Element):
	"""
	creates cells within table rows
	"""
	class Attrs(coreattrs):
		pass


class em(xsc.Element):
	"""
	displays all text between <markup>&lt;em&gt;</markup> and <markup>&lt;/em&gt;</markup> formatted with emphasis
	"""
	class Attrs(coreattrs):
		pass


class strong(xsc.Element):
	"""
	displays all text between <markup>&lt;strong&gt;</markup> and <markup>&lt;/strong&gt;</markup> formatted with strong emphasis
	"""
	class Attrs(coreattrs):
		pass


class b(xsc.Element):
	"""
	displays all text between <markup>&lt;b&gt;</markup> and <markup>&lt;/b&gt;</markup> in bold text
	"""
	class Attrs(coreattrs):
		pass


class i(xsc.Element):
	"""
	displays all text between <markup>&lt;i&gt;</markup> and <markup>&lt;/i&gt;</markup> in italic text
	"""
	class Attrs(coreattrs):
		pass


class u(xsc.Element):
	"""
	displays all text between <markup>&lt;u&gt;</markup> and <markup>&lt;/u&gt;</markup> as underlined text
	"""
	class Attrs(coreattrs):
		pass


class big(xsc.Element):
	"""
	displays all text between <markup>&lt;big&gt;</markup> and <markup>&lt;/big&gt;</markup> in a large font
	"""
	class Attrs(coreattrs):
		pass


class small(xsc.Element):
	"""
	displays all text between <markup>&lt;small&gt;</markup> and <markup>&lt;/small&gt;</markup> in a small font
	"""
	class Attrs(coreattrs):
		pass


class p(xsc.Element):
	"""
	creates a paragraph, establishing alignment and wrapping for all text within it
	"""
	class Attrs(coreattrs):
		class align(xsc.TextAttr): pass
		class mode(xsc.TextAttr): pass


class br(xsc.Element):
	"""
	forces a line break
	"""
	class Attrs(coreattrs):
		class type(xsc.TextAttr): pass


class pre(xsc.Element):
	"""
	preformatted text
	"""
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


class xmlns(xsc.Namespace):
	xmlname = "wml"
	xmlurl = "http://www.wapforum.org/DTD/wml13.dtd"
xmlns.makemod(vars())
