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

import cStringIO as StringIO, warnings

from xml import sax
from xml.sax import saxlib

from ll import url

import xsc, errors

class TidyArgs(xsc.Args):
	add_xml_decl = True
	assume_xml_procins = True
	bare = True
	break_before_br = False
	doctype = "loose"
	drop_proprietary_attributes = True
	fix_bad_comments = True
	fix_uri = True
	join_styles = False
	lower_literals = True
	ncr = True
	numeric_entities = True
	output_xhtml = True
	output_xml = True
	quote_ampersand = True
	quote_nbsp = False
	literal_attributes = True
	markup = True
	wrap = 0
	wrap_php = False
	wrap_sections = False
	ascii_chars = False
	force_output = True
	tidy_mark = False

def tidystring(text, encoding, sysid, args):
	args = TidyArgs(args)
	args["input_encoding"] = encoding
	args["output_encoding"] = "utf8"

	try:
		import tidy
	except ImportError:
		from mx import Tidy
		args["quiet"] = 1
		(nerrors, nwarnings, outputdata, errordata) = Tidy.tidy(text, **args)
		if nerrors>0:
			raise saxlib.SAXException("can't tidy %r (%d errors, %d warnings):\n%s" % (sysid, nerrors, nwarnings, errordata))
		text = outputdata
	else:
		doc = tidy.parseString(text, **args)
		for error in doc.get_errors():
			warning = errors.TidyWarning(error.message, xsc.Location(sysid=sysid, line=error.line, col=error.col))
			warnings.warn(warning)
		text = str(doc)
	return (text, "utf-8")

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
	def __init__(self, text, sysid="STRING", base=None, encoding=None, tidy=False):
		"""
		<par>Create a new <class>StringInputSource</class> instance. Arguments are:</par>
		<ulist>
		<item><arg>text</arg>: The text to be parsed;</item>
		<item><arg>sysid</arg>: The system id to be used;</item>
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
		self.setSystemId(sysid)
		if isinstance(text, unicode):
			encoding = "utf-8"
			text = text.encode(encoding)
		if isinstance(tidy, int):
			if tidy:
				tidy = {}
			else:
				tidy = None
		if tidy is not None:
			(text, encoding) = tidystring(text, encoding, sysid, tidy)
		self.setByteStream(StringIO.StringIO(text))
		if encoding is not None:
			self.setEncoding(encoding)

class URLInputSource(InputSource):
	"""
	An <class>InputSource</class> where the data is read from
	an &url;.
	"""
	def __init__(self, id, base=None, encoding=None, tidy=False, headers=None, data=None):
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
		sysid = id.url
		self.setSystemId(sysid)
		resource = id.openread(headers=headers, data=data)
		if isinstance(tidy, int):
			if tidy:
				tidy = {}
			else:
				tidy = None
		if tidy is not None:
			text = resource.read()
			(text, encoding) = tidystring(text, encoding, sysid, tidy)
			resource = StringIO.StringIO(text)
		self.setByteStream(resource)
		if encoding is not None:
			self.setEncoding(encoding)

