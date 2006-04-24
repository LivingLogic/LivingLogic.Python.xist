#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# This example requires CherryPy: http://www.cherrypy.org/


import sys, os, glob

import cherrypy
from cherrypy.lib import cptools

from ll.xist import xsc, converters
from ll.xist.ns import xml, html, specials, htmlspecials, meta

cols = 6

class Icons(object):
	def __init__(self, directory):
		self.directory = directory

	@cherrypy.expose
	def default(self, *args):
		return cptools.serveFile(os.path.abspath("/".join(args)))

	@cherrypy.expose
	def images(self, filename):
		return cptools.serveFile("%s/%s" % (self.directory, filename))

	@cherrypy.expose
	def index(self):
		table = htmlspecials.plaintable()

		collect = xsc.Frag()
		i = 0

		def isimg(name):
			if name.endswith(".gif") or name.endswith(".jpg") or name.endswith(".png"):
				return os.path.isfile(os.path.join(self.directory, name))
			return False

		names = [name for name in os.listdir(self.directory) if isimg(name)]
		names.sort()

		for name in names:
			collect.append(html.td(htmlspecials.autoimg(src=("/images/", name)), html.br(), name, align="center"))
			i += 1
			if i == cols:
				table.append(html.tr(collect))
				collect = xsc.Frag()
				i = 0
		if collect:
			table.append(html.tr(collect))

		e = xsc.Frag(
			xml.XML10(), "\n",
			html.DocTypeXHTML10transitional(), "\n",
			html.html(
				html.head(
					meta.contenttype(),
					html.title("All images from ", specials.z(self.directory)),
					html.link(rel="stylesheet", type="text/css", href="images.css")
				)
			),
			html.body(table)
		)
		return e.conv().bytes()


directory = "."
if len(sys.argv) > 1:
	directory = sys.argv[1]
cherrypy.root = Icons(directory)
cherrypy.server.start()
