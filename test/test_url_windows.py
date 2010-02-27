#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2005-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import warnings

import py.test

from ll import url


def test_escape():
	assert url.URL("%u0042").file == u"\x42"

	warnings.filterwarnings("error", category=UserWarning)
	py.test.raises(UserWarning, url.URL, "%u00")
	py.test.raises(UserWarning, url.URL, "%u00xx")

	warnings.filterwarnings("ignore", category=UserWarning)
	assert url.URL("%u00").file == u"%u00"
	assert url.URL("%u00xx").file == u"%u00xx"
