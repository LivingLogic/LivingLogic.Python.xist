#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; namespace that contains definitions for all the elements and
entities in <link href="http://www.w3.org/TR/html4/loose.dtd">&html; 4.0 transitional</link>
(and a few additional ones).</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import cgi # for parse_header

from ll.xist import xsc, utils
from ll.xist.ns import xml


# common attributes types
class DirAttr(xsc.TextAttr): "direction for weak/neutral text"; values = ("ltr", "rtl")
class ContentTypeAttr(xsc.TextAttr): "media type, as per [RFC2045]"
class ContentTypesAttr(xsc.TextAttr): "comma-separated list of media types, as per [RFC2045]"
class CharsetAttr(xsc.TextAttr): "a character encoding, as per [RFC2045]"
class CharsetsAttr(xsc.TextAttr): "a space separated list of character encodings, as per [RFC2045]"
class LanguageCodeAttr(xsc.TextAttr): "a language code, as per [RFC3066]"
class CharacterAttr(xsc.TextAttr): "a single character, as per section 2.2 of [XML]"
class LinkTypesAttr(xsc.TextAttr): "space-separated list of link types"
class MediaDescAttr(xsc.TextAttr): "single or comma-separated list of media descriptors"
class URIListAttr(xsc.TextAttr): "a space separated list of Uniform Resource Identifiers"
class DatetimeAttr(xsc.TextAttr): "date and time information. ISO date format"
class ScriptAttr(xsc.TextAttr): "script expression"
class StyleSheetAttr(xsc.StyleAttr): "style sheet data"
class TextAttr(xsc.TextAttr): "used for titles etc."
class FrameTargetAttr(xsc.TextAttr): "render in this frame"
class LengthAttr(xsc.TextAttr): "<rep>nn</rep> for pixels or <rep>nn%</rep> for percentage length"
class MultiLengthAttr(xsc.TextAttr): "pixel, percentage, or relative"
class PixelsAttr(xsc.IntAttr): "integer representing length in pixels"
class ShapeAttr(xsc.TextAttr): "image shapes"; values = ("rect", "circle", "poly", "default")
class CoordsAttr(xsc.TextAttr): "comma separated list of lengths"
class ImgAlignAttr(xsc.TextAttr): "image alignment"; values = ("top", "middle", "bottom", "left", "right", "absmiddle")
class ColorAttr(xsc.ColorAttr): "a color using sRGB: #RRGGBB as Hex values"
class TextAlignAttr(xsc.TextAttr): "text alignment"; values = ("left", "right", "center", "justify")
class OLStyleAttr(xsc.TextAttr): values = "1aAiI"
class ULStyleAttr(xsc.TextAttr): values = ("disc", "square", "circle")
class InputTypeAttr(xsc.TextAttr): values = ("text", "password", "checkbox", "radio", "submit", "reset", "file", "hidden", "image", "button")
class TRulesAttr(xsc.TextAttr): values = ("none", "groups", "rows", "cols", "all")
class TAlignAttr(xsc.TextAttr): values = ("left", "right", "center")
class CAlignAttr(xsc.TextAttr): values = ("top", "bottom", "left", "right")
class TFrameAttr(xsc.TextAttr): values = ("void", "above", "below", "hsides", "lhs", "rhs", "vsides", "box", "border")
class ScopeAttr(xsc.TextAttr): values = ("row", "col", "rowgroup", "colgroup")


# common attributes sets
class coreattrs(xsc.Element.Attrs):
	"core attributes common to most elements"
	class id(xsc.IDAttr): "document-wide unique id"
	class class_(xsc.TextAttr): "space separated list of classes"; xmlname = "class"
	class style(StyleSheetAttr): "associated style info"
	class title(TextAttr): "advisory title/amplification"


class i18nattrs(xsc.Element.Attrs):
	"internationalization attributes"
	class lang(LanguageCodeAttr): "language code (backwards compatible)"
	class dir(DirAttr): pass


