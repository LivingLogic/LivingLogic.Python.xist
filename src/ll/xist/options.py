# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
Contains everthing related to options in &xist; (apart for syntax highlighting
which can be found in presenters.py).
"""


import sys, os


__docformat__ = "xist"


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


repransi = getenvint("LL_XIST_REPRANSI", 0)  # should ANSI escape sequences be used for dumping the DOM tree and which ones? (0=off, 1=dark background, 2=light background)
reprtab = getenvstr("LL_XIST_REPR_TAB", u"  ") # how to represent an indentation in the DOM tree?
reprencoding = sys.getdefaultencoding()

server = "localhost" # Host for server relative URLs
