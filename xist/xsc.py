#! /usr/bin/env python

## Copyright 1999-2000 by Living Logic AG, Bayreuth, Germany.
## Copyright 1999-2000 by Walter Dörwald
##
## See the file LICENSE for licensing details

"""
XIST is a HTML preprocessor/generator and an XML transformation engine.
It is easily extensible with new XML elements, allows embedding
Python code in XML files and works together with httpdapy/mod_python.

It was written as a replacement for the HTML preprocessor HSC
(http://www.giga.or.at/~agi/hsc/), and borrows some features and ideas from it.

It also borrows the basic ideas (XML/HTML elements as Python objects)
from HTMLgen (http://starship.skyport.net/crew/friedrich/HTMLgen/html/main.html)
or HyperText (http://dustman.net/andy/python/HyperText/)

XIST is based on XML, so you have two choices when constructing
your hierarchical tree of HTML objects: You can directly construct
it, like HTMLgen and HyperText do, as a tree of Python objects or
you can get a tree by parsing an XML file.

For every HTML element there exists a corresponding class, that
has a constructor of the form
	class(*content,**attrs),
so constructing an HTML element works like this:
	e = html.div(
		"Go to ",
		html.a("Python.org",href="http://www.python.org/"),
		"!"
	)

This object can be converted to a printable string with
the method asString():
	print e.asString()

In XIST you're not limited to the HTML element types.
You can define your own! To be able to convert these
new element types to a HTML object tree, you must implement
the method asHTML, and you must derive your class from
xsc.Element as in the following example:

	class cool(xsc.Element):
		empty = 1

		def asHTML(self):
			return html.b("Python is cool!")

Using this element is as simple as this:
	e = cool()
	print e.asHTML().asString()

The class variable empty in the above example specifies
if the element type has an empty content model (like <br/>
or <img/>) or not.

To be able to use your own classes in XML files, you have
to tell the parser about them. This is done with the
function registerElement(element,namespacename,elementname = None)
(see its docstring) or if you want to register all element
classes in a module with registerAllElements(dict,namespacename)
(again see its docstring for further info).


URLs, path markers and the URL stack
====================================
XIST has a class for URLs (URL.URL) which is a thin
wrapper around urlparse's features. You can add URLs
via +, e.g.
	URL("http://www.foo.org/") + URL("/images/bar.png")
yields an URL object equivalent to
	URL("http://www.foo.org/images/bar.png").

Path markers
------------
XIST supports so called "path markers". Any directory
name in an URL starting with "*" is not a real directory
name, but marks a position in the path. When you add
two URLs and the second one starts with a path marker,
the second URL will be considered relative to the part
of the path before the first occurence of the same path
marker in the first URL. Example:
	URL("http://www.foo.org/gurk/*root/hurz/hinz.html") + URL("*root/kunz/hinz.png")
yields the following URL
	URL("http://www.foo.org/gurk/*root/kunz/hinz.png")
which is equivalent to
	URL("http://www.foo.org/gurk/kunz/hinz.png").
You can use this feature to simplify the handling of
deeply nested directory structures.

The URL stack
-------------
XIST maintains a stack of URLs that is used in parsing files.

Whenever you parse an XML file via xsc.xsc.parse(name),
the URL corresponding to name will be pushed onto the stack.
All URL attributes (e.g. the href in <a>, or the src in <img>)
encountered during the parsing of the file will be interpreted
relative to the URL on top of the stack. After parsing the file
the URL will be popped of the stack again. This means that
all URLs will point to the correct location.

When an URL is pushed onto the stack the URL itself will be
interpreted relative to the old one on top of the stack.
XIST itself always pushes "*/" onto the stack when starting
up. ("*/" is a nameless path marker that allows you to easily
return to the root of your directory tree)

Example:
When you parse a file "foo/bar/baz.xml" via
	element = xsc.xsc.parse("foo/bar/baz.xml")
and this file contains an image
	<img src="*/images/gurk.png"/>
the following will happen:
The URL "foo/bar/baz.xml" will be pushed onto the stack.
As the stack already contains the URL "*/", this will
result in a new stacktop "*/foo/bar/baz.xml". Now when
the image is encountered, the stacktop and the image
URL will be added together to yield
	"*/images/gurk.png".

Output of URLs
--------------
So what happens with the URL "*/images/gurk.png" in the
above example, when the element is converted to a string?
All URLs encountered during this conversion will be made
relative to the URL on the stacktop and output in this
way. This means the following:
You have to manually push the URL of the file you read
onto the stack:
	xsc.xsc.pushURL("foo/bar/baz.xml")
and then the image URL "*/images/gurk.png" from above
will be output as "../../images/gurk.png".
(And don't forget to pop the URL again with xsc.xsc.popURL())

There is another situation where you will want to manually
push an URL onto the stack: When some of your own elements
generate new URLs in their asHTML() methods. As this
conversion happens sometime after the file is parsed, the URL
of the file is already gone from the stack. But of course
you will want new URLs to be interpreted relative to the file
name in which the element was encountered. So you have to push
the URL to the stack manually. Of course all these steps can
be combined into the following:
	url = "foo/bar/baz.xml"
	element = xsc.xsc.parse(url)
	xsc.xsc.pushURL(url)
	str = element.asHTML().asString()
	xsc.xsc.popURL()

Automatic generation of image size attributes
=============================================
Most elements from the html module (i.e. the HTML
"tags") don't do anything fancy in their own asHTML()
member (They only call asHTML() recursively for their
own content).

The img element is one exception. Its asHTML() method
determines the size of the image and sets the HEIGHT
and WIDTH attribute accordingly.

This is not the whole truth. When the WIDTH or HEIGHT attribute
is already specified, the following happens:
%-formatting is used on the attribute value, the width and
height of the image is passed to the % operator as a dictionary
with the keys "width" and "height". The resulting string is
eval()uated and it's result is used for the attribute. So to make
an image twice as wide and high do the following:
	<img src="foo.png" width="%(width)d*2" height="%(height)d*2"/>

Embedding Python code
=====================
It's possible to embed Python code into XIST XML files. For this
XIST support two new processing instruction targets: xsc-exec and
xsc-eval. The content of xsc-exec will be executed when the processing
instruction node is instantiated, i.e. when the XML file is parsed,
so anything you do there will be available afterwards.

The result of a call to asHTML() for a xsc-eval processing instruction
is whatever the Python code in the content returns. For example, consider
the following XML file:
	<?xsc-exec
	def gauss(top = 100):
		sum = 0
		for i in xrange(top+1):
			sum = sum + i
		return sum
	?>
	<b><?xsc-eval return gauss()?></b>
Parsing this file and converting it to HTML results in the following:
	<b>5050</b>

For further information see the class ProcInst.

Requirements
============
XSC requires Python 1.5.2.

XSC uses sgmlop for parsing XML files, so you either need the
Python XML package (at least 0.5.5.1), or a standalone version
of sgmlop (not tested; available from
http://www.pythonware.com/products/xml/index.htm)

To determine image sizes, XSC needs the Python Imaging library (PIL)
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import os
import string
import types
import sys
import getopt

# for file size checking
import stat

# for image size checking
import Image

# for parsing XML files
import sgmlop

# for reading remote files
import urllib

# our sandbox
import procinst

# our own new URL class
from URL import URL

# exceptions
from errors import *

###
### configuration
###

def getStringFromEnv(name,default):
	try:
		var = os.environ[name]
	except:
		return default
	return var

def getIntFromEnv(name,default):
	try:
		var = int(os.environ[name])
	except:
		return default
	return var

def getANSICodesFromEnv(name,default):
	"""
	parses an environment variable from a string list and returns it or
	the default if the environment variable can't be found or parsed.
	"""
	try:
		var = eval(os.environ[name])
	except:
		return default
	if type(var) is types.StringType:
		var = [ var,var ]
	return var

retrieveremote = getIntFromEnv("XSC_RETRIEVEREMOTE",1)                                          # should remote URLs be retrieved? (for filesize and imagesize tests)
retrievelocal = getIntFromEnv("XSC_RETRIEVELOCAL",1)                                            # should local URLs be retrieved? (for filesize and imagesize tests)
reprcharreflowerlimit = getIntFromEnv("XSC_REPRCHARREFLOWERLIMIT",128)                          # chracters with an ASCII (or Unicode) code above reprcharreflowerlimit wll be dumped as charcter references
repransi = getIntFromEnv("XSC_REPRANSI",0)                                                      # should ANSI escape sequences be used for dumping the DOM tree and which ones? (0=off,1=dark background,2=light background)
reprtab = getStringFromEnv("XSC_REPRTAB",". ")                                                  # how to represent an indentation in the DOM tree?
repransitab = getANSICodesFromEnv("XSC_REPRANSI_TAB",[ "1;34","37" ])                           # ANSI escape sequence to be used for tabs
repransiquote = getANSICodesFromEnv("XSC_REPRANSI_QUOTE",[ "1;32","32" ])                       # ANSI escape sequence to be used for quotes (delimiters for text and attribute nodes)
repransislash = getANSICodesFromEnv("XSC_REPRANSI_SLASH",[ "","" ])                             # ANSI escape sequence to be used for slashes in element names
repransibracket = getANSICodesFromEnv("XSC_REPRANSI_BRACKET",[ "1;32","32" ])                   # ANSI escape sequence to be used for brackets (delimiters for tags)
repransiquestion = getANSICodesFromEnv("XSC_REPRANSI_QUESTION",[ "1;32","1;32" ])               # ANSI escape sequence to be used for question marks (delimiters for processing instructions)
repransiexclamation = getANSICodesFromEnv("XSC_REPRANSI_EXCLAMATION",[ "1;32","1;32" ])         # ANSI escape sequence to be used for exclamation marks (used in comments and doctypes)
repransitext = getANSICodesFromEnv("XSC_REPRANSI_TEXT",[ "","" ])                               # ANSI escape sequence to be used for text
repransicharref = getANSICodesFromEnv("XSC_REPRANSI_CHARREF",[ "37","34" ])                     # ANSI escape sequence to be used for character references
repransielementnamespace = getANSICodesFromEnv("XSC_REPRANSI_ELEMENTNAMESPACE",[ "1;36","36" ]) # ANSI escape sequence to be used for element namespaces
repransielementname = getANSICodesFromEnv("XSC_REPRANSI_ELEMENTNAME",[ "1;36","36" ])           # ANSI escape sequence to be used for element names
repransiattrname = getANSICodesFromEnv("XSC_REPRANSI_ATTRNAME",[ "1;36","36" ])                 # ANSI escape sequence to be used for attribute names
repransidoctypemarker = getANSICodesFromEnv("XSC_REPRANSI_DOCTYPEMARKER",[ "1","1" ])           # ANSI escape sequence to be used for document types marker (i.e. !DOCTYPE)
repransidoctypetext = getANSICodesFromEnv("XSC_REPRANSI_DOCTYPETEXT",[ "","" ])                 # ANSI escape sequence to be used for document types
repransicommentmarker = getANSICodesFromEnv("XSC_REPRANSI_COMMENTMARKER",[ "","" ])             # ANSI escape sequence to be used for comment markers (i.e. --)
repransicommenttext = getANSICodesFromEnv("XSC_REPRANSI_COMMENTTEXT",[ "","" ])                 # ANSI escape sequence to be used for comment text
repransiattrvalue = getANSICodesFromEnv("XSC_REPRANSI_ATTRVALUE",[ "","" ])                     # ANSI escape sequence to be used for attribute values
repransiurl = getANSICodesFromEnv("XSC_REPRANSI_URL",[ "1;33","33" ])                           # ANSI escape sequence to be used for URLs
repransiprocinsttarget = getANSICodesFromEnv("XSC_REPRANSI_PROCINSTTARGET",[ "1;31","1;31" ])   # ANSI escape sequence to be used for processing instruction targets
repransiprocinstdata = getANSICodesFromEnv("XSC_REPRANSI_PROCINSTDATA",[ "","" ])               # ANSI escape sequence to be used for processing instruction data
outputXHTML = getIntFromEnv("XSC_OUTPUT_XHTML",1)                                               # XHTML output format (0 = plain HTML, 1 = HTML compatible XHTML, 2 = pure XHTML)

###
### helpers
###

def _stransi(codes,string,ansi = None):
	if ansi is None:
		ansi = repransi
	if ansi and len(codes[ansi-1]) and string:
		return "\033[" + codes[ansi-1] + "m" + string + "\033[0m"
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

def strDocTypeMarker(ansi = None):
	return _stransi(repransidoctypemarker,"DOCTYPE",ansi = ansi)

def strDocTypeText(text,ansi = None):
	return _stransi(repransidoctypetext,text,ansi = ansi)

def strCommentMarker(ansi = None):
	return _stransi(repransicommentmarker,"--",ansi = ansi)

def strCommentText(text,ansi = None):
	return _stransi(repransicommenttext,text,ansi = ansi)

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

def strExclamation(ansi = None):
	return _stransi(repransiexclamation,"!",ansi)

def strQuote(ansi = None):
	return _stransi(repransiquote,'"',ansi)

def strTab(count,ansi = None):
	return _stransi(repransitab,reprtab*count,ansi = ansi)

def strURL(URL,ansi = None):
	return _stransi(repransiurl,URL,ansi)

def nodeName(nodeClass):
	"""
	returns a list with the namespacename, the elementname and the emptyness of the node.
	Note that for this to work the element has to be registered.
	"""
	try:
		namespacename = nodeClass.namespacename
	except AttributeError:
		namespacename = "xsc" # this is (hopefully) an XSC class
	try:
		elementname = nodeClass.elementname
	except AttributeError:
		elementname = nodeClass.__name__

	return [namespacename,elementname,nodeClass.empty]

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

def ToNode(value):
	t = type(value)
	if t == types.InstanceType:
		if isinstance(value,Frag):
			l = len(value)
			if l==1:
				return ToNode(value[0]) # recursively try to simplify the tree
			elif l==0:
				return Null
			else:
				if isinstance(value,Attr):
					node = Frag() # repack the attribute in a fragment, and we have a valid XSC node
					for i in value:
						node.append(ToNode(i))
					return node
				else:
					return value
		elif isinstance(value,Node):
			return value
	elif t in ( types.StringType,types.IntType,types.LongType,types.FloatType ):
		return Text(value)
	elif t == types.NoneType:
		return Null
	elif t in ( types.ListType,types.TupleType ):
		node = Frag()
		for i in value:
			node.append(ToNode(i))
		l = len(node)
		if l==1:
			return node[0] # recursively try to simplify the tree
		elif l==0:
			return Null
		else:
			return node
	raise IllegalObjectError(-1,value) # none of the above, so we throw and exception

_elementHandlers = {} # dictionary for mapping element names to classes, this dictionary contains the element names as keys and another dictionary as values, this second dictionary contains the namespace names as keys and the element classes as values

class Node:
	"""
	base class for nodes in the document tree. Derived classes must
	implement asHTML() and/or asString()
	"""

	empty = 1

	# location of this node in a file (will be hidden in derived classes, but is specified here, so that no special tests are required. In derived classes this will be set by the parser)
	startloc = None
	endloc = None

	def __repr__(self):
		if xsc.reprtree == 1:
			return self.reprtree()
		else:
			return self.repr()

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
		lenloc = 0
		lenelementno = 0
		for line in lines:
			if line[1] is not None: # convert location to a string
				line[1] = str(line[1])
			else:
				line[1] = ""
			line[2] = string.join(map(str,line[2]),".") # convert element number to a string
			line[3] = strTab(line[0]) + line[3] # add indentation
			lenloc = max(lenloc,len(line[1]))
			lenelementno = max(lenelementno,len(line[2]))

		for line in lines:
			v.append("%*s %-*s %s\n" % (lenloc,line[1],lenelementno,line[2],line[3]))
		return string.join(v,"")

	def _dorepr(self,ansi = None):
		# returns a string representation of the node
		return strBracketOpen(ansi) + strBracketClose(ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		# returns an array containing arrays consisting of the (nestinglevel,location,elementnumber,string representation) of the nodes
		return [[nest,self.startloc,elementno,self._dorepr(ansi)]]

	def asHTML(self):
		"""
		returns a version of this node and it's content converted to HTML,
		so when you define your own element classes you should overwrite asHTML().

		E.g. when you want to define an element that packs it's content into an HTML
		bold element, do the following:

		def foo(xsc.Element):
			empty = 0

			def asHTML(self):
				return html.b(self.content).asHTML()
		"""
		return Null

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

		E.g. asPlainString might be used to construct a title element
		for a page from a part of the content of the page.
		"""
		return ""

	def asInt(self):
		"""
		returns this node converted to an integer.
		"""
		return int(self.asPlainString())

	def asFloat(self,decimal = "."):
		"""
		asFloat(self,decimal = ".") -> float

		returns this node converted to a float.

		decimal specifies which decimal separator is used in the value
		(e.g. "." (the default) or ",").
		"""
		s = self.asPlainString()
		if decimal != ".":
			s = string.replace(s,decimal,".")
		return float(s)

	def asString(self,XHTML = None):
		"""
		asString(self,XHTML = None) -> string

		returns this element as a string suitable for writing to an HTML file or
		printing from a CGI script.

		There will only be 7bit characters in the string, so can use "us-ascii"
		as the chraracter set.

		With the parameter XHTML you can specify if you want HTML output
		(i.e. elements with a content model EMPTY as <foo>) with XHTML == 0, or
		XHTML output that is compatible with HTML browsers (element with an
		empty content model as <foo /> and others that just happen to be empty
		as <foo></foo>) with XHTML == 1 or just plain XHTML with XHTML == 2
		(all empty elements as <foo/>).

		When you use the default (None) that value of the global variable
		outputXHTML will be used, which defaults to 1, but can be overwritten
		by the environment variable XSC_OUTPUT_XHTML and can of course be
		changed dynamically.
		"""
		return ""

	def findNodes(self,type = None,searchchildren = 0,searchattrs = 0,subtype = 0,attrs = None):
		"""
		findNodes(self,type = None,searchchildren = 0,searchattrs = 0,subtype = 0,attrs = None) -> fragment

		returns a fragment which contains child elements of this node.

		If you specify type as the class of an XSC node only nodes of this class
		will be returned. If you pass a list of classes, nodes that are an instance
		of one of the classes will be returned.

		If you set subtype to 1 nodes that are a subtype of type will be returned too.

		If you set searchchildren to 1 not only the immediate children but also the grandchildren
		will be searched for nodes matching the other criteria.

		If you set searchattrs to 1 the attributes of the nodes (if type is Element or one
		of its subtypes) will be searched too.

		If you pass a dictionary as attrs it has to contain string pairs and is used to
		match attribute values for elements. To match the attribute values their
		asPlainString() representation will be used. You can use None as the value to
		test that the attribute is set without testing the value.

		Note that the node has to be of type element (or a subclass of this) to match
		attrs.
		"""
		return Frag()

	def compact(self):
		"""
		returns this node, where textnodes or character references that contain
		only linefeeds are removed, i.e. potentially needless whitespace is removed.
		"""
		return Null

	def _matchesAttrs(self,attrs):
		if attrs is None:
			return 1
		else:
			if isinstance(self,Element):
				for attr in attrs.keys():
					if not self.hasAttr(attr) or ((attrs[attr] is not None) and (self[attr].asPlainString() != attrs[attr])):
						return 0
				else:
					return 1
			else:
				return 0

	def _matches(self,type_,subtype,attrs):
		if type_ is not None:
			if type(type_) not in [ types.ListType, types.TupleType ]:
				type_ = ( type_ , )
			for t in type_:
				if subtype:
					if isinstance(self,t):
						return self._matchesAttrs(attrs)
				else:
					if self.__class__ == t:
						return self._matchesAttrs(attrs)
			else:
				return 0
		else:
			return self._matchesAttrs(attrs)

	def _doreprtreeMultiLine(self,nest,elementno,head,tail,text,formatter,extraFirstLine,ansi = None):
  		lines = string.split(text,"\n")
		l = len(lines)
		if l>1 and extraFirstLine:
			lines.insert(0,"")
			l = l + 1
		v = []
		for i in xrange(l):
			mynest = nest
			s = lines[i]
			while len(s) and s[0] == "\t":
				mynest = mynest + 1
				s = s[1:]
			s = formatter(s,ansi)
			if i == 0:
				s = head + s
			if i == l-1:
				s = s + tail
			v.append([mynest,self._getLoc(i),elementno,s])
		return v

	def _getLoc(self,relrow):
		"""
		Return a location that is relrow rows further down than the starting location
		for this node. Returns None if the location is unknown.
		"""

		if self.startloc is None:
			return None
		else:
			return Location(self.startloc.url,self.startloc.row + relrow)

	def _decorateNode(self,node):
		node.startloc = self.startloc
		node.endloc = self.endloc
		return node

