# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<par>Contains the global attributes for the &xml; namespace (like <lit>xml:lang</lit>),
and classes for the &xml; declaration.</par>
"""


from ll.xist import xsc, utils, sims


__docformat__ = "xist"


xmlns = xsc.xml_xmlns


class Attrs(xsc.Attrs):
	class space(xsc.TextAttr):
		xmlns = xmlns
		values = (u"default", u"preserve")

	class lang(xsc.TextAttr):
		xmlns = xmlns

	class base(xsc.URLAttr):
		xmlns = xmlns


class XML(xsc.ProcInst):
	"""
	&xml; declaration. The encoding will be automatically set when publishing
	(by the &xml; codec).
	"""
	xmlname = "xml"

	def __init__(self, version="1.0", encoding="utf-8"):
		xsc.ProcInst.__init__(self, u'version="%s" encoding="%s"' % (version, encoding))


class XMLStyleSheet(xsc.ProcInst):
	"""
	XML stylesheet declaration.
	"""
	xmlname = "xml-stylesheet"


class declaration(xsc.Element):
	"""
	<par>The &xml; declaration as an element. This makes it possible to generate
	a declaration from within an &xml; file.
	"""
	xmlns = xmlns
	model = sims.Empty()

	def convert(self, converter):
		node = XML()
		return node.convert(converter)
