#! /usr/bin/env python

"""
A module that allows you to embed PHP processing instructions.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc

class php(xsc.ProcInst):
	"""
	<doc:par>PHP processing instruction
	(must be used with an explicit target php to work with &xml;)</doc:par>
	"""

class If(php):
	name = "if"

	def convert(self, converter):
		return php(u"if (" + self.content + "){")

class Else(php):
	name = "else"

	def convert(self, converter):
		return php(u"}else{")

class ElIf(php):
	name = "elif"

	def convert(self, converter):
		return php(u"}else if (" + self.content + "){")

class End(php):
	name = "end"

	def convert(self, converter):
		return php(u"}")

# register all the classes we've defined so far
namespace = xsc.Namespace("php", "http://www.php.net/", vars())
