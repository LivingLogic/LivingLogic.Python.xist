#! /usr/bin/env python
# -*- coding: Latin-1 -*-

import os
import glob

from ll.xist import xsc
from ll.xist.ns import html, specials

cols = 6

e = xsc.Frag()

collect = xsc.Frag()
i = 0

files = glob.glob("*.gif")
files.sort()

for file in files:
	collect.append(html.td(specials.autoimg(src=("/icons/", file)), html.br(), file, align="center"))
	i = i + 1
	if i == cols:
		e.append(html.tr(collect))
		collect = xsc.Frag()
		i = 0
if len(collect):
	e.append(html.tr(collect))

e = html.html(
	html.head(
		html.title("All icons"),
		html.link(rel="stylesheet", type="text/css", href="/icons/icons.css")
	),
	html.body(
		specials.plaintable(e)
	)
)

s = e.conv().asBytes(encoding="us-ascii", XHTML=0)

print "Content-Type: text/html"
print
print s
