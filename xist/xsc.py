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
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import os
import os.path
import string
import types
import exceptions
import sys
import getopt

# for file size checking
import stat

# for image size checking
import Image

# for parsing XML files
from xml.parsers import xmllib

# for reading remote files
import urllib

# our sandbox
import procinst

# our own new URL class
from URL import URL

###
### exceptions
###

class Error(Exception):
	"""
	base class for all XSC exceptions
	"""

	def __init__(self,lineno):
		self.lineno = lineno

	def __str__(self):
		if self.lineno>0:
			return " (line " + str(self.lineno) + ")"
		else:
			return ""

class EmptyElementWithContentError(Error):
	"""
	exception that is raised, when an element has content,
	but it shouldn't (i.e. empty==1)
	"""

	def __init__(self,lineno,element):
		Error.__init__(self,lineno)
		self.element = element

	def __str__(self):
		return Error.__str__(self) + "element " + self.element._str() + " specified to be empty, but has content"

class IllegalAttributeError(Error):
	"""
	exception that is raised, when an element has an illegal attribute
	(i.e. one that isn't contained in it's attrHandlers)
	"""

	def __init__(self,lineno,element,attr):
		Error.__init__(self,lineno)
		self.element = element
		self.attr = attr

	def __str__(self):
		attrs = self.element.attrHandlers.keys();
		attrs.sort()

		v = []

		for attr in attrs:
			v.append(strAttrName(attr))

		return Error.__str__(self) + "Attribute " + strAttrName(self.attr) + " not allowed in element " + self.element._str() + ". Allowed attributes are: " + string.join(v,", ") + "."

class AttributeNotFoundError(Error):
	"""
	exception that is raised, when an attribute is fetched that isn't there
	"""

	def __init__(self,lineno,element,attr):
		Error.__init__(self,lineno)
		self.element = element
		self.attr = attr

	def __str__(self):
		attrs = self.element.attrs.keys();

		s = Error.__str__(self) + "Attribute " + strAttrName(self.attr) + " not found in element " + self.element._str() +". "

		if len(attrs):
			attrs.sort()
			v = []
			for attr in attrs:
				v.append(strAttrName(attr))
			s = s + "Available attributes are: " + string.join(v,", ") + "."
		else:
			s = s + "No attributes available."

		return s

class IllegalElementError(Error):
	"""
	exception that is raised, when an illegal element is encountered
	(i.e. one that isn't registered via registerElement
	"""

	def __init__(self,lineno,name):
		Error.__init__(self,lineno)
		self.name = name

	def __str__(self):
		elementnames = []
		for elementname in _elementHandlers.keys():
			for namespace in _elementHandlers[elementname].keys():
				elementnames.append(_strNode(_elementHandlers[elementname][namespace],brackets = 1))
		elementnames.sort()

		s = Error.__str__(self) + "element " + _strName((self.name[0],self.name[1],0)) + " not allowed. "
		if elementnames:
			s = s + "Allowed elements are: " + string.join(elementnames,", ") + "."
		else:
			s = s + "There are no allowed elements."
		return s

class IllegalElementNestingError(Error):
	"""
	exception that is raised, when an element has an illegal nesting
	(e.g. <a><b></a></b>)
	"""

	def __init__(self,lineno,expectedelement,foundelement):
		Error.__init__(self,lineno)
		self.expectedelement = expectedelement
		self.foundelement = foundelement

	def __str__(self):
		return Error.__str__(self) + "illegal element nesting (" + _strNode(self.expectedelement) + " expected; " + _strNode(self.foundelement) + " found)"

class ImageSizeFormatError(Error):
	"""
	exception that is raised, when XSC can't format or evaluate image size attributes
	"""

	def __init__(self,lineno,element,attr):
		Error.__init__(self,lineno)
		self.element = element
		self.attr = attr

	def __str__(self):
		return Error.__str__(self) + "the value '" + self.element[self.attr].asPlainString() + "' for the image size attribute " + strAttrName(self.attr) + " of the element " + self.element._str() + " can't be formatted or evaluated"

class FileNotFoundError(Error):
	"""
	exception that is raised, when XSC can't open an image for getting image size
	"""

	def __init__(self,lineno,url):
		Error.__init__(self,lineno)
		self.url = url

	def __str__(self):
		return Error.__str__(self) + "file " + strURL(str(self.url)) + " can't be opened"

class IllegalObjectError(Error):
	"""
	exception that is raised, when XSC finds an illegal object in its object tree
	"""

	def __init__(self,lineno,object):
		Error.__init__(self,lineno)
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

	def __init__(self,lineno,name):
		Error.__init__(self,lineno)
		self.name = name

	def __str__(self):
		return Error.__str__(self) + "malformed character reference: &#" + self.name + ";"

class UnknownEntityError(Error):
	"""
	exception that is raised, when an unknown entity is encountered
	(i.e. one that wasn't registered via registerEntity)
	"""

	def __init__(self,lineno,name):
		Error.__init__(self,lineno)
		self.name = name

	def __str__(self):
		return Error.__str__(self) + "Unknown entitiy: &" + self.name + ";"

class AmbiguousElementError(Error):
	"""
	exception that is raised, when an element is encountered without a namespace
	and there is more than one element registered with this name.
	"""

	def __init__(self,lineno,name):
		Error.__init__(self,lineno)
		self.name = name

	def __str__(self):
		elementnames = []
		for namespace in _elementHandlers[self.name[1]].keys():
			elementnames.append(_strNode(_elementHandlers[self.name[1]][namespace]))
		elementnames.sort()

		return Error.__str__(self) + "element " + _strName((self.name[0],self.name[1],0)) + " is ambigous. Possible elements are: " + string.join(elementnames,", ") + "."

###
### configuration
###

# should remote URLs be retrieved? (for filesize and imagesize tests)
try:
	retrieveremote = string.atoi(os.environ["XSC_RETRIEVEREMOTE"])
except KeyError:
	retrieveremote = 1

# should local URLs be retrieved? (for filesize and imagesize tests)
try:
	retrievelocal = string.atoi(os.environ["XSC_RETRIEVELOCAL"])
except KeyError:
	retrievelocal = 1

# chracters with an ASCII (or Unix) code above reprcharreflowerlimit wll be dumped as charcter references
try:
	reprcharreflowerlimit = string.atoi(os.environ["XSC_REPRCHARREFLOWERLIMIT"])
except KeyError:
	reprcharreflowerlimit = 128

# should ANSI escape sequences be used for dumping the DOM tree?
try:
	repransi = string.atoi(os.environ["XSC_REPRANSI"])
except KeyError:
	repransi = 0

# how to represent an indentation in the DOM tree
try:
	reprtab = os.environ["XSC_REPRTAB"]
except KeyError:
	reprtab = ". "

# should the default ANSI escape sequences be a terminal with a dark or light background?
try:
	repransidark = string.atoi(os.environ["XSC_REPRANSI_DARK"])
