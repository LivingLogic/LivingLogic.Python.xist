#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import re, datetime, StringIO

import py.test

from ll import ul4c, color


def check(result, source, **variables):
	# Check with template compiled from source
	t1 = ul4c.compile(source)
	s1 = unicode(t1)
	assert result == t1.renders(**variables)

	# Check with template loaded again via the string interface
	t2 = ul4c.loads(t1.dumps())
	s2 = unicode(t2)
	assert result == t2.renders(**variables)

	# Check with template loaded again via the stream interface
	stream = StringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = ul4c.load(stream)
	s3 = unicode(t3)
	assert result == t3.renders(**variables)
	assert s1 == s2 == s3


def checkle(result, source, **variables):
	# Check with template compiled from source
	t1 = ul4c.compile(source)
	s1 = unicode(t1)
	assert result <= t1.renders(**variables)

	# Check with template loaded again via the string interface
	t2 = ul4c.loads(t1.dumps())
	s2 = unicode(t2)
	assert result <= t2.renders(**variables)

	# Check with template loaded again via the stream interface
	stream = StringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = ul4c.load(stream)
	s3 = unicode(t3)
	assert result <= t3.renders(**variables)
	assert s1 == s2 == s3


def checkcompileerror(msg, source):
	try:
		ul4c.compile(source)
	except Exception, exc:
		assert re.search(msg, str(exc)) is not None
	else:
		py.test.fail("Didn't raise exception")


def checkrunerror(msg, source, **variables):
	# Check with template compiled from source
	t1 = ul4c.compile(source)
	s1 = unicode(t1)
	try:
		t1.renders(**variables)
	except Exception, exc:
		assert re.search(msg, "%s.%s: %s" % (exc.__class__.__module__, exc.__class__.__name__, exc)) is not None
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the string interface
	t2 = ul4c.loads(t1.dumps())
	s2 = unicode(t2)
	try:
		t2.renders(**variables)
	except Exception, exc:
		assert re.search(msg, "%s.%s: %s" % (exc.__class__.__module__, exc.__class__.__name__, exc)) is not None
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the stream interface
	stream = StringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = ul4c.load(stream)
	s3 = unicode(t3)
	try:
		t3.renders(**variables)
	except Exception, exc:
		assert re.search(msg, "%s.%s: %s" % (exc.__class__.__module__, exc.__class__.__name__, exc)) is not None
	else:
		py.test.fail("Didn't raise exception")
	assert s1 == s2 == s3


def test_text():
	check(u'gurk', u'gurk')
	check(u'g\xfcrk', u'g\xfcrk')


def test_none():
	check('', u'<?print None?>')

	check('no', u'<?if None?>yes<?else?>no<?end if?>')


def test_false():
	check('False', u'<?print False?>')

	check('no', u'<?if False?>yes<?else?>no<?end if?>')


def test_true():
	check('True', u'<?print True?>')

	check('yes', u'<?if True?>yes<?else?>no<?end if?>')


def test_int():
	check('0', u'<?print 0?>')
	check('42', u'<?print 42?>')
	check('-42', u'<?print -42?>')
	check('255', u'<?print 0xff?>')
	check('255', u'<?print 0Xff?>')
	check('-255', u'<?print -0xff?>')
	check('-255', u'<?print -0Xff?>')
	check('63', u'<?print 0o77?>')
	check('63', u'<?print 0O77?>')
	check('-63', u'<?print -0o77?>')
	check('-63', u'<?print -0O77?>')
	check('7', u'<?print 0b111?>')
	check('7', u'<?print 0B111?>')
	check('-7', u'<?print -0b111?>')
	check('-7', u'<?print -0B111?>')

	check('no', u'<?if 0?>yes<?else?>no<?end if?>')
	check('yes', u'<?if 1?>yes<?else?>no<?end if?>')
	check('yes', u'<?if -1?>yes<?else?>no<?end if?>')


def test_float():
	check('0.0', u'<?print 0.?>')
	check('42.0', u'<?print 42.?>')
	check('-42.0', u'<?print -42.?>')
	check('1e+42', u'<?print 1E42?>')
	check('1e+42', u'<?print 1e42?>')
	check('-1e+42', u'<?print -1E42?>')
	check('-1e+42', u'<?print -1e42?>')

	check('no', u'<?if 0.?>yes<?else?>no<?end if?>')
	check('yes', u'<?if 1.?>yes<?else?>no<?end if?>')
	check('yes', u'<?if -1.?>yes<?else?>no<?end if?>')


def test_string():
	check('foo', u'<?print "foo"?>')
	check('\n', u'<?print "\\n"?>')
	check('\r', u'<?print "\\r"?>')
	check('\t', u'<?print "\\t"?>')
	check('\f', u'<?print "\\f"?>')
	check('\b', u'<?print "\\b"?>')
	check('\a', u'<?print "\\a"?>')
	check('\x1b', u'<?print "\\e"?>')
	check('"', u'<?print "\\""?>')
	check("'", u'<?print "\\\'"?>')
	check(u'\u20ac', u'<?print "\u20ac"?>')
	check(u'\xff', u'<?print "\\xff"?>')
	check(u'\u20ac', u'''<?print "\\u20ac"?>''')
	checkcompileerror("Unterminated string", u'<?print "?>')
	check("\\xxx", u'<?print "\\xxx"?>')
	check("a\nb", u'<?print "a\nb"?>')

	check('no', u'<?if ""?>yes<?else?>no<?end if?>')
	check('yes', u'<?if "foo"?>yes<?else?>no<?end if?>')


def test_date():
	check('2000-02-29T00:00:00', u'<?print 2000-02-29T.isoformat()?>')
	check('2000-02-29T12:34:00', u'<?print 2000-02-29T12:34.isoformat()?>')
	check('2000-02-29T12:34:56', u'<?print 2000-02-29T12:34:56.isoformat()?>')
	check('2000-02-29T12:34:56.987654', u'<?print 2000-02-29T12:34:56.987654.isoformat()?>')
	check('yes', u'<?if 2000-02-29T12:34:56.987654?>yes<?else?>no<?end if?>')


