# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

# Copyright 2007-2019 by LivingLogic AG, Bayreuth/Germany
# Copyright 2007-2019 by Walter Dörwald
#
# All Rights Reserved
#
# See ll/xist/__init__.py for the license


"""
This module implements a codec that can be used for encoding and decoding XML.
Once the encoding has been determined the decoding/encoding process falls back
to using the codec for that particular encoding to do the rest of the work, so
this XML codec supports all encodings supported by Python itself.

On decoding the XML codec determines the encoding by either inspecting the
first few bytes of the byte stream/string or by extracting the encoding from
the XML declaration. If the encoding can't be determined from the first few
bytes and there is no XML declaration the codec falls back to using UTF-8.
When the encoding is specified by an external source (e.g. a Content-Type
header in an HTTP response), this encoding can be passed as an argument to the
codec, which will then bypass encoding detection. If there's an XML declaration
in the input, the XML declaration passed to the application then will contain
the externally specified encoding instead of the original one.

On encoding the XML codec extracts the encoding from the XML declaration and
will encode the output in that encoding. If there's no XML declaration UTF-8
will be used. It's possible to pass an external encoding to the encoder too.
The encoder will then encode the output in that encoding and put the correct
encoding into the XML declaration (if there is one).
"""


import codecs

try:
	from ._xml_codec import detectencoding as _detectencoding, fixencoding as _fixencoding
except ImportError:
	import re

	def _detectencoding(input, final=False):
		raise NotImplementedError("C module _xml_codec missing, _detectencoding() not supported")

	_xmlheader = re.compile("""(<\\?xml\\s+version\\s*=\\s*['"][^'"]+['"]\\s+encoding\\s*=\\s*['"])([^'"]+)(['"])""")

	def _fixencoding(input, encoding, final=False):
		if final or input.startswith("<?xml"):
			match = _xmlheader.match(input)
			if match:
				return ''.join((match.group(1), encoding, match.group(3), input[match.end(0):]))
			if "?>" in input or final:
				return input
			return None
		elif "<?xml".startswith(input[:5]):
			return None
		else:
			return input


def decode(input, errors="strict", encoding=None):
	if encoding is None:
		encoding = _detectencoding(input, True)
	if encoding == "xml":
		raise ValueError("xml not allowed as encoding name")
	(input, consumed) = codecs.getdecoder(encoding)(input, errors)
	return (_fixencoding(input, str(encoding), True), consumed)


def encode(input, errors="strict", encoding=None):
	consumed = len(input)
	if encoding is None:
		encoding = _detectencoding(input, True)
	else:
		input = _fixencoding(input, str(encoding), True)
	if encoding == "xml":
		raise ValueError("xml not allowed as encoding name")
	info = codecs.lookup(encoding)
	return (info.encode(input, errors)[0], consumed)


class IncrementalDecoder(codecs.IncrementalDecoder):
	def __init__(self, errors="strict", encoding=None):
		self.decoder = None
		self._initial_encoding = self.encoding = encoding
		codecs.IncrementalDecoder.__init__(self, errors)
		self._errors = errors # Store ``errors`` somewhere else, because we have to hide it in a property
		self.buffer = b""
		self.headerfixed = False

	def iterdecode(self, input):
		for part in input:
			result = self.decode(part, False)
			if result:
				yield result
		result = self.decode(b"", True)
		if result:
			yield result

	def decode(self, input, final=False):
		# We're doing basically the same as a ``BufferedIncrementalDecoder``,
		# but since the buffer is only relevant until the encoding has been detected
		# (in which case the buffer of the underlying codec might kick in),
		# we're implementing buffering ourselves to avoid some overhead.
		if self.decoder is None:
			input = self.buffer + input
			if self.encoding is None:
				self.encoding = _detectencoding(input, final)
				if self.encoding is None:
					self.buffer = input # retry the complete input on the next call
					return "" # no encoding determined yet, so no output
			if self.encoding == "xml":
				raise ValueError("xml not allowed as encoding name")
			self.buffer = b"" # isn't needed any more, as the decoder might keep its own buffer
			self.decoder = codecs.getincrementaldecoder(self.encoding)(self._errors)
		if self.headerfixed:
			return self.decoder.decode(input, final)
		# If we haven't fixed the header yet, the content of ``self.buffer`` is a :class:`str` object
		buffer = self.buffer
		if isinstance(buffer, bytes):
			buffer = buffer.decode("ascii")
		output = buffer + self.decoder.decode(input, final)
		newoutput = _fixencoding(output, self.encoding, final)
		if newoutput is None:
			self.buffer = output # retry fixing the declaration (but keep the decoded stuff)
			return ""
		self.headerfixed = True
		return newoutput

	def reset(self):
		codecs.IncrementalDecoder.reset(self)
		self.encoding = self._initial_encoding
		self.decoder = None
		self.buffer = b""
		self.headerfixed = False

	def _geterrors(self):
		return self._errors

	def _seterrors(self, errors):
		# Setting ``errors`` must be done on the real decoder too
		if self.decoder is not None:
			self.decoder.errors = errors
		self._errors = errors
	errors = property(_geterrors, _seterrors)


