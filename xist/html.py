#! /usr/bin/env python

"""
A XSC module that contains definitions for all the elements in HTML 4.0 transitional
(and a few additional ones).
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import sys
import xsc

# common attributes
coreattrs  = { "id" : xsc.TextAttr , "class" : xsc.TextAttr , "style" : xsc.TextAttr , "title" : xsc.TextAttr }
i18n       = { "lang" : xsc.TextAttr , "dir"  : xsc.TextAttr }
events     = { "onclick" : xsc.TextAttr , "ondblclick" : xsc.TextAttr , "onmousedown" : xsc.TextAttr , "onmouseup" : xsc.TextAttr , "onmouseover" : xsc.TextAttr , "onmousemove" : xsc.TextAttr , "onmouseout" : xsc.TextAttr , "onkeypress" : xsc.TextAttr , "onkeydown" : xsc.TextAttr , "onkeyup" : xsc.TextAttr }
attrs      = xsc.appendDict(coreattrs,i18n,events)
cellhalign = { "align" : xsc.TextAttr , "char" : xsc.TextAttr , "charoff" : xsc.TextAttr  }
cellvalign = { "valign" : xsc.TextAttr }

class DocTypeHTML40transitional(xsc.DocType):
	"""
	document type for HTML 4.0 transitional
	"""
	def __init__(self,dtd = ""):
		s = 'HTML PUBLIC "-//W3C//DTD HTML 4.0 transitional//EN"'
		if dtd:
			s = s + " " + dtd
		xsc.DocType.__init__(self,s)

class DocTypeXHTML10strict(xsc.DocType):
	"""
	document type for XHTML 1.0 strict
	"""
	def __init__(self,dtd = ""):
		s = 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'
		if dtd:
			s = s + " " + dtd
		xsc.DocType.__init__(self,s)

# The global structure of an HTML document
class html(xsc.Element):
	"""
	document root element
	"""
	empty = 0
	attrHandlers = xsc.appendDict(i18n,{ "xmlns" : xsc.TextAttr })

class head(xsc.Element):
	"""
	document head
	"""
	empty = 0
	attrHandlers = xsc.appendDict(i18n,{ "profile" : xsc.TextAttr })

class title(xsc.Element):
	"""
	document title
	"""
	empty = 0
	attrHandlers = i18n

	def asHTML(self):
		e = title(self.attrs)
		e.append(self.content.asHTML().asPlainString())

		return e

class meta(xsc.Element):
	"""
	generic metainformation
	"""
	empty = 1
	attrHandlers = xsc.appendDict(i18n,{ "http_equiv" : xsc.TextAttr , "http-equiv" : xsc.TextAttr , "name" : xsc.TextAttr ,"content" : xsc.TextAttr ,"scheme" : xsc.TextAttr })

	def __init__(self,*_content,**_attrs):
		# we have two names for one and the same attribute http_equiv and http-equiv
		apply(xsc.Element.__init__,(self,) + _content,_attrs)
		if self.hasAttr("http_equiv"):
			if not self.hasAttr("http-equiv"):
				self["http-equiv"] = self["http_equiv"]
			del self["http_equiv"]

class body(xsc.Element):
	"""
	document body
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "onload" : xsc.TextAttr , "onunload" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "background" : xsc.URLAttr , "bgcolor" : xsc.ColorAttr , "text" : xsc.ColorAttr , "link" : xsc.ColorAttr , "vlink" : xsc.ColorAttr , "alink" : xsc.ColorAttr , "leftmargin" : xsc.TextAttr , "topmargin" : xsc.TextAttr , "marginwidth" : xsc.TextAttr , "marginheight" : xsc.TextAttr }) # deprecated

class div(xsc.Element):
	"""
	generic language/style container
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated

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
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated

class h2(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated

class h3(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated

class h4(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated

class h5(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated

class h6(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated

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
	attrHandlers = xsc.appendDict(coreattrs,i18n)

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
	attrHandlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr })

class q(xsc.Element):
	"""
	short inline quotation
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr })

	def asPlainString(self):
		return '«' + self.content.asPlainString() + '»'

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
	attrHandlers = attrs
	attrHandlers = xsc.appendDict({ "align" : xsc.TextAttr }) # deprecated

class br(xsc.Element):
	"""
	forced line break
	"""
	empty = 1
	attrHandlers = coreattrs

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
	attrHandlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr , "datetime" : xsc.TextAttr })

class Del(xsc.Element):
	"""
	deleted text
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr , "datetime" : xsc.TextAttr })

class ul(xsc.Element):
	"""
	unordered list
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr }) # deprecated

class ol(xsc.Element):
	"""
	ordered list
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr }) # deprecated

class li(xsc.Element):
	"""
	list item
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr }) # deprecated

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
	attrHandlers = xsc.appendDict(attrs,{ "summary" : xsc.TextAttr ,"width" : xsc.TextAttr ,"border" : xsc.TextAttr ,"frame" : xsc.TextAttr ,"rules" : xsc.TextAttr ,"cellspacing" : xsc.TextAttr ,"cellpadding" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "height" : xsc.TextAttr , "align" : xsc.TextAttr , "bgcolor" : xsc.ColorAttr }) # deprecated

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
	attrHandlers = xsc.appendDict(attrs,cellhalign,cellvalign)

class tfoot(xsc.Element):
	"""
	table footer
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,cellhalign,cellvalign)

class tbody(xsc.Element):
	"""
	table body
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,cellhalign,cellvalign)

class colgroup(xsc.Element):
	"""
	table column group
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "span" : xsc.TextAttr , "width" : xsc.TextAttr },cellhalign,cellvalign)

class col(xsc.Element):
	"""
	table column
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "span" : xsc.TextAttr , "width" : xsc.TextAttr },cellhalign,cellvalign)

