#! /usr/bin/env python

"""
"""

__version__ = "$Revision$"
# $Source$

import os
import string
import types
import exceptions
import sys
import _socket

# for file size checking
import stat

# for image size checking
import Image

# for parsing XML files
from xml.sax import saxlib
from xml.sax import saxexts
from xml.parsers import xmllib

# for parsing URLs
import urlparse

# for reading remote files
import urllib

# our sandbox
import procinst

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
		return Error.__str__(self) + "element " + self.element._strname() + " specified to be empty, but has content"

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

		return Error.__str__(self) + "Attribute " + _strattrname(self.attr) + " not allowed in element " + self.element._strname() + ". Allowed attributes are: " + string.join(v,", ") + "."

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

		s = Error.__str__(self) + "Attribute " + _strattrname(self.attr) + " not found in element " + self.element._strname() +". "

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
				elementnames.append(_strNodeName(_elementHandlers[elementname][namespace]))
		elementnames.sort()

		if self.name[0]:
			name = _strelementname(self.name[0]) + ":" + _strelementname(self.name[1])
		else:
			name = _strelementname(self.name[1])

		return Error.__str__(self) + "element " + name + " not allowed. Allowed elements are: " + string.join(elementnames,", ") + "."

class IllegalElementNestingError(Error):
	"""
	exception that is raised, when an element has an illegal nesting
	(e.g. <a><b></a></b>)
	"""

	def __init__(self,lineno,expectedelementname,foundelementname):
		Error.__init__(self,lineno)
		self.expectedelementname = expectedelementname
		self.foundelementname = foundelementname

	def __str__(self):
		return Error.__str__(self) + "illegal element nesting (" + _strelementname(self.expectedelementname) + " expected; " + _strelementname(self.foundelementname) + " found)"

class ImageSizeFormatError(Error):
	"""
	exception that is raised, when XSC can't format or evaluate image size attributes
	"""

	def __init__(self,lineno,element,attr):
		Error.__init__(self,lineno)
		self.element = element
		self.attr = attr

	def __str__(self):
		return Error.__str__(self) + "the value '" + str(self.element[self.attr]) + "' for the image size attribute " + _strattrname(self.attr) + " of the element " + self.element._strname() + " can't be formatted or evaluated"

class FileNotFoundError(Error):
	"""
	exception that is raised, when XSC can't open an image for getting image size
	"""

	def __init__(self,lineno,url):
		Error.__init__(self,lineno)
		self.url = url

	def __str__(self):
		return Error.__str__(self) + "file " + self.url.repr() + " can't be opened"

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
			elementnames.append(_strNodeName(_elementHandlers[self.name[1]][namespace]))
		elementnames.sort()

		if self.name[0]:
			name = _strelementname(self.name[0]) + ":" + _strelementname(self.name[1])
		else:
			name = _strelementname(self.name[1])

		return Error.__str__(self) + "element " + name + " is ambigous. Possible elements are: " + string.join(elementnames,", ") + "."

###
### helpers
###

def _stransi(codes,string):
	if Node.repransi and codes!="" and string!="":
		return "\033[" + codes + "m" + string + "\033[0m"
	else:
		return string

def _strelementname(elementname):
	return _stransi(Element.repransiname,elementname)

def _strattrname(attrname):
	return _stransi(Attr.repransiname,attrname)

def nodeName(nodeClass):
	"""
	returns a tuple with the namespace of the node, which is the module in which the node is implemented
	and a name which is the name of the class. Both strings are converted to lowercase.
	"""
	return string.lower(nodeClass.__module__) , string.lower(nodeClass.__name__)

