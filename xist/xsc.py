#! /usr/bin/env python

import os
import string
import types

# for file size checking
import stat

# for image size checking
import Image

# for parsing XML files
import xmllib

# for parsing URLs
import urlparse

# for reading remote files
import urllib

###
### exceptions
###

class XSCError:
	"base class for all XSC exceptions"

	def __init__(self,lineno):
		self.lineno = lineno

	def __str__(self):
		if self.lineno>0:
			return "XSC: error (line " + str(self.lineno) + "): "
		else:
			return "XSC: error: "

class XSCEmptyElementWithContentError(XSCError):
	"exception that is raised, when an element has content, but it shouldn't (i.e. close==0)"

	def __init__(self,lineno,element):
		XSCError.__init__(self,lineno)
		self.element = element

	def __str__(self):
		return XSCError.__str__(self) + "the element '" + self.element.name + "' is specified to be empty, but has content"

class XSCIllegalAttributeError(XSCError):
	"exception that is raised, when an element has an illegal attribute (i.e. one that isn't contained in it's attr_handlers)"

	def __init__(self,lineno,attrs,attr):
		XSCError.__init__(self,lineno)
		self.attrs = attrs
		self.attr = attr

	def __str__(self):
		return XSCError.__str__(self) + "The attribute '" + self.attr + "' is not allowed here. The only allowed attributes are: " + str(self.attrs.attr_handlers.keys())

class XSCIllegalElementError(XSCError):
	"exception that is raised, when an illegal element is encountered (i.e. one that isn't registered via RegisterElement"

	def __init__(self,lineno,elementname):
		XSCError.__init__(self,lineno)
		self.elementname = elementname

	def __str__(self):
		return XSCError.__str__(self) + "The element '" + self.elementname + "' is not allowed. The only allowed elements are: " + str(element_handlers.keys())

class XSCImageSizeFormatError(XSCError):
	"exception that is raised, when XSC can't format or evaluate image size attributes"

	def __init__(self,lineno,element,attr):
		XSCError.__init__(self,lineno)
		self.element = element
		self.attr = attr

	def __str__(self):
		return XSCError.__str__(self) + "the value '" + str(self.element[self.attr]) + "' for the image size attribute '" + self.attr + "' of the element '" + self.element.name + "' can't be formatted or evaluated"

class XSCFileNotFoundError(XSCError):
	"exception that is raised, when XSC can't open an image for getting image size"

	def __init__(self,lineno,url):
		XSC.__init__(self,lineno)
		self.url = url

	def __str__(self):
		return XSCError.__str__(self) + "the image file '" + self.url + "' can't be opened"

class XSCIllegalObjectError(XSCError):
	"exception that is raised, when XSC finds an illegal object found in its obejct tree"

	def __init__(self,lineno,object):
		XSCError.__init__(self,lineno)
		self.object = object

	def __str__(self):
		return XSCError.__str__(self) + "an illegal object of type " + type(self.object).__name__ + " has been found in the XSC tree"

###
###
###

def FileSize(url):
	"returns the size of a file in bytes"

	size = -1
	if xsc.retrieveremote or (not xsc.is_remote(url)):
		filename,headers = urllib.urlretrieve(url)
		size = os.stat(filename)[stat.ST_SIZE]
		urllib.urlcleanup()
	return size

def ImageSize(url):
	"returns the size of an image as a tuple"

	size = (-1,-1)
	if xsc.retrieveremote or (not xsc.is_remote(url)):
		filename,headers = urllib.urlretrieve(url)
		if headers.has_key("content-type") and headers["content-type"][:6] == "image/":
			img = Image.open(filename)
			size = img.size
		del img
		urllib.urlcleanup()
	return size

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
		if value.__class__ == XSCFrag:
			if len(value.content)==1:
				return ToNode(value.content[0]) # recursively try to simplify the tree
			else:
				return value
		else:
			return value
	raise XSCIllegalObjectError(xsc.parser.lineno,value) # none of the above, so we throw and exception

element_handlers = {} # dictionary for mapping element names to classes

class XSCNode:
	"base class for nodes in the document tree. Derived class must implement __str__()"

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
			else:
				self.content = [ ToNode(content) ]
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
		self.content = [ ToNode(other) ] + self.content[:]

