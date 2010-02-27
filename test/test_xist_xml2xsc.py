#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2007-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 2007-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import cStringIO, types

from ll.xist import xsc, sims
from ll.xist.scripts import xml2xsc

try:
	import lxml
except ImportError:
	parser = "etree"
else:
	parser = "lxml"


def xml2mod(s, parser="etree", sims="simple"):
	with xsc.Pool():
		xnd = xml2xsc.stream2xnd(cStringIO.StringIO(s), parser=parser, sims=sims)

		code = xnd.aspy().encode()
		code = compile(code, "test.py", "exec")

		mod = types.ModuleType("test")
		mod.__file__ = "test.py"
		exec code in mod.__dict__
		return mod


def test_basics():
	xml = "<foo><bar/><?baz gurk?></foo>"
	mod = xml2mod(xml, parser=parser)

	assert issubclass(mod.foo, xsc.Element)
	assert isinstance(mod.foo.model, sims.Any)
	assert issubclass(mod.bar, xsc.Element)
	assert isinstance(mod.bar.model, sims.Empty)
	if parser == "lxml":
		assert issubclass(mod.baz, xsc.ProcInst)


def test_attrs():
	xml = "<foo a='1'><foo b='2'/></foo>"
	mod = xml2mod(xml, parser=parser)

	assert set(a.xmlname for a in mod.foo.Attrs.allowedattrs()) == set("ab")


def test_model1():
	xml = "<foo><foo/><bar><foo/></bar></foo>"
	mod = xml2mod(xml, parser=parser, sims="full")

	assert mod.foo in mod.foo.model.elements
	assert mod.bar in mod.foo.model.elements
	assert mod.foo in mod.bar.model.elements
	assert mod.bar not in mod.bar.model.elements


def test_model2():
	xml = "<foo><bar>gurk<bar/></bar><baz><!--nix--><baz/></baz></foo>"
	mod = xml2mod(xml, parser=parser, sims="full")

	assert isinstance(mod.foo.model, sims.Elements)
	assert isinstance(mod.bar.model, sims.ElementsOrText)
	assert isinstance(mod.baz.model, sims.Elements) # Comments don't count as content
