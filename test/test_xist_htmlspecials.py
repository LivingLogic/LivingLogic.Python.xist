#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


from ll.xist import xsc, xfind
from ll.xist.ns import xml, html, htmlspecials


def test_pixel():
	e = htmlspecials.pixel()
	assert str(e.conv().attrs.src) == "root:px/spc.gif"

	e = htmlspecials.pixel(src="root:nix.gif")
	assert str(e.conv().attrs.src) == "root:nix.gif"

	c = xsc.Converter()
	c[htmlspecials.pixel].src = "root:spam.gif"
	e = htmlspecials.pixel()
	assert str(e.conv(c).attrs.src) == "root:spam.gif"

	e = htmlspecials.pixel(color="red")
	assert str(e.conv().attrs.style) == "background-color: red;"

	e = htmlspecials.pixel(color="red", style="display: block;")
	assert str(e.conv().attrs.style) == "background-color: red; display: block;"


def test_html():
	# Without a conversion language ``htmlspecials.html`` will not touch the language attributes
	e = htmlspecials.html().conv()
	assert "lang" not in e.attrs
	assert xml.Attrs.lang not in e.attrs

	e = htmlspecials.html().conv(lang="de")
	assert str(e.attrs.lang) == "de"
	assert str(e.attrs[xml.Attrs.lang]) == "de"

	# If ``lang`` is given ``htmlspecials.html`` will not touch it
	e = htmlspecials.html(lang="en").conv(lang="de")
	assert str(e.attrs.lang) == "en"
	assert str(e.attrs[xml.Attrs.lang]) == "de"

	# If ``xml:lang`` is given ``htmlspecials.html`` will not touch it
	e = htmlspecials.html(xml.Attrs(lang="en")).conv(lang="de")
	assert str(e.attrs.lang) == "de"
	assert str(e.attrs[xml.Attrs.lang]) == "en"


def test_plaintable():
	e = htmlspecials.plaintable().conv()
	assert str(e.attrs.border) == "0"
	assert str(e.attrs.cellspacing) == "0"
	assert str(e.attrs.cellpadding) == "0"

	e = htmlspecials.plaintable(border=1, cellspacing=2, cellpadding=3).conv()
	assert str(e.attrs.border) == "1"
	assert str(e.attrs.cellspacing) == "2"
	assert str(e.attrs.cellpadding) == "3"


def test_plainbody():
	e = htmlspecials.plainbody().conv()
	assert str(e.attrs.leftmargin) == "0"
	assert str(e.attrs.topmargin) == "0"
	assert str(e.attrs.marginheight) == "0"
	assert str(e.attrs.marginwidth) == "0"

	e = htmlspecials.plainbody(leftmargin=1, topmargin=2, marginheight=3, marginwidth=4).conv()
	assert str(e.attrs.leftmargin) == "1"
	assert str(e.attrs.topmargin) == "2"
	assert str(e.attrs.marginheight) == "3"
	assert str(e.attrs.marginwidth) == "4"


def test_javascript():
	e = htmlspecials.javascript().conv()
	assert str(e.attrs.language) == "javascript"
	assert str(e.attrs.type) == "text/javascript"


def test_flash():
	e = htmlspecials.flash(src="gurk.flv").conv()
	assert str(e.walknodes(html.param & xfind.attrhasvalue("name", "movie"))[0].attrs.value) == "gurk.flv"
	assert str(e.walknodes(html.embed)[0].attrs.src) == "gurk.flv"


def test_quicktime():
	e = htmlspecials.quicktime(src="gurk.mov").conv()
	assert str(e.walknodes(html.param & xfind.attrhasvalue("name", "src"))[0].attrs.value) == "gurk.mov"
	assert str(e.walknodes(html.embed)[0].attrs.src) == "gurk.mov"
