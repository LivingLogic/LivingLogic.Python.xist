#! /usr/bin/env python

"""
A XSC module that contains a collection of useful elements.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import sys
import types
import time
time_ = time
import string
import xsc,html
html_ = html

class plaintable(html_.table):
	"""
	a HTML table where the values of the attributes cellpadding, cellspacing and
	border default to 0.
	"""
	empty = 0

	def asHTML(self):
		e = html_.table(self.content,self.attrs)
		if not e.hasAttr("cellpadding"):
			e["cellpadding"] = 0
		if not e.hasAttr("cellspacing"):
			e["cellspacing"] = 0
		if not e.hasAttr("border"):
			e["border"] = 0

		return e.asHTML()

class plainbody(html_.body):
	"""
	a HTML body where the attributes leftmaring, topmargin, marginheight and
	marginwidth default to 0.
	"""
	empty = 0

	def asHTML(self):
		e = html_.body(self.content,self.attrs)
		if not e.hasAttr("leftmargin"):
			e["leftmargin"] = 0
		if not e.hasAttr("topmargin"):
			e["topmargin"] = 0
		if not e.hasAttr("marginheight"):
			e["marginheight"] = 0
		if not e.hasAttr("marginwidth"):
			e["marginwidth"] = 0

		return e.asHTML()

class z(xsc.Element):
	"""
	puts it's content into french quotes
	"""
	empty = 0

	def asHTML(self):
		e = xsc.Frag("«",self.content,"»")

		return e.asHTML()

	def asPlainString(self):
		return '«' + self.content.asPlainString() + '»'

class nbsp(xsc.Element):
	"""
	a nonbreakable space as an element
	"""
	empty = 1

	def asHTML(self):
		return xsc.CharRef(160)

class filesize(xsc.Element):
	"""
	the size (in bytes) of the file whose URL is the attribute href
	as a text node.
	"""
	empty = 1
	attrHandlers = { "href" : xsc.URLAttr }

	def asHTML(self):
		size = self["href"].FileSize()
		if size is not None:
			return xsc.Text(size)
		else:
			return xsc.Text("?")

class filetime(xsc.Element):
	"""
	the time of the last modification of the file whose URL is in the attibute href
	as a text node.
	"""
	empty = 1
	attrHandlers = { "href" : xsc.URLAttr , "format" : xsc.TextAttr }

	def asHTML(self):
		return xsc.Text(self["href"].FileTime())

class time(xsc.Element):
	"""
	the current time (i.e. the time when asHTML() is called). You can specify the
	format of the string in the attribute format, which is a strftime() compatible
	string.
	"""
	empty = 1
	attrHandlers = { "format" : xsc.TextAttr }

	def asHTML(self):
		if self.hasAttr("format"):
			format = self["format"].asHTML().asPlainString()
		else:
			format = "%d. %b. %Y, %H:%M"

		return xsc.Text(time_.strftime(format,time_.gmtime(time_.time())))

class x(xsc.Element):
	"""
	element whose content will be ignored when converted to HTML:
	this can be used to comment out stuff.
	"""
	empty = 0

	def asHTML(self):
		return xsc.Null()

class pixel(html_.img):
	"""
	element for single pixel images, the default is the image
	"*/Images/Pixels/dot_clear.gif", but you can specify the color
	as a six digit hex string, which will be used as the filename,
	i.e. <pixel color="000000"/> results in
	<img src="*/Images/Pixels/000000.gif">.

	In addition to that you can specify width and height attributes
	(and every other allowed attribute for the img element) as usual.
	"""

	empty = 1
	attrHandlers = html_.img.attrHandlers.copy()
	attrHandlers.update({ "color" : xsc.ColorAttr })
	del attrHandlers["src"]

	def publish(self,publisher,encoding = None,XHTML = None):
		xsc.Element.publish(self,publisher,encoding,XHTML)

	def asHTML(self):
		e = html_.img()
		color = "dot_clear"
		for attr in self.attrs.keys():
			if attr == "color":
				color = self["color"]
			else:
				e[attr] = self[attr]
		e["src"] = ("*/Images/Pixels/",color,".gif")

		return e.asHTML()

class caps(xsc.Element):
	"""
	returns a fragment that contains the content string converted to caps and small caps.
	This is done by converting all lowercase letters to uppercase and packing them into a
	<span class="nini">...</span>. This element is meant to be a workaround until all
	browsers support the CSS feature "font-variant: small-caps".
	"""
	empty = 0

	def asHTML(self):
		e = self.content.asPlainString() + "?"
		result = xsc.Frag()
		collect = ""
		innini = 0
		for i in range(len(e)):
			if (i == len(e)) or ((e[i] in string.lowercase) and (innini==0)) or ((e[i] not in string.lowercase) and (innini==1)):
				if innini==0:
					result.append(collect)
				else:
					result.append(html_.span([ collect.upper() ],Class="nini" ))
				if i != len(e):
					collect = e[i]
				innini = 1-innini
			else:
				collect = collect + e[i]
		return result

	def asPlainString(self):
			return self.content.asPlainString().upper()

class endash(xsc.Element):
	empty = 1

	def asHTML(self):
		return xsc.Text("-")

class emdash(xsc.Element):
	empty = 1

	def asHTML(self):
		return xsc.Text("-")

class include(xsc.Element):
	empty = 1
	attrHandlers = { "src" : xsc.URLAttr }

	def asHTML(self):
		e = xsc.xsc.parse(self["src"].forInput())

		return e.asHTML()

class center(xsc.Element):
	empty = 0

class par(html_.div):
	empty = 0
	attrHandlers = xsc.appendDict(html_.div.attrHandlers, {"noindent" : xsc.TextAttr})

	def asHTML(self):
		e = html_.div(self.content.clone())
		indent = 1
		for attr in self.attrs.keys():
			if attr == "noindent":
				indent = None
			else:
				e[attr] = self[attr]
		if indent is not None:
			e["class"] = "indent"
		return e.asHTML()

def _generateImgAttrs(element,urlattrname,widthattrname,heightattrname):
	pass

class autoimg(html.img):
	def asHTML(self):
		e = html_.img(**self.attrs)
		e._addImageSizeAttributes("src","width","height")
		return e.asHTML()

class autoinput(html.img):
	def asHTML(self):
		if self.hasAttr("type") and self["type"].asHTML().asPlainString() == u"image":
			e = html_.input(*self.content,**self.attrs)
			e._addImageSizeAttributes("src","size",None) # no height
			return e.asHTML()
		else:
			return html.img.asHTML(self)

class loremipsum(xsc.Element):
	empty = 1
	attrHandlers = { "len" : xsc.IntAttr }

	text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diem nonummy nibh euismod tincidnut ut lacreet dolore magna aliguam erat volutpat. Ut wisis enim ad minim veniam, quis nostrud exerci tution ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis te feugifacilisi. Duis antem dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zril delinit au gue duis dolore te feugat nulla facilisi."

	def asHTML(self):
		if self.hasAttr("len"):
			text = self.text[:self["len"].asInt()]
		else:
			text = self.text
		return xsc.Text(text)

class redirectpage(xsc.Element):
	empty = 1
	attrHandlers = { "href" : xsc.URLAttr }

	def asHTML(self):
		url = self["href"]
		e = html_.html_(
			html_.head(html_.title("Redirection")),
			html_.body(
				"Your browser doesn't understand redirects. This page has been redirected to ",
				html_.a(url,href = url)
			)
		)
		return e.asHTML()

# Control characters (not part of HTML)
class lf(xsc.Entity): "line feed"; codepoint = 10
class cr(xsc.Entity): "carriage return"; codepoint = 13
class tab(xsc.Entity): "horizontal tab"; codepoint = 9
class esc(xsc.Entity): "escape"; codepoint = 27

class html(xsc.Entity):
	def asHTML(self):
		return html_.abbr("HTML",title="Hypertext Markup Language",lang="en")
	def asPlainString(self):
		return u"HTML"

class xml(xsc.Entity):
	def asHTML(self):
		return html_.abbr("XML",title="Extensible Markup Language",lang="en")
	def asPlainString(self):
		return u"XML"

class css(xsc.Entity):
	def asHTML(self):
		return html_.abbr("CSS",title="Cascading Style Sheet",lang="en")
	def asPlainString(self):
		return u"CSS"

class cgi(xsc.Entity):
	def asHTML(self):
		return html_.abbr("CGI",title="Common Gateway Interface",lang="en")
	def asPlainString(self):
		return u"CGI"

class www(xsc.Entity):
	def asHTML(self):
		return html_.abbr("WWW",title="World Wide Web",lang="en")
	def asPlainString(self):
		return u"WWW"

class pdf(xsc.Entity):
	def asHTML(self):
		return html_.abbr("PDF",title="Protable Document Format",lang="en")
	def asPlainString(self):
		return u"PDF"

class url(xsc.Entity):
	def asHTML(self):
		return html_.abbr("URL",title="Uniform Resource Locator",lang="en")
	def asPlainString(self):
		return u"URL"

class http(xsc.Entity):
	def asHTML(self):
		return html_.abbr("HTTP",title="Hypertext Transfer Protocol",lang="en")
	def asPlainString(self):
		return u"HTTP"

class smtp(xsc.Entity):
	def asHTML(self):
		return html_.abbr("SMTP",title="Simple Mail Transfer Protocol",lang="en")
	def asPlainString(self):
		return u"SMTP"

class ftp(xsc.Entity):
	def asHTML(self):
		return html_.abbr("FTP",title="File Transfer Protocol",lang="en")
	def asPlainString(self):
		return u"FTP"

class pop3(xsc.Entity):
	def asHTML(self):
		return html_.abbr("POP3",title="Post Office Protocol 3",lang="en")
	def asPlainString(self):
		return u"POP3"

class cvs(xsc.Entity):
	def asHTML(self):
		return html_.abbr("CVS",title="Concurrent Versions System",lang="en")
	def asPlainString(self):
		return u"CVS"

class faq(xsc.Entity):
	def asHTML(self):
		return html_.abbr("FAQ",title="Frequently Asked Question",lang="en")
	def asPlainString(self):
		return u"FAQ"

class gnu(xsc.Entity):
	def asHTML(self):
		return html_.abbr("GNU",title="GNU's Not UNIX",lang="en")
		# we could do it ;): return html_.abbr("GNU",title=(self,"'s Not UNIX"),lang="en")
	def asPlainString(self):
		return u"GNU"

class dns(xsc.Entity):
	def asHTML(self):
		return html_.abbr("DNS",title="Domain Name Service",lang="en")
	def asPlainString(self):
		return u"DNS"

class ppp(xsc.Entity):
	def asHTML(self):
		return html_.abbr("PPP",title="Domain Name Service",lang="en")
	def asPlainString(self):
		return u"PPP"

class isdn(xsc.Entity):
	def asHTML(self):
		return html_.abbr("ISDN",title="Integrated Services Digital Network",lang="en")
	def asPlainString(self):
		return u"ISDN"

namespace = xsc.Namespace("specials","http://www.livinglogic.de/DTDs/specials.dtd",vars())

if __name__ == "__main__":
	xsc.make()

