# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST module that contains elements that simplify handling meta data. All
elements in this module will generate a :class:`ll.xist.ns.html.meta` element
when converted.
"""


from ll.xist import xsc, sims
from ll.xist.ns import ihtml, html


__docformat__ = "reStructuredText"


xmlns = "http://xmlns.livinglogic.de/xist/ns/meta"


class contenttype(html.meta):
	"""
	Can be used for a ``<meta http-equiv="Content-Type" content="text/html"/>``,
	where the character set will be automatically inserted on a call to
	:meth:`ll.xist.xsc.Node.publish`.

	Usage is simple: ``meta.contenttype()``.
	"""
	xmlns = xmlns
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None
		class mimetype(xsc.TextAttr):
			required = True
			default = "text/html"

	def convert(self, converter):
		target = converter.target
		if target.xmlns in (ihtml.xmlns, html.xmlns):
			e = target.meta(
				self.attrs.withoutnames("mimetype"),
				http_equiv="Content-Type",
				content=self["mimetype"],
			)
		else:
			raise ValueError(f"unknown conversion target {target!r}")
		return e.convert(converter)

	def publish(self, publisher):
		# fall back to the Element method
		return xsc.Element.publish(self, publisher) # return a generator-iterator


class contentscripttype(html.meta):
	"""
	Can be used for a ``<meta http-equiv="Content-Script-Type" content="..."/>``.

	Usage is simple: ``<markup>meta.contentscripttype(type="text/javascript")``.
	"""
	xmlns = xmlns
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None
		class type(xsc.TextAttr): pass

	def convert(self, converter):
		e = html.meta(self.attrs.withoutnames("type"))
		e.attrs["http-equiv"] = "Content-Script-Type"
		e.attrs["content"] = self["type"]
		return e.convert(converter)


class keywords(html.meta):
	"""
	Can be used for a ``<meta name="keywords" content="..."/>``.

	Usage is simple: ``meta.keywords("foo, bar")``.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None

	def convert(self, converter):
		e = html.meta(self.attrs)
		e.attrs["name"] = "keywords"
		e.attrs["content"] = self.content
		return e.convert(converter)


class description(html.meta):
	"""
	Can be used for a ``<meta name="description" content="..."/>``.

	Usage is simple: ``meta.description("This page describes the ...")``.
	"""
	xmlns = xmlns
	model = sims.NoElements()
	class Attrs(html.meta.Attrs):
		http_equiv = None
		name = None
		content = None

	def convert(self, converter):
		e = html.meta(self.attrs)
		e.attrs["name"] = "description"
		e.attrs["content"] = self.content
		return e.convert(converter)


class stylesheet(html.link):
	"""
	Can be used for a ``<link rel="stylesheet" type="text/css" href="..."/>``.

	Usage is simple: ``meta.stylesheet(href="root:stylesheets/main.css")``.
	"""
	xmlns = xmlns
	class Attrs(html.link.Attrs):
		rel = None
		type = None

	def convert(self, converter):
		e = html.link(self.attrs, rel="stylesheet", type="text/css")
		return e.convert(converter)


class made(html.link):
	"""
	Can be used for a ``<link rel="made" href="mailto:..."/>``.

	Usage is simple: ``meta.made(href="foobert@bar.org")``.
	"""
	xmlns = xmlns
	class Attrs(html.link.Attrs):
		rel = None

	def convert(self, converter):
		e = html.link(self.attrs, rel="made", href=("mailto:", self["href"]))
		return e.convert(converter)


class author(xsc.Element):
	"""
	Can be used to embed author information in the header. It will generate
	``<link rel="made"/>`` and ``<meta name="author"/>`` elements.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class lang(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class email(xsc.TextAttr): pass

	def convert(self, converter):
		e = xsc.Frag()
		if "name" in self.attrs:
			e.append(html.meta(name="author", content=self.attrs["name"]))
			if "lang" in self.attrs:
				e[-1].attrs["lang"] = self["lang"]
		if "email" in self.attrs:
			e.append(html.link(rel="made", href=("mailto:", self["email"])))
		return e.convert(converter)


class refresh(xsc.Element):
	"""
	A refresh header.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(xsc.Element.Attrs):
		class secs(xsc.IntAttr):
			default = 0
		class href(xsc.URLAttr): pass

	def convert(self, converter):
		e = html.meta(http_equiv="Refresh", content=(self.attrs["secs"], "; url=", self.attrs["href"]))
		return e.convert(converter)
