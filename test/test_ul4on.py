#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2011-2012 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2011-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import io, os, datetime

from ll import ul4on, color

import py.test


def test_all():
	def check(data):
		data2 = ul4on.loads(ul4on.dumps(data))
		assert data2 == data

	yield check, None
	yield check, False
	yield check, True
	yield check, 42
	yield check, "gurk"
	yield check, color.Color(0x66, 0x99, 0xcc, 0xff)
	yield check, datetime.datetime.now()
	yield check, []
	yield check, {}
	yield check, [1, 2, 3]
	yield check, {None: 42, 1: 2, "foo": "bar", "baz": datetime.datetime.now(), "gurk": ["hurz"]}
