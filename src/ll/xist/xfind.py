# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<par>This module contains XFind and CSS selectors and related classes and functions.</par>

<par>A selector is a &xist; tree traversal filter that traverses the complete
&xml; tree and outputs those nodes specified by the selector. Selectors can
be combined with various operations and form a language comparable to
<link href="http://www.w3.org/TR/xpath">XPath</link> but implemented as Python
expressions. The following code shows some
examples. First lets define some support code:</par>

<example><title>Support code (put in <filename>help.py</filename>)</title>
<prog>
from ll.xist import xsc, xfind, parsers
from ll.xist.ns import html

node = parsers.parseURL("http://www.python.org", tidy=True)

def output(selector):
	for n in node.walknode(selector):
		print n.bytes()
</prog>
</example>

<par>We can now use this code in a Python session via <lit>from help import *</lit>.</par>

<prog>
<prompt>>>> </prompt><input>output(html.a/html.img) # images children of a elements</input>
<![CDATA[<img src="/images/python-logo.gif" alt="homepage" id="logo" border="0" />
<img id="skiptonav" alt="skip to navigation" src="/images/trans.gif" border="0" />
<img id="skiptocontent" alt="skip to content" src="/images/trans.gif" border="0" />
<img alt="success story photo" class="success" src="/images/success/nasa.jpg" />]]>

