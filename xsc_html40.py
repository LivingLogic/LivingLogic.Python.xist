#! /usr/bin/python

import sys
from xsc import *

# common attributes
coreattrs  = { "id" : XSCStringAttr , "class" : XSCStringAttr , "style" : XSCStringAttr , "title" : XSCStringAttr }
i18n       = { "lang" : XSCStringAttr , "dir"  : XSCStringAttr }
events     = { "onclick" : XSCStringAttr , "ondblclick" : XSCStringAttr , "onmousedown" : XSCStringAttr , "onmouseup" : XSCStringAttr , "onmouseover" : XSCStringAttr , "onmousemove" : XSCStringAttr , "onmouseout" : XSCStringAttr , "onkeypress" : XSCStringAttr , "onkeydown" : XSCStringAttr , "onkeyup" : XSCStringAttr }
attrs      = AppendDict(coreattrs,i18n,events)
cellhalign = { "align" : XSCStringAttr , "char" : XSCStringAttr , "charoff" : XSCStringAttr  }
cellvalign = { "valign" : XSCStringAttr }

# The global structure of an HTML document
class html(XSCElement):
	close = 1
	attr_handlers = i18n
handlers["html"] = html

class head(XSCElement):
	close = 1
	attr_handlers = AppendDict(i18n,{ "profile" : XSCStringAttr })
handlers["head"] = head

class title(XSCElement):
	close = 1
	attr_handlers = i18n
handlers["title"] = title

class meta(XSCElement):
	close = 0
	attr_handlers = AppendDict(i18n,{ "http-equiv" : XSCStringAttr , "name" : XSCStringAttr ,"content" : XSCStringAttr ,"scheme" : XSCStringAttr })
handlers["meta"] = meta

class body(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "onload" : XSCStringAttr , "onunload" : XSCStringAttr })
	attr_handlers = AppendDict(attr_handlers,{ "background" : XSCStringAttr , "bgcolor" : XSCStringAttr , "text" : XSCStringAttr , "link" : XSCStringAttr , "vlink" : XSCStringAttr , "alink" : XSCStringAttr , "leftmargin" : XSCStringAttr , "topmargin" : XSCStringAttr , "marginwidth" : XSCStringAttr , "marginheight" : XSCStringAttr }) # deprecated

