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
<doc:par>This file contains everything you need to parse &xist; objects from files, strings, &url;s etc.</doc:par>

<doc:par>It contains different &sax;2 parser driver classes (mostly for sgmlop, everything else
is from <app moreinfo="http://pyxml.sf.net/">PyXML</app>). It includes a
<pyref class="HTMLParser"><class>HTMLParser</class></pyref> that uses sgmlop to parse &html;
and emit &sax;2 events. It also contains various classes derived from
<class>xml.sax.xmlreader.InputSource</class>.</doc:par>
"""

from __future__ import nested_scopes # for the lambda in the call to replaceInitialURL

import sys, os, os.path, types, cStringIO as StringIO, urllib

from xml import sax
from xml.parsers import sgmlop
from xml.sax import expatreader
from xml.sax import saxlib

from mx import Tidy

#try:
#	import timeoutsocket
#except ImportError:
timeoutsocket = None

import fileutils

import xsc, url as url_, errors, utils
from ns import html

class InputSource(sax.xmlreader.InputSource):
	def __init__(self, base):
		sax.xmlreader.InputSource.__init__(self)
		self.base = base

class StringInputSource(InputSource):
	def __init__(self, text, base=None, defaultEncoding="utf-8"):
		InputSource.__init__(self, base)
		self.setSystemId("STRING")
		if type(text) is types.UnicodeType:
			defaultEncoding = "utf-8"
			text = text.encode(defaultEncoding)
		self.setByteStream(StringIO.StringIO(text))
		self.setEncoding(defaultEncoding)

class FileInputSource(InputSource):
	def __init__(self, stream, base=None, defaultEncoding="utf-8"):
		InputSource.__init__(self, base)
		self.setSystemId(str(base))
		if isinstance(stream, (str, unicode)):
			stream = fileutils.Filename(stream)
		if isinstance(stream, fileutils.Filename):
			stream = stream.open("rb")
		self.setByteStream(stream)
		self.setEncoding(defaultEncoding)

class URLInputSource(InputSource):
	def __init__(self, url, defaultEncoding="utf-8"):
		if isinstance(url, url_.URL):
			url = url.asPlainString()
		InputSource.__init__(self, url)
		self.setSystemId(url)
		if type(url) is types.UnicodeType:
			url = url.encode("utf-8")
		self.setByteStream(urllib.urlopen(url))
		self.setEncoding(defaultEncoding)

	def setTimeout(self, secs):
		if timeoutsocket is not None:
			timeoutsocket.setDefaultSocketTimeout(sec)

	def getTimeout(self):
		if timeoutsocket is not None:
			timeoutsocket.getDefaultSocketTimeout()

class TidyURLInputSource(InputSource):
	def __init__(self, url, defaultEncoding="utf-8"):
		if isinstance(url, url_.URL):
			url = url.asPlainString()
		InputSource.__init__(self, url)
		self.setSystemId(url)
		if type(url) is types.UnicodeType:
			url = url.encode("utf-8")
		(nerrors, nwarnings, outputdata, error) = Tidy.tidy(urllib.urlopen(url).read(), numeric_entities=1, output_xhtml=1, output_xml=1, quiet=1, tidy_mark=0, wrap=0)
		if nerrors>0:
			raise SAXParseException("can't tidy %r: %r" % (url, errordata))
		self.setByteStream(StringIO.StringIO(outputdata))
		self.setEncoding(defaultEncoding)

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
			raise
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

	def handle_comment(self, data):
		self.content_handler.comment(unicode(data, self.encoding))
		self.headerJustRead = 0

	# don't define handle_charref or handle_cdata, so we will get those through handle_data

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
						try:
							node.append(self.content_handler.namespaces.entityFromName(text[1:i])())
						except KeyError:
							raise errors.UnknownEntityError(text[1:i])
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

class HTMLParser(SGMLOPParser):
	"""
	A SAX2 parser that can parse HTML.
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
			newattrs[attrname.lower()] = attrvalue
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
		if len(self.__nesting) and html.namespace.elementsByName[self.__nesting[-1]].empty:
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
					try:
						node.append(html.namespace.entitiesByName[part[:pos]](), part[pos+1:])
					except KeyError: # no entity with such a name => append it literally
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

ExpatParser = expatreader.ExpatParser