class tr(xsc.Element):
	"""
	table row
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,cellhalign,cellvalign)
	attrHandlers = xsc.appendDict(attrHandlers,{ "nowrap" : xsc.TextAttr , "bgcolor" : xsc.ColorAttr , "width" : xsc.TextAttr }) # deprecated

class th(xsc.Element):
	"""
	table header cell
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "abbr" : xsc.TextAttr , "axis" : xsc.TextAttr , "headers" : xsc.TextAttr , "scope" : xsc.TextAttr , "rowspan" : xsc.TextAttr , "colspan" : xsc.TextAttr },cellhalign,cellvalign)

class td(xsc.Element):
	"""
	table data cell
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "abbr" : xsc.TextAttr , "axis" : xsc.TextAttr , "headers" : xsc.TextAttr , "scope" : xsc.TextAttr , "rowspan" : xsc.TextAttr , "colspan" : xsc.TextAttr },cellhalign,cellvalign)
	attrHandlers = xsc.appendDict(attrHandlers,{ "nowrap" : xsc.TextAttr , "bgcolor" : xsc.ColorAttr , "width" : xsc.TextAttr , "height" : xsc.TextAttr , "background" : xsc.URLAttr }) # deprecated

class a(xsc.Element):
	"""
	anchor
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "charset" : xsc.TextAttr , "type" : xsc.TextAttr , "name" : xsc.TextAttr , "href" : xsc.URLAttr , "hreflang" : xsc.TextAttr , "rel" : xsc.TextAttr , "rev" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "shape" : xsc.TextAttr , "coords" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "target" : xsc.TextAttr }) # deprecated

class link(xsc.Element):
	"""
	a media-independent link
	"""
	empty = 1
	attrHandlers = xsc.appendDict(attrs,{ "charset" : xsc.TextAttr , "href" : xsc.URLAttr , "hreflang" : xsc.TextAttr , "type" : xsc.TextAttr , "rel" : xsc.TextAttr , "rev" : xsc.TextAttr , "media" : xsc.TextAttr })

class base(xsc.Element):
	"""
	document base URI
	"""
	empty = 1
	attrHandlers = { "href" : xsc.URLAttr }

class img(xsc.Element):
	"""
	Embedded image
	"""
	empty = 1
	attrHandlers = xsc.appendDict(attrs,{ "src" : xsc.URLAttr , "alt" : xsc.TextAttr , "longdesc" : xsc.TextAttr , "width" : xsc.TextAttr , "height" : xsc.TextAttr , "usemap" : xsc.TextAttr , "ismap" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "name" : xsc.TextAttr , "border" : xsc.TextAttr , "align" : xsc.TextAttr , "hspace" : xsc.TextAttr , "vspace" : xsc.TextAttr , "lowsrc" : xsc.URLAttr }) # deprecated

	def asHTML(self):
		e = self.clone()
		e.addImageSizeAttributes("src")

		return e

	def asPlainString(self):
		if self.hasAttr("alt"):
			return self["alt"].asPlainString()
		else:
			return ""

class object(xsc.Element):
	"""
	generic embedded object
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "declare" : xsc.TextAttr , "classid" : xsc.TextAttr , "codebase" : xsc.TextAttr , "data" : xsc.TextAttr , "type" : xsc.TextAttr , "codetype" : xsc.TextAttr , "archive" : xsc.TextAttr , "standby" : xsc.TextAttr , "height" : xsc.TextAttr , "width" : xsc.TextAttr , "usemap" : xsc.TextAttr , "name" : xsc.TextAttr , "tabindex" : xsc.TextAttr })

class param(xsc.Element):
	"""
	named property value
	"""
	empty = 1
	attrHandlers = { "id" : xsc.TextAttr , "name" : xsc.TextAttr , "value" : xsc.TextAttr , "valuetype" : xsc.TextAttr , "type" : xsc.TextAttr }

class map(xsc.Element):
	"""
	client-side image map
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr })

class area(xsc.Element):
	"""
	client-side image map area
	"""
	empty = 1
	attrHandlers = xsc.appendDict(attrs,{ "shape" : xsc.TextAttr , "coords" : xsc.TextAttr , "href" : xsc.URLAttr , "nohref" : xsc.TextAttr , "alt" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })

class style(xsc.Element):
	"""
	style info
	"""
	empty = 0
	attrHandlers = xsc.appendDict(i18n,{ "type" : xsc.TextAttr , "media" : xsc.TextAttr , "title" : xsc.TextAttr })

class hr(xsc.Element):
	"""
	horizontal rule
	"""
	empty = 1
	attrHandlers = xsc.appendDict(coreattrs,events)
	attrHandlers = xsc.appendDict(attrHandlers,{ "noshade" : xsc.TextAttr , "size" : xsc.TextAttr } ) # deprecated

# The pain, the pain ...
class frameset(xsc.Element):
	"""
	window subdivision
	"""
	empty = 0
	attrHandlers = xsc.appendDict(coreattrs,{ "rows" : xsc.TextAttr ,"cols" : xsc.TextAttr ,"onload" : xsc.TextAttr ,"onunload" : xsc.TextAttr })

class frame(xsc.Element):
	"""
	subwindow
	"""
	empty = 0
	attrHandlers = xsc.appendDict(coreattrs,{ "longdesc" : xsc.TextAttr , "name" : xsc.TextAttr , "src" : xsc.URLAttr , "frameborder" : xsc.TextAttr , "marginwidht" : xsc.TextAttr , "marginheight" : xsc.TextAttr , "noresize" : xsc.TextAttr , "scrolling" : xsc.TextAttr })

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
	attrHandlers = xsc.appendDict(coreattrs,{ "longdesc" : xsc.TextAttr , "name" : xsc.TextAttr , "src" : xsc.URLAttr , "frameborder" : xsc.TextAttr , "marginwidht" : xsc.TextAttr , "marginheight" : xsc.TextAttr , "noresize" : xsc.TextAttr , "scrolling" : xsc.TextAttr , "align" : xsc.TextAttr , "height" : xsc.TextAttr , "width" : xsc.TextAttr })

