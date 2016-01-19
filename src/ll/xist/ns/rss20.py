# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2007-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2007-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This is a namespace module implementing RSS 2.0.
"""


from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://feedvalidator.org/docs/rss2.html" # Just a guess


class rss(xsc.Element):
	"""
	The root element.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class version(xsc.TextAttr):
			required = True
			default = "2.0"
			values = ("2.0",)


class channel(xsc.Element):
	"""
	Information about a particular channel. Everything pertaining to an
	individual channel is contained within this tag.
	"""
	xmlns = xmlns


class title(xsc.Element):
	"""
	The name of the :class:`channel`, :class:`item`, :class:`image` or
	:class:`textInput`.
	"""
	xmlns = xmlns


class link(xsc.Element):
	"""
	The URLto the HTML website corresponding to the :class:`channel`,
	:class:`item` or :class:`image`. Inside :class:`textInput` element it's
	the URL of the CGI script that processes text input requests.
	"""
	xmlns = xmlns


class description(xsc.Element):
	"""
	Phrase or sentence describing the :class:`channel`, :class:`item` or
	:class:`textInput`.
	"""
	xmlns = xmlns


class language(xsc.Element):
	"""
	The language the channel is written in.
	"""
	xmlns = xmlns


class copyright(xsc.Element):
	"""
	Copyright notice for content in the channel.
	"""
	xmlns = xmlns


class managingEditor(xsc.Element):
	"""
	Email address for person responsible for editorial content.
	"""
	xmlns = xmlns


class webMaster(xsc.Element):
	"""
	Email address for person responsible for technical issues relating to channel.
	"""
	xmlns = xmlns


class pubDate(xsc.Element):
	"""
	The publication date for the content in the channel.
	"""
	xmlns = xmlns


class lastBuildDate(xsc.Element):
	"""
	The last time the content of the channel changed.
	"""
	xmlns = xmlns


class category(xsc.Element):
	"""
	Specify one or more categories that the channel or item belongs to.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class domain(xsc.TextAttr): pass


class generator(xsc.Element):
	"""
	A string indicating the program used to generate the channel.
	"""
	xmlns = xmlns


class docs(xsc.Element):
	"""
	A URL that points to the documentation for the format used in the RSS file.
	"""
	xmlns = xmlns


class cloud(xsc.Element):
	"""
	Allows processes to register with a cloud to be notified of updates to the
	channel, implementing a lightweight publish-subscribe protocol for RSS feeds.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class domain(xsc.TextAttr): pass
		class port(xsc.IntAttr): pass
		class path(xsc.IntAttr): pass
		class registerProcedure(xsc.IntAttr): pass
		class protocol(xsc.IntAttr): pass


class ttl(xsc.Element):
	"""
	:class:`ttl` stands for time to live. It's a number of minutes that
	indicates how long a channel can be cached before refreshing from the
	source.
	"""
	xmlns = xmlns


class image(xsc.Element):
	"""
	Specifies a GIF, JPEG or PNG image that can be displayed with the channel.
	"""
	xmlns = xmlns


class textInput(xsc.Element):
	"""
	Specifies a text input box that can be displayed with the channel.
	"""
	xmlns = xmlns


class name(xsc.Element):
	"""
	The name of the text object in the  :class:`textInput` area.
	"""
	xmlns = xmlns


class skipHours(xsc.Element):
	"""
	A hint for aggregators telling them which hours they can skip.
	"""
	xmlns = xmlns


class skipDays(xsc.Element):
	"""
	A hint for aggregators telling them which days they can skip.
	"""
	xmlns = xmlns


class day(xsc.Element):
	"""
	The day of the week, spelled out in English.
	"""
	xmlns = xmlns


class hour(xsc.Element):
	"""
	Specifies an hour of the day. Should be an integer value between 0 and 23.
	See :class:`skipHours`.
	"""
	xmlns = xmlns


class url(xsc.Element):
	"""
	The URL of a GIF, JPEG or PNG image that represents the channel.
	"""
	xmlns = xmlns


class width(xsc.Element):
	"""
	Image width.
	"""
	xmlns = xmlns


class height(xsc.Element):
	"""
	Image height.
	"""
	xmlns = xmlns


class item(xsc.Element):
	"""
	An item that is associated with a :class:`channel`. The item should
	represent a web-page, or subsection within a web page. It should have a
	unique URL associated with it. Each item must contain a :class:`title` or
	:class:`description`.
	"""
	xmlns = xmlns


class author(xsc.Element):
	"""
	Author of an :class:`item`.
	"""
	xmlns = xmlns


class comments(xsc.Element):
	"""
	URL of a page for comments relating to the item.
	"""
	xmlns = xmlns


class enclosure(xsc.Element):
	"""
	Describes a media object that is attached to the item.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class url(xsc.URLAttr): required = True
		class length(xsc.IntAttr): required = True
		class type(xsc.TextAttr): required = True


class guid(xsc.Element):
	"""
	A string that uniquely identifies the item.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class isPermaLink(xsc.TextAttr):
			values = ("false", "true")


class source(xsc.Element):
	"""
	The RSS channel that the item came from.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class url(xsc.URLAttr): required = True


rss.model = sims.Elements(channel)
channel.model = sims.Elements(title, link, description, language, copyright, managingEditor, webMaster, pubDate, lastBuildDate, category, generator, docs, cloud, ttl, image, textInput, skipHours, skipDays, item)
image.model = sims.Elements(url, title, link, width, height)
enclosure.model = \
cloud.model = sims.Empty()
ttl.model = sims.NoElements()
textInput.model = sims.Elements(title, description, name, link)
item.model = sims.Elements(title, link, description, author, category, comments, enclosure, guid, pubDate, source)
skipDays.model = sims.Elements(day)
skipHours.model = sims.Elements(hour)
copyright.model = \
day.model = \
description.model = \
docs.model = \
height.model = \
hour.model = \
language.model = \
lastBuildDate.model = \
link.model = \
managingEditor.model = \
name.model = \
pubDate.model = \
title.model = \
url.model = \
webMaster.model = \
guid.model = \
category.model = \
author.model = \
comments.model = \
source.model = \
generator.model = \
width.model = sims.NoElements()
