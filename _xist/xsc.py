#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
This module contains all the central &dom; classes, the namespace classes and a few helper
classes and functions.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from __future__ import generators

import os, types, sys, urllib, random

from ll import url, ansistyle

import presenters, publishers, sources, cssparsers, converters, errors, options, utils, helpers

###
### helpers
###

def ToNode(value):
	"""
	<par>convert the <arg>value</arg> passed in to an &xist; <pyref class="Node"><class>Node</class></pyref>.</par>

	<par>If <arg>value</arg> is a tuple or list, it will be (recursively) converted
	to a <pyref class="Frag"><class>Frag</class></pyref>. Integers, strings, etc. will be converted to a
	<pyref class="Text"><class>Text</class></pyref>.
	If <arg>value</arg> is a <pyref class="Node"><class>Node</class></pyref> already, nothing will be done.
	In the case of <lit>None</lit> the &xist; Null (<class>xsc.Null</class>) will be returned).
	Anything else raises an exception.</par>
	"""
	if isinstance(value, Node):
		if isinstance(value, Attr):
			return Frag(*value) # repack the attribute in a fragment, and we have a valid XSC node
		return value
	elif isinstance(value, url.URL):
		return Text(value)
	elif isinstance(value, (str, unicode, int, long, float)):
		return Text(value)
	elif value is None:
		return Null
	elif isinstance(value, (list, tuple)):
		return Frag(*value)
	errors.warn(errors.IllegalObjectWarning(value)) # none of the above, so we report it and maybe throw an exception
	return Null

###
###
###

class Base(object):
	"""
	<par>Base class that adds an enhanced class <method>__repr__</method>
	and a class method <pyref method="__fullname__"><method>__fullname</method></pyref>
	to subclasses. Subclasses of <class>Base</class> will have an attribute
	<lit>__outerclass__</lit> that references the containing class (if there
	is any). <method>__repr__</method> uses this to show the fully qualified
	class name.</par>
	"""
	class __metaclass__(type):
		def __new__(cls, name, bases, dict):
			dict["__outerclass__"] = None
			res = type.__new__(cls, name, bases, dict)
			for (key, value) in dict.items():
				if isinstance(value, type):
					value.__outerclass__ = res
			return res
		def __repr__(self):
			return "<class %s/%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def __fullname__(cls):
		"""
		<par>Return the fully qualified class name (i.e. including containing
		classes, if this class has been defined inside another one).</par>
		"""
		name = cls.__name__
		while 1:
			cls = cls.__outerclass__
			if cls is None:
				return name
			name = cls.__name__ + "." + name
	__fullname__ = classmethod(__fullname__)

class Node(Base):
	"""
	base class for nodes in the document tree. Derived classes must
	overwrite <pyref method="convert"><method>convert</method></pyref>
	and may overwrite <pyref method="publish"><method>publish</method></pyref>
	and <pyref method="__unicode__"><method>__unicode__</method></pyref>.
	"""
	empty = True

	# location of this node in the XML file (will be hidden in derived classes, but is
	# specified here, so that no special tests are required. In derived classes
	# this will be set by the parser)
	startLoc = None
	endLoc = None

	# specifies that this class should be registered in a namespace
	# this won't be used for all the DOM classes (Element, ProcInst etc.) themselves but only for derived classes
	# i.e. Node, Element etc. will never be registered

	class __metaclass__(Base.__metaclass__):
		def __new__(cls, name, bases, dict):
			if not dict.has_key("xmlname"):
				xmlname = name
				dict["xmlname"] = xmlname
			dict["xmlns"] = None
			if not dict.has_key("register"):
				dict["register"] = True
			# needsxmlns may be defined a constant, this magically turns it into method
			if dict.has_key("needsxmlns"):
				needsxmlns_value = dict["needsxmlns"]
				if not isinstance(needsxmlns_value, classmethod):
					def needsxmlns(cls, publisher=None):
						return needsxmlns_value
					dict["needsxmlns"] = classmethod(needsxmlns)
			if dict.has_key("xmlprefix"):
				xmlprefix_value = dict["xmlprefix"]
				if not isinstance(xmlprefix_value, classmethod):
					def xmlprefix(cls, publisher=None):
						return xmlprefix_value
					dict["xmlprefix"] = classmethod(xmlprefix)
			return Base.__metaclass__.__new__(cls, name, bases, dict)

	def _registerns(cls, ns):
		cls.xmlns = None
	_registerns = classmethod(_registerns)

	def __repr__(self):
		return self.repr(presenters.defaultPresenterClass())

	def __ne__(self, other):
		return not self==other

	def _strbase(cls, formatter, s, fullname, xmlname):
		if fullname:
			if xmlname:
				s.append(presenters.strNamespace(cls.xmlprefix()))
			else:
				s.append(presenters.strNamespace(cls.__module__))
			s.append(presenters.strColon())
		if xmlname:
			s.append(formatter(cls.xmlname))
		elif fullname:
			s.append(formatter(cls.__fullname__()))
		else:
			s.append(formatter(cls.__name__))
	_strbase = classmethod(_strbase)

	def clone(self):
		"""
		returns an identical clone of the node and it's children.
		"""
		raise NotImplementedError("clone method not implemented in %s" % self.__class__.__name__)

	def repr(self, presenter=None):
		"""
		<par>Return a string representation of <self/>.
		When you don't pass in a <arg>presenter</arg>, you'll
		get the default presentation. Else <arg>presenter</arg>
		should be an instance of <pyref module="ll.xist.presenters" class="Presenter"><class>xist.presenters.Presenter</class></pyref>
		(or one of the subclasses).</par>
		"""
		if presenter is None:
			presenter = presenters.defaultPresenterClass()
		return presenter.doPresentation(self)

	def present(self, presenter):
		"""
		<par><method>present</method> is used as a central
		dispatch method for the <pyref module="ll.xist.presenters">presenter classes</pyref>.
		Normally it is not called by the user, but internally by the
		presenter. The user should call <pyref method="repr"><method>repr</method></pyref>
		instead.</par>
		"""
		raise NotImplementedError("present method not implemented in %s" % self.__class__.__name__)

	def conv(self, converter=None, root=None, mode=None, stage=None, target=None, lang=None, makeaction=None, maketarget=None):
		"""
		<par>returns a version of this node and it's content converted to &html; (or any other target).</par>
		"""
		if converter is None:
			return self.convert(converters.Converter(root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, maketarget=maketarget))
		else:
			converter.push(root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, maketarget=maketarget)
			node = self.convert(converter)
			converter.pop()
			return node

	def convert(self, converter):
		"""
		<par>implementation of the conversion method.
		When you define your own element classes you have to overwrite this method.</par>

		<par>E.g. when you want to define an element that packs it's content into an &html;
		bold element, do the following:

		<programlisting>
		class foo(xsc.Element):
			empty = False

			def convert(self, converter):
				return html.b(self.content).convert(converter)
		</programlisting>
		</par>
		"""
		raise NotImplementedError("convert method not implemented in %s" % self.__class__.__name__)

	def __unicode__(self):
		"""
		<par>returns this node as a (unicode) string.
		Comments and processing instructions will be filtered out.
		For elements you'll get the element content.</par>

		<par>It might be useful to overwrite this function in your own
		elements. Suppose you have the following element:
		<programlisting>
		class caps(xsc.Element):
			empty = False

			def convert(self, converter):
				return html.span(
					self.content.convert(converter),
					style="font-variant: small-caps;"
				)
		</programlisting>

		that renders its content in small caps, then it might be useful
		to define <method>__unicode__</method> in the following way:
		<programlisting>
		def __unicode__(self):
			return unicode(self.content).upper()
		</programlisting>

		<method>__unicode__</method> can be used everywhere where
		a plain string representation of the node is required.</par>
		"""
		raise NotImplementedError("__unicode__ method not implemented in %s" % self.__class__.__name__)

	def asPlainString(self):
		errors.warn(DeprecationWarning("asPlainString() is deprecated, use unicode() (or str()) instead"))
		return unicode(self)

	def __str__(self):
		return str(unicode(self))

	def asText(self, monochrome=1, squeezeBlankLines=0, lineNumbers=0, cols=80):
		"""
		<par>Return the node as a formatted plain &ascii; string.
		Note that this really only make sense for &html; trees.</par>

		<par>This requires that <app moreinfo="http://w3m.sf.net/">w3m</app> is installed.</par>
		"""

		options = ""
		if monochrome==1:
			options += " -M"
		if squeezeBlankLines==1:
			options += " -S"
		if lineNumbers==1:
			options += " -num"
		if cols!=80:
			options += " -cols %d" % cols

		text = self.asBytes(encoding="us-ascii")

		(stdin, stdout) = os.popen2("w3m %s -T text/html -dump" % options)

		stdin.write(text)
		stdin.close()
		text = stdout.read()
		stdout.close()
		text = "\n".join([ line.rstrip() for line in text.splitlines()])
		return text

	def __int__(self):
		"""
		returns this node converted to an integer.
		"""
		return int(unicode(self))

	def __long__(self):
		"""
		returns this node converted to an integer.
		"""
		return long(unicode(self))

	def asFloat(self, decimal=".", ignore=""):
		"""
		<par>returns this node converted to a float. <arg>decimal</arg>
		specifies which decimal separator is used in the value
		(e.g. <lit>"."</lit> (the default) or <lit>","</lit>).
		<arg>ignore</arg> specifies which character will be ignored.</par>
		"""
		s = unicode(self)
		for c in ignore:
			s = s.replace(c, "")
		if decimal != ".":
			s = s.replace(decimal, ".")
		return float(s)

	def __float__(self):
		"""
		returns this node converted to a float.
		"""
		return self.asFloat()

	def __complex__(self):
		"""
		returns this node converted to an integer.
		"""
		return long(unicode(self))

	def needsxmlns(self, publisher=None):
		"""
		<par>Return what type of namespace prefix/declaration
		is needed for <self/> when publishing. Possible return
		values are:</par>
		<ulist>
		<item><lit>0</lit>: Neither a prefix nor a declaration
		is required;</item>
		<item><lit>1</lit>: A prefix is required, but no
		declaration (e.g. for the <pyref module="ll.xist.ns.xml"><module>xml</module></pyref>
		namespace, whose prefix is always defined.</item>
		<item><lit>2</lit>: Both a prefix and a declaration
		for this prefix are required.</item>
		</ulist>
		<par>The implementation of this method for
		<pyref class="Element"><class>Element</class></pyref>,
		<pyref class="ProcInst"><class>ProcInst</class></pyref> and
		<pyref class="Entity"><class>Entity</class></pyref>
		fetch this information from the <arg>publisher</arg>.</par>
		"""
		return 0
	needsxmlns = classmethod(needsxmlns)

	def xmlprefix(cls, publisher=None):
		"""
		<par>Return the namespace prefix configured for publishing the
		instances of this class with the publisher <arg>publisher</arg>
		(or the default prefix from the namespace if <arg>publisher</arg>
		is <lit>None</lit>.</par>
		"""
		if cls.xmlns is None:
			return None
		else:
			return cls.xmlns.xmlprefix
	xmlprefix = classmethod(xmlprefix)

	def _publishName(self, publisher):
		if self.needsxmlns(publisher)>=1:
			prefix = self.xmlprefix(publisher)
			if prefix is not None:
				publisher.publish(prefix)
				publisher.publish(u":")
		publisher.publish(self.xmlname)

	def parsed(self, handler):
		"""
		<par>This method will be called by the parsing handler <arg>handler</arg>
		once after <self/> is created by the parser. This is e.g. used by
		<pyref class="URLAttr"><class>URLAttr</class></pyref> to incorporate
		the base <pyref module="ll.url" class="URL"><class>URL</class></pyref>
		<arg>base</arg> into the attribute.</par>
		"""
		pass

	def publish(self, publisher):
		"""
		<par>generates unicode strings for the node, and passes
		the strings to the callable object <arg>publisher</arg>.</par>

		<par>The encoding and xhtml specification are taken from the <arg>publisher</arg>.</par>
		"""
		raise NotImplementedError("publish method not implemented in %s" % self.__class__.__name__)

	def asString(self, base=None, root=None, xhtml=None, prefixes=None, elementmode=1, procinstmode=0, entitymode=0):
		"""
		<par>returns this element as a unicode string.</par>

		<par>For the parameters see <pyref method="publish"><method>publish</method></pyref>.</par>
		"""
		publisher = publishers.StringPublisher(base=base, root=root, xhtml=xhtml, prefixes=prefixes, elementmode=elementmode, procinstmode=procinstmode, entitymode=entitymode)
		return publisher.doPublication(self)

	def asBytes(self, base=None, root=None, encoding=None, xhtml=None, prefixes=None, elementmode=1, procinstmode=0, entitymode=0):
		"""
		<par>returns this element as a byte string suitable for writing
		to an &html; file or printing from a CGI script.</par>

		<par>For the parameters see <pyref method="publish"><method>publish</method></pyref>.</par>
		"""
		publisher = publishers.BytePublisher(base=base, root=root, encoding=encoding, xhtml=xhtml, prefixes=prefixes, elementmode=elementmode, procinstmode=procinstmode, entitymode=entitymode)
		return publisher.doPublication(self)

	def write(self, stream, base=None, root=None, encoding=None, xhtml=None, prefixes=None, elementmode=1, procinstmode=0, entitymode=0):
		"""
		<par>writes the element to the file like object <arg>file</arg>.</par>

		<par>For the rest of the parameters see <pyref method="publish"><method>publish</method></pyref>.</par>
		"""
		publisher = publishers.FilePublisher(stream, base=base, root=root, encoding=encoding, xhtml=xhtml, prefixes=prefixes, elementmode=elementmode, procinstmode=procinstmode, entitymode=entitymode)
		return publisher.doPublication(self)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		"""
		<par>returns a fragment which contains child elements of this node.</par>

		<par>If you specify <arg>type</arg> as the class of an XSC node only nodes
		of this class will be returned. If you pass a list of classes, nodes that are an
		instance of one of the classes will be returned.</par>

		<par>If you set <arg>subtype</arg> to <lit>1</lit> nodes that are a
		subtype of <arg>type</arg> will be returned too.</par>

		<par>If you pass a dictionary as <arg>attrs</arg> it has to contain
		string pairs and is used to match attribute values for elements. To match
		the attribute values their <pyref class="Node" method="__unicode__"><method>__unicode__</method></pyref>
		representation will be used. You can use <lit>None</lit> as the value to test that
		the attribute is set without testing the value.</par>

		<par>Additionally you can pass a test function in <arg>test</arg>, that
		returns <lit>1</lit>, when the node passed in has to be included in the
		result and <lit>0</lit> otherwise.</par>

		<par>If you set <arg>searchchildren</arg> to <lit>1</lit> not only
		the immediate children but also the grandchildren will be searched for nodes
		matching the other criteria.</par>

		<par>If you set <arg>searchattrs</arg> to <lit>1</lit> the attributes
		of the nodes (if <arg>type</arg> is <pyref class="Element"><class>Element</class></pyref>
		or one of its subtypes) will be searched too.</par>

		<par>Note that the node has to be of type <pyref class="Element"><class>Element</class></pyref>
		(or a subclass of it) to match <arg>attrs</arg>.</par>
		"""
		node = Frag()
		if self._matches(type, subtype, attrs, test):
			node.append(self)
		return node

	def compact(self):
		"""
		returns a version of <self/>, where textnodes or character references that contain
		only linefeeds are removed, i.e. potentially needless whitespace is removed.
		"""
		raise NotImplementedError("compact method not implemented in %s" % self.__class__.__name__)

	def _matchesAttrs(self, attrs):
		if attrs is None:
			return 1
		else:
			if isinstance(self, Element):
				for attr in attrs.keys():
					if (not self.hasAttr(attr)) or ((attrs[attr] is not None) and (unicode(self[attr]) != attrs[attr])):
						return 0
				return 1
			else:
				return 0

	def _matches(self, type_, subtype, attrs, test):
		res = 1
		if type_ is not None:
			if not isinstance(type_, list) and not isinstance(type_, tuple):
				type_ = (type_,)
			for t in type_:
				if subtype:
					if isinstance(self, t):
						res = self._matchesAttrs(attrs)
						break
				else:
					if self.__class__ == t:
						res = self._matchesAttrs(attrs)
						break
			else:
				res = 0
		else:
			res = self._matchesAttrs(attrs)
		if res and (test is not None):
			res = test(self)
		return res

	def _decorateNode(self, node):
		"""
		<par>decorate the <pyref class="Node"><class>Node</class></pyref>
		<arg>node</arg> with the same location information as <self/>.</par>
		"""

		node.startLoc = self.startLoc
		node.endLoc = self.endLoc
		return node

	def mapped(self, function):
		"""
		<par>returns the node mapped through the function <arg>function</arg>.
		This call works recursively (for <pyref class="Frag"><class>Frag</class></pyref>
		and <pyref class="Element"><class>Element</class></pyref>).</par>
		<par>When you want an unmodified node you simply can return <self/>. <method>mapped</method>
		will make a copy of it and fill the content recursively. Note that element attributes
		will not be mapped. When you return a different node from <function>function</function>
		this node will be incorporated into the result as-is.</par>
		"""
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		return node

	def normalized(self):
		"""
		<par>return a normalized version of <self/>, which means, that consecutive
		<pyref class="Text"><class>Text</class> nodes</pyref> are merged.</par>
		"""
		return self

	def __mul__(self, factor):
		"""
		<par>return a <pyref class="Frag"><class>Frag</class></pyref> with <arg>factor</arg> times
		the node as an entry. Note that the node will not be copied, i.e. it is a
		<z>shallow <method>__mul__</method></z>.</par>
		"""
		return Frag(*factor*[self])

	def __rmul__(self, factor):
		"""
		<par>returns a <pyref class="Frag"><class>Frag</class></pyref> with <arg>factor</arg> times
		the node as an entry.</par>
		"""
		return Frag(*[self]*factor)

	def pretty(self, level=0, indent="\t"):
		"""
		<par>Returns a prettyfied version of <self/>, i.e. one with
		properly nested and indented tags (as far as possible). If an element
		has mixed content (i.e. <pyref class="Text"><class>Text</class></pyref> and
		non-<pyref class="Text"><class>Text</class></pyref> nodes) the content will be
		returned as is.</par>
		<par>Note that whitespace will prevent pretty printing too, so
		you might want to call <pyref method="normalized"><method>normalized</method></pyref>
		and <pyref method="compact"><method>compact</method></pyref> before
		calling <method>pretty</method> to remove whitespace.</par>
		"""
		if level==0:
			return self
		else:
			return Frag(indent*level, self)

	def walk(self, before=True, after=False, attrs=False, attrbefore=True, attrafter=False):
		"""
		<par>walk the tree. This method is a generator.</par>
		<par>For <pyref class="Frag"><class>Frag</class>s</pyref> and
		<pyref class="Element"><class>Element</class>s</pyref> nodes
		it's possible to specify whether they should be <lit>yield</lit>ed
		before or after their children (or both, or none
		in which case only leaf nodes will be <lit>yield</lit>ed) through
		<arg>before</arg> and <arg>after</arg>. <arg>attrs</arg>
		specifies wether attribute content should be walked too,
		a with <arg>attrbefore</arg> and <arg>attrafter</arg> it can
		be specified how the attribute node itself should be <lit>yield</lit>ed.</par>
		"""
		yield self

	def walkPath(self, before=True, after=False, attrs=False, attrsbefore=True, attrafter=False):
		"""
		<par>walk the tree. This method is a generator and for each node
		in the tree generates a list with the <z>path</z> to the node, i.e.
		the node and all its ancestor nodes.</par>
		<par>For the arguments see <pyref method="walk"><method>walk</method></pyref>.</par>
		"""
		yield [self]

