#! /usr/bin/env python

""""""

__version__ = "$Revision$"
# $Source$

import os
import string
import types
import exceptions

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

class XSCError(Exception):
	"""base class for all XSC exceptions"""

	def __init__(self,lineno):
		self.lineno = lineno

	def __str__(self):
		s = self.__class__.__name__
		if self.lineno>0:
			s = s + " (line " + str(self.lineno) + ")"
		s = s + ": "

		return s

class XSCEmptyElementWithContentError(XSCError):
	"""exception that is raised, when an element has content, but it shouldn't (i.e. empty=1)"""

	def __init__(self,lineno,element):
		XSCError.__init__(self,lineno)
		self.element = element

	def __str__(self):
		return XSCError.__str__(self) + "the element " + _strelementname(self.element.name) + " is specified to be empty, but has content"

class XSCIllegalAttributeError(XSCError):
	"""exception that is raised, when an element has an illegal attribute (i.e. one that isn't contained in it's attr_handlers)"""

	def __init__(self,lineno,attrs,attr):
		XSCError.__init__(self,lineno)
		self.attrs = attrs
		self.attr = attr

	def __str__(self):
		attrs = self.attrs.attr_handlers.keys();
		attrs.sort()

		v = []

		for attr in attrs:
			v.append(_strattrname(attr))

		return XSCError.__str__(self) + "The attribute " + _strattrname(self.attr) + " is not allowed here. The only allowed attributes are: " + string.join(v,", ") + "."

class XSCAttributeNotFoundError(XSCError):
	"""exception that is raised, when an attribute is fetched that isn't there"""

	def __init__(self,lineno,attrs,attr):
		XSCError.__init__(self,lineno)
		self.attrs = attrs
		self.attr = attr

	def __str__(self):
		attrs = self.attrs.keys();

		s = XSCError.__str__(self) + "The attribute " + _strattrname(self.attr) + " could not be found. "

		if len(attrs):
			attrs.sort()
			v = []
			for attr in attrs:
				v.append(_strattrname(attr))
			s = s + "The only available attributes are: " + string.join(v,", ") + "."
		else:
			s = s + "There are no attributes available."

		return s

class XSCIllegalElementError(XSCError):
	"""exception that is raised, when an illegal element is encountered (i.e. one that isn't registered via RegisterElement"""

	def __init__(self,lineno,elementname):
		XSCError.__init__(self,lineno)
		self.elementname = elementname

	def __str__(self):
		elements = _element_handlers.keys();
		elements.sort()

		v = []

		for element in elements:
			v.append(_strelementname(element))
	
		return XSCError.__str__(self) + "The element " + _strelementname(self.elementname) + " is not allowed. The only allowed elements are: " + string.join(v,", ") + "."

class XSCIllegalElementNestingError(XSCError):
	"""exception that is raised, when an element has an illegal nesting (e.g. <a><b></a></b>)"""

	def __init__(self,lineno,expectedelementname,foundelementname):
		XSCError.__init__(self,lineno)
		self.expectedelementname = expectedelementname
		self.foundelementname = foundelementname

	def __str__(self):
		return XSCError.__str__(self) + "Illegal element nesting (" + _strelementname(self.expectedelementname) + " expected; " + _strelementname(self.foundelementname) + " found)"

class XSCImageSizeFormatError(XSCError):
	"""exception that is raised, when XSC can't format or evaluate image size attributes"""

	def __init__(self,lineno,element,attr):
		XSCError.__init__(self,lineno)
		self.element = element
		self.attr = attr

	def __str__(self):
		return XSCError.__str__(self) + "the value '" + str(self.element[self.attr]) + "' for the image size attribute " + _strattrname(self.attr) + " of the element " + _strelementname(self.element.name) + " can't be formatted or evaluated"

class XSCFileNotFoundError(XSCError):
	"""exception that is raised, when XSC can't open an image for getting image size"""

	def __init__(self,lineno,url):
		XSCError.__init__(self,lineno)
		self.url = url

	def __str__(self):
		return XSCError.__str__(self) + "the file " + self.url.repr() + " can't be opened"

