#! /usr/bin/python

import os
import string
import types

# for file size checking
import stat

# for image size checking
import Image

# for parsing XML files
from xmllib import *

###
### exceptions
###

class EHSCException:
	"base class for all HSC exceptions"

	def __str__(self):
		return "Something wonderful has happened"

class EHSCEmptyElementWithContent(EHSCException):
	"this element is specified to be empty, but has content"

	def __init__(self,element):
		self.element = element

	def __str__(self):
		return "the element '" + self.element.name + "' is specified to be empty, but has content"

class EHSCIllegalAttribute(EHSCException):
	"this element has an attribute that is not allowed"

	def __init__(self,element,attr):
		self.element = element
		self.attr = attr

	def __str__(self):
		return "the element '" + self.element.name + "' has an attribute ('" + self.attr + "') that is not allowed here. The only allowed attributes are: " + str(self.element.attr_handlers.keys())

class EHSCImageSizeFormat(EHSCException):
	"Can't format or evaluate image size attribute"

	def __init__(self,element,attr):
		self.element = element
		self.attr = attr

	def __str__(self):
		return "the value '" + html(self.element[self.attr]) + "' for the image size attribute '" + self.attr + "' of the element '" + self.element.name + "' can't be formatted or evaluated"

class EHSCFileNotFound(EHSCException):
	"Can't open image for getting image size"

	def __init__(self,url):
		self.url = url

	def __str__(self):
		return "the image file '" + self.url + "' can't be opened"

###
###
###

def FileSize(url):
	"returns the size of a file in bytes"

	return os.stat(url)[stat.ST_SIZE]

def ImageSize(url):
	"returns the size of an image as a tuple"

	try:
		img = Image.open(url)
		return img.size
	except:
		raise EHSCFileNotFound(url)

def AppendDict(*dicts):
	result = {}
	for dict in dicts:
		for key in dict.keys():
			result[key] = dict[key]
	return result

def ToNode(value):
	if type(value) == types.StringType:
		return XSCText(value)
	elif type(value) in [ types.NoneType,types.IntType,types.LongType,types.FloatType ] :
		return XSCText(str(value))
	elif type(value) in [ types.ListType,types.TupleType ]:
		v = XSCDocumentFragment()
		for i in value:
			v.append(ToNode(i))
		return v
	elif type(value) == types.DictType:
		v = XSCAttrList()
		for i in value.keys():
			v[i] = ToNode(value[i])
		return v
	else:
		return value

element_handlers = {} # dictionary for mapping element names to classes

class XSCNode:
	"base class for nodes in the document tree. Derived class must implement html()"

	def __add__(self,other):
		return XSCFrag(self) + other

	def __radd__(self,other):
		return XSCFrag(other) + self

	def __repr__(self):
		return "<?>"

class XSCText(XSCNode):
	"text"

	def __init__(self,content = ""):
		self.content = content

	def __str__(self):
		v = []
		for i in self.content:
			if i == '<':
				v.append('&lt;')
			elif i == '>':
				v.append('&gt;')
			elif i == '&':
				v.append('&amp;')
			elif i == '"':
				v.append('&quot')
			elif ord(i)>=128:
				v.append('&#' + str(ord(i)) + ';')
			else:
				v.append(i)
		return string.joinfields(v,"")

	def __repr__(self):
		return self.content

class XSCFrag(XSCNode):
	"contains a list of XSCNodes"

	def __init__(self,content = []):
		if type(content) == types.InstanceType:
			if content.__class__ == XSCFrag:
				self.content = map(ToNode,content.content)
		elif type(content) in [ types.ListType , types.TupleType ]:
			self.content = map(ToNode,content)
		else:
			self.content = [ ToNode(content) ]

	def __add__(self,other):
		res = XSCFrag(self.content)
		res.append(other)
		return res

	def __radd__(self,other):
		res = XSCFrag(self.content)
		res.preppend(other)

	def __str__(self):
		return string.joinfields(map(str,self.content),"")

	def __repr__(self):
		return string.joinfields(map(repr,self.content),"")

	def append(self,other):
		self.content.append(ToNode(other))

	def preppend(self,other):
		self.content[0:0] = ToNode(other)

class XSCComment(XSCNode):
	"comments"

	def __init__(self,content = ""):
		self.content = content

	def __repr__(self):
		return "<!--" + self.content + "-->"

class XSCDocType(XSCNode):
	"document type"

	def __init__(self,content = ""):
		self.content = content

	def __repr__(self):
		return "<!DOCTYPE " + self.content + ">"

class XSCStringAttr(XSCNode):
	"string attribute"

	def __init__(self,content):
		self.content = content

	def __repr__(self):
		return repr(self.content)

	def __str__(self):
		return str(self.content)

class XSCURLAttr(XSCNode):
	"url attribute"

	def __init__(self,content):
		self.content = content

	def __repr__(self):
		url = repr(self.content)
		if url[0] == ":":
			url = url[1:]
		return url

	def __str__(self):
		url = str(self.content) 
		if url[0] == ":":
			# split both path
			source = string.splitfields(xsc_filename,os.sep)
			dest = string.splitfields(url[1:],os.sep)
			# throw away identical directories in both path
			while len(source)>1 and len(dest)>1 and source[0]==dest[0]:
				del source[0]
				del dest[0]
			url = string.joinfields(([os.pardir]*(len(source)-1)) + dest,os.sep)
		return url

