#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Setup script for XIST

__version__ = tuple(map(int,"$Revision$"[11:-2].split(".")))
# $Source$

from distutils.core import setup, Extension

DESCRIPTION = """
XIST is an XML based extensible HTML generator. XIST is also
a DOM parser (built on top of SAX2) with a very simple and
pythonesque tree API. Every XML element type corresponds to a
Python class and these Python classes provide a conversion method
to transform the XML tree (e.g. into HTML). XIST can be considered
'object oriented XSL'.
"""

CLASSIFIERS="""
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Intended Audience :: Developers
License :: OSI Approved :: Python License (CNRI Python License)
Operating System :: OS Independent
Programming Language :: Python
Topic :: Internet :: WWW/HTTP :: Dynamic Content
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Text Processing :: Markup :: HTML
Topic :: Text Processing :: Markup :: XML
"""

KEYWORDS = """
XML
HTML
XHTML
XSLT
HSC
XSL-FO
SVG
WML
iHTML
"""

setup(
	name="ll-XIST",
	version="2.2",
	description="An XML-based extensible HTML generator",
	long_description=DESCRIPTION.strip(),
	author="Walter Doerwald",
	author_email="walter@livinglogic.de",
	url="http://www.livinglogic.de/Python/xist/",
	#download_url="http://www.livinglogic.de/Python/xist/Download.html",
	license="Python",
	classifiers=CLASSIFIERS.strip().split("\n"),
	keywords=",".join(KEYWORDS.strip().split("\n")),
	packages=["ll", "ll.xist", "ll.xist.ns", "ll.xist.tools"],
	package_dir={"ll": ".", "ll.xist": "_xist"},
	ext_modules=[
		Extension("ll.xist.csstokenizer", ["_xist/csstokenizer.cxx"]),
		Extension("ll.xist.helpers", ["_xist/helpers.c"])
	],
	scripts=["scripts/dtd2xsc.py", "scripts/tld2xsc.py", "scripts/doc2txt.py", "scripts/xscmake.py" ]
)
