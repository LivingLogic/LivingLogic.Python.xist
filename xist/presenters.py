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
This module contains classes that are used for dumping elements
to the terminal.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import os
import xsc, options, color

def getStringFromEnv(name, default):
	try:
		return os.environ[name]
	except:
		return default

def getIntFromEnv(name, default):
	try:
		return int(os.environ[name])
	except:
		return default

class EnvText(color.Text):
	def __init__(self, *data):
		color.Text.__init__(self, *data)
		if not "color" in self.__class__.__dict__.keys(): # no inheritance
			try:
				var = eval(os.environ[self.envname])
				if type(var) is types.StringType:
					var = (var, var)
				self.__class__.color = var
			except:
				self.__class__.color = self.default

	def getColor(self):
		if options.repransi==0:
			return -1
		else:
			return self.color[options.repransi-1]

class EnvTextForTab(EnvText):
	"""
	ANSI escape sequence to be used for tabs
	"""
	envname = "XSC_REPRANSI_TAB"
	default = (0x8, 0x8)

class EnvTextForQuote(EnvText):
	"""
	ANSI escape sequence to be used for quotes
	(delimiters for text and attribute nodes)
	"""
	envname = "XSC_REPRANSI_QUOTE"
	default = (0xa, 0xf)

class EnvTextForSlash(EnvText):
	envname = "XSC_REPRANSI_SLASH"
	default = (0x7, 0xf)

class EnvTextForBracket(EnvText):
	"""
	ANSI escape sequence to be used for quotes
	(delimiters for text and attribute nodes)
	"""
	envname = "XSC_REPRANSI_BRACKET"
	default = (0xa, 0xf)

class EnvTextForColon(EnvText):
	"""
	ANSI escape sequence to be used for colon
	(i.e. namespace separator)
	"""
	envname = "XSC_REPRANSI_BRACKET"
	default = (0xa, 0xf)

class EnvTextForQuestion(EnvText):
	"""
	ANSI escape sequence to be used for question marks
	(delimiters for processing instructions)
	"""
	envname = "XSC_REPRANSI_QUESTION"
	default = (0xa, 0xf)

class EnvTextForExclamation(EnvText):
	"""
	ANSI escape sequence to be used for exclamation marks
	(used in comments and doctypes)
	"""
	envname = "XSC_REPRANSI_EXCLAMATION"
	default = (0xa, 0xf)

class EnvTextForText(EnvText):
	"""
	ANSI escape sequence to be used for text
	"""
	envname = "XSC_REPRANSI_TEXT"
	default = (0x7, 0x7)

class EnvTextForCharRef(EnvText):
	"""
	ANSI escape sequence to be used for character references
	"""
	envname = "XSC_REPRANSI_CHARREF"
	default = (0xf, 0x5)

class EnvTextForNamespace(EnvText):
	"""
	ANSI escape sequence to be used for namespaces
	"""
	envname = "XSC_REPRANSI_NAMESPACE"
	default = (0xf, 0x4)

class EnvTextForElementName(EnvText):
	"""
	ANSI escape sequence to be used for element names
	"""
	envname = "XSC_REPRANSI_ELEMENTNAME"
	default = (0xe, 0xc)

class EnvTextForEntityName(EnvText):
	"""
	ANSI escape sequence to be used for entity names
	"""
	envname = "XSC_REPRANSI_ENTITYNAME"
	default = (0xf, 0xc)

class EnvTextForAttrName(EnvText):
	"""
	ANSI escape sequence to be used for attribute names
	"""
	envname = "XSC_REPRANSI_ATTRNAME"
	default = (0xf, 0xc)

class EnvTextForDocTypeMarker(EnvText):
	"""
	ANSI escape sequence to be used for document types
	marker (i.e. !DOCTYPE)
	"""
	envname = "XSC_REPRANSI_DOCTYPEMARKER"
	default = (0xf, 0xf)

