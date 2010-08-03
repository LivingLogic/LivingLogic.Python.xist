#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll.xist import xsc
from ll.xist.ns import xml, htmlspecials


def test_pixel():
	e = htmlspecials.pixel()
	assert unicode(e.conv().attrs.src) == u"root:px/spc.gif"

	e = htmlspecials.pixel(src=u"root:nix.gif")
	assert unicode(e.conv().attrs.src) == u"root:nix.gif"

	c = xsc.Converter()
	c[htmlspecials.pixel].src = u"root:spam.gif"
	e = htmlspecials.pixel()
	assert unicode(e.conv(c).attrs.src) == u"root:spam.gif"

	e = htmlspecials.pixel(color=u"red")
	assert unicode(e.conv().attrs.style) == u"background-color: red;"

	e = htmlspecials.pixel(color=u"red", style=u"display: block;")
	assert unicode(e.conv().attrs.style) == u"background-color: red; display: block;"


def test_html():
	# Without a conversion language ``htmlspecials.html`` will not touch the language attributes
	e = htmlspecials.html().conv()
	assert "lang" not in e.attrs
	assert xml.Attrs.lang not in e.attrs

	e = htmlspecials.html().conv(lang="de")
	assert unicode(e.attrs.lang) == "de"
	assert unicode(e.attrs[xml.Attrs.lang]) == "de"

	# If ``lang`` is given ``htmlspecials.html`` will not touch it
	e = htmlspecials.html(lang="en").conv(lang="de")
	assert unicode(e.attrs.lang) == "en"
	assert unicode(e.attrs[xml.Attrs.lang]) == "de"

	# If ``xml:lang`` is given ``htmlspecials.html`` will not touch it
	e = htmlspecials.html(xml.Attrs(lang="en")).conv(lang="de")
	assert unicode(e.attrs.lang) == "de"
	assert unicode(e.attrs[xml.Attrs.lang]) == "en"
