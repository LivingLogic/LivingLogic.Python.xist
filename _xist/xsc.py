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

import os, types, sys, stat, urllib, random

import url, presenters, publishers, converters, errors, options, utils, helpers

###
### helpers
###

def ToNode(value):
	"""
	<doc:par>convert the <pyref arg="value">value</pyref> passed in to an &xist; <pyref class="Node">Node</pyref>.</doc:par>

	<doc:par>If <pyref arg="value">value</pyref> is a tuple or list, it will be (recursively) converted
	to a <pyref class="Frag">Frag</pyref>. Integers, strings, etc. will be converted to a <pyref class="Text">Text</pyref>.
	If <pyref arg="value">value</pyref> is a <pyref class="Node">Node</pyref> already, nothing will be done.
	In the case of <code>None</code> the XSC Null (<pyref class="Null">xsc.Null</pyref>) will be returned).
	Anything else raises an exception.</doc:par>
	"""
	t = type(value)
	if t is types.InstanceType:
		if isinstance(value, Node):
			if isinstance(value, Attr):
				return Frag(*value) # repack the attribute in a fragment, and we have a valid XSC node
			return value
		elif isinstance(value, url.URL):
			return Text(value.asString())
	elif t in (types.StringType, types.UnicodeType, types.IntType, types.LongType, types.FloatType):
		return Text(value)
	elif t is types.NoneType:
		return Null
	elif t in (types.ListType, types.TupleType):
		return Frag(*value)
	raise errors.IllegalObjectError(value) # none of the above, so we throw and exception

# FIXME this will become classmethods in Python 2.2
def classNamespace(class_):
	return getattr(class_, "_ns", None)

def classPrefix(class_):
	ns = classNamespace(class_)
	if ns is not None:
		return ns.prefix
	else:
		return unicode(class_.__module__)

###
###
###

