# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
An XIST module that contains a collection of useful elements for generating
HTML.
"""


import sys, types, time as time_, string, warnings

from ll.xist import xsc, parsers, sims
from ll.xist.ns import ihtml, html, meta, specials


__docformat__ = "reStructuredText"


xmlns = "http://xmlns.livinglogic.de/xist/ns/htmlspecials"


class plaintable(html.table):
	"""
	a HTML table where the values of the attributes ``cellpadding``,
	``cellspacing`` and ``border`` default to ``0``.
	"""
	xmlns = xmlns
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
	a HTML body where the attributes ``leftmargin``, ``topmargin``,
	``marginheight`` and ``marginwidth`` default to ``0``.
	"""
	xmlns = xmlns
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


class _pixelbase(html.img):
	xmlns = xmlns
	class Context(html.img.Context):
		def __init__(self):
			self.src = "root:px/spc.gif"

	class Attrs(html.img.Attrs):
		class color(xsc.TextAttr):
			"""
			The pixel color as a CSS value. Leave it blank to get a transparent
			pixel.
			"""

		class alt(html.img.Attrs.alt):
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
			self.attrs.withoutnames(u"color"),
			style=style,
			src=src,
		)
		return e.convert(converter)


class autoimg(html.img):
	"""
	An image were width and height attributes are automatically generated.
	
	If the attributes are already there, they won't be modified.
	"""
	xmlns = xmlns
	def convert(self, converter):
		target = converter.target
		if target.xmlns in (ihtml.xmlns, html.xmlns):
			e = target.img(self.attrs.convert(converter))
		else:
			raise ValueError("unknown conversion target %r" % target)
		src = self[u"src"].convert(converter).forInput(converter.root)
		e._addimagesizeattributes(src, u"width", u"height")
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
		if target.xmlns not in (ihtml.xmlns, html.xmlns):
			raise ValueError("unknown conversion target %r" % target)
		e = target.img(self.attrs.withoutnames(u"color"))
		src = self.attrs.src.convert(converter).forInput(converter.root)
		e._addimagesizeattributes(src, u"width", u"height")
		e.attrs.src = converter[self].src
		return e


class autoinput(html.input):
	"""
	Extends :class:`ll.xist.ns.html.input` with the ability to automatically
	set the size, if this element has ``type=="image"``.
	"""
	xmlns = xmlns
	def convert(self, converter):
		target = converter.target
		e = target.input(self.content, self.attrs)
		if u"type" in self.attrs and unicode(self[u"type"].convert(converter)) == u"image":
			src = self[u"src"].convert(converter).forInput(converter.root)
			e._addimagesizeattributes(src, u"size", None) # no height
		return e.convert(converter)


class redirectpage(xsc.Element):
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class href(xsc.URLAttr): required = True

	langs = {
		"en": (u"Redirection to ", u"Your browser doesn't understand redirects. This page has been redirected to "),
		"de": (u"Weiterleitung auf ", u"Ihr Browser unterstützt keine Weiterleitung. Diese Seite wurde weitergeleitet auf ")
	}

	def convert(self, converter):
		target = converter.target
		(title, text) = self.langs.get(converter.lang, self.langs[u"en"])
		url = self[u"href"]
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


class javascript(html.script):
	"""
	Can be used for javascript.
	"""
	xmlns = xmlns
	class Attrs(html.script.Attrs):
		language = None
		type = None

	def convert(self, converter):
		target = converter.target
		e = target.script(self.content, self.attrs, language=u"javascript", type=u"text/javascript")
		return e.convert(converter)


class flash(xsc.Element):
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class src(xsc.URLAttr): required = True
		class width(xsc.IntAttr): required = True
		class height(xsc.IntAttr): required = True
		class quality(xsc.TextAttr): default = u"high"
		class bgcolor(xsc.ColorAttr): pass

	def convert(self, converter):
		target = converter.target
		e = target.object(
			target.param(name=u"movie", value=self[u"src"]),
			target.embed(
				src=self[u"src"],
				quality=self[u"quality"],
				bgcolor=self[u"bgcolor"],
				width=self[u"width"],
				height=self[u"height"],
				type=u"application/x-shockwave-flash",
				pluginspage=u"http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash"
			),
			classid=u"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000",
			codebase=u"http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=5,0,0,0",
			width=self[u"width"],
			height=self[u"height"]
		)

		# copy optional attributes
		for attrname in (u"quality", u"bgcolor"):
			if attrname in self.attrs:
				e.insert(0, target.param(name=attrname, value=self[attrname]))

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
		class controller(xsc.ColorAttr): values = (u"true", u"false")
		class autoplay(xsc.ColorAttr): values = (u"true", u"false")
		class border(xsc.IntAttr): pass

	def convert(self, converter):
		target = converter.target
		e = target.object(
			target.param(name=u"src", value=self[u"src"]),
			target.param(name=u"type", value=u"video/quicktime"),
			target.param(name=u"pluginspage", value=u"http://www.apple.com/quicktime/download/indext.html"),
			target.embed(
				src=self[u"src"],
				href=self[u"href"],
				target=self[u"target"],
				bgcolor=self[u"bgcolor"],
				width=self[u"width"],
				height=self[u"height"],
				type=u"video/quicktime",
				border=self[u"border"],
				pluginspage=u"http://www.apple.com/quicktime/download/indext.html"
			),
			classid=u"clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B",
			codebase=u"http://www.apple.com/qtactivex/qtplugin.cab#version=6,0,2,0",
			width=self[u"width"],
			height=self[u"height"]
		)

		# copy optional attributes
		for attrname in (u"href", u"target", u"bgcolor", u"controller", u"autoplay"):
			if attrname in self.attrs:
				e.insert(0, target.param(name=attrname, value=self[attrname]))

		return e.convert(converter)


class ImgAttrDecorator(specials.AttrDecorator):
	xmlns = xmlns
	class Attrs(html.img.Attrs):
		pass
	idecoratable = (html.img,)


class InputAttrDecorator(specials.AttrDecorator):
	xmlns = xmlns
	class Attrs(html.input.Attrs):
		pass
	decoratable = (html.input,)


class FormAttrDecorator(specials.AttrDecorator):
	xmlns = xmlns
	class Attrs(html.form.Attrs):
		pass
	decoratable = (html.form,)


class TextAreaAttrDecorator(specials.AttrDecorator):
	xmlns = xmlns
	class Attrs(html.textarea.Attrs):
		pass
	decoratable = (html.textarea,)
