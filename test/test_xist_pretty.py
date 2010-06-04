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
		(html.p(u"apple", u"tree"), b"<p>appletree</p>"),
		(html.p(u"apple", html.br(), u"tree"), b"<p>apple<br />tree</p>"),
		(html.p(php.php(u"apple")), b"<p>\n\t<?php apple?>\n</p>"),
		(html.p(php.php(u"apple"), u"tree"), b"<p><?php apple?>tree</p>"),
		(
			html.div(2*html.p(u"apple", u"tree"), html.br()),
			b"<div>\n\t<p>appletree</p>\n\t<p>appletree</p>\n\t<br />\n</div>"
		),
		(
			html.div(
				php.php(u"apple"),
				html.p(u"apple", u"tree"),
				html.div(
					html.p(u"apple"),
					html.p(u"tree"),
				),
				html.br()
			),
			b"<div>\n\t<?php apple?>\n\t<p>appletree</p>\n\t<div>\n\t\t<p>apple</p>\n\t\t<p>tree</p>\n\t</div>\n\t<br />\n</div>"
		),
	]
	for (got, exp) in tests:
		yield check, got, exp