def _strNodeName(nodeClass):
	name = nodeName(nodeClass)
	return _stransi(nodeClass.repransinamespace,name[0]) + ":" + _stransi(nodeClass.repransiname,name[1])

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
				return value
		elif isinstance(value,Attr): # unpack the attribute, and we have a valid XSC node
			return value.content
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

	# line numbers where this node starts and ends in a file (will be hidden in derived classes, but is specified here, so that no special tests are required. In derived classes both variables will be set by the parser)
	startlineno = -1
	endlineno = -1

	repransinamespace = "31"
	repransiname = ""
	repransibrackets = "34;1"
	reprtab = ". " # how to represent an indentation in the DOM tree
	repransi = 0 # should ANSI escape sequences be used for dumping the DOM tree?
	repransitab = "32" # ANSI escape sequence to be used for tabs

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

	def _strname(self):
		return _strNodeName(self.__class__)

	def clone(self):
		"""
		returns an identical clone of the node and it's children.
		"""
		pass

	def repr(self):
		return self._dorepr()

	def reprtree(self):
		nest = 0
		v = []
		lines = self._doreprtree(nest,[])
		lenlineno = 0
		lenelementno = 0
		for line in lines:
			if line[1] != -1: # convert line number to a string
				line[1] = str(line[1])
			else:
				line[1] = "?"
			line[2] = string.join(map(str,line[2]),".") # convert element number to a string
			line[3] = _stransi(self.repransitab,self.reprtab*line[0]) + line[3] # add indentation
			lenlineno = max(lenlineno,len(line[1]))
			lenelementno = max(lenelementno,len(line[2]))

		for line in lines:
			v.append("%*s %-*s %s\n" % (lenlineno,line[1],lenelementno,line[2],line[3]))
		return string.join(v,"")

	def _dorepr(self):
		# returns a string representation of the node
		return self._strtag("?")

	def _doreprtree(self,nest,elementno):
		# returns and array containing arrays consisting of the (nestinglevel,linenumber,elementnumber,string representation) of the nodes
		return [[nest,self.startlineno,elementno,self._strtag("?")]]

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

	def _strtag(self,content):
		return _stransi(self.repransibrackets,'<') + content + _stransi(self.repransibrackets,'>')

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

	repransiname = ""
	repransiquotes = "34;1"

	strescapes = { '<' : 'lt' , '>' : 'gt' , '&' : 'amp' , '"' : 'quot' }

	def __init__(self,_content = ""):
		self.content = _content

	def asHTML(self):
		return Text(self.content)

	clone = asHTML

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

	def __strtext(self,refwhite):
		# we could put ANSI escapes around every character or reference that we output, but this would result in strings that are way to long, especially if output over a serial connection, so we collect runs of characters with the same highlighting and put the ANSI escapes around those. (of course, when we're not doing highlighting, this routine does way to much useless calculations)
		v = [] # collect all colored string here
		charref = -1 # the type of characters we're currently collecting (0==normal character, 1==character that has to be output as an entity, -1==at the start)
		start = 0 # the position where our current run of characters for the same class started
		end = 0 # the current position we're testing
		while end<=len(self.content): # one more than the length of the string
			do = 0 # we will have to do something with the string collected so far ...
			if end == len(self.content): # ... if we're at the end of the string ...
				do = 1
			else:
				c = self.content[end] # ... or if the character we're at is different from those we've collected so far
				ascharref = (0 <= ord(c) <= 31 or 128 <= ord(c))
				if not refwhite and (c == "\n" or c == "\t"):
					ascharref = 0
				if ascharref != charref:
					do = 1
					charref = 1-ascharref # this does nothing, except at the start, where it enforces the correct processing
			if do: # process the string we have so far
				if charref: # we've collected references so far
					s = ""
					for i in self.content[start:end]:
						ent = Parser.entitiesByNumber[ord(i)] # use names if a available, or number otherwise
						if len(ent):
							s = s + '&' + ent[0] + ';'
						else:
							s = s + '&#' + str(ord(i)) + ';'
					v.append(_stransi(CharRef.repransiname,s))
				else:
					s = self.content[start:end]
					v.append(_stransi(Text.repransiname,s))
				charref = 1-charref # switch to the other class
				start = end # the next string we want to work on starts from here
			end = end + 1 # to the next character
		return string.join(v,"")

	def _dorepr(self):
		# constructs a string of this Text with syntaxhighlighting. Special characters will be output as CharRefs (with special highlighting)
		return self.__strtext(0)

	def _doreprtree(self,nest,elementno):
		s = _stransi(self.repransiquotes,'"') + _stransi(self.repransiname,self.__strtext(1)) + _stransi(self.repransiquotes,'"')
		return [[nest,self.startlineno,elementno,s]]

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

	def __str__(self):
		if 0<=self.content<=127:
			if self.content != ord("\r"):
				if self.__notdirect.has_key(self.content):
					return '&' + self.__notdirect[self.content] + ';'
				else:
					return chr(self.content)
		else:
			return '&#' + str(self.content) + ';'

	def __strcharref(self,s):
		return _stransi(self.repransiname,s)

	def _dorepr(self):
		if len(Parser.entitiesByNumber[self.content]):
			return self.__strcharref('&' + Parser.entitiesByNumber[self.content][0] + ';')
		else:
			return self.__strcharref('&#' + str(self.content) + ';')

	def _doreprtree(self,nest,elementno):
		s = self.__strcharref('&#' + str(self.content) + ';') + ' (' + self.__strcharref('&#x' + hex(self.content)[2:] + ';')
		for name in Parser.entitiesByNumber[self.content]:
			s = s + ' ' + self.__strcharref('&' + name + ';')
		s = s + ')'
		if 0 <= self.content <= 255:
			s = s + ' ' + Text(chr(self.content))._doreprtree(0,0)[0][-1]
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

	repransiname = ""

	def __init__(self,_content = []):
		t = type(_content)
		if t == types.InstanceType:
			if isinstance(_content,Frag):
				self.__content = _content
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
		res = Frag(self.__content)
		newother = ToNode(other)
		if not isinstance(newother,Null):
			if isinstance(newother,Frag):
				res.__content = res.__content + newother.__content
			else:
				res.__content.append(newother)
		return res

	def __radd__(self,other):
		res = Frag(self.__content)
		newother = ToNode(other)
		if not isinstance(newother,Null):
			if isinstance(newother,Frag):
				res.__content = newother.__content + res.__content
			else:
				res.__content.insert(0,newother)
		return res

	def asHTML(self):
		e = Frag()
		for child in self:
			e.append(child.asHTML())
		return e

	def clone(self):
		e = Frag()
		for child in self:
			e.append(child.clone())
		return e

	def _dorepr(self):
		v = []
		for child in self:
			v.append(child._dorepr())
		return string.join(v,"")

	def _doreprtree(self,nest,elementno):
		v = []
		v.append([nest,self.startlineno,elementno,self._strtag(self._strname())])
		i = 0
		for child in self:
			v = v + child._doreprtree(nest+1,elementno + [i])
			i = i + 1
		v.append([nest,self.endlineno,elementno,self._strtag(_strelementname("/")+self._strname())])
		return v

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
		return Frag(self.__content[index1:index2])

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
		e = Frag()
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

	def _dorepr(self):
		return self._strtag("!--" + self.__content + "--")

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

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

	def name(self):
		return self._strtag(_stransi(self.repransiname,"doctype"))

	def asHTML(self):
		return DocType(self.__content)

	clone = asHTML

	def _dorepr(self):
		return self._strtag(_stransi(self.repransiname,"!DOCTYPE " + self.__content))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

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
	repransiquestion = "34"
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

	def _dorepr(self):
		return self._strtag(_stransi(self.repransiquestion,"?") + _stransi(self.repransiname,self.target) + " " + _stransi(self.repransidata,self.content) + _stransi(self.repransiquestion,"?"))

	def _doreprtree(self,nest,elementno):
		lines = string.split(self.content,"\n")
		while lines[0] == "":
			del lines[0]
		while lines[-1] == "":
			del lines[-1]
		if len(lines) == 1:
			return [[nest,self.startlineno,elementno,self._dorepr()]]
		else:
			v = []
			for i in xrange(len(lines)+2):
				if self.startlineno == -1:
					no = -1
				else:
					no = self.startlineno + i
				if i == 0:
					mynest = nest
					s = _stransi(self.repransibrackets,'<')+_stransi(self.repransiquestion,"?") + " " + _stransi(self.repransiname,self.target)
				elif i == len(lines)+1:
					mynest = nest
					s = _stransi(self.repransiquestion,"?")+_stransi(self.repransibrackets,'>')
				else:
					mynest = nest+1
					s = lines[i-1]
					while len(s) and s[0] == "\t":
						mynest = mynest + 1
						s = s[1:]
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
	repransiattrquotes = "34"

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

	def _dorepr(self):
		v = []
		if self.empty:
			v.append(self._strtag(self._strname() + self.__strattrs() + _strelementname("/")))
		else:
			v.append(self._strtag(self._strname() + self.__strattrs()))
			for child in self:
				v.append(child._dorepr())
			v.append(self._strtag(_strelementname("/") + self._strname()))
		return string.join(v,"")

	def _doreprtree(self,nest,elementno):
		v = []
		if self.empty:
			v.append([nest,self.startlineno,elementno,self._strtag(self._strname() + self.__strattrs() + _strelementname("/"))])
		else:
			v.append([nest,self.startlineno,elementno,self._strtag(self._strname() + self.__strattrs())])
			i = 0
			for child in self:
				v = v + child._doreprtree(nest+1,elementno + [i])
				i = i + 1
			v.append([nest,self.endlineno,elementno,self._strtag(_strelementname(_strelementname("/") + self._strname()))])
		return v

	def __str__(self):
		v = []
		v.append("<")
		v.append(string.lower(self.__class__.__name__))
		for attr in self.attrs.keys():
			v.append(' ')
			v.append(attr)
			value = self[attr]
			if not isinstance(value.content,Null):
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

	def __strattrs(self):
		v = []
		for attr in self.attrs.keys():
			v.append(" ")
			v.append(_strattrname(attr))
			value = self[attr]
			if not isinstance(value.content,Null):
				v.append('=')
				v.append(_stransi(self.repransiattrquotes,'"'))
				v.append(value._dorepr())
				v.append(_stransi(self.repransiattrquotes,'"'))
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
				e = e + self[attr].content.elements(element,subtype,children,attr)
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
		return self._strtag(self._strname() + _strelementname("/"))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

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

