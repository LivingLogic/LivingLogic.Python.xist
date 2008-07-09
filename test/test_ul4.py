#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 2008 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import re, datetime, StringIO

import py.test

from ll import ul4c


def check(result, source, templates={}, **variables):
	# Check with template compiled from source
	t1 = ul4c.compile(source)
	assert result == t1.renders(templates, **variables)

	# Check with template loaded again via the string interface
	t2 = ul4c.loads(t1.dumps())
	assert result == t2.renders(templates, **variables)

	# Check with template loaded again via the stream interface
	stream = StringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = ul4c.load(stream)
	assert result == t3.renders(templates, **variables)


def checkle(result, source, templates={}, **variables):
	# Check with template compiled from source
	t1 = ul4c.compile(source)
	assert result <= t1.renders(templates, **variables)

	# Check with template loaded again via the string interface
	t2 = ul4c.loads(t1.dumps())
	assert result <= t2.renders(templates, **variables)

	# Check with template loaded again via the stream interface
	stream = StringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = ul4c.load(stream)
	assert result <= t3.renders(templates, **variables)


def checkcompileerror(msg, source):
	try:
		ul4c.compile(source)
	except Exception, exc:
		assert re.search(msg, str(exc)) is not None
	else:
		py.test.fail("Didn't raise exception")


def checkrunerror(msg, source, templates={}, **variables):
	# Check with template compiled from source
	t1 = ul4c.compile(source)
	try:
		t1.renders(templates, **variables)
	except Exception, exc:
		assert re.search(msg, "%s.%s: %s" % (exc.__class__.__module__, exc.__class__.__name__, exc)) is not None
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the string interface
	t2 = ul4c.loads(t1.dumps())
	try:
		t2.renders(templates, **variables)
	except Exception, exc:
		assert re.search(msg, "%s.%s: %s" % (exc.__class__.__module__, exc.__class__.__name__, exc)) is not None
	else:
		py.test.fail("Didn't raise exception")

	# Check with template loaded again via the stream interface
	stream = StringIO.StringIO()
	t1.dump(stream)
	stream.seek(0)
	t3 = ul4c.load(stream)
	try:
		t3.renders(templates, **variables)
	except Exception, exc:
		assert re.search(msg, "%s.%s: %s" % (exc.__class__.__module__, exc.__class__.__name__, exc)) is not None
	else:
		py.test.fail("Didn't raise exception")


def test_format():
	tmpl = ul4c.compile("<?for (i, item) in enumerate(data)?><?print (i+1).format('>3d')?>. <?print item[0].format('.<10')?> <?print item[1]?>\n<?end for?>")
	assert str(tmpl) == unicode(tmpl)


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


def test_date():
	check('2000-02-29T00:00:00', '<?print 2000-02-29T.isoformat()?>')
	check('2000-02-29T12:34:00', '<?print 2000-02-29T12:34.isoformat()?>')
	check('2000-02-29T12:34:56', '<?print 2000-02-29T12:34:56.isoformat()?>')
	check('2000-02-29T12:34:56.987654', '<?print 2000-02-29T12:34:56.987654.isoformat()?>')
	check('yes', '<?if 2000-02-29T12:34:56.987654?>yes<?else?>no<?end if?>')


def test_list():
	check('', '<?for item in []?><?print item?>;<?end for?>')
	check('1;', '<?for item in [1]?><?print item?>;<?end for?>')
	check('1;', '<?for item in [1,]?><?print item?>;<?end for?>')
	check('1;2;', '<?for item in [1, 2]?><?print item?>;<?end for?>')
	check('1;2;', '<?for item in [1, 2,]?><?print item?>;<?end for?>')
	check('no', '<?if []?>yes<?else?>no<?end if?>')
	check('yes', '<?if [1]?>yes<?else?>no<?end if?>')


