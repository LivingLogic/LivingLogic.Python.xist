#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
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
A XSC module that contains definitions for all the elements in WML 1.3
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import string
import xsc

# common attributes
coreattrs  = {"id": xsc.TextAttr, "class": xsc.TextAttr}
cardev  = {"onenterforward": xsc.URLAttr, "onenterbackward": xsc.URLAttr, "ontimer": xsc.URLAttr}
attrs = coreattrs.copy()
attrs.update(cardev)

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
	empty = 0
	attrHandlers = coreattrs.copy()

class card(xsc.Element):
	"""
	defines and names a new card
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"title": xsc.TextAttr, "newcontext": xsc.TextAttr, "ordered": xsc.TextAttr}) 

class do(xsc.Element):
	"""
	mechanism used to allow user actions within a card
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"type": xsc.TextAttr, "label": xsc.TextAttr, "name": xsc.TextAttr, "optional": xsc.BoolAttr}) 

class onevent(xsc.Element):
	"""
	specifies an action to be performed when specific events occur
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"type": xsc.TextAttr}) 

class head(xsc.Element):
	"""
	provides information for an entire deck
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class template(xsc.Element):
	"""
	specifies a template containing settings that will be used deck wide
	"""
	empty = 0
	attrHandlers = attrs.copy()

class access(xsc.Element):
	"""
	applies access-control rules to a deck effectively restricting referred access
	"""
	empty = 1
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"domain": xsc.TextAttr, "path": xsc.TextAttr}) 

class meta(xsc.Element):
	"""
	specifies deck-specific meta information within a <head> block
	"""
	empty = 1
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"http-equiv": xsc.TextAttr, "name": xsc.TextAttr, "forua": xsc.TextAttr, "content": xsc.TextAttr, "scheme": xsc.TextAttr}) 

class go(xsc.Element):
	"""
	opens a specified URL using GET or POST methods
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"href": xsc.URLAttr, "sendreferer": xsc.TextAttr, "method": xsc.TextAttr, "enctype": xsc.TextAttr, "cache-control": xsc.TextAttr, "accept-charset": xsc.TextAttr}) 

class prev(xsc.Element):
	"""
	returns to the previous card
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class refresh(xsc.Element):
	"""
	refreshes (or resets) variables to initial or updated values
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class noop(xsc.Element):
	"""
	does nothing (as in no operation)
	"""
	empty = 1
	attrHandlers = coreattrs.copy()

class postfield(xsc.Element):
	"""
	specifies a field and value to be sent to a URL
	"""
	empty = 1
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"name": xsc.TextAttr, "value": xsc.TextAttr}) 

class setvar(xsc.Element):
	"""
	sets a variable to a specified value
	"""
	empty = 1
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"name": xsc.TextAttr, "value": xsc.TextAttr}) 

class select(xsc.Element):
	"""
	displays a list of options for user selection
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"title": xsc.TextAttr, "name": xsc.TextAttr, "value": xsc.TextAttr, "iname": xsc.TextAttr, "ivalue": xsc.TextAttr, "multiple": xsc.TextAttr, "tabindex": xsc.IntAttr}) 

class optgroup(xsc.Element):
	"""
	groups options together so that the browser can optimize the display appropriately
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"title": xsc.TextAttr}) 

class option(xsc.Element):
	"""
	creates options within a <select> list
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"value": xsc.TextAttr, "title": xsc.TextAttr, "onpick": xsc.URLAttr}) 

class input(xsc.Element):
	"""
	prompts for user input which will be saved to a variable
	"""
	empty = 1
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"name": xsc.TextAttr, "type": xsc.TextAttr, "value": xsc.TextAttr, "format": xsc.TextAttr, "emptyok": xsc.TextAttr, "size": xsc.IntAttr, "maxlength": xsc.IntAttr, "tabindex": xsc.IntAttr, "title": xsc.TextAttr, "accesskey": xsc.TextAttr}) 

class fieldset(xsc.Element):
	"""
	groups input field together so that the browser can optimize the display appropriately
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"title": xsc.TextAttr}) 

class timer(xsc.Element):
	"""
	invokes a timer after a specified amount of inactivity
	"""
	empty = 1
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"name": xsc.TextAttr, "value": xsc.TextAttr}) 

class img(xsc.Element):
	"""
	displays an image in the browser
	"""
	empty = 1
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"alt": xsc.TextAttr, "src": xsc.URLAttr, "localsrc": xsc.TextAttr, "vspace": xsc.TextAttr, "hspace": xsc.TextAttr, "align": xsc.TextAttr, "height": xsc.TextAttr, "width": xsc.TextAttr}) 

class anchor(xsc.Element):
	"""
	creates an anchor (also called a link) associated with <go>, <prev> or <refresh> tasks
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"title": xsc.TextAttr, "accesskey": xsc.TextAttr}) 

class a(xsc.Element):
	"""
	creates an anchor (also called a link)
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"href": xsc.URLAttr, "title": xsc.TextAttr, "accesskey": xsc.TextAttr}) 

class table(xsc.Element):
	"""
	creates a columnar table providing control over table alignment
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"title": xsc.TextAttr, "align": xsc.TextAttr, "columns": xsc.IntAttr}) 

class tr(xsc.Element):
	"""
	creates rows within a table
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class td(xsc.Element):
	"""
	creates cells within table rows
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class em(xsc.Element):
	"""
	displays all text between <em> and </em> formatted with emphasis
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class strong(xsc.Element):
	"""
	displays all text between <strong> and </strong> formatted with strong emphasis
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class b(xsc.Element):
	"""
	displays all text between <b> and </b> in bold text
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class i(xsc.Element):
	"""
	displays all text between <i> and </i> in italic text
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class u(xsc.Element):
	"""
	displays all text between <u> and </u> as underlined text
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class big(xsc.Element):
	"""
	displays all text between <big> and </big> in a large font
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class small(xsc.Element):
	"""
	displays all text between <small> and </small> in a small font
	"""
	empty = 0
	attrHandlers = coreattrs.copy()

class p(xsc.Element):
	"""
	creates a paragraph, establishing alignment and wrapping for all text within it
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"align": xsc.TextAttr, "mode": xsc.TextAttr})

class br(xsc.Element):
	"""
	forces a line break
	"""
	empty = 1
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"type": xsc.TextAttr})

class pre(xsc.Element):
	"""
	preformatted text
	"""
	empty = 0
	attrHandlers = coreattrs.copy()


# Entities in DTD
class nbsp(xsc.Entity): "no-break space = non-breaking space, U+00A0 ISOnum"; codepoint = 160
class shy(xsc.Entity): "soft hyphen = discretionary hyphen, U+00AD ISOnum"; codepoint = 173

# register all the classes we've defined so far
namespace = xsc.Namespace("wml", "http://www.wapforum.org/DTD/wml13.dtd", vars())
