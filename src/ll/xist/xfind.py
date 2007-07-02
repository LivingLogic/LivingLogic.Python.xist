#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
This module contains XFind and CSS walk filters and related classes and functions.
"""

__version__ = "$Revision$".split()[1]
# $Source$


# because we want to define isinstance() as a selector
from __builtin__ import isinstance as isinstance_

try:
	import cssutils
	from cssutils.css import cssstylerule
	from cssutils.css import cssnamespacerule
except ImportError:
	pass

from ll import misc
from ll.xist import xsc


def makeselector(obj):
	if isinstance_(obj, type) and issubclass(obj, xsc.Node):
		obj = isinstance(obj)
	elif callable(obj) and not isinstance_(obj, Selector):
		obj = CallableSelector(obj)
	return obj


class Selector(xsc.FindVisitAll):
	def __div__(self, other):
		return ChildCombinator(self, makeselector(other))

	def __floordiv__(self, other):
		return DescendantCombinator(self, makeselector(other))

	def __mul__(self, other):
		return AdjacentSiblingCombinator(self, makeselector(other))

	def __pow__(self, other):
		return GeneralSiblingCombinator(self, makeselector(other))

	def __and__(self, other):
		return AndCombinator(self, makeselector(other))

	def __or__(self, other):
		return OrCombinator(self, makeselector(other))

	def __invert__(self):
		return NotCombinator(self)


class isinstance(Selector):
	def __init__(self, *types):
		self.types = types

	def match(self, path):
		if path:
			return isinstance_(path[-1], self.types)
		return False

	def __repr__(self):
		if len(self.types) == 1:
			return "%s.%s" % (self.types[0].__module__, self.types[0].__name__)
		else:
			return "%s(%s)" % (self.__class__.__name__, ", ".join("%s.%s" % (type.__module__, type.__name__) for type in self.types))


class IsSelector(Selector):
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


class isempty(Selector):
	def match(self, path):
		if path:
			node = path[-1]
			if isinstance_(node, (xsc.Element, xsc.Frag)):
				return len(node) == 0
		return False

	def __repr__(self):
		return "isempty"


isempty = isempty()


class isonlychild(Selector):
	def match(self, path):
		if len(path) < 2:
			return False
		parent = path[-2]
		if not isinstance_(parent, xsc.Element):
			return False
		return len(parent)==1 and parent[0] is path[-1]

	def __repr__(self):
		return "isonlychild"


isonlychild = isonlychild()


class isonlyoftype(Selector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		parent = path[-2]
		if not isinstance_(parent, xsc.Element):
			return False
		for child in parent.content:
			if isinstance_(child, node.__class__):
				if child is not node:
					return False
		return True

	def __repr__(self):
		return "isonlyoftype"


isonlyoftype = isonlyoftype()


class hasattr(Selector):
	def __init__(self, attrname):
		self.attrname = attrname

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed(self.attrname):
			return False
		return node.attrs.has(self.attrname)

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.attrname)


class hasattr_xml(Selector):
	def __init__(self, attrname):
		self.attrname = attrname

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attrname):
			return False
		return node.attrs.has_xml(self.attrname)

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.attrname)


class attrhasvalue(Selector):
	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed(self.attrname):
			return False
		attr = node.attrs.get(self.attrname)
		if attr.isfancy(): # if there are PIs, say no
			return False
		return unicode(attr) == self.attrvalue

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrhasvalue_xml(Selector):
	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attrname):
			return False
		attr = node.attrs.get_xml(self.attrname)
		if attr.isfancy(): # if there are PIs, say no
			return False
		return unicode(attr) == self.attrvalue

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)

	def __str__(self):
		return "[%s=%r]" % (self.attributename, self.attributevalue)


class attrcontains(Selector):
	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed(self.attrname):
			return False
		attr = node.attrs.get(self.attrname)
		if attr.isfancy(): # if there are PIs, say no
			return False
		return self.attrvalue in unicode(attr)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrcontains_xml(Selector):
	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attrname):
			return False
		attr = node.attrs.get_xml(self.attrname)
		if attr.isfancy(): # if there are PIs, say no
			return False
		return self.attrvalue in unicode(attr)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)

	def __str__(self):
		return "[%s*=%r]" % (self.attrname, self.attrvalue)


class attrstartswith(Selector):
	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed(self.attrname):
			return False
		attr = node.attrs.get(self.attrname)
		if attr.isfancy(): # if there are PIs, say no
			return False
		return unicode(attr).startswith(self.attrvalue)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrstartswith_xml(Selector):
	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attrname):
			return False
		attr = node.attrs.get_xml(self.attrname)
		if attr.isfancy(): # if there are PIs, say no
			return False
		return unicode(attr).startswith(self.attrvalue)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)

	def __str__(self):
		return "[%s^=%r]" % (self.attrname, self.attrvalue)


class attrendswith(Selector):
	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed(self.attrname):
			return False
		attr = node.attrs.get(self.attrname)
		if attr.isfancy(): # if there are PIs, say no
			return False
		return unicode(attr).endswith(self.attrvalue)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)


class attrendswith_xml(Selector):
	def __init__(self, attrname, attrvalue):
		self.attrname = attrname
		self.attrvalue = attrvalue

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attrname):
			return False
		attr = node.attrs.get_xml(self.attrname)
		if attr.isfancy(): # if there are PIs, say no
			return False
		return unicode(attr).startswith(self.attrvalue)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attrname, self.attrvalue)

	def __str__(self):
		return "[%s$=%r]" % (self.attributename, self.attributevalue)


class inattr(Selector):
	def match(self, path):
		return any(isinstance_(node, xsc.Attr) for node in path)

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
		if isinstance_(self.left, Combinator) and not isinstance_(self.left, self.__class__):
			left = "(%s)" % left
		right = repr(self.right)
		if isinstance_(self.right, Combinator) and not isinstance_(self.right, self.__class__):
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
			if isinstance_(selector, Combinator) and not isinstance_(selector, self.__class__):
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
		if isinstance_(self.selector, Combinator) and not isinstance_(self.selector, NotCombinator):
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
		if len(path) < 2:
			return False
		try:
			return path[-2][self.index] is path[-1]
		except IndexError:
			return False

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.index)


class nthoftype(Selector):
	def __init__(self, index):
		self.index = index

	def match(self, path):
		if len(path) < 2:
			return False
		try:
			return path[-2][path[-1].__class__][self.index] is path[-1]
		except IndexError:
			return False

	def __repr__(self):
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
		if not isinstance_(index, (int, long)):
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
		if not isinstance_(index, (int, long)):
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
		if isinstance_(child, xsc.Element) and child.xmlname == type:
			yield child


###
### CSS selectors
###

class CSSHasAttributeSelector(Selector):
	def __init__(self, attributename):
		self.attributename = attributename

	def match(self, path):
		node = path[-1]
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attributename):
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
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attributename):
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
		if not isinstance_(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attributename):
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


class CSSClassSelector(Selector):
	def __init__(self, classname):
		self.classname = classname

	def match(self, path):
		node = path[-1]
		return isinstance_(node, xsc.Element) and node.Attrs.isallowed("class_") and not node.attrs.class_.isfancy() and self.classname in unicode(node.attrs.class_).split()

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.classname)

	def __str__(self):
		return ".%s" % (self.classname)


class CSSIDSelector(Selector):
	def __init__(self, id):
		self.id = id

	def match(self, path):
		node = path[-1]
		return isinstance_(node, xsc.Element) and node.Attrs.isallowed("id") and not node.attrs.id.isfancy() and unicode(node.attrs.id) == self.id

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.id)

	def __str__(self):
		return "#%s" % (self.id)


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
		return isinstance_(node, xsc.Element) and _is_nth_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, 1)
	def __str__(self):

		return ":first-of-type"


class CSSLastOfTypeSelector(Selector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		return isinstance_(node, xsc.Element) and _is_nth_last_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, 1)

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
		if not isinstance_(node, xsc.Element):
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
		if not isinstance_(node, xsc.Element):
			return False
		for child in path[-1].content:
			if isinstance_(child, xsc.Element) or (isinstance_(child, xsc.Text) and child):
				return False
		return True

	def __str__(self):
		return ":empty"


class CSSRootSelector(Selector):
	def match(self, path):
		return len(path) == 1 and isinstance_(path[-1], xsc.Element)

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
		if not isinstance_(node, xsc.Element):
			return False
		return _is_nth_node(path[-2][xsc.Element], node, self.value)

	def __str__(self):
		return ":nth-child(%s)" % self.value


class CSSNthLastChildSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance_(node, xsc.Element):
			return False
		return _is_nth_last_node(path[-2][xsc.Element], node, self.value)

	def __str__(self):
		return ":nth-last-child(%s)" % self.value


class CSSNthOfTypeSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance_(node, xsc.Element):
			return False
		return _is_nth_node(self._children_of_type(path[-2], node.xmlname), node, self.value)

	def __str__(self):
		return ":nth-of-type(%s)" % self.value


class CSSNthLastOfTypeSelector(CSSFunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance_(node, xsc.Element):
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
		
	if isinstance_(selectors, basestring):
		if prefixes is not None:
			prefixes = dict((key, xsc.nsname(value)) for (key, value) in prefixes.iteritems())
			selectors = "%s\n%s{}" % ("\n".join("@namespace %s %r;" % (key if key is not None else "", value) for (key, value) in prefixes.iteritems()), selectors)
		else:
			selectors = "%s{}" % selectors
		for rule in cssutils.CSSParser().parseString(selectors).cssRules:
			if isinstance_(rule, cssstylerule.CSSStyleRule):
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
					rule.type = xmlns
				prefix = None
			elif type == "type":
				rule.type = value
			elif type == "id":
				rule.selectors.append(CSSIDSelector(value.lstrip("#")))
			elif type == "classname":
				rule.selectors.append(CSSClassSelector(value))
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
