#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 2008 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import re, StringIO

import py.test

from ll import ullc


def check(result, source, data={}, templates={}):
	# Check with template compiled from source
	t1 = ullc.compile(source)
	assert t1.renders(data, templates) == result

	# Check with template loaded again via the string interface
	t2 = ullc.loads(t1.dumps())
	assert t2.renders(data, templates) == result

	# Check with template loaded again via the stream interface
	stream = StringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = ullc.load(stream)
	assert t3.renders(data, templates) == result


def checkcompileerror(msg, source):
	try:
		ullc.compile(source)
	except Exception, exc:
		assert re.search(msg, str(exc)) is not None
	else:
		py.test.fail("Didn't raise exception")


def checkrunerror(msg, source, data={}, templates={}):
	# Check with template compiled from source
	t1 = ullc.compile(source)
	try:
		t1.renders(data, templates)
	except Exception, exc:
		assert re.search(msg, "%s.%s: %s" % (exc.__class__.__module__, exc.__class__.__name__, exc)) is not None
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the string interface
	t2 = ullc.loads(t1.dumps())
	try:
		t2.renders(data, templates)
	except Exception, exc:
		assert re.search(msg, "%s.%s: %s" % (exc.__class__.__module__, exc.__class__.__name__, exc)) is not None
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the stream interface
	stream = StringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = ullc.load(stream)
	try:
		t3.renders(data, templates)
	except Exception, exc:
		assert re.search(msg, "%s.%s: %s" % (exc.__class__.__module__, exc.__class__.__name__, exc)) is not None
	else:
		py.test.fail("Didn't raise exception")


def test_text():
	check('gurk', 'gurk')
	check(u'gurk', u'gurk')
	check(u'g\xfcrk', u'g\xfcrk')


def test_none():
	check('', '<?print None?>')

	check('no', '<?if None?>yes<?else?>no<?end if?>')


def test_false():
	check('False', '<?print False?>')

	check('no', '<?if False?>yes<?else?>no<?end if?>')


def test_true():
	check('True', '<?print True?>')

	check('yes', '<?if True?>yes<?else?>no<?end if?>')


def test_int():
	check('0', '<?print 0?>')
	check('42', '<?print 42?>')
	check('-42', '<?print -42?>')
	check('255', '<?print 0xff?>')
	check('255', '<?print 0Xff?>')
	check('-255', '<?print -0xff?>')
	check('-255', '<?print -0Xff?>')
	check('63', '<?print 0o77?>')
	check('63', '<?print 0O77?>')
	check('-63', '<?print -0o77?>')
	check('-63', '<?print -0O77?>')
	check('7', '<?print 0b111?>')
	check('7', '<?print 0B111?>')
	check('-7', '<?print -0b111?>')
	check('-7', '<?print -0B111?>')

	check('no', '<?if 0?>yes<?else?>no<?end if?>')
	check('yes', '<?if 1?>yes<?else?>no<?end if?>')
	check('yes', '<?if -1?>yes<?else?>no<?end if?>')


def test_float():
	check('0.0', '<?print 0.?>')
	check('42.0', '<?print 42.?>')
	check('-42.0', '<?print -42.?>')
	check('1e+42', '<?print 1E42?>')
	check('1e+42', '<?print 1e42?>')
	check('-1e+42', '<?print -1E42?>')
	check('-1e+42', '<?print -1e42?>')

	check('no', '<?if 0.?>yes<?else?>no<?end if?>')
	check('yes', '<?if 1.?>yes<?else?>no<?end if?>')
	check('yes', '<?if -1.?>yes<?else?>no<?end if?>')


def test_string():
	check('foo', '<?print "foo"?>')
	check('\n', '<?print "\\n"?>')
	check('\r', '<?print "\\r"?>')
	check('\t', '<?print "\\t"?>')
	check('\f', '<?print "\\f"?>')
	check('\b', '<?print "\\b"?>')
	check('\a', '<?print "\\a"?>')
	check('\x1b', '<?print "\\e"?>')
	check('"', '<?print "\\""?>')
	check("'", '<?print "\\\'"?>')
	check(u'\u20ac', u'<?print "\u20ac"?>')
	check(u'\xff', u'<?print "\\xff"?>')
	check(u'\u20ac', u'''<?print "\\u20ac"?>''')
	checkcompileerror("Unterminated string", '<?print "?>')
	check("\\xxx", '<?print "\\xxx"?>')
	check("a\nb", '<?print "a\nb"?>')

	check('no', '<?if ""?>yes<?else?>no<?end if?>')
	check('yes', '<?if "foo"?>yes<?else?>no<?end if?>')