class eventattrs(xsc.Element.Attrs):
	"attributes for common UI events"
	class onclick(ScriptAttr): "a pointer button was clicked"
	class ondblclick(ScriptAttr): "a pointer button was double clicked"
	class onmousedown(ScriptAttr): "a pointer button was pressed down"
	class onmouseup(ScriptAttr): "a pointer button was released"
	class onmousemove(ScriptAttr): "a pointer was moved onto the element"
	class onmouseover(ScriptAttr): "a pointer was moved onto the element" # deprecated
	class onmouseout(ScriptAttr): "a pointer was moved away from the element"
	class onkeypress(ScriptAttr): "a key was pressed and released"
	class onkeydown(ScriptAttr): "a key was pressed down"
	class onkeyup(ScriptAttr): "a key was released"


class focusattrs(xsc.Element.Attrs):
	"attributes for elements that can get the focus"
	class accesskey(CharacterAttr): "accessibility key character"
	class tabindex(xsc.IntAttr): "position in tabbing order"
	class onfocus(ScriptAttr): "the element got the focus"
	class onblur(ScriptAttr): "the element lost the focus"


class allattrs(coreattrs, i18nattrs, eventattrs):
	pass


class cellhalignattrs(xsc.Element.Attrs):
	class align(xsc.TextAttr): values = ("left", "center", "right", "justify", "char")
	class char(CharacterAttr): pass
	class charoff(LengthAttr): pass


class cellvalignattrs(xsc.Element.Attrs):
	class valign(xsc.TextAttr): values = ("top", "middle", "bottom", "baseline")


class DocTypeHTML40transitional(xsc.DocType):
	"""
	document type for HTML 4.0 transitional
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd"')


class DocTypeHTML401transitional(xsc.DocType):
	"""
	document type for HTML 4.01 transitional
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"')


class DocTypeXHTML10strict(xsc.DocType):
	"""
	document type for XHTML 1.0 strict
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"')


class DocTypeXHTML10transitional(xsc.DocType):
	"""
	document type for XHTML 1.0 transitional
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"')

# The global structure of an HTML document
class html(xsc.Element):
	"""
	Document Structure
	"""
	empty = False
	class Attrs(i18nattrs):
		class id(xsc.IDAttr): pass

	def convert(self, converter):
		if converter.lang is not None and (unicode(self["lang"].convert(converter)) != converter.lang or unicode(self[(xml, "lang")].convert(converter)) != converter.lang):
			node = html(self.content, self.attrs, {"lang": converter.lang, (xml, "lang"): converter.lang})
			return node.convert(converter)
		else:
			return super(html, self).convert(converter)


class head(xsc.Element):
	"""
	Document Head
	"""
	empty = False
	class Attrs(i18nattrs):
		class id(xsc.IDAttr): pass
		class profile(xsc.URLAttr): pass


class title(xsc.Element):
	"""
	document title
	"""
	empty = False
	class Attrs(i18nattrs):
		class id(xsc.IDAttr): pass

	def unwrapHTML(self, node, converter):
		if isinstance(node, xsc.Element) and issubclass(node.xmlns, xmlns): # is this one of our own elements => filter it out
			if isinstance(node, img):
				node = node["alt"]
			else:
				node = node.content.mapped(self.unwrapHTML, converter)
		return node

	def convert(self, converter):
		content = self.content.convert(converter)
		content = content.mapped(self.unwrapHTML, converter)
		return title(content, self.attrs)


