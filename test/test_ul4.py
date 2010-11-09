#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import os, re, datetime, StringIO, json, contextlib, tempfile

import py.test

from ll import ul4c, color


@contextlib.contextmanager
def raises(msg):
	# Check that the ``with`` block raises an exception that matches a regexp
	try:
		yield
	except Exception, exc:
		assert re.search(msg, "{0.__class__.__module__}.{0.__class__.__name__}: {0}".format(exc)) is not None
	else:
		py.test.fail("failed to raise exception")


def render(__, **variables):
	__ = ul4c.compile(__)
	print "Testing Python template:"
	print __.pythonsource()
	return __.renders(**variables)


def renderdumps(__, **variables):
	__ = ul4c.compile(__)
	__ = ul4c.loads(__.dumps()) # Recreate the template from the binary dump
	print "Testing Python template loaded from string:"
	print __.pythonsource()
	return __.renders(**variables)


def renderdump(__, **variables):
	__ = ul4c.compile(__)
	stream = StringIO.StringIO()
	__.dump(stream)
	stream.seek(0)
	__ = ul4c.load(stream) # Recreate the template from the stream
	print "Testing Python template loaded from stream:"
	print __.pythonsource()
	return __.renders(**variables)


def renderjs(__, **variables):
	# Check the Javascript version (this requires an installed ``d8`` shell from V8 (http://code.google.com/p/v8/))
	__ = ul4c.compile(__)
	js = __.jssource()
	print "Testing Javascript template:"
	print js.encode("utf-8")
	js = u"template = {};\ndata = {};\nprint(template.renders(data));\n".format(js, ul4c._json(variables))
	with tempfile.NamedTemporaryFile(mode="wb", suffix=".js") as f:
		f.write(js.encode("utf-8"))
		f.flush()
		result = os.popen("d8 js/ul4.js {}".format(f.name), "rb").read()
	result = result.decode("utf-8")[:-1] # Drop the "\n"
	# Check if we have an exception
	if result.endswith("^"):
		raise RuntimeError(result.splitlines()[0])
	return result


def with_all_renderers(func):
	# Decorator that turns a test into a generative test testing the function ``func`` with all ``render*`` functions.
	def decorated():
		yield func, render
		yield func, renderdumps
		yield func, renderdump
		yield func, renderjs
	return decorated


@with_all_renderers
def test_text(r):
	assert u'gurk' == r(u'gurk')
	assert u'g\xfcrk' == r(u'g\xfcrk')


@with_all_renderers
def test_none(r):
	assert '' == r(u'<?print None?>')
	assert 'no' == r(u'<?if None?>yes<?else?>no<?end if?>')


@with_all_renderers
def test_false(r):
	assert 'False' == r(u'<?print False?>')
	assert 'no' == r(u'<?if False?>yes<?else?>no<?end if?>')


@with_all_renderers
def test_true(r):
	assert 'True' == r(u'<?print True?>')
	assert 'yes' == r(u'<?if True?>yes<?else?>no<?end if?>')


@with_all_renderers
def test_int(r):
	assert '0' == r(u'<?print 0?>')
	assert '42' == r(u'<?print 42?>')
	assert '-42' == r(u'<?print -42?>')
	assert '255' == r(u'<?print 0xff?>')
	assert '255' == r(u'<?print 0Xff?>')
	assert '-255' == r(u'<?print -0xff?>')
	assert '-255' == r(u'<?print -0Xff?>')
	assert '63' == r(u'<?print 0o77?>')
	assert '63' == r(u'<?print 0O77?>')
	assert '-63' == r(u'<?print -0o77?>')
	assert '-63' == r(u'<?print -0O77?>')
	assert '7' == r(u'<?print 0b111?>')
	assert '7' == r(u'<?print 0B111?>')
	assert '-7' == r(u'<?print -0b111?>')
	assert '-7' == r(u'<?print -0B111?>')

	assert 'no' == r(u'<?if 0?>yes<?else?>no<?end if?>')
	assert 'yes' == r(u'<?if 1?>yes<?else?>no<?end if?>')
	assert 'yes' == r(u'<?if -1?>yes<?else?>no<?end if?>')


@with_all_renderers
def test_float(r):
	# str() output might differ slightly between Python and JS, so eval the output again for tests
	assert 0.0 == eval(r(u'<?print 0.?>'))
	assert 42.0 == eval(r(u'<?print 42.?>'))
	assert -42.0 == eval(r(u'<?print -42.?>'))
	assert -42.5 == eval(r(u'<?print -42.5?>'))
	assert 1e42 == eval(r(u'<?print 1E42?>'))
	assert 1e42 == eval(r(u'<?print 1e42?>'))
	assert -1e42 == eval(r(u'<?print -1E42?>'))
	assert -1e42 == eval(r(u'<?print -1e42?>'))

	assert 'no' == r(u'<?if 0.?>yes<?else?>no<?end if?>')
	assert 'yes' == r(u'<?if 1.?>yes<?else?>no<?end if?>')
	assert 'yes' == r(u'<?if -1.?>yes<?else?>no<?end if?>')


@with_all_renderers
def test_string(r):
	with raises("Unterminated string"):
		r(u'<?print "?>')
	assert 'foo' == r(u'<?print "foo"?>')
	assert '\n' == r(u'<?print "\\n"?>')
	assert '\r' == r(u'<?print "\\r"?>')
	assert '\t' == r(u'<?print "\\t"?>')
	assert '\f' == r(u'<?print "\\f"?>')
	assert '\b' == r(u'<?print "\\b"?>')
	assert '\a' == r(u'<?print "\\a"?>')
	assert '\x1b' == r(u'<?print "\\e"?>')
	assert '"' == r(u'<?print "\\""?>')
	assert "'" == r(u'<?print "\\\'"?>')
	assert u'\u20ac' == r(u'<?print "\u20ac"?>')
	assert u'\xff' == r(u'<?print "\\xff"?>')
	assert u'\u20ac' == r(u'''<?print "\\u20ac"?>''')
	assert "\\xxx" == r(u'<?print "\\xxx"?>')
	assert "a\nb" == r(u'<?print "a\nb"?>')

	assert 'no' == r(u'<?if ""?>yes<?else?>no<?end if?>')
	assert 'yes' == r(u'<?if "foo"?>yes<?else?>no<?end if?>')


@with_all_renderers
def test_date(r):
	assert '2000-02-29T00:00:00' == r(u'<?print @2000-02-29T.isoformat()?>')
	assert '2000-02-29T12:34:00' == r(u'<?print @2000-02-29T12:34.isoformat()?>')
	assert '2000-02-29T12:34:56' == r(u'<?print @2000-02-29T12:34:56.isoformat()?>')
	assert '2000-02-29T12:34:56.987000' == r(u'<?print @2000-02-29T12:34:56.987000.isoformat()?>') # JS only supports milliseconds
	assert 'yes' == r(u'<?if @2000-02-29T12:34:56.987654?>yes<?else?>no<?end if?>')


