#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
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

import os, sys, random, copy, warnings, new, cStringIO

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
	<par>convert the <arg>value</arg> passed in to an &xist; <pyref class="Node"><class>Node</class></pyref>.</par>

	<par>If <arg>value</arg> is a tuple or list, it will be (recursively) converted
	to a <pyref class="Frag"><class>Frag</class></pyref>. Integers, strings, etc. will be converted to a
	<pyref class="Text"><class>Text</class></pyref>.
	If <arg>value</arg> is a <pyref class="Node"><class>Node</class></pyref> already, nothing will be done.
	In the case of <lit>None</lit> the &xist; Null (<class>xsc.Null</class>) will be returned.
	Anything else raises an exception.</par>
	"""
	if isinstance(value, Node):
		#if isinstance(value, Attr):
		#	return Frag(*value) # repack the attribute in a fragment, and we have a valid XSC node
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
		# Maybe it's an iterator?
		try:
			return Frag(*list(value))
		except TypeError:
			pass
	warnings.warn(errors.IllegalObjectWarning(value)) # none of the above, so we report it and maybe throw an exception
	return Null


###
###
###

# XPython support
def append(*args, **kwargs):
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

class Args(dict):
	def __init__(self, *args, **kwargs):
		dict.__init__(self)
		for k in self.__class__.__dict__:
			if not k.startswith("__"):
				self[k] = self.__class__.__dict__[k]
		for arg in args:
			if isinstance(arg, dict):
				self.update(arg)
			else:
				for (key, value) in arg:
					self[key] = value
		self.update(kwargs)

	def __getattr__(self, key):
		return self.__getitem__(key)

	def __setattr__(self, key, value):
		self.__setitem__(key, value)

	def __delattr__(self, key):
		self.__detitem__(key)

	def __repr__(self):
		rep = ", ".join([ "%s=%r" % (key, value) for (key, value) in self.iteritems() if key not in self.__class__.__dict__ or self[key] != self.__class__.__dict__[key] ]) # FIXME: Use GE in 2.4
		return "%s(%s)" % (self.__class__.__name__, rep)

	def copy(self):
		return self.__class__(self.iteritems())


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
			return "<class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def __repr__(self):
		return "<%s:%s object at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

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
	__fullname__ = classmethod(__fullname__)


###
### Magic constants for tree traversal
###

class Const(object):
	pass

entercontent = Const()
enterattrs = Const()


###
### Common tree traversal filters
###

class FindType(object):
	"""
	Tree traversal filter, that finds nodes of a certain type on the first level
	of the tree without decending further down.
	"""
	def __init__(self, *types):
		self.types = types
	def __call__(self, node):
		return (isinstance(node, self.types), )


class FindTypeAll(object):
	"""
	Tree traversal filter, that finds nodes of a certain type searching the complete tree
	"""
	def __init__(self, *types):
		self.types = types
	def __call__(self, node):
		return (isinstance(node, self.types), entercontent)


class FindTypeAllAttrs(object):
	"""
	Tree traversal filter, that finds nodes of a certain type searching the complete tree
	(including attributes)
	"""
	def __init__(self, *types):
		self.types = types
	def __call__(self, node):
		return (isinstance(node, self.types), entercontent, enterattrs)


class FindTypeTop(object):
	"""
	Tree traversal filter, that find nodes of a certain type searching the complete tree,
	but traversal of a the children of a node is skipped if this node is of the specified
	type.
	"""
	def __init__(self, *types):
		self.types = types
	def __call__(self, node):
		if isinstance(node, self.types):
			return (True,)
		else:
			return (entercontent,)


class FindOld(object):
	"""
	<par>Tree traversal filter that tries to be backwards compatible with older &xist; versions.</par>
	"""

	def __init__(self, type=None, subtype=False, attrs=None, test=None, searchchildren=False, searchattrs=False):
		"""
		<par>If you specify <arg>type</arg> as the class of an &xist; node only nodes
		of this class will be returned. If you pass a list of classes, nodes that are an
		instance of one of the classes will be returned.</par>

		<par>If you set <arg>subtype</arg> to <lit>True</lit> nodes that are a
		subtype of <arg>type</arg> will be returned too.</par>

		<par>If you pass a dictionary as <arg>attrs</arg> it has to contain
		string pairs and is used to match attribute values for elements. To match
		the attribute values their <pyref class="Node" method="__unicode__"><method>__unicode__</method></pyref>
		representation will be used. You can use <lit>None</lit> as the value to test that
		the attribute is set without testing the value.</par>

		<par>Additionally you can pass a test function in <arg>test</arg>, that
		returns <lit>True</lit>, when the node passed in has to be included in the
		result and <lit>False</lit> otherwise.</par>

		<par>If you set <arg>searchchildren</arg> to <lit>True</lit> not only
		the immediate children but also the grandchildren will be searched for nodes
		matching the other criteria.</par>

		<par>If you set <arg>searchattrs</arg> to <lit>True</lit> the attributes
		of the nodes (if <arg>type</arg> is <pyref class="Element"><class>Element</class></pyref>
		or one of its subtypes) will be searched too.</par>

		<par>Note that the node has to be of type <pyref class="Element"><class>Element</class></pyref>
		(or a subclass of it) to match <arg>attrs</arg>.</par>
		"""
		self.type = type
		self.subtype = subtype
		self.attrs = attrs
		self.test = test
		self.searchchildren = searchchildren
		self.searchattrs = searchattrs

	def __call__(self, node):
		result = []
		if isinstance(node, Attrs):
			if self.searchattrs:
				res.append(enterattrs)
		elif isinstance(node, Frag):
			if self.searchchildren:
				result.append(entercontent)
		elif isinstance(node, Element):
			if self._matches(node):
				result.append(True)
			if self.searchchildren:
				result.append(entercontent)
			if self.searchattrs:
				res.append(enterattrs)
		else:
			if self._matches(node):
				result.append(True)
		return result

	def _matchesattrs(self, node):
		if self.attrs is None:
			return True
		else:
			if isinstance(node, Element):
				for attr in self.attrs:
					if (attr not in node.Attrs or attr not in node.attrs) or ((self.attrs[attr] is not None) and (unicode(node[attr]) != self.attrs[attr])):
						return False
				return True
			else:
				return False

	def _matches(self, node):
		res = True
		type = self.type
		if type is not None:
			if not isinstance(type, (list, tuple)):
				type = (type,)
			for t in type:
				if self.subtype:
					if isinstance(node, t):
						res = self._matchesattrs(node)
						break
				else:
					if self.__class__ == t:
						res = self._matchesattrs(node)
						break
			else:
				res = False
		else:
			res = self._matchesattrs(node)
		if res and (self.test is not None):
			res = self.test(node)
		return res


###
### XFind support
###

class _XFindBase(object):
	def xfind(self, iterator, operators):
		return _XFinder(self.xwalk(iterator), operators)


class _XFinder(object):
	__slots__ = ("iterator", "operators")

	def __init__(self, iterator, *operators):
		self.iterator = iterator
		self.operators = operators

	def next(self):
		return self.iterator.next()

	def __iter__(self):
		if self.operators:
			return self.operators[0].xfind(self.iterator, self.operators[1:])
		else:
			return self

	def __getitem__(self, index):
		for item in self:
			if not index:
				return item
			index -= 1
		raise IndexError

	def __div__(self, other):
		return _XFinder(self.iterator, *(self.operators + (other,)))

	def __floordiv__(self, other):
		from ll.xist import xfind
		return _XFinder(self.iterator, *(self.operators + (xfind.all, other)))

	def __repr__(self):
		if self.operators:
			ops = "/" + "/".join([repr(op) for op in self.operators])  # FIXME: Use a GE in Python 2.4
		else:
			ops = ""
		return "<%s.%s object for %r%s at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self._iterator, ops, id(self))


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
### The DOM classes
###

class Node(Base):
	"""
	base class for nodes in the document tree. Derived classes must
	overwrite <pyref method="convert"><method>convert</method></pyref>
	and may overwrite <pyref method="publish"><method>publish</method></pyref>
	and <pyref method="__unicode__"><method>__unicode__</method></pyref>.
	"""
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

	class __metaclass__(Base.__metaclass__, _XFindBase):
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

		def xwalk(self, iterator):
			for child in iterator:
				if isinstance(child, (Frag, Element)):
					for subchild in child:
						if isinstance(subchild, self):
							yield subchild

	class Context(_Context):
		pass

	def __repr__(self):
		"""
		<par>uses the default presenter (defined in <pyref module="ll.xist.presenters"><module>ll.xist.presenters</module></pyref>)
		to return a string representation.</par>
		"""
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
		return a clone of <self/>. Compared to <pyref method="deepcopy"><method>deepcopy</method></pyref> <method>clone</method>
		will create multiple instances of objects that can be found in the tree more than once. <method>clone</method> can't
		clone trees that contains cycles.
		"""
		return self

	def copy(self):
		"""
		return a shallow copy of <self/>.
		"""
		return self.__copy__()

	def __copy__(self):
		return self

	def deepcopy(self):
		"""
		return a deep copy of <self/>.
		"""
		return self.__deepcopy__()

	def __deepcopy__(self, memo=None):
		return self

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
		<par>Convenience method for calling <pyref method="convert"><method>convert</method></pyref>.</par>
		<par><method>conv</method> will automatically set <lit><arg>converter</arg>.node</lit> to <self/> to remember the
		<z>document root</z> for which <method>conv</method> has been called, this means that you should not call
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

	def convert(self, converter):
		"""
		<par>implementation of the conversion method.
		When you define your own element classes you have to overwrite this method.</par>

		<par>E.g. when you want to define an element that packs its content into an &html;
		bold element, do the following:</par>

		<prog>
		class foo(xsc.Element):
			def convert(self, converter):
				return html.b(self.content).convert(converter)
		</prog>
		"""
		raise NotImplementedError("convert method not implemented in %s" % self.__class__.__name__)

	def __unicode__(self):
		"""
		<par>Return the character content of <self/> as a unicode string.
		This means that comments and processing instructions will be filtered out.
		For elements you'll get the element content.</par>

		<par>It might be useful to overwrite this function in your own
		elements. Suppose you have the following element:</par>
		<prog>
		class caps(xsc.Element):
			def convert(self, converter):
				return html.span(
					self.content.convert(converter),
					style="font-variant: small-caps;"
				)
		</prog>

		<par>that renders its content in small caps, then it might be useful
		to define <method>__unicode__</method> in the following way:</par>
		<prog>
		def __unicode__(self):
			return unicode(self.content).upper()
		</prog>

		<par><method>__unicode__</method> can be used everywhere where
		a plain string representation of the node is required.</par>
		"""
		raise NotImplementedError("__unicode__ method not implemented in %s" % self.__class__.__name__)

	def __str__(self):
		"""
		Return the character content of <self/> as a string (if possible, i.e.
		there are no character that are unencodable in the default encoding).
		"""
		return str(unicode(self))

	def asText(self, monochrome=True, squeezeBlankLines=False, lineNumbers=False, width=72):
		"""
		<par>Return the node as a formatted plain &ascii; string.
		Note that this really only make sense for &html; trees.</par>

		<par>This requires that <app moreinfo="http://w3m.sf.net/">w3m</app> is installed.</par>
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
		text = "\n".join([ line.rstrip() for line in text.splitlines()]) # FIXME: Use GE in 2.4
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
		"""
		if publisher is not None:
			return publisher.prefixmode
		else:
			return 0
	needsxmlns = classmethod(needsxmlns)

	def xmlprefix(cls, publisher=None):
		"""
		<par>Return the namespace prefix configured for publishing elements
		of this class with the publisher <arg>publisher</arg>
		(or the default prefix from the namespace if <arg>publisher</arg>
		is <lit>None</lit>.</par>
		"""
		if cls.xmlns is None:
			return None
		else:
			if publisher is None:
				return cls.xmlns.xmlname[True]
			else:
				return publisher.prefixes.prefix4ns(cls.xmlns)[0]
	xmlprefix = classmethod(xmlprefix)

	def _publishname(self, publisher):
		"""
		<par>publishes the name of <self/> to the <arg>publisher</arg> including
		a namespace prefix if required.</par>
		"""
		if self.needsxmlns(publisher)>=1:
			prefix = self.xmlprefix(publisher)
			if prefix is not None:
				publisher.publish(prefix)
				publisher.publish(u":")
		publisher.publish(self.xmlname[True])

	def parsed(self, parser, start=None):
		"""
		<par>This method will be called by the parser <arg>parser</arg>
		once after <self/> is created by the parser. This is e.g. used by
		<pyref class="URLAttr"><class>URLAttr</class></pyref> to incorporate
		the base <pyref module="ll.url" class="URL"><class>URL</class></pyref>
		into the attribute.</par>

		<par>For elements <function>parsed</function> will be called twice:
		once at the beginning (i.e. before the content is parsed) with <lit><arg>start</arg>==True</lit>
		and once at the end after parsing of the content is finished <lit><arg>start</arg>==False</lit>.</par>
		"""
		pass

	def checkvalid(self):
		"""
		<par>This method will be called when parsing or publishing to check whether <self/> is valid.</par>
		<par>If the object is found to be invalid a warning should be issued through the Python warning framework.</par>
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

	def asString(self, base=None, publisher=None, **publishargs):
		"""
		<par>returns this node as a unicode string.</par>

		<par>For the parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref> constructor.</par>
		"""
		stream = cStringIO.StringIO()
		if publisher is None:
			publisher = publishers.Publisher(**publishargs)
		oldencoding = publisher.encoding
		try:
			publisher.encoding = "utf-8"
			publisher.dopublication(stream, self, base)
		finally:
			publisher.encoding = oldencoding
		return stream.getvalue().decode("utf-8")

	def asBytes(self, base=None, publisher=None, **publishargs):
		"""
		<par>returns this node as a byte string suitable for writing
		to an &html; file or printing from a CGI script.</par>

		<par>For the parameters see the
		<pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref> constructor.</par>
		"""
		stream = cStringIO.StringIO()
		if publisher is None:
			publisher = publishers.Publisher(**publishargs)
		publisher.dopublication(stream, self, base)
		return stream.getvalue()

	def write(self, stream, base=None, publisher=None, **publishargs):
		"""
		<par>writes <self/> to the file like object <arg>stream</arg>.</par>

		<par>For the rest of the parameters
		see the <pyref module="ll.xist.publishers" class="Publisher"><class>ll.xist.publishers.Publisher</class></pyref> constructor.</par>
		"""
		if publisher is None:
			publisher = publishers.Publisher(**publishargs)
		publisher.dopublication(stream, self, base)

	def _walk(self, filter, path, filterpath, walkpath, skiproot):
		"""
		<par>Internal helper for <pyref method="walk"><method>walk</method></pyref>.</par>
		"""
		if filterpath or walkpath:
			path = path + [self]

		if callable(filter):
			if filterpath:
				found = filter(path)
			else:
				found = filter(self)
		else:
			found = filter

		for option in found:
			if option is not entercontent and option is not enterattrs and option:
				if walkpath:
					yield path
				else:
					yield self

	def walk(self, filter=(True, entercontent), filterpath=False, walkpath=False, skiproot=False):
		"""
		<par>Return an iterator for traversing the tree rooted at <self/>.</par>

		<par><arg>filter</arg> is used for specifying whether or not a node should be yielded
		and when the children of this node should be traversed.
		If <arg>filter</arg> is callable, it will be called for each node visited during
		the traversal and must return a sequence of <z>node handling options</z>. Otherwise
		(i.e. if <arg>filter</arg> is not callable) <arg>filter</arg> must be a sequence of
		node handling options that will be used for all visited nodes.</par>

		<par>Entries in this sequence can be the following:</par>

		<dlist>
		<term><lit>True</lit></term><item>This tells <method>walk</method> to yield this node from the iterator.</item>
		<term><lit>False</lit></term><item>Don't yield this node from the iterator (or simply leave this entry away).</item>
		<term><lit>enterattrs</lit></term><item>This is a global constant in <module>ll.xist.xsc</module> and
		tells <method>walk</method> to traverse the attributes of this node (if it's an
		<pyref class="Element"><class>Element</class></pyref>, otherwise this option will be ignored).</item>
		<term><lit>entercontent</lit></term><item>This is a global constant in <module>ll.xist.xsc</module> and
		tells <method>walk</method> to traverse the child nodes of this node (if it's an
		<pyref class="Element"><class>Element</class></pyref>, otherwise this option will be ignored).</item>
		</dlist>

		<par>These options will be executed in the order they are specified in the sequence, so
		to get a top down traversal of a tree (without entering attributes), the following call
		can be made:</par>

		<prog>
		<rep>node</rep>.walk((True, xsc.entercontent))
		</prog>

		<par>For a bottom up traversal the following call can be made:</par>

		<prog>
		<rep>node</rep>.walk((xsc.entercontent, True))
		</prog>

		<par><arg>filterpath</arg> specifies how <arg>filter</arg> will be called:
		If <arg>filterpath</arg> is false, <method>walk</method> will pass the node itself
		to the filter function, if <arg>filterpath</arg> is true, a list containing the complete
		path from the root node to the node to be tested will be passed to <arg>filter</arg>.</par>

		<par><arg>walkpath</arg> works similar to <arg>filterpath</arg> and specifies whether
		the node or a path to the node will be yielded from the iterator.</par>

		<par><arg>skiproot</arg> is only significant if <self/> is an element: If <arg>skiproot</arg> is true,
		the element itself will always be skipped, i.e. iteration starts with the content of the element.</par>
		"""
		return _XFinder(self._walk(filter, [], filterpath, walkpath, skiproot))

	def _visit(self, filter, path, filterpath, visitpath, skiproot):
		"""
		<par>Internal helper for <pyref method="visit"><method>visit</method></pyref>.</par>
		"""
		if filterpath or visitpath:
			path = path + [self]

		if callable(filter):
			if filterpath:
				found = filter(path)
			else:
				found = filter(self)
		else:
			found = filter

		for option in found:
			if callable(option):
				if visitpath:
					option(path)
				else:
					option(self)

	def visit(self, filter, filterpath=False, visitpath=False, skiproot=False):
		"""
		<par>Iterate through the tree and call a user specifyable function for each visited node.</par>

		<par><arg>filter</arg> works similar to the <arg>filter</arg> argument in
		<pyref method="walk"><method>walk</method></pyref>, but the <z>node handling options</z> are
		different: Instead of boolean values that tell <method>walk</method> whether
		the node (or a path to the node) must be yielded, <method>visit</method> expects callable objects
		and will pass the node (or a path to the node, if <arg>visitpath</arg> is true) to those callable objects.</par>

		<par>The <arg>filterpath</arg> and <arg>skiproot</arg> arguments have the same meaning as for
		<pyref method="walk"><method>walk</method></pyref>.</par>
		"""
		self._visit(filter, [], filterpath, visitpath, skiproot)

	def find(self, filter=(True, entercontent), filterpath=False, skiproot=False):
		"""
		Return a <pyref class="Frag"><class>Frag</class></pyref> containing all nodes
		found by the filter function <arg>filter</arg>. See <pyref method="walk"><method>walk</method></pyref>
		for an explanation of the arguments.
		"""
		return Frag(list(self.walk(filter, filterpath, False, skiproot)))

	def findfirst(self, filter=(True, entercontent), filterpath=False, skiproot=False):
		"""
		Return the first node found by the filter function <arg>filter</arg>.
		See <pyref method="walk"><method>walk</method></pyref> for an explanation of the arguments.
		"""
		for item in self.walk(filter, filterpath, False, skiproot):
			return item
		raise errors.NodeNotFoundError()

	def __div__(self, other):
		def _iterone(node):
			yield node
		return _XFinder(_iterone(self), other)

	def __floordiv__(self, other):
		def _iterone(node):
			yield node
		from ll.xist import xfind
		return _XFinder(_iterone(self), xfind.all, other)

	def compact(self):
		"""
		returns a version of <self/>, where textnodes or character references that contain
		only linefeeds are removed, i.e. potentially needless whitespace is removed.
		"""
		return self

	def _decoratenode(self, node):
		"""
		<par>decorate the <pyref class="Node"><class>Node</class></pyref>
		<arg>node</arg> with the same location information as <self/>.</par>
		"""

		node.startloc = self.startloc
		node.endloc = self.endloc
		return node

	def mapped(self, function, converter):
		"""
		<par>returns the node mapped through the function <arg>function</arg>.
		This call works recursively (for <pyref class="Frag"><class>Frag</class></pyref>
		and <pyref class="Element"><class>Element</class></pyref>).</par>
		<par>When you want an unmodified node you simply can return <self/>. <method>mapped</method>
		will make a copy of it and fill the content recursively. Note that element attributes
		will not be mapped. When you return a different node from <function>function</function>
		this node will be incorporated into the result as-is.</par>
		"""
		node = function(self, converter)
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

	def withSep(self, separator, clone=False):
		warnings.warn(DeprecationWarning("withSep() is deprecated, use withsep() instead"))
		return self.withsep(separator, clone)


class CharacterData(Node):
	"""
	<par>base class for &xml; character data (text, proc insts, comment, doctype etc.)</par>

	<par>provides nearly the same functionality as <class>UserString</class>,
	but omits a few methods.</par>
	"""
	__slots__ = ("__content",)

	def __init__(self, *content):
		self.__content = u"".join([unicode(x) for x in content]) # FIXME: Use GE in 2.4

	def __getcontent(self):
		return self.__content

	content = property(__getcontent, None, None, "<par>The text content of the node as a <class>unicode</class> object.</par>")

	def __hash__(self):
		return self.__content.__hash__()

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.__content==other.__content

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
		return self.__content.rfind(sub, start, end)

	def rindex(self, sub, start=0, end=sys.maxint):
		return self.__content.rindex(sub, start, end)

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

	def __unicode__(self):
		return self.content

	def publish(self, publisher):
		publisher.publishtext(self.content)

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
		list.extend(node, [ child.clone() for child in self ]) # FIXME: Use GE in 2.4
		return self._decoratenode(node)

	def __copy__(self):
		node = self._create()
		list.extend(node, self)
		return self._decoratenode(node)

	def __deepcopy__(self, memo=None):
		node = self._create()
		if memo is None:
			memo = {}
		memo[id(self)] = node
		list.extend(node, [ copy.deepcopy(child, memo) for child in self ]) # FIXME: Use GE in 2.4
		return self._decoratenode(node)

	def present(self, presenter):
		presenter.presentFrag(self)

	def __unicode__(self):
		return u"".join([ unicode(child) for child in self ]) # FIXME: Use GE in 2.4

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
			if index:
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
			if index:
				node = self
				for subindex in index[:-1]:
					node = node[subindex]
				del node[index[-1]]
		else:
			list.__delitem__(self, index)

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
		list.__setslice__(self, index1, index2, Frag(sequence))

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

	def __iadd__(self, other):
		self.extend(other)
		return self

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

	def extend(self, items):
		"""
		<par>append all items from the sequence <arg>other</arg> to <self/>.</par>
		"""
		self.append(items)

	def insert(self, index, *others):
		"""
		<par>inserts all items in <arg>others</arg> at the position <arg>index</arg>.
		(this is the same as <lit><self/>[<arg>index</arg>:<arg>index</arg>] = <arg>others</arg></lit>)
		"""
		other = Frag(*others)
		list.__setslice__(self, index, index, other)

	def _walk(self, filter, path, filterpath, walkpath, skiproot):
		for child in self:
			for object in child._walk(filter, path, filterpath, walkpath, False):
				yield object

	def _visit(self, filter, path, filterpath, visitpath, skiproot):
		for child in self:
			child._visit(filter, path, filterpath, visitpath, False)

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
		node = list(self)
		node.sort(compare)
		return self.__class__(node)

	def reversed(self):
		"""
		<par>returns a reversed version of the <self/>.</par>
		"""
		node = list(self)
		node.reverse()
		return self.__class__(node)

	def filtered(self, function):
		"""
		<par>returns a filtered version of the <self/>.</par>
		"""
		node = self._create()
		list.extend(node, [ child for child in self if function(child) ]) # FIXME: Use GE in 2.4
		return node

	def shuffled(self):
		"""
		<par>return a shuffled version of <self/>.</par>
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
	A comment node
	"""

	def convert(self, converter):
		return self

	def __unicode__(self):
		return u""

	def present(self, presenter):
		presenter.presentComment(self)

	def publish(self, publisher):
		if publisher.inattr:
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

	def present(self, presenter):
		presenter.presentDocType(self)

	def publish(self, publisher):
		if publisher.inattr:
			raise errors.IllegalAttrNodeError(self)
		publisher.publish(u"<!DOCTYPE ")
		publisher.publish(self.content)
		publisher.publish(u">")

	def __unicode__(self):
		return u""


class ProcInst(CharacterData):
	"""
	<par>Base class for processing instructions. This class is abstract.</par>

	<par>Processing instructions for specific targets must
	be implemented as subclasses of <class>ProcInst</class>.</par>
	"""
	register = None

	class __metaclass__(CharacterData.__metaclass__):
		def __repr__(self):
			return "<procinst class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

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

	def present(self, presenter):
		presenter.presentProcInst(self)

	def publish(self, publisher):
		if self.content.find(u"?>")!=-1:
			raise errors.IllegalProcInstFormatError(self)
		publisher.publish(u"<?")
		publisher.publish(self.xmlname[True])
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

	def publish(self, publisher):
		pass

	def present(self, presenter):
		presenter.presentNull(self)

	def __unicode__(self):
		return u""

Null = Null() # Singleton, the Python way


class Attr(Frag):
	r"""
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
	<prog>
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
	</prog>
	</example>
	"""
	required = False
	default = None
	values = None
	class __metaclass__(Frag.__metaclass__, _XFindBase):
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
					dict["values"] = tuple([unicode(entry) for entry in dict["values"]]) # FIXME: Use GE in 2.4
			return Frag.__metaclass__.__new__(cls, name, bases, dict)

		def __repr__(self):
			return "<attribute class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

		def xwalk(self, iterator):
			for child in iterator:
				if isinstance(child, Element):
					for (attrname, attrvalue) in child.attrs.iteritems():
						if isinstance(attrvalue, self):
							yield attrvalue

	def isfancy(self):
		"""
		<par>Return whether <self/> contains nodes
		other than <pyref class="Text"><class>Text</class></pyref>.</par>
		"""
		for child in self:
			if not isinstance(child, Text):
				return True
		return False

	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		cls._strbase(presenters.strAttrName, s, fullname=fullname, xml=xml)
		return s
	_str = classmethod(_str)

	def present(self, presenter):
		presenter.presentAttr(self)

	def needsxmlns(self, publisher=None):
		if self.xmlns is not None:
			return 2
		else:
			return 0
	needsxmlns = classmethod(needsxmlns)

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
				warnings.warn(errors.IllegalAttrValueWarning(self))

	def _walk(self, filter, path, filterpath, walkpath, skiproot):
		if filterpath or walkpath:
			path = path + [self]

		if callable(filter):
			if filterpath:
				found = filter(path)
			else:
				found = filter(self)
		else:
			found = filter

		for option in found:
			if option is entercontent:
				for object in Frag._walk(self, filter, path, filterpath, walkpath, False):
					yield object
			elif option is enterattrs:
				pass
			elif option:
				if walkpath:
					yield path
				else:
					yield self

	def _visit(self, filter, path, filterpath, visitpath, skiproot):
		if filterpath or visitpath:
			path = path + [self]

		if callable(filter):
			if filterpath:
				found = filter(path)
			else:
				found = filter(self)
		else:
			found = filter

		for option in found:
			if option is entercontent:
				super(Attr, self)._visit(filter, path, filterpath, visitpath, False)
			elif option is enterattrs:
				pass
			elif callable(option):
				if visitpath:
					option(path)
				else:
					option(self)

	def _publishAttrValue(self, publisher):
		Frag.publish(self, publisher)

	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		publisher.inattr += 1
		self._publishname(publisher) # publish the XML name, not the Python name
		publisher.publish(u"=\"")
		publisher.pushtextfilter(helpers.escapeattr)
		self._publishAttrValue(publisher)
		publisher.poptextfilter()
		publisher.publish(u"\"")
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
		if publisher.validate:
			self.checkvalid()
		publisher.inattr += 1
		self._publishname(publisher) # publish the XML name, not the Python name
		if publisher.xhtml>0:
			publisher.publish(u"=\"")
			publisher.pushtextfilter(helpers.escapeattr)
			publisher.publish(self.__class__.xmlname[True])
			publisher.poptextfilter()
			publisher.publish(u"\"")
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


class Attrs(Node, dict):
	"""
	<par>An attribute map. Allowed entries are specified through nested subclasses
	of <pyref class="Attr"><class>Attr</class></pyref>.</par>
	"""

	class __metaclass__(Node.__metaclass__):
		def __new__(mcl, name, bases, dict):
			# Automatically inherit the attributes from the base class (because the global Attrs require a pointer back to their defining namespace)
			for base in bases:
				for attrname in dir(base):
					attr = getattr(base, attrname)
					if isinstance(attr, type) and issubclass(attr, Attr) and attrname not in dict:
						classdict = {"__module__": dict["__module__"]}
						if attr.xmlname[False] != attr.xmlname[True]:
							classdict["xmlname"] = attr.xmlname[True]
						classdict["__outerclass__"] = 42
						dict[attrname] = attr.__class__(attr.__name__, (attr,), classdict)
			dict["_attrs"] = ({}, {}) # cache for attributes (by Python name and by XML name)
			dict["_defaultattrs"] = ({}, {}) # cache for attributes that have a default value (by Python name and by XML name)
			cls = Node.__metaclass__.__new__(mcl, name, bases, dict)
			# go through the attributes and put them in the cache
			for (key, value) in cls.__dict__.iteritems():
				if isinstance(value, type):
					if getattr(value, "__outerclass__", None) == 42:
						value.__outerclass__ = cls
					if issubclass(value, Attr):
						setattr(cls, key, value)
			return cls

		def __repr__(self):
			return "<attrs class %s:%s with %s attrs at 0x%x>" % (self.__module__, self.__fullname__(), len(self._attrs[0]), id(self))

		def __getitem__(cls, key):
			return cls._attrs[False][key]

		def __delattr__(cls, key):
			value = cls.__dict__.get(key, None) # no inheritance
			if isinstance(value, type) and issubclass(value, Attr):
				for xml in (False, True):
					name = value.xmlname[xml]
					cls._attrs[xml].pop(name, None)
					cls._defaultattrs[xml].pop(name, None)
			return Node.__metaclass__.__delattr__(cls, key)

		def __setattr__(cls, key, value):
			oldvalue = cls.__dict__.get(key, None) # no inheritance
			if isinstance(oldvalue, type) and issubclass(oldvalue, Attr):
				for xml in (False, True):
					# ignore KeyError exceptions, because in the meta class constructor the attributes *are* in the class dict, but haven't gone through __setattr__, so they are not in the cache
					cls._attrs[xml].pop(oldvalue.xmlname[xml], None)
					cls._defaultattrs[xml].pop(oldvalue.xmlname[xml], None)
			if isinstance(value, type) and issubclass(value, Attr):
				for xml in (False, True):
					name = value.xmlname[xml]
					cls._attrs[xml][name] = value
					if value.default:
						cls._defaultattrs[xml][name] = value
			return Node.__metaclass__.__setattr__(cls, key, value)

		def __contains__(cls, key):
			return key in cls._attrs[False]

	def __init__(self, content=None, **attrs):
		dict.__init__(self)
		# set default attribute values
		for (key, value) in self._defaultattrs[False].iteritems():
			self[key] = value.default.clone()
		# set attributes, this might overwrite (or delete) default attributes
		self.update(content, **attrs)

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

	def _walk(self, filter, path, filterpath, walkpath, skiproot):
		for child in self.itervalues():
			for object in child._walk(filter, path, filterpath, walkpath, False):
				yield object

	def _visit(self, filter, path, filterpath, visitpath, skiproot):
		for child in self.itervalues():
			child._visit(filter, path, filterpath, visitpath, False)

	def present(self, presenter):
		presenter.presentAttrs(self)

	def checkvalid(self):
		# collect required attributes
		attrs = {} # FIXME: Use a set with Python 2.4
		for (key, value) in self.iteralloweditems():
			if value.required:
				attrs[key] = None
		# Check each attribute and remove it from the list of required ones
		for (attrname, attrvalue) in self.iteritems():
			attrvalue.checkvalid()
			try:
				del attrs[attrname]
			except KeyError:
				pass
		# are there any required attributes remaining that haven't been specified? => warn about it
		if attrs:
			warnings.warn(errors.RequiredAttrMissingWarning(self, attrs.keys()))

	def publish(self, publisher):
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
			warnings.warn(errors.RequiredAttrMissingWarning(self, attrs.keys()))

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
		attr = self.allowedattr(name, xml=xml)(value)
		dict.__setitem__(self, self._allowedattrkey(name, xml=xml), attr) # put the attribute in our dict

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
						self[(attrvalue.xmlns, attrname)] = attrvalue
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
						if (attrvalue.xmlns, attrname) in self:
							self[(attrvalue.xmlns, attrname)] = attrvalue
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
						if (attrvalue.xmlns, attrname) not in self:
							self[(attrvalue.xmlns, attrname)] = attrvalue
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

	def iterallowedkeys(cls, xml=False):
		"""
		<par>return an iterator for iterating through the names of allowed attributes. <arg>xml</arg>
		specifies whether &xml; names (<lit><arg>xml</arg>==True</lit>) or Python names
		(<lit><arg>xml</arg>==False</lit>) should be returned.</par>
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
		return cls._attrs[False].itervalues()
	iterallowedvalues = classmethod(iterallowedvalues)

	def allowedvalues(cls):
		"""
		<par>return a list of values for the allowed values.</par>
		"""
		return cls._attrs[False].values()
	allowedvalues = classmethod(allowedvalues)

	def iteralloweditems(cls, xml=False):
		return cls._attrs[xml].iteritems()
	iteralloweditems = classmethod(iteralloweditems)

	def alloweditems(cls, xml=False):
		return cls._attrs[xml].items()
	alloweditems = classmethod(alloweditems)

	def _allowedattrkey(cls, name, xml=False):
		try:
			return cls._attrs[xml][name].xmlname[False]
		except KeyError:
			raise errors.IllegalAttrError(cls, name, xml=xml)
	_allowedattrkey = classmethod(_allowedattrkey)

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
			if value:
				if isinstance(key, tuple):
					yield (value.xmlns, value.xmlname[xml])
				else:
					yield value.xmlname[xml]

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
					yield ((value.xmlns, value.xmlname[xml]), value)
				else:
					yield (value.xmlname[xml], value)

	def items(self, xml=False):
		return list(self.iteritems(xml=xml))

	def _iterallitems(self):
		"""
		Iterate all items, even the unset ones
		"""
		for (key, value) in dict.iteritems(self):
			if isinstance(key, tuple):
				yield ((value.xmlns, value.xmlname[False]), value)
			else:
				yield (value.xmlname[False], value)

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
	by deriving <pyref class="Namespace"><class>Namespace</class></pyref>
	classes.</par>

	<par>Every element class should have two class variables:
	<lit>model</lit>: this is an object that is used for validating the
	content of the element. See the module <pyref module="ll.xist.sims"><module>ll.xist.sims</module></pyref>
	for more info. If <lit>model</lit> is <lit>None</lit> validation will
	be skipped, otherwise it will be performed when parsing or publishing.</par>

	<par><lit>Attrs</lit>, which is a class derived from
	<pyref class="Element.Attrs"><class>Element.Attrs</class></pyref>
	and should define all attributes as classes nested inside this
	<class>Attrs</class> class.</par>
	"""

	model = None
	register = None

	class __metaclass__(Node.__metaclass__):
		def __new__(cls, name, bases, dict):
			if "name" in dict and isinstance(dict["name"], basestring):
				warnings.warn(DeprecationWarning("name is deprecated, use xmlname instead"))
				dict["xmlname"] = dict["name"]
				del dict["name"]
			if "attrHandlers" in dict:
				warnings.warn(DeprecationWarning("attrHandlers is deprecated, use a nested Attrs class instead"), stacklevel=2)
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
			
			return Node.__metaclass__.__new__(cls, name, bases, dict)

		def __repr__(self):
			return "<element class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	class Attrs(Attrs):
		def _allowedattrkey(cls, name, xml=False):
			if isinstance(name, tuple):
				return (name[0], name[0].Attrs._allowedattrkey(name[1], xml=xml)) # ask namespace about global attribute
			try:
				return cls._attrs[xml][name].xmlname[False]
			except KeyError:
				raise errors.IllegalAttrError(cls, name, xml=xml)
		_allowedattrkey = classmethod(_allowedattrkey)

		def allowedattr(cls, name, xml=False):
			if isinstance(name, tuple):
				return name[0].Attrs.allowedattr(name[1], xml=xml) # ask namespace about global attribute
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
	_str = classmethod(_str)

	def checkvalid(self):
		if self.model is not None:
			self.model.checkvalid(self)
		self.attrs.checkvalid()

	def append(self, *items):
		"""
		<par>appends to content (see <pyref class="Frag" method="append"><method>Frag.append</method></pyref>
		for more info)</par>
		"""
		self.content.append(*items)

	def extend(self, items):
		"""
		<par>appends to content (see <pyref class="Frag" method="extend"><method>Frag.extend</method></pyref>
		for more info)</par>
		"""
		self.content.extend(items)

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
		hhe width of the image will be put into the attribute with the name <arg>widthattr</arg>
		if <arg>widthattr</arg> is not <lit>None</lit> and the attribute is not set. The
		same will happen for the height, which will be put into the <arg>heighattr</arg>.</par>
		"""

		try:
			size = url.openread().imagesize
		except IOError, exc:
			warnings.warn(errors.FileNotFoundWarning("can't read image", url, exc))
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
		publisher.publish(u"<")
		self._publishname(publisher)
		# we're the first element to be published, so we have to create the xmlns attributes
		if publisher.publishxmlns:
			for (ns, prefix) in publisher.publishxmlns.iteritems():
				publisher.publish(u" xmlns")
				if prefix is not None:
					publisher.publish(u":")
					publisher.publish(prefix)
				publisher.publish(u"=\"")
				publisher.publish(ns.xmlurl)
				publisher.publish(u"\"")
			# reset the note, so the next element won't create the attributes again
			publisher.publishxmlns = None
		self.attrs.publish(publisher)
		if len(self):
			publisher.publish(u">")
			self.content.publish(publisher)
			publisher.publish(u"</")
			self._publishname(publisher)
			publisher.publish(u">")
		else:
			if publisher.xhtml in (0, 1):
				if self.model is not None and self.model.empty:
					if publisher.xhtml==1:
						publisher.publish(u" /")
					publisher.publish(u">")
				else:
					publisher.publish(u"></")
					self._publishname(publisher)
					publisher.publish(u">")
			elif publisher.xhtml == 2:
				publisher.publish(u"/>")

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
		returns an attribute or one of the content nodes depending on whether
		an 8bit or unicode string (i.e. attribute name) or a number or list
		(i.e. content node index) is passed in.
		"""
		if isinstance(index, list):
			node = self
			for subindex in index:
				node = node[subindex]
			return node
		elif isinstance(index, (int, long)):
			return self.content[index]
		elif isinstance(index, slice):
			return self.__class__(self.content[index], self.attrs)
		else:
			return self.attrs[index]

	def __setitem__(self, index, value):
		"""
		<par>sets an attribute or one of the content nodes depending on whether
		an 8bit or unicode string (i.e. attribute name) or a number or list (i.e.
		content node index) is passed in.</par>
		"""
		if isinstance(index, list):
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
		removes an attribute or one of the content nodes depending on whether
		a string (i.e. attribute name) or a number or list (i.e. content node index) is passed in.
		"""
		if isinstance(index, list):
			if index:
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

	def __iadd__(self, other):
		self.extend(other)
		return self

	def hasAttr(self, attrname, xml=False):
		warnings.warn(DeprecationWarning("foo.hasAttr() is deprecated, use foo.attrs.has() instead"))
		return self.attrs.has(attrname, xml=xml)

	def hasattr(self, attrname, xml=False):
		warnings.warn(DeprecationWarning("foo.hasattr() is deprecated, use foo.attrs.has() instead"))
		return self.attrs.has(attrname, xml=xml)

	def isallowedattr(cls, attrname):
		"""
		<par>return whether the attribute named <arg>attrname</arg> is allowed for <self/>.</par>
		"""
		warnings.warn(DeprecationWarning("foo.isallowedattr() is deprecated, use foo.Attrs.isallowed() instead"))
		return cls.Attrs.isallowed(attrname)
	isallowedattr = classmethod(isallowedattr)

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

	def allowedattrkeys(cls, xml=False):
		warnings.warn(DeprecationWarning("foo.allowedattrkeys() is deprecated, use foo.attrs.allowedkeys() instead"))
		return cls.Attrs.allowedkeys(xml=xml)
	allowedattrkeys = classmethod(allowedattrkeys)

	def allowedattrvalues(cls):
		warnings.warn(DeprecationWarning("foo.allowedattrvalues() is deprecated, use foo.attrs.allowedvalues() instead"))
		return cls.Attrs.allowedvalues()
	allowedattrvalues = classmethod(allowedattrvalues)

	def allowedattritems(cls, xml=False):
		warnings.warn(DeprecationWarning("foo.allowedattritems() is deprecated, use foo.attrs.alloweditems() instead"))
		return cls.Attrs.alloweditems(xml=xml)
	allowedattritems = classmethod(allowedattritems)

	def iterallowedattrkeys(cls, xml=False):
		warnings.warn(DeprecationWarning("foo.iterallowedattrkeys() is deprecated, use foo.attrs.iterattrkeys() instead"))
		return cls.Attrs.iterallowedkeys(xml=xml)
	iterallowedattrkeys = classmethod(iterallowedattrkeys)

	def iterallowedattrvalues(cls):
		warnings.warn(DeprecationWarning("foo.iterallowedattrvalues() is deprecated, use foo.attrs.iterattrvalues() instead"))
		return cls.Attrs.iterallowedvalues()
	iterallowedattrvalues = classmethod(iterallowedattrvalues)

	def iterallowedattritems(cls, xml=False):
		warnings.warn(DeprecationWarning("foo.iterallowedattritems() is deprecated, use foo.attrs.iterattritems() instead"))
		return cls.Attrs.iteralloweditems(xml=xml)
	iterallowedattritems = classmethod(iterallowedattritems)

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

	def _walk(self, filter, path, filterpath, walkpath, skiproot):
		if filterpath or walkpath:
			path = path + [self]

		if skiproot:
			for object in self.content._walk(filter, path, filterpath, walkpath, False):
				yield object
		else:
			if callable(filter):
				if filterpath:
					found = filter(path)
				else:
					found = filter(self)
			else:
				found = filter

			for option in found:
				if option is entercontent:
					for object in self.content._walk(filter, path, filterpath, walkpath, False):
						yield object
				elif option is enterattrs:
					for object in self.attrs._walk(filter, path, filterpath, walkpath, False):
						yield object
				elif option:
					if walkpath:
						yield path
					else:
						yield self

	def _visit(self, filter, path, filterpath, visitpath, skiproot):
		if filterpath or visitpath:
			path = path + [self]

		if skiproot:
			self.content._visit(filter, path, filterpath, visitpath, False)
		else:
			if callable(filter):
				if filterpath:
					found = filter(path)
				else:
					found = filter(self)
			else:
				found = filter

			for option in found:
				if option is entercontent:
					self.content._visit(filter, path, filterpath, visitpath, False)
				elif option is enterattrs:
					self.attrs._visit(filter, path, filterpath, visitpath, False)
				elif callable(option):
					if visitpath:
						option(path)
					else:
						option(self)

	def copyDefaultAttrs(self, fromMapping):
		"""
		<par>Sets attributes that are not set in <self/> to the default
		values taken from the <arg>fromMapping</arg> mapping.
		If <arg>fromDict</arg> is omitted, defaults are taken from
		<lit><self/>.defaults</lit>.</par>

		<par>Note that boolean attributes may savely be set to e.g. <lit>1</lit>,
		as only the fact that a boolean attribute exists matters.</par>
		"""

		warnings.warn(DeprecationWarning("foo.copyDefaultAttrs() is deprecated, use foo.attrs.updateexisting() instead"))
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


