#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
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
import url
import presenters, publishers, converters, errors, options, utils, helpers

###
### helpers
###

def ToNode(value):
	"""
	<doc:par>convert the <arg>value</arg> passed in to an &xist; <pyref class="Node"><class>Node</class></pyref>.</doc:par>

	<doc:par>If <arg>value</arg> is a tuple or list, it will be (recursively) converted
	to a <pyref class="Frag"><class>Frag</class></pyref>. Integers, strings, etc. will be converted to a
	<pyref class="Text"><class>Text</class></pyref>.
	If <arg>value</arg> is a <pyref class="Node"><class>Node</class></pyref> already, nothing will be done.
	In the case of <code>None</code> the XSC Null (<class>xsc.Null</class>) will be returned).
	Anything else raises an exception.</doc:par>
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

class Node(object):
	"""
	base class for nodes in the document tree. Derived classes must
	overwrite <pyref module="xist.xsc" class="Node" method="convert"><method>convert</method></pyref>
	and may overwrite <pyref module="xist.xsc" class="Node" method="publish"><method>publish</method></pyref>
	and <pyref module="xist.xsc" class="Node" method="__unicode__"><method>__unicode__</method></pyref>.
	"""
	empty = 1

	# location of this node in the XML file (will be hidden in derived classes, but is
	# specified here, so that no special tests are required. In derived classes
	# this will be set by the parser)
	startLoc = None
	endLoc = None

	# specifies if a prefix should be presented or published. Can be 0 or 1 or None
	# which mean use the default
	presentPrefix = None
	publishPrefix = None

	# specifies that this class should be registered in a namespace
	# this won't be used for all the DOM classes (Element, ProcInst etc.) themselves but only for derived classes
	# i.e. Node, Element etc. will never be registered

	def __repr__(self):
		return self.repr(presenters.defaultPresenterClass())

	def __ne__(self, other):
		return not self==other

	def clone(self):
		"""
		returns an identical clone of the node and it's children.
		"""
		raise NotImplementedError("clone method not implemented in %s" % self.__class__.__name__)

	class __metaclass__(type):
		def __new__(cls, name, bases, dict):
			try:
				realname = dict["name"]
			except KeyError:
				realname = name
				if realname.endswith("_"):
					realname = realname[:-1]
			dict["name"] = unicode(realname)
			if not dict.has_key("register"):
				dict["register"] = 1
			return type.__new__(cls, name, bases, dict)

	def namespace(cls):
		"""
		return the namespace object for this class or None.
		"""
		return getattr(cls, "_namespace", None)
	namespace = classmethod(namespace)

	def prefix(cls):
		"""
		return the namespace prefix for this class or the
		module name, if there is no namespace.
		"""
		ns = cls.namespace()
		if ns is not None:
			return ns.prefix
		else:
			return unicode(cls.__module__)
	prefix = classmethod(prefix)

	def repr(self, presenter=None):
		"""
		<doc:par>Return a string representation of <self/>.
		When you don't pass in a <arg>presenter</arg>, you'll
		get the default presentation. Else <arg>presenter</arg>
		should be an instance of <pyref module="xist.presenters" class="Presenter"><class>xist.presenters.Presenter</class></pyref>
		(or one of the subclasses).</doc:par>
		"""
		if presenter is None:
			presenter = presenters.defaultPresenterClass()
		presenter.beginPresentation()
		self.present(presenter)
		return presenter.endPresentation()

	def present(self, presenter):
		"""
		<doc:par><method>present</method> is used as a central
		dispatch method for the <pyref module="xist.presenters">presenter classes</pyref>.
		Normally it is not called by the user, but internally by the
		presenter. The user should call <pyref method="repr"><method>repr</method></pyref>
		instead.</doc:par>
		"""
		raise NotImplementedError("present method not implemented in %s" % self.__class__.__name__)

	def conv(self, converter=None, root=None, mode=None, stage=None, target=None, lang=None, makeaction=None, maketarget=None):
		"""
		<doc:par>returns a version of this node and it's content converted to &html; (or any other target).</doc:par>
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
		<doc:par>implementation of the conversion method.
		When you define your own element classes you have to overwrite this method.</doc:par>

		<doc:par>E.g. when you want to define an element that packs it's content into an &html;
		bold element, do the following:

		<doc:programlisting>
		class foo(xsc.Element):
			empty = 0

			def convert(self, converter):
				return html.b(self.content).convert(converter)
		</doc:programlisting>
		</doc:par>
		"""
		raise NotImplementedError("convert method not implemented in %s" % self.__class__.__name__)

	def __unicode__(self):
		"""
		<doc:par>returns this node as a (unicode) string.
		Comments and processing instructions will be filtered out.
		For elements you'll get the element content.</doc:par>

		<doc:par>It might be useful to overwrite this function in your own
		elements. Suppose you have the following element:
		<doc:programlisting>
		class caps(xsc.Element):
			empty = 0

			def convert(self, converter):
				return html.span(
					self.content.convert(converter),
					style="font-variant: small-caps;"
				)
		</doc:programlisting>

		that renders its content in small caps, then it might be useful
		to define <method>__unicode__</method> in the following way:
		<doc:programlisting>
		def __unicode__(self):
			return unicode(self.content).upper()
		</doc:programlisting>

		<method>__unicode__</method> can be used everywhere, where
		a plain string representation of the node is required.</doc:par>
		"""
		raise NotImplementedError("__unicode__ method not implemented in %s" % self.__class__.__name__)

	def asPlainString(self):
		errors.warn(DeprecationWarning("asPlainString() is deprecated, use unicode() (or str()) instead"))
		return unicode(self)

	def __str__(self):
		return str(unicode(self))

	def asText(self, monochrome=1, squeezeBlankLines=0, lineNumbers=0, cols=80):
		"""
		<doc:par>Return the node as a formatted plain &ascii; string.
		Note that this really only make sense for &html; trees.</doc:par>

		<doc:par>This requires that <app moreinfo="http://w3m.sf.net/">w3m</app> is installed.</doc:par>
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
		<doc:par>returns this node converted to a float. <arg>decimal</arg>
		specifies which decimal separator is used in the value
		(e.g. <lit>"."</lit> (the default) or <code>","</code>).
		<arg>ignore</arg> specifies which character will be ignored.</doc:par>
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

	def publish(self, publisher):
		"""
		<doc:par>generates unicode strings for the node, and passes
		the strings to the callable object <arg>publisher</arg>.</doc:par>

		<doc:par>The encoding and xhtml specification are taken from the <arg>publisher</arg>.</doc:par>
		"""
		raise NotImplementedError("publish method not implemented in %s" % self.__class__.__name__)

	def asString(self, base=None, root=None, xhtml=None, publishPrefix=0):
		"""
		<doc:par>returns this element as a unicode string.</doc:par>

		<doc:par>For an explanation of <arg>xhtml</arg> and <arg>publishPrefix</arg>
		see <pyref method="publish"><method>publish</method></pyref>.</doc:par>
		"""
		publisher = publishers.StringPublisher(base=base, root=root, xhtml=xhtml, publishPrefix=publishPrefix)
		self.publish(publisher)
		return publisher.asString()

	def asBytes(self, base=None, root=None, encoding=None, xhtml=None, publishPrefix=0):
		"""
		<doc:par>returns this element as a byte string suitable for writing
		to an &html; file or printing from a CGI script.</doc:par>

		<doc:par>For the parameters see <pyref method="publish"><method>publish</method></pyref>.</doc:par>
		"""
		publisher = publishers.BytePublisher(base=base, root=root, encoding=encoding, xhtml=xhtml, publishPrefix=publishPrefix)
		self.publish(publisher)
		return publisher.asBytes()

	def write(self, stream, base=None, root=None, encoding=None, xhtml=None, publishPrefix=0):
		"""
		<doc:par>writes the element to the file like object <arg>file</arg>.</doc:par>

		<doc:par>For the rest of the parameters see <pyref method="publish"><method>publish</method></pyref>.</doc:par>
		"""
		publisher = publishers.FilePublisher(stream, base=base, root=root, encoding=encoding, xhtml=xhtml, publishPrefix=publishPrefix)
		self.publish(publisher)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		"""
		<doc:par>returns a fragment which contains child elements of this node.</doc:par>

		<doc:par>If you specify <arg>type</arg> as the class of an XSC node only nodes
		of this class will be returned. If you pass a list of classes, nodes that are an
		instance of one of the classes will be returned.</doc:par>

		<doc:par>If you set <arg>subtype</arg> to <lit>1</lit> nodes that are a
		subtype of <arg>type</arg> will be returned too.</doc:par>

		<doc:par>If you pass a dictionary as <arg>attrs</arg> it has to contain
		string pairs and is used to match attribute values for elements. To match
		the attribute values their <pyref class="Node" method="__unicode__"><method>__unicode__</method></pyref>
		representation will be used. You can use <lit>None</lit> as the value to test that
		the attribute is set without testing the value.</doc:par>

		<doc:par>Additionally you can pass a test function in <arg>test</arg>, that
		returns <lit>1</lit>, when the node passed in has to be included in the
		result and <lit>0</lit> otherwise.</doc:par>

		<doc:par>If you set <arg>searchchildren</arg> to <lit>1</lit> not only
		the immediate children but also the grandchildren will be searched for nodes
		matching the other criteria.</doc:par>

		<doc:par>If you set <arg>searchattrs</arg> to <lit>1</lit> the attributes
		of the nodes (if <arg>type</arg> is <pyref class="Element"><class>Element</class></pyref>
		or one of its subtypes) will be searched too.</doc:par>

		<doc:par>Note that the node has to be of type <pyref class="Element"><class>Element</class></pyref>
		(or a subclass of it) to match <arg>attrs</arg>.</doc:par>
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
		<doc:par>decorate the <pyref class="Node"><class>Node</class></pyref>
		<arg>node</arg> with the same location information as <self/>.</doc:par>
		"""

		node.startLoc = self.startLoc
		node.endLoc = self.endLoc
		return node

	def _publishName(self, publisher):
		if self.publishPrefix is not None:
			publishPrefix = self.publishPrefix
		else:
			publishPrefix = publisher.publishPrefix
		prefix = self.prefix()
		if publishPrefix and prefix is not None:
			publisher.publish(prefix)
			publisher.publish(u":")
		publisher.publish(self.name)

	def mapped(self, function):
		"""
		<doc:par>returns the node mapped through the function <arg>function</arg>.
		This call works recursively (for <pyref class="Frag"><class>Frag</class></pyref>
		and <pyref class="Element"><class>Element</class></pyref>).</doc:par>
		<doc:par>When you want an unmodified node you simply can return <self/>. <method>mapped</method>
		will make a copy of it and fill the content recursively. Note that element attributes
		will not be mapped. When you return a different node from <function>function</function>
		this node will be incorporated into the result as-is.</doc:par>
		"""
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		return node

	def normalized(self):
		"""
		<doc:par>return a normalized version of <self/>, which means, that consecutive
		<pyref class="Text"><class>Text</class> nodes</pyref> are merged.</doc:par>
		"""
		return self

	def __mul__(self, factor):
		"""
		<doc:par>return a <pyref class="Frag"><class>Frag</class></pyref> with <arg>factor</arg> times
		the node as an entry. Note that the node will not be copied, i.e. it is a
		<z>shallow <method>__mul__</method></z>.</doc:par>
		"""
		return Frag(*factor*[self])

	def __rmul__(self, factor):
		"""
		<doc:par>returns a <pyref class="Frag"><class>Frag</class></pyref> with <arg>factor</arg> times
		the node as an entry.</doc:par>
		"""
		return Frag(*[self]*factor)

	def pretty(self, level=0, indent="\t"):
		"""
		<doc:par>Returns a prettyfied version of <self/>, i.e. one with
		properly nested and indented tags (as far as possible). If an element
		has mixed content (i.e. <pyref class="Text"><class>Text</class></pyref> and
		non-<pyref class="Text"><class>Text</class></pyref> nodes) the content will be
		returned as is.</doc:par>
		<doc:par>Note that whitespace will prevent pretty printing too, so
		you might want to call <pyref method="normalized"><method>normalized</method></pyref>
		and <pyref method="compact"><method>compact</method></pyref> before
		calling <method>pretty</method> to remove whitespace.</doc:par>
		"""
		if level==0:
			return self
		else:
			return Frag(indent*level, self)

	def walk(self, before=1, after=0):
		"""
		<doc:par>walk the tree. This method is a generator.</doc:par>
		<doc:par>For nodes that have content (like
		<pyref class="Frag"><class>Frag</class>s</pyref> and
		<pyref class="Element"><class>Element</class>s</pyref>)
		it's possible to specify if the should be <lit>yield</lit>ed
		before or after there children (or both, or none
		in which case only leaf nodes will be <lit>yield</lit>ed).</doc:par>
		"""
		yield self

	def walkPath(self, before=1, after=0):
		"""
		<doc:par>walk the tree. This method is a generator and for each node
		in the tree generates a list with the <z>path</z> to the node, i.e.
		the node and all its ancestor nodes.</doc:par>
		<doc:par>For <arg>before</arg> and <arg>after</arg> see
		<pyref method="walk"><method>walk</method></pyref>.</doc:par>
		"""
		yield [self]

