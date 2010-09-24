#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2007-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 2007-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import py.test

from ll import url
from ll.xist import xsc
from ll.xist.ns import detox


class defblock(xsc.Element):
	class Attrs(xsc.Element.Attrs):
		class func(xsc.TextAttr): pass

	def convert(self, converter):
		e = xsc.Frag(
			detox.def_(self.attrs.func),
				self.content,
			detox.end(u"def")
		)
		return e.convert(converter)


class forblock(xsc.Element):
	class Attrs(xsc.Element.Attrs):
		class loop(xsc.TextAttr): pass

	def convert(self, converter):
		e = xsc.Frag(
			detox.for_(self.attrs.loop),
				self.content,
			detox.end(u"for")
		)
		return e.convert(converter)


class whileblock(xsc.Element):
	class Attrs(xsc.Element.Attrs):
		class loop(xsc.TextAttr): pass

	def convert(self, converter):
		e = xsc.Frag(
			detox.while_(self.attrs.loop),
				self.content,
			detox.end(u"while")
		)
		return e.convert(converter)


def makemod(node):
	return detox.xml2mod(node.conv().string())


def makeoutput(node, function, *args, **kwargs):
	mod = makemod(node)
	return u"".join(getattr(mod, function)(*args, **kwargs))


def test_modulecode():
	assert makemod(detox.code(u"x = 42")).x == 42


def test_text():
	with xsc.build():
		with xsc.Frag() as e:
			+detox.def_(u"gurk()")
			+xsc.Text(u"foo")
			+detox.end(u"def")
	assert makeoutput(e, u"gurk") == u"foo"


def test_expr():
	with xsc.build():
		with xsc.Frag() as e:
			with defblock(func=u"gurk(arg)"):
				+detox.expr(u"arg")

	assert makeoutput(e, u"gurk", u"hurz") == u"hurz"


def test_for():
	with xsc.build():
		with xsc.Frag() as e:
			with defblock(func=u"gurk(arg)"):
				with forblock(loop=u"i in xrange(arg)"):
					+detox.expr(u"str(i)")

	assert makeoutput(e, u"gurk", 3) == u"012"


def test_if():
	with xsc.build():
		with xsc.Frag() as e:
			with defblock(func=u"gurk(arg)"):
				+detox.if_(u"arg>2")
				+detox.expr(u"str(2*arg)")
				+detox.else_()
				+detox.expr(u"str(3*arg)")
				+detox.end(u"if")

	assert makeoutput(e, u"gurk", 0) == u"0"
	assert makeoutput(e, u"gurk", 1) == u"3"
	assert makeoutput(e, u"gurk", 2) == u"6"
	assert makeoutput(e, u"gurk", 3) == u"6"
	assert makeoutput(e, u"gurk", 4) == u"8"


def test_while():
	with xsc.build():
		with xsc.Frag() as e:
			with defblock(func=u"gurk(arg)"):
				+detox.code(u"i = 0")
				with whileblock(loop=u"i < arg"):
					+detox.expr(u"str(i)")
					+detox.code(u"i += 1")

	assert makeoutput(e, u"gurk", 3) == u"012"


def test_scopecheck():
	with xsc.build():
		with xsc.Frag() as e:
			+detox.def_(u"gurk()")
			+xsc.Text(u"hurz")
			+detox.end()

	assert makeoutput(e, u"gurk") == u"hurz"

	with xsc.build():
		with xsc.Frag() as e:
			+detox.def_(u"gurk()")
			+xsc.Text(u"hurz")
			+detox.end(u"for")

	with py.test.raises(SyntaxError):
		makeoutput(e, u"gurk")


def test_textexpr():
	with xsc.build():
		with xsc.Frag() as e:
			with defblock(func=u"gurk()"):
				+detox.code(u"""s = '"a" < "b" & "b" > "a"'""")
				+detox.textexpr(u"s")

	assert makeoutput(e, u"gurk") == u'&quot;a&quot; &lt; &quot;b&quot; &amp; &quot;b&quot; &gt; &quot;a&quot;'
