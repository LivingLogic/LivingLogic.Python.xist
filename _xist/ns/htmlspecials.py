#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
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

import sys, types, time as time_, string, warnings

from ll.xist import xsc, parsers, sims
from ll.xist.ns import ihtml, html, meta, specials


class plaintable(html.table):
	"""
	<par>a &html; table where the values of the attributes <lit>cellpadding</lit>,
	<lit>cellspacing</lit> and <lit>border</lit> default to <lit>0</lit>.</par>
	"""
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
	class Attrs(html.img.Attrs):
		class color(xsc.TextAttr):
			"""
			The pixel color as a three digit hex value or <lit>spc</lit> to
			get a transparent pixel.
			"""
			default = u"spc"

			def checkvalid(self):
				if len(self) and not self.isfancy():
					content = unicode(self)
					if content != u"spc":
						if len(content) == 3:
							for c in content:
								if c not in u"0369cf":
									warnings.warn(xsc.IllegalAttrValueWarning(self))
						else:
							warnings.warn(xsc.IllegalAttrValueWarning(self))

		class alt(html.img.Attrs.alt):
			default = ""


class pixel(_pixelbase):
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

	class Attrs(_pixelbase.Attrs):
		class width(html.img.Attrs.width):
			default = 1
		class height(html.img.Attrs.height):
			default = 1
		src = None # remove source attribute

	def convert(self, converter):
		self.attrs.checkvalid()
		e = converter.target.img(
			self.attrs.without([u"color"]),
			src=(u"root:px/", self[u"color"], u".gif")
		)
		return e.convert(converter)


class autoimg(html.img):
	"""
	<par>An image were width and height attributes are automatically generated.</par>
	
	<par>If the attributes are already there, they won't be modified.</par>
	"""
	def convert(self, converter):
		target = converter.target
		if issubclass(target, (ihtml, html)):
			e = target.img(self.attrs.convert(converter))
		else:
			raise ValueError("unknown conversion target %r" % target)
		src = self[u"src"].convert(converter).forInput(converter.root)
		e._addimagesizeattributes(src, u"width", u"height")
		return e


class autopixel(_pixelbase):
	"""
	<par>A pixel image were width and height attributes are automatically generated.</par>
	
	<par>This works like <pyref class="pixel"><class>pixel</class></pyref> but the
	size is <z>inherited</z> from the image specified via the <lit>src</lit> attribute.</par>
	"""

	def convert(self, converter):
		target = converter.target
		if not issubclass(target, (ihtml, html)):
			raise ValueError("unknown conversion target %r" % target)
		self.attrs.checkvalid()
		e = target.img(self.attrs.without([u"color"]))
		src = self[u"src"].convert(converter).forInput(converter.root)
		e._addimagesizeattributes(src, u"width", u"height")
		e[u"src"] = (u"root:px/", self[u"color"], u".gif")
		return e


class autoinput(html.input):
	"""
	<par>Extends <pyref module="ll.xist.ns.html" class="input"><class>input</class></pyref>
	with the ability to automatically set the size, if this element
	has <lit>type=="image"</lit>.</par>
	"""
	def convert(self, converter):
		target = converter.target
		e = target.input(self.content, self.attrs)
		if u"type" in self.attrs and unicode(self[u"type"].convert(converter)) == u"image":
			src = self[u"src"].convert(converter).forInput(converter.root)
			e._addimagesizeattributes(src, u"size", None) # no height
		return e.convert(converter)


class redirectpage(xsc.Element):
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
	<par>can be used for javascript.</par>
	"""
	class Attrs(html.script.Attrs):
		language = None
		type = None

	def convert(self, converter):
		target = converter.target
		e = target.script(self.content, self.attrs, language=u"javascript", type=u"text/javascript")
		return e.convert(converter)


class flash(xsc.Element):
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
	class Attrs(html.img.Attrs):
		pass
	idecoratable = (html.img,)


class InputAttrDecorator(specials.AttrDecorator):
	class Attrs(html.input.Attrs):
		pass
	decoratable = (html.input,)


class FormAttrDecorator(specials.AttrDecorator):
	class Attrs(html.form.Attrs):
		pass
	decoratable = (html.form,)


class TextAreaAttrDecorator(specials.AttrDecorator):
	class Attrs(html.textarea.Attrs):
		pass
	decoratable = (html.textarea,)


class __ns__(xsc.Namespace):
	xmlname = "htmlspecials"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/htmlspecials"
__ns__.makemod(vars())
