# -*- coding: utf-8 -*-

## Copyright 1999-2012 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
This module contains all the central XML tree classes, the namespace classes,
exception and warning classes and a few helper classes and functions.
"""


__docformat__ = "reStructuredText"


import sys, os, random, copy, warnings, pickle, threading, weakref, types, codecs

import cssutils

from ll import misc, url as url_, xml_codec

try:
	import astyle
except ImportError:
	astyle = None

__docformat__ = "reStructuredText"


xml_xmlns = "http://www.w3.org/XML/1998/namespace"


###
### helpers
###

def tonode(value):
	"""
	convert :var:`value` to an XIST :class:`Node`.

	If :var:`value` is a tuple or list, it will be (recursively) converted to a
	:class:`Frag`. Integers, strings, etc. will be converted to a :class:`Text`.
	If :var:`value` is a :class:`Node` already, it will be returned unchanged.
	In the case of :const:`None` the XIST Null (:data:`ll.xist.xsc.Null`) will be
	returned. If :var:`value` is iterable, a :class:`Frag` will be generated
	from the items. Anything else will raise an :exc:`IllegalObjectError`
	exception.
	"""
	if isinstance(value, Node):
		if isinstance(value, Attrs):
			raise IllegalObjectError(value)
		# we don't have to turn an Attr into a Frag, because this will be done once the Attr is put back into the tree
		return value
	elif isinstance(value, (str, int, float)):
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
			value = iter(value)
		except TypeError:
			pass
		else:
			return Frag(*list(value))
	raise IllegalObjectError(value) # none of the above => bail out


class ThreadLocalNodeHander(threading.local):
	handler = None

threadlocalnodehandler = ThreadLocalNodeHander()


class build(object):
	"""
	A :class:`build` object can be used as a ``with`` block handler to create a
	new XIST tree::

		with xsc.build():
			with html.ul() as e:
				+html.li("gurk")
				+html.li("hurz")
	"""

	def __init__(self):
		self.stack = []

	def __enter__(self):
		self.prev = threadlocalnodehandler.handler
		threadlocalnodehandler.handler = self

	def __exit__(self, type, value, traceback):
		threadlocalnodehandler.handler = self.prev
		del self.prev

	def enter(self, node):
		if self.stack:
			self.stack[-1](node)
		self.stack.append(node)
		return node

	def exit(self):
		self.stack.pop()

	def add(self, *args, **kwargs):
		self.stack[-1](*args, **kwargs)


class addattr(object):
	"""
	An :class:`addattr` object can be used as a ``with`` block handler to modify
	an attribute of an element::

		with xsc.build():
			with html.div() as e:
				with xsc.addattr("align"):
					+xsc.Text("right")
	"""

	def __init__(self, attrname):
		"""
		Create an :class:`addattr` object for adding to the attribute named
		:var:`attrname` (which can be the Python name of an attribute or an
		attribute class).
		"""
		self.attr = threadlocalnodehandler.handler.stack[-1][attrname]

	def __enter__(self):
		threadlocalnodehandler.handler.stack.append(self.attr)
		return self.attr

	def __exit__(self, type, value, traceback):
		threadlocalnodehandler.handler.stack.pop()

	def add(self, *args):
		self.attr(*args)


def add(*args, **kwargs):
	"""
	:func:`add` appends items in :var:`args` and sets attributes in
	:var:`kwargs` in the currenly active node in the ``with`` stack.
	"""
	threadlocalnodehandler.handler.add(*args, **kwargs)


###
### Conversion context
###

class Context(object):
	"""
	This is an empty class that can be used by the :meth:`convert` method to
	hold element or namespace specific data during the :meth:`convert` call.
	The method :meth:`Converter.__getitem__` will return a unique instance of
	this class.
	"""
	__fullname__ = "Context"


###
### Exceptions and warnings
###

class Error(Exception):
	"""
	Base class for all XIST exceptions
	"""
	pass


class Warning(UserWarning):
	"""
	Base class for all warning exceptions (i.e. those that won't result in a
	program termination.)
	"""
	pass


class IllegalAttrValueWarning(Warning):
	"""
	Warning that is issued when an attribute has an illegal value when parsing
	or publishing.
	"""

	def __init__(self, attr):
		self.attr = attr

	def __str__(self):
		attr = self.attr
		return "Attribute value {!r} not allowed for {}".format(str(attr), attr._str(fullname=True, xml=False, decorate=False))


class RequiredAttrMissingWarning(Warning):
	"""
	Warning that is issued when a required attribute is missing during parsing
	or publishing.
	"""

	def __init__(self, attrs, reqattrs):
		self.attrs = attrs
		self.reqattrs = reqattrs

	def __str__(self):
		return "Required attribute{} {} missing in {}".format(("s" if len(self.reqattrs) > 1 else ""), ", ".join(repr(attr) for attr in self.reqattrs), self.attrs._str(fullname=True, xml=False, decorate=False))


class IllegalPrefixError(Error, LookupError):
	"""
	Exception that is raised when a namespace prefix is undefined.
	"""
	def __init__(self, prefix):
		self.prefix = prefix

	def __str__(self):
		return "namespace prefix {} is undefined".format(self.prefix)


class IllegalElementError(Error, LookupError):
	"""
	Exception that is raised when an illegal element class is requested
	"""

	def __init__(self, name, xmlns, xml=False):
		self.name = name
		self.xmlns = xmlns
		self.xml = xml

	def __str__(self):
		xmlns = self.xmlns
		if isinstance(xmlns, (list, tuple)):
			if len(xmlns) > 1:
				return "no element with {} name {} in namespaces {}".format("XML" if self.xml else "Python", self.name, ", ".join(nsclark(xmlns) for xmlns in xmlns))
			xmlns = xmlns[0]
		return "no element with {} name {}{}".format("XML" if self.xml else "Python", nsclark(xmlns), self.name)


class IllegalProcInstError(Error, LookupError):
	"""
	Exception that is raised when an illegal procinst class is requested
	"""

	def __init__(self, name, xml=False):
		self.name = name
		self.xml = xml

	def __str__(self):
		return "no procinst with {} name {}".format("XML" if self.xml else "Python", self.name)


class IllegalEntityError(Error, LookupError):
	"""
	Exception that is raised when an illegal entity class is requested
	"""

	def __init__(self, name, xml=False):
		self.name = name
		self.xml = xml

	def __str__(self):
		return "no entity with {} name {}".format("XML" if self.xml else "Python", self.name)


class IllegalCharRefError(Error, LookupError):
	"""
	Exception that is raised when an illegal charref class is requested
	"""

	def __init__(self, name, xml=False):
		self.name = name
		self.xml = xml

	def __str__(self):
		if isinstance(self.name, int):
			return "no charref with codepoint {}".format(self.name)
		return "no charref with {} name {}".format("XML" if self.xml else "Python", self.name)


class IllegalAttrError(Error, LookupError):
	"""
	Exception that is raised when an illegal attribute is requested.
	"""

	def __init__(self, name, cls, xml=False):
		self.name = name
		self.cls = cls
		self.xml = xml

	def __str__(self):
		if isinstance(self.name, str):
			return "no local attribute with {} name {!r} in {!r}".format("XML" if self.xml else "Python", self.name, self.cls)
		elif self.name.xmlns is None:
			return "no local attribute with class {!r} in {!r}".format(self.name, self.cls)
		else:
			return "no global attribute with class {!r}".format(self.name)


class MultipleRootsError(Error):
	def __str__(self):
		return "can't add namespace attributes: XML tree has multiple roots"


class ElementNestingError(Error):
	"""
	Exception that is raised when an element has an illegal nesting
	(e.g. ``<a><b></a></b>``)
	"""

	def __init__(self, expectedelement, foundelement):
		self.expectedelement = expectedelement
		self.foundelement = foundelement

	def __str__(self):
		return "mismatched element nesting (close tag for {} expected; close tag for {} found)".format(self.expectedelement._str(fullname=True, xml=False, decorate=True), self.foundelement._str(fullname=True, xml=False, decorate=True))


class FileNotFoundWarning(Warning):
	"""
	Warning that is issued when a file can't be found.
	"""
	def __init__(self, message, filename, exc):
		Warning.__init__(self, message, filename, exc)
		self.message = message
		self.filename = filename
		self.exc = exc

	def __str__(self):
		return "{0.message}: {0.filename!r} not found ({0.exc})".format(self)


class IllegalObjectError(Error, TypeError):
	"""
	Exception that is raised when an XIST constructor gets passed an
	unconvertable object.
	"""

	def __init__(self, object):
		self.object = object

	def __str__(self):
		return "can't convert object {!r} of type {} to an XIST node".format(self.object, type(self.object).__name__)


class IllegalCommentContentWarning(Warning):
	"""
	Warning that is issued when there is an illegal comment, i.e. one containing
	``--`` or ending in ``-``. (This can only happen when the comment was created
	by code, not when parsed from an XML file.)
	"""

	def __init__(self, comment):
		self.comment = comment

	def __str__(self):
		return "comment with content {!r} is illegal, as it contains '--' or ends in '-'".format(self.comment.content)


class IllegalProcInstFormatError(Error):
	"""
	Exception that is raised when there is an illegal processing instruction,
	i.e. one containing ``?>``. (This can only happen when the processing
	instruction was created by code, not when parsed from an XML file.)
	"""

	def __init__(self, procinst):
		self.procinst = procinst

	def __str__(self):
		return "processing instruction with content {!r} is illegal, as it contains '?>'".format(self.procinst.content)


###
### Context containing state during :meth:`convert` calls
###

class ConverterState(object):
	def __init__(self, node, root, mode, stage, target, lang, makeaction, makeproject):
		self.node = node
		self.root = root
		self.mode = mode
		self.stage = stage
		if target is None:
			from ll.xist.ns import html
			target = html
		self.target = target
		self.lang = lang
		self.makeaction = makeaction
		self.makeproject = makeproject


class Converter(object):
	"""
	An instance of this class is passed around in calls to the :meth:`convert`
	method. A :class:`Converter` object can be used when some element needs to
	keep state across a nested :meth:`convert` call. A typical example are nested
	chapter/subchapter elements with automatic numbering. For an example see the
	element :class:`ll.xist.ns.doc.section`.
	"""

	def __init__(self, node=None, root=None, mode=None, stage=None, target=None, lang=None, makeaction=None, makeproject=None):
		"""
		Create a :class:`Converter`. Arguments are used to initialize the
		:class:`Converter` properties of the same name.
		"""
		self.states = [ ConverterState(node=node, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, makeproject=makeproject) ]
		self.contexts = {}

	class node(misc.propclass):
		"""
		The root node for which conversion has been called. This is automatically
		set by the :meth:`conv` method of :class:`Node` objects.
		"""
		def __get__(self):
			return self.states[-1].node

		def __set__(self, node):
			self.states[-1].node = node

		def __delete__(self):
			self.states[-1].node = None

	class root(misc.propclass):
		"""
		The root URL for the conversion. Resolving URLs during the conversion
		process should be done relative to :prop:`root`.
		"""
		def __get__(self):
			return self.states[-1].root

		def __set__(self, root):
			self.states[-1].root = root

		def __delete__(self):
			self.states[-1].root = None

	class mode(misc.propclass):
		"""
		The conversion mode. This corresponds directly to the mode in XSLT.
		The default is :const:`None`.
		"""
		def __get__(self):
			return self.states[-1].mode

		def __set__(self, mode):
			self.states[-1].mode = mode

		def __delete__(self):
			self.states[-1].mode = None

	class stage(misc.propclass):
		"""
		If your conversion is done in multiple steps or stages you can use this
		property to specify in which stage the conversion process currently is.
		The default is :const:`"deliver"`.
		"""
		def __get__(self):
			if self.states[-1].stage is None:
				return "deliver"
			else:
				return self.states[-1].stage

		def __set__(self, stage):
			self.states[-1].stage = stage

		def __delete__(self):
			self.states[-1].stage = None

	class target(misc.propclass):
		"""
		Specifies the conversion target. This must be a namespace module or
		similar object.
		"""
		def __get__(self):
			return self.states[-1].target

		def __set__(self, target):
			self.states[-1].target = target

		def __delete__(self):
			self.states[-1].target = None

	class lang(misc.propclass):
		"""
		The target language. The default is :const:`None`.
		"""
		def __get__(self):
			return self.states[-1].lang

		def __set__(self, lang):
			self.states[-1].lang = lang

		def __delete__(self):
			self.states[-1].lang = None

	class makeaction(misc.propclass):
		"""
		If an XIST conversion is done by an :class:`ll.make.XISTConvertAction`
		this property will hold the action object during that conversion. If
		you're not using the :mod:`ll.make` module you can simply ignore this
		property. The default is :const:`None`.
		"""
		def __get__(self):
			return self.states[-1].makeaction

		def __set__(self, makeaction):
			self.states[-1].makeaction = makeaction

		def __delete__(self):
			self.states[-1].makeaction = None

	class makeproject(misc.propclass):
		"""
		If an XIST conversion is done by an :class:`ll.make.XISTConvertAction`
		this property will hold the :class:`Project` object during that conversion.
		If you're not using the :mod:`ll.make` module you can simply ignore this
		property.
		"""
		def __get__(self):
			return self.states[-1].makeproject

		def __set__(self, makeproject):
			self.states[-1].makeproject = makeproject

		def __delete__(self):
			self.states[-1].makeproject = None

	def push(self, node=None, root=None, mode=None, stage=None, target=None, lang=None, makeaction=None, makeproject=None):
		self.lastnode = None
		if node is None:
			node = self.node
		if root is None:
			root = self.root
		if mode is None:
			mode = self.mode
		if stage is None:
			stage = self.stage
		if target is None:
			target = self.target
		if lang is None:
			lang = self.lang
		if makeaction is None:
			makeaction = self.makeaction
		if makeproject is None:
			makeproject = self.makeproject
		self.states.append(ConverterState(node=node, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, makeproject=makeproject))

	def pop(self):
		if len(self.states) == 1:
			raise IndexError("can't pop last state")
		state = self.states.pop()
		self.lastnode = state.node
		return state

	def __getitem__(self, obj):
		"""
		Return a context object for :var:`obj`, which should be an
		:class:`ll.xist.xsc.Node` instance or subclass. Each of these classes
		that defines its own :class:`Context` class gets a unique instance of
		this class. This instance will be created on the first access and the
		element can store information there that needs to be available across
		calls to :meth:`convert`.
		"""
		contextclass = obj.Context
		# don't use :meth:`setdefault`, as constructing the context object might involve some overhead
		try:
			return self.contexts[contextclass]
		except KeyError:
			context = contextclass()
			self.contexts[contextclass] = context
			return context


###
### Publisher for serializing XML trees to strings
###

class Publisher(object):
	"""
	A :class:`Publisher` object is used for serializing an XIST tree into a byte
	sequence.
	"""

	def __init__(self, encoding=None, xhtml=1, validate=True, prefixes={}, prefixdefault=False, hidexmlns=(), showxmlns=()):
		"""
		Create a publisher. Arguments have the following meaning:

		:var:`encoding` : string or :const:`None`
			Specifies the encoding to be used for the byte sequence. If
			:const:`None` is used the encoding in the XML declaration will be used.
			If there is no XML declaration, UTF-8 will be used.

		:var:`xhtml` : int
			With the parameter :var:`xhtml` you can specify if you want HTML
			output:

			HTML (``xhtml==0``)
				Elements with a empty content model will be published as ``<foo>``.

			HTML browser compatible XML (``xhtml==1``)
				Elements with an empty content model will be published as ``<foo />``
				and others that just happen to be empty as ``<foo></foo>``. This is
				the default.

			Pure XML (``xhtml==2``)
				All empty elements will be published as ``<foo/>``.

		:var:`validate` : bool
			Specifies whether validation should be done before publishing.

		:var:`prefixes` : mapping
			A dictionary that specifies which namespace prefixes should be used
			for publishing. Keys in the dictionary are either namespace names or
			objects that have an ``xmlns`` attribute which is the namespace name.
			Values can be:

			:const:`False`
				Treat elements in this namespace as if they are not in any
				namespace (if global attributes from this namespace are encountered,
				a non-empty prefix will be used nonetheless).

			:const:`None`
				Treat the namespace as the default namespaces (i.e. use unprefixed
				element names). Global attributes will again result in a non-empty
				prefix.

			:const:`True`
				The publisher uses a unique non-empty prefix for this namespace.

			A string
				Use this prefix for the namespace.

		:var:`prefixdefault` : string or :const:`None`
			If an element or attribute is encountered whose namespace name is not
			in :var:`prefixes` :var:`prefixdefault` is used as the fallback.

		:var:`hidexmlns` : list or set
			:var:`hidexmlns` can be a list or set that contains namespace names
			for which no ``xmlns`` attributes should be published. (This can be
			used to hide the namespace declarations for e.g. Java taglibs.)

		:var:`showxmlns` : list or set
			:var:`showxmlns` can be a list or set that contains namespace names
			for which ``xmlns`` attributes *will* be published, even if there are
			no elements from this namespace in the tree.
		"""
		self.base = None
		self.encoding = encoding
		self.encoder = None
		self.xhtml = xhtml
		self.validate = validate
		self.prefixes = {nsname(xmlns): prefix for (xmlns, prefix) in prefixes.items()}
		self.prefixdefault = prefixdefault
		self.hidexmlns = {nsname(xmlns) for xmlns in hidexmlns}
		self.showxmlns = {nsname(xmlns) for xmlns in showxmlns}
		self._ns2prefix = {}
		self._prefix2ns = {}

	def encode(self, text):
		"""
		Encode :var:`text` with the encoding and error handling currently active
		and return the resulting byte string.
		"""
		return self.encoder.encode(text)

	def encodetext(self, text):
		"""
		Encode :var:`test` as text data. :var:`text` must be a :class:`unicode`
		object. The publisher will apply the configured encoding, error handling
		and the current text filter (which escapes characters that can't appear
		in text data (like ``<`` etc.)) and returns the resulting :class:`str`
		object.
		"""
		self.encoder.errors = self.__errors[-1]
		result = self.encoder.encode(self.__textfilters[-1](text))
		self.encoder.errors = "strict"
		return result

	def pushtextfilter(self, filter):
		"""
		Pushes a new text filter function ontp the text filter stack. This
		function is responsible for escaping characters that can't appear in text
		data (like ``<``)). This is used to switch on escaping of ``"`` inside
		attribute values.
		"""
		self.__textfilters.append(filter)

	def poptextfilter(self):
		"""
		Pops the current text filter function from the stack.
		"""
		self.__textfilters.pop()

	def pusherrors(self, errors):
		"""
		Pushes a new error handling scheme onto the error handling stack.
		"""
		self.__errors.append(errors)

	def poperrors(self):
		"""
		Pop the current error handling scheme from the error handling stack.
		"""
		self.__errors.pop()

	def _newprefix(self):
		prefix = "ns"
		suffix = 2
		while True:
			if prefix not in self._prefix2ns:
				return prefix
			prefix = "ns{}".format(suffix)
			suffix += 1

	def getencoding(self):
		"""
		Return the encoding currently in effect.
		"""
		if self.encoding is not None:
			# The encoding has been prescribed, so this *will* be used.
			return self.encoding
		elif self.encoder is not None:
			# The encoding is determined by the XML declaration in the output,
			# so use that if it has been determined already. If the encoder hasn't
			# determined the encoding yet (e.g. because nothing has been output
			# yet) use utf-8 (which will be what the encoder eventually will decide
			# to use too). Note that this will not work if nothing has been output
			# yet, but later an XML declaration (using a different encoding) will
			# be output, but this shouldn't happen anyway.
			return self.encoder.encoding or "utf-8"
		return "utf-8"

	def getnamespaceprefix(self, xmlns):
		"""
		Return (and register) a namespace prefix for the namespace name
		:var:`xmlns`. This honors the namespace configuration from ``self.prefixes``
		and ``self.prefixdefault``. Furthermore the same prefix will be returned
		from now on (except when the empty prefix becomes invalid once global
		attributes are encountered)
		"""
		if xmlns is None:
			return None

		if xmlns == xml_xmlns: # We don't need a namespace mapping for the xml namespace
			prefix = "xml"
		else:
			try:
				prefix = self._ns2prefix[xmlns]
			except KeyError: # A namespace we haven't encountered yet
				prefix = self.prefixes.get(xmlns, self.prefixdefault)
				if prefix is True:
					prefix = self._newprefix()
				if prefix is not False:
					try:
						oldxmlns = self._prefix2ns[prefix]
					except KeyError:
						pass
					else:
						# If this prefix has already been used for another namespace, we need a new one
						if oldxmlns != xmlns:
							prefix = self._newprefix()
					self._ns2prefix[xmlns] = prefix
					self._prefix2ns[prefix] = xmlns
		return prefix

	def getobjectprefix(self, object):
		"""
		Get and register a namespace prefix for the namespace :var:`object` lives
		in (specified by the :attr:`xmlns` attribute of :var:`object`). Similar
		to :meth:`getnamespaceprefix` this honors the namespace configuration from
		``self.prefixes`` and ``self.prefixdefault`` (except when a global
		attribute requires a non-empty prefix).
		"""
		xmlns = getattr(object, "xmlns")
		if xmlns is None:
			return None

		if xmlns == xml_xmlns: # We don't need a namespace mapping for the xml namespace
			prefix = "xml"
		else:
			emptyok = isinstance(object, Element) # If it's e.g. a procinst assume we need a non-empty prefix
			try:
				prefix = self._ns2prefix[xmlns]
			except KeyError: # A namespace we haven't encountered yet
				prefix = self.prefixes.get(xmlns, self.prefixdefault)
				# global attributes always require prefixed names
				if prefix is True or ((prefix is None or prefix is False) and not emptyok):
					prefix = self._newprefix()
				if prefix is not False:
					try:
						oldxmlns = self._prefix2ns[prefix]
					except KeyError:
						pass
					else:
						# If this prefix has already been used for another namespace, we need a new one
						if oldxmlns != xmlns:
							prefix = self._newprefix()
					self._ns2prefix[xmlns] = prefix
					self._prefix2ns[prefix] = xmlns
			else:
				# We can't use the unprefixed names for global attributes
				if (prefix is None or prefix is False) and not emptyok:
					# Use a new one
					prefix = self._newprefix()
					self._ns2prefix[xmlns] = prefix
					self._prefix2ns[prefix] = xmlns
		return prefix

	def iterbytes(self, node, base=None):
		"""
		Output the node :var:`node`. This method is a generator that will yield
		the resulting XML byte sequence in fragments.
		"""
		self._ns2prefix.clear()
		self._prefix2ns.clear()
		# iterate through every node in the tree
		for n in node.walknodes(Node):
			self.getobjectprefix(n)
		# Add the prefixes forced by ``self.showxmlns``
		for xmlns in self.showxmlns:
			self.getnamespaceprefix(xmlns)

		# Do we have to publish xmlns attributes?
		self._publishxmlns = False
		if self._ns2prefix:
			# Determine if we have multiple roots
			if isinstance(node, Frag):
				count = 0
				for child in node:
					if isinstance(node, Element) and node.xmlns not in self.hidexmlns:
						count += 1
				if count > 1:
					raise MultipleRootsError()
			self._publishxmlns = True

		self.inattr = 0
		self.__textfilters = [ misc.xmlescape_text ]

		self.__errors = [ "xmlcharrefreplace" ]

		self.base = url_.URL(base)
		self.node = node

		self.encoder = codecs.getincrementalencoder("xml")(encoding=self.encoding)

		for part in self.node.publish(self):
			if part:
				yield part
		rest = self.encoder.encode("", True) # finish encoding and flush buffers
		if rest:
			yield rest

		self.inattr = 0
		self.__textfilters = [ misc.xmlescape_text ]

		self.__errors = [ "xmlcharrefreplace" ]

		self._publishxmlns = False
		self._ns2prefix.clear()
		self._prefix2ns.clear()

		self.encoder = None

	def bytes(self, node, base=None):
		"""
		Return a byte string in XML format for the XIST node :var:`node`.
		"""
		return b"".join(self.iterbytes(node, base))

	def iterstring(self, node, base=None):
		"""
		A generator that will produce a serialized string of :var:`node`.
		"""
		decoder = codecs.getincrementaldecoder("xml")(encoding=self.encoding)
		for part in self.iterbytes(node, base):
			part = decoder.decode(part, False)
			if part:
				yield part
		part = decoder.decode(b"", True)
		if part:
			yield part

	def string(self, node, base=None):
		"""
		Return a unicode string for :var:`node`.
		"""
		decoder = codecs.getdecoder("xml")
		result = self.bytes(node, base)
		return decoder(result, encoding=self.encoding)[0]

	def write(self, stream, node, base=None):
		"""
		Write :var:`node` to the file-like object :var:`stream` (which must
		provide a :meth:`write` method).
		"""
		for part in self.iterbytes(node, base):
			stream.write(part)


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
		return "<class {0.__module__}:{0.__fullname__} at {1:#x}>".format(self, id(self))

	def __truediv__(self, other):
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
		return xfind.IsInstanceSelector(self)[index]

	def __invert__(self):
		from ll.xist import xfind
		return ~xfind.IsInstanceSelector(self)


class Node(object, metaclass=_Node_Meta):
	"""
	base class for nodes in the document tree. Derived classes may
	overwrite :meth:`convert` or :meth:`publish`.
	"""

	# location of this node in the XML file (will be hidden in derived classes,
	# but is specified here, so that no special tests are required. In derived
	# classes this will be set by the parser)
	startloc = None
	endloc = None

	# Subclasses relevant for parsing (i.e. Element, ProcInst, Entity and CharRef)
	# have an additional class attribute named register. This attribute may have
	# two values:
	# :const:`False`: Don't register for parsing.
	# :const:`True`:  Use for parsing.
	# If register is not set it defaults to :const:`True`

	Context = Context

	prettyindentbefore = 0
	prettyindentafter = 0

	def __repr__(self):
		return "<{0.__module__}:{0.__fullname__} object at {1:#x}>".format(self, id(self))

	def __ne__(self, other):
		return not self == other

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
		threadlocalnodehandler.handler.add(self)

	def __truediv__(self, other):
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
		return a clone of :var:`self`. Compared to :meth:`deepcopy` :meth:`clone`
		will create multiple instances of objects that can be found in the tree
		more than once. :meth:`clone` can't clone trees that contain cycles.
		"""
		return self

	def copy(self):
		"""
		Return a shallow copy of :var:`self`.
		"""
		return self.__copy__()

	def __copy__(self):
		return self

	def deepcopy(self):
		"""
		Return a deep copy of :var:`self`.
		"""
		return self.__deepcopy__()

	def __deepcopy__(self, memo=None):
		return self

	@misc.notimplemented
	def present(self, presenter):
		"""
		:meth:`present` is used as a central dispatch method for the
		presenter classes. Normally it is not called by the user, but internally
		by the presenter. The user should use the appropriate presenter class
		directly.
		"""
		# Subclasses of ``Node`` implement this method by calling the appropriate
		# ``present*`` method in the publisher (i.e. double dispatch)

	def conv(self, converter=None, root=None, mode=None, stage=None, target=None, lang=None, function=None, makeaction=None, makeproject=None):
		"""
		Convenience method for calling :meth:`convert`.

		:meth:`conv` will automatically set ``:var:`converter`.node`` to :var:`self`
		to remember the "document root node" for which :meth:`conv` has been
		called, this means that you should not call :meth:`conv` in any of the
		recursive calls, as you would loose this information. Call :meth:`convert`
		directly instead.
		"""
		if converter is None:
			converter = Converter(node=self, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, makeproject=makeproject)
			return self.convert(converter)
		else:
			converter.push(node=self, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, makeproject=makeproject)
			node = self.convert(converter)
			converter.pop()
			return node

	@misc.notimplemented
	def convert(self, converter):
		"""
		implementation of the conversion method. When you define your own element
		classes you have to overwrite this method and implement the desired
		conversion.

		This method must return an instance of :class:`Node`. It may *not* change
		:var:`self`.
		"""

	@misc.notimplemented
	def __str__(self):
		"""
		Return the character content of :var:`self` as a string. This means that
		comments and processing instructions will be filtered out.
		For elements you'll get the element content.

		:meth:`__str__` can be used everywhere where a plain string
		representation of the node is required.
		"""
		pass

	def __int__(self):
		"""
		Convert the character content of :var:`self` to an :class:`int`.
		"""
		return int(str(self))

	def asFloat(self, decimal=".", ignore=""):
		"""
		Convert the character content of :var:`self` to an :class:`float`.
		:var:`decimal` specifies which decimal separator is used in the value
		(e.g. ``"."`` (the default) or ``","``). :var:`ignore` specifies which
		characters will be ignored.
		"""
		s = str(self)
		for c in ignore:
			s = s.replace(c, "")
		if decimal != ".":
			s = s.replace(decimal, ".")
		return float(s)

	def __float__(self):
		"""
		Convert the character content of :var:`self` to an :class:`float`.
		"""
		return self.asFloat()

	def __complex__(self):
		"""
		Convert the character content of :var:`self` to an :class:`complex`.
		"""
		return complex(str(self))

	def parsed(self, parser, event):
		"""
		This method will be called by the parser :var:`parser` once after
		:var:`self` is created by the parser (This is used e.g. by
		:class:`URLAttr` to incorporate the base URL into the attribute).

		:var:`event` is the parser event that initiated the call.
		"""

	def checkvalid(self):
		"""
		This method will be called when parsing or publishing to check whether
		:var`self` is valid.

		If :var:`self` is found to be invalid a warning should be issued through
		the Python warning framework.
		"""

	@misc.notimplemented
	def publish(self, publisher):
		"""
		Generate unicode strings for the node. :var:`publisher` must be an
		instance of :class:`ll.xist.xsc.Publisher`.

		The encoding and xhtml specification are taken from the :var:`publisher`.
		"""

	def iterbytes(self, base=None, publisher=None, **publishargs):
		"""
		A generator that will produce this node as a serialized byte string.

		For the possible parameters see the :class:`ll.xist.xsc.Publisher`
		constructor.
		"""
		if publisher is None:
			publisher = Publisher(**publishargs)

		return publisher.iterbytes(self, base) # return a generator-iterator

	def bytes(self, base=None, publisher=None, **publishargs):
		"""
		Return :var:`self` as a serialized byte string.

		For the possible parameters see the :class:`ll.xist.xsc.Publisher`
		constructor.
		"""
		if publisher is None:
			publisher = Publisher(**publishargs)

		return publisher.bytes(self, base)

	def iterstring(self, base=None, publisher=None, **publishargs):
		"""
		A generator that will produce a serialized byte string of :var:`self`.

		For the possible parameters see the :class:`ll.xist.xsc.Publisher`
		constructor.
		"""
		if publisher is None:
			publisher = Publisher(**publishargs)

		return publisher.iterstring(self, base) # return a generator-iterator

	def string(self, base=None, publisher=None, **publishargs):
		"""
		Return a serialized unicode string for :var:`self`.

		For the possible parameters see the :class:`ll.xist.xsc.Publisher`
		constructor.
		"""
		if publisher is None:
			publisher = Publisher(**publishargs)
		return publisher.string(self, base)

	def write(self, stream, base=None, publisher=None, **publishargs):
		"""
		Write :var:`self` to the file-like object :var:`stream` (which must provide
		a :meth:`write` method).

		For the rest of the parameters see the :class:`ll.xist.xsc.Publisher`
		constructor.
		"""
		if publisher is None:
			publisher = Publisher(**publishargs)
		return publisher.write(stream, self, base)

	def walk(self, walkfilter=None):
		"""
		Return an iterator for traversing the tree rooted at :var:`self`.

		:var:`walkfilter` is used for specifying whether or not a node should be
		yielded and when the children of this node should be traversed. If
		:var:`walkfilter` is callable, it will be called for each node visited
		during the traversal. A path (i.e. a list of all nodes from the root to
		the current node) will be passed to the filter on each call and the
		filter must return a sequence of "node handling options". If
		:var:`walkfilter` is not callable, it must be a sequence of node
		handling options that will be used for all visited nodes.

		Entries in this returned sequence can be the following:

		:const:`True`
			This tells :meth:`walk` to yield this node from the iterator.

		:const:`False`
			Don't yield this node from the iterator.

		:const:`xfind.enterattrs`
			This is a global constant in :mod:`ll.xist.xfind` and tells :meth:`walk`
			to traverse the attributes of this node (if it's an :class:`Element`,
			otherwise this option will be ignored).

		:const:`xfind.entercontent`
			This is a global constant in :mod:`ll.xist.xfind` and tells :meth:`walk`
			to traverse the child nodes of this node (if it's an :class:`Element`,
			otherwise this option will be ignored).

		These options will be executed in the order they are specified in the
		sequence, so to get a top down traversal of a tree (without entering
		attributes), ``(True, xfind.entercontent)`` can be used. For a bottom up
		traversal ``(xfind.entercontent, True)`` can be used.

		Each item produced by the iterator is a path list. :meth:`walk` reuses
		this list, so you can't rely on the value of the list being the same
		across calls to :meth:`next`.
		"""
		from ll.xist import xfind
		return xfind.makewalkfilter(walkfilter).walk(self)

	def walknodes(self, walkfilter=None):
		"""
		Return an iterator for traversing the tree. :var:`filter` works the same
		as the :var:`walkfilter` argument for :meth:`walk`. The items produced
		by the iterator are the nodes themselves.
		"""
		from ll.xist import xfind
		return xfind.makewalkfilter(walkfilter).walknodes(self)

	def walkpaths(self, walkfilter=None):
		"""
		Return an iterator for traversing the tree. :var:`walkfilter` works
		the same as the :var:`walkfilter` argument for :meth:`walk`. The items
		produced by the iterator are copies of the path.
		"""
		from ll.xist import xfind
		return xfind.makewalkfilter(walkfilter).walkpaths(self)

	def compacted(self):
		"""
		Return a version of :var:`self`, where textnodes or character references
		that contain only linefeeds are removed, i.e. potentially useless
		whitespace is removed.
		"""
		return self

	def _decoratenode(self, node):
		# Decorate the :class:`Node` :var:`node` with the same location
		# information as :var:`self`.

		node.startloc = self.startloc
		node.endloc = self.endloc
		return node

	def mapped(self, function, converter=None, **converterargs):
		"""
		Return the node mapped through the function :var:`function`. This call
		works recursively (for :class:`Frag` and :class:`Element`).

		When you want an unmodified node you simply can return :var:`self`.
		:meth:`mapped` will make a copy of it and fill the content recursively.
		Note that element attributes will not be mapped. When you return a
		different node from :func:`function` this node will be incorporated
		into the result as-is.
		"""
		if converter is None:
			converter = Converter(**converterargs)
		node = function(self, converter)
		assert isinstance(node, Node), "the mapped method returned the illegal object {!r} (type {!r}) when mapping {!r}".format(node, type(node), self)
		return node

	def normalized(self):
		"""
		Return a normalized version of :var:`self`, which means that consecutive
		:class:`Text` nodes are merged.
		"""
		return self

	def __mul__(self, factor):
		"""
		Return a :class:`Frag` with :var:`factor` times the node as an entry.
		Note that the node will not be copied, i.e. this is a
		"shallow :meth:`__mul__`".
		"""
		return Frag(*factor*[self])

	def __rmul__(self, factor):
		"""
		Return a :class:`Frag` with :var:`factor` times the node as an entry.
		"""
		return Frag(*[self]*factor)

	def pretty(self, level=0, indent="\t"):
		"""
		Return a prettyfied version of :var:`self`, i.e. one with properly nested
		and indented tags (as far as possible). If an element has mixed content
		(i.e. :class:`Text` and non-:class:`Text` nodes) the content will be
		returned as is.

		Note that whitespace will prevent pretty printing too, so you might want
		to call :meth:`normalized` and :meth:`compact` before calling
		:meth:`pretty` to remove whitespace.
		"""
		if level:
			return Frag(indent*level, self)
		else:
			return self


