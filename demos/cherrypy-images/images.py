#! /usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

# This example requires CherryPy: http://www.cherrypy.org/


import sys, os, glob

import cherrypy
from cherrypy.lib import cptools

from ll.xist import xsc
from ll.xist.ns import xml, html, doc, htmlspecials, meta

cols = 6

class Icons:
	def __init__(self, directory):
		self.directory = directory

	@cherrypy.expose
	def default(self, *args):
		return cptools.serveFile(os.path.abspath("/".join(args)))

	@cherrypy.expose
	def images(self, filename):
		return cptools.serveFile(f"{self.directory}/{filename}")

	@cherrypy.expose
	def index(self):
		def isimg(name):
			if name.endswith(".gif") or name.endswith(".jpg") or name.endswith(".png"):
				return os.path.isfile(os.path.join(self.directory, name))
			return False

		names = [name for name in os.listdir(self.directory) if isimg(name)]
		names.sort()

		collect = xsc.Frag()
		i = 0

		with xsc.build():
			with xsc.Frag() as e:
				+xml.XML()
				+html.DocTypeXHTML10transitional()
				with html.html():
					with html.head():
						+meta.contenttype()
						+html.title("All images from ", doc.z(self.directory))
						+html.link(rel="stylesheet", type="text/css", href="images.css")
					with html.body():
						with htmlspecials.plaintable():
							for name in names:
								collect.append(html.td(htmlspecials.autoimg(src=("/images/", name)), html.br(), name, align="center"))
								i += 1
								if i == cols:
									+html.tr(collect)
									collect = xsc.Frag()
									i = 0
							if collect:
								+html.tr(collect)

		return e.conv().bytes()


directory = "."
if len(sys.argv) > 1:
	directory = sys.argv[1]
cherrypy.root = Icons(directory)
cherrypy.server.start()
