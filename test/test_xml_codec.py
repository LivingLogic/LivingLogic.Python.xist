#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2007-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2007-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import py.test

import codecs

from ll import xml_codec # registers the codec

try:
	codecs.lookup("utf-32")
except LookupError:
	haveutf32 = False
else:
	haveutf32 = True


def test_detectencoding_str():
	assert xml_codec._detectencoding("") is None
	assert xml_codec._detectencoding("\xef") is None
	assert xml_codec._detectencoding("\xef\x33") == "utf-8"
	assert xml_codec._detectencoding("\xef\xbb") is None
	assert xml_codec._detectencoding("\xef\xbb\x33") == "utf-8"
	assert xml_codec._detectencoding("\xef\xbb\xbf") == "utf-8-sig"
	assert xml_codec._detectencoding("\xff") is None
	assert xml_codec._detectencoding("\xff\x33") == "utf-8"
	assert xml_codec._detectencoding("\xff\xfe") is None
	assert xml_codec._detectencoding("\xff\xfe\x33") == "utf-16"
	assert xml_codec._detectencoding("\xff\xfe\x00") is None
	assert xml_codec._detectencoding("\xff\xfe\x00\x33") == "utf-16"
	assert xml_codec._detectencoding("\xff\xfe\x00\x00") == "utf-32"
	assert xml_codec._detectencoding("\x00") is None
	assert xml_codec._detectencoding("\x00\x33") == "utf-8"
	assert xml_codec._detectencoding("\x00\x00") is None
	assert xml_codec._detectencoding("\x00\x00\x33") == "utf-8"
	assert xml_codec._detectencoding("\x00\x00\xfe") is None
	assert xml_codec._detectencoding("\x00\x00\x00\x33") == "utf-8"
	assert xml_codec._detectencoding("\x00\x00\x00<") == "utf-32-be"
	assert xml_codec._detectencoding("\x00\x00\xfe\xff") == "utf-32"
	assert xml_codec._detectencoding("<") is None
	assert xml_codec._detectencoding("<\x33") == "utf-8"
	assert xml_codec._detectencoding("<\x00") is None
	assert xml_codec._detectencoding("<\x00\x33") == "utf-8"
	assert xml_codec._detectencoding("<\x00\x00") is None
	assert xml_codec._detectencoding("<\x00\x00\x33") == "utf-8"
	assert xml_codec._detectencoding("<\x00\x00\x00") == "utf-32-le"
	assert xml_codec._detectencoding("\x4c") is None
	assert xml_codec._detectencoding("\x4c\x33") == "utf-8"
	assert xml_codec._detectencoding("\x4c\x6f") is None
	assert xml_codec._detectencoding("\x4c\x6f\x33") == "utf-8"
	assert xml_codec._detectencoding("\x4c\x6f\xa7") is None
	assert xml_codec._detectencoding("\x4c\x6f\xa7\x33") == "utf-8"
	assert xml_codec._detectencoding("\x4c\x6f\xa7\x94") == "cp037"
	assert xml_codec._detectencoding("<?") is None
	assert xml_codec._detectencoding("<?x") is None
	assert xml_codec._detectencoding("<?xm") is None
	assert xml_codec._detectencoding("<?xml") is None
	assert xml_codec._detectencoding("<?xml\r") is None
	assert xml_codec._detectencoding("<?xml\rversion='1.0'") is None
	assert xml_codec._detectencoding("<?xml\rversion='1.0' encoding='x") is None
	assert xml_codec._detectencoding("<?xml\rversion='1.0' encoding='x'") == "x"
	assert xml_codec._detectencoding('<?xml\rversion="1.0" encoding="x"') == "x"
	assert xml_codec._detectencoding('<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x"') == "x"
	assert xml_codec._detectencoding("<?xml\rversion='1.0' ?>") == "utf-8"
	assert xml_codec._detectencoding("<?xml\rversion='1.0' Encoding='x'") is None # encoding not recognized (might come later)
	assert xml_codec._detectencoding("<?xml\rVersion='1.0'") is None
	py.test.raises(ValueError, xml_codec._detectencoding, "<?xml\rversion='1.0' encoding=''") # empty encoding
	assert xml_codec._detectencoding("<", False) is None
	assert xml_codec._detectencoding("<", True) == "utf-8"
	assert xml_codec._detectencoding("<?", False) is None
	assert xml_codec._detectencoding("<?", True) == "utf-8"


def test_detectencoding_unicode():
	# Unicode version (only parses the header)
	assert xml_codec._detectencoding(u'<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x') is None
	assert xml_codec._detectencoding(u'<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x', True) == "utf-8"
	assert xml_codec._detectencoding(u'<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x"') == "x"


def test_fixencoding():
	s = u'<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x'
	assert xml_codec._fixencoding(s, u"utf-8") is None

	s = u'<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x'
	assert xml_codec._fixencoding(s, u"utf-8", True) == s

	s = u'<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x"?>'
	assert xml_codec._fixencoding(s, u"utf-8") == s.replace('"x"', '"utf-8"')


def check_partial(decoder, input, *parts):
	assert len(input) == len(parts)
	for (c, part) in zip(input, parts):
		assert decoder.decode(c) == part