class XSCAttrs(XSCNode):
	"contains a dictionary of XSCNodes which are wrapped into attribute nodes"

	def __init__(self,attr_handlers,content = {},**restcontent):
		self.attr_handlers = attr_handlers
		self.content = {}
		for attr in content.keys():
			self[attr] = content[attr]
		for attr in restcontent.keys():
			self[attr] = restcontent[attr]

	def __add__(self,other):
		res = XSCAttrs(self.content)
		for attr in other.keys():
			res[attr] = other[attr]
		return res

	def __sub__(self,attrs):
		"removes attributes from the list"
		res = XSCAttrs(self.content)
		for attr in attrs:
			del res[attr]
		return res

	def __str__(self):
		v = []
		for attr in self.content.keys():
			v.append(attr + '="' + str(self.content[attr]) + '"')
		return string.joinfields(v," ")

	def __repr__(self):
		v = []
		for attr in self.content.keys():
			v.append(attr + '="' + repr(self.content[attr]) + '"')
		return string.joinfields(v," ")

	def has_attr(self,index):
		return self.content.has_key(index)

	def __getitem__(self,index):
		return self.content[index] # we're returning the packed attribute here, because otherwise there would be no possibility to get an expanded URL

	def __setitem__(self,index,value):
		"insert a value into the attribute dictionary"
		# values are converted to Nodes first and then wrapped into the attribute nodes as specified via the attr_handlers dictionary
		lowerindex = string.lower(index)
		if self.attr_handlers.has_key(lowerindex):
			self.content[lowerindex] = self.attr_handlers[lowerindex](ToNode(value)) # convert the attribute to a node and pack it into an attribute object
		else:
			raise XSCIllegalAttributeError(xsc.parser.lineno,self,index)

	def __delitem__(self,index):
		"removes a dictionary entry"
		if self.has_attr(index):
			del self.content[index]

	def keys(self):
		"returns the keys of the dictionary, i.e. a list of the attribute names"
		return self.content.keys()

	def __len__(self):
		"return the number of attributes"
		return len(self.keys())

	def update(self,other):
		for attr in other.keys():
			self[attr] = other[attr]

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

class XSCElement(XSCNode):
	"XML elements"

	close = 0 # 0 => stand alone element, 1 => element with content
	attr_handlers = {}

	def __init__(self,content = [],attrs = {},**restattrs):
		self.content = XSCFrag(content)
		self.attrs = XSCAttrs(self.attr_handlers,{})

		self.attrs.update(attrs)
		self.attrs.update(restattrs)

	def append(self,item):
		self.content.append(item)

	def __repr__(self):
		"returns this element as a string"
		v = []
		v.append("<")
		v.append(self.name)
		if len(self.attrs):
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
				raise XSCEmptyElementWithContentError(xsc.parser.lineno,self)
			v.append(">")

		return string.joinfields(v,"")

	def __str__(self):
		"returns this element as a string converted to HTML"

		v = []
		v.append("<")
		v.append(self.name)
		if len(self.attrs):
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
				raise XSCEmptyElementWithContentError(xsc.parser.lineno,self)
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
		return self.attrs.has_attr(attr)

	def AddImageSizeAttributes(self,imgattr,widthattr = "width",heightattr = "height"):
		"add width and height attributes to the element for the image that can be found in the attributes imgattr. if the attribute is already there it is taken as a formating template with the size passed in as a dictionary with the keys 'width' and 'height', i.e. you could make your image twice as wide with width='%(width)d*2'"

		if self.has_attr(imgattr):
			url = repr(self[imgattr])
			size = ImageSize(url)
			sizedict = { "width": size[0], "height": size[1] }
			if size[0] != -1: # the width was retrieved so we can use it
				if self.has_attr(widthattr):
					try:
						self[widthattr] = eval(str(self[widthattr]) % sizedict)
					except:
						raise XSCImageSizeFormatError(xsc.parser.lineno,self,widthattr)
				else:
					self[widthattr] = size[0]
			if size[1] != -1: # the height was retrieved so we can use it
				if self.has_attr(heightattr):
					try:
						self[heightattr] = eval(str(self[heightattr]) % sizedict)
					except:
						raise XSCImageSizeFormatError(xsc.parser.lineno,self,heightattr)
				else:
					self[heightattr] = size[1]

def RegisterElement(name,element):
	element_handlers[name] = element
	element.name = name

