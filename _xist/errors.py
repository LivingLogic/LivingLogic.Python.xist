#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
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
<doc:par>This module contains all the exception classes of &xist;.
But note that &xist; will raise other exceptions as well.</doc:par>

<doc:par>All exceptions defined in this module are derived from
the base class <pyref class="Error"><class>Error</class></pyref>.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import types, warnings

import xsc, presenters

def warn(warning, level=3): # stacklevel==3, i.e. report the caller of our caller
	cls = UserWarning
	if isinstance(warning, DeprecationWarning):
		cls = DeprecationWarning
	warnings.warn(str(warning), cls, level)

class Error(Exception):
	"""
	base class for all XSC exceptions
	"""
	pass

class Warning(UserWarning):
	"""
	base class for all warning exceptions (i.e. those that won't
	result in a program termination.)
	"""
	pass

class EmptyElementWithContentError(Error):
	"""
	exception that is raised, when an element has content,
	but it shouldn't (i.e. empty==1)
	"""

	def __init__(self, element):
		self.element = element

	def __str__(self):
		return "element %s has EMPTY content model, but has content" % self.element._str(fullname=0, xmlname=0, decorate=1)

class IllegalAttrError(Warning, LookupError):
	"""
	exception that is raised, when an element has an illegal attribute
	(i.e. one that isn't defined in the appropriate attributes class)
	"""

	def __init__(self, attrs, attrname):
		self.attrs = attrs
		self.attrname = attrname

	def __str__(self):
		return "Attribute named %r not allowed for %s" % (self.attrname, self.attrs._str(fullname=True, xmlname=False, decorate=False))

class IllegalAttrValueWarning(Warning):
	"""
	warning that is issued, when an attribute has an illegal value when parsing or publishing.
	"""

	def __init__(self, attr):
		self.attr = attr

	def __str__(self):
		attr = self.attr
		return "Attribute value %r not allowed for %s. " % (str(attr), attr._str(fullname=True, xmlname=False, decorate=False))

class RequiredAttrMissingWarning(Warning):
	"""
	warning that is issued, when required attribute is missing when parsing or publishing.
	"""

	def __init__(self, attrs, reqattrs):
		self.attrs = attrs
		self.reqattrs = reqattrs

	def __str__(self):
		v = ["Required attribute"]
		if len(self.reqattrs)>1:
			v.append("s ")
			v.append(", ".join(["%r" % attr for attr in self.reqattrs]))
		else:
			v.append(" %r" % self.reqattrs[0])
		v.append(" missing in %s." % self.attrs._str(fullname=True, xmlname=False, decorate=False))
		return "".join(v)

class IllegalPrefixError(Error, LookupError):
	"""
	Exception that is raised when a namespace prefix is undefined.
	"""
	def __init__(self, prefix):
		self.prefix = prefix

	def __str__(self):
		return "namespace prefix %r is undefined" % self.prefix

class IllegalNamespaceError(Error, LookupError):
	"""
	Exception that is raised when a namespace name is undefined
	i.e. if there is no namespace with this name.
	"""
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "namespace name %r is undefined" % self.name

class IllegalElementError(Error):
	"""
	exception that is raised, when an illegal element is encountered
	(i.e. one that isn't registered via xsc.Namespace.register())
	"""

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "element named %r not allowed. " % (self.name, )

class IllegalProcInstError(Error):
	"""
	exception that is raised, when an illegal processing instruction is encountered
	(i.e. one that isn't registered via xsc.Namespace.register())
	"""

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "procinst named %r not allowed" % (self.name, )

class ElementNestingError(Error):
	"""
	exception that is raised, when an element has an illegal nesting
	(e.g. <code>&lt;a&gt;&lt;b&gt;&lt;/a&gt;&lt;/b&gt;</code>)
	"""

	def __init__(self, expectedelement, foundelement):
		self.expectedelement = expectedelement
		self.foundelement = foundelement

	def __str__(self):
		return "mismatched element nesting (close tag for %s expected; close tag for %s found)" % (self.expectedelement._str(fullname=1, xmlname=0, decorate=1), self.foundelement._str(fullname=1, xmlname=0, decorate=1))

