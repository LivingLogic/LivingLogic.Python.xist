#! /usr/bin/env python

"""
A XSC module that contains definition for all the elements in HTML 4.0 transitional
(and a few additional ones).
"""

__version__ = "$Revision$"
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

# The global structure of an HTML document
class html(xsc.Element):
	"""
	document root element
	"""
	empty = 0
	attrHandlers = i18n
xsc.registerElement(html)

class head(xsc.Element):
	"""
	document head
	"""
	empty = 0
	attrHandlers = xsc.appendDict(i18n,{ "profile" : xsc.TextAttr })
xsc.registerElement(head)

class title(xsc.Element):
	"""
	document title
	"""
	empty = 0
	attrHandlers = i18n
xsc.registerElement(title)

class meta(xsc.Element):
	"""
	generic metainformation
	"""
	empty = 1
	attrHandlers = xsc.appendDict(i18n,{ "http_equiv" : xsc.TextAttr , "http-equiv" : xsc.TextAttr , "name" : xsc.TextAttr ,"content" : xsc.TextAttr ,"scheme" : xsc.TextAttr })

	def __init__(self,_content = [],_attrs = {},**_restattrs):
		# we have two names for one and the same attribute http_equiv and http-equiv
		apply(xsc.Element.__init__,(self,_content,_attrs),_restattrs)
		if self.has_attr("http_equiv"):
			if not self.has_attr("http-equiv"):
				self["http-equiv"] = self["http_equiv"]
			del self["http_equiv"]
xsc.registerElement(meta)

class body(xsc.Element):
	"""
	document body
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "onload" : xsc.TextAttr , "onunload" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "background" : xsc.URLAttr , "bgcolor" : xsc.ColorAttr , "text" : xsc.ColorAttr , "link" : xsc.ColorAttr , "vlink" : xsc.ColorAttr , "alink" : xsc.ColorAttr , "leftmargin" : xsc.TextAttr , "topmargin" : xsc.TextAttr , "marginwidth" : xsc.TextAttr , "marginheight" : xsc.TextAttr }) # deprecated
xsc.registerElement(body)

class div(xsc.Element):
	"""
	generic language/style container
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(div)

class span(xsc.Element):
	"""
	generic language/style container
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(span)

class h1(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h1)

class h2(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h2)

class h3(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h3)

class h4(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h4)

class h5(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h5)

class h6(xsc.Element):
	"""
	heading
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrHandlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h6)

class address(xsc.Element):
	"""
	information on author
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(address)

class bdo(xsc.Element):
	"""
	I18N BiDi over-ride
	"""
	empty = 0
	attrHandlers = xsc.appendDict(coreattrs,i18n)
xsc.registerElement(bdo)

class tt(xsc.Element):
	"""
	teletype or monospaced text style
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(tt)

class i(xsc.Element):
	"""
	italic text style
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(i)

class b(xsc.Element):
	"""
	bold text style
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(b)

class big(xsc.Element):
	"""
	large text style
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(big)

class small(xsc.Element):
	"""
	small text style
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(small)

class em(xsc.Element):
	"""
	emphasis
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(em)

class strong(xsc.Element):
	"""
	strong emphasis
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(strong)

class dfn(xsc.Element):
	"""
	instance definition
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(dfn)

class code(xsc.Element):
	"""
	computer code fragment
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(code)

class samp(xsc.Element):
	"""
	sample program output, scripts, etc.
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(samp)

class kbd(xsc.Element):
	"""
	text to be entered by the user
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(kbd)

class var(xsc.Element):
	"""
	instance of a variable or program argument
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(var)

class cite(xsc.Element):
	"""
	citation
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(cite)

class abbr(xsc.Element):
	"""
	abbreviated form (e.g., WWW, HTTP, etc.)
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(abbr)

class acronym(xsc.Element):
	"""
	acronym
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(acronym)

class blockquote(xsc.Element):
	"""
	long quotation
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr })
xsc.registerElement(blockquote)

class q(xsc.Element):
	"""
	short inline quotation
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr })
xsc.registerElement(q)

class sub(xsc.Element):
	"""
	subscript
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(sub)

class sup(xsc.Element):
	"""
	superscript
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(sup)

