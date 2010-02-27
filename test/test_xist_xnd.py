#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import types

from ll.xist import xsc, xnd, sims


xmlns = "http://xmlns.example.com/"


def xnd2ns(data):
	with xsc.Pool(): # don't pollute the defaultpool
		mod = types.ModuleType("test")
		mod.__file__ = "test.py"
		encoding = "iso-8859-1"
		code = data.aspy(encoding=encoding).encode(encoding)
		print code
		code = compile(code, "test.py", "exec")
		exec code in mod.__dict__
		return mod


def test_xmlns():
	e = xnd.Module(xmlns)()
	ns = xnd2ns(e)
	assert ns.xsc is xsc


def test_element():
	e = xnd.Module(xmlns)(
		xnd.Element("foo", xmlns="http://xmlns.foo.com"),
		xnd.Element("foo", xmlns="http://xmlns.foo2.com"),
	)
	ns = xnd2ns(e)
	assert ns.foo.xmlname == "foo"
	assert ns.foo.xmlns == "http://xmlns.foo.com"
	assert ns.foo2.xmlname == "foo"
	assert ns.foo2.xmlns == "http://xmlns.foo2.com"


def test_procinst():
	e = xnd.Module(xmlns)(
		xnd.ProcInst("foo", doc="gurk")
	)
	ns = xnd2ns(e)

	assert issubclass(ns.foo, xsc.ProcInst)
	assert ns.foo.__doc__.strip() == "gurk"

	e = xnd.Module(xmlns)(
		xnd.ProcInst("f-o-o")
	)
	ns = xnd2ns(e)
	assert issubclass(ns.f_o_o, xsc.ProcInst)
	assert ns.f_o_o.xmlname == "f-o-o"


def test_entity():
	e = xnd.Module(xmlns)(
		xnd.Entity("foo", doc="gurk")
	)
	ns = xnd2ns(e)
	assert issubclass(ns.foo, xsc.Entity)
	assert ns.foo.__doc__.strip() == "gurk"

	e = xnd.Module(xmlns)(
		xnd.Entity("f-o-o")
	)
	ns = xnd2ns(e)
	assert issubclass(ns.f_o_o, xsc.Entity)
	assert ns.f_o_o.xmlname == "f-o-o"


def test_charref():
	e = xnd.Module(xmlns)(
		xnd.CharRef("foo", doc="gurk", codepoint=0x3042)
	)
	ns = xnd2ns(e)
	assert issubclass(ns.foo, xsc.CharRef)
	assert ns.foo.__doc__.strip() == "gurk"
	assert ns.foo.codepoint == 0x3042

	e = xnd.Module(xmlns)(
		xnd.CharRef("f-o-o", codepoint=0x3042)
	)
	ns = xnd2ns(e)
	assert issubclass(ns.f_o_o, xsc.CharRef)
	assert ns.f_o_o.xmlname == "f-o-o"


def test_model():
	e = xnd.Module(xmlns)(
		xnd.Element("foo", modeltype=True)
	)
	ns = xnd2ns(e)
	assert isinstance(ns.foo.model, sims.Any)

	e = xnd.Module(xmlns)(
		xnd.Element("foo", modeltype=False)
	)
	ns = xnd2ns(e)
	assert isinstance(ns.foo.model, sims.Empty)
