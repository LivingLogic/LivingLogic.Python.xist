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


def check(source, data, result):
	# Check with template compiled from source
	t1 = l4c.compile(source)
	assert t1.renders(data) == result

	# Check with template loaded again via the string interface
	t2 = l4c.loads(t1.dumps())
	assert t2.renders(data) == result

	# Check with template loaded again via the stream interface
	stream = cStringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = l4c.load(stream)
	assert t3.renders(data) == result


def checkcompileerror(source, data, msg):
	try:
		l4c.compile(source)
	except Exception, exc:
		assert msg in str(exc)
	else:
		py.test.fail("Didn't raise exception")


def checkrunerror(source, data, msg):
	# Check with template compiled from source
	t1 = l4c.compile(source)
	try:
		t1.renders(data)
	except Exception, exc:
		assert msg in str(exc)
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the string interface
	t2 = l4c.loads(t1.dumps())
	try:
		t2.renders(data)
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
		t3.renders(data)
	except Exception, exc:
		assert msg in str(exc)
	else:
		py.test.fail("Didn't raise exception")


def test_text():
	yield check, 'gurk', {}, 'gurk'
	yield check, u'gurk', {}, u'gurk'
	yield check, u'g\xfcrk', {}, u'g\xfcrk'


def test_none():
	yield check, '<?print None?>', {}, ''

	yield check, '<?if None?>yes<?else?>no<?end if?>', {}, 'no'


def test_false():
	yield check, '<?print False?>', {}, 'False'

	yield check, '<?if False?>yes<?else?>no<?end if?>', {}, 'no'


def test_true():
	yield check, '<?print True?>', {}, 'True'

	yield check, '<?if True?>yes<?else?>no<?end if?>', {}, 'yes'


def test_int():
	yield check, '<?print 0?>', {}, '0'
	yield check, '<?print 42?>', {}, '42'
	yield check, '<?print -42?>', {}, '-42'
	yield check, '<?print 0xff?>', {}, '255'
	yield check, '<?print 0Xff?>', {}, '255'
	yield check, '<?print -0xff?>', {}, '-255'
	yield check, '<?print -0Xff?>', {}, '-255'
	yield check, '<?print 0o77?>', {}, '63'
	yield check, '<?print 0O77?>', {}, '63'
	yield check, '<?print -0o77?>', {}, '-63'
	yield check, '<?print -0O77?>', {}, '-63'
	yield check, '<?print 0b111?>', {}, '7'
	yield check, '<?print 0B111?>', {}, '7'
	yield check, '<?print -0b111?>', {}, '-7'
	yield check, '<?print -0B111?>', {}, '-7'

	yield check, '<?if 0?>yes<?else?>no<?end if?>', {}, 'no'
	yield check, '<?if 1?>yes<?else?>no<?end if?>', {}, 'yes'
	yield check, '<?if -1?>yes<?else?>no<?end if?>', {}, 'yes'


def test_float():
	yield check, '<?print 0.?>', {}, '0.0'
	yield check, '<?print 42.?>', {}, '42.0'
	yield check, '<?print -42.?>', {}, '-42.0'
	yield check, '<?print 1E42?>', {}, '1e+42'
	yield check, '<?print 1e42?>', {}, '1e+42'
	yield check, '<?print -1E42?>', {}, '-1e+42'
	yield check, '<?print -1e42?>', {}, '-1e+42'

	yield check, '<?if 0.?>yes<?else?>no<?end if?>', {}, 'no'
	yield check, '<?if 1.?>yes<?else?>no<?end if?>', {}, 'yes'
	yield check, '<?if -1.?>yes<?else?>no<?end if?>', {}, 'yes'


def test_string():
	yield check, u'''<?print "foo"?>''', {}, u'foo'
	yield check, u'''<?print "\\n"?>''', {}, u'\n'
	yield check, u'''<?print "\\r"?>''', {}, u'\r'
	yield check, u'''<?print "\\t"?>''', {}, u'\t'
	yield check, u'''<?print "\\f"?>''', {}, u'\f'
	yield check, u'''<?print "\\b"?>''', {}, u'\b'
	yield check, u'''<?print "\\a"?>''', {}, u'\a'
	yield check, u'''<?print "\\e"?>''', {}, u'\x1b'
	yield check, u'''<?print "\\""?>''', {}, u'"'
	yield check, u'''<?print "\\'"?>''', {}, u"'"
	yield check, u'''<?print "\u20ac"?>''', {}, u'\u20ac'
	yield check, u'''<?print "\\xff"?>''', {}, u'\xff'
	yield check, u'''<?print "\\u20ac"?>''', {}, u'\u20ac'
	yield checkcompileerror, u'''<?print "?>''', {}, "Unterminated string"
	yield check, u'''<?print "\\xxx"?>''', {}, "\\xxx"
	yield check, u'''<?print "a\nb"?>''', {}, "a\nb"

	yield check, '<?if ""?>yes<?else?>no<?end if?>', {}, 'no'
	yield check, '<?if "foo"?>yes<?else?>no<?end if?>', {}, 'yes'


