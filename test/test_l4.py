#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 2008 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import cStringIO

import py.test

from ll import l4c


def check(result, source, data={}, templates={}):
	# Check with template compiled from source
	t1 = l4c.compile(source)
	assert t1.renders(data, templates) == result

	# Check with template loaded again via the string interface
	t2 = l4c.loads(t1.dumps())
	assert t2.renders(data, templates) == result

	# Check with template loaded again via the stream interface
	stream = cStringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = l4c.load(stream)
	assert t3.renders(data, templates) == result


def checkcompileerror(msg, source):
	try:
		l4c.compile(source)
	except Exception, exc:
		assert msg in str(exc)
	else:
		py.test.fail("Didn't raise exception")


def checkrunerror(msg, source, data={}, templates={}):
	# Check with template compiled from source
	t1 = l4c.compile(source)
	try:
		t1.renders(data, templates)
	except Exception, exc:
		assert msg in str(exc)
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the string interface
	t2 = l4c.loads(t1.dumps())
	try:
		t2.renders(data, templates)
	except Exception, exc:
		assert msg in str(exc)
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the stream interface
	stream = cStringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = l4c.load(stream)
	try:
		t3.renders(data, templates)
	except Exception, exc:
		assert msg in str(exc)
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
	yield checkcompileerror, "else already seen", '<?if data?><?else?><?elif data?>'
	yield checkcompileerror, "else already seen", '<?if data?><?elif data?><?elif data?><?else?><?elif data?>'


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


def test_nested():
	s = "4"
	n = 4
	for i in xrange(10):
		s = "(%s)+(%s)" % (s, s)
		n = n+n
	yield check, str(n), '<?print %s?>' % s


def test_render():
	t = l4c.compile('(<?print data?>)')
	yield check, '(f)(o)(o)', '<?for i in data?><?render t(i)?><?end for?>', 'foo', dict(t=t)
