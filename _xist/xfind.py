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


from ll.xist import xsc


class all(object):
	def xfind(self, lhs):
		for child in lhs:
			for subchild in child.walk():
				yield subchild
all = all()


class attrs(object):
	def xfind(self, lhs):
		for child in lhs:
			if isinstance(child, xsc.Element):
				for (attrname, attrvalue) in child.attrs.iteritems():
					yield attrvalue
attrs = attrs()


class hasattr(object):
	def __init__(self, attr):
		self.attr = attr

	def xfind(self, lhs):
		for child in lhs:
			if isinstance(child, xsc.Element):
				for attrvalue in child.attrs.itervalues():
					if isinstance(attrvalue, self.attr):
						yield attrvalue

	def __repr__(self):
		return "<%s.%s object attr=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attr, id(self))


class hasattrnamed(object):
	def __init__(self, attrname, xml=False):
		self.attrname = attrname
		self.xml = xml

	def xfind(self, lhs):
		for child in lhs:
			if isinstance(child, xsc.Element) and child.attrs.isallowed(self.attrname, self.xml) and child.attrs.has(self.attrname, self.xml):
				yield child

	def __repr__(self):
		return "<%s.%s object attrname=%r xml=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attrname, self.xml, id(self))


class is_(object):
	def __init__(self, class_):
		self.class_= class_

	def xfind(self, lhs):
		for child in lhs:
			if isinstance(child, self.class_):
				yield child

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class isnot(object):
	def __init__(self, class_):
		self.class_= class_

	def xfind(self, lhs):
		for child in lhs:
			if not isinstance(child, self.class_):
				yield child

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class contains(object):
	def __init__(self, class_):
		self.class_= class_

	def xfind(self, lhs):
		for child in lhs:
			if isinstance(child, (xsc.Frag, xsc.Element)):
				for subchild in child:
					if isinstance(subchild, self.class_):
						yield child
						break

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class child(object):
	def __init__(self, class_):
		self.class_= class_

	def xfind(self, lhs):
		for child in lhs:
			if isinstance(child, (xsc.Frag, xsc.Element)):
				for subchild in child:
					if isinstance(subchild, self.class_):
						yield subchild

	def __repr__(self):
		return "<%s.%s object class=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.class_, id(self))


class attrnamed(object):
	def __init__(self, attrname, xml=False):
		self.attrname = attrname
		self.xml = xml

	def xfind(self, lhs):
		for child in lhs:
			if isinstance(child, xsc.Element) and child.attrs.isallowed(self.attrname, self.xml) and child.attrs.has(self.attrname, self.xml):
				yield child.attrs.get(self.attrname, xml=self.xml)

	def __repr__(self):
		return "<%s.%s object attrname=%r xml=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attrname, self.xml, id(self))


class attr(object):
	def __init__(self, attr):
		self.attr = attr

	def xfind(self, lhs):
		for child in lhs:
			if isinstance(child, xsc.Element):
				for attrvalue in child.attrs.itervalues():
					if isinstance(attrvalue, self.attr):
						yield attrvalue

	def __repr__(self):
		return "<%s.%s object attr=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.attr, id(self))
