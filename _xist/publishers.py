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
handler in <pyref module="xist.xsc" class="Node">publish</pyref>.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, types, array, codecs

import xsc, options, utils, errors, url, helpers

class Publisher:
	"""
	base class for all publishers.
	"""

	def __init__(self, base=None, root=None, encoding=None, xhtml=None, publishPrefix=0):
		"""
		<doc:par><pyref arg="base">base</pyref> specifies the url to which the result
		will be output.</doc:par>

		<doc:par><pyref arg="encoding">encoding</pyref> specifies the encoding to be used.
		The encoding itself (i.e. calling <code>encode</code> on the
		unicode strings) must be done by <pyref method="publish">xist.publishers.Publisher.publish</pyref>
		and not by <pyref module="xist.xsc" class="Node">xist.xsc.Node.publish</pyref>.</doc:par>

		<doc:par>The only exception is in the case of encodings that can't encode
		the full range of unicode characters like <code>us-ascii</code>
		or <code>iso-8859-1</code>. In this case non encodable characters will be replaced
		by characters references (if possible, if not (e.g. in comments or processing
		instructions) an exception will be raised) before they are passed to
		<pyref method="publish">publish</pyref>.</doc:par>

		<doc:par>With the parameter <pyref arg="xhtml">xhtml</pyref> you can specify if you want &html; output
		(i.e. elements with a content model EMPTY as <code>&lt;foo&gt;</code>) with
		<code><pyref arg="xhtml">xhtml</pyref>==0</code>, or XHTML output that is compatible with &html; browsers
		(element with an empty content model as <code>&lt;foo /&gt;</code> and others that
		just happen to be empty as <code>&lt;foo&gt;&lt;/foo&gt;</code>) with
		<code><pyref arg="xhtml">xhtml</pyref>==1</code> or just plain XHTML with
		<code><pyref arg="xhtml">xhtml</pyref>==2</code> (all empty elements as <code>&lt;foo/&gt;</code>).
		When you use the default (<code>None</code>) that value of the global variable
		<code>outputXHTML</code> will be used, which defaults to 1, but can be overwritten
		by the environment variable <code>XSC_OUTPUT_XHTML</code> and can of course be
		changed dynamically.</doc:par>

		<doc:par><pyref arg="publishPrefix">publishPrefix</pyref> specifies if the prefix from element name
		should be output too.</doc:par>
		"""
		if base is None:
			self.base = url.URL(scheme="root")
		else:
			self.base = url.URL(scheme="root")/url.URL(base)
		if root is None:
			self.root = url.URL(scheme="root")
		else:
			self.root = url.URL(scheme="root")/url.URL(root)
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
	<pyref module="xist.publishers" class="StringPublisher" method="asString">asString</pyref>
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
	<pyref method="asBytes">asBytes</pyref> as a byte
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

