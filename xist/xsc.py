#! /usr/bin/env python

""""""

__version__ = "$Revision$"
# $Source$

import os
import string
import types
import exceptions
import sys

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

###
### exceptions
###

class Error(Exception):
	"""base class for all XSC exceptions"""

	def __init__(self,lineno):
		self.lineno = lineno

	def __str__(self):
		if self.lineno>0:
			return " (line " + str(self.lineno) + ")"
		else:
			return ""

class EmptyElementWithContentError(Error):
	"""exception that is raised, when an element has content, but it shouldn't (i.e. empty=1)"""

	def __init__(self,lineno,element):
		Error.__init__(self,lineno)
		self.element = element

	def __str__(self):
		return Error.__str__(self) + "element " + self.element._strname() + " specified to be empty, but has content"

class IllegalAttributeError(Error):
	"""exception that is raised, when an element has an illegal attribute (i.e. one that isn't contained in it's attr_handlers)"""

	def __init__(self,lineno,element,attr):
		Error.__init__(self,lineno)
		self.element = element
		self.attr = attr

	def __str__(self):
		attrs = self.element.attr_handlers.keys();
		attrs.sort()

		v = []

		for attr in attrs:
			v.append(_strattrname(attr))

		return Error.__str__(self) + "Attribute " + _strattrname(self.attr) + " not allowed in element " + self.element._strname() + ". Allowed attributes are: " + string.join(v,", ") + "."

class AttributeNotFoundError(Error):
	"""exception that is raised, when an attribute is fetched that isn't there"""

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
	"""exception that is raised, when an illegal element is encountered (i.e. one that isn't registered via registerElement"""

	def __init__(self,lineno,name):
		Error.__init__(self,lineno)
		self.name = name

	def __str__(self):
		elementnames = []
		for elementname in _element_handlers.keys():
			for namespace in _element_handlers[elementname].keys():
				elementnames.append(_strNodeName(_element_handlers[elementname][namespace]))
		elementnames.sort()

		if self.name[0]:
			name = _strelementname(self.name[0]) + ":" + _strelementname(self.name[1])
		else:
			name = _strelementname(self.name[1])

		return Error.__str__(self) + "element " + name + " not allowed. Allowed elements are: " + string.join(elementnames,", ") + "."

class IllegalElementNestingError(Error):
	"""exception that is raised, when an element has an illegal nesting (e.g. <a><b></a></b>)"""

	def __init__(self,lineno,expectedelementname,foundelementname):
		Error.__init__(self,lineno)
		self.expectedelementname = expectedelementname
		self.foundelementname = foundelementname

	def __str__(self):
		return Error.__str__(self) + "illegal element nesting (" + _strelementname(self.expectedelementname) + " expected; " + _strelementname(self.foundelementname) + " found)"

class ImageSizeFormatError(Error):
	"""exception that is raised, when XSC can't format or evaluate image size attributes"""

	def __init__(self,lineno,element,attr):
		Error.__init__(self,lineno)
		self.element = element
		self.attr = attr

	def __str__(self):
		return Error.__str__(self) + "the value '" + str(self.element[self.attr]) + "' for the image size attribute " + _strattrname(self.attr) + " of the element " + self.element._strname() + " can't be formatted or evaluated"

class FileNotFoundError(Error):
	"""exception that is raised, when XSC can't open an image for getting image size"""

	def __init__(self,lineno,url):
		Error.__init__(self,lineno)
		self.url = url

	def __str__(self):
		return Error.__str__(self) + "file " + self.url.repr() + " can't be opened"

class IllegalObjectError(Error):
	"""exception that is raised, when XSC finds an illegal object found in its object tree"""

	def __init__(self,lineno,object):
		Error.__init__(self,lineno)
		self.object = object

	def __str__(self):
		return Error.__str__(self) + "an illegal object of type " + type(self.object).__name__ + " has been found in the XSC tree"

class MalformedCharRefError(Error):
	"""exception that is raised, when a character reference is malformed (e.g. &#foo;)"""

	def __init__(self,lineno,name):
		Error.__init__(self,lineno)
		self.name = name

	def __str__(self):
		return Error.__str__(self) + "malformed character reference: &#" + self.name + ";"