class form(xsc.Element):
	"""
	interactive form
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "action" : xsc.URLAttr , "method" : xsc.TextAttr , "enctype" : xsc.TextAttr , "onsubmit" : xsc.TextAttr , "onreset" : xsc.TextAttr , "accept-charset" : xsc.TextAttr })

class input(xsc.Element):
	"""
	form control
	"""
	empty = 1
	attrHandlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr , "name" : xsc.TextAttr , "value" : xsc.TextAttr , "checked" : xsc.TextAttr , "disabled" : xsc.TextAttr , "readonly" : xsc.TextAttr , "size" : xsc.TextAttr , "maxlength" : xsc.TextAttr , "src" : xsc.URLAttr , "alt" : xsc.TextAttr , "usemap" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr , "onselect" : xsc.TextAttr , "onchange" : xsc.TextAttr , "accept" : xsc.TextAttr })

class button(xsc.Element):
	"""
	push button
	"""
	empty = 1
	attrHandlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr , "value" : xsc.TextAttr , "type" : xsc.TextAttr , "disabled" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })

class select(xsc.Element):
	"""
	option selector
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr , "size" : xsc.TextAttr , "multiple" : xsc.TextAttr , "disabled" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr , "onchange" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "rows" : xsc.TextAttr }) # deprecated

class optgroup(xsc.Element):
	"""
	option group
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "disabled" : xsc.TextAttr , "label" : xsc.TextAttr })

class option(xsc.Element):
	"""
	selectable choice
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "selected" : xsc.TextAttr , "disabled" : xsc.TextAttr , "label" : xsc.TextAttr , "value" : xsc.TextAttr })

class textarea(xsc.Element):
	"""
	multi-line text field
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr , "rows" : xsc.TextAttr , "cols" : xsc.TextAttr , "disabled" : xsc.TextAttr , "readonly" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr , "onselect" : xsc.TextAttr , "onchange" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "wrap" : xsc.TextAttr })

class label(xsc.Element):
	"""
	form field label text
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "for" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })

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
	attrHandlers = xsc.appendDict(attrs,{ "accesskey" : xsc.TextAttr })

class script(xsc.Element):
	"""
	script statements
	"""
	empty = 0
	attrHandlers = { "charset" : xsc.TextAttr , "type" : xsc.TextAttr , "src" : xsc.URLAttr , "defer" : xsc.TextAttr }
	attrHandlers = xsc.appendDict(attrHandlers,{ "language" : xsc.TextAttr }) # deprecated

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
	attrHandlers = { "face" : xsc.TextAttr , "size" : xsc.TextAttr , "color" : xsc.ColorAttr }

class applet(xsc.Element): # deprecated
	"""
	Java applet
	"""
	empty = 0
	attrHandlers = { "archive" : xsc.URLAttr , "code" : xsc.URLAttr , "width" : xsc.TextAttr , "height" : xsc.TextAttr }

# register all the classes we've defined so far
xsc.registerAllElements(vars(),"html")

