#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2007-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2007-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import pytest

import codecs

from ll import xml_codec # registers the codec


def test_detectencoding_str():
	assert xml_codec._detectencoding(b"") is None
	assert xml_codec._detectencoding(b"\xef") is None
	assert xml_codec._detectencoding(b"\xef\x33") == "utf-8"
	assert xml_codec._detectencoding(b"\xef\xbb") is None
	assert xml_codec._detectencoding(b"\xef\xbb\x33") == "utf-8"
	assert xml_codec._detectencoding(b"\xef\xbb\xbf") == "utf-8-sig"
	assert xml_codec._detectencoding(b"\xff") is None
	assert xml_codec._detectencoding(b"\xff\x33") == "utf-8"
	assert xml_codec._detectencoding(b"\xff\xfe") is None
	assert xml_codec._detectencoding(b"\xff\xfe\x33") == "utf-16"
	assert xml_codec._detectencoding(b"\xff\xfe\x00") is None
	assert xml_codec._detectencoding(b"\xff\xfe\x00\x33") == "utf-16"
	assert xml_codec._detectencoding(b"\xff\xfe\x00\x00") == "utf-32"
	assert xml_codec._detectencoding(b"\x00") is None
	assert xml_codec._detectencoding(b"\x00\x33") == "utf-8"
	assert xml_codec._detectencoding(b"\x00\x00") is None
	assert xml_codec._detectencoding(b"\x00\x00\x33") == "utf-8"
	assert xml_codec._detectencoding(b"\x00\x00\xfe") is None
	assert xml_codec._detectencoding(b"\x00\x00\x00\x33") == "utf-8"
	assert xml_codec._detectencoding(b"\x00\x00\x00<") == "utf-32-be"
	assert xml_codec._detectencoding(b"\x00\x00\xfe\xff") == "utf-32"
	assert xml_codec._detectencoding(b"<") is None
	assert xml_codec._detectencoding(b"<\x33") == "utf-8"
	assert xml_codec._detectencoding(b"<\x00") is None
	assert xml_codec._detectencoding(b"<\x00\x33") == "utf-8"
	assert xml_codec._detectencoding(b"<\x00\x00") is None
	assert xml_codec._detectencoding(b"<\x00\x00\x33") == "utf-8"
	assert xml_codec._detectencoding(b"<\x00\x00\x00") == "utf-32-le"
	assert xml_codec._detectencoding(b"\x4c") is None
	assert xml_codec._detectencoding(b"\x4c\x33") == "utf-8"
	assert xml_codec._detectencoding(b"\x4c\x6f") is None
	assert xml_codec._detectencoding(b"\x4c\x6f\x33") == "utf-8"
	assert xml_codec._detectencoding(b"\x4c\x6f\xa7") is None
	assert xml_codec._detectencoding(b"\x4c\x6f\xa7\x33") == "utf-8"
	assert xml_codec._detectencoding(b"\x4c\x6f\xa7\x94") == "cp037"
	assert xml_codec._detectencoding(b"<?") is None
	assert xml_codec._detectencoding(b"<?x") is None
	assert xml_codec._detectencoding(b"<?xm") is None
	assert xml_codec._detectencoding(b"<?xml") is None
	assert xml_codec._detectencoding(b"<?xml\r") is None
	assert xml_codec._detectencoding(b"<?xml\rversion='1.0'") is None
	assert xml_codec._detectencoding(b"<?xml\rversion='1.0' encoding='x") is None
	assert xml_codec._detectencoding(b"<?xml\rversion='1.0' encoding='x'") == "x"
	assert xml_codec._detectencoding(b'<?xml\rversion="1.0" encoding="x"') == "x"
	assert xml_codec._detectencoding(b'<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x"') == "x"
	assert xml_codec._detectencoding(b"<?xml\rversion='1.0' ?>") == "utf-8"
	assert xml_codec._detectencoding(b"<?xml\rversion='1.0' Encoding='x'") is None # encoding not recognized (might come later)
	assert xml_codec._detectencoding(b"<?xml\rVersion='1.0'") is None
	with pytest.raises(ValueError):
		xml_codec._detectencoding(b"<?xml\rversion='1.0' encoding=''") # empty encoding
	assert xml_codec._detectencoding(b"<", False) is None
	assert xml_codec._detectencoding(b"<", True) == "utf-8"
	assert xml_codec._detectencoding(b"<?", False) is None
	assert xml_codec._detectencoding(b"<?", True) == "utf-8"


def test_detectencoding_unicode():
	# Unicode version (only parses the header)
	assert xml_codec._detectencoding('<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x') is None
	assert xml_codec._detectencoding('<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x', True) == "utf-8"
	assert xml_codec._detectencoding('<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x"') == "x"


def test_fixencoding():
	s = '<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x'
	assert xml_codec._fixencoding(s, "utf-8") is None

	s = '<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x'
	assert xml_codec._fixencoding(s, "utf-8", True) == s

	s = '<?xml \r\n\t \r\n\t \r\n\tversion \r\n\t \r\n\t= \r\n\t \r\n\t"1.0" \r\n\t \r\n\t \r\n\tencoding \r\n\t \r\n\t= \r\n\t \r\n\t"x"?>'
	assert xml_codec._fixencoding(s, "utf-8") == s.replace('"x"', '"utf-8"')


def check_partial(decoder, input, *parts):
	assert len(input) == len(parts)
	for (c, part) in zip(input, parts):
		c = bytes([c])
		assert decoder.decode(c) == part