class XSCIllegalObjectError(XSCError):
	"""exception that is raised, when XSC finds an illegal object found in its object tree"""

	def __init__(self,lineno,object):
		XSCError.__init__(self,lineno)
		self.object = object

	def __str__(self):
		return XSCError.__str__(self) + "an illegal object of type " + type(self.object).__name__ + " has been found in the XSC tree"

class XSCMalformedCharRefError(XSCError):
	"""exception that is raised, when a character reference is malformed (e.g. &#foo;)"""

	def __init__(self,lineno,name):
		XSCError.__init__(self,lineno)
		self.name = name

	def __str__(self):
		return XSCError.__str__(self) + "Malformed character reference: &#" + self.name + ";"

class XSCUnknownEntityError(XSCError):
	"""exception that is raised, when an unknown entity (i.e. one that wasn't registered via RegisterEntity) is encountered"""

	def __init__(self,lineno,name):
		XSCError.__init__(self,lineno)
		self.name = name

	def __str__(self):
		return XSCError.__str__(self) + "Unknown entitiy: &" + self.name + ";"

###
### helpers
###

def _stransi(codes,string):
	if xsc.repransi and codes!="" and string!="":
		return "\033[" + codes + "m" + string + "\033[0m"
	else:
		return string

def _strelementname(name):
	return _stransi(xsc.repransielementname,name)

def _strattrname(name):
	return _stransi(xsc.repransiattrname,name)

def AppendDict(*dicts):
	result = {}
	for dict in dicts:
		for key in dict.keys():
			result[key] = dict[key]
	return result

def ToNode(value):
	if type(value) == types.StringType:
		return XSCText(value)
	elif type(value) == types.NoneType:
		return None
	elif type(value) in [ types.IntType,types.LongType ] :
		return XSCCharRef(value)
	elif type(value) == types.FloatType :
		return XSCText(str(value))
	elif type(value) in [ types.ListType,types.TupleType ]:
		v = XSCFrag()
		for i in value:
			v.append(ToNode(i))
		return v
	elif type(value) == types.DictType:
		v = XSCAttrs()
		for i in value.keys():
			v[i] = ToNode(value[i])
		return v
	elif type(value) == types.InstanceType:
		if isinstance(value,XSCFrag):
			if len(value)==1:
				return ToNode(value[0]) # recursively try to simplify the tree
			else:
				return value
		else:
			return value
	raise XSCIllegalObjectError(xsc.parser.lineno,value) # none of the above, so we throw and exception

_element_handlers = {} # dictionary for mapping element names to classes

class XSCNode:
	"""base class for nodes in the document tree. Derived class must implement __str__()"""

	# line numbers where this node starts and ends in a file (will be hidden in derived classes, but is specified here, so that no special tests are required. In derived classes both variables will be set by the parser)
	startlineno = -1
	endlineno = -1
	name = "XSCNode" # will be changed for derived classes/elements in RegisterElement()

	def __add__(self,other):
		if other != None:
			return XSCFrag(self) + other
		else:
			return self

	def __radd__(self,other):
		if other != None:
			return XSCFrag(other) + self
		else:
			return self

	def __repr__(self):
		if xsc.reprtree == 1:
			return self.reprtree()
		else:
			return self.repr()

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
		return [[nest,self.lineno,elementno,self._strtag("?")]]

	def asHTML(self):
		return None

	def _strtag(self,content):
		return _stransi(xsc.repransibrackets,'<') + content + _stransi(xsc.repransibrackets,'>')
 
	def __str__(self):
		return ""

	def findElementsNamed(self,name):
		"""returns a fragment that contains all elements in the subtree of the node with the type name"""
		return XSCFrag()
 
	def withoutLinefeeds(self):
		"""returns this node, where all linefeeds that are in a text
		(or character reference) by themselves are removed, i.e. potentially
		needless whitespace is removed"""
		return None
		
