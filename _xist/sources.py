#! /usr/bin/env python
# -*- coding: Latin-1 -*-

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
<doc:par>This module contains variousclasses derived from
<class>xml.sax.xmlreader.InputSource</class>.</doc:par>
"""

import cStringIO as StringIO

from xml import sax
from xml.sax import saxlib

from mx import Tidy

from ll import url

class InputSource(sax.xmlreader.InputSource):
	def __init__(self, base):
		sax.xmlreader.InputSource.__init__(self)
		self.base = url.URL(base)

class StringInputSource(InputSource):
	def __init__(self, text, systemId="STRING", base=None, defaultEncoding="utf-8", tidy=False):
		InputSource.__init__(self, base)
		self.setSystemId(systemId)
		if isinstance(text, unicode):
			defaultEncoding = "utf-8"
			text = text.encode(defaultEncoding)
		if tidy:
			(nerrors, nwarnings, outputdata, errordata) = Tidy.tidy(text, numeric_entities=1, output_xhtml=1, output_xml=1, quiet=1, tidy_mark=0, wrap=0)
			if nerrors>0:
				raise saxlib.SAXException("can't tidy %r (%d errors, %d warnings):\n%s" % (systemId, nerrors, nwarnings, errordata))
			text = outputdata
		self.setByteStream(StringIO.StringIO(text))
		self.setEncoding(defaultEncoding)

class URLInputSource(InputSource):
	def __init__(self, id, base=None, defaultEncoding="utf-8", tidy=False, headers=None, data=None):
		if isinstance(id, (str, unicode)):
			id = url.URL(id)
		if base is None:
			base = id.url
		InputSource.__init__(self, base)
		self.setSystemId(id.url)
		resource = id.openread(headers=headers, data=data)
		if tidy:
			(nerrors, nwarnings, outputdata, error) = Tidy.tidy(resource.read(), numeric_entities=1, output_xhtml=1, output_xml=1, quiet=1, tidy_mark=0, wrap=0)
			if nerrors>0:
				raise SAXParseException("can't tidy %r: %r" % (url, errordata))
			resource = StringIO.StringIO(outputdata)
		self.setByteStream(resource)
		self.setEncoding(defaultEncoding)

	def setTimeout(self, secs):
		if timeoutsocket is not None:
			timeoutsocket.setDefaultSocketTimeout(sec)

	def getTimeout(self):
		if timeoutsocket is not None:
			timeoutsocket.getDefaultSocketTimeout()