class Node:
	"""
	base class for nodes in the document tree. Derived classes must
	overwrite <pyref module="xist.xsc" class="Node" method="convert">convert</pyref>
	and may overwrite <pyref module="xist.xsc" class="Node" method="publish">publish</pyref>
	and <pyref module="xist.xsc" class="Node" method="asPlainString">asPlainString</pyref>.
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
	register = 1

	def __repr__(self):
		return self.repr(presenters.defaultPresenterClass())

	def clone(self):
		"""
		returns an identical clone of the node and it's children.
		"""
		raise NotImplementedError("clone method not implemented in %s" % self.__class__.__name__)

	def namespace(self):
		"""
		return the namespace object for this object or None.
		"""
		return getattr(self.__class__, "_ns", None)

	def prefix(self):
		"""
		return the namespace prefix for this object or the module name, if there is no namespace
		"""
		ns = self.namespace()
		if ns is not None:
			return ns.prefix
		else:
			return unicode(self.__class__.__module__)

	def repr(self, presenter=None):
		if presenter is None:
			presenter = presenters.defaultPresenterClass()
		presenter.beginPresentation()
		self.present(presenter)
		return presenter.endPresentation()

	def present(self, presenter):
		raise NotImplementedError("present method not implemented in %s" % self.__class__.__name__)

	def conv(self, converter=None, mode=None, stage=None, target=None, lang=None):
		"""
		<doc:par>returns a version of this node and it's content converted to HTML (or any other target).</doc:par>
		"""
		if converter is None:
			return self.convert(converters.Converter(mode=mode, stage=stage, target=target, lang=lang))
		else:
			oldmode = converter.mode
			oldstage = converter.stage
			oldtarget = converter.target
			oldlang = converter.lang
			converter.mode = mode
			converter.stage = stage
			converter.target = target
			converter.lang = lang
			node = self.convert(converter)
			converter.mode = oldmode
			converter.stage = oldstage
			converter.target = oldtarget
			converter.lang = oldlang
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

	def asPlainString(self):
		"""
		<doc:par>returns this node as a (unicode) string without any character references.
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
		to define <pyref method="asPlainString" nolink>asPlainString</pyref> in the following way:
		<doc:programlisting>
		def asPlainString(self):
			return self.content.asPlainString().upper()
		</doc:programlisting>

		<pyref method="asPlainString" nolink>asPlainString</pyref> can be used everywhere, where
		a plain string representation of the node is required.
		<pyref module="xist.ns.html" class="title">title</pyref> uses this function on its content,
		so you can safely use &html; elements in your title elements (e.g. if your
		title is dynamically constructed from a &dom; tree.)</doc:par>
		"""
		raise NotImplementedError("asPlainString method not implemented in %s" % self.__class__.__name__)

	def asText(self, monochrome=1, squeezeBlankLines=0, lineNumbers=0, cols=80):
		"""
		<doc:par>Return the node as a formatted plain &ascii; string.
		Note that this really only make sense for &html; trees.</doc:par>

		<doc:par>This requires that <app moreinfo="http://ei5nazha.yz.yamagata-u.ac.jp/~aito/w3m/eng/">w3m</app> is installed.</doc:par>
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
		return int(self.asPlainString())

	def asInt(self):
		"""
		returns this node converted to an integer.
		"""
		return int(self)

	def asFloat(self, decimal=".", ignore=""):
		"""
		<doc:par>returns this node converted to a float. <pyref arg="decimal">decimal</pyref>
		specifies which decimal separator is used in the value
		(e.g. <code>"."</code> (the default) or <code>","</code>).
		<pyref arg="ignore">ignore</pyref>specifies which character will be ignored.</doc:par>
		"""
		s = self.asPlainString()
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

	def publish(self, publisher):
		"""
		<doc:par>generates unicode strings for the node, and passes
		the strings to the callable object <pyref arg="publisher">publisher</pyref>.</doc:par>

		<doc:par>The encoding and xhtml specification are taken from the <pyref arg="publisher">publisher</pyref>.</doc:par>
		"""
		raise NotImplementedError("publish method not implemented in %s" % self.__class__.__name__)

	def asString(self, base=None, root=None, xhtml=None, publishPrefix=0):
		"""
		<doc:par>returns this element as a unicode string.</doc:par>

		<doc:par>For an explanation of <pyref arg="xhtml">xhtml</pyref> and
		<pyref arg="publishPrefix">publishPrefix</pyref> see <pyref method="publish">publish</pyref>.</doc:par>
		"""
		publisher = publishers.StringPublisher(base=base, root=root, xhtml=xhtml, publishPrefix=publishPrefix)
		self.publish(publisher)
		return publisher.asString()

	def asBytes(self, base=None, root=None, encoding=None, xhtml=None, publishPrefix=0):
		"""
		<doc:par>returns this element as a byte string suitable for writing
		to an &html; file or printing from a CGI script.</doc:par>

		<doc:par>For the parameters see <pyref method="publish">publish</pyref>.</doc:par>
		"""
		publisher = publishers.BytePublisher(base=base, root=root, encoding=encoding, xhtml=xhtml, publishPrefix=publishPrefix)
		self.publish(publisher)
		return publisher.asBytes()

	def write(self, stream, base=None, root=None, encoding=None, xhtml=None, publishPrefix=0):
		"""
		<doc:par>writes the element to the file like
		object <pyref arg="file">file</pyref></doc:par>

		<doc:par>For the rest of the parameters see <pyref method="publish">publish</pyref>.</doc:par>
		"""
		publisher = publishers.FilePublisher(stream, base=base, root=root, encoding=encoding, xhtml=xhtml, publishPrefix=publishPrefix)
		self.publish(publisher)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		"""
		<doc:par>returns a fragment which contains child elements of this node.</doc:par>

		<doc:par>If you specify <pyref arg="type">type</pyref> as the class of an XSC node only nodes
		of this class will be returned. If you pass a list of classes, nodes that are an
		instance of one of the classes will be returned.</doc:par>

		<doc:par>If you set <pyref arg="subtype">subtype</pyref> to <code>1</code> nodes that are a
		subtype of <pyref arg="type">type</pyref> will be returned too.</doc:par>

		<doc:par>If you pass a dictionary as <pyref arg="attrs">attrs</pyref> it has to contain
		string pairs and is used to match attribute values for elements. To match
		the attribute values their <pyref class="Node" method="asPlainString">asPlainString</pyref>
		representation will be used. You can use <code>None</code> as the value to test that
		the attribute is set without testing the value.</doc:par>

		<doc:par>Additionally you can pass a test function in <pyref arg="test">test</pyref>, that
		returns <code>1</code>, when the node passed in has to be included in the
		result and <code>0</code> otherwise.</doc:par>

		<doc:par>If you set <pyref arg="searchchildren">searchchildren</pyref> to <code>1</code>
		not only the immediate children but also the grandchildren will be searched for nodes
		matching the other criteria.</doc:par>

		<doc:par>If you set <pyref arg="searchattrs">searchattrs</pyref> to <code>1</code> the attributes
		of the nodes (if <pyref arg="type">type</pyref> is <pyref class="Element">Element</pyref> or one
		of its subtypes) will be searched too.</doc:par>

		<doc:par>Note that the node has to be of type <pyref class="Element">Element</pyref>
		(or a subclass of it) to match <pyref arg="attrs">attrs</pyref>.</doc:par>
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
					if (not self.hasAttr(attr)) or ((attrs[attr] is not None) and (self[attr].asPlainString() != attrs[attr])):
						return 0
				return 1
			else:
				return 0

	def _matches(self, type_, subtype, attrs, test):
		res = 1
		if type_ is not None:
			if type(type_) not in [types.ListType, types.TupleType]:
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
		<doc:par>decorate the node <pyref module="xist.xsc" class="Node" method="_decorateNode" arg="node">node</pyref>
		with the same location information as <self/>.</doc:par>
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
		if hasattr(self, "name"):
			publisher.publish(self.name)
		else:
			publisher.publish(self.__class__.__name__)

	def mapped(self, function):
		"""
		<doc:par>returns the node mapped through the function <pyref arg="function">function</pyref>.
		This call works recursively (for <pyref class="Frag">Frag</pyref> and <pyref class="Element">Element</pyref>.
		When you want an unmodified node you simply can return <self/>. <pyref nolink=1>mapped</pyref>
		will make a copy of it and fill the content recursively. Note that element attributes
		will not be mapped.</doc:par>
		"""
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		return node

	def normalized(self):
		"""
		<doc:par>return a normalized version of <self/>, which means, that consecutive
		<pyref class="Text">Text nodes</pyref> are merged.</doc:par>
		"""
		return self

	def __mul__(self, factor):
		"""
		<doc:par>return a <pyref class="Frag">Frag</pyref> with <pyref arg="factor">factor</pyref> times
		the node as an entry.</doc:par>
		"""
		return Frag(*factor*[self])

	def __rmul__(self, factor):
		"""
		<doc:par>returns a <pyref class="Frag">Frag</pyref> with <pyref arg="factor">factor</pyref> times
		the node as an entry.</doc:par>
		"""
		return Frag(*[self]*factor)

class CharacterData(Node):
	"""
	<doc:par>provides nearly the same functionality as <pyref module="UserString" class="UserString">UserString</pyref>,
	but omits a few methods (<code>__str__</code> etc.)</doc:par>
	"""
	def __init__(self, content=u""):
		self.content = helpers.unistr(content)

	def __iadd__(self, other):
		other = ToNode(other)
		return self.__class__(self.content+other.content)

	__add__ = __iadd__

	def __radd__(self, other):
		other = ToNode(other)
		return self.__class__(other.content+self.content)

	def __imul__(self, n):
		return self.__class__(self.content*n)

	__mul__ = __imul__

	def __cmp__(self, other):
		if isinstance(other, self.__class__):
			return cmp(self.content, other.content)
		else:
			return cmp(self.content, other)

	def __contains__(self, char):
		return helpers.unistr(char) in self.content

	def __hash__(self):
		return hash(self.content)

	def __len__(self):
		return len(self.content)

	def __getitem__(self, index):
		return self.content[index]

	def __getslice__(self, index1, index2):
		return self.__class__(self.content[index1:index2])

	def capitalize(self):
		return self.__class__(self.content.capitalize())

	def center(self, width):
		return self.__class__(self.content.center(width))

	def count(self, sub, start=0, end=sys.maxint):
		return self.content.count(sub, start, end)

	def endswith(self, suffix, start=0, end=sys.maxint):
		return self.content.endswith(helpers.unistr(suffix), start, end)

	# no find here def find(self, sub, start=0, end=sys.maxint):
	#	return self.content.find(helpers.unistr(sub), start, end)

	def index(self, sub, start=0, end=sys.maxint):
		return self.content.index(helpers.unistr(sub), start, end)

	def isalpha(self):
		return self.content.isalpha()

	def isalnum(self):
		return self.content.isalnum()

	def isdecimal(self):
		return self.content.isdecimal()

	def isdigit(self):
		return self.content.isdigit()

	def islower(self):
		return self.content.islower()

	def isnumeric(self):
		return self.content.isnumeric()

	def isspace(self):
		return self.content.isspace()

	def istitle(self):
		return self.content.istitle()

	def join(self, frag):
		return frag.withSep(self)

	def isupper(self):
		return self.content.isupper()

	def ljust(self, width):
		return self.__class__(self.content.ljust(width))

	def lower(self):
		return self.__class__(self.content.lower())

	def lstrip(self):
		return self.__class__(self.content.lstrip())

	def replace(self, old, new, maxsplit=-1):
		return self.__class__(self.content.replace(helpers.unistr(old), helpers.unistr(new), maxsplit))

	def rfind(self, sub, start=0, end=sys.maxint):
		return self.content.rfind(helpers.unistr(sub), start, end)

	def rindex(self, sub, start=0, end=sys.maxint):
		return self.content.rindex(helpers.unistr(sub), start, end)

	def rjust(self, width):
		return self.__class__(self.content.rjust(width))

	def rstrip(self):
		return self.__class__(self.content.rstrip())

	def split(self, sep=None, maxsplit=-1):
		return Frag(self.content.split(sep, maxsplit))

	def splitlines(self, keepends=0):
		return Frag(self.content.splitlines(keepends))

	def startswith(self, prefix, start=0, end=sys.maxint):
		return self.content.startswith(helpers.unistr(prefix), start, end)

	def strip(self):
		return self.__class__(self.content.strip())

	def swapcase(self):
		return self.__class__(self.content.swapcase())

	def title(self):
		return self.__class__(self.content.title())

	def translate(self, *args):
		return self.__class__(self.content.translate(*args))

	def upper(self):
		return self.__class__(self.content.upper())

class Text(CharacterData):
	"""
	<doc:par>text node. The characters <markup>&lt;</markup>, <markup>&gt;</markup>, <markup>&amp;</markup>
	(and <markup>"</markup> inside attributes) will be "escaped" with the
	appropriate character entities.</doc:par>
	"""

	def __init__(self, content=u""):
		if isinstance(content, Text):
			content = content.content
		CharacterData.__init__(self, content)

	def convert(self, converter):
		return self

	def clone(self):
		return self

	def asPlainString(self):
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

class Frag(Node):
	"""
	<doc:par>A fragment contains a list of nodes and can be used for dynamically constructing content.
	The member content of an <pyref class="Element">Element</pyref> is a <pyref nolink>Frag</pyref>.</doc:par>
	"""

	empty = 0

	def __init__(self, *content):
		self.__content = []
		for child in content:
			child = ToNode(child)
			if isinstance(child, Frag):
				self.__content.extend(child)
			elif child is not Null:
				self.__content.append(child)

	def convert(self, converter):
		node = self.__class__() # virtual constructor => attributes (which are derived from Frag) will be handled correctly)
		for child in self.__content:
			convertedchild = child.convert(converter)
			assert isinstance(convertedchild, Node), "the convert method returned the illegal object %r (type %r) when converting %r" % (convertedchild, type(convertedchild), self)
			if convertedchild is not Null:
				node.__content.append(convertedchild)
		return self._decorateNode(node)

	def clone(self):
		node = self.__class__() # virtual constructor => attributes (which are derived from Frag) will be handled correctly)
		node.__content = [ child.clone() for child in self.__content ]
		return self._decorateNode(node)

	def present(self, presenter):
		presenter.presentFrag(self)

	def asPlainString(self):
		return u"".join([ child.asPlainString() for child in self.__content ])

	def publish(self, publisher):
		for child in self.__content:
			child.publish(publisher)

	def __getitem__(self, index):
		"""
		<doc:par>Return the <pyref arg="index">index</pyref>'th node for the content of the fragment.
		If <pyref arg="index">index</pyref> is a list <pyref nolink>__getitem__</pyref> will work
		recursively. If <pyref arg="index">index</pyref> is empty, <self/> will be returned.</doc:par>
		"""
		if type(index) in (types.IntType, types.LongType):
			return self.__content[index]
		elif type(index) is types.ListType:
			node = self
			for subindex in index:
				node = node[subindex]
			return node
		else:
			raise TypeError("index must be int, long or list not %s" % type(index).__name__)

	def __setitem__(self, index, value):
		"""
		<doc:par>Allows you to replace the <pyref arg="index">index</pyref>'th content node of the fragment
		with the new value <pyref arg="value">value</pyref> (which will be converted to a node).
		If  <pyref arg="index">index</pyref> is a list <pyref nolink=1>__setitem__</pyref> will be applied
		to the innermost index after traversing the rest of <pyref arg="index">index</pyref> recursively.
		If <pyref arg="index">index</pyref> is empty the call will be ignored.</doc:par>
		"""
		value = Frag(value).__content
		try:
			self.__content[index:index+1] = value
		except TypeError: # assume index is a list
			if len(index):
				node = self
				for subindex in index[:-1]:
					node = node[subindex]
				index = index[-1]
				node[index:index+1] = value

	def __delitem__(self, index):
		"""
		<doc:par>Remove the <pyref arg="index">index</pyref>'th content node from the fragment.
		If <pyref arg="index">index</pyref> is a list, the innermost index will be deleted,
		after traversing the rest of <pyref arg="index">index</pyref> recursively.
		If <pyref arg="index">index</pyref> is empty the call will be ignored.</doc:par>
		"""
		try:
			del self.__content[index]
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
		node.__content = self.__content[index1:index2]
		return node

	def __setslice__(self, index1, index2, sequence):
		"""
		replaces a slice of the content of the fragment
		"""
		self.__content[index1:index2] = Frag(*sequence).__content

	def __delslice__(self, index1, index2):
		"""
		removes a slice of the content of the fragment
		"""
		del self.__content[index1:index2]

	def __mul__(self, factor):
		"""
		returns a <pyref module="xist.ns" class="Frag">Frag</pyref> with <pyref arg="factor">factor</pyref> times
		the content of <self/>.
		"""
		return Frag(*factor*self.__content)

	def __rmul__(self, factor):
		"""
		returns a <pyref module="xist.ns" class="Frag">Frag</pyref> with <pyref arg="factor">factor</pyref> times
		the content of <self/>.
		"""
		return Frag(*self.__content*factor)

	def __nonzero__(self):
		"""
		return whether the fragment is not empty (this should be a little faster than defaulting to __len__)
		"""
		return len(self.__content)>0

	def __len__(self):
		"""
		return the number of children
		"""
		return len(self.__content)

	def append(self, *others):
		"""
		<doc:par>append all items in <pyref module="xist.xsc" class="Frag" method="append" arg="others">others</pyref> to <self/>.</doc:par>
		"""
		for other in others:
			other = ToNode(other)
			if isinstance(other, Frag):
				self.__content.extend(other)
			elif other is not Null:
				self.__content.append(other)

	def insert(self, index, *others):
		"""
		<doc:par>inserts all items in <pyref arg="others">others</pyref> at the position <pyref arg="index">index</pyref>.
		(this is the same as <code><self/>[<pyref arg="index">index</pyref>:<pyref arg="index">index</pyref>] = <pyref arg="index">others</pyref></code>)
		"""
		other = Frag(*others)
		self.__content[index:index] = other.__content

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		for child in self.__content:
			if child._matches(type, subtype, attrs, test):
				node.append(child)
			if searchchildren:
				node.append(child.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def compact(self):
		node = self.__class__()
		for child in self.__content:
			compactedchild = child.compact()
			assert isinstance(compactedchild, Node), "the compact method returned the illegal object %r (type %r) when compacting %r" % (compactedchild, type(compactedchild), child)
			if compactedchild is not Null:
				node.__content.append(compactedchild)
		return self._decorateNode(node)

	def withSep(self, separator, clone=0):
		"""
		<doc:par>return a version of <self/> with a separator node between the nodes of <self/>.</doc:par>

		<doc:par>if <code><pyref arg="clone">clone</pyref>==0</code> one node will be inserted several times,
		if <code><pyref arg="clone">clone</pyref>==1</code> clones of this node will be used.</doc:par>
		"""
		node = Frag()
		newseparator = ToNode(separator)
		for child in self.__content:
			if len(node):
				node.append(newseparator)
				if clone:
					newseparator = newseparator.clone()
			node.append(child)
		return node

	def sorted(self, compare=lambda node1, node2: cmp(node1.asPlainString(), node2.asPlainString())):
		"""
		<doc:par>returns a sorted version of the <self/>. <pyref arg="compare">compare</pyref> is
		a comparison function returning -1, 0, 1 respectively and defaults to comparing the
		<pyref class="Node" method="asPlainString">asPlainString</pyref> value.</doc:par>
		"""
		node = Frag()
		node.__content = self.__content[:]
		node.__content.sort(compare)
		return node

	def reversed(self):
		"""
		<doc:par>returns a reversed version of the <self/>.</doc:par>
		"""
		node = Frag()
		node.__content = self.__content[:]
		node.__content.reverse()
		return node

	def filtered(self, function):
		"""
		<doc:par>returns a filtered version of the <self/>.</doc:par>
		"""
		node = Frag()
		node.__content = [ child for child in self.__content if function(child) ]
		return node

	def shuffled(self):
		"""
		<doc:par>return a shuffled version of <self/>.</doc:par>
		"""
		content = self.__content[:]
		node = Frag()
		while content:
			index = random.randrange(len(content))
			node.__content.append(content[index])
			del content[index]
		return node

	def mapped(self, function):
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = Frag(*[ child.mapped(function) for child in self.__content])
		return node

	def normalized(self):
		node = Frag()
		lasttypeOK = 0
		for child in self.__content:
			normalizedchild = child.normalized()
			thistypeOK = isinstance(normalizedchild, Text)
			if thistypeOK and lasttypeOK:
				node.__content[-1] += normalizedchild
			else:
				node.__content.append(normalizedchild)
			lasttypeOK = thistypeOK
		return node

class Comment(CharacterData):
	"""
	a comment node
	"""

	def convert(self, converter):
		return self

	def clone(self):
		return self

	compact = clone

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

class ProcInst(CharacterData):
	"""
	<doc:par>Class for processing instruction. This class is abstract.</doc:par>

	<doc:par>Processing instruction with the target <code>xml</code> will be 
	handled by the derived class <pyref module="xist.xsc" class="XML">XML</pyref>.
	All other processing instructions will be handled
	by other classes derived from <pyref module="xist.xsc" class="ProcInst" nolink>ProcInst</pyref>.</doc:par>
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

	def asPlainString(self):
		return u""

class XML(ProcInst):
	"""
	&xml; header
	"""

	name = u"xml"
	presentPrefix = 0
	publishPrefix = 0

	def publish(self, publisher):
		encodingfound = utils.findAttr(self.content, u"encoding")
		versionfound = utils.findAttr(self.content, u"version")
		standalonefound = utils.findAttr(self.content, u"standalone")
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

class Element(Node):
	"""
	<doc:par>This class represents &xml;/&xist; elements. All elements
	implemented by the user must be derived from this class.</doc:par>

	<doc:par>If you not only want to construct a &dom; tree via a Python script
	(by directly instantiating these classes), but to read an &xml; file
	you must register the element class with the parser, this can be done
	by creating <pyref module="xist.xsc" class="Namespace">Namespace</pyref>
	objects.</doc:par>

	<doc:par>Every element class should have two class variables:
	<code>empty</code>: this is either <code>0</code> or <code>1</code>
	and specifies whether the element type is allowed to have content
	or not. Note that the parser does not use this as some sort of
	static DTD, i.e. you still must write your empty tags
	like this: <markup>&lt;foo/&gt;</markup>.</doc:par>

	<doc:par><pyref var="attrHandlers">attrHandlers</pyref> is a dictionary that maps attribute
	names to attribute classes, which are all derived from <pyref class="Attr">Attr</pyref>.
	Assigning to an attribute with a name that is not in <code>attrHandlers.keys()</code>
	is an error.</doc:par>
	"""

	empty = 1 # 0 => element with content; 1 => stand alone element
	attrHandlers = {} # maps attribute names to attribute classes

	def __init__(self, *content, **attrs):
		"""
		positional arguments are treated as content nodes.

		keyword arguments and dictionaries are treated as attributes.
		"""
		self.attrs = {}
		newcontent = []
		for child in content:
			if isinstance(child, types.DictType):
				for (attrname, attrvalue) in child.items():
					self[attrname] = attrvalue
			else:
				newcontent.append(child)
		self.content = Frag(*newcontent)
		for (attrname, attrvalue) in attrs.items():
			self[attrname] = attrvalue

	def append(self, *items):
		"""
		<doc:par>appends to content (see <pyref class="Frag" method="append">Frag.append</pyref> for more info)</doc:par>
		"""

		self.content.append(*items)
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def insert(self, index, *items):
		"""
		<doc:par>inserts into the content (see <pyref class="Frag" method="insert">Frag.insert</pyref> for more info)</doc:par>
		"""
		self.content.insert(index, *items)
		if self.empty and len(self):
			raise errors.EmptyElementWithContentError(self)

	def convert(self, converter):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.convert(converter)
		for attrname in self.attrs.keys():
			attr = self.attrs[attrname]
			convertedattr = attr.convert(converter)
			assert isinstance(convertedattr, Node), "the convert method returned the illegal object %r (type %r) when converting the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
			node.attrs[attrname] = convertedattr
		return self._decorateNode(node)

	def clone(self):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.clone() # this is faster than passing it in the constructor (no ToNode call)
		for attr in self.attrs.keys():
			node.attrs[attr] = self.attrs[attr].clone()
		return self._decorateNode(node)

	def asPlainString(self):
		return self.content.asPlainString()

	def _addImageSizeAttributes(self, publisher, imgattr, widthattr=None, heightattr=None):
		"""
		<doc:par>add width and height attributes to the element for the image that can be found in the attribute
		<pyref arg="imgattr">imgattr</pyref>. If the attributes are already there, they are taken as a formatting
		template with the size passed in as a dictionary with the keys <code>"width"</code> and <code>"height"</code>,
		i.e. you could make your image twice as wide with <code>width="%(width)d*2"</code>.</doc:par>

		<doc:par>Passing <code>None</code> as <pyref arg="widthattr">widthattr</pyref> or
		<pyref arg="heightattr">heightattr</pyref> will prevent the respective attributes
		from being modified in any way.</doc:par>
		"""

		if self.hasAttr(imgattr):
			attr = self[imgattr]
			size = attr.imageSize(publisher)
			if size is not None: # the size was retrieved so we can use it
				sizedict = {"width": size[0], "height": size[1]}
				for attr in (heightattr, widthattr):
					if attr is not None: # do something to the width/height
						if self.hasAttr(attr):
							try:
								s = self[attr].asPlainString() % sizedict
								s = str(eval(s))
								s = helpers.unistr(s)
								self[attr] = s
							except TypeError: # ignore "not all argument converted"
								pass
							except:
								raise errors.ImageSizeFormatError(self, attr)
						else:
							self[attr] = size[attr==heightattr]

	def present(self, presenter):
		presenter.presentElement(self)

	def _publishAttrs(self, publisher):
		"""
		publishes the attributes. Factored out, so that it
		can be reused.
		"""
		for (attrname, attrvalue) in self.attrs.items():
			if not len(attrvalue): # skip empty attributes
				continue
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

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		publisher.publish(u"<")
		self._publishName(publisher)
		self._publishAttrs(publisher)
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
		if type(index) in (types.StringType, types.UnicodeType):
			if index[-1] == "_":
				index = index[:-1]
			# we're returning the packed attribute here, because otherwise there would be no possibility to get an expanded URL
			try:
				attr = self.attrs[index]
			except KeyError: # if the attribute is not there generate an empty one ...
				try:
					attr = self.attrHandlers[index]()
				except KeyError: # ... if we can
					raise errors.IllegalAttrError(self, index)
				self.attrs[index] = attr
			return attr
		else:
			return self.content[index]

	def __setitem__(self, index, value):
		"""
		<doc:par>sets an attribute or one of the content nodes depending on whether
		an 8bit or unicode string (i.e. attribute name) or a number or list (i.e.
		content node index) is passed in.</doc:par>
		"""
		if type(index) in (types.StringType, types.UnicodeType):
			if index[-1] == "_":
				index = index[:-1]
			# values are constructed via the attribute classes specified in the attrHandlers dictionary, which do the conversion
			try:
				attr = self.attrHandlers[index]() # create an empty attribute of the right type
			except KeyError:
				raise errors.IllegalAttrError(self, index)
			attr.append(value) # put the value into the attribute
			self.attrs[index] = attr # put the attribute in our dict
		else:
			self.content[index] = value

	def __delitem__(self, index):
		"""
		removes an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number or list (i.e. content node index) is passed in.
		"""
		if type(index) in (types.StringType, types.UnicodeType):
			if index[-1] == "_":
				index = index[:-1]
			try:
				del self.attrs[index]
			except KeyError: # ignore non-existing attributes (even if the name is not in self.attrHandlers.keys()
				pass
		else:
			del self.content[index]

	def hasAttr(self, attrname):
		"""
		<doc:par>return whether <self/> has an attribute named <pyref arg="attr">attr</pyref>.</doc:par>
		"""
		try:
			attr = self.attrs[attrname]
		except KeyError:
			return 0
		return len(attr)>0

	def getAttr(self, attrname, default=None):
		"""
		<doc:par>works like the method <code>get()</code> of dictionaries,
		it returns the attribute with the name <pyref arg="attr">attr</pyref>,
		or if <self/> has no such attribute, <pyref arg="default">default</pyref>
		(after converting it to a node and wrapping it into the appropriate
		attribute node.)</doc:par>
		"""
		attr = self[attrname]
		if attr:
			return attr
		else:
			return self.attrHandlers[attrname](default) # pack the attribute into an attribute object

	def setDefaultAttr(self, attrname, default=None):
		"""
		<doc:par>works like the method <code>setdefault()</code> of dictionaries,
		it returns the attribute with the name <pyref arg="attr">attr</pyref>,
		or if <self/> has no such attribute, <pyref arg="default">default</pyref>
		(after converting it to a node and wrapping it into the appropriate
		attribute node.). In this case <pyref arg="default">default</pyref> will be
		kept as the attribute value.</doc:par>
		"""
		attr = self[attrname]
		if not attr:
			attr = self.attrHandlers[attrname](default) # pack the attribute into an attribute object
			self.attrs[index] = attr
		return attr

	def attrKeys(self):
		"""
		return a list with all the attribute names of <self/>.
		"""
		return [ attrname for (attrname, attrvalue) in self.attrs.items() if len(attrvalue) ]

	def attrValues(self):
		"""
		return a list with all the attribute values of <self/>.
		"""
		return [ attrvalue for (attrname, attrvalue) in self.attrs.items() if len(attrvalue) ]

	def attrItems(self):
		"""
		return a list with all the attribute name/value tuples of <self/>.
		"""
		return [ (attrname, attrvalue) for (attrname, attrvalue) in self.attrs.items() if len(attrvalue) ]

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
		for attr in self.attrs.keys():
			convertedattr = self.attrs[attr].compact()
			assert isinstance(convertedattr, Node), "the compact method returned the illegal object %r (type %r) when compacting the attribute %s with the value %r" % (convertedchild, type(convertedchild), presenters.strAttrName(attrname), child)
			node.attrs[attr] = convertedattr
		return self._decorateNode(node)

	def find(self, type=None, subtype=0, attrs=None, test=None, searchchildren=0, searchattrs=0):
		node = Frag()
		if searchattrs:
			for attr in self.attrValues():
				node.append(attr.find(type, subtype, attrs, test, searchchildren, searchattrs))
		node.append(self.content.find(type, subtype, attrs, test, searchchildren, searchattrs))
		return node

	def copyDefaultAttrs(self, fromDict=None):
		"""
		<doc:par>Sets attributes that are not set in <self/> to the default
		values taken from the fromDict dictionary.
		If <pyref arg="fromDict">fromDict</pyref> is omitted, defaults are taken from
		<code>self.defaults</code>.</doc:par>

		<doc:par>Note that boolean attributes may savely be set to zero or one (integer).
		as only the fact that a boolean attribte exists matters.</doc:par>
		"""

		if fromDict is None:
			fromDict = self.defaults
		for (attrname, attrvalue) in fromDict.items():
			if not self.hasAttr(attrname):
				self[attrname] = attrvalue

	def withSep(self, separator, clone=0):
		"""
		<doc:par>returns a version of <self/> with a separator node between the child nodes of <self/>.
		for more info see <pyref class="Frag" method="withSep">Frag.withSep</pyref>.</doc:par>
		"""
		node = self.__class__(self.attrs)
		node.content = self.content.withSep(separator, clone)
		return node

	def sorted(self, compare=lambda node1, node2: cmp(node1.asPlainString(), node2.asPlainString())):
		"""
		returns a sorted version of <self/>.
		"""
		node = self.__class__(**self.attrs)
		node.content = self.content.sorted(compare)
		return node

	def reversed(self):
		"""
		returns a reversed version of <self/>.
		"""
		node = self.__class__(**self.attrs)
		node.content = self.content.reversed()
		return node

	def filtered(self, function):
		"""
		returns a filtered version of the <self/>.
		"""
		node = self.__class__()
		node.content = self.content.filtered(function)
		node.attrs = self.attrs
		return node

	def shuffled(self):
		"""
		returns a shuffled version of the <self/>.
		"""
		node = self.__class__()
		node.content = self.content.shuffled()
		node.attrs = self.attrs
		return node

	def mapped(self, function):
		node = function(self)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = self.__class__(*self.content.mapped(function))
			for (attrname, attrvalue) in self.attrs.items():
				if len(attrvalue):
					node[attrname] = attrvalue.mapped(function)
		return node

	def normalized(self):
		node = self.__class__()
		node.content = self.content.normalized()
		for (attrname, attrvalue) in self.attrs.items():
			node[attrname] = attrvalue.normalized()
		return node

class Entity(Node):
	"""
	<doc:par>Class for entities. Derive your own entities from
	it and overwrite <pyref class="Node" method="convert">convert</pyref>
	and <pyref class="Node" method="asPlainString">asPlainString</pyref>.</doc:par>
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
	<pyref var="codepoint">codepoint</pyref>.</doc:par>
	"""

	def convert(self, converter):
		node = Text(unichr(self.codepoint))
		return self._decorateNode(node)

	def asPlainString(self):
		return unichr(self.codepoint)

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

Null = Null() # Singleton, the Python way

class Attr(Frag):
	"""
	<doc:par>Base classes of all attribute classes.</doc:par>

	<doc:par>The content of an attribute may be any other XSC node. This is different from
	a normal DOM, where only text and character references are allowed. The reason for
	this is to allow dynamic content (implemented as elements or processing instructions)
	to be put into attributes.</doc:par>

	<doc:par>Of course, this dynamic content when finally converted to HTML will normally result in
	a fragment consisting only of text and character references.</doc:par>
	"""

	def present(self, presenter):
		presenter.presentAttr(self)

	def publish(self, publisher):
		if publisher.inAttr:
			raise errors.IllegalAttrNodeError(self)
		publisher.inAttr = 1
		Frag.publish(self, publisher)
		publisher.inAttr = 0

	def __cmp__(self, other):
		"""
		<doc:par>compares the attribute with another attribute,
		or to a string (8bit or Unicode) based on the
		<pyref class="Node" method="asPlainString">asPlainString</pyref> value.</doc:par>
		"""
		if type(other) in (types.StringType, types.UnicodeType):
			return cmp(self.asPlainString(), other)
		elif isinstance(other, Attr):
			return cmp(self.asPlainString(), other.asPlainString())
		else:
			raise TypeError("can't compare Attr with %s" % type(other))

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
		publisher.inAttr = 1
		u = self.asURL().relativeTo(publisher.base)
		Text(u.asPlainString()).publish(publisher)
		publisher.inAttr = 0

	def asURL(self):
		return url.URL(self.asPlainString())

	def forInput(self, publisher=None):
		u = self.asURL()
		if publisher is not None:
			u = url.URL(publisher.root)/url.URL(publisher.file)/u
		if u.scheme == "server":
			u = url.URL(scheme="http", server=options.server)/u
		return u

	def imageSize(self, publisher=None):
		"""
		returns the size of an image as a tuple or None if the image shouldn't be read
		"""
		return self.forInput(publisher).imageSize()

	def fileSize(self, publisher=None):
		"""
		returns the size of a file in bytes or None if the file shouldn't be read
		"""
		return self.forInput(publisher).fileSize()

	def open(self, publisher=None):
		"""
		opens the URL via urllib
		"""
		return self.forInput(publisher).open()

###
###
###

class Namespace:
	"""
	<doc:par>an &xml; namespace, contains the classes for the elements, entities and processing instructions
	in the namespace.</doc:par>
	"""

	def __init__(self, prefix, uri, thing=None):
		self.prefix = helpers.unistr(prefix)
		self.uri = helpers.unistr(uri)
		self.elementsByName = {} # dictionary for mapping element names to classes
		self.entitiesByName = {} # dictionary for mapping entity names to classes
		self.procInstsByName = {} # dictionary for mapping processing instruction target names to classes
		self.charrefsByName = {} # dictionary for mapping character reference names to classes
		self.charrefsByNumber = {} # dictionary for mapping character reference code points to classes
		self.register(thing)
		namespaceRegistry.register(self)

	def register(self, thing):
		"""
		<doc:par>this function lets you register <pyref arg="thing">thing</pyref> in the namespace.
		If <pyref arg="thing">thing</pyref> is a class derived from <pyref class="Element">Element</pyref>,
		<pyref class="Entity">Entity</pyref> or <pyref class="ProcInst">ProcInst</pyref> it will be registered
		under it's class name (<code><pyref arg="thing">thing</pyref>.__name__</code>). If you want
		to change this behaviour, do the following: set a class variable <code>name</code> to
		the name you want to be used. If you don't want <pyref arg="thing">thing</pyref> to be
		registered at all, set <code>register</code> to <code>None</code>.</doc:par>

		<doc:par>After the call <pyref arg="thing">thing</pyref> will have two class attributes:
		<code>name</code>, which is the name under which the class is registered and
		<code>namespace</code>, which is the namespace itself (i.e. <self/>).</doc:par>

		<doc:par>If <pyref arg="thing">thing</pyref> already has an attribute <code>namespace</code>,
		it won't be registered again.</doc:par>

		<doc:par>If <pyref arg="thing">thing</pyref> is a dictionary, every object in the dictionary
		will be registered.</doc:par>

		<doc:par>All other objects are ignored.</doc:par>
		"""

		t = type(thing)
		if t is types.ClassType:
			iselement = thing is not Element and issubclass(thing, Element)
			isentity = thing is not Entity and issubclass(thing, Entity)
			if isentity:
				ischarref = thing is not CharRef and issubclass(thing, CharRef)
				if ischarref:
					isentity = 0
			else:
				ischarref = 0
			isprocinst = thing is not ProcInst and issubclass(thing, ProcInst)
			if iselement or isentity or ischarref or isprocinst:
				# if the class attribute register is 0, the class won't be registered
				# and if the class already has a _ns attribute, it is already registered, so it won't be registered again
				# (we're accessing __dict__ here, because we don't want the attribute from the base class object)
				if thing.register and (not thing.__dict__.has_key("_ns")):
					try:
						name = thing.__dict__["name"] # no inheritance, otherwise we might get the name attribute from an already registered base class
					except KeyError:
						name = thing.__name__
					thing._ns = self # this creates a cycle
					if name is not None:
						name = helpers.unistr(name)
						thing.name = name
						if iselement:
							self.elementsByName[name] = thing
						elif isentity:
							self.entitiesByName[name] = thing
						elif ischarref:
							self.charrefsByName[name] = thing
							self.charrefsByNumber.setdefault(thing.codepoint, []).append(thing)
						else: # if isprocinst:
							self.procInstsByName[name] = thing
		elif t is types.DictionaryType:
			for key in thing.keys():
				self.register(thing[key])

	def __repr__(self):
		return "<%s.%s instance prefix=%r uri=%r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.prefix, self.uri, id(self))

class NamespaceRegistry:
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
		if not namespace in self.sequential:
			self.sequential.insert(0, namespace)

namespaceRegistry = NamespaceRegistry()

class Namespaces:
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
		pushes the namespaces onto the stack in this order,
		i.e. the last one in the list will be the first
		one to be searched.

		items in namespaces can be:
			1. namespace objects,
			2. Module objects, in which case module.namespace
			   will be used as the Namespace object
			3. strings, which specify the namespace
			   prefix, i.e. namespaceRegistry.byPrefix[string]
			   will be used.
		"""
		for namespace in namespaces:
			if type(namespace) is types.ModuleType:
				namespace = namespace.namespace
			elif type(namespace) in (types.StringType, types.UnicodeType):
				namespace = namespaceRegistry.byPrefix[namespace]
			self.namespaces.insert(0, namespace) # built in reverse order, so a simple "for in" finds the most recent entry.

	def popNamespace(self, count=1):
		del self.namespaces[:count]

	def __splitName(self, name):
		"""
		split a qualified name into a namespace,name pair
		"""
		name = name.split(":")
		if len(name) == 1: # no namespace specified
			name.insert(0, None)
		return name

	def __allNamespaces(self):
		"""
		returns a list of all namespaces to be searched in this order
		"""
		return self.namespaces+namespaceRegistry.sequential

	def elementFromName(self, name):
		"""
		returns the element class for the name name (which might include a namespace).
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
		returns the entity or charref class for the name name (which might include a namespace).
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
			if name[0] is None or name[0] == namespace.prefix:
				try:
					return namespace.entitiesByName[name[1]]
				except KeyError: # no entity in this namespace with this name
					pass
		raise errors.IllegalEntityError(name) # entities with this name couldn't be found

	def procInstFromName(self, name):
		"""
		returns the processing instruction class for the name name (which might include a namespace).
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
		returns the first charref class for the codepoint number.
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

class Location:
	"""
	<doc:par>Represents a location in an &xml; entity.</doc:par>
	"""

	def __init__(self, locator=None, sysID=None, pubID=None, lineNumber=-1, columnNumber=-1):
		"""
		<doc:par>Initialized by being passed a <pyref arg="locator">locator</pyref>, from which it reads
		off the current location, which is then stored internally. In addition to that the system ID,
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
			columnNumber = -1
		else:
			columnNumber = 1
		return Location(sysID=self.__sysID, pubID=self.__pubID, lineNumber=self.__lineNumber+offset, columnNumber=columnNumber)

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