class CharacterData(Node):
	"""
	Base class for XML character data (:class:`Text`, :class:`ProcInst`,
	:class:`Comment` and :class:`DocType`).

	(Provides nearly the same functionality as :class:`UserString`,
	but omits a few methods.)
	"""
	__slots__ = ("_content",)

	def __init__(self, *content):
		self._content = "".join(str(x) for x in content)

	def _repr_pretty_(self, p, cycle):
		p.text("{}.{}({!r})".format(self.__class__.__module__, self.__class__.__name__, self.content))

	def __getstate__(self):
		return self._content

	def __setstate__(self, content):
		self._content = content

	class content(misc.propclass):
		"""
		The text content of the node as a :class:`str` object.
		"""
		def __get__(self):
			return self._content

	def __hash__(self):
		return self._content.__hash__()

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self._content == other._content

	def __lt__(self, other):
		if not issubclass(self.__class__, other.__class__) and not issubclass(other.__class__, self.__class__):
			raise TypeError("unorderable types")
		return self._content < other._content

	def __le__(self, other):
		if not issubclass(self.__class__, other.__class__) and not issubclass(other.__class__, self.__class__):
			raise TypeError("unorderable types")
		return self._content <= other._content

	def __gt__(self, other):
		if not issubclass(self.__class__, other.__class__) and not issubclass(other.__class__, self.__class__):
			raise TypeError("unorderable types")
		return self._content > other._content

	def __ge__(self, other):
		if not issubclass(self.__class__, other.__class__) and not issubclass(other.__class__, self.__class__):
			raise TypeError("unorderable types")
		return self._content >= other._content

	def __len__(self):
		return self._content.__len__()

	def __getitem__(self, index):
		return self.__class__(self._content.__getitem__(index))

	def __add__(self, other):
		return self.__class__(self._content + other)

	def __radd__(self, other):
		return self.__class__(str(other) + self._content)

	def __mul__(self, n):
		return self.__class__(n * self._content)

	def __rmul__(self, n):
		return self.__class__(n * self._content)

	def capitalize(self):
		return self.__class__(self._content.capitalize())

	def center(self, width):
		return self.__class__(self._content.center(width))

	def count(self, sub, start=0, end=sys.maxsize):
		return self._content.count(sub, start, end)

	def endswith(self, suffix, start=0, end=sys.maxsize):
		return self._content.endswith(suffix, start, end)

	def index(self, sub, start=0, end=sys.maxsize):
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

	def ljust(self, width, fill=" "):
		return self.__class__(self._content.ljust(width, fill))

	def lower(self):
		return self.__class__(self._content.lower())

	def lstrip(self, chars=None):
		return self.__class__(self._content.lstrip(chars))

	def replace(self, old, new, maxsplit=-1):
		return self.__class__(self._content.replace(old, new, maxsplit))

	def rjust(self, width, fill=" "):
		return self.__class__(self._content.rjust(width, fill))

	def rstrip(self, chars=None):
		return self.__class__(self._content.rstrip(chars))

	def rfind(self, sub, start=0, end=sys.maxsize):
		return self._content.rfind(sub, start, end)

	def rindex(self, sub, start=0, end=sys.maxsize):
		return self._content.rindex(sub, start, end)

	def split(self, sep=None, maxsplit=-1):
		return Frag(self._content.split(sep, maxsplit))

	def splitlines(self, keepends=0):
		return Frag(self._content.splitlines(keepends))

	def startswith(self, prefix, start=0, end=sys.maxsize):
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
			loc = " (from {})".format(self.startloc)
		else:
			loc = ""
		return "<{0.__class__.__module__}.{0.__class__.__fullname__} content={0.content!r}{1} at {2:#x}>".format(self, loc, id(self))


