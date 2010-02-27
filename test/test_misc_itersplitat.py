#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2009-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll import misc


def test_itersplitat():
	assert tuple(misc.itersplitat("20090609172345", (4, 6, 8, 10, 12))) == ("2009", "06", "09", "17", "23", "45")
	assert tuple(misc.itersplitat("200906091723", (4, 6, 8, 10, 12))) == ("2009", "06", "09", "17", "23")
	assert tuple(misc.itersplitat("20090609172345", (-10, -8, -6, -4, -2))) == ("2009", "06", "09", "17", "23", "45")