except KeyError:
	repransidark = 1

# ANSI escape sequence to be used for tabs
try:
	repransitab = os.environ["XSC_REPRANSI_TAB"]
except KeyError:
	repransitab = "1;34"

# ANSI escape sequence to be used for quotes (delimiters for text and attribute nodes)
try:
	repransiquote = os.environ["XSC_REPRANSI_QUOTE"]
except KeyError:
	repransiquote = "1;32"

# ANSI escape sequence to be used for slashes in element names
try:
	repransislash = os.environ["XSC_REPRANSI_SLASH"]
except KeyError:
	repransislash = ""

# ANSI escape sequence to be used for brackets (delimiters for tags)
try:
	repransibracket = os.environ["XSC_REPRANSI_BRACKET"]
except KeyError:
	repransibracket = "1;32"

# ANSI escape sequence to be used for question marks (delimiters for processing instructions)
try:
	repransiquestion = os.environ["XSC_REPRANSI_QUESTION"]
except KeyError:
	repransiquestion = "1;32"

# ANSI escape sequence to be used for text
try:
	repransitext = os.environ["XSC_REPRANSI_TEXT"]
except KeyError:
	repransitext = ""

# ANSI escape sequence to be used for character references
try:
	repransicharref = os.environ["XSC_REPRANSI_CHARREF"]
except KeyError:
	repransicharref = "37"

# ANSI escape sequence to be used for element namespaces
try:
	repransielementnamespace = os.environ["XSC_REPRANSI_ELEMENTNAMESPACE"]
except KeyError:
	repransielementnamespace = "1;36"

# ANSI escape sequence to be used for element names
try:
	repransielementname = os.environ["XSC_REPRANSI_ELEMENTNAME"]
except KeyError:
	repransielementname = "1;36"

# ANSI escape sequence to be used for attribute names
try:
	repransiattrname = os.environ["XSC_REPRANSI_ATTRNAME"]
except KeyError:
	repransiattrname = "1;36"

# ANSI escape sequence to be used for document types
try:
	repransidoctype = os.environ["XSC_REPRANSI_DOCTYPE"]
except KeyError:
	repransidoctype = ""

# ANSI escape sequence to be used for attribute values
try:
	repransiattrvalue = os.environ["XSC_REPRANSI_ATTRVALUE"]
except KeyError:
	repransiattrvalue = ""

# ANSI escape sequence to be used for URLs
try:
	repransiurl = os.environ["XSC_REPRANSI_URL"]
except KeyError:
	repransiurl = "1;33"

# ANSI escape sequence to be used for processing instruction targets
try:
	repransiprocinsttarget = os.environ["XSC_REPRANSI_PROCINSTTARGET"]
except KeyError:
	repransiprocinsttarget = "1;31"

# ANSI escape sequence to be used for processing instruction data
try:
	repransiprocinstdata = os.environ["XSC_REPRANSI_PROCINSTDATA"]
except KeyError:
	repransiprocinstdata = ""

###
### helpers
###

def _stransi(codes,string,ansi = None):
	if ansi is None:
		ansi = repransi
	if ansi==1 and codes!="" and string!="":
		return "\033[" + codes + "m" + string + "\033[0m"
	else:
		return string

def strElementNameSpace(elementnamespace,ansi = None):
	return _stransi(repransielementnamespace,elementnamespace,ansi)

def strElementName(elementname,ansi = None):
	return _stransi(repransielementname,elementname,ansi)

def strAttrName(attrname,ansi = None):
	return _stransi(repransiattrname,attrname,ansi)

def strAttrValue(attrvalue,ansi = None):
	return _stransi(repransiattrvalue,attrvalue,ansi)

def strCharRef(charref,ansi = None):
	return _stransi(repransicharref,charref,ansi = ansi)

def strDocType(doctype,ansi = None):
	return _stransi(repransidoctype,doctype,ansi = ansi)

def strProcInstTarget(target,ansi = None):
	return _stransi(repransiprocinsttarget,target,ansi = ansi)

def strProcInstData(data,ansi = None):
	return _stransi(repransiprocinstdata,data,ansi = ansi)

def strText(text,ansi = None):
	return _stransi(repransitext,text,ansi = ansi)

def strSlash(attrname,ansi = None):
	return _stransi(repransislash,"/",ansi)

def strBracketOpen(attrname,ansi = None):
	return _stransi(repransibracket,"<",ansi)

def strBracketClose(attrname,ansi = None):
	return _stransi(repransibracket,">",ansi)

def strQuestion(ansi = None):
	return _stransi(repransiquestion,"?",ansi)

def strQuote(ansi = None):
	return _stransi(repransiquote,'"',ansi)

def strTab(count,ansi = None):
	return _stransi(repransitab,reprtab*count,ansi = ansi)

def strURL(URL,ansi = None):
	return _stransi(repransiurl,URL,ansi)

def nameOfMainModule():
	if len(sys.argv)>0:
		return os.path.splitext(os.path.split(sys.argv[0])[1])[0]
	else:
		return "__main__"

def namespaceName(nodeClass):
	namespace = nodeClass.__module__
	if namespace == "__main__": # the element class came from the main module, get the name from sys.argv
		namespace = string.lower(nameOfMainModule())
	else:
		namespace = string.lower(namespace)
	return namespace

def elementName(nodeClass):
	return string.lower(nodeClass.__name__)
	
def nodeName(nodeClass):
	"""
	returns a tuple with the namespace of the node, which is the module in which the node is implemented
	and a name which is the name of the class. Both strings are converted to lowercase.
	"""
	return [namespaceName(nodeClass),elementName(nodeClass),nodeClass.empty]

def _strName(nodeName,content = None,brackets = 1,slash = None,ansi = None):
	# slash == -1: before; 0: nowhere; 1:after
	if slash is None:
		if nodeName is None:
			slash = 0
		else:
			slash = nodeName[2]
	s = ""
	if slash < 0:
		s = s + strSlash(ansi)
	if nodeName is not None:
		if nodeName[0]:
			s = s + strElementNameSpace(nodeName[0],ansi) + ":"
		s = s + strElementName(nodeName[1],ansi)
	if content is not None and slash>=0:
		s = s + content
	if slash > 0:
		s = s + strSlash(ansi)
	if brackets is not None:
		s = strBracketOpen(ansi) + s + strBracketClose(ansi)
	return s

def _strNode(nodeClass,content = None,brackets = None,slash = None,ansi = None):
	name = nodeName(nodeClass)
	return _strName(name,content,brackets,slash,ansi)

def appendDict(*dicts):
	result = {}
	for dict in dicts:
		for key in dict.keys():
			result[key] = dict[key]
	return result

