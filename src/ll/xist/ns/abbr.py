# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


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

	def __str__(self):
		return str(self.content)


class rmi(base):
	"""
	"Remote Method Invocation"
	"""
	content = "RMI"
	title = "Remote Method Invocation"
	lang = "en"


class jini(base):
	"""
	"Java Intelligent Network Infrastructure"
	"""
	content = "JINI"
	title = "Java Intelligent Network Infrastructure"
	lang = "en"


class jfc(base):
	"""
	"Java Foundation Classes"
	"""
	content = "JFC"
	title = "Java Foundation Classes"
	lang = "en"


class awt(base):
	"""
	"Abstract Window Toolkit"
	"""
	content = "AWT"
	title = "Abstract Window Toolkit"
	lang = "en"


class jdbc(base):
	"""
	"Java Database Connectivity"
	"""
	content = "JDBC"
	title = "Java Database Connectivity"
	lang = "en"


class jndi(base):
	"""
	"Java Naming and Directory Interface"
	"""
	content = "JNDI"
	title = "Java Naming and Directory Interface"
	lang = "en"


class jpda(base):
	"""
	"Java Platform Debugger Architecture"
	"""
	content = "JPDA"
	title = "Java Platform Debugger Architecture"
	lang = "en"


class jvmpi(base):
	"""
	"Java Virtual Machine Profiler Interface"
	"""
	content = "JVMPI"
	title = "Java Virtual Machine Profiler Interface"
	lang = "en"


class jni(base):
	"""
	"Java Native Interface"
	"""
	content = "JNI"
	title = "Java Native Interface"
	lang = "en"


class ejb(base):
	"""
	"Enterprice Java Beans"
	"""
	content = "EJB"
	title = "Enterprice Java Beans"
	lang = "en"


class jnlp(base):
	"""
	"Java Network Launch Protocol"
	"""
	content = "JNLP"
	title = "Java Network Launch Protocol"
	lang = "en"


class jaoe(base):
	"""
	"Java Acronym Overflow Error"
	"""
	content = "JAOE"
	title = "Java Acronym Overflow Error"
	lang = "en"


class jgl(base):
	"""
	"Java Generic Library"
	"""
	content = "JGL"
	title = "Java Generic Library"
	lang = "en"


class sgml(base):
	"""
	"Standard Generalized Markup Language"
	"""
	content = "SGML"
	title = "Standard Generalized Markup Language"
	lang = "en"


class html(base):
	"""
	"Hypertext Markup Language"
	"""
	content = "HTML"
	title = "Hypertext Markup Language"
	lang = "en"


class xhtml(base):
	content = "XHTML"


class xml(base):
	"""
	"Extensible Markup Language"
	"""
	content = "XML"
	title = "Extensible Markup Language"
	lang = "en"


class css(base):
	"""
	"Cascading Style Sheet"
	"""
	content = "CSS"
	title = "Cascading Style Sheet"
	lang = "en"


class cgi(base):
	"""
	"Common Gateway Interface"
	"""
	content = "CGI"
	title = "Common Gateway Interface"
	lang = "en"


class www(base):
	"""
	"World Wide Web"
	"""
	content = "WWW"
	title = "World Wide Web"
	lang = "en"


class pdf(base):
	"""
	"Protable Document Format"
	"""
	content = "PDF"
	title = "Protable Document Format"
	lang = "en"


class url(base):
	"""
	"Uniform Resource Locator"
	"""
	content = "URL"
	title = "Uniform Resource Locator"
	lang = "en"


class http(base):
	"""
	"Hypertext Transfer Protocol"
	"""
	content = "HTTP"
	title = "Hypertext Transfer Protocol"
	lang = "en"


class smtp(base):
	"""
	"Simple Mail Transfer Protocol"
	"""
	content = "SMTP"
	title = "Simple Mail Transfer Protocol"
	lang = "en"


class ftp(base):
	"""
	"File Transfer Protocol"
	"""
	content = "FTP"
	title = "File Transfer Protocol"
	lang = "en"


class pop3(base):
	"""
	"Post Office Protocol 3"
	"""
	content = "POP3"
	title = "Post Office Protocol 3"
	lang = "en"


class cvs(base):
	"""
	"Concurrent Versions System"
	"""
	content = "CVS"
	title = "Concurrent Versions System"
	lang = "en"


class faq(base):
	"""
	"Frequently Asked Question"
	"""
	content = "FAQ"
	title = "Frequently Asked Question"
	lang = "en"


class gnu(base):
	"""
	"GNU's Not UNIX"
	"""
	content = "GNU"
	title = "GNU's Not UNIX"
	lang = "en"


class dns(base):
	"""
	"Domain Name Service"
	"""
	content = "DNS"
	title = "Domain Name Service"
	lang = "en"


class ppp(base):
	"""
	"Point To Point Protocol"
	"""
	content = "PPP"
	title = "Point To Point Protocol"
	lang = "en"


class isdn(base):
	"""
	"Integrated Services Digital Network"
	"""
	content = "ISDN"
	title = "Integrated Services Digital Network"
	lang = "en"


class corba(base):
	"""
	"Common Object Request Broker Architecture"
	"""
	content = "CORBA"
	title = "Common Object Request Broker Architecture"
	lang = "en"


