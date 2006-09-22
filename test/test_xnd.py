#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2006 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


from ll.xist import xsc, xnd, sims


def xnd2ns(data):
	mod = {"__name__": str(data.name)}
	encoding = "iso-8859-1"
	code = data.aspy(encoding=encoding, asmod=False).encode(encoding)
	exec code in mod

	return mod["__ns__"]


def test_procinst():
	e = xnd.Namespace("ns")(
		xnd.ProcInst("foo", doc="gurk")
	)
	ns = xnd2ns(e)
	assert issubclass(ns.foo, xsc.ProcInst)
	assert ns.foo.__doc__.strip() == "gurk"

	e = xnd.Namespace("ns")(
		xnd.ProcInst("f-o-o")
	)
	ns = xnd2ns(e)
	assert issubclass(ns.f_o_o, xsc.ProcInst)
	assert ns.f_o_o.xmlname == "f-o-o"


def test_entity():
	e = xnd.Namespace("ns")(
		xnd.Entity("foo", doc="gurk")
	)
	ns = xnd2ns(e)
	assert issubclass(ns.foo, xsc.Entity)
	assert ns.foo.__doc__.strip() == "gurk"

	e = xnd.Namespace("ns")(
		xnd.Entity("f-o-o")
	)
	ns = xnd2ns(e)
	assert issubclass(ns.f_o_o, xsc.Entity)
	assert ns.f_o_o.xmlname == "f-o-o"


def test_charref():
	e = xnd.Namespace("ns")(
		xnd.CharRef("foo", doc="gurk", codepoint=0x3042)
	)
	ns = xnd2ns(e)
	assert issubclass(ns.foo, xsc.CharRef)
	assert ns.foo.__doc__.strip() == "gurk"
	assert ns.foo.codepoint == 0x3042

	e = xnd.Namespace("ns")(
		xnd.CharRef("f-o-o", codepoint=0x3042)
	)
	ns = xnd2ns(e)
	assert issubclass(ns.f_o_o, xsc.CharRef)
	assert ns.f_o_o.xmlname == "f-o-o"


def test_model():
	e = xnd.Namespace("ns")(
		xnd.Element("foo", modeltype=True)
	)
	ns = xnd2ns(e)
	assert isinstance(ns.foo.model, sims.Any)

	e = xnd.Namespace("ns")(
		xnd.Element("foo", modeltype=False)
	)
	ns = xnd2ns(e)
	assert isinstance(ns.foo.model, sims.Empty)
