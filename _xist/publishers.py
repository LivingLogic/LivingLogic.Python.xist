#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
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

import sys, codecs, cStringIO

from ll import url

import xsc, options, helpers


def cssescapereplace(exc):
	if not isinstance(exc, UnicodeEncodeError):
		raise TypeError("don't know how to handle %r" % exc)
	return (helpers.cssescapereplace(exc.object[exc.start:exc.end], exc.encoding), exc.end)
codecs.register_error("cssescapereplace", cssescapereplace)


class Publisher(object):
	"""
	base class for all publishers.
	"""

	def __init__(self, stream, base=None, root=None, encoding=None, xhtml=None, prefixes=None, prefixmode=0):
		"""
		<par><arg>base</arg> specifies the url to which the result
		will be output.</par>

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
		<par><arg>procinstmode</arg> is used for processing instructions
		and <arg>entitymode</arg> for entities.</par>
		"""
		self.base = url.URL(base)
		self.root = url.URL(root)
		if encoding is None:
			encoding = options.outputEncoding
		self.encoding = encoding
		if xhtml is None:
			xhtml = options.outputXHTML
		if xhtml<0 or xhtml>2:
			raise ValueError("xhtml must be 0, 1 or 2, not %r" % (xhtml,))
		self.xhtml = xhtml

		if prefixes is None:
			prefixes = xsc.OldPrefixes()
		self.prefixes = prefixes
		self.prefixmode = prefixmode

		self.inAttr = 0
		self.__textfilters = [ helpers.escapetext ]
		self.__currenttextfilter = helpers.escapetext

		self.__errors = [ "xmlcharrefreplace" ]
		self.__currenterrors = "xmlcharrefreplace"

		streamwriterclass = codecs.getwriter(self.encoding)
		self.stream = streamwriterclass(stream)
		self.publish = self.stream.write

		self.publishxmlns = None # signals that xmlns attributes should be generated to the first element encountered, if not empty

	def publish(self, text):
		"""
		receives the strings to be printed.
		The strings are still unicode objects, and you have to do the encoding yourself.
		overwrite this method.
		"""
		self.stream.write(text)

	def publishText(self, text):
		"""
		<par>is used to publish text data. This uses the current
		text filter, which is responsible for escaping characters.</par>
		"""
		self.stream.errors = self.__currenterrors
		self.publish(self.__currenttextfilter(text))
		self.stream.errors = "strict"

	def pushTextFilter(self, filter):
		"""
		<par>pushes a new text filter function.</par>
		"""
		self.__textfilters.append(filter)
		self.__currenttextfilter = filter

	def popTextFilter(self):
		self.__textfilters.pop()
		if self.__textfilters:
			self.__currenttextfilter = self.__textfilters[-1]
		else:
			self.__currenttextfilter = None

	def pushErrors(self, errors):
		"""
		<par>pushes a new error handling function.</par>
		"""
		self.__errors.append(errors)
		self.__currenterrors = errors

	def popErrors(self):
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

	def beginpublication(self):
		"""
		<par>called once before the publication of the node <arg>node</arg> begins.</par>
		"""
		def iselorat(node):
			return (isinstance(node, (xsc.Element, xsc.Attr)), xsc.entercontent, xsc.enterattrs)

		# We have to search for namespaces even if the prefix doesn't specify it,
		# because global attribute require xmlns attribute generation
		prefixes2def = {}
		# collect all the namespaces that are used and their required mode
		for child in self.node.walk(iselorat):
			if child.needsxmlns(self) == 2:
				prefixes2def[child.xmlns] = True

		# Determine if we have to introduce an artificial root element that gets the xmlns attributes
		if prefixes2def and isinstance(self.node, xsc.Frag) and len(self.node.find(xsc.FindType(xsc.Element))) > 1:
			raise errors.MultipleRootsError()

		if prefixes2def:
			self.publishxmlns = {}
			# get the prefixes for all namespaces from the prefix mapping
			for ns in prefixes2def:
				self.publishxmlns[ns] = self.prefixes.prefix4ns(ns)[0]

	def endpublication(self):
		"""
		<par>called once after the publication of the node <arg>node</arg> has ended.</par>
		"""
		del self.node
		self.publishxmlns = None

	def dopublication(self, node):
		"""
		<par>performs the publication of the node <arg>node</arg>.</par>
		"""
		self.node = node
		self.beginpublication()
		self.node.publish(self) # use self.node, because it might have been replaced by beginpublication()
		return self.endpublication()

	def tell(self):
		"""
		return the current position.
		"""
		return self.stream.tell()

FilePublisher = Publisher


class PrintPublisher(Publisher):
	"""
	writes the strings to <lit>sys.stdout</lit>.
	"""
	def __init__(self, base=None, root=None, encoding=None, xhtml=None, prefixes=None, prefixmode=0):
		super(PrintPublisher, self).__init__(sys.stdout, base=base, root=root, encoding=encoding, xhtml=xhtml, prefixes=prefixes, prefixmode=prefixmode)


class BytePublisher(Publisher):
	"""
	collects all strings in an array.
	The joined strings are available via
	<pyref method="asBytes"><method>asBytes</method></pyref> as a byte
	string suitable for writing to a file.
	"""

	def __init__(self, base=None, root=None, encoding=None, xhtml=None, prefixes=None, prefixmode=0):
		super(BytePublisher, self).__init__(cStringIO.StringIO(), base=base, root=root, encoding=encoding, xhtml=xhtml, prefixes=prefixes, prefixmode=prefixmode)

	def endpublication(self):
		result = self.stream.getvalue()
		super(BytePublisher, self).endpublication()
		return result


class StringPublisher(BytePublisher):
	"""
	collects all strings in an array.
	The joined strings are available via
	<pyref module="ll.xist.publishers" class="StringPublisher" method="asString"><method>asString</method></pyref>
	"""

	def __init__(self, base=None, root=None, xhtml=None, prefixes=None, prefixmode=0):
		super(StringPublisher, self).__init__(base=base, root=root, encoding="utf8", xhtml=xhtml, prefixes=prefixes, prefixmode=prefixmode)

	def endpublication(self):
		result = super(StringPublisher, self).endpublication()
		return unicode(result, "utf8")
