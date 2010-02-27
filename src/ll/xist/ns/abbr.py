# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
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
	"""
	"Remote Method Invocation"
	"""
	content = u"RMI"
	title = u"Remote Method Invocation"
	lang = u"en"


class jini(base):
	"""
	"Java Intelligent Network Infrastructure"
	"""
	content = u"JINI"
	title = u"Java Intelligent Network Infrastructure"
	lang = u"en"


class jfc(base):
	"""
	"Java Foundation Classes"
	"""
	content = u"JFC"
	title = u"Java Foundation Classes"
	lang = u"en"


class awt(base):
	"""
	"Abstract Window Toolkit"
	"""
	content = u"AWT"
	title = u"Abstract Window Toolkit"
	lang = u"en"


class jdbc(base):
	"""
	"Java Database Connectivity"
	"""
	content = u"JDBC"
	title = u"Java Database Connectivity"
	lang = u"en"


class jndi(base):
	"""
	"Java Naming and Directory Interface"
	"""
	content = u"JNDI"
	title = u"Java Naming and Directory Interface"
	lang = u"en"


class jpda(base):
	"""
	"Java Platform Debugger Architecture"
	"""
	content = u"JPDA"
	title = u"Java Platform Debugger Architecture"
	lang = u"en"


class jvmpi(base):
	"""
	"Java Virtual Machine Profiler Interface"
	"""
	content = u"JVMPI"
	title = u"Java Virtual Machine Profiler Interface"
	lang = u"en"


class jni(base):
	"""
	"Java Native Interface"
	"""
	content = u"JNI"
	title = u"Java Native Interface"
	lang = u"en"


class ejb(base):
	"""
	"Enterprice Java Beans"
	"""
	content = u"EJB"
	title = u"Enterprice Java Beans"
	lang = u"en"


class jnlp(base):
	"""
	"Java Network Launch Protocol"
	"""
	content = u"JNLP"
	title = u"Java Network Launch Protocol"
	lang = u"en"


class jaoe(base):
	"""
	"Java Acronym Overflow Error"
	"""
	content = u"JAOE"
	title = u"Java Acronym Overflow Error"
	lang = u"en"


class jgl(base):
	"""
	"Java Generic Library"
	"""
	content = u"JGL"
	title = u"Java Generic Library"
	lang = u"en"


class sgml(base):
	"""
	"Standard Generalized Markup Language"
	"""
	content = u"SGML"
	title = u"Standard Generalized Markup Language"
	lang = u"en"


class html(base):
	"""
	"Hypertext Markup Language"
	"""
	content = u"HTML"
	title = u"Hypertext Markup Language"
	lang = u"en"


class xhtml(base):
	content = u"XHTML"


class xml(base):
	"""
	"Extensible Markup Language"
	"""
	content = u"XML"
	title = u"Extensible Markup Language"
	lang = u"en"


class css(base):
	"""
	"Cascading Style Sheet"
	"""
	content = u"CSS"
	title = u"Cascading Style Sheet"
	lang = u"en"


class cgi(base):
	"""
	"Common Gateway Interface"
	"""
	content = u"CGI"
	title = u"Common Gateway Interface"
	lang = u"en"


class www(base):
	"""
	"World Wide Web"
	"""
	content = u"WWW"
	title = u"World Wide Web"
	lang = u"en"


class pdf(base):
	"""
	"Protable Document Format"
	"""
	content = u"PDF"
	title = u"Protable Document Format"
	lang = u"en"


class url(base):
	"""
	"Uniform Resource Locator"
	"""
	content = u"URL"
	title = u"Uniform Resource Locator"
	lang = u"en"


class http(base):
	"""
	"Hypertext Transfer Protocol"
	"""
	content = u"HTTP"
	title = u"Hypertext Transfer Protocol"
	lang = u"en"


class smtp(base):
	"""
	"Simple Mail Transfer Protocol"
	"""
	content = u"SMTP"
	title = u"Simple Mail Transfer Protocol"
	lang = u"en"


class ftp(base):
	"""
	"File Transfer Protocol"
	"""
	content = u"FTP"
	title = u"File Transfer Protocol"
	lang = u"en"


class pop3(base):
	"""
	"Post Office Protocol 3"
	"""
	content = u"POP3"
	title = u"Post Office Protocol 3"
	lang = u"en"


class cvs(base):
	"""
	"Concurrent Versions System"
	"""
	content = u"CVS"
	title = u"Concurrent Versions System"
	lang = u"en"


class faq(base):
	"""
	"Frequently Asked Question"
	"""
	content = u"FAQ"
	title = u"Frequently Asked Question"
	lang = u"en"


class gnu(base):
	"""
	"GNU's Not UNIX"
	"""
	content = u"GNU"
	title = u"GNU's Not UNIX"
	lang = u"en"


class dns(base):
	"""
	"Domain Name Service"
	"""
	content = u"DNS"
	title = u"Domain Name Service"
	lang = u"en"


class ppp(base):
	"""
	"Point To Point Protocol"
	"""
	content = u"PPP"
	title = u"Point To Point Protocol"
	lang = u"en"


class isdn(base):
	"""
	"Integrated Services Digital Network"
	"""
	content = u"ISDN"
	title = u"Integrated Services Digital Network"
	lang = u"en"


class corba(base):
	"""
	"Common Object Request Broker Architecture"
	"""
	content = u"CORBA"
	title = u"Common Object Request Broker Architecture"
	lang = u"en"


