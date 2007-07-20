#! /usr/bin/env python
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
	from cssutils.css import cssnamespacerule
except ImportError:
	pass

from ll import misc
from ll.xist import xsc


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
	<prompt>>>> </prompt><input>for node in doc.walknode(html.a):</input>
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

	def __repr__(self):
		if len(self.types) == 1:
			return "%s.%s" % (self.types[0].__module__, self.types[0].__name__)
		else:
			return "(%s)" % " | ".join("%s.%s" % (type.__module__, type.__name__) for type in self.types)


class hasname(Selector):
	"""
	<par>Selector that selects all nodes that have a specified Python name (which
	only selects elements, processing instructions and entities).</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(xfind.hasname("img")):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<img border="0" src="http://www.python.org/images/python-logo.gif" alt="homepage" id="logo" />
	<img border="0" id="skiptonav" alt="skip to navigation" src="http://www.python.org/images/trans.gif" />
	<img border="0" id="skiptocontent" alt="skip to content" src="http://www.python.org/images/trans.gif" />
	<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />]]>
	</tty>
	</example>
	"""
	def __init__(self, name):
		self.name = name

	def match(self, path):
		if path:
			node = path[-1]
			return IsInstanceSelector(node, (xsc.Element, xsc.ProcInst, xsc.Entity)) and node.__class__.__name__ == self.name
		return False

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.name)


class hasname_xml(Selector):
	"""
	<class>hasname_xml</class> work similar to <pyref class="hasname"><class>hasname</class></pyref>
	except that the specified name is treated as the &xml; name, not the Python name.
	"""
	def __init__(self, name):
		self.name = name

	def match(self, path):
		if path:
			node = path[-1]
			return IsInstanceSelector(node, (xsc.Element, xsc.ProcInst, xsc.Entity)) and node.xmlname == self.name
		return False

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.name)


class IsSelector(Selector):
	"""
	<par>Selector that selects one specific node in the tree. This can be
	combined with other selectors via <pyref class="ChildCombinator"><class>ChildCombinator</class>s</pyref>
	or <pyref class="DescendantCombinator"><class>DescendantCombinator</class>s</pyref>
	to select children of this specific node. You can either create an
	<class>IsSelector</class> directly or simply pass a node to a function that
	expects a walk filter.</par>
	"""
	def __init__(self, node):
		self.node = node

	def match(self, path):
		return path and path[-1] is self.node

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.node)


class isroot(Selector):
	def match(self, path):
		return len(path) == 1

	def __repr__(self):
		return "isroot"


isroot = isroot()


class empty(Selector):
	"""
	<par>Selector that selects all empty elements or fragments.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(xfind.empty):</input>
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

	def __repr__(self):
		return "empty"


empty = empty()


class onlychild(Selector):
	"""
	<par>Selector that selects all node that are the only child of their parents.</par>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(xfind.onlychild & html.a):</input>
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

	def __repr__(self):
		return "onlychild"


onlychild = onlychild()


class onlyoftype(Selector):
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

	def __repr__(self):
		return "onlyoftype"


onlyoftype = onlyoftype()


class hasattr(Selector):
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

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join(repr(attrname) for attrname in self.attrnames))


class hasattr_xml(Selector):
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

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join(repr(attrname) for attrname in self.attrnames))


class attrhasvalue(Selector):
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

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrhasvalue_xml(Selector):
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

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)

	def __str__(self):
		return "[%s=%r]" % (self.attributename, self.attributevalue)


class attrcontains(Selector):
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

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrcontains_xml(Selector):
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

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)

	def __str__(self):
		return "[%s*=%r]" % (self.attrname, self.attrvalue)


class attrstartswith(Selector):
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

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrstartswith_xml(Selector):
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

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)

	def __str__(self):
		return "[%s^=%r]" % (self.attrname, self.attrvalue)


class attrendswith(Selector):
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

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrendswith_xml(Selector):
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

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)

	def __str__(self):
		return "[%s$=%r]" % (self.attributename, self.attributevalue)


class hasid(Selector):
	"""
	<par>Selector that selects all element nodes where the <lit>id</lit> attribute
	has the specified value.</par>
	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(xfind.hasid("logo")):</input>
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

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.id)

	def __str__(self):
		return "#%s" % (self.id)


class hasclass(Selector):
	"""
	<par>Selector that selects all element nodes where the <lit>class</lit> attribute
	has the specified value.</par>
	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(xfind.hasclass("reference")):</input>
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

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.classname)

	def __str__(self):
		return ".%s" % (self.classname)


