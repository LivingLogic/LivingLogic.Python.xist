#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
This modules contains the base class for the converter objects used in the call to the
<pyref module="ll.xist.xsc" class="Node" method="convert"><method>convert</method></pyref> method.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import types

class Context(object):
	"""
	This is an empty class, that can be used by the
	<pyref module="ll.xist.xsc" class="Node" method="convert"><method>convert</method></pyref>
	method to hold element specific data during the convert call. The method
	<pyref class="Converter" method="__getitem__"><method>Converter.__getitem__</method></pyref>
	will return a unique instance of this class.
	"""
	
	def __init__(self):
		pass

class ConverterState(object):
	def __init__(self, root, mode, stage, target, lang, makeaction, maketarget):
		self.root = root
		self.mode = mode
		self.stage = stage
		self.target = target
		self.lang = lang
		self.makeaction = makeaction
		self.maketarget = maketarget

class Converter(object):
	"""
	<doc:par>An instance of this class is passed around in calls to the
	<pyref module="ll.xist.xsc" class="Node" method="convert"><method>convert</method></pyref> method.
	This instance can be used when some element needs to keep state across a nested convert call.
	A typical example are nested chapter/subchapter elements with automatic numbering.
	For an example see the element <pyref module="ll.xist.ns.doc" class="section"><class>ll.xist.ns.doc.section</class></pyref>.</doc:par>
	"""
	def __init__(self, root=None, mode=None, stage=None, target=None, lang=None, makeaction=None, maketarget=None):
		"""
		<doc:par>Create a <class>Converter</class>.</doc:par>
		<doc:par>Arguments are used to initialize the <class>Converter</class> properties of the
		same name.</doc:par>
		"""
		self.states = [ ConverterState(root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, maketarget=maketarget)]
		self.contexts = {}

	def __getroot(self):
		return self.states[-1].root

	def __setroot(self, root):
		self.states[-1].root = root

	def __delroot(self):
		self.states[-1].root = None

	root = property(
		__getroot,
		__setroot,
		__delroot,
		"""
		<doc:par>The conversion mode. This corresponds directy with the mode in &xslt;.
		The default is <lit>None</lit>.</doc:par>
		"""
	)

	def __getmode(self):
		return self.states[-1].mode

	def __setmode(self, mode):
		self.states[-1].mode = mode

	def __delmode(self):
		self.states[-1].mode = None

	mode = property(
		__getmode,
		__setmode,
		__delmode,
		"""
		<doc:par>The conversion mode. This corresponds directy with the mode in &xslt;.
		The default is <lit>None</lit>.</doc:par>
		"""
	)

	def __getstage(self):
		if self.states[-1].stage is None:
			return "deliver"
		else:
			return self.states[-1].stage

	def __setstage(self, stage):
		self.states[-1].stage = stage

	def __delstage(self):
		self.states[-1].stage = None

	stage = property(
		__getstage,
		__setstage,
		__delstage,
		"""
		<doc:par>If your conversion is done in multiple steps or stages you can use this property
		to specify in which stage the conversion process currently is. The default is
		<lit>"deliver"</lit>.</doc:par>
		"""
	)

	def __gettarget(self):
		if self.states[-1].target is None:
			return "html"
		else:
			return self.states[-1].target

	def __settarget(self, target):
		self.states[-1].target = target

	def __deltarget(self):
		self.states[-1].targes = None

	target = property(
		__gettarget,
		__settarget,
		__deltarget,
		"""
		<doc:par>Specifies the conversion target. This could be <lit>"text"</lit>,
		<lit>"html"</lit>, <lit>"wml"</lit>, <lit>"docbook"</lit>
		or anything like that. The default is <lit>"html"</lit>.</doc:par>
		"""
	)

	def __getlang(self):
		return self.states[-1].lang

	def __setlang(self, lang):
		self.states[-1].lang = lang

	def __dellang(self):
		self.states[-1].lang = None

	lang = property(
		__getlang,
		__setlang,
		__dellang,
		"""
		<doc:par>The target language. The default is <lit>None</lit>.</doc:par>
		"""
	)

	def __getmakeaction(self):
		return self.states[-1].makeaction

	def __setmakeaction(self, makeaction):
		self.states[-1].makeaction = makeaction

	def __delmakeaction(self):
		self.states[-1].makeaction = None

	makeaction = property(
		__getmakeaction,
		__setmakeaction,
		__delmakeaction,
		"""
		<doc:par>If an &xist; conversion is done by an <pyref module="ll.make" class="XISTAction"><class>XISTAction</class></pyref>
		this property will hold the action object during that conversion. If you're not using the
		<pyref module="ll.make"><module>make</module></pyref> module you can simply ignore this property. The default is <lit>None</lit>.</doc:par>
		"""
	)

	def __getmaketarget(self):
		return self.states[-1].maketarget

	def __setmaketarget(self, maketarget):
		self.states[-1].maketarget = maketarget

	def __delmaketarget(self):
		self.states[-1].maketarget = None

	maketarget = property(
		__getmaketarget,
		__setmaketarget,
		__delmaketarget,
		"""
		<doc:par>If an &xist; conversion is done by an <pyref module="ll.make" class="XISTAction"><class>XISTAction</class></pyref>
		this property will hold the <pyref module="ll.make" class="Target"><class>Target</class></pyref> object during that conversion.
		If you're not using the <pyref module="ll.make"><module>make</module></pyref> module you can simply ignore this property.
		The default is <lit>None</lit>.</doc:par>
		"""
	)

	def __getmakeproject(self):
		maketarget = self.maketarget
		if maketarget is None:
			return None
		else:
			return maketarget.project

	makeproject = property(
		__getmakeproject,
		None,
		None,
		"""
		<doc:par>If an &xist; conversion is done by an <pyref module="ll.make" class="XISTAction"><class>XISTAction</class></pyref>
		this property will hold the <pyref module="ll.make" class="Project"><class>Project</class></pyref> object during that conversion.
		If you're not using the <pyref module="ll.make"><module>make</module></pyref> module you can simply ignore this property.
		"""
	)

	def push(self, root=None, mode=None, stage=None, target=None, lang=None, makeaction=None, maketarget=None):
		if root is None:
			root = self.root
		if mode is None:
			mode = self.mode
		if stage is None:
			stage = self.stage
		if target is None:
			target = self.target
		if lang is None:
			lang = self.lang
		if makeaction is None:
			makeaction = self.makeaction
		if maketarget is None:
			maketarget = self.maketarget
		self.states.append(ConverterState(root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, maketarget=maketarget))

	def pop(self):
		if len(self.states)==1:
			raise IndexError("can't pop last state")
		return self.states.pop()

	def __getitem__(self, class_):
		"""
		<doc:par>Return a context object that is unique for <arg>class_</arg>,
		which should be the class object of an element type. This means that every element type
		gets its own context and can store information there that needs to be available
		across calls to <pyref module="ll.xist.xsc" class="Node" method="convert"><method>convert</method></pyref>.</doc:par>
		"""
		return self.contexts.setdefault(class_, Context())
