#! /usr/bin/env python

"""
A XSC module that contains definitions for all the elements in HTML 4.0 transitional
(and a few additional ones).
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import string
import xsc

# common attributes
coreattrs  = {"id": xsc.TextAttr, "class": xsc.TextAttr, "style": xsc.TextAttr, "title": xsc.TextAttr}
i18n = {"lang": xsc.TextAttr, "dir": xsc.TextAttr}
events = {"onclick": xsc.TextAttr, "ondblclick": xsc.TextAttr, "onmousedown": xsc.TextAttr, "onmouseup": xsc.TextAttr, "onmouseover": xsc.TextAttr, "onmousemove": xsc.TextAttr, "onmouseout": xsc.TextAttr, "onkeypress": xsc.TextAttr, "onkeydown": xsc.TextAttr, "onkeyup": xsc.TextAttr}
attrs = coreattrs.copy()
attrs.update(i18n)
attrs.update(events)
cellhalign = {"align": xsc.TextAttr, "char": xsc.TextAttr, "charoff": xsc.TextAttr}
cellvalign = {"valign": xsc.TextAttr}

class DocTypeHTML401transitional(xsc.DocType):
	"""
	document type for HTML 4.0 transitional
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"')

class DocTypeXHTML10strict(xsc.DocType):
	"""
	document type for XHTML 1.0 strict
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"')

class DocTypeXHTML10transitional(xsc.DocType):
	"""
	document type for XHTML 1.0 strict
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"')

# The global structure of an HTML document
class html(xsc.Element):
	"""
	document root element
	"""
	empty = 0
	attrHandlers = i18n.copy()
	attrHandlers.update({"xmlns": xsc.TextAttr})

class head(xsc.Element):
	"""
	document head
	"""
	empty = 0
	attrHandlers = i18n.copy()
	attrHandlers.update({"profile": xsc.TextAttr})

class title(xsc.Element):
	"""
	document title
	"""
	empty = 0
	attrHandlers = i18n

	def asHTML(self, mode=None):
		return title(self.content.asHTML(mode=None).asPlainString(), **self.attrs)

class meta(xsc.Element):
	"""
	generic metainformation
	"""
	empty = 1
	attrHandlers = i18n.copy()
	attrHandlers.update({"http_equiv": xsc.TextAttr, "http-equiv": xsc.TextAttr, "name": xsc.TextAttr, "content": xsc.TextAttr, "scheme": xsc.TextAttr})

	def __init__(self, *_content, **_attrs):
		# we have two names for one and the same attribute http_equiv and http-equiv
		xsc.Element.__init__(self, *_content, **_attrs)
		if self.hasAttr("http_equiv"):
			if not self.hasAttr("http-equiv"):
				self["http-equiv"] = self["http_equiv"]
			del self["http_equiv"]

	def publish(self, publisher):
		if self.hasAttr("http-equiv"):
			ctype = self["http-equiv"].asPlainString()
			if ctype.lower() == u"content-type" and self.hasAttr("content"):
				content = self["content"].asPlainString()
				found = self.__findCharSet()
				if found is None or publisher.encoding != content[found[0]:found[1]]:
					node = meta(http_equiv="Content-Type")
					if found is None:
						node["content"] = content+u"; charset="+publisher.encoding
					else:
						node["content"] = content[:found[0]]+publisher.encoding+content[found[1]:]
					node.publish(publisher)
					return
		xsc.Element.publish(self, publisher)

	def __findCharSet(self):
		content = self["content"].asPlainString()
		startpos = content.find(u"charset")
		if startpos != -1:
			startpos = startpos+8 # skip '='
			endpos = content.find(";", startpos)
			if endpos != -1:
				return (startpos, endpos)
			else:
				return (startpos, len(content))
		return None

class body(xsc.Element):
	"""
	document body
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"onload": xsc.TextAttr, "onunload": xsc.TextAttr})
	attrHandlers.update({"background": xsc.URLAttr, "bgcolor": xsc.ColorAttr, "text": xsc.ColorAttr, "link": xsc.ColorAttr, "vlink": xsc.ColorAttr, "alink": xsc.ColorAttr, "leftmargin": xsc.TextAttr, "topmargin": xsc.TextAttr, "marginwidth": xsc.TextAttr, "marginheight": xsc.TextAttr}) # deprecated

class div(xsc.Element):
	"""
	generic language/style container
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"align": xsc.TextAttr}) # deprecated

class span(xsc.Element):
	"""
	generic language/style container
	"""
	empty = 0
	attrHandlers = attrs

class h1(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"align": xsc.TextAttr}) # deprecated

class h2(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"align": xsc.TextAttr}) # deprecated

class h3(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"align": xsc.TextAttr}) # deprecated

class h4(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"align": xsc.TextAttr}) # deprecated

class h5(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"align": xsc.TextAttr}) # deprecated

class h6(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"align": xsc.TextAttr}) # deprecated

class address(xsc.Element):
	"""
	information on author
	"""
	empty = 0
	attrHandlers = attrs

class bdo(xsc.Element):
	"""
	I18N BiDi over-ride
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update(i18n)

class tt(xsc.Element):
	"""
	teletype or monospaced text style
	"""
	empty = 0
	attrHandlers = attrs

class i(xsc.Element):
	"""
	italic text style
	"""
	empty = 0
	attrHandlers = attrs

class b(xsc.Element):
	"""
	bold text style
	"""
	empty = 0
	attrHandlers = attrs

class big(xsc.Element):
	"""
	large text style
	"""
	empty = 0
	attrHandlers = attrs

class small(xsc.Element):
	"""
	small text style
	"""
	empty = 0
	attrHandlers = attrs

class em(xsc.Element):
	"""
	Indicates emphasis.
	"""
	empty = 0
	attrHandlers = attrs

class strong(xsc.Element):
	"""
	Indicates stronger emphasis than em.
	"""
	empty = 0
	attrHandlers = attrs

class dfn(xsc.Element):
	"""
	Indicates that this is the defining instance of the enclosed term.
	"""
	empty = 0
	attrHandlers = attrs

class code(xsc.Element):
	"""
	Designates a fragment of computer code. 
	"""
	empty = 0
	attrHandlers = attrs

class samp(xsc.Element):
	"""
	Designates sample output from programs, scripts, etc. 
	"""
	empty = 0
	attrHandlers = attrs

class kbd(xsc.Element):
	"""
	Indicates text to be entered by the user.
	"""
	empty = 0
	attrHandlers = attrs

class var(xsc.Element):
	"""
	Indicates an instance of a variable or program argument. 
	"""
	empty = 0
	attrHandlers = attrs

class cite(xsc.Element):
	"""
	Contains a citation or a reference to other sources.
	"""
	empty = 0
	attrHandlers = attrs

class abbr(xsc.Element):
	"""
	Indicates an abbreviated form (e.g., WWW, HTTP, URI, Mass., etc.)
	"""
	empty = 0
	attrHandlers = attrs

class acronym(xsc.Element):
	"""
	Indicates an acronym (e.g., WAC, radar, etc.).
	"""
	empty = 0
	attrHandlers = attrs

class blockquote(xsc.Element):
	"""
	long quotation
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"cite": xsc.TextAttr})

