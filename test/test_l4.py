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