class Attr(Node):
	"""
	Base classes of all attribute classes.

	The content of an attribute may be any other XSC node. This is different from
	a normal DOM, where only text and character references are allowed. The reason for
	this is to allow dynamic content (implemented as elements) to be put into attributes.
	The database module db makes use of this.

	Of course, this dynamic content when finally converted to HTML will normally result in
	a fragment consisting only of text and character references.
	"""

	repransi = "33"
	repransiname = "31"

	def __init__(self,_content):
		self.content = ToNode(_content)

	def __add__(self,other):
		newother = ToNode(other)
		if not isinstance(newother,Null):
			return self.__class__(self.content+newother)
		else:
			return self

	def __radd__(self,other):
		newother = ToNode(other)
		if not isinstance(newother,Null):
			return self.__class__(newother+self.content)
		else:
			return self

	def clone(self):
		return self.__class__(self.content.clone()) # "virtual copy constructor"

class TextAttr(Attr):
	"""
	Attribute class that is used for normal text attributes.
	"""

	repransitext = ""

	def __init__(self,_content):
		Attr.__init__(self,_content)

	def _dorepr(self):
		return _stransi(self.repransitext,str(self.content))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		return str(self.content)

	def asHTML(self):
		return TextAttr(self.content.asHTML())

class ColorAttr(Attr):
	"""
	Attribute class that is used for a color attributes.
	"""

	repransitext = ""

	def __init__(self,_content):
		Attr.__init__(self,_content)

	def _dorepr(self):
		return _stransi(self.repransitext,str(self.content))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		return str(self.content)

	def asHTML(self):
		return ColorAttr(self.content.asHTML())

class _URL:
	def __init__(self,url = None,scheme = None,server = None,path = None,parameters = None,query = None,fragment = None):
		if url is not None:
			(self.scheme,self.server,self.path,self.parameters,self.query,self.fragment) = urlparse.urlparse(url)
			self.path = string.split(self.path,"/")
			if self.scheme == "" and self.server == "": # do we have a local file?
				if len(self.path) and not len(self.path[0]): # this is a server relative URL
					del self.path[0] # drop the empty string in front of the first "/" ...
					self.scheme = "server" # ... and use a special scheme for that
				elif len(self.path) and len(self.path[0]) and self.path[0][0] == ":": # project relative, i.e. relative to the current directory
					self.path[0] = self.path[0][1:] # drop of the ":" ...
					self.scheme = "project" # special scheme name
			else:
				if self.scheme == "http":
					del self.path[0] # if we had a http, the path from urlparse started with "/" too
		else:
			self.scheme     = scheme
			self.server     = server
			self.path       = path[:]
			self.parameters = parameters
			self.query      = query
			self.fragment   = fragment
		self.__optimize()

	def __repr__(self):
		sep = "/" # use the normal URL separator by default
		path = self.path[:]
		if self.scheme == "" or self.scheme == "project":
			# replace URL syntax with the path syntax on our system (won't do anything under UNIX, replaces / with  \ under Windows)
			for i in range(len(path)):
				if path[i] == "..":
					path[i] = os.pardir
			sep = os.sep # we have a local file, so we should use the local directory separator instead
		url = urlparse.urlunparse((self.scheme,self.server,string.join(path,sep),self.parameters,self.query,self.fragment))
		return _stransi(URLAttr.repransiurl,url)

	def __str__(self):
		path = self.path[:]
		if self.scheme == "project":
			scheme = "" # remove our own private scheme name
		elif scheme == "server":
			scheme = "" # remove our own private scheme name
			path[:0] = [ "" ]
		return urlparse.urlunparse((scheme,self.server,string.join(path,"/"),self.parameters,self.query,self.fragment))

	def __add__(self,other):
		new = self.clone()
		if other.scheme == "":
			new.path[-1:]  = other.path[:]
			new.parameters = other.parameters
			new.query      = other.query
			new.fragment   = other.fragment
		elif other.scheme == "project" or other.scheme=="server":
			new.path       = other.path[:]
			new.parameters = other.parameters
			new.query      = other.query
			new.fragment   = other.fragment
		else: # URL to be joined is absolute, so we the second URL
			return other.clone()
		new.__optimize()
		return new

	def clone(self):
		return _URL(scheme = self.scheme,server = self.server,path = self.path,parameters = self.parameters,query = self.query,fragment = self.fragment)
		
	def relativeTo(self,other):
		if self.scheme != "" and self.scheme != "project":
			return self.clone()
		else:
			pass

	def __optimize(self):
		# optimize the path by removing combinations of down/up
		while 1:
			for i in xrange(len(self.path)):
				if self.path[i]==".." and i>0 and self.path[i-1]!="..": # found a down/up
					del self.path[i-1:i+1] # remove it
					break # restart the search
			else: # no down/up found
				break

