#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Setup script for XIST


try:
	import setuptools as tools
except ImportError:
	from distutils import core as tools

import textwrap, re


DESCRIPTION = """
XIST provides an extensible HTML and XML generator. XIST is also a XML parser
with a very simple and pythonesque tree API. Every XML element type corresponds
to a Python class and these Python classes provide a conversion method to
transform the XML tree (e.g. into HTML). XIST can be considered
'object oriented XSLT'.

XIST also includes the following modules and packages:

*	:mod:`ll.make` is an object oriented make replacement. Like make it allows
	you to specify dependencies between files and actions to be executed
	when files don't exist or are out of date with respect to one
	of their sources. But unlike make you can do this in a object oriented
	way and targets are not only limited to files.

*	:mod:`ll.url` provides classes for parsing and constructing RFC 2396
	compliant URLs.

*	:mod:`ll.orasql` provides utilities for working with cx_Oracle_:

	-	It allows calling functions and procedures with keyword arguments.

	-	Query results will be put into Record objects, where database fields
		are accessible as object attributes.

	-	The :class:`Connection` class provides methods for iterating through the
		database metadata.

	-	Importing the modules adds support for URLs with the scheme ``oracle`` to
		:mod:`ll.url`.

	.. _cx_Oracle: http://cx-oracle.sourceforge.net/

*	:mod:`ll.ul4c` is compiler for a templating language with similar capabilities
	to `Django's templating language`__. ``UL4`` templates are compiled to an
	internal bytecode format, which makes it possible to implement template
	renderers in other languages and makes the template code "secure" (i.e.
	template code can't open or delete files).

	__ http://www.djangoproject.com/documentation/templates/

*	:mod:`ll.astyle` can be used for colored terminal output (via ANSI escape
	sequences).

*	:mod:`ll.color` provides classes and functions for handling RGB color values.
	This includes the ability to convert between different color models
	(RGB, HSV, HLS) as well as to and from CSS format, and several functions
	for modifying and mixing colors.

*	:mod:`ll.misc` provides several small utility functions and classes.

*	:mod:`ll.sisyphus` provides classes for running Python scripts as cron jobs.

*	:mod:`ll.daemon` can be used on UNIX to fork a daemon process.

*	:mod:`ll.xml_codec` contains a complete codec for encoding and decoding XML.

*	:mod:`ll.nightshade` can be used to serve the output of PL/SQL
	functions/procedures with CherryPy__.

__ http://www.cherrypy.org/
"""

CLASSIFIERS = """
# Common
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules

# ansistyle
Topic :: Terminals
Topic :: Text Processing :: General

# color
Topic :: Multimedia :: Graphics

# make
Topic :: Software Development :: Build Tools

# daemon
Environment :: No Input/Output (Daemon)
Operating System :: POSIX

# url
Topic :: Internet
Topic :: Internet :: File Transfer Protocol (FTP)
Topic :: Internet :: WWW/HTTP

# ul4
Topic :: Internet :: WWW/HTTP :: Dynamic Content
Topic :: Text Processing :: General

# xml_codec
Topic :: Text Processing :: Markup :: XML

# XIST
Environment :: Web Environment
Topic :: Internet :: WWW/HTTP :: Dynamic Content
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Text Processing :: Markup :: HTML
Topic :: Text Processing :: Markup :: XML

# TOXIC
Topic :: Database

# orasql
Topic :: Database
"""

KEYWORDS = """
# misc
property
decorator
iterator

# ansistyle
ANSI
escape sequence
color
terminal

# color
color
RGB
HSV
HSB
HLS
CSS

# make
make
build

# sisyphus
cron
job

# daemon
daemon
UNIX
fork

# url
URL
RFC 2396
HTTP
FTP
ssh
py.execnet

# xml_codec
XML
codec

# XIST
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

# TOXIC
Oracle
user defined function
PL/SQL
XML
HTML
processing instruction
PI

# ul4
template
templating language

# orasql
Oracle
cx_Oracle
record
procedure
schema

# nightshade
CherryPy
toxic
Oracle
PL/SQL
"""

try:
	news = list(open("NEWS.rst", "r"))
except IOError:
	description = DESCRIPTION.strip()