def test_dict():
	check('', '<?for (key, value) in {}.items()?><?print key?>:<?print value?>\n<?end for?>')
	check('1:2\n', '<?for (key, value) in {1:2}.items()?><?print key?>:<?print value?>\n<?end for?>')
	check('1:2\n', '<?for (key, value) in {1:2,}.items()?><?print key?>:<?print value?>\n<?end for?>')
	# With duplicate keys, later ones simply overwrite earlier ones
	check('1:3\n', '<?for (key, value) in {1:2, 1: 3}.items()?><?print key?>:<?print value?>\n<?end for?>')
	check('no', '<?if {}?>yes<?else?>no<?end if?>')
	check('yes', '<?if {1:2}?>yes<?else?>no<?end if?>')


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
	check('', '<?for c in data?>(<?print c?>)<?end for?>', data="")
	check('(g)(u)(r)(k)', '<?for c in data?>(<?print c?>)<?end for?>', data="gurk")


def test_for_list():
	check('', '<?for c in data?>(<?print c?>)<?end for?>', data="")
	check('(g)(u)(r)(k)', '<?for c in data?>(<?print c?>)<?end for?>', data=["g", "u", "r", "k"])


def test_for_dict():
	check('', '<?for c in data?>(<?print c?>)<?end for?>', data={})
	check('(a)(b)(c)', '<?for c in sorted(data)?>(<?print c?>)<?end for?>', data=dict(a=1, b=2, c=3))


def test_for_nested():
	check('[(1)(2)][(3)(4)]', '<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>', data=[[1, 2], [3, 4]])


def test_break():
	check('1, 2, ', '<?for i in [1,2,3]?><?print i?>, <?if i==2?><?break?><?end if?><?end for?>')


def test_break_nested():
	check('1, 1, 2, 1, 2, 3, ', '<?for i in [1,2,3,4]?><?for j in [1,2,3,4]?><?print j?>, <?if j>=i?><?break?><?end if?><?end for?><?if i>=3?><?break?><?end if?><?end for?>')


def test_continue():
	check('1, 3, ', '<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?print i?>, <?end for?>')


def test_continue_nested():
	check('1, 3, \n1, 3, \n', '<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?for j in [1,2,3]?><?if j==2?><?continue?><?end if?><?print j?>, <?end for?>\n<?end for?>')


def test_if():
	check('42', '<?if data?><?print data?><?end if?>', data=42)


def test_else():
	check('42', '<?if data?><?print data?><?else?>no<?end if?>', data=42)
	check('no', '<?if data?><?print data?><?else?>no<?end if?>', data=0)


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
	check('42', '<?print 21+21?>')
	check('42', '<?code x=21?><?code y=21?><?print x+y?>')
	check('foobar', '<?code x="foo"?><?code y="bar"?><?print x+y?>')
	check('(f)(o)(o)(b)(a)(r)', '<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>', data=dict(foo="foo", bar="bar"))


def test_sub():
	check('0', '<?print 21-21?>')
	check('0', '<?code x=21?><?code y=21?><?print x-y?>')



def test_mul():
	check(str(17*23), '<?print 17*23?>')
	check(str(17*23), '<?code x=17?><?code y=23?><?print x*y?>')
	check(17*"foo", '<?print 17*"foo"?>')
	check(17*"foo", '<?code x=17?><?code y="foo"?><?print x*y?>')
	check("foo"*17, '<?code x="foo"?><?code y=17?><?print x*y?>')
	check("foo"*17, '<?print "foo"*17?>')
	check("(foo)(bar)(foo)(bar)(foo)(bar)", '<?for i in 3*data?>(<?print i?>)<?end for?>', data=["foo", "bar"])


def test_truediv():
	check("0.5", '<?print 1/2?>')
	check("0.5", '<?code x=1?><?code y=2?><?print x/y?>')


def test_floordiv():
	check("0", '<?print 1//2?>')
	check("0", '<?code x=1?><?code y=2?><?print x//y?>')


def test_mod():
	check(str(42%17), '<?print 42%17?>')
	check(str(42%17), '<?code x=42?><?code y=17?><?print x%y?>')


def test_eq():
	check("False", '<?print 17==23?>')
	check("True", '<?print 17==17?>')
	check("False", '<?print x==23?>', x=17)
	check("True", '<?print x==23?>', x=23)