class Entity(Node):
	"""
	<par>Class for entities. Derive your own entities from
	it and overwrite <pyref class="Node" method="convert"><method>convert</method></pyref>
	and <pyref class="Node" method="__unicode__"><method>__unicode__</method></pyref>.</par>
	"""
	register = None

	class __metaclass__(Node.__metaclass__):
		def __repr__(self):
			return "<entity class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

	def _str(cls, fullname=True, xml=True, decorate=True):
		s = ansistyle.Text()
		if decorate:
			s.append(presenters.strAmp())
		cls._strbase(presenters.strEntityName, s, fullname=fullname, xml=xml)
		if decorate:
			s.append(presenters.strSemi())
		return s
	_str = classmethod(_str)

	def compact(self):
		return self

	def present(self, presenter):
		presenter.presentEntity(self)

	def publish(self, publisher):
		publisher.publish(u"&")
		publisher.publish(self.xmlname[True])
		publisher.publish(u";")


class CharRef(Text, Entity):
	"""
	<par>A simple character reference, the codepoint is in the class attribute
	<lit>codepoint</lit>.</par>
	"""
	register = None

	class __metaclass__(Entity.__metaclass__):
		def __repr__(self):
			return "<charref class %s:%s at 0x%x>" % (self.__module__, self.__fullname__(), id(self))

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

	def ljust(self, width):
		return Text(self.content.ljust(width))

	def lower(self):
		return Text(self.content.lower())

	def lstrip(self):
		return Text(self.content.lstrip())

	def replace(self, old, new, maxsplit=-1):
		return Text(self.content.replace(old, new, maxsplit))

	def rjust(self, width):
		return Text(self.content.rjust(width))

	def rstrip(self):
		return Text(self.content.rstrip())

	def strip(self):
		return Text(self.content.strip())

	def swapcase(self):
		return Text(self.content.swapcase())

	def title(self):
		return Text(self.content.title())

	def translate(self, table):
		return Text(self.content.translate(table))

	def upper(self):
		return Text(self.content.upper())


