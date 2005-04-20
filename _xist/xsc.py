#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
This module contains all the central &xml; tree classes, the namespace classes,
exception and warning classes and a few helper classes and functions.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import os, sys, random, copy, warnings, new, cStringIO, cPickle

import ll
from ll import url, ansistyle


# XPython support
try:
	import iexec
except ImportError:
	iexec = None


###
### helpers
###

def ToNode(value):
	"""
	<par>convert <arg>value</arg> to an &xist; <pyref class="Node"><class>Node</class></pyref>.</par>

	<par>If <arg>value</arg> is a tuple or list, it will be (recursively) converted
	to a <pyref class="Frag"><class>Frag</class></pyref>. Integers, strings, etc.
	will be converted to a <pyref class="Text"><class>Text</class></pyref>.
	If <arg>value</arg> is a <pyref class="Node"><class>Node</class></pyref> already,
	it will be returned unchanged. In the case of <lit>None</lit> the &xist; Null
	(<class>ll.xist.xsc.Null</class>) will be returned. If <arg>value</arg> is
	iteratable, a <class>Frag</class> will be generated from the items.
	Anything else will issue a warning and will be ignored (by returning
	<class>Null</class>).</par>
	"""
	if isinstance(value, Node):
		# we don't have to turn an Attr into a Frag, because this will be done once the Attr is put back into the tree
		return value
	elif isinstance(value, (basestring, int, long, float)):
		return Text(value)
	elif value is None:
		return Null
	elif isinstance(value, (list, tuple)):
		return Frag(*value)
	elif isinstance(value, url.URL):
		return Text(value)
	else:
		# Maybe it's an iterator/generator?
		try:
			return Frag(*list(value))
		except TypeError:
			pass
	warnings.warn(IllegalObjectWarning(value)) # none of the above, so we report it and maybe throw an exception
	return Null


###
### XPython support
###

def append(*args, **kwargs):
	"""
	<function>append</function> can be used with XPython. It append items in
	<arg>args</arg> (or sets attributes in <arg>kwargs</arg>) in the currenty
	active node.
	"""
	node = iexec.getinstance((converters.Converter, Frag, Element)) # requires XPython
	if node is not None:
		if isinstance(node, converters.Converter):
			node.node.append(*args)
		elif isinstance(node, Frag):
			node(*args)
		else:
			node(*args, **kwargs)


###
###
###

class _Base_Meta(type):
	def __new__(cls, name, bases, dict):
		dict["__outerclass__"] = None
		self = super(_Base_Meta, cls).__new__(cls, name, bases, dict)
		for (key, value) in dict.iteritems():
			if isinstance(value, type):
				value.__outerclass__ = self
		return self

	def __repr__(self):
		return "<class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))


class Base(object):
	"""
	<par>Base class that adds an enhanced class <method>__repr__</method> method
	and a class method <pyref method="__fullname__"><method>__fullname__</method></pyref>
	to subclasses. Subclasses of <class>Base</class> will have an attribute
	<lit>__outerclass__</lit> that references the containing class (if there
	is any). <method>__repr__</method> uses this to show the fully qualified
	class name.</par>
	"""
	__metaclass__ = _Base_Meta

	def __repr__(self):
		return "<%s:%s object at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	@classmethod
	def __fullname__(cls):
		"""
		<par>Return the fully qualified class name (i.e. including containing
		classes, if this class has been defined inside another one).</par>
		"""
		name = cls.__name__.split(".")[-1]
		while True:
			cls = cls.__outerclass__
			if cls is None:
				return name
			name = cls.__name__.split(".")[-1] + "." + name


###
### Magic constants for tree traversal
###

class Const(object):
	__slots__ = ("_name")

	def __init__(self, name):
		self._name = name

	def __repr__(self):
		return "%s.%s" % (self.__module__, self._name)

entercontent = Const("entercontent")
enterattrs = Const("enterattrs")
walknode = Const("walknode")
walkpath = Const("walkpath")
walkindex = Const("walkindex")
walkrootindex = Const("walkrootindex")


###
### Common tree traversal filters
###

class FindType(object):
	"""
	Tree traversal filter that finds nodes of a certain type on the first level
	of the tree without decending further down.
	"""
	def __init__(self, *types):
		self.types = types

	def __call__(self, node):
		return (isinstance(node, self.types), )


class FindTypeAll(object):
	"""
	Tree traversal filter that finds nodes of a certain type searching the
	complete tree.
	"""
	def __init__(self, *types):
		self.types = types

	def __call__(self, node):
		return (isinstance(node, self.types), entercontent)


class FindTypeAllAttrs(object):
	"""
	Tree traversal filter that finds nodes of a certain type searching the
	complete tree (including attributes).
	"""
	def __init__(self, *types):
		self.types = types

	def __call__(self, node):
		return (isinstance(node, self.types), entercontent, enterattrs)


class FindTypeTop(object):
	"""
	Tree traversal filter, that find nodes of a certain type searching the
	complete tree, but traversal of the children of a node is skipped if this
	node is of the specified type.
	"""
	def __init__(self, *types):
		self.types = types
	def __call__(self, node):
		if isinstance(node, self.types):
			return (True,)
		else:
			return (entercontent,)


###
### Conversion context
###

class Context(Base, list):
	"""
	<par>This is an empty class, that can be used by the
	<pyref class="Node" method="convert"><method>convert</method></pyref>
	method to hold element or namespace specific data during the convert call.
	The method <pyref class="Converter" method="__getitem__"><method>Converter.__getitem__</method></pyref>
	will return a unique instance of this class.</par>
	"""

_Context = Context


###
### Exceptions and warnings
###

class Error(Exception):
	"""
	base class for all &xist; exceptions
	"""
	pass


class Warning(UserWarning):
	"""
	base class for all warning exceptions (i.e. those that won't
	result in a program termination.)
	"""
	pass


class IllegalAttrError(Warning, LookupError):
	"""
	exception that is raised, when an element has an illegal attribute
	(i.e. one that isn't defined in the appropriate attributes class)
	"""

	def __init__(self, attrs, attrname, xml=False):
		self.attrs = attrs
		self.attrname = attrname
		self.xml = xml

	def __str__(self):
		if self.attrs is not None:
			return "Attribute with %s name %r not allowed for %s" % (("Python", "XML")[self.xml], self.attrname, self.attrs._str(fullname=True, xml=False, decorate=False))
		else:
			return "Global attribute with %s name %r not allowed" % (("Python", "XML")[self.xml], self.attrname)


class IllegalAttrValueWarning(Warning):
	"""
	warning that is issued when an attribute has an illegal value when parsing or publishing.
	"""

	def __init__(self, attr):
		self.attr = attr

	def __str__(self):
		attr = self.attr
		return "Attribute value %r not allowed for %s. " % (str(attr), attr._str(fullname=True, xml=False, decorate=False))


class RequiredAttrMissingWarning(Warning):
	"""
	warning that is issued when a required attribute is missing during parsing or publishing.
	"""

	def __init__(self, attrs, reqattrs):
		self.attrs = attrs
		self.reqattrs = reqattrs

	def __str__(self):
		v = ["Required attribute"]
		if len(self.reqattrs)>1:
			v.append("s ")
			v.append(", ".join("%r" % attr for attr in self.reqattrs))
		else:
			v.append(" %r" % self.reqattrs[0])
		v.append(" missing in %s." % self.attrs._str(fullname=True, xml=False, decorate=False))
		return "".join(v)


class IllegalDTDChildWarning(Warning):
	"""
	warning that is issued when the <pyref module="ll.xist.parsers" class="HTMLParser"><class>HTMLParser</class></pyref>
	detects an element that is not allowed inside its parent element according to the &html; &dtd;
	"""

	def __init__(self, childname, parentname):
		self.childname = childname
		self.parentname = parentname

	def __str__(self):
		return "Element %s not allowed as a child of element %s" % (self.childname, self.parentname)


class IllegalCloseTagWarning(Warning):
	"""
	warning that is issued when the <pyref module="ll.xist.parsers" class="HTMLParser"><class>HTMLParser</class></pyref>
	finds an end tag that has no corresponding start tag.
	"""

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "Element %s has never been opened" % (self.name,)


class IllegalPrefixError(Error, LookupError):
	"""
	Exception that is raised when a namespace prefix is undefined.
	"""
	def __init__(self, prefix):
		self.prefix = prefix

	def __str__(self):
		return "namespace prefix %r is undefined" % self.prefix


class IllegalNamespaceError(Error, LookupError):
	"""
	Exception that is raised when a namespace name is undefined
	i.e. if there is no namespace with this name.
	"""
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "namespace name %r is undefined" % self.name


class IllegalNodeError(Error, LookupError):
	"""
	exception that is raised, when an illegal node class (element, procinst, entity or charref) is requested
	"""

	type = "node"

	def __init__(self, name, xml=False):
		self.name = name
		self.xml = xml

	def __str__(self):
		return "%s with %s name %r not allowed" % (self.type, ("Python", "XML")[self.xml], self.name, )


class IllegalElementError(IllegalNodeError):
	type = "element"


class IllegalProcInstError(IllegalNodeError):
	type = "procinst"


class IllegalEntityError(IllegalNodeError):
	type = "entity"


class IllegalCharRefError(IllegalNodeError):
	type = "charref"

	def __str__(self):
		if isinstance(self.name, (int, long)):
			return "%s with codepoint %s not allowed" % (self.type, self.name)
		else:
			return IllegalNodeError.__str__(self)


class AmbiguousNodeError(Error, LookupError):
	"""
	exception that is raised, when an node class is ambiguous (most commonly for processing instructions or entities)
	"""

	type = "node"

	def __init__(self, name, xml=False):
		self.name = name
		self.xml = xml

	def __str__(self):
		return "%s with %s name %r is ambigous" % (self.type, ("Python", "XML")[self.xml], self.name)


class AmbiguousProcInstError(AmbiguousNodeError):
	type = "procinst"


class AmbiguousEntityError(AmbiguousNodeError):
	type = "entity"


class AmbiguousCharRefError(AmbiguousNodeError):
	type = "charref"

	def __str__(self):
		if isinstance(self.name, (int, long)):
			return "%s with codepoint %r is ambigous" % (self.type, self.name)
		else:
			return AmbiguousNodeError.__str__(self)


class MultipleRootsError(Error):
	def __str__(self):
		return "can't add namespace attributes: XML tree has multiple roots"


class ElementNestingError(Error):
	"""
	exception that is raised, when an element has an illegal nesting
	(e.g. <lit>&lt;a&gt;&lt;b&gt;&lt;/a&gt;&lt;/b&gt;</lit>)
	"""

	def __init__(self, expectedelement, foundelement):
		self.expectedelement = expectedelement
		self.foundelement = foundelement

	def __str__(self):
		return "mismatched element nesting (close tag for %s expected; close tag for %s found)" % (self.expectedelement._str(fullname=1, xml=0, decorate=1), self.foundelement._str(fullname=1, xml=0, decorate=1))


