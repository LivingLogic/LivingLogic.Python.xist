#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Contains everthing related to options in XIST (apart for syntax highlighting
which can be found in presenters.py).
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys, os

def getStringFromEnv(name, default):
	try:
		return os.environ[name]
	except:
		return default

def getIntFromEnv(name, default):
	try:
		return int(os.environ[name])
	except:
		return default

retrieveremote = getIntFromEnv("XSC_RETRIEVEREMOTE", 1)              # should remote URLs be retrieved? (for filesize and imagesize tests)
retrievelocal = getIntFromEnv("XSC_RETRIEVELOCAL", 1)                # should local URLs be retrieved? (for filesize and imagesize tests)
repransi = getIntFromEnv("XSC_REPRANSI", 0)                          # should ANSI escape sequences be used for dumping the DOM tree and which ones? (0=off, 1=dark background, 2=light background)
reprtab = getStringFromEnv("XSC_REPRTAB", "  ")                      # how to represent an indentation in the DOM tree?
outputXHTML = getIntFromEnv("XSC_OUTPUT_XHTML", 1)                   # XHTML output format (0 = plain HTML, 1 = HTML compatible XHTML, 2 = pure XHTML)
outputEncoding = getStringFromEnv("XSC_OUTPUT_ENCODING", "us-ascii") # Encoding to be used in publish() (and asBytes())
reprEncoding = sys.getdefaultencoding()

server = "localhost" # Host for server relative URLs
