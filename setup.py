#!/usr/bin/env python

# Setup script for XIST

__version__ = tuple(map(int,"$Revision$"[11:-2].split(".")))
# $Source$

from distutils.core import setup, Extension

setup(
	name = "XIST",
	version = "1.1",
	description = "An XML-based extensible HTML generator",
	author = "Walter Dörwald",
	author_email = "walter@livinglogic.de",
	url = "http://www.livinglogic.de/Python/xist/",
	licence = "Python",
	packages = ['xist', 'xist.ns'],
	package_dir = {"xist": "_xist"},
	ext_modules = [Extension("xist.helpers", ["_xist/helpers.c"])],
	scripts = ["scripts/dtd2xsc.py", "scripts/dbl2txt.py", "scripts/xscmake.py" ]
)
