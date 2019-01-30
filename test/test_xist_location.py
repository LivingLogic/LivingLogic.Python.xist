#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


from ll.xist import xsc


def test_locationeq():
	l1 = xsc.Location(url="http://gurk.com", line=42, col=666)
	l2 = xsc.Location(url="http://gurk.com", line=42, col=666)
	l3 = xsc.Location(url="http://hurz.com", line=42, col=666)
	l4 = xsc.Location(url="http://gurk.com", line=43, col=666)
	l5 = xsc.Location(url="http://gurk.com", line=43, col=667)
	l6 = xsc.Location(url="http://gurk.com")
	assert l1 == l2
	assert l1 != l3
	assert l1 != l4
	assert l1 != l5
	assert l1 != l6


def test_locationoffset():
	l1 = xsc.Location(url="http://gurk.com", line=42, col=666)
	assert l1 == l1.offset(0)
	l2 = l1.offset(1)
	assert l1.url == l2.url
	assert l1.line+1 == l2.line
