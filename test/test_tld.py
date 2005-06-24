#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


from ll.xist import xsc, parsers, sims
from ll.xist.ns import tld


def tld2ns(s, xmlname, shareattrs=None):
	node = parsers.parseString(s, prefixes=xsc.Prefixes(tld))
	node = node.walknode(xsc.FindType(tld.taglib))[0]

	data = node.asxnd()

	if shareattrs is not None:
		data.shareattrs(shareattrs)

	mod = {"__name__": xmlname}
	encoding = "iso-8859-1"
	code = data.aspy(encoding=encoding, asmod=False).encode(encoding)
	exec code in mod

	return mod["__ns__"]


def test_tld2xsc():
	tldstring = """<?xml version="1.0" encoding="ISO-8859-1"?>
	<!DOCTYPE taglib PUBLIC "-//Sun Microsystems, Inc.//DTD JSP Tag Library 1.1//EN" "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd">
	<taglib>
		<tlibversion>1.0</tlibversion>
		<jspversion>1.1</jspversion>
		<shortname>foo</shortname>
		<tag>
			<name>bar</name>
			<tagclass>com.foo.bar</tagclass>
			<bodycontent>empty</bodycontent>
			<info>info</info>
			<attribute>
				<name>name</name>
				<required>true</required>
				<rtexprvalue>true</rtexprvalue>
			</attribute>
			<attribute>
				<name>response</name>
				<required>false</required>
				<rtexprvalue>true</rtexprvalue>
			</attribute>
			<attribute>
				<name>controllerElement</name>
				<required>false</required>
				<rtexprvalue>true</rtexprvalue>
			</attribute>
			<attribute>
				<name>type</name>
				<required>false</required>
				<rtexprvalue>true</rtexprvalue>
			</attribute>
		</tag>
	</taglib>
	"""
	ns = tld2ns(tldstring, "foo")
	assert ns.xmlname == u"foo"
	assert ns.bar.xmlname == u"bar"
	assert isinstance(ns.bar.model, sims.Empty)
	assert ns.bar.__doc__.strip() == "info"

	assert issubclass(ns.bar.Attrs.name, xsc.TextAttr)
	assert ns.bar.Attrs.name.required is True

	assert issubclass(ns.bar.Attrs.response, xsc.TextAttr)
	assert ns.bar.Attrs.response.required is False
