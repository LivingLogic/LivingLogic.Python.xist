#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2005 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2005 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>An &xist; module that allows embedding Python code in &xml;</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys

from ll.xist import xsc, sandbox
import html


class Code(object):
	def __init__(self, text, ignorefirst=False):
		# get the individual lines; ignore "\r" as this would mess up whitespace handling later
		# use list comprehension to get a list and not a Frag
		lines = [ line for line in text.replace(u"\r", u"").splitlines() ]
		# split of the whitespace at the beginning of each line
		for i in xrange(len(lines)):
			line = lines[i]
			rest = line.lstrip()
			white = line[:len(line)-len(rest)]
			lines[i] = [white, rest]
		# drop all empty lines at the beginning; if we drop a line we no longer have to handle the first specifically
		while lines and not lines[0][1]:
			del lines[0]
			ignorefirst = False
		# drop all empty lines at the end
		while lines and not lines[-1][1]:
			del lines[-1]
		# complain, if the first line contains whitespace, although ignorewhitespace said it doesn't
		if ignorefirst and lines and lines[0][0]:
			raise ValueError("can't ignore the first line, as it does contain whitespace")
		# find the shortest whitespace in non empty lines
		shortestlen = sys.maxint
		for i in xrange(ignorefirst, len(lines)):
			if lines[i][1]:
				shortestlen = min(shortestlen, len(lines[i][0]))
		# remove the common whitespace; a check is done, whether the common whitespace is the same in all lines
		common = None
		if shortestlen:
			for i in xrange(ignorefirst, len(lines)):
				if lines[i][1]:
					test = lines[i][0][:shortestlen]
					if common is not None:
						if common != test:
							raise SyntaxError("indentation mismatch")
					common = test
					lines[i][0] = lines[i][0][shortestlen:]
				else:
					lines[i][0] = u""
		self.lines = lines

	def indent(self):
		for line in self.lines:
			line[0] = u"\t" + line[0]

	def funcify(self, name=u"__"):
		self.indent()
		self.lines.insert(0, [u"", u"def %s(converter):" % name])

	def asString(self):
		v = []
		for line in self.lines:
			v += line
			v += u"\n"
		return u"".join(v)


class pyexec(xsc.ProcInst):
	"""
	<par>here the content of the processing instruction is executed
	as Python code, so you can define and register &xist; elements here.
	Execution is done when the node is constructed, so definitions made
	here will be available afterwards (e.g. during the rest of the
	file parsing stage). When converted to &html; such a node will result
	in an empty <lit>Null</lit> node.</par>

	<par>These processing instructions will be evaluated and executed in the
	namespace of the module <module>sandbox</module>.</par>
	"""

	def __init__(self, content=u""):
		xsc.ProcInst.__init__(self, content)
		code = Code(self.content, 1)
		exec code.asString() in sandbox.__dict__ # requires Python 2.0b2 (and doesn't really work)

	def convert(self, converter):
		return xsc.Null # has been executed at construction time already, so we don't have to do anything here


class pyeval(xsc.ProcInst):
	"""
	<par>here the code will be executed when the node is converted to &html;
	as if it was the body of a function, so you can return an expression
	here. Although the content is used as a function body no indentation
	is neccessary or allowed. The returned value will be converted to a
	node and this resulting node will be converted to &html;.</par>

	<par>These processing instructions will be evaluated and executed in the
	namespace of the module <module>ll.xist.sandbox</module>.</par>

	<par>Note that you should not define the symbol <lit>__</lit> in any of your &xist;
	processing instructions, as it is used by &xist; for internal purposes.</par>
	"""

	def convert(self, converter):
		"""
		<par>Evaluates the code as if it was the body of a Python funtion.
		The <arg>converter</arg> argument will be available
		under the name <arg>converter</arg> as an argument to the function.</par>
		"""
		code = Code(self.content, 1)
		code.funcify()
		exec code.asString() in sandbox.__dict__ # requires Python 2.0b2 (and doesn't really work)
		return xsc.ToNode(sandbox.__(converter)).convert(converter)


class __ns__(xsc.Namespace):
	xmlname = "code"
	xmlurl = "http://xmlns.livinglogic.de/xist/ns/code"
__ns__.makemod(vars())

