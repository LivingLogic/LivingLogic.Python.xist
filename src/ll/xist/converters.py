# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
This modules contains the base class for the converter objects used in the call to the
<pyref module="ll.xist.xsc" class="Node" method="convert"><meth>convert</meth></pyref> method.
"""


from ll import misc
import xsc


__docformat__ = "xist"


class ConverterState(object):
	def __init__(self, node, root, mode, stage, target, lang, makeaction, makeproject):
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
		self.makeproject = makeproject


class Converter(object):
	"""
	<p>An instance of this class is passed around in calls to the
	<pyref module="ll.xist.xsc" class="Node" method="convert"><meth>convert</meth></pyref> method.
	This instance can be used when some element needs to keep state across a nested convert call.
	A typical example are nested chapter/subchapter elements with automatic numbering.
	For an example see the element <pyref module="ll.xist.ns.doc" class="section"><class>ll.xist.ns.doc.section</class></pyref>.</p>
	"""
	def __init__(self, node=None, root=None, mode=None, stage=None, target=None, lang=None, makeaction=None, makeproject=None):
		"""
		<p>Create a <class>Converter</class>.</p>
		<p>Arguments are used to initialize the <class>Converter</class> properties of the
		same name.</p>
		"""
		self.states = [ ConverterState(node=node, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, makeproject=makeproject)]
		self.contexts = {}

	class node(misc.propclass):
		"""
		<p>The root node for which conversion has been called. This is automatically set by the
		<pyref module="ll.xist.xsc" class="Node" method="conv"><meth>conv</meth></pyref> method.</p>
		"""
		def __get__(self):
			return self.states[-1].node
	
		def __set__(self, node):
			self.states[-1].node = node
	
		def __delete__(self):
			self.states[-1].node = None

	class root(misc.propclass):
		"""
		<p>The root &url; for the conversion. Resolving &url;s during the conversion process should be done
		relative to <lit>root</lit>.</p>
		"""
		def __get__(self):
			return self.states[-1].root
	
		def __set__(self, root):
			self.states[-1].root = root
	
		def __delete__(self):
			self.states[-1].root = None

	class mode(misc.propclass):
		"""
		<p>The conversion mode. This corresponds directly to the mode in &xslt;.
		The default is <lit>None</lit>.</p>
		"""
		def __get__(self):
			return self.states[-1].mode
	
		def __set__(self, mode):
			self.states[-1].mode = mode
	
		def __delete__(self):
			self.states[-1].mode = None

	class stage(misc.propclass):
		"""
		<p>If your conversion is done in multiple steps or stages you can use this property
		to specify in which stage the conversion process currently is. The default is
		<lit>"deliver"</lit>.</p>
		"""
		def __get__(self):
			if self.states[-1].stage is None:
				return "deliver"
			else:
				return self.states[-1].stage
	
		def __set__(self, stage):
			self.states[-1].stage = stage
	
		def __delete__(self):
			self.states[-1].stage = None

	class target(misc.propclass):
		"""
		<p>Specifies the conversion target. This must be a
		namespace module or simiar object.</p>
		"""
		def __get__(self):
			if self.states[-1].target is None:
				from ll.xist.ns import html
				return html.xmlns
			else:
				return self.states[-1].target
	
		def __set__(self, target):
			self.states[-1].target = target
	
		def __delete__(self):
			self.states[-1].target = None

	class lang(misc.propclass):
		"""
		<p>The target language. The default is <lit>None</lit>.</p>
		"""
		def __get__(self):
			return self.states[-1].lang
	
		def __set__(self, lang):
			self.states[-1].lang = lang
	
		def __delete__(self):
			self.states[-1].lang = None

	class makeaction(misc.propclass):
		"""
		<p>If an &xist; conversion is done by an <pyref module="ll.make" class="XISTConvertAction"><class>XISTConvertAction</class></pyref>
		this property will hold the action object during that conversion. If you're not using the
		<pyref module="ll.make"><mod>make</mod></pyref> module you can simply ignore this property. The default is <lit>None</lit>.</p>
		"""
		def __get__(self):
			return self.states[-1].makeaction
	
		def __set__(self, makeaction):
			self.states[-1].makeaction = makeaction
	
		def __delete__(self):
			self.states[-1].makeaction = None

	class makeproject(misc.propclass):
		"""
		<p>If an &xist; conversion is done by an <pyref module="ll.make" class="XISTConvertAction"><class>XISTConvertAction</class></pyref>
		this property will hold the <pyref module="ll.make" class="Project"><class>Project</class></pyref> object during that conversion.
		If you're not using the <pyref module="ll.make"><mod>make</mod></pyref> module you can simply ignore this property.
		"""
		def __get__(self):
			return self.states[-1].makeproject
	
		def __set__(self, makeproject):
			self.states[-1].makeproject = makeproject
	
		def __delete__(self):
			self.states[-1].makeproject = None

	def push(self, node=None, root=None, mode=None, stage=None, target=None, lang=None, makeaction=None, makeproject=None):
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
		if makeproject is None:
			makeproject = self.makeproject
		self.states.append(ConverterState(node=node, root=root, mode=mode, stage=stage, target=target, lang=lang, makeaction=makeaction, makeproject=makeproject))

	def pop(self):
		if len(self.states)==1:
			raise IndexError("can't pop last state")
		state = self.states.pop()
		self.lastnode = state.node
		return state

	def __getitem__(self, obj):
		"""
		<p>Return a context object for <arg>obj</arg>, which should be an
		<pyref module="ll.xist.xsc" class="Node"><class>Node</class></pyref> subclass.
		Each of these classes that defines its own
		<pyref module="ll.xist.xsc" class="Element.Context"><class>Context</class></pyref>
		class gets a unique instance of this class. This instance will be created
		on the first access and the element can store information there that needs
		to be available across calls to
		<pyref module="ll.xist.xsc" class="Node" method="convert"><meth>convert</meth></pyref>.</p>
		"""
		contextclass = obj.Context
		# don't use setdefault(), as constructing the Context object might involve some overhead
		try:
			return self.contexts[contextclass]
		except KeyError:
			context = contextclass()
			self.contexts[contextclass] = context
			return context