class base(xsc.Element):
	"""
	document base URI
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class id(xsc.IDAttr): pass
		class href(xsc.URLAttr): pass
		class target(FrameTargetAttr): pass


class meta(xsc.Element):
	"""
	generic metainformation
	"""
	empty = True
	class Attrs(i18nattrs):
		class id(xsc.IDAttr): pass
		class http_equiv(xsc.TextAttr): xmlname = "http-equiv"
		class name(xsc.TextAttr): pass
		class content(xsc.TextAttr): required = True
		class scheme(xsc.TextAttr): pass

	def publish(self, publisher):
		if self.attrs.has("http_equiv"):
			ctype = unicode(self["http_equiv"]).lower()
			if ctype == u"content-type" and self.attrs.has("content"):
				(contenttype, options) = cgi.parse_header(unicode(self["content"]))
				if u"charset" not in options or options[u"charset"] != publisher.encoding:
					options[u"charset"] = publisher.encoding
					node = self.__class__(
						self.attrs,
						http_equiv="Content-Type",
						content=(contenttype, u"; ", u"; ".join([ "%s=%s" % option for option in options.items()]))
					)
					node.publish(publisher)
					return
		super(meta, self).publish(publisher)


class link(xsc.Element):
	"""
	a media-independent link
	"""
	empty = True
	class Attrs(allattrs):
		class charset(CharsetAttr): pass
		class href(xsc.URLAttr): pass
		class hreflang(LanguageCodeAttr): pass
		class type(ContentTypeAttr): pass
		class rel(LinkTypesAttr): pass
		class rev(LinkTypesAttr): pass
		class media(MediaDescAttr): pass
		class target(FrameTargetAttr): pass


class style(xsc.Element):
	"""
	style info, which may include CDATA sections
	"""
	empty = False
	class Attrs(i18nattrs):
		class id(xsc.IDAttr): pass
		class type(ContentTypeAttr): required = True
		class media(MediaDescAttr): pass
		class title(TextAttr): pass


class script(xsc.Element):
	"""
	script statements, which may include CDATA sections
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.IDAttr): pass
		class charset(CharsetAttr): pass
		class type(ContentTypeAttr): required = True
		class language(xsc.TextAttr): pass
		class src(xsc.URLAttr): pass
		class defer(xsc.BoolAttr): pass


class noscript(xsc.Element):
	"""
	alternate content container for non script-based rendering
	"""
	empty = False
	class Attrs(allattrs):
		pass


class iframe(xsc.Element):
	"""
	inline subwindow
	"""
	empty = False
	class Attrs(coreattrs):
		class longdesc(xsc.URLAttr): pass
		class name(xsc.TextAttr): pass
		class src(xsc.URLAttr): pass
		class frameborder(xsc.TextAttr): values = (1, 0)
		class marginwidth(PixelsAttr): pass
		class marginheight(PixelsAttr): pass
		class noresize(xsc.BoolAttr): pass # deprecated
		class scrolling(xsc.TextAttr): values = ("yes", "no", "auto")
		class align(ImgAlignAttr): pass
		class height(LengthAttr): pass
		class width(LengthAttr): pass
		class hspace(xsc.IntAttr): pass # deprecated
		class vspace(xsc.IntAttr): pass # deprecated
		class bordercolor(xsc.ColorAttr): pass # deprecated


class noframes(xsc.Element):
	"""
	alternate content container for non frame-based rendering
	"""
	empty = False
	class Attrs(allattrs):
		pass


class body(xsc.Element):
	"""
	document body
	"""
	empty = False
	class Attrs(allattrs):
		class onload(ScriptAttr): pass
		class onunload(ScriptAttr): pass
		class onfocus(xsc.TextAttr): pass # deprecated
		class background(xsc.URLAttr): pass # deprecated
		class bgcolor(xsc.ColorAttr): pass # deprecated
		class text(xsc.ColorAttr): pass # deprecated
		class link(xsc.ColorAttr): pass # deprecated
		class vlink(xsc.ColorAttr): pass # deprecated
		class alink(xsc.ColorAttr): pass # deprecated
		class leftmargin(xsc.IntAttr): pass # deprecated
		class topmargin(xsc.IntAttr): pass # deprecated
		class marginwidth(xsc.IntAttr): pass # deprecated
		class marginheight(xsc.IntAttr): pass # deprecated


class div(xsc.Element):
	"""
	generic language/style container
	"""
	empty = False
	class Attrs(allattrs):
		class align(TextAlignAttr): pass


class p(xsc.Element):
	"""
	paragraph
	"""
	empty = False
	class Attrs(allattrs):
		class align(TextAlignAttr): pass


class h1(xsc.Element):
	"""
	heading
	"""
	empty = False
	class Attrs(allattrs):
		class align(TextAlignAttr): pass


class h2(xsc.Element):
	"""
	heading
	"""
	empty = False
	class Attrs(allattrs):
		class align(TextAlignAttr): pass


class h3(xsc.Element):
	"""
	heading
	"""
	empty = False
	class Attrs(allattrs):
		class align(TextAlignAttr): pass


class h4(xsc.Element):
	"""
	heading
	"""
	empty = False
	class Attrs(allattrs):
		class align(TextAlignAttr): pass


class h5(xsc.Element):
	"""
	heading
	"""
	empty = False
	class Attrs(allattrs):
		class align(TextAlignAttr): pass


