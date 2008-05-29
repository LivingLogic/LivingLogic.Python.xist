#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 2008 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import re, cStringIO

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
	stream = cStringIO.StringIO()
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
		assert re.search(msg, str(exc)) is not None
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the string interface
	t2 = ullc.loads(t1.dumps())
	try:
		t2.renders(data, templates)
	except Exception, exc:
		assert re.search(msg, str(exc)) is not None
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the stream interface
	stream = cStringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = ullc.load(stream)
	try:
		t3.renders(data, templates)
	except Exception, exc:
		assert re.search(msg, str(exc)) is not None
	else:
		py.test.fail("Didn't raise exception")


def test_text():
	yield check, 'gurk', 'gurk'
	yield check, u'gurk', u'gurk'
	yield check, u'g\xfcrk', u'g\xfcrk'


def test_none():
	yield check, '', '<?print None?>'

	yield check, 'no', '<?if None?>yes<?else?>no<?end if?>'


def test_false():
	yield check, 'False', '<?print False?>'

	yield check, 'no', '<?if False?>yes<?else?>no<?end if?>'


def test_true():
	yield check, 'True', '<?print True?>'

	yield check, 'yes', '<?if True?>yes<?else?>no<?end if?>'


def test_int():
	yield check, '0', '<?print 0?>'
	yield check, '42', '<?print 42?>'
	yield check, '-42', '<?print -42?>'
	yield check, '255', '<?print 0xff?>'
	yield check, '255', '<?print 0Xff?>'
	yield check, '-255', '<?print -0xff?>'
	yield check, '-255', '<?print -0Xff?>'
	yield check, '63', '<?print 0o77?>'
	yield check, '63', '<?print 0O77?>'
	yield check, '-63', '<?print -0o77?>'
	yield check, '-63', '<?print -0O77?>'
	yield check, '7', '<?print 0b111?>'
	yield check, '7', '<?print 0B111?>'
	yield check, '-7', '<?print -0b111?>'
	yield check, '-7', '<?print -0B111?>'

	yield check, 'no', '<?if 0?>yes<?else?>no<?end if?>'
	yield check, 'yes', '<?if 1?>yes<?else?>no<?end if?>'
	yield check, 'yes', '<?if -1?>yes<?else?>no<?end if?>'


def test_float():
	yield check, '0.0', '<?print 0.?>'
	yield check, '42.0', '<?print 42.?>'
	yield check, '-42.0', '<?print -42.?>'
	yield check, '1e+42', '<?print 1E42?>'
	yield check, '1e+42', '<?print 1e42?>'
	yield check, '-1e+42', '<?print -1E42?>'
	yield check, '-1e+42', '<?print -1e42?>'

	yield check, 'no', '<?if 0.?>yes<?else?>no<?end if?>'
	yield check, 'yes', '<?if 1.?>yes<?else?>no<?end if?>'
	yield check, 'yes', '<?if -1.?>yes<?else?>no<?end if?>'


def test_string():
	yield check, 'foo', '<?print "foo"?>'
	yield check, '\n', '<?print "\\n"?>'
	yield check, '\r', '<?print "\\r"?>'
	yield check, '\t', '<?print "\\t"?>'
	yield check, '\f', '<?print "\\f"?>'
	yield check, '\b', '<?print "\\b"?>'
	yield check, '\a', '<?print "\\a"?>'
	yield check, '\x1b', '<?print "\\e"?>'
	yield check, '"', '<?print "\\""?>'
	yield check, "'", '<?print "\\\'"?>'
	yield check, u'\u20ac', u'<?print "\u20ac"?>'
	yield check, u'\xff', u'<?print "\\xff"?>'
	yield check, u'\u20ac', u'''<?print "\\u20ac"?>'''
	yield checkcompileerror, "Unterminated string", '<?print "?>'
	yield check, "\\xxx", '<?print "\\xxx"?>'
	yield check, "a\nb", '<?print "a\nb"?>'

	yield check, 'no', '<?if ""?>yes<?else?>no<?end if?>'
	yield check, 'yes', '<?if "foo"?>yes<?else?>no<?end if?>'


def test_code_storevar():
	yield check, '42', '<?code x = 42?><?print x?>'
	yield check, 'xyzzy', '<?code x = "xyzzy"?><?print x?>'


def test_code_addvar():
	yield check, '40', '<?code x = 17?><?code x += 23?><?print x?>'
	yield check, 'xyzzy', '<?code x = "xyz"?><?code x += "zy"?><?print x?>'


