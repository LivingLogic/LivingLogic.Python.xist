#! /usr/bin/env python

## Copyright 1999-2000 by Living Logic AG, Bayreuth, Germany.
## Copyright 1999-2000 by Walter Dörwald
##
## See the file LICENSE for licensing details

"""
This module contains classes that may be used as publishing
handler in <methodref module="xist.xsc" class="Node">publish</methodref>.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import sys
import types
from encodings.aliases import aliases
import codecs
import options, xsc, utils

strescapes = {'<': 'lt', '>': 'gt', '&': 'amp', '"': 'quot'}

# the following is from ftp://ftp.isi.edu/in-notes/iana/assignments/character-sets
__encodings = {
	"ansi_x3.4-1968": "ascii",
	"iso-ir-6": "ascii",
	"ansi_x3.4-1986": "ascii",
	"iso_646.irv:1991": "ascii",
	"ascii": "ascii",
	"iso646-us": "ascii",
	"us-ascii": "ascii",
	"us": "ascii",
	"ibm367": "ascii",
	"cp367": "ascii",
	"csascii": "ascii",
	"ISO_8859-1:1987": "latin1",
	"iso-ir-100": "latin1",
	"ISO_8859-1": "latin1",
	"ISO-8859-1": "latin1",
	"latin1": "latin1",
	"l1": "latin1",
	"IBM819": "latin1",
	"CP819": "latin1",
	"csISOLatin1": "latin1",
}

def mustBeEncodedAsCharRef(char, encoding):
	encoding = encoding.lower()
	try:
		encoding = __encodings[encoding]
	except KeyError:
		pass
	if encoding=="ascii" and ord(char)>=128:
		return 1
	elif encoding=="latin1" and ord(char)>=256:
		return 1
	else:
		return 0

class Publisher:
	"""
	base class for all publishers.
	"""
	def __init__(self, encoding=None, XHTML=None):
		"""
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
		"""
		if encoding is None:
			encoding = options.outputEncoding
		self.encoding = encoding
		if XHTML is None:
			XHTML = options.outputXHTML
		if XHTML<0 or XHTML>2:
			raise ValueError("XHTML must be 0, 1 or 2")
		self.XHTML = XHTML

	def __call__(self, *texts):
		"""
		receives the strings to be printed.
		"""
		for text in texts:
			if type(text) in (types.ListType, types.TupleType):
				self(text)
			else:
				self.publish(utils.stringFromCode(text))

	def publish(self, text):
		"""
		overwrite this method
		"""
		pass

	def _encodeLegal(self, text):
		"""
		encodes the text <argref>text</argref> with the encoding <code><self/>.encoding</code>.
		using character references for <code>&amp;lt;</code> etc. and non encodabel characters
		is legal.
		"""
		v = []
		for c in text:
			if c == u'\r':
				continue
			if strescapes.has_key(c):
				v.append('&' + strescapes[c] + ';')
			elif mustBeEncodedAsCharRef(c, self.encoding):
				v.append('&#' + str(ord(c)) + ';')
			else:
				v.append(c)
		return u"".join(v)

	def _encodeIllegal(self, text):
		"""
		encodes the text <argref>text</argref> with the encoding <code><self/>.encoding</code>.
		anything that requires a character reference (e.g. element names) is illegal.
		"""
		v = []
		for c in text:
			if c == u'\r':
				continue
			if strescapes.has_key(c) or mustBeEncodedAsCharRef(c, self.encoding):
				raise EncodingImpossibleError(self.startloc, self.encoding, text, c)
			else:
				v.append(c)
		return u"".join(v)

class FilePublisher(Publisher):
	"""
	writes the strings to a file.
	"""
	def __init__(self, file, encoding=None, XHTML=None):
		Publisher.__init__(self, encoding, XHTML)
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
	def __init__(self, encoding=None, XHTML=None):
		FilePublisher.__init__(self, sys.stdout, encoding, XHTML)

class StringPublisher(Publisher):
	"""
	collects all strings in an array.
	The joined strings are available via
	<methodref>asString</methodref>
	"""

	def __init__(self, XHTML=None):
		Publisher.__init__(self, None, XHTML)
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

	def __init__(self, encoding=None, XHTML=None):
		Publisher.__init__(self, encoding, XHTML)
		self.texts = []

	def publish(self, text):
		self.texts.append(text)

	def asBytes(self):
		"""
		Return the published strings as one long byte string.
		"""
		return u"".join(self.texts).encode(self.encoding)

