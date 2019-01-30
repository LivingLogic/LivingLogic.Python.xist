#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import types

import pytest

from ll.xist import xsc, xnd, sims
from ll.xist.scripts import dtd2xsc


def dtd2mod(s, shareattrs=None, **kwargs):
	xnd = dtd2xsc.urls2xnd([s], encoding="utf-8", model="fullonce", **kwargs)

	if shareattrs is not None:
		xnd.shareattrs(shareattrs)

	mod = types.ModuleType("test")
	mod.__file__ = "test.py"

	code = str(xnd)
	print("Module source generated from DTDs:")
	print(code)
	code = compile(code, "test.py", "exec")
	exec(code, mod.__dict__)
	return mod


@pytest.mark.lxml
def test_convert():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo (bar+)>
	<!ATTLIST foo
		id    ID    #IMPLIED
		xmlns CDATA #FIXED "http://xmlns.foo.com/foo"
	>
	<!ELEMENT bar EMPTY>
	<!ATTLIST bar
		bar1 CDATA               #REQUIRED
		bar2 (bar2)              #IMPLIED
		bar3 (bar3a|bar3b|bar3c) #IMPLIED
		bar-4 (bar-4a|bar-4b)    #IMPLIED
		bar_4 (bar_4a|bar_4b)    #IMPLIED
		bar_42 (bar_42a|bar_42b) #IMPLIED
		class CDATA              #IMPLIED
		foo:bar CDATA            #IMPLIED
	>
	"""
	ns = dtd2mod(dtdstring)

	assert ns.foo.xmlns == "http://xmlns.foo.com/foo"
	assert isinstance(ns.foo.model, sims.Elements)
	assert len(ns.foo.model.elements) == 1
	assert ns.foo.model.elements[0] == ns.bar
	assert issubclass(ns.foo.Attrs.id, xsc.IDAttr)
	assert "xmlns" not in ns.foo.Attrs
	assert isinstance(ns.bar.model, sims.Empty)

	assert "bar" not in ns.bar.Attrs

	assert issubclass(ns.bar.Attrs.bar1, xsc.TextAttr)
	assert ns.bar.Attrs.bar1.required is True

	assert issubclass(ns.bar.Attrs.bar2, xsc.BoolAttr)
	assert ns.bar.Attrs.bar2.required is False

	assert issubclass(ns.bar.Attrs.bar3, xsc.TextAttr)
	assert ns.bar.Attrs.bar3.required is False
	assert ns.bar.Attrs.bar3.values == ("bar3a", "bar3b", "bar3c")

	# Attributes are alphabetically sorted
	assert issubclass(ns.bar.Attrs.bar_4, xsc.TextAttr)
	assert ns.bar.Attrs.bar_4.xmlname == "bar-4"
	assert ns.bar.Attrs.bar_4.values == ("bar-4a", "bar-4b")

	assert issubclass(ns.bar.Attrs.bar_42, xsc.TextAttr)
	assert ns.bar.Attrs.bar_42.xmlname == "bar_4"
	assert ns.bar.Attrs.bar_42.values == ("bar_4a", "bar_4b")

	assert issubclass(ns.bar.Attrs.bar_422, xsc.TextAttr)
	assert ns.bar.Attrs.bar_422.xmlname == "bar_42"
	assert ns.bar.Attrs.bar_422.values == ("bar_42a", "bar_42b")


@pytest.mark.lxml
def test_charref():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo EMPTY>
	<!ENTITY bar "&#xff;">
	"""
	ns = dtd2mod(dtdstring)

	assert ns.bar.codepoint == 0xff


@pytest.mark.lxml
def test_keyword():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo EMPTY>
	<!ATTLIST foo
		class CDATA              #IMPLIED
	>
	"""
	ns = dtd2mod(dtdstring)
	assert issubclass(ns.foo.Attrs.class_, xsc.TextAttr)
	assert ns.foo.Attrs.class_.__name__ == "class_"
	assert ns.foo.Attrs.class_.xmlname == "class"


@pytest.mark.lxml
def test_quotes():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo EMPTY>
	"""
	ns = dtd2mod(dtdstring, defaultxmlns='"')
	assert ns.foo.xmlns == '"'


@pytest.mark.lxml
def test_unicode():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo EMPTY>
	"""
	ns = dtd2mod(dtdstring, defaultxmlns='\u3042')
	assert ns.foo.xmlns == '\u3042'


@pytest.mark.lxml
def test_unicodequotes():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo EMPTY>
	"""
	ns = dtd2mod(dtdstring, defaultxmlns='"\u3042"')
	assert ns.foo.xmlns == '"\u3042"'


@pytest.mark.lxml
def test_badelementname():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT class EMPTY>
	"""
	ns = dtd2mod(dtdstring)
	assert issubclass(ns.class_, xsc.Element)


@pytest.mark.lxml
def test_shareattrsnone():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo (bar)>
	<!ATTLIST foo
		baz CDATA              #IMPLIED
	>
	<!ELEMENT bar EMPTY>
	<!ATTLIST bar
		baz CDATA              #IMPLIED
	>
	"""
	ns = dtd2mod(dtdstring, shareattrs=None)
	assert not hasattr(ns, "baz")


@pytest.mark.lxml
def test_shareattrsdupes():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo (bar)>
	<!ATTLIST foo
		baz  CDATA             #IMPLIED
		baz2 CDATA             #IMPLIED
	>
	<!ELEMENT bar EMPTY>
	<!ATTLIST bar
		baz  CDATA             #IMPLIED
		baz2 CDATA             #REQUIRED
	>
	"""
	ns = dtd2mod(dtdstring, shareattrs=False)
	assert issubclass(ns.foo.Attrs.baz, ns.baz.baz)
	assert issubclass(ns.bar.Attrs.baz, ns.baz.baz)
	assert not hasattr(ns, "baz2")
	assert not ns.foo.Attrs.baz2.required
	assert ns.bar.Attrs.baz2.required


@pytest.mark.lxml
def test_shareattrsall():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo (bar)>
	<!ATTLIST foo
		baz  CDATA             #IMPLIED
		bazz CDATA             #IMPLIED
	>
	<!ELEMENT bar EMPTY>
	<!ATTLIST bar
		baz  CDATA             #IMPLIED
		bazz CDATA             #REQUIRED
	>
	"""
	ns = dtd2mod(dtdstring, shareattrs=True)
	assert issubclass(ns.foo.Attrs.baz, ns.baz.baz)
	assert issubclass(ns.bar.Attrs.baz, ns.baz.baz)

	assert not ns.foo.Attrs.bazz.required
	assert ns.bar.Attrs.bazz.required