class Text(CharacterData):
	"""
	A text node. The characters ``<``, ``>``, ``&`` (and ``"`` inside
	attributes) will be "escaped" with the appropriate character entities when
	this node is published.
	"""

	def convert(self, converter):
		return self

	def __str__(self):
		return self._content

	def _repr_pretty_(self, p, cycle):
		if len(p.group_stack) <= 2:
			p.text("xsc.Text({!r})".format(self._content))
		else:
			p.text(repr(self._content))

	def publish(self, publisher):
		yield publisher.encodetext(self._content)

	def present(self, presenter):
		return presenter.presentText(self) # return a generator-iterator

	def compacted(self):
		return Null if self.content.isspace() else self

	def pretty(self, level=0, indent="\t"):
		return self


class Frag(Node, list):
	"""
	A fragment contains a list of nodes and can be used for dynamically
	constructing content. The attribute :attr:`content` of an :class:`Element`
	is a :class:`Frag`.
	"""

	def __init__(self, *content):
		list.__init__(self)
		for child in content:
			child = tonode(child)
			if isinstance(child, Frag):
				list.extend(self, child)
			elif child is not Null:
				list.append(self, child)

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("xsc.Frag(...)")
		else:
			with p.group(3, "xsc.Frag(", ")"):
				for (i, child) in enumerate(self):
					if i:
						p.text(",")
						p.breakable()
					else:
						p.breakable("")
					p.pretty(child)

	def __enter__(self):
		return threadlocalnodehandler.handler.enter(self)

	def __exit__(self, type, value, traceback):
		threadlocalnodehandler.handler.exit()

	def __call__(self, *content):
		self.extend(content)
		return self

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = cls._strbase(fullname=fullname, xml=xml)
		if decorate:
			s = "<{}>".format(s)
		return s

	def _create(self):
		"""
		internal helper that is used to create an empty clone of :var:`self`.
		"""
		# This is overwritten by :class:`Attr` to insure that attributes don't
		# get initialized with the default value when used in various methods
		# that create new attributes.
		return self.__class__()

	def clear(self):
		"""
		Make :var:`self` empty.
		"""
		del self[:]

	def convert(self, converter):
		node = self._create()
		for child in self:
			convertedchild = child.convert(converter)
			assert isinstance(convertedchild, Node), "the convert method returned the illegal object {!r} (type {!r}) when converting {!r}".format(convertedchild, type(convertedchild), self)
			node.append(convertedchild)
		return self._decoratenode(node)

	def clone(self):
		node = self._create()
		list.extend(node, (child.clone() for child in self))
		return self._decoratenode(node)

	def __copy__(self):
		"""
		helper for the :mod:`copy` module.
		"""
		node = self._create()
		list.extend(node, self)
		return self._decoratenode(node)

	def __deepcopy__(self, memo=None):
		"""
		helper for the :mod:`copy` module.
		"""
		node = self._create()
		if memo is None:
			memo = {}
		memo[id(self)] = node
		list.extend(node, (copy.deepcopy(child, memo) for child in self))
		return self._decoratenode(node)

	def present(self, presenter):
		return presenter.presentFrag(self) # return a generator-iterator

	def __str__(self):
		return "".join(str(child) for child in self)

	def __eq__(self, other):
		return self.__class__ is other.__class__ and list.__eq__(self, other)

	def publish(self, publisher):
		for child in self:
			for part in child.publish(publisher):
				yield part

	def __getitem__(self, index):
		"""
		Return the :var:`index`'th node of the content of the fragment. If
		:var:`index` is a list :meth:`__getitem__` will work recursively.
		If :var:`index` is an empty list, :var:`self` will be returned.
		:meth:`__getitem__` also supports walk filters.
		"""
		if isinstance(index, list):
			node = self
			for subindex in index:
				node = node[subindex]
			return node
		elif isinstance(index, int):
			return list.__getitem__(self, index)
		elif isinstance(index, slice):
			node = self._create()
			list.extend(node, list.__getitem__(self, index))
			return node
		else:
			from ll.xist import xfind
			def iterate(matcher):
				path = [self, None]
				for child in self:
					path[-1] = child
					if matcher(path):
						yield child
			return misc.Iterator(iterate(xfind.makewalkfilter(index).matchpath))

	def __setitem__(self, index, value):
		"""
		Allows you to replace the :var:`index`'th content node of the fragment
		with the new value :var:`value` (which will be converted to a node).
		If  :var:`index` is a list :meth:`__setitem__` will be applied to the
		innermost index after traversing the rest of :var:`index` recursively.
		If :var:`index` is an empty list, an exception will be raised.
		:meth:`__setitem__` also supports walk filters.
		"""
		if isinstance(index, list):
			if not index:
				raise ValueError("can't replace self")
			node = self
			for subindex in index[:-1]:
				node = node[subindex]
			node[index[-1]] = value
		elif isinstance(index, int):
			value = Frag(value)
			if index==-1:
				l = len(self)
				list.__setitem__(self, slice(l-1, l), value)
			else:
				list.__setitem__(self, slice(index, index+1), value)
		elif isinstance(index, slice):
			list.__setitem__(self, index, Frag(value))
		else:
			from ll.xist import xfind
			matcher = xfind.makewalkfilter(index).matchpath
			value = Frag(value)
			newcontent = []
			path = [self, None]
			for child in self:
				path[-1] = child
				if matcher(path):
					newcontent.extend(value)
				else:
					newcontent.append(child)
			list.__setitem__(self, slice(0, len(self)), newcontent)

	def __delitem__(self, index):
		"""
		Remove the :var:`index`'th content node from the fragment. If :var:`index`
		is a list, the innermost index will be deleted, after traversing the rest
		of :var:`index` recursively. If :var:`index` is an empty list, an
		exception will be raised. Anything except :class:`list`, :class:`int` and
		:class:`slice` objects will be turned into a walk filter and any child
		node matching this filter will be deleted from :var:`self`.
		"""
		if isinstance(index, list):
			if not index:
				raise ValueError("can't delete self")
			node = self
			for subindex in index[:-1]:
				node = node[subindex]
			del node[index[-1]]
		elif isinstance(index, (int, slice)):
			list.__delitem__(self, index)
		else:
			from ll.xist import xfind
			matcher = xfind.makewalkfilter(index).matchpath
			list.__setitem__(self, slice(0, len(self)), [child for child in self if not matcher([self, child])])

	def __mul__(self, factor):
		"""
		Return a :class:`Frag` with :var:`factor` times the content of :var:`self`.
		Note that no copies of the content will be generated, so this is a
		"shallow :meth:`__mul__`".
		"""
		node = self._create()
		list.extend(node, list.__mul__(self, factor))
		return node

	__rmul__ = __mul__

	def __iadd__(self, other):
		self.extend(other)
		return self

	# no need to implement __len__ or __bool__

	def append(self, *others):
		"""
		Append every item in :var:`others` to :var:`self`.
		"""
		for other in others:
			other = tonode(other)
			if isinstance(other, Frag):
				list.extend(self, other)
			elif other is not Null:
				list.append(self, other)

	def extend(self, items):
		"""
		Append all items from the sequence :var:`items` to :var:`self`.
		"""
		self.append(items)

	def insert(self, index, *others):
		"""
		Insert all items in :var:`others` at the position :var:`index`. (this is
		the same as ``self[index:index] = others``)
		"""
		other = Frag(*others)
		list.__setitem__(self, slice(index, index), other)

	def compacted(self):
		node = self._create()
		for child in self:
			compactedchild = child.compacted()
			assert isinstance(compactedchild, Node), "the compact method returned the illegal object {!r} (type {!r}) when compacting {!r}".format(compactedchild, type(compactedchild), child)
			if compactedchild is not Null:
				list.append(node, compactedchild)
		return self._decoratenode(node)

	def withsep(self, separator, clone=False):
		"""
		Return a version of :var:`self` with a separator node between the nodes of
		:var:`self`.

		if :var:`clone` is false, one node will be inserted several times, if
		:var:`clone` is true, clones of this node will be used.
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

	def reversed(self):
		"""
		Return a reversed version of the :var:`self`.
		"""
		node = list(self)
		node.reverse()
		return self.__class__(node)

	def filtered(self, function):
		"""
		Return a filtered version of the :var:`self`, i.e. a copy of :var:`self`,
		where only content nodes for which :func:`function` returns true will
		be copied.
		"""
		node = self._create()
		list.extend(node, (child for child in self if function(child)))
		return node

	def shuffled(self):
		"""
		Return a shuffled version of :var:`self`, i.e. a copy of :var:`self` where the
		content nodes are randomly reshuffled.
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
			converter = Converter(**converterargs)
		node = function(self, converter)
		assert isinstance(node, Node), "the mapped method returned the illegal object {!r} (type {!r}) when mapping {!r}".format(node, type(node), self)
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
			level += child.prettyindentbefore
			node.append(child.pretty(level, indent))
			level += child.prettyindentafter
		return node

	def __repr__(self):
		l = len(self)
		if l==0:
			info = "no children"
		elif l==1:
			info = "1 child"
		else:
			info = "{} children".format(l)
		loc = " (from {})".format(self.startloc) if self.startloc is not None else ""
		return "<{0.__class__.__module__}.{0.__class__.__fullname__} object ({1}){2} at {3:#x}>".format(self, info, loc, id(self))


