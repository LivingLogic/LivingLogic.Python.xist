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

class PrintPublisher:
	"""
	passes the strings to print.
	"""
	def __call__(self,*texts):
		for text in texts:
			sys.stdout.write(text)

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
			self.texts.append(text)

	def __str__(self):
		"""
		Return the published strings as one long string.
		"""
		return string.join(self.texts,"")

