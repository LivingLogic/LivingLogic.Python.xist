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
	empty = 0
	attr_handlers = i18n
xsc.registerElement(html)

class head(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(i18n,{ "profile" : xsc.TextAttr })
xsc.registerElement(head)

class title(xsc.Element):
	empty = 0
	attr_handlers = i18n
xsc.registerElement(title)

class meta(xsc.Element):
	empty = 1
	attr_handlers = xsc.appendDict(i18n,{ "http_equiv" : xsc.TextAttr , "http-equiv" : xsc.TextAttr , "name" : xsc.TextAttr ,"content" : xsc.TextAttr ,"scheme" : xsc.TextAttr })

	def __init__(self,_content = [],_attrs = {},**_restattrs):
		# we have two names for one and the same attribute http_equiv and http-equiv
		apply(xsc.Element.__init__,(self,_content,_attrs),_restattrs)
		if self.has_attr("http_equiv"):
			if not self.has_attr("http-equiv"):
				self["http-equiv"] = self["http_equiv"]
			del self["http_equiv"]
xsc.registerElement(meta)

class body(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "onload" : xsc.TextAttr , "onunload" : xsc.TextAttr })
	attr_handlers = xsc.appendDict(attr_handlers,{ "background" : xsc.URLAttr , "bgcolor" : xsc.ColorAttr , "text" : xsc.ColorAttr , "link" : xsc.ColorAttr , "vlink" : xsc.ColorAttr , "alink" : xsc.ColorAttr , "leftmargin" : xsc.TextAttr , "topmargin" : xsc.TextAttr , "marginwidth" : xsc.TextAttr , "marginheight" : xsc.TextAttr }) # deprecated
xsc.registerElement(body)