class XSCurl(XSCElement):
	"URLS (may be used as an element or an attribute)"

	def __init__(self,content = [],attrs = {},**restattrs):
		if type(content) == types.InstanceType and content.__class__ == XSCurl:
			self.content = content.content
		else:
			self.content = XSCFrag(content)

	def __repr__(self):
		(scheme,server,path,parameters,query,fragment) = urlparse.urlparse(repr(self.content))
		if scheme == "" and server == "":
			if len(path) and path[0] == "/": # this is a server relative URL, use the server specified in the options (usually localhost)
				scheme = "http"
				server = xsc.server
			else:
				if len(path) and path[0] == ":": # project relative, i.e. relative to the current directory
					path = path[1:]
				# now we have an URL that is relative to the current directory, replace URL syntax with the path syntax on our system (won't do anything under UNIX, replaces / with  \ under Windows)
				pathsplit = string.splitfields(path,"/")
				for i in range(len(pathsplit)):
					if pathsplit[i] == "..":
						pathsplit[i] = os.pardir
				path = string.joinfields(pathsplit,os.sep)
		return urlparse.urlunparse((scheme,server,path,parameters,query,fragment))

	def __str__(self):
		url = str(self.content)
		if url[0] == ":":
			# split both path
			source = string.splitfields(xsc.filename,"/")
			dest = string.splitfields(url[1:],os.sep)
			# throw away identical directories in both path
			while len(source)>1 and len(dest)>1 and source[0]==dest[0]:
				del source[0]
				del dest[0]
			url = string.joinfields(([".."]*(len(source)-1)) + dest,"/")
		return url
RegisterElement("url",XSCurl)

###
###
###

class XSCParser(xmllib.XMLParser):
	"Reads a XML file and constructs an XSC tree from it."

	def __init__(self):
		xmllib.XMLParser.__init__(self)
		self.reset()

	def reset(self):
		xmllib.XMLParser.reset(self)
		self.nesting = [ XSCFrag() ] # our nodes do not have a parent link, therefore we have to store the active path through the tree in a stack (which we call nesting, because stack is already used by the base class
		self.root = self.nesting[0]
		self.lineno = -1

	def processingInstruction(self,target,remainder):
		pass

	def unknown_starttag(self,name,attrs = {}):
		lowername = string.lower(name)
		if element_handlers.has_key(lowername):
			e = element_handlers[lowername]([],attrs)
		else:
			raise XSCIllegalElementError(xsc.parser.lineno,lowername)
		self.nesting[-1].append(e) # add the new element to the content of the innermost element (or to the array)
		self.nesting.append(e) # push new innermost element onto the stack

	def unknown_endtag(self,name):
		self.nesting[-1:] = [] # pop the innermost element off the stack

	def handle_data(self,data):
		self.nesting[-1].append(data) # add the new string to the content of the innermost element

	def handle_comment(self,comment):
		self.nesting[-1].append(XSCComment(comment))

###
###
###

class XSC:
	# protocol string that will be recognised as being remote files, where no path translation takes place
	protocols = [ "http" , "ftp" ]

	def __init__(self):
		self.filename = ""
		self.server = "localhost"
		self.retrieveremote = 1
		self.parser = XSCParser()

	def parsestring(self,filename,string):
		"Parses a string and returns the resulting XSC"
		self.filename = filename
		self.parser.reset()
		self.parser.feed(string)
		self.parser.close()
		return self.parser.root

	def parsefile(self,filename):
		"Reads and parses a XML file and returns the resulting XSC"
		self.filename = filename
		self.parser.reset()
		self.parser.feed(open(filename).read())
		self.parser.close()
		return self.parser.root

	def parseurl(self,url):
		"Reads and parses a XML file from an URL and returns the resulting XSC"
		self.filename = url
		self.parser.reset()
		self.parser.feed(urllib.urlopen(url).read())
		self.parser.close()
		urllib.urlcleanup()
		return self.parser.root

	def __repr__(self):
		return '<xsc filename="' + self.filename + '" server="' + self.server + '" retrieveremote=' + [ 'no' , 'yes' ][self.retrieveremote] + '>'

	def is_remote(self,url):
		for protocol in self.protocols:
			test = protocol + "://"
			if test == url[:len(test)]: # this is a complete URL so we don't have to do any translation
				return 1
		else:
			return 0

xsc = XSC()


