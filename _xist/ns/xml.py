#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>Contains the global attributes for the &xml; namespace.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc, utils


class XML(xsc.ProcInst):
	"""
	&xml; header
	"""
	xmlname = "xml"

	def publish(self, publisher):
		content = self.content
		encodingfound = utils.findAttr(content, u"encoding")
		versionfound = utils.findAttr(content, u"version")
		standalonefound = utils.findAttr(content, u"standalone")
		if publisher.encoding != encodingfound: # if self has the wrong encoding specification (or none), we construct a new XML ProcInst and publish that (this doesn't lead to infinite recursion, because the next call will skip it)
			node = XML(u"version='%s' encoding='%s'" % (versionfound, publisher.encoding))
			if standalonefound is not None:
				node += u" standalone='%s'" % standalonefound
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
	xmlname = "xml-stylesheet"

	needsxmlns = 0


class header(xsc.Element):
	"""
	<par>The &xml; header processing instruction as an element. This makes it
	possible to generate a header from within an &xml; file.
	"""
	empty = True

	def convert(self, converter):
		return XML10()


class xmlns(xsc.Namespace):
	xmlname = "xml"
	xmlurl = "http://www.w3.org/XML/1998/namespace"

	class Attrs(xsc.Namespace.Attrs):
		class space(xsc.TextAttr):
			needsxmlns = 1
			xmlprefix = "xml"
			values = ("default", "preserve")
		class lang(xsc.TextAttr):
			needsxmlns = 1
			xmlprefix = "xml"
		class base(xsc.URLAttr):
			needsxmlns = 1
			xmlprefix = "xml"
xmlns.makemod(vars())
