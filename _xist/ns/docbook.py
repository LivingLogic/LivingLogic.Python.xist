#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
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
<doc:par>A XSC module that contains definitions for all the elements in DocBook 4.12</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import string

from xist import xsc

class DocTypeDocBook41(xsc.DocType):
	"""
	document type for DocBook 4.1
	"""
	def __init__(self, type):
		xsc.DocType.__init__(self, type + ' PUBLIC "-//OASIS//DTD DocBook V4.1//EN"')


class abbrev(xsc.Element):
	"""
	An abbreviation, especially one followed by a period
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class abstract(xsc.Element):
	"""
	A summary
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class accel(xsc.Element):
	"""
	A graphical user interface (GUI) keyboard shortcut
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class ackno(xsc.Element):
	"""
	Acknowledgements in an Article
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class acronym(xsc.Element):
	"""
	An often pronounceable word made from the initial (or selected) letters of a name or phrase
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class action(xsc.Element):
	"""
	A response to a user event
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class address(xsc.Element):
	"""
	A real-world address, generally a postal address
	"""
	empty = 0
	attrHandlers = {"format": xsc.TextAttr, "linenumbering": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class affiliation(xsc.Element):
	"""
	The institutional affiliation of an individual
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class alt(xsc.Element):
	"""
	Text representation for a graphical element
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class anchor(xsc.Element):
	"""
	A spot in the document
	"""
	empty = 1
	attrHandlers = {"id": xsc.TextAttr, "pagenum": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class answer(xsc.Element):
	"""
	An answer to a question posed in a QandASet
	 """
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class appendix(xsc.Element):
	"""
	An appendix in a Book or Article
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class appendixinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class application(xsc.Element):
	"""
	The name of a software program
	 """
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class area(xsc.Element):
	"""
	A region defined for a Callout in a graphic or code example
	 """
	empty = 1
	attrHandlers = {"label": xsc.TextAttr, "linkends": xsc.TextAttr, "units": xsc.TextAttr, "otherunits": xsc.TextAttr, "coords": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class areaset(xsc.Element):
	"""
	A set of related areas in a graphic or code example
	 """
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "units": xsc.TextAttr, "otherunits": xsc.TextAttr, "coords": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class areaspec(xsc.Element):
	"""
	A collection of regions in a graphic or code example
	 """
	empty = 0
	attrHandlers = {"units": xsc.TextAttr, "otherunits": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class arg(xsc.Element):
	"""
	An argument in a CmdSynopsis
	 """
	empty = 0
	attrHandlers = {"choice": xsc.TextAttr, "rep": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class article(xsc.Element):
	"""
	An article
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "parentbook": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class articleinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class artpagenums(xsc.Element):
	"""
	The page numbers of an article as published
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class attribution(xsc.Element):
	"""
	The source of a block quote or epigraph
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class audiodata(xsc.Element):
	"""
	Pointer to external audio data
	"""
	empty = 1
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "entityref": xsc.TextAttr, "fileref": xsc.TextAttr, "format": xsc.TextAttr, "srccredit": xsc.TextAttr, "role": xsc.TextAttr}

class audioobject(xsc.Element):
	"""
	A wrapper for audio data and its associated meta-information
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class author(xsc.Element):
	"""
	The name of an individual author
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class authorblurb(xsc.Element):
	"""
	A short description or note about an author
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class authorgroup(xsc.Element):
	"""
	Wrapper for author information when a document has multiple authors or collabarators
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class authorinitials(xsc.Element):
	"""
	The initials or other short identifier for an author
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class beginpage(xsc.Element):
	"""
	The location of a page break in a print version of the document
	"""
	empty = 1
	attrHandlers = {"pagenum": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class bibliodiv(xsc.Element):
	"""
	A section of a Bibliography
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class biblioentry(xsc.Element):
	"""
	An entry in a Bibliography
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class bibliography(xsc.Element):
	"""
	A bibliography
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class bibliographyinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class bibliomisc(xsc.Element):
	"""
	Untyped bibliographic information
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class bibliomixed(xsc.Element):
	"""
	An entry in a bibliography
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class bibliomset(xsc.Element):
	"""
	A "cooked" container for related bibliographic information
	"""
	empty = 0
	attrHandlers = {"relation": xsc.TextAttr, "role": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr}

class biblioset(xsc.Element):
	"""
	A "raw" container for related bibliographic information
	"""
	empty = 0
	attrHandlers = {"relation": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class blockquote(xsc.Element):
	"""
	A quotation set off from the main text
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class book(xsc.Element):
	"""
	A book
	"""
	empty = 0
	attrHandlers = {"fpi": xsc.TextAttr, "label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class bookinfo(xsc.Element):
	"""
	Meta-information for a Book
	"""
	empty = 0
	attrHandlers = {"contents": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class bridgehead(xsc.Element):
	"""
	A free-floating heading
	"""
	empty = 0
	attrHandlers = {"renderas": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class callout(xsc.Element):
	"""
	A "called out" description of a marked Area
	"""
	empty = 0
	attrHandlers = {"arearefs": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class calloutlist(xsc.Element):
	"""
	A list of Callouts
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class caption(xsc.Element):
	"""
	A caption
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class caution(xsc.Element):
	"""
	A note of caution
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class chapter(xsc.Element):
	"""
	A chapter, as of a book
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class chapterinfo(xsc.Element):
	"""

	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class citation(xsc.Element):
	"""
	An inline bibliographic reference to another published work
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class citerefentry(xsc.Element):
	"""
	A citation to a reference page
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class citetitle(xsc.Element):
	"""
	The title of a cited work
	"""
	empty = 0
	attrHandlers = {"pubwork": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class city(xsc.Element):
	"""
	The name of a city in an address
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class classname(xsc.Element):
	"""
	The name of a class, in the object-oriented programming sense
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class classsynopsis(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr, "language": xsc.TextAttr, "class": xsc.TextAttr}

class classsynopsisinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"format": xsc.TextAttr, "linenumbering": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class cmdsynopsis(xsc.Element):
	"""
	A syntax summary for a software command
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "sepchar": xsc.TextAttr, "cmdlength": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class co(xsc.Element):
	"""
	
	"""
	empty = 1
	attrHandlers = {"label": xsc.TextAttr, "linkends": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class collab(xsc.Element):
	"""
	Identifies a collaborator
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class collabname(xsc.Element):
	"""
	The name of a collaborator
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class colophon(xsc.Element):
	"""
	Text at the back of a book describing facts about its production
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class colspec(xsc.Element):
	"""

	"""
	empty = 1
	attrHandlers = {"colnum": xsc.TextAttr, "colname": xsc.TextAttr, "colwidth": xsc.TextAttr, "colsep": xsc.TextAttr, "rowsep": xsc.TextAttr, "align": xsc.TextAttr, "char": xsc.TextAttr, "charoff": xsc.TextAttr}

class command(xsc.Element):
	"""
	The name of an executable program or other software command
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class computeroutput(xsc.Element):
	"""
	Data, generally text, displayed or presented by a computer
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class confdates(xsc.Element):
	"""
	The dates of a conference for which a document was written
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class confgroup(xsc.Element):
	"""
	A wrapper for document meta-information about a conference
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class confnum(xsc.Element):
	"""
	An identifier, frequently numerical, associated with a conference for which a document was written
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class confsponsor(xsc.Element):
	"""
	The sponsor of a conference for which a document was written
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class conftitle(xsc.Element):
	"""
	The title of a conference for which a document was written
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class constant(xsc.Element):
	"""
	A programming or system constant
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr, "class": xsc.TextAttr}

class constructorsynopsis(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class contractnum(xsc.Element):
	"""
	The contract number of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class contractsponsor(xsc.Element):
	"""
	The sponsor of a contract
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class contrib(xsc.Element):
	"""
	A summary of the contributions made to a document by a credited source
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class copyright(xsc.Element):
	"""
	Copyright information about a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class corpauthor(xsc.Element):
	"""
	A corporate author, as opposed to an individual
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class corpname(xsc.Element):
	"""
	The name of a corporation
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class country(xsc.Element):
	"""
	The name of a country
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class database(xsc.Element):
	"""
	The name of a database, or part of a database
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class date(xsc.Element):
	"""
	The date of publication or revision of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class dedication(xsc.Element):
	"""
	A wrapper for the dedication section of a book
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class destructorsynopsis(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class edition(xsc.Element):
	"""
	The name or number of an edition of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class editor(xsc.Element):
	"""
	The name of the editor of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class email(xsc.Element):
	"""
	An email address
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class emphasis(xsc.Element):
	"""
	Emphasized text
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class entry(xsc.Element):
	"""
	A cell in a table
	"""
	empty = 0
	attrHandlers = {"colname": xsc.TextAttr, "namest": xsc.TextAttr, "nameend": xsc.TextAttr, "spanname": xsc.TextAttr, "morerows": xsc.TextAttr, "colsep": xsc.TextAttr, "rowsep": xsc.TextAttr, "align": xsc.TextAttr, "char": xsc.TextAttr, "charoff": xsc.TextAttr, "rotate": xsc.TextAttr, "valign": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class entrytbl(xsc.Element):
	"""
	A subtable appearing in place of an Entry in a table
	"""
	empty = 0
	attrHandlers = {"cols": xsc.TextAttr, "tgroupstyle": xsc.TextAttr, "colname": xsc.TextAttr, "spanname": xsc.TextAttr, "namest": xsc.TextAttr, "nameend": xsc.TextAttr, "colsep": xsc.TextAttr, "rowsep": xsc.TextAttr, "align": xsc.TextAttr, "char": xsc.TextAttr, "charoff": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class envar(xsc.Element):
	"""
	A software environment variable
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class epigraph(xsc.Element):
	"""
	A short inscription at the beginning of a document or component
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class equation(xsc.Element):
	"""
	A displayed mathematical equation
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class errorcode(xsc.Element):
	"""
	An error code
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class errorname(xsc.Element):
	"""
	An error message
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class errortype(xsc.Element):
	"""
	The classification of an error message
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class example(xsc.Element):
	"""
	A formal example, with a title
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "width": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class exceptionname(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class fax(xsc.Element):
	"""
	A fax number
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class fieldsynopsis(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class figure(xsc.Element):
	"""
	A formal figure, generally an illustration, with a title
	"""
	empty = 0
	attrHandlers = {"float": xsc.TextAttr, "pgwide": xsc.TextAttr, "label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class filename(xsc.Element):
	"""
	The name of a file
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "path": xsc.TextAttr, "moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class firstname(xsc.Element):
	"""
	The first name of a person
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class firstterm(xsc.Element):
	"""
	The first occurrence of a term
	"""
	empty = 0
	attrHandlers = {"linkend": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class footnote(xsc.Element):
	"""
	A footnote
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class footnoteref(xsc.Element):
	"""
	A cross reference to a footnote (a footnote mark)
	"""
	empty = 1
	attrHandlers = {"linkend": xsc.TextAttr, "label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class foreignphrase(xsc.Element):
	"""
	A word or phrase in a language other than the primary language of the document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class formalpara(xsc.Element):
	"""
	A paragraph with a title
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class funcdef(xsc.Element):
	"""
	A function (subroutine) name and its return type
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class funcparams(xsc.Element):
	"""
	Parameters for a function referenced through a function pointer in a synopsis
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class funcprototype(xsc.Element):
	"""
	The prototype of a function
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class funcsynopsis(xsc.Element):
	"""
	The syntax summary for a function definition
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class funcsynopsisinfo(xsc.Element):
	"""
	Information supplementing the FuncDefs of a FuncSynopsis
	"""
	empty = 0
	attrHandlers = {"format": xsc.TextAttr, "linenumbering": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class function(xsc.Element):
	"""
	The name of a function or subroutine, as in a programming language
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class glossary(xsc.Element):
	"""
	A glossary
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class glossaryinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class glossdef(xsc.Element):
	"""
	A definition in a GlossEntry
	"""
	empty = 0
	attrHandlers = {"subject": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class glossdiv(xsc.Element):
	"""
	A division in a Glossary
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class glossentry(xsc.Element):
	"""
	An entry in a Glossary or GlossList
	"""
	empty = 0
	attrHandlers = {"sortas": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class glosslist(xsc.Element):
	"""
	A wrapper for a set of GlossEntrys
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class glosssee(xsc.Element):
	"""
	A cross-reference from one GlossEntry to another
	"""
	empty = 0
	attrHandlers = {"otherterm": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class glossseealso(xsc.Element):
	"""
	A cross-reference from one GlossEntry to another
	"""
	empty = 0
	attrHandlers = {"otherterm": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class glossterm(xsc.Element):
	"""
	A glossary term
	"""
	empty = 0
	attrHandlers = {"linkend": xsc.TextAttr, "baseform": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class graphic(xsc.Element):
	"""
	A displayed graphical object (not an inline)
	"""
	empty = 1
	attrHandlers = {"entityref": xsc.TextAttr, "fileref": xsc.TextAttr, "format": xsc.TextAttr, "srccredit": xsc.TextAttr, "width": xsc.TextAttr, "depth": xsc.TextAttr, "align": xsc.TextAttr, "scale": xsc.TextAttr, "scalefit": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class graphicco(xsc.Element):
	"""
	A graphic that contains callout areas
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class group(xsc.Element):
	"""
	A group of elements in a CmdSynopsis
	"""
	empty = 0
	attrHandlers = {"choice": xsc.TextAttr, "rep": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class guibutton(xsc.Element):
	"""
	The text on a button in a GUI
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class guiicon(xsc.Element):
	"""
	Graphic and/or text appearing as a icon in a GUI
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class guilabel(xsc.Element):
	"""
	The text of a label in a GUI
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class guimenu(xsc.Element):
	"""
	The name of a menu in a GUI
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class guimenuitem(xsc.Element):
	"""
	The name of a terminal menu item in a GUI
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class guisubmenu(xsc.Element):
	"""
	The name of a submenu in a GUI
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class hardware(xsc.Element):
	"""
	A physical part of a computer system
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class highlights(xsc.Element):
	"""
	A summary of the main points of the discussed component
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class holder(xsc.Element):
	"""
	The name of the individual or organization that holds a copyright
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class honorific(xsc.Element):
	"""
	The title of a person
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class imagedata(xsc.Element):
	"""
	Pointer to external image data
	"""
	empty = 1
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "entityref": xsc.TextAttr, "fileref": xsc.TextAttr, "format": xsc.TextAttr, "srccredit": xsc.TextAttr, "width": xsc.TextAttr, "depth": xsc.TextAttr, "align": xsc.TextAttr, "scale": xsc.TextAttr, "scalefit": xsc.TextAttr, "role": xsc.TextAttr}

class imageobject(xsc.Element):
	"""
	A wrapper for image data and its associated meta-information
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class imageobjectco(xsc.Element):
	"""
	A wrapper for an image object with callouts
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class important(xsc.Element):
	"""
	An admonition set off from the text
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class index(xsc.Element):
	"""
	An index
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class indexdiv(xsc.Element):
	"""
	A division in an index
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class indexentry(xsc.Element):
	"""
	An entry in an index
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class indexinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class indexterm(xsc.Element):
	"""
	A wrapper for terms to be indexed
	"""
	empty = 0
	attrHandlers = {"pagenum": xsc.TextAttr, "scope": xsc.TextAttr, "significance": xsc.TextAttr, "class": xsc.TextAttr, "startref": xsc.TextAttr, "zone": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class informalequation(xsc.Element):
	"""
	A displayed mathematical equation without a title
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class informalexample(xsc.Element):
	"""
	A displayed example without a title
	"""
	empty = 0
	attrHandlers = {"width": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class informalfigure(xsc.Element):
	"""
	A untitled figure
	"""
	empty = 0
	attrHandlers = {"float": xsc.TextAttr, "pgwide": xsc.TextAttr, "label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class informaltable(xsc.Element):
	"""
	A table without a title
	"""
	empty = 0
	attrHandlers = {"frame": xsc.TextAttr, "colsep": xsc.TextAttr, "rowsep": xsc.TextAttr, "label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr, "tabstyle": xsc.TextAttr, "tocentry": xsc.TextAttr, "shortentry": xsc.TextAttr, "orient": xsc.TextAttr, "pgwide": xsc.TextAttr}

class initializer(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class inlineequation(xsc.Element):
	"""
	A mathematical equation or expression occurring inline
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class inlinegraphic(xsc.Element):
	"""
	An object containing or pointing to graphical data that will be rendered inline
	"""
	empty = 1
	attrHandlers = {"entityref": xsc.TextAttr, "fileref": xsc.TextAttr, "format": xsc.TextAttr, "srccredit": xsc.TextAttr, "width": xsc.TextAttr, "depth": xsc.TextAttr, "align": xsc.TextAttr, "scale": xsc.TextAttr, "scalefit": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class inlinemediaobject(xsc.Element):
	"""
	An inline media object (video, audio, image, and so on)
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class interface(xsc.Element):
	"""
	An element of a GUI
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class interfacename(xsc.Element):
	"""
	The name of a formal specification of a GUI
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class invpartnumber(xsc.Element):
	"""
	An inventory part number
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class isbn(xsc.Element):
	"""
	The International Standard Book Number of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class issn(xsc.Element):
	"""
	The International Standard Serial Number of a periodical
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class issuenum(xsc.Element):
	"""
	The number of an issue of a journal
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class itemizedlist(xsc.Element):
	"""
	A list in which each entry is marked with a bullet or other dingbat
	"""
	empty = 0
	attrHandlers = {"spacing": xsc.TextAttr, "mark": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class itermset(xsc.Element):
	"""
	A set of index terms in the meta-information of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class jobtitle(xsc.Element):
	"""
	The title of an individual in an organization
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class keycap(xsc.Element):
	"""
	The text printed on a key on a keyboard
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class keycode(xsc.Element):
	"""
	The internal, frequently numeric, identifier for a key on a
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class keycombo(xsc.Element):
	"""
	A combination of input actions
	"""
	empty = 0
	attrHandlers = {"action": xsc.TextAttr, "otheraction": xsc.TextAttr, "moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class keysym(xsc.Element):
	"""
	The symbolic name of a key on a keyboard
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class keyword(xsc.Element):
	"""
	One of a set of keywords describing the content of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class keywordset(xsc.Element):
	"""
	A set of keywords describing the content of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class label(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class legalnotice(xsc.Element):
	"""
	A statement of legal obligations or requirements
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class lineage(xsc.Element):
	"""
	The portion of a person's name indicating a relationship to ancestors
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class lineannotation(xsc.Element):
	"""
	A comment on a line in a verbatim listing
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class link(xsc.Element):
	"""
	A hypertext link
	"""
	empty = 0
	attrHandlers = {"endterm": xsc.TextAttr, "linkend": xsc.TextAttr, "type": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class listitem(xsc.Element):
	"""
	A wrapper for the elements of a list item
	"""
	empty = 0
	attrHandlers = {"override": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class literal(xsc.Element):
	"""
	Inline text that is some literal value
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class literallayout(xsc.Element):
	"""
	A block of text in which line breaks and white space are to be reproduced faithfully
	"""
	empty = 0
	attrHandlers = {"width": xsc.TextAttr, "format": xsc.TextAttr, "linenumbering": xsc.TextAttr, "class": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class lot(xsc.Element):
	"""
	 A list of the titles of formal objects (as tables or figures) in a document 
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class lotentry(xsc.Element):
	"""
	An entry in a list of titles
	"""
	empty = 0
	attrHandlers = {"srccredit": xsc.TextAttr, "pagenum": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "linkend": xsc.TextAttr, "role": xsc.TextAttr}

class manvolnum(xsc.Element):
	"""
	A reference volume number
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class markup(xsc.Element):
	"""
	A string of formatting markup in text that is to be represented literally
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class medialabel(xsc.Element):
	"""
	A name that identifies the physical medium on which some information resides
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class mediaobject(xsc.Element):
	"""
	A displayed media object (video, audio, image, etc.)
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class mediaobjectco(xsc.Element):
	"""
	A media object that contains callouts
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class member(xsc.Element):
	"""
	An element of a simple list
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class menuchoice(xsc.Element):
	"""
	A selection or series of selections from a menu
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class methodname(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class methodparam(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr, "choice": xsc.TextAttr, "rep": xsc.TextAttr}

class methodsynopsis(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class modespec(xsc.Element):
	"""
	Application-specific information necessary for the completion of an OLink
	"""
	empty = 0
	attrHandlers = {"application": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class modifier(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class mousebutton(xsc.Element):
	"""
	The conventional name of a mouse button
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msg(xsc.Element):
	"""
	A message in a message set
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msgaud(xsc.Element):
	"""
	The audience to which a message in a message set is relevant
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msgentry(xsc.Element):
	"""
	A wrapper for an entry in a message set
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msgexplan(xsc.Element):
	"""
	Explanatory material relating to a message in a message set
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msginfo(xsc.Element):
	"""
	Information about a message in a message set
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msglevel(xsc.Element):
	"""
	The level of importance or severity of a message in a message set
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msgmain(xsc.Element):
	"""
	The primary component of a message in a message set
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msgorig(xsc.Element):
	"""
	The origin of a message in a message set
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msgrel(xsc.Element):
	"""
	A related component of a message in a message set
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msgset(xsc.Element):
	"""
	A detailed set of messages, usually error messages
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msgsub(xsc.Element):
	"""
	A subcomponent of a message in a message set
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class msgtext(xsc.Element):
	"""
	The actual text of a message component in a message set
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class note(xsc.Element):
	"""
	A message set off from the text
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class objectinfo(xsc.Element):
	"""
	Meta-information for an object
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class olink(xsc.Element):
	"""
	A link that addresses its target indirectly, through an entity
	"""
	empty = 0
	attrHandlers = {"targetdocent": xsc.TextAttr, "linkmode": xsc.TextAttr, "localinfo": xsc.TextAttr, "type": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class ooclass(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class ooexception(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class oointerface(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class option(xsc.Element):
	"""
	An option for a software command
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class optional(xsc.Element):
	"""
	Optional information
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class orderedlist(xsc.Element):
	"""
	A list in which each entry is marked with a sequentially incremented label
	"""
	empty = 0
	attrHandlers = {"numeration": xsc.TextAttr, "inheritnum": xsc.TextAttr, "continuation": xsc.TextAttr, "spacing": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class orgdiv(xsc.Element):
	"""
	A division of an organization
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class orgname(xsc.Element):
	"""
	The name of an organization other than a corporation
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class otheraddr(xsc.Element):
	"""
	Uncategorized information in address
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class othercredit(xsc.Element):
	"""
	A person or entity, other than an author or editor, credited in a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class othername(xsc.Element):
	"""
	A component of a persons name that is not a first name, surname, or lineage
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class pagenums(xsc.Element):
	"""
	The numbers of the pages in a book, for use in a bibliographic entry
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class para(xsc.Element):
	"""
	A paragraph
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class paramdef(xsc.Element):
	"""
	Information about a function parameter in a programming language
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class parameter(xsc.Element):
	"""
	A value or a symbolic reference to a value
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class part(xsc.Element):
	"""
	A division in a book
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class partinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class partintro(xsc.Element):
	"""
	An introduction to the contents of a part
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class phone(xsc.Element):
	"""
	A telephone number
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class phrase(xsc.Element):
	"""
	A span of text
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class pob(xsc.Element):
	"""
	A post office box in an address
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class postcode(xsc.Element):
	"""
	A postal code in an address
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class preface(xsc.Element):
	"""
	Introductory matter preceding the first chapter of a book
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class prefaceinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class primary(xsc.Element):
	"""
	The primary word or phrase under which an index term should be sorted
	"""
	empty = 0
	attrHandlers = {"sortas": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class primaryie(xsc.Element):
	"""
	A primary term in an index entry, not in the text
	"""
	empty = 0
	attrHandlers = {"linkends": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class printhistory(xsc.Element):
	"""
	The printing history of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class procedure(xsc.Element):
	"""
	A list of operations to be performed in a well-defined sequence
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class productname(xsc.Element):
	"""
	The formal name of a product
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class productnumber(xsc.Element):
	"""
	A number assigned to a product
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class programlisting(xsc.Element):
	"""
	A literal listing of all or part of a program
	"""
	empty = 0
	attrHandlers = {"width": xsc.TextAttr, "format": xsc.TextAttr, "linenumbering": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class programlistingco(xsc.Element):
	"""
	A program listing with associated areas used in callouts
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class prompt(xsc.Element):
	"""
	A character or string indicating the start of an input field in a computer display
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class property(xsc.Element):
	"""
	A unit of data associated with some part of a computer system
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class pubdate(xsc.Element):
	"""
	The date of publication of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class publisher(xsc.Element):
	"""
	The publisher of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class publishername(xsc.Element):
	"""
	The name of the publisher of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class pubsnumber(xsc.Element):
	"""
	A number assigned to a publication other than an ISBN or ISSN or inventory part number
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class qandadiv(xsc.Element):
	"""
	A titled division in a QandASet
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class qandaentry(xsc.Element):
	"""
	A question/answer set within a QandASet
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class qandaset(xsc.Element):
	"""
	A question-and-answer set
	"""
	empty = 0
	attrHandlers = {"defaultlabel": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class question(xsc.Element):
	"""
	A question in a QandASet
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class quote(xsc.Element):
	"""
	An inline quotation
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refclass(xsc.Element):
	"""
	The scope or other indication of applicability of a reference entry 
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refdescriptor(xsc.Element):
	"""
	A description of the topic of a reference page
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refentry(xsc.Element):
	"""
	A reference page (originally a UNIX man-style reference page)
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refentryinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refentrytitle(xsc.Element):
	"""
	The title of a reference page
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class reference(xsc.Element):
	"""
	A collection of reference entries
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class referenceinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refmeta(xsc.Element):
	"""
	Meta-information for a reference entry
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refmiscinfo(xsc.Element):
	"""
	Meta-information for a reference entry other than the title and volume number 
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refname(xsc.Element):
	"""
	The name of (one of) the subject(s) of a reference page
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refnamediv(xsc.Element):
	"""
	The name, purpose, and classification of a reference page
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refpurpose(xsc.Element):
	"""
	A short (one sentence) synopsis of the topic of a reference page
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refsect1(xsc.Element):
	"""
	A major subsection of a reference entry
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refsect1info(xsc.Element):
	"""
	Meta-information for a RefSect1
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refsect2(xsc.Element):
	"""
	A subsection of a RefSect1
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refsect2info(xsc.Element):
	"""
	Meta-information for a RefSect2
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refsect3(xsc.Element):
	"""
	A subsection of a RefSect2
	"""
	empty = 0
	attrHandlers = {"status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refsect3info(xsc.Element):
	"""
	Meta-information for a RefSect3
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refsynopsisdiv(xsc.Element):
	"""
	A syntactic synopsis of the subject of the reference page
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class refsynopsisdivinfo(xsc.Element):
	"""
	Meta-information for a RefSynopsisDiv
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class releaseinfo(xsc.Element):
	"""
	Information about a particular release of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class remark(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class replaceable(xsc.Element):
	"""
	Content that may or must be replaced by the user
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class returnvalue(xsc.Element):
	"""
	The value returned by a function
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class revdescription(xsc.Element):
	"""

	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class revhistory(xsc.Element):
	"""
	A history of the revisions to a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class revision(xsc.Element):
	"""
	An entry describing a single revision in the history of the revisions to a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class revnumber(xsc.Element):
	"""
	A document revision number
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class revremark(xsc.Element):
	"""
	A description of a revision to a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class row(xsc.Element):
	"""
	A row in a table
	"""
	empty = 0
	attrHandlers = {"rowsep": xsc.TextAttr, "valign": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sbr(xsc.Element):
	"""
	An explicit line break in a command synopsis
	"""
	empty = 1
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class screen(xsc.Element):
	"""
	Text that a user sees or might see on a computer screen
	"""
	empty = 0
	attrHandlers = {"width": xsc.TextAttr, "format": xsc.TextAttr, "linenumbering": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class screenco(xsc.Element):
	"""
	A screen with associated areas used in callouts
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class screeninfo(xsc.Element):
	"""
	Information about how a screen shot was produced
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class screenshot(xsc.Element):
	"""
	A representation of what the user sees or might see on a computer screen
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class secondary(xsc.Element):
	"""
	A secondary word or phrase in an index term
	"""
	empty = 0
	attrHandlers = {"sortas": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class secondaryie(xsc.Element):
	"""
	A secondary term in an index entry, rather than in the text
	"""
	empty = 0
	attrHandlers = {"linkends": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sect1(xsc.Element):
	"""
	A top-level section of document
	"""
	empty = 0
	attrHandlers = {"renderas": xsc.TextAttr, "label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sect1info(xsc.Element):
	"""
	Meta-information for a Sect1
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sect2(xsc.Element):
	"""
	A subsection within a Sect1
	"""
	empty = 0
	attrHandlers = {"renderas": xsc.TextAttr, "label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sect2info(xsc.Element):
	"""
	Meta-information for a Sect2
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sect3(xsc.Element):
	"""
	A subsection within a Sect2
	"""
	empty = 0
	attrHandlers = {"renderas": xsc.TextAttr, "label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sect3info(xsc.Element):
	"""
	Meta-information for a Sect3
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sect4(xsc.Element):
	"""
	A subsection within a Sect3
	"""
	empty = 0
	attrHandlers = {"renderas": xsc.TextAttr, "label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sect4info(xsc.Element):
	"""
	Meta-information for a Sect4
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sect5(xsc.Element):
	"""
	A subsection within a Sect4
	"""
	empty = 0
	attrHandlers = {"renderas": xsc.TextAttr, "label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sect5info(xsc.Element):
	"""
	Meta-information for a Sect5
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class section(xsc.Element):
	"""
	A recursive section
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sectioninfo(xsc.Element):
	"""
	Meta-information for a recursive section
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class see(xsc.Element):
	"""
	Part of an index term directing the reader instead to another entry in the index
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class seealso(xsc.Element):
	"""
	Part of an index term directing the reader also to another entry in the index
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class seealsoie(xsc.Element):
	"""
	A "See also" entry in an index, rather than in the text
	"""
	empty = 0
	attrHandlers = {"linkends": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class seeie(xsc.Element):
	"""
	A "See" entry in an index, rather than in the text
	"""
	empty = 0
	attrHandlers = {"linkend": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class seg(xsc.Element):
	"""
	An element of a list item in a segmented list
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class seglistitem(xsc.Element):
	"""
	A list item in a segmented list
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class segmentedlist(xsc.Element):
	"""
	A segmented list, a list of sets of elements
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class segtitle(xsc.Element):
	"""
	The title of an element of a list item in a segmented list
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class seriesvolnums(xsc.Element):
	"""
	Numbers of the volumes in a series of books
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class set(xsc.Element):
	"""
	A collection of books
	"""
	empty = 0
	attrHandlers = {"fpi": xsc.TextAttr, "status": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class setindex(xsc.Element):
	"""
	An index to a set of books
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class setindexinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class setinfo(xsc.Element):
	"""
	Meta-information for a Set
	"""
	empty = 0
	attrHandlers = {"contents": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sgmltag(xsc.Element):
	"""
	A component of SGML markup
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class shortaffil(xsc.Element):
	"""
	A brief description of an affiliation
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class shortcut(xsc.Element):
	"""
	A key combination for an action that is also accessible through a menu
	"""
	empty = 0
	attrHandlers = {"action": xsc.TextAttr, "otheraction": xsc.TextAttr, "moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sidebar(xsc.Element):
	"""
	A portion of a document that is isolated from the main narrative flow
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class sidebarinfo(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class simpara(xsc.Element):
	"""
	A paragraph that contains only text and inline markup, no block elements
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class simplelist(xsc.Element):
	"""
	An undecorated list of single words or short phrases
	"""
	empty = 0
	attrHandlers = {"columns": xsc.TextAttr, "type": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class simplemsgentry(xsc.Element):
	"""
	
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr, "audience": xsc.TextAttr, "level": xsc.TextAttr, "origin": xsc.TextAttr}

class simplesect(xsc.Element):
	"""
	A section of a document with no subdivisions
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class spanspec(xsc.Element):
	"""
	Formatting information for a spanned column in a table
	"""
	empty = 1
	attrHandlers = {"namest": xsc.TextAttr, "nameend": xsc.TextAttr, "spanname": xsc.TextAttr, "colsep": xsc.TextAttr, "rowsep": xsc.TextAttr, "align": xsc.TextAttr, "char": xsc.TextAttr, "charoff": xsc.TextAttr}

class state(xsc.Element):
	"""
	A state or province in an address
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class step(xsc.Element):
	"""
	A unit of action in a procedure
	"""
	empty = 0
	attrHandlers = {"performance": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class street(xsc.Element):
	"""
	A street address in an address
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class structfield(xsc.Element):
	"""
	A field in a structure (in the programming language sense)
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class structname(xsc.Element):
	"""
	The name of a structure (in the programming language sense)
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class subject(xsc.Element):
	"""
	One of a group of terms describing the subject matter of a document
	"""
	empty = 0
	attrHandlers = {"weight": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class subjectset(xsc.Element):
	"""
	A set of terms describing the subject matter of a document
	"""
	empty = 0
	attrHandlers = {"scheme": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class subjectterm(xsc.Element):
	"""
	A term in a group of terms describing the subject matter of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class subscript(xsc.Element):
	"""
	A subscript (as in H2O, the molecular formula for water)
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class substeps(xsc.Element):
	"""
	A wrapper for steps that occur within steps in a procedure
	"""
	empty = 0
	attrHandlers = {"performance": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class subtitle(xsc.Element):
	"""
	The subtitle of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class superscript(xsc.Element):
	"""
	A superscript (as in x2, the mathematical notation for x multiplied by itself)
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class surname(xsc.Element):
	"""
	A family name, in western cultures the "last name"
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class symbol(xsc.Element):
	"""
	A name that is replaced by a value before processing
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class synopfragment(xsc.Element):
	"""
	A portion of a CmdSynopsis broken out from the main body of the synopsis
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class synopfragmentref(xsc.Element):
	"""
	A reference to a fragment of a command synopsis
	"""
	empty = 0
	attrHandlers = {"linkend": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class synopsis(xsc.Element):
	"""
	A general-purpose element for representing the syntax of commands or functions
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "format": xsc.TextAttr, "linenumbering": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class systemitem(xsc.Element):
	"""
	A system-related item or term
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class table(xsc.Element):
	"""
	A formal table in a document
	"""
	empty = 0
	attrHandlers = {"frame": xsc.TextAttr, "colsep": xsc.TextAttr, "rowsep": xsc.TextAttr, "tabstyle": xsc.TextAttr, "tocentry": xsc.TextAttr, "shortentry": xsc.TextAttr, "orient": xsc.TextAttr, "pgwide": xsc.TextAttr, "label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tbody(xsc.Element):
	"""
	A wrapper for the rows of a table or informal table
	"""
	empty = 0
	attrHandlers = {"valign": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class term(xsc.Element):
	"""
	The word or phrase being defined or described in a variable list
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tertiary(xsc.Element):
	"""
	A tertiary word or phrase in an index term
	"""
	empty = 0
	attrHandlers = {"sortas": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tertiaryie(xsc.Element):
	"""
	A tertiary term in an index entry, rather than in the text
	"""
	empty = 0
	attrHandlers = {"linkends": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class textobject(xsc.Element):
	"""
	A wrapper for a text description of an object and its associated meta-information
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tfoot(xsc.Element):
	"""
	A table footer consisting of one or more rows
	"""
	empty = 0
	attrHandlers = {"valign": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tgroup(xsc.Element):
	"""
	A wrapper for the main content of a table, or part of a table
	"""
	empty = 0
	attrHandlers = {"cols": xsc.TextAttr, "tgroupstyle": xsc.TextAttr, "colsep": xsc.TextAttr, "rowsep": xsc.TextAttr, "align": xsc.TextAttr, "char": xsc.TextAttr, "charoff": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class thead(xsc.Element):
	"""
	A table header consisting of one or more rows
	"""
	empty = 0
	attrHandlers = {"valign": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tip(xsc.Element):
	"""
	A suggestion to the user, set off from the text
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class title(xsc.Element):
	"""
	The text of the title of a section of a document or of a formal block-level element
	"""
	empty = 0
	attrHandlers = {"pagenum": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class titleabbrev(xsc.Element):
	"""
	The abbreviation of a Title
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class toc(xsc.Element):
	"""
	A table of contents
	"""
	empty = 0
	attrHandlers = {"pagenum": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tocback(xsc.Element):
	"""
	An entry in a table of contents for a back matter component
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "linkend": xsc.TextAttr, "pagenum": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tocchap(xsc.Element):
	"""
	An entry in a table of contents for a component in the body of a document
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tocentry(xsc.Element):
	"""
	A component title in a table of contents
	"""
	empty = 0
	attrHandlers = {"linkend": xsc.TextAttr, "pagenum": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tocfront(xsc.Element):
	"""
	An entry in a table of contents for a front matter component
	"""
	empty = 0
	attrHandlers = {"label": xsc.TextAttr, "linkend": xsc.TextAttr, "pagenum": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class toclevel1(xsc.Element):
	"""
	A top-level entry within a table of contents entry for a chapter-like component
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class toclevel2(xsc.Element):
	"""
	A second-level entry within a table of contents entry for a chapter-like component
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class toclevel3(xsc.Element):
	"""
	A third-level entry within a table of contents entry for a chapter-like component
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class toclevel4(xsc.Element):
	"""
	A fourth-level entry within a table of contents entry for a chapter-like component
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class toclevel5(xsc.Element):
	"""
	A fifth-level entry within a table of contents entry for a chapter-like component
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class tocpart(xsc.Element):
	"""
	An entry in a table of contents for a part of a book
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class token(xsc.Element):
	"""
	A unit of information
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class trademark(xsc.Element):
	"""
	A trademark
	"""
	empty = 0
	attrHandlers = {"class": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class type(xsc.Element):
	"""
	The classification of a value
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class ulink(xsc.Element):
	"""
	A link that addresses its target by means of a URL (Uniform Resource Locator)
	"""
	empty = 0
	attrHandlers = {"url": xsc.TextAttr, "type": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class userinput(xsc.Element):
	"""
	Data entered by the user
	"""
	empty = 0
	attrHandlers = {"moreinfo": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class varargs(xsc.Element):
	"""
	An empty element in a function synopsis indicating a variable number of arguments
	"""
	empty = 1
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class variablelist(xsc.Element):
	"""
	A list in which each entry is composed of a set of one or more terms and an associated description
	"""
	empty = 0
	attrHandlers = {"termlength": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class varlistentry(xsc.Element):
	"""
	A wrapper for a set of terms and the associated description in a variable list
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class varname(xsc.Element):
	"""
	The name of a variable
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class videodata(xsc.Element):
	"""
	Pointer to external video data
	"""
	empty = 1
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "entityref": xsc.TextAttr, "fileref": xsc.TextAttr, "format": xsc.TextAttr, "srccredit": xsc.TextAttr, "width": xsc.TextAttr, "depth": xsc.TextAttr, "align": xsc.TextAttr, "scale": xsc.TextAttr, "scalefit": xsc.TextAttr, "role": xsc.TextAttr}

class videoobject(xsc.Element):
	"""
	A wrapper for video data and its associated meta-information
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class void(xsc.Element):
	"""
	An empty element in a function synopsis indicating that the function in question takes no arguments
	"""
	empty = 1
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class volumenum(xsc.Element):
	"""
	The volume number of a document in a set (as of books in a set or articles in a journal)
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class warning(xsc.Element):
	"""
	An admonition set off from the text
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class wordasword(xsc.Element):
	"""
	A word meant specifically as a word and not representing anything else
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class xref(xsc.Element):
	"""
	A cross reference to another part of the document
	"""
	empty = 1
	attrHandlers = {"endterm": xsc.TextAttr, "linkend": xsc.TextAttr, "id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

class year(xsc.Element):
	"""
	The year of publication of a document
	"""
	empty = 0
	attrHandlers = {"id": xsc.TextAttr, "lang": xsc.TextAttr, "remap": xsc.TextAttr, "xreflabel": xsc.TextAttr, "revisionflag": xsc.TextAttr, "arch": xsc.TextAttr, "condition": xsc.TextAttr, "conformance": xsc.TextAttr, "os": xsc.TextAttr, "revision": xsc.TextAttr, "security": xsc.TextAttr, "userlevel": xsc.TextAttr, "vendor": xsc.TextAttr, "role": xsc.TextAttr}

# register all the classes we've defined so far
namespace = xsc.Namespace("docbook", "http://www.oasis-open.org/docbook/xml/4.0/docbookx.dtd", vars())
