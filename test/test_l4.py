#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 2008 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll import l4c

def check(source, data, result):
	t1 = l4c.Template.fromsrc(source)
	assert t1.renderstring(data) == result
	t2 = l4c.Template.frombin(t1.asbin())
	assert t2.renderstring(data) == result


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
	yield check, '<?if ""?>yes<?else?>no<?end if?>', {}, 'no'
	yield check, '<?if "foo"?>yes<?else?>no<?end if?>', {}, 'yes'
