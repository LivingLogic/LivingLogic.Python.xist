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
class XSChtml(XSCElement):
	close = 1
	attr_handlers = i18n
RegisterElement("html",XSChtml)

class XSChead(XSCElement):
	close = 1
	attr_handlers = AppendDict(i18n,{ "profile" : XSCStringAttr })
RegisterElement("head",XSChead)

class XSCtitle(XSCElement):
	close = 1
	attr_handlers = i18n
RegisterElement("title",XSCtitle)

class XSCmeta(XSCElement):
	close = 0
	attr_handlers = AppendDict(i18n,{ "http-equiv" : XSCStringAttr , "name" : XSCStringAttr ,"content" : XSCStringAttr ,"scheme" : XSCStringAttr })
RegisterElement("meta",XSCmeta)

class XSCbody(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "onload" : XSCStringAttr , "onunload" : XSCStringAttr })
	attr_handlers = AppendDict(attr_handlers,{ "background" : XSCStringAttr , "bgcolor" : XSCStringAttr , "text" : XSCStringAttr , "link" : XSCStringAttr , "vlink" : XSCStringAttr , "alink" : XSCStringAttr , "leftmargin" : XSCStringAttr , "topmargin" : XSCStringAttr , "marginwidth" : XSCStringAttr , "marginheight" : XSCStringAttr }) # deprecated
RegisterElement("body",XSCbody)

