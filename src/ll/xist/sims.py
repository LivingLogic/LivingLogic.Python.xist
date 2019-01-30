# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
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

	def __hash__(self):
		return hash(str(self))

	def __eq__(self, other):
		return isinstance(other, self.__class__) and str(self) == str(other)


class EmptyElementWithContentWarning(SIMSWarning):
	"""
	Warning that is issued when an element has content, but it shouldn't
	(i.e. :attr:`model` is :class:`Empty`)
	"""

	def __init__(self, path):
		self.path = tuple(path)

	def __str__(self):
		return f"{self.path[-1]._str()} doesn't allow content"


class WrongElementWarning(SIMSWarning):
	"""
	Warning that is issued when an element contains another element of a
	certain type, but shouldn't.
	"""

	def __init__(self, path, badnode):
		self.path = tuple(path)
		self.badnode = badnode

	def __str__(self):
		return f"{self.path[-1]._str()} may not contain {self.badnode._str()}"


class ElementWarning(SIMSWarning):
	"""
	Warning that is issued when an element contains another element but
	shouldn't contain any.
	"""

	def __init__(self, path, badnode):
		self.path = tuple(path)
		self.badnode = badnode

	def __str__(self):
		return f"{self.path[-1]._str()} may not contain other elements"


class IllegalTextWarning(SIMSWarning):
	"""
	Warning that is issued when an element contains a text node but shouldn't.
	"""

	def __init__(self, path, badnode):
		self.path = tuple(path)
		self.badnode = badnode

	def __str__(self):
		return f"{self.path[-1]._str()} may not contain text"


class AnyWarning(SIMSWarning):
	"""
	Warning that is issued when an element contains a text node but shouldn't.
	"""

	def __init__(self, path, warnings):
		self.path = tuple(path)
		self.warnings = warnings

	def __str__(self):
		return " or ".join(" and ".join(f"({warning})" for warning in warnings) for warnings in self.warnings)


def badtext(node):
	"""
	Return whether :obj:`node` is a text node (i.e. :class:`ll.xist.xsc.Text`
	that does not consist of whitespace only).
	"""
	if isinstance(node, xsc.Text):
		if node and not node.isspace():
			return True
	return False


class Empty:
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


class Transparent:
	"""
	This validator implements the "transparent" content model of HTML5.
	"""
	empty = False

	def validate(self, path):
		model = None
		for parent in path[-2::-1]:
			if isinstance(parent, xsc.Element) and parent.model is not None and not isinstance(parent.model, Transparent):
				model = parent.model
				break
		if model is not None:
			yield from model.validate(path)


class NoElements:
	"""
	This validator checks that an element does not have child elements from the
	same namespace.
	"""
	empty = False

	def __repr__(self):
		return "NoElements()"

	def validate(self, path):
		"""
		check that the content of :obj:`node` is valid.
		"""
		node = path[-1]
		if isinstance(node, xsc.Element):
			for child in node.content:
				if isinstance(child, xsc.Element) and node.xmlns is not None and child.xmlns is not None and child.xmlns == node.xmlns:
					yield ElementWarning(path, child)


class NoElementsOrText:
	"""
	This validator checks that an element does have neither child elements
	from the same namespace nor real (i.e. not-whitespace) text nodes.
	"""
	empty = False

	def __repr__(self):
		return "NoElementsOrText()"

	def validate(self, path):
		"""
		check that the content of :obj:`node` is valid.
		"""
		node = path[-1]
		if isinstance(node, xsc.Element):
			for child in node.content:
				if badtext(child):
					yield IllegalTextWarning(path, child)
				elif isinstance(child, xsc.Element) and node.xmlns is not None and child.xmlns is not None and child.xmlns == node.xmlns:
					yield ElementWarning(path, child)