def test_code_subvar():
	yield check, '-6', '<?code x = 17?><?code x -= 23?><?print x?>'


def test_code_mulvar():
	yield check, '391', '<?code x = 17?><?code x *= 23?><?print x?>'
	yield check, 17*'xyzzy', '<?code x = 17?><?code x *= "xyzzy"?><?print x?>'
	yield check, 17*'xyzzy', '<?code x = "xyzzy"?><?code x *= 17?><?print x?>'


def test_code_floordivvar():
	yield check, '2', '<?code x = 5?><?code x //= 2?><?print x?>'
	yield check, '-3', '<?code x = -5?><?code x //= 2?><?print x?>'


def test_code_truedivvar():
	yield check, '2.5', '<?code x = 5?><?code x /= 2?><?print x?>'
	yield check, '-2.5', '<?code x = -5?><?code x /= 2?><?print x?>'


def test_code_modvar():
	yield check, '4', '<?code x = 1729?><?code x %= 23?><?print x?>'


def test_code_delvar():
	yield checkrunerror, 'KeyError', '<?code x = 1729?><?code del x?><?print x?>'


def test_for_string():
	yield check, '', '<?for c in data?>(<?print c?>)<?end for?>', ""
	yield check, '(g)(u)(r)(k)', '<?for c in data?>(<?print c?>)<?end for?>', "gurk"


def test_for_list():
	yield check, '', '<?for c in data?>(<?print c?>)<?end for?>', ""
	yield check, '(g)(u)(r)(k)', '<?for c in data?>(<?print c?>)<?end for?>', ["g", "u", "r", "k"]


def test_for_dict():
	yield check, '', '<?for c in data?>(<?print c?>)<?end for?>', {}
	yield check, '(a)(b)(c)', '<?for c in sorted(data)?>(<?print c?>)<?end for?>', dict(a=1, b=2, c=3)


def test_for_nested():
	yield check, '[(1)(2)][(3)(4)]', '<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>', [[1, 2], [3, 4]]


def test_if():
	yield check, '42', '<?if data?><?print data?><?end if?>', 42


def test_else():
	yield check, '42', '<?if data?><?print data?><?else?>no<?end if?>', 42
	yield check, 'no', '<?if data?><?print data?><?else?>no<?end if?>', 0


def test_block_errors():
	yield checkcompileerror, "unclosed blocks", '<?for x in data?>'
	yield checkcompileerror, "endif doesn't match any if", '<?for x in data?><?end if?>'
	yield checkcompileerror, "not in any block", '<?end?>'
	yield checkcompileerror, "not in any block", '<?end for?>'
	yield checkcompileerror, "not in any block", '<?end if?>'
	yield checkcompileerror, "else doesn't match any if", '<?else?>'
	yield checkcompileerror, "unclosed blocks", '<?if data?>'
	yield checkcompileerror, "unclosed blocks", '<?if data?><?else?>'
	yield checkcompileerror, "duplicate else", '<?if data?><?else?><?else?>'
	yield checkcompileerror, "else already seen in elif", '<?if data?><?else?><?elif data?>'
	yield checkcompileerror, "else already seen in elif", '<?if data?><?elif data?><?elif data?><?else?><?elif data?>'


def test_empty():
	yield checkcompileerror, "expression required", '<?print?>'
	yield checkcompileerror, "expression required", '<?if?>'
	yield checkcompileerror, "expression required", '<<?if x?><?elif?><?end if?>'
	yield checkcompileerror, "loop expression required", '<?for?>'
	yield checkcompileerror, "statement required", '<?code?>'
	yield checkcompileerror, "render statement required", '<?render?>'


def test_add():
	yield check, '42', '<?code x=21?><?code y=21?><?print x+y?>'
	yield check, 'foobar', '<?code x="foo"?><?code y="bar"?><?print x+y?>'
	yield check, '(f)(o)(o)(b)(a)(r)', '<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>', dict(foo="foo", bar="bar")


def test_sub():
	yield check, '0', '<?code x=21?><?code y=21?><?print x-y?>'



def test_mul():
	yield check, str(17*23), '<?code x=17?><?code y=23?><?print x*y?>'
	yield check, 17*"foo", '<?code x=17?><?code y="foo"?><?print x*y?>'
	yield check, "foo"*17, '<?code x="foo"?><?code y=17?><?print x*y?>'
	yield check, "(foo)(bar)(foo)(bar)(foo)(bar)", '<?for i in 3*data?>(<?print i?>)<?end for?>', ["foo", "bar"]


