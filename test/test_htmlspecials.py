#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2006 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


import py.test

from ll.xist import converters
from ll.xist.ns import htmlspecials


def test_pixel():
	e = htmlspecials.pixel()
	assert str(e.conv().attrs.src) == "root:px/spc.gif"

	e = htmlspecials.pixel(src="root:nix.gif")
	assert str(e.conv().attrs.src) == "root:nix.gif"

	c = converters.Converter()
	c[htmlspecials.pixel].src = "root:spam.gif"
	e = htmlspecials.pixel()
	assert str(e.conv(c).attrs.src) == "root:spam.gif"

	e = htmlspecials.pixel(color="red")
	assert str(e.conv().attrs.style) == "background-color: red;"

	e = htmlspecials.pixel(color="red", style="display: block;")
	assert str(e.conv().attrs.style) == "background-color: red; display: block;"

