# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This module contains XFind selectors and related classes and functions.

A selector specifies a condition that a node in an XIST tree must satisfy to
match the selector. For example the method :meth:`Node.walk` will only output
nodes that match the specified selector.

Selectors can be combined with various operations and form a language comparable
to XPath__ but implemented as Python expressions.

__ http://www.w3.org/TR/xpath
"""


import builtins
from collections import abc

from ll import misc
from ll.xist import xsc


__docformat__ = "reStructuredText"


###
### Function for filtering a :class:`xsc.Cursor` iterator against a :class:`Selector`.
###

def filter(iter, *selectors):
	"""
	Filter an iterator over :class:`xsc.Cursor` objects against a
	:class:`Selector` object.

	Example::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> [c.node.string() for c in xfind.filter(doc.walk(), html.b, html.title)]
		[
			'<title>Welcome to Python.org</title>',
			'<b>Web Programming</b>',
			'<b>GUI Development</b>',
			'<b>Scientific and Numeric</b>',
			'<b>Software Development</b>',
			'<b>System Administration</b>'
		]
	"""
	sel = selector(*selectors)
	for cursor in iter:
		if cursor.path in sel:
			yield cursor


###
### Function for creating a :class:`Selector` object.
###

def selector(*objs):
	"""
	Create a :class:`Selector` object from :obj:`objs`.

	If :obj:`objs` is empty (i.e. :func:`selector` is called without arguments)
	``any`` is returned (which matches every node).

	If more than one argument is passed (or the argument is a tuple), an
	:class:`OrCombinator` is returned.

	Otherwise the following steps are taken for the single argument ``obj``:

	*	if ``obj`` already is a :class:`Selector` object it is returned unchanged;

	*	if ``obj`` is a :class:`Node` subclass, an :class:`IsInstanceSelector`
		is returned (which matches if the node is an instance of this class);

	*	if ``obj`` is a :class:`Node` instance, an :class:`IsSelector` is returned
		(which matches only ``obj``);

	*	if ``obj`` is callable a :class:`CallableSelector` is returned
		(where matching is done by calling ``obj``);

	*	if ``obj`` is ``None`` ``any`` will be returned;

	*	otherwise :func:`selector` will raise a :exc:`TypeError`.
	"""
	if not objs:
		return any
	if len(objs) == 1:
		obj = objs[0]
		if isinstance(obj, Selector):
			return obj
		if isinstance(obj, xsc._Node_Meta):
			return IsInstanceSelector(obj)
		elif isinstance(obj, tuple):
			return selector(*obj)
		elif isinstance(obj, xsc.Node):
			return IsSelector(obj)
		elif isinstance(obj, abc.Callable):
			return CallableSelector(obj)
		elif obj is None:
			return any
		else:
			raise TypeError(f"can't convert {obj!r} to selector")
	elif all(isinstance(sel, type) for sel in objs):
		return IsInstanceSelector(*objs)
	return OrCombinator(*objs)


###
### Selectors for the :meth:`walk` method.
###

class Selector:
	"""
	A selector specifies a condition that a node in an XIST tree must satisfy
	to match the selector.

	Whether a node matches the selector can be specified by overwriting the
	:meth:`__contains__` method. Selectors can be combined with various
	operations (see methods below).
	"""

	@misc.notimplemented
	def __contains__(self, path):
		"""
		Return whether :obj:`path` (which is a list of XIST nodes from the root
		of the tree to the node in question) matches the selector.
		"""

	def __truediv__(self, other):
		"""
		Create a :class:`ChildCombinator` with :obj:`self` as the left hand
		selector and :obj:`other` as the right hand selector.
		"""
		return ChildCombinator(self, selector(other))

	def __floordiv__(self, other):
		"""
		Create a :class:`DescendantCombinator` with :obj:`self` as the left hand
		selector and :obj:`other` as the right hand selector.
		"""
		return DescendantCombinator(self, selector(other))

	def __mul__(self, other):
		"""
		Create an :class:`AdjacentSiblingCombinator` with :obj:`self` as the left
		hand selector and :obj:`other` as the right hand selector.
		"""
		return AdjacentSiblingCombinator(self, selector(other))

	def __pow__(self, other):
		"""
		Create a :class:`GeneralSiblingCombinator` with :obj:`self` as the left
		hand selector and :obj:`other` as the right hand selector.
		"""
		return GeneralSiblingCombinator(self, selector(other))

	def __and__(self, other):
		"""
		Create an :class:`AndCombinator` from :obj:`self` and :obj:`other`.
		"""
		return AndCombinator(self, selector(other))

	def __or__(self, other):
		"""
		Create an :class:`OrCombinator` from :obj:`self` and :obj:`other`.
		"""
		return OrCombinator(self, selector(other))

	def __invert__(self):
		"""
		Create a :class:`NotCombinator` inverting :obj:`self`.
		"""
		return NotCombinator(self)



class AnySelector(Selector):
	"""
	Selector that selects all nodes.

	An instance of this class named ``any`` is created as a module global, i.e.
	you can use ``xfind.any``.
	"""

	def __contains__(self, path):
		return True

	def __and__(self, other):
		return selector(other)

	def __or__(self, other):
		return self


any = AnySelector()


class IsInstanceSelector(Selector):
	"""
	Selector that selects all nodes that are instances of the specified type.
	You can either create an :class:`IsInstanceSelector` object directly
	or simply pass a class to a function that expects a selector (this class
	will be automatically wrapped in an :class:`IsInstanceSelector`)::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(html.a):
		... 	print(node.attrs.href, node.attrs.title)
		...
		https://www.python.org/#content Skip to content
		https://www.python.org/#python-network
		https://www.python.org/ The Python Programming Language
		https://www.python.org/psf-landing/ The Python Software Foundation
		...
	"""
	def __init__(self, *types):
		self.types = types

	def __contains__(self, path):
		return isinstance(path[-1], self.types)

	def __or__(self, other):
		# If ``other`` is a type check too, combine ``self`` and ``other`` into one :class:`IsInstanceSelector` object
		if isinstance(other, xsc._Node_Meta):
			return IsInstanceSelector(*(self.types + (other,)))
		elif isinstance(other, IsInstanceSelector):
			return IsInstanceSelector(*(self.types+other.types))
		return Selector.__or__(self, other)

	def __getitem__(self, index):
		"""
		Return an :class:`nthoftype` selector that uses :obj:`index` as the
		index and ``self.types`` as the types.
		"""
		return nthoftype(index, *self.types)

	def __str__(self):
		if len(self.types) == 1:
			return f"{self.types[0].__module__}.{self.types[0].__name__}"
		else:
			types = " | ".join(f"{type.__module__}.{type.__name__}" for type in self.types)
			return f"({types})"


class element(Selector):
	"""
	Selector that selects all elements that have a specified namespace name and
	element name::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.element(html, "img")):
		... 	print(node.string())
		...
		<img alt="python™" class="python-logo" src="https://www.python.org/static/img/python-logo.png" />
	"""
	def __init__(self, xmlns, xmlname):
		self.xmlns = xsc.nsname(xmlns)
		self.xmlname = xmlname

	def __contains__(self, path):
		node = path[-1]
		return isinstance(node, xsc.Element) and node.xmlns == self.xmlns and node.xmlname == self.xmlname

	def __str__(self):
		return f"{self.__class__.__qualname__}({self.name!r}, {self.xmlns!r})"


class procinst(Selector):
	"""
	Selector that selects all processing instructions that have a specified name.
	"""
	def __init__(self, xmlname):
		self.xmlname = xmlname

	def __contains__(self, path):
		node = path[-1]
		return isinstance(node, xsc.ProcInst) and node.xmlname == self.xmlname

	def __str__(self):
		return f"{self.__class__.__qualname__}({self.name!r})"


class entity(Selector):
	"""
	Selector that selects all entities that have a specified name.
	"""
	def __init__(self, xmlname):
		self.xmlname = xmlname

	def __contains__(self, path):
		node = path[-1]
		return isinstance(node, xsc.Entity) and node.xmlname == self.xmlname

	def __str__(self):
		return f"{self.__class__.__qualname__}({self.name!r})"


class IsSelector(Selector):
	"""
	Selector that selects one specific node in the tree. This can be combined
	with other selectors via :class:`ChildCombinator` or
	:class:`DescendantCombinator` selectors to select children of this specific
	node. You can either create an :class:`IsSelector` directly or simply pass
	a node to a function that expects a selector::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(doc[0]/xsc.Element):
		... 	print(repr(node))
		...
		<element ll.xist.ns.html.head xmlns='http://www.w3.org/1999/xhtml' (89 children/no attrs) location='https://www.python.org/:?:?' at 0x104ad7630>
		<element ll.xist.ns.html.body xmlns='http://www.w3.org/1999/xhtml' (14 children/2 attrs) location='https://www.python.org/:?:?' at 0x104cc1f28>
	"""
	def __init__(self, node):
		self.node = node

	def __contains__(self, path):
		return path[-1] is self.node

	def __str__(self):
		return f"{self.__class__.__qualname__}({self.node!r})"


class IsRootSelector(Selector):
	"""
	Selector that selects the node that is the root of the traversal.

	An instance of this class named ``isroot`` is created as a module global,
	i.e. you can use ``xfind.isroot``.
	"""
	def __contains__(self, path):
		return len(path) == 1


isroot = IsRootSelector()


class IsEmptySelector(Selector):
	"""
	Selector that selects all empty elements or fragments.

	An instance of this class named ``empty`` is created as a module global,
	i.e. you can use ``xfind.empty``::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.empty):
		... 	print(node.string())
		...
		<meta charset="utf-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<link href="https://ajax.googleapis.com/" rel="prefetch" />
		<meta name="application-name" content="Python.org" />
		...
	"""

	def __contains__(self, path):
		node = path[-1]
		if isinstance(node, (xsc.Element, xsc.Frag)):
			return len(node) == 0
		return False


empty = IsEmptySelector()


class OnlyChildSelector(Selector):
	"""
	Selector that selects all nodes that are the only child of their parents.

	An instance of this class named ``onlychild`` is created as a module global,
	i.e. you can use ``xfind.onlychild``::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.onlychild & html.a):
		... 	print(node.string())
		...
		<a class="text-shrink" href="javascript:;" title="Make Text Smaller">Smaller</a>
		<a class="text-grow" href="javascript:;" title="Make Text Larger">Larger</a>
		<a class="text-reset" href="javascript:;" title="Reset any font size changes I have made">Reset</a>
		<a href="http://plus.google.com/+Python"><span aria-hidden="true" class="icon-google-plus"></span>Google+</a>
		...
	"""

	def __contains__(self, path):
		if len(path) >= 2:
			parent = path[-2]
			if isinstance(parent, (xsc.Frag, xsc.Element)):
				return len(parent) == 1 and parent[0] is path[-1]
		return False

	def __str__(self):
		return "onlychild"


onlychild = OnlyChildSelector()


class OnlyOfTypeSelector(Selector):
	"""
	Selector that selects all nodes that are the only nodes of their type among
	their siblings.

	An instance of this class named ``onlyoftype`` is created as a module global,
	i.e. you can use ``xfind.onlyoftype``::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.onlyoftype & xsc.Element):
		... 	print(repr(node))
		...
		<element ll.xist.ns.html.html xmlns='http://www.w3.org/1999/xhtml' (7 children/3 attrs) location='https://www.python.org/:?:?' at 0x108858d30>
		<element ll.xist.ns.html.head xmlns='http://www.w3.org/1999/xhtml' (89 children/no attrs) location='https://www.python.org/:?:?' at 0x108858630>
		<element ll.xist.ns.html.title xmlns='http://www.w3.org/1999/xhtml' (1 child/no attrs) location='https://www.python.org/:?:?' at 0x108c547b8>
		<element ll.xist.ns.html.body xmlns='http://www.w3.org/1999/xhtml' (14 children/2 attrs) location='https://www.python.org/:?:?' at 0x108c54eb8>
		...
	"""

	def __contains__(self, path):
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


onlyoftype = OnlyOfTypeSelector()


class hasattr(Selector):
	"""
	Selector that selects all element nodes that have an attribute with one of
	the specified names. (Names can be strings, (attribute name, namespace name)
	tuples or attribute classes or instances)::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.hasattr("id")):
		... 	print(node.xmlname, node.attrs.id)
		...
		body homepage
		div touchnav-wrapper
		div top
		a close-python-network
		...
	"""

	def __init__(self, *attrnames):
		self.attrnames = attrnames

	def __contains__(self, path):
		node = path[-1]
		if isinstance(node, xsc.Element):
			for attrname in self.attrnames:
				if attrname in node.attrs:
					return True
		return False

	def __str__(self):
		attrnames = ", ".join(repr(attrname) for attrname in self.attrnames)
		return f"{self.__class__.__qualname__}({attrname})"


class attrhasvalue(Selector):
	"""
	Selector that selects all element nodes where an attribute with the specified
	name has one of the specified values. (Names can be strings,
	(attribute name, namespace name) tuples or attribute classes or instances).
	Note that "fancy" attributes (i.e. those containing non-text) will not be
	considered::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.attrhasvalue("rel", "stylesheet")):
		... 	print(node.attrs.href)
		...
		https://www.python.org/static/stylesheets/style.css
		https://www.python.org/static/stylesheets/mq.css
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def __contains__(self, path):
		node = path[-1]
		if isinstance(node, xsc.Element):
			attr = node.attrs.get(self.attrname)
			if not attr.isfancy(): # if there are PIs, say no
				return str(attr) in self.attrvalues
		return False

	def __str__(self):
		attrvalues = repr(self.attrvalues)[1:-1]
		return f"{self.__class__.__qualname__}({self.attrname!r}, {attrvalues})"


