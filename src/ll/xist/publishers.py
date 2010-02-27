# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
This module contains classes that may be used as publishing handlers in
:meth:`ll.xist.xsc.Node.publish`.
"""


import sys, codecs

from ll import misc, url
from ll import xml_codec # registers the "xml" encoding

import xsc


__docformat__ = "reStructuredText"


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
		self.prefixes = dict((xsc.nsname(xmlns), prefix) for (xmlns, prefix) in prefixes.iteritems())
		self.prefixdefault = prefixdefault
		self.hidexmlns = set(xsc.nsname(xmlns) for xmlns in hidexmlns)
		self.showxmlns = set(xsc.nsname(xmlns) for xmlns in showxmlns)
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
			prefix = "ns%d" % suffix
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

		if xmlns == xsc.xml_xmlns: # We don't need a namespace mapping for the xml namespace
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

		if xmlns == xsc.xml_xmlns: # We don't need a namespace mapping for the xml namespace
			prefix = "xml"
		else:
			emptyok = isinstance(object, xsc.Element) # If it's e.g. a procinst assume we need a non-empty prefix
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
		for n in node.walknode(xsc.Node):
			self.getobjectprefix(n)
		# Add the prefixes forced by ``self.showxmlns``
		for xmlns in self.showxmlns:
			self.getnamespaceprefix(xmlns)

		# Do we have to publish xmlns attributes?
		self._publishxmlns = False
		if self._ns2prefix:
			# Determine if we have multiple roots
			if isinstance(node, xsc.Frag):
				count = 0
				for child in node:
					if isinstance(node, xsc.Element) and node.xmlns not in self.hidexmlns:
						count += 1
				if count > 1:
					raise xsc.MultipleRootsError()
			self._publishxmlns = True

		self.inattr = 0
		self.__textfilters = [ misc.xmlescape_text ]

		self.__errors = [ "xmlcharrefreplace" ]

		self.base = url.URL(base)
		self.node = node

		self.encoder = codecs.getincrementalencoder("xml")(encoding=self.encoding)

		for part in self.node.publish(self):
			yield part
		rest = self.encoder.encode(u"", True) # finish encoding and flush buffers
		if rest:
			yield rest
	
		self.inattr = 0
		self.__textfilters = [ misc.xmlescape_text ]

		self.__errors = [ "xmlcharrefreplace" ]

		self.publishxmlns = False
		self._ns2prefix.clear()
		self._prefix2ns.clear()

		self.encoder = None

	def bytes(self, node, base=None):
		"""
		Return a byte string in XML format for the XIST node :var:`node`.
		"""
		return "".join(self.iterbytes(node, base))

	def iterstring(self, node, base=None):
		"""
		A generator that will produce a serialized string of :var:`node`.
		"""
		decoder = codecs.getincrementaldecoder("xml")(encoding=self.encoding)
		for part in self.iterbytes(node, base):
			part = decoder.decode(part, False)
			if part:
				yield part
		part = decoder.decode("", True)
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
