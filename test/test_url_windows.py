#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2005-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll import url


def test_escape(recwarn):
	assert url.URL("%u0042").file == u"\x42"

	url.URL("%u00")
	recwarn.pop(UserWarning)

	url.URL("%u00xx")
	recwarn.pop(UserWarning)

	assert url.URL("%u00").file == u"%u00"
	assert url.URL("%u00xx").file == u"%u00xx"
