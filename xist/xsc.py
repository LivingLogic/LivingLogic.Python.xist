#! /usr/bin/env python

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
		if self.lineno>0:
			return "XSC: error (line " + str(self.lineno) + "): " + str(xsc.handler.nesting)
		else:
			return "XSC: error: "

class XSCEmptyElementWithContentError(XSCError):
	"""exception that is raised, when an element has content, but it shouldn't (i.e. close==0)"""

	def __init__(self,lineno,element):
		XSCError.__init__(self,lineno)
		self.element = element

	def __str__(self):
		return XSCError.__str__(self) + "the element '" + self.element.name + "' is specified to be empty, but has content"

class XSCIllegalAttributeError(XSCError):
	"""exception that is raised, when an element has an illegal attribute (i.e. one that isn't contained in it's attr_handlers)"""

	def __init__(self,lineno,attrs,attr):
		XSCError.__init__(self,lineno)
		self.attrs = attrs
		self.attr = attr

	def __str__(self):
		attrs = self.attrs.attr_handlers.keys();
		attrs.sort()
		return XSCError.__str__(self) + "The attribute '" + self.attr + "' is not allowed here. The only allowed attributes are: " + str(attrs)

class XSCIllegalElementError(XSCError):
	"""exception that is raised, when an illegal element is encountered (i.e. one that isn't registered via RegisterElement"""

	def __init__(self,lineno,elementname):
		XSCError.__init__(self,lineno)
		self.elementname = elementname

	def __str__(self):
		elements = element_handlers.keys();
		elements.sort()
		return XSCError.__str__(self) + "The element '" + self.elementname + "' is not allowed. The only allowed elements are: " + elements

class XSCImageSizeFormatError(XSCError):
	"""exception that is raised, when XSC can't format or evaluate image size attributes"""

	def __init__(self,lineno,element,attr):
		XSCError.__init__(self,lineno)
		self.element = element
		self.attr = attr

	def __str__(self):
		return XSCError.__str__(self) + "the value '" + str(self.element[self.attr]) + "' for the image size attribute '" + self.attr + "' of the element '" + self.element.name + "' can't be formatted or evaluated"

class XSCFileNotFoundError(XSCError):
	"""exception that is raised, when XSC can't open an image for getting image size"""

	def __init__(self,lineno,url):
		XSCError.__init__(self,lineno)
		self.url = url

	def __str__(self):
		return XSCError.__str__(self) + "the file '" + self.url + "' can't be opened"

class XSCIllegalObjectError(XSCError):
	"""exception that is raised, when XSC finds an illegal object found in its object tree"""

	def __init__(self,lineno,object):
		XSCError.__init__(self,lineno)
		self.object = object

	def __str__(self):
		return XSCError.__str__(self) + "an illegal object of type " + type(self.object).__name__ + " has been found in the XSC tree"

###
###
###

def URLForInput(url):
	(scheme,server,path,parameters,query,fragment) = urlparse.urlparse(url)
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

def URLForOutput(url):
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

def FileSize(url):
	"""returns the size of a file in bytes or -1 if the file shouldn't be read"""

	size = -1
	if xsc.is_retrieve(url):
		try:
			filename,headers = urllib.urlretrieve(url)
			size = os.stat(filename)[stat.ST_SIZE]
			urllib.urlcleanup()
		except IOError:
			urllib.urlcleanup()
			raise XSCFileNotFoundError(xsc.handler.lineno,url)
	return size

def ImageSize(url):
	"""returns the size of an image as a tuple or (-1,-1) if the image shouldn't be read"""

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
			raise XSCFileNotFoundError(xsc.handler.lineno,url)
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
	elif type(value) == types.NoneType:
		return XSCText("")
	elif type(value) in [ types.IntType,types.LongType,types.FloatType ] :
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
	raise XSCIllegalObjectError(xsc.handler.lineno,value) # none of the above, so we throw and exception