class XSCText(XSCNode):
	"""text"""

	represcapes = { '\t' : '\\t' , '\033' : '\\e' , '\\' : '\\\\' }
	reprtreeescapes = { '\r' : '\\r' , '\n' : '\\n' , '\t' : '\\t' , '\033' : '\\e' , '\\' : '\\\\' }
	strescapes = { '<' : 'lt' , '>' : 'gt' , '&' : 'amp' , '"' : 'quot' }

	repransi = ""
	repransiquotes = "34"

	def __init__(self,content = ""):
		self.__content = content

	def asHTML(self):
		return XSCText(self.__content)

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
		# we could put ANSI escapes around every character or reference that we output, but this would result in strings that are way to long, especially if output over a serial cable, so we collect runs of characters with the same highlighting and put the ANSI escapes around those string. (of course, when we're not doing highlighting, this routine does way to much useless calculations)
		v = [] # collect all colored string here
		charref = -1 # the type of characters we're currently collecting (0==normal character, 1==character that have to be output as entities, -1==at the start)
		start = 0 # the position we our current run of characters for the same class started
		end = 0 # the current position we're testing
		while end<=len(self.__content): # one more than the length of the string
			do = 0 # we will have to do smething with the string collected so far ...
			if end == len(self.__content): # ... if we're at the end of the string
				do = 1
			else:
				c = self.__content[end] # or if the character we're at, is different from those we've collected so far
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
						ent = XSCParser.entitiesByNumber[ord(i)] # use names if a available, or number otherwise
						if len(ent):
							s = s + '&' + ent[0] + ';'
						else:
							s = s + '&#' + str(self.__content) + ';'
					v.append(_stransi(XSCCharRef.repransi,s))
					charref = 0 # switch to the other class
				else:
					s = self.__content[start:end]
					v.append(_stransi(XSCText.repransi,s))
					charref = 1 # switch to the other class
				start = end # the next string  we want to work on starts from here
			end = end + 1 # to the next character
				
		return string.join(v,"")

	def _dorepr(self):
		# constructs a string of this XSCText with syntaxhighlighting. Special characters will be output as CharRefs (with special highlighting)
		return self.__strtext(0)

	def _doreprtree(self,nest,elementno):
		s = _stransi(self.repransiquotes,'"') + _stransi(self.repransi,self.__strtext(1)) + _stransi(self.repransiquotes,'"')
		return [[nest,self.startlineno,elementno,s]]

	def withoutLinefeeds(self):
		for i in self.__content:
			if i != '\n' and i != '\r':
				return XSCText(self.__content)
		else:
			return None

class XSCCharRef(XSCNode):
	"""character reference (i.e &#42; or &#x42;)"""

	__notdirect = { ord("&") : "amp" , ord("<") : "lt" , ord(">") : "gt", ord('"') : "quot" , ord("'") : "apos" }
	__linefeeds = [ ord("\r") , ord("\n") ]

	repransi = "32"

	def __init__(self,content):
		self.__content = content

	def asHTML(self):
		return XSCCharRef(self.__content)

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
		return _stransi(self.repransi,s)
 
	def _dorepr(self):
		if len(XSCParser.entitiesByNumber[self.__content]):
			return self.__strcharref('#' + XSCParser.entitiesByNumber[self.__content][0] + ';')
		else:
			return self.__strcharref('&#' + str(self.__content) + ';')

	def _doreprtree(self,nest,elementno):
		s = self.__strcharref('&#' + str(self.__content) + ';') + ' (' + self.__strcharref('&#x' + hex(self.__content)[2:] + ';')
		for name in XSCParser.entitiesByNumber[self.__content]:
			s = s + ' ' + self.__strcharref('&' + name + ';')
		s = s + ')'
		if 0 <= self.__content <= 255:
			s = s + ' ' + XSCText(chr(self.__content))._doreprtree(0,0)[0][-1]
		return [[nest,self.startlineno,elementno,s]]

	def withoutLinefeeds(self):
		if self.__content in self.__linefeeds:
			return None
		else:
			return XSCCharRef(self.__content)