class h6(xsc.Element):
	"""
	heading
	"""
	empty = False
	class Attrs(allattrs):
		class align(TextAlignAttr): pass


class ul(xsc.Element):
	"""
	unordered list
	"""
	empty = False
	class Attrs(allattrs):
		class type(ULStyleAttr): pass
		class compact(xsc.BoolAttr): pass


class ol(xsc.Element):
	"""
	ordered list
	"""
	empty = False
	class Attrs(allattrs):
		class type(OLStyleAttr): pass
		class compact(xsc.BoolAttr): pass
		class start(xsc.IntAttr): pass


class menu(xsc.Element):
	"""
	single column list (deprecated)
	"""
	empty = False
	class Attrs(allattrs):
		class compact(xsc.BoolAttr): pass


class dir(xsc.Element):
	"""
	multiple column list (deprecated)
	"""
	empty = False
	class Attrs(allattrs):
		class compact(xsc.BoolAttr): pass


class li(xsc.Element):
	"""
	list item
	"""
	empty = False
	class Attrs(allattrs):
		class type(xsc.TextAttr): pass
		class value(xsc.IntAttr): pass


class dl(xsc.Element):
	"""
	definition list
	"""
	empty = False
	class Attrs(allattrs):
		class compact(xsc.BoolAttr): pass


class dt(xsc.Element):
	"""
	definition term
	"""
	empty = False
	class Attrs(allattrs):
		pass


class dd(xsc.Element):
	"""
	definition description
	"""
	empty = False
	class Attrs(allattrs):
		pass


class address(xsc.Element):
	"""
	information on author
	"""
	empty = False
	class Attrs(allattrs):
		pass


class hr(xsc.Element):
	"""
	horizontal rule
	"""
	empty = True
	class Attrs(allattrs):
		class align(xsc.TextAttr): values = ("left", "right", "center")
		class noshade(xsc.BoolAttr): pass
		class size(PixelsAttr): pass
		class width(LengthAttr): pass # deprecated
		class color(xsc.ColorAttr): pass # deprecated


class pre(xsc.Element):
	"""
	preformatted text
	"""
	empty = False
	class Attrs(allattrs):
		class width(xsc.IntAttr): pass


class blockquote(xsc.Element):
	"""
	block-like quotes
	"""
	empty = False
	class Attrs(allattrs):
		class cite(xsc.URLAttr): pass


class center(xsc.Element): # deprecated
	"""
	centered block level element
	"""
	empty = False
	class Attrs(allattrs):
		pass


class ins(xsc.Element):
	"""
	inserted text
	"""
	empty = False
	class Attrs(allattrs):
		class cite(xsc.URLAttr): pass
		class datetime(DatetimeAttr): pass


class del_(xsc.Element):
	"""
	deleted text
	"""
	empty = False
	xmlname = "del"
	class Attrs(allattrs):
		class cite(xsc.URLAttr): pass
		class datetime(DatetimeAttr): pass


class a(xsc.Element):
	"""
	anchor
	"""
	empty = False
	class Attrs(allattrs, focusattrs):
		class charset(CharsetAttr): pass
		class type(ContentTypeAttr): pass
		class name(xsc.TextAttr): pass
		class href(xsc.URLAttr): pass
		class hreflang(LanguageCodeAttr): pass
		class rel(LinkTypesAttr): pass
		class rev(LinkTypesAttr): pass
		class shape(ShapeAttr): pass
		class coords(CoordsAttr): pass
		class target(FrameTargetAttr): pass
		class oncontextmenu(xsc.TextAttr): pass # deprecated


class span(xsc.Element):
	"""
	generic language/style container
	"""
	empty = False
	class Attrs(allattrs):
		pass


class bdo(xsc.Element):
	"""
	I18N BiDi over-ride
	"""
	empty = False
	class Attrs(coreattrs, eventattrs):
		class lang(LanguageCodeAttr): pass
		class dir(DirAttr): required = True


class br(xsc.Element):
	"""
	forced line break
	"""
	empty = True
	class Attrs(coreattrs):
		class clear(xsc.TextAttr): values = ("left", "all", "right", "none")