class q(xsc.Element):
	"""
	short inline quotation
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"cite": xsc.TextAttr})

	def asPlainString(self):
		return u"«" + self.content.asPlainString() + u"»"

class sub(xsc.Element):
	"""
	subscript
	"""
	empty = 0
	attrHandlers = attrs

class sup(xsc.Element):
	"""
	superscript
	"""
	empty = 0
	attrHandlers = attrs

class p(xsc.Element):
	"""
	paragraph
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"align": xsc.TextAttr}) # deprecated

class br(xsc.Element):
	"""
	forced line break
	"""
	empty = 1
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"clear": xsc.TextAttr}) # deprecated

class pre(xsc.Element):
	"""
	preformatted text
	"""
	empty = 0
	attrHandlers = attrs

class ins(xsc.Element):
	"""
	inserted text
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"cite": xsc.TextAttr, "datetime": xsc.TextAttr})

class Del(xsc.Element):
	"""
	deleted text
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"cite": xsc.TextAttr, "datetime": xsc.TextAttr})
	name = "del" # we need a special name here

class ul(xsc.Element):
	"""
	unordered list
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"type": xsc.TextAttr}) # deprecated

class ol(xsc.Element):
	"""
	ordered list
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"type": xsc.TextAttr}) # deprecated

class li(xsc.Element):
	"""
	list item
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"type": xsc.TextAttr}) # deprecated

class dl(xsc.Element):
	"""
	definition list
	"""
	empty = 0
	attrHandlers = attrs

class dt(xsc.Element):
	"""
	definition term
	"""
	empty = 0
	attrHandlers = attrs

class dd(xsc.Element):
	"""
	definition description
	"""
	empty = 0
	attrHandlers = attrs

class table(xsc.Element):
	"""
	table
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"summary": xsc.TextAttr, "width": xsc.TextAttr, "border": xsc.TextAttr, "frame": xsc.TextAttr, "rules": xsc.TextAttr, "cellspacing": xsc.TextAttr, "cellpadding": xsc.TextAttr})
	attrHandlers.update({"height": xsc.TextAttr, "align": xsc.TextAttr, "bgcolor": xsc.ColorAttr, "background": xsc.URLAttr, "bordercolor": xsc.ColorAttr}) # deprecated

class caption(xsc.Element):
	"""
	table caption
	"""
	empty = 0
	attrHandlers = attrs

class thead(xsc.Element):
	"""
	table header
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update(cellhalign)
	attrHandlers.update(cellvalign)

class tfoot(xsc.Element):
	"""
	table footer
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update(cellhalign)
	attrHandlers.update(cellvalign)

class tbody(xsc.Element):
	"""
	table body
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update(cellhalign)
	attrHandlers.update(cellvalign)

class colgroup(xsc.Element):
	"""
	table column group
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update(cellhalign)
	attrHandlers.update(cellvalign)
	attrHandlers.update({"span": xsc.TextAttr, "width": xsc.TextAttr})

class col(xsc.Element):
	"""
	table column
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update(cellhalign)
	attrHandlers.update(cellvalign)
	attrHandlers.update({"span": xsc.TextAttr, "width": xsc.TextAttr})

class tr(xsc.Element):
	"""
	table row
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update(cellhalign)
	attrHandlers.update(cellvalign)
	attrHandlers.update({"nowrap": xsc.TextAttr, "bgcolor": xsc.ColorAttr, "width": xsc.TextAttr}) # deprecated

class th(xsc.Element):
	"""
	table header cell
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update(cellhalign)
	attrHandlers.update(cellvalign)
	attrHandlers.update({"abbr": xsc.TextAttr, "axis": xsc.TextAttr, "headers": xsc.TextAttr, "scope": xsc.TextAttr, "rowspan": xsc.TextAttr, "colspan": xsc.TextAttr})
	attrHandlers.update({"nowrap": xsc.TextAttr, "bgcolor": xsc.ColorAttr, "width": xsc.TextAttr, "height": xsc.TextAttr, "background": xsc.URLAttr}) # deprecated

class td(xsc.Element):
	"""
	table data cell
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update(cellhalign)
	attrHandlers.update(cellvalign)
	attrHandlers.update({"abbr": xsc.TextAttr, "axis": xsc.TextAttr, "headers": xsc.TextAttr, "scope": xsc.TextAttr, "rowspan": xsc.TextAttr, "colspan": xsc.TextAttr})
	attrHandlers.update({"nowrap": xsc.BoolAttr, "bgcolor": xsc.ColorAttr, "width": xsc.TextAttr, "height": xsc.TextAttr, "background": xsc.URLAttr, "bordercolor": xsc.ColorAttr}) # deprecated

