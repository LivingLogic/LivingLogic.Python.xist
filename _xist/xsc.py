#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
This module contains all the central &dom; classes, the namespace classes and a few helper
classes and functions.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from __future__ import generators

import os, sys, random, types, new

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
	elif isinstance(value, (str, unicode, int, long, float)):
		return Text(value)
	elif value is None:
		return Null
	elif isinstance(value, (list, tuple)):
		return Frag(*value)
	elif isinstance(value, url.URL):
		return Text(value)
	errors.warn(errors.IllegalObjectWarning(value)) # none of the above, so we report it and maybe throw an exception
	return Null

###
###
###

class Base(object):
	"""
	<par>Base class that adds an enhanced class <method>__repr__</method>
	and a class method <pyref method="__fullname__"><method>__fullname__</method></pyref>
	to subclasses. Subclasses of <class>Base</class> will have an attribute
	<lit>__outerclass__</lit> that references the containing class (if there
	is any). <method>__repr__</method> uses this to show the fully qualified
	class name.</par>
	"""
	class __metaclass__(type):
		def __new__(cls, name, bases, dict):
			dict["__outerclass__"] = None
			res = type.__new__(cls, name, bases, dict)
			for (key, value) in dict.iteritems():
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
		name = cls.__name__.split(".")[-1]
		while 1:
			cls = cls.__outerclass__
			if cls is None:
				return name
			name = cls.__name__.split(".")[-1] + "." + name
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
	startloc = None
	endloc = None

	# Subclasses relevant for parsing (i.e. Element, ProcInst, Entity and CharRef)
	# have an additional class attribute named register. This attribute may have three values:
	# None:  don't add this class to a namespace, not even to the "global" namespace,
	#        the xmlns attribute of those classes will be None. This is used for Element etc.
	#        to avoid bootstrapping problems and should never be used by user classes
	# False: Register with the namespace, i.e. ns.element("foo") will return it and foo.xmlns
	#        will be set to the namespace class, but don't use this class for parsing
	# True:  Register with the namespace and use for parsing.
	# If register is not set it defaults to True

	class __metaclass__(Base.__metaclass__):
		def __new__(cls, name, bases, dict):
			if "register" not in dict:
				dict["register"] = True
			dict["xmlns"] = None
			# needsxmlns may be defined as a constant, this magically turns it into method
			if "needsxmlns" in dict:
				needsxmlns_value = dict["needsxmlns"]
				if not isinstance(needsxmlns_value, classmethod):
					def needsxmlns(cls, publisher=None):
						return needsxmlns_value
					dict["needsxmlns"] = classmethod(needsxmlns)
			if "xmlprefix" in dict:
				xmlprefix_value = dict["xmlprefix"]
				if not isinstance(xmlprefix_value, classmethod):
					def xmlprefix(cls, publisher=None):
						return xmlprefix_value
					dict["xmlprefix"] = classmethod(xmlprefix)
			pyname = unicode(name.split(".")[-1])
			if "xmlname" in dict:
				xmlname = unicode(dict["xmlname"])
			else:
				xmlname = pyname
			dict["xmlname"] = (pyname, xmlname)
			return Base.__metaclass__.__new__(cls, name, bases, dict)

	class Context(Base, list):
		"""
		<par>This is an empty class, that can be used by the
		<pyref module="ll.xist.xsc" class="Node" method="convert"><method>convert</method></pyref>
		method to hold element specific data during the convert call. The method
		<pyref class="Converter" method="__getitem__"><method>Converter.__getitem__</method></pyref>
		will return a unique instance of this class.</par>
		"""

		def __init__(self):
			list.__init__(self)

	def __repr__(self):
		return self.repr(presenters.defaultPresenterClass())

	def __ne__(self, other):
		return not self==other

	def _strbase(cls, formatter, s, fullname, xml):
		if fullname:
			if xml:
				s.append(presenters.strNamespace(cls.xmlname[xml]))
			else:
				s.append(presenters.strNamespace(cls.__module__))
			s.append(presenters.strColon())
		if xml:
			s.append(formatter(cls.xmlname[xml]))
		elif fullname:
			s.append(formatter(cls.__fullname__()))
		else:
			s.append(formatter(cls.xmlname[xml]))
	_strbase = classmethod(_strbase)

	def clone(self):
		"""
		returns an identical clone of the node and its children.
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

	def conv(self, converter=None, root=None, mode=None, stage=None, target=None, lang=None, function=None, makeaction=None, maketarget=None):
		"""
		<par>Convenience method for calling either <pyref method="mapped"><method>mapped</method></pyref> or
		<pyref method="convert"><method>convert</method></pyref>, depending on whether <arg>function</arg> is specified or not.</par>
		<par><method>conv</method> will automatically set <lit><arg>converter</arg>.node</lit> to <self/> to remember the
		<z>document root</z> for which <method>conv</method> has been called, this means that you should not call <method>conv</method>
		in any of the recursive calls, as you would loose this information. Call <pyref method="convert"><method>convert</method></pyref>
		or <pyref method="mapped"><method>mapped</method></pyref> directly instead.</par>
		"""
		if converter is None:
			converter = converters.Converter(node=self, root=root, mode=mode, stage=stage, target=target, lang=lang, function=function, makeaction=makeaction, maketarget=maketarget)
			if converter.function is not None:
				return self.mapped(converter)
			else:
				return self.convert(converter)
		else:
			converter.push(node=self, root=root, mode=mode, stage=stage, target=target, lang=lang, function=function, makeaction=makeaction, maketarget=maketarget)
			if converter.function is not None:
				node = self.mapped(converter)
			else:
				node = self.convert(converter)
			converter.pop()
			return node

	def convert(self, converter):
		"""
		<par>implementation of the conversion method.
		When you define your own element classes you have to overwrite this method.</par>

		<par>E.g. when you want to define an element that packs its content into an &html;
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

	def __str__(self):
		return str(unicode(self))

	def asText(self, monochrome=1, squeezeBlankLines=0, lineNumbers=0, width=72):
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
		if width!=80:
			options += " -cols %d" % width

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
		returns this node converted to a long integer.
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
		returns this node converted to a complex number.
		"""
		return complex(unicode(self))

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
			return cls.xmlns.xmlname
	xmlprefix = classmethod(xmlprefix)

	def _publishname(self, publisher):
		if self.needsxmlns(publisher)>=1:
			prefix = self.xmlprefix(publisher)
			if prefix is not None:
				publisher.publish(prefix)
				publisher.publish(u":")
		publisher.publish(self.xmlname[True])

	def parsed(self, handler, begin=None):
		"""
		<par>This method will be called by the parsing handler <arg>handler</arg>
		once after <self/> is created by the parser. This is e.g. used by
		<pyref class="URLAttr"><class>URLAttr</class></pyref> to incorporate
		the base <pyref module="ll.url" class="URL"><class>URL</class></pyref>
		<arg>base</arg> into the attribute.</par>
		<par>For elements <function>parsed</function> will be called twice:
		once at the beginning of the element with <lit><arg>begin</arg>==True</lit>
		and once at the end of the element with <lit><arg>begin</arg>==False</lit>.</par>
		"""
		pass

	def publish(self, publisher):
		"""
		<par>generates unicode strings for the node, and passes
		the strings to <arg>publisher</arg>, which must
		be an instance of <pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref>.</par>

		<par>The encoding and xhtml specification are taken from the <arg>publisher</arg>.</par>
		"""
		raise NotImplementedError("publish method not implemented in %s" % self.__class__.__name__)

	def asString(self, base=None, root=None, xhtml=None, prefixes=None, elementmode=0, procinstmode=0, entitymode=0):
		"""
		<par>returns this element as a unicode string.</par>

		<par>For the parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref> constructor.</par>
		"""
		publisher = publishers.StringPublisher(base=base, root=root, xhtml=xhtml, prefixes=prefixes, elementmode=elementmode, procinstmode=procinstmode, entitymode=entitymode)
		return publisher.doPublication(self)

	def asBytes(self, base=None, root=None, encoding=None, xhtml=None, prefixes=None, elementmode=0, procinstmode=0, entitymode=0):
		"""
		<par>returns this element as a byte string suitable for writing
		to an &html; file or printing from a CGI script.</par>

		<par>For the parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref> constructor.</par>
		"""
		publisher = publishers.BytePublisher(base=base, root=root, encoding=encoding, xhtml=xhtml, prefixes=prefixes, elementmode=elementmode, procinstmode=procinstmode, entitymode=entitymode)
		return publisher.doPublication(self)

	def write(self, stream, base=None, root=None, encoding=None, xhtml=None, prefixes=None, elementmode=0, procinstmode=0, entitymode=0):
		"""
		<par>writes the element to the file like object <arg>file</arg>.</par>

		<par>For the rest of the parameters
		see the <pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref> constructor.</par>
		"""
		publisher = publishers.FilePublisher(stream, base=base, root=root, encoding=encoding, xhtml=xhtml, prefixes=prefixes, elementmode=elementmode, procinstmode=procinstmode, entitymode=entitymode)
		return publisher.doPublication(self)

	def find(self, type=None, subtype=False, attrs=None, test=None, searchchildren=False, searchattrs=False):
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

	def _matchesattrs(self, attrs):
		if attrs is None:
			return True
		else:
			if isinstance(self, Element):
				for attr in attrs.keys():
					if (not self.attrs.has(attr)) or ((attrs[attr] is not None) and (unicode(self[attr]) != attrs[attr])):
						return False
				return True
			else:
				return False

	def _matches(self, type_, subtype, attrs, test):
		res = True
		if type_ is not None:
			if not isinstance(type_, list) and not isinstance(type_, tuple):
				type_ = (type_,)
			for t in type_:
				if subtype:
					if isinstance(self, t):
						res = self._matchesattrs(attrs)
						break
				else:
					if self.__class__ == t:
						res = self._matchesattrs(attrs)
						break
			else:
				res = False
		else:
			res = self._matchesattrs(attrs)
		if res and (test is not None):
			res = test(self)
		return bool(res)

	def _decoratenode(self, node):
		"""
		<par>decorate the <pyref class="Node"><class>Node</class></pyref>
		<arg>node</arg> with the same location information as <self/>.</par>
		"""

		node.startloc = self.startloc
		node.endloc = self.endloc
		return node

	def mapped(self, converter):
		"""
		<par>returns the node mapped through the function <arg>function</arg>.
		This call works recursively (for <pyref class="Frag"><class>Frag</class></pyref>
		and <pyref class="Element"><class>Element</class></pyref>).</par>
		<par>When you want an unmodified node you simply can return <self/>. <method>mapped</method>
		will make a copy of it and fill the content recursively. Note that element attributes
		will not be mapped. When you return a different node from <function>function</function>
		this node will be incorporated into the result as-is.</par>
		"""
		node = converter.function(self, converter)
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

	def walkpath(self, before=True, after=False, attrs=False, attrsbefore=True, attrafter=False):
		"""
		<par>walk the tree. This method is a generator and for each node
		in the tree generates a list with the <z>path</z> to the node, i.e.
		the node and all its ancestor nodes.</par>
		<par>For the arguments see <pyref method="walk"><method>walk</method></pyref>.</par>
		"""
		yield [self]

	def withSep(self, separator, clone=False):
		errors.warn(DeprecationWarning("withSep() is deprecated, use withsep() instead"))
		return self.withsep(separator, clone)

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
		return frag.withsep(self)

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
	<par>A text node. The characters <markup>&lt;</markup>, <markup>&gt;</markup>, <markup>&amp;</markup>
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

	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen(), presenters.strSlash())
		cls._strbase(presenters.strElementName, s, fullname=fullname, xml=xml)
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
		return self._decoratenode(node)

	def clone(self):
		node = self._create()
		list.extend(node, [ child.clone() for child in self ])
		return self._decoratenode(node)

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

	__rmul__ = __mul__

	# no need to implement __len__ or __nonzero__

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

	def find(self, type=None, subtype=False, attrs=None, test=None, searchchildren=False, searchattrs=False):
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
		return self._decoratenode(node)

	def withsep(self, separator, clone=False):
		"""
		<par>return a version of <self/> with a separator node between the nodes of <self/>.</par>

		<par>if <arg>clone</arg> is false one node will be inserted several times,
		if <arg>clone</arg> is true clones of this node will be used.</par>
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

	def mapped(self, converter):
		node = converter.function(self, converter)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = self._create()
			for child in self:
				node.append(child.mapped(converter))
		return node

	def normalized(self):
		node = self._create()
		lasttypeOK = False
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

	def walkpath(self, before=True, after=False, attrs=False, attrbefore=True, attrafter=False):
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
	register = None

	# we don't need a constructor, because we don't have to store the target,
	# because the target is our classname (or the class attribute name)

	class __metaclass__(CharacterData.__metaclass__):
		def __new__(cls, name, bases, dict):
			self = CharacterData.__metaclass__.__new__(cls, name, bases, dict)
			if self.register is not None:
				setattr(xmlns, name, self)
			return self

		def __repr__(self):
			return "<procinst class %s/%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def _registerns(cls, ns):
		if cls.xmlns is not None:
			for xml in (False, True):
				del cls.xmlns._procinsts[xml][cls.xmlname[xml]]
			cls.xmlns = None
		if ns is not None:
			for xml in (False, True):
				ns._procinsts[xml][cls.xmlname[xml]] = cls
			cls.xmlns = ns
	_registerns = classmethod(_registerns)

	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen(), presenters.strQuestion())
		cls._strbase(presenters.strProcInstTarget, s, fullname=fullname, xml=xml)
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
				return cls.xmlns.xmlname[True]
			else:
				return publisher.prefixes.procinstprefix4ns(cls.xmlns)[0]
	xmlprefix = classmethod(xmlprefix)

	def publish(self, publisher):
		if self.content.find(u"?>")!=-1:
			raise errors.IllegalProcInstFormatError(self)
		publisher.publish(u"<?")
		self._publishname(publisher)
		publisher.publish(u" ")
		publisher.publish(self.content)
		publisher.publish(u"?>")

	def __unicode__(self):
		return u""