class UnknownEntityError(Error):
	"""
	exception that is raised, when an unknown entity (i.e. one that wasn't registered via RegisterEntity) is encountered
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
		for namespace in _element_handlers[self.name[1]].keys():
			elementnames.append(_strNodeName(_element_handlers[self.name[1]][namespace]))
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
	if xsc.repransi and codes!="" and string!="":
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

def ToNode(value):
	if type(value) == types.StringType:
		return Text(value)
	elif type(value) == types.NoneType:
		return None
	elif type(value) in [ types.IntType,types.LongType ] :
		return CharRef(value)
	elif type(value) == types.FloatType :
		return Text(str(value))
	elif type(value) in [ types.ListType,types.TupleType ]:
		v = Frag()
		for i in value:
			v.append(ToNode(i))
		return v
	elif type(value) == types.DictType:
		raise IllegalObjectError(xsc.parser.lineno,value) # no dictionaries allowed
	elif type(value) == types.InstanceType:
		if isinstance(value,Frag):
			if len(value)==1:
				return ToNode(value[0]) # recursively try to simplify the tree
			else:
				return value
		elif isinstance(value,Attr):
			return value.content
		else:
			return value
	raise IllegalObjectError(xsc.parser.lineno,value) # none of the above, so we throw and exception

_element_handlers = {} # dictionary for mapping element names to classes, this dictionary contains the element names as keys and another dictionary as values, this second dictionary contains the namespace names as keys and the element classes as values

class Node:
	"""base class for nodes in the document tree. Derived class must implement __str__()"""

	# line numbers where this node starts and ends in a file (will be hidden in derived classes, but is specified here, so that no special tests are required. In derived classes both variables will be set by the parser)
	startlineno = -1
	endlineno = -1
	repransinamespace = "31"
	repransiname = ""
	repransibrackets = "34;1"

	def __add__(self,other):
		if other != None:
			return Frag(self) + other
		else:
			return self

	def __radd__(self,other):
		if other != None:
			return Frag(other) + self
		else:
			return self

	def __repr__(self):
		if xsc.reprtree == 1:
			return self.reprtree()
		else:
			return self.repr()

	def name(self):
		"""
		returns a tuple with the namespace of the node, which is the module in which the node is implemented
		and a name which is the name of the class. Both strings are converted to lowercase.
		"""
		return nodeName(self.__class__)

	def _strname(self):
		return _strNodeName(self.__class__)

	def clone(self):
		"""
		returns an identical clone of the node.
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
			line[3] = _stransi(xsc.repransitab,xsc.reprtab*line[0]) + line[3] # add indentation
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
		return None

	def _strtag(self,content):
		return _stransi(self.repransibrackets,'<') + content + _stransi(self.repransibrackets,'>')
 
	def __str__(self):
		return ""

	def elements(self):
		"""
		returns a fragment with all child elements of this node.
		"""
		return Frag()

	def elementsNamed(self,element):
		"""
		returns a fragment with all child elements of this node that are of the type element
		(which has to be the class of an element).
		"""
		return Frag()

	def elementsDerivedFrom(self,element):
		"""
		returns a fragment with all child elements of this node that are derived from the type element
		(which has to be the class of an element).
		"""
		return Frag()

	def allElementsNamed(self,element):
		"""
		returns a fragment with all elements (children and grandchildren) of this node that are of type element.
		(which has to be the class of an element).
		"""
		return Frag()
 
	def allElementsDerivedFrom(self,element):
		"""
		returns a fragment with all elements (children and grandchildren) of this node that are derived from the type element.
		(which has to be the class of an element).
		"""
		return Frag()
 
	def withoutLinefeeds(self):
		"""returns this node, where all linefeeds that are in a text
		(or character reference) by themselves are removed, i.e. potentially
		needless whitespace is removed"""
		return None
		