@with_all_renderers
def test_color(r):
	assert '255,255,255,255' == r(u'<?code c = #fff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	assert '255,255,255,255' == r(u'<?code c = #ffffff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	assert '18,52,86,255' == r(u'<?code c = #123456?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	assert '17,34,51,68' == r(u'<?code c = #1234?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	assert '18,52,86,120' == r(u'<?code c = #12345678?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	assert 'yes' == r(u'<?if #fff?>yes<?else?>no<?end if?>')


@with_all_renderers
def test_list(r):
	assert '' == r(u'<?for item in []?><?print item?>;<?end for?>')
	assert '1;' == r(u'<?for item in [1]?><?print item?>;<?end for?>')
	assert '1;' == r(u'<?for item in [1,]?><?print item?>;<?end for?>')
	assert '1;2;' == r(u'<?for item in [1, 2]?><?print item?>;<?end for?>')
	assert '1;2;' == r(u'<?for item in [1, 2,]?><?print item?>;<?end for?>')
	assert 'no' == r(u'<?if []?>yes<?else?>no<?end if?>')
	assert 'yes' == r(u'<?if [1]?>yes<?else?>no<?end if?>')


@with_all_renderers
def test_dict(r):
	assert '' == r(u'<?for (key, value) in {}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert '1:2\n' == r(u'<?for (key, value) in {1:2}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert '1:2\n' == r(u'<?for (key, value) in {1:2,}.items()?><?print key?>:<?print value?>\n<?end for?>')
	# With duplicate keys, later ones simply overwrite earlier ones
	assert '1:3\n' == r(u'<?for (key, value) in {1:2, 1: 3}.items()?><?print key?>:<?print value?>\n<?end for?>')
	# Test **
	assert '1:2\n' == r(u'<?for (key, value) in {**{1:2}}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert '1:4\n' == r(u'<?for (key, value) in {1:1, **{1:2}, 1:3, **{1:4}}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert 'no' == r(u'<?if {}?>yes<?else?>no<?end if?>')
	assert 'yes' == r(u'<?if {1:2}?>yes<?else?>no<?end if?>')


@with_all_renderers
def test_code_storevar(r):
	assert '42' == r(u'<?code x = 42?><?print x?>')
	assert 'xyzzy' == r(u'<?code x = "xyzzy"?><?print x?>')


@with_all_renderers
def test_code_addvar(r):
	assert '40' == r(u'<?code x = 17?><?code x += 23?><?print x?>')
	assert 'xyzzy' == r(u'<?code x = "xyz"?><?code x += "zy"?><?print x?>')


@with_all_renderers
def test_code_subvar(r):
	assert '-6' == r(u'<?code x = 17?><?code x -= 23?><?print x?>')


@with_all_renderers
def test_code_mulvar(r):
	assert '391' == r(u'<?code x = 17?><?code x *= 23?><?print x?>')
	assert 17*'xyzzy' == r(u'<?code x = 17?><?code x *= "xyzzy"?><?print x?>')
	assert 17*'xyzzy' == r(u'<?code x = "xyzzy"?><?code x *= 17?><?print x?>')


@with_all_renderers
def test_code_floordivvar(r):
	assert '2' == r(u'<?code x = 5?><?code x //= 2?><?print x?>')
	assert '-3' == r(u'<?code x = -5?><?code x //= 2?><?print x?>')


@with_all_renderers
def test_code_truedivvar(r):
	assert '2.5' == r(u'<?code x = 5?><?code x /= 2?><?print x?>')
	assert '-2.5' == r(u'<?code x = -5?><?code x /= 2?><?print x?>')


@with_all_renderers
def test_code_modvar(r):
	assert '4' == r(u'<?code x = 1729?><?code x %= 23?><?print x?>')


@with_all_renderers
def test_code_delvar(r):
	with raises("(KeyError|not found)"):
		r(u'<?code x = 1729?><?code del x?><?print x?>')


@with_all_renderers
def test_for_string(r):
	assert '' == r(u'<?for c in data?>(<?print c?>)<?end for?>', data="")
	assert '(g)(u)(r)(k)' == r(u'<?for c in data?>(<?print c?>)<?end for?>', data="gurk")


@with_all_renderers
def test_for_list(r):
	assert '' == r(u'<?for c in data?>(<?print c?>)<?end for?>', data="")
	assert '(g)(u)(r)(k)' == r(u'<?for c in data?>(<?print c?>)<?end for?>', data=["g", "u", "r", "k"])


@with_all_renderers
def test_for_dict(r):
	assert '' == r(u'<?for c in data?>(<?print c?>)<?end for?>', data={})
	assert '(a)(b)(c)' == r(u'<?for c in sorted(data)?>(<?print c?>)<?end for?>', data=dict(a=1, b=2, c=3))


@with_all_renderers
def test_for_nested(r):
	assert '[(1)(2)][(3)(4)]' == r(u'<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>', data=[[1, 2], [3, 4]])


@with_all_renderers
def test_for_unpacking(r):
	data = [
		("spam", "eggs", 17),
		("gurk", "hurz", 23),
		("hinz", "kunz", 42)
	]

	assert '(spam)(gurk)(hinz)' == r(u'<?for (a,) in data?>(<?print a?>)<?end for?>', data=data)
	assert '(spam,eggs)(gurk,hurz)(hinz,kunz)' == r(u'<?for (a, b) in data?>(<?print a?>,<?print b?>)<?end for?>', data=data)
	assert '(spam,eggs,17)(gurk,hurz,23)(hinz,kunz,42)' == r(u'<?for (a, b, c) in data?>(<?print a?>,<?print b?>,<?print c?>)<?end for?>', data=data)


@with_all_renderers
def test_break(r):
	assert '1, 2, ' == r(u'<?for i in [1,2,3]?><?print i?>, <?if i==2?><?break?><?end if?><?end for?>')


@with_all_renderers
def test_break_nested(r):
	assert '1, 1, 2, 1, 2, 3, ' == r(u'<?for i in [1,2,3,4]?><?for j in [1,2,3,4]?><?print j?>, <?if j>=i?><?break?><?end if?><?end for?><?if i>=3?><?break?><?end if?><?end for?>')


@with_all_renderers
def test_continue(r):
	assert '1, 3, ' == r(u'<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?print i?>, <?end for?>')


@with_all_renderers
def test_continue_nested(r):
	assert '1, 3, \n1, 3, \n' == r(u'<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?for j in [1,2,3]?><?if j==2?><?continue?><?end if?><?print j?>, <?end for?>\n<?end for?>')


@with_all_renderers
def test_if(r):
	assert '42' == r(u'<?if data?><?print data?><?end if?>', data=42)


@with_all_renderers
def test_else(r):
	assert '42' == r(u'<?if data?><?print data?><?else?>no<?end if?>', data=42)
	assert 'no' == r(u'<?if data?><?print data?><?else?>no<?end if?>', data=0)


def test_block_errors():
	with raises("in u?.<.for x in data.>..*block unclosed"):
		render(u'<?for x in data?>')
	with raises("endif doesn't match any if"):
		render(u'<?for x in data?><?end if?>')
	with raises("not in any block"):
		render(u'<?end?>')
	with raises("not in any block"):
		render(u'<?end for?>')
	with raises("not in any block"):
		render(u'<?end if?>')
	with raises("else doesn't match any if"):
		render(u'<?else?>')
	with raises("in u?.<.if data.>..*block unclosed"):
		render(u'<?if data?>')
	with raises("in u?.<.if data.>..*block unclosed"):
		render(u'<?if data?><?else?>')
	with raises("duplicate else"):
		render(u'<?if data?><?else?><?else?>')
	with raises("else already seen in elif"):
		render(u'<?if data?><?else?><?elif data?>')
	with raises("else already seen in elif"):
		render(u'<?if data?><?elif data?><?elif data?><?else?><?elif data?>')


def test_empty():
	with raises("expression required"):
		render(u'<?print?>')
	with raises("expression required"):
		render(u'<?if?>')
	with raises("expression required"):
		render(u'<<?if x?><?elif?><?end if?>')
	with raises("loop expression required"):
		render(u'<?for?>')
	with raises("statement required"):
		render(u'<?code?>')
	with raises("render statement required"):
		render(u'<?render?>')


@with_all_renderers
def test_add(r):
	assert '42' == r(u'<?print 21+21?>')
	assert '42' == r(u'<?code x=21?><?code y=21?><?print x+y?>')
	assert 'foobar' == r(u'<?code x="foo"?><?code y="bar"?><?print x+y?>')
	assert '(f)(o)(o)(b)(a)(r)' == r(u'<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>', data=dict(foo="foo", bar="bar"))


@with_all_renderers
def test_sub(r):
	assert '0' == r(u'<?print 21-21?>')
	assert '0' == r(u'<?code x=21?><?code y=21?><?print x-y?>')


@with_all_renderers
def test_mul(r):
	assert str(17*23) == r(u'<?print 17*23?>')
	assert str(17*23) == r(u'<?code x=17?><?code y=23?><?print x*y?>')
	assert 17*"foo" == r(u'<?print 17*"foo"?>')
	assert 17*"foo" == r(u'<?code x=17?><?code y="foo"?><?print x*y?>')
	assert "foo"*17 == r(u'<?code x="foo"?><?code y=17?><?print x*y?>')
	assert "foo"*17 == r(u'<?print "foo"*17?>')
	assert "(foo)(bar)(foo)(bar)(foo)(bar)" == r(u'<?for i in 3*data?>(<?print i?>)<?end for?>', data=["foo", "bar"])


@with_all_renderers
def test_truediv(r):
	assert "0.5" == r(u'<?print 1/2?>')
	assert "0.5" == r(u'<?code x=1?><?code y=2?><?print x/y?>')


@with_all_renderers
def test_floordiv(r):
	assert "0" == r(u'<?print 1//2?>')
	assert "0" == r(u'<?code x=1?><?code y=2?><?print x//y?>')


@with_all_renderers
def test_mod(r):
	assert str(42%17) == r(u'<?print 42%17?>')
	assert str(42%17) == r(u'<?code x=42?><?code y=17?><?print x%y?>')


@with_all_renderers
def test_eq(r):
	assert "False" == r(u'<?print 17==23?>')
	assert "True" == r(u'<?print 17==17?>')
	assert "False" == r(u'<?print x==23?>', x=17)
	assert "True" == r(u'<?print x==23?>', x=23)


@with_all_renderers
def test_ne(r):
	assert "True" == r(u'<?print 17!=23?>')
	assert "False" == r(u'<?print 17!=17?>')
	assert "True" == r(u'<?print x!=23?>', x=17)
	assert "False" == r(u'<?print x!=23?>', x=23)


@with_all_renderers
def test_lt(r):
	assert "True" == r(u'<?print 1<2?>')
	assert "False" == r(u'<?print 2<2?>')
	assert "False" == r(u'<?print 3<2?>')
	assert "True" == r(u'<?print x<2?>', x=1)
	assert "False" == r(u'<?print x<2?>', x=2)
	assert "False" == r(u'<?print x<2?>', x=3)


@with_all_renderers
def test_le(r):
	assert "True" == r(u'<?print 1<=2?>')
	assert "True" == r(u'<?print 2<=2?>')
	assert "False" == r(u'<?print 3<=2?>')
	assert "True" == r(u'<?print x<=2?>', x=1)
	assert "True" == r(u'<?print x<=2?>', x=2)
	assert "False" == r(u'<?print x<=2?>', x=3)


@with_all_renderers
def test_gt(r):
	assert "False" == r(u'<?print 1>2?>')
	assert "False" == r(u'<?print 2>2?>')
	assert "True" == r(u'<?print 3>2?>')
	assert "False" == r(u'<?print x>2?>', x=1)
	assert "False" == r(u'<?print x>2?>', x=2)
	assert "True" == r(u'<?print x>2?>', x=3)


@with_all_renderers
def test_ge(r):
	assert "False" == r(u'<?print 1>=2?>')
	assert "True" == r(u'<?print 2>=2?>')
	assert "True" == r(u'<?print 3>=2?>')
	assert "False" == r(u'<?print x>=2?>', x=1)
	assert "True" == r(u'<?print x>=2?>', x=2)
	assert "True" == r(u'<?print x>=2?>', x=3)


@with_all_renderers
def test_contains(r):
	code = u'<?print x in y?>'

	assert "True" == r(code, x=2, y=[1, 2, 3])
	assert "False" == r(code, x=4, y=[1, 2, 3])
	assert "True" == r(code, x="ur", y="gurk")
	assert "False" == r(code, x="un", y="gurk")
	assert "True" == r(code, x="a", y={"a": 1, "b": 2})
	assert "False" == r(code, x="c", y={"a": 1, "b": 2})
	assert "True" == r(code, x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42))
	assert "False" == r(code, x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42))


@with_all_renderers
def test_notcontains(r):
	code = u'<?print x not in y?>'

	assert "False" == r(code, x=2, y=[1, 2, 3])
	assert "True" == r(code, x=4, y=[1, 2, 3])
	assert "False" == r(code, x="ur", y="gurk")
	assert "True" == r(code, x="un", y="gurk")
	assert "False" == r(code, x="a", y={"a": 1, "b": 2})
	assert "True" == r(code, x="c", y={"a": 1, "b": 2})
	assert "False" == r(code, x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42))
	assert "True" == r(code, x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42))


