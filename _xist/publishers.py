#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
<par>This module contains classes that may be used as publishing
handler in <pyref module="ll.xist.xsc" class="Node" method="publish"><method>publish</method></pyref>.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, codecs, types

from ll import url

import xsc, options, utils, errors, helpers

class Publisher(object):
	"""
	base class for all publishers.
	"""

	def __init__(self, base=None, root=None, encoding=None, xhtml=None, prefixes=None, elementmode=0, procinstmode=0, entitymode=0):
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

		<par><arg>prefixes</arg> is and instance of <pyref module="ll.xist.xsc" class="Prefixes"><class>Prefixes</class></pyref>
		and maps <pyref module="ll.xist.xsc" class="Namespace"><class>Namespace</class></pyref>
		objects to prefixes that should be used (or <lit>None</lit>, if no prefix should be used.).
		With <arg>elementmode</arg> you can specify how prefixes for elements should be
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
		self.elementmode = elementmode
		self.procinstmode = procinstmode
		self.entitymode = entitymode

		self.inAttr = 0
		self.__textFilters = [ helpers.escapeText ]
		self.__currentTextFilter = helpers.escapeText

	def publish(self, text):
		"""
		receives the strings to be printed.
		The strings are still unicode objects, and you have to do the encoding yourself.
		overwrite this method.
		"""
		pass

	def publishText(self, text):
		"""
		<par>is used to publish text data. This uses the current
		text filter, which is responsible for escaping characters.</par>
		"""
		self.publish(self.__currentTextFilter(text, self.encoding))

	def pushTextFilter(self, filter):
		"""
		<par>pushes a new text filter function.</par>
		"""
		self.__textFilters.append(filter)
		self.__currentTextFilter = filter

	def popTextFilter(self):
		self.__textFilters.pop()
		if self.__textFilters:
			self.__currentTextFilter = self.__textFilters[-1]
		else:
			self.__currentTextFilter = None

	def _neededxmlnsdefs(self, node):
		"""
		<par>Return a list of nodes in <arg>node</arg> that
		need a <lit>xmlns</lit> attribute.</par>
		"""
		if isinstance(node, (xsc.Element, xsc.ProcInst, xsc.Entity)):
			if node.needsxmlns(self)==xsc.Prefixes.DECLAREANDUSEPREFIX:
				return [node]
		elif isinstance(node, xsc.Frag):
			nodes = []
			for child in node:
				nodes.extend(self._neededxmlnsdefs(child))
			return nodes
		return []

	def beginPublication(self):
		"""
		<par>called once before the publication of the node <arg>node</arg> begins.</par>
		"""
		self.prefixes2use = {}
		# If no xmlns declaration attributes are to be used we don't have to do anything
		mode = xsc.Prefixes.DECLAREANDUSEPREFIX
		if self.elementmode==mode or self.procinstmode==mode or self.entitymode==mode:
			# Determine if we have to introduce an artificial root element that gets the xmlns attributes
			if not isinstance(self.node, xsc.Element): # An element is the wrapper itself
				needed = self._neededxmlnsdefs(self.node)
				if needed:
					if len(needed)>1 or not isinstance(needed[0], xsc.Element):
						from ll.xist.ns import specials
						self.node = specials.wrap(self.node)

			prefixes2use = {}
			# collect all the namespaces that are used and their required mode
			for child in self.node.walk(attrs=True):
				if isinstance(child, xsc.Element):
					type = xsc.Prefixes.ELEMENT
				elif isinstance(child, xsc.ProcInst):
					type = xsc.Prefixes.PROCINST
				elif isinstance(child, xsc.Entity):
					type = xsc.Prefixes.ENTITY
				else:
					continue
				prefixes2use[(type, child.xmlns)] = max(prefixes2use.get((type, child.xmlns), 0), child.needsxmlns(self))
			if len(prefixes2use):
				self.publishxmlns = None # signal to the first element that it should generate xmlns attributes
				# get the prefixes for all namespaces from the prefix mapping
				for (type, ns) in prefixes2use:
					nsprefix = [u"xmlns", u"procinstns", u"entityns"][type]
					self.prefixes2use[(nsprefix, ns)] = (prefixes2use[(type, ns)], self.prefixes.prefix4ns(ns, type)[0])

	def endPublication(self):
		"""
		<par>called once after the publication of the node <arg>node</arg> has ended.</par>
		"""
		del self.prefixes2use
		del self.node

	def doPublication(self, node):
		"""
		<par>performs the publication of the node <arg>node</arg>.</par>
		"""
		self.node = node
		self.beginPublication()
		self.node.publish(self) # use self.node, because it might have been replaced by beginPublication
		return self.endPublication()

class FilePublisher(Publisher):
	"""
	writes the strings to a file.
	"""
	def __init__(self, stream, base=None, root=None, encoding=None, xhtml=None, prefixes=None, elementmode=0, procinstmode=0, entitymode=0):
		super(FilePublisher, self).__init__(base=base, root=root, encoding=encoding, xhtml=xhtml, prefixes=prefixes, elementmode=elementmode, procinstmode=procinstmode, entitymode=entitymode)
		streamwriterclass = codecs.getwriter(self.encoding)
		self.stream = streamwriterclass(stream)

	def publish(self, text):
		self.stream.write(text)

	def tell(self):
		"""
		return the current position.
		"""
		return self.stream.tell()

class PrintPublisher(FilePublisher):
	"""
	writes the strings to <lit>sys.stdout</lit>.
	"""
	def __init__(self, base=None, root=None, encoding=None, xhtml=None, prefixes=None, elementmode=0, procinstmode=0, entitymode=0):
		super(PrintPublisher, self).__init__(sys.stdout, base=base, root=root, encoding=encoding, xhtml=xhtml, prefixes=prefixes, elementmode=elementmode, procinstmode=procinstmode, entitymode=entitymode)

class StringPublisher(Publisher):
	"""
	collects all strings in an array.
	The joined strings are available via
	<pyref module="ll.xist.publishers" class="StringPublisher" method="asString"><method>asString</method></pyref>
	"""

	def __init__(self, base=None, root=None, xhtml=None, prefixes=None, elementmode=0, procinstmode=0, entitymode=0):
		super(StringPublisher, self).__init__(base=base, root=root, encoding="utf16", xhtml=xhtml, prefixes=prefixes, elementmode=elementmode, procinstmode=procinstmode, entitymode=entitymode)

	def publish(self, text):
		self.texts.append(text)

	def beginPublication(self):
		super(StringPublisher, self).beginPublication()
		self.texts = []

	def endPublication(self):
		result = u"".join(self.texts)
		del self.texts
		super(StringPublisher, self).endPublication()
		return result

class BytePublisher(Publisher):
	"""
	collects all strings in an array.
	The joined strings are available via
	<pyref method="asBytes"><method>asBytes</method></pyref> as a byte
	string suitable for writing to a file.
	"""

	def publish(self, text):
		self.texts.append(text)

	def beginPublication(self):
		super(BytePublisher, self).beginPublication()
		self.texts = []

	def endPublication(self):
		result = u"".join(self.texts).encode(self.encoding)
		del self.texts
		super(BytePublisher, self).endPublication()
		return result

