#! /usr/bin/env python

""""""

__version__ = "$Revision$"
# $Source$

import sys
from xsc import *

# common attributes
coreattrs  = { "id" : XSCTextAttr , "class" : XSCTextAttr , "style" : XSCTextAttr , "title" : XSCTextAttr }
i18n       = { "lang" : XSCTextAttr , "dir"  : XSCTextAttr }
events     = { "onclick" : XSCTextAttr , "ondblclick" : XSCTextAttr , "onmousedown" : XSCTextAttr , "onmouseup" : XSCTextAttr , "onmouseover" : XSCTextAttr , "onmousemove" : XSCTextAttr , "onmouseout" : XSCTextAttr , "onkeypress" : XSCTextAttr , "onkeydown" : XSCTextAttr , "onkeyup" : XSCTextAttr }
attrs      = AppendDict(coreattrs,i18n,events)
cellhalign = { "align" : XSCTextAttr , "char" : XSCTextAttr , "charoff" : XSCTextAttr  }
cellvalign = { "valign" : XSCTextAttr }

# The global structure of an HTML document
class html(XSCElement):
	empty = 0
	attr_handlers = i18n
RegisterElement("html",html)

class head(XSCElement):
	empty = 0
	attr_handlers = AppendDict(i18n,{ "profile" : XSCTextAttr })
RegisterElement("head",head)

class title(XSCElement):
	empty = 0
	attr_handlers = i18n
RegisterElement("title",title)

class meta(XSCElement):
	empty = 1
	attr_handlers = AppendDict(i18n,{ "http_equiv" : XSCTextAttr , "http-equiv" : XSCTextAttr , "name" : XSCTextAttr ,"content" : XSCTextAttr ,"scheme" : XSCTextAttr })

	def __init__(self,_content = [],_attrs = {},**_restattrs):
		# we have two names for one and the same attribute http_equiv and http-equiv
		apply(XSCElement.__init__,(self,_content,_attrs),_restattrs)
		if self.has_attr("http_equiv"):
			if not self.has_attr("http-equiv"):
				self["http-equiv"] = self["http_equiv"]
			del self["http_equiv"]
RegisterElement("meta",meta)

class body(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "onload" : XSCTextAttr , "onunload" : XSCTextAttr })
	attr_handlers = AppendDict(attr_handlers,{ "background" : XSCURLAttr , "bgcolor" : XSCColorAttr , "text" : XSCColorAttr , "link" : XSCColorAttr , "vlink" : XSCColorAttr , "alink" : XSCColorAttr , "leftmargin" : XSCTextAttr , "topmargin" : XSCTextAttr , "marginwidth" : XSCTextAttr , "marginheight" : XSCTextAttr }) # deprecated
RegisterElement("body",body)

class div(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCTextAttr }) # deprecated
RegisterElement("div",div)

class span(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("span",span)

class h1(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCTextAttr }) # deprecated
RegisterElement("h1",h1)

class h2(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCTextAttr }) # deprecated
RegisterElement("h2",h2)

class h3(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCTextAttr }) # deprecated
RegisterElement("h3",h3)

class h4(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCTextAttr }) # deprecated
RegisterElement("h4",h4)

class h5(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCTextAttr }) # deprecated
RegisterElement("h5",h5)

class h6(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCTextAttr }) # deprecated
RegisterElement("h6",h6)

