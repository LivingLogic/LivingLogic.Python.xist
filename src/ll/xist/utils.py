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


def replaceInitialURL(frag, callback):
	"""
	This function replaces to the text nodes of a fragment,
	which will be interpreted as an URL with another URL. All
	text nodes up to the first non text node are converted to a
	URL. This URL will be passed to the callback and the result
	will be put in into the frag instead of the old text nodes.
	"""
	newfrag = xsc.Frag()
	if len(frag):
		for i in xrange(len(frag)):
			v = frag[i]
			if isinstance(v, xsc.Text):
				newfrag.append(v)
			else:
				break
		else:
			i += 1
		if len(newfrag): # do the replacement only if we have something static
			u = url_.URL(unicode(newfrag).lstrip())
			u = callback(u)
			newfrag = xsc.Frag(u.url)
		while i < len(frag):
			newfrag.append(frag[i])
			i += 1
	return newfrag