###
### Classes for namespace handling
###

class NSPool(dict):
	"""
	<par>A pool of namespaces identified by their name.</par>
	<par>A pool may only have one namespace for one namespace name.</par>
	"""
	def __init__(self, *args):
		dict.__init__(self, [(arg.xmlurl, arg) for arg in args]) # FIXME: Use GE in 2.4

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

	def __init__(self, nswithoutprefix=None, **nswithprefix):
		dict.__init__(self)
		if nswithoutprefix is not None:
			self[None] = nswithoutprefix
		for (prefix, ns) in nswithprefix.iteritems():
			self[prefix] = ns

	def __repr__(self):
		return "<%s.%s %s at 0x%x>" % (self.__module__, self.__class__.__name__, " ".join(["%s=%r" % (key or "None", value) for (key, value) in self.iteritems()]), id(self)) # FIXME: Use GE in 2.4

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
			return [ns.xmlname[True]]

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
		(prefix, name) = self.__splitqname(qname)
		for ns in self[prefix]:
			try:
				element = ns.element(name, xml=True)
				if element.register:
					return element
			except LookupError: # no element in this namespace with this name
				pass
		raise errors.IllegalElementError(qname, xml=True) # elements with this name couldn't be found

	def procinst(self, name):
		"""
		<par>returns the processing instruction class for the name <arg>name</arg>.</par>
		"""
		candidates = {} # FIXME: Use a set in Python 2.4
		for nss in self.itervalues():
			for ns in nss:
				try:
					procinst = ns.procinst(name, xml=True)
				except LookupError: # no processing instruction in this namespace with this name
					pass
				else:
					if procinst.register:
						candidates[procinst] = True
		if len(candidates)==1:
			return candidates.popitem()[0]
		elif len(candidates)==0:
			raise errors.IllegalProcInstError(name, xml=True) # processing instructions with this name couldn't be found
		else:
			raise errors.AmbiguousProcInstError(name, xml=True) # there was more than one processing instructions with this name

	def entity(self, name):
		"""
		<par>returns the entity or charref class for the name <arg>name</arg>.</par>
		"""
		candidates = {} # FIXME: Use a set in Python 2.4
		for nss in self.itervalues():
			for ns in nss:
				try:
					entity = ns.entity(name, xml=True)
				except LookupError: # no entity in this namespace with this name
					pass
				else:
					if entity.register:
						candidates[entity] = True
		if len(candidates)==1:
			return candidates.popitem()[0]
		elif len(candidates)==0:
			raise errors.IllegalEntityError(name, xml=True) # entities with this name couldn't be found
		else:
			raise errors.AmbiguousEntityError(name, xml=True) # there was more than one entity with this name

	def charref(self, name):
		"""
		<par>returns the first charref class for the name or codepoint <arg>name</arg>.</par>
		"""
		candidates = {} # FIXME: Use a set in Python 2.4
		for nss in self.itervalues():
			for ns in nss:
				try:
					charref = ns.charref(name, xml=True)
				except LookupError: # no entity in this namespace with this name
					pass
				else:
					if charref.register:
						candidates[charref] = True
		if len(candidates)==1:
			return candidates.popitem()[0]
		elif len(candidates)==0:
			raise errors.IllegalCharRefError(name, xml=True) # character references with this name/codepoint couldn't be found
		else:
			raise errors.AmbiguousCharRefError(name, xml=True) # there was more than one character reference with this name

	def attrnamefromqname(self, element, qname):
		"""
		<par>returns the Python name for an attribute for the qualified
		&xml; name <arg>qname</arg> (which might include a prefix, in which case
		a tuple with the namespace object and the name will be returned, otherwise
		it will be an attribute from the element <arg>element</arg>, which must
		be a subclass of <pyref class="Element"><class>Element</class></pyref>).</par>
		"""
		qname = self.__splitqname(qname)
		if qname[0] is None:
			return element.Attrs.allowedattr(qname[1], xml=True).xmlname[False]
		else:
			for ns in self[qname[0]]:
				try:
					attr = ns.Attrs.allowedattr(qname[1], xml=True)
					if attr.register:
						return (ns, attr.xmlname[False])
				except errors.IllegalAttrError: # no attribute in this namespace with this name
					pass
			raise errors.IllegalAttrError(None, qname, xml=True)

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
				self[ns.xmlname[True]].append(ns)
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
				self[ns.xmlname[True]] = ns


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