class a(xsc.Element):
	"""
	anchor
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"charset": xsc.TextAttr, "type": xsc.TextAttr, "name": xsc.TextAttr, "href": xsc.URLAttr, "hreflang": xsc.TextAttr, "rel": xsc.TextAttr, "rev": xsc.TextAttr, "accesskey": xsc.TextAttr, "shape": xsc.TextAttr, "coords": xsc.TextAttr, "tabindex": xsc.TextAttr, "onfocus": xsc.TextAttr, "onblur": xsc.TextAttr})
	attrHandlers.update({"target": xsc.TextAttr}) # deprecated

class link(xsc.Element):
	"""
	a media-independent link
	"""
	empty = 1
	attrHandlers = attrs.copy()
	attrHandlers.update({"charset": xsc.TextAttr, "href": xsc.URLAttr, "hreflang": xsc.TextAttr, "type": xsc.TextAttr, "rel": xsc.TextAttr, "rev": xsc.TextAttr, "media": xsc.TextAttr})

class base(xsc.Element):
	"""
	document base URI
	"""
	empty = 1
	attrHandlers = {"href": xsc.URLAttr}
	attrHandlers.update({"target": xsc.TextAttr}) # deprecated

class img(xsc.Element):
	"""
	Embedded image
	"""
	empty = 1
	attrHandlers = attrs.copy()
	attrHandlers.update({"src": xsc.URLAttr, "alt": xsc.TextAttr, "longdesc": xsc.TextAttr, "width": xsc.TextAttr, "height": xsc.TextAttr, "usemap": xsc.TextAttr, "ismap": xsc.TextAttr})
	attrHandlers.update({"name": xsc.TextAttr, "border": xsc.TextAttr, "align": xsc.TextAttr, "hspace": xsc.TextAttr, "vspace": xsc.TextAttr, "lowsrc": xsc.URLAttr}) # deprecated

	def asPlainString(self):
		if self.hasAttr("alt"):
			return self["alt"].asPlainString()
		else:
			return u""

class object(xsc.Element):
	"""
	generic embedded object
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"declare": xsc.TextAttr, "classid": xsc.TextAttr, "codebase": xsc.TextAttr, "data": xsc.TextAttr, "type": xsc.TextAttr, "codetype": xsc.TextAttr, "archive": xsc.TextAttr, "standby": xsc.TextAttr, "height": xsc.TextAttr, "width": xsc.TextAttr, "usemap": xsc.TextAttr, "name": xsc.TextAttr, "tabindex": xsc.TextAttr})

class param(xsc.Element):
	"""
	named property value
	"""
	empty = 1
	attrHandlers = {"id": xsc.TextAttr, "name": xsc.TextAttr, "value": xsc.TextAttr, "valuetype": xsc.TextAttr, "type": xsc.TextAttr}

class map(xsc.Element):
	"""
	client-side image map
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"name": xsc.TextAttr})

class area(xsc.Element):
	"""
	client-side image map area
	"""
	empty = 1
	attrHandlers = attrs.copy()
	attrHandlers.update({"shape": xsc.TextAttr, "coords": xsc.TextAttr, "href": xsc.URLAttr, "nohref": xsc.TextAttr, "alt": xsc.TextAttr, "tabindex": xsc.TextAttr, "accesskey": xsc.TextAttr, "onfocus": xsc.TextAttr, "onblur": xsc.TextAttr})

class style(xsc.Element):
	"""
	style info
	"""
	empty = 0
	attrHandlers = i18n.copy()
	attrHandlers.update({"type": xsc.TextAttr, "media": xsc.TextAttr, "title": xsc.TextAttr})

class hr(xsc.Element):
	"""
	horizontal rule
	"""
	empty = 1
	attrHandlers = coreattrs.copy()
	attrHandlers.update(events)
	attrHandlers.update({"noshade": xsc.TextAttr, "size": xsc.TextAttr, "color": xsc.ColorAttr, "width": xsc.TextAttr, "align": xsc.TextAttr}) # deprecated

# The pain, the pain ...
class frameset(xsc.Element):
	"""
	window subdivision
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"rows": xsc.TextAttr, "cols": xsc.TextAttr, "onload": xsc.TextAttr, "onunload": xsc.TextAttr})
	attrHandlers.update({"framespacing": xsc.TextAttr, "border": xsc.IntAttr, "marginwidth": xsc.IntAttr, "marginheight": xsc.IntAttr, "frameborder": xsc.IntAttr, "noresize": xsc.BoolAttr}) # deprecated

class frame(xsc.Element):
	"""
	subwindow
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"longdesc": xsc.TextAttr, "name": xsc.TextAttr, "src": xsc.URLAttr, "frameborder": xsc.TextAttr, "marginwidht": xsc.TextAttr, "marginheight": xsc.TextAttr, "noresize": xsc.BoolAttr, "scrolling": xsc.TextAttr})

class noframes(xsc.Element):
	"""
	alternate content container for non frame-based rendering
	"""
	empty = 0
	attrHandlers = attrs

class iframe(xsc.Element):
	"""
	inline subwindow
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update({"longdesc": xsc.TextAttr, "name": xsc.TextAttr, "src": xsc.URLAttr, "frameborder": xsc.TextAttr, "marginwidht": xsc.TextAttr, "marginheight": xsc.TextAttr, "noresize": xsc.BoolAttr, "scrolling": xsc.TextAttr, "align": xsc.TextAttr, "height": xsc.TextAttr, "width": xsc.TextAttr})

class form(xsc.Element):
	"""
	interactive form
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"action": xsc.URLAttr, "method": xsc.TextAttr, "enctype": xsc.TextAttr, "onsubmit": xsc.TextAttr, "onreset": xsc.TextAttr, "accept-charset": xsc.TextAttr})
	attrHandlers.update({"target": xsc.TextAttr}) # frame
	attrHandlers.update({"name": xsc.TextAttr}) # deprecated

class input(xsc.Element):
	"""
	form control
	"""
	empty = 1
	attrHandlers = attrs.copy()
	attrHandlers.update({"type": xsc.TextAttr, "name": xsc.TextAttr, "value": xsc.TextAttr, "checked": xsc.TextAttr, "disabled": xsc.TextAttr, "readonly": xsc.TextAttr, "size": xsc.TextAttr, "maxlength": xsc.TextAttr, "src": xsc.URLAttr, "alt": xsc.TextAttr, "usemap": xsc.TextAttr, "tabindex": xsc.TextAttr, "accesskey": xsc.TextAttr, "onfocus": xsc.TextAttr, "onblur": xsc.TextAttr, "onselect": xsc.TextAttr, "onchange": xsc.TextAttr, "accept": xsc.TextAttr})
	attrHandlers.update({"border": xsc.IntAttr}) # deprecated

class button(xsc.Element):
	"""
	push button
	"""
	empty = 1
	attrHandlers = attrs.copy()
	attrHandlers.update({"name": xsc.TextAttr, "value": xsc.TextAttr, "type": xsc.TextAttr, "disabled": xsc.TextAttr, "tabindex": xsc.TextAttr, "accesskey": xsc.TextAttr, "onfocus": xsc.TextAttr, "onblur": xsc.TextAttr})

class select(xsc.Element):
	"""
	option selector
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"name": xsc.TextAttr, "size": xsc.TextAttr, "multiple": xsc.TextAttr, "disabled": xsc.TextAttr, "tabindex": xsc.TextAttr, "onfocus": xsc.TextAttr, "onblur": xsc.TextAttr, "onchange": xsc.TextAttr})
	attrHandlers.update({"rows": xsc.TextAttr}) # deprecated