class XSCdiv(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("div",XSCdiv)

class XSCspan(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("span",XSCspan)

class XSCh1(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("h1",XSCh1)

class XSCh2(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("h2",XSCh2)

class XSCh3(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("h3",XSCh3)

class XSCh4(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("h4",XSCh4)

class XSCh5(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("h5",XSCh5)

class XSCh6(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("h6",XSCh6)

class XSCaddress(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("address",XSCaddress)

class XSCbdo(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,i18n)
RegisterElement("bdo",XSCbdo)

class XSCtt(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("tt",XSCtt)

class XSCi(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("i",XSCi)

class XSCb(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("b",XSCb)

class XSCbig(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("big",XSCbig)

class XSCsmall(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("small",XSCsmall)

class XSCem(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("em",XSCem)

class XSCstrong(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("strong",XSCstrong)

class XSCdfn(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("dfn",XSCdfn)

class XSCcode(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("code",XSCcode)

class XSCsamp(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("samp",XSCsamp)

class XSCkbd(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("kbd",XSCkbd)

class XSCvar(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("var",XSCvar)

class XSCcite(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("cite",XSCcite)

class XSCabbr(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("abbr",XSCabbr)

class XSCacronym(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("acronym",XSCacronym)

class XSCblockquote(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCStringAttr })
RegisterElement("blockquote",XSCblockquote)

class XSCq(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCStringAttr })
RegisterElement("q",XSCq)

class XSCsub(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("sub",XSCsub)

class XSCsup(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("sup",XSCsup)

class XSCp(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("p",XSCp)

class XSCbr(XSCElement):
	close = 0
	attr_handlers = coreattrs
RegisterElement("br",XSCbr)

class XSCpre(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("pre",XSCpre)

class XSCins(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCStringAttr , "datetime" : XSCStringAttr })
RegisterElement("ins",XSCins)

class XSCdel(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCStringAttr , "datetime" : XSCStringAttr })
RegisterElement("del",XSCdel)

class XSCul(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("ul",XSCul)

class XSCol(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("ol",XSCol)

class XSCli(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("li",XSCli)

class XSCdl(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("dl",XSCdl)

class XSCdt(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("dt",XSCdt)

class XSCdd(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("dd",XSCdd)

class XSCtable(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "summary" : XSCStringAttr ,"width" : XSCStringAttr ,"border" : XSCStringAttr ,"frame" : XSCStringAttr ,"rules" : XSCStringAttr ,"cellspacing" : XSCStringAttr ,"cellpadding" : XSCStringAttr })
	attr_handlers = AppendDict(attr_handlers,{ "height" : XSCStringAttr }) # deprecated
RegisterElement("table",XSCtable)

class XSCcaption(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("caption",XSCcaption)

class XSCthead(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("thead",XSCthead)

class XSCtfoot(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("tfoot",XSCtfoot)

class XSCtbody(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("tbody",XSCtbody)

class XSCcolgroup(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "span" : XSCStringAttr , "width" : XSCStringAttr },cellhalign,cellvalign)
RegisterElement("colgroup",XSCcolgroup)

class XSCcol(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "span" : XSCStringAttr , "width" : XSCStringAttr },cellhalign,cellvalign)
RegisterElement("col",XSCcol)

class XSCtr(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("tr",XSCtr)

class XSCth(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCStringAttr , "axis" : XSCStringAttr , "headers" : XSCStringAttr , "scope" : XSCStringAttr , "rowspan" : XSCStringAttr , "colspan" : XSCStringAttr },cellhalign,cellvalign)
RegisterElement("th",XSCth)

class XSCtd(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCStringAttr , "axis" : XSCStringAttr , "headers" : XSCStringAttr , "scope" : XSCStringAttr , "rowspan" : XSCStringAttr , "colspan" : XSCStringAttr },cellhalign,cellvalign)
RegisterElement("td",XSCtd)

class XSCa(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "charset" : XSCStringAttr , "type" : XSCStringAttr , "name" : XSCStringAttr , "href" : XSCURLAttr , "hreflang" : XSCStringAttr , "rel" : XSCStringAttr , "rev" : XSCStringAttr , "accesskey" : XSCStringAttr , "shape" : XSCStringAttr , "coords" : XSCStringAttr , "tabindex" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr })
RegisterElement("a",XSCa)

class XSClink(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "charset" : XSCStringAttr , "href" : XSCURLAttr , "hreflang" : XSCStringAttr , "type" : XSCStringAttr , "rel" : XSCStringAttr , "rev" : XSCStringAttr , "media" : XSCStringAttr })
RegisterElement("link",XSClink)

class XSCbase(XSCElement):
	close = 0
	attr_handlers = { "href" : XSCURLAttr }
RegisterElement("base",XSCbase)

class XSCimg(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "src" : XSCURLAttr , "alt" : XSCStringAttr , "longdesc" : XSCStringAttr , "width" : XSCStringAttr , "height" : XSCStringAttr , "usemap" : XSCStringAttr , "ismap" : XSCStringAttr })
	attr_handlers = AppendDict(attr_handlers,{ "border" : XSCStringAttr }) # deprecated

	def AsHTML(self,xsc,mode = None):
		e = XSCElement.AsHTML(self,xsc,mode)

		xsc.AddImageSizeAttributes(e,"src")

		return e
RegisterElement("img",XSCimg)

class XSCobject(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "declare" : XSCStringAttr , "classid" : XSCStringAttr , "codebase" : XSCStringAttr , "data" : XSCStringAttr , "type" : XSCStringAttr , "codetype" : XSCStringAttr , "archive" : XSCStringAttr , "standby" : XSCStringAttr , "height" : XSCStringAttr , "width" : XSCStringAttr , "usemap" : XSCStringAttr , "name" : XSCStringAttr , "tabindex" : XSCStringAttr })
RegisterElement("object",XSCobject)

class XSCparam(XSCElement):
	close = 0
	attr_handlers = { "id" : XSCStringAttr , "name" : XSCStringAttr , "value" : XSCStringAttr , "valuetype" : XSCStringAttr , "type" : XSCStringAttr }
RegisterElement("param",XSCparam)

class XSCmap(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCStringAttr })
RegisterElement("map",XSCmap)

class XSCarea(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "shape" : XSCStringAttr , "coords" : XSCStringAttr , "href" : XSCURLAttr , "nohref" : XSCStringAttr , "alt" : XSCStringAttr , "tabindex" : XSCStringAttr , "accesskey" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr })
RegisterElement("area",XSCarea)

class XSCstyle(XSCElement):
	close = 1
	attr_handlers = AppendDict(i18n,{ "type" : XSCStringAttr , "media" : XSCStringAttr , "title" : XSCStringAttr })
RegisterElement("style",XSCstyle)

class XSChr(XSCElement):
	close = 0
	attr_handlers = AppendDict(coreattrs,events)
RegisterElement("hr",XSChr)

# The pain, the pain ...
class XSCframeset(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "rows" : XSCStringAttr ,"cols" : XSCStringAttr ,"onload" : XSCStringAttr ,"onunload" : XSCStringAttr })
RegisterElement("frameset",XSCframeset)

class XSCframe(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCStringAttr , "name" : XSCStringAttr , "src" : XSCURLAttr , "frameborder" : XSCStringAttr , "marginwidht" : XSCStringAttr , "marginheight" : XSCStringAttr , "noresize" : XSCStringAttr , "scrolling" : XSCStringAttr })
RegisterElement("frame",XSCframe)

class XSCnoframes(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("noframes",XSCnoframes)

class XSCiframe(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCStringAttr , "name" : XSCStringAttr , "src" : XSCURLAttr , "frameborder" : XSCStringAttr , "marginwidht" : XSCStringAttr , "marginheight" : XSCStringAttr , "noresize" : XSCStringAttr , "scrolling" : XSCStringAttr , "align" : XSCStringAttr , "height" : XSCStringAttr , "width" : XSCStringAttr })
RegisterElement("iframe",XSCiframe)

class XSCform(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "action" : XSCURLAttr , "method" : XSCStringAttr , "enctype" : XSCStringAttr , "onsubmit" : XSCStringAttr , "onreset" : XSCStringAttr , "accept-charset" : XSCStringAttr })
RegisterElement("form",XSCform)

class XSCinput(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "type" : XSCStringAttr , "name" : XSCStringAttr , "value" : XSCStringAttr , "checked" : XSCStringAttr , "disabled" : XSCStringAttr , "readonly" : XSCStringAttr , "size" : XSCStringAttr , "maxlength" : XSCStringAttr , "src" : XSCURLAttr , "alt" : XSCStringAttr , "usemap" : XSCStringAttr , "tabindex" : XSCStringAttr , "accesskey" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr , "onselect" : XSCStringAttr , "onchange" : XSCStringAttr , "accept" : XSCStringAttr })
RegisterElement("input",XSCinput)

class XSCbutton(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "name" : XSCStringAttr , "value" : XSCStringAttr , "type" : XSCStringAttr , "disabled" : XSCStringAttr , "tabindex" : XSCStringAttr , "accesskey" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr })
RegisterElement("button",XSCbutton)

class XSCselect(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCStringAttr , "size" : XSCStringAttr , "multiple" : XSCStringAttr , "disabled" : XSCStringAttr , "tabindex" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr , "onchange" : XSCStringAttr })
RegisterElement("select",XSCselect)

class XSCoptgroup(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "disabled" : XSCStringAttr , "label" : XSCStringAttr })
RegisterElement("optgroup",XSCoptgroup)

class XSCoption(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "selected" : XSCStringAttr , "disabled" : XSCStringAttr , "label" : XSCStringAttr , "value" : XSCStringAttr })
RegisterElement("option",XSCoption)

class XSCtextarea(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCStringAttr , "rows" : XSCStringAttr , "cols" : XSCStringAttr , "disabled" : XSCStringAttr , "readonly" : XSCStringAttr , "tabindex" : XSCStringAttr , "accesskey" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr , "onselect" : XSCStringAttr , "onchange" : XSCStringAttr })
RegisterElement("textarea",XSCtextarea)

class XSClabel(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "for" : XSCStringAttr , "accesskey" : XSCStringAttr , "onfocus" : XSCStringAttr , "onblur" : XSCStringAttr })
RegisterElement("label",XSClabel)

class XSCfieldset(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("fieldset",XSCfieldset)

class XSClegend(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "accesskey" : XSCStringAttr })
RegisterElement("legend",XSClegend)

class XSCscript(XSCElement):
	close = 1
	attr_handlers = { "charset" : XSCStringAttr , "type" : XSCStringAttr , "src" : XSCURLAttr , "defer" : XSCStringAttr }
RegisterElement("script",XSCscript)

class XSCnoscript(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("noscript",XSCnoscript)

if __name__ == "__main__":
	h = XSC(sys.argv[1])
	print str(h)