<prompt>>>> </prompt><input>output(html.ul//html.a) # a descendants of ul elements</input>
<![CDATA[<a title="About The Python Language" href="/about/">About</a>
<a title="Major Happenings Within the Python Community" href="/news/">News</a>
<a title="Tutorials, Library Reference, C API" href="/doc/">Documentation</a>]]>

<prompt>>>> </prompt><input>output(html.img & xfind.attrendswith("src", ".jpg")) # JPEG images</input>
<![CDATA[<img alt="success story photo" class="success" src="/images/success/nasa.jpg" />]]>

<prompt>>>> </prompt><input>output(html.img & ~xfind.hasattr("title")) # All images without a title attribute</input>
<![CDATA[<img src="/images/python-logo.gif" border="0" id="logo" alt="homepage" />
<img id="skiptonav" border="0" src="/images/trans.gif" alt="skip to navigation" />
<img id="skiptocontent" border="0" src="/images/trans.gif" alt="skip to content" />
<img alt="success story photo" src="/images/success/nasa.jpg" class="success" />]]>

<prompt>>>> </prompt><input>output(html.a & xfind.hasclass("reference")) # Links with 'reference' class</input>
<![CDATA[<a class="reference" href="/search">Advanced Search</a>
<a href="about/success/rackspace" class="reference">Rackspace</a>
<a href="about/success/ilm" class="reference">Industrial Light and Magic</a>]]>

<prompt>>>> </prompt><input>output(html.ul/html.li[0]) # Every li element that is the first li child of its ul parent</input>
<![CDATA[<li>
          <a title="About The Python Language" href="/about/">About</a>
        </li>
<li><a title="Manuals for Latest Stable Release" href="http://docs.python.org/">Documentation</a></li>
<li class="group"><a href="http://wiki.python.org/moin/WebProgramming">Web Programming</a></li>]]>

</prog>
"""

__version__ = "$Revision$".split()[1]
# $Source$


try:
	import cssutils
	from cssutils.css import cssstylerule
	from cssutils.css import selector as cssselector
	from cssutils.css import cssnamespacerule
except ImportError:
	pass

from ll import misc
from ll.xist import xsc


class CSSWeight(tuple):
	"""
	The specificity of a &CSS; selector as a 3-item tuple as specified by
	<link href="http://www.w3.org/TR/css3-selectors/#specificity">CSS3</link>.
	"""

	def __new__(cls, a=0, b=0, c=0):
		return tuple.__new__(cls, (a, b, c))

	def __add__(self, other):
		return CSSWeight(self[0]+other[0], self[1]+other[1], self[2]+other[2])

	def __repr__(self):
		return "CSSWeight(%r, %r, %r)" % (self[0], self[1], self[2])


class Selector(xsc.WalkFilter):
	"""
	Base class for all tree traversal filters that visit the complete tree.
	Whether a node gets output can be specified by overwriting the
	<method>match</method> method. Selectors can be combined with various
	operations (see methods below).
	"""

	@misc.notimplemented
	def match(self, path):
		pass

	def filter(self, path):
		return (True, xsc.entercontent, xsc.enterattrs) if self.match(path) else (xsc.entercontent, xsc.enterattrs)

	def __div__(self, other):
		return ChildCombinator(self, xsc.makewalkfilter(other))

	def __floordiv__(self, other):
		return DescendantCombinator(self, xsc.makewalkfilter(other))

	def __mul__(self, other):
		return AdjacentSiblingCombinator(self, xsc.makewalkfilter(other))

	def __pow__(self, other):
		return GeneralSiblingCombinator(self, xsc.makewalkfilter(other))

	def __and__(self, other):
		return AndCombinator(self, xsc.makewalkfilter(other))

	def __or__(self, other):
		return OrCombinator(self, xsc.makewalkfilter(other))

	def __invert__(self):
		return NotCombinator(self)

	def cssweight(self):
		"""
		Return the &CSS; specificity of <self/> as a
		<pyref class="CSSWeight"><class>CSSWeight</class></pyref> object.
		"""
		return CSSWeight()


class IsInstanceSelector(Selector):
	"""
	<par>Selector that selects all nodes that are instances of the specified type.
	You can either create an <class>IsInstanceSelector</class> object directly
	or simply pass a class to a function that expects a walk filter.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>html.a</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a id="logolink" accesskey="1" href="http://www.python.org/"><img src="http://www.python.org/images/python-logo.gif" id="logo" border="0" alt="homepage" /></a>
	<a accesskey="2" href="http://www.python.org/#left%2dhand%2dnavigation"><img id="skiptonav" src="http://www.python.org/images/trans.gif" border="0" alt="skip to navigation" /></a>
	<a accesskey="3" href="http://www.python.org/#content%2dbody"><img id="skiptocontent" src="http://www.python.org/images/trans.gif" border="0" alt="skip to content" /></a>
	<a class="reference" href="http://www.python.org/search">Advanced Search</a>
	<a title="About The Python Language" href="http://www.python.org/about/">About</a>]]>
	<rep>...</rep>
	</tty>
	</example>
	"""
	def __init__(self, *types):
		self.types = types

	def match(self, path):
		if path:
			return isinstance(path[-1], self.types)
		return False

	def __or__(self, other):
		# If other is a type check too, combine self and other into one isinstance instance
		if isinstance(other, xsc._Node_Meta):
			return IsInstanceSelector(*(self.types + (other,)))
		elif isinstance(other, IsInstanceSelector):
			return IsInstanceSelector(*(self.types+other.types))
		return Selector.__or__(self, other)

	def __getitem__(self, index):
		return nthoftype(index, *self.types)

	def __str__(self):
		if len(self.types) == 1:
			return "%s.%s" % (self.types[0].__module__, self.types[0].__name__)
		else:
			return "(%s)" % " | ".join("%s.%s" % (type.__module__, type.__name__) for type in self.types)


class hasname(Selector):
	"""
	<par>Selector that selects all nodes that have a specified Python name (which
	only selects elements, processing instructions and entities). Also a namespace
	name can be specified as a second argument, which will only select elements
	from the specified namespace.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.hasname("img")</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<img border="0" src="http://www.python.org/images/python-logo.gif" alt="homepage" id="logo" />
	<img border="0" id="skiptonav" alt="skip to navigation" src="http://www.python.org/images/trans.gif" />
	<img border="0" id="skiptocontent" alt="skip to content" src="http://www.python.org/images/trans.gif" />
	<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />]]>
	</tty>
	</example>
	"""
	def __init__(self, name, xmlns=None):
		self.name = name
		self.xmlns = xsc.nsname(xmlns)

	def match(self, path):
		if path:
			node = path[-1]
			if self.xmlns is not None:
				return isinstance(node, xsc.Element) and node.__class__.__name__ == self.name and node.xmlns == self.xmlns
			else:
				return isinstance(node, (xsc.Element, xsc.ProcInst, xsc.Entity)) and node.__class__.__name__ == self.name
		return False

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.name)


class hasname_xml(Selector):
	"""
	<class>hasname_xml</class> works similar to <pyref class="hasname"><class>hasname</class></pyref>
	except that the specified name is treated as the &xml; name, not the Python name.
	"""
	def __init__(self, name, xmlns=None):
		self.name = name
		self.xmlns = xsc.nsname(xmlns)

	def match(self, path):
		if path:
			node = path[-1]
			if self.xmlns is not None:
				return isinstance(node, xsc.Element) and node.xmlname == self.name and node.xmlns == self.xmlns
			else:
				return isinstance(node, (xsc.Element, xsc.ProcInst, xsc.Entity)) and node.xmlname == self.name
		return False

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.name)


class IsSelector(Selector):
	"""
	<par>Selector that selects one specific node in the tree. This can be
	combined with other selectors via <pyref class="ChildCombinator"><class>ChildCombinator</class>s</pyref>
	or <pyref class="DescendantCombinator"><class>DescendantCombinator</class>s</pyref>
	to select children of this specific node. You can either create an
	<class>IsSelector</class> directly or simply pass a node to a function that
	expects a walk filter.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>doc[0]/xsc.Element</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<ll.xist.ns.html.head element object (13 children/no attrs) (from http://www.python.org/:6:?) at 0xb6c82f4c>
	<ll.xist.ns.html.body element object (19 children/no attrs) (from http://www.python.org/:26:?) at 0xb6c3154c>]]>
	</tty>
	</example>
	"""
	def __init__(self, node):
		self.node = node

	def match(self, path):
		return path and path[-1] is self.node

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.node)


class isroot(Selector):
	def match(self, path):
		return len(path) == 1

	def __str__(self):
		return "isroot"


isroot = isroot()


class empty(Selector):
	"""
	<par>Selector that selects all empty elements or fragments.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.empty</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<meta content="text/html; charset=utf-8" http-equiv="content-type" />
	<meta content="python programming language object oriented web free source" name="keywords" />
	<meta content="      Home page for Python, an interpreted, interactive, object-oriented, extensible
	      programming language. It provides an extraordinary combination of clarity and
	      versatility, and is free and comprehensively ported. " name="description" />
	<link type="application/rss+xml" href="http://www.python.org/channews.rdf" rel="alternate" title="RSS" />]]>
	<rep>...</rep>
	</tty>
	</example>
	"""

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, (xsc.Element, xsc.Frag)):
				return len(node) == 0
		return False

	def __str__(self):
		return "empty"


empty = empty()


class onlychild(Selector):
	"""
	<par>Selector that selects all node that are the only child of their parents.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.onlychild &amp; html.a</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a accesskey="2" href="http://www.python.org/#left%2dhand%2dnavigation"><img id="skiptonav" alt="skip to navigation" src="http://www.python.org/images/trans.gif" border="0" /></a>
	<a accesskey="3" href="http://www.python.org/#content%2dbody"><img id="skiptocontent" alt="skip to content" src="http://www.python.org/images/trans.gif" border="0" /></a>
	<a href="http://www.python.org/download/releases/2.5.1">Quick Links (2.5.1)</a>
	<a title="Manuals for Latest Stable Release" href="http://docs.python.org/">Documentation</a>]]>
	<rep>...</rep>
	</tty>
	</example>
	"""

	def match(self, path):
		if len(path) >= 2:
			parent = path[-2]
			if isinstance(parent, (xsc.Frag, xsc.Element)):
				return len(parent)==1 and parent[0] is path[-1]
		return False

	def __str__(self):
		return "onlychild"


onlychild = onlychild()


class onlyoftype(Selector):
	"""
	<par>Selector that selects all nodes that are the only nodes of their type among
	their siblings.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.onlyoftype &amp; xsc.Element</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<ll.xist.ns.html.html element object (2 children/1 attr) (from http://www.python.org/:4:?) at 0xb6d6e7ec>
	<ll.xist.ns.html.head element object (13 children/no attrs) (from http://www.python.org/:6:?) at 0xb6cc1f8c>
	<ll.xist.ns.html.title element object (1 child/no attrs) (from http://www.python.org/:8:?) at 0xb6d79b8c>
	<ll.xist.ns.html.body element object (19 children/no attrs) (from http://www.python.org/:26:?) at 0xb6d7282c>]]>
	<rep>...</rep>
	</tty>
	</example>
	"""

	def match(self, path):
		if len(path) >= 2:
			node = path[-1]
			parent = path[-2]
			if isinstance(parent, (xsc.Frag, xsc.Element)):
				for child in parent:
					if isinstance(child, node.__class__):
						if child is not node:
							return False
				return True
		return False

	def __str__(self):
		return "onlyoftype"


onlyoftype = onlyoftype()


class hasattr(Selector):
	"""
	<par>Selector that selects all element nodes that have an attribute with one
	of the specified Python names. For selecting nodes with global attributes
	the attribute class can be passed.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html, xml</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.onlyoftype &amp; xsc.Element</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<ll.xist.ns.html.html element object (2 children/1 attr) (from http://www.python.org/:4:?) at 0xb6d6e7ec>
	<ll.xist.ns.html.head element object (13 children/no attrs) (from http://www.python.org/:6:?) at 0xb6cc1f8c>
	<ll.xist.ns.html.title element object (1 child/no attrs) (from http://www.python.org/:8:?) at 0xb6d79b8c>
	<ll.xist.ns.html.body element object (19 children/no attrs) (from http://www.python.org/:26:?) at 0xb6d7282c>]]>
	<rep>...</rep>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.hasattr(xml.Attrs.lang</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<ll.xist.ns.html.html element object (2 children/2 attrs) (from http://www.python.org/:4:?) at 0xb6d71d4c>]]>
	</tty>
	</example>
	"""

	def __init__(self, *attrnames):
		self.attrnames = attrnames

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element):
				for attrname in self.attrnames:
					if node.Attrs.isallowed(attrname) and node.attrs.has(attrname):
						return True
		return False

	def __str__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join(repr(attrname) for attrname in self.attrnames))


class hasattr_xml(Selector):
	"""
	<class>hasattr_xml</class> works similar to <pyref class="hasattr"><class>hasattr</class></pyref>
	except that the specified names are treated as &xml; names instead of Python names.
	"""

	def __init__(self, *attrnames):
		self.attrnames = attrnames

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element):
				for attrname in self.attrnames:
					if node.Attrs.isallowed_xml(attrname) and node.attrs.has_xml(attrname):
						return True
		return False

	def __str__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join(repr(attrname) for attrname in self.attrnames))


class attrhasvalue(Selector):
	"""
	<par>Selector that selects all element nodes where an attribute with the
	specified Python name has the specified value. For global attributes
	the attribute class can be passed. Note that
	<pyref module="ll.xist.xsc" class="Attr" method="isfancy">fancy</pyref> attributes
	will not be considered.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.attrhasvalue("rel", "stylesheet")</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<link media="screen" type="text/css" href="http://www.python.org/styles/screen-switcher-default.css" rel="stylesheet" id="screen-switcher-stylesheet" />
	<link media="scReen" type="text/css" rel="stylesheet" href="http://www.python.org/styles/netscape4.css" />
	<link media="print" type="text/css" rel="stylesheet" href="http://www.python.org/styles/print.css" />]]>
	</tty>
	</example>
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed(self.attrname):
				attr = node.attrs.get(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return unicode(attr) == self.attrvalue
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrhasvalue_xml(Selector):
	"""
	<class>attrhasvalue_xml</class> works similar to <pyref class="attrhasvalue"><class>attrhasvalue</class></pyref>
	except that the specified name is treated as an &xml; name instead of a Python name.
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attrname):
				attr = node.attrs.get_xml(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return unicode(attr) == self.attrvalue
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrcontains(Selector):
	"""
	<par>Selector that selects all element nodes where an attribute with the
	specified Python name contains the specified subtring in its value. For
	global attributes the attribute class can be passed. Note that
	<pyref module="ll.xist.xsc" class="Attr" method="isfancy">fancy</pyref>
	attributes will not be considered.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.attrcontains("rel", "stylesheet")</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<link type="text/css" id="screen-switcher-stylesheet" media="screen" rel="stylesheet" href="http://www.python.org/styles/screen-switcher-default.css" />
	<link type="text/css" media="scReen" rel="stylesheet" href="http://www.python.org/styles/netscape4.css" />
	<link type="text/css" media="print" rel="stylesheet" href="http://www.python.org/styles/print.css" />
	<link type="text/css" title="large text" media="screen" rel="alternate stylesheet" href="http://www.python.org/styles/largestyles.css" />
	<link type="text/css" title="default fonts" media="screen" rel="alternate stylesheet" href="http://www.python.org/styles/defaultfonts.css" />]]>
	</tty>
	</example>
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed(self.attrname):
				attr = node.attrs.get(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return self.attrvalue in unicode(attr)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrcontains_xml(Selector):
	"""
	<class>attrcontains_xml</class> works similar to <pyref class="attrcontains"><class>attrcontains</class></pyref>
	except that the specified name is treated as an &xml; name instead of a Python name.
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attrname):
				attr = node.attrs.get_xml(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return self.attrvalue in unicode(attr)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrstartswith(Selector):
	"""
	<par>Selector that selects all element nodes where an attribute with the
	specified Python name starts with the specified string. For global attributes
	the attribute class can be passed. Note that
	<pyref module="ll.xist.xsc" class="Attr" method="isfancy">fancy</pyref> attributes
	will not be considered.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.attrstartswith("class_", "input-")</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<input class="input-text" id="q" type="text" name="q" />
	<input value="search" class="input-button" id="submit" type="submit" name="submit" />]]>
	</tty>
	</example>
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed(self.attrname):
				attr = node.attrs.get(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return unicode(attr).startswith(self.attrvalue)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrstartswith_xml(Selector):
	"""
	<class>attrstartswith_xml</class> works similar to <pyref class="attrstartswith"><class>attrstartswith</class></pyref>
	except that the specified name is treated as an &xml; name instead of a Python name.
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attrname):
				attr = node.attrs.get_xml(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return unicode(attr).startswith(self.attrvalue)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrendswith(Selector):
	"""
	<par>Selector that selects all element nodes where an attribute with the
	specified Python name ends with the specified string. For global attributes
	the attribute class can be passed. Note that
	<pyref module="ll.xist.xsc" class="Attr" method="isfancy">fancy</pyref> attributes
	will not be considered.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.attrendswith("href", ".css")</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<link href="http://www.python.org/styles/screen-switcher-default.css" type="text/css" rel="stylesheet" id="screen-switcher-stylesheet" media="screen" />
	<link type="text/css" rel="stylesheet" href="http://www.python.org/styles/netscape4.css" media="scReen" />
	<link type="text/css" rel="stylesheet" href="http://www.python.org/styles/print.css" media="print" />
	<link title="large text" type="text/css" rel="alternate stylesheet" href="http://www.python.org/styles/largestyles.css" media="screen" />
	<link title="default fonts" type="text/css" rel="alternate stylesheet" href="http://www.python.org/styles/defaultfonts.css" media="screen" />]]>
	</tty>
	</example>
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed(self.attrname):
				attr = node.attrs.get(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return unicode(attr).endswith(self.attrvalue)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrendswith_xml(Selector):
	"""
	<class>attrendswith_xml</class> works similar to <pyref class="attrendswith"><class>attrendswith</class></pyref>
	except that the specified name is treated as an &xml; name instead of a Python name.
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attrname):
				attr = node.attrs.get_xml(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return unicode(attr).endswith(self.attrvalue)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class hasid(Selector):
	"""
	<par>Selector that selects all element nodes where the <lit>id</lit> attribute
	has the specified value.</par>
	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.hasid("logo")</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<img src="http://www.python.org/images/python-logo.gif" id="logo" alt="homepage" border="0" />]]>
	</tty>
	</example>
	"""

	def __init__(self, id):
		self.id = id

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml("id"):
				attr = node.attrs.get_xml("id")
				if not attr.isfancy():
					return unicode(attr) == self.id
		return False

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.id)

	def cssweight(self):
		return CSSWeight(1, 0, 0)


class hasclass(Selector):
	"""
	<par>Selector that selects all element nodes where the <lit>class</lit> attribute
	has the specified value.</par>
	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.hasclass("reference")</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a class="reference" href="http://www.python.org/search">Advanced Search</a>
	<a href="http://www.python.org/about/success/rackspace" class="reference">Rackspace</a>
	<a href="http://www.python.org/about/success/ilm" class="reference">Industrial Light and Magic</a>
	<a href="http://www.python.org/about/success/astra" class="reference">AstraZeneca</a>]]>
	<rep>...</rep>
	</tty>
	</example>
	"""

	def __init__(self, classname):
		self.classname = classname

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml("class"):
				attr = node.attrs.get_xml("class")
				if not attr.isfancy():
					return self.classname in unicode(attr).split()
		return False

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.classname)

	def cssweight(self):
		return CSSWeight(0, 1, 0)


class inattr(Selector):
	"""
	<par>Selector that selects all attribute nodes and nodes inside of attributes.</par>
	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.inattr &amp; xsc.Text</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	text/html; charset=utf-8
	content-type
	python programming language object oriented web free source	
	<rep>...</rep>
	</tty>
	</example>
	"""
	def match(self, path):
		return any(isinstance(node, xsc.Attr) for node in path)

	def __str__(self):
		return "inattr"


inattr = inattr()


class Combinator(Selector):
	"""
	<par>A <class>Combinator</class> is a selector that transforms one or combines
	two or more other selectors in a certain way.</par>
	"""


class BinaryCombinator(Combinator):
	"""
	<par>A <class>BinaryCombinator</class> is a combinator that combines two selector:
	the left hand selector and the right hand selector.</par>
	"""
	symbol = None

	def __init__(self, left, right):
		self.left = left
		self.right = right

	def __str__(self):
		left = str(self.left)
		if isinstance(self.left, Combinator) and not isinstance(self.left, self.__class__):
			left = "(%s)" % left
		right = str(self.right)
		if isinstance(self.right, Combinator) and not isinstance(self.right, self.__class__):
			right = "(%s)" % right
		return "%s%s%s" % (left, self.symbol, right)

	def cssweight(self):
		return self.left.cssweight()+self.right.cssweight()


class ChildCombinator(BinaryCombinator):
	"""
	<par>A <class>ChildCombinator</class> is a <class>BinaryCombinator</class>.
	To match the <class>ChildCombinator</class> the node must match the
	right hand selector and it's immediate parent must match the left hand
	selector (i.e. it works similar to the <lit>&gt;</lit> combinator in &css;
	or the <lit>/</lit> combinator in XPath.</par>

	<par><class>ChildCombinator</class>s can be created via the division operator (<lit>/</lit>):</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>html.a/html.img</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<img src="http://www.python.org/images/python-logo.gif" alt="homepage" id="logo" border="0" />
	<img id="skiptonav" alt="skip to navigation" src="http://www.python.org/images/trans.gif" border="0" />
	<img id="skiptocontent" alt="skip to content" src="http://www.python.org/images/trans.gif" border="0" />
	<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />]]>
	</tty>
	</example>
	"""
	def match(self, path):
		if path and self.right.match(path):
			return self.left.match(path[:-1])
		return False

	symbol = " / "


class DescendantCombinator(BinaryCombinator):
	"""
	<par>A <class>DescendantCombinator</class> is a <class>BinaryCombinator</class>.
	To match the <class>DescendantCombinator</class> the node must match the
	right hand selector and any of it's ancestor nodes must match the left hand
	selector (i.e. it works similar to the descendant combinator in &css;
	or the <lit>//</lit> combinator in XPath.</par>

	<par><class>DescendantCombinator</class>s can be created via the floor division
	operator (<lit>//</lit>):</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>html.div//html.img</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<img id="skiptonav" alt="skip to navigation" src="http://www.python.org/images/trans.gif" border="0" />
	<img id="skiptocontent" alt="skip to content" src="http://www.python.org/images/trans.gif" border="0" />
	<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />]]>
	</tty>
	</example>
	"""
	def match(self, path):
		if path and self.right.match(path):
			while path:
				path = path[:-1]
				if self.left.match(path):
					return True
		return False

	symbol = " // "


class AdjacentSiblingCombinator(BinaryCombinator):
	"""
	<par>A <class>AdjacentSiblingCombinator</class> is a <class>BinaryCombinator</class>.
	To match the <class>AdjacentSiblingCombinator</class> the node must match the
	right hand selector and the immediately preceding sibling must match the left
	hand selector.</par>

	<par><class>AdjacentSiblingCombinator</class>s can be created via the
	multiplication operator (<lit>*</lit>). The following example outputs all links
	inside those <class>p</class> elements that immediately follow a
	<class>h2</class> element:</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>html.h2*html.p/html.a</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a href="http://www.scipy.org/SciPy2007" class="reference">SciPy Conference</a>
	<a href="https://www.enthought.com/scipy07/" class="reference">early registration</a>
	<a href="http://www.europython.org/sections/registration_issues/how-to-register" class="reference">Online registration</a>
	<a href="http://europython.org/" class="reference">EuroPython 2007</a>
	<a href="http://www.osdc.com.au/papers/cfp.html" class="reference">Call For Papers</a>
	<a href="http://www.swa.hpi.uni-potsdam.de/dls07/" class="reference">DLS 2007</a>
	<a href="http://pythonpapers.cgpublisher.com/" class="reference">The Python Papers</a>
	<a href="http://www.pyconuk.org/" class="reference">PyCon UK</a>
	<a href="http://www.pyconuk.org/submit.html" class="reference">proposals for talks</a>
	<a href="http://www.pycon.it/registration/" class="reference">registration online</a>]]>
	</tty>
	</example>
	"""

	def match(self, path):
		if len(path) >= 2 and self.right.match(path):
			# Find sibling
			node = path[-1]
			sibling = None
			for child in path[-2]:
				if child is node:
					break
				sibling = child
			if sibling is not None:
				return self.left.match(path[:-1]+[sibling])
		return False

	symbol = " * "


class GeneralSiblingCombinator(BinaryCombinator):
	"""
	<par>A <class>GeneralSiblingCombinator</class> is a <class>BinaryCombinator</class>.
	To match the <class>GeneralSiblingCombinator</class> the node must match the
	right hand selector and any of the preceding siblings must match the left
	hand selector.</par>

	<par><class>AdjacentSiblingCombinator</class>s can be created via the
	exponentiation operator (<lit>**</lit>). The following example outputs all links
	that are not the first links inside their parent (i.e. they have another link
	among their preceding siblings):</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>html.a**html.a</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a href="http://www.python.org/about/success/ilm" class="reference">Industrial Light and Magic</a>
	<a href="http://www.python.org/about/success/astra" class="reference">AstraZeneca</a>
	<a href="http://www.python.org/about/success/honeywell" class="reference">Honeywell</a>
	<a href="http://www.python.org/about/success" class="reference">and many others</a>
	<a href="http://www.zope.org/">Zope</a>]]>
	<rep>...</rep>
	</tty>
	</example>
	"""

	def match(self, path):
		if len(path) >= 2 and self.right.match(path):
			node = path[-1]
			for child in path[-2]:
				if child is node: # no previous siblings
					return False
				if self.left.match(path[:-1]+[child]):
					return True
		return False

	symbol = " ** "


class ChainedCombinator(Combinator):
	"""
	<par>A <class>ChainedCombinator</class> combines any number of other
	selectors.</par>
	"""

	symbol = None

	def __init__(self, *selectors):
		self.selectors = selectors

	def __str__(self):
		v = []
		for selector in self.selectors:
			s = str(selector)
			if isinstance(selector, Combinator) and not isinstance(selector, self.__class__):
				s = "(%s)" % s
			v.append(s)
		return self.symbol.join(v)

	def cssweight(self):
		raise TypeError("no weight info for chained combinator")


class OrCombinator(ChainedCombinator):
	"""
	<par>An <class>OrCombinator</class> is a <class>ChainedCombinator</class> where
	the node must match at least one of the selectors to match the <class>OrCombinator</class>.
	An <class>OrCombinator</class> can be created with the binary or operator (<lit>|</lit>).</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.hasattr("href") | xfind.hasattr("src")</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<link type="application/rss+xml" title="RSS" rel="alternate" href="http://www.python.org/channews.rdf" />
	<link media="screen" type="text/css" id="screen-switcher-stylesheet" rel="stylesheet" href="http://www.python.org/styles/screen-switcher-default.css" />
	<link media="scReen" type="text/css" rel="stylesheet" href="http://www.python.org/styles/netscape4.css" />
	<link media="print" type="text/css" rel="stylesheet" href="http://www.python.org/styles/print.css" />
	<link media="screen" type="text/css" title="large text" rel="alternate stylesheet" href="http://www.python.org/styles/largestyles.css" />
	<link media="screen" type="text/css" title="default fonts" rel="alternate stylesheet" href="http://www.python.org/styles/defaultfonts.css" />
	<script src="http://www.python.org/js/iotbs2-key-directors-load.js" type="text/javascript"></script>
	<script src="http://www.python.org/js/iotbs2-directors.js" type="text/javascript"></script>
	<script src="http://www.python.org/js/iotbs2-core.js" type="text/javascript"></script>
	<a accesskey="1" id="logolink" href="http://www.python.org/"><img alt="homepage" src="http://www.python.org/images/python-logo.gif" id="logo" border="0" /></a>]]>
	<rep>...</rep>
	</tty>
	</example>
	"""

	def match(self, path):
		return any(selector.match(path) for selector in self.selectors)

	symbol = " | "

	def __or__(self, other):
		return OrCombinator(*(self.selectors + (xsc.makewalkfilter(other),)))


class AndCombinator(ChainedCombinator):
	"""
	<par>An <class>AndCombinator</class> is a <class>ChainedCombinator</class> where
	the node must match all of the combined selectors to match the <class>AndCombinator</class>.
	An <class>AndCombinator</class> can be created with the binary and operator (<lit>&amp;</lit>).</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>html.input & xfind.hasattr("id")</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<input id="domains" name="domains" value="www.python.org" type="hidden" />
	<input id="sitesearch" name="sitesearch" value="www.python.org" type="hidden" />
	<input id="sourceid" name="sourceid" value="google-search" type="hidden" />
	<input id="q" class="input-text" name="q" type="text" />
	<input id="submit" value="search" name="submit" type="submit" class="input-button" />]]>
	</tty>
	</example>
	"""

	def match(self, path):
		return all(selector.match(path) for selector in self.selectors)

	def __and__(self, other):
		return AndCombinator(*(self.selectors + (xsc.makewalkfilter(other),)))

	symbol = " & "


class NotCombinator(Combinator):
	"""
	<par>A <class>NotCombinator</class> inverts the selection logic of the
	underlying selector, i.e. a node matches only if it does not match the underlying
	selector. A <class>NotCombinator</class> can be created with the unary inversion operator (<lit>~</lit>).</par>

	<par>The following example outputs all images that don't have a <lit>border</lit> attribute:</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>html.img &amp; ~xfind.hasattr("border")</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />]]>
	</tty>
	</example>
	"""

	def __init__(self, selector):
		self.selector = selector

	def match(self, path):
		return not self.selector.match(path)

	def __str__(self):
		if isinstance(self.selector, Combinator) and not isinstance(self.selector, NotCombinator):
			return "~(%s)" % self.selector
		else:
			return "~%s" % self.selector


class CallableSelector(Selector):
	"""
	<par>A <class>CallableSelector</class> is a selector that calls a user specified
	callable to select nodes. The callable gets passed the path and must return
	a bool specifying whether this path is selected. A <class>CallableSelector</class>
	is created implicitely whenever a callable is passed to a method that expects
	a walk filter.</par>

	<par>The following example outputs all links that point outside the <lit>python.org</lit> domain:</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>def foreignlink(path):</input>
	<prompt>... </prompt><input>	return path and isinstance(path[-1], html.a) and not path[-1].attrs.href.asURL().server.endswith(".python.org")</input>
	<prompt>... </prompt><input></input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>foreignlink</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a href="http://homegain.com/" class="reference">HomeGain.com</a>
	<a href="http://www.zope.org/">Zope</a>
	<a href="http://www.djangoproject.com/">Django</a>
	<a href="http://www.turbogears.org/">TurboGears</a>
	<a href="http://pyxml.sourceforge.net/topics/">XML</a>]]>
	<rep>..</rep>
	</tty>
	</example>
	"""
	def __init__(self, func):
		self.func = func

	def match(self, path):
		return self.func(path)

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.func)


class nthchild(Selector):
	def __init__(self, index):
		self.index = index

	def match(self, path):
		if len(path) >= 2:
			if self.index in ("even", "odd"):
				for (i, child) in enumerate(path[-2]):
					if child is path[-1]:
						return (i % 2) == (self.index == "odd")
			else:
				try:
					return path[-2][self.index] is path[-1]
				except IndexError:
					return False
		return False

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.index)


class nthoftype(Selector):
	def __init__(self, index, *types):
		self.index = index
		self.types = types

	def _find(self, path):
		types = self.types if self.types else path[-1].__class__
		for child in path[-2]:
			if isinstance(child, types):
				yield child

	def match(self, path):
		if len(path) >= 2:
			if self.index in ("even", "odd"):
				for (i, child) in enumerate(self._find(path)):
					if child is path[-1]:
						return (i % 2) == (self.index == "odd")
			else:
				try:
					return misc.item(self._find(path), self.index) is path[-1]
				except IndexError:
					return False
		return False

	def __str__(self):
		if self.types:
			return "%s(%r, %s)" % (self.__class__.__name__, self.index, ", ".join("%s.%s" % (type.__module__, type.__name__) for type in self.types))
		else:
			return "%s(%r)" % (self.__class__.__name__, self.index)


###
### CSS helper functions
###

def _is_nth_node(iterator, node, index):
	# Return whether node is the index'th node in iterator (starting at 1)
	# index is an int or int string or "even" or "odd"
	if index == "even":
		for (i, child) in enumerate(iterator):
			if child is node:
				return i % 2 == 1
		return False
	elif index == "odd":
		for (i, child) in enumerate(iterator):
			if child is node:
				return i % 2 == 0
		return False
	else:
		if not isinstance(index, (int, long)):
			try:
				index = int(index)
			except ValueError:
				raise ValueError("illegal argument %r" % index)
			else:
				if index < 1:
					return False
		try:
			return iterator[index-1] is node
		except IndexError:
			return False


def _is_nth_last_node(iterator, node, index):
	# Return whether node is the index'th last node in iterator
	# index is an int or int string or "even" or "odd"
	if index == "even":
		pos = None
		for (i, child) in enumerate(iterator):
			if child is node:
				pos = i
		return pos is None or (i-pos) % 2 == 1
	elif index == "odd":
		pos = None
		for (i, child) in enumerate(iterator):
			if child is node:
				pos = i
		return pos is None or (i-pos) % 2 == 0
	else:
		if not isinstance(index, (int, long)):
			try:
				index = int(index)
			except ValueError:
				raise ValueError("illegal argument %r" % index)
			else:
				if index < 1:
					return False
		try:
			return iterator[-index] is node
		except IndexError:
			return False


def _children_of_type(node, type):
	for child in node:
		if isinstance(child, xsc.Element) and child.xmlname == type:
			yield child


###
### CSS selectors
###

class CSSWeightedSelector(Selector):
	def cssweight(self):
		return CSSWeight(0, 1, 0)


class CSSHasAttributeSelector(CSSWeightedSelector):
	def __init__(self, attributename):
		self.attributename = attributename

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attributename):
				return node.attrs.has_xml(self.attributename)
		return False

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.attributename)


class CSSAttributeListSelector(CSSWeightedSelector):
	def __init__(self, attributename, attributevalue):
		self.attributename = attributename
		self.attributevalue = attributevalue

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attributename):
				attr = node.attrs.get_xml(self.attributename)
				return self.attributevalue in unicode(attr).split()
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attributename, self.attributevalue)


class CSSAttributeLangSelector(CSSWeightedSelector):
	def __init__(self, attributename, attributevalue):
		self.attributename = attributename
		self.attributevalue = attributevalue

	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attributename):
				attr = node.attrs.get_xml(self.attributename)
				parts = unicode(attr).split("-", 1)
				if parts:
					return parts[0] == self.attributevalue
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attributename, self.attributevalue)


class CSSFirstChildSelector(CSSWeightedSelector):
	def match(self, path):
		return len(path) >= 2 and _is_nth_node(path[-2][xsc.Element], path[-1], 1)

	def __str__(self):
		return "CSSFirstChildSelector()"


class CSSLastChildSelector(CSSWeightedSelector):
	def match(self, path):
		return len(path) >= 2 and _is_nth_last_node(path[-2][xsc.Element], path[-1], 1)

	def __str__(self):
		return "CSSLastChildSelector()"


class CSSFirstOfTypeSelector(CSSWeightedSelector):
	def match(self, path):
		if len(path) >= 2:
			node = path[-1]
			return isinstance(node, xsc.Element) and _is_nth_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, 1)
		return False

	def __str__(self):
		return "CSSFirstOfTypeSelector()"


class CSSLastOfTypeSelector(CSSWeightedSelector):
	def match(self, path):
		if len(path) >= 2:
			node = path[-1]
			return isinstance(node, xsc.Element) and _is_nth_last_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, 1)
		return False

	def __str__(self):
		return "CSSLastOfTypeSelector()"


class CSSOnlyChildSelector(CSSWeightedSelector):
	def match(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				for child in path[-2][xsc.Element]:
					if child is not node:
						return False
				return True
		return False

	def __str__(self):
		return "CSSOnlyChildSelector()"


class CSSOnlyOfTypeSelector(CSSWeightedSelector):
	def match(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				for child in _children_of_type(path[-2], node.xmlname):
					if child is not node:
						return False
				return True
		return False

	def __str__(self):
		return "CSSOnlyOfTypeSelector()"


class CSSEmptySelector(CSSWeightedSelector):
	def match(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element):
				for child in path[-1].content:
					if isinstance(child, xsc.Element) or (isinstance(child, xsc.Text) and child):
						return False
				return True
		return False

	def __str__(self):
		return "CSSEmptySelector()"


class CSSRootSelector(CSSWeightedSelector):
	def match(self, path):
		return len(path) == 1 and isinstance(path[-1], xsc.Element)

	def __str__(self):
		return "CSSRootSelector()"


class CSSLinkSelector(CSSWeightedSelector):
	def match(self, path):
		if path:
			node = path[-1]
			return isinstance(node, xsc.Element) and node.xmlns=="http://www.w3.org/1999/xhtml" and node.xmlname=="a" and "href" in node.attrs
		return False

	def __str__(self):
		return "%s()" % self.__class__.__name__


class CSSInvalidPseudoSelector(CSSWeightedSelector):
	def match(self, path):
		return False

	def __str__(self):
		return "%s()" % self.__class__.__name__


class CSSHoverSelector(CSSInvalidPseudoSelector):
	pass


class CSSActiveSelector(CSSInvalidPseudoSelector):
	pass


class CSSVisitedSelector(CSSInvalidPseudoSelector):
	pass


class CSSFunctionSelector(CSSWeightedSelector):
	def __init__(self, value=None):
		self.value = value

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.value)


class CSSNthChildSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				return _is_nth_node(path[-2][xsc.Element], node, self.value)
		return False


class CSSNthLastChildSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				return _is_nth_last_node(path[-2][xsc.Element], node, self.value)
		return False


class CSSNthOfTypeSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				return _is_nth_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, self.value)
		return False


class CSSNthLastOfTypeSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) >= 2:
			node = path[-1]
			if isinstance(node, xsc.Element):
				return _is_nth_last_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, self.value)
		return False


class CSSTypeSelector(Selector):
	def __init__(self, type="*", xmlns="*", *selectors):
		self.type = type
		self.xmlns = xsc.nsname(xmlns)
		self.selectors = [] # id, class, attribute etc. selectors for this node

	def match(self, path):
		if not path:
			return False
		node = path[-1]
		if self.type != "*" and node.xmlname != self.type:
			return False
		if self.xmlns != "*" and node.xmlns != self.xmlns:
			return False
		for selector in self.selectors:
			if not selector.match(path):
				return False
		return True

	def __str__(self):
		v = [self.__class__.__name__, "("]
		if self.type != "*" or self.xmlns != "*" or self.selectors:
			v.append(repr(self.type))
		if self.xmlns != "*" or self.selectors:
			v.append(", ")
			v.append(repr(self.xmlns))
		for selector in self.selectors:
			v.append(", ")
			v.append(str(selector))
		v.append(")")
		return "".join(v)

	def cssweight(self):
		result = CSSWeight(0, 0, int(self.type != "*"))
		for selector in self.selectors:
			result += selector.cssweight()
		return result


class CSSAdjacentSiblingCombinator(BinaryCombinator):
	"""
	<par>A <class>CSSAdjacentSiblingCombinator</class> work similar to an
	<class>AdjacentSiblingCombinator</class> except that only preceding elements
	are considered.</par>
	"""

	def match(self, path):
		if len(path) >= 2 and self.right.match(path):
			# Find sibling
			node = path[-1]
			sibling = None
			for child in path[-2][xsc.Element]:
				if child is node:
					break
				sibling = child
			if sibling is not None:
				return self.left.match(path[:-1]+[sibling])
		return False

	def __str__(self):
		return "%s(%s, %s)" % (self.__class__.__name__, self.left, self.right)


class CSSGeneralSiblingCombinator(BinaryCombinator):
	"""
	<par>A <class>CSSGeneralSiblingCombinator</class> work similar to an
	<class>GeneralSiblingCombinator</class> except that only preceding elements
	are considered.</par>
	"""

	def match(self, path):
		if len(path) >= 2 and self.right.match(path):
			node = path[-1]
			for child in path[-2][xsc.Element]:
				if child is node: # no previous element siblings
					return False
				if self.left.match(path[:-1]+[child]):
					return True
		return False

	def __str__(self):
		return "%s(%s, %s)" % (self.__class__.__name__, self.left, self.right)


_attributecombinator2class = {
	"=": attrhasvalue_xml,
	"~=": CSSAttributeListSelector,
	"|=": CSSAttributeLangSelector,
	"^=": attrstartswith_xml,
	"$=": attrendswith_xml,
	"*=": attrcontains_xml,
}

_combinator2class = {
	" ": DescendantCombinator,
	">": ChildCombinator,
	"+": CSSAdjacentSiblingCombinator,
	"~": CSSGeneralSiblingCombinator,
}

_pseudoname2class = {
	"first-child": CSSFirstChildSelector,
	"last-child": CSSLastChildSelector,
	"first-of-type": CSSFirstOfTypeSelector,
	"last-of-type": CSSLastOfTypeSelector,
	"only-child": CSSOnlyChildSelector,
	"only-of-type": CSSOnlyOfTypeSelector,
	"empty": CSSEmptySelector,
	"root": CSSRootSelector,
	"hover": CSSHoverSelector,
	"link": CSSLinkSelector,
	"visited": CSSVisitedSelector,
	"active": CSSActiveSelector,
}

_function2class = {
	"nth-child": CSSNthChildSelector,
	"nth-last-child": CSSNthLastChildSelector,
	"nth-of-type": CSSNthOfTypeSelector,
	"nth-last-of-type": CSSNthLastOfTypeSelector,
}


def css(selectors, prefixes=None):
	"""
	Create a walk filter that will yield all nodes that match the specified
	&css; expression. <arg>selectors</arg> can be a string or a
	<class>cssutils.css.selector.Selector</class> object. <arg>prefixes</arg>
	may is a mapping mapping namespace prefixes to namespace names.
	"""
		
	if isinstance(selectors, basestring):
		if prefixes is not None:
			prefixes = dict((key, xsc.nsname(value)) for (key, value) in prefixes.iteritems())
			selectors = "%s\n%s{}" % ("\n".join("@namespace %s %r;" % (key if key is not None else "", value) for (key, value) in prefixes.iteritems()), selectors)
		else:
			selectors = "%s{}" % selectors
		for rule in cssutils.CSSParser().parseString(selectors).cssRules:
			if isinstance(rule, cssstylerule.CSSStyleRule):
				selectors = rule.selectorList
				break
		else:
			raise ValueError("can't happen")
	elif isinstance(selectors, cssstylerule.CSSStyleRule):
		selectors = selectors.selectorList
	elif isinstance(selectors, cssselector.Selector):
		selectors = [selectors]
	else:
		raise TypeError("can't handle %r" % type(selectors))
	orcombinators = []
	for selector in selectors:
		rule = root = CSSTypeSelector()
		prefix = None
		attributename = None
		attributevalue = None
		combinator = None
		inattr = False
		for x in selector.seq:
			t = x["type"]
			v = x["value"]
			if t == "prefix":
				prefix = v
			elif t == "pipe":
				if prefix != "*":
					try:
						xmlns = prefixes[prefix]
					except KeyError:
						raise xsc.IllegalPrefixError(prefix)
					rule.xmlns = xmlns
				prefix = None
			elif t == "type":
				rule.type = v
			elif t == "id":
				rule.selectors.append(hasid(v.lstrip("#")))
			elif t == "classname":
				rule.selectors.append(hasclass(v))
			elif t == "pseudoname":
				try:
					rule.selectors.append(_pseudoname2class[v]())
				except KeyError:
					raise ValueError("unknown pseudoname %s" % v)
			elif t == "function":
				try:
					rule.selectors.append(_function2class[v.rstrip("(")]())
				except KeyError:
					raise ValueError("unknown function %s" % v)
				rule.function = v
			elif t == "functionvalue":
				rule.selectors[-1].value = v
			elif t == "attributename":
				attributename = v
			elif t == "attributevalue":
				if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
					v = v[1:-1]
				attributevalue = v
			elif t == "attribute selector":
				combinator = None
				inattr = True
			elif t == "attribute selector end":
				if combinator is None:
					rule.selectors.append(CSSHasAttributeSelector(attributename))
				else:
					try:
						rule.selectors.append(_attributecombinator2class[combinator](attributename, attributevalue))
					except KeyError:
						raise ValueError("unknown combinator %s" % attributevalue)
				inattr = False
			elif t == "combinator":
				if inattr:
					combinator = v
				else:
					try:
						rule = CSSTypeSelector()
						root = _combinator2class[v](root, rule)
					except KeyError:
						raise ValueError("unknown combinator %s" % v)
					xmlns = "*"
		orcombinators.append(root)
	return orcombinators[0] if len(orcombinators) == 1 else OrCombinator(*orcombinators)
