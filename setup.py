#!/usr/bin/env python

# Setup script for XIST

__version__ = "$Revision$"[11:-2]
# $Source$

from distutils.core import setup

setup(name = "XIST",
      version = "0.3.6",
      description = "XML based extensible HTML generator",
      author = "Walter D�rwald",
      author_email = "walter@livinglogic.de",
      #url = "http://www.catsystems.de/xsc/",
      licence = "Python",
      packages = ['xist']
     )
