#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
<doc:par>This module contains several functions and classes,
that are used internally by &xist;.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import xsc, url as url_

def findAttr(content, name):
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
	for i in xrange(len(frag)):
		v = frag[i]
		if isinstance(v, (xsc.Text, xsc.CharRef)):
			newfrag.append(v)
		else:
			break
	else:
		i += 1
	if len(newfrag): # do the replacement only if we have something static
		u = url_.URL(unicode(newfrag))
		u = callback(u)
		newfrag = xsc.Frag(u.asString())
	while i < len(frag):
		newfrag.append(frag[i])
		i += 1
	return newfrag