class Null(CharacterData):
	"""
	node that does not contain anything.
	"""

	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen())
		cls._strbase(presenters.strElementName, s, fullname=fullname, xml=xml)
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
	<example><title>Elements inside attributes</title>
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
	required = False
	default = None
	values = None
	class __metaclass__(Frag.__metaclass__):
		def __new__(cls, name, bases, dict):
			# can be overwritten in subclasses, to specify that this attributes is required
			if "required" in dict:
				dict["required"] = bool(dict["required"])
			# convert the default to a Frag
			if "default" in dict:
				dict["default"] = Frag(dict["default"])
			# convert the entries in values to unicode
			if "values" in dict:
				values = dict["values"]
				if values is not None:
					dict["values"] = tuple([unicode(entry) for entry in dict["values"]])
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

	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		cls._strbase(presenters.strAttrName, s, fullname=fullname, xml=xml)
		return s
	_str = classmethod(_str)

	def present(self, presenter):
		presenter.presentAttr(self)

	def checkvalid(self):
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

	def parsed(self, handler, begin=None):
		self.checkvalid()

	def _publishAttrValue(self, publisher):
		Frag.publish(self, publisher)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		self.checkvalid()
		publisher.inAttr += 1
		self._publishname(publisher) # publish the XML name, not the Python name
		publisher.publish(u"=\"")
		publisher.pushTextFilter(helpers.escapeattr)
		self._publishAttrValue(publisher)
		publisher.popTextFilter()
		publisher.publish(u"\"")
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

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		self.checkvalid()
		publisher.inAttr += 1
		self._publishname(publisher) # publish the XML name, not the Python name
		if publisher.xhtml>0:
			publisher.publish(u"=\"")
			publisher.pushTextFilter(helpers.escapeattr)
			publisher.publish(self.__class__.xmlname[True])
			publisher.popTextFilter()
			publisher.publish(u"\"")
		publisher.inAttr -= 1