class XSCFrag(XSCNode):
	"""contains a list of XSCNodes"""

	def __init__(self,_content = []):
		if type(_content) == types.InstanceType:
			if isinstance(_content,XSCFrag):
				self._content = map(ToNode,_content._content)
			else:
				self._content = [ ToNode(_content) ]
		elif type(_content) in [ types.ListType , types.TupleType ]:
			self._content = map(ToNode,_content)
		else:
			self._content = [ ToNode(_content) ]

	def __add__(self,other):
		res = XSCFrag(self._content)
		if other is not None:
			newother = ToNode(other)
			if isinstance(newother,XSCFrag):
				res._content = res._content + newother._content
			else:
				res._content.append(newother)
		return res

	def __radd__(self,other):
		res = XSCFrag(self._content)
		if other is not None:
			newother = ToNode(other)
			if isinstance(newother,XSCFrag):
				res._content = newother._content + res._content
			else:
				res._content = [ newother ] + res._content
		return res

	def asHTML(self):
		e = XSCFrag()
		for child in self:
			e.append(child.asHTML())
		return e

	def _dorepr(self):
		v = []
		for child in self:
			v.append(child._dorepr())
		return string.join(v,"")

	def _doreprtree(self,nest,elementno):
		v = []
		v.append([nest,self.startlineno,elementno,self._strtag('XSCFrag')])
		i = 0
		for child in self:
			v = v + child._doreprtree(nest+1,elementno + [i])
			i = i + 1
		v.append([nest,self.endlineno,elementno,self._strtag('/XSCFrag')])
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
		return XSCFrag(self._content[index1:index2])

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

	def findElementsNamed(self,name):
		e = XSCFrag()
		for child in self:
			e = e + child.findElementsNamed(name)
		return e

	def withoutLinefeeds(self):
		e = XSCFrag()
		for child in self:
			e.append(child.withoutLinefeeds())
		return e

	def elements(self):
		e = XSCFrag()
		for child in self:
			if isinstance(child,XSCElement):
				e.append(child)

		return e

class XSCAttrs(XSCNode):
	"""contains a dictionary of XSCNodes which are wrapped into attribute nodes"""

	repransiquotes = "34"

	def __init__(self,attr_handlers,_content = {},**_restcontent):
		self.attr_handlers = attr_handlers
		self.__content = {}
		for attr in _content.keys():
			self[attr] = _content[attr]
		for attr in _restcontent.keys():
			self[attr] = _restcontent[attr]

	def __add__(self,other):
		"""adds attributes to the list"""
		res = XSCAttrs(self.__content)
		for attr in other.keys():
			res[attr] = other[attr]
		return res

	def __sub__(self,attrs):
		"""removes attributes from the list"""
		res = XSCAttrs(self.__content)
		for attr in attrs:
			del res[attr]
		return res

	def asHTML(self):
		return XSCAttrs(self.attr_handlers,self.__content)

	def __strattr(self,s):
		return _stransi(self.repransiquotes,'"') + s + _stransi(self.repransiquotes,'"')

	def _dorepr(self):
		v = []
		for attr in self.keys():
			v.append(" " + _strattrname(attr) + '=' + self.__strattr(self[attr]._dorepr()))
		return string.join(v,"")

	def _doreprtree(self,nest,elementno):
		v = [nest,self.startlineno,elementno,""]
		for attr in self.keys():
			line = self[attr]._dorepr()
			v[-1] = v[-1] + " " + _strattrname(attr) + '=' + self.__strattr(line)
		return [v]

	def __str__(self):
		v = []
		for attr in self.keys():
			v.append(' ' + attr + '="' + str(self[attr]) + '"')
		return string.join(v,"")

	def has_attr(self,index):
		return self.__content.has_key(index)

	def __getitem__(self,index):
		"""returns the attribute with the name index"""
		lowerindex = string.lower(index)
		if self.__content.has_key(lowerindex):
			return self.__content[lowerindex] # we're returning the packed attribute here, because otherwise there would be no possibility to get an expanded URL
		else:
			raise XSCAttributeNotFoundError(xsc.parser.lineno,self,index)

	def __setitem__(self,index,value):
		"""insert an attribute with the name index and the value value into the attribute dictionary"""
		# values are contructed via the attribute classes specified in the attr_handlers dictionary, which do the conversion
		lowerindex = string.lower(index)
		if self.attr_handlers.has_key(lowerindex):
			self.__content[lowerindex] = self.attr_handlers[lowerindex](value) # pack the attribute into an attribute object
		else:
			raise XSCIllegalAttributeError(xsc.parser.lineno,self,index)

	def __delitem__(self,index):
		"""removes the attribute with the name index (if there is one)"""
		lowerindex = string.lower(index)
		if self.__content.has_key(lowerindex):
			del self.__content[lowerindex]

	def keys(self):
		"""returns the keys of the dictionary, i.e. a list of the attribute names"""
		return self.__content.keys()

	def __len__(self):
		"""return the number of attributes"""
		return len(self.keys())

	def update(self,other):
		for attr in other.keys():
			self[attr] = other[attr]

	def withoutLinefeeds(self):
		return XSCAttrs(self.attr_handlers,self.__content)

