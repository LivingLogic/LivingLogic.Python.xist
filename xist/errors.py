#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of Living Logic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVING LOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVING LOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
This module contains all the exception classes of XSC.
But note that XSC does raise other exceptions as well.

All exceptions defined in this module are derived from
the base class Error.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import xsc
import exceptions
import types

class Error(Exception):
	"""
	base class for all XSC exceptions
	"""

	def __init__(self, location = None):
		self.location = location

	def __str__(self):
		s = str(self.location)
		if s:
			s = s + ": "
		return s

class EmptyElementWithContentError(Error):
	"""
	exception that is raised, when an element has content,
	but it shouldn't (i.e. empty==1)
	"""

	def __init__(self, element):
		Error.__init__(self, element.startloc)
		self.element = element

	def __str__(self):
		return Error.__str__(self) + "element " + self.element._str() + " specified to be empty, but has content"

class IllegalAttrError(Error):
	"""
	exception that is raised, when an element has an illegal attribute
	(i.e. one that isn't contained in it's attrHandlers)
	"""

	def __init__(self, element, attr):
		Error.__init__(self)
		self.element = element
		self.attr = attr

	def __str__(self):
		attrs = self.element.attrHandlers.keys()
		s = Error.__str__(self) + "Attribute " + xsc.strAttrName(self.attr) + " not allowed in element " + xsc._strNode(self.element.__class__) + ". "
		if len(attrs):
			attrs.sort()
			attrs = ", ".join(map(xsc.strAttrName, attrs))
			s = s + "Allowed attributes are: " + attrs + "."
		else:
			s = s + "No attributes allowed."
		return s

class AttributeNotFoundError(Error):
	"""
	exception that is raised, when an attribute is fetched that isn't there
	"""

	def __init__(self, element, attr):
		Error.__init__(self)
		self.element = element
		self.attr = attr

	def __str__(self):
		attrs = self.element.attrs.keys()

		s = Error.__str__(self) + "Attribute " + xsc.strAttrName(self.attr) + " not found in element " + xsc._strNode(self.element.__class__) +". "

		if len(attrs):
			attrs.sort()
			attrs = ", ".join(map(xsc.strAttrName, attrs))
			s = s + "Available attributes are: " + attrs + "."
		else:
			s = s + "No attributes available."

		return s

class IllegalElementError(Error):
	"""
	exception that is raised, when an illegal element is encountered
	(i.e. one that isn't registered via xsc.Namespace.register())
	"""

	def __init__(self, location, name):
		Error.__init__(self, location)
		self.name = name

	def __str__(self):
		# List the element sorted by name
		all = {}
		for namespace in xsc.namespaceRegistry.byPrefix.values():
			for element in namespace.elementsByName.values():
				all[(element.name, element.namespace.prefix)] = element

		allkeys = all.keys()
		allkeys.sort()
		allAsList = []
		for key in allkeys:
			element = all[key]
			allAsList.append(xsc.strElement(element.namespace.prefix, element.name, element.empty))

		s = Error.__str__(self) + "element " + xsc._strName((self.name[0], self.name[1], 0)) + " not allowed. "
		if allAsList:
			s = s + "Allowed elements are: " + ", ".join(allAsList) + "."
		else:
			s = s + "There are no allowed elements."
		return s

class IllegalProcInstError(Error):
	"""
	exception that is raised, when an illegal processing instruction is encountered
	(i.e. one that isn't registered via xsc.Namespace.register())
	"""

	def __init__(self, location, name):
		Error.__init__(self, location)
		self.name = name

	def __str__(self):
		# List the element sorted by name
		all = {}
		for namespace in xsc.namespaceRegistry.byPrefix.values():
			for procinst in namespace.procInstsByName.values():
				all[(procinst.name, procinst.namespace.prefix)] = procinst

		allkeys = all.keys()
		allkeys.sort()
		allAsList = []
		for key in allkeys:
			procinst = all[key]
			allAsList.append(xsc.strProcInstTarget(procinst.name))

		s = Error.__str__(self) + "procinst " + xsc.strProcInstTarget(self.name[1]) + " not allowed. "
		if allAsList:
			s += "Allowed procinsts are: " + ", ".join(allAsList) + "."
		else:
			s += "There are no allowed procinsts."
		return s

class IllegalElementNestingError(Error):
	"""
	exception that is raised, when an element has an illegal nesting
	(e.g. <code>&lt;a&gt;&lt;b&gt;&lt;/a&gt;&lt;/b&gt;</code>)
	"""

	def __init__(self, lineno, expectedelement, foundelement):
		Error.__init__(self, lineno)
		self.expectedelement = expectedelement
		self.foundelement = foundelement

	def __str__(self):
		return Error.__str__(self) + "illegal element nesting (" + xsc._strNode(self.expectedelement) + " expected; " + xsc._strNode(self.foundelement) + " found)"

class IllegalAttrNodeError(Error):
	"""
	exception that is raised, when something is found
	in an element attribute that doesn't belong there.
	"""

	def __init__(self, lineno, node):
		Error.__init__(self, lineno)
		self.node = node

	def __str__(self):
		return Error.__str__(self) + "illegal node of type " + self.node.__class__.__name__ + " found inside attribute"

