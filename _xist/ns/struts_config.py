#!/usr/bin/env python
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
import xml


class DocType(xsc.DocType):
	def __init__(self):
		xsc.DocType.__init__(
			self,
			'struts-config PUBLIC '
			'"-//Apache Software Foundation//DTD Struts Configuration 1.1//EN" '
			'"http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd"'
		)


class ElementWithID(xsc.Element):
	class Attrs(xsc.Element.Attrs):
		class id(xsc.IDAttr): pass


class struts_config(ElementWithID):
	xmlname = "struts-config"
	empty = False


class data_sources(ElementWithID):
	xmlname = "data-sources"
	empty = False


class data_source(ElementWithID):
	xmlname = "data-source"
	empty = False
	class Attrs(xsc.Element.Attrs):
		class className(xsc.TextAttr): pass
		class key(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass


class form_beans(ElementWithID):
	xmlname = "form-beans"
	empty = False
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class form_bean(ElementWithID):
	xmlname = "form-bean"
	empty = False
	class Attrs(xsc.Element.Attrs):
		class className(xsc.TextAttr): pass
		class dynamic(xsc.TextAttr): values = ("true", "false", "yes", "no")
		class name(xsc.TextAttr): required = True
		class type(xsc.TextAttr): required = True


class form_property(xsc.Element):
	xmlname = "form-property"
	empty = False
	class Attrs(xsc.Element.Attrs):
		class className(xsc.TextAttr): pass
		class initial(xsc.TextAttr): pass
		class name(xsc.TextAttr): required = True
		class size(xsc.TextAttr): pass
		class type(xsc.TextAttr): required = True


class global_exceptions(ElementWithID):
	xmlname = "global-exceptions"
	empty = False


class exception(ElementWithID):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class bundle(xsc.TextAttr): pass
		class className(xsc.TextAttr): pass
		class handler(xsc.TextAttr): pass
		class key(xsc.TextAttr): required = True
		class path(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class type(xsc.TextAttr): required = True


class global_forwards(ElementWithID):
	xmlname = "global-forwards"
	empty = False
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class forward(ElementWithID):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class className(xsc.TextAttr): pass
		class contextRelative(xsc.TextAttr): values = ("true", "false", "yes", "no")
		class name(xsc.TextAttr): required = True
		class path(xsc.TextAttr): required = True
		class redirect(xsc.TextAttr): values = ("true", "false", "yes", "no")


class action_mappings(ElementWithID):
	xmlname = "action-mappings"
	empty = False
	class Attrs(xsc.Element.Attrs):
		class type(xsc.TextAttr): pass


class action(ElementWithID):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class attribute(xsc.TextAttr): pass
		class className(xsc.TextAttr): pass
		class forward(xsc.TextAttr): pass
		class include(xsc.TextAttr): pass
		class input(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class parameter(xsc.TextAttr): pass
		class path(xsc.TextAttr): required = True
		class prefix(xsc.TextAttr): pass
		class roles(xsc.TextAttr): pass
		class scope(xsc.TextAttr): values = ("request", "session")
		class suffix(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
		class unknown(xsc.TextAttr): values = ("true", "false", "yes", "no")
		class validate(xsc.TextAttr): values = ("true", "false", "yes", "no")


class controller(ElementWithID):
	empty = False
	class Attrs(xsc.Element.Attrs):
		class bufferSize(xsc.TextAttr): pass
		class className(xsc.TextAttr): pass
		class contentType(xsc.TextAttr): pass
		class debug(xsc.TextAttr): pass
		class forwardPattern(xsc.TextAttr): pass
		class inputForward(xsc.TextAttr): values = ("true", "false", "yes", "no")
		class locale(xsc.TextAttr): values = ("true", "false", "yes", "no")
		class maxFileSize(xsc.TextAttr): pass
		class memFileSize(xsc.TextAttr): pass
		class multipartClass(xsc.TextAttr): pass
		class nocache(xsc.TextAttr): values = ("true", "false", "yes", "no")
		class pagePattern(xsc.TextAttr): pass
		class processorClass(xsc.TextAttr): pass
		class tempDir(xsc.TextAttr): pass


class message_resources(ElementWithID):
	xmlname = "message-resources"
	empty = False
	class Attrs(xsc.Element.Attrs):
		class className(xsc.TextAttr): pass
		class factory(xsc.TextAttr): pass
		class key(xsc.TextAttr): pass
		class null(xsc.TextAttr): values = ("true", "false", "yes", "no")
		class parameter(xsc.TextAttr): required = True


class plug_in(ElementWithID):
	xmlname = "plug-in"
	empty = False
	class Attrs(xsc.Element.Attrs):
		class className(xsc.TextAttr): required = True


class description(ElementWithID):
	empty = False


class display_name(ElementWithID):
	xmlname = "display-name"
	empty = False


class icon(ElementWithID):
	empty = False


class large_icon(ElementWithID):
	xmlname = "large-icon"
	empty = False


class set_property(ElementWithID):
	xmlname = "set-property"
	empty = True
	class Attrs(xsc.Element.Attrs):
		class property(xsc.TextAttr): required = True
		class value(xsc.TextAttr): required = True


class small_icon(ElementWithID):
	xmlname = "small-icon"
	empty = False


# this is no "official" struts-config element, but nonetheless useful for generating
# the final XML output
class user_struts_config(xsc.Element):
	empty = False
	name = "user-struts-config"

	def convert(self, converter):
		e = xsc.Frag(
			xml.XML10(),
			u"\n",
			DocType(),
			u"\n",
			struts_config(self.content)
		)
		return e.convert(converter)


class xmlns(xsc.Namespace):
	xmlname = "struts_config"
	xmlurl = "http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd"
xmlns.makemod(vars())