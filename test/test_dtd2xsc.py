#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


from ll.xist import xsc, xnd, sims


def dtd2ns(s, xmlname, xmlurl=None, shareattrs=None):
	from xml.parsers.xmlproc import dtdparser

	dtd = dtdparser.load_dtd_string(s)
	data = xnd.fromdtd(dtd, xmlname=xmlname, xmlurl=xmlurl)

	if shareattrs is not None:
		data.shareattrs(shareattrs)

	mod = {"__name__": xmlname}
	encoding = "iso-8859-1"
	code = data.aspy(encoding=encoding, asmod=False).encode(encoding)
	exec code in mod

	return mod["__ns__"]


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
	ns = dtd2ns(dtdstring, "foo")

	assert issubclass(ns, xsc.Namespace)
	assert ns.xmlname == "foo"
	assert ns.xmlurl == "http://xmlns.foo.com/foo"
	assert isinstance(ns.foo.model, sims.Elements)
	assert len(ns.foo.model.elements) == 1
	assert ns.foo.model.elements[0] == ns.bar
	assert issubclass(ns.foo.Attrs.id, xsc.IDAttr)
	assert "xmlns" not in ns.foo.Attrs
	assert isinstance(ns.bar.model, sims.Empty)

	assert "bar" not in ns.bar.Attrs

	assert issubclass(ns.bar.Attrs.bar1, xsc.TextAttr)
	assert ns.bar.Attrs.bar1.required == True

	assert issubclass(ns.bar.Attrs.bar2, xsc.BoolAttr)
	assert ns.bar.Attrs.bar2.required == False

	assert issubclass(ns.bar.Attrs.bar3, xsc.TextAttr)
	assert ns.bar.Attrs.bar3.required == False
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


def test_charref():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo (EMPTY)>
	<!ENTITY bar "&#xff;">
	"""
	ns = dtd2ns(dtdstring, "foo")

	assert ns.bar.codepoint == 0xff


def test_keyword():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo EMPTY>
	<!ATTLIST foo
		class CDATA              #IMPLIED
	>
	"""
	ns = dtd2ns(dtdstring, "foo")
	assert issubclass(ns.foo.Attrs.class_, xsc.TextAttr)
	assert ns.foo.Attrs.class_.__name__ == "class_"
	assert ns.foo.Attrs.class_.xmlname == u"class"


def test_quotes():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo EMPTY>
	"""
	ns = dtd2ns(dtdstring, "foo", xmlurl='"')
	assert ns.xmlurl == '"'


def test_unicode():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo EMPTY>
	"""
	ns = dtd2ns(dtdstring, "foo", xmlurl=u'\u3042')
	assert ns.xmlurl == u'\u3042'


def test_unicodequotes():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT foo EMPTY>
	"""
	ns = dtd2ns(dtdstring, "foo", xmlurl=u'"\u3042"')
	assert ns.xmlurl == u'"\u3042"'


def test_badelementname():
	dtdstring = """<?xml version='1.0' encoding='us-ascii'?>
	<!ELEMENT class EMPTY>
	"""
	ns = dtd2ns(dtdstring, "foo")
	assert issubclass(ns.class_, xsc.Element)


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
	ns = dtd2ns(dtdstring, "foo", shareattrs=None)
	assert not hasattr(ns, "baz")


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
	ns = dtd2ns(dtdstring, "foo", shareattrs=False)
	assert issubclass(ns.foo.Attrs.baz, ns.baz.baz)
	assert issubclass(ns.bar.Attrs.baz, ns.baz.baz)
	assert not hasattr(ns, "baz2")
	assert not ns.foo.Attrs.baz2.required
	assert ns.bar.Attrs.baz2.required


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
	ns = dtd2ns(dtdstring, "foo", shareattrs=True)
	assert issubclass(ns.foo.Attrs.baz, ns.baz.baz)
	assert issubclass(ns.bar.Attrs.baz, ns.baz.baz)

	assert ns.foo.Attrs.bazz.__bases__[0] is not xsc.TextAttr
	assert ns.bar.Attrs.bazz.__bases__[0] is not xsc.TextAttr
	assert ns.foo.Attrs.bazz.__bases__ != ns.bar.Attrs.bazz.__bases__

	assert not ns.foo.Attrs.bazz.required
	assert ns.bar.Attrs.bazz.required
