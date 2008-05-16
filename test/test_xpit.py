#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2005/2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005/2006 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import py.test

from ll import xpit


def test_plain():
	assert xpit.convert("foo") == "foo"
	assert xpit.convert("foo<?>bar") == "foo<?bar"


def test_expr():
	assert xpit.convert("<?= a+b?>", globals=dict(a=17, b=23)) == "40"


def test_if():
	assert xpit.convert("<?if a==17?>gurk<?else?>hurz<?endif?>", globals=dict(a=17, b=23)) == "gurk"
	assert xpit.convert("<?if a>0?>foo<?elif a==0?>bar<?else?>baz<?endif?>", globals=dict(a=17)) == "foo"


def test_nestedif():
	code = """
	<?if a==16?>
		a==16
	<?elif a==17?>
		a==17
		<?if b==17?>
			b==17
		<?else?>
			b!=17
		<?endif?>
	<?else?>
		a != (16, 17)
	<?endif?>
	"""
	assert "".join(xpit.convert(code, globals=dict(a=17, b=23)).split()) == "a==17b!=17"
