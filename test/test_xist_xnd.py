#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2011 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2011 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import types

from ll.xist import xsc, xnd, sims


xmlns = "http://xmlns.example.com/"


def xnd2ns(data):
	with xsc.Pool(): # don't pollute the defaultpool
		code = str(data)
		code = compile(code, "test.py", "exec")
		mod = types.ModuleType("test")
		mod.__file__ = "test.py"
		exec code in mod.__dict__
		return mod


def test_xmlns():
	ns = xnd.Module(xmlns)
	ns = xnd2ns(ns)
	assert ns.xsc is xsc


def test_element():
	ns = xnd.Module()
	ns += xnd.Element("foo", xmlns="http://xmlns.foo.com")
	ns += xnd.Element("foo", xmlns="http://xmlns.foo2.com")
	ns = xnd2ns(ns)
	assert ns.foo.xmlname == "foo"
	assert ns.foo.xmlns == "http://xmlns.foo.com"
	assert ns.foo2.xmlname == "foo"
	assert ns.foo2.xmlns == "http://xmlns.foo2.com"


def test_procinst():
	ns = xnd.Module()
	ns += xnd.ProcInst("foo", doc="gurk")
	ns = xnd2ns(ns)

	assert issubclass(ns.foo, xsc.ProcInst)
	assert ns.foo.__doc__.strip() == "gurk"

	ns = xnd.Module(xmlns)
	ns += xnd.ProcInst("f-o-o")
	ns = xnd2ns(ns)
	assert issubclass(ns.f_o_o, xsc.ProcInst)
	assert ns.f_o_o.xmlname == "f-o-o"


def test_entity():
	ns = xnd.Module()
	ns += xnd.Entity("foo", doc="gurk")
	ns = xnd2ns(ns)
	assert issubclass(ns.foo, xsc.Entity)
	assert ns.foo.__doc__.strip() == "gurk"

	ns = xnd.Module()
	ns += xnd.Entity("f-o-o")
	ns = xnd2ns(ns)
	assert issubclass(ns.f_o_o, xsc.Entity)
	assert ns.f_o_o.xmlname == "f-o-o"


def test_charref():
	ns = xnd.Module()
	ns += xnd.CharRef("foo", doc="gurk", codepoint=0x3042)
	ns = xnd2ns(ns)
	assert issubclass(ns.foo, xsc.CharRef)
	assert ns.foo.__doc__.strip() == "gurk"
	assert ns.foo.codepoint == 0x3042

	ns = xnd.Module()
	ns += xnd.CharRef("f-o-o", codepoint=0x3042)
	ns = xnd2ns(ns)
	assert issubclass(ns.f_o_o, xsc.CharRef)
	assert ns.f_o_o.xmlname == "f-o-o"


def test_model():
	ns = xnd.Module(xmlns)
	ns += xnd.Element("foo", modeltype=True)
	ns = xnd2ns(ns)
	assert isinstance(ns.foo.model, sims.Any)

	ns = xnd.Module()
	ns += xnd.Element("foo", modeltype=False)
	ns = xnd2ns(ns)
	assert isinstance(ns.foo.model, sims.Empty)
