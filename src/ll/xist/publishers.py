# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<p>This module contains classes that may be used as publishing
handlers in <pyref module="ll.xist.xsc" class="Node" method="publish"><meth>publish</meth></pyref>.</p>
"""


import sys, codecs

from ll import misc, url
from ll import xml_codec # registers the "xml" encoding

import xsc, helpers


__docformat__ = "xist"


def cssescapereplace(exc):
	"""
	PEP 293 codec callback that escapes unencodable character for CSS output.
	"""
	if not isinstance(exc, UnicodeEncodeError):
		raise TypeError("don't know how to handle %r" % exc)
	return (helpers.cssescapereplace(exc.object[exc.start:exc.end], exc.encoding), exc.end)
codecs.register_error("cssescapereplace", cssescapereplace)


class Publisher(object):
	"""
	A <class>Publisher</class> object is used for serializing an &xist; tree into
	a byte sequence.
	"""

	def __init__(self, encoding=None, xhtml=1, validate=True, prefixes={}, prefixdefault=False, hidexmlns=()):
		"""
		<p><arg>encoding</arg> specifies the encoding to be used for the byte sequence.
		If <lit>None</lit> is used the encoding in the &xml; declaration will be
		used. If there is none, UTF-8 will be used.</p>

		<p>With the parameter <arg>xhtml</arg> you can specify if you want &html; output:</p>
		<dl>
		<dt>&html; (<lit><arg>xhtml</arg>==0</lit>)</dt>
		<dd>Elements with a empty content model will be published as
		<markup>&lt;foo&gt;</markup>.</dd>
		<dt>&html; browser compatible &xml; (<lit><arg>xhtml</arg>==1</lit>)</dt>
		<dd>Elements with an empty content model will be published as <markup>&lt;foo /&gt;</markup>
		and others that just happen to be empty as <markup>&lt;foo&gt;&lt;/foo&gt;</markup>. This
		is the default.</dd>
		<dt>Pure &xml; (<lit><arg>xhtml</arg>==2</lit>)</dt>
		<dd>All empty elements will be published as <markup>&lt;foo/&gt;</markup>.</dd>
		</dl>

		<p><arg>validate</arg> specifies whether validation should be done before
		publishing.</p>

		<p><arg>prefixes</arg> is a dictionary that specifies which namespace
		prefixes should be used for publishing. Keys in the dictionary are either
		namespace names or objects that have an <lit>xmlns</lit> attribute which
		is the namespace name. Value can be:</p>

		<dl>
		<dt><lit>False</lit></dt>
		<dd>Treat elements in this namespace as if they are not in any namespace
		(if global attributes from this namespace are encountered, a prefix will
		be used nonetheless).</dd>
		<dt><lit>None</lit></dt>
		<dd>Treat the namespace as the default namespaces (i.e. use unprefixed
		element names). Global attributes will again result in a prefix.</dd>
		<dt><lit>True</lit></dt>
		<dd>The publisher uses a unique non-empty prefix for this namespace.</dd>
		<dt>A string</dt>
		<dd>Use this prefix for the namespace.</dd>
		</dl>

		<p>If an element or attribute is encountered whose namespace is not in
		<arg>prefixes</arg> <arg>prefixdefault</arg> is used as the fallback.</p>

		<p><arg>hidexmlns</arg> can be a list or set that contains namespace names
		for which no <lit>xmlns</lit> attributes should be published. (This can be
		used to hide the namespace declarations for e.g. Java taglibs.)</p>
		"""
		self.base = None
		self.encoding = encoding
		self.encoder = None
		self.xhtml = xhtml
		self.validate = validate
		self.prefixes = dict((xsc.nsname(xmlns), prefix) for (xmlns, prefix) in prefixes.iteritems())
		self.prefixdefault = prefixdefault
		self.hidexmlns = set(xsc.nsname(xmlns) for xmlns in hidexmlns)
		self._ns2prefix = {}
		self._prefix2ns = {}

	def encode(self, text):
		"""
		Encode <arg>text</arg> with the encoding and error handling currently
		active and return the resulting byte string.
		"""
		return self.encoder.encode(text)

	def encodetext(self, text):
		"""
		<p>Encode <arg>test</arg> as text data. <arg>text</arg> must
		be a <class>unicode</class> object. The publisher will apply the configured
		encoding, error handling and the current text filter (which escapes
		characters that can't appear in text data (like <lit>&lt;</lit> etc.))
		and return the resulting <class>str</class> object.
		"""
		self.encoder.errors = self.__errors[-1]
		result = self.encoder.encode(self.__textfilters[-1](text))
		self.encoder.errors = "strict"
		return result

	def pushtextfilter(self, filter):
		"""
		<p>pushes a new text filter function on the text filter stack.
		This function is responsible for escaping characters that can't appear
		in text data (like <lit>&lt;</lit>)). This is used to switch on escaping
		of <lit>"</lit> inside attribute values.</p>
		"""
		self.__textfilters.append(filter)

	def poptextfilter(self):
		"""
		<p>pops the current text filter function from the stack.</p>
		"""
		self.__textfilters.pop()

	def pusherrors(self, errors):
		"""
		<p>pushes a new error handling scheme onto the error handling stack.</p>
		"""
		self.__errors.append(errors)

	def poperrors(self):
		"""
		<p>pop the current error handling scheme from the error handling stack.</p>
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

	def getprefix(self, object):
		"""
		Can be used during publication by custom publish methods: Return the prefix
		configured for object <arg>object</arg>.
		"""
		xmlns = getattr(object, "xmlns")
		if xmlns is not None:
			emptyok = isinstance(object, xsc.Element) # If it's e.g. a procinst assume we need a non-empty prefix
			try:
				prefix = self._ns2prefix[xmlns]
			except KeyError: # A namespace we haven't encountered yet
				if xmlns != xsc.xml_xmlns: # We don't need a namespace mapping for the xml namespace
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
					return "xml"
			else:
				# We can't use the unprefixed names for global attributes
				if (prefix is None or prefix is False) and not emptyok:
					# Use a new one
					prefix = self._newprefix()
					self._ns2prefix[xmlns] = prefix
					self._prefix2ns[prefix] = xmlns

	def publish(self, node, base=None):
		"""
		<p>publish the node <arg>node</arg>. This method is a generator that
		will yield the resulting &xml; byte sequence in fragments.</p>
		"""
		self._ns2prefix.clear()
		self._prefix2ns.clear()
		# iterate through every node in the tree
		for n in node.walknode(xsc.Node):
			self.getprefix(n)

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
		self.__textfilters = [ helpers.escapetext ]

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
		self.__textfilters = [ helpers.escapetext ]

		self.__errors = [ "xmlcharrefreplace" ]

		self.publishxmlns = False
		self._ns2prefix.clear()
		self._prefix2ns.clear()

		self.encoder = None
