#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter D�rwald
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

import os, types, keyword

import ansistyle

import xsc, options, url

def getStringFromEnv(name, default):
	try:
		return os.environ[name]
	except KeyError:
		return default

def getIntFromEnv(name, default):
	try:
		return int(os.environ[name])
	except KeyError:
		return default

def getColorsFromEnv(name, default):
	try:
		var = eval(os.environ[name])
		if type(var) is types.StringType:
			var = (var, var)
		return var
	except KeyError:
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
	color = getColorsFromEnv("XSC_REPRANSI_TAB", (0x4, 0x8))

class EnvTextForQuote(EnvText):
	"""
	ANSI escape sequence to be used for quotes
	(delimiters for text and attribute nodes)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_QUOTE", (0x3, 0xf))

class EnvTextForSlash(EnvText):
	color = getColorsFromEnv("XSC_REPRANSI_SLASH", (0x3, 0xf))

class EnvTextForBracket(EnvText):
	"""
	ANSI escape sequence to be used for quotes
	(delimiters for text and attribute nodes)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_BRACKET", (0x3, 0xf))

class EnvTextForColon(EnvText):
	"""
	ANSI escape sequence to be used for colon
	(i.e. namespace separator)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_BRACKET", (0x3, 0xf))

class EnvTextForQuestion(EnvText):
	"""
	ANSI escape sequence to be used for question marks
	(delimiters for processing instructions)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_QUESTION", (0x3, 0xf))

