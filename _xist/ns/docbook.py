#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; namespace module that contains definitions for all the elements in DocBook 4.12</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc

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
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class abstract(xsc.Element):
	"""
	A summary
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class accel(xsc.Element):
	"""
	A graphical user interface (GUI) keyboard shortcut
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class ackno(xsc.Element):
	"""
	Acknowledgements in an Article
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class acronym(xsc.Element):
	"""
	An often pronounceable word made from the initial (or selected) letters of a name or phrase
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class action(xsc.Element):
	"""
	A response to a user event
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class address(xsc.Element):
	"""
	A real-world address, generally a postal address
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class format(xsc.TextAttr): pass
		class linenumbering(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class affiliation(xsc.Element):
	"""
	The institutional affiliation of an individual
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class alt(xsc.Element):
	"""
	Text representation for a graphical element
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class anchor(xsc.Element):
	"""
	A spot in the document
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class pagenum(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class answer(xsc.Element):
	"""
	An answer to a question posed in a QandASet
	 """
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class appendix(xsc.Element):
	"""
	An appendix in a Book or Article
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class appendixinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class application(xsc.Element):
	"""
	The name of a software program
	 """
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class area(xsc.Element):
	"""
	A region defined for a Callout in a graphic or code example
	 """
	empty = True
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class linkends(xsc.TextAttr): pass
		class units(xsc.TextAttr): pass
		class otherunits(xsc.TextAttr): pass
		class coords(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class areaset(xsc.Element):
	"""
	A set of related areas in a graphic or code example
	 """
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class units(xsc.TextAttr): pass
		class otherunits(xsc.TextAttr): pass
		class coords(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class areaspec(xsc.Element):
	"""
	A collection of regions in a graphic or code example
	 """
	empty = False
	class Attrs(xsc.Element.Attrs):
		class units(xsc.TextAttr): pass
		class otherunits(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class arg(xsc.Element):
	"""
	An argument in a CmdSynopsis
	 """
	empty = False
	class Attrs(xsc.Element.Attrs):
		class choice(xsc.TextAttr): pass
		class rep(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class article(xsc.Element):
	"""
	An article
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class parentbook(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class articleinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class artpagenums(xsc.Element):
	"""
	The page numbers of an article as published
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class attribution(xsc.Element):
	"""
	The source of a block quote or epigraph
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class audiodata(xsc.Element):
	"""
	Pointer to external audio data
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class entityref(xsc.TextAttr): pass
		class fileref(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class srccredit(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class audioobject(xsc.Element):
	"""
	A wrapper for audio data and its associated meta-information
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class author(xsc.Element):
	"""
	The name of an individual author
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class authorblurb(xsc.Element):
	"""
	A short description or note about an author
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class authorgroup(xsc.Element):
	"""
	Wrapper for author information when a document has multiple authors or collabarators
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class authorinitials(xsc.Element):
	"""
	The initials or other short identifier for an author
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class beginpage(xsc.Element):
	"""
	The location of a page break in a print version of the document
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class pagenum(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class bibliodiv(xsc.Element):
	"""
	A section of a Bibliography
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class biblioentry(xsc.Element):
	"""
	An entry in a Bibliography
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class bibliography(xsc.Element):
	"""
	A bibliography
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class bibliographyinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class bibliomisc(xsc.Element):
	"""
	Untyped bibliographic information
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class bibliomixed(xsc.Element):
	"""
	An entry in a bibliography
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class bibliomset(xsc.Element):
	"""
	A "cooked" container for related bibliographic information
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class relation(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass

class biblioset(xsc.Element):
	"""
	A "raw" container for related bibliographic information
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class relation(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class blockquote(xsc.Element):
	"""
	A quotation set off from the main text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class book(xsc.Element):
	"""
	A book
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class fpi(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class bookinfo(xsc.Element):
	"""
	Meta-information for a Book
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class contents(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class bridgehead(xsc.Element):
	"""
	A free-floating heading
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class renderas(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class callout(xsc.Element):
	"""
	A "called out" description of a marked Area
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class arearefs(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class calloutlist(xsc.Element):
	"""
	A list of Callouts
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class caption(xsc.Element):
	"""
	A caption
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class caution(xsc.Element):
	"""
	A note of caution
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class chapter(xsc.Element):
	"""
	A chapter, as of a book
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class chapterinfo(xsc.Element):
	"""

	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class citation(xsc.Element):
	"""
	An inline bibliographic reference to another published work
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class citerefentry(xsc.Element):
	"""
	A citation to a reference page
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class citetitle(xsc.Element):
	"""
	The title of a cited work
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class pubwork(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class city(xsc.Element):
	"""
	The name of a city in an address
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class classname(xsc.Element):
	"""
	The name of a class, in the object-oriented programming sense
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class classsynopsis(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass
		class language(xsc.TextAttr): pass
		class class_(xsc.TextAttr): xmlname = "class"

class classsynopsisinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class format(xsc.TextAttr): pass
		class linenumbering(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class cmdsynopsis(xsc.Element):
	"""
	A syntax summary for a software command
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class sepchar(xsc.TextAttr): pass
		class cmdlength(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class co(xsc.Element):
	"""
	
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class linkends(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class collab(xsc.Element):
	"""
	Identifies a collaborator
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class collabname(xsc.Element):
	"""
	The name of a collaborator
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class colophon(xsc.Element):
	"""
	Text at the back of a book describing facts about its production
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class colspec(xsc.Element):
	"""

	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class colnum(xsc.TextAttr): pass
		class colname(xsc.TextAttr): pass
		class colwidth(xsc.TextAttr): pass
		class colsep(xsc.TextAttr): pass
		class rowsep(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class char(xsc.TextAttr): pass
		class charoff(xsc.TextAttr): pass

class command(xsc.Element):
	"""
	The name of an executable program or other software command
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class computeroutput(xsc.Element):
	"""
	Data, generally text, displayed or presented by a computer
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class confdates(xsc.Element):
	"""
	The dates of a conference for which a document was written
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class confgroup(xsc.Element):
	"""
	A wrapper for document meta-information about a conference
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class confnum(xsc.Element):
	"""
	An identifier, frequently numerical, associated with a conference for which a document was written
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class confsponsor(xsc.Element):
	"""
	The sponsor of a conference for which a document was written
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class conftitle(xsc.Element):
	"""
	The title of a conference for which a document was written
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class constant(xsc.Element):
	"""
	A programming or system constant
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass
		class class_(xsc.TextAttr): xmlname = "class"

class constructorsynopsis(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class contractnum(xsc.Element):
	"""
	The contract number of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class contractsponsor(xsc.Element):
	"""
	The sponsor of a contract
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class contrib(xsc.Element):
	"""
	A summary of the contributions made to a document by a credited source
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class copyright(xsc.Element):
	"""
	Copyright information about a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class corpauthor(xsc.Element):
	"""
	A corporate author, as opposed to an individual
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class corpname(xsc.Element):
	"""
	The name of a corporation
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class country(xsc.Element):
	"""
	The name of a country
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class database(xsc.Element):
	"""
	The name of a database, or part of a database
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class date(xsc.Element):
	"""
	The date of publication or revision of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class dedication(xsc.Element):
	"""
	A wrapper for the dedication section of a book
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class destructorsynopsis(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class edition(xsc.Element):
	"""
	The name or number of an edition of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class editor(xsc.Element):
	"""
	The name of the editor of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class email(xsc.Element):
	"""
	An email address
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class emphasis(xsc.Element):
	"""
	Emphasized text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class entry(xsc.Element):
	"""
	A cell in a table
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class colname(xsc.TextAttr): pass
		class namest(xsc.TextAttr): pass
		class nameend(xsc.TextAttr): pass
		class spanname(xsc.TextAttr): pass
		class morerows(xsc.TextAttr): pass
		class colsep(xsc.TextAttr): pass
		class rowsep(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class char(xsc.TextAttr): pass
		class charoff(xsc.TextAttr): pass
		class rotate(xsc.TextAttr): pass
		class valign(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class entrytbl(xsc.Element):
	"""
	A subtable appearing in place of an Entry in a table
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class cols(xsc.TextAttr): pass
		class tgroupstyle(xsc.TextAttr): pass
		class colname(xsc.TextAttr): pass
		class spanname(xsc.TextAttr): pass
		class namest(xsc.TextAttr): pass
		class nameend(xsc.TextAttr): pass
		class colsep(xsc.TextAttr): pass
		class rowsep(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class char(xsc.TextAttr): pass
		class charoff(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class envar(xsc.Element):
	"""
	A software environment variable
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class epigraph(xsc.Element):
	"""
	A short inscription at the beginning of a document or component
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class equation(xsc.Element):
	"""
	A displayed mathematical equation
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class errorcode(xsc.Element):
	"""
	An error code
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class errorname(xsc.Element):
	"""
	An error message
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class errortype(xsc.Element):
	"""
	The classification of an error message
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class example(xsc.Element):
	"""
	A formal example, with a title
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class width(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class exceptionname(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class fax(xsc.Element):
	"""
	A fax number
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class fieldsynopsis(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class figure(xsc.Element):
	"""
	A formal figure, generally an illustration, with a title
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class float(xsc.TextAttr): pass
		class pgwide(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class filename(xsc.Element):
	"""
	The name of a file
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class path(xsc.TextAttr): pass
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class firstname(xsc.Element):
	"""
	The first name of a person
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class firstterm(xsc.Element):
	"""
	The first occurrence of a term
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class linkend(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class footnote(xsc.Element):
	"""
	A footnote
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class footnoteref(xsc.Element):
	"""
	A cross reference to a footnote (a footnote mark)
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class linkend(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class foreignphrase(xsc.Element):
	"""
	A word or phrase in a language other than the primary language of the document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class formalpara(xsc.Element):
	"""
	A paragraph with a title
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class funcdef(xsc.Element):
	"""
	A function (subroutine) name and its return type
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class funcparams(xsc.Element):
	"""
	Parameters for a function referenced through a function pointer in a synopsis
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class funcprototype(xsc.Element):
	"""
	The prototype of a function
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class funcsynopsis(xsc.Element):
	"""
	The syntax summary for a function definition
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class funcsynopsisinfo(xsc.Element):
	"""
	Information supplementing the FuncDefs of a FuncSynopsis
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class format(xsc.TextAttr): pass
		class linenumbering(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class function(xsc.Element):
	"""
	The name of a function or subroutine, as in a programming language
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class glossary(xsc.Element):
	"""
	A glossary
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class glossaryinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class glossdef(xsc.Element):
	"""
	A definition in a GlossEntry
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class subject(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class glossdiv(xsc.Element):
	"""
	A division in a Glossary
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class glossentry(xsc.Element):
	"""
	An entry in a Glossary or GlossList
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class sortas(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class glosslist(xsc.Element):
	"""
	A wrapper for a set of GlossEntrys
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class glosssee(xsc.Element):
	"""
	A cross-reference from one GlossEntry to another
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class otherterm(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class glossseealso(xsc.Element):
	"""
	A cross-reference from one GlossEntry to another
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class otherterm(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class glossterm(xsc.Element):
	"""
	A glossary term
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class linkend(xsc.TextAttr): pass
		class baseform(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class graphic(xsc.Element):
	"""
	A displayed graphical object (not an inline)
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class entityref(xsc.TextAttr): pass
		class fileref(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class srccredit(xsc.TextAttr): pass
		class width(xsc.TextAttr): pass
		class depth(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class scale(xsc.TextAttr): pass
		class scalefit(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class graphicco(xsc.Element):
	"""
	A graphic that contains callout areas
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class group(xsc.Element):
	"""
	A group of elements in a CmdSynopsis
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class choice(xsc.TextAttr): pass
		class rep(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class guibutton(xsc.Element):
	"""
	The text on a button in a GUI
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class guiicon(xsc.Element):
	"""
	Graphic and/or text appearing as a icon in a GUI
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class guilabel(xsc.Element):
	"""
	The text of a label in a GUI
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class guimenu(xsc.Element):
	"""
	The name of a menu in a GUI
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class guimenuitem(xsc.Element):
	"""
	The name of a terminal menu item in a GUI
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class guisubmenu(xsc.Element):
	"""
	The name of a submenu in a GUI
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class hardware(xsc.Element):
	"""
	A physical part of a computer system
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class highlights(xsc.Element):
	"""
	A summary of the main points of the discussed component
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class holder(xsc.Element):
	"""
	The name of the individual or organization that holds a copyright
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class honorific(xsc.Element):
	"""
	The title of a person
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class imagedata(xsc.Element):
	"""
	Pointer to external image data
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class entityref(xsc.TextAttr): pass
		class fileref(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class srccredit(xsc.TextAttr): pass
		class width(xsc.TextAttr): pass
		class depth(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class scale(xsc.TextAttr): pass
		class scalefit(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class imageobject(xsc.Element):
	"""
	A wrapper for image data and its associated meta-information
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class imageobjectco(xsc.Element):
	"""
	A wrapper for an image object with callouts
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class important(xsc.Element):
	"""
	An admonition set off from the text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class index(xsc.Element):
	"""
	An index
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class indexdiv(xsc.Element):
	"""
	A division in an index
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class indexentry(xsc.Element):
	"""
	An entry in an index
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class indexinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class indexterm(xsc.Element):
	"""
	A wrapper for terms to be indexed
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class pagenum(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class significance(xsc.TextAttr): pass
		class class_(xsc.TextAttr): xmlname = "class"
		class startref(xsc.TextAttr): pass
		class zone(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class informalequation(xsc.Element):
	"""
	A displayed mathematical equation without a title
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class informalexample(xsc.Element):
	"""
	A displayed example without a title
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class width(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class informalfigure(xsc.Element):
	"""
	A untitled figure
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class float(xsc.TextAttr): pass
		class pgwide(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class informaltable(xsc.Element):
	"""
	A table without a title
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class frame(xsc.TextAttr): pass
		class colsep(xsc.TextAttr): pass
		class rowsep(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass
		class tabstyle(xsc.TextAttr): pass
		class tocentry(xsc.TextAttr): pass
		class shortentry(xsc.TextAttr): pass
		class orient(xsc.TextAttr): pass
		class pgwide(xsc.TextAttr): pass

class initializer(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class inlineequation(xsc.Element):
	"""
	A mathematical equation or expression occurring inline
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class inlinegraphic(xsc.Element):
	"""
	An object containing or pointing to graphical data that will be rendered inline
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class entityref(xsc.TextAttr): pass
		class fileref(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class srccredit(xsc.TextAttr): pass
		class width(xsc.TextAttr): pass
		class depth(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class scale(xsc.TextAttr): pass
		class scalefit(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class inlinemediaobject(xsc.Element):
	"""
	An inline media object (video, audio, image, and so on)
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class interface(xsc.Element):
	"""
	An element of a GUI
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class interfacename(xsc.Element):
	"""
	The name of a formal specification of a GUI
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class invpartnumber(xsc.Element):
	"""
	An inventory part number
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class isbn(xsc.Element):
	"""
	The International Standard Book Number of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class issn(xsc.Element):
	"""
	The International Standard Serial Number of a periodical
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class issuenum(xsc.Element):
	"""
	The number of an issue of a journal
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class itemizedlist(xsc.Element):
	"""
	A list in which each entry is marked with a bullet or other dingbat
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class spacing(xsc.TextAttr): pass
		class mark(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class itermset(xsc.Element):
	"""
	A set of index terms in the meta-information of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class jobtitle(xsc.Element):
	"""
	The title of an individual in an organization
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class keycap(xsc.Element):
	"""
	The text printed on a key on a keyboard
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class keycode(xsc.Element):
	"""
	The internal, frequently numeric, identifier for a key on a
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class keycombo(xsc.Element):
	"""
	A combination of input actions
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class action(xsc.TextAttr): pass
		class otheraction(xsc.TextAttr): pass
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class keysym(xsc.Element):
	"""
	The symbolic name of a key on a keyboard
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class keyword(xsc.Element):
	"""
	One of a set of keywords describing the content of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class keywordset(xsc.Element):
	"""
	A set of keywords describing the content of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class label(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class legalnotice(xsc.Element):
	"""
	A statement of legal obligations or requirements
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class lineage(xsc.Element):
	"""
	The portion of a person's name indicating a relationship to ancestors
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class lineannotation(xsc.Element):
	"""
	A comment on a line in a verbatim listing
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class link(xsc.Element):
	"""
	A hypertext link
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class endterm(xsc.TextAttr): pass
		class linkend(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class listitem(xsc.Element):
	"""
	A wrapper for the elements of a list item
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class override(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class literal(xsc.Element):
	"""
	Inline text that is some literal value
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class literallayout(xsc.Element):
	"""
	A block of text in which line breaks and white space are to be reproduced faithfully
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class width(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class linenumbering(xsc.TextAttr): pass
		class class_(xsc.TextAttr): xmlname = "class"
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class lot(xsc.Element):
	"""
	 A list of the titles of formal objects (as tables or figures) in a document 
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class lotentry(xsc.Element):
	"""
	An entry in a list of titles
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class srccredit(xsc.TextAttr): pass
		class pagenum(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class linkend(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class manvolnum(xsc.Element):
	"""
	A reference volume number
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class markup(xsc.Element):
	"""
	A string of formatting markup in text that is to be represented literally
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class medialabel(xsc.Element):
	"""
	A name that identifies the physical medium on which some information resides
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class mediaobject(xsc.Element):
	"""
	A displayed media object (video, audio, image, etc.)
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class mediaobjectco(xsc.Element):
	"""
	A media object that contains callouts
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class member(xsc.Element):
	"""
	An element of a simple list
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class menuchoice(xsc.Element):
	"""
	A selection or series of selections from a menu
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class methodname(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class methodparam(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass
		class choice(xsc.TextAttr): pass
		class rep(xsc.TextAttr): pass

class methodsynopsis(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class modespec(xsc.Element):
	"""
	Application-specific information necessary for the completion of an OLink
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class application(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class modifier(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class mousebutton(xsc.Element):
	"""
	The conventional name of a mouse button
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msg(xsc.Element):
	"""
	A message in a message set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msgaud(xsc.Element):
	"""
	The audience to which a message in a message set is relevant
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msgentry(xsc.Element):
	"""
	A wrapper for an entry in a message set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msgexplan(xsc.Element):
	"""
	Explanatory material relating to a message in a message set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msginfo(xsc.Element):
	"""
	Information about a message in a message set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msglevel(xsc.Element):
	"""
	The level of importance or severity of a message in a message set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msgmain(xsc.Element):
	"""
	The primary component of a message in a message set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msgorig(xsc.Element):
	"""
	The origin of a message in a message set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msgrel(xsc.Element):
	"""
	A related component of a message in a message set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msgset(xsc.Element):
	"""
	A detailed set of messages, usually error messages
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msgsub(xsc.Element):
	"""
	A subcomponent of a message in a message set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class msgtext(xsc.Element):
	"""
	The actual text of a message component in a message set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class note(xsc.Element):
	"""
	A message set off from the text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class objectinfo(xsc.Element):
	"""
	Meta-information for an object
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class olink(xsc.Element):
	"""
	A link that addresses its target indirectly, through an entity
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class targetdocent(xsc.TextAttr): pass
		class linkmode(xsc.TextAttr): pass
		class localinfo(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class ooclass(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class ooexception(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class oointerface(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class option(xsc.Element):
	"""
	An option for a software command
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class optional(xsc.Element):
	"""
	Optional information
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class orderedlist(xsc.Element):
	"""
	A list in which each entry is marked with a sequentially incremented label
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class numeration(xsc.TextAttr): pass
		class inheritnum(xsc.TextAttr): pass
		class continuation(xsc.TextAttr): pass
		class spacing(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class orgdiv(xsc.Element):
	"""
	A division of an organization
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class orgname(xsc.Element):
	"""
	The name of an organization other than a corporation
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class otheraddr(xsc.Element):
	"""
	Uncategorized information in address
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class othercredit(xsc.Element):
	"""
	A person or entity, other than an author or editor, credited in a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class othername(xsc.Element):
	"""
	A component of a persons name that is not a first name, surname, or lineage
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class pagenums(xsc.Element):
	"""
	The numbers of the pages in a book, for use in a bibliographic entry
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class para(xsc.Element):
	"""
	A paragraph
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class paramdef(xsc.Element):
	"""
	Information about a function parameter in a programming language
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class parameter(xsc.Element):
	"""
	A value or a symbolic reference to a value
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class part(xsc.Element):
	"""
	A division in a book
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class partinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class partintro(xsc.Element):
	"""
	An introduction to the contents of a part
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class phone(xsc.Element):
	"""
	A telephone number
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class phrase(xsc.Element):
	"""
	A span of text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class pob(xsc.Element):
	"""
	A post office box in an address
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class postcode(xsc.Element):
	"""
	A postal code in an address
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class preface(xsc.Element):
	"""
	Introductory matter preceding the first chapter of a book
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class prefaceinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class primary(xsc.Element):
	"""
	The primary word or phrase under which an index term should be sorted
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class sortas(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class primaryie(xsc.Element):
	"""
	A primary term in an index entry, not in the text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class linkends(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class printhistory(xsc.Element):
	"""
	The printing history of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class procedure(xsc.Element):
	"""
	A list of operations to be performed in a well-defined sequence
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class productname(xsc.Element):
	"""
	The formal name of a product
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class productnumber(xsc.Element):
	"""
	A number assigned to a product
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class programlisting(xsc.Element):
	"""
	A literal listing of all or part of a program
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class width(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class linenumbering(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class programlistingco(xsc.Element):
	"""
	A program listing with associated areas used in callouts
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class prompt(xsc.Element):
	"""
	A character or string indicating the start of an input field in a computer display
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class property(xsc.Element):
	"""
	A unit of data associated with some part of a computer system
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class pubdate(xsc.Element):
	"""
	The date of publication of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class publisher(xsc.Element):
	"""
	The publisher of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class publishername(xsc.Element):
	"""
	The name of the publisher of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class pubsnumber(xsc.Element):
	"""
	A number assigned to a publication other than an ISBN or ISSN or inventory part number
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class qandadiv(xsc.Element):
	"""
	A titled division in a QandASet
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class qandaentry(xsc.Element):
	"""
	A question/answer set within a QandASet
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class qandaset(xsc.Element):
	"""
	A question-and-answer set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class defaultlabel(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class question(xsc.Element):
	"""
	A question in a QandASet
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class quote(xsc.Element):
	"""
	An inline quotation
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refclass(xsc.Element):
	"""
	The scope or other indication of applicability of a reference entry 
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refdescriptor(xsc.Element):
	"""
	A description of the topic of a reference page
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refentry(xsc.Element):
	"""
	A reference page (originally a UNIX man-style reference page)
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refentryinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refentrytitle(xsc.Element):
	"""
	The title of a reference page
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class reference(xsc.Element):
	"""
	A collection of reference entries
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class referenceinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refmeta(xsc.Element):
	"""
	Meta-information for a reference entry
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refmiscinfo(xsc.Element):
	"""
	Meta-information for a reference entry other than the title and volume number 
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refname(xsc.Element):
	"""
	The name of (one of) the subject(s) of a reference page
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refnamediv(xsc.Element):
	"""
	The name, purpose, and classification of a reference page
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refpurpose(xsc.Element):
	"""
	A short (one sentence) synopsis of the topic of a reference page
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refsect1(xsc.Element):
	"""
	A major subsection of a reference entry
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refsect1info(xsc.Element):
	"""
	Meta-information for a RefSect1
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refsect2(xsc.Element):
	"""
	A subsection of a RefSect1
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refsect2info(xsc.Element):
	"""
	Meta-information for a RefSect2
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refsect3(xsc.Element):
	"""
	A subsection of a RefSect2
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refsect3info(xsc.Element):
	"""
	Meta-information for a RefSect3
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refsynopsisdiv(xsc.Element):
	"""
	A syntactic synopsis of the subject of the reference page
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class refsynopsisdivinfo(xsc.Element):
	"""
	Meta-information for a RefSynopsisDiv
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class releaseinfo(xsc.Element):
	"""
	Information about a particular release of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class remark(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class replaceable(xsc.Element):
	"""
	Content that may or must be replaced by the user
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class returnvalue(xsc.Element):
	"""
	The value returned by a function
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class revdescription(xsc.Element):
	"""

	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class revhistory(xsc.Element):
	"""
	A history of the revisions to a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class revision(xsc.Element):
	"""
	An entry describing a single revision in the history of the revisions to a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class revnumber(xsc.Element):
	"""
	A document revision number
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class revremark(xsc.Element):
	"""
	A description of a revision to a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class row(xsc.Element):
	"""
	A row in a table
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class rowsep(xsc.TextAttr): pass
		class valign(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sbr(xsc.Element):
	"""
	An explicit line break in a command synopsis
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class screen(xsc.Element):
	"""
	Text that a user sees or might see on a computer screen
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class width(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class linenumbering(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class screenco(xsc.Element):
	"""
	A screen with associated areas used in callouts
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class screeninfo(xsc.Element):
	"""
	Information about how a screen shot was produced
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class screenshot(xsc.Element):
	"""
	A representation of what the user sees or might see on a computer screen
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class secondary(xsc.Element):
	"""
	A secondary word or phrase in an index term
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class sortas(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class secondaryie(xsc.Element):
	"""
	A secondary term in an index entry, rather than in the text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class linkends(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sect1(xsc.Element):
	"""
	A top-level section of document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class renderas(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sect1info(xsc.Element):
	"""
	Meta-information for a Sect1
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sect2(xsc.Element):
	"""
	A subsection within a Sect1
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class renderas(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sect2info(xsc.Element):
	"""
	Meta-information for a Sect2
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sect3(xsc.Element):
	"""
	A subsection within a Sect2
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class renderas(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sect3info(xsc.Element):
	"""
	Meta-information for a Sect3
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sect4(xsc.Element):
	"""
	A subsection within a Sect3
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class renderas(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sect4info(xsc.Element):
	"""
	Meta-information for a Sect4
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sect5(xsc.Element):
	"""
	A subsection within a Sect4
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class renderas(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sect5info(xsc.Element):
	"""
	Meta-information for a Sect5
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class section(xsc.Element):
	"""
	A recursive section
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sectioninfo(xsc.Element):
	"""
	Meta-information for a recursive section
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class see(xsc.Element):
	"""
	Part of an index term directing the reader instead to another entry in the index
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class seealso(xsc.Element):
	"""
	Part of an index term directing the reader also to another entry in the index
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class seealsoie(xsc.Element):
	"""
	A "See also" entry in an index, rather than in the text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class linkends(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class seeie(xsc.Element):
	"""
	A "See" entry in an index, rather than in the text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class linkend(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class seg(xsc.Element):
	"""
	An element of a list item in a segmented list
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class seglistitem(xsc.Element):
	"""
	A list item in a segmented list
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class segmentedlist(xsc.Element):
	"""
	A segmented list, a list of sets of elements
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class segtitle(xsc.Element):
	"""
	The title of an element of a list item in a segmented list
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class seriesvolnums(xsc.Element):
	"""
	Numbers of the volumes in a series of books
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class set(xsc.Element):
	"""
	A collection of books
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class fpi(xsc.TextAttr): pass
		class status(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class setindex(xsc.Element):
	"""
	An index to a set of books
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class setindexinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class setinfo(xsc.Element):
	"""
	Meta-information for a Set
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class contents(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sgmltag(xsc.Element):
	"""
	A component of SGML markup
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class shortaffil(xsc.Element):
	"""
	A brief description of an affiliation
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class shortcut(xsc.Element):
	"""
	A key combination for an action that is also accessible through a menu
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class action(xsc.TextAttr): pass
		class otheraction(xsc.TextAttr): pass
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sidebar(xsc.Element):
	"""
	A portion of a document that is isolated from the main narrative flow
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class sidebarinfo(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class simpara(xsc.Element):
	"""
	A paragraph that contains only text and inline markup, no block elements
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class simplelist(xsc.Element):
	"""
	An undecorated list of single words or short phrases
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class columns(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class simplemsgentry(xsc.Element):
	"""
	
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass
		class audience(xsc.TextAttr): pass
		class level(xsc.TextAttr): pass
		class origin(xsc.TextAttr): pass

class simplesect(xsc.Element):
	"""
	A section of a document with no subdivisions
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class spanspec(xsc.Element):
	"""
	Formatting information for a spanned column in a table
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class namest(xsc.TextAttr): pass
		class nameend(xsc.TextAttr): pass
		class spanname(xsc.TextAttr): pass
		class colsep(xsc.TextAttr): pass
		class rowsep(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class char(xsc.TextAttr): pass
		class charoff(xsc.TextAttr): pass

class state(xsc.Element):
	"""
	A state or province in an address
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class step(xsc.Element):
	"""
	A unit of action in a procedure
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class performance(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class street(xsc.Element):
	"""
	A street address in an address
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class structfield(xsc.Element):
	"""
	A field in a structure (in the programming language sense)
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class structname(xsc.Element):
	"""
	The name of a structure (in the programming language sense)
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class subject(xsc.Element):
	"""
	One of a group of terms describing the subject matter of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class weight(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class subjectset(xsc.Element):
	"""
	A set of terms describing the subject matter of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class scheme(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class subjectterm(xsc.Element):
	"""
	A term in a group of terms describing the subject matter of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class subscript(xsc.Element):
	"""
	A subscript (as in H2O, the molecular formula for water)
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class substeps(xsc.Element):
	"""
	A wrapper for steps that occur within steps in a procedure
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class performance(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class subtitle(xsc.Element):
	"""
	The subtitle of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class superscript(xsc.Element):
	"""
	A superscript (as in x2, the mathematical notation for x multiplied by itself)
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class surname(xsc.Element):
	"""
	A family name, in western cultures the "last name"
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class symbol(xsc.Element):
	"""
	A name that is replaced by a value before processing
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class synopfragment(xsc.Element):
	"""
	A portion of a CmdSynopsis broken out from the main body of the synopsis
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class synopfragmentref(xsc.Element):
	"""
	A reference to a fragment of a command synopsis
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class linkend(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class synopsis(xsc.Element):
	"""
	A general-purpose element for representing the syntax of commands or functions
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class linenumbering(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class systemitem(xsc.Element):
	"""
	A system-related item or term
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class table(xsc.Element):
	"""
	A formal table in a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class frame(xsc.TextAttr): pass
		class colsep(xsc.TextAttr): pass
		class rowsep(xsc.TextAttr): pass
		class tabstyle(xsc.TextAttr): pass
		class tocentry(xsc.TextAttr): pass
		class shortentry(xsc.TextAttr): pass
		class orient(xsc.TextAttr): pass
		class pgwide(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tbody(xsc.Element):
	"""
	A wrapper for the rows of a table or informal table
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class valign(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class term(xsc.Element):
	"""
	The word or phrase being defined or described in a variable list
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tertiary(xsc.Element):
	"""
	A tertiary word or phrase in an index term
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class sortas(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tertiaryie(xsc.Element):
	"""
	A tertiary term in an index entry, rather than in the text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class linkends(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class textobject(xsc.Element):
	"""
	A wrapper for a text description of an object and its associated meta-information
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tfoot(xsc.Element):
	"""
	A table footer consisting of one or more rows
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class valign(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tgroup(xsc.Element):
	"""
	A wrapper for the main content of a table, or part of a table
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class cols(xsc.TextAttr): pass
		class tgroupstyle(xsc.TextAttr): pass
		class colsep(xsc.TextAttr): pass
		class rowsep(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class char(xsc.TextAttr): pass
		class charoff(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class thead(xsc.Element):
	"""
	A table header consisting of one or more rows
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class valign(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tip(xsc.Element):
	"""
	A suggestion to the user, set off from the text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class title(xsc.Element):
	"""
	The text of the title of a section of a document or of a formal block-level element
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class pagenum(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class titleabbrev(xsc.Element):
	"""
	The abbreviation of a Title
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class toc(xsc.Element):
	"""
	A table of contents
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class pagenum(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tocback(xsc.Element):
	"""
	An entry in a table of contents for a back matter component
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class linkend(xsc.TextAttr): pass
		class pagenum(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tocchap(xsc.Element):
	"""
	An entry in a table of contents for a component in the body of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tocentry(xsc.Element):
	"""
	A component title in a table of contents
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class linkend(xsc.TextAttr): pass
		class pagenum(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tocfront(xsc.Element):
	"""
	An entry in a table of contents for a front matter component
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class label(xsc.TextAttr): pass
		class linkend(xsc.TextAttr): pass
		class pagenum(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class toclevel1(xsc.Element):
	"""
	A top-level entry within a table of contents entry for a chapter-like component
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class toclevel2(xsc.Element):
	"""
	A second-level entry within a table of contents entry for a chapter-like component
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class toclevel3(xsc.Element):
	"""
	A third-level entry within a table of contents entry for a chapter-like component
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class toclevel4(xsc.Element):
	"""
	A fourth-level entry within a table of contents entry for a chapter-like component
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class toclevel5(xsc.Element):
	"""
	A fifth-level entry within a table of contents entry for a chapter-like component
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class tocpart(xsc.Element):
	"""
	An entry in a table of contents for a part of a book
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class token(xsc.Element):
	"""
	A unit of information
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class trademark(xsc.Element):
	"""
	A trademark
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class class_(xsc.TextAttr): xmlname = "class"
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class type(xsc.Element):
	"""
	The classification of a value
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class ulink(xsc.Element):
	"""
	A link that addresses its target by means of a URL (Uniform Resource Locator)
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class url(xsc.URLAttr): pass
		class type(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class userinput(xsc.Element):
	"""
	Data entered by the user
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class moreinfo(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class varargs(xsc.Element):
	"""
	An empty element in a function synopsis indicating a variable number of arguments
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class variablelist(xsc.Element):
	"""
	A list in which each entry is composed of a set of one or more terms and an associated description
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class termlength(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class varlistentry(xsc.Element):
	"""
	A wrapper for a set of terms and the associated description in a variable list
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class varname(xsc.Element):
	"""
	The name of a variable
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class videodata(xsc.Element):
	"""
	Pointer to external video data
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class entityref(xsc.TextAttr): pass
		class fileref(xsc.TextAttr): pass
		class format(xsc.TextAttr): pass
		class srccredit(xsc.TextAttr): pass
		class width(xsc.TextAttr): pass
		class depth(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class scale(xsc.TextAttr): pass
		class scalefit(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class videoobject(xsc.Element):
	"""
	A wrapper for video data and its associated meta-information
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class void(xsc.Element):
	"""
	An empty element in a function synopsis indicating that the function in question takes no arguments
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class volumenum(xsc.Element):
	"""
	The volume number of a document in a set (as of books in a set or articles in a journal)
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class warning(xsc.Element):
	"""
	An admonition set off from the text
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class wordasword(xsc.Element):
	"""
	A word meant specifically as a word and not representing anything else
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class xref(xsc.Element):
	"""
	A cross reference to another part of the document
	"""
	empty = True
	class Attrs(xsc.Element.Attrs):
		class endterm(xsc.TextAttr): pass
		class linkend(xsc.TextAttr): pass
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class year(xsc.Element):
	"""
	The year of publication of a document
	"""
	empty = False
	class Attrs(xsc.Element.Attrs):
		class id(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class remap(xsc.TextAttr): pass
		class xreflabel(xsc.TextAttr): pass
		class revisionflag(xsc.TextAttr): pass
		class arch(xsc.TextAttr): pass
		class condition(xsc.TextAttr): pass
		class conformance(xsc.TextAttr): pass
		class os(xsc.TextAttr): pass
		class revision(xsc.TextAttr): pass
		class security(xsc.TextAttr): pass
		class userlevel(xsc.TextAttr): pass
		class vendor(xsc.TextAttr): pass
		class role(xsc.TextAttr): pass

class xmlns(xsc.Namespace):
	xmlname = "docbook"
	xmlurl = "http://www.oasis-open.org/docbook/xml/4.0/docbookx.dtd"
xmlns.makemod(vars())