def test_ne():
	check("True", '<?print 17!=23?>')
	check("False", '<?print 17!=17?>')
	check("True", '<?print x!=23?>', x=17)
	check("False", '<?print x!=23?>', x=23)


def test_lt():
	check("True", '<?print 1<2?>')
	check("False", '<?print 2<2?>')
	check("False", '<?print 3<2?>')
	check("True", '<?print x<2?>', x=1)
	check("False", '<?print x<2?>', x=2)
	check("False", '<?print x<2?>', x=3)


def test_le():
	check("True", '<?print 1<=2?>')
	check("True", '<?print 2<=2?>')
	check("False", '<?print 3<=2?>')
	check("True", '<?print x<=2?>', x=1)
	check("True", '<?print x<=2?>', x=2)
	check("False", '<?print x<=2?>', x=3)


def test_gt():
	check("False", '<?print 1>2?>')
	check("False", '<?print 2>2?>')
	check("True", '<?print 3>2?>')
	check("False", '<?print x>2?>', x=1)
	check("False", '<?print x>2?>', x=2)
	check("True", '<?print x>2?>', x=3)


def test_ge():
	check("False", '<?print 1>=2?>')
	check("True", '<?print 2>=2?>')
	check("True", '<?print 3>=2?>')
	check("False", '<?print x>=2?>', x=1)
	check("True", '<?print x>=2?>', x=2)
	check("True", '<?print x>=2?>', x=3)


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
	check("42", '<?print 2*data.value?>', data=dict(value=21))
	check("42", '<?print data.value[0]?>', data=dict(value=[42]))
	check("42", '<?print data[0].value?>', data=[dict(value=42)])
	check("42", '<?print data[0][0][0]?>', data=[[[42]]])
	check("42", '<?print data.value.value[0]?>', data=dict(value=dict(value=[42])))
	check("42", '<?print data.value.value[0].value.value[0]?>', data=dict(value=dict(value=[dict(value=dict(value=[42]))])))


def test_bracket():
	sc = "4"
	sv = "x"
	for i in xrange(10):
		sc = "(%s)" % sc
		sv = "(%s)" % sv

	check("4", '<?print %s?>' % sc)
	check("4", '<?code x=4?><?print %s?>' % sv)


def test_function_now():
	checkrunerror("function u?'now' unknown", "<?print now(1)?>")
	checkrunerror("function u?'now' unknown", "<?print now(1, 2)?>")
	now = unicode(datetime.datetime.now())
	checkle(now, "<?print now()?>")


def test_function_vars():
	checkrunerror("function u?'vars' unknown", "<?print vars(1)?>")
	checkrunerror("function u?'vars' unknown", "<?print vars(1, 2)?>")
	check("yes", "<?if 'spam' in vars()?>yes<?else?>no<?end if?>", spam="eggs")


def test_function_xmlescape():
	checkrunerror("function u?'xmlescape' unknown", "<?print xmlescape()?>")
	checkrunerror("function u?'xmlescape' unknown", "<?print xmlescape(1, 2)?>")
	check("&lt;&gt;&amp;&#39;&quot;gurk", "<?print xmlescape(data)?>", data='<>&\'"gurk')


def test_function_csvescape():
	checkrunerror("function u?'csvescape' unknown", "<?print csvescape()?>")
	checkrunerror("function u?'csvescape' unknown", "<?print csvescape(1, 2)?>")
	check("", "<?print csvescape(data)?>", data=None)
	check("False", "<?print csvescape(data)?>", data=False)
	check("True", "<?print csvescape(data)?>", data=True)
	check("42", "<?print csvescape(data)?>", data=42)
	# no check for float
	check("abc", "<?print csvescape(data)?>", data="abc")
	check('"a,b,c"', "<?print csvescape(data)?>", data="a,b,c")
	check('"a""b""c"', "<?print csvescape(data)?>", data='a"b"c')
	check('"a\nb\nc"', "<?print csvescape(data)?>", data="a\nb\nc")