class em(xsc.Element):
	"""
	Indicates emphasis.
	"""
	empty = False
	class Attrs(allattrs):
		pass


class strong(xsc.Element):
	"""
	Indicates stronger emphasis than em.
	"""
	empty = False
	class Attrs(allattrs):
		pass


class dfn(xsc.Element):
	"""
	Indicates that this is the defining instance of the enclosed term.
	"""
	empty = False
	class Attrs(allattrs):
		pass


class code(xsc.Element):
	"""
	Designates a fragment of computer code. 
	"""
	empty = False
	class Attrs(allattrs):
		pass


class samp(xsc.Element):
	"""
	Designates sample output from programs, scripts, etc.
	"""
	empty = False
	class Attrs(allattrs):
		pass


class kbd(xsc.Element):
	"""
	Indicates text to be entered by the user.
	"""
	empty = False
	class Attrs(allattrs):
		pass


class var(xsc.Element):
	"""
	Indicates an instance of a variable or program argument. 
	"""
	empty = False
	class Attrs(allattrs):
		pass


class cite(xsc.Element):
	"""
	Contains a citation or a reference to other sources.
	"""
	empty = False
	class Attrs(allattrs):
		pass


class abbr(xsc.Element):
	"""
	Indicates an abbreviated form (e.g., WWW, HTTP, URI, Mass., etc.)
	"""
	empty = False
	class Attrs(allattrs):
		pass


class acronym(xsc.Element):
	"""
	Indicates an acronym (e.g., WAC, radar, etc.).
	"""
	empty = False
	class Attrs(allattrs):
		pass


class q(xsc.Element):
	"""
	short inline quotation
	"""
	empty = False
	class Attrs(allattrs):
		class cite(xsc.URLAttr): pass


class sub(xsc.Element):
	"""
	subscript
	"""
	empty = False
	class Attrs(allattrs):
		pass


class sup(xsc.Element):
	"""
	superscript
	"""
	empty = False
	class Attrs(allattrs):
		pass


class tt(xsc.Element):
	"""
	teletype or monospaced text style
	"""
	empty = False
	class Attrs(allattrs):
		pass


class i(xsc.Element):
	"""
	italic text style
	"""
	empty = False
	class Attrs(allattrs):
		pass


class b(xsc.Element):
	"""
	bold text style
	"""
	empty = False
	class Attrs(allattrs):
		pass


class big(xsc.Element):
	"""
	large text style
	"""
	empty = False
	class Attrs(allattrs):
		pass


class small(xsc.Element):
	"""
	small text style
	"""
	empty = False
	class Attrs(allattrs):
		pass


class u(xsc.Element):
	"""
	underline text style
	"""
	empty = False
	class Attrs(allattrs):
		pass


class s(xsc.Element):
	"""
	strike-through text style
	"""
	empty = False
	class Attrs(allattrs):
		pass


class strike(xsc.Element):
	"""
	strike-through text style
	"""
	empty = False
	class Attrs(allattrs):
		pass


class basefont(xsc.Element): # deprecated
	"""
	base font size
	"""
	empty = True
	class Attrs(coreattrs, i18nattrs):
		class id(xsc.IDAttr): pass
		class size(xsc.TextAttr): required = True
		class color(xsc.ColorAttr): pass
		class face(xsc.TextAttr): pass


class font(xsc.Element): # deprecated
	"""
	local change to font
	"""
	empty = False
	class Attrs(coreattrs, i18nattrs):
		class face(xsc.TextAttr): pass
		class size(xsc.TextAttr): pass
		class color(xsc.ColorAttr): pass


class object(xsc.Element):
	"""
	generic embedded object
	"""
	empty = False
	class Attrs(allattrs):
		class declare(xsc.BoolAttr): pass
		class classid(xsc.URLAttr): pass
		class codebase(xsc.URLAttr): pass
		class data(xsc.URLAttr): pass
		class type(ContentTypeAttr): pass
		class codetype(ContentTypeAttr): pass
		class archive(URIListAttr): pass
		class standby(TextAttr): pass
		class height(LengthAttr): pass
		class width(LengthAttr): pass
		class usemap(xsc.URLAttr): pass
		class name(xsc.TextAttr): pass
		class tabindex(xsc.IntAttr): pass
		class align(ImgAlignAttr): pass
		class border(PixelsAttr): pass
		class hspace(PixelsAttr): pass
		class vspace(PixelsAttr): pass


