#! /usr/bin/python

import os
import string
import types

# for file size checking
import stat

# for image size checking
import Image

# for parsing XML files
import sys
import xml.sax.saxlib
import xml.sax.saxexts

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
		return "the element '" + self.element.__class__.__name__ + "' is specified to be empty, but has content"

class EHSCIllegalAttribute(EHSCException):
	"this element has an attribute that is not allowed"

	def __init__(self,element,attr):
		self.element = element
		self.attr = attr

	def __str__(self):
		return "the element '" + self.element.__class__.__name__ + "' has an attribute ('" + self.attr + "') that is not allowed here. The only allowed attributes are: " + str(self.element.permitted_attrs)

class EHSCImageSizeFormat(EHSCException):
	"Can't format or evaluate image size attribute"

	def __init__(self,element,attr):
		self.element = element
		self.attr = attr

	def __str__(self):
		return "the value '" + str(self.element[self.attr]) + "' for the image size attribute '" + self.attr + "' of the element '" + self.element.__class__.__name__ + "' can't be formatted or evaluated"

class EHSCFileNotFound(EHSCException):
	"Can't open image for getting image size"

	def __init__(self,url):
		self.url = url

	def __str__(self):
		return "the image file '" + self.url + "' can't be opened"

###
### functions implementing special HSC features
###

def ExpandedURL(url):
	"expands URLs"

	return url

def ImageSize(url):
	"returns the size of an image as a tuple"

	try:
		img = Image.open(url)
		return img.size
	except:
		raise EHSCFileNotFound(url)

def FileSize(url):
	"returns the size of a file in bytes"

	return os.stat(url)[stat.ST_SIZE]

###
###
###

class CNode:
	"base class for nodes in the document tree. Derived class must implement AsString() und AsHTML()"

	def __add__(self,other):
		return [self] + other

	def __radd__(self,other):
		return other + [self]

class CComment(CNode):
	"comments"

	def __init__(self,content = ""):
		self.content = content

	def AsHTML(self,mode = None):
		return CComment(self.content)

	def AsString(self):
		return "<!--" + self.content + "-->"

class CElement(CNode):
	"XML elements"

	close = 0
	permitted_attrs = []

	def __init__(self,content = [],attrs = {},**restattrs):
		self.content = content
		self.attrs = {}

		# make a deep copy here
		for i in attrs.keys():
			self.attrs[i] = attrs[i]
		for i in restattrs.keys():
			self.attrs[i] = restattrs[i]

	def append(self,item):
		self.content.append(item)

	def CheckAttrs(self):
		"checks that only attributes that are allow are used (raises an exception otherwise)"

		for attr in self.attrs.keys():
			if attr not in self.permitted_attrs:
				raise EHSCIllegalAttribute(self,attr)

	def ExpandLinkAttribute(self,attr):
		"expands the url that is the value of attr"

		if self.has_attr(attr):
			self[attr] = ExpandedURL(self[attr])

	def AddImageSizeAttributes(self,imgattr,widthattr = "width",heightattr = "height"):
		"add width and height attributes to the element for the image that can be found in the attributes imgattr. if the attribute is already there it is taken as a formating template with the size passed in as a dictionary with the keys 'width' and 'height', i.e. you could make your image twice as wide with width='%(width)d*2'"

		if self.has_attr(imgattr):
			self.ExpandLinkAttribute(imgattr)
			size = ImageSize(self[imgattr])
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

	def AsHTML(self,mode = None):
		self.CheckAttrs()

		e = self
		e.content = AsHTML(self.content,mode)
		e.attrs   = AsHTML(self.attrs,mode)

		return e

	def AsString(self):
		"returns this element as a string. For the content and the attributes the global function AsString() is called recursively"

		v = []
		v.append("<")
		v.append(self.__class__.__name__)
		if len(self.attrs.keys()):
			v.append(" ")
			v.append(AsString(self.attrs))
		s = AsString(self.content)
		if self.close:
			v.append(">")
			v.append(s)
			v.append("</")
			v.append(self.__class__.__name__) # name must be a string without any nasty characters
			v.append(">")
		else:
			if len(s):
				raise EHSCEmptyElementWithContent(self)
			v.append("/>")

		return string.joinfields(v,"")

	def __getitem__(self,index):
		return self.attrs[index]

	def __setitem__(self,index,value):
		self.attrs[index] = value

	def has_attr(self,attr):
		return self.attrs.has_key(attr)

def AsHTML(value,mode = None):
	"transforms a value into its HTML equivalent: this means that HSC nodes get expanded to their equivalent HTML subtree. Scalar types are returned as is. Lists, tuples and dictionaries are treated recurcively"

	if type(value) in [ types.StringType,types.NoneType,types.IntType,types.LongType,types.FloatType ]:
		return value
	elif type(value) in [ types.ListType,types.TupleType ]:
		v = []
		for i in value:
			v.append(AsHTML(i,mode))
		return v
	elif type(value) == types.DictType:
		v = {}
		for i in value.keys():
			v[i] = AsHTML(value[i])
		return v
	else:
		return value.AsHTML(mode)

