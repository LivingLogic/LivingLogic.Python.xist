#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>This module contains various classes derived from
<class>xml.sax.xmlreader.InputSource</class>.</par>
"""

import cStringIO as StringIO

from xml import sax
from xml.sax import saxlib

from mx import Tidy

from ll import url

class InputSource(sax.xmlreader.InputSource):
	"""
	A class that defines an input stream from which a &sax; parser
	reads its input.
	"""
	def __init__(self, base):
		sax.xmlreader.InputSource.__init__(self)
		self.base = url.URL(base)

class StringInputSource(InputSource):
	"""
	An <class>InputSource</class> where the data is read from
	a string.
	"""
	def __init__(self, text, systemId="STRING", base=None, encoding="utf-8", tidy=False):
		"""
		<par>Create a new <class>StringInputSource</class> instance. Arguments are:</par>
		<ulist>
		<item><arg>text</arg>: The text to be parsed;</item>
		<item><arg>systemId</arg>: The system id to be used;</item>
		<item><arg>base</arg>: The base &url; (it will be prepended
		to all &url;s created during the parsing of this input source);</item>
		<item><arg>encoding</arg>: The encoding to be used when
		no &xml; header can the found in the input source (this is not
		supported by all parsers);</item>
		<item><arg>tidy</arg>: allows you to specify, whether
		Marc-Andr&eacute; Lemburg's <app moreinfo="http://www.lemburg.com/files/python/">mxTidy</app> should
		be used for cleaning up broken &html; before parsing the result.</item>
		</ulist>
		"""
		InputSource.__init__(self, base)
		self.setSystemId(systemId)
		if isinstance(text, unicode):
			encoding = "utf-8"
			text = text.encode(encoding)
		if tidy:
			(nerrors, nwarnings, outputdata, errordata) = Tidy.tidy(text, numeric_entities=1, output_xhtml=1, output_xml=1, quiet=1, tidy_mark=0, wrap=0)
			if nerrors>0:
				raise saxlib.SAXException("can't tidy %r (%d errors, %d warnings):\n%s" % (systemId, nerrors, nwarnings, errordata))
			text = outputdata
		self.setByteStream(StringIO.StringIO(text))
		self.setEncoding(encoding)

class URLInputSource(InputSource):
	"""
	An <class>InputSource</class> where the data is read from
	an &url;.
	"""
	def __init__(self, id, base=None, encoding="utf-8", tidy=False, headers=None, data=None):
		"""
		<par>Create a new <class>StringInputSource</class> instance. Arguments are:</par>
		<ulist>
		<item><arg>id</arg>: The &url; to parse (this can be a <class>str</class>, <class>unicode</class>
		or <pyref module="ll.url" class="URL"><class>ll.url.URL</class></pyref> instance);</item>
		<item><arg>headers</arg>: The additional headers to pass in the request (a dictionary);</item>
		<item><arg>data</arg>: The data the post to <arg>id</arg> (a dictionary).</item>
		</ulist>
		<par>For the rest of the argument see <pyref class="StringInputSource" method="__init__"><method>StringInputSource.__init__</method></pyref>.</par>
		"""
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
		self.setEncoding(encoding)

	def setTimeout(self, secs):
		if timeoutsocket is not None:
			timeoutsocket.setDefaultSocketTimeout(sec)

	def getTimeout(self):
		if timeoutsocket is not None:
			timeoutsocket.getDefaultSocketTimeout()