class XSCComment(XSCNode):
	"""comments"""

	def __init__(self,content = ""):
		self.__content = content

	def asHTML(self):
		return XSCComment(self.__content)

	def _dorepr(self):
		return self._strtag("!--" + self.__content + "--")

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._strtag("!--" + self.__content + "--")]]

	def __str__(self):
		return "<!--" + self.__content + "-->"

	def withoutLinefeeds(self):
		return XSCComment(self.__content)

class XSCDocType(XSCNode):
	"""document type"""

	def __init__(self,content = ""):
		self.__content = content

	def asHTML(self):
		return XSCDocType(self.__content)

	def _dorepr(self):
		return self._strtag("!DOCTYPE " + self.__content)

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._strtag("!DOCTYPE " + self.__content)]]

	def __str__(self):
		return "<!DOCTYPE " + self.__content + ">"

	def withoutLinefeeds(self):
		return XSCDocType(self.__content)

class XSCProcInst(XSCNode):
	"""processing instructions"""

	repransiquestion = "34"
	repransitarget = "34"
	repransidata = "36"

	def __init__(self,target,content = ""):
		self.__target = target
		self.__content = content

	def asHTML(self):
		return XSCProcInst(self.__target,self.__content)

	def _dorepr(self):
		return self._strtag(_stransi(self.repransiquestion,"?") + _stransi(self.repransitarget,self.__target) + " " + _stransi(self.repransidata,self.__content) + _stransi(self.repransiquestion,"?"))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		return "<?" + self.__target + " " + self.__content + "?>"

	def withoutLinefeeds(self):
		return XSCProcInst(self.__target,self.__content)

