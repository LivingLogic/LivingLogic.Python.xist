#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
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

import sys, os, os.path, warnings, cStringIO

from xml import sax
from xml.parsers import sgmlop
from xml.sax import expatreader
from xml.sax import saxlib
from xml.sax import handler
from xml.dom import html as htmldtd

from ll import url

import xsc, errors, utils, cssparsers
from ns import html


class SGMLOPParser(sax.xmlreader.XMLReader, sax.xmlreader.Locator):
	"""
	This is a rudimentary, buggy, halfworking, untested SAX2 drivers for sgmlop that
	only works in the context of &xist;. And I didn't even know, what I was doing.
	"""
	_whichparser = sgmlop.XMLParser

	def __init__(self, bufsize=8000):
		sax.xmlreader.XMLReader.__init__(self)
		self.encoding = None
		self._parser = None
		self._bufsize = bufsize

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
			self._cont_handler.endDocument()
			self._parser.close()
			self._parser.register(None)
			self._parser = None

	def parse(self, source):
		self.source = source
		stream = source.getByteStream()
		encoding = source.getEncoding()
		if encoding is None:
			encoding = "utf-8"
		self.encoding = encoding
		self._cont_handler.setDocumentLocator(self)
		self._cont_handler.startDocument()
		self.lineNumber = 1
		# we don't keep a column number, because otherwise parsing would be much to slow
		self.headerJustRead = False # will be used for skipping whitespace after the XML header

		parsed = False
		try:
			while True:
				data = stream.read(self._bufsize)
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
			self.close()
			self.source = None
			self.encoding = None
			raise
		except KeyboardInterrupt:
			self.close()
			self.source = None
			self.encoding = None
			raise
		except Exception, exc:
			try:
				self.close()
			except SystemExit:
				raise
			except KeyboardInterrupt:
				raise
			except Exception, exc2:
				self.source = None
				self.encoding = None
			errhandler = self.getErrorHandler()
			if errhandler is not None:
				errhandler.fatalError(exc)
			else:
				raise
		self.close()
		self.source = None
		self.encoding = None

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
			return sax.xmlreader.IncrementalParser.setFeature(self, name)

	def handle_comment(self, data):
		self.getContentHandler().comment(self._makestring(data))
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
			self.getContentHandler().characters(data)
			self.headerJustRead = False

	def handle_data(self, data):
		data = self._makestring(data)
		if not self.headerJustRead or not data.isspace():
			self.getContentHandler().characters(data)
			self.headerJustRead = False

	def handle_proc(self, target, data):
		target = self._makestring(target)
		data = self._makestring(data)
		if target != u'xml': # Don't report <?xml?> as a processing instruction
			self.getContentHandler().processingInstruction(target, data)
			self.headerJustRead = False
		else: # extract the encoding
			encoding = utils.findattr(data, u"encoding")
			if encoding is not None:
				self.encoding = encoding
			self.headerJustRead = True

	def handle_entityref(self, name):
		try:
			c = {"lt": u"<", "gt": u">", "amp": u"&", "quot": u'"', "apos": u"'"}[name]
		except KeyError:
			self.getContentHandler().skippedEntity(self._makestring(name))
		else:
			self.getContentHandler().characters(c)
		self.headerJustRead = False

	def finish_starttag(self, name, attrs):
		newattrs = sax.xmlreader.AttributesImpl({})
		for (attrname, attrvalue) in attrs.items():
			if attrvalue is None:
				attrvalue = attrname
			else:
				attrvalue = self._string2fragment(self._makestring(attrvalue))
			newattrs._attrs[self._makestring(attrname)] = attrvalue
		self.getContentHandler().startElement(self._makestring(name), newattrs)
		self.headerJustRead = False

	def finish_endtag(self, name):
		self.getContentHandler().endElement(self._makestring(name))
		self.headerJustRead = False

	def _string2fragment(self, text):
		"""
		parses a string that might contain entities into a fragment
		with text nodes, entities and character references.
		"""
		if text is None:
			return xsc.Null
		ct = self.getContentHandler().createText
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
					node.append(self.getContentHandler().createEntity(name))
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
				self.getContentHandler().skippedEntity(name)
			except errors.IllegalEntityError:
				try:
					entity = html.entity(name, xml=True)
				except errors.IllegalEntityError:
					self.getContentHandler().characters(u"&%s;" % name)
				else:
					if issubclass(entity, xsc.CharRef):
						self.getContentHandler().characters(unichr(entity.codepoint))
					else:
						self.getContentHandler().characters(u"&%s;" % name)
		else:
			self.getContentHandler().characters(c)
		self.headerJustRead = False

	def _string2fragment(self, text):
		"""
		This version tries to pass illegal content literally.
		"""
		if text is None:
			return xsc.Null
		node = xsc.Frag()
		ct = self.getContentHandler().createText
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
							entity = self.getContentHandler().createEntity(name)
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
			self.getContentHandler().characters(data)
			self.headerJustRead = False


