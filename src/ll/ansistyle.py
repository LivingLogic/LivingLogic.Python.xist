# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2000-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2000-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`ll.ansistyle` is a module that helps colorize terminal output
with ANSI escape sequences.

Color values are integers between -1 and 511 (octal 0777).
The lowest 3 bits are used for the background colors 0-7. Bits 3-5 are used for
the foreground color. Bit 6 (0100) is used for bold (or other shades of the
color 0-7, depending on your terminal). Bit 7 (0200) is used for underlined text
and bit 8 (0400) is used for blinking text. The color value -1 means
"don't change the color".

To add color switching escape sequences to normal output test, use a
:class:`Colorizer` object like this::

	>>> from ll import ansistyle
	>>> c = ansistyle.Colorizer()
	>>> list(c.feed("spam", 0157, "eggs", None))
	['spam', '\x1b[1;35;47m', 'eggs', '\x1b[0m']

For more info see the description of :meth:`Colorizer.feed`.

There is a second level API for :class:`ansistyle.Colorizer`, which
can be used like this::

	>>> from ll import ansistyle
	>>> list(ansistyle.Text("spam", 0157, "eggs").parts())
	['spam', '\x1b[1;35;47m', 'eggs', '\x1b[0m']

Furthermore you can print :class:`ansistyle.Text` instances directly
to get colored output.

For more information see the documentation for :class:`ansistyle.Text`.
"""


from ll._ansistyle import switchcolor


__docformat__ = "xist"


class Colorizer(object):
	"""
	A :class:`Colorizer` object manages the current color and style and will
	intersperse normal output text with ANSI escape sequences for switching
	output color and style.
	"""

	def __init__(self, colored=True):
		"""
		Create a :class:`Colorizer` instance. If :obj:`colored` is false,
		output will never contain any color/style switching escape sequences.
		"""
		self.colored = colored
		self._colors = [0o070]
		self._activecolor = 0o070

	def pushcolor(self, color):
		"""
		Push :obj:`color` onto the color stack
		"""
		self._colors.append(color)

	def popcolor(self):
		"""
		Pop a color from the color stack.
		"""
		return self._colors.pop(-1)

	def _switchcolor(self, color):
		if self.colored and color != -1:
			result = switchcolor(self._activecolor, color)
			self._activecolor = color
			return result
		return ""

	def feed(self, *strings):
		"""
		This method is a generator and will yield all the strings in :obj:`strings`
		with interspersed color switching escape sequences. Items in :obj:`strings`
		can be the following:

			Strings
				Strings will be output by :meth:`feed` in the appropriate spot.

			Numbers
				A number in the argument sequence will switch to that color value.

			``None``
				This will switch back to the default color (This is different from
				using the color number 0070, because 0070 will only switch colors
				if there is some output string afterwards).

			Sequences
				Those will be recursively fed to :meth:`feed` with the following
				added functionality: The color that was active before the start
				of the sequence will be restored after the end.
		"""
		for string in strings:
			if isinstance(string, int):
				if string != -1:
					self._colors[-1] = string
			elif string is None:
				part = self._switchcolor(0o070)
				if part:
					yield part
			elif isinstance(string, str):
				if string:
					part = self._switchcolor(self._colors[-1])
					if part:
						yield part
					yield string
			else:
				self.pushcolor(self._colors[-1]) # duplicate current color
				yield from self.feed(*string)
				self.popcolor()


class Text(list):
	"""
	A colored string. A :class:`Text` object is a sequence, the sequence
	items may either be strings or :class:`Text` objects themselves.
	"""

	def __init__(self, *content):
		list.__init__(self, content)

	def append(self, *others):
		list.extend(self, others)

	def __call__(self, *others):
		list.extend(self, others)
		return self

	def insert(self, index, *others):
		list.__setitem__(self, slice(index, index), list(others))

	def __repr__(self):
		return "%s.%s(%s)" % (self.__class__.__module__, self.__class__.__qualname__, list.__repr__(self)[1:-1])

	def parts(self, colored=True):
		"""
		This generator yields the strings that will make up the final colorized string.
		"""
		colorizer = Colorizer(colored)
		yield from colorizer.feed(self, None)

	def string(self, colored=True):
		"""
		Return the resulting string (with escape sequences, if :obj:`colored` is true).
		"""
		return "".join(self.parts(colored))

	def __str__(self):
		"""
		Return the resulting string with ANSI color escape sequences.
		"""
		return self.string(True)


class EscapedText(Text):
	"""
	An extension to the :class:`Text` class. Special characters can be replaced
	by customized :class:`Text` objects via the :meth:`escapechar` method.
	"""
	def __init__(self, *content):
		newcontent = []
		for text in content:
			if isinstance(text, str):
				wasstr = None
				for c in text:
					c = self.escapechar(c)
					isstr = isinstance(c, str)
					if wasstr and isstr:
						newcontent[-1] += c
					else:
						newcontent.append(c)
					wasstr = isstr
			else:
				newcontent.append(text)
		Text.__init__(self, *newcontent)

	def escapechar(self, char):
		"""
		Return a replacement :class:`Text` object for the character :obj:`char`
		or :obj:`char` itself, if the character should be used as is. This method
		should be overwritten by subclasses.
		"""
		return char
