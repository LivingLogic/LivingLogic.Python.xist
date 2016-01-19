# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
Contains the global attributes for the XML namespace (like ``xml:lang``),
and classes for the XML declaration.
"""


from ll import xml_codec
from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = xsc.xml_xmlns


class Attrs(xsc.Attrs):
	xmlns = xmlns

	class space(xsc.TextAttr):
		xmlns = xmlns
		values = ("default", "preserve")

	class lang(xsc.TextAttr):
		xmlns = xmlns

	class base(xsc.URLAttr):
		xmlns = xmlns


class XML(xsc.ProcInst):
	"""
	XML declaration. The encoding will be automatically set when publishing.
	"""
	xmlname = "xml"

	def __init__(self, version="1.0", encoding="utf-8", standalone=None):
		v = []
		v.append('version="{}"'.format(version)) # According to http://www.w3.org/TR/2000/REC-xml-20001006#NT-XMLDecl version is required
		if encoding is not None:
			v.append('encoding="{}"'.format(encoding))
		if standalone is not None:
			v.append('standalone="{}"'.format("yes" if standalone else "no"))
		xsc.ProcInst.__init__(self, " ".join(v))

	def publish(self, publisher):
		xml = "<?xml {}?>".format(self.content)
		if publisher.encoding is not None:
			xml = xml_codec._fixencoding(xml, str(publisher.encoding))
		yield publisher.encode(xml)


class XMLStyleSheet(xsc.ProcInst):
	"""
	XML stylesheet declaration.
	"""
	xmlname = "xml-stylesheet"


class declaration(xsc.Element):
	"""
	The XML declaration as an element. This makes it possible to generate a
	declaration from within an XML file.
	"""
	xmlns = xmlns
	model = sims.Empty()

	def convert(self, converter):
		node = XML()
		return node.convert(converter)