class IllegalAttrNodeError(Error):
	"""
	exception that is raised, when something is found
	in an attribute that doesn't belong there (e.g. an element or a comment).
	"""

	def __init__(self, node):
		self.node = node

	def __str__(self):
		return "illegal node of type %s found inside attribute" % self.node.__class__.__name__

class FileNotFoundWarning(Warning):
	"""
	warning that is raised, when a file can't be found
	"""
	def __init__(self, message, filename, exc):
		Warning.__init__(self, message, filename, exc)
		self.message = message
		self.filename = filename
		self.exc = exc

	def __str__(self):
		return "%s: file %s not found (%s)" % (self.message, self.filename, self.exc)

class ImageSizeFormatWarning(UserWarning):
	"""
	warning that is raised, when XSC can't format or evaluate image size attributes.
	"""

	def __init__(self, element, attr, exc):
		UserWarning.__init__(self, element, attr, exc)
		self.element = element
		self.attr = attr
		self.exc = exc

	def __str__(self):
		return "the value %r for the image size attribute %s of the element %s can't be formatted or evaluated (%s). The attribute will be dropped." % (unicode(self.attr), self.attr._str(fullname=0, xmlname=0, decorate=0), self.element._str(fullname=1, xmlname=1, decorate=1), self.exc)

class IllegalObjectWarning(Warning):
	"""
	warning that is issued, when XSC finds an illegal object in its object tree.
	"""

	def __init__(self, object):
		self.object = object

	def __str__(self):
		s = "an illegal object %r of type %s" % (self.object, type(self.object).__name__)
		if type(self.object) is types.InstanceType:
			s += " (class %s)" % self.object.__class__.__name__
		s += " has been found in the XSC tree. The object will be ignored."
		return s

class MalformedCharRefError(Error):
	"""
	exception that is raised, when a character reference is malformed (e.g. &#foo;)
	"""

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "malformed character reference: &#%s;" % self.name

class IllegalEntityError(Error):
	"""
	exception that is raised, when an illegal entity or charref is encountered
	(i.e. one that wasn't registered via Namespace.register)
	"""

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "entity named %r not allowed" % (self.name, )

class IllegalCommentContentError(Error):
	"""
	exception that is raised, when there is an illegal comment, i.e. one
	containing <code>--</code> or ending in <code>-</code>.
	(This can only happen, when the comment is instantiated by the
	program, not when parsed from an XML file.)
	"""

	def __init__(self, comment):
		self.comment = comment

	def __str__(self):
		return "comment with content %s is illegal, as it contains '--' or ends in '-'." % presenters.strTextOutsideAttr(self.comment.content)

class IllegalProcInstFormatError(Error):
	"""
	exception that is raised, when there is an illegal processing instruction, i.e. one containing <code>?&gt;</code>.
	(This can only happen, when the processing instruction is instantiated by the
	program, not when parsed from an XML file.)
	"""

	def __init__(self, procinst):
		self.procinst = procinst

	def __str__(self):
		return "processing instruction with content %s is illegal, as it contains %r." % (presenters.strProcInstContent(self.procinst.content), "?>")

class IllegalXMLDeclFormatError(Error):
	"""
	exception that is raised, when there is an illegal XML declaration,
	i.e. there something wrong in <code><&lt;?xml ...?&gt;</code>.
	(This can only happen, when the processing instruction is instantiated by the
	program, not when parsed from an XML file.)
	"""

	def __init__(self, procinst):
		self.procinst = procinst

	def __str__(self):
		return "XML declaration with content %r is malformed." % presenters.strProcInstContent(self.procinst.content)

class EncodingImpossibleError(Error):
	"""
	exception that is raised, when the &xml; tree can't be encoded, because
	an encoding is used that requires character references for certain
	characters (e.g. <code>us-ascii</code> or <code>iso-8859-1</code>)
	and those characters where encountered in a place where the can't
	be replaced with character references (e.g. inside a comment)
	"""

	def __init__(self, encoding, text, char):
		self.encoding = encoding
		self.text = text
		self.char = char

	def __str__(self):
		return "text %r can't be encoded with the encoding %r because it contains the character %r." % (self.text, self.encoding, self.char)

# FIXME: This doesn't work yet, because warnings.warn does not allow passing Warning
# instances, so the filter is ineffective. This will change in Python 2.3
warnings.filterwarnings("always", category=Warning)

