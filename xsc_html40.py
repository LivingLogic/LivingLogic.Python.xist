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
class XSChtml(XSCElement):
	close = 1
	attr_handlers = i18n
RegisterElement("html",XSChtml)

class XSChead(XSCElement):
	close = 1
	attr_handlers = AppendDict(i18n,{ "profile" : XSCFrag })
RegisterElement("head",XSChead)

class XSCtitle(XSCElement):
	close = 1
	attr_handlers = i18n
RegisterElement("title",XSCtitle)

class XSCmeta(XSCElement):
	close = 0
	attr_handlers = AppendDict(i18n,{ "http-equiv" : XSCFrag , "name" : XSCFrag ,"content" : XSCFrag ,"scheme" : XSCFrag })
RegisterElement("meta",XSCmeta)

class XSCbody(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "onload" : XSCFrag , "onunload" : XSCFrag })
	attr_handlers = AppendDict(attr_handlers,{ "background" : XSCFrag , "bgcolor" : XSCFrag , "text" : XSCFrag , "link" : XSCFrag , "vlink" : XSCFrag , "alink" : XSCFrag , "leftmargin" : XSCFrag , "topmargin" : XSCFrag , "marginwidth" : XSCFrag , "marginheight" : XSCFrag }) # deprecated
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
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h1",XSCh1)

class XSCh2(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h2",XSCh2)

class XSCh3(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h3",XSCh3)

class XSCh4(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h4",XSCh4)

class XSCh5(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
RegisterElement("h5",XSCh5)

class XSCh6(XSCElement):
	close = 1
	attr_handlers = attrs
	attr_handlers = AppendDict(attr_handlers, { "align" : XSCFrag }) # deprecated
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
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag })
RegisterElement("blockquote",XSCblockquote)

class XSCq(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag })
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
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag , "datetime" : XSCFrag })
RegisterElement("ins",XSCins)

class XSCdel(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "cite" : XSCFrag , "datetime" : XSCFrag })
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
	attr_handlers = AppendDict(attrs,{ "summary" : XSCFrag ,"width" : XSCFrag ,"border" : XSCFrag ,"frame" : XSCFrag ,"rules" : XSCFrag ,"cellspacing" : XSCFrag ,"cellpadding" : XSCFrag })
	attr_handlers = AppendDict(attr_handlers,{ "height" : XSCFrag }) # deprecated
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
	attr_handlers = AppendDict(attrs,{ "span" : XSCFrag , "width" : XSCFrag },cellhalign,cellvalign)
RegisterElement("colgroup",XSCcolgroup)

class XSCcol(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "span" : XSCFrag , "width" : XSCFrag },cellhalign,cellvalign)
RegisterElement("col",XSCcol)

class XSCtr(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,cellhalign,cellvalign)
RegisterElement("tr",XSCtr)

class XSCth(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCFrag , "axis" : XSCFrag , "headers" : XSCFrag , "scope" : XSCFrag , "rowspan" : XSCFrag , "colspan" : XSCFrag },cellhalign,cellvalign)
RegisterElement("th",XSCth)

class XSCtd(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "abbr" : XSCFrag , "axis" : XSCFrag , "headers" : XSCFrag , "scope" : XSCFrag , "rowspan" : XSCFrag , "colspan" : XSCFrag },cellhalign,cellvalign)
	attr_handlers = AppendDict(attr_handlers,{ "nowrap" : XSCFrag , "bgcolor" : XSCFrag , "width" : XSCFrag }) # deprecated
RegisterElement("td",XSCtd)

class XSCa(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "charset" : XSCFrag , "type" : XSCFrag , "name" : XSCFrag , "href" : XSCurl , "hreflang" : XSCFrag , "rel" : XSCFrag , "rev" : XSCFrag , "accesskey" : XSCFrag , "shape" : XSCFrag , "coords" : XSCFrag , "tabindex" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("a",XSCa)

class XSClink(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "charset" : XSCFrag , "href" : XSCurl , "hreflang" : XSCFrag , "type" : XSCFrag , "rel" : XSCFrag , "rev" : XSCFrag , "media" : XSCFrag })
RegisterElement("link",XSClink)

class XSCbase(XSCElement):
	close = 0
	attr_handlers = { "href" : XSCurl }
RegisterElement("base",XSCbase)

class XSCimg(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "src" : XSCurl , "alt" : XSCFrag , "longdesc" : XSCFrag , "width" : XSCFrag , "height" : XSCFrag , "usemap" : XSCFrag , "ismap" : XSCFrag })
	attr_handlers = AppendDict(attr_handlers,{ "border" : XSCFrag , "align" : XSCFrag , "hspace" : XSCFrag , "vspace" : XSCFrag }) # deprecated

	def __str__(self):
		e = XSCimg(self.content,self.attrs)
		e.AddImageSizeAttributes("src")

		return XSCElement.__str__(e)
RegisterElement("img",XSCimg)

