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
import xsc, options

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
	try:
		var = eval(os.environ[name])
	except:
		return default
	if type(var) is types.StringType:
		var = [var, var]
	return var

class ANSIStringBuffer:
	"""
	simplifies handling ANSI colors
	"""

	def __init__(self, ansi=None):
		if ansi is None:
			ansi = options.repransi
		self.ansi = ansi
		self.buffer = []
		self.colorStack = [(7,7)]
		self.activeColor = 7

	def pushColor(self, color):
		self.colorStack.append(color)

	def popColor(self):
		self.colorStack.pop()

	def _switchColor(self, *colors):
		color = colors[self.ansi-1]
		if self.activeColor != color:
			if color == 0x7:
				s = "\033[0m"
			s = "\033[0"
			if color != 0x7:
				if color&0x8:
					s += ";1"
				s += ";" + str(30+(color&0x7))
			s += "m"
			self.buffer.append(s)
			self.activeColor = color

	def write(self, *texts):
		if self.ansi:
			self._switchColor(*self.colorStack[-1])
		self.buffer.extend(texts)

	def __str__(self):
		if self.ansi:
			self._switchColor(7,7)
		return "".join(self.buffer)

class Presenter:
	"""
	base class for all presenters.
	"""

	def __init__(self, encoding=None, ansi=None):
		if encoding is None:
			encoding = options.reprEncoding
		self.encoding = encoding
		self.refwhite = 0
		self.ansi = ansi
		self.reset()

	def reset(self):
		self.buffer = ANSIStringBuffer(self.ansi)
		self.inAttr = 0

	def _colorText(self, text):
		# we could put ANSI escapes around every character or reference that we output,
		# but this would result in strings that are way to long, especially if output
		# over a serial connection, so we collect runs of characters with the same
		# highlighting and put the ANSI escapes around those. (of course, when we're
		# not doing highlighting, this routine does way to much useless calculations)
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
				self.buffer.pushColor(options.repransitab)
				self.buffer.write(c)
				self.buffer.popColor()
			elif ascharref:
				self.buffer.pushColor(options.repransicharref)
				self.buffer.write("&#" + str(oc) + ";")
				self.buffer.popColor()
			else:
				self.buffer.write(c.encode(self.encoding))

	def writeElement(self, node):
		if hasattr(node, "namespace"):
			self.buffer.pushColor(options.repransinamespace)
			self._colorText(node.namespace.prefix)
			self.buffer.popColor()
			self.writeColon()
		if hasattr(node, "name"):
			name = node.name
		else:
			name = node.__class__.name
		self.buffer.pushColor(options.repransinamespace)
		self._colorText(name)
		self.buffer.popColor()

	def writeEntity(self, node):
		self.buffer.write("&")
		if hasattr(node, "namespace"):
			self.buffer.pushColor(options.repransinamespace)
			self._colorText(node.namespace.prefix)
			self.writeColon()
			self.buffer.popColor()
		if hasattr(node, "name"):
			name = node.name
		else:
			name = node.__class__.name
		self.buffer.pushColor(options.repransientityname)
		self._colorText(name)
		self.buffer.popColor()
		self.buffer.write(";")

	def writeAttrName(self, attrname):
		self.buffer.pushColor(options.repransiattrname)
		self._colorText(attrname)
		self.buffer.popColor()

	def writeAttrValue(self, attrvalue):
		self.buffer.pushColor(options.repransiattrvalue)
		self._colorText(attrvalue)
		self.buffer.popColor()

	def writeDocTypeMarker(self):
		self.buffer.pushColor(options.repransidoctypemarker)
		self.buffer.write("DOCTYPE")
		self.buffer.popColor()

	def writeDocTypeText(self, text):
		self.buffer.pushColor(options.repransidoctypetext)
		self._colorText(text)
		self.buffer.popColor()

	def writeCommentMarker(self):
		self.buffer.pushColor(options.repransicommentmarker)
		self.buffer.write("--")
		self.buffer.popColor()

	def writeCommentText(self, text):
		self.buffer.pushColor(options.repransicommenttext)
		self._colorText(text)
		self.buffer.popColor()

	def writeProcInstTarget(self, target):
		self.buffer.pushColor(options.repransiprocinsttarget)
		self._colorText(target)
		self.buffer.popColor()

	def writeProcInstData(self, data):
		self.buffer.pushColor(options.repransiprocinstdata)
		self._colorText(data)
		self.buffer.popColor()

	def writeText(self, text):
		self.buffer.pushColor(options.repransitext)
		self._colorText(text)
		self.buffer.popColor()

	def writeSlash(self):
		self.buffer.pushColor(options.repransislash)
		self.buffer.write("/")
		self.buffer.popColor()

	def writeBracketOpen(self):
		self.buffer.pushColor(options.repransibracket)
		self.buffer.write("<")
		self.buffer.popColor()

	def writeBracketClose(self):
		self.buffer.pushColor(options.repransibracket)
		self.buffer.write(">")
		self.buffer.popColor()

	def writeColon(self):
		self.buffer.pushColor(options.repransicolon)
		self.buffer.write(":")
		self.buffer.popColor()

	def writeQuestion(self):
		self.buffer.pushColor(options.repransiquestion)
		self.buffer.write("?")
		self.buffer.popColor()

	def writeExclamation(self):
		self.buffer.pushColor(options.repransiexclamation)
		self.buffer.write("!")
		self.buffer.popColor()

	def writeQuote(self):
		self.buffer.pushColor(options.repransiquote)
		self.buffer.write('"')
		self.buffer.popColor()

	def writeTab(self, count):
		self.buffer.pushColor(options.repransitab)
		self.buffer.write(options.reprtab*count)
		self.buffer.popColor()

	def writeURL(self, url):
		self.buffer.pushColor(options.repransiurl)
		self._colorText(url)
		self.buffer.popColor()

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