class param(xsc.Element):
	"""
	named property value
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class id(xsc.IDAttr): pass
		class name(xsc.TextAttr): required = True
		class value(xsc.TextAttr): pass
		class valuetype(xsc.TextAttr): values = ("data", "ref", "object")
		class type(ContentTypeAttr): pass


class applet(xsc.Element): # deprecated
	"""
	Java applet
	"""
	empty = False
	class Attrs(coreattrs):
		class codebase(xsc.URLAttr): pass
		class archive(xsc.TextAttr): pass
		class code(xsc.TextAttr): pass
		class object(xsc.TextAttr): pass
		class alt(TextAttr): pass
		class name(xsc.TextAttr): pass
		class width(LengthAttr): required = True
		class height(LengthAttr): required = True
		class align(ImgAlignAttr): pass
		class hspace(PixelsAttr): pass
		class vspace(PixelsAttr): pass


class img(xsc.Element):
	"""
	Embedded image
	"""
	empty = True
	class Attrs(allattrs):
		class src(xsc.URLAttr): required = True
		class alt(TextAttr): required = True
		class name(xsc.TextAttr): pass
		class longdesc(xsc.URLAttr): pass
		class width(LengthAttr): pass
		class height(LengthAttr): pass
		class usemap(xsc.URLAttr): pass
		class ismap(xsc.BoolAttr): pass
		class align(ImgAlignAttr): pass
		class border(LengthAttr): pass
		class hspace(PixelsAttr): pass
		class vspace(PixelsAttr): pass
		class lowsrc(xsc.URLAttr): pass # deprecated

	def __unicode__(self):
		return unicode(self["alt"])


class map(xsc.Element):
	"""
	client-side image map
	"""
	empty = False
	class Attrs(i18nattrs, eventattrs):
		class id(xsc.IDAttr): required = True
		class class_(xsc.TextAttr): pass
		class style(StyleSheetAttr): pass
		class title(TextAttr): pass
		class name(xsc.TextAttr): pass


class area(xsc.Element):
	"""
	client-side image map area
	"""
	empty = True
	class Attrs(allattrs, focusattrs):
		class shape(ShapeAttr): pass
		class coords(CoordsAttr): pass
		class href(xsc.URLAttr): pass
		class nohref(xsc.BoolAttr): pass
		class alt(TextAttr): required = True
		class target(FrameTargetAttr): pass


class form(xsc.Element):
	"""
	interactive form
	"""
	empty = False
	class Attrs(allattrs):
		class action(xsc.URLAttr): required = True
		class method(xsc.TextAttr): values = ("get", "post")
		class name(xsc.TextAttr): pass
		class enctype(ContentTypeAttr): pass
		class onsubmit(ScriptAttr): pass
		class onreset(ScriptAttr): pass
		class accept_charset(CharsetsAttr): xmlname = "accept-charset"
		class target(FrameTargetAttr): pass


class label(xsc.Element):
	"""
	form field label text
	"""
	empty = False
	class Attrs(allattrs):
		class for_(xsc.TextAttr): xmlname = "for"
		class accesskey(CharacterAttr): pass
		class onfocus(ScriptAttr): pass
		class onblur(ScriptAttr): pass


class input(xsc.Element):
	"""
	form control
	"""
	empty = True
	class Attrs(allattrs, focusattrs):
		class type(InputTypeAttr): pass
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass
		class checked(xsc.BoolAttr): pass
		class disabled(xsc.BoolAttr): pass
		class readonly(xsc.BoolAttr): pass
		class size(xsc.TextAttr): pass
		class maxlength(xsc.IntAttr): pass
		class src(xsc.URLAttr): pass
		class alt(xsc.TextAttr): pass
		class usemap(xsc.URLAttr): pass
		class onselect(ScriptAttr): pass
		class onchange(ScriptAttr): pass
		class accept(ContentTypesAttr): pass
		class align(ImgAlignAttr): pass
		class border(xsc.IntAttr): pass # deprecated


class select(xsc.Element):
	"""
	option selector
	"""
	empty = False
	class Attrs(allattrs):
		class name(xsc.TextAttr): pass
		class size(xsc.IntAttr): pass
		class multiple(xsc.BoolAttr): pass
		class disabled(xsc.BoolAttr): pass
		class tabindex(xsc.IntAttr): pass
		class onfocus(ScriptAttr): pass
		class onblur(ScriptAttr): pass
		class onchange(ScriptAttr): pass
		class rows(xsc.TextAttr): pass # deprecated


class optgroup(xsc.Element):
	"""
	option group
	"""
	empty = False
	class Attrs(allattrs):
		class disabled(xsc.BoolAttr): pass
		class label(TextAttr): required = True


class option(xsc.Element):
	"""
	selectable choice
	"""
	empty = False
	class Attrs(allattrs):
		class selected(xsc.BoolAttr): pass
		class disabled(xsc.BoolAttr): pass
		class label(TextAttr): pass
		class value(xsc.TextAttr): pass


class textarea(xsc.Element):
	"""
	multi-line text field
	"""
	empty = False
	class Attrs(allattrs, focusattrs):
		class name(xsc.TextAttr): pass
		class rows(xsc.IntAttr): required = True
		class cols(xsc.IntAttr): required = True
		class disabled(xsc.BoolAttr): pass
		class readonly(xsc.BoolAttr): pass
		class onselect(ScriptAttr): pass
		class onchange(ScriptAttr): pass
		class wrap(xsc.TextAttr): values = ("virtual", "physical", "off") # deprecated


class fieldset(xsc.Element):
	"""
	form control group
	"""
	empty = False
	class Attrs(allattrs):
		pass


class legend(xsc.Element):
	"""
	fieldset legend
	"""
	empty = False
	class Attrs(allattrs):
		class accesskey(xsc.TextAttr): pass
		class align(xsc.TextAttr): values = ("top", "bottom", "left", "right")


class button(xsc.Element):
	"""
	push button
	"""
	empty = False
	class Attrs(allattrs, focusattrs):
		class name(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass
		class type(xsc.TextAttr): values = ("button", "submit", "reset")
		class disabled(xsc.BoolAttr): pass


class isindex(xsc.Element):
	empty = True
	class Attrs(coreattrs, i18nattrs):
		class prompt(TextAttr): pass


class table(xsc.Element):
	"""
	table
	"""
	empty = False
	class Attrs(allattrs):
		class summary(TextAttr): pass
		class width(LengthAttr): pass
		class border(PixelsAttr): pass
		class frame(TFrameAttr): pass
		class rules(TRulesAttr): pass
		class cellspacing(LengthAttr): pass
		class cellpadding(LengthAttr): pass
		class align(TAlignAttr): pass
		class bgcolor(xsc.ColorAttr): pass # deprecated
		class height(xsc.TextAttr): pass # deprecated
		class background(xsc.URLAttr): pass # deprecated
		class bordercolor(xsc.ColorAttr): pass # deprecated
		class hspace(xsc.IntAttr): pass # deprecated
		class vspace(xsc.IntAttr): pass # deprecated


class caption(xsc.Element):
	"""
	table caption
	"""
	empty = False
	class Attrs(allattrs):
		class align(CAlignAttr): pass


class colgroup(xsc.Element):
	"""
	table column group
	"""
	empty = False
	class Attrs(allattrs, cellhalignattrs, cellvalignattrs):
		class span(xsc.TextAttr): pass
		class width(MultiLengthAttr): pass


class col(xsc.Element):
	"""
	table column
	"""
	empty = False
	class Attrs(allattrs, cellhalignattrs, cellvalignattrs):
		class span(xsc.TextAttr): pass
		class width(MultiLengthAttr): pass


class thead(xsc.Element):
	"""
	table header
	"""
	empty = False
	class Attrs(allattrs, cellhalignattrs, cellvalignattrs):
		pass


class tfoot(xsc.Element):
	"""
	table footer
	"""
	empty = False
	class Attrs(allattrs, cellhalignattrs, cellvalignattrs):
		pass


class tbody(xsc.Element):
	"""
	table body
	"""
	empty = False
	class Attrs(allattrs, cellhalignattrs, cellvalignattrs):
		pass


class tr(xsc.Element):
	"""
	table row
	"""
	empty = False
	class Attrs(allattrs, cellhalignattrs, cellvalignattrs):
		class bgcolor(xsc.ColorAttr): pass
		class nowrap(xsc.BoolAttr): pass # deprecated
		class width(LengthAttr): pass # deprecated
		class background(xsc.URLAttr): pass # deprecated


class th(xsc.Element):
	"""
	table header cell
	"""
	empty = False
	class Attrs(allattrs, cellhalignattrs, cellvalignattrs):
		class abbr(TextAttr): pass
		class axis(xsc.TextAttr): pass
		class headers(xsc.TextAttr): pass
		class scope(ScopeAttr): pass
		class rowspan(xsc.IntAttr): pass
		class colspan(xsc.IntAttr): pass
		class nowrap(xsc.BoolAttr): pass
		class bgcolor(xsc.ColorAttr): pass
		class width(LengthAttr): pass
		class height(LengthAttr): pass
		class background(xsc.URLAttr): pass # deprecated
		class bordercolor(xsc.ColorAttr): pass # deprecated


class td(xsc.Element):
	"""
	table data cell
	"""
	empty = False
	class Attrs(allattrs, cellhalignattrs, cellvalignattrs):
		class abbr(TextAttr): pass
		class axis(xsc.TextAttr): pass
		class headers(xsc.TextAttr): pass
		class scope(ScopeAttr): pass
		class rowspan(xsc.IntAttr): pass
		class colspan(xsc.IntAttr): pass
		class nowrap(xsc.BoolAttr): pass
		class bgcolor(xsc.ColorAttr): pass
		class width(LengthAttr): pass
		class height(LengthAttr): pass
		class background(xsc.URLAttr): pass # deprecated
		class bordercolor(xsc.ColorAttr): pass # deprecated


class embed(xsc.Element):
	"""
	generic embedded object (Internet Exploder)
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class width(xsc.TextAttr): pass
		class height(xsc.TextAttr): pass
		class src(xsc.URLAttr): pass
		class controller(xsc.TextAttr): pass
		class href(xsc.URLAttr): pass
		class target(xsc.TextAttr): pass
		class border(xsc.IntAttr): pass
		class pluginspage(xsc.URLAttr): pass
		class quality(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
		class bgcolor(xsc.ColorAttr): pass
		class menu(xsc.TextAttr): pass # deprecated


# The pain, the pain ...
class frameset(xsc.Element):
	"""
	window subdivision
	"""
	empty = False
	class Attrs(coreattrs):
		class rows(xsc.TextAttr): pass
		class cols(xsc.TextAttr): pass
		class onload(xsc.TextAttr): pass
		class onunload(xsc.TextAttr): pass
		class framespacing(xsc.TextAttr): pass # deprecated
		class border(xsc.IntAttr): pass # deprecated
		class marginwidth(xsc.IntAttr): pass # deprecated
		class marginheight(xsc.IntAttr): pass # deprecated
		class frameborder(xsc.IntAttr): pass # deprecated
		class noresize(xsc.BoolAttr): pass # deprecated
		class scrolling(xsc.TextAttr): pass # deprecated


class frame(xsc.Element):
	"""
	subwindow
	"""
	empty = True
	class Attrs(coreattrs):
		class longdesc(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class src(xsc.URLAttr): pass
		class frameborder(xsc.TextAttr): pass
		class marginwidht(xsc.TextAttr): pass
		class marginheight(xsc.TextAttr): pass
		class noresize(xsc.BoolAttr): pass
		class scrolling(xsc.TextAttr): pass
		class framespacing(xsc.TextAttr): pass # deprecated
		class border(xsc.IntAttr): pass # deprecated
		class marginwidth(xsc.IntAttr): pass # deprecated
		class marginheight(xsc.IntAttr): pass # deprecated
		class frameborder(xsc.IntAttr): pass # deprecated
		class noresize(xsc.BoolAttr): pass # deprecated
		class scrolling(xsc.TextAttr): pass # deprecated


# More pain
class nobr(xsc.Element): # deprecated
	"""
	prevents line breaks
	"""
	empty = False


class xmlns(xsc.Namespace):
	xmlname = "html"
	xmlurl = "http://www.w3.org/1999/xhtml"
xmlns.makemod(vars())

