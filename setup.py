#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Setup script for XIST


try:
	import setuptools as tools
except ImportError:
	from distutils import core as tools

import textwrap


DESCRIPTION = """
XIST is an extensible HTML and XML generator. XIST is also a XML parser with a
very simple and pythonesque tree API. Every XML element type corresponds to a
Python class and these Python classes provide a conversion method to transform
the XML tree (e.g. into HTML). XIST can be considered 'object oriented XSLT'.
"""

CLASSIFIERS="""
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Intended Audience :: Developers
License :: OSI Approved :: MIT License
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

try:
	news = list(open("NEWS.rst", "r"))
except IOError:
	description = DESCRIPTION.strip()
else:
	underlines = [i for (i, line) in enumerate(news) if line.startswith("---")]
	news = news[underlines[0]-1:underlines[1]-1]
	news = "".join(news)
	description = "%s\n\n\n%s" % (DESCRIPTION.strip(), news)


args = dict(
	name="ll-xist",
	version="3.0",
	description="An extensible HTML/XML generator",
	long_description=description,
	author="Walter Doerwald",
	author_email="walter@livinglogic.de",
	url="http://www.livinglogic.de/Python/xist/",
	download_url="http://www.livinglogic.de/Python/xist/Download.html",
	license="MIT",
	classifiers=CLASSIFIERS.strip().splitlines(),
	keywords=",".join(KEYWORDS.strip().splitlines()),
	package_dir={"": "src"},
	packages=["ll", "ll.xist", "ll.xist.ns", "ll.xist.scripts"],
	ext_modules=[
		tools.Extension("ll.xist.helpers", ["src/ll/xist/helpers.c"]),
		tools.Extension("ll.xist.sgmlop", ["src/ll/xist/sgmlop.c"], define_macros=[("SGMLOP_UNICODE_SUPPORT", None)]),
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
		"ll-core >= 1.11",
		"cssutils == 0.9.4b1",
	],
	namespace_packages=["ll"],
	zip_safe=False,
)


if __name__ == "__main__":
	tools.setup(**args)
