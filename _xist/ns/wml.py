#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
<par>An &xist; namespace module that contains definitions for all the elements in &wml; 1.3.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import string

from ll.xist import xsc

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
	empty = False
	class Attrs(coreattrs):
		pass

class card(xsc.Element):
	"""
	defines and names a new card
	"""
	empty = False
	class Attrs(allattrs):
		class title(xsc.TextAttr): pass
		class newcontext(xsc.TextAttr): pass
		class ordered(xsc.TextAttr): pass

class do(xsc.Element):
	"""
	mechanism used to allow user actions within a card
	"""
	empty = False
	class Attrs(coreattrs):
		class type(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class optional(xsc.BoolAttr): pass

class onevent(xsc.Element):
	"""
	specifies an action to be performed when specific events occur
	"""
	empty = False
	class Attrs(coreattrs):
		class type(xsc.TextAttr): pass

class head(xsc.Element):
	"""
	provides information for an entire deck
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class template(xsc.Element):
	"""
	specifies a template containing settings that will be used deck wide
	"""
	empty = False
	class Attrs(allattrs):
		pass

class access(xsc.Element):
	"""
	applies access-control rules to a deck effectively restricting referred access
	"""
	empty = True
	class Attrs(coreattrs):
		class domain(xsc.TextAttr): pass
		class path(xsc.TextAttr): pass

class meta(xsc.Element):
	"""
	specifies deck-specific meta information within a <pyref class="head"><class>head</class></pyref> block
	"""
	empty = True
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
	empty = False
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
	empty = False
	class Attrs(coreattrs):
		pass

class refresh(xsc.Element):
	"""
	refreshes (or resets) variables to initial or updated values
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class noop(xsc.Element):
	"""
	does nothing (as in no operation)
	"""
	empty = True
	class Attrs(coreattrs):
		pass

class postfield(xsc.Element):
	"""
	specifies a field and value to be sent to a URL
	"""
	empty = True
	class Attrs(coreattrs):
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class setvar(xsc.Element):
	"""
	sets a variable to a specified value
	"""
	empty = True
	class Attrs(coreattrs):
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class select(xsc.Element):
	"""
	displays a list of options for user selection
	"""
	empty = False
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
	empty = False
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass

class option(xsc.Element):
	"""
	creates options within a <pyref class="select"><class>select</class></pyref> list
	"""
	empty = False
	class Attrs(coreattrs):
		class value(xsc.TextAttr): pass
		class title(xsc.TextAttr): pass
		class onpick(xsc.URLAttr): pass

class input(xsc.Element):
	"""
	prompts for user input which will be saved to a variable
	"""
	empty = True
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
	empty = False
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass

class timer(xsc.Element):
	"""
	invokes a timer after a specified amount of inactivity
	"""
	empty = True
	class Attrs(coreattrs):
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class img(xsc.Element):
	"""
	displays an image in the browser
	"""
	empty = True
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
	empty = False
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass
		class accesskey(xsc.TextAttr): pass

class a(xsc.Element):
	"""
	creates an anchor (also called a link)
	"""
	empty = False
	class Attrs(coreattrs):
		class href(xsc.URLAttr): pass
		class title(xsc.TextAttr): pass
		class accesskey(xsc.TextAttr): pass

class table(xsc.Element):
	"""
	creates a columnar table providing control over table alignment
	"""
	empty = False
	class Attrs(coreattrs):
		class title(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class columns(xsc.IntAttr): pass

class tr(xsc.Element):
	"""
	creates rows within a table
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class td(xsc.Element):
	"""
	creates cells within table rows
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class em(xsc.Element):
	"""
	displays all text between <markup>&lt;em&gt;</markup> and <markup>&lt;/em&gt;</markup> formatted with emphasis
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class strong(xsc.Element):
	"""
	displays all text between <markup>&lt;strong&gt;</markup> and <markup>&lt;/strong&gt;</markup> formatted with strong emphasis
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class b(xsc.Element):
	"""
	displays all text between <markup>&lt;b&gt;</markup> and <markup>&lt;/b&gt;</markup> in bold text
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class i(xsc.Element):
	"""
	displays all text between <markup>&lt;i&gt;</markup> and <markup>&lt;/i&gt;</markup> in italic text
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class u(xsc.Element):
	"""
	displays all text between <markup>&lt;u&gt;</markup> and <markup>&lt;/u&gt;</markup> as underlined text
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class big(xsc.Element):
	"""
	displays all text between <markup>&lt;big&gt;</markup> and <markup>&lt;/big&gt;</markup> in a large font
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class small(xsc.Element):
	"""
	displays all text between <markup>&lt;small&gt;</markup> and <markup>&lt;/small&gt;</markup> in a small font
	"""
	empty = False
	class Attrs(coreattrs):
		pass

class p(xsc.Element):
	"""
	creates a paragraph, establishing alignment and wrapping for all text within it
	"""
	empty = False
	class Attrs(coreattrs):
		class align(xsc.TextAttr): pass
		class mode(xsc.TextAttr): pass

class br(xsc.Element):
	"""
	forces a line break
	"""
	empty = True
	class Attrs(coreattrs):
		class type(xsc.TextAttr): pass

class pre(xsc.Element):
	"""
	preformatted text
	"""
	empty = False
	class Attrs(coreattrs):
		pass

# Entities in DTD
class nbsp(xsc.CharRef): "no-break space = non-breaking space, U+00A0 ISOnum"; codepoint = 160
class shy(xsc.CharRef): "soft hyphen = discretionary hyphen, U+00AD ISOnum"; codepoint = 173

# register all the classes we've defined so far
xmlns = xsc.Namespace("wml", "http://www.wapforum.org/DTD/wml13.dtd", vars())