# Latin 1 characters
xsc.registerEntity("nbsp",xsc.CharRef(160)) # no-break space = non-breaking space, U+00A0 ISOnum
xsc.registerEntity("iexcl",xsc.CharRef(161)) # inverted exclamation mark, U+00A1 ISOnum
xsc.registerEntity("cent",xsc.CharRef(162)) # cent sign, U+00A2 ISOnum
xsc.registerEntity("pound",xsc.CharRef(163)) # pound sign, U+00A3 ISOnum
xsc.registerEntity("curren",xsc.CharRef(164)) # currency sign, U+00A4 ISOnum
xsc.registerEntity("yen",xsc.CharRef(165)) # yen sign = yuan sign, U+00A5 ISOnum
xsc.registerEntity("brvbar",xsc.CharRef(166)) # broken bar = broken vertical bar, U+00A6 ISOnum
xsc.registerEntity("sect",xsc.CharRef(167)) # section sign, U+00A7 ISOnum
xsc.registerEntity("uml",xsc.CharRef(168)) # diaeresis = spacing diaeresis, U+00A8 ISOdia
xsc.registerEntity("copy",xsc.CharRef(169)) # copyright sign, U+00A9 ISOnum
xsc.registerEntity("ordf",xsc.CharRef(170)) # feminine ordinal indicator, U+00AA ISOnum
xsc.registerEntity("laquo",xsc.CharRef(171)) # left-pointing double angle quotation mark = left pointing guillemet, U+00AB ISOnum
xsc.registerEntity("not",xsc.CharRef(172)) # not sign, U+00AC ISOnum
xsc.registerEntity("shy",xsc.CharRef(173)) # soft hyphen = discretionary hyphen, U+00AD ISOnum
xsc.registerEntity("reg",xsc.CharRef(174)) # registered sign = registered trade mark sign, U+00AE ISOnum
xsc.registerEntity("macr",xsc.CharRef(175)) # macron = spacing macron = overline = APL overbar, U+00AF ISOdia
xsc.registerEntity("deg",xsc.CharRef(176)) # degree sign, U+00B0 ISOnum
xsc.registerEntity("plusmn",xsc.CharRef(177)) # plus-minus sign = plus-or-minus sign, U+00B1 ISOnum
xsc.registerEntity("sup2",xsc.CharRef(178)) # superscript two = superscript digit two = squared, U+00B2 ISOnum
xsc.registerEntity("sup3",xsc.CharRef(179)) # superscript three = superscript digit three = cubed, U+00B3 ISOnum
xsc.registerEntity("acute",xsc.CharRef(180)) # acute accent = spacing acute, U+00B4 ISOdia
xsc.registerEntity("micro",xsc.CharRef(181)) # micro sign, U+00B5 ISOnum
xsc.registerEntity("para",xsc.CharRef(182)) # pilcrow sign = paragraph sign, U+00B6 ISOnum
xsc.registerEntity("middot",xsc.CharRef(183)) # middle dot = Georgian comma = Greek middle dot, U+00B7 ISOnum
xsc.registerEntity("cedil",xsc.CharRef(184)) # cedilla = spacing cedilla, U+00B8 ISOdia
xsc.registerEntity("sup1",xsc.CharRef(185)) # superscript one = superscript digit one, U+00B9 ISOnum
xsc.registerEntity("ordm",xsc.CharRef(186)) # masculine ordinal indicator, U+00BA ISOnum
xsc.registerEntity("raquo",xsc.CharRef(187)) # right-pointing double angle quotation mark = right pointing guillemet, U+00BB ISOnum
xsc.registerEntity("frac14",xsc.CharRef(188)) # vulgar fraction one quarter = fraction one quarter, U+00BC ISOnum
xsc.registerEntity("frac12",xsc.CharRef(189)) # vulgar fraction one half = fraction one half, U+00BD ISOnum
xsc.registerEntity("frac34",xsc.CharRef(190)) # vulgar fraction three quarters = fraction three quarters, U+00BE ISOnum
xsc.registerEntity("iquest",xsc.CharRef(191)) # inverted question mark = turned question mark, U+00BF ISOnum
xsc.registerEntity("Agrave",xsc.CharRef(192)) # latin capital letter A with grave = latin capital letter A grave, U+00C0 ISOlat1
xsc.registerEntity("Aacute",xsc.CharRef(193)) # latin capital letter A with acute, U+00C1 ISOlat1
xsc.registerEntity("Acirc",xsc.CharRef(194)) # latin capital letter A with circumflex, U+00C2 ISOlat1
xsc.registerEntity("Atilde",xsc.CharRef(195)) # latin capital letter A with tilde, U+00C3 ISOlat1
xsc.registerEntity("Auml",xsc.CharRef(196)) # latin capital letter A with diaeresis, U+00C4 ISOlat1
xsc.registerEntity("Aring",xsc.CharRef(197)) # latin capital letter A with ring above = latin capital letter A ring, U+00C5 ISOlat1
xsc.registerEntity("AElig",xsc.CharRef(198)) # latin capital letter AE = latin capital ligature AE, U+00C6 ISOlat1
xsc.registerEntity("Ccedil",xsc.CharRef(199)) # latin capital letter C with cedilla, U+00C7 ISOlat1
xsc.registerEntity("Egrave",xsc.CharRef(200)) # latin capital letter E with grave, U+00C8 ISOlat1
xsc.registerEntity("Eacute",xsc.CharRef(201)) # latin capital letter E with acute, U+00C9 ISOlat1
xsc.registerEntity("Ecirc",xsc.CharRef(202)) # latin capital letter E with circumflex, U+00CA ISOlat1
xsc.registerEntity("Euml",xsc.CharRef(203)) # latin capital letter E with diaeresis, U+00CB ISOlat1
xsc.registerEntity("Igrave",xsc.CharRef(204)) # latin capital letter I with grave, U+00CC ISOlat1
xsc.registerEntity("Iacute",xsc.CharRef(205)) # latin capital letter I with acute, U+00CD ISOlat1
xsc.registerEntity("Icirc",xsc.CharRef(206)) # latin capital letter I with circumflex, U+00CE ISOlat1
xsc.registerEntity("Iuml",xsc.CharRef(207)) # latin capital letter I with diaeresis, U+00CF ISOlat1
xsc.registerEntity("ETH",xsc.CharRef(208)) # latin capital letter ETH, U+00D0 ISOlat1
xsc.registerEntity("Ntilde",xsc.CharRef(209)) # latin capital letter N with tilde, U+00D1 ISOlat1
xsc.registerEntity("Ograve",xsc.CharRef(210)) # latin capital letter O with grave, U+00D2 ISOlat1
xsc.registerEntity("Oacute",xsc.CharRef(211)) # latin capital letter O with acute, U+00D3 ISOlat1
xsc.registerEntity("Ocirc",xsc.CharRef(212)) # latin capital letter O with circumflex, U+00D4 ISOlat1
xsc.registerEntity("Otilde",xsc.CharRef(213)) # latin capital letter O with tilde, U+00D5 ISOlat1
xsc.registerEntity("Ouml",xsc.CharRef(214)) # latin capital letter O with diaeresis, U+00D6 ISOlat1
xsc.registerEntity("times",xsc.CharRef(215)) # multiplication sign, U+00D7 ISOnum
xsc.registerEntity("Oslash",xsc.CharRef(216)) # latin capital letter O with stroke = latin capital letter O slash, U+00D8 ISOlat1
xsc.registerEntity("Ugrave",xsc.CharRef(217)) # latin capital letter U with grave, U+00D9 ISOlat1
xsc.registerEntity("Uacute",xsc.CharRef(218)) # latin capital letter U with acute, U+00DA ISOlat1
xsc.registerEntity("Ucirc",xsc.CharRef(219)) # latin capital letter U with circumflex, U+00DB ISOlat1
xsc.registerEntity("Uuml",xsc.CharRef(220)) # latin capital letter U with diaeresis, U+00DC ISOlat1
xsc.registerEntity("Yacute",xsc.CharRef(221)) # latin capital letter Y with acute, U+00DD ISOlat1
xsc.registerEntity("THORN",xsc.CharRef(222)) # latin capital letter THORN, U+00DE ISOlat1
xsc.registerEntity("szlig",xsc.CharRef(223)) # latin small letter sharp s = ess-zed, U+00DF ISOlat1
xsc.registerEntity("agrave",xsc.CharRef(224)) # latin small letter a with grave = latin small letter a grave, U+00E0 ISOlat1
xsc.registerEntity("aacute",xsc.CharRef(225)) # latin small letter a with acute, U+00E1 ISOlat1
xsc.registerEntity("acirc",xsc.CharRef(226)) # latin small letter a with circumflex, U+00E2 ISOlat1
xsc.registerEntity("atilde",xsc.CharRef(227)) # latin small letter a with tilde, U+00E3 ISOlat1
xsc.registerEntity("auml",xsc.CharRef(228)) # latin small letter a with diaeresis, U+00E4 ISOlat1
xsc.registerEntity("aring",xsc.CharRef(229)) # latin small letter a with ring above = latin small letter a ring, U+00E5 ISOlat1
xsc.registerEntity("aelig",xsc.CharRef(230)) # latin small letter ae = latin small ligature ae, U+00E6 ISOlat1
xsc.registerEntity("ccedil",xsc.CharRef(231)) # latin small letter c with cedilla, U+00E7 ISOlat1
xsc.registerEntity("egrave",xsc.CharRef(232)) # latin small letter e with grave, U+00E8 ISOlat1
xsc.registerEntity("eacute",xsc.CharRef(233)) # latin small letter e with acute, U+00E9 ISOlat1
xsc.registerEntity("ecirc",xsc.CharRef(234)) # latin small letter e with circumflex, U+00EA ISOlat1
xsc.registerEntity("euml",xsc.CharRef(235)) # latin small letter e with diaeresis, U+00EB ISOlat1
xsc.registerEntity("igrave",xsc.CharRef(236)) # latin small letter i with grave, U+00EC ISOlat1
xsc.registerEntity("iacute",xsc.CharRef(237)) # latin small letter i with acute, U+00ED ISOlat1
xsc.registerEntity("icirc",xsc.CharRef(238)) # latin small letter i with circumflex, U+00EE ISOlat1
xsc.registerEntity("iuml",xsc.CharRef(239)) # latin small letter i with diaeresis, U+00EF ISOlat1
xsc.registerEntity("eth",xsc.CharRef(240)) # latin small letter eth, U+00F0 ISOlat1
xsc.registerEntity("ntilde",xsc.CharRef(241)) # latin small letter n with tilde, U+00F1 ISOlat1
xsc.registerEntity("ograve",xsc.CharRef(242)) # latin small letter o with grave, U+00F2 ISOlat1
xsc.registerEntity("oacute",xsc.CharRef(243)) # latin small letter o with acute, U+00F3 ISOlat1
xsc.registerEntity("ocirc",xsc.CharRef(244)) # latin small letter o with circumflex, U+00F4 ISOlat1
xsc.registerEntity("otilde",xsc.CharRef(245)) # latin small letter o with tilde, U+00F5 ISOlat1
xsc.registerEntity("ouml",xsc.CharRef(246)) # latin small letter o with diaeresis, U+00F6 ISOlat1
xsc.registerEntity("divide",xsc.CharRef(247)) # division sign, U+00F7 ISOnum
xsc.registerEntity("oslash",xsc.CharRef(248)) # latin small letter o with stroke, = latin small letter o slash, U+00F8 ISOlat1
xsc.registerEntity("ugrave",xsc.CharRef(249)) # latin small letter u with grave, U+00F9 ISOlat1
xsc.registerEntity("uacute",xsc.CharRef(250)) # latin small letter u with acute, U+00FA ISOlat1
xsc.registerEntity("ucirc",xsc.CharRef(251)) # latin small letter u with circumflex, U+00FB ISOlat1
xsc.registerEntity("uuml",xsc.CharRef(252)) # latin small letter u with diaeresis, U+00FC ISOlat1
xsc.registerEntity("yacute",xsc.CharRef(253)) # latin small letter y with acute, U+00FD ISOlat1
xsc.registerEntity("thorn",xsc.CharRef(254)) # latin small letter thorn, U+00FE ISOlat1
xsc.registerEntity("yuml",xsc.CharRef(255)) # latin small letter y with diaeresis, U+00FF ISOlat1