class EnvTextForExclamation(EnvText):
	"""
	ANSI escape sequence to be used for exclamation marks
	(used in comments and doctypes)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_EXCLAMATION", (0x3, 0xf))

class EnvTextForText(EnvText):
	"""
	ANSI escape sequence to be used for text
	"""
	color = getColorsFromEnv("XSC_REPRANSI_TEXT", (0x7, 0x7))

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
	color = getColorsFromEnv("XSC_REPRANSI_ENTITYNAME", (0x5, 0x5))

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

class EnvTextForProcInstContent(EnvText):
	"""
	ANSI escape sequence to be used for processing instruction content
	"""
	color = getColorsFromEnv("XSC_REPRANSI_PROCINSTCONTENT", (0x7, 0x7))

class EnvTextForNumber(EnvText):
	"""
	ANSI escape sequence to be used for numbers in error messages etc.
	"""
	color = getColorsFromEnv("XSC_REPRANSI_NUMBER", (0x4, 0x4))

class EnvTextForString(EnvText):
	"""
	ANSI escape sequence to be used for variable strings in error messages etc.
	"""
	color = getColorsFromEnv("XSC_REPRANSI_STRING", (0x5, 0x5))

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
				entity = xsc.defaultNamespaces.charrefFromNumber(charcode)
				if entity is not None:
					return EnvTextForEntityName("&", entity.name, ";")
				else:
					return EnvTextForEntityName("&#", str(charcode), ";")
		return char

class EscInlineAttr(EscInlineText):
	ascharref = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f<>\"&"
	ascolor   = "\x09\x0a"

class EscOutlineText(EscInlineText):
	ascharref = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f<>&"
	ascolor   = ""

class EscOutlineAttr(EscInlineText):
	ascharref = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f<>\"&"
	ascolor   = ""

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

def strNumber(number):
	return EnvTextForNumber(str(number))

def strString(string):
	return EnvTextForString(string)

def strURL(u):
	if isinstance(u, url.URL):
		u = u.asString()
	return EnvTextForURL(EscInlineText(u))

def strDocTypeMarker():
	return EnvTextForDocTypeMarker("DOCTYPE")

def strDocTypeText(text):
	return EnvTextForDocTypeText(EscInlineText(text))

def strCommentMarker():
	return EnvTextForCommentMarker("--")

def strCommentText(text):
	return EnvTextForCommentText(EscInlineText(text))

def strElementName(namespacename=None, elementname=None, slash=0):
	s = ansistyle.Text()
	if slash<0:
		s.append(EnvTextForSlash("/"))
	if namespacename is not None:
		s.append(
			EnvTextForNamespace(EscInlineText(namespacename)),
			EnvTextForColon(":")
		)
	if elementname is None:
		elementname = "unnamed"
	s.append(EnvTextForElementName(EscInlineText(elementname)))
	if slash>0:
		s.append(EnvTextForSlash("/"))
	return s

def strElementNameWithBrackets(namespacename=None, elementname=None, slash=0):
	return ansistyle.Text(strBracketOpen(), strElementName(namespacename, elementname, slash), strBracketClose())

def strElementClass(class_, slash=0):
	namespacename = None
	if class_.presentPrefix!=0:
		namespacename = class_.prefix()
	return strElementName(namespacename, class_.name, slash)

def strElementClassWithBrackets(class_, slash=0):
	return ansistyle.Text(strBracketOpen(), strElementClass(class_, slash), strBracketClose())

def strElement(node, slash=0):
	return strElementClass(node.__class__, slash)

def strElementWithBrackets(node, slash=0):
	return strElementClassWithBrackets(node.__class__, slash)

def strEntityName(namespacename=None, entityname=None):
	s = EnvTextForEntityName("&")
	if namespacename is not None:
		s.append(EscInlineText(namespacename), ":")
	if entityname is None:
		entityname = "unnamed"
	s.append(EscInlineText(entityname), ";")
	return s

def strEntity(node):
	if node.presentPrefix!=0:
		namespacename = node.prefix()
	else:
		namespacename = None
	return strEntityName(namespacename, node.name)

def strProcInstTarget(namespacename=None, target=None):
	s = ansistyle.Text()
	if namespacename is not None:
		if namespacename=="":
			namespacename = "unnamed"
		s.append(
			EnvTextForNamespace(EscInlineText(namespacename)),
			EnvTextForColon(":")
		)
	if target is None:
		target = "unnamed"
	s.append(EnvTextForProcInstTarget(EscInlineText(target)))
	return s

def strProcInstContent(content):
	return EnvTextForProcInstContent(EscInlineText(content))

def strTextOutsideAttr(text):
	return EnvTextForText(EscInlineText(text))

def strTextInAttr(text):
	return EnvTextForAttrValue(EscInlineAttr(text))

def strProcInst(node):
	if node.presentPrefix!=0:
		namespacename = node.prefix()
	else:
		namespacename = None
	return strProcInstTarget(namespacename, node.name)

def strProcInstTargetWithBrackets(namespacename=None, target=None):
	return ansistyle.Text(strBracketOpen(), strQuestion(), strProcInstTarget(namespacename, target), strQuestion(), strBracketClose())

def strProcInstWithBrackets(node):
	return ansistyle.Text(strBracketOpen(), strQuestion(), strProcInst(node), strQuestion(), strBracketClose())

def strAttrName(attrname):
	return EnvTextForAttrName(EscInlineText(attrname))

def strAttrValue(attrvalue):
	return EnvTextForAttrValue(EscInlineAttr(attrvalue))

class Presenter:
	"""
	<doc:par>This class is the base of the presenter classes. It is abstract
	and only serves as documentation for the methods.</doc:par>
	<doc:par>A <class>Presenter</class> generates a specific
	string representation of a node to be printed on the screen.</doc:par>
	"""

	def beginPresentation(self):
		"""
		<doc:par>called by the <pyref module="xist.xsc" class="Node">node</pyref> once
		at the start when <pyref module="xist.xsc" class="Node" method="repr"><method>repr</method></pyref>
		is called. Initializes the presenter.</doc:par>
		"""
		raise NotImplementedError("beginPresentation")

	def endPresentation(self):
		"""
		<doc:par>called by the <pyref module="xist.xsc" class="Node">node</pyref> after
		the call to <pyref module="xist.xsc" class="Node" method="present"><method>present</method></pyref>.
		This method handles cleanups if necessary and returns the string to be printed.</doc:par>
		"""
		raise NotImplementedError("endPresentation")

	def presentText(self, node):
		"""
		<doc:par>present a <pyref module="xist.xsc" class="Text"><class>Text</class></pyref> node.</doc:par>
		"""
		raise NotImplementedError("presentText")

	def presentFrag(self, node):
		"""
		<doc:par>present a <pyref module="xist.xsc" class="Frag"><class>Frag</class></pyref> node.</doc:par>
		"""
		raise NotImplementedError("presentFrag")

	def presentComment(self, node):
		"""
		<doc:par>present a <pyref module="xist.xsc" class="Comment"><class>Comment</class></pyref> node.</doc:par>
		"""
		raise NotImplementedError("presentComment")

	def presentDocType(self, node):
		"""
		<doc:par>present a <pyref module="xist.xsc" class="DocType"><class>DocType</class></pyref> node.</doc:par>
		"""
		raise NotImplementedError("presentDocType")

	def presentProcInst(self, node):
		"""
		<doc:par>present a <pyref module="xist.xsc" class="ProcInst"><class>ProcInst</class></pyref> node.</doc:par>
		"""
		raise NotImplementedError("presentProcInst")

	def presentAttrs(self, node):
		"""
		<doc:par>present an <pyref module="xist.xsc" class="Attrs"><class>Attrs</class></pyref> node.</doc:par>
		"""
		raise NotImplementedError("presentAttrs")

	def presentElement(self, node):
		"""
		<doc:par>present an <pyref module="xist.xsc" class="Element"><class>Element</class></pyref> node.</doc:par>
		"""
		raise NotImplementedError("presentElement")

	def presentEntity(self, node):
		"""
		<doc:par>present a <pyref module="xist.xsc" class="Entity"><class>Entity</class></pyref> node.</doc:par>
		"""
		raise NotImplementedError("presentEntity")

	def presentNull(self, node):
		"""
		<doc:par>present the <class>Null</class> node.</doc:par>
		"""
		raise NotImplementedError("presentNull")

	def presentAttr(self, node):
		"""
		<doc:par>present an <pyref module="xist.xsc" class="Attr"><class>Attr</class></pyref> node.</doc:par>
		"""
		raise NotImplementedError("presentAttr")

	def presentURLAttr(self, node):
		"""
		<doc:par>present an <pyref module="xist.xsc" class="URLAttr"><class>URLAttr</class></pyref> node.</doc:par>
		"""
		raise NotImplementedError("presentURLAttr")

class PlainPresenter(Presenter):
	"""
	<doc:par>This presenter shows only the root node of the tree (with a little additional
	information about the number of nested nodes). It is used as the default presenter
	in <pyref module="xist.xsc" class="Node" method="__repr__"><method>Node.__repr__</method></pyref>.</doc:par>
	"""
	def __init__(self, maxlen=60):
		self.maxlen = maxlen

	def beginPresentation(self):
		self.buffer = None

	def endPresentation(self):
		result = self.buffer
		self.buffer = None
		return result

	def presentCharacterData(self, node):
		if len(node)>self.maxlen:
			content = node.content[:self.maxlen/2] + u"..." + node.content[-self.maxlen/2:]
		else:
			content = node.content
		self.buffer = "<%s.%s instance content=%r at 0x%x>" % (node.__class__.__module__, node.__class__.__name__, content, id(node))

	presentText = presentCharacterData

	def presentFrag(self, node):
		l = len(node)
		if l==0:
			info = "with no children"
		elif l==1:
			info = "with 1 child"
		else:
			info = "with %d children" % l
		self.buffer = "<%s.%s instance %s at 0x%x>" % (node.__class__.__module__, node.__class__.__name__, info, id(node))

	presentComment = presentCharacterData
	presentDocType = presentCharacterData
	presentProcInst = presentCharacterData

	def presentAttrs(self, node):
		l = len(node)
		if l==0:
			info = "with no attributes"
		elif l==1:
			info = "with 1 attributes"
		else:
			info = "with %d attributes" % l
		self.buffer = "<%s.%s instance %s at 0x%x>" % (node.__class__.__module__, node.__class__.__name__, info, id(node))

	def presentElement(self, node):
		lc = len(node.content)
		if lc==0:
			infoc = "with no children"
		elif lc==1:
			infoc = "with 1 child"
		else:
			infoc = "with %d children" % lc
		la = len(node.attrs)
		if la==0:
			infoa = "and no attrs"
		elif la==1:
			infoa = "and 1 attr"
		else:
			infoa = "and %d attrs" % lc
		self.buffer = "<%s.%s instance %s %s at 0x%x>" % (node.__class__.__module__, node.__class__.__name__, infoc, infoa, id(node))

	def presentEntity(self, node):
		self.buffer = "<%s.%s instance at 0x%x>" % (node.__class__.__module__, node.__class__.__name__, id(node))

	def presentNull(self, node):
		self.buffer = "<%s.%s instance at 0x%x>" % (node.__class__.__module__, node.__class__.__name__, id(node))

	presentAttr = presentFrag
	presentURLAttr = presentAttr

class NormalPresenter(Presenter):
	def beginPresentation(self):
		self.buffer = ansistyle.Text()
		self.inAttr = 0

	def endPresentation(self):
		result = str(self.buffer)
		self.buffer = None
		return result

	def presentText(self, node):
		if self.inAttr:
			self.buffer.append(strTextInAttr(node.content))
		else:
			self.buffer.append(strTextOutsideAttr(node.content))

	def presentFrag(self, node):
		for child in node:
			child.present(self)

	def presentComment(self, node):
		self.buffer.append(
			strBracketOpen(),
			strExclamation(),
			strCommentMarker(),
			strCommentText(node.content),
			strCommentMarker(),
			strBracketClose()
		)

	def presentDocType(self, node):
		self.buffer.append(
			strBracketOpen(),
			strExclamation(),
			strDocTypeMarker(),
			" ",
			strDocTypeText(node.content),
			strBracketClose()
		)

	def presentProcInst(self, node):
		self.buffer.append(
			strBracketOpen(),
			strQuestion(),
			strProcInst(node),
			" ",
			strProcInstContent(node.content),
			strQuestion(),
			strBracketClose()
		)

	def presentAttrs(self, node):
		for (attrname, attrvalue) in node.items():
			self.buffer.append(" ", strAttrName(attrname), "=", strQuote())
			attrvalue.present(self)
			self.buffer.append(strQuote())

	def presentElement(self, node):
		if node.empty:
			self.buffer.append(strBracketOpen(), strElement(node))
			node.attrs.present(self)
			self.buffer.append(strSlash(), strBracketClose())
		else:
			self.buffer.append(strBracketOpen(), strElement(node))
			node.attrs.present(self)
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

class TreePresenter(Presenter):
	"""
	This presenter shows the object as a nested tree.
	"""
	def __init__(self, showLocation=1, showPath=1):
		self.showLocation = showLocation
		self.showPath = showPath

	def beginPresentation(self):
		self.inAttr = 0
		self.lines = [] # the final lines consisting of (location, numerical path, nesting, content)
		self.currentPath = [] # numerical path
		self.buffers = [] # list of ansistyle.Text objects used for formatting attributes (this is a list for elements that contains elements in their attributes)

	def endPresentation(self):
		lenloc = 0
		lennumpath = 0
		for line in self.lines:
			if self.showPath:
				line[1] = ".".join(map(str, line[1]))
			line[3] = ansistyle.Text(strTab(line[2]), line[3])
			if self.showLocation:
				if line[0] is not None:
					line[0] = str(line[0])
					lenloc = max(lenloc, len(line[0]))
				else:
					line[0] = str(xsc.Location())
			lennumpath = max(lennumpath, len(line[1]))
		newlines = []
		for line in self.lines:
			if self.showLocation:
				newlines.append("%-*s " % (lenloc, line[0]))
			if self.showPath:
				newlines.append("%-*s " % (lennumpath, line[1]))
			newlines.append("%s\n" % line[3])
		self.lines = []
		return "".join(newlines)

	def _doMultiLine(self, node, lines, indent, formatter, head=None, tail=None):
		loc = node.startLoc
		nest = len(self.currentPath)
		l = len(lines)
		for i in xrange(l):
			if loc is not None:
				hereloc = loc.offset(i)
			else:
				hereloc = None
			mynest = nest
			s = lines[i]
			if isinstance(s, (str, unicode)):
				if indent:
					while len(s) and s[0] == "\t":
						mynest += 1
						s = s[1:]
			s = formatter(s)
			if i == 0 and head is not None:
				s.content.insert(0, head)
			if i == l-1 and tail is not None:
				s.content.append(tail)
			self.lines.append([hereloc, self.currentPath[:], mynest, s])

	def strTextLineOutsideAttr(self, text):
		return ansistyle.Text(strQuote(), EnvTextForText(EscOutlineText(text)), strQuote())

	def strTextInAttr(self, text):
		return EnvTextForAttrValue(EscOutlineAttr(text))

	def strProcInstContentLine(self, text):
		return EnvTextForProcInstContent(EscOutlineText(text))

	def strCommentTextLine(self, text):
		return EnvTextForCommentText(EscOutlineText(text))

	def strDocTypeTextLine(self, text):
		return EnvTextForDocTypeText(EscOutlineText(text))

	def presentFrag(self, node):
		if self.inAttr:
			for child in node:
				child.present(self)
		else:
			if len(node):
				self.lines.append([node.startLoc, self.currentPath[:], len(self.currentPath), strElementWithBrackets(node, 0)])
				self.currentPath.append(0)
				for child in node:
					child.present(self)
					self.currentPath[-1] += 1
				del self.currentPath[-1]
				self.lines.append([node.endLoc, self.currentPath[:], len(self.currentPath), strElementWithBrackets(node, -1)])
			else:
				self.lines.append([node.startLoc, self.currentPath[:], len(self.currentPath), strElementWithBrackets(node, 1)])

	def presentAttrs(self, node):
		if self.inAttr:
			for (attrname, attrvalue) in node.items():
				self.buffers[-1].append(" ", strAttrName(attrname), "=", strQuote())
				attrvalue.present(self)
				self.buffers[-1].append(strQuote())
		else:
			s = ansistyle.Text(strBracketOpen(), strElement(node), strBracketClose())
			self.lines.append([node.startLoc, self.currentPath[:], len(self.currentPath), s])
			self.currentPath.append(None)
			for (attrname, attrvalue) in node.items():
				self.currentPath[-1] = attrname
				attrvalue.present(self)
			self.currentPath.pop()
			s = ansistyle.Text(strBracketOpen(), strSlash(), strElement(node), strBracketClose())
			self.lines.append([node.endLoc, self.currentPath[:], len(self.currentPath), s])

	def presentElement(self, node):
		if self.inAttr:
			self.buffers[-1].append(strBracketOpen(), strElement(node))
			self.inAttr += 1
			node.attrs.present(self)
			self.inAttr -= 1
			if len(node):
				self.buffers[-1].append(strBracketClose())
				node.content.present(self)
				self.buffers[-1].append(strBracketOpen(), strSlash(), strElement(node), strBracketClose())
			else:
				self.buffers[-1].append(strSlash(), strBracketClose())
		else:
			self.buffers.append(ansistyle.Text(strBracketOpen(), strElement(node)))
			self.inAttr += 1
			node.attrs.present(self)
			self.inAttr -= 1
			if len(node):
				self.buffers[-1].append(strBracketClose())
				self.lines.append([node.startLoc, self.currentPath[:], len(self.currentPath), ansistyle.Text(*self.buffers)])
				self.buffers = [] # we're done with the buffers for the header
				self.currentPath.append(0)
				for child in node:
					child.present(self)
					self.currentPath[-1] += 1
				self.currentPath.pop()
				self.lines.append([node.endLoc, self.currentPath[:], len(self.currentPath), strElementWithBrackets(node, -1)])
			else:
				self.buffers[-1].append(strSlash(), strBracketClose())
				self.lines.append([node.startLoc, self.currentPath[:], len(self.currentPath), ansistyle.Text(*self.buffers)])
				self.buffers = [] # we're done with the buffers for the header

	def presentNull(self, node):
		if self.inAttr:
			pass
		else:
			s = ansistyle.Text(strBracketOpen(), strElement(node), strSlash(), strBracketClose())
			self.lines.append([node.startLoc, self.currentPath[:], len(self.currentPath), s])

	def presentText(self, node):
		if self.inAttr:
			self.buffers[-1].append(strTextInAttr(node.content))
		else:
			lines = node.content.splitlines(1)
			self._doMultiLine(node, lines, 0, self.strTextLineOutsideAttr)

	def presentEntity(self, node):
		if self.inAttr:
			self.buffers[-1].append(strEntity(node))
		else:
			self.lines.append([node.startLoc, self.currentPath[:], len(self.currentPath), strEntity(node)])

	def presentProcInst(self, node):
		if self.inAttr:
			self.buffers[-1].append(
				strBracketOpen(),
				strQuestion(),
				strProcInst(node),
				" ",
				EnvTextForProcInstContent(EscOutlineAttr(node.content)),
				strQuestion(),
				strBracketClose()
			)
		else:
			head = ansistyle.Text(strBracketOpen(), strQuestion(), strProcInst(node), " ")
			tail = ansistyle.Text(strQuestion(), strBracketClose())
			lines = node.content.splitlines()
			if len(lines)>1:
				lines.insert(0, "")
			self._doMultiLine(node, lines, 1, self.strProcInstContentLine, head, tail)

	def presentComment(self, node):
		if self.inAttr:
			self.buffers[-1].append(
				strBracketOpen(),
				strExclamation(),
				strCommentMarker(),
				EnvTextForCommentText(EscOutlineAttr(node.content)),
				strCommentMarker(),
				strBracketClose()
			)
		else:
			head = ansistyle.Text(strBracketOpen(), strExclamation(), strCommentMarker())
			tail = ansistyle.Text(strCommentMarker(), strBracketClose())
			lines = node.content.splitlines()
			self._doMultiLine(node, lines, 1, self.strCommentTextLine, head, tail)

	def presentDocType(self, node):
		if self.inAttr:
			self.buffers[-1].append(
				strBracketOpen(),
				strExclamation(),
				strDocTypeMarker(),
				" ",
				EnvTextForDocTypeText(EscOutlineAttr(node.content)),
				strBracketClose()
			)
		else:
			head = ansistyle.Text(strBracketOpen(), strExclamation(), strDocTypeMarker(), " ")
			tail = ansistyle.Text(strBracketClose())
			lines = node.content.splitlines()
			self._doMultiLine(node, lines, 1, self.strDocTypeTextLine, head, tail)

	def presentAttr(self, node):
		if self.inAttr:
			# this will not be popped at the and of this method, because presentElement needs it
			self.buffers.append(EnvTextForAttrValue())
		self.presentFrag(node)

	def presentURLAttr(self, node):
		if self.inAttr:
			self.buffers.append(EnvTextForURL())
		self.presentFrag(node)

class CodePresenter(Presenter):
	"""
	<doc:par>This presenter formats the object as a nested Python object tree.</doc:par>
	
	<doc:par>This makes it possible to quickly convert &html;/&xml; files to &xist;
	constructor calls.</doc:par>
	"""
	def beginPresentation(self):
		self.inAttr = 0
		self.buffer = []
		self.level = 0

	def endPresentation(self):
		s = "".join(self.buffer)
		self.buffer = []
		return s

	def _indent(self):
		if not self.inAttr:
			if self.buffer:
				self.buffer.append("\n")
			if self.level:
				self.buffer.append("\t"*self.level)

	def _text(self, text):
		try:
			s = text.encode("us-ascii")
		except UnicodeError:
			s = text
		try:
			i = int(s)
		except ValueError:
			pass
		else:
			if str(i) == s:
				s = i
		return s

	def presentFrag(self, node):
		self._indent()
		if not self.inAttr:
			self.buffer.append("xsc.Frag")
		self.buffer.append("(")
		if len(node):
			i = 0
			self.level += 1
			for child in node:
				if i:
					self.buffer.append(",")
					if self.inAttr:
						self.buffer.append(" ")
				child.present(self)
				i += 1
			self.level -= 1
			self._indent()
		self.buffer.append(")")

	def presentAttrs(self, node):
		self._indent()
		self.buffer.append("{")
		self.level += 1
		i = 0
		for (attrname, attrvalue) in node.items():
			if i:
				self.buffer.append(",")
				if self.inAttr:
					self.buffer.append(" ")
			self._indent()
			self.inAttr += 1
			if keyword.iskeyword(attrname):
				attrname += "_"
			self.buffer.append("%r: " % attrname)
			if len(attrvalue)==1: # optimize away the tuple ()
				attrvalue[0].present(self)
			else:
				attrvalue.present(self)
			self._indent()
			self.inAttr -= 1
			i += 1
		self.level -= 1
		self._indent()
		self.buffer.append("}")

	def presentElement(self, node):
		self._indent()
		self.buffer.append("%s.%s(" % (node.__module__, node.__class__.__name__))
		if len(node.content) or len(node.attrs):
			i = 0
			self.level += 1
			for child in node:
				if i:
					self.buffer.append(",")
					if self.inAttr:
						self.buffer.append(" ")
				child.present(self)
				i += 1
			for (attrname, attrvalue) in node.attrs.items():
				if i:
					self.buffer.append(",")
					if self.inAttr:
						self.buffer.append(" ")
				self._indent()
				self.inAttr += 1
				if keyword.iskeyword(attrname):
					attrname += "_"
				self.buffer.append("%s=" % attrname)
				if len(attrvalue)==1: # optimize away the tuple ()
					attrvalue[0].present(self)
				else:
					attrvalue.present(self)
				self.inAttr -= 1
				i += 1
			self.level -= 1
			self._indent()
		self.buffer.append(")")

	def presentNull(self, node):
		pass

	def presentText(self, node):
		self._indent()
		self.buffer.append("%r" % self._text(node.content))

	def presentEntity(self, node):
		self._indent()
		self.buffer.append("%s.%s()" % (node.__module__, node.__class__.__name__))

	def presentProcInst(self, node):
		self._indent()
		self.buffer.append("%s.%s(%r)" % (node.__module__, node.__class__.__name__, self._text(node.content)))

	def presentComment(self, node):
		self._indent()
		self.buffer.append("xsc.Comment(%r)" % self._text(node.content))

	def presentDocType(self, node):
		self._indent()
		self.buffer.append("xsc.DocType(%r)" % self._text(node.content))

	def presentAttr(self, node):
		self.presentFrag(node)

	def presentURLAttr(self, node):
		self.presentFrag(node)

defaultPresenterClass = PlainPresenter