element_handlers = {} # dictionary for mapping element names to classes

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
		return self.repr(xsc.reprtree)

	def repr(self,tree,nest = 0):
		if tree!=0:
			v = []
			lines = self._doreprtree(nest,[])
			lenlineno = 0
			lenelementno = 0
			for line in lines:
				if line[1] != -1: # convert line number to a string
					line[1] = str(line[1])
				else:
					line[1] = "?"
				line[2] = string.joinfields(map(str,line[2]),".") # convert element number to a string
				line[3] = self._stransi(xsc.repransitab,xsc.reprtab*line[0]) + line[3] # add indentation
				lenlineno = max(lenlineno,len(line[1]))
				lenelementno = max(lenelementno,len(line[2]))

			for line in lines:
				v.append("%*s %-*s %s\n" % (lenlineno,line[1],lenelementno,line[2],line[3]))
			return string.joinfields(v,"")
		else:
			return self._dorepr()

	def _dorepr(self):
		# returns a string representation of the node
		return self._strtag("?")
	
	def _doreprtree(self,nest,elementno):
		# returns and array containing arrays consisting of the (nestinglevel,linenumber,elementnumber,string representation) of the nodes
		return [[nest,self.lineno,elementno,self._strtag("?")]]

	def asHTML(self):
		return ToNode(self._doAsHTML())

	def _doAsHTML(self):
		return None

	def _stransi(self,codes,string):
		if xsc.repransi and codes!="":
			return "\033[" + codes + "m" + string + "\033[0m"
		else:
			return (string)

	def _strelementname(self,name):
		return self._stransi(xsc.repransielementname,name)

	def _strattrname(self,name):
		return self._stransi(xsc.repransiattrname,name)

	def _strtext(self,text):
		return self._stransi(xsc.repransitext,text)

	def _strtag(self,content):
		return self._stransi(xsc.repransibrackets,'<') + content + self._stransi(xsc.repransibrackets,'>')
 
	def _strtextquotes(self,content):
		return self._stransi(xsc.repransiquotes,'"') + content + self._stransi(xsc.repransiquotes,'"')
 
	def _strattrquotes(self,content):
		return self._stransi(xsc.repransiquotes,'"') + content + self._stransi(xsc.repransiquotes,'"')

	def _strpi(self,target,data):
		return self._strtag(self._stransi(xsc.repransipiquestion,"?") + self._stransi(xsc.repransipitarget,target) + " " + self._stransi(xsc.repransipidata,data) + self._stransi(xsc.repransipiquestion,"?"))

	def __str__(self):
		return self.dostr()
 
class XSCText(XSCNode):
	"""text"""

	represcapes = { '\t' : '\\t' , '\033' : '\\e' , '\\' : '\\\\' }
	reprtreeescapes = { '\n' : '\\n' , '\t' : '\\t' , '\033' : '\\e' , '\\' : '\\\\' }
	strescapes = { '<' : '&lt;' , '>' : '&gt;' , '&' : '&amp;' , '"' : '&quot;' }

	def __init__(self,content = ""):
		self.content = content

	def _doAsHTML(self):
		return XSCText(self.content)

	def dostr(self):
		v = []
		for i in self.content:
			if self.strescapes.has_key(i):
				v.append(self.strescapes[i])
			elif ord(i)>=128:
				v.append('&#' + str(ord(i)) + ';')
			else:
				v.append(i)
		return string.joinfields(v,"")

	def _dorepr(self):
		v = []
		for i in self.content:
			if self.represcapes.has_key(i):
				v.append(self.represcapes[i])
			else:
				v.append(i)
		return string.joinfields(v,"") 

	def _doreprtree(self,nest,elementno):
		v = []
		for i in self.content:
			if self.reprtreeescapes.has_key(i):
				v.append(self.reprtreeescapes[i])
			elif ord(i)<32:
				v.append("\\x" + str(ord(i)))
			else:
				v.append(i)
		s = string.joinfields(v,"") 
		return [[nest,self.startlineno,elementno,self._strtextquotes(self._strtext(s))]]