class attrcontains(Selector):
	"""
	Selector that selects all element nodes where an attribute with the specified
	name contains one of the specified substrings in its value. (Names can be
	strings, (attribute name, namespace name) tuples or attribute classes or
	instances). Note that "fancy" attributes (i.e. those containing non-text)
	will not be considered::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.attrcontains("rel", "stylesheet")):
		... 	print(node.attrs.rel, node.attrs.href)
		...
		stylesheet https://www.python.org/static/stylesheets/style.css
		stylesheet https://www.python.org/static/stylesheets/mq.css
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def __contains__(self, path):
		node = path[-1]
		if isinstance(node, xsc.Element):
			attr = node.attrs.get(self.attrname)
			if not attr.isfancy(): # if there are PIs, say no
				return builtins.any(attrvalue in str(attr) for attrvalue in self.attrvalues)
		return False

	def __str__(self):
		attrvalues = repr(self.attrvalues)[1:-1]
		return f"{self.__class__.__qualname__}({self.attrname!r}, {attrvalues})"


class attrstartswith(Selector):
	"""
	Selector that selects all element nodes where an attribute with the specified
	name starts with any of the specified strings. (Names can be strings,
	(attribute name, namespace name) tuples or attribute classes or instances).
	Note that "fancy" attributes (i.e. those containing non-text) will not be
	considered::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.attrstartswith("class", "icon-")):
		... 	print(node.string())
		...
		<span aria-hidden="true" class="icon-arrow-down"><span>▼</span></span>
		<span aria-hidden="true" class="icon-arrow-up"><span>▲</span></span>
		<span aria-hidden="true" class="icon-search"></span>
		<span aria-hidden="true" class="icon-google-plus"></span>
		...
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def __contains__(self, path):
		node = path[-1]
		if isinstance(node, xsc.Element):
			attr = node.attrs.get(self.attrname)
			if not attr.isfancy(): # if there are PIs, say no
				return builtins.any(str(attr).startswith(attrvalue) for attrvalue in self.attrvalues)
		return False

	def __str__(self):
		attrvalues = repr(self.attrvalues)[1:-1]
		return f"{self.__class__.__qualname__}({self.attrname!r}, {attrvalues})"