class Text(Node):
	"""
	text node. The characters <, >, & and " will be "escaped" with the
	appropriate character entities. Characters with an ASCII code bigger
	than 127 will be escaped too.
	"""

	empty = 1

	strescapes = { '<' : 'lt' , '>' : 'gt' , '&' : 'amp' , '"' : 'quot' }

	def __init__(self,content = ""):
		self.content = str(content)

	def asHTML(self):
		return self._decorateNode(Text(self.content))

	clone = asHTML

	def asPlainString(self):
		return self.content

	def asString(self,XHTML = None):
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
						ent = entitiesByNumber[ord(i)] # use names if a available, or number otherwise
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
			s = strQuote(ansi) + strText(self.__strtext(1,lines[i],ansi),ansi) + strQuote(ansi)
			v.append([nest,self._getLoc(i),elementno,s])
		return v

	def compact(self):
		for i in self.content:
			if i != '\n' and i != '\r':
				return self._decorateNode(Text(self.content))
		else:
			return Null

class CharRef(Node):
	"""
	character reference (i.e <code>&amp;#42</code>; or <code>&amp;#x42;</code>
	or <code>&amp;uuml;</code>) The content member of the node will be the
	ASCII code of the character.
	"""

	__notdirect = { ord("&") : "amp" , ord("<") : "lt" , ord(">") : "gt", ord('"') : "quot" , ord("'") : "apos" }
	__linefeeds = [ ord("\r") , ord("\n") ]

	def __init__(self,content = 42):
		self.content = content

	def asHTML(self):
		return self._decorateNode(CharRef(self.content))

	clone = asHTML

	def asPlainString(self):
		return chr(self.content)

	def asString(self,XHTML = None):
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

	def _dorepr(self,ansi = None):
		if len(entitiesByNumber[self.content]):
			return self.__strcharref('&' + entitiesByNumber[self.content][0] + ';',ansi)
		else:
			return self.__strcharref('&#' + str(self.content) + ';',ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		s = self.__strcharref('&#' + str(self.content) + ';',ansi) + ' (' + self.__strcharref('&#x' + hex(self.content)[2:] + ';',ansi)
		for name in entitiesByNumber[self.content]:
			s = s + ' ' + self.__strcharref('&' + name + ';',ansi)
		s = s + ')'
		if 0 <= self.content < reprcharreflowerlimit:
			s = s + ' ' + Text(chr(self.content))._doreprtree(0,0,ansi)[0][-1]
		return [[nest,self.startloc,elementno,s]]

	def compact(self):
		if self.content in self.__linefeeds:
			return Null
		else:
			return self._decorateNode(CharRef(self.content))

class Frag(Node):
	"""
	A fragment contains a list of nodes and can be used for dynamically constructing content.
	The member content of an Element is a Frag.
	"""

	empty = 0

	def __init__(self,*content):
		self.__content = []
		for child in content:
			self.extend(child)

	def asHTML(self):
		node = self.__class__()
		for child in self:
			node.append(child.asHTML())
		return self._decorateNode(node)

	def clone(self):
		node = self.__class__()
		for child in self:
			node.append(child.clone())
		return self._decorateNode(node)

	def _dorepr(self,ansi = None):
		v = []
		for child in self:
			v.append(child._dorepr(ansi = ansi))
		return string.join(v,"")

	def _doreprtree(self,nest,elementno,ansi = None):
		v = []
		if len(self):
			v.append([nest,self.startloc,elementno,self._str(brackets = 1,ansi = ansi)])
			i = 0
			for child in self:
				v = v + child._doreprtree(nest+1,elementno + [i],ansi)
				i = i + 1
			v.append([nest,self.endloc,elementno,self._str(brackets = 1,ansi = ansi,slash = -1)])
		else:
			v.append([nest,self.startloc,elementno,self._str(brackets = 1,ansi = ansi,slash = 1)])
		return v

	def asPlainString(self):
		v = []
		for child in self:
			v.append(child.asPlainString())
		return string.join(v,"")

	def asString(self,XHTML = None):
		v = []
		for child in self:
			v.append(child.asString(XHTML))
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
		node = self.__class__()
		for child in self.__content[index1:index2]:
			node.append(child)
		return node

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

	def append(self,*others):
		"""
		append(self,*others)

		appends all items in others to the fragment.
		"""
		for other in others:
			newother = ToNode(other)
			if newother is not Null:
				self.__content.append(newother)

	def insert(self,index,*others):
		"""
		insert(self,index,*others)

		inserts all items in others at the position index.
		(this is the same as self[index:index] = others)
		"""
		for other in others:
			newother = ToNode(other)
			if newother is not Null:
				self.__content.insert(index,newother)
				index = index + 1

	def extend(self,*others):
		"""
		extend(self,*others)

		extends this fragment by all items in others.
		"""
		for other in others:
			newother = ToNode(other)
			if isinstance(newother,Frag):
				for child in newother:
					self.__content.append(child)
			elif newother is not Null:
				self.__content.append(newother)

	def findNodes(self,type = None,subtype = 0,searchchildren = 0,searchattrs = 0,attrs = None):
		node = Frag()
		for child in self:
			if child._matches(type,subtype,attrs):
				node.append(child)
			if searchchildren:
				node.extend(child.findNodes(type,subtype,searchchildren,searchattrs,attrs))
		return node

	def compact(self):
		node = self.__class__()
		for child in self:
			node.append(child.compact())
		return self._decorateNode(node)

	def withSeparator(self,separator,clone = 0):
		"""
		withSeparator(self,separator,clone = 0) -> fragment

		adds a separator node between the nodes of the fragment.

		if clone==0 one node will be inserted several times,
		if clone==1 clones of this node will be used.
		"""
		node = Frag()
		newseparator = ToNode(separator)
		for child in self:
			if len(node):
				node.append(newseparator)
				if clone:
					newseparator = newseparator.clone()
			node.append(child)
		return node

class Comment(Node):
	"""
	a comment node
	"""

	def __init__(self,content = ""):
		self.content = content

	def asHTML(self):
		return self._decorateNode(Comment(self.content))

	clone = asHTML

	def _dorepr(self,ansi = None):
		return strBracketOpen(ansi) + strExclamation(ansi) + strCommentMarker(ansi) + strCommentText(self.content,ansi) + strCommentMarker(ansi) + strBracketClose(ansi)

	def _doreprtree(self,nest,elementno,ansi):
		head = strBracketOpen(ansi) + strExclamation(ansi) + strCommentMarker(ansi)
		tail = strCommentMarker(ansi) + strBracketClose(ansi)
		return self._doreprtreeMultiLine(nest,elementno,head,tail,self.content,strCommentText,0,ansi = ansi)

	def asString(self,XHTML = None):
		return "<!--" + self.content + "-->"

	def compact(self):
		return self._decorateNode(Comment(self.content))

class DocType(Node):
	"""
	a document type node
	"""

	def __init__(self,content = ""):
		self.content = content

	def asHTML(self):
		return self._decorateNode(DocType(self.content))

	clone = asHTML

	def _dorepr(self,ansi = None):
		return strBracketOpen(ansi) + strExclamation(ansi) + strDocTypeMarker(ansi) + " " + strDocTypeText(self.content,ansi) + strBracketClose(ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		return [[nest,self.startloc,elementno,self._dorepr(ansi)]]

	def asString(self,XHTML = None):
		return "<!DOCTYPE " + self.content + ">"

	def compact(self):
		return self._decorateNode(DocType(self.content))

class ProcInst(Node):
	"""
	processing instructions.

	There are two special targets available:

	xsc-exec (e.g. <?xsc-exec pass?>)
	here the content of the processing instruction is executed
	as Python code, so you can define and register XSC elements here.
	Execution is done when the node is constructed, so definitions made
	here will be available afterwards (e.g. during the rest of the
	file parsing stage). When converted to HTML such a node will result
	in an empty Null node.

	xsc-eval (e.g. <?xsc-eval return "foo"?>)
	here the code will be executed when the node is converted to HTML
	as if it was the body of a function, so you can return an expression
	here. Although the content is used as a function body no indentation
	is neccessary or allowed. The returned value will be converted to a
	node and this resulting node will be converted to HTML.

	XSC processing instructions will be evaluated and executed in the
	namespace of the module procinst.

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
		if string.lower(self.target) == "xsc-exec": # execute the code now, so that classes defined here are available for the parser
			exec self.content in procinst.__dict__

	def asHTML(self):
		if string.lower(self.target) == "xsc-exec": # XSC processing instruction, has been executed at construction time already, so we don't have to do anything here
			return Null
		elif string.lower(self.target) == "xsc-eval": # XSC processing instruction, return the result as a node
			function = "def __():\n\t" + string.replace(string.strip(self.content),"\n","\n\t") + "\n"
			exec function in procinst.__dict__
			return ToNode(eval("__()",procinst.__dict__)).asHTML()
		else: # anything else like XML, PHP, etc. is just passed through
			return self._decorateNode(ProcInst(self.target,self.content))

	def clone(self):
		return self._decorateNode(ProcInst(self.target,self.content))

	def _dorepr(self,ansi = None):
		return self._str(content = strQuestion(ansi) + strProcInstTarget(self.target,ansi) + " " + strProcInstData(self.content,ansi) + strQuestion(ansi),brackets = 1,ansi = ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		head = strBracketOpen(ansi) + strQuestion(ansi) + strProcInstTarget(self.target,ansi) + " "
		tail = strQuestion(ansi) + strBracketClose(ansi)
		return self._doreprtreeMultiLine(nest,elementno,head,tail,self.content,strProcInstData,1,ansi = ansi)

	def asString(self,XHTML = None):
		return "<?" + self.target + " " + self.content + "?>"

	def compact(self):
		return self._decorateNode(ProcInst(self.target,self.content))

class Element(Node):
	"""
	<par noindent>This class represents XML/XSC elements. All elements
	implemented by the user must be derived from this class.</par>

	<par>If you not only want to construct a DOM tree via a Python script
	(by directly instantiating these classes), but to read an XML/XSC file
	you must register the element class with the parser, this can be done
	by passing the class object to the function
	<functionref>registerElement</functionref>.</par>

	<par>Every element class should have two class variables:
	<code>empty</code>: this is either <code>0</code> or <code>1</code>
	and specifies whether the element type is allowed to have content
	or not. Note that the parser does not use this as some sort of
	static DTD, i.e. you still must write your empty tags
	like this: <code>&lt;foo/&gt;</code>.</par>

	<par><code>attrHandlers</code> is a dictionary that maps attribute
	names to attribute classes, which are all derived from <classref>Attr</classref>.
	Assigning to an attribute with a name that is not in <code>attrHandlers.keys()</code>
	is an error.</par>
	"""

	empty = 1 # 0 => element with content; 1 => stand alone element
 	attrHandlers = {} # maps attribute names to attribute classes

	def __init__(self,*content,**attrs):
		"""
		__init__(self,*content,**attrs)

		positional arguments are treated as content nodes.

		keyword arguments and dictionaries are treated as attributes.
		"""
		self.content = Frag()
		self.attrs = {}
		for child in content:
			if type(child) == types.DictionaryType:
				for attr in child.keys():
					self[attr] = child[attr]
			else:
				self.extend(child)
		for attr in attrs.keys():
			self[attr] = attrs[attr]

	def append(self,*items):
		"""
		append(self,*items)

		appends to the content (see Frag.append for more info)
		"""

		apply(self.content.append,items)
		if self.empty and len(self):
			raise EmptyElementWithContentError(self)

	def insert(self,index,*items):
		"""
		insert(self,index,*items)

		inserts into the content (see Frag.insert for more info)
		"""
		apply(self.content.insert,(index,) + items)
		if self.empty and len(self):
			raise EmptyElementWithContentError(self)

	def extend(self,*items):
		"""
		extend(self,items)

		extends the content (see Frag.extend for more info)
		"""
		apply(self.content.extend,items)
		if self.empty and len(self):
			raise EmptyElementWithContentError(self)

	def asHTML(self):
		node = self.__class__(self.content.asHTML()) # "virtual" copy constructor
		for attr in self.attrs.keys():
			node[attr] = self[attr].asHTML()
		return self._decorateNode(node)

	def clone(self):
		node = self.__class__(self.content.clone()) # "virtual" copy constructor
		for attr in self.attrs.keys():
			node[attr] = self[attr].clone()
		return self._decorateNode(node)

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
			v.append([nest,self.startloc,elementno,self._str(content = self.__strattrs(ansi),brackets = 1,slash = 1,ansi = ansi)])
		else:
			v.append([nest,self.startloc,elementno,self._str(content = self.__strattrs(ansi),brackets = 1,ansi = ansi)])
			i = 0
			for child in self:
				v = v + child._doreprtree(nest+1,elementno + [i],ansi)
				i = i + 1
			if self.startloc is None:
				v.append([nest,self.startloc,elementno,self._str(brackets = 1,slash = -1,ansi = ansi)])
			else:
				v.append([nest,self.endloc,elementno,self._str(brackets = 1,slash = -1,ansi = ansi)])
		return v

	def asString(self,XHTML = None):
		v = []
		v.append("<")
		v.append(self.elementname) # requires that the element is registered via registerElement()
		for attr in self.attrs.keys():
			v.append(' ')
			v.append(attr)
			value = self[attr]
			if len(value):
				v.append('="')
				v.append(value.asString(XHTML))
				v.append('"')
		if len(self):
			if self.empty:
				raise EmptyElementWithContentError(self)
			v.append(">")
			v.append(self.content.asString(XHTML))
			v.append("</")
			v.append(self.elementname)
			v.append(">")
		else:
			if XHTML is None:
				XHTML = outputXHTML
			if XHTML in (0,1):
				if self.empty:
					if XHTML==1:
						v.append(" /")
					v.append(">")
				else:
					v.append("></")
					v.append(self.elementname)
					v.append(">")
			elif XHTML == 2:
				v.append("/>")
			else:
				raise ValueError("XHTML must be 0, 1, 2 or None")

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
				raise AttributeNotFoundError(self,index)
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
				raise IllegalAttributeError(self,index)
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

	def hasAttr(self,attr):
		"""
		S.hasAttr(attr) -> bool

		returns, if S has an attribute named attr.
		"""

		return self.attrs.has_key(attr)

	def getAttr(self,attr,default = None):
		"""
		S.getAttr(attr,default = None) -> node

		works like the method get() of dictionaries,
		it returns the attribute with the name attr, or if S has no
		such attribute, default (after converting it to a node and
		wrapping it into the appropriate attribute node.)
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

	def addImageSizeAttributes(self,imgattr,widthattr = "width",heightattr = "height"):
		"""
		add width and height attributes to the element for the image that can be found in the attribute
		<argref>imgattr</argref>. If the attributes are already there, they are taken as a formatting
		template with the size passed in as a dictionary with the keys <code>"width"</code> and <code>"height"</code>,
		i.e. you could make your image twice as wide with <code>width="%(width)d*2"</code>.
		"""

		if self.hasAttr(imgattr):
			size = self[imgattr].ImageSize()
			sizedict = { "width": size[0], "height": size[1] }
			if size is not None: # the size was retrieved so we can use it
				if self.hasAttr(widthattr):
					try:
						self[widthattr] = eval(self[widthattr].asPlainString() % sizedict)
					except:
						raise ImageSizeFormatError(self,widthattr)
				else:
					self[widthattr] = size[0]
				if self.hasAttr(heightattr):
					try:
						self[heightattr] = eval(self[heightattr].asPlainString() % sizedict)
					except:
						raise ImageSizeFormatError(self,heightattr)
				else:
					self[heightattr] = size[1]

	def compact(self):
		node = self.__class__(self.content.compact())
		for attr in self.attrs.keys():
			node[attr] = self[attr].compact()
		return self._decorateNode(node)

	def findNodes(self,type = None,subtype = 0,searchchildren = 0,searchattrs = 0,attrs = None):
		node = Frag()
		if searchattrs:
			for attr in self.attrs.keys():
				node.extend(self[attr].findNodes(type,subtype,searchchildren,searchattrs,attrs))
		node.extend(self.content.findNodes(type,subtype,searchchildren,searchattrs,attrs))
		return node

class Null(Node):
	"""
	node that does not contain anything.
	"""

	def asHTML(self):
		return self

	clone = compact = asHTML

	def asString(self,XHTML = None):
		return ""

	def _dorepr(self,ansi = None):
		return self._str(slash = 1,ansi = ansi)

	def _doreprtree(self,nest,elementno,ansi = None):
		return [[nest,self.startloc,elementno,self._dorepr(ansi)]]

Null = Null() # Singleton, the Python way

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

class NumberAttr(Attr):
	"""
	Attribute class that is used for normal number attributes.
	"""

class IntAttr(NumberAttr):
	"""
	Attribute class that is used for normal integer attributes.
	"""

class FloatAttr(NumberAttr):
	"""
	Attribute class that is used for normal float attributes.
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

	XSC has one additional feature, path markers (these are directory names starting with *).
	An URL starting with a path marker is relative to the directory marked with the same path
	marker in the appropriate base URL.

	With this feature you don't have to remember how deeply you've nested your XSC file tree, you
	can specify a file from everywhere via "*/dir/to/file.xsc". XSC will change this to an URL
	that correctly locates the file (e.g. "../../../dir/to/file.xsc", when you're currenty nested three levels
	deep in a different directory than "dir".

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
		return strURL(self.asString(),ansi = ansi)

	def asString(self,XHTML = None):
		return Text(self.forOutput().asString()).asString(XHTML)

	def asHTML(self):
		node = Attr.asHTML(self)
		node.base = self.base.clone()
		return node

	def clone(self):
		node = Attr.clone(self)
		node.base = self.base.clone()
		return node

	def compact(self):
		node = Attr.compact(self)
		node.base = self.base.clone()
		return node

	def asURL(self):
		return URL(Attr.asPlainString(self))

	def asPlainString(self):
		return self.asURL().asString()

	def forInput(self):
		url = self.base + self.asURL()
		if url.scheme == "server":
			url = url.relativeTo(URL(scheme = "http",server = xsc.server))
		return url

	def forOutput(self):
		return self.asURL().relativeTo(xsc.filename[-1])

	def ImageSize(self):
		"""
		returns the size of an image as a tuple or None if the image shouldn't be read
		"""

		url = self.forInput()
		size = None
		if xsc.isRetrieve(url):
			try:
				filename,headers = urllib.urlretrieve(url.asString())
				if headers.maintype == "image":
					img = Image.open(filename)
					size = img.size
					del img
				urllib.urlcleanup()
			except IOError:
				urllib.urlcleanup()
				raise FileNotFoundError(self.startloc,url)
		return size

	def FileSize(self):
		"""
		returns the size of a file in bytes or None if the file shouldn't be read
		"""

		url = self.forInput()

		size = None
		if xsc.isRetrieve(url):
			try:
				filename,headers = urllib.urlretrieve(url.asString())
				size = os.stat(filename)[stat.ST_SIZE]
				urllib.urlcleanup()
			except IOError:
				urllib.urlcleanup()
				raise FileNotFoundError(self.startloc,url)
		return size

###
###
###

entitiesByNumber = [ ]

for i in xrange(65536):
	entitiesByNumber.append([])

entitiesByName = {}

###
###
###

def registerElement(element,namespacename,elementname = None):
	"""
	<par noindent>registers the element handler class <argref>element</argref> to be used
	for elements with the appropriate name.
	The element will be registered in the namespace <argref>namespacename</argref> and the element name
	<argref>elementname</argref>. If <argref>elementname</argref> is <code>None<code>, the lowercase name
	of the class will be used (to help prevent conflicts between Python keywords and class names
	(e.g. for the HTML element del).</par>
	<par>This function sets the class member <code>elementname</code> to the element name.
	If this member is already present, the above method for determining the element name
	will be skipped, and this member will be used.</par>
	"""
	element.namespacename = namespacename
	if hasattr(element,elementname):
		elementname = element.elementname
	else:
		if elementname is None:
			elementname = string.lower(element.__name__)
		element.elementname = elementname

	if _elementHandlers.has_key(elementname):
		_elementHandlers[elementname][namespacename] = element
	else:
		_elementHandlers[elementname] = { namespacename : element }

def registerAllElements(dict,namespacename):
	"""
	registerAllElements(dict,namespacename)

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

def registerEntity(name,value):
	"""
	registerEntity(name,value)

	registers the value value (which will be converted to an XSC node)
	as an entity with the name name.
	"""
	newvalue = ToNode(value)
	if isinstance(newvalue,CharRef):
		entitiesByNumber[newvalue.content].append(name)
	entitiesByName[name] = newvalue

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

class Location:
	"""
	specifies a position in an XML file.
	"""

	def __init__(self,url = None,row = None,col = None):
		self.url = url
		self.row = row
		self.col = col

	def __str__(self):
		if self.url is not None:
			s = '"' + str(self.url) + '" ('
			s = s + "L" + str(self.row)
			if self.col is not None:
				s = s + "C" + str(self.col)
			s = s + ")"
			return s
		else:
			return ""

	def __repr__(self):
		return "Location(" + repr(self.url) + "," + repr(self.row) + "," + repr(self.col) + ")"

###
###
###

class XSC:
	"""
	contains the parser and the options and functions for handling XML files
	"""

	def __init__(self):
		self.filename = [ URL("*/") ]
		self.server = "localhost"
		self.reprtree = 1

	def pushURL(self,url):
		url = URL(url)
		if len(self.filename):
			url = self.filename[-1] + url
		self.filename.append(url)

	def popURL(self):
		self.filename.pop()

	def handle_special(self,data):
		if data[:7] == "DOCTYPE":
			self.__appendNode(DocType(data[8:]))

	def handle_proc(self,target,data):
		self.__appendNode(ProcInst(target,data))

	def handle_charref(self,name):
		try:
			if name[0] == 'x':
				code = string.atoi(name[1:],16)
			else:
				code = int(name)
		except ValueError:
			raise MalformedCharRefError(self.__here(),name)

		self.__appendNode(CharRef(code))

	def handle_entityref(self,name):
		try:
			self.__appendNode(entitiesByName[name].clone())
		except KeyError:
			raise UnknownEntityError(self.__here(),name)

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
			raise IllegalElementError(self.__here(),name)
		if name[0] is None: # element name was unqualified ...
			if len(elementsfornamespaces.keys())==1: # ... and there is exactly one element with this name => use it
				element = elementsfornamespaces.values()[0]
			else:
				raise AmbiguousElementError(-1,name) # there is more than one
		else: # element name was qualified with a namespace
			try:
				element = elementsfornamespaces[name[0]]
			except KeyError:
				raise IllegalElementError(self.__here(),name) # elements with this name were available, but none in this namespace
		return element

	def finish_starttag(self,name,attrs):
		node = self.elementFromName(name)()
		for name,value in attrs:
			node[name] = self.__string2Fragment(value)
		self.__appendNode(node)
		self.__nesting.append(node) # push new innermost element onto the stack

	def finish_endtag(self,name):
		element = self.elementFromName(name)
		currentelement = self.__nesting[-1].__class__
		if element != currentelement:
			raise IllegalElementNestingError(self.__here(),currentelement,element)
		self.__nesting[-1].endloc = self.__here()
		self.__nesting.pop() # pop the innermost element off the stack

	def handle_data(self,data):
		if data != "":
			self.__appendNode(Text(data))

	def handle_comment(self,data):
		self.__appendNode(Comment(data))

	def __parseLines(self,lines):
		self.__nesting = [ Frag() ]
		parser = sgmlop.SGMLParser()
		parser.register(self)
		self.lineno = 1
		for line in lines:
			parser.feed(line)
			self.lineno = self.lineno + 1
		parser.close()
		return self.__nesting[0]

	def parseString(self,text):
		"""
		Parses a string and returns the resulting XSC
		"""
		self.pushURL("STRING")
		lines = string.split(text,"\n")
		for i in xrange(len(lines)):
			lines[i] = lines[i] + "\n"
		element = self.__parseLines(lines)
		self.popURL()
		return element

	def parse(self,url):
		"""
		Reads and parses a XML file from an URL and returns the resulting XSC
		"""
		self.pushURL(url)
		lines = self.filename[-1].readlines()
		element = self.__parseLines(lines)
		self.popURL()
		return element

		# our nodes do not have a parent link, therefore we have to store the active path through the tree in a stack (which we call nesting, because stack is already used by the base class (there is no base class anymore, but who cares))
		# after we've finished parsing, the Frag that we put at the bottom of the stack will be our document root
		return self.__nesting[0]

	def __repr__(self):
		return '<xsc filename="' + self.filename + '" server="' + self.server + '" retrieveremote=' + [ 'no' , 'yes' ][retrieveremote] + '" retrievelocal=' + [ 'no' , 'yes' ][retrievelocal] + '>'

	def isRetrieve(self,url):
		remote = url.isRemote()
		if (retrieveremote and remote) or (retrievelocal and (not remote)):
			return 1
		else:
			return 0

	def __here(self):
		return Location(self.filename[-1],self.lineno)

	def __appendNode(self,node):
		node.startloc = self.__here()
		last = self.__nesting[-1]
		if len(last) and isinstance(last[-1],Text):
			if isinstance(node,Text):
				last[-1].content = last[-1].content + node.content
				return
			elif isinstance(node,CharRef) and node.content < 256: # 256 test will disappear in Python 1.6 with SXP
				last[-1].content = last[-1].content + chr(node.content)
				return
		last.append(node) # add the new node to the content of the innermost element (or fragment)

	def __string2Fragment(self,text):
		"""
		parses a string that might contain entities into a fragment
		with text nodes and character references (and other stuff,
		if the string contains entities).
		"""
		node = Frag()
		while 1:
			try:
				i = string.index(text,"&")
				if i != 0:
					node.append(text[:i])
					text = text[i:]
				try:
					i = string.index(text,";")
					if text[1] == "#":
						if text[2] == "x":
							node.append(CharRef(string.atoi(text[3:i],16)))
						else:
							node.append(CharRef(int(text[2:i])))
					else:
						try:
							node.append(entitiesByName[text[1:i]])
						except KeyError:
							raise UnknownEntityError(self.__here(),text[1:i])
					text = text[i+1:]
				except ValueError:
					raise MalformedCharRefError(self.__here(),text)
			except ValueError:
				if len(text):
					node.append(text)
				break
		return node

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

xsc = XSC()

def make():
	"""
	use XSC as a compiler script, i.e. read an input file from args[1]
	and writes it to args[2]
	"""

	(options,args) = getopt.getopt(sys.argv[1:],"i:o:",["include=","output="])

	globaloutname = URL("*/")
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
			sys.stderr.write('XSC: converting ' + repr(str(inname)) + ' to ' + repr(str(outname)) + ' ...')
			e_in = xsc.parse(inname)
			xsc.pushURL(inname)
			e_out = e_in.asHTML()
			s_out = e_out.asString()
			__forceopen(outname.asString(),"wb").write(s_out)
			sys.stderr.write(" " + _stransi("1",str(len(s_out))) + "\n")
			xsc.popURL()
	else:
		sys.stderr.write("XSC: no files to convert.\n")

if __name__ == "__main__":
	make()
