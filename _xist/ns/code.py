#! /usr/bin/env python
# -*- coding: Latin-1 -*-

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
<doc:par>An &xist; module that allows embedding Python code in &xml;</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import sys

from ll.xist import xsc, sandbox
import html

class Code:
	def __init__(self, text, ignorefirst=0):
		# get the individual lines; ignore "\r" as this would mess up whitespace handling later
		# use list comprehension to get a list and not a Frag
		lines = [ line for line in text.replace("\r", "").splitlines() ]
		# split of the whitespace at the beginning of each line
		for i in xrange(len(lines)):
			line = lines[i]
			rest = line.lstrip()
			white = line[:len(line)-len(rest)]
			lines[i] = [white, rest]
		# drop all empty lines at the beginning; if we drop a line we no longer have to handle the first specifically
		while lines and not lines[0][1]:
			del lines[0]
			ignorefirst = 0
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
			line[0] = "\t" + line[0]

	def funcify(self, name="__"):
		self.indent()
		self.lines.insert(0, [u"", u"def " + name + u"(converter):"])

	def asString(self):
		v = []
		for line in self.lines:
			v += line
			v += "\n"
		return "".join(v)

class exec_(xsc.ProcInst):
	"""
	<doc:par>here the content of the processing instruction is executed
	as Python code, so you can define and register &xist; elements here.
	Execution is done when the node is constructed, so definitions made
	here will be available afterwards (e.g. during the rest of the
	file parsing stage). When converted to &html; such a node will result
	in an empty <lit>Null</lit> node.</doc:par>

	<doc:par>These processing instructions will be evaluated and executed in the
	namespace of the module <module>sandbox</module>.</doc:par>
	"""
	xmlname = "exec"

	def __init__(self, content=u""):
		xsc.ProcInst.__init__(self, content)
		code = Code(self.content, 1)
		exec code.asString() in sandbox.__dict__ # requires Python 2.0b2 (and doesn't really work)

	def convert(self, converter):
		return xsc.Null # has been executed at construction time already, so we don't have to do anything here

class eval_(xsc.ProcInst):
	"""
	<doc:par>here the code will be executed when the node is converted to &html;
	as if it was the body of a function, so you can return an expression
	here. Although the content is used as a function body no indentation
	is neccessary or allowed. The returned value will be converted to a
	node and this resulting node will be converted to &html;.</doc:par>

	<doc:par>These processing instructions will be evaluated and executed in the
	namespace of the module <module>sandbox</module>.</doc:par>

	<doc:par>Note that you should not define the symbol <lit>__</lit> in any of your &xist;
	processing instructions, as it is used by &xist; for internal purposes.</doc:par>
	"""
	xmlname = "eval"

	def convert(self, converter):
		"""
		<doc:par>Evaluates the code as if it was the body of a Python funtion.
		The <arg>converter</arg> argument will be available
		under the name <arg>converter</arg> as an argument to the function.</doc:par>
		"""
		code = Code(self.content, 1)
		code.funcify()
		exec code.asString() in sandbox.__dict__ # requires Python 2.0b2 (and doesn't really work)
		return xsc.ToNode(sandbox.__(converter)).convert(converter)

xmlns = xsc.Namespace("code", "http://xmlns.livinglogic.de/xist/ns/code", vars())
