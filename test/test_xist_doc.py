#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


from ll.xist import xsc
from ll.xist.ns import doc


__docformat__ = "xist"


def test_explain():
	"""
	This is <func>test_explain</func>.
	"""
	assert str(doc.explain(test_explain, format="xist").walknodes(doc.func)[0]) == "test_explain"
