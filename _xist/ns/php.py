#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
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
<doc:par>A module that allows you to embed PHP processing instructions.</doc:par>
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
