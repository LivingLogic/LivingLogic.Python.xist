#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2005/2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005/2006 by Walter Dörwald
##
## All Rights Reserved
##
## See __init__.py for the license


import sys, re

from ll import misc


# The following includes \x00 in addition to those characters defined in
# http://www.w3.org/TR/2004/REC-xml11-20040204/#NT-RestrictedChar
restrictedchars = re.compile(u"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]")


escape_input = u"".join([unichr(i) for i in xrange(1000)] + [unichr(i) for i in xrange(sys.maxunicode-10, sys.maxunicode+1)])


def test_xmlescape():
	escape_output = []
	for c in escape_input:
		if c==u"&":
			escape_output.append(u"&amp;")
		elif c==u"<":
			escape_output.append(u"&lt;")
		elif c==u">":
			escape_output.append(u"&gt;")
		elif c==u'"':
			escape_output.append(u"&quot;")
		elif c==u"'":
			escape_output.append(u"&apos;")
		elif restrictedchars.match(c) is not None:
			escape_output.append(u"&#%d;" % ord(c))
		else:
			escape_output.append(c)
	escape_output = "".join(escape_output)
	assert misc.xmlescape(escape_input) == escape_output
