#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# This script requires XPython
# (see http://codespeak.net/svn/user/hpk/talks/xpython-talk.txt)

import os
import glob

from ll.xist import xsc, converters
from ll.xist.ns import html, htmlspecials, meta

cols = 6

c = converters.Converter()
<c>:
	<html.html()>:
		<html.head()>:
			xsc.append(
				meta.contenttype(),
				html.title("All icons"),
				html.link(rel="stylesheet", type="text/css", href="/icons/icons.css")
			)
		<html.body()>:
			<htmlspecials.plaintable()>:
				collect = xsc.Frag()
				i = 0

				files = glob.glob("*.gif")
				files.sort()

				for file in files:
					collect.append(html.td(htmlspecials.autoimg(src=("/icons/", file)), html.br(), file, align="center"))
					i = i + 1
					if i == cols:
						xsc.append(html.tr(collect))
						collect = xsc.Frag()
						i = 0
				if collect:
					xsc.append(html.tr(collect))


s = c.lastnode.asBytes(encoding="us-ascii", xhtml=0)

print "Content-Type: text/html"
print
print s
