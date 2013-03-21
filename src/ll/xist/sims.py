# -*- coding: utf-8 -*-

## Copyright 1999-2013 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2013 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This module contains classes for a very simple validation model.

Validation is specified like this::

	class inner(xsc.Element):
		model = sims.NoElements()

	class outer(xsc.Element):
		model = sims.Elements(inner)

With this configuration :class:`inner` elements may only contain text and
:class:`outer` elements may only contain :class:`inner` elements. Everything
else will issue warnings when parsing or publishing.
"""


import warnings
from ll.xist import xsc


__docformat__ = "reStructuredText"


class SIMSWarning(xsc.Warning):
	"""
	Base class for all warning classes in this module.
	"""


class EmptyElementWithContentWarning(SIMSWarning):
	"""
	Warning that is issued when an element has content, but it shouldn't
	(i.e. :attr:`model` is :class:`Empty`)
	"""

	def __init__(self, path):
		self.path = path[:]

	def __str__(self):
		return "{} doesn't allow content".format(self.path[-1]._str())


class WrongElementWarning(SIMSWarning):
	"""
	Warning that is issued when an element contains another element of a
	certain type, but shouldn't.
	"""

	def __init__(self, model, path, badnode):
		self.model = model
		self.path = path
		self.badnode = badnode

	def __str__(self):
		return "{} may not contain {}".format(self.path[-1]._str(), self.badnode._str())


class ElementWarning(SIMSWarning):
	"""
	Warning that is issued when an element contains another element but
	shouldn't contain any.
	"""

	def __init__(self, node, badnode):
		self.node = node
		self.badnode = badnode

	def __str__(self):
		return "{} may not contain other elements".format(self.node._str())


class IllegalTextWarning(SIMSWarning):
	"""
	Warning that is issued when an element contains a text node but shouldn't.
	"""

	def __init__(self, node, badnode):
		self.node = node
		self.badnode = badnode

	def __str__(self):
		return "{} may not contain text".format(self.node._str())


def badtext(node):
	"""
	Return whether :var:`node` is a text node (i.e. :class:`ll.xist.xsc.Text`
	that does not consist of whitespace only).
	"""
	if isinstance(node, xsc.Text):
		if node and not node.isspace():
			return True
	return False


class Empty(object):
	"""
	This validator checks that an element has no content.
	"""
	empty = True

	def __repr__(self):
		return "Empty()"

	def validate(self, path):
		node = path[-1]
		if isinstance(node, xsc.Element):
			if len(node):
				yield EmptyElementWithContentWarning(path)


class Transparent(object):
	"""
	This validator implements the "transparent" content model of HTML5:
	"""
	def validate(self, path):
		model = None
		for parent in path[-2::-1]:
			if isinstance(parent, xsc.Element) and parent.model is not None and not isinstance(parent.model, Transparent):
				model = parent.model
				break
		if model is not None:
			yield from model.validate(path)


class NoElements(object):
	"""
	This validator checks that an element does not have child elements from the
	same namespace.
	"""
	empty = False

	def __repr__(self):
		return "NoElements()"

	def validate(self, path):
		"""
		check that the content of :var:`node` is valid.
		"""
		node = path[-1]
		if isinstance(node, xsc.Element):
			for child in node.content:
				if isinstance(child, xsc.Element) and node.xmlns is not None and child.xmlns is not None and child.xmlns == node.xmlns:
					yield ElementWarning(node, child)


class NoElementsOrText(object):
	"""
	This validator checks that an element does have neither child elements
	from the same namespace nor real (i.e. not-whitespace) text nodes.
	"""
	empty = False

	def __repr__(self):
		return "NoElementsOrText()"

	def validate(self, path):
		"""
		check that the content of :var:`node` is valid.
		"""
		node = path[-1]
		if isinstance(node, xsc.Element):
			for child in node.content:
				if badtext(child):
					yield IllegalTextWarning(node, child)
				elif isinstance(child, xsc.Element) and node.xmlns is not None and child.xmlns is not None and child.xmlns == node.xmlns:
					yield ElementWarning(node, child)


class Elements(object):
	"""
	This validator checks that an element does have neither child elements
	from any of the namespaces of those elements specified in the constructor
	except for those elements itself nor real (i.e. not-whitespace) text nodes.
	"""
	empty = False

	def __init__(self, *elements):
		"""
		Every element in :var:`elements` may be in the content of the node to
		which this validator is attached. Any other element from one of the
		namespaces of those elements is invalid. Elements from other namespaces
		are OK.
		"""
		self.elements = elements

	def __repr__(self):
		return "Elements({})".format(", ".join("{0.__module__}.{0.__name__}".format(cls) for cls in self.elements))

	def validate(self, path):
		"""
		check that the content of :var:`node` is valid.
		"""
		node = path[-1]
		ns = None
		if isinstance(node, xsc.Element):
			for child in node.content:
				if badtext(child):
					warnings.warn(IllegalTextWarning(node, child))
				elif isinstance(child, xsc.Element) and node.xmlns is not None and not isinstance(child, self.elements):
					if ns is None: # Calculate the first time we need it
						ns = {el.xmlns for el in self.elements if el.xmlns is not None}
					if child.xmlns in ns:
						yield WrongElementWarning(self, path, child)


class ElementsOrText(Elements):
	"""
	This validator checks that an element doesn't have child elements from the
	same namespace except those specified in the constructor.
	"""

	def __init__(self, *elements):
		"""
		Every element in :var:`elements` may be in the content of the node to
		which this validator is attached. Any other element from one of the
		namespaces of those elements is invalid. Elements from other namespaces
		are OK.
		"""
		self.elements = elements

	def __repr__(self):
		return "ElementsOrText({})".format(", ".join("{0.__module__}.{0.__name__}".format(cls) for cls in self.elements))

	def validate(self, path):
		"""
		Check that the content of :var:`node` is valid.
		"""
		node = path[-1]
		ns = None
		if isinstance(node, xsc.Element):
			for child in node.content:
				if isinstance(child, xsc.Element) and node.xmlns is not None and not isinstance(child, self.elements):
					if ns is None: # Calculate the first time we need it
						ns = {el.xmlns for el in self.elements if el.xmlns is not None}
					if child.xmlns in ns:
						yield WrongElementWarning(self, path, child)


class Any(object):
	"""
	This validator declares any content to be valid.
	"""
	empty = False

	def __repr__(self):
		return "Any()"

	def validate(self, path):
		"""
		Check that the content of :var:`node` is valid. This method does nothing
		as anything is valid.
		"""
		yield from ()


# always show warnings from sims errors
warnings.filterwarnings("always", category=SIMSWarning)