class ColorAttr(Attr):
	"""
	<par>Attribute class that is used for a color attributes.</par>
	"""

class StyleAttr(Attr):
	"""
	<par>Attribute class that is used for &css; style attributes.</par>
	"""

	def parsed(self, handler, begin=None):
		if not self.isfancy():
			value = cssparsers.parseString(unicode(self), handler=cssparsers.ParseHandler(), base=handler.base)
			self[:] = (value, )

	def _publishAttrValue(self, publisher):
		if not self.isfancy():
			value = cssparsers.parseString(unicode(self), handler=cssparsers.PublishHandler(), base=publisher.base)
			new = Frag(value)
			new.publish(publisher)
		else:
			super(StyleAttr, self)._publishAttrValue(publisher)

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
	<par>Attribute class that is used for &url;s. See the module <pyref module="ll.url"><module>ll.url</module></pyref>
	for more information about &url; handling.</par>
	"""

	def parsed(self, handler, begin=None):
		self[:] = utils.replaceInitialURL(self, lambda u: handler.base/u)

	def _publishAttrValue(self, publisher):
		new = utils.replaceInitialURL(self, lambda u: u.relative(publisher.base))
		new.publish(publisher)

	def asURL(self):
		"""
		<par>Return <self/> as a <pyref module="ll.url" class="URL"><class>URL</class></pyref>
		instance (note that non-character content will be filtered out).</par>
		"""
		return url.URL(Attr.__unicode__(self))

	def __unicode__(self):
		return self.asURL().url

	def forInput(self, root=None):
		"""
		<par>return a <pyref module="ll.url" class="URL"><class>URL</class></pyref> pointing
		to the real location of the referenced resource. <arg>root</arg> must be the
		root &url; relative to which <self/> will be interpreted and usually
		comes from the <lit>root</lit> attribute of the <arg>converter</arg> argument in
		<pyref class="Node" method="convert"><method>convert</method></pyref>.</par>
		"""
		u = self.asURL()
		if u.scheme == "root":
			u.scheme = None
		u = url.URL(root)/u
		return u

	def imagesize(self, root=None):
		"""
		Return the size of an image as a tuple.
		"""
		return self.openread(root).imagesize

	def contentlength(self, root=None):
		"""
		Return the size of a file in bytes.
		"""
		return self.openread(root).contentlength

	def lastmodified(self, root=None):
		"""
		returns the timestamp for the last modification to the file
		"""
		return self.openread(root).lastmodified

	def openread(self, root=None):
		"""
		Return a <pyref module="ll.url" class="ReadResource"><class>ReadResource</class></pyref>
		for reading from the &url;.
		"""
		return self.forInput(root).openread()

	def openwrite(self, root=None):
		"""
		Return a <pyref module="ll.url" class="WriteResource"><class>WriteResource</class></pyref>
		for writing to the &url;.
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
	of <pyref class="Attr"><class>Attr</class></pyref>.</par>
	"""

	class __metaclass__(Node.__metaclass__):
		def __new__(cls, name, bases, dict):
			# Automatically inherit the attributes from the base class (because the global Attrs require a pointer back to their defining namespace)
			for base in bases:
				for attrname in dir(base):
					attr = getattr(base, attrname)
					if isinstance(attr, type) and issubclass(attr, Attr) and attrname not in dict:
						classdict = {"__module__": dict["__module__"]}
						if attr.xmlname[0] != attr.xmlname[1]:
							classdict["xmlname"] = attr.xmlname[1]
						dict[attrname] = attr.__class__(attr.__name__, (attr,), classdict)
			self = Node.__metaclass__.__new__(cls, name, bases, {})
			self._attrs = ({}, {})
			for (key, value) in dict.iteritems():
				setattr(self, key, value)
			return self

		def __repr__(self):
			return "<attrs class %s/%s with %s attrs at 0x%x>" % (self.__module__, self.__fullname__(), len(self._attrs[0]), id(self))

		def __getitem__(cls, key):
			return cls._attrs[0][key]

		def __delattr__(cls, key):
			value = cls.__dict__.get(key, None) # no inheritance
			if isinstance(value, type) and issubclass(value, Attr):
				for xml in (False, True):
					del cls._attrs[xml][value.xmlname[xml]]
			return Node.__metaclass__.__delattr__(cls, key)

		def __setattr__(cls, key, value):
			oldvalue = cls.__dict__.get(key, None) # no inheritance
			if isinstance(oldvalue, type) and issubclass(oldvalue, Attr):
				for xml in (False, True):
					del cls._attrs[xml][oldvalue.xmlname[xml]]
			if isinstance(value, type) and issubclass(value, Attr):
				for xml in (False, True):
					cls._attrs[xml][value.xmlname[xml]] = value
			return Node.__metaclass__.__setattr__(cls, key, value)

	def __init__(self, content=None, **attrs):
		dict.__init__(self)
		if content is not None:
			for (attrname, attrvalue) in content.iteritems():
				self[attrname] = attrvalue
		for (attrname, attrvalue) in attrs.iteritems():
			self[attrname] = attrvalue

	def __eq__(self, other):
		return self.__class__ is other.__class__ and dict.__eq__(self, other)

	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		cls._strbase(presenters.strAttrsName, s, fullname=fullname, xml=xml)
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
		for attrvalue in self.itervalues():
			attrvalue.clear()

	def clone(self):
		node = self._create()
		for (key, value) in dict.iteritems(self):
			dict.__setitem__(node, key, value.clone())
		return node

	def convert(self, converter):
		node = self._create()
		for (attrname, attrvalue) in self.iteritems():
			convertedattr = attrvalue.convert(converter)
			assert isinstance(convertedattr, Node), "the convert method returned the illegal object %r (type %r) when converting the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
			node[attrname] = convertedattr
		return node

	def compact(self):
		node = self._create()
		for (attrname, attrvalue) in self.iteritems():
			convertedattr = attrvalue.compact()
			assert isinstance(convertedattr, Node), "the compact method returned the illegal object %r (type %r) when compacting the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
			node[attrname] = convertedattr
		return node

	def normalized(self):
		node = self._create()
		for (attrname, attrvalue) in self.iteritems():
			convertedattr = attrvalue.normalized()
			assert isinstance(convertedattr, Node), "the normalized method returned the illegal object %r (type %r) when normalizing the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
			node[attrname] = convertedattr
		return node

	def find(self, type=None, subtype=False, attrs=None, test=None, searchchildren=False, searchattrs=False):
		node = Frag()
		if searchattrs:
			for attrvalue in self.itervalues():
				node.append(attrvalue.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def present(self, presenter):
		presenter.presentAttrs(self)

	def parsed(self, handler, begin=None):
		# collect required attributes
		attrs = {}
		for (key, value) in self.iteralloweditems():
			if value.required:
				attrs[key] = None
		# if a required attribute is encountered, remove from the list of outstanding ones
		for attrname in self.iterkeys():
			try:
				del attrs[attrname]
			except KeyError:
				pass
		# are there any required attributes remaining that haven't been specified? => warn about it
		if attrs:
			errors.warn(errors.RequiredAttrMissingWarning(self, attrs.keys()))

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		# collect required attributes
		attrs = {}
		for (key, value) in self.iteralloweditems():
			if value.required:
				attrs[key] = None
		for (attrname, attrvalue) in self.iteritems():
			publisher.publish(u" ")
			# if a required attribute is encountered, remove from the list of outstanding ones
			try:
				del attrs[attrname]
			except KeyError:
				pass
			attrvalue.publish(publisher)
		# are there any required attributes remaining that haven't been specified? => warn about it
		if attrs:
			errors.warn(errors.RequiredAttrMissingWarning(self, attrs.keys()))

	def __unicode__(self):
		return u""

	def isallowed(cls, name, xml=False):
		return name in cls._attrs[xml]
	isallowed = classmethod(isallowed)

	def __getitem__(self, name):
		return self.attr(name)

	def __setitem__(self, name, value):
		return self.set(name, value)

	def __delitem__(self, name):
		attr = self.allowedattr(name)
		dict.__delitem__(self, attr.xmlname[False])

	def has(self, name, xml=False):
		"""
		<par>return whether <self/> has an attribute named <arg>name</arg>. <arg>xml</arg>
		speficies whether <arg>name</arg> should be treated as an &xml; name
		(<lit><arg>xml</arg>==True</lit>) or a Python name (<lit><arg>xml</arg>==False</lit>).</par>
		"""
		attr = self.allowedattr(name, xml=xml)
		try:
			attr = dict.__getitem__(self, attr.xmlname[False])
		except KeyError:
			attr = attr.default
		return len(attr)>0

	def get(self, name, default=None, xml=False):
		"""
		<par>works like the dictionary method <method>get</method>,
		it returns the attribute with the name <arg>name</arg>,
		or <arg>default</arg> if <self/> has no such attribute. <arg>xml</arg>
		speficies whether <arg>name</arg> should be treated as an &xml; name
		(<lit><arg>xml</arg>==True</lit>) or a Python name (<lit><arg>xml</arg>==False</lit>).</par>
		"""
		attr = self.attr(name, xml=xml)
		if not attr:
			attr = self.allowedattr(name, xml=xml)(default) # pack the attribute into an attribute object
		return attr

	def set(self, name, value=None, xml=False):
		attr = self.allowedattr(name, xml=xml)(value)
		dict.__setitem__(self, name, attr) # put the attribute in our dict

	def setdefault(self, name, xml=False, default=None):
		"""
		<par>works like the dictionary method <method>setdefault</method>,
		it returns the attribute with the name <arg>name</arg>.
		If <self/> has no such attribute, it will be set to <arg>default</arg>
		and <arg>default</arg> will be returned as the new attribute value. <arg>xml</arg>
		speficies whether <arg>name</arg> should be treated as an &xml; name
		(<lit><arg>xml</arg>==True</lit>) or a Python name (<lit><arg>xml</arg>==False</lit>).</par>
		"""
		attr = self.attr(name, xml=xml)
		if not attr:
			attr = self.allowedattr(name, xml=xml)(default) # pack the attribute into an attribute object
			dict.__setitem__(self, name, attr)
		return attr

	def update(self, mapping):
		"""
		Copies attributes over from <arg>mapping</arg>.
		"""
		for (attrname, attrvalue) in mapping.iteritems():
			self[attrname] = attrvalue

	def updateexisting(self, mapping):
		"""
		Copies attributes over from <arg>mapping</arg>, but only if
		they exist in <self/>.
		"""
		for (attrname, attrvalue) in mapping.iteritems():
			if self.has(attrname):
				self[attrname] = attrvalue

	def updatenew(self, mapping):
		"""
		Copies attributes over from <arg>mapping</arg>, but only if
		they don't exist in <self/>.
		"""
		for (attrname, attrvalue) in mapping.iteritems():
			if not self.has(attrname):
				self[attrname] = attrvalue

	def copydefaults(self, fromMapping):
		errors.warn(DeprecationWarning("Attrs.copydefaults() is deprecated, use Attrs.updateexisting() instead"))
		return self.updateexisting(fromMapping)

	def iterallowedkeys(cls, xml=False):
		"""
		<par>return an iterator for iterating through the names of allowed attributes. <arg>xml</arg>
		speficies whether &xml; names (<lit><arg>xml</arg>==True</lit>) or Python names
		(<lit><arg>xml</arg>==False</lit>)i should be returned.</par>
		"""
		return cls._attrs[xml].iterkeys()
	iterallowedkeys = classmethod(iterallowedkeys)

	def allowedkeys(cls, xml=False):
		"""
		<par>return a list of allowed keys (i.e. attribute names)</par>
		"""
		return cls._attrs[xml].keys()
	allowedkeys = classmethod(allowedkeys)

	def iterallowedvalues(cls):
		return cls._attrs[0].itervalues()
	iterallowedvalues = classmethod(iterallowedvalues)

	def allowedvalues(cls):
		"""
		<par>return a list of values for the allowed values.</par>
		"""
		return cls._attrs[0].values()
	allowedvalues = classmethod(allowedvalues)

	def iteralloweditems(cls, xml=False):
		return cls._attrs[xml].iteritems()
	iteralloweditems = classmethod(iteralloweditems)

	def alloweditems(cls, xml=False):
		return cls._attrs[xml].items()
	alloweditems = classmethod(alloweditems)

	def allowedattr(cls, name, xml=False):
		try:
			return cls._attrs[xml][name]
		except KeyError:
			raise errors.IllegalAttrError(cls, name, xml=xml)
	allowedattr = classmethod(allowedattr)

	def __iter__(self):
		return self.iterkeys()

	def __len__(self):
		return len(self.keys())

	def __contains__(self, key):
		return self.has(key)

	def iterkeys(self, xml=False):
		found = {}
		for (key, value) in dict.iteritems(self):
			if len(value):
				if isinstance(key, tuple):
					yield (value.xmlns, value.xmlname[xml])
				else:
					yield value.xmlname[xml]
		# fetch the keys of attributes with a default value (if it hasn't been overwritten)
		for (key, value) in self.alloweditems():
			if value.default and not dict.has_key(self, key):
				yield value.xmlname[xml]

	def keys(self, xml=False):
		return list(self.iterkeys(xml=xml))

	def itervalues(self):
		# fetch the existing attribute keys/values
		for value in dict.itervalues(self):
			if len(value):
				yield value
		# fetch the keys of attributes with a default value (if it hasn't been overwritten)
		for (key, value) in self.iteralloweditems():
			if value.default and not dict.has_key(self, key):
				value = value(value.default.clone())
				dict.__setitem__(self, key, value)
				yield value

	def values(self):
		return list(self.itervalues())

	def iteritems(self, xml=False):
		# fetch the existing attribute keys/values
		for (key, value) in dict.iteritems(self):
			if len(value):
				if isinstance(key, tuple):
					yield ((value.xmlns, value.xmlname[xml]), value)
				else:
					yield (value.xmlname[xml], value)
		# fetch the keys of attributes with a default value (if it hasn't been overwritten)
		for (key, value) in self.iteralloweditems():
			if value.default and not dict.has_key(self, key):
				value = value(value.default.clone())
				dict.__setitem__(self, key, value)
				yield (value.xmlname[xml], value)

	def items(self, xml=False):
		return list(self.iteritems(xml=xml))

	def attr(self, name, xml=False):
		attr = self.allowedattr(name, xml=xml)
		try:
			attr = dict.__getitem__(self, attr.xmlname[False])
		except KeyError: # if the attribute is not there generate a new one (containing the default value)
			attr = attr()
			dict.__setitem__(self, name, attr)
		return attr

	def filtered(self, function):
		"""
		returns a filtered version of the <self/>.
		"""
		node = self._create()
		for (name, value) in self.iteritems():
			if function(value):
				node[name] = value
		return node

	def with(self, names=[], xml=False):
		"""
		<par>Return a copy of <self/> where only the attributes in <arg>names</arg> are
		kept, all others are removed.</par>
		"""
		return self.filtered(lambda n: n.xmlname[xml] in names)

	def without(self, names=[], xml=False):
		"""
		<par>Return a copy of <self/> where all the attributes in <arg>names</arg> are
		removed.</par>
		"""
		return self.filtered(lambda n: n.xmlname[xml] not in names)

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
	<lit>empty</lit>: this is either <lit>False</lit> or <lit>True</lit>
	and specifies whether the element type is allowed to have content
	or not. This will be checked when parsing or publishing.</par>

	<par><lit>Attrs</lit>, which is a class derived from
	<pyref class="Element.Attrs"><class>Element.Attrs</class></pyref>
	and should define all attributes as classes nested inside this
	<class>Attrs</class> class.</par>
	"""

	empty = False # False => element with content; True => element without content
	register = None

	class __metaclass__(Node.__metaclass__):
		def __new__(cls, name, bases, dict):
			if "name" in dict and isinstance(dict["name"], (str, unicode)):
				errors.warn(DeprecationWarning("name is deprecated, use xmlname instead"))
				dict["xmlname"] = dict["name"]
				del dict["name"]
			if "attrHandlers" in dict:
				errors.warn(DeprecationWarning("attrHandlers is deprecated, use a nested Attrs class instead"))
			self = Node.__metaclass__.__new__(cls, name, bases, dict)
			if self.register is not None:
				setattr(xmlns, name, self)
			return self
		def __repr__(self):
			return "<element class %s/%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	class Attrs(Attrs):
		def allowedattr(cls, name, xml=False):
			if isinstance(name, tuple):
				return name[0].Attrs.allowedattr(name[1], xml=xml)
			else:
				# FIXME reimplemented here, because super does not work
				try:
					return cls._attrs[xml][name]
				except KeyError:
					raise errors.IllegalAttrError(cls, name, xml=xml)
		allowedattr = classmethod(allowedattr)

		def with(self, names=[], namespaces=(), keepglobals=False, xml=False):
			"""
			<par>Return a copy of <self/> where only the attributes in <arg>names</arg> are
			kept, all others names are removed. <arg>names</arg> may contain local or
			global names. In additional to that, global attributes will be kept if the
			namespace of the global attribute is in <arg>namespaces</arg>. If <arg>keepglobals</arg>
			is true all global attributes will be kept.</par>
			<par>For testing namespaces a subclass check will be done,
			i.e. attributes from derived namespaces will be kept, if the base namespace
			is specified in <arg>namespaces</arg> or <arg>names</arg>.</par>
			"""

			def keep(node):
				name = node.xmlname[xml]
				if node.xmlns is None:
					return name in names
				else:
					if keepglobals:
						return True
					for ns in namespaces:
						if issubclass(node.xmlns, ns):
							return True
					for testname in names:
						if isinstance(testname, tuple) and issubclass(node.xmlns, testname[0]) and name==testname[1]:
							return True
					return False

			return self.filtered(keep)

		def without(self, names=[], namespaces=(), keepglobals=True, xml=False):
			"""
			<par>Return a copy of <self/> where all the attributes in <arg>names</arg> are
			removed. In additional to that a global attribute will be removed if its
			namespace is found in <arg>namespaces</arg> or if <arg>keepglobals</arg> is false.</par>
			<par>For testing namespaces a subclass check will be done,
			i.e. attributes from derived namespaces will be removed, if the base namespace
			is specified in <arg>namespaces</arg> or <arg>names</arg>.</par>
			"""
			def keep(node):
				name = node.xmlname[xml]
				if node.xmlns is None:
					return name not in names
				else:
					if not keepglobals:
						return False
					for ns in namespaces:
						if issubclass(node.xmlns, ns):
							return False
					for testname in names:
						if isinstance(testname, tuple) and issubclass(node.xmlns, testname[0]) and name==testname[1]:
							return False
					return True

			return self.filtered(keep)

	def __init__(self, *content, **attrs):
		"""
		<par>Create a new <class>Element</class> instance.</par>
		
		<par>positional arguments are treated as content nodes.
		Keyword arguments and dictionaries are treated as attributes.</par>
		"""
		self.attrs = self.Attrs()
		newcontent = []
		for child in content:
			if isinstance(child, dict):
				for (attrname, attrvalue) in child.iteritems():
					self.attrs[attrname] = attrvalue
			else:
				newcontent.append(child)
		self.content = Frag(*newcontent)
		for (attrname, attrvalue) in attrs.iteritems():
			self.attrs[attrname] = attrvalue

	def _registerns(cls, ns):
		if cls.xmlns is not None:
			for xml in (False, True):
				del cls.xmlns._elements[xml][cls.xmlname[xml]]
			cls.xmlns = None
		if ns is not None:
			for xml in (False, True):
				ns._elements[xml][cls.xmlname[xml]] = cls
			cls.xmlns = ns
	_registerns = classmethod(_registerns)

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.content==other.content and self.attrs==other.attrs

	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen())
		cls._strbase(presenters.strElementName, s, fullname=fullname, xml=xml)
		if decorate:
			if cls.empty:
				s.append(presenters.strSlash())
			s.append(presenters.strBracketClose())
		return s
	_str = classmethod(_str)

	def checkvalid(self):
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def parsed(self, handler, begin=None):
		if not begin:
			self.checkvalid()

	def append(self, *items):
		"""
		<par>appends to content (see <pyref class="Frag" method="append"><method>Frag.append</method></pyref>
		for more info)</par>
		"""
		self.content.append(*items)

	def insert(self, index, *items):
		"""
		<par>inserts into the content (see <pyref class="Frag" method="insert"><method>Frag.insert</method></pyref>
		for more info)</par>
		"""
		self.content.insert(index, *items)

	def convert(self, converter):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.convert(converter)
		node.attrs = self.attrs.convert(converter)
		return self._decoratenode(node)

	def clone(self):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.clone() # this is faster than passing it in the constructor (no ToNode call)
		node.attrs = self.attrs.clone()
		return self._decoratenode(node)

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

		if self.attrs.has(imgattr):
			attr = self[imgattr]
			try:
				size = attr.imagesize(root)
			except IOError, exc:
				errors.warn(errors.FileNotFoundWarning("can't read image", unicode(attr), exc))
			else:
				sizedict = {"width": size[0], "height": size[1]}
				for attr in (heightattr, widthattr):
					if attr is not None: # do something to the width/height
						if self.attrs.has(attr):
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
				return cls.xmlns.xmlname[True]
			else:
				return publisher.prefixes.elementprefix4ns(cls.xmlns)[0]
	xmlprefix = classmethod(xmlprefix)

	def publish(self, publisher):
		self.checkvalid()
		if publisher.inAttr:
			# publish the content only, when we are inside an attribute
			# this works much like using the plain string value, but
			# even works with processing instructions, or what the Entity &xist; returns
			self.content.publish(publisher)
		else:
			publisher.publish(u"<")
			self._publishname(publisher)
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
				self._publishname(publisher)
				publisher.publish(u">")
			else:
				if publisher.xhtml in (0, 1):
					if self.empty:
						if publisher.xhtml==1:
							publisher.publish(u" /")
						publisher.publish(u">")
					else:
						publisher.publish(u"></")
						self._publishname(publisher)
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

	def hasAttr(self, attrname, xml=False):
		errors.warn(DeprecationWarning("foo.hasAttr() is deprecated, use foo.attrs.has() instead"))
		return self.attrs.has(attrname, xml=xml)

	def hasattr(self, attrname, xml=False):
		errors.warn(DeprecationWarning("foo.hasattr() is deprecated, use foo.attrs.has() instead"))
		return self.attrs.has(attrname, xml=xml)

	def isallowedattr(cls, attrname):
		"""
		<par>return whether the attribute named <arg>attrname</arg> is allowed for <self/>.</par>
		"""
		errors.warn(DeprecationWarning("foo.isallowedattr() is deprecated, use foo.Attrs.isallowed() instead"))
		return cls.Attrs.isallowed(attrname)
	isallowedattr = classmethod(isallowedattr)

	def getAttr(self, attrname, default=None):
		errors.warn(DeprecationWarning("foo.getAttr() is deprecated, use foo.attrs.get() instead"))
		return self.getattr(attrname, default)

	def getattr(self, attrname, default=None):
		errors.warn(DeprecationWarning("foo.getattr() is deprecated, use foo.attrs.get() instead"))
		return self.attrs.get(attrname, default)

	def setDefaultAttr(self, attrname, default=None):
		errors.warn(DeprecationWarning("foo.setDefaultAttr() is deprecated, use foo.attrs.setdefault() instead"))
		return self.setdefault(attrname, default=default)

	def setdefaultattr(self, attrname, default=None):
		errors.warn(DeprecationWarning("foo.setDefaultAttr() is deprecated, use foo.attrs.setdefault() instead"))
		return self.attrs.setdefault(attrname, default)

	def attrkeys(self, xml=False):
		errors.warn(DeprecationWarning("foo.attrkeys() is deprecated, use foo.attrs.keys() instead"))
		return self.attrs.keys(xml=xml)

	def attrvalues(self):
		errors.warn(DeprecationWarning("foo.attrvalues() is deprecated, use foo.attrs.values() instead"))
		return self.attrs.values()

	def attritems(self, xml=False):
		errors.warn(DeprecationWarning("foo.attritems() is deprecated, use foo.attrs.items() instead"))
		return self.attrs.items(xml=xml)

	def iterattrkeys(self, xml=False):
		errors.warn(DeprecationWarning("foo.iterattrkeys() is deprecated, use foo.attrs.iterkeys() instead"))
		return self.attrs.iterkeys(xml=xml)

	def iterattrvalues(self):
		errors.warn(DeprecationWarning("foo.iterattrvalues() is deprecated, use foo.attrs.itervalues() instead"))
		return self.attrs.itervalues()

	def iterattritems(self, xml=False):
		errors.warn(DeprecationWarning("foo.iterattritems() is deprecated, use foo.attrs.iteritems() instead"))
		return self.attrs.iteritems(xml=xml)

	def allowedattrkeys(cls, xml=False):
		errors.warn(DeprecationWarning("foo.allowedattrkeys() is deprecated, use foo.attrs.allowedkeys() instead"))
		return cls.Attrs.allowedkeys(xml=xml)
	allowedattrkeys = classmethod(allowedattrkeys)

	def allowedattrvalues(cls):
		errors.warn(DeprecationWarning("foo.allowedattrvalues() is deprecated, use foo.attrs.allowedvalues() instead"))
		return cls.Attrs.allowedvalues()
	allowedattrvalues = classmethod(allowedattrvalues)

	def allowedattritems(cls, xml=False):
		errors.warn(DeprecationWarning("foo.allowedattritems() is deprecated, use foo.attrs.alloweditems() instead"))
		return cls.Attrs.alloweditems(xml=xml)
	allowedattritems = classmethod(allowedattritems)

	def iterallowedattrkeys(cls, xml=False):
		errors.warn(DeprecationWarning("foo.iterallowedattrkeys() is deprecated, use foo.attrs.iterattrkeys() instead"))
		return cls.Attrs.iterallowedkeys(xml=xml)
	iterallowedattrkeys = classmethod(iterallowedattrkeys)

	def iterallowedattrvalues(cls):
		errors.warn(DeprecationWarning("foo.iterallowedattrvalues() is deprecated, use foo.attrs.iterattrvalues() instead"))
		return cls.Attrs.iterallowedvalues()
	iterallowedattrvalues = classmethod(iterallowedattrvalues)

	def iterallowedattritems(cls, xml=False):
		errors.warn(DeprecationWarning("foo.iterallowedattritems() is deprecated, use foo.attrs.iterattritems() instead"))
		return cls.Attrs.iteralloweditems(xml=xml)
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

	def __len__(self):
		"""
		return the number of children
		"""
		return len(self.content)

	def compact(self):
		node = self.__class__()
		node.content = self.content.compact()
		node.attrs = self.attrs.compact()
		return self._decoratenode(node)

	def find(self, type=None, subtype=False, attrs=None, test=None, searchchildren=False, searchattrs=False):
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

		errors.warn(DeprecationWarning("foo.copyDefaultAttrs() is deprecated, use foo.attrs.updateexisting() instead"))
		self.attrs.updateexisting(fromMapping)

	def withsep(self, separator, clone=False):
		"""
		<par>returns a version of <self/> with a separator node between the child nodes of <self/>.
		for more info see <pyref class="Frag" method="withsep"><method>Frag.withsep</method></pyref>.</par>
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.withsep(separator, clone)
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

	def mapped(self, converter):
		node = converter.function(self, converter)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = self.__class__(self.content.mapped(converter))
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

	def walk(self, before=True, after=False, attrs=False, attrbefore=True, attrafter=False):
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

	def walkpath(self, before=True, after=False, attrs=False, attrbefore=True, attrafter=False):
		if before:
			yield [self]
		if attrs:
			for child in self.attrs.values():
				if attrbefore:
					yield [self] + child
				for grandchildPath in child.walkpath(before, after, attrs, attrbefore, attrafter):
					yield [self] + grandchildPath
				if attrafter:
					yield [self] + child
		for child in self.content:
			for grandchildPath in child.walkpath(before, after, attrs, attrbefore, attrafter):
				yield [self] + grandchildPath
		if after:
			yield [self]

class Entity(Node):
	"""
	<par>Class for entities. Derive your own entities from
	it and overwrite <pyref class="Node" method="convert"><method>convert</method></pyref>
	and <pyref class="Node" method="__unicode__"><method>__unicode__</method></pyref>.</par>
	"""
	register = None

	class __metaclass__(Node.__metaclass__):
		def __new__(cls, name, bases, dict):
			self = Node.__metaclass__.__new__(cls, name, bases, dict)
			if self.register is not None:
				setattr(xmlns, name, self)
			return self

		def __repr__(self):
			return "<entity class %s/%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def _registerns(cls, ns):
		if cls.xmlns is not None:
			for xml in (False, True):
				del cls.xmlns._entities[xml][cls.xmlname[xml]]
			cls.xmlns = None
		if ns is not None:
			for xml in (False, True):
				ns._entities[xml][cls.xmlname[xml]] = cls
			cls.xmlns = ns
	_registerns = classmethod(_registerns)

	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strAmp())
		cls._strbase(presenters.strEntityName, s, fullname=fullname, xml=xml)
		if decorate:
			s.append(presenters.strSemi())
		return s
	_str = classmethod(_str)

	def clone(self):
		return self
	
	def compact(self):
		return self

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
				return cls.xmlns.xmlname[True]
			else:
				return publisher.prefixes.entityprefix4ns(cls.xmlns)[0]
	xmlprefix = classmethod(xmlprefix)

	def publish(self, publisher):
		publisher.publish(u"&")
		self._publishname(publisher)
		publisher.publish(u";")

class CharRef(Entity):
	"""
	<par>A simple character reference, the codepoint is in the class attribute
	<lit>codepoint</lit>.</par>
	"""
	register = None

	class __metaclass__(Entity.__metaclass__):
		def __new__(cls, name, bases, dict):
			self = Node.__metaclass__.__new__(cls, name, bases, dict)
			if self.register is not None:
				setattr(xmlns, name, self)
			return self

		def __repr__(self):
			return "<charref class %s/%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def _registerns(cls, ns):
		if cls.xmlns is not None:
			map = cls.xmlns._charrefs
			for xml in (False, True):
				del map[xml][cls.xmlname[xml]]
			l = map[2][cls.codepoint]
			if len(l)==1:
				del map[2][cls.codepoint]
			else:
				l.remove(cls)
		super(CharRef, cls)._registerns(ns)
		if ns is not None:
			map = ns._charrefs
			for xml in (False, True):
				map[xml][cls.xmlname[xml]] = cls
			map[2].setdefault(cls.codepoint, []).append(cls)
	_registerns = classmethod(_registerns)

	def convert(self, converter):
		node = Text(unichr(self.codepoint))
		return self._decoratenode(node)

	def __unicode__(self):
		return unichr(self.codepoint)

###
###
###

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
		<arg>ns</arg> must be a <pyref class="Namespace"><class>Namespace</class></pyref> class.</par>
		"""
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
		<arg>ns</arg> must be a <pyref class="Namespace"><class>Namespace</class></pyref> class.</par>
		<par>If <arg>prefix</arg> is not specified, all prefixes for
		the namespace <arg>ns</arg> will be removed. If <arg>ns</arg> is not specified
		all namespaces for the prefix <arg>prefix</arg> will be removed. If
		both are unspecified the mapping will be empty afterwards.</par>
		"""
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
		prefixes = []
		for (prefix, prefix2ns) in self._prefix2ns[type].iteritems():
			if prefix2ns and ns in prefix2ns[0]:
				prefixes.append(prefix)
		if prefixes:
			return prefixes
		else:
			return [ns.xmlname[True]]

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
		pos = qname.find(":")
		if pos>=0:
			return (qname[:pos], qname[pos+1:])
		else:
			return (None, qname) # no namespace specified

	def element(self, qname):
		"""
		<par>returns the element class for the name
		<arg>qname</arg> (which might include a prefix).</par>
		"""
		qname = self.__splitqname(qname)
		for ns in self.ns4elementprefix(qname[0]):
			try:
				element = ns.element(qname[1], xml=True)
				if element.register:
					return element
			except LookupError: # no element in this namespace with this name
				pass
		raise errors.IllegalElementError(qname, xml=True) # elements with this name couldn't be found

	def procinst(self, qname):
		"""
		<par>returns the processing instruction class for the name
		<arg>qname</arg> (which might include a prefix).</par>
		"""
		qname = self.__splitqname(qname)
		for ns in self.ns4procinstprefix(qname[0]):
			try:
				procinst = ns.procinst(qname[1], xml=True)
				if procinst.register:
					return procinst
			except LookupError: # no processing instruction in this namespace with this name
				pass
		raise errors.IllegalProcInstError(qname, xml=True) # processing instructions with this name couldn't be found

	def entity(self, qname):
		"""
		<par>returns the entity or charref class for the name
		<arg>qname</arg> (which might include a prefix).</par>
		"""
		qname = self.__splitqname(qname)
		for ns in self.ns4entityprefix(qname[0]):
			try:
				entity = ns.entity(qname[1], xml=True)
				if entity.register:
					return entity
			except LookupError: # no entity in this namespace with this name
				pass
		raise errors.IllegalEntityError(qname, xml=True) # entities with this name couldn't be found

	def charref(self, qname):
		"""
		<par>returns the first charref class for the name or codepoint <arg>qname</arg>.</par>
		"""
		if isinstance(qname, basestring):
			qname = self.__splitqname(qname)
			for ns in self.ns4entityprefix(qname[0]):
				try:
					charref = ns.charref(qname[1], xml=True)
					if charref.register:
						return charref
				except LookupError: # no entity in this namespace with this name
					pass
		else:
			for ns in Namespace.all:
				try:
					charref = ns.charref(qname)[0]
					if charref.register:
						return charref
				except LookupError:
					pass
		raise errors.IllegalCharRefError(qname, xml=True) # charref with this name/codepoint couldn't be found

	def attrnameFromQName(self, element, qname):
		"""
		<par>returns the Python name for an attribute for the qualified
		&xml; name <arg>qname</arg> (which might include a prefix, in which case
		a tuple with the namespace object and the name will be returned).</par>
		"""
		qname = self.__splitqname(qname)
		if qname[0] is None:
			return element.Attrs.allowedattr(qname[1], xml=True).xmlname[False]
		else:
			for ns in self.ns4elementprefix(qname[0]):
				try:
					attr = ns.Attrs.allowedattr(qname[1], xml=True)
					if attr.register:
						return (ns, attr.xmlname[False])
				except errors.IllegalAttrError: # no attribute in this namespace with this name
					pass
			raise errors.IllegalAttrError(None, qname, xml=True)

class OldPrefixes(Prefixes):
	"""
	<par>Prefix mapping that is compatible to the mapping used
	prior to &xist; version 2.0.</par>
	"""
	def __init__(self):
		super(OldPrefixes, self).__init__()
		for ns in Namespace.all:
			if ns.xmlurl == "http://www.w3.org/XML/1998/namespace":
				self.addElementPrefixMapping("xml", ns, mode="append")
				self.addProcInstPrefixMapping(None, ns, mode="append")
			else:
				self.addPrefixMapping(None, ns, mode="append")
				self.addPrefixMapping(ns.xmlname[True], ns, mode="append")

class DefaultPrefixes(Prefixes):
	"""
	<par>Prefix mapping that maps all defined namespace
	to their default prefix, except for one which is mapped
	to None.</par>
	"""
	def __init__(self, default=None):
		super(DefaultPrefixes, self).__init__()
		for ns in Namespace.all:
			if ns is default:
				self.addPrefixMapping(None, ns)
			else:
				self.addElementPrefixMapping(ns.xmlname[True], ns)
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

defaultPrefixes = Prefixes()

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
	def needsxmlns(self, publisher=None):
		return 2
	needsxmlns = classmethod(needsxmlns)

class Namespace(object):
	"""
	<par>an &xml; namespace, contains the classes for the elements,
	entities and processing instructions in the namespace.</par>
	"""

	xmlname = None
	xmlurl = None

	nsbyname = {}
	nsbyurl = {}
	all = []

	class __metaclass__(type):
		def __new__(cls, name, bases, dict):
			pyname = unicode(name.split(".")[-1])
			if "xmlname" in dict:
				xmlname = dict["xmlname"]
				if isinstance(xmlname, str):
					xmlname = unicode(xmlname)
			else:
				xmlname = pyname
			dict["xmlname"] = (pyname, xmlname)
			if "xmlurl" in dict:
				xmlurl = dict["xmlurl"]
				if xmlurl is not None:
					xmlurl = unicode(xmlurl)
				dict["xmlurl"] = xmlurl
			# automatically inherit all element, procinst, entity and Attrs classes, that aren't overwritten.
			for base in bases:
				for attrname in dir(base):
					attr = getattr(base, attrname)
					if isinstance(attr, type) and issubclass(attr, (Element, ProcInst, Entity, Attrs)) and attrname not in dict:
						classdict = {"__module__": dict["__module__"]}
						if attr.xmlname[0] != attr.xmlname[1]:
							classdict["xmlname"] = attr.xmlname[1]
						dict[attrname] = attr.__class__(attr.__name__, (attr, ), classdict)
			self = type.__new__(cls, name, bases, {})
			self._elements = ({}, {})
			self._procinsts = ({}, {})
			self._entities = ({}, {})
			self._charrefs = ({}, {}, {})
			for (key, value) in dict.iteritems():
				setattr(self, key, value)
			for attr in self.Attrs.iterallowedvalues():
				attr.xmlns = self
			if self.xmlurl is not None:
				self.nsbyname.setdefault(self.xmlname, []).insert(0, self)
				self.nsbyurl.setdefault(self.xmlurl, []).insert(0, self)
				self.all.append(self)
				defaultPrefixes.addPrefixMapping(None, self, mode="prepend")
				defaultPrefixes.addPrefixMapping(self.xmlname[True], self, mode="prepend")
			return self

		def __eq__(self, other):
			return self.xmlname[True]==other.xmlname[True] and self.xmlurl==other.xmlurl

		def __ne__(self, other):
			return not self==other

		def __hash__(self):
			return hash(self.xmlname[True]) ^ hash(self.xmlurl)

		def __repr__(self):
			counts = []

			keys = self.elementkeys()
			if keys:
				counts.append("%d elements" % len(keys))

			keys = self.procinstkeys()
			if keys:
				counts.append("%d procinsts" % len(keys))

			keys = self.entitykeys()
			if keys:
				counts.append("%d entities" % len(keys))

			keys = self.charrefkeys()
			if keys:
				counts.append("%d charrefs" % len(keys))

			allowedattrs = self.Attrs.allowedkeys()
			if len(allowedattrs):
				counts.append("%d attrs" % len(allowedattrs))

			if counts:
				counts = " with " + ", ".join(counts)
			else:
				counts = ""

			if self.__dict__.has_key("__file__"): # no inheritance
				fromfile = " from %r" % self.__file__
			else:
				fromfile = ""
			return "<namespace %s/%s name=%r url=%r%s%s at 0x%x>" % (self.__module__, self.__name__, self.xmlname[True], self.xmlurl, counts, fromfile, id(self))

		def __delattr__(cls, key):
			value = cls.__dict__.get(key, None) # no inheritance
			if isinstance(value, type) and issubclass(value, (Element, ProcInst, CharRef)):
				value._registerns(xmlns)
			return type.__delattr__(cls, key)

		def __setattr__(cls, key, value):
			oldvalue = cls.__dict__.get(key, None) # no inheritance
			if isinstance(oldvalue, type) and issubclass(oldvalue, (Element, ProcInst, Entity)):
				oldvalue._registerns(xmlns)
			if isinstance(value, type) and issubclass(value, (Element, ProcInst, Entity)):
				ns = value.__dict__.get("xmlns") # no inheritance
				if ns is not None:
					delattr(ns, key)
				value._registerns(cls)
			return type.__setattr__(cls, key, value)

	class Attrs(_Attrs):
		pass

	def iterelementkeys(cls, xml=False):
		return cls._elements[xml].iterkeys()
	iterelementkeys = classmethod(iterelementkeys)

	def elementkeys(cls, xml=False):
		return cls._elements[xml].keys()
	elementkeys = classmethod(elementkeys)

	def iterelementvalues(cls):
		return cls._elements[False].itervalues()
	iterelementvalues = classmethod(iterelementvalues)

	def elementvalues(cls):
		return cls._elements[False].values()
	elementvalues = classmethod(elementvalues)

	def iterelementitems(cls, xml=False):
		return cls._elements[xml].iteritems()
	iterelementitems = classmethod(iterelementitems)

	def elementitems(cls, xml=False):
		return cls._elements[xml].items()
	elementitems = classmethod(elementitems)

	def element(cls, name, xml=False):
		try:
			return cls._elements[xml][name]
		except KeyError:
			raise errors.IllegalElementError(name, xml=xml)
	element = classmethod(element)

	def iterprocinstkeys(cls, xml=False):
		return cls._procinsts[xml].iterkeys()
	iterprocinstkeys = classmethod(iterprocinstkeys)

	def procinstkeys(cls, xml=False):
		return cls._procinsts[xml].keys()
	procinstkeys = classmethod(procinstkeys)

	def iterprocinstvalues(cls):
		return cls._procinsts[False].itervalues()
	iterprocinstvalues = classmethod(iterprocinstvalues)

	def procinstvalues(cls):
		return cls._procinsts[False].values()
	procinstvalues = classmethod(procinstvalues)

	def iterprocinstitems(cls, xml=False):
		return cls._procinsts[xml].iteritems()
	iterprocinstitems = classmethod(iterprocinstitems)

	def procinstitems(cls, xml=False):
		return cls._procinsts[xml].items()
	procinstitems = classmethod(procinstitems)

	def procinst(cls, name, xml=False):
		try:
			return cls._procinsts[xml][name]
		except KeyError:
			raise errors.IllegalProcInstError(name, xml=xml)
	procinst = classmethod(procinst)

	def iterentitykeys(cls, xml=False):
		return cls._entities[xml].iterkeys()
	iterentitykeys = classmethod(iterentitykeys)

	def entitykeys(cls, xml=False):
		return cls._entities[xml].keys()
	entitykeys = classmethod(entitykeys)

	def iterentityvalues(cls):
		return cls._entities[False].itervalues()
	iterentityvalues = classmethod(iterentityvalues)

	def entityvalues(cls):
		return cls._entities[False].values()
	entityvalues = classmethod(entityvalues)

	def iterentityitems(cls, xml=False):
		return cls._entities[xml].iteritems()
	iterentityitems = classmethod(iterentityitems)

	def entityitems(cls, xml=False):
		return cls._entities[xml].items()
	entityitems = classmethod(entityitems)

	def entity(cls, name, xml=False):
		try:
			return cls._entities[xml][name]
		except KeyError:
			raise errors.IllegalEntityError(name, xml=xml)
	entity = classmethod(entity)

	def itercharrefkeys(cls, xml=False):
		return cls._charrefs[xml].iterkeys()
	itercharrefkeys = classmethod(itercharrefkeys)

	def charrefkeys(cls, xml=False):
		return cls._charrefs[xml].keys()
	charrefkeys = classmethod(charrefkeys)

	def itercharrefvalues(cls):
		return cls._charrefs[False].itervalues()
	itercharrefvalues = classmethod(itercharrefvalues)

	def charrefvalues(cls):
		return cls._charrefs[False].values()
	charrefvalues = classmethod(charrefvalues)

	def itercharrefitems(cls, xml=False):
		return cls._charrefs[xml].iteritems()
	itercharrefitems = classmethod(itercharrefitems)

	def charrefitems(cls, xml=False):
		return cls._charrefs[xml].items()
	charrefitems = classmethod(charrefitems)

	def charref(cls, name, xml=False):
		try:
			if isinstance(name, (int, long)):
				return cls._charrefs[2][name]
			else:
				return cls._charrefs[xml][name]
		except KeyError:
			raise errors.IllegalCharRefError(name, xml=xml)
	charref = classmethod(charref)

	def addvars(cls, vars):
		for (key, value) in vars.iteritems():
			if value is not cls and key not in ("__name__", "__dict__"):
				setattr(cls, key, value)
	addvars = classmethod(addvars)

	def makemod(cls, vars=None):
		if vars is not None:
			cls.addvars(vars)
		# we have to keep the original module alive, otherwise Python would set all module attribute to None
		cls.__originalmodule__ = sys.modules[vars["__name__"]]
		sys.modules[vars["__name__"]] = cls
	makemod = classmethod(makemod)

	def __init__(self, xmlprefix, xmlname, thing=None):
		raise TypeError("Namespace classes can't be instantiated")

class xmlns(Namespace):
	xmlname = None
	xmlurl = None

# C0 Controls and Basic Latin
class quot(CharRef): "quotation mark = APL quote, U+0022 ISOnum"; codepoint = 34
class amp(CharRef): "ampersand, U+0026 ISOnum"; codepoint = 38
class lt(CharRef): "less-than sign, U+003C ISOnum"; codepoint = 60
class gt(CharRef): "greater-than sign, U+003E ISOnum"; codepoint = 62
class apos(CharRef): "apostrophe mark, U+0027 ISOnum"; codepoint = 39

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
