#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
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
<doc:par>This module contains classes that may be used as publishing
handler in <pyref module="xist.xsc" class="Node" method="publish"><method>publish</method></pyref>.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, codecs

import xsc, options, utils, errors, url, helpers

class Publisher:
	"""
	base class for all publishers.
	"""

	def __init__(self, base=None, root=None, encoding=None, xhtml=None, publishPrefix=0):
		"""
		<doc:par><arg>base</arg> specifies the url to which the result
		will be output.</doc:par>

		<doc:par><arg>encoding</arg> specifies the encoding to be used.
		The encoding itself (i.e. calling <method>encode</method> on the
		unicode strings) must be done by <pyref method="publish"><method>xist.publishers.Publisher.publish</method></pyref>
		and not by <pyref module="xist.xsc" class="Node"><method>xist.xsc.Node.publish</method></pyref>.</doc:par>

		<doc:par>The only exception is in the case of encodings that can't encode
		the full range of unicode characters like <lit>us-ascii</lit>
		or <lit>iso-8859-1</lit>. In this case non encodable characters will be replaced
		by characters references (if possible, if not (e.g. in comments or processing
		instructions) an exception will be raised) before they are passed to
		<pyref method="publish"><method>publish</method></pyref>.</doc:par>

		<doc:par>With the parameter <arg>xhtml</arg> you can specify if you want &html; output
		(i.e. elements with a content model EMPTY as <markup>&lt;foo&gt;</markup>) with
		<code><arg>xhtml</arg>==0</code>, or XHTML output that is compatible with &html; browsers
		(element with an empty content model as <markup>&lt;foo /&gt;</markup> and others that
		just happen to be empty as <markup>&lt;foo&gt;&lt;/foo&gt;</markup>) with
		<code><arg>xhtml</arg>==1</code> or just plain XHTML with
		<code><arg>xhtml</arg>==2</code> (all empty elements as <markup>&lt;foo/&gt;</markup>).
		When you use the default (<code>None</code>) that value of the global variable
		<code>outputXHTML</code> will be used, which defaults to 1, but can be overwritten
		by the environment variable <code>XSC_OUTPUT_XHTML</code> and can of course be
		changed dynamically.</doc:par>

		<doc:par><arg>publishPrefix</arg> specifies if the prefix from element name
		should be output too.</doc:par>
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
		self.publishPrefix = publishPrefix
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
		<doc:par>is used to publish text data. This uses the current
		text filter, which is responsible for escaping characters.</doc:par>
		"""
		self.publish(self.__currentTextFilter(text, self.encoding))

	def pushTextFilter(self, filter):
		"""
		<doc:par>pushes a new text filter function.</doc:par>
		"""
		self.__textFilters.append(filter)
		self.__currentTextFilter = filter

	def popTextFilter(self):
		self.__textFilters.pop()
		if self.__textFilters:
			self.__currentTextFilter = self.__textFilters[-1]
		else:
			self.__currentTextFilter = None

class FilePublisher(Publisher):
	"""
	writes the strings to a file.
	"""
	def __init__(self, stream, base=None, root=None, encoding=None, xhtml=None, publishPrefix=0):
		Publisher.__init__(self, base=base, root=root, encoding=encoding, xhtml=xhtml, publishPrefix=publishPrefix)
		(encode, decode, streamReaderClass, streamWriterClass) = codecs.lookup(self.encoding)
		self.stream = streamWriterClass(stream)

	def publish(self, text):
		self.stream.write(text)

	def tell(self):
		"""
		return the current position.
		"""
		return self.stream.tell()

class PrintPublisher(FilePublisher):
	"""
	writes the strings to <code>sys.stdout</code>.
	"""
	def __init__(self, base=None, root=None, encoding=None, xhtml=None, publishPrefix=0):
		FilePublisher.__init__(self, sys.stdout, base=base, root=root, encoding=encoding, xhtml=xhtml, publishPrefix=publishPrefix)

class StringPublisher(Publisher):
	"""
	collects all strings in an array.
	The joined strings are available via
	<pyref module="xist.publishers" class="StringPublisher" method="asString"><method>asString</method></pyref>
	"""

	def __init__(self, base=None, root=None, xhtml=None, publishPrefix=0):
		Publisher.__init__(self, base=base, root=root, encoding="utf16", xhtml=xhtml, publishPrefix=publishPrefix)
		self.texts = []

	def publish(self, text):
		self.texts.append(text)

	def asString(self):
		"""
		Return the published strings as one long string.
		"""
		return u"".join(self.texts)

class BytePublisher(Publisher):
	"""
	collects all strings in an array.
	The joined strings are available via
	<pyref method="asBytes"><method>asBytes</method></pyref> as a byte
	string suitable for writing to a file.
	"""

	def __init__(self, base=None, root=None, encoding=None, xhtml=None, publishPrefix=0):
		Publisher.__init__(self, base=base, root=root, encoding=encoding, xhtml=xhtml, publishPrefix=publishPrefix)
		self.texts = []

	def publish(self, text):
		self.texts.append(text)

	def asBytes(self):
		"""
		Return the published strings as one long byte string.
		"""
		return u"".join(self.texts).encode(self.encoding)

