#! /usr/bin/env/python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2006 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2006 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


from ll import url
from ll.xist import cssparsers


def test_parse():
	csshandler = cssparsers.ParseHandler()
	s = "div {border: 0px;}"
	assert csshandler.parseString(s) == s

	s = "div {background-image: url(gurk.gif);}"
	assert csshandler.parseString(s) == s

	s = "div {background-image: url(gurk.gif);}"
	assert csshandler.parseString(s, base="root:hurz/index.css") == \
	       "div {background-image: url(root:hurz/gurk.gif);}"


def test_publish():
	csshandler = cssparsers.PublishHandler()
	s = "div {border: 0px;}"
	assert csshandler.parseString(s) == s

	s = "div {background-image: url(gurk.gif);}"
	assert csshandler.parseString(s) == s


	s = "div {background-image: url(root:hurz/gurk.gif);}"
	assert csshandler.parseString(s, base="root:hurz/index.css") == \
	       "div {background-image: url(gurk.gif);}"


def test_collect():
	csshandler = cssparsers.CollectHandler()
	s = """
		div.c1 {background-image: url(root:hurz/hinz.gif);}
		div.c1 {background-image: url(root:hurz/kunz.gif);}
	"""
	csshandler.parseString(s)
	assert len(csshandler.urls) == 2
	assert csshandler.urls[0] == url.URL("root:hurz/hinz.gif")
	assert csshandler.urls[1] == url.URL("root:hurz/kunz.gif")
