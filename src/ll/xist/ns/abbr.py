# -*- coding: utf-8 -*-

## Copyright 1999-2009 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2009 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
This module contains entities for many abbreviations and acronyms.
"""


from ll.xist import xsc
from ll.xist.ns import doc


__docformat__ = "reStructuredText"


xmlns = "http://xmlns.livinglogic.de/xist/ns/abbr"


class base(xsc.Entity):
	"""
	The base of all entity classes in this namespace.
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
	content = u"RMI"
	title = u"Remote Method Invocation"
	lang = u"en"


class jini(base):
	content = u"JINI"
	title = u"Java Intelligent Network Infrastructure"
	lang = u"en"


class jfc(base):
	content = u"JFC"
	title = u"Java Foundation Classes"
	lang = u"en"


class awt(base):
	content = u"AWT"
	title = u"Abstract Window Toolkit"
	lang = u"en"


class jdbc(base):
	content = u"JDBC"
	title = u"Java Database Connectivity"
	lang = u"en"


class jndi(base):
	content = u"JNDI"
	title = u"Java Naming and Directory Interface"
	lang = u"en"


class jpda(base):
	content = u"JPDA"
	title = u"Java Platform Debugger Architecture"
	lang = u"en"


class jvmpi(base):
	content = u"JVMPI"
	title = u"Java Virtual Machine Profiler Interface"
	lang = u"en"


class jni(base):
	content = u"JNI"
	title = u"Java Native Interface"
	lang = u"en"


class ejb(base):
	content = u"EJB"
	title = u"Enterprice Java Beans"
	lang = u"en"


class jnlp(base):
	content = u"JNLP"
	title = u"Java Network Launch Protocol"
	lang = u"en"


class jaoe(base):
	content = u"JAOE"
	title = u"Java Acronym Overflow Error"
	lang = u"en"


class jgl(base):
	content = u"JGL"
	title = u"Java Generic Library"
	lang = u"en"


class sgml(base):
	content = u"SGML"
	title = u"Standard Generalized Markup Language"
	lang = u"en"


class html(base):
	content = u"HTML"
	title = u"Hypertext Markup Language"
	lang = u"en"


class xhtml(base):
	content = u"XHTML"


class xml(base):
	content = u"XML"
	title = u"Extensible Markup Language"
	lang = u"en"


class css(base):
	content = u"CSS"
	title = u"Cascading Style Sheet"
	lang = u"en"


class cgi(base):
	content = u"CGI"
	title = u"Common Gateway Interface"
	lang = u"en"


class www(base):
	content = u"WWW"
	title = u"World Wide Web"
	lang = u"en"


class pdf(base):
	content = u"PDF"
	title = u"Protable Document Format"
	lang = u"en"


class url(base):
	content = u"URL"
	title = u"Uniform Resource Locator"
	lang = u"en"


class http(base):
	content = u"HTTP"
	title = u"Hypertext Transfer Protocol"
	lang = u"en"


class smtp(base):
	content = u"SMTP"
	title = u"Simple Mail Transfer Protocol"
	lang = u"en"


class ftp(base):
	content = u"FTP"
	title = u"File Transfer Protocol"
	lang = u"en"


class pop3(base):
	content = u"POP3"
	title = u"Post Office Protocol 3"
	lang = u"en"


class cvs(base):
	content = u"CVS"
	title = u"Concurrent Versions System"
	lang = u"en"


class faq(base):
	content = u"FAQ"
	title = u"Frequently Asked Question"
	lang = u"en"


class gnu(base):
	content = u"GNU"
	title = u"GNU's Not UNIX"
	lang = u"en"


class dns(base):
	content = u"DNS"
	title = u"Domain Name Service"
	lang = u"en"


class ppp(base):
	content = u"PPP"
	title = u"Point To Point Protocol"
	lang = u"en"


class isdn(base):
	content = u"ISDN"
	title = u"Integrated Services Digital Network"
	lang = u"en"


class corba(base):
	content = u"CORBA"
	title = u"Common Object Request Broker Architecture"
	lang = u"en"


