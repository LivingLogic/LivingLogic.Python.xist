#! /usr/bin/env python

## Copyright 1999-2000 by Living Logic AG, Bayreuth, Germany.
## Copyright 1999-2000 by Walter Dörwald
##
## See the file LICENSE for licensing details

"""
This module contains classes that may be used as publishing
handler in <methodref module="xist.xsc" class="Node">publish</methodref>.
"""

import sys
import string

class Publisher:
	"""
	base class. just an interface.
	"""
	def __call__(self,*texts):
		"""
		receives the strings to be printed.
		"""
		pass

class FilePublisher:
	"""
	writes the strings to a file.
	"""
	def __init__(self,fh):
		self.fh = fh

	def __call__(self,*texts):
		for text in texts:
			if type(text) in (ListType,TupleType):
				apply(self,text)
			else:
				self.fh.write(str(text))

class PrintPublisher(FilePublisher):
	"""
	passes the strings to <code>print</code>.
	"""
	def __init__(self):
		FilePublisher.__init__(self,sys.stdout)

class StringPublisher:
	"""
	collects all strings in an array.
	The joined strings are available via
	<methodref>__str__</methodref>
	"""

	def __init__(self):
		self.texts = []

	def __call__(self,*texts):
		for text in texts:
			self.texts.append(str(text))

 	def __str__(self):
		"""
		Return the published strings as one long string.
		"""
		return string.join(self.texts,"")