@with_all_renderers
def test_and(r):
	assert "False" == r(u'<?print x and y?>', x=False, y=False)
	assert "False" == r(u'<?print x and y?>', x=False, y=True)
	assert "0" == r(u'<?print x and y?>', x=0, y=True)


@with_all_renderers
def test_or(r):
	assert "False" == r(u'<?print x or y?>', x=False, y=False)
	assert "True" == r(u'<?print x or y?>', x=False, y=True)
	assert "42" == r(u'<?print x or y?>', x=42, y=True)


@with_all_renderers
def test_not(r):
	assert "True" == r(u'<?print not x?>', x=False)
	assert "False" == r(u'<?print not x?>', x=42)


@with_all_renderers
def test_getitem(r):
	assert "u" == r(u"<?print 'gurk'[1]?>")
	assert "u" == r(u"<?print x[1]?>", x="gurk")
	assert "u" == r(u"<?print 'gurk'[-3]?>")
	assert "u" == r(u"<?print x[-3]?>", x="gurk")
	with raises("IndexError"):
		r(u"<?print 'gurk'[4]?>")
	with raises("index (4 )?out of range"):
		r(u"<?print x[4]?>", x="gurk")
	with raises("IndexError"):
		r(u"<?print 'gurk'[-5]?>")
	with raises("index (-5 )?out of range"):
		r(u"<?print x[-5]?>", x="gurk")


@with_all_renderers
def test_getslice12(r):
	assert "ur" == r(u"<?print 'gurk'[1:3]?>")
	assert "ur" == r(u"<?print x[1:3]?>", x="gurk")
	assert "ur" == r(u"<?print 'gurk'[-3:-1]?>")
	assert "ur" == r(u"<?print x[-3:-1]?>", x="gurk")
	assert "" == r(u"<?print 'gurk'[4:10]?>")
	assert "" == r(u"<?print x[4:10]?>", x="gurk")
	assert "" == r(u"<?print 'gurk'[-10:-5]?>")
	assert "" == r(u"<?print x[-10:-5]?>", x="gurk")