def test_code_storevar():
	check('42', '<?code x = 42?><?print x?>')
	check('xyzzy', '<?code x = "xyzzy"?><?print x?>')


def test_code_addvar():
	check('40', '<?code x = 17?><?code x += 23?><?print x?>')
	check('xyzzy', '<?code x = "xyz"?><?code x += "zy"?><?print x?>')


def test_code_subvar():
	check('-6', '<?code x = 17?><?code x -= 23?><?print x?>')


def test_code_mulvar():
	check('391', '<?code x = 17?><?code x *= 23?><?print x?>')
	check(17*'xyzzy', '<?code x = 17?><?code x *= "xyzzy"?><?print x?>')
	check(17*'xyzzy', '<?code x = "xyzzy"?><?code x *= 17?><?print x?>')


def test_code_floordivvar():
	check('2', '<?code x = 5?><?code x //= 2?><?print x?>')
	check('-3', '<?code x = -5?><?code x //= 2?><?print x?>')


def test_code_truedivvar():
	check('2.5', '<?code x = 5?><?code x /= 2?><?print x?>')
	check('-2.5', '<?code x = -5?><?code x /= 2?><?print x?>')


def test_code_modvar():
	check('4', '<?code x = 1729?><?code x %= 23?><?print x?>')


def test_code_delvar():
	checkrunerror('KeyError', '<?code x = 1729?><?code del x?><?print x?>')


def test_for_string():
	check('', '<?for c in data?>(<?print c?>)<?end for?>', "")
	check('(g)(u)(r)(k)', '<?for c in data?>(<?print c?>)<?end for?>', "gurk")


def test_for_list():
	check('', '<?for c in data?>(<?print c?>)<?end for?>', "")
	check('(g)(u)(r)(k)', '<?for c in data?>(<?print c?>)<?end for?>', ["g", "u", "r", "k"])


def test_for_dict():
	check('', '<?for c in data?>(<?print c?>)<?end for?>', {})
	check('(a)(b)(c)', '<?for c in sorted(data)?>(<?print c?>)<?end for?>', dict(a=1, b=2, c=3))


def test_for_nested():
	check('[(1)(2)][(3)(4)]', '<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>', [[1, 2], [3, 4]])


def test_if():
	check('42', '<?if data?><?print data?><?end if?>', 42)


def test_else():
	check('42', '<?if data?><?print data?><?else?>no<?end if?>', 42)
	check('no', '<?if data?><?print data?><?else?>no<?end if?>', 0)


def test_block_errors():
	checkcompileerror("unclosed blocks", '<?for x in data?>')
	checkcompileerror("endif doesn't match any if", '<?for x in data?><?end if?>')
	checkcompileerror("not in any block", '<?end?>')
	checkcompileerror("not in any block", '<?end for?>')
	checkcompileerror("not in any block", '<?end if?>')
	checkcompileerror("else doesn't match any if", '<?else?>')
	checkcompileerror("unclosed blocks", '<?if data?>')
	checkcompileerror("unclosed blocks", '<?if data?><?else?>')
	checkcompileerror("duplicate else", '<?if data?><?else?><?else?>')
	checkcompileerror("else already seen in elif", '<?if data?><?else?><?elif data?>')
	checkcompileerror("else already seen in elif", '<?if data?><?elif data?><?elif data?><?else?><?elif data?>')


def test_empty():
	checkcompileerror("expression required", '<?print?>')
	checkcompileerror("expression required", '<?if?>')
	checkcompileerror("expression required", '<<?if x?><?elif?><?end if?>')
	checkcompileerror("loop expression required", '<?for?>')
	checkcompileerror("statement required", '<?code?>')
	checkcompileerror("render statement required", '<?render?>')


def test_add():
	check('42', '<?code x=21?><?code y=21?><?print x+y?>')
	check('foobar', '<?code x="foo"?><?code y="bar"?><?print x+y?>')
	check('(f)(o)(o)(b)(a)(r)', '<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>', dict(foo="foo", bar="bar"))