def string2Fragment(s):
	"""
	parses a string that might contain entities into a fragment
	with text nodes and character references.
	"""
	e = Frag()
	while 1:
		try:
			i = string.index(s,"&")
			if i != 0:
				e.append(s[:i])
				s = s[i:]
			try:
				i = string.index(s,";")
				if s[1] == "#":
					if s[2] == "x":
						e.append(CharRef(string.atoi(s[3:i],16)))
					else:
						e.append(CharRef(string.atoi(s[2:i])))
				else:
					try:
						e.append(Parser.entitiesByName[s[1:i]])
					except KeyError:
						raise UnknownEntityError(xsc.parser.lineno,s[1:i])
				s = s[i+1:]
			except ValueError:
				raise MalformedCharRefError(xsc.parser.lineno,s)
		except ValueError:
			if len(s):
				e.append(s)
			break
	return e

def ToNode(value):
	t = type(value)
	if t == types.InstanceType:
		if isinstance(value,Frag):
			l = len(value)
			if l==1:
				return ToNode(value[0]) # recursively try to simplify the tree
			elif l==0:
				return Null()
			else:
				if isinstance(value,Attr):
					e = Frag() # repack the attribute in a fragment, and we have a valid XSC node
					for i in value:
						e.append(ToNode(i))
					return e
				else:
					return value
		elif isinstance(value,Node):
			return value
	elif t in [ types.StringType,types.IntType,types.LongType,types.FloatType ]:
		return Text(value)
	elif t == types.NoneType:
		return Null()
	elif t in [ types.ListType,types.TupleType ]:
		l = len(value)
		if l==1:
			return ToNode(value[0]) # recursively try to simplify the tree
		elif l==0:
			return Null()
		else:
			e = Frag()
			for i in value:
				e.append(ToNode(i))
			return e
	raise IllegalObjectError(xsc.parser.lineno,value) # none of the above, so we throw and exception

_elementHandlers = {} # dictionary for mapping element names to classes, this dictionary contains the element names as keys and another dictionary as values, this second dictionary contains the namespace names as keys and the element classes as values

