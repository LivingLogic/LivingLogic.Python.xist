#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
This module contains classes that are used for dumping elements
to the terminal.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import os, types, keyword

from ll import ansistyle, url

import xsc, options

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

class EnvTextForAmp(EnvText):
	"""
	ANSI escape sequence to be used for & (used in entity)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_AMP", (0x3, 0xf))

class EnvTextForSemi(EnvText):
	"""
	ANSI escape sequence to be used for semicolons (used in entities)
	"""
	color = getColorsFromEnv("XSC_REPRANSI_SEMI", (0x3, 0xf))

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

class EnvTextForAttrName(EnvText):
	"""
	ANSI escape sequence to be used for attr class name
	"""
	color = getColorsFromEnv("XSC_REPRANSI_ATTRNAME", (0xe, 0xc))

class EnvTextForAttrsName(EnvText):
	"""
	ANSI escape sequence to be used for attrs class name
	"""
	color = getColorsFromEnv("XSC_REPRANSI_ATTRSNAME", (0xe, 0xc))

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
				entity = xsc.defaultPrefixes.charref(charcode)
				if entity is not None:
					return EnvTextForEntityName("&", entity.xmlname[True], ";")
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

def strAmp():
	return EnvTextForAmp("&")

def strSemi():
	return EnvTextForSemi(";")

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
		u = u.url
	return EnvTextForURL(EscInlineText(u))

def strDocTypeMarker():
	return EnvTextForDocTypeMarker("DOCTYPE")

def strDocTypeText(text):
	return EnvTextForDocTypeText(EscInlineText(text))

def strCommentMarker():
	return EnvTextForCommentMarker("--")

def strCommentText(text):
	return EnvTextForCommentText(EscInlineText(text))

def strNamespace(namespace):
	return EnvTextForNamespace(EscInlineText(namespace))

def strElementName(name):
	return EnvTextForElementName(EscInlineText(name))

def strAttrName(name):
	return EnvTextForAttrName(EscInlineText(name))

def strAttrsName(name):
	return EnvTextForAttrsName(EscInlineText(name))

def strEntityName(name):
	return EnvTextForEntityName(EscInlineText(name))

def strProcInstTarget(target):
	return EnvTextForProcInstTarget(EscInlineText(target))

def strProcInstContent(content):
	return EnvTextForProcInstContent(EscInlineText(content))

def strTextOutsideAttr(text):
	return EnvTextForText(EscInlineText(text))

def strTextInAttr(text):
	return EnvTextForAttrValue(EscInlineAttr(text))

def strAttrValue(attrvalue):
	return EnvTextForAttrValue(EscInlineAttr(attrvalue))

class Presenter:
	"""
	<par>This class is the base of the presenter classes. It is abstract
	and only serves as documentation for the methods.</par>
	<par>A <class>Presenter</class> generates a specific
	string representation of a node to be printed on the screen.</par>
	"""

	def beginPresentation(self):
		"""
		<par>called by once at the start when <pyref module="ll.xist.xsc" class="Node" method="repr"><method>repr</method></pyref>
		is called. Initializes the presenter.</par>
		"""
		pass

	def endPresentation(self):
		"""
		<par>called once after the call to <pyref module="ll.xist.xsc" class="Node" method="present"><method>present</method></pyref>.
		This method handles cleanups if necessary and returns the string to be printed.</par>
		"""
		pass

	def doPresentation(self, node):
		"""
		<par>create a string presentation for <arg>node</arg> and return the resulting string.</par>
		"""
		self.beginPresentation()
		node.present(self)
		return self.endPresentation()
	
	def presentText(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="Text"><class>Text</class></pyref> node.</par>
		"""
		raise NotImplementedError("presentText")

	def presentFrag(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="Frag"><class>Frag</class></pyref> node.</par>
		"""
		raise NotImplementedError("presentFrag")

	def presentComment(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="Comment"><class>Comment</class></pyref> node.</par>
		"""
		raise NotImplementedError("presentComment")

	def presentDocType(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="DocType"><class>DocType</class></pyref> node.</par>
		"""
		raise NotImplementedError("presentDocType")

	def presentProcInst(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="ProcInst"><class>ProcInst</class></pyref> node.</par>
		"""
		raise NotImplementedError("presentProcInst")

	def presentAttrs(self, node):
		"""
		<par>present an <pyref module="ll.xist.xsc" class="Attrs"><class>Attrs</class></pyref> node.</par>
		"""
		raise NotImplementedError("presentAttrs")

	def presentElement(self, node):
		"""
		<par>present an <pyref module="ll.xist.xsc" class="Element"><class>Element</class></pyref> node.</par>
		"""
		raise NotImplementedError("presentElement")

	def presentEntity(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="Entity"><class>Entity</class></pyref> node.</par>
		"""
		raise NotImplementedError("presentEntity")

	def presentNull(self, node):
		"""
		<par>present the <class>Null</class> node.</par>
		"""
		raise NotImplementedError("presentNull")

	def presentAttr(self, node):
		"""
		<par>present an <pyref module="ll.xist.xsc" class="Attr"><class>Attr</class></pyref> node.</par>
		"""
		raise NotImplementedError("presentAttr")

class PlainPresenter(Presenter):
	"""
	<par>This presenter shows only the root node of the tree (with a little additional
	information about the number of nested nodes). It is used as the default presenter
	in <pyref module="ll.xist.xsc" class="Node" method="__repr__"><method>Node.__repr__</method></pyref>.</par>
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
		self.buffer = "<%s/%s instance content=%r at 0x%x>" % (node.__class__.__module__, node.__class__.__fullname__(), content, id(node))

	presentText = presentCharacterData

	def presentFrag(self, node):
		l = len(node)
		if l==0:
			info = "with no children"
		elif l==1:
			info = "with 1 child"
		else:
			info = "with %d children" % l
		self.buffer = "<%s/%s instance %s at 0x%x>" % (node.__class__.__module__, node.__class__.__fullname__(), info, id(node))

	def presentAttr(self, node):
		l = len(node)
		if l==0:
			info = "with no children"
		elif l==1:
			info = "with 1 child"
		else:
			info = "with %d children" % l
		self.buffer = "<attr instance %s/%s %s at 0x%x>" % (node.__class__.__module__, node.__class__.__fullname__(), info, id(node))

	presentComment = presentCharacterData
	presentDocType = presentCharacterData
	def presentProcInst(self, node):
		if len(node)>self.maxlen:
			content = node.content[:self.maxlen/2] + u"..." + node.content[-self.maxlen/2:]
		else:
			content = node.content
		self.buffer = "<procinst instance %s/%s content=%r at 0x%x>" % (node.__class__.__module__, node.__class__.__fullname__(), content, id(node))

	def presentAttrs(self, node):
		l = len(node)
		if l==0:
			info = "with no attributes"
		elif l==1:
			info = "with 1 attribute"
		else:
			info = "with %d attributes" % l
		self.buffer = "<attrs instance %s/%s %s at 0x%x>" % (node.__class__.__module__, node.__class__.__fullname__(), info, id(node))

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
			infoa = "and no attributes"
		elif la==1:
			infoa = "and 1 attribute"
		else:
			infoa = "and %d attributes" % la
		self.buffer = "<element instance %s/%s %s %s at 0x%x>" % (node.__class__.__module__, node.__class__.__fullname__(), infoc, infoa, id(node))

	def presentEntity(self, node):
		self.buffer = "<entity instance %s/%s at 0x%x>" % (node.__class__.__module__, node.__class__.__fullname__(), id(node))

	def presentNull(self, node):
		self.buffer = "<instance %s/%s at 0x%x>" % (node.__class__.__module__, node.__class__.__fullname__(), id(node))

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
			node._str(fullname=1, xml=0, decorate=0),
			" ",
			strProcInstContent(node.content),
			strQuestion(),
			strBracketClose()
		)

	def presentAttrs(self, node):
		for (attrname, attrvalue) in node.items():
			self.buffer.append(" ")
			if isinstance(attrname, tuple):
				self.buffer.append(attrvalue._str(fullname=0, xml=0, decorate=0))
			else:
				self.buffer.append(strAttrName(attrname))
			self.buffer.append("=", strQuote())
			attrvalue.present(self)
			self.buffer.append(strQuote())

	def presentElement(self, node):
		if node.empty:
			self.buffer.append(strBracketOpen(), node._str(fullname=1, xml=0, decorate=0))
			node.attrs.present(self)
			self.buffer.append(strSlash(), strBracketClose())
		else:
			self.buffer.append(strBracketOpen(), node._str(fullname=1, xml=0, decorate=0))
			node.attrs.present(self)
			self.buffer.append(strBracketClose())
			for child in node:
				child.present(self)
			self.buffer.append(strBracketOpen(), strSlash(), node._str(fullname=1, xml=0, decorate=0), strBracketClose())

	def presentEntity(self, node):
		self.buffer.append(node._str(fullname=1, xml=0, decorate=1))

	def presentNull(self, node):
		self.buffer.append(node._str(fullname=1, xml=0, decorate=0))

	def presentAttr(self, node):
		xsc.Frag.present(node, self)

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
				newline1 = []
				for comp in line[1]:
					if isinstance(comp, tuple):
						newline1.append("%s.%s" % (comp[0].xmlprefix, comp[1]))
					else:
						newline1.append(str(comp))
				line[1] = "/".join(newline1)
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
		loc = node.startloc
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
				self.lines.append([node.startloc, self.currentPath[:], len(self.currentPath), ansistyle.Text(strBracketOpen(), node._str(fullname=1, xml=0, decorate=0), strBracketClose())])
				self.currentPath.append(0)
				for child in node:
					child.present(self)
					self.currentPath[-1] += 1
				del self.currentPath[-1]
				self.lines.append([node.endloc, self.currentPath[:], len(self.currentPath), ansistyle.Text(strBracketOpen(), strSlash(), node._str(fullname=1, xml=0, decorate=0), strBracketClose())])
			else:
				self.lines.append([node.startloc, self.currentPath[:], len(self.currentPath), ansistyle.Text(strBracketOpen(), node._str(fullname=1, xml=0, decorate=0), strSlash(), strBracketClose())])

	def presentAttrs(self, node):
		if self.inAttr:
			for (attrname, attrvalue) in node.items():
				self.buffers[-1].append(" ")
				if isinstance(attrname, tuple):
					self.buffers[-1].append(strNamespace(attrname[0].xmlprefix), strColon(), strAttrName(attrname[1]))
				else:
					self.buffers[-1].append(strAttrName(attrname))
				self.buffers[-1].append("=", strQuote())
				attrvalue.present(self)
				self.buffers[-1].append(strQuote())
		else:
			s = ansistyle.Text(strBracketOpen(), node._str(fullname=1, xml=0, decorate=0), strBracketClose())
			self.lines.append([node.startloc, self.currentPath[:], len(self.currentPath), s])
			self.currentPath.append(None)
			for (attrname, attrvalue) in node.items():
				self.currentPath[-1] = attrname
				attrvalue.present(self)
			self.currentPath.pop()
			s = ansistyle.Text(strBracketOpen(), strSlash(), node._str(fullname=1, xml=0, decorate=0), strBracketClose())
			self.lines.append([node.endloc, self.currentPath[:], len(self.currentPath), s])

	def presentElement(self, node):
		if self.inAttr:
			self.buffers[-1].append(strBracketOpen(), node._str(fullname=1, xml=0, decorate=0))
			self.inAttr += 1
			node.attrs.present(self)
			self.inAttr -= 1
			if len(node):
				self.buffers[-1].append(strBracketClose())
				node.content.present(self)
				self.buffers[-1].append(strBracketOpen(), strSlash(), node._str(fullname=1, xml=0, decorate=0), strBracketClose())
			else:
				self.buffers[-1].append(strSlash(), strBracketClose())
		else:
			self.buffers.append(ansistyle.Text(strBracketOpen(), node._str(fullname=1, xml=0, decorate=0)))
			self.inAttr += 1
			node.attrs.present(self)
			self.inAttr -= 1
			if len(node):
				self.buffers[-1].append(strBracketClose())
				self.lines.append([node.startloc, self.currentPath[:], len(self.currentPath), ansistyle.Text(*self.buffers)])
				self.buffers = [] # we're done with the buffers for the header
				self.currentPath.append(0)
				for child in node:
					child.present(self)
					self.currentPath[-1] += 1
				self.currentPath.pop()
				self.lines.append([node.endloc, self.currentPath[:], len(self.currentPath), ansistyle.Text(strBracketOpen(), strSlash(), node._str(fullname=1, xml=0, decorate=0), strBracketClose())])
			else:
				self.buffers[-1].append(strSlash(), strBracketClose())
				self.lines.append([node.startloc, self.currentPath[:], len(self.currentPath), ansistyle.Text(*self.buffers)])
				self.buffers = [] # we're done with the buffers for the header

	def presentNull(self, node):
		if not self.inAttr:
			self.lines.append([node.startloc, self.currentPath[:], len(self.currentPath), node._str(fullname=1, xml=0, decorate=1)])

	def presentText(self, node):
		if self.inAttr:
			self.buffers[-1].append(strTextInAttr(node.content))
		else:
			lines = node.content.splitlines(1)
			self._doMultiLine(node, lines, 0, self.strTextLineOutsideAttr)

	def presentEntity(self, node):
		if self.inAttr:
			self.buffers[-1].append(node._str(fullname=1, xml=0, decorate=1))
		else:
			self.lines.append([node.startloc, self.currentPath[:], len(self.currentPath), node._str(fullname=1, xml=0, decorate=1)])

	def presentProcInst(self, node):
		if self.inAttr:
			self.buffers[-1].append(
				strBracketOpen(),
				strQuestion(),
				node._str(fullname=1, xml=0, decorate=0),
				" ",
				EnvTextForProcInstContent(EscOutlineAttr(node.content)),
				strQuestion(),
				strBracketClose()
			)
		else:
			head = ansistyle.Text(strBracketOpen(), strQuestion(), node._str(fullname=1, xml=0, decorate=0), " ")
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

class CodePresenter(Presenter):
	"""
	<par>This presenter formats the object as a nested Python object tree.</par>
	
	<par>This makes it possible to quickly convert &html;/&xml; files to &xist;
	constructor calls.</par>
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
			self.buffer.append("%s.%s" % (node.__module__, node.__fullname__()))
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
			if isinstance(attrname, tuple):
				ns = attrname[0].__module__
				attrname = attrname[1]
				if keyword.iskeyword(attrname):
					attrname += "_"
				self.buffer.append("(%s, %r): " % (ns, attrname))
			else:
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
		self.buffer.append("%s.%s(" % (node.__module__, node.__class__.__fullname__()))
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
			globalattrs = {}
			for (attrname, attrvalue) in node.attrs.items():
				if isinstance(attrname, tuple):
					globalattrs[attrname] = attrvalue
			if len(globalattrs):
				for (attrname, attrvalue) in globalattrs.items():
					if i:
						self.buffer.append(", ")
						if self.inAttr:
							self.buffer.append(" ")
					self._indent()
					self.buffer.append("{ ")
					self.inAttr += 1
					ns = attrname[0].__module__
					attrname = attrname[1]
					self.buffer.append("(%s, %r): " % (ns, attrname))
					if len(attrvalue)==1: # optimize away the tuple ()
						attrvalue[0].present(self)
					else:
						attrvalue.present(self)
					self.inAttr -= 1
					self.buffer.append(" }")
					i += 1
			for (attrname, attrvalue) in node.attrs.items():
				if not isinstance(attrname, tuple):
					if i:
						self.buffer.append(",")
						if self.inAttr:
							self.buffer.append(" ")
					self._indent()
					self.inAttr += 1
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
		self.buffer.append("%s.%s()" % (node.__module__, node.__class__.__fullname__()))

	def presentProcInst(self, node):
		self._indent()
		self.buffer.append("%s.%s(%r)" % (node.__module__, node.__class__.__fullname__(), self._text(node.content)))

	def presentComment(self, node):
		self._indent()
		self.buffer.append("xsc.Comment(%r)" % self._text(node.content))

	def presentDocType(self, node):
		self._indent()
		self.buffer.append("xsc.DocType(%r)" % self._text(node.content))

	def presentAttr(self, node):
		self.presentFrag(node)

defaultPresenterClass = PlainPresenter
