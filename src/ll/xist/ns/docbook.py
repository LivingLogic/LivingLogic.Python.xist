# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
An XIST namespace module that contains definitions for all the elements in
DocBook 4.3
"""


from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://www.docbook.org/xml/4.3/docbookx.dtd"


class DocTypeDocBook43(xsc.DocType):
	"""
	document type for DocBook 4.3
	"""
	def __init__(self, type):
		xsc.DocType.__init__(self, type + ' PUBLIC "-//OASIS//DTD DocBook XML V4.3//EN" "http://www.docbook.org/xml/4.3/docbookx.dtd"')


###
### Attributes
###

class arch(xsc.Attrs):
	class arch(xsc.TextAttr): pass


class condition(xsc.Attrs):
	class condition(xsc.TextAttr): pass


class conformance(xsc.Attrs):
	class conformance(xsc.TextAttr): pass


class dir(xsc.Attrs):
	class dir(xsc.TextAttr): values = (u"ltr", u"rtl", u"lro", u"rlo")


class id(xsc.Attrs):
	class id(xsc.IDAttr): pass


class lang(xsc.Attrs):
	class lang(xsc.TextAttr): pass


class os(xsc.Attrs):
	class os(xsc.TextAttr): pass


class remap(xsc.Attrs):
	class remap(xsc.TextAttr): pass


class revision2(xsc.Attrs):
	class revision(xsc.TextAttr): pass


class revisionflag(xsc.Attrs):
	class revisionflag(xsc.TextAttr): values = ("changed", "added", "deleted", "off")


class role(xsc.Attrs):
	class role(xsc.TextAttr): pass


class security(xsc.Attrs):
	class security(xsc.TextAttr): pass


class userlevel(xsc.Attrs):
	class userlevel(xsc.TextAttr): pass


class vendor(xsc.Attrs):
	class vendor(xsc.TextAttr): pass


class xreflabel(xsc.Attrs):
	class xreflabel(xsc.TextAttr): pass


class moreinfo(xsc.Attrs):
	class moreinfo(xsc.TextAttr): values = (u"refentry", u"none")


class continuation(xsc.Attrs):
	class continuation(xsc.TextAttr): values = (u"continues", u"restarts")


class format(xsc.Attrs):
	class format(xsc.TextAttr): pass


class language(xsc.Attrs):
	class language(xsc.TextAttr): pass


class linenumbering(xsc.Attrs):
	class linenumbering(xsc.TextAttr): values = (u"numbered", u"unnumbered")


class startinglinenumber(xsc.Attrs):
	class startinglinenumber(xsc.TextAttr): pass


class id2(xsc.Attrs):
	class id(xsc.IDAttr): required = True


class pagenum(xsc.Attrs):
	class pagenum(xsc.TextAttr): pass


class label2(xsc.Attrs):
	class label(xsc.TextAttr): pass


class status(xsc.Attrs):
	class status(xsc.TextAttr): pass


class coords(xsc.Attrs):
	class coords(xsc.TextAttr): required = True


class linkends(xsc.Attrs):
	class linkends(xsc.TextAttr): pass


class otherunits(xsc.Attrs):
	class otherunits(xsc.TextAttr): pass


class units(xsc.Attrs):
	class units(xsc.TextAttr): values = (u"calspair", u"linecolumn", u"linerange", u"linecolumnpair", u"other")


class choice(xsc.Attrs):
	class choice(xsc.TextAttr): values = (u"opt", u"req", u"plain")


class rep(xsc.Attrs):
	class rep(xsc.TextAttr): values = (u"norepeat", u"repeat")


class entityref(xsc.Attrs):
	class entityref(xsc.TextAttr): pass


class fileref(xsc.Attrs):
	class fileref(xsc.TextAttr): pass


class format2(xsc.Attrs):
	class format(xsc.TextAttr): values = (u"BMP", u"CGM-CHAR", u"CGM-BINARY", u"CGM-CLEAR", u"DITROFF", u"DVI", u"EPS", u"EQN", u"FAX", u"GIF", u"GIF87a", u"GIF89a", u"JPG", u"JPEG", u"IGES", u"PCX", u"PIC", u"PNG", u"PS", u"SGML", u"TBL", u"TEX", u"TIFF", u"WMF", u"WPG", u"SVG", u"PDF", u"SWF", u"linespecific")


class srccredit(xsc.Attrs):
	class srccredit(xsc.TextAttr): pass


class class_(xsc.Attrs):
	class class_(xsc.TextAttr):
		xmlname = u"class"
		values = (u"uri", u"doi", u"isbn", u"issn", u"libraryofcongress", u"pubnumber", u"other")


class otherclass(xsc.Attrs):
	class otherclass(xsc.TextAttr): pass


class relation(xsc.Attrs):
	class relation(xsc.TextAttr): pass


class fpi(xsc.Attrs):
	class fpi(xsc.TextAttr): pass


class contents(xsc.Attrs):
	class contents(xsc.TextAttr): pass


class class2(xsc.Attrs):
	class class_(xsc.TextAttr): xmlname = "class"


class onclick(xsc.Attrs):
	class onclick(xsc.TextAttr): pass


class ondblclick(xsc.Attrs):
	class ondblclick(xsc.TextAttr): pass


class onkeydown(xsc.Attrs):
	class onkeydown(xsc.TextAttr): pass


class onkeypress(xsc.Attrs):
	class onkeypress(xsc.TextAttr): pass


class onkeyup(xsc.Attrs):
	class onkeyup(xsc.TextAttr): pass


class onmousedown(xsc.Attrs):
	class onmousedown(xsc.TextAttr): pass


class onmousemove(xsc.Attrs):
	class onmousemove(xsc.TextAttr): pass


class onmouseout(xsc.Attrs):
	class onmouseout(xsc.TextAttr): pass


class onmouseover(xsc.Attrs):
	class onmouseover(xsc.TextAttr): pass


class onmouseup(xsc.Attrs):
	class onmouseup(xsc.TextAttr): pass


class style(xsc.Attrs):
	class style(xsc.TextAttr): pass


class title2(xsc.Attrs):
	class title(xsc.TextAttr): pass


class align(xsc.Attrs):
	class align(xsc.TextAttr): values = (u"left", u"center", u"right", u"justify", u"char")


class char(xsc.Attrs):
	class char(xsc.TextAttr): pass


class charoff(xsc.Attrs):
	class charoff(xsc.TextAttr): pass


class span(xsc.Attrs):
	class span(xsc.TextAttr): pass


class valign(xsc.Attrs):
	class valign(xsc.TextAttr): values = (u"top", u"middle", u"bottom", u"baseline")


class width(xsc.Attrs):
	class width(xsc.TextAttr): pass


class align2(xsc.Attrs):
	class align(xsc.TextAttr): values = (u"left", u"right", u"center", u"justify", u"char")


class colname(xsc.Attrs):
	class colname(xsc.TextAttr): pass


class colsep(xsc.Attrs):
	class colsep(xsc.TextAttr): pass


class rowsep(xsc.Attrs):
	class rowsep(xsc.TextAttr): pass


class class3(xsc.Attrs):
	class class_(xsc.BoolAttr): xmlname = "class"


class linkend(xsc.Attrs):
	class linkend(xsc.TextAttr): required = True


class class4(xsc.Attrs):
	class class_(xsc.TextAttr):
		xmlname = "class"
		values = (u"graphicdesigner", u"productioneditor", u"copyeditor", u"technicaleditor", u"translator", u"other")


class nameend(xsc.Attrs):
	class nameend(xsc.TextAttr): pass


class namest(xsc.Attrs):
	class namest(xsc.TextAttr): pass


class spanname(xsc.Attrs):
	class spanname(xsc.TextAttr): pass


class valign2(xsc.Attrs):
	class valign(xsc.TextAttr): values = (u"top", u"middle", u"bottom")


class cols(xsc.Attrs):
	class cols(xsc.TextAttr): required = True


class tgroupstyle(xsc.Attrs):
	class tgroupstyle(xsc.TextAttr): pass


class floatstyle(xsc.Attrs):
	class floatstyle(xsc.TextAttr): pass


class float(xsc.Attrs):
	class float(xsc.TextAttr): pass


class pgwide(xsc.Attrs):
	class pgwide(xsc.TextAttr): pass


class baseform(xsc.Attrs):
	class baseform(xsc.TextAttr): pass


class linkend2(xsc.Attrs):
	class linkend(xsc.TextAttr): pass


class sortas(xsc.Attrs):
	class sortas(xsc.TextAttr): pass


class otherterm(xsc.Attrs):
	class otherterm(xsc.TextAttr): pass


class align3(xsc.Attrs):
	class align(xsc.TextAttr): values = (u"left", u"right", u"center")


class contentdepth(xsc.Attrs):
	class contentdepth(xsc.TextAttr): pass


class contentwidth(xsc.Attrs):
	class contentwidth(xsc.TextAttr): pass


class depth(xsc.Attrs):
	class depth(xsc.TextAttr): pass


class scale(xsc.Attrs):
	class scale(xsc.TextAttr): pass


class scalefit(xsc.Attrs):
	class scalefit(xsc.TextAttr): pass


class type2(xsc.Attrs):
	class type(xsc.TextAttr): pass


class align4(xsc.Attrs):
	class align(xsc.TextAttr): values = (u"left", u"center", u"right")


class bgcolor(xsc.Attrs):
	class bgcolor(xsc.TextAttr): pass


class border(xsc.Attrs):
	class border(xsc.TextAttr): pass


class cellpadding(xsc.Attrs):
	class cellpadding(xsc.TextAttr): pass


class cellspacing(xsc.Attrs):
	class cellspacing(xsc.TextAttr): pass


class frame(xsc.Attrs):
	class frame(xsc.TextAttr): values = (u"void", u"above", u"below", u"hsides", u"lhs", u"rhs", u"vsides", u"box", u"border", u"top", u"bottom", u"topbot", u"all", u"sides", u"none")


class orient(xsc.Attrs):
	class orient(xsc.TextAttr): values = (u"port", u"land")


class rules(xsc.Attrs):
	class rules(xsc.TextAttr): values = (u"none", u"groups", u"rows", u"cols", u"all")


class shortentry(xsc.Attrs):
	class shortentry(xsc.TextAttr): pass


class summary(xsc.Attrs):
	class summary(xsc.TextAttr): pass


class tabstyle(xsc.Attrs):
	class tabstyle(xsc.TextAttr): pass


class tocentry2(xsc.Attrs):
	class tocentry(xsc.TextAttr): pass


class spacing(xsc.Attrs):
	class spacing(xsc.TextAttr): values = (u"normal", u"compact")


class action2(xsc.Attrs):
	class action(xsc.TextAttr): values = (u"click", u"double-click", u"press", u"seq", u"simul", u"other")


class otheraction(xsc.Attrs):
	class otheraction(xsc.TextAttr): pass


class endterm(xsc.Attrs):
	class endterm(xsc.TextAttr): pass


class xrefstyle(xsc.Attrs):
	class xrefstyle(xsc.TextAttr): pass


class class5(xsc.Attrs):
	class class_(xsc.TextAttr):
		xmlname = "class"
		values = (u"service", u"trade", u"registered", u"copyright")


class performance(xsc.Attrs):
	class performance(xsc.TextAttr): values = (u"optional", u"required")


class abbr(xsc.Attrs):
	class abbr(xsc.TextAttr): pass


class axis(xsc.Attrs):
	class axis(xsc.TextAttr): pass


class colspan(xsc.Attrs):
	class colspan(xsc.TextAttr): pass


class headers(xsc.Attrs):
	class headers(xsc.TextAttr): pass


class height(xsc.Attrs):
	class height(xsc.TextAttr): pass


class nowrap(xsc.Attrs):
	class nowrap(xsc.BoolAttr): pass


class rowspan(xsc.Attrs):
	class rowspan(xsc.TextAttr): pass


class scope(xsc.Attrs):
	class scope(xsc.TextAttr): values = (u"row", u"col", u"rowgroup", u"colgroup")


###
### Elements
###

class abbrev(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class abstract(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class accel(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class ackno(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class acronym(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class action(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class address(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, continuation, dir, format, id, lang, language, linenumbering, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, xreflabel):
		pass


class affiliation(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class alt(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class anchor(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, id2, os, pagenum, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class answer(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class appendix(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class appendixinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class application(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"hardware", u"software")


class area(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, coords, dir, id2, label2, lang, linkends, os, otherunits, remap, revision2, revisionflag, role, security, units, userlevel, vendor, xreflabel):
		pass


class areaset(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, coords, dir, id2, label2, lang, os, otherunits, remap, revision2, revisionflag, role, security, units, userlevel, vendor, xreflabel):
		pass


class areaspec(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, otherunits, remap, revision2, revisionflag, role, security, units, userlevel, vendor, xreflabel):
		pass


class arg(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, choice, condition, conformance, dir, id, lang, os, remap, rep, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class article(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"journalarticle", u"productsheet", u"whitepaper", u"techreport", u"specification", u"faq")
		class parentbook(xsc.TextAttr): pass


class articleinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class artpagenums(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class attribution(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class audiodata(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, entityref, fileref, format2, id, lang, os, remap, revision2, revisionflag, role, security, srccredit, userlevel, vendor, xreflabel):
		pass


class audioobject(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class author(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class authorblurb(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class authorgroup(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class authorinitials(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class beginpage(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, pagenum, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class bibliocoverage(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class otherspatial(xsc.TextAttr): pass
		class othertemporal(xsc.TextAttr): pass
		class spatial(xsc.TextAttr): values = (u"dcmipoint", u"iso3166", u"dcmibox", u"tgn", u"otherspatial")
		class temporal(xsc.TextAttr): values = (u"dcmiperiod", u"w3c-dtf", u"othertemporal")


class bibliodiv(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class biblioentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class bibliography(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class bibliographyinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class biblioid(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class_, condition, conformance, dir, id, lang, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class bibliomisc(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class bibliomixed(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class bibliomset(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, relation, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class bibliorelation(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class_, condition, conformance, dir, id, lang, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class othertype(xsc.TextAttr): pass
		class type(xsc.TextAttr): values = (u"isversionof", u"hasversion", u"isreplacedby", u"replaces", u"isrequiredby", u"requires", u"ispartof", u"haspart", u"isreferencedby", u"references", u"isformatof", u"hasformat", u"othertype")


class biblioset(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, relation, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class bibliosource(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class_, condition, conformance, dir, id, lang, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class blockinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class blockquote(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class book(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, fpi, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class bookinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, contents, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class bridgehead(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class renderas(xsc.TextAttr): values = (u"other", u"sect1", u"sect2", u"sect3", u"sect4", u"sect5")


class callout(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class arearefs(xsc.TextAttr): required = True


class calloutlist(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class caption(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class2, condition, conformance, dir, id, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, security, style, title2, userlevel, vendor, xreflabel):
		class align(xsc.TextAttr): values = (u"top", u"bottom", u"left", u"right")


class caution(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class chapter(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class chapterinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class citation(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class citebiblioid(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class_, condition, conformance, dir, id, lang, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class citerefentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class citetitle(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class pubwork(xsc.TextAttr): values = (u"article", u"book", u"chapter", u"part", u"refentry", u"section", u"journal", u"series", u"set", u"manuscript", u"cdrom", u"dvd", u"wiki", u"gopher", u"bbs", u"emailmessage", u"webpage", u"newsposting")


class city(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class classname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class classsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, language, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"class", u"interface")


class classsynopsisinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, continuation, dir, format, id, lang, language, linenumbering, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, xreflabel):
		pass


class cmdsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class cmdlength(xsc.TextAttr): pass
		class sepchar(xsc.TextAttr): pass


class co(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id2, label2, lang, linkends, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class code(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, language, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class col(xsc.Element):
	xmlns = xmlns
	class Attrs(align, char, charoff, class2, id, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, span, style, title2, valign, width):
		pass


class colgroup(xsc.Element):
	xmlns = xmlns
	class Attrs(align, char, charoff, class2, id, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, span, style, title2, valign, width):
		pass


class collab(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class collabname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class colophon(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class colspec(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, char, charoff, colname, colsep, rowsep):
		class colnum(xsc.TextAttr): pass
		class colwidth(xsc.TextAttr): pass


class command(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class computeroutput(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class confdates(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class confgroup(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class confnum(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class confsponsor(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class conftitle(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class constant(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class3, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class constructorsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, language, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class contractnum(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class contractsponsor(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class contrib(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class copyright(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class coref(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class corpauthor(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class corpcredit(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class4, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class corpname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class country(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class database(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"name", u"table", u"field", u"key1", u"key2", u"record", u"index", u"view", u"primarykey", u"secondarykey", u"foreignkey", u"altkey", u"procedure", u"datatype", u"constraint", u"rule", u"user", u"group")


class date(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class dedication(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class destructorsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, language, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class edition(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class editor(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class email(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class emphasis(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class entry(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, arch, char, charoff, class2, colname, colsep, condition, conformance, dir, id, lang, nameend, namest, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, rowsep, security, spanname, style, title2, userlevel, valign2, vendor, xreflabel):
		class morerows(xsc.TextAttr): pass
		class rotate(xsc.TextAttr): pass


class entrytbl(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, arch, char, charoff, class2, colname, cols, colsep, condition, conformance, dir, id, lang, nameend, namest, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, rowsep, security, spanname, style, tgroupstyle, title2, userlevel, vendor, xreflabel):
		pass


class envar(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class epigraph(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class equation(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, floatstyle, id, label2, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class errorcode(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class errorname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class errortext(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class errortype(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class example(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, floatstyle, id, label2, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, width, xreflabel):
		pass


class exceptionname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class fax(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class fieldsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, language, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class figure(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, float, floatstyle, id, label2, lang, os, pgwide, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class filename(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"headerfile", u"partition", u"devicefile", u"libraryfile", u"directory", u"extension", u"symlink")
		class path(xsc.TextAttr): pass


class firstname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class firstterm(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, baseform, condition, conformance, dir, id, lang, linkend2, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class footnote(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class footnoteref(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class foreignphrase(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class formalpara(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class funcdef(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class funcparams(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class funcprototype(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class funcsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class funcsynopsisinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, continuation, dir, format, id, lang, language, linenumbering, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, xreflabel):
		pass


class function(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class glossary(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class glossaryinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class glossdef(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class subject(xsc.TextAttr): pass


class glossdiv(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class glossentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, sortas, userlevel, vendor, xreflabel):
		pass


class glosslist(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class glosssee(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, otherterm, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class glossseealso(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, otherterm, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class glossterm(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, baseform, condition, conformance, dir, id, lang, linkend2, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class graphic(xsc.Element):
	xmlns = xmlns
	class Attrs(align3, arch, condition, conformance, contentdepth, contentwidth, depth, dir, entityref, fileref, format2, id, lang, os, remap, revision2, revisionflag, role, scale, scalefit, security, srccredit, userlevel, valign2, vendor, width, xreflabel):
		pass


class graphicco(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class group(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, choice, condition, conformance, dir, id, lang, os, remap, rep, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class guibutton(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class guiicon(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class guilabel(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class guimenu(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class guimenuitem(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class guisubmenu(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class hardware(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class highlights(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class holder(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class honorific(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class imagedata(xsc.Element):
	xmlns = xmlns
	class Attrs(align3, arch, condition, conformance, contentdepth, contentwidth, depth, dir, entityref, fileref, format2, id, lang, os, remap, revision2, revisionflag, role, scale, scalefit, security, srccredit, userlevel, valign2, vendor, width, xreflabel):
		pass


class imageobject(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class imageobjectco(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class important(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class index(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, type2, userlevel, vendor, xreflabel):
		pass


class indexdiv(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class indexentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class indexinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class indexterm(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, pagenum, remap, revision2, revisionflag, role, security, type2, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"singular", u"startofrange", u"endofrange")
		class scope(xsc.TextAttr): values = (u"all", u"global", u"local")
		class significance(xsc.TextAttr): values = (u"preferred", u"normal")
		class startref(xsc.TextAttr): pass
		class zone(xsc.TextAttr): pass


class informalequation(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, floatstyle, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class informalexample(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, floatstyle, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, width, xreflabel):
		pass


class informalfigure(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, float, floatstyle, id, label2, lang, os, pgwide, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class informaltable(xsc.Element):
	xmlns = xmlns
	class Attrs(align4, arch, bgcolor, border, cellpadding, cellspacing, class2, colsep, condition, conformance, dir, floatstyle, frame, id, label2, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, orient, os, pgwide, remap, revision2, revisionflag, role, rowsep, rules, security, shortentry, style, summary, tabstyle, title2, tocentry2, userlevel, vendor, width, xreflabel):
		pass


class initializer(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class inlineequation(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class inlinegraphic(xsc.Element):
	xmlns = xmlns
	class Attrs(align3, arch, condition, conformance, contentdepth, contentwidth, depth, dir, entityref, fileref, format2, id, lang, os, remap, revision2, revisionflag, role, scale, scalefit, security, srccredit, userlevel, valign2, vendor, width, xreflabel):
		pass


class inlinemediaobject(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class interface(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class interfacename(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class invpartnumber(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class isbn(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class issn(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class issuenum(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class itemizedlist(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, spacing, userlevel, vendor, xreflabel):
		class mark(xsc.TextAttr): pass


class itermset(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class jobtitle(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class keycap(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class function(xsc.TextAttr): values = (u"alt", u"control", u"shift", u"meta", u"escape", u"enter", u"tab", u"backspace", u"command", u"option", u"space", u"delete", u"insert", u"up", u"down", u"left", u"right", u"home", u"end", u"pageup", u"pagedown", u"other")
		class otherfunction(xsc.TextAttr): pass


class keycode(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class keycombo(xsc.Element):
	xmlns = xmlns
	class Attrs(action2, arch, condition, conformance, dir, id, lang, moreinfo, os, otheraction, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class keysym(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class keyword(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class keywordset(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class label(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class legalnotice(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class lineage(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class lineannotation(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class link(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, endterm, id, lang, linkend, os, remap, revision2, revisionflag, role, security, type2, userlevel, vendor, xreflabel, xrefstyle):
		pass


class listitem(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class override(xsc.TextAttr): pass


class literal(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class literallayout(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, continuation, dir, format, id, lang, language, linenumbering, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, width, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"monospaced", u"normal")


class lot(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class lotentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, linkend2, os, pagenum, remap, revision2, revisionflag, role, security, srccredit, userlevel, vendor, xreflabel):
		pass


class manvolnum(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class markup(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class medialabel(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"cartridge", u"cdrom", u"disk", u"tape")


class mediaobject(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class mediaobjectco(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class member(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class menuchoice(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class methodname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class methodparam(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, rep, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class choice(xsc.TextAttr): values = (u"opt", u"req", u"plain")


class methodsynopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, language, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class modespec(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class application(xsc.TextAttr): pass


class modifier(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class mousebutton(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msg(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msgaud(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msgentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msgexplan(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msginfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msglevel(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msgmain(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msgorig(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msgrel(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msgset(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msgsub(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class msgtext(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class note(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class objectinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class olink(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, type2, userlevel, vendor, xreflabel, xrefstyle):
		class linkmode(xsc.TextAttr): pass
		class localinfo(xsc.TextAttr): pass
		class targetdoc(xsc.TextAttr): pass
		class targetdocent(xsc.TextAttr): pass
		class targetptr(xsc.TextAttr): pass


class ooclass(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class ooexception(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class oointerface(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class option(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class optional(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class orderedlist(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, spacing, userlevel, vendor, xreflabel):
		class continuation(xsc.TextAttr): values = (u"continues", u"restarts")
		class inheritnum(xsc.TextAttr): values = (u"inherit", u"ignore")
		class numeration(xsc.TextAttr): values = (u"arabic", u"upperalpha", u"loweralpha", u"upperroman", u"lowerroman")


class orgdiv(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class orgname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, otherclass, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"corporation", u"nonprofit", u"consortium", u"informal", u"other")


class otheraddr(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class othercredit(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class4, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class othername(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class pagenums(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class para(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class paramdef(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class choice(xsc.TextAttr): values = (u"opt", u"req")


class parameter(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"command", u"function", u"option")


class part(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class partinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class partintro(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class personblurb(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class personname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class phone(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class phrase(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class pob(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class postcode(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class preface(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class prefaceinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class primary(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, sortas, userlevel, vendor, xreflabel):
		pass


class primaryie(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, linkends, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class printhistory(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class procedure(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class productname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class5, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class productnumber(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class programlisting(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, continuation, dir, format, id, lang, language, linenumbering, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, width, xreflabel):
		pass


class programlistingco(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class prompt(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class property(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class pubdate(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class publisher(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class publishername(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class pubsnumber(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class qandadiv(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class qandaentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class qandaset(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class defaultlabel(xsc.TextAttr): values = (u"qanda", u"number", u"none")


class question(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class quote(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refclass(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refdescriptor(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class refentryinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refentrytitle(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class reference(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class referenceinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refmeta(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refmiscinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class2, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refnamediv(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refpurpose(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refsect1(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class refsect1info(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refsect2(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class refsect2info(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refsect3(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class refsect3info(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refsection(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class refsectioninfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refsynopsisdiv(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class refsynopsisdivinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class releaseinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class remark(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class replaceable(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"command", u"function", u"option", u"parameter")


class returnvalue(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class revdescription(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class revhistory(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class revision(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class revnumber(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class revremark(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class row(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class2, condition, conformance, dir, id, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, rowsep, security, style, title2, userlevel, valign2, vendor, xreflabel):
		pass


class sbr(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class screen(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, continuation, dir, format, id, lang, language, linenumbering, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, width, xreflabel):
		pass


class screenco(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class screeninfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class screenshot(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class secondary(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, sortas, userlevel, vendor, xreflabel):
		pass


class secondaryie(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, linkends, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class sect1(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		class renderas(xsc.TextAttr): values = (u"sect2", u"sect3", u"sect4", u"sect5")


class sect1info(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class sect2(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		class renderas(xsc.TextAttr): values = (u"sect1", u"sect3", u"sect4", u"sect5")


class sect2info(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class sect3(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		class renderas(xsc.TextAttr): values = (u"sect1", u"sect2", u"sect4", u"sect5")


class sect3info(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class sect4(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		class renderas(xsc.TextAttr): values = (u"sect1", u"sect2", u"sect3", u"sect5")


class sect4info(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class sect5(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		class renderas(xsc.TextAttr): values = (u"sect1", u"sect2", u"sect3", u"sect4")


class sect5info(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class section(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class sectioninfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class see(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class seealso(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class seealsoie(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, linkends, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class seeie(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, linkend2, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class seg(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class seglistitem(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class segmentedlist(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class segtitle(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class seriesvolnums(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class set(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, fpi, id, lang, os, remap, revision2, revisionflag, role, security, status, userlevel, vendor, xreflabel):
		pass


class setindex(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class setindexinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class setinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, contents, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class sgmltag(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"attribute", u"attvalue", u"element", u"endtag", u"emptytag", u"genentity", u"numcharref", u"paramentity", u"pi", u"xmlpi", u"starttag", u"sgmlcomment", u"prefix", u"namespace", u"localname")
		class namespace(xsc.TextAttr): pass


class shortaffil(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class shortcut(xsc.Element):
	xmlns = xmlns
	class Attrs(action2, arch, condition, conformance, dir, id, lang, moreinfo, os, otheraction, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class sidebar(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class sidebarinfo(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class simpara(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class simplelist(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class columns(xsc.TextAttr): pass
		class type(xsc.TextAttr): values = (u"inline", u"vert", u"horiz")


class simplemsgentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class audience(xsc.TextAttr): pass
		class level(xsc.TextAttr): pass
		class origin(xsc.TextAttr): pass


class simplesect(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class spanspec(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, char, charoff, colsep, rowsep):
		class nameend(xsc.TextAttr): required = True
		class namest(xsc.TextAttr): required = True
		class spanname(xsc.TextAttr): required = True


class state(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class step(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, performance, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class stepalternatives(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, performance, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class street(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class structfield(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class structname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class subject(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class weight(xsc.TextAttr): pass


class subjectset(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class scheme(xsc.TextAttr): pass


class subjectterm(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class subscript(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class substeps(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, performance, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class subtitle(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class superscript(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class surname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class symbol(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class3, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class synopfragment(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id2, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class synopfragmentref(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class synopsis(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, continuation, dir, format, id, label2, lang, language, linenumbering, os, remap, revision2, revisionflag, role, security, startinglinenumber, userlevel, vendor, xreflabel):
		pass


class systemitem(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class class_(xsc.TextAttr):
			xmlname = "class"
			values = (u"constant", u"event", u"eventhandler", u"domainname", u"fqdomainname", u"ipaddress", u"netmask", u"etheraddress", u"groupname", u"library", u"macro", u"osname", u"filesystem", u"resource", u"systemname", u"username", u"newsgroup", u"process", u"service", u"server", u"daemon")


class table(xsc.Element):
	xmlns = xmlns
	class Attrs(align4, arch, bgcolor, border, cellpadding, cellspacing, class2, colsep, condition, conformance, dir, floatstyle, frame, id, label2, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, orient, os, pgwide, remap, revision2, revisionflag, role, rowsep, rules, security, shortentry, style, summary, tabstyle, title2, tocentry2, userlevel, vendor, width, xreflabel):
		pass


class task(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class taskprerequisites(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class taskrelated(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class tasksummary(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class tbody(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class2, condition, conformance, dir, id, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, security, style, title2, userlevel, valign2, vendor, xreflabel):
		pass


class td(xsc.Element):
	xmlns = xmlns
	class Attrs(abbr, align, axis, bgcolor, char, charoff, class2, colspan, headers, height, id, nowrap, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, rowspan, scope, style, title2, valign, width):
		pass


class term(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class tertiary(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, sortas, userlevel, vendor, xreflabel):
		pass


class tertiaryie(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, linkends, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class textdata(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, entityref, fileref, format2, id, lang, os, remap, revision2, revisionflag, role, security, srccredit, userlevel, vendor, xreflabel):
		class encoding(xsc.TextAttr): pass


class textobject(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class tfoot(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class2, condition, conformance, dir, id, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, security, style, title2, userlevel, valign2, vendor, xreflabel):
		pass


class tgroup(xsc.Element):
	xmlns = xmlns
	class Attrs(align2, arch, char, charoff, class2, cols, colsep, condition, conformance, dir, id, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, rowsep, security, style, tgroupstyle, title2, userlevel, vendor, xreflabel):
		pass


class th(xsc.Element):
	xmlns = xmlns
	class Attrs(abbr, align, axis, bgcolor, char, charoff, class2, colspan, headers, height, id, nowrap, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, rowspan, scope, style, title2, valign, width):
		pass


class thead(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class2, condition, conformance, dir, id, lang, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, os, remap, revision2, revisionflag, role, security, style, title2, userlevel, valign2, vendor, xreflabel):
		pass


class tip(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class title(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, pagenum, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class titleabbrev(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class toc(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, pagenum, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class tocback(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, linkend2, os, pagenum, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class tocchap(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class tocentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, linkend2, os, pagenum, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class tocfront(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, label2, lang, linkend2, os, pagenum, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class toclevel1(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class toclevel2(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class toclevel3(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class toclevel4(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class toclevel5(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class tocpart(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class token(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class tr(xsc.Element):
	xmlns = xmlns
	class Attrs(align, bgcolor, char, charoff, class2, id, onclick, ondblclick, onkeydown, onkeypress, onkeyup, onmousedown, onmousemove, onmouseout, onmouseover, onmouseup, style, title2, valign):
		pass


class trademark(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, class5, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class type(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class ulink(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, type2, userlevel, vendor, xreflabel, xrefstyle):
		class url(xsc.TextAttr): required = True


class uri(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, type2, userlevel, vendor, xreflabel):
		pass


class userinput(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, moreinfo, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class varargs(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class variablelist(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		class termlength(xsc.TextAttr): pass


class varlistentry(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class varname(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class videodata(xsc.Element):
	xmlns = xmlns
	class Attrs(align3, arch, condition, conformance, contentdepth, contentwidth, depth, dir, entityref, fileref, format2, id, lang, os, remap, revision2, revisionflag, role, scale, scalefit, security, srccredit, userlevel, valign2, vendor, width, xreflabel):
		pass


class videoobject(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class void(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class volumenum(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class warning(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class wordasword(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


class xref(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, endterm, id, lang, linkend, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel, xrefstyle):
		pass


class year(xsc.Element):
	xmlns = xmlns
	class Attrs(arch, condition, conformance, dir, id, lang, os, remap, revision2, revisionflag, role, security, userlevel, vendor, xreflabel):
		pass


glossentry.model = sims.Elements(abbrev, glossdef, glosssee, revhistory, acronym, glossterm, indexterm)
collab.model = sims.Elements(affiliation, collabname)
qandaentry.model = sims.Elements(answer, blockinfo, question, revhistory)
areaset.model = sims.Elements(area)
areaspec.model = sims.Elements(areaset, area)
mediaobject.model = sims.Elements(audioobject, caption, videoobject, textobject, objectinfo, imageobject)
inlinemediaobject.model = sims.Elements(audioobject, objectinfo, imageobject, videoobject, textobject)
glosslist.model = sims.Elements(blockinfo, glossentry, titleabbrev, title)
set.model = sims.Elements(book, setinfo, subtitle, title, toc, set, setindex, titleabbrev)
calloutlist.model = sims.Elements(callout, titleabbrev, title)
ooclass.model = sims.Elements(classname, modifier)
classsynopsis.model = sims.Elements(classsynopsisinfo, destructorsynopsis, methodsynopsis, fieldsynopsis, oointerface, ooclass, ooexception, constructorsynopsis)
colgroup.model = sims.Elements(col)
entrytbl.model = sims.Elements(colspec, spanspec, tbody, thead)
tgroup.model = sims.Elements(colspec, spanspec, tfoot, tbody, thead)
tfoot.model = \
thead.model = sims.Elements(colspec, tr, row)
confgroup.model = sims.Elements(confdates, conftitle, confsponsor, confnum, address)
biblioentry.model = sims.Elements(contractsponsor, isbn, contractnum, pubdate, productnumber, abstract, address, invpartnumber, titleabbrev, printhistory, edition, releaseinfo, pubsnumber, contrib, seriesvolnums, corpauthor, bibliorelation, authorgroup, artpagenums, author, orgname, confgroup, authorinitials, pagenums, editor, volumenum, honorific, corpname, indexterm, othername, firstname, citebiblioid, issuenum, collab, othercredit, corpcredit, citetitle, biblioset, bibliomisc, date, surname, lineage, publisher, biblioid, publishername, copyright, subtitle, affiliation, bibliocoverage, issn, articleinfo, bibliosource, productname, authorblurb, personname, abbrev, title, revhistory)
biblioset.model = sims.Elements(contractsponsor, isbn, contractnum, pubdate, productnumber, abstract, bibliomisc, invpartnumber, titleabbrev, printhistory, edition, releaseinfo, pubsnumber, contrib, seriesvolnums, corpauthor, authorgroup, artpagenums, author, orgname, confgroup, authorinitials, pagenums, editor, volumenum, honorific, corpname, indexterm, othername, issuenum, firstname, citebiblioid, bibliorelation, collab, othercredit, corpcredit, citetitle, biblioset, address, date, surname, lineage, publisher, biblioid, publishername, copyright, subtitle, affiliation, bibliocoverage, issn, bibliosource, productname, authorblurb, personname, abbrev, title, revhistory)
authorgroup.model = sims.Elements(editor, author, corpauthor, collab, othercredit, corpcredit)
row.model = sims.Elements(entry, entrytbl)
funcsynopsis.model = sims.Elements(funcprototype, funcsynopsisinfo)
graphicco.model = sims.Elements(graphic, areaspec, calloutlist)
informaltable.model = sims.Elements(graphic, colgroup, mediaobject, tr, tbody, tgroup, tfoot, textobject, blockinfo, col, thead)
table.model = sims.Elements(graphic, title, mediaobject, colgroup, tr, titleabbrev, tbody, caption, tgroup, tfoot, textobject, blockinfo, indexterm, col, thead)
synopfragment.model = sims.Elements(group, arg)
menuchoice.model = sims.Elements(guimenu, guilabel, guisubmenu, shortcut, guibutton, interface, guiicon, guimenuitem)
copyright.model = sims.Elements(holder, year)
personname.model = sims.Elements(honorific, lineage, othername, surname, firstname)
imageobjectco.model = sims.Elements(imageobject, areaspec, calloutlist)
mediaobjectco.model = sims.Elements(imageobjectco, objectinfo, textobject)
itermset.model = sims.Elements(indexterm)
formalpara.model = sims.Elements(indexterm, para, title)
inlineequation.model = sims.Elements(inlinemediaobject, alt, graphic)
appendixinfo.model = \
articleinfo.model = \
bibliographyinfo.model = \
blockinfo.model = \
bookinfo.model = \
chapterinfo.model = \
glossaryinfo.model = \
indexinfo.model = \
objectinfo.model = \
partinfo.model = \
prefaceinfo.model = \
refentryinfo.model = \
referenceinfo.model = \
refsect1info.model = \
refsect2info.model = \
refsect3info.model = \
refsectioninfo.model = \
refsynopsisdivinfo.model = \
sect1info.model = \
sect2info.model = \
sect3info.model = \
sect4info.model = \
sect5info.model = \
sectioninfo.model = \
setindexinfo.model = \
setinfo.model = \
sidebarinfo.model = sims.Elements(isbn, contractnum, productnumber, mediaobject, revhistory, itermset, printhistory, modespec, contrib, surname, copyright, title, personname, authorinitials, editor, volumenum, honorific, othername, keywordset, issuenum, corpcredit, othercredit, titleabbrev, biblioset, legalnotice, bibliomisc, lineage, graphic, subtitle, affiliation, bibliosource, productname, contractsponsor, seriesvolnums, pubdate, abstract, invpartnumber, authorblurb, edition, releaseinfo, pubsnumber, corpauthor, authorgroup, author, orgname, confgroup, pagenums, bibliorelation, corpname, indexterm, subjectset, firstname, citebiblioid, collab, citetitle, address, date, publisher, biblioid, publishername, artpagenums, bibliocoverage, issn, abbrev)
keycombo.model = \
shortcut.model = sims.Elements(keycap, mousebutton, keysym, keycombo)
keywordset.model = sims.Elements(keyword)
author.model = \
editor.model = \
othercredit.model = sims.Elements(lineage, surname, firstname, authorblurb, personname, othername, address, personblurb, affiliation, honorific, contrib, email)
lot.model = sims.Elements(lotentry, beginpage, subtitle, titleabbrev, title)
citerefentry.model = sims.Elements(manvolnum, refentrytitle)
refmeta.model = sims.Elements(manvolnum, refmiscinfo, indexterm, refentrytitle)
informalequation.model = sims.Elements(mediaobject, blockinfo, graphic, alt)
equation.model = sims.Elements(mediaobject, graphic, informalequation, alt, title, blockinfo, titleabbrev)
screenshot.model = sims.Elements(mediaobjectco, screeninfo, graphic, mediaobject, graphicco)
simplelist.model = sims.Elements(member)
methodsynopsis.model = sims.Elements(methodparam, exceptionname, methodname, void, modifier, type)
constructorsynopsis.model = \
destructorsynopsis.model = sims.Elements(methodparam, void, modifier, methodname, exceptionname)
ooexception.model = sims.Elements(modifier, exceptionname)
oointerface.model = sims.Elements(modifier, interfacename)
msgentry.model = sims.Elements(msg, msgexplan, msginfo)
msgset.model = sims.Elements(msgentry, blockinfo, titleabbrev, simplemsgentry, title)
msginfo.model = sims.Elements(msglevel, msgorig, msgaud)
msg.model = sims.Elements(msgmain, msgsub, msgrel, title)
simplemsgentry.model = sims.Elements(msgtext, msgexplan)
msgmain.model = \
msgrel.model = \
msgsub.model = sims.Elements(msgtext, title)
audioobject.model = sims.Elements(objectinfo, audiodata)
imageobject.model = sims.Elements(objectinfo, imagedata)
affiliation.model = sims.Elements(orgname, jobtitle, orgdiv, shortaffil, address)
highlights.model = sims.Elements(para, tip, formalpara, warning, caution, glosslist, orderedlist, indexterm, simpara, segmentedlist, note, important, variablelist, simplelist, itemizedlist, calloutlist)
funcprototype.model = sims.Elements(paramdef, varargs, funcdef, void, modifier)
programlistingco.model = sims.Elements(programlisting, areaspec, calloutlist)
informalfigure.model = sims.Elements(programlisting, blockquote, funcsynopsis, screenshot, cmdsynopsis, mediaobject, graphicco, mediaobjectco, informalequation, fieldsynopsis, link, informalexample, address, blockinfo, literallayout, beginpage, classsynopsis, graphic, destructorsynopsis, programlistingco, screenco, informalfigure, methodsynopsis, informaltable, synopsis, constructorsynopsis, ulink, indexterm, screen, olink)
legalnotice.model = sims.Elements(programlisting, blockquote, para, simpara, screen, beginpage, segmentedlist, warning, caution, blockinfo, glosslist, orderedlist, literallayout, itemizedlist, screenshot, title, programlistingco, tip, formalpara, note, screenco, important, variablelist, simplelist, indexterm, calloutlist)
textobject.model = sims.Elements(programlisting, blockquote, para, tip, screen, textdata, formalpara, warning, caution, phrase, literallayout, objectinfo, orderedlist, glosslist, screenshot, programlistingco, simpara, segmentedlist, note, screenco, important, variablelist, simplelist, itemizedlist, calloutlist)
dedication.model = sims.Elements(programlisting, blockquote, subtitle, para, simpara, screen, beginpage, titleabbrev, segmentedlist, warning, caution, literallayout, glosslist, orderedlist, itemizedlist, screenshot, title, programlistingco, tip, formalpara, note, screenco, important, variablelist, simplelist, indexterm, calloutlist)
colophon.model = sims.Elements(programlisting, blockquote, subtitle, para, simpara, screen, titleabbrev, segmentedlist, warning, caution, literallayout, glosslist, orderedlist, screenshot, title, programlistingco, tip, formalpara, note, screenco, important, variablelist, simplelist, itemizedlist, calloutlist)
step.model = sims.Elements(programlisting, bridgehead, funcsynopsis, figure, cmdsynopsis, mediaobject, mediaobjectco, segmentedlist, informalequation, fieldsynopsis, caution, informalexample, table, literallayout, msgset, graphicco, task, glosslist, destructorsynopsis, title, screenshot, highlights, substeps, tip, formalpara, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, indexterm, abstract, calloutlist, blockquote, para, screen, beginpage, qandaset, simplelist, important, address, orderedlist, classsynopsis, sidebar, remark, graphic, stepalternatives, programlistingco, equation, authorblurb, example, synopsis, warning, variablelist, simpara, epigraph, itemizedlist, anchor, procedure)
sect1.model = sims.Elements(programlisting, bridgehead, subtitle, cmdsynopsis, mediaobject, titleabbrev, informalequation, fieldsynopsis, funcsynopsis, literallayout, msgset, bibliography, title, highlights, formalpara, methodsynopsis, lot, toc, calloutlist, blockquote, para, remark, qandaset, orderedlist, classsynopsis, graphic, glossary, equation, epigraph, itemizedlist, anchor, procedure, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, index, sidebar, destructorsynopsis, authorblurb, sect1info, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, beginpage, screenshot, screen, graphicco, refentry, important, address, sect2, simplelist, mediaobjectco, task, programlistingco, example, synopsis, variablelist, simpara)
itemizedlist.model = \
orderedlist.model = sims.Elements(programlisting, funcsynopsis, cmdsynopsis, abstract, titleabbrev, tip, informalequation, warning, caution, informalexample, blockinfo, literallayout, destructorsynopsis, title, highlights, bridgehead, simpara, formalpara, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, indexterm, mediaobject, listitem, blockquote, screenshot, screen, graphicco, remark, important, para, address, beginpage, classsynopsis, mediaobjectco, graphic, programlistingco, authorblurb, synopsis, fieldsynopsis, epigraph, anchor)
informalexample.model = sims.Elements(programlisting, funcsynopsis, cmdsynopsis, mediaobject, mediaobjectco, segmentedlist, informalequation, fieldsynopsis, informalexample, blockinfo, glosslist, literallayout, para, informaltable, simpara, formalpara, informalfigure, methodsynopsis, destructorsynopsis, screenco, constructorsynopsis, indexterm, calloutlist, blockquote, screenshot, screen, graphicco, address, orderedlist, beginpage, classsynopsis, graphic, programlistingco, synopsis, variablelist, simplelist, itemizedlist)
footnote.model = sims.Elements(programlisting, funcsynopsis, cmdsynopsis, mediaobject, mediaobjectco, segmentedlist, informalequation, fieldsynopsis, informalexample, literallayout, glosslist, para, informaltable, simpara, formalpara, informalfigure, methodsynopsis, destructorsynopsis, screenco, constructorsynopsis, calloutlist, blockquote, screenshot, screen, graphicco, address, orderedlist, classsynopsis, graphic, programlistingco, synopsis, variablelist, simplelist, itemizedlist)
figure.model = sims.Elements(programlisting, funcsynopsis, cmdsynopsis, mediaobject, titleabbrev, informalequation, fieldsynopsis, informalexample, blockinfo, literallayout, destructorsynopsis, title, informalfigure, methodsynopsis, informaltable, screenco, constructorsynopsis, indexterm, olink, blockquote, screenshot, screen, graphicco, link, address, beginpage, classsynopsis, mediaobjectco, graphic, programlistingco, synopsis, ulink)
example.model = sims.Elements(programlisting, funcsynopsis, cmdsynopsis, mediaobject, titleabbrev, segmentedlist, informalequation, fieldsynopsis, informalexample, blockinfo, glosslist, literallayout, para, title, simpara, formalpara, informalfigure, methodsynopsis, destructorsynopsis, screenco, constructorsynopsis, indexterm, calloutlist, blockquote, screenshot, screen, graphicco, address, orderedlist, beginpage, classsynopsis, mediaobjectco, graphic, informaltable, programlistingco, synopsis, variablelist, simplelist, itemizedlist)
caution.model = \
important.model = \
note.model = \
tip.model = \
warning.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, mediaobjectco, formalpara, informalequation, fieldsynopsis, informalexample, table, literallayout, glosslist, sidebar, destructorsynopsis, title, screenshot, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, informaltable, screenco, constructorsynopsis, indexterm, calloutlist, blockquote, para, screen, graphicco, address, orderedlist, beginpage, classsynopsis, remark, graphic, programlistingco, equation, example, synopsis, variablelist, simplelist, itemizedlist, anchor, procedure)
revdescription.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, mediaobjectco, formalpara, informalequation, warning, caution, informalexample, table, literallayout, glosslist, destructorsynopsis, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, indexterm, calloutlist, blockquote, screenshot, screen, graphicco, important, para, address, orderedlist, classsynopsis, remark, graphic, programlistingco, equation, tip, example, synopsis, fieldsynopsis, variablelist, simplelist, itemizedlist, anchor, procedure)
answer.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, mediaobjectco, formalpara, informalequation, warning, caution, informalexample, table, literallayout, glosslist, methodsynopsis, destructorsynopsis, highlights, bridgehead, simpara, segmentedlist, informalfigure, label, note, informaltable, screenco, constructorsynopsis, indexterm, calloutlist, blockquote, screenshot, qandaentry, screen, graphicco, important, para, address, orderedlist, classsynopsis, remark, graphic, programlistingco, equation, tip, example, synopsis, fieldsynopsis, variablelist, simplelist, itemizedlist, anchor, procedure)
question.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, mediaobjectco, formalpara, informalequation, warning, caution, informalexample, table, literallayout, glosslist, methodsynopsis, destructorsynopsis, highlights, bridgehead, simpara, segmentedlist, informalfigure, label, note, informaltable, screenco, constructorsynopsis, indexterm, calloutlist, blockquote, screenshot, screen, graphicco, important, para, address, orderedlist, classsynopsis, remark, graphic, programlistingco, equation, tip, example, synopsis, fieldsynopsis, variablelist, simplelist, itemizedlist, anchor, procedure)
blockquote.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, mediaobjectco, formalpara, tip, informalequation, warning, caution, informalexample, table, blockinfo, glosslist, literallayout, msgset, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, attribution, screenshot, screen, graphicco, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, remark, task, programlistingco, equation, authorblurb, example, synopsis, fieldsynopsis, variablelist, epigraph, itemizedlist, anchor, procedure)
callout.model = \
listitem.model = \
msgtext.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, mediaobjectco, formalpara, tip, informalequation, warning, caution, informalexample, table, literallayout, glosslist, msgset, destructorsynopsis, authorblurb, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, remark, task, programlistingco, equation, graphic, example, synopsis, fieldsynopsis, variablelist, epigraph, itemizedlist, anchor, procedure)
msgexplan.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, mediaobjectco, formalpara, tip, informalequation, warning, caution, informalexample, table, literallayout, glosslist, msgset, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, remark, task, programlistingco, equation, authorblurb, example, synopsis, fieldsynopsis, variablelist, epigraph, itemizedlist, anchor, procedure)
glossdef.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, mediaobjectco, segmentedlist, informalequation, fieldsynopsis, informalexample, table, literallayout, glosslist, glossseealso, para, informaltable, simpara, formalpara, informalfigure, methodsynopsis, destructorsynopsis, screenco, constructorsynopsis, indexterm, calloutlist, blockquote, screenshot, screen, graphicco, address, orderedlist, beginpage, classsynopsis, remark, graphic, equation, example, synopsis, variablelist, simplelist, itemizedlist, programlistingco)
qandadiv.model = \
qandaset.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, informalequation, warning, caution, informalexample, table, blockinfo, glosslist, literallayout, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, indexterm, calloutlist, blockquote, screenshot, qandaentry, screen, graphicco, remark, important, para, address, orderedlist, classsynopsis, mediaobjectco, graphic, qandadiv, programlistingco, equation, tip, example, synopsis, fieldsynopsis, variablelist, simplelist, itemizedlist, anchor, procedure)
taskprerequisites.model = \
taskrelated.model = \
tasksummary.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, blockinfo, glosslist, literallayout, msgset, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, equation, authorblurb, example, synopsis, fieldsynopsis, variablelist, epigraph, itemizedlist, anchor, procedure)
procedure.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, blockinfo, glosslist, literallayout, msgset, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, remark, qandaset, simplelist, step, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, equation, authorblurb, example, synopsis, fieldsynopsis, variablelist, epigraph, itemizedlist, anchor, procedure)
sidebar.model = sims.Elements(programlisting, funcsynopsis, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, literallayout, glosslist, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, indexterm, calloutlist, blockquote, screenshot, screen, graphicco, remark, important, para, address, orderedlist, beginpage, classsynopsis, mediaobjectco, sidebarinfo, programlistingco, equation, graphic, example, synopsis, fieldsynopsis, variablelist, simplelist, itemizedlist, anchor, procedure)
variablelist.model = sims.Elements(programlisting, funcsynopsis, varlistentry, cmdsynopsis, abstract, titleabbrev, tip, informalequation, warning, caution, informalexample, blockinfo, literallayout, destructorsynopsis, title, highlights, bridgehead, simpara, formalpara, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, indexterm, mediaobject, blockquote, screenshot, screen, graphicco, remark, important, para, address, beginpage, classsynopsis, mediaobjectco, graphic, programlistingco, authorblurb, synopsis, fieldsynopsis, epigraph, anchor)
sect3.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, sect3info, informalequation, fieldsynopsis, funcsynopsis, literallayout, msgset, sect4, bibliography, title, highlights, formalpara, methodsynopsis, lot, toc, calloutlist, blockquote, para, remark, titleabbrev, orderedlist, classsynopsis, graphic, glossary, equation, epigraph, itemizedlist, anchor, procedure, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, index, sidebar, destructorsynopsis, authorblurb, bridgehead, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, beginpage, screenshot, screen, graphicco, refentry, important, address, qandaset, simplelist, mediaobjectco, task, programlistingco, example, synopsis, variablelist, simpara)
indexdiv.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, titleabbrev, formalpara, informalequation, fieldsynopsis, informalexample, funcsynopsis, literallayout, destructorsynopsis, title, screenshot, indexentry, simpara, segmentedlist, informalfigure, methodsynopsis, informaltable, screenco, constructorsynopsis, olink, blockquote, para, screen, graphicco, remark, ulink, address, orderedlist, beginpage, classsynopsis, mediaobjectco, graphic, programlistingco, synopsis, variablelist, simplelist, link, itemizedlist, anchor)
sect2.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, titleabbrev, informalequation, fieldsynopsis, funcsynopsis, literallayout, msgset, bibliography, sect3, title, highlights, formalpara, methodsynopsis, lot, toc, calloutlist, blockquote, para, remark, qandaset, orderedlist, classsynopsis, graphic, glossary, equation, epigraph, itemizedlist, anchor, procedure, sect2info, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, index, sidebar, destructorsynopsis, authorblurb, bridgehead, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, beginpage, screenshot, screen, graphicco, refentry, important, address, simplelist, mediaobjectco, task, programlistingco, example, synopsis, variablelist, simpara)
sect5.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, titleabbrev, informalequation, fieldsynopsis, funcsynopsis, literallayout, msgset, bibliography, title, highlights, formalpara, methodsynopsis, lot, sect5info, toc, calloutlist, blockquote, para, remark, qandaset, orderedlist, classsynopsis, graphic, glossary, equation, epigraph, itemizedlist, anchor, procedure, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, index, sidebar, destructorsynopsis, authorblurb, bridgehead, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, beginpage, screenshot, screen, graphicco, refentry, important, address, simplelist, mediaobjectco, task, programlistingco, example, synopsis, variablelist, simpara)
section.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, titleabbrev, informalequation, fieldsynopsis, funcsynopsis, literallayout, msgset, bibliography, title, highlights, formalpara, methodsynopsis, lot, toc, sectioninfo, calloutlist, blockquote, para, remark, qandaset, orderedlist, classsynopsis, graphic, glossary, equation, epigraph, itemizedlist, anchor, procedure, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, index, sidebar, destructorsynopsis, authorblurb, section, bridgehead, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, beginpage, screenshot, screen, graphicco, refentry, important, address, simplelist, mediaobjectco, task, programlistingco, example, synopsis, variablelist, simpara)
sect4.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, titleabbrev, informalequation, fieldsynopsis, funcsynopsis, literallayout, msgset, sect5, bibliography, title, highlights, formalpara, methodsynopsis, lot, toc, calloutlist, blockquote, para, remark, qandaset, orderedlist, classsynopsis, graphic, glossary, equation, epigraph, itemizedlist, anchor, procedure, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, index, sidebar, destructorsynopsis, authorblurb, bridgehead, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, beginpage, screenshot, screen, graphicco, refentry, important, address, simplelist, mediaobjectco, task, programlistingco, example, synopsis, variablelist, simpara, sect4info)
partintro.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, titleabbrev, informalequation, fieldsynopsis, funcsynopsis, literallayout, msgset, title, highlights, formalpara, methodsynopsis, calloutlist, blockquote, para, remark, qandaset, orderedlist, classsynopsis, graphic, equation, epigraph, itemizedlist, anchor, procedure, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, sidebar, destructorsynopsis, authorblurb, section, bridgehead, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, beginpage, screenshot, screen, graphicco, refentry, important, address, simplelist, mediaobjectco, task, programlistingco, sect1, example, synopsis, variablelist, simpara)
article.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, titleabbrev, informalequation, tocchap, funcsynopsis, literallayout, msgset, bibliography, title, highlights, formalpara, methodsynopsis, lot, toc, calloutlist, blockquote, para, remark, qandaset, appendix, orderedlist, classsynopsis, graphic, glossary, equation, fieldsynopsis, epigraph, itemizedlist, anchor, procedure, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, index, sidebar, destructorsynopsis, authorblurb, section, bridgehead, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, beginpage, screenshot, screen, graphicco, refentry, important, address, simplelist, mediaobjectco, task, ackno, programlistingco, sect1, articleinfo, example, synopsis, variablelist, simpara)
chapter.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, titleabbrev, informalequation, tocchap, funcsynopsis, literallayout, msgset, bibliography, title, highlights, formalpara, methodsynopsis, lot, toc, calloutlist, blockquote, para, remark, qandaset, orderedlist, classsynopsis, graphic, glossary, equation, fieldsynopsis, epigraph, itemizedlist, anchor, procedure, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, index, sidebar, destructorsynopsis, authorblurb, section, bridgehead, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, chapterinfo, graphicco, screenshot, screen, beginpage, refentry, important, address, simplelist, mediaobjectco, task, programlistingco, sect1, example, synopsis, variablelist, simpara)
appendix.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, titleabbrev, informalequation, tocchap, funcsynopsis, literallayout, msgset, bibliography, title, highlights, formalpara, methodsynopsis, lot, toc, calloutlist, blockquote, para, remark, qandaset, orderedlist, classsynopsis, graphic, glossary, equation, fieldsynopsis, epigraph, itemizedlist, anchor, procedure, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, index, sidebar, destructorsynopsis, authorblurb, section, bridgehead, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, graphicco, screenshot, screen, beginpage, refentry, important, address, simplelist, mediaobjectco, task, programlistingco, sect1, example, synopsis, variablelist, simpara, appendixinfo)
preface.model = sims.Elements(programlisting, subtitle, cmdsynopsis, mediaobject, titleabbrev, informalequation, tocchap, funcsynopsis, literallayout, msgset, bibliography, title, highlights, formalpara, methodsynopsis, lot, toc, calloutlist, blockquote, para, remark, qandaset, orderedlist, classsynopsis, graphic, glossary, equation, fieldsynopsis, epigraph, itemizedlist, anchor, procedure, simplesect, figure, abstract, warning, caution, informalexample, table, glosslist, index, sidebar, destructorsynopsis, authorblurb, section, bridgehead, tip, segmentedlist, informalfigure, note, informaltable, screenco, constructorsynopsis, indexterm, graphicco, screenshot, screen, beginpage, refentry, important, address, simplelist, mediaobjectco, task, programlistingco, sect1, example, synopsis, variablelist, simpara, prefaceinfo)
glossary.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, glossdiv, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, glossentry, msgset, bibliography, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, glossaryinfo, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, equation, authorblurb, example, synopsis, fieldsynopsis, variablelist, epigraph, itemizedlist, anchor, procedure)
refsection.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, equation, informalequation, warning, caution, informalexample, refsectioninfo, table, funcsynopsis, literallayout, glosslist, msgset, destructorsynopsis, title, highlights, bridgehead, tip, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, refsection, programlistingco, authorblurb, example, synopsis, fieldsynopsis, variablelist, simpara, epigraph, itemizedlist, anchor, procedure)
refsect1.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, equation, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, msgset, destructorsynopsis, title, highlights, bridgehead, tip, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, refsect2, blockquote, screenshot, screen, graphicco, remark, refsect1info, simplelist, important, para, address, qandaset, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, authorblurb, example, synopsis, fieldsynopsis, variablelist, simpara, epigraph, itemizedlist, anchor, procedure)
refsynopsisdiv.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, equation, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, msgset, destructorsynopsis, title, highlights, bridgehead, tip, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, refsynopsisdivinfo, constructorsynopsis, graphic, indexterm, abstract, calloutlist, refsect2, blockquote, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, authorblurb, example, synopsis, fieldsynopsis, variablelist, simpara, epigraph, itemizedlist, anchor, procedure)
refsect2.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, equation, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, note, msgset, destructorsynopsis, title, highlights, bridgehead, tip, segmentedlist, informalfigure, methodsynopsis, refsect2info, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, refsect3, mediaobjectco, task, programlistingco, authorblurb, example, synopsis, fieldsynopsis, variablelist, simpara, epigraph, itemizedlist, anchor, procedure)
bibliography.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, bibliodiv, msgset, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, bibliomixed, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, equation, authorblurb, bibliographyinfo, example, synopsis, fieldsynopsis, variablelist, epigraph, biblioentry, itemizedlist, anchor, procedure)
glossdiv.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, glossentry, msgset, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, equation, authorblurb, example, synopsis, fieldsynopsis, variablelist, epigraph, itemizedlist, anchor, procedure)
bibliodiv.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, msgset, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, bibliomixed, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, equation, authorblurb, example, synopsis, fieldsynopsis, variablelist, epigraph, biblioentry, itemizedlist, anchor, procedure)
simplesect.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, msgset, destructorsynopsis, title, highlights, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, equation, authorblurb, example, synopsis, fieldsynopsis, variablelist, epigraph, itemizedlist, anchor, procedure)
setindex.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, msgset, destructorsynopsis, title, highlights, indexentry, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, equation, authorblurb, setindexinfo, indexdiv, example, synopsis, fieldsynopsis, variablelist, epigraph, itemizedlist, anchor, procedure)
index.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, msgset, destructorsynopsis, title, highlights, indexentry, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, programlistingco, beginpage, classsynopsis, sidebar, mediaobjectco, task, indexinfo, equation, authorblurb, indexdiv, example, synopsis, fieldsynopsis, variablelist, epigraph, itemizedlist, anchor, procedure)
refsect3.model = sims.Elements(programlisting, subtitle, figure, cmdsynopsis, mediaobject, titleabbrev, formalpara, tip, informalequation, warning, caution, informalexample, table, funcsynopsis, literallayout, glosslist, msgset, destructorsynopsis, title, refsect3info, bridgehead, simpara, segmentedlist, informalfigure, methodsynopsis, note, informaltable, screenco, constructorsynopsis, graphic, indexterm, abstract, calloutlist, blockquote, screenshot, screen, graphicco, remark, qandaset, simplelist, important, para, address, orderedlist, beginpage, classsynopsis, sidebar, mediaobjectco, task, programlistingco, equation, authorblurb, example, synopsis, fieldsynopsis, variablelist, highlights, epigraph, itemizedlist, anchor, procedure)
publisher.model = sims.Elements(publishername, address)
reference.model = sims.Elements(refentry, referenceinfo, subtitle, partintro, title, beginpage, titleabbrev)
refnamediv.model = sims.Elements(remark, refpurpose, refname, ulink, refclass, link, olink, refdescriptor)
refentry.model = sims.Elements(remark, refsect1, refsection, refmeta, refnamediv, beginpage, refsynopsisdiv, ulink, link, refentryinfo, indexterm, olink)
revhistory.model = sims.Elements(revision)
revision.model = sims.Elements(revnumber, revdescription, author, date, revremark, authorinitials)
cmdsynopsis.model = sims.Elements(sbr, command, synopfragment, group, arg)
group.model = sims.Elements(sbr, group, option, synopfragmentref, arg, replaceable)
screenco.model = sims.Elements(screen, areaspec, calloutlist)
indexterm.model = sims.Elements(see, seealso, primary, tertiary, secondary)
seglistitem.model = sims.Elements(seg)
segmentedlist.model = sims.Elements(seglistitem, segtitle, titleabbrev, title)
printhistory.model = sims.Elements(simpara, formalpara, para)
abstract.model = \
authorblurb.model = \
personblurb.model = sims.Elements(simpara, formalpara, para, title)
epigraph.model = sims.Elements(simpara, literallayout, attribution, formalpara, para)
stepalternatives.model = \
substeps.model = sims.Elements(step)
subjectset.model = sims.Elements(subject)
subject.model = sims.Elements(subjectterm)
book.model = sims.Elements(subtitle, colophon, titleabbrev, bookinfo, appendix, preface, dedication, article, chapter, index, bibliography, reference, title, glossary, setindex, part, lot, toc)
part.model = sims.Elements(subtitle, reference, beginpage, titleabbrev, refentry, appendix, preface, article, chapter, index, partintro, bibliography, title, glossary, partinfo, lot, toc)
task.model = sims.Elements(taskprerequisites, taskrelated, example, title, blockinfo, indexterm, titleabbrev, procedure, tasksummary)
tr.model = sims.Elements(td, th)
varlistentry.model = sims.Elements(term, listitem)
indexentry.model = sims.Elements(tertiaryie, primaryie, secondaryie, seeie, seealsoie)
toc.model = sims.Elements(tocback, beginpage, subtitle, title, tocchap, tocpart, tocfront, titleabbrev)
toclevel5.model = sims.Elements(tocentry)
tocpart.model = sims.Elements(tocentry, tocchap)
tocchap.model = sims.Elements(tocentry, toclevel1)
toclevel1.model = sims.Elements(tocentry, toclevel2)
toclevel2.model = sims.Elements(tocentry, toclevel3)
toclevel3.model = sims.Elements(toclevel4, tocentry)
toclevel4.model = sims.Elements(toclevel5, tocentry)
tbody.model = sims.Elements(tr, row)
methodparam.model = sims.Elements(type, modifier, parameter, funcparams, initializer)
fieldsynopsis.model = sims.Elements(varname, modifier, type, initializer)
videoobject.model = sims.Elements(videodata, objectinfo)
refclass.model = sims.ElementsOrText(application)
classsynopsisinfo.model = \
funcsynopsisinfo.model = sims.ElementsOrText(code, constant, keycombo, menuchoice, guilabel, prompt, errorname, classname, returnvalue, guiicon, inlinegraphic, ooexception, option, guimenu, type, guisubmenu, userinput, errortext, filename, errorcode, application, literal, computeroutput, lineannotation, subscript, indexterm, parameter, keysym, olink, function, beginpage, sgmltag, interfacename, mousebutton, replaceable, envar, structname, action, exceptionname, ulink, oointerface, interface, systemitem, guimenuitem, optional, keycode, hardware, remark, methodname, anchor, database, keycap, markup, errortype, symbol, uri, email, textobject, inlinemediaobject, token, command, ooclass, varname, guibutton, link, property, medialabel, structfield, superscript)
systemitem.model = sims.ElementsOrText(code, constant, keycombo, menuchoice, guilabel, prompt, errorname, classname, returnvalue, guiicon, inlinegraphic, ooexception, option, guimenu, type, guisubmenu, userinput, errortext, filename, errorcode, application, literal, computeroutput, subscript, indexterm, parameter, keysym, olink, function, beginpage, sgmltag, interfacename, acronym, mousebutton, replaceable, envar, structname, action, exceptionname, ulink, oointerface, interface, systemitem, guimenuitem, optional, keycode, hardware, remark, methodname, anchor, co, database, keycap, markup, errortype, symbol, uri, email, inlinemediaobject, token, command, ooclass, varname, guibutton, link, property, medialabel, structfield, superscript)
computeroutput.model = \
userinput.model = sims.ElementsOrText(code, constant, keycombo, menuchoice, guilabel, prompt, errorname, classname, returnvalue, guiicon, inlinegraphic, ooexception, option, guimenu, type, guisubmenu, userinput, errortext, filename, errorcode, application, literal, computeroutput, subscript, indexterm, parameter, keysym, olink, function, beginpage, sgmltag, interfacename, mousebutton, replaceable, envar, structname, action, exceptionname, ulink, oointerface, interface, systemitem, guimenuitem, optional, keycode, hardware, remark, methodname, anchor, co, database, keycap, markup, errortype, symbol, uri, email, inlinemediaobject, token, command, ooclass, varname, guibutton, link, property, medialabel, structfield, superscript)
action.model = \
code.model = \
command.model = \
database.model = \
filename.model = \
funcparams.model = \
function.model = \
hardware.model = \
interfacename.model = \
keycap.model = \
literal.model = \
option.model = \
optional.model = \
parameter.model = \
property.model = sims.ElementsOrText(code, constant, keycombo, menuchoice, guilabel, prompt, errorname, classname, returnvalue, guiicon, inlinegraphic, ooexception, option, guimenu, type, guisubmenu, userinput, errortext, filename, errorcode, application, literal, computeroutput, subscript, indexterm, parameter, keysym, olink, function, beginpage, sgmltag, interfacename, mousebutton, replaceable, envar, structname, action, exceptionname, ulink, oointerface, interface, systemitem, guimenuitem, optional, keycode, hardware, remark, methodname, anchor, database, keycap, markup, errortype, symbol, uri, email, inlinemediaobject, token, command, ooclass, varname, guibutton, link, property, medialabel, structfield, superscript)
trademark.model = sims.ElementsOrText(code, constant, keycombo, menuchoice, guilabel, prompt, errorname, classname, returnvalue, guiicon, inlinegraphic, ooexception, option, guimenu, type, guisubmenu, userinput, errortext, filename, errorcode, application, literal, computeroutput, subscript, parameter, keysym, olink, emphasis, function, sgmltag, interfacename, mousebutton, replaceable, envar, structname, action, exceptionname, ulink, oointerface, interface, systemitem, guimenuitem, optional, keycode, hardware, remark, methodname, anchor, database, keycap, markup, errortype, symbol, uri, email, inlinemediaobject, token, command, ooclass, varname, guibutton, link, property, medialabel, structfield, superscript)
refdescriptor.model = \
refname.model = sims.ElementsOrText(code, constant, keycombo, menuchoice, guilabel, prompt, errorname, classname, returnvalue, guiicon, ooexception, option, guimenu, type, guisubmenu, userinput, errortext, filename, errorcode, application, literal, computeroutput, parameter, keysym, function, sgmltag, interfacename, mousebutton, replaceable, envar, structname, action, exceptionname, oointerface, interface, systemitem, guimenuitem, optional, keycode, hardware, methodname, database, keycap, markup, errortype, symbol, uri, email, token, command, ooclass, varname, guibutton, property, medialabel, structfield)
application.model = \
attribution.model = \
bibliomisc.model = \
citation.model = \
citetitle.model = \
emphasis.model = \
firstterm.model = \
foreignphrase.model = \
glosssee.model = \
glossseealso.model = \
glossterm.model = \
lineannotation.model = \
link.model = \
lotentry.model = \
member.model = \
msgaud.model = \
olink.model = \
phrase.model = \
productname.model = \
quote.model = \
refentrytitle.model = \
remark.model = \
screeninfo.model = \
seg.model = \
simpara.model = \
term.model = \
tocback.model = \
tocentry.model = \
tocfront.model = \
ulink.model = sims.ElementsOrText(code, funcsynopsis, keycombo, productnumber, trademark, classname, fieldsynopsis, citerefentry, prompt, inlinegraphic, foreignphrase, guimenu, personname, guisubmenu, authorinitials, userinput, errortext, methodsynopsis, literal, footnoteref, inlineequation, type, olink, function, option, mousebutton, productname, envar, othercredit, ulink, methodname, guimenuitem, classsynopsis, systemitem, structname, firstterm, inlinemediaobject, token, glossterm, modespec, property, medialabel, anchor, returnvalue, constant, menuchoice, footnote, guilabel, citation, errorname, hardware, guiicon, phrase, wordasword, corpauthor, ooexception, interfacename, keycap, xref, destructorsynopsis, author, orgname, synopsis, filename, errorcode, application, emphasis, constructorsynopsis, computeroutput, subscript, indexterm, parameter, email, beginpage, sgmltag, acronym, quote, symbol, replaceable, cmdsynopsis, corpcredit, citetitle, action, exceptionname, oointerface, revhistory, interface, optional, keycode, remark, database, varname, markup, errortype, uri, abbrev, command, ooclass, guibutton, link, keysym, structfield, superscript)
literallayout.model = \
programlisting.model = \
screen.model = sims.ElementsOrText(code, funcsynopsis, keycombo, productnumber, trademark, classname, fieldsynopsis, citerefentry, prompt, inlinegraphic, foreignphrase, lineannotation, guimenu, personname, guisubmenu, authorinitials, userinput, errortext, methodsynopsis, literal, footnoteref, inlineequation, type, olink, function, option, mousebutton, productname, envar, othercredit, ulink, methodname, guimenuitem, classsynopsis, systemitem, co, structname, firstterm, inlinemediaobject, token, glossterm, modespec, property, medialabel, anchor, returnvalue, constant, menuchoice, footnote, guilabel, citation, errorname, hardware, guiicon, phrase, wordasword, corpauthor, ooexception, interfacename, keycap, xref, destructorsynopsis, author, orgname, synopsis, filename, errorcode, application, emphasis, constructorsynopsis, computeroutput, subscript, indexterm, parameter, email, beginpage, sgmltag, acronym, quote, symbol, replaceable, cmdsynopsis, corpcredit, citetitle, action, exceptionname, oointerface, revhistory, interface, optional, keycode, remark, database, varname, markup, errortype, coref, uri, textobject, abbrev, command, ooclass, guibutton, link, keysym, structfield, superscript)
synopsis.model = sims.ElementsOrText(code, funcsynopsis, keycombo, productnumber, trademark, mediaobject, classname, fieldsynopsis, citerefentry, prompt, inlinegraphic, foreignphrase, lineannotation, guimenu, personname, guisubmenu, authorinitials, userinput, errortext, methodsynopsis, literal, footnoteref, inlineequation, type, olink, function, option, mousebutton, productname, envar, othercredit, ulink, methodname, guimenuitem, classsynopsis, graphic, systemitem, co, structname, firstterm, inlinemediaobject, token, glossterm, modespec, property, medialabel, anchor, returnvalue, constant, menuchoice, footnote, guilabel, citation, errorname, hardware, guiicon, phrase, wordasword, corpauthor, ooexception, interfacename, keycap, xref, destructorsynopsis, author, orgname, synopsis, filename, errorcode, application, emphasis, constructorsynopsis, computeroutput, subscript, indexterm, parameter, email, beginpage, sgmltag, acronym, quote, symbol, replaceable, cmdsynopsis, corpcredit, citetitle, action, exceptionname, oointerface, revhistory, interface, optional, keycode, remark, database, varname, markup, errortype, coref, uri, textobject, abbrev, command, ooclass, guibutton, link, keysym, structfield, superscript)
refpurpose.model = sims.ElementsOrText(code, keycombo, productnumber, trademark, classname, citerefentry, prompt, foreignphrase, guimenu, personname, guisubmenu, authorinitials, userinput, errortext, literal, footnoteref, type, olink, function, option, mousebutton, productname, envar, othercredit, ulink, methodname, guimenuitem, systemitem, structname, firstterm, token, glossterm, modespec, property, medialabel, anchor, returnvalue, constant, menuchoice, footnote, guilabel, citation, errorname, hardware, guiicon, phrase, wordasword, corpauthor, ooexception, interfacename, keycap, xref, author, orgname, filename, errorcode, application, emphasis, computeroutput, subscript, indexterm, parameter, email, beginpage, sgmltag, acronym, quote, symbol, replaceable, corpcredit, citetitle, action, exceptionname, oointerface, revhistory, interface, optional, keycode, remark, database, varname, markup, errortype, uri, abbrev, command, ooclass, guibutton, link, keysym, structfield, superscript)
bridgehead.model = \
segtitle.model = \
subtitle.model = \
title.model = \
titleabbrev.model = sims.ElementsOrText(code, keycombo, productnumber, trademark, classname, citerefentry, prompt, inlinegraphic, foreignphrase, guimenu, personname, guisubmenu, authorinitials, userinput, errortext, literal, footnoteref, inlineequation, type, olink, function, option, mousebutton, productname, envar, othercredit, ulink, methodname, guimenuitem, systemitem, structname, firstterm, inlinemediaobject, token, glossterm, modespec, property, medialabel, anchor, returnvalue, constant, menuchoice, footnote, guilabel, citation, errorname, hardware, guiicon, phrase, wordasword, corpauthor, ooexception, interfacename, keycap, xref, author, orgname, filename, errorcode, application, emphasis, computeroutput, subscript, indexterm, parameter, email, sgmltag, acronym, quote, symbol, replaceable, corpcredit, citetitle, action, exceptionname, oointerface, revhistory, interface, optional, keycode, remark, database, varname, markup, errortype, uri, abbrev, command, ooclass, guibutton, link, keysym, structfield, superscript)
primary.model = \
primaryie.model = \
secondary.model = \
secondaryie.model = \
see.model = \
seealso.model = \
seealsoie.model = \
seeie.model = \
tertiary.model = \
tertiaryie.model = sims.ElementsOrText(code, keycombo, productnumber, trademark, classname, citerefentry, prompt, inlinegraphic, foreignphrase, guimenu, personname, guisubmenu, authorinitials, userinput, errortext, literal, footnoteref, type, olink, function, option, mousebutton, productname, envar, othercredit, ulink, methodname, guimenuitem, systemitem, structname, firstterm, inlinemediaobject, token, glossterm, modespec, property, medialabel, anchor, returnvalue, constant, menuchoice, footnote, guilabel, citation, errorname, hardware, guiicon, phrase, wordasword, corpauthor, ooexception, interfacename, keycap, xref, author, orgname, filename, errorcode, application, emphasis, computeroutput, subscript, parameter, email, sgmltag, acronym, quote, symbol, replaceable, corpcredit, citetitle, action, exceptionname, oointerface, revhistory, interface, optional, keycode, remark, database, varname, markup, errortype, uri, abbrev, command, ooclass, guibutton, link, keysym, structfield, superscript)
bibliomixed.model = \
bibliomset.model = sims.ElementsOrText(contractsponsor, isbn, contractnum, pubdate, productnumber, abstract, address, invpartnumber, titleabbrev, printhistory, edition, releaseinfo, pubsnumber, contrib, seriesvolnums, corpauthor, bibliomset, authorgroup, artpagenums, author, orgname, volumenum, confgroup, authorinitials, pagenums, editor, bibliorelation, honorific, corpname, indexterm, othername, firstname, citebiblioid, issuenum, collab, othercredit, corpcredit, citetitle, biblioset, bibliomisc, date, surname, lineage, publisher, biblioid, publishername, copyright, subtitle, affiliation, bibliocoverage, issn, bibliosource, productname, authorblurb, personname, abbrev, title, revhistory)
funcdef.model = sims.ElementsOrText(function, replaceable, type)
prompt.model = sims.ElementsOrText(inlinemediaobject, indexterm, co, replaceable, inlinegraphic, beginpage)
guibutton.model = \
guiicon.model = \
guilabel.model = \
guimenu.model = \
guimenuitem.model = \
guisubmenu.model = \
interface.model = sims.ElementsOrText(inlinemediaobject, indexterm, replaceable, inlinegraphic, accel, beginpage)
accel.model = \
classname.model = \
constant.model = \
envar.model = \
errorcode.model = \
errorname.model = \
errortext.model = \
errortype.model = \
exceptionname.model = \
initializer.model = \
keycode.model = \
keysym.model = \
markup.model = \
medialabel.model = \
methodname.model = \
modifier.model = \
mousebutton.model = \
msglevel.model = \
msgorig.model = \
returnvalue.model = \
sgmltag.model = \
structfield.model = \
structname.model = \
symbol.model = \
token.model = \
type.model = \
uri.model = \
varname.model = sims.ElementsOrText(inlinemediaobject, indexterm, replaceable, inlinegraphic, beginpage)
address.model = sims.ElementsOrText(lineage, city, fax, surname, firstname, personname, country, othername, authorblurb, otheraddr, contrib, affiliation, state, street, postcode, honorific, pob, email, phone)
caption.model = sims.ElementsOrText(programlisting, blockquote, para, simpara, screen, formalpara, warning, caution, literallayout, glosslist, orderedlist, screenshot, programlistingco, tip, segmentedlist, note, screenco, important, variablelist, simplelist, itemizedlist, calloutlist)
para.model = sims.ElementsOrText(programlisting, code, funcsynopsis, keycombo, productnumber, trademark, mediaobject, address, mediaobjectco, segmentedlist, classname, informalequation, fieldsynopsis, citerefentry, screen, prompt, literallayout, inlinegraphic, foreignphrase, graphicco, note, guimenu, figure, personname, guisubmenu, authorinitials, userinput, errortext, methodsynopsis, literal, footnoteref, inlineequation, type, olink, calloutlist, function, blockquote, option, informaltable, mousebutton, productname, envar, othercredit, ulink, methodname, guimenuitem, orderedlist, programlistingco, classsynopsis, graphic, systemitem, structname, equation, firstterm, inlinemediaobject, token, glossterm, simplelist, modespec, property, medialabel, anchor, returnvalue, constant, menuchoice, footnote, guilabel, citation, table, errorname, hardware, warning, caution, informalexample, guiicon, phrase, wordasword, corpauthor, ooexception, interfacename, keycap, xref, destructorsynopsis, author, orgname, tip, synopsis, informalfigure, filename, errorcode, application, emphasis, constructorsynopsis, computeroutput, variablelist, subscript, indexterm, parameter, email, beginpage, sgmltag, screenshot, acronym, quote, symbol, replaceable, cmdsynopsis, corpcredit, citetitle, action, exceptionname, oointerface, revhistory, interface, optional, keycode, remark, itemizedlist, database, varname, markup, errortype, uri, example, glosslist, abbrev, important, command, ooclass, screenco, guibutton, link, keysym, structfield, superscript)
entry.model = \
td.model = \
th.model = sims.ElementsOrText(programlisting, code, funcsynopsis, keycombo, productnumber, trademark, mediaobject, segmentedlist, classname, fieldsynopsis, citerefentry, screen, prompt, literallayout, inlinegraphic, foreignphrase, formalpara, note, guimenu, personname, guisubmenu, authorinitials, userinput, errortext, methodsynopsis, literal, footnoteref, inlineequation, type, olink, calloutlist, function, option, para, mousebutton, productname, envar, othercredit, ulink, methodname, guimenuitem, orderedlist, programlistingco, classsynopsis, graphic, systemitem, structname, firstterm, inlinemediaobject, token, simpara, glossterm, simplelist, modespec, property, medialabel, anchor, returnvalue, constant, menuchoice, footnote, guilabel, citation, errorname, hardware, warning, caution, guiicon, phrase, wordasword, corpauthor, ooexception, interfacename, keycap, xref, destructorsynopsis, author, orgname, tip, synopsis, filename, errorcode, application, emphasis, constructorsynopsis, computeroutput, variablelist, subscript, indexterm, parameter, email, beginpage, sgmltag, screenshot, acronym, quote, symbol, replaceable, cmdsynopsis, corpcredit, citetitle, action, exceptionname, oointerface, revhistory, interface, optional, keycode, remark, itemizedlist, database, varname, markup, errortype, uri, glosslist, abbrev, important, command, ooclass, screenco, guibutton, link, keysym, structfield, superscript)
abbrev.model = \
acronym.model = \
label.model = \
manvolnum.model = \
wordasword.model = sims.ElementsOrText(remark, acronym, beginpage, trademark, inlinemediaobject, emphasis, link, ulink, subscript, indexterm, inlinegraphic, anchor, olink, superscript)
replaceable.model = sims.ElementsOrText(remark, co, optional, inlinemediaobject, ulink, link, subscript, inlinegraphic, anchor, olink, superscript)
ackno.model = \
artpagenums.model = \
authorinitials.model = \
bibliocoverage.model = \
biblioid.model = \
bibliorelation.model = \
bibliosource.model = \
citebiblioid.model = \
city.model = \
collabname.model = \
confdates.model = \
confnum.model = \
confsponsor.model = \
conftitle.model = \
contractnum.model = \
contractsponsor.model = \
contrib.model = \
corpauthor.model = \
corpcredit.model = \
corpname.model = \
country.model = \
date.model = \
edition.model = \
email.model = \
fax.model = \
firstname.model = \
holder.model = \
honorific.model = \
invpartnumber.model = \
isbn.model = \
issn.model = \
issuenum.model = \
jobtitle.model = \
lineage.model = \
modespec.model = \
orgdiv.model = \
orgname.model = \
otheraddr.model = \
othername.model = \
pagenums.model = \
phone.model = \
pob.model = \
postcode.model = \
productnumber.model = \
pubdate.model = \
publishername.model = \
pubsnumber.model = \
refmiscinfo.model = \
releaseinfo.model = \
revnumber.model = \
revremark.model = \
seriesvolnums.model = \
shortaffil.model = \
state.model = \
street.model = \
surname.model = \
volumenum.model = \
year.model = sims.ElementsOrText(remark, replaceable, trademark, inlinemediaobject, emphasis, ulink, link, subscript, indexterm, inlinegraphic, olink, superscript)
subscript.model = \
superscript.model = sims.ElementsOrText(remark, symbol, replaceable, inlinemediaobject, emphasis, ulink, link, subscript, inlinegraphic, anchor, olink, superscript)
arg.model = sims.ElementsOrText(sbr, replaceable, group, option, synopfragmentref, arg)
paramdef.model = sims.ElementsOrText(type, replaceable, parameter, funcparams, initializer)
anchor.model = \
area.model = \
audiodata.model = \
beginpage.model = \
co.model = \
col.model = \
colspec.model = \
coref.model = \
footnoteref.model = \
graphic.model = \
imagedata.model = \
inlinegraphic.model = \
sbr.model = \
spanspec.model = \
textdata.model = \
varargs.model = \
videodata.model = \
void.model = \
xref.model = sims.Empty()
alt.model = \
keyword.model = \
subjectterm.model = \
synopfragmentref.model = sims.NoElements()
