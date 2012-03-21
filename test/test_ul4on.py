#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2011-2012 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2011-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import io, os, datetime, math

from ll import ul4on, ul4c, color

import py.test


def flatten(data):
	# This is use to be able to compare templates (by comparing their output)
	if isinstance(data, ul4c.Template):
		return data.renders()
	elif isinstance(data, list):
		return [flatten(item) for item in data]
	elif isinstance(data, dict):
		return {key: flatten(value) for (key, value) in data.items()}
	else:
		return data


def test_loads_dumps():
	def check(data):
		data2 = ul4on.loads(ul4on.dumps(data))
		assert flatten(data2) == flatten(data)

	t = ul4c.Template("<?for i in range(10)?>(<?print i?>)<?end for?>")
	yield check, None
	yield check, False
	yield check, True
	yield check, 42
	yield check, math.pi
	yield check, "gurk"
	yield check, color.Color(0x66, 0x99, 0xcc, 0xff)
	yield check, datetime.datetime.now()
	yield check, []
	yield check, {}
	yield check, t
	yield check, [1, 2, 3]
	yield check, {None: 42, 1: 2, "foo": "bar", "baz": datetime.datetime.now(), "gurk": ["hurz"], "template": t}


def test_encoder_list():
	enc = ul4on.Encoder(io.StringIO())

	with enc.list():
		for i in range(10):
			with enc.list():
				enc.write(i)

	assert ul4on.loads(enc.getvalue()) == [[i] for i in range(10)]


def test_encoder_dict():
	enc = ul4on.Encoder(io.StringIO())

	with enc.dict():
		enc.write("eins")
		enc.write(1)
		enc.write("zwei")
		enc.write(2)
		enc.write("drei")
		enc.write(3)

	assert ul4on.loads(enc.getvalue()) == dict(eins=1, zwei=2, drei=3)