#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2005-2008 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
:mod:`ll.xpit` contains functions that make it possible to embed Python
expressions and conditionals in text. For example::

	from ll import xpit

	text = '''
	a = <?= a?>
	b = <?= b?>
	The sum is <?= a+b?>
	<?if a>0?>a is positive<?elif a==0?>a is 0<?else?>a is negative<?endif?>
	'''

	print xpit.convert(text, dict(a=23, b=42))

This will print::

	a = 23
	b = 42
	The sum is 65
	a is positive
"""


__docformat__ = "reStructuredText"


def tokenize(string):
	"""
	Tokenize the string :var:`string` and split it into processing instructions
	and text. :func:`tokenize` will generate tuples with the first item being
	the processing instruction target and the second being the PI data. "Text"
	content (i.e. anything other than PIs) will be returned as ``(None, data)``.
	A literal ``<?`` can be written as ``<?>`` and will be returned as text.
	"""
	pos = 0
	while True:
		pos1 = string.find("<?", pos)
		if pos1<0:
			part = string[pos:]
			if part:
				yield (None, part)
			return
		pos2 = string.find("?>", pos1)
		if pos2<0:
			part = string[pos:]
			if part:
				yield (None, part)
			return
		elif pos2 == pos1+1: # <?>
			yield (None, string[pos:pos1+2])
			pos = pos1+3
			continue
		part = string[pos:pos1]
		if part:
			yield (None, part)
		parts = string[pos1+2:pos2].split(None, 1)
		if len(parts) > 1:
			yield tuple(parts)
		else:
			yield (parts[0], parts[0][:0]) # empty string of correct type as data
		pos = pos2+2


class UnknownTargetError(ValueError):
	"""
	Exception that is raised when an unknown PI target (i.e. anything except
	``=``, ``if``, ``elif``, ``else``, ``endif``) is encountered.
	"""
	def __init__(self, target):
		self.target = target

	def __str__(self):
		return "Unknown PI target %s" % self.target


def convert(string, globals=None, locals=None):
	"""
	Convert :var:`string` using :var:`globals` and :var:`locals` as the global
	and local namespace.

	All processing instructions in :var:`string` with the target ``=`` (e.g.
	``<?=23+42?>``) will be evaluated with :var:`globals` as the global and
	:var:`locals` as the local namespace. Plain text will be passed through
	literally. Other allowed PI targets are ``if``, ``else``, ``elif`` and
	``endif``. These PIs implement conditional output. The PI content of ``if``
	and ``elif`` is evaluated as a Python expression. If it is true, everything
	after this PI (up to the next ``else``, ``endif`` etc.) will be included in
	the output. All these PIs will have :var:`globals` as the global and
	:var:`locals` as the local namespace.

	Processing instructions with other targets will raise an
	:exc:`UnknownTargetError` exception.
	"""
	v = []
	conds = [] # stack of (condition type, if-expression, else-expresion)
	for (action, data) in tokenize(string):
		if action is None:
			if all(ifcond for (type, ifcond, notelsecond) in conds):
				v.append(data)
		elif action == "if":
			cond = eval(data, globals, locals)
			conds.append(("if", cond, not cond))
		elif action == "elif":
			cond = eval(data, globals, locals)
			conds[-1] = ("elif", cond, conds[-1][2] and not cond)
		elif action == "else":
			conds[-1] = ("else", conds[-1][2], False)
		elif action == "endif":
			del conds[-1]
		elif action == "=":
			if all(ifcond for (type, ifcond, notelsecond) in conds):
				data = str(eval(data, globals, locals))
				v.append(data)
		elif action is not None:
			raise UnknownTargetError(action)
	return "".join(v)
