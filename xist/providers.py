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

class NestedNamespace:
	def __init__(self, parent=None):
		self.server = "localhost"
		if parent is None:
			self.filenames = [url.URL("*/")]
			self.namespaces = [xsc.namespace]
		else:
			self.filenames = [ parent.filenames[-1] ]
			self.namespaces = parent.namespaces[:]

	def pushURL(self, u):
		u = url.URL(u)
		if len(self.filenames):
			u = self.filenames[-1] + u
		self.filenames.append(u)

	def popURL(self):
		self.filenames.pop()

	def pushNamespace(self, *namespaces):
		for namespace in namespaces:
			if type(namespace) is types.ModuleType:
				namespace = namespace.namespace
			self.namespaces.insert(0, namespace) # built in reverse order, so a simple "for in" finds the most recent entry.

	def popNamespace(self, count):
		del self.namespaces[:count]

	def __nodeFromName(self, name, type):
		# type==0 => element; type==1 => entity; type==2 => procinst
		name = name.split(":")
		if len(name) == 1: # no namespace specified
			name.insert(0, None)
		# search for the element
		# first search the namespace stack (i.e. namespaces that are registered via the normal XML namespace mechanism)
		# if the element can't be found, search all existing namespaces.
		allnamespaces = self.namespaces+xsc.namespaceRegistry.byPrefix.values()
		for namespace in allnamespaces:
			if name[0] is None or name[0] == namespace.prefix:
				try:
					if type==0:
						return namespace.elementsByName[name[1]]
					elif type==1:
						return namespace.entitiesByName[name[1]]
					else: # if type==2:
						return namespace.procInstsByName[name[1]]
				except KeyError: # no element/entity in this namespace with this name
					pass
		if type==0:
			raise errors.IllegalElementError(self.getLocation(), name) # elements with this name couldn't be found
		elif type==1:
			raise errors.IllegalEntityError(self.getLocation(), name) # entities with this name couldn't be found
		else: # if type==2:
			raise errors.IllegalProcInstError(self.getLocation(), name) # procinsts with this name couldn't be found

	def elementFromName(self, name):
		"""
		returns the element class for the name name (which might include a namespace).
		"""
		return self.__nodeFromName(name, 0)

	def entityFromName(self, name):
		"""
		returns the entity class for the name name (which might include a namespace).
		"""
		return self.__nodeFromName(name, 1)

	def procInstFromName(self, name):
		"""
		returns the processing instruction class for the name name (which might include a namespace).
		"""
		return self.__nodeFromName(name, 2)

	def getLocation(self):
		return None

class Provider(NestedNamespace):
	"""
	contains the parser and the options and functions for handling XML files
	"""

	def __init__(self, encoding=None):
		NestedNamespace.__init__(self)
		if encoding is None:
			encoding = "iso-8859-1" # We assume that all source code is in this encoding
		self.encoding = encoding

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
			raise errors.IllegalElementNestingError(self.getLocation(), currentelement, element)
		self.__nesting[-1].endloc = self.getLocation()
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
			raise errors.MalformedCharRefError(self.getLocation(), name)

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
							node.append(self.entityFromName(text[1:i])())
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

