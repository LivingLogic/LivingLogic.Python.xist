#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; module that contains a collection of useful elements for
generating &html;.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, types, time as time_, string

from ll.xist import xsc, parsers
from ll.xist.ns import ihtml, html, meta, specials

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
	<par>element for single pixel images.</par>
	
	<par>The default is the image <filename>root:px/0.gif</filename>, but
	you can specify the color as a three digit hex string, which will be
	used as the filename, i.e. <markup>&lt;pixel color="000"/&gt;</markup>
	results in <markup>&lt;img src="root:px/000.gif"&gt;</markup>.</par>

	<par>In addition to that you can specify width and height attributes
	(and every other allowed attribute for the <class>img</class> element)
	as usual.</par>
	"""

	empty = True
	class Attrs(html.img.Attrs):
		class color(xsc.TextAttr):
			"""
			The pixel color as a three digit hex value.
			"""
			default = 0
		class alt(html.img.Attrs.alt):
			default = ""
		class width(html.img.Attrs.width):
			default = 1
		class height(html.img.Attrs.height):
			default = 1
		src = None # remove source attribute

	def convert(self, converter):
		e = html.img(
			self.attrs.without(["color"]),
			src=("root:px/", self.attrs.get("color"), ".gif")
		)
		return e.convert(converter)

class caps(xsc.Element):
	"""
	<par>returns a fragment that contains the content string
	converted to caps and small caps.</par>
	
	<par>This is done by converting all lowercase letters to
	uppercase and packing them into a
	<markup>&lt;span class="nini"&gt;...&lt;/span&gt;</markup>.
	This element is meant to be a workaround until all
	browsers support the &css; feature <lit>font-variant: small-caps</lit>.</par>
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
		if not self.attrs.has("noindent"):
			e["class_"] = "indent"
		return e.convert(converter)

class autoimg(html.img):
	"""
	<par>An image were width and height attributes are automatically generated.</par>
	
	<par>If the attributes are already there, they won't be modified.</par>
	"""
	def convert(self, converter):
		target = converter.target
		if issubclass(target, ihtml) or issubclass(target, html):
			e = target.img(self.attrs.convert(converter))
		else:
			raise ValueError("unknown conversion target %r" % target)
		src = self["src"].convert(converter).forInput(converter.root)
		e._addimagesizeattributes(src, "width", "height")
		return e

class autopixel(html.img):
	"""
	<par>A pixel image were width and height attributes are automatically generated.</par>
	
	<par>This works like <pyref class="pixel"><class>pixel</class></pyref> but the
	size is <z>inherited</z> from the image specified via the <lit>src</lit> attribute.</par>
	"""
	class Attrs(html.img.Attrs):
		class color(xsc.TextAttr):
			"""
			<par>The pixel color as a three digit hex value.</par>
			"""
			default = 0
		class alt(html.img.Attrs.alt):
			default = ""

	def convert(self, converter):
		target = converter.target
		if issubclass(target, ihtml) or issubclass(target, html):
			e = target.img(self.attrs.without(["color"]))
		else:
			raise ValueError("unknown conversion target %r" % target)
		src = self["src"].convert(converter).forInput(converter.root)
		e._addimagesizeattributes(src, "width", "height")
		e["src"] = ("root:px/", self.attrs.get("color"), ".gif")
		return e

class autoinput(html.input):
	"""
	<par>Extends <pyref module="ll.xist.ns.html" class="input"><class>input</class></pyref>
	with the ability to automatically set the size, if this element
	has <lit>type=="image"</lit>.</par>
	"""
	def convert(self, converter):
		e = html.input(self.content, self.attrs)
		if u"type" in self.attrs and unicode(self["type"].convert(converter)) == u"image":
			src = self["src"].convert(converter).forInput(converter.root)
			e._addimagesizeattributes(src, "size", None) # no height
		return e.convert(converter)

class redirectpage(xsc.Element):
	empty = True
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): required = True

	def convert(self, converter):
		url = self["href"]
		e = html.html(
			html.head(
				meta.contenttype(),
				html.title("Redirection to ", url)
			),
			html.body(
				"Your browser doesn't understand redirects. This page has been redirected to ",
				html.a(url, href=url)
			)
		)
		return e.convert(converter)

class javascript(html.script):
	"""
	<par>can be used for javascript.</par>
	"""
	empty = False
	class Attrs(html.script.Attrs):
		language = None
		type = None

	def convert(self, converter):
		e = html.script(self.content, self.attrs, language="javascript", type="text/javascript")
		return e.convert(converter)

class ImgAttrDecorator(specials.AttrDecorator):
	class Attrs(html.img.Attrs):
		pass
	idecoratable = (html.img,)

class xmlns(xsc.Namespace):
	xmlname = "htmlspecials"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/htmlspecials"
xmlns.makemod(vars())