level = 0
class Handler(object):
	"""
	contains the parser and the options and functions for handling XML files
	"""

	def __init__(self, parser=None, namespaces=None):
		if parser is None:
			parser = SGMLOPParser()
		self.parser = parser

		if namespaces is None:
			namespaces = xsc.defaultNamespaces
		self.namespaces = namespaces

	def parse(self, source):
		self.source = source

		# register us for callbacks
		self.parser.setErrorHandler(self)
		self.parser.setContentHandler(self)
		self.parser.setDTDHandler(self)
		self.parser.setEntityResolver(self)

		self.skippingWhitespace = 0
		self.parser.parse(source)

		# unregister us to break the cycles
		self.parser.setEntityResolver(None)
		self.parser.setDTDHandler(None)
		self.parser.setContentHandler(None)
		self.parser.setErrorHandler(None)

	def setDocumentLocator(self, locator):
		self._locator = locator

	def startDocument(self):
		# our nodes do not have a parent link, therefore we have to store the active
		# path through the tree in a stack (which we call __nesting)

		# after we've finished parsing, the Frag that we put at the bottom of the stack will be our document root
		self.__nesting = [ xsc.Frag() ]

	def endDocument(self):
		self.root = self.__nesting[0]
		self.__nesting = None

	def startElement(self, name, attrs):
		node = self.namespaces.elementFromName(name)()
		for (attrname, attrvalue) in attrs.items():
			# for URLs incorporate the base URL into the value
			if node.attrHandlers.has_key(attrname) and issubclass(node.attrHandlers[attrname], xsc.URLAttr) and hasattr(self.source, "base"):
				if isinstance(attrvalue, unicode):
					attrvalue = xsc.Frag(attrvalue)
				attrvalue = utils.replaceInitialURL(attrvalue, lambda u: url_.URL(self.source.base)/u )
			node[attrname] = attrvalue
		self.__appendNode(node)
		self.__nesting.append(node) # push new innermost element onto the stack
		self.skippingWhitespace = 0

	def endElement(self, name):
		element = self.namespaces.elementFromName(name)
		currentelement = self.__nesting[-1].__class__
		if element is not currentelement:
			raise errors.ElementNestingError(currentelement, element)
		self.__nesting[-1].endLoc = self.getLocation()
		self.__nesting.pop() # pop the innermost element off the stack
		self.skippingWhitespace = 0

	def characters(self, content):
		if self.skippingWhitespace:
			content = content.lstrip()
		if content:
			last = self.__nesting[-1]
			if len(last) and isinstance(last[-1], xsc.Text):
				last[-1] += content # join consecutive Text nodes
			else:
				self.__appendNode(xsc.Text(content))
			self.skippingWhitespace = 0

	def comment(self, content):
		self.__appendNode(xsc.Comment(content))
		self.skippingWhitespace = 0

	def processingInstruction(self, target, data):
		if target=="x":
			self.skippingWhitespace = 1
		else:
			self.__appendNode(self.namespaces.procInstFromName(target)(data))
			self.skippingWhitespace = 0

	def skippedEntity(self, name):
		node = self.namespaces.entityFromName(name)()
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
		self.__nesting[-1].append(node) # add the new node to the content of the innermost element (or fragment)

def parse(source, handler=None, parser=None, namespaces=None):
	if handler is None:
		handler = Handler(parser, namespaces)
	handler.parse(source)
	return handler.root

def parseString(text, base=None, handler=None, parser=None, namespaces=None, defaultEncoding="utf-8"):
	return parse(StringInputSource(text, base=base, defaultEncoding=defaultEncoding), handler=handler, parser=parser, namespaces=namespaces)

def parseFile(filename, base=None, handler=None, parser=None, namespaces=None, defaultEncoding="utf-8"):
	return parse(FileInputSource(filename, base=base, defaultEncoding=defaultEncoding), handler=handler, parser=parser, namespaces=namespaces)

def parseURL(url, handler=None, parser=None, namespaces=None, defaultEncoding="utf-8"):
	return parse(URLInputSource(url, defaultEncoding=defaultEncoding), handler=handler, parser=parser, namespaces=namespaces)

def parseTidyURL(url, handler=None, parser=None, namespaces=None, defaultEncoding="utf-8"):
	return parse(TidyURLInputSource(url, defaultEncoding=defaultEncoding), handler=handler, parser=parser, namespaces=namespaces)