def test_partial():
	decoder = codecs.getincrementaldecoder("xml")()

	# UTF-16
	check_partial(decoder, u"\ufeff".encode("utf-16-be"), u"", u"")
	decoder.reset()

	check_partial(decoder, u"\ufeff".encode("utf-16-le"), u"", u"")
	decoder.reset()

	result = (u"", u"", u"", u"\u1234", u"", u"a")

	check_partial(decoder, u"\u1234a".encode("utf-16"), *result)
	decoder.reset()

	# Fake utf-16 stored big endian
	check_partial(decoder, u"\ufeff\u1234a".encode("utf-16-be"), *result)
	decoder.reset()

	# Fake utf-16 stored little endian
	check_partial(decoder, u"\ufeff\u1234a".encode("utf-16-le"), *result)
	decoder.reset()

	# UTF-32
	if haveutf32:
		result = (u"", u"", u"", u"", u"", u"", u"", u"\u1234", u"", u"", u"", u"a")
		check_partial(decoder, u"\u1234a".encode("utf-32"), *result)
		decoder.reset()
	
		# Fake utf-32 stored big endian
		check_partial(decoder, u"\ufeff\u1234a".encode("utf-32-be"), *result)
		decoder.reset()
	
		# Fake utf-32 stored little endian
		check_partial(decoder, u"\ufeff\u1234a".encode("utf-32-le"), *result)
		decoder.reset()

	# UTF-8-Sig
	check_partial(decoder, u"\u1234a".encode("utf-8-sig"), u"", u"", u"", u"", u"", u"\u1234", u"a")
	decoder.reset()


def test_decoder():
	def checkauto(encoding, input=u"<?xml version='1.0' encoding='x'?>gürk\u20ac"):
		# Check stateless decoder
		d = codecs.getdecoder("xml")
		assert d(input.encode(encoding))[0] == input.replace("'x'", repr(encoding))

		# Check stateless decoder with specified encoding
		assert d(input.encode(encoding), encoding=encoding)[0] == input.replace("'x'", repr(encoding))

		# Check incremental decoder
		id = codecs.getincrementaldecoder("xml")()
		assert "".join(id.iterdecode(input.encode(encoding))) == input.replace("'x'", repr(encoding))

		# Check incremental decoder with specified encoding
		id = codecs.getincrementaldecoder("xml")(encoding)
		assert "".join(id.iterdecode(input.encode(encoding))) == input.replace("'x'", repr(encoding))

	# Autodetectable encodings
	yield checkauto, "utf-8-sig"
	yield checkauto, "utf-16"
	yield checkauto, "utf-16-le"
	yield checkauto, "utf-16-be"
	if haveutf32:
		yield checkauto, "utf-32"
		yield checkauto, "utf-32-le"
		yield checkauto, "utf-32-be"

	def checkdecl(encoding, input=u"<?xml version='1.0' encoding=%r?><gürk>\u20ac</gürk>"):
		# Check stateless decoder with encoding autodetection
		d = codecs.getdecoder("xml")
		input = input % encoding
		assert d(input.encode(encoding))[0] == input

		# Check stateless decoder with specified encoding
		assert d(input.encode(encoding), encoding=encoding)[0] == input

		# Check incremental decoder with encoding autodetection
		id = codecs.getincrementaldecoder("xml")()
		assert "".join(id.iterdecode(input.encode(encoding))) == input

		# Check incremental decoder with specified encoding
		id = codecs.getincrementaldecoder("xml")(encoding)
		assert "".join(id.iterdecode(input.encode(encoding))) == input

	# Use correct declaration
	yield checkdecl, "utf-8"
	yield checkdecl, "iso-8859-1", u"<?xml version='1.0' encoding=%r?><gürk/>"
	yield checkdecl, "iso-8859-15"
	yield checkdecl, "cp1252"

	# No recursion
	py.test.raises(ValueError, "<?xml version='1.0' encoding='xml'?><gurk/>".decode, "xml")


def test_encoder():
	def check(encoding, input=u"<?xml version='1.0' encoding='x'?>gürk\u20ac"):
		# Check stateless encoder with encoding autodetection
		e = codecs.getencoder("xml")
		inputdecl = input.replace("'x'", repr(encoding))
		assert e(inputdecl)[0].decode(encoding) == inputdecl

		# Check stateless encoder with specified encoding
		assert e(input, encoding=encoding)[0].decode(encoding) == inputdecl

		# Check incremental encoder with encoding autodetection
		ie = codecs.getincrementalencoder("xml")()
		assert "".join(ie.iterencode(inputdecl)).decode(encoding) == inputdecl

		# Check incremental encoder with specified encoding
		ie = codecs.getincrementalencoder("xml")(encoding=encoding)
		assert "".join(ie.iterencode(input)).decode(encoding) == inputdecl

	# Autodetectable encodings
	yield check, "utf-8-sig"
	yield check, "utf-16"
	yield check, "utf-16-le"
	yield check, "utf-16-be"
	if haveutf32:
		yield check, "utf-32"
		yield check, "utf-32-le"
		yield check, "utf-32-be"
	yield check, "utf-8"
	yield check, "iso-8859-1", u"<?xml version='1.0' encoding='x'?><gürk/>"
	yield check, "iso-8859-15"
	yield check, "cp1252"

	# No recursion
	py.test.raises(ValueError, u"<?xml version='1.0' encoding='xml'?><gurk/>".encode, "xml")
	