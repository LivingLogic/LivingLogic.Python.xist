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
	close = 1
	attr_handlers = i18n
RegisterElement("html",html)

class head(XSCElement):
	close = 1
	attr_handlers = AppendDict(i18n,{ "profile" : XSCFrag })
RegisterElement("head",head)

class title(XSCElement):
	close = 1
	attr_handlers = i18n
RegisterElement("title",title)

class meta(XSCElement):
	close = 0
	attr_handlers = AppendDict(i18n,{ "http-equiv" : XSCFrag , "name" : XSCFrag ,"content" : XSCFrag ,"scheme" : XSCFrag })
RegisterElement("meta",meta)

class body(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "onload" : XSCFrag , "onunload" : XSCFrag })
	attr_handlers = AppendDict(attr_handlers,{ "background" : XSCFrag , "bgcolor" : XSCFrag , "text" : XSCFrag , "link" : XSCFrag , "vlink" : XSCFrag , "alink" : XSCFrag , "leftmargin" : XSCFrag , "topmargin" : XSCFrag , "marginwidth" : XSCFrag , "marginheight" : XSCFrag }) # deprecated
RegisterElement("body",body)

class div(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("div",div)

class span(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("span",span)

class h1(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h1",h1)

class h2(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h2",h2)

class h3(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h3",h3)

class h4(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h4",h4)

class h5(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h5",h5)

class h6(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h6",h6)

class address(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("address",address)

class bdo(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,i18n)
RegisterElement("bdo",bdo)

class tt(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("tt",tt)

class i(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("i",i)

class b(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("b",b)

class big(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("big",big)

class small(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("small",small)

class em(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("em",em)

class strong(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("strong",strong)

class dfn(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("dfn",dfn)

class code(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("code",code)

class samp(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("samp",samp)

class kbd(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("kbd",kbd)

class var(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("var",var)

class cite(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("cite",cite)

class abbr(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("abbr",abbr)

class acronym(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("acronym",acronym)

class blockquote(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag })
RegisterElement("blockquote",blockquote)

class q(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag })
RegisterElement("q",q)

class sub(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("sub",sub)

class sup(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("sup",sup)

class p(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("p",p)

class br(XSCElement):
	close = 0
	attr_handlers = coreattrs
RegisterElement("br",br)

class pre(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("pre",pre)

class ins(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag , "datetime" : XSCFrag })
RegisterElement("ins",ins)

class del(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag , "datetime" : XSCFrag })
RegisterElement("del",del)

class ul(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("ul",ul)

class ol(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("ol",ol)

class li(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("li",li)

class dl(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("dl",dl)

class dt(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("dt",dt)

class dd(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("dd",dd)

class table(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "summary" : XSCFrag ,"width" : XSCFrag ,"border" : XSCFrag ,"frame" : XSCFrag ,"rules" : XSCFrag ,"cellspacing" : XSCFrag ,"cellpadding" : XSCFrag })
	attr_handlers = AppendDict(attr_handlers,{ "height" : XSCFrag }) # deprecated
RegisterElement("table",table)

class caption(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("caption",caption)

class thead(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("thead",thead)

class tfoot(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("tfoot",tfoot)

class tbody(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("tbody",tbody)

class colgroup(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "span" : XSCFrag , "width" : XSCFrag },cellhalign,cellvalign)
RegisterElement("colgroup",colgroup)

class col(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "span" : XSCFrag , "width" : XSCFrag },cellhalign,cellvalign)
RegisterElement("col",col)

class tr(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("tr",tr)

class th(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCFrag , "axis" : XSCFrag , "headers" : XSCFrag , "scope" : XSCFrag , "rowspan" : XSCFrag , "colspan" : XSCFrag },cellhalign,cellvalign)
RegisterElement("th",th)

class td(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCFrag , "axis" : XSCFrag , "headers" : XSCFrag , "scope" : XSCFrag , "rowspan" : XSCFrag , "colspan" : XSCFrag },cellhalign,cellvalign)
	attr_handlers = AppendDict(attr_handlers,{ "nowrap" : XSCFrag , "bgcolor" : XSCFrag , "width" : XSCFrag }) # deprecated
RegisterElement("td",td)

class a(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "charset" : XSCFrag , "type" : XSCFrag , "name" : XSCFrag , "href" : XSCurl , "hreflang" : XSCFrag , "rel" : XSCFrag , "rev" : XSCFrag , "accesskey" : XSCFrag , "shape" : XSCFrag , "coords" : XSCFrag , "tabindex" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("a",a)

class link(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "charset" : XSCFrag , "href" : XSCurl , "hreflang" : XSCFrag , "type" : XSCFrag , "rel" : XSCFrag , "rev" : XSCFrag , "media" : XSCFrag })
RegisterElement("link",link)

class base(XSCElement):
	close = 0
	attr_handlers = { "href" : XSCurl }
RegisterElement("base",base)

class img(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "src" : XSCurl , "alt" : XSCFrag , "longdesc" : XSCFrag , "width" : XSCFrag , "height" : XSCFrag , "usemap" : XSCFrag , "ismap" : XSCFrag })
	attr_handlers = AppendDict(attr_handlers,{ "border" : XSCFrag , "align" : XSCFrag , "hspace" : XSCFrag , "vspace" : XSCFrag }) # deprecated

	def __str__(self):
		e = XSCimg(self.content,self.attrs)
		e.AddImageSizeAttributes("src")

		return XSCElement.__str__(e)
RegisterElement("img",img)

class object(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "declare" : XSCFrag , "classid" : XSCFrag , "codebase" : XSCFrag , "data" : XSCFrag , "type" : XSCFrag , "codetype" : XSCFrag , "archive" : XSCFrag , "standby" : XSCFrag , "height" : XSCFrag , "width" : XSCFrag , "usemap" : XSCFrag , "name" : XSCFrag , "tabindex" : XSCFrag })
RegisterElement("object",object)

class param(XSCElement):
	close = 0
	attr_handlers = { "id" : XSCFrag , "name" : XSCFrag , "value" : XSCFrag , "valuetype" : XSCFrag , "type" : XSCFrag }
RegisterElement("param",param)

class map(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag })
RegisterElement("map",map)

class area(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "shape" : XSCFrag , "coords" : XSCFrag , "href" : XSCurl , "nohref" : XSCFrag , "alt" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("area",area)

class style(XSCElement):
	close = 1
	attr_handlers = AppendDict(i18n,{ "type" : XSCFrag , "media" : XSCFrag , "title" : XSCFrag })
RegisterElement("style",style)

class hr(XSCElement):
	close = 0
	attr_handlers = AppendDict(coreattrs,events)
RegisterElement("hr",hr)

# The pain, the pain ...
class frameset(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "rows" : XSCFrag ,"cols" : XSCFrag ,"onload" : XSCFrag ,"onunload" : XSCFrag })
RegisterElement("frameset",frameset)

class frame(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCFrag , "name" : XSCFrag , "src" : XSCurl , "frameborder" : XSCFrag , "marginwidht" : XSCFrag , "marginheight" : XSCFrag , "noresize" : XSCFrag , "scrolling" : XSCFrag })
RegisterElement("frame",frame)

class noframes(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("noframes",noframes)

class iframe(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCFrag , "name" : XSCFrag , "src" : XSCurl , "frameborder" : XSCFrag , "marginwidht" : XSCFrag , "marginheight" : XSCFrag , "noresize" : XSCFrag , "scrolling" : XSCFrag , "align" : XSCFrag , "height" : XSCFrag , "width" : XSCFrag })
RegisterElement("iframe",iframe)

class form(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "action" : XSCurl , "method" : XSCFrag , "enctype" : XSCFrag , "onsubmit" : XSCFrag , "onreset" : XSCFrag , "accept-charset" : XSCFrag })
RegisterElement("form",form)

class input(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "type" : XSCFrag , "name" : XSCFrag , "value" : XSCFrag , "checked" : XSCFrag , "disabled" : XSCFrag , "readonly" : XSCFrag , "size" : XSCFrag , "maxlength" : XSCFrag , "src" : XSCurl , "alt" : XSCFrag , "usemap" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag , "onselect" : XSCFrag , "onchange" : XSCFrag , "accept" : XSCFrag })
RegisterElement("input",input)

class button(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag , "value" : XSCFrag , "type" : XSCFrag , "disabled" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("button",button)

class select(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag , "size" : XSCFrag , "multiple" : XSCFrag , "disabled" : XSCFrag , "tabindex" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag , "onchange" : XSCFrag })
RegisterElement("select",select)

class optgroup(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "disabled" : XSCFrag , "label" : XSCFrag })
RegisterElement("optgroup",optgroup)

class option(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "selected" : XSCFrag , "disabled" : XSCFrag , "label" : XSCFrag , "value" : XSCFrag })
RegisterElement("option",option)

class textarea(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag , "rows" : XSCFrag , "cols" : XSCFrag , "disabled" : XSCFrag , "readonly" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag , "onselect" : XSCFrag , "onchange" : XSCFrag })
RegisterElement("textarea",textarea)

class label(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "for" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("label",label)

class fieldset(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("fieldset",fieldset)

class legend(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "accesskey" : XSCFrag })
RegisterElement("legend",legend)

class script(XSCElement):
	close = 1
	attr_handlers = { "charset" : XSCFrag , "type" : XSCFrag , "src" : XSCurl , "defer" : XSCFrag }
RegisterElement("script",script)

class noscript(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("noscript",noscript)

if __name__ == "__main__":
	try:
		print str(xsc.arsefile(sys.argv[1]))
	except XSCError,e:
		print str(e)


