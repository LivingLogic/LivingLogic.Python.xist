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
This modules contains the base class for the converter objects
used in the call to the convert method.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import types

class Context:
	"""
	This is an empty class, that can be used by the
	<pyref module="xist.xsc" class="Node" method="convert">convert</pyref>
	method to hold element specific data during the convert call. The method
	<pyref class="Converter" method="__getitem__">Converter.__getitem__</pyref>
	will return a unique instance of this class.
	"""
	
	def __init__(self):
		pass

class Converter:
	"""
	An instance of this class is passed around in calls to the
	<pyref module="xist.xsc class="Node" method="convert">convert</pyref> method. This instance can
	be used when some element needs to keep state across a nested convert call. A typical example
	are nested chapter/subchapter elements with automatic numbering. For an example see the element
	<pyref module="xist.ns.doc" class="section">section</pyref>.
	"""
	def __init__(self, mode=None, stage=None, target=None, lang=None):
		self.mode = mode
		if stage is None:
			self.stage = "deliver"
		else:
			self.stage = stage
		if target is None:
			self.target = "html"
		else:
			self.target = target
		self.lang = lang
		self.contexts = {}

	def __getitem__(self, class_):
		"""
		<doc:par>Return a context object that is unique for <pyref arg="class_">class_</pyref>,
		which should be the class object of an element type. This means that every element type
		gets it's own context and can store information there that needs to be available
		across calls to <pyref module="xist.xsc class="Node" method="convert">convert</pyref>.</doc:par>
		"""
		return self.contexts.setdefault(class_, Context())