@with_all_renderers
def test_getslice1(r):
	assert "urk" == r(u"<?print 'gurk'[1:]?>")
	assert "urk" == r(u"<?print x[1:]?>", x="gurk")
	assert "urk" == r(u"<?print 'gurk'[-3:]?>")
	assert "urk" == r(u"<?print x[-3:]?>", x="gurk")
	assert "" == r(u"<?print 'gurk'[4:]?>")
	assert "" == r(u"<?print x[4:]?>", x="gurk")
	assert "gurk" == r(u"<?print 'gurk'[-10:]?>")
	assert "gurk" == r(u"<?print x[-10:]?>", x="gurk")


@with_all_renderers
def test_getslice2(r):
	assert "gur" == r(u"<?print 'gurk'[:3]?>")
	assert "gur" == r(u"<?print x[:3]?>", x="gurk")
	assert "gur" == r(u"<?print 'gurk'[:-1]?>")
	assert "gur" == r(u"<?print x[:-1]?>", x="gurk")
	assert "gurk" == r(u"<?print 'gurk'[:10]?>")
	assert "gurk" == r(u"<?print x[:10]?>", x="gurk")
	assert "" == r(u"<?print 'gurk'[:-5]?>")
	assert "" == r(u"<?print x[:-5]?>", x="gurk")


@with_all_renderers
def test_nested(r):
	sc = u"4"
	sv = u"x"
	n = 4
	for i in xrange(8): # when using 10 compiling the variable will run out of registers
		sc = u"({})+({})".format(sc, sc)
		sv = u"({})+({})".format(sv, sv)
		n = n + n

	assert str(n) == r(u'<?print {}?>'.format(sc))
	assert str(n) == r(u'<?code x=4?><?print {}?>'.format(sv))


@with_all_renderers
def test_precedence(r):
	assert "14" == r(u'<?print 2+3*4?>')
	assert "20" == r(u'<?print (2+3)*4?>')
	assert "10" == r(u'<?print -2+-3*-4?>')
	assert "14" == r(u'<?print --2+--3*--4?>')
	assert "14" == r(u'<?print (-(-2))+(-((-3)*-(-4)))?>')
	assert "42" == r(u'<?print 2*data.value?>', data=dict(value=21))
	assert "42" == r(u'<?print data.value[0]?>', data=dict(value=[42]))
	assert "42" == r(u'<?print data[0].value?>', data=[dict(value=42)])
	assert "42" == r(u'<?print data[0][0][0]?>', data=[[[42]]])
	assert "42" == r(u'<?print data.value.value[0]?>', data=dict(value=dict(value=[42])))
	assert "42" == r(u'<?print data.value.value[0].value.value[0]?>', data=dict(value=dict(value=[dict(value=dict(value=[42]))])))


@with_all_renderers
def test_bracket(r):
	sc = u"4"
	sv = u"x"
	for i in xrange(10):
		sc = u"({})".format(sc)
		sv = u"({})".format(sv)

	assert "4" == r(u'<?print {}?>'.format(sc))
	assert "4" == r(u'<?code x=4?><?print {}?>'.format(sv))


@with_all_renderers
def test_function_now(r):
	now = unicode(datetime.datetime.now())

	with raises("now.*unknown"):
		r(u"<?print now(1)?>")
	with raises("now.*unknown"):
		r(u"<?print now(1, 2)?>")
	assert now <= r(u"<?print now()?>")


@with_all_renderers
def test_function_utcnow(r):
	utcnow = unicode(datetime.datetime.utcnow())

	with raises("utcnow.*unknown"):
		r(u"<?print utcnow(1)?>")
	with raises("utcnow.*unknown"):
		r(u"<?print utcnow(1, 2)?>")
	assert utcnow <= r(u"<?print utcnow()?>")


@with_all_renderers
def test_function_vars(r):
	code = u"<?if var in vars()?>yes<?else?>no<?end if?>"

	with raises("vars.*unknown"):
		r("<?print vars(1)?>")
	with raises("vars.*unknown"):
		r("<?print vars(1, 2)?>")
	assert "yes" == r(code, var="spam", spam="eggs")
	assert "no" == r(code, var="nospam", spam="eggs")


@with_all_renderers
def test_function_random(r):
	with raises("random.*unknown"):
		r("<?print random(1)?>")
	with raises("random.*unknown"):
		r("<?print random(1, 2)?>")
	assert "ok" == r(u"<?code r = random()?><?if r>=0 and r<1?>ok<?else?>fail<?end if?>")


@with_all_renderers
def test_function_randrange(r):
	with raises("randrange.*unknown"):
		r("<?print randrange()?>")
	assert "ok" == r(u"<?code r = randrange(4)?><?if r>=0 and r<4?>ok<?else?>fail<?end if?>")
	assert "ok" == r(u"<?code r = randrange(17, 23)?><?if r>=17 and r<23?>ok<?else?>fail<?end if?>")
	assert "ok" == r(u"<?code r = randrange(17, 23, 2)?><?if r>=17 and r<23 and r%2?>ok<?else?>fail<?end if?>")


@with_all_renderers
def test_function_randchoice(r):
	with raises("randchoice.*unknown"):
		r("<?print randchoice()?>")
	assert "ok" == r(u"<?code r = randchoice('abc')?><?if r in 'abc'?>ok<?else?>fail<?end if?>")
	assert "ok" == r(u"<?code s = [17, 23, 42]?><?code r = randchoice(s)?><?if r in s?>ok<?else?>fail<?end if?>")
	assert "ok" == r(u"<?code s = #12345678?><?code sl = [0x12, 0x34, 0x56, 0x78]?><?code r = randchoice(s)?><?if r in sl?>ok<?else?>fail<?end if?>")


@with_all_renderers
def test_function_xmlescape(r):
	with raises("xmlescape.*unknown"):
		r(u"<?print xmlescape()?>")
	with raises("xmlescape.*unknown"):
		r(u"<?print xmlescape(1, 2)?>")
	assert "&lt;&lt;&gt;&gt;&amp;&#39;&quot;gurk" == r(u"<?print xmlescape(data)?>", data='<<>>&\'"gurk')


@with_all_renderers
def test_function_csv(r):
	with raises("csv.*unknown"):
		r(u"<?print csv()?>")
	with raises("csv.*unknown"):
		r(u"<?print csv(1, 2)?>")
	assert "" == r(u"<?print csv(data)?>", data=None)
	assert "False" == r(u"<?print csv(data)?>", data=False)
	assert "True" == r(u"<?print csv(data)?>", data=True)
	assert "42" == r(u"<?print csv(data)?>", data=42)
	# no check for float
	assert "abc" == r(u"<?print csv(data)?>", data="abc")
	assert '"a,b,c"' == r(u"<?print csv(data)?>", data="a,b,c")
	assert '"a""b""c"' == r(u"<?print csv(data)?>", data='a"b"c')
	assert '"a\nb\nc"' == r(u"<?print csv(data)?>", data="a\nb\nc")


@with_all_renderers
def test_function_json(r):
	with raises("json.*unknown"):
		r(u"<?print json()?>")
	with raises("json.*unknown"):
		r(u"<?print json(1, 2)?>")
	assert "null" == r(u"<?print json(data)?>", data=None)
	assert "false" == r(u"<?print json(data)?>", data=False)
	assert "true" == r(u"<?print json(data)?>", data=True)
	assert "42" == r(u"<?print json(data)?>", data=42)
	# no check for float
	assert '"abc"' == r(u"<?print json(data)?>", data="abc")
	assert '[1, 2, 3]', r(u"<?print json(data)?>", data=[1, 2, 3])
	assert '{"one": 1}' == r(u"<?print json(data)?>", data={"one": 1})


