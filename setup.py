#!/usr/bin/env python

# Setup script for XIST

__version__ = "$Revision$"[11:-2]
# $Source$

from distutils.core import setup

setup(name = "XIST",
      version = "0.3.8",
      description = "An XML based extensible HTML generator",
      author = "Walter Dörwald",
      author_email = "walter@livinglogic.de",
      #url = "http://www.catsystems.de/xsc/",
      licence = "Python",
      packages = ['xist']
     )
