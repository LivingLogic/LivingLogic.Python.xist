#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>This module contains entities for many abbreviations and acronyms.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc
import doc


class base(xsc.Entity):
	"""
	The base of all entity classes. Used for dispatching the
	to conversion targets.
	"""
	register = False
	content = None
	title = None
	lang = None

	def convert(self, converter):
		node = doc.abbr(self.__class__.content, title=self.__class__.title, lang=self.__class__.lang)
		return node.convert(converter)

	def __unicode__(self):
		return unicode(self.content)


class rmi(base):
	content = "RMI"
	title = "Remote Method Invocation"
	lang = "en"



class jini(base):
	content = "JINI"
	title = "Java Intelligent Network Infrastructure"
	lang = "en"


class jfc(base):
	content = "JFC"
	title = "Java Foundation Classes"
	lang = "en"


class awt(base):
	content = "AWT"
	title = "Abstract Window Toolkit"
	lang = "en"


class jdbc(base):
	content = "JDBC"
	title = "Java Database Connectivity"
	lang = "en"


class jndi(base):
	content = "JNDI"
	title = "Java Naming and Directory Interface"
	lang = "en"


class jpda(base):
	content = "JPDA"
	title = "Java Platform Debugger Architecture"
	lang = "en"


class jvmpi(base):
	content = "JVMPI"
	title = "Java Virtual Machine Profiler Interface"
	lang = "en"


class jni(base):
	content = "JNI"
	title = "Java Native Interface"
	lang = "en"


class ejb(base):
	content = "EJB"
	title = "Enterprice Java Beans"
	lang = "en"


class jnlp(base):
	content = "JNLP"
	title = "Java Network Launch Protocol"
	lang = "en"


class jaoe(base):
	content = "JAOE"
	title = "Java Acronym Overflow Error"
	lang = "en"


class jgl(base):
	content = "JGL"
	title = "Java Generic Library"
	lang = "en"


class sgml(base):
	content = "SGML"
	title = "Standard Generalized Markup Language"
	lang = "en"


class html(base):
	content = "HTML"
	title = "Hypertext Markup Language"
	lang = "en"


class xhtml(base):
	content = "XHTML"


class xml(base):
	content = "XML"
	title = "Extensible Markup Language"
	lang = "en"


class css(base):
	content = "CSS"
	title = "Cascading Style Sheet"
	lang = "en"


class cgi(base):
	content = "CGI"
	title = "Common Gateway Interface"
	lang = "en"


class www(base):
	content = "WWW"
	title = "World Wide Web"
	lang = "en"


class pdf(base):
	content = "PDF"
	title = "Protable Document Format"
	lang = "en"


class url(base):
	content = "URL"
	title = "Uniform Resource Locator"
	lang = "en"


class http(base):
	content = "HTTP"
	title = "Hypertext Transfer Protocol"
	lang = "en"


class smtp(base):
	content = "SMTP"
	title = "Simple Mail Transfer Protocol"
	lang = "en"


class ftp(base):
	content = "FTP"
	title = "File Transfer Protocol"
	lang = "en"


class pop3(base):
	content = "POP3"
	title = "Post Office Protocol 3"
	lang = "en"


class cvs(base):
	content = "CVS"
	title = "Concurrent Versions System"
	lang = "en"


class faq(base):
	content = "FAQ"
	title = "Frequently Asked Question"
	lang = "en"


class gnu(base):
	content = "GNU"
	title = "GNU's Not UNIX"
	lang = "en"


class dns(base):
	content = "DNS"
	title = "Domain Name Service"
	lang = "en"


class ppp(base):
	content = "PPP"
	title = "Point To Point Protocol"
	lang = "en"


class isdn(base):
	content = "ISDN"
	title = "Integrated Services Digital Network"
	lang = "en"


class corba(base):
	content = "CORBA"
	title = "Common Object Request Broker Architecture"
	lang = "en"


class wap(base):
	content = "WAP"
	title = "Wireless Application Protocol"
	lang = "en"


class wml(base):
	content = "WML"
	title = "Wireless Markup Language"
	lang = "en"


class mac(base):
	content = "MAC"
	title = "Media Access Control"
	lang = "en"


class nat(base):
	content = "NAT"
	title = "Network Address Translation"
	lang = "en"


class sql(base):
	content = "SQL"
	title = "Structured Query Language"
	lang = "en"


class xsl(base):
	content = "XSL"
	title = "Extensible Stylesheet Language"
	lang = "en"


class xslt(base):
	content = "XSLT"
	title = "Extensible Stylesheet Language For Transformations"
	lang = "en"


class smil(base):
	content = "SMIL"
	title = "Synchronized Multimedia Integration Language"
	lang = "en"


class dtd(base):
	content = "DTD"
	title = "Document Type Definiton"
	lang = "en"


class dom(base):
	content = "DOM"
	title = "Document Object Model"
	lang = "en"


class api(base):
	content = "API"
	title = "Application Programming Interface"
	lang = "en"


class sax(base):
	content = "SAX"
	title = ("Simple ", api(), " for ", xml())
	lang = "en"


class dbms(base):
	content = "DBMS"
	title = "Database Management System"
	lang = "en"


class ansi(base):
	content = "ANSI"
	title = "American National Standards Institute"
	lang = "en"


class jsp(base):
	content = "JSP"
	title = "Java Server Pages"
	lang = "en"


class ascii(base):
	content = "ASCII"
	title = "American Standard Code for Information Interchange"
	lang = "en"


class sms(base):
	content = "SMS"
	title = "Small Message Service"
	lang = "en"


class p2p(base):
	content = "P2P"
	title = "Peer To Peer"
	lang = "en"


class gif(base):
	content = "GIF"
	title = "Graphics Interchange Format"
	lang = "en"


class png(base):
	content = "PNG"
	title = "Portable Network Graphics"
	lang = "en"


class uddi(base):
	content = "UDDI"
	title = "Universal Description, Discovery and Integration"
	lang = "en"


class wsdl(base):
	content = "WSDL"
	title = "Web Services Description Language"
	lang = "en"


class cdrom(base):
	content = "CDROM"


class snmp(base):
	content = "SNMP"
	title = "Simple Network Management Protocol"
	lang = "en"


class ssl(base):
	content = "SSL"
	title = "Secure Socket Layer"
	lang = "en"


class vrml(base):
	content = "VRML"
	title = "Virtual Reality Modelling Language"
	lang = "en"


class tco(base):
	content = "TCO"
	title = "Total Cost of Ownership"
	lang = "en"


class crm(base):
	content = "CRM"
	title = "Customer Relationship Management"
	lang = "en"


class cms(base):
	content = "CMS"
	title = "Content Management System"
	lang = "en"


class bnf(base):
	content = "BNF"
	title = "Backus Naur Form"
	lang = "en"


class mime(base):
	content = "MIME"
	title = "Multipurpose Internet Mail Extensions"
	lang = "en"


class wysiwyg(base):
	content = "WYSIWYG"
	title = "What You See Is What You Get"
	lang = "en"


class hsc(base):
	content = "HSC"


class xist(base):
	content = "XIST"


class xist4c(base):
	content = "XIST4C"


class php(base):
	content = "PHP"


class svg(base):
	content = "SVG"
	title = "Scalable Vector Graphics"
	lang = "en"


class utc(base):
	content = "UTC"
	title = "Coordinated Universal Time"
	lang = "en"


class xmlns(xsc.Namespace):
	xmlname = "abbr"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/abbr"
xmlns.makemod(vars())