class Comment(CharacterData):
	"""
	An XML comment.
	"""

	def convert(self, converter):
		return self

	def __str__(self):
		return ""

	def present(self, presenter):
		return presenter.presentComment(self)  # return a generator-iterator

	def publish(self, publisher):
		if not publisher.inattr:
			content = self.content
			if "--" in content or content.endswith("-"):
				warnings.warn(IllegalCommentContentWarning(self))
			yield publisher.encode("<!--")
			yield publisher.encode(content)
			yield publisher.encode("-->")


class _DocType_Meta(type(Node)):
	def __repr__(self):
		return "<doctype class {0.__module__}:{0.__fullname__} at {1:#x}>".format(self, id(self))


class DocType(CharacterData, metaclass=_DocType_Meta):
	"""
	An XML document type declaration.
	"""

	def convert(self, converter):
		return self

	def present(self, presenter):
		return presenter.presentDocType(self) # return a generator-iterator

	def publish(self, publisher):
		if not publisher.inattr:
			yield publisher.encode("<!DOCTYPE ")
			yield publisher.encode(self.content)
			yield publisher.encode(">")

	def __str__(self):
		return ""


class _ProcInst_Meta(type(Node)):
	def __new__(cls, name, bases, dict):
		self = super(_ProcInst_Meta, cls).__new__(cls, name, bases, dict)
		if dict.get("register") is not None: # check here as the pool isn't defined yet
			threadlocalpool.pool.register(self)
		return self

	def __repr__(self):
		return "<procinst class {0.__module__}:{0.__fullname__} at {1:#x}>".format(self, id(self))


