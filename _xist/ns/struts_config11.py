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
configuration files: <link href="http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd">http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd</link>.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc
import struts_config as struts_config10
import xml

class DocType(xsc.DocType):
	def __init__(self):
		xsc.DocType.__init__(
			self,
			'struts-config PUBLIC '
			'"-//Apache Software Foundation//DTD Struts Configuration 1.1//EN" '
			'"http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd"'
		)

class data_source(struts_config10.data_source):
	class Attrs(struts_config10.data_source.Attrs):
		class className(xsc.TextAttr): pass
	xmlname = "data-source"

class global_exceptions(xsc.Element):
	empty = False
	xmlname = "global-exceptions"

class exception(xsc.Element):
	empty = True
	class Attrs(xsc.Element.Attrs):
		class className(xsc.TextAttr): pass
		class handler(xsc.TextAttr): pass
		class key(xsc.TextAttr): pass
		class path(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass

class form_bean(struts_config10.form_bean):
	empty = False
	class Attrs(struts_config10.form_bean.Attrs):
		class className(xsc.TextAttr): pass
		class dynamic(xsc.TextAttr): pass
	xmlname = "form-bean"

class form_property(xsc.Element):
	empty = True
	class Attrs(struts_config10.form_bean.Attrs):
		class className(xsc.TextAttr): pass
		class initial(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
	xmlname = "form-property"

class forward(struts_config10.forward):
	class Attrs(struts_config10.forward.Attrs):
		class className(xsc.TextAttr): pass
		class contextRelative(xsc.TextAttr): pass

class action_mappings(struts_config10.action_mappings):
	xmlname = "action-mappings"
	class Attrs(struts_config10.action_mappings.Attrs):
		class id(xsc.IDAttr): pass
		class type(xsc.TextAttr): pass

class action(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class attribute(xsc.TextAttr): pass
		class className(xsc.TextAttr): pass
		class forward(xsc.TextAttr): pass
		class include(xsc.TextAttr): pass
		class input(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class parameter(xsc.TextAttr): pass
		class path(xsc.TextAttr): pass
		class prefix(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class suffix(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
		class unknown(xsc.TextAttr): pass
		class validate(xsc.TextAttr): pass

class controller(xsc.Element):
	empty = True
	class Attrs(xsc.Element.Attrs):
		class bufferSize(xsc.TextAttr): pass
		class className(xsc.TextAttr): pass
		class contentType(xsc.TextAttr): pass
		class debug(xsc.TextAttr): pass
		class locale(xsc.TextAttr): pass
		class maxFileSize(xsc.TextAttr): pass
		class multipartClass(xsc.TextAttr): pass
		class nocache(xsc.TextAttr): pass
		class processorClass(xsc.TextAttr): pass
		class tempDir(xsc.TextAttr): pass

class plug_in(xsc.Element):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class className(xsc.TextAttr): pass
	xmlname = "plug-in"

class message_resources(xsc.Element):
	empty = True
	class Attrs(xsc.Element.Attrs):
		class className(xsc.TextAttr): pass
		class factory(xsc.TextAttr): pass
		class key(xsc.TextAttr): pass
		class null(xsc.TextAttr): pass
		class parameter(xsc.TextAttr): pass
	xmlname = "message-resources"

# this is no "official" struts-config element, but nontheless useful for generating
# the final XML output
class user_struts_config(xsc.Element):
	empty = False
	xmlname = "user-struts-config"

	def convert(self, converter):
		e = xsc.Frag(
			xml.XML10(),
			u"\n",
			DocType(),
			u"\n",
			struts_config11.struts_config(self.content)
		)
		return e.convert(converter)

class xmlns(struts_config10):
	xmlname = "struts_config11"
	xmlurl = "http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd"
xmlns.makemod(vars())