def test_partial():
	decoder = codecs.getincrementaldecoder("xml")()

	# UTF-16
	check_partial(decoder, "\ufeff".encode("utf-16-be"), "", "")
	decoder.reset()

	check_partial(decoder, "\ufeff".encode("utf-16-le"), "", "")
	decoder.reset()

	result = ("", "", "", "\u1234", "", "a")

	check_partial(decoder, "\u1234a".encode("utf-16"), *result)
	decoder.reset()

	# Fake utf-16 stored big endian
	check_partial(decoder, "\ufeff\u1234a".encode("utf-16-be"), *result)
	decoder.reset()

	# Fake utf-16 stored little endian
	check_partial(decoder, "\ufeff\u1234a".encode("utf-16-le"), *result)
	decoder.reset()

	# UTF-32
	result = ("", "", "", "", "", "", "", "\u1234", "", "", "", "a")
	check_partial(decoder, "\u1234a".encode("utf-32"), *result)
	decoder.reset()

	# Fake utf-32 stored big endian
	check_partial(decoder, "\ufeff\u1234a".encode("utf-32-be"), *result)
	decoder.reset()

	# Fake utf-32 stored little endian
	check_partial(decoder, "\ufeff\u1234a".encode("utf-32-le"), *result)
	decoder.reset()

	# UTF-8-Sig
	check_partial(decoder, "\u1234a".encode("utf-8-sig"), "", "", "", "", "", "\u1234", "a")
	decoder.reset()


def test_decoder():
	def checkauto(encoding, input="<?xml version='1.0' encoding='x'?>gürk\u20ac"):
		# Check stateless decoder
		d = codecs.getdecoder("xml")
		assert d(input.encode(encoding))[0] == input.replace("'x'", repr(encoding))

		# Check stateless decoder with specified encoding
		assert d(input.encode(encoding), encoding=encoding)[0] == input.replace("'x'", repr(encoding))

		# Check incremental decoder
		id = codecs.getincrementaldecoder("xml")()
		assert "".join(id.iterdecode(bytes([c]) for c in input.encode(encoding))) == input.replace("'x'", repr(encoding))

		# Check incremental decoder with specified encoding
		id = codecs.getincrementaldecoder("xml")(encoding)
		assert "".join(id.iterdecode(bytes([c]) for c in input.encode(encoding))) == input.replace("'x'", repr(encoding))

	id = codecs.getincrementaldecoder("xml")(encoding="ascii")
	assert id.decode(b"<?xml version='1.0' encoding='utf-16'?>") == "<?xml version='1.0' encoding='ascii'?>"

	# Autodetectable encodings
	checkauto("utf-8-sig")
	checkauto("utf-16")
	checkauto("utf-16-le")
	checkauto("utf-16-be")
	checkauto("utf-32")
	checkauto("utf-32-le")
	checkauto("utf-32-be")

	def checkdecl(encoding, input="<?xml version='1.0' encoding={encoding!r}?><gürk>\u20ac</gürk>"):
		# Check stateless decoder with encoding autodetection
		d = codecs.getdecoder("xml")
		input = input.format(encoding=encoding)
		assert d(input.encode(encoding))[0] == input

		# Check stateless decoder with specified encoding
		assert d(input.encode(encoding), encoding=encoding)[0] == input

		# Check incremental decoder with encoding autodetection
		id = codecs.getincrementaldecoder("xml")()
		assert "".join(id.iterdecode(bytes([c]) for c in input.encode(encoding))) == input

		# Check incremental decoder with specified encoding
		id = codecs.getincrementaldecoder("xml")(encoding)
		assert "".join(id.iterdecode(bytes([c]) for c in input.encode(encoding))) == input

	# Use correct declaration
	checkdecl("utf-8")
	checkdecl("iso-8859-1", "<?xml version='1.0' encoding={encoding!r}?><gürk/>")
	checkdecl("iso-8859-15")
	checkdecl("cp1252")

	# No recursion
	with pytest.raises(ValueError):
		b"<?xml version='1.0' encoding='xml'?><gurk/>".decode("xml")


def test_encoder():
	def check(encoding, input="<?xml version='1.0' encoding='x'?>gürk\u20ac"):
		# Check stateless encoder with encoding autodetection
		e = codecs.getencoder("xml")
		inputdecl = input.replace("'x'", repr(encoding))
		assert e(inputdecl)[0].decode(encoding) == inputdecl

		# Check stateless encoder with specified encoding
		assert e(input, encoding=encoding)[0].decode(encoding) == inputdecl

		# Check incremental encoder with encoding autodetection
		ie = codecs.getincrementalencoder("xml")()
		assert b"".join(ie.iterencode(inputdecl)).decode(encoding) == inputdecl

		# Check incremental encoder with specified encoding
		ie = codecs.getincrementalencoder("xml")(encoding=encoding)
		assert b"".join(ie.iterencode(input)).decode(encoding) == inputdecl

	# Autodetectable encodings
	check("utf-8-sig")
	check("utf-16")
	check("utf-16-le")
	check("utf-16-be")
	check("utf-32")
	check("utf-32-le")
	check("utf-32-be")
	check("utf-8")
	check("iso-8859-1", "<?xml version='1.0' encoding='x'?><gürk/>")
	check("iso-8859-15")
	check("cp1252")

	# No recursion
	with pytest.raises(ValueError):
		"<?xml version='1.0' encoding='xml'?><gurk/>".encode("xml")
