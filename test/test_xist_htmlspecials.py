#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


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