class optgroup(xsc.Element):
	"""
	option group
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"disabled": xsc.TextAttr, "label": xsc.TextAttr})

class option(xsc.Element):
	"""
	selectable choice
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"selected": xsc.BoolAttr, "disabled": xsc.TextAttr, "label": xsc.TextAttr, "value": xsc.TextAttr})

class textarea(xsc.Element):
	"""
	multi-line text field
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"name": xsc.TextAttr, "rows": xsc.TextAttr, "cols": xsc.TextAttr, "disabled": xsc.TextAttr, "readonly": xsc.TextAttr, "tabindex": xsc.TextAttr, "accesskey": xsc.TextAttr, "onfocus": xsc.TextAttr, "onblur": xsc.TextAttr, "onselect": xsc.TextAttr, "onchange": xsc.TextAttr})
	attrHandlers.update({"wrap": xsc.TextAttr})

class label(xsc.Element):
	"""
	form field label text
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"for": xsc.TextAttr, "accesskey": xsc.TextAttr, "onfocus": xsc.TextAttr, "onblur": xsc.TextAttr})

class fieldset(xsc.Element):
	"""
	form control group
	"""
	empty = 0
	attrHandlers = attrs

class legend(xsc.Element):
	"""
	fieldset legend
	"""
	empty = 0
	attrHandlers = attrs.copy()
	attrHandlers.update({"accesskey": xsc.TextAttr})

class script(xsc.Element):
	"""
	script statements
	"""
	empty = 0
	attrHandlers = {"charset": xsc.TextAttr, "type": xsc.TextAttr, "src": xsc.URLAttr, "defer": xsc.TextAttr}
	attrHandlers.update({"language": xsc.TextAttr}) # deprecated

class noscript(xsc.Element):
	"""
	alternate content container for non script-based rendering
	"""
	empty = 0
	attrHandlers = attrs

# More pain
class font(xsc.Element): # deprecated
	"""
	local change to font
	"""
	empty = 0
	attrHandlers = coreattrs.copy()
	attrHandlers.update(i18n)
	attrHandlers.update({"face": xsc.TextAttr, "size": xsc.TextAttr, "color": xsc.ColorAttr})

class applet(xsc.Element): # deprecated
	"""
	Java applet
	"""
	empty = 0
	attrHandlers = {"archive": xsc.URLAttr, "code": xsc.URLAttr, "width": xsc.TextAttr, "height": xsc.TextAttr}
	attrHandlers.update({"codebase": xsc.TextAttr}) # deprecated

class nobr(xsc.Element): # deprecated
	"""
	prevents line breaks
	"""
	empty = 0

class center(xsc.Element): # deprecated
	"""
	centered block level element
	"""
	empty = 0