class CharacterData(Node):
	"""
	<doc:par>base class for &xml; character data (text, proc insts, comment, doctype etc.)</doc:par>

	<doc:par>provides nearly the same functionality as <class>UserString</class>,
	but omits a few methods.</doc:par>
	"""

	def __init__(self, content=u""):
		self.__content = unicode(content)

	def __getContent(self):
		return self.__content

	content = property(__getContent, None, None, "<doc:par>The text content of the node as a <class>unicode</class> object.</doc:par>")

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
	<doc:par>text node. The characters <markup>&lt;</markup>, <markup>&gt;</markup>, <markup>&amp;</markup>
	(and <markup>"</markup> inside attributes) will be <z>escaped</z> with the
	appropriate character entities when this node is published.</doc:par>
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
	<doc:par>A fragment contains a list of nodes and can be used for dynamically constructing content.
	The member <lit>content</lit> of an <pyref class="Element"><class>Element</class></pyref> is a <class>Frag</class>.</doc:par>
	"""

	empty = 0

	def __init__(self, *content):
		list.__init__(self)
		for child in content:
			child = ToNode(child)
			if isinstance(child, Frag):
				list.extend(self, child)
			elif child is not Null:
				list.append(self, child)

	def convert(self, converter):
		node = self.__class__() # virtual constructor => attributes (which are derived from Frag) will be handled correctly)
		for child in self:
			convertedchild = child.convert(converter)
			assert isinstance(convertedchild, Node), "the convert method returned the illegal object %r (type %r) when converting %r" % (convertedchild, type(convertedchild), self)
			node.append(convertedchild)
		return self._decorateNode(node)

	def clone(self):
		node = self.__class__() # virtual constructor => attributes (which are derived from Frag) will be handled correctly)
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
		<doc:par>Return the <arg>index</arg>'th node for the content of the fragment.
		If <arg>index</arg> is a list <method>__getitem__</method> will work
		recursively. If <arg>index</arg> is an empty list, <self/> will be returned.</doc:par>
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
		<doc:par>Allows you to replace the <arg>index</arg>'th content node of the fragment
		with the new value <arg>value</arg> (which will be converted to a node).
		If  <arg>index</arg> is a list <method>__setitem__</method> will be applied
		to the innermost index after traversing the rest of <arg>index</arg> recursively.
		If <arg>index</arg> is an empty list, the call will be ignored.</doc:par>
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
		<doc:par>Remove the <arg>index</arg>'th content node from the fragment.
		If <arg>index</arg> is a list, the innermost index will be deleted,
		after traversing the rest of <arg>index</arg> recursively.
		If <arg>index</arg> is an empty list the call will be ignored.</doc:par>
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
		node = self.__class__()
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
		node = self.__class__()
		list.extend(node, list.__mul__(self, factor))
		return node

	def __rmul__(self, factor):
		"""
		returns a <pyref class="Frag"><class>Frag</class></pyref> with <arg>factor</arg> times
		the content of <self/>.
		"""
		node = self.__class__()
		list.extend(node, list.__mul__(factor, self))
		return node

	def __nonzero__(self):
		"""
		<doc:par>return whether this fragment is not empty.</doc:par>
		"""
		return len(self) != 0

	# no need to implement __len__

	def append(self, *others):
		"""
		<doc:par>append all items in <arg>others</arg> to <self/>.</doc:par>
		"""
		for other in others:
			other = ToNode(other)
			if isinstance(other, Frag):
				list.extend(self, other)
			elif other is not Null:
				list.append(self, other)

	def insert(self, index, *others):
		"""
		<doc:par>inserts all items in <arg>others</arg> at the position <arg>index</arg>.
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
		node = self.__class__()
		for child in self:
			compactedchild = child.compact()
			assert isinstance(compactedchild, Node), "the compact method returned the illegal object %r (type %r) when compacting %r" % (compactedchild, type(compactedchild), child)
			if compactedchild is not Null:
				list.append(node, compactedchild)
		return self._decorateNode(node)

	def withSep(self, separator, clone=0):
		"""
		<doc:par>return a version of <self/> with a separator node between the nodes of <self/>.</doc:par>

		<doc:par>if <lit><arg>clone</arg>==0</lit> one node will be inserted several times,
		if <lit><arg>clone</arg>==1</lit> clones of this node will be used.</doc:par>
		"""
		node = Frag()
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
		<doc:par>returns a sorted version of the <self/>. <arg>compare</arg> is
		a comparison function returning -1, 0, 1 respectively and defaults to comparing the
		<pyref class="Node" method="__unicode__"><class>__unicode__</class></pyref> value.</doc:par>
		"""
		node = Frag()
		list.extend(node, list.__getslice__(self, 0, sys.maxint))
		list.sort(node, compare)
		return node

	def reversed(self):
		"""
		<doc:par>returns a reversed version of the <self/>.</doc:par>
		"""
		node = Frag()
		list.extend(node, list.__getslice__(self, 0, sys.maxint))
		list.reverse(node)
		return node

	def filtered(self, function):
		"""
		<doc:par>returns a filtered version of the <self/>.</doc:par>
		"""
		node = Frag()
		list.extend(node, [ child for child in self if function(child) ])
		return node

	def shuffled(self):
		"""
		<doc:par>return a shuffled version of <self/>.</doc:par>
		"""
		content = list.__getslice__(self, 0, sys.maxint)
		node = Frag()
		while content:
			index = random.randrange(len(content))
			list.append(node, content[index])
			del content[index]
		return node

	def mapped(self, function):
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = Frag(*[ child.mapped(function) for child in self])
		return node

	def normalized(self):
		node = Frag()
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
		node = Frag()
		i = 0
		for child in self:
			if i:
				node.append("\n")
			node.append(child.pretty(level, indent))
			i += 1
		return node

	def walk(self, before=1, after=0):
		if before:
			yield self
		for child in self:
			for grandchild in child.walk(before, after):
				yield grandchild
		if after:
			yield self

	def walkPath(self, before=1, after=0):
		if before:
			yield [self]
		for child in self:
			for grandchildPath in child.walkpath(before, after):
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
	<doc:par>Class for processing instruction. This class is abstract.</doc:par>

	<doc:par>Processing instruction with the target <code>xml</code> will be
	handled by the derived class <pyref module="xist.xsc" class="XML"><class>XML</class></pyref>.
	All other processing instructions will be handled
	by other classes derived from <class>ProcInst</class>.</doc:par>
	"""

	# we don't need a constructor, because we don't have to store the target,
	# because the target is our classname (or the class attribute name)

	def convert(self, converter):
		return self

	def clone(self):
		return self

	compact = clone

	def present(self, presenter):
		presenter.presentProcInst(self)

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

class XML(ProcInst):
	"""
	&xml; header
	"""

	name = u"xml"
	presentPrefix = 0
	publishPrefix = 0

	def publish(self, publisher):
		content = self.content
		encodingfound = utils.findAttr(content, u"encoding")
		versionfound = utils.findAttr(content, u"version")
		standalonefound = utils.findAttr(content, u"standalone")
		if publisher.encoding != encodingfound: # if self has the wrong encoding specification (or none), we construct a new XML ProcInst and publish that (this doesn't lead to infinite recursion, because the next call will skip it)
			node = XML(u"version='" + versionfound + u"' encoding='" + publisher.encoding + u"'")
			if standalonefound is not None:
				node += u" standalone='" + standalonefound + u"'"
			node.publish(publisher)
			return
		ProcInst.publish(self, publisher)

class XML10(XML):
	"""
	&xml; header version 1.0, i.e. <markup>&lt;?xml version="1.0"?&gt;</markup>
	"""
	name = u"xml10"
	register = 0 # don't register this ProcInst, because it will never be parsed from a file, this is just a convenience class

	def __init__(self):
		XML.__init__(self, 'version="1.0"')

class XMLStyleSheet(ProcInst):
	"""
	XML stylesheet declaration
	"""

	name = u"xml-stylesheet"
	presentPrefix = 0
	publishPrefix = 0

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

class Attr(Frag):
	r"""
	<doc:par>Base classes of all attribute classes.</doc:par>

	<doc:par>The content of an attribute may be any other XSC node. This is different from
	a normal &dom;, where only text and character references are allowed. The reason for
	this is to allow dynamic content (implemented as elements or processing instructions)
	to be put into attributes.</doc:par>

	<doc:par>Of course, this dynamic content when finally converted to &html; will normally result in
	a fragment consisting only of text and character references. But note that it is allowed
	to have elements and processing instructions inside of attributes even when publishing.
	Processing instructions will be published as is and for elements their content will be
	published.</doc:par>
	<doc:example title="Elements inside attributes">
	<doc:programlisting>
	&gt;&gt;&gt; from xist.ns import html
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
	</doc:programlisting>
	</doc:example>
	"""

	def present(self, presenter):
		presenter.presentAttr(self)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		publisher.inAttr += 1
		publisher.pushTextFilter(helpers.escapeAttr)
		Frag.publish(self, publisher)
		publisher.popTextFilter()
		publisher.inAttr -= 1

	def __lt__(self, other):
		return unicode(self) < other

	def __le__(self, other):
		return unicode(self) <= other

	def __eq__(self, other):
		return unicode(self) == other

	def __ne__(self, other):
		return unicode(self) != other

	def __gt__(self, other):
		return unicode(self) > other

	def __ge__(self, other):
		return unicode(self) >= other

	def pretty(self, level=0, indent="\t"):
		return self.clone()

class TextAttr(Attr):
	"""
	<doc:par>Attribute class that is used for normal text attributes.</doc:par>
	"""

class NumberAttr(Attr):
	"""
	<doc:par>Attribute class that is used for normal number attributes.</doc:par>
	"""

class IntAttr(NumberAttr):
	"""
	<doc:par>Attribute class that is used for normal integer attributes.</doc:par>
	"""

class FloatAttr(NumberAttr):
	"""
	<doc:par>Attribute class that is used for normal float attributes.</doc:par>
	"""

class BoolAttr(Attr):
	"""
	<doc:par>Attribute class that is used for boolean attributes.</doc:par>
	"""

class ColorAttr(Attr):
	"""
	<doc:par>Attribute class that is used for a color attributes.</doc:par>
	"""

class URLAttr(Attr):
	"""
	Attribute class that is used for URLs.

	XSC has one additional feature, path markers (these are directory names starting with *).
	An URL starting with a path marker is relative to the directory marked with the same path
	marker in the appropriate base URL.

	With this feature you don't have to remember how deeply you've nested your XSC file tree, you
	can specify a file from everywhere via "*/dir/to/file.xsc". XSC will change this to an URL
	that correctly locates the file (e.g. "../../../dir/to/file.xsc", when you're currenty nested three levels
	deep in a different directory than "dir".

	Server relative URLs will be shown with the pseudo scheme "server". For checking these URLs
	for image or file size, a http request will be made to the server specified in the server
	option (options.server).

	For all other URLs a normal request will be made corresponding to the specified scheme
	(http, ftp, etc.)
	"""

	def present(self, presenter):
		presenter.presentURLAttr(self)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		new = utils.replaceInitialURL(self, publisher._publishableURL)
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

class Attrs(Node, dict):
	"""
	<doc:par>An attribute map</doc:par>
	"""

	def __init__(self, handlers):
		dict.__init__(self)
		self.handlers = handlers

	def __eq__(self, other):
		return self.__class__ is other.__class__ and dict.__eq__(self, other)

	def clone(self):
		node = self.__class__(self.handlers)
		for (key, value) in dict.items(self):
			### dict.__setitem__(node, key, value.clone())
			dict.__setitem__(node, key, value)
		return node

	def convert(self, converter):
		node = self.__class__(self.handlers) # "virtual" constructor
		for (attrname, attrvalue) in dict.items(self):
			if len(attrvalue):
				convertedattr = attrvalue.convert(converter)
				assert isinstance(convertedattr, Node), "the convert method returned the illegal object %r (type %r) when converting the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
				node[attrname] = convertedattr
		return node

	def compact(self):
		node = self.__class__(self.handlers)
		for (attrname, attrvalue) in dict.items(self):
			if len(attrvalue):
				convertedattr = attrvalue.compact()
				assert isinstance(convertedattr, Node), "the compact method returned the illegal object %r (type %r) when compacting the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
				node[attrname] = convertedattr
		return node

	def normalized(self):
		node = self.__class__(self.handlers)
		for (attrname, attrvalue) in dict.items(self):
			if len(attrvalue):
				convertedattr = attrvalue.normalized()
				assert isinstance(convertedattr, Node), "the normalized method returned the illegal object %r (type %r) when normalizing the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
				node[attrname] = convertedattr
		return node

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		if searchattrs:
			for attrvalue in dict.values(self):
				if len(attrvalue):
					node.append(attrvalue.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def present(self, presenter):
		presenter.presentAttrs(self)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		for (attrname, attrvalue) in dict.items(self):
			if len(attrvalue):
				publisher.publish(u" ")
				publisher.publish(attrname)
				if isinstance(attrvalue, BoolAttr):
					if publisher.xhtml>0:
						publisher.publish(u"=\"")
						publisher.publish(attrname)
						publisher.publish(u"\"")
				else:
					publisher.publish(u"=\"")
					attrvalue.publish(publisher)
					publisher.publish(u"\"")

	def __unicode__(self):
		return u""

	def __getitem__(self, key):
		if key.endswith("_"):
			key = key[:-1]
		# we're returning the packed attribute here, because otherwise there would be no possibility to get an expanded URL
		try:
			attr = dict.__getitem__(self, key)
		except KeyError: # if the attribute is not there generate an empty one ...
			try:
				attr = self.handlers[key]()
			except KeyError: # ... if we can
				raise errors.IllegalAttrError(self, key)
			dict.__setitem__(self, key, attr)
		return attr

	def __setitem__(self, key, value):
		if key.endswith("_"):
			key = key[:-1]
		# values are constructed via the attribute classes specified in the handlers dictionary, which does the conversion
		try:
			attr = self.handlers[key](value) # create an empty attribute of the right type
		except KeyError:
			raise errors.IllegalAttrError(self, key)
		dict.__setitem__(self, key, attr) # put the attribute in our dict

	def __delitem__(self, key):
		if key.endswith("_"):
			key = key[:-1]
		try:
			dict.__delitem__(self, key)
		except KeyError: # ignore non-existing attributes (but only if the name is in self.handlers.keys())
			if key not in self.handlers:
				raise errors.IllegalAttrError(self, key)

	def has(self, key):
		try:
			attr = dict.__getitem__(self, key)
		except KeyError:
			return 0
		return len(attr)>0

	def get(self, key, default=None):
		attr = self[key]
		if attr:
			return attr
		else:
			return self.handlers[key](default) # pack the attribute into an attribute object

	def setdefault(self, key, default=None):
		attr = self[key]
		if not attr:
			attr = self.handlers[key](default) # pack the attribute into an attribute object
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

	def keys(self):
		return [ key for (key, value) in dict.items(self) if len(value) ]

	def values(self):
		return [ value for value in dict.values(self) if len(value) ]

	def items(self):
		return [ kv for kv in dict.items(self) if len(kv[1]) ]

	def without(self, nameseq):
		"""
		<doc:par>Return a copy of <self/> where all the names in <arg>nameseq</arg> are
		removed. A name in <arg>nameseq</arg> that is not in <self/> will not raise
		an exception.</doc:par>
		"""
		node = self.__class__(self.handlers)
		for (key, value) in dict.items(self):
			if not key in nameseq:
				dict.__setitem__(node, key, value)
		return node

class Element(Node):
	"""
	<doc:par>This class represents &xml;/&xist; elements. All elements
	implemented by the user must be derived from this class.</doc:par>

	<doc:par>If you not only want to construct a &dom; tree via a Python script
	(by directly instantiating these classes), but to read an &xml; file
	you must register the element class with the parser, this can be done
	by creating <pyref module="xist.xsc" class="Namespace"><class>Namespace</class></pyref>
	objects.</doc:par>

	<doc:par>Every element class should have two class variables:
	<lit>empty</lit>: this is either <lit>0</lit> or <lit>1</lit>
	and specifies whether the element type is allowed to have content
	or not. Note that the parser does not use this as some sort of
	static DTD, i.e. you still must write your empty tags
	like this: <markup>&lt;foo/&gt;</markup>.</doc:par>

	<doc:par><lit>attrHandlers</lit> is a dictionary that maps attribute
	names to attribute classes, which are all derived from
	<pyref class="Attr"><class>Attr</class></pyref>.
	Assigning to an attribute with a name that is not in
	<lit>attrHandlers.keys()</lit> is an error.</doc:par>
	"""

	empty = 1 # 0 => element with content; 1 => stand alone element
	attrHandlers = {} # maps attribute names to attribute classes

	def __init__(self, *content, **attrs):
		"""
		<doc:par>Create a new <class>Element</class> instance.</doc:par>
		
		<doc:par>positional arguments are treated as content nodes.
		keyword arguments and dictionaries are treated as attributes.</doc:par>
		"""
		self.attrs = Attrs(self.attrHandlers)
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

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.content==other.content and self.attrs==other.attrs

	def append(self, *items):
		"""
		<doc:par>appends to content (see <pyref class="Frag" method="append"><method>Frag.append</method></pyref>
		for more info)</doc:par>
		"""

		self.content.append(*items)
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def insert(self, index, *items):
		"""
		<doc:par>inserts into the content (see <pyref class="Frag" method="insert"><method>Frag.insert</method></pyref>
		for more info)</doc:par>
		"""
		self.content.insert(index, *items)
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

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
		<doc:par>add width and height attributes to the element for the image that can be found in the attribute
		<arg>imgattr</arg>. If the attributes are already there, they are taken as a formatting
		template with the size passed in as a dictionary with the keys <lit>"width"</lit> and <lit>"height"</lit>,
		i.e. you could make your image twice as wide with <lit>width="%(width)d*2"</lit>.</doc:par>

		<doc:par>Passing <lit>None</lit> as <arg>widthattr</arg> or
		<arg>heightattr</arg> will prevent the respective attributes
		from being modified in any way.</doc:par>
		"""

		if self.hasAttr(imgattr):
			attr = self[imgattr]
			size = attr.imagesize(root)
			if size is not None: # the size was retrieved so we can use it
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
								errors.warn(errors.ImageSizeFormatWarning(self, attr, unicode(self[attr]), exc))
								del self[attr]
						else:
							self[attr] = size[attr==heightattr]

	def present(self, presenter):
		presenter.presentElement(self)

	def publish(self, publisher):
		if publisher.inAttr:
			# publish the content only, when we are inside an attribute
			# this works much like using the plain string value, but
			# even works with processing instructions, or what the Entity &xist; returns
			self.content.publish(publisher)
		else:
			publisher.publish(u"<")
			self._publishName(publisher)
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
		if isinstance(index, (str, unicode)):
			return self.attrs[index]
		else:
			return self.content[index]

	def __setitem__(self, index, value):
		"""
		<doc:par>sets an attribute or one of the content nodes depending on whether
		an 8bit or unicode string (i.e. attribute name) or a number or list (i.e.
		content node index) is passed in.</doc:par>
		"""
		if isinstance(index, (str, unicode)):
			self.attrs[index] = value
		else:
			self.content[index] = value

	def __delitem__(self, index):
		"""
		removes an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number or list (i.e. content node index) is passed in.
		"""
		if isinstance(index, (str, unicode)):
			del self.attrs[index]
		else:
			del self.content[index]

	def hasAttr(self, attrname):
		"""
		<doc:par>return whether <self/> has an attribute named <arg>attr</arg>.</doc:par>
		"""
		return self.attrs.has(attrname)

	def getAttr(self, attrname, default=None):
		"""
		<doc:par>works like the dictionary method <method>get</method>,
		it returns the attribute with the name <arg>attrname</arg>,
		or if <self/> has no such attribute, <arg>default</arg>
		(after converting it to a node and wrapping it into the appropriate
		attribute node.)</doc:par>
		"""
		return self.attrs.get(attrname, default)

	def setDefaultAttr(self, attrname, default=None):
		"""
		<doc:par>works like the dictionary method <method>setdefault</method>,
		it returns the attribute with the name <arg>attrname</arg>,
		or if <self/> has no such attribute, <arg>default</arg>
		(after converting it to a node and wrapping it into the appropriate
		attribute node.). In this case <arg>default</arg> will be
		kept as the attribute value.</doc:par>
		"""
		return self.attrs.setdefault(attrname, default)

	def attrKeys(self):
		"""
		return a list with all the attribute names of <self/>.
		"""
		return self.attrs.keys()

	def attrValues(self):
		"""
		return a list with all the attribute values of <self/>.
		"""
		return self.attrs.values()

	def attrItems(self):
		"""
		return a list with all the attribute name/value tuples of <self/>.
		"""
		return self.attrs.items()

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
		<doc:par>Sets attributes that are not set in <self/> to the default
		values taken from the <arg>fromMapping</arg> mapping.
		If <arg>fromDict</arg> is omitted, defaults are taken from
		<lit><self/>.defaults</lit>.</doc:par>

		<doc:par>Note that boolean attributes may savely be set to e.g. <lit>1</lit>,
		as only the fact that a boolean attribute exists matters.</doc:par>
		"""

		self.attrs.copydefaults(fromMapping)

	def withSep(self, separator, clone=0):
		"""
		<doc:par>returns a version of <self/> with a separator node between the child nodes of <self/>.
		for more info see <pyref class="Frag" method="withSep"><method>Frag.withSep</method></pyref>.</doc:par>
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

	def walk(self, before=1, after=0):
		if before:
			yield self
		for child in self.attrs.values():
			for grandchild in child.walk(before, after):
				yield grandchild
		for child in self.content:
			for grandchild in child.walk(before, after):
				yield grandchild
		if after:
			yield self

	def walkPath(self, before=1, after=0):
		if before:
			yield [self]
		for child in self.attrs.values():
			for grandchildPath in child.walkPath(before, after):
				yield [self] + grandchildPath
		for child in self.content:
			for grandchildPath in child.walkPath(before, after):
				yield [self] + grandchildPath
		if after:
			yield [self]

class Entity(Node):
	"""
	<doc:par>Class for entities. Derive your own entities from
	it and overwrite <pyref class="Node" method="convert"><method>convert</method></pyref>
	and <pyref class="Node" method="__unicode__"><method>__unicode__</method></pyref>.</doc:par>
	"""

	def compact(self):
		return self

	clone = compact

	def present(self, presenter):
		presenter.presentEntity(self)

	def publish(self, publisher):
		publisher.publish(u"&")
		self._publishName(publisher)
		publisher.publish(u";")

class CharRef(Entity):
	"""
	<doc:par>A simple character reference, the codepoint is in the class attribute
	<lit>codepoint</lit>.</doc:par>
	"""

	def convert(self, converter):
		node = Text(unichr(self.codepoint))
		return self._decorateNode(node)

	def __unicode__(self):
		return unichr(self.codepoint)

###
###
###

class Namespace(object):
	"""
	<doc:par>an &xml; namespace, contains the classes for the elements,
	entities and processing instructions in the namespace.</doc:par>
	"""

	def __init__(self, prefix, uri, thing=None):
		"""
		<doc:par>Create a new <class>Namespace</class> instance.</doc:par>
		
		<doc:par>All classes from the module the <class>Namespace</class> instance is in will be registered if
		they are derived from <pyref class="Element"><class>Element</class></pyref>, <pyref class="Entity"><class>Entity</class></pyref> or
		<pyref class="ProcInst"><class>ProcInst</class></pyref> in the following way: The class <arg>thing</arg>
		will be registered under it's class name (<lit><arg>thing</arg>.__name__</lit>).
		If you want to change this behaviour, do the following: set a class variable
		<lit>name</lit> to the name you want to be used. If you don't want
		<arg>thing</arg> to be registered at all, set <lit>name</lit> to <lit>None</lit>.
		"""
		self.prefix = unicode(prefix) or ""
		self.uri = unicode(uri) or ""
		self.elementsByName = {} # dictionary for mapping element names to classes
		self.entitiesByName = {} # dictionary for mapping entity names to classes
		self.procInstsByName = {} # dictionary for mapping processing instruction target names to classes
		self.charrefsByName = {} # dictionary for mapping character reference names to classes
		self.charrefsByNumber = {} # dictionary for mapping character reference code points to classes
		self.register(thing)
		namespaceRegistry.register(self)

	def register(self, thing):
		"""
		<doc:par>this function lets you register <arg>thing</arg> in the namespace.
		If <arg>thing</arg> is a class derived from <pyref class="Element"><class>Element</class></pyref>,
		<pyref class="Entity"><class>Entity</class></pyref> or <pyref class="ProcInst"><class>ProcInst</class></pyref>
		it will be registered under its class name (<lit><arg>thing</arg>.__name__</lit>). If you want
		to change this behaviour, do the following: set a class variable <lit>name</lit> to
		the name you want to be used. If you don't want <arg>thing</arg> to be
		registered at all, set <lit>register</lit> to <lit>0</lit>.</doc:par>

		<doc:par>After the call <arg>thing</arg> will have two class attributes:
		<lit>name</lit>, which is the name under which the class is registered and
		<lit>namespace</lit>, which is the namespace itself (i.e. <self/>).</doc:par>

		<doc:par>If <arg>thing</arg> is a dictionary, every object in the dictionary
		will be registered.</doc:par>

		<doc:par>All other objects are ignored.</doc:par>
		"""

		if isinstance(thing, type): # this is a class object
			iselement = thing is not Element and issubclass(thing, Element)
			isentity = thing is not Entity and thing is not CharRef and issubclass(thing, Entity)
			if isentity:
				ischarref = thing is not CharRef and issubclass(thing, CharRef)
				if ischarref:
					isentity = 0
			else:
				ischarref = 0
			isprocinst = thing is not ProcInst and issubclass(thing, ProcInst)
			if iselement or isentity or ischarref or isprocinst:
				name = thing.name
				# if the class attribute register is false, the class won't be registered
				if thing.register:
					thing._namespace = self # this creates a cycle
					if iselement:
						self.elementsByName[name] = thing
					elif isentity:
						self.entitiesByName[name] = thing
					elif ischarref:
						self.charrefsByName[name] = thing
						self.charrefsByNumber.setdefault(thing.codepoint, []).append(thing)
					else: # if isprocinst:
						self.procInstsByName[name] = thing
		elif isinstance(thing, dict):
			for key in thing.keys():
				self.register(thing[key])

	def __repr__(self):
		return "<%s.%s instance prefix=%r uri=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.prefix, self.uri, id(self))

class NamespaceRegistry(object):
	"""
	<doc:par>global registry for all namespaces</doc:par>
	"""
	def __init__(self):
		self.byPrefix = {}
		self.byURI = {}
		self.sequential = []

	def register(self, namespace):
		self.byPrefix[namespace.prefix] = namespace
		self.byURI[namespace.uri] = namespace
		if namespace not in self.sequential:
			self.sequential.insert(0, namespace)

namespaceRegistry = NamespaceRegistry()

class Namespaces(object):
	"""
	<doc:par>list of namespaces to be searched in a specific order
	to instantiate elements, entities and procinsts.</doc:par>
	"""
	def __init__(self, *namespaces):
		self.namespaces = []
		self.pushNamespace(namespace) # always include the namespace object from our own modules with &gt; etc.
		self.pushNamespace(*namespaces)

	def pushNamespace(self, *namespaces):
		"""
		<doc:par>pushes the <arg>namespaces</arg> onto the stack in this order,
		i.e. the last one in the list will be the first
		one to be searched. Items in namespaces can be:</doc:par>
		<doc:olist>
		<doc:item><pyref class="Namespace">namespace objects</pyref>,</doc:item>
		<doc:item>Module objects, in which case <lit><rep>module</rep>.namespace</lit>
		will be used as the <pyref class="Namespace"><class>Namespace</class> object</pyref>,</doc:item>
		<doc:item>strings, which specify the namespace
		prefix, i.e. <lit>namespaceRegistry.byPrefix[<rep>string</rep>]</lit>
		will be used.</doc:item>
		</doc:olist>
		"""
		for namespace in namespaces:
			if isinstance(namespace, types.ModuleType):
				namespace = namespace.namespace
			elif isinstance(namespace, (str, unicode)):
				namespace = namespaceRegistry.byPrefix[namespace]
			self.namespaces.insert(0, namespace) # built in reverse order, so a simple "for in" finds the most recent entry.

	def popNamespace(self, count=1):
		del self.namespaces[:count]

	def __splitName(self, name):
		"""
		split a qualified name into a (namespace, name) pair
		"""
		name = name.split(":")
		if len(name) == 1: # no namespace specified
			name.insert(0, None)
		return name

	def __allNamespaces(self):
		"""
		<doc:par>returns a list of all namespaces to be searched in this order.</doc:par>
		"""
		return self.namespaces+namespaceRegistry.sequential

	def elementFromName(self, name):
		"""
		<doc:par>returns the element class for the name
		<arg>name</arg> (which might include a namespace).</doc:par>
		"""
		name = self.__splitName(name)
		for namespace in self.__allNamespaces():
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.elementsByName[name[1]]
				except KeyError: # no element in this namespace with this name
					pass
		raise errors.IllegalElementError(name) # elements with this name couldn't be found

	def entityFromName(self, name):
		"""
		<doc:par>returns the entity or charref class for the name
		<arg>name</arg> (which might include a namespace).</doc:par>
		"""
		name = self.__splitName(name)
		namespaces = self.__allNamespaces()
		# try the charrefs first
		for namespace in namespaces:
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.charrefsByName[name[1]]
				except KeyError: # no charref in this namespace with this name
					pass
		# no charrefs => try the entities now
		for namespace in namespaces:
			if name[0] is None or name[0] == namespace.prefix():
				try:
					return namespace.entitiesByName[name[1]]
				except KeyError: # no entity in this namespace with this name
					pass
		raise errors.IllegalEntityError(name) # entities with this name couldn't be found

	def procInstFromName(self, name):
		"""
		<doc:par>returns the processing instruction class for the name
		<arg>name</arg> (which might include a namespace).</doc:par>
		"""
		name = self.__splitName(name)
		for namespace in self.__allNamespaces():
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.procInstsByName[name[1]]
				except KeyError: # no processing instruction in this namespace with this name
					pass
		raise errors.IllegalProcInstError(name) # processing instructions with this name couldn't be found

	def charrefFromNumber(self, number):
		"""
		<doc:par>returns the first charref class for the codepoint <arg>number</arg>.</doc:par>
		"""
		for namespace in self.__allNamespaces():
			try:
				return namespace.charrefsByNumber[number][0]
			except KeyError:
				pass
		return None

# C0 Controls and Basic Latin
class quot(CharRef): "quotation mark = APL quote, U+0022 ISOnum"; codepoint = 34
class amp(CharRef): "ampersand, U+0026 ISOnum"; codepoint = 38
class lt(CharRef): "less-than sign, U+003C ISOnum"; codepoint = 60
class gt(CharRef): "greater-than sign, U+003E ISOnum"; codepoint = 62

namespace = Namespace("xsc", "", vars())

defaultNamespaces = Namespaces()

###
###
###

class Location(object):
	"""
	<doc:par>Represents a location in an &xml; entity.</doc:par>
	"""

	def __init__(self, locator=None, sysID=None, pubID=None, lineNumber=-1, columnNumber=-1):
		"""
		<doc:par>Create a new <class>Location</class> instance by reading off the current location from
		the <arg>locator</arg>, which is then stored internally. In addition to that the system ID,
		public ID, line number and column number can be overwritten by explicit arguments.</doc:par>
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
		"<doc:par>Return the column number of this location.</doc:par>"
		return self.__columnNumber

	def getLineNumber(self):
		"<doc:par>Return the line number of this location.</doc:par>"
		return self.__lineNumber

	def getPublicId(self):
		"<doc:par>Return the public identifier for this location.</doc:par>"
		return self.__pubID

	def getSystemId(self):
		"<doc:par>Return the system identifier for this location.</doc:par>"
		return self.__sysID

	def offset(self, offset):
		"""
		<doc:par>returns a location where the line number is incremented by offset
		(and the column number is reset to 1).</doc:par>
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