class div(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict(attr_handlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(div)

class span(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(span)

class h1(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict(attr_handlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h1)

class h2(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict(attr_handlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h2)

class h3(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict(attr_handlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h3)

class h4(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict(attr_handlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h4)

class h5(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict(attr_handlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h5)

class h6(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict(attr_handlers, { "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(h6)

class address(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(address)

class bdo(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(coreattrs,i18n)
xsc.registerElement(bdo)

class tt(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(tt)

class i(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(i)

class b(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(b)

class big(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(big)

class small(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(small)

class em(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(em)

class strong(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(strong)

class dfn(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(dfn)

class code(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(code)

class samp(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(samp)

class kbd(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(kbd)

class var(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(var)

class cite(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(cite)

class abbr(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(abbr)

class acronym(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(acronym)

class blockquote(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr })
xsc.registerElement(blockquote)

class q(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr })
xsc.registerElement(q)

class sub(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(sub)

class sup(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(sup)

class p(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict({ "align" : xsc.TextAttr }) # deprecated
xsc.registerElement(p)

class br(xsc.Element):
	empty = 1
	attr_handlers = coreattrs
xsc.registerElement(br)

class pre(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(pre)

class ins(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr , "datetime" : xsc.TextAttr })
xsc.registerElement(ins)

class Del(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "cite" : xsc.TextAttr , "datetime" : xsc.TextAttr })
xsc.registerElement(Del)

class ul(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr }) # deprecated
xsc.registerElement(ul)

class ol(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr }) # deprecated
xsc.registerElement(ol)

class li(xsc.Element):
	empty = 0
	attr_handlers = attrs
	attr_handlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr }) # deprecated
xsc.registerElement(li)

class dl(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(dl)

class dt(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(dt)

class dd(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(dd)

class table(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "summary" : xsc.TextAttr ,"width" : xsc.TextAttr ,"border" : xsc.TextAttr ,"frame" : xsc.TextAttr ,"rules" : xsc.TextAttr ,"cellspacing" : xsc.TextAttr ,"cellpadding" : xsc.TextAttr })
	attr_handlers = xsc.appendDict(attr_handlers,{ "height" : xsc.TextAttr , "align" : xsc.TextAttr , "bgcolor" : xsc.ColorAttr }) # deprecated
xsc.registerElement(table)

class caption(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(caption)

class thead(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,cellhalign,cellvalign)
xsc.registerElement(thead)

class tfoot(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,cellhalign,cellvalign)
xsc.registerElement(tfoot)

class tbody(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,cellhalign,cellvalign)
xsc.registerElement(tbody)

class colgroup(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "span" : xsc.TextAttr , "width" : xsc.TextAttr },cellhalign,cellvalign)
xsc.registerElement(colgroup)

class col(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "span" : xsc.TextAttr , "width" : xsc.TextAttr },cellhalign,cellvalign)
xsc.registerElement(col)

class tr(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,cellhalign,cellvalign)
	attr_handlers = xsc.appendDict(attr_handlers,{ "nowrap" : xsc.TextAttr , "bgcolor" : xsc.ColorAttr , "width" : xsc.TextAttr }) # deprecated
xsc.registerElement(tr)

class th(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "abbr" : xsc.TextAttr , "axis" : xsc.TextAttr , "headers" : xsc.TextAttr , "scope" : xsc.TextAttr , "rowspan" : xsc.TextAttr , "colspan" : xsc.TextAttr },cellhalign,cellvalign)
xsc.registerElement(th)

class td(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "abbr" : xsc.TextAttr , "axis" : xsc.TextAttr , "headers" : xsc.TextAttr , "scope" : xsc.TextAttr , "rowspan" : xsc.TextAttr , "colspan" : xsc.TextAttr },cellhalign,cellvalign)
	attr_handlers = xsc.appendDict(attr_handlers,{ "nowrap" : xsc.TextAttr , "bgcolor" : xsc.ColorAttr , "width" : xsc.TextAttr }) # deprecated
xsc.registerElement(td)

class a(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "charset" : xsc.TextAttr , "type" : xsc.TextAttr , "name" : xsc.TextAttr , "href" : xsc.URLAttr , "hreflang" : xsc.TextAttr , "rel" : xsc.TextAttr , "rev" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "shape" : xsc.TextAttr , "coords" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })
	attr_handlers = xsc.appendDict(attr_handlers,{ "target" : xsc.TextAttr }) # deprecated
xsc.registerElement(a)

class link(xsc.Element):
	empty = 1
	attr_handlers = xsc.appendDict(attrs,{ "charset" : xsc.TextAttr , "href" : xsc.URLAttr , "hreflang" : xsc.TextAttr , "type" : xsc.TextAttr , "rel" : xsc.TextAttr , "rev" : xsc.TextAttr , "media" : xsc.TextAttr })
xsc.registerElement(link)

class base(xsc.Element):
	empty = 1
	attr_handlers = { "href" : xsc.URLAttr }
xsc.registerElement(base)

class img(xsc.Element):
	empty = 1
	attr_handlers = xsc.appendDict(attrs,{ "src" : xsc.URLAttr , "alt" : xsc.TextAttr , "longdesc" : xsc.TextAttr , "width" : xsc.TextAttr , "height" : xsc.TextAttr , "usemap" : xsc.TextAttr , "ismap" : xsc.TextAttr })
	attr_handlers = xsc.appendDict(attr_handlers,{ "name" : xsc.TextAttr , "border" : xsc.TextAttr , "align" : xsc.TextAttr , "hspace" : xsc.TextAttr , "vspace" : xsc.TextAttr , "lowsrc" : xsc.URLAttr }) # deprecated

	def asHTML(self):
		e = self.clone()
		e.AddImageSizeAttributes("src")

		return e
xsc.registerElement(img)

class object(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "declare" : xsc.TextAttr , "classid" : xsc.TextAttr , "codebase" : xsc.TextAttr , "data" : xsc.TextAttr , "type" : xsc.TextAttr , "codetype" : xsc.TextAttr , "archive" : xsc.TextAttr , "standby" : xsc.TextAttr , "height" : xsc.TextAttr , "width" : xsc.TextAttr , "usemap" : xsc.TextAttr , "name" : xsc.TextAttr , "tabindex" : xsc.TextAttr })
xsc.registerElement(object)

class param(xsc.Element):
	empty = 1
	attr_handlers = { "id" : xsc.TextAttr , "name" : xsc.TextAttr , "value" : xsc.TextAttr , "valuetype" : xsc.TextAttr , "type" : xsc.TextAttr }
xsc.registerElement(param)

class map(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr })
xsc.registerElement(map)

class area(xsc.Element):
	empty = 1
	attr_handlers = xsc.appendDict(attrs,{ "shape" : xsc.TextAttr , "coords" : xsc.TextAttr , "href" : xsc.URLAttr , "nohref" : xsc.TextAttr , "alt" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })
xsc.registerElement(area)

class style(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(i18n,{ "type" : xsc.TextAttr , "media" : xsc.TextAttr , "title" : xsc.TextAttr })
xsc.registerElement(style)

class hr(xsc.Element):
	empty = 1
	attr_handlers = xsc.appendDict(coreattrs,events)
xsc.registerElement(hr)

# The pain, the pain ...
class frameset(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(coreattrs,{ "rows" : xsc.TextAttr ,"cols" : xsc.TextAttr ,"onload" : xsc.TextAttr ,"onunload" : xsc.TextAttr })
xsc.registerElement(frameset)

class frame(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(coreattrs,{ "longdesc" : xsc.TextAttr , "name" : xsc.TextAttr , "src" : xsc.URLAttr , "frameborder" : xsc.TextAttr , "marginwidht" : xsc.TextAttr , "marginheight" : xsc.TextAttr , "noresize" : xsc.TextAttr , "scrolling" : xsc.TextAttr })
xsc.registerElement(frame)

class noframes(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(noframes)

class iframe(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(coreattrs,{ "longdesc" : xsc.TextAttr , "name" : xsc.TextAttr , "src" : xsc.URLAttr , "frameborder" : xsc.TextAttr , "marginwidht" : xsc.TextAttr , "marginheight" : xsc.TextAttr , "noresize" : xsc.TextAttr , "scrolling" : xsc.TextAttr , "align" : xsc.TextAttr , "height" : xsc.TextAttr , "width" : xsc.TextAttr })
xsc.registerElement(iframe)

class form(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "action" : xsc.URLAttr , "method" : xsc.TextAttr , "enctype" : xsc.TextAttr , "onsubmit" : xsc.TextAttr , "onreset" : xsc.TextAttr , "accept-charset" : xsc.TextAttr })
xsc.registerElement(form)

class input(xsc.Element):
	empty = 1
	attr_handlers = xsc.appendDict(attrs,{ "type" : xsc.TextAttr , "name" : xsc.TextAttr , "value" : xsc.TextAttr , "checked" : xsc.TextAttr , "disabled" : xsc.TextAttr , "readonly" : xsc.TextAttr , "size" : xsc.TextAttr , "maxlength" : xsc.TextAttr , "src" : xsc.URLAttr , "alt" : xsc.TextAttr , "usemap" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr , "onselect" : xsc.TextAttr , "onchange" : xsc.TextAttr , "accept" : xsc.TextAttr })
xsc.registerElement(input)

class button(xsc.Element):
	empty = 1
	attr_handlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr , "value" : xsc.TextAttr , "type" : xsc.TextAttr , "disabled" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })
xsc.registerElement(button)

class select(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr , "size" : xsc.TextAttr , "multiple" : xsc.TextAttr , "disabled" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr , "onchange" : xsc.TextAttr })
	attr_handlers = xsc.appendDict(attr_handlers,{ "rows" : xsc.TextAttr }) # deprecated
xsc.registerElement(select)

class optgroup(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "disabled" : xsc.TextAttr , "label" : xsc.TextAttr })
xsc.registerElement(optgroup)

class option(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "selected" : xsc.TextAttr , "disabled" : xsc.TextAttr , "label" : xsc.TextAttr , "value" : xsc.TextAttr })
xsc.registerElement(option)

class textarea(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "name" : xsc.TextAttr , "rows" : xsc.TextAttr , "cols" : xsc.TextAttr , "disabled" : xsc.TextAttr , "readonly" : xsc.TextAttr , "tabindex" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr , "onselect" : xsc.TextAttr , "onchange" : xsc.TextAttr })
xsc.registerElement(textarea)

class label(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "for" : xsc.TextAttr , "accesskey" : xsc.TextAttr , "onfocus" : xsc.TextAttr , "onblur" : xsc.TextAttr })
xsc.registerElement(label)

class fieldset(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(fieldset)

class legend(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(attrs,{ "accesskey" : xsc.TextAttr })
xsc.registerElement(legend)

class script(xsc.Element):
	empty = 0
	attr_handlers = { "charset" : xsc.TextAttr , "type" : xsc.TextAttr , "src" : xsc.URLAttr , "defer" : xsc.TextAttr }
	attr_handlers = xsc.appendDict(attr_handlers,{ "language" : xsc.TextAttr }) # deprecated
xsc.registerElement(script)

class noscript(xsc.Element):
	empty = 0
	attr_handlers = attrs
xsc.registerElement(noscript)

# More pain
class font(xsc.Element): # deprecated
	empty = 0
	attr_handlers = { "face" : xsc.TextAttr , "size" : xsc.TextAttr , "color" : xsc.ColorAttr }
xsc.registerElement(font)

class applet(xsc.Element): # deprecated
	empty = 0
	attr_handlers = { "archive" : xsc.URLAttr , "code" : xsc.URLAttr , "width" : xsc.TextAttr , "height" : xsc.TextAttr }
xsc.registerElement(applet)

if __name__ == "__main__":
	xsc.make()

