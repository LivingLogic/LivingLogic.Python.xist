#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$


class Operator(object):
	def xfind(self, iterator, *operators):
		"""
		Apply self to the <arg>iterator</arg> first, and then the
		<arg>operators</arg> in sequence.
		"""
		# we have to resolve the iterator here
		return iter(Finder(self.xwalk(iterator), *operators))


class Finder(object):
	"""
	A <class>Finder</class> object is a <z>parsed</z> XFind expression.
	The expression <lit><rep>a</rep>/<rep>b</rep>/<rep>c</rep> will return an
	<class>Finder</class> object if <lit><rep>a</rep></lit> is either a
	<pyref class="Node"><class>Node</class></pyref> object or an
	<class>Finder</class> object and <lit><rep>b</rep></lit> and <lit><rep>c</rep></lit>
	are operator objects, such as the subclasses of <pyref module="ll.xist.xsc" class="Node"><class>Node</class></pyref>
	or the subclasses of <pyref class="Operator"><class>Operator</module></pyref>.
	"""
	__slots__ = ("iterator", "operators")

	def __init__(self, iterator, *operators):
		self.iterator = iterator
		self.operators = operators

	def next(self):
		return self.iterator.next()

	def __iter__(self):
		if self.operators:
			return self.operators[0].xfind(self.iterator, *self.operators[1:])
		else:
			return self

	def __getitem__(self, index):
		print index
		if isinstance(index, slice):
			return list(self)[index] # fall back to materializing the list
		else:
			if index>=0:
				for item in self:
					if not index:
						return item
					index -= 1
				raise IndexError
			else:
				index = -index
				cache = []
				for item in self:
					cache.append(item)
					if len(cache)>index:
						cache.pop(0)
				if len(cache)==index:
					return cache[0]
				else:
					raise IndexError

	# We can't implement __len__, because if a Finder object is passed to list(), __len__() would be called, exhausting the iterator

	def __nonzero__(self):
		for node in self:
			return True
		return False

	def __div__(self, other):
		return Finder(self.iterator, *(self.operators + (other,)))

	def __floordiv__(self, other):
		return Finder(self.iterator, *(self.operators + (xfind.all, other)))

	def __repr__(self):
		if self.operators:
			ops = "/" + "/".join([repr(op) for op in self.operators])  # FIXME: Use a GE in Python 2.4
		else:
			ops = ""
		return "<%s.%s object for %r%s at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.iterator, ops, id(self))


def first(iterator, default=None):
	"""
	<par>Return the first object produced by the iterator <arg>iterator</arg> or
	<arg>default</arg> if the iterator didn't produce any items.</par>
	<par>Calling this function will consume one item from the iterator.</par>
	"""
	for node in iterator:
		return node
	return default


def last(iterator, default=None):
	"""
	<par>Return the last object from the iterator <arg>iterator</arg> or
	<arg>default</arg> if the iterator didn't produce any items.</par>
	<par>Calling this function will exhaust the iterator.</par>
	"""
	node = default
	for node in iterator:
		pass
	return node


def count(iterator):
	"""
	<par>Return the number of items produced by the iterator <arg>iterator</arg>.</par>
	<par>Calling this function will exhaust the iterator.</par>
	"""
	count = 0
	for node in iterator:
		count += 1
	return count


class all(Operator):
	def xwalk(self, iterator):
		for child in iterator:
			for subchild in child.walk():
				yield subchild
all = all()


class attrs(Operator):
	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, xsc.Element):
				for (attrname, attrvalue) in child.attrs.iteritems():
					yield attrvalue
attrs = attrs()


class hasattr(Operator):
	def __init__(self, attr):
		self.attr = attr

	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, xsc.Element):
				for attrvalue in child.attrs.itervalues():
					if isinstance(attrvalue, self.attr):
						yield child
						break

	def __repr__(self):
		return "<%s.%s object attr=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attr, id(self))


class hasattrnamed(Operator):
	def __init__(self, attrname, xml=False):
		self.attrname = attrname
		self.xml = xml

	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, xsc.Element) and child.attrs.isallowed(self.attrname, self.xml) and child.attrs.has(self.attrname, self.xml):
				yield child

	def __repr__(self):
		return "<%s.%s object attrname=%r xml=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attrname, self.xml, id(self))


class is_(Operator):
	def __init__(self, class_):
		self.class_= class_

	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, self.class_):
				yield child

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class isnot(Operator):
	def __init__(self, class_):
		self.class_= class_

	def xwalk(self, iterator):
		for child in iterator:
			if not isinstance(child, self.class_):
				yield child

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class contains(Operator):
	def __init__(self, class_):
		self.class_= class_

	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, (xsc.Frag, xsc.Element)):
				for subchild in child:
					if isinstance(subchild, self.class_):
						yield child
						break

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class child(Operator):
	def __init__(self, class_):
		self.class_= class_

	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, (xsc.Frag, xsc.Element)):
				for subchild in child:
					if isinstance(subchild, self.class_):
						yield subchild

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class attrnamed(Operator):
	def __init__(self, attrname, xml=False):
		self.attrname = attrname
		self.xml = xml

	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, xsc.Element) and child.attrs.isallowed(self.attrname, self.xml) and child.attrs.has(self.attrname, self.xml):
				yield child.attrs.get(self.attrname, xml=self.xml)

	def __repr__(self):
		return "<%s.%s object attrname=%r xml=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attrname, self.xml, id(self))


class attr(Operator):
	def __init__(self, attr):
		self.attr = attr

	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, xsc.Element):
				for attrvalue in child.attrs.itervalues():
					if isinstance(attrvalue, self.attr):
						yield attrvalue

	def __repr__(self):
		return "<%s.%s object attr=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attr, id(self))
