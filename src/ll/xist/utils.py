# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<p>This module contains several functions and classes,
that are used internally by &xist;.</p>
"""


from ll import url as url_

import xsc


__docformat__ = "xist"


def findattr(content, name):
	startpos = content.find(name)
	if startpos != -1:
		startpos = startpos+len(name)
		while content[startpos].isspace():
			startpos += 1
		startpos += 1 # skip '='
		while content[startpos].isspace():
			startpos += 1
		char = content[startpos]
		startpos += 1
		endpos = content.find(char, startpos)
		if endpos != -1:
			return content[startpos:endpos]
	return None