class Text(Node):
	"""text"""

	repransiname = ""
	repransiquotes = "34;1"

	represcapes = { '\t' : '\\t' , '\033' : '\\e' , '\\' : '\\\\' }
	reprtreeescapes = { '\r' : '\\r' , '\n' : '\\n' , '\t' : '\\t' , '\033' : '\\e' , '\\' : '\\\\' }
	strescapes = { '<' : 'lt' , '>' : 'gt' , '&' : 'amp' , '"' : 'quot' }

	def __init__(self,content = ""):
		self.__content = content

	def asHTML(self):
		return Text(self.__content)

	clone = asHTML

	def __str__(self):
		v = []
		for i in self.__content:
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
		charref = -1 # the type of characters we're currently collecting (0==normal character, 1==character that have to be output as entities, -1==at the start)
		start = 0 # the position where our current run of characters for the same class started
		end = 0 # the current position we're testing
		while end<=len(self.__content): # one more than the length of the string
			do = 0 # we will have to do something with the string collected so far ...
			if end == len(self.__content): # ... if we're at the end of the string
				do = 1
			else:
				c = self.__content[end] # or if the character we're at is different from those we've collected so far
				ascharref = (0 <= ord(c) <= 31 or 128 <= ord(c))
				if not refwhite and (c == "\n" or c == "\t"):
					ascharref = 0
				if ascharref != charref:
					do = 1
					charref = 1-ascharref # this does nothing, except at the start, where it enforces the correct processing
			if do: # process the string we have so far
				if charref: # we've collected references so far
					s = ""
					for i in self.__content[start:end]:
						ent = Parser.entitiesByNumber[ord(i)] # use names if a available, or number otherwise
						if len(ent):
							s = s + '&' + ent[0] + ';'
						else:
							s = s + '&#' + str(self.__content) + ';'
					v.append(_stransi(CharRef.repransiname,s))
				else:
					s = self.__content[start:end]
					v.append(_stransi(Text.repransiname,s))
				charref = 1-charref # switch to the other class
				start = end # the next string  we want to work on starts from here
			end = end + 1 # to the next character
				
		return string.join(v,"")

	def _dorepr(self):
		# constructs a string of this Text with syntaxhighlighting. Special characters will be output as CharRefs (with special highlighting)
		return self.__strtext(0)

	def _doreprtree(self,nest,elementno):
		s = _stransi(self.repransiquotes,'"') + _stransi(self.repransiname,self.__strtext(1)) + _stransi(self.repransiquotes,'"')
		return [[nest,self.startlineno,elementno,s]]

	def withoutLinefeeds(self):
		for i in self.__content:
			if i != '\n' and i != '\r':
				return Text(self.__content)
		else:
			return None

class CharRef(Node):
	"""character reference (i.e &#42; or &#x42;)"""

	repransiname = "32"

	__notdirect = { ord("&") : "amp" , ord("<") : "lt" , ord(">") : "gt", ord('"') : "quot" , ord("'") : "apos" }
	__linefeeds = [ ord("\r") , ord("\n") ]

	def __init__(self,content):
		self.__content = content

	def asHTML(self):
		return CharRef(self.__content)

	clone = asHTML

	def __str__(self):
		if 0<=self.__content<=127:
			if self.__content != ord("\r"):
				if self.__notdirect.has_key(self.__content):
					return '&' + self.__notdirect[self.__content] + ';'
				else:
					return chr(self.__content)
		else:
			return '&#' + str(self.__content) + ';'

	def __strcharref(self,s):
		return _stransi(self.repransiname,s)
 
	def _dorepr(self):
		if len(Parser.entitiesByNumber[self.__content]):
			return self.__strcharref('#' + Parser.entitiesByNumber[self.__content][0] + ';')
		else:
			return self.__strcharref('&#' + str(self.__content) + ';')

	def _doreprtree(self,nest,elementno):
		s = self.__strcharref('&#' + str(self.__content) + ';') + ' (' + self.__strcharref('&#x' + hex(self.__content)[2:] + ';')
		for name in Parser.entitiesByNumber[self.__content]:
			s = s + ' ' + self.__strcharref('&' + name + ';')
		s = s + ')'
		if 0 <= self.__content <= 255:
			s = s + ' ' + Text(chr(self.__content))._doreprtree(0,0)[0][-1]
		return [[nest,self.startlineno,elementno,s]]

	def withoutLinefeeds(self):
		if self.__content in self.__linefeeds:
			return None
		else:
			return CharRef(self.__content)