def test_truediv():
	yield check, "0.5", '<?code x=1?><?code y=2?><?print x/y?>'


def test_floordiv():
	yield check, "0", '<?code x=1?><?code y=2?><?print x//y?>'


def test_mod():
	yield check, str(42%17), '<?code x=42?><?code y=17?><?print x%y?>'


def test_mod():
	yield check, str(42%17), '<?code x=42?><?code y=17?><?print x%y?>'


def test_nested():
	sc = "4"
	sv = "x"
	n = 4
	for i in xrange(8): # when using 10 compiling the variable will run out of registers
		sc = "(%s)+(%s)" % (sc, sc)
		sv = "(%s)+(%s)" % (sv, sv)
		n = n+n
	yield check, str(n), '<?print %s?>' % sc
	yield check, str(n), '<?code x=4?><?print %s?>' % sv


def test_precedence():
	yield check, "14", '<?print 2+3*4?>'
	yield check, "20", '<?print (2+3)*4?>'
	yield check, "10", '<?print -2+-3*-4?>'
	yield check, "14", '<?print --2+--3*--4?>'
	yield check, "14", '<?print (-(-2))+(-((-3)*-(-4)))?>'
	yield check, "42", '<?print 2*data.value?>', dict(value=21)
	yield check, "42", '<?print data.value[0]?>', dict(value=[42])
	yield check, "42", '<?print data[0].value?>', [dict(value=42)]
	yield check, "42", '<?print data[0][0][0]?>', [[[42]]]
	yield check, "42", '<?print data.value.value[0]?>', dict(value=dict(value=[42]))
	yield check, "42", '<?print data.value.value[0].value.value[0]?>', dict(value=dict(value=[dict(value=dict(value=[42]))]))


def test_bracket():
	sc = "4"
	sv = "x"
	for i in xrange(10):
		sc = "(%s)" % sc
		sv = "(%s)" % sv

	yield check, "4", '<?print %s?>' % sc
	yield check, "4", '<?code x=4?><?print %s?>' % sv


def test_function_xmlescape():
	yield checkrunerror, "function u?'xmlescape' unknown", "<?print xmlescape()?>"
	yield checkrunerror, "function u?'xmlescape' unknown", "<?print xmlescape(1, 2)?>"
	yield check, "&lt;&gt;&amp;&#39;&quot;gurk", "<?print xmlescape(data)?>", '<>&\'"gurk'


def test_function_str():
	yield checkrunerror, "function u?'str' unknown", "<?print str()?>"
	yield checkrunerror, "function u?'str' unknown", "<?print str(1, 2)?>"
	yield check, "", "<?print str(data)?>", None
	yield check, "True", "<?print str(data)?>", True
	yield check, "False", "<?print str(data)?>", False
	yield check, "42", "<?print str(data)?>", 42
	yield check, "4.2", "<?print str(data)?>", 4.2
	yield check, "foo", "<?print str(data)?>", "foo"


def test_function_int():
	yield checkrunerror, "function u?'int' unknown", "<?print int()?>"
	yield checkrunerror, "function u?'int' unknown", "<?print int(1, 2)?>"
	yield checkrunerror, "int\\(\\) argument must be a string or a number, not 'NoneType'", "<?print int(data)?>", None
	yield check, "1", "<?print int(data)?>", True
	yield check, "0", "<?print int(data)?>", False
	yield check, "42", "<?print int(data)?>", 42
	yield check, "4", "<?print int(data)?>", 4.2
	yield check, "42", "<?print int(data)?>", "42"
	yield checkrunerror, "invalid literal for int\\(\\) with base 10: 'foo'", "<?print int(data)?>", "foo"


def test_function_len():
	yield checkrunerror, "function u?'len' unknown", "<?print len()?>"
	yield checkrunerror, "function u?'len' unknown", "<?print len(1, 2)?>"
	yield checkrunerror, "object of type 'NoneType' has no len", "<?print len(data)?>", None
	yield checkrunerror, "object of type 'bool' has no len", "<?print len(data)?>", True
	yield checkrunerror, "object of type 'bool' has no len", "<?print len(data)?>", False
	yield checkrunerror, "object of type 'int' has no len", "<?print len(data)?>", 42
	yield checkrunerror, "object of type 'float' has no len", "<?print len(data)?>", 4.2
	yield check, "42", "<?print len(data)?>", 42*"?"
	yield check, "42", "<?print len(data)?>", 42*[None]
	yield check, "42", "<?print len(data)?>", dict.fromkeys(xrange(42))


