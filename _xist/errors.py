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
This module contains all the exception classes of XSC.
But note that XSC does raise other exceptions as well.

All exceptions defined in this module are derived from
the base class Error.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import types, exceptions

import xsc, presenters

class Error(Exception):
	"""
	base class for all XSC exceptions
	"""

	def __init__(self):
		self.location = None # will be filled in by the parser, that catches us, modifies us and raises us again.

	def __str__(self):
		if self.location is not None:
			return "%s: " % self.location
		else:
			return ""

class EmptyElementWithContentError(Error):
	"""
	exception that is raised, when an element has content,
	but it shouldn't (i.e. empty==1)
	"""

	def __init__(self, element):
		Error.__init__(self)
		self.element = element

	def __str__(self):
		return Error.__str__(self) + "element %s specified to be empty, but has content" % presenters.strElementWithBrackets(self.element)

class IllegalAttrError(Error):
	"""
	exception that is raised, when an element has an illegal attribute
	(i.e. one that isn't contained in it's attrHandlers)
	"""

	def __init__(self, element, attrname):
		Error.__init__(self)
		self.element = element
		self.attrname = attrname

	def __str__(self):
		attrs = self.element.attrHandlers.keys()
		s = Error.__str__(self) + "Attribute %s not allowed in element %s. " % (presenters.strAttrName(self.attrname), presenters.strElementWithBrackets(self.element))
		if len(attrs):
			attrs.sort()
			attrs = ", ".join([ str(presenters.strAttrName(attr)) for attr in attrs])
			s = s + "Allowed attributes are: %s." % attrs
		else:
			s = s + "No attributes allowed."
		return s

class AttrNotFoundError(Error):
	"""
	exception that is raised, when an attribute is fetched that isn't there
	"""

	def __init__(self, element, attrname):
		Error.__init__(self)
		self.element = element
		self.attrname = attrname

	def __str__(self):
		attrs = self.element.attrs.keys()

		s = Error.__str__(self) + "Attribute %s not found in element %s. " % (presenters.strAttrName(self.attrname), presenters.strElementWithBrackets(self.element))

		if len(attrs):
			attrs.sort()
			attrs = ", ".join([ str(presenters.strAttrName(attr)) for attr in attrs ])
			s = s + "Available attributes are: %s." % attrs
		else:
			s = s + "No attributes available."

		return s

class IllegalElementError(Error):
	"""
	exception that is raised, when an illegal element is encountered
	(i.e. one that isn't registered via xsc.Namespace.register())
	"""

	def __init__(self, name):
		Error.__init__(self)
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
			allAsList.append(str(presenters.strElementWithBrackets(element)))

		s = Error.__str__(self) + "element %s not allowed. " % presenters.strElementNameWithBrackets(self.name[0], self.name[1])
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

	def __init__(self, name):
		Error.__init__(self)
		self.name = name

	def __str__(self):
		# List the procinsts sorted by name
		all = {}
		for namespace in xsc.namespaceRegistry.byPrefix.values():
			for procinst in namespace.procInstsByName.values():
				all[(procinst.name, procinst.namespace.prefix)] = procinst

		allkeys = all.keys()
		allkeys.sort()
		allAsList = []
		for key in allkeys:
			procinst = all[key]
			allAsList.append(str(presenters.strProcInstWithBrackets(procinst)))

		s = Error.__str__(self) + "procinst %s not allowed. " % presenters.strProcInstTargetWithBrackets(self.name[0], self.name[1])
		if allAsList:
			s = s + "Allowed procinsts are: " + ", ".join(allAsList) + "."
		else:
			s = s + "There are no allowed procinsts."
		return s

class IllegalElementNestingError(Error):
	"""
	exception that is raised, when an element has an illegal nesting
	(e.g. <code>&lt;a&gt;&lt;b&gt;&lt;/a&gt;&lt;/b&gt;</code>)
	"""

	def __init__(self, expectedelement, foundelement):
		Error.__init__(self)
		self.expectedelement = expectedelement
		self.foundelement = foundelement

	def __str__(self):
		return Error.__str__(self) + "illegal element nesting (%s expected; %s found)" % (presenters.strElementWithBrackets(self.expectedelement), presenters.strElementWithBrackets(self.foundelement))

class IllegalAttrNodeError(Error):
	"""
	exception that is raised, when something is found
	in an attribute that doesn't belong there (e.g. an element or a comment).
	"""

	def __init__(self, node):
		Error.__init__(self)
		self.node = node

	def __str__(self):
		return Error.__str__(self) + "illegal node of type %s found inside attribute" % self.node.__class__.__name__

