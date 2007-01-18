#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Setup script for XIST

__version__ = tuple(map(int,"$Revision$"[11:-2].split(".")))
# $Source$


try:
	import setuptools as tools
except ImportError:
	from distutils import core as tools

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


args = dict(
	name="ll-xist",
	version="2.15.2",
	description="An extensible HTML/XML generator",
	long_description=DESCRIPTION,
	author="Walter Doerwald",
	author_email="walter@livinglogic.de",
	url="http://www.livinglogic.de/Python/xist/",
	download_url="http://www.livinglogic.de/Python/xist/Download.html",
	license="Python",
	classifiers=CLASSIFIERS.strip().splitlines(),
	keywords=",".join(KEYWORDS.strip().splitlines()),
	package_dir={"": "src"},
	packages=["ll", "ll.xist", "ll.xist.ns", "ll.xist.scripts"],
	ext_modules=[
		tools.Extension("ll.xist.csstokenizer", ["src/ll/xist/csstokenizer.cxx"]),
		tools.Extension("ll.xist.helpers", ["src/ll/xist/helpers.c"]),
		tools.Extension("ll.xist.sgmlop", ["src/ll/xist/sgmlop.c"])
	],
	entry_points=dict(
		console_scripts=[
			"dtd2xsc = ll.xist.scripts.dtd2xsc:main",
			"tld2xsc = ll.xist.scripts.tld2xsc:main",
			"doc2txt = ll.xist.scripts.doc2txt:main",
			"xml2xsc = ll.xist.scripts.xml2xsc:main",
		]
	),
	scripts=[
		"scripts/dtd2xsc.py",
		"scripts/tld2xsc.py",
		"scripts/doc2txt.py",
		"scripts/xml2xsc.py",
	],
	install_requires=[
		"ll-core >= 1.5",
		"PyXML >= 0.8.4",
	],
	namespace_packages=["ll"],
	zip_safe=False,
	dependency_links=[
		"http://sourceforge.net/project/showfiles.php?group_id=6473", # PyXML
	],
)


if __name__ == "__main__":
	tools.setup(**args)
