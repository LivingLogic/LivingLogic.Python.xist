#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2004 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2004 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
This modules contains the base class for the converter objects used in the call to the
<pyref module="ll.xist.xsc" class="Node" method="convert"><method>convert</method></pyref> method.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

import xsc


class ConverterState(object):
	def __init__(self, node, root, mode, stage, target, lang, makeaction, maketarget):
		self.node = node
		self.root = root
		self.mode = mode
		self.stage = stage
		if target is None:
			from ll.xist.ns import html
			target = html
		self.target = target
		self.lang = lang
		self.makeaction = makeaction
		self.maketarget = maketarget


def parselang(lang):
	"""
	Parse an <lit>Accept-Language</lit> header into a dictionary mapping
	language codes to quality values.
	"""
	result = {}
	for part in lang.split(","):
		parts = part.split(";", 1)
		qual = 1.0
		if len(parts) == 2 and parts[1].startswith("q="):
			try:
				qual = float(parts[1][2:])
			except ValueError:
				qual = 0.01
		result[parts[0]] = qual
	return result


def formatlang(lang):
	"""
	Format a dictionary mapping language codes to quality values into an
	<lit>Accept-Language</lit> header.
	"""
	fields = []
	for (lang, qual) in lang.iteritems():
		if qual <= 0.0:
			continue
		elif qual == 1.0:
			field = lang
		else:
			field = "%s;q=%s" % (lang, ("%.8f" % qual).rstrip("0"))
		fields.append((-qual, field))
	fields.sort()
	return ",".join([field for (qual, field) in fields]) # FIXME: Use a GE in 2.4


