# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True
 
## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST namespace module that contains definitions for all the elements in
`DocBook 5.0`__.

__ http://www.docbook.org/schemas/5x.html
"""

 
from ll.xist import xsc, sims
 
 
__docformat__ = "reStructuredText"


xmlns = "http://docbook.org/ns/docbook"


class annotations(xsc.Element.Attrs):
	class annotations(xsc.TextAttr): pass


class arch(xsc.Element.Attrs):
	class arch(xsc.TextAttr): pass


class audience(xsc.Element.Attrs):
	class audience(xsc.TextAttr): pass


class condition(xsc.Element.Attrs):
	class condition(xsc.TextAttr): pass


class conformance(xsc.Element.Attrs):
	class conformance(xsc.TextAttr): pass


class dir(xsc.Element.Attrs):
	class dir(xsc.TextAttr): values = ("ltr", "rtl", "lro", "rlo")


class linkend(xsc.Element.Attrs):
	class linkend(xsc.TextAttr): pass


class os(xsc.Element.Attrs):
	class os(xsc.TextAttr): pass


class remap(xsc.Element.Attrs):
	class remap(xsc.TextAttr): pass


class revision2(xsc.Element.Attrs):
	class revision(xsc.TextAttr): pass


class revisionflag(xsc.Element.Attrs):
	class revisionflag(xsc.TextAttr): values = ("changed", "added", "deleted", "off")


class role(xsc.Element.Attrs):
	class role(xsc.TextAttr): pass


class security(xsc.Element.Attrs):
	class security(xsc.TextAttr): pass


class userlevel(xsc.Element.Attrs):
	class userlevel(xsc.TextAttr): pass


class vendor(xsc.Element.Attrs):
	class vendor(xsc.TextAttr): pass


class version(xsc.Element.Attrs):
	class version(xsc.TextAttr): pass


class wordsize(xsc.Element.Attrs):
	class wordsize(xsc.TextAttr): pass


class xreflabel(xsc.Element.Attrs):
	class xreflabel(xsc.TextAttr): pass


class label2(xsc.Element.Attrs):
	class label(xsc.TextAttr): pass


class status(xsc.Element.Attrs):
	class status(xsc.TextAttr): pass


class continuation(xsc.Element.Attrs):
	class continuation(xsc.TextAttr): values = ("continues", "restarts")


class language(xsc.Element.Attrs):
	class language(xsc.TextAttr): pass


class linenumbering(xsc.Element.Attrs):
	class linenumbering(xsc.TextAttr): values = ("numbered", "unnumbered")


class startinglinenumber(xsc.Element.Attrs):
	class startinglinenumber(xsc.TextAttr): pass


class linkends(xsc.Element.Attrs):
	class linkends(xsc.TextAttr): pass


class otherunits(xsc.Element.Attrs):
	class otherunits(xsc.TextAttr): pass


class units(xsc.Element.Attrs):
	class units(xsc.TextAttr): values = ("calspair", "linecolumn", "linecolumnpair", "linerange", "other")


class choice(xsc.Element.Attrs):
	class choice(xsc.TextAttr): values = ("opt", "plain", "req")


class rep(xsc.Element.Attrs):
	class rep(xsc.TextAttr): values = ("norepeat", "repeat")


class entityref(xsc.Element.Attrs):
	class entityref(xsc.TextAttr): pass


class fileref(xsc.Element.Attrs):
	class fileref(xsc.TextAttr): pass


class format(xsc.Element.Attrs):
	class format(xsc.TextAttr): pass


class class_(xsc.Element.Attrs):
	class class_(xsc.TextAttr):
		xmlname = "class"
		values = ("doi", "isbn", "isrn", "issn", "libraryofcongress", "pubsnumber", "uri", "other")


class otherclass(xsc.Element.Attrs):
	class otherclass(xsc.TextAttr): pass


class relation(xsc.Element.Attrs):
	class relation(xsc.TextAttr): pass


class endterm(xsc.Element.Attrs):
	class endterm(xsc.TextAttr): pass


class xrefstyle(xsc.Element.Attrs):
	class xrefstyle(xsc.TextAttr): pass


class class2(xsc.Element.Attrs):
	class class_(xsc.TextAttr): xmlname = "class"


class lang(xsc.Element.Attrs):
	class lang(xsc.TextAttr): pass


class onclick(xsc.Element.Attrs):
	class onclick(xsc.TextAttr): pass


class ondblclick(xsc.Element.Attrs):
	class ondblclick(xsc.TextAttr): pass


class onkeydown(xsc.Element.Attrs):
	class onkeydown(xsc.TextAttr): pass


class onkeypress(xsc.Element.Attrs):
	class onkeypress(xsc.TextAttr): pass


class onkeyup(xsc.Element.Attrs):
	class onkeyup(xsc.TextAttr): pass


class onmousedown(xsc.Element.Attrs):
	class onmousedown(xsc.TextAttr): pass


class onmousemove(xsc.Element.Attrs):
	class onmousemove(xsc.TextAttr): pass


class onmouseout(xsc.Element.Attrs):
	class onmouseout(xsc.TextAttr): pass


class onmouseover(xsc.Element.Attrs):
	class onmouseover(xsc.TextAttr): pass


class onmouseup(xsc.Element.Attrs):
	class onmouseup(xsc.TextAttr): pass


class style(xsc.Element.Attrs):
	class style(xsc.TextAttr): pass


class title2(xsc.Element.Attrs):
	class title(xsc.TextAttr): pass


class align(xsc.Element.Attrs):
	class align(xsc.TextAttr): values = ("left", "center", "right", "justify", "char")


class char(xsc.Element.Attrs):
	class char(xsc.TextAttr): pass


class charoff(xsc.Element.Attrs):
	class charoff(xsc.TextAttr): pass


class span(xsc.Element.Attrs):
	class span(xsc.TextAttr): pass


class valign(xsc.Element.Attrs):
	class valign(xsc.TextAttr): values = ("top", "middle", "bottom", "baseline")


class width(xsc.Element.Attrs):
	class width(xsc.TextAttr): pass


class align2(xsc.Element.Attrs):
	class align(xsc.TextAttr): values = ("center", "char", "justify", "left", "right")


class colname(xsc.Element.Attrs):
	class colname(xsc.TextAttr): pass


class colsep(xsc.Element.Attrs):
	class colsep(xsc.TextAttr): values = (0, 1)


class rowsep(xsc.Element.Attrs):
	class rowsep(xsc.TextAttr): values = (0, 1)


class class3(xsc.Element.Attrs):
	class class_(xsc.BoolAttr): xmlname = "class"


class nameend(xsc.Element.Attrs):
	class nameend(xsc.TextAttr): pass


class namest(xsc.Element.Attrs):
	class namest(xsc.TextAttr): pass


class spanname(xsc.Element.Attrs):
	class spanname(xsc.TextAttr): pass


class valign2(xsc.Element.Attrs):
	class valign(xsc.TextAttr): values = ("bottom", "middle", "top")


class tgroupstyle(xsc.Element.Attrs):
	class tgroupstyle(xsc.TextAttr): pass


class floatstyle(xsc.Element.Attrs):
	class floatstyle(xsc.TextAttr): pass


class pgwide(xsc.Element.Attrs):
	class pgwide(xsc.TextAttr): values = (0, 1)


class baseform(xsc.Element.Attrs):
	class baseform(xsc.TextAttr): pass


class sortas(xsc.Element.Attrs):
	class sortas(xsc.TextAttr): pass


class otherterm(xsc.Element.Attrs):
	class otherterm(xsc.TextAttr): pass


class contentdepth(xsc.Element.Attrs):
	class contentdepth(xsc.TextAttr): pass


class contentwidth(xsc.Element.Attrs):
	class contentwidth(xsc.TextAttr): pass


class depth(xsc.Element.Attrs):
	class depth(xsc.TextAttr): pass


class scale(xsc.Element.Attrs):
	class scale(xsc.TextAttr): pass


class scalefit(xsc.Element.Attrs):
	class scalefit(xsc.TextAttr): values = (0, 1)


class type2(xsc.Element.Attrs):
	class type(xsc.TextAttr): pass


class pagenum(xsc.Element.Attrs):
	class pagenum(xsc.TextAttr): pass


class border(xsc.Element.Attrs):
	class border(xsc.TextAttr): pass


class cellpadding(xsc.Element.Attrs):
	class cellpadding(xsc.TextAttr): pass


class cellspacing(xsc.Element.Attrs):
	class cellspacing(xsc.TextAttr): pass


class frame(xsc.Element.Attrs):
	class frame(xsc.TextAttr): values = ("all", "bottom", "none", "sides", "top", "topbot", "void", "above", "below", "hsides", "lhs", "rhs", "vsides", "box", "border")


class orient(xsc.Element.Attrs):
	class orient(xsc.TextAttr): values = ("land", "port")


class rowheader(xsc.Element.Attrs):
	class rowheader(xsc.TextAttr): values = ("firstcol", "norowheader")


class rules(xsc.Element.Attrs):
	class rules(xsc.TextAttr): values = ("none", "groups", "rows", "cols", "all")


class summary(xsc.Element.Attrs):
	class summary(xsc.TextAttr): pass


class tabstyle(xsc.Element.Attrs):
	class tabstyle(xsc.TextAttr): pass


class spacing(xsc.Element.Attrs):
	class spacing(xsc.TextAttr): values = ("compact", "normal")


class action(xsc.Element.Attrs):
	class action(xsc.TextAttr): values = ("click", "double-click", "press", "seq", "simul", "other")


class otheraction(xsc.Element.Attrs):
	class otheraction(xsc.TextAttr): pass


class class4(xsc.Element.Attrs):
	class class_(xsc.TextAttr):
		xmlname = "class"
		values = ("copyright", "registered", "service", "trade")


class performance(xsc.Element.Attrs):
	class performance(xsc.TextAttr): values = ("optional", "required")


class valign3(xsc.Element.Attrs):
	class valign(xsc.TextAttr): values = ("bottom", "middle", "top", "baseline")


class abbr(xsc.Element.Attrs):
	class abbr(xsc.TextAttr): pass


class axis(xsc.Element.Attrs):
	class axis(xsc.TextAttr): pass


class colspan(xsc.Element.Attrs):
	class colspan(xsc.TextAttr): pass


class headers(xsc.Element.Attrs):
	class headers(xsc.TextAttr): pass


class rowspan(xsc.Element.Attrs):
	class rowspan(xsc.TextAttr): pass


class scope(xsc.Element.Attrs):
	class scope(xsc.TextAttr): values = ("row", "col", "rowgroup", "colgroup")


class abbrev(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class abstract(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class accel(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class acknowledgements(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class acronym(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class address(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, continuation, dir, language, linenumbering, linkend, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, version, wordsize, xreflabel):
		pass


class affiliation(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class alt(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class anchor(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class annotation(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class annotates(xsc.TextAttr): pass


class answer(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class appendix(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class application(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("hardware", "software")


class arc(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class area(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkends, os, otherunits, remap, revision2, revisionflag, role, security, units, userlevel, vendor, version, wordsize, xreflabel):
		class coords(xsc.TextAttr): required = True


class areaset(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkends, os, otherunits, remap, revision2, revisionflag, role, security, units, userlevel, vendor, version, wordsize, xreflabel):
		pass


class areaspec(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, otherunits, remap, revision2, revisionflag, role, security, units, userlevel, vendor, version, wordsize, xreflabel):
		pass


class arg(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, choice, condition, conformance, dir, linkend, os, remap, rep, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class article(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("faq", "journalarticle", "productsheet", "specification", "techreport", "whitepaper")


class artpagenums(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class attribution(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class audiodata(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, entityref, fileref, format, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class audioobject(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class author(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class authorgroup(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class authorinitials(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class bibliocoverage(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class otherspatial(xsc.TextAttr): pass
		class othertemporal(xsc.TextAttr): pass
		class spatial(xsc.TextAttr): values = ("dcmipoint", "iso3166", "dcmibox", "tgn", "otherspatial")
		class temporal(xsc.TextAttr): values = ("dcmiperiod", "w3c-dtf", "othertemporal")


class bibliodiv(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class biblioentry(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class bibliography(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class biblioid(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, class_, condition, conformance, dir, linkend, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class bibliolist(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class bibliomisc(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class bibliomixed(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class bibliomset(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, relation, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class biblioref(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, endterm, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel, xrefstyle):
		class begin(xsc.TextAttr): pass
		class end(xsc.TextAttr): pass
		class units(xsc.TextAttr): pass


class bibliorelation(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, class_, condition, conformance, dir, linkend, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class othertype(xsc.TextAttr): pass
		class type(xsc.TextAttr): values = ("hasformat", "haspart", "hasversion", "isformatof", "ispartof", "isreferencedby", "isreplacedby", "isrequiredby", "isversionof", "references", "replaces", "requires", "othertype")


class biblioset(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, relation, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class bibliosource(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, class_, condition, conformance, dir, linkend, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class blockquote(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class book(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class bridgehead(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class otherrenderas(xsc.TextAttr): pass
		class renderas(xsc.TextAttr): values = ("sect1", "sect2", "sect3", "sect4", "sect5", "other")


class callout(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class arearefs(xsc.TextAttr): required = True


class calloutlist(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class caption(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, class2, condition, conformance, dir, lang, linkend, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, security, style, title2, userlevel, vendor, version, wordsize, xreflabel):
		pass


class caution(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class chapter(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class citation(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class citebiblioid(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, class_, condition, conformance, dir, linkend, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class citerefentry(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class citetitle(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class pubwork(xsc.TextAttr): values = ("article", "bbs", "book", "cdrom", "chapter", "dvd", "emailmessage", "gopher", "journal", "manuscript", "newsposting", "part", "refentry", "section", "series", "set", "webpage", "wiki")


class city(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class classname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class classsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, language, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("class", "interface")


class classsynopsisinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, continuation, dir, language, linenumbering, linkend, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, version, wordsize, xreflabel):
		pass


class cmdsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class cmdlength(xsc.TextAttr): pass
		class sepchar(xsc.TextAttr): pass


class co(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkends, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class code(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, language, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class col(xsc.Element):
	xmlns = xmlns
	class Attrs(align, annotations, arch, audience, char, charoff, class2, condition, conformance, dir, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, security, span, style, title2, userlevel, valign, vendor, version, width, wordsize, xreflabel):
		pass


class colgroup(xsc.Element):
	xmlns = xmlns
	class Attrs(align, annotations, arch, audience, char, charoff, class2, condition, conformance, dir, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, security, span, style, title2, userlevel, valign, vendor, version, width, wordsize, xreflabel):
		pass


class collab(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class colophon(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class colspec(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, annotations, arch, audience, char, charoff, colname, colsep, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, rowsep, security, userlevel, vendor, version, wordsize, xreflabel):
		class colnum(xsc.TextAttr): pass
		class colwidth(xsc.TextAttr): pass


class command(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class computeroutput(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class confdates(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class confgroup(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class confnum(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class confsponsor(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class conftitle(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class constant(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, class3, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class constraint(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class constraintdef(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class constructorsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, language, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class contractnum(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class contractsponsor(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class contrib(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class copyright(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class coref(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class country(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class cover(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class database(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("altkey", "constraint", "datatype", "field", "foreignkey", "group", "index", "key1", "key2", "name", "primarykey", "procedure", "record", "rule", "secondarykey", "table", "user", "view")


class date(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class dedication(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class destructorsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, language, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class edition(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class editor(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class email(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class emphasis(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class entry(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, annotations, arch, audience, char, charoff, colname, colsep, condition, conformance, dir, linkend, nameend, namest, os, remap, revision2, revisionflag, role, rowsep, security, spanname, userlevel, valign2, vendor, version, wordsize, xreflabel):
		class morerows(xsc.TextAttr): pass
		class rotate(xsc.TextAttr): values = (0, 1)


class entrytbl(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, annotations, arch, audience, char, charoff, colname, colsep, condition, conformance, dir, linkend, nameend, namest, os, remap, revision2, revisionflag, role, rowsep, security, spanname, tgroupstyle, userlevel, vendor, version, wordsize, xreflabel):
		class cols(xsc.TextAttr): pass


class envar(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class epigraph(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class equation(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, floatstyle, label2, linkend, os, pgwide, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class errorcode(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class errorname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class errortext(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class errortype(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class example(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, floatstyle, label2, linkend, os, pgwide, remap, revision2, revisionflag, role, security, userlevel, vendor, version, width, wordsize, xreflabel):
		pass


class exceptionname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class extendedlink(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class fax(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class fieldsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, language, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class figure(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, floatstyle, label2, linkend, os, pgwide, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class filename(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("devicefile", "directory", "extension", "headerfile", "libraryfile", "partition", "symlink")
		class path(xsc.TextAttr): pass


class firstname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class firstterm(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, baseform, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class footnote(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class footnoteref(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class foreignphrase(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class formalpara(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class funcdef(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class funcparams(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class funcprototype(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class funcsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, language, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class funcsynopsisinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, continuation, dir, language, linenumbering, linkend, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, version, wordsize, xreflabel):
		pass


class function(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class glossary(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class glossdef(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class subject(xsc.TextAttr): pass


class glossdiv(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class glossentry(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, sortas, userlevel, vendor, version, wordsize, xreflabel):
		pass


class glosslist(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class glosssee(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, otherterm, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class glossseealso(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, otherterm, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class glossterm(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, baseform, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class group(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, choice, condition, conformance, dir, linkend, os, remap, rep, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class guibutton(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class guiicon(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class guilabel(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class guimenu(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class guimenuitem(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class guisubmenu(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class hardware(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class holder(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class honorific(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class imagedata(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, annotations, arch, audience, condition, conformance, contentdepth, contentwidth, depth, dir, entityref, fileref, format, os, remap, revision2, revisionflag, role, scale, scalefit, security, userlevel, valign2, vendor, version, width, wordsize, xreflabel):
		pass


class imageobject(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class imageobjectco(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class important(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class index(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, type2, userlevel, vendor, version, wordsize, xreflabel):
		pass


class indexdiv(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class indexentry(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class indexterm(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, pagenum, remap, revision2, revisionflag, role, security, type2, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("singular", "startofrange", "endofrange")
		class scope(xsc.TextAttr): values = ("all", "global", "local")
		class significance(xsc.TextAttr): values = ("normal", "preferred")
		class startref(xsc.TextAttr): pass
		class zone(xsc.TextAttr): pass


class info(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class informalequation(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class informalexample(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, floatstyle, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, width, wordsize, xreflabel):
		pass


class informalfigure(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, floatstyle, label2, linkend, os, pgwide, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class informaltable(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, border, cellpadding, cellspacing, class2, colsep, condition, conformance, dir, floatstyle, frame, lang, linkend, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, orient, os, pgwide, remap, revision2, revisionflag, role, rowheader, rowsep, rules, security, style, summary, tabstyle, title2, userlevel, vendor, version, width, wordsize, xreflabel):
		pass


class initializer(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class inlineequation(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class inlinemediaobject(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class interfacename(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class issuenum(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class itemizedlist(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, spacing, userlevel, vendor, version, wordsize, xreflabel):
		class mark(xsc.TextAttr): pass


class itermset(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class jobtitle(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class keycap(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class function(xsc.TextAttr): values = ("alt", "backspace", "command", "control", "delete", "down", "end", "enter", "escape", "home", "insert", "left", "meta", "option", "pagedown", "pageup", "right", "shift", "space", "tab", "up", "other")
		class otherfunction(xsc.TextAttr): pass


class keycode(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class keycombo(xsc.Element):
	xmlns = xmlns
	class Attrs(action, annotations, arch, audience, condition, conformance, dir, linkend, os, otheraction, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class keysym(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class keyword(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class keywordset(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class label(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class legalnotice(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class lhs(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class lineage(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class lineannotation(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class link(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, endterm, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel, xrefstyle):
		pass


class listitem(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class override(xsc.TextAttr): pass


class literal(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class literallayout(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, continuation, dir, language, linenumbering, linkend, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("monospaced", "normal")


class locator(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class manvolnum(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class markup(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class mathphrase(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class mediaobject(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class member(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class menuchoice(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class methodname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class methodparam(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, rep, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class choice(xsc.TextAttr): values = ("opt", "plain", "req")


class methodsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, language, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class modifier(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class mousebutton(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msg(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msgaud(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msgentry(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msgexplan(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msginfo(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msglevel(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msgmain(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msgorig(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msgrel(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msgset(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msgsub(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class msgtext(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class nonterminal(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class def_(xsc.TextAttr):
			xmlname = "def"
			required = True


class note(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class olink(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, os, remap, revision2, revisionflag, role, security, type2, userlevel, vendor, version, wordsize, xreflabel, xrefstyle):
		class localinfo(xsc.TextAttr): pass
		class targetdoc(xsc.TextAttr): pass
		class targetptr(xsc.TextAttr): pass


class ooclass(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class ooexception(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class oointerface(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class option(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class optional(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class orderedlist(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, continuation, dir, linkend, os, remap, revision2, revisionflag, role, security, spacing, userlevel, vendor, version, wordsize, xreflabel):
		class inheritnum(xsc.TextAttr): values = ("ignore", "inherit")
		class numeration(xsc.TextAttr): values = ("arabic", "upperalpha", "loweralpha", "upperroman", "lowerroman")
		class startingnumber(xsc.TextAttr): pass


class org(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class orgdiv(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class orgname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("consortium", "corporation", "informal", "nonprofit", "other")


class otheraddr(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class othercredit(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("copyeditor", "graphicdesigner", "other", "productioneditor", "technicaleditor", "translator")


class othername(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class package(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class pagenums(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class para(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class paramdef(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class choice(xsc.TextAttr): values = ("opt", "req")


class parameter(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("command", "function", "option")


class part(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class partintro(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class person(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class personblurb(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class personname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class phone(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class phrase(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class pob(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class postcode(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class preface(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class primary(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, sortas, userlevel, vendor, version, wordsize, xreflabel):
		pass


class primaryie(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkends, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class printhistory(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class procedure(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class production(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class productionrecap(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class productionset(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class productname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, class4, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class productnumber(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class programlisting(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, continuation, dir, language, linenumbering, linkend, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, version, width, wordsize, xreflabel):
		pass


class programlistingco(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class prompt(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class property(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class pubdate(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class publisher(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class publishername(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class qandadiv(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class qandaentry(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class qandaset(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class defaultlabel(xsc.TextAttr): values = ("none", "number", "qanda")


class question(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class quote(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refclass(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refdescriptor(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refentry(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refentrytitle(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class reference(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refmeta(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refmiscinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("source", "version", "manual", "sectdesc", "software", "other")


class refname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refnamediv(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refpurpose(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refsect1(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refsect2(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refsect3(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refsection(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class refsynopsisdiv(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class releaseinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class remark(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class replaceable(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("command", "function", "option", "parameter")


class returnvalue(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class revdescription(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class revhistory(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class revision(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class revnumber(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class revremark(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class rhs(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class row(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, rowsep, security, userlevel, valign2, vendor, version, wordsize, xreflabel):
		pass


class sbr(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class screen(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, continuation, dir, language, linenumbering, linkend, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, version, width, wordsize, xreflabel):
		pass


class screenco(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class screenshot(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class secondary(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, sortas, userlevel, vendor, version, wordsize, xreflabel):
		pass


class secondaryie(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkends, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class sect1(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class sect2(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class sect3(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class sect4(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class sect5(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class section(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class see(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class seealso(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class seealsoie(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkends, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class seeie(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class seg(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class seglistitem(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class segmentedlist(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class segtitle(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class seriesvolnums(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class set(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class setindex(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, type2, userlevel, vendor, version, wordsize, xreflabel):
		pass


class shortaffil(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class shortcut(xsc.Element):
	xmlns = xmlns
	class Attrs(action, annotations, arch, audience, condition, conformance, dir, linkend, os, otheraction, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class sidebar(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class simpara(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class simplelist(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class columns(xsc.TextAttr): pass
		class type(xsc.TextAttr): values = ("horiz", "vert", "inline")


class simplemsgentry(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class msgaud(xsc.TextAttr): pass
		class msglevel(xsc.TextAttr): pass
		class msgorig(xsc.TextAttr): pass


class simplesect(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, label2, linkend, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, version, wordsize, xreflabel):
		pass


class spanspec(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, annotations, arch, audience, char, charoff, colsep, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, rowsep, security, userlevel, vendor, version, wordsize, xreflabel):
		class nameend(xsc.TextAttr): required = True
		class namest(xsc.TextAttr): required = True
		class spanname(xsc.TextAttr): required = True


class state(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class step(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, performance, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class stepalternatives(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, performance, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class street(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class subject(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class weight(xsc.TextAttr): pass


class subjectset(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class scheme(xsc.TextAttr): pass


class subjectterm(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class subscript(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class substeps(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, performance, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class subtitle(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class superscript(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class surname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class symbol(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, class3, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class synopfragment(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class synopfragmentref(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class synopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, continuation, dir, label2, language, linenumbering, linkend, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, version, wordsize, xreflabel):
		pass


class systemitem(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("daemon", "domainname", "etheraddress", "event", "eventhandler", "filesystem", "fqdomainname", "groupname", "ipaddress", "library", "macro", "netmask", "newsgroup", "osname", "process", "protocol", "resource", "server", "service", "systemname", "username")


class table(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, border, cellpadding, cellspacing, class2, colsep, condition, conformance, dir, floatstyle, frame, label2, lang, linkend, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, orient, os, pgwide, remap, revision2, revisionflag, role, rowheader, rowsep, rules, security, style, summary, tabstyle, title2, userlevel, vendor, version, width, wordsize, xreflabel):
		class shortentry(xsc.TextAttr): values = (0, 1)
		class tocentry(xsc.TextAttr): values = (0, 1)


class tag(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = ("attribute", "attvalue", "element", "emptytag", "endtag", "genentity", "localname", "namespace", "numcharref", "paramentity", "pi", "prefix", "comment", "starttag", "xmlpi")
		class namespace(xsc.TextAttr): pass


class task(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class taskprerequisites(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class taskrelated(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class tasksummary(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class tbody(xsc.Element):
	xmlns = xmlns
	class Attrs(align, annotations, arch, audience, char, charoff, class2, condition, conformance, dir, lang, linkend, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, security, style, title2, userlevel, valign3, vendor, version, wordsize, xreflabel):
		pass


class td(xsc.Element):
	xmlns = xmlns
	class Attrs(abbr, align, annotations, arch, audience, axis, char, charoff, class2, colspan, condition, conformance, dir, headers, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, rowspan, scope, security, style, title2, userlevel, valign, vendor, version, wordsize, xreflabel):
		pass


class term(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class termdef(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, baseform, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, sortas, userlevel, vendor, version, wordsize, xreflabel):
		pass


class tertiary(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, sortas, userlevel, vendor, version, wordsize, xreflabel):
		pass


class tertiaryie(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkends, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class textdata(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, entityref, fileref, format, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		class encoding(xsc.TextAttr): pass


class textobject(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class tfoot(xsc.Element):
	xmlns = xmlns
	class Attrs(align, annotations, arch, audience, char, charoff, class2, condition, conformance, dir, lang, linkend, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, security, style, title2, userlevel, valign3, vendor, version, wordsize, xreflabel):
		pass


class tgroup(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, annotations, arch, audience, char, charoff, colsep, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, rowsep, security, tgroupstyle, userlevel, vendor, version, wordsize, xreflabel):
		class cols(xsc.TextAttr): required = True


class th(xsc.Element):
	xmlns = xmlns
	class Attrs(abbr, align, annotations, arch, audience, axis, char, charoff, class2, colspan, condition, conformance, dir, headers, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, rowspan, scope, security, style, title2, userlevel, valign, vendor, version, wordsize, xreflabel):
		pass


class thead(xsc.Element):
	xmlns = xmlns
	class Attrs(align, annotations, arch, audience, char, charoff, class2, condition, conformance, dir, lang, linkend, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, security, style, title2, userlevel, valign3, vendor, version, wordsize, xreflabel):
		pass


class tip(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class title(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class titleabbrev(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class toc(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class tocdiv(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, pagenum, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class tocentry(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, pagenum, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class token(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class tr(xsc.Element):
	xmlns = xmlns
	class Attrs(align, annotations, arch, audience, char, charoff, class2, condition, conformance, dir, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, security, style, title2, userlevel, valign, vendor, version, wordsize, xreflabel):
		pass


class trademark(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, class4, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class type(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class uri(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, type2, userlevel, vendor, version, wordsize, xreflabel):
		pass


class userinput(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class varargs(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class variablelist(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, spacing, userlevel, vendor, version, wordsize, xreflabel):
		class termlength(xsc.TextAttr): pass


class varlistentry(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class varname(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class videodata(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, annotations, arch, audience, condition, conformance, contentdepth, contentwidth, depth, dir, entityref, fileref, format, os, remap, revision2, revisionflag, role, scale, scalefit, security, userlevel, valign2, vendor, version, width, wordsize, xreflabel):
		pass


class videoobject(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class void(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class volumenum(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class warning(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class wordasword(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


class xref(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, endterm, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel, xrefstyle):
		pass


class year(xsc.Element):
	xmlns = xmlns
	class Attrs(annotations, arch, audience, condition, conformance, dir, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, version, wordsize, xreflabel):
		pass


info.model = sims.Elements(address, pubdate, pagenums, itermset, subtitle, titleabbrev, bibliosource, contractsponsor, biblioset, publisher, confgroup, contractnum, legalnotice, keywordset, revhistory, subjectset, productnumber, mediaobject, org, artpagenums, authorgroup, publishername, productname, bibliomset, title, issuenum, authorinitials, extendedlink, biblioid, volumenum, releaseinfo, othercredit, cover, bibliocoverage, copyright, bibliomisc, abstract, printhistory, seriesvolnums, bibliorelation, author, editor, edition, annotation, orgname, collab, date)
area.model = sims.Elements(alt)
epigraph.model = sims.Elements(anchor, attribution, literallayout, para, info, formalpara, simpara)
printhistory.model = sims.Elements(anchor, simpara, formalpara, para)
abstract.model = \
personblurb.model = sims.Elements(anchor, titleabbrev, simpara, para, info, formalpara, title)
extendedlink.model = sims.Elements(arc, locator)
areaset.model = sims.Elements(area)
areaspec.model = sims.Elements(areaset, area)
audioobject.model = sims.Elements(audiodata, info)
mediaobject.model = sims.Elements(audioobject, caption, alt, videoobject, info, imageobject, imageobjectco, textobject)
inlinemediaobject.model = sims.Elements(audioobject, videoobject, info, imageobject, alt, imageobjectco, textobject)
revision.model = sims.Elements(authorinitials, revnumber, revdescription, revremark, author, date)
screenco.model = sims.Elements(calloutlist, info, areaspec, screen)
imageobjectco.model = sims.Elements(calloutlist, info, imageobject, areaspec)
programlistingco.model = sims.Elements(calloutlist, info, programlisting, areaspec)
colgroup.model = sims.Elements(col)
confgroup.model = sims.Elements(confsponsor, confnum, confdates, address, conftitle)
classsynopsis.model = sims.Elements(constructorsynopsis, oointerface, destructorsynopsis, ooexception, fieldsynopsis, ooclass, classsynopsisinfo, methodsynopsis)
authorgroup.model = sims.Elements(editor, othercredit, author)
row.model = sims.Elements(entrytbl, entry)
informalexample.model = \
informalfigure.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote, caption)
glossary.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, subtitle, titleabbrev, bibliography, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, glossdiv, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, glossentry, sidebar, equation, important, informalfigure, annotation, blockquote)
bibliography.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, subtitle, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, bibliomixed, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, bibliodiv, productionset, cmdsynopsis, sidebar, warning, equation, important, informalfigure, annotation, blockquote, biblioentry)
bibliodiv.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, subtitle, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, bibliomixed, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote, biblioentry)
glossdiv.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, subtitle, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, glossentry, sidebar, equation, important, informalfigure, annotation, blockquote)
tocdiv.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, subtitle, titleabbrev, glosslist, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, tocentry, tocdiv, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote)
blockquote.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, titleabbrev, attribution, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote)
qandadiv.model = \
qandaset.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, qandadiv, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, qandaentry, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, para, sidebar, equation, important, informalfigure, annotation, blockquote)
bibliolist.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, bibliomixed, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote, biblioentry)
glosslist.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, glossentry, sidebar, equation, important, informalfigure, annotation, blockquote)
calloutlist.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote, callout)
example.model = \
figure.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote, caption)
variablelist.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote, varlistentry)
procedure.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, step, sidebar, equation, important, informalfigure, annotation, blockquote)
itemizedlist.model = \
orderedlist.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, listitem, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote)
toc.model = sims.Elements(epigraph, caution, tip, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, titleabbrev, glosslist, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, tocentry, tocdiv, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote)
sect5.model = sims.Elements(epigraph, para, destructorsynopsis, itemizedlist, constraintdef, informalexample, titleabbrev, bibliography, funcsynopsis, msgset, simplelist, methodsynopsis, programlisting, glossary, revhistory, procedure, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, literallayout, table, classsynopsis, productionset, informalfigure, blockquote, index, tip, address, segmentedlist, subtitle, task, simpara, orderedlist, mediaobject, screenco, anchor, glosslist, toc, example, programlistingco, info, screenshot, simplesect, caution, fieldsynopsis, remark, informalequation, constructorsynopsis, synopsis, note, qandaset, warning, cmdsynopsis, sidebar, equation, important, annotation, bibliolist)
section.model = sims.Elements(epigraph, para, destructorsynopsis, itemizedlist, constraintdef, informalexample, titleabbrev, bibliography, funcsynopsis, msgset, simplelist, methodsynopsis, programlisting, glossary, revhistory, procedure, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, literallayout, table, productionset, classsynopsis, section, refentry, informalfigure, blockquote, index, tip, address, segmentedlist, subtitle, task, simpara, orderedlist, mediaobject, screenco, anchor, glosslist, toc, example, programlistingco, info, screenshot, simplesect, caution, fieldsynopsis, remark, informalequation, constructorsynopsis, synopsis, note, qandaset, warning, cmdsynopsis, sidebar, equation, important, annotation, bibliolist)
sect1.model = sims.Elements(epigraph, para, destructorsynopsis, itemizedlist, constraintdef, informalexample, titleabbrev, bibliography, funcsynopsis, msgset, simplelist, methodsynopsis, programlisting, glossary, revhistory, sect2, procedure, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, literallayout, table, classsynopsis, productionset, informalfigure, blockquote, index, tip, address, segmentedlist, subtitle, task, simpara, orderedlist, mediaobject, screenco, anchor, glosslist, toc, example, programlistingco, info, screenshot, simplesect, caution, fieldsynopsis, remark, informalequation, constructorsynopsis, synopsis, note, qandaset, warning, cmdsynopsis, sidebar, equation, important, annotation, bibliolist)
sect2.model = sims.Elements(epigraph, para, destructorsynopsis, itemizedlist, constraintdef, informalexample, titleabbrev, bibliography, funcsynopsis, msgset, simplelist, methodsynopsis, programlisting, glossary, revhistory, sect3, procedure, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, literallayout, table, classsynopsis, productionset, informalfigure, blockquote, index, tip, address, segmentedlist, subtitle, task, simpara, orderedlist, mediaobject, screenco, anchor, glosslist, toc, example, programlistingco, info, screenshot, simplesect, caution, fieldsynopsis, remark, informalequation, constructorsynopsis, synopsis, note, qandaset, warning, cmdsynopsis, sidebar, equation, important, annotation, bibliolist)
sect3.model = sims.Elements(epigraph, para, destructorsynopsis, itemizedlist, constraintdef, informalexample, titleabbrev, bibliography, funcsynopsis, msgset, simplelist, methodsynopsis, programlisting, glossary, revhistory, sect4, procedure, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, literallayout, table, classsynopsis, productionset, informalfigure, blockquote, index, tip, address, segmentedlist, subtitle, task, simpara, orderedlist, mediaobject, screenco, anchor, glosslist, toc, example, programlistingco, info, screenshot, simplesect, caution, fieldsynopsis, remark, informalequation, constructorsynopsis, synopsis, note, qandaset, warning, cmdsynopsis, sidebar, equation, important, annotation, bibliolist)
sect4.model = sims.Elements(epigraph, para, destructorsynopsis, itemizedlist, constraintdef, informalexample, titleabbrev, bibliography, funcsynopsis, msgset, simplelist, methodsynopsis, programlisting, glossary, revhistory, sect5, procedure, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, literallayout, table, classsynopsis, productionset, informalfigure, blockquote, index, tip, address, segmentedlist, subtitle, task, simpara, orderedlist, mediaobject, screenco, anchor, glosslist, toc, example, programlistingco, info, screenshot, simplesect, caution, fieldsynopsis, remark, informalequation, constructorsynopsis, synopsis, note, qandaset, warning, cmdsynopsis, sidebar, equation, important, annotation, bibliolist)
article.model = sims.Elements(epigraph, para, destructorsynopsis, itemizedlist, constraintdef, informalexample, titleabbrev, bibliography, funcsynopsis, msgset, simplelist, toc, programlisting, glossary, revhistory, sect1, procedure, title, variablelist, informaltable, bridgehead, calloutlist, address, programlistingco, figure, indexterm, literallayout, table, classsynopsis, appendix, colophon, productionset, refentry, section, blockquote, index, tip, formalpara, segmentedlist, subtitle, task, simpara, orderedlist, mediaobject, screenco, anchor, glosslist, methodsynopsis, example, screen, info, screenshot, acknowledgements, simplesect, informalfigure, caution, annotation, remark, informalequation, constructorsynopsis, synopsis, note, qandaset, warning, cmdsynopsis, sidebar, equation, important, fieldsynopsis, bibliolist)
appendix.model = \
chapter.model = \
preface.model = sims.Elements(epigraph, para, destructorsynopsis, itemizedlist, constraintdef, informalexample, titleabbrev, bibliography, funcsynopsis, msgset, simplelist, toc, programlisting, glossary, revhistory, sect1, procedure, title, variablelist, informaltable, bridgehead, calloutlist, address, programlistingco, figure, indexterm, literallayout, table, classsynopsis, productionset, refentry, section, blockquote, index, tip, formalpara, segmentedlist, subtitle, task, simpara, orderedlist, mediaobject, screenco, anchor, glosslist, methodsynopsis, example, screen, info, screenshot, simplesect, informalfigure, caution, annotation, remark, informalequation, constructorsynopsis, synopsis, note, qandaset, warning, cmdsynopsis, sidebar, equation, important, fieldsynopsis, bibliolist)
cover.model = sims.Elements(epigraph, para, destructorsynopsis, itemizedlist, formalpara, segmentedlist, informalexample, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, screen, procedure, address, screenshot, variablelist, informaltable, bridgehead, calloutlist, constraintdef, programlistingco, programlisting, remark, literallayout, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, qandaset, productionset, cmdsynopsis, sidebar, informalfigure, fieldsynopsis, blockquote)
refsect1.model = sims.Elements(epigraph, refsect2, tip, destructorsynopsis, itemizedlist, remark, address, informaltable, informalexample, subtitle, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, constraintdef, screenshot, title, variablelist, informalequation, segmentedlist, bridgehead, calloutlist, formalpara, screen, caution, indexterm, annotation, programlisting, procedure, para, literallayout, table, figure, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist)
refsynopsisdiv.model = sims.Elements(epigraph, refsect2, tip, destructorsynopsis, itemizedlist, remark, address, informaltable, informalexample, subtitle, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, constraintdef, screenshot, title, variablelist, informalequation, segmentedlist, bridgehead, calloutlist, formalpara, screen, caution, indexterm, annotation, programlisting, procedure, para, literallayout, table, figure, blockquote, constructorsynopsis, synopsis, classsynopsis, note, refsection, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist)
refsect2.model = sims.Elements(epigraph, refsect3, tip, destructorsynopsis, itemizedlist, remark, address, informaltable, informalexample, subtitle, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, constraintdef, screenshot, title, variablelist, informalequation, segmentedlist, bridgehead, calloutlist, formalpara, screen, caution, indexterm, annotation, programlisting, procedure, para, literallayout, table, figure, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist)
setindex.model = sims.Elements(epigraph, screenco, caution, indexentry, destructorsynopsis, itemizedlist, remark, address, segmentedlist, informalexample, subtitle, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, tip, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, constraintdef, warning, productionset, cmdsynopsis, sidebar, indexdiv, equation, important, informalfigure, annotation, blockquote)
indexdiv.model = sims.Elements(epigraph, screenco, indexentry, destructorsynopsis, itemizedlist, remark, address, informaltable, informalexample, subtitle, titleabbrev, formalpara, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, tip, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informalequation, segmentedlist, bridgehead, calloutlist, constraintdef, screen, figure, indexterm, annotation, programlisting, procedure, para, literallayout, table, caution, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist)
index.model = sims.Elements(epigraph, screenco, indexentry, destructorsynopsis, itemizedlist, remark, address, informaltable, informalexample, subtitle, titleabbrev, formalpara, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, tip, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informalequation, segmentedlist, bridgehead, calloutlist, constraintdef, screen, figure, indexterm, annotation, programlisting, procedure, para, literallayout, table, caution, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, indexdiv, equation, important, informalfigure, fieldsynopsis, bibliolist)
step.model = sims.Elements(epigraph, screenco, para, destructorsynopsis, itemizedlist, remark, constraintdef, informaltable, informalexample, simpara, titleabbrev, funcsynopsis, msgset, simplelist, methodsynopsis, programlisting, revhistory, orderedlist, mediaobject, task, tip, anchor, glosslist, example, programlistingco, info, address, screenshot, title, variablelist, informalequation, segmentedlist, bridgehead, calloutlist, formalpara, screen, figure, indexterm, annotation, stepalternatives, procedure, literallayout, table, caution, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, blockquote, substeps)
glossdef.model = sims.Elements(epigraph, tip, destructorsynopsis, itemizedlist, address, informaltable, informalexample, formalpara, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, procedure, screenshot, variablelist, informalequation, glossseealso, segmentedlist, bridgehead, calloutlist, constraintdef, screen, figure, indexterm, annotation, programlisting, remark, para, literallayout, table, caution, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist)
answer.model = \
question.model = sims.Elements(epigraph, tip, destructorsynopsis, itemizedlist, address, informaltable, informalexample, formalpara, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, procedure, screenshot, variablelist, informalequation, label, segmentedlist, bridgehead, calloutlist, constraintdef, screen, figure, indexterm, annotation, programlisting, remark, para, literallayout, table, caution, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist)
callout.model = \
footnote.model = \
listitem.model = \
msgtext.model = \
revdescription.model = sims.Elements(epigraph, tip, destructorsynopsis, itemizedlist, address, segmentedlist, informalexample, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, procedure, constraintdef, screenshot, variablelist, informaltable, bridgehead, calloutlist, formalpara, screen, figure, caution, indexterm, fieldsynopsis, programlisting, remark, para, literallayout, table, informalequation, bibliolist, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, annotation, blockquote)
textobject.model = sims.Elements(epigraph, tip, destructorsynopsis, itemizedlist, remark, address, informaltable, informalexample, annotation, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, constraintdef, screenshot, variablelist, informalequation, segmentedlist, bridgehead, calloutlist, formalpara, screen, caution, indexterm, fieldsynopsis, programlisting, procedure, para, literallayout, table, figure, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, textdata, bibliolist, phrase)
acknowledgements.model = \
colophon.model = \
dedication.model = \
refsect3.model = \
simplesect.model = sims.Elements(epigraph, tip, destructorsynopsis, itemizedlist, remark, address, informaltable, informalexample, subtitle, titleabbrev, formalpara, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informalequation, segmentedlist, bridgehead, calloutlist, constraintdef, screen, figure, indexterm, annotation, programlisting, procedure, para, literallayout, table, caution, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist)
partintro.model = sims.Elements(epigraph, tip, destructorsynopsis, itemizedlist, remark, address, informaltable, informalexample, subtitle, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, sect1, simplelist, anchor, glosslist, example, programlistingco, info, constraintdef, screenshot, title, variablelist, informalequation, segmentedlist, simplesect, bridgehead, calloutlist, formalpara, screen, caution, indexterm, annotation, programlisting, procedure, para, literallayout, table, figure, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, section, cmdsynopsis, refentry, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist, productionset)
refsection.model = sims.Elements(epigraph, tip, destructorsynopsis, itemizedlist, remark, address, informaltable, informalexample, subtitle, titleabbrev, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, constraintdef, screenshot, title, variablelist, informalequation, segmentedlist, bridgehead, calloutlist, formalpara, screen, caution, indexterm, annotation, programlisting, procedure, para, literallayout, table, figure, blockquote, constructorsynopsis, synopsis, classsynopsis, note, refsection, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist)
annotation.model = \
caution.model = \
constraintdef.model = \
important.model = \
legalnotice.model = \
msgexplan.model = \
note.model = \
sidebar.model = \
taskprerequisites.model = \
taskrelated.model = \
tasksummary.model = \
tip.model = \
warning.model = sims.Elements(epigraph, tip, destructorsynopsis, itemizedlist, remark, address, informaltable, informalexample, titleabbrev, formalpara, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, programlistingco, info, screenshot, title, variablelist, informalequation, segmentedlist, bridgehead, calloutlist, constraintdef, screen, figure, indexterm, annotation, programlisting, procedure, para, literallayout, table, caution, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist)
constructorsynopsis.model = \
destructorsynopsis.model = sims.Elements(exceptionname, methodname, modifier, void, methodparam)
ooexception.model = sims.Elements(exceptionname, modifier, package)
methodsynopsis.model = sims.Elements(exceptionname, type, modifier, methodname, methodparam, void)
synopfragment.model = sims.Elements(group, arg)
menuchoice.model = sims.Elements(guimenu, guimenuitem, shortcut, guiicon, guisubmenu, guilabel, guibutton)
copyright.model = sims.Elements(holder, year)
book.model = sims.Elements(index, article, reference, subtitle, titleabbrev, bibliography, preface, chapter, toc, appendix, glossary, dedication, part, info, colophon, title, acknowledgements)
part.model = sims.Elements(index, article, reference, subtitle, titleabbrev, bibliography, preface, chapter, toc, appendix, glossary, refentry, dedication, partintro, info, colophon, title, acknowledgements)
itermset.model = sims.Elements(indexterm)
glossentry.model = sims.Elements(indexterm, glossterm, acronym, glosssee, abbrev, glossdef)
formalpara.model = sims.Elements(indexterm, info, titleabbrev, title, para)
refmeta.model = sims.Elements(indexterm, refentrytitle, manvolnum, refmiscinfo)
refentry.model = sims.Elements(indexterm, refsect1, info, refmeta, refsynopsisdiv, refnamediv, refsection)
audiodata.model = \
imagedata.model = \
textdata.model = \
videodata.model = sims.Elements(info)
informalequation.model = sims.Elements(info, caption, alt, mathphrase, mediaobject)
funcsynopsis.model = sims.Elements(info, funcsynopsisinfo, funcprototype)
imageobject.model = sims.Elements(info, imagedata)
stepalternatives.model = sims.Elements(info, step)
segmentedlist.model = sims.Elements(info, titleabbrev, seglistitem, title, segtitle)
msgmain.model = \
msgrel.model = \
msgsub.model = sims.Elements(info, titleabbrev, title, msgtext)
productionset.model = sims.Elements(info, titleabbrev, title, productionrecap, production)
qandaentry.model = sims.Elements(info, titleabbrev, title, question, answer)
revhistory.model = sims.Elements(info, titleabbrev, title, revision)
videoobject.model = sims.Elements(info, videodata)
fieldsynopsis.model = sims.Elements(initializer, type, modifier, varname)
inlineequation.model = sims.Elements(inlinemediaobject, alt, mathphrase)
keycombo.model = \
shortcut.model = sims.Elements(keycap, mousebutton, keycombo, keysym)
keywordset.model = sims.Elements(keyword)
production.model = sims.Elements(lhs, rhs, constraint)
simplelist.model = sims.Elements(member)
ooclass.model = sims.Elements(modifier, package, classname)
oointerface.model = sims.Elements(modifier, package, interfacename)
simplemsgentry.model = sims.Elements(msgexplan, msgtext)
msgentry.model = sims.Elements(msginfo, msgexplan, msg)
msginfo.model = sims.Elements(msgorig, msglevel, msgaud)
group.model = sims.Elements(option, group, arg, replaceable, sbr, synopfragmentref)
org.model = sims.Elements(orgdiv, affiliation, uri, orgname, address, email)
affiliation.model = sims.Elements(orgdiv, jobtitle, org, orgname, address, shortaffil)
author.model = \
editor.model = \
othercredit.model = sims.Elements(orgdiv, personname, affiliation, personblurb, address, email, contrib, uri, orgname)
person.model = sims.Elements(personname, affiliation, uri, personblurb, address, email)
collab.model = sims.Elements(personname, org, orgname, person, affiliation)
publisher.model = sims.Elements(publishername, address)
biblioentry.model = \
biblioset.model = sims.Elements(quote, volumenum, pagenums, glossterm, bibliosource, contractsponsor, citerefentry, publisher, footnote, foreignphrase, superscript, revhistory, subjectset, artpagenums, publishername, bibliomset, title, issuenum, footnoteref, extendedlink, biblioid, productname, releaseinfo, bibliocoverage, printhistory, personblurb, abbrev, titleabbrev, citebiblioid, acronym, editor, edition, orgname, citetitle, address, pubdate, itermset, subtitle, bibliorelation, biblioset, confgroup, contractnum, legalnotice, keywordset, productnumber, mediaobject, org, person, authorgroup, copyright, authorinitials, coref, othercredit, emphasis, cover, bibliomisc, personname, subscript, abstract, firstterm, seriesvolnums, author, phrase, annotation, collab, date, wordasword)
reference.model = sims.Elements(refentry, subtitle, titleabbrev, partintro, info, title)
citerefentry.model = sims.Elements(refentrytitle, manvolnum)
refnamediv.model = sims.Elements(refpurpose, refdescriptor, refclass, refname)
tbody.model = sims.Elements(row, tr)
tfoot.model = \
thead.model = sims.Elements(row, tr, colspec)
indexentry.model = sims.Elements(secondaryie, seeie, tertiaryie, seealsoie, primaryie)
indexterm.model = sims.Elements(seealso, secondary, tertiary, primary, see)
seglistitem.model = sims.Elements(seg)
set.model = sims.Elements(setindex, book, subtitle, titleabbrev, set, info, title, toc)
msgset.model = sims.Elements(simplemsgentry, info, titleabbrev, title, msgentry)
entrytbl.model = sims.Elements(spanspec, colspec, thead, tbody)
tgroup.model = sims.Elements(spanspec, colspec, thead, tfoot, tbody)
substeps.model = sims.Elements(step)
subjectset.model = sims.Elements(subject)
subject.model = sims.Elements(subjectterm)
screenshot.model = sims.Elements(subtitle, titleabbrev, title, mediaobject, info)
cmdsynopsis.model = sims.Elements(synopfragment, sbr, arg, group, info, command)
task.model = sims.Elements(taskrelated, taskprerequisites, subtitle, titleabbrev, example, procedure, info, title, tasksummary)
table.model = sims.Elements(tbody, tfoot, mediaobject, caption, tgroup, indexterm, col, titleabbrev, thead, tr, info, title, colgroup, textobject)
informaltable.model = sims.Elements(tbody, tfoot, mediaobject, colgroup, tgroup, col, tr, info, thead, textobject)
varlistentry.model = sims.Elements(term, listitem)
tr.model = sims.Elements(th, td)
equation.model = sims.Elements(titleabbrev, mathphrase, mediaobject, info, caption, title, alt)
msg.model = sims.Elements(titleabbrev, msgmain, msgsub, info, title, msgrel)
methodparam.model = sims.Elements(type, modifier, parameter, funcparams, initializer)
funcprototype.model = sims.Elements(varargs, paramdef, modifier, void, funcdef)
accel.model = \
application.model = \
artpagenums.model = \
authorinitials.model = \
bibliocoverage.model = \
biblioid.model = \
bibliomisc.model = \
bibliorelation.model = \
bibliosource.model = \
citebiblioid.model = \
city.model = \
classname.model = \
command.model = \
confdates.model = \
confnum.model = \
confsponsor.model = \
conftitle.model = \
constant.model = \
contractnum.model = \
contractsponsor.model = \
contrib.model = \
country.model = \
database.model = \
edition.model = \
email.model = \
envar.model = \
errorcode.model = \
errorname.model = \
errortext.model = \
errortype.model = \
exceptionname.model = \
fax.model = \
filename.model = \
firstname.model = \
funcparams.model = \
function.model = \
hardware.model = \
holder.model = \
honorific.model = \
initializer.model = \
interfacename.model = \
issuenum.model = \
jobtitle.model = \
keycap.model = \
keycode.model = \
keysym.model = \
label.model = \
lineage.model = \
lineannotation.model = \
literal.model = \
manvolnum.model = \
markup.model = \
methodname.model = \
modifier.model = \
mousebutton.model = \
msgaud.model = \
msglevel.model = \
msgorig.model = \
option.model = \
optional.model = \
orgname.model = \
otheraddr.model = \
othername.model = \
package.model = \
pagenums.model = \
parameter.model = \
phone.model = \
pob.model = \
postcode.model = \
productname.model = \
productnumber.model = \
property.model = \
publishername.model = \
refmiscinfo.model = \
releaseinfo.model = \
remark.model = \
returnvalue.model = \
revnumber.model = \
revremark.model = \
seriesvolnums.model = \
shortaffil.model = \
state.model = \
street.model = \
subscript.model = \
superscript.model = \
surname.model = \
symbol.model = \
tag.model = \
token.model = \
trademark.model = \
type.model = \
uri.model = \
varname.model = \
volumenum.model = \
wordasword.model = \
year.model = sims.ElementsOrText(anchor, superscript, biblioref, subscript, inlinemediaobject, link, indexterm, olink, phrase, xref, remark, annotation, replaceable, alt)
refclass.model = sims.ElementsOrText(application)
caption.model = sims.ElementsOrText(epigraph, caution, tip, destructorsynopsis, itemizedlist, address, informaltable, informalexample, formalpara, funcsynopsis, msgset, task, methodsynopsis, simpara, revhistory, orderedlist, mediaobject, screenco, simplelist, anchor, glosslist, example, screen, procedure, screenshot, variablelist, segmentedlist, bridgehead, calloutlist, constraintdef, programlistingco, figure, indexterm, annotation, programlisting, remark, para, literallayout, table, informalequation, blockquote, constructorsynopsis, synopsis, classsynopsis, note, qandaset, warning, productionset, cmdsynopsis, sidebar, equation, important, informalfigure, fieldsynopsis, bibliolist)
para.model = sims.ElementsOrText(guimenu, epigraph, quote, mousebutton, itemizedlist, informalexample, exceptionname, optional, glossterm, uri, footnote, table, citation, termdef, menuchoice, procedure, variablelist, footnoteref, bridgehead, constraintdef, figure, parameter, ooexception, literallayout, returnvalue, classsynopsis, guiicon, function, productionset, citebiblioid, option, code, informalfigure, blockquote, command, citetitle, tip, tag, inlinemediaobject, funcsynopsis, task, modifier, application, orderedlist, keycap, mediaobject, org, trademark, person, anchor, envar, glosslist, example, programlistingco, info, olink, errortype, keycombo, coref, subscript, foreignphrase, computeroutput, remark, emphasis, synopsis, personname, nonterminal, qandaset, firstterm, equation, classname, annotation, bibliolist, literal, prompt, destructorsynopsis, biblioref, productname, initializer, citerefentry, msgset, simplelist, methodsynopsis, shortcut, superscript, revhistory, guisubmenu, package, type, informaltable, calloutlist, filename, link, indexterm, symbol, database, systemitem, abbrev, acronym, editor, orgname, errorname, inlineequation, replaceable, address, email, constant, ooclass, keysym, keycode, guimenuitem, varname, oointerface, productnumber, token, screenco, accel, methodname, screen, phrase, property, screenshot, alt, userinput, interfacename, jobtitle, caution, hardware, markup, errortext, guilabel, programlisting, informalequation, segmentedlist, constructorsynopsis, note, warning, cmdsynopsis, errorcode, author, guibutton, sidebar, important, xref, fieldsynopsis, date, wordasword)
entry.model = \
td.model = \
th.model = sims.ElementsOrText(guimenu, epigraph, quote, para, itemizedlist, informalexample, exceptionname, optional, glossterm, uri, footnote, table, citation, termdef, menuchoice, procedure, variablelist, footnoteref, bridgehead, constraintdef, figure, parameter, ooexception, literallayout, returnvalue, classsynopsis, guiicon, function, productionset, citebiblioid, option, code, informalfigure, blockquote, command, abbrev, tip, tag, inlinemediaobject, funcsynopsis, task, modifier, interfacename, orderedlist, keycap, mediaobject, org, coref, person, anchor, envar, glosslist, example, programlistingco, olink, errortype, keycombo, trademark, subscript, foreignphrase, computeroutput, remark, caution, synopsis, personname, nonterminal, qandaset, firstterm, equation, classname, annotation, bibliolist, mousebutton, prompt, destructorsynopsis, biblioref, productname, guilabel, citerefentry, msgset, simplelist, methodsynopsis, shortcut, superscript, revhistory, guisubmenu, package, type, informaltable, calloutlist, formalpara, filename, literal, indexterm, symbol, database, systemitem, citetitle, acronym, editor, orgname, email, errorname, inlineequation, replaceable, address, link, constant, ooclass, keysym, keycode, guimenuitem, varname, simpara, oointerface, productnumber, token, screenco, accel, methodname, screen, important, property, screenshot, alt, userinput, application, jobtitle, emphasis, hardware, markup, errortext, initializer, programlisting, informalequation, segmentedlist, constructorsynopsis, note, warning, cmdsynopsis, errorcode, author, guibutton, sidebar, phrase, xref, fieldsynopsis, date, wordasword)
bridgehead.model = \
citation.model = \
citetitle.model = \
emphasis.model = \
firstterm.model = \
glosssee.model = \
glossseealso.model = \
glossterm.model = \
link.model = \
member.model = \
olink.model = \
orgdiv.model = \
phrase.model = \
primary.model = \
primaryie.model = \
quote.model = \
refdescriptor.model = \
refentrytitle.model = \
refname.model = \
refpurpose.model = \
secondary.model = \
secondaryie.model = \
see.model = \
seealso.model = \
seealsoie.model = \
seeie.model = \
seg.model = \
segtitle.model = \
subtitle.model = \
term.model = \
termdef.model = \
tertiary.model = \
tertiaryie.model = \
title.model = \
titleabbrev.model = \
tocentry.model = sims.ElementsOrText(guimenu, literal, quote, guilabel, prompt, mousebutton, biblioref, productname, exceptionname, optional, glossterm, citerefentry, uri, footnote, citation, termdef, shortcut, superscript, guisubmenu, menuchoice, package, type, email, footnoteref, filename, indexterm, parameter, ooexception, symbol, database, returnvalue, systemitem, guiicon, function, abbrev, citebiblioid, olink, option, code, acronym, editor, command, errorname, inlineequation, citetitle, replaceable, tag, link, inlinemediaobject, constant, ooclass, keysym, keycode, guimenuitem, varname, interfacename, oointerface, productnumber, token, org, coref, person, accel, anchor, methodname, envar, property, alt, errortype, userinput, keycombo, application, trademark, jobtitle, modifier, foreignphrase, hardware, markup, errortext, remark, initializer, emphasis, personname, subscript, orgname, nonterminal, firstterm, errorcode, author, guibutton, keycap, computeroutput, phrase, xref, classname, annotation, date, wordasword)
classsynopsisinfo.model = \
funcsynopsisinfo.model = \
literallayout.model = \
programlisting.model = \
screen.model = \
synopsis.model = sims.ElementsOrText(guimenu, literal, quote, guilabel, prompt, mousebutton, biblioref, productname, exceptionname, optional, glossterm, citerefentry, uri, footnote, citation, termdef, shortcut, superscript, guisubmenu, package, type, email, footnoteref, filename, indexterm, parameter, ooexception, symbol, database, returnvalue, systemitem, guiicon, function, abbrev, citebiblioid, olink, option, code, acronym, editor, command, errorname, co, inlineequation, citetitle, replaceable, tag, link, inlinemediaobject, constant, ooclass, keysym, keycode, textobject, guimenuitem, varname, interfacename, computeroutput, oointerface, productnumber, token, org, coref, person, accel, anchor, methodname, envar, info, property, alt, errortype, userinput, keycombo, application, trademark, jobtitle, modifier, lineannotation, foreignphrase, hardware, menuchoice, errortext, remark, initializer, emphasis, personname, subscript, orgname, nonterminal, firstterm, errorcode, author, guibutton, keycap, markup, phrase, xref, classname, annotation, date, wordasword)
simpara.model = sims.ElementsOrText(guimenu, literal, quote, initializer, prompt, mousebutton, biblioref, productname, exceptionname, optional, glossterm, citerefentry, uri, footnote, citation, termdef, shortcut, superscript, guisubmenu, package, type, email, footnoteref, filename, indexterm, parameter, ooexception, symbol, database, returnvalue, systemitem, guiicon, function, abbrev, citebiblioid, alt, option, code, acronym, editor, command, errorname, inlineequation, citetitle, replaceable, tag, link, inlinemediaobject, constant, ooclass, keysym, keycode, guimenuitem, varname, application, computeroutput, oointerface, productnumber, token, org, trademark, person, accel, anchor, methodname, envar, info, property, olink, errortype, userinput, keycombo, interfacename, coref, jobtitle, modifier, foreignphrase, hardware, menuchoice, errortext, remark, guilabel, emphasis, personname, subscript, orgname, nonterminal, firstterm, errorcode, author, guibutton, keycap, markup, phrase, xref, classname, annotation, date, wordasword)
userinput.model = sims.ElementsOrText(guimenu, literal, replaceable, prompt, mousebutton, tag, biblioref, symbol, link, inlinemediaobject, optional, parameter, co, uri, keysym, keycode, termdef, guimenuitem, shortcut, superscript, guisubmenu, keycap, token, menuchoice, accel, anchor, envar, package, property, olink, userinput, email, keycombo, filename, subscript, indexterm, computeroutput, remark, guilabel, alt, systemitem, nonterminal, guiicon, guibutton, option, code, markup, xref, annotation, command, constant)
guibutton.model = \
guiicon.model = \
guilabel.model = \
guimenu.model = \
guimenuitem.model = \
guisubmenu.model = sims.ElementsOrText(indexterm, superscript, biblioref, subscript, inlinemediaobject, link, anchor, olink, phrase, accel, xref, remark, annotation, replaceable, alt)
prompt.model = \
replaceable.model = \
systemitem.model = sims.ElementsOrText(indexterm, superscript, biblioref, subscript, inlinemediaobject, link, anchor, olink, phrase, co, xref, remark, annotation, replaceable, alt)
mathphrase.model = sims.ElementsOrText(indexterm, superscript, biblioref, subscript, inlinemediaobject, link, anchor, olink, phrase, xref, remark, annotation, replaceable, emphasis, alt)
abbrev.model = \
acronym.model = sims.ElementsOrText(indexterm, superscript, trademark, biblioref, subscript, inlinemediaobject, link, anchor, olink, phrase, xref, remark, annotation, replaceable, alt)
alt.model = sims.ElementsOrText(inlinemediaobject)
computeroutput.model = sims.ElementsOrText(literal, replaceable, prompt, tag, biblioref, symbol, link, inlinemediaobject, optional, co, uri, termdef, superscript, computeroutput, token, anchor, envar, package, property, alt, userinput, email, filename, subscript, indexterm, parameter, remark, systemitem, nonterminal, olink, option, code, markup, xref, annotation, command, constant)
address.model = sims.ElementsOrText(postcode, email, replaceable, biblioref, subscript, inlinemediaobject, link, indexterm, uri, remark, city, pob, personname, superscript, otheraddr, country, street, state, olink, anchor, phrase, xref, fax, annotation, phone, alt)
foreignphrase.model = sims.ElementsOrText(quote, abbrev, biblioref, productname, link, inlinemediaobject, glossterm, citerefentry, footnote, citation, superscript, productnumber, org, trademark, person, anchor, editor, olink, footnoteref, application, coref, author, jobtitle, foreignphrase, emphasis, indexterm, hardware, database, personname, subscript, firstterm, citetitle, citebiblioid, acronym, phrase, xref, orgname, date, wordasword)
bibliomset.model = sims.ElementsOrText(quote, biblioref, productname, pagenums, glossterm, bibliosource, contractsponsor, citerefentry, publisher, footnote, superscript, revhistory, subjectset, artpagenums, publishername, bibliomset, title, issuenum, footnoteref, extendedlink, biblioid, volumenum, releaseinfo, pubdate, indexterm, bibliocoverage, emphasis, printhistory, personblurb, abbrev, titleabbrev, citebiblioid, olink, acronym, editor, edition, orgname, citetitle, replaceable, address, link, inlinemediaobject, itermset, subtitle, bibliorelation, biblioset, confgroup, contractnum, legalnotice, keywordset, productnumber, mediaobject, org, person, anchor, authorgroup, copyright, alt, authorinitials, coref, foreignphrase, othercredit, remark, cover, bibliomisc, personname, subscript, abstract, firstterm, seriesvolnums, author, phrase, xref, annotation, collab, date, wordasword)
bibliomixed.model = sims.ElementsOrText(quote, volumenum, pagenums, glossterm, bibliosource, contractsponsor, citerefentry, publisher, footnote, superscript, revhistory, subjectset, artpagenums, publishername, bibliomset, title, issuenum, footnoteref, extendedlink, biblioid, productname, releaseinfo, bibliocoverage, printhistory, personblurb, abbrev, titleabbrev, citebiblioid, acronym, editor, edition, orgname, cover, citetitle, address, pubdate, itermset, subtitle, bibliorelation, biblioset, confgroup, contractnum, legalnotice, keywordset, productnumber, mediaobject, org, person, authorgroup, copyright, authorinitials, coref, foreignphrase, othercredit, emphasis, bibliomisc, personname, subscript, abstract, firstterm, seriesvolnums, author, phrase, annotation, collab, date, wordasword)
arg.model = sims.ElementsOrText(replaceable, biblioref, sbr, subscript, inlinemediaobject, link, indexterm, remark, option, superscript, olink, anchor, synopfragmentref, arg, xref, annotation, phrase, group, alt)
attribution.model = sims.ElementsOrText(replaceable, biblioref, subscript, inlinemediaobject, link, indexterm, remark, citation, personname, superscript, citetitle, person, olink, anchor, phrase, xref, annotation, alt)
personname.model = sims.ElementsOrText(replaceable, lineage, biblioref, subscript, inlinemediaobject, link, indexterm, remark, alt, surname, othername, superscript, honorific, anchor, olink, phrase, xref, annotation, firstname)
rhs.model = sims.ElementsOrText(sbr, nonterminal, lineannotation)
funcdef.model = sims.ElementsOrText(type, replaceable, biblioref, subscript, inlinemediaobject, link, indexterm, function, remark, superscript, olink, anchor, phrase, xref, annotation, alt)
paramdef.model = sims.ElementsOrText(type, replaceable, biblioref, subscript, inlinemediaobject, link, indexterm, parameter, remark, initializer, superscript, funcparams, olink, anchor, phrase, xref, annotation, alt)
code.model = sims.ElementsOrText(type, replaceable, interfacename, biblioref, classname, subscript, inlinemediaobject, link, exceptionname, function, parameter, ooexception, remark, initializer, ooclass, returnvalue, indexterm, varname, superscript, oointerface, olink, anchor, methodname, phrase, xref, modifier, annotation, alt)
anchor.model = \
arc.model = \
biblioref.model = \
co.model = \
col.model = \
colspec.model = \
constraint.model = \
coref.model = \
footnoteref.model = \
locator.model = \
productionrecap.model = \
sbr.model = \
spanspec.model = \
varargs.model = \
void.model = \
xref.model = sims.Empty()
date.model = \
keyword.model = \
lhs.model = \
nonterminal.model = \
pubdate.model = \
subjectterm.model = \
synopfragmentref.model = sims.NoElements()