class IllegalAttrNodeError(Error):
	"""
	exception that is raised, when something is found
	in an attribute that doesn't belong there (e.g. an element or a comment).
	"""

	def __init__(self, node):
		self.node = node

	def __str__(self):
		return "illegal node of type %s found inside attribute" % self.node.__class__.__name__


class NodeNotFoundError(Error):
	"""
	exception that is raised when <pyref module="ll.xist.xsc" class="Node" method="findfirst"><method>findfirst</method></pyref> fails.
	"""
	def __str__(self):
		return "no appropriate node found"


class FileNotFoundWarning(Warning):
	"""
	warning that is raised, when a file can't be found
	"""
	def __init__(self, message, filename, exc):
		Warning.__init__(self, message, filename, exc)
		self.message = message
		self.filename = filename
		self.exc = exc

	def __str__(self):
		return "%s: %r not found (%s)" % (self.message, self.filename, self.exc)


class IllegalObjectWarning(Warning):
	"""
	warning that is issued when &xist; finds an illegal object in its object tree.
	"""

	def __init__(self, object):
		self.object = object

	def __str__(self):
		s = "an illegal object %r of type %s has been found in the XSC tree. The object will be ignored." % (self.object, type(self.object).__name__)
		return s


class MalformedCharRefWarning(Warning):
	"""
	exception that is raised when a character reference is malformed (e.g. <lit>&amp;#foo;</lit>)
	"""

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "malformed character reference: &%s;" % self.name


class IllegalCommentContentWarning(Warning):
	"""
	warning that is issued when there is an illegal comment, i.e. one
	containing <lit>--</lit> or ending in <lit>-</lit>.
	(This can only happen, when the comment is instantiated by the
	program, not when parsed from an &xml; file.)
	"""

	def __init__(self, comment):
		self.comment = comment

	def __str__(self):
		return "comment with content %s is illegal, as it contains '--' or ends in '-'." % presenters.strTextOutsideAttr(self.comment.content)


class IllegalProcInstFormatError(Error):
	"""
	exception that is raised, when there is an illegal processing instruction, i.e. one containing <lit>?&gt;</lit>.
	(This can only happen, when the processing instruction is instantiated by the
	program, not when parsed from an &xml; file.)
	"""

	def __init__(self, procinst):
		self.procinst = procinst

	def __str__(self):
		return "processing instruction with content %s is illegal, as it contains %r." % (presenters.strProcInstContent(self.procinst.content), "?>")


class IllegalXMLDeclFormatError(Error):
	"""
	exception that is raised, when there is an illegal XML declaration,
	i.e. there something wrong in <lit>&lt;?xml ...?&gt;</lit>.
	(This can only happen, when the processing instruction is instantiated by the
	program, not when parsed from an &xml; file.)
	"""

	def __init__(self, procinst):
		self.procinst = procinst

	def __str__(self):
		return "XML declaration with content %r is malformed." % presenters.strProcInstContent(self.procinst.content)


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
	Error that is raised, when a convert method can't find required context
	info.
	"""

	def __init__(self, node, outerclass):
		self.node = node
		self.outerclass = outerclass

	def __str__(self):
		s = "node %s" % self.node._str(fullname=True, xml=False, decorate=True)
		if self.node.startloc is not None:
			s += " at %s" % self.node.startloc
		s += " outside of %r" % self.outerclass
		return s


###
### The DOM classes
###

import xfind

class _Node_Meta(Base.__metaclass__, xfind.Operator):
	def __new__(cls, name, bases, dict):
		if "register" not in dict:
			dict["register"] = True
		dict["__ns__"] = None
		# needsxmlns may be defined as a constant, this magically turns it into method
		if "needsxmlns" in dict:
			needsxmlns_value = dict["needsxmlns"]
			if not isinstance(needsxmlns_value, classmethod):
				@classmethod
				def needsxmlns(cls, publisher=None):
					return needsxmlns_value
				dict["needsxmlns"] = needsxmlns
		if "xmlprefix" in dict:
			xmlprefix_value = dict["xmlprefix"]
			if not isinstance(xmlprefix_value, classmethod):
				@classmethod
				def xmlprefix(cls, publisher=None):
					return xmlprefix_value
				dict["xmlprefix"] = xmlprefix
		dict["xmlname"] = dict.get("xmlname", name).split(".")[-1]
		return super(_Node_Meta, cls).__new__(cls, name, bases, dict)

	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, (Frag, Element)):
				for subchild in child:
					if isinstance(subchild, self):
						yield subchild


class Node(Base):
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
	# None:  don't add this class to a namespace, not even to the "global" namespace,
	#        the xmlns attribute of those classes will be None. This is used for Element etc.
	#        to avoid bootstrapping problems and should never be used by user classes
	# False: Register with the namespace, i.e. ns.element("foo") will return it and foo.xmlns
	#        will be set to the namespace class, but don't use this class for parsing
	# True:  Register with the namespace and use for parsing.
	# If register is not set it defaults to True

	class Context(_Context):
		pass

	def __repr__(self):
		"""
		<par>Use the default presenter (defined in
		<pyref module="ll.xist.presenters"><module>ll.xist.presenters</module></pyref>)
		to return a string representation.</par>
		"""
		return self.repr(presenters.defaultpresenter)

	def __ne__(self, other):
		return not self==other

	@classmethod
	def _strbase(cls, formatter, s, fullname, xml):
		if fullname:
			if xml:
				s.append(presenters.strNamespace(cls.xmlname))
			else:
				s.append(presenters.strNamespace(cls.__module__))
			s.append(presenters.strColon())
		if xml:
			s.append(formatter(cls.xmlname))
		elif fullname:
			s.append(formatter(cls.__fullname__()))
		else:
			s.append(formatter(cls.__name__))

	def clone(self):
		"""
		return a clone of <self/>. Compared to <pyref method="deepcopy"><method>deepcopy</method></pyref> <method>clone</method>
		will create multiple instances of objects that can be found in the tree more than once. <method>clone</method> can't
		clone trees that contains cycles.
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

	def repr(self, presenter=None):
		"""
		<par>Return a string representation of <self/>. When you don't pass in a
		<arg>presenter</arg>, you'll get the default presentation. Else
		<arg>presenter</arg> should be an instance of
		<pyref module="ll.xist.presenters" class="Presenter"><class>ll.xist.presenters.Presenter</class></pyref>
		(or one of the subclasses).</par>
		"""
		if presenter is None:
			presenter = presenters.defaultpresenter
		return presenter.present(self)

	@ll.notimplemented
	def present(self, presenter):
		"""
		<par><method>present</method> is used as a central dispatch method for
		the <pyref module="ll.xist.presenters">presenter classes</pyref>. Normally
		it is not called by the user, but internally by the presenter. The user
		should call <pyref method="repr"><method>repr</method></pyref>
		instead.</par>
		"""
		# Subclasses of Node implement this method by calling the appropriate present* method in the publisher (i.e. double dispatch)

	def conv(self, converter=None, root=None, mode=None, stage=None, target=None, lang=None, function=None, makeaction=None, maketarget=None):
		"""
		<par>Convenience method for calling <pyref method="convert"><method>convert</method></pyref>.</par>
		<par><method>conv</method> will automatically set <lit><arg>converter</arg>.node</lit> to <self/> to remember the
		<z>document root node</z> for which <method>conv</method> has been called, this means that you should not call
		<method>conv</method> in any of the recursive calls, as you would loose this information. Call
		<pyref method="convert"><method>convert</method></pyref> directly instead.</par>
		"""
		if converter is None:
			converter = converters.Converter(node=self, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, maketarget=maketarget)
			return self.convert(converter)
		else:
			converter.push(node=self, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, maketarget=maketarget)
			node = self.convert(converter)
			converter.pop()
			return node

	@ll.notimplemented
	def convert(self, converter):
		"""
		<par>implementation of the conversion method. When you define your own
		element classes you have to overwrite this method and implement the desired
		conversion.</par>

		<par>This method must return an instance of <class>Node</class>.</par>
		"""
		pass

	@ll.notimplemented
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

	def asText(self, monochrome=True, squeezeBlankLines=False, lineNumbers=False, width=72):
		"""
		<par>Return the node as a formatted plain string. Note that this really
		only make sense for &html; trees.</par>

		<par>This requires that <app moreinfo="http://w3m.sf.net/">w3m</app> is
		installed.</par>
		"""

		options = []
		if monochrome:
			options.append("-M")
		if squeezeBlankLines:
			options.append("-S")
		if lineNumbers:
			options.append("-num")
		if width != 80:
			options.append("-cols %d" % width)

		text = self.asBytes(encoding="iso-8859-1")

		cmd = "w3m %s -T text/html -dump" % " ".join(options)
		(stdin, stdout) = os.popen2(cmd)

		stdin.write(text)
		stdin.close()
		text = stdout.read()
		stdout.close()
		text = "\n".join(line.rstrip() for line in text.splitlines())
		return text

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

	@classmethod
	def needsxmlns(self, publisher=None):
		"""
		<par>Return what type of namespace prefix/declaration is needed for
		<self/> when publishing. Possible return values are:</par>
		<ulist>
		<item><lit>0</lit>: Neither a prefix nor a declaration is required;</item>
		<item><lit>1</lit>: A prefix is required, but no declaration (e.g. for the
		<pyref module="ll.xist.ns.xml"><module>xml</module></pyref> namespace,
		whose prefix is always defined.</item>
		<item><lit>2</lit>: Both a prefix and a declaration for this prefix are
		required.</item>
		</ulist>
		"""
		if publisher is not None:
			return publisher.prefixmode
		else:
			return 0

	@classmethod
	def xmlprefix(cls, publisher=None):
		"""
		Return the namespace prefix configured for publishing elements of this
		class with the publisher <arg>publisher</arg> (or the default prefix
		from the namespace if <arg>publisher</arg> is <lit>None</lit>).
		"""
		if cls.__ns__ is None:
			return None
		else:
			if publisher is None:
				return cls.__ns__.xmlname
			else:
				return publisher.prefixes.prefix4ns(cls.__ns__)[0]

	def _publishname(self, publisher):
		"""
		Publish the name of <self/> to the <arg>publisher</arg> including a
		namespace prefix if required.
		"""
		if self.needsxmlns(publisher)>=1:
			prefix = self.xmlprefix(publisher)
			if prefix is not None:
				publisher.write(prefix)
				publisher.write(u":")
		publisher.write(self.xmlname)

	def parsed(self, parser, start=None):
		"""
		<par>This method will be called by the parser <arg>parser</arg> once after
		<self/> is created by the parser. This is e.g. used by
		<pyref class="URLAttr"><class>URLAttr</class></pyref> to incorporate
		the base <pyref module="ll.url" class="URL"><class>URL</class></pyref>
		into the attribute.</par>

		<par>For elements <function>parsed</function> will be called twice:
		Once at the beginning (i.e. before the content is parsed) with
		<lit><arg>start</arg>==True</lit> and once at the end after parsing of
		the content is finished <lit><arg>start</arg>==False</lit>.</par>
		"""
		pass

	def checkvalid(self):
		"""
		<par>This method will be called when parsing or publishing to check
		whether <self/> is valid.</par>
	
		<par>If <self/> is found to be invalid a warning should be issued through
		the <pyref module="warnings">Python warning framework</pyref>.</par>
		"""
		pass

	@ll.notimplemented
	def publish(self, publisher):
		"""
		Generate unicode strings for the node, and pass the strings to
		<lit><arg>publisher</arg>.write</lit>. <arg>publisher</arg> must be an
		instance of
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref>.

		<par>The encoding and xhtml specification are taken from the <arg>publisher</arg>.</par>
		"""
		pass

	def asString(self, base=None, publisher=None, **publishargs):
		"""
		<par>Return this node as a serialized unicode string.</par>

		<par>For the possible parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref>
		constructor.</par>
		"""
		stream = cStringIO.StringIO()
		if publisher is None:
			publisher = publishers.Publisher(**publishargs)
		oldencoding = publisher.encoding
		try:
			publisher.encoding = "utf-8"
			publisher.publish(stream, self, base)
		finally:
			publisher.encoding = oldencoding
		return stream.getvalue().decode("utf-8")

	def asBytes(self, base=None, publisher=None, **publishargs):
		"""
		<par>Return this node as a serialized byte string.</par>

		<par>For the possible parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref>
		constructor.</par>
		"""
		stream = cStringIO.StringIO()
		if publisher is None:
			publisher = publishers.Publisher(**publishargs)
		publisher.publish(stream, self, base)
		return stream.getvalue()

	def write(self, stream, base=None, publisher=None, **publishargs):
		"""
		<par>Write <self/> to the file-like object <arg>stream</arg> (which must
		provide a <method>write</method> method).</par>

		<par>For the rest of the parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref>
		constructor.</par>
		"""
		if publisher is None:
			publisher = publishers.Publisher(**publishargs)
		publisher.publish(stream, self, base)

	def _walk(self, filter, path, index, inmode, outmode):
		"""
		<par>Internal helper for <pyref method="walk"><method>walk</method></pyref>.</par>
		"""
		if callable(filter):
			if inmode is walknode:
				found = filter(self)
			elif inmode is walkpath:
				found = filter(path)
			elif inmode is walkindex:
				found = filter(index)
			elif inmode is walkrootindex:
				found = filter(path[0], index)
			else:
				raise ValueError("unknown inmode %r" % inmode)
		else:
			found = filter

		for option in found:
			if option is not entercontent and option is not enterattrs and option:
				if outmode is walknode:
					yield self
				elif outmode is walkpath:
					yield path[:]
				elif outmode is walkindex:
					yield index[:]
				elif outmode is walkrootindex:
					yield (path[0], index[:])
				else:
					raise ValueError("unknown outmode %r" % outmode)

	def walk(self, filter=(True, entercontent), inmode=walknode, outmode=walknode):
		"""
		<par>Return an iterator for traversing the tree rooted at <self/>.</par>

		<par><arg>filter</arg> is used for specifying whether or not a node should
		be yielded and when the children of this node should be traversed. If
		<arg>filter</arg> is callable, it will be called for each node visited
		during the traversal and must return a sequence of <z>node handling
		options</z>. Otherwise (i.e. if <arg>filter</arg> is not callable)
		<arg>filter</arg> must be a sequence of node handling options that will
		be used for all visited nodes.</par>

		<par>Entries in this sequence can be the following:</par>

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

		<par><arg>immode</arg> specifies how <arg>filter</arg> will be called.
		There are four constant that can be passed:</par>
		<dlist>
		<term><lit>walknode</lit></term><item><method>walk</method>
		will pass the node itself to the filter function;</item>
		<term><lit>walkpath</lit></term><item>a list containing the complete path
		from the root node to the node to be tested will be passed to <arg>filter</arg>;</item>
		<term><lit>walkindex</lit></term><item>A list of child indizes and attribute
		names that specifies the path to the node in question is passed.</item>
		<term><lit>walkrootindex</lit></term><item>Two arguments will be passed to
		the filter function. The first is the root node and the second is an index
		path (just like for <lit>walkindex</lit>).</item>
		</dlist>

		<par><arg>outmode</arg> works similar to <arg>inmode</arg> and
		specifies what will be yielded from the iterator.</par>
		"""
		return self._walk(filter, [self], [], inmode, outmode)

	def find(self, filter=(True, entercontent), inmode=walknode):
		"""
		Return a <pyref class="Frag"><class>Frag</class></pyref> containing all
		nodes found by the filter function <arg>filter</arg>. See
		<pyref method="walk"><method>walk</method></pyref> for an explanation of
		the arguments.
		"""
		return Frag(self.walk(filter, inmode, walknode))

	def findfirst(self, filter=(True, entercontent), inmode=walknode):
		"""
		Return the first node found by the filter function <arg>filter</arg>.
		See <pyref method="walk"><method>walk</method></pyref> for an explanation
		of the arguments.
		"""
		for item in self.walk(filter, inmode, walknode):
			return item
		raise NodeNotFoundError()

	def __div__(self, other):
		return xfind.Expr(self, other)
		
	def __floordiv__(self, other):
		return xfind.Expr(self, xfind.all, other)
		
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

	def mapped(self, function, converter):
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

	def withSep(self, separator, clone=False):
		warnings.warn(DeprecationWarning("withSep() is deprecated, use withsep() instead"))
		return self.withsep(separator, clone)


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

	class content(ll.propclass):
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

	# find will be the one inherited from Node

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
		publisher.writetext(self._content)

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

	def __init__(self, *content):
		list.__init__(self)
		for child in content:
			child = ToNode(child)
			if isinstance(child, Frag):
				list.extend(self, child)
			elif child is not Null:
				list.append(self, child)

	def __call__(self, *content):
		self.extend(content)
		return self

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen())
		cls._strbase(presenters.strElementName, s, fullname=fullname, xml=xml)
		if decorate:
			s.append(presenters.strBracketClose())
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
		presenter.presentFrag(self)

	def __unicode__(self):
		return u"".join(unicode(child) for child in self)

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
		if isinstance(index, list):
			node = self
			for subindex in index:
				node = node[subindex]
			return node
		elif isinstance(index, type) and issubclass(index, Node):
			# We can't use yield directly, because this method can't be both a function and a generator
			def iterate(self, index):
				for child in self:
					if isinstance(child, index):
						yield child
			return iterate(self, index)
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
		If <arg>index</arg> is an empty list, the call will be ignored.</par>
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
		If <arg>index</arg> is an empty list the call will be ignored.</par>
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
			other = ToNode(other)
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

	def _walk(self, filter, path, index, inmode, outmode):
		path.append(None)
		index.append(0)
		for child in self:
			path[-1] = child
			for result in child._walk(filter, path, index, inmode, outmode):
				yield result
			index[-1] += 1
		path.pop()
		index.pop()

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
		<par>Return a sorted version of the <self/>. <arg>compare</arg> is
		a comparison function returning -1, 0, 1 respectively and defaults to comparing the
		<pyref class="Node" method="__unicode__"><class>__unicode__</class></pyref> value.</par>
		"""
		node = list(self)
		node.sort(compare)
		return self.__class__(node)

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
		<par>Return a shuffled version of <self/>i, i.e. a copy of <self/> where
		the content nodes are randomly reshuffled.</par>
		"""
		content = list(self)
		node = self._create()
		while content:
			index = random.randrange(len(content))
			list.append(node, content[index])
			del content[index]
		return node

	def mapped(self, function, converter):
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