class CharacterData(Node):
	"""
	<par>base class for &xml; character data (text, proc insts, comment, doctype etc.)</par>

	<par>provides nearly the same functionality as <class>UserString</class>,
	but omits a few methods.</par>
	"""

	def __init__(self, content=u""):
		self.__content = unicode(content)

	def __getContent(self):
		return self.__content

	content = property(__getContent, None, None, "<par>The text content of the node as a <class>unicode</class> object.</par>")

	def __hash__(self):
		return self.__content.__hash__()

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.content==other.content

	def __len__(self):
		return self.__content.__len__()

	def __getitem__(self, index):
		return self.__class__(self.__content.__getitem__(index))

	def __add__(self, other):
		return self.__class__(self.__content + other)

	def __radd__(self, other):
		return self.__class__(unicode(other) + self.__content)

	def __mul__(self, n):
		return self.__class__(n * self.__content)

	def __rmul__(self, n):
		return self.__class__(n * self.__content)

	def __getslice__(self, index1, index2):
		return self.__class__(self.__content.__getslice__(index1, index2))

	def capitalize(self):
		return self.__class__(self.__content.capitalize())

	def center(self, width):
		return self.__class__(self.__content.center(width))

	def count(self, sub, start=0, end=sys.maxint):
		return self.__content.count(sub, start, end)

	# find will be the one inherited from Node

	def endswith(self, suffix, start=0, end=sys.maxint):
		return self.__content.endswith(suffix, start, end)

	def index(self, sub, start=0, end=sys.maxint):
		return self.__content.index(sub, start, end)

	def isalpha(self):
		return self.__content.isalpha()

	def isalnum(self):
		return self.__content.isalnum()

	def isdecimal(self):
		return self.__content.isdecimal()

	def isdigit(self):
		return self.__content.isdigit()

	def islower(self):
		return self.__content.islower()

	def isnumeric(self):
		return self.__content.isnumeric()

	def isspace(self):
		return self.__content.isspace()

	def istitle(self):
		return self.__content.istitle()

	def isupper(self):
		return self.__content.isupper()

	def join(self, frag):
		return frag.withSep(self)

	def ljust(self, width):
		return self.__class__(self.__content.ljust(width))

	def lower(self):
		return self.__class__(self.__content.lower())

	def lstrip(self):
		return self.__class__(self.__content.lstrip())

	def replace(self, old, new, maxsplit=-1):
		return self.__class__(self.__content.replace(old, new, maxsplit))

	def rjust(self, width):
		return self.__class__(self.__content.rjust(width))

	def rstrip(self):
		return self.__class__(self.__content.rstrip())

	def rfind(self, sub, start=0, end=sys.maxint):
		return self.data.rfind(sub, start, end)

	def rindex(self, sub, start=0, end=sys.maxint):
		return self.data.rindex(sub, start, end)

	def split(self, sep=None, maxsplit=-1):
		return Frag(self.__content.split(sep, maxsplit))

	def splitlines(self, keepends=0):
		return Frag(self.__content.splitlines(keepends))

	def startswith(self, prefix, start=0, end=sys.maxint):
		return self.__content.startswith(prefix, start, end)

	def strip(self):
		return self.__class__(self.__content.strip())

	def swapcase(self):
		return self.__class__(self.__content.swapcase())

	def title(self):
		return self.__class__(self.__content.title())

	def translate(self, table):
		return self.__class__(self.__content.translate(table))

	def upper(self):
		return self.__class__(self.__content.upper())

class Text(CharacterData):
	"""
	<par>text node. The characters <markup>&lt;</markup>, <markup>&gt;</markup>, <markup>&amp;</markup>
	(and <markup>"</markup> inside attributes) will be <z>escaped</z> with the
	appropriate character entities when this node is published.</par>
	"""

	def convert(self, converter):
		return self

	def clone(self):
		return self

	def __unicode__(self):
		return self.content

	def publish(self, publisher):
		publisher.publishText(self.content)

	def present(self, presenter):
		presenter.presentText(self)

	def compact(self):
		if self.content.isspace():
			return Null
		else:
			return self

	def pretty(self, level=0, indent="\t"):
		return self

