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
This module contains classes that are used for dumping elements
to the terminal.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import os
import xsc, options
import ansistyle

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

def getColorsFromEnv(name, default):
	try:
		var = eval(os.environ[self.envname])
		if type(var) is types.StringType:
			var = (var, var)
		return var
	except:
		return default

class EnvText(ansistyle.Text):
	def getColor(self):
		if options.repransi==0:
			return -1
		else:
			return self.color[options.repransi-1]

class EnvTextForTab(EnvText):
	"""
	ANSI escape sequence to be used for tabs
	"""
	color = getColorsFromEnv("XSC_REPRANSI_TAB", (0x8, 0x8))

class EnvTextForQuote(EnvText):
	"""
	ANSI escape sequence to be used for quotes
	(delimiters for text and attribute nodes)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_QUOTE", (0xa, 0xf))

class EnvTextForSlash(EnvText):
	color = getColorsFromEnv("XSC_REPRANSI_SLASH", (0x7, 0xf))

class EnvTextForBracket(EnvText):
	"""
	ANSI escape sequence to be used for quotes
	(delimiters for text and attribute nodes)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_BRACKET", (0xa, 0xf))

class EnvTextForColon(EnvText):
	"""
	ANSI escape sequence to be used for colon
	(i.e. namespace separator)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_BRACKET", (0xa, 0xf))

class EnvTextForQuestion(EnvText):
	"""
	ANSI escape sequence to be used for question marks
	(delimiters for processing instructions)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_QUESTION", (0xa, 0xf))

class EnvTextForExclamation(EnvText):
	"""
	ANSI escape sequence to be used for exclamation marks
	(used in comments and doctypes)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_EXCLAMATION", (0xa, 0xf))

class EnvTextForText(EnvText):
	"""
	ANSI escape sequence to be used for text
	"""
	color = getColorsFromEnv("XSC_REPRANSI_TEXT", (0x7, 0x7))

class EnvTextForCharRef(EnvText):
	"""
	ANSI escape sequence to be used for character references
	"""
	color = getColorsFromEnv("XSC_REPRANSI_CHARREF", (0xf, 0x5))

class EnvTextForNamespace(EnvText):
	"""
	ANSI escape sequence to be used for namespaces
	"""
	color = getColorsFromEnv("XSC_REPRANSI_NAMESPACE", (0xf, 0x4))

class EnvTextForElementName(EnvText):
	"""
	ANSI escape sequence to be used for element names
	"""
	color = getColorsFromEnv("XSC_REPRANSI_ELEMENTNAME", (0xe, 0xc))

class EnvTextForEntityName(EnvText):
	"""
	ANSI escape sequence to be used for entity names
	"""
	color = getColorsFromEnv("XSC_REPRANSI_ENTITYNAME", (0xf, 0xc))

class EnvTextForAttrName(EnvText):
	"""
	ANSI escape sequence to be used for attribute names
	"""
	color = getColorsFromEnv("XSC_REPRANSI_ATTRNAME", (0xf, 0xc))

class EnvTextForDocTypeMarker(EnvText):
	"""
	ANSI escape sequence to be used for document types
	marker (i.e. !DOCTYPE)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_DOCTYPEMARKER", (0xf, 0xf))

class EnvTextForDocTypeText(EnvText):
	"""
	ANSI escape sequence to be used for document types
	"""
	color = getColorsFromEnv("XSC_REPRANSI_DOCTYPETEXT", (0x7, 0x7))