class Comment(CharacterData):
	"""
	An &xml; comment.
	"""

	def convert(self, converter):
		return self

	def __unicode__(self):
		return u""

	def present(self, presenter):
		presenter.presentComment(self)

	def publish(self, publisher):
		if publisher.inattr:
			raise IllegalAttrNodeError(self)
		content = self.content
		if u"--" in content or content.endswith(u"-"):
			warnings.warn(IllegalCommentContentWarning(self))
		publisher.write(u"<!--")
		publisher.write(content)
		publisher.write(u"-->")


class DocType(CharacterData):
	"""
	An &xml; document type declaration.
	"""

	def convert(self, converter):
		return self

	def present(self, presenter):
		presenter.presentDocType(self)

	def publish(self, publisher):
		if publisher.inattr:
			raise IllegalAttrNodeError(self)
		publisher.write(u"<!DOCTYPE ")
		publisher.write(self.content)
		publisher.write(u">")

	def __unicode__(self):
		return u""


class _ProcInst_Meta(CharacterData.__metaclass__):
	def __repr__(self):
		return "<procinst class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))


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
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen(), presenters.strQuestion())
		cls._strbase(presenters.strProcInstTarget, s, fullname=fullname, xml=xml)
		if decorate:
			s.append(presenters.strQuestion(), presenters.strBracketClose())
		return s

	def convert(self, converter):
		return self

	def present(self, presenter):
		presenter.presentProcInst(self)

	def publish(self, publisher):
		content = self.content
		if u"?>" in content:
			raise IllegalProcInstFormatError(self)
		publisher.write(u"<?")
		publisher.write(self.xmlname)
		publisher.write(u" ")
		publisher.write(content)
		publisher.write(u"?>")

	def __unicode__(self):
		return u""


class Null(CharacterData):
	"""
	node that does not contain anything.
	"""

	@classmethod
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

	def convert(self, converter):
		return self

	def publish(self, publisher):
		pass

	def present(self, presenter):
		presenter.presentNull(self)

	def __unicode__(self):
		return u""

Null = Null() # Singleton, the Python way


class _Attr_Meta(Frag.__metaclass__, xfind.Operator):
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
				dict["values"] = tuple(unicode(entry) for entry in dict["values"])
		return super(_Attr_Meta, cls).__new__(cls, name, bases, dict)

	def __repr__(self):
		return "<attribute class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def xwalk(self, iterator):
		for child in iterator:
			if isinstance(child, Element):
				for (attrname, attrvalue) in child.attrs.iteritems():
					if isinstance(attrvalue, self):
						yield attrvalue


