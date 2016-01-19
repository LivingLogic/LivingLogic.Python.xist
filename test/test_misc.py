#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2005-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2005-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import sys, re

from ll import misc, ul4c

import pytest


# The following includes \x00 in addition to those characters defined in
# http://www.w3.org/TR/2004/REC-xml11-20040204/#NT-RestrictedChar
restrictedchars = re.compile("[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]")


escape_input = "".join(chr(i) for i in range(1000)) + "".join(chr(i) for i in range(sys.maxunicode-10, sys.maxunicode+1))


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
			if c=="&":
				escape_output.append("&amp;")
			elif c=="<":
				escape_output.append("&lt;")
			elif c==">":
				escape_output.append("&gt;")
			elif restrictedchars.match(c) is not None:
				escape_output.append("&#{};".format(ord(c)))
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
		yield from range(n)
		raise SyntaxError

	e = iter(range(10))
	assert misc.item(e, 0) == 0
	assert misc.item(e, 0) == 1
	assert misc.item(e, -1) == 9
	assert misc.item(e, -1) is None
	assert misc.item(e, -1, 42) == 42

	e = iter(range(10))
	assert misc.item(e, 4) == 4

	e = iter(range(10))
	assert misc.item(e, 10) is None

	e = iter(range(10))
	assert misc.item(e, 10, 42) == 42

	e = iter(range(10))
	assert misc.item(e, -1) == 9

	e = iter(range(10))
	assert misc.item(e, -10) == 0

	e = iter(range(10))
	assert misc.item(e, -11) is None

	e = iter(range(10))
	assert misc.item(e, -11, 42) == 42

	iterable = [17, 23, 37]

	# Wrong arguments
	with pytest.raises(TypeError):
		misc.item()
	with pytest.raises(TypeError):
		misc.item([])
	with pytest.raises(TypeError):
		misc.item(42, 42)

	# Non-negative index
	assert misc.item(iterable, 0) == 17
	assert misc.item(iterable, 2) == 37
	assert misc.item(iterable, 3) is None
	assert misc.item(iterable, 3, 42) == 42
	assert misc.item(err(10), 9) == 9
	with pytest.raises(SyntaxError):
		misc.item(err(10), 10)

	# Negative index
	assert misc.item(iterable, -1) == 37
	assert misc.item(iterable, -3) == 17
	assert misc.item(iterable, -4) is None
	assert misc.item(iterable, -4, 42) == 42
	# iterator is always exhausted
	with pytest.raises(SyntaxError):
		misc.item(err(10), -1)

	# Check index lists
	assert misc.item(["foo", "bar"], (1, -1)) == "r"


def test_first():
	e = iter(range(10))
	assert misc.first(e) == 0
	assert misc.first(e) == 1
	assert misc.first([]) is None
	assert misc.first([], 42) == 42


def test_last():
	e = iter(range(10))
	assert misc.last(e) == 9
	assert misc.last(e) is None
	assert misc.last([]) is None
	assert misc.last([], 42) == 42


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
	assert next(e) == 0
	assert next(e) == 1
	with pytest.raises(StopIteration):
		next(e)


def test_iterator_getitem():
	e = misc.Iterator(iter(range(10)))
	assert e[0] == 0
	assert e[0] == 1
	assert e[-1] == 9
	with pytest.raises(IndexError):
		e[-1]


def test_format_class():
	import http.client
	assert "ValueError" == misc.format_class(ValueError())
	assert "http.client.HTTPException" == misc.format_class(http.client.HTTPException())


def test_format_exception():
	assert "ValueError: bad value" == misc.format_exception(ValueError("  bad value  "))


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


def test_jsmin():
	assert misc.jsmin("gurk \t = \t 42;") == "gurk=42;"


def test_notimplemented():
	class Bad:
		@misc.notimplemented
		def bad(self):
			pass

	with pytest.raises(NotImplementedError):
		Bad().bad()


def test_javaexpr():
	# None
	assert "null" == misc.javaexpr(None)
	# bool
	assert "true" == misc.javaexpr(True)
	assert "false" == misc.javaexpr(False)
	# int
	assert "42" == misc.javaexpr(42)
	assert str((1<<31)-1) == misc.javaexpr((1<<31)-1)
	assert str(1<<31)+"L" == misc.javaexpr(1<<31)
	assert str(-(1<<31)) == misc.javaexpr(-(1<<31))
	assert str(-(1<<31)-1) + "L" == misc.javaexpr(-(1<<31)-1)
	assert str((1<<63)-1) + "L" == misc.javaexpr((1<<63)-1)
	assert 'new java.math.BigInteger("{}")'.format(1<<64) == misc.javaexpr(1<<64)
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
	assert '"\\u00ff"' == misc.javaexpr("\xff")
	assert '"\\u20ac"' == misc.javaexpr("\u20ac")
	# list
	assert "java.util.Arrays.asList()" == misc.javaexpr(())
	assert "java.util.Arrays.asList(1, 2, 3)" == misc.javaexpr([1, 2, 3])
	# dict
	assert "com.livinglogic.utils.MapUtils.makeMap()" == misc.javaexpr({})
	assert "com.livinglogic.utils.MapUtils.makeMap(1, 2)" == misc.javaexpr({1: 2})
	# undefined
	assert 'new com.livinglogic.ul4.UndefinedKey("foo")' == misc.javaexpr(ul4c.UndefinedKey("foo"))
	assert 'new com.livinglogic.ul4.UndefinedVariable("foo")' == misc.javaexpr(ul4c.UndefinedVariable("foo"))
	assert 'new com.livinglogic.ul4.UndefinedIndex(42)' == misc.javaexpr(ul4c.UndefinedIndex(42))


def test_sysinfo():
	# At least make sure that we don't produce exceptions by accessing each attribute once
	misc.sysinfo.host_name
	misc.sysinfo.host_fqdn
	misc.sysinfo.host_ip
	misc.sysinfo.host_sysname
	misc.sysinfo.host_nodename
	misc.sysinfo.host_release
	misc.sysinfo.host_version
	misc.sysinfo.host_machine
	misc.sysinfo.user_name
	misc.sysinfo.user_uid
	misc.sysinfo.user_gid
	misc.sysinfo.user_gecos
	misc.sysinfo.user_dir
	misc.sysinfo.user_shell
	misc.sysinfo.python_executable
	misc.sysinfo.python_version
	misc.sysinfo.pid
	misc.sysinfo.script_name
	misc.sysinfo.short_script_name


def test_prettycsv():
	assert "".join(misc.prettycsv([["a", "b", "c"], ["abc", "defg", "hijkl"]])) == "a     b      c\nabc   defg   hijkl\n"
	assert "".join(misc.prettycsv([["a", "b "], ["abc", "def"]])) == "a     b\nabc   def\n"
	assert "".join(misc.prettycsv([["a"], ["abc", "def"]])) == "a\nabc   def\n"
	assert "".join(misc.prettycsv([["a", "b"], ["abc", "def"]], "..")) == "a  ..b\nabc..def\n"


def test_timeout():
	with pytest.raises(misc.Timeout):
		with misc.timeout(3):
			while True:
				pass