lement_handlers = {} # dictionary that links element names to element classes

class XSCElement(XSCNode):
	"XML elements"

	close = 0
	attr_handlers = {}

	def __init__(self,content = [],attrs = {},**restattrs):
		self.content = XSCFrag(content)
		self.attrs = {}

		# construct the attribute dictionary, keys are the attribute names, values are the various nodes for the differnet attribute type; checks that only attributes that are allow are used (raises an exception otherwise)"
		for attr in attrs.keys():
			lowerattr = string.lower(attr)
			if self.attr_handlers.has_key(lowerattr):
				self.attrs[lowerattr] = self.attr_handlers[lowerattr](attrs[attr])
			else:
				raise EHSCIllegalAttribute(self,attr)
		for attr in restattrs.keys():
			lowerattr = string.lower(attr)
			if self.attr_handlers.has_key(lowerattr):
				self.attrs[lowerattr] = self.attr_handlers[lowerattr](restattrs[attr])
			else:
				raise EHSCIllegalAttribute(self,attr)

	def append(self,item):
		self.content.append(item)

	def __repr__(self):
		"returns this element as a string"
		v = []
		v.append("<")
		v.append(self.name)
		if len(self.attrs.keys()):
			v.append(" ")
			v.append(repr(self.attrs))
		s = repr(self.content)
		if self.close == 1:
			v.append(">")
			v.append(s)
			v.append("</")
			v.append(self.name) # name must be a string without any nasty characters
			v.append(">")
		else:
			if len(s):
				raise EHSCEmptyElementWithContent(self)
			v.append(">")

		return string.joinfields(v,"")

	def __str__(self):
		"returns this element as a string converted to HTML"

		v = []
		v.append("<")
		v.append(self.name)
		if len(self.attrs.keys()):
			v.append(" ")
			v.append(str(self.attrs))
		s = str(self.content)
		if self.close == 1:
			v.append(">")
			v.append(s)
			v.append("</")
			v.append(self.name) # name must be a string without any nasty characters
			v.append(">")
		else:
			if len(s):
				raise EHSCEmptyElementWithContent(self)
			v.append(">")

		return string.joinfields(v,"")

	def __getitem__(self,index):
		return self.attrs[index]

	def __setitem__(self,index,value):
		self.attrs[index] = value

	def __delitem__(self,index):
		if self.has_attr(index):
			del self.attrs[index]

	def has_attr(self,attr):
		return self.attrs.has_key(attr)

	def AddImageSizeAttributes(self,imgattr,widthattr = "width",heightattr = "height"):
		"add width and height attributes to the element for the image that can be found in the attributes imgattr. if the attribute is already there it is taken as a formating template with the size passed in as a dictionary with the keys 'width' and 'height', i.e. you could make your image twice as wide with width='%(width)d*2'"

		if self.has_attr(imgattr):
			url = str(self[imgattr])
			size = ImageSize(url)
			sizedict = { "width": size[0], "height": size[1] }
			if self.has_attr(widthattr):
				try:
					self[widthattr] = eval(str(self[widthattr]) % sizedict)
				except:
					raise EHSCImageSizeFormat(self,widthattr)
			else:
				self[widthattr] = size[0]
			if self.has_attr(heightattr):
				try:
					self[heightattr] = eval(str(self[heightattr]) % sizedict)
				except:
					raise EHSCImageSizeFormat(self,heightattr)
			else:
				self[heightattr] = size[1]


def RegisterElement(name,element):
	element_handlers[name] = element
	element.name = name

###
###
###

xsc_filename = ""

class XSC(XMLParser):
	"Reads a XML file and constructs an XSC tree from it."

	def __init__(self,filename,parse = 1):
		global xsc_filename
		XMLParser.__init__(self)
		xsc_filename = filename
		if parse == 1:
			self.nesting = [ [] ] # our nodes do not have a parent link, therefore we have to store the active path through the tree in a stack (which we call nesting, because stack is already used by the base class
			self.feed(open(filename).read())
			self.close()
			self.root = self.nesting[0]
		else:
			self.root = None

	def processingInstruction (self,target, remainder):
		pass

	def unknown_starttag(self,name,attrs = {}):
		e = element_handlers[string.lower(name)]([],attrs)
		e.xsc = self
		self.nesting[-1].append(e) # add the new element to the content of the innermost element (or to the array)
		self.nesting.append(e) # push new innermost element onto the stack
		
	def unknown_endtag(self,name):
		self.nesting[-1:] = [] # pop the innermost element off the stack

	def handle_data(self,data):
		self.nesting[-1].append(data) # add the new string to the content of the innermost element

	def handle_comment(self,comment):
		self.nesting[-1].append(XSCComment(comment))

	def __repr__(self):
		return repr(self.root)

	def __str__(self):
		return str(self.root)

