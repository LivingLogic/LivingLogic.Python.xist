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


def test_print():
	yield check, u'<?print "foo"?>', {}, u'foo'
	yield check, u'<?print "\u20ac"?>', {}, u'\u20ac'
	yield check, u'<?print "\\xff"?>', {}, u'\xff'
	yield check, u'<?print "\\u20ac"?>', {}, u'\u20ac'