@with_all_renderers
def test_function_str(r):
	with raises("str.*unknown"):
		r(u"<?print str()?>")
	with raises("str.*unknown"):
		r(u"<?print str(1, 2)?>")
	assert "" == r(u"<?print str(data)?>", data=None)
	assert "True" == r(u"<?print str(data)?>", data=True)
	assert "False" == r(u"<?print str(data)?>", data=False)
	assert "42" == r(u"<?print str(data)?>", data=42)
	assert "4.2" == r(u"<?print str(data)?>", data=4.2)
	assert "foo" == r(u"<?print str(data)?>", data="foo")


@with_all_renderers
def test_function_int(r):
	with raises("int.*unknown"):
		r(u"<?print int()?>")
	with raises("int.*unknown"):
		r(u"<?print int(1, 2, 3)?>")
	with raises("int\\(\\) argument must be a string or a number"):
		r(u"<?print int(data)?>", data=None)
	with raises("invalid literal for int"):
		r(u"<?print int(data)?>", data="foo")
	assert "1" == r(u"<?print int(data)?>", data=True)
	assert "0" == r(u"<?print int(data)?>", data=False)
	assert "42" == r(u"<?print int(data)?>", data=42)
	assert "4" == r(u"<?print int(data)?>", data=4.2)
	assert "42" == r(u"<?print int(data)?>", data="42")
	assert "66" == r(u"<?print int(data, 16)?>", data="42")


@with_all_renderers
def test_function_float(r):
	code = u"<?print float(data)?>"

	with raises("float.*unknown"):
		r(u"<?print float()?>")
	with raises("float.*unknown"):
		r(u"<?print float(1, 2, 3)?>")
	with raises("float\\(\\) argument must be a string or a number"):
		r(code, data=None)
	assert "4.2" == r(code, data=4.2)
	if r is not renderjs:
		assert "1.0" == r(code, data=True)
		assert "0.0" == r(code, data=False)
		assert "42.0" == r(code, data=42)
		assert "42.0" == r(code, data="42")
	else:
		assert 1.0 == eval(r(code, data=True))
		assert 0.0 == eval(r(code, data=False))
		assert 42.0 == eval(r(code, data=42))
		assert 42.0 == eval(r(code, data="42"))


@with_all_renderers
def test_function_len(r):
	code = u"<?print len(data)?>"
	with raises("len.*unknown"):
		r(u"<?print len()?>")
	with raises("len.*unknown"):
		r(u"<?print len(1, 2)?>")
	with raises("has no len\\(\\)"):
		r(code, data=None)
	with raises("has no len\\(\\)"):
		r(code, data=True)
	with raises("has no len\\(\\)"):
		r(code, data=False)
	with raises("has no len\\(\\)"):
		r(code, data=42)
	with raises("has no len\\(\\)"):
		r(code, data=4.2)
	assert "42" == r(code, data=42*"?")
	assert "42" == r(code, data=42*[None])
	assert "42" == r(code, data=dict.fromkeys(xrange(42)))


@with_all_renderers
def test_function_enumerate(r):
	code = u"<?for (i, value) in enumerate(data)?><?print i?>:<?print value?>\n<?end for?>"
	with raises("enumerate.*unknown"):
		r(u"<?print enumerate()?>")
	with raises("enumerate.*unknown"):
		r(u"<?print enumerate(1, 2)?>")
	with raises("is not iterable"):
		r(code, data=None)
	with raises("is not iterable"):
		r(code, data=True)
	with raises("is not iterable"):
		r(code, data=False)
	with raises("is not iterable"):
		r(code, data=42)
	with raises("is not iterable"):
		r(code, data=4.2)
	assert "0:f\n1:o\n2:o\n" == r(code, data="foo")
	assert "0:foo\n1:bar\n" == r(code, data=["foo", "bar"])
	assert "0:foo\n" == r(code, data=dict(foo=True))


@with_all_renderers
def test_function_isnone(r):
	code = u"<?print isnone(data)?>"
	with raises("isnone.*unknown"):
		r(u"<?print isnone()?>")
	with raises("isnone.*unknown"):
		r(u"<?print isnone(1, 2)?>")
	assert "True" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.compile(u""))
	assert "False" == r(code, data=color.red)


@with_all_renderers
def test_function_isbool(r):
	code = u"<?print isbool(data)?>"

	with raises("isbool.*unknown"):
		r(u"<?print isbool()?>")
	with raises("isbool.*unknown"):
		r(u"<?print isbool(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "True" == r(code, data=True)
	assert "True" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.compile(u""))
	assert "False" == r(code, data=color.red)