class p(xsc.Element):
	"""
	paragraph
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict({ "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(p)

class br(xsc.Element):
	"""
	forced line break
	"""
	empty = 1
	attrHandlers = coreattrs
xsc.registerElement(br)

class pre(xsc.Element):
	"""
	preformatted text
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(pre)

class ins(xsc.Element):
	"""
	inserted text
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr , "datetime" : xsc.TextAttr })
xsc.registerElement(ins)

class Del(xsc.Element):
	"""
	deleted text
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr , "datetime" : xsc.TextAttr })
xsc.registerElement(Del)

class ul(xsc.Element):
	"""
	unordered list
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr }) # deprecated
xsc.registerElement(ul)

class ol(xsc.Element):
	"""
	ordered list
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr }) # deprecated
xsc.registerElement(ol)

class li(xsc.Element):
	"""
	list item
	"""
	empty = 0
	attrHandlers = attrs
	attrHandlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr }) # deprecated
xsc.registerElement(li)

class dl(xsc.Element):
	"""
	definition list
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(dl)

class dt(xsc.Element):
	"""
	definition term
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(dt)

class dd(xsc.Element):
	"""
	definition description
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(dd)

class table(xsc.Element):
	"""
	table
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "summary" : xsc.TextAttr ,"width" : xsc.TextAttr ,"border" : xsc.TextAttr ,"frame" : xsc.TextAttr ,"rules" : xsc.TextAttr ,"cellspacing" : xsc.TextAttr ,"cellpadding" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "height" : xsc.TextAttr , "align" : xsc.TextAttr , "bgcolor" : xsc.ColorAttr }) # deprecated
xsc.registerElement(table)

class caption(xsc.Element):
	"""
	table caption
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(caption)

class thead(xsc.Element):
	"""
	table header
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,cellhalign,cellvalign)
xsc.registerElement(thead)

class tfoot(xsc.Element):
	"""
	table footer
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,cellhalign,cellvalign)
xsc.registerElement(tfoot)

class tbody(xsc.Element):
	"""
	table body
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,cellhalign,cellvalign)
xsc.registerElement(tbody)

class colgroup(xsc.Element):
	"""
	table column group
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "span" : xsc.TextAttr , "width" : xsc.TextAttr },cellhalign,cellvalign)
xsc.registerElement(colgroup)

class col(xsc.Element):
	"""
	table column
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "span" : xsc.TextAttr , "width" : xsc.TextAttr },cellhalign,cellvalign)
xsc.registerElement(col)

class tr(xsc.Element):
	"""
	table row
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,cellhalign,cellvalign)
	attrHandlers = xsc.appendDict(attrHandlers,{ "nowrap" : xsc.TextAttr , "bgcolor" : xsc.ColorAttr , "width" : xsc.TextAttr }) # deprecated
xsc.registerElement(tr)

class th(xsc.Element):
	"""
	table header cell
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "abbr" : xsc.TextAttr , "axis" : xsc.TextAttr , "headers" : xsc.TextAttr , "scope" : xsc.TextAttr , "rowspan" : xsc.TextAttr , "colspan" : xsc.TextAttr },cellhalign,cellvalign)
xsc.registerElement(th)

class td(xsc.Element):
	"""
	table data cell
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "abbr" : xsc.TextAttr , "axis" : xsc.TextAttr , "headers" : xsc.TextAttr , "scope" : xsc.TextAttr , "rowspan" : xsc.TextAttr , "colspan" : xsc.TextAttr },cellhalign,cellvalign)
	attrHandlers = xsc.appendDict(attrHandlers,{ "nowrap" : xsc.TextAttr , "bgcolor" : xsc.ColorAttr , "width" : xsc.TextAttr }) # deprecated
xsc.registerElement(td)

class a(xsc.Element):
	"""
	anchor
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "charset" : xsc.TextAttr , "type" : xsc.TextAttr , "name" : xsc.TextAttr , "href" : xsc.URLAttr , "hreflang" : xsc.TextAttr , "rel" : xsc.TextAttr , "rev" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "shape" : xsc.TextAttr , "coords" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "target" : xsc.TextAttr }) # deprecated
xsc.registerElement(a)

