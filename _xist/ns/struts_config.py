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
<doc:par>Namespace module for struts-config: <code>http://jakarta.apache.org/struts/dtds/struts-config_1_0.dtd</code>.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc

class DocType(xsc.DocType):
	def __init__(self):
		xsc.DocType.__init__(
			self,
			'struts-config PUBLIC '
			'"-//Apache Software Foundation//DTD Struts Configuration 1.0//EN" '
			'"http://jakarta.apache.org/struts/dtds/struts-config_1_0.dtd"'
		)

class data_sources(xsc.Element):
	empty = 0
	name = "data-sources"

class data_source(xsc.Element):
	empty = 0
	name = "data-source"

class set_property(xsc.Element):
	empty = 0
	attrHandlers = {"property": xsc.TextAttr, "value": xsc.TextAttr}
	name = "set-property"

class struts_config(xsc.Element):
	empty = 0
	name = "struts-config"

class form_beans(xsc.Element):
	empty = 0
	name = "form-beans"

class form_bean(xsc.Element):
	empty = 1
	attrHandlers = {"type": xsc.TextAttr, "name": xsc.TextAttr}
	name = "form-bean"

class global_forwards(xsc.Element):
	empty = 0
	name = "global-forwards"

class forward(xsc.Element):
	empty = 1
	attrHandlers = {"name": xsc.TextAttr, "path": xsc.TextAttr, "redirect": xsc.TextAttr}

class action_mappings(xsc.Element):
	empty = 0
	name = "action-mappings"

class action(xsc.Element):
	empty = 0
	attrHandlers = {
		"path": xsc.TextAttr, "type": xsc.TextAttr, "input": xsc.TextAttr,
		"name": xsc.TextAttr, "scope": xsc.TextAttr
	}

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

namespace = xsc.Namespace("struts-config", "http://jakarta.apache.org/struts/dtds/struts-config_1_0.dtd", vars())

