#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Setup script for XIST

__version__ = tuple(map(int,"$Revision$"[11:-2].split(".")))
# $Source$

from distutils.core import setup, Extension

setup(
	name="XIST",
	version="2.1",
	description="An XML-based extensible HTML generator",
	long_description=\
		"XIST is an XML based extensible HTML generator. XIST is also\n"
		"a DOM parser (built on top of SAX2) with a very simple and\n"
		"pythonesque tree API. Every XML element type corresponds to a\n"
		"Python class and these Python classes provide a conversion method\n"
		"to transform the XML tree (e.g. into HTML). XIST can be considered\n"
		"'object oriented XSL'.",
	author="Walter Doerwald",
	author_email="walter@livinglogic.de",
	url="http://www.livinglogic.de/Python/xist/",
	license="Python",
	packages=["ll", "ll.xist", "ll.xist.ns"],
	package_dir={"ll": ".", "ll.xist": "_xist"},
	ext_modules=[
		Extension("ll.xist.csstokenizer", ["_xist/csstokenizer.cxx"]),
		Extension("ll.xist.helpers", ["_xist/helpers.c"])
	],
	scripts=["scripts/dtd2xsc.py", "scripts/tld2xsc.py", "scripts/doc2txt.py", "scripts/xscmake.py" ]
)
