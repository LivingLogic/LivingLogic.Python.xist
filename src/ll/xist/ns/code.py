# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
An XIST module that allows embedding Python code in XML.
"""


import sys

from ll.xist import xsc
from ll.xist.ns import html


__docformat__ = "reStructuredText"


class Code:
	def __init__(self, text, ignorefirst=False):
		# get the individual lines; ignore "\r" as this would mess up whitespace handling later
		# use list comprehension to get a list and not a Frag
		lines = [ line for line in text.replace("\r", "").splitlines() ]
		# split of the whitespace at the beginning of each line
		for i in range(len(lines)):
			line = lines[i]
			rest = line.lstrip()
			white = line[:len(line)-len(rest)]
			lines[i] = [white, rest]
		# drop all empty lines at the beginning; if we drop a line, we no longer have to handle the first specifically
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
		shortestlen = sys.maxsize
		for i in range(ignorefirst, len(lines)):
			if lines[i][1]:
				shortestlen = min(shortestlen, len(lines[i][0]))
		# remove the common whitespace; a check is done, whether the common whitespace is the same in all lines
		common = None
		if shortestlen:
			for i in range(ignorefirst, len(lines)):
				if lines[i][1]:
					test = lines[i][0][:shortestlen]
					if common is not None:
						if common != test:
							raise SyntaxError("indentation mismatch")
					common = test
					lines[i][0] = lines[i][0][shortestlen:]
				else:
					lines[i][0] = ""
		self.lines = lines

	def indent(self):
		for line in self.lines:
			line[0] = "\t" + line[0]

	def funcify(self, name="__"):
		self.indent()
		self.lines.insert(0, ["", f"def {name}(converter):"])

	def asstring(self):
		v = []
		for line in self.lines:
			v.extend(line)
			v.append("\n")
		return "".join(v)


class _base(xsc.ProcInst):
	register = False

	class Context(xsc.ProcInst.Context):
		def __init__(self):
			xsc.ProcInst.Context.__init__(self)
			self.sandbox = {}


class pyexec(_base):
	"""
	When converting a :class:`pyexec` object the content of the processing
	instruction is executed as Python code. Execution is done when the node
	is converted. When converted such a node will result in an empty
	:data:`Null` node.

	These processing instructions will be evaluated and executed in the
	namespace of the module sandbox (which will be store in the converter
	context).
	"""

	def convert(self, converter):
		code = Code(self.content, True)
		sandbox = converter[self].sandbox
		exec(code.string(), sandbox) # requires Python 2.0b2 (and doesn't really work)
		return xsc.Null


class pyeval(_base):
	"""
	The content of a :class:`pyeval` processing instruction will be executed
	when the node is converted as if it was the body of a function, so you
	can return an expression here. Although the content is used as a function
	body no indentation is necessary or allowed. The returned value will be
	converted to a node and this resulting node will be converted.

	These processing instructions will be evaluated and executed in the
	namespace of the module sandbox (which will be store in the converter
	context).

	Note that you should not define the symbol ``__`` in any of your XIST
	processing instructions, as it is used by XIST for internal purposes.
	"""

	def convert(self, converter):
		"""
		Evaluates the code as if it was the body of a Python function. The
		:obj:`converter` argument will be available under the name
		:obj:`converter` as an argument to the function.
		"""
		code = Code(self.content, True)
		code.funcify()
		sandbox = converter[self].sandbox
		exec(code.asstring(), sandbox) # requires Python 2.0b2 (and doesn't really work)
		return xsc.tonode(sandbox["__"](converter)).convert(converter)