class XSCobject(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "declare" : XSCFrag , "classid" : XSCFrag , "codebase" : XSCFrag , "data" : XSCFrag , "type" : XSCFrag , "codetype" : XSCFrag , "archive" : XSCFrag , "standby" : XSCFrag , "height" : XSCFrag , "width" : XSCFrag , "usemap" : XSCFrag , "name" : XSCFrag , "tabindex" : XSCFrag })
RegisterElement("object",XSCobject)

class XSCparam(XSCElement):
	close = 0
	attr_handlers = { "id" : XSCFrag , "name" : XSCFrag , "value" : XSCFrag , "valuetype" : XSCFrag , "type" : XSCFrag }
RegisterElement("param",XSCparam)

class XSCmap(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag })
RegisterElement("map",XSCmap)

class XSCarea(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "shape" : XSCFrag , "coords" : XSCFrag , "href" : XSCurl , "nohref" : XSCFrag , "alt" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("area",XSCarea)

class XSCstyle(XSCElement):
	close = 1
	attr_handlers = AppendDict(i18n,{ "type" : XSCFrag , "media" : XSCFrag , "title" : XSCFrag })
RegisterElement("style",XSCstyle)

class XSChr(XSCElement):
	close = 0
	attr_handlers = AppendDict(coreattrs,events)
RegisterElement("hr",XSChr)

# The pain, the pain ...
class XSCframeset(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "rows" : XSCFrag ,"cols" : XSCFrag ,"onload" : XSCFrag ,"onunload" : XSCFrag })
RegisterElement("frameset",XSCframeset)

class XSCframe(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCFrag , "name" : XSCFrag , "src" : XSCurl , "frameborder" : XSCFrag , "marginwidht" : XSCFrag , "marginheight" : XSCFrag , "noresize" : XSCFrag , "scrolling" : XSCFrag })
RegisterElement("frame",XSCframe)

class XSCnoframes(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("noframes",XSCnoframes)

class XSCiframe(XSCElement):
	close = 1
	attr_handlers = AppendDict(coreattrs,{ "longdesc" : XSCFrag , "name" : XSCFrag , "src" : XSCurl , "frameborder" : XSCFrag , "marginwidht" : XSCFrag , "marginheight" : XSCFrag , "noresize" : XSCFrag , "scrolling" : XSCFrag , "align" : XSCFrag , "height" : XSCFrag , "width" : XSCFrag })
RegisterElement("iframe",XSCiframe)

class XSCform(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "action" : XSCurl , "method" : XSCFrag , "enctype" : XSCFrag , "onsubmit" : XSCFrag , "onreset" : XSCFrag , "accept-charset" : XSCFrag })
RegisterElement("form",XSCform)

class XSCinput(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "type" : XSCFrag , "name" : XSCFrag , "value" : XSCFrag , "checked" : XSCFrag , "disabled" : XSCFrag , "readonly" : XSCFrag , "size" : XSCFrag , "maxlength" : XSCFrag , "src" : XSCurl , "alt" : XSCFrag , "usemap" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag , "onselect" : XSCFrag , "onchange" : XSCFrag , "accept" : XSCFrag })
RegisterElement("input",XSCinput)

class XSCbutton(XSCElement):
	close = 0
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag , "value" : XSCFrag , "type" : XSCFrag , "disabled" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("button",XSCbutton)

class XSCselect(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag , "size" : XSCFrag , "multiple" : XSCFrag , "disabled" : XSCFrag , "tabindex" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag , "onchange" : XSCFrag })
RegisterElement("select",XSCselect)

class XSCoptgroup(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "disabled" : XSCFrag , "label" : XSCFrag })
RegisterElement("optgroup",XSCoptgroup)

class XSCoption(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "selected" : XSCFrag , "disabled" : XSCFrag , "label" : XSCFrag , "value" : XSCFrag })
RegisterElement("option",XSCoption)

class XSCtextarea(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "name" : XSCFrag , "rows" : XSCFrag , "cols" : XSCFrag , "disabled" : XSCFrag , "readonly" : XSCFrag , "tabindex" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag , "onselect" : XSCFrag , "onchange" : XSCFrag })
RegisterElement("textarea",XSCtextarea)

class XSClabel(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "for" : XSCFrag , "accesskey" : XSCFrag , "onfocus" : XSCFrag , "onblur" : XSCFrag })
RegisterElement("label",XSClabel)

class XSCfieldset(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("fieldset",XSCfieldset)

class XSClegend(XSCElement):
	close = 1
	attr_handlers = AppendDict(attrs,{ "accesskey" : XSCFrag })
RegisterElement("legend",XSClegend)

class XSCscript(XSCElement):
	close = 1
	attr_handlers = { "charset" : XSCFrag , "type" : XSCFrag , "src" : XSCurl , "defer" : XSCFrag }
RegisterElement("script",XSCscript)

class XSCnoscript(XSCElement):
	close = 1
	attr_handlers = attrs
RegisterElement("noscript",XSCnoscript)

if __name__ == "__main__":
	try:
		print str(xsc.arsefile(sys.argv[1]))
	except XSCError,e:
		print str(e)


