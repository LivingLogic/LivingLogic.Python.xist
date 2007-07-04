#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2007 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2007 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
This module contains all the central &xml; tree classes, the namespace classes,
exception and warning classes and a few helper classes and functions.
"""


__version__ = "$Revision$".split()[1]
# $Source$


import sys, os, random, copy, warnings, cPickle, threading, weakref, itertools, types

from ll import misc, url as url_

try:
	 import astyle
except ImportError:
	astyle = None

# IPython/ipipe support
try:
	import ipipe
except ImportError:
	ipipe = None


local = threading.local()

def getstack():
	try:
		stack = getattr(local, "ll.xist.xsc.nodes")
	except AttributeError:
		stack = []
		setattr(local, "ll.xist.xsc.nodes", stack)
	return stack


xml_xmlns = "http://www.w3.org/XML/1998/namespace"


###
### helpers
###

def tonode(value):
	"""
	<par>convert <arg>value</arg> to an &xist; <pyref class="Node"><class>Node</class></pyref>.</par>

	<par>If <arg>value</arg> is a tuple or list, it will be (recursively) converted
	to a <pyref class="Frag"><class>Frag</class></pyref>. Integers, strings, etc.
	will be converted to a <pyref class="Text"><class>Text</class></pyref>.
	If <arg>value</arg> is a <pyref class="Node"><class>Node</class></pyref> already,
	it will be returned unchanged. In the case of <lit>None</lit> the &xist; Null
	(<class>ll.xist.xsc.Null</class>) will be returned. If <arg>value</arg> is
	iterable, a <class>Frag</class> will be generated from the items.
	Anything else will issue a warning and will be ignored (by returning
	<class>Null</class>).</par>
	"""
	if isinstance(value, Node):
		if isinstance(value, Attrs):
			raise IllegalObjectError(value)
		# we don't have to turn an Attr into a Frag, because this will be done once the Attr is put back into the tree
		return value
	elif isinstance(value, (basestring, int, long, float)):
		return Text(value)
	elif value is None:
		return Null
	elif isinstance(value, (list, tuple)):
		return Frag(*value)
	elif isinstance(value, url_.URL):
		return Text(value)
	elif not isinstance(value, _Node_Meta): # avoid Node classes (whose __getitem__() returns an xfind selector)
		# Maybe it's an iterator/generator?
		try:
			return Frag(*list(value))
		except TypeError:
			pass
	raise IllegalObjectError(value) # none of the above => bail out


def add(*args, **kwargs):
	"""
	<function>add</function> appends items in <arg>args</arg> and sets attributes
	in <arg>kwargs</arg> in the currenly active node in the <lit>with</lit> stack.
	"""
	getstack()[-1](*args, **kwargs)


###
### Magic constants for tree traversal
###

entercontent = misc.Const("entercontent")
enterattrs = misc.Const("enterattrs")


###
### Common walk filters
###

class WalkFilter(object):
	"""
	A <class>WalkFilter</class> can be passed to the
	<pyref class="Node" method="walk"><method>walk</method></pyref> method of
	nodes to specify how to traverse the tree and which nodes to output.
	"""
	@misc.notimplemented
	def filter(self, path):
		pass


class FindType(WalkFilter):
	"""
	Tree traversal filter that finds nodes of a certain type on the first level
	of the tree without decending further down.
	"""
	def __init__(self, *types):
		self.types = types

	def filter(self, path):
		return (isinstance(path[-1], self.types), )


class FindTypeAll(WalkFilter):
	"""
	Tree traversal filter that finds nodes of a certain type searching the
	complete tree.
	"""
	def __init__(self, *types):
		self.types = types

	def filter(self, path):
		return (isinstance(path[-1], self.types), entercontent)


class FindTypeAllAttrs(WalkFilter):
	"""
	Tree traversal filter that finds nodes of a certain type searching the
	complete tree (including attributes).
	"""
	def __init__(self, *types):
		self.types = types

	def filter(self, path):
		return (isinstance(path[-1], self.types), entercontent, enterattrs)


class FindTypeTop(WalkFilter):
	"""
	Tree traversal filter that finds nodes of a certain type searching the
	complete tree, but traversal of the children of a node is skipped if this
	node is of the specified type.
	"""
	def __init__(self, *types):
		self.types = types

	def filter(self, path):
		if isinstance(path[-1], self.types):
			return (True,)
		else:
			return (entercontent,)


class CallableWalkFilter(WalkFilter):
	"""
	Tree traversal filter that returns the result of a function call.
	"""
	def __init__(self, func):
		self.func = func

	def filter(self, path):
		return self.func(path)


class ConstantWalkFilter(WalkFilter):
	"""
	Tree traversal filter that returns the same value for all nodes.
	"""
	def __init__(self, value):
		self.value = value

	def filter(self, path):
		return self.value


###
### Conversion context
###

class Context(object):
	"""
	<par>This is an empty class, that can be used by the
	<pyref class="Node" method="convert"><method>convert</method></pyref>
	method to hold element or namespace specific data during the convert call.
	The method <pyref class="Converter" method="__getitem__"><method>Converter.__getitem__</method></pyref>
	will return a unique instance of this class.</par>
	"""
	__fullname__ = "Context"


###
### Exceptions and warnings
###

class Error(Exception):
	"""
	Base class for all &xist; exceptions
	"""
	pass


class Warning(UserWarning):
	"""
	Base class for all warning exceptions (i.e. those that won't
	result in a program termination.)
	"""
	pass


class IllegalAttrValueWarning(Warning):
	"""
	Warning that is issued when an attribute has an illegal value when parsing or publishing.
	"""

	def __init__(self, attr):
		self.attr = attr

	def __str__(self):
		attr = self.attr
		return "Attribute value %r not allowed for %s" % (unicode(attr), attr._str(fullname=True, xml=False, decorate=False))


class RequiredAttrMissingWarning(Warning):
	"""
	Warning that is issued when a required attribute is missing during parsing or publishing.
	"""

	def __init__(self, attrs, reqattrs):
		self.attrs = attrs
		self.reqattrs = reqattrs

	def __str__(self):
		return "Required attribute%s %s missing in %s" % (("s" if len(self.reqattrs)>1 else ""), ", ".join(attr.__class__.__name__ for attr in self.reqattrs), self.attrs._str(fullname=True, xml=False, decorate=False))


class IllegalDTDChildWarning(Warning):
	"""
	Warning that is issued when the <pyref module="ll.xist.parsers" class="HTMLParser"><class>HTMLParser</class></pyref>
	detects an element that is not allowed inside its parent element according to the &html; &dtd;
	"""

	def __init__(self, childname, parentname):
		self.childname = childname
		self.parentname = parentname

	def __str__(self):
		return "Element %s not allowed as a child of element %s" % (self.childname, self.parentname)


class IllegalCloseTagWarning(Warning):
	"""
	Warning that is issued when the <pyref module="ll.xist.parsers" class="HTMLParser"><class>HTMLParser</class></pyref>
	finds an end tag that has no corresponding start tag.
	"""

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "Element %s has never been opened" % (self.name,)


class PrefixNeededError(Error, ValueError):
	"""
	Exception that is raised when something requires a prefix on publishing.
	"""
	def __init__(self, xmlns):
		self.xmlns = xmlns

	def __str__(self):
		return "namespace %s needs a prefix" % nsclark(self.xmlns)


class IllegalPrefixError(Error, LookupError):
	"""
	Exception that is raised when a namespace prefix is undefined.
	"""
	def __init__(self, prefix):
		self.prefix = prefix

	def __str__(self):
		return "namespace prefix %s is undefined" % (self.prefix,)


class IllegalNamespaceError(Error, LookupError):
	"""
	Exception that is raised when a namespace name is undefined
	i.e. if there is no namespace with this name.
	"""
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "namespace name %s is undefined" % (self.name,)


class IllegalElementError(Error, LookupError):
	"""
	Exception that is raised, when an illegal element class is requested
	"""

	def __init__(self, name, xmlns, xml=False):
		self.name = name
		self.xmlns = xmlns
		self.xml = xml

	def __str__(self):
		xmlns = self.xmlns
		if isinstance(xmlns, (list, tuple)):
			if len(xmlns) > 1:
				return "no element with %s name %s in namespaces %s" % (("Python", "XML")[self.xml], self.name, ", ".join(nsclark(xmlns) for xmlns in xmlns))
			xmlns = xmlns[0]
		return "no element with %s name %s%s" % (("Python", "XML")[self.xml], nsclark(xmlns), self.name)


class IllegalProcInstError(Error, LookupError):
	"""
	Exception that is raised, when an illegal procinst class is requested
	"""

	def __init__(self, name, xml=False):
		self.name = name
		self.xml = xml

	def __str__(self):
		return "no procinst with %s name %s" % (("Python", "XML")[self.xml], self.name)


class IllegalEntityError(Error, LookupError):
	"""
	Exception that is raised, when an illegal entity class is requested
	"""

	def __init__(self, name, xml=False):
		self.name = name
		self.xml = xml

	def __str__(self):
		return "no entity with %s name %s" % (("Python", "XML")[self.xml], self.name)


class IllegalCharRefError(Error, LookupError):
	"""
	Exception that is raised, when an illegal charref class is requested
	"""

	def __init__(self, name, xml=False):
		self.name = name
		self.xml = xml

	def __str__(self):
		if isinstance(self.name, (int, long)):
			return "no charref with codepoint %s" % self.name
		return "no charref with %s name %s" % (("Python", "XML")[self.xml], self.name)


class IllegalAttrError(Error, LookupError):
	"""
	Exception that is raised, when an illegal attribute is requested.
	"""

	def __init__(self, name, cls, xml=False):
		self.name = name
		self.cls = cls
		self.xml = xml

	def __str__(self):
		if isinstance(self.name, basestring):
			return "no local attribute with %s name %s in %r" % (("Python", "XML")[self.xml], self.name, self.cls)
		elif self.name.xmlns is None:
			return "no local attribute with class %r in %r" % (self.name, self.cls)
		else:
			return "no global attribute with class %r" % self.name


class AmbiguousNodeError(Error, LookupError):
	"""
	exception that is raised, when an node class is ambiguous (most commonly for processing instructions or entities)
	"""

	type = "node"

	def __init__(self, name, xml=False):
		self.name = name
		self.xml = xml

	def __str__(self):
		return "%s with %s name %s is ambigous" % (self.type, ("Python", "XML")[self.xml], self.name)


class AmbiguousProcInstError(AmbiguousNodeError):
	type = "procinst"


class AmbiguousEntityError(AmbiguousNodeError):
	type = "entity"


class AmbiguousCharRefError(AmbiguousNodeError):
	type = "charref"

	def __str__(self):
		if isinstance(self.name, (int, long)):
			return "%s with codepoint %s is ambigous" % (self.type, self.name)
		else:
			return AmbiguousNodeError.__str__(self)


class MultipleRootsError(Error):
	def __str__(self):
		return "can't add namespace attributes: XML tree has multiple roots"


class ElementNestingError(Error):
	"""
	Exception that is raised, when an element has an illegal nesting
	(e.g. <lit>&lt;a&gt;&lt;b&gt;&lt;/a&gt;&lt;/b&gt;</lit>)
	"""

	def __init__(self, expectedelement, foundelement):
		self.expectedelement = expectedelement
		self.foundelement = foundelement

	def __str__(self):
		return "mismatched element nesting (close tag for %s expected; close tag for %s found)" % (self.expectedelement._str(fullname=True, xml=False, decorate=True), self.foundelement._str(fullname=True, xml=False, decorate=True))


class IllegalAttrNodeError(Error):
	"""
	Exception that is raised, when something is found in an attribute that
	doesn't belong there (e.g. an element or a comment).
	"""

	def __init__(self, node):
		self.node = node

	def __str__(self):
		return "illegal node of type %s found inside attribute" % self.node.__class__.__name__


class NodeNotFoundError(Error):
	"""
	Exception that is raised when <pyref module="ll.xist.xsc" class="Node" method="findfirst"><method>findfirst</method></pyref> fails.
	"""
	def __str__(self):
		return "no appropriate node found"


class FileNotFoundWarning(Warning):
	"""
	Warning that is issued, when a file can't be found.
	"""
	def __init__(self, message, filename, exc):
		Warning.__init__(self, message, filename, exc)
		self.message = message
		self.filename = filename
		self.exc = exc

	def __str__(self):
		return "%s: %r not found (%s)" % (self.message, self.filename, self.exc)


class IllegalObjectError(TypeError):
	"""
	Exception that is raised when an &xist; constructor gets passed an unconvertable object.
	"""

	def __init__(self, object):
		self.object = object

	def __str__(self):
		return "can't convert object %r of type %s to an XIST node" % (self.object, type(self.object).__name__)


class MalformedCharRefWarning(Warning):
	"""
	Exception that is raised when a character reference is malformed (e.g. <lit>&amp;#foo;</lit>)
	"""

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "malformed character reference: &%s;" % self.name


class IllegalCommentContentWarning(Warning):
	"""
	Warning that is issued when there is an illegal comment, i.e. one
	containing <lit>--</lit> or ending in <lit>-</lit>.
	(This can only happen, when the comment is instantiated by the
	program, not when parsed from an &xml; file.)
	"""

	def __init__(self, comment):
		self.comment = comment

	def __str__(self):
		return "comment with content %r is illegal, as it contains '--' or ends in '-'." % self.comment.content


class IllegalProcInstFormatError(Error):
	"""
	Exception that is raised, when there is an illegal processing instruction, i.e. one containing <lit>?&gt;</lit>.
	(This can only happen, when the processing instruction is instantiated by the
	program, not when parsed from an &xml; file.)
	"""

	def __init__(self, procinst):
		self.procinst = procinst

	def __str__(self):
		return "processing instruction with content %r is illegal, as it contains '?>'." % self.procinst.content


class IllegalXMLDeclFormatError(Error):
	"""
	Exception that is raised, when there is an illegal XML declaration,
	i.e. there something wrong in <lit>&lt;?xml ...?&gt;</lit>.
	(This can only happen, when the processing instruction is instantiated by the
	program, not when parsed from an &xml; file.)
	"""

	def __init__(self, procinst):
		self.procinst = procinst

	def __str__(self):
		return "XML declaration with content %r is malformed." % self.procinst.content


class ParseWarning(Warning):
	"""
	General warning issued during parsing.
	"""


class IllegalElementParseWarning(IllegalElementError, ParseWarning):
	"""
	Warning about an illegal element that is issued during parsing.
	"""
warnings.filterwarnings("error", category=IllegalElementParseWarning)


class IllegalProcInstParseWarning(IllegalProcInstError, ParseWarning):
	"""
	Warning about an illegal processing instruction that is issued during parsing.
	"""
warnings.filterwarnings("error", category=IllegalProcInstParseWarning)


class AmbiguousProcInstParseWarning(AmbiguousProcInstError, ParseWarning):
	"""
	Warning about an ambigous processing instruction that is issued during parsing.
	"""
warnings.filterwarnings("error", category=AmbiguousProcInstParseWarning)


class IllegalEntityParseWarning(IllegalEntityError, ParseWarning):
	"""
	Warning about an illegal entity that is issued during parsing.
	"""
warnings.filterwarnings("error", category=IllegalEntityParseWarning)


class AmbiguousEntityParseWarning(AmbiguousEntityError, ParseWarning):
	"""
	Warning about an ambigous entity that is issued during parsing.
	"""
warnings.filterwarnings("error", category=AmbiguousEntityParseWarning)


class IllegalCharRefParseWarning(IllegalCharRefError, ParseWarning):
	"""
	Warning about an illegal character references that is issued during parsing.
	"""
warnings.filterwarnings("error", category=IllegalCharRefParseWarning)


class AmbiguousCharRefParseWarning(AmbiguousCharRefError, ParseWarning):
	"""
	Warning about an ambigous character references that is issued during parsing.
	"""
warnings.filterwarnings("error", category=AmbiguousCharRefParseWarning)


class IllegalAttrParseWarning(IllegalAttrError, ParseWarning):
	"""
	Warning about an illegal attribute that is issued during parsing.
	"""
warnings.filterwarnings("error", category=IllegalAttrParseWarning)


class NodeOutsideContextError(Error):
	"""
	Error that is raised, when a convert method can't find required context info.
	"""

	def __init__(self, node, outerclass):
		self.node = node
		self.outerclass = outerclass

	def __str__(self):
		return "node %s outside of %s" % (self.node._str(fullname=True, xml=False, decorate=True), self.outerclass._str(fullname=True, xml=False, decorate=True))


###
### The DOM classes
###

class _Node_Meta(type):
	def __new__(cls, name, bases, dict):
		dict["__fullname__"] = name
		if "register" not in dict:
			dict["register"] = True
		if "xmlname" not in dict:
			dict["xmlname"] = name.rsplit(".", 1)[-1]
		return type.__new__(cls, name, bases, dict)

	def __repr__(self):
		return "<class %s:%s at 0x%x>" % (self.__module__, self.__fullname__, id(self))

	def __div__(self, other):
		from ll.xist import xfind
		return xfind.IsInstanceSelector(self) / other

	def __floordiv__(self, other):
		from ll.xist import xfind
		return xfind.IsInstanceSelector(self) // other

	def __mul__(self, other):
		from ll.xist import xfind
		return xfind.IsInstanceSelector(self) * other

	def __pow__(self, other):
		from ll.xist import xfind
		return xfind.IsInstanceSelector(self) ** other

	def __and__(self, other):
		from ll.xist import xfind
		return xfind.IsInstanceSelector(self) & other

	def __or__(self, other):
		from ll.xist import xfind
		return xfind.IsInstanceSelector(self) | other

	def __getitem__(self, index):
		from ll.xist import xfind
		return xfind.nthoftype(index, self)

	def __invert__(self):
		from ll.xist import xfind
		return xfind.NotCombinator(xfind.IsInstanceSelector(self))


class Node(object):
	"""
	base class for nodes in the document tree. Derived classes must
	overwrite <pyref method="convert"><method>convert</method></pyref>
	and may overwrite <pyref method="publish"><method>publish</method></pyref>.
	"""
	__metaclass__ = _Node_Meta

	# location of this node in the XML file (will be hidden in derived classes, but is
	# specified here, so that no special tests are required. In derived classes
	# this will be set by the parser)
	startloc = None
	endloc = None

	# Subclasses relevant for parsing (i.e. Element, ProcInst, Entity and CharRef)
	# have an additional class attribute named register. This attribute may have three values:
	# False: Don't register for parsing.
	# True:  Use for parsing.
	# If register is not set it defaults to True

	Context = Context

	def __repr__(self):
		return "<%s:%s object at 0x%x>" % (self.__module__, self.__fullname__, id(self))

	def __ne__(self, other):
		return not self==other

	xmlname = None
	xmlns = None

	@classmethod
	def _strbase(cls, fullname, xml):
		v = []
		if fullname:
			ns = cls.xmlns if xml else cls.__module__
			if ns is not None:
				v.append(ns)
				v.append(":")
		if xml:
			name = cls.xmlname
		elif fullname:
			name = cls.__fullname__
		else:
			name = cls.__name__
		v.append(name)
		return "".join(v)

	def __pos__(self):
		getstack()[-1].append(self)

	def __div__(self, other):
		from ll.xist import xfind
		return xfind.IsSelector(self) / other

	def __floordiv__(self, other):
		from ll.xist import xfind
		return xfind.IsSelector(self) // other

	def __mul__(self, other):
		from ll.xist import xfind
		return xfind.IsSelector(self) * other

	def __pow__(self, other):
		from ll.xist import xfind
		return xfind.IsSelector(self) ** other

	def __and__(self, other):
		from ll.xist import xfind
		return xfind.IsSelector(self) & other

	def __or__(self, other):
		from ll.xist import xfind
		return xfind.IsSelector(self) | other

	def clone(self):
		"""
		return a clone of <self/>. Compared to <pyref method="deepcopy"><method>deepcopy</method></pyref> <method>clone</method>
		will create multiple instances of objects that can be found in the tree more than once. <method>clone</method> can't
		clone trees that contain cycles.
		"""
		return self

	def copy(self):
		"""
		Return a shallow copy of <self/>.
		"""
		return self.__copy__()

	def __copy__(self):
		return self

	def deepcopy(self):
		"""
		Return a deep copy of <self/>.
		"""
		return self.__deepcopy__()

	def __deepcopy__(self, memo=None):
		return self

	@misc.notimplemented
	def present(self, presenter):
		"""
		<par><method>present</method> is used as a central dispatch method for
		the <pyref module="ll.xist.presenters">presenter classes</pyref>. Normally
		it is not called by the user, but internally by the presenter. The user
		should call <pyref method="repr"><method>repr</method></pyref>
		instead.</par>
		"""
		# Subclasses of Node implement this method by calling the appropriate present* method in the publisher (i.e. double dispatch)

	def conv(self, converter=None, root=None, mode=None, stage=None, target=None, lang=None, function=None, makeaction=None, makeproject=None):
		"""
		<par>Convenience method for calling <pyref method="convert"><method>convert</method></pyref>.</par>
		<par><method>conv</method> will automatically set <lit><arg>converter</arg>.node</lit> to <self/> to remember the
		<z>document root node</z> for which <method>conv</method> has been called, this means that you should not call
		<method>conv</method> in any of the recursive calls, as you would loose this information. Call
		<pyref method="convert"><method>convert</method></pyref> directly instead.</par>
		"""
		if converter is None:
			converter = converters.Converter(node=self, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, makeproject=makeproject)
			return self.convert(converter)
		else:
			converter.push(node=self, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, makeproject=makeproject)
			node = self.convert(converter)
			converter.pop()
			return node

	@misc.notimplemented
	def convert(self, converter):
		"""
		<par>implementation of the conversion method. When you define your own
		element classes you have to overwrite this method and implement the desired
		conversion.</par>

		<par>This method must return an instance of <class>Node</class>.
		It may <em>not</em> change <self/>.</par>
		"""
		pass

	@misc.notimplemented
	def __unicode__(self):
		"""
		<par>Return the character content of <self/> as a unicode string.
		This means that comments and processing instructions will be filtered out.
		For elements you'll get the element content.</par>

		<par><method>__unicode__</method> can be used everywhere where
		a plain string representation of the node is required.</par>
		"""
		pass

	def __str__(self):
		"""
		Return the character content of <self/> as a string (if possible, i.e.
		there are no characters that are unencodable in the default encoding).
		"""
		return str(unicode(self))

	def __int__(self):
		"""
		Convert the character content of <self/> to an <class>int</class>.
		"""
		return int(unicode(self))

	def __long__(self):
		"""
		Convert the character content of <self/> to an <class>long</class>.
		"""
		return long(unicode(self))

	def asFloat(self, decimal=".", ignore=""):
		"""
		<par>Convert the character content of <self/> to an <class>float</class>.
		<arg>decimal</arg> specifies which decimal separator is used in the value
		(e.g. <lit>"."</lit> (the default) or <lit>","</lit>).
		<arg>ignore</arg> specifies which character will be ignored.</par>
		"""
		s = unicode(self)
		for c in ignore:
			s = s.replace(c, u"")
		if decimal != u".":
			s = s.replace(decimal, u".")
		return float(s)

	def __float__(self):
		"""
		Convert the character content of <self/> to an <class>float</class>.
		"""
		return self.asFloat()

	def __complex__(self):
		"""
		Convert the character content of <self/> to an <class>complex</class>.
		"""
		return complex(unicode(self))

	def parsed(self, parser, start=None):
		"""
		<par>This method will be called by the parser <arg>parser</arg> once after
		<self/> is created by the parser and must return the node that is to be
		put into the tree (in most cases this is <self/>, it's used e.g. by
		<pyref class="URLAttr"><class>URLAttr</class></pyref> to incorporate
		the base <pyref module="ll.url" class="URL"><class>URL</class></pyref>
		into the attribute.</par>

		<par>For elements <function>parsed</function> will be called twice:
		Once at the beginning (i.e. before the content is parsed) with
		<lit><arg>start</arg>==True</lit> and once at the end after parsing of
		the content is finished <lit><arg>start</arg>==False</lit>. For the
		second call the return value will be ignored.</par>
		"""
		return self

	def checkvalid(self):
		"""
		<par>This method will be called when parsing or publishing to check
		whether <self/> is valid.</par>

		<par>If <self/> is found to be invalid a warning should be issued through
		the <pyref module="warnings">Python warning framework</pyref>.</par>
		"""

	@misc.notimplemented
	def publish(self, publisher):
		"""
		<par>Generate unicode strings for the node. <arg>publisher</arg> must be an instance of
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref>.</par>

		<par>The encoding and xhtml specification are taken from the <arg>publisher</arg>.</par>
		"""

	def iterbytes(self, base=None, publisher=None, **publishargs):
		"""
		<par>A generator that will produce this node as a serialized byte string.</par>

		<par>For the possible parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref>
		constructor.</par>
		"""
		if publisher is None:
			publisher = publishers.Publisher(**publishargs)

		return publisher.publish(self, base) # return a generator-iterator

	def bytes(self, base=None, publisher=None, **publishargs):
		"""
		<par>Return this node as a serialized byte string.</par>

		<par>For the possible parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref>
		constructor.</par>
		"""
		return "".join(self.iterbytes(base, publisher, **publishargs))

	def asBytes(self, base=None, publisher=None, **publishargs):
		warnings.warn("asBytes() is deprecated, use bytes() instead", DeprecationWarning)
		return "".join(self.iterbytes(base, publisher, **publishargs))

	def asString(self, base=None, publisher=None, **publishargs):
		"""
		<par>Return this node as a serialized unicode string.</par>

		<par>For the possible parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref>
		constructor.</par>
		"""
		if publisher is None:
			publisher = publishers.Publisher(**publishargs)
		encoding = publisher.encoding
		result = "".join(publisher.publish(self, base))
		return result.decode(encoding)

	def write(self, stream, *args, **publishargs):
		"""
		<par>Write <self/> to the file-like object <arg>stream</arg> (which must
		provide a <method>write</method> method).</par>

		<par>For the rest of the parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref>
		constructor.</par>
		"""
		for part in self.bytes(*args, **publishargs):
			stream.write(part)

	def _walk(self, filter, path):
		"""
		<par>Internal helper for <pyref method="walk"><method>walk</method></pyref>.</par>
		"""
		for option in filter.filter(path):
			if option is not entercontent and option is not enterattrs and option:
				yield path

	def walk(self, filter=(True, entercontent)):
		"""
		<par>Return an iterator for traversing the tree rooted at <self/>.</par>

		<par><arg>filter</arg> is used for specifying whether or not a node should
		be yielded and when the children of this node should be traversed. If
		<arg>filter</arg> is callable, it will be called for each node visited
		during the traversal. A path (i.e. a list of all nodes from the root to
		the current node) will be passed to the filter on each call and the
		filter must return a sequence of <z>node handling options</z>.
		If <arg>filter</arg> is not callable, it must be a sequence of node
		handling options that will be used for all visited nodes.</par>

		<par>Entries in this returned sequence can be the following:</par>

		<dlist>
		<term><lit>True</lit></term><item>This tells <method>walk</method> to
		yield this node from the iterator.</item>
		<term><lit>False</lit></term><item>Don't yield this node from the iterator.</item>
		<term><lit>enterattrs</lit></term><item>This is a global constant in
		<module>ll.xist.xsc</module> and tells <method>walk</method> to traverse
		the attributes of this node (if it's an
		<pyref class="Element"><class>Element</class></pyref>, otherwise this
		option will be ignored).</item>
		<term><lit>entercontent</lit></term><item>This is a global constant in
		<module>ll.xist.xsc</module> and tells <method>walk</method> to traverse
		the child nodes of this node (if it's an
		<pyref class="Element"><class>Element</class></pyref>, otherwise this
		option will be ignored).</item>
		</dlist>

		<par>These options will be executed in the order they are specified in the
		sequence, so to get a top down traversal of a tree (without entering
		attributes), the following call can be made:</par>

		<prog>
		<rep>node</rep>.walk((True, xsc.entercontent))
		</prog>

		<par>For a bottom up traversal the following call can be made:</par>

		<prog>
		<rep>node</rep>.walk((xsc.entercontent, True))
		</prog>

		<par>Each item produced by the iterator is a path list.
		<method>walk</method> reuses this list, so you can't rely on the value
		of the list being the same across calls to <method>next</method>.</par>
		"""
		from ll.xist import xfind
		filter = xfind.makewalkfilter(filter)
		return self._walk(filter, [self])

	def walknode(self, filter=(True, entercontent)):
		"""
		Return an iterator for traversing the tree. <arg>filter</arg> works the
		same as the <arg>filter</arg> argument for <pyref method="walk"><method>walk</method></pyref>.
		The items produced by the iterator are the nodes themselves.
		"""
		from ll.xist import xfind
		filter = xfind.makewalkfilter(filter)
		def iterate(path):
			for path in self._walk(filter, path):
				yield path[-1]
		return misc.Iterator(iterate([self]))

	def walkpath(self, filter=(True, entercontent)):
		"""
		Return an iterator for traversing the tree. <arg>filter</arg> works the
		same as the <arg>filter</arg> argument for <pyref method="walk"><method>walk</method></pyref>.
		The items produced by the iterator are copies of the path.
		"""
		from ll.xist import xfind
		filter = xfind.makewalkfilter(filter)
		def iterate(path):
			for path in self._walk(filter, path):
				yield path[:]
		return misc.Iterator(iterate([self]))

	def compact(self):
		"""
		Return a version of <self/>, where textnodes or character references that
		contain only linefeeds are removed, i.e. potentially needless whitespace
		is removed.
		"""
		return self

	def _decoratenode(self, node):
		"""
		Decorate the <pyref class="Node"><class>Node</class></pyref>
		<arg>node</arg> with the same location information as <self/>.
		"""

		node.startloc = self.startloc
		node.endloc = self.endloc
		return node

	def mapped(self, function, converter=None, **converterargs):
		"""
		<par>Return the node mapped through the function <arg>function</arg>. This
		call works recursively (for <pyref class="Frag"><class>Frag</class></pyref>
		and <pyref class="Element"><class>Element</class></pyref>).</par>

		<par>When you want an unmodified node you simply can return <self/>.
		<method>mapped</method> will make a copy of it and fill the content
		recursively. Note that element attributes will not be mapped. When you
		return a different node from <function>function</function> this node will
		be incorporated into the result as-is.
		"""
		if converter is None:
			converter = converters.Converter(**converterargs)
		node = function(self, converter)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		return node

	def normalized(self):
		"""
		<par>Return a normalized version of <self/>, which means that consecutive
		<pyref class="Text"><class>Text</class> nodes</pyref> are merged.</par>
		"""
		return self

	def __mul__(self, factor):
		"""
		<par>Return a <pyref class="Frag"><class>Frag</class></pyref> with
		<arg>factor</arg> times the node as an entry. Note that the node will not
		be copied, i.e. it is a <z>shallow <method>__mul__</method></z>.</par>
		"""
		return Frag(*factor*[self])

	def __rmul__(self, factor):
		"""
		<par>Return a <pyref class="Frag"><class>Frag</class></pyref> with
		<arg>factor</arg> times the node as an entry.</par>
		"""
		return Frag(*[self]*factor)

	def pretty(self, level=0, indent="\t"):
		"""
		<par>Return a prettyfied version of <self/>, i.e. one with properly
		nested and indented tags (as far as possible). If an element has mixed
		content (i.e. <pyref class="Text"><class>Text</class></pyref> and
		non-<pyref class="Text"><class>Text</class></pyref> nodes) the content
		will be returned as is.</par>

		<par>Note that whitespace will prevent pretty printing too, so
		you might want to call <pyref method="normalized"><method>normalized</method></pyref>
		and <pyref method="compact"><method>compact</method></pyref> before
		calling <method>pretty</method> to remove whitespace.</par>
		"""
		if level:
			return Frag(indent*level, self)
		else:
			return self


###
### Helper functions for ipipe
###


if ipipe is not None:
	def _ipipe_type(node):
		"The type of the node"
		if node is Null:
			return "null"
		elif isinstance(node, Element):
			return "element"
		elif isinstance(node, ProcInst):
			return "procinst"
		elif isinstance(node, CharRef):
			return "charref"
		elif isinstance(node, Entity):
			return "entity"
		elif isinstance(node, Text):
			return "text"
		elif isinstance(node, Comment):
			return "comment"
		elif isinstance(node, DocType):
			return "doctype"
		elif isinstance(node, Attr):
			return "attr"
		elif isinstance(node, Frag):
			return "frag"
		return ipipe.noitem
	_ipipe_type.__xname__ = "type"


	def _ipipe_ns(node):
		"The namespace"
		return node.xmlns
	_ipipe_ns.__xname__ = "ns"


	def _ipipe_name(node):
		"The element/procinst/entity/attribute name of the node"
		if isinstance(node, (Element, ProcInst, Entity, Attr)):
			return "%s.%s" % (node.__class__.__module__, node.__fullname__)
		return ipipe.noitem
	_ipipe_name.__xname__ = "name"


	def _ipipe_childrencount(node):
		"The number of child nodes"
		if isinstance(node, Element):
			return len(node.content)
		elif isinstance(node, Frag):
			return len(node)
		return ipipe.noitem
	_ipipe_childrencount.__xname__ = "# children"


	def _ipipe_attrscount(node):
		"The number of attribute nodes"
		if isinstance(node, Element):
			return len(node.attrs)
		return ipipe.noitem
	_ipipe_attrscount.__xname__ = "# attrs"


	def _ipipe_content(node):
		"The text content"
		if isinstance(node, CharacterData):
			return unicode(node.content)
		elif isinstance(node, Attr):
			return unicode(node)
		return ipipe.noitem
	_ipipe_content.__xname__ = "content"


	@ipipe.xrepr.when_type(_Node_Meta)
	def repr_nodeclass(self, mode="default"):
		yield (astyle.style_type_type, "%s.%s" % (self.__module__, self.__fullname__))


	@ipipe.xattrs.when_type(Node)
	def xattrs_nodeclass(self, mode="default"):
		yield ipipe.AttributeDescriptor("startloc", doc="the locate in the XML file")
		yield ipipe.FunctionDescriptor(_ipipe_type)
		yield ipipe.AttributeDescriptor("xmlns", doc="the XML namespace of the node")
		yield ipipe.FunctionDescriptor(_ipipe_name, "name")
		yield ipipe.FunctionDescriptor(_ipipe_content, "content")
		if mode == "detail":
			yield ipipe.IterAttributeDescriptor("content", "the element content")
			yield ipipe.IterAttributeDescriptor("attrs", "the element attributes")
		else:
			yield ipipe.FunctionDescriptor(_ipipe_childrencount, "children")
			yield ipipe.FunctionDescriptor(_ipipe_attrscount, "attrs")


class CharacterData(Node):
	"""
	<par>Base class for &xml; character data (<pyref class="Text"><class>Text</class></pyref>,
	<pyref class="ProcInst"><class>ProcInst</class></pyref>,
	<pyref class="Comment"><class>Comment</class></pyref> and
	<pyref class="DocType"><class>DocType</class></pyref>)</par>

	<par>Provides nearly the same functionality as <class>UserString</class>,
	but omits a few methods.</par>
	"""
	__slots__ = ("_content",)

	def __init__(self, *content):
		self._content = u"".join(unicode(x) for x in content)

	def __getstate__(self):
		return self._content

	def __setstate__(self, content):
		self._content = content

	class content(misc.propclass):
		"""
		The text content of the node as a <class>unicode</class> object.
		"""
		def __get__(self):
			return self._content

	def __hash__(self):
		return self._content.__hash__()

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self._content==other._content

	def __len__(self):
		return self._content.__len__()

	def __getitem__(self, index):
		return self.__class__(self._content.__getitem__(index))

	def __add__(self, other):
		return self.__class__(self._content + other)

	def __radd__(self, other):
		return self.__class__(unicode(other) + self._content)

	def __mul__(self, n):
		return self.__class__(n * self._content)

	def __rmul__(self, n):
		return self.__class__(n * self._content)

	def __getslice__(self, index1, index2):
		return self.__class__(self._content.__getslice__(index1, index2))

	def capitalize(self):
		return self.__class__(self._content.capitalize())

	def center(self, width):
		return self.__class__(self._content.center(width))

	def count(self, sub, start=0, end=sys.maxint):
		return self._content.count(sub, start, end)

	def endswith(self, suffix, start=0, end=sys.maxint):
		return self._content.endswith(suffix, start, end)

	def index(self, sub, start=0, end=sys.maxint):
		return self._content.index(sub, start, end)

	def isalpha(self):
		return self._content.isalpha()

	def isalnum(self):
		return self._content.isalnum()

	def isdecimal(self):
		return self._content.isdecimal()

	def isdigit(self):
		return self._content.isdigit()

	def islower(self):
		return self._content.islower()

	def isnumeric(self):
		return self._content.isnumeric()

	def isspace(self):
		return self._content.isspace()

	def istitle(self):
		return self._content.istitle()

	def isupper(self):
		return self._content.isupper()

	def join(self, frag):
		return frag.withsep(self)

	def ljust(self, width, fill=u" "):
		return self.__class__(self._content.ljust(width, fill))

	def lower(self):
		return self.__class__(self._content.lower())

	def lstrip(self, chars=None):
		return self.__class__(self._content.lstrip(chars))

	def replace(self, old, new, maxsplit=-1):
		return self.__class__(self._content.replace(old, new, maxsplit))

	def rjust(self, width, fill=u" "):
		return self.__class__(self._content.rjust(width, fill))

	def rstrip(self, chars=None):
		return self.__class__(self._content.rstrip(chars))

	def rfind(self, sub, start=0, end=sys.maxint):
		return self._content.rfind(sub, start, end)

	def rindex(self, sub, start=0, end=sys.maxint):
		return self._content.rindex(sub, start, end)

	def split(self, sep=None, maxsplit=-1):
		return Frag(self._content.split(sep, maxsplit))

	def splitlines(self, keepends=0):
		return Frag(self._content.splitlines(keepends))

	def startswith(self, prefix, start=0, end=sys.maxint):
		return self._content.startswith(prefix, start, end)

	def strip(self, chars=None):
		return self.__class__(self._content.strip(chars))

	def swapcase(self):
		return self.__class__(self._content.swapcase())

	def title(self):
		return self.__class__(self._content.title())

	def translate(self, table):
		return self.__class__(self._content.translate(table))

	def upper(self):
		return self.__class__(self._content.upper())

	def __repr__(self):
		if self.startloc is not None:
			loc = " (from %s)" % self.startloc
		else:
			loc = ""
		return "<%s.%s content=%r%s at 0x%x>" % (self.__class__.__module__, self.__fullname__, self.content, loc, id(self))


class Text(CharacterData):
	"""
	<par>A text node. The characters <markup>&lt;</markup>, <markup>&gt;</markup>, <markup>&amp;</markup>
	(and <markup>"</markup> inside attributes) will be <z>escaped</z> with the
	appropriate character entities when this node is published.</par>
	"""

	def convert(self, converter):
		return self

	def __unicode__(self):
		return self._content

	def publish(self, publisher):
		yield publisher.encodetext(self._content)

	def present(self, presenter):
		return presenter.presentText(self) # return a generator-iterator

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

	def __init__(self, *content):
		list.__init__(self)
		for child in content:
			child = tonode(child)
			if isinstance(child, Frag):
				list.extend(self, child)
			elif child is not Null:
				list.append(self, child)

	def __enter__(self):
		stack = getstack()
		if stack:
			stack[-1].append(self)
		stack.append(self)
		return self

	def __exit__(self, type, value, traceback):
		getstack().pop()

	def __call__(self, *content):
		self.extend(content)
		return self

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = cls._strbase(fullname=fullname, xml=xml)
		if decorate:
			s = "<%s>" % s
		return s

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
		Make <self/> empty.
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
		list.extend(node, (child.clone() for child in self))
		return self._decoratenode(node)

	def __copy__(self):
		"""
		helper for the <pyref module="copy"><module>copy</module></pyref> module.
		"""
		node = self._create()
		list.extend(node, self)
		return self._decoratenode(node)

	def __deepcopy__(self, memo=None):
		"""
		helper for the <pyref module="copy"><module>copy</module></pyref> module.
		"""
		node = self._create()
		if memo is None:
			memo = {}
		memo[id(self)] = node
		list.extend(node, (copy.deepcopy(child, memo) for child in self))
		return self._decoratenode(node)

	def present(self, presenter):
		return presenter.presentFrag(self) # return a generator-iterator

	def __unicode__(self):
		return u"".join(unicode(child) for child in self)

	def __eq__(self, other):
		return self.__class__ is other.__class__ and list.__eq__(self, other)

	def publish(self, publisher):
		for child in self:
			for part in child.publish(publisher):
				yield part

	def __getitem__(self, index):
		"""
		<par>Return the <arg>index</arg>'th node for the content of the fragment.
		If <arg>index</arg> is a list <method>__getitem__</method> will work
		recursively. If <arg>index</arg> is an empty list, <self/> will be returned.</par>
		"""
		if isinstance(index, list):
			node = self
			for subindex in index:
				node = node[subindex]
			return node
		elif isinstance(index, _Node_Meta):
			def iterate(self, index):
				for child in self:
					if isinstance(child, index):
						yield child
			return misc.Iterator(iterate(self, index))
		elif isinstance(index, slice):
			return self.__class__(list.__getitem__(self, index))
		else:
			return list.__getitem__(self, index)

	def __setitem__(self, index, value):
		"""
		<par>Allows you to replace the <arg>index</arg>'th content node of the fragment
		with the new value <arg>value</arg> (which will be converted to a node).
		If  <arg>index</arg> is a list <method>__setitem__</method> will be applied
		to the innermost index after traversing the rest of <arg>index</arg> recursively.
		If <arg>index</arg> is an empty list, an exception will be raised.</par>
		"""
		if isinstance(index, list):
			if not index:
				raise ValueError("can't replace self")
			node = self
			for subindex in index[:-1]:
				node = node[subindex]
			node[index[-1]] = value
		else:
			value = Frag(value)
			if isinstance(index, slice):
				list.__setitem__(self, index, value)
			else:
				if index==-1:
					l = len(self)
					list.__setslice__(self, l-1, l, value)
				else:
					list.__setslice__(self, index, index+1, value)

	def __delitem__(self, index):
		"""
		<par>Remove the <arg>index</arg>'th content node from the fragment.
		If <arg>index</arg> is a list, the innermost index will be deleted,
		after traversing the rest of <arg>index</arg> recursively.
		If <arg>index</arg> is an empty list, an exception will be raised.</par>
		"""
		if isinstance(index, list):
			if not index:
				raise ValueError("can't delete self")
			node = self
			for subindex in index[:-1]:
				node = node[subindex]
			del node[index[-1]]
		else:
			list.__delitem__(self, index)

	def __getslice__(self, index1, index2):
		"""
		Returns slice of the content of the fragment.
		"""
		node = self._create()
		list.extend(node, list.__getslice__(self, index1, index2))
		return node

	def __setslice__(self, index1, index2, sequence):
		"""
		Replace a slice of the content of the fragment
		"""
		list.__setslice__(self, index1, index2, Frag(sequence))

	# no need to implement __delslice__

	def __mul__(self, factor):
		"""
		Return a <pyref class="Frag"><class>Frag</class></pyref> with
		<arg>factor</arg> times the content of <self/>. Note that no copies of the
		content will be generated, so this is a <z>shallow <method>__mul__</method></z>.
		"""
		node = self._create()
		list.extend(node, list.__mul__(self, factor))
		return node

	__rmul__ = __mul__

	def __iadd__(self, other):
		self.extend(other)
		return self

	# no need to implement __len__ or __nonzero__

	def append(self, *others):
		"""
		<par>Append every item in <arg>others</arg> to <self/>.</par>
		"""
		for other in others:
			other = tonode(other)
			if isinstance(other, Frag):
				list.extend(self, other)
			elif other is not Null:
				list.append(self, other)

	def extend(self, items):
		"""
		<par>Append all items from the sequence <arg>items</arg> to <self/>.</par>
		"""
		self.append(items)

	def insert(self, index, *others):
		"""
		<par>Insert all items in <arg>others</arg> at the position <arg>index</arg>.
		(this is the same as <lit><self/>[<arg>index</arg>:<arg>index</arg>] = <arg>others</arg></lit>)
		"""
		other = Frag(*others)
		list.__setslice__(self, index, index, other)

	def _walk(self, filter, path):
		path.append(None)
		for child in self:
			path[-1] = child
			for result in child._walk(filter, path):
				yield result
		path.pop()

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
		<par>Return a version of <self/> with a separator node between the nodes of <self/>.</par>

		<par>if <arg>clone</arg> is false one node will be inserted several times,
		if <arg>clone</arg> is true, clones of this node will be used.</par>
		"""
		node = self._create()
		newseparator = tonode(separator)
		for child in self:
			if len(node):
				node.append(newseparator)
				if clone:
					newseparator = newseparator.clone()
			node.append(child)
		return node

	def sorted(self, cmp=None, key=None, reverse=False):
		"""
		<par>Return a sorted version of the <self/>. <arg>cmp</arg>, <arg>key</arg>
		and <arg>reverse</arg> have to same meaning as for the builtin function
		<function>sorted</function>.
		"""
		return self.__class__(sorted(self, cmp, key, reverse))

	def reversed(self):
		"""
		<par>Return a reversed version of the <self/>.</par>
		"""
		node = list(self)
		node.reverse()
		return self.__class__(node)

	def filtered(self, function):
		"""
		<par>Return a filtered version of the <self/>, i.e. a copy of <self/>,
		where only content nodes for which <function>function</function> returns
		true will be copied.</par>
		"""
		node = self._create()
		list.extend(node, (child for child in self if function(child)))
		return node

	def shuffled(self):
		"""
		<par>Return a shuffled version of <self/>, i.e. a copy of <self/> where
		the content nodes are randomly reshuffled.</par>
		"""
		content = list(self)
		node = self._create()
		while content:
			index = random.randrange(len(content))
			list.append(node, content[index])
			del content[index]
		return node

	def mapped(self, function, converter=None, **converterargs):
		if converter is None:
			converter = converters.Converter(**converterargs)
		node = function(self, converter)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = self._create()
			for child in self:
				node.append(child.mapped(function, converter))
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
		for (i, child) in enumerate(self):
			if i:
				node.append("\n")
			node.append(child.pretty(level, indent))
		return node

	def __repr__(self):
		l = len(self)
		if l==0:
			info = "no children"
		elif l==1:
			info = "1 child"
		else:
			info = "%d children" % l
		loc = " (from %s)" % self.startloc if self.startloc is not None else ""
		return "<%s.%s object (%s)%s at 0x%x>" % (self.__class__.__module__, self.__fullname__, info, loc, id(self))


class Comment(CharacterData):
	"""
	An &xml; comment.
	"""

	def convert(self, converter):
		return self

	def __unicode__(self):
		return u""

	def present(self, presenter):
		return presenter.presentComment(self)  # return a generator-iterator

	def publish(self, publisher):
		if publisher.inattr:
			raise IllegalAttrNodeError(self)
		content = self.content
		if u"--" in content or content.endswith(u"-"):
			warnings.warn(IllegalCommentContentWarning(self))
		yield publisher.encode(u"<!--")
		yield publisher.encode(content)
		yield publisher.encode(u"-->")


class _DocType_Meta(Node.__metaclass__):
	def __repr__(self):
		return "<doctype class %s:%s at 0x%x>" % (self.__module__, self.__fullname__, id(self))


class DocType(CharacterData):
	"""
	An &xml; document type declaration.
	"""

	__metaclass__ = _DocType_Meta

	def convert(self, converter):
		return self

	def present(self, presenter):
		return presenter.presentDocType(self) # return a generator-iterator

	def publish(self, publisher):
		if publisher.inattr:
			raise IllegalAttrNodeError(self)
		yield publisher.encode(u"<!DOCTYPE ")
		yield publisher.encode(self.content)
		yield publisher.encode(u">")

	def __unicode__(self):
		return u""


class _ProcInst_Meta(Node.__metaclass__):
	def __new__(cls, name, bases, dict):
		self = super(_ProcInst_Meta, cls).__new__(cls, name, bases, dict)
		if dict.get("register") is not None: # check here as getpoolstack isn't defined yet
			getpoolstack()[-1].register(self)
		return self

	def __repr__(self):
		return "<procinst class %s:%s at 0x%x>" % (self.__module__, self.__fullname__, id(self))


class ProcInst(CharacterData):
	"""
	<par>Base class for processing instructions. This class is abstract.</par>

	<par>Processing instructions for specific targets must
	be implemented as subclasses of <class>ProcInst</class>.</par>
	"""
	__metaclass__ = _ProcInst_Meta

	register = None

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = cls._strbase(fullname=fullname, xml=xml)
		if decorate:
			s = "<%s>" % s
		return s

	def convert(self, converter):
		return self

	def present(self, presenter):
		return presenter.presentProcInst(self) # return a generator-iterator

	def publish(self, publisher):
		content = self.content
		if u"?>" in content:
			raise IllegalProcInstFormatError(self)
		yield publisher.encode(u"<?")
		yield publisher.encode(self.xmlname)
		yield publisher.encode(u" ")
		yield publisher.encode(content)
		yield publisher.encode(u"?>")

	def __unicode__(self):
		return u""

	def __repr__(self):
		if self.startloc is not None:
			loc = " (from %s)" % self.startloc
		else:
			loc = ""
		return "<%s.%s procinst content=%r%s at 0x%x>" % (self.__class__.__module__, self.__fullname__, self.content, loc, id(self))


class Null(CharacterData):
	"""
	node that does not contain anything.
	"""

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = cls._strbase(fullname=fullname, xml=xml)
		if decorate:
			s = "<%s>" % s
		return s

	def convert(self, converter):
		return self

	def publish(self, publisher):
		if False:
			yield ""

	def present(self, presenter):
		return presenter.presentNull(self) # return a generator-iterator

	def __unicode__(self):
		return u""

	def __repr__(self):
		return "<null>"


Null = Null() # Singleton, the Python way


class _Attr_Meta(Frag.__metaclass__):
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
				dict["values"] = tuple(unicode(entry) for entry in values)
		self = super(_Attr_Meta, cls).__new__(cls, name, bases, dict)
		if self.xmlns is not None:
			getpoolstack()[-1].register(self)
		return self

	def __repr__(self):
		return "<attribute class %s:%s at 0x%x>" % (self.__module__, self.__fullname__, id(self))


class Attr(Frag):
	"""
	<par>Base class of all attribute classes.</par>

	<par>The content of an attribute may be any other &xist; node. This is different from
	a normal &dom;, where only text and character references are allowed. The reason for
	this is to allow dynamic content (implemented as elements or processing instructions)
	to be put into attributes.</par>

	<par>Of course, this dynamic content when finally converted to &html; will normally result in
	a fragment consisting only of text and character references. But note that it is allowed
	to have elements and processing instructions inside of attributes even when publishing.
	Processing instructions will be published as is and for elements their content will be
	published.</par>
	<example><title>Elements inside attributes</title>
	<tty>
	<prompt>&gt;&gt;&gt; </prompt><input>from ll.xist.ns import html, php</input>
	<prompt>&gt;&gt;&gt; </prompt><input>node = html.img(</input>
	<prompt>... </prompt><input>   src=php.php("echo 'eggs.gif'"),</input>
	<prompt>... </prompt><input>   alt=html.abbr(</input>
	<prompt>... </prompt><input>      "EGGS",</input>
	<prompt>... </prompt><input>      title="Extensible Graphics Generation System",</input>
	<prompt>... </prompt><input>      lang="en"</input>
	<prompt>... </prompt><input>   )</input>
	<prompt>... </prompt><input>)</input>
	&gt;&gt;&gt; print node.asBytes()
	&lt;img alt="EGGS" src="&lt;?php echo 'eggs.gif'?&gt;" /&gt;
	</tty>
	</example>
	"""
	__metaclass__ = _Attr_Meta
	required = False
	default = None
	values = None

	def isfancy(self):
		"""
		<par>Return whether <self/> contains nodes other than
		<pyref class="Text"><class>Text</class></pyref>.</par>
		"""
		for child in self:
			if not isinstance(child, Text):
				return True
		return False

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		return cls._strbase(fullname=fullname, xml=xml)

	def present(self, presenter):
		return presenter.presentAttr(self) # return a generator-iterator

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
				warnings.warn(IllegalAttrValueWarning(self))

	def _walk(self, filter, path):
		for option in filter.filter(path):
			if option is entercontent:
				for result in Frag._walk(self, filter, path):
					yield result
			elif option is enterattrs:
				pass
			elif option:
				yield path

	def _publishname(self, publisher):
		if self.xmlns is not None:
			prefix = publisher._ns2prefix.get(self.xmlns) if self.xmlns != xml_xmlns else u"xml"
			if prefix is not None:
				return u"%s:%s" % (prefix, self.xmlname)
		return self.xmlname

	def _publishattrvalue(self, publisher):
		# Internal helper that is used to publish the attribute value
		# (can be overwritten in subclass (done by e.g. StyleAttr and URLAttr)
		return Frag.publish(self, publisher)

	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		publisher.inattr += 1
		yield publisher.encode(self._publishname(publisher)) # publish the XML name, not the Python name
		yield publisher.encode(u"=\"")
		publisher.pushtextfilter(helpers.escapeattr)
		for part in self._publishattrvalue(publisher):
			yield part
		publisher.poptextfilter()
		yield publisher.encode(u"\"")
		publisher.inattr -= 1

	def pretty(self, level=0, indent="\t"):
		return self.clone()

	def __repr__(self):
		l = len(self)
		if l==0:
			info = u"no children"
		elif l==1:
			info = u"1 child"
		else:
			info = u"%d children" % l
		loc = " (from %s)" % self.startloc if self.startloc is not None else ""
		return "<%s.%s attr object (%s)%s at 0x%x>" % (self.__class__.__module__, self.__fullname__, info, loc, id(self))


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
	<par>Attribute class that is used for when the attribute value may be any kind
	of number.</par>
	"""


class IntAttr(NumberAttr):
	"""
	<par>Attribute class that is used when the attribute value may be an
	integer.</par>
	"""


class FloatAttr(NumberAttr):
	"""
	<par>Attribute class that is used when the attribute value may be a
	floating point value.</par>
	"""


class BoolAttr(Attr):
	"""
	<par>Attribute class that is used for boolean attributes. When publishing
	the value will always be the attribute name, regardless of the real value.</par>
	"""

	# We can't simply overwrite _publishattrvalue(), because for xhtml==0 we don't output a "proper" attribute
	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		publisher.inattr += 1
		name = self._publishname(publisher)
		yield publisher.encode(name) # publish the XML name, not the Python name
		if publisher.xhtml>0:
			yield publisher.encode(u"=\"")
			publisher.pushtextfilter(helpers.escapeattr)
			yield publisher.encode(name)
			publisher.poptextfilter()
			yield publisher.encode(u"\"")
		publisher.inattr -= 1


class ColorAttr(Attr):
	"""
	<par>Attribute class that is used for a color attributes.</par>
	"""


class StyleAttr(Attr):
	"""
	<par>Attribute class that is used for &css; style attributes.</par>
	"""

	def parsed(self, parser, start=None):
		if not self.isfancy():
			csshandler = cssparsers.ParseHandler(ignorecharset=True)
			value = csshandler.parseString(unicode(self), base=parser.base)
			return self.__class__(value)
		return self

	def _publishattrvalue(self, publisher):
		if not self.isfancy():
			csshandler = cssparsers.PublishHandler(ignorecharset=True)
			value = csshandler.parseString(unicode(self), base=publisher.base)
			new = Frag(value)
			for part in new.publish(publisher):
				yield part
		else:
			for part in super(StyleAttr, self)._publishattrvalue(publisher):
				yield part

	def urls(self, base=None):
		"""
		<par>Return a list of all the <pyref module="ll.url" class="URL"><class>URL</class></pyref>s
		found in the style attribute.</par>
		"""
		csshandler = cssparsers.CollectHandler(ignorecharset=True)
		csshandler.parseString(unicode(self), base=base)
		urls = csshandler.urls
		return urls


class URLAttr(Attr):
	"""
	<par>Attribute class that is used for &url;s. See the module <pyref module="ll.url"><module>ll.url</module></pyref>
	for more information about &url; handling.</par>
	"""

	def parsed(self, parser, start=None):
		return self.__class__(utils.replaceInitialURL(self, lambda u: parser.base/u))

	def _publishattrvalue(self, publisher):
		new = utils.replaceInitialURL(self, lambda u: u.relative(publisher.base))
		for part in new.publish(publisher):
			yield part

	def asURL(self):
		"""
		<par>Return <self/> as a <pyref module="ll.url" class="URL"><class>URL</class></pyref>
		instance (note that non-character content will be filtered out).</par>
		"""
		return url_.URL(Attr.__unicode__(self))

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
		u = url_.URL(root)/u
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


class _Attrs_Meta(Node.__metaclass__):
	def __new__(cls, name, bases, dict):
		self = super(_Attrs_Meta, cls).__new__(cls, name, bases, dict)
		self._byxmlname = weakref.WeakValueDictionary() # map XML name to attribute class
		self._bypyname = weakref.WeakValueDictionary() # map Python name to attribute class
		self._defaultattrsxml = weakref.WeakValueDictionary() # map XML name to attribute class with default value
		self._defaultattrspy = weakref.WeakValueDictionary() # map Python name to attribute class with default value

		# go through the attributes and register them in the cache
		for key in dir(self):
			value = getattr(self, key)
			if isinstance(value, _Attr_Meta):
				self.add(value)
		return self

	def __repr__(self):
		return "<attrs class %s:%s with %s attrs at 0x%x>" % (self.__module__, self.__fullname__, len(self._bypyname), id(self))

	def __contains__(self, key):
		if isinstance(key, basestring):
			return key in self._bypyname
		if key.xmlns is not None:
			return True
		return self._bypyname.get(key.__name__, None) is key


class Attrs(Node, dict):
	"""
	<par>An attribute map. Allowed entries are specified through nested subclasses
	of <pyref class="Attr"><class>Attr</class></pyref>.</par>
	"""
	__metaclass__ = _Attrs_Meta

	def __init__(self, _content=None, **attrs):
		dict.__init__(self)
		# set default attribute values
		for (key, value) in self._defaultattrspy.iteritems():
			self[key] = value.default.clone()
		# set attributes, this might overwrite (or delete) default attributes
		self.update(_content, **attrs)

	def __eq__(self, other):
		return self.__class__ is other.__class__ and dict.__eq__(self, other)

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		return cls._strbase(fullname=fullname, xml=xml)

	@classmethod
	def add(cls, value):
		cls._byxmlname[value.xmlname] = value
		cls._bypyname[value.__name__] = value
		if value.default:
			cls._defaultattrsxml[value.xmlname] = value
			cls._defaultattrspy[value.__name__] = value
		# fix classname (but don't patch inherited attributes)
		if "." not in value.__fullname__:
			value.__fullname__ = "%s.%s" % (cls.__fullname__, value.__fullname__)

	def _create(self):
		node = self.__class__() # "virtual" constructor
		node.clear()
		return node

	def clone(self):
		node = self._create()
		for value in dict.values(self):
			dict.__setitem__(node, value.__class__, value.clone())
		return self._decoratenode(node)

	def __copy__(self):
		node = self._create()
		for value in dict.values(self):
			dict.__setitem__(node, value.__class__, value)
		return self._decoratenode(node)

	def __deepcopy__(self, memo=None):
		node = self._create()
		if memo is None:
			memo = {}
		memo[id(self)] = node
		for value in dict.values(self):
			dict.__setitem__(node, value.__class__, copy.deepcopy(value, memo))
		return self._decoratenode(node)

	def convert(self, converter):
		node = self._create()
		for value in self.values():
			newvalue = value.convert(converter)
			assert isinstance(newvalue, Node), "the convert method returned the illegal object %r (type %r) when converting the attribute %s with the value %r" % (newvalue, type(newvalue), value.__class__.__name__, value)
			node[value.__class__] = newvalue
		return node

	def compact(self):
		node = self._create()
		for value in self.values():
			newvalue = value.compact()
			assert isinstance(newvalue, Node), "the compact method returned the illegal object %r (type %r) when compacting the attribute %s with the value %r" % (newvalue, type(newvalue), value.__class__.__name__, value)
			node[value.__class__] = newvalue
		return node

	def normalized(self):
		node = self._create()
		for value in self.values():
			newvalue = value.normalized()
			assert isinstance(newvalue, Node), "the normalized method returned the illegal object %r (type %r) when normalizing the attribute %s with the value %r" % (newvalue, type(newvalue), value.__class__.__name__, value)
			node[value.__class__] = newvalue
		return node

	def _walk(self, filter, path):
		path.append(None)
		for child in self.values():
			path[-1] = child
			for result in child._walk(filter, path):
				yield result
		path.pop()

	def present(self, presenter):
		return presenter.presentAttrs(self) # return a generator-iterator

	def checkvalid(self):
		# collect required attributes
		attrs = set()
		for value in self.allowedattrs():
			if value.required:
				attrs.add(value)
		# Check each attribute and remove it from the list of required ones
		for value in self.values():
			value.checkvalid()
			try:
				attrs.remove(value.__class__)
			except KeyError:
				pass
		# are there any required attributes remaining that haven't been specified? => warn about it
		if attrs:
			warnings.warn(RequiredAttrMissingWarning(self, list(attrs)))

	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		for value in self.values():
			yield publisher.encode(u" ")
			for part in value.publish(publisher):
				yield part

	def __unicode__(self):
		return u""

	@classmethod
	def isallowed(cls, name):
		if isinstance(name, basestring):
			return name in cls._bypyname
		if name.xmlns is not None:
			return True
		try:
			candidate = cls._bypyname[name.__name__]
		except KeyError:
			return False
		# make sure that both Python name and XML name match
		return candidate.xmlname == name.xmlname

	@classmethod
	def isallowed_xml(cls, name, xmlns=None):
		if isinstance(name, basestring):
			return name in cls._byxmlname
		if name.xmlns is not None:
			return True
		try:
			candidate = cls._bypyname[name.__name__]
		except KeyError:
			return False
		# make sure that both Python name and XML name match
		return candidate.xmlname == name.xmlname

	def __getattribute__(self, name):
		sup = super(Attrs, self)
		if name in sup.__getattribute__("_bypyname"): # avoid recursion
			return self.__getitem__(name)
		else:
			return sup.__getattribute__(name)

	def __setattr__(self, name, value):
		sup = super(Attrs, self)
		if name in sup.__getattribute__("_bypyname"): # avoid recursion
			return self.__setitem__(name, value)
		else:
			return sup.__setattr__(name, value)

	def __delattr__(self, name):
		sup = super(Attrs, self)
		if name in sup.__getattribute__("_bypyname"): # avoid recursion
			return self.__detitem__(name)
		else:
			return sup.__delattr__(name)

	def __getitem__(self, name):
		if isinstance(name, list):
			node = self
			for subname in name:
				node = node[subname]
			return node
		return self.attr(name)

	def __setitem__(self, name, value):
		if isinstance(name, list):
			if not name:
				raise ValueError("can't replace self")
			node = self
			for subname in name[:-1]:
				node = node[subname]
			node[name[-1]] = value
		return self.set(name, value)

	def __delitem__(self, name):
		if isinstance(name, list):
			if not name:
				raise ValueError("can't delete self")
			node = self
			for subname in name[:-1]:
				node = node[subname]
			del node[name[-1]]
		dict.__delitem__(self, self.allowedattr(name))

	def has(self, name):
		"""
		<par>return whether <self/> has an attribute with a Python name <arg>name</arg>.
		<arg>name</arg> may also be an attribute class (either from <lit><self/>.Attrs</lit>
		are a global attribute).</par>
		"""
		try:
			attr = dict.__getitem__(self, self.allowedattr(name))
		except KeyError:
			return False
		return len(attr)>0

	def has_xml(self, name):
		"""
		<par>return whether <self/> has an attribute with an XML name <arg>name</arg>.
		<arg>name</arg> may also be an attribute class (either from <lit><self/>.Attrs</lit>
		or for a global attribute).</par>
		"""
		try:
			attr = dict.__getitem__(self, self.allowedattr_xml(name))
		except KeyError:
			return False
		return len(attr)>0

	def __contains__(self, name):
		return self.has(name)

	def get(self, name, default=None):
		"""
		<par>works like the dictionary method <method>get</method>,
		it returns the attribute with the Python name <arg>name</arg>,
		or <arg>default</arg> if <self/> has no such attribute.
		<arg>name</arg> may also be an attribute class (either from
		<lit><self/>.Attrs</lit> or for a global attribute).</par>
		"""
		attr = self.attr(name)
		if not attr:
			attr = self.allowedattr(name)(default) # pack the attribute into an attribute object
		return attr

	def get_xml(self, name, default=None):
		"""
		<par>works like the dictionary method <method>get</method>,
		it returns the attribute with the XML name <arg>name</arg>,
		or <arg>default</arg> if <self/> has no such attribute.
		<arg>name</arg> may also be an attribute class (either from
		<lit><self/>.Attrs</lit> or for a global attribute).</par>
		"""
		attr = self.attr_xml(name)
		if not attr:
			attr = self.allowedattr_xml(name)(default) # pack the attribute into an attribute object
		return attr

	def set(self, name, value):
		"""
		<par>Set the attribute with the Python <arg>name</arg> to the value <arg>value</arg>.
		<arg>name</arg> may be a string or an attribute class.</par>
		<par>The newly set attribute will be returned.</par>
		"""
		attr = self.allowedattr(name)
		value = attr(value)
		dict.__setitem__(self, attr, value) # put the attribute in our dict
		return value

	def set_xml(self, name, value):
		"""
		<par>Set the attribute with the XML <arg>name</arg> to the value <arg>value</arg>.
		<par>The newly set attribute will be returned.</par>
		"""
		attr = self.allowedattr_xml(name)
		value = attr(value)
		dict.__setitem__(self, attr, value) # put the attribute in our dict
		return value

	def setdefault(self, name, default):
		"""
		<par>works like the dictionary method <method>setdefault</method>,
		it returns the attribute with the Python name <arg>name</arg>.
		If <self/> has no such attribute, it will be set to <arg>default</arg>
		and <arg>default</arg> will be returned as the new attribute value.</par>
		"""
		value = self.attr(name)
		if not value:
			attr = self.allowedattr(name)
			value = attr(default) # pack the attribute into an attribute object
			dict.__setitem__(self, attr, value)
		return value

	def setdefault_xml(self, name, default):
		"""
		<par>works like the dictionary method <method>setdefault</method>,
		it returns the attribute with the XML name <arg>name</arg>.
		If <self/> has no such attribute, it will be set to <arg>default</arg>
		and <arg>default</arg> will be returned as the new attribute value.</par>
		"""
		value = self.attr_xml(name)
		if not value:
			attr = self.allowedattr(name)
			value = attr(default) # pack the attribute into an attribute object
			dict.__setitem__(self, attr, value)
		return value

	def update(self, *args, **kwargs):
		"""
		Copies attributes over from all mappings in <arg>args</arg> and from <arg>kwargs</arg>.
		"""
		for mapping in args + (kwargs,):
			if mapping is not None:
				if isinstance(mapping, Attrs):
					# This makes sure that global attributes are copied properly
					for value in mapping._iterallvalues():
						self[value.__class__] = value
				else:
					for (attrname, attrvalue) in mapping.iteritems():
						self[attrname] = attrvalue

	@classmethod
	def allowedattrs(cls):
		"""
		<par>Return an iterator over all allowed attribute classes.
		"""
		return cls._bypyname.itervalues()

	@classmethod
	def allowedattr(cls, name):
		if isinstance(name, basestring):
			try:
				return cls._bypyname[name]
			except KeyError:
				raise IllegalAttrError(name, cls, False)
		# name is an attribute class
		if name.xmlns is not None: # if the attribute class is for a global attribute we accept it
			return name
		try:
			candidate = cls._bypyname[name.__name__]
		except KeyError:
			raise IllegalAttrError(name, cls, False)
		else:
			# make sure that both Python name and XML name match
			if candidate.xmlname == name.xmlname:
				return candidate
			raise IllegalAttrError(name, cls, False)

	@classmethod
	def allowedattr_xml(cls, name):
		if isinstance(name, basestring):
			try:
				return cls._byxmlname[name]
			except KeyError:
				raise IllegalAttrError(name, cls, True)
		# name is an attribute class
		if name.xmlns is not None: # if the attribute class is for a global attribute we accept it
			return name
		try:
			candidate = cls._bypyname[name.__name__]
		except KeyError:
			raise IllegalAttrError(name, cls, False)
		else:
			# make sure that both Python name and XML name match
			if candidate.xmlname == name.xmlname:
				return candidate
			raise IllegalAttrError(name, cls, True)

	def __len__(self):
		return misc.count(self.values())

	def keys(self):
		for value in dict.itervalues(self):
			if value:
				yield value.__class__

	iterkeys = __iter__ = keys

	def values(self):
		for value in dict.itervalues(self):
			if value:
				yield value

	itervalues = values

	def items(self):
		for value in dict.itervalues(self):
			if value:
				yield (value.__class__, value)

	iteritems = items

	def _iterallvalues(self):
		"""
		Iterate all values, even the unset ones
		"""
		return dict.itervalues(self)

	def attr(self, name):
		attr = self.allowedattr(name)
		try:
			value = dict.__getitem__(self, attr)
		except KeyError: # if the attribute is not there generate a new empty one
			value = attr()
			dict.__setitem__(self, attr, value)
		return value

	def attr_xml(self, name):
		attr = self.allowedattr_xml(name)
		try:
			value = dict.__getitem__(self, attr)
		except KeyError: # if the attribute is not there generate a new empty one
			value = attr()
			dict.__setitem__(self, attr, value)
		return value

	def filtered(self, function):
		"""
		returns a filtered version of the <self/>.
		"""
		node = self._create()
		for (name, value) in self.items():
			if function(value):
				node[name] = value
		return node

	def _fixnames(self, names):
		newnames = []
		for name in names:
			if isinstance(name, basestring):
				try:
					name = self.allowedattr(name)
				except IllegalAttrError:
					continue
			newnames.append(name)
		return tuple(newnames)

	def _fixnames_xml(self, names):
		newnames = []
		for name in names:
			if isinstance(name, basestring):
				try:
					name = self.allowedattr_xml(name)
				except IllegalAttrError:
					continue
			newnames.append(name)
		return tuple(newnames)

	def withnames(self, *names):
		"""
		<par>Return a copy of <self/> where only the attributes with Python names
		in <arg>names</arg> are kept, all others are removed.</par>
		"""
		def isok(node):
			return isinstance(node, names)

		names = self._fixnames(names)
		return self.filtered(isok)

	def withnames_xml(self, *names):
		"""
		<par>Return a copy of <self/> where only the attributes with XML names
		in <arg>names</arg> are kept, all others are removed.</par>
		"""
		def isok(node):
			return isinstance(node, names)

		names = self._fixnames_xml(names)
		return self.filtered(isok)

	def withoutnames(self, *names):
		"""
		<par>Return a copy of <self/> where all the attributes with Python names
		in <arg>names</arg> are removed.</par>
		"""
		def isok(node):
			return not isinstance(node, names)

		names = self._fixnames(names)
		return self.filtered(isok)

	def withoutnames_xml(self, *names):
		"""
		<par>Return a copy of <self/> where all the attributes with XML names
		in <arg>names</arg> are removed.</par>
		"""
		def isok(node):
			return not isinstance(node, names)

		names = self._fixnames_xml(names)
		return self.filtered(isok)

	def __repr__(self):
		l = len(self)
		if l==0:
			info = "(no attrs)"
		elif l==1:
			info = "(1 attr)"
		else:
			info = "(%d attrs)" % l
		if self.startloc is not None:
			loc = " (from %s)" % self.startloc
		else:
			loc = ""
		return "<%s.%s attrs %s%s at 0x%x>" % (self.__class__.__module__, self.__fullname__, info, loc, id(self))


def _patchclassnames(dict, name):
	# If an Attrs class has been provided patch up its class names
	try:
		attrs = dict["Attrs"]
	except KeyError:
		pass
	else:
		attrs.__fullname__ = "%s.Attrs" % name
		for (key, value) in attrs.__dict__.iteritems():
			if isinstance(value, _Attr_Meta):
				value.__fullname__ = "%s.%s" % (name, value.__fullname__)

	# If a Context has been provided patch up its class names
	try:
		context = dict["Context"]
	except KeyError:
		pass
	else:
		context.__fullname__ = "%s.%s" % (name, context.__fullname__)


class _Element_Meta(Node.__metaclass__):
	def __new__(cls, name, bases, dict):
		if "model" in dict and isinstance(dict["model"], bool):
			from ll.xist import sims
			if dict["model"]:
				dict["model"] = sims.Any()
			else:
				dict["model"] = sims.Empty()
		_patchclassnames(dict, name)
		self = super(_Element_Meta, cls).__new__(cls, name, bases, dict)
		if dict.get("register") is not None:
			getpoolstack()[-1].register(self)
		return self

	def __repr__(self):
		return "<element class %s:%s at 0x%x>" % (self.__module__, self.__fullname__, id(self))


class Element(Node):
	"""
	<par>This class represents &xml;/&xist; elements. All elements implemented
	by the user must be derived from this class.</par>

	<par>Elements support the following class variables:</par>
	<dlist>
	<term><lit>model</lit></term><item>This is an object that is used for
	validating the content of the element. See the module
	<pyref module="ll.xist.sims"><module>ll.xist.sims</module></pyref>
	for more info. If <lit>model</lit> is <lit>None</lit> validation will
	be skipped, otherwise it will be performed when parsing or publishing.</item>

	<term><lit>Attrs</lit></term><item>This is a class derived from
	<pyref class="Element.Attrs"><class>Element.Attrs</class></pyref>
	and should define all attributes as classes nested inside this
	<class>Attrs</class> class.</item>

	<term><lit>xmlns</lit></term><item>This is the name of the namespace this
	element belong to.</item>

	<term><lit>register</lit></term><item>If <lit>register</lit> is false the
	element won't be registered with the parser.</item>

	<term><lit>xmlname</lit></term><item>If the class name has to be different
	from the &xml; name (e.g. because the &xml; name is not a valid Python identifier)
	<lit>xmlname</lit> can be used to specify the real &xml; name.</item>
	</dlist>
	"""
	__metaclass__ = _Element_Meta

	model = None
	register = None

	Attrs = Attrs

	def __enter__(self):
		stack = getstack()
		if stack:
			stack[-1].append(self)
		stack.append(self)
		return self

	def __exit__(self, type, value, traceback):
		getstack().pop()

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
				self.attrs.update(child)
			else:
				newcontent.append(child)
		self.content = Frag(*newcontent)
		self.attrs.update(attrs)

	def __getstate__(self):
		attrs = {}
		for (key, value) in self.attrs.iteritems():
			if key.xmlns is None:
				key = key.__name__
			else:
				key = (key.__module__, key.__fullname__)
			attrs[key] = Frag(value)
		return (self.content, attrs)

	def __setstate__(self, (content, attrs)):
		self.content = content
		self.attrs = self.Attrs()
		for (key, value) in attrs.iteritems():
			if not isinstance(key, basestring):
				obj = __import__(key[0])
				for name in key[0].split(".")[1:]:
					obj = getattr(obj, name)
				for name in key[1].split("."):
					obj = getattr(obj, name)
				key = obj
			self.attrs[key] = value

	def __call__(self, *content, **attrs):
		for child in content:
			if isinstance(child, dict):
				self.attrs.update(child)
			else:
				self.content.append(child)
		for (attrname, attrvalue) in attrs.iteritems():
			self.attrs[attrname] = attrvalue
		return self

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.content==other.content and self.attrs==other.attrs

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = cls._strbase(fullname=fullname, xml=xml)
		if decorate:
			if cls.model is not None and cls.model.empty:
				s = "<%s/>" % s
			else:
				s = "<%s>" % s
		return s

	def checkvalid(self):
		if self.model is not None:
			self.model.checkvalid(self)
		self.attrs.checkvalid()

	def append(self, *items):
		"""
		<par>Append every item in <arg>items</arg> to the element content.</par>
		"""
		self.content.append(*items)

	def extend(self, items):
		"""
		<par>Append all items in <arg>items</arg> to element content.</par>
		"""
		self.content.extend(items)

	def insert(self, index, *items):
		"""
		<par>Insert every item in <arg>items</arg> at the position <arg>index</arg>.</par>
		"""
		self.content.insert(index, *items)

	def convert(self, converter):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.convert(converter)
		node.attrs = self.attrs.convert(converter)
		return self._decoratenode(node)

	def clone(self):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.clone() # this is faster than passing it in the constructor (no tonode call)
		node.attrs = self.attrs.clone()
		return self._decoratenode(node)

	def __copy__(self):
		node = self.__class__()
		node.content = copy.copy(self.content)
		node.attrs = copy.copy(self.attrs)
		return self._decoratenode(node)

	def __deepcopy__(self, memo=None):
		node = self.__class__()
		if memo is None:
			memo = {}
		memo[id(self)] = node
		node.content = copy.deepcopy(self.content, memo)
		node.attrs = copy.deepcopy(self.attrs, memo)
		return self._decoratenode(node)

	def __unicode__(self):
		return unicode(self.content)

	def _addimagesizeattributes(self, url, widthattr=None, heightattr=None):
		"""
		<par>Automatically set image width and height attributes.</par>

		<par>The size of the image with the &url; <arg>url</arg> will be determined and
		the width of the image will be put into the attribute with the name <arg>widthattr</arg>
		if <arg>widthattr</arg> is not <lit>None</lit> and the attribute is not set. The
		same will happen for the height, which will be put into the <arg>heighattr</arg>.</par>
		"""

		try:
			size = url.imagesize()
		except IOError, exc:
			warnings.warn(FileNotFoundWarning("can't read image", url, exc))
		else:
			for attr in (heightattr, widthattr):
				if attr is not None: # do something to the width/height
					if not self.attrs.has(attr):
						self[attr] = size[attr==heightattr]

	def present(self, presenter):
		return presenter.presentElement(self) # return a generator-iterator

	def _publishname(self, publisher):
		if self.xmlns is not None:
			prefix = publisher._ns2prefix.get(self.xmlns)
			if prefix is not None:
				return u"%s:%s" % (prefix, self.xmlname)
		return self.xmlname

	def _publishfull(self, publisher):
		"""
		Does the full publication of the element. If you need full elements
		inside attributes (e.g. for &jsp; tag libraries), you can overwrite
		<method>publish</method> and simply call this method.
		"""
		name = self._publishname(publisher)
		yield publisher.encode(u"<")
		yield publisher.encode(name)
		# we're the first element to be published, so we have to create the xmlns attributes
		if publisher._publishxmlns:
			for (xmlns, prefix) in publisher._ns2prefix.iteritems():
				if xmlns not in publisher.hidexmlns:
					yield publisher.encode(u" xmlns")
					if prefix is not None:
						yield publisher.encode(u":")
						yield publisher.encode(prefix)
					yield publisher.encode(u'="')
					yield publisher.encode(xmlns)
					yield publisher.encode('"')
			# reset the note, so the next element won't create the attributes again
			publisher._publishxmlns = False
		for part in self.attrs.publish(publisher):
			yield part
		if len(self):
			yield publisher.encode(u">")
			for part in self.content.publish(publisher):
				yield part
			yield publisher.encode(u"</")
			yield publisher.encode(name)
			yield publisher.encode(u">")
		else:
			if publisher.xhtml in (0, 1):
				if self.model is not None and self.model.empty:
					if publisher.xhtml==1:
						yield publisher.encode(u" /")
					yield publisher.encode(u">")
				else:
					yield publisher.encode(u"></")
					yield publisher.encode(name)
					yield publisher.encode(u">")
			elif publisher.xhtml == 2:
				yield publisher.encode(u"/>")

	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		if publisher.inattr:
			# publish the content only when we are inside an attribute. This works much like using the plain string value,
			# but even works with processing instructions, or what the abbreviation entities return
			return self.content.publish(publisher) # return a generator-iterator
		else:
			return self._publishfull(publisher) # return a generator-iterator

	def __getitem__(self, index):
		"""
		<par>If <arg>index</arg> is a string, return the attribute with this (Python) name.</par>
		<par>If <arg>index</arg> is a tuple consisting of a namespace and a string,
		return the global attribute with this (Python) name.</par>
		<par>If <arg>index</arg> is a number return the appropriate content node.</par>
		<par><arg>index</arg> may also be a list, in with case <method>__getitem__</method>
		will be applied recusively.</par>
		"""
		if isinstance(index, list):
			node = self
			for subindex in index:
				node = node[subindex]
			return node
		elif isinstance(index, _Attr_Meta):
			return self.attrs[index]
		elif isinstance(index, _Node_Meta):
			return self.content[index]
		elif isinstance(index, (int, long)):
			return self.content[index]
		elif isinstance(index, slice):
			return self.__class__(self.content[index], self.attrs)
		else:
			return self.attrs[index]

	def __setitem__(self, index, value):
		"""
		<par>Set an attribute or content node to the value <arg>value</arg>.</par>
		<par>For possible types for <arg>index</arg> see <pyref method="__getitem__"><method>__getitem__</method></pyref>.</par>
		"""
		if isinstance(index, list):
			if not index:
				raise ValueError("can't replace self")
			node = self
			for subindex in index[:-1]:
				node = node[subindex]
			node[index[-1]] = value
		elif isinstance(index, (int, long, slice)):
			self.content[index] = value
		else:
			self.attrs[index] = value

	def __delitem__(self, index):
		"""
		<par>Remove an attribute or content node.</par>
		<par>For possible types for <arg>index</arg> see <pyref method="__getitem__"><method>__getitem__</method></pyref>.</par>
		"""
		if isinstance(index, list):
			if not index:
				raise ValueError("can't delete self")
			node = self
			for subindex in index[:-1]:
				node = node[subindex]
			del node[index[-1]]
		elif isinstance(index, (int, long, slice)):
			del self.content[index]
		else:
			del self.attrs[index]

	def __getslice__(self, index1, index2):
		"""
		Returns a copy of the element that contains a slice of the content.
		"""
		return self.__class__(self.content[index1:index2], self.attrs)

	def __setslice__(self, index1, index2, sequence):
		"""
		Replaces a slice of the content of the element.
		"""
		self.content[index1:index2] = sequence

	def __delslice__(self, index1, index2):
		"""
		Removes a slice of the content of the element.
		"""
		del self.content[index1:index2]

	def __iadd__(self, other):
		self.extend(other)
		return self

	def __len__(self):
		"""
		return the number of children.
		"""
		return len(self.content)

	def __iter__(self):
		return iter(self.content)

	def compact(self):
		node = self.__class__()
		node.content = self.content.compact()
		node.attrs = self.attrs.compact()
		return self._decoratenode(node)

	def _walk(self, filter, path):
		for option in filter.filter(path):
			if option is entercontent:
				for result in self.content._walk(filter, path):
					yield result
			elif option is enterattrs:
				for result in self.attrs._walk(filter, path):
					yield result
			elif option:
				yield path

	def withsep(self, separator, clone=False):
		"""
		<par>returns a version of <self/> with a separator node between the child
		nodes of <self/>. For more info see
		<pyref class="Frag" method="withsep"><method>Frag.withsep</method></pyref>.</par>
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.withsep(separator, clone)
		return node

	def sorted(self, cmp=None, key=None, reverse=False):
		"""
		returns a sorted version of <self/>. <arg>compare</arg> is a comparison
		function. If <arg>compare</arg> is omitted, the character content will
		be compared.
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.sorted(cmp, key, reverse)
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

	def mapped(self, function, converter=None, **converterargs):
		if converter is None:
			converter = converters.Converter(**converterargs)
		node = function(self, converter)
		assert isinstance(node, Node), "the mapped method returned the illegal object %r (type %r) when mapping %r" % (node, type(node), self)
		if node is self:
			node = self.__class__(self.content.mapped(function, converter))
			node.attrs = self.attrs.clone()
		return node

	def normalized(self):
		node = self.__class__()
		node.attrs = self.attrs.normalized()
		node.content = self.content.normalized()
		return node

	def pretty(self, level=0, indent="\t"):
		node = self.__class__(self.attrs)
		if len(self):
			# search for text content
			for child in self:
				if isinstance(child, Text):
					# leave content alone
					node.append(self.content.clone())
					break
			else:
				for child in self:
					node.append("\n", child.pretty(level+1, indent))
				node.append("\n", indent*level)
		if level>0:
			node = Frag(indent*level, node)
		return node

	def __repr__(self):
		lc = len(self.content)
		if lc==0:
			infoc = "no children"
		elif lc==1:
			infoc = "1 child"
		else:
			infoc = "%d children" % lc
		la = len(self.attrs)
		if la==0:
			infoa = "no attrs"
		elif la==1:
			infoa = "1 attr"
		else:
			infoa = "%d attrs" % la
		if self.startloc is not None:
			loc = " (from %s)" % self.startloc
		else:
			loc = ""
		return "<%s.%s element object (%s/%s)%s at 0x%x>" % (self.__class__.__module__, self.__fullname__, infoc, infoa, loc, id(self))


class _Entity_Meta(Node.__metaclass__):
	def __new__(cls, name, bases, dict):
		self = super(_Entity_Meta, cls).__new__(cls, name, bases, dict)
		if dict.get("register") is not None:
			getpoolstack()[-1].register(self)
		return self

	def __repr__(self):
		return "<entity class %s:%s at 0x%x>" % (self.__module__, self.__fullname__, id(self))


class Entity(Node):
	"""
	<par>Class for entities. Derive your own entities from it and overwrite
	<pyref class="Node" method="convert"><method>convert</method></pyref>.</par>
	"""
	__metaclass__ = _Entity_Meta

	register = None

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = cls._strbase(fullname=fullname, xml=xml)
		if decorate:
			s = "&%s;" % s
		return s

	def __eq__(self, other):
		return self.__class__ is other.__class__

	def compact(self):
		return self

	def present(self, presenter):
		return presenter.presentEntity(self) # return a generator-iterator

	def publish(self, publisher):
		yield publisher.encode(u"&")
		yield publisher.encode(self.xmlname)
		yield publisher.encode(u";")

	def __repr__(self):
		if self.startloc is not None:
			loc = " (from %s)" % self.startloc
		else:
			loc = ""
		return "<%s.%s entity object%s at 0x%x>" % (self.__class__.__module__, self.__fullname__, loc, id(self))


class _CharRef_Meta(Entity.__metaclass__): # don't subclass Text.__metaclass__, as this is redundant
	def __repr__(self):
		return "<charref class %s:%s at 0x%x>" % (self.__module__, self.__fullname__, id(self))


class CharRef(Text, Entity):
	"""
	<par>A simple character reference, the codepoint is in the class attribute
	<lit>codepoint</lit>.</par>
	"""
	__metaclass__ = _CharRef_Meta
	register = None

	def __init__(self):
		Text.__init__(self, unichr(self.codepoint))
		Entity.__init__(self)

	def __getnewargs__(self):
		return ()

	def present(self, presenter):
		return presenter.presentEntity(self) # return a generator-iterator

	# The rest is the same as for Text, but does not return CharRefs, but Texts
	def __getitem__(self, index):
		return Text(self.content.__getitem__(index))

	def __add__(self, other):
		return Text(self.content + other)

	def __radd__(self, other):
		return Text(unicode(other) + self.content)

	def __mul__(self, n):
		return Text(n * self.content)

	def __rmul__(self, n):
		return Text(n * self.content)

	def __getslice__(self, index1, index2):
		return Text(self.content.__getslice__(index1, index2))

	def capitalize(self):
		return Text(self.content.capitalize())

	def center(self, width):
		return Text(self.content.center(width))

	def ljust(self, width, fill=u" "):
		return Text(self.content.ljust(width, fill))

	def lower(self):
		return Text(self.content.lower())

	def lstrip(self, chars=None):
		return Text(self.content.lstrip(chars))

	def replace(self, old, new, maxsplit=-1):
		return Text(self.content.replace(old, new, maxsplit))

	def rjust(self, width, fill=u" "):
		return Text(self.content.rjust(width, fill))

	def rstrip(self, chars=None):
		return Text(self.content.rstrip(chars))

	def strip(self, chars=None):
		return Text(self.content.strip(chars))

	def swapcase(self):
		return Text(self.content.swapcase())

	def title(self):
		return Text(self.content.title())

	def translate(self, table):
		return Text(self.content.translate(table))

	def upper(self):
		return Text(self.content.upper())


import publishers, cssparsers, converters, utils, helpers


###
### XML class pool
###

class Pool(object):
	"""
	<par>Class pool for <pyref class="Element">element</pyref>,
	<pyref class="ProcInst">procinst</pyref>, <pyref class="Entity">entity</pyref>,
	<pyref class="CharRef">charref</pyref> and <pyref class="Attr">attribute</pyref> classes.</par>

	<par>This is used by the parser to map names to classes.</par>
	"""
	def __init__(self, *objects):
		"""
		<par>Create a new pool. All objects in <arg>objects</arg> will be passed
		to the <method>register</method> method.</par>
		"""
		self._elementsbyxmlname = weakref.WeakValueDictionary()
		self._elementsbypyname = weakref.WeakValueDictionary()
		self._procinstsbyxmlname = weakref.WeakValueDictionary()
		self._procinstsbypyname = weakref.WeakValueDictionary()
		self._entitiesbyxmlname = weakref.WeakValueDictionary()
		self._entitiesbypyname = weakref.WeakValueDictionary()
		self._charrefsbyxmlname = weakref.WeakValueDictionary()
		self._charrefsbypyname = weakref.WeakValueDictionary()
		self._charrefsbycodepoint = weakref.WeakValueDictionary()
		self._attrsbyxmlname = weakref.WeakValueDictionary()
		self._attrsbypyname = weakref.WeakValueDictionary()
		self.bases = []
		for object in objects:
			self.register(object)

	def register(self, object):
		"""
		<par>Register <arg>object</arg> in the pool. <arg>object</arg> can be:</par>
		<ulist>
		<item>A <pyref class="Element"><class>Element</class></pyref>,
		<pyref class="ProcInst"><class>ProcInst</class></pyref>,
		<pyref class="Entity"><class>Entity</class></pyref>,
		<pyref class="CharRef"><class>CharRef</class></pyref> class;</item>
		<item>An <pyref class="Attr"><class>Attr</class></pyref> class
		for a global attribute;</item>
		<item>An <pyref class="Attrs"><class>Attrs</class></pyref> class
		containing global attributes;</item>
		<item>A <class>dict</class> (all <class>Node</class> classes in the
		values will be registered, this makes it possible to e.g. register all
		local variables by passing <lit>vars()</lit>);</item>
		<item>A module (all <class>Node</class> classes in the
		module will be registered);</item>
		<item>A <class>Pool</class> object (this pool object will be added to the
		base pools. If a class isn't found in <self/> the search continues in these
		base pool;</item>
		<item><lit>True</lit>, which add the current default pool to the base pools.</item>
		</ulist>
		"""
		if isinstance(object, type):
			if issubclass(object, Element):
				if object.register:
					self._elementsbyxmlname[(object.xmlname, object.xmlns)] = object
					self._elementsbypyname[(object.__name__, object.xmlns)] = object
			elif issubclass(object, ProcInst):
				if object.register:
					self._procinstsbyxmlname[object.xmlname] = object
					self._procinstsbypyname[object.__name__] = object
			elif issubclass(object, Entity):
				if object.register:
					self._entitiesbyxmlname[object.xmlname] = object
					self._entitiesbypyname[object.__name__] = object
					if issubclass(object, CharRef):
						self._charrefsbyxmlname[object.xmlname] = object
						self._charrefsbypyname[object.__name__] = object
						self._charrefsbycodepoint[object.codepoint] = object
			elif issubclass(object, Attr):
				if object.register:
					self._attrsbyxmlname[(object.xmlname, object.xmlns)] = object
					self._attrsbypyname[(object.__name__, object.xmlns)] = object
			elif issubclass(object, Attrs):
				for attr in object.allowedattrs():
					self.register(attr)
		elif isinstance(object, types.ModuleType):
			for value in object.__dict__.itervalues():
				if isinstance(value, type): # This avoids recursive module registration
					self.register(value)
		elif isinstance(object, dict):
			for value in object.itervalues():
				if isinstance(value, type): # This avoids recursive module registration
					self.register(value)
		elif object is True:
			self.bases.append(getpoolstack()[-1])
		elif isinstance(object, Pool):
			self.bases.append(object)

	def __enter__(self):
		getpoolstack().append(self)
		return self

	def __exit__(self, type, value, traceback):
		getpoolstack().pop()

	def elements(self):
		"""
		Return an iterator for all registered element classes.
		"""
		return self._elementsbypyname.itervalues()

	def elementclass(self, name, xmlns):
		"""
		Return the element class for the element with the Python name
		<arg>name</arg> and the namespace <arg>xmlns</arg>. If the class can't
		be found the search continues in the base pools. If the element can't be
		found a <class>IllegalElementError</class> will be raised.
		"""
		if isinstance(xmlns, (list, tuple)):
			for xmlns in xmlns:
				xmlns = nsname(xmlns)
				try:
					return self._elementsbypyname[(name, xmlns)]
				except KeyError:
					pass
		else:
			xmlns = nsname(xmlns)
			try:
				return self._elementsbypyname[(name, xmlns)]
			except KeyError:
				pass
		for base in self.bases:
			try:
				return base.elementclass(name, xmlns)
			except IllegalElementError:
				pass
		raise IllegalElementError(name, xmlns, False)

	def elementclass_xml(self, name, xmlns):
		"""
		Return the element class for the element type with the &xml; name
		<arg>name</arg> and the namespace <arg>xmlns</arg>. If the class can't
		be found the search continues in the base pools. If the element can't be
		found a <class>IllegalElementError</class> will be raised.
		"""
		if isinstance(xmlns, (list, tuple)):
			for xmlns in xmlns:
				xmlns = nsname(xmlns)
				try:
					return self._elementsbyxmlname[(name, xmlns)]
				except KeyError:
					pass
		else:
			xmlns = nsname(xmlns)
			try:
				return self._elementsbyxmlname[(name, xmlns)]
			except KeyError:
				pass
		for base in self.bases:
			try:
				return base.elementclass_xml(name, xmlns)
			except IllegalElementError:
				pass
		raise IllegalElementError(name, xmlns, True)

	def element(self, name, xmlns):
		"""
		Return an element object for the element type with the Python name
		<arg>name</arg> and the namespace <arg>xmlns</arg>. If the class can't
		be found the search continues in the base pools.
		"""
		return self.elementclass(name, xmlns)()

	def element_xml(self, name, xmlns):
		"""
		Return an element object for the element type with the &xml; name
		<arg>name</arg> and the namespace <arg>xmlns</arg>. If the class can't
		be found the search continues in the base pools.
		"""
		return self.elementclass_xml(name, xmlns)()

	def haselement(self, name, xmlns):
		"""
		Is there a registered element class in <self/> for the element type
		with the Python name <arg>name</arg> and the namespace <arg>xmlns</arg>?
		"""
		return (name, nsname(xmlns)) in self._elementsbypyname

	def haselement_xml(self, name, xmlns):
		"""
		Is there a registered element class in <self/> for the element type
		with the &xml; name <arg>name</arg> and the namespace <arg>xmlns</arg>?
		"""
		return (name, nsname(xmlns)) in self._elementsbyxmlname

	def procinsts(self):
		"""
		Return an iterator for all registered processing instruction classes.
		"""
		return self._procinstsbypyname.itervalues()

	def procinstclass(self, name):
		"""
		Return the processing instruction class for the PI with the Python name
		<arg>name</arg>. If the class can't be found the search continues in the
		base pools. If the element can't be found a <class>IllegalProcInstError</class>
		will be raised.
		"""
		try:
			return self._procinstsbypyname[name]
		except KeyError:
			for base in self.bases:
				try:
					return self.base.procinstclass(name)
				except IllegalProcInstError:
					pass
			raise IllegalProcInstError(name, False)

	def procinstclass_xml(self, name):
		"""
		Return the processing instruction class for the PI with the &xml; name
		<arg>name</arg>. If the class can't be found the search continues in the
		base pools. If the element can't be found a <class>IllegalProcInstError</class>
		will be raised.
		"""
		try:
			return self._procinstsbyxmlname[name]
		except KeyError:
			for base in self.bases:
				try:
					return self.base.procinstclass_xml(name)
				except IllegalProcInstError:
					pass
			raise IllegalProcInstError(name, True)

	def procinst(self, name, content):
		"""
		Return a processing instruction object for the PI type with the Python
		target name <arg>name</arg>. If the class can't be found the search
		continues in the base pools.
		"""
		return self.procinstclass(name)(content)

	def procinst_xml(self, name, content):
		"""
		Return a processing instruction object for the PI type with the &xml;
		target name <arg>name</arg>. If the class can't be found the search
		continues in the base pools.
		"""
		return self.procinstclass_xml(name)(content)

	def hasprocinst(self, name):
		"""
		Is there a registered processing instruction class in <self/> for the
		PI with the Python name <arg>name</arg>?
		"""
		return name in self._procinstsbypyname

	def hasprocinst_xml(self, name):
		"""
		Is there a registered processing instruction class in <self/> for the
		PI with the &xml; name <arg>name</arg>?
		"""
		return name in self._procinstsbyxmlname

	def entities(self):
		"""
		Return an iterator for all registered entity classes.
		"""
		return self._entitiesbypyname.itervalues()

	def entityclass(self, name):
		"""
		Return the entity for the entity with the Python name <arg>name</arg>.
		If the class can't be found the search continues in the base pools. If the
		element can't be found a <class>IllegalEntityError</class> will be raised.
		"""
		try:
			return self._entitiesbypyname[name]
		except KeyError:
			for base in self.bases:
				try:
					return self.base.entityclass(name)
				except IllegalEntityError:
					pass
			raise IllegalEntityError(name, False)

	def entityclass_xml(self, name):
		"""
		Return the entity for the entity with the &xml; name <arg>name</arg>.
		If the class can't be found the search continues in the base pools. If the
		element can't be found a <class>IllegalEntityError</class> will be raised.
		"""
		try:
			return self._entitiesbyxmlname[name]
		except KeyError:
			for base in self.bases:
				try:
					return self.base.entityclass_xml(name)
				except IllegalEntityError:
					pass
			raise IllegalEntityError(name, True)

	def entity(self, name):
		"""
		Return an entity object for the entity with the Python name
		<arg>name</arg>. If the class can't be found the search continues in
		the base pools.
		"""
		return self.entityclass(name)()

	def entity_xml(self, name):
		"""
		Return an entity object for the entity with the &xml; name
		<arg>name</arg>. If the class can't be found the search continues in
		the base pools.
		"""
		return self.entityclass_xml(name)()

	def hasentity(self, name):
		"""
		Is there a registered entity class in <self/> for the entity with the
		Python name <arg>name</arg>?
		"""
		return name in self._entitiesbypyname

	def hasentity_xml(self, name):
		"""
		Is there a registered entity class in <self/> for the entity with the
		&xml; name <arg>name</arg>?
		"""
		return name in self._entitiesbyxmlname

	def charrefs(self):
		"""
		Return an iterator for all character entity classes.
		"""
		return self._charrefsbypyname.itervalues()

	def charrefclass(self, name):
		"""
		Return the character entity with the Python name <arg>name</arg>.
		<arg>name</arg> can also be an <class>int</class> specifying the codepoint.
		If the class can't be found the search continues in the base pools. If the
		element can't be found a <class>IllegalEntityError</class> will be raised.
		"""
		try:
			if isinstance(name, (int, long)):
				return self._charrefsbycodepoint[name]
			return self._charrefsbypyname[name]
		except KeyError:
			for base in self.bases:
				try:
					return self.base.charrefclass(name)
				except IllegalEntityError:
					pass
			raise IllegalEntityError(name, False)

	def charrefclass_xml(self, name):
		"""
		Return the character entity with the &xml; name <arg>name</arg>.
		<arg>name</arg> can also be an <class>int</class> specifying the codepoint.
		If the class can't be found the search continues in the base pools. If the
		element can't be found a <class>IllegalEntityError</class> will be raised.
		"""
		try:
			if isinstance(name, (int, long)):
				return self._charrefsbycodepoint[name]
			return self._charrefsbyxmlname[name]
		except KeyError:
			for base in self.bases:
				try:
					return self.base.charrefclass_xml(name)
				except IllegalEntityError:
					pass
			raise IllegalEntityError(name, True)

	def charref(self, name):
		"""
		Return a character entity object for the chacter with the Python name
		or codepoint <arg>name</arg>. If the class can't be found the search
		continues in the base pools.
		"""
		return self.charrefclass(name)()

	def charref_xml(self, name):
		"""
		Return a character entity object for the chacter with the &xml; name
		or codepoint <arg>name</arg>. If the class can't be found the search
		continues in the base pools.
		"""
		return self.charrefclass_xml(name)()

	def hascharref(self, name):
		"""
		Is there a registered character entity class in <self/> with the Python
		name or codepoint <arg>name</arg>?
		"""
		if isinstance(name, (int, long)):
			return name in self._charrefsbycodepoint
		else:
			return name in self._charrefsbypyname

	def hascharref_xml(self, name):
		"""
		Is there a registered character entity class in <self/> with the &xml;
		name or codepoint <arg>name</arg>?
		"""
		if isinstance(name, (int, long)):
			return name in self._charrefsbycodepoint
		else:
			return name in self._charrefsbypyname

	def attrclass(self, name, xmlns):
		"""
		Return the aatribute class for the global attribute with the Python name
		<arg>name</arg> and the namespace <arg>xmlns</arg>. If the class can't be
		found the search continues in the base pools. If the attribute can't be
		found a <class>IllegalAttrError</class> will be raised.
		"""
		if not isinstance(xmlns, (list, tuple)):
			xmlns = (xmlns,)
		for xmlns in xmlns:
			xmlns = nsname(xmlns)
			try:
				return self._attrsbypyname[(name, xmlns)]
			except KeyError:
				pass
		for base in self.bases:
			try:
				return base.attrclass(name, xmlns)
			except IllegalAttrError:
				pass
		raise IllegalAttrError(name, xmlns, False)

	def attrclass_xml(self, name, xmlns):
		"""
		Return the aatribute class for the global attribute with the &xml; name
		<arg>name</arg> and the namespace <arg>xmlns</arg>. If the class can't be
		found the search continues in the base pools. If the attribute can't be
		found a <class>IllegalAttrError</class> will be raised.
		"""
		if not isinstance(xmlns, (list, tuple)):
			xmlns = (xmlns,)
		for xmlns in xmlns:
			xmlns = nsname(xmlns)
			try:
				return self._attrsbyxmlname[(name, xmlns)]
			except KeyError:
				pass
		for base in self.bases:
			try:
				return base.attrclass_xml(name, xmlns)
			except IllegalAttrError:
				pass
		raise IllegalAttrError(name, xmlns, True)

	def text(self, content):
		"""
		Create a text node with the content <arg>content</arg>.
		"""
		return Text(content)

	def comment(self, content):
		"""
		Create a comment node with the content <arg>content</arg>.
		"""
		return Comment(content)

	def clone(self):
		"""
		Return a copy of <self/>.
		"""
		copy = Pool()
		copy._elementsbyxmlname = self._elementsbyxmlname.copy()
		copy._elementsbypyname = self._elementsbypyname.copy()
		copy._procinstsbyxmlname = self._procinstsbyxmlname.copy()
		copy._procinstsbypyname = self._procinstsbypyname.copy()
		copy._entitiesbyxmlname = self._entitiesbyxmlname.copy()
		copy._entitiesbypyname = self._entitiesbypyname.copy()
		copy._charrefsbyxmlname = self._charrefsbyxmlname.copy()
		copy._charrefsbypyname = self._charrefsbypyname.copy()
		copy._charrefsbycodepoint = self._charrefsbycodepoint.copy()
		copy._attrsbyxmlname = self._attrsbyxmlname.copy()
		copy._attrsbypyname = self._attrsbypyname.copy()
		copy.bases = self.bases[:]
		return copy

# Default class pool
defaultpool = Pool()


def getpoolstack():
	try:
		stack = getattr(local, "ll.xist.xsc.pools")
	except AttributeError:
		stack = [defaultpool]
		setattr(local, "ll.xist.xsc.pools", stack)
	return stack


###
### Functions for namespace handling
###

def docprefixes():
	"""
	Return a prefix mapping suitable for parsing &xist; docstrings.
	"""
	from ll.xist.ns import html, chars, abbr, doc, specials
	return {None: (doc, specials, html, chars, abbr)}


def nsname(xmlns):
	"""
	If <arg>xmlns</arg> is a module, return <lit><arg>xmlns</arg>.xmlns</lit>.
	Else return <arg>xmlns</arg> unchanged.
	"""
	if xmlns is not None and not isinstance(xmlns, basestring):
		xmlns = xmlns.xmlns
	return xmlns


def nsclark(xmlns):
	"""
	Return a namespace name in Clark notation. <arg>xmlns</arg> can be
	<lit>None</lit>, a string or a module.
	"""
	if xmlns is None:
		return "{}"
	elif not isinstance(xmlns, basestring):
		xmlns = xmlns.xmlns
	return "{%s}" % xmlns


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
	__slots__ = ("sysid", "pubid", "line", "col")

	def __init__(self, locator=None, sysid=None, pubid=None, line=None, col=None):
		"""
		<par>Create a new <class>Location</class> instance by reading off the
		current location from the <arg>locator</arg>, which is then stored
		internally. In addition to that the system ID, public ID, line number and
		column number can be overwritten by explicit arguments.</par>
		"""
		self.sysid = None
		self.pubid = None
		self.line = None
		self.col = None

		if locator is not None:
			self.sysid = locator.getSystemId()
			self.pubid = locator.getPublicId()
			self.line = locator.getLineNumber()
			self.col = locator.getColumnNumber()

		if sysid is not None:
			self.sysid = sysid

		if pubid is not None:
			self.pubid = pubid

		if line is not None:
			self.line = line

		if col is not None:
			self.col = col

	def getColumnNumber(self):
		"<par>Return the column number of this location.</par>"
		return self.col

	def getLineNumber(self):
		"<par>Return the line number of this location.</par>"
		return self.line

	def getPublicId(self):
		"<par>Return the public identifier for this location.</par>"
		return self.pubid

	def getSystemId(self):
		"<par>Return the system identifier for this location.</par>"
		return self.sysid

	def offset(self, offset):
		"""
		<par>Return a location where the line number is incremented by offset
		(and the column number is reset to 1).</par>
		"""
		if offset==0:
			return self
		elif self.line is None:
			return Location(sysid=self.sysid, pubid=self.pubid, line=None, col=1)
		return Location(sysid=self.sysid, pubid=self.pubid, line=self.line+offset, col=1)

	def __str__(self):
		# get and format the system ID
		sysid = self.sysid
		if sysid is None:
			sysid = "???"
		else:
			sysid = str(sysid)

		# get and format the line number
		line = self.line
		if line is None or line < 0:
			line = "?"
		else:
			line = str(line)

		# get and format the column number
		col = self.col
		if col is None or col < 0:
			col = "?"
		else:
			col = str(col)

		# now we have the parts => format them
		return "%s:%s:%s" % (sysid, line, col)

	def __repr__(self):
		return "<%s object sysid=%r, pubid=%r, line=%r, col=%r at %08x>" % (self.__class__.__name__, self.sysid, self.pubid, self.line, self.col, id(self))

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.pubid==other.pubid and self.sysid==other.sysid and self.line==other.line and self.col==other.col

	def __ne__(self, other):
		return not self==other

	def __xattrs__(self, mode="default"):
		return ("sysid", "pubid", "line", "col")

	def __xrepr__(self, mode="default"):
		yield (astyle.style_url, self.sysid)
		yield (astyle.style_default, ":")
		for part in ipipe.xrepr(self.line, mode):
			yield part
		yield (astyle.style_default, ":")
		for part in ipipe.xrepr(self.col, mode):
			yield part
