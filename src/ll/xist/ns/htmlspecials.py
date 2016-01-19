# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST module that contains a collection of useful elements for generating
HTML.
"""


import sys, types, time as time_, string, warnings

from ll.xist import xsc, sims
from ll.xist.ns import xml, ihtml, html as html_, meta, specials


__docformat__ = "reStructuredText"


xmlns = "http://xmlns.livinglogic.de/xist/ns/htmlspecials"


class html(html_.html):
	"""
	Creates an :class:`ll.xist.ns.html.html` element and automatically sets the
	``lang`` and ``xml:lang`` attributes to the ``converter``\s configured language.
	"""
	xmlns = xmlns

	def convert(self, converter):
		node = html_.html(self.content, self.attrs)
		if converter.lang is not None:
			if "lang" not in node.attrs:
				node.attrs.lang = converter.lang
			if xml.Attrs.lang not in node.attrs:
				node.attrs[xml.Attrs.lang] = converter.lang
		return node.convert(converter)


class plaintable(html_.table):
	"""
	a HTML table where the values of the attributes ``cellpadding``,
	``cellspacing`` and ``border`` default to ``0``.
	"""
	xmlns = xmlns
	class Attrs(html_.table.Attrs):
		class cellpadding(html_.table.Attrs.cellpadding):
			default = 0
		class cellspacing(html_.table.Attrs.cellspacing):
			default = 0
		class border(html_.table.Attrs.border):
			default = 0

	def convert(self, converter):
		e = html_.table(self.content, self.attrs)
		return e.convert(converter)


class plainbody(html_.body):
	"""
	a HTML body where the attributes ``leftmargin``, ``topmargin``,
	``marginheight`` and ``marginwidth`` default to ``0``.
	"""
	xmlns = xmlns
	class Attrs(html_.body.Attrs):
		class leftmargin(html_.body.Attrs.leftmargin):
			default = 0
		class topmargin(html_.body.Attrs.topmargin):
			default = 0
		class marginheight(html_.body.Attrs.marginheight):
			default = 0
		class marginwidth(html_.body.Attrs.marginwidth):
			default = 0

	def convert(self, converter):
		e = html_.body(self.content, self.attrs)
		return e.convert(converter)


class _pixelbase(html_.img):
	xmlns = xmlns
	class Context(html_.img.Context):
		def __init__(self):
			self.src = "root:px/spc.gif"

	class Attrs(html_.img.Attrs):
		class color(xsc.TextAttr):
			"""
			The pixel color as a CSS value. Leave it blank to get a transparent
			pixel.
			"""

		class alt(html_.img.Attrs.alt):
			default = ""


class pixel(_pixelbase):
	"""
	Element for single transparent pixel image.

	You can specify the pixel color via the ``color`` attribute (which will set
	the background-color in the style attribute).

	In addition to that you can specify width and height attributes (and every
	other allowed attribute for the :class:`img` element) as usual.
	"""
	xmlns = xmlns
	class Attrs(_pixelbase.Attrs):
		class width(_pixelbase.Attrs.width):
			default = 1
		class height(_pixelbase.Attrs.height):
			default = 1

	def convert(self, converter):
		if self.attrs.src:
			src = self.attrs.src
		else:
			src = converter[self].src
		if self.attrs.color:
			style = ["background-color: ", self.attrs.color, ";"]
			if self.attrs.style:
				style.append(" ")
				style.append(self.attrs.style)
		else:
			style = self.attrs.style
		e = converter.target.img(
			self.attrs.withoutnames("color"),
			style=style,
			src=src,
		)
		return e.convert(converter)


class autoimg(html_.img):
	"""
	An image were width and height attributes are automatically generated.

	If the attributes are already there, they won't be modified.
	"""
	xmlns = xmlns
	def convert(self, converter):
		target = converter.target
		if target.xmlns in (ihtml.xmlns, html_.xmlns):
			e = target.img(self.attrs.convert(converter))
		else:
			raise ValueError("unknown conversion target {!r}".format(target))
		src = self["src"].convert(converter).forInput(converter.root)
		e._addimagesizeattributes(src, "width", "height")
		return e


class autopixel(_pixelbase):
	"""
	A pixel image were width and height attributes are automatically generated.

	This works like :class:`pixel` but the size is "inherited" from the image
	specified via the ``src`` attribute.
	"""
	xmlns = xmlns
	def convert(self, converter):
		target = converter.target
		if target.xmlns not in (ihtml.xmlns, html_.xmlns):
			raise ValueError("unknown conversion target {!r}".format(target))
		e = target.img(self.attrs.withoutnames("color"))
		src = self.attrs.src.convert(converter).forInput(converter.root)
		e._addimagesizeattributes(src, "width", "height")
		e.attrs.src = converter[self].src
		return e


class autoinput(html_.input):
	"""
	Extends :class:`ll.xist.ns.html.input` with the ability to automatically
	set the size, if this element has ``type=="image"``.
	"""
	xmlns = xmlns
	def convert(self, converter):
		target = converter.target
		e = target.input(self.content, self.attrs)
		if "type" in self.attrs and str(self.attrs.type.convert(converter)) == "image":
			src = self.attrs.src.convert(converter).forInput(converter.root)
			e._addimagesizeattributes(src, "size", None) # no height
		return e.convert(converter)


class redirectpage(xsc.Element):
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): required = True

	langs = {
		"en": ("Redirection to ", "Your browser doesn't understand redirects. This page has been redirected to "),
		"de": ("Weiterleitung auf ", "Ihr Browser unterstützt keine Weiterleitung. Diese Seite wurde weitergeleitet auf ")
	}

	def convert(self, converter):
		target = converter.target
		(title, text) = self.langs.get(converter.lang, self.langs["en"])
		url = self["href"]
		e = target.html(
			target.head(
				meta.contenttype(),
				target.title(title, url)
			),
			target.body(
				text, target.a(url, href=url)
			)
		)
		return e.convert(converter)


class javascript(html_.script):
	"""
	Can be used for javascript.
	"""
	xmlns = xmlns
	class Attrs(html_.script.Attrs):
		language = None
		type = None

	def convert(self, converter):
		target = converter.target
		e = target.script(self.content, self.attrs, language="javascript", type="text/javascript")
		return e.convert(converter)


class flash(xsc.Element):
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class src(xsc.URLAttr): required = True
		class width(xsc.IntAttr): required = True
		class height(xsc.IntAttr): required = True
		class quality(xsc.TextAttr): default = "high"
		class bgcolor(xsc.ColorAttr): pass

	def convert(self, converter):
		target = converter.target
		e = target.object(
			target.param(name="movie", value=self.attrs.src),
			target.embed(
				src=self.attrs.src,
				quality=self.attrs.quality,
				bgcolor=self.attrs.bgcolor,
				width=self.attrs.width,
				height=self.attrs.height,
				type="application/x-shockwave-flash",
				pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash"
			),
			classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000",
			codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=5,0,0,0",
			width=self.attrs.width,
			height=self.attrs.height
		)

		# copy optional attributes
		for attrname in ("quality", "bgcolor"):
			if attrname in self.attrs:
				e.insert(0, target.param(name=attrname, value=self.attrs[attrname]))

		return e.convert(converter)


class quicktime(xsc.Element):
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class src(xsc.URLAttr): required = True
		class href(xsc.URLAttr): pass
		class target(xsc.TextAttr): pass
		class width(xsc.IntAttr): required = True
		class height(xsc.IntAttr): required = True
		class bgcolor(xsc.ColorAttr): pass
		class controller(xsc.ColorAttr): values = ("true", "false")
		class autoplay(xsc.ColorAttr): values = ("true", "false")
		class border(xsc.IntAttr): pass

	def convert(self, converter):
		target = converter.target
		e = target.object(
			target.param(name="src", value=self.attrs.src),
			target.param(name="type", value="video/quicktime"),
			target.param(name="pluginspage", value="http://www.apple.com/quicktime/download/indext.html"),
			target.embed(
				src=self.attrs.src,
				href=self.attrs.href,
				target=self.attrs.target,
				bgcolor=self.attrs.bgcolor,
				width=self.attrs.width,
				height=self.attrs.height,
				type="video/quicktime",
				border=self.attrs.border,
				pluginspage="http://www.apple.com/quicktime/download/indext.html"
			),
			classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B",
			codebase="http://www.apple.com/qtactivex/qtplugin.cab#version=6,0,2,0",
			width=self.attrs.width,
			height=self.attrs.height
		)

		# copy optional attributes
		for attrname in ("href", "target", "bgcolor", "controller", "autoplay"):
			if attrname in self.attrs:
				e.insert(0, target.param(name=attrname, value=self[attrname]))

		return e.convert(converter)


class ImgAttrDecorator(specials.AttrDecorator):
	xmlns = xmlns
	class Attrs(html_.img.Attrs):
		pass
	idecoratable = (html_.img,)


class InputAttrDecorator(specials.AttrDecorator):
	xmlns = xmlns
	class Attrs(html_.input.Attrs):
		pass
	decoratable = (html_.input,)


class FormAttrDecorator(specials.AttrDecorator):
	xmlns = xmlns
	class Attrs(html_.form.Attrs):
		pass
	decoratable = (html_.form,)


class TextAreaAttrDecorator(specials.AttrDecorator):
	xmlns = xmlns
	class Attrs(html_.textarea.Attrs):
		pass
	decoratable = (html_.textarea,)
