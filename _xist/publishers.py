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
handler in <pyref module="ll.xist.xsc" class="Node" method="publish"><method>publish</method></pyref>.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, codecs

from ll import url

import xsc, options, helpers, errors


def cssescapereplace(exc):
	if not isinstance(exc, UnicodeEncodeError):
		raise TypeError("don't know how to handle %r" % exc)
	return (helpers.cssescapereplace(exc.object[exc.start:exc.end], exc.encoding), exc.end)
codecs.register_error("cssescapereplace", cssescapereplace)


class Publisher(object):
	"""
	base class for all publishers.
	"""

	def __init__(self, encoding="utf-8", xhtml=1, prefixes=None, prefixmode=0):
		"""
		<par><arg>encoding</arg> specifies the encoding to be used.
		The encoding itself (i.e. calling <method>encode</method> on the
		unicode strings) must be done by <pyref method="publish"><method>ll.xist.publishers.Publisher.publish</method></pyref>
		and not by <pyref module="ll.xist.xsc" class="Node"><method>ll.xist.xsc.Node.publish</method></pyref>.</par>

		<par>The only exception is in the case of encodings that can't encode
		the full range of unicode characters like <lit>us-ascii</lit>
		or <lit>iso-8859-1</lit>. In this case non encodable characters will be replaced
		by characters references (if possible, if not (e.g. in comments or processing
		instructions) an exception will be raised) before they are passed to
		<pyref method="publish"><method>publish</method></pyref>.</par>

		<par>With the parameter <arg>xhtml</arg> you can specify if you want &html; output
		(i.e. elements with a content model EMPTY as <markup>&lt;foo&gt;</markup>) with
		<lit><arg>xhtml</arg>==0</lit>, or XHTML output that is compatible with &html; browsers
		(element with an empty content model as <markup>&lt;foo /&gt;</markup> and others that
		just happen to be empty as <markup>&lt;foo&gt;&lt;/foo&gt;</markup>) with
		<lit><arg>xhtml</arg>==1</lit> or just plain XHTML with
		<lit><arg>xhtml</arg>==2</lit> (all empty elements as <markup>&lt;foo/&gt;</markup>).
		When you use the default (<lit>None</lit>) that value of the global variable
		<lit>outputXHTML</lit> will be used, which defaults to <lit>1</lit>, but can be overwritten
		by the environment variable <lit>XSC_OUTPUT_XHTML</lit> and can of course be
		changed dynamically.</par>

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

		if prefixes is None:
			prefixes = xsc.OldPrefixes()
		self.prefixes = prefixes
		self.prefixmode = prefixmode

	def publish(self, text):
		"""
		receives the strings to be printed.
		The strings are still unicode objects, and you have to do the encoding yourself.
		overwrite this method.
		"""
		self.stream.write(text)

	def publishtext(self, text):
		"""
		<par>is used to publish text data. This uses the current
		text filter, which is responsible for escaping characters.</par>
		"""
		self.stream.errors = self.__currenterrors
		self.publish(self.__currenttextfilter(text))
		self.stream.errors = "strict"

	def pushtextfilter(self, filter):
		"""
		<par>pushes a new text filter function.</par>
		"""
		self.__textfilters.append(filter)
		self.__currenttextfilter = filter

	def poptextfilter(self):
		self.__textfilters.pop()
		if self.__textfilters:
			self.__currenttextfilter = self.__textfilters[-1]
		else:
			self.__currenttextfilter = None

	def pusherrors(self, errors):
		"""
		<par>pushes a new error handling function.</par>
		"""
		self.__errors.append(errors)
		self.__currenterrors = errors

	def poperrors(self):
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

	def beginpublication(self, stream, node, base=None):
		"""
		<par>called once before the publication of the node <arg>node</arg> begins.</par>
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

		# Determine if we have to introduce an artificial root element that gets the xmlns attributes
		if prefixes2def and isinstance(node, xsc.Frag) and len(node.find(xsc.FindType(xsc.Element))) > 1:
			raise errors.MultipleRootsError()

		if prefixes2def:
			self.publishxmlns = {}
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

		self.stream = codecs.getwriter(self.encoding)(stream)
		self.publish = self.stream.write

		self.base = url.URL(base)
		self.node = node

	def endpublication(self):
		"""
		<par>called once after the publication of the node <arg>node</arg> has ended.</par>
		"""
		self.inattr = 0
		self.__textfilters = [ helpers.escapetext ]
		self.__currenttextfilter = helpers.escapetext

		self.__errors = [ "xmlcharrefreplace" ]
		self.__currenterrors = "xmlcharrefreplace"

		if "publish" in self.__dict__: # Remove performance shortcut
			del self.publish

		self.publishxmlns = None # signals that xmlns attributes should be generated to the first element encountered, if not empty
		self.stream = None

	def dopublication(self, stream, node, base=None):
		"""
		<par>performs the publication of the node <arg>node</arg>.</par>
		"""
		try:
			self.beginpublication(stream, node, base)
			self.node.publish(self) # use self.node, because it might have been replaced by beginpublication()
		finally:
			self.endpublication()
