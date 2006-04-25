#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2006 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
This module contains presenter classes, which are used for displaying &xist;
nodes on screen (either on the terminal or via
<pyref module="IPython.Extensions.ipipe"><module>ipipe</module></pyref> browser).
"""


__version__ = "$Revision$".split()[1]
# $Source$


import sys, os, keyword, codecs

# IPython/ipipe support
try:
	from IPython.Extensions import ipipe
except ImportError:
	ipipe = None

from ll import misc, astyle, url

import xsc, options


###
### Colors for output
###

# style to be used for tabs
s4tab = astyle.Style.fromenv("LL_XIST_REPRANSI_TAB", "black:black:bold")


# style to be used for quotes (delimiters for text and attribute nodes)
s4quote = astyle.Style.fromenv("LL_XIST_REPRANSI_QUOTE", "white:black:bold")


# style to be used for text
s4text = astyle.Style.fromenv("LL_XIST_REPRANSI_TEXT", "white:black")


# style to be used for namespaces
s4ns = astyle.Style.fromenv("LL_XIST_REPRANSI_NAMESPACE", "blue:black")


# style to be used for Null object
s4null = astyle.Style.fromenv("LL_XIST_REPRANSI_NULL", "white:black:bold")


# style to be used for Null name
s4nullname = astyle.Style.fromenv("LL_XIST_REPRANSI_NULLNAME", "white:black:bold")


# style to be used a Frag object
s4frag = astyle.Style.fromenv("LL_XIST_REPRANSI_FRAG", "white:black:bold")


# style to be used for Frag name
s4fragname = astyle.Style.fromenv("LL_XIST_REPRANSI_FRAGNAME", "white:black:bold")


# style to be used for elements (i.e. the <, > and / characters
s4element = astyle.Style.fromenv("LL_XIST_REPRANSI_ELEMENT", "white:black:bold")


# style to be used for element names
s4elementname = astyle.Style.fromenv("LL_XIST_REPRANSI_ELEMENTNAME", "blue:black:bold")


# style to be used for processing instructions
s4procinst = astyle.Style.fromenv("LL_XIST_REPRANSI_PROCINST", "red:black:bold")


# style to be used for processing instruction targets
s4procinsttarget = astyle.Style.fromenv("LL_XIST_REPRANSI_PROCINSTTARGET", "red:black:bold")


# style to be used for processing instruction content
s4procinstcontent = astyle.Style.fromenv("LL_XIST_REPRANSI_PROCINSTCONTENT", "white:black")


# style to be used for attributes (i.e. the quotes around their value)
s4attr = astyle.Style.fromenv("LL_XIST_REPRANSI_ATTR", "blue:black:bold")


# style to be used for attribute names
s4attrname = astyle.Style.fromenv("LL_XIST_REPRANSI_ATTRNAME", "blue:black:bold")


# style to be used for attrs class name
s4attrs = astyle.Style.fromenv("LL_XIST_REPRANSI_ATTRS", "blue:black:bold")


# style to be used for attrs class name
s4attrsname = astyle.Style.fromenv("LL_XIST_REPRANSI_ATTRSNAME", "blue:black:bold")


# style to be used for entities
s4entity = astyle.Style.fromenv("LL_XIST_REPRANSI_ENTITY", "magenta:black")


# style to be used for entity names
s4entityname = astyle.Style.fromenv("LL_XIST_REPRANSI_ENTITYNAME", "magenta:black")


# style to be used for charref names or codepoints
s4charrefname = astyle.Style.fromenv("LL_XIST_REPRANSI_CHARREFNAME", "magenta:black")


# style to be used for document types
s4doctype = astyle.Style.fromenv("LL_XIST_REPRANSI_DOCTYPE", "white:black:bold")


# style to be used for document types
s4doctypetext = astyle.Style.fromenv("LL_XIST_REPRANSI_DOCTYPETEXT", "white:black:bold")


# style to be used for comment (i.e. <!-- and -->)
s4comment = astyle.Style.fromenv("LL_XIST_REPRANSI_COMMENT", "black:black:bold")


# style to be used for comment text
s4commenttext = astyle.Style.fromenv("LL_XIST_REPRANSI_COMMENTTEXT", "black:black:bold")


# style to be used for attribute values
s4attrvalue = astyle.Style.fromenv("LL_XIST_REPRANSI_ATTRVALUE", "yellow:black")


# style to be used for URLs
s4url = astyle.Style.fromenv("LL_XIST_REPRANSI_URL", "green:black")


# style to be used for numbers in error messages etc.
s4number = astyle.Style.fromenv("LL_XIST_REPRANSI_NUMBER", "blue:black")


# style to be used for variable strings in error messages etc.
s4string = astyle.Style.fromenv("LL_XIST_REPRANSI_STRING", "magenta:black")


# style to be used for IDs in repr()
s4id = astyle.Style.fromenv("LL_XIST_REPRANSI_ID", "yellow:black")


class Queue(object):
	"""
	queue: write bytes at one end, read bytes from the other end
	"""
	def __init__(self):
		self._buffer = ""

	def write(self, chars):
		self._buffer += chars

	def read(self, size=-1):
		if size<0:
			s = self._buffer
			self._buffer = ""
			return s
		else:
			s = self._buffer[:size]
			self._buffer = self._buffer[size:]
			return s


def encode(encoding, *iterators):
	queue = Queue()
	writer = codecs.getwriter(encoding)(queue)
	for iterator in iterators:
		for text in iterator:
			writer.write(text)
			yield queue.read()


class EscInlineText(object):
	ascharref = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f<>&"
	ascolor   = "\x09"

	@classmethod
	def parts(cls, style, string):
		for char in string:
			if char in cls.ascolor:
				yield s4tab(char)
			else:
				ascharref = char in cls.ascharref
				if not ascharref:
					try:
						char.encode(options.reprencoding)
					except:
						ascharref = True
				if ascharref:
					charcode = ord(char)
					try:
						entity = xsc.defaultPrefixes.charref(charcode)
					except LookupError:
						yield s4charrefname(u"&#", unicode(charcode), u";")
					else:
						yield s4entityname(u"&", unicode(entity.xmlname), u";")
				else:
					yield style(char)


class EscInlineAttr(EscInlineText):
	ascharref = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f<>\"&"
	ascolor   = "\x09\x0a"


class EscOutlineText(EscInlineText):
	ascharref = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f<>&"
	ascolor   = ""


class EscOutlineAttr(EscInlineText):
	ascharref = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f<>\"&"
	ascolor   = ""


def strtab(count):
	return s4tab(unicode(options.reprtab)*count)


def strTextInAttr(text):
	return s4attrvalue(text)


if ipipe is not None:
	presenterbase = ipipe.Table
else:
	class presenterbase(object):
		def __iter__(self):
			return self.__xiter__("default")


class Presenter(presenterbase):
	"""
	<par>This class is the base of the presenter classes. It is abstract
	and only serves as documentation for the methods.</par>
	<par>A <class>Presenter</class> generates a specific
	string representation of a node to be printed on the screen.</par>
	"""

	def __init__(self, node):
		self.node = node

	@misc.notimplemented
	def presentText(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="Text"><class>Text</class></pyref> node.</par>
		"""

	@misc.notimplemented
	def presentFrag(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="Frag"><class>Frag</class></pyref> node.</par>
		"""

	@misc.notimplemented
	def presentComment(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="Comment"><class>Comment</class></pyref> node.</par>
		"""

	@misc.notimplemented
	def presentDocType(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="DocType"><class>DocType</class></pyref> node.</par>
		"""

	@misc.notimplemented
	def presentProcInst(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="ProcInst"><class>ProcInst</class></pyref> node.</par>
		"""

	@misc.notimplemented
	def presentAttrs(self, node):
		"""
		<par>present an <pyref module="ll.xist.xsc" class="Attrs"><class>Attrs</class></pyref> node.</par>
		"""

	@misc.notimplemented
	def presentElement(self, node):
		"""
		<par>present an <pyref module="ll.xist.xsc" class="Element"><class>Element</class></pyref> node.</par>
		"""

	@misc.notimplemented
	def presentEntity(self, node):
		"""
		<par>present a <pyref module="ll.xist.xsc" class="Entity"><class>Entity</class></pyref> node.</par>
		"""

	@misc.notimplemented
	def presentNull(self, node):
		"""
		<par>present the <class>Null</class> node.</par>
		"""

	@misc.notimplemented
	def presentAttr(self, node):
		"""
		<par>present an <pyref module="ll.xist.xsc" class="Attr"><class>Attr</class></pyref> node.</par>
		"""


class PlainPresenter(Presenter):
	"""
	<par>This presenter shows only the root node of the tree (with a little additional
	information about the number of nested nodes). It is used as the default presenter
	in <pyref module="ll.xist.xsc" class="Node" method="__repr__"><method>Node.__repr__</method></pyref>.</par>
	"""
	def __init__(self, encoding=None, maxlen=60):
		Presenter.__init__(self, encoding)
		self.maxlen = maxlen

	def presentCharacterData(self, node):
		content = node.content
		if len(content)>self.maxlen:
			content = u"%s...%s" % (content[:self.maxlen/2], content[-self.maxlen/2:])
		yield astyle.default(u"<", s4ns(unicode(node.__class__.__module__)), u":", unicode(node.__class__.__fullname__()), u" object content=", unicode(repr(content)), u" at ", s4id(u"0x%x" % id(node)), u">")

	presentText = presentCharacterData

	def presentFrag(self, node):
		l = len(node)
		if l==0:
			info = u"no children"
		elif l==1:
			info = u"1 child"
		else:
			info = u"%d children" % l
		yield astyle.default(u"<", node._str(fullname=True, xml=False, decorate=False), u" object (", info, u") at ", s4id(u"0x%x" % id(node)), u">")

	def presentAttr(self, node):
		l = len(node)
		if l==0:
			info = u"no children"
		elif l==1:
			info = u"1 child"
		else:
			info = u"%d children" % l
		yield astyle.default(u"<", node._str(fullname=True, xml=False, decorate=False), u" attr object (", info, u") at ", s4id(u"0x%x" % id(node)), u">")

	presentComment = presentCharacterData
	presentDocType = presentCharacterData
	def presentProcInst(self, node):
		content = node.content
		if len(content)>self.maxlen:
			content = content[:self.maxlen/2] + u"..." + content[-self.maxlen/2:]
		yield astyle.default(u"<", node._str(fullname=True, xml=False, decorate=False), u" procinst object content=", repr(content), u") at ", s4id(u"0x%x" % id(node)), u">")

	def presentAttrs(self, node):
		l = len(node)
		if l==0:
			info = u"(no attrs)"
		elif l==1:
			info = u"(1 attr)"
		else:
			info = u"(%d attrs)" % l
		yield astyle.default(u"<", node._str(fullname=True, xml=False, decorate=False), u" attrs object ", info, u" at ", s4id(u"0x%x" % id(node)), u">")

	def presentElement(self, node):
		lc = len(node.content)
		if lc==0:
			infoc = u"no children"
		elif lc==1:
			infoc = u"1 child"
		else:
			infoc = u"%d children" % lc
		la = len(node.attrs)
		if la==0:
			infoa = u"no attrs"
		elif la==1:
			infoa = u"1 attr"
		else:
			infoa = u"%d attrs" % la
		yield astyle.default(u"<", node._str(fullname=True, xml=False, decorate=False), u" element object (", infoc, u"/", infoa, u") at ", s4id(u"0x%x" % id(node)), u">")

	def presentEntity(self, node):
		yield astyle.default(u"<", node._str(fullname=True, xml=False, decorate=False), u" entity object at ", s4id(u"0x%x" % id(node)), u">")

	def presentNull(self, node):
		yield astyle.default(u"<", node._str(fullname=True, xml=False, decorate=False), u" object at ", s4id(u"0x%x" % id(node)), u">")


class NormalPresenter(Presenter):
	def present(self, node):
		self.inattr = 0
		for part in node.present(self):
			yield part

	def presentText(self, node):
		if self.inattr:
			yield astyle.aunicode().join(EscOutlineAttr.parts(xsc.c4attrvalue, node.content))
		else:
			yield astyle.aunicode().join(EscInlineText.parts(astyle.color, node.content))

	def presentFrag(self, node):
		for child in node:
			for part in child.present(self):
				yield part

	def presentComment(self, node):
		yield s4comment(u"<!--")
		yield astyle.aunicode().join(EscOutlineText.parts(xsc.c4commenttext, node.content))
		yield s4comment(u"-->")

	def presentDocType(self, node):
		yield s4doctype(u"<!DOCTYPE ")
		yield astyle.aunicode().join(EscOutlineText.parts(xsc.c4doctypetext, node.content))
		yield s4doctype(u">")

	def presentProcInst(self, node):
		yield s4procinst(u"<?")
		yield node._str(fullname=True, xml=False, decorate=False)
		yield s4procinst(u" ")
		yield astyle.aunicode().join(EscOutlineText.parts(xsc.c4doctypetext, node.content))
		yield s4procinst(u"?>")

	def presentAttrs(self, node):
		self.inattr += 1
		for (attrname, attrvalue) in node.iteritems():
			yield u" "
			if isinstance(attrname, tuple):
				yield attrvalue._str(fullname=False, xml=False, decorate=False)
			else:
				yield s4attrname(attrname)
			yield u"="
			yield s4attr(u'"')
			for part in attrvalue.present(self):
				yield part
			yield s4attr(u'"')
		self.inattr -= 1

	def presentElement(self, node):
		yield s4element(u"<")
		yield node._str(fullname=True, xml=False, decorate=False)
		for part in node.attrs.present(self):
			yield part
		if not len(node) and node.model and node.model.empty:
			yield s4element(u"/>")
		else:
			yield s4element(u">")
			for child in node:
				for part in child.present(self):
					yield part
			yield s4element(u"</")
			yield node._str(fullname=True, xml=False, decorate=False)
			yield s4element(u">")

	def presentEntity(self, node):
		yield node._str(fullname=True, xml=False, decorate=True)

	def presentNull(self, node):
		yield node._str(fullname=True, xml=False, decorate=True)

	def presentAttr(self, node):
		for part in xsc.Frag.present(node, self):
			yield part


class TreePresenter(Presenter):
	"""
	This presenter shows the object as a nested tree.
	"""
	def __init__(self, encoding=None, showlocation=True, showpath=1):
		"""
		<par>Create a <class>TreePresenter</class> instance. Arguments have the
		following meaning:</par>
		<dlist>
		<term><arg>showlocation</arg></term><item>Should the location of the
		node (i.e. system id, line and column number) be displayed as the first
		column? (default <lit>True</lit>).</item>
		<term><arg>showpath</arg></term><item><par>This specifies if and how
		the path (i.e. the position of the node in the tree) should be displayed.
		Possible values are:</par>
		<ulist>
		<item><lit>0</lit>: Don't show a path.</item>
		<item><lit>1</lit>: Show a path (e.g. as <lit>0/2/3</lit>,
		i.e. this node is the 4th child of the 3rd child of the 1st child of the
		root node). This is the default.</item>
		<item><lit>2</lit>: Show a path as a usable Python
		expression (e.g. as <lit>[0,2,3]</lit>).</item>
		</ulist>
		</item>
		</dlist>
		"""
		Presenter.__init__(self, encoding)
		self.showlocation = showlocation
		self.showpath = showpath

	def present(self, node):
		self._inattr = 0
		self._currentpath = [] # numerical path
		self._buffers = [] # list of [color, string] lists used for formatting attributes (this is a list, because elements may contain elements in their attributes)

		if not self.showpath and not self.showlocation:
			# we need no column formatting, so we can yield the result directly
			for (loc, path, line) in node.present(self):
				yield line
				yield u"\n"
		else:
			lines = list(node.present(self))
	
			lenloc = 0
			lennumpath = 0
			for line in lines:
				# format and calculate width of location info
				if self.showlocation:
					loc = line[0]
					if loc is None:
						loc = xsc.Location()
					loc = str(loc)
					lenloc = max(lenloc, len(loc))
					line[0] = loc

				# format and calculate width of path info
				if self.showpath:
					newline1 = []
					if self.showpath == 1:
						for comp in line[1]:
							if isinstance(comp, tuple):
								newline1.append(u"%s:%s" % (comp[0].xmlname, comp[1]))
							else:
								newline1.append(unicode(comp))
						line[1] = u"/".join(newline1)
					else:
						for comp in line[1]:
							if isinstance(comp, tuple):
								newline1.append(u"(%s,%r)" % (comp[0].xmlname, comp[1]))
							else:
								newline1.append(repr(comp))
						line[1] = u"[%s]" % u",".join(newline1)
				lennumpath = max(lennumpath, len(line[1]))

			newlines = []
			for line in lines:
				if self.showlocation:
					yield line[0]
					yield u" " * (lenloc-len(line[0])+1) # filler
				if self.showpath:
					yield line[1]
					yield u" " * (lennumpath-len(line[1])+1) # filler
				yield line[2]
				yield "\n"
		del self._inattr
		del self._buffers
		del self._currentpath

	def _domultiline(self, node, lines, indent, formatter, head=None, tail=None):
		loc = node.startloc
		nest = len(self._currentpath)
		l = len(lines)
		for i in xrange(max(1, l)): # at least one line
			if loc is not None:
				hereloc = loc.offset(i)
			else:
				hereloc = None
			mynest = nest
			if i<len(lines):
				s = lines[i]
			else:
				s = u""
			if indent:
				oldlen = len(s)
				s = s.lstrip(u"\t")
				mynest += len(s)-oldlen
			s = formatter(s)
			if i == 0 and head is not None: # prepend head to first line
				s = head + s
			if i >= l-1 and tail is not None: # append tail to last line
				s = s + tail
			yield [hereloc, self._currentpath[:], strtab(mynest) + s]

	def strTextLineOutsideAttr(self, text):
		return s4text(s4quote(u'"'), astyle.aunicode().join(EscOutlineText.parts(xsc.c4text, text)), s4quote(u'"'))

	def strTextInAttr(self, text):
		return astyle.aunicode().join(EscOutlineAttr.parts(xsc.c4attrvalue, text))

	def strProcInstContentLine(self, text):
		return astyle.aunicode().join(EscOutlineText.parts(xsc.c4procinstcontent, text))

	def strCommentTextLine(self, text):
		return astyle.aunicode().join(EscOutlineText.parts(xsc.c4commenttext, text))

	def strDocTypeTextLine(self, text):
		return astyle.aunicode().join(EscOutlineText(xsc.c4doctypetext, text).parts(text))

	def presentFrag(self, node):
		if self._inattr:
			for child in node:
				for line in child.present(self):
					yield line
		else:
			if len(node):
				yield [
					node.startloc,
					self._currentpath[:],
					s4frag(
						strtab(len(self._currentpath)),
						u"<",
						node._str(fullname=True, xml=False, decorate=False),
						u">",
					)
				]
				self._currentpath.append(0)
				for child in node:
					for line in child.present(self):
						yield line
					self._currentpath[-1] += 1
				self._currentpath.pop(-1)
				yield [
					node.endloc,
					self._currentpath[:],
					s4frag(
						strtab(len(self._currentpath)),
						u"</",
						node._str(fullname=True, xml=False, decorate=False),
						u">",
					)
				]
			else:
				yield [
					node.startloc,
					self._currentpath[:],
					s4frag(
						strtab(len(self._currentpath)),
						u"<",
						node._str(fullname=True, xml=False, decorate=False),
						u"/>",
					)
				]

	def presentAttrs(self, node):
		if self._inattr:
			for (attrname, attrvalue) in node.iteritems():
				self._buffers[-1] += xsc.c4attrs(" ")
				if isinstance(attrname, tuple):
					self._buffers[-1] += s4attr(xsc.c4ns(unicode(attrname[0].xmlname)), u":", s4attrname(unicode(attrname[1])))
				else:
					self._buffers[-1] += s4attrname(unicode(attrname))
				self._buffers[-1] += s4attr(u'="')
				for line in attrvalue.present(self):
					yield line
				self._buffers[-1] += s4attr(u'"')
		else:
			yield [
				node.startloc,
				self._currentpath[:],
				s4attrs(
					strtab(len(self._currentpath)),
					u"<",
					node._str(fullname=True, xml=False, decorate=False),
					u">",
				)
			]
			self._currentpath.append(None)
			for (attrname, attrvalue) in node.iteritems():
				self._currentpath[-1] = attrname
				for line in attrvalue.present(self):
					yield line
			self._currentpath.pop()
			yield [
				node.endloc,
				self._currentpath[:],
				s4attrs(
					strtab(len(self._currentpath)),
					u"</",
					node._str(fullname=True, xml=False, decorate=False),
					u">",
				)
			]

	def presentElement(self, node):
		if self._inattr:
			self._buffers[-1] += s4element(u"<", node._str(fullname=True, xml=False, decorate=False))
			self._inattr += 1
			for line in node.attrs.present(self):
				yield line
			self._inattr -= 1
			if len(node):
				self._buffers[-1] += s4element(u">")
				for line in node.content.present(self):
					yield line
				self._buffers[-1] += s4element(u"</", node._str(fullname=True, xml=False, decorate=False), u">")
			else:
				self._buffers[-1] += s4element(u"/>")
		else:
			self._buffers.append(s4element(u"<", node._str(fullname=True, xml=False, decorate=False)))
			self._inattr += 1
			for line in node.attrs.present(self):
				yield line
			self._inattr -= 1
			if len(node):
				self._buffers[-1] += s4element(u">")
				yield [
					node.startloc,
					self._currentpath[:],
					s4element(
						strtab(len(self._currentpath)),
						*self._buffers
					)
				]
				self._buffers = [] # we're done with the buffers for the header
				self._currentpath.append(0)
				for child in node:
					for line in child.present(self):
						yield line
					self._currentpath[-1] += 1
				self._currentpath.pop()
				yield [
					node.endloc,
					self._currentpath[:],
					s4element(
						strtab(len(self._currentpath)),
						u"</",
						node._str(fullname=True, xml=False, decorate=False),
						u">",
					)
				]
			else:
				self._buffers[-1] += xsc.c4element(u"/>")
				yield [
					node.startloc,
					self._currentpath[:],
					s4element(
						strtab(len(self._currentpath)),
						*self._buffers
					)
				]
				self._buffers = [] # we're done with the buffers for the header

	def presentNull(self, node):
		if not self._inattr:
			yield [
				node.startloc,
				self._currentpath[:],
				s4null(
					strtab(len(self._currentpath)),
					node._str(fullname=True, xml=False, decorate=True)
				)
			]

	def presentText(self, node):
		if self._inattr:
			self._buffers[-1] += strTextInAttr(node.content)
		else:
			lines = node.content.splitlines(True)
			for line in self._domultiline(node, lines, 0, self.strTextLineOutsideAttr):
				yield line

	def presentEntity(self, node):
		if self._inattr:
			self._buffers[-1].append(node._str(fullname=True, xml=False, decorate=True))
		else:
			yield [
				node.startloc,
				self._currentpath[:],
				s4entity(
					strtab(len(self._currentpath)),
					node._str(fullname=True, xml=False, decorate=True)
				)
			]

	def presentProcInst(self, node):
		if self._inattr:
			self._buffers[-1] += xsc.c4procinst(
				u"<?",
				node._str(fullname=True, xml=False, decorate=False),
				u" ",
				astyle.Text(color4procinstcontent, EscOutlineAttr(node.content)),
				u"?>",
			)
		else:
			head = s4procinst(u"<?", node._str(fullname=True, xml=False, decorate=False), u" ")
			tail = s4procinst(u"?>")
			lines = node.content.splitlines()
			if len(lines)>1:
				lines.insert(0, u"")
			for line in self._domultiline(node, lines, 1, self.strProcInstContentLine, head, tail):
				yield line

	def presentComment(self, node):
		if self._inattr:
			self._buffers[-1] += s4comment(
				u"<!--",
				EnvTextForCommentText(EscOutlineAttr(node.content)),
				u"-->",
			)
		else:
			head = s4comment(u"<!--")
			tail = s4comment(u"-->")
			lines = node.content.splitlines()
			for line in self._domultiline(node, lines, 1, self.strCommentTextLine, head, tail):
				yield line

	def presentDocType(self, node):
		if self._inattr:
			self._buffers[-1] += s4doctype(
				u"<!DOCTYPE ",
				EnvTextForDocTypeText(EscOutlineAttr(node.content)),
				u">",
			)
		else:
			head = s4doctype(u"<!DOCTYPE ")
			tail = s4doctype(u">")
			lines = node.content.splitlines()
			for line in self._domultiline(node, lines, 1, self.strDocTypeTextLine, head, tail):
				yield line

	def presentAttr(self, node):
		if self._inattr:
			# this will not be popped at the and of this method, because presentElement needs it
			self._buffers.append(s4attrvalue())
		for line in self.presentFrag(node):
			yield line


class CodePresenter(Presenter):
	"""
	<par>This presenter formats the object as a nested Python object tree.</par>
	
	<par>This makes it possible to quickly convert &html;/&xml; files to &xist;
	constructor calls.</par>
	"""
	def __init__(self, node, indent="\t"):
		Presenter.__init__(self, node)
		self.indent = indent

	def __str__(self):
		return "\n".join(self)

	def present(self, node):
		self._inattr = 0
		self._level = 0
		for part in node.present(self):
			yield part
		del self._level
		del self._inattr

	def __xiter__(self, mode="default"):
		return self.present(self.node)

	def _indent(self):
		if self._inattr:
			return ""
		else:
			return self.indent*self._level

	def _text(self, text):
		# Find the simplest object to display
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
		if len(node):
			if not self._inattr: # skip "(" for attributes, they will be added by presentElement()
				yield "%s%s.%s(" % (self._indent(), node.__class__.__module__, node.__fullname__())
			self._level += 1
			for (i, child) in enumerate(node):
				if i==len(node)-1:
					for line in child.present(self):
						yield line
				else:
					lines = list(child.present(self))
					for (j, line) in enumerate(lines):
						if i==len(node)-1:
							yield line
						else:
							yield "%s," % line
			self._level -= 1
			if not self._inattr:
				yield "%s)" % self._indent()
		else:
			if not self._inattr:
				yield "%s%s.%s()" % (self._indent(), node.__class__.__module__, node.__fullname__())

	def presentAttrs(self, node):
		if len(node):
			globalattrs = {}
			localattrs = {}
			for (attrname, attrvalue) in node.iteritems():
				if isinstance(attrname, tuple):
					globalattrs[attrname] = attrvalue
				else:
					localattrs[attrname] = attrvalue

			yield "%s%s.%s(" % (self._indent(), node.__class__.__module__, node.__fullname__())
			self._level += 1
			if globalattrs:
				yield "%s{" % self._indent()
				for (i, (attrname, attrvalue)) in enumerate(globalattrs.iteritems()):
					attrname = "(%s, %r)" % (attrname[0].__module__, attrname[1])
					self._inattr += 1
					if len(attrvalue)==1: # optimize away the tuple ()
						attrvalue = " ".join(attrvalue[0].present(self))
					else:
						attrvalue = "(%s)" % " ".join(attrvalue.present(self))
					self._inattr -= 1
					self._level += 1
					line = "%s%s: %s" % (self._indent(), attrname, attrvalue)
					if i != len(globalattrs) or not localattrs:
						line += ","
					yield line
					self._level -= 1
				line = "%s}" % self._indent()
				if localattrs:
					line += ","
				yield line
			for (i, (attrname, attrvalue)) in enumerate(localattrs.iteritems()):
				self._inattr += 1
				if len(attrvalue)==1: # optimize away the tuple ()
					attrvalue = " ".join(attrvalue[0].present(self))
				else:
					attrvalue = "(%s)" % " ".join(attrvalue.present(self))
				self._inattr -= 1
				line = "%s%s=%s" % (self._indent(), attrname, attrvalue)
				if i != len(localattrs)-1:
					line += ","
				yield line
			self._level -= 1
			yield "%s)" % self._indent()
		else:
			yield "%s%s.%s()" % (self._indent(), node.__class__.__module__, node.__fullname__())

	def presentElement(self, node):
		if len(node.content) or len(node.attrs):
			yield "%s%s.%s(" % (self._indent(), node.__class__.__module__, node.__fullname__())

			self._level += 1
			for (i, child) in enumerate(node):
				if i==len(node)-1 and not node.attrs:
					for line in child.present(self):
						yield line
				else:
					lines = list(child.present(self))
					for (j, line) in enumerate(lines):
						if j == len(lines)-1:
							line += ","
						yield line

			globalattrs = {}
			localattrs = {}
			for (attrname, attrvalue) in node.attrs.iteritems():
				if isinstance(attrname, tuple):
					globalattrs[attrname] = attrvalue
				else:
					localattrs[attrname] = attrvalue

			if globalattrs:
				yield "%s{" % self._indent()
				for (i, (attrname, attrvalue)) in enumerate(globalattrs.iteritems()):
					attrname = "(%s, %r)" % (attrname[0].__module__, attrname[1])
					self._inattr += 1
					if len(attrvalue)==1: # optimize away the tuple ()
						attrvalue = " ".join(attrvalue[0].present(self))
					else:
						attrvalue = "(%s)" % " ".join(attrvalue.present(self))
					self._inattr -= 1
					self._level += 1
					line = "%s%s: %s" % (self._indent(), attrname, attrvalue)
					if i != len(globalattrs) or not localattrs:
						line += ","
					yield line
					self._level -= 1
				line = "%s}" % self._indent()
				if localattrs:
					line += ","
				yield line
			for (i, (attrname, attrvalue)) in enumerate(localattrs.iteritems()):
				self._inattr += 1
				if len(attrvalue)==1: # optimize away the tuple ()
					attrvalue = " ".join(attrvalue[0].present(self))
				else:
					attrvalue = "(%s)" % " ".join(attrvalue.present(self))
				self._inattr -= 1
				line = "%s%s=%s" % (self._indent(), attrname, attrvalue)
				if i != len(localattrs)-1:
					line += ","
				yield line
			self._level -= 1
			yield "%s)" % self._indent()
		else:
			yield "%s%s.%s()" % (self._indent(), node.__class__.__module__, node.__fullname__())

	def presentNull(self, node):
		yield "%sxsc.Null" % self._indent()

	def presentText(self, node):
		yield "%s%r" % (self._indent(), self._text(node.content))

	def presentEntity(self, node):
		yield "%s%s.%s()" % (self._indent(), node.__module__, node.__fullname__())

	def presentProcInst(self, node):
		yield "%s%s.%s(%r)" % (self._indent(), node.__module__, node.__fullname__(), self._text(node.content))

	def presentComment(self, node):
		yield "%sxsc.Comment(%r)" % (self._indent(), self._text(node.content))

	def presentDocType(self, node):
		yield "%sxsc.DocType(%r)" % (self._indent(), self._text(node.content))

	def presentAttr(self, node):
		return self.presentFrag(node)


defaultpresenter = PlainPresenter # used for __repr__
hookpresenter = TreePresenter # used in the displayhook below


def displayhook(out, obj):
	if isinstance(obj, xsc.Node):
		encoding = getattr(sys.stdout, "encoding", sys.getdefaultencoding())
		for part in obj.repr(hookpresenter(encoding=encoding)):
			out.write(part)
		out.write("\n")
		return True
	return False