else:
	# Extract the first section (which are the changes for the current version)
	underlines = [i for (i, line) in enumerate(news) if line.startswith("---")]
	news = news[underlines[0]-1:underlines[1]-1]
	news = "".join(news)
	descr = "%s\n\n\n%s" % (DESCRIPTION.strip(), news)

	# Get rid of text roles PyPI doesn't know about
	descr = re.subn(":[a-z]+:`([a-zA-Z0-9_.]+)`", "``\\1``", descr)[0]

	# Expand tabs (so they won't show up as 8 spaces in the Windows installer)
	descr = descr.expandtabs(2)

args = dict(
	name="ll-xist",
	version="3.7.4",
	description="Extensible HTML/XML generator, cross-platform templating language, Oracle utilities and various other tools",
	long_description=descr,
	author="Walter Doerwald",
	author_email="walter@livinglogic.de",
	url="http://www.livinglogic.de/Python/xist/",
	download_url="http://www.livinglogic.de/Python/Download.html#xist",
	license="MIT",
	classifiers=sorted(set(c for c in CLASSIFIERS.strip().splitlines() if c.strip() and not c.strip().startswith("#"))),
	keywords=", ".join(sorted(set(k.strip() for k in KEYWORDS.strip().splitlines() if k.strip() and not k.strip().startswith("#")))),
	package_dir={"": "src"},
	packages=["ll", "ll.scripts", "ll.xist", "ll.xist.ns", "ll.xist.scripts", "ll.orasql", "ll.orasql.scripts"],
	ext_modules=[
		tools.Extension("ll._url", ["src/ll/_url.c"]),
		tools.Extension("ll._ansistyle", ["src/ll/_ansistyle.c"]),
		tools.Extension("ll._misc", ["src/ll/_misc.c", "src/ll/_misc_include.c"]),
		tools.Extension("ll._xml_codec", ["src/ll/_xml_codec.c", "src/ll/_xml_codec_include.c"]),
		tools.Extension("ll.xist.sgmlop", ["src/ll/xist/sgmlop.c"], define_macros=[("SGMLOP_UNICODE_SUPPORT", None)]),
	],
	entry_points=dict(
		console_scripts=[
			"uls = ll.scripts.uls:main",
			"ucp = ll.scripts.ucp:main",
			"ucat = ll.scripts.ucat:main",
			"db2ul4 = ll.scripts.db2ul4:main",
			"dtd2xsc = ll.xist.scripts.dtd2xsc:main",
			"tld2xsc = ll.xist.scripts.tld2xsc:main",
			"doc2txt = ll.xist.scripts.doc2txt:main",
			"xml2xsc = ll.xist.scripts.xml2xsc:main",
			"oracreate = ll.orasql.scripts.oracreate:main [oracle]",
			"oradrop = ll.orasql.scripts.oradrop:main [oracle]",
			"oradelete = ll.orasql.scripts.oradelete:main [oracle]",
			"oradiff = ll.orasql.scripts.oradiff:main [oracle]",
			"oramerge = ll.orasql.scripts.oramerge:main [oracle]",
			"oragrant = ll.orasql.scripts.oragrant:main [oracle]",
			"orafind = ll.orasql.scripts.orafind:main [oracle]",
		]
	),
	scripts=[
		"scripts/uls.py",
		"scripts/ucp.py",
		"scripts/ucat.py",
		"scripts/db2ul4.py",
		"scripts/dtd2xsc.py",
		"scripts/tld2xsc.py",
		"scripts/doc2txt.py",
		"scripts/xml2xsc.py",
		"scripts/oracreate.py",
		"scripts/oradrop.py",
		"scripts/oradelete.py",
		"scripts/oradiff.py",
		"scripts/oramerge.py",
		"scripts/oragrant.py",
		"scripts/orafind.py",
	],
	install_requires=[
		"cssutils == 0.9.5.1",
	],
	extras_require = {
		"oracle":  ["cx_Oracle >= 5.0.1"],
	},
	namespace_packages=["ll"],
	zip_safe=False,
	dependency_links=[
		"http://cx-oracle.sourceforge.net/", # cx_Oracle
	],
)


if __name__ == "__main__":
	tools.setup(**args)