class Frag(Node):
	"""contains a list of Nodes"""

	repransiname = ""

	def __init__(self,_content = []):
		if _content is None:
			self._content = []
		elif type(_content) == types.InstanceType:
			if isinstance(_content,Frag):
				self._content = map(ToNode,_content._content)
			else:
				self._content = [ ToNode(_content) ]
		elif type(_content) in [ types.ListType , types.TupleType ]:
			self._content = map(ToNode,_content)
		else:
			self._content = [ ToNode(_content) ]

	def __add__(self,other):
		res = Frag(self._content)
		if other is not None:
			newother = ToNode(other)
			if isinstance(newother,Frag):
				res._content = res._content + newother._content
			else:
				res._content.append(newother)
		return res

	def __radd__(self,other):
		res = Frag(self._content)
		if other is not None:
			newother = ToNode(other)
			if isinstance(newother,Frag):
				res._content = newother._content + res._content
			else:
				res._content = [ newother ] + res._content
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
		"""returns the index'th node for the content of the fragment"""
		return self._content[index]

	def __setitem__(self,index,value):
		"""allows you to replace the index'th content node of the fragment"""
		if len(self._content)>index:
			self._content[index] = ToNode(value)

	def __delitem__(self,index):
		"""removes the index'th content node from the fragment"""
		if len(self._content)>index:
			del self._content[index]

	def __getslice__(self,index1,index2):
		"""returns a slice of the content of the fragment"""
		return Frag(self._content[index1:index2])

	def __setslice__(self,index1,index2,sequence):
		"""modifies a slice of the content of the fragment"""
		self._content[index1:index2] = map(ToNode,sequence)

	def __delslice__(self,index1,index2):
		"""removes a slice of the content of the fragment"""
		del self._content[index1:index2]

	def __len__(self):
		"""return the number of children"""
		return len(self._content)

	def append(self,other):
		if other != None:
			self._content.append(ToNode(other))

	def preppend(self,other):
		if other != None:
			self._content = [ ToNode(other) ] + self._content[:]

	def withoutLinefeeds(self):
		e = Frag()
		for child in self:
			e.append(child.withoutLinefeeds())
		return e

	def elements(self):
		e = Frag()
		for child in self:
			if isinstance(child,Element):
				e.append(child)
		return e

	def elementsNamed(self,element):
		e = Frag()
		for child in self:
			if child.__class__ == element:
				e.append(child)
		return e

	def elementsDerivedFrom(self,element):
		e = Frag()
		for child in self:
			if isinstance(child,element):
				e.append(child)
		return e

	def allElementsNamed(self,element):
		e = Frag()
		for child in self:
			e = e + child.allElementsNamed(element)
		return e

	def allElementsDerivedFrom(self,element):
		e = Frag()
		for child in self:
			e = e + child.allElementsDerivedFrom(element)
		return e

class Comment(Node):
	"""comments"""

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

	def withoutLinefeeds(self):
		return Comment(self.__content)

class DocType(Node):
	"""document type"""

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

	def withoutLinefeeds(self):
		return DocType(self.__content)

class ProcInst(Node):
	"""processing instructions"""

	repriansiname = "34"
	repransiquestion = "34"
	repransidata = "36"

	def __init__(self,target,content = ""):
		self.__target = target
		self.__content = content

	def asHTML(self):
		return ProcInst(self.__target,self.__content)

	clone = asHTML

	def _dorepr(self):
		return self._strtag(_stransi(self.repransiquestion,"?") + _stransi(self.repransiname,self.__target) + " " + _stransi(self.repransidata,self.__content) + _stransi(self.repransiquestion,"?"))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		return "<?" + self.__target + " " + self.__content + "?>"

	def withoutLinefeeds(self):
		return ProcInst(self.__target,self.__content)