# Latin Extended-A
xsc.registerEntity("OElig",xsc.CharRef(338)) # latin capital ligature OE, U+0152 ISOlat2
xsc.registerEntity("oelig",xsc.CharRef(339)) # latin small ligature oe, U+0153 ISOlat2
xsc.registerEntity("Scaron",xsc.CharRef(352)) # latin capital letter S with caron, U+0160 ISOlat2
xsc.registerEntity("scaron",xsc.CharRef(353)) # latin small letter s with caron, U+0161 ISOlat2
xsc.registerEntity("Yuml",xsc.CharRef(376)) # latin capital letter Y with diaeresis, U+0178 ISOlat2

# Spacing Modifier Letters
xsc.registerEntity("circ",xsc.CharRef(710)) # modifier letter circumflex accent, U+02C6 ISOpub
xsc.registerEntity("tilde",xsc.CharRef(732)) # small tilde, U+02DC ISOdia

# General Punctuation
xsc.registerEntity("ensp",xsc.CharRef(8194)) # en space, U+2002 ISOpub
xsc.registerEntity("emsp",xsc.CharRef(8195)) # em space, U+2003 ISOpub
xsc.registerEntity("thinsp",xsc.CharRef(8201)) # thin space, U+2009 ISOpub
xsc.registerEntity("zwnj",xsc.CharRef(8204)) # zero width non-joiner, U+200C NEW RFC 2070
xsc.registerEntity("zwj",xsc.CharRef(8205)) # zero width joiner, U+200D NEW RFC 2070
xsc.registerEntity("lrm",xsc.CharRef(8206)) # left-to-right mark, U+200E NEW RFC 2070
xsc.registerEntity("rlm",xsc.CharRef(8207)) # right-to-left mark, U+200F NEW RFC 2070
xsc.registerEntity("ndash",xsc.CharRef(8211)) # en dash, U+2013 ISOpub
xsc.registerEntity("mdash",xsc.CharRef(8212)) # em dash, U+2014 ISOpub
xsc.registerEntity("lsquo",xsc.CharRef(8216)) # left single quotation mark, U+2018 ISOnum
xsc.registerEntity("rsquo",xsc.CharRef(8217)) # right single quotation mark, U+2019 ISOnum
xsc.registerEntity("sbquo",xsc.CharRef(8218)) # single low-9 quotation mark, U+201A NEW
xsc.registerEntity("ldquo",xsc.CharRef(8220)) # left double quotation mark, U+201C ISOnum
xsc.registerEntity("rdquo",xsc.CharRef(8221)) # right double quotation mark, U+201D ISOnum
xsc.registerEntity("bdquo",xsc.CharRef(8222)) # double low-9 quotation mark, U+201E NEW
xsc.registerEntity("dagger",xsc.CharRef(8224)) # dagger, U+2020 ISOpub
xsc.registerEntity("Dagger",xsc.CharRef(8225)) # double dagger, U+2021 ISOpub
xsc.registerEntity("permil",xsc.CharRef(8240)) # per mille sign, U+2030 ISOtech
xsc.registerEntity("lsaquo",xsc.CharRef(8249)) # single left-pointing angle quotation mark, U+2039 ISO proposed
xsc.registerEntity("rsaquo",xsc.CharRef(8250)) # single right-pointing angle quotation mark, U+203A ISO proposed
xsc.registerEntity("euro",xsc.CharRef(8364)) # euro sign, U+20AC NEW

