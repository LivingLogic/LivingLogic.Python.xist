#! /usr/bin/env python

"""
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import os
import string
import types
import exceptions
import sys
import socket

# for file size checking
import stat

# for image size checking
import Image

# for parsing XML files
from xml.sax import saxlib
from xml.sax import saxexts
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
			v.append(_strattrname(attr))

		return Error.__str__(self) + "Attribute " + _strattrname(self.attr) + " not allowed in element " + self.element._str() + ". Allowed attributes are: " + string.join(v,", ") + "."

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

		s = Error.__str__(self) + "Attribute " + _strattrname(self.attr) + " not found in element " + self.element._str() +". "

		if len(attrs):
			attrs.sort()
			v = []
			for attr in attrs:
				v.append(_strattrname(attr))
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
				elementnames.append(_strNode(_elementHandlers[elementname][namespace]))
		elementnames.sort()

		return Error.__str__(self) + "element " + _strName((self.name[0],self.name[1],0))+ " not allowed. Allowed elements are: " + string.join(elementnames,", ") + "."

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
		return Error.__str__(self) + "the value '" + str(self.element[self.attr]) + "' for the image size attribute " + _strattrname(self.attr) + " of the element " + self.element._str() + " can't be formatted or evaluated"

class FileNotFoundError(Error):
	"""
	exception that is raised, when XSC can't open an image for getting image size
	"""

	def __init__(self,lineno,url):
		Error.__init__(self,lineno)
		self.url = url

	def __str__(self):
		return Error.__str__(self) + "file " + _stransi(repransiurl,str(self.url)) + " can't be opened"

class IllegalObjectError(Error):
	"""
	exception that is raised, when XSC finds an illegal object in its object tree
	"""

	def __init__(self,lineno,object):
		Error.__init__(self,lineno)
		self.object = object

	def __str__(self):
		return Error.__str__(self) + "an illegal object of type " + type(self.object).__name__ + " has been found in the XSC tree"

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

		return Error.__str__(self) + "element " + _strName((name[0],name[1],0)) + " is ambigous. Possible elements are: " + string.join(elementnames,", ") + "."

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

e ANSI escape sequence to be used for slashes in element names
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

def _strelementnamespace(elementnamespace,ansi = None):
	return _stransi(repransielementnamespace,elementname,ansi)

def _strelementname(elementname,ansi = None):
	return _stransi(repransielementname,elementname,ansi)

def _strattrname(attrname,ansi = None):
	return _stransi(repransiattrname,attrname,ansi)

def nodeName(nodeClass):
	"""
	returns a tuple with the namespace of the node, which is the module in which the node is implemented
	and a name which is the name of the class. Both strings are converted to lowercase.
	"""
	return string.lower(nodeClass.__module__) , string.lower(nodeClass.__name__) , nodeClass.empty

def _strName(nodeName,content = None,brackets = None,slash = None,ansi = None):
	# slash == -1: before; 0: nowhere; 1:after
	if slash is None:
		if nodeName is None:
			slash = 0
		else:
			slash = nodeName[2]
	s = ""
	if slash < 0:
		s = s + _stransi(repransislash,"/",ansi)
	if nodeName is not None:
		if len(nodeName[0]):
			s = s + _stransi(repransielementnamespace,nodeName[0],ansi) + ":"
		s = s + _stransi(repransielementname,nodeName[1],ansi)
	if content is not None and slash>=0:
		s = s + content
	if slash > 0:
		s = s + _stransi(repransislash,"/",ansi)
	if brackets is not None:
		s = _stransi(repransibracket,'<',ansi) + s + _stransi(repransibracket,'>',ansi)
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
		if isinstance(value,Attr): # repack the attribute in a fragment, and we have a valid XSC node
			return Frag(value)
		elif isinstance(value,Frag):
			l = len(value)
			if l==1:
				return ToNode(value[0]) # recursively try to simplify the tree
			elif l==0:
				return Null()
			else:
				return value
		elif isinstance(value,Node):
			return value
	elif t in [ types.StringType,types.IntType,types.LongType,types.FloatType ]:
		return Text(str(value))
	elif t == types.NoneType:
		return Null()
	elif t in [ types.ListType,types.TupleType ]:
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

	def __add__(self,other):
		newother = ToNode(other)
		if not isinstance(newother,Null):
			return Frag(self) + newother
		else:
			return self

	def __radd__(self,other):
		newother = ToNode(other)
		if not isinstance(newother,Null):
			return Frag(newother) + self
		else:
			return self

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

	def _str(self,content = None,brackets = None,slash = None,ansi = None):
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
			line[3] = _stransi(repransitab,reprtab*line[0],ansi = ansi) + line[3] # add indentation
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
		returns this node as a string without <, > and & as character references.
		This only works with text node, character references and fragments of
		consisting only of those.
		"""
		raise IllegalObjectError(-1,self)

	def __str__(self):
		"""
		returns this element as a string
		"""
		return ""

	def elements(self,element = None,subtype = 0,children = 0,attrs = 0):
		"""
		returns a fragment which contains child elements of this node.

		If you specify element as the class of an XSC element only elements of this class
		will be returned.

		If you set subtype to 1 elements that are a subtype of element will be returned too.

		If you set children to 1 not only the immediate children but also the grandchildren
		will be searched for elements matching the other criteria.

		If you set attrs to 1 the attributes of the elements will be searched too.
		"""
		return Frag()

	def _elementOK(self,element,subtype):
		if element is not None:
			if subtype:
				return isinstance(self,element)
			else:
				return self.__class__ == element
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
		self.content = _content

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
					v.append(_stransi(repransicharref,s,ansi))
				else:
					s = content[start:end]
					v.append(_stransi(repransitext,s,ansi))
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
			s = _stransi(repransiquote,'"',ansi) + _stransi(repransitext,self.__strtext(1,lines[i],ansi),ansi) + _stransi(repransiquote,'"',ansi)
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
		return _stransi(repransicharref,s,ansi)

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

	def __init__(self,_content = []):
		t = type(_content)
		if t == types.InstanceType:
			if isinstance(_content,Frag): # if this was an attribute, we have it downcast now
				self.__content = []
				for child in _content:
					self.append(child)
			elif isinstance(_content,Null):
				self.__content = []
			else:
				self.__content = [ ToNode(_content) ]
		elif t in [ types.ListType , types.TupleType ]:
			self.__content = map(ToNode,_content)
		elif _content is None:
			self.__content = []
		else:
			self.__content = [ ToNode(_content) ]

	def __add__(self,other):
		res = self.__class__(self.__content) # "virtual" copy
		newother = ToNode(other)
		if not isinstance(newother,Null):
			if isinstance(newother,Frag):
				for child in newother:
					res.append(child)
			else:
				res.append(newother)
		return res

	def __radd__(self,other):
		res = self.__class__(self.__content) # "virtual" copy
		newother = ToNode(other)
		if not isinstance(newother,Null):
			if isinstance(newother,Frag):
				res.__content = newother.__content + res.__content
			else:
				res.__content.insert(0,newother)
		return res

	def asHTML(self):
		e = self.__class__([])
		for child in self:
			e.append(child.asHTML())
		return e

	def clone(self):
		e = self.__class__([])
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
		return self.__class__(self.__content[index1:index2])

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

	def elements(self,element = None,subtype = 0,children = 0,attrs = 0):
		e = Frag()
		for child in self:
			if child._elementOK(element,subtype):
				e.append(child)
			if children:
				e = e + child.elements(element,subtype,children,attrs)
		return e

	def compact(self):
		e = self.__class__()
		for child in self:
			e.append(child.compact())
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
		return self._str(content = _stransi(repransidoctype,"!DOCTYPE " + self.__content,ansi),brackets = 1,ansi = ansi)

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
		return self._str(content = _stransi(repransiquestion,"?",ansi) + _stransi(repransiprocinsttarget,self.target,ansi) + " " + _stransi(repransiprocinstdata,self.content,ansi) + _stransi(repransiquestion,"?",ansi),brackets = 1,ansi = ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		lines = string.split(self.content,"\n")
		if len(lines) and lines[-1] == "":
			del lines[-1]
		if len(lines) == 1:
			s = self._str(content = _stransi(repransiquestion,"?",ansi) + _stransi(repransiprocinsttarget,self.target,ansi) + " " + _stransi(repransiprocinstdata,string.rstrip(lines[0]),ansi) + _stransi(repransiquestion,"?",ansi),brackets = 1,ansi = ansi)
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
					s = _stransi(repransibracket,"<",ansi)+_stransi(repransiquestion,"?",ansi) + _stransi(repransiprocinsttarget,self.target,ansi)
				elif i == len(lines)+1:
					mynest = nest
					s = _stransi(repransiquestion,"?",ansi)+_stransi(repransibracket,">",ansi)
				else:
					mynest = nest+1
					s = lines[i-1]
					while len(s) and s[0] == "\t":
						mynest = mynest + 1
						s = s[1:]
				v.append([mynest,no,elementno,string.rstrip(s)])
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

	def __init__(self,_content = [],_attrs = {},**_restattrs):
		self.content = Frag(_content)
		self.attrs = {}
		for attr in _attrs.keys():
			self[attr] = _attrs[attr]
		for attr in _restattrs.keys():
			self[attr] = _restattrs[attr]

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
		raise IllegalObjectError(-1,self)

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
				self.attrs[lowerindex] = self.attrHandlers[lowerindex](value) # pack the attribute into an attribute object
			except KeyError:
				raise IllegalAttributeError(xsc.parser.lineno,self,index)
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
		"""returns a copy of the element that contains a slice of the content"""
		return self.__class__(self.content[index1:index2],self.attrs)

	def __setslice__(self,index1,index2,sequence):
		"""modifies a slice of the content of the element"""
		self.content[index1:index2] = sequence

	def __delslice__(self,index1,index2):
		"""removes a slice of the content of the element"""
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
			v.append(_strattrname(attr,ansi))
			value = self[attr]
			if len(value):
				v.append('=')
				v.append(_stransi(repransiquote,'"',ansi = ansi))
				v.append(value._dorepr(ansi = ansi))
				v.append(_stransi(repransiquote,'"',ansi = ansi))
		return string.join(v,"")

	def AddImageSizeAttributes(self,imgattr,widthattr = "width",heightattr = "height"):
		"""add width and height attributes to the element for the image that can be found in the attributes imgattr. if the attribute is already there it is taken as a formating template with the size passed in as a dictionary with the keys 'width' and 'height', i.e. you could make your image twice as wide with width='%(width)d*2'"""

		if self.has_attr(imgattr):
			size = self[imgattr].ImageSize()
			sizedict = { "width": size[0], "height": size[1] }
			if size[0] != -1: # the width was retrieved so we can use it
				if self.has_attr(widthattr):
					try:
						self[widthattr] = str(eval(str(self[widthattr]) % sizedict))
					except:
						raise ImageSizeFormatError(xsc.parser.lineno,self,widthattr)
				else:
					self[widthattr] = str(size[0])
			if size[1] != -1: # the height was retrieved so we can use it
				if self.has_attr(heightattr):
					try:
						self[heightattr] = str(eval(str(self[heightattr]) % sizedict))
					except:
						raise ImageSizeFormatError(xsc.parser.lineno,self,heightattr)
				else:
					self[heightattr] = str(size[1])

	def compact(self):
		return self.__class__(self.content.compact(),self.attrs)

	def elements(self,element = None,subtype = 0,children = 0,attrs = 0):
		e = Frag()
		if attrs:
			for attr in self.attrs.keys():
				e = e + self[attr].elements(element,subtype,children,attr)
		e = e + self.content.elements(element,subtype,children,attrs)
		return e

class Null(Element):
	"""
	node that does not contain anything.
	"""

	repransiname = "33"

	def asHTML(self):
		return Null()

	clone = asHTML

	def __str__(self):
		return ""

	def _dorepr(self):
		# constructs a string of this Text with syntaxhighlighting. Special characters will be output as CharRefs (with special highlighting)
		return self._str(slash = 1,ansi = ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		return [[nest,self.startlineno,elementno,self._dorepr(ansi)]]

	def compact(self):
		return Null()

def registerElement(element):
	"""
	registers the element handler element to be used for elements with the appropriate name.
	"""
	name = nodeName(element)
	if _elementHandlers.has_key(name[1]):
		_elementHandlers[name[1]][name[0]] = element
	else:
		_elementHandlers[name[1]] = { name[0] : element }

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

class TextAttr(Attr):
	"""
	Attribute class that is used for normal text attributes.
	"""

	def _dorepr(self,ansi = None):
		return _stransi(repransiattrvalue,Attr._dorepr(self,ansi = 0),ansi)

class ColorAttr(Attr):
	"""
	Attribute class that is used for a color attributes.
	"""

	repransitext = ""

	def _dorepr(self,ansi = None):
		return _stransi(repransiattrvalue,Attr._dorepr(self,ansi = 0),ansi)

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

	def __init__(self,_content = []):
		Attr.__init__(self,_content)
		self.base = xsc.filename[-1]

	def _str(self,content = None,brackets = None,slash = None,ansi = None):
		attr = " " + _strattrname("base",ansi) + "=" + _stransi(repransiquote,'"',ansi = ansi) + _stransi(repransiurl,str(self.base),ansi = ansi) + _stransi(repransiquote,'"',ansi = ansi)
		return Attr._str(self,content = attr,brackets = brackets,slash = slash,ansi = ansi)

	def _dorepr(self,ansi = None):
		return _stransi(repransiurl,str(self),ansi = ansi)

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
			url = url.relativeTo(xsc.infilename)
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

	def attributes2Fragments(self,attrs):
		newattrs = {}
		for attr in attrs.keys():
			newattrs[attr] = string2Fragment(attrs[attr])
		return newattrs

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
		element = self.elementFromName(name)
		e = element([],self.attributes2Fragments(attrs))
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
		self.infilename = URL(scheme = "project") # this is the filename that we are reading and will be set via make()
		self.reprtree = 1
		self.parser = Parser()

	def __pushName(self,name):
		self.filename.append(URL(name))

	def __popName(self):
		self.filename.pop()

	def parseString(self,string):
		"""
		Parses a string and returns the resulting XSC
		"""
		self.parser.reset()
		self.parser.feed(string)
		self.parser.close()
		return self.parser.root

	def parse(self,url):
		"""
		Reads and parses a XML file from an URL and returns the resulting XSC
		"""
		self.__pushName(url)
		self.parser.reset()
		url = reduce(lambda x,y: x+y,self.filename,URL())
		print url
		self.parser.feed(urllib.urlopen(str(url)).read())
		self.parser.close()
		self.__popName()
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

def make():
	"""
	use XSC as a compiler script, i.e. read an input file from args[1]
	and writes it to args[2]
	"""

	infilename = URL(sys.argv[1])
	outfilename = URL(sys.argv[2])
	xsc.infilename = infilename
	if outfilename.file and not len(outfilename.file):
		if infilename.file and infilename.file[-3:] == "hsc" or infilename.file[-3:] == "xsc":
			outfilename.file = infilename.file[:-3] + "html"
		else:
			outfilename.file = infilename.file
	e_in = xsc.parse(infilename)
	e_out = e_in.asHTML()
	__forceopen(str(outfilename),"wb").write(str(e_out))

xsc = XSC()

if __name__ == "__main__":
	make()

