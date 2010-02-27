#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll.xist import xsc
from ll.xist.ns import html, php


def test_pretty():
	def check(node, result):
		assert node.pretty().bytes() == result

	tests = [
		(html.p("apple", "tree"), "<p>appletree</p>"),
		(html.p("apple", html.br(), "tree"), "<p>apple<br />tree</p>"),
		(html.p(php.php("apple")), "<p>\n\t<?php apple?>\n</p>"),
		(html.p(php.php("apple"), "tree"), "<p><?php apple?>tree</p>"),
		(
			html.div(2*html.p("apple", "tree"), html.br()),
			"<div>\n\t<p>appletree</p>\n\t<p>appletree</p>\n\t<br />\n</div>"
		),
		(
			html.div(
				php.php("apple"),
				html.p("apple", "tree"),
				html.div(
					html.p("apple"),
					html.p("tree"),
				),
				html.br()
			),
			"<div>\n\t<?php apple?>\n\t<p>appletree</p>\n\t<div>\n\t\t<p>apple</p>\n\t\t<p>tree</p>\n\t</div>\n\t<br />\n</div>"
		),
	]
	for (got, exp) in tests:
		yield check, got, exp