class ProcInst(CharacterData, metaclass=_ProcInst_Meta):
	"""
	Base class for processing instructions.

	Processing instructions for specific targets must be implemented as
	subclasses of :class:`ProcInst`.
	"""

	register = None

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = cls._strbase(fullname=fullname, xml=xml)
		if decorate:
			s = "<{}>".format(s)
		return s

	def convert(self, converter):
		return self

	def present(self, presenter):
		return presenter.presentProcInst(self) # return a generator-iterator

	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		content = self.content
		if "?>" in content:
			raise IllegalProcInstFormatError(self)
		yield publisher.encode("<?{} {}?>".format(self.xmlname, content))

	def __str__(self):
		return ""

	def __repr__(self):
		if self.startloc is not None:
			loc = " (from {})".format(self.startloc)
		else:
			loc = ""
		return "<{0.__class__.__module__}.{0.__class__.__fullname__} procinst content={0.content!r}{1} at {2:#x}>".format(self, loc, id(self))

	def __mul__(self, n):
		return Node.__mul__(self, n) # don't inherit ``CharacterData.__mul__``

	def __rmul__(self, n):
		return Node.__rmul__(self, n) # don't inherit ``CharacterData.__rmul__``


class Null(CharacterData):
	"""
	node that does not contain anything.
	"""

	def _repr_pretty_(self, p, cycle):
		p.text("xsc.Null")

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = cls._strbase(fullname=fullname, xml=xml)
		if decorate:
			s = "<{}>".format(s)
		return s

	def convert(self, converter):
		return self

	def publish(self, publisher):
		if False:
			yield ""

	def present(self, presenter):
		return presenter.presentNull(self) # return a generator-iterator

	def __str__(self):
		return ""

	def __repr__(self):
		return "ll.xist.xsc.Null"


Null = Null() # Singleton, the Python way


class _Attr_Meta(type(Frag)):
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
				dict["values"] = tuple(str(entry) for entry in values)
		self = super(_Attr_Meta, cls).__new__(cls, name, bases, dict)
		if self.xmlns is not None:
			threadlocalpool.pool.register(self)
		return self

	def __repr__(self):
		return "<attribute class {0.__module__}:{0.__fullname__} at {1:#x}>".format(self, id(self))


class Attr(Frag, metaclass=_Attr_Meta):
	"""
	Base class of all attribute classes.

	The content of an attribute may be any other XIST node. This is different
	from a normal DOM, where only text and character references are allowed.
	The reason for this is to allow dynamic content (implemented as elements or
	processing instructions) to be put into attributes.

	Of course, this dynamic content when finally converted to HTML should
	normally result in a fragment consisting only of text and character
	references. But note that it is allowed to have elements and processing
	instructions inside of attributes even when publishing. Processing
	instructions will be published as is and for elements their content will be
	published::

		>>> from ll.xist.ns import html, php
		>>> node = html.img(
		...    src=php.php("echo 'eggs.gif'"),
		...    alt=html.abbr(
		...       "EGGS",
		...       title="Extensible Graphics Generation System",
		...       lang="en"
		...    )
		... )
		>>> print node.bytes()
		<img alt="EGGS" src="<?php echo 'eggs.gif'?>" />
	"""
	required = False
	default = None
	values = None

	def isfancy(self):
		"""
		Return whether :var:`self` contains nodes other than :class:`Text`.
		"""
		for child in self:
			if not isinstance(child, Text):
				return True
		return False

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("{}.{}(...)".format(self.__class__.__module__, self.__class__.__name__))
		else:
			with p.group(3, "{}.{}(".format(self.__class__.__module__, self.__class__.__name__), ")"):
				for (i, child) in enumerate(self):
					if i:
						p.text(",")
						p.breakable()
					else:
						p.breakable("")
					p.pretty(child)

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		return cls._strbase(fullname=fullname, xml=xml)

	def present(self, presenter):
		return presenter.presentAttr(self) # return a generator-iterator

	def checkvalid(self):
		"""
		Check whether :var:`self` has an allowed value, i.e. one that is specified
		in the class attribute ``values``. If the value is not allowed a warning
		will be issued through the Python warning framework.

		If :var:`self` is "fancy" (i.e. contains non-:class:`Text` nodes), no
		check will be done.
		"""
		values = self.__class__.values
		if self and isinstance(values, tuple) and not self.isfancy():
			value = str(self)
			if value not in values:
				warnings.warn(IllegalAttrValueWarning(self))

	def _publishname(self, publisher):
		if self.xmlns is not None:
			prefix = publisher._ns2prefix.get(self.xmlns) if self.xmlns != xml_xmlns else "xml"
			if prefix is not None:
				return "{}:{}".format(prefix, self.xmlname)
		return self.xmlname

	def _publishattrvalue(self, publisher):
		# Internal helper that is used to publish the attribute value
		# (can be overwritten in subclass (done by e.g. :class:`StyleAttr` and
		# :class:`URLAttr`)
		return Frag.publish(self, publisher)

	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		if len(self)==1 and isinstance(self[0], AttrElement):
			for part in self[0].publishattr(publisher, self):
				yield part
		else:
			publisher.inattr += 1
			yield publisher.encode(' {}="'.format(self._publishname(publisher)))
			publisher.pushtextfilter(misc.xmlescape_attr)
			for part in self._publishattrvalue(publisher):
				yield part
			publisher.poptextfilter()
			yield publisher.encode('"')
			publisher.inattr -= 1

	def pretty(self, level=0, indent="\t"):
		return self.clone()

	def __repr__(self):
		l = len(self)
		if l==0:
			info = "no children"
		elif l==1:
			info = "1 child"
		else:
			info = "{} children".format(l)
		loc = " (from {})".format(self.startloc) if self.startloc is not None else ""
		return "<{0.__class__.__module__}.{0.__class__.__fullname__} attr object ({1}){2} at {3:#x}>".format(self, info, loc, id(self))


class TextAttr(Attr):
	"""
	Attribute class that is used for normal text attributes.
	"""


class IDAttr(Attr):
	"""
	Attribute used for ids.
	"""


class NumberAttr(Attr):
	"""
	Attribute class that is used for when the attribute value may be any kind
	of number.
	"""


class IntAttr(NumberAttr):
	"""
	Attribute class that is used when the attribute value may be an integer.
	"""


class FloatAttr(NumberAttr):
	"""
	Attribute class that is used when the attribute value may be a
	floating point value.
	"""


class BoolAttr(Attr):
	"""
	Attribute class that is used for boolean attributes. When publishing
	the value will always be the attribute name, regardless of the real value.
	"""

	# We can't simply overwrite :meth:`_publishattrvalue`, because for ``xhtml==0`` we don't output a "proper" attribute
	def publish(self, publisher):
		if publisher.validate:
			self.checkvalid()
		if len(self)==1 and isinstance(self[0], AttrElement):
			for part in self[0].publishboolattr(publisher, self):
				yield part
		else:
			publisher.inattr += 1
			name = self._publishname(publisher)
			yield publisher.encode(" {}".format(name))
			if publisher.xhtml>0:
				yield publisher.encode('="')
				publisher.pushtextfilter(misc.xmlescape)
				yield publisher.encode(name)
				publisher.poptextfilter()
				yield publisher.encode('"')
			publisher.inattr -= 1


class ColorAttr(Attr):
	"""
	Attribute class that is used for a color attributes.
	"""


class StyleAttr(Attr):
	"""
	Attribute class that is used for CSS style attributes.
	"""

	def _transform(self, replacer):
		from ll.xist import css
		stylesheet = cssutils.parseString("a{{{}}}".format(self))
		css.replaceurls(stylesheet, replacer)
		return stylesheet.cssRules[0].style.getCssText(separator=" ")

	def replaceurls(self, replacer):
		"""
		Replace each URL in the style. Each URL will be passed to the callable
		:var:`replacer` and replaced with the returned value.
		"""
		self[:] = self._transform(replacer)

	def parsed(self, parser, event):
		if event == "leaveattrns" and not self.isfancy() and parser.base is not None:
			from ll.xist import css
			def prependbase(u):
				return parser.base/u
			self.replaceurls(prependbase)

	def _publishattrvalue(self, publisher):
		if not self.isfancy() and publisher.base is not None:
			from ll.xist import css
			def reltobase(u):
				return u.relative(publisher.base)
			for part in Frag(self._transform(reltobase)).publish(publisher):
				yield part
		else:
			for part in super(StyleAttr, self)._publishattrvalue(publisher):
				yield part

	def urls(self, base=None):
		"""
		Return a list of all the URLs (as :class:`URL` objects) found in the style
		attribute.
		"""
		from ll.xist import css
		urls = []
		def collect(u):
			urls.append(u)
			return u
		s = cssutils.parseString("a{{{}}}".format(self))
		css.replaceurls(s, collect)
		return urls


class URLAttr(Attr):
	"""
	Attribute class that is used for URLs. See the module :mod:`ll.url` for more
	information about URL handling.
	"""

	def parsed(self, parser, event):
		if event == "leaveattrns" and not self.isfancy() and parser.base is not None:
			self[:] = (url_.URL(parser.base/str(self)),)

	def _publishattrvalue(self, publisher):
		if self.isfancy():
			return Attr._publishattrvalue(self, publisher)
		else:
			new = Attr(url_.URL(str(self)).relative(publisher.base))
			return new._publishattrvalue(publisher)

	def asURL(self):
		"""
		Return :var:`self` as a :class:`URL` object (note that non-:class:`Text`
		content will be filtered out).
		"""
		return url_.URL(Attr.__str__(self))

	def forInput(self, root=None):
		"""
		return a :class:`URL` pointing to the real location of the referenced
		resource. :var:`root` must be the root URL relative to which :var:`self`
		will be interpreted and usually comes from the ``root`` attribute of the
		:var:`converter` argument in :meth:`convert`.
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
		Return a :class:`Resource` for reading from the URL.
		"""
		return self.forInput(root).openread()

	def openwrite(self, root=None):
		"""
		Return a :class:`Resource` for writing to the URL.
		"""
		return self.forInput(root).openwrite()


class _Attrs_Meta(type(Node)):
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
		return "<attrs class {0.__module__}:{0.__fullname__} with {1} attrs at {2:#x}>".format(self, len(self._bypyname), id(self))

	def __contains__(self, key):
		if isinstance(key, str):
			return key in self._bypyname
		if key.xmlns is not None:
			return True
		return self._bypyname.get(key.__name__, None) is key