def test_sub():
	check('0', '<?code x=21?><?code y=21?><?print x-y?>')



def test_mul():
	check(str(17*23), '<?code x=17?><?code y=23?><?print x*y?>')
	check(17*"foo", '<?code x=17?><?code y="foo"?><?print x*y?>')
	check("foo"*17, '<?code x="foo"?><?code y=17?><?print x*y?>')
	check("(foo)(bar)(foo)(bar)(foo)(bar)", '<?for i in 3*data?>(<?print i?>)<?end for?>', ["foo", "bar"])


def test_truediv():
	check("0.5", '<?code x=1?><?code y=2?><?print x/y?>')


def test_floordiv():
	check("0", '<?code x=1?><?code y=2?><?print x//y?>')


def test_mod():
	check(str(42%17), '<?code x=42?><?code y=17?><?print x%y?>')


def test_mod():
	check(str(42%17), '<?code x=42?><?code y=17?><?print x%y?>')


def test_nested():
	sc = "4"
	sv = "x"
	n = 4
	for i in xrange(8): # when using 10 compiling the variable will run out of registers
		sc = "(%s)+(%s)" % (sc, sc)
		sv = "(%s)+(%s)" % (sv, sv)
		n = n+n
	check(str(n), '<?print %s?>' % sc)
	check(str(n), '<?code x=4?><?print %s?>' % sv)


def test_precedence():
	check("14", '<?print 2+3*4?>')
	check("20", '<?print (2+3)*4?>')
	check("10", '<?print -2+-3*-4?>')
	check("14", '<?print --2+--3*--4?>')
	check("14", '<?print (-(-2))+(-((-3)*-(-4)))?>')
	check("42", '<?print 2*data.value?>', dict(value=21))
	check("42", '<?print data.value[0]?>', dict(value=[42]))
	check("42", '<?print data[0].value?>', [dict(value=42)])
	check("42", '<?print data[0][0][0]?>', [[[42]]])
	check("42", '<?print data.value.value[0]?>', dict(value=dict(value=[42])))
	check("42", '<?print data.value.value[0].value.value[0]?>', dict(value=dict(value=[dict(value=dict(value=[42]))])))


def test_bracket():
	sc = "4"
	sv = "x"
	for i in xrange(10):
		sc = "(%s)" % sc
		sv = "(%s)" % sv

	check("4", '<?print %s?>' % sc)
	check("4", '<?code x=4?><?print %s?>' % sv)


def test_function_xmlescape():
	checkrunerror("function u?'xmlescape' unknown", "<?print xmlescape()?>")
	checkrunerror("function u?'xmlescape' unknown", "<?print xmlescape(1, 2)?>")
	check("&lt;&gt;&amp;&#39;&quot;gurk", "<?print xmlescape(data)?>", '<>&\'"gurk')


def test_function_str():
	checkrunerror("function u?'str' unknown", "<?print str()?>")
	checkrunerror("function u?'str' unknown", "<?print str(1, 2)?>")
	check("", "<?print str(data)?>", None)
	check("True", "<?print str(data)?>", True)
	check("False", "<?print str(data)?>", False)
	check("42", "<?print str(data)?>", 42)
	check("4.2", "<?print str(data)?>", 4.2)
	check("foo", "<?print str(data)?>", "foo")


def test_function_int():
	checkrunerror("function u?'int' unknown", "<?print int()?>")
	checkrunerror("function u?'int' unknown", "<?print int(1, 2)?>")
	checkrunerror("int\\(\\) argument must be a string or a number, not 'NoneType'", "<?print int(data)?>", None)
	check("1", "<?print int(data)?>", True)
	check("0", "<?print int(data)?>", False)
	check("42", "<?print int(data)?>", 42)
	check("4", "<?print int(data)?>", 4.2)
	check("42", "<?print int(data)?>", "42")
	checkrunerror("invalid literal for int\\(\\) with base 10: 'foo'", "<?print int(data)?>", "foo")