class Frag(Node, list):
	"""
	<par>A fragment contains a list of nodes and can be used for dynamically constructing content.
	The member <lit>content</lit> of an <pyref class="Element"><class>Element</class></pyref> is a <class>Frag</class>.</par>
	"""

	empty = False

	def __init__(self, *content):
		list.__init__(self)
		for child in content:
			child = ToNode(child)
			if isinstance(child, Frag):
				list.extend(self, child)
			elif child is not Null:
				list.append(self, child)

	def _str(cls, fullname=True, xmlname=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen(), presenters.strSlash())
		cls._strbase(presenters.strElementName, s, fullname=fullname, xmlname=xmlname)
		if decorate:
			if cls.empty:
				s.append(presenters.strSlash())
			s.append(presenters.strBracketClose())
		return s
	_str = classmethod(_str)

	def _create(self):
		"""
		<par>internal helper that is used to create an empty clone of <self/>.
		This is overwritten by <pyref class="Attr"><class>Attr</class></pyref>
		to insure that attributes don't get initialized with the default
		value when used in various methods that create new attributes.</par>
		"""
		return self.__class__()

	def clear(self):
		"""
		makes <self/> empty.
		"""
		del self[:]

	def convert(self, converter):
		node = self._create()
		for child in self:
			convertedchild = child.convert(converter)
			assert isinstance(convertedchild, Node), "the convert method returned the illegal object %r (type %r) when converting %r" % (convertedchild, type(convertedchild), self)
			node.append(convertedchild)
		return self._decorateNode(node)

	def clone(self):
		node = self._create()
		list.extend(node, [ child.clone() for child in self ])
		return self._decorateNode(node)

	def present(self, presenter):
		presenter.presentFrag(self)

	def __unicode__(self):
		return u"".join([ unicode(child) for child in self ])

	def __eq__(self, other):
		return self.__class__ is other.__class__ and list.__eq__(self, other)

	def publish(self, publisher):
		for child in self:
			child.publish(publisher)

	def __getitem__(self, index):
		"""
		<par>Return the <arg>index</arg>'th node for the content of the fragment.
		If <arg>index</arg> is a list <method>__getitem__</method> will work
		recursively. If <arg>index</arg> is an empty list, <self/> will be returned.</par>
		"""
		if isinstance(index, (int, long)):
			return list.__getitem__(self, index)
		elif isinstance(index, list):
			node = self
			for subindex in index:
				node = node[subindex]
			return node
		else:
			raise TypeError("index must be int, long or list not %s" % type(index).__name__)

	def __setitem__(self, index, value):
		"""
		<par>Allows you to replace the <arg>index</arg>'th content node of the fragment
		with the new value <arg>value</arg> (which will be converted to a node).
		If  <arg>index</arg> is a list <method>__setitem__</method> will be applied
		to the innermost index after traversing the rest of <arg>index</arg> recursively.
		If <arg>index</arg> is an empty list, the call will be ignored.</par>
		"""
		value = Frag(value)
		try:
			if index==-1:
				l = len(self)
				list.__setslice__(self, l-1, l, value)
			else:
				list.__setslice__(self, index, index+1, value)
		except TypeError: # assume index is a list
			if len(index):
				node = self
				for subindex in index[:-1]:
					node = node[subindex]
				index = index[-1]
				if index==-1:
					list.__setslice__(self, index, len(self), value)
				else:
					list.__setslice__(self, index, index+1, value)

	def __delitem__(self, index):
		"""
		<par>Remove the <arg>index</arg>'th content node from the fragment.
		If <arg>index</arg> is a list, the innermost index will be deleted,
		after traversing the rest of <arg>index</arg> recursively.
		If <arg>index</arg> is an empty list the call will be ignored.</par>
		"""
		try:
			list.__delitem__(self, index)
		except TypeError: # assume index is a list
			if len(index):
				node = self
				for subindex in index[:-1]:
					node = node[subindex]
				del node[index[-1]]

	def __getslice__(self, index1, index2):
		"""
		returns a slice of the content of the fragment
		"""
		node = self._create()
		list.extend(node, list.__getslice__(self, index1, index2))
		return node

	def __setslice__(self, index1, index2, sequence):
		"""
		replaces a slice of the content of the fragment
		"""
		list.__setslice__(self, index1, index2, Frag(*sequence))

	# no need to implement __delslice__

	def __mul__(self, factor):
		"""
		returns a <pyref class="Frag"><class>Frag</class></pyref> with <arg>factor</arg> times
		the content of <self/>. Note that no copies of the content will be generated, so
		this is a <z>shallow <method>__mul__</method></z>.
		"""
		node = self._create()
		list.extend(node, list.__mul__(self, factor))
		return node

	def __rmul__(self, factor):
		"""
		returns a <pyref class="Frag"><class>Frag</class></pyref> with <arg>factor</arg> times
		the content of <self/>.
		"""
		node = self._create()
		list.extend(node, list.__mul__(factor, self))
		return node

	def __nonzero__(self):
		"""
		<par>return whether this fragment is not empty.</par>
		"""
		return len(self) != 0

	# no need to implement __len__

	def append(self, *others):
		"""
		<par>append all items in <arg>others</arg> to <self/>.</par>
		"""
		for other in others:
			other = ToNode(other)
			if isinstance(other, Frag):
				list.extend(self, other)
			elif other is not Null:
				list.append(self, other)

	def insert(self, index, *others):
		"""
		<par>inserts all items in <arg>others</arg> at the position <arg>index</arg>.
		(this is the same as <lit><self/>[<arg>index</arg>:<arg>index</arg>] = <arg>others</arg></lit>)
		"""
		other = Frag(*others)
		list.__setslice__(self, index, index, other)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		for child in self:
			if child._matches(type, subtype, attrs, test):
				node.append(child)
			if searchchildren:
				node.append(child.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def compact(self):
		node = self._create()
		for child in self:
			compactedchild = child.compact()
			assert isinstance(compactedchild, Node), "the compact method returned the illegal object %r (type %r) when compacting %r" % (compactedchild, type(compactedchild), child)
			if compactedchild is not Null:
				list.append(node, compactedchild)
		return self._decorateNode(node)

	def withSep(self, separator, clone=0):
		"""
		<par>return a version of <self/> with a separator node between the nodes of <self/>.</par>

		<par>if <lit><arg>clone</arg>==0</lit> one node will be inserted several times,
		if <lit><arg>clone</arg>==1</lit> clones of this node will be used.</par>
		"""
		node = self._create()
		newseparator = ToNode(separator)
		for child in self:
			if len(node):
				node.append(newseparator)
				if clone:
					newseparator = newseparator.clone()
			node.append(child)
		return node

	def sorted(self, compare=lambda node1, node2: cmp(unicode(node1), unicode(node2))):
		"""
		<par>returns a sorted version of the <self/>. <arg>compare</arg> is
		a comparison function returning -1, 0, 1 respectively and defaults to comparing the
		<pyref class="Node" method="__unicode__"><class>__unicode__</class></pyref> value.</par>
		"""
		node = self._create()
		list.extend(node, list.__getslice__(self, 0, sys.maxint))
		list.sort(node, compare)
		return node

	def reversed(self):
		"""
		<par>returns a reversed version of the <self/>.</par>
		"""
		node = self._create()
		list.extend(node, list.__getslice__(self, 0, sys.maxint))
		list.reverse(node)
		return node

	def filtered(self, function):
		"""
		<par>returns a filtered version of the <self/>.</par>
		"""
		node = self._create()
		list.extend(node, [ child for child in self if function(child) ])
		return node

	def shuffled(self):
		"""
		<par>return a shuffled version of <self/>.</par>
		"""
		content = list.__getslice__(self, 0, sys.maxint)
		node = self._create()
		while content:
			index = random.randrange(len(content))
			list.append(node, content[index])
			del content[index]
		return node

	def mapped(self, function):
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = self._create()
			for child in self:
				node.append(child.mapped(function))
		return node

	def normalized(self):
		node = self._create()
		lasttypeOK = 0
		for child in self:
			normalizedchild = child.normalized()
			thistypeOK = isinstance(normalizedchild, Text)
			if thistypeOK and lasttypeOK:
				node[-1] += normalizedchild
			else:
				list.append(node, normalizedchild)
			lasttypeOK = thistypeOK
		return node

	def pretty(self, level=0, indent="\t"):
		node = self._create()
		i = 0
		for child in self:
			if i:
				node.append("\n")
			node.append(child.pretty(level, indent))
			i += 1
		return node

	def walk(self, before=True, after=False, attrs=False, attrbefore=True, attrafter=False):
		if before:
			yield self
		for child in self:
			for grandchild in child.walk(before, after, attrs, attrbefore, attrafter):
				yield grandchild
		if after:
			yield self

	def walkPath(self, before=True, after=False, attrs=False, attrbefore=True, attrafter=False):
		if before:
			yield [self]
		for child in self:
			for grandchildPath in child.walkpath(before, after, attrs, attrbefore, attrafter):
				yield [self] + grandchildPath
		if after:
			yield [self]

class Comment(CharacterData):
	"""
	a comment node
	"""

	def convert(self, converter):
		return self

	def clone(self):
		return self

	compact = clone

	def __unicode__(self):
		return u""

	def present(self, presenter):
		presenter.presentComment(self)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		if self.content.find(u"--")!=-1 or self.content[-1:]==u"-":
			raise errors.IllegalCommentContentError(self)
		publisher.publish(u"<!--")
		publisher.publish(self.content)
		publisher.publish(u"-->")

class DocType(CharacterData):
	"""
	a document type node
	"""

	def convert(self, converter):
		return self

	def clone(self):
		return self

	compact = clone

	def present(self, presenter):
		presenter.presentDocType(self)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		publisher.publish(u"<!DOCTYPE ")
		publisher.publish(self.content)
		publisher.publish(u">")

	def __unicode__(self):
		return u""

class ProcInst(CharacterData):
	"""
	<par>Class for processing instruction. This class is abstract.</par>

	<par>Processing instruction with the target <lit>xml</lit> will be
	handled by the derived class <pyref module="ll.xist.ns.xml" class="XML"><class>XML</class></pyref>.
	All other processing instructions will be handled
	by other classes derived from <class>ProcInst</class>.</par>
	"""

	# we don't need a constructor, because we don't have to store the target,
	# because the target is our classname (or the class attribute name)

	class __metaclass__(CharacterData.__metaclass__):
		def __repr__(self):
			return "<procinst class %s/%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def _registerns(cls, ns):
		if cls.xmlns:
			del cls.xmlns.procinstsByName[cls.xmlname]
		cls.xmlns = None
		if ns:
			ns.procinstsByName[cls.xmlname] = cls
			cls.xmlns = ns
	_registerns = classmethod(_registerns)

	def _str(cls, fullname=True, xmlname=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen(), presenters.strQuestion())
		cls._strbase(presenters.strProcInstTarget, s, fullname=fullname, xmlname=xmlname)
		if decorate:
			s.append(presenters.strQuestion(), presenters.strBracketClose())
		return s
	_str = classmethod(_str)

	def convert(self, converter):
		return self

	def clone(self):
		return self

	compact = clone

	def present(self, presenter):
		presenter.presentProcInst(self)

	def needsxmlns(self, publisher=None):
		if publisher is not None:
			return publisher.procinstmode
		return 0
	needsxmlns = classmethod(needsxmlns)

	def xmlprefix(cls, publisher=None):
		if cls.xmlns is None:
			return None
		else:
			if publisher is None:
				return cls.xmlns.xmlprefix
			else:
				return publisher.prefixes.procinstprefix4ns(cls.xmlns)[0]
	xmlprefix = classmethod(xmlprefix)

	def publish(self, publisher):
		if self.content.find(u"?>")!=-1:
			raise errors.IllegalProcInstFormatError(self)
		publisher.publish(u"<?")
		self._publishName(publisher)
		publisher.publish(u" ")
		publisher.publish(self.content)
		publisher.publish(u"?>")

	def __unicode__(self):
		return u""

class Null(CharacterData):
	"""
	node that does not contain anything.
	"""

	def _str(cls, fullname=True, xmlname=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen())
		cls._strbase(presenters.strElementName, s, fullname=fullname, xmlname=xmlname)
		if decorate:
			s.append(
				presenters.strSlash(),
				presenters.strBracketClose()
			)
		return s
	_str = classmethod(_str)

	def convert(self, converter):
		return self

	def clone(self):
		pass

	compact = clone

	def publish(self, publisher):
		pass

	def present(self, presenter):
		presenter.presentNull(self)

	def pretty(self, level=0):
		return self

Null = Null() # Singleton, the Python way

class Attr(Frag):
	r"""
	<par>Base classes of all attribute classes.</par>

	<par>The content of an attribute may be any other XSC node. This is different from
	a normal &dom;, where only text and character references are allowed. The reason for
	this is to allow dynamic content (implemented as elements or processing instructions)
	to be put into attributes.</par>

	<par>Of course, this dynamic content when finally converted to &html; will normally result in
	a fragment consisting only of text and character references. But note that it is allowed
	to have elements and processing instructions inside of attributes even when publishing.
	Processing instructions will be published as is and for elements their content will be
	published.</par>
	<example title="Elements inside attributes">
	<programlisting>
	&gt;&gt;&gt; from ll.xist.ns import html
	&gt;&gt;&gt; node = html.img( \
	...    src="eggs.gif", \
	...    alt=html.abbr( \
	...       "EGGS", \
	...       title="Extensible Graphics Generation System", \
	...       lang="en" \
	...    ) \
	... )
	&gt;&gt;&gt; print node.asBytes()
	&lt;img alt="EGGS" src="eggs.gif" /&gt;
	</programlisting>
	</example>
	"""
	class __metaclass__(Frag.__metaclass__):
		def __new__(cls, name, bases, dict):
			# can be overwritten in subclasses, to specify that this attributes is required
			dict["required"] = bool(dict.get("required", False))
			# convert the default to a Frag
			dict["default"] = Frag(dict.get("default", None))
			# convert the entries in values to unicode
			if dict.has_key("values"):
				dict["values"] = tuple([unicode(entry) for entry in dict["values"]])
			else:
				dict["values"] = None
			return Frag.__metaclass__.__new__(cls, name, bases, dict)
		def __repr__(self):
			return "<attribute class %s/%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def __init__(self, *content):
		# if the constructor has been called without arguments, use the default
		if not content:
			content = self.__class__.default.clone()
		super(Attr, self).__init__(*content)

	def _create(self):
		node = super(Attr, self)._create()
		node.clear()
		return node

	def isfancy(self):
		"""
		<par>Return whether <self/> contains nodes
		other than <pyref class="Text"><class>Text</class></pyref> or
		<pyref class="CharRef"><class>CharRef</class></pyref>.</par>
		"""
		for child in self:
			if not isinstance(child, (Text, CharRef)):
				return True
		return False

	def _str(cls, fullname=True, xmlname=True, decorate=True):
		s = ansistyle.Text()
		cls._strbase(presenters.strAttrName, s, fullname=fullname, xmlname=xmlname)
		return s
	_str = classmethod(_str)

	def present(self, presenter):
		presenter.presentAttr(self)

	def checkValid(self):
		"""
		<par>Check whether <self/> has an allowed value, i.e. one
		that is specified in the class attribute <lit>values</lit>.
		If the value is not allowed a warning will be issued through
		the Python warning framework.</par>
		<par>If <self/> is <pyref method="isfancy">isfancy</pyref>,
		no check will be done.</par>
		"""
		values = self.__class__.values
		if len(self) and isinstance(values, tuple) and not self.isfancy():
			value = unicode(self)
			if value not in values:
				errors.warn(errors.IllegalAttrValueWarning(self))

	def parsed(self, handler):
		self.checkValid()

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		self.checkValid()
		publisher.inAttr += 1
		publisher.pushTextFilter(helpers.escapeAttr)
		Frag.publish(self, publisher)
		publisher.popTextFilter()
		publisher.inAttr -= 1

	def pretty(self, level=0, indent="\t"):
		return self.clone()

class TextAttr(Attr):
	"""
	<par>Attribute class that is used for normal text attributes.</par>
	"""

class IDAttr(Attr):
	"""
	<par>Attribute used for ids.</par>
	"""

class NumberAttr(Attr):
	"""
	<par>Attribute class that is used for normal number attributes.</par>
	"""

class IntAttr(NumberAttr):
	"""
	<par>Attribute class that is used for normal integer attributes.</par>
	"""

class FloatAttr(NumberAttr):
	"""
	<par>Attribute class that is used for normal float attributes.</par>
	"""

class BoolAttr(Attr):
	"""
	<par>Attribute class that is used for boolean attributes.</par>
	"""

class ColorAttr(Attr):
	"""
	<par>Attribute class that is used for a color attributes.</par>
	"""

class StyleAttr(Attr):
	"""
	<par>Attribute class that is used for &css; style attributes.</par>
	"""

	def parsed(self, handler):
		if not self.isfancy():
			value = cssparsers.parseString(unicode(self), handler=cssparsers.ParseHandler(), base=handler.base)
			self[:] = (value, )

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		if not self.isfancy():
			value = cssparsers.parseString(unicode(self), handler=cssparsers.PublishHandler(), base=publisher.base)
			new = Attr(value)
			new.publish(publisher)
		else:
			super(StyleAttr, self).publish(publisher)

	def urls(self):
		"""
		<par>Return a list of all the <pyref module="ll.url" class="URL"><class>URL</class></pyref>s
		found in the style attribute.</par>
		"""
		source = sources.StringInputSource(unicode(self))
		handler = cssparsers.CollectHandler()
		handler.parse(source, ignoreCharset=1)
		urls = handler.urls
		handler.close()
		return urls

class URLAttr(Attr):
	"""
	Attribute class that is used for URLs. See RFC 2396.
	"""

	def parsed(self, handler):
		self[:] = utils.replaceInitialURL(self, lambda u: handler.base/u)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		new = utils.replaceInitialURL(self, lambda u: u.relative(publisher.base))
		publisher.inAttr = 1
		new.publish(publisher)
		publisher.inAttr = 0

	def asURL(self):
		return url.URL(Attr.__unicode__(self))

	def __unicode__(self):
		return self.asURL().url

	def forInput(self, root=None):
		u = self.asURL()
		if u.scheme == "root":
			u.scheme = None
		u = url.URL(root)/u
		return u

	def imagesize(self, root=None):
		"""
		returns the size of an image as a tuple or None if the image shouldn't be read
		"""
		return self.openread(root).imagesize

	def contentlength(self, root=None):
		"""
		returns the size of a file in bytes or None if the file shouldn't be read
		"""
		return self.openread(root).contentlength

	def lastmodified(self, root=None):
		"""
		returns the timestamp for the last modification to the file
		"""
		return self.openread(root).lastmodified

	def openread(self, root=None):
		"""
		opens the URL for reading
		"""
		return self.forInput(root).openread()

	def openwrite(self, root=None):
		"""
		opens the URL for writing
		"""
		return self.forInput(root).openwrite()

class Null(CharacterData):
	"""
	node that does not contain anything.
	"""

	def convert(self, converter):
		return self

	def clone(self):
		pass

	compact = clone

	def publish(self, publisher):
		pass

	def present(self, presenter):
		presenter.presentNull(self)

	def pretty(self, level=0):
		return self

Null = Null() # Singleton, the Python way

class Attrs(Node, dict):
	"""
	<par>An attribute map. Allowed entries are specified through nested subclasses
	of <pyref class="Attr"><class>Attr</class></pyref></par>
	"""

	class __metaclass__(Node.__metaclass__):
		def __new__(cls, name, bases, dict):
			handlersByPyName = {}
			handlersByXMLName = {}
			res = Node.__metaclass__.__new__(cls, name, bases, dict)
			for key in dir(res):
				value = getattr(res, key)
				if isinstance(value, type) and issubclass(value, Attr):
					handlersByPyName[value.__name__] = value
					handlersByXMLName[value.xmlname] = value
			res._handlersByPyName = handlersByPyName
			res._handlersByXMLName = handlersByXMLName
			return res

	def __init__(self, content=None, **attrs):
		dict.__init__(self)
		if content is not None:
			for (attrname, attrvalue) in content.items():
				self[attrname] = attrvalue
		for (attrname, attrvalue) in attrs.items():
			self[attrname] = attrvalue

	def __eq__(self, other):
		return self.__class__ is other.__class__ and dict.__eq__(self, other)

	def _str(cls, fullname=True, xmlname=True, decorate=True):
		s = ansistyle.Text()
		cls._strbase(presenters.strAttrsName, s, fullname=fullname, xmlname=xmlname)
		return s
	_str = classmethod(_str)

	def _create(self):
		node = self.__class__() # "virtual" constructor
		node.clear()
		return node

	def clear(self):
		"""
		makes <self/> empty. (This also removes default attributes)
		"""
		for (key, value) in self.items():
			value.clear()

	def clone(self):
		node = self._create()
		for (key, value) in dict.items(self):
			dict.__setitem__(node, key, value.clone())
		return node

	def convert(self, converter):
		node = self._create()
		for (attrname, attrvalue) in self.items():
			convertedattr = attrvalue.convert(converter)
			assert isinstance(convertedattr, Node), "the convert method returned the illegal object %r (type %r) when converting the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
			node[attrname] = convertedattr
		return node

	def compact(self):
		node = self._create()
		for (attrname, attrvalue) in self.items():
			convertedattr = attrvalue.compact()
			assert isinstance(convertedattr, Node), "the compact method returned the illegal object %r (type %r) when compacting the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
			node[attrname] = convertedattr
		return node

	def normalized(self):
		node = self._create()
		for (attrname, attrvalue) in self.items():
			convertedattr = attrvalue.normalized()
			assert isinstance(convertedattr, Node), "the normalized method returned the illegal object %r (type %r) when normalizing the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
			node[attrname] = convertedattr
		return node

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		if searchattrs:
			for attrvalue in self.values():
				if len(attrvalue):
					node.append(attrvalue.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def present(self, presenter):
		presenter.presentAttrs(self)

	def parsed(self, handler):
		attrs = [key for (key, value) in self.alloweditems() if value.required]
		for attrname in self.keys():
			if isinstance(attrname, tuple): # global attribute?
				try:
					attrs.remove(attrname)
				except KeyError:
					pass
		if attrs:
			errors.warn(errors.RequiredAttrMissingWarning(self, attrs))

	def publish(self, publisher):
		attrs = [key for (key, value) in self.alloweditems() if value.required]
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		for (attrname, attrvalue) in dict.items(self):
			if len(attrvalue):
				publisher.publish(u" ")
				if isinstance(attrname, tuple): # global attribute?
					publisher.publish(publisher.prefixes.elementprefix4ns(attrname[0])[0])
					publisher.publish(u":")
				else:
					try:
						attrs.remove(attrname)
					except ValueError:
						pass
				publisher.publish(attrvalue.xmlname) # publish the XML name, not the Python name
				if isinstance(attrvalue, BoolAttr):
					if publisher.xhtml>0:
						publisher.publish(u"=\"")
						publisher.publish(attrname)
						publisher.publish(u"\"")
				else:
					publisher.publish(u"=\"")
					attrvalue.publish(publisher)
					publisher.publish(u"\"")
		if attrs:
			errors.warn(errors.RequiredAttrMissingWarning(self, attrs))

	def __unicode__(self):
		return u""

	def isallowed(cls, key):
		return cls._handlersByPyName.has_key(key)
	isallowed = classmethod(isallowed)

	def _attrClass(cls, key):
		try:
			return cls._handlersByPyName[key]
		except KeyError:
			raise errors.IllegalAttrError(cls, key)
	_attrClass = classmethod(_attrClass)

	def __getitem__(self, key):
		# we're returning the packed attribute here, because otherwise there would be no possibility to get an expanded URL
		try:
			attr = dict.__getitem__(self, key)
		except KeyError: # if the attribute is not there generate a new one (containing the default value)
			attr = self._attrClass(key)()
			dict.__setitem__(self, key, attr)
		return attr

	def __setitem__(self, key, value):
		# values are constructed via the attribute classes specified as nested classes, which does the conversion
		attr = self._attrClass(key)(value)
		dict.__setitem__(self, key, attr) # put the attribute in our dict

	def __delitem__(self, key):
		try:
			dict.__delitem__(self, key)
		except KeyError: # ignore non-existing attributes (but only if the name is allowed)
			attrclass = self._attrClass(key)

	def has(self, key):
		try:
			attr = dict.__getitem__(self, key)
		except KeyError:
			attr = self._attrClass(key).default
		return len(attr)>0

	def get(self, key, default=None):
		attr = self[key]
		if attr:
			return attr
		else:
			return self._attrClass(key)(default) # pack the attribute into an attribute object

	def setdefault(self, key, default=None):
		attr = self[key]
		if not attr:
			attr = self._attrClass(key)(default) # pack the attribute into an attribute object
			dict.__setitem__(self, key, attr)
		return attr

	def copydefaults(self, fromMapping):
		"""
		Sets attributes that are not set in <self/> to the default
		values taken from the <arg>fromMapping</arg> mapping.
		"""

		for (attrname, attrvalue) in fromMapping.items():
			if not self.has(attrname):
				self[attrname] = attrvalue

	def iterallowedkeys(cls):
		return cls._handlersByPyName.iterkeys()
	iterallowedkeys = classmethod(iterallowedkeys)

	def allowedkeys(cls):
		"""
		<par>return a list of allowed keys (i.e. attribute names)</par>
		"""
		return cls._handlersByPyName.keys()
	allowedkeys = classmethod(allowedkeys)

	def iterallowedvalues(cls):
		return cls._handlersByPyName.itervalues()
	iterallowedvalues = classmethod(iterallowedvalues)

	def allowedvalues(cls):
		"""
		<par>return a list of values for the allowed values.</par>
		"""
		return cls._handlersByPyName.values()
	allowedvalues = classmethod(allowedvalues)

	def iteralloweditems(cls):
		return cls._handlersByPyName.iteritems()
	iteralloweditems = classmethod(iteralloweditems)

	def alloweditems(cls):
		return cls._handlersByPyName.items()
	alloweditems = classmethod(alloweditems)

	def __iter__(self):
		return iter(self.keys())

	def __len__(self):
		return len(self.keys())

	def iterkeys(self):
		return iter(self.keys())

	def keys(self):
		keys = {} # use a dict to avoid duplicates
		# fetch the existing attribute keys
		for (key, value) in dict.items(self):
			if len(value):
				keys[key] = None
		# fetch the keys of attributes with a default value (if it hasn't been overwritten)
		for (key, value) in self.alloweditems():
			if value.default and not dict.has_key(self, key):
				keys[key] = None
		return keys.keys()

	def itervalues(self):
		return iter(self.values())

	def values(self):
		values = []
		for key in self.keys():
			values.append(self[key])
		return values

	def iterItems(self):
		return iter(self.items())

	def items(self):
		items = []
		for key in self.keys():
			items.append((key, self[key]))
		return items

	def without(self, nameseq):
		"""
		<par>Return a copy of <self/> where all the attributes in <arg>nameseq</arg> are
		removed. A name in <arg>nameseq</arg> that is not in <self/> will not raise
		an exception (if it is allowed).</par>
		"""
		node = self._create()
		for (key, value) in self.items():
			if key not in nameseq:
				node[key] = value
			else:
				# make sure to hide attributes that have default values
				attrclass = self._attrClass(key)
				if attrclass.default:
					node[key] = None
		return node

_Attrs = Attrs

class Element(Node):
	"""
	<par>This class represents &xml;/&xist; elements. All elements
	implemented by the user must be derived from this class.</par>

	<par>If you not only want to construct a &dom; tree via a Python script
	(by directly instantiating these classes), but to read an &xml; file
	you must register the element class with the parser, this can be done
	by creating <pyref class="Namespace"><class>Namespace</class></pyref>
	objects.</par>

	<par>Every element class should have two class variables:
	<lit>empty</lit>: this is either <lit>0</lit> or <lit>1</lit>
	and specifies whether the element type is allowed to have content
	or not. Note that the parser does not use this as some sort of
	static DTD, i.e. you still must write your empty tags
	like this: <markup>&lt;foo/&gt;</markup>.</par>

	<par><lit>Attrs</lit>, which is a class derived from
	<pyref class="Element.Attrs"><class>Element.Attrs</class></pyref>
	and should define all attributes as classes nested inside this
	<class>Attrs</class> class.</par>
	"""

	empty = True # False => element with content; True => element without content

	class __metaclass__(Node.__metaclass__):
		def __new__(cls, name, bases, dict):
			if dict.has_key("name") and isinstance(dict["name"], (str, unicode)):
				errors.warn(DeprecationWarning("name is deprecated, use xmlname instead"))
				dict["xmlname"] = dict["name"]
				del dict["name"]
			if dict.has_key("attrHandlers"):
				errors.warn(DeprecationWarning("attrHandlers is deprecated, use a nested Attrs class instead"))
				# make it work anyway
				import new
				if dict.has_key("Attrs"):
					base = dict["Attrs"]
				else:
					base = Element.Attrs
				newdict = {}
				for (key, value) in dict["attrHandlers"].items():
					newdict[key] = new.classobj(key, (value, ), {})
				dict["Attrs"] = new.classobj("Attrs", (base, ), newdict)
			cls = Node.__metaclass__.__new__(cls, name, bases, dict)
			# make the attrHandlers dictionary available for derived classes that want to use it
			attrHandlers = {}
			for key in dir(cls.Attrs):
				value = getattr(cls.Attrs, key)
				if isinstance(value, type) and issubclass(value, Attr):
					attrHandlers[key] = value
			cls.attrHandlers = attrHandlers
			return cls
		def __repr__(self):
			return "<element class %s/%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))


	class Attrs(Attrs):
		def _attrClass(cls, key):
			if isinstance(key, tuple):
				key = (getNS(key[0]), key[1])
				return key[0].Attrs._attrClass(key[1])
			else:
				# FIXME reimplemented here, because super does not work
				try:
					return cls._handlersByPyName[key]
				except KeyError:
					raise errors.IllegalAttrError(cls, key)
		_attrClass = classmethod(_attrClass)

		def has(self, key):
			if isinstance(key, tuple):
				key = (getNS(key[0]), key[1])
			return _Attrs.has(self, key)

		def __setitem__(self, key, value):
			if isinstance(key, tuple):
				key = (getNS(key[0]), key[1])
			_Attrs.__setitem__(self, key, value)

		def __getitem__(self, key):
			if isinstance(key, tuple):
				key = (getNS(key[0]), key[1])
			return _Attrs.__getitem__(self, key)

		def __delitem__(self, key):
			if isinstance(key, tuple):
				key = (getNS(key[0]), key[1])
			return _Attrs.__delitem__(self, key)

		def without(self, nameseq):
			"""
			<par>Return a copy of <self/> where all the attributes in <arg>nameseq</arg> are
			removed. A name in <arg>nameseq</arg> that is not in <self/> will not raise
			an exception (if it is allowed).</par>
			<par>Names can be strings (<class>str</class> and <class>unicode</class>),
			(namespace/module, string) tuples (for global attributes), namespaces/modules
			for removing all global attributes from this namespace and <lit>None</lit>
			for removing all global attributes.</par>
			"""
			node = self._create()
			localnames = []
			globalnames = []
			namespaces = []
			allglobals = 0
			for name in nameseq:
				if isinstance(name, (str, unicode)):
					localnames.append(name)
				elif isinstance(name, types.ModuleType):
					namespaces.append(name.xmlns)
				elif isinstance(name, Namespace):
					namespaces.append(name)
				elif name is None:
					allglobals = 1
				else:
					globalnames.append((getNS(name[0]), name[1]))
			for (key, value) in self.items():
				if isinstance(key, (str, unicode)):
					if key not in localnames:
						node[key] = value
						continue
				else:
					if not allglobals and key not in globalnames and key[0] not in namespaces:
						node[key] = value
						continue
				# must be removed => make sure to hide attributes that have default values
				attrclass = self._attrClass(key)
				if attrclass.default:
					node[key] = None
			return node

	def __init__(self, *content, **attrs):
		"""
		<par>Create a new <class>Element</class> instance.</par>
		
		<par>positional arguments are treated as content nodes.
		keyword arguments and dictionaries are treated as attributes.</par>
		"""
		self.attrs = self.Attrs()
		newcontent = []
		for child in content:
			if isinstance(child, dict):
				for (attrname, attrvalue) in child.items():
					self.attrs[attrname] = attrvalue
			else:
				newcontent.append(child)
		self.content = Frag(*newcontent)
		for (attrname, attrvalue) in attrs.items():
			self.attrs[attrname] = attrvalue

	def _registerns(cls, ns):
		if cls is not Element:
			if cls.xmlns:
				del cls.xmlns.elementsByName[cls.xmlname]
			cls.xmlns = None
			if ns:
				ns.elementsByName[cls.xmlname] = cls
				cls.xmlns = ns
	_registerns = classmethod(_registerns)

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.content==other.content and self.attrs==other.attrs

	def _str(cls, fullname=True, xmlname=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen())
		cls._strbase(presenters.strElementName, s, fullname=fullname, xmlname=xmlname)
		if decorate:
			if cls.empty:
				s.append(presenters.strSlash())
			s.append(presenters.strBracketClose())
		return s
	_str = classmethod(_str)

	def checkValid(self):
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def append(self, *items):
		"""
		<par>appends to content (see <pyref class="Frag" method="append"><method>Frag.append</method></pyref>
		for more info)</par>
		"""

		self.content.append(*items)
		self.checkValid()

	def insert(self, index, *items):
		"""
		<par>inserts into the content (see <pyref class="Frag" method="insert"><method>Frag.insert</method></pyref>
		for more info)</par>
		"""
		self.content.insert(index, *items)
		self.checkValid()

	def convert(self, converter):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.convert(converter)
		node.attrs = self.attrs.convert(converter)
		return self._decorateNode(node)

	def clone(self):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.clone() # this is faster than passing it in the constructor (no ToNode call)
		node.attrs = self.attrs.clone()
		return self._decorateNode(node)

	def __unicode__(self):
		return unicode(self.content)

	def _addImageSizeAttributes(self, root, imgattr, widthattr=None, heightattr=None):
		"""
		<par>add width and height attributes to the element for the image that can be found in the attribute
		<arg>imgattr</arg>. If the attributes are already there, they are taken as a formatting
		template with the size passed in as a dictionary with the keys <lit>"width"</lit> and <lit>"height"</lit>,
		i.e. you could make your image twice as wide with <lit>width="%(width)d*2"</lit>.</par>

		<par>Passing <lit>None</lit> as <arg>widthattr</arg> or
		<arg>heightattr</arg> will prevent the respective attributes
		from being modified in any way.</par>
		"""

		if self.hasAttr(imgattr):
			attr = self[imgattr]
			try:
				size = attr.imagesize(root)
			except IOError, exc:
				errors.warn(errors.FileNotFoundWarning("can't read image", unicode(attr), exc))
			else:
				sizedict = {"width": size[0], "height": size[1]}
				for attr in (heightattr, widthattr):
					if attr is not None: # do something to the width/height
						if self.hasAttr(attr):
							try:
								s = unicode(self[attr]) % sizedict
								s = unicode(eval(s))
								self[attr] = s
							except TypeError: # ignore "not all argument converted"
								pass
							except Exception, exc:
								errors.warn(errors.ImageSizeFormatWarning(self, self[attr], exc))
								del self[attr]
						else:
							self[attr] = size[attr==heightattr]

	def present(self, presenter):
		presenter.presentElement(self)

	def needsxmlns(self, publisher=None):
		if publisher is not None:
			return publisher.elementmode
		return 1
	needsxmlns = classmethod(needsxmlns)

	def xmlprefix(cls, publisher=None):
		if cls.xmlns is None:
			return None
		else:
			if publisher is None:
				return cls.xmlns.xmlprefix
			else:
				return publisher.prefixes.elementprefix4ns(cls.xmlns)[0]
	xmlprefix = classmethod(xmlprefix)

	def publish(self, publisher):
		if publisher.inAttr:
			# publish the content only, when we are inside an attribute
			# this works much like using the plain string value, but
			# even works with processing instructions, or what the Entity &xist; returns
			self.content.publish(publisher)
		else:
			publisher.publish(u"<")
			self._publishName(publisher)
			# we're the first element to be published, so we have to create the xmlns attributes
			if hasattr(publisher, "publishxmlns"):
				for ((nsprefix, ns), (mode, prefix)) in publisher.prefixes2use.iteritems():
					if mode==2:
						publisher.publish(u" ")
						publisher.publish(nsprefix)
						if prefix is not None:
							publisher.publish(u":")
							publisher.publish(prefix)
						publisher.publish(u"=\"")
						publisher.publish(ns.xmlurl)
						publisher.publish(u"\"")
				# delete the note, so the next element won't create the attributes again
				del publisher.publishxmlns
			self.attrs.publish(publisher)
			if len(self):
				if self.empty:
					raise errors.EmptyElementWithContentError(self)
				publisher.publish(u">")
				self.content.publish(publisher)
				publisher.publish(u"</")
				self._publishName(publisher)
				publisher.publish(u">")
			else:
				if publisher.xhtml in (0, 1):
					if self.empty:
						if publisher.xhtml==1:
							publisher.publish(u" /")
						publisher.publish(u">")
					else:
						publisher.publish(u"></")
						self._publishName(publisher)
						publisher.publish(u">")
				elif publisher.xhtml == 2:
					publisher.publish(u"/>")

	def __getitem__(self, index):
		"""
		returns an attribute or one of the content nodes depending on whether
		an 8bit or unicode string (i.e. attribute name) or a number or list
		(i.e. content node index) is passed in.
		"""
		if isinstance(index, (int, long, list)):
			return self.content[index]
		else:
			return self.attrs[index]

	def __setitem__(self, index, value):
		"""
		<par>sets an attribute or one of the content nodes depending on whether
		an 8bit or unicode string (i.e. attribute name) or a number or list (i.e.
		content node index) is passed in.</par>
		"""
		if isinstance(index, (int, long, list)):
			self.content[index] = value
		else:
			self.attrs[index] = value

	def __delitem__(self, index):
		"""
		removes an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number or list (i.e. content node index) is passed in.
		"""
		if isinstance(index, (int, long, list)):
			del self.content[index]
		else:
			del self.attrs[index]

	def hasAttr(self, attrname):
		return self.hasattr(attrname)

	def hasattr(self, attrname):
		"""
		<par>return whether <self/> has an attribute named <arg>attr</arg>.</par>
		"""
		return self.attrs.has(attrname)

	def isallowedattr(cls, attrname):
		"""
		<par>return whether the attribute named <arg>attrname</arg> is allowed for <self/>.</par>
		"""
		return self.attrs.isallowed(attrname)
	isallowedattr = classmethod(isallowedattr)

	def getAttr(self, attrname, default=None):
		return self.getattr(attrname, default)

	def getattr(self, attrname, default=None):
		"""
		<par>works like the dictionary method <method>get</method>,
		it returns the attribute with the name <arg>attrname</arg>,
		or if <self/> has no such attribute, <arg>default</arg>
		(after converting it to a node and wrapping it into the appropriate
		attribute node.)</par>
		"""
		return self.attrs.get(attrname, default)

	def setDefaultAttr(self, attrname, default=None):
		return self.setdefaultattr(attrname, default)

	def setdefaultattr(self, attrname, default=None):
		"""
		<par>works like the dictionary method <method>setdefault</method>,
		it returns the attribute with the name <arg>attrname</arg>,
		or if <self/> has no such attribute, <arg>default</arg>
		(after converting it to a node and wrapping it into the appropriate
		attribute node.). In this case <arg>default</arg> will be
		kept as the attribute value.</par>
		"""
		return self.attrs.setdefault(attrname, default)

	def attrkeys(self):
		"""
		return a list with all the attribute names of <self/>.
		"""
		return self.attrs.keys()

	def attrvalues(self):
		"""
		return a list with all the attribute values of <self/>.
		"""
		return self.attrs.values()

	def attritems(self):
		"""
		return a list with all the attribute name/value tuples of <self/>.
		"""
		return self.attrs.items()

	def iterattrkeys(self):
		"""
		return an iterator for the attribute names of <self/>.
		"""
		return self.attrs.iterkeys()

	def iterattrvalues(self):
		"""
		return an iterator for the attribute values of <self/>.
		"""
		return self.attrs.itervalues()

	def iterattritems(self):
		"""
		return an iterator for the attribute name/value tuples of <self/>.
		"""
		return self.attrs.items()

	def allowedattrkeys(cls):
		"""
		return a list with all the allowed attribute names of <self/>.
		"""
		return cls.Attrs.allowedkeys()
	allowedattrkeys = classmethod(allowedattrkeys)

	def allowedattrvalues(cls):
		"""
		return a list with all the allowed attribute values of <self/>.
		"""
		return cls.Attrs.allowedvalues()
	allowedattrvalues = classmethod(allowedattrvalues)

	def allowedattritems(cls):
		"""
		return a list with all the allowed attribute name/value tuples of <self/>.
		"""
		return cls.Attrs.alloweditems()
	allowedattritems = classmethod(allowedattritems)

	def iterallowedattrkeys(cls):
		"""
		return an iterator for the allowed attribute names of <self/>.
		"""
		return cls.Attrs.iterallowedkeys()
	iterallowedattrkeys = classmethod(iterallowedattrkeys)

	def iterallowedattrvalues(cls):
		"""
		return an iterator for the allowed attribute values of <self/>.
		"""
		return cls.Attrs.iterallowedvalues()
	iterallowedattrvalues = classmethod(iterallowedattrvalues)

	def iterallowedattritems(cls):
		"""
		return an iterator for the allowed attribute name/value tuples of <self/>.
		"""
		return cls.Attrs.iteralloweditems()
	iterallowedattritems = classmethod(iterallowedattritems)

	def __getslice__(self, index1, index2):
		"""
		returns a copy of the element that contains a slice of the content
		"""
		return self.__class__(self.content[index1:index2], self.attrs)

	def __setslice__(self, index1, index2, sequence):
		"""
		modifies a slice of the content of the element
		"""
		self.content[index1:index2] = sequence

	def __delslice__(self, index1, index2):
		"""
		removes a slice of the content of the element
		"""
		del self.content[index1:index2]

	def __nonzero__(self):
		"""
		return whether the element is not empty (this should be a little faster than defaulting to __len__)
		"""
		return self.content.__nonzero__()

	def __len__(self):
		"""
		return the number of children
		"""
		return len(self.content)

	def compact(self):
		node = self.__class__()
		node.content = self.content.compact()
		node.attrs = self.attrs.compact()
		return self._decorateNode(node)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		node.append(self.attrs.find(type, subtype, attrs, test, searchchildren, searchattrs))
		node.append(self.content.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def copyDefaultAttrs(self, fromMapping):
		"""
		<par>Sets attributes that are not set in <self/> to the default
		values taken from the <arg>fromMapping</arg> mapping.
		If <arg>fromDict</arg> is omitted, defaults are taken from
		<lit><self/>.defaults</lit>.</par>

		<par>Note that boolean attributes may savely be set to e.g. <lit>1</lit>,
		as only the fact that a boolean attribute exists matters.</par>
		"""

		self.attrs.copydefaults(fromMapping)

	def withSep(self, separator, clone=0):
		"""
		<par>returns a version of <self/> with a separator node between the child nodes of <self/>.
		for more info see <pyref class="Frag" method="withSep"><method>Frag.withSep</method></pyref>.</par>
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.withSep(separator, clone)
		return node

	def sorted(self, compare=lambda node1, node2: cmp(unicode(node1), unicode(node2))):
		"""
		returns a sorted version of <self/>.
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.sorted(compare)
		return node

	def reversed(self):
		"""
		returns a reversed version of <self/>.
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.reversed()
		return node

	def filtered(self, function):
		"""
		returns a filtered version of the <self/>.
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.filtered(function)
		return node

	def shuffled(self):
		"""
		returns a shuffled version of the <self/>.
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.shuffled()
		return node

	def mapped(self, function):
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = self.__class__(self.content.mapped(function))
			node.attrs = self.attrs.clone()
		return node

	def normalized(self):
		node = self.__class__()
		node.attrs = self.attrs.normalized()
		node.content = self.content.normalized()
		return node

	def pretty(self, level=0, indent="\t"):
		node = self.__class__(self.attrs)
		if len(self)==1 and isinstance(self[0], Text):
			node.append(self[0])
		elif len(self)==0:
			pass
		else:
			# search for mixed content
			text = 0
			nontext = 0
			for child in self:
				if isinstance(child, Text):
					text += 1
				else:
					nontext += 1
			# if mixed content, leave it alone
			if text and nontext:
				node.append(self.content.clone())
			else:
				for child in self:
					node.append("\n", child.pretty(level+1, indent))
				node.append("\n", indent*level)
		if level>0:
			node = Frag(indent*level, node)
		return node

	def walk(self, before=True, after=False, attrs=True, attrbefore=True, attrafter=False):
		if before:
			yield self
		if attrs:
			for child in self.attrs.values():
				if attrbefore:
					yield child
				for grandchild in child.walk(before, after, attrs, attrbefore, attrafter):
					yield grandchild
				if attrafter:
					yield child
		for child in self.content:
			for grandchild in child.walk(before, after, attrs, attrbefore, attrafter):
				yield grandchild
		if after:
			yield self

	def walkPath(self, before=True, after=False, attrs=False, attrbefore=True, attrafter=False):
		if before:
			yield [self]
		if attrs:
			for child in self.attrs.values():
				if attrbefore:
					yield [self] + child
				for grandchildPath in child.walkPath(before, after, attrs, attrbefore, attrafter):
					yield [self] + grandchildPath
				if attrafter:
					yield [self] + child
		for child in self.content:
			for grandchildPath in child.walkPath(before, after, attrs, attrbefore, attrafter):
				yield [self] + grandchildPath
		if after:
			yield [self]

class Entity(Node):
	"""
	<par>Class for entities. Derive your own entities from
	it and overwrite <pyref class="Node" method="convert"><method>convert</method></pyref>
	and <pyref class="Node" method="__unicode__"><method>__unicode__</method></pyref>.</par>
	"""

	class __metaclass__(Node.__metaclass__):
		def __repr__(self):
			return "<entity class %s/%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def _registerns(cls, ns):
		if cls is not Entity and cls is not CharRef:
			if cls.xmlns:
				del cls.xmlns.entitiesByName[cls.xmlname]
			cls.xmlns = None
			if ns:
				ns.entitiesByName[cls.xmlname] = cls
				cls.xmlns = ns
	_registerns = classmethod(_registerns)

	def _str(cls, fullname=True, xmlname=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strAmp())
		cls._strbase(presenters.strEntityName, s, fullname=fullname, xmlname=xmlname)
		if decorate:
			s.append(presenters.strSemi())
		return s
	_str = classmethod(_str)

	def compact(self):
		return self

	clone = compact

	def present(self, presenter):
		presenter.presentEntity(self)

	def needsxmlns(self, publisher=None):
		if publisher is not None:
			return publisher.entitymode
		return 0
	needsxmlns = classmethod(needsxmlns)

	def xmlprefix(cls, publisher=None):
		if cls.xmlns is None:
			return None
		else:
			if publisher is None:
				return cls.xmlns.xmlprefix
			else:
				return publisher.prefixes.entityprefix4ns(cls.xmlns)[0]
	xmlprefix = classmethod(xmlprefix)

	def publish(self, publisher):
		publisher.publish(u"&")
		self._publishName(publisher)
		publisher.publish(u";")

class CharRef(Entity):
	"""
	<par>A simple character reference, the codepoint is in the class attribute
	<lit>codepoint</lit>.</par>
	"""

	class __metaclass__(Entity.__metaclass__):
		def __repr__(self):
			return "<charref class %s/%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def _registerns(cls, ns):
		if cls is not CharRef:
			if cls.xmlns:
				del cls.xmlns.charrefsByName[cls.xmlname]
				cls.xmlns.charrefsByNumber[cls.codepoint].remove(cls)
			cls.xmlns = None
			if ns:
				ns.charrefsByName[cls.xmlname] = cls
				ns.charrefsByNumber.setdefault(cls.codepoint, []).append(cls)
				cls.xmlns = ns
	_registerns = classmethod(_registerns)

	def convert(self, converter):
		node = Text(unichr(self.codepoint))
		return self._decorateNode(node)

	def __unicode__(self):
		return unichr(self.codepoint)

###
###
###

class NamespaceAttrMixIn(object):
	"""
	<par>Attributes in namespaces always need a prefix and
	most of them (except those for the prefix <lit>xml</lit>),
	require that their namespace is declared. This class can
	be used as a mixin class to achieve that.</par>
	"""
	needsxmlns = 2

class Namespace(Base):
	"""
	<par>an &xml; namespace, contains the classes for the elements,
	entities and processing instructions in the namespace.</par>
	"""

	class Attrs(_Attrs):
		pass

	def __init__(self, xmlprefix, xmlurl, thing=None):
		"""
		<par>Create a new <class>Namespace</class> instance.</par>

		<par>All classes from the module the <class>Namespace</class> instance is in will be registered if
		they are derived from <pyref class="Element"><class>Element</class></pyref>, <pyref class="Entity"><class>Entity</class></pyref> or
		<pyref class="ProcInst"><class>ProcInst</class></pyref> in the following way: The class <arg>thing</arg>
		will be registered under it's class name (<lit><arg>thing</arg>.__name__</lit>).
		If you want to change this behaviour, do the following: set a class attribute
		<lit>xmlname</lit> to the name you want to be used. If you don't want
		<arg>thing</arg> to be registered at all, set the class attribute
		<lit>register</lit> to <lit>0</lit>.
		"""
		self.xmlprefix = unicode(xmlprefix)
		if xmlurl is not None: # may be None, which mean no "xmlns:..." has to be used.
			xmlurl = unicode(xmlurl)
		self.xmlurl = xmlurl
		self.elementsByName = {} # dictionary for mapping element names to classes
		self.entitiesByName = {} # dictionary for mapping entity names to classes
		self.procinstsByName = {} # dictionary for mapping processing instruction target names to classes
		self.charrefsByName = {} # dictionary for mapping character reference names to classes
		self.charrefsByNumber = {} # dictionary for mapping character reference code points to classes
		self.register(thing)
		for value in self.Attrs.allowedvalues():
			value.xmlns = self
		namespaceRegistry.register(self)

	def register(self, thing):
		"""
		<par>this function lets you register <arg>thing</arg> in the namespace.
		If <arg>thing</arg> is a class derived from <pyref class="Element"><class>Element</class></pyref>,
		<pyref class="Entity"><class>Entity</class></pyref> or <pyref class="ProcInst"><class>ProcInst</class></pyref>
		it will be registered under its class name (<lit><arg>thing</arg>.__name__</lit>). If you want
		to change this behaviour, do the following: set a class variable <lit>xmlname</lit> to
		the name you want to be used. If you don't want <arg>thing</arg> to be
		registered at all, set <lit>register</lit> to <lit>None</lit>. (This will
		still register <arg>thing</arg>, but it will not be used for parsing.)</par>

		<par>After the call <arg>thing</arg> will have two class attributes:
		<lit>xmlname</lit>, which is the name under which the class is registered and
		<lit>xmlns</lit>, which is the namespace itself (i.e. <self/>).</par>

		<par>If <arg>thing</arg> is a dictionary, every object in the dictionary
		will be registered.</par>

		<par>All other objects are ignored.</par>
		"""

		if isinstance(thing, type) and issubclass(thing, Node): # this is a Node type
			thing._registerns(self)
		elif isinstance(thing, dict):
			for key in thing.keys():
				self.register(thing[key])

	def __repr__(self):
		counts = []
		if len(self.elementsByName):
			counts.append("%d elements" % len(self.elementsByName))
		if len(self.entitiesByName):
			counts.append("%d entities" % len(self.entitiesByName))
		if len(self.procinstsByName):
			counts.append("%d procinsts" % len(self.procinstsByName))
		if len(self.charrefsByName):
			counts.append("%d charrefs" % len(self.charrefsByName))
		allowedattrs = self.Attrs.allowedkeys()
		if len(allowedattrs):
			counts.append("%d attrs" % len(allowedattrs))
		if len(counts):
			counts = " with " + ", ".join(counts)
		else:
			counts = ""
		return "<%s.%s instance xmlprefix=%r xmlurl=%r%s at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.xmlprefix, self.xmlurl, counts, id(self))

	def __eq__(self, other):
		return self.xmlprefix==other.xmlprefix and self.xmlurl==other.xmlurl

	def __ne__(self, other):
		return not self==other

	def __hash__(self):
		return hash(self.xmlprefix) ^ hash(self.xmlurl)

class NamespaceRegistry(object):
	"""
	<par>global registry for all namespaces</par>
	"""
	def __init__(self):
		self.byPrefix = {}
		self.byURL = {}
		self.all = []

	def register(self, namespace):
		self.byPrefix.setdefault(namespace.xmlprefix, []).insert(0, namespace)
		self.byURL.setdefault(namespace.xmlurl, []).insert(0, namespace)
		self.all.insert(0, namespace)

namespaceRegistry = NamespaceRegistry()

def getNS(ns):
	if isinstance(ns, types.ModuleType):
		if not hasattr(ns, "xmlns") and hasattr(ns, "namespace"):
			errors.warn(DeprecationWarning("the variable name namespace is deprecated, use xmlns instead"))
			return ns.namespace
		else:
			return ns.xmlns
	elif isinstance(ns, Namespace):
		return ns
	elif isinstance(ns, (tuple, list)):
		newns = [ getNS(x) for x in ns]
		if isinstance(ns, tuple):
			newns = tuple(newns)
		return newns
	else:
		try:
			return namespaceRegistry.byURL[ns][0]
		except KeyError:
			raise errors.IllegalNamespaceError(ns)

class Prefixes(object):
	"""
	<par>Specifies a mapping between namespace prefixes and namespaces both
	for parsing and publishing. Each namespace can have multiple prefixes, and
	every prefix can be used by multiple namespaces. A <class>Prefixes</class>
	instance keeps three seperate mappings: one for <pyref class="Element">elements</pyref>,
	one for <pyref class="ProcInst">processing instructions</pyref> and one
	for <pyref class="Entity">entities</pyref>.</par>
	"""
	ELEMENT = 0
	PROCINST = 1
	ENTITY = 2

	NOPREFIX = 0
	USEPREFIX = 1
	DECLAREANDUSEPREFIX = 2

	def __init__(self):
		"""
		Create a <class>Prefixes</class> instance.
		"""
		self._prefix2ns = ({}, {}, {}) # for elements, procinsts and entities

	def addPrefixMapping(self, prefix, ns, mode="prepend", types=(ELEMENT, PROCINST, ENTITY)):
		"""
		<par>Add a mapping from the namespace prefix <arg>prefix</arg>
		to the namespace <arg>ns</arg> to the current configuration.
		<arg>ns</arg> can be a <pyref class="Namespace"><class>Namespace</class></pyref> object,
		a module or a namespace name, because <pyref function="getNS"><function>getNS</function></pyref>
		is used.</par>
		"""
		ns = getNS(ns)
		if isinstance(types, int):
			types = (types, )
		for type in types:
			prefix2ns = self._prefix2ns[type].setdefault(prefix, [])
			if not prefix2ns:
				prefix2ns.append([])
			if mode=="replace":
				prefix2ns[0] = [ns]
			else:
				prefix2ns = prefix2ns[0]
				if mode in ("append", "prepend"):
					try:
						prefix2ns.remove(ns)
					except ValueError:
						pass
					if mode=="append":
						prefix2ns.append(ns)
					else:
						prefix2ns.insert(0, ns)
				else:
					raise ValueError("mode %r unknown" % mode)
		return self

	def addElementPrefixMapping(self, prefix, ns, mode="prepend"):
		return self.addPrefixMapping(prefix, ns, mode, types=Prefixes.ELEMENT)

	def addProcInstPrefixMapping(self, prefix, ns, mode="prepend"):
		return self.addPrefixMapping(prefix, ns, mode, types=Prefixes.PROCINST)

	def addEntityPrefixMapping(self, prefix, ns, mode="prepend"):
		return self.addPrefixMapping(prefix, ns, mode, types=Prefixes.ENTITY)

	def delPrefixMapping(self, prefix=False, ns=False, types=(ELEMENT, PROCINST, ENTITY)):
		"""
		<par>Remove the mapping from the namespace prefix <arg>prefix</arg>
		to the namespace <arg>ns</arg> from the current configuration.
		<arg>ns</arg> can be a <pyref class="Namespace"><class>Namespace</class></pyref> object,
		a module or a namespace name, because <pyref function="getNS"><function>getNS</function></pyref>
		is used.</par>
		<par>If <arg>prefix</arg> is not specified, all prefixes for
		the namespace <arg>ns</arg> will be removed. If <arg>ns</arg> is not specified
		all namespaces for the prefix <arg>prefix</arg> will be removed. If
		both are unspecified the mapping will be empty afterwards.</par>
		"""
		if ns is not False:
			ns = getNS(ns)
		if isinstance(types, int):
			types = (types, )
		for type in types:
			if ns is not False:
				if prefix is not False:
					try:
						prefix2ns = self._prefix2ns[type][prefix]
						prefix2ns[0].remove(ns)
					except (KeyError, IndexError, ValueError):
						pass
				else:
					for prefix2ns in self._prefix2ns[type].itervalues():
						try:
							prefix2ns[0].remove(ns)
						except (IndexError, ValueError):
							pass
			else:
				try:
					prefix2ns = self._prefix2ns[type][prefix][0] = []
				except (KeyError, IndexError):
					pass
				else:
					self._prefix2ns[type] = {}
		return self

	def delElementPrefixMapping(self, prefix=False, ns=False):
		return self.delPrefixMapping(prefix, ns, types=Prefixes.ELEMENT)

	def delProcInstPrefixMapping(self, prefix=False, ns=False):
		return self.delPrefixMapping(prefix, ns, types=Prefixes.PROCINST)

	def delEntityPrefixMapping(self, prefix=False, ns=False):
		return self.delPrefixMapping(prefix, ns, types=Prefixes.ENTITY)

	def startPrefixMapping(self, prefix, ns, mode="replace", types=(ELEMENT, PROCINST, ENTITY)):
		ns = getNS(ns)
		if isinstance(types, int):
			types = (types, )
		for type in types:
			prefix2ns = self._prefix2ns[type].setdefault(prefix, [])
			if mode=="replace":
				prefix2ns.insert(0, [ns])
			elif mode in ("append", "prepend"):
				if prefix2ns:
					old = prefix2ns[0][:]
				else:
					old = []
				if mode=="append":
					prefix2ns.insert(0, old + [ns])
				else:
					prefix2ns.insert(0, [ns] + old)
			else:
				raise ValueError("mode %r unknown" % mode)

	def startElementPrefixMapping(self, prefix, ns, mode="replace"):
		self.startPrefixMapping(prefix, ns, mode, types=Prefixes.ELEMENT)

	def startProcInstPrefixMapping(self, prefix, ns, mode="replace"):
		self.startPrefixMapping(prefix, ns, mode, types=Prefixes.PROCINST)

	def startEntityPrefixMapping(self, prefix, ns, mode="replace"):
		self.startPrefixMapping(prefix, ns, mode, types=Prefixes.ENTITY)

	def endPrefixMapping(self, prefix, types=(ELEMENT, PROCINST, ENTITY)):
		if isinstance(types, int):
			types = (types, )
		for type in types:
			self._prefix2ns[type][prefix].pop(0)

	def endElementPrefixMapping(self, prefix):
		self.endPrefixMapping(prefix, types=Prefixes.ELEMENT)

	def endProcInstPrefixMapping(self, prefix):
		self._endPrefixMapping(prefix, types=Prefixes.PROCINST)

	def endEntityPrefixMapping(self, prefix):
		self._endPrefixMapping(prefix, types=Prefixes.ENTITY)

	def ns4prefix(self, prefix, type):
		"""
		<par>Return the currently active namespace list for the prefix <arg>prefix</arg>.</par>
		"""
		try:
			return self._prefix2ns[type][prefix][0]
		except (KeyError, IndexError):
			return []

	def ns4elementprefix(self, prefix):
		return self.ns4prefix(prefix, Prefixes.ELEMENT)

	def ns4procinstprefix(self, prefix):
		return self.ns4prefix(prefix, Prefixes.PROCINST)

	def ns4entityprefix(self, prefix):
		return self.ns4prefix(prefix, Prefixes.ENTITY)

	def prefix4ns(self, ns, type):
		"""
		<par>Return the currently active prefixes for the namespace <arg>ns</arg>.</par>
		"""
		ns = getNS(ns)
		prefixes = []
		for (prefix, prefix2ns) in self._prefix2ns[type].iteritems():
			if prefix2ns and ns in prefix2ns[0]:
				prefixes.append(prefix)
		if prefixes:
			return prefixes
		else:
			return [ns.xmlprefix]

	def elementprefix4ns(self, ns):
		return self.prefix4ns(ns, Prefixes.ELEMENT)

	def procinstprefix4ns(self, ns):
		return self.prefix4ns(ns, Prefixes.PROCINST)

	def entityprefix4ns(self, ns):
		return self.prefix4ns(ns, Prefixes.ENTITY)

	def __splitqname(self, qname):
		"""
		split a qualified name into a (prefix, local name) pair
		"""
		qname = qname.split(":", 1)
		if len(qname) == 1: # no namespace specified
			qname.insert(0, None)
		return qname

	def elementFromQName(self, qname):
		"""
		<par>returns the element class for the name
		<arg>qname</arg> (which might include a prefix).</par>
		"""
		qname = self.__splitqname(qname)
		for ns in self.ns4elementprefix(qname[0]):
			try:
				cls = ns.elementsByName[qname[1]]
				if not cls.register:
					continue
				return cls
			except KeyError: # no element in this namespace with this name
				pass
		raise errors.IllegalElementError(qname) # elements with this name couldn't be found

	def procInstFromQName(self, qname):
		"""
		<par>returns the processing instruction class for the name
		<arg>qname</arg> (which might include a prefix).</par>
		"""
		qname = self.__splitqname(qname)
		for ns in self.ns4procinstprefix(qname[0]):
			try:
				cls = ns.procinstsByName[qname[1]]
				if not cls.register:
					continue
				return cls
			except KeyError: # no processing instruction in this namespace with this name
				pass
		raise errors.IllegalProcInstError(qname) # processing instructions with this name couldn't be found

	def entityFromQName(self, qname):
		"""
		<par>returns the entity or charref class for the name
		<arg>qname</arg> (which might include a prefix).</par>
		"""
		qname = self.__splitqname(qname)
		# try the charrefs first
		nss = self.ns4entityprefix(qname[0])
		for ns in nss:
			try:
				cls = ns.charrefsByName[qname[1]]
				if not cls.register:
					continue
				return cls
			except KeyError: # no charref in this namespace with this name
				pass
		# no charrefs => try the entities now
		for ns in nss:
			try:
				cls = ns.entitiesByName[qname[1]]
				if not cls.register:
					continue
				return cls
			except KeyError: # no entity in this namespace with this name
				pass
		raise errors.IllegalEntityError(qname) # entities with this name couldn't be found

	def charrefFromNumber(self, number):
		"""
		<par>returns the first charref class for the codepoint <arg>number</arg>.</par>
		"""
		for ns in namespaceRegistry.all:
			try:
				cls = ns.charrefsByNumber[number][0]
				if not cls.register:
					continue
				return cls
			except KeyError:
				pass
		return None

	def attrnameFromQName(self, element, qname):
		"""
		<par>returns the Python name for an attribute for the qualified
		&xml; name <arg>qname</arg> (which might include a prefix, in which case
		a tuple with the namespace object and the name will be returned).</par>
		"""
		qname = self.__splitqname(qname)
		if qname[0] is None:
			try:
				return element.Attrs._handlersByXMLName[qname[1]].__name__
			except KeyError:
				raise errors.IllegalAttrError(element.Attrs, qname[1])
		else:
			for ns in self.ns4prefix(qname[0]):
				try:
					return (ns, ns.Attrs._handlersByXMLName[qname[1]].__name__)
				except KeyError: # no attribute in this namespace with this name
					pass
			raise errors.IllegalAttrError(None, qname)

class OldPrefixes(Prefixes):
	"""
	<par>Prefix mapping that is compatible to the mapping used
	prior to &xist; version 2.0.</par>
	"""
	def __init__(self):
		super(OldPrefixes, self).__init__()
		for ns in namespaceRegistry.all:
			if ns.xmlurl == "http://www.w3.org/XML/1998/namespace":
				self.addPrefixMapping("xml", ns, mode="append")
			else:
				self.addPrefixMapping(None, ns, mode="append")
				self.addPrefixMapping(ns.xmlprefix, ns, mode="append")

class DefaultPrefixes(Prefixes):
	"""
	<par>Prefix mapping that maps all defined namespace
	to their default prefix, except for one which is mapped
	to None.</par>
	"""
	def __init__(self, default=None):
		super(DefaultPrefixes, self).__init__()
		if default is not None:
			default = getNS(default)
		for ns in namespaceRegistry.all:
			if ns is default:
				self.addPrefixMapping(None, ns)
			else:
				self.addElementPrefixMapping(ns.xmlprefix, ns)
				self.addProcInstPrefixMapping(None, ns)
				self.addEntityPrefixMapping(None, ns)

class DocPrefixes(Prefixes):
	"""
	<par>Prefix mapping that is used for &xist; docstrings.</par>
	<par>The <pyref module="ll.xist.ns.doc"><module>doc</module> namespace</pyref>
	and the <pyref module="ll.xist.ns.specials"><module>specials</module> namespace</pyref>
	are mapped to the empty prefix for element. The
	<pyref module="ll.xist.ns.html">&html; namespace</pyref>
	and the <pyref module="ll.xist.ns.abbr"><module>abbr</module> namespace</pyref>
	are available from entities.</par>
	"""
	def __init__(self, default=None):
		super(DocPrefixes, self).__init__()
		from ll.xist.ns import html, abbr, doc, specials
		self.addElementPrefixMapping(None, doc)
		self.addElementPrefixMapping(None, specials)
		self.addEntityPrefixMapping(None, html)
		self.addEntityPrefixMapping(None, abbr)

# C0 Controls and Basic Latin
class quot(CharRef): "quotation mark = APL quote, U+0022 ISOnum"; codepoint = 34
class amp(CharRef): "ampersand, U+0026 ISOnum"; codepoint = 38
class lt(CharRef): "less-than sign, U+003C ISOnum"; codepoint = 60
class gt(CharRef): "greater-than sign, U+003E ISOnum"; codepoint = 62
class apos(CharRef): "apostrophe mark, U+0027 ISOnum"; codepoint = 39

xmlns = Namespace("xsc", None, vars())

prefixes4charrefs = DefaultPrefixes()

###
###
###

class Location(object):
	"""
	<par>Represents a location in an &xml; entity.</par>
	"""

	def __init__(self, locator=None, sysID=None, pubID=None, lineNumber=-1, columnNumber=-1):
		"""
		<par>Create a new <class>Location</class> instance by reading off the current location from
		the <arg>locator</arg>, which is then stored internally. In addition to that the system ID,
		public ID, line number and column number can be overwritten by explicit arguments.</par>
		"""
		if locator is None:
			self.__sysID = None
			self.__pubID = None
			self.__lineNumber = -1
			self.__columnNumber = -1
		else:
			self.__sysID = locator.getSystemId()
			self.__pubID = locator.getPublicId()
			self.__lineNumber = locator.getLineNumber()
			self.__columnNumber = locator.getColumnNumber()
		if self.__sysID is None:
			self.__sysID = sysID
		if self.__pubID is None:
			self.__pubID = pubID
		if self.__lineNumber == -1:
			self.__lineNumber = lineNumber
		if self.__columnNumber == -1:
			self.__columnNumber = columnNumber

	def getColumnNumber(self):
		"<par>Return the column number of this location.</par>"
		return self.__columnNumber

	def getLineNumber(self):
		"<par>Return the line number of this location.</par>"
		return self.__lineNumber

	def getPublicId(self):
		"<par>Return the public identifier for this location.</par>"
		return self.__pubID

	def getSystemId(self):
		"<par>Return the system identifier for this location.</par>"
		return self.__sysID

	def offset(self, offset):
		"""
		<par>returns a location where the line number is incremented by offset
		(and the column number is reset to 1).</par>
		"""
		if offset==0:
			return self
		return Location(sysID=self.__sysID, pubID=self.__pubID, lineNumber=self.__lineNumber+offset, columnNumber=1)

	def __str__(self):
		# get and format the system ID
		sysID = self.getSystemId()
		if sysID is None:
			sysID = "???"

		# get and format the line number
		line = self.getLineNumber()
		if line==-1:
			line = "?"
		else:
			line = str(line)

		# get and format the column number
		column = self.getColumnNumber()
		if column==-1:
			column = "?"
		else:
			column = str(column)

		# now we have the parts => format them
		return "%s:%s:%s" % (presenters.strURL(sysID), presenters.strNumber(line), presenters.strNumber(column))

	def __repr__(self):
		return "<%s object sysID=%r, pubID=%r, lineNumber=%r, columnNumber=%r at %08x>" % \
			(self.__class__.__name__, self.getSystemId(), self.getPublicId(), self.getLineNumber(), self.getColumnNumber(), id(self))

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.getPublicId()==other.getPublicId() and self.getSystemId()==other.getSystemId() and self.getLineNumber()==other.getLineNumber() and self.getColumnNumber()==other.getColumnNumber()

	def __ne__(self, other):
		return not self==other
