#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of Living Logic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVING LOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVING LOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Contains everthing related to options in XIST.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys
import os
import types

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

def getANSICodesFromEnv(name, default):
	"""
	parses an environment variable from a color code tuple and returns it or
	the default if the environment variable can't be found or parsed.
	"""
	try:
		var = eval(os.environ[name])
	except:
		return default
	return var

retrieveremote = getIntFromEnv("XSC_RETRIEVEREMOTE", 1)                                 # should remote URLs be retrieved? (for filesize and imagesize tests)
retrievelocal = getIntFromEnv("XSC_RETRIEVELOCAL", 1)                                   # should local URLs be retrieved? (for filesize and imagesize tests)
repransi = getIntFromEnv("XSC_REPRANSI", 0)                                             # should ANSI escape sequences be used for dumping the DOM tree and which ones? (0=off, 1=dark background, 2=light background)
reprtab = getStringFromEnv("XSC_REPRTAB", "  ")                                         # how to represent an indentation in the DOM tree?
repransitab = getANSICodesFromEnv("XSC_REPRANSI_TAB", (0x8, 0x8))                       # ANSI escape sequence to be used for tabs
repransiquote = getANSICodesFromEnv("XSC_REPRANSI_QUOTE", (0xa, 0xf))                   # ANSI escape sequence to be used for quotes (delimiters for text and attribute nodes)
repransislash = getANSICodesFromEnv("XSC_REPRANSI_SLASH", (0x7, 0xf))                   # ANSI escape sequence to be used for slashes in element names
repransibracket = getANSICodesFromEnv("XSC_REPRANSI_BRACKET", (0xa, 0xf))               # ANSI escape sequence to be used for brackets (delimiters for tags)
repransicolon = getANSICodesFromEnv("XSC_REPRANSI_COLON", (0xa, 0xf))                   # ANSI escape sequence to be used for colon (i.e. namespace separator)
repransiquestion = getANSICodesFromEnv("XSC_REPRANSI_QUESTION", (0xa, 0xf))             # ANSI escape sequence to be used for question marks (delimiters for processing instructions)
repransiexclamation = getANSICodesFromEnv("XSC_REPRANSI_EXCLAMATION", (0xa, 0xf))       # ANSI escape sequence to be used for exclamation marks (used in comments and doctypes)
repransitext = getANSICodesFromEnv("XSC_REPRANSI_TEXT", (0x7, 0x7))                     # ANSI escape sequence to be used for text
repransicharref = getANSICodesFromEnv("XSC_REPRANSI_CHARREF", (0xf, 0x5))               # ANSI escape sequence to be used for character references
repransinamespace = getANSICodesFromEnv("XSC_REPRANSI_NAMESPACE", (0xf, 0x4))           # ANSI escape sequence to be used for namespaces
repransielementname = getANSICodesFromEnv("XSC_REPRANSI_ELEMENTNAME", (0xe, 0xc))       # ANSI escape sequence to be used for element names
repransientityname = getANSICodesFromEnv("XSC_REPRANSI_ENTITYNAME", (0xf, 0xc))         # ANSI escape sequence to be used for entity names
repransiattrname = getANSICodesFromEnv("XSC_REPRANSI_ATTRNAME", (0xf, 0xc))             # ANSI escape sequence to be used for attribute names
repransidoctypemarker = getANSICodesFromEnv("XSC_REPRANSI_DOCTYPEMARKER", (0xf, 0xf))   # ANSI escape sequence to be used for document types marker (i.e. !DOCTYPE)
repransidoctypetext = getANSICodesFromEnv("XSC_REPRANSI_DOCTYPETEXT", (0x7, 0x7))       # ANSI escape sequence to be used for document types
repransicommentmarker = getANSICodesFromEnv("XSC_REPRANSI_COMMENTMARKER", (0x7, 0xf))   # ANSI escape sequence to be used for comment markers (i.e. --)
repransicommenttext = getANSICodesFromEnv("XSC_REPRANSI_COMMENTTEXT", (0x7, 0x7))       # ANSI escape sequence to be used for comment text
repransiattrvalue = getANSICodesFromEnv("XSC_REPRANSI_ATTRVALUE", (0x7, 0x6))           # ANSI escape sequence to be used for attribute values
repransiurl = getANSICodesFromEnv("XSC_REPRANSI_URL", (0xb, 0x2))                       # ANSI escape sequence to be used for URLs
repransiprocinsttarget = getANSICodesFromEnv("XSC_REPRANSI_PROCINSTTARGET", (0x9, 0x9)) # ANSI escape sequence to be used for processing instruction targets
repransiprocinstdata = getANSICodesFromEnv("XSC_REPRANSI_PROCINSTDATA", (0x7, 0x7))     # ANSI escape sequence to be used for processing instruction data
outputXHTML = getIntFromEnv("XSC_OUTPUT_XHTML", 1)                                      # XHTML output format (0 = plain HTML, 1 = HTML compatible XHTML, 2 = pure XHTML)
outputEncoding = getStringFromEnv("XSC_OUTPUT_ENCODING", "us-ascii")                    # Encoding to be used in publish() (and asBytes())
reprEncoding = sys.getdefaultencoding()