class EnvTextForDocTypeText(EnvText):
	"""
	ANSI escape sequence to be used for document types
	"""
	envname = "XSC_REPRANSI_DOCTYPETEXT"
	default = (0x7, 0x7)

class EnvTextForCommentMarker(EnvText):
	"""
	ANSI escape sequence to be used for comment markers (i.e. --)
	"""
	envname = "XSC_REPRANSI_COMMENTMARKER"
	default = (0x7, 0xf)

class EnvTextForCommentText(EnvText):
	"""
	ANSI escape sequence to be used for comment text
	"""
	envname = "XSC_REPRANSI_COMMENTTEXT"
	default = (0x7, 0x7)

class EnvTextForAttrValue(EnvText):
	"""
	ANSI escape sequence to be used for attribute values
	"""
	envname = "XSC_REPRANSI_ATTRVALUE"
	default = (0x7, 0x6)

class EnvTextForURL(EnvText):
	"""
	ANSI escape sequence to be used for URLs
	"""
	envname = "XSC_REPRANSI_URL"
	default = (0xb, 0x2)

class EnvTextForProcInstTarget(EnvText):
	"""
	ANSI escape sequence to be used for processing instruction targets
	"""
	envname = "XSC_REPRANSI_PROCINSTTARGET"
	default = (0x9, 0x9)

class EnvTextForProcInstData(EnvText):
	"""
	ANSI escape sequence to be used for processing instruction data
	"""
	envname = "XSC_REPRANSI_PROCINSTDATA"
	default = (0x7, 0x7)

class EscInlineText(color.EscapedText):
	ascharref = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f<>&"
	ascolor   = "\x09\x0a"

	def escapeChar(self, char):
		if char in self.ascolor:
			return EnvTextForTab(char)
		else:
			ascharref = char in self.ascharref
			if not ascharref:
				try:
					char.encode(options.reprEncoding)
				except:
					ascharref = 1
			if ascharref:
				charcode = ord(char)
				entity = xsc.defaultNamespaces.entityFromNumber(charcode)
				if entity is not None:
					return EnvTextForCharRef("&", entity.name, ";")
				else:
					return EnvTextForCharRef("&#", str(charcode), ";")
		return char

class EscInlineAttr(EscInlineText):
	ascharref = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f<>\"&"
	ascolor   = "\x09\x0a"

class Presenter:
	"""
	base class for all presenters.
	"""

	def __init__(self, namespaces=None, encoding=None, ansi=None):
		if namespaces is None:
			namespaces = xsc.defaultNamespaces
		self.namespaces = namespaces
		if encoding is None:
			encoding = options.reprEncoding
		self.encoding = encoding
		self.ansi = ansi

	def reset(self):
		self.buffer = color.StringBuffer()
		self.stream = color.Stream(self.buffer)
		self.inAttr = 0

	def strElement(self, node):
		s = color.Text()
		if hasattr(node, "namespace"):
			s.append(EnvTextForNamespace(EscInlineText(node.namespace.prefix)))
			s.append(self.strColon())
		if hasattr(node, "name"):
			name = node.name
		else:
			name = node.__class__.name
		s.append(EnvTextForElementName(EscInlineText(name)))
		return s

	def strEntity(self, node):
		s = color.Text("&")
		if hasattr(node, "namespace"):
			s.append(EnvTextForNamespace(EscInlineText(node.namespace.prefix)))
			s.append(EnvTextForColon(":"))
		if hasattr(node, "name"):
			name = node.name
		else:
			name = node.__class__.name
		s.append(EnvTextForEntityName(EscInlineText(name)))
		s.append(";")
		return s

	def strAttrName(self, attrname):
		return EnvTextForAttrName(EscInlineText(attrname))

	def strDocTypeMarker(self):
		return EnvTextForDocTypeMarker("DOCTYPE")

	def strDocTypeText(self, text):
		return EnvTextForDocTypeText(EscInlineText(text))

	def strCommentMarker(self):
		return EnvTextForCommentMarker("--")

	def strCommentText(self, text):
		return EnvTextForCommentText(EscInlineText(text))

	def strProcInstTarget(self, target):
		return EnvTextForProcInstTarget(EscInlineText(target))

	def strProcInstData(self, data):
		return EnvTextForProcInstData(EscInlineText(data))

	def strTextOutsideAttr(self, text):
		return EnvTextForText(EscInlineText(text))

	def strTextInAttr(self, text):
		return EnvTextForAttrValue(EscInlineAttr(text))

	def strSlash(self):
		return EnvTextForSlash("/")

	def strBracketOpen(self):
		return EnvTextForBracket("<")

	def strBracketClose(self):
		return EnvTextForBracket(">")

	def strColon(self):
		return EnvTextForColon(":")

	def strQuestion(self):
		return EnvTextForQuestion("?")

	def strExclamation(self):
		return EnvTextForExclamation("!")

	def strQuote(self):
		return EnvTextForQuote('"')

	def strTab(self, count):
		return EnvTextForTab(options.reprtab*count)

	def strURL(self, url):
		return EnvTextForURL(EscInlineText(url))

