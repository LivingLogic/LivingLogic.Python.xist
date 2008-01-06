# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<p>This module contains XFind and CSS selectors and related classes and functions.</p>

<p>A selector is a &xist; tree traversal filter that traverses the complete
&xml; tree and outputs those nodes specified by the selector. Selectors can
be combined with various operations and form a language comparable to
<a href="http://www.w3.org/TR/xpath">XPath</a> but implemented as Python
expressions.</p>
"""


from ll import misc
from ll.xist import xsc


__docformat__ = "xist"


class CSSWeight(tuple):
	"""
	The specificity of a &css; selector as a 3-item tuple as specified by
	<a href="http://www.w3.org/TR/css3-selectors/#specificity">CSS3</a>.
	"""

	def __new__(cls, a=0, b=0, c=0, d=0):
		return tuple.__new__(cls, (a, b, c, d))

	def __add__(self, other):
		return CSSWeight(self[0]+other[0], self[1]+other[1], self[2]+other[2], self[3]+other[3])

	def __repr__(self):
		return "CSSWeight(%r, %r, %r, %r)" % (self[0], self[1], self[2], self[3])


class Selector(xsc.WalkFilter):
	"""
	Base class for all tree traversal filters that visit the complete tree.
	Whether a node gets output can be specified by overwriting the
	<meth>matchpath</meth> method. Selectors can be combined with various
	operations (see methods below).
	"""

	@misc.notimplemented
	def matchpath(self, path):
		pass

	def filterpath(self, path):
		return (True, xsc.entercontent, xsc.enterattrs) if self.matchpath(path) else (xsc.entercontent, xsc.enterattrs)

	def __div__(self, other):
		"""
		Create a <pyref class="ChildCombinator"><class>ChildCombinator</class></pyref>
		with <self/> as the left hand selector and <arg>other</arg> as the right
		hand selector.
		"""
		return ChildCombinator(self, xsc.makewalkfilter(other))

	def __floordiv__(self, other):
		"""
		Create a <pyref class="DescendantCombinator"><class>DescendantCombinator</class></pyref>
		with <self/> as the left hand selector and <arg>other</arg> as the right
		hand selector.
		"""
		return DescendantCombinator(self, xsc.makewalkfilter(other))

	def __mul__(self, other):
		"""
		Create an <pyref class="AdjacentSiblingCombinator"><class>AdjacentSiblingCombinator</class></pyref>
		with <self/> as the left hand selector and <arg>other</arg> as the right
		hand selector.
		"""
		return AdjacentSiblingCombinator(self, xsc.makewalkfilter(other))

	def __pow__(self, other):
		"""
		Create a <pyref class="GeneralSiblingCombinator"><class>GeneralSiblingCombinator</class></pyref>
		with <self/> as the left hand selector and <arg>other</arg> as the right
		hand selector.
		"""
		return GeneralSiblingCombinator(self, xsc.makewalkfilter(other))

	def __and__(self, other):
		"""
		Create an <pyref class="AndCombinator"><class>AndCombinator</class></pyref>
		from <self/> and <arg>other</arg>.
		"""
		return AndCombinator(self, xsc.makewalkfilter(other))

	def __or__(self, other):
		"""
		Create an <pyref class="OrCombinator"><class>OrCombinator</class></pyref>
		from <self/> and <arg>other</arg>.
		"""
		return OrCombinator(self, xsc.makewalkfilter(other))

	def __invert__(self):
		"""
		Create a <pyref class="NotCombinator"><class>NotCombinator</class></pyref>
		inverting <self/>.
		"""
		return NotCombinator(self)

	def cssweight(self):
		"""
		Return the &css; specificity of <self/> as a
		<pyref class="CSSWeight"><class>CSSWeight</class></pyref> object.
		"""
		return CSSWeight()


class IsInstanceSelector(Selector):
	"""
	<p>Selector that selects all nodes that are instances of the specified type.
	You can either create an <class>IsInstanceSelector</class> object directly
	or simply pass a class to a function that expects a walk filter (this class
	will be automatically wrapped in an <class>IsInstanceSelector</class>).</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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

	def matchpath(self, path):
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
		"""
		Return an <pyref class="nthoftype"><class>nthoftype</class></pyref>
		selector that uses <arg>index</arg> as the index and <self/>s types
		as the types.
		"""
		return nthoftype(index, *self.types)

	def __str__(self):
		if len(self.types) == 1:
			return "%s.%s" % (self.types[0].__module__, self.types[0].__name__)
		else:
			return "(%s)" % " | ".join("%s.%s" % (type.__module__, type.__name__) for type in self.types)