class div(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["div"] = div

class span(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["span"] = span

class h1(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["h1"] = h1

class h2(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["h2"] = h2

class h3(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["h3"] = h3

class h4(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["h4"] = h4

class h5(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["h5"] = h5

class h6(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["h6"] = h6

class address(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["address"] = address

class bdo(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,i18n)
handlers["bdo"] = bdo

class tt(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["tt"] = tt

class i(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["i"] = i

class b(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["b"] = b

class big(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["big"] = big

class small(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["small"] = small

class em(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["em"] = em

class strong(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["strong"] = strong

class dfn(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["dfn"] = dfn

class code(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["code"] = code

class samp(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["samp"] = samp

class kbd(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["kbd"] = kbd

class var(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["var"] = var

class cite(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["cite"] = cite

class abbr(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["abbr"] = abbr

class acronym(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["acronym"] = acronym

class blockquote(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCStringAttr })
handlers["blockquote"] = blockquote

class q(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCStringAttr })
handlers["q"] = q

class sub(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["sub"] = sub

class sup(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["sup"] = sup

class p(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["p"] = p

class br(XSCElement):
	close = 0
	attr_handlers = coreattrs
handlers["br"] = br

class pre(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["pre"] = pre

class ins(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCStringAttr , "datetime" : XSCStringAttr })
handlers["ins"] = ins

class Del(XSCElement): # name clash
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCStringAttr , "datetime" : XSCStringAttr })
handlers["del"] = Del

class ul(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["ul"] = ul

class ol(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["ol"] = ol

class li(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["li"] = li

class dl(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["dl"] = dl

class dt(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["dt"] = dt

class dd(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["dd"] = dd

class table(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "summary" : XSCStringAttr ,"width" : XSCStringAttr ,"border" : XSCStringAttr ,"frame" : XSCStringAttr ,"rules" : XSCStringAttr ,"cellspacing" : XSCStringAttr ,"cellpadding" : XSCStringAttr })
	attr_handlers = AppendDict(attr_handlers,{ "height" : XSCStringAttr }) # deprecated
handlers["table"] = table

class caption(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["caption"] = caption

class thead(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
handlers["thead"] = thead

class tfoot(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
handlers["tfoot"] = tfoot

class tbody(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
handlers["tbody"] = tbody

class colgroup(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "span" : XSCStringAttr , "width" : XSCStringAttr },cellhalign,cellvalign)
handlers["colgroup"] = colgroup

class col(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "span" : XSCStringAttr , "width" : XSCStringAttr },cellhalign,cellvalign)
handlers["col"] = col

class tr(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
handlers["tr"] = tr

class th(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCStringAttr , "axis" : XSCStringAttr , "headers" : XSCStringAttr , "scope" : XSCStringAttr , "rowspan" : XSCStringAttr , "colspan" : XSCStringAttr },cellhalign,cellvalign)
handlers["th"] = th

class td(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCStringAttr , "axis" : XSCStringAttr , "headers" : XSCStringAttr , "scope" : XSCStringAttr , "rowspan" : XSCStringAttr , "colspan" : XSCStringAttr },cellhalign,cellvalign)
handlers["td"] = td

class a(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "charset" : XSCStringAttr , "type" : XSCStringAttr , "name" : XSCStringAttr , "href" : XSCURLAttr , "hreflang" : XSCStringAttr , "rel" : XSCStringAttr , "rev" : XSCStringAttr , "accesskey" : XSCStringAttr , "shape" : XSCStringAttr , "coords" : XSCStringAttr , "tabindex" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr })
handlers["a"] = a

class link(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "charset" : XSCStringAttr , "href" : XSCURLAttr , "hreflang" : XSCStringAttr , "type" : XSCStringAttr , "rel" : XSCStringAttr , "rev" : XSCStringAttr , "media" : XSCStringAttr })
handlers["link"] = link

class base(XSCElement):
	close = 0
	attr_handlers = { "href" : XSCURLAttr }
handlers["base"] = base

class img(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "src" : XSCURLAttr , "alt" : XSCStringAttr , "longdesc" : XSCStringAttr , "width" : XSCStringAttr , "height" : XSCStringAttr , "usemap" : XSCStringAttr , "ismap" : XSCStringAttr })
	attr_handlers = AppendDict(attr_handlers,{ "border" : XSCStringAttr }) # deprecated

	def AsHTML(self,xsc,mode = None):
		e = XSCElement.AsHTML(self,xsc,mode)

		xsc.AddImageSizeAttributes(e,"src")

		return e
handlers["img"] = img

class object(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "declare" : XSCStringAttr , "classid" : XSCStringAttr , "codebase" : XSCStringAttr , "data" : XSCStringAttr , "type" : XSCStringAttr , "codetype" : XSCStringAttr , "archive" : XSCStringAttr , "standby" : XSCStringAttr , "height" : XSCStringAttr , "width" : XSCStringAttr , "usemap" : XSCStringAttr , "name" : XSCStringAttr , "tabindex" : XSCStringAttr })
handlers["object"] = object

class param(XSCElement):
	close = 0
	attr_handlers = { "id" : XSCStringAttr , "name" : XSCStringAttr , "value" : XSCStringAttr , "valuetype" : XSCStringAttr , "type" : XSCStringAttr }
handlers["param"] = param

class map(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCStringAttr })
handlers["map"] = map

class area(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "shape" : XSCStringAttr , "coords" : XSCStringAttr , "href" : XSCURLAttr , "nohref" : XSCStringAttr , "alt" : XSCStringAttr , "tabindex" : XSCStringAttr , "accesskey" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr })
handlers["area"] = area

class style(XSCElement):
	close = 1
	attr_handlers = AppendDict(i18n,{ "type" : XSCStringAttr , "media" : XSCStringAttr , "title" : XSCStringAttr })
handlers["style"] = style

class hr(XSCElement):
	close = 0
	attr_handlers = AppendDict(coreattrs,events)
handlers["hr"] = hr

# The pain, the pain ...
class frameset(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "rows" : XSCStringAttr ,"cols" : XSCStringAttr ,"onload" : XSCStringAttr ,"onunload" : XSCStringAttr })
handlers["frameset"] = frameset

class frame(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCStringAttr , "name" : XSCStringAttr , "src" : XSCURLAttr , "frameborder" : XSCStringAttr , "marginwidht" : XSCStringAttr , "marginheight" : XSCStringAttr , "noresize" : XSCStringAttr , "scrolling" : XSCStringAttr })
handlers["frame"] = frame

class noframes(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["noframes"] = noframes

class iframe(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCStringAttr , "name" : XSCStringAttr , "src" : XSCURLAttr , "frameborder" : XSCStringAttr , "marginwidht" : XSCStringAttr , "marginheight" : XSCStringAttr , "noresize" : XSCStringAttr , "scrolling" : XSCStringAttr , "align" : XSCStringAttr , "height" : XSCStringAttr , "width" : XSCStringAttr })
handlers["iframe"] = iframe

class form(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "action" : XSCURLAttr , "method" : XSCStringAttr , "enctype" : XSCStringAttr , "onsubmit" : XSCStringAttr , "onreset" : XSCStringAttr , "accept-charset" : XSCStringAttr })
handlers["form"] = form

class input(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "type" : XSCStringAttr , "name" : XSCStringAttr , "value" : XSCStringAttr , "checked" : XSCStringAttr , "disabled" : XSCStringAttr , "readonly" : XSCStringAttr , "size" : XSCStringAttr , "maxlength" : XSCStringAttr , "src" : XSCURLAttr , "alt" : XSCStringAttr , "usemap" : XSCStringAttr , "tabindex" : XSCStringAttr , "accesskey" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr , "onselect" : XSCStringAttr , "onchange" : XSCStringAttr , "accept" : XSCStringAttr })
handlers["input"] = input

class button(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "name" : XSCStringAttr , "value" : XSCStringAttr , "type" : XSCStringAttr , "disabled" : XSCStringAttr , "tabindex" : XSCStringAttr , "accesskey" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr })
handlers["button"] = button

class select(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCStringAttr , "size" : XSCStringAttr , "multiple" : XSCStringAttr , "disabled" : XSCStringAttr , "tabindex" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr , "onchange" : XSCStringAttr })
handlers["select"] = select

class optgroup(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "disabled" : XSCStringAttr , "label" : XSCStringAttr })
handlers["optgroup"] = optgroup

class option(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "selected" : XSCStringAttr , "disabled" : XSCStringAttr , "label" : XSCStringAttr , "value" : XSCStringAttr })
handlers["option"] = option

class textarea(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCStringAttr , "rows" : XSCStringAttr , "cols" : XSCStringAttr , "disabled" : XSCStringAttr , "readonly" : XSCStringAttr , "tabindex" : XSCStringAttr , "accesskey" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr , "onselect" : XSCStringAttr , "onchange" : XSCStringAttr })
handlers["textarea"] = textarea

class label(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "for" : XSCStringAttr , "accesskey" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr })
handlers["label"] = label

class fieldset(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["fieldset"] = fieldset

class legend(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "accesskey" : XSCStringAttr })
handlers["legend"] = legend

class script(XSCElement):
	close = 1
	attr_handlers = { "charset" : XSCStringAttr , "type" : XSCStringAttr , "src" : XSCURLAttr , "defer" : XSCStringAttr }
handlers["script"] = script

class noscript(XSCElement):
	close = 1
	attr_handlers = attrs
handlers["noscript"] = noscript

if __name__ == "__main__":
	h = XSC(sys.argv[1])
	print str(h)