# Mathematical, Greek and Symbolic characters
# Latin Extended-B
xsc.registerEntity("fnof",xsc.CharRef(402)) # latin small f with hook = function = florin, U+0192 ISOtech

# Greek
xsc.registerEntity("Alpha",xsc.CharRef(913)) # greek capital letter alpha, U+0391
xsc.registerEntity("Beta",xsc.CharRef(914)) # greek capital letter beta, U+0392
xsc.registerEntity("Gamma",xsc.CharRef(915)) # greek capital letter gamma, U+0393 ISOgrk3
xsc.registerEntity("Delta",xsc.CharRef(916)) # greek capital letter delta, U+0394 ISOgrk3
xsc.registerEntity("Epsilon",xsc.CharRef(917)) # greek capital letter epsilon, U+0395
xsc.registerEntity("Zeta",xsc.CharRef(918)) # greek capital letter zeta, U+0396
xsc.registerEntity("Eta",xsc.CharRef(919)) # greek capital letter eta, U+0397
xsc.registerEntity("Theta",xsc.CharRef(920)) # greek capital letter theta, U+0398 ISOgrk3
xsc.registerEntity("Iota",xsc.CharRef(921)) # greek capital letter iota, U+0399
xsc.registerEntity("Kappa",xsc.CharRef(922)) # greek capital letter kappa, U+039A
xsc.registerEntity("Lambda",xsc.CharRef(923)) # greek capital letter lambda, U+039B ISOgrk3
xsc.registerEntity("Mu",xsc.CharRef(924)) # greek capital letter mu, U+039C
xsc.registerEntity("Nu",xsc.CharRef(925)) # greek capital letter nu, U+039D
xsc.registerEntity("Xi",xsc.CharRef(926)) # greek capital letter xi, U+039E ISOgrk3
xsc.registerEntity("Omicron",xsc.CharRef(927)) # greek capital letter omicron, U+039F
xsc.registerEntity("Pi",xsc.CharRef(928)) # greek capital letter pi, U+03A0 ISOgrk3
xsc.registerEntity("Rho",xsc.CharRef(929)) # greek capital letter rho, U+03A1
xsc.registerEntity("Sigma",xsc.CharRef(931)) # greek capital letter sigma, U+03A3 ISOgrk3
xsc.registerEntity("Tau",xsc.CharRef(932)) # greek capital letter tau, U+03A4
xsc.registerEntity("Upsilon",xsc.CharRef(933)) # greek capital letter upsilon, U+03A5 ISOgrk3
xsc.registerEntity("Phi",xsc.CharRef(934)) # greek capital letter phi, U+03A6 ISOgrk3
xsc.registerEntity("Chi",xsc.CharRef(935)) # greek capital letter chi, U+03A7
xsc.registerEntity("Psi",xsc.CharRef(936)) # greek capital letter psi, U+03A8 ISOgrk3
xsc.registerEntity("Omega",xsc.CharRef(937)) # greek capital letter omega, U+03A9 ISOgrk3
xsc.registerEntity("alpha",xsc.CharRef(945)) # greek small letter alpha, U+03B1 ISOgrk3
xsc.registerEntity("beta",xsc.CharRef(946)) # greek small letter beta, U+03B2 ISOgrk3
xsc.registerEntity("gamma",xsc.CharRef(947)) # greek small letter gamma, U+03B3 ISOgrk3
xsc.registerEntity("delta",xsc.CharRef(948)) # greek small letter delta, U+03B4 ISOgrk3
xsc.registerEntity("epsilon",xsc.CharRef(949)) # greek small letter epsilon, U+03B5 ISOgrk3
xsc.registerEntity("zeta",xsc.CharRef(950)) # greek small letter zeta, U+03B6 ISOgrk3
xsc.registerEntity("eta",xsc.CharRef(951)) # greek small letter eta, U+03B7 ISOgrk3
xsc.registerEntity("theta",xsc.CharRef(952)) # greek small letter theta, U+03B8 ISOgrk3
xsc.registerEntity("iota",xsc.CharRef(953)) # greek small letter iota, U+03B9 ISOgrk3
xsc.registerEntity("kappa",xsc.CharRef(954)) # greek small letter kappa, U+03BA ISOgrk3
xsc.registerEntity("lambda",xsc.CharRef(955)) # greek small letter lambda, U+03BB ISOgrk3
xsc.registerEntity("mu",xsc.CharRef(956)) # greek small letter mu, U+03BC ISOgrk3
xsc.registerEntity("nu",xsc.CharRef(957)) # greek small letter nu, U+03BD ISOgrk3
xsc.registerEntity("xi",xsc.CharRef(958)) # greek small letter xi, U+03BE ISOgrk3
xsc.registerEntity("omicron",xsc.CharRef(959)) # greek small letter omicron, U+03BF NEW
xsc.registerEntity("pi",xsc.CharRef(960)) # greek small letter pi, U+03C0 ISOgrk3
xsc.registerEntity("rho",xsc.CharRef(961)) # greek small letter rho, U+03C1 ISOgrk3
xsc.registerEntity("sigmaf",xsc.CharRef(962)) # greek small letter final sigma, U+03C2 ISOgrk3
xsc.registerEntity("sigma",xsc.CharRef(963)) # greek small letter sigma, U+03C3 ISOgrk3
xsc.registerEntity("tau",xsc.CharRef(964)) # greek small letter tau, U+03C4 ISOgrk3
xsc.registerEntity("upsilon",xsc.CharRef(965)) # greek small letter upsilon, U+03C5 ISOgrk3
xsc.registerEntity("phi",xsc.CharRef(966)) # greek small letter phi, U+03C6 ISOgrk3
xsc.registerEntity("chi",xsc.CharRef(967)) # greek small letter chi, U+03C7 ISOgrk3
xsc.registerEntity("psi",xsc.CharRef(968)) # greek small letter psi, U+03C8 ISOgrk3
xsc.registerEntity("omega",xsc.CharRef(969)) # greek small letter omega, U+03C9 ISOgrk3
xsc.registerEntity("thetasym",xsc.CharRef(977)) # greek small letter theta symbol, U+03D1 NEW
xsc.registerEntity("upsih",xsc.CharRef(978)) # greek upsilon with hook symbol, U+03D2 NEW
xsc.registerEntity("piv",xsc.CharRef(982)) # greek pi symbol, U+03D6 ISOgrk3

