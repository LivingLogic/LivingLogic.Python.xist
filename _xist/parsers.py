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
and emit &sax;2 events.</par>
"""

import sys, os, os.path, types, urllib, warnings

from xml import sax
from xml.parsers import sgmlop
from xml.sax import expatreader
from xml.sax import saxlib
from xml.sax import handler
from xml.dom import html as htmldtd

from ll import url

import xsc, errors, utils, sources, cssparsers
from ns import ihtml, html

class SGMLOPParser(sax.xmlreader.IncrementalParser, sax.xmlreader.Locator):
	"""
	This is a rudimentary, buggy, halfworking, untested SAX2 drivers for sgmlop.
	And I didn't even know, what I was doing, but it seems to work.
	"""
	def __init__(self, namespaceHandling=0, bufsize=2**16-20, encoding=None):
		sax.xmlreader.IncrementalParser.__init__(self, bufsize)
		if encoding is None:
			encoding = "utf-8"
		self.encoding = encoding
		self._parser = None
		self.reset()

	def _whichparser(self):
		return sgmlop.XMLParser()

	def _makestring(self, data):
		return unicode(data, self.encoding).replace(u"\r\n", u"\n").replace(u"\r", u"\n")

	def reset(self):
		self.close()
		self.source = None
		self.lineNumber = -1

	def feed(self, data):
		if self._parser is None:
			self._parser = self._whichparser()
			self._parser.register(self)
			self._cont_handler.startDocument()
		self._parser.feed(data)

	def close(self):
		if self._parser is not None:
			self._parser.close()
			self._parser.register(None)
			self._parser = None
			self._cont_handler.endDocument()

	def parse(self, source):
		self.source = source
		file = source.getByteStream()
		encoding = source.getEncoding()
		if encoding is not None:
			self.encoding = encoding
		self._cont_handler.setDocumentLocator(self)
		self._cont_handler.startDocument()
		self.lineNumber = 1
		# we don't keep a column number, because otherwise parsing would be much to slow
		self.headerJustRead = False # will be used for skipping whitespace after the XML header

		parsed = False
		try:
			while True:
				data = file.read(self._bufsize)
				if not data:
					if not parsed:
						self.feed("")
					break
				while True:
					pos = data.find("\n")
					if pos==-1:
						break
					self.feed(data[:pos+1])
					self.parsed = True
					data = data[pos+1:]
					self.lineNumber += 1
				self.feed(data)
				self.parsed = True
		except SystemExit:
			raise
		except KeyboardInterrupt:
			raise
		except Exception, exc:
			if self._err_handler is not None:
				self._err_handler.fatalError(exc)
			else:
				raise
		self.close()
		self.source = None
		del self.encoding

	# Locator methods will be called by the application
	def getColumnNumber(self):
		return -1

	def getLineNumber(self):
		if self._parser is None:
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
		elif name == handler.feature_external_ges:
			if state:
				raise sax.SAXNotSupportedException("processing of external general entities not available")
		else:
			sax.xmlreader.IncrementalParser.setFeature(self, name, state)

	def getFeature(self, name):
		if name == handler.feature_namespaces:
			return 0
		else:
			sax.xmlreader.IncrementalParser.setFeature(self, name, state)

	def handle_comment(self, data):
		self._cont_handler.comment(self._makestring(data))
		self.headerJustRead = False

	# don't define handle_charref or handle_cdata, so we will get those through handle_data
	# but unfortunately we have to define handle_charref here, because of a bug in
	# sgmlop: unicode characters i.e. "&#8364;" don't work.

	def handle_charref(self, data):
		data = self._makestring(data)
		if data.startswith(u"x"):
			data = unichr(int(data[1:], 16))
		else:
			data = unichr(int(data))
		if not self.headerJustRead or not data.isspace():
			self._cont_handler.characters(data)
			self.headerJustRead = False

	def handle_data(self, data):
		data = self._makestring(data)
		if not self.headerJustRead or not data.isspace():
			self._cont_handler.characters(data)
			self.headerJustRead = False

	def handle_proc(self, target, data):
		target = self._makestring(target)
		data = self._makestring(data)
		if target!=u'xml': # Don't report <?xml?> as a processing instruction
			self._cont_handler.processingInstruction(target, data)
			self.headerJustRead = False
		else: # extract the encoding
			encodingFound = utils.findAttr(data, u"encoding")
			if encodingFound is not None:
				self.encoding = encodingFound
			self.headerJustRead = True

	def handle_entityref(self, name):
		try:
			c = {"lt": u"<", "gt": u">", "amp": u"&", "quot": u'"', "apos": u"'"}[name]
		except KeyError:
			self._cont_handler.skippedEntity(self._makestring(name))
		else:
			self._cont_handler.characters(c)
		self.headerJustRead = False

	def finish_starttag(self, name, attrs):
		newattrs = sax.xmlreader.AttributesImpl({})
		for (attrname, attrvalue) in attrs.items():
			if attrvalue is None:
				attrvalue = attrname
			else:
				attrvalue = self._string2Fragment(self._makestring(attrvalue))
			newattrs._attrs[self._makestring(attrname)] = attrvalue
		self._cont_handler.startElement(self._makestring(name), newattrs)
		self.headerJustRead = False

	def finish_endtag(self, name):
		self._cont_handler.endElement(self._makestring(name))
		self.headerJustRead = False

	def _string2Fragment(self, text):
		"""
		parses a string that might contain entities into a fragment
		with text nodes, entities and character references.
		"""
		if text is None:
			return xsc.Null
		ct = self._cont_handler.createText
		node = xsc.Frag()
		while True:
			texts = text.split(u"&", 1)
			text = texts[0]
			if text:
				node.append(ct(text))
			if len(texts)==1:
				break
			texts = texts[1].split(u";", 1)
			name = texts[0]
			if len(texts)==1:
				raise errors.MalformedCharRefWarning(name)
			if name.startswith(u"#"):
				try:
					if name.startswith(u"#x"):
						node.append(ct(unichr(int(name[2:], 16))))
					else:
						node.append(ct(unichr(int(name[1:]))))
				except ValueError:
					raise errors.MalformedCharRefWarning(name)
			else:
				try:
					c = {"lt": u"<", "gt": u">", "amp": u"&", "quot": u'"', "apos": u"'"}[name]
				except KeyError:
					node.append(self._cont_handler.createEntity(name))
				else:
					node.append(ct(c))
			text = texts[1]
		if not node:
			node.append(ct(u""))
		return node

class BadEntityParser(SGMLOPParser):
	"""
	<par>A &sax;2 parser that recognizes the character entities
	defined in &html; and tries to pass on unknown or malformed
	entities to the handler literally.</par>
	"""

	def handle_entityref(self, name):
		try:
			c = {"lt": u"<", "gt": u">", "amp": u"&", "quot": u'"', "apos": u"'"}[name]
		except KeyError:
			name = self._makestring(name)
			try:
				self._cont_handler.skippedEntity(name)
			except errors.IllegalEntityError:
				try:
					entity = html.entity(name, xml=True)
				except errors.IllegalEntityError:
					self._cont_handler.characters(u"&%s;" % name)
				else:
					if issubclass(entity, xsc.CharRef):
						self._cont_handler.characters(unichr(entity.codepoint))
					else:
						self._cont_handler.characters(u"&%s;" % name)
		else:
			self._cont_handler.characters(c)
		self.headerJustRead = False

	def _string2Fragment(self, text):
		"""
		This version tries to pass illegal content literally.
		"""
		if text is None:
			return xsc.Null
		node = xsc.Frag()
		ct = self._cont_handler.createText
		while True:
			texts = text.split(u"&", 1)
			text = texts[0]
			if text:
				node.append(ct(text))
			if len(texts)==1:
				break
			texts = texts[1].split(u";", 1)
			name = texts[0]
			if len(texts)==1: # no ; found, so it's no entity => append it literally
				name = u"&" + name
				warnings.warn(errors.MalformedCharRefWarning(name))
				node.append(ct(name))
				break
			else:
				if name.startswith(u"#"): # character reference
					try:
						if name.startswith(u"#x"): # hexadecimal character reference
							node.append(ct(unichr(int(name[2:], 16))))
						else: # decimal character reference
							node.append(ct(unichr(int(name[1:]))))
					except (ValueError, OverflowError): # illegal format => append it literally
						name = u"&%s;" % name
						warnings.warn(errors.MalformedCharRefWarning(name))
						node.append(ct(name))
				else: # entity reference
					try:
						entity = {"lt": u"<", "gt": u">", "amp": u"&", "quot": u'"', "apos": u"'"}[name]
					except KeyError:
						try:
							entity = self._cont_handler.createEntity(name)
						except errors.IllegalEntityError:
							try:
								entity = html.entity(name, xml=True)
								if issubclass(entity, xsc.CharRef):
									entity = ct(unichr(entity.codepoint))
								else:
									entity = entity()
							except errors.IllegalEntityError:
								name = u"&%s;" % name
								warnings.warn(errors.MalformedCharRefWarning(name))
								entity = ct(name)
					else:
						entity = ct(entity)
					node.append(entity)
			text = texts[1]
		return node

	def handle_charref(self, data):
		data = self._makestring(data)
		try:
			if data.startswith("x"):
				data = unichr(int(data[1:], 16))
			else:
				data = unichr(int(data))
		except (ValueError, OverflowError):
			data = u"&#%s;" % data
		if not self.headerJustRead or not data.isspace():
			self._cont_handler.characters(data)
			self.headerJustRead = False

class HTMLParser(BadEntityParser):
	"""
	<par>A &sax;2 parser that can parse &html;.</par>
	"""

	def __init__(self, namespaceHandling=0, bufsize=2**16-20, encoding="iso-8859-1"):
		self._stack = []
		BadEntityParser.__init__(self, namespaceHandling, bufsize, encoding)

	def _whichparser(self):
		return sgmlop.SGMLParser()

	def reset(self):
		self._stack = []
		BadEntityParser.reset(self)

	def close(self):
		while self._stack: # close all open elements
			self.finish_endtag(self._stack[-1])
		BadEntityParser.close(self)

	def finish_starttag(self, name, attrs):
		name = name.lower()

		# guess omitted close tags
		while self._stack and self._stack[-1].upper() in htmldtd.HTML_OPT_END and name not in htmldtd.HTML_DTD.get(self._stack[-1], []):
			BadEntityParser.finish_endtag(self, self._stack[-1])
			del self._stack[-1]

		# Check whether this element is allowed in the current context
		if self._stack and name not in htmldtd.HTML_DTD.get(self._stack[-1], []):
			warnings.warn(errors.IllegalDTDChildWarning(name, self._stack[-1]))

		# Skip unknown attributes (but warn about them)
		newattrs = {}
		element = html.element(name, xml=True)
		for (attrname, attrvalue) in attrs:
			if attrname in ("xmlns", "procinstns", "entityns") or ":" in attrname or element.Attrs.isallowed(attrname.lower(), xml=True):
				newattrs[attrname.lower()] = attrvalue
			else:
				warnings.warn(errors.IllegalAttrError(element.Attrs, attrname.lower(), xml=True))
		BadEntityParser.finish_starttag(self, name, newattrs)

		if name.upper() in htmldtd.HTML_FORBIDDEN_END:
			# close tags immediately for which we won't get an end
			BadEntityParser.finish_endtag(self, name)
			return 0
		else:
			self._stack.append(name)
		return 1

	def finish_endtag(self, name):
		name = name.lower()
		if name.upper() in htmldtd.HTML_FORBIDDEN_END:
			# do nothing: we've already closed it
			return
		if name in self._stack:
			# close any open elements that were not closed explicitely
			while self._stack and self._stack[-1] != name:
				BadEntityParser.finish_endtag(self, self._stack[-1])
				del self._stack[-1]
			BadEntityParser.finish_endtag(self, name)
			del self._stack[-1]
		else:
			warnings.warn(errors.IllegalCloseTagWarning(name))

class ExpatParser(expatreader.ExpatParser):
	def reset(self):
		expatreader.ExpatParser.reset(self)
		self._parser.UseForeignDTD(True)

class Handler(object):
	"""
	contains the parser and the options and functions for handling XML files
	"""

	def __init__(self, parser=None, prefixes=None, loc=True):
		if parser is None:
			parser = SGMLOPParser()
		self.parser = parser

		if prefixes is None:
			prefixes = xsc.defaultPrefixes
		self.prefixes = prefixes

		self._locator = None
		self.loc = loc

	def parse(self, source):
		self.source = source
		self.base = getattr(self.source, "base", None)

		# register us for callbacks
		self.parser.setErrorHandler(self)
		self.parser.setContentHandler(self)
		self.parser.setDTDHandler(self)
		self.parser.setEntityResolver(self)

		# Configure the parser
		self.parser.setFeature(handler.feature_namespaces, False) # We do our own namespace processing
		self.parser.setFeature(handler.feature_external_ges, False) # Don't process external entities, but pass them to skippedEntity

		self.skippingWhitespace = False
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
			ns = xsc.Namespace.nsbyurl[unicode(attrvalue)][0]
			self.prefixes.startPrefixMapping(prefix, ns, "replace", type)
		node = self.createElement(name)
		for (attrname, attrvalue) in attrs.items():
			if attrname!="xmlns" and not attrname.startswith("xmlns:") and \
			   attrname!="procinstns" and not attrname.startswith("procinstns:") and \
			   attrname!="entityns" and not attrname.startswith("entityns:"):
				attrname = self.prefixes.attrnameFromQName(node, attrname)
				node[attrname] = attrvalue
				node[attrname].parsed(self)
		node.attrs.parsed(self)
		node.parsed(self, start=True)
		self.__appendNode(node)
		self.__nesting.append((node, prefixes)) # push new innermost element onto the stack, together with the list of prefix mappings defined by this node
		self.skippingWhitespace = False

	def endElement(self, name):
		currentelement = self.__nesting[-1][0]
		currentelement.parsed(self, start=False)
		element = self.createElement(name) # Unfortunately this creates the element a second time.
		if element.__class__ is not currentelement.__class__:
			raise errors.ElementNestingError(currentelement.__class__, element.__class__)
		if self.loc:
			self.__nesting[-1][0].endloc = self.getLocation()
		# SAX specifies that the order of calls to endPrefixMapping is undefined, so we use the same order as in startElement
		for (type, prefix) in self.__nesting[-1][1]:
			self.prefixes.endPrefixMapping(prefix, type)
		self.__nesting.pop() # pop the innermost element off the stack
		self.skippingWhitespace = False

	def characters(self, content):
		if self.skippingWhitespace:
			# the following could be content = content.lstrip(), but this would remove nbsps
			# FIXME use lstrip(???) with Python 2.3
			while content and content[0].isspace() and content[0] != u"\xa0":
				content = content[1:]
		if content:
			node = self.createText(content)
			node.parsed(self)
			last = self.__nesting[-1][0]
			if len(last) and isinstance(last[-1], xsc.Text):
				node = last[-1] + node.content # join consecutive Text nodes
				node.startloc = last[-1].startloc # make sure the replacement node has the original location
				last[-1] = node # replace it
			else:
				self.__appendNode(node)
			self.skippingWhitespace = False

	def comment(self, content):
		node = self.createComment(content)
		node.parsed(self)
		self.__appendNode(node)
		self.skippingWhitespace = False

	def processingInstruction(self, target, data):
		if target=="x":
			self.skippingWhitespace = True
		else:
			node = self.createProcInst(target, data)
			node.parsed(self)
			self.__appendNode(node)
			self.skippingWhitespace = False

	def skippedEntity(self, name):
		node = self.createEntity(name)
		if isinstance(node, xsc.CharRef):
			self.characters(unichr(node.codepoint))
		else:
			node.parsed(self)
			self.__appendNode(node)
		self.skippingWhitespace = False

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
		# This doesn't work properly with expat, as expat fiddles with the traceback
		raise self.__decorateException(exception)

	def fatalError(self, exception):
		"Handle a non-recoverable error."
		# This doesn't work properly with expat, as expat fiddles with the traceback
		raise self.__decorateException(exception)

	def warning(self, exception):
		"Handle a warning."
		print self.__decorateException(exception)

	def getLocation(self):
		return xsc.Location(self._locator)

	def __appendNode(self, node):
		if self.loc:
			node.startloc = self.getLocation()
		self.__nesting[-1][0].append(node) # add the new node to the content of the innermost element (or fragment)

	def createText(self, content):
		return xsc.Text(content)

	def createComment(self, content):
		return xsc.Comment(content)

	def createElement(self, name):
		return self.prefixes.element(name)()

	def createProcInst(self, target, data):
		return self.prefixes.procinst(target)(data)

	def createEntity(self, name):
		return self.prefixes.entity(name)()

def parse(source, handler=None, parser=None, prefixes=None):
	"""
	<par>Parse the source <arg>source</arg> (an <pyref module="ll.xist.sources" class="InputSource"><class>InputSource</class></pyref> instance)
	and return the resulting object tree.</par>

	<par><arg>handler</arg> is the handler to be used for the parser. It's the job
	of the handler to create the object tree from the &sax; events generated by
	the parser. If <arg>handler</arg> is not specified a new instance of
	<pyref class="Handler"><class>ll.xist.parsers.Handler</class></pyref> will be created
	and used.</par>

	<par><arg>parser</arg> is an instance of a &sax;2 compatible parser. &xist;
	itself provides several &sax;2 parsers
	(all based on Fredrik Lundh's <app>sgmlop</app> from <app moreinfo="http://pyxml.sf.net/">PyXML</app>):</par>
	<ulist>
	<item><pyref module="ll.xist.parsers" class="SGMLOPParser"><class>ll.xist.parsers.SGMLOPParser</class></pyref>
	(which is the default if the <arg>parser</arg> argument is not given);</item>
	<item><pyref module="ll.xist.parsers" class="BadEntityParser"><class>ll.xist.parsers.BadEntityParser</class></pyref>
	(which is based on <class>SGMLOPParser</class> and tries to pass on unknown entity references as literal content);</item>
	<item><pyref module="ll.xist.parsers" class="HTMLParser"><class>HTMLParser</class></pyref> (which is
	based on BadEntityParser and tries to make sense of &html; sources).</item>
	</ulist>

	<par><arg>prefixes</arg> is an instance of <pyref module="ll.xist.xsc" class="Prefixes"><class>ll.xist.xsc.Prefixes</class></pyref>
	specifies which namespace modules should be available during parsing
	and to which prefixes they are mapped (but of course this
	mapping can be changed during parsing by using <lit>xmlns</lit>
	attributes in the usual way).</par>
	"""
	if handler is None:
		handler = Handler(parser, prefixes=prefixes)
	handler.parse(source)
	result = handler.root
	handler.close()
	return result

def parseString(text, sysid="STRING", base=None, handler=None, parser=None, prefixes=None, encoding=None, tidy=False):
	return parse(sources.StringInputSource(text, sysid=sysid, base=base, encoding=encoding, tidy=tidy), handler=handler, parser=parser, prefixes=prefixes)

def parseURL(id, base=None, handler=None, parser=None, prefixes=None, encoding=None, tidy=False, headers=None, data=None):
	return parse(sources.URLInputSource(id, base=base, encoding=encoding, tidy=tidy, headers=headers, data=data), handler=handler, parser=parser, prefixes=prefixes)

def parseFile(filename, base=None, handler=None, parser=None, prefixes=None, encoding=None, tidy=False):
	return parseURL(url.Filename(filename), base=base, encoding=encoding, tidy=tidy, handler=handler, parser=parser, prefixes=prefixes)
