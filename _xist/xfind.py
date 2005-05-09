#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
This module contains XFind operators and related classes and functions.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$


import collections

import ll


###
### General iterator utilities
###

_defaultitem = object()

def item(iterator, index, default=_defaultitem):
	"""
	<par>Return the <arg>index</arg>th item from the iterator <arg>iterator</arg>.
	<arg>index</arg> must be an integer (negative integers are relative to the
	end (i.e. the last item produced by the iterator)).</par>

	<par>If <arg>default</arg> is given, this will be the default value when
	the iterator doesn't contain an item at this position. Otherwise an
	<class>IndexError</class> will be raised.</par>
	"""
	i = index
	if i>=0:
		for item in iterator:
			if not i:
				return item
			i -= 1
	else:
		i = -index
		cache = collections.deque()
		for item in iterator:
			cache.append(item)
			if len(cache)>i:
				cache.popleft()
		if len(cache)==i:
			return cache.popleft()
	if default is _defaultitem:
		raise IndexError(index)
	else:
		return default


def first(iterator, default=_defaultitem):
	"""
	<par>Return the first object produced by the iterator <arg>iterator</arg> or
	<arg>default</arg> if the iterator didn't produce any items.</par>
	<par>Calling this function will consume one item from the iterator.</par>
	"""
	return item(iterator, 0, default)


def last(iterator, default=_defaultitem):
	"""
	<par>Return the last object from the iterator <arg>iterator</arg> or
	<arg>default</arg> if the iterator didn't produce any items.</par>
	<par>Calling this function will exhaust the iterator.</par>
	"""
	return item(iterator, -1, default)


def count(iterator):
	"""
	<par>Return the number of items produced by the iterator <arg>iterator</arg>.</par>
	<par>Calling this function will exhaust the iterator.</par>
	"""
	count = 0
	for node in iterator:
		count += 1
	return count


def iterone(node):
	"""
	Return an iterator that will produce one item: <arg>node</arg>.
	"""
	yield node


###
###
###

class Iterator(object):
	__slots__ = "iterator"

	def __init__(self, iterator):
		self.iterator = iterator

	def __getitem__(self, index):
		if isinstance(index, slice):
			return list(self.iterator)[index]
		return item(self, index)

	def __iter__(self):
		return self

	def next(self):
		return self.iterator.next()

	# We can't implement __len__, because if such an object is passed to list(), __len__() would be called, exhausting the iterator

	def __nonzero__(self):
		for node in self:
			return True
		return False


###
### XFind expression
###

