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
<doc:par>This module contains entities for many abbreviations and acronyms.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc
import html as html_

class rmi(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("RMI", title="Remote Method Invocation", lang="en")
	def __unicode__(self):
		return u"RMI"

class jini(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JINI", title="Java Intelligent Network Infrastructure", lang="en")
	def __unicode__(self):
		return u"JINI"

class jfc(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JFC", title="Java Foundation Classes", lang="en")
	def __unicode__(self):
		return u"JFC"

class awt(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("AWT", title="Abstract Window Toolkit", lang="en")
	def __unicode__(self):
		return u"AWT"

class jdbc(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JDBC", title="Java Database Connectivity", lang="en")
	def __unicode__(self):
		return u"JDBC"

class jndi(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JNDI", title="Java Naming and Directory Interface", lang="en")
	def __unicode__(self):
		return u"JNDI"

class jpda(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JPDA", title="Java Platform Debugger Architecture", lang="en")
	def __unicode__(self):
		return u"JPDA"

class jvmpi(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JVMPI", title="Java Virtual Machine Profiler Interface", lang="en")
	def __unicode__(self):
		return u"JVMPI"

class jni(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JNI", title="Java Native Interface", lang="en")
	def __unicode__(self):
		return u"JNI"

class ejb(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("EJB", title="Enterprice Java Beans", lang="en")
	def __unicode__(self):
		return u"EJB"

class jnlp(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JNLP", title="Java Network Launch Protocol", lang="en")
	def __unicode__(self):
		return u"JNLP"

class jaoe(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JAOE", title="Java Acronym Overflow Error", lang="en")
	def __unicode__(self):
		return u"jaoe"

class jgl(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JGL", title="Java Generic Library", lang="en")
	def __unicode__(self):
		return u"JGL"

class sgml(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("SGML", title="Standard Generalized Markup Language", lang="en")
	def __unicode__(self):
		return u"SGML"

class html(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("HTML", title="Hypertext Markup Language", lang="en")
	def __unicode__(self):
		return u"HTML"

class xhtml(xsc.Entity):
	def convert(self, converter):
		return xsc.Text("XHTML")
	def __unicode__(self):
		return u"XHTML"

class xml(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("XML", title="Extensible Markup Language", lang="en")
	def __unicode__(self):
		return u"XML"

class css(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("CSS", title="Cascading Style Sheet", lang="en")
	def __unicode__(self):
		return u"CSS"

class cgi(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("CGI", title="Common Gateway Interface", lang="en")
	def __unicode__(self):
		return u"CGI"

class www(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("WWW", title="World Wide Web", lang="en")
	def __unicode__(self):
		return u"WWW"

class pdf(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("PDF", title="Protable Document Format", lang="en")
	def __unicode__(self):
		return u"PDF"

class url(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("URL", title="Uniform Resource Locator", lang="en")
	def __unicode__(self):
		return u"URL"

class http(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("HTTP", title="Hypertext Transfer Protocol", lang="en")
	def __unicode__(self):
		return u"HTTP"

class smtp(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("SMTP", title="Simple Mail Transfer Protocol", lang="en")
	def __unicode__(self):
		return u"SMTP"

class ftp(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("FTP", title="File Transfer Protocol", lang="en")
	def __unicode__(self):
		return u"FTP"

class pop3(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("POP3", title="Post Office Protocol 3", lang="en")
	def __unicode__(self):
		return u"POP3"

class cvs(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("CVS", title="Concurrent Versions System", lang="en")
	def __unicode__(self):
		return u"CVS"

class faq(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("FAQ", title="Frequently Asked Question", lang="en")
	def __unicode__(self):
		return u"FAQ"

class gnu(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("GNU", title="GNU's Not UNIX", lang="en")
		# we could do it ;): return html_.abbr("GNU", title=(self, "'s Not UNIX"), lang="en")
	def __unicode__(self):
		return u"GNU"

class dns(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("DNS", title="Domain Name Service", lang="en")
	def __unicode__(self):
		return u"DNS"

class ppp(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("PPP", title="Domain Name Service", lang="en")
	def __unicode__(self):
		return u"PPP"

class isdn(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("ISDN", title="Integrated Services Digital Network", lang="en")
	def __unicode__(self):
		return u"ISDN"

class corba(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("CORBA", title="Common Object Request Broker Architecture", lang="en"), class_="caps")
	def __unicode__(self):
		return u"CORBA"

class wap(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("WAP", title="Wireless Application Protocol", lang="en"), class_="caps")
	def __unicode__(self):
		return u"WAP"

class wml(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("WML", title="Wireless Markup Language", lang="en"), class_="caps")
	def __unicode__(self):
		return u"WML"

class mac(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("MAC", title="Media Access Control", lang="en"), class_="caps")
	def __unicode__(self):
		return u"MAC"

class nat(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("NAT", title="Network Address Translation", lang="en"), class_="caps")
	def __unicode__(self):
		return u"NAT"

class sql(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("SQL", title="Structured Query Language", lang="en"), class_="caps")
	def __unicode__(self):
		return u"SQL"

class xsl(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("XSL", title="Extensible Stylesheet Language", lang="en"), class_="caps")
	def __unicode__(self):
		return u"XSL"

class xslt(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("XSLT", title="Extensible Stylesheet Language Transformations", lang="en"), class_="caps")
	def __unicode__(self):
		return u"XSLT"

class smil(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("SMIL", title="Synchronized Multimedia Integration Language", lang="en"), class_="caps")
	def __unicode__(self):
		return u"SMIL"

class dtd(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("DTD", title="Document Type Definiton", lang="en"), class_="caps")
	def __unicode__(self):
		return u"DTD"

class dom(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("DOM", title="Document Object Model", lang="en"), class_="caps")
	def __unicode__(self):
		return u"DOM"

class api(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("API", title="Application Programming Interface", lang="en"), class_="caps")
	def __unicode__(self):
		return u"API"

class sax(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("SAX", title="Simple API for XML", lang="en"), class_="caps")
	def __unicode__(self):
		return u"SAX"

class dbms(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("DBMS", title="Database Management System", lang="en"), class_="caps")
	def __unicode__(self):
		return u"DBMS"

class ansi(xsc.Entity):
	def convert(self, converter):
		return html_.span(html_.abbr("ANSI", title="American National Standards Institute", lang="en"), class_="caps")
	def __unicode__(self):
		return u"ANSI"

class jsp(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("JSP", title="Java Server Pages", lang="en")
	def __unicode__(self):
		return u"JSP"

class ascii(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("ASCII", title="American Standard Code for Information Interchange", lang="en")
	def __unicode__(self):
		return u"ASCII"

class dtd(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("DTD", title="Document Type Definition", lang="en")
	def __unicode__(self):
		return u"DTD"

class ftp(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("FTP", title="File Transfer Protocol", lang="en")
	def __unicode__(self):
		return u"FTP"

class sms(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("SMS", title="Small Message Service", lang="en")
	def __unicode__(self):
		return u"SMS"

class p2p(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("P2P", title="Peer To Peer", lang="en")
	def __unicode__(self):
		return u"P2P"

class gif(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("GIF", title="Graphics Interchange Format", lang="en")
	def __unicode__(self):
		return u"GIF"

class png(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("PNG", title="Portable Network Graphics", lang="en")
	def __unicode__(self):
		return u"PNG"

class uddi(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("UDDI", title="Universal Description, Discovery and Integration", lang="en")
	def __unicode__(self):
		return u"UDDI"

class wsdl(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("WSDL", title="Web Services Description Language", lang="en")
	def __unicode__(self):
		return u"WSDL"

class cdrom(xsc.Entity):
	def convert(self, converter):
		return xsc.Text("CDROM")
	def __unicode__(self):
		return u"CDROM"

class snmp(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("SNMP", title="Simple Network Management Protocol", lang="en")
	def __unicode__(self):
		return u"SNMP"

class ssl(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("SSL", title="Secure Socket Layer", lang="en")
	def __unicode__(self):
		return u"SSL"

class vrml(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("VRML", title="Virtual Reality Modelling Language", lang="en")
	def __unicode__(self):
		return u"VRML"

class tco(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("TCO", title="Total Cost of Ownership", lang="en")
	def __unicode__(self):
		return u"TCO"

class crm(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("CRM", title="Customer Relationship Management", lang="en")
	def __unicode__(self):
		return u"CRM"

class cms(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("CMS", title="Content Management System", lang="en")
	def __unicode__(self):
		return u"CMS"

class sms(xsc.Entity):
	def convert(self, converter):
		return html_.abbr("SMS", title="Short Message Service", lang="en")
	def __unicode__(self):
		return u"SMS"

namespace = xsc.Namespace("abbr", "http://xmlns.livinglogic.de/xist/abbr.dtd", vars())