class Attrs(Node, dict, metaclass=_Attrs_Meta):
	"""
	An attribute map. Allowed entries are specified through nested subclasses
	of :class:`Attr`.
	"""

	def __init__(self, _content=None, **attrs):
		dict.__init__(self)
		# set default attribute values
		for (key, value) in self._defaultattrspy.items():
			self[key] = value.default.clone()
		# set attributes, this might overwrite (or delete) default attributes
		self.update(_content, **attrs)

	@staticmethod
	def _sortorder(cls):
		return (getattr(cls, "xmlorder", "\uffff"), nsclark(cls.xmlns) + cls.xmlname)

	def _repr_pretty_content_(self, p, first=True):
		for attr in sorted(self.values(), key=self._sortorder):
			if first:
				p.breakable("")
				first = False
			else:
				p.text(",")
				p.breakable()
			if attr.xmlns is not None:
				attrname = "{}.{}".format(attr.__class__.__module__, attr.__class__.__fullname__)
			else:
				attrname = attr.__class__.__name__
			if len(attr) == 1:
				p.text(attrname)
				p.text("=")
				p.pretty(attr[0])
			else:
				with p.group(3, "{}=(".format(attrname), ")"):
					attrfirst = True
					for attrchild in attr:
						if attrfirst:
							p.breakable("")
							attrfirst = False
						else:
							p.text(",")
							p.breakable()
						p.pretty(attrchild)

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("{}.{}(...)".format(self.__class__.__module__, self.__class__.__fullname__))
		else:
			with p.group(3, "{}.{}(".format(self.__class__.__module__, self.__class__.__fullname__), ")"):
				self._repr_pretty_content_(p, True)

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
			value.__fullname__ = "{}.{}".format(cls.__fullname__, value.__fullname__)

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
			assert isinstance(newvalue, Node), "the convert method returned the illegal object {0!r} (type {1!r}) when converting the attribute {2.__class__.__name__} with the value {2!r}".format(newvalue, type(newvalue), value)
			node[value.__class__] = newvalue
		return node

	def compacted(self):
		node = self._create()
		for value in self.values():
			newvalue = value.compacted()
			assert isinstance(newvalue, Node), "the compacted method returned the illegal object {0!r} (type {1!r}) when compacting the attribute {2.__class__.__name__} with the value {2!r}".format(newvalue, type(newvalue), value)
			node[value.__class__] = newvalue
		return node

	def normalized(self):
		node = self._create()
		for value in self.values():
			newvalue = value.normalized()
			assert isinstance(newvalue, Node), "the normalized method returned the illegal object {0!r} (type {1!r}) when normalizing the attribute {2.__class__.__name__} with the value {2!r}".format(newvalue, type(newvalue), value)
			node[value.__class__] = newvalue
		return node

	def present(self, presenter):
		return presenter.presentAttrs(self) # return a generator-iterator

	def checkvalid(self):
		# collect required attributes
		attrs = {value for value in self.allowedattrs() if value.required}
		# Check each existing attribute and remove it from the list of required ones
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

		for value in sorted(self.values(), key=self._sortorder):
			for part in value.publish(publisher):
				yield part

	def __str__(self):
		return ""

	@classmethod
	def isallowed(cls, name):
		if isinstance(name, str):
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
		if isinstance(name, str):
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
		Return whether :var:`self` has an attribute with a Python name :var:`name`.
		:var:`name` may also be an attribute class (either from ``self.Attrs``
		or a global attribute).
		"""
		try:
			attr = dict.__getitem__(self, self.allowedattr(name))
		except KeyError:
			return False
		return len(attr)>0

	def has_xml(self, name):
		"""
		Similar to :meth:`has`, but :var:`name` is treated as the XML name
		instead of the Python name.
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
		works like the dictionary method :meth:`get`, it returns the attribute
		with the Python name :var:`name`, or :var:`default` if :var:`self` has no
		such attribute. :var:`name` may also be an attribute class (either from
		``self.Attrs`` or a global attribute).
		"""
		attr = self.attr(name)
		if not attr:
			attr = self.allowedattr(name)(default) # pack the attribute into an attribute object
		return attr

	def get_xml(self, name, default=None):
		"""
		Similar to :meth:`get`, but :var:`name` is treated as the XML name
		instead of the Python name.
		"""
		attr = self.attr_xml(name)
		if not attr:
			attr = self.allowedattr_xml(name)(default) # pack the attribute into an attribute object
		return attr

	def set(self, name, value):
		"""
		Set the attribute with the Python :var:`name` to the value :var:`value`.
		:var:`name` may be a string or an attribute class. The newly set attribute
		will be returned.
		"""
		attr = self.allowedattr(name)
		value = attr(value)
		dict.__setitem__(self, attr, value) # put the attribute in our dict
		return value

	def set_xml(self, name, value):
		"""
		Similar to :meth:`set`, but :var:`name` is treated as the XML name
		instead of the Python name.
		"""
		attr = self.allowedattr_xml(name)
		value = attr(value)
		dict.__setitem__(self, attr, value) # put the attribute in our dict
		return value

	def setdefault(self, name, default):
		"""
		Works like the dictionary method :meth:`setdefault`, it returns the
		attribute with the Python name :var:`name`. If :var:`self` has no such
		attribute, it will be set to :var:`default` and :var:`default` will be
		returned as the new attribute value.
		"""
		value = self.attr(name)
		if not value:
			attr = self.allowedattr(name)
			value = attr(default) # pack the attribute into an attribute object
			dict.__setitem__(self, attr, value)
		return value

	def setdefault_xml(self, name, default):
		"""
		Similar to :meth:`setdefault`, but :var:`name` is treated as the XML name
		instead of the Python name.
		"""
		value = self.attr_xml(name)
		if not value:
			attr = self.allowedattr(name)
			value = attr(default) # pack the attribute into an attribute object
			dict.__setitem__(self, attr, value)
		return value

	def update(self, *args, **kwargs):
		"""
		Copies attributes over from all mappings in :var:`args` and from
		:var:`kwargs`.
		"""
		for mapping in args + (kwargs,):
			if mapping is not None:
				if isinstance(mapping, Attrs):
					# This makes sure that global attributes are copied properly
					for value in mapping._allvalues():
						self[value.__class__] = value
				else:
					for (attrname, attrvalue) in mapping.items():
						self[attrname] = attrvalue

	@classmethod
	def allowedattrs(cls):
		"""
		Return an iterator over all allowed attribute classes.
		"""
		return iter(cls._bypyname.values())

	@classmethod
	def allowedattr(cls, name):
		if isinstance(name, str):
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
		if isinstance(name, str):
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
		for value in dict.values(self):
			if value:
				yield value.__class__

	iterkeys = __iter__ = keys

	def values(self):
		for value in dict.values(self):
			if value:
				yield value

	itervalues = values

	def items(self):
		for value in dict.values(self):
			if value:
				yield (value.__class__, value)

	iteritems = items

	def _allvalues(self):
		"""
		Iterate through all values, even the unset ones.
		"""
		return dict.values(self)

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
		Return a filtered version of :var:`self`.
		"""
		node = self._create()
		for (name, value) in self.items():
			if function(value):
				node[name] = value
		return node

	def _fixnames(self, names):
		newnames = []
		for name in names:
			if isinstance(name, str):
				try:
					name = self.allowedattr(name)
				except IllegalAttrError:
					continue
			newnames.append(name)
		return tuple(newnames)

	def _fixnames_xml(self, names):
		newnames = []
		for name in names:
			if isinstance(name, str):
				try:
					name = self.allowedattr_xml(name)
				except IllegalAttrError:
					continue
			newnames.append(name)
		return tuple(newnames)

	def withnames(self, *names):
		"""
		Return a copy of :var:`self` where only the attributes with Python names
		in :var:`names` are kept, all others are removed.
		"""
		def isok(node):
			return isinstance(node, names)

		names = self._fixnames(names)
		return self.filtered(isok)

	def withnames_xml(self, *names):
		"""
		Return a copy of :var:`self` where only the attributes with XML names
		in :var:`names` are kept, all others are removed.
		"""
		def isok(node):
			return isinstance(node, names)

		names = self._fixnames_xml(names)
		return self.filtered(isok)

	def withoutnames(self, *names):
		"""
		Return a copy of :var:`self` where all the attributes with Python names
		in :var:`names` are removed.
		"""
		def isok(node):
			return not isinstance(node, names)

		names = self._fixnames(names)
		return self.filtered(isok)

	def withoutnames_xml(self, *names):
		"""
		Return a copy of :var:`self` where all the attributes with XML names
		in :var:`names` are removed.
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
			info = "({} attrs)".format(l)
		if self.startloc is not None:
			loc = " (from {})".format(self.startloc)
		else:
			loc = ""
		return "<{0.__class__.__module__}.{0.__class__.__fullname__} attrs {1}{2} at {3:#x}>".format(self, info, loc, id(self))


def _patchclassnames(dict, name):
	# If an :class:`Attrs` class has been provided patch up its class names
	try:
		attrs = dict["Attrs"]
	except KeyError:
		pass
	else:
		attrs.__fullname__ = "{}.Attrs".format(name)
		for (key, value) in attrs.__dict__.items():
			if isinstance(value, _Attr_Meta):
				value.__fullname__ = "{}.{}".format(name, value.__fullname__)

	# If a Context has been provided patch up its class names
	try:
		context = dict["Context"]
	except KeyError:
		pass
	else:
		context.__fullname__ = "{}.{}".format(name, context.__fullname__)


class _Element_Meta(type(Node)):
	def __new__(cls, name, bases, dict):
		if "model" in dict and isinstance(dict["model"], bool):
			from ll.xist import sims
			dict["model"] = sims.Any() if dict["model"] else sims.Empty()
		_patchclassnames(dict, name)
		self = super(_Element_Meta, cls).__new__(cls, name, bases, dict)
		if dict.get("register") is not None:
			threadlocalpool.pool.register(self)
		return self

	def __repr__(self):
		return "<element class {0.__module__}:{0.__fullname__} at {1:#x}>".format(self, id(self))


class Element(Node, metaclass=_Element_Meta):
	"""
	This class represents XML/XIST elements. All elements implemented by the
	user must be derived from this class.

	Elements support the following class variables:

	:attr:`model` : object with :meth:`checkvalid` method
		This is an object that is used for validating the content of the element.
		See the module :mod:`ll.xist.sims` for more info. If :attr:`model` is
		:const:`None` validation will be skipped, otherwise it will be performed
		when parsing or publishing.

	:attr:`Attrs` : :class:`Element.Attrs` subclass
		This is a class derived from :class:`Element.Attrs` and must define all
		attributes as classes nested inside this :class:`Attrs` class.

	:attr:`xmlns` : string
		This is the name of the namespace this element belong to.

	:attr:`register` : bool
		If :attr:`register` is false the element will never be registered in a
		:class:`Pool`. The default is :const:`True`.

	:attr:`xmlname` : string
		If the class name has to be different from the XML name (e.g. because the
		XML name is not a valid Python identifier) :attr:`xmlname` can be used to
		specify the real XML name. Otherwise the XML name will be the Python name.
	"""

	model = None
	register = None

	Attrs = Attrs

	def __init__(self, *content, **attrs):
		"""
		Create a new :class:`Element` instance.

		Positional arguments are treated as content nodes. Keyword arguments and
		dictionaries are treated as attributes.
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

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text("{}.{}(...)".format(self.__class__.__module__, self.__class__.__name__))
		else:
			text = "{}.{}(".format(self.__class__.__module__, self.__class__.__name__)
			with p.group(3, text, ")"):
				first = True
				for child in self:
					if first:
						p.breakable("")
						first = False
					else:
						p.text(",")
						p.breakable()
					p.pretty(child)

				self.attrs._repr_pretty_content_(p, first)

	def __getstate__(self):
		attrs = {}
		for (key, value) in self.attrs.items():
			if key.xmlns is None:
				key = key.__name__
			else:
				key = (key.__module__, key.__fullname__)
			attrs[key] = Frag(value)
		return (self.content, attrs)

	def __setstate__(self, data):
		(content, attrs) = data
		self.content = content
		self.attrs = self.Attrs()
		for (key, value) in attrs.items():
			if not isinstance(key, str):
				obj = __import__(key[0])
				for name in key[0].split(".")[1:]:
					obj = getattr(obj, name)
				for name in key[1].split("."):
					obj = getattr(obj, name)
				key = obj
			self.attrs[key] = value

	def __enter__(self):
		"""
		:class:`Element` nodes can be used in ``with`` blocks to build XIST trees.
		Inside a ``with`` block ``+`` and :func:`add` can be used to append node
		to the currently active element in the ``with`` block::

			with xsc.build():
				with html.ul() as node:
					+html.li("I hear and I forget.")
					+html.li("I see and I believe.")
					+html.li("I do and I understand.")
					xsc.add(class_="quote")
			print node.bytes()
		"""
		threadlocalnodehandler.handler.enter(self)
		return self

	def __exit__(self, type, value, traceback):
		threadlocalnodehandler.handler.exit()

	def __call__(self, *content, **attrs):
		"""
		Calling an element add items in :var:`content` to the element content
		and set attributes from :var:`attrs`. The element itself will be returned.
		"""
		for child in content:
			if isinstance(child, dict):
				self.attrs.update(child)
			else:
				self.content.append(child)
		for (attrname, attrvalue) in attrs.items():
			self.attrs[attrname] = attrvalue
		return self

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.content==other.content and self.attrs==other.attrs

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = cls._strbase(fullname=fullname, xml=xml)
		if decorate:
			if cls.model is not None and cls.model.empty:
				s = "<{}/>".format(s)
			else:
				s = "<{}>".format(s)
		return s

	def checkvalid(self):
		if self.model is not None:
			self.model.checkvalid(self)
		self.attrs.checkvalid()

	def append(self, *items):
		"""
		Append every item in :var:`items` to the elements content.
		"""
		self.content.append(*items)

	def extend(self, items):
		"""
		Append all items in :var:`items` to the elements content.
		"""
		self.content.extend(items)

	def insert(self, index, *items):
		"""
		Insert every item in :var:`items` at the position :var:`index`.
		"""
		self.content.insert(index, *items)

	def convert(self, converter):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.convert(converter)
		node.attrs = self.attrs.convert(converter)
		return self._decoratenode(node)

	def clone(self):
		node = self.__class__() # "virtual" constructor
		node.content = self.content.clone() # this is faster than passing it in the constructor (no :func:`tonode` call)
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

	def __str__(self):
		return str(self.content)

	def _addimagesizeattributes(self, url, widthattr=None, heightattr=None):
		"""
		Automatically set image width and height attributes.

		The size of the image with the URL :var:`url` will be determined and the
		width of the image will be put into the attribute with the name
		:var:`widthattr` if :var:`widthattr` is not :const:`None` and the
		attribute is not set already. The same will happen for the height, which
		will be put into the attribute named :var:`heighattr`.
		"""
		try:
			size = url.imagesize()
		except IOError as exc:
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
				return "{}:{}".format(prefix, self.xmlname)
		return self.xmlname

	def _publishfull(self, publisher):
		"""
		Does the full publication of the element. If you need full elements
		inside attributes (e.g. for JSP tag libraries), you can overwrite
		:meth:`publish` and simply call this method.
		"""
		name = self._publishname(publisher)
		yield publisher.encode("<")
		yield publisher.encode(name)
		# we're the first element to be published, so we have to create the xmlns attributes
		if publisher._publishxmlns:
			for (xmlns, prefix) in publisher._ns2prefix.items():
				if xmlns not in publisher.hidexmlns:
					yield publisher.encode(" xmlns")
					if prefix is not None:
						yield publisher.encode(":")
						yield publisher.encode(prefix)
					yield publisher.encode('="')
					yield publisher.encode(xmlns)
					yield publisher.encode('"')
			# reset the note, so the next element won't create the attributes again
			publisher._publishxmlns = False
		for part in self.attrs.publish(publisher):
			yield part
		if len(self):
			yield publisher.encode(">")
			for part in self.content.publish(publisher):
				yield part
			yield publisher.encode("</")
			yield publisher.encode(name)
			yield publisher.encode(">")
		else:
			if publisher.xhtml in (0, 1):
				if self.model is not None and self.model.empty:
					if publisher.xhtml==1:
						yield publisher.encode(" /")
					yield publisher.encode(">")
				else:
					yield publisher.encode("></")
					yield publisher.encode(name)
					yield publisher.encode(">")
			elif publisher.xhtml == 2:
				yield publisher.encode("/>")

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
		If :var:`index` is a string, return the attribute with this (Python)
		name. If :var:`index` is an attribute class, return the attribute
		that is an instance of this class. If :var:`index` is a number or slice
		return the appropriate content node. :var:`index` may also be a list, in
		with case :meth:`__getitem__` will be applied recusively.
		:meth:`__getitem__` also supports walk filters.

		"""
		if isinstance(index, (str, _Attr_Meta)):
			return self.attrs[index]
		elif isinstance(index, (list, int, slice)):
			return self.content[index]
		else:
			from ll.xist import xfind
			def iterate(matcher):
				path = [self, None]
				for child in self:
					path[-1] = child
					if matcher(path):
						yield child
			return misc.Iterator(iterate(xfind.makewalkfilter(index).matchpath))

	def __setitem__(self, index, value):
		"""
		Set an attribute or content node to the value :var:`value`. For possible
		types for :var:`index` see :meth:`__getitem__`.
		"""
		if isinstance(index, (str, _Attr_Meta)):
			self.attrs[index] = value
		elif isinstance(index, (list, int, slice)):
			self.content[index] = value
		else:
			from ll.xist import xfind
			matcher = xfind.makewalkfilter(index).matchpath
			value = Frag(value)
			newcontent = []
			path = [self, None]
			for child in self:
				path[-1] = child
				if matcher(path):
					newcontent.extend(value)
				else:
					newcontent.append(child)
			self.content[:] = newcontent

	def __delitem__(self, index):
		"""
		Remove an attribute or content node. For possible types for :var:`index`
		see :meth:`__getitem__`.
		"""
		if isinstance(index, (str, _Attr_Meta)):
			del self.attrs[index]
		elif isinstance(index, (list, int, slice)):
			del self.content[index]
		else:
			from ll.xist import xfind
			matcher = xfind.makewalkfilter(index).matchpath
			self.content = Frag(child for child in self if not matcher([self, child]))

	def __iadd__(self, other):
		self.extend(other)
		return self

	def __len__(self):
		"""
		Return the number of children.
		"""
		return len(self.content)

	def __iter__(self):
		return iter(self.content)

	def compacted(self):
		node = self.__class__()
		node.content = self.content.compacted()
		node.attrs = self.attrs.compacted()
		return self._decoratenode(node)

	def withsep(self, separator, clone=False):
		"""
		Return a version of :var:`self` with a separator node between the child
		nodes of :var:`self`. For more info see :meth:`Frag.withsep`.
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.withsep(separator, clone)
		return node

	def reversed(self):
		"""
		Return a reversed version of :var:`self`.
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.reversed()
		return node

	def filtered(self, function):
		"""
		Return a filtered version of the :var:`self`.
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.filtered(function)
		return node

	def shuffled(self):
		"""
		Return a shuffled version of the :var:`self`.
		"""
		node = self.__class__()
		node.attrs = self.attrs.clone()
		node.content = self.content.shuffled()
		return node

	def mapped(self, function, converter=None, **converterargs):
		if converter is None:
			converter = Converter(**converterargs)
		node = function(self, converter)
		assert isinstance(node, Node), "the mapped method returned the illegal object {!r} (type {!r}) when mapping {!r}".format(node, type(node), self)
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
		orglevel = level # Remember the original indent level, so that any misconfiguration inside the element doesn't mess with the indentation
		node = self.__class__(self.attrs)
		if len(self):
			# search for text content
			for child in self:
				if isinstance(child, Text):
					# leave content alone
					node.append(self.content.clone())
					break
			else:
				level += 1
				for child in self:
					level += child.prettyindentbefore
					node.append("\n", child.pretty(level, indent))
					level += child.prettyindentafter
				node.append("\n", indent*orglevel)
		if orglevel>0:
			node = Frag(indent*orglevel, node)
		return node

	def __repr__(self):
		lc = len(self.content)
		if lc==0:
			infoc = "no children"
		elif lc==1:
			infoc = "1 child"
		else:
			infoc = "{} children".format(lc)
		la = len(self.attrs)
		if la==0:
			infoa = "no attrs"
		elif la==1:
			infoa = "1 attr"
		else:
			infoa = "{} attrs".format(la)
		if self.startloc is not None:
			loc = " (from {})".format(self.startloc)
		else:
			loc = ""
		return "<{0.__class__.__module__}.{0.__class__.__fullname__} element object ({1}/{2}){3} at {4:#x}>".format(self, infoc, infoa, loc, id(self))