# Latin 1 characters
class nbsp(xsc.Entity): "no-break space = non-breaking space, U+00A0 ISOnum"; codepoint = 160
class iexcl(xsc.Entity): "inverted exclamation mark, U+00A1 ISOnum"; codepoint = 161
class cent(xsc.Entity): "cent sign, U+00A2 ISOnum"; codepoint = 162
class pound(xsc.Entity): "pound sign, U+00A3 ISOnum"; codepoint = 163
class curren(xsc.Entity): "currency sign, U+00A4 ISOnum"; codepoint = 164
class yen(xsc.Entity): "yen sign = yuan sign, U+00A5 ISOnum"; codepoint = 165
class brvbar(xsc.Entity): "broken bar = broken vertical bar, U+00A6 ISOnum"; codepoint = 166
class sect(xsc.Entity): "section sign, U+00A7 ISOnum"; codepoint = 167
class uml(xsc.Entity): "diaeresis = spacing diaeresis, U+00A8 ISOdia"; codepoint = 168
class copy(xsc.Entity): "copyright sign, U+00A9 ISOnum"; codepoint = 169
class ordf(xsc.Entity): "feminine ordinal indicator, U+00AA ISOnum"; codepoint = 170
class laquo(xsc.Entity): "left-pointing double angle quotation mark = left pointing guillemet, U+00AB ISOnum"; codepoint = 171
class Not(xsc.Entity): "not sign, U+00AC ISOnum"; codepoint = 172; name = "not"
class shy(xsc.Entity): "soft hyphen = discretionary hyphen, U+00AD ISOnum"; codepoint = 173
class reg(xsc.Entity): "registered sign = registered trade mark sign, U+00AE ISOnum"; codepoint = 174
class macr(xsc.Entity): "macron = spacing macron = overline = APL overbar, U+00AF ISOdia"; codepoint = 175
class deg(xsc.Entity): "degree sign, U+00B0 ISOnum"; codepoint = 176
class plusmn(xsc.Entity): "plus-minus sign = plus-or-minus sign, U+00B1 ISOnum"; codepoint = 177
class sup2(xsc.Entity): "superscript two = superscript digit two = squared, U+00B2 ISOnum"; codepoint = 178
class sup3(xsc.Entity): "superscript three = superscript digit three = cubed, U+00B3 ISOnum"; codepoint = 179
class acute(xsc.Entity): "acute accent = spacing acute, U+00B4 ISOdia"; codepoint = 180
class micro(xsc.Entity): "micro sign, U+00B5 ISOnum"; codepoint = 181
class para(xsc.Entity): "pilcrow sign = paragraph sign, U+00B6 ISOnum"; codepoint = 182
class middot(xsc.Entity): "middle dot = Georgian comma = Greek middle dot, U+00B7 ISOnum"; codepoint = 183
class cedil(xsc.Entity): "cedilla = spacing cedilla, U+00B8 ISOdia"; codepoint = 184
class sup1(xsc.Entity): "superscript one = superscript digit one, U+00B9 ISOnum"; codepoint = 185
class ordm(xsc.Entity): "masculine ordinal indicator, U+00BA ISOnum"; codepoint = 186
class raquo(xsc.Entity): "right-pointing double angle quotation mark = right pointing guillemet, U+00BB ISOnum"; codepoint = 187
class frac14(xsc.Entity): "vulgar fraction one quarter = fraction one quarter, U+00BC ISOnum"; codepoint = 188
class frac12(xsc.Entity): "vulgar fraction one half = fraction one half, U+00BD ISOnum"; codepoint = 189
class frac34(xsc.Entity): "vulgar fraction three quarters = fraction three quarters, U+00BE ISOnum"; codepoint = 190
class iquest(xsc.Entity): "inverted question mark = turned question mark, U+00BF ISOnum"; codepoint = 191
class Agrave(xsc.Entity): "latin capital letter A with grave = latin capital letter A grave, U+00C0 ISOlat1"; codepoint = 192
class Aacute(xsc.Entity): "latin capital letter A with acute, U+00C1 ISOlat1"; codepoint = 193
class Acirc(xsc.Entity): "latin capital letter A with circumflex, U+00C2 ISOlat1"; codepoint = 194
class Atilde(xsc.Entity): "latin capital letter A with tilde, U+00C3 ISOlat1"; codepoint = 195
class Auml(xsc.Entity): "latin capital letter A with diaeresis, U+00C4 ISOlat1"; codepoint = 196
class Aring(xsc.Entity): "latin capital letter A with ring above = latin capital letter A ring, U+00C5 ISOlat1"; codepoint = 197
class AElig(xsc.Entity): "latin capital letter AE = latin capital ligature AE, U+00C6 ISOlat1"; codepoint = 198
class Ccedil(xsc.Entity): "latin capital letter C with cedilla, U+00C7 ISOlat1"; codepoint = 199
class Egrave(xsc.Entity): "latin capital letter E with grave, U+00C8 ISOlat1"; codepoint = 200
class Eacute(xsc.Entity): "latin capital letter E with acute, U+00C9 ISOlat1"; codepoint = 201
class Ecirc(xsc.Entity): "latin capital letter E with circumflex, U+00CA ISOlat1"; codepoint = 202
class Euml(xsc.Entity): "latin capital letter E with diaeresis, U+00CB ISOlat1"; codepoint = 203
class Igrave(xsc.Entity): "latin capital letter I with grave, U+00CC ISOlat1"; codepoint = 204
class Iacute(xsc.Entity): "latin capital letter I with acute, U+00CD ISOlat1"; codepoint = 205
class Icirc(xsc.Entity): "latin capital letter I with circumflex, U+00CE ISOlat1"; codepoint = 206
class Iuml(xsc.Entity): "latin capital letter I with diaeresis, U+00CF ISOlat1"; codepoint = 207
class ETH(xsc.Entity): "latin capital letter ETH, U+00D0 ISOlat1"; codepoint = 208
class Ntilde(xsc.Entity): "latin capital letter N with tilde, U+00D1 ISOlat1"; codepoint = 209
class Ograve(xsc.Entity): "latin capital letter O with grave, U+00D2 ISOlat1"; codepoint = 210
class Oacute(xsc.Entity): "latin capital letter O with acute, U+00D3 ISOlat1"; codepoint = 211
class Ocirc(xsc.Entity): "latin capital letter O with circumflex, U+00D4 ISOlat1"; codepoint = 212
class Otilde(xsc.Entity): "latin capital letter O with tilde, U+00D5 ISOlat1"; codepoint = 213
class Ouml(xsc.Entity): "latin capital letter O with diaeresis, U+00D6 ISOlat1"; codepoint = 214
class times(xsc.Entity): "multiplication sign, U+00D7 ISOnum"; codepoint = 215
class Oslash(xsc.Entity): "latin capital letter O with stroke = latin capital letter O slash, U+00D8 ISOlat1"; codepoint = 216
class Ugrave(xsc.Entity): "latin capital letter U with grave, U+00D9 ISOlat1"; codepoint = 217
class Uacute(xsc.Entity): "latin capital letter U with acute, U+00DA ISOlat1"; codepoint = 218
class Ucirc(xsc.Entity): "latin capital letter U with circumflex, U+00DB ISOlat1"; codepoint = 219
class Uuml(xsc.Entity): "latin capital letter U with diaeresis, U+00DC ISOlat1"; codepoint = 220
class Yacute(xsc.Entity): "latin capital letter Y with acute, U+00DD ISOlat1"; codepoint = 221
class THORN(xsc.Entity): "latin capital letter THORN, U+00DE ISOlat1"; codepoint = 222
class szlig(xsc.Entity): "latin small letter sharp s = ess-zed, U+00DF ISOlat1"; codepoint = 223
class agrave(xsc.Entity): "latin small letter a with grave = latin small letter a grave, U+00E0 ISOlat1"; codepoint = 224
class aacute(xsc.Entity): "latin small letter a with acute, U+00E1 ISOlat1"; codepoint = 225
class acirc(xsc.Entity): "latin small letter a with circumflex, U+00E2 ISOlat1"; codepoint = 226
class atilde(xsc.Entity): "latin small letter a with tilde, U+00E3 ISOlat1"; codepoint = 227
class auml(xsc.Entity): "latin small letter a with diaeresis, U+00E4 ISOlat1"; codepoint = 228
class aring(xsc.Entity): "latin small letter a with ring above = latin small letter a ring, U+00E5 ISOlat1"; codepoint = 229
class aelig(xsc.Entity): "latin small letter ae = latin small ligature ae, U+00E6 ISOlat1"; codepoint = 230
class ccedil(xsc.Entity): "latin small letter c with cedilla, U+00E7 ISOlat1"; codepoint = 231
class egrave(xsc.Entity): "latin small letter e with grave, U+00E8 ISOlat1"; codepoint = 232
class eacute(xsc.Entity): "latin small letter e with acute, U+00E9 ISOlat1"; codepoint = 233
class ecirc(xsc.Entity): "latin small letter e with circumflex, U+00EA ISOlat1"; codepoint = 234
class euml(xsc.Entity): "latin small letter e with diaeresis, U+00EB ISOlat1"; codepoint = 235
class igrave(xsc.Entity): "latin small letter i with grave, U+00EC ISOlat1"; codepoint = 236
class iacute(xsc.Entity): "latin small letter i with acute, U+00ED ISOlat1"; codepoint = 237
class icirc(xsc.Entity): "latin small letter i with circumflex, U+00EE ISOlat1"; codepoint = 238
class iuml(xsc.Entity): "latin small letter i with diaeresis, U+00EF ISOlat1"; codepoint = 239
class eth(xsc.Entity): "latin small letter eth, U+00F0 ISOlat1"; codepoint = 240
class ntilde(xsc.Entity): "latin small letter n with tilde, U+00F1 ISOlat1"; codepoint = 241
class ograve(xsc.Entity): "latin small letter o with grave, U+00F2 ISOlat1"; codepoint = 242
class oacute(xsc.Entity): "latin small letter o with acute, U+00F3 ISOlat1"; codepoint = 243
class ocirc(xsc.Entity): "latin small letter o with circumflex, U+00F4 ISOlat1"; codepoint = 244
class otilde(xsc.Entity): "latin small letter o with tilde, U+00F5 ISOlat1"; codepoint = 245
class ouml(xsc.Entity): "latin small letter o with diaeresis, U+00F6 ISOlat1"; codepoint = 246
class divide(xsc.Entity): "division sign, U+00F7 ISOnum"; codepoint = 247
class oslash(xsc.Entity): "latin small letter o with stroke, = latin small letter o slash, U+00F8 ISOlat1"; codepoint = 248
class ugrave(xsc.Entity): "latin small letter u with grave, U+00F9 ISOlat1"; codepoint = 249
class uacute(xsc.Entity): "latin small letter u with acute, U+00FA ISOlat1"; codepoint = 250
class ucirc(xsc.Entity): "latin small letter u with circumflex, U+00FB ISOlat1"; codepoint = 251
class uuml(xsc.Entity): "latin small letter u with diaeresis, U+00FC ISOlat1"; codepoint = 252
class yacute(xsc.Entity): "latin small letter y with acute, U+00FD ISOlat1"; codepoint = 253
class thorn(xsc.Entity): "latin small letter thorn, U+00FE ISOlat1"; codepoint = 254
class yuml(xsc.Entity): "latin small letter y with diaeresis, U+00FF ISOlat1"; codepoint = 255