class Elements:
	"""
	This validator checks that an element does have neither child elements
	from any of the namespaces of those elements specified in the constructor
	except for those elements itself nor real (i.e. not-whitespace) text nodes.
	"""
	empty = False

	def __init__(self, *elements):
		"""
		Every element in :obj:`elements` may be in the content of the node to
		which this validator is attached. Any other element from one of the
		namespaces of those elements is invalid. Elements from other namespaces
		are OK.
		"""
		self.elements = elements

	def __repr__(self):
		elements = ", ".join(f"{cls.__module__}.{cls.__qualname__}" for cls in self.elements)
		return f"Elements({elements})"

	def validate(self, path):
		"""
		check that the content of :obj:`node` is valid.
		"""
		node = path[-1]
		ns = None
		if isinstance(node, xsc.Element):
			for child in node.content:
				if badtext(child):
					yield IllegalTextWarning(path, child)
				elif isinstance(child, xsc.Element) and node.xmlns is not None and not isinstance(child, self.elements):
					if ns is None: # Calculate the first time we need it
						ns = {el.xmlns for el in self.elements if el.xmlns is not None}
					if child.xmlns in ns:
						yield WrongElementWarning(path, child)


class ElementsOrText(Elements):
	"""
	This validator checks that an element doesn't have child elements from the
	same namespace except those specified in the constructor.
	"""

	def __init__(self, *elements):
		"""
		Every element in :obj:`elements` may be in the content of the node to
		which this validator is attached. Any other element from one of the
		namespaces of those elements is invalid. Elements from other namespaces
		are OK.
		"""
		self.elements = elements

	def __repr__(self):
		elements = ", ".join(f"{cls.__module__}.{cls.__name__}" for cls in self.elements)
		return f"ElementsOrText({elements})"

	def validate(self, path):
		"""
		Check that the content of :obj:`node` is valid.
		"""
		node = path[-1]
		ns = None
		if isinstance(node, xsc.Element):
			for child in node.content:
				if isinstance(child, xsc.Element) and node.xmlns is not None and not isinstance(child, self.elements):
					if ns is None: # Calculate the first time we need it
						ns = {el.xmlns for el in self.elements if el.xmlns is not None}
					if child.xmlns in ns:
						yield WrongElementWarning(path, child)


class NotElements:
	"""
	This validator checks that an element doesn't contain any of the specified
	elements.
	"""
	empty = False

	def __init__(self, *elements):
		"""
		Every element in :obj:`elements` may not be in the content of the node to
		which this validator is attached.
		"""
		self.elements = elements

	def __repr__(self):
		elements = ", ".join(f"{cls.__module__}.{cls.__name__}" for cls in self.elements)
		return f"NotElements({elements})"

	def validate(self, path):
		node = path[-1]
		if isinstance(node, xsc.Element):
			for child in node.content:
				if isinstance(child, self.elements):
					yield WrongElementWarning(path, child)


class All:
	"""
	This meta validator checks that all its child validators declare the content
	of the element to be valid.
	"""
	empty = False

	def __init__(self, *validators):
		self.validators = validators

	def __repr__(self):
		validators = " ".join(repr(validator) for validator in self.validators)
		return f"<{self.__class__.__module__}:{self.__class__.__qualname__} {validators} at {id(self):#x}>"

	def validate(self, path):
		seen = set()
		for validator in self.validators:
			for warning in validator.validate(path):
				if warning not in seen:
					yield warning
					seen.add(warning)


class Any:
	"""
	This meta validator checks that at least one of its child validators declares
	the content of the element to be valid.
	"""
	empty = False

	def __init__(self, *validators):
		self.validators = validators

	def __repr__(self):
		validators = " ".join(repr(validator) for validator in self.validators)
		return f"<{self.__class__.__module__}:{self.__class__.__qualname__} {validators} at {id(self):#x}>"

	def validate(self, path):
		if self.validators:
			seen = set()
			allwarnings = []
			for validator in self.validators:
				warnings = list(validator.validate(path))
				if not warnings:
					return
				allwarnings.append(warnings)
			# If a warning is in all alternatives, we can report it as a separate warning and remove it from the alternatives
			restwarnings = allwarnings[1:]
			for warning in allwarnings[0]:
				if all(warning in warnings for warnings in restwarnings):
					seen.add(warning)
					yield warning
					for warnings in allwarnings:
						warnings.remove(warning)
			# If any of the alternatives is empty now, remove it
			allwarnings = [warnings for warnings in allwarnings if warnings]
			if allwarnings:
				# if we have only one alternative left, split it into individual warnings again
				if len(allwarnings) == 1:
					for warning in allwarnings[0]:
						if warning not in seen:
							yield warning
				else:
					yield AnyWarning(path, allwarnings)


# always show warnings from sims errors
warnings.simplefilter("always", category=SIMSWarning)