class Element(Node):
	"""XML elements"""

	repransiname = "34"
	repransiattrquotes = "34"

	empty = 1 # 0 => element with content; 1 => stand alone element
 	attr_handlers = {}

	def __init__(self,_content = [],_attrs = {},**_restattrs):
		self.content = Frag(_content)
		self.attrs = {}
		for attr in _attrs.keys():
			self[attr] = _attrs[attr]
		for attr in _restattrs.keys():
			self[attr] = _restattrs[attr]

	def append(self,item):
		if item is not None:
			if self.empty:
				raise EmptyElementWithContentError(xsc.parser.lineno,self)
			else:
				self.content.append(item)

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
			v.append(self._strname() + self.__strattrs() + _strelementname("/"))
		else:
			v.append(self._strname() + self.__strattrs())
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
		"""returns this element as a string converted to HTML"""

		v = []
		v.append("<")
		v.append(string.lower(self.__class__.__name__))
		for attr in self.attrs.keys():
			v.append(' ')
			v.append(attr)
			v.append('="')
			v.append(str(self[attr]))
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
			if self.attrs.has_key(lowerindex):
				return self.attrs[lowerindex] # we're returning the packed attribute here, because otherwise there would be no possibility to get an expanded URL
			else:
				raise AttributeNotFoundError(xsc.parser.lineno,self,index)
		else:
			return self.content[index]

	def __setitem__(self,index,value):
		"""
		sets an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number (i.e. content node index) is passed in.
		"""
		if type(index)==types.StringType:
			# values are contructed via the attribute classes specified in the attr_handlers dictionary, which do the conversion
			lowerindex = string.lower(index)
			if self.attr_handlers.has_key(lowerindex):
				self.attrs[lowerindex] = self.attr_handlers[lowerindex](value) # pack the attribute into an attribute object
			else:
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
			v.append('=')
			v.append(_stransi(self.repransiattrquotes,'"'))
			v.append(self[attr]._dorepr())
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

	def withoutLinefeeds(self):
		return self.__class__(self.content.withoutLinefeeds(),self.attrs)

	def elements(self):
		return self.content.elements()

	def elementsNamed(self,element):
		return self.content.elementsNamed(element)

	def elementsDerivedFrom(self,element):
		return self.content.elementsDerivedFrom(element)

	def allElementsNamed(self,element):
		e = Frag()
		if self.__class__ == element:
				e.append(self)
		e = e + self.content.allElementsNamed(element)
		return e

	def allElementsDerivedFrom(self,element):
		e = Frag()
		if isinstance(self,element):
			e.append(self)
		e = e + self.content.allElementsDerivedFrom(element)
		return e


def registerElement(element):
	"""
	registers the element handler element to be used for elements with the appropriate name.
	"""
	name = nodeName(element)
	if _element_handlers.has_key(name[1]):
		_element_handlers[name[1]][name[0]] = element
	else:
		_element_handlers[name[1]] = { name[0] : element }

class Attr(Node):
	"""
	Base classes of all attribute classes
	"""

	repransi = "33"

	def __init__(self,_content):
		self.content = ToNode(_content)

	def __add__(self,other):
		if other is not None:
			return self.__class__(self.content+ToNode(other))
		else:
			return self

	def __radd__(self,other):
		if other is not None:
			return self.__class__(ToNode(other)+self.content)
		else:
			return self

class TextAttr(Attr):
	"""
	Attribute class that is used for normal text attributes.
	"""

	def __init__(self,_content):
		Attr.__init__(self,_content)

	def _dorepr(self):
		return _stransi(xsc.repransitextattrs,str(self.content))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		return str(self.content)

	def asHTML(self):
		return TextAttr(self.content.clone())

	clone = asHTML

class ColorAttr(Attr):
	"""
	Attribute class that is used for a color attributes.
	"""

	def __init__(self,_content):
		Attr.__init__(self,_content)

	def _dorepr(self):
		return _stransi(xsc.repransitextattrs,str(self.content))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		return str(self.content)

	def asHTML(self):
		return ColorAttr(self.content.clone())

	clone = asHTML