def test_function_enumerate():
	yield checkrunerror, "function u?'enumerate' unknown", "<?print enumerate()?>"
	yield checkrunerror, "function u?'enumerate' unknown", "<?print enumerate(1, 2)?>"
	code = "<?for (i, value) in enumerate(data)?><?print i?>:<?print value?>\n<?end for?>"
	yield checkrunerror, "'NoneType' object is not iterable", code, None
	yield checkrunerror, "'bool' object is not iterable", code, True
	yield checkrunerror, "'bool' object is not iterable", code, False
	yield checkrunerror, "'int' object is not iterable", code, 42
	yield checkrunerror, "'float' object is not iterable", code, 4.2
	yield check, "0:f\n1:o\n2:o\n", code, "foo"
	yield check, "0:foo\n1:bar\n", code, ["foo", "bar"]
	yield check, "0:foo\n", code, dict(foo=True)


def test_function_isnone():
	yield checkrunerror, "function u?'isnone' unknown", "<?print isnone()?>"
	yield checkrunerror, "function u?'isnone' unknown", "<?print isnone(1, 2)?>"
	code = "<?print isnone(data)?>"
	yield check, "True", code, None
	yield check, "False", code, True
	yield check, "False", code, False
	yield check, "False", code, 42
	yield check, "False", code, 4.2
	yield check, "False", code, "foo"
	yield check, "False", code, ()
	yield check, "False", code, []
	yield check, "False", code, {}


def test_function_isbool():
	yield checkrunerror, "function u?'isbool' unknown", "<?print isbool()?>"
	yield checkrunerror, "function u?'isbool' unknown", "<?print isbool(1, 2)?>"
	code = "<?print isbool(data)?>"
	yield check, "False", code, None
	yield check, "True", code, True
	yield check, "True", code, False
	yield check, "False", code, 42
	yield check, "False", code, 4.2
	yield check, "False", code, "foo"
	yield check, "False", code, ()
	yield check, "False", code, []
	yield check, "False", code, {}


def test_function_isint():
	yield checkrunerror, "function u?'isint' unknown", "<?print isint()?>"
	yield checkrunerror, "function u?'isint' unknown", "<?print isint(1, 2)?>"
	code = "<?print isint(data)?>"
	yield check, "False", code, None
	yield check, "False", code, True
	yield check, "False", code, False
	yield check, "True", code, 42
	yield check, "False", code, 4.2
	yield check, "False", code, "foo"
	yield check, "False", code, ()
	yield check, "False", code, []
	yield check, "False", code, {}


def test_function_isfloat():
	yield checkrunerror, "function u?'isfloat' unknown", "<?print isfloat()?>"
	yield checkrunerror, "function u?'isfloat' unknown", "<?print isfloat(1, 2)?>"
	code = "<?print isfloat(data)?>"
	yield check, "False", code, None
	yield check, "False", code, True
	yield check, "False", code, False
	yield check, "False", code, 42
	yield check, "True", code, 4.2
	yield check, "False", code, "foo"
	yield check, "False", code, ()
	yield check, "False", code, []
	yield check, "False", code, {}


def test_function_isstr():
	yield checkrunerror, "function u?'isstr' unknown", "<?print isstr()?>"
	yield checkrunerror, "function u?'isstr' unknown", "<?print isstr(1, 2)?>"
	code = "<?print isstr(data)?>"
	yield check, "False", code, None
	yield check, "False", code, True
	yield check, "False", code, False
	yield check, "False", code, 42
	yield check, "False", code, 4.2
	yield check, "True", code, "foo"
	yield check, "False", code, ()
	yield check, "False", code, []
	yield check, "False", code, {}


def test_function_islist():
	yield checkrunerror, "function u?'islist' unknown", "<?print islist()?>"
	yield checkrunerror, "function u?'islist' unknown", "<?print islist(1, 2)?>"
	code = "<?print islist(data)?>"
	yield check, "False", code, None
	yield check, "False", code, True
	yield check, "False", code, False
	yield check, "False", code, 42
	yield check, "False", code, 4.2
	yield check, "False", code, "foo"
	yield check, "True", code, ()
	yield check, "True", code, []
	yield check, "False", code, {}


