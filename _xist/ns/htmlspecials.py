#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
<par>An &xist; module that contains a collection of useful elements for
generating &html;.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, types, time as time_, string

from ll.xist import xsc, parsers
import ihtml, html, meta

class plaintable(html.table):
	"""
	<par>a &html; table where the values of the attributes <lit>cellpadding</lit>,
	<lit>cellspacing</lit> and <lit>border</lit> default to <lit>0</lit>.</par>
	"""
	empty = False
	class Attrs(html.table.Attrs):
		class cellpadding(html.table.Attrs.cellpadding):
			default = 0
		class cellspacing(html.table.Attrs.cellspacing):
			default = 0
		class border(html.table.Attrs.border):
			default = 0

	def convert(self, converter):
		e = html.table(self.content, self.attrs)
		return e.convert(converter)

class plainbody(html.body):
	"""
	<par>a &html; body where the attributes <lit>leftmargin</lit>, <lit>topmargin</lit>,
	<lit>marginheight</lit> and <lit>marginwidth</lit> default to <lit>0</lit>.</par>
	"""
	empty = False
	class Attrs(html.body.Attrs):
		class leftmargin(html.body.Attrs.leftmargin):
			default = 0
		class topmargin(html.body.Attrs.topmargin):
			default = 0
		class marginheight(html.body.Attrs.marginheight):
			default = 0
		class marginwidth(html.body.Attrs.marginwidth):
			default = 0

	def convert(self, converter):
		e = html.body(self.content, self.attrs)
		return e.convert(converter)

class pixel(html.img):
	"""
	<par>element for single pixel images, the default is the image
	<filename>root:Images/Pixels/dot_clear.gif</filename>, but you can specify the color
	as a six digit hex string, which will be used as the filename,
	i.e. <markup>&lt;pixel color="000"/&gt;</markup> results in
	<markup>&lt;img src="root:images/pixels/000.gif"&gt;</markup>.</par>

	<par>In addition to that you can specify width and height attributes
	(and every other allowed attribute for the img element) as usual.</par>
	"""

	empty = True
	class Attrs(html.img.Attrs):
		class color(xsc.ColorAttr): pass
		src = None

	def convert(self, converter):
		e = html.img()
		color = "0"
		for attr in self.attrs.keys():
			if attr == "color":
				color = self["color"]
			else:
				e[attr] = self[attr]
		if not e.hasAttr("alt"):
			e["alt"] = u""
		if not e.hasAttr("width"):
			e["width"] = 1
		if not e.hasAttr("height"):
			e["height"] = 1
		e["src"] = ("root:images/pixels/", color, ".gif")

		return e.convert(converter)

class caps(xsc.Element):
	"""
	<par>returns a fragment that contains the content string converted to caps and small caps.
	This is done by converting all lowercase letters to uppercase and packing them into a
	<markup>&lt;span class="nini"&gt;...&lt;/span&gt;</markup>. This element is meant to be a workaround until all
	browsers support the CSS feature "font-variant: small-caps".</par>
	"""
	empty = False

	lowercase = unicode(string.lowercase, "latin-1") + u" "

	def convert(self, converter):
		e = unicode(self.content.convert(converter))
		result = xsc.Frag()
		if e: # if we have nothing to do, we skip everything to avoid errors
			collect = ""
			last_was_lower = e[0] in self.lowercase
			for c in e:
				if (c in self.lowercase) != last_was_lower:
					if last_was_lower:
						result.append(html.span(collect.upper(), class_="nini"))
					else:
						result.append(collect)
					last_was_lower = not last_was_lower
					collect = ""
				collect = collect + c
			if collect:
				if last_was_lower:
					result.append(html.span(collect.upper(), class_="nini" ))
				else:
					result.append(collect)
		return result

	def __unicode__(self):
			return unicode(self.content).upper()

class par(html.div):
	empty = False
	class Attrs(html.div.Attrs):
		class noindent(xsc.BoolAttr): pass

	def convert(self, converter):
		e = html.div(self.content, self.attrs.without(["noindent"]))
		if not self.hasAttr("noindent"):
			e["class_"] = "indent"
		return e.convert(converter)

class autoimg(html.img):
	"""
	<par>An image were width and height attributes are automatically generated.
	If the attributes are already there, they are taken as a
	formatting template with the size passed in as a dictionary with the keys
	<lit>width</lit> and <lit>height</lit>, i.e. you could make your image twice
	as wide with <lit>width="2*%(width)d"</lit>.</par>
	"""
	def convert(self, converter):
		if converter.target=="ihtml":
			e = ihtml.img(self.attrs)
		else:
			e = html.img(self.attrs)
		e._addImageSizeAttributes(converter.root, "src", "width", "height")
		return e.convert(converter)

class autoinput(html.input):
	"""
	<par>Extends <pyref module="ll.xist.ns.html" class="input"><class>input</class></pyref>
	with the ability to automatically set the size, if this element
	has <lit>type=="image"</lit>.</par>
	"""
	def convert(self, converter):
		if self.hasAttr("type") and self["type"].convert(converter) == u"image":
			e = html.input(self.content, self.attrs)
			e._addImageSizeAttributes(converter.root, "src", "size", None) # no height
			return e.convert(converter)
		else:
			return html.img.convert(self, converter)

class redirectpage(xsc.Element):
	empty = True
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): pass

	def convert(self, converter):
		url = self["href"]
		e = html.html(
			html.head(
				meta.contenttype(),
				html.title("Redirection")
			),
			html.body(
				"Your browser doesn't understand redirects. This page has been redirected to ",
				html.a(url, href=url)
			)
		)
		return e.convert(converter)

class javascript(xsc.Element):
	"""
	<par>can be used for javascript.</par>
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class src(xsc.TextAttr): pass

	def convert(self, converter):
		e = html.script(self.content, language="javascript", type="text/javascript", src=self["src"])
		return e.convert(converter)

xmlns = xsc.Namespace("htmlspecials", "http://xmlns.livinglogic.de/xist/ns/htmlspecials", vars())

