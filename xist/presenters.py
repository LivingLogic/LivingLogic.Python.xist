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

def getANSICodesFromEnv(name, default):
	"""
	parses an environment variable from a string list and returns it or
	the default if the environment variable can't be found or parsed.
	"""

class EnvText(color.Text):
	def __init__(self, *data):
		color.Text.__init__(self, *data)
		try:
			var = eval(os.environ[self.envname])
			if type(var) is types.StringType:
				var = [var, var]
			self.color = var
		except:
			self.color = self.default

	def getColor(self):
		if options.repransi==0:
			return 0x7
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
		self.refwhite = 0
		self.ansi = ansi

	def reset(self):
		self.buffer = StringBuffer()
		self.stream = NamedANSIColorStream(self.buffer, self.ansi)
		self.inAttr = 0

	def _colorText(self, text):
		v = [] # collect all colored string here
		for c in text:
			oc = ord(c)
			ascharref = (oc <= 31) or (128 <= oc <= 159)
			if not ascharref:
				try:
					c.encode(self.encoding)
				except UnicodeError:
					ascharref = 1
			if (c == "\n" or c == "\t") and not self.refwhite:
				self.stream.writeWithColor("tab", c)
			elif ascharref:
				entity = self.namespaces.entityFromNumber(oc)
				if entity is not None:
					self.stream.writeWithColor("charref", "&", entity.name, ";")
				else:
					self.stream.writeWithColor("charref", "&#", str(oc), ";")
			else:
				self.stream.write(c.encode(self.encoding))

	def writeElement(self, node):
		if hasattr(node, "namespace"):
			self.stream.pushColor("namespace")
			self._colorText(node.namespace.prefix)
			self.stream.popColor()
			self.writeColon()
		if hasattr(node, "name"):
			name = node.name
		else:
			name = node.__class__.name
		self.stream.pushColor("elementname")
		self._colorText(name)
		self.stream.popColor()

	def writeEntity(self, node):
		self.stream.write("&")
		if hasattr(node, "namespace"):
			self.stream.pushColor("namespace")
			self._colorText(node.namespace.prefix)
			self.writeColon()
			self.stream.popColor()
		if hasattr(node, "name"):
			name = node.name
		else:
			name = node.__class__.name
		self.stream.pushColor("entityname")
		self._colorText(name)
		self.stream.popColor()
		self.stream.write(";")

	def writeAttrName(self, attrname):
		self.stream.pushColor("attrname")
		self._colorText(attrname)
		self.stream.popColor()

	def writeAttrValue(self, attrvalue):
		self.buffer.pushColor("attrvalue")
		self._colorText(attrvalue)
		self.buffer.popColor()

	def writeDocTypeMarker(self):
		self.stream.pushColor("doctypemarker")
		self.stream.write("DOCTYPE")
		self.stream.popColor()

	def writeDocTypeText(self, text):
		self.stream.pushColor("doctypetext")
		self._colorText(text)
		self.stream.popColor()

	def writeCommentMarker(self):
		self.stream.pushColor("commentmarker")
		self.stream.write("--")
		self.stream.popColor()

	def writeCommentText(self, text):
		self.stream.pushColor("commenttext")
		self._colorText(text)
		self.stream.popColor()

	def writeProcInstTarget(self, target):
		self.stream.pushColor("procinsttarget")
		self._colorText(target)
		self.stream.popColor()

	def writeProcInstData(self, data):
		self.stream.pushColor("procinstdata")
		self._colorText(data)
		self.stream.popColor()

	def writeText(self, text):
		self.stream.pushColor("text")
		self._colorText(text)
		self.stream.popColor()

	def writeSlash(self):
		self.stream.writeWithColor("slash", "/")

	def writeBracketOpen(self):
		self.stream.writeWithColor("bracket", "<")

	def writeBracketClose(self):
		self.stream.writeWithColor("bracket", ">")

	def writeColon(self):
		self.stream.writeWithColor("colon", ":")

	def writeQuestion(self):
		self.stream.writeWithColor("question", "?")

	def writeExclamation(self):
		self.stream.writeWithColor("exclamation", "!")

	def writeQuote(self):
		self.stream.writeWithColor("quote", '"')

	def writeTab(self, count):
		self.stream.writeWithColor("tab", options.reprtab*count)

	def writeURL(self, url):
		self.stream.pushColor("url")
		self._colorText(url)
		self.stream.popColor()

	def _colorAttrs(self, dict):
		v = []
		for attr in dict.keys():
			v.append(" ")
			v.append(self.strAttrName(attr))
			value = dict[attr]
			if len(value):
				v.append('=')
				v.append(self.strQuote())
				v.append(self.strAttrValue(value.asPlainString().encode(self.encoding)))
				v.append(self.strQuote())
		return "".join(v)

class NormalPresenter(Presenter):
	def __init__(self, encoding=None, ansi=None):
		Presenter.__init__(self, encoding, ansi)
		self.refwhite = 0

	def beginPresentation(self):
		self.reset()

	def endPresentation(self):
		self.stream.finish()
		result = str(self.buffer)
		self.reset()
		return result

	def presentText(self, node):
		self.writeText(node._content)

	def presentFrag(self, node):
		for child in node:
			child.present(self)

	def presentComment(self, node):
		self.writeBracketOpen()
		self.writeExclamation()
		self.writeCommentMarker()
		self.writeCommentText(node._content)
		self.writeCommentMarker()
		self.writeBracketClose()

	def presentDocType(self, node):
		self.writeBracketOpen()
		self.writeExclamation()
		self.writeDocTypeMarker()
		self.buffer.write(" ")
		self.writeDocTypeText(node._content)
		self.writeBracketClose()

	def presentProcInst(self, node):
		self.writeBracketOpen()
		self.writeQuestion()
		self.writeProcInstTarget(node._target)
		self.buffer.write(" ")
		self.writeProcInstData(node._content)
		self.writeQuestion()
		self.writeBracketClose()

	def presentElement(self, node):
		if node.empty:
			self.writeBracketOpen()
			self.writeElement(node)
			self.writeSlash()
			self.writeBracketClose()
		else:
			self.writeBracketOpen()
			self.writeElement(node)
			self.writeBracketClose()
			for child in node:
				child.present(self)
			self.writeBracketOpen()
			self.writeSlash()
			self.writeElement(node)
			self.writeBracketClose()

	def presentEntity(self, node):
		self.writeEntity(node)

	def presentNull(self, node):
		self.writeBracketOpen()
		self.writeElement(node)
		self.writeSlash()
		self.writeBracketClose()

	def presentAttr(self, node):
		ansi = self.ansi
		self.ansi = 0
		self.v.append(self.strAttrValue(xsc.Frag.present(node, self)))
		self.ansi = ansi

	def presentURLAttr(self, node):
		self.v.append(self.strURL(node.asString()))

defaultPresenterClass = NormalPresenter
