#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

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
<par>This module contains entities for many abbreviations and acronyms.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc
import html as html_
import docbook

class base(xsc.Entity):
	"""
	The base of all entity classes. Used for dispatching the
	to conversion targets.
	"""
	register = False

	def convert(self, converter):
		target = converter.target
		if issubclass(target, docbook):
			e = self.convert_docbook(converter)
		elif issubclass(target, html_):
			e = self.convert_html(converter)
		else:
			raise ValueError("unknown conversion target %r" % target)
		return e.convert(converter)

class rmi(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("RMI", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("RMI", title="Remote Method Invocation", lang="en")
	def __unicode__(self):
		return u"RMI"

class jini(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JINI", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JINI", title="Java Intelligent Network Infrastructure", lang="en")
	def __unicode__(self):
		return u"JINI"

class jfc(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JFC", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JFC", title="Java Foundation Classes", lang="en")
	def __unicode__(self):
		return u"JFC"

class awt(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("AWT", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("AWT", title="Abstract Window Toolkit", lang="en")
	def __unicode__(self):
		return u"AWT"

class jdbc(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JDBC", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JDBC", title="Java Database Connectivity", lang="en")
	def __unicode__(self):
		return u"JDBC"

class jndi(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JNDI", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JNDI", title="Java Naming and Directory Interface", lang="en")
	def __unicode__(self):
		return u"JNDI"

class jpda(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JPDA", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JPDA", title="Java Platform Debugger Architecture", lang="en")
	def __unicode__(self):
		return u"JPDA"

class jvmpi(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JVMPI", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JVMPI", title="Java Virtual Machine Profiler Interface", lang="en")
	def __unicode__(self):
		return u"JVMPI"

class jni(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JNI", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JNI", title="Java Native Interface", lang="en")
	def __unicode__(self):
		return u"JNI"

class ejb(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("EJB", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("EJB", title="Enterprice Java Beans", lang="en")
	def __unicode__(self):
		return u"EJB"

class jnlp(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JNLP", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JNLP", title="Java Network Launch Protocol", lang="en")
	def __unicode__(self):
		return u"JNLP"

class jaoe(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JAOE", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JAOE", title="Java Acronym Overflow Error", lang="en")
	def __unicode__(self):
		return u"jaoe"

class jgl(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JGL", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JGL", title="Java Generic Library", lang="en")
	def __unicode__(self):
		return u"JGL"

class sgml(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("SGML", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("SGML", title="Standard Generalized Markup Language", lang="en")
	def __unicode__(self):
		return u"SGML"

class html(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("HTML", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("HTML", title="Hypertext Markup Language", lang="en")
	def __unicode__(self):
		return u"HTML"

class xhtml(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("XHTML", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("XHTML")
	def __unicode__(self):
		return u"XHTML"

class xml(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("XML", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("XML", title="Extensible Markup Language", lang="en")
	def __unicode__(self):
		return u"XML"

class css(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("CSS", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("CSS", title="Cascading Style Sheet", lang="en")
	def __unicode__(self):
		return u"CSS"

class cgi(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("CGI", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("CGI", title="Common Gateway Interface", lang="en")
	def __unicode__(self):
		return u"CGI"

class www(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("WWW", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("WWW", title="World Wide Web", lang="en")
	def __unicode__(self):
		return u"WWW"

class pdf(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("PDF", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("PDF", title="Protable Document Format", lang="en")
	def __unicode__(self):
		return u"PDF"

class url(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("URL", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("URL", title="Uniform Resource Locator", lang="en")
	def __unicode__(self):
		return u"URL"

class http(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("HTTP", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("HTTP", title="Hypertext Transfer Protocol", lang="en")
	def __unicode__(self):
		return u"HTTP"

class smtp(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("SMTP", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("SMTP", title="Simple Mail Transfer Protocol", lang="en")
	def __unicode__(self):
		return u"SMTP"

class ftp(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("FTP", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("FTP", title="File Transfer Protocol", lang="en")
	def __unicode__(self):
		return u"FTP"

class pop3(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("POP3", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("POP3", title="Post Office Protocol 3", lang="en")
	def __unicode__(self):
		return u"POP3"

class cvs(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("CVS", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("CVS", title="Concurrent Versions System", lang="en")
	def __unicode__(self):
		return u"CVS"

class faq(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("FAQ", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("FAQ", title="Frequently Asked Question", lang="en")
	def __unicode__(self):
		return u"FAQ"

class gnu(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("GNU", lang="en")
	def convert_html(self, converter):
			# we could do it ;): return html_.abbr("GNU", title=(self, "'s Not UNIX"), lang="en")
		return converter.target.abbr("GNU", title="GNU's Not UNIX", lang="en")
	def __unicode__(self):
		return u"GNU"

class dns(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("DNS", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("DNS", title="Domain Name Service", lang="en")
	def __unicode__(self):
		return u"DNS"

class ppp(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("PPP", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("PPP", title="Point To Point Protocol", lang="en")
	def __unicode__(self):
		return u"PPP"

class isdn(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("ISDN", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("ISDN", title="Integrated Services Digital Network", lang="en")
	def __unicode__(self):
		return u"ISDN"

class corba(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("CORBA", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("CORBA", title="Common Object Request Broker Architecture", lang="en")
	def __unicode__(self):
		return u"CORBA"

class wap(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("WAP", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("WAP", title="Wireless Application Protocol", lang="en")
	def __unicode__(self):
		return u"WAP"

class wml(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("WML", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("WML", title="Wireless Markup Language", lang="en")
	def __unicode__(self):
		return u"WML"

class mac(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("MAC", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("MAC", title="Media Access Control", lang="en")
	def __unicode__(self):
		return u"MAC"

class nat(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("NAT", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("NAT", title="Network Address Translation", lang="en")
	def __unicode__(self):
		return u"NAT"

class sql(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("SQL", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("SQL", title="Structured Query Language", lang="en")
	def __unicode__(self):
		return u"SQL"

class xsl(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("XSL", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("XSL", title="Extensible Stylesheet Language", lang="en")
	def __unicode__(self):
		return u"XSL"

class xslt(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("XSLT", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("XSLT", title="Extensible Stylesheet Language For Transformations", lang="en")
	def __unicode__(self):
		return u"XSLT"

class smil(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("SMIL", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("SMIL", title="Synchronized Multimedia Integration Language", lang="en")
	def __unicode__(self):
		return u"SMIL"

class dtd(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("DTD", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("DTD", title="Document Type Definiton", lang="en")
	def __unicode__(self):
		return u"DTD"

class dom(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("DOM", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("DOM", title="Document Object Model", lang="en")
	def __unicode__(self):
		return u"DOM"

class api(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("API", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("API", title="Application Programming Interface", lang="en")
	def __unicode__(self):
		return u"API"

class sax(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("SAX", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("SAX", title=("Simple ", self.xmlns.api(), " for ", self.xmlns.xml()), lang="en").convert(converter)
	def __unicode__(self):
		return u"SAX"

class dbms(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("DBMS", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("DBMS", title="Database Management System", lang="en")
	def __unicode__(self):
		return u"DBMS"

class ansi(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("ANSI", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("ANSI", title="American National Standards Institute", lang="en")
	def __unicode__(self):
		return u"ANSI"

class jsp(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("JSP", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("JSP", title="Java Server Pages", lang="en")
	def __unicode__(self):
		return u"JSP"

class ascii(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("ASCII", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("ASCII", title="American Standard Code for Information Interchange", lang="en")
	def __unicode__(self):
		return u"ASCII"

class sms(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("SMS", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("SMS", title="Small Message Service", lang="en")
	def __unicode__(self):
		return u"SMS"

class p2p(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("P2P", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("P2P", title="Peer To Peer", lang="en")
	def __unicode__(self):
		return u"P2P"

class gif(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("GIF", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("GIF", title="Graphics Interchange Format", lang="en")
	def __unicode__(self):
		return u"GIF"

class png(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("PNG", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("PNG", title="Portable Network Graphics", lang="en")
	def __unicode__(self):
		return u"PNG"

class uddi(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("UDDI", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("UDDI", title="Universal Description, Discovery and Integration", lang="en")
	def __unicode__(self):
		return u"UDDI"

class wsdl(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("WSDL", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("WSDL", title="Web Services Description Language", lang="en")
	def __unicode__(self):
		return u"WSDL"

class cdrom(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("CDROM", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("CDROM")
	def __unicode__(self):
		return u"CDROM"

class snmp(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("SNMP", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("SNMP", title="Simple Network Management Protocol", lang="en")
	def __unicode__(self):
		return u"SNMP"

class ssl(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("SSL", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("SSL", title="Secure Socket Layer", lang="en")
	def __unicode__(self):
		return u"SSL"

class vrml(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("VRML", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("VRML", title="Virtual Reality Modelling Language", lang="en")
	def __unicode__(self):
		return u"VRML"

class tco(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("TCO", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("TCO", title="Total Cost of Ownership", lang="en")
	def __unicode__(self):
		return u"TCO"

class crm(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("CRM", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("CRM", title="Customer Relationship Management", lang="en")
	def __unicode__(self):
		return u"CRM"

class cms(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("CMS", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("CMS", title="Content Management System", lang="en")
	def __unicode__(self):
		return u"CMS"

class bnf(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("BNF", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("BNF", title="Backus Naur Form", lang="en")
	def __unicode__(self):
		return u"BNF"

class mime(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("MIME", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("MIME", title="Multipurpose Internet Mail Extensions", lang="en")
	def __unicode__(self):
		return u"MIME"

class wysiwyg(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("WYSIWYG", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("WYSIWYG", title="What You See Is What You Get", lang="en")
	def __unicode__(self):
		return u"WYSIWYG"

class hsc(base):
	def convert(self, converter):
		return xsc.Text("HSC")
	def __unicode__(self):
		return u"HSC"

class xist(base):
	def convert(self, converter):
		return xsc.Text("XIST")
	def __unicode__(self):
		return u"XIST"

class xist4c(base):
	def convert(self, converter):
		return xsc.Text("XIST4C")
	def __unicode__(self):
		return u"XIST4C"

class php(base):
	def convert(self, converter):
		return xsc.Text("PHP")
	def __unicode__(self):
		return u"PHP"

class svg(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("SVG", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("SVG", title="Scalable Vector Graphics", lang="en")
	def __unicode__(self):
		return u"SVG"

class utc(base):
	def convert_docbook(self, converter):
		return converter.target.abbrev("UTC", lang="en")
	def convert_html(self, converter):
		return converter.target.abbr("UTC", title="Coordinated Universal Time", lang="en")
	def __unicode__(self):
		return u"UTC"

class xmlns(xsc.Namespace):
	xmlname = "abbr"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/abbr"
xmlns.makemod(vars())