def test_color():
	check('255,255,255,255', u'<?code c = #fff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	check('255,255,255,255', u'<?code c = #ffffff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	check('18,52,86,255', u'<?code c = #123456?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	check('17,34,51,68', u'<?code c = #1234?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	check('18,52,86,120', u'<?code c = #12345678?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	check('yes', u'<?if #fff?>yes<?else?>no<?end if?>')


def test_list():
	check('', u'<?for item in []?><?print item?>;<?end for?>')
	check('1;', u'<?for item in [1]?><?print item?>;<?end for?>')
	check('1;', u'<?for item in [1,]?><?print item?>;<?end for?>')
	check('1;2;', u'<?for item in [1, 2]?><?print item?>;<?end for?>')
	check('1;2;', u'<?for item in [1, 2,]?><?print item?>;<?end for?>')
	check('no', u'<?if []?>yes<?else?>no<?end if?>')
	check('yes', u'<?if [1]?>yes<?else?>no<?end if?>')


def test_dict():
	check('', u'<?for (key, value) in {}.items()?><?print key?>:<?print value?>\n<?end for?>')
	check('1:2\n', u'<?for (key, value) in {1:2}.items()?><?print key?>:<?print value?>\n<?end for?>')
	check('1:2\n', u'<?for (key, value) in {1:2,}.items()?><?print key?>:<?print value?>\n<?end for?>')
	# With duplicate keys, later ones simply overwrite earlier ones
	check('1:3\n', u'<?for (key, value) in {1:2, 1: 3}.items()?><?print key?>:<?print value?>\n<?end for?>')
	# Test **
	check('1:2\n', u'<?for (key, value) in {**{1:2}}.items()?><?print key?>:<?print value?>\n<?end for?>')
	check('1:4\n', u'<?for (key, value) in {1:1, **{1:2}, 1:3, **{1:4}}.items()?><?print key?>:<?print value?>\n<?end for?>')
	check('no', u'<?if {}?>yes<?else?>no<?end if?>')
	check('yes', u'<?if {1:2}?>yes<?else?>no<?end if?>')


def test_code_storevar():
	check('42', u'<?code x = 42?><?print x?>')
	check('xyzzy', u'<?code x = "xyzzy"?><?print x?>')


def test_code_addvar():
	check('40', u'<?code x = 17?><?code x += 23?><?print x?>')
	check('xyzzy', u'<?code x = "xyz"?><?code x += "zy"?><?print x?>')


def test_code_subvar():
	check('-6', u'<?code x = 17?><?code x -= 23?><?print x?>')


def test_code_mulvar():
	check('391', u'<?code x = 17?><?code x *= 23?><?print x?>')
	check(17*'xyzzy', u'<?code x = 17?><?code x *= "xyzzy"?><?print x?>')
	check(17*'xyzzy', u'<?code x = "xyzzy"?><?code x *= 17?><?print x?>')


def test_code_floordivvar():
	check('2', u'<?code x = 5?><?code x //= 2?><?print x?>')
	check('-3', u'<?code x = -5?><?code x //= 2?><?print x?>')


def test_code_truedivvar():
	check('2.5', u'<?code x = 5?><?code x /= 2?><?print x?>')
	check('-2.5', u'<?code x = -5?><?code x /= 2?><?print x?>')


def test_code_modvar():
	check('4', u'<?code x = 1729?><?code x %= 23?><?print x?>')


def test_code_delvar():
	checkrunerror('KeyError', u'<?code x = 1729?><?code del x?><?print x?>')


def test_for_string():
	check('', u'<?for c in data?>(<?print c?>)<?end for?>', data="")
	check('(g)(u)(r)(k)', u'<?for c in data?>(<?print c?>)<?end for?>', data="gurk")


def test_for_list():
	check('', u'<?for c in data?>(<?print c?>)<?end for?>', data="")
	check('(g)(u)(r)(k)', u'<?for c in data?>(<?print c?>)<?end for?>', data=["g", "u", "r", "k"])


def test_for_dict():
	check('', u'<?for c in data?>(<?print c?>)<?end for?>', data={})
	check('(a)(b)(c)', u'<?for c in sorted(data)?>(<?print c?>)<?end for?>', data=dict(a=1, b=2, c=3))


def test_for_nested():
	check('[(1)(2)][(3)(4)]', u'<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>', data=[[1, 2], [3, 4]])


def test_for_unpacking():
	data = [
		("spam", "eggs", 17),
		("gurk", "hurz", 23),
		("hinz", "kunz", 42)
	]
	check('(spam)(gurk)(hinz)', u'<?for (a,) in data?>(<?print a?>)<?end for?>', data=data)
	check('(spam,eggs)(gurk,hurz)(hinz,kunz)', u'<?for (a, b) in data?>(<?print a?>,<?print b?>)<?end for?>', data=data)
	check('(spam,eggs,17)(gurk,hurz,23)(hinz,kunz,42)', u'<?for (a, b, c) in data?>(<?print a?>,<?print b?>,<?print c?>)<?end for?>', data=data)


def test_break():
	check('1, 2, ', u'<?for i in [1,2,3]?><?print i?>, <?if i==2?><?break?><?end if?><?end for?>')


def test_break_nested():
	check('1, 1, 2, 1, 2, 3, ', u'<?for i in [1,2,3,4]?><?for j in [1,2,3,4]?><?print j?>, <?if j>=i?><?break?><?end if?><?end for?><?if i>=3?><?break?><?end if?><?end for?>')


def test_continue():
	check('1, 3, ', u'<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?print i?>, <?end for?>')


def test_continue_nested():
	check('1, 3, \n1, 3, \n', u'<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?for j in [1,2,3]?><?if j==2?><?continue?><?end if?><?print j?>, <?end for?>\n<?end for?>')


def test_if():
	check('42', u'<?if data?><?print data?><?end if?>', data=42)


def test_else():
	check('42', u'<?if data?><?print data?><?else?>no<?end if?>', data=42)
	check('no', u'<?if data?><?print data?><?else?>no<?end if?>', data=0)


def test_block_errors():
	checkcompileerror("in u?.<.for x in data.>..*block unclosed", u'<?for x in data?>')
	checkcompileerror("endif doesn't match any if", u'<?for x in data?><?end if?>')
	checkcompileerror("not in any block", u'<?end?>')
	checkcompileerror("not in any block", u'<?end for?>')
	checkcompileerror("not in any block", u'<?end if?>')
	checkcompileerror("else doesn't match any if", u'<?else?>')
	checkcompileerror("in u?.<.if data.>..*block unclosed", u'<?if data?>')
	checkcompileerror("in u?.<.if data.>..*block unclosed", u'<?if data?><?else?>')
	checkcompileerror("duplicate else", u'<?if data?><?else?><?else?>')
	checkcompileerror("else already seen in elif", u'<?if data?><?else?><?elif data?>')
	checkcompileerror("else already seen in elif", u'<?if data?><?elif data?><?elif data?><?else?><?elif data?>')


def test_empty():
	checkcompileerror("expression required", u'<?print?>')
	checkcompileerror("expression required", u'<?if?>')
	checkcompileerror("expression required", u'<<?if x?><?elif?><?end if?>')
	checkcompileerror("loop expression required", u'<?for?>')
	checkcompileerror("statement required", u'<?code?>')
	checkcompileerror("render statement required", u'<?render?>')


def test_add():
	check('42', u'<?print 21+21?>')
	check('42', u'<?code x=21?><?code y=21?><?print x+y?>')
	check('foobar', u'<?code x="foo"?><?code y="bar"?><?print x+y?>')
	check('(f)(o)(o)(b)(a)(r)', u'<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>', data=dict(foo="foo", bar="bar"))


def test_sub():
	check('0', u'<?print 21-21?>')
	check('0', u'<?code x=21?><?code y=21?><?print x-y?>')



def test_mul():
	check(str(17*23), u'<?print 17*23?>')
	check(str(17*23), u'<?code x=17?><?code y=23?><?print x*y?>')
	check(17*"foo", u'<?print 17*"foo"?>')
	check(17*"foo", u'<?code x=17?><?code y="foo"?><?print x*y?>')
	check("foo"*17, u'<?code x="foo"?><?code y=17?><?print x*y?>')
	check("foo"*17, u'<?print "foo"*17?>')
	check("(foo)(bar)(foo)(bar)(foo)(bar)", u'<?for i in 3*data?>(<?print i?>)<?end for?>', data=["foo", "bar"])


def test_truediv():
	check("0.5", u'<?print 1/2?>')
	check("0.5", u'<?code x=1?><?code y=2?><?print x/y?>')


def test_floordiv():
	check("0", u'<?print 1//2?>')
	check("0", u'<?code x=1?><?code y=2?><?print x//y?>')


def test_mod():
	check(str(42%17), u'<?print 42%17?>')
	check(str(42%17), u'<?code x=42?><?code y=17?><?print x%y?>')


def test_eq():
	check("False", u'<?print 17==23?>')
	check("True", u'<?print 17==17?>')
	check("False", u'<?print x==23?>', x=17)
	check("True", u'<?print x==23?>', x=23)


def test_ne():
	check("True", u'<?print 17!=23?>')
	check("False", u'<?print 17!=17?>')
	check("True", u'<?print x!=23?>', x=17)
	check("False", u'<?print x!=23?>', x=23)


def test_lt():
	check("True", u'<?print 1<2?>')
	check("False", u'<?print 2<2?>')
	check("False", u'<?print 3<2?>')
	check("True", u'<?print x<2?>', x=1)
	check("False", u'<?print x<2?>', x=2)
	check("False", u'<?print x<2?>', x=3)


def test_le():
	check("True", u'<?print 1<=2?>')
	check("True", u'<?print 2<=2?>')
	check("False", u'<?print 3<=2?>')
	check("True", u'<?print x<=2?>', x=1)
	check("True", u'<?print x<=2?>', x=2)
	check("False", u'<?print x<=2?>', x=3)


def test_gt():
	check("False", u'<?print 1>2?>')
	check("False", u'<?print 2>2?>')
	check("True", u'<?print 3>2?>')
	check("False", u'<?print x>2?>', x=1)
	check("False", u'<?print x>2?>', x=2)
	check("True", u'<?print x>2?>', x=3)


def test_and():
	check("False", u'<?print x and y?>', x=False, y=False)
	check("False", u'<?print x and y?>', x=False, y=True)
	check("0", u'<?print x and y?>', x=0, y=True)


def test_or():
	check("False", u'<?print x or y?>', x=False, y=False)
	check("True", u'<?print x or y?>', x=False, y=True)
	check("42", u'<?print x or y?>', x=42, y=True)


def test_not():
	check("True", u'<?print not x?>', x=False)
	check("False", u'<?print not x?>', x=42)


def test_ge():
	check("False", u'<?print 1>=2?>')
	check("True", u'<?print 2>=2?>')
	check("True", u'<?print 3>=2?>')
	check("False", u'<?print x>=2?>', x=1)
	check("True", u'<?print x>=2?>', x=2)
	check("True", u'<?print x>=2?>', x=3)


def test_getitem():
	check("u", u"<?print 'gurk'[1]?>")
	check("u", u"<?print x[1]?>", x="gurk")
	check("u", u"<?print 'gurk'[-3]?>")
	check("u", u"<?print x[-3]?>", x="gurk")
	checkcompileerror("IndexError", u"<?print 'gurk'[4]?>")
	checkrunerror("IndexError", u"<?print x[4]?>", x="gurk")
	checkcompileerror("IndexError", u"<?print 'gurk'[-5]?>")
	checkrunerror("IndexError", u"<?print x[-5]?>", x="gurk")


def test_getslice12():
	check("ur", u"<?print 'gurk'[1:3]?>")
	check("ur", u"<?print x[1:3]?>", x="gurk")
	check("ur", u"<?print 'gurk'[-3:-1]?>")
	check("ur", u"<?print x[-3:-1]?>", x="gurk")
	check("", u"<?print 'gurk'[4:10]?>")
	check("", u"<?print x[4:10]?>", x="gurk")
	check("", u"<?print 'gurk'[-10:-5]?>")
	check("", u"<?print x[-10:-5]?>", x="gurk")


def test_getslice1():
	check("urk", u"<?print 'gurk'[1:]?>")
	check("urk", u"<?print x[1:]?>", x="gurk")
	check("urk", u"<?print 'gurk'[-3:]?>")
	check("urk", u"<?print x[-3:]?>", x="gurk")
	check("", u"<?print 'gurk'[4:]?>")
	check("", u"<?print x[4:]?>", x="gurk")
	check("gurk", u"<?print 'gurk'[-10:]?>")
	check("gurk", u"<?print x[-10:]?>", x="gurk")


def test_getslice2():
	check("gur", u"<?print 'gurk'[:3]?>")
	check("gur", u"<?print x[:3]?>", x="gurk")
	check("gur", u"<?print 'gurk'[:-1]?>")
	check("gur", u"<?print x[:-1]?>", x="gurk")
	check("gurk", u"<?print 'gurk'[:10]?>")
	check("gurk", u"<?print x[:10]?>", x="gurk")
	check("", u"<?print 'gurk'[:-5]?>")
	check("", u"<?print x[:-5]?>", x="gurk")


def test_nested():
	sc = u"4"
	sv = u"x"
	n = 4
	for i in xrange(8): # when using 10 compiling the variable will run out of registers
		sc = u"(%s)+(%s)" % (sc, sc)
		sv = u"(%s)+(%s)" % (sv, sv)
		n = n+n
	check(str(n), u'<?print %s?>' % sc)
	check(str(n), u'<?code x=4?><?print %s?>' % sv)


def test_precedence():
	check("14", u'<?print 2+3*4?>')
	check("20", u'<?print (2+3)*4?>')
	check("10", u'<?print -2+-3*-4?>')
	check("14", u'<?print --2+--3*--4?>')
	check("14", u'<?print (-(-2))+(-((-3)*-(-4)))?>')
	check("42", u'<?print 2*data.value?>', data=dict(value=21))
	check("42", u'<?print data.value[0]?>', data=dict(value=[42]))
	check("42", u'<?print data[0].value?>', data=[dict(value=42)])
	check("42", u'<?print data[0][0][0]?>', data=[[[42]]])
	check("42", u'<?print data.value.value[0]?>', data=dict(value=dict(value=[42])))
	check("42", u'<?print data.value.value[0].value.value[0]?>', data=dict(value=dict(value=[dict(value=dict(value=[42]))])))


def test_bracket():
	sc = u"4"
	sv = u"x"
	for i in xrange(10):
		sc = u"(%s)" % sc
		sv = u"(%s)" % sv

	check("4", u'<?print %s?>' % sc)
	check("4", u'<?code x=4?><?print %s?>' % sv)


def test_function_now():
	checkrunerror("function u?'now' unknown", u"<?print now(1)?>")
	checkrunerror("function u?'now' unknown", u"<?print now(1, 2)?>")
	now = unicode(datetime.datetime.now())
	checkle(now, u"<?print now()?>")


def test_function_vars():
	checkrunerror("function u?'vars' unknown", "<?print vars(1)?>")
	checkrunerror("function u?'vars' unknown", "<?print vars(1, 2)?>")
	check("yes", u"<?if 'spam' in vars()?>yes<?else?>no<?end if?>", spam="eggs")


def test_function_xmlescape():
	checkrunerror("function u?'xmlescape' unknown", u"<?print xmlescape()?>")
	checkrunerror("function u?'xmlescape' unknown", u"<?print xmlescape(1, 2)?>")
	check("&lt;&gt;&amp;&#39;&quot;gurk", u"<?print xmlescape(data)?>", data='<>&\'"gurk')


def test_function_csv():
	checkrunerror("function u?'csv' unknown", u"<?print csv()?>")
	checkrunerror("function u?'csv' unknown", u"<?print csv(1, 2)?>")
	check("", u"<?print csv(data)?>", data=None)
	check("False", u"<?print csv(data)?>", data=False)
	check("True", u"<?print csv(data)?>", data=True)
	check("42", u"<?print csv(data)?>", data=42)
	# no check for float
	check("abc", u"<?print csv(data)?>", data="abc")
	check('"a,b,c"', u"<?print csv(data)?>", data="a,b,c")
	check('"a""b""c"', u"<?print csv(data)?>", data='a"b"c')
	check('"a\nb\nc"', u"<?print csv(data)?>", data="a\nb\nc")


def test_function_json():
	checkrunerror("function u?'json' unknown", u"<?print json()?>")
	checkrunerror("function u?'json' unknown", u"<?print json(1, 2)?>")
	check("null", u"<?print json(data)?>", data=None)
	check("false", u"<?print json(data)?>", data=False)
	check("true", u"<?print json(data)?>", data=True)
	check("42", u"<?print json(data)?>", data=42)
	# no check for float
	check('"abc"', u"<?print json(data)?>", data="abc")
	check('[1, 2, 3]', u"<?print json(data)?>", data=[1, 2, 3])
	check('{"one": 1}', u"<?print json(data)?>", data={"one": 1})


def test_function_str():
	checkrunerror("function u?'str' unknown", u"<?print str()?>")
	checkrunerror("function u?'str' unknown", u"<?print str(1, 2)?>")
	check("", u"<?print str(data)?>", data=None)
	check("True", u"<?print str(data)?>", data=True)
	check("False", u"<?print str(data)?>", data=False)
	check("42", u"<?print str(data)?>", data=42)
	check("4.2", u"<?print str(data)?>", data=4.2)
	check("foo", u"<?print str(data)?>", data="foo")


def test_function_int():
	checkrunerror("function u?'int' unknown", u"<?print int()?>")
	checkrunerror("function u?'int' unknown", u"<?print int(1, 2, 3)?>")
	checkrunerror("int\\(\\) argument must be a string or a number, not 'NoneType'", u"<?print int(data)?>", data=None)
	check("1", u"<?print int(data)?>", data=True)
	check("0", u"<?print int(data)?>", data=False)
	check("42", u"<?print int(data)?>", data=42)
	check("4", u"<?print int(data)?>", data=4.2)
	check("42", u"<?print int(data)?>", data="42")
	check("66", u"<?print int(data, 16)?>", data="42")
	checkrunerror("invalid literal for int\\(\\) with base 10: 'foo'", u"<?print int(data)?>", data="foo")


def test_function_float():
	checkrunerror("function u?'float' unknown", u"<?print float()?>")
	checkrunerror("function u?'float' unknown", u"<?print float(1, 2, 3)?>")
	checkrunerror("float\\(\\) argument must be a string or a number", u"<?print float(data)?>", data=None)
	check("1.0", u"<?print float(data)?>", data=True)
	check("0.0", u"<?print float(data)?>", data=False)
	check("42.0", u"<?print float(data)?>", data=42)
	check("4.2", u"<?print float(data)?>", data=4.2)
	check("42.0", u"<?print float(data)?>", data="42")


def test_function_len():
	checkrunerror("function u?'len' unknown", u"<?print len()?>")
	checkrunerror("function u?'len' unknown", u"<?print len(1, 2)?>")
	checkrunerror("object of type 'NoneType' has no len", u"<?print len(data)?>", data=None)
	checkrunerror("object of type 'bool' has no len", u"<?print len(data)?>", data=True)
	checkrunerror("object of type 'bool' has no len", u"<?print len(data)?>", data=False)
	checkrunerror("object of type 'int' has no len", u"<?print len(data)?>", data=42)
	checkrunerror("object of type 'float' has no len", u"<?print len(data)?>", data=4.2)
	check("42", u"<?print len(data)?>", data=42*"?")
	check("42", u"<?print len(data)?>", data=42*[None])
	check("42", u"<?print len(data)?>", data=dict.fromkeys(xrange(42)))


def test_function_enumerate():
	checkrunerror("function u?'enumerate' unknown", u"<?print enumerate()?>")
	checkrunerror("function u?'enumerate' unknown", u"<?print enumerate(1, 2)?>")
	code = u"<?for (i, value) in enumerate(data)?><?print i?>:<?print value?>\n<?end for?>"
	checkrunerror("'NoneType' object is not iterable", code, data=None)
	checkrunerror("'bool' object is not iterable", code, data=True)
	checkrunerror("'bool' object is not iterable", code, data=False)
	checkrunerror("'int' object is not iterable", code, data=42)
	checkrunerror("'float' object is not iterable", code, data=4.2)
	check("0:f\n1:o\n2:o\n", code, data="foo")
	check("0:foo\n1:bar\n", code, data=["foo", "bar"])
	check("0:foo\n", code, data=dict(foo=True))


def test_function_isnone():
	checkrunerror("function u?'isnone' unknown", u"<?print isnone()?>")
	checkrunerror("function u?'isnone' unknown", u"<?print isnone(1, 2)?>")
	code = u"<?print isnone(data)?>"
	check("True", code, data=None)
	check("False", code, data=True)
	check("False", code, data=False)
	check("False", code, data=42)
	check("False", code, data=4.2)
	check("False", code, data="foo")
	check("False", code, data=datetime.datetime.now())
	check("False", code, data=())
	check("False", code, data=[])
	check("False", code, data={})
	check("False", code, data=ul4c.compile(u""))
	check("False", code, data=color.red)


def test_function_isbool():
	checkrunerror("function u?'isbool' unknown", u"<?print isbool()?>")
	checkrunerror("function u?'isbool' unknown", u"<?print isbool(1, 2)?>")
	code = u"<?print isbool(data)?>"
	check("False", code, data=None)
	check("True", code, data=True)
	check("True", code, data=False)
	check("False", code, data=42)
	check("False", code, data=4.2)
	check("False", code, data="foo")
	check("False", code, data=datetime.datetime.now())
	check("False", code, data=())
	check("False", code, data=[])
	check("False", code, data={})
	check("False", code, data=ul4c.compile(u""))
	check("False", code, data=color.red)


def test_function_isint():
	checkrunerror("function u?'isint' unknown", u"<?print isint()?>")
	checkrunerror("function u?'isint' unknown", u"<?print isint(1, 2)?>")
	code = u"<?print isint(data)?>"
	check("False", code, data=None)
	check("False", code, data=True)
	check("False", code, data=False)
	check("True", code, data=42)
	check("False", code, data=4.2)
	check("False", code, data="foo")
	check("False", code, data=datetime.datetime.now())
	check("False", code, data=())
	check("False", code, data=[])
	check("False", code, data={})
	check("False", code, data=ul4c.compile(u""))
	check("False", code, data=color.red)


def test_function_isfloat():
	checkrunerror("function u?'isfloat' unknown", u"<?print isfloat()?>")
	checkrunerror("function u?'isfloat' unknown", u"<?print isfloat(1, 2)?>")
	code = u"<?print isfloat(data)?>"
	check("False", code, data=None)
	check("False", code, data=True)
	check("False", code, data=False)
	check("False", code, data=42)
	check("True", code, data=4.2)
	check("False", code, data="foo")
	check("False", code, data=datetime.datetime.now())
	check("False", code, data=())
	check("False", code, data=[])
	check("False", code, data={})
	check("False", code, data=ul4c.compile(u""))
	check("False", code, data=color.red)


def test_function_isstr():
	checkrunerror("function u?'isstr' unknown", u"<?print isstr()?>")
	checkrunerror("function u?'isstr' unknown", u"<?print isstr(1, 2)?>")
	code = u"<?print isstr(data)?>"
	check("False", code, data=None)
	check("False", code, data=True)
	check("False", code, data=False)
	check("False", code, data=42)
	check("False", code, data=4.2)
	check("True", code, data="foo")
	check("False", code, data=datetime.datetime.now())
	check("False", code, data=())
	check("False", code, data=[])
	check("False", code, data={})
	check("False", code, data=ul4c.compile(u""))
	check("False", code, data=color.red)


def test_function_isdate():
	checkrunerror("function u?'isdate' unknown", u"<?print isdate()?>")
	checkrunerror("function u?'isdate' unknown", u"<?print isdate(1, 2)?>")
	code = u"<?print isdate(data)?>"
	check("False", code, data=None)
	check("False", code, data=True)
	check("False", code, data=False)
	check("False", code, data=42)
	check("False", code, data=4.2)
	check("False", code, data="foo")
	check("True", code, data=datetime.datetime.now())
	check("False", code, data=())
	check("False", code, data=[])
	check("False", code, data={})
	check("False", code, data=ul4c.compile(u""))
	check("False", code, data=color.red)


def test_function_islist():
	checkrunerror("function u?'islist' unknown", u"<?print islist()?>")
	checkrunerror("function u?'islist' unknown", u"<?print islist(1, 2)?>")
	code = u"<?print islist(data)?>"
	check("False", code, data=None)
	check("False", code, data=True)
	check("False", code, data=False)
	check("False", code, data=42)
	check("False", code, data=4.2)
	check("False", code, data="foo")
	check("False", code, data=datetime.datetime.now())
	check("True", code, data=())
	check("True", code, data=[])
	check("False", code, data={})
	check("False", code, data=ul4c.compile(u""))
	check("False", code, data=color.red)


def test_function_isdict():
	checkrunerror("function u?'isdict' unknown", u"<?print isdict()?>")
	checkrunerror("function u?'isdict' unknown", u"<?print isdict(1, 2)?>")
	code = u"<?print isdict(data)?>"
	check("False", code, data=None)
	check("False", code, data=True)
	check("False", code, data=False)
	check("False", code, data=42)
	check("False", code, data=4.2)
	check("False", code, data="foo")
	check("False", code, data=datetime.datetime.now())
	check("False", code, data=())
	check("False", code, data=[])
	check("True", code, data={})
	check("False", code, data=ul4c.compile(u""))
	check("False", code, data=color.red)


def test_function_istemplate():
	checkrunerror("function u?'istemplate' unknown", u"<?print istemplate()?>")
	checkrunerror("function u?'istemplate' unknown", u"<?print istemplate(1, 2)?>")
	code = u"<?print istemplate(data)?>"
	check("False", code, data=None)
	check("False", code, data=True)
	check("False", code, data=False)
	check("False", code, data=42)
	check("False", code, data=4.2)
	check("False", code, data="foo")
	check("False", code, data=datetime.datetime.now())
	check("False", code, data=())
	check("False", code, data=[])
	check("False", code, data={})
	check("True", code, data=ul4c.compile(u""))
	check("False", code, data=color.red)


def test_function_iscolor():
	checkrunerror("function u?'iscolor' unknown", u"<?print iscolor()?>")
	checkrunerror("function u?'iscolor' unknown", u"<?print iscolor(1, 2)?>")
	code = u"<?print iscolor(data)?>"
	check("False", code, data=None)
	check("False", code, data=True)
	check("False", code, data=False)
	check("False", code, data=42)
	check("False", code, data=4.2)
	check("False", code, data="foo")
	check("False", code, data=datetime.datetime.now())
	check("False", code, data=())
	check("False", code, data=[])
	check("False", code, data={})
	check("False", code, data=ul4c.compile(u""))
	check("True", code, data=color.red)


def test_function_get():
	checkrunerror("function u?'get' unknown", u"<?print get()?>")
	check("", u"<?print get('x')?>")
	check("42", u"<?print get('x')?>", x=42)
	check("17", u"<?print get('x', 17)?>")
	check("42", u"<?print get('x', 17)?>", x=42)


def test_function_repr():
	checkrunerror("function u?'repr' unknown", u"<?print repr()?>")
	checkrunerror("function u?'repr' unknown", u"<?print repr(1, 2)?>")
	code = u"<?print repr(data)?>"
	check("None", code, data=None)
	check("True", code, data=True)
	check("False", code, data=False)
	check("42", code, data=42)
	# no test for float
	check("'foo'", code, data="foo")
	# no test for tuples, lists and dicts


def test_function_chr():
	checkrunerror("function u?'chr' unknown", u"<?print chr()?>")
	checkrunerror("function u?'chr' unknown", u"<?print chr(1, 2)?>")
	code = u"<?print chr(data)?>"
	check("\x00", code, data=0)
	check("a", code, data=ord("a"))
	check(u"\u20ac", code, data=0x20ac)


def test_function_ord():
	checkrunerror("function u?'ord' unknown", u"<?print ord()?>")
	checkrunerror("function u?'ord' unknown", u"<?print ord(1, 2)?>")
	code = u"<?print ord(data)?>"
	check("0", code, data="\x00")
	check(str(ord("a")), code, data="a")
	check(str(0x20ac), code, data=u"\u20ac")


def test_function_hex():
	checkrunerror("function u?'hex' unknown", u"<?print hex()?>")
	checkrunerror("function u?'hex' unknown", u"<?print hex(1, 2)?>")
	code = u"<?print hex(data)?>"
	check("0x0", code, data=0)
	check("0xff", code, data=0xff)
	check("0xffff", code, data=0xffff)
	check("-0xffff", code, data=-0xffff)


def test_function_oct():
	checkrunerror("function u?'oct' unknown", u"<?print oct()?>")
	checkrunerror("function u?'oct' unknown", u"<?print oct(1, 2)?>")
	code = u"<?print oct(data)?>"
	check("0o0", code, data=0)
	check("0o77", code, data=077)
	check("0o7777", code, data=07777)
	check("-0o7777", code, data=-07777)


def test_function_bin():
	checkrunerror("function u?'bin' unknown", u"<?print bin()?>")
	checkrunerror("function u?'bin' unknown", u"<?print bin(1, 2)?>")
	code = u"<?print bin(data)?>"
	check("0b0", code, data=0)
	check("0b11", code, data=3)
	check("-0b1111", code, data=-15)


def test_function_sorted():
	checkrunerror("function u?'sorted' unknown", u"<?print sorted()?>")
	checkrunerror("function u?'sorted' unknown", u"<?print sorted(1, 2)?>")
	code = u"<?for i in sorted(data)?><?print i?><?end for?>"
	check("gkru", code, data="gurk")
	check("24679", code, data="92746")
	check("012", code, data={0: "zero", 1: "one", 2: "two"})


def test_function_range():
	checkrunerror("function u?'sorted' unknown", u"<?print sorted()?>")
	code = u"<?for i in range(data)?><?print i?><?end for?>"
	check("", code, data=-10)
	check("", code, data=0)
	check("0", code, data=1)
	check("01234", code, data=5)
	code = u"<?for i in range(data[0], data[1])?><?print i?><?end for?>"
	check("", code, data=[0, -10])
	check("", code, data=[0, 0])
	check("01234", code, data=[0, 5])
	check("-5-4-3-2-101234", code, data=[-5, 5])
	code = u"<?for i in range(data[0], data[1], data[2])?><?print i?><?end for?>"
	check("", code, data=[0, -10, 1])
	check("", code, data=[0, 0, 1])
	check("02468", code, data=[0, 10, 2])
	check("", code, data=[0, 10, -2])
	check("108642", code, data=[10, 0, -2])
	check("", code, data=[10, 0, 2])


def test_function_zip():
	checkrunerror("function u?'zip' unknown", u"<?print zip()?>")
	checkrunerror("function u?'zip' unknown", u"<?print zip(1)?>")
	code = u"<?for (ix, iy) in zip(x, y)?><?print ix?>-<?print iy?>;<?end for?>"
	check("", code, x=[], y=[])
	check("1-3;2-4;", code, x=[1, 2], y=[3, 4])
	check("1-4;2-5;", code, x=[1, 2, 3], y=[4, 5])
	code = u"<?for (ix, iy, iz) in zip(x, y, z)?><?print ix?>-<?print iy?>+<?print iz?>;<?end for?>"
	check("", code, x=[], y=[], z=[])
	check("1-3+5;2-4+6;", code, x=[1, 2], y=[3, 4], z=[5, 6])
	check("1-4+6;", code, x=[1, 2, 3], y=[4, 5], z=[6])


def test_function_type():
	checkrunerror("function u?'type' unknown", u"<?print type()?>")
	checkrunerror("function u?'type' unknown", u"<?print type(1, 2)?>")
	code = u"<?print type(x)?>"
	check("none", code, x=None)
	check("bool", code, x=False)
	check("bool", code, x=True)
	check("int", code, x=42)
	check("int", code, x=42L)
	check("float", code, x=4.2)
	check("str", code, x="foo")
	check("str", code, x=u"foo")
	check("date", code, x=datetime.datetime.now())
	check("date", code, x=datetime.date.today())
	check("list", code, x=(1, 2))
	check("list", code, x=[1, 2])
	check("dict", code, x={1: 2})
	check("template", code, x=ul4c.compile(""))
	check("color", code, x=color.red)
	check("", code, x=1j)


def test_function_reversed():
	checkrunerror("function u?'reversed' unknown", u"<?print reversed()?>")
	checkrunerror("function u?'reversed' unknown", u"<?print reversed(1, 2)?>")
	code = u"<?for i in reversed(x)?>(<?print i?>)<?end for?>"
	check("(3)(2)(1)", code, x="123")
	check("(3)(2)(1)", code, x=[1, 2, 3])
	check("(3)(2)(1)", code, x=(1, 2, 3))


def test_method_upper():
	check("GURK", u"<?print 'gurk'.upper()?>")


def test_method_lower():
	check("gurk", u"<?print 'GURK'.lower()?>")


def test_method_capitalize():
	check("Gurk", u"<?print 'gURK'.capitalize()?>")


def test_method_startswith():
	check("True", u"<?print 'gurkhurz'.startswith('gurk')?>")
	check("False", u"<?print 'gurkhurz'.startswith('hurz')?>")


def test_method_endswith():
	check("True", u"<?print 'gurkhurz'.endswith('hurz')?>")
	check("False", u"<?print 'gurkhurz'.endswith('gurk')?>")


def test_method_strip():
	check("gurk", r"<?print ' \t\r\ngurk \t\r\n'.strip()?>")
	check("gurk", r"<?print 'xyzzygurkxyzzy'.strip('xyz')?>")


def test_method_lstrip():
	check("gurk \t\r\n", ur"<?print ' \t\r\ngurk \t\r\n'.lstrip()?>")
	check("gurkxyzzy", ur"<?print 'xyzzygurkxyzzy'.lstrip('xyz')?>")


def test_method_rstrip():
	check(" \t\r\ngurk", ur"<?print ' \t\r\ngurk \t\r\n'.rstrip()?>")
	check("xyzzygurk", ur"<?print 'xyzzygurkxyzzy'.rstrip('xyz')?>")


def test_method_split():
	check("(g)(u)(r)(k)", ur"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.split()?>(<?print item?>)<?end for?>")
	check("(g)(u \t\r\nr \t\r\nk \t\r\n)", ur"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.split(None, 1)?>(<?print item?>)<?end for?>")
	check("()(g)(u)(r)(k)()", ur"<?for item in 'xxgxxuxxrxxkxx'.split('xx')?>(<?print item?>)<?end for?>")
	check("()(g)(uxxrxxkxx)", ur"<?for item in 'xxgxxuxxrxxkxx'.split('xx', 2)?>(<?print item?>)<?end for?>")


def test_method_rsplit():
	check("(g)(u)(r)(k)", ur"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.rsplit()?>(<?print item?>)<?end for?>")
	check("( \t\r\ng \t\r\nu \t\r\nr)(k)", ur"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.rsplit(None, 1)?>(<?print item?>)<?end for?>")
	check("()(g)(u)(r)(k)()", ur"<?for item in 'xxgxxuxxrxxkxx'.rsplit('xx')?>(<?print item?>)<?end for?>")
	check("(xxgxxuxxr)(k)()", ur"<?for item in 'xxgxxuxxrxxkxx'.rsplit('xx', 2)?>(<?print item?>)<?end for?>")


def test_method_replace():
	check('goork', ur"<?print 'gurk'.replace('u', 'oo')?>")


def test_method_render():
	t = ul4c.compile(u'(<?print data?>)')
	check('(GURK)', u"<?print t.render(data='gurk').upper()?>", t=t)
	check('(GURK)', u"<?print t.render(**{'data': 'gurk'}).upper()?>", t=t)

	t = ul4c.compile(u'(gurk)')
	check('(GURK)', u"<?print t.render().upper()?>", t=t)


def test_method_format():
	now = datetime.datetime.now()
	format = "%Y-%m-%d %H:%M:%S"
	check(now.strftime(format), ur"<?print data.format('%s')?>" % format, data=now)
	check('987654', u'<?print 2000-02-29T12:34:56.987654.format("%f")?>')


def test_method_isoformat():
	now = datetime.datetime.now()
	check(now.isoformat(), ur"<?print data.isoformat()?>", data=now)


def test_method_get():
	check("42", u"<?print {}.get('foo', 42)?>")
	check("17", u"<?print {'foo': 17}.get('foo', 42)?>")
	check("", u"<?print {}.get('foo')?>")
	check("17", u"<?print {'foo': 17}.get('foo')?>")


def test_method_r_g_b_a():
	check('0x11', u'<?code c = #123?><?print hex(c.r())?>')
	check('0x22', u'<?code c = #123?><?print hex(c.g())?>')
	check('0x33', u'<?code c = #123?><?print hex(c.b())?>')
	check('0xff', u'<?code c = #123?><?print hex(c.a())?>')


def test_method_hls():
	check('0', u'<?code c = #fff?><?print int(c.hls()[0])?>')
	check('1', u'<?code c = #fff?><?print int(c.hls()[1])?>')
	check('0', u'<?code c = #fff?><?print int(c.hls()[2])?>')


def test_method_hlsa():
	check('0', u'<?code c = #fff?><?print int(c.hlsa()[0])?>')
	check('1', u'<?code c = #fff?><?print int(c.hlsa()[1])?>')
	check('0', u'<?code c = #fff?><?print int(c.hlsa()[2])?>')
	check('1', u'<?code c = #fff?><?print int(c.hlsa()[3])?>')


def test_method_hsv():
	check('0', u'<?code c = #fff?><?print int(c.hsv()[0])?>')
	check('0', u'<?code c = #fff?><?print int(c.hsv()[1])?>')
	check('1', u'<?code c = #fff?><?print int(c.hsv()[2])?>')


def test_method_hsva():
	check('0', u'<?code c = #fff?><?print int(c.hsva()[0])?>')
	check('0', u'<?code c = #fff?><?print int(c.hsva()[1])?>')
	check('1', u'<?code c = #fff?><?print int(c.hsva()[2])?>')
	check('1', u'<?code c = #fff?><?print int(c.hsva()[3])?>')


def test_method_lum():
	check('True', u'<?print #fff.lum() == 1?>')


def test_method_withlum():
	check('#fff', u'<?print #000.withlum(1)?>')


def test_method_witha():
	check('#0063a82a', u'<?print repr(#0063a8.witha(42))?>')


def test_method_join():
	check('1,2,3,4', u'<?print ",".join("1234")?>')
	check('1,2,3,4', u'<?print ",".join([1, 2, 3, 4])?>')


def test_render():
	t = ul4c.compile(u'<?print prefix?><?print data?><?print suffix?>')
	check('(f)(o)(o)', u'<?for c in data?><?render t(data=c, prefix="(", suffix=")")?><?end for?>', t=t, data='foo')
	check('(f)(o)(o)', u'<?for c in data?><?render t(data=c, **{"prefix": "(", "suffix": ")"})?><?end for?>', t=t, data='foo')


def test_render_var():
	t = ul4c.compile(u'<?code x += 1?><?print x?>')
	check('42,43,42', u'<?print x?>,<?render t(x=x)?>,<?print x?>', t=t, x=42)


def test_def():
	check('foo', u'<?def lower?><?print x.lower()?><?end def?><?print lower.render(x="FOO")?>')


def test_parse():
	check('42', u'<?print data.Noner?>', data=dict(Noner=42))


def test_nested_exceptions():
	tmpl1 = ul4c.compile(u"<?print 2*x?>")
	tmpl2 = ul4c.compile(u"<?render tmpl1(x=x)?>")
	tmpl3 = ul4c.compile(u"<?render tmpl2(tmpl1=tmpl1, x=x)?>")

	checkrunerror(r"TypeError .*render tmpl3.*render tmpl2.*render tmpl1.*print 2.*unsupported operand type", u"<?render tmpl3(tmpl1=tmpl1, tmpl2=tmpl2, x=x)?>", tmpl1=tmpl1, tmpl2=tmpl2, tmpl3=tmpl3, x=None)


def test_note():
	check("foo", u"f<?note This is?>o<?note a comment?>o")


def universaltemplate():
	return ul4c.compile("""
		text
		<?code x = 'gurk'?>
		<?code x = 42?>
		<?code x = 4.2?>
		<?code x = None?>
		<?code x = False?>
		<?code x = True?>
		<?code x = 2009-01-04T?>
		<?code x = #0063a8?>
		<?code x = [42]?>
		<?code x = {"fortytwo": 42}?>
		<?code x = {**{"fortytwo": 42}}?>
		<?code x = y?>
		<?code x += 42?>
		<?code x -= 42?>
		<?code x *= 42?>
		<?code x /= 42?>
		<?code x //= 42?>
		<?code x %= 42?>
		<?code del x?>
		<?print x.gurk?>
		<?print x["gurk"]?>
		<?print x[1:2]?>
		<?print x[1:]?>
		<?print x[:2]?>
		<?printx x?>
		<?for x in "12"?><?print x?><?break?><?continue?><?end for?>
		<?print not x?>
		<?print -x?>
		<?print x in y?>
		<?print x not in y?>
		<?print x==y?>
		<?print x!=y?>
		<?print x<y?>
		<?print x<=y?>
		<?print x>y?>
		<?print x>=y?>
		<?print x+y?>
		<?print x*y?>
		<?print x/y?>
		<?print x//y?>
		<?print x and y?>
		<?print x or y?>
		<?print x % y?>
		<?print now()?>
		<?print repr(1)?>
		<?print range(1, 2)?>
		<?print range(1, 2, 3)?>
		<?print rgb(1, 2, 3, 4)?>
		<?print x.r()?>
		<?print x.find(1)?>
		<?print x.find(1, 2)?>
		<?print x.find(1, 2, 3)?>
		<?if x?>gurk<?elif y?>hurz<?else?>hinz<?end if?>
		<?render x(a=1, b=2)?>
		<?def x?>foo<?end def?>
		<?render x()?>
	""")


def test_strtemplate():
	t = universaltemplate()
	str(t)


def test_pythonsource():
	t = universaltemplate()
	t.pythonsource()
	t.pythonsource("template")


def test_pythonfunction():
	t = universaltemplate()
	t.pythonfunction()