def test_function_len():
	checkrunerror("function u?'len' unknown", "<?print len()?>")
	checkrunerror("function u?'len' unknown", "<?print len(1, 2)?>")
	checkrunerror("object of type 'NoneType' has no len", "<?print len(data)?>", None)
	checkrunerror("object of type 'bool' has no len", "<?print len(data)?>", True)
	checkrunerror("object of type 'bool' has no len", "<?print len(data)?>", False)
	checkrunerror("object of type 'int' has no len", "<?print len(data)?>", 42)
	checkrunerror("object of type 'float' has no len", "<?print len(data)?>", 4.2)
	check("42", "<?print len(data)?>", 42*"?")
	check("42", "<?print len(data)?>", 42*[None])
	check("42", "<?print len(data)?>", dict.fromkeys(xrange(42)))


def test_function_enumerate():
	checkrunerror("function u?'enumerate' unknown", "<?print enumerate()?>")
	checkrunerror("function u?'enumerate' unknown", "<?print enumerate(1, 2)?>")
	code = "<?for (i, value) in enumerate(data)?><?print i?>:<?print value?>\n<?end for?>"
	checkrunerror("'NoneType' object is not iterable", code, None)
	checkrunerror("'bool' object is not iterable", code, True)
	checkrunerror("'bool' object is not iterable", code, False)
	checkrunerror("'int' object is not iterable", code, 42)
	checkrunerror("'float' object is not iterable", code, 4.2)
	check("0:f\n1:o\n2:o\n", code, "foo")
	check("0:foo\n1:bar\n", code, ["foo", "bar"])
	check("0:foo\n", code, dict(foo=True))


def test_function_isnone():
	checkrunerror("function u?'isnone' unknown", "<?print isnone()?>")
	checkrunerror("function u?'isnone' unknown", "<?print isnone(1, 2)?>")
	code = "<?print isnone(data)?>"
	check("True", code, None)
	check("False", code, True)
	check("False", code, False)
	check("False", code, 42)
	check("False", code, 4.2)
	check("False", code, "foo")
	check("False", code, ())
	check("False", code, [])
	check("False", code, {})


def test_function_isbool():
	checkrunerror("function u?'isbool' unknown", "<?print isbool()?>")
	checkrunerror("function u?'isbool' unknown", "<?print isbool(1, 2)?>")
	code = "<?print isbool(data)?>"
	check("False", code, None)
	check("True", code, True)
	check("True", code, False)
	check("False", code, 42)
	check("False", code, 4.2)
	check("False", code, "foo")
	check("False", code, ())
	check("False", code, [])
	check("False", code, {})


def test_function_isint():
	checkrunerror("function u?'isint' unknown", "<?print isint()?>")
	checkrunerror("function u?'isint' unknown", "<?print isint(1, 2)?>")
	code = "<?print isint(data)?>"
	check("False", code, None)
	check("False", code, True)
	check("False", code, False)
	check("True", code, 42)
	check("False", code, 4.2)
	check("False", code, "foo")
	check("False", code, ())
	check("False", code, [])
	check("False", code, {})


def test_function_isfloat():
	checkrunerror("function u?'isfloat' unknown", "<?print isfloat()?>")
	checkrunerror("function u?'isfloat' unknown", "<?print isfloat(1, 2)?>")
	code = "<?print isfloat(data)?>"
	check("False", code, None)
	check("False", code, True)
	check("False", code, False)
	check("False", code, 42)
	check("True", code, 4.2)
	check("False", code, "foo")
	check("False", code, ())
	check("False", code, [])
	check("False", code, {})


def test_function_isstr():
	checkrunerror("function u?'isstr' unknown", "<?print isstr()?>")
	checkrunerror("function u?'isstr' unknown", "<?print isstr(1, 2)?>")
	code = "<?print isstr(data)?>"
	check("False", code, None)
	check("False", code, True)
	check("False", code, False)
	check("False", code, 42)
	check("False", code, 4.2)
	check("True", code, "foo")
	check("False", code, ())
	check("False", code, [])
	check("False", code, {})


def test_function_islist():
	checkrunerror("function u?'islist' unknown", "<?print islist()?>")
	checkrunerror("function u?'islist' unknown", "<?print islist(1, 2)?>")
	code = "<?print islist(data)?>"
	check("False", code, None)
	check("False", code, True)
	check("False", code, False)
	check("False", code, 42)
	check("False", code, 4.2)
	check("False", code, "foo")
	check("True", code, ())
	check("True", code, [])
	check("False", code, {})