class inattr(Selector):
	"""
	<par>Selector that is true only if the node is an attribute or is inside an
	attribute.</par>
	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseURL("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(xfind.inattr & xsc.Text):</input>
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

	def __repr__(self):
		return "inattr"


inattr = inattr()


class Combinator(Selector):
	pass


class BinaryCombinator(Combinator):
	reprsymbol = None

	def __init__(self, left, right):
		self.left = left
		self.right = right

	def __repr__(self):
		left = repr(self.left)
		if isinstance(self.left, Combinator) and not isinstance(self.left, self.__class__):
			left = "(%s)" % left
		right = repr(self.right)
		if isinstance(self.right, Combinator) and not isinstance(self.right, self.__class__):
			right = "(%s)" % right
		return "%s%s%s" % (left, self.reprsymbol, right)


class ChildCombinator(BinaryCombinator):
	def match(self, path):
		if path and self.right.match(path):
			return self.left.match(path[:-1])
		return False

	reprsymbol = " / "

	def __str__(self):
		return "%s>%s" % (self.left, self.right)


class DescendantCombinator(BinaryCombinator):
	def match(self, path):
		if path and self.right.match(path):
			while path:
				path = path[:-1]
				if self.left.match(path):
					return True
		return False

	reprsymbol = " // "

	def __str__(self):
		return "%s %s" % (self.left, self.right)


class AdjacentSiblingCombinator(BinaryCombinator):
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

	reprsymbol = " * "

	def __str__(self):
		return "%s+%s" % (self.left, self.right)


class GeneralSiblingCombinator(BinaryCombinator):
	def match(self, path):
		if len(path) >= 2 and self.right.match(path):
			node = path[-1]
			for child in path[-2][xsc.Element]:
				if child is node:
					return False
				if self.left.match(path[:-1]+[child]):
					return True
		return False

	reprsymbol = " ** "

	def __str__(self):
		return "%s~%s" % (self.left, self.right)


class ChainedCombinator(Combinator):
	reprsymbol = None

	def __init__(self, *selectors):
		self.selectors = selectors

	def __repr__(self):
		v = []
		for selector in self.selectors:
			s = repr(selector)
			if isinstance(selector, Combinator) and not isinstance(selector, self.__class__):
				s = "(%s)" % s
			v.append(s)
		return self.reprsymbol.join(v)


class OrCombinator(ChainedCombinator):
	def match(self, path):
		return any(selector.match(path) for selector in self.selectors)

	reprsymbol = " | "

	def __str__(self):
		return ", ".join(str(selector) for selector in self.selectors)


class AndCombinator(ChainedCombinator):
	def match(self, path):
		return all(selector.match(path) for selector in self.selectors)

	reprsymbol = " & "

	def __str__(self):
		return " and ".join(str(selector) for selector in self.selectors)


class NotCombinator(Combinator):
	def __init__(self, selector):
		self.selector = selector

	def match(self, path):
		return not self.selector.match(path)

	def __repr__(self):
		if isinstance(self.selector, Combinator) and not isinstance(self.selector, NotCombinator):
			return "~(%r)" % self.selector
		else:
			return "~%r" % self.selector


class CallableSelector(Selector):
	def __init__(self, func):
		self.func = func

	def match(self, path):
		return self.func(path)

	def __repr__(self):
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

	def __repr__(self):
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

	def __repr__(self):
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
	for child in node.content:
		if isinstance(child, xsc.Element) and child.xmlname == type:
			yield child


###
### CSS selectors
###

class CSSHasAttributeSelector(Selector):
	def __init__(self, attributename):
		self.attributename = attributename

	def match(self, path):
		node = path[-1]
		if not isinstance(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attributename):
			return False
		return node.attrs.has_xml(self.attributename)

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.attributename)

	def __str__(self):
		return "[%s]" % self.attributename


class CSSAttributeListSelector(Selector):
	def __init__(self, attributename, attributevalue):
		self.attributename = attributename
		self.attributevalue = attributevalue

	def match(self, path):
		node = path[-1]
		if not isinstance(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attributename):
			return False
		attr = node.attrs.get_xml(self.attributename)
		return self.attributevalue in unicode(attr).split()

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attributename, self.attributevalue)

	def __str__(self):
		return "[%s~=%r]" % (self.attributename, self.attributevalue)


class CSSAttributeLangSelector(Selector):
	def __init__(self, attributename, attributevalue):
		self.attributename = attributename
		self.attributevalue = attributevalue

	def match(self, path):
		node = path[-1]
		if not isinstance(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attributename):
			return False
		attr = node.attrs.get_xml(self.attributename)
		parts = unicode(attr).split("-", 1)
		if not parts:
			return False
		return parts[0] == self.attributevalue

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attributename, self.attributevalue)

	def __str__(self):
		return "[%s|=%r]" % (self.attributename, self.attributevalue)


class CSSFirstChildSelector(Selector):
	def match(self, path):
		return len(path) >= 2 and _is_nth_node(path[-2][xsc.Element], path[-1], 1)

	def __str__(self):
		return ":first-child"


class CSSLastChildSelector(Selector):
	def match(self, path):
		return len(path) >= 2 and _is_nth_last_node(path[-2][xsc.Element], path[-1], 1)

	def __str__(self):
		return ":last-child"


class CSSFirstOfTypeSelector(Selector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		return isinstance(node, xsc.Element) and _is_nth_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, 1)
	def __str__(self):

		return ":first-of-type"


class CSSLastOfTypeSelector(Selector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		return isinstance(node, xsc.Element) and _is_nth_last_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, 1)

	def __str__(self):
		return ":last-of-type"


class CSSOnlyChildSelector(Selector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		for child in path[-2][xsc.Element]:
			if child is not node:
				return False
		return True

	def __str__(self):
		return ":only-child"


class CSSOnlyOfTypeSelector(Selector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance(node, xsc.Element):
			return False
		for child in _children_of_type(path[-2], node.xmlname):
			if child is not node:
				return False
		return True

	def __str__(self):
		return ":only-of-type"


class CSSEmptySelector(Selector):
	def match(self, path):
		if not path:
			return False
		node = path[-1]
		if not isinstance(node, xsc.Element):
			return False
		for child in path[-1].content:
			if isinstance(child, xsc.Element) or (isinstance(child, xsc.Text) and child):
				return False
		return True

	def __str__(self):
		return ":empty"


class CSSRootSelector(Selector):
	def match(self, path):
		return len(path) == 1 and isinstance(path[-1], xsc.Element)

	def __str__(self):
		return ":root"


class CSSFunctionSelector(Selector):
	def __init__(self, value=None):
		self.value = value


class CSSNthChildSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance(node, xsc.Element):
			return False
		return _is_nth_node(path[-2][xsc.Element], node, self.value)

	def __str__(self):
		return ":nth-child(%s)" % self.value


class CSSNthLastChildSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance(node, xsc.Element):
			return False
		return _is_nth_last_node(path[-2][xsc.Element], node, self.value)

	def __str__(self):
		return ":nth-last-child(%s)" % self.value


class CSSNthOfTypeSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance(node, xsc.Element):
			return False
		return _is_nth_node(self._children_of_type(path[-2], node.xmlname), node, self.value)

	def __str__(self):
		return ":nth-of-type(%s)" % self.value


class CSSNthLastOfTypeSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance(node, xsc.Element):
			return False
		return _is_nth_last_node(self._children_of_type(path[-2], node.xmlname), node, self.value)

	def __str__(self):
		return ":nth-last-of-type(%s)" % self.value


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

	def __repr__(self):
		v = [self.__class__.__name__, "("]
		if self.type != "*" or self.xmlns != "*" or self.selectors:
			v.append(repr(self.type))
		if self.xmlns != "*" or self.selectors:
			v.append(", ")
			v.append(repr(self.xmlns))
		for selector in self.selectors:
			v.append(", ")
			v.append(repr(selector))
		v.append(")")
		return "".join(v)

	def __str__(self):
		v = []
		xmlns = self.xmlns
		if xmlns != "*":
			if xmlns is not None:
				v.append(xmlns)
			v.append("|")
		type = self.type
		if type != "*" or self.selectors or (not self.selectors and self.xmlns=="*"):
			v.append(type)
		for selector in self.selectors:
			v.append(str(selector))
		return "".join(v)


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
	"+": AdjacentSiblingCombinator,
	"~": GeneralSiblingCombinator,
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
	CSS expression. <arg>selectors</arg> can be a string or a
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
	else:
		raise TypeError # FIXME: cssutils object
	orcombinators = []
	for selector in selectors:
		rule = root = CSSTypeSelector()
		prefix = None
		attributename = None
		attributevalue = None
		combinator = None
		inattr = False
		for x in selector.seq:
			type = x["type"]
			value = x["value"]
			if type == "prefix":
				prefix = value
			elif type == "pipe":
				if prefix != "*":
					try:
						xmlns = prefixes[prefix]
					except KeyError:
						raise xsc.IllegalPrefixError(prefix)
					rule.xmlns = xmlns
				prefix = None
			elif type == "type":
				rule.type = value
			elif type == "id":
				rule.selectors.append(hasid(value.lstrip("#")))
			elif type == "classname":
				rule.selectors.append(hasclass(value))
			elif type == "pseudoname":
				try:
					rule.selectors.append(_pseudoname2class[value]())
				except KeyError:
					raise ValueError("unknown pseudoname %s" % value)
			elif type == "function":
				try:
					rule.selectors.append(_function2class[value.rstrip("(")]())
				except KeyError:
					raise ValueError("unknown function %s" % value)
				rule.function = value
			elif type == "functionvalue":
				rule.selectors[-1].value = value
			elif type == "attributename":
				attributename = value
			elif type == "attributevalue":
				if value.startswith("'") and value.endswith("'"):
					value = value[1:-1]
				elif value.startswith('"') and value.endswith('"'):
					value = value[1:-1]
				attributevalue = value
			elif type == "attribute selector":
				combinator = None
				inattr = True
			elif type == "attribute selector end":
				if combinator is None:
					rule.selectors.append(CSSHasAttributeSelector(attributename))
				else:
					try:
						rule.selectors.append(_attributecombinator2class[combinator](attributename, attributevalue))
					except KeyError:
						raise ValueError("unknown combinator %s" % attributevalue)
				inattr = False
			elif type == "combinator":
				if inattr:
					combinator = value
				else:
					try:
						rule = CSSTypeSelector()
						root = _combinator2class[value](root, rule)
					except KeyError:
						raise ValueError("unknown combinator %s" % value)
					xmlns = "*"
		orcombinators.append(root)
	return orcombinators[0] if len(orcombinators) == 1 else OrCombinator(*orcombinators)