# Latin Extended-A
class OElig(xsc.Entity): "latin capital ligature OE, U+0152 ISOlat2"; codepoint = 338
class oelig(xsc.Entity): "latin small ligature oe, U+0153 ISOlat2"; codepoint = 339
class Scaron(xsc.Entity): "latin capital letter S with caron, U+0160 ISOlat2"; codepoint = 352
class scaron(xsc.Entity): "latin small letter s with caron, U+0161 ISOlat2"; codepoint = 353
class Yuml(xsc.Entity): "latin capital letter Y with diaeresis, U+0178 ISOlat2"; codepoint = 376

# Spacing Modifier Letters
class circ(xsc.Entity): "modifier letter circumflex accent, U+02C6 ISOpub"; codepoint = 710
class tilde(xsc.Entity): "small tilde, U+02DC ISOdia"; codepoint = 732

# General Punctuation
class ensp(xsc.Entity): "en space, U+2002 ISOpub"; codepoint = 8194
class emsp(xsc.Entity): "em space, U+2003 ISOpub"; codepoint = 8195
class thinsp(xsc.Entity): "thin space, U+2009 ISOpub"; codepoint = 8201
class zwnj(xsc.Entity): "zero width non-joiner, U+200C NEW RFC 2070"; codepoint = 8204
class zwj(xsc.Entity): "zero width joiner, U+200D NEW RFC 2070"; codepoint = 8205
class lrm(xsc.Entity): "left-to-right mark, U+200E NEW RFC 2070"; codepoint = 8206
class rlm(xsc.Entity): "right-to-left mark, U+200F NEW RFC 2070"; codepoint = 8207
class ndash(xsc.Entity): "en dash, U+2013 ISOpub"; codepoint = 8211
class mdash(xsc.Entity): "em dash, U+2014 ISOpub"; codepoint = 8212
class lsquo(xsc.Entity): "left single quotation mark, U+2018 ISOnum"; codepoint = 8216
class rsquo(xsc.Entity): "right single quotation mark, U+2019 ISOnum"; codepoint = 8217
class sbquo(xsc.Entity): "single low-9 quotation mark, U+201A NEW"; codepoint = 8218
class ldquo(xsc.Entity): "left double quotation mark, U+201C ISOnum"; codepoint = 8220
class rdquo(xsc.Entity): "right double quotation mark, U+201D ISOnum"; codepoint = 8221
class bdquo(xsc.Entity): "double low-9 quotation mark, U+201E NEW"; codepoint = 8222
class dagger(xsc.Entity): "dagger, U+2020 ISOpub"; codepoint = 8224
class Dagger(xsc.Entity): "double dagger, U+2021 ISOpub"; codepoint = 8225
class permil(xsc.Entity): "per mille sign, U+2030 ISOtech"; codepoint = 8240
class lsaquo(xsc.Entity): "single left-pointing angle quotation mark, U+2039 ISO proposed"; codepoint = 8249
class rsaquo(xsc.Entity): "single right-pointing angle quotation mark, U+203A ISO proposed"; codepoint = 8250
class euro(xsc.Entity): "euro sign, U+20AC NEW"; codepoint = 8364

# Mathematical, Greek and Symbolic characters
# Latin Extended-B
class fnof(xsc.Entity): "latin small f with hook = function = florin, U+0192 ISOtech"; codepoint = 402