class Attr(Frag):
	"""
	<par>Base class of all attribute classes.</par>

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
		<par>Return whether <self/> contains nodes
		other than <pyref class="Text"><class>Text</class></pyref>.</par>
		"""
		for child in self:
			if not isinstance(child, Text):
				return True
		return False

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		cls._strbase(presenters.strAttrName, s, fullname=fullname, xml=xml)
		return s

	def present(self, presenter):
		presenter.presentAttr(self)

	@classmethod
	def needsxmlns(self, publisher=None):
		if self.__ns__ is not None:
			return 2
		else:
			return 0

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

	def _walk(self, filter, path, index, inmode, outmode):
		if callable(filter):
			if inmode is walknode:
				found = filter(self)
			elif inmode is walkpath:
				found = filter(path)
			elif inmode is walkindex:
				found = filter(index)
			elif inmode is walkrootindex:
				found = filter(path[0], index)
			else:
				raise ValueError("unknown inmode %r" % inmode)
		else:
			found = filter

		for option in found:
			if option is entercontent:
				for object in Frag._walk(self, filter, path, index, inmode, outmode):
					yield object
			elif option is enterattrs:
				pass
			elif option:
				if outmode is walknode:
					yield self
				elif outmode is walkpath:
					yield path[:]
				elif outmode is walkindex:
					yield index[:]
				elif outmode is walkrootindex:
					yield (path[0], index[:])
				else:
					raise ValueError("unknown outmode %r" % outmode)

	def _publishAttrValue(self, publisher):
		Frag.publish(self, publisher)

	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		publisher.inattr += 1
		self._publishname(publisher) # publish the XML name, not the Python name
		publisher.write(u"=\"")
		publisher.pushtextfilter(helpers.escapeattr)
		self._publishAttrValue(publisher)
		publisher.poptextfilter()
		publisher.write(u"\"")
		publisher.inattr -= 1

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

	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		publisher.inattr += 1
		self._publishname(publisher) # publish the XML name, not the Python name
		if publisher.xhtml>0:
			publisher.write(u"=\"")
			publisher.pushtextfilter(helpers.escapeattr)
			publisher.write(self.__class__.xmlname)
			publisher.poptextfilter()
			publisher.write(u"\"")
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
			self[:] = (value, )

	def _publishAttrValue(self, publisher):
		if not self.isfancy():
			csshandler = cssparsers.PublishHandler(ignorecharset=True)
			value = csshandler.parseString(unicode(self), base=publisher.base)
			new = Frag(value)
			new.publish(publisher)
		else:
			super(StyleAttr, self)._publishAttrValue(publisher)

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
		self[:] = utils.replaceInitialURL(self, lambda u: parser.base/u)

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


class _Attrs_Meta(Node.__metaclass__):
	def __new__(cls, name, bases, dict):
		# Automatically inherit the attributes from the base class (because the global Attrs require a pointer back to their defining namespace)
		for base in bases:
			for attrname in dir(base):
				attr = getattr(base, attrname)
				if isinstance(attr, type) and issubclass(attr, Attr) and attrname not in dict:
					classdict = {"__module__": dict["__module__"]}
					if attr.__name__ != attr.xmlname:
						classdict["xmlname"] = attr.xmlname
					classdict["__outerclass__"] = 42
					dict[attrname] = attr.__class__(attr.__name__, (attr,), classdict)
		dict["_attrs"] = ({}, {}) # cache for attributes (by Python name and by XML name)
		dict["_defaultattrs"] = ({}, {}) # cache for attributes that have a default value (by Python name and by XML name)
		self = super(_Attrs_Meta, cls).__new__(cls, name, bases, dict)
		# go through the attributes and put them in the cache
		for (key, value) in self.__dict__.iteritems():
			if isinstance(value, type):
				if getattr(value, "__outerclass__", None) == 42:
					value.__outerclass__ = self
				if issubclass(value, Attr):
					setattr(self, key, value)
		return self

	def __repr__(self):
		return "<attrs class %s:%s with %s attrs at 0x%x>" % (self.__module__, self.__fullname__(), len(self._attrs[0]), id(self))

	def __getitem__(self, key):
		return self._attrs[False][key]

	def __delattr__(self, key):
		value = self.__dict__.get(key, None) # no inheritance
		if isinstance(value, type) and issubclass(value, Attr):
			for (xml, name) in ((False, value.__name__), (True, value.xmlname)):
				self._attrs[xml].pop(name, None)
				self._defaultattrs[xml].pop(name, None)
		return super(_Attrs_Meta, self).__delattr__(key)

	def __setattr__(self, key, value):
		oldvalue = self.__dict__.get(key, None) # no inheritance
		if isinstance(oldvalue, type) and issubclass(oldvalue, Attr):
			for (xml, name) in ((False, oldvalue.__name__), (True, oldvalue.xmlname)):
				# ignore KeyError exceptions, because in the meta class constructor the attributes *are* in the class dict, but haven't gone through __setattr__, so they are not in the cache
				self._attrs[xml].pop(name, None)
				self._defaultattrs[xml].pop(name, None)
		if isinstance(value, type) and issubclass(value, Attr):
			for (xml, name) in ((False, value.__name__), (True, value.xmlname)):
				self._attrs[xml][name] = value
				if value.default:
					self._defaultattrs[xml][name] = value
		return super(_Attrs_Meta, self).__setattr__(key, value)

	def __contains__(self, key):
		return key in self._attrs[False]


class Attrs(Node, dict):
	"""
	<par>An attribute map. Allowed entries are specified through nested subclasses
	of <pyref class="Attr"><class>Attr</class></pyref>.</par>
	"""
	__metaclass__ = _Attrs_Meta

	def __init__(self, content=None, **attrs):
		dict.__init__(self)
		# set default attribute values
		for (key, value) in self._defaultattrs[False].iteritems():
			self[key] = value.default.clone()
		# set attributes, this might overwrite (or delete) default attributes
		self.update(content, **attrs)

	def __eq__(self, other):
		return self.__class__ is other.__class__ and dict.__eq__(self, other)

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		cls._strbase(presenters.strAttrsName, s, fullname=fullname, xml=xml)
		return s

	def _create(self):
		node = self.__class__() # "virtual" constructor
		node.clear()
		return node

	def clone(self):
		node = self._create()
		for (key, value) in dict.iteritems(self):
			dict.__setitem__(node, key, value.clone())
		return self._decoratenode(node)

	def __copy__(self):
		node = self._create()
		for (key, value) in dict.iteritems(self):
			dict.__setitem__(node, key, value)
		return self._decoratenode(node)

	def __deepcopy__(self, memo=None):
		node = self._create()
		if memo is None:
			memo = {}
		memo[id(self)] = node
		for (key, value) in dict.iteritems(self):
			dict.__setitem__(node, key, copy.deepcopy(value, memo))
		return self._decoratenode(node)

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

	def _walk(self, filter, path, index, inmode, outmode):
		path.append(None)
		index.append(None)
		for (key, child) in self.iteritems():
			path[-1] = child
			index[-1] = key
			for result in child._walk(filter, path, index, inmode, outmode):
				yield result
		path.pop()
		index.pop()

	def present(self, presenter):
		presenter.presentAttrs(self)

	def checkvalid(self):
		# collect required attributes
		attrs = set()
		for (key, value) in self.iteralloweditems():
			if value.required:
				attrs.add(key)
		# Check each attribute and remove it from the list of required ones
		for (attrname, attrvalue) in self.iteritems():
			attrvalue.checkvalid()
			try:
				attrs.remove(attrname)
			except KeyError:
				pass
		# are there any required attributes remaining that haven't been specified? => warn about it
		if attrs:
			warnings.warn(RequiredAttrMissingWarning(self, list(attrs)))

	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		for (attrname, attrvalue) in self.iteritems():
			publisher.write(u" ")
			attrvalue.publish(publisher)

	def __unicode__(self):
		return u""

	@classmethod
	def isallowed(cls, name, xml=False):
		return name in cls._attrs[xml]

	def __getattribute__(self, name):
		sup = super(Attrs, self)
		if name in sup.__getattribute__("_attrs")[False]: # avoid recursion
			return self.__getitem__(name)
		else:
			return sup.__getattribute__(name)

	def __setattr__(self, name, value):
		sup = super(Attrs, self)
		if name in sup.__getattribute__("_attrs")[False]: # avoid recursion
			return self.__setitem__(name, value)
		else:
			return sup.__setattr__(name, value)

	def __delattr__(self, name):
		sup = super(Attrs, self)
		if name in sup.__getattribute__("_attrs")[False]: # avoid recursion
			return self.__detitem__(name)
		else:
			return sup.__delattr__(name)

	def __getitem__(self, name):
		if isinstance(name, list):
			node = self
			for subname in name:
				node = node[subname]
			return node
		else:
			return self.attr(name)

	def __setitem__(self, name, value):
		if isinstance(name, list):
			if not name:
				raise ValueError("can't replace self")
			node = self
			for subname in name[:-1]:
				node = node[subname]
			node[name[-1]] = value
		else:
			return self.set(name, value)

	def __delitem__(self, name):
		if isinstance(name, list):
			if not name:
				raise ValueError("can't delete self")
			node = self
			for subname in name[:-1]:
				node = node[subname]
			del node[name[-1]]
		else:
			attr = self.allowedattr(name)
			dict.__delitem__(self, attr.__name__)

	def has(self, name, xml=False):
		"""
		<par>return whether <self/> has an attribute named <arg>name</arg>. <arg>xml</arg>
		specifies whether <arg>name</arg> should be treated as an &xml; name
		(<lit><arg>xml</arg>==True</lit>) or a Python name (<lit><arg>xml</arg>==False</lit>).</par>
		"""
		try:
			attr = dict.__getitem__(self, self._allowedattrkey(name, xml=xml))
		except KeyError:
			return False
		return len(attr)>0

	def has_key(self, name, xml=False):
		return self.has(name, xml=xml)

	def get(self, name, default=None, xml=False):
		"""
		<par>works like the dictionary method <method>get</method>,
		it returns the attribute with the name <arg>name</arg>,
		or <arg>default</arg> if <self/> has no such attribute. <arg>xml</arg>
		specifies whether <arg>name</arg> should be treated as an &xml; name
		(<lit><arg>xml</arg>==True</lit>) or a Python name (<lit><arg>xml</arg>==False</lit>).</par>
		"""
		attr = self.attr(name, xml=xml)
		if not attr:
			attr = self.allowedattr(name, xml=xml)(default) # pack the attribute into an attribute object
		return attr

	def set(self, name, value=None, xml=False):
		"""
		<par>Set the attribute named <arg>name</arg> to the value <arg>value</arg>.
		<arg>xml</arg> specifies whether <arg>name</arg> should be treated as an
		&xml; name (<lit><arg>xml</arg>==True</lit>) or a Python name
		(<lit><arg>xml</arg>==False</lit>).</par>
		<par>The newly set attribute will be returned.</par>
		"""
		attr = self.allowedattr(name, xml=xml)(value)
		dict.__setitem__(self, self._allowedattrkey(name, xml=xml), attr) # put the attribute in our dict
		return attr

	def setdefault(self, name, default=None, xml=False):
		"""
		<par>works like the dictionary method <method>setdefault</method>,
		it returns the attribute with the name <arg>name</arg>.
		If <self/> has no such attribute, it will be set to <arg>default</arg>
		and <arg>default</arg> will be returned as the new attribute value. <arg>xml</arg>
		specifies whether <arg>name</arg> should be treated as an &xml; name
		(<lit><arg>xml</arg>==True</lit>) or a Python name (<lit><arg>xml</arg>==False</lit>).</par>
		"""
		attr = self.attr(name, xml=xml)
		if not attr:
			attr = self.allowedattr(name, xml=xml)(default) # pack the attribute into an attribute object
			dict.__setitem__(self, self._allowedattrkey(name, xml=xml), attr)
		return attr

	def update(self, *args, **kwargs):
		"""
		Copies attributes over from all mappings in <arg>args</arg> and from <arg>kwargs</arg>.
		"""
		for mapping in args + (kwargs,):
			if mapping is not None:
				if isinstance(mapping, Namespace.Attrs):
					for (attrname, attrvalue) in mapping._iterallitems():
						self[(attrvalue.__ns__, attrname)] = attrvalue
				else:
					try:
						for (attrname, attrvalue) in mapping._iterallitems():
							self[attrname] = attrvalue
					except AttributeError:
						for (attrname, attrvalue) in mapping.iteritems():
							self[attrname] = attrvalue

	def updateexisting(self, *args, **kwargs):
		"""
		Copies attributes over from all mappings in <arg>args</arg> and from <arg>kwargs</arg>,
		but only if they exist in <self/>.
		"""
		for mapping in args + (kwargs,):
			if mapping is not None:
				if isinstance(mapping, Namespace.Attrs):
					for (attrname, attrvalue) in mapping._iterallitems():
						if (attrvalue.__ns__, attrname) in self:
							self[(attrvalue.__ns__, attrname)] = attrvalue
				else:
					try:
						for (attrname, attrvalue) in mapping._iterallitems():
							if attrname in self:
								self[attrname] = attrvalue
					except AttributeError:
						for (attrname, attrvalue) in mapping.iteritems():
							if attrname in self:
								self[attrname] = attrvalue

	def updatenew(self, *args, **kwargs):
		"""
		Copies attributes over from all mappings in <arg>args</arg> and from <arg>kwargs</arg>,
		but only if they don't exist in <self/>.
		"""
		args = list(args)
		args.reverse()
		for mapping in [kwargs] + args: # Iterate in reverse order, so the last entry wins
			if mapping is not None:
				if isinstance(mapping, Namespace.Attrs):
					for (attrname, attrvalue) in mapping._iterallitems():
						if (attrvalue.__ns__, attrname) not in self:
							self[(attrvalue.__ns__, attrname)] = attrvalue
				else:
					try:
						for (attrname, attrvalue) in mapping._iterallitems():
							if attrname not in self:
								self[attrname] = attrvalue
					except AttributeError:
						for (attrname, attrvalue) in mapping.iteritems():
							if attrname not in self:
								self[attrname] = attrvalue

	def copydefaults(self, fromMapping):
		warnings.warn(DeprecationWarning("Attrs.copydefaults() is deprecated, use Attrs.updateexisting() instead"))
		return self.updateexisting(fromMapping)

	@classmethod
	def iterallowedkeys(cls, xml=False):
		"""
		<par>return an iterator for iterating through the names of allowed attributes. <arg>xml</arg>
		specifies whether &xml; names (<lit><arg>xml</arg>==True</lit>) or Python names
		(<lit><arg>xml</arg>==False</lit>) should be returned.</par>
		"""
		return cls._attrs[xml].iterkeys()

	@classmethod
	def allowedkeys(cls, xml=False):
		"""
		<par>return a list of allowed keys (i.e. attribute names)</par>
		"""
		return cls._attrs[xml].keys()

	@classmethod
	def iterallowedvalues(cls):
		return cls._attrs[False].itervalues()

	@classmethod
	def allowedvalues(cls):
		"""
		<par>return a list of values for the allowed values.</par>
		"""
		return cls._attrs[False].values()

	@classmethod
	def iteralloweditems(cls, xml=False):
		return cls._attrs[xml].iteritems()

	@classmethod
	def alloweditems(cls, xml=False):
		return cls._attrs[xml].items()

	@classmethod
	def _allowedattrkey(cls, name, xml=False):
		try:
			return cls._attrs[xml][name].__name__
		except KeyError:
			raise IllegalAttrError(cls, name, xml=xml)

	@classmethod
	def allowedattr(cls, name, xml=False):
		try:
			return cls._attrs[xml][name]
		except KeyError:
			raise IllegalAttrError(cls, name, xml=xml)

	def __iter__(self):
		return self.iterkeys()

	def __len__(self):
		return len(self.keys())

	def __contains__(self, key):
		return self.has(key)

	def iterkeys(self, xml=False):
		found = {}
		for (key, value) in dict.iteritems(self):
			if value:
				if isinstance(key, tuple):
					if xml:
						yield (value.__ns__, value.xmlname)
					else:
						yield (value.__ns__, value.__class__.__name__)
				else:
					if xml:
						yield value.xmlname
					else:
						yield value.__class__.__name__

	def keys(self, xml=False):
		return list(self.iterkeys(xml=xml))

	def itervalues(self):
		for value in dict.itervalues(self):
			if value:
				yield value

	def values(self):
		return list(self.itervalues())

	def iteritems(self, xml=False):
		for (key, value) in dict.iteritems(self):
			if value:
				if isinstance(key, tuple):
					if xml:
						yield ((value.__ns__, value.xmlname), value)
					else:
						yield ((value.__ns__, value.__class__.__name__), value)
				else:
					if xml:
						yield (value.xmlname, value)
					else:
						yield (value.__class__.__name__, value)

	def items(self, xml=False):
		return list(self.iteritems(xml=xml))

	def _iterallitems(self):
		"""
		Iterate all items, even the unset ones
		"""
		return dict.iteritems(self)

	def attr(self, name, xml=False):
		key = self._allowedattrkey(name, xml=xml)
		try:
			attr = dict.__getitem__(self, key)
		except KeyError: # if the attribute is not there generate a new empty one
			attr = self.allowedattr(name, xml=xml)()
			dict.__setitem__(self, key, attr)
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
		if xml:
			return self.filtered(lambda n: n.xmlname in names)
		else:
			return self.filtered(lambda n: n.__class__.__name__ in names)

	def without(self, names=[], xml=False):
		"""
		<par>Return a copy of <self/> where all the attributes in <arg>names</arg> are
		removed.</par>
		"""
		if xml:
			return self.filtered(lambda n: n.xmlname not in names)
		else:
			return self.filtered(lambda n: n.__class__.__name__ not in names)

