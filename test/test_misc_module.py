#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2009 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll import misc


def test_module():
	m = misc.module("a = 42")
	assert m.a == 42
	assert m.__name__ == "unnamed"
	assert m.__file__ == "unnamed.py"

	m = misc.module("a = 42", "/Users/walter/test.py")
	assert m.a == 42
	assert m.__name__ == "test"
	assert m.__file__ == "/Users/walter/test.py"

	m = misc.module("a = 42", "/Users/walter/test.py", "pest")
	assert m.a == 42
	assert m.__name__ == "pest"
	assert m.__file__ == "/Users/walter/test.py"
