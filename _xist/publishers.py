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
This module contains classes that may be used as publishing
handler in <methodref module="xist.xsc" class="Node">publish</methodref>.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, types, array, codecs

import xsc, options, utils, errors, url, helpers

class Publisher:
	"""
	base class for all publishers.
	"""

	def __init__(self, base=None, encoding=None, XHTML=None, publishPrefix=0):
		"""
		<par><argref>base</argref> specifies the url to which the result
		will be output.</par>

		<par><argref>encoding</argref> specifies the encoding to be used.
		The encoding itself (i.e. calling <code>encode</code> on the
		unicode strings) must be done by <methodref>publish</methodref>
		and not by <methodref class="xsc.Node">publish</methodref>.</par>

		<par>The only exception is in the case of encodings that can't encode
		the full range of unicode characters like <code>us-ascii</code>
		or <code>iso-8859-1</code>. In this case non encodable characters will be replaced
		by characters references (if possible, if not (e.g. in comments or processing
		instructions) an exception will be raised) before they are passed to
		<methodref>publish</methodref>.</par>

		<par>With the parameter <argref>XHTML</argref> you can specify if you want HTML output
		(i.e. elements with a content model EMPTY as <code>&lt;foo&gt;</code>) with
		<code><argref>XHTML</argref>==0</code>, or XHTML output that is compatible with HTML browsers
		(element with an empty content model as <code>&lt;foo /&gt;</code> and others that
		just happen to be empty as <code>&lt;foo&gt;&lt;/foo&gt;</code>) with
		<code><argref>XHTML</argref>==1</code> or just plain XHTML with
		<code><argref>XHTML</argref>==2</code> (all empty elements as <code>&lt;foo/&gt;</code>).
		When you use the default (None) that value of the global variable
		outputXHTML will be used, which defaults to 1, but can be overwritten
		by the environment variable XSC_OUTPUT_XHTML and can of course be
		changed dynamically.</par>

		<par>publishPrefix specifies if the prefix from element name should be output too.</par>
		"""
		if base is None:
			base = url.URL(scheme="root")
		base = url.URL(scheme="root") + base
		self.base = base
		if encoding is None:
			encoding = options.outputEncoding
		self.encoding = encoding
		if XHTML is None:
			XHTML = options.outputXHTML
		if XHTML<0 or XHTML>2:
			raise ValueError("XHTML must be 0, 1 or 2, not %r" % (XHTML,))
		self.XHTML = XHTML
		self.publishPrefix = publishPrefix
		self.inAttr = 0

	def publish(self, text):
		"""
		receives the strings to be printed.
		The strings are still unicode objects, and you have to do the encoding yourself.
		overwrite this method.
		"""
		pass

	def publishText(self, text):
		if self.inAttr:
			self.publish(helpers.escapeAttr(text, self.encoding))
		else:
			self.publish(helpers.escapeText(text, self.encoding))

class FilePublisher(Publisher):
	"""
	writes the strings to a file.
	"""
	def __init__(self, file, base=None, encoding=None, XHTML=None, publishPrefix=0):
		Publisher.__init__(self, base=base, encoding=encoding, XHTML=XHTML, publishPrefix=publishPrefix)
		(encode, decode, streamReaderClass, streamWriterClass) = codecs.lookup(self.encoding)
		self.file = streamWriterClass(file)

	def publish(self, text):
		self.file.write(text)

	def tell(self):
		"""
		return the current position.
		"""
		return self.file.tell()

class PrintPublisher(FilePublisher):
	"""
	writes the strings to <code>sys.stdout</code>.
	"""
	def __init__(self, base=None, encoding=None, XHTML=None, publishPrefix=0):
		FilePublisher.__init__(self, sys.stdout, base=base, encoding=encoding, XHTML=XHTML, publishPrefix=publishPrefix)

class StringPublisher(Publisher):
	"""
	collects all strings in an array.
	The joined strings are available via
	<methodref>asString</methodref>
	"""

	def __init__(self, base=None, XHTML=None, publishPrefix=0):
		Publisher.__init__(self, base=base, encoding="utf16", XHTML=XHTML, publishPrefix=publishPrefix)
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
	<methodref>asBytes</methodref> as a byte
	string suitable for writing to a file.
	"""

	def __init__(self, base=None, encoding=None, XHTML=None, publishPrefix=0):
		Publisher.__init__(self, base=base, encoding=encoding, XHTML=XHTML, publishPrefix=publishPrefix)
		self.texts = []

	def publish(self, text):
		self.texts.append(text)

	def asBytes(self):
		"""
		Return the published strings as one long byte string.
		"""
		return u"".join(self.texts).encode(self.encoding)

