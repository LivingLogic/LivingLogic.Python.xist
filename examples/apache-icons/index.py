#! /usr/bin/env python

import httpdapi

from xist import xsc,html,specials

import glob
import os

cols = 6

class RequestHandler(httpdapi.RequestHandler):
	def Content(self):
		xsc.xsc.pushURL("/icons/") # from now on (until popURL() is called) all URLs will be relative to /icons

		e = xsc.Frag()

		collect = xsc.Frag()
		i = 0

		files = glob.glob("*.gif")
		files.sort()

		for file in files:
			collect.append(html.td(html.img(src = file),html.br(),file,align="center")) # src is relative to the top of the URL stack
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
				html.link(rel="stylesheet",type="text/css",href="icons.css") # href is relative to the top of the URL stack
			),
			html.body(
				specials.plaintable(e)
			)
		)

		s = e.asHTML().asString(XHTML=0)

		xsc.xsc.popURL() # don't forget to call popURL(), otherwise the URL stack will be messed up.

		return s
