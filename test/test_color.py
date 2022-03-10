#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2009-2022 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2022 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import math

import pytest

from ll import color


def test_constructor():
	assert color.Color(10, 20, 30) == (10, 20, 30, 255)
	assert color.Color(40, 50, 60, 70) == (40, 50, 60, 70)


def test_fromcss():
	assert color.Color.fromcss("red") == (0xff, 0x0, 0x0, 0xff)
	assert color.Color.fromcss("#123") == (0x11, 0x22, 0x33, 0xff)
	assert color.Color.fromcss("#123456") == (0x12, 0x34, 0x56, 0xff)
	assert color.Color.fromcss("#abcdef") == (0xab, 0xcd, 0xef, 0xff)
	assert color.Color.fromcss("#ABCDEF") == (0xab, 0xcd, 0xef, 0xff)
	assert color.Color.fromcss("rgb(12, 34, 56)") == (12, 34, 56, 0xff)
	assert color.Color.fromcss("rgb(20%, 40%, 60%)") == (0x33, 0x66, 0x99, 0xff)
	assert color.Color.fromcss("rgba(12, 34, 56, 0)") == (12, 34, 56, 0x0)
	assert color.Color.fromcss("rgba(12, 34, 56, 1)") == (12, 34, 56, 0xff)
	assert color.Color.fromcss("rgba(20%, 40%, 60%, 0)") == (0x33, 0x66, 0x99, 0x0)
	assert color.Color.fromcss("rgba(20%, 40%, 60%, 1)") == (0x33, 0x66, 0x99, 0xff)


def test_fromrgb():
	assert color.Color.fromrgb(0.2, 0.4, 0.6, 0.8) == color.Color(0x33, 0x66, 0x99, 0xcc)


def test_repr():
	assert repr(color.red) == "Color(0xff, 0x00, 0x00)"
	assert repr(color.Color(0x12, 0x34, 0x56, 0x78)) == "Color(0x12, 0x34, 0x56, 0x78)"


def test_str():
	assert str(color.Color(0x12, 0x34, 0x56)) == "#123456"
	assert str(color.Color(0x12, 0x34, 0x56, 0x78)) == "rgba(18,52,86,0.471)"


def test_r_g_b():
	c = color.Color(0x12, 0x34, 0x56, 0x78)
	assert c.r() == 0x12
	assert c.g() == 0x34
	assert c.b() == 0x56
	assert c.a() == 0x78


def test_hls():
	assert (0, 1, 0) == tuple(map(int, color.css("#fff").hls()))


def test_hlsa():
	assert (0, 1, 0, 1) == tuple(map(int, color.css("#fff").hlsa()))


def test_hsv():
	assert (0, 0, 1) == tuple(map(int, color.css("#fff").hsv()))


def test_hsva():
	assert (0, 0, 1, 1) == tuple(map(int, color.css("#fff").hsva()))


def test_hue():
	assert math.isclose(color.css("#f00").hue(), 0)
	assert math.isclose(color.css("#0f0").hue(), 120/360)
	assert math.isclose(color.css("#00f").hue(), 240/360)


def test_sat():
	assert math.isclose(0, color.css("#000").sat())
	assert math.isclose(0, color.css("#fff").sat())
	assert math.isclose(1, color.css("#f00").sat())
	assert math.isclose(1, color.css("#0f0").sat())
	assert math.isclose(1, color.css("#00f").sat())


def test_light():
	math.isclose(0, color.css("#000").light())
	math.isclose(1, color.css("#fff").light())


def test_lum():
	assert math.isclose(1.0   , color.css("#fff").lum())
	assert math.isclose(0.0   , color.css("#000").lum())
	assert math.isclose(0.2126, color.css("#f00").lum())
	assert math.isclose(0.7152, color.css("#0f0").lum())
	assert math.isclose(0.0722, color.css("#00f").lum())


def test_withhue():
	assert color.css("#f00") == color.css("#0f0").withhue(0/6)
	assert color.css("#0f0") == color.css("#f00").withhue(2/6)


def test_withlight():
	assert color.white == color.black.withlight(1.0)
	assert color.black == color.black.withlight(0.0)
	assert color.white == color.white.withlight(1.0)
	assert color.black == color.white.withlight(0.0)


def test_abslight():
	assert color.white == color.black.abslight(1.0)
	assert color.css('#333') == color.black.abslight(0.2)
	assert color.css('#666') == color.css('#333').abslight(0.2)
	assert color.black == color.black.abslight(0.0)
	assert color.black == color.black.abslight(-1.0)
	assert color.white == color.white.abslight(1.0)
	assert color.white == color.white.abslight(0.0)
	assert color.css('#ccc') == color.white.abslight(-0.2)
	assert color.black == color.white.abslight(-1.0)


def test_rellight():
	assert color.white == color.black.rellight(1.0)
	assert color.css('#333') == color.black.rellight(0.2)
	assert color.css('#999') == color.css('#333').rellight(0.5)
	assert color.black == color.black.rellight(0.0)
	assert color.black == color.black.rellight(-1.0)
	assert color.white == color.white.rellight(1.0)
	assert color.white == color.white.rellight(0.0)
	assert color.css('#ccc') == color.white.rellight(-0.2)
	assert color.css('#666') == color.css('#ccc').rellight(-0.5)
	assert color.black == color.white.rellight(-1.0)


def test_withsat():
	assert color.css("#7f7f7f") == color.css("#0f0").withsat(0.0)
	assert color.css("#0f0") == color.css("#0f0").withsat(1.0)


def test_witha():
	assert color.Color(0x00, 0x63, 0xa8, 0x2a) == color.Color(0x00, 0x63, 0xa8).witha(42)


