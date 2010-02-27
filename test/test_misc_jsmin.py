#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2009-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll import misc


def test_jsmin():
	assert misc.jsmin("gurk \t = \t 42;") == "gurk=42;"
