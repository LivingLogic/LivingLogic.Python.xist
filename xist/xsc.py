#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
XIST is a HTML preprocessor/generator and an XML transformation engine.
It is easily extensible with new XML elements, allows embedding
Python code in XML files and works together with httpdapy/mod_python.

It was written as a replacement for the HTML preprocessor HSC
(http://www.giga.or.at/~agi/hsc/), and borrows some features and ideas from it.

It also borrows the basic ideas (XML/HTML elements as Python objects)
from HTMLgen (http://starship.python.net/crew/friedrich/HTMLgen/html/main.html)
or HyperText (http://dustman.net/andy/python/HyperText/)

XIST is based on XML, so you have two choices when constructing
your hierarchical tree of HTML objects: You can directly construct
it, like HTMLgen and HyperText do, as a tree of Python objects or
you can get a tree by parsing an XML file.

For every HTML element there exists a corresponding class, that
has a constructor of the form
	class(*content, **attrs),
so constructing an HTML element works like this:
	e = html.div(
		"Go to ",
		html.a("Python.org", href="http://www.python.org/"),
		"!"
	)

This object can be converted to a printable unicode string with
the method asString():
	print e.asString()

In XIST you're not limited to the HTML element types.
You can define your own! To be able to convert these
new element types to a HTML object tree, you must implement
the method convert, and you must derive your class from
xsc.Element as in the following example:

	class cool(xsc.Element):
		empty = 1

		def convert(self, converter=None):
			return html.b("Python is cool!")

Using this element is as simple as this:
	e = cool()
	print e.convert().asString()

(The additional argument converter allows you to implement
different processing modes or stages)

The class variable empty in the above example specifies
that the element type has an empty content model (like <br/>
or <img/>).

To be able to use your own classes in XML files, you have
to tell the parser about them. This is done with
namespace objects (see the docstring for the Namespace class).
What you have to do is construct a namespace object for all the
elements in your module:
namespace = xsc.Namespace("foo", "http://www.foo.net/dtd/foo.dtd", vars())


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
generate new URLs in their convert() methods. As this
conversion happens sometime after the file is parsed, the URL
of the file is already gone from the stack. But of course
you will want new URLs to be interpreted relative to the file
name in which the element was encountered. So you have to push
the URL to the stack manually. Of course all these steps can
be combined into the following:
	url = "foo/bar/baz.xml"
	element = xsc.xsc.parse(url)
	xsc.xsc.pushURL(url)
	str = element.convert().asString()
	xsc.xsc.popURL()

Automatic generation of image size attributes
=============================================
The module special contains an element autoimg, that extends
html.img. When converted to HTML via the convert() method the
size of the image will be determined and the HEIGHT
and WIDTH attributes will be set accordingly.

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
XIST support two new processing instruction targets: xsc:exec and
xsc:eval. The content of xsc:exec will be executed when the processing
instruction node is instantiated, i.e. when the XML file is parsed,
so anything you do there will be available afterwards.

The result of a call to convert() for a xsc:eval processing instruction
is whatever the Python code in the content returns. For example, consider
the following XML file:
	<?xsc:exec
	# sum
	def gauss(top=100):
		sum = 0
		for i in xrange(top+1):
			sum += i
		return sum
	?>
	<b><?xsc:eval return gauss()?></b>
Parsing this file and converting it to HTML results in the following:
	<b>5050</b>

For further information see the class ProcInst and it's two derived
classes Eval and Exec.

Requirements
============
XSC requires Python 2.0b2.

XSC uses the Python XML package for parsing XML files, so you'll
need the Python XML package (at least 0.5.5.1)
(available from http://pyxml.sourceforge.net/).

To determine image sizes, XSC needs the Python Imaging library
(available from http://www.pythonware.com/products/pil/).
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import os, string, types, sys, stat, urllib

import Image

from xml.sax import saxutils

from xist import procinst, url, presenters, publishers, error, options, utils, helpers

###
### helpers
###

def nodeName(nodeClass):
	"""
	returns a list with the namespacename, the elementname and the emptyness of the node.
	Note that for this to work the element has to be registered.
	"""
	try:
		namespacename = nodeClass.namespace.prefix
	except AttributeError:
		namespacename = "xsc" # this is (hopefully) an XSC class
	try:
		elementname = nodeClass.name
	except AttributeError:
		elementname = nodeClass.__name__

	return [namespacename, elementname, nodeClass.empty]

def ToNode(value):
	"""
	<par noindent>convert the <argref>value</argref> passed in to a XSC <classref>Node</classref>.</par>

	<par>If <argref>value</argref> is a tuple or list, it will be (recursively) converted
	to a <classref>Frag</classref>. Integers, strings, etc. will be converted to a <classref>Text</classref>.
	If <argref>value</argref> is a <classref>Node</classref> already, nothing will be done.
	In the case of <code>None</code> the XSC Null (<code>xsc.Null</code>) will be returned).
	Anything else raises an exception.</par>
	"""
	t = type(value)
	if t is types.InstanceType:
		if isinstance(value, Frag):
			l = len(value)
			if l==1:
				return ToNode(value[0]) # recursively try to simplify the tree
			elif l==0:
				return Null
			elif isinstance(value, Attr):
				return Frag(*value) # repack the attribute in a fragment, and we have a valid XSC node
			else:
				return value
		elif isinstance(value, Node):
			return value
		elif isinstance(value, url.URL):
			return Text(value.asString())
	elif t in (types.StringType, types.UnicodeType, types.IntType, types.LongType, types.FloatType):
		return Text(value)
	elif t is types.NoneType:
		return Null
	elif t in (types.ListType, types.TupleType):
		return Frag(*value)
	raise errors.IllegalObjectError(-1, value) # none of the above, so we throw and exception

class Node:
	"""
	base class for nodes in the document tree. Derived classes must
	implement <methodref>convert</methodref> and may implement
	<methodref>publish</methodref> and <methodref>asPlainString</methodref>.
	"""

	empty = 1

	# location of this node in the XML file (will be hidden in derived classes, but is
	# specified here, so that no special tests are required. In derived classes
	# this will be set by the parser)
	startLoc = None
	endLoc = None

	# specifies if a prefix should be presented or published. Can be 0 or 1 or None
	# which mean use the default
	presentPrefix = None
	publishPrefix = None

	# specifies that this class should be registered in a namespace
	# this won't be used for all the DOM classes (Element, ProcInst etc.) themselves but only for derived classes
	# i.e. Node, Element etc. will never be registered
	register = 1

	def __repr__(self):
		return self.repr(presenters.defaultPresenterClass())

	def _str(self, content=None, brackets=1, slash=None, ansi=None):
		return _strNode(self.__class__, content, brackets, slash, ansi)

	def clone(self):
		"""
		returns an identical clone of the node and it's children.
		"""
		return Null

	def repr(self, presenter=None):
		if presenter is None:
			presenter = presenters.defaultPresenterClass()
		presenter.beginPresentation()
		self.present(presenter)
		return presenter.endPresentation()

	def reprtree(self, presenter=None):
		if presenter is None:
			presenter = presenters.Presenter()
		nest = 0
		lines = self._doreprtree(nest, [], presenter=presenter)
		lenloc = 0
		lenelementno = 0
		for line in lines: # (nest, location, elementno, string)
			if line[1] is not None: # convert location to a string
				line[1] = str(line[1])
			else:
				line[1] = ""
			line[2] = ".".join(map(str, line[2])) # convert element number to a string
			line[3] = strTab(line[0]) + line[3] # add indentation
			lenloc = max(lenloc, len(line[1]))
			lenelementno = max(lenelementno, len(line[2]))

		return "".join([ "%*s %-*s %s\n" % (lenloc, line[1], lenelementno, line[2], line[3]) for line in lines ])

	def present(self, presenter):
		pass

	def _doreprtree(self, nest, elementno, presenter):
		# returns an array containing arrays consisting of the
		# (nestinglevel, location, elementnumber, string representation) of the nodes
		return [[nest, self.startLoc, elementno, self._dorepr(presenter)]]

	def convert(self, converter=None):
		"""
		<par noindent>returns a version of this node and it's content converted to HTML,
		so when you define your own element classes you should overwrite <methodref>convert</methodref>.</par>

		<par>E.g. when you want to define an element that packs it's content into an HTML
		bold element, do the following:

		<pre>
		class foo(xsc.Element):
			empty = 0

			def convert(self, converter=None):
				return html.b(self.content).convert(converter)
		</pre>
		</par>
		"""
		return Null

	def asPlainString(self):
		"""
		<par noindent>returns this node as a (unicode) string without any character references.
		Comments and processing instructions will be filtered out.
		For elements you'll get the element content.</par>

		<par>It might be useful to overwrite this function in your own
		elements. Suppose you have the following element:
		<pre>
		class caps(xsc.Element):
			empty = 0

			def convert(self, converter=None):
				return html.span(
					self.content.convert(converter),
					style="font-variant: small-caps;"
				)
		</pre>

		that renders its content in small caps, then it might be useful
		to define <methodref>asPlainString</methodref> in the following way:
		<pre>
		def asPlainString(self):
			return self.content.asPlainString().upper()
		</pre>

		<methodref>asPlainString</methodref> can be used everywhere, where
		a plain string representation of the node is required.
		<classref module="html">title</classref> uses this function on its content,
		so you can safely use HTML elements in your title elements (e.g. if your
		title is dynamically constructed from a DOM tree.)</par>
		"""
		return u""

	def asInt(self):
		"""
		returns this node converted to an integer.
		"""
		return int(self.asPlainString())

	def asFloat(self, decimal=".", ignore=""):
		"""
		returns this node converted to a float. <argref>decimal</argref>
		specifies which decimal separator is used in the value
		(e.g. <code>"."</code> (the default) or <code>","</code>).
		<argref>ignore</argref>specifies which character will be ignored.
		"""
		s = self.asPlainString()
		for c in ignore:
			s = string.replace(s, c, "")
		if decimal != ".":
			s = string.replace(s, decimal, ".")
		return float(s)

	def publish(self, publisher):
		"""
		<par noindent>generates unicode strings for the node, and passes
		the strings to the callable object <argref>publisher</argref>.</par>

		<par>The encoding and XHTML specification are taken from the <argref>publisher</argref>.</par>
		"""
		pass

	def asString(self, XHTML=None, publishPrefix=0):
		"""
		<par noindent>returns this element as a unicode string.</par>

		<par>For an explanation of <argref>XHTML</argref> and <argref>publishPrefix</argref> see <funcref>publish</funcref>.</par>
		"""
		publisher = publishers.StringPublisher(XHTML=XHTML, publishPrefix=publishPrefix)
		self.publish(publisher)
		return publisher.asString()

	def asBytes(self, base=None, encoding=None, XHTML=None, publishPrefix=0):
		"""
		<par noindent>returns this element as a byte string suitable for writing
		to an HTML file or printing from a CGI script.</par>

		<par>For the parameters see <funcref>publish</funcref>.</par>
		"""
		publisher = publishers.BytePublisher(base=base, encoding=encoding, XHTML=XHTML, publishPrefix=publishPrefix)
		self.publish(publisher)
		return publisher.asBytes()

	def write(self, file, base=None, encoding=None, XHTML=None, publishPrefix=0):
		"""
		<par noindent>writes the element to the file like
		object <argref>file</argref></par>

		<par>For the parameters see <funcref>publish</funcref>.</par>
		"""
		publisher = publishers.FilePublisher(file, base=base, encoding=encoding, XHTML=XHTML, publishPrefix=publishPrefix)
		self.publish(publisher)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		"""
		<par noindent>returns a fragment which contains child elements of this node.</par>

		<par>If you specify <argref>type</argref> as the class of an XSC node only nodes
		of this class will be returned. If you pass a list of classes, nodes that are an
		instance of one of the classes will be returned.</par>

		<par>If you set <argref>subtype</argref> to <code>1</code> nodes that are a
		subtype of <argref>type</argref> will be returned too.</par>

		<par>If you pass a dictionary as <argref>attrs</argref> it has to contain
		string pairs and is used to match attribute values for elements. To match
		the attribute values their <code>asPlainString()</code> representation will
		be used. You can use <code>None</code> as the value to test that the attribute
		is set without testing the value.</par>

		<par>Additionally you can pass a test function in <argref>test</argref>, that
		returns <code>1</code>, when the node passed in has to be included in the
		result and <code>0</code> otherwise.</par>

		<par>If you set <argref>searchchildren</argref> to <code>1</code> not only the
		immediate children but also the grandchildren will be searched for nodes
		matching the other criteria.</par>

		<par>If you set <argref>searchattrs</argref> to <code>1</code> the attributes
		of the nodes (if <argref>type</argref> is <classref>Element</classref> or one
		of its subtypes) will be searched too.</par>

		<par>Note that the node has to be of type <classref>Element</classref>
		(or a subclass of it) to match <argref>attrs</argref>.</par>
		"""
		return Frag()

	def compact(self):
		"""
		returns a version of <self/>, where textnodes or character references that contain
		only linefeeds are removed, i.e. potentially needless whitespace is removed.
		"""
		return Null

	def _matchesAttrs(self, attrs):
		if attrs is None:
			return 1
		else:
			if isinstance(self, Element):
				for attr in attrs.keys():
					if (not self.hasAttr(attr)) or ((attrs[attr] is not None) and (self[attr].asPlainString() != attrs[attr])):
						return 0
				return 1
			else:
				return 0

	def _matches(self, type_, subtype, attrs, test):
		res = 1
		if type_ is not None:
			if type(type_) not in [types.ListType, types.TupleType]:
				type_ = (type_,)
			for t in type_:
				if subtype:
					if isinstance(self, t):
						res = self._matchesAttrs(attrs)
						break
				else:
					if self.__class__ == t:
						res = self._matchesAttrs(attrs)
						break
			else:
				res = 0
		else:
			res = self._matchesAttrs(attrs)
		if res and (test is not None):
			res = test(self)
		return res

	def _doreprtreeMultiLine(self, nest, elementno, head, tail, text, formatter, extraFirstLine, presenter):
		lines = text.split("\n")
		l = len(lines)
		if l>1 and extraFirstLine:
			lines.insert(0, "")
			l += 1
		v = []
		for i in xrange(l):
			mynest = nest
			s = lines[i]
			while len(s) and s[0] == "\t":
				mynest += 1
				s = s[1:]
			s = formatter(s)
			if i == 0:
				s = head + s
			if i == l-1:
				s += tail
			v.append([mynest, self._getLoc(i), elementno, s])
		return v

	def _getLoc(self, relrow):
		"""
		Return a location that is <argref>relrow</argref> rows further down than
		the starting location for this node. Returns <code>None</code> if the
		location is unknown.
		"""

		if self.startLoc is None:
			return None
		else:
			return Location(locator=self.startLoc, lineNumber=self.startLoc.getLineNumber()+relrow)

	def _decorateNode(self, node):
		"""
		decorate the node <argref>node</argref> with the same location information as <self/>.
		"""

		node.startLoc = self.startLoc
		node.endLoc = self.endLoc
		return node

class StringMixIn:
	"""
	provides nearly the same functionality as <classref>UserString</classref>, but omits
	a few methods (<code>__str__</code> etc.)
	"""
	def __init__(self, content):
		self._content = utils.stringFromCode(content)

	def __iadd__(self, other):
		other = ToNode(other)
		return self.__class__(self._content+other._content)

	__add__ = __iadd__

	def __radd__(self, other):
		other = ToNode(other)
		return self.__class__(other._content+self._content)

	def __imul__(self, n):
		return self.__class__(self._content*n)

	__mul__ = __imul__

	def __cmp__(self, other):
		if isinstance(other, self.__class__):
			return cmp(self._content, other._content)
		else:
			return cmp(self._content, other)

	def __contains__(self, char):
		return utils.stringFromCode(char) in self._content

	def __hash__(self):
		return hash(self._content)

	def __len__(self):
		return len(self._content)

	def __getitem__(self, index):
		return self._content[index]

	def __getslice__(self, index1, index2):
		return self.__class__(self._content[index1:index2])

	def capitalize(self):
		return self.__class__(self._content.capitalize())

	def center(self, width):
		return self.__class__(self._content.center(width))

	def count(self, sub, start=0, end=sys.maxint):
		return self._content.count(sub, start, end)

	def endswith(self, suffix, start=0, end=sys.maxint):
		return self._content.endswith(utils.stringFromCode(suffix), start, end)

	def find(self, sub, start=0, end=sys.maxint):
		return self._content.find(utils.stringFromCode(sub), start, end)

	def index(self, sub, start=0, end=sys.maxint):
		return self._content.index(utils.stringFromCode(sub), start, end)

	def isalpha(self):
		return self._content.isalpha()

	def isalnum(self):
		return self._content.isalnum()

	def isdecimal(self):
		return self._content.isdecimal()

	def isdigit(self):
		return self._content.isdigit()

	def islower(self):
		return self._content.islower()

	def isnumeric(self):
		return self._content.isnumeric()

	def isspace(self):
		return self._content.isspace()

	def istitle(self):
		return self._content.istitle()

	def join(self, frag):
		return frag.withSeparator(self)

	def isupper(self):
		return self._content.isupper()

	def ljust(self, width):
		return self.__class__(self._content.ljust(width))

	def lower(self):
		return self.__class__(self._content.lower())

	def lstrip(self):
		return self.__class__(self._content.lstrip())

	def replace(self, old, new, maxsplit=-1):
		return self.__class__(self._content.replace(utils.stringFromCode(old), utils.stringFromCode(new), maxsplit))

	def rfind(self, sub, start=0, end=sys.maxint):
		return self._content.rfind(utils.stringFromCode(sub), start, end)

	def rindex(self, sub, start=0, end=sys.maxint):
		return self._content.rindex(utils.stringFromCode(sub), start, end)

	def rjust(self, width):
		return self.__class__(self._content.rjust(width))

	def rstrip(self):
		return self.__class__(self._content.rstrip())

	def split(self, sep=None, maxsplit=-1):
		return Frag(self._content.split(sep, maxsplit))

	def splitlines(self, keepends=0):
		return Frag(self._content.splitlines(keepends))

	def startswith(self, prefix, start=0, end=sys.maxint):
		return self._content.startswith(utils.stringFromCode(prefix), start, end)

	def strip(self):
		return self.__class__(self._content.strip())

	def swapcase(self):
		return self.__class__(self._content.swapcase())

	def title(self):
		return self.__class__(self._content.title())

	def translate(self, *args):
		return self.__class__(self._content.translate(*args))

	def upper(self):
		return self.__class__(self._content.upper())

class Text(Node, StringMixIn):
	"""
	text node. The characters <, >, & and " will be "escaped" with the
	appropriate character entities.
	"""

	def __init__(self, content=""):
		if isinstance(content, Text):
			content = content._content
		StringMixIn.__init__(self, content)

	def convert(self, converter=None):
		return self

	clone = convert

	def asPlainString(self):
		return self._content

	def publish(self, publisher):
		publisher.publishText(self._content)

	def present(self, presenter):
		presenter.presentText(self)

	def _doreprtree(self, nest, elementno, presenter):
		lines = self._content.split("\n")
		if len(lines) and lines[-1] == "":
			del lines[-1]
		v = []
		for i in xrange(len(lines)):
			s = presenter.strQuote() + presenter.strText(self.__strtext(1, lines[i], presenter)) + presenter.strQuote()
			v.append([nest, self._getLoc(i), elementno, s])
		return v

	def compact(self):
		if self._content.isspace():
			return Null
		else:
			return self

class Frag(Node):
	"""
	A fragment contains a list of nodes and can be used for dynamically constructing content.
	The member content of an Element is a Frag.
	"""

	empty = 0

	def __init__(self, *content):
		self.__content = []
		for child in content:
			self.extend(child)

	def convert(self, converter=None):
		node = self.__class__() # virtual constructor => attributes (which are derived from Frag) will be handled correctly)
		for child in self.__content:
			convertedchild = child.convert(converter)
			assert isinstance(convertedchild, Node), "the convert method returned the illegal object %r when converting %r" % (convertedchild, child)
			if convertedchild is not Null:
				node.__content.append(convertedchild)
		return self._decorateNode(node)

	def clone(self):
		node = self.__class__() # virtual constructor => attributes (which are derived from Frag) will be handled correctly)
		node.__content = [ child.clone() for child in self.__content ]
		return self._decorateNode(node)

	def present(self, presenter):
		presenter.presentFrag(self)

	def _doreprtree(self, nest, elementno, presenter):
		v = []
		if len(self):
			v.append([nest, self.startLoc, elementno, self._str(brackets=1, ansi=presenter.ansi)])
			i = 0
			for child in self.__content:
				v.extend(child._doreprtree(nest+1, elementno + [i], presenter))
				i += 1
			v.append([nest, self.endLoc, elementno, self._str(brackets=1, ansi=presenter.ansi, slash=-1)])
		else:
			v.append([nest, self.startLoc, elementno, self._str(brackets=1, ansi=presenter.ansi, slash=1)])
		return v

	def asPlainString(self):
		return u"".join([ child.asPlainString() for child in self.__content ])

	def publish(self, publisher):
		for child in self.__content:
			child.publish(publisher)

	def __getitem__(self, index):
		"""
		Return the <argref>index</argref>'th node for the content of the fragment.
		If <argref>index</argref> is a list <code>__getitem__</code> will work
		recursively. If <argref>index</argref> is empty, <self/> will be returned.
		"""
		if type(index) in (types.IntType, types.LongType):
			return self.__content[index]
		elif type(index) is types.ListType:
			node = self
			for subindex in index:
				node = node[subindex]
			return node
		else:
			raise TypeError("index must be int, long or string not %s" % type(index).__name__)

	def __setitem__(self, index, value):
		"""
		Allows you to replace the <argref>index</argref>'th content node of the fragment
		with the new value <argref>value</argref> (which will be converted to a node).
		If  <argref>index</argref> is a list <code>__setitem__</code> will be applied
		to the innermost index after traversing the rest of <argref>index</argref> recursively.
		If <argref>index</argref> is empty the call will be ignored.
		"""
		value = ToNode(value)
		try:
			self.__content[index] = value
		except TypeError: # assume index is a list
			if len(index):
				node = self
				for subindex in index[:-1]:
					node = node[subindex]
				node[index[-1]] = value

	def __delitem__(self, index):
		"""
		Remove the <argref>index</argref>'th content node from the fragment.
		If <argref>index</argref> is a list, the innermost index will be deleted,
		after traversing the rest of <argref>index</argref> recursively.
		If <argref>index</argref> is empty the call will be ignored.
		"""
		try:
			del self.__content[index]
		except TypeError: # assume index is a list
			if len(index):
				node = self
				for subindex in index[:-1]:
					node = node[subindex]
				del node[index[-1]]

	def __getslice__(self, index1, index2):
		"""
		returns a slice of the content of the fragment
		"""
		node = self.__class__()
		node.__content = self.__content[index1:index2]
		return node

	def __setslice__(self, index1, index2, sequence):
		"""
		replaces a slice of the content of the fragment
		"""
		self.__content[index1:index2] = map(ToNode, sequence)

	def __delslice__(self, index1, index2):
		"""
		removes a slice of the content of the fragment
		"""
		del self.__content[index1:index2]

	def __len__(self):
		"""
		return the number of children
		"""
		return len(self.__content)

	def append(self, *others):
		"""
		appends all items in <argref>others</argref> to <self/>.
		"""
		for other in others:
			newother = ToNode(other)
			if newother is not Null:
				self.__content.append(newother)

	def insert(self, index, *others):
		"""
		inserts all items in <argref>others</argref> at the position <argref>index</argref>.
		(this is the same as <code><self/>[<argref>index</argref>:<argref>index</argref>] = <argref>others</argref></code>)
		"""
		for other in others:
			newother = ToNode(other)
			if newother is not Null:
				self.__content.insert(index, newother)
				index += 1

	def extend(self, *others):
		"""
		extends this fragment by all items in <argref>others</argref>.
		"""
		for other in others:
			newother = ToNode(other)
			if isinstance(newother, Frag):
				self.__content.extend(newother)
			elif newother is not Null:
				self.__content.append(newother)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		for child in self.__content:
			if child._matches(type, subtype, attrs, test):
				node.append(child)
			if searchchildren:
				node.extend(child.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def compact(self):
		node = self.__class__()
		for child in self.__content:
			newchild = child.compact()
			if newchild is not Null:
				node.__content.append(newchild)
		return self._decorateNode(node)

	def withSeparator(self, separator, clone=0):
		"""
		returns a version of <self/> with a separator node between the nodes of <self/>.

		if <code><argref>clone</argref>==0</code> one node will be inserted several times,
		if <code><argref>clone</argref>==1</code> clones of this node will be used.
		"""
		node = Frag()
		newseparator = ToNode(separator)
		for child in self.__content:
			if len(node):
				node.append(newseparator)
				if clone:
					newseparator = newseparator.clone()
			node.append(child)
		return node

class Comment(Node, StringMixIn):
	"""
	a comment node
	"""

	def __init__(self, content=""):
		StringMixIn.__init__(self, content)

	def convert(self, converter=None):
		return self

	def clone(self):
		return self

	compact = clone

	def present(self, presenter):
		presenter.presentComment(self)

	def _doreprtree(self, nest, elementno, presenter):
		head = presenter.strBracketOpen() + presenter.strExclamation() + presenter.strCommentMarker()
		tail = presenter.strCommentMarker() + presenter.strBracketClose()
		return self._doreprtreeMultiLine(nest, elementno, head, tail, self._content.encode(presenter.encoding), presenter.strCommentText, 0, presenter)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self.startLoc, self)
		if self._content.find(u"--")!=-1 or self._content[-1:]==u"-":
			raise errors.IllegalCommentContentError(self.startLoc, self)
		publisher.publish(u"<!--")
		publisher.publish(self._content)
		publisher.publish(u"-->")

class DocType(Node, StringMixIn):
	"""
	a document type node
	"""

	def __init__(self, content=""):
		StringMixIn.__init__(self, content)

	def convert(self, converter=None):
		return self

	def clone(self):
		return self

	compact = clone

	def present(self, presenter):
		presenter.presentDocType(self)

	def _doreprtree(self, nest, elementno, presenter):
		head = presenter.strBracketOpen() + presenter.strExclamation() + presenter.strDocTypeMarker() + " "
		tail = presenter.strBracketClose()
		return self._doreprtreeMultiLine(nest, elementno, head, tail, self._content.encode(presenter.encoding), presenter.strDocTypeText, 0, presenter)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self.startLoc, self)
		publisher.publish(u"<!DOCTYPE ")
		publisher.publish(self._content)
		publisher.publish(u">")

class ProcInst(Node, StringMixIn):
	"""
	<par noindent>There are two special targets available: <code>xsc:exec</code>
	and <code>xsc:eval</code> which will be handled by the
	special classes <classref>Exec</classref> and <classref>Eval</classref>
	derived from ProcInst.</par>

	<par>Processing instruction with the target <code>xml</code> will be 
	handled by the class <classref>XML</classref>.

	<par>All other processing instructions (PHP, etc.) will be handled
	by <classref>ProcInst</classref> itself and are passed through without
	processing of any kind.</par>
	"""

	def __init__(self, target, content=u""):
		self._target = utils.stringFromCode(target)
		StringMixIn.__init__(self, content)

	def convert(self, converter=None):
		return self

	def clone(self):
		return self

	compact = clone

	def present(self, presenter):
		presenter.presentProcInst(self)

	def _doreprtree(self, nest, elementno, presenter):
		head = presenter.strBracketOpen() + presenter.strQuestion() + presenter.strProcInst(self) + " "
		tail = presenter.strQuestion() + presenter.strBracketClose()
		return self._doreprtreeMultiLine(nest, elementno, head, tail, self._content.encode(presenter.encoding), presenter.strProcInstData, 1, presenter)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self.startLoc, self)
		if self._content.find(u"?>")!=-1:
			raise errors.IllegalProcInstFormatError(self.startLoc, self)
		publisher.publish(u"<?")
		if self.publishPrefix is not None:
			publishPrefix = self.publishPrefix
		else:
			publishPrefix = publisher.publishPrefix
		if publishPrefix:
			publisher.publish(self.namespace.prefix) # must be registered to work
			publisher.publish(u" ")
		publisher.publish(self._target)
		publisher.publish(u" ")
		publisher.publish(self._content)
		publisher.publish(u"?>")

class PythonCode(ProcInst):
	"""
	helper class
	"""

	register = 0 # don't register the class
	presentPrefix = 1
	publishPrefix = 1

	def _doreprtree(self, nest, elementno, encoding=None, ansi=None):
		head = strBracketOpen(ansi) + strQuestion(ansi) + strProcInstTarget(self._target, ansi) + " "
		tail = strQuestion(ansi) + strBracketClose(ansi)
		code = utils.Code(self._content, 1)
		code.indent()
		return self._doreprtreeMultiLine(nest, elementno, head, tail, code.asString().encode(encoding), strProcInstData, 1, presenter)

class Exec(PythonCode):
	"""
	<par noindent>here the content of the processing instruction is executed
	as Python code, so you can define and register XSC elements here.
	Execution is done when the node is constructed, so definitions made
	here will be available afterwards (e.g. during the rest of the
	file parsing stage). When converted to HTML such a node will result
	in an empty Null node.</par>

	<par>XSC processing instructions will be evaluated and executed in the
	namespace of the module procinst.</par>
	"""
	name = u"exec"

	def __init__(self, content=u""):
		ProcInst.__init__(self, u"exec", content)
		code = utils.Code(self._content, 1)
		exec code.asString() in procinst.__dict__ # requires Python 2.0b2 (and doesn't really work)

	def convert(self, converter=None):
		return Null # has been executed at construction time already, so we don't have to do anything here

class Eval(PythonCode):
	"""
	<par noindent>here the code will be executed when the node is converted to HTML
	as if it was the body of a function, so you can return an expression
	here. Although the content is used as a function body no indentation
	is neccessary or allowed. The returned value will be converted to a
	node and this resulting node will be converted to HTML.</par>

	<par>XSC processing instructions will be evaluated and executed in the
	namespace of the module <moduleref>procinst</moduleref>.</par>

	<par>Note that you should not define the symbol <code>__</code> in any of your XSC
	processing instructions, as it is used by XSC for internal purposes.</par>
	"""

	name = u"eval"

	def __init__(self, content=u""):
		ProcInst.__init__(self, u"eval", content)

	def convert(self, converter=None):
		"""
		Evaluates the code. The <argref>converter</argref> argument will be available
		under the name <code>converter</code> as an argument.
		"""
		code = utils.Code(self._content, 1)
		code.funcify()
		exec code.asString() in procinst.__dict__ # requires Python 2.0b2 (and doesn't really work)
		return ToNode(procinst.__(converter)).convert(converter)

class XML(ProcInst):
	"""
	XML header
	"""

	name = u"xml"
	presentPrefix = 0
	publishPrefix = 0

	def __init__(self, content=u""):
		ProcInst.__init__(self, u"xml", content)

	def __findAttr(self, name):
		startpos = self._content.find(name)
		if startpos != -1:
			startpos = startpos+len(name)
			while self._content[startpos].isspace():
				startpos += 1
			startpos += 1 # skip '='
			while self._content[startpos].isspace():
				startpos += 1
			char = self._content[startpos]
			startpos += 1
			endpos = self._content.find(char, startpos)
			if endpos != -1:
				return self._content[startpos:endpos]
		return None

	def publish(self, publisher):
		encodingfound = self.__findAttr(u"encoding")
		versionfound = self.__findAttr(u"version")
		standalonefound = self.__findAttr(u"standalone")
		if publisher.encoding != encodingfound: # if self has the wrong encoding specification (or none), we construct a new XML ProcInst and publish that (this doesn't lead to infinite recursion, because the next call will skip it)
			node = XML(u"version='" + versionfound + u"' encoding='" + publisher.encoding + u"'")
			if standalonefound is not None:
				node += u" standalone='" + standalonefound + u"'"
			node.publish(publisher)
			return
		ProcInst.publish(self, publisher)

class XML10(XML):
	"""
	XML header version 1.0
	"""
	register = 0 # don't register this ProcInst, because it will never be parsed from a file, this is just a convenience class

	def __init__(self):
		XML.__init__(self, 'version="1.0"')

class XMLStyleSheet(ProcInst):
	"""
	XML stylesheet declaration
	"""

	name = u"xml-stylesheet"
	presentPrefix = 0
	publishPrefix = 0

	def __init__(self, content=u""):
		ProcInst.__init__(self, u"xml-stylesheet", content)

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

	def __init__(self, *content, **attrs):
		"""
		positional arguments are treated as content nodes.

		keyword arguments and dictionaries are treated as attributes.
		"""
		self.content = Frag()
		self.attrs = {}
		for child in content:
			if type(child) is types.DictionaryType:
				for attr in child.keys():
					self[attr] = child[attr]
			else:
				self.extend(child)
		for attr in attrs.keys():
			self[attr] = attrs[attr]

	def append(self, *items):
		"""
		append(self, *items)

		appends to the content (see Frag.append for more info)
		"""

		self.content.append(*items)
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def insert(self, index, *items):
		"""
		insert(self, index, *items)

		inserts into the content (see Frag.insert for more info)
		"""
		self.content.insert(index, *items)
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def extend(self, *items):
		"""
		extend(self, items)

		extends the content (see Frag.extend for more info)
		"""
		self.content.extend(*items)
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def convert(self, converter=None):
		node = self.__class__() # "virtual" copy constructor
		node.content = self.content.convert(converter)
		for attrname in self.attrs.keys():
			attr = self.attrs[attrname]
			convertedattr = attr.convert(converter)
			assert isinstance(convertedattr, Node), "the convert method returned the illegal object %r when converting the attribute %s with the value %r" % (convertedchild, presenters.strAttrName(attrname), child)
			node.attrs[attrname] = convertedattr
		return self._decorateNode(node)

	def clone(self):
		node = self.__class__() # "virtual" copy constructor
		node.content = self.content.clone() # this is faster than passing it in the constructor (no ToNode call)
		for attr in self.attrs.keys():
			node.attrs[attr] = self.attrs[attr].clone()
		return self._decorateNode(node)

	def asPlainString(self):
		return self.content.asPlainString()

	def _addImageSizeAttributes(self, converter, imgattr, widthattr=None, heightattr=None):
		"""
		<par noindent>add width and height attributes to the element for the image that can be found in the attribute
		<argref>imgattr</argref>. If the attributes are already there, they are taken as a formatting
		template with the size passed in as a dictionary with the keys <code>"width"</code> and <code>"height"</code>,
		i.e. you could make your image twice as wide with <code>width="%(width)d*2"</code>.</par>

		<par>Passing <code>None</code> as <argref>widthattr</argref> or <argref>heightattr</argref> will
		prevent the repsective attributes from being touched in any way.</par>
		"""

		if self.hasAttr(imgattr):
			size = self[imgattr].convert(converter).ImageSize()
			if size is not None: # the size was retrieved so we can use it
				sizedict = {"width": size[0], "height": size[1]}
				for attr in (heightattr, widthattr):
					if attr is not None: # do something to the width/height
						if self.hasAttr(attr):
							try:
								s = self[attr].convert(converter).asPlainString() % sizedict
								s = str(eval(s))
								s = utils.stringFromCode(s)
								self[attr] = s
							except TypeError: # ignore "not all argument converted"
								pass
							except:
								raise errors.ImageSizeFormatError(self, attr)
						else:
							self[attr] = size[attr==heightattr]

	def present(self, presenter):
		presenter.presentElement(self)

	def _doreprtree(self, nest, elementno, presenter):
		v = []
		if self.empty:
			v.append([nest, self.startLoc, elementno, self._str(content=self.__strattrs(presenter), brackets=1, slash=1, ansi=presenter.ansi)])
		else:
			v.append([nest, self.startLoc, elementno, self._str(content=self.__strattrs(presenter), brackets=1, ansi=presenter.ansi)])
			i = 0
			for child in self:
				v.extend(child._doreprtree(nest+1, elementno + [i], presenter))
				i += 1
			if self.startLoc is None:
				v.append([nest, self.startLoc, elementno, self._str(brackets=1, slash=-1, ansi=presenter.ansi)])
			else:
				v.append([nest, self.endLoc, elementno, self._str(brackets=1, slash=-1, ansi=presenter.ansi)])
		return v

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self.startLoc, self)
		publisher.publish(u"<")
		if self.publishPrefix is not None:
			publishPrefix = self.publishPrefix
		else:
			publishPrefix = publisher.publishPrefix
		if publishPrefix:
			publisher.publish(self.namespace.prefix) # requires that the element is registered via registerElement()
			publisher.publish(u":")
		publisher.publish(self.name) # requires that the element is registered via registerElement()
		for attrname in self.attrs.keys():
			publisher.publish(u" ")
			publisher.publish(attrname)
			value = self[attrname]
			if isinstance(value, BoolAttr):
				if publisher.XHTML>0:
					publisher.publish(u"=\"")
					publisher.publish(attrname)
					publisher.publish(u"\"")
			else:
				publisher.publish(u"=\"")
				value.publish(publisher)
				publisher.publish(u"\"")
		if len(self):
			if self.empty:
				raise errors.EmptyElementWithContentError(self)
			publisher.publish(u">")
			self.content.publish(publisher)
			publisher.publish(u"</")
			if publishPrefix:
				publisher.publish(self.namespace.prefix) # requires that the element is registered via registerElement()
				publisher.publish(u":")
			publisher.publish(self.name)
			publisher.publish(u">")
		else:
			if publisher.XHTML in (0, 1):
				if self.empty:
					if publisher.XHTML==1:
						publisher.publish(u" /")
					publisher.publish(u">")
				else:
					publisher.publish(u"></")
					if publishPrefix:
						publisher.publish(self.namespace.prefix) # requires that the element is registered via registerElement()
						publisher.publish(u":")
					publisher.publish(self.name)
					publisher.publish(u">")
			elif publisher.XHTML == 2:
				publisher.publish(u"/>")

	def __getitem__(self, index):
		"""
		returns an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number or list (i.e. content node index) is passed in.
		"""
		if type(index) in (types.StringType, types.UnicodeType):
			if index[-1] == "_":
				index = index[:-1]
			try:
				return self.attrs[index] # we're returning the packed attribute here, because otherwise there would be no possibility to get an expanded URL
			except KeyError:
				raise errors.AttrNotFoundError(self, index)
		else:
			return self.content[index]

	def __setitem__(self, index, value):
		"""
		sets an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number or list (i.e. content node index) is passed in.
		"""
		if type(index) in (types.StringType, types.UnicodeType):
			if index[-1] == "_":
				index = index[:-1]
			# values are contructed via the attribute classes specified in the attrHandlers dictionary, which do the conversion
			try:
				attr = self.attrHandlers[index]() # create an empty attribute of the right type
			except KeyError:
				raise errors.IllegalAttrError(self, index)
			attr.extend(value) # put the value into the attribute
			self.attrs[index] = attr # put the attribute in our dict
		else:
			self.content[index] = value

	def __delitem__(self, index):
		"""
		removes an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number or list (i.e. content node index) is passed in.
		"""
		if type(index) in (types.StringType, types.UnicodeType):
			if index[-1] == "_":
				index = index[:-1]
			try:
				del self.attrs[index]
			except KeyError:
				raise errors.AttrNotFoundError(self, index)
		else:
			del self.content[index]

	def hasAttr(self, attr):
		"""
		return whether <self/> has an attribute named <argref>attr</argref>.
		"""

		return self.attrs.has_key(attr)

	def getAttr(self, attr, default=None):
		"""
		works like the method <code>get()</code> of dictionaries,
		it returns the attribute with the name <argref>attr</argref>,
		or if <self/> has no such attribute, <argref>default</argref>
		(after converting it to a node and wrapping it into the appropriate
		attribute node.)
		"""
		try:
			return self[attr]
		except errors.AttrNotFoundError:
			return self.attrHandlers[attr](default) # pack the attribute into an attribute object

	def __getslice__(self, index1, index2):
		"""
		returns a copy of the element that contains a slice of the content
		"""
		return self.__class__(self.content[index1:index2], self.attrs)

	def __setslice__(self, index1, index2, sequence):
		"""
		modifies a slice of the content of the element
		"""
		self.content[index1:index2] = sequence

	def __delslice__(self, index1, index2):
		"""
		removes a slice of the content of the element
		"""
		del self.content[index1:index2]

	def __len__(self):
		"""
		return the number of children
		"""
		return len(self.content)

	def compact(self):
		node = self.__class__()
		node.content = self.content.compact()
		for attr in self.attrs.keys():
			node.attrs[attr] = self.attrs[attr].compact()
		return self._decorateNode(node)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		if searchattrs:
			for attr in self.attrs.keys():
				node.extend(self[attr].find(type, subtype, attrs, test, searchchildren, searchattrs))
		node.extend(self.content.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def copyDefaultAttrs(self, fromDict=None):
		"""
		Sets attributes that are not set <self/> to the default
		values taken from the fromDict dictionary.
		If fromDict is omitted, defaults are taken from self.defaults.

		Note: Boolean attributes may savely be set to zero or one (integer).
		as only the fact that a boolean attribte exists matters.
		"""

		if fromDict is None:
			fromDict = self.defaults
		for (attr, value) in fromDict.items():
			if not self.hasAttr(attr):
				self[attr] = value

class Entity(Node):
	"""
	<par noindent>Class for entities. Derive your own entities from
	it and implement <code>convert()</code> and <code>asPlainString()</code>.</par>

	<par>If this entity is a simple character reference, you don't have to implement
	those functions. Simply set the class attribute <code>codepoint</code>, and
	you're done.</par>
	"""

	def convert(self, converter=None):
		node = Text(unichr(self.codepoint))
		return self._decorateNode(node)

	def compact(self):
		return self

	clone = compact

	def asPlainString(self):
		return unichr(self.codepoint)

	def present(self, presenter):
		presenter.presentEntity(self)

	def _doreprtree(self, nest, elementno, presenter):
		return [[nest, self.startLoc, elementno, self._dorepr(presenter)]]

	def publish(self, publisher):
		publisher.publish(u"&")
		if self.publishPrefix is not None:
			publishPrefix = self.publishPrefix
		else:
			publishPrefix = publisher.publishPrefix
		if publishPrefix:
			publisher.publish(self.namespace.prefix) # requires that the entity is registered via Namespace.register()
			publisher.publish(u":")
		publisher.publish(self.name) # requires that the entity is registered via Namespace.register()
		publisher.publish(u";")

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		if self._matches(type, subtype, attrs, test):
			node.append(self)
		return node

class Null(Node):
	"""
	node that does not contain anything.
	"""

	def convert(self, converter=None):
		return self

	def clone(self):
		pass

	compact = clone

	def publish(self, publisher):
		pass

	def present(self, presenter):
		presenter.presentNull(self)

	def _doreprtree(self, nest, elementno, presenter):
		return [[nest, self.startLoc, elementno, self._dorepr(presenter)]]

Null = Null() # Singleton, the Python way

class Attr(Frag):
	"""
	<par noindent>Base classes of all attribute classes.</par>

	<par>The content of an attribute may be any other XSC node. This is different from
	a normal DOM, where only text and character references are allowed. The reason for
	this is to allow dynamic content (implemented as elements) to be put into attributes.</par>

	<par>Of course, this dynamic content when finally converted to HTML will normally result in
	a fragment consisting only of text and character references.</par>
	"""

	def present(self, presenter):
		presenter.inAttr = 1
		presenter.presentAttr(self)
		presenter.inAttr = 0

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self.startLoc, self)
		publisher.inAttr = 1
		Frag.publish(self, publisher)
		publisher.inAttr = 0

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
	for image or file size, a http request will be made to the server specified in the server
	option (options.server).

	For all other URLs a normal request will be made corresponding to the specified scheme
	(http, ftp, etc.)
	"""

	def __init__(self, *_content):
		self.base = url.URL()
		Attr.__init__(self, *_content)

	def _str(self, content=None, brackets=None, slash=None, ansi=None):
		attr = " %s=%s%s%s" % (strAttrName("base", ansi), strQuote(ansi=ansi), strURL(self.base.asString(), ansi=ansi), strQuote(ansi=ansi))
		return Attr._str(self, content=attr, brackets=brackets, slash=slash, ansi=ansi)

	def present(self, presenter):
		presenter.presentURLAttr(self)

	def publish(self, publisher):
		u = self.asURL()
		if u.scheme is None and (len(u)==0 or url._isNoPathMarker(u[0])):
			return Text(u.asPlainString()).publish(publisher)
		else:
			return Text(u.relativeTo(publisher.base).asPlainString()).publish(publisher)

	def convert(self, converter=None):
		node = Attr.convert(self, converter)
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
		return url.URL(Attr.asPlainString(self))

	def asPlainString(self):
		return self.asURL().asString()

	def forInput(self):
		u = self.base + self.asURL()
		if u.scheme == "server":
			u = u.relativeTo(url.URL(scheme="http", server=options.server))
		return u

	def ImageSize(self):
		"""
		returns the size of an image as a tuple or None if the image shouldn't be read
		"""

		url = self.forInput()
		size = None
		if 1: # FIXME xsc.isRetrieve(url):
			try:
				(filename, headers) = url.retrieve()
				if headers.maintype == "image":
					img = Image.open(filename)
					size = img.size
					del img
				urllib.urlcleanup()
			except IOError:
				urllib.urlcleanup()
				raise errors.FileNotFoundError(self.startLoc, url)
		return size

	def FileSize(self):
		"""
		returns the size of a file in bytes or None if the file shouldn't be read
		"""

		url = self.forInput()

		size = None
		if 1: # FIXME xsc.isRetrieve(url):
			try:
				(filename, headers) = url.retrieve()
				size = os.stat(filename)[stat.ST_SIZE]
				urllib.urlcleanup()
			except IOError:
				urllib.urlcleanup()
				raise errors.FileNotFoundError(self.startLoc, url)
		return size

	def open(self):
		"""
		opens the URL via urllib
		"""
		return self.forInput().open()

###
###
###

class Namespace:
	"""
	an XML namespace, contains the classes for the elements, entities and processing instructions
	in the namespace.
	"""

	def __init__(self, prefix, uri, thing=None):
		self.prefix = utils.stringFromCode(prefix)
		self.uri = utils.stringFromCode(uri)
		self.elementsByName = {} # dictionary for mapping element names to classes
		self.entitiesByName = {} # dictionary for mapping entity names to classes
		self.entitiesByNumber = [ [] for i in xrange(65536) ]
		self.procInstsByName = {} # dictionary for mapping processing instruction target names to classes
		self.register(thing)
		namespaceRegistry.register(self)

	def register(self, thing):
		"""
		<par noindent>this function lets you register <argref>thing</argref> in the namespace.
		If <argref>thing</argref> is a class derived from <classref>Element</classref>,
		<classref>Entity</classref> or <classref>ProcInst</classref> it will be registered
		in the following way: The class <argref>thing</argref> will be registered under it's
		class name (<code><argref>thing</argref>.__name__</code>). If you want to change this
		behaviour, do the following: set a class variable <code>name</code> to the name you
		want to be used. If you don't want <argref>thing</argref> to be registered at all,
		set <code>name</code> to <code>None</code>.

		<par>After the call <argref>thing</argref> will have two class attributes:
		<code>name</code>, which is the name under which the class is registered and
		<code>namespace</code>, which is the namespace itself (i.e. <self/>).</par>

		<par>If <argref>thing</argref> already has an attribute <code>namespace</code>, it
		won't be registered again.</par>

		<par>If <argref>thing</argref> is a dictionary, every object in the dictionary
		will be registered.</par>

		<par>All other objects are ignored.</par>
		"""

		t = type(thing)
		if t is types.ClassType:
			iselement = thing is not Element and issubclass(thing, Element)
			isentity = thing is not Entity and issubclass(thing, Entity)
			isprocinst = thing is not ProcInst and issubclass(thing, ProcInst)
			if iselement or isentity or isprocinst:
				# if the class attribute register is 0, the class won't be registered
				# and if the class already has a namespace attribute, it is already registered, so it won't be registered again
				# (we're accessing __dict__ here, because we don't want the attribute from the base class object)
				if thing.register and (not thing.__dict__.has_key("namespace")):
					try:
						name = thing.__dict__["name"] # no inheritance, otherwise we might get the name attribute from an already registered base class
					except KeyError:
						name = thing.__name__
					thing.namespace = self # this creates a cycle
					if name is not None:
						name = utils.stringFromCode(name)
						thing.name = name
						if iselement:
							self.elementsByName[name] = thing
						elif isentity:
							self.entitiesByName[name] = thing
							try:
								self.entitiesByNumber[thing.codepoint].append(thing)
							except AttributeError: # no codepoint attribute in the class, so this isn't a char ref
								pass
						else: # if isprocinst:
							self.procInstsByName[name] = thing
		elif t is types.DictionaryType:
			for key in thing.keys():
				self.register(thing[key])

	def __repr__(self):
		return "<%s.%s instance prefix=%r uri=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.prefix, self.uri, id(self))

class NamespaceRegistry:
	"""
	global registry for all namespaces
	"""
	def __init__(self):
		self.byPrefix = {}
		self.byURI = {}

	def register(self, namespace):
		self.byPrefix[namespace.prefix] = namespace
		self.byURI[namespace.uri] = namespace

namespaceRegistry = NamespaceRegistry()

class Namespaces:
	"""
	list of namespaces.
	"""
	def __init__(self, *namespaces):
		self.namespaces = []
		self.pushNamespace(namespace) # always include the namespace object from our own modules with &gt; etc.
		self.pushNamespace(*namespaces)

	def pushNamespace(self, *namespaces):
		for namespace in namespaces:
			if type(namespace) is types.ModuleType:
				namespace = namespace.namespace
			self.namespaces.insert(0, namespace) # built in reverse order, so a simple "for in" finds the most recent entry.

	def popNamespace(self, count=1):
		del self.namespaces[:count]

	def __splitName(self, name):
		"""
		split a qualified name into a namespace,name pair
		"""
		name = name.split(":")
		if len(name) == 1: # no namespace specified
			name.insert(0, None)
		return name

	def __allNamespaces(self):
		"""
		returns a list of all namespaces to be searched in this order
		"""
		return self.namespaces+namespaceRegistry.byPrefix.values()

	def elementFromName(self, name):
		"""
		returns the element class for the name name (which might include a namespace).
		"""
		name = self.__splitName(name)
		for namespace in self.__allNamespaces():
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.elementsByName[name[1]]
				except KeyError: # no element in this namespace with this name
					pass
		raise errors.IllegalElementError(self.getLocation(), name) # elements with this name couldn't be found

	def entityFromName(self, name):
		"""
		returns the entity class for the name name (which might include a namespace).
		"""
		name = self.__splitName(name)
		for namespace in self.__allNamespaces():
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.entitiesByName[name[1]]
				except KeyError: # no entity in this namespace with this name
					pass
		raise errors.IllegalEntityError(self.getLocation(), name) # entities with this name couldn't be found

	def procInstFromName(self, name):
		"""
		returns the processing instruction class for the name name (which might include a namespace).
		"""
		name = self.__splitName(name)
		for namespace in self.__allNamespaces():
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.procInstsByName[name[1]]
				except KeyError: # no processing instruction in this namespace with this name
					pass
		raise errors.IllegalProcInstError(self.getLocation(), name) # processing instructions with this name couldn't be found

	def entityFromNumber(self, number):
		"""
		returns the first entity class for the codepoint number.
		"""
		for namespace in self.__allNamespaces():
			if len(namespace.entitiesByNumber[number]):
				return namespace.entitiesByNumber[number][0]
		return None

	def getLocation(self):
		return None

# C0 Controls and Basic Latin
class quot(Entity): "quotation mark = APL quote, U+0022 ISOnum"; codepoint = 34
class amp(Entity): "ampersand, U+0026 ISOnum"; codepoint = 38
class lt(Entity): "less-than sign, U+003C ISOnum"; codepoint = 60
class gt(Entity): "greater-than sign, U+003E ISOnum"; codepoint = 62

namespace = Namespace("xsc", "", vars())

defaultNamespaces = Namespaces()

###
###
###

class Location:
	"""
	Represents a location in an XML entity.
	"""

	def __init__(self, locator=None, sysID=None, pubID=None, lineNumber=-1, columnNumber=-1):
		"""
		Initialized by being passed a locator, from which it reads off the current location,
		which is then stored internally. In addition to that the systemID, public ID, line number
		and column number can be overwritten by explicit arguments.
		"""
		if locator is not None:
			self.__sysID = locator.getSystemId()
			self.__pubID = locator.getPublicId()
			self.__lineNumber = locator.getLineNumber()
			self.__columnNumber = locator.getColumnNumber()
		else:
			self.__sysID = None
			self.__pubID = None
			self.__lineNumber = -1
			self.__columnNumber = -1
		if self.__sysID is None:
			self.__sysID = sysID
		if self.__pubID is None:
			self.__pubID = pubID
		if self.__lineNumber == -1:
			self.__lineNumber = lineNumber
		if self.__columnNumber == -1:
			self.__columnNumber = columnNumber

	def getColumnNumber(self):
		"Return the column number of this location."
		return self.__columnNumber

	def getLineNumber(self):
		"Return the line number of this location."
		return self.__lineNumber

	def getPublicId(self):
		"Return the public identifier for this location."
		return self.__pubID

	def getSystemId(self):
		"Return the system identifier for this location."
		return self.__sysID

	def __str__(self):
		# get and format the system ID
		sysID = self.getSystemId()
		if sysID is None:
			sysID = "<unknown>"

		# get and format the line number
		line = self.getLineNumber()
		if line==-1:
			line = "?"
		else:
			line = str(line)

		# get and format the column number
		column = self.getColumnNumber()
		if column==-1:
			column = "?"
		else:
			column = str(column)

		# now we have the parts => format them
		return "%s:%s:%s" % (presenters.strURL(sysID), presenters.strNumber(line), presenters.strNumber(column))

	def __repr__(self):
		return "<%s object sysID=%r, pubID=%r, lineNumber=%r, columnNumber=%r at %08x>" % \
			(self.__class__.__name__, self.getSystemId(), self.getPublicId(), self.getLineNumber(), self.getColumnNumber(), id(self))