class attrendswith(Selector):
	"""
	Selector that selects all element nodes where an attribute with the specified
	name ends with one of the specified strings. (Names can be strings,
	(attribute name, namespace name) tuples or attribute classes or instances).
	Note that "fancy" attributes (i.e. those containing non-text) will not be
	considered::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.attrendswith("href", ".css")):
		... 	print(node.attrs.href)
		...
		https://www.python.org/static/stylesheets/style.css
		https://www.python.org/static/stylesheets/mq.css
	"""

	def __init__(self, attrname, *attrvalues):
		self.attrname = attrname
		if not attrvalues:
			raise ValueError("need at least one attribute value")
		self.attrvalues = attrvalues

	def __contains__(self, path):
		node = path[-1]
		if isinstance(node, xsc.Element):
			attr = node.attrs.get(self.attrname)
			if not attr.isfancy(): # if there are PIs, say no
				return builtins.any(str(attr).endswith(attrvalue) for attrvalue in self.attrvalues)
		return False

	def __str__(self):
		attrvalues = repr(self.attrvalues)[1:-1]
		return f"{self.__class__.__qualname__}({self.attrname!r}, {attrvalues})"


class hasid(Selector):
	"""
	Selector that selects all element nodes where the ``id`` attribute has one
	if the specified values::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.hasid("id-search-field")):
		... 	print(node.string())
		...
		<input class="search-field" id="id-search-field" name="q" placeholder="Search" role="textbox" tabindex="1" type="search" />
	"""

	def __init__(self, *ids):
		if not ids:
			raise ValueError("need at least one id")
		self.ids = ids

	def __contains__(self, path):
		node = path[-1]
		if isinstance(node, xsc.Element):
			attr = node.attrs.get("id")
			if not attr.isfancy():
				return str(attr) in self.ids
		return False

	def __str__(self):
		ids = repr(self.ids)[1:-1]
		return f"{self.__class__.__qualname__}({ids})"


