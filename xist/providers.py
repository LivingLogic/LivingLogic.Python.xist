#! /usr/bin/env python

## Copyright 2000 by Living Logic AG, Bayreuth, Germany.
## Copyright 2000 by Walter Dörwald
##
## See the file LICENSE for licensing details

"""
Contains classes for generating XSC trees from
XML files (or other data sources).
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import os
import types
import urllib

try:
	import sgmlop # for parsing XML files
except ImportError:
	from xml.parsers import sgmlop # get it from the XML package

import errors
import options
import xsc
import url

providers = [] # provider stack

def getURL():
	if len(providers):
		return providers[-1].filenames[-1]
	else:
		return url.URL("*/")

class Provider(xsc.NestedNamespace):
	"""
	contains the parser and the options and functions for handling XML files
	"""

	def __init__(self):
		xsc.NestedNamespace.__init__(self)

	def finish_starttag(self, name, attrs):
		node = self.elementFromName(unicode(name, self.encoding))()
		for name in attrs.keys():
			node[name] = self.__string2Fragment(attrs[name])
		self.__appendNode(node)
		self.__nesting.append(node) # push new innermost element onto the stack

	def finish_endtag(self, name):
		element = self.elementFromName(unicode(name, self.encoding))
		currentelement = self.__nesting[-1].__class__
		if element != currentelement:
			raise errors.IllegalElementNestingError(self.__here(), currentelement, element)
		self.__nesting[-1].endloc = self.__here()
		self.__nesting.pop() # pop the innermost element off the stack

	def handle_data(self, data):
		if data != "":
			self.__appendNode(xsc.Text(unicode(data, self.encoding)))

	def handle_comment(self, data):
		self.__appendNode(xsc.Comment(unicode(data, self.encoding)))

	def handle_special(self, data):
		if data[:7] == "DOCTYPE":
			self.__appendNode(xsc.DocType(unicode(data, self.encoding)[8:]))

	def handle_proc(self, target, data):
		self.__appendNode(self.procInstFromName(unicode(target, self.encoding))(unicode(data, self.encoding)))

	def handle_entityref(self, name):
		self.__appendNode(self.entityFromName(unicode(name, self.encoding))())

	def handle_charref(self, name):
		try:
			if name[0] == 'x':
				code = int(name[1:], 16)
			else:
				code = int(name)
		except ValueError:
			raise errors.MalformedCharRefError(self.__here(), name)

		self.__appendNode(xsc.Text(unichr(code)))

	def parseLines(self, lines):
		self.__nesting = [xsc.Frag()]
		parser = sgmlop.XMLParser()
		parser.register(self)
		self.lineno = 1
		for line in lines:
			parser.feed(line)
			self.lineno += 1
		parser.close()
		# our nodes do not have a parent link, therefore we have to store the active
		# path through the tree in a stack (which we call nesting, because stack is
		# already used by the base class (there is no base class anymore, but who cares))

		# after we've finished parsing, the Frag that we put at the bottom of the stack will be our document root
		return self.__nesting[0]

	def isRetrieve(self, url):
		remote = url.isRemote()
		if (options.retrieveremote and remote) or (options.retrievelocal and (not remote)):
			return 1
		else:
			return 0

	def getLocation(self):
		return xsc.Location(self.filenames[-1], self.lineno)

	def __appendNode(self, node):
		node.startloc = self.__here()
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
							node.append(self.entityFromName(text[1:i])())
						except KeyError:
							raise errors.UnknownEntityError(self.__here(), text[1:i])
					text = text[i+1:]
				except ValueError:
					raise errors.MalformedCharRefError(self.__here(), text)
			except ValueError:
				if len(text):
					node.append(text)
				break
		return node

class URIProvider(Provider):
	def parse(self, url):
		"""
		Reads and parses a XML file from an URL and returns the resulting XSC
		"""
		try:
			self.pushURL(url)
			lines = self.filenames[-1].readlines()
			element = self.parseLines(lines)
		finally:
			self.popURL()
		return element

class StringProvider(Provider):
	def parse(self, text):
		"""
		Parses a string and returns the resulting XSC
		"""
		self.pushURL("STRING")
		lines = [ line+"\n" for line in text.split("\n") ]
		element = self.parseLines(lines)
		self.popURL()
		return element

class TidyURIProvider(Provider):
	def parse(self, url):
		self.pushURL(url)
		url = self.filenames[-1]
		try:
			(tidyin, tidyout, tidyerr) = os.popen3("tidy --tidy-mark no --wrap 0 --output-xhtml --numeric-entities yes --show-warnings no --quiet yes -asxml -quiet", "b") # open the pipe to and from tidy
			tidyin.write(url.open().read()) # get the desired file from the url and pipe it to tidy
			tidyin.close() # tell tidy, that we're finished
			lines = tidyout.readlines() # read the output
			tidyout.close()
			tidyerr.close()
			element = self.parseLines(lines)
			return element
		finally:
			urllib.urlcleanup() # throw away the temporary filename
			self.popURL()

class XSC(URIProvider, StringProvider):
	def parseString(self, text):
		return StringProvider.parse(self, text)