class Namespace(Base):
	"""
	<par>an &xml; namespace.</par>
	
	<par>Classes for elements, entities and processing instructions
	can be defined as nested classes inside subclasses of <class>Namespace</class>.
	This class will never be instantiated.</par>
	"""

	xmlname = None
	xmlurl = None

	nsbyname = {}
	nsbyurl = {}
	all = []

	class __metaclass__(Base.__metaclass__):
		def __new__(mcl, name, bases, dict):
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
						if attr.xmlname[0] != attr.xmlname[1]:
							classdict["xmlname"] = attr.xmlname[1]
						classdict["__outerclass__"] = 42
						dict[attrname] = attr.__class__(attr.__name__, (attr, ), classdict)
			dict["_cache"] = None
			cls = Base.__metaclass__.__new__(mcl, name, bases, dict)
			cls.__originalname = name # preserves the name even after makemod() (used by __repr__)
			for (key, value) in cls.__dict__.iteritems():
				if isinstance(value, type):
					if getattr(value, "__outerclass__", None) == 42:
						value.__outerclass__ = cls
					if issubclass(value, (Element, ProcInst, Entity)):
						value.xmlns = cls
			for attr in cls.Attrs.iterallowedvalues():
				attr.xmlns = cls
			if cls.xmlurl is not None:
				name = cls.xmlname[True]
				cls.nsbyname.setdefault(name, []).insert(0, cls)
				cls.nsbyurl.setdefault(cls.xmlurl, []).insert(0, cls)
				cls.all.append(cls)
				defaultPrefixes[None].insert(0, cls)
				defaultPrefixes[name].insert(0, cls)
				defaultnspool.add(cls)
			return cls

		def __eq__(self, other):
			if isinstance(other, type) and issubclass(other, Namespace):
				return self.xmlname[True]==other.xmlname[True] and self.xmlurl==other.xmlurl
			return False

		def __ne__(self, other):
			return not self==other

		def __hash__(self):
			return hash(self.xmlname[True]) ^ hash(self.xmlurl)

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
			return "<namespace %s:%s name=%r url=%r%s%s at 0x%x>" % (self.__module__, self.__originalname, self.xmlname[True], self.xmlurl, counts, fromfile, id(self))

		def __delattr__(cls, key):
			value = cls.__dict__.get(key, None) # no inheritance
			if isinstance(value, type) and issubclass(value, (Element, ProcInst, CharRef)):
				value.xmlns = None
				cls._cache = None
			return type.__delattr__(cls, key)

		def __setattr__(cls, key, value):
			# Remove old attribute
			oldvalue = cls.__dict__.get(key, None) # no inheritance
			if isinstance(oldvalue, type) and issubclass(oldvalue, (Element, ProcInst, Entity)):
				if oldvalue.xmlns is not None:
					oldvalue.xmlns._cache = None
					oldvalue.xmlns = None
			# Set new attribute
			if isinstance(value, type) and issubclass(value, (Element, ProcInst, Entity)):
				if value.xmlns is not None:
					value.xmlns._cache = None
					value.xmlns = None
				cls._cache = None
				value.xmlns = cls
			elif isinstance(value, new.function):
				value = staticmethod(value)
			return type.__setattr__(cls, key, value)

	class Attrs(_Attrs):
		pass

	class Context(_Context):
		pass

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
					for xml in (False, True):
						c[0][xml][value.xmlname[xml]] = value
				elif issubclass(value, ProcInst):
					for xml in (False, True):
						c[1][xml][value.xmlname[xml]] = value
				elif issubclass(value, Entity):
					for xml in (False, True):
						c[2][xml][value.xmlname[xml]] = value
					if issubclass(value, CharRef):
						for xml in (False, True):
							c[3][xml][value.xmlname[xml]] = value
						c[3][2].setdefault(value.codepoint, []).append(value)
		cls._cache = c
		return c
	_getcache = classmethod(_getcache)

	def iterelementkeys(cls, xml=False):
		"""
		Return an iterator for iterating over the names of all <pyref class="Element">element</pyref> classes
		in <cls/>. <arg>xml</arg> specifies whether Python or &xml; names
		should be returned.
		"""
		return cls._getcache()[0][xml].iterkeys()
	iterelementkeys = classmethod(iterelementkeys)

	def elementkeys(cls, xml=False):
		"""
		Return a list of the names of all <pyref class="Element">element</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[0][xml].keys()
	elementkeys = classmethod(elementkeys)

	def iterelementvalues(cls):
		"""
		Return an iterator for iterating over all <pyref class="Element">element</pyref> classes in <cls/>.
		"""
		return cls._getcache()[0][False].itervalues()
	iterelementvalues = classmethod(iterelementvalues)

	def elementvalues(cls):
		"""
		Return a list of all <pyref class="Element">element</pyref> classes in <cls/>.
		"""
		return cls._getcache()[0][False].values()
	elementvalues = classmethod(elementvalues)

	def iterelementitems(cls, xml=False):
		"""
		Return an iterator for iterating over the (name, class) items of all <pyref class="Element">element</pyref> classes
		in <cls/>. <arg>xml</arg> specifies whether Python or &xml; names
		should be returned.
		"""
		return cls._getcache()[0][xml].iteritems()
	iterelementitems = classmethod(iterelementitems)

	def elementitems(cls, xml=False):
		"""
		Return a list of all (name, class) items of all <pyref class="Element">element</pyref> classes
		in <cls/>. <arg>xml</arg> specifies whether Python or &xml; names
		should be returned.
		"""
		return cls._getcache()[0][xml].items()
	elementitems = classmethod(elementitems)

	def element(cls, name, xml=False):
		"""
		Return the <pyref class="Element">element</pyref> class with the name <arg>name</arg>.
		<arg>xml</arg> specifies whether <arg>name</arg> should be
		treated as a Python or &xml; name. If an element class
		with this name doesn't exist an <class>IllegalElementError</class>
		is raised.
		"""
		try:
			return cls._getcache()[0][xml][name]
		except KeyError:
			raise errors.IllegalElementError(name, xml=xml)
	element = classmethod(element)

	def iterprocinstkeys(cls, xml=False):
		"""
		Return an iterator for iterating over the names of all
		<pyref class="ProcInst">processing instruction</pyref> classes in <cls/>. <arg>xml</arg> specifies
		whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[1][xml].iterkeys()
	iterprocinstkeys = classmethod(iterprocinstkeys)

	def procinstkeys(cls, xml=False):
		"""
		Return a list of the names of all <pyref class="ProcInst">processing instruction</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[1][xml].keys()
	procinstkeys = classmethod(procinstkeys)

	def iterprocinstvalues(cls):
		"""
		Return an iterator for iterating over all <pyref class="ProcInst">processing instruction</pyref> classes in <cls/>.
		"""
		return cls._getcache()[1][False].itervalues()
	iterprocinstvalues = classmethod(iterprocinstvalues)

	def procinstvalues(cls):
		"""
		Return a list of all <pyref class="ProcInst">processing instruction</pyref> classes in <cls/>.
		"""
		return cls._getcache()[1][False].values()
	procinstvalues = classmethod(procinstvalues)

	def iterprocinstitems(cls, xml=False):
		"""
		Return an iterator for iterating over the (name, class) items of all <pyref class="ProcInst">processing instruction</pyref> classes
		in <cls/>. <arg>xml</arg> specifies whether Python or &xml; names
		should be returned.
		"""
		return cls._getcache()[1][xml].iteritems()
	iterprocinstitems = classmethod(iterprocinstitems)

	def procinstitems(cls, xml=False):
		"""
		Return a list of all (name, class) items of all <pyref class="ProcInst">processing instruction</pyref> classes
		in <cls/>. <arg>xml</arg> specifies whether Python or &xml; names
		should be returned.
		"""
		return cls._getcache()[1][xml].items()
	procinstitems = classmethod(procinstitems)

	def procinst(cls, name, xml=False):
		"""
		Return the <pyref class="ProcInst">processing instruction</pyref> class with the name <arg>name</arg>.
		<arg>xml</arg> specifies whether <arg>name</arg> should be
		treated as a Python or &xml; name. If a processing instruction class
		with this name doesn't exist an <class>IllegalProcInstError</class>
		is raised.
		"""
		try:
			return cls._getcache()[1][xml][name]
		except KeyError:
			raise errors.IllegalProcInstError(name, xml=xml)
	procinst = classmethod(procinst)

	def iterentitykeys(cls, xml=False):
		"""
		Return an iterator for iterating over the names of all <pyref class="Entity">entity</pyref>
		and <pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[2][xml].iterkeys()
	iterentitykeys = classmethod(iterentitykeys)

	def entitykeys(cls, xml=False):
		"""
		Return a list of the names of all <pyref class="Entity">entity</pyref> and
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[2][xml].keys()
	entitykeys = classmethod(entitykeys)

	def iterentityvalues(cls):
		"""
		Return an iterator for iterating over all <pyref class="Entity">entity</pyref>
		and <pyref class="CharRef">character reference</pyref> classes in <cls/>.
		"""
		return cls._getcache()[2][False].itervalues()
	iterentityvalues = classmethod(iterentityvalues)

	def entityvalues(cls):
		"""
		Return a list of all <pyref class="Entity">entity</pyref> and
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		"""
		return cls._getcache()[2][False].values()
	entityvalues = classmethod(entityvalues)

	def iterentityitems(cls, xml=False):
		"""
		Return an iterator for iterating over the (name, class) items of all
		<pyref class="Entity">entity</pyref> and <pyref class="CharRef">character reference</pyref>
		classes in <cls/>. <arg>xml</arg> specifies whether Python or &xml; names
		should be returned.
		"""
		return cls._getcache()[2][xml].iteritems()
	iterentityitems = classmethod(iterentityitems)

	def entityitems(cls, xml=False):
		"""
		Return a list of all (name, class) items of all <pyref class="Entity">entity</pyref>
		and <pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[2][xml].items()
	entityitems = classmethod(entityitems)

	def entity(cls, name, xml=False):
		"""
		Return the <pyref class="Entity">entity</pyref> or <pyref class="CharRef">character reference</pyref>
		class with the name <arg>name</arg>. <arg>xml</arg> specifies whether <arg>name</arg> should be
		treated as a Python or &xml; name. If an entity or character reference class
		with this name doesn't exist an <class>IllegalEntityError</class>
		is raised.
		"""
		try:
			return cls._getcache()[2][xml][name]
		except KeyError:
			raise errors.IllegalEntityError(name, xml=xml)
	entity = classmethod(entity)

	def itercharrefkeys(cls, xml=False):
		"""
		Return an iterator for iterating over the names of all
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[3][xml].iterkeys()
	itercharrefkeys = classmethod(itercharrefkeys)

	def charrefkeys(cls, xml=False):
		"""
		Return a list of the names of all <pyref class="CharRef">character reference</pyref>
		classes in <cls/>. <arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[3][xml].keys()
	charrefkeys = classmethod(charrefkeys)

	def itercharrefvalues(cls):
		"""
		Return an iterator for iterating over all <pyref class="CharRef">character reference</pyref> classes in <cls/>.
		"""
		return cls._getcache()[3][False].itervalues()
	itercharrefvalues = classmethod(itercharrefvalues)

	def charrefvalues(cls):
		"""
		Return a list of all <pyref class="CharRef">character reference</pyref> classes in <cls/>.
		"""
		return cls._getcache()[3][False].values()
	charrefvalues = classmethod(charrefvalues)

	def itercharrefitems(cls, xml=False):
		"""
		Return an iterator for iterating over the (name, class) items of all
		<pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names
		should be returned.
		"""
		return cls._getcache()[3][xml].iteritems()
	itercharrefitems = classmethod(itercharrefitems)

	def charrefitems(cls, xml=False):
		"""
		Return a list of all (name, class) items of all <pyref class="CharRef">character reference</pyref> classes in <cls/>.
		<arg>xml</arg> specifies whether Python or &xml; names should be returned.
		"""
		return cls._getcache()[3][xml].items()
	charrefitems = classmethod(charrefitems)

	def charref(cls, name, xml=False):
		"""
		Return the <pyref class="CharRef">character reference</pyref>
		class with the name <arg>name</arg>. If <arg>name</arg> is a number return
		the character reference class defined for this codepoint.
		<arg>xml</arg> specifies whether <arg>name</arg> should be
		treated as a Python or &xml; name. If a character reference class
		with this name or codepoint doesn't exist an <class>IllegalCharRefError</class>
		is raised. If there are multiple character reference class for
		one codepoint an <class>AmbiguousCharRefError</class> will be raise
		"""
		cache = cls._getcache()
		try:
			if isinstance(name, (int, long)):
				charrefs = cache[3][2][name]
				if len(charrefs) > 1:
					raise errors.AmbiguousCharRefError(name, xml)
				return charrefs[0]
			else:
				return cache[3][xml][name]
		except KeyError:
			raise errors.IllegalCharRefError(name, xml=xml)
	charref = classmethod(charref)

	def update(cls, *args, **kwargs):
		"""
		Copies attributes over from all mappings in <arg>args</arg> and from <arg>kwargs</arg>.
		"""
		for mapping in args + (kwargs,):
			for (key, value) in mapping.iteritems():
				if value is not cls and key not in ("__name__", "__dict__"):
					setattr(cls, key, value)
	update = classmethod(update)

	def updateexisting(cls, *args, **kwargs):
		"""
		Copies attributes over from all mappings in <arg>args</arg> and from <arg>kwargs</arg>,
		but only if they exist in <self/>.
		"""
		for mapping in args + (kwargs,):
			for (key, value) in mapping.iteritems():
				if value is not cls and key not in ("__name__", "__dict__") and hasattr(cls, key):
					setattr(cls, key, value)
	updateexisting = classmethod(updateexisting)

	def updatenew(cls, *args, **kwargs):
		"""
		Copies attributes over from all mappings in <arg>args</arg> and from <arg>kwargs</arg>,
		but only if they don't exist in <self/>.
		"""
		args = list(args)
		args.reverse()
		for mapping in [kwargs] + args: # Iterate in reverse order, so the last entry wins
			for (key, value) in mapping.iteritems():
				if value is not cls and key not in ("__name__", "__dict__") and not hasattr(cls, key):
					setattr(cls, key, value)
	updatenew = classmethod(updatenew)

	def makemod(cls, vars=None):
		if vars is not None:
			cls.update(vars)
		name = vars["__name__"]
		if name in sys.modules: # If the name can't be found, the import is probably done by execfile(), in this case we can't communicate back that the module has been replaced
			cls.__originalmodule__ = sys.modules[name] # we have to keep the original module alive, otherwise Python would set all module attribute to None
			sys.modules[name] = cls
		# set the class name to the original module name, otherwise inspect.getmodule() will get problems
		cls.__name__ = name
	makemod = classmethod(makemod)

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
		<par>Create a new <class>Location</class> instance by reading off the current location from
		the <arg>locator</arg>, which is then stored internally. In addition to that the system ID,
		public ID, line number and column number can be overwritten by explicit arguments.</par>
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
		<par>returns a location where the line number is incremented by offset
		(and the column number is reset to 1).</par>
		"""
		if offset==0:
			return self
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


import presenters, publishers, cssparsers, converters, errors, options, utils, helpers
