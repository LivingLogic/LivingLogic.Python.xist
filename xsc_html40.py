#! /usr/bin/env python

import sys
from xsc import *

# common attributes
coreattrs  = { "id" : XSCFrag , "class" : XSCFrag , "style" : XSCFrag , "title" : XSCFrag }
i18n       = { "lang" : XSCFrag , "dir"  : XSCFrag }
events     = { "onclick" : XSCFrag , "ondblclick" : XSCFrag , "onmousedown" : XSCFrag , "onmouseup" : XSCFrag , "onmouseover" : XSCFrag , "onmousemove" : XSCFrag , "onmouseout" : XSCFrag , "onkeypress" : XSCFrag , "onkeydown" : XSCFrag , "onkeyup" : XSCFrag }
attrs      = AppendDict(coreattrs,i18n,events)
cellhalign = { "align" : XSCFrag , "char" : XSCFrag , "charoff" : XSCFrag  }
cellvalign = { "valign" : XSCFrag }

# The global structure of an HTML document
class html(XSCElement):
	empty = 0
	attr_handlers = i18n
RegisterElement("html",html)

class head(XSCElement):
	empty = 0
	attr_handlers = AppendDict(i18n,{ "profile" : XSCFrag })
RegisterElement("head",head)

class title(XSCElement):
	empty = 0
	attr_handlers = i18n
RegisterElement("title",title)

class meta(XSCElement):
	empty = 1
	attr_handlers = AppendDict(i18n,{ "http_equiv" : XSCFrag , "http-equiv" : XSCFrag , "name" : XSCFrag ,"content" : XSCFrag ,"scheme" : XSCFrag })

	def __init__(self,content = [],attrs = {},**restattrs):
		# we have two names for one and the same attribute http_equiv and http-equiv
		apply(XSCElement.__init__,(self,content,attrs),restattrs)
		if self.has_attr("http_equiv"):
			if not self.has_attr("http-equiv"):
				self["http-equiv"] = self["http_equiv"]
			del self["http_equiv"]
RegisterElement("meta",meta)

class body(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "onload" : XSCFrag , "onunload" : XSCFrag })
	attr_handlers = AppendDict(attr_handlers,{ "background" : XSCFrag , "bgcolor" : XSCFrag , "text" : XSCFrag , "link" : XSCFrag , "vlink" : XSCFrag , "alink" : XSCFrag , "leftmargin" : XSCFrag , "topmargin" : XSCFrag , "marginwidth" : XSCFrag , "marginheight" : XSCFrag }) # deprecated
RegisterElement("body",body)

class div(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("div",div)

class span(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("span",span)

class h1(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h1",h1)

class h2(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h2",h2)

class h3(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h3",h3)

class h4(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h4",h4)

class h5(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h5",h5)

class h6(XSCElement):
	empty = 0
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
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
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag })
RegisterElement("blockquote",blockquote)

class q(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag })
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
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag , "datetime" : XSCFrag })
RegisterElement("ins",ins)

class del_(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag , "datetime" : XSCFrag })
RegisterElement("del",del_)

class ul(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("ul",ul)

class ol(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("ol",ol)

class li(XSCElement):
	empty = 0
	attr_handlers = attrs
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
	attr_handlers = AppendDict(attrs,{ "summary" : XSCFrag ,"width" : XSCFrag ,"border" : XSCFrag ,"frame" : XSCFrag ,"rules" : XSCFrag ,"cellspacing" : XSCFrag ,"cellpadding" : XSCFrag })
	attr_handlers = AppendDict(attr_handlers,{ "height" : XSCFrag }) # deprecated
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
	attr_handlers = AppendDict(attrs,{ "span" : XSCFrag , "width" : XSCFrag },cellhalign,cellvalign)
RegisterElement("colgroup",colgroup)

class col(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "span" : XSCFrag , "width" : XSCFrag },cellhalign,cellvalign)
RegisterElement("col",col)

class tr(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("tr",tr)

class th(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCFrag , "axis" : XSCFrag , "headers" : XSCFrag , "scope" : XSCFrag , "rowspan" : XSCFrag , "colspan" : XSCFrag },cellhalign,cellvalign)
RegisterElement("th",th)

class td(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCFrag , "axis" : XSCFrag , "headers" : XSCFrag , "scope" : XSCFrag , "rowspan" : XSCFrag , "colspan" : XSCFrag },cellhalign,cellvalign)
	attr_handlers = AppendDict(attr_handlers,{ "nowrap" : XSCFrag , "bgcolor" : XSCFrag , "width" : XSCFrag }) # deprecated
RegisterElement("td",td)

class a(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "charset" : XSCFrag , "type" : XSCFrag , "name" : XSCFrag , "href" : XSCurl , "hreflang" : XSCFrag , "rel" : XSCFrag , "rev" : XSCFrag , "accesskey" : XSCFrag , "shape" : XSCFrag , "coords" : XSCFrag , "tabindex" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
	attr_handlers = AppendDict(attr_handlers,{ "target" : XSCFrag }) # deprecated
RegisterElement("a",a)

class link(XSCElement):
	empty = 1
	attr_handlers = AppendDict(attrs,{ "charset" : XSCFrag , "href" : XSCurl , "hreflang" : XSCFrag , "type" : XSCFrag , "rel" : XSCFrag , "rev" : XSCFrag , "media" : XSCFrag })
RegisterElement("link",link)

class base(XSCElement):
	empty = 1
	attr_handlers = { "href" : XSCurl }
RegisterElement("base",base)

class img(XSCElement):
	empty = 1
	attr_handlers = AppendDict(attrs,{ "src" : XSCurl , "alt" : XSCFrag , "longdesc" : XSCFrag , "width" : XSCFrag , "height" : XSCFrag , "usemap" : XSCFrag , "ismap" : XSCFrag })
	attr_handlers = AppendDict(attr_handlers,{ "border" : XSCFrag , "align" : XSCFrag , "hspace" : XSCFrag , "vspace" : XSCFrag }) # deprecated

	def __str__(self):
		e = img(self.content,self.attrs)
		e.AddImageSizeAttributes("src")

		return e
RegisterElement("img",img)

class object(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "declare" : XSCFrag , "classid" : XSCFrag , "codebase" : XSCFrag , "data" : XSCFrag , "type" : XSCFrag , "codetype" : XSCFrag , "archive" : XSCFrag , "standby" : XSCFrag , "height" : XSCFrag , "width" : XSCFrag , "usemap" : XSCFrag , "name" : XSCFrag , "tabindex" : XSCFrag })
RegisterElement("object",object)

class param(XSCElement):
	empty = 1
	attr_handlers = { "id" : XSCFrag , "name" : XSCFrag , "value" : XSCFrag , "valuetype" : XSCFrag , "type" : XSCFrag }
RegisterElement("param",param)

class map(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag })
RegisterElement("map",map)

