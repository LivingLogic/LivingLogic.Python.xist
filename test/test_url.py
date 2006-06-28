#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


import py.test

from ll.xist import xsc, parsers
from ll.xist.ns import specials


def test_url():
	node = parsers.parseString("<?url root:images/gurk.gif?>")
	assert node.asBytes(base="root:about/us.html") == "../images/gurk.gif"
