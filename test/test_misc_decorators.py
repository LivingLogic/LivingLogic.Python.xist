#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2005-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import py.test

from ll import misc


def test_notimplemented():
	class Bad(object):
		@misc.notimplemented
		def bad(self):
			pass

	py.test.raises(NotImplementedError, Bad().bad)
