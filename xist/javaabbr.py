#! /usr/bin/env python

"""
This module contains entities for a bunch of Java abbreviations and acronyms.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

from xist import xsc,html

class rmi(xsc.Entity):
	def asHTML(self):
		return html.abbr("RMI", title="Remote Method Invocation", lang="en")
	def asPlainString(self):
		return u"RMI"

class jfc(xsc.Entity):
	def asHTML(self):
		return html.abbr("JFC", title="Java Foundation Classes", lang="en")
	def asPlainString(self):
		return u"JFC"

class awt(xsc.Entity):
	def asHTML(self):
		return html.abbr("AWT", title="Abstract Window Toolkit", lang="en")
	def asPlainString(self):
		return u"AWT"

class jdbc(xsc.Entity):
	def asHTML(self):
		return html.abbr("JDBC", title="Java Database Connectivity", lang="en")
	def asPlainString(self):
		return u"JDBC"

class jndi(xsc.Entity):
	def asHTML(self):
		return html.abbr("JNDI", title="Java Naming and Directory Interface", lang="en")
	def asPlainString(self):
		return u"JNDI"

class jpda(xsc.Entity):
	def asHTML(self):
		return html.abbr("JPDA", title="Java Platform Debugger Architecture", lang="en")
	def asPlainString(self):
		return u"JPDA"

class jvmpi(xsc.Entity):
	def asHTML(self):
		return html.abbr("JVMPI", title="Java Virtual Machine Profiler Interface", lang="en")
	def asPlainString(self):
		return u"JVMPI"

class jni(xsc.Entity):
	def asHTML(self):
		return html.abbr("JNI", title="Java Native Interface", lang="en")
	def asPlainString(self):
		return u"JNI"

class ejb(xsc.Entity):
	def asHTML(self):
		return html.abbr("EJB", title="Enterprice Java Beans", lang="en")
	def asPlainString(self):
		return u"EJB"

class jgl(xsc.Entity):
	def asHTML(self):
		return html.abbr("JGL", title="Java Generic Library", lang="en")
	def asPlainString(self):
		return u"JGL"

namespace = xsc.Namespace("javaabbr", "http://www.livinglogic.de/DTDs/javaabbr.dtd", vars())
