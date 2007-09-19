#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


import py.test

from ll.xist import xsc, parsers
from ll.xist.ns import specials


def test_url():
	node = parsers.parsestring("<?url root:images/gurk.gif?>")
	assert node.bytes(base="root:about/us.html") == "../images/gurk.gif"
