#! /usr/bin/env python

## Copyright 2000 by Living Logic AG, Bayreuth, Germany.
## Copyright 2000 by Walter Dörwald
##
## See the file LICENSE for licensing details

"""
Contains everthing related to options in XIST.
"""

__version__ = "$Revision$"[11:-2]
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
	parses an environment variable from a string list and returns it or
	the default if the environment variable can't be found or parsed.
	"""
	try:
		var = eval(os.environ[name])
	except:
		return default
	if type(var) is types.StringType:
		var = [var, var]
	return var

retrieveremote = getIntFromEnv("XSC_RETRIEVEREMOTE", 1)                                       # should remote URLs be retrieved? (for filesize and imagesize tests)
retrievelocal = getIntFromEnv("XSC_RETRIEVELOCAL", 1)                                         # should local URLs be retrieved? (for filesize and imagesize tests)
repransi = getIntFromEnv("XSC_REPRANSI", 0)                                                   # should ANSI escape sequences be used for dumping the DOM tree and which ones? (0=off, 1=dark background, 2=light background)
reprtab = getStringFromEnv("XSC_REPRTAB", "  ")                                               # how to represent an indentation in the DOM tree?
repransitab = getANSICodesFromEnv("XSC_REPRANSI_TAB", ["1;30", "37"])                         # ANSI escape sequence to be used for tabs
repransiquote = getANSICodesFromEnv("XSC_REPRANSI_QUOTE", ["1;32", "1;32"])                   # ANSI escape sequence to be used for quotes (delimiters for text and attribute nodes)
repransislash = getANSICodesFromEnv("XSC_REPRANSI_SLASH", ["", ""])                           # ANSI escape sequence to be used for slashes in element names
repransibracket = getANSICodesFromEnv("XSC_REPRANSI_BRACKET", ["1;32", "32"])                 # ANSI escape sequence to be used for brackets (delimiters for tags)
repransicolon = getANSICodesFromEnv("XSC_REPRANSI_COLON", ["1;32", "1;32"])                   # ANSI escape sequence to be used for colon (i.e. namespace separator)
repransiquestion = getANSICodesFromEnv("XSC_REPRANSI_QUESTION", ["1;32", "1;32"])             # ANSI escape sequence to be used for question marks (delimiters for processing instructions)
repransiexclamation = getANSICodesFromEnv("XSC_REPRANSI_EXCLAMATION", ["1;32", "1;32"])       # ANSI escape sequence to be used for exclamation marks (used in comments and doctypes)
repransitext = getANSICodesFromEnv("XSC_REPRANSI_TEXT", ["", ""])                             # ANSI escape sequence to be used for text
repransicharref = getANSICodesFromEnv("XSC_REPRANSI_CHARREF", ["1;37", "34"])                 # ANSI escape sequence to be used for character references
repransinamespace = getANSICodesFromEnv("XSC_REPRANSI_NAMESPACE", ["1;37", "36"])             # ANSI escape sequence to be used for namespaces
repransielementname = getANSICodesFromEnv("XSC_REPRANSI_ELEMENTNAME", ["1;36", "34"])         # ANSI escape sequence to be used for element names
repransientityname = getANSICodesFromEnv("XSC_REPRANSI_ENTITYNAME", ["1;37", "35"])           # ANSI escape sequence to be used for entity names
repransiattrname = getANSICodesFromEnv("XSC_REPRANSI_ATTRNAME", ["1;36", "36"])               # ANSI escape sequence to be used for attribute names
repransidoctypemarker = getANSICodesFromEnv("XSC_REPRANSI_DOCTYPEMARKER", ["1", "1"])         # ANSI escape sequence to be used for document types marker (i.e. !DOCTYPE)
repransidoctypetext = getANSICodesFromEnv("XSC_REPRANSI_DOCTYPETEXT", ["", ""])               # ANSI escape sequence to be used for document types
repransicommentmarker = getANSICodesFromEnv("XSC_REPRANSI_COMMENTMARKER", ["", ""])           # ANSI escape sequence to be used for comment markers (i.e. --)
repransicommenttext = getANSICodesFromEnv("XSC_REPRANSI_COMMENTTEXT", ["", ""])               # ANSI escape sequence to be used for comment text
repransiattrvalue = getANSICodesFromEnv("XSC_REPRANSI_ATTRVALUE", ["", "36"])                 # ANSI escape sequence to be used for attribute values
repransiurl = getANSICodesFromEnv("XSC_REPRANSI_URL", ["1;33", "1;34"])                       # ANSI escape sequence to be used for URLs
repransiprocinsttarget = getANSICodesFromEnv("XSC_REPRANSI_PROCINSTTARGET", ["1;31", "1;31"]) # ANSI escape sequence to be used for processing instruction targets
repransiprocinstdata = getANSICodesFromEnv("XSC_REPRANSI_PROCINSTDATA", ["", ""])             # ANSI escape sequence to be used for processing instruction data
outputXHTML = getIntFromEnv("XSC_OUTPUT_XHTML", 1)                                            # XHTML output format (0 = plain HTML, 1 = HTML compatible XHTML, 2 = pure XHTML)
outputEncoding = getStringFromEnv("XSC_OUTPUT_ENCODING", "us-ascii")                          # Encoding to be used in publish() (and asBytes())