class EnvTextForCommentMarker(EnvText):
	"""
	ANSI escape sequence to be used for comment markers (i.e. --)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_COMMENTMARKER", (0x7, 0xf))

class EnvTextForCommentText(EnvText):
	"""
	ANSI escape sequence to be used for comment text
	"""
	color = getColorsFromEnv("XSC_REPRANSI_COMMENTTEXT", (0x7, 0x7))

class EnvTextForAttrValue(EnvText):
	"""
	ANSI escape sequence to be used for attribute values
	"""
	color = getColorsFromEnv("XSC_REPRANSI_ATTRVALUE", (0x7, 0x6))

class EnvTextForURL(EnvText):
	"""
	ANSI escape sequence to be used for URLs
	"""
	color = getColorsFromEnv("XSC_REPRANSI_URL", (0xb, 0x2))

class EnvTextForProcInstTarget(EnvText):
	"""
	ANSI escape sequence to be used for processing instruction targets
	"""
	color = getColorsFromEnv("XSC_REPRANSI_PROCINSTTARGET", (0x9, 0x9))

class EnvTextForProcInstData(EnvText):
	"""
	ANSI escape sequence to be used for processing instruction data
	"""
	color = getColorsFromEnv("XSC_REPRANSI_PROCINSTDATA", (0x7, 0x7))

class EscInlineText(ansistyle.EscapedText):
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

def strBracketOpen():
	return EnvTextForBracket("<")

def strBracketClose():
	return EnvTextForBracket(">")

def strSlash():
	return EnvTextForSlash("/")

def strColon():
	return EnvTextForColon(":")

def strQuestion():
	return EnvTextForQuestion("?")

def strExclamation():
	return EnvTextForExclamation("!")

def strQuote():
	return EnvTextForQuote('"')

def strTab(count):
	return EnvTextForTab(options.reprtab*count)

def strURL(url):
	return EnvTextForURL(EscInlineText(url))

def strDocTypeMarker():
	return EnvTextForDocTypeMarker("DOCTYPE")

def strDocTypeText(text):
	return EnvTextForDocTypeText(EscInlineText(text))

def strCommentMarker():
	return EnvTextForCommentMarker("--")

def strCommentText(text):
	return EnvTextForCommentText(EscInlineText(text))

def strElementName(namespacename=None, elementname=None):
	s = ansistyle.Text()
	if namespacename is not None:
		s.append(
			EnvTextForNamespace(EscInlineText(namespacename)),
			EnvTextForColon(":")
		)
	if elementname is None:
		elementname = "unnamed"
	s.append(EnvTextForElementName(EscInlineText(elementname)))
	return s

def strElementNameWithBrackets(namespacename=None, elementname=None):
	return ansistyle.Text(strBracketOpen(), strElementName(namespacename, elementname), EnvTextForBracket(">"))

def strElement(node):
	if hasattr(node, "namespace"):
		namespacename = node.namespace.prefix
	else:
		namespacename = None
	if hasattr(node, "name"):
		elementname = node.name
	else:
		elementname = node.__class__.__name__
	return strElementName(namespacename, elementname)

def strElementWithBrackets(node):
	return ansistyle.Text(strBracketOpen(), strElement(node), strBracketClose())

def strEntityName(namespacename=None, entityname=None):
	s = ansistyle.Text("&")
	if namespacename is not None:
		s.append(
			EnvTextForNamespace(EscInlineText(namespacename)),
			EnvTextForColon(":")
		)
	if entityname is None:
		entityname = "unnamed"
	s.append(
		EnvTextForEntityName(EscInlineText(entityname)),
		";"
	)
	return s

def strEntity(node):
	if hasattr(node, "namespace"):
		namespacename = node.namespace.prefix
	else:
		namespacename = None
	if hasattr(node, "name"):
		entityname = node.name
	else:
		entityname = node.__class__.__name__
	return strEntityName(namespacename, entityname)

def strProcInstTarget(target):
	return EnvTextForProcInstTarget(EscInlineText(target))

def strProcInstData(data):
	return EnvTextForProcInstData(EscInlineText(data))

def strTextOutsideAttr(text):
	return EnvTextForText(EscInlineText(text))

def strTextInAttr(text):
	return EnvTextForAttrValue(EscInlineAttr(text))

def strProcInst(node):
	if hasattr(node, "name"):
		target = node.name
	else:
		target = node.__class__.__name__
	return strProcInstTarget(target)

def strProcInstTargetWithBrackets(target):
	return ansistyle.Text(strBracketOpen(), strQuestion(), strProcInstTarget(target), strQuestion(), strBracketClose())

def strProcInstWithBrackets(node):
	return ansistyle.Text(strBracketOpen(), strQuestion(), strProcInst(node), strQuestion(), strBracketClose())

def strAttrName(attrname):
	return EnvTextForAttrName(EscInlineText(attrname))

def strAttrValue(attrvalue):
	return EnvTextForAttrValue(EscInlineAttr(attrvalue))

class NormalPresenter:
	def beginPresentation(self):
		self.buffer = ansistyle.Text()
		self.inAttr = 0

	def endPresentation(self):
		result = str(self.buffer)
		self.buffer = None
		return result

	def presentText(self, node):
		if self.inAttr:
			self.buffer.append(strTextInAttr(node._content))
		else:
			self.buffer.append(strTextOutsideAttr(node._content))

	def presentFrag(self, node):
		for child in node:
			child.present(self)

	def presentComment(self, node):
		self.buffer.append(
			strBracketOpen(),
			strExclamation(),
			strCommentMarker(),
			strCommentText(node._content),
			strCommentMarker(),
			strBracketClose()
		)

	def presentDocType(self, node):
		self.buffer.append(
			strBracketOpen(),
			strExclamation(),
			strDocTypeMarker(),
			" ",
			strDocTypeText(node._content),
			strBracketClose()
		)

	def presentProcInst(self, node):
		self.buffer.append(
			strBracketOpen(),
			strQuestion(),
			strProcInstTarget(node._target),
			" ",
			strProcInstData(node._content),
			strQuestion(),
			strBracketClose()
		)

	def _appendAttrs(self, dict):
		for attr in dict.keys():
			self.buffer.append(" ", strAttrName(attr))
			value = dict[attr]
			if len(value):
				self.buffer.append("=", strQuote())
				value.present(self)
				self.buffer.append(strQuote())

	def presentElement(self, node):
		if node.empty:
			self.buffer.append(strBracketOpen(), strElement(node))
			self._appendAttrs(node.attrs)
			self.buffer.append(strSlash(), strBracketClose())
		else:
			self.buffer.append(strBracketOpen(), strElement(node))
			self._appendAttrs(node.attrs)
			self.buffer.append(strBracketClose())
			for child in node:
				child.present(self)
			self.buffer.append(strBracketOpen(), strSlash(), strElement(node), strBracketClose())

	def presentEntity(self, node):
		self.buffer.append(strEntity(node))

	def presentNull(self, node):
		self.buffer.append(strBracketOpen(), strElement(node), strSlash(), strBracketClose())

	def presentAttr(self, node):
		xsc.Frag.present(node, self)

	def presentURLAttr(self, node):
		self.buffer.append(strURL(node.asString()))

class TreePresenter:
	def beginPresentation(self):
		self.inAttr = 0
		self.lines = []

	def endPresentation(self):
		buffer = ansistyle.Text()
		result = str(self.buffer)
		self.buffer = None
		return result

defaultPresenterClass = NormalPresenter
