#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


from ll.xist import xsc


def test_locationeq():
	l1 = xsc.Location(sysid="gurk", pubid="http://gurk.com", line=42, col=666)
	l2 = xsc.Location(sysid="gurk", pubid="http://gurk.com", line=42, col=666)
	l3 = xsc.Location(sysid="hurz", pubid="http://gurk.com", line=42, col=666)
	l4 = xsc.Location(sysid="gurk", pubid="http://hurz.com", line=42, col=666)
	l5 = xsc.Location(sysid="gurk", pubid="http://gurk.com", line=43, col=666)
	l6 = xsc.Location(sysid="gurk", pubid="http://gurk.com", line=43, col=667)
	l7 = xsc.Location(sysid="gurk", pubid="http://gurk.com")
	assert l1 == l2
	assert l1 != l3
	assert l1 != l4
	assert l1 != l5
	assert l1 != l6
	assert l1 != l7


def test_locationoffset():
	l1 = xsc.Location(sysid="gurk", pubid="http://gurk.com", line=42, col=666)
	assert l1 == l1.offset(0)
	l2 = l1.offset(1)
	assert l1.getSystemId() == l2.getSystemId()
	assert l1.getPublicId() == l2.getPublicId()
	assert l1.getLineNumber()+1 == l2.getLineNumber()