class XSCFrag(XSCNode):
	"""contains a list of XSCNodes"""

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

	def _doAsHTML(self):
		v = []
		for child in self.content:
			v.append(child.asHTML())
		return XSCFrag(v)

	def _dorepr(self):
		v = []
		for child in self:
			v.append(child._dorepr())
		return string.joinfields(v,"")

	def _doreprtree(self,nest,elementno):
		v = []
		v.append([nest,self.startlineno,elementno,self._strtag('XSCFrag')])
		i = 0
		for child in self:
			v = v + child._doreprtree(nest+1,elementno + [i])
			i = i + 1
		v.append([nest,self.endlineno,elementno,self._strtag('/XSCFrag')])
		return v

	def dostr(self):
		v = []
		for child in self.content:
			v.append(child.dostr())
		return string.joinfields(v,"")

	def __getitem__(self,index):
		"""returns the index'th node for the content of the fragment"""
		return self.content[index]

	def __setitem__(self,index,value):
		"""allows you to replace the index'th content node of the fragment"""
		if len(self.content)>index:
			self.content[index] = ToNode(value)

	def __delitem__(self,index):
		"""removes the index'th content node from the fragment"""
		if len(self.content)>index:
			del self.content[index]

	def __getslice__(self,index1,index2):
		"""returns a slice of the content of the fragment"""
		return XSCFrag(self.content[index1:index2])

	def __setslice__(self,index1,index2,sequence):
		"""modifies a slice of the content of the fragment"""
		self.content[index1:index2] = map(ToNode,sequence)

	def __delslice__(self,index1,index2):
		"""removes a slice of the content of the fragment"""
		del self.content[index1:index2]

	def __len__(self):
		"""return the number of children"""
		return len(self.content)

	def append(self,other):
		self.content.append(ToNode(other))

	def preppend(self,other):
		self.content = [ ToNode(other) ] + self.content[:]

class XSCAttrs(XSCNode):
	"""contains a dictionary of XSCNodes which are wrapped into attribute nodes"""

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
		"""removes attributes from the list"""
		res = XSCAttrs(self.content)
		for attr in attrs:
			del res[attr]
		return res

	def _doAsHTML(self):
		return XSCAttrs(self.attr_handlers,self.content)

	def _dorepr(self):
		v = []
		for attr in self.keys():
			v.append(" " + self._strattrname(attr) + '=' + self._strattrquotes(self[attr]._dorepr()))
		return string.joinfields(v,"")

	def _doreprtree(self,nest,elementno):
		v = [nest,self.startlineno,elementno,""]
		for attr in self.keys():
			line = self[attr]._dorepr()
			v[-1] = v[-1] + " " + self._strattrname(attr) + '=' + self._strattrquotes(line)
		return [v]

	def dostr(self):
		v = []
		for attr in self.keys():
			v.append(" " + attr + '="' + self[attr].dostr() + '"')
		return string.joinfields(v,"")

	def has_attr(self,index):
		return self.content.has_key(index)

	def __getitem__(self,index):
		"""returns the attribute with the name index"""
		return self.content[index] # we're returning the packed attribute here, because otherwise there would be no possibility to get an expanded URL

	def __setitem__(self,index,value):
		"""insert an attribute with the name index and the value value into the attribute dictionary"""
		# values are converted to Nodes first and then wrapped into the attribute nodes as specified via the attr_handlers dictionary
		lowerindex = string.lower(index)
		if self.attr_handlers.has_key(lowerindex):
			self.content[lowerindex] = self.attr_handlers[lowerindex](ToNode(value)) # convert the attribute to a node and pack it into an attribute object
		else:
			raise XSCIllegalAttributeError(xsc.handler.lineno,self,index)

	def __delitem__(self,index):
		"""removes the attribute with the name index (if there is one)"""
		if self.has_attr(index):
			del self.content[index]

	def keys(self):
		"""returns the keys of the dictionary, i.e. a list of the attribute names"""
		return self.content.keys()

	def __len__(self):
		"""return the number of attributes"""
		return len(self.keys())

	def update(self,other):
		for attr in other.keys():
			self[attr] = other[attr]

class XSCComment(XSCNode):
	"""comments"""

	def __init__(self,content = ""):
		self.content = content

	def _doAsHTML(self):
		return XSCComment(self.content)

	def _dorepr(self):
		return self._strtag("!--" + self.content + "--")

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._strtag("!--" + self.content + "--")]]

	def dostr(self):
		return "<!--" + self.content + "-->"