class Expr(Iterator):
	"""
	A <class>Expr</class> object is a <z>parsed</z> XFind expression.
	The expression <lit><rep>a</rep>/<rep>b</rep></lit> will return an
	<class>Expr</class> object if <lit><rep>a</rep></lit> is either a
	<pyref class="Node"><class>Node</class></pyref> object or an iterator
	producing nodes and <lit><rep>b</rep></lit> is an operator object, such as
	the subclasses of <pyref module="ll.xist.xsc" class="Node"><class>Node</class></pyref>
	or the instances of <pyref class="Operator"><class>Operator</class></pyref>.
	"""
	__slots__ = ("iterator", "operator")

	def __init__(self, iterator, *operators):
		from ll.xist import xsc
		if isinstance(iterator, xsc.Node):
			iterator = iterone(iterator)
		Iterator.__init__(self, iterator)
		self.operator = OperatorChain(*operators)

	def __iter__(self):
		if self.operator.operators:
			return self.operator.xfind(self.iterator)
		else:
			return self.iterator

	def __div__(self, other):
		return Expr(self.iterator, self.operator/other)

	def __floordiv__(self, other):
		return Expr(self.iterator, self.operator//other)

	def __repr__(self):
		if self.operator.operators:
			ops = "/" + "/".join(repr(op) for op in self.operator.operators)
		else:
			ops = ""
		return "<%s.%s object for %r%s at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.iterator, ops, id(self))


###
### XFind operators
###

class Operator(object):
	"""
	The base class of all XFind operators.
	"""
	def xfind(self, iterator, *operators):
		"""
		Apply <self/> to the nodes produced by <arg>iterator</arg> first, and
		apply the operators in <arg>operators</arg> in sequence to the result.
		Return an iterator. This method may be overwritten by iterators that need
		to know the other operators after themselves in the XFind expression. All
		others should overwrite <pyref method="xwalk"><method>xwalk</method></pyref>.
		"""
		# we have to resolve the iterator here
		return iter(Expr(self.xwalk(iterator), *operators))

	@ll.notimplemented
	def xwalk(self, iterator):
		"""
		Apply <self/> to the nodes produced by <arg>iterator</arg> and return
		an iterator for the result.
		"""
		pass

	def __div__(self, other):
		"""
		Return a combined iterator.
		"""
		if isinstance(other, OperatorChain):
			return OperatorChain(self, *other.operators)
		else:
			return OperatorChain(self, other)

	def __floordiv__(self, other):
		"""
		Return a combined iterator.
		"""
		if isinstance(other, OperatorChain):
			return OperatorChain(self, all, *other.operators)
		else:
			return OperatorChain(self, all, other)

	def __getitem__(self, index):
		"""
		Return an iterator that applies <self/>, but only yields the <arg>index</arg>th
		node from the result.
		"""
		if isinstance(index, slice):
			return SliceOperator(self, slice)
		else:
			return ItemOperator(self, index)

	def __getslice__(self, index1, index2):
		"""
		Return an iterator that applies <self/>, but only yields the nodes from
		the specified slice.
		"""
		return SliceOperator(self, slice(index1, index2))


class ItemOperator(Operator):
	"""
	"""
	def __init__(self, operator, index):
		self.operator = operator
		self.index = index

	def xwalk(self, iterator):
		for child in iterator:
			node = item(child/self.operator, self.index, None)
			if node is not None:
				yield node


class SliceOperator(Operator):
	"""
	"""
	def __init__(self, operator, slice):
		self.operator = operator
		self.slice = slice

	def xwalk(self, iterator):
		for child in iterator:
			for subchild in list(child/self.operator)[self.slice]: # materialize the iterator
				yield subchild


class OperatorChain(Operator):
	"""
	"""
	def __init__(self, *operators):
		newoperators = []
		for operator in operators:
			if isinstance(operator, OperatorChain):
				newoperators.extend(operator.operators)
			else:
				if not isinstance(operator, Operator):
					operator = Walker(operator)
				newoperators.append(operator)
		self.operators = newoperators

	def xwalk(self, iterator):
		if self.operators:
			return iter(Expr(self.operators[0].xfind(iterator, *self.operators[1:])))
		else:
			return iterator

	def __div__(self, other):
		if isinstance(other, OperatorChain):
			return OperatorChain(*(self.operators + other.operators))
		else:
			return OperatorChain(*(self.operators + [other]))

	def __floordiv__(self, other):
		if isinstance(other, OperatorChain):
			return OperatorChain(*(self.operators + [all] + other.operators))
		else:
			return OperatorChain(*(self.operators + [all, other]))

	def __repr__(self):
		if self.operators:
			ops = "/".join(repr(op) for op in self.operators)
		else:
			ops = ""
		return "<%s.%s for %s at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, ops, id(self))


class Walker(Operator):
	def __init__(self, function):
		self.function = function

	def xwalk(self, iterator):
		for child in iterator:
			for subchild in child.walk(self.function):
				yield subchild


class all(Operator):
	def xwalk(self, iterator):
		for child in iterator:
			for subchild in child.walk():
				yield subchild
all = all()


class attrs(Operator):
	def xwalk(self, iterator):
		from ll.xist import xsc
		for child in iterator:
			if isinstance(child, xsc.Element):
				for (attrname, attrvalue) in child.attrs.iteritems():
					yield attrvalue
attrs = attrs()


class hasattr(Operator):
	"""
	An XFind operator that acts as a filter: Only produces those element nodes
	from the left hand side of the XFind expresssion, that have an attribute
	of the type specified in the constructor.
	"""
	def __init__(self, *attrs):
		"""
		Create a <class>hasattr</class> operator. Only elements having an attribute
		of one of the types in <arg>attr</arg> will be produced.
		"""
		self.attrs = attrs

	def xwalk(self, iterator):
		from ll.xist import xsc
		for child in iterator:
			if isinstance(child, xsc.Element):
				for attrvalue in child.attrs.itervalues():
					if isinstance(attrvalue, self.attrs):
						yield child
						break

	def __repr__(self):
		return "<%s.%s object attr=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attr, id(self))


class hasattrnamed(Operator):
	"""
	An XFind operator that acts as a filter: Only produces those element nodes
	from the left hand side of the XFind expresssion, that have an attribute
	with a name specified in the constructor.
	"""
	def __init__(self, attrname, xml=False):
		"""
		Create a <class>hasattrnamed</class> operator. Only elements having an
		attribute with the name <arg>attrname</arg> will be produced.
		<arg>xml</arg> specifies whether <arg>attrname</arg> is a Python or an
		&xml; name.
		"""
		self.attrname = attrname
		self.xml = xml

	def xwalk(self, iterator):
		from ll.xist import xsc
		for child in iterator:
			if isinstance(child, xsc.Element) and child.attrs.isallowed(self.attrname, self.xml) and child.attrs.has(self.attrname, self.xml):
				yield child

	def __repr__(self):
		return "<%s.%s object attrname=%r xml=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attrname, self.xml, id(self))


class is_(Operator):
	"""
	An XFind operator that acts as a filter: Only produces those nodes from the
	left hand side of the XFind expresssion, that are of a type specified
	in the constructor.
	"""
	def __init__(self, *types):
		"""
		Create an <class>is_</class> operator. Only nodes of one of the types in
		<arg>types</arg> will be produced.
		"""
		self.types = types

	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, self.types):
				yield child

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class isnot(Operator):
	"""
	An XFind operator that acts as a filter: Only produces those nodes from the
	left hand side of the XFind expression, that are not of a type specified
	in the constructor.
	"""
	def __init__(self, *types):
		"""
		Create an <class>isnot</class> operator. Only nodes not of any of the
		types in <arg>types</arg> will be produced.
		"""
		self.types = types

	def xwalk(self, iterator):
		for child in iterator:
			if not isinstance(child, self.types):
				yield child

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class contains(Operator):
	"""
	An XFind operator that acts as a filter: Only produces elements (or fragments)
	from the left hand side of the XFind expression, that contain child node of
	a type specified in the constructor.
	"""
	def __init__(self, *types):
		"""
		Create a <class>contains</class> operator. Only elements and fragment
		containing child nodes of one of the types in <arg>types</arg> will
		be produced.
		"""
		self.types = types

	def xwalk(self, iterator):
		from ll.xist import xsc
		for child in iterator:
			if isinstance(child, (xsc.Frag, xsc.Element)):
				for subchild in child:
					if isinstance(subchild, self.types):
						yield child
						break

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class child(Operator):
	"""
	An XFind operator that produces all the child nodes of the type specified
	in the constructor for the elements (or fragments) from the left hand side
	of the XFind expresssion.
	"""
	def __init__(self, *types):
		"""
		Create a <class>child</class> operator. All child nodes of one of the
		types in <arg>types</arg> from the elements or fragments from the left
		hand side of the XFind expression will be produced.
		"""
		self.types = types

	def xwalk(self, iterator):
		from ll.xist import xsc
		for child in iterator:
			if isinstance(child, (xsc.Frag, xsc.Element)):
				for subchild in child:
					if isinstance(subchild, self.types):
						yield subchild

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class attrnamed(Operator):
	"""
	An XFind operator that produces all the attribute nodes having a name
	specified in the constructor for the elements from the left hand side of the
	XFind expresssion.
	"""

	def __init__(self, attrname, xml=False):
		"""
		Create an <class>attrnamed</class> operator. All attribute nodes having
		a name <arg>attrname</arg> from the elements from the left hand side of
		the XFind expression will be produced. <arg>xml</arg> specifies whether
		<arg>attrname</arg> is a Python or an &xml; name.
		"""
		self.attrname = attrname
		self.xml = xml

	def xwalk(self, iterator):
		from ll.xist import xsc
		for child in iterator:
			if isinstance(child, xsc.Element) and child.attrs.isallowed(self.attrname, self.xml) and child.attrs.has(self.attrname, self.xml):
				yield child.attrs.get(self.attrname, xml=self.xml)

	def __repr__(self):
		return "<%s.%s object attrname=%r xml=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attrname, self.xml, id(self))


class attr(Operator):
	"""
	An XFind operator that produces all the attribute nodes of the type specified
	in the constructor for the elements from the left hand side of the XFind
	expresssion.
	"""

	def __init__(self, *types):
		"""
		Create an <class>attr</class> operator. All attribute nodes of one of the
		types in <arg>types</arg> from the elements from the left hand side of the
		XFind expression will be produced.
		"""
		self.types = types

	def xwalk(self, iterator):
		from ll.xist import xsc
		for child in iterator:
			if isinstance(child, xsc.Element):
				for attrvalue in child.attrs.itervalues():
					if isinstance(attrvalue, self.types):
						yield attrvalue

	def __repr__(self):
		return "<%s.%s object types=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.types, id(self))
