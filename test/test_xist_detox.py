#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2007-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2007-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import pytest

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
			detox.end("def")
		)
		return e.convert(converter)


class forblock(xsc.Element):
	class Attrs(xsc.Element.Attrs):
		class loop(xsc.TextAttr): pass

	def convert(self, converter):
		e = xsc.Frag(
			detox.for_(self.attrs.loop),
				self.content,
			detox.end("for")
		)
		return e.convert(converter)


class whileblock(xsc.Element):
	class Attrs(xsc.Element.Attrs):
		class loop(xsc.TextAttr): pass

	def convert(self, converter):
		e = xsc.Frag(
			detox.while_(self.attrs.loop),
				self.content,
			detox.end("while")
		)
		return e.convert(converter)


def makemod(node):
	return detox.xml2mod(node.conv().string())


def makeoutput(node, function, *args, **kwargs):
	mod = makemod(node)
	return "".join(getattr(mod, function)(*args, **kwargs))


def test_modulecode():
	assert makemod(detox.code("x = 42")).x == 42


def test_text():
	with xsc.build():
		with xsc.Frag() as e:
			+detox.def_("gurk()")
			+xsc.Text("foo")
			+detox.end("def")
	assert makeoutput(e, "gurk") == "foo"


def test_expr():
	with xsc.build():
		with xsc.Frag() as e:
			with defblock(func="gurk(arg)"):
				+detox.expr("arg")

	assert makeoutput(e, "gurk", "hurz") == "hurz"


def test_for():
	with xsc.build():
		with xsc.Frag() as e:
			with defblock(func="gurk(arg)"):
				with forblock(loop="i in range(arg)"):
					+detox.expr("str(i)")

	assert makeoutput(e, "gurk", 3) == "012"


def test_if():
	with xsc.build():
		with xsc.Frag() as e:
			with defblock(func="gurk(arg)"):
				+detox.if_("arg>2")
				+detox.expr("str(2*arg)")
				+detox.else_()
				+detox.expr("str(3*arg)")
				+detox.end("if")

	assert makeoutput(e, "gurk", 0) == "0"
	assert makeoutput(e, "gurk", 1) == "3"
	assert makeoutput(e, "gurk", 2) == "6"
	assert makeoutput(e, "gurk", 3) == "6"
	assert makeoutput(e, "gurk", 4) == "8"


def test_while():
	with xsc.build():
		with xsc.Frag() as e:
			with defblock(func="gurk(arg)"):
				+detox.code("i = 0")
				with whileblock(loop="i < arg"):
					+detox.expr("str(i)")
					+detox.code("i += 1")

	assert makeoutput(e, "gurk", 3) == "012"


def test_scopecheck():
	with xsc.build():
		with xsc.Frag() as e:
			+detox.def_("gurk()")
			+xsc.Text("hurz")
			+detox.end()

	assert makeoutput(e, "gurk") == "hurz"

	with xsc.build():
		with xsc.Frag() as e:
			+detox.def_("gurk()")
			+xsc.Text("hurz")
			+detox.end("for")

	with pytest.raises(SyntaxError):
		makeoutput(e, "gurk")


def test_textexpr():
	with xsc.build():
		with xsc.Frag() as e:
			with defblock(func="gurk()"):
				+detox.code("""s = '"a" < "b" & "b" > "a"'""")
				+detox.textexpr("s")

	assert makeoutput(e, "gurk") == '&quot;a&quot; &lt; &quot;b&quot; &amp; &quot;b&quot; &gt; &quot;a&quot;'
