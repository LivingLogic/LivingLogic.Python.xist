# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
This module contains XFind and CSS selectors and related classes and functions.

A selector is a XIST tree traversal filter that traverses the complete XML tree
and outputs those nodes specified by the selector. Selectors can be combined
with various operations and form a language comparable to XPath__ but
implemented as Python expressions.

__ http://www.w3.org/TR/xpath
"""


from ll import misc
from ll.xist import xsc


__docformat__ = "reStructuredText"


class Selector(xsc.WalkFilter):
	"""
	Base class for all tree traversal filters that visit the complete tree.
	Whether a node gets output can be specified by overwriting the
	:meth:`matchpath` method. Selectors can be combined with various operations
	(see methods below).
	"""

	@misc.notimplemented
	def matchpath(self, path):
		pass

	def filterpath(self, path):
		return (True, xsc.entercontent, xsc.enterattrs) if self.matchpath(path) else (xsc.entercontent, xsc.enterattrs)

	def __div__(self, other):
		"""
		Create a :class:`ChildCombinator` with :var:`self` as the left hand
		selector and :var:`other` as the right hand selector.
		"""
		return ChildCombinator(self, xsc.makewalkfilter(other))

	def __floordiv__(self, other):
		"""
		Create a :class:`DescendantCombinator` with :var:`self` as the left hand
		selector and :var:`other` as the right hand selector.
		"""
		return DescendantCombinator(self, xsc.makewalkfilter(other))

	def __mul__(self, other):
		"""
		Create an :class:`AdjacentSiblingCombinator` with :var:`self` as the left
		hand selector and :var:`other` as the right hand selector.
		"""
		return AdjacentSiblingCombinator(self, xsc.makewalkfilter(other))

	def __pow__(self, other):
		"""
		Create a :class:`GeneralSiblingCombinator` with :var:`self` as the left
		hand selector and :var:`other` as the right hand selector.
		"""
		return GeneralSiblingCombinator(self, xsc.makewalkfilter(other))

	def __and__(self, other):
		"""
		Create an :class:`AndCombinator` from :var:`self` and :var:`other`.
		"""
		return AndCombinator(self, xsc.makewalkfilter(other))

	def __or__(self, other):
		"""
		Create an :class:`OrCombinator` from :var:`self` and :var:`other`.
		"""
		return OrCombinator(self, xsc.makewalkfilter(other))

	def __invert__(self):
		"""
		Create a :class:`NotCombinator` inverting :var:`self`.
		"""
		return NotCombinator(self)


class IsInstanceSelector(Selector):
	"""
	Selector that selects all nodes that are instances of the specified type.
	You can either create an :class:`IsInstanceSelector` object directly
	or simply pass a class to a function that expects a walk filter (this class
	will be automatically wrapped in an :class:`IsInstanceSelector`)::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(html.a):
		... 	print node.attrs.href, node.attrs.title
		... 
		http://www.python.org/ 
		http://www.python.org/#left%2Dhand%2Dnavigation 
		http://www.python.org/#content%2Dbody 
		http://www.python.org/search 
		http://www.python.org/about/ About The Python Language
		http://www.python.org/news/ Major Happenings Within the Python Community
		http://www.python.org/doc/ Tutorials, Library Reference, C API
		http://www.python.org/download/ Start Running Python Under Windows, Mac, Linux and Others
		...
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
		Return an :class:`nthoftype` selector that uses :var:`index` as the
		index and ``self.types`` as the types.
		"""
		return nthoftype(index, *self.types)

	def __str__(self):
		if len(self.types) == 1:
			return "%s.%s" % (self.types[0].__module__, self.types[0].__name__)
		else:
			return "(%s)" % " | ".join("%s.%s" % (type.__module__, type.__name__) for type in self.types)


class hasname(Selector):
	"""
	Selector that selects all nodes that have a specified Python name (which
	only selects elements, processing instructions and entities). Also a namespace
	name can be specified as a second argument, which will only select elements
	from the specified namespace::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.hasname("img")):
		... 	print node.bytes()
		... 
		<img border="0" src="http://www.python.org/images/python-logo.gif" alt="homepage" id="logo" />
		<img border="0" id="skiptonav" alt="skip to navigation" src="http://www.python.org/images/trans.gif" />
		<img border="0" id="skiptocontent" alt="skip to content" src="http://www.python.org/images/trans.gif" />
		<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />
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
	:class:`hasname_xml` works similar to :class:`hasname` except that the
	specified name is treated as the XML name, not the Python name.
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
	Selector that selects one specific node in the tree. This can be combined
	with other selectors via :class:`ChildCombinator` or
	:class:`DescendantCombinator` selectors to select children of this specific
	node. You can either create an :class:`IsSelector` directly or simply pass
	a node to a function that expects a walk filter::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(doc[0]/xsc.Element):
		... 	print repr(node)
		... 
		<ll.xist.ns.html.head element object (13 children/no attrs) (from http://www.python.org/:6:?) at 0xb6c82f4c>
		<ll.xist.ns.html.body element object (19 children/no attrs) (from http://www.python.org/:26:?) at 0xb6c3154c>
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
	Selector that selects all empty elements or fragments::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.empty):
		... 	print node.bytes()
		... 
		<meta content="text/html; charset=utf-8" http-equiv="content-type" />
		<meta content="python programming language object oriented web free source" name="keywords" />
		<meta content="      Home page for Python, an interpreted, interactive, object-oriented, extensible
		      programming language. It provides an extraordinary combination of clarity and
		      versatility, and is free and comprehensively ported. " name="description" />
		<a type="application/rss+xml" href="http://www.python.org/channews.rdf" rel="alternate" title="RSS" />
		...
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
	Selector that selects all node that are the only child of their parents::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.onlychild & html.a):
		... 	print node.bytes()
		... 
		<a accesskey="2" href="http://www.python.org/#left%2dhand%2dnavigation"><img id="skiptonav" alt="skip to navigation" src="http://www.python.org/images/trans.gif" border="0" /></a>
		<a accesskey="3" href="http://www.python.org/#content%2dbody"><img id="skiptocontent" alt="skip to content" src="http://www.python.org/images/trans.gif" border="0" /></a>
		<a href="http://www.python.org/download/releases/2.5.1">Quick Links (2.5.1)</a>
		<a title="Manuals for Latest Stable Release" href="http://docs.python.org/">Documentation</a>
		...
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
	Selector that selects all nodes that are the only nodes of their type among
	their siblings::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.onlyoftype & xsc.Element):
		... 	print repr(node)
		... 
		<ll.xist.ns.html.html element object (2 children/1 attr) (from http://www.python.org/:4:?) at 0xb6d6e7ec>
		<ll.xist.ns.html.head element object (13 children/no attrs) (from http://www.python.org/:6:?) at 0xb6cc1f8c>
		<ll.xist.ns.html.title element object (1 child/no attrs) (from http://www.python.org/:8:?) at 0xb6d79b8c>
		<ll.xist.ns.html.body element object (19 children/no attrs) (from http://www.python.org/:26:?) at 0xb6d7282c>
		...
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
	Selector that selects all element nodes that have an attribute with one
	of the specified Python names. For selecting nodes with global attributes
	the attribute class can be passed::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html, xml
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.hasattr(xml.Attrs.lang)):
		... 	print repr(node)
		... 
		<ll.xist.ns.html.html element object (2 children/2 attrs) (from http://www.python.org/:4:?) at 0xb6d71d4c>
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
	:class:`hasattr_xml` works similar to :class:`hasattr` except that the
	specified names are treated as XML names instead of Python names.
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
	Selector that selects all element nodes where an attribute with the
	specified Python name has one of the specified values. For global attributes
	the attribute class can be passed. Note that "fancy" attributes (i.e. those
	containing non-text) will not be considered::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.attrhasvalue("rel", "stylesheet")):
		... 	print node.attrs.href
		... 
		http://www.python.org/styles/screen-switcher-default.css
		http://www.python.org/styles/netscape4.css
		http://www.python.org/styles/print.css
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed(self.attrname):
				attr = node.attrs.get(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return unicode(attr) in self.attrvalues
		return False

	def __str__(self):
		return "%s(%r, %s)" % (self.__class__.__name__, self.attrname, repr(self.attrvalues)[1:-1])


class attrhasvalue_xml(Selector):
	"""
	:class:`attrhasvalue_xml` works similar to :class:`attrhasvalue` except that
	the specified name is treated as an XML name instead of a Python name.
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attrname):
				attr = node.attrs.get_xml(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return unicode(attr) in self.attrvalues
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrcontains(Selector):
	"""
	Selector that selects all element nodes where an attribute with the
	specified Python name contains one of the specified substrings in its value.
	For global attributes the attribute class can be passed. Note that "fancy"
	attributes (i.e. those containing non-text) will not be considered::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.attrcontains("rel", "stylesheet")):
		... 	print node.attrs.rel, node.attrs.href
		... 

		stylesheet http://www.python.org/styles/screen-switcher-default.css
		stylesheet http://www.python.org/styles/netscape4.css
		stylesheet http://www.python.org/styles/print.css
		alternate stylesheet http://www.python.org/styles/largestyles.css
		alternate stylesheet http://www.python.org/styles/defaultfonts.css
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed(self.attrname):
				attr = node.attrs.get(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return any(attrvalue in unicode(attr) for attrvalue in self.attrvalues)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrcontains_xml(Selector):
	"""
	:class:`attrcontains_xml` works similar to :class:`attrcontains` except that
	the specified name is treated as an XML name instead of a Python name.
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attrname):
				attr = node.attrs.get_xml(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return any(attrvalue in unicode(attr) for attrvalue in self.attrvalues)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrstartswith(Selector):
	"""
	Selector that selects all element nodes where an attribute with the
	specified Python name starts with any of the specified strings. For global
	attributes the attribute class can be passed. Note that "fancy" attributes
	(i.e. those containing non-text) will not be considered::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.attrstartswith("class_", "input-")):
		... 	print repr(node)
		... 
		<input class="input-text" id="q" type="text" name="q" />
		<input value="search" class="input-button" id="submit" type="submit" name="submit" />
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed(self.attrname):
				attr = node.attrs.get(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return any(unicode(attr).startswith(attrvalue) for attrvalue in self.attrvalues)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrstartswith_xml(Selector):
	"""
	:class:`attrstartswith_xml` works similar to :class:`attrstartswith` except
	that the specified name is treated as an XML name instead of a Python name.
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attrname):
				attr = node.attrs.get_xml(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return any(unicode(attr).startswith(attrvalue) for attrvalue in self.attrvalues)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrendswith(Selector):
	"""
	Selector that selects all element nodes where an attribute with the
	specified Python name ends with one of the specified strings. For global
	attributes the attribute class can be passed. Note that "fancy" attributes
	(i.e. those containing non-text) will not be considered::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.attrendswith("href", ".css")):
		... 	print node.attrs.href
		... 
		http://www.python.org/styles/screen-switcher-default.css
		http://www.python.org/styles/netscape4.css
		http://www.python.org/styles/print.css
		http://www.python.org/styles/largestyles.css
		http://www.python.org/styles/defaultfonts.css
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed(self.attrname):
				attr = node.attrs.get(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return any(unicode(attr).endswith(attrvalue) for attrvalue in self.attrvalues)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrendswith_xml(Selector):
	"""
	:class:`attrendswith_xml` works similar to :class:`attrendswith` except that
	the specified name is treated as an XML name instead of a Python name.
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml(self.attrname):
				attr = node.attrs.get_xml(self.attrname)
				if not attr.isfancy(): # if there are PIs, say no
					return any(unicode(attr).endswith(attrvalue) for attrvalue in self.attrvalues)
		return False

	def __str__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class hasid(Selector):
	"""
	Selector that selects all element nodes where the ``id`` attribute has one
	if the specified values::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.hasid("logo")):
		... 	print node.bytes()
		... 
		<img src="http://www.python.org/images/python-logo.gif" id="logo" alt="homepage" border="0" />
	"""

	def __init__(self, *ids):
		if not ids:
			raise ValueError("need at least one id")
		self.ids = ids

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml("id"):
				attr = node.attrs.get_xml("id")
				if not attr.isfancy():
					return unicode(attr) in self.ids
		return False

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.id)


class hasclass(Selector):
	"""
	Selector that selects all element nodes where the ``class`` attribute contains
	one of the specified values::

		>>> from ll.xist import parsers, xfind
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.hasclass("reference")):
		... 	print node.bytes()
		... 
		<a class="reference" href="http://www.python.org/search">Advanced Search</a>
		<a href="http://www.python.org/about/success/rackspace" class="reference">Rackspace</a>
		<a href="http://www.python.org/about/success/ilm" class="reference">Industrial Light and Magic</a>
		<a href="http://www.python.org/about/success/astra" class="reference">AstraZeneca</a>
		...
	"""

	def __init__(self, *classnames):
		if not classnames:
			raise ValueError("need at least one classname")
		self.classnames = classnames

	def matchpath(self, path):
		if path:
			node = path[-1]
			if isinstance(node, xsc.Element) and node.Attrs.isallowed_xml("class"):
				attr = node.attrs.get_xml("class")
				if not attr.isfancy():
					return any(classname in unicode(attr).split() for classname in self.classnames)
		return False

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.classname)


class inattr(Selector):
	"""
	Selector that selects all attribute nodes and nodes inside of attributes::

	>>> from ll.xist import parsers, xfind
	>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
	>>> for node in doc.walknode(xfind.inattr & xsc.Text):
	... 	print node.bytes()
	... 
	text/html; charset=utf-8
	content-type
	python programming language object oriented web free source
	...
	"""
	def matchpath(self, path):
		return any(isinstance(node, xsc.Attr) for node in path)

	def __str__(self):
		return "inattr"


inattr = inattr()


class Combinator(Selector):
	"""
	A :class:`Combinator` is a selector that transforms one or combines two or
	more other selectors in a certain way.
	"""


class BinaryCombinator(Combinator):
	"""
	A :class:`BinaryCombinator` is a combinator that combines two selector:
	the left hand selector and the right hand selector.
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


class ChildCombinator(BinaryCombinator):
	"""
	A :class:`ChildCombinator` is a :class:`BinaryCombinator`. To match the
	:class:`ChildCombinator` the node must match the right hand selector and
	it's immediate parent must match the left hand selector (i.e. it works
	similar to the ``>`` combinator in CSS or the ``/`` combinator in XPath).

	:class:`ChildCombinator` objects can be created via the division operator
	(``/``)::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(html.a/html.img):
		... 	print node.bytes()
		... 
		<img src="http://www.python.org/images/python-logo.gif" alt="homepage" id="logo" border="0" />
		<img id="skiptonav" alt="skip to navigation" src="http://www.python.org/images/trans.gif" border="0" />
		<img id="skiptocontent" alt="skip to content" src="http://www.python.org/images/trans.gif" border="0" />
		<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />
	"""
	def matchpath(self, path):
		if path and self.right.matchpath(path):
			return self.left.matchpath(path[:-1])
		return False

	symbol = " / "


class DescendantCombinator(BinaryCombinator):
	"""
	A :class:`DescendantCombinator` is a :class:`BinaryCombinator`. To match the
	:class:`DescendantCombinator` the node must match the right hand selector
	and any of it's ancestor nodes must match the left hand selector (i.e. it
	works similar to the descendant combinator in CSS or the ``//`` combinator
	in XPath).

	:class:`DescendantCombinator` objects can be created via the floor division
	operator (``//``)::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(html.div//html.img):
		... 	print node.bytes()
		... 
		<img id="skiptonav" alt="skip to navigation" src="http://www.python.org/images/trans.gif" border="0" />
		<img id="skiptocontent" alt="skip to content" src="http://www.python.org/images/trans.gif" border="0" />
		<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />
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
	A :class:`AdjacentSiblingCombinator` is a :class:`BinaryCombinator`.
	To match the :class:`AdjacentSiblingCombinator` the node must match the
	right hand selector and the immediately preceding sibling must match the
	left hand selector.

	:class:`AdjacentSiblingCombinator` objects can be created via the
	multiplication operator (``*``). The following example outputs all links
	inside those :class:`p` elements that immediately follow a :class:`h2`
	element::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(html.h2*html.p/html.a):
		... 	print node.bytes()
		... 
		<a href="http://www.scipy.org/SciPy2007" class="reference">SciPy Conference</a>
		<a href="https://www.enthought.com/scipy07/" class="reference">early registration</a>
		<a href="http://www.europython.org/sections/registration_issues/how-to-register" class="reference">Online registration</a>
		<a href="http://europython.org/" class="reference">EuroPython 2007</a>
		<a href="http://www.osdc.com.au/papers/cfp.html" class="reference">Call For Papers</a>
		<a href="http://www.swa.hpi.uni-potsdam.de/dls07/" class="reference">DLS 2007</a>
		<a href="http://pythonpapers.cgpublisher.com/" class="reference">The Python Papers</a>
		<a href="http://www.pyconuk.org/" class="reference">PyCon UK</a>
		<a href="http://www.pyconuk.org/submit.html" class="reference">proposals for talks</a>
		<a href="http://www.pycon.it/registration/" class="reference">registration online</a>
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
	A :class:`GeneralSiblingCombinator` is a :class:`BinaryCombinator`.
	To match the :class:`GeneralSiblingCombinator` the node must match the
	right hand selector and any of the preceding siblings must match the left
	hand selector.

	:class:`AdjacentSiblingCombinator` objects can be created via the
	exponentiation operator (``**``). The following example outputs all links
	that are not the first links inside their parent (i.e. they have another
	link among their preceding siblings)::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(html.a**html.a):
		... 	print node.bytes()
		... 
		<a href="http://www.python.org/about/success/ilm" class="reference">Industrial Light and Magic</a>
		<a href="http://www.python.org/about/success/astra" class="reference">AstraZeneca</a>
		<a href="http://www.python.org/about/success/honeywell" class="reference">Honeywell</a>
		<a href="http://www.python.org/about/success" class="reference">and many others</a>
		<a href="http://www.zope.org/">Zope</a>
		...
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
	A :class:`ChainedCombinator` combines any number of other selectors.
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


class OrCombinator(ChainedCombinator):
	"""
	An :class:`OrCombinator` is a :class:`ChainedCombinator` where the node must
	match at least one of the selectors to match the :class:`OrCombinator`. An
	:class:`OrCombinator` can be created with the binary or operator (``|``)::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.hasattr("href") | xfind.hasattr("src")):
		... 	print node.attrs.href if "href" in node.Attrs else node.attrs.src
		... 
		http://www.python.org/channews.rdf
		http://aspn.activestate.com/ASPN/Cookbook/Python/index_rss
		http://python-groups.blogspot.com/feeds/posts/default
		http://www.showmedo.com/latestVideoFeed/rss2.0?tag=python
		http://www.awaretek.com/python/index.xml
		http://pyfound.blogspot.com/feeds/posts/default
		http://www.python.org/dev/peps/peps.rss
		http://www.python.org/community/jobs/jobs.rss
		http://www.reddit.com/r/Python/.rss
		http://www.python.org/styles/screen-switcher-default.css
		http://www.python.org/styles/netscape4.css
		http://www.python.org/styles/print.css
		http://www.python.org/styles/largestyles.css
		http://www.python.org/styles/defaultfonts.css
		...
	"""

	def matchpath(self, path):
		return any(selector.matchpath(path) for selector in self.selectors)

	symbol = " | "

	def __or__(self, other):
		return OrCombinator(*(self.selectors + (xsc.makewalkfilter(other),)))


class AndCombinator(ChainedCombinator):
	"""
	An :class:`AndCombinator` is a :class:`ChainedCombinator` where the node
	must match all of the combined selectors to match the :class:`AndCombinator`.
	An :class:`AndCombinator` can be created with the binary and operator
	(``&``)::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(html.input & xfind.hasattr("id")):
		... 	print node.bytes()
		... 
		<input id="domains" name="domains" value="www.python.org" type="hidden" />
		<input id="sitesearch" name="sitesearch" value="www.python.org" type="hidden" />
		<input id="sourceid" name="sourceid" value="google-search" type="hidden" />
		<input id="q" class="input-text" name="q" type="text" />
		<input id="submit" value="search" name="submit" type="submit" class="input-button" />
	"""

	def matchpath(self, path):
		return all(selector.matchpath(path) for selector in self.selectors)

	def __and__(self, other):
		return AndCombinator(*(self.selectors + (xsc.makewalkfilter(other),)))

	symbol = " & "


class NotCombinator(Combinator):
	"""
	A :class:`NotCombinator` inverts the selection logic of the underlying
	selector, i.e. a node matches only if it does not match the underlying
	selector. A :class:`NotCombinator` can be created with the unary inversion
	operator (``~``).

	The following example outputs all images that don't have a ``border``
	attribute::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(html.img & ~xfind.hasattr("border")):
		... 	print node.bytes()
		... 
		<img alt="success story photo" class="success" src="http://www.python.org/images/success/nasa.jpg" />
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
	A :class:`CallableSelector` is a selector that calls a user specified
	callable to select nodes. The callable gets passed the path and must return
	a bool specifying whether this path is selected. A :class:`CallableSelector`
	is created implicitely whenever a callable is passed to a method that
	expects a walk filter.

	The following example outputs all links that point outside the ``python.org``
	domain::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> def foreignlink(path):
		... 	return path and isinstance(path[-1], html.a) and not path[-1].attrs.href.asURL().server.endswith(".python.org")
		... 
		>>> for node in doc.walknode(foreignlink):
		... 	print node.bytes()
		... 
		<a href="http://youtube.com/" class="reference">YouTube.com</a>
		<a href="http://www.zope.org/">Zope</a>
		<a href="http://www.djangoproject.com/">Django</a>
		<a href="http://www.turbogears.org/">TurboGears</a>
		<a href="http://pyxml.sourceforge.net/topics/">XML</a>
		..
	"""

	def __init__(self, func):
		self.func = func

	def matchpath(self, path):
		return self.func(path)

	def __str__(self):
		return "%s(%r)" % (self.__class__.__name__, self.func)


class nthchild(Selector):
	"""
	An :class:`nthchild` object is a selector that selects every node that is
	the n-th child of its parent. E.g. ``nthchild(0)`` selects every first
	child, ``nthchild(-1)`` selects each last child. Furthermore
	``nthchild("even")`` selects each first, third, fifth, ... child and
	``nthchild("odd")`` selects each second, fourth, sixth, ... child.
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
	An :class:`nthoftype` object is a selector that selects every node that is
	the n-th node of a specified type among its siblings. Similar to
	:class:`nthchild` :class:`nthoftype` supports negative and positive indices
	as well as ``"even"`` and ``"odd"``. Which types are checked can be passed
	explicitly. If no types are passed the type of the node itself is used::

		>>> from ll.xist import parsers, xfind
		>>> from ll.xist.ns import html
		>>> doc = parsers.parseurl("http://www.python.org", tidy=True)
		>>> for node in doc.walknode(xfind.nthoftype(0, html.h2)):
		... 	print node.bytes()
		... 
		<h2 class="news">SciPy 2007 - Conference for Scientific Computing</h2>
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