# Greek
class Alpha(xsc.Entity): "greek capital letter alpha, U+0391"; codepoint = 913
class Beta(xsc.Entity): "greek capital letter beta, U+0392"; codepoint = 914
class Gamma(xsc.Entity): "greek capital letter gamma, U+0393 ISOgrk3"; codepoint = 915
class Delta(xsc.Entity): "greek capital letter delta, U+0394 ISOgrk3"; codepoint = 916
class Epsilon(xsc.Entity): "greek capital letter epsilon, U+0395"; codepoint = 917
class Zeta(xsc.Entity): "greek capital letter zeta, U+0396"; codepoint = 918
class Eta(xsc.Entity): "greek capital letter eta, U+0397"; codepoint = 919
class Theta(xsc.Entity): "greek capital letter theta, U+0398 ISOgrk3"; codepoint = 920
class Iota(xsc.Entity): "greek capital letter iota, U+0399"; codepoint = 921
class Kappa(xsc.Entity): "greek capital letter kappa, U+039A"; codepoint = 922
class Lambda(xsc.Entity): "greek capital letter lambda, U+039B ISOgrk3"; codepoint = 923
class Mu(xsc.Entity): "greek capital letter mu, U+039C"; codepoint = 924
class Nu(xsc.Entity): "greek capital letter nu, U+039D"; codepoint = 925
class Xi(xsc.Entity): "greek capital letter xi, U+039E ISOgrk3"; codepoint = 926
class Omicron(xsc.Entity): "greek capital letter omicron, U+039F"; codepoint = 927
class Pi(xsc.Entity): "greek capital letter pi, U+03A0 ISOgrk3"; codepoint = 928
class Rho(xsc.Entity): "greek capital letter rho, U+03A1"; codepoint = 929
class Sigma(xsc.Entity): "greek capital letter sigma, U+03A3 ISOgrk3"; codepoint = 931
class Tau(xsc.Entity): "greek capital letter tau, U+03A4"; codepoint = 932
class Upsilon(xsc.Entity): "greek capital letter upsilon, U+03A5 ISOgrk3"; codepoint = 933
class Phi(xsc.Entity): "greek capital letter phi, U+03A6 ISOgrk3"; codepoint = 934
class Chi(xsc.Entity): "greek capital letter chi, U+03A7"; codepoint = 935
class Psi(xsc.Entity): "greek capital letter psi, U+03A8 ISOgrk3"; codepoint = 936
class Omega(xsc.Entity): "greek capital letter omega, U+03A9 ISOgrk3"; codepoint = 937
class alpha(xsc.Entity): "greek small letter alpha, U+03B1 ISOgrk3"; codepoint = 945
class beta(xsc.Entity): "greek small letter beta, U+03B2 ISOgrk3"; codepoint = 946
class gamma(xsc.Entity): "greek small letter gamma, U+03B3 ISOgrk3"; codepoint = 947
class delta(xsc.Entity): "greek small letter delta, U+03B4 ISOgrk3"; codepoint = 948
class epsilon(xsc.Entity): "greek small letter epsilon, U+03B5 ISOgrk3"; codepoint = 949
class zeta(xsc.Entity): "greek small letter zeta, U+03B6 ISOgrk3"; codepoint = 950
class eta(xsc.Entity): "greek small letter eta, U+03B7 ISOgrk3"; codepoint = 951
class theta(xsc.Entity): "greek small letter theta, U+03B8 ISOgrk3"; codepoint = 952
class iota(xsc.Entity): "greek small letter iota, U+03B9 ISOgrk3"; codepoint = 953
class kappa(xsc.Entity): "greek small letter kappa, U+03BA ISOgrk3"; codepoint = 954
class lambda_(xsc.Entity): "greek small letter lambda, U+03BB ISOgrk3"; codepoint = 955; name = "lambda"
class mu(xsc.Entity): "greek small letter mu, U+03BC ISOgrk3"; codepoint = 956
class nu(xsc.Entity): "greek small letter nu, U+03BD ISOgrk3"; codepoint = 957
class xi(xsc.Entity): "greek small letter xi, U+03BE ISOgrk3"; codepoint = 958
class omicron(xsc.Entity): "greek small letter omicron, U+03BF NEW"; codepoint = 959
class pi(xsc.Entity): "greek small letter pi, U+03C0 ISOgrk3"; codepoint = 960
class rho(xsc.Entity): "greek small letter rho, U+03C1 ISOgrk3"; codepoint = 961
class sigmaf(xsc.Entity): "greek small letter final sigma, U+03C2 ISOgrk3"; codepoint = 962
class sigma(xsc.Entity): "greek small letter sigma, U+03C3 ISOgrk3"; codepoint = 963
class tau(xsc.Entity): "greek small letter tau, U+03C4 ISOgrk3"; codepoint = 964
class upsilon(xsc.Entity): "greek small letter upsilon, U+03C5 ISOgrk3"; codepoint = 965
class phi(xsc.Entity): "greek small letter phi, U+03C6 ISOgrk3"; codepoint = 966
class chi(xsc.Entity): "greek small letter chi, U+03C7 ISOgrk3"; codepoint = 967
class psi(xsc.Entity): "greek small letter psi, U+03C8 ISOgrk3"; codepoint = 968
class omega(xsc.Entity): "greek small letter omega, U+03C9 ISOgrk3"; codepoint = 969
class thetasym(xsc.Entity): "greek small letter theta symbol, U+03D1 NEW"; codepoint = 977
class upsih(xsc.Entity): "greek upsilon with hook symbol, U+03D2 NEW"; codepoint = 978
class piv(xsc.Entity): "greek pi symbol, U+03D6 ISOgrk3"; codepoint = 982

# General Punctuation
class bull(xsc.Entity): "bullet = black small circle, U+2022 ISOpub"; codepoint = 8226
class hellip(xsc.Entity): "horizontal ellipsis = three dot leader, U+2026 ISOpub"; codepoint = 8230
class prime(xsc.Entity): "prime = minutes = feet, U+2032 ISOtech"; codepoint = 8242
class Prime(xsc.Entity): "double prime = seconds = inches, U+2033 ISOtech"; codepoint = 8243
class oline(xsc.Entity): "overline = spacing overscore, U+203E NEW"; codepoint = 8254
class frasl(xsc.Entity): "fraction slash, U+2044 NEW"; codepoint = 8260

# Letterlike Symbols
class weierp(xsc.Entity): "script capital P = power set = Weierstrass p, U+2118 ISOamso"; codepoint = 8472
class image(xsc.Entity): "blackletter capital I = imaginary part, U+2111 ISOamso"; codepoint = 8465
class real(xsc.Entity): "blackletter capital R = real part symbol, U+211C ISOamso"; codepoint = 8476
class trade(xsc.Entity): "trade mark sign, U+2122 ISOnum"; codepoint = 8482
class alefsym(xsc.Entity): "alef symbol = first transfinite cardinal, U+2135 NEW"; codepoint = 8501

