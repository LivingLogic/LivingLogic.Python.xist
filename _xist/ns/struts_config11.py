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
<doc:par>Namespace module for <a href="http://jakarta.apache.org/struts/">Struts</a>
configuration files: <lit><a href="http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd">http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd</a></lit>.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc
import struts_config as struts_config10

class DocType(xsc.DocType):
	def __init__(self):
		xsc.DocType.__init__(
			self,
			'struts-config PUBLIC '
			'"-//Apache Software Foundation//DTD Struts Configuration 1.1//EN" '
			'"http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd"'
		)

class data_sources(struts_config10.data_sources):
	name = "data-sources"

class data_source(struts_config10.data_source):
	attrHandlers = {"className": xsc.TextAttr, "key": xsc.TextAttr, "type": xsc.TextAttr}
	name = "data-source"

class set_property(struts_config10.set_property):
	name = "set-property"

class struts_config(struts_config10.struts_config):
	name = "struts-config"

class global_exceptions(xsc.Element):
	empty = 0
	name = "global-exceptions"

class exception(xsc.Element):
	empty = 1
	attrHandlers = {
		"className": xsc.TextAttr, "handler": xsc.TextAttr, "key": xsc.TextAttr,
		"path": xsc.TextAttr, "scope": xsc.TextAttr, "type": xsc.TextAttr
	}

class form_beans(struts_config10.form_beans):
	name = "form-beans"

class form_bean(struts_config10.form_bean):
	empty = 0
	attrHandlers = {
		"className": xsc.TextAttr, "dynamic": xsc.TextAttr, "name": xsc.TextAttr,
		"type": xsc.TextAttr
	}
	name = "form-bean"

class form_property(xsc.Element):
	empty = 1
	attrHandlers = {
		"className": xsc.TextAttr, "initial": xsc.TextAttr, "name": xsc.TextAttr,
		"type": xsc.TextAttr
	}
	name = "form-property"

class global_forwards(struts_config10.global_forwards):
	name = "global-forwards"

class forward(struts_config10.forward):
	attrHandlers = {
		"className": xsc.TextAttr, "contextRelative": xsc.TextAttr, "name": xsc.TextAttr,
		"path": xsc.TextAttr, "redirect": xsc.TextAttr
	}

class action_mappings(struts_config10.action_mappings):
	name = "action-mappings"

class action(xsc.Element):
	"""
	<doc:par>This element represents a struts action mapping using the
	struts workflow extension mapping class (<class>ApplicationMapping</class>)
	as its default instead of the action mapping class included in
	the official struts 1.1 package. If you want to use the default
	struts action mapping class, you have to specify its fully qualified
	class name in the <lit>className</lit> attribute.</doc:par>
	"""
	empty = 0
	attrHandlers = {
		"attribute": xsc.TextAttr, "className": xsc.TextAttr, "forward": xsc.TextAttr,
		"include": xsc.TextAttr, "input": xsc.TextAttr, "name": xsc.TextAttr,
		"parameter": xsc.TextAttr, "path": xsc.TextAttr, "prefix": xsc.TextAttr,
		"scope": xsc.TextAttr, "suffix": xsc.TextAttr, "type": xsc.TextAttr,
		"unknown": xsc.TextAttr, "validate": xsc.TextAttr
	}

	def convert(self, converter):
		e = action(
			self.content.convert(converter),
			self.attrs.convert(converter)
		)
		e.setDefaultAttr("className", "com.livinglogic.struts.workflow.ApplicationMapping")
		return e

class controller(xsc.Element):
	empty = 1
	attrHandlers = {
		"bufferSize": xsc.TextAttr, "className": xsc.TextAttr,
		"contentType": xsc.TextAttr, "debug": xsc.TextAttr, "locale": xsc.TextAttr,
		"maxFileSize": xsc.TextAttr, "multipartClass": xsc.TextAttr,
		"nocache": xsc.TextAttr, "processorClass": xsc.TextAttr, "tempDir": xsc.TextAttr
	}

class plug_in(xsc.Element):
	empty = 1
	attrHandlers = {"className": xsc.TextAttr}
	name = "plug-in"

class message_resources(xsc.Element):
	empty = 1
	attrHandlers = {
		"className": xsc.TextAttr, "factory": xsc.TextAttr,
		"key": xsc.TextAttr, "null": xsc.TextAttr, "parameter": xsc.TextAttr
	}
	name = "message-resources"

# this is no "official" struts-config element, but nontheless useful for generating
# the final XML output
class user_struts_config(xsc.Element):
	empty = 0
	name = "user-struts-config"

	def convert(self, converter):
		e = xsc.Frag(
			xsc.XML10(),
			u"\n",
			DocType(),
			u"\n",
			struts_config(self.content)
		)
		return e.convert(converter)

namespace = xsc.Namespace("struts-config_1_1", "http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd", vars())