def test_function_isdict():
	yield checkrunerror, "function u?'isdict' unknown", "<?print isdict()?>"
	yield checkrunerror, "function u?'isdict' unknown", "<?print isdict(1, 2)?>"
	code = "<?print isdict(data)?>"
	yield check, "False", code, None
	yield check, "False", code, True
	yield check, "False", code, False
	yield check, "False", code, 42
	yield check, "False", code, 4.2
	yield check, "False", code, "foo"
	yield check, "False", code, ()
	yield check, "False", code, []
	yield check, "True", code, {}


def test_function_repr():
	yield checkrunerror, "function u?'repr' unknown", "<?print repr()?>"
	yield checkrunerror, "function u?'repr' unknown", "<?print repr(1, 2)?>"
	code = "<?print repr(data)?>"
	yield check, "None", code, None
	yield check, "True", code, True
	yield check, "False", code, False
	yield check, "42", code, 42
	# no test for float
	yield check, "'foo'", code, "foo"
	# no test for tuples, lists and dicts


def test_function_chr():
	yield checkrunerror, "function u?'chr' unknown", "<?print chr()?>"
	yield checkrunerror, "function u?'chr' unknown", "<?print chr(1, 2)?>"
	code = "<?print chr(data)?>"
	yield check, "\x00", code, 0
	yield check, "a", code, ord("a")
	yield check, u"\u20ac", code, 0x20ac


def test_function_ord():
	yield checkrunerror, "function u?'ord' unknown", "<?print ord()?>"
	yield checkrunerror, "function u?'ord' unknown", "<?print ord(1, 2)?>"
	code = "<?print ord(data)?>"
	yield check, "0", code, "\x00"
	yield check, str(ord("a")), code, "a"
	yield check, str(0x20ac), code, u"\u20ac"


def test_function_hex():
	yield checkrunerror, "function u?'hex' unknown", "<?print hex()?>"
	yield checkrunerror, "function u?'hex' unknown", "<?print hex(1, 2)?>"
	code = "<?print hex(data)?>"
	yield check, "0x0", code, 0
	yield check, "0xff", code, 0xff
	yield check, "0xffff", code, 0xffff
	yield check, "-0xffff", code, -0xffff


def test_function_oct():
	yield checkrunerror, "function u?'oct' unknown", "<?print oct()?>"
	yield checkrunerror, "function u?'oct' unknown", "<?print oct(1, 2)?>"
	code = "<?print oct(data)?>"
	yield check, "0o0", code, 0
	yield check, "0o77", code, 077
	yield check, "0o7777", code, 07777
	yield check, "-0o7777", code, -07777


def test_function_bin():
	yield checkrunerror, "function u?'bin' unknown", "<?print bin()?>"
	yield checkrunerror, "function u?'bin' unknown", "<?print bin(1, 2)?>"
	code = "<?print bin(data)?>"
	yield check, "0b0", code, 0
	yield check, "0b11", code, 3
	yield check, "-0b1111", code, -15


def test_function_sorted():
	yield checkrunerror, "function u?'sorted' unknown", "<?print sorted()?>"
	yield checkrunerror, "function u?'sorted' unknown", "<?print sorted(1, 2)?>"
	code = "<?for i in sorted(data)?><?print i?><?end for?>"
	yield check, "gkru", code, "gurk"
	yield check, "24679", code, "92746"
	yield check, "012", code, {0: "zero", 1: "one", 2: "two"}


def test_function_range():
	yield checkrunerror, "function u?'sorted' unknown", "<?print sorted()?>"
	code = "<?for i in range(data)?><?print i?><?end for?>"
	yield check, "", code, -10
	yield check, "", code, 0
	yield check, "0", code, 1
	yield check, "01234", code, 5
	code = "<?for i in range(data[0], data[1])?><?print i?><?end for?>"
	yield check, "", code, [0, -10]
	yield check, "", code, [0, 0]
	yield check, "01234", code, [0, 5]
	yield check, "-5-4-3-2-101234", code, [-5, 5]
	code = "<?for i in range(data[0], data[1], data[2])?><?print i?><?end for?>"
	yield check, "", code, [0, -10, 1]
	yield check, "", code, [0, 0, 1]
	yield check, "02468", code, [0, 10, 2]
	yield check, "", code, [0, 10, -2]
	yield check, "108642", code, [10, 0, -2]
	yield check, "", code, [10, 0, 2]


def test_render():
	t = ullc.compile('(<?print data?>)')
	yield check, '(f)(o)(o)', '<?for i in data?><?render t(i)?><?end for?>', 'foo', dict(t=t)
