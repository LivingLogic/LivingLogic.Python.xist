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
This file contains everything you need to parse XIST DOMs from files, strings, URLs etc.

It contains different SAX2 parser driver classes. (In fact in contains one one, the
sgmlop driver, everything else is from PyXML) and various classes derived from
xml.sax.xmlreader.InputSource.
"""

import types
import cStringIO as StringIO
import urllib

from xml import sax
from xml.parsers import sgmlop
from xml.sax import expatreader

#try:
#	import timeoutsocket
#except ImportError:
timeoutsocket = None

class StringInputSource(sax.xmlreader.InputSource):
	def __init__(self, text):
		sax.xmlreader.InputSource.__init__(self)
		self.setSystemId("STRING")
		if type(text) is types.UnicodeType:
			encoding = "utf-8"
			text = text.encode(encodig)
		else:
			encoding = sys.getdefaultencoding()
		self.setByteStream(StringIO.StringIO(text))
		self.setEncoding(encoding)

class FileInputSource(sax.xmlreader.InputSource):
	def __init__(self, filename):
		sax.xmlreader.InputSource.__init__(self)
		self.setSystemId(filename)
		self.setByteStream(open(file, "r"))

class URLInputSource(sax.xmlreader.InputSource):
	def __init__(self, url):
		sax.xmlreader.InputSource.__init__(self)
		self.setSystemId(url)
		self.setByteStream(urllib.urlopen(url))

	def setTimeout(self, secs):
		if timeoutsocket is not None:
			timeoutsocket.setDefaultSocketTimeout(sec)

	def getTimeout(self):
		if timeoutsocket is not None:
			timeoutsocket.getDefaultSocketTimeout()


class TidyURLInputSource(sax.xmlreader.InputSource):
	def __init__(self, url):
		sax.xmlreader.InputSource.__init__(self)
		self.tidyin = None
		self.tidyout = None
		self.tidyerr = None
		self.setSystemId(url)
		try:
			(self.tidyin, self.tidyout, self.tidyerr) = os.popen3("tidy --tidy-mark no --wrap 0 --output-xhtml --numeric-entities yes --show-warnings no --quiet yes -asxml -quiet", "b") # open the pipe to and from tidy
			self.tidyin.write(urllib.urlopen().read()) # get the desired file from the url and pipe it to tidy
			self.tidyin.close() # tell tidy, that we're finished
			self.tidyin = None
			self.setByteStream(tidyout)
		except:
			if self.tidyin is not None:
				self.tidyin.close()
			if self.tidyout is not None:
				self.tidyout.close()
			if self.tidyerr is not None:
				self.tidyerr.close()
			urllib.urlcleanup() # throw away the temporary filename

	def __del__(self):
		if self.tidyin is not None:
			self.tidyin.close()
		if self.tidyout is not None:
			self.tidyout.close()
		if self.tidyerr is not None:
			self.tidyerr.close()
		urllib.urlcleanup()

class SGMLOPParser(sax.xmlreader.IncrementalParser, sax.xmlreader.Locator):
	"""
	This is a rudimentary, buggy, halfworking, untested SAX2 drivers for sgmlop.
	And I didn't even know, what I was doing, but it seems to work.
	"""
	encoding = "latin-1"

	def __init__(self, naespaceHandling=0, bufsize=2**16-20):
		sax.xmlreader.IncrementalParser.__init__(self, bufsize)
		self.reset()

	def setErrorHandler(self, handler):
		self.parser.register(self)
		self.error_handler = handler

	def setContentHandler(self, handler):
		self.parser.register(self)
		self.content_handler = handler

	def setDTDHandler(self, handler):
		self.parser.register(self)
		self.dtd_handler = handler

	def setEntityResolver(self, handler):
		self.parser.register(self)
		self.entity_resolver = handler

	def parse(self, source):
		file = source.getByteStream()
		self._parsing = 1
		self.content_handler.startDocument()
		parser = self.parser

		while 1:
			data = file.read(self.bufsize)
			if not data:
				break
			parser.feed(data)

		self.close()

	def handle_cdata(self, data):
		self.content_handler.characters(data)

	def handle_data(self, data):
		self.content_handler.characters(data)

	def handle_proc(self, target, data):
		if target!='xml': # Don't report <?xml?> as a processing instruction
			self.content_handler.processingInstruction(unicode(target, self.encoding), unicode(data, self.encoding))

	def handle_charref(self, charno):
		self.content_handler.characters(unichr(charno))

	def handle_entityref(self, name):
		if hasattr(self.content_handler, "entity"):
			self.content_handler.entity(unicode(name, self.encoding))

	def finish_starttag(self, name, attrs):
		newattrs = sax.xmlreader.AttributesImpl(attrs)
		for (attrname, attrvalue) in attrs.items():
			newattrs._attrs[unicode(attrname, self.encoding)] = unicode(attrvalue, self.encoding)
		self.content_handler.startElement(unicode(name, self.encoding), newattrs)

	def finish_endtag(self,name):
		self.content_handler.endElement(unicode(name, self.encoding))

	def reset(self):
		self.parser=sgmlop.XMLParser()
		self._parsing = 0

	def feed(self, data):
		if not self._parsing:
			self.content_handler.startDocument()
			self._parsing = 1
		self.parser.feed(data)

	def close(self):
		self.parser.close()
		self.content_handler.endDocument()

ExpatParser = expatreader.ExpatParser

class Handler:
	"""
	contains the parser and the options and functions for handling XML files
	"""

	def __init__(self, parser=None, namespaces=None):
		if parser is None:
			parser = parsers.SGMLOPParser()
		self.parser = parser

		if namespaces is None:
			namespaces = xsc.defaultNamespaces
		self.namespaces = namespaces

		self.server = "localhost"
		self.filenames = [url.URL("*/")]

	def pushURL(self, u):
		u = url.URL(u)
		if len(self.filenames):
			u = self.filenames[-1] + u
		self.filenames.append(u)

	def popURL(self):
		self.filenames.pop()

	def startDocument(self):
		self.__nesting = [ xsc.Frag() ]
		self.lineno = 1

	def endDocument(self):
		pass

	def startElement(self, name, attrs):
		node = self.namespaces.elementFromName(name)()
		for name in attrs.keys():
			node[name] = self.__string2Fragment(attrs[name])
		self.__appendNode(node)
		self.__nesting.append(node) # push new innermost element onto the stack

	def endElement(self, name):
		element = self.namespaces.elementFromName(name)
		currentelement = self.__nesting[-1].__class__
		if element != currentelement:
			raise errors.IllegalElementNestingError(self.getLocation(), currentelement, element)
		self.__nesting[-1].endloc = self.getLocation()
		self.__nesting.pop() # pop the innermost element off the stack

	def characters(self, content):
		if content != "":
			self.__appendNode(xsc.Text(content))

	def comment(self, content):
		self.__appendNode(xsc.Comment(content))

	def processsingInstruction(self, target, data):
		self.__appendNode(self.namespaces.procInstFromName(target)(data))

	def entity(self, name):
		self.__appendNode(self.namespaces.entityFromName(name)())

	def handle_charref(self, name):
		try:
			if name[0] == 'x':
				code = int(name[1:], 16)
			else:
				code = int(name)
		except ValueError:
			raise errors.MalformedCharRefError(self.getLocation(), name)
		self.__appendNode(xsc.Text(unichr(code)))

	def isRetrieve(self, url):
		remote = url.isRemote()
		if (options.retrieveremote and remote) or (options.retrievelocal and (not remote)):
			return 1
		else:
			return 0

	def getLocation(self):
		return xsc.Location(self.filenames[-1], self.lineno)

	def __appendNode(self, node):
		node.startloc = self.getLocation()
		last = self.__nesting[-1]
		if len(last) and isinstance(last[-1], xsc.Text):
			if isinstance(node, xsc.Text):
				last[-1] += node
				return
		last.append(node) # add the new node to the content of the innermost element (or fragment)

	def __string2Fragment(self, text):
		"""
		parses a string that might contain entities into a fragment
		with text nodes and character references (and other stuff,
		if the string contains entities).
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
							node.append(xsc.Text(unichr(int(text[3:i], 16))))
						else:
							node.append(xsc.Text(unichr(int(text[2:i]))))
					else:
						try:
							node.append(self.namespaces.entityFromName(text[1:i])())
						except KeyError:
							raise errors.UnknownEntityError(self.getLocation(), text[1:i])
					text = text[i+1:]
				except ValueError:
					raise errors.MalformedCharRefError(self.getLocation(), text)
			except ValueError:
				if len(text):
					node.append(text)
				break
		return node

def parse(inputsource, namespaces=None, parser=None)
	handler = Handler(parser, namespaces)
	try:
		self.pushURL(url)

		# our nodes do not have a parent link, therefore we have to store the active
		# path through the tree in a stack (which we call nesting, because stack is
		# already used by the base class (there is no base class anymore, but who cares))

		# after we've finished parsing, the Frag that we put at the bottom of the stack will be our document root
		parser = self.parser()
		parser.setErrorHandler(self)
		parser.setContentHandler(self)
		parser.setDTDHandler(self)
		parser.setEntityResolver(self)
		parser.parse(inputsource)
		root = self.__nesting[0]
	finally:
		self.popURL()
	return root