class ImageSizeFormatError(Error):
	"""
	exception that is raised, when XSC can't format or evaluate image size attributes
	"""

	def __init__(self, element, attrname):
		Error.__init__(self)
		self.element = element
		self.attrname = attrname

	def __str__(self):
		return Error.__str__(self) + "the value %s for the image size attribute %s of the element %s can't be formatted or evaluated" % (presenters.strAttrValue(self.element[self.attrname].asPlainString()), presenters.strAttrName(self.attrname), presenters.strElementWithBrackets(self.element))

class FileNotFoundError(Error):
	"""
	exception that is raised, when XSC can't open a file.
	"""

	def __init__(self, url):
		Error.__init__(self)
		self.url = url

	def __str__(self):
		return Error.__str__(self) + "file %s can't be opened" % presenters.strURL(self.url.asString())

class IllegalObjectError(Error):
	"""
	exception that is raised, when XSC finds an illegal object in its object tree
	"""

	def __init__(self, object):
		Error.__init__(self)
		self.object = object

	def __str__(self):
		s = Error.__str__(self) + "an illegal object %r of type %s" + (self.object, type(self.object).__name__)
		if type(self.object) is types.InstanceType:
			s += " (class %s)" % self.object.__class__.__name__
		s += " has been found in the XSC tree"
		return s

class MalformedCharRefError(Error):
	"""
	exception that is raised, when a character reference is malformed (e.g. &#foo;)
	"""

	def __init__(self, name):
		Error.__init__(self)
		self.name = name

	def __str__(self):
		return Error.__str__(self) + "malformed character reference: &#%s;" % self.name

class IllegalEntityError(Error):
	"""
	exception that is raised, when an illegal entity is encountered
	(i.e. one that wasn't registered via Namespace.register)
	"""

	def __init__(self, name):
		Error.__init__(self)
		self.name = name

	def __str__(self):
		# List the entities sorted by name
		all = {}
		for namespace in xsc.namespaceRegistry.byPrefix.values():
			for entity in namespace.entitiesByName.values():
				all[(entity.name, entity.namespace.prefix)] = entity

		allkeys = all.keys()
		allkeys.sort()
		allAsList = []
		for key in allkeys:
			entity = all[key]
			allAsList.append(str(presenters.strEntity(entity)))

		s = Error.__str__(self) + "entity %s not allowed. " % presenters.strEntityName(self.name[0], self.name[1])
		if allAsList:
			s = s + "Allowed entities are: " + ", ".join(allAsList) + "."
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

	def __init__(self, comment):
		Error.__init__(self)
		self.comment = comment

	def __str__(self):
		return Error.__str__(self) + "comment with content %s is illegal, as it contains '--' or ends in '-'." % presenters.strTextOutsideAttr(self.comment._content)

class IllegalProcInstFormatError(Error):
	"""
	exception that is raised, when there is an illegal processing instruction, i.e. one containing <code>?&gt;</code>.
	(This can only happen, when the processing instruction is instantiated by the
	program, not when parsed from an XML file.)
	"""

	def __init__(self, procinst):
		Error.__init__(self)
		self.procinst = procinst

	def __str__(self):
		return Error.__str__(self) + "processing instruction with content %s is illegal, as it contains %r." % (presenters.strProcInstContent(self.procinst._content), "?>")

class IllegalXMLDeclFormatError(Error):
	"""
	exception that is raised, when there is an illegal XML declaration,
	i.e. there something wrong in <code><&lt;?xml ...?&gt;</code>.
	(This can only happen, when the processing instruction is instantiated by the
	program, not when parsed from an XML file.)
	"""

	def __init__(self, procinst):
		Error.__init__(self)
		self.procinst = procinst

	def __str__(self):
		return Error.__str__(self) + "XML declaration with content %r is malformed." % presenters.strProcInstContent(self.procinst._content)

class EncodingImpossibleError(Error):
	"""
	exception that is raised, when the XML tree can't be encoded, because
	an encoding is used that requires character references for certain
	characters (e.g. <code>us-ascii</code> or <code>iso-8859-1</code>)
	and those characters where encountered in a place where the can't
	be replaced with character references (e.g. inside a comment)
	"""

	def __init__(self, encoding, text, char):
		Error.__init__(self)
		self.encoding = encoding
		self.text = text
		self.char = char

	def __str__(self):
		# FIXME can't use %r because this returns a Unicode string
		return "%stext %s can't be encoded with the encoding %s because it contains the character %s." % (Error.__str__(self), repr(self.text), repr(self.encoding), repr(self.char))