class AttrElement(Element):
	"""
	Special subclass of :class:`Element`.

	When an :class:`AttrElement` node is the only node in an attribute, it
	takes over publishing of the attribute (via the methods :meth:`publishattr`
	and :meth:`publishboolattr`). In all other cases publishing is done in the
	normal way (and must be overwritten with the :meth:`publish` method).
	"""

	register = None

	@misc.notimplemented
	def publish(self, publisher):
		"""
		Publish ``self`` to the publisher :var:`publisher` (outside of any
		attribute)
		"""

	@misc.notimplemented
	def publishattr(self, publisher, attr):
		"""
		Publish the attribute :var:`attr` to the publisher :var:`publisher`.
		"""

	@misc.notimplemented
	def publishboolattr(self, publisher, attr):
		"""
		Publish the boolean attribute :var:`attr` to the publisher
		"""


class _Entity_Meta(type(Node)):
	def __new__(cls, name, bases, dict):
		self = super(_Entity_Meta, cls).__new__(cls, name, bases, dict)
		if dict.get("register") is not None:
			threadlocalpool.pool.register(self)
		return self

	def __repr__(self):
		return "<entity class {0.__module__}:{0.__fullname__} at {1:#x}>".format(self, id(self))


class Entity(Node, metaclass=_Entity_Meta):
	"""
	Class for entities. Derive your own entities from it and overwrite
	:meth:`convert`.
	"""

	register = None

	def _repr_pretty_(self, p, cycle):
		p.text("{}.{}()".format(self.__class__.__module__, self.__class__.__name__))

	@classmethod
	def _str(cls, fullname=True, xml=True, decorate=True):
		s = cls._strbase(fullname=fullname, xml=xml)
		if decorate:
			s = "&{};".format(s)
		return s

	def __eq__(self, other):
		return self.__class__ is other.__class__

	def compacted(self):
		return self

	def present(self, presenter):
		return presenter.presentEntity(self) # return a generator-iterator

	def publish(self, publisher):
		yield publisher.encode("&")
		yield publisher.encode(self.xmlname)
		yield publisher.encode(";")

	def __repr__(self):
		if self.startloc is not None:
			loc = " (from {})".format(self.startloc)
		else:
			loc = ""
		return "<{0.__class__.__module__}.{0.__class__.__fullname__} entity object{1} at {2:#x}>".format(self, loc, id(self))


class _CharRef_Meta(type(Entity)): # don't subclass Text.__metaclass__, as this is redundant
	def __repr__(self):
		return "<charref class {0.__module__}:{0.__fullname__} at {1:#x}>".format(self, id(self))


class CharRef(Text, Entity, metaclass=_CharRef_Meta):
	"""
	A simple named character reference, the codepoint is in the class attribute
	:attr:`codepoint`.
	"""
	register = None

	def __init__(self):
		Text.__init__(self, chr(self.codepoint))
		Entity.__init__(self)

	def _repr_pretty_(self, p, cycle):
		p.text("{}.{}()".format(self.__class__.__module__, self.__class__.__name__))

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
		return Text(str(other) + self.content)

	def __mul__(self, n):
		return Text(n * self.content)

	def __rmul__(self, n):
		return Text(n * self.content)

	def capitalize(self):
		return Text(self.content.capitalize())

	def center(self, width):
		return Text(self.content.center(width))

	def ljust(self, width, fill=" "):
		return Text(self.content.ljust(width, fill))

	def lower(self):
		return Text(self.content.lower())

	def lstrip(self, chars=None):
		return Text(self.content.lstrip(chars))

	def replace(self, old, new, maxsplit=-1):
		return Text(self.content.replace(old, new, maxsplit))

	def rjust(self, width, fill=" "):
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


###
### XML class pool
###

