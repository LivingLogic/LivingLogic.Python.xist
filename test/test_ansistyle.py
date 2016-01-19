#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2000-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2000-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


from ll import ansistyle


def test_noswitch():
	def check(c):
		assert not ansistyle.switchcolor(c, c)

	for blink in (0000, 0o400):
		for underline in (0000, 0o200):
			for bold in (0000, 0o100):
				for foreground in (0000, 0o070):
					for background in (0000, 0o007):
						yield check, blink|underline|bold|foreground|background


def test_blink():
	assert str(ansistyle.Text(0o470, "foo")) == "\033[5mfoo\033[0m"
	assert str(ansistyle.Text(0o470, "foo", ansistyle.Text(0o070, "bar"))) == "\033[5mfoo\033[0mbar"


def test_underline():
	assert str(ansistyle.Text(0o270, "foo")) == "\033[4mfoo\033[0m"
	assert str(ansistyle.Text(0o270, "foo", ansistyle.Text(0o070, "bar"))) == "\033[4mfoo\033[0mbar"


def test_bold():
	assert str(ansistyle.Text(0o170, "foo")) == "\033[1mfoo\033[0m"
	assert str(ansistyle.Text(0o170, "foo", ansistyle.Text(0o070, "bar"))) == "\033[1mfoo\033[0mbar"


def test_background():
	assert str(ansistyle.Text(0o075, "foo")) == "\033[45mfoo\033[0m"
	assert str(ansistyle.Text(0o075, "foo", ansistyle.Text(0o070, "bar"))) == "\033[45mfoo\033[0mbar"


def test_foreground():
	assert str(ansistyle.Text(0o050, "foo")) == "\033[35mfoo\033[0m"
	assert str(ansistyle.Text(0o050, "foo", ansistyle.Text(0o070, "bar"))) == "\033[35mfoo\033[0mbar"


def test_all():
	assert str(ansistyle.Text(0o754, "foo")) == "\033[1;4;5;35;44mfoo\033[0m"
	assert str(ansistyle.Text(0o754, "foo", ansistyle.Text(0o070, "bar"))) == "\033[1;4;5;35;44mfoo\033[0mbar"


def test_nested():
	assert str(ansistyle.Text(0o075, "foo", ansistyle.Text(0o050, "bar"))) == "\033[45mfoo\033[35;40mbar\033[0m"
	assert str(ansistyle.Text(0o075, "foo", (0o050, "bar"))) == "\033[45mfoo\033[35;40mbar\033[0m"
	assert str(ansistyle.Text(0o075, "foo", (0o050, (0o060, "bar"), "baz"))) == "\033[45mfoo\033[36;40mbar\033[35mbaz\033[0m"


def test_bug():
	assert str(ansistyle.Text(-1, "x", (0o150, "y"), "z")) == "x\033[1;35my\033[0mz"


def test_escaped():
	class Escaped(ansistyle.EscapedText):
		def escapechar(self, c):
			if c == "?":
				return (0o060, "?")
			else:
				return c

	assert str(Escaped("!?!")) == "!\033[36m?\033[0m!"


def test_pushpop():
	c = ansistyle.Colorizer()
	c.pushcolor(0o060)
	assert "".join(c.feed("gurk")) == "\033[36mgurk"
	c.pushcolor(0o050)
	assert "".join(c.feed("hurz")) == "\033[35mhurz"
	c.popcolor()
	assert "".join(c.feed("hinz")) == "\033[36mhinz"
	c.popcolor()
	assert "".join(c.feed("kunz")) == "\033[0mkunz"