class Node:
	"""
	base class for nodes in the document tree. Derived classes must
	implement asHTML() and/or __str__()
	"""

	empty = 1

	# line numbers where this node starts and ends in a file (will be hidden in derived classes, but is specified here, so that no special tests are required. In derived classes both variables will be set by the parser)
	startlineno = -1
	endlineno = -1

	repransinamespace = "31"
	repransiname = ""

	def __repr__(self):
		if xsc.reprtree == 1:
			return self.reprtree()
		else:
			return self.repr()

	def name(self):
		"""
		returns a tuple with the namespace of the node, which is the module
		in which the node is implemented and a name which is the name of the
		class. Both strings are converted to lowercase.
		"""
		return nodeName(self.__class__)

	def _str(self,content = None,brackets = 1,slash = None,ansi = None):
		return _strNode(self.__class__,content,brackets,slash,ansi)

	def clone(self):
		"""
		returns an identical clone of the node and it's children.
		"""
		pass

	def repr(self,ansi = None):
		return self._dorepr(ansi)

	def reprtree(self,ansi = None):
		nest = 0
		v = []
		lines = self._doreprtree(nest,[],ansi = ansi)
		lenlineno = 0
		lenelementno = 0
		for line in lines:
			if line[1] != -1: # convert line number to a string
				line[1] = str(line[1])
			else:
				line[1] = "?"
			line[2] = string.join(map(str,line[2]),".") # convert element number to a string
			line[3] = strTab(line[0]) + line[3] # add indentation
			lenlineno = max(lenlineno,len(line[1]))
			lenelementno = max(lenelementno,len(line[2]))

		for line in lines:
			v.append("%*s %-*s %s\n" % (lenlineno,line[1],lenelementno,line[2],line[3]))
		return string.join(v,"")

	def _dorepr(self,ansi = None):
		# returns a string representation of the node
		return self._str(brackets = 1,ansi = ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		# returns and array containing arrays consisting of the (nestinglevel,linenumber,elementnumber,string representation) of the nodes
		return [[nest,self.startlineno,elementno,self._dorepr(ansi)]]

	def asHTML(self):
		"""
		returns a version of this Node and it's content converted to HTML,
		so when you define your own element classes you should overwrite asHTML().

		E.g. when you want to define an element that packs it's content into an HTML
		bold element, do the following:

		def foo(xsc.Element):
			empty = 0

			def asHTML(self):
				return html.b(self.content).asHTML()
		"""
		return Null()

	def asPlainString(self):
		"""
		returns this node as a string without any character references.
		Comments and processing instructions will be filtered out.
		For elements you'll get the element content.

		It might be useful to overwrite this function in your own
		elements. Suppose you have the following element:

		class caps(xsc.Element):
			empty = 0

			def asHTML(self):
				return html.span(self.content,style="font-variant: small-caps;").asHTML()

		that renders its content in small caps, then it might be useful
		to define asPlainString in the following way:

			def asPlainString(self):
				return string.upper(self.content.asPlainString())

		E.g. asPlainString might be used the construct a title element
		for a page for a part of the content of the page.
		"""
		return ""

	def asInt(self):
		"""
		returns this node converted to an integer.
		"""
		return string.atoi(self.asPlainString())

	def __str__(self):
		"""
		returns this element as a string
		"""
		return ""

	def nodes(self,type = None,subtype = 0,children = 0,attrs = 0):
		"""
		returns a fragment which contains child elements of this node.

		If you specify type as the class of an XSC node only nodes of this class
		will be returned.

		If you set subtype to 1 nodes that are a subtype of type will be returned too.

		If you set children to 1 not only the immediate children but also the grandchildren
		will be searched for nodes matching the other criteria.

		If you set attrs to 1 the attributes of the nodes (if type is Element or one
		of it's subtypes) will be searched too.
		"""
		return Frag()

	def _nodeOK(self,type,subtype):
		if type is not None:
			if subtype:
				return isinstance(self,type)
			else:
				return self.__class__ == type
		else:
			return 1

	def compact(self):
		"""
		returns this node, where textnodes or character references that contain
		only linefeeds are removed, i.e. potentially needless whitespace is removed.
		"""
		return Null()

class Text(Node):
	"""
	text node. The characters <, >, & and " will be "escaped" with the
	appropriate character entities. Characters with an ASCII code bigger
	than 127 will be escaped too.
	"""

	empty = 1

	repransiname = ""

	strescapes = { '<' : 'lt' , '>' : 'gt' , '&' : 'amp' , '"' : 'quot' }

	def __init__(self,_content = ""):
		self.content = str(_content)

	def asHTML(self):
		return Text(self.content)

	clone = asHTML

	def asPlainString(self):
		return self.content

	def __str__(self):
		v = []
		for i in self.content:
			if i == '\r':
				continue
			if self.strescapes.has_key(i):
				v.append('&' + self.strescapes[i] + ';')
			elif ord(i)>=128:
				v.append('&#' + str(ord(i)) + ';')
			else:
				v.append(i)
		return string.join(v,"")

	def __strtext(self,refwhite,content,ansi = None):
		# we could put ANSI escapes around every character or reference that we output, but this would result in strings that are way to long, especially if output over a serial connection, so we collect runs of characters with the same highlighting and put the ANSI escapes around those. (of course, when we're not doing highlighting, this routine does way to much useless calculations)
		v = [] # collect all colored string here
		charref = -1 # the type of characters we're currently collecting (0==normal character, 1==character that has to be output as an entity, -1==at the start)
		start = 0 # the position where our current run of characters for the same class started
		end = 0 # the current position we're testing
		while end<=len(content): # one more than the length of the string
			do = 0 # we will have to do something with the string collected so far ...
			if end == len(content): # ... if we're at the end of the string ...
				do = 1
			else:
				c = content[end] # ... or if the character we're at is different from those we've collected so far
				ascharref = (0 <= ord(c) <= 31 or reprcharreflowerlimit <= ord(c))
				if not refwhite and (c == "\n" or c == "\t"):
					ascharref = 0
				if ascharref != charref:
					do = 1
					charref = 1-ascharref # this does nothing, except at the start, where it enforces the correct processing
			if do: # process the string we have so far
				if charref: # we've collected references so far
					s = ""
					for i in content[start:end]:
						ent = Parser.entitiesByNumber[ord(i)] # use names if a available, or number otherwise
						if len(ent):
							s = s + '&' + ent[0] + ';'
						else:
							s = s + '&#' + str(ord(i)) + ';'
					v.append(strCharRef(s,ansi))
				else:
					s = content[start:end]
					v.append(strText(s,ansi))
				charref = 1-charref # switch to the other class
				start = end # the next string we want to work on starts from here
			end = end + 1 # to the next character
		return string.join(v,"")

	def _dorepr(self,ansi = None):
		# constructs a string of this Text with syntaxhighlighting. Special characters will be output as CharRefs (with special highlighting)
		return self.__strtext(0,self.content,ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		lines = string.split(self.content,"\n")
		if len(lines) and lines[-1] == "":
			del lines[-1]
		v = []
		for i in xrange(len(lines)):
			if self.startlineno == -1:
				no = -1
			else:
				no = self.startlineno + i
			s = strQuote(ansi) + strText(self.__strtext(1,lines[i],ansi),ansi) + strQuote(ansi)
			v.append([nest,no,elementno,s])
		return v

	def compact(self):
		for i in self.content:
			if i != '\n' and i != '\r':
				return Text(self.content)
		else:
			return Null()

class CharRef(Node):
	"""
	character reference (i.e &#42; or &#x42; or &uuml;) The content member
	of the node will be the ASCII code of the character.
	"""

	repransiname = "32"

	__notdirect = { ord("&") : "amp" , ord("<") : "lt" , ord(">") : "gt", ord('"') : "quot" , ord("'") : "apos" }
	__linefeeds = [ ord("\r") , ord("\n") ]

	def __init__(self,_content = 42):
		self.content = _content

	def asHTML(self):
		return CharRef(self.content)

	clone = asHTML

	def asPlainString(self):
		return chr(self.content)

	def __str__(self):
		if 0<=self.content<=127:
			if self.content != ord("\r"):
				if self.__notdirect.has_key(self.content):
					return '&' + self.__notdirect[self.content] + ';'
				else:
					return chr(self.content)
		else:
			return '&#' + str(self.content) + ';'

	def __strcharref(self,s,ansi = None):
		return strCharRef(s,ansi)

	def _dorepr(self,ansi):
		if len(Parser.entitiesByNumber[self.content]):
			return self.__strcharref('&' + Parser.entitiesByNumber[self.content][0] + ';',ansi)
		else:
			return self.__strcharref('&#' + str(self.content) + ';',ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		s = self.__strcharref('&#' + str(self.content) + ';',ansi) + ' (' + self.__strcharref('&#x' + hex(self.content)[2:] + ';',ansi)
		for name in Parser.entitiesByNumber[self.content]:
			s = s + ' ' + self.__strcharref('&' + name + ';',ansi)
		s = s + ')'
		if 0 <= self.content < reprcharreflowerlimit:
			s = s + ' ' + Text(chr(self.content))._doreprtree(0,0,ansi)[0][-1]
		return [[nest,self.startlineno,elementno,s]]

	def compact(self):
		if self.content in self.__linefeeds:
			return Null()
		else:
			return CharRef(self.content)

class Frag(Node):
	"""
	A fragment contains a list of nodes and can be used for dynamically constructing content.
	The member content of an Element is a Frag.
	"""

	empty = 0

	repransiname = ""

	def __init__(self,*_content):
		self.__content = []
		for child in _content:
			self.extend(child)

	def asHTML(self):
		e = self.__class__()
		for child in self:
			e.append(child.asHTML())
		return e

	def clone(self):
		e = self.__class__()
		for child in self:
			e.append(child.clone())
		return e

	def _dorepr(self,ansi = None):
		v = []
		for child in self:
			v.append(child._dorepr(ansi = ansi))
		return string.join(v,"")

	def _doreprtree(self,nest,elementno,ansi = None):
		v = []
		if len(self):
			v.append([nest,self.startlineno,elementno,self._str(brackets = 1,ansi = ansi)])
			i = 0
			for child in self:
				v = v + child._doreprtree(nest+1,elementno + [i],ansi)
				i = i + 1
			v.append([nest,self.endlineno,elementno,self._str(brackets = 1,ansi = ansi,slash = -1)])
		else:
			v.append([nest,self.startlineno,elementno,self._str(brackets = 1,ansi = ansi,slash = 1)])
		return v

	def asPlainString(self):
		v = []
		for child in self:
			v.append(child.asPlainString())
		return string.join(v,"")

	def __str__(self):
		v = []
		for child in self:
			v.append(str(child))
		return string.join(v,"")

	def __getitem__(self,index):
		"""
		returns the index'th node for the content of the fragment
		"""
		return self.__content[index]

	def __setitem__(self,index,value):
		"""
		allows you to replace the index'th content node of the fragment
		"""
		if len(self.__content)>index:
			self.__content[index] = ToNode(value)

	def __delitem__(self,index):
		"""
		removes the index'th content node from the fragment
		"""
		if len(self.__content)>index:
			del self.__content[index]

	def __getslice__(self,index1,index2):
		"""
		returns a slice of the content of the fragment
		"""
		e = self.__class__()
		for child in self.__content[index1:index2]:
			e.append(child)
		return e

	def __setslice__(self,index1,index2,sequence):
		"""
		replaces a slice of the content of the fragment
		"""
		self.__content[index1:index2] = map(ToNode,sequence)

	def __delslice__(self,index1,index2):
		"""
		removes a slice of the content of the fragment
		"""
		del self.__content[index1:index2]

	def __len__(self):
		"""
		return the number of children
		"""
		return len(self.__content)

	def append(self,other):
		"""
		appends the item to the fragment.
		"""
		newother = ToNode(other)
		if not isinstance(newother,Null):
			self.__content.append(newother)

	def insert(self,index,other):
		"""
		inserts the item into the fragment at the position index.
		"""
		newother = ToNode(other)
		if not isinstance(newother,Null):
			self.__content.insert(index,newother)

	def extend(self,other):
		"""
		appends the items in the other object to the fragment.
		"""
		newother = ToNode(other)
		if isinstance(newother,Frag):
			for child in newother:
				self.__content.append(child)
		elif not isinstance(newother,Null):
			self.__content.append(newother)

	def nodes(self,type = None,subtype = 0,children = 0,attrs = 0):
		e = Frag()
		for child in self:
			if child._nodeOK(type,subtype):
				e.append(child)
			if children:
				e.extend(child.nodes(type,subtype,children,attrs))
		return e

	def compact(self):
		e = self.__class__()
		for child in self:
			e.append(child.compact())
		return e

	def addSeparator(self,separator):
		e = Frag()
		newseparator = ToNode(separator)
		for child in self:
			if len(e):
				e.append(newseparator.clone())
			e.append(child)
		return e

class Comment(Node):
	"""
	a comment node
	"""

	repransiname = ""

	def __init__(self,content = ""):
		self.__content = content

	def asHTML(self):
		return Comment(self.__content)

	clone = asHTML

	def _dorepr(self,ansi = None):
		return self._str(content = "!--" + self.__content + "--",brackets = 1,ansi = ansi)

	def _doreprtree(self,nest,elementno,ansi):
		return [[nest,self.startlineno,elementno,self._dorepr(ansi)]]

	def __str__(self):
		return "<!--" + self.__content + "-->"

	def compact(self):
		return Comment(self.__content)

class DocType(Node):
	"""
	a document type node
	"""

	repransiname = ""

	def __init__(self,content = ""):
		self.__content = content

	def asHTML(self):
		return DocType(self.__content)

	clone = asHTML

	def _dorepr(self,ansi = None):
		return self._str(content = strDocType("!DOCTYPE " + self.__content,ansi),brackets = 1,ansi = ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		return [[nest,self.startlineno,elementno,self._dorepr(ansi)]]

	def __str__(self):
		return "<!DOCTYPE " + self.__content + ">"

	def compact(self):
		return DocType(self.__content)

class ProcInst(Node):
	"""
	processing instructions.

	There are two special targets available:

	xsc:exec (e.g. <?xsc:exec pass?>)
	here the content of the processing instruction is executed
	as Python code, so you can define and register XSC elements here.
	Execution is done when the node is constructed, so definitions made
	here will be available afterwards (e.g. during the rest of the
	file parsing stage). When converted to HTML such a node will result
	in an empty Null node.

	xsc:eval (e.g. <?xsc:eval return "foo"?>)
	here the code will be executed when the node is converted to HTML
	as if it was the body of a function, so you can return an expression
	here. Although the content is used as a function body no indentation
	is neccessary or allowed. The returned value will be converted to a
	node and this resulting node will be converted to HTML.

	All other processing instructions (XML, PHP, etc.) are passed through
	without processing of any kind.

	Note that you should not define the symbol __ in any of your XSC
	processing instructions, as it is used by XSC for internal purposes.
	"""

	repriansiname = "34"
	repransidata = "36"

	def __init__(self,target,content = ""):
		self.target = target
		self.content = content
		if string.lower(self.target) == "xsc:exec": # execute the code now, so that classes defined here are available for the parser
			exec self.content in procinst.__dict__

	def asHTML(self):
		if string.lower(self.target) == "xsc:exec": # XSC processing instruction, has been executed at construction time already, so we don't have to do anything here
			return Null()
		elif string.lower(self.target) == "xsc:eval": # XSC processing instruction,
			function = "def __():\n\t" + string.replace(string.strip(self.content),"\n","\n\t") + "\n"
			exec function in procinst.__dict__
			return ToNode(eval("__()",procinst.__dict__)).asHTML()
		else: # anything else like XML, PHP, etc. is just passed through
			return ProcInst(self.target,self.content)

	def clone(self):
		return ProcInst(self.target,self.content)

	def _dorepr(self,ansi = None):
		return self._str(content = strQuestion(ansi) + strProcInstTarget(self.target,ansi) + " " + strProcInstData(self.content,ansi) + strQuestion(ansi),brackets = 1,ansi = ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		lines = string.split(self.content,"\n")
		if len(lines) and lines[-1] == "":
			del lines[-1]
		if len(lines) == 1:
			s = self._str(content = strQuestion(ansi) + strProcInstTarget(self.target,ansi) + " " + strProcInstData(string.rstrip(lines[0]),ansi) + strQuestion(ansi),brackets = 1,ansi = ansi)
			return [[nest,self.startlineno,elementno,s]]
		else:
			v = []
			for i in xrange(len(lines)+2):
				if self.startlineno == -1:
					no = -1
				else:
					if i == 0:
						no = self.startlineno
					elif i == lines(lines) + 1:
						no = self.endlineno
					else:
						no = self.startlineno + i-1
				if i == 0:
					mynest = nest
					s = strBracketOpen(ansi) + strQuestion(ansi) + strProcInstTarget(self.target,ansi)
				elif i == len(lines)+1:
					mynest = nest
					s = strQuestion(ansi) + strBracketClose(ansi)
				else:
					mynest = nest+1
					s = lines[i-1]
					while len(s) and s[0] == "\t":
						mynest = mynest + 1
						s = s[1:]
					s = strProcInstData(string.rstrip(s),ansi)
				v.append([mynest,no,elementno,s])
			return v

	def __str__(self):
		return "<?" + self.target + " " + self.content + "?>"

	def compact(self):
		return ProcInst(self.target,self.content)

class Element(Node):
	"""
	XML/XSC elements.

	All elements implemented by the user must be derived from this class.

	If you not only want to construct a DOM tree via a Python script
	(by directly instantiating these classes), but to read an XML/XSC file
	you must register the element class with the parser, this can be done
	by passing the class object to the function registerElement().

	Every element class should have two class variables:
	empty: this is either 0 or 1 and specifies whether the element type is
	allowed to have content or not. Note that the parser does not use this
	as some sort of static DTD, i.e. you still must write your empty tags
	like this: <foo/>.
	attrHandlers: this is a dictionary that maps attribute names to attribute
	classes, which are all derived from Attr. Assigning to an attribute with
	a name that is not in attrHandlers.keys() is an error.
	"""

	repransiname = "34"

	empty = 1 # 0 => element with content; 1 => stand alone element
 	attrHandlers = {} # maps attribute names to attribute classes

	def __init__(self,*_content,**_attrs):
		self.content = Frag()
		self.attrs = {}
		for child in _content:
			if type(child) == types.DictionaryType:
				for attr in child.keys():
					self[attr] = child[attr]
			else:
				self.extend(child)
		for attr in _attrs.keys():
			self[attr] = _attrs[attr]

	def append(self,item):
		"""
		appends the item to the content of the element.
		"""
		newother = ToNode(item)
		if not isinstance(newother,Null):
			if self.empty:
				raise EmptyElementWithContentError(xsc.parser.lineno,self)
			else:
				self.content.append(item)

	def insert(self,index,item):
		"""
		inserts the item into the content of the element at the position index.
		"""
		newother = ToNode(item)
		if not isinstance(newother,Null):
			if self.empty:
				raise EmptyElementWithContentError(xsc.parser.lineno,self)
			else:
				self.content.insert(index,item)

	def extend(self,item):
		"""
		extend the elements by appending nodes in the other element
		"""
		newother = ToNode(item)
		if (not self.empty) or isinstance(newother,Null):
			self.content.extend(item)
		else:
			raise EmptyElementWithContentError(xsc.parser.lineno,self)

	def asHTML(self):
		e = self.__class__(self.content.asHTML()) # "virtual" copy constructor
		for attr in self.attrs.keys():
			e[attr] = self[attr].asHTML()
		return e

	def clone(self):
		e = self.__class__(self.content.clone()) # "virtual" copy constructor
		for attr in self.attrs.keys():
			e[attr] = self[attr].clone()
		return e

	def asPlainString(self):
		return self.content.asPlainString()

	def _dorepr(self,ansi = None):
		v = []
		if self.empty:
			v.append(self._str(content = self.__strattrs(ansi),brackets = 1,slash = 1,ansi = ansi))
		else:
			v.append(self._str(content = self.__strattrs(ansi),brackets = 1,ansi = ansi))
			for child in self:
				v.append(child._dorepr(ansi))
			v.append(self._str(brackets = 1,slash = -1,ansi = ansi))
		return string.join(v,"")

	def _doreprtree(self,nest,elementno,ansi = None):
		v = []
		if self.empty:
			v.append([nest,self.startlineno,elementno,self._str(content = self.__strattrs(ansi),brackets = 1,slash = 1,ansi = ansi)])
		else:
			v.append([nest,self.startlineno,elementno,self._str(content = self.__strattrs(ansi),brackets = 1,ansi = ansi)])
			i = 0
			for child in self:
				v = v + child._doreprtree(nest+1,elementno + [i],ansi)
				i = i + 1
			v.append([nest,self.endlineno,elementno,self._str(brackets = 1,slash = -1,ansi = ansi)])
		return v

	def __str__(self):
		v = []
		v.append("<")
		v.append(string.lower(self.__class__.__name__))
		for attr in self.attrs.keys():
			v.append(' ')
			v.append(attr)
			value = self[attr]
			if len(value):
				v.append('="')
				v.append(str(value))
				v.append('"')
		s = str(self.content)
		if self.empty:
			if len(s):
				raise EmptyElementWithContentError(xsc.parser.lineno,self)
			v.append(">")
		else:
			v.append(">")
			v.append(s)
			v.append("</")
			v.append(string.lower(self.__class__.__name__))
			v.append(">")

		return string.join(v,"")

	def __getitem__(self,index):
		"""
		returns an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number (i.e. content node index) is passed in.
		"""
		if type(index)==types.StringType:
			lowerindex = string.lower(index)
			try:
				return self.attrs[lowerindex] # we're returning the packed attribute here, because otherwise there would be no possibility to get an expanded URL
			except KeyError:
				raise AttributeNotFoundError(xsc.parser.lineno,self,index)
		else:
			return self.content[index]

	def __setitem__(self,index,value):
		"""
		sets an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number (i.e. content node index) is passed in.
		"""
		if type(index)==types.StringType:
			# values are contructed via the attribute classes specified in the attrHandlers dictionary, which do the conversion
			lowerindex = string.lower(index)
			try:
				attr = self.attrHandlers[lowerindex]() # pack the attribute into an attribute object
			except KeyError:
				raise IllegalAttributeError(xsc.parser.lineno,self,index)
			attr.extend(value)
			self.attrs[lowerindex] = attr
		else:
			self.content[index] = value

	def __delitem__(self,index):
		"""
		removes an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number (i.e. content node index) is passed in.
		"""
		if type(index)==types.StringType:
			lowerindex = string.lower(index)
			if self.attrs.has_key(lowerindex):
				del self.attrs[lowerindex]
		else:
			del self.content[index]

	def get_attr(self,attr,default):
		"""
		works like the method get() of dictionaries,
		it returns the attribute with the name attr, or if this doesn't exist,
		default (after converting it to a node and wrapping it into the
		appropriate attribute node.
		"""
		try:
			return self[attr]
		except AttributeNotFoundError:
			return self.attrHandlers[string.lower(attr)](default) # pack the attribute into an attribute object

	def __getslice__(self,index1,index2):
		"""
		returns a copy of the element that contains a slice of the content
		"""
		return self.__class__(self.content[index1:index2],self.attrs)

	def __setslice__(self,index1,index2,sequence):
		"""
		modifies a slice of the content of the element
		"""
		self.content[index1:index2] = sequence

	def __delslice__(self,index1,index2):
		"""
		removes a slice of the content of the element
		"""
		del self.content[index1:index2]

	def __len__(self):
		"""return the number of children"""
		return len(self.content)

	def has_attr(self,attr):
		return self.attrs.has_key(attr)

	def __strattrs(self,ansi = None):
		v = []
		for attr in self.attrs.keys():
			v.append(" ")
			v.append(strAttrName(attr,ansi))
			value = self[attr]
			if len(value):
				v.append('=')
				v.append(strQuote(ansi = ansi))
				v.append(value._dorepr(ansi = ansi))
				v.append(strQuote(ansi = ansi))
		return string.join(v,"")

	def AddImageSizeAttributes(self,imgattr,widthattr = "width",heightattr = "height"):
		"""add width and height attributes to the element for the image that can be found in the attributes imgattr. if the attribute is already there it is taken as a formating template with the size passed in as a dictionary with the keys 'width' and 'height', i.e. you could make your image twice as wide with width='%(width)d*2'"""

		if self.has_attr(imgattr):
			size = self[imgattr].ImageSize()
			sizedict = { "width": size[0], "height": size[1] }
			if size[0] != -1: # the width was retrieved so we can use it
				if self.has_attr(widthattr):
					try:
						self[widthattr] = eval(self[widthattr].asPlainString() % sizedict)
					except:
						raise ImageSizeFormatError(xsc.parser.lineno,self,widthattr)
				else:
					self[widthattr] = str(size[0])
			if size[1] != -1: # the height was retrieved so we can use it
				if self.has_attr(heightattr):
					try:
						self[heightattr] = eval(self[heightattr].asPlainString() % sizedict)
					except:
						raise ImageSizeFormatError(xsc.parser.lineno,self,heightattr)
				else:
					self[heightattr] = str(size[1])

	def compact(self):
		e = self.__class__(self.content.compact())
		for attr in self.attrs.keys():
			e[attr] = self[attr].compact()
		return e

	def nodes(self,type = None,subtype = 0,children = 0,attrs = 0):
		e = Frag()
		if attrs:
			for attr in self.attrs.keys():
				e.extend(self[attr].nodes(type,subtype,children,attr))
		e.extend(self.content.nodes(type,subtype,children,attrs))
		return e

class Null(Element):
	"""
	node that does not contain anything.
	"""

	repransiname = "33"

	def asHTML(self):
		return Null()

	clone = compact = asHTML

	def __str__(self):
		return ""

	def _dorepr(self):
		return self._str(slash = 1,ansi = ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		return [[nest,self.startlineno,elementno,self._dorepr(ansi)]]

def registerElement(element,namespacename = None,elementname = None):
	"""
	registers the element handler element to be used for elements with the appropriate name.
	The element will be registered under in the namespace namespacename and the element
	elementname. If namespacename is None the name of the module in which the element class
	is defined is used, or - if the module is __main__, the appropriate part of sys.argv[0].
	If elementname is None, the name of the class will be used.
	Names will be converted to lowercase in any case, to help prevent conflicts between
	Python keywords and class names (e.g. for the HTML element del).
	"""
	if namespacename is None:
		namespacename = namespaceName(element)
	if elementname is None:
		elementname = elementName(element)
	if _elementHandlers.has_key(elementname):
		_elementHandlers[elementname][namespacename] = element
	else:
		_elementHandlers[elementname] = { namespacename : element }

def registerAllElements(dict,namespacename = None):
	"""
	registers all elements in a dictionary under the namespace namespacename.
	This can be used to register all elements in a module simply by
	passing vars() to the function.
	As namespacename will be passed to registerElement(), see its
	documentation for comments about the default value.
	"""
	for name in dict.keys():
		object = dict[name]
		if type(object) == types.ClassType and issubclass(object,Element):
			registerElement(object,namespacename)

class Attr(Frag):
	"""
	Base classes of all attribute classes.

	The content of an attribute may be any other XSC node. This is different from
	a normal DOM, where only text and character references are allowed. The reason for
	this is to allow dynamic content (implemented as elements) to be put into attributes.
	The database module db makes use of this.

	Of course, this dynamic content when finally converted to HTML will normally result in
	a fragment consisting only of text and character references.
	"""

	def _dorepr(self,ansi = None):
		return strAttrValue(Frag._dorepr(self,ansi = 0),ansi)

class TextAttr(Attr):
	"""
	Attribute class that is used for normal text attributes.
	"""

class BoolAttr(Attr):
	"""
	Attribute class that is used for boolean attributes.
	"""

class ColorAttr(Attr):
	"""
	Attribute class that is used for a color attributes.
	"""

	repransitext = ""

class URLAttr(Attr):
	"""
	Attribute class that is used for URLs.

	XSC has one additional feature, that it allows URLs that are local filenames starting with a ':'.
	Those filenames are not relative to the directory containing the file where the URL originated,
	but local to the "project" directory, i.e. the root directory of all XSC files, which is the
	current directory.

	With this feature you don't have to remember how deeply you've nested your XSC file tree, you
	can specify a file from everywhere via ":dir/to/file.xsc". XSC will change this to an URL
	that correctly locates the file (e.g. "../../../dir/to/file.xsc", when you're nested three levels
	deep in a different directory than "dir".

	When dumping these URLs in the interactive Python environment (i.e. calling __repr__) these
	URLs will be shown with the pseudo scheme "project".

	Server relative URLs will be shown with the pseudo scheme "server". For checking these URLs
	for image or file size, a http request will be made to the server specified in the "server"
	option.

	For all other URLs a normal request will be made corresponding to the specified scheme
	(http, ftp, etc.)
	"""

	repransiurl = "32"

	def __init__(self,*_content):
		apply(Attr.__init__,(self,) + _content)
		self.base = xsc.filename[-1]

	def _str(self,content = None,brackets = None,slash = None,ansi = None):
		attr = " " + strAttrName("base",ansi) + "=" + strQuote(ansi = ansi) + strURL(str(self.base),ansi = ansi) + strQuote(ansi = ansi)
		return Attr._str(self,content = attr,brackets = brackets,slash = slash,ansi = ansi)

	def _dorepr(self,ansi = None):
		return strURL(str(self),ansi = ansi)

	def __str__(self):
		return str(Text(str(self.forOutput())))

	def asHTML(self):
		e = Attr.asHTML(self)
		e.base = self.base.clone()
		return e

	def clone(self):
		e = Attr.clone(self)
		e.base = self.base.clone()
		return e

	def compact(self):
		e = Attr.compact(self)
		e.base = self.base.clone()
		return e

	def _asURL(self):
		return URL(Attr.asPlainString(self))

	def asPlainString(self):
		return str(self._asURL())

	def forInput(self):
		url = self.base + self._asURL()
		if url.scheme == "server":
			url = url.relativeTo(URL(scheme = "http",server = xsc.server))
		return url

	def forOutput(self):
		url = self._asURL()
		if url.scheme == "server":
			url = url.relativeTo(URL(scheme = "http",server = xsc.server))
		else:
			url = url.relativeTo(xsc.filename[-1])
		return url

	def ImageSize(self):
		"""
		returns the size of an image as a tuple or (-1,-1) if the image shouldn't be read
		"""

		url = self.forInput()
		size = (-1,-1)
		if xsc.isRetrieve(url):
			try:
				filename,headers = urllib.urlretrieve(str(url))
				if headers.maintype == "image":
					img = Image.open(filename)
					size = img.size
					del img
				urllib.urlcleanup()
			except IOError:
				urllib.urlcleanup()
				raise FileNotFoundError(xsc.parser.lineno,url)
		return size

	def FileSize(self):
		"""
		returns the size of a file in bytes or -1 if the file shouldn't be read
		"""

		url = self.forInput()

		size = -1
		if xsc.isRetrieve(url):
			try:
				filename,headers = urllib.urlretrieve(str(url))
				size = os.stat(filename)[stat.ST_SIZE]
				urllib.urlcleanup()
			except IOError:
				urllib.urlcleanup()
				raise FileNotFoundError(xsc.parser.lineno,url)
		return size

###
###
###

class Parser(xmllib.XMLParser):
	entitiesByNumber = [ ]

	for i in xrange(65536):
		entitiesByNumber.append([])

	entitiesByName = {}

	def reset(self):
		xmllib.XMLParser.reset(self)
		# our nodes do not have a parent link, therefore we have to store the active path through the tree in a stack (which we call nesting, because stack is already used by the base class
		# after we've finished parsing the Frag that we put at the bottom of the stack will be our document root
		self.nesting = [ Frag() ]
		self.lineno = -1
		self.root = None

	def close(self):
		self.root = self.nesting[0]
		xmllib.XMLParser.close(self)

	def __appendNode(self,node):
		node.startlineno = self.lineno
		self.nesting[-1].append(node) # add the new node to the content of the innermost element

	def handle_proc(self,target,data):
		self.__appendNode(ProcInst(target,data))

	def handle_charref(self,name):
		try:
			if name[0] == 'x':
				n = string.atoi(name[1:],16)
			else:
				n = string.atoi(name)
		except string.atoi_error:
			raise MalformedCharRefError(xsc.parser.lineno,name)

		self.__appendNode(CharRef(n))

	def handle_entityref(self,name):
		try:
			self.__appendNode(self.entitiesByName[name])
		except KeyError:
			raise UnknownEntityError(xsc.parser.lineno,name)

	def elementFromName(self,name):
		"""
		returns the element class for the name name (which might include a namespace).
		"""
		name = string.split(string.lower(name),":")
		if len(name) == 1: # no namespace specified
			name.insert(0,None)

		try: # are there any elements with this name?
			elementsfornamespaces = _elementHandlers[name[1]]
		except KeyError: # nope!
			raise IllegalElementError(xsc.parser.lineno,name)
		if name[0] is None: # element name was unqualified ...
			if len(elementsfornamespaces.keys())==1: # ... and there is exactly one element with this name => use it
				element = elementsfornamespaces.values()[0]
			else:
				raise AmbiguousElementError(xsc.parser.lineno,name) # there is more than one
		else: # element name was qualified with a namespace
			try:
				element = elementsfornamespaces[name[0]]
			except KeyError:
				raise IllegalElementError(xsc.parser.lineno,name) # elements with this name were available, but none in this namespace
		return element

	def unknown_starttag(self,name,attrs):
		e = self.elementFromName(name)()
		for attr in attrs.keys():
			e[attr] = string2Fragment(attrs[attr])
		self.__appendNode(e)
		self.nesting.append(e) # push new innermost element onto the stack

	def unknown_endtag(self,name):
		element = self.elementFromName(name)
		currentelement = self.nesting[-1].__class__
		if element != currentelement:
			raise IllegalElementNestingError(xsc.parser.lineno,currentelement,element)
		self.nesting[-1].endlineno = self.lineno
		self.nesting.pop() # pop the innermost element off the stack

	def handle_data(self,data):
		if data != "":
			self.__appendNode(Text(data))

	def handle_comment(self,data):
		self.__appendNode(Comment(data))

def registerEntity(name,value):
	newvalue = ToNode(value)
	if isinstance(newvalue,CharRef):
		Parser.entitiesByNumber[newvalue.content].append(name)
	Parser.entitiesByName[name] = newvalue

###
###
###

# C0 Controls and Basic Latin
registerEntity("quot",CharRef(34)) # quotation mark = APL quote, U+0022 ISOnum
registerEntity("amp",CharRef(38)) # ampersand, U+0026 ISOnum
registerEntity("lt",CharRef(60)) # less-than sign, U+003C ISOnum
registerEntity("gt",CharRef(62)) # greater-than sign, U+003E ISOnum

###
###
###

class XSC:
	"""
	contains the options and functions for handling the XML files
	"""

	def __init__(self):
		self.filename = [ URL(scheme = "project") ]
		self.server = "localhost"
		self.reprtree = 1
		self.parser = Parser()

	def pushName(self,name):
		url = URL(name)
		if len(self.filename):
			url = self.filename[-1] + url
		self.filename.append(url)

	def popName(self):
		self.filename.pop()

	def parseString(self,string):
		"""
		Parses a string and returns the resulting XSC
		"""
		self.parser.reset()
		self.parser.feed(string)
		self.parser.feed(" ")
		self.parser.close()
		return self.parser.root

	def parse(self,url):
		"""
		Reads and parses a XML file from an URL and returns the resulting XSC
		"""
		self.pushName(url)
		self.parser.reset()
		self.parser.feed(xsc.filename[-1].read())
		self.parser.close()
		self.popName()
		return self.parser.root

	def __repr__(self):
		return '<xsc filename="' + self.filename + '" server="' + self.server + '" retrieveremote=' + [ 'no' , 'yes' ][retrieveremote] + '" retrievelocal=' + [ 'no' , 'yes' ][retrievelocal] + '>'

	def isRetrieve(self,url):
		remote = url.isRemote()
		if (retrieveremote and remote) or (retrievelocal and (not remote)):
			return 1
		else:
			return 0

def __forceopen(name,mode):
	try:
		return open(name,mode)
	except IOError,e:
		if e[0] != 2: # didn't work for some other reason
			raise
		found = string.rfind(name,"/")
		if found == -1:
			raise
		os.makedirs(name[:found])
		return open(name,mode)

def extXSC2HTML(ext):
	try:
		return { "hsc" : "html" , "shsc" : "shtml" , "phsc" : "phtml" , "xsc" : "html" , "sxsc" : "shtml" , "pxsc" : "phtml"}[ext]
	except KeyError:
		return ext

def extHTML2XSC(ext):
	try:
		return { "html" : "hsc" , "shtml" : "shsc" , "phtml" : "phsc"}[ext]
	except KeyError:
		return ext

def make():
	"""
	use XSC as a compiler script, i.e. read an input file from args[1]
	and writes it to args[2]
	"""

	(options,args) = getopt.getopt(sys.argv[1:],"i:o:",["include=","output="])

	globaloutname = URL(scheme = "project")
	for (option,value) in options:
		if option=="-i" or option=="--include":
			__import__(value)
		elif  option=="-o" or option=="--output":
			globaloutname = URL(value)

	if args:
		for file in args:
			inname = URL(file)
			outname = globaloutname.clone()
			if not outname.file:
				outname = outname + inname
			if not outname.file:
				outname.file = "noname"
			try:
				outname.ext = { "hsc" : "html" , "shsc" : "shtml" , "phsc" : "phtml" , "xsc" : "html" , "sxsc" : "shtml" , "pxsc" : "phtml"}[inname.ext]
			except KeyError:
				outname.ext = "html"
			sys.stderr.write('XSC: converting "' + str(inname) + '"' + ' to "' + str(outname) + '"...\n')
			e_in = xsc.parse(inname)
			xsc.pushName(inname)
			e_out = e_in.asHTML()
			__forceopen(str(outname),"wb").write(str(e_out))
			xsc.popName()
	else:
		sys.stderr.write("XSC: no files to convert.\n")

xsc = XSC()

if __name__ == "__main__":
	make()
