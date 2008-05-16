#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2005-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import py.test

from ll import misc


def test_pool():
	pool = misc.Pool(misc)
	assert pool.Pool is pool["Pool"] is misc.Pool
