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
<par>This file contains everything you need to parse &xist; objects from files, strings, &url;s etc.</par>

<par>It contains different &sax;2 parser driver classes (mostly for sgmlop, everything else
is from <app moreinfo="http://pyxml.sf.net/">PyXML</app>). It includes a
<pyref class="HTMLParser"><class>HTMLParser</class></pyref> that uses sgmlop to parse &html;
and emit &sax;2 events. It also contains various classes derived from
<class>xml.sax.xmlreader.InputSource</class>.</par>
"""

import sys, os, os.path, types, urllib

from xml import sax
from xml.parsers import sgmlop
from xml.sax import expatreader
from xml.sax import saxlib
from xml.sax import handler

from mx import Tidy

#try:
#	import timeoutsocket
#except ImportError:
timeoutsocket = None

from ll import url

import xsc, errors, utils, sources, cssparsers
from ns import ihtml, html

class SGMLOPParser(sax.xmlreader.IncrementalParser, sax.xmlreader.Locator):
	"""
	This is a rudimentary, buggy, halfworking, untested SAX2 drivers for sgmlop.
	And I didn't even know, what I was doing, but it seems to work.
	"""
	def __init__(self, namespaceHandling=0, bufsize=2**16-20, defaultEncoding="utf-8"):
		sax.xmlreader.IncrementalParser.__init__(self, bufsize)
		self.bufsize = bufsize
		self.defaultEncoding = defaultEncoding
		self.reset()

	def whichParser(self):
		return sgmlop.XMLParser()

	def reset(self):
		self.parser = self.whichParser()
		self._parsing = 0
		self.source = None
		self.lineNumber = -1

	def feed(self, data):
		if not self._parsing:
			self.content_handler.startDocument()
			self._parsing = 1
		self.parser.feed(data)

	def close(self):
		self._parsing = 0
		self.parser.close()
		self.content_handler.endDocument()

	def parse(self, source):
		self.source = source
		file = source.getByteStream()
		self.encoding = source.getEncoding()
		if self.encoding is None:
			self.encoding = self.defaultEncoding
		self._parsing = 1
		self.content_handler.setDocumentLocator(self)
		self.content_handler.startDocument()
		self.lineNumber = 1
		# nothing done for the column number, because otherwise parsing would be much to slow.
		self.headerJustRead = 0 # will be used for skipping whitespace after the XML header

		self.parser.register(self)
		try:
			while 1:
				data = file.read(self.bufsize)
				if not data:
					break
				while 1:
					pos = data.find("\n")
					if pos==-1:
						break
					self.parser.feed(data[:pos+1])
					data = data[pos+1:]
					self.lineNumber += 1
				self.parser.feed(data)
			self.close()
		except SystemExit:
			raise
		except KeyboardInterrupt:
			raise
		except Exception, ex:
			if self.error_handler is not None:
				self.error_handler.fatalError(ex)
			else:
				raise
		self.parser.register(None)
		self.source = None
		del self.encoding

	def setErrorHandler(self, handler):
		self.error_handler = handler

	def setContentHandler(self, handler):
		self.content_handler = handler

	def setDTDHandler(self, handler):
		self.dtd_handler = handler

	def setEntityResolver(self, handler):
		self.entity_resolver = handler

	# Locator methods will be called by the application
	def getColumnNumber(self):
		return -1

	def getLineNumber(self):
		if self.parser is None:
			return -1
		return self.lineNumber

	def getPublicId(self):
		if self.source is None:
			return None
		return self.source.getPublicId()

	def getSystemId(self):
		if self.source is None:
			return None
		return self.source.getSystemId()

	def setFeature(self, name, state):
		if name == handler.feature_namespaces:
			if state:
				raise sax.SAXNotSupportedException("no namespace processing available")
		else:
			super(SGMLOPParser, self).setFeature(name, state)

	def getFeature(self, name):
		if name == handler.feature_namespaces:
			return 0
		else:
			super(SGMLOPParser, self).setFeature(name, state)

	def handle_comment(self, data):
		self.content_handler.comment(unicode(data, self.encoding))
		self.headerJustRead = 0

	# don't define handle_charref or handle_cdata, so we will get those through handle_data
	# but unfortunately we have to define handle_charref here, because of a bug in
	# sgmlop: unicode characters i.e. "&#8364;" don't work.

	def handle_charref(self, data):
		data = unicode(data, self.encoding)
		if data[:1] == "x":
			data = unichr(int(data[1:], 16))
		else:
			data = unichr(int(data))
		if not self.headerJustRead or not data.isspace():
			self.content_handler.characters(data)
			self.headerJustRead = 0

	def handle_data(self, data):
		data = unicode(data, self.encoding).replace(u"\r\n", u"\n").replace(u"\r", u"\n")
		if not self.headerJustRead or not data.isspace():
			self.content_handler.characters(data)
			self.headerJustRead = 0

	def handle_proc(self, target, data):
		target = unicode(target, self.encoding)
		data = unicode(data, self.encoding)
		if target!=u'xml': # Don't report <?xml?> as a processing instruction
			self.content_handler.processingInstruction(target, data)
			self.headerJustRead = 0
		else: # extract the encoding
			encodingFound = utils.findAttr(data, u"encoding")
			if encodingFound is not None:
				self.encoding = encodingFound
			self.headerJustRead = 1

	def handle_entityref(self, name):
		if name=="lt":
			self.content_handler.characters(u"<")
		elif name=="gt":
			self.content_handler.characters(u">")
		elif name=="amp":
			self.content_handler.characters(u"&")
		elif name=="quot":
			self.content_handler.characters(u'"')
		elif name=="apos":
			self.content_handler.characters(u"'")
		else:
			self.content_handler.skippedEntity(unicode(name, self.encoding))
		self.headerJustRead = 0

	def finish_starttag(self, name, attrs):
		newattrs = sax.xmlreader.AttributesImpl({})
		for (attrname, attrvalue) in attrs.items():
			if attrvalue is None:
				attrvalue = attrname
			else:
				attrvalue = self._string2Fragment(unicode(attrvalue, self.encoding))
			newattrs._attrs[unicode(attrname, self.encoding)] = attrvalue
		self.content_handler.startElement(unicode(name, self.encoding), newattrs)
		self.headerJustRead = 0

	def finish_endtag(self, name):
		self.content_handler.endElement(unicode(name, self.encoding))
		self.headerJustRead = 0

	def _string2Fragment(self, text):
		"""
		parses a string that might contain entities into a fragment
		with text nodes, entities and character references.
		"""
		if text is None:
			return xsc.Null
		node = xsc.Frag()
		while 1:
			try:
				i = text.index("&")
				if i != 0:
					node.append(text[:i])
					text = text[i:]
				try:
					i = text.index(";")
					if text[1] == "#":
						if text[2] == "x":
							node.append(unichr(int(text[3:i], 16)))
						else:
							node.append(unichr(int(text[2:i])))
					else:
						node.append(self.content_handler.prefixes.entityFromQName(text[1:i])())
					text = text[i+1:]
				except ValueError:
					raise errors.MalformedCharRefError(text)
			except ValueError:
				if len(text):
					node.append(text)
				break
		if not len(node):
			node.append("")
		return node

class BadEntityParser(SGMLOPParser):
	"""
	<par>A &sax;2 parser that recognizes the character entities
	defined in &html; and tries to pass on unknown or malformed
	entities to the handler literally.</par>
	"""

	def _string2Fragment(self, text):
		"""
		This version tries to pass illegal content literally.
		"""
		if text is None:
			return xsc.Null
		node = xsc.Frag()
		parts = text.split("&")
		node.append(parts[0])
		del parts[0]
		for part in parts:
			pos = part.find(";")
			if pos == -1: # no ; found, so it's no entity => append it literally
				node.append("&", part)
			else: # ; found
				if part[0] != "#": # named entity
					name = part[:pos]
					if html.namespace.charrefsByName.has_key(name):
						node.append(html.namespace.charrefsByName[name](), part[pos+1:])
					elif xsc.namespace.charrefsByName.has_key(name):
						node.append(xsc.namespace.charrefsByName[name](), part[pos+1:])
					else:
						node.append("&", part)
				else: # numeric entity
					try:
						if part[1] == "x": # hex entity
							node.append(unichr(int(part[2:pos], 16)), part[pos+1:])
						else: # decimal entity
							node.append(unichr(int(part[1:pos])), part[pos+1:])
					except ValueError: # illegal format => append it literally
						node.append("&", part)
		return node

class HTMLParser(BadEntityParser):
	"""
	<par>A &sax;2 parser that can parse &html;.</par>
	"""

	headElements = ("title", "base", "script", "style", "meta", "link", "object") # Elements that may appear in the <head>
	minimizedElements = {"p": ("p",), "td": ("td", "th"), "th": ("td", "th")} # elements that can't be nested, so a start tag automatically closes a previous end tag

	def __init__(self, namespaceHandling=0, bufsize=2**16-20, defaultEncoding="iso-8859-1"):
		SGMLOPParser.__init__(self, namespaceHandling, bufsize, defaultEncoding)

	def whichParser(self):
		return sgmlop.SGMLParser()

	def reset(self):
		SGMLOPParser.reset(self)
		self.__nesting = []

	def close(self):
		while len(self.__nesting): # close all open elements
			self.finish_endtag(self.__nesting[-1])
		SGMLOPParser.close(self)

	def handle_comment(self, data):
		self.__closeEmpty()
		SGMLOPParser.handle_comment(self, data)

	def handle_data(self, data):
		self.__closeEmpty()
		SGMLOPParser.handle_data(self, data)

	def handle_proc(self, target, data):
		self.__closeEmpty()
		SGMLOPParser.handle_proc(self, target, data)

	def handle_entityref(self, name):
		self.__closeEmpty()
		SGMLOPParser.handle_entityref(self, name)

	def finish_starttag(self, name, attrs):
		self.__closeEmpty()
		name = name.lower()
		if name != "html":
			if not len(self.__nesting): # root element <html> missing?
				self.finish_starttag("html", []) # add it
			self.__closeMimimizedOnStart(name)

		self.__nesting.append(name)
		newattrs = {}
		for (attrname, attrvalue) in attrs:
			attrname = attrname.lower()
			element = html.xmlns.elementsByName[name]
			if element.isallowedattr(attrname):
				newattrs[attrname] = attrvalue
			else:
				errors.warn(errors.IllegalAttrError(element.Attrs, attrname))
		SGMLOPParser.finish_starttag(self, name, newattrs)

	def finish_endtag(self, name):
		name = name.lower()
		if len(self.__nesting): # we ignore end tag without the matching start tags
			if self.__nesting[-1] != name: # e.g. <div><img></div> when </div> is encountered
				self.__closeEmpty()
			if self.__nesting[-1] != name:
				self.__closeMinimizedOnEnd(name) #  maybe an open <p> tag etc. has been left open; eg. <div><p>gurk</div>
			SGMLOPParser.finish_endtag(self, name)
			del self.__nesting[-1]

	def __closeEmpty(self):
		if len(self.__nesting) and html.xmlns.elementsByName[self.__nesting[-1]].empty:
			self.finish_endtag(self.__nesting[-1])

	def __closeMimimizedOnStart(self, name):
		if len(self.__nesting):
			lastname = self.__nesting[-1]
			try:
				minigroup = self.minimizedElements[lastname]
			except KeyError:
				return
			if name in minigroup: # starting a tag from the same group?
				self.finish_endtag(name)

	def __closeMinimizedOnEnd(self, name):
		if len(self.__nesting):
			lastname = self.__nesting[-1]
			try:
				minigroup = self.minimizedElements[lastname]
			except KeyError:
				return
			if not self.minimizedElements.has_key(name):
				self.finish_endtag(lastname)

ExpatParser = expatreader.ExpatParser

class Handler(object):
	"""
	contains the parser and the options and functions for handling XML files
	"""

	def __init__(self, parser=None, prefixes=None):
		if parser is None:
			parser = SGMLOPParser()
		self.parser = parser

		if prefixes is None:
			prefixes = xsc.OldPrefixes()
		self.prefixes = prefixes

		self._locator = None

	def parse(self, source):
		self.source = source
		self.base = getattr(self.source, "base", None)

		# register us for callbacks
		self.parser.setErrorHandler(self)
		self.parser.setContentHandler(self)
		self.parser.setDTDHandler(self)
		self.parser.setEntityResolver(self)

		# Configure the parser
		self.parser.setFeature(handler.feature_namespaces, 0) # We do our own namespace processing

		self.skippingWhitespace = 0
		self.parser.parse(source)

		# unregister us to break the cycles
		self.parser.setEntityResolver(None)
		self.parser.setDTDHandler(None)
		self.parser.setContentHandler(None)
		self.parser.setErrorHandler(None)

	def close(self):
		self.root = None
		self.source = None
		self.base = None

	def setDocumentLocator(self, locator):
		self._locator = locator

	def startDocument(self):
		# our nodes do not have a parent link, therefore we have to store the active
		# path through the tree in a stack (which we call __nesting)
		# and we store the namespace prefixes defined by the elements

		# after we've finished parsing, the Frag that we put at the bottom of the stack will be our document root
		self.__nesting = [ (xsc.Frag(),) ]

	def endDocument(self):
		self.root = self.__nesting[0][0]
		self.__nesting = None

	def startElement(self, name, attrs):
		prefixes = []
		for (attrname, attrvalue) in attrs.items():
			if attrname=="xmlns":
				prefix = None
				type = xsc.Prefixes.ELEMENT
			elif attrname.startswith("xmlns:"):
				prefix = attrname[6:]
				type = xsc.Prefixes.ELEMENT
			elif attrname=="procinstns":
				prefix = None
				type = xsc.Prefixes.PROCINST
			elif attrname.startswith("procinstns:"):
				prefix = attrname[11:]
				type = xsc.Prefixes.PROCINST
			elif attrname=="entityns":
				prefix = None
				type = xsc.Prefixes.ENTITY
			elif attrname.startswith("entityns:"):
				prefix = attrname[9:]
				type = xsc.Prefixes.ENTITY
			else:
				continue
			prefixes.append((type, prefix))
			self.prefixes.startPrefixMapping(prefix, unicode(attrvalue), "replace", type)
		node = self.prefixes.elementFromQName(name)()
		node.parsed(self)
		for (attrname, attrvalue) in attrs.items():
			if attrname!="xmlns" and not attrname.startswith("xmlns:") and \
			   attrname!="procinstns" and not attrname.startswith("procinstns:") and \
			   attrname!="entityns" and not attrname.startswith("entityns:"):
				attrname = self.prefixes.attrnameFromQName(node, attrname)
				node[attrname] = attrvalue
				node[attrname].parsed(self)
		self.__appendNode(node)
		self.__nesting.append((node, prefixes)) # push new innermost element onto the stack, together with the list of prefix mappings defined by this node
		self.skippingWhitespace = 0

	def endElement(self, name):
		element = self.prefixes.elementFromQName(name)
		currentelement = self.__nesting[-1][0].__class__
		if element is not currentelement:
			raise errors.ElementNestingError(currentelement, element)
		self.__nesting[-1][0].endLoc = self.getLocation()
		# SAX specifies that the order of calls to endPrefixMapping is undefined, so we use the same order as in beginElement
		for (type, prefix) in self.__nesting[-1][1]:
			self.prefixes.endPrefixMapping(prefix, type)
		self.__nesting.pop() # pop the innermost element off the stack
		self.skippingWhitespace = 0

	def characters(self, content):
		if self.skippingWhitespace:
			# the following could be content = content.lstrip(), but this would remove nbsps
			# FIXME use lstrip(???) with Python 2.3
			while content and content[0].isspace() and content[0] != "\xa0":
				content = content[1:]
		if content:
			node = xsc.Text(content)
			node.parsed(self)
			last = self.__nesting[-1][0]
			if len(last) and isinstance(last[-1], xsc.Text):
				node = last[-1] + node.content # join consecutive Text nodes
				node.startLoc = last[-1].startLoc # make sure the replacement node has the original location
				last[-1] = node # replace it
			else:
				self.__appendNode(node)
			self.skippingWhitespace = 0

	def comment(self, content):
		node = xsc.Comment(content)
		node.parsed(self)
		self.__appendNode(node)
		self.skippingWhitespace = 0

	def processingInstruction(self, target, data):
		if target=="x":
			self.skippingWhitespace = 1
		else:
			node = self.prefixes.procInstFromQName(target)(data)
			node.parsed(self)
			self.__appendNode(node)
			self.skippingWhitespace = 0

	def skippedEntity(self, name):
		node = self.prefixes.entityFromQName(name)()
		node.parsed(self)
		if isinstance(node, xsc.CharRef):
			self.characters(unichr(node.codepoint))
		else:
			self.__appendNode(node)
		self.skippingWhitespace = 0

	def __decorateException(self, exception):
		if not isinstance(exception, saxlib.SAXParseException):
			msg = exception.__class__.__name__
			msg2 = str(exception)
			if msg2:
				msg += ": " + msg2
			exception = saxlib.SAXParseException(msg, exception, self._locator)
		return exception

	def error(self, exception):
		"Handle a recoverable error."
		raise self.__decorateException(exception)

	def fatalError(self, exception):
		"Handle a non-recoverable error."
		raise self.__decorateException(exception)

	def warning(self, exception):
		"Handle a warning."
		print self.__decorateException(exception)

	def getLocation(self):
		return xsc.Location(self._locator)

	def __appendNode(self, node):
		node.startLoc = self.getLocation()
		self.__nesting[-1][0].append(node) # add the new node to the content of the innermost element (or fragment)

def parse(source, handler=None, parser=None, prefixes=None):
	if handler is None:
		handler = Handler(parser, prefixes=prefixes)
	handler.parse(source)
	result = handler.root
	handler.close()
	return result

def parseString(text, systemId="STRING", base=None, handler=None, parser=None, prefixes=None, defaultEncoding="utf-8", tidy=0):
	return parse(sources.StringInputSource(text, systemId=systemId, base=base, defaultEncoding=defaultEncoding, tidy=tidy), handler=handler, parser=parser, prefixes=prefixes)

def parseURL(id, base=None, handler=None, parser=None, prefixes=None, defaultEncoding="utf-8", tidy=0, headers=None, data=None):
	return parse(sources.URLInputSource(id, base=base, defaultEncoding=defaultEncoding, tidy=tidy, headers=headers, data=data), handler=handler, parser=parser, prefixes=prefixes)

def parseFile(filename, base=None, handler=None, parser=None, prefixes=None, defaultEncoding="utf-8", tidy=0):
	return parseURL(url.Filename(filename), base=base, defaultEncoding=defaultEncoding, tidy=tidy, handler=handler, parser=parser, prefixes=prefixes)