class XSCElement(XSCNode):
	"""XML elements"""

	empty = 1 # 0 => element with content; 1 => stand alone element
 	attr_handlers = {}
	name = "XSCElement" # will be changed for derived classes/elements in RegisterElement()

	def __init__(self,_content = [],_attrs = {},**_restattrs):
		self.content = XSCFrag(_content)
		self.attrs = XSCAttrs(self.attr_handlers,{})

		self.attrs.update(_attrs)
		self.attrs.update(_restattrs)

	def append(self,item):
		if item is not None:
			if self.empty:
				raise XSCEmptyElementWithContentError(xsc.parser.lineno,self)
			else:
				self.content.append(item)

	def asHTML(self):
		return self.__class__(self.content.asHTML(),self.attrs.asHTML()) # "virtual" copy constructor

	def _dorepr(self):
		v = []
		if self.empty:
			v.append(self._strtag(_strelementname(self.name) + self.attrs._dorepr() + _strelementname("/")))
		else:
			v.append(self._strtag(_strelementname(self.name) + self.attrs._dorepr()))
			for child in self:
				v.append(child._dorepr())
			v.append(self._strtag(_strelementname("/" + self.name)))
		return string.join(v,"")

	def _doreprtree(self,nest,elementno):
		v = []
		if self.empty:
			v.append([nest,self.startlineno,elementno,self._strtag(_strelementname(self.name) + self.attrs._dorepr() + _strelementname("/"))])
		else:
			v.append([nest,self.startlineno,elementno,self._strtag(_strelementname(self.name) + self.attrs._dorepr())])
			i = 0
			for child in self:
				v = v + child._doreprtree(nest+1,elementno + [i])
				i = i + 1
			v.append([nest,self.endlineno,elementno,self._strtag(_strelementname("/" + self.name))])
		return v

	def __str__(self):
		"""returns this element as a string converted to HTML"""

		v = []
		v.append("<")
		v.append(self.name)
		v.append(str(self.attrs))
		s = str(self.content)
		if self.empty:
			if len(s):
				raise XSCEmptyElementWithContentError(xsc.parser.lineno,self)
			v.append(">")
		else:
			v.append(">")
			v.append(s)
			v.append("</")
			v.append(self.name) # name must be a string without any nasty characters
			v.append(">")

		return string.join(v,"")

	def __getitem__(self,index):
		"returns an attribute or one of the content nodes depending on whether a string (i.e. attribute name) or a number (i.e. content node index) is passed in"""
		if type(index)==types.StringType:
			return self.attrs[index]
		else:
			return self.content[index]

	def __setitem__(self,index,value):
		"sets an attribute or one of the content nodes depending on whether a string (i.e. attribute name) or a number (i.e. content node index) is passed in"""
		if type(index)==types.StringType:
			self.attrs[index] = value
		else:
			self.content[index] = value

	def __delitem__(self,index):
		"""removes an attribute or one of the content nodes depending on whether a string (i.e. attribute name) or a number (i.e. content node index) is passed in"""
		if type(index)==types.StringType:
			del self.attrs[index]
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
		return self.attrs.has_attr(attr)

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
						raise XSCImageSizeFormatError(xsc.parser.lineno,self,widthattr)
				else:
					self[widthattr] = str(size[0])
			if size[1] != -1: # the height was retrieved so we can use it
				if self.has_attr(heightattr):
					try:
						self[heightattr] = str(eval(str(self[heightattr]) % sizedict))
					except:
						raise XSCImageSizeFormatError(xsc.parser.lineno,self,heightattr)
				else:
					self[heightattr] = str(size[1])

	def findElementsNamed(self,name):
		e = XSCFrag()
		if self.name == string.lower(name):
				e.append(self)
		e = e + self.content.findElementsNamed(name)
		return e

	def withoutLinefeeds(self):
		return self.__class__(self.content.withoutLinefeeds(),self.attrs.withoutLinefeeds())

	def elements(self):
		return self.content.elements()

def RegisterElement(name,element):
	"""registers the element handler element to be used for elements with name name"""
	_element_handlers[name] = element
	element.name = name

class XSCAttr(XSCNode):
	"""
	Base classes of all attribute classes
	"""

	def __init__(self,_content):
		self._content = str(ToNode(_content))

	def __add__(self,other):
		if other != None:
			return self.__class__(self._content+str(ToNode(other)))
		else:
			return self

	def __radd__(self,other):
		if other != None:
			return self.__class__(str(ToNode(other))+self._content)
		else:
			return self

class XSCTextAttr(XSCAttr):
	"""
	Attribute class that is used for normal text attributes.
	"""

	def __init__(self,_content):
		XSCAttr.__init__(self,_content)

	def _dorepr(self):
		return _stransi(xsc.repransitextattrs,str(self._content))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		v = []
		for i in self._content:
			if i == '"':
				v.append("&quot;")
			elif ord(i)>=128:
				v.append('&#' + str(ord(i)) + ';')
			else:
				v.append(i)
		return string.join(v,"")

	def asHTML(self):
		return XSCTextAttr(self._content)