# General Punctuation
xsc.registerEntity("bull",xsc.CharRef(8226)) # bullet = black small circle, U+2022 ISOpub
xsc.registerEntity("hellip",xsc.CharRef(8230)) # horizontal ellipsis = three dot leader, U+2026 ISOpub
xsc.registerEntity("prime",xsc.CharRef(8242)) # prime = minutes = feet, U+2032 ISOtech
xsc.registerEntity("Prime",xsc.CharRef(8243)) # double prime = seconds = inches, U+2033 ISOtech
xsc.registerEntity("oline",xsc.CharRef(8254)) # overline = spacing overscore, U+203E NEW
xsc.registerEntity("frasl",xsc.CharRef(8260)) # fraction slash, U+2044 NEW

# Letterlike Symbols
xsc.registerEntity("weierp",xsc.CharRef(8472)) # script capital P = power set = Weierstrass p, U+2118 ISOamso
xsc.registerEntity("image",xsc.CharRef(8465)) # blackletter capital I = imaginary part, U+2111 ISOamso
xsc.registerEntity("real",xsc.CharRef(8476)) # blackletter capital R = real part symbol, U+211C ISOamso
xsc.registerEntity("trade",xsc.CharRef(8482)) # trade mark sign, U+2122 ISOnum
xsc.registerEntity("alefsym",xsc.CharRef(8501)) # alef symbol = first transfinite cardinal, U+2135 NEW

# Arrows
xsc.registerEntity("larr",xsc.CharRef(8592)) # leftwards arrow, U+2190 ISOnum
xsc.registerEntity("uarr",xsc.CharRef(8593)) # upwards arrow, U+2191 ISOnu
xsc.registerEntity("rarr",xsc.CharRef(8594)) # rightwards arrow, U+2192 ISOnum
xsc.registerEntity("darr",xsc.CharRef(8595)) # downwards arrow, U+2193 ISOnum
xsc.registerEntity("harr",xsc.CharRef(8596)) # left right arrow, U+2194 ISOamsa
xsc.registerEntity("crarr",xsc.CharRef(8629)) # downwards arrow with corner leftwards = carriage return, U+21B5 NEW
xsc.registerEntity("lArr",xsc.CharRef(8656)) # leftwards double arrow, U+21D0 ISOtech
xsc.registerEntity("uArr",xsc.CharRef(8657)) # upwards double arrow, U+21D1 ISOamsa
xsc.registerEntity("rArr",xsc.CharRef(8658)) # rightwards double arrow, U+21D2 ISOtech
xsc.registerEntity("dArr",xsc.CharRef(8659)) # downwards double arrow, U+21D3 ISOamsa
xsc.registerEntity("hArr",xsc.CharRef(8660)) # left right double arrow, U+21D4 ISOamsa

