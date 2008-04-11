# -*- coding: utf-8 -*-

## Copyright 2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


try:
	from _helpers import *
except ImportError:
	def escapetext(s):
		return s.replace("&", "&amp;").replace("<", "&lt;").replace("&", "&gt;")

	def escapeattr(s):
		return s.replace("&", "&amp;").replace("<", "&lt;").replace("&", "&gt;").replace("'", "&apos;").replace('"', "&quot;")