class URLAttr(Attr):
	"""
	Attribute class that is used for URLs.

	XSC has one additional feature, that it allows URLs that are local filenames starting with a ':'.
	Those filenames are not relative to the directory containing the file where the URL originated,
	but local to the "project" directory, i.e. the root directory of all XSC files, which is the
	current directory.

	With this feature you don't have to remember how deeply you've nested your XSC file tree, you
	can specify such file from everywhere via ":dir/to/file.xsc". XSC will change this to an URL
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

	def __make(self):
		url = _URL(str(self.content))
		return (url.scheme,url.server,url.path,url.parameters,url.query,url.fragment)

	def _dorepr(self):
		return repr(_URL(str(self.content)))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		return self.forOutput()

	def asHTML(self):
		return URLAttr(self.content.asHTML())

	def forInput(self):
		(scheme,server,path,parameters,query,fragment) = self.__make()
		path = path[:]
		sep = "/" # use the normal URL separator by default
		if scheme == "server":
			scheme = "http"
			server = xsc.server
		elif scheme == "project" or scheme == "":
			file = xsc.filename[-1].path[:]
			if scheme == "project": # make the path relative to the directory of the file
				path[:0] = [".."] * (len(file)-1) # go up from the file directory to the current directory
				# now we have an URL that is relative to the file directory
			path[:0] = file[:-1] # make it relative to the current directory by adding the directories of file
			# now optimize the path by removing combinations of down/up
			while 1:
				for i in xrange(len(path)):
					if path[i]==".." and i>0 and path[i-1]!="..": # found a down/up
						del path[i-1:i+1] # remove it
						break # restart the search
				else: # no down/up found
					break
			# replace URL syntax with the path syntax on our system (won't do anything under UNIX, replaces / with  \ under Windows)
			for i in range(len(path)):
				if path[i] == "..":
					path[i] = os.pardir
			sep = os.sep # we have a local file, so we should use the local directory separator instead
			scheme = "" # remove our own private scheme name
		return urlparse.urlunparse((scheme,server,string.join(path,sep),parameters,query,fragment))

	def forOutput(self):
		(scheme,server,path,parameters,query,fragment) = self.__make()
		path = path[:]
		if scheme == "project":
			file = xsc.filename[-1].path[:]
			while len(file)>1 and len(path)>1 and file[0]==path[0]: # throw away identical directories in both paths (we don't have to go up from file and down to path for these identical directories
				del file[0]
				del path[0]
			path[:0] = [".."]*(len(file)-1) # now for the rest of the path we have to go up from file and down to path (the directories for this are still in path)
			scheme = "" # remove our own private scheme name
		elif scheme == "server":
			scheme = ""
			path[:0] = [ "" ]
		return urlparse.urlunparse((scheme,server,string.join(path,"/"),parameters,query,fragment))

	def ImageSize(self):
		"""
		returns the size of an image as a tuple or (-1,-1) if the image shouldn't be read
		"""

		url = self.forInput()
		size = (-1,-1)
		if xsc.is_retrieve(url):
			try:
				filename,headers = urllib.urlretrieve(url)
				if headers.has_key("content-type") and headers["content-type"][:6] == "image/":
					img = Image.open(filename)
					size = img.size
					del img
				urllib.urlcleanup()
			except IOError:
				urllib.urlcleanup()
				raise FileNotFoundError(xsc.parser.lineno,self)
		return size

	def FileSize(self):
		"""
		returns the size of a file in bytes or -1 if the file shouldn't be read
		"""

		url = self.forInput()

		size = -1
		if xsc.is_retrieve(url):
			try:
				filename,headers = urllib.urlretrieve(url)
				size = os.stat(filename)[stat.ST_SIZE]
				urllib.urlcleanup()
			except IOError:
				urllib.urlcleanup()
				raise FileNotFoundError(xsc.parser.lineno,self)
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

	def unknown_starttag(self,name,attrs):
		lowername = string.split(string.lower(name),":")
		if len(lowername) == 2: # namespace specified
			name = lowername
		else:
			name = [ None , lowername[0] ]
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
		e = element([],self.attributes2Fragments(attrs))
		self.__appendNode(e)
		self.nesting.append(e) # push new innermost element onto the stack

	def unknown_endtag(self,name):
		currentname = string.lower(self.nesting[-1].__class__.__name__)
		if string.lower(name) != currentname:
			raise IllegalElementNestingError(xsc.parser.lineno,currentname,name)
		self.nesting[-1].endlineno = self.lineno
		self.nesting[-1:] = [] # pop the innermost element off the stack

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

registerEntity("lf",CharRef(10)) # line feed
registerEntity("cr",CharRef(13)) # carriage return
registerEntity("tab",CharRef(9)) # horizontal tab
registerEntity("esc",CharRef(27)) # escape

# Latin 1 characters
registerEntity("nbsp",CharRef(160)) # no-break space = non-breaking space, U+00A0 ISOnum
registerEntity("iexcl",CharRef(161)) # inverted exclamation mark, U+00A1 ISOnum
registerEntity("cent",CharRef(162)) # cent sign, U+00A2 ISOnum
registerEntity("pound",CharRef(163)) # pound sign, U+00A3 ISOnum
registerEntity("curren",CharRef(164)) # currency sign, U+00A4 ISOnum
registerEntity("yen",CharRef(165)) # yen sign = yuan sign, U+00A5 ISOnum
registerEntity("brvbar",CharRef(166)) # broken bar = broken vertical bar, U+00A6 ISOnum
registerEntity("sect",CharRef(167)) # section sign, U+00A7 ISOnum
registerEntity("uml",CharRef(168)) # diaeresis = spacing diaeresis, U+00A8 ISOdia
registerEntity("copy",CharRef(169)) # copyright sign, U+00A9 ISOnum
registerEntity("ordf",CharRef(170)) # feminine ordinal indicator, U+00AA ISOnum
registerEntity("laquo",CharRef(171)) # left-pointing double angle quotation mark = left pointing guillemet, U+00AB ISOnum
registerEntity("not",CharRef(172)) # not sign, U+00AC ISOnum
registerEntity("shy",CharRef(173)) # soft hyphen = discretionary hyphen, U+00AD ISOnum
registerEntity("reg",CharRef(174)) # registered sign = registered trade mark sign, U+00AE ISOnum
registerEntity("macr",CharRef(175)) # macron = spacing macron = overline = APL overbar, U+00AF ISOdia
registerEntity("deg",CharRef(176)) # degree sign, U+00B0 ISOnum
registerEntity("plusmn",CharRef(177)) # plus-minus sign = plus-or-minus sign, U+00B1 ISOnum
registerEntity("sup2",CharRef(178)) # superscript two = superscript digit two = squared, U+00B2 ISOnum
registerEntity("sup3",CharRef(179)) # superscript three = superscript digit three = cubed, U+00B3 ISOnum
registerEntity("acute",CharRef(180)) # acute accent = spacing acute, U+00B4 ISOdia
registerEntity("micro",CharRef(181)) # micro sign, U+00B5 ISOnum
registerEntity("para",CharRef(182)) # pilcrow sign = paragraph sign, U+00B6 ISOnum
registerEntity("middot",CharRef(183)) # middle dot = Georgian comma = Greek middle dot, U+00B7 ISOnum
registerEntity("cedil",CharRef(184)) # cedilla = spacing cedilla, U+00B8 ISOdia
registerEntity("sup1",CharRef(185)) # superscript one = superscript digit one, U+00B9 ISOnum
registerEntity("ordm",CharRef(186)) # masculine ordinal indicator, U+00BA ISOnum
registerEntity("raquo",CharRef(187)) # right-pointing double angle quotation mark = right pointing guillemet, U+00BB ISOnum
registerEntity("frac14",CharRef(188)) # vulgar fraction one quarter = fraction one quarter, U+00BC ISOnum
registerEntity("frac12",CharRef(189)) # vulgar fraction one half = fraction one half, U+00BD ISOnum
registerEntity("frac34",CharRef(190)) # vulgar fraction three quarters = fraction three quarters, U+00BE ISOnum
registerEntity("iquest",CharRef(191)) # inverted question mark = turned question mark, U+00BF ISOnum
registerEntity("Agrave",CharRef(192)) # latin capital letter A with grave = latin capital letter A grave, U+00C0 ISOlat1
registerEntity("Aacute",CharRef(193)) # latin capital letter A with acute, U+00C1 ISOlat1
registerEntity("Acirc",CharRef(194)) # latin capital letter A with circumflex, U+00C2 ISOlat1
registerEntity("Atilde",CharRef(195)) # latin capital letter A with tilde, U+00C3 ISOlat1
registerEntity("Auml",CharRef(196)) # latin capital letter A with diaeresis, U+00C4 ISOlat1
registerEntity("Aring",CharRef(197)) # latin capital letter A with ring above = latin capital letter A ring, U+00C5 ISOlat1
registerEntity("AElig",CharRef(198)) # latin capital letter AE = latin capital ligature AE, U+00C6 ISOlat1
registerEntity("Ccedil",CharRef(199)) # latin capital letter C with cedilla, U+00C7 ISOlat1
registerEntity("Egrave",CharRef(200)) # latin capital letter E with grave, U+00C8 ISOlat1
registerEntity("Eacute",CharRef(201)) # latin capital letter E with acute, U+00C9 ISOlat1
registerEntity("Ecirc",CharRef(202)) # latin capital letter E with circumflex, U+00CA ISOlat1
registerEntity("Euml",CharRef(203)) # latin capital letter E with diaeresis, U+00CB ISOlat1
registerEntity("Igrave",CharRef(204)) # latin capital letter I with grave, U+00CC ISOlat1
registerEntity("Iacute",CharRef(205)) # latin capital letter I with acute, U+00CD ISOlat1
registerEntity("Icirc",CharRef(206)) # latin capital letter I with circumflex, U+00CE ISOlat1
registerEntity("Iuml",CharRef(207)) # latin capital letter I with diaeresis, U+00CF ISOlat1
registerEntity("ETH",CharRef(208)) # latin capital letter ETH, U+00D0 ISOlat1
registerEntity("Ntilde",CharRef(209)) # latin capital letter N with tilde, U+00D1 ISOlat1
registerEntity("Ograve",CharRef(210)) # latin capital letter O with grave, U+00D2 ISOlat1
registerEntity("Oacute",CharRef(211)) # latin capital letter O with acute, U+00D3 ISOlat1
registerEntity("Ocirc",CharRef(212)) # latin capital letter O with circumflex, U+00D4 ISOlat1
registerEntity("Otilde",CharRef(213)) # latin capital letter O with tilde, U+00D5 ISOlat1
registerEntity("Ouml",CharRef(214)) # latin capital letter O with diaeresis, U+00D6 ISOlat1
registerEntity("times",CharRef(215)) # multiplication sign, U+00D7 ISOnum
registerEntity("Oslash",CharRef(216)) # latin capital letter O with stroke = latin capital letter O slash, U+00D8 ISOlat1
registerEntity("Ugrave",CharRef(217)) # latin capital letter U with grave, U+00D9 ISOlat1
registerEntity("Uacute",CharRef(218)) # latin capital letter U with acute, U+00DA ISOlat1
registerEntity("Ucirc",CharRef(219)) # latin capital letter U with circumflex, U+00DB ISOlat1
registerEntity("Uuml",CharRef(220)) # latin capital letter U with diaeresis, U+00DC ISOlat1
registerEntity("Yacute",CharRef(221)) # latin capital letter Y with acute, U+00DD ISOlat1
registerEntity("THORN",CharRef(222)) # latin capital letter THORN, U+00DE ISOlat1
registerEntity("szlig",CharRef(223)) # latin small letter sharp s = ess-zed, U+00DF ISOlat1
registerEntity("agrave",CharRef(224)) # latin small letter a with grave = latin small letter a grave, U+00E0 ISOlat1
registerEntity("aacute",CharRef(225)) # latin small letter a with acute, U+00E1 ISOlat1
registerEntity("acirc",CharRef(226)) # latin small letter a with circumflex, U+00E2 ISOlat1
registerEntity("atilde",CharRef(227)) # latin small letter a with tilde, U+00E3 ISOlat1
registerEntity("auml",CharRef(228)) # latin small letter a with diaeresis, U+00E4 ISOlat1
registerEntity("aring",CharRef(229)) # latin small letter a with ring above = latin small letter a ring, U+00E5 ISOlat1
registerEntity("aelig",CharRef(230)) # latin small letter ae = latin small ligature ae, U+00E6 ISOlat1
registerEntity("ccedil",CharRef(231)) # latin small letter c with cedilla, U+00E7 ISOlat1
registerEntity("egrave",CharRef(232)) # latin small letter e with grave, U+00E8 ISOlat1
registerEntity("eacute",CharRef(233)) # latin small letter e with acute, U+00E9 ISOlat1
registerEntity("ecirc",CharRef(234)) # latin small letter e with circumflex, U+00EA ISOlat1
registerEntity("euml",CharRef(235)) # latin small letter e with diaeresis, U+00EB ISOlat1
registerEntity("igrave",CharRef(236)) # latin small letter i with grave, U+00EC ISOlat1
registerEntity("iacute",CharRef(237)) # latin small letter i with acute, U+00ED ISOlat1
registerEntity("icirc",CharRef(238)) # latin small letter i with circumflex, U+00EE ISOlat1
registerEntity("iuml",CharRef(239)) # latin small letter i with diaeresis, U+00EF ISOlat1
registerEntity("eth",CharRef(240)) # latin small letter eth, U+00F0 ISOlat1
registerEntity("ntilde",CharRef(241)) # latin small letter n with tilde, U+00F1 ISOlat1
registerEntity("ograve",CharRef(242)) # latin small letter o with grave, U+00F2 ISOlat1
registerEntity("oacute",CharRef(243)) # latin small letter o with acute, U+00F3 ISOlat1
registerEntity("ocirc",CharRef(244)) # latin small letter o with circumflex, U+00F4 ISOlat1
registerEntity("otilde",CharRef(245)) # latin small letter o with tilde, U+00F5 ISOlat1
registerEntity("ouml",CharRef(246)) # latin small letter o with diaeresis, U+00F6 ISOlat1
registerEntity("divide",CharRef(247)) # division sign, U+00F7 ISOnum
registerEntity("oslash",CharRef(248)) # latin small letter o with stroke, = latin small letter o slash, U+00F8 ISOlat1
registerEntity("ugrave",CharRef(249)) # latin small letter u with grave, U+00F9 ISOlat1
registerEntity("uacute",CharRef(250)) # latin small letter u with acute, U+00FA ISOlat1
registerEntity("ucirc",CharRef(251)) # latin small letter u with circumflex, U+00FB ISOlat1
registerEntity("uuml",CharRef(252)) # latin small letter u with diaeresis, U+00FC ISOlat1
registerEntity("yacute",CharRef(253)) # latin small letter y with acute, U+00FD ISOlat1
registerEntity("thorn",CharRef(254)) # latin small letter thorn, U+00FE ISOlat1
registerEntity("yuml",CharRef(255)) # latin small letter y with diaeresis, U+00FF ISOlat1

# C0 Controls and Basic Latin
registerEntity("quot",CharRef(34)) # quotation mark = APL quote, U+0022 ISOnum
registerEntity("amp",CharRef(38)) # ampersand, U+0026 ISOnum
registerEntity("lt",CharRef(60)) # less-than sign, U+003C ISOnum
registerEntity("gt",CharRef(62)) # greater-than sign, U+003E ISOnum

# Latin Extended-A
registerEntity("OElig",CharRef(338)) # latin capital ligature OE, U+0152 ISOlat2
registerEntity("oelig",CharRef(339)) # latin small ligature oe, U+0153 ISOlat2
registerEntity("Scaron",CharRef(352)) # latin capital letter S with caron, U+0160 ISOlat2
registerEntity("scaron",CharRef(353)) # latin small letter s with caron, U+0161 ISOlat2
registerEntity("Yuml",CharRef(376)) # latin capital letter Y with diaeresis, U+0178 ISOlat2

# Spacing Modifier Letters
registerEntity("circ",CharRef(710)) # modifier letter circumflex accent, U+02C6 ISOpub
registerEntity("tilde",CharRef(732)) # small tilde, U+02DC ISOdia

# General Punctuation
registerEntity("ensp",CharRef(8194)) # en space, U+2002 ISOpub
registerEntity("emsp",CharRef(8195)) # em space, U+2003 ISOpub
registerEntity("thinsp",CharRef(8201)) # thin space, U+2009 ISOpub
registerEntity("zwnj",CharRef(8204)) # zero width non-joiner, U+200C NEW RFC 2070
registerEntity("zwj",CharRef(8205)) # zero width joiner, U+200D NEW RFC 2070
registerEntity("lrm",CharRef(8206)) # left-to-right mark, U+200E NEW RFC 2070
registerEntity("rlm",CharRef(8207)) # right-to-left mark, U+200F NEW RFC 2070
registerEntity("ndash",CharRef(8211)) # en dash, U+2013 ISOpub
registerEntity("mdash",CharRef(8212)) # em dash, U+2014 ISOpub
registerEntity("lsquo",CharRef(8216)) # left single quotation mark, U+2018 ISOnum
registerEntity("rsquo",CharRef(8217)) # right single quotation mark, U+2019 ISOnum
registerEntity("sbquo",CharRef(8218)) # single low-9 quotation mark, U+201A NEW
registerEntity("ldquo",CharRef(8220)) # left double quotation mark, U+201C ISOnum
registerEntity("rdquo",CharRef(8221)) # right double quotation mark, U+201D ISOnum
registerEntity("bdquo",CharRef(8222)) # double low-9 quotation mark, U+201E NEW
registerEntity("dagger",CharRef(8224)) # dagger, U+2020 ISOpub
registerEntity("Dagger",CharRef(8225)) # double dagger, U+2021 ISOpub
registerEntity("permil",CharRef(8240)) # per mille sign, U+2030 ISOtech
registerEntity("lsaquo",CharRef(8249)) # single left-pointing angle quotation mark, U+2039 ISO proposed
registerEntity("rsaquo",CharRef(8250)) # single right-pointing angle quotation mark, U+203A ISO proposed
registerEntity("euro",CharRef(8364)) # euro sign, U+20AC NEW

# Mathematical, Greek and Symbolic characters
# Latin Extended-B
registerEntity("fnof",CharRef(402)) # latin small f with hook = function = florin, U+0192 ISOtech

# Greek
registerEntity("Alpha",CharRef(913)) # greek capital letter alpha, U+0391
registerEntity("Beta",CharRef(914)) # greek capital letter beta, U+0392
registerEntity("Gamma",CharRef(915)) # greek capital letter gamma, U+0393 ISOgrk3
registerEntity("Delta",CharRef(916)) # greek capital letter delta, U+0394 ISOgrk3
registerEntity("Epsilon",CharRef(917)) # greek capital letter epsilon, U+0395
registerEntity("Zeta",CharRef(918)) # greek capital letter zeta, U+0396
registerEntity("Eta",CharRef(919)) # greek capital letter eta, U+0397
registerEntity("Theta",CharRef(920)) # greek capital letter theta, U+0398 ISOgrk3
registerEntity("Iota",CharRef(921)) # greek capital letter iota, U+0399
registerEntity("Kappa",CharRef(922)) # greek capital letter kappa, U+039A
registerEntity("Lambda",CharRef(923)) # greek capital letter lambda, U+039B ISOgrk3
registerEntity("Mu",CharRef(924)) # greek capital letter mu, U+039C
registerEntity("Nu",CharRef(925)) # greek capital letter nu, U+039D
registerEntity("Xi",CharRef(926)) # greek capital letter xi, U+039E ISOgrk3
registerEntity("Omicron",CharRef(927)) # greek capital letter omicron, U+039F
registerEntity("Pi",CharRef(928)) # greek capital letter pi, U+03A0 ISOgrk3
registerEntity("Rho",CharRef(929)) # greek capital letter rho, U+03A1
registerEntity("Sigma",CharRef(931)) # greek capital letter sigma, U+03A3 ISOgrk3
registerEntity("Tau",CharRef(932)) # greek capital letter tau, U+03A4
registerEntity("Upsilon",CharRef(933)) # greek capital letter upsilon, U+03A5 ISOgrk3
registerEntity("Phi",CharRef(934)) # greek capital letter phi, U+03A6 ISOgrk3
registerEntity("Chi",CharRef(935)) # greek capital letter chi, U+03A7
registerEntity("Psi",CharRef(936)) # greek capital letter psi, U+03A8 ISOgrk3
registerEntity("Omega",CharRef(937)) # greek capital letter omega, U+03A9 ISOgrk3
registerEntity("alpha",CharRef(945)) # greek small letter alpha, U+03B1 ISOgrk3
registerEntity("beta",CharRef(946)) # greek small letter beta, U+03B2 ISOgrk3
registerEntity("gamma",CharRef(947)) # greek small letter gamma, U+03B3 ISOgrk3
registerEntity("delta",CharRef(948)) # greek small letter delta, U+03B4 ISOgrk3
registerEntity("epsilon",CharRef(949)) # greek small letter epsilon, U+03B5 ISOgrk3
registerEntity("zeta",CharRef(950)) # greek small letter zeta, U+03B6 ISOgrk3
registerEntity("eta",CharRef(951)) # greek small letter eta, U+03B7 ISOgrk3
registerEntity("theta",CharRef(952)) # greek small letter theta, U+03B8 ISOgrk3
registerEntity("iota",CharRef(953)) # greek small letter iota, U+03B9 ISOgrk3
registerEntity("kappa",CharRef(954)) # greek small letter kappa, U+03BA ISOgrk3
registerEntity("lambda",CharRef(955)) # greek small letter lambda, U+03BB ISOgrk3
registerEntity("mu",CharRef(956)) # greek small letter mu, U+03BC ISOgrk3
registerEntity("nu",CharRef(957)) # greek small letter nu, U+03BD ISOgrk3
registerEntity("xi",CharRef(958)) # greek small letter xi, U+03BE ISOgrk3
registerEntity("omicron",CharRef(959)) # greek small letter omicron, U+03BF NEW
registerEntity("pi",CharRef(960)) # greek small letter pi, U+03C0 ISOgrk3
registerEntity("rho",CharRef(961)) # greek small letter rho, U+03C1 ISOgrk3
registerEntity("sigmaf",CharRef(962)) # greek small letter final sigma, U+03C2 ISOgrk3
registerEntity("sigma",CharRef(963)) # greek small letter sigma, U+03C3 ISOgrk3
registerEntity("tau",CharRef(964)) # greek small letter tau, U+03C4 ISOgrk3
registerEntity("upsilon",CharRef(965)) # greek small letter upsilon, U+03C5 ISOgrk3
registerEntity("phi",CharRef(966)) # greek small letter phi, U+03C6 ISOgrk3
registerEntity("chi",CharRef(967)) # greek small letter chi, U+03C7 ISOgrk3
registerEntity("psi",CharRef(968)) # greek small letter psi, U+03C8 ISOgrk3
registerEntity("omega",CharRef(969)) # greek small letter omega, U+03C9 ISOgrk3
registerEntity("thetasym",CharRef(977)) # greek small letter theta symbol, U+03D1 NEW
registerEntity("upsih",CharRef(978)) # greek upsilon with hook symbol, U+03D2 NEW
registerEntity("piv",CharRef(982)) # greek pi symbol, U+03D6 ISOgrk3

# General Punctuation
registerEntity("bull",CharRef(8226)) # bullet = black small circle, U+2022 ISOpub
registerEntity("hellip",CharRef(8230)) # horizontal ellipsis = three dot leader, U+2026 ISOpub
registerEntity("prime",CharRef(8242)) # prime = minutes = feet, U+2032 ISOtech
registerEntity("Prime",CharRef(8243)) # double prime = seconds = inches, U+2033 ISOtech
registerEntity("oline",CharRef(8254)) # overline = spacing overscore, U+203E NEW
registerEntity("frasl",CharRef(8260)) # fraction slash, U+2044 NEW

# Letterlike Symbols
registerEntity("weierp",CharRef(8472)) # script capital P = power set = Weierstrass p, U+2118 ISOamso
registerEntity("image",CharRef(8465)) # blackletter capital I = imaginary part, U+2111 ISOamso
registerEntity("real",CharRef(8476)) # blackletter capital R = real part symbol, U+211C ISOamso
registerEntity("trade",CharRef(8482)) # trade mark sign, U+2122 ISOnum
registerEntity("alefsym",CharRef(8501)) # alef symbol = first transfinite cardinal, U+2135 NEW

# Arrows
registerEntity("larr",CharRef(8592)) # leftwards arrow, U+2190 ISOnum
registerEntity("uarr",CharRef(8593)) # upwards arrow, U+2191 ISOnu
registerEntity("rarr",CharRef(8594)) # rightwards arrow, U+2192 ISOnum
registerEntity("darr",CharRef(8595)) # downwards arrow, U+2193 ISOnum
registerEntity("harr",CharRef(8596)) # left right arrow, U+2194 ISOamsa
registerEntity("crarr",CharRef(8629)) # downwards arrow with corner leftwards = carriage return, U+21B5 NEW
registerEntity("lArr",CharRef(8656)) # leftwards double arrow, U+21D0 ISOtech
registerEntity("uArr",CharRef(8657)) # upwards double arrow, U+21D1 ISOamsa
registerEntity("rArr",CharRef(8658)) # rightwards double arrow, U+21D2 ISOtech
registerEntity("dArr",CharRef(8659)) # downwards double arrow, U+21D3 ISOamsa
registerEntity("hArr",CharRef(8660)) # left right double arrow, U+21D4 ISOamsa

# Mathematical Operators
registerEntity("forall",CharRef(8704)) # for all, U+2200 ISOtech
registerEntity("part",CharRef(8706)) # partial differential, U+2202 ISOtech
registerEntity("exist",CharRef(8707)) # there exists, U+2203 ISOtech
registerEntity("empty",CharRef(8709)) # empty set = null set = diameter, U+2205 ISOamso
registerEntity("nabla",CharRef(8711)) # nabla = backward difference, U+2207 ISOtech
registerEntity("isin",CharRef(8712)) # element of, U+2208 ISOtech
registerEntity("notin",CharRef(8713)) # not an element of, U+2209 ISOtech
registerEntity("ni",CharRef(8715)) # contains as member, U+220B ISOtech
registerEntity("prod",CharRef(8719)) # n-ary product = product sign, U+220F ISOamsb
registerEntity("sum",CharRef(8721)) # n-ary sumation, U+2211 ISOamsb
registerEntity("minus",CharRef(8722)) # minus sign, U+2212 ISOtech
registerEntity("lowast",CharRef(8727)) # asterisk operator, U+2217 ISOtech
registerEntity("radic",CharRef(8730)) # square root = radical sign, U+221A ISOtech
registerEntity("prop",CharRef(8733)) # proportional to, U+221D ISOtech
registerEntity("infin",CharRef(8734)) # infinity, U+221E ISOtech
registerEntity("ang",CharRef(8736)) # angle, U+2220 ISOamso
registerEntity("and",CharRef(8743)) # logical and = wedge, U+2227 ISOtech
registerEntity("or",CharRef(8744)) # logical or = vee, U+2228 ISOtech
registerEntity("cap",CharRef(8745)) # intersection = cap, U+2229 ISOtech
registerEntity("cup",CharRef(8746)) # union = cup, U+222A ISOtech
registerEntity("int",CharRef(8747)) # integral, U+222B ISOtech
registerEntity("there4",CharRef(8756)) # therefore, U+2234 ISOtech
registerEntity("sim",CharRef(8764)) # tilde operator = varies with = similar to, U+223C ISOtech
registerEntity("cong",CharRef(8773)) # approximately equal to, U+2245 ISOtech
registerEntity("asymp",CharRef(8776)) # almost equal to = asymptotic to, U+2248 ISOamsr
registerEntity("ne",CharRef(8800)) # not equal to, U+2260 ISOtech
registerEntity("equiv",CharRef(8801)) # identical to, U+2261 ISOtech
registerEntity("le",CharRef(8804)) # less-than or equal to, U+2264 ISOtech
registerEntity("ge",CharRef(8805)) # greater-than or equal to, U+2265 ISOtech
registerEntity("sub",CharRef(8834)) # subset of, U+2282 ISOtech
registerEntity("sup",CharRef(8835)) # superset of, U+2283 ISOtech
registerEntity("nsub",CharRef(8836)) # not a subset of, U+2284 ISOamsn
registerEntity("sube",CharRef(8838)) # subset of or equal to, U+2286 ISOtech
registerEntity("supe",CharRef(8839)) # superset of or equal to, U+2287 ISOtech
registerEntity("oplus",CharRef(8853)) # circled plus = direct sum, U+2295 ISOamsb
registerEntity("otimes",CharRef(8855)) # circled times = vector product, U+2297 ISOamsb
registerEntity("perp",CharRef(8869)) # up tack = orthogonal to = perpendicular, U+22A5 ISOtech
registerEntity("sdot",CharRef(8901)) # dot operator, U+22C5 ISOamsb

# Miscellaneous Technical
registerEntity("lceil",CharRef(8968)) # left ceiling = apl upstile, U+2308 ISOamsc
registerEntity("rceil",CharRef(8969)) # right ceiling, U+2309 ISOamsc
registerEntity("lfloor",CharRef(8970)) # left floor = apl downstile, U+230A ISOamsc
registerEntity("rfloor",CharRef(8971)) # right floor, U+230B ISOamsc
registerEntity("lang",CharRef(9001)) # left-pointing angle bracket = bra, U+2329 ISOtech
registerEntity("rang",CharRef(9002)) # right-pointing angle bracket = ket, U+232A ISOtech

# Geometric Shapes
registerEntity("loz",CharRef(9674)) # lozenge, U+25CA ISOpub

# Miscellaneous Symbols
registerEntity("spades",CharRef(9824)) # black spade suit, U+2660 ISOpub
registerEntity("clubs",CharRef(9827)) # black club suit = shamrock, U+2663 ISOpub
registerEntity("hearts",CharRef(9829)) # black heart suit = valentine, U+2665 ISOpub
registerEntity("diams",CharRef(9830)) # black diamond suit, U+2666 ISOpub

###
###
###

class XSC:
	"""
	contains the options and functions for handling the XML files
	"""

	def __init__(self):
		self.filename = []
		self.server = "localhost"
		self.repransielementname = "35"
		self.reprtree = 1
		self.parser = Parser()

	def __pushName(self,name):
		url = _URL(name)
		if url.scheme == "":
			url.scheme = "project"
		if len(self.filename) <= 2:
			self.filename = [ url , url ]
		else:
			self.filename.append(url)

	def __popName(self):
		self.filename.pop()

	def parseString(self,name,string):
		"""
		Parses a string and returns the resulting XSC
		"""
		self.__pushName(name)
		self.parser.reset()
		self.parser.feed(string)
		self.parser.close()
		self.__popName()
		return self.parser.root

	def parseFile(self,name):
		"""
		Reads and parses a XML file and returns the resulting XSC
		"""
		self.__pushName(name)
		self.parser.reset()
		self.parser.feed(open(name).read())
		self.parser.close()
		self.__popName()
		return self.parser.root

	def parseURL(self,url):
		"""
		Reads and parses a XML file from an URL and returns the resulting XSC
		"""
		self.__pushName(name)
		self.parser.reset()
		self.parser.feed(urllib.urlopen(name).read())
		self.parser.close()
		urllib.urlcleanup()
		self.__popName()
		return self.parser.root

	def __repr__(self):
		return '<xsc filename="' + self.filename + '" server="' + self.server + '" retrieveremote=' + [ 'no' , 'yes' ][retrieveremote] + '" retrievelocal=' + [ 'no' , 'yes' ][retrievelocal] + '>'

	def is_remote(self,url):
		(scheme,server,path,parameters,query,fragment) = urlparse.urlparse(url)
		if scheme != "":
			if server != "localhost" and server != _socket.gethostname():
				return 1
		return 0

	def is_retrieve(self,url):
		remote = self.is_remote(url)
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

retrieveremote = 1 # should remote URLs be retrieved? (for filesize and imagesize tests)
retrievelocal  = 1 # should local URLs be retrieved? (for filesize and imagesize tests)

def make():
	"""
	use XSC as a compiler script, i.e. read an input file from args[1]
	and writes it to args[2]
	"""

	infilename = sys.argv[1]
	outfilename = sys.argv[2]
	if len(outfilename) and outfilename[-1] == "/":
		outfilename = outfilename + infilename
	e_in = xsc.parseFile(infilename)
	e_out = e_in.asHTML()
	__forceopen(outfilename,"wb").write(str(e_out))

xsc = XSC()

if __name__ == "__main__":
	make()

