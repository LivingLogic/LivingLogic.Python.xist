#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>This module contains classes that may be used as publishing
handlers in <pyref module="ll.xist.xsc" class="Node" method="publish"><method>publish</method></pyref>.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, codecs

from ll import url

import xsc, options, helpers, errors


def cssescapereplace(exc):
	"""
	PEP 293 codec callback that excapes unencodable character for CSS output.
	"""
	if not isinstance(exc, UnicodeEncodeError):
		raise TypeError("don't know how to handle %r" % exc)
	return (helpers.cssescapereplace(exc.object[exc.start:exc.end], exc.encoding), exc.end)
codecs.register_error("cssescapereplace", cssescapereplace)


class Publisher(object):
	"""
	base class for all publishers.
	"""

	def __init__(self, encoding="utf-8", xhtml=1, validate=True, prefixes=None, prefixmode=0):
		"""
		<par><arg>encoding</arg> specifies the encoding to be used.
		The encoding itself (i.e. calling <method>encode</method> on the
		unicode strings) must be done by <pyref method="publish"><method>ll.xist.publishers.Publisher.write</method></pyref>
		and not by <pyref module="ll.xist.xsc" class="Node"><method>ll.xist.xsc.Node.publish</method></pyref>.</par>

		<par>The only exception is in the case of encodings that can't encode
		the full range of unicode characters like <lit>us-ascii</lit>
		or <lit>iso-8859-1</lit>. In this case non encodable characters will be replaced
		by characters references (if possible, if not (e.g. in comments or processing
		instructions) an exception will be raised) before they are passed to
		<pyref method="write"><method>write</method></pyref>.</par>

		<par>With the parameter <arg>xhtml</arg> you can specify if you want &html; output
		(i.e. elements with a content model EMPTY as <markup>&lt;foo&gt;</markup>) with
		<lit><arg>xhtml</arg>==0</lit>, or XHTML output that is compatible with &html; browsers
		(element with an empty content model as <markup>&lt;foo /&gt;</markup> and others that
		just happen to be empty as <markup>&lt;foo&gt;&lt;/foo&gt;</markup>) with
		<lit><arg>xhtml</arg>==1</lit> (the default) or just plain XHTML with
		<lit><arg>xhtml</arg>==2</lit> (all empty elements as <markup>&lt;foo/&gt;</markup>).</par>

		<par><arg>validate</arg> specifies whether validation should be done before
		publishing.</par>

		<par><arg>prefixes</arg> is an instance of <pyref module="ll.xist.xsc" class="Prefixes"><class>Prefixes</class></pyref>
		and maps <pyref module="ll.xist.xsc" class="Namespace"><class>Namespace</class></pyref>
		objects to prefixes that should be used (or <lit>None</lit>, if no prefix should be used).
		With <arg>prefixmode</arg> you can specify how prefixes for elements should be
		treated:</par>
		<ulist>
		<item><lit>0</lit>: Never publish a prefix;</item>
		<item><lit>1</lit>: Publish prefixes, but do not use <lit>xmlns</lit> attributes;</item>
		<item><lit>2</lit>: Publish prefixes and issue the appropriate <lit>xmlns</lit> attributes.</item>
		</ulist>
		"""
		self.base = None
		self.encoding = encoding
		self.xhtml = xhtml
		self.validate = validate

		if prefixes is None:
			prefixes = xsc.OldPrefixes()
		self.prefixes = prefixes
		self.prefixmode = prefixmode

	def write(self, text):
		"""
		receives the text to be written to the output. <arg>text</arg> must be a
		<class>unicode</class> object. The publisher will apply the configured
		encoding and error handling and write the resulting <class>str</class>
		object to the output stream.
		"""
		self.stream.write(text)

	def writetext(self, text):
		"""
		<par>is used to write text data to the output stream. <arg>text</arg> must
		be a <class>unicode</class> object. The publisher will apply the configured
		encoding, error handling and the current text filter (which escapes
		characters that can't appear in text data (like <lit>&lt;</lit> etc.))
		and writes the resulting<class>str</class> object to the output stream.
		"""
		self.stream.errors = self.__currenterrors
		self.write(self.__currenttextfilter(text))
		self.stream.errors = "strict"

	def pushtextfilter(self, filter):
		"""
		<par>pushes a new text filter function on the text filter stack stack.
		This function is responsible for escaping characters that can't appear
		in text data (like <lit>&lt;</lit>)). This is used to switch on escaping
		of <lit>"</lit> inside attribute values.</par>
		"""
		self.__textfilters.append(filter)
		self.__currenttextfilter = filter

	def poptextfilter(self):
		"""
		<par>pops the current text filter function from the stack.</par>
		"""
		self.__textfilters.pop()
		if self.__textfilters:
			self.__currenttextfilter = self.__textfilters[-1]
		else:
			self.__currenttextfilter = None

	def pusherrors(self, errors):
		"""
		<par>pushes a new error handling scheme onto the error handling stack.</par>
		"""
		self.__errors.append(errors)
		self.__currenterrors = errors

	def poperrors(self):
		"""
		<par>pop the current error handling scheme from the error handling stack.</par>
		"""
		self.__errors.pop()
		if self.__errors:
			self.__currenterrors = self.__errors[-1]
		else:
			self.__currenterrors = "strict"

	def _neededxmlnsdefs(self, node):
		"""
		<par>Return a list of nodes in <arg>node</arg> that
		need a <lit>xmlns</lit> attribute.</par>
		"""
		if isinstance(node, xsc.Element):
			return [node]
		elif isinstance(node, xsc.Frag):
			nodes = []
			for child in node:
				nodes.extend(self._neededxmlnsdefs(child))
			return nodes
		return []

	def publish(self, stream, node, base=None):
		"""
		<par>publish the node <arg>node</arg> to the stream <arg>stream</arg>.
		All &url;s will be published relative to <arg>base</arg>.</par>
		"""
		def iselorat(node):
			return (isinstance(node, (xsc.Element, xsc.Attr)), xsc.entercontent, xsc.enterattrs)

		# We have to search for namespaces even if the prefix doesn't specify it,
		# because global attribute require xmlns attribute generation
		prefixes2def = {}
		# collect all the namespaces that are used and their required mode
		for child in node.walk(iselorat):
			if child.needsxmlns(self) == 2:
				prefixes2def[child.xmlns] = True

		# Determine if we have multiple roots
		if prefixes2def and isinstance(node, xsc.Frag) and len(node.find(xsc.FindType(xsc.Element))) > 1:
			raise errors.MultipleRootsError()

		if prefixes2def:
			self.publishxmlns = {} # signals that xmlns attributes should be generated to the first element encountered, if not empty
			# get the prefixes for all namespaces from the prefix mapping
			for ns in prefixes2def:
				self.publishxmlns[ns] = self.prefixes.prefix4ns(ns)[0]
		else:
			self.publishxmlns = None

		self.inattr = 0
		self.__textfilters = [ helpers.escapetext ]
		self.__currenttextfilter = helpers.escapetext

		self.__errors = [ "xmlcharrefreplace" ]
		self.__currenterrors = "xmlcharrefreplace"

		self.base = url.URL(base)
		self.node = node

		self.stream = codecs.getwriter(self.encoding)(stream)
		self.write = self.stream.write

		try:
			self.node.publish(self)
		finally:
			if "write" in self.__dict__: # Remove performance shortcut
				del self.write
			self.stream = None
	
		self.inattr = 0
		self.__textfilters = [ helpers.escapetext ]
		self.__currenttextfilter = helpers.escapetext

		self.__errors = [ "xmlcharrefreplace" ]
		self.__currenterrors = "xmlcharrefreplace"

		self.publishxmlns = None
