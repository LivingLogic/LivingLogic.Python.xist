#!/usr/bin/env python

# Setup script for the XIST Web Publishing System

__version__ = "$Revision$"[11:-2]
# $Source$

from distutils.core import setup

setup(name = "XIST",
      version = "0.1.0",
      description = "Extensible Site Publishing Toolkit",
      author = "Walter Dörwald",
      author_email = "walter@bnbt.de",
      #url = "http://www.catsystems.de/xsc/",
      licence = "Python",
      packages = ['xist']
     )