def AsString(value):
	"transforms a value into a string: string are returned with 'nasty' characters replaced with entities, HSC and HTML nodes are output as one would expect. Lists, tuples and dictionaries are treated recursively"

	if type(value) == types.StringType:
		v = []
		for i in value:
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
	elif type(value) in [ types.NoneType,types.IntType,types.LongType,types.FloatType ] :
		return str(value)
	elif type(value) in [ types.ListType,types.TupleType ]:
		v = []
		for i in value:
			v.append(AsString(i))
		return string.joinfields(v,"")
	elif type(value) == types.DictType:
		v = []
		for i in value.keys():
			if len(v):
				v.append(" ")
			v.append(i) # keys must be strings without any nasty characters
			s = AsString(value[i])
			if len(s):
				v.append('="') # we can use double quotes here, because all double quotes will be replaced with the entity in the string
				v.append(s)
				v.append('"')
		return string.joinfields(v,"")
	else:
		return value.AsString()

class html(CElement):
	close = 1

class head(CElement):
	close = 1

class title(CElement):
	close = 1

class link(CElement):
	close = 0

class body(CElement):
	close = 1
	permitted_attrs = [ "background","bgcolor","text","link","vlink","alink","leftmargin","topmargin","marginwidth","marginheight","style","onload"]

class h1(CElement):
	close = 1

class h2(CElement):
	close = 1

class h3(CElement):
	close = 1

class h4(CElement):
	close = 1

class h5(CElement):
	close = 1

class h6(CElement):
	close = 1

class p(CElement):
	close = 1

class div(CElement):
	close = 1

class table(CElement):
	close = 1

class tr(CElement):
	close = 1

class th(CElement):
	close = 1

class td(CElement):
	close = 1

class img(CElement):
	close = 0
	permitted_attrs = [ "src","alt","border","width","height" ]

	def AsHTML(self,mode = None):
		e = CElement.AsHTML(self,mode)

		e.AddImageSizeAttributes("src")

		return e

class br(CElement):
	close = 0

class hr(CElement):
	close = 0

class a(CElement):
	close = 1
	permitted_attrs = [ "href","name" ]

	def AsHTML(self,mode = None):	
		e = CElement.AsHTML(self,mode)

		e.ExpandLinkAttribute("href")

		return e

class b(CElement):
	close = 1

class plaintable(table):
	close = 1

	def AsHTML(self,mode = None):
		e = table(AsHTML(self.content,mode),AsHTML(self.attrs,mode))

		if not e.has_attr("cellpadding"):
			e["cellpadding"] = 0
		if not e.has_attr("cellspacing"):
			e["cellspacing"] = 0
		if not e.has_attr("border"):
			e["border"] = 0

		return e

class plainbody(body):
	close = 1

	def AsHTML(self,mode = None):
		e = body(AsHTML(self.content,mode),AsHTML(self.attrs,mode))

		if not e.has_attr("leftmargin"):
			e["leftmargin"] = 0
		if not e.has_attr("topmargin"):
			e["topmargin"] = 0
		if not e.has_attr("marginheight"):
			e["marginheight"] = 0
		if not e.has_attr("marginwidth"):
			e["marginwidth"] = 0

		return e

class z(CElement):
	close = 1

	def AsHTML(self,mode = None):
		return AsHTML(["«",AsHTML(self.content,mode),"»"],mode)

class nbsp(CElement):
	close = 0

	def AsHTML(self,mode = None):
		return AsHTML("\xA0",mode)

class filesize(CElement):
	close=1

	def AsHTML(self,mode = None):
		return FileSize(ExpandedURL(AsString(self.content)))

class HSC(xml.sax.saxlib.HandlerBase):
	"Reads a XML file and constructs a HSC tree from it."

	def __init__(self,filename):
		xml.sax.saxlib.HandlerBase.__init__(self)
		self.stack = [] # our nodes do not have a parent link, therefore we have to store the active path through the tree in a stack
		parser = xml.sax.saxexts.make_parser()
		parser.setDocumentHandler(self)
		parser.parseFile(open(filename))
		parser.close()

	def processingInstruction (self,target, remainder):
		pass

	def startElement(self,name,attrs = {}):
		e = eval(name+"([],attrs)")
		self.stack[-1].append(e)
		self.stack.append(e)
		
	def endElement(self,name):
		self.stack[-1:] = []

	def ignorableWhitespace(self,data,start_ix,length):
		pass
#        self.characters(data,start_ix,length)

	def characters(self,data,start_ix,length):
		self.stack[-1].append(data[start_ix:start_ix+length])

	def handle_comment(self,s):
		print s
		self.stack[-1].append(CComment(s))

	def startDocument(self):
		self.stack.append([])

	def endDocument(self):
		self.root = self.stack[0]

if __name__ == "__main__":
	h = HSC(sys.argv[1])
	print AsString(AsHTML(h.root))

