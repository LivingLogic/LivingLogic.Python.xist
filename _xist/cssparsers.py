#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>This file contains classes that make it possible to transform &url;s found inside
&css; code (either <lit>style</lit> attributes or complete &css; files).</par>
"""

import cStringIO

from ll import url

from ll.xist import csstokenizer


class Handler(object):
	def __init__(self, encoding="utf-8", ignorecharset=False):
		self.texts = []
		self.base = None
		self.encoding = encoding
		self.ignorecharset = ignorecharset

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

	def _parse(self, stream, base, encoding):
		self.base = url.URL(base)
		self.encoding = encoding
		tokenizer = csstokenizer.CSSTokenizer()
		tokenizer.register(self)
		data = stream.read()
		tokenizer.parse(data)
		data = unicode(self)
		tokenizer.register(None)
		self.texts = []
		self.base = None
		return data

	def parse(self, stream, base=None):
		return self.parse(stream, base, self.encoding)

	def parseString(self, string, base=None):
		if isinstance(string, unicode):
			encoding = "utf-8"
			string = string.encode(encoding)
		else:
			encoding = self.encoding
		stream = cStringIO.StringIO(string)
		if base is None:
			base = "STRING"
		return self._parse(stream, base, encoding)

	def parseURL(self, name, base=None, headers=None, data=None):
		stream = name.openread(headers=headers, data=data)
		if base is None:
			base = stream.finalurl
		return self._parse(stream, base, self.encoding)

	def parseFile(self, name, base=None):
		stream = open(name, "r")
		if base is None:
			base = url.File(name)
		return self._parse(stream, base, self.encoding)


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
