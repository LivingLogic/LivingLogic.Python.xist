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
This module contains classes for handling ANSI colors.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import UserList

class StringBuffer:
	def __init__(self):
		self.buffer = []
	def write(self, text):
		self.buffer.append(text)
	def __str__(self):
		return "".join(self.buffer)

class Text(UserList.UserList):
	"""
	a colored string, that may consist of
	many parts, some of them may be Text
	objects themselves.
	"""
	color = 0x7 # default color

	def __init__(self, *data):
		UserList.UserList.__init__(self, data)

	def getColor(self):
		"""
		return the color of this string. Overwrite this method
		or the class attribute color to change the behaviour.
		"""
		return self.color

	def write(self, stream):
		"""
		writes self to the Stream object stream.
		"""
		stream.pushColor(self.getColor())
		for text in self.data:
			if isinstance(text, Text):
				text.write(stream)
			else:
				stream.write(text)
		stream.popColor()

	def __repr__(self):
		return self.__class__.__name__ + "(" + ", ".join([ repr(text) for text in self.data ]) + ")"

	def __str__(self):
		buffer = StringBuffer()
		stream = Stream(buffer)
		self.write(stream)
		stream.finish()
		return str(buffer)

class Stream:
	"""
	adds color capability to an output stream. A Stream
	keeps track of the current color and writes ANSI color escape
	sequences to the stream where appropriate. colors are numbers
	from 0 to 15.
	"""

	def __init__(self, stream):
		self._basestream = stream
		self._colorStack = [0x7]
		self._activeColor = 0x7

	def pushColor(self, color):
		"""
		push the color color onto the color stack.
		It becames the current color. Returning to
		the previous color is possible with
		popColor().
		"""
		self._colorStack.append(color)

	def popColor(self):
		"""
		return to the previous active color.
		"""
		self._colorStack.pop()

	def _switchColor(self, color):
		"""
		internal method: switches to the color color.
		If color is different from the currently active
		color, the appropriate ANSI escape sequence will
		be written to the stream.
		"""
		if self._activeColor != color:
			if color == 0x7:
				s = "0"
			else:
				s = ""
				if (self._activeColor&0x8) != (color&0x8):
					if color&0x8:
						s += "1;"
					else:
						s += "0;"
				s += str(30+(color&0x7))
			self._basestream.write("\033[" + s + "m")
			self._activeColor = color

	def write(self, *texts):
		"""
		writes the texts to the stream, and ensures,
		that the texts will be in the correct color.
		"""
		for text in texts:
			if isinstance(text, Text):
				text.write(self)
			else:
				if len(text):
					self._switchColor(self._colorStack[-1])
					self._basestream.write(text)

	def finish(self):
		"""
		should be called at the end of an output
		sequence to return to the default
		color.
		"""
		self._switchColor(7)
