# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This module contains all the central XML tree classes, exception and warning
classes and a few helper classes and functions.
"""


__docformat__ = "reStructuredText"


import sys, random, copy, warnings, threading, weakref, types, codecs

import cssutils

from ll import misc, url as url_, xml_codec


xml_xmlns = "http://www.w3.org/XML/1998/namespace"


###
### helpers
###

def tonode(value):
	"""
	Convert :obj:`value` to an XIST :class:`Node`.

	If :obj:`value` is a tuple or list, it will be (recursively) converted to a
	:class:`Frag`. Integers, strings, etc. will be converted to a :class:`Text`.
	If :obj:`value` is a :class:`Node` already, it will be returned unchanged.
	In the case of :const:`None` the XIST Null (:data:`ll.xist.xsc.Null`) will be
	returned. If :obj:`value` is iterable, a :class:`Frag` will be generated
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
			value = tuple(value)
		except TypeError:
			pass
		else:
			return Frag(*value)
	raise IllegalObjectError(value) # none of the above => bail out


class ThreadLocalNodeHander(threading.local):
	handler = None

threadlocalnodehandler = ThreadLocalNodeHander()


class build:
	"""
	A :class:`build` object can be used as a context handler to create a new
	XIST tree::

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


class addattr:
	"""
	An :class:`addattr` object can be used as a context handler to modify an
	attribute of an element::

		with xsc.build():
			with html.div() as e:
				with xsc.addattr("align"):
					+xsc.Text("right")
	"""

	def __init__(self, attrname):
		"""
		Create an :class:`addattr` object for adding to the attribute named
		:obj:`attrname` (which can be the Python name of an attribute or an
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
	:func:`add` appends items in :obj:`args` and sets attributes in
	:obj:`kwargs` in the currently active node in the :keyword:`with` stack.
	"""
	threadlocalnodehandler.handler.add(*args, **kwargs)


###
### Conversion context
###

class Context:
	"""
	This is an empty class that can be used by the :meth:`convert` method to
	hold element or namespace specific data during the :meth:`convert` call.
	The method :meth:`Converter.__getitem__` will return a unique instance of
	this class.
	"""


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
	Warning that is issued when an attribute has an illegal value.
	"""

	def __init__(self, attr):
		self.attr = attr

	def __str__(self):
		return f"Attribute value {str(self.attr)!r} not allowed for {nsclark(self.attr)}"


class RequiredAttrMissingWarning(Warning):
	"""
	Warning that is issued when a required attribute is missing.
	"""

	def __init__(self, attrs, attr):
		self.attrs = attrs
		self.attr = attr

	def __str__(self):
		return f"Required attribute {nsclark(self.attr)} missing in {self.attrs!r}"


class UndeclaredAttrWarning(Warning):
	"""
	Warning that is issued when a local attribute is not declared.
	"""

	def __init__(self, attrs, attr):
		self.attrs = attrs
		self.attr = attr

	def __str__(self):
		return f"Attribute {nsclark(self.attr)} is undeclared in {self.attrs!r}"


class UndeclaredNodeWarning(Warning):
	"""
	Warning that is issued when a node (i.e. element, entity or processing
	instruction) is not declared.
	"""

	def __init__(self, obj):
		self.obj = obj

	def __str__(self):
		return f"{self.obj!r} is undeclared"


class IllegalPrefixError(Error, LookupError):
	"""
	Exception that is raised when a namespace prefix is undefined.
	"""
	def __init__(self, prefix):
		self.prefix = prefix

	def __str__(self):
		return f"namespace prefix {self.prefix!r} is undefined"


class MultipleRootsError(Error):
	def __str__(self):
		return "can't add namespace attributes: XML tree has multiple roots"


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
		return f"{self.message}: {self.filename!r} not found ({self.exc})"


class IllegalObjectError(Error, TypeError):
	"""
	Exception that is raised when an XIST constructor gets passed an
	unconvertable object.
	"""

	def __init__(self, object):
		self.object = object

	def __str__(self):
		return f"can't convert object {self.object!r} of type {type(self.object).__name__} to an XIST node"


class IllegalCommentContentWarning(Warning):
	"""
	Warning that is issued when there is an illegal comment, i.e. one containing
	``--`` or ending in ``-``. (This can only happen when the comment was created
	by code, not when parsed from an XML file.)
	"""

	def __init__(self, comment):
		self.comment = comment

	def __str__(self):
		return f"comment with content {self.comment.content!r} is illegal, as it contains '--' or ends in '-'"


class IllegalProcInstFormatError(Error):
	"""
	Exception that is raised when there is an illegal processing instruction,
	i.e. one containing ``?>``. (This can only happen when the processing
	instruction was created by code, not when parsed from an XML file.)
	"""

	def __init__(self, procinst):
		self.procinst = procinst

	def __str__(self):
		return f"processing instruction with content {self.procinst.content!r} is illegal, as it contains '?>'"


warnings.simplefilter("always", category=Warning)


###
### Context containing state during :meth:`convert` calls
###

class ConverterState:
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


class Converter:
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

	def __getitem__(self, key):
		"""
		Return a context object for :obj:`key`. Two variants are supported:

		*	:obj:`key` may be a string, in which case it should be a hierarchical
			dot-separated name similar to Java package names (e.g.
			``"org.example.project.handler"``). This helps avoid name collisions.
			Context objects of this type must be explicitly created via
			:meth:`__setitem__`.

		*	:obj:`key` may be a :class:`ll.xist.xsc.Node` instance or subclass.
			Each of these classes that defines its own :class:`Context` class gets
			a unique instance of this class. This instance will be created on the
			first access and the element can store information there that needs to
			be available across calls to :meth:`convert`.
		"""
		if isinstance(key, str):
			return self.contexts[key]
		else:
			contextclass = key.Context
			# don't use :meth:`setdefault`, as constructing the context object might involve some overhead
			try:
				return self.contexts[contextclass]
			except KeyError:
				context = contextclass()
				self.contexts[contextclass] = context
				return context

	def __setitem__(self, key, value):
		self.contexts[key] = value


###
### Publisher for serializing XML trees to strings
###

class Publisher:
	"""
	A :class:`Publisher` object is used for serializing an XIST tree into a byte
	sequence.
	"""

	def __init__(self, encoding=None, xhtml=1, validate=False, prefixes={}, prefixdefault=False, hidexmlns=(), showxmlns=()):
		"""
		Create a publisher. Arguments have the following meaning:

		:obj:`encoding` : string or :const:`None`
			Specifies the encoding to be used for the byte sequence. If
			:const:`None` is used the encoding in the XML declaration will be used.
			If there is no XML declaration, UTF-8 will be used.

		:obj:`xhtml` : int
			With the parameter :obj:`xhtml` you can specify if you want HTML
			output:

			HTML (``xhtml==0``)
				Elements with a empty content model will be published as ``<foo>``.

			HTML browser compatible XML (``xhtml==1``)
				Elements with an empty content model will be published as ``<foo />``
				and others that just happen to be empty as ``<foo></foo>``. This is
				the default.

			Pure XML (``xhtml==2``)
				All empty elements will be published as ``<foo/>``.

		:obj:`validate` : bool
			Specifies whether validation should be done before publishing.

		:obj:`prefixes` : mapping
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

		:obj:`prefixdefault` : string or :const:`None`
			If an element or attribute is encountered whose namespace name is not
			in :obj:`prefixes` :obj:`prefixdefault` is used as the fallback.

		:obj:`hidexmlns` : list or set
			:obj:`hidexmlns` can be a list or set that contains namespace names
			for which no ``xmlns`` attributes should be published. (This can be
			used to hide the namespace declarations for e.g. Java taglibs.)

		:obj:`showxmlns` : list or set
			:obj:`showxmlns` can be a list or set that contains namespace names
			for which ``xmlns`` attributes *will* be published, even if there are
			no elements from this namespace in the tree.
		"""
		self.base = None
		self.allowschemerelurls = False
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
		Encode :obj:`text` with the encoding and error handling currently active
		and return the resulting byte string.
		"""
		return self.encoder.encode(text)

	def encodetext(self, text):
		"""
		Encode :obj:`test` as text data. :obj:`text` must be a :class:`str`
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
			prefix = f"ns{suffix}"
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
		:obj:`xmlns`. This honors the namespace configuration from ``self.prefixes``
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

	def getobjectprefix(self, obj):
		"""
		Get and register a namespace prefix for the namespace :obj:`obj` lives
		in (specified by the :attr:`xmlns` attribute of :obj:`obj`). Similar
		to :meth:`getnamespaceprefix` this honors the namespace configuration from
		``self.prefixes`` and ``self.prefixdefault`` (except when a global
		attribute requires a non-empty prefix).
		"""
		xmlns = getattr(obj, "xmlns")
		if xmlns is None:
			return None

		if xmlns == xml_xmlns: # We don't need a namespace mapping for the xml namespace
			prefix = "xml"
		else:
			emptyok = isinstance(obj, Element) # If it's e.g. a procinst assume we need a non-empty prefix
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

	def iterbytes(self, node, base=None, allowschemerelurls=False):
		"""
		Output the node :obj:`node`. This method is a generator that will yield
		the resulting XML byte sequence in fragments.
		"""
		if self.validate:
			for warning in node.validate(True, [node]):
				warnings.warn(warning)
		self._ns2prefix.clear()
		self._prefix2ns.clear()
		# iterate through every node in the tree
		for n in node.walknodes(Element, Attr, enterattrs=True):
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
					if isinstance(child, Element) and child.xmlns not in self.hidexmlns:
						count += 1
				if count > 1:
					raise MultipleRootsError()
			self._publishxmlns = True

		self.inattr = 0
		self.__textfilters = [ misc.xmlescape_text ]

		self.__errors = [ "xmlcharrefreplace" ]

		self.base = url_.URL(base)
		self.allowschemerelurls = allowschemerelurls
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

	def bytes(self, node, base=None, allowschemerelurls=False):
		"""
		Return a :class:`bytes` object in XML format for the XIST node :obj:`node`.
		"""
		return b"".join(self.iterbytes(node, base, allowschemerelurls))

	def iterstring(self, node, base=None, allowschemerelurls=False):
		"""
		A generator that will produce a serialized string of :obj:`node`.
		"""
		decoder = codecs.getincrementaldecoder("xml")(encoding=self.encoding)
		for part in self.iterbytes(node, base, allowschemerelurls):
			part = decoder.decode(part, False)
			if part:
				yield part
		part = decoder.decode(b"", True)
		if part:
			yield part

	def string(self, node, base=None, allowschemerelurls=False):
		"""
		Return a string for :obj:`node`.
		"""
		decoder = codecs.getdecoder("xml")
		result = self.bytes(node, base, allowschemerelurls)
		return decoder(result, encoding=self.encoding)[0]

	def write(self, stream, node, base=None, allowschemerelurls=False):
		"""
		Write :obj:`node` to the file-like object :obj:`stream` (which must
		provide a :meth:`write` method).
		"""
		for part in self.iterbytes(node, base, allowschemerelurls):
			stream.write(part)


###
### Cursor for the :meth:`walk` method
###

class Cursor:
	"""
	A :class:`Cursor` object is used by the :meth:`walk` method during tree
	traversal. It contains information about the state of the traversal and can
	be used to influence which parts of the tree are traversed and in which order.

	Information about the state of the traversal is provided in the following
	attributes:

	``root``
		The node where traversal has been started (i.e. the object for which the
		:meth:`walk` method has been called).

	``node``
		The current node being traversed.

	``path``
		A list of nodes that contains the path through the tree from the root to
		the current node (i.e. ``path[0] is root`` and ``path[-1] is node``).

	``index``
		A path of indices (e.g. ``[0, 1]`` if the current node is the second child
		of the first child of the root). Inside attributes the index path will
		contain the name of the attribute (or a (attribute name, namespace name)
		tuple inside a global attribute).

	``event``
		A string that specifies which event is currently handled. Possible values
		are: ``"enterelementnode"``, ``"leaveelementnode"``, ``"enterattrnode"``,
		``"leaveattrnode"``, ``"textnode"``, ``"commentnode"``, ``"doctypenode"``,
		``"procinstnode"``, ``"entitynode"`` and ``"nullnode"``.

	The following attributes specify which part of the tree should be traversed:

	``entercontent``
		Should the content of an element be entered?

	``enterattrs``
		Should the attributes of an element be entered? (Note that the attributes
		will always be entered before the content.)

	``enterattr``
		Should the content of the attributes of an element be entered? (This is
		only relevant if ``enterattrs`` is true.)

	``enterelementnode``
		Should the generator yield a ``"enterelementnode"`` event (i.e. return
		before entering the content or attributes of an element)?

	``leaveelementnode``
		Should the generator yield an ``"leaveelementnode"`` event (i.e. return
		after entering the content or attributes of an element)?

	``enterattrnode``
		Should the generator yield a ``"enterattrnode"`` event (i.e. return
		before entering the content of an attribute)? This is only relevant if
		``enterattrs`` is true.

	``leaveattrnode``
		Should the generator yield an ``"leaveattrnode"`` event (i.e. return
		after entering the content of an attribute)? This is only relevant if
		``enterattrs`` is true. Furthermore if ``enterattr`` is false, the
		behaviour is essentially the same as for ``enterattrnode``.

	Note that if any of these attributes is changed by the code consuming the
	generator, this new value will be used for the next traversal step once the
	generator is resumed and will be reset to its initial value (specified in
	the constructor) afterwards.
	"""
	def __init__(self, node, entercontent=True, enterattrs=False, enterattr=False, enterelementnode=True, leaveelementnode=False, enterattrnode=True, leaveattrnode=False):
		"""
		Create a new :class:`Cursor` object for a tree traversal rooted at the node
		:obj:`node`.

		The arguments :obj:`entercontent`, :obj:`enterattrs`, :obj:`enterattr`,
		:obj:`enterelementnode`, :obj:`leaveelementnode`, :obj:`enterattrnode` and
		:obj:`leaveattrnode` are used as the initial values for the attributes of
		the same name. (see the class docstring for info about their use).
		"""
		self.root = self.node = node
		self.path = [node]
		self.index = []
		self.event = None
		self.entercontent = self._entercontent = entercontent
		self.enterattrs = self._enterattrs = enterattrs
		self.enterattr = self._enterattr = enterattr
		self.enterelementnode = self._enterelementnode = enterelementnode
		self.leaveelementnode = self._leaveelementnode = leaveelementnode
		self.enterattrnode = self._enterattrnode = enterattrnode
		self.leaveattrnode = self._leaveattrnode = leaveattrnode

	def restore(self):
		"""
		Restore the attributes ``entercontent``, ``enterattrs``, ``enterattr``,
		``enterelementnode``, ``leaveelementnode``, ``enterattrnode`` and
		``leaveattrnode`` to their initial value.
		"""
		self.entercontent = self._entercontent
		self.enterattrs = self._enterattrs
		self.enterattr = self._enterattr
		self.enterelementnode = self._enterelementnode
		self.leaveelementnode = self._leaveelementnode
		self.enterattrnode = self._enterattrnode
		self.leaveattrnode = self._leaveattrnode


###
### The DOM classes and their meta classes
###

class _Node_Meta(type):
	def __new__(cls, name, bases, dict):
		if "register" not in dict:
			dict["register"] = True
		if "xmlname" not in dict:
			dict["xmlname"] = name
		return type.__new__(cls, name, bases, dict)

	def __repr__(self):
		return f"<class {self.__module__}:{self.__qualname__} at {id(self):#x}>"

	def _repr_pretty_(self, p, cycle):
		p.text(repr(self))

	def __contains__(self, path):
		from ll.xist import xfind
		return path in xfind.IsInstanceSelector(self)

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
	Base class for nodes in the document tree. Derived classes may
	overwrite :meth:`convert` or :meth:`publish`.
	"""

	# location of this node in the XML file (will be hidden in derived classes,
	# but is specified here, so that no special tests are required. In derived
	# classes this will be set by the parser)
	startloc = None
	endloc = None

	# Subclasses relevant for parsing (i.e. Element, ProcInst and Entity)
	# have an additional class attribute named register. This attribute may have
	# two values:
	# :const:`False`: Don't register for parsing.
	# :const:`True`:  Use for parsing.
	# If register is not set it defaults to :const:`True`

	Context = Context

	prettyindentbefore = 0
	prettyindentafter = 0

	def __repr__(self):
		return f"<{self.__module__}:{self.__qualname__} object at {id(self):#x}>"

	def __ne__(self, other):
		return not self == other

	xmlname = None
	xmlns = None

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
		Return a clone of :obj:`self`. Compared to :meth:`deepcopy` :meth:`clone`
		will create multiple instances of objects that can be found in the tree
		more than once. :meth:`clone` can't clone trees that contain cycles.
		"""
		return self

	def copy(self):
		"""
		Return a shallow copy of :obj:`self`.
		"""
		return self.__copy__()

	def __copy__(self):
		return self

	def deepcopy(self):
		"""
		Return a deep copy of :obj:`self`.
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

		:meth:`conv` will automatically set ``:obj:`converter`.node`` to :obj:`self`
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
		Implementation of the conversion method. When you define your own element
		classes you have to overwrite this method and implement the desired
		conversion.

		This method must return an instance of :class:`Node`. It may *not* change
		:obj:`self`.
		"""

	@misc.notimplemented
	def __str__(self):
		"""
		Return the character content of :obj:`self` as a string. This means that
		comments and processing instructions will be filtered out.
		For elements you'll get the element content.

		:meth:`__str__` can be used everywhere where a plain string
		representation of the node is required.

		For example::

			>>> from ll.xist.ns import html
			>>> e = html.html(
			...    html.head(
			...       html.title("The page")
			...    ),
			...    html.body(
			...       html.h1("The header"),
			...       html.p("The content", class_="content")
			...    )
			... )
			>>> print(e)
			The pageThe headerThe content
		"""
		pass

	def __int__(self):
		"""
		Convert the character content of :obj:`self` to an :class:`int`.
		"""
		return int(str(self))

	def asFloat(self, decimal=".", ignore=""):
		"""
		Convert the character content of :obj:`self` to an :class:`float`.
		:obj:`decimal` specifies which decimal separator is used in the value
		(e.g. ``"."`` (the default) or ``","``). :obj:`ignore` specifies which
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
		Convert the character content of :obj:`self` to an :class:`float`.
		"""
		return self.asFloat()

	def __complex__(self):
		"""
		Convert the character content of :obj:`self` to an :class:`complex`.
		"""
		return complex(str(self))

	def parsed(self, parser, event):
		"""
		This method will be called by the parser :obj:`parser` once after
		:obj:`self` is created by the parser (This is used e.g. by
		:class:`URLAttr` to incorporate the base URL into the attribute).

		:obj:`event` is the parser event that initiated the call.
		"""

	def validate(self, recursive=True, path=None):
		"""
		This method will be called when parsing or publishing to check whether
		:obj:`self` is valid.

		If :obj:`self` is found to be invalid a warning should be issued through
		the Python warning framework.
		"""
		yield from ()

	@misc.notimplemented
	def publish(self, publisher):
		"""
		Generate unicode strings for the node. :obj:`publisher` must be an
		instance of :class:`ll.xist.xsc.Publisher`.

		The encoding and xhtml specification are taken from the :obj:`publisher`.
		"""

	def iterbytes(self, base=None, allowschemerelurls=False, publisher=None, **publishargs):
		"""
		A generator that will produce this node as a serialized byte string. (i.e.
		it will output what the method :meth:`bytes` outputs, but incremetally).

		For the possible parameters see the :class:`ll.xist.xsc.Publisher`
		constructor.
		"""
		if publisher is None:
			publisher = Publisher(**publishargs)

		return publisher.iterbytes(self, base, allowschemerelurls) # return a generator-iterator

	def bytes(self, base=None, allowschemerelurls=False, publisher=None, **publishargs):
		"""
		Return :obj:`self` as a serialized bytes object.

		For the possible parameters see the :class:`ll.xist.xsc.Publisher`
		constructor.

		For example::

			>>> from ll.xist.ns import html
			>>> e = html.div(
			...    html.h1("The header"),
			...    html.p("The content", class_="content")
			... )
			>>> print(e.bytes())
			b'<div><h1>The header</h1><p class="content">The content</p></div>'
		"""
		if publisher is None:
			publisher = Publisher(**publishargs)

		return publisher.bytes(self, base, allowschemerelurls)

	def iterstring(self, base=None, allowschemerelurls=False, publisher=None, **publishargs):
		"""
		A generator that will produce a serialized string of :obj:`self` (i.e.
		it will output what the method :meth:`string` outputs, but incremetally).

		For the possible parameters see the :class:`ll.xist.xsc.Publisher`
		constructor.
		"""
		if publisher is None:
			publisher = Publisher(**publishargs)

		return publisher.iterstring(self, base, allowschemerelurls) # return a generator-iterator

	def string(self, base=None, allowschemerelurls=False, publisher=None, **publishargs):
		"""
		Return a serialized (unicode) string for :obj:`self`.

		For the possible parameters see the :class:`ll.xist.xsc.Publisher`
		constructor.

		For example::

			>>> from ll.xist.ns import html
			>>> e = html.div(
			...    html.h1("The header"),
			...    html.p("The content", class_="content")
			... )
			>>> print(e.string())
			<div><h1>The header</h1><p class="content">The content</p></div>
		"""
		if publisher is None:
			publisher = Publisher(**publishargs)
		return publisher.string(self, base, allowschemerelurls)

	def write(self, stream, base=None, allowschemerelurls=False, publisher=None, **publishargs):
		"""
		Write :obj:`self` to the file-like object :obj:`stream` (which must provide
		a :meth:`write` method).

		For the rest of the parameters see the :class:`ll.xist.xsc.Publisher`
		constructor.
		"""
		if publisher is None:
			publisher = Publisher(**publishargs)
		return publisher.write(stream, self, base, allowschemerelurls)

	def _walk(self, cursor):
		yield cursor
		cursor.restore()

	def walk(self, *selectors, entercontent=True, enterattrs=False, enterattr=False, enterelementnode=True, leaveelementnode=False, enterattrnode=True, leaveattrnode=False):
		"""
		Return an iterator for traversing the tree rooted at :obj:`self`.

		Each item produced by the iterator is a :class:`Cursor` object.
		It contains information about the state of the traversal and can be used
		to influence which parts of the tree are traversed and in which order.

		:obj:`selectors` is used for filtering which nodes to return from the
		iterator. The arguments :obj:`entercontent`, :obj:`enterattrs`,
		:obj:`enterattr`, :obj:`enterelementnode`, :obj:`leaveelementnode`,
		:obj:`enterattrnode` and :obj:`leaveattrnode` specify how the tree should
		be traversed. For more information see the :class:`Cursor` class.

		Note that the :class:`Cursor` object is reused by :meth:`walk`, so you
		can't rely on any attributes remaining the same across calls to
		:func:`next`.

		The following example shows how to extract the text of an HTML ``label``
		element for an input element with a specified HTML id::

			from ll import misc
			from ll.xist import xsc, xfind
			from ll.xist.ns import html

			def label(doc, id):
				label = misc.first(doc.walk(xfind.attrhasvalue("for", id)), None)
				if label is None:
					return None
				texts = []
				for c in label.node.walk(html.textarea, xsc.Text):
					if isinstance(c.node, html.textarea):
						c.entercontent = False
					else:
						texts.append(str(c.node))
				return " ".join("".join(texts).split()).strip()

			doc = html.div(
				html.p(
					html.label(
						"Input your text here: ",
						html.textarea("Default value", rows=20, cols=80, id="foo"),
						" (just a test)",
						for_="foo",
					)
				)
			)

			print(repr(label(doc, "foo")))

		This will output::

			'Input your text here: (just a test)'
		"""
		cursor = Cursor(self, entercontent=entercontent, enterattrs=enterattrs, enterattr=enterattr, enterelementnode=enterelementnode, leaveelementnode=leaveelementnode, enterattrnode=enterattrnode, leaveattrnode=leaveattrnode)
		if selectors:
			from ll.xist import xfind
			return xfind.filter(self._walk(cursor), *selectors)
		else:
			return self._walk(cursor)

	def walknodes(self, *selectors, entercontent=True, enterattrs=False, enterattr=False, enterelementnode=True, leaveelementnode=False, enterattrnode=True, leaveattrnode=False):
		"""
		Return an iterator for traversing the tree. The arguments have the same
		meaning as those for :meth:`walk`. The items produced by the iterator
		are the nodes themselves.
		"""
		cursor = Cursor(self, entercontent=entercontent, enterattrs=enterattrs, enterattr=enterattr, enterelementnode=enterelementnode, leaveelementnode=leaveelementnode, enterattrnode=enterattrnode, leaveattrnode=leaveattrnode)
		from ll.xist import xfind
		selector = xfind.selector(*selectors)
		return misc.Iterator(c.path[-1] for c in self._walk(cursor) if c.path in selector)

	def walkpaths(self, *selectors, entercontent=True, enterattrs=False, enterattr=False, enterelementnode=True, leaveelementnode=False, enterattrnode=True, leaveattrnode=False):
		"""
		Return an iterator for traversing the tree. The arguments have the same
		meaning as those for :meth:`walk`. The items produced by the iterator
		are copies of the path.
		"""
		cursor = Cursor(self, entercontent=entercontent, enterattrs=enterattrs, enterattr=enterattr, enterelementnode=enterelementnode, leaveelementnode=leaveelementnode, enterattrnode=enterattrnode, leaveattrnode=leaveattrnode)
		from ll.xist import xfind
		selector = xfind.selector(*selectors)
		return misc.Iterator(c.path[:] for c in self._walk(cursor) if c.path in selector)

	def compacted(self):
		"""
		Return a version of :obj:`self`, where textnodes or character references
		that contain only linefeeds are removed, i.e. potentially useless
		whitespace is removed.
		"""
		return self

	def _decoratenode(self, node):
		# Decorate the :class:`Node` :obj:`node` with the same location
		# information as :obj:`self`.

		node.startloc = self.startloc
		node.endloc = self.endloc
		return node

	def mapped(self, function, converter=None, **converterargs):
		"""
		Return the node mapped through the function :obj:`function`. This call
		works recursively (for :class:`Frag` and :class:`Element`).

		When you want an unmodified node you simply can return :obj:`self`.
		:meth:`mapped` will make a copy of it and fill the content recursively.
		Note that element attributes will not be mapped. When you return a
		different node from :func:`function` this node will be incorporated
		into the result as-is.
		"""
		if converter is None:
			converter = Converter(**converterargs)
		node = function(self, converter)
		assert isinstance(node, Node), f"the mapped method returned the illegal object {node!r} (type {type(node)!r}) when mapping {self!r}"
		return node

	def normalized(self):
		"""
		Return a normalized version of :obj:`self`, which means that consecutive
		:class:`Text` nodes are merged.
		"""
		return self

	def __mul__(self, factor):
		"""
		Return a :class:`Frag` with :obj:`factor` times the node as an entry.
		Note that the node will not be copied, i.e. this is a
		"shallow :meth:`__mul__`".
		"""
		return Frag(*factor*[self])

	def __rmul__(self, factor):
		"""
		Return a :class:`Frag` with :obj:`factor` times the node as an entry.
		"""
		return Frag(*[self]*factor)

	def pretty(self, level=0, indent="\t"):
		"""
		Return a prettyfied version of :obj:`self`, i.e. one with properly nested
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

	def __repr__(self):
		if self.startloc is not None:
			loc = f" location={str(self.startloc)!r}"
		else:
			loc = ""
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} content={self.content!r}{loc} at {id(self):#x}>"

	def _repr_pretty_(self, p, cycle):
		with p.group(4, f"<{self.__class__.__module__}.{self.__class__.__qualname__}", ">"):
			p.breakable()
			p.text(f"content={self.content!r}")
			if self.startloc is not None:
				p.breakable()
				p.text(f"location={str(self.startloc)!r}")
			p.breakable()
			p.text(f"at {id(self):#x}")

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
		if self.__class__ is other.__class__:
			return self._content == other._content
		return NotImplemented

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


class Text(CharacterData):
	"""
	A text node. The characters ``<``, ``>``, ``&`` (and ``"`` inside
	attributes) will be "escaped" with the appropriate character entities when
	this node is published.
	"""

	def __str__(self):
		return self._content

	def _str(self):
		return "text"

	def convert(self, converter):
		return self

	def publish(self, publisher):
		yield publisher.encodetext(self._content)

	def present(self, presenter):
		return presenter.presentText(self) # return a generator-iterator

	def compacted(self):
		return Null if self.content.isspace() else self

	def pretty(self, level=0, indent="\t"):
		return self

	def _walk(self, cursor):
		cursor.event = "textnode"
		yield cursor
		cursor.restore()


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

	def __repr__(self):
		l = len(self)
		if l == 0:
			childcount = "no children"
		elif l == 1:
			childcount = "1 child"
		else:
			childcount = f"{l:,} children"
		loc = f" location={str(self.startloc)!r}" if self.startloc is not None else ""
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object ({childcount}){loc} at {id(self):#x}>"

	def _repr_pretty_(self, p, cycle):
		with p.group(4, f"<{self.__class__.__module__}.{self.__class__.__qualname__}", ">"):
			if self.startloc is not None:
				p.breakable()
				p.text(f"location={str(self.startloc)!r}")
			if cycle:
				p.text("...")
			for child in self:
				p.breakable()
				p.pretty(child)
			p.breakable()
			p.text(f"at {id(self):#x}")

	def __str__(self):
		return "".join(str(child) for child in self)

	def _str(self):
		return "fragment"

	def __enter__(self):
		return threadlocalnodehandler.handler.enter(self)

	def __exit__(self, type, value, traceback):
		threadlocalnodehandler.handler.exit()

	def __call__(self, *content):
		self.extend(content)
		return self

	def _create(self):
		"""
		internal helper that is used to create an empty clone of :obj:`self`.
		"""
		# This is overwritten by :class:`Attr` to insure that attributes don't
		# get initialized with the default value when used in various methods
		# that create new attributes.
		return self.__class__()

	def clear(self):
		"""
		Make :obj:`self` empty.
		"""
		del self[:]

	def convert(self, converter):
		node = self._create()
		for child in self:
			convertedchild = child.convert(converter)
			assert isinstance(convertedchild, Node), f"the convert method returned the illegal object {convertedchild!r} (type {type(convertedchild)!r}) when converting {self!r}"
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

	def __eq__(self, other):
		if self.__class__ is other.__class__:
			return list.__eq__(self, other)
		return NotImplemented

	def validate(self, recursive=True, path=None):
		if path is None:
			path = []
		path.append(None)
		for child in self:
			path[-1] = child
			yield from child.validate(recursive, path)
		path.pop()

	def publish(self, publisher):
		for child in self:
			yield from child.publish(publisher)

	def __getitem__(self, index):
		"""
		Return the :obj:`index`'th node of the content of the fragment. If
		:obj:`index` is a list :meth:`__getitem__` will work recursively.
		If :obj:`index` is an empty list, :obj:`self` will be returned.
		:meth:`__getitem__` also supports selectors (i.e. :class:`xfind.Selector`
		objects).
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

			def iterate(selector):
				path = [self, None]
				for child in self:
					path[-1] = child
					if path in selector:
						yield child
			return misc.Iterator(iterate(xfind.selector(index)))

	def __setitem__(self, index, value):
		"""
		Allows you to replace the :obj:`index`'th content node of the fragment
		with the new value :obj:`value` (which will be converted to a node).
		If  :obj:`index` is a list :meth:`__setitem__` will be applied to the
		innermost index after traversing the rest of :obj:`index` recursively.
		If :obj:`index` is an empty list, an exception will be raised.
		:meth:`__setitem__` also supports selectors (i.e. :class:`xfind.Selector`
		objects).
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
			if index == -1:
				l = len(self)
				list.__setitem__(self, slice(l-1, l), value)
			else:
				list.__setitem__(self, slice(index, index+1), value)
		elif isinstance(index, slice):
			list.__setitem__(self, index, Frag(value))
		else:
			from ll.xist import xfind
			selector = xfind.selector(index)
			value = Frag(value)
			newcontent = []
			path = [self, None]
			for child in self:
				path[-1] = child
				if path in selector:
					newcontent.extend(value)
				else:
					newcontent.append(child)
			list.__setitem__(self, slice(0, len(self)), newcontent)

	def __delitem__(self, index):
		"""
		Remove the :obj:`index`'th content node from the fragment. If :obj:`index`
		is a list, the innermost index will be deleted, after traversing the rest
		of :obj:`index` recursively. If :obj:`index` is an empty list, an
		exception will be raised. Anything except :class:`list`, :class:`int` and
		:class:`slice` objects will be turned into a selector (i.e. an
		:class:`xfind.Selector` objects) and any child node matching this selector
		will be deleted from :obj:`self`.
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
			selector = xfind.selector(index)
			list.__setitem__(self, slice(0, len(self)), [child for child in self if [self, child] not in selector])

	def __mul__(self, factor):
		"""
		Return a :class:`Frag` with :obj:`factor` times the content of :obj:`self`.
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
		Append every item in :obj:`others` to :obj:`self`.
		"""
		for other in others:
			other = tonode(other)
			if isinstance(other, Frag):
				list.extend(self, other)
			elif other is not Null:
				list.append(self, other)

	def extend(self, items):
		"""
		Append all items from the sequence :obj:`items` to :obj:`self`.
		"""
		self.append(items)

	def insert(self, index, *others):
		"""
		Insert all items in :obj:`others` at the position :obj:`index`. (this is
		the same as ``self[index:index] = others``)
		"""
		other = Frag(*others)
		list.__setitem__(self, slice(index, index), other)

	def compacted(self):
		node = self._create()
		for child in self:
			compactedchild = child.compacted()
			assert isinstance(compactedchild, Node), f"the compact method returned the illegal object {compactedchild!r} (type {type(compactedchild)!r}) when compacting {child!r}"
			if compactedchild is not Null:
				list.append(node, compactedchild)
		return self._decoratenode(node)

	def withsep(self, separator, clone=False):
		"""
		Return a version of :obj:`self` with a separator node between the nodes of
		:obj:`self`.

		if :obj:`clone` is false, one node will be inserted several times, if
		:obj:`clone` is true, clones of this node will be used.
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
		Return a reversed version of the :obj:`self`.
		"""
		node = list(self)
		node.reverse()
		return self.__class__(node)

	def filtered(self, function):
		"""
		Return a filtered version of the :obj:`self`, i.e. a copy of :obj:`self`,
		where only content nodes for which :func:`function` returns true will
		be copied.
		"""
		node = self._create()
		list.extend(node, (child for child in self if function(child)))
		return node

	def shuffled(self):
		"""
		Return a shuffled version of :obj:`self`, i.e. a copy of :obj:`self` where the
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
		assert isinstance(node, Node), f"the mapped method returned the illegal object {node!r} (type {type(node)!r}) when mapping {self!r}"
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

	def _walk(self, cursor):
		# ``Frag``\s don't get tested
		cursor.path.append(None)
		cursor.index.append(-1)
		for child in self:
			cursor.path[-1] = cursor.node = child
			cursor.index[-1] += 1
			yield from child._walk(cursor)
		cursor.path.pop()
		cursor.index.pop()
		cursor.node = cursor.path[-1]


class Comment(CharacterData):
	"""
	An XML comment.
	"""

	def __str__(self):
		return ""

	def _str(self):
		return "comment"

	def convert(self, converter):
		return self

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

	def _walk(self, cursor):
		cursor.event = "commentnode"
		yield cursor
		cursor.restore()


class _DocType_Meta(type(Node)):
	def __repr__(self):
		return f"<doctype class {self.__module__}:{self.__name__} at {id(self):#x}>"


class DocType(CharacterData, metaclass=_DocType_Meta):
	"""
	An XML document type declaration.
	"""

	def convert(self, converter):
		return self

	def __str__(self):
		return ""

	def present(self, presenter):
		return presenter.presentDocType(self) # return a generator-iterator

	def publish(self, publisher):
		if not publisher.inattr:
			yield publisher.encode("<!DOCTYPE ")
			yield publisher.encode(self.content)
			yield publisher.encode(">")

	def _walk(self, cursor):
		cursor.event = "doctypenode"
		yield cursor
		cursor.restore()


class _ProcInst_Meta(type(Node)):
	def __new__(cls, name, bases, dict):
		self = super(_ProcInst_Meta, cls).__new__(cls, name, bases, dict)
		if dict.get("register") is not None: # check here as the pool isn't defined yet
			threadlocalpool.pool.register(self)
		return self

	def __repr__(self):
		if self.xmlname != self.__name__:
			xmlname = f" xmlname={self.xmlname!r}"
		else:
			xmlname = ""
		return f"<procinst class {self.__module__}:{self.__name__}{xmlname} at {id(self):#x}>"


class ProcInst(CharacterData, metaclass=_ProcInst_Meta):
	"""
	Base class for processing instructions.

	Processing instructions for specific targets must be implemented as
	subclasses of :class:`ProcInst`.
	"""

	register = None

	def __repr__(self):
		if self.xmlname != self.__class__.__name__:
			xmlname = f" xmlname={self.xmlname!r}"
		else:
			xmlname = ""
		if self.startloc is not None:
			loc = f" location={str(self.startloc)!r}"
		else:
			loc = ""
		return f"<procinst {self.__class__.__module__}.{self.__class__.__qualname__}{xmlname} content={self.content!r}{loc} at {id(self):#x}>"

	def _repr_pretty_(self, p, cycle):
		with p.group(4, f"<procinst {self.__class__.__module__}.{self.__class__.__qualname__}", ">"):
			if self.xmlname != self.__class__.__name__:
				p.breakable()
				p.text(f"xmlname={self.xmlname!r}")
			p.breakable()
			p.text(f"content={self.content!r}")
			if self.startloc is not None:
				p.breakable()
				p.text(f"location={str(self.startloc)!r}")
			p.breakable()
			p.text(f"at {id(self):#x}")

	def __str__(self):
		return ""

	def _str(self):
		return f"processing instruction {self.xmlname}"

	def __eq__(self, other):
		if isinstance(other, ProcInst):
			return self.xmlname == other.xmlname and self._content == other._content
		return NotImplemented

	def validate(self, recursive=True, path=None):
		if self.__class__ is ProcInst:
			yield UndeclaredNodeWarning(self)

	def convert(self, converter):
		return self

	def present(self, presenter):
		return presenter.presentProcInst(self) # return a generator-iterator

	def publish(self, publisher):
		content = self.content
		if "?>" in content:
			raise IllegalProcInstFormatError(self)
		yield publisher.encode(f"<?{self.xmlname} {content}?>")

	def _walk(self, cursor):
		cursor.event = "procinstnode"
		yield cursor
		cursor.restore()

	def __mul__(self, n):
		return Node.__mul__(self, n) # don't inherit ``CharacterData.__mul__``

	def __rmul__(self, n):
		return Node.__rmul__(self, n) # don't inherit ``CharacterData.__rmul__``


class Null(CharacterData):
	"""
	node that does not contain anything.
	"""

	def __repr__(self):
		return "ll.xist.xsc.Null"

	def _repr_pretty_(self, p, cycle):
		p.text(f"<{self.__class__.__module__}.{self.__class__.__qualname__} at {id(self):#x}>")

	def __str__(self):
		return ""

	def _str(self):
		return "null"

	def convert(self, converter):
		return self

	def publish(self, publisher):
		if False:
			yield ""

	def present(self, presenter):
		return presenter.presentNull(self) # return a generator-iterator

	def _walk(self, cursor):
		cursor.event = "nullnode"
		yield cursor
		cursor.restore()


Null = Null() # Singleton, the Python way


class _Attr_Meta(type(Frag)):
	def __new__(cls, name, bases, dict):
		# can be overwritten in subclasses, to specify that this attributes is required
		if "required" in dict:
			dict["required"] = bool(dict["required"])
		# convert the default to a Frag
		if "default" in dict:
			dict["default"] = Frag(dict["default"])
		# convert the entries in values to strings
		if "values" in dict:
			values = dict["values"]
			if values is not None:
				dict["values"] = tuple(str(entry) for entry in values)
		self = super(_Attr_Meta, cls).__new__(cls, name, bases, dict)
		if self.xmlns is not None:
			threadlocalpool.pool.register(self)
		return self

	def __repr__(self):
		if self.xmlname != self.__name__:
			xmlname = f" xmlname={self.xmlname!r}"
		else:
			xmlname = ""
		if self.xmlns is not None:
			isglobal = "global "
			xmlns = f" xmlns={self.xmlns!r}"
		else:
			isglobal = ""
			xmlns = ""
		return f"<{isglobal}attribute class {self.__module__}:{self.__qualname__}{xmlname}{xmlns} at {id(self):#x}>"


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
		>>> print(node.string())
		<img alt="EGGS" src="<?php echo 'eggs.gif'?>" />
	"""
	required = False
	default = None
	values = None

	def __repr__(self):
		if self.xmlname != self.__class__.__name__:
			xmlname = f" xmlname={self.xmlname!r}"
		else:
			xmlname = ""

		if self.xmlns is not None:
			isglobal = "global "
			xmlns = f" xmlns={self.xmlns!r}"
		else:
			isglobal = ""
			xmlns = ""

		l = len(self)
		if l == 0:
			childcount = "no children"
		elif l == 1:
			childcount = "1 child"
		else:
			childcount = f"{l:,} children"

		loc = f" location={str(self.startloc)!r}" if self.startloc is not None else ""

		return f"<{isglobal}attribute {self.__class__.__module__}.{self.__class__.__qualname__}{xmlns}{xmlname} ({childcount}){loc} at {id(self):#x}>"

	def _repr_pretty_(self, p, cycle):
		isglobal = "global " if self.xmlns is not None else ""
		with p.group(4, f"<{isglobal}attribute {self.__class__.__module__}.{self.__class__.__qualname__}", ">"):
			if self.xmlns is not None:
				p.breakable()
				p.text(f"xmlns={self.xmlns!r}")
			if self.xmlname != self.__class__.__name__:
				p.breakable()
				p.text(f"xmlname={self.xmlname!r}")
			if self.startloc is not None:
				p.breakable()
				p.text(f"location={str(self.startloc)!r}")
			if cycle:
				p.breakable()
				p.text("...")
			else:
				for child in self:
					p.breakable()
					p.pretty(child)
			p.breakable()
			p.text(f"at {id(self):#x}")

	def _str(self):
		if self.xmlns is not None:
			return f"attribute {{{self.xmlns}}}{self.xmlname}"
		else:
			return f"attribute {self.xmlname}"

	def _create(self):
		node = self.__class__()
		if self.__class__ is Attr:
			node.xmlname = self.xmlname
			node.xmlns = self.xmlns
		return node

	def isfancy(self):
		"""
		Return whether :obj:`self` contains nodes other than :class:`Text`.
		"""
		for child in self:
			if not isinstance(child, Text):
				return True
		return False

	def present(self, presenter):
		return presenter.presentAttr(self) # return a generator-iterator

	def validate(self, recursive=True, path=None):
		"""
		Check whether :obj:`self` has an allowed value, i.e. one that is specified
		in the class attribute ``values``. If the value is not allowed a warning
		will be issued through the Python warning framework.

		If :obj:`self` is "fancy" (i.e. contains non-:class:`Text` nodes), no
		check will be done.
		"""
		if path is None:
			path = []
		values = self.__class__.values
		if self and isinstance(values, tuple) and not self.isfancy():
			value = str(self)
			if value not in values:
				yield IllegalAttrValueWarning(self)
		yield from Frag.validate(self, True, path)

	def _publishname(self, publisher):
		if self.xmlns is not None:
			prefix = publisher._ns2prefix.get(self.xmlns) if self.xmlns != xml_xmlns else "xml"
			if prefix is not None:
				return f"{prefix}:{self.xmlname}"
		return self.xmlname

	def _publishattrvalue(self, publisher):
		# Internal helper that is used to publish the attribute value
		# (can be overwritten in subclass (done by e.g. :class:`StyleAttr` and
		# :class:`URLAttr`)
		return Frag.publish(self, publisher)

	def publish(self, publisher):
		if len(self) == 1 and isinstance(self[0], AttrElement):
			yield from self[0].publishattr(publisher, self)
		else:
			publisher.inattr += 1
			yield publisher.encode(f' {self._publishname(publisher)}="')
			publisher.pushtextfilter(misc.xmlescape_attr)
			yield from self._publishattrvalue(publisher)
			publisher.poptextfilter()
			yield publisher.encode('"')
			publisher.inattr -= 1

	def pretty(self, level=0, indent="\t"):
		return self.clone()

	def _walk(self, cursor):
		if cursor.enterattrnode:
			cursor.event = "enterattrnode"
			yield cursor
			# The user may have altered ``cursor`` attributes outside the generator
			enterattr = cursor.enterattr
			leaveattrnode = cursor.leaveattrnode
			cursor.restore()
		else:
			# These are the initial options
			enterattr = cursor.enterattr
			leaveattrnode = cursor.leaveattrnode
		if enterattr:
			yield from Frag._walk(self, cursor)
		if leaveattrnode:
			cursor.event = "leaveattrnode"
			yield cursor
			cursor.restore()


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
		if len(self) == 1 and isinstance(self[0], AttrElement):
			yield from self[0].publishboolattr(publisher, self)
		else:
			publisher.inattr += 1
			name = self._publishname(publisher)
			yield publisher.encode(f" {name}")
			if publisher.xhtml > 0:
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
		stylesheet = cssutils.parseString(f"a{{{self}}}")
		css.replaceurls(stylesheet, replacer)
		return stylesheet.cssRules[0].style.getCssText(separator=" ")

	def replaceurls(self, replacer):
		"""
		Replace each URL in the style. Each URL will be passed to the callable
		:obj:`replacer` and replaced with the returned value.
		"""
		self[:] = self._transform(replacer)

	def parsed(self, parser, event):
		if event == "leaveattrns" and not self.isfancy() and parser.base is not None:
			def prependbase(u):
				return parser.base/u
			self.replaceurls(prependbase)

	def _publishattrvalue(self, publisher):
		if not self.isfancy() and publisher.base is not None:
			def reltobase(u):
				return u.relative(publisher.base, publisher.allowschemerelurls)
			yield from Frag(self._transform(reltobase)).publish(publisher)
		else:
			yield from super(StyleAttr, self)._publishattrvalue(publisher)

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
		s = cssutils.parseString(f"a{{{self}}}")
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
			new = Attr(url_.URL(str(self)).relative(publisher.base, publisher.allowschemerelurls))
			return new._publishattrvalue(publisher)

	def asURL(self):
		"""
		Return :obj:`self` as a :class:`URL` object (note that non-:class:`Text`
		content will be filtered out).
		"""
		return url_.URL(Attr.__str__(self))

	def forInput(self, root=None):
		"""
		return a :class:`URL` pointing to the real location of the referenced
		resource. :obj:`root` must be the root URL relative to which :obj:`self`
		will be interpreted and usually comes from the ``root`` attribute of the
		:obj:`converter` argument in :meth:`convert`.
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
		self._defaultattrs = weakref.WeakValueDictionary() # map XML name to attribute class with default value

		# go through the attributes and register them in the cache
		for key in dir(self):
			value = getattr(self, key)
			if isinstance(value, _Attr_Meta):
				self.add(value)
		return self

	def __repr__(self):
		l = len(self._bypyname)
		if l == 0:
			attrcount = "no attrs"
		elif l == 1:
			attrcount = "1 attr"
		else:
			attrcount = f"{l:,} attrs"
		return f"<attributes class {self.__module__}:{self.__qualname__} ({attrcount}) at {id(self):#x}>"

	def _attrinfo(self, name):
		if isinstance(name, str):
			if name.startswith("{"):
				name = name[1:].partition("}")
				if name[1] is not None:
					return (name[0], name[2], self._byxmlname.get((name[0], name[2]), Attr))
			try:
				attrclass = self._byxmlname[(None, name)]
			except KeyError:
				return (None, name, Attr)
			else:
				return (attrclass.xmlns or self.xmlns, attrclass.xmlname, attrclass)
		elif isinstance(name, tuple):
			xmlns = nsname(name[0])
			return (xmlns, name[1], self._byxmlname.get((xmlns, name[1]), Attr))
		elif isinstance(name, _Attr_Meta):
			return (name.xmlns, name.xmlname, name)
		elif isinstance(name, Attr):
			return (name.xmlns, name.xmlname, name.__class__)
		else:
			raise TypeError(f"can't handle attribute name {name!r}")

	def __contains__(self, key):
		(attrxmlns, attrname, attrclass) = self._attrinfo(key)
		return (attrxmlns, attrname) in self._byxmlname


class Attrs(Node, dict, metaclass=_Attrs_Meta):
	"""
	An attribute map. Predefined attributes can be declared through nested
	subclasses of :class:`Attr`.
	"""

	def __init__(self, *args, **kwargs):
		dict.__init__(self)
		# set default attribute values
		for value in self._defaultattrs.values():
			self[value] = value.default.clone()
		# update attributes, this might overwrite (or delete) default attributes
		self.update(*args, **kwargs)

	def __repr__(self):
		l = len(self)
		if l == 0:
			attrcount = "no attrs"
		elif l == 1:
			attrcount = "1 attr"
		else:
			attrcount = f"{l:,} attrs"
		if self.startloc is not None:
			loc = f" location={str(self.startloc)!r}"
		else:
			loc = ""
		return f"<attributes {self.__class__.__module__}.{self.__class__.__qualname__} ({attrcount}){loc} at {id(self):#x}>"

	def _repr_pretty_content_(self, p):
		for attr in self.values():
			p.breakable()
			p.pretty(attr)

	def _repr_pretty_(self, p, cycle):
		with p.group(4, f"<attributes {self.__class__.__module__}.{self.__class__.__qualname__}", ">"):
			if self.startloc is not None:
				p.breakable()
				p.text(f"location={str(self.startloc)!r}")
			if cycle:
				p.breakable()
				p.text("...")
			else:
				self._repr_pretty_content_(p)
			p.breakable()
			p.text(f"at {id(self):#x}")

	def __str__(self):
		return ""

	def _str(self):
		return "attrs"

	def __eq__(self, other):
		if isinstance(other, Attrs):
			if len(self) != len(other):
				return False
			for (key, value) in self.items():
				if other[key] != value:
					return False
			return True
		return NotImplemented

	@classmethod
	def add(cls, value):
		cls._byxmlname[(value.xmlns, value.xmlname)] = value
		cls._bypyname[(value.xmlns, value.__name__)] = value
		if value.default:
			cls._defaultattrs[(value.xmlns, value.xmlname)] = value

	def _create(self):
		node = self.__class__() # "virtual" constructor
		node.clear()
		return node

	def clone(self):
		node = self._create()
		for (key, value) in dict.items(self):
			dict.__setitem__(node, key, value.clone())
		return self._decoratenode(node)

	def __copy__(self):
		node = self._create()
		for (key, value) in dict.items(self):
			dict.__setitem__(node, key, value)
		return self._decoratenode(node)

	def __deepcopy__(self, memo=None):
		node = self._create()
		if memo is None:
			memo = {}
		memo[id(self)] = node
		for (key, value) in dict.items(self):
			dict.__setitem__(node, key, copy.deepcopy(value, memo))
		return self._decoratenode(node)

	def __getitem__(self, name):
		"""
		Return the attribute with the name :obj:`name`. :obj:`name` can be one of
		the following types:

		A string
			:obj:`name` will be treated as the XML name of a local attribute.

		A two-item tuple
			The first item is treated as the XML attribute name and the second
			item as the namespace name. If the namespace name is ``None`` this
			refers to a local attributes, otherwise to a global attribute.

		An :class:`Attr` subclass
		"""
		if isinstance(name, list) and not isinstance(name, Node):
			node = self
			for subname in name:
				node = node[subname]
			return node
		(attrxmlns, attrname, attrclass) = self._attrinfo(name)
		try:
			return dict.__getitem__(self, (attrxmlns, attrname))
		except KeyError: # if the attribute is not there generate a new empty one
			attrvalue = self._makeattr(attrxmlns, attrname, attrclass)
			dict.__setitem__(self, (attrxmlns, attrname), attrvalue)
			return attrvalue

	def __setitem__(self, name, value):
		"""
		Set the attribute with the XML :obj:`name` to the value :obj:`value`.
		:obj:`name` may be a string or an attribute class or instance. The newly
		set attribute object will be returned.
		"""
		if isinstance(name, list) and not isinstance(name, Node):
			if not name:
				raise ValueError("can't replace self")
			node = self
			for subname in name[:-1]:
				node = node[subname]
			node[name[-1]] = value
		(attrxmlns, attrname, attrclass) = self._attrinfo(name)
		attrvalue = self._makeattr(attrxmlns, attrname, attrclass, value)
		dict.__setitem__(self, (attrxmlns, attrname), attrvalue)

	def __delitem__(self, name):
		"""
		"""
		if isinstance(name, list) and not isinstance(name, Node):
			if not name:
				raise ValueError("can't delete self")
			node = self
			for subname in name[:-1]:
				node = node[subname]
			del node[name[-1]]
		(attrxmlns, attrname, attrclass) = self._attrinfo(name)
		dict.__delitem__(self, (attrxmlns, attrname))

	def __contains__(self, name):
		(attrxmlns, attrname, attrclass) = self._attrinfo(name)
		return dict.__contains__(self, (attrxmlns, attrname)) and bool(dict.__getitem__(self, (attrxmlns, attrname)))

	def convert(self, converter):
		node = self._create()
		for value in self.values():
			newvalue = value.convert(converter)
			assert isinstance(newvalue, Node), f"the convert method returned the illegal object {newvalue!r} (type {type(newvalue)!r}) when converting the attribute {value.__class__.__qualname__} with the value {value!r}"
			node[value] = newvalue
		return node

	def compacted(self):
		node = self._create()
		for value in self.values():
			newvalue = value.compacted()
			assert isinstance(newvalue, Node), f"the compacted method returned the illegal object {newvalue!r} (type {type(newvalue)!r}) when compacting the attribute {value.__class__.__qualname__} with the value {value!r}"
			node[value] = newvalue
		return node

	def normalized(self):
		node = self._create()
		for value in self.values():
			newvalue = value.normalized()
			assert isinstance(newvalue, Node), f"the normalized method returned the illegal object {newvalue!r} (type {type(newvalue)!r}) when normalizing the attribute {value.__class__.__qualname__} with the value {value!r}"
			node[value] = newvalue
		return node

	def present(self, presenter):
		return presenter.presentAttrs(self) # return a generator-iterator

	def validate(self, recursive=True, path=None):
		if path is None:
			path = []
		# collect required attributes
		attrs = {value for value in self.declaredattrs() if value.required}
		path.append(None)
		# Check each existing attribute and remove it from the list of required ones
		for value in self.values():
			path[-1] = value
			yield from self.validateattr(path)
			yield from value.validate(recursive, path)
			try:
				attrs.remove(value.__class__)
			except KeyError:
				pass
		path.pop()
		# are there any required attributes remaining that haven't been specified? => issue warnings about it
		for attr in attrs:
			yield RequiredAttrMissingWarning(self.__class__, attr)

	def validateattr(self, path):
		node = path[-1]
		if node.xmlns is None and not self.isdeclared(node):
			yield UndeclaredAttrWarning(self.__class__, node)

	def publish(self, publisher):
		for value in self.values():
			yield from value.publish(publisher)

	@classmethod
	def isdeclared(cls, name):
		(attrxmlns, attrname, attrclass) = cls._attrinfo(name)
		return (attrxmlns, attrname) in cls._byxmlname

	def __getattribute__(self, name):
		xmlns = super().__getattribute__("xmlns")
		_bypyname = super().__getattribute__("_bypyname")
		if (xmlns, name) in _bypyname:
			return self[_bypyname[(xmlns, name)]]
		else:
			return super().__getattribute__(name)

	def __setattr__(self, name, value):
		if (self.xmlns, name) in self._bypyname:
			self[self._pyname2xmlname(name)] = value
		else:
			super().__setattr__(name, value)

	def __delattr__(self, name):
		if (self.xmlns, name) in self._bypyname:
			del self[self._bypyname[(self.xmlns, name)]]
		else:
			super().__delattr__(name)

	def get(self, name, default=None):
		"""
		Works like the dictionary method :meth:`get`, it returns the attribute
		with the XML name :obj:`name`, or :obj:`default` if :obj:`self` has no
		such attribute. :obj:`name` may also be an attribute class (either from
		``self.Attrs`` or a global attribute).
		"""
		attrvalue = self[name]
		if not attrvalue:
			(attrxmlns, attrname, attrclass) = self._attrinfo(name)
			attrvalue = self._makeattr(attrxmlns, attrname, attrclass, default) # pack the attribute into an attribute object
		return attrvalue

	def setdefault(self, name, default):
		"""
		Works like the dictionary method :meth:`setdefault`, it returns the
		attribute with the Python name :obj:`name`. If :obj:`self` has no such
		attribute, it will be set to :obj:`default` and :obj:`default` will be
		returned as the new attribute value.
		"""
		attrvalue = self[name]
		if not attrvalue:
			(attrname, attrclass) = self._attrinfo(name)
			attrvalue = self._makeattr(attrname, attrclass, default) # pack the attribute into an attribute object
			dict.__setitem__(self, attrname, attrvalue)
		return attrvalue

	def update(self, *args, **kwargs):
		"""
		Copies attributes over from all mappings in :obj:`args` and from
		:obj:`kwargs`. Keywords are treated as the Python names of attributes.
		"""
		for mapping in args:
			if mapping is not None:
				if isinstance(mapping, Attrs):
					# This makes sure that global attributes are copied properly
					for (key, value) in dict.items(mapping): # Iterate through all attributes, even the empty ones.
						dict.__setitem__(self, key, value)
				else:
					for (attrname, attrvalue) in mapping.items():
						self[attrname] = attrvalue
		for (attrname, attrvalue) in kwargs.items():
			self[self._pyname2xmlname(attrname)] = attrvalue

	@classmethod
	def declaredattrs(cls):
		"""
		Return an iterator over all declared attribute classes.
		"""
		return cls._bypyname.values()

	@classmethod
	def _attrinfo(cls, name):
		return cls.__class__._attrinfo(cls, name)

	@classmethod
	def _makeattr(cls, attrxmlns, attrname, attrclass, value=None):
		attrvalue = attrclass(value)
		if attrclass is Attr:
			attrvalue.xmlns = attrxmlns
			attrvalue.xmlname = attrname
		return attrvalue

	@classmethod
	def _pyname2xmlname(cls, name):
		# using ``cls.xmlns`` makes sure, that ``element(xml.Attrs(lang='de'))`` really creates a global attribute
		# (because ``xml.Attrs`` and ``xml.Attrs.lang`` have ``xmlns`` set appropriately)
		if (cls.xmlns, name) in cls._bypyname:
			return cls._bypyname[(cls.xmlns, name)]
		return name

	def __len__(self):
		return misc.count(self.values())

	def keys(self):
		for (key, value) in dict.items(self):
			if value:
				yield key

	__iter__ = keys

	def values(self):
		for value in dict.values(self):
			if value:
				yield value

	def items(self):
		for (key, value) in dict.items(self):
			if value:
				yield (key, value)

	def filtered(self, function):
		"""
		Return a filtered version of :obj:`self`.
		"""
		node = self._create()
		for (name, value) in self.items():
			if function(value):
				node[name] = value
		return node

	def _fixnames(self, names):
		# Helper for :meth:`withnames` and :meth:`withoutnames`
		newnames = []
		for name in names:
			(attrxmlns, attrname, attrclass) = self._attrinfo(name)
			newnames.append((attrxmlns, attrname))
		return tuple(newnames)

	def withnames(self, *names):
		"""
		Return a copy of :obj:`self` where only the attributes with XML names
		in :obj:`names` are kept, all others are removed.
		"""
		def isok(node):
			if node.xmlns is None:
				return (node.xmlns, node.xmlname) in names or node.xmlname in names
			else:
				return (node.xmlns, node.xmlname) in names

		names = self._fixnames(names)
		return self.filtered(isok)

	def withoutnames(self, *names):
		"""
		Return a copy of :obj:`self` where all the attributes with XML names
		in :obj:`names` are removed.
		"""
		def isok(node):
			if node.xmlns is None:
				return (node.xmlns, node.xmlname) not in names and node.xmlname not in names
			else:
				return (node.xmlns, node.xmlname) not in names

		names = self._fixnames(names)
		return self.filtered(isok)

	def _walk(self, cursor):
		cursor.path.append(None)
		cursor.index.append(None)
		for child in self.values():
			cursor.path[-1] = cursor.node = child
			cursor.index[-1] = child.xmlname if child.xmlns is None else (child.xmlname, child.xmlns)
			yield from child._walk(cursor)
		cursor.path.pop()
		cursor.index.pop()
		cursor.node = cursor.path[-1]


class _Element_Meta(type(Node)):
	def __new__(cls, name, bases, dict):
		if "model" in dict and isinstance(dict["model"], bool):
			from ll.xist import sims
			dict["model"] = sims.Any() if dict["model"] else sims.Empty()
		self = super(_Element_Meta, cls).__new__(cls, name, bases, dict)
		if dict.get("register") is not None:
			threadlocalpool.pool.register(self)
		return self

	def __repr__(self):
		if self.xmlname != self.__name__:
			xmlname = f" xmlname={self.xmlname!r}"
		else:
			xmlname = ""

		if self.xmlns is not None:
			xmlns = f" xmlns={self.xmlns!r}"
		else:
			xmlns = ""

		return f"<element class {self.__module__}:{self.__qualname__}{xmlname}{xmlns} at {id(self):#x}>"


class Element(Node, metaclass=_Element_Meta):
	"""
	This class represents XML/XIST elements. All elements implemented by the
	user must be derived from this class.

	Elements support the following class variables:

	:attr:`model` : object with :meth:`validate` method
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
		contentargs = []
		attrargs = []
		for child in content:
			if isinstance(child, dict):
				attrargs.append(child)
			else:
				contentargs.append(child)
		self.content = Frag(*contentargs)
		self.attrs = self.Attrs(*attrargs, **attrs)

	def __repr__(self):
		if self.xmlns is not None:
			xmlns = f" xmlns={self.xmlns!r}"
		else:
			xmlns = ""

		if self.xmlname != self.__class__.__name__:
			xmlname = f" xmlname={self.xmlname!r}"
		else:
			xmlname = ""

		lc = len(self.content)
		if lc == 0:
			childcount = "no children"
		elif lc == 1:
			childcount = "1 child"
		else:
			childcount = f"{lc:,} children"
		la = len(self.attrs)
		if la == 0:
			attrcount = "no attrs"
		elif la == 1:
			attrcount = "1 attr"
		else:
			attrcount = f"{la:,} attrs"
		if self.startloc is not None:
			loc = f" location={str(self.startloc)!r}"
		else:
			loc = ""
		return f"<element {self.__class__.__module__}.{self.__class__.__qualname__}{xmlns}{xmlname} ({childcount}/{attrcount}){loc} at {id(self):#x}>"

	def _repr_pretty_(self, p, cycle):
		with p.group(4, f"<element {self.__class__.__module__}.{self.__class__.__qualname__}", ">"):
			if self.xmlns is not None:
				p.breakable()
				p.text(f"xmlns={self.xmlns!r}")
			if self.xmlname != self.__class__.__name__:
				p.breakable()
				p.text(f"xmlname={self.xmlname!r}")
			if self.startloc is not None:
				p.breakable()
				p.text(f"location={str(self.startloc)!r}")
			if cycle:
				p.breakable()
				p.text("...")
			else:
				self.attrs._repr_pretty_content_(p)
				for child in self.content:
					p.breakable()
					p.pretty(child)
			p.breakable()
			p.text(f"at {id(self):#x}")

	def __str__(self):
		return str(self.content)

	def _str(self):
		return f"element {{{self.xmlns}}}{self.xmlname}"

	def __getstate__(self):
		attrs = {key : (value.__class__.__module__, value.__class__.__qualname__, Frag(value)) for (key, value) in dict.items(self.attrs)}
		return (self.content, attrs)

	def __setstate__(self, data):
		import importlib
		(content, attrs) = data
		self.content = content
		self.attrs = self.Attrs()
		for (key, value) in attrs.items():
			obj = importlib.import_module(value[0])
			for name in value[1].split("."):
				obj = getattr(obj, name)
			value = obj(value[2])
			dict.__setitem__(self.attrs, key, value)

	def __enter__(self):
		"""
		:class:`Element` nodes can be used in :keyword:`with` blocks to build XIST trees.
		Inside a :keyword:`with` block ``+`` and :func:`add` can be used to append node
		to the currently active element in the :keyword:`with` block::

			with xsc.build():
				with html.ul() as node:
					+html.li("I hear and I forget.")
					+html.li("I see and I believe.")
					+html.li("I do and I understand.")
					xsc.add(class_="quote")
			print(node.bytes())
		"""
		threadlocalnodehandler.handler.enter(self)
		return self

	def __exit__(self, type, value, traceback):
		threadlocalnodehandler.handler.exit()

	def __call__(self, *content, **attrs):
		"""
		Calling an element add items in :obj:`content` to the element content
		and set attributes from :obj:`attrs`. The element itself will be returned.
		"""
		for child in content:
			if isinstance(child, dict):
				self.attrs.update(child)
			else:
				self.content.append(child)
		self.attrs.update({self.attrs._pyname2xmlname(key): value for (key, value) in attrs.items()})
		return self

	def __eq__(self, other):
		if isinstance(other, Element):
			return self.xmlname == other.xmlname and self.xmlns == other.xmlns and self.content == other.content and self.attrs == other.attrs
		return NotImplemented

	def validate(self, recursive=True, path=None):
		if path is None:
			path = [self]
		if self.__class__ is Element:
			yield UndeclaredNodeWarning(self)
		if self.model is not None:
			yield from self.model.validate(path)
		yield from self.attrs.validate(recursive, path)
		if recursive:
			yield from self.content.validate(recursive, path)

	def append(self, *items):
		"""
		Append every item in :obj:`items` to the elements content.
		"""
		self.content.append(*items)

	def extend(self, items):
		"""
		Append all items in :obj:`items` to the elements content.
		"""
		self.content.extend(items)

	def insert(self, index, *items):
		"""
		Insert every item in :obj:`items` at the position :obj:`index`.
		"""
		self.content.insert(index, *items)

	def _create(self):
		node = self.__class__() # "virtual" constructor
		if self.__class__ is Element:
			node.xmlname = self.xmlname
			node.xmlns = self.xmlns
		return node

	def convert(self, converter):
		node = self._create()
		node.content = self.content.convert(converter)
		node.attrs = self.attrs.convert(converter)
		return self._decoratenode(node)

	def clone(self):
		node = self._create()
		node.content = self.content.clone() # this is faster than passing it in the constructor (no :func:`tonode` call)
		node.attrs = self.attrs.clone()
		return self._decoratenode(node)

	def __copy__(self):
		node = self._create()
		node.content = copy.copy(self.content)
		node.attrs = copy.copy(self.attrs)
		return self._decoratenode(node)

	def __deepcopy__(self, memo=None):
		node = self._create()
		if memo is None:
			memo = {}
		memo[id(self)] = node
		node.content = copy.deepcopy(self.content, memo)
		node.attrs = copy.deepcopy(self.attrs, memo)
		return self._decoratenode(node)

	def _addimagesizeattributes(self, url, widthattr=None, heightattr=None):
		"""
		Automatically set image width and height attributes.

		The size of the image with the URL :obj:`url` will be determined and the
		width of the image will be put into the attribute with the name
		:obj:`widthattr` if :obj:`widthattr` is not :const:`None` and the
		attribute is not set already. The same will happen for the height, which
		will be put into the attribute named :obj:`heighattr`.
		"""
		try:
			size = url.imagesize()
		except IOError as exc:
			warnings.warn(FileNotFoundWarning("can't read image", url, exc))
		else:
			for attr in (heightattr, widthattr):
				if attr is not None: # do something to the width/height
					if attr not in self.attrs:
						self[attr] = size[attr == heightattr]

	def present(self, presenter):
		return presenter.presentElement(self) # return a generator-iterator

	def _publishname(self, publisher):
		if self.xmlns is not None:
			prefix = publisher._ns2prefix.get(self.xmlns)
			if prefix is not None:
				return f"{prefix}:{self.xmlname}"
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
			for (xmlns, prefix) in sorted(publisher._ns2prefix.items(), key=lambda item: item[1] or ""):
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
		yield from self.attrs.publish(publisher)
		if len(self):
			yield publisher.encode(">")
			yield from self.content.publish(publisher)
			yield publisher.encode("</")
			yield publisher.encode(name)
			yield publisher.encode(">")
		else:
			if publisher.xhtml in (0, 1):
				if self.model is not None and self.model.empty:
					if publisher.xhtml == 1:
						yield publisher.encode(" /")
					yield publisher.encode(">")
				else:
					yield publisher.encode("></")
					yield publisher.encode(name)
					yield publisher.encode(">")
			elif publisher.xhtml == 2:
				yield publisher.encode("/>")

	def publish(self, publisher):
		if publisher.inattr:
			# publish the content only when we are inside an attribute. This works much like using the plain string value,
			# but even works with processing instructions, or what the abbreviation entities return
			return self.content.publish(publisher) # return a generator-iterator
		else:
			return self._publishfull(publisher) # return a generator-iterator

	def __getitem__(self, index):
		"""
		If :obj:`index` is a string, return the attribute with this (Python)
		name. If :obj:`index` is an attribute class, return the attribute
		that is an instance of this class. If :obj:`index` is a number or slice
		return the appropriate content node. :obj:`index` may also be a list, in
		with case :meth:`__getitem__` will be applied recusively.
		:meth:`__getitem__` also supports walk filters.

		"""
		if isinstance(index, (str, _Attr_Meta)):
			return self.attrs[index]
		elif isinstance(index, int):
			return self.content[index]
		elif isinstance(index, list):
			if index:
				return self.content[index]
			else:
				return self
		elif isinstance(index, slice):
			result = self._create()
			result.content = self.content[index]
			result.attrs = self.attrs
			return result
		else:
			from ll.xist import xfind

			def iterate(selector):
				path = [self, None]
				for child in self:
					path[-1] = child
					if path in selector:
						yield child
			return misc.Iterator(iterate(xfind.selector(index)))

	def __setitem__(self, index, value):
		"""
		Set an attribute or content node to the value :obj:`value`. For possible
		types for :obj:`index` see :meth:`__getitem__`.
		"""
		if isinstance(index, (str, _Attr_Meta)):
			self.attrs[index] = value
		elif isinstance(index, (list, int, slice)):
			self.content[index] = value
		else:
			from ll.xist import xfind
			selector = xfind.selector(index)
			value = Frag(value)
			newcontent = []
			path = [self, None]
			for child in self:
				path[-1] = child
				if path in selector:
					newcontent.extend(value)
				else:
					newcontent.append(child)
			self.content[:] = newcontent

	def __delitem__(self, index):
		"""
		Remove an attribute or content node. For possible types for :obj:`index`
		see :meth:`__getitem__`.
		"""
		if isinstance(index, (str, _Attr_Meta)):
			del self.attrs[index]
		elif isinstance(index, (list, int, slice)):
			del self.content[index]
		else:
			from ll.xist import xfind
			selector = xfind.selector(index)
			self.content = Frag(child for child in self if [self, child] not in selector)

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
		node = self._create()
		node.content = self.content.compacted()
		node.attrs = self.attrs.compacted()
		return self._decoratenode(node)

	def withsep(self, separator, clone=False):
		"""
		Return a version of :obj:`self` with a separator node between the child
		nodes of :obj:`self`. For more info see :meth:`Frag.withsep`.
		"""
		node = self._create()
		node.attrs = self.attrs.clone()
		node.content = self.content.withsep(separator, clone)
		return node

	def reversed(self):
		"""
		Return a reversed version of :obj:`self`.
		"""
		node = self._create()
		node.attrs = self.attrs.clone()
		node.content = self.content.reversed()
		return node

	def filtered(self, function):
		"""
		Return a filtered version of the :obj:`self`.
		"""
		node = self._create()
		node.attrs = self.attrs.clone()
		node.content = self.content.filtered(function)
		return node

	def shuffled(self):
		"""
		Return a shuffled version of the :obj:`self`.
		"""
		node = self._create()
		node.attrs = self.attrs.clone()
		node.content = self.content.shuffled()
		return node

	def mapped(self, function, converter=None, **converterargs):
		if converter is None:
			converter = Converter(**converterargs)
		node = function(self, converter)
		assert isinstance(node, Node), f"the mapped method returned the illegal object {node!r} (type {type(node)!r}) when mapping {self!r}"
		if node is self:
			node = self._create()
			node.content = Frag(self.content.mapped(function, converter))
			node.attrs = self.attrs.clone()
		return node

	def normalized(self):
		node = self._create()
		node.attrs = self.attrs.normalized()
		node.content = self.content.normalized()
		return node

	def pretty(self, level=0, indent="\t"):
		orglevel = level # Remember the original indent level, so that any misconfiguration inside the element doesn't mess with the indentation
		node = self._create()
		node.attrs.update(self.attrs)
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
		if orglevel > 0:
			node = Frag(indent*orglevel, node)
		return node

	def _walk(self, cursor):
		enterelementnode = cursor.enterelementnode
		if enterelementnode:
			cursor.event = "enterelementnode"
			yield cursor
			# The user may have altered ``cursor`` attributes outside the generator, so we refetch them
			entercontent = cursor.entercontent
			enterattrs = cursor.enterattrs
			leaveelementnode = cursor.leaveelementnode
			cursor.restore()
		else:
			# These are the initial options
			entercontent = cursor.entercontent
			enterattrs = cursor.enterattrs
			leaveelementnode = cursor.leaveelementnode
		if enterattrs:
			yield from self.attrs._walk(cursor)
		if entercontent:
			yield from self.content._walk(cursor)
		if leaveelementnode:
			cursor.event = "leaveelementnode"
			yield cursor
			cursor.restore()


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
		Publish ``self`` to the publisher :obj:`publisher` (outside of any
		attribute)
		"""

	@misc.notimplemented
	def publishattr(self, publisher, attr):
		"""
		Publish the attribute :obj:`attr` to the publisher :obj:`publisher`.
		"""

	@misc.notimplemented
	def publishboolattr(self, publisher, attr):
		"""
		Publish the boolean attribute :obj:`attr` to the publisher
		"""


class _Entity_Meta(type(Node)):
	def __new__(cls, name, bases, dict):
		self = super(_Entity_Meta, cls).__new__(cls, name, bases, dict)
		if dict.get("register") is not None:
			threadlocalpool.pool.register(self)
		return self

	def __repr__(self):
		if self.xmlname != self.__name__:
			xmlname = f" xmlname={self.xmlname!r}"
		else:
			xmlname = ""

		return f"<entity class {self.__module__}:{self.__qualname__}{xmlname} at {id(self):#x}>"


class Entity(Node, metaclass=_Entity_Meta):
	"""
	Class for entities. Derive your own entities from it and overwrite
	:meth:`convert`.
	"""

	register = None

	def __repr__(self):
		if self.xmlname != self.__class__.__name__:
			xmlname = f" xmlname={self.xmlname!r}"
		else:
			xmlname = ""

		if self.startloc is not None:
			loc = f" location={str(self.startloc)!r}"
		else:
			loc = ""
		return f"<entity {self.__class__.__module__}.{self.__class__.__qualname__}{xmlname}{loc} at {id(self):#x}>"

	def _repr_pretty_(self, p, cycle):
		with p.group(4, f"<entity {self.__class__.__module__}.{self.__class__.__qualname__}", ">"):
			if self.xmlname != self.__class__.__name__:
				p.breakable()
				p.text(f"xmlname={self.xmlname!r}")
			if self.startloc is not None:
				p.breakable()
				p.text(f"location={str(self.startloc)!r}")
			p.breakable()
			p.text(f"at {id(self):#x}")

	def _str(self):
		return f"entity {self.xmlname}"

	def __eq__(self, other):
		if isinstance(other, Entity):
			return self.xmlname == other.xmlname
		return NotImplemented

	def validate(self, recursive=True, path=None):
		if self.__class__ is Entity:
			yield UndeclaredNodeWarning(self)

	def convert(self, converter):
		return self

	def compacted(self):
		return self

	def present(self, presenter):
		return presenter.presentEntity(self) # return a generator-iterator

	def publish(self, publisher):
		yield publisher.encode("&")
		yield publisher.encode(self.xmlname)
		yield publisher.encode(";")

	def _walk(self, cursor):
		cursor.event = "entitynode"
		yield cursor
		cursor.restore()


class _CharRef_Meta(type(Entity)): # don't subclass type(Text), as this is redundant
	def __repr__(self):
		if self.xmlname != self.__name__:
			xmlname = f" xmlname={self.xmlname!r}"
		else:
			xmlname = ""
		return f"<charref class {self.__module__}:{self.__qualname__}{xmlname} at {id(self):#x}>"


class CharRef(Text, Entity, metaclass=_CharRef_Meta):
	"""
	A simple named character reference, the code point is in the class attribute
	:attr:`codepoint`.
	"""
	register = None

	def __init__(self):
		Text.__init__(self, chr(self.codepoint))
		Entity.__init__(self)

	def __repr__(self):
		if self.xmlname != self.__class__.__name__:
			xmlname = f" xmlname={self.xmlname!r}"
		else:
			xmlname = ""

		if self.startloc is not None:
			loc = f" location={str(self.startloc)!r}"
		else:
			loc = ""
		return f"<charref {self.__class__.__module__}.{self.__class__.__qualname__}{xmlname} content={self.content!r}{loc} at {id(self):#x}>"

	def _repr_pretty_(self, p, cycle):
		with p.group(4, f"<charref {self.__class__.__module__}.{self.__class__.__qualname__}", ">"):
			if self.xmlname != self.__class__.__name__:
				p.breakable()
				p.text(f"xmlname={self.xmlname!r}")
			if self.startloc is not None:
				p.breakable()
				p.text(f"location={str(self.startloc)!r}")
			p.breakable()
			p.text(f"codepoint={self.codepoint:#x}")
			p.breakable()
			p.text(f"at {id(self):#x}")

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
		Create a :class:`Pool` object. All items in :obj:`objects` will be
		registered in the pool.
		"""
		self._elementsbyname = {}
		self._procinstsbyname = {}
		self._entitiesbyname = {}
		self._charrefsbyname = {}
		self._charrefsbycodepoint = {}
		self._attrsbyname = {}
		misc.Pool.__init__(self, *objects)

	def register(self, object):
		"""
		Register :obj:`object` in the pool. :obj:`object` can be:

		*	a :class:`Element`, :class:`ProcInst` or :class:`Entity` class;

		*	an :class:`Attr` class for a global attribute;

		*	an :class:`Attrs` class containing global attributes;

		*	a :class:`dict` (all values will be registered, this makes it possible
			to e.g. register all local variables by passing ``vars()``);

		*	a module (all attributes in the module will be registered).
		"""
		# Note that the following is a complete reimplementation of :meth:`misc.Pool.register`, otherwise the interactions would be too complicated.
		if isinstance(object, type):
			if issubclass(object, Element):
				if object.register:
					self._elementsbyname[(object.xmlns, object.xmlname)] = object
			elif issubclass(object, ProcInst):
				if object.register:
					self._procinstsbyname[object.xmlname] = object
			elif issubclass(object, Entity):
				if object.register:
					self._entitiesbyname[object.xmlname] = object
			elif issubclass(object, Attr):
				if object.xmlns is not None and object.register:
					self._attrsbyname[(object.xmlns, object.xmlname)] = object
			elif issubclass(object, Attrs):
				for attr in object.declaredattrs():
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
		Make :obj:`self` empty.
		"""
		self._elementsbyname.clear()
		self._procinstsbyname.clear()
		self._entitiesbyname.clear()
		self._attrsbyname.clear()
		misc.Pool.clear(self)

	def clone(self):
		"""
		Return a copy of :obj:`self`.
		"""
		copy = misc.Pool.clone(self)
		copy._elementsbyname = self._elementsbyname.copy()
		copy._procinstsbyname = self._procinstsbyname.copy()
		copy._entitiesbyname = self._entitiesbyname.copy()
		copy._attrsbyname = self._attrsbyname.copy()
		return copy

	def elements(self):
		"""
		Return an iterator for all registered element classes.
		"""
		seen = set()
		for element in self._elementsbyname.values():
			yield element
			seen.add((element.xmlns, element.xmlname))
		for base in self.bases:
			for element in base.elements():
				if (element.xmlns, element.xmlname) not in seen:
					yield element
					seen.add((element.xmlns, element.xmlname))

	def elementclass(self, xmlns, name):
		"""
		Return the element class for the element with the XML name :obj:`name`
		and the namespace :obj:`xmlns`. If the element can't be found an
		:class:`Element` will be returned.
		"""
		xmlns = nsname(xmlns)
		try:
			return self._elementsbyname[(xmlns, name)]
		except KeyError:
			for base in self.bases:
				result = base.elementclass(xmlns, name)
				if result is not Element:
					return result
		return Element

	def element(self, xmlns, name):
		"""
		Return an element object for the element type with the XML name
		:obj:`name` and the namespace :obj:`xmlns`.
		"""
		xmlns = nsname(xmlns)
		result = self.elementclass(xmlns, name)()
		if result.__class__ is Element:
			result.xmlns = xmlns
			result.xmlname = name
		return result

	def haselement(self, xmlns, name):
		"""
		Is there a registered element class in :obj:`self` for the element type
		with the Python name :obj:`name` and the namespace :obj:`xmlns`?
		"""
		return (nsname(xmlns), name) in self._elementsbyname or any(base.haselement(xmlns, name) for base in self.bases)

	def procinsts(self):
		"""
		Return an iterator for all registered processing instruction classes.
		"""
		seen = set()
		for procinst in self._procinstsbyname.values():
			yield procinst
			seen.add(procinst.xmlname)
		for base in self.bases:
			for procinst in base.procinsts():
				if procinst.xmlname not in seen:
					yield procinst
					seen.add(procinst.xmlname)

	def procinstclass(self, name):
		"""
		Return the processing instruction class for the PI with the target name
		:obj:`name`. If the processing instruction can't be found an
		return :class:`ProcInst`.
		"""
		try:
			return self._procinstsbyname[name]
		except KeyError:
			for base in self.bases:
				result = base.procinstclass(name)
				if result is not ProcInst:
					return result
		return ProcInst

	def procinst(self, name, content):
		"""
		Return a processing instruction object for the PI type with the target
		name :obj:`name`.
		"""
		result = self.procinstclass(name)(content)
		if result.__class__ is ProcInst:
			result.xmlname = name
		return result

	def hasprocinst(self, name):
		"""
		Is there a registered processing instruction class in :obj:`self` for the
		PI with the target name :obj:`name`?
		"""
		return name in self._procinstsbyname or any(base.hasprocinst(name) for base in self.bases)

	def entities(self):
		"""
		Return an iterator for all registered entity classes.
		"""
		seen = set()
		for entity in self._entitiesbyname.values():
			yield entity
			seen.add(entity.xmlname)
		for base in self.bases:
			for entity in base.entities():
				if entity.xmlname not in seen:
					yield entity
					seen.add(entity.xmlname)

	def entityclass(self, name):
		"""
		Return the entity class for the entity with the XML name :obj:`name`.
		If the entity can't be found return :class:`Entity`.
		"""
		try:
			return self._entitiesbyname[name]
		except KeyError:
			for base in self.bases:
				result = base.entityclass(name)
				if result is not Entity:
					return result
		return Entity

	def entity(self, name):
		"""
		Return an entity object for the entity with the XML name :obj:`name`.
		"""
		result = self.entityclass(name)()
		if result.__class__ is Entity:
			result.xmlname = name
		return result

	def hasentity(self, name):
		"""
		Is there a registered entity class in :obj:`self` for the entity with the
		XML name :obj:`name`?
		"""
		return name in self._entitiesbyname or any(base.hasentity(name) for base in self.bases)

	def attrkey(self, xmlns, name):
		"""
		Return the key that can be used to set the attribute with the name
		:obj:`name` and the namespace :obj:`xmlns`. If :obj:`self` (or one of the
		base pools) has any global attribute registered for that name/namespace,
		the attribute class will be returned. Otherwise the tuple ``(name, xmlns)``
		(or ``name`` itself for a local attribute) will be returned. With this key
		:meth:`Attrs.__setitem__` will create the appropriate attribute class.
		"""
		if xmlns is None:
			return name
		xmlns = nsname(xmlns)
		try:
			return self._attrsbyname[(xmlns, name)]
		except KeyError:
			for base in self.bases:
				result = base.attrkey(name, xmlns)
				if isinstance(result, _Attr_Meta):
					return result
		return (xmlns, name)

	def text(self, content):
		"""
		Create a text node with the content :obj:`content`.
		"""
		return Text(content)

	def comment(self, content):
		"""
		Create a comment node with the content :obj:`content`.
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
	If :obj:`xmlns` is a module, return ``xmlns.xmlns``, else return
	:obj:`xmlns` unchanged.
	"""
	if xmlns is not None and not isinstance(xmlns, str):
		xmlns = xmlns.xmlns
	return xmlns


def nsclark(obj):
	"""
	Return a name in Clark notation. :obj:`xmlns` can be :const:`None`,
	a string or a module to return a namespace name, or a :class:`Node` instance
	to return a namespace name + node name combination::

		>>> from ll.xist import xsc
		>>> from ll.xist.ns import html
		>>> xsc.nsclark(None)
		'{}'
		>>> xsc.nsclark(html)
		'{http://www.w3.org/1999/xhtml}'
		>>> xsc.nsclark(html.a)
		'{http://www.w3.org/1999/xhtml}a'
		>>> xsc.nsclark(html.a())
		'{http://www.w3.org/1999/xhtml}a'
	"""
	if obj is None:
		return "{}"
	elif isinstance(obj, (Element, _Element_Meta)):
		return f"{{{obj.xmlns}}}{obj.xmlname}"
	elif isinstance(obj, (Attr, _Attr_Meta)):
		if obj.xmlns is None:
			return obj.xmlname
		else:
			return f"{{{obj.xmlns}}}{obj.xmlname}"
	elif isinstance(obj, (Node, _Node_Meta)):
		return obj.xmlname
	elif not isinstance(obj, str):
		return f"{{{obj.xmlns}}}"
	return f"{{{obj}}}"


# C0 Controls and Basic Latin
class quot(CharRef): "quotation mark = APL quote, U+0022 ISOnum"; codepoint = 34
class amp(CharRef): "ampersand, U+0026 ISOnum"; codepoint = 38
class lt(CharRef): "less-than sign, U+003C ISOnum"; codepoint = 60
class gt(CharRef): "greater-than sign, U+003E ISOnum"; codepoint = 62
class apos(CharRef): "apostrophe mark, U+0027 ISOnum"; codepoint = 39


###
### Functions for creating plain elements, entities and processing instructions
###

def element(xmlns, xmlname, *content, **attrs):
	"""
	Create a plain element object with the namespace name :obj:`xmlns`
	and the element name :obj:`xmlname`. This object will be an instance of
	:class:`Element` (not an instance of a subclass). :obj:`content` and
	:obj:`attrs` will be used to initialize the content and attributes of the
	element.
	"""
	element = Element(*content, **attrs)
	element.xmlns = nsname(xmlns)
	element.xmlname = xmlname
	return element


def entity(xmlname):
	"""
	Create a plain entity object with the entity name :obj:`xmlname`. This
	object will be an instance of :class:`Entity` (not an instance of a subclass).
	"""
	entity = Entity()
	entity.xmlname = xmlname
	return entity


def procinst(xmlname, *content):
	"""
	Create a plain processing instruction object with the target name
	:obj:`xmlname`. This object will be an instance of :class:`ProcInst`
	(not an instance of a subclass). :obj:`content` will be used to initialize
	the content of the processing instruction.
	"""
	procinst = ProcInst(*content)
	procinst.xmlname = xmlname
	return procinst


###
### Location information
###

class Location:
	"""
	Represents a location in an XML entity.
	"""
	__slots__ = ("url", "line", "col")

	def __init__(self, url=None, line=None, col=None):
		"""
		Create a new :class:`Location` object using the arguments passed in.
		:obj:`url` is the URL/filename. :obj:`line` is the line number and
		:obj:`col` is the column number (both starting at 0).
		"""
		self.url = url
		self.line = line
		self.col = col

	def offset(self, offset):
		"""
		Return a location where the line number is incremented by offset
		(and the column number is reset to 0).
		"""
		if offset == 0:
			return self
		elif self.line is None:
			return Location(url=self.url, col=0)
		return Location(url=self.url, line=self.line+offset, col=0)

	def __str__(self):
		url = str(self.url) if self.url is not None else "???"
		line = str(self.line) if self.line is not None else "?"
		col = str(self.col) if self.col is not None else "?"
		return f"{url}:{line}:{col}"

	def __repr__(self):
		attrs = ", ".join(f"{attr}={getattr(self, attr)!r}" for attr in ("url", "line", "col") if getattr(self, attr) is not None)
		return f"{self.__class__.__qualname__}({attrs})"

	def __eq__(self, other):
		if self.__class__ is other.__class__:
			return self.url == other.url and self.line == other.line and self.col == other.col
		return NotImplemented
