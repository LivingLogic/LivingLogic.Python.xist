#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>Namespace module for <link href="http://jakarta.apache.org/struts/">Struts</link>
configuration files: <link href="http://jakarta.apache.org/struts/dtds/struts-config_1_0.dtd">http://jakarta.apache.org/struts/dtds/struts-config_1_0.dtd</link>.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc
import xml

class DocType(xsc.DocType):
	def __init__(self):
		xsc.DocType.__init__(
			self,
			'struts-config PUBLIC '
			'"-//Apache Software Foundation//DTD Struts Configuration 1.0//EN" '
			'"http://jakarta.apache.org/struts/dtds/struts-config_1_0.dtd"'
		)

class data_sources(xsc.Element):
	empty = False
	xmlname = "data-sources"

class data_source(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class key(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
	xmlname = "data-source"

class set_property(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class property(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass
	xmlname = "set-property"

class struts_config(xsc.Element):
	empty = False
	xmlname = "struts-config"

class form_beans(xsc.Element):
	empty = False
	xmlname = "form-beans"

class form_bean(xsc.Element):
	empty = True
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
	xmlname = "form-bean"

class global_forwards(xsc.Element):
	empty = False
	xmlname = "global-forwards"

class forward(xsc.Element):
	empty = True
	class Attrs(xsc.Element.Attrs):
		class name(xsc.TextAttr): pass
		class path(xsc.TextAttr): pass
		class redirect(xsc.TextAttr): pass

class action_mappings(xsc.Element):
	empty = False
	xmlname = "action-mappings"

class action(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class path(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
		class input(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass

# this is no "official" struts-config element, but nonetheless useful
# for generating the final XML output
class user_struts_config(xsc.Element):
	empty = False
	xmlname = "user-struts-config"

	def convert(self, converter):
		e = xsc.Frag(
			xml.XML10(),
			u"\n",
			DocType(),
			u"\n",
			struts_config.struts_config(self.content)
		)
		return e.convert(converter)

class xmlns(xsc.Namespace):
	xmlname = "struts_config"
	xmlurl = "http://jakarta.apache.org/struts/dtds/struts-config_1_0.dtd"
xmlns.makemod(vars())

