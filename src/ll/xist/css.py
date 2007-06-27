#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
"""


__version__ = "$Revision$".split()[1]
# $Source$


import cssutils
from cssutils.css import cssstylerule
from cssutils.css import cssnamespacerule

from ll import misc
from ll.xist import xsc


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


class Selector(xsc.FindVisitAll):
	def __div__(self, other):
		if isinstance(other, type) and issubclass(other, xsc.Node):
			other = IsSelector(other)
		return ChildCombinator(self, other)

	def __floordiv__(self, other):
		if isinstance(other, type) and issubclass(other, xsc.Node):
			other = IsSelector(other)
		return DescendantCombinator(self, other)

	def __mul__(self, other):
		if isinstance(other, type) and issubclass(other, xsc.Node):
			other = IsSelector(other)
		return AdjacentSiblingCombinator(self, other)

	def __pow__(self, other):
		if isinstance(other, type) and issubclass(other, xsc.Node):
			other = IsSelector(other)
		return GeneralSiblingCombinator(self, other)


class HasAttributeSelector(Selector):
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


class CSSAttributeIsSelector(Selector):
	def __init__(self, attributename, attributevalue):
		self.attributename = attributename
		self.attributevalue = attributevalue

	def match(self, path):
		node = path[-1]
		if not isinstance(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attributename):
			return False
		attr = node.attrs.get_xml(self.attributename)
		if attr.isfancy(): # if there are PIs, say no
			return False
		return unicode(attr) == self.attributevalue

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attributename, self.attributevalue)

	def __str__(self):
		return "[%s=%r]" % (self.attributename, self.attributevalue)


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


class CSSAttributeStartsWithSelector(Selector):
	def __init__(self, attributename, attributevalue):
		self.attributename = attributename
		self.attributevalue = attributevalue

	def match(self, path):
		node = path[-1]
		if not isinstance(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attributename):
			return False
		attr = node.attrs.get_xml(self.attributename)
		return unicode(attr).startswith(self.attributevalue)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attributename, self.attributevalue)

	def __str__(self):
		return "[%s^=%r]" % (self.attributename, self.attributevalue)


class CSSAttributeEndsWithSelector(Selector):
	def __init__(self, attributename, attributevalue):
		self.attributename = attributename
		self.attributevalue = attributevalue

	def match(self, path):
		node = path[-1]
		if not isinstance(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attributename):
			return False
		attr = node.attrs.get_xml(self.attributename)
		return unicode(attr).endswith(self.attributevalue)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attributename, self.attributevalue)

	def __str__(self):
		return "[%s$=%r]" % (self.attributename, self.attributevalue)


class CSSAttributeContainsSelector(Selector):
	def __init__(self, attributename, attributevalue):
		self.attributename = attributename
		self.attributevalue = attributevalue

	def match(self, path):
		node = path[-1]
		if not isinstance(node, xsc.Element) or not node.Attrs.isallowed_xml(self.attributename):
			return False
		attr = node.attrs.get_xml(self.attributename)
		return self.attributevalue in unicode(attr)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.attributename, self.attributevalue)

	def __str__(self):
		return "[%s*=%r]" % (self.attributename, self.attributevalue)


class CSSClassSelector(Selector):
	def __init__(self, classname):
		self.classname = classname

	def match(self, path):
		node = path[-1]
		return isinstance(node, xsc.Element) and node.Attrs.isallowed("class_") and not node.attrs.class_.isfancy() and self.classname in unicode(node.attrs.class_).split()

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.classname)

	def __str__(self):
		return ".%s" % (self.classname)


class CSSIDSelector(Selector):
	def __init__(self, id):
		self.id = id

	def match(self, path):
		node = path[-1]
		return isinstance(node, xsc.Element) and node.Attrs.isallowed("id") and not node.attrs.id.isfancy() and unicode(node.attrs.id) == self.id

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.id)

	def __str__(self):
		return "#%s" % (self.id)


class FirstChildSelector(Selector):
	def match(self, path):
		return len(path) >= 2 and _is_nth_node(path[-2][xsc.Element], path[-1], 1)

	def __str__(self):
		return ":first-child"


class LastChildSelector(Selector):
	def match(self, path):
		return len(path) >= 2 and _is_nth_last_node(path[-2][xsc.Element], path[-1], 1)

	def __str__(self):
		return ":last-child"


class FirstOfTypeSelector(Selector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		return isinstance(node, xsc.Element) and _is_nth_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, 1)

	def __str__(self):
		return ":first-of-type"


class LastOfTypeSelector(Selector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		return isinstance(node, xsc.Element) and _is_nth_last_node(misc.Iterator(_children_of_type(path[-2], node.xmlname)), node, 1)

	def __str__(self):
		return ":last-of-type"


class OnlyChildSelector(Selector):
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


class OnlyOfTypeSelector(Selector):
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


class EmptySelector(Selector):
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


class RootSelector(Selector):
	def match(self, path):
		return len(path) == 1 and isinstance(path[-1], xsc.Element)

	def __str__(self):
		return ":root"


class FunctionSelector(Selector):
	def __init__(self, value=None):
		self.value = value


class NthChildSelector(FunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance(node, xsc.Element):
			return False
		return _is_nth_node(path[-2][xsc.Element], node, self.value)

	def __str__(self):
		return ":nth-child(%s)" % self.value


class NthLastChildSelector(FunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance(node, xsc.Element):
			return False
		return _is_nth_last_node(path[-2][xsc.Element], node, self.value)

	def __str__(self):
		return ":nth-last-child(%s)" % self.value


class NthOfTypeSelector(FunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance(node, xsc.Element):
			return False
		return _is_nth_node(self._children_of_type(path[-2], node.xmlname), node, self.value)

	def __str__(self):
		return ":nth-of-type(%s)" % self.value


class NthLastOfTypeSelector(FunctionSelector):
	def match(self, path):
		if len(path) < 2:
			return False
		node = path[-1]
		if not isinstance(node, xsc.Element):
			return False
		return _is_nth_last_node(self._children_of_type(path[-2], node.xmlname), node, self.value)

	def __str__(self):
		return ":nth-last-of-type(%s)" % self.value


class Combinator(Selector):
	def __init__(self, left, right):
		self.left = left
		self.right = right


class ChildCombinator(Combinator):
	def match(self, path):
		if path and self.right.match(path):
			return self.left.match(path[:-1])
		return False

	def __repr__(self):
		return "%r/%r" % (self.left, self.right)

	def __str__(self):
		return "%s>%s" % (self.left, self.right)


class DescendantCombinator(Combinator):
	def match(self, path):
		if path and self.right.match(path):
			while path:
				path = path[:-1]
				if self.left.match(path):
					return True
		return False

	def __repr__(self):
		return "%r//%r" % (self.left, self.right)

	def __str__(self):
		return "%s %s" % (self.left, self.right)


class AdjacentSiblingCombinator(Combinator):
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

	def __repr__(self):
		return "%r*%r" % (self.left, self.right)

	def __str__(self):
		return "%s+%s" % (self.left, self.right)


class GeneralSiblingCombinator(Combinator):
	def match(self, path):
		if len(path) >= 2 and self.right.match(path):
			node = path[-1]
			for child in path[-2][xsc.Element]:
				if child is node:
					return False
				if self.left.match(path[:-1]+[child]):
					return True
		return False

	def __repr__(self):
		return "%r**%r" % (self.left, self.right)

	def __str__(self):
		return "%s~%s" % (self.left, self.right)


class OrCombinator(Selector):
	def __init__(self, *selectors):
		self.selectors = selectors

	def match(self, path):
		return any(selector.match(path) for selector in self.selectors)

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join(repr(selector) for selector in self.selectors))

	def __str__(self):
		return ", ".join(str(selector) for selector in self.selectors)


class AndCombinator(Selector):
	def __init__(self, *selectors):
		self.selectors = selectors

	def match(self, path):
		return all(selector.match(path) for selector in self.selectors)

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join(repr(selector) for selector in self.selectors))

	def __str__(self):
		return " and ".join(str(selector) for selector in self.selectors)


class IsSelector(Selector):
	def __init__(self, *types):
		self.types = types

	def match(self, path):
		if path:
			return isinstance(path[-1], self.types)
		return False

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join("%s.%s" % (type.__module__, type.__name__) for type in self.types))


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
	"=": CSSAttributeIsSelector,
	"~=": CSSAttributeListSelector,
	"|=": CSSAttributeLangSelector,
	"$=": CSSAttributeStartsWithSelector,
	"$=": CSSAttributeEndsWithSelector,
	"*=": CSSAttributeContainsSelector,
}

_combinator2class = {
	" ": DescendantCombinator,
	">": ChildCombinator,
	"+": AdjacentSiblingCombinator,
	"~": GeneralSiblingCombinator,
}

_pseudoname2class = {
	"first-child": FirstChildSelector,
	"last-child": LastChildSelector,
	"first-of-type": FirstOfTypeSelector,
	"last-of-type": LastOfTypeSelector,
	"only-child": OnlyChildSelector,
	"only-of-type": OnlyOfTypeSelector,
	"empty": EmptySelector,
	"root": RootSelector,
}

_function2class = {
	"nth-child": NthChildSelector,
	"nth-last-child": NthLastChildSelector,
	"nth-of-type": NthOfTypeSelector,
	"nth-last-of-type": NthLastOfTypeSelector,
}


def findcss(selectors, prefixes=None):
	"""
	Create a new <class>FindCSS<class>. <arg>selectors</arg> can be a string
	or a <class>cssutils.css.selector.Selector</class> object. <arg>prefixes</arg>
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
					rule.selectors.append(HasAttributeSelector(attributename))
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