class address(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("address",address)

class bdo(XSCElement):
	empty = 0
	attr_handlers = AppendDict(coreattrs,i18n)
RegisterElement("bdo",bdo)

class tt(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("tt",tt)

class i(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("i",i)

class b(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("b",b)

class big(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("big",big)

class small(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("small",small)

class em(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("em",em)

class strong(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("strong",strong)

class dfn(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("dfn",dfn)

class code(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("code",code)

class samp(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("samp",samp)

class kbd(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("kbd",kbd)

class var(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("var",var)

class cite(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("cite",cite)

class abbr(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("abbr",abbr)

class acronym(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("acronym",acronym)

class blockquote(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "cite" : XSCTextAttr })
RegisterElement("blockquote",blockquote)

class q(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "cite" : XSCTextAttr })
RegisterElement("q",q)

class sub(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("sub",sub)

class sup(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("sup",sup)

class p(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict({ "align" : XSCTextAttr }) # deprecated
RegisterElement("p",p)

class br(XSCElement):
	empty = 1
	attr_handlers = coreattrs
RegisterElement("br",br)

class pre(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("pre",pre)

class ins(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "cite" : XSCTextAttr , "datetime" : XSCTextAttr })
RegisterElement("ins",ins)

class del_(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "cite" : XSCTextAttr , "datetime" : XSCTextAttr })
RegisterElement("del",del_)

class ul(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attrs,{ "type" : XSCTextAttr }) # deprecated
RegisterElement("ul",ul)

class ol(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attrs,{ "type" : XSCTextAttr }) # deprecated
RegisterElement("ol",ol)

class li(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attrs,{ "type" : XSCTextAttr }) # deprecated
RegisterElement("li",li)

class dl(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("dl",dl)

class dt(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("dt",dt)

class dd(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("dd",dd)

class table(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "summary" : XSCTextAttr ,"width" : XSCTextAttr ,"border" : XSCTextAttr ,"frame" : XSCTextAttr ,"rules" : XSCTextAttr ,"cellspacing" : XSCTextAttr ,"cellpadding" : XSCTextAttr })
	attr_handlers = AppendDict(attr_handlers,{ "height" : XSCTextAttr , "align" : XSCTextAttr , "bgcolor" : XSCColorAttr }) # deprecated
RegisterElement("table",table)

class caption(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("caption",caption)

class thead(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("thead",thead)

class tfoot(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("tfoot",tfoot)

class tbody(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("tbody",tbody)

class colgroup(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "span" : XSCTextAttr , "width" : XSCTextAttr },cellhalign,cellvalign)
RegisterElement("colgroup",colgroup)

class col(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "span" : XSCTextAttr , "width" : XSCTextAttr },cellhalign,cellvalign)
RegisterElement("col",col)

class tr(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
	attr_handlers = AppendDict(attr_handlers,{ "nowrap" : XSCTextAttr , "bgcolor" : XSCColorAttr , "width" : XSCTextAttr }) # deprecated
RegisterElement("tr",tr)

class th(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCTextAttr , "axis" : XSCTextAttr , "headers" : XSCTextAttr , "scope" : XSCTextAttr , "rowspan" : XSCTextAttr , "colspan" : XSCTextAttr },cellhalign,cellvalign)
RegisterElement("th",th)

class td(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCTextAttr , "axis" : XSCTextAttr , "headers" : XSCTextAttr , "scope" : XSCTextAttr , "rowspan" : XSCTextAttr , "colspan" : XSCTextAttr },cellhalign,cellvalign)
	attr_handlers = AppendDict(attr_handlers,{ "nowrap" : XSCTextAttr , "bgcolor" : XSCColorAttr , "width" : XSCTextAttr }) # deprecated
RegisterElement("td",td)

class a(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "charset" : XSCTextAttr , "type" : XSCTextAttr , "name" : XSCTextAttr , "href" : XSCURLAttr , "hreflang" : XSCTextAttr , "rel" : XSCTextAttr , "rev" : XSCTextAttr , "accesskey" : XSCTextAttr , "shape" : XSCTextAttr , "coords" : XSCTextAttr , "tabindex" : XSCTextAttr , "onfocus" : XSCTextAttr , "onblur" : XSCTextAttr })
	attr_handlers = AppendDict(attr_handlers,{ "target" : XSCTextAttr }) # deprecated
RegisterElement("a",a)

class link(XSCElement):
	empty = 1
	attr_handlers = AppendDict(attrs,{ "charset" : XSCTextAttr , "href" : XSCURLAttr , "hreflang" : XSCTextAttr , "type" : XSCTextAttr , "rel" : XSCTextAttr , "rev" : XSCTextAttr , "media" : XSCTextAttr })
RegisterElement("link",link)

class base(XSCElement):
	empty = 1
	attr_handlers = { "href" : XSCURLAttr }
RegisterElement("base",base)

class img(XSCElement):
	empty = 1
	attr_handlers = AppendDict(attrs,{ "src" : XSCURLAttr , "alt" : XSCTextAttr , "longdesc" : XSCTextAttr , "width" : XSCTextAttr , "height" : XSCTextAttr , "usemap" : XSCTextAttr , "ismap" : XSCTextAttr })
	attr_handlers = AppendDict(attr_handlers,{ "name" : XSCTextAttr , "border" : XSCTextAttr , "align" : XSCTextAttr , "hspace" : XSCTextAttr , "vspace" : XSCTextAttr , "lowsrc" : XSCURLAttr }) # deprecated

	def asHTML(self):
		e = img(self.content.asHTML(),self.attrs.asHTML())
		e.AddImageSizeAttributes("src")

		return e
RegisterElement("img",img)

class object(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "declare" : XSCTextAttr , "classid" : XSCTextAttr , "codebase" : XSCTextAttr , "data" : XSCTextAttr , "type" : XSCTextAttr , "codetype" : XSCTextAttr , "archive" : XSCTextAttr , "standby" : XSCTextAttr , "height" : XSCTextAttr , "width" : XSCTextAttr , "usemap" : XSCTextAttr , "name" : XSCTextAttr , "tabindex" : XSCTextAttr })
RegisterElement("object",object)

class param(XSCElement):
	empty = 1
	attr_handlers = { "id" : XSCTextAttr , "name" : XSCTextAttr , "value" : XSCTextAttr , "valuetype" : XSCTextAttr , "type" : XSCTextAttr }
RegisterElement("param",param)

class map(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "name" : XSCTextAttr })
RegisterElement("map",map)

class area(XSCElement):
	empty = 1
	attr_handlers = AppendDict(attrs,{ "shape" : XSCTextAttr , "coords" : XSCTextAttr , "href" : XSCURLAttr , "nohref" : XSCTextAttr , "alt" : XSCTextAttr , "tabindex" : XSCTextAttr , "accesskey" : XSCTextAttr , "onfocus" : XSCTextAttr , "onblur" : XSCTextAttr })
RegisterElement("area",area)

class style(XSCElement):
	empty = 0
	attr_handlers = AppendDict(i18n,{ "type" : XSCTextAttr , "media" : XSCTextAttr , "title" : XSCTextAttr })
RegisterElement("style",style)

class hr(XSCElement):
	empty = 1
	attr_handlers = AppendDict(coreattrs,events)
RegisterElement("hr",hr)

# The pain, the pain ...
class frameset(XSCElement):
	empty = 0
	attr_handlers = AppendDict(coreattrs,{ "rows" : XSCTextAttr ,"cols" : XSCTextAttr ,"onload" : XSCTextAttr ,"onunload" : XSCTextAttr })
RegisterElement("frameset",frameset)

class frame(XSCElement):
	empty = 0
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCTextAttr , "name" : XSCTextAttr , "src" : XSCURLAttr , "frameborder" : XSCTextAttr , "marginwidht" : XSCTextAttr , "marginheight" : XSCTextAttr , "noresize" : XSCTextAttr , "scrolling" : XSCTextAttr })
RegisterElement("frame",frame)

class noframes(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("noframes",noframes)

class iframe(XSCElement):
	empty = 0
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCTextAttr , "name" : XSCTextAttr , "src" : XSCURLAttr , "frameborder" : XSCTextAttr , "marginwidht" : XSCTextAttr , "marginheight" : XSCTextAttr , "noresize" : XSCTextAttr , "scrolling" : XSCTextAttr , "align" : XSCTextAttr , "height" : XSCTextAttr , "width" : XSCTextAttr })
RegisterElement("iframe",iframe)

class form(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "action" : XSCURLAttr , "method" : XSCTextAttr , "enctype" : XSCTextAttr , "onsubmit" : XSCTextAttr , "onreset" : XSCTextAttr , "accept-charset" : XSCTextAttr })
RegisterElement("form",form)

class input(XSCElement):
	empty = 1
	attr_handlers = AppendDict(attrs,{ "type" : XSCTextAttr , "name" : XSCTextAttr , "value" : XSCTextAttr , "checked" : XSCTextAttr , "disabled" : XSCTextAttr , "readonly" : XSCTextAttr , "size" : XSCTextAttr , "maxlength" : XSCTextAttr , "src" : XSCURLAttr , "alt" : XSCTextAttr , "usemap" : XSCTextAttr , "tabindex" : XSCTextAttr , "accesskey" : XSCTextAttr , "onfocus" : XSCTextAttr , "onblur" : XSCTextAttr , "onselect" : XSCTextAttr , "onchange" : XSCTextAttr , "accept" : XSCTextAttr })
RegisterElement("input",input)

class button(XSCElement):
	empty = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCTextAttr , "value" : XSCTextAttr , "type" : XSCTextAttr , "disabled" : XSCTextAttr , "tabindex" : XSCTextAttr , "accesskey" : XSCTextAttr , "onfocus" : XSCTextAttr , "onblur" : XSCTextAttr })
RegisterElement("button",button)

class select(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "name" : XSCTextAttr , "size" : XSCTextAttr , "multiple" : XSCTextAttr , "disabled" : XSCTextAttr , "tabindex" : XSCTextAttr , "onfocus" : XSCTextAttr , "onblur" : XSCTextAttr , "onchange" : XSCTextAttr })
	attr_handlers = AppendDict(attr_handlers,{ "rows" : XSCTextAttr }) # deprecated
RegisterElement("select",select)

class optgroup(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "disabled" : XSCTextAttr , "label" : XSCTextAttr })
RegisterElement("optgroup",optgroup)

class option(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "selected" : XSCTextAttr , "disabled" : XSCTextAttr , "label" : XSCTextAttr , "value" : XSCTextAttr })
RegisterElement("option",option)

class textarea(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "name" : XSCTextAttr , "rows" : XSCTextAttr , "cols" : XSCTextAttr , "disabled" : XSCTextAttr , "readonly" : XSCTextAttr , "tabindex" : XSCTextAttr , "accesskey" : XSCTextAttr , "onfocus" : XSCTextAttr , "onblur" : XSCTextAttr , "onselect" : XSCTextAttr , "onchange" : XSCTextAttr })
RegisterElement("textarea",textarea)

class label(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "for" : XSCTextAttr , "accesskey" : XSCTextAttr , "onfocus" : XSCTextAttr , "onblur" : XSCTextAttr })
RegisterElement("label",label)

class fieldset(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("fieldset",fieldset)

class legend(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "accesskey" : XSCTextAttr })
RegisterElement("legend",legend)

class script(XSCElement):
	empty = 0
	attr_handlers = { "charset" : XSCTextAttr , "type" : XSCTextAttr , "src" : XSCURLAttr , "defer" : XSCTextAttr }
	attr_handlers = AppendDict(attr_handlers,{ "language" : XSCTextAttr }) # deprecated
RegisterElement("script",script)

class noscript(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("noscript",noscript)

# More pain
class font(XSCElement): # deprecated
	empty = 0
	attr_handlers = { "face" : XSCTextAttr , "size" : XSCTextAttr , "color" : XSCColorAttr }
RegisterElement("font",font)

class applet(XSCElement): # deprecated
	empty = 0
	attr_handlers = { "archive" : XSCURLAttr , "code" : XSCURLAttr , "width" : XSCTextAttr , "height" : XSCTextAttr }
RegisterElement("applet",applet)

if __name__ == "__main__":
	make(sys.argv)