class area(XSCElement):
	empty = 1
	attr_handlers = AppendDict(attrs,{ "shape" : XSCFrag , "coords" : XSCFrag , "href" : XSCurl , "nohref" : XSCFrag , "alt" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("area",area)

class style(XSCElement):
	empty = 0
	attr_handlers = AppendDict(i18n,{ "type" : XSCFrag , "media" : XSCFrag , "title" : XSCFrag })
RegisterElement("style",style)

class hr(XSCElement):
	empty = 1
	attr_handlers = AppendDict(coreattrs,events)
RegisterElement("hr",hr)

# The pain, the pain ...
class frameset(XSCElement):
	empty = 0
	attr_handlers = AppendDict(coreattrs,{ "rows" : XSCFrag ,"cols" : XSCFrag ,"onload" : XSCFrag ,"onunload" : XSCFrag })
RegisterElement("frameset",frameset)

class frame(XSCElement):
	empty = 0
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCFrag , "name" : XSCFrag , "src" : XSCurl , "frameborder" : XSCFrag , "marginwidht" : XSCFrag , "marginheight" : XSCFrag , "noresize" : XSCFrag , "scrolling" : XSCFrag })
RegisterElement("frame",frame)

class noframes(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("noframes",noframes)

class iframe(XSCElement):
	empty = 0
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCFrag , "name" : XSCFrag , "src" : XSCurl , "frameborder" : XSCFrag , "marginwidht" : XSCFrag , "marginheight" : XSCFrag , "noresize" : XSCFrag , "scrolling" : XSCFrag , "align" : XSCFrag , "height" : XSCFrag , "width" : XSCFrag })
RegisterElement("iframe",iframe)

class form(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "action" : XSCurl , "method" : XSCFrag , "enctype" : XSCFrag , "onsubmit" : XSCFrag , "onreset" : XSCFrag , "accept-charset" : XSCFrag })
RegisterElement("form",form)

class input(XSCElement):
	empty = 1
	attr_handlers = AppendDict(attrs,{ "type" : XSCFrag , "name" : XSCFrag , "value" : XSCFrag , "checked" : XSCFrag , "disabled" : XSCFrag , "readonly" : XSCFrag , "size" : XSCFrag , "maxlength" : XSCFrag , "src" : XSCurl , "alt" : XSCFrag , "usemap" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag , "onselect" : XSCFrag , "onchange" : XSCFrag , "accept" : XSCFrag })
RegisterElement("input",input)

class button(XSCElement):
	empty = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag , "value" : XSCFrag , "type" : XSCFrag , "disabled" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("button",button)

class select(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag , "size" : XSCFrag , "multiple" : XSCFrag , "disabled" : XSCFrag , "tabindex" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag , "onchange" : XSCFrag })
RegisterElement("select",select)

class optgroup(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "disabled" : XSCFrag , "label" : XSCFrag })
RegisterElement("optgroup",optgroup)

class option(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "selected" : XSCFrag , "disabled" : XSCFrag , "label" : XSCFrag , "value" : XSCFrag })
RegisterElement("option",option)

class textarea(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag , "rows" : XSCFrag , "cols" : XSCFrag , "disabled" : XSCFrag , "readonly" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag , "onselect" : XSCFrag , "onchange" : XSCFrag })
RegisterElement("textarea",textarea)

class label(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "for" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("label",label)

class fieldset(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("fieldset",fieldset)

class legend(XSCElement):
	empty = 0
	attr_handlers = AppendDict(attrs,{ "accesskey" : XSCFrag })
RegisterElement("legend",legend)

class script(XSCElement):
	empty = 0
	attr_handlers = { "charset" : XSCFrag , "type" : XSCFrag , "src" : XSCurl , "defer" : XSCFrag }
RegisterElement("script",script)

class noscript(XSCElement):
	empty = 0
	attr_handlers = attrs
RegisterElement("noscript",noscript)

if __name__ == "__main__":
	try:
		print str(xsc.parseFile(sys.argv[1]).asHTML())
	except XSCError,e:
		print str(e)


