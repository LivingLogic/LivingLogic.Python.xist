#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


import warnings

from ll.xist import xsc
from ll.xist.ns import doc


def test_explain():
	"""
	This is <function>test_explain</function>.
	"""
	assert unicode(doc.explain(test_explain).walknode(doc.function)[0]) == u"test_explain"