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
<doc:par>This file contains everything you need to parse &xist; objects from files, strings, &url;s etc.</doc:par>

<doc:par>It contains different &sax;2 parser driver classes (mostly for sgmlop, everything else
is from <app moreinfo="http://pyxml.sf.net/">PyXML</app>). It includes a
<pyref class="HTMLParser"><class>HTMLParser</class></pyref> that uses sgmlop to parse &html;
and emit &sax;2 events. It also contains various classes derived from
<class>xml.sax.xmlreader.InputSource</class>.</doc:par>
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

def parseString(text, systemId="STRING", base=None, handler=None, defaultEncoding="utf-8", ignoreCharset=0):
	return parse(sources.StringInputSource(text, systemId=systemId, base=base, defaultEncoding=defaultEncoding), handler=handler, ignoreCharset=ignoreCharset)

def parseURL(id, base=None, handler=None, defaultEncoding="utf-8", ignoreCharset=0, headers=None, data=None):
	return parse(sources.URLInputSource(id, base=base, defaultEncoding=defaultEncoding, headers=headers, data=data), handler=handler, ignoreCharset=ignoreCharset)

def parseFile(filename, base=None, handler=None, defaultEncoding="utf-8", ignoreCharset=0):
	return parseURL(url.Filename(filename), base=base, defaultEncoding=defaultEncoding, handler=handler, ignoreCharset=ignoreCharset)