def test_function_str():
	checkrunerror("function u?'str' unknown", "<?print str()?>")
	checkrunerror("function u?'str' unknown", "<?print str(1, 2)?>")
	check("", "<?print str(data)?>", data=None)
	check("True", "<?print str(data)?>", data=True)
	check("False", "<?print str(data)?>", data=False)
	check("42", "<?print str(data)?>", data=42)
	check("4.2", "<?print str(data)?>", data=4.2)
	check("foo", "<?print str(data)?>", data="foo")


def test_function_int():
	checkrunerror("function u?'int' unknown", "<?print int()?>")
	checkrunerror("function u?'int' unknown", "<?print int(1, 2)?>")
	checkrunerror("int\\(\\) argument must be a string or a number, not 'NoneType'", "<?print int(data)?>", data=None)
	check("1", "<?print int(data)?>", data=True)
	check("0", "<?print int(data)?>", data=False)
	check("42", "<?print int(data)?>", data=42)
	check("4", "<?print int(data)?>", data=4.2)
	check("42", "<?print int(data)?>", data="42")
	checkrunerror("invalid literal for int\\(\\) with base 10: 'foo'", "<?print int(data)?>", data="foo")


def test_function_len():
	checkrunerror("function u?'len' unknown", "<?print len()?>")
	checkrunerror("function u?'len' unknown", "<?print len(1, 2)?>")
	checkrunerror("object of type 'NoneType' has no len", "<?print len(data)?>", data=None)
	checkrunerror("object of type 'bool' has no len", "<?print len(data)?>", data=True)
	checkrunerror("object of type 'bool' has no len", "<?print len(data)?>", data=False)
	checkrunerror("object of type 'int' has no len", "<?print len(data)?>", data=42)
	checkrunerror("object of type 'float' has no len", "<?print len(data)?>", data=4.2)
	check("42", "<?print len(data)?>", data=42*"?")
	check("42", "<?print len(data)?>", data=42*[None])
	check("42", "<?print len(data)?>", data=dict.fromkeys(xrange(42)))


def test_function_enumerate():
	checkrunerror("function u?'enumerate' unknown", "<?print enumerate()?>")
	checkrunerror("function u?'enumerate' unknown", "<?print enumerate(1, 2)?>")
	code = "<?for (i, value) in enumerate(data)?><?print i?>:<?print value?>\n<?end for?>"
	checkrunerror("'NoneType' object is not iterable", code, data=None)
	checkrunerror("'bool' object is not iterable", code, data=True)
	checkrunerror("'bool' object is not iterable", code, data=False)
	checkrunerror("'int' object is not iterable", code, data=42)
	checkrunerror("'float' object is not iterable", code, data=4.2)
	check("0:f\n1:o\n2:o\n", code, data="foo")
	check("0:foo\n1:bar\n", code, data=["foo", "bar"])
	check("0:foo\n", code, data=dict(foo=True))


def test_function_isnone():
	checkrunerror("function u?'isnone' unknown", "<?print isnone()?>")
	checkrunerror("function u?'isnone' unknown", "<?print isnone(1, 2)?>")
	code = "<?print isnone(data)?>"
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


def test_function_isbool():
	checkrunerror("function u?'isbool' unknown", "<?print isbool()?>")
	checkrunerror("function u?'isbool' unknown", "<?print isbool(1, 2)?>")
	code = "<?print isbool(data)?>"
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


def test_function_isint():
	checkrunerror("function u?'isint' unknown", "<?print isint()?>")
	checkrunerror("function u?'isint' unknown", "<?print isint(1, 2)?>")
	code = "<?print isint(data)?>"
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


def test_function_isfloat():
	checkrunerror("function u?'isfloat' unknown", "<?print isfloat()?>")
	checkrunerror("function u?'isfloat' unknown", "<?print isfloat(1, 2)?>")
	code = "<?print isfloat(data)?>"
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