_Attrs = Attrs


class _Element_Meta(Node.__metaclass__):
	def __new__(cls, name, bases, dict):
		if "model" in dict and isinstance(dict["model"], bool):
			from ll.xist import sims
			if dict["model"]:
				dict["model"] = sims.Any()
			else:
				dict["model"] = sims.Empty()
		if "empty" in dict:
			warnings.warn(PendingDeprecationWarning("empty is deprecated, use model (and ll.xist.sims) instead"), stacklevel=2)
			from ll.xist import sims
			if dict["empty"]:
				model = sims.Empty()
			else:
				model = sims.Any()
			del dict["empty"]
			dict["model"] = model
		
		return super(_Element_Meta, cls).__new__(cls, name, bases, dict)

	def __repr__(self):
		return "<element class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))


class Element(Node):
	"""
	<par>This class represents &xml;/&xist; elements. All elements implemented
	by the user must be derived from this class.</par>

	<par>If you not only want to construct a tree via a Python script (by
	directly instantiating these classes), but to read an &xml; file you must
	register the element class with the parser, this can be done by deriving
	<pyref class="Namespace"><class>Namespace</class></pyref> classes.</par>

	<par>Every element class should have two class variables:</par>
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
	</dlist>
	"""
	__metaclass__ = _Element_Meta

	model = None
	register = None

	class Attrs(Attrs):
		"""
		Attribute mapping for elements. This version supports global attributes.
		"""
		@classmethod
		def _allowedattrkey(cls, name, xml=False):
			if isinstance(name, tuple):
				return (name[0], name[0].Attrs._allowedattrkey(name[1], xml=xml)) # ask namespace about global attribute
			try:
				return cls._attrs[xml][name].__name__
			except KeyError:
				raise IllegalAttrError(cls, name, xml=xml)

		@classmethod
		def allowedattr(cls, name, xml=False):
			if isinstance(name, tuple):
				return name[0].Attrs.allowedattr(name[1], xml=xml) # ask namespace about global attribute
			else:
				# FIXME: reimplemented here, because super does not work
				try:
					return cls._attrs[xml][name]
				except KeyError:
					raise IllegalAttrError(cls, name, xml=xml)

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
				if xml:
					name = node.__name__
				else:
					name = node.xmlname
				if node.__ns__ is None:
					return name in names
				else:
					if keepglobals:
						return True
					for ns in namespaces:
						if issubclass(node.__ns__, ns):
							return True
					for testname in names:
						if isinstance(testname, tuple) and issubclass(node.__ns__, testname[0]) and name==testname[1]:
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
				if xml:
					name = node.xmlname
				else:
					name = node.__class__.__name__
				if node.__ns__ is None:
					return name not in names
				else:
					if not keepglobals:
						return False
					for ns in namespaces:
						if issubclass(node.__ns__, ns):
							return False
					for testname in names:
						if isinstance(testname, tuple) and issubclass(node.__ns__, testname[0]) and name==testname[1]:
							return False
					return True

			return self.filtered(keep)

	# XPython support
	def __enter__(self):
		append(self)

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
		for (attrname, attrvalue) in attrs.iteritems():
			self.attrs[attrname] = attrvalue

	def __getstate__(self):
		attrs = {}
		for (key, value) in self.attrs.iteritems():
			if isinstance(key, tuple):
				# Pickle namespace module name instead
				# (for the the namespace must be a module, i.e. generated via makemod())
				if not hasattr(key[0], "__file__"):
					raise cPickle.PicklingError("can't pickle namespace %r: must be module" % key[0])
				key = (key[0].__name__, key[1])
			attrs[key] = Frag(value)
		return (self.content, attrs)

	def __setstate__(self, (content, attrs)):
		self.content = content
		self.attrs = self.Attrs()
		for (key, value) in attrs.iteritems():
			if isinstance(key, tuple):
				# Import namespace module
				__import__(key[0])
				key = (sys.modules[key[0]], key[1])
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
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strBracketOpen())
		cls._strbase(presenters.strElementName, s, fullname=fullname, xml=xml)
		if decorate:
			if cls.model is not None and cls.model.empty:
				s.append(presenters.strSlash())
			s.append(presenters.strBracketClose())
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
		node.content = self.content.clone() # this is faster than passing it in the constructor (no ToNode call)
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
			size = url.openread().imagesize
		except IOError, exc:
			warnings.warn(FileNotFoundWarning("can't read image", url, exc))
		else:
			for attr in (heightattr, widthattr):
				if attr is not None: # do something to the width/height
					if not self.attrs.has(attr):
						self[attr] = size[attr==heightattr]

	def present(self, presenter):
		presenter.presentElement(self)

	def _publishfull(self, publisher):
		"""
		Does the full publication of the element. If you need full elements
		inside attributes (e.g. for &jsp; tag libraries), you can overwrite
		<method>publish</method> and simply call this method.
		"""
		publisher.write(u"<")
		self._publishname(publisher)
		# we're the first element to be published, so we have to create the xmlns attributes
		if publisher.publishxmlns:
			for (ns, prefix) in publisher.publishxmlns.iteritems():
				publisher.write(u" xmlns")
				if prefix is not None:
					publisher.write(u":")
					publisher.write(prefix)
				publisher.write(u"=\"")
				publisher.write(ns.xmlurl)
				publisher.write(u"\"")
			# reset the note, so the next element won't create the attributes again
			publisher.publishxmlns = None
		self.attrs.publish(publisher)
		if len(self):
			publisher.write(u">")
			self.content.publish(publisher)
			publisher.write(u"</")
			self._publishname(publisher)
			publisher.write(u">")
		else:
			if publisher.xhtml in (0, 1):
				if self.model is not None and self.model.empty:
					if publisher.xhtml==1:
						publisher.write(u" /")
					publisher.write(u">")
				else:
					publisher.write(u"></")
					self._publishname(publisher)
					publisher.write(u">")
			elif publisher.xhtml == 2:
				publisher.write(u"/>")

	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		if publisher.inattr:
			# publish the content only when we are inside an attribute. This works much like using the plain string value,
			# but even works with processing instructions, or what the abbreviation entities return
			self.content.publish(publisher)
		else:
			self._publishfull(publisher)

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
		elif isinstance(index, type) and issubclass(index, Node):
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

	def hasAttr(self, attrname, xml=False):
		warnings.warn(DeprecationWarning("foo.hasAttr() is deprecated, use foo.attrs.has() instead"))
		return self.attrs.has(attrname, xml=xml)

	def hasattr(self, attrname, xml=False):
		warnings.warn(DeprecationWarning("foo.hasattr() is deprecated, use foo.attrs.has() instead"))
		return self.attrs.has(attrname, xml=xml)

	@classmethod
	def isallowedattr(cls, attrname):
		warnings.warn(DeprecationWarning("foo.isallowedattr() is deprecated, use foo.Attrs.isallowed() instead"))
		return cls.Attrs.isallowed(attrname)

	def getAttr(self, attrname, default=None):
		warnings.warn(DeprecationWarning("foo.getAttr() is deprecated, use foo.attrs.get() instead"), stacklevel=2)
		return self.getattr(attrname, default)

	def getattr(self, attrname, default=None):
		warnings.warn(DeprecationWarning("foo.getattr() is deprecated, use foo.attrs.get() instead"), stacklevel=2)
		return self.attrs.get(attrname, default)

	def setDefaultAttr(self, attrname, default=None):
		warnings.warn(DeprecationWarning("foo.setDefaultAttr() is deprecated, use foo.attrs.setdefault() instead"))
		return self.setdefault(attrname, default=default)

	def setdefaultattr(self, attrname, default=None):
		warnings.warn(DeprecationWarning("foo.setDefaultAttr() is deprecated, use foo.attrs.setdefault() instead"))
		return self.attrs.setdefault(attrname, default)

	def attrkeys(self, xml=False):
		warnings.warn(DeprecationWarning("foo.attrkeys() is deprecated, use foo.attrs.keys() instead"))
		return self.attrs.keys(xml=xml)

	def attrvalues(self):
		warnings.warn(DeprecationWarning("foo.attrvalues() is deprecated, use foo.attrs.values() instead"))
		return self.attrs.values()

	def attritems(self, xml=False):
		warnings.warn(DeprecationWarning("foo.attritems() is deprecated, use foo.attrs.items() instead"))
		return self.attrs.items(xml=xml)

	def iterattrkeys(self, xml=False):
		warnings.warn(DeprecationWarning("foo.iterattrkeys() is deprecated, use foo.attrs.iterkeys() instead"))
		return self.attrs.iterkeys(xml=xml)

	def iterattrvalues(self):
		warnings.warn(DeprecationWarning("foo.iterattrvalues() is deprecated, use foo.attrs.itervalues() instead"))
		return self.attrs.itervalues()

	def iterattritems(self, xml=False):
		warnings.warn(DeprecationWarning("foo.iterattritems() is deprecated, use foo.attrs.iteritems() instead"))
		return self.attrs.iteritems(xml=xml)

	@classmethod
	def allowedattrkeys(cls, xml=False):
		warnings.warn(DeprecationWarning("foo.allowedattrkeys() is deprecated, use foo.attrs.allowedkeys() instead"))
		return cls.Attrs.allowedkeys(xml=xml)

	@classmethod
	def allowedattrvalues(cls):
		warnings.warn(DeprecationWarning("foo.allowedattrvalues() is deprecated, use foo.attrs.allowedvalues() instead"))
		return cls.Attrs.allowedvalues()

	@classmethod
	def allowedattritems(cls, xml=False):
		warnings.warn(DeprecationWarning("foo.allowedattritems() is deprecated, use foo.attrs.alloweditems() instead"))
		return cls.Attrs.alloweditems(xml=xml)

	@classmethod
	def iterallowedattrkeys(cls, xml=False):
		warnings.warn(DeprecationWarning("foo.iterallowedattrkeys() is deprecated, use foo.attrs.iterattrkeys() instead"))
		return cls.Attrs.iterallowedkeys(xml=xml)

	@classmethod
	def iterallowedattrvalues(cls):
		warnings.warn(DeprecationWarning("foo.iterallowedattrvalues() is deprecated, use foo.attrs.iterattrvalues() instead"))
		return cls.Attrs.iterallowedvalues()

	@classmethod
	def iterallowedattritems(cls, xml=False):
		warnings.warn(DeprecationWarning("foo.iterallowedattritems() is deprecated, use foo.attrs.iterattritems() instead"))
		return cls.Attrs.iteralloweditems(xml=xml)

	def __len__(self):
		"""
		return the number of children.
		"""
		return len(self.content)

	def compact(self):
		node = self.__class__()
		node.content = self.content.compact()
		node.attrs = self.attrs.compact()
		return self._decoratenode(node)

	def _walk(self, filter, path, index, inmode, outmode):
		if callable(filter):
			if inmode is walknode:
				found = filter(self)
			elif inmode is walkpath:
				found = filter(path)
			elif inmode is walkindex:
				found = filter(index)
			elif inmode is walkrootindex:
				found = filter(path[0], index)
			else:
				raise ValueError("unknown inmode %r" % inmode)
		else:
			found = filter

		for option in found:
			if option is entercontent:
				for object in self.content._walk(filter, path, index, inmode, outmode):
					yield object
			elif option is enterattrs:
				for object in self.attrs._walk(filter, path, index, inmode, outmode):
					yield object
			elif option:
				if outmode is walknode:
					yield self
				elif outmode is walkpath:
					yield path[:]
				elif outmode is walkindex:
					yield index[:]
				elif outmode is walkrootindex:
					yield (path[0], index[:])
				else:
					raise ValueError("unknown outmode %r" % outmode)

	def copyDefaultAttrs(self, fromMapping):
		"""
		<par>Sets attributes that are not set in <self/> to the default
		values taken from the <arg>fromMapping</arg> mapping.</par>

		<par>Note that boolean attributes may savely be set to e.g. <lit>True</lit>,
		as only the fact that a boolean attribute exists matters.</par>
		"""

		warnings.warn(DeprecationWarning("foo.copyDefaultAttrs() is deprecated, use foo.attrs.updateexisting() instead"))
		self.attrs.updateexisting(fromMapping)

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

	def sorted(self, compare=lambda node1, node2: cmp(unicode(node1), unicode(node2))):
		"""
		returns a sorted version of <self/>. <arg>compare</arg> is a comparison
		function. If <arg>compare</arg> is omitted, the character content will
		be compared.
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

	def mapped(self, function, converter):
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


class _Entity_Meta(Node.__metaclass__):
	def __repr__(self):
		return "<entity class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))


class Entity(Node):
	"""
	<par>Class for entities. Derive your own entities from it and overwrite
	<pyref class="Node" method="convert"><method>convert</method></pyref>.</par>
	"""
	__metaclass__ = _Entity_Meta

	register = None

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strAmp())
		cls._strbase(presenters.strEntityName, s, fullname=fullname, xml=xml)
		if decorate:
			s.append(presenters.strSemi())
		return s

	def __eq__(self, other):
		return self.__class__ is other.__class__

	def compact(self):
		return self

	def present(self, presenter):
		presenter.presentEntity(self)

	def publish(self, publisher):
		publisher.write(u"&")
		publisher.write(self.xmlname)
		publisher.write(u";")


class _CharRef_Meta(Entity.__metaclass__): # don't subclass Text.__metaclass__, as this is redundant
	def __repr__(self):
		return "<charref class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))


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

	def present(self, presenter):
		presenter.presentEntity(self)

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


import presenters, publishers, cssparsers, converters, utils, helpers

###
### Classes for namespace handling
###

class NSPool(dict):
	"""
	<par>A pool of namespaces identified by their name.</par>
	<par>A pool may only have one namespace class for one namespace name.</par>
	"""
	def __init__(self, *args):
		dict.__init__(self, ((arg.xmlurl, arg) for arg in args))

	def add(self, ns):
		"""
		Add the namespace <arg>ns</arg> to the pool. Any previous namespace with
		this name will be replaced.
		"""
		self[ns.xmlurl] = ns

	def remove(self, ns):
		"""
		Remove the namespace <arg>ns</arg> from the pool. A different namespace
		with the same name will be removed too. If a namespace with this name
		is not in the pool, nothing happens.
		"""
		try:
			del self[ns.xmlurl]
		except KeyError:
			pass

defaultnspool = NSPool()


class Prefixes(dict):
	"""
	<par>Specifies a mapping between namespace prefixes and namespaces both
	for parsing and publishing. Each namespace can have multiple prefixes, and
	every prefix can be used by multiple namespaces.</par>
	"""
	NOPREFIX = 0
	USEPREFIX = 1
	DECLAREANDUSEPREFIX = 2

	# Warning classes
	IllegalElementWarning = IllegalElementParseWarning
	IllegalProcInstWarning = IllegalProcInstParseWarning
	AmbiguousProcInstWarning = AmbiguousProcInstParseWarning
	IllegalEntityWarning = IllegalEntityParseWarning
	AmbiguousEntityWarning = AmbiguousEntityParseWarning
	IllegalCharRefWarning = IllegalCharRefParseWarning
	AmbiguousCharRefWarning = AmbiguousCharRefParseWarning
	IllegalAttrWarning = IllegalAttrParseWarning

	def __init__(self, nswithoutprefix=None, **nswithprefix):
		dict.__init__(self)
		if nswithoutprefix is not None:
			self[None] = nswithoutprefix
		for (prefix, ns) in nswithprefix.iteritems():
			self[prefix] = ns

	def __repr__(self):
		return "<%s.%s %s at 0x%x>" % (self.__module__, self.__class__.__name__, " ".join("%s=%r" % (key or "None", value) for (key, value) in self.iteritems()), id(self))

	def __getitem__(self, prefix):
		return self.setdefault(prefix, [])

	def __setitem__(self, prefix, namespaces):
		if isinstance(namespaces, type) and issubclass(namespaces, Namespace):
			namespaces = [namespaces]
		dict.__setitem__(self, prefix, namespaces)

	def ns4prefix(self, prefix):
		"""
		<par>Return the namespace list for the prefix <arg>prefix</arg>.</par>
		"""
		return self[prefix]

	def prefix4ns(self, ns):
		"""
		<par>Return the prefixes for the namespace <arg>ns</arg>.</par>
		"""
		prefixes = []
		for (prefix, namespaces) in self.iteritems():
			for ourns in namespaces:
				if issubclass(ns, ourns):
					prefixes.append(prefix)
		if prefixes:
			return prefixes
		else:
			return [ns.xmlname]

	def __splitqname(self, qname):
		"""
		Split a qualified name into a (prefix, local name) pair.
		"""
		pos = qname.find(":")
		if pos>=0:
			return (qname[:pos], qname[pos+1:])
		else:
			return (None, qname) # no namespace specified

	def element(self, qname):
		"""
		<par>Return the element class for the name
		<arg>qname</arg> (which might include a prefix).</par>
		<par>If the element can't be found issue a warning (which
		defaults to an exception) and return <lit>None</lit>.
		"""
		(prefix, name) = self.__splitqname(qname)
		for ns in self[prefix]:
			try:
				element = ns.element(name, xml=True)
				if element.register:
					return element
			except LookupError: # no element in this namespace with this name
				pass
		warnings.warn(self.IllegalElementWarning(qname, xml=True)) # elements with this name couldn't be found
		return None

	def procinst(self, name):
		"""
		<par>Return the processing instruction class for the name <arg>name</arg>.</par>
		<par>If the processing instruction can't be found or is ambigous
		issue a warning (which defaults to an exception) and return <lit>None</lit>.
		"""
		candidates = set()
		for nss in self.itervalues():
			for ns in nss:
				try:
					procinst = ns.procinst(name, xml=True)
				except LookupError: # no processing instruction in this namespace with this name
					pass
				else:
					if procinst.register:
						candidates.add(procinst)
		if len(candidates)==1:
			return candidates.pop()
		elif len(candidates)==0:
			warnings.warn(self.IllegalProcInstWarning(name, xml=True)) # processing instructions with this name couldn't be found
		else:
			warnings.warn(self.AmbiguousProcInstWarning(name, xml=True)) # there was more than one processing instructions with this name
		return None

	def entity(self, name):
		"""
		<par>Return the entity or charref class for the name <arg>name</arg>.</par>
		<par>If the entity can't be found or is ambigous issue a warning
		(which defaults to an exception) and return <lit>None</lit>.
		"""
		candidates = set()
		for nss in self.itervalues():
			for ns in nss:
				try:
					entity = ns.entity(name, xml=True)
				except LookupError: # no entity in this namespace with this name
					pass
				else:
					if entity.register:
						candidates.add(entity)
		if len(candidates)==1:
			return candidates.pop()
		elif len(candidates)==0:
			warnings.warn(self.IllegalEntityWarning(name, xml=True)) # entities with this name couldn't be found
		else:
			warnings.warn(self.AmbiguousEntityWarning(name, xml=True)) # there was more than one entity with this name
		return None

	def charref(self, name):
		"""
		<par>Return the first charref class for the name or codepoint <arg>name</arg>.</par>
		<par>If the character reference can't be found or is ambigous issue a warning
		(which defaults to an exception) and return <lit>None</lit>.
		"""
		candidates = set()
		for nss in self.itervalues():
			for ns in nss:
				try:
					charref = ns.charref(name, xml=True)
				except LookupError: # no entity in this namespace with this name
					pass
				else:
					if charref.register:
						candidates.add(charref)
		if len(candidates)==1:
			return candidates.pop()
		elif len(candidates)==0:
			warnings.warn(self.IllegalCharRefWarning(name, xml=True)) # character references with this name/codepoint couldn't be found
		else:
			warnings.warn(self.AmbiguousCharRefWarning(name, xml=True)) # there was more than one character reference with this name
		return None

	def attrnamefromqname(self, element, qname):
		"""
		<par>Return the Python name for an attribute for the qualified
		&xml; name <arg>qname</arg> (which might include a prefix, in which case
		a tuple with the namespace class and the name will be returned, otherwise
		it will be an attribute from the element <arg>element</arg>, which must
		be a subclass of <pyref class="Element"><class>Element</class></pyref>).</par>
		<par>If the attribute can't be found issue a warning
		(which defaults to an exception) and return <lit>None</lit>.
		"""
		qname = self.__splitqname(qname)
		if qname[0] is None:
			try:
				return element.Attrs.allowedattr(qname[1], xml=True).__name__
			except IllegalAttrError:
				warnings.warn(self.IllegalAttrWarning(element.attrs, qname[1], xml=True))
		else:
			for ns in self[qname[0]]:
				try:
					attr = ns.Attrs.allowedattr(qname[1], xml=True)
					if attr.register:
						return (ns, attr.__name__)
				except IllegalAttrError: # no attribute in this namespace with this name
					pass
			warnings.warn(self.IllegalAttrWarning(None, qname, xml=True))
		return None

	def clone(self):
		other = self.__class__()
		for (key, value) in self.iteritems():
			other[key] = value[:]
		return other


class OldPrefixes(Prefixes):
	"""
	<par>Prefix mapping that is compatible to the mapping used
	prior to &xist; version 2.0.</par>
	"""
	def __init__(self):
		super(OldPrefixes, self).__init__()
		for ns in Namespace.all:
			if ns.xmlurl == "http://www.w3.org/XML/1998/namespace":
				self["xml"].append(ns)
				self[None].append(ns)
			else:
				self[ns.xmlname].append(ns)
				self[None].append(ns)


class DefaultPrefixes(Prefixes):
	"""
	<par>Prefix mapping that maps all defined namespace
	to their default prefix, except for one which is mapped
	to <lit>None</lit>.</par>
	"""
	def __init__(self, default=None):
		super(DefaultPrefixes, self).__init__()
		for ns in Namespace.all:
			if ns is default:
				self[None] = ns
			else:
				self[ns.xmlname] = ns


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
		from ll.xist.ns import html, chars, abbr, doc, specials
		self[None] = [doc, specials, html, chars, abbr]

defaultPrefixes = Prefixes()


###
### Namespaces
###

class _Namespace_Meta(Base.__metaclass__, ll.Namespace.__metaclass__):
	def __new__(cls, name, bases, dict):
		dict["xmlname"] = dict.get("xmlname", name).split(".")[-1]
		if "xmlurl" in dict:
			xmlurl = dict["xmlurl"]
			if xmlurl is not None:
				xmlurl = unicode(xmlurl)
			dict["xmlurl"] = xmlurl
		# Convert functions to staticmethods as Namespaces won't be instantiated anyway
		# If you need a classmethod simply define one
		for (key, value) in dict.iteritems():
			if isinstance(value, new.function):
				dict[key] = staticmethod(value)
		# automatically inherit all element, procinst, entity and Attrs classes, that aren't overwritten.
		for base in bases:
			for attrname in dir(base):
				attr = getattr(base, attrname)
				if isinstance(attr, type) and issubclass(attr, (Element, ProcInst, Entity, Attrs)) and attrname not in dict:
					classdict = {"__module__": dict["__module__"]}
					if attr.__name__ != attr.xmlname:
						classdict["xmlname"] = attr.xmlname
					classdict["__outerclass__"] = 42
					dict[attrname] = attr.__class__(attr.__name__, (attr, ), classdict)
		dict["_cache"] = None
		self = super(_Namespace_Meta, cls).__new__(cls, name, bases, dict)
		self.__originalname = name # preserves the name even after makemod() (used by __repr__)
		for (key, value) in self.__dict__.iteritems():
			if isinstance(value, type):
				if getattr(value, "__outerclass__", None) == 42:
					value.__outerclass__ = self
				if issubclass(value, (Element, ProcInst, Entity)):
					value.__ns__ = self
		for attr in self.Attrs.iterallowedvalues():
			attr.__ns__ = self
		if self.xmlurl is not None:
			name = self.xmlname
			self.nsbyname.setdefault(name, []).insert(0, self)
			self.nsbyurl.setdefault(self.xmlurl, []).insert(0, self)
			self.all.append(self)
			defaultPrefixes[None].insert(0, self)
			defaultPrefixes[name].insert(0, self)
			defaultnspool.add(self)
		return self

	def __eq__(self, other):
		if isinstance(other, type) and issubclass(other, Namespace):
			return self.xmlname==other.xmlname and self.xmlurl==other.xmlurl
		return False

	def __ne__(self, other):
		return not self==other

	def __hash__(self):
		return hash(self.xmlname) ^ hash(self.xmlurl)

	def __repr__(self):
		counts = []

		elementkeys = self.elementkeys()
		if elementkeys:
			counts.append("%d elements" % len(elementkeys))

		procinstkeys = self.procinstkeys()
		if procinstkeys:
			counts.append("%d procinsts" % len(procinstkeys))

		entitykeys = self.entitykeys()
		charrefkeys = self.charrefkeys()
		count = len(entitykeys)-len(charrefkeys)
		if count:
			counts.append("%d entities" % count)

		if len(charrefkeys):
			counts.append("%d charrefs" % len(charrefkeys))

		allowedattrs = self.Attrs.allowedkeys()
		if len(allowedattrs):
			counts.append("%d attrs" % len(allowedattrs))

		if counts:
			counts = " with " + ", ".join(counts)
		else:
			counts = ""

		if "__file__" in self.__dict__: # no inheritance
			fromfile = " from %r" % self.__file__
		else:
			fromfile = ""
		return "<namespace %s:%s name=%r url=%r%s%s at 0x%x>" % (self.__module__, self.__originalname, self.xmlname, self.xmlurl, counts, fromfile, id(self))

	def __delattr__(self, key):
		value = self.__dict__.get(key, None) # no inheritance
		if isinstance(value, type) and issubclass(value, (Element, ProcInst, CharRef)):
			self._cache = None
			value.__ns__ = None
		return super(_Namespace_Meta, self).__delattr__(key)

	def __setattr__(self, key, value):
		# Remove old attribute
		oldvalue = self.__dict__.get(key, None) # no inheritance
		if isinstance(oldvalue, type) and issubclass(oldvalue, (Element, ProcInst, Entity)):
			if oldvalue.__ns__ is not None:
				oldvalue.__ns__._cache = None
				oldvalue.__ns__ = None
		# Set new attribute
		if isinstance(value, type) and issubclass(value, (Element, ProcInst, Entity)):
			if value.__ns__ is not None:
				value.__ns__._cache = None
				value.__ns__ = None
			self._cache = None
			value.__ns__ = self
		return super(_Namespace_Meta, self).__setattr__(key, value)


class Namespace(Base, ll.Namespace):
	"""
	<par>An &xml; namespace.</par>
	
	<par>Classes for elements, entities and processing instructions can be
	defined as nested classes inside subclasses of <class>Namespace</class>.
	This class will never be instantiated.</par>
	"""
	__metaclass__ = _Namespace_Meta

	xmlurl = None

	nsbyname = {}
	nsbyurl = {}
	all = []

	class Attrs(_Attrs):
		"""
		Attribute mapping for namespaces. Derived namespace will define their
		global attributes as nested classes.
		"""
		pass

	class Context(_Context):
		pass

	@classmethod
	def _getcache(cls):
		if cls._cache is not None:
			return cls._cache
		c = (
			({}, {}), # cache for elements (by Python name and by XML name)
			({}, {}), # cache for processing instructions (by Python name and by XML name)
			({}, {}), # cache for entities (by Python name and by XML name)
			({}, {}, {}), # cache for character references (by Python name, by XML name and by codepoint)
		)

		for key in dir(cls):
			value = getattr(cls, key)
			if isinstance(value, type):
				if issubclass(value, Element):
					c[0][False][value.__name__] = value
					c[0][True][value.xmlname] = value
				elif issubclass(value, ProcInst):
					c[1][False][value.__name__] = value
					c[1][True][value.xmlname] = value
				elif issubclass(value, Entity):
					c[2][False][value.__name__] = value
					c[2][True][value.xmlname] = value
					if issubclass(value, CharRef):
						c[3][False][value.__name__] = value
						c[3][True][value.xmlname] = value
						c[3][2].setdefault(value.codepoint, []).append(value)
		cls._cache = c
		return c

	@classmethod
	def iterelementkeys(cls, xml=False):
		"""
		Return an iterator for iterating over the names of all
		<pyref class="Element">element</pyref> classes in <cls/>. <arg>xml</arg>
		specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[0][xml].iterkeys()

	@classmethod
	def elementkeys(cls, xml=False):
		"""
		Return a list of the names of all <pyref class="Element">element</pyref>
		classes in <cls/>. <arg>xml</arg> specifies whether Python or &xml; names
		should be returned.
		"""
		return cls._getcache()[0][xml].keys()

	@classmethod
	def iterelementvalues(cls):
		"""
		Return an iterator for iterating over all
		<pyref class="Element">element</pyref> classes in <cls/>.
		"""
		return cls._getcache()[0][False].itervalues()

	@classmethod
	def elementvalues(cls):
		"""
		Return a list of all <pyref class="Element">element</pyref> classes in
		<cls/>.
		"""
		return cls._getcache()[0][False].values()

	@classmethod
	def iterelementitems(cls, xml=False):
		"""
		Return an iterator for iterating over the (name, class) items of all
		<pyref class="Element">element</pyref> classes in <cls/>. <arg>xml</arg>
		specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[0][xml].iteritems()

	@classmethod
	def elementitems(cls, xml=False):
		"""
		Return a list of all (name, class) items of all
		<pyref class="Element">element</pyref> classes in <cls/>. <arg>xml</arg>
		specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[0][xml].items()

	@classmethod
	def element(cls, name, xml=False):
		"""
		Return the <pyref class="Element">element</pyref> class with the name
		<arg>name</arg>. <arg>xml</arg> specifies whether <arg>name</arg> should
		be treated as a Python or &xml; name. If an element class with this name
		doesn't exist an <class>IllegalElementError</class> is raised.
		"""
		try:
			return cls._getcache()[0][xml][name]
		except KeyError:
			raise IllegalElementError(name, xml=xml)

	@classmethod
	def iterprocinstkeys(cls, xml=False):
		"""
		Return an iterator for iterating over the names of all
		<pyref class="ProcInst">processing instruction</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[1][xml].iterkeys()

	@classmethod
	def procinstkeys(cls, xml=False):
		"""
		Return a list of the names of all
		<pyref class="ProcInst">processing instruction</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[1][xml].keys()

	@classmethod
	def iterprocinstvalues(cls):
		"""
		Return an iterator for iterating over all
		<pyref class="ProcInst">processing instruction</pyref> classes in <cls/>.
		"""
		return cls._getcache()[1][False].itervalues()

	@classmethod
	def procinstvalues(cls):
		"""
		Return a list of all <pyref class="ProcInst">processing instruction</pyref>
		classes in <cls/>.
		"""
		return cls._getcache()[1][False].values()

	@classmethod
	def iterprocinstitems(cls, xml=False):
		"""
		Return an iterator for iterating over the (name, class) items of all
		<pyref class="ProcInst">processing instruction</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[1][xml].iteritems()

	@classmethod
	def procinstitems(cls, xml=False):
		"""
		Return a list of all (name, class) items of all
		<pyref class="ProcInst">processing instruction</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[1][xml].items()

	@classmethod
	def procinst(cls, name, xml=False):
		"""
		Return the <pyref class="ProcInst">processing instruction</pyref> class
		with the name <arg>name</arg>. <arg>xml</arg> specifies whether
		<arg>name</arg> should be treated as a Python or &xml; name. If a
		processing instruction class with this name doesn't exist an
		<class>IllegalProcInstError</class> is raised.
		"""
		try:
			return cls._getcache()[1][xml][name]
		except KeyError:
			raise IllegalProcInstError(name, xml=xml)

	@classmethod
	def iterentitykeys(cls, xml=False):
		"""
		Return an iterator for iterating over the names of all
		<pyref class="Entity">entity</pyref> and
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[2][xml].iterkeys()

	@classmethod
	def entitykeys(cls, xml=False):
		"""
		Return a list of the names of all <pyref class="Entity">entity</pyref> and
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[2][xml].keys()

	@classmethod
	def iterentityvalues(cls):
		"""
		Return an iterator for iterating over all <pyref class="Entity">entity</pyref>
		and <pyref class="CharRef">character reference</pyref> classes in <cls/>.
		"""
		return cls._getcache()[2][False].itervalues()

	@classmethod
	def entityvalues(cls):
		"""
		Return a list of all <pyref class="Entity">entity</pyref> and
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		"""
		return cls._getcache()[2][False].values()

	@classmethod
	def iterentityitems(cls, xml=False):
		"""
		Return an iterator for iterating over the (name, class) items of all
		<pyref class="Entity">entity</pyref> and
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[2][xml].iteritems()

	@classmethod
	def entityitems(cls, xml=False):
		"""
		Return a list of all (name, class) items of all <pyref class="Entity">entity</pyref>
		and <pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[2][xml].items()

	@classmethod
	def entity(cls, name, xml=False):
		"""
		Return the <pyref class="Entity">entity</pyref> or
		<pyref class="CharRef">character reference</pyref> class with the name
		<arg>name</arg>. <arg>xml</arg> specifies whether <arg>name</arg> should
		be treated as a Python or &xml; name. If an entity or character reference
		class with this name doesn't exist an <class>IllegalEntityError</class>
		is raised.
		"""
		try:
			return cls._getcache()[2][xml][name]
		except KeyError:
			raise IllegalEntityError(name, xml=xml)

	@classmethod
	def itercharrefkeys(cls, xml=False):
		"""
		Return an iterator for iterating over the names of all
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[3][xml].iterkeys()

	@classmethod
	def charrefkeys(cls, xml=False):
		"""
		Return a list of the names of all
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[3][xml].keys()

	@classmethod
	def itercharrefvalues(cls):
		"""
		Return an iterator for iterating over all
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		"""
		return cls._getcache()[3][False].itervalues()

	@classmethod
	def charrefvalues(cls):
		"""
		Return a list of all <pyref class="CharRef">character reference</pyref>
		classes in <cls/>.
		"""
		return cls._getcache()[3][False].values()

	@classmethod
	def itercharrefitems(cls, xml=False):
		"""
		Return an iterator for iterating over the (name, class) items of all
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[3][xml].iteritems()

	@classmethod
	def charrefitems(cls, xml=False):
		"""
		Return a list of all (name, class) items of all
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[3][xml].items()

	@classmethod
	def charref(cls, name, xml=False):
		"""
		Return the <pyref class="CharRef">character reference</pyref> class with
		the name <arg>name</arg>. If <arg>name</arg> is a number return the
		character reference class defined for this codepoint. <arg>xml</arg>
		specifies whether <arg>name</arg> should be treated as a Python or &xml;
		name. If a character reference class with this name or codepoint doesn't
		exist an <class>IllegalCharRefError</class> is raised. If there are
		multiple character reference class for one codepoint an
		<class>AmbiguousCharRefError</class> will be raised.
		"""
		cache = cls._getcache()
		try:
			if isinstance(name, (int, long)):
				charrefs = cache[3][2][name]
				if len(charrefs) > 1:
					raise AmbiguousCharRefError(name, xml)
				return charrefs[0]
			else:
				return cache[3][xml][name]
		except KeyError:
			raise IllegalCharRefError(name, xml=xml)

	@classmethod
	def updateexisting(cls, *args, **kwargs):
		"""
		Copy attributes from all mappings in <arg>args</arg> and from
		<arg>kwargs</arg>, but only if they exist in <self/>.
		"""
		for mapping in args + (kwargs,):
			for (key, value) in mapping.iteritems():
				if value is not cls and key not in ("__name__", "__dict__") and hasattr(cls, key):
					setattr(cls, key, value)

	@classmethod
	def updatenew(cls, *args, **kwargs):
		"""
		Copy attributes over from all mappings in <arg>args</arg> and from
		<arg>kwargs</arg>, but only if they don't exist in <self/>.
		"""
		args = list(args)
		args.reverse()
		for mapping in [kwargs] + args: # Iterate in reverse order, so the last entry wins
			for (key, value) in mapping.iteritems():
				if value is not cls and key not in ("__name__", "__dict__") and not hasattr(cls, key):
					setattr(cls, key, value)

	@classmethod
	def tokenize(cls, string, encoding):
		"""
		Tokenize the string <arg>string</arg> (which must be an &xml; string
		generated by &xist; in the encoding <arg>encoding</arg>) according
		to the processing instructions available in <cls/>. <function>tokenize</function>
		will generate tuples with the first item being the processing instruction
		class and the second being the PI data. <z>Text</z> content (i.e. anything
		other than PIs) will be returned as <lit>(str, <rep>data</rep>)</lit>.
		Unknown processing instructions (i.e. those from namespaces other that
		<cls/>) will be returned as literal text (i.e. as
		<lit>(str, "&lt;?<rep>target</rep> <rep>data</rep>?&gt;")</lit>).
		"""
		pos = 0
		while True:
			pos1 = string.find("<?", pos)
			if pos1<0:
				part = string[pos:]
				if part:
					yield (str, part)
				return
			pos2 = string.find("?>", pos1)
			if pos2<0:
				part = string[pos:]
				if part:
					yield (str, part)
				return
			part = string[pos:pos1]
			if part:
				yield (str, part)
			part = string[pos1+2: pos2].strip()
			parts = part.split(None, 1)
			target = parts[0]
			if len(parts) > 1:
				data = parts[1]
			else:
				data = ""
			try:
				yield (cls.procinst(unicode(target, encoding), xml=True), data)
			except IllegalProcInstError:
				yield (str, "<?%s %s?>" % (target, data)) # return unknown PIs as text
			pos = pos2+2

	def __init__(self, xmlprefix, xmlname, thing=None):
		raise TypeError("Namespace classes can't be instantiated")


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

		# get and format the line number
		line = self.line
		if line is None:
			line = "?"
		else:
			line = str(line)

		# get and format the column number
		col = self.col
		if col is None:
			col = "?"
		else:
			col = str(col)

		# now we have the parts => format them
		return "%s:%s:%s" % (presenters.strURL(sysid), presenters.strNumber(line), presenters.strNumber(col))

	def __repr__(self):
		return "<%s object sysid=%r, pubid=%r, line=%r, col=%r at %08x>" % \
			(self.__class__.__name__, self.sysid, self.pubid, self.line, self.col, id(self))

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.pubid==other.pubid and self.sysid==other.sysid and self.line==other.line and self.col==other.col

	def __ne__(self, other):
		return not self==other