class XSCColorAttr(XSCAttr):
	"""
	Attribute class that is used for a color attributes.
	"""

	def __init__(self,_content):
		XSCAttr.__init__(self,_content)

	def _dorepr(self):
		return _stransi(xsc.repransitextattrs,str(self._content))

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		return self._content

	def asHTML(self):
		return XSCColorAttr(self._content)

class XSCURLAttr(XSCAttr):
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

	def __init__(self,_content):
		XSCAttr.__init__(self,_content)
		url = str(self._content)
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
		return _stransi(xsc.repransiurlattrs,url)

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._dorepr()]]

	def __str__(self):
		return self.forOutput()

	def asHTML(self):
		return XSCURLAttr(XSCText(self.forOutput()))

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
				raise XSCFileNotFoundError(xsc.parser.lineno,self)
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
				raise XSCFileNotFoundError(xsc.parser.lineno,self)
		return size

###
###
###

class XSCParser(xmllib.XMLParser):
	entitiesByNumber = [ ]

	for i in xrange(65536):
		entitiesByNumber.append([])

	entitiesByName = {}

	def reset(self):
		xmllib.XMLParser.reset(self)
		# our nodes do not have a parent link, therefore we have to store the active path through the tree in a stack (which we call nesting, because stack is already used by the base class
		# after we've finished parsing the XSCFrag that we put at the bottom of the stack will be our document root
		self.nesting = [ XSCFrag() ]
		self.lineno = -1
		self.root = None

	def close(self):
		self.root = self.nesting[0]
		xmllib.XMLParser.close(self)

	def __appendNode(self,node):
		node.startlineno = self.lineno
		self.nesting[-1].append(node) # add the new node to the content of the innermost element

	def handle_proc(self,target,data):
		self.__appendNode(XSCProcInst(target,data))

	def handle_charref(self,name):
		try:
			if name[0] == 'x':
				n = string.atoi(name[1:],16)
			else:
				n = string.atoi(name)
		except string.atoi_error:
			raise XSCMalformedCharRefError(xsc.parser.lineno,name)

		self.__appendNode(XSCCharRef(n))

	def handle_entityref(self,name):
		if self.entitiesByName.has_key(name):
			self.__appendNode(XSCCharRef(self.entitiesByName[name]))
		else:
			raise XSCUnknownEntityError(xsc.parser.lineno,name)

	def unknown_starttag(self,name,attrs):
  		lowername = string.lower(name)
		if _element_handlers.has_key(lowername):
			e = _element_handlers[lowername]([],attrs)
			e.startlineno = self.lineno
		else:
			raise XSCIllegalElementError(xsc.parser.lineno,lowername)
		self.__appendNode(e)
		self.nesting.append(e) # push new innermost element onto the stack

	def unknown_endtag(self,name):
		if string.lower(name) != self.nesting[-1].name:
			raise XSCIllegalElementNestingError(xsc.parser.lineno,self.nesting[-1].name,name)
		self.nesting[-1].endlineno = self.lineno
		self.nesting[-1:] = [] # pop the innermost element off the stack

	def handle_data(self,data):
		if data != "":
			self.__appendNode(XSCText(data))

	def handle_comment(self,data):
		self.__appendNode(XSCComment(data))

def RegisterEntity(name,number):
	if XSCParser.entitiesByNumber[number] == None:
		XSCParser.entitiesByNumber[number] = []
	XSCParser.entitiesByNumber[number].append(name)
	XSCParser.entitiesByName[name] = number