def test_code_storevar():
	yield check, u'''<?code x = 42?><?print x?>''', {}, u'42'
	yield check, u'''<?code x = "xyzzy"?><?print x?>''', {}, u'xyzzy'


def test_code_addvar():
	yield check, u'''<?code x = 17?><?code x += 23?><?print x?>''', {}, u'40'
	yield check, u'''<?code x = "xyz"?><?code x += "zy"?><?print x?>''', {}, u'xyzzy'


def test_code_subvar():
	yield check, u'''<?code x = 17?><?code x -= 23?><?print x?>''', {}, u'-6'


def test_code_mulvar():
	yield check, u'''<?code x = 17?><?code x *= 23?><?print x?>''', {}, u'391'
	yield check, u'''<?code x = 17?><?code x *= "xyzzy"?><?print x?>''', {}, 17*u'xyzzy'
	yield check, u'''<?code x = "xyzzy"?><?code x *= 17?><?print x?>''', {}, 17*u'xyzzy'


def test_code_floordivvar():
	yield check, u'''<?code x = 5?><?code x //= 2?><?print x?>''', {}, u'2'
	yield check, u'''<?code x = -5?><?code x //= 2?><?print x?>''', {}, u'-3'


def test_code_truedivvar():
	yield check, u'''<?code x = 5?><?code x /= 2?><?print x?>''', {}, u'2.5'
	yield check, u'''<?code x = -5?><?code x /= 2?><?print x?>''', {}, u'-2.5'


def test_code_modvar():
	yield check, u'''<?code x = 1729?><?code x %= 23?><?print x?>''', {}, u'4'


def test_code_delvar():
	yield checkrunerror, u'''<?code x = 1729?><?code del x?><?print x?>''', {}, u'KeyError'


def test_for_string():
	yield check, u'''<?for c in data?>(<?print c?>)<?end for?>''', "", u''
	yield check, u'''<?for c in data?>(<?print c?>)<?end for?>''', "gurk", u'(g)(u)(r)(k)'


def test_for_list():
	yield check, u'''<?for c in data?>(<?print c?>)<?end for?>''', "", u''
	yield check, u'''<?for c in data?>(<?print c?>)<?end for?>''', "gurk", u'(g)(u)(r)(k)'


def test_for_dict():
	yield check, u'''<?for c in data?>(<?print c?>)<?end for?>''', {}, u''
	yield check, u'''<?for c in sorted(data)?>(<?print c?>)<?end for?>''', dict(a=1, b=2, c=3), u'(a)(b)(c)'


def test_for_nested():
	yield check, u'''<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>''', [[1, 2, 3], [4, 5, 6], [7, 8, 9]], u'[(1)(2)(3)][(4)(5)(6)][(7)(8)(9)]'


def test_if():
	yield check, u'''<?if data?><?print data?><?end if?>''', 42, u'42'


def test_else():
	yield check, u'''<?if data?><?print data?><?else?>no<?end if?>''', 42, u'42'
	yield check, u'''<?if data?><?print data?><?else?>no<?end if?>''', 0, u'no'


def test_block_errors():
	yield checkcompileerror, u'''<?for x in data?>''', {}, "unclosed blocks"
	yield checkcompileerror, u'''<?for x in data?><?end if?>''', {}, "endif doesn't match any if"
	yield checkcompileerror, u'''<?end?>''', {}, "not in any block"
	yield checkcompileerror, u'''<?end for?>''', {}, "not in any block"
	yield checkcompileerror, u'''<?end if?>''', {}, "not in any block"
	yield checkcompileerror, u'''<?else?>''', {}, "else doesn't match any if"
	yield checkcompileerror, u'''<?if data?>''', {}, "unclosed blocks"
	yield checkcompileerror, u'''<?if data?><?else?>''', {}, "unclosed blocks"
	yield checkcompileerror, u'''<?if data?><?else?><?else?>''', {}, "duplicate else"
	yield checkcompileerror, u'''<?if data?><?else?><?elif data?>''', {}, "else already seen"
	yield checkcompileerror, u'''<?if data?><?elif data?><?elif data?><?else?><?elif data?>''', {}, "else already seen"


def test_empty():
	yield checkcompileerror, u'''<?print?>''', {}, "expression required"
	yield checkcompileerror, u'''<?if?>''', {}, "expression required"
	yield checkcompileerror, u'''<<?if x?><?elif?><?end if?>''', {}, "expression required"
	yield checkcompileerror, u'''<?for?>''', {}, "loop expression required"
	yield checkcompileerror, u'''<?code?>''', {}, "statement required"
