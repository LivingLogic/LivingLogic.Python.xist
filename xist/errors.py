#! /usr/bin/env python

## Copyright 1999-2000 by Living Logic AG, Bayreuth, Germany.
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission notice
## appear in supporting documentation, and that the name of Living Logic AG not be used
## in advertising or publicity pertaining to distribution of the software without specific,
## written prior permission.
##
## LIVING LOGIC AG DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
## ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL LIVING LOGIC AG
## BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
## RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
## OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
## OF THIS SOFTWARE.

"""
This module contains all the exception classes of XSC.
But note that XSC does raise other exceptions as well.

All exceptions defined in this module are derived from
the base class Error.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import string
import xsc
import exceptions
import types

class Error(Exception):
	"""
	base class for all XSC exceptions
	"""

	def __init__(self,location = None):
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

	def __init__(self,element):
		Error.__init__(self)
		self.element = element

	def __str__(self):
		return Error.__str__(self) + "element " + self.element._str() + " specified to be empty, but has content"

class IllegalAttributeError(Error):
	"""
	exception that is raised, when an element has an illegal attribute
	(i.e. one that isn't contained in it's attrHandlers)
	"""

	def __init__(self,element,attr):
		Error.__init__(self)
		self.element = element
		self.attr = attr

	def __str__(self):
		attrs = self.element.attrHandlers.keys();
		attrs.sort()

		v = []

		for attr in attrs:
			v.append(xsc.strAttrName(attr))

		return Error.__str__(self) + "Attribute " + xsc.strAttrName(self.attr) + " not allowed in element " + xsc._strNode(self.element.__class__) + ". Allowed attributes are: " + string.join(v,", ") + "."

class AttributeNotFoundError(Error):
	"""
	exception that is raised, when an attribute is fetched that isn't there
	"""

	def __init__(self,element,attr):
		Error.__init__(self)
		self.element = element
		self.attr = attr

	def __str__(self):
		attrs = self.element.attrs.keys();

		s = Error.__str__(self) + "Attribute " + xsc.strAttrName(self.attr) + " not found in element " + xsc._strNode(self.element.__class__) +". "

		if len(attrs):
			attrs.sort()
			v = []
			for attr in attrs:
				v.append(xsc.strAttrName(attr))
			s = s + "Available attributes are: " + string.join(v,", ") + "."
		else:
			s = s + "No attributes available."

		return s

class IllegalElementError(Error):
	"""
	exception that is raised, when an illegal element is encountered
	(i.e. one that isn't registered via registerElement)
	"""

	def __init__(self,location,name):
		Error.__init__(self,location)
		self.name = name

	def __str__(self):
		elementnames = []
		for elementname in xsc._elementHandlers.keys():
			for namespace in xsc._elementHandlers[elementname].keys():
				elementnames.append(xsc._strNode(xsc._elementHandlers[elementname][namespace],brackets = 1))
		elementnames.sort()

		s = Error.__str__(self) + "element " + xsc._strName((self.name[0],self.name[1],0)) + " not allowed. "
		if elementnames:
			s = s + "Allowed elements are: " + string.join(elementnames,", ") + "."
		else:
			s = s + "There are no allowed elements."
		return s

class IllegalElementNestingError(Error):
	"""
	exception that is raised, when an element has an illegal nesting
	(e.g. <code>&lt;a&gt;&lt;b&gt;&lt;/a&gt;&lt;/b&gt;</code>)
	"""

	def __init__(self,lineno,expectedelement,foundelement):
		Error.__init__(self,lineno)
		self.expectedelement = expectedelement
		self.foundelement = foundelement

	def __str__(self):
		return Error.__str__(self) + "illegal element nesting (" + xsc._strNode(self.expectedelement) + " expected; " + xsc._strNode(self.foundelement) + " found)"

class ImageSizeFormatError(Error):
	"""
	exception that is raised, when XSC can't format or evaluate image size attributes
	"""

	def __init__(self,element,attr):
		Error.__init__(self,element.location)
		self.element = element
		self.attr = attr

	def __str__(self):
		return Error.__str__(self) + "the value '" + self.element[self.attr].asPlainString() + "' for the image size attribute " + strAttrName(self.attr) + " of the element " + self.element._str() + " can't be formatted or evaluated"

class FileNotFoundError(Error):
	"""
	exception that is raised, when XSC can't open a file.
	"""

	def __init__(self,location,url):
		Error.__init__(self,location)
		self.url = url

	def __str__(self):
		return Error.__str__(self) + "file " + xsc.strURL(str(self.url)) + " can't be opened"

class IllegalObjectError(Error):
	"""
	exception that is raised, when XSC finds an illegal object in its object tree
	"""

	def __init__(self,location,object):
		Error.__init__(self,location)
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

	def __init__(self,location,name):
		Error.__init__(self,location)
		self.name = name

	def __str__(self):
		return Error.__str__(self) + "malformed character reference: &#" + self.name + ";"

class UnknownEntityError(Error):
	"""
	exception that is raised, when an unknown entity is encountered
	(i.e. one that wasn't registered via registerEntity)
	"""

	def __init__(self,location,name):
		Error.__init__(self,location)
		self.name = name

	def __str__(self):
		return Error.__str__(self) + "Unknown entitiy: &" + self.name + ";"

class AmbiguousElementError(Error):
	"""
	exception that is raised, when an element is encountered without a namespace
	and there is more than one element registered with this name.
	"""

	def __init__(self,location,name):
		Error.__init__(self,location)
		self.name = name

	def __str__(self):
		elementnames = []
		for namespace in xsc._elementHandlers[self.name[1]].keys():
			elementnames.append(xsc._strNode(xsc._elementHandlers[self.name[1]][namespace]))
		elementnames.sort()

		return Error.__str__(self) + "element " + _strName((self.name[0],self.name[1],0)) + " is ambigous. Possible elements are: " + string.join(elementnames,", ") + "."