class IncrementalEncoder(codecs.IncrementalEncoder):
	def __init__(self, errors="strict", encoding=None):
		self.encoder = None
		self._initial_encoding = self.encoding = encoding
		codecs.IncrementalEncoder.__init__(self, errors)
		self._errors = errors # Store ``errors`` somewhere else, because we have to hide it in a property
		self.buffer = ""

	def iterencode(self, input):
		for part in input:
			result = self.encode(part, False)
			if result:
				yield result
		result = self.encode("", True)
		if result:
			yield result

	def encode(self, input, final=False):
		if self.encoder is None:
			input = self.buffer + input
			if self.encoding is not None:
				# Replace encoding in the declaration with the specified one
				newinput = _fixencoding(input, str(self.encoding), final)
				if newinput is None: # declaration not complete => Retry next time
					self.buffer = input
					return b""
				input = newinput
			else:
				# Use encoding from the XML declaration
				self.encoding = _detectencoding(input, final)
			if self.encoding is not None:
				if self.encoding == "xml":
					raise ValueError("xml not allowed as encoding name")
				info = codecs.lookup(self.encoding)
				self.encoder = info.incrementalencoder(self._errors)
				self.buffer = ""
			else:
				self.buffer = input
				return b""
		return self.encoder.encode(input, final)

	def reset(self):
		codecs.IncrementalEncoder.reset(self)
		self.encoding = self._initial_encoding
		self.encoder = None
		self.buffer = ""

	def _geterrors(self):
		return self._errors

	def _seterrors(self, errors):
		# Setting ``errors ``must be done on the real encoder too
		if self.encoder is not None:
			self.encoder.errors = errors
		self._errors = errors
	errors = property(_geterrors, _seterrors)


class StreamWriter(codecs.StreamWriter):
	def __init__(self, stream, errors="strict", encoding="utf-8", header=False):
		codecs.StreamWriter.__init__(self, stream, errors)
		self.encoder = IncrementalEncoder(errors)
		self._errors = errors

	def encode(self, input, errors='strict'):
		return (self.encoder.encode(input, False), len(input))

	def _geterrors(self):
		return self._errors

	def _seterrors(self, errors):
		# Setting ``errors`` must be done on the encoder too
		if self.encoder is not None:
			self.encoder.errors = errors
		self._errors = errors
	errors = property(_geterrors, _seterrors)


class StreamReader(codecs.StreamReader):
	def __init__(self, stream, errors="strict"):
		codecs.StreamReader.__init__(self, stream, errors)
		self.decoder = IncrementalDecoder(errors)
		self._errors = errors

	def decode(self, input, errors='strict'):
		return (self.decoder.decode(input, False), len(input))

	def _geterrors(self):
		return self._errors

	def _seterrors(self, errors):
		# Setting ``errors`` must be done on the decoder too
		if self.decoder is not None:
			self.decoder.errors = errors
		self._errors = errors
	errors = property(_geterrors, _seterrors)


def search_function(name):
	if name == "xml":
		return codecs.CodecInfo(
			name="xml",
			encode=encode,
			decode=decode,
			incrementalencoder=IncrementalEncoder,
			incrementaldecoder=IncrementalDecoder,
			streamwriter=StreamWriter,
			streamreader=StreamReader,
		)


codecs.register(search_function)