class hasname(Selector):
	"""
	<p>Selector that selects all nodes that have a specified Python name (which
	only selects elements, processing instructions and entities). Also a namespace
	name can be specified as a second argument, which will only select elements
	from the specified namespace.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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

	def matchpath(self, path):
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

	def matchpath(self, path):
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
	<p>Selector that selects one specific node in the tree. This can be
	combined with other selectors via <pyref class="ChildCombinator"><class>ChildCombinator</class>s</pyref>
	or <pyref class="DescendantCombinator"><class>DescendantCombinator</class>s</pyref>
	to select children of this specific node. You can either create an
	<class>IsSelector</class> directly or simply pass a node to a function that
	expects a walk filter.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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

	def matchpath(self, path):
		return path and path[-1] is self.node

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.node)


class isroot(Selector):
	def matchpath(self, path):
		return len(path) == 1

	def __str__(self):
		return "isroot"


isroot = isroot()


class empty(Selector):
	"""
	<p>Selector that selects all empty elements or fragments.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.empty</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<meta content="text/html; charset=utf-8" http-equiv="content-type" />
	<meta content="python programming language object oriented web free source" name="keywords" />
	<meta content="      Home page for Python, an interpreted, interactive, object-oriented, extensible
	      programming language. It provides an extraordinary combination of clarity and
	      versatility, and is free and comprehensively ported. " name="description" />
	<a type="application/rss+xml" href="http://www.python.org/channews.rdf" rel="alternate" title="RSS" />]]>
	<rep>...</rep>
	</tty>
	</example>
	"""

	def matchpath(self, path):
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
	<p>Selector that selects all node that are the only child of their parents.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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

	def matchpath(self, path):
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
	<p>Selector that selects all nodes that are the only nodes of their type among
	their siblings.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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

	def matchpath(self, path):
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
	<p>Selector that selects all element nodes that have an attribute with one
	of the specified Python names. For selecting nodes with global attributes
	the attribute class can be passed.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html, xml</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.hasattr(xml.Attrs.lang)</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<ll.xist.ns.html.html element object (2 children/2 attrs) (from http://www.python.org/:4:?) at 0xb6d71d4c>]]>
	</tty>
	</example>
	"""

	def __init__(self, *attrnames):
		self.attrnames = attrnames

	def matchpath(self, path):
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

	def matchpath(self, path):
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
	<p>Selector that selects all element nodes where an attribute with the
	specified Python name has the specified value. For global attributes
	the attribute class can be passed. Note that
	<pyref module="ll.xist.xsc" class="Attr" method="isfancy">fancy</pyref> attributes
	will not be considered.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.attrhasvalue("rel", "stylesheet")</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a media="screen" type="text/css" href="http://www.python.org/styles/screen-switcher-default.css" rel="stylesheet" id="screen-switcher-stylesheet" />
	<a media="scReen" type="text/css" rel="stylesheet" href="http://www.python.org/styles/netscape4.css" />
	<a media="print" type="text/css" rel="stylesheet" href="http://www.python.org/styles/print.css" />]]>
	</tty>
	</example>
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def matchpath(self, path):
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

	def matchpath(self, path):
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
	<p>Selector that selects all element nodes where an attribute with the
	specified Python name contains the specified substring in its value. For
	global attributes the attribute class can be passed. Note that
	<pyref module="ll.xist.xsc" class="Attr" method="isfancy">fancy</pyref>
	attributes will not be considered.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.attrcontains("rel", "stylesheet")</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a type="text/css" id="screen-switcher-stylesheet" media="screen" rel="stylesheet" href="http://www.python.org/styles/screen-switcher-default.css" />
	<a type="text/css" media="scReen" rel="stylesheet" href="http://www.python.org/styles/netscape4.css" />
	<a type="text/css" media="print" rel="stylesheet" href="http://www.python.org/styles/print.css" />
	<a type="text/css" title="large text" media="screen" rel="alternate stylesheet" href="http://www.python.org/styles/largestyles.css" />
	<a type="text/css" title="default fonts" media="screen" rel="alternate stylesheet" href="http://www.python.org/styles/defaultfonts.css" />]]>
	</tty>
	</example>
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def matchpath(self, path):
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

	def matchpath(self, path):
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
	<p>Selector that selects all element nodes where an attribute with the
	specified Python name starts with the specified string. For global attributes
	the attribute class can be passed. Note that
	<pyref module="ll.xist.xsc" class="Attr" method="isfancy">fancy</pyref> attributes
	will not be considered.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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

	def matchpath(self, path):
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

	def matchpath(self, path):
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
	<p>Selector that selects all element nodes where an attribute with the
	specified Python name ends with the specified string. For global attributes
	the attribute class can be passed. Note that
	<pyref module="ll.xist.xsc" class="Attr" method="isfancy">fancy</pyref> attributes
	will not be considered.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.attrendswith("href", ".css")</em>):</input>
	<prompt>... </prompt><input>\tprint repr(node)</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a href="http://www.python.org/styles/screen-switcher-default.css" type="text/css" rel="stylesheet" id="screen-switcher-stylesheet" media="screen" />
	<a type="text/css" rel="stylesheet" href="http://www.python.org/styles/netscape4.css" media="scReen" />
	<a type="text/css" rel="stylesheet" href="http://www.python.org/styles/print.css" media="print" />
	<a title="large text" type="text/css" rel="alternate stylesheet" href="http://www.python.org/styles/largestyles.css" media="screen" />
	<a title="default fonts" type="text/css" rel="alternate stylesheet" href="http://www.python.org/styles/defaultfonts.css" media="screen" />]]>
	</tty>
	</example>
	"""

	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def matchpath(self, path):
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

	def matchpath(self, path):
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
	<p>Selector that selects all element nodes where the <lit>id</lit> attribute
	has the specified value.</p>
	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.hasid("logo")</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<img src="http://www.python.org/images/python-logo.gif" id="logo" alt="homepage" border="0" />]]>
	</tty>
	</example>
	"""

	def __init__(self, id):
		self.id = id

	def matchpath(self, path):
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
		return CSSWeight(0, 1, 0, 0)


