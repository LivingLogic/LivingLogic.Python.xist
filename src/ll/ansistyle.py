#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2000-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2000-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


r"""
<p><mod>ll.ansistyle</mod> is a module that helps colorize terminal output
with &ansi; escape sequences.</p>

<p>Color values are integers between -1 and 511 (octal 0777).
The lowest 3 bits are used for the background colors 0-7. Bits 3-5 are used for
the foreground color. Bit 6 (0100) is used for bold (or other shades of the
color 0-7, depending on your terminal). Bit 7 (0200) is used for underlined text
and bit 8 (0400) is used for blinking text. The color value -1 means
<z>don't change the color</z>.</p>

<p>To add color switching escape sequences to normal output test, use a
<class>Colorizer</class> object like this:</p>
<tty>
<prompt>&gt;&gt;&gt; </prompt><input>from ll import ansistyle</input>
<prompt>&gt;&gt;&gt; </prompt><input>c = ansistyle.Colorizer()</input>
<prompt>&gt;&gt;&gt; </prompt><input>list(c.feed("spam", 0157, "eggs", None))</input>
['spam', '\x1b[1;35;47m', 'eggs', '\x1b[0m']
</tty>

<p>For more info see the description of the
<pyref class="Colorizer" method="feed"><meth>feed</meth></pyref>.</p>

<p>There is a second level &api; for <class>ansistyle.Colorizer</class>, which
can be used like this:</p>

<tty>
<prompt>&gt;&gt;&gt; </prompt><input>from ll import ansistyle</input>
<prompt>&gt;&gt;&gt; </prompt><input>list(ansistyle.Text("spam", 0157, "eggs").parts())</input>
['spam', '\x1b[1;35;47m', 'eggs', '\x1b[0m']
</tty>

<p>Furthermore you can print <class>ansistyle.Text</class> instances directly
to get colored output.</p>

<p>For more information see the documentation for
<pyref class="Text"><class>ansistyle.Text</class></pyref>.</p>
"""


from _ansistyle import switchcolor


__docformat__ = "xist"


class Colorizer(object):
	"""
	A <class>Colorizer</class> object manages the current color and style and will
	intersperse normal output text with &ansi; escape sequences for switching
	output color and style.
	"""

	def __init__(self, colored=True):
		"""
		Create a <class>Colorizer</class> instance. If <arg>colored</arg> is false,
		output will never contain any color/style switching escape sequences.
		"""
		self.colored = colored
		self._colors = [0070]
		self._activecolor = 0070

	def pushcolor(self, color):
		"""
		Push <arg>color</arg> onto the color stack
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
		<p>This method is a generator and will yield all the strings in <arg>strings</arg>
		with interspersed color switching escape sequences. Items in <arg>strings</arg>
		can be the following:</p>
		<dl>
		<term>Strings (<class>str</class> and <class>unicode</class>)</term>
		<item>Strings will be output by <meth>feed</meth> in the appropriate spot.</item>
		<term>Numbers</term>
		<item>A number in the argument sequence will switch to that color value.</item>
		<term><lit>None</lit></term>
		<item>This will switch back to the default color (This is different from
		using the color number 0070, because 0070 will only switch colors if there
		is some output string afterwards).</item>
		<term>Sequences</term>
		<item>Those will be recursively fed to <meth>feed</meth> with the following
		added functionality: The color that was active before the start of the
		sequence will be restored after the end.</item>
		</dl>
		"""
		for string in strings:
			if isinstance(string, (int, long)):
				if string != -1:
					self._colors[-1] = string
			elif string is None:
				part = self._switchcolor(0070)
				if part:
					yield part
			elif isinstance(string, basestring):
				if string:
					part = self._switchcolor(self._colors[-1])
					if part:
						yield part
					yield string
			else:
				self.pushcolor(self._colors[-1]) # duplicate current color
				for part in self.feed(*string):
					yield part
				self.popcolor()


class Text(list):
	"""
	A colored string. A <class>Text</class> object is a sequence, the sequence
	items may either be strings or <class>Text</class> objects themselves.
	"""

	def __init__(self, *content):
		list.__init__(self, content)

	def append(self, *others):
		list.extend(self, others)

	def __call__(self, *others):
		list.extend(self, others)
		return self

	def insert(self, index, *others):
		list.__setslice__(self, index, index, list(others))

	def __repr__(self):
		return "%s.%s(%s)" % (self.__class__.__module__, self.__class__.__name__, list.__repr__(self)[1:-1])

	def parts(self, colored=True):
		"""
		This generator yields the strings that will make up the final colorized string.
		"""
		colorizer = Colorizer(colored)
		for part in colorizer.feed(self, None):
			yield part

	def string(self, colored=True):
		"""
		Return the resulting string (with escape sequences, if <arg>colored</arg> is true).
		"""
		return "".join(self.parts(colored))

	def __str__(self):
		"""
		Return the resulting string with &ansi; color escape sequences.
		"""
		return self.string(True)


class EscapedText(Text):
	"""
	An extension to the <class>Text</class> class. Special characters can be
	replaced by customized <class>Text</class> objects via the
	<meth>escapechar</meth> method.
	"""
	def __init__(self, *content):
		newcontent = []
		for text in content:
			if isinstance(text, basestring):
				wasstr = None
				for c in text:
					c = self.escapechar(c)
					isstr = isinstance(c, basestring)
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
		Return a replacement <class>Text</class> object for the character
		<arg>char</arg> or <arg>char</arg> itself, if the character should be
		used as is. This method should be overwritten by subclasses.
		"""
		return char
