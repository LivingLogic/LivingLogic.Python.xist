#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>This file contains everything you need to parse &xist; objects from files, strings, &url;s etc.</par>

<par>It contains different &sax;2 parser driver classes (mostly for sgmlop, everything else
is from <app moreinfo="http://pyxml.sf.net/">PyXML</app>). It includes a
<pyref class="HTMLParser"><class>HTMLParser</class></pyref> that uses sgmlop to parse &html;
and emit &sax;2 events. It also contains various classes derived from
<class>xml.sax.xmlreader.InputSource</class>.</par>
"""

from ll import url

import sources, csstokenizer

class Handler(object):
	def __init__(self):
		self.close()

	def startDocument(self):
		self.texts = []

	def endDocument(self):
		pass

	def token(self, token, data):
		data = unicode(data, self.encoding)
		if token=="URI":
			u = url.URL(data)
			u = self.transformURL(u)
			self.texts.append(u"url(%s)" % unicode(u))
		elif token in ("EX", "EM", "CM", "MM", "IN", "MS", "HZ", "S", "PC", "PT", "PX", "DEG", "RAD", "GRAD", "KHZ"):
			self.texts.append(u"%s%s" % (data, token.lower()))
		elif token=="COMMENT":
			self.texts.append(u"/*%s*/" % data)
		elif token=="HASH":
			self.texts.append(u"#%s" % data)
		elif token=="FUNCTION":
			self.texts.append(u"%s(" % data)
		elif token=="STRING":
			if u'"' in data:
				self.texts.append(u"'%s'" % data)
			elif u"'" in data:
				raise ValueError("' found in %r" % data)
			else:
				self.texts.append(u'"%s"' % data)
		elif token in ("IMPORT_SYMBOL", "AT_KEYWORD", "FONT_FACE_SYMBOL", "MEDIA_SYMBOL", "PAGE_SYMBOL"):
			self.texts.append(u"@%s" % data)
		elif token=="CHARSET_SYMBOL":
			self.texts.append(u"@%s" % data)
			if not self.ignorecharset:
				self.encoding = data.encode("ascii")
		elif token=="PERCENTAGE":
			self.texts.append(u"%s%%" % data)
		else:
			self.texts.append(data)

	def __unicode__(self):
		return u"".join(self.texts)

	def transformURL(self, u):
		return u

	def close(self):
		self.texts = []
		self.soure = None
		self.base = None

	def parse(self, source, ignoreCharset=0):
		self.source = source
		self.base = getattr(source, "base", None)
		self.encoding = source.getEncoding()
		self.ignoreCharset = ignoreCharset
		tokenizer = csstokenizer.CSSTokenizer()
		tokenizer.register(self)
		data = source.getByteStream().read()
		tokenizer.parse(data)
		data = unicode(self)
		tokenizer.register(None)

class ParseHandler(Handler):
	def transformURL(self, u):
		if self.base is not None:
			u = self.base/u
		return u

class PublishHandler(Handler):
	def transformURL(self, u):
		if self.base is not None:
			u = u.relative(self.base)
		return u

class CollectHandler(Handler):
	def startDocument(self):
		super(CollectHandler, self).startDocument()
		self.urls = []

	def transformURL(self, u):
		self.urls.append(u)
		return u

def parse(source, handler=None, ignoreCharset=0):
	if handler is None:
		handler = Handler()
	handler.parse(source, ignoreCharset=ignoreCharset)
	result = unicode(handler)
	handler.close()
	return result

def parseString(text, systemId="STRING", base=None, handler=None, encoding="utf-8", ignoreCharset=0):
	return parse(sources.StringInputSource(text, systemId=systemId, base=base, encoding=encoding), handler=handler, ignoreCharset=ignoreCharset)

def parseURL(id, base=None, handler=None, encoding="utf-8", ignoreCharset=0, headers=None, data=None):
	return parse(sources.URLInputSource(id, base=base, encoding=encoding, headers=headers, data=data), handler=handler, ignoreCharset=ignoreCharset)

def parseFile(filename, base=None, handler=None, encoding="utf-8", ignoreCharset=0):
	return parseURL(url.Filename(filename), base=base, encoding=encoding, handler=handler, ignoreCharset=ignoreCharset)

