#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
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
<doc:par>Contains the global attributes for the &xml; namespace.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from __future__ import nested_scopes
from ll.xist import xsc, utils

class XML(xsc.ProcInst):
	"""
	&xml; header
	"""
	xmlname = "xml"

	needsxmlns = 0

	def publish(self, publisher):
		content = self.content
		encodingfound = utils.findAttr(content, u"encoding")
		versionfound = utils.findAttr(content, u"version")
		standalonefound = utils.findAttr(content, u"standalone")
		if publisher.encoding != encodingfound: # if self has the wrong encoding specification (or none), we construct a new XML ProcInst and publish that (this doesn't lead to infinite recursion, because the next call will skip it)
			node = XML(u"version='" + versionfound + u"' encoding='" + publisher.encoding + u"'")
			if standalonefound is not None:
				node += u" standalone='" + standalonefound + u"'"
			node.publish(publisher)
			return
		xsc.ProcInst.publish(self, publisher)

class XML10(XML):
	"""
	&xml; header version 1.0, i.e. <markup>&lt;?xml version="1.0"?&gt;</markup>
	"""
	xmlname = "xml10"
	register = False # don't register this ProcInst, because it will never be parsed from a file, this is just a convenience class

	def __init__(self):
		super(XML10, self).__init__('version="1.0"')

class XMLStyleSheet(xsc.ProcInst):
	"""
	XML stylesheet declaration
	"""
	xmlname = u"xml-stylesheet"

	needsxmlns = 0

class xmlns(xsc.Namespace):
	xmlname = "xml"
	xmlurl = "http://www.w3.org/XML/1998/namespace"

	class Attrs(xsc.Namespace.Attrs):
		class space(xsc.NamespaceAttrMixIn, xsc.TextAttr):
			needsxmlns = 1
			xmlprefix = u"xml"
			values = ("default", "preserve")
		class lang(xsc.NamespaceAttrMixIn, xsc.TextAttr):
			needsxmlns = 1
			xmlprefix = u"xml"
		class base(xsc.NamespaceAttrMixIn, xsc.URLAttr):
			needsxmlns = 1
			xmlprefix = u"xml"
xmlns.makemod(vars())