class hasclass(Selector):
	"""
	Selector that selects all element nodes where the ``class`` attribute contains
	one of the specified values::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.hasclass("tier-1")/html.a):
		... 	print(node.string())
		...
		A A
		Socialize
		Sign In
		About
		Downloads
		...
	"""

	def __init__(self, *classnames):
		if not classnames:
			raise ValueError("need at least one classname")
		self.classnames = classnames

	def __contains__(self, path):
		node = path[-1]
		if isinstance(node, xsc.Element):
			attr = node.attrs.get("class")
			if not attr.isfancy():
				return builtins.any(classname in str(attr).split() for classname in self.classnames)
		return False

	def __str__(self):
		classnames = repr(self.classnames)[1:-1]
		return f"{self.__class__.__qualname__}({classnames})"


class InAttrSelector(Selector):
	"""
	Selector that selects all attribute nodes and nodes inside of attributes::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for path in doc.walkpaths(xfind.inattr & xsc.Text, enterattrs=True, enterattr=True):
		... 	print(path[-3].xmlname, path[-2].xmlname, path[-1].string())
		...
		html class no-js
		html dir ltr
		html lang en
		meta charset utf-8
		meta content IE=edge
		meta http-equiv X-UA-Compatible
		...
	"""
	def __contains__(self, path):
		return builtins.any(isinstance(node, xsc.Attr) for node in path)

	def __str__(self):
		return "inattr"


