#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2009 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll import misc


def test_gzip():
	assert misc.gunzip(misc.gzip("gurk", 0)) == "gurk"
	assert misc.gunzip(misc.gzip("gurk", 9)) == "gurk"