class XSCDocType(XSCNode):
	"""document type"""

	def __init__(self,content = ""):
		self.content = content

	def _dorepr(self):
		return self._strtag("!DOCTYPE " + self.content)

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._strtag("!DOCTYPE " + self.content)]]

	def dostr(self):
		return "<!DOCTYPE " + self.content + ">"

class XSCProcInst(XSCNode):
	"""processing instructions"""

	def __init__(self,target,content = ""):
		self.target = target
		self.content = content

	def _dorepr(self):
		return self._strpi(self.target,self.content)

	def _doreprtree(self,nest,elementno):
		return [[nest,self.startlineno,elementno,self._strpi(self.target,self.content)]]

	def dostr(self):
		return "<?" + self.target + " " + self.content + "?>"

class XSCElement(XSCNode):
	"""XML elements"""

	close = 0 # 0 => stand alone element, 1 => element with content
	attr_handlers = {}
	name = "XSCElement" # will be changed for derived classes/elements in RegisterElement()

	def __init__(self,content = [],attrs = {},**restattrs):
		self.content = XSCFrag(content)
		self.attrs = XSCAttrs(self.attr_handlers,{})

		self.attrs.update(attrs)
		self.attrs.update(restattrs)

	def append(self,item):
		self.content.append(item)

	def _doAsHTML(self):
		return self.__class__(self.content.asHTML(),self.attrs.asHTML()) # "virtual" copy constructor

	def _dorepr(self):
		v = []
		if self.close:
			v.append(self._strtag(self._strelementname(self.name) + self.attrs._dorepr()))
			for child in self:
				v.append(child._dorepr())
			v.append(self._strtag(self._strelementname("/" + self.name)))
		else:
			v.append(self._strtag(self._strelementname(self.name) + self.attrs._dorepr() + self._strelementname("/")))
		return string.joinfields(v,"")

	def _doreprtree(self,nest,elementno):
		v = []
		if self.close:
			v.append([nest,self.startlineno,elementno,self._strtag(self._strelementname(self.name) + self.attrs._dorepr())])
			i = 0
			for child in self:
				v = v + child._doreprtree(nest+1,elementno + [i])
				i = i + 1
			v.append([nest,self.endlineno,elementno,self._strtag(self._strelementname("/" + self.name))])
		else:
			v.append([nest,self.startlineno,elementno,self._strtag(self._strelementname(self.name) + self.attrs._dorepr() + self._strelementname("/"))])
		return v

	def dostr(self):
		"""returns this element as a string converted to HTML"""

		v = []
		v.append("<")
		v.append(self.name)
		v.append(self.attrs.dostr())
		s = self.content.dostr()
		if self.close == 1:
			v.append(">")
			v.append(s)
			v.append("</")
			v.append(self.name) # name must be a string without any nasty characters
			v.append(">")
		else:
			if len(s):
				raise XSCEmptyElementWithContentError(xsc.handler.lineno,self)
			v.append(">")

		return string.joinfields(v,"")

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
		"removes an attribute or one of the content nodes depending on whether a string (i.e. attribute name) or a number (i.e. content node index) is passed in"""
		if type(index)==types.StringType:
			del self.attrs[index]
		else:
			del self.content[index]

	def __getslice__(self,index1,index2):
		"""returns a slice of the content of the element"""
		return self.content[index1:index2]

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
			url = repr(self[imgattr])
			size = ImageSize(url)
			sizedict = { "width": size[0], "height": size[1] }
			if size[0] != -1: # the width was retrieved so we can use it
				if self.has_attr(widthattr):
					try:
						self[widthattr] = eval(str(self[widthattr]) % sizedict)
					except:
						raise XSCImageSizeFormatError(xsc.handler.lineno,self,widthattr)
				else:
					self[widthattr] = size[0]
			if size[1] != -1: # the height was retrieved so we can use it
				if self.has_attr(heightattr):
					try:
						self[heightattr] = eval(str(self[heightattr]) % sizedict)
					except:
						raise XSCImageSizeFormatError(xsc.handler.lineno,self,heightattr)
				else:
					self[heightattr] = size[1]

