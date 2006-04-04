#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Setup script for XIST

__version__ = tuple(map(int,"$Revision$"[11:-2].split(".")))
# $Source$

from distutils.core import setup, Extension
import textwrap

DESCRIPTION = """
XIST is an extensible HTML and XML generator. XIST is also a DOM parser
(built on top of SAX2) with a very simple and pythonesque tree API.
Every XML element type corresponds to a Python class and these Python
classes provide a conversion method to transform the XML tree
(e.g. into HTML). XIST can be considered 'object oriented XSLT'.
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
Relax NG
"""

DESCRIPTION = "\n".join(textwrap.wrap(DESCRIPTION.strip(), width=64, replace_whitespace=True))

setup(
	name="ll-xist",
	version="2.13",
	description="An extensible HTML/XML generator",
	long_description=DESCRIPTION,
	author=u"Walter Dörwald",
	author_email="walter@livinglogic.de",
	url="http://www.livinglogic.de/Python/xist/",
	download_url="http://www.livinglogic.de/Python/xist/Download.html",
	license="Python",
	classifiers=CLASSIFIERS.strip().splitlines(),
	keywords=",".join(KEYWORDS.strip().splitlines()),
	packages=["ll.xist", "ll.xist.ns"],
	package_dir={"ll.xist": "_xist"},
	ext_modules=[
		Extension("ll.xist.csstokenizer", ["_xist/csstokenizer.cxx"]),
		Extension("ll.xist.helpers", ["_xist/helpers.c"])
	],
	scripts=[
		"scripts/dtd2xsc.py",
		"scripts/tld2xsc.py",
		"scripts/doc2txt.py",
		"scripts/xml2xsc.py",
	]
)