class wap(base):
	content = u"WAP"
	title = u"Wireless Application Protocol"
	lang = u"en"


class wml(base):
	content = u"WML"
	title = u"Wireless Markup Language"
	lang = u"en"


class mac(base):
	content = u"MAC"
	title = u"Media Access Control"
	lang = u"en"


class nat(base):
	content = u"NAT"
	title = u"Network Address Translation"
	lang = u"en"


class sql(base):
	content = u"SQL"
	title = u"Structured Query Language"
	lang = u"en"


class xsl(base):
	content = u"XSL"
	title = u"Extensible Stylesheet Language"
	lang = u"en"


class xslt(base):
	content = u"XSLT"
	title = u"Extensible Stylesheet Language For Transformations"
	lang = u"en"


class smil(base):
	content = u"SMIL"
	title = u"Synchronized Multimedia Integration Language"
	lang = u"en"


class dtd(base):
	content = u"DTD"
	title = u"Document Type Definiton"
	lang = u"en"


class dom(base):
	content = u"DOM"
	title = u"Document Object Model"
	lang = u"en"


class api(base):
	content = u"API"
	title = u"Application Programming Interface"
	lang = u"en"


class sax(base):
	content = u"SAX"
	title = (u"Simple ", api(), u" for ", xml())
	lang = u"en"


class dbms(base):
	content = u"DBMS"
	title = u"Database Management System"
	lang = u"en"


class ansi(base):
	content = u"ANSI"
	title = u"American National Standards Institute"
	lang = u"en"


class jsp(base):
	content = u"JSP"
	title = u"Java Server Pages"
	lang = u"en"


class ascii(base):
	content = u"ASCII"
	title = u"American Standard Code for Information Interchange"
	lang = u"en"


class sms(base):
	content = u"SMS"
	title = u"Small Message Service"
	lang = u"en"


class p2p(base):
	content = u"P2P"
	title = u"Peer To Peer"
	lang = u"en"


class gif(base):
	content = u"GIF"
	title = u"Graphics Interchange Format"
	lang = u"en"


class png(base):
	content = u"PNG"
	title = u"Portable Network Graphics"
	lang = u"en"


class uddi(base):
	content = u"UDDI"
	title = u"Universal Description, Discovery and Integration"
	lang = u"en"


class wsdl(base):
	content = u"WSDL"
	title = u"Web Services Description Language"
	lang = u"en"


class cdrom(base):
	content = u"CDROM"


class snmp(base):
	content = u"SNMP"
	title = u"Simple Network Management Protocol"
	lang = u"en"


class ssl(base):
	content = u"SSL"
	title = u"Secure Socket Layer"
	lang = u"en"


class vrml(base):
	content = u"VRML"
	title = u"Virtual Reality Modelling Language"
	lang = u"en"


class tco(base):
	content = u"TCO"
	title = u"Total Cost of Ownership"
	lang = u"en"


class crm(base):
	content = u"CRM"
	title = u"Customer Relationship Management"
	lang = u"en"


class cms(base):
	content = u"CMS"
	title = u"Content Management System"
	lang = u"en"


class bnf(base):
	content = u"BNF"
	title = u"Backus Naur Form"
	lang = u"en"


class mime(base):
	content = u"MIME"
	title = u"Multipurpose Internet Mail Extensions"
	lang = u"en"


class wysiwyg(base):
	content = u"WYSIWYG"
	title = u"What You See Is What You Get"
	lang = u"en"


class hsc(base):
	content = u"HSC"


class xist(base):
	content = U"XIST"


class xist4c(base):
	content = u"XIST4C"


class php(base):
	content = u"PHP"


class svg(base):
	content = u"SVG"
	title = u"Scalable Vector Graphics"
	lang = u"en"


class utc(base):
	content = u"UTC"
	title = u"Coordinated Universal Time"
	lang = u"en"


class wsgi(base):
	content = u"WSGI"
	title = u"Web Server Gateway Interface"
	lang = u"en"
