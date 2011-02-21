#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2005-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, re

from ll import misc

import py.test


# The following includes \x00 in addition to those characters defined in
# http://www.w3.org/TR/2004/REC-xml11-20040204/#NT-RestrictedChar
restrictedchars = re.compile(u"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]")


escape_input = u"".join(unichr(i) for i in xrange(1000)) + u"".join(unichr(i) for i in xrange(sys.maxunicode-10, sys.maxunicode+1))


def test_xmlescape():
	for input in (escape_input, escape_input.encode("iso-8859-1", "ignore")):
		escape_output = []
		for c in escape_input:
			if c=="&":
				escape_output.append("&amp;")
			elif c=="<":
				escape_output.append("&lt;")
			elif c==">":
				escape_output.append("&gt;")
			elif c=='"':
				escape_output.append("&quot;")
			elif c=="'":
				escape_output.append("&#39;")
			elif restrictedchars.match(c) is not None:
				escape_output.append("&#{};".format(ord(c)))
			else:
				escape_output.append(c)
		escape_output = "".join(escape_output)
		assert misc.xmlescape(escape_input) == escape_output


def test_xmlescape_text():
	for input in (escape_input, escape_input.encode("iso-8859-1", "ignore")):
		escape_output = []
		for c in escape_input:
			if c==u"&":
				escape_output.append(u"&amp;")
			elif c==u"<":
				escape_output.append(u"&lt;")
			elif c==u">":
				escape_output.append(u"&gt;")
			elif restrictedchars.match(c) is not None:
				escape_output.append(u"&#{};".format(ord(c)))
			else:
				escape_output.append(c)
		escape_output = "".join(escape_output)
		assert misc.xmlescape_text(escape_input) == escape_output


def test_xmlescape_attr():
	for input in (escape_input, escape_input.encode("iso-8859-1", "ignore")):
		escape_output = []
		for c in escape_input:
			if c=="&":
				escape_output.append("&amp;")
			elif c=="<":
				escape_output.append("&lt;")
			elif c==">":
				escape_output.append("&gt;")
			elif c=='"':
				escape_output.append("&quot;")
			elif restrictedchars.match(c) is not None:
				escape_output.append("&#{};".format(ord(c)))
			else:
				escape_output.append(c)
		escape_output = "".join(escape_output)
		assert misc.xmlescape_attr(escape_input) == escape_output


def test_item():
	def err(n):
		for i in xrange(n):
			yield i
		raise SyntaxError

	e = iter(range(10))
	assert misc.item(e, 0) == 0
	assert misc.item(e, 0) == 1
	assert misc.item(e, -1) == 9
	with py.test.raises(IndexError):
		misc.item(e, -1)
	assert misc.item(e, -1, 42) == 42

	e = iter(range(10))
	assert misc.item(e, 4) == 4

	e = iter(range(10))
	with py.test.raises(IndexError):
		misc.item(e, 10)

	e = iter(range(10))
	assert misc.item(e, 10, 42) == 42

	e = iter(range(10))
	assert misc.item(e, -1) == 9

	e = iter(range(10))
	assert misc.item(e, -10) == 0

	e = iter(range(10))
	with py.test.raises(IndexError):
		misc.item(e, -11)

	e = iter(range(10))
	assert misc.item(e, -11, 42) == 42

	iterable = [17, 23, 37]

	# Wrong arguments
	with py.test.raises(TypeError):
		misc.item()
	with py.test.raises(TypeError):
		misc.item([])
	with py.test.raises(TypeError):
		misc.item(42, 42)

	# Non-negative index
	assert misc.item(iterable, 0), 17
	assert misc.item(iterable, 2), 37
	with py.test.raises(IndexError):
		misc.item(iterable, 3)
	assert misc.item(iterable, 3, 42), 42
	assert misc.item(err(10), 9), 9
	with py.test.raises(SyntaxError):
		misc.item(err(10), 10)

	# Negative index
	assert misc.item(iterable, -1), 37
	assert misc.item(iterable, -3), 17
	with py.test.raises(IndexError):
		misc.item(iterable, -4)
	assert misc.item(iterable, -4, 42), 42
	# iterator is always exhausted
	with py.test.raises(SyntaxError):
		misc.item(err(10), -1)


def test_first():
	e = iter(range(10))
	assert misc.first(e) == 0
	assert misc.first(e) == 1

	e = iter([])
	with py.test.raises(IndexError):
		misc.first(e)

	e = iter([])
	assert misc.first(e, 42) == 42


def test_last():
	e = iter(range(10))
	assert misc.last(e) == 9
	with py.test.raises(IndexError):
		misc.last(e)

	e = iter([])
	with py.test.raises(IndexError):
		misc.last(e)

	e = iter([])
	assert misc.last(e, 42) == 42


