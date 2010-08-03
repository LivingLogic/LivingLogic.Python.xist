#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll.xist import xsc, xfind
from ll.xist.ns import xml, html, htmlspecials


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
	assert u"lang" not in e.attrs
	assert xml.Attrs.lang not in e.attrs

	e = htmlspecials.html().conv(lang=u"de")
	assert unicode(e.attrs.lang) == u"de"
	assert unicode(e.attrs[xml.Attrs.lang]) == u"de"

	# If ``lang`` is given ``htmlspecials.html`` will not touch it
	e = htmlspecials.html(lang=u"en").conv(lang=u"de")
	assert unicode(e.attrs.lang) == u"en"
	assert unicode(e.attrs[xml.Attrs.lang]) == u"de"

	# If ``xml:lang`` is given ``htmlspecials.html`` will not touch it
	e = htmlspecials.html(xml.Attrs(lang=u"en")).conv(lang=u"de")
	assert unicode(e.attrs.lang) == u"de"
	assert unicode(e.attrs[xml.Attrs.lang]) == u"en"


def test_plaintable():
	e = htmlspecials.plaintable().conv()
	assert unicode(e.attrs.border) == u"0"
	assert unicode(e.attrs.cellspacing) == u"0"
	assert unicode(e.attrs.cellpadding) == u"0"

	e = htmlspecials.plaintable(border=1, cellspacing=2, cellpadding=3).conv()
	assert unicode(e.attrs.border) == u"1"
	assert unicode(e.attrs.cellspacing) == u"2"
	assert unicode(e.attrs.cellpadding) == u"3"


def test_plainbody():
	e = htmlspecials.plainbody().conv()
	assert unicode(e.attrs.leftmargin) == u"0"
	assert unicode(e.attrs.topmargin) == u"0"
	assert unicode(e.attrs.marginheight) == u"0"
	assert unicode(e.attrs.marginwidth) == u"0"

	e = htmlspecials.plainbody(leftmargin=1, topmargin=2, marginheight=3, marginwidth=4).conv()
	assert unicode(e.attrs.leftmargin) == u"1"
	assert unicode(e.attrs.topmargin) == u"2"
	assert unicode(e.attrs.marginheight) == u"3"
	assert unicode(e.attrs.marginwidth) == u"4"


def test_javascript():
	e = htmlspecials.javascript().conv()
	assert unicode(e.attrs.language) == u"javascript"
	assert unicode(e.attrs.type) == "text/javascript"


def test_flash():
	e = htmlspecials.flash(src="gurk.flv").conv()
	assert unicode(e.walknodes(html.param & xfind.attrhasvalue("name", "movie"))[0].attrs.value) == u"gurk.flv"
	assert unicode(e.walknodes(html.embed)[0].attrs.src) == u"gurk.flv"


def test_quicktime():
	e = htmlspecials.quicktime(src="gurk.mov").conv()
	assert unicode(e.walknodes(html.param & xfind.attrhasvalue("name", "src"))[0].attrs.value) == u"gurk.mov"
	assert unicode(e.walknodes(html.embed)[0].attrs.src) == u"gurk.mov"