inattr = InAttrSelector()


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
			left = f"({left})"
		right = str(self.right)
		if isinstance(self.right, Combinator) and not isinstance(self.right, self.__class__):
			right = f"({right})"
		return f"{left}{self.symbol}{right}"


class ChildCombinator(BinaryCombinator):
	"""
	A :class:`ChildCombinator` is a :class:`BinaryCombinator`. To match the
	:class:`ChildCombinator` the node must match the right hand selector and
	its immediate parent must match the left hand selector (i.e. it works
	similar to the ``>`` combinator in CSS or the ``/`` combinator in XPath).

	:class:`ChildCombinator` objects can be created via the division operator
	(``/``)::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(html.a/html.img):
		... 	print(node.string())
		...
		<img alt="python™" class="python-logo" src="https://www.python.org/static/img/python-logo.png" />
	"""
	def __contains__(self, path):
		if len(path) > 1 and path in self.right:
			return path[:-1] in self.left
		return False

	symbol = " / "


class DescendantCombinator(BinaryCombinator):
	"""
	A :class:`DescendantCombinator` is a :class:`BinaryCombinator`. To match the
	:class:`DescendantCombinator` the node must match the right hand selector
	and any of its ancestor nodes must match the left hand selector (i.e. it
	works similar to the descendant combinator in CSS or the ``//`` combinator
	in XPath).

	:class:`DescendantCombinator` objects can be created via the floor division
	operator (``//``)::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(html.div//html.img):
		... 	print(node.string())
		...
		<img alt="python™" class="python-logo" src="https://www.python.org/static/img/python-logo.png" />
	"""
	def __contains__(self, path):
		if path in self.right:
			while len(path) > 1:
				path = path[:-1]
				if path in self.left:
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
	multiplication operator (``*``). The following example outputs all
	:class:`span` elements that immediately follow a :class:`form` element::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(html.form*html.span):
		... 	print(node.string())
		...
		<span class="breaker"></span>
	"""

	def __contains__(self, path):
		if len(path) > 1 and path in self.right:
			# Find sibling
			node = path[-1]
			sibling = None
			for child in path[-2]:
				if child is node:
					break
				sibling = child
			if sibling is not None:
				return path[:-1]+[sibling] in self.left
		return False

	symbol = " * "


class GeneralSiblingCombinator(BinaryCombinator):
	"""
	A :class:`GeneralSiblingCombinator` is a :class:`BinaryCombinator`.
	To match the :class:`GeneralSiblingCombinator` the node must match the
	right hand selector and any of the preceding siblings must match the left
	hand selector.

	:class:`AdjacentSiblingCombinator` objects can be created via the
	exponentiation operator (``**``). The following example outputs all
	:class:`meta` element that come after the :class:`link` elements::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(html.link**html.meta):
		... 	print(node.string())
		...
		<meta name="application-name" content="Python.org" />
		<meta name="msapplication-tooltip" content="The official home of the Python Programming Language" />
		<meta name="apple-mobile-web-app-title" content="Python.org" />
		<meta name="apple-mobile-web-app-capable" content="yes" />
		<meta name="apple-mobile-web-app-status-bar-style" content="black" />
		...
	"""

	def __contains__(self, path):
		if len(path) > 1 and path in self.right:
			node = path[-1]
			for child in path[-2]:
				if child is node: # no previous siblings
					return False
				if path[:-1]+[child] in self.left:
					return True
		return False

	symbol = " ** "


class ChainedCombinator(Combinator):
	"""
	A :class:`ChainedCombinator` combines any number of other selectors.
	"""

	symbol = None

	def __init__(self, *selectors):
		self.selectors = tuple(selector(sel) for sel in selectors)

	def __str__(self):
		v = []
		for sel in self.selectors:
			if isinstance(sel, Combinator) and not isinstance(sel, self.__class__):
				s = f"({sel})"
			else:
				s = str(sel)
			v.append(s)
		return self.symbol.join(v)


class OrCombinator(ChainedCombinator):
	"""
	An :class:`OrCombinator` is a :class:`ChainedCombinator` where the node must
	match at least one of the selectors to match the :class:`OrCombinator`. An
	:class:`OrCombinator` can be created with the binary or operator (``|``)::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.hasattr("href") | xfind.hasattr("src")):
		... 	print(node.attrs.href if "href" in node.Attrs else node.attrs.src)
		...
		https://ajax.googleapis.com/
		https://www.python.org/static/js/libs/modernizr.js
		https://www.python.org/static/stylesheets/style.css
		https://www.python.org/static/stylesheets/mq.css
		https://www.python.org/static/favicon.ico
		...
	"""

	def __contains__(self, path):
		return builtins.any(path in sel for sel in self.selectors)

	symbol = " | "

	def __or__(self, other):
		return OrCombinator(*(self.selectors + (selector(other),)))


class AndCombinator(ChainedCombinator):
	"""
	An :class:`AndCombinator` is a :class:`ChainedCombinator` where the node
	must match all of the combined selectors to match the :class:`AndCombinator`.
	An :class:`AndCombinator` can be created with the binary and operator
	(``&``)::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(html.input & xfind.hasattr("id")):
		... 	print(node.string())
		...
		<input class="search-field" id="id-search-field" name="q" placeholder="Search" role="textbox" tabindex="1" type="search" />
	"""

	def __contains__(self, path):
		return all(path in sel for sel in self.selectors)

	def __and__(self, other):
		return AndCombinator(*(self.selectors + (selector(other),)))

	symbol = " & "


class NotCombinator(Combinator):
	"""
	A :class:`NotCombinator` inverts the selection logic of the underlying
	selector, i.e. a node matches only if it does not match the underlying
	selector. A :class:`NotCombinator` can be created with the unary inversion
	operator (``~``).

	The following example outputs all internal scripts::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(html.script & ~xfind.hasattr("src")):
		... 	print(node.string())
		...
		<script type="text/javascript">
		    var _gaq = _gaq || [];
		    _gaq.push(['_setAccount', 'UA-39055973-1']);
		    _gaq.push(['_trackPageview']);
		
		    (function() {
		        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
		        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
		        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
		    })();
		    </script>
		<script>window.jQuery || document.write('&lt;script src="/static/js/libs/jquery-1.8.2.min.js"&gt;&lt;\\/script&gt;')</script>
	"""

	def __init__(self, selector):
		self.selector = selector

	def __contains__(self, path):
		return path not in self.selector

	def __str__(self):
		if isinstance(self.selector, Combinator) and not isinstance(self.selector, NotCombinator):
			return f"~({self.selector})"
		else:
			return f"~{self.selector}"


class CallableSelector(Selector):
	"""
	A :class:`CallableSelector` is a selector that calls a user specified
	callable to select nodes. The callable gets passed the path and must return
	a bool specifying whether this path is selected. A :class:`CallableSelector`
	is created implicitely whenever a callable is passed to a method that
	expects a selector.

	The following example outputs all links that point outside the ``python.org``
	domain::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> def isextlink(path):
		... 	return isinstance(path[-1], html.a) and not str(path[-1].attrs.href).startswith("https://www.python.org")
		...
		>>> for node in doc.walknodes(isextlink):
		... 	print(node.string())
		...
		<a href="http://docs.python.org/" title="Python Documentation">Docs</a>
		<a href="https://pypi.python.org/" title="Python Package Index">PyPI</a>
		<a class="text-shrink" href="javascript:;" title="Make Text Smaller">Smaller</a>
		<a class="text-grow" href="javascript:;" title="Make Text Larger">Larger</a>
		..
	"""

	def __init__(self, func):
		self.func = func

	def __contains__(self, path):
		return self.func(path)

	def __str__(self):
		return f"{self.__class__.__qualname__}({self.func!r})"


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

	def __contains__(self, path):
		if len(path) > 1:
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
		return f"{self.__class__.__qualname__}({self.index!r})"


class nthoftype(Selector):
	"""
	An :class:`nthoftype` object is a selector that selects every node that is
	the n-th node of a specified type among its siblings. Similar to
	:class:`nthchild` :class:`nthoftype` supports negative and positive indices
	as well as ``"even"`` and ``"odd"``. Which types are checked can be passed
	explicitly. If no types are passed the type of the node itself is used::

		>>> from ll.xist import xsc, parse, xfind
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("https://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> for node in doc.walknodes(xfind.nthoftype(0, html.h2)):
		... 	print(node.string())
		...
		<h2 class="widget-title"><span aria-hidden="true" class="icon-get-started"></span>Get Started</h2>
		<h2 class="widget-title"><span aria-hidden="true" class="icon-download"></span>Download</h2>
		<h2 class="widget-title"><span aria-hidden="true" class="icon-documentation"></span>Docs</h2>
		<h2 class="widget-title"><span aria-hidden="true" class="icon-jobs"></span>Jobs</h2>
		...
	"""

	def __init__(self, index, *types):
		self.index = index
		self.types = types

	def _find(self, path):
		types = self.types if self.types else path[-1].__class__
		for child in path[-2]:
			if isinstance(child, types):
				yield child

	def __contains__(self, path):
		if len(path) > 1:
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
			types = ", ".join(f"{type.__module__}.{type.__qualname__}" for type in self.types)
			return f"{self.__class__.__qualname__}({self.index!r}, {types})"
		else:
			return f"{self.__class__.__qualname__}({self.index!r})"