def test_withlum():
	assert "#000" == str(color.css("#fff").withlum(0))
	assert "#333" == str(color.css("#fff").withlum(0.2))
	assert "#f00" == str(color.css("#f00").withlum(0.2126))
	assert "#0f0" == str(color.css("#0f0").withlum(0.7152))
	assert "#00f" == str(color.css("#00f").withlum(0.0722))


def test_abslum():
	assert "#fff" == str(color.css("#000").abslum(1))
	assert "#fff" == str(color.css("#fff").abslum(0))
	assert "#000" == str(color.css("#fff").abslum(-1))
	assert "#333" == str(color.css("#000").abslum(0.2))


def test_rellum():
	assert "#fff" == str(color.css("#000").rellum(1))
	assert "#fff" == str(color.css("#fff").rellum(0))
	assert "#000" == str(color.css("#fff").rellum(-1))
	assert "#888" == str(color.css("#888").rellum(0))
	assert "#f33" == str(color.css("#f00").rellum(0.2))
	assert "#3f3" == str(color.css("#0f0").rellum(0.2))
	assert "#33f" == str(color.css("#00f").rellum(0.2))


def test_invert():
	assert "#000" == str(color.css("#000").invert(0))
	assert "#333" == str(color.css("#000").invert(0.2))
	assert "#fff" == str(color.css("#000").invert(1))
	assert "#fff" == str(color.css("#000").invert())
	assert "#fff" == str(color.css("#fff").invert(0))
	assert "#ccc" == str(color.css("#fff").invert(0.2))
	assert "#000" == str(color.css("#fff").invert(1))
	assert "#000" == str(color.css("#fff").invert())
	assert "#0ff" == str(color.css("#f00").invert())
	assert "#f0f" == str(color.css("#0f0").invert())
	assert "#ff0" == str(color.css("#00f").invert())


def test_rgb():
	assert color.Color(0x33, 0x66, 0x99, 0xcc).rgb() == (0.2, 0.4, 0.6)


def test_rgba():
	assert color.Color(0x33, 0x66, 0x99, 0xcc).rgba() == (0.2, 0.4, 0.6, 0.8)


def test_combine():
	assert color.Color(0x12, 0x34, 0x56).combine(r=0x78) == (0x78, 0x34, 0x56, 0xff)
	assert color.Color(0x12, 0x34, 0x56).combine(g=0x78) == (0x12, 0x78, 0x56, 0xff)
	assert color.Color(0x12, 0x34, 0x56).combine(b=0x78) == (0x12, 0x34, 0x78, 0xff)
	assert color.Color(0x12, 0x34, 0x56).combine(a=0x78) == (0x12, 0x34, 0x56, 0x78)


def test_mul():
	assert 2*color.Color(0x12, 0x34, 0x56) == color.Color(0x24, 0x68, 0xac)
	assert color.Color(0x12, 0x34, 0x56)*2 == color.Color(0x24, 0x68, 0xac)


def test_truediv():
	assert color.Color(0x24, 0x68, 0xac)/2 == color.Color(0x12, 0x34, 0x56)


def test_floordiv():
	assert color.Color(0x25, 0x69, 0xad)//2 == color.Color(0x12, 0x34, 0x56)


def test_mod():
	assert color.Color(0x80, 0x80, 0x80) % color.Color(0xff, 0xff, 0xff) == color.Color(0x80, 0x80, 0x80)
	assert color.Color(0x80, 0x80, 0x80, 0x00) % color.Color(0xff, 0xff, 0xff) == color.Color(0xff, 0xff, 0xff)
	assert color.Color(0x80, 0x80, 0x80, 0x80) % color.Color(0xff, 0xff, 0xff) == color.Color(0xbf, 0xbf, 0xbf)


def test_css():
	assert color.Color(0x00, 0x00, 0x00) == color.css('black')
	assert color.Color(0xff, 0xff, 0xff) == color.css('white')
	assert color.Color(0x11, 0x22, 0x33) == color.css('#123')
	assert color.Color(0x11, 0x22, 0x33, 0x44) == color.css('#1234')
	assert color.Color(0x12, 0x34, 0x56) == color.css('#123456')
	assert color.Color(0x12, 0x34, 0x56, 0x78) == color.css('#12345678')
	assert color.Color(0x11, 0x33, 0x66) == color.css('rgb(17, 20%, 40%)')
	assert color.Color(0x11, 0x33, 0x66, 0x99) == color.css('rgba(17, 20%, 40%, 0.6)')
	assert color.Color(0x11, 0x33, 0x66, 0x99) == color.css('rgba(17, 20%, 40%, 60%)')
	with pytest.raises(ValueError):
		color.css('bad')
	assert color.Color(0x11, 0x22, 0x33) == color.css('bad', color.Color(0x11, 0x22, 0x33))


def test_mix():
	black = color.Color(0x00, 0x00, 0x00)
	white = color.Color(0xff, 0xff, 0xff)
	red = color.Color(0xff, 0x00, 0x00)
	green = color.Color(0x00, 0xff, 0x00)
	blue = color.Color(0x00, 0x00, 0xff)
	unblack = color.Color(0x00, 0x00, 0x00, 0x00)

	assert color.Color(0xaa, 0xaa, 0xaa) == color.mix(black, white, white)
	assert color.Color(0x55, 0x55, 0x55) == color.mix(black, black, white)
	assert color.Color(0xaa, 0xaa, 0xaa, 0xaa) == color.mix(unblack, white, white)
	assert color.Color(0xaa, 0xaa, 0xaa) == color.mix(black, 2, white)
	assert color.Color(0x11, 0x22, 0xcc) == color.mix(red, 2, green, 12, blue)
