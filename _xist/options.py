#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
Contains everthing related to options in XIST (apart for syntax highlighting
which can be found in presenters.py).
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, os


def getenvstr(name, default):
	try:
		return os.environ[name]
	except:
		return default


def getenvint(name, default):
	try:
		return int(os.environ[name])
	except:
		return default


retrieveremote = getenvint("XSC_RETRIEVEREMOTE", 1)           # should remote URLs be retrieved? (for filesize and imagesize tests)
retrievelocal = getenvint("XSC_RETRIEVELOCAL", 1)             # should local URLs be retrieved? (for filesize and imagesize tests)
repransi = getenvint("XSC_REPRANSI", 0)                       # should ANSI escape sequences be used for dumping the DOM tree and which ones? (0=off, 1=dark background, 2=light background)
reprtab = getenvstr("XSC_REPRTAB", "  ")                      # how to represent an indentation in the DOM tree?
outputXHTML = getenvint("XSC_OUTPUT_XHTML", 1)                # XHTML output format (0 = plain HTML, 1 = HTML compatible XHTML, 2 = pure XHTML)
outputEncoding = getenvstr("XSC_OUTPUT_ENCODING", "us-ascii") # Encoding to be used in publish() (and asBytes())
reprEncoding = sys.getdefaultencoding()

server = "localhost" # Host for server relative URLs