def test_count():
	e = iter(range(10))
	assert misc.count(e) == 10
	assert misc.count(e) == 0

	e = iter([])
	assert misc.count(e) == 0


def test_iterator_bool():
	e = misc.Iterator(iter(range(10)))
	assert e

	e = misc.Iterator(iter([]))
	assert not e


def test_iterator_next():
	e = misc.Iterator(iter(range(2)))
	assert e.next() == 0
	assert e.next() == 1
	with py.test.raises(StopIteration):
		e.next()


def test_iterator_getitem():
	e = misc.Iterator(iter(range(10)))
	assert e[0] == 0
	assert e[0] == 1
	assert e[-1] == 9
	with py.test.raises(IndexError):
		e[-1]


def test_pool():
	pool = misc.Pool(misc)
	assert pool.Pool is pool["Pool"] is misc.Pool


def test_module():
	m = misc.module("a = 42")
	assert m.a == 42
	assert m.__name__ == "unnamed"
	assert m.__file__ == "unnamed.py"

	m = misc.module("a = 42", "/Users/walter/test.py")
	assert m.a == 42
	assert m.__name__ == "test"
	assert m.__file__ == "/Users/walter/test.py"

	m = misc.module("a = 42", "/Users/walter/test.py", "pest")
	assert m.a == 42
	assert m.__name__ == "pest"
	assert m.__file__ == "/Users/walter/test.py"


def test_itersplitat():
	assert tuple(misc.itersplitat("20090609172345", (4, 6, 8, 10, 12))) == ("2009", "06", "09", "17", "23", "45")
	assert tuple(misc.itersplitat("200906091723", (4, 6, 8, 10, 12))) == ("2009", "06", "09", "17", "23")
	assert tuple(misc.itersplitat("20090609172345", (-10, -8, -6, -4, -2))) == ("2009", "06", "09", "17", "23", "45")


def test_gzip():
	assert misc.gunzip(misc.gzip("gurk", 0)) == "gurk"
	assert misc.gunzip(misc.gzip("gurk", 9)) == "gurk"


def test_jsmin():
	assert misc.jsmin("gurk \t = \t 42;") == "gurk=42;"


def test_notimplemented():
	class Bad(object):
		@misc.notimplemented
		def bad(self):
			pass

	with py.test.raises(NotImplementedError):
		Bad().bad()


def test_javaexpr():
	# None
	assert "null" == misc.javaexpr(None)
	# bool
	assert "true" == misc.javaexpr(True)
	assert "false" == misc.javaexpr(False)
	# int
	assert "42" == misc.javaexpr(42)
	assert str(1<<32) == misc.javaexpr(1<<32)
	assert 'new BigInteger("{}")'.format(1<<64) == misc.javaexpr(1<<64)
	# float
	assert "42.5" == misc.javaexpr(42.5)
	assert "1e+20" == misc.javaexpr(1e20)
	# string
	assert '""' == misc.javaexpr("")
	assert '"abc"' == misc.javaexpr("abc")
	assert '"\'"' == misc.javaexpr("'")
	assert '"\\n"' == misc.javaexpr("\n")
	assert '"\\r"' == misc.javaexpr("\r")
	assert '"\\t"' == misc.javaexpr("\t")
	assert '"\\f"' == misc.javaexpr("\f")
	assert '"\\b"' == misc.javaexpr("\b")
	assert '"\\""' == misc.javaexpr('"')
	assert '"\\u0000"' == misc.javaexpr("\x00")
	assert '"\\u00ff"' == misc.javaexpr(u"\xff")
	assert '"\\u20ac"' == misc.javaexpr(u"\u20ac")
	# list
	assert "java.util.Arrays.asList()" == misc.javaexpr(())
	assert "java.util.Arrays.asList(1, 2, 3)" == misc.javaexpr([1, 2, 3])
	# dict
	assert "com.livinglogic.ul4.Utils.makeMap()" == misc.javaexpr({})
	assert "com.livinglogic.ul4.Utils.makeMap(1, 2)" == misc.javaexpr({1: 2})


def test_prettycsv():
	assert "".join(misc.prettycsv([["a", "b", "c"], ["abc", "defg", "hijkl"]])) == "a     b      c\nabc   defg   hijkl\n"
	assert "".join(misc.prettycsv([["a", "b "], ["abc", "def"]])) == "a     b\nabc   def\n"
	assert "".join(misc.prettycsv([["a"], ["abc", "def"]])) == "a\nabc   def\n"
	assert "".join(misc.prettycsv([["a", "b"], ["abc", "def"]], "..")) == "a  ..b\nabc..def\n"