class link(xsc.Element):
	"""
	a media-independent link
	"""
	empty = 1
	attrHandlers = xsc.appendDict(attrs,{ "charset" : xsc.TextAttr , "href" : xsc.URLAttr , "hreflang" : xsc.TextAttr , "type" : xsc.TextAttr , "rel" : xsc.TextAttr , "rev" : xsc.TextAttr , "media" : xsc.TextAttr })
xsc.registerElement(link)

class base(xsc.Element):
	"""
	document base URI
	"""
	empty = 1
	attrHandlers = { "href" : xsc.URLAttr }
xsc.registerElement(base)

class img(xsc.Element):
	"""
	Embedded image
	"""
	empty = 1
	attrHandlers = xsc.appendDict(attrs,{ "src" : xsc.URLAttr , "alt" : xsc.TextAttr , "longdesc" : xsc.TextAttr , "width" : xsc.TextAttr , "height" : xsc.TextAttr , "usemap" : xsc.TextAttr , "ismap" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "name" : xsc.TextAttr , "border" : xsc.TextAttr , "align" : xsc.TextAttr , "hspace" : xsc.TextAttr , "vspace" : xsc.TextAttr , "lowsrc" : xsc.URLAttr }) # deprecated

	def asHTML(self):
		e = self.clone()
		e.AddImageSizeAttributes("src")

		return e
xsc.registerElement(img)

class object(xsc.Element):
	"""
	generic embedded object
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "declare" : xsc.TextAttr , "classid" : xsc.TextAttr , "codebase" : xsc.TextAttr , "data" : xsc.TextAttr , "type" : xsc.TextAttr , "codetype" : xsc.TextAttr , "archive" : xsc.TextAttr , "standby" : xsc.TextAttr , "height" : xsc.TextAttr , "width" : xsc.TextAttr , "usemap" : xsc.TextAttr , "name" : xsc.TextAttr , "tabindex" : xsc.TextAttr })
xsc.registerElement(object)

class param(xsc.Element):
	"""
	named property value
	"""
	empty = 1
	attrHandlers = { "id" : xsc.TextAttr , "name" : xsc.TextAttr , "value" : xsc.TextAttr , "valuetype" : xsc.TextAttr , "type" : xsc.TextAttr }
xsc.registerElement(param)

class map(xsc.Element):
	"""
	client-side image map
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr })
xsc.registerElement(map)

class area(xsc.Element):
	"""
	client-side image map area
	"""
	empty = 1
	attrHandlers = xsc.appendDict(attrs,{ "shape" : xsc.TextAttr , "coords" : xsc.TextAttr , "href" : xsc.URLAttr , "nohref" : xsc.TextAttr , "alt" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })
xsc.registerElement(area)

class style(xsc.Element):
	"""
	style info
	"""
	empty = 0
	attrHandlers = xsc.appendDict(i18n,{ "type" : xsc.TextAttr , "media" : xsc.TextAttr , "title" : xsc.TextAttr })
xsc.registerElement(style)

class hr(xsc.Element):
	"""
	horizontal rule
	"""
	empty = 1
	attrHandlers = xsc.appendDict(coreattrs,events)
xsc.registerElement(hr)

# The pain, the pain ...
class frameset(xsc.Element):
	"""
	window subdivision
	"""
	empty = 0
	attrHandlers = xsc.appendDict(coreattrs,{ "rows" : xsc.TextAttr ,"cols" : xsc.TextAttr ,"onload" : xsc.TextAttr ,"onunload" : xsc.TextAttr })
xsc.registerElement(frameset)

class frame(xsc.Element):
	"""
	subwindow
	"""
	empty = 0
	attrHandlers = xsc.appendDict(coreattrs,{ "longdesc" : xsc.TextAttr , "name" : xsc.TextAttr , "src" : xsc.URLAttr , "frameborder" : xsc.TextAttr , "marginwidht" : xsc.TextAttr , "marginheight" : xsc.TextAttr , "noresize" : xsc.TextAttr , "scrolling" : xsc.TextAttr })
xsc.registerElement(frame)