class HTMLParser(BadEntityParser):
	"""
	<par>A &sax;2 parser that can parse &html;.</par>
	"""

	_whichparser = sgmlop.SGMLParser

	def __init__(self, bufsize=2**16-20):
		BadEntityParser.__init__(self, bufsize)
		self._stack = []

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
			if attrname=="xmlns" or ":" in attrname or element.Attrs.isallowed(attrname.lower(), xml=True):
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


class Parser(object):
	"""
	<par>It is the job of a <class>Parser</class> to create the object tree from the
	&sax; events generated by the underlying &sax; parser.</par>
	"""

	def __init__(self, saxparser=SGMLOPParser, nspool=None, prefixes=None, tidy=False, loc=True, validate=True, encoding="utf-8"):
		"""
		<par>Create a new <class>Parser</class> instance.</par>

		<par>Arguments have the following meaning:</par>
		<dlist>
		<term><arg>saxparser</arg></term><item><par>a callable that returns an instance of a &sax;2 compatible parser.
		&xist; itself provides several &sax;2 parsers
		(all based on Fredrik Lundh's <app>sgmlop</app> from <app moreinfo="http://pyxml.sf.net/">PyXML</app>):</par>
		<ulist>
		<item><pyref module="ll.xist.parsers" class="SGMLOPParser"><class>ll.xist.parsers.SGMLOPParser</class></pyref>
		(which is the default if the <arg>parser</arg> argument is not given);</item>
		<item><pyref module="ll.xist.parsers" class="BadEntityParser"><class>ll.xist.parsers.BadEntityParser</class></pyref>
		(which is based on <class>SGMLOPParser</class> and tries to pass on unknown entity references as literal content);</item>
		<item><pyref module="ll.xist.parsers" class="HTMLParser"><class>HTMLParser</class></pyref> (which is
		based on BadEntityParser and tries to make sense of &html; sources).</item>
		</ulist>
		</item>
	
		<term><arg>nspool</arg></term><item>an instance of <pyref module="ll.xist.xsc" class="NSPool"><class>ll.xist.xsc.NSPool</class></pyref>;
		From this namespace pool namespaces will be taken when the parser
		encounters <lit>xmlns</lit> attributes.</item>

		<term><arg>prefixes</arg></term><item>an instance of <pyref module="ll.xist.xsc" class="Prefixes"><class>ll.xist.xsc.Prefixes</class></pyref>;
		Specifies which namespace modules should be available during parsing
		and to which prefixes they are mapped (but of course this
		mapping can be changed during parsing by using <lit>xmlns</lit>
		attributes in the usual way).</item>

		<term><arg>loc</arg></term><item>Should location information be attached to the generated nodes?</item>

		<term><arg>validate</arg></term><item>Should the parsed &xml; nodes be validated after parsing?</item>

		<term><arg>encoding</arg></term><item>The default encoding to use, when to source doesn't provide an &xml; header.</item>
		</dlist>
		"""
		self.saxparser = saxparser

		if nspool is None:
			nspool = xsc.defaultnspool
		self.nspool = nspool

		if prefixes is None:
			prefixes = xsc.defaultPrefixes.clone()
		self.prefixes = prefixes # the currently active prefix mapping (will be replaced once xmlns attributes are encountered)

		self._locator = None
		self.tidy = tidy
		self.loc = loc
		self.validate = validate
		self.encoding = encoding

	def _last(self):
		"""
		return the newest node from the stack that is a real node.
		(There might be false node on the stack, because we are inside
		of illegal elements).
		"""
		for (node, prefixes) in reversed(self._nesting):
			if node is not None:
				return node

	def _parseHTML(self, stream, base, sysid, encoding):
		import libxml2 # This requires libxml2 (see http://www.xmlsoft.org/)

		def decode(s):
			try:
				return s.decode("utf-8")
			except UnicodeDecodeError:
				return s.decode("iso-8859-1")

		data = stream.read()
		doc = libxml2.htmlReadMemory(data, len(data), sysid, encoding, 0x60)
		ns = self.nspool.get(html.xmlname, html)
		def toxsc(node):
			if node.type == "document_html":
				newnode = xsc.Frag()
				child = node.children
				while child is not None:
					newnode.append(toxsc(child))
					child = child.next
			elif node.type == "element":
				name = decode(node.name).lower()
				try:
					newnode = ns.element(name, xml=True)()
				except errors.IllegalElementError:
					newnode = xsc.Frag()
				else:
					attr = node.properties
					while attr is not None:
						name = decode(attr.name).lower()
						if attr.content is None:
							content = u""
						else:
							content = decode(attr.content)
						try:
							attrnode = newnode.attrs.set(name, content, xml=True)
						except errors.IllegalAttrError:
							pass
						else:
							attrnode.parsed(self)
						attr = attr.next
					newnode.attrs.parsed(self)
					newnode.parsed(self, start=True)
				child = node.children
				while child is not None:
					newnode.append(toxsc(child))
					child = child.next
				if isinstance(node, xsc.Element): # if we did recognize the element, otherwise we're in a Frag
					newnode.parsed(self, start=False)
			elif node.type in ("text", "cdata"):
				newnode = xsc.Text(decode(node.content))
			elif node.type == "comment":
				newnode = xsc.Comment(decode(node.content))
			else:
				newnode = xsc.Null
			newnode.startloc = xsc.Location(sysid=sysid) # FIXME: get line from node.lineNo()
			return newnode
		node = toxsc(doc)
		doc.freeDoc()
		return node

	def _parse(self, stream, base, sysid, encoding):
		self.base = url.URL(base)

		parser = self.saxparser()
		# register us for callbacks
		parser.setErrorHandler(self)
		parser.setContentHandler(self)
		parser.setDTDHandler(self)
		parser.setEntityResolver(self)

		# Configure the parser
		parser.setFeature(handler.feature_namespaces, False) # We do our own namespace processing
		parser.setFeature(handler.feature_external_ges, False) # Don't process external entities, but pass them to skippedEntity

		self.skippingwhitespace = False

		if self.tidy:
			return self._parseHTML(stream, base, sysid, encoding)

		source = sax.xmlreader.InputSource(sysid)
		source.setByteStream(stream)
		source.setEncoding(encoding)

		# XIST nodes do not have a parent link, therefore we have to store the
		# active path through the tree in a stack (which we call _nesting)
		# together with the namespace prefixes defined by each element.
		#
		# After we've finished parsing, the Frag that we put at the bottom of the
		# stack will be our document root.
		#
		# The parser provides the ability to skip illegal elements, attributes,
		# processing instructions or entity references, but for illegal elements,
		# it must still record the new namespaces defined by the illegal element
		# in this case None is stored in the stack instead of the element node.

		self._nesting = [ (xsc.Frag(), self.prefixes) ]
		try:
			parser.parse(source)
			root = self._nesting[0][0]
		finally:
			self._nesting = None
		return root

	def parse(self, stream, base=None, sysid=None):
		if sysid is None:
			sysid = base
		return self._parse(stream, base, self.encoding)

	def parseString(self, string, base=None, sysid=None):
		if isinstance(string, unicode):
			encoding = "utf-8"
			string = string.encode(encoding)
		else:
			encoding = self.encoding
		stream = cStringIO.StringIO(string)
		if base is None:
			base = url.URL("root:STRING")
		if sysid is None:
			sysid = str(base)
		return self._parse(stream, base, sysid, encoding)

	def parseURL(self, name, base=None, sysid=None, headers=None, data=None):
		name = url.URL(name)
		stream = name.openread(headers=headers, data=data)
		if base is None:
			base = stream.finalurl
		if sysid is None:
			sysid = str(base)
		return self._parse(stream, base, sysid, self.encoding)

	def parseFile(self, name, base=None, sysid=None):
		name = os.path.expanduser(name)
		stream = open(name, "r")
		if base is None:
			base = url.File(name)
		if sysid is None:
			sysid = str(base)
		return self._parse(stream, base, sysid, self.encoding)

	def setDocumentLocator(self, locator):
		self._locator = locator

	def startDocument(self):
		pass

	def endDocument(self):
		pass

	def startElement(self, name, attrs):
		newprefixes = {}
		for (attrname, attrvalue) in attrs.items():
			if attrname==u"xmlns" or attrname.startswith(u"xmlns:"):
				ns = self.nspool[unicode(attrvalue)]
				newprefixes[attrname[6:] or None] = [ns]

		prefixes = self.prefixes
		if newprefixes:
			prefixes = prefixes.clone()
			prefixes.update(newprefixes)
			self.prefixes = prefixes
		node = self.createElement(name)
		if node is not None:
			for (attrname, attrvalue) in attrs.items():
				if attrname != u"xmlns" and not attrname.startswith(u"xmlns:"):
					attrname = prefixes.attrnamefromqname(node, attrname)
					if attrname is not None: # None means an illegal attribute
						node[attrname] = attrvalue
						node[attrname].parsed(self)
			node.attrs.parsed(self)
			node.parsed(self, start=True)
			self.__appendNode(node)
		# push new innermost element onto the stack, together with the list of prefix mappings defined by this node
		# If the element is bad (i.e. createElement returned None), we push None as the node
		self._nesting.append((node, prefixes))
		self.skippingwhitespace = False

	def endElement(self, name):
		currentelement = self._last()
		if currentelement is not None: # we're not in an bad element
			currentelement.parsed(self, start=False)
			if self.validate:
				currentelement.checkvalid()
			if self.loc:
				currentelement.endloc = self.getLocation()
		self.prefixes = self._nesting.pop()[1] # pop the innermost element off the stack and restore the old prefixes mapping

		# We have to check after the old prefix mapping from this element has been dropped
		element = self.createElement(name) # Unfortunately this creates the element a second time.
		if element is not None and element.__class__ is not currentelement.__class__:
			raise errors.ElementNestingError(currentelement.__class__, element.__class__)
		self.skippingwhitespace = False

	def characters(self, content):
		if self.skippingwhitespace:
			# the following could be content = content.lstrip(), but this would remove nbsps
			while content and content[0].isspace() and content[0] != u"\xa0":
				content = content[1:]
		if content:
			node = self.createText(content)
			node.parsed(self)
			last = self._last()
			if len(last) and isinstance(last[-1], xsc.Text):
				node = last[-1] + node.content # join consecutive Text nodes
				node.startloc = last[-1].startloc # make sure the replacement node has the original location
				last[-1] = node # replace it
			else:
				self.__appendNode(node)
			self.skippingwhitespace = False

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
			if node is not None:
				node.parsed(self)
				self.__appendNode(node)
			self.skippingWhitespace = False

	def skippedEntity(self, name):
		node = self.createEntity(name)
		if node is not None:
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
		self._last().append(node) # add the new node to the content of the innermost element (or fragment)

	def createText(self, content):
		return xsc.Text(content)

	def createComment(self, content):
		return xsc.Comment(content)

	def createElement(self, name):
		element = self.prefixes.element(name)
		if element is not None: # None means that the element should be ignored
			element = element()
		return element

	def createProcInst(self, target, data):
		procinst = self.prefixes.procinst(target)
		if procinst is not None: # None means that the procinst should be ignored
			procinst = procinst(data)
		return procinst

	def createEntity(self, name):
		entity = self.prefixes.entity(name)
		if entity is not None: # None means that the entity should be ignored
			entity = entity()
		return entity


def parse(stream, base, sysid=None, **parserargs):
	parser = Parser(**parserargs)
	return parser.parse(stream, base, sysid)


def parseString(text, base=None, sysid=None, **parserargs):
	parser = Parser(**parserargs)
	return parser.parseString(text, base, sysid)


def parseURL(url, base=None, sysid=None, headers=None, data=None, **parserargs):
	parser = Parser(**parserargs)
	return parser.parseURL(url, base, sysid, headers, data)


def parseFile(filename, base=None, sysid=None, **parserargs):
	parser = Parser(**parserargs)
	return parser.parseFile(filename, base, sysid)
