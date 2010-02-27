#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import types, cStringIO

from ll.xist import xsc, parsers, sims
from ll.xist.ns import tld
from ll.xist.scripts import tld2xsc


def tld2ns(s, shareattrs=None):
	xnd = tld2xsc.tld2xnd(cStringIO.StringIO(s), shareattrs=shareattrs)

	mod = types.ModuleType("test")
	mod.__file__ = "test.py"
	encoding = "iso-8859-1"
	code = xnd.aspy(encoding=encoding).encode(encoding)
	code = compile(code, "test.py", "exec")
	exec code in mod.__dict__
	return mod


def test_tld2xsc():
	xmlns = "http://xmlns.example.com/foo"

	tldstring = """<?xml version="1.0" encoding="ISO-8859-1"?>
	<!DOCTYPE taglib PUBLIC "-//Sun Microsystems, Inc.//DTD JSP Tag Library 1.1//EN" "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd">
	<taglib>
		<tlibversion>1.0</tlibversion>
		<jspversion>1.1</jspversion>
		<shortname>foo</shortname>
		<info>just a test</info>
		<uri>%s</uri>
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
	""" % xmlns
	ns = tld2ns(tldstring)
	assert ns.bar.xmlns == xmlns
	assert ns.__doc__.strip() == "just a test"
	assert ns.bar.xmlname == u"bar"
	assert isinstance(ns.bar.model, sims.Empty)
	assert ns.bar.__doc__.strip() == "info"

	assert issubclass(ns.bar.Attrs.name, xsc.TextAttr)
	assert ns.bar.Attrs.name.required is True

	assert issubclass(ns.bar.Attrs.response, xsc.TextAttr)
	assert ns.bar.Attrs.response.required is False
