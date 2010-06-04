#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll.xist import xsc
from ll.xist.ns import html


def test_mapped():
	def maplang(node, converter):
		if isinstance(node, xsc.Text):
			node = node.replace(u"lang", converter.lang)
		return node

	node = xsc.Frag(
		u"lang",
		html.div(
			u"lang",
			class_=u"lang",
		)
	)
	node2 = node.mapped(maplang, lang="en")
	assert node == xsc.Frag(
		u"lang",
		html.div(
			u"lang",
			class_=u"lang",
		)
	)
	assert node2 == xsc.Frag(
		u"en",
		html.div(
			u"en",
			class_=u"lang", # No replacement in attributes
		)
	)