class wap(base):
	"""
	"Wireless Application Protocol"
	"""
	content = "WAP"
	title = "Wireless Application Protocol"
	lang = "en"


class wml(base):
	"""
	"Wireless Markup Language"
	"""
	content = "WML"
	title = "Wireless Markup Language"
	lang = "en"


class mac(base):
	"""
	"Media Access Control"
	"""
	content = "MAC"
	title = "Media Access Control"
	lang = "en"


class nat(base):
	"""
	"Network Address Translation"
	"""
	content = "NAT"
	title = "Network Address Translation"
	lang = "en"


class sql(base):
	"""
	"Structured Query Language"
	"""
	content = "SQL"
	title = "Structured Query Language"
	lang = "en"


class xsl(base):
	"""
	"Extensible Stylesheet Language"
	"""
	content = "XSL"
	title = "Extensible Stylesheet Language"
	lang = "en"


class xslt(base):
	"""
	"Extensible Stylesheet Language For Transformations"
	"""
	content = "XSLT"
	title = "Extensible Stylesheet Language For Transformations"
	lang = "en"


class smil(base):
	"""
	"Synchronized Multimedia Integration Language"
	"""
	content = "SMIL"
	title = "Synchronized Multimedia Integration Language"
	lang = "en"


class dtd(base):
	"""
	"Document Type Definiton"
	"""
	content = "DTD"
	title = "Document Type Definiton"
	lang = "en"


class dom(base):
	"""
	"Document Object Model"
	"""
	content = "DOM"
	title = "Document Object Model"
	lang = "en"


class api(base):
	"""
	"Application Programming Interface"
	"""
	content = "API"
	title = "Application Programming Interface"
	lang = "en"


class sax(base):
	"""
	"Simple API for XML"
	"""
	content = "SAX"
	title = ("Simple ", api(), " for ", xml())
	lang = "en"


class dbms(base):
	"""
	"Database Management System"
	"""
	content = "DBMS"
	title = "Database Management System"
	lang = "en"


class ansi(base):
	"""
	"American National Standards Institute"
	"""
	content = "ANSI"
	title = "American National Standards Institute"
	lang = "en"


class jsp(base):
	"""
	"Java Server Pages"
	"""
	content = "JSP"
	title = "Java Server Pages"
	lang = "en"


class ascii(base):
	"""
	"American Standard Code for Information Interchange"
	"""
	content = "ASCII"
	title = "American Standard Code for Information Interchange"
	lang = "en"


class sms(base):
	"""
	"Small Message Service"
	"""
	content = "SMS"
	title = "Small Message Service"
	lang = "en"


class p2p(base):
	"""
	"Peer To Peer"
	"""
	content = "P2P"
	title = "Peer To Peer"
	lang = "en"


class gif(base):
	"""
	"Graphics Interchange Format"
	"""
	content = "GIF"
	title = "Graphics Interchange Format"
	lang = "en"


class png(base):
	"""
	"Portable Network Graphics"
	"""
	content = "PNG"
	title = "Portable Network Graphics"
	lang = "en"


class uddi(base):
	"""
	"Universal Description, Discovery and Integration"
	"""
	content = "UDDI"
	title = "Universal Description, Discovery and Integration"
	lang = "en"


class wsdl(base):
	"""
	"Web Services Description Language"
	"""
	content = "WSDL"
	title = "Web Services Description Language"
	lang = "en"


class cdrom(base):
	content = "CDROM"


class snmp(base):
	"""
	"Simple Network Management Protocol"
	"""
	content = "SNMP"
	title = "Simple Network Management Protocol"
	lang = "en"


class ssl(base):
	"""
	"Secure Socket Layer"
	"""
	content = "SSL"
	title = "Secure Socket Layer"
	lang = "en"


class vrml(base):
	"""
	"Virtual Reality Modelling Language"
	"""
	content = "VRML"
	title = "Virtual Reality Modelling Language"
	lang = "en"


class tco(base):
	"""
	"Total Cost of Ownership"
	"""
	content = "TCO"
	title = "Total Cost of Ownership"
	lang = "en"


class crm(base):
	"""
	"Customer Relationship Management"
	"""
	content = "CRM"
	title = "Customer Relationship Management"
	lang = "en"


class cms(base):
	"""
	"Content Management System"
	"""
	content = "CMS"
	title = "Content Management System"
	lang = "en"


class bnf(base):
	"""
	"Backus Naur Form"
	"""
	content = "BNF"
	title = "Backus Naur Form"
	lang = "en"


class mime(base):
	"""
	"Multipurpose Internet Mail Extensions"
	"""
	content = "MIME"
	title = "Multipurpose Internet Mail Extensions"
	lang = "en"


class wysiwyg(base):
	"""
	"What You See Is What You Get"
	"""
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
	"""
	"Scalable Vector Graphics"
	"""
	content = "SVG"
	title = "Scalable Vector Graphics"
	lang = "en"


class utc(base):
	"""
	"Coordinated Universal Time"
	"""
	content = "UTC"
	title = "Coordinated Universal Time"
	lang = "en"


class wsgi(base):
	"""
	"Web Server Gateway Interface"
	"""
	content = "WSGI"
	title = "Web Server Gateway Interface"
	lang = "en"