class noframes(xsc.Element):
	"""
	alternate content container for non frame-based rendering
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(noframes)

class iframe(xsc.Element):
	"""
	inline subwindow
	"""
	empty = 0
	attrHandlers = xsc.appendDict(coreattrs,{ "longdesc" : xsc.TextAttr , "name" : xsc.TextAttr , "src" : xsc.URLAttr , "frameborder" : xsc.TextAttr , "marginwidht" : xsc.TextAttr , "marginheight" : xsc.TextAttr , "noresize" : xsc.TextAttr , "scrolling" : xsc.TextAttr , "align" : xsc.TextAttr , "height" : xsc.TextAttr , "width" : xsc.TextAttr })
xsc.registerElement(iframe)

class form(xsc.Element):
	"""
	interactive form
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "action" : xsc.URLAttr , "method" : xsc.TextAttr , "enctype" : xsc.TextAttr , "onsubmit" : xsc.TextAttr , "onreset" : xsc.TextAttr , "accept-charset" : xsc.TextAttr })
xsc.registerElement(form)

class input(xsc.Element):
	"""
	form control
	"""
	empty = 1
	attrHandlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr , "name" : xsc.TextAttr , "value" : xsc.TextAttr , "checked" : xsc.TextAttr , "disabled" : xsc.TextAttr , "readonly" : xsc.TextAttr , "size" : xsc.TextAttr , "maxlength" : xsc.TextAttr , "src" : xsc.URLAttr , "alt" : xsc.TextAttr , "usemap" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr , "onselect" : xsc.TextAttr , "onchange" : xsc.TextAttr , "accept" : xsc.TextAttr })
xsc.registerElement(input)

class button(xsc.Element):
	"""
	push button
	"""
	empty = 1
	attrHandlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr , "value" : xsc.TextAttr , "type" : xsc.TextAttr , "disabled" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })
xsc.registerElement(button)

class select(xsc.Element):
	"""
	option selector
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr , "size" : xsc.TextAttr , "multiple" : xsc.TextAttr , "disabled" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr , "onchange" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "rows" : xsc.TextAttr }) # deprecated
xsc.registerElement(select)

class optgroup(xsc.Element):
	"""
	option group
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "disabled" : xsc.TextAttr , "label" : xsc.TextAttr })
xsc.registerElement(optgroup)

class option(xsc.Element):
	"""
	selectable choice
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "selected" : xsc.TextAttr , "disabled" : xsc.TextAttr , "label" : xsc.TextAttr , "value" : xsc.TextAttr })
xsc.registerElement(option)

class textarea(xsc.Element):
	"""
	multi-line text field
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr , "rows" : xsc.TextAttr , "cols" : xsc.TextAttr , "disabled" : xsc.TextAttr , "readonly" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr , "onselect" : xsc.TextAttr , "onchange" : xsc.TextAttr })
	attrHandlers = xsc.appendDict(attrHandlers,{ "wrap" : xsc.TextAttr })
xsc.registerElement(textarea)

class label(xsc.Element):
	"""
	form field label text
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "for" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })
xsc.registerElement(label)

class fieldset(xsc.Element):
	"""
	form control group
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(fieldset)

class legend(xsc.Element):
	"""
	fieldset legend
	"""
	empty = 0
	attrHandlers = xsc.appendDict(attrs,{ "accesskey" : xsc.TextAttr })
xsc.registerElement(legend)

class script(xsc.Element):
	"""
	script statements
	"""
	empty = 0
	attrHandlers = { "charset" : xsc.TextAttr , "type" : xsc.TextAttr , "src" : xsc.URLAttr , "defer" : xsc.TextAttr }
	attrHandlers = xsc.appendDict(attrHandlers,{ "language" : xsc.TextAttr }) # deprecated
xsc.registerElement(script)

class noscript(xsc.Element):
	"""
	alternate content container for non script-based rendering
	"""
	empty = 0
	attrHandlers = attrs
xsc.registerElement(noscript)

# More pain
class font(xsc.Element): # deprecated
	"""
	local change to font
	"""
	empty = 0
	attrHandlers = { "face" : xsc.TextAttr , "size" : xsc.TextAttr , "color" : xsc.ColorAttr }
xsc.registerElement(font)

class applet(xsc.Element): # deprecated
	"""
	Java applet
	"""
	empty = 0
	attrHandlers = { "archive" : xsc.URLAttr , "code" : xsc.URLAttr , "width" : xsc.TextAttr , "height" : xsc.TextAttr }
xsc.registerElement(applet)

if __name__ == "__main__":
	xsc.make()

