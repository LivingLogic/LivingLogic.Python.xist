#! /usr/bin/python

import sys
from xsc import *

# common attributes
coreattrs  = [ "id","class","style","title" ]
i18n       = [ "lang","dir" ]
events     = [ "onclick","ondblclick","onmousedown","onmouseup","onmouseover","onmousemove","onmouseout","onkeypress","onkeydown","onkeyup" ]
attrs      = coreattrs + i18n + events
cellhalign = [ "align","char","charoff" ]
cellvalign = [ "valign" ]

# The global structure of an HTML document
class html(XSCElement):
	close = 1
	permitted_attrs = i18n
handlers["html"] = html

class head(XSCElement):
	close = 1
	permitted_attrs = i18n + [ "profile" ]
handlers["head"] = head

class title(XSCElement):
	close = 1
	permitted_attrs = i18n
handlers["title"] = title

class meta(XSCElement):
	close = 0
	permitted_attrs = i18n + [ "http-equiv","name","content","scheme" ]
handlers["meta"] = meta

class body(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "onload","onunload" ] + [ "background","bgcolor","text","link","vlink","alink","leftmargin","topmargin","marginwidth","marginheight"] # deprecated

class div(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["div"] = div

class span(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["span"] = span

class h1(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["h1"] = h1

class h2(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["h2"] = h2

class h3(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["h3"] = h3

class h4(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["h4"] = h4

class h5(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["h5"] = h5

class h6(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["h6"] = h6

class address(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["address"] = address

class bdo(XSCElement):
	close = 1
	permitted_attrs = coreattrs + i18n
handlers["bdo"] = bdo

class tt(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["tt"] = tt

class i(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["i"] = i

class b(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["b"] = b

class big(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["big"] = big

class small(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["small"] = small

class em(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["em"] = em

class strong(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["strong"] = strong

class dfn(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["dfn"] = dfn

class code(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["code"] = code

class samp(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["samp"] = samp

class kbd(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["kbd"] = kbd

class var(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["var"] = var

class cite(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["cite"] = cite

class abbr(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["abbr"] = abbr

class acronym(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["acronym"] = acronym

class blockquote(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "cite" ]
handlers["blockquote"] = blockquote

class q(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "cite" ]
handlers["q"] = q

class sub(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["sub"] = sub

class sup(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["sup"] = sup

class p(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["p"] = p

class br(XSCElement):
	close = 0
	permitted_attrs = coreattrs
handlers["br"] = br

class pre(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["pre"] = pre

class ins(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "cite","datetime" ]
handlers["ins"] = ins

class Del(XSCElement): # name clash
	close = 1
	permitted_attrs = attrs + [ "cite","datetime" ]
handlers["del"] = Del

class ul(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["ul"] = ul

class ol(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["ol"] = ol

class li(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["li"] = li

class dl(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["dl"] = dl

class dt(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["dt"] = dt

class dd(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["dd"] = dd

class table(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "summary","width","border","frame","rules","cellspacing","cellpadding" ] + [ "height" ] # deprecated
handlers["table"] = table

class caption(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["caption"] = caption

class thead(XSCElement):
	close = 1
	permitted_attrs = attrs + cellhalign + cellvalign
handlers["thead"] = thead

class tfoot(XSCElement):
	close = 1
	permitted_attrs = attrs + cellhalign + cellvalign
handlers["tfoot"] = tfoot

class tbody(XSCElement):
	close = 1
	permitted_attrs = attrs + cellhalign + cellvalign
handlers["tbody"] = tbody

class colgroup(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "span","width" ] + cellhalign + cellvalign
handlers["colgroup"] = colgroup

class col(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "span","width" ] + cellhalign + cellvalign
handlers["col"] = col

class tr(XSCElement):
	close = 1
	permitted_attrs = attrs + cellhalign + cellvalign
handlers["tr"] = tr

class th(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "abbr","axis","headers","scope","rowspan","colspan" ] + cellhalign + cellvalign
handlers["th"] = th

class td(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "abbr","axis","headers","scope","rowspan","colspan" ] + cellhalign + cellvalign
handlers["td"] = td

class a(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "charset","type","name","href","hreflang","rel","rev","accesskey","shape","coords","tabindex","onfocus","onblur" ]

	def AsHTML(self,mode = None):	
		e = XSCElement.AsHTML(self,mode)

		e.ExpandLinkAttribute("href")

		return e
handlers["a"] = a

class link(XSCElement):
	close = 0
	permitted_attrs = attrs + [ "charset","href","hreflang","type","rel","rev","media" ]
handlers["link"] = link

class base(XSCElement):
	close = 0
	permitted_attrs = [ "href" ]
handlers["base"] = base

class img(XSCElement):
	close = 0
	permitted_attrs = attrs + [ "src","alt","longdesc","width","height","usemap","ismap" ] + [ "border" ] # deprecated

	def AsHTML(self,mode = None):
		e = XSCElement.AsHTML(self,mode)

		e.AddImageSizeAttributes("src")

		return e
handlers["img"] = img

class object(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "declare","classid","codebase","data","type","codetype","archive","standby","height","width","usemap","name","tabindex" ]
handlers["object"] = object

class param(XSCElement):
	close = 0
	permitted_attrs = [ "id","name","value","valuetype","type" ]
handlers["param"] = param

class map(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "name" ]
handlers["map"] = map

class area(XSCElement):
	close = 0
	permitted_attrs = attrs + [ "shape","coords","href","nohref","alt","tabindex","accesskey","onfocus","onblur" ]
handlers["area"] = area

class style(XSCElement):
	close = 1
	permitted_attrs = i18n + [ "type","media","title" ]
handlers["style"] = style

class hr(XSCElement):
	close = 0
	permitted_attrs = coreattrs + events
handlers["hr"] = hr

# The pain, the pain ...
class frameset(XSCElement):
	close = 1
	permitted_attrs = coreattrs + [ "rows","cols","onload","onunload" ]
handlers["frameset"] = frameset

class frame(XSCElement):
	close = 1
	permitted_attrs = coreattrs + [ "longdesc","name","src","frameborder","marginwidht","marginheight","noresize","scrolling" ]
handlers["frame"] = frame

class noframes(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["noframes"] = noframes

class iframe(XSCElement):
	close = 1
	permitted_attrs = coreattrs + [ "longdesc","name","src","frameborder","marginwidht","marginheight","noresize","scrolling","align","height","width" ]
handlers["iframe"] = iframe

class form(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "action","method","enctype","onsubmit","onreset","accept-charset" ]
handlers["form"] = form

class input(XSCElement):
	close = 0
	permitted_attrs = attrs + [ "type","name","value","checked","disabled","readonly","size","maxlength","src","alt","usemap","tabindex","accesskey","onfocus","onblur","onselect","onchange","accept" ]
handlers["input"] = input

class button(XSCElement):
	close = 0
	permitted_attrs = attrs + [ "name","value","type","disabled","tabindex","accesskey","onfocus","onblur" ]
handlers["button"] = button

class select(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "name","size","multiple","disabled","tabindex","onfocus","onblur","onchange" ]
handlers["select"] = select

class optgroup(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "disabled","label" ]
handlers["optgroup"] = optgroup

class option(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "selected","disabled","label","value" ]
handlers["option"] = option

class textarea(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "name","rows","cols","disabled","readonly","tabindex","accesskey","onfocus","onblur","onselect","onchange" ]
handlers["textarea"] = textarea

class label(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "for","accesskey","onfocus","onblur" ]
handlers["label"] = label

class fieldset(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["fieldset"] = fieldset

class legend(XSCElement):
	close = 1
	permitted_attrs = attrs + [ "accesskey" ]
handlers["legend"] = legend

class script(XSCElement):
	close = 1
	permitted_attrs = [ "charset","type","src","defer" ]
handlers["script"] = script

class noscript(XSCElement):
	close = 1
	permitted_attrs = attrs
handlers["noscript"] = noscript

if __name__ == "__main__":
	h = XSC(sys.argv[1])
	print str(h)