class Converter(object):
	"""
	<par>An instance of this class is passed around in calls to the
	<pyref module="ll.xist.xsc" class="Node" method="convert"><method>convert</method></pyref> method.
	This instance can be used when some element needs to keep state across a nested convert call.
	A typical example are nested chapter/subchapter elements with automatic numbering.
	For an example see the element <pyref module="ll.xist.ns.doc" class="section"><class>ll.xist.ns.doc.section</class></pyref>.</par>
	"""
	def __init__(self, node=None, root=None, mode=None, stage=None, target=None, lang=None, makeaction=None, maketarget=None):
		"""
		<par>Create a <class>Converter</class>.</par>
		<par>Arguments are used to initialize the <class>Converter</class> properties of the
		same name.</par>
		"""
		self.states = [ ConverterState(node=node, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, maketarget=maketarget)]
		self.contexts = {}

	def __getnode(self):
		return self.states[-1].node

	def __setnode(self, node):
		self.states[-1].node = node

	def __delnode(self):
		self.states[-1].node = None

	node = property(
		__getnode,
		__setnode,
		__delnode,
		"""
		<par>The root node for which conversion has been called. This is automatically set by the
		<pyref module="ll.xist.xsc" class="Node" method="conv"><method>conv</method></pyref> method.</par>
		"""
	)

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
		<par>The root &url; for the conversion. Resolving &url;s during the conversion process should be done
		relative to <lit>root</lit>.</par>
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
		<par>The conversion mode. This corresponds directy with the mode in &xslt;.
		The default is <lit>None</lit>.</par>
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
		<par>If your conversion is done in multiple steps or stages you can use this property
		to specify in which stage the conversion process currently is. The default is
		<lit>"deliver"</lit>.</par>
		"""
	)

	def __gettarget(self):
		if self.states[-1].target is None:
			from ll.xist.ns import html
			return html
		else:
			return self.states[-1].target

	def __settarget(self, target):
		self.states[-1].target = target

	def __deltarget(self):
		self.states[-1].target = None

	target = property(
		__gettarget,
		__settarget,
		__deltarget,
		"""
		<par>Specifies the conversion target. This must be a
		<pyref module="ll.xist.xsc" class="Namespace"><class>Namespace</class></pyref> subclass.</par>
		"""
	)

	def bestlang(self, havelangs=None, default=None):
		"""
		Return the best language. <arg>havelangs</arg> specifies the language
		provided by the document as a &http; <lit>Accept-Language</lit> header
		string or a mapping from language codes to quality values. If
		<arg>havelangs</arg> is <lit>None</lit> the best language from
		<lit><self/>.lang</lit> is returned. If <lit><self/>.lang</lit> is
		<lit>None</lit> the best language from <arg>havelangs</arg> is returned.
		If both are <lit>None</lit>, <lit>default</lit> will be returned.
		"""
		def bestfromone(langs):
			if langs is not None:
				if isinstance(langs, basestring):
					langs = parselang(langs)
				items = [(qual, lang) for (lang, qual) in langs.iteritems()]
				if items:
					items.sort()
					return items[-1][-1]
			return default

		wantlangs = self.lang
		if wantlangs is None: # ignore target languages
			return bestfromone(havelangs)
		elif havelangs is None: # ignore document languages
			return bestfromone(wantlangs)

		wantlangs = parselang(wantlangs)
		if isinstance(havelangs, basestring):
			havelangs = parselang(havelangs)
		items = []
		for (lang, qual) in havelangs.items():
			if lang in wantlangs:
				items.append((1, qual*wantlangs[lang], lang))
			elif "*" in wantlangs:
				items.append((1, qual*wantlangs["*"], lang))
			else:
				items.append((0, qual, lang)) # add available languages as a fallback
		if items:
			items.sort()
			return items[-1][-1]
		return default

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
		<par>The target language. The default is <lit>None</lit>. This may be
		a string in the style of the &http; <lit>Accept-Language</lit> header
		or a simple language code (like <lit>"en"</lit> etc.).</par>
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
		<par>If an &xist; conversion is done by an <pyref module="ll.make" class="XISTAction"><class>XISTAction</class></pyref>
		this property will hold the action object during that conversion. If you're not using the
		<pyref module="ll.make"><module>make</module></pyref> module you can simply ignore this property. The default is <lit>None</lit>.</par>
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
		<par>If an &xist; conversion is done by an <pyref module="ll.make" class="XISTAction"><class>XISTAction</class></pyref>
		this property will hold the <pyref module="ll.make" class="Target"><class>Target</class></pyref> object during that conversion.
		If you're not using the <pyref module="ll.make"><module>make</module></pyref> module you can simply ignore this property.
		The default is <lit>None</lit>.</par>
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
		<par>If an &xist; conversion is done by an <pyref module="ll.make" class="XISTAction"><class>XISTAction</class></pyref>
		this property will hold the <pyref module="ll.make" class="Project"><class>Project</class></pyref> object during that conversion.
		If you're not using the <pyref module="ll.make"><module>make</module></pyref> module you can simply ignore this property.
		"""
	)

	def push(self, node=None, root=None, mode=None, stage=None, target=None, lang=None, makeaction=None, maketarget=None):
		self.lastnode = None
		if node is None:
			node = self.node
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
		self.states.append(ConverterState(node=node, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, maketarget=maketarget))

	def pop(self):
		if len(self.states)==1:
			raise IndexError("can't pop last state")
		state = self.states.pop()
		self.lastnode = state.node
		return state

	def __getitem__(self, obj):
		"""
		<par>Return a context object for <arg>obj</arg>, which should be the
		class object of an element type. Every element type that defines its own
		<pyref module="ll.xist.xsc" class="Element.Context"><class>Context</class></pyref>
		class gets a unique instance of this class. This instance will be creates
		on the first access and the element can store information there that needs
		to be available across calls to
		<pyref module="ll.xist.xsc" class="Node" method="convert"><method>convert</method></pyref>.</par>
		"""
		contextclass = obj.Context
		# don't use setdefault(), as constructing the Context object might involve some overhead
		try:
			return self.contexts[contextclass]
		except KeyError:
			return self.contexts.setdefault(contextclass, contextclass())

	# XPython support
	def __enter__(self):
		self.push(node=xsc.Frag())

	# XPython support
	def __leave__(self):
		self.pop()
		self.lastnode = self.lastnode.convert(self)
