#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of Living Logic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVING LOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVING LOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
This module contains entities for a bunch of Java abbreviations and acronyms.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc, html

class rmi(xsc.Entity):
	def transform(self, transformer=None):
		return html.abbr("RMI", title="Remote Method Invocation", lang="en")
	def asPlainString(self):
		return u"RMI"

class jfc(xsc.Entity):
	def transform(self, transformer=None):
		return html.abbr("JFC", title="Java Foundation Classes", lang="en")
	def asPlainString(self):
		return u"JFC"

class awt(xsc.Entity):
	def transform(self, transformer=None):
		return html.abbr("AWT", title="Abstract Window Toolkit", lang="en")
	def asPlainString(self):
		return u"AWT"

class jdbc(xsc.Entity):
	def transform(self, transformer=None):
		return html.abbr("JDBC", title="Java Database Connectivity", lang="en")
	def asPlainString(self):
		return u"JDBC"

class jndi(xsc.Entity):
	def transform(self, transformer=None):
		return html.abbr("JNDI", title="Java Naming and Directory Interface", lang="en")
	def asPlainString(self):
		return u"JNDI"

class jpda(xsc.Entity):
	def transform(self, transformer=None):
		return html.abbr("JPDA", title="Java Platform Debugger Architecture", lang="en")
	def asPlainString(self):
		return u"JPDA"

class jvmpi(xsc.Entity):
	def transform(self, transformer=None):
		return html.abbr("JVMPI", title="Java Virtual Machine Profiler Interface", lang="en")
	def asPlainString(self):
		return u"JVMPI"

class jni(xsc.Entity):
	def transform(self, transformer=None):
		return html.abbr("JNI", title="Java Native Interface", lang="en")
	def asPlainString(self):
		return u"JNI"

class ejb(xsc.Entity):
	def transform(self, transformer=None):
		return html.abbr("EJB", title="Enterprice Java Beans", lang="en")
	def asPlainString(self):
		return u"EJB"

class jgl(xsc.Entity):
	def transform(self, transformer=None):
		return html.abbr("JGL", title="Java Generic Library", lang="en")
	def asPlainString(self):
		return u"JGL"

namespace = xsc.Namespace("javaabbr", "http://www.livinglogic.de/DTDs/javaabbr.dtd", vars())
