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
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
This module contains classes for handling ANSI colors.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import UserList

class Text(UserList.UserList):
	"""
	a colored string, colors can be numbers from
	0 to 15 for the 16 ANSI colors or -1 if this
	Text should use the current color. A Text object
	is a sequence, the sequence items may either be
	strings or Text objects themselves.
	"""
	color = -1 # the default color, which means "do not switch color"

	def __init__(self, *content):
		self._content = list(content)

	def __getitem__(self, index):
		return self._content[index]

	def __setitem__(self, index, value):
		self._content[index] = value

	def __delitem__(self, index):
		del self._content[index]

	def __getslice__(self, index1, index2):
		return self._content[index1:index2]

	def __setslice__(self, index1, index2, sequence):
		self._content[index1:index2] = sequence

	def __delslice__(self, index1, index2):
		del self._content[index1:index2]

	def __len__(self):
		return len(self._content)

	def append(self, *others):
		self._content.extend(others)

	def insert(self, index, *others):
		self._content[index:index] = others

	def getColor(self):
		"""
		return the color of this string. Overwrite this method
		or the class attribute color to change the behaviour.
		"""
		return self.color

	def __repr__(self):
		return self.__class__.__name__ + "(" + ", ".join([ repr(text) for text in self.data ]) + ")"

	def __str__(self):
		"""
		return the resulting string with ANSI color escape sequences.
		"""
		stream = Stream()
		stream._write(self)
		stream._switchColor(7) # return to the default color
		return str(stream)

class EscapedText(Text):
	"""
	An extension to the text class. Special characters can be replaced
	by customized Text objects via the escapeChar method.
	"""
	def __init__(self, *data):
		newdata = []
		for text in data:
			if isinstance(text, Text):
				newdata.append(text)
			else:
				for c in text:
					c = self.escapeChar(c)
					newdata.append(c)
		Text.__init__(self, *newdata)

	def escapeChar(self, char):
		"""
		return a replacement Text object for the character char
		or char itself, if the character should be used as is.
		This method should be overwritten by subclasses.
		"""
		return char

class Stream:
	"""
	adds color capability to an output stream. A Stream
	keeps track of the current color and writes ANSI color escape
	sequences to the stream where appropriate. colors are numbers
	from 0 to 15 (or -1 for "no color change").
	"""

	def __init__(self):
		self._buffer = []
		self._colorStack = [0x7]
		self._activeColor = 0x7

	def _switchColor(self, color):
		"""
		internal method: switches to the color color.
		If color is different from the currently active
		color (and not -1), the appropriate ANSI escape
		sequence will be written to the buffer.
		"""
		if color != -1 and self._activeColor != color:
			if color == 0x7:
				s = "0"
			else:
				if (self._activeColor&0x8) != (color&0x8):
					if color&0x8:
						s = "1"
						if (self._activeColor&0x7) != (color&0x7):
							s += ";" + str(30+(color&0x7))
					else:
						s = "0;" + str(30+(color&0x7))
				else:
					s = str(30+(color&0x7))
			self._buffer.append("\033[" + s + "m")
			self._activeColor = color

	def _write(self, text):
		"""
		writes text to the buffer in self.
		"""
		if isinstance(text, Text):
			color = text.getColor()
			if color != -1:
				self._colorStack.append(color) # push the color onto the stack
				for text in text._content:
					self._write(text)
				self._colorStack.pop() # pop the color from the stack
			else:
				for text in text._content:
					self._write(text)
		else:
			self._switchColor(self._colorStack[-1])
			self._buffer.append(text)

	def __str__(self):
		return "".join(self._buffer)