RegisterEntity("amp",38)
RegisterEntity("lt",60)
RegisterEntity("gt",62)
RegisterEntity("apos",39)
RegisterEntity("quot",34)
RegisterEntity("lf",10)
RegisterEntity("cr",13)
RegisterEntity("ht",9)
RegisterEntity("tab",9)
RegisterEntity("esc",27)
RegisterEntity("nbsp",160)
RegisterEntity("iexcl",161)
RegisterEntity("cent",162)
RegisterEntity("pound",163)
RegisterEntity("curren",164)
RegisterEntity("yen",165)
RegisterEntity("brvbar",166)
RegisterEntity("sect",167)
RegisterEntity("die",168)
RegisterEntity("copy",169)
RegisterEntity("ordf",170)
RegisterEntity("laquo",171)
RegisterEntity("not",172)
RegisterEntity("shy",173)
RegisterEntity("reg",174)
RegisterEntity("macr",175)
RegisterEntity("deg",176)
RegisterEntity("plusmn",177)
RegisterEntity("sup2",178)
RegisterEntity("sup3",179)
RegisterEntity("acute",180)
RegisterEntity("micro",181)
RegisterEntity("para",182)
RegisterEntity("middot",183)
RegisterEntity("cedil",184)
RegisterEntity("sup1",185)
RegisterEntity("ordm",186)
RegisterEntity("raquo",187)
RegisterEntity("frac14",188)
RegisterEntity("frac12",189)
RegisterEntity("frac34",190)
RegisterEntity("iquest",191)
RegisterEntity("Agrave",192)
RegisterEntity("Aacute",193)
RegisterEntity("Acirc",194)
RegisterEntity("Atilde",195)
RegisterEntity("Auml",196)
RegisterEntity("Aring",197)
RegisterEntity("AElig",198)
RegisterEntity("Ccedil",199)
RegisterEntity("Egrave",200)
RegisterEntity("Eacute",201)
RegisterEntity("Ecirc",202)
RegisterEntity("Euml",203)
RegisterEntity("Igrave",204)
RegisterEntity("Iacute",205)
RegisterEntity("Icirc",206)
RegisterEntity("Iuml",207)
RegisterEntity("ETH",208)
RegisterEntity("Ntilde",209)
RegisterEntity("Ograve",210)
RegisterEntity("Oacute",211)
RegisterEntity("Ocirc",212)
RegisterEntity("Otilde",213)
RegisterEntity("Ouml",214)
RegisterEntity("times",215)
RegisterEntity("Oslash",216)
RegisterEntity("Ugrave",217)
RegisterEntity("Uacute",218)
RegisterEntity("Ucirc",219)
RegisterEntity("Uuml",220)
RegisterEntity("Yacute",221)
RegisterEntity("THORN",222)
RegisterEntity("szlig",223)
RegisterEntity("agrave",224)
RegisterEntity("aacute",225)
RegisterEntity("acirc",226)
RegisterEntity("atilde",227)
RegisterEntity("auml",228)
RegisterEntity("aring",229)
RegisterEntity("aelig",230)
RegisterEntity("ccedil",231)
RegisterEntity("egrave",232)
RegisterEntity("eacute",233)
RegisterEntity("ecirc",234)
RegisterEntity("euml",235)
RegisterEntity("igrave",236)
RegisterEntity("iacute",237)
RegisterEntity("icirc",238)
RegisterEntity("iuml",239)
RegisterEntity("eth",240)
RegisterEntity("ntilde",241)
RegisterEntity("ograve",242)
RegisterEntity("oacute",243)
RegisterEntity("ocirc",244)
RegisterEntity("otilde",245)
RegisterEntity("ouml",246)
RegisterEntity("divide",247)
RegisterEntity("oslash",248)
RegisterEntity("ugrave",249)
RegisterEntity("uacute",250)
RegisterEntity("ucirc",251)
RegisterEntity("uuml",252)
RegisterEntity("yacute",253)
RegisterEntity("thorn",254)
RegisterEntity("yuml",255)

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
		self.repransibrackets = "34;1"
		self.repransielementname = "35"
		self.repransiattrname = "33"
		self.repransiurlattrs = "31"
		self.repransitextattrs = ""
		self.repransicolorattrs = ""
		self.reprtree = 1
		self.parser = XSCParser()

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

def make(args):
	"""class XSC as a compiles, i.e. read an input file from args[1] and writes it to args[2]"""
	print "from:",args[0],"to:",args[1]
	e_in = xsc.parseFile(args[1])
	e_out = e_in.asHTML()
	open(args[2],"wb").write(str(e_out))

xsc = XSC()

if __name__ == "__main__":
	import sys
	make(sys.argv)