class wap(base):
	"""
	"Wireless Application Protocol"
	"""
	content = u"WAP"
	title = u"Wireless Application Protocol"
	lang = u"en"


class wml(base):
	"""
	"Wireless Markup Language"
	"""
	content = u"WML"
	title = u"Wireless Markup Language"
	lang = u"en"


class mac(base):
	"""
	"Media Access Control"
	"""
	content = u"MAC"
	title = u"Media Access Control"
	lang = u"en"


class nat(base):
	"""
	"Network Address Translation"
	"""
	content = u"NAT"
	title = u"Network Address Translation"
	lang = u"en"


class sql(base):
	"""
	"Structured Query Language"
	"""
	content = u"SQL"
	title = u"Structured Query Language"
	lang = u"en"


class xsl(base):
	"""
	"Extensible Stylesheet Language"
	"""
	content = u"XSL"
	title = u"Extensible Stylesheet Language"
	lang = u"en"


class xslt(base):
	"""
	"Extensible Stylesheet Language For Transformations"
	"""
	content = u"XSLT"
	title = u"Extensible Stylesheet Language For Transformations"
	lang = u"en"


class smil(base):
	"""
	"Synchronized Multimedia Integration Language"
	"""
	content = u"SMIL"
	title = u"Synchronized Multimedia Integration Language"
	lang = u"en"


class dtd(base):
	"""
	"Document Type Definiton"
	"""
	content = u"DTD"
	title = u"Document Type Definiton"
	lang = u"en"


class dom(base):
	"""
	"Document Object Model"
	"""
	content = u"DOM"
	title = u"Document Object Model"
	lang = u"en"


class api(base):
	"""
	"Application Programming Interface"
	"""
	content = u"API"
	title = u"Application Programming Interface"
	lang = u"en"


class sax(base):
	"""
	"Simple API for XML"
	"""
	content = u"SAX"
	title = (u"Simple ", api(), u" for ", xml())
	lang = u"en"


class dbms(base):
	"""
	"Database Management System"
	"""
	content = u"DBMS"
	title = u"Database Management System"
	lang = u"en"


class ansi(base):
	"""
	"American National Standards Institute"
	"""
	content = u"ANSI"
	title = u"American National Standards Institute"
	lang = u"en"


class jsp(base):
	"""
	"Java Server Pages"
	"""
	content = u"JSP"
	title = u"Java Server Pages"
	lang = u"en"


class ascii(base):
	"""
	"American Standard Code for Information Interchange"
	"""
	content = u"ASCII"
	title = u"American Standard Code for Information Interchange"
	lang = u"en"


class sms(base):
	"""
	"Small Message Service"
	"""
	content = u"SMS"
	title = u"Small Message Service"
	lang = u"en"


class p2p(base):
	"""
	"Peer To Peer"
	"""
	content = u"P2P"
	title = u"Peer To Peer"
	lang = u"en"


class gif(base):
	"""
	"Graphics Interchange Format"
	"""
	content = u"GIF"
	title = u"Graphics Interchange Format"
	lang = u"en"


class png(base):
	"""
	"Portable Network Graphics"
	"""
	content = u"PNG"
	title = u"Portable Network Graphics"
	lang = u"en"


class uddi(base):
	"""
	"Universal Description, Discovery and Integration"
	"""
	content = u"UDDI"
	title = u"Universal Description, Discovery and Integration"
	lang = u"en"


class wsdl(base):
	"""
	"Web Services Description Language"
	"""
	content = u"WSDL"
	title = u"Web Services Description Language"
	lang = u"en"


class cdrom(base):
	content = u"CDROM"


class snmp(base):
	"""
	"Simple Network Management Protocol"
	"""
	content = u"SNMP"
	title = u"Simple Network Management Protocol"
	lang = u"en"


class ssl(base):
	"""
	"Secure Socket Layer"
	"""
	content = u"SSL"
	title = u"Secure Socket Layer"
	lang = u"en"


class vrml(base):
	"""
	"Virtual Reality Modelling Language"
	"""
	content = u"VRML"
	title = u"Virtual Reality Modelling Language"
	lang = u"en"


class tco(base):
	"""
	"Total Cost of Ownership"
	"""
	content = u"TCO"
	title = u"Total Cost of Ownership"
	lang = u"en"


class crm(base):
	"""
	"Customer Relationship Management"
	"""
	content = u"CRM"
	title = u"Customer Relationship Management"
	lang = u"en"


class cms(base):
	"""
	"Content Management System"
	"""
	content = u"CMS"
	title = u"Content Management System"
	lang = u"en"


class bnf(base):
	"""
	"Backus Naur Form"
	"""
	content = u"BNF"
	title = u"Backus Naur Form"
	lang = u"en"


class mime(base):
	"""
	"Multipurpose Internet Mail Extensions"
	"""
	content = u"MIME"
	title = u"Multipurpose Internet Mail Extensions"
	lang = u"en"


class wysiwyg(base):
	"""
	"What You See Is What You Get"
	"""
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
	"""
	"Scalable Vector Graphics"
	"""
	content = u"SVG"
	title = u"Scalable Vector Graphics"
	lang = u"en"


class utc(base):
	"""
	"Coordinated Universal Time"
	"""
	content = u"UTC"
	title = u"Coordinated Universal Time"
	lang = u"en"


class wsgi(base):
	"""
	"Web Server Gateway Interface"
	"""
	content = u"WSGI"
	title = u"Web Server Gateway Interface"
	lang = u"en"