class hasclass(Selector):
	"""
	<p>Selector that selects all element nodes where the <lit>class</lit> attribute
	has the specified value.</p>
	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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

	def matchpath(self, path):
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
		return CSSWeight(0, 0, 1, 0)


class inattr(Selector):
	"""
	<p>Selector that selects all attribute nodes and nodes inside of attributes.</p>
	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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
	def matchpath(self, path):
		return any(isinstance(node, xsc.Attr) for node in path)

	def __str__(self):
		return "inattr"


inattr = inattr()


class Combinator(Selector):
	"""
	<p>A <class>Combinator</class> is a selector that transforms one or combines
	two or more other selectors in a certain way.</p>
	"""


class BinaryCombinator(Combinator):
	"""
	<p>A <class>BinaryCombinator</class> is a combinator that combines two selector:
	the left hand selector and the right hand selector.</p>
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
	<p>A <class>ChildCombinator</class> is a <class>BinaryCombinator</class>.
	To match the <class>ChildCombinator</class> the node must match the
	right hand selector and it's immediate parent must match the left hand
	selector (i.e. it works similar to the <lit>&gt;</lit> combinator in &css;
	or the <lit>/</lit> combinator in XPath).</p>

	<p><class>ChildCombinator</class>s can be created via the division operator (<lit>/</lit>):</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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
	def matchpath(self, path):
		if path and self.right.matchpath(path):
			return self.left.matchpath(path[:-1])
		return False

	symbol = " / "


class DescendantCombinator(BinaryCombinator):
	"""
	<p>A <class>DescendantCombinator</class> is a <class>BinaryCombinator</class>.
	To match the <class>DescendantCombinator</class> the node must match the
	right hand selector and any of it's ancestor nodes must match the left hand
	selector (i.e. it works similar to the descendant combinator in &css;
	or the <lit>//</lit> combinator in XPath).</p>

	<p><class>DescendantCombinator</class>s can be created via the floor division
	operator (<lit>//</lit>):</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>html.div//html.img</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<img id="skiptonav" alt="skip to navigation" src="http://www.python.org/images/trans.gif" border="0" />
	<img id="skiptocontent" alt="skip to content" src="http://www.python.org/images/trans.gif" border="0" />
	<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />]]>
	</tty>
	</example>
	"""
	def matchpath(self, path):
		if path and self.right.matchpath(path):
			while path:
				path = path[:-1]
				if self.left.matchpath(path):
					return True
		return False

	symbol = " // "


class AdjacentSiblingCombinator(BinaryCombinator):
	"""
	<p>A <class>AdjacentSiblingCombinator</class> is a <class>BinaryCombinator</class>.
	To match the <class>AdjacentSiblingCombinator</class> the node must match the
	right hand selector and the immediately preceding sibling must match the left
	hand selector.</p>

	<p><class>AdjacentSiblingCombinator</class>s can be created via the
	multiplication operator (<lit>*</lit>). The following example outputs all links
	inside those <class>p</class> elements that immediately follow a
	<class>h2</class> element:</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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

	def matchpath(self, path):
		if len(path) >= 2 and self.right.matchpath(path):
			# Find sibling
			node = path[-1]
			sibling = None
			for child in path[-2]:
				if child is node:
					break
				sibling = child
			if sibling is not None:
				return self.left.matchpath(path[:-1]+[sibling])
		return False

	symbol = " * "


