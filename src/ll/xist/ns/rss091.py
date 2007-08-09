# -*- coding: iso-8859-1 -*-

## Copyright 2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
This is a namespace module implementing RSS 0.91.
"""


from ll.xist import xsc, sims


xmlns = "http://my.netscape.com/publish/formats/rss-0.91.dtd"


class DocType(xsc.DocType):
	"""
	Document type for RSS 0.91
	"""

	def __init__(self):
		xsc.DocType.__init__(self, 'rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd"')


class channel(xsc.Element):
	"""
	Information about a particular channel. Everything pertaining to an individual
	channel is contained within this tag.
	"""
	xmlns = xmlns


class copyright(xsc.Element):
	"""
	Copyright string.
	"""
	xmlns = xmlns


class day(xsc.Element):
	"""
	The day of the week, spelled out in English.
	"""
	xmlns = xmlns


class description(xsc.Element):
	"""
	A plain text description of an <class>item</class>, <class>channel</class>,
	<class>image</class>, or <class>textinput</class>.
	"""
	xmlns = xmlns


class docs(xsc.Element):
	"""
	This tag should contain a &url; that references a description of the channel.
	"""
	xmlns = xmlns


class height(xsc.Element):
	"""
	Specifies the height of an <pyref class="image"><class>image</class></pyref>.
	Should be an integer value.
	"""
	xmlns = xmlns


class hour(xsc.Element):
	"""
	Specifies an hour of the day. Should be an integer value between 0 and 23.
	See <pyref class="skipHours"><class>skipHours</class></pyref>.
	"""
	xmlns = xmlns


class image(xsc.Element):
	"""
	Specifies an image associated with a
	<pyref class="channel"><class>channel</class></pyref>.
	"""
	xmlns = xmlns


class item(xsc.Element):
	"""
	An item that is associated with a <pyref class="channel"><class>channel</class></pyref>.
	The item should represent a web-page, or subsection within a web page.
	It should have a unique URL associated with it. Each item must contain a
	<pyref class="title"><class>title</class></pyref> and a
	<pyref class="link"><class>link</class></pyref>. A
	<pyref class="description"><class>description</class></pyref> is optional.
	"""
	xmlns = xmlns


class language(xsc.Element):
	"""
	Specifies the language of a channel.
	"""
	xmlns = xmlns


class lastBuildDate(xsc.Element):
	"""
	The last time the channel was modified.
	"""
	xmlns = xmlns


class link(xsc.Element):
	"""
	This is a url that a user is expected to click on, as opposed to a
	<pyref class="url"><class>url</class></pyref> that is for loading a resource,
	such as an image.
	"""
	xmlns = xmlns


class managingEditor(xsc.Element):
	"""
	The email address of the managing editor of the site, the person to contact
	for editorial inquiries.
	"""
	xmlns = xmlns


class name(xsc.Element):
	"""
	The name of an object, corresponding to the <lit>name</lit> attribute of an
	&html; <pyref module="ll.xist.ns.html" class="input"><class>input</class></pyref> element.
	Currently, this only applies to <pyref class="textinput"><class>textinput</class></pyref>.
	"""
	xmlns = xmlns


class pubDate(xsc.Element):
	"""
	Date when channel was published.
	"""
	xmlns = xmlns


class rating(xsc.Element):
	"""
	PICS rating of the channel.
	"""
	xmlns = xmlns


class rss(xsc.Element):
	"""
	Root element.
	"""
	xmlns = xmlns
	class Attrs(xsc.Element.Attrs):
		class version(xsc.TextAttr):
			required = True
			default = "0.91"
			values = ("0.91",)


class skipDays(xsc.Element):
	"""
	A list of <pyref class="day"><class>day</class></pyref>s of the week, in English,
	indicating the days of the week when your channel will not be updated. As
	with <pyref class="activeHours"><class>activeHours</class></pyref>, if you
	know your channel will never be updated on Saturday or Sunday, for example.
	"""
	xmlns = xmlns


class skipHours(xsc.Element):
	"""
	A list of <pyref class="hour"><class>hours</class></pyref> indicating the
	hours in the day, GMT, when the channel is unlikely to be updated. If this
	sub-item is omitted, the channel is assumed to be updated hourly.
	"""
	xmlns = xmlns


class textinput(xsc.Element):
	"""
	An input field for the purpose of allowing users to submit queries back to
	the publisher's site.
	"""
	xmlns = xmlns


class title(xsc.Element):
	"""
	An identifying string for a resource. When used in an
	<pyref class="item"><class>item</class></pyref>, this is the name of the item's
	link. When used in an <pyref class="image"><class>image</class></pyref>, this
	is the <z>alt</z> text for the image. When used in a
	<pyref class="channel"><class>channel</class></pyref>, this is the channel's
	title. When used in a <pyref class="textinput"><class>textinput</class></pyref>,
	this is the the textinput's title.
	"""
	xmlns = xmlns


class url(xsc.Element):
	"""
	Location to load a resource from. Note that this is slightly different from
	the <pyref class="link"><class>link</class></pyref> tag, which specifies where
	a user should be re-directed to if a resource is selected.
	"""
	xmlns = xmlns


class webMaster(xsc.Element):
	"""
	The email address of the webmaster for the site, the person to contact if
	there are technical problems with the channel.
	"""
	xmlns = xmlns


class width(xsc.Element):
	"""
	Specifies the width of an <pyref class="image"><class>image</class></pyref>.
	Should be an integer value.
	"""
	xmlns = xmlns


rss.model = sims.Elements(channel)
skipDays.model = sims.Elements(day)
skipHours.model = sims.Elements(hour)
textinput.model = sims.Elements(link, description, name, title)
item.model = sims.Elements(link, description, title)
channel.model = sims.Elements(rating, skipHours, description, language, title, docs, image, pubDate, webMaster, item, link, skipDays, lastBuildDate, copyright, managingEditor, textinput)
image.model = sims.Elements(width, link, description, title, url, height)
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
rating.model = \
title.model = \
url.model = \
webMaster.model = \
width.model = sims.NoElements()