def test_function_isstr():
	checkrunerror("function u?'isstr' unknown", "<?print isstr()?>")
	checkrunerror("function u?'isstr' unknown", "<?print isstr(1, 2)?>")
	code = "<?print isstr(data)?>"
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


def test_function_isdate():
	checkrunerror("function u?'isdate' unknown", "<?print isdate()?>")
	checkrunerror("function u?'isdate' unknown", "<?print isdate(1, 2)?>")
	code = "<?print isdate(data)?>"
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


def test_function_islist():
	checkrunerror("function u?'islist' unknown", "<?print islist()?>")
	checkrunerror("function u?'islist' unknown", "<?print islist(1, 2)?>")
	code = "<?print islist(data)?>"
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


def test_function_isdict():
	checkrunerror("function u?'isdict' unknown", "<?print isdict()?>")
	checkrunerror("function u?'isdict' unknown", "<?print isdict(1, 2)?>")
	code = "<?print isdict(data)?>"
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


def test_function_repr():
	checkrunerror("function u?'repr' unknown", "<?print repr()?>")
	checkrunerror("function u?'repr' unknown", "<?print repr(1, 2)?>")
	code = "<?print repr(data)?>"
	check("None", code, data=None)
	check("True", code, data=True)
	check("False", code, data=False)
	check("42", code, data=42)
	# no test for float
	check("'foo'", code, data="foo")
	# no test for tuples, lists and dicts


def test_function_chr():
	checkrunerror("function u?'chr' unknown", "<?print chr()?>")
	checkrunerror("function u?'chr' unknown", "<?print chr(1, 2)?>")
	code = "<?print chr(data)?>"
	check("\x00", code, data=0)
	check("a", code, data=ord("a"))
	check(u"\u20ac", code, data=0x20ac)


def test_function_ord():
	checkrunerror("function u?'ord' unknown", "<?print ord()?>")
	checkrunerror("function u?'ord' unknown", "<?print ord(1, 2)?>")
	code = "<?print ord(data)?>"
	check("0", code, data="\x00")
	check(str(ord("a")), code, data="a")
	check(str(0x20ac), code, data=u"\u20ac")


def test_function_hex():
	checkrunerror("function u?'hex' unknown", "<?print hex()?>")
	checkrunerror("function u?'hex' unknown", "<?print hex(1, 2)?>")
	code = "<?print hex(data)?>"
	check("0x0", code, data=0)
	check("0xff", code, data=0xff)
	check("0xffff", code, data=0xffff)
	check("-0xffff", code, data=-0xffff)


def test_function_oct():
	checkrunerror("function u?'oct' unknown", "<?print oct()?>")
	checkrunerror("function u?'oct' unknown", "<?print oct(1, 2)?>")
	code = "<?print oct(data)?>"
	check("0o0", code, data=0)
	check("0o77", code, data=077)
	check("0o7777", code, data=07777)
	check("-0o7777", code, data=-07777)


def test_function_bin():
	checkrunerror("function u?'bin' unknown", "<?print bin()?>")
	checkrunerror("function u?'bin' unknown", "<?print bin(1, 2)?>")
	code = "<?print bin(data)?>"
	check("0b0", code, data=0)
	check("0b11", code, data=3)
	check("-0b1111", code, data=-15)


def test_function_sorted():
	checkrunerror("function u?'sorted' unknown", "<?print sorted()?>")
	checkrunerror("function u?'sorted' unknown", "<?print sorted(1, 2)?>")
	code = "<?for i in sorted(data)?><?print i?><?end for?>"
	check("gkru", code, data="gurk")
	check("24679", code, data="92746")
	check("012", code, data={0: "zero", 1: "one", 2: "two"})