class NormalPresenter(Presenter):
	def beginPresentation(self):
		self.reset()

	def endPresentation(self):
		self.stream.finish()
		result = str(self.buffer)
		self.reset()
		return result

	def presentText(self, node):
		if self.inAttr:
			self.stream.write(self.strTextInAttr(node._content))
		else:
			self.stream.write(self.strTextOutsideAttr(node._content))

	def presentFrag(self, node):
		for child in node:
			child.present(self)

	def presentComment(self, node):
		self.stream.write(
			self.strBracketOpen(),
			self.strExclamation(),
			self.strCommentMarker(),
			self.strCommentText(node._content),
			self.strCommentMarker(),
			self.strBracketClose()
		)

	def presentDocType(self, node):
		self.stream.write(
			self.strBracketOpen(),
			self.strExclamation(),
			self.strDocTypeMarker(),
			" ",
			self.strDocTypeText(node._content),
			self.strBracketClose()
		)

	def presentProcInst(self, node):
		self.stream.write(
			self.strBracketOpen(),
			self.strQuestion(),
			self.strProcInstTarget(node._target),
			" ",
			self.strProcInstData(node._content),
			self.strQuestion(),
			self.strBracketClose()
		)

	def _writeAttrs(self, dict):
		for attr in dict.keys():
			self.stream.write(" ")
			self.stream.write(self.strAttrName(attr))
			value = dict[attr]
			if len(value):
				self.stream.write("=")
				self.stream.write(self.strQuote())
				value.present(self)
				self.stream.write(self.strQuote())

	def presentElement(self, node):
		if node.empty:
			self.stream.write(
				self.strBracketOpen(),
				self.strElement(node)
			)
			self._writeAttrs(node.attrs)
			self.stream.write(
				self.strSlash(),
				self.strBracketClose()
			)
		else:
			self.stream.write(
				self.strBracketOpen(),
				self.strElement(node)
			)
			self._writeAttrs(node.attrs)
			self.stream.write(self.strBracketClose())
			for child in node:
				child.present(self)
			self.stream.write(
				self.strBracketOpen(),
				self.strSlash(),
				self.strElement(node),
				self.strBracketClose()
			)

	def presentEntity(self, node):
		self.stream.write(self.strEntity(node))

	def presentNull(self, node):
		self.stream.write(
			self.strBracketOpen(),
			self.strElement(node),
			self.strSlash(),
			self.strBracketClose()
		)

	def presentAttr(self, node):
		self.inAttr = 1
		xsc.Frag.present(node, self)
		self.inAttr = 0

	def presentURLAttr(self, node):
		self.inAttr = 1
		self.stream.write(self.strURL(node.asString()))
		self.inAttr = 0

defaultPresenterClass = NormalPresenter