@with_all_renderers
def test_function_isint(r):
	code = u"<?print isint(data)?>"

	with raises("isint.*unknown"):
		r(u"<?print isint()?>")
	with raises("isint.*unknown"):
		r(u"<?print isint(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "True" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.compile(u""))
	assert "False" == r(code, data=color.red)


@with_all_renderers
def test_function_isfloat(r):
	code = u"<?print isfloat(data)?>"

	with raises("isfloat.*unknown"):
		r(u"<?print isfloat()?>")
	with raises("isfloat.*unknown"):
		r(u"<?print isfloat(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "True" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.compile(u""))
	assert "False" == r(code, data=color.red)


@with_all_renderers
def test_function_isstr(r):
	code = u"<?print isstr(data)?>"

	with raises("isstr.*unknown"):
		r(u"<?print isstr()?>")
	with raises("isstr.*unknown"):
		r(u"<?print isstr(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "True" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.compile(u""))
	assert "False" == r(code, data=color.red)


@with_all_renderers
def test_function_isdate(r):
	code = u"<?print isdate(data)?>"

	with raises("isdate.*unknown"):
		r(u"<?print isdate()?>")
	with raises("isdate.*unknown"):
		r(u"<?print isdate(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "True" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.compile(u""))
	assert "False" == r(code, data=color.red)


@with_all_renderers
def test_function_islist(r):
	code = u"<?print islist(data)?>"

	with raises("islist.*unknown"):
		r(u"<?print islist()?>")
	with raises("islist.*unknown"):
		r(u"<?print islist(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "True" == r(code, data=())
	assert "True" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.compile(u""))
	assert "False" == r(code, data=color.red)


@with_all_renderers
def test_function_isdict(r):
	code = u"<?print isdict(data)?>"

	with raises("isdict.*unknown"):
		r(u"<?print isdict()?>")
	with raises("isdict.*unknown"):
		r(u"<?print isdict(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "True" == r(code, data={})
	assert "False" == r(code, data=ul4c.compile(u""))
	assert "False" == r(code, data=color.red)


@with_all_renderers
def test_function_istemplate(r):
	code = u"<?print istemplate(data)?>"

	with raises("istemplate.*unknown"):
		r(u"<?print istemplate()?>")
	with raises("istemplate.*unknown"):
		r(u"<?print istemplate(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "True" == r(code, data=ul4c.compile(u""))
	assert "False" == r(code, data=color.red)


@with_all_renderers
def test_function_iscolor(r):
	code = u"<?print iscolor(data)?>"

	with raises("iscolor.*unknown"):
		r(u"<?print iscolor()?>")
	with raises("iscolor.*unknown"):
		r(u"<?print iscolor(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.compile(u""))
	assert "True" == r(code, data=color.red)


@with_all_renderers
def test_function_get(r):
	with raises("get.*unknown"):
		r(u"<?print get()?>")
	assert "" == r(u"<?print get('x')?>")
	assert "42" == r(u"<?print get('x')?>", x=42)
	assert "17" == r(u"<?print get('x', 17)?>")
	assert "42" == r(u"<?print get('x', 17)?>", x=42)


@with_all_renderers
def test_function_repr(r):
	code = u"<?print repr(data)?>"

	with raises("repr.*unknown"):
		r(u"<?print repr()?>")
	with raises("repr.*unknown"):
		r(u"<?print repr(1, 2)?>")
	assert "None" == r(code, data=None)
	assert "True" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "42" == r(code, data=42)
	assert 42.5 == eval(r(code, data=42.5))
	assert r(code, data="foo") in ('"foo"', "'foo'")
	assert [1, 2, 3] == eval(r(code, data=[1, 2, 3]))
	if r is not renderjs:
		assert (1, 2, 3) == eval(r(code, data=(1, 2, 3)))
	assert {"a": 1, "b": 2} == eval(r(code, data={"a": 1, "b": 2}))


@with_all_renderers
def test_function_chr(r):
	code = u"<?print chr(data)?>"

	with raises("chr.*unknown"):
		r(u"<?print chr()?>")
	with raises("chr.*unknown"):
		r(u"<?print chr(1, 2)?>")
	assert "\x00" == r(code, data=0)
	assert "a" == r(code, data=ord("a"))
	assert u"\u20ac" == r(code, data=0x20ac)


@with_all_renderers
def test_function_ord(r):
	code = u"<?print ord(data)?>"

	with raises("ord.*unknown"):
		r(u"<?print ord()?>")
	with raises("ord.*unknown"):
		r(u"<?print ord(1, 2)?>")
	assert "0" == r(code, data="\x00")
	assert str(ord("a")) == r(code, data="a")
	assert str(0x20ac) == r(code, data=u"\u20ac")


@with_all_renderers
def test_function_hex(r):
	code = u"<?print hex(data)?>"

	with raises("hex.*unknown"):
		r(u"<?print hex()?>")
	with raises("hex.*unknown"):
		r(u"<?print hex(1, 2)?>")
	assert "0x0" == r(code, data=0)
	assert "0xff" == r(code, data=0xff)
	assert "0xffff" == r(code, data=0xffff)
	assert "-0xffff" == r(code, data=-0xffff)


@with_all_renderers
def test_function_oct(r):
	code = u"<?print oct(data)?>"

	with raises("oct.*unknown"):
		r(u"<?print oct()?>")
	with raises("oct.*unknown"):
		r(u"<?print oct(1, 2)?>")
	assert "0o0" == r(code, data=0)
	assert "0o77" == r(code, data=077)
	assert "0o7777" == r(code, data=07777)
	assert "-0o7777" == r(code, data=-07777)


@with_all_renderers
def test_function_bin(r):
	code = u"<?print bin(data)?>"

	with raises("bin.*unknown"):
		r(u"<?print bin()?>")
	with raises("bin.*unknown"):
		r(u"<?print bin(1, 2)?>")
	assert "0b0" == r(code, data=0)
	assert "0b11" == r(code, data=3)
	assert "-0b1111" == r(code, data=-15)


@with_all_renderers
def test_function_abs(r):
	code = u"<?print abs(data)?>"

	with raises("abs.*unknown"):
		r(u"<?print abs()?>")
	with raises("abs.*unknown"):
		r(u"<?print abs(1, 2)?>")
	assert "0" == r(code, data=0)
	assert "42" == r(code, data=42)
	assert "42" == r(code, data=-42)


@with_all_renderers
def test_function_sorted(r):
	code = u"<?for i in sorted(data)?><?print i?><?end for?>"

	with raises("sorted.*unknown"):
		r(u"<?print sorted()?>")
	with raises("sorted.*unknown"):
		r(u"<?print sorted(1, 2)?>")
	assert "gkru" == r(code, data="gurk")
	assert "24679" == r(code, data="92746")
	assert "012" == r(code, data={0: "zero", 1: "one", 2: "two"})


@with_all_renderers
def test_function_range(r):
	with raises("range.*unknown"):
		r(u"<?print range()?>")
	code = u"<?for i in range(data)?><?print i?><?end for?>"
	assert "" == r(code, data=-10)
	assert "" == r(code, data=0)
	assert "0" == r(code, data=1)
	assert "01234" == r(code, data=5)
	code = u"<?for i in range(data[0], data[1])?><?print i?><?end for?>"
	assert "" == r(code, data=[0, -10])
	assert "" == r(code, data=[0, 0])
	assert "01234" == r(code, data=[0, 5])
	assert "-5-4-3-2-101234" == r(code, data=[-5, 5])
	code = u"<?for i in range(data[0], data[1], data[2])?><?print i?><?end for?>"
	assert "" == r(code, data=[0, -10, 1])
	assert "" == r(code, data=[0, 0, 1])
	assert "02468" == r(code, data=[0, 10, 2])
	assert "" == r(code, data=[0, 10, -2])
	assert "108642" == r(code, data=[10, 0, -2])
	assert "" == r(code, data=[10, 0, 2])


@with_all_renderers
def test_function_zip(r):
	with raises("zip.*unknown"):
		r(u"<?print zip()?>")
	with raises("zip.*unknown"):
		r(u"<?print zip(1)?>")
	code = u"<?for (ix, iy) in zip(x, y)?><?print ix?>-<?print iy?>;<?end for?>"
	assert "" == r(code, x=[], y=[])
	assert "1-3;2-4;" == r(code, x=[1, 2], y=[3, 4])
	assert "1-4;2-5;" == r(code, x=[1, 2, 3], y=[4, 5])
	code = u"<?for (ix, iy, iz) in zip(x, y, z)?><?print ix?>-<?print iy?>+<?print iz?>;<?end for?>"
	assert "" == r(code, x=[], y=[], z=[])
	assert "1-3+5;2-4+6;" == r(code, x=[1, 2], y=[3, 4], z=[5, 6])
	assert "1-4+6;" == r(code, x=[1, 2, 3], y=[4, 5], z=[6])


@with_all_renderers
def test_function_type(r):
	code = u"<?print type(x)?>"

	with raises("type.*unknown"):
		r(u"<?print type()?>")
	with raises("type.*unknown"):
		r(u"<?print type(1, 2)?>")
	assert "none" == r(code, x=None)
	assert "bool" == r(code, x=False)
	assert "bool" == r(code, x=True)
	assert "int" == r(code, x=42)
	assert "int" == r(code, x=42L)
	assert "float" == r(code, x=4.2)
	assert "str" == r(code, x="foo")
	assert "str" == r(code, x=u"foo")
	assert "date" == r(code, x=datetime.datetime.now())
	assert "date" == r(code, x=datetime.date.today())
	assert "list" == r(code, x=(1, 2))
	assert "list" == r(code, x=[1, 2])
	assert "dict" == r(code, x={1: 2})
	assert "template" == r(code, x=ul4c.compile(""))
	assert "color" == r(code, x=color.red)


@with_all_renderers
def test_function_reversed(r):
	code = u"<?for i in reversed(x)?>(<?print i?>)<?end for?>"

	with raises("reversed.*unknown"):
		r(u"<?print reversed()?>")
	with raises("reversed.*unknown"):
		r(u"<?print reversed(1, 2)?>")
	assert "(3)(2)(1)" == r(code, x="123")
	assert "(3)(2)(1)" == r(code, x=[1, 2, 3])
	assert "(3)(2)(1)" == r(code, x=(1, 2, 3))


@with_all_renderers
def test_function_rgb(r):
	assert "#369" == r("<?print repr(rgb(0.2, 0.4, 0.6))?>")
	assert "#369c" == r("<?print repr(rgb(0.2, 0.4, 0.6, 0.8))?>")


@with_all_renderers
def test_function_hls(r):
	assert "#fff" == r("<?print repr(hls(0, 1, 0))?>")
	assert "#fff0" == r("<?print repr(hls(0, 1, 0, 0))?>")


@with_all_renderers
def test_function_hsv(r):
	assert "#fff" == r("<?print repr(hsv(0, 0, 1))?>")
	assert "#fff0" == r("<?print repr(hsv(0, 0, 1, 0))?>")


@with_all_renderers
def test_method_upper(r):
	assert "GURK" == r(u"<?print 'gurk'.upper()?>")


@with_all_renderers
def test_method_lower(r):
	assert "gurk" == r(u"<?print 'GURK'.lower()?>")


@with_all_renderers
def test_method_capitalize(r):
	assert "Gurk" == r(u"<?print 'gURK'.capitalize()?>")


@with_all_renderers
def test_method_startswith(r):
	assert "True" == r(u"<?print 'gurkhurz'.startswith('gurk')?>")
	assert "False" == r(u"<?print 'gurkhurz'.startswith('hurz')?>")


@with_all_renderers
def test_method_endswith(r):
	assert "True" == r(u"<?print 'gurkhurz'.endswith('hurz')?>")
	assert "False" == r(u"<?print 'gurkhurz'.endswith('gurk')?>")


@with_all_renderers
def test_method_strip(r):
	assert "gurk" == r(r"<?print ' \t\r\ngurk \t\r\n'.strip()?>")
	assert "gurk" == r(r"<?print 'xyzzygurkxyzzy'.strip('xyz')?>")


@with_all_renderers
def test_method_lstrip(r):
	assert "gurk \t\r\n" == r(ur"<?print ' \t\r\ngurk \t\r\n'.lstrip()?>")
	assert "gurkxyzzy" == r(ur"<?print 'xyzzygurkxyzzy'.lstrip('xyz')?>")


@with_all_renderers
def test_method_rstrip(r):
	assert " \t\r\ngurk" == r(ur"<?print ' \t\r\ngurk \t\r\n'.rstrip()?>")
	assert "xyzzygurk" == r(ur"<?print 'xyzzygurkxyzzy'.rstrip('xyz')?>")


@with_all_renderers
def test_method_split(r):
	assert "(g)(u)(r)(k)" == r(ur"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.split()?>(<?print item?>)<?end for?>")
	assert "(g)(u \t\r\nr \t\r\nk \t\r\n)" == r(ur"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.split(None, 1)?>(<?print item?>)<?end for?>")
	assert "()(g)(u)(r)(k)()" == r(ur"<?for item in 'xxgxxuxxrxxkxx'.split('xx')?>(<?print item?>)<?end for?>")
	assert "()(g)(uxxrxxkxx)" == r(ur"<?for item in 'xxgxxuxxrxxkxx'.split('xx', 2)?>(<?print item?>)<?end for?>")


@with_all_renderers
def test_method_rsplit(r):
	assert "(g)(u)(r)(k)" == r(ur"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.rsplit()?>(<?print item?>)<?end for?>")
	assert "( \t\r\ng \t\r\nu \t\r\nr)(k)" == r(ur"<?for item in ' \t\r\ng \t\r\nu \t\r\nr \t\r\nk \t\r\n'.rsplit(None, 1)?>(<?print item?>)<?end for?>")
	assert "()(g)(u)(r)(k)()" == r(ur"<?for item in 'xxgxxuxxrxxkxx'.rsplit('xx')?>(<?print item?>)<?end for?>")
	assert "(xxgxxuxxr)(k)()" == r(ur"<?for item in 'xxgxxuxxrxxkxx'.rsplit('xx', 2)?>(<?print item?>)<?end for?>")


@with_all_renderers
def test_method_replace(r):
	assert 'goork' == r(ur"<?print 'gurk'.replace('u', 'oo')?>")


@with_all_renderers
def test_method_render(r):
	t = ul4c.compile(u'(<?print data?>)')
	assert '(GURK)' == r(u"<?print t.render(data='gurk').upper()?>", t=t)
	assert '(GURK)' == r(u"<?print t.render(**{'data': 'gurk'}).upper()?>", t=t)

	t = ul4c.compile(u'(gurk)')
	assert '(GURK)' == r(u"<?print t.render().upper()?>", t=t)


@with_all_renderers
def test_method_format(r):
	t = datetime.datetime(2010, 11, 2, 12, 34, 56, 987000)
	format = "%Y-%m-%d %H:%M:%S.%f %a %A %b %B %% %I %j %p %U %w %W %y"
	assert t.strftime(format) == r(u"<?print data.format('{}')?>".format(format), data=t)


@with_all_renderers
def test_method_isoformat(r):
	t = datetime.datetime(2010, 02, 22, 12, 34, 56)
	assert 'Mon, 22 Feb 2010 12:34:56 GMT' == r(ur"<?print data.mimeformat()?>", data=t)


@with_all_renderers
def test_method_get(r):
	assert "42" == r(u"<?print {}.get('foo', 42)?>")
	assert "17" == r(u"<?print {'foo': 17}.get('foo', 42)?>")
	assert "" == r(u"<?print {}.get('foo')?>")
	assert "17" == r(u"<?print {'foo': 17}.get('foo')?>")


@with_all_renderers
def test_method_r_g_b_a(r):
	assert '0x11' == r(u'<?code c = #123?><?print hex(c.r())?>')
	assert '0x22' == r(u'<?code c = #123?><?print hex(c.g())?>')
	assert '0x33' == r(u'<?code c = #123?><?print hex(c.b())?>')
	assert '0xff' == r(u'<?code c = #123?><?print hex(c.a())?>')


@with_all_renderers
def test_method_hls(r):
	assert '0' == r(u'<?code c = #fff?><?print int(c.hls()[0])?>')
	assert '1' == r(u'<?code c = #fff?><?print int(c.hls()[1])?>')
	assert '0' == r(u'<?code c = #fff?><?print int(c.hls()[2])?>')


@with_all_renderers
def test_method_hlsa(r):
	assert '0' == r(u'<?code c = #fff?><?print int(c.hlsa()[0])?>')
	assert '1' == r(u'<?code c = #fff?><?print int(c.hlsa()[1])?>')
	assert '0' == r(u'<?code c = #fff?><?print int(c.hlsa()[2])?>')
	assert '1' == r(u'<?code c = #fff?><?print int(c.hlsa()[3])?>')


@with_all_renderers
def test_method_hsv(r):
	assert '0' == r(u'<?code c = #fff?><?print int(c.hsv()[0])?>')
	assert '0' == r(u'<?code c = #fff?><?print int(c.hsv()[1])?>')
	assert '1' == r(u'<?code c = #fff?><?print int(c.hsv()[2])?>')


@with_all_renderers
def test_method_hsva(r):
	assert '0' == r(u'<?code c = #fff?><?print int(c.hsva()[0])?>')
	assert '0' == r(u'<?code c = #fff?><?print int(c.hsva()[1])?>')
	assert '1' == r(u'<?code c = #fff?><?print int(c.hsva()[2])?>')
	assert '1' == r(u'<?code c = #fff?><?print int(c.hsva()[3])?>')


@with_all_renderers
def test_method_lum(r):
	assert 'True' == r(u'<?print #fff.lum() == 1?>')


@with_all_renderers
def test_method_withlum(r):
	assert '#fff' == r(u'<?print #000.withlum(1)?>')


@with_all_renderers
def test_method_witha(r):
	assert '#0063a82a' == r(u'<?print repr(#0063a8.witha(42))?>')


@with_all_renderers
def test_method_join(r):
	assert '1,2,3,4' == r(u'<?print ",".join("1234")?>')
	assert '1,2,3,4' == r(u'<?print ",".join([1, 2, 3, 4])?>')


@with_all_renderers
def test_method_find(r):
	assert '-1' == r(u'<?print s.find("ks")?>', s="gurkgurk")
	assert '2' == r(u'<?print s.find("rk")?>', s="gurkgurk")
	assert '2' == r(u'<?print s.find("rk", 2)?>', s="gurkgurk")
	assert '2' == r(u'<?print s.find("rk", 2, 4)?>', s="gurkgurk")
	assert '6' == r(u'<?print s.find("rk", 4, 8)?>', s="gurkgurk")
	assert '-1' == r(u'<?print s.find("rk", 2, 3)?>', s="gurkgurk")
	assert '-1' == r(u'<?print s.find("rk", 7)?>', s="gurkgurk")


@with_all_renderers
def test_method_rfind(r):
	assert '-1' == r(u'<?print s.rfind("ks")?>', s="gurkgurk")
	assert '6' == r(u'<?print s.rfind("rk")?>', s="gurkgurk")
	assert '6' == r(u'<?print s.rfind("rk", 2)?>', s="gurkgurk")
	assert '2' == r(u'<?print s.rfind("rk", 2, 4)?>', s="gurkgurk")
	assert '6' == r(u'<?print s.rfind("rk", 4, 8)?>', s="gurkgurk")
	assert '-1' == r(u'<?print s.rfind("rk", 2, 3)?>', s="gurkgurk")
	assert '-1' == r(u'<?print s.rfind("rk", 7)?>', s="gurkgurk")


@with_all_renderers
def test_method_day(r):
	assert '12' == r(u'<?print @2010-05-12T.day()?>')
	assert '12' == r(u'<?print d.day()?>', d=datetime.date(2010, 5, 12))


@with_all_renderers
def test_method_month(r):
	assert '5' == r(u'<?print @2010-05-12T.month()?>')
	assert '5' == r(u'<?print d.month()?>', d=datetime.date(2010, 5, 12))


@with_all_renderers
def test_method_year(r):
	assert '5' == r(u'<?print @2010-05-12T.month()?>')
	assert '5' == r(u'<?print d.month()?>', d=datetime.date(2010, 5, 12))


@with_all_renderers
def test_method_hour(r):
	assert '16' == r(u'<?print @2010-05-12T16:47:56.hour()?>')
	assert '16' == r(u'<?print d.hour()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@with_all_renderers
def test_method_minute(r):
	assert '47' == r(u'<?print @2010-05-12T16:47:56.minute()?>')
	assert '47' == r(u'<?print d.minute()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@with_all_renderers
def test_method_second(r):
	assert '56' == r(u'<?print @2010-05-12T16:47:56.second()?>')
	assert '56' == r(u'<?print d.second()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@with_all_renderers
def test_method_microsecond(r):
	assert '123000' == r(u'<?print @2010-05-12T16:47:56.123000.microsecond()?>')
	assert '123000' == r(u'<?print d.microsecond()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56, 123000))


@with_all_renderers
def test_method_weekday(r):
	assert '2' == r(u'<?print @2010-05-12T.weekday()?>')
	assert '2' == r(u'<?print d.weekday()?>', d=datetime.date(2010, 5, 12))


@with_all_renderers
def test_method_yearday(r):
	assert '1' == r(u'<?print @2010-01-01T.yearday()?>')
	assert '366' == r(u'<?print @2008-12-31T.yearday()?>')
	assert '365' == r(u'<?print @2010-12-31T.yearday()?>')
	assert '132' == r(u'<?print @2010-05-12T.yearday()?>')
	assert '132' == r(u'<?print @2010-05-12T16:47:56.yearday()?>')
	assert '132' == r(u'<?print d.yearday()?>', d=datetime.date(2010, 5, 12))
	assert '132' == r(u'<?print d.yearday()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@with_all_renderers
def test_render(r):
	t = ul4c.compile(u'<?print prefix?><?print data?><?print suffix?>')
	assert '(f)(o)(o)' == r(u'<?for c in data?><?render t(data=c, prefix="(", suffix=")")?><?end for?>', t=t, data='foo')
	assert '(f)(o)(o)' == r(u'<?for c in data?><?render t(data=c, **{"prefix": "(", "suffix": ")"})?><?end for?>', t=t, data='foo')


@with_all_renderers
def test_render_var(r):
	t = ul4c.compile(u'<?code x += 1?><?print x?>')
	assert '42,43,42' == r(u'<?print x?>,<?render t(x=x)?>,<?print x?>', t=t, x=42)


@with_all_renderers
def test_def(r):
	assert 'foo' == r(u'<?def lower?><?print x.lower()?><?end def?><?print lower.render(x="FOO")?>')


@with_all_renderers
def test_parse(r):
	assert '42' == r(u'<?print data.Noner?>', data=dict(Noner=42))


@with_all_renderers
def test_nested_exceptions(r):
	tmpl1 = ul4c.compile(u"<?print 2*x?>")
	tmpl2 = ul4c.compile(u"<?render tmpl1(x=x)?>")
	tmpl3 = ul4c.compile(u"<?render tmpl2(tmpl1=tmpl1, x=x)?>")

	if r is not renderjs:
		msg = "TypeError .*render tmpl3.*render tmpl2.*render tmpl1.*print 2.*unsupported operand type"
		with raises(msg):
			r(u"<?render tmpl3(tmpl1=tmpl1, tmpl2=tmpl2, x=x)?>", tmpl1=tmpl1, tmpl2=tmpl2, tmpl3=tmpl3, x=None)


@with_all_renderers
def test_note(r):
	assert "foo" == r(u"f<?note This is?>o<?note a comment?>o")


@with_all_renderers
def test_templateattributes(r):
	if r is not renderjs:
		s = "<?print x?>"
		t = ul4c.compile(s)
		assert "<?" == r(u"<?print template.startdelim?>", template=t)
		assert "?>" == r(u"<?print template.enddelim?>", template=t)
		assert s == r(u"<?print template.source?>", template=t)
		assert "2" == r(u"<?print len(template.opcodes)?>", template=t)
		assert "loadvar" == r(u"<?print template.opcodes[0].code?>", template=t)
		assert "0" == r(u"<?print template.opcodes[0].r1?>", template=t)
		assert "" == r(u"<?print template.opcodes[0].r2?>", template=t)
		assert "x" == r(u"<?print template.opcodes[0].arg?>", template=t)
		assert s == r(u"<?code loc = template.opcodes[0].location?><?print template.source[loc.starttag:loc.endtag]?>", template=t)
		assert "x" == r(u"<?code loc = template.opcodes[0].location?><?print template.source[loc.startcode:loc.endcode]?>", template=t)


def universaltemplate():
	return ul4c.compile("""
		text
		<?code x = 'gurk'?>
		<?code x = 42?>
		<?code x = 4.2?>
		<?code x = None?>
		<?code x = False?>
		<?code x = True?>
		<?code x = @2009-01-04T?>
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


def test_jssource():
	t = universaltemplate()
	t.jssource()


def test_javasource():
	t = universaltemplate()
	t.javasource()