class GeneralSiblingCombinator(BinaryCombinator):
	"""
	<p>A <class>GeneralSiblingCombinator</class> is a <class>BinaryCombinator</class>.
	To match the <class>GeneralSiblingCombinator</class> the node must match the
	right hand selector and any of the preceding siblings must match the left
	hand selector.</p>

	<p><class>AdjacentSiblingCombinator</class>s can be created via the
	exponentiation operator (<lit>**</lit>). The following example outputs all links
	that are not the first links inside their parent (i.e. they have another link
	among their preceding siblings):</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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

	def matchpath(self, path):
		if len(path) >= 2 and self.right.matchpath(path):
			node = path[-1]
			for child in path[-2]:
				if child is node: # no previous siblings
					return False
				if self.left.matchpath(path[:-1]+[child]):
					return True
		return False

	symbol = " ** "


class ChainedCombinator(Combinator):
	"""
	<p>A <class>ChainedCombinator</class> combines any number of other
	selectors.</p>
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
	<p>An <class>OrCombinator</class> is a <class>ChainedCombinator</class> where
	the node must match at least one of the selectors to match the <class>OrCombinator</class>.
	An <class>OrCombinator</class> can be created with the binary or operator (<lit>|</lit>).</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.hasattr("href") | xfind.hasattr("src")</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a type="application/rss+xml" title="RSS" rel="alternate" href="http://www.python.org/channews.rdf" />
	<a media="screen" type="text/css" id="screen-switcher-stylesheet" rel="stylesheet" href="http://www.python.org/styles/screen-switcher-default.css" />
	<a media="scReen" type="text/css" rel="stylesheet" href="http://www.python.org/styles/netscape4.css" />
	<a media="print" type="text/css" rel="stylesheet" href="http://www.python.org/styles/print.css" />
	<a media="screen" type="text/css" title="large text" rel="alternate stylesheet" href="http://www.python.org/styles/largestyles.css" />
	<a media="screen" type="text/css" title="default fonts" rel="alternate stylesheet" href="http://www.python.org/styles/defaultfonts.css" />
	<script src="http://www.python.org/js/iotbs2-key-directors-load.js" type="text/javascript"></script>
	<script src="http://www.python.org/js/iotbs2-directors.js" type="text/javascript"></script>
	<script src="http://www.python.org/js/iotbs2-core.js" type="text/javascript"></script>
	<a accesskey="1" id="logolink" href="http://www.python.org/"><img alt="homepage" src="http://www.python.org/images/python-logo.gif" id="logo" border="0" /></a>]]>
	<rep>...</rep>
	</tty>
	</example>
	"""

	def matchpath(self, path):
		return any(selector.matchpath(path) for selector in self.selectors)

	symbol = " | "

	def __or__(self, other):
		return OrCombinator(*(self.selectors + (xsc.makewalkfilter(other),)))


class AndCombinator(ChainedCombinator):
	"""
	<p>An <class>AndCombinator</class> is a <class>ChainedCombinator</class> where
	the node must match all of the combined selectors to match the <class>AndCombinator</class>.
	An <class>AndCombinator</class> can be created with the binary and operator (<lit>&amp;</lit>).</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
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

	def matchpath(self, path):
		return all(selector.matchpath(path) for selector in self.selectors)

	def __and__(self, other):
		return AndCombinator(*(self.selectors + (xsc.makewalkfilter(other),)))

	symbol = " & "


