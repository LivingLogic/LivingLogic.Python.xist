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
<par>Namespace module for <link href="http://jakarta.apache.org/struts/">Struts</link>
configuration files: <link href="http://jakarta.apache.org/struts/dtds/struts-config_1_0.dtd">http://jakarta.apache.org/struts/dtds/struts-config_1_0.dtd</link>.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc
from xml import xml

class struts_config(xsc.Namespace):
	xmlurl = "http://jakarta.apache.org/struts/dtds/struts-config_1_0.dtd"

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