# Mathematical Operators
xsc.registerEntity("forall",xsc.CharRef(8704)) # for all, U+2200 ISOtech
xsc.registerEntity("part",xsc.CharRef(8706)) # partial differential, U+2202 ISOtech
xsc.registerEntity("exist",xsc.CharRef(8707)) # there exists, U+2203 ISOtech
xsc.registerEntity("empty",xsc.CharRef(8709)) # empty set = null set = diameter, U+2205 ISOamso
xsc.registerEntity("nabla",xsc.CharRef(8711)) # nabla = backward difference, U+2207 ISOtech
xsc.registerEntity("isin",xsc.CharRef(8712)) # element of, U+2208 ISOtech
xsc.registerEntity("notin",xsc.CharRef(8713)) # not an element of, U+2209 ISOtech
xsc.registerEntity("ni",xsc.CharRef(8715)) # contains as member, U+220B ISOtech
xsc.registerEntity("prod",xsc.CharRef(8719)) # n-ary product = product sign, U+220F ISOamsb
xsc.registerEntity("sum",xsc.CharRef(8721)) # n-ary sumation, U+2211 ISOamsb
xsc.registerEntity("minus",xsc.CharRef(8722)) # minus sign, U+2212 ISOtech
xsc.registerEntity("lowast",xsc.CharRef(8727)) # asterisk operator, U+2217 ISOtech
xsc.registerEntity("radic",xsc.CharRef(8730)) # square root = radical sign, U+221A ISOtech
xsc.registerEntity("prop",xsc.CharRef(8733)) # proportional to, U+221D ISOtech
xsc.registerEntity("infin",xsc.CharRef(8734)) # infinity, U+221E ISOtech
xsc.registerEntity("ang",xsc.CharRef(8736)) # angle, U+2220 ISOamso
xsc.registerEntity("and",xsc.CharRef(8743)) # logical and = wedge, U+2227 ISOtech
xsc.registerEntity("or",xsc.CharRef(8744)) # logical or = vee, U+2228 ISOtech
xsc.registerEntity("cap",xsc.CharRef(8745)) # intersection = cap, U+2229 ISOtech
xsc.registerEntity("cup",xsc.CharRef(8746)) # union = cup, U+222A ISOtech
xsc.registerEntity("int",xsc.CharRef(8747)) # integral, U+222B ISOtech
xsc.registerEntity("there4",xsc.CharRef(8756)) # therefore, U+2234 ISOtech
xsc.registerEntity("sim",xsc.CharRef(8764)) # tilde operator = varies with = similar to, U+223C ISOtech
xsc.registerEntity("cong",xsc.CharRef(8773)) # approximately equal to, U+2245 ISOtech
xsc.registerEntity("asymp",xsc.CharRef(8776)) # almost equal to = asymptotic to, U+2248 ISOamsr
xsc.registerEntity("ne",xsc.CharRef(8800)) # not equal to, U+2260 ISOtech
xsc.registerEntity("equiv",xsc.CharRef(8801)) # identical to, U+2261 ISOtech
xsc.registerEntity("le",xsc.CharRef(8804)) # less-than or equal to, U+2264 ISOtech
xsc.registerEntity("ge",xsc.CharRef(8805)) # greater-than or equal to, U+2265 ISOtech
xsc.registerEntity("sub",xsc.CharRef(8834)) # subset of, U+2282 ISOtech
xsc.registerEntity("sup",xsc.CharRef(8835)) # superset of, U+2283 ISOtech
xsc.registerEntity("nsub",xsc.CharRef(8836)) # not a subset of, U+2284 ISOamsn
xsc.registerEntity("sube",xsc.CharRef(8838)) # subset of or equal to, U+2286 ISOtech
xsc.registerEntity("supe",xsc.CharRef(8839)) # superset of or equal to, U+2287 ISOtech
xsc.registerEntity("oplus",xsc.CharRef(8853)) # circled plus = direct sum, U+2295 ISOamsb
xsc.registerEntity("otimes",xsc.CharRef(8855)) # circled times = vector product, U+2297 ISOamsb
xsc.registerEntity("perp",xsc.CharRef(8869)) # up tack = orthogonal to = perpendicular, U+22A5 ISOtech
xsc.registerEntity("sdot",xsc.CharRef(8901)) # dot operator, U+22C5 ISOamsb

# Miscellaneous Technical
xsc.registerEntity("lceil",xsc.CharRef(8968)) # left ceiling = apl upstile, U+2308 ISOamsc
xsc.registerEntity("rceil",xsc.CharRef(8969)) # right ceiling, U+2309 ISOamsc
xsc.registerEntity("lfloor",xsc.CharRef(8970)) # left floor = apl downstile, U+230A ISOamsc
xsc.registerEntity("rfloor",xsc.CharRef(8971)) # right floor, U+230B ISOamsc
xsc.registerEntity("lang",xsc.CharRef(9001)) # left-pointing angle bracket = bra, U+2329 ISOtech
xsc.registerEntity("rang",xsc.CharRef(9002)) # right-pointing angle bracket = ket, U+232A ISOtech

# Geometric Shapes
xsc.registerEntity("loz",xsc.CharRef(9674)) # lozenge, U+25CA ISOpub

# Miscellaneous Symbols
xsc.registerEntity("spades",xsc.CharRef(9824)) # black spade suit, U+2660 ISOpub
xsc.registerEntity("clubs",xsc.CharRef(9827)) # black club suit = shamrock, U+2663 ISOpub
xsc.registerEntity("hearts",xsc.CharRef(9829)) # black heart suit = valentine, U+2665 ISOpub
xsc.registerEntity("diams",xsc.CharRef(9830)) # black diamond suit, U+2666 ISOpub

if __name__ == "__main__":
	xsc.make()

