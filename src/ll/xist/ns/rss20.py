#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2006 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
This is a namespace module implementing RSS 2.0.
"""

__version__ = "$Revision$".split()[1]
# $Source$


from ll.xist import xsc, sims


class rss(xsc.Element):
	"""
	The root element.
	"""
	class Attrs(xsc.Element.Attrs):
		class version(xsc.TextAttr):
			required = True
			default = "2.0"
			values = ("2.0",)


class channel(xsc.Element):
	"""
	Information about a particular channel. Everything pertaining to an individual
	channel is contained within this tag.
	"""


class title(xsc.Element):
	"""
	The name of the <pyref class="channel"><class>channel</class></pyref>,
	<pyref class="item"><class>item</class></pyref>,
	<pyref class="image"><class>image</class></pyref> or
	<pyref class="textInput"><class>textInput</class></pyref>.
	"""


class link(xsc.Element):
	"""
	The &url;to the &html; website corresponding to the
	<pyref class="channel"><class>channel</class></pyref>,
	<pyref class="item"><class>item</class></pyref> or
	<pyref class="image"><class>image</class></pyref>.
	Inside <pyref class="textInput"><class>textInput</class></pyref> element it's
	the &url; of the CGI script that processes text input requests.
	"""


class description(xsc.Element):
	"""
	Phrase or sentence describing the <pyref class="channel"><class>channel</class></pyref>,
	<pyref class="item"><class>item</class></pyref> or
	<pyref class="textInput"><class>textInput</class></pyref>.
	"""


class language(xsc.Element):
	"""
	The language the channel is written in.
	"""


class copyright(xsc.Element):
	"""
	Copyright notice for content in the channel.
	"""


class managingEditor(xsc.Element):
	"""
	Email address for person responsible for editorial content.
	"""


class webMaster(xsc.Element):
	"""
	Email address for person responsible for technical issues relating to channel.
	"""


class pubDate(xsc.Element):
	"""
	The publication date for the content in the channel.
	"""


class lastBuildDate(xsc.Element):
	"""
	The last time the content of the channel changed.
	"""


class category(xsc.Element):
	"""
	Specify one or more categories that the channel or item belongs to.
	"""
	class Attrs(xsc.Element.Attrs):
		class domain(xsc.TextAttr): pass


class generator(xsc.Element):
	"""
	A string indicating the program used to generate the channel.
	"""


class docs(xsc.Element):
	"""
	A URL that points to the documentation for the format used in the RSS file.
	"""


class cloud(xsc.Element):
	"""
	Allows processes to register with a cloud to be notified of updates to the
	channel, implementing a lightweight publish-subscribe protocol for RSS feeds.
	"""
	class Attrs(xsc.Element.Attrs):
		class domain(xsc.TextAttr): pass
		class port(xsc.IntAttr): pass
		class path(xsc.IntAttr): pass
		class registerProcedure(xsc.IntAttr): pass
		class protocol(xsc.IntAttr): pass


class ttl(xsc.Element):
	"""
	<class>ttl</class> stands for time to live. It's a number of minutes that
	indicates how long a channel can be cached before refreshing from the source.
	"""
	pass


class image(xsc.Element):
	"""
	Specifies a GIF, JPEG or PNG image that can be displayed with the channel.
	"""


class textInput(xsc.Element):
	"""
	Specifies a text input box that can be displayed with the channel.
	"""


class name(xsc.Element):
	"""
	The name of the text object in the 
	<pyref class="textInput"><class>textInput</class></pyref> area.
	"""


class skipHours(xsc.Element):
	"""
	A hint for aggregators telling them which hours they can skip.
	"""


class skipDays(xsc.Element):
	"""
	A hint for aggregators telling them which days they can skip.
	"""


class day(xsc.Element):
	"""
	The day of the week, spelled out in English.
	"""


class hour(xsc.Element):
	"""
	Specifies an hour of the day. Should be an integer value between 0 and 23.
	See <pyref class="skipHours"><class>skipHours</class></pyref>.
	"""


class url(xsc.Element):
	"""
	The URL of a GIF, JPEG or PNG image that represents the channel.
	"""


class width(xsc.Element):
	"""
	Image width.
	"""


class height(xsc.Element):
	"""
	Image height.
	"""


class item(xsc.Element):
	"""
	An item that is associated with a <pyref class="channel"><class>channel</class></pyref>.
	The item should represent a web-page, or subsection within a web page.
	It should have a unique &url; associated with it. Each item must contain a
	<pyref class="title"><class>title</class></pyref> or
	<pyref class="description"><class>description</class></pyref>.
	"""

class author(xsc.Element):
	"""
	Author of an <pyref class="item"><class>item</class></pyref>.
	"""


class comments(xsc.Element):
	"""
	&url; of a page for comments relating to the item.
	"""


class enclosure(xsc.Element):
	"""
	Describes a media object that is attached to the item.
	"""
	class Attrs(xsc.Element.Attrs):
		class url(xsc.URLAttr): required = True
		class length(xsc.IntAttr): required = True
		class type(xsc.TextAttr): required = True


class guid(xsc.Element):
	"""
	A string that uniquely identifies the item.
	"""
	class Attrs(xsc.Element.Attrs):
		class isPermaLink(xsc.URLAttr):
			values = ("false", "true")


class source(xsc.Element):
	"""
	The RSS channel that the item came from.
	"""
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


class __ns__(xsc.Namespace):
	xmlname = "rss"
	xmlurl = "http://feedvalidator.org/docs/rss2.html" # Just a guess
__ns__.makemod(vars())
