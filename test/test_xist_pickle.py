#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license

import pickle

from ll.xist import xsc
from ll.xist.ns import xml, html, chars, abbr, php


def test_pickle():
	e = xsc.Frag(
		xml.XML(),
		html.DocTypeXHTML10transitional(),
		xsc.Comment("foo"),
		html.html(xml.Attrs(lang="de"), lang="de"),
		php.expression("$foo"),
		chars.nbsp(),
		abbr.xml(),
	)
	e.append(e[3])
	e2 = pickle.loads(pickle.dumps(e, 2))
	assert e == e2
	assert e2[3] is e2[-1]