class URLAttr(Attr):
	"""
	Attribute class that is used for URLs.

	XSC has one additional feature, that it allows URLs that are local filenames starting with a ':'.
	Those filenames are not relative to the directory containing the file where the URL originated,
	but local to the "project" directory, i.e. the root directory of all XSC files, which is the
	current directory.

	With this feature you don't have to remember how deeply you've nested your XSC file tree, you
	can specify such file from everywhere via ":dir/to/file.xsc". XSC will change this to an URL
	that correctly locates the file (e.g. "../../../dir/to/file", when you're nested three levels
	deep in a different directory that "dir".

	When dumping these URLs in the interactive Python environment (i.e. calling __repr__) these
	URLs will be shown with the pseudo scheme "project".

	Server relative URLs will be shown with the pseudo scheme "server". For checking these URLs
	for image or file size, a http request will be made to the server specified in the "server"
	option.

	For all other URLs a normal request will be made corresponding to the specified scheme
	(http, ftp, etc.)
	"""

	repransiname = "31"
	repransiurl = "32"

	def __init__(self,_content):
		Attr.__init__(self,_content)
		url = str(self.content)
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
			del self.path[0] # if we had a http, the path from urlparse started with "/" too

	def _dorepr(self):
		url = urlparse.urlunparse((self.scheme,self.server,string.join(self.path,"/"),self.parameters,self.query,self.fragment))
		return _stransi(self.repransiurl,url)

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		return self.forOutput()

	def asHTML(self):
		return URLAttr(Text(self.forOutput()))

	clone = asHTML

	def forInput(self):
		scheme = self.scheme
		server = self.server
		path = self.path[:]
		parameters = self.parameters
		query = self.query
		fragment = self.fragment
		sep = "/" # use the normal URL separator by default
		if scheme == "server":
			scheme = "http"
			server = xsc.server
		elif scheme == "project" or scheme == "":
			file = string.split(xsc.filename,"/")
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
		scheme = self.scheme
		path = self.path[:]
		if scheme == "project":
			file = string.split(xsc.filename,"/") # split the file path too
			while len(file)>1 and len(path)>1 and file[0]==path[0]: # throw away identical directories in both paths (we don't have to go up from file and down to path for these identical directories
				del file[0]
				del path[0]
			path[:0] = [".."]*(len(file)-1) # now for the rest of the path we have to go up from file and down to path (the directories for this are still in path)
			scheme = "" # remove our own private scheme name
		elif scheme == "server":
			scheme = ""
			path[:0] = [ "" ]
		return urlparse.urlunparse((scheme,self.server,string.join(path,"/"),self.parameters,self.query,self.fragment))

	def ImageSize(self):
		"""returns the size of an image as a tuple or (-1,-1) if the image shouldn't be read"""

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
		"""returns the size of a file in bytes or -1 if the file shouldn't be read"""

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
		if self.entitiesByName.has_key(name):
			self.__appendNode(CharRef(self.entitiesByName[name]))
		else:
			raise UnknownEntityError(xsc.parser.lineno,name)

	def unknown_starttag(self,name,attrs):
  		lowername = string.split(string.lower(name),":")
		if len(lowername) == 2: # namespace specified
			name = lowername
		else:
			name = [	None , lowername[0] ]
		try: # are there any elements with this name?
			elementsfornamespaces = _element_handlers[name[1]]
		except KeyError: # nope!
			raise IllegalElementError(xsc.parser.lineno,name)
		if name[0] is None: # element name was unqualified ...
			if len(elementsfornamespaces.keys())==1: # ... and there is exactly one element with this name => use it
				e = elementsfornamespaces.values()[0]([],attrs)
			else:
				raise AmbiguousElementError(xsc.parser.lineno,name) # there is more than one
		else: # element name was qualified with a namespace
			try:
				element = elementsfornamespaces[name[0]]
			except KeyError:
				raise IllegalElementError(xsc.parser.lineno,name) # elements with this name were available, but none in this namespace
			e = element([],attrs)
			e.startlineno = self.lineno
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

def registerEntity(name,number):
	if Parser.entitiesByNumber[number] == None:
		Parser.entitiesByNumber[number] = []
	Parser.entitiesByNumber[number].append(name)
	Parser.entitiesByName[name] = number

