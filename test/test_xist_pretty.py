#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 1999-2011 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2011 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll.xist import xsc
from ll.xist.ns import html, php, ul4


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
		(
			html.ul(
				ul4.for_("name in names"),
				html.li(
					ul4.printx("name"),
				),
				ul4.end("for"),
			),
			b"<ul>\n\t<?for name in names?>\n\t\t<li>\n\t\t\t<?printx name?>\n\t\t</li>\n\t<?end for?>\n</ul>"
		),
		(
			xsc.Frag(
				ul4.if_("n == 0"),
					html.span("zero"),
				ul4.elif_("n == 1"),
					html.span("one"),
				ul4.else_(),
					html.span("many"),
				ul4.end("if"),
			),
			b"<?if n == 0?>\n\t<span>zero</span>\n<?elif n == 1?>\n\t<span>one</span>\n<?else ?>\n\t<span>many</span>\n<?end if?>"
		),
		(
			xsc.Frag(
				ul4.def_("spam"),
					ul4.printx("eggs"),
				ul4.end("def"),
			),
			b"<?def spam?>\n\t<?printx eggs?>\n<?end def?>"
		),
	]
	for (got, exp) in tests:
		yield check, got, exp