def RegisterElement(name,element):
	"""registers the element handler element to be used for elements with name name"""
	element_handlers[name] = element
	element.name = name

class XSCurl(XSCElement):
	"""URLS (may be used as an element or an attribute)"""

	def __init__(self,content = [],attrs = {},**restattrs):
		if type(content) == types.InstanceType and content.__class__ == XSCurl:
			self.content = content.content
		else:
			self.content = XSCFrag(content)

	def _dorepr(self):
		return URLForInput(self.content.dostr())

	def _doreprtree(self,nest,elementno):
		url = URLForInput(self.content.dostr())
		return [[nest,self.startlineno,elementno,url]]

	def dostr(self):
		return URLForOutput(self.content.dostr())
RegisterElement("url",XSCurl)

###
###
###

def RegisterEntity(name,number):
	pass
#	xmllib.XMLParser.entitydefs[name] = "&#" + str(number) + ";"

class XSCHandler(saxlib.HandlerBase):
	def startDocument(self):
		self.nesting = [ XSCFrag() ] # our nodes do not have a parent link, therefore we have to store the active path through the tree in a stack (which we call nesting, because stack is already used by the base class
		self.lineno = -1

	def endDocument(self):
		self.root = self.nesting[0] # we're finished parsing and the XSCFrag that we put at the bottom of the stack is our document root

	def processingInstruction(self,target,data):
		e = XSCProcInst(target,data)
		e.startlineno = self.lineno
		self.nesting[-1].append(e) # add the new PI to the content of the innermost element

	def startElement(self, name, attrs):
  		lowername = string.lower(name)
		if element_handlers.has_key(lowername):
			e = element_handlers[lowername]([],attrs)
			e.startlineno = self.lineno
		else:
			raise XSCIllegalElementError(xsc.handler.lineno,lowername)
		self.nesting[-1].append(e) # add the new element to the content of the innermost element (or to the array)
		self.nesting.append(e) # push new innermost element onto the stack

	def endElement(self, name):
		self.nesting[-1].endlineno = self.lineno
		self.nesting[-1:] = [] # pop the innermost element off the stack

	def characters(self, ch, start, length):
		data = ch[start:start+length]

		if data != "" and (data != "\n" or xsc.ignorelinefeed==0):
			e = XSCText(data)
			e.startlineno = self.lineno
			self.nesting[-1].append(e) # add the new string to the content of the innermost element

	def resolveEntity(self, publicId, systemId):
		print "'",publicID,"'",systemId,"'"
		return systemID

	def unparsedEntityDecl(self, name, publicId, systemId, ndata):
		print "'",name,"'",publicID,"'",systemId,"'",ndata,"'"

	def setDocumentLocator(locator):
		print "#"*80,locator.getLineNumber()
		self.lineno = locator.getLineNumber()
		
	def handle_comment(self,comment):
		e = XSCComment(comment) 
		e.startlineno = self.lineno
		self.nesting[-1].append(e)

	def warning(self,exception):
		print str(exception)

	def error(self,exception):
		raise exception

	def fatalError(self,exception):
		raise exception

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
		self.repransibrackets = "36"
		self.repransielementname = "33"
		self.repransiattrname = "33"
		self.repransitext = ""
		self.repransiquotes = "36"
		self.repransipiquestion = "36"
		self.repransipitarget = "36"
		self.repransipidata = "36"
		self.reprtree = 1
		self.ignorelinefeed = 0
		self.parser = saxexts.make_parser()
		self.handler = XSCHandler()
		self.parser.setDocumentHandler(self.handler) # Tell the parser to use our handler
		self.parser.setErrorHandler(self.handler) # Use our handler for reporting errors too

	def parsestring(self,filename,string):
		"""Parses a string and returns the resulting XSC"""
		self.filename = filename
		self.parser.reset()
		self.parser.feed(string)
		self.parser.close()
		return self.parser.root

	def parsefile(self,filename):
		"""Reads and parses a XML file and returns the resulting XSC"""
		self.filename = filename
		self.parser.parseFile(open(filename))
		self.parser.close()
		return self.handler.root

	def parseurl(self,url):
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

xsc = XSC()