def test_function_isdict():
	checkrunerror("function u?'isdict' unknown", "<?print isdict()?>")
	checkrunerror("function u?'isdict' unknown", "<?print isdict(1, 2)?>")
	code = "<?print isdict(data)?>"
	check("False", code, None)
	check("False", code, True)
	check("False", code, False)
	check("False", code, 42)
	check("False", code, 4.2)
	check("False", code, "foo")
	check("False", code, ())
	check("False", code, [])
	check("True", code, {})


def test_function_repr():
	checkrunerror("function u?'repr' unknown", "<?print repr()?>")
	checkrunerror("function u?'repr' unknown", "<?print repr(1, 2)?>")
	code = "<?print repr(data)?>"
	check("None", code, None)
	check("True", code, True)
	check("False", code, False)
	check("42", code, 42)
	# no test for float
	check("'foo'", code, "foo")
	# no test for tuples, lists and dicts


def test_function_chr():
	checkrunerror("function u?'chr' unknown", "<?print chr()?>")
	checkrunerror("function u?'chr' unknown", "<?print chr(1, 2)?>")
	code = "<?print chr(data)?>"
	check("\x00", code, 0)
	check("a", code, ord("a"))
	check(u"\u20ac", code, 0x20ac)


def test_function_ord():
	checkrunerror("function u?'ord' unknown", "<?print ord()?>")
	checkrunerror("function u?'ord' unknown", "<?print ord(1, 2)?>")
	code = "<?print ord(data)?>"
	check("0", code, "\x00")
	check(str(ord("a")), code, "a")
	check(str(0x20ac), code, u"\u20ac")


def test_function_hex():
	checkrunerror("function u?'hex' unknown", "<?print hex()?>")
	checkrunerror("function u?'hex' unknown", "<?print hex(1, 2)?>")
	code = "<?print hex(data)?>"
	check("0x0", code, 0)
	check("0xff", code, 0xff)
	check("0xffff", code, 0xffff)
	check("-0xffff", code, -0xffff)


def test_function_oct():
	checkrunerror("function u?'oct' unknown", "<?print oct()?>")
	checkrunerror("function u?'oct' unknown", "<?print oct(1, 2)?>")
	code = "<?print oct(data)?>"
	check("0o0", code, 0)
	check("0o77", code, 077)
	check("0o7777", code, 07777)
	check("-0o7777", code, -07777)


def test_function_bin():
	checkrunerror("function u?'bin' unknown", "<?print bin()?>")
	checkrunerror("function u?'bin' unknown", "<?print bin(1, 2)?>")
	code = "<?print bin(data)?>"
	check("0b0", code, 0)
	check("0b11", code, 3)
	check("-0b1111", code, -15)


def test_function_sorted():
	checkrunerror("function u?'sorted' unknown", "<?print sorted()?>")
	checkrunerror("function u?'sorted' unknown", "<?print sorted(1, 2)?>")
	code = "<?for i in sorted(data)?><?print i?><?end for?>"
	check("gkru", code, "gurk")
	check("24679", code, "92746")
	check("012", code, {0: "zero", 1: "one", 2: "two"})


def test_function_range():
	checkrunerror("function u?'sorted' unknown", "<?print sorted()?>")
	code = "<?for i in range(data)?><?print i?><?end for?>"
	check("", code, -10)
	check("", code, 0)
	check("0", code, 1)
	check("01234", code, 5)
	code = "<?for i in range(data[0], data[1])?><?print i?><?end for?>"
	check("", code, [0, -10])
	check("", code, [0, 0])
	check("01234", code, [0, 5])
	check("-5-4-3-2-101234", code, [-5, 5])
	code = "<?for i in range(data[0], data[1], data[2])?><?print i?><?end for?>"
	check("", code, [0, -10, 1])
	check("", code, [0, 0, 1])
	check("02468", code, [0, 10, 2])
	check("", code, [0, 10, -2])
	check("108642", code, [10, 0, -2])
	check("", code, [10, 0, 2])


def test_render():
	t = ullc.compile('(<?print data?>)')
	check('(f)(o)(o)', '<?for i in data?><?render t(i)?><?end for?>', 'foo', dict(t=t))


def test_parse():
	check('42', '<?print data.Noner?>', dict(Noner=42))