class NotCombinator(Combinator):
	"""
	<p>A <class>NotCombinator</class> inverts the selection logic of the
	underlying selector, i.e. a node matches only if it does not match the underlying
	selector. A <class>NotCombinator</class> can be created with the unary inversion operator (<lit>~</lit>).</p>

	<p>The following example outputs all images that don't have a <lit>border</lit> attribute:</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>html.img &amp; ~xfind.hasattr("border")</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />]]>
	</tty>
	</example>
	"""

	def __init__(self, selector):
		self.selector = selector

	def matchpath(self, path):
		return not self.selector.matchpath(path)

	def __str__(self):
		if isinstance(self.selector, Combinator) and not isinstance(self.selector, NotCombinator):
			return "~(%s)" % self.selector
		else:
			return "~%s" % self.selector


class CallableSelector(Selector):
	"""
	<p>A <class>CallableSelector</class> is a selector that calls a user specified
	callable to select nodes. The callable gets passed the path and must return
	a bool specifying whether this path is selected. A <class>CallableSelector</class>
	is created implicitely whenever a callable is passed to a method that expects
	a walk filter.</p>

	<p>The following example outputs all links that point outside the <lit>python.org</lit> domain:</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>def foreignlink(path):</input>
	<prompt>... </prompt><input>	return path and isinstance(path[-1], html.a) and not path[-1].attrs.href.asURL().server.endswith(".python.org")</input>
	<prompt>... </prompt><input></input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>foreignlink</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<a href="http://youtube.com/" class="reference">YouTube.com</a>
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

	def matchpath(self, path):
		return self.func(path)

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.func)


class nthchild(Selector):
	"""
	<p>An <class>nthchild</class> object is a selector that selects every node
	that is the n-th child of its parent. E.g. <lit>nthchild(0)</lit> selects
	every first child, <lit>nthchild(-1)</lit> selects each last child.
	Furthermore <lit>nthchild("even")</lit> selects each first, third, fifth, ...
	child and <lit>nthchild("odd")</lit> selects each second, fourth, sixth, ...
	child.</p>
	"""

	def __init__(self, index):
		self.index = index

	def matchpath(self, path):
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
	"""
	<p>An <class>nthchild</class> object is a selector that selects every node
	that is the n-th node of a specified type among its siblings. Similar to
	<pyref class="nthchild"><class>nthchild</class></pyref> <class>nthoftype</class>
	supports negative and positive indices as well as <lit>"even"</lit> and
	<lit>"odd"</lit>. Which types are checked can be passed explicitely. If no
	types are passed the type of the node itself is used.</p>

	<example>
	<tty>
	<prompt>>>> </prompt><input>from ll.xist import parsers, xfind</input>
	<prompt>>>> </prompt><input>from ll.xist.ns import html</input>
	<prompt>>>> </prompt><input>doc = parsers.parseurl("http://www.python.org", tidy=True)</input>
	<prompt>>>> </prompt><input>for node in doc.walknode(<em>xfind.nthoftype(0, html.h2)</em>):</input>
	<prompt>... </prompt><input>\tprint node.bytes()</input>
	<prompt>... </prompt><input></input>
	<![CDATA[<h2 class="news">SciPy 2007 - Conference for Scientific Computing</h2>]]>
	</tty>
	</example>
	"""

	def __init__(self, index, *types):
		self.index = index
		self.types = types

	def _find(self, path):
		types = self.types if self.types else path[-1].__class__
		for child in path[-2]:
			if isinstance(child, types):
				yield child

	def matchpath(self, path):
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


