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
Contains classes for generating XSC trees from
XML files (or other data sources).
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import os
import types
import urllib

import errors
import options
import xsc
import url

import inputsources
import parsers

providers = [] # provider stack

def getURL():
	if len(providers):
		return providers[-1].filenames[-1]
	else:
		return url.URL("*/")

class Provider:
	"""
	contains the parser and the options and functions for handling XML files
	"""

	def __init__(self, parser=None, namespaces=None, encoding=None):
		if parser is None:
			parser = parsers.SGMLOPParser
		self.parser = parser

		if namespaces is None:
			namespaces = xsc.defaultNamespaces
		self.namespaces = namespaces

		if encoding is None:
			encoding = "iso-8859-1" # We assume that all source code is in this encoding
		self.encoding = encoding

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

