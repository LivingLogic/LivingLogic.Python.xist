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

class StringBuffer:
	def __init__(self):
		self.buffer = []
	def write(self, text):
		self.buffer.append(text)
	def __str__(self):
		return "".join(self.buffer)

class Colored:
	"""
	a colored string, that may consist of
	many parts, some of them may be Colored
	objects themselves.
	"""
	color = 0x7 # default color

	def __init__(self, *texts):
		self.texts = texts

	def write(self, colorstream):
		colorstream.pushColor(self.color)
		for text in self.texts:
			if isinstance(text, Colored):
				text.write(colorstream)
			else:
				colorstream.write(text)
		colorstream.popColor()

	def __str__(self):
		buffer = StringBuffer()
		stream = ANSIColorStream(buffer)
		self.write(stream)
		stream.finish()
		return str(buffer)

class ANSIColorStream:
	"""
	adds color capability to an output stream. An ANSIColorStream
	keeps track of the current color and writes ANSI color escape
	sequences to the stream where appropriate. colors are numbers
	from 0 to 15.
	"""

	def __init__(self, stream):
		self._basestream = stream
		self._colorStack = [7]
		self._activeColor = 7

	def pushColor(self, color):
		"""
		push the color color onto the color stack.
		It becames the current color. Returning to
		the previous color is possible with
		popColor().
		"""
		self._colorStack.append(color)

	def popColor(self):
		"""
		return to the previous active color.
		"""
		self._colorStack.pop()

	def _switchColor(self, color):
		"""
		internal method: switches to the color color.
		If color is different from the currently active
		color, the appropriate ANSI escape sequence will
		be written to the stream.
		"""
		if self._activeColor != color:
			if color == 0x7:
				s = "0"
			else:
				s = ""
				if (self._activeColor&0x8) != (color&0x8):
					if color&0x8:
						s += "1;"
					else:
						s += "0;"
				s += str(30+(color&0x7))
			self._basestream.write("\033[" + s + "m")
			self._activeColor = color

	def write(self, *texts):
		"""
		writes the texts to the stream, and ensures,
		that the texts will be in the correct color.
		"""
		for text in texts:
			if isinstance(text, Colored):
				text.write(self)
			else:
				if len(text):
					self._switchColor(self._colorStack[-1])
					self._basestream.write(text)

	def writeWithColor(self, color, *texts):
		"""
		writes the texts in the color color
		and then switches back to the previos
		color.
		"""
		self.pushColor(color)
		self.write(*texts)
		self.popColor()

	def finish(self):
		"""
		can be called at the end of an output
		sequence to return to the default
		color.
		"""
		self._switchColor(7)

class NamedANSIColorStream(ANSIColorStream):
	"""
	Adds two features to the underlying ANSIColorStream:
	colors can be registered under a name, and the stream
	may have different modes, with a different collection
	of color (e.g. on set for light background and one
	set for dark background)
	"""

	def __init__(self, stream, mode=None):
		ANSIColorStream.__init__(self, stream)
		if mode is None:
			mode = options.repransi
		self.mode = mode
		self.colors = {}

	def registerColor(self, name, colors):
		self.colors[name] = colors

	def unregisterColor(self, name):
		del self.colors[name]

	def pushColor(self, colorName):
		if self.mode != 0:
			ANSIColorStream.pushColor(self, self.colors[colorName][self.mode-1])

	def popColor(self):
		if self.mode != 0:
			ANSIColorStream.popColor(self)

	def writeWithColor(self, colorName, *texts):
		if self.colors.has_key(colorName):
			self.pushColor(colorName)
			ANSIColorStream.write(self, *texts)
			self.popColor()
		else:
			print "writeWithColor:", colorName, self.mode, texts, "unknown color"
			ANSIColorStream.write(self, *texts)

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
		self.stream.registerColor("text", options.repransitext)
		self.stream.registerColor("tab", options.repransitab)
		self.stream.registerColor("namespace", options.repransinamespace)
		self.stream.registerColor("elementname", options.repransielementname)
		self.stream.registerColor("entityname", options.repransientityname)
		self.stream.registerColor("charref", options.repransicharref)
		self.stream.registerColor("bracket", options.repransibracket)
		self.stream.registerColor("colon", options.repransicolon)
		self.stream.registerColor("slash", options.repransislash)
		self.stream.registerColor("question", options.repransiquestion)
		self.stream.registerColor("exclamation", options.repransiexclamation)
		self.stream.registerColor("commentmarker", options.repransicommentmarker)
		self.stream.registerColor("commenttext", options.repransicommenttext)
		self.stream.registerColor("procinsttarget", options.repransiprocinsttarget)
		self.stream.registerColor("procinstdata", options.repransiprocinstdata)
		self.stream.registerColor("doctypemarker", options.repransidoctypemarker)
		self.stream.registerColor("doctypetext", options.repransidoctypetext)
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