class Pool(misc.Pool):
	"""
	A :class:`Pool` stores a collection of XIST classes and can be passed to a
	parser. The parser will ask the pool which classes to use when elements,
	processing instructions etc. have to be instantiated.
	"""

	def __init__(self, *objects):
		"""
		Create a :class:`Pool` object. All items in :var:`objects` will be
		registered in the pool.
		"""
		self._elementsbyxmlname = {}
		self._elementsbypyname = {}
		self._procinstsbyxmlname = {}
		self._procinstsbypyname = {}
		self._entitiesbyxmlname = {}
		self._entitiesbypyname = {}
		self._charrefsbyxmlname = {}
		self._charrefsbypyname = {}
		self._charrefsbycodepoint = {}
		self._attrsbyxmlname = {}
		self._attrsbypyname = {}
		misc.Pool.__init__(self, *objects)

	def register(self, object):
		"""
		Register :var:`object` in the pool. :var:`object` can be:

		*	a :class:`Element`, :class:`ProcInst`, :class:`Entity`, or
			:class:`CharRef` class;

		*	an :class:`Attr` class for a global attribute;

		*	an :class:`Attrs` class containing global attributes;

		*	a :class:`dict` (all values will be registered, this makes it possible
			to e.g. register all local variables by passing ``vars()``);

		*	a module (all attributes in the module will be registered).
		"""
		# Note that the following is a complete reimplementation, otherwise the interactions would be too complicated.
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
				if object.xmlns is not None and object.register:
					self._attrsbyxmlname[(object.xmlname, object.xmlns)] = object
					self._attrsbypyname[(object.__name__, object.xmlns)] = object
			elif issubclass(object, Attrs):
				for attr in object.allowedattrs():
					self.register(attr)
			self._attrs[object.__name__] = object
		elif isinstance(object, types.ModuleType):
			self.register(object.__dict__)
		elif isinstance(object, dict):
			for (key, value) in object.items():
				if key == "__bases__":
					for base in value:
						if not isinstance(base, Pool):
							base = self.__class__(base)
						self.bases.append(base)
				elif isinstance(value, type):
					self.register(value)
				elif not isinstance(value, (types.ModuleType, dict)):
					try:
						self._attrs[key] = value
					except TypeError:
						pass
		elif isinstance(object, Pool):
			self.bases.append(object)

	def __enter__(self):
		self.prev = threadlocalpool.pool
		threadlocalpool.pool = self
		return self

	def __exit__(self, type, value, traceback):
		threadlocalpool.pool = self.prev
		del self.prev

	def clear(self):
		"""
		Make :var:`self` empty.
		"""
		self._elementsbyxmlname.clear()
		self._elementsbypyname.clear()
		self._procinstsbyxmlname.clear()
		self._procinstsbypyname.clear()
		self._entitiesbyxmlname.clear()
		self._entitiesbypyname.clear()
		self._charrefsbyxmlname.clear()
		self._charrefsbypyname.clear()
		self._charrefsbycodepoint.clear()
		self._attrsbyxmlname.clear()
		self._attrsbypyname.clear()
		misc.Pool.clear(self)

	def clone(self):
		"""
		Return a copy of :var:`self`.
		"""
		copy = misc.Pool.clone(self)
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
		return copy

	def elements(self):
		"""
		Return an iterator for all registered element classes.
		"""
		seen = set()
		for element in self._elementsbypyname.values():
			yield element
			seen.add((element.xmlname, element.xmlns))
		for base in self.bases:
			for element in base.elements():
				if (element.xmlname, element.xmlns) not in seen:
					yield element
					seen.add((element.xmlname, element.xmlns))

	def elementclass(self, name, xmlns):
		"""
		Return the element class for the element with the Python name :var:`name`
		and the namespace :var:`xmlns`. If the element can't be found an
		:exc:`IllegalElementError` will be raised.
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
		Return the element class for the element type with the XML name
		:var:`name` and the namespace :var:`xmlns`. If the element can't
		be found an :exc:`IllegalElementError` will be raised.
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
		:var:`name` and the namespace :var:`xmlns`.
		"""
		return self.elementclass(name, xmlns)()

	def element_xml(self, name, xmlns):
		"""
		Return an element object for the element type with the XML name
		:var:`name` and the namespace :var:`xmlns`.
		"""
		return self.elementclass_xml(name, xmlns)()

	def haselement(self, name, xmlns):
		"""
		Is there a registered element class in :var:`self` for the element type
		with the Python name :var:`name` and the namespace :var:`xmlns`?
		"""
		return (name, nsname(xmlns)) in self._elementsbypyname or any(base.haselement(name, xmlns) for base in self.bases)

	def haselement_xml(self, name, xmlns):
		"""
		Is there a registered element class in :var:`self` for the element type
		with the XML name :var:`name` and the namespace :var:`xmlns`?
		"""
		return (name, nsname(xmlns)) in self._elementsbyxmlname or any(base.haselement_xml(name, xmlns) for base in self.bases)

	def procinsts(self):
		"""
		Return an iterator for all registered processing instruction classes.
		"""
		seen = set()
		for procinst in self._procinstsbypyname.values():
			yield procinst
			seen.add(procinst.xmlname)
		for base in self.bases:
			for procinst in base.procinsts():
				if procinst.xmlname not in seen:
					yield procinst
					seen.add(procinst.xmlname)

	def procinstclass(self, name):
		"""
		Return the processing instruction class for the PI with the Python name
		:var:`name`. If the processing instruction can't be found an
		:exc:`IllegalProcInstError` will be raised.
		"""
		try:
			return self._procinstsbypyname[name]
		except KeyError:
			for base in self.bases:
				try:
					return base.procinstclass(name)
				except IllegalProcInstError:
					pass
			raise IllegalProcInstError(name, False)

	def procinstclass_xml(self, name):
		"""
		Return the processing instruction class for the PI with the XML name
		:var:`name`. If the processing instruction can't be found an
		:exc:`IllegalProcInstError` will be raised.
		"""
		try:
			return self._procinstsbyxmlname[name]
		except KeyError:
			for base in self.bases:
				try:
					return base.procinstclass_xml(name)
				except IllegalProcInstError:
					pass
			raise IllegalProcInstError(name, True)

	def procinst(self, name, content):
		"""
		Return a processing instruction object for the PI type with the Python
		target name :var:`name`.
		"""
		return self.procinstclass(name)(content)

	def procinst_xml(self, name, content):
		"""
		Return a processing instruction object for the PI type with the XML
		target name :var:`name`.
		"""
		return self.procinstclass_xml(name)(content)

	def hasprocinst(self, name):
		"""
		Is there a registered processing instruction class in :var:`self` for the
		PI with the Python name :var:`name`?
		"""
		return name in self._procinstsbypyname or any(base.hasprocinst(name) for base in self.bases)

	def hasprocinst_xml(self, name):
		"""
		Is there a registered processing instruction class in :var:`self` for the
		PI with the XML name :var:`name`?
		"""
		return name in self._procinstsbyxmlname or any(base.hasprocinst_xml(name) for base in self.bases)

	def entities(self):
		"""
		Return an iterator for all registered entity classes.
		"""
		seen = set()
		for entity in self._entitiesbypyname.values():
			yield entity
			seen.add(entity.xmlname)
		for base in self.bases:
			for entity in base.entities():
				if entity.xmlname not in seen:
					yield entity
					seen.add(entity.xmlname)

	def entityclass(self, name):
		"""
		Return the entity class for the entity with the Python name :var:`name`.
		If the entity can't be found an :exc:`IllegalEntityError` will be raised.
		"""
		try:
			return self._entitiesbypyname[name]
		except KeyError:
			for base in self.bases:
				try:
					return base.entityclass(name)
				except IllegalEntityError:
					pass
			raise IllegalEntityError(name, False)

	def entityclass_xml(self, name):
		"""
		Return the entity class for the entity with the XML name :var:`name`.
		If the entity can't be found an :exc:`IllegalEntityError` will be raised.
		"""
		try:
			return self._entitiesbyxmlname[name]
		except KeyError:
			for base in self.bases:
				try:
					return base.entityclass_xml(name)
				except IllegalEntityError:
					pass
			raise IllegalEntityError(name, True)

	def entity(self, name):
		"""
		Return an entity object for the entity with the Python name :var:`name`.
		"""
		return self.entityclass(name)()

	def entity_xml(self, name):
		"""
		Return an entity object for the entity with the XML name :var:`name`.
		"""
		return self.entityclass_xml(name)()

	def hasentity(self, name):
		"""
		Is there a registered entity class in :var:`self` for the entity with the
		Python name :var:`name`?
		"""
		return name in self._entitiesbypyname or any(base.hasentity(name) for base in self.bases)

	def hasentity_xml(self, name):
		"""
		Is there a registered entity class in :var:`self` for the entity with the
		XML name :var:`name`?
		"""
		return name in self._entitiesbyxmlname or any(base.hasentity_xml(name) for base in self.bases)

	def charrefs(self):
		"""
		Return an iterator for all character entity classes.
		"""
		seen = set()
		for charref in self._charrefsbypyname.values():
			yield charref
			seen.add(charref.xmlname)
		for base in self.bases:
			for charref in base.charrefs():
				if charref.xmlname not in seen:
					yield charref
					seen.add(charref.xmlname)

	def charrefclass(self, name):
		"""
		Return the character entity with the Python name :var:`name`.
		:var:`name` can also be an :class:`int` specifying the codepoint.
		If the character entity can't be found a :exc:`IllegalEntityError`
		will be raised.
		"""
		try:
			if isinstance(name, int):
				return self._charrefsbycodepoint[name]
			return self._charrefsbypyname[name]
		except KeyError:
			for base in self.bases:
				try:
					return base.charrefclass(name)
				except IllegalEntityError:
					pass
			raise IllegalEntityError(name, False)

	def charrefclass_xml(self, name):
		"""
		Return the character entity with the XML name :var:`name`.
		:var:`name` can also be an :class:`int` specifying the codepoint.
		If the character entity can't be found a :exc:`IllegalEntityError`
		will be raised.
		"""
		try:
			if isinstance(name, int):
				return self._charrefsbycodepoint[name]
			return self._charrefsbyxmlname[name]
		except KeyError:
			for base in self.bases:
				try:
					return base.charrefclass_xml(name)
				except IllegalEntityError:
					pass
			raise IllegalEntityError(name, True)

	def charref(self, name):
		"""
		Return a character entity object for the character with the Python name
		or codepoint :var:`name`.
		"""
		return self.charrefclass(name)()

	def charref_xml(self, name):
		"""
		Return a character entity object for the character with the XML name
		or codepoint :var:`name`.
		"""
		return self.charrefclass_xml(name)()

	def hascharref(self, name):
		"""
		Is there a registered character entity class in :var:`self` with the
		Python name or codepoint :var:`name`?
		"""
		if isinstance(name, int):
			has = name in self._charrefsbycodepoint
		else:
			has = name in self._charrefsbypyname
		return has or any(base.hascharref(name) for base in self.bases)

	def hascharref_xml(self, name):
		"""
		Is there a registered character entity class in :var:`self` with the XML
		name or codepoint :var:`name`?
		"""
		if isinstance(name, int):
			has = name in self._charrefsbycodepoint
		else:
			has = name in self._charrefsbypyname
		return has or any(base.hascharref_xml(name) for base in self.bases)

	def attrclass(self, name, xmlns):
		"""
		Return the attribute class for the global attribute with the Python name
		:var:`name` and the namespace :var:`xmlns`. If the attribute can't
		be found a :exc:`IllegalAttrError` will be raised.
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
		Return the attribute class for the global attribute with the XML name
		:var:`name` and the namespace :var:`xmlns`. If the attribute can't
		be found a :exc:`IllegalAttrError` will be raised.
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
		Create a text node with the content :var:`content`.
		"""
		return Text(content)

	def comment(self, content):
		"""
		Create a comment node with the content :var:`content`.
		"""
		return Comment(content)

	def __getattr__(self, key):
		try:
			return self._attrs[key]
		except KeyError:
			for base in self.bases:
				return getattr(base, key)
			raise AttributeError(key)


# Default pool (can be temporarily changed via ``with xsc.Pool() as pool:``)
class ThreadLocalPool(threading.local):
	pool = Pool()

threadlocalpool = ThreadLocalPool()


###
### Functions for namespace handling
###

def docpool():
	"""
	Return a pool suitable for parsing XIST docstrings.
	"""
	from ll.xist.ns import html, chars, abbr, doc, specials
	return Pool(doc, specials, html, chars, abbr)


def nsname(xmlns):
	"""
	If :var:`xmlns` is a module, return ``xmlns.xmlns``, else return
	:var:`xmlns` unchanged.
	"""
	if xmlns is not None and not isinstance(xmlns, str):
		xmlns = xmlns.xmlns
	return xmlns


def nsclark(xmlns):
	"""
	Return a namespace name in Clark notation. :var:`xmlns` can be :const:`None`,
	a string or a module.
	"""
	if xmlns is None:
		return "{}"
	elif not isinstance(xmlns, str):
		xmlns = xmlns.xmlns
	return "{{{}}}".format(xmlns)


# C0 Controls and Basic Latin
class quot(CharRef): "quotation mark = APL quote, U+0022 ISOnum"; codepoint = 34
class amp(CharRef): "ampersand, U+0026 ISOnum"; codepoint = 38
class lt(CharRef): "less-than sign, U+003C ISOnum"; codepoint = 60
class gt(CharRef): "greater-than sign, U+003E ISOnum"; codepoint = 62
class apos(CharRef): "apostrophe mark, U+0027 ISOnum"; codepoint = 39


###
### Location information
###

class Location(object):
	"""
	Represents a location in an XML entity.
	"""
	__slots__ = ("url", "line", "col", "char")

	def __init__(self, url=None, line=None, col=None):
		"""
		Create a new :class:`Location` object using the arguments passed in.
		:var:`url` is the URL/filename. :var:`line` is the line number and
		:var:`col` is the column number (both starting at 0).
		"""
		self.url = url
		self.line = line
		self.col = col

	def offset(self, offset):
		"""
		Return a location where the line number is incremented by offset
		(and the column number is reset to 0).
		"""
		if offset==0:
			return self
		elif self.line is None:
			return Location(url=self.url, col=0)
		return Location(url=self.url, line=self.line+offset, col=0)

	def __str__(self):
		url = str(self.url) if self.url is not None else "???"
		line = str(self.line) if self.line is not None else "?"
		col = str(self.col) if self.col is not None else "?"
		return "{}:{}:{}".format(url, line, col)

	def __repr__(self):
		return "{0.__class__.__name__}({1})".format(self, ", ".join("{}={!r}".format(attr, getattr(self, attr)) for attr in ("url", "line", "col") if getattr(self, attr) is not None))

	def __eq__(self, other):
		return self.__class__ is other.__class__ and self.url==other.url and self.line==other.line and self.col==other.col

	def __ne__(self, other):
		return not self==other