registerEntity("amp",38)
registerEntity("lt",60)
registerEntity("gt",62)
registerEntity("apos",39)
registerEntity("quot",34)
registerEntity("lf",10)
registerEntity("cr",13)
registerEntity("ht",9)
registerEntity("tab",9)
registerEntity("esc",27)
registerEntity("nbsp",160)
registerEntity("iexcl",161)
registerEntity("cent",162)
registerEntity("pound",163)
registerEntity("curren",164)
registerEntity("yen",165)
registerEntity("brvbar",166)
registerEntity("sect",167)
registerEntity("die",168)
registerEntity("copy",169)
registerEntity("ordf",170)
registerEntity("laquo",171)
registerEntity("not",172)
registerEntity("shy",173)
registerEntity("reg",174)
registerEntity("macr",175)
registerEntity("deg",176)
registerEntity("plusmn",177)
registerEntity("sup2",178)
registerEntity("sup3",179)
registerEntity("acute",180)
registerEntity("micro",181)
registerEntity("para",182)
registerEntity("middot",183)
registerEntity("cedil",184)
registerEntity("sup1",185)
registerEntity("ordm",186)
registerEntity("raquo",187)
registerEntity("frac14",188)
registerEntity("frac12",189)
registerEntity("frac34",190)
registerEntity("iquest",191)
registerEntity("Agrave",192)
registerEntity("Aacute",193)
registerEntity("Acirc",194)
registerEntity("Atilde",195)
registerEntity("Auml",196)
registerEntity("Aring",197)
registerEntity("AElig",198)
registerEntity("Ccedil",199)
registerEntity("Egrave",200)
registerEntity("Eacute",201)
registerEntity("Ecirc",202)
registerEntity("Euml",203)
registerEntity("Igrave",204)
registerEntity("Iacute",205)
registerEntity("Icirc",206)
registerEntity("Iuml",207)
registerEntity("ETH",208)
registerEntity("Ntilde",209)
registerEntity("Ograve",210)
registerEntity("Oacute",211)
registerEntity("Ocirc",212)
registerEntity("Otilde",213)
registerEntity("Ouml",214)
registerEntity("times",215)
registerEntity("Oslash",216)
registerEntity("Ugrave",217)
registerEntity("Uacute",218)
registerEntity("Ucirc",219)
registerEntity("Uuml",220)
registerEntity("Yacute",221)
registerEntity("THORN",222)
registerEntity("szlig",223)
registerEntity("agrave",224)
registerEntity("aacute",225)
registerEntity("acirc",226)
registerEntity("atilde",227)
registerEntity("auml",228)
registerEntity("aring",229)
registerEntity("aelig",230)
registerEntity("ccedil",231)
registerEntity("egrave",232)
registerEntity("eacute",233)
registerEntity("ecirc",234)
registerEntity("euml",235)
registerEntity("igrave",236)
registerEntity("iacute",237)
registerEntity("icirc",238)
registerEntity("iuml",239)
registerEntity("eth",240)
registerEntity("ntilde",241)
registerEntity("ograve",242)
registerEntity("oacute",243)
registerEntity("ocirc",244)
registerEntity("otilde",245)
registerEntity("ouml",246)
registerEntity("divide",247)
registerEntity("oslash",248)
registerEntity("ugrave",249)
registerEntity("uacute",250)
registerEntity("ucirc",251)
registerEntity("uuml",252)
registerEntity("yacute",253)
registerEntity("thorn",254)
registerEntity("yuml",255)

###
###
###

class XSC:
	"""contains the options and functions for handling the XML files"""

	def __init__(self):
		self.filename = ""
		self.server = "localhost"
		self.retrieveremote = 1
		self.retrievelocal  = 1
		self.reprtab = ". "
		self.repransi = 1
		self.repransitab = "32"
		self.repransielementname = "35"
		self.repransitextattrs = ""
		self.repransicolorattrs = ""
		self.reprtree = 1
		self.parser = Parser()

	def parseString(self,filename,string):
		"""Parses a string and returns the resulting XSC"""
		self.filename = filename
		self.parser.reset()
		self.parser.feed(string)
		self.parser.close()
		return self.parser.root

	def parseFile(self,filename):
		"""Reads and parses a XML file and returns the resulting XSC"""
		self.filename = filename
		self.parser.reset()
		self.parser.feed(open(filename).read())
		self.parser.close()
		return self.parser.root

	def parseURL(self,url):
		"""Reads and parses a XML file from an URL and returns the resulting XSC"""
		self.filename = url
		self.parser.reset()
		self.parser.feed(urllib.urlopen(url).read())
		self.parser.close()
		urllib.urlcleanup()
		return self.parser.root

	def __repr__(self):
		return '<xsc filename="' + self.filename + '" server="' + self.server + '" retrieveremote=' + [ 'no' , 'yes' ][self.retrieveremote] + '" retrievelocal=' + [ 'no' , 'yes' ][self.retrievelocal] + '>'

	def is_remote(self,url):
		(scheme,server,path,parameters,query,fragment) = urlparse.urlparse(url)
		if scheme != "":
			return 1
		else:
			return 0

	def is_retrieve(self,url):
		remote = self.is_remote(url)
		if (self.retrieveremote and remote) or (self.retrievelocal and (not remote)):
			return 1
		else:
			return 0

def make():
	"""use XSC as a compiler script, i.e. read an input file from args[1] and writes it to args[2]"""
	infilename = sys.argv[1]
	outfilename = sys.argv[2]
	print "from:",infilename,"to:",outfilename
	e_in = xsc.parseFile(infilename)
	e_out = e_in.asHTML()
	open(outfilename,"wb").write(str(e_out))

xsc = XSC()

if __name__ == "__main__":
	make()

