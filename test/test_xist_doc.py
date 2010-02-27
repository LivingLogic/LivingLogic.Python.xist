#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import warnings

from ll.xist import xsc
from ll.xist.ns import doc


__docformat__ = "xist"


def test_explain():
	"""
	This is <func>test_explain</func>.
	"""
	assert unicode(doc.explain(test_explain, format="xist").walknode(doc.func)[0]) == u"test_explain"