def test_function_range():
	checkrunerror("function u?'sorted' unknown", "<?print sorted()?>")
	code = "<?for i in range(data)?><?print i?><?end for?>"
	check("", code, data=-10)
	check("", code, data=0)
	check("0", code, data=1)
	check("01234", code, data=5)
	code = "<?for i in range(data[0], data[1])?><?print i?><?end for?>"
	check("", code, data=[0, -10])
	check("", code, data=[0, 0])
	check("01234", code, data=[0, 5])
	check("-5-4-3-2-101234", code, data=[-5, 5])
	code = "<?for i in range(data[0], data[1], data[2])?><?print i?><?end for?>"
	check("", code, data=[0, -10, 1])
	check("", code, data=[0, 0, 1])
	check("02468", code, data=[0, 10, 2])
	check("", code, data=[0, 10, -2])
	check("108642", code, data=[10, 0, -2])
	check("", code, data=[10, 0, 2])


def test_method_upper():
	check("GURK", "<?print 'gurk'.upper()?>")


def test_method_lower():
	check("gurk", "<?print 'GURK'.lower()?>")


def test_method_startswith():
	check("True", "<?print 'gurkhurz'.startswith('gurk')?>")
	check("False", "<?print 'gurkhurz'.startswith('hurz')?>")


def test_method_endswith():
	check("True", "<?print 'gurkhurz'.endswith('hurz')?>")
	check("False", "<?print 'gurkhurz'.endswith('gurk')?>")


def test_method_strip():
	check("gurk", r"<?print ' \t\r\ngurk \t\r\n'.strip()?>")
	check("gurk", r"<?print 'xyzzygurkxyzzy'.strip('xyz')?>")


def test_method_lstrip():
	check("gurk \t\r\n", r"<?print ' \t\r\ngurk \t\r\n'.lstrip()?>")
	check("gurkxyzzy", r"<?print 'xyzzygurkxyzzy'.lstrip('xyz')?>")


def test_method_rstrip():
	check(" \t\r\ngurk", r"<?print ' \t\r\ngurk \t\r\n'.rstrip()?>")
	check("xyzzygurk", r"<?print 'xyzzygurkxyzzy'.rstrip('xyz')?>")


def test_method_split():
	check("(g)(u)(r)(k)", r"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.split()?>(<?print item?>)<?end for?>")
	check("(g)(u \t\r\nr \t\r\nk \t\r\n)", r"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.split(None, 1)?>(<?print item?>)<?end for?>")
	check("()(g)(u)(r)(k)()", r"<?for item in 'xxgxxuxxrxxkxx'.split('xx')?>(<?print item?>)<?end for?>")
	check("()(g)(uxxrxxkxx)", r"<?for item in 'xxgxxuxxrxxkxx'.split('xx', 2)?>(<?print item?>)<?end for?>")


def test_method_rsplit():
	check("(g)(u)(r)(k)", r"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.rsplit()?>(<?print item?>)<?end for?>")
	check("( \t\r\ng \t\r\nu \t\r\nr)(k)", r"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.rsplit(None, 1)?>(<?print item?>)<?end for?>")
	check("()(g)(u)(r)(k)()", r"<?for item in 'xxgxxuxxrxxkxx'.rsplit('xx')?>(<?print item?>)<?end for?>")
	check("(xxgxxuxxr)(k)()", r"<?for item in 'xxgxxuxxrxxkxx'.rsplit('xx', 2)?>(<?print item?>)<?end for?>")


def test_method_replace():
	check('goork', r"<?print 'gurk'.replace('u', 'oo')?>")


def test_method_format():
	now = datetime.datetime.now()
	format = "%Y-%m-%d %H:%M:%S"
	check(now.strftime(format), r"<?print data.format('%s')?>" % format, data=now)


def test_method_isoformat():
	now = datetime.datetime.now()
	check(now.isoformat(), r"<?print data.isoformat()?>", data=now)


def test_render():
	t = ul4c.compile('<?print prefix?><?print data?><?print suffix?>')
	check('(f)(o)(o)', '<?for c in data?><?render t(data=c, prefix="(", suffix=")")?><?end for?>', dict(t=t), data='foo')


def test_render_var():
	t = ul4c.compile('<?code x += 1?><?print x?>')
	check('42,43,42', '<?print x?>,<?render t(x=x)?>,<?print x?>', dict(t=t), x=42)


def test_parse():
	check('42', '<?print data.Noner?>', data=dict(Noner=42))