# Arrows
class larr(xsc.Entity): "leftwards arrow, U+2190 ISOnum"; codepoint = 8592
class uarr(xsc.Entity): "upwards arrow, U+2191 ISOnu"; codepoint = 8593
class rarr(xsc.Entity): "rightwards arrow, U+2192 ISOnum"; codepoint = 8594
class darr(xsc.Entity): "downwards arrow, U+2193 ISOnum"; codepoint = 8595
class harr(xsc.Entity): "left right arrow, U+2194 ISOamsa"; codepoint = 8596
class crarr(xsc.Entity): "downwards arrow with corner leftwards = carriage return, U+21B5 NEW"; codepoint = 8629
class lArr(xsc.Entity): "leftwards double arrow, U+21D0 ISOtech"; codepoint = 8656
class uArr(xsc.Entity): "upwards double arrow, U+21D1 ISOamsa"; codepoint = 8657
class rArr(xsc.Entity): "rightwards double arrow, U+21D2 ISOtech"; codepoint = 8658
class dArr(xsc.Entity): "downwards double arrow, U+21D3 ISOamsa"; codepoint = 8659
class hArr(xsc.Entity): "left right double arrow, U+21D4 ISOamsa"; codepoint = 8660

# Mathematical Operators
class forall(xsc.Entity): "for all, U+2200 ISOtech"; codepoint = 8704
class part(xsc.Entity): "partial differential, U+2202 ISOtech"; codepoint = 8706
class exist(xsc.Entity): "there exists, U+2203 ISOtech"; codepoint = 8707
class empty(xsc.Entity): "empty set = null set = diameter, U+2205 ISOamso"; codepoint = 8709
class nabla(xsc.Entity): "nabla = backward difference, U+2207 ISOtech"; codepoint = 8711
class isin(xsc.Entity): "element of, U+2208 ISOtech"; codepoint = 8712
class notin(xsc.Entity): "not an element of, U+2209 ISOtech"; codepoint = 8713
class ni(xsc.Entity): "contains as member, U+220B ISOtech"; codepoint = 8715
class prod(xsc.Entity): "n-ary product = product sign, U+220F ISOamsb"; codepoint = 8719
class sum(xsc.Entity): "n-ary sumation, U+2211 ISOamsb"; codepoint = 8721
class minus(xsc.Entity): "minus sign, U+2212 ISOtech"; codepoint = 8722
class lowast(xsc.Entity): "asterisk operator, U+2217 ISOtech"; codepoint = 8727
class radic(xsc.Entity): "square root = radical sign, U+221A ISOtech"; codepoint = 8730
class prop(xsc.Entity): "proportional to, U+221D ISOtech"; codepoint = 8733
class infin(xsc.Entity): "infinity, U+221E ISOtech"; codepoint = 8734
class ang(xsc.Entity): "angle, U+2220 ISOamso"; codepoint = 8736
class and_(xsc.Entity): "logical and = wedge, U+2227 ISOtech"; codepoint = 8743; name = "and"
class or_(xsc.Entity): "logical or = vee, U+2228 ISOtech"; codepoint = 8744; name = "or"
class cap(xsc.Entity): "intersection = cap, U+2229 ISOtech"; codepoint = 8745
class cup(xsc.Entity): "union = cup, U+222A ISOtech"; codepoint = 8746
class int(xsc.Entity): "integral, U+222B ISOtech"; codepoint = 8747
class there4(xsc.Entity): "therefore, U+2234 ISOtech"; codepoint = 8756
class sim(xsc.Entity): "tilde operator = varies with = similar to, U+223C ISOtech"; codepoint = 8764
class cong(xsc.Entity): "approximately equal to, U+2245 ISOtech"; codepoint = 8773
class asymp(xsc.Entity): "almost equal to = asymptotic to, U+2248 ISOamsr"; codepoint = 8776
class ne(xsc.Entity): "not equal to, U+2260 ISOtech"; codepoint = 8800
class equiv(xsc.Entity): "identical to, U+2261 ISOtech"; codepoint = 8801
class le(xsc.Entity): "less-than or equal to, U+2264 ISOtech"; codepoint = 8804
class ge(xsc.Entity): "greater-than or equal to, U+2265 ISOtech"; codepoint = 8805
class Sub(xsc.Entity): "subset of, U+2282 ISOtech"; codepoint = 8834; name = "sub"
class Sup(xsc.Entity): "superset of, U+2283 ISOtech"; codepoint = 8835; name = "sup"
class nsub(xsc.Entity): "not a subset of, U+2284 ISOamsn"; codepoint = 8836
class sube(xsc.Entity): "subset of or equal to, U+2286 ISOtech"; codepoint = 8838
class supe(xsc.Entity): "superset of or equal to, U+2287 ISOtech"; codepoint = 8839
class oplus(xsc.Entity): "circled plus = direct sum, U+2295 ISOamsb"; codepoint = 8853
class otimes(xsc.Entity): "circled times = vector product, U+2297 ISOamsb"; codepoint = 8855
class perp(xsc.Entity): "up tack = orthogonal to = perpendicular, U+22A5 ISOtech"; codepoint = 8869
class sdot(xsc.Entity): "dot operator, U+22C5 ISOamsb"; codepoint = 8901

# Miscellaneous Technical
class lceil(xsc.Entity): "left ceiling = apl upstile, U+2308 ISOamsc"; codepoint = 8968
class rceil(xsc.Entity): "right ceiling, U+2309 ISOamsc"; codepoint = 8969
class lfloor(xsc.Entity): "left floor = apl downstile, U+230A ISOamsc"; codepoint = 8970
class rfloor(xsc.Entity): "right floor, U+230B ISOamsc"; codepoint = 8971
class lang(xsc.Entity): "left-pointing angle bracket = bra, U+2329 ISOtech"; codepoint = 9001
class rang(xsc.Entity): "right-pointing angle bracket = ket, U+232A ISOtech"; codepoint = 9002

# Geometric Shapes
class loz(xsc.Entity): "lozenge, U+25CA ISOpub"; codepoint = 9674

# Miscellaneous Symbols
class spades(xsc.Entity): "black spade suit, U+2660 ISOpub"; codepoint = 9824
class clubs(xsc.Entity): "black club suit = shamrock, U+2663 ISOpub"; codepoint = 9827
class hearts(xsc.Entity): "black heart suit = valentine, U+2665 ISOpub"; codepoint = 9829
class diams(xsc.Entity): "black diamond suit, U+2666 ISOpub"; codepoint = 9830

# register all the classes we've defined so far
namespace = xsc.Namespace("html", "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd", vars())