class ImageSizeFormatError(Error):
	"""
	exception that is raised, when XSC can't format or evaluate image size attributes
	"""

	def __init__(self, element, attr):
		Error.__init__(self, element.startloc)
		self.element = element
		self.attr = attr

	def __str__(self):
		return Error.__str__(self) + "the value %r for the image size attribute %s of the element %s can't be formatted or evaluated" % (self.element[self.attr].asPlainString(), xsc.strAttrName(self.attr), self.element._str())

class FileNotFoundError(Error):
	"""
	exception that is raised, when XSC can't open a file.
	"""

	def __init__(self, location, url):
		Error.__init__(self, location)
		self.url = url

	def __str__(self):
		return Error.__str__(self) + "file " + xsc.strURL(self.url.asString()) + " can't be opened"

class IllegalObjectError(Error):
	"""
	exception that is raised, when XSC finds an illegal object in its object tree
	"""

	def __init__(self, location, object):
		Error.__init__(self, location)
		self.object = object

	def __str__(self):
		s = Error.__str__(self) + "an illegal object " + repr(self.object) + " of type " + type(self.object).__name__
		if type(self.object) == types.InstanceType:
			s = s + " (class " + self.object.__class__.__name__ + ")"
		s = s + " has been found in the XSC tree"
		return s

class MalformedCharRefError(Error):
	"""
	exception that is raised, when a character reference is malformed (e.g. &#foo;)
	"""

	def __init__(self, location, name):
		Error.__init__(self, location)
		self.name = name

	def __str__(self):
		return Error.__str__(self) + "malformed character reference: &#" + self.name + ";"

class IllegalEntityError(Error):
	"""
	exception that is raised, when an illegal entity is encountered
	(i.e. one that wasn't registered via Namespace.register)
	"""

	def __init__(self, location, name):
		Error.__init__(self, location)
		self.name = name

	def __str__(self):
		entitynames = []
		for namespacename in xsc.namespaceRegistry.byPrefix.keys():
			namespace = xsc.namespaceRegistry.byPrefix[namespacename]
			try:
				entity = namespace.entitiesByName[self.name[1]]
				entitynames.append(xsc.strEntity(entity.namespace.prefix, entity.name))
			except KeyError: # this namespace doesn't have an entity with this name
				pass
		entitynames.sort()

		s = Error.__str__(self) + "entity " + xsc.strEntity(self.name[0], self.name[1]) + " not allowed. "
		if entitynames:
			s = s + "Allowed entities are: " + ", ".join(entitynames) + "."
		else:
			s = s + "There are no allowed entities."
		return s

class IllegalCommentContentError(Error):
	"""
	exception that is raised, when there is an illegal comment, i.e. one
	containing <code>--</code> or ending in <code>-</code>.
	(This can only happen, when the comment is instantiated by the
	program, not when parsed from an XML file.)
	"""

	def __init__(self, location, comment):
		Error.__init__(self, location)
		self.comment = comment

	def __str__(self):
		return Error.__str__(self) + "comment with content " + repr(self.comment.content) + " is illegal, as it contains '--' or ends in '-'."

class IllegalProcInstFormatError(Error):
	"""
	exception that is raised, when there is an illegal processing instruction, i.e. one containing <code>?&gt;</code>.
	(This can only happen, when the processing instruction is instantiated by the
	program, not when parsed from an XML file.)
	"""

	def __init__(self, location, procinst):
		Error.__init__(self, location)
		self.procinst = procinst

	def __str__(self):
		return Error.__str__(self) + "processing instruction with content " + repr(self.procinst.content) + " is illegal, as it contains " + repr("?>") + "."

class IllegalXMLDeclFormatError(Error):
	"""
	exception that is raised, when there is an illegal XML declaration,
	i.e. there something wrong in <code><&lt;?xml ...?&gt;</code>.
	(This can only happen, when the processing instruction is instantiated by the
	program, not when parsed from an XML file.)
	"""

	def __init__(self, location, procinst):
		Error.__init__(self, location)
		self.procinst = procinst

	def __str__(self):
		return Error.__str__(self) + "XML declaration with content " + repr(self.procinst.content) + " is malformed."

class EncodingImpossibleError(Error):
	"""
	exception that is raised, when the XML tree can't be encoded, because
	an encoding is used that requires character references for certain
	characters (e.g. <code>us-ascii</code> or <code>iso-8859-1</code>)
	and those characters where encountered in a place where the can't
	be replaced with character references (e.g. inside a comment)
	"""

	def __init__(self, location, encoding, text, char):
		Error.__init__(self, location)
		self.encoding = encoding
		self.text = text
		self.char = char

	def __str__(self):
		# FIXME can't use %r because this returns a Unicode string
		return "%stext %s can't be encoded with the encoding %s because it contains the character %s." % (Error.__str__(self), repr(self.text), repr(self.encoding), repr(self.char))

