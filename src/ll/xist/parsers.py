# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<p>This file contains everything you need to parse &xist; objects from files,
strings, &url;s etc.</p>
"""


from __future__ import with_statement

import sys, os, os.path, warnings, cStringIO, codecs, pyexpat, contextlib

from xml.parsers import expat

from ll import url, xml_codec
from ll.xist import xsc, utils, sgmlop
from ll.xist.ns import html


__docformat__ = "xist"


class Parser(object):
	def __init__(self):
		self.application = None

	def begin(self, application):
		self.application = application

	def end(self):
		self.application = None

	def feed(self, data, final):
		pass


class SGMLOPParser(Parser):
	def __init__(self, encoding=None):
		Parser.__init__(self)
		self.encoding = encoding
		self._decoder = None
		self._parser = None

	def begin(self, application):
		Parser.begin(self, application)
		self._decoder = codecs.getincrementaldecoder("xml")(self.encoding)
		if self._parser is not None:
			self._parser.register(None)
		self._parser = sgmlop.XMLParser()
		self._parser.register(self)

	def feed(self, data, final):
		self._parser.feed(self._decoder.decode(data, final))

	def end(self):
		Parser.end(self)
		self._parser.close()
		if self._parser is not None:
			self._parser.register(None)
			self._parser = None
		self._decoder = None

	def handle_comment(self, data):
		self.application.handle_comment(data, None, None)

	def handle_data(self, data):
		self.application.handle_data(data, None, None)

	def handle_cdata(self, data):
		self.application.handle_cdata(data, None, None)

	def handle_proc(self, target, data):
		self.application.handle_proc(target, data, None, None)

	def handle_entityref(self, name):
		self.application.handle_entityref(name, None, None)

	def handle_enterstarttag(self, name):
		self.application.handle_enterstarttag(name, None, None)

	def handle_leavestarttag(self, name):
		self.application.handle_leavestarttag(name, None, None)

	def handle_enterattr(self, name):
		self.application.handle_enterattr(name, None, None)

	def handle_leaveattr(self, name):
		self.application.handle_leaveattr(name, None, None)

	def handle_endtag(self, name):
		self.application.handle_endtag(name, None, None)


class ExpatParser(Parser):
	def __init__(self, encoding=None, transcode=False):
		Parser.__init__(self)
		self.encoding = encoding
		self._parser = None
		self._decoder = None
		self._encoder = None
		self._transcode = transcode

	def begin(self, application):
		Parser.begin(self, application)
		self._parser = expat.ParserCreate(self.encoding)
		self._parser.buffer_text = True
		self._parser.ordered_attributes = True
		self._parser.UseForeignDTD(True)
		self._parser.CharacterDataHandler = self.handle_data
		self._parser.StartElementHandler = self.handle_startelement
		self._parser.EndElementHandler = self.handle_endelement
		self._parser.ProcessingInstructionHandler = self.handle_proc
		self._parser.CommentHandler = self.handle_comment
		self._parser.DefaultHandler = self.handle_default
		if self._transcode:
			self._decoder = codecs.getincrementaldecoder("xml")()
			self._encoder = codecs.getincrementalencoder("xml")(encoding="utf-8")

	def end(self):
		Parser.end(self)
		self._parser = None
		self._encoder = None
		self._decoder = None

	def handle_default(self, data):
		if data.startswith("&") and data.endswith(";"):
			self.application.handle_entityref(data[1:-1], self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)

	def handle_comment(self, data):
		self.application.handle_comment(data, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)

	def handle_data(self, data):
		self.application.handle_data(data, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)

	def handle_startelement(self, name, attrs):
		self.application.handle_enterstarttag(name, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)
		for i in xrange(0, len(attrs), 2):
			key = attrs[i]
			self.application.handle_enterattr(key, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)
			self.application.handle_data(attrs[i+1], self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)
			self.application.handle_leaveattr(key, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)
		self.application.handle_leavestarttag(name, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)

	def handle_endelement(self, name):
		self.application.handle_endtag(name, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)

	def handle_proc(self, target, data):
		self.application.handle_proc(target, data, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)

	def feed(self, data, final):
		if self._transcode:
			data = self._decoder.decode(data, final)
			data = self._encoder.encode(data, final)
		self._parser.Parse(data, final)


class LaxAttrs(xsc.Attrs):
	@classmethod
	def _allowedattrkey(cls, name, xmlns=None):
		if xmlns is not None:
			xmlns = xsc.nsname(xmlns)
			try:
				return (xsc.getpoolstack()[-1].attrname(name, xmlns), xmlns) # ask namespace about global attribute
			except xsc.IllegalAttrError:
				return (name, xmlns)
		return name

	@classmethod
	def _allowedattrkey_xml(cls, name, xmlns=None):
		if xmlns is not None:
			xmlns = xsc.nsname(xmlns)
			try:
				return (xsc.getpoolstack()[-1].attrname_xml(name, xmlns), xmlns) # ask namespace about global attribute
			except xsc.IllegalAttrError:
				return (name, xmlns)
		return name

	def set(self, name, xmlns=None, value=None):
		attr = self.allowedattr(name, xmlns)(value)()
		attr.xmlname = name
		dict.__setitem__(self, self._allowedattrkey(name, xmlns), attr) # put the attribute in our dict
		return attr

	def set_xml(self, name, xmlns=None, value=None):
		attr = self.allowedattr_xml(name, xmlns)(value)()
		attr.xmlname = name
		dict.__setitem__(self, self._allowedattrkey_xml(name, xmlns), attr) # put the attribute in our dict
		return attr

	@classmethod
	def allowedattr(cls, name, xmlns):
		if xmlns is not None:
			xmlns = xsc.nsname(xmlns)
			try:
				return xsc.getpoolstack()[-1].attrclass(name, xmlns) # return global attribute
			except xsc.IllegalAttrError:
				return xsc.TextAttr
		else:
			return xsc.TextAttr

	@classmethod
	def allowedattr(cls, name, xmlns, xml=False):
		if xmlns is not None:
			xmlns = xsc.nsname(xmlns)
			try:
				return xsc.getpoolstack()[-1].attrclass_xml(name, xmlns) # return global attribute
			except xsc.IllegalAttrError:
				return xsc.TextAttr
		else:
			return xsc.TextAttr


class LaxElement(xsc.Element):
	register = None
	Attrs = LaxAttrs


class Builder(object):
	"""
	<p>It is the job of a <class>Builder</class> to create the object tree from
	the events generated by the underlying parser.</p>
	"""

	def __init__(self, parser=None, prefixes=None, tidy=False, loc=True, validate=True, encoding=None, pool=None):
		"""
		<p>Create a new <class>Builder</class> instance.</p>

		<p>Arguments have the following meaning:</p>
		<dl>
		<dt><arg>parser</arg></dt><dd>an instance of the
		<pyref class="Parser"><class>Parser</class></pyref> class (or any object
		that provides the appropriate interface).</dd>

		<dt><arg>prefixes</arg></dt><dd>a mapping that maps namespace
		prefixes to namespace names/modules) (or lists of namespace names/modules).
		This is used to preinitialize the namespace prefix mapping.</dd>

		<dt><arg>tidy</arg></dt><dd>If <arg>tidy</arg> is true,
		<a href="http://xmlsoft.org/">libxml2</a>'s &html; parser will be
		used for parsing broken &html;.</dd>

		<dt><arg>loc</arg></dt><dd>Should location information be attached
		to the generated nodes?</dd>

		<dt><arg>validate</arg></dt><dd>Should the parsed &xml; nodes be
		validated after parsing?</dd>

		<dt><arg>encoding</arg></dt><dd>The default encoding to use, when the
		source doesn't provide an encoding. The default <lit>None</lit> results in
		the encoding being detected from the &xml; itself.</dd>

		<dt><arg>pool</arg></dt><dd>A <pyref module="ll.xist.xsc" class="Pool"><class>ll.xist.xsc.Pool</class></pyref>
		object which will be used for instantiating all nodes during parsing.</dd>
		</dl>
		"""
		self.parser = parser

		self.pool = (pool if pool is not None else xsc.getpoolstack()[-1])

		# the currently active prefix mapping (will be replaced once xmlns attributes are encountered)
		if prefixes is None:
			# make all currently known namespaces available without prefix
			# (if there are elements with colliding namespace, which one will be used is random (based on dict iteration order))
			self.prefixes = {None: list(set(c.xmlns for c in self.pool.elements()))}
		else:
			self.prefixes = {}
			for (prefix, xmlns) in prefixes.iteritems():
				if prefix is not None and not isinstance(prefix, basestring):
					raise TypeError("Prefix must be None or string, not %r" % prefix)
				if isinstance(xmlns, (list, tuple)):
					self.prefixes[prefix] = map(xsc.nsname, xmlns)
				else:
					self.prefixes[prefix] = xsc.nsname(xmlns)

		self.url = None
		self.tidy = tidy
		self.loc = loc
		self.validate = validate
		self.encoding = encoding
		self._attr = None
		self._attrs = None

	def _parseHTML(self, data, base, sysid, encoding):
		"""
		Internal helper method for parsing &html; via <mod>libxml2</mod>.
		"""
		import libxml2 # This requires libxml2 (see http://www.xmlsoft.org/)

		def decode(s):
			try:
				return s.decode("utf-8")
			except UnicodeDecodeError:
				return s.decode("iso-8859-1")

		def toxsc(node):
			if node.type == "document_html":
				newnode = xsc.Frag()
				child = node.children
				while child is not None:
					newnode.append(toxsc(child))
					child = child.next
			elif node.type == "element":
				name = decode(node.name).lower()
				try:
					newnode = self.pool.element_xml(name, html)
					if self.loc:
						newnode.startloc = xsc.Location(url=self.base, line=node.lineNo())
				except xsc.IllegalElementError:
					newnode = xsc.Frag()
				else:
					attr = node.properties
					while attr is not None:
						name = decode(attr.name).lower()
						if attr.content is None:
							content = u""
						else:
							content = decode(attr.content)
						try:
							attrnode = newnode.attrs.set_xml(name, value=content)
						except xsc.IllegalAttrError:
							pass
						else:
							attrnode = attrnode.parsed(self)
							newnode.attrs.set_xml(name, value=attrnode)
						attr = attr.next
					newnode.attrs = newnode.attrs.parsed(self)
					newnode = newnode.parsed(self, start=True)
				child = node.children
				while child is not None:
					newnode.append(toxsc(child))
					child = child.next
				if isinstance(node, xsc.Element): # if we did recognize the element, otherwise we're in a Frag
					newnode = newnode.parsed(self, start=False)
			elif node.type in ("text", "cdata"):
				newnode = self.pool.text(decode(node.content))
				if self.loc:
					newnode.startloc = xsc.Location(url=self.base, line=node.lineNo())
			elif node.type == "comment":
				newnode = self.pool.comment(decode(node.content))
				if self.loc:
					newnode.startloc = xsc.Location(url=self.base, line=node.lineNo())
			else:
				newnode = xsc.Null
			return newnode

		self.base = base

		try:
			olddefault = libxml2.lineNumbersDefault(1)
			doc = libxml2.htmlReadMemory(data, len(data), sysid, encoding, 0x160)
			try:
				node = toxsc(doc)
			finally:
				doc.freeDoc()
		finally:
			libxml2.lineNumbersDefault(olddefault)
		return node

	def _begin(self, base=None, encoding=None):
		# Internal helper: create a parser and initialize the stack
		if self.parser is None:
			parser = SGMLOPParser(encoding=encoding)
		else:
			parser = self.parser
		self.base = url.URL(base)
		# XIST nodes do not have a parent link, therefore we have to store the
		# active path through the tree in a stack (which we call ``_nesting``)
		# together with the namespace prefixes defined by each element.
		#
		# After we've finished parsing, the ``Frag`` that we put at the bottom of
		# the stack will be our document root.
		self._nesting = [ (xsc.Frag(), self.prefixes) ]
		parser.begin(self)
		return parser

	def _end(self, parser):
		# Internal helper: finish parsing and return the root node
		parser.end()
		return self._nesting[0][0]

	def parsestring(self, data, base=None, encoding=None):
		"""
		Parse the string <arg>data</arg> (<class>str</class> or <class>unicode</class>)
		into an &xist; tree. <arg>base</arg> is the base &url; for the parsing
		process, <arg>encoding</arg> can be used to force the parser to use the
		specified encoding.
		"""
		self.url = url.URL(base if base is not None else "STRING")
		if isinstance(data, unicode):
			encoding = "utf-8"
			data = data.encode(encoding)
		if self.tidy:
			return self._parseHTML(data, base=base, sysid=str(self.url), encoding=encoding)
		parser = self._begin(base=base, encoding=encoding)
		parser.feed(data, True)
		return self._end(parser)

	def parseiter(self, iterable, base=None, encoding=None):
		"""
		Parse the input from the iterable <arg>iterable<arg> (which must produce
		the input in chunks of bytes) into an &xist; tree. <arg>base</arg> is the
		base &url; for the parsing process, <arg>encoding</arg> can be used to
		force the parser to use the specified encoding.
		"""
		self.url = url.URL(base if base is not None else "ITER")
		if self.tidy:
			return self._parseHTML("".join(iterable), base=base, sysid=str(self.url), encoding=encoding)
		parser = self._begin(base=base, encoding=encoding)
		for chunk in iterable:
			parser.feed(chunk, False)
		parser.feed("", True)
		return self._end(parser)

	def parsestream(self, stream, base=None, encoding=None, bufsize=8192):
		"""
		Parse &xml; input from the stream <arg>stream</arg>. <arg>base</arg> is
		the base &url; for the parsing process, <arg>encoding</arg> can be used
		to force the parser to use the specified encoding. <arg>bufsize</arg> is
		the buffer size used from reading the stream in blocks.
		"""
		self.url = url.URL(base if base is not None else "STREAM")
		parser = self._begin(base=base, encoding=encoding)
		if self.tidy:
			return self._parseHTML(stream.read(), base=base, sysid=str(self.url), encoding=encoding)
		while True:
			data = stream.read(bufsize)
			final = not data
			parser.feed(data, final)
			if final:
				return self._end(parser)

	def parsefile(self, filename, base=None, encoding=None, bufsize=8192):
		"""
		Parse &xml; input from the file named <arg>filename</arg>. <arg>base</arg>
		is the base &url; for the parsing process (defaulting to <arg>filename</arg>
		if not specified), <arg>encoding</arg> can be used to force the parser to
		use the specified encoding. <arg>bufsize</arg> is the buffer size used
		from reading the stream in blocks.
		"""
		self.url = url.File(filename)
		if base is None:
			base = self.url
		filename = os.path.expanduser(filename)
		with contextlib.closing(open(filename, "rb")) as stream:
			if self.tidy:
				return self._parseHTML(stream.read(), base=base, sysid=str(self.url), encoding=encoding)
			parser = self._begin(base=base, encoding=encoding)
			while True:
				data = stream.read(bufsize)
				final = not data
				parser.feed(data, final)
				if final:
					return self._end(parser)

	def parseurl(self, name, base=None, encoding=None, bufsize=8192, *args, **kwargs):
		"""
		Parse &xml; input from the &url; <arg>name</arg> which might be a string
		or an <pyref module="ll.url" class="URL"><class>URL</class></pyref> object
		into an &xist; tree. <arg>base</arg> is the base &url; for the parsing process
		(defaulting to the final &url; of the response (i.e. including redirects)).
		<arg>encoding</arg> can be used to force the parser to use the specified
		encoding. <arg>bufsize</arg> is the buffer size used from reading the
		response in blocks <arg>*args</arg> and <arg>**kwargs</arg> will be passed
		on to the <meth>open</meth> call.
		"""
		name = url.URL(name)
		with contextlib.closing(name.open("rb", *args, **kwargs)) as stream:
			self.url = stream.finalurl()
			if base is None:
				base = self.url
			if self.tidy:
				return self._parseHTML(stream.read(), base=base, sysid=str(self.url), encoding=encoding)
			parser = self._begin(base=base, encoding=encoding)
			while True:
				data = stream.read(bufsize)
				final = not data
				parser.feed(data, final)
				if final:
					return self._end(parser)

	def parseetree(self, tree, base=None):
		"""
		Parse &xml; input from the object <arg>tree</arg> which must support the
		<a href="http://effbot.org/zone/element-index.htm">ElementTree</a>
		&api;. <arg>base</arg> is the base &url; for the parsing process
		(i.e. this &url; will be prepended to all links in the tree).
		"""
		def toxsc(node):
			if "Element" in type(node).__name__:
				xmlns = None
				name = node.tag
				if node.tag.startswith("{"):
					(xmlns, sep, name) = node.tag[1:].partition("}")
				else:
					xmlns = defaultxmlns
				newnode = self.pool.element_xml(name, xmlns)
				for (attrname, attrvalue) in node.items():
					if attrname.startswith("{"):
						(xmlns, sep, attrname) = attrname[1:].partition("}")
						attrname = self.pool.attrclass_xml(attrname, xmlns)
					attrvalue = newnode.attrs.set_xml(attrname, attrvalue)
					newnode.attrs.set_xml(attrname, attrvalue.parsed(self))
				newnode = newnode.parsed(self, start=True)
				if node.text:
					newnode.append(node.text)
				for child in node:
					newchild = toxsc(child)
					newnode.append(newchild)
					if hasattr(child, "tail") and child.tail:
						newnode.append(child.tail)
				newnode = newnode.parsed(self, start=False)
				return newnode
			elif "ProcessingInstruction" in type(node).__name__:
				newnode = self.pool.procinst_xml(node.target, node.text)
				newnode = newnode.parsed(self)
				return newnode
			elif "Comment" in type(node).__name__:
				newnode = self.pool.comment(node.text)
				newnode = newnode.parsed(self)
				return newnode
			return xsc.Null
		self.base = url.URL(base)

		defaultxmlns = None
		try:
			defaultxmlns = self.prefixes[None][0]
		except (KeyError, IndexError):
			pass

		return toxsc(tree)

	def handle_enterstarttag(self, name, line, col):
		self._attrs = {}

	def handle_enterattr(self, name, line, col):
		node = xsc.Frag()
		self._attrs[name] = node
		self._nesting.append((node, self._nesting[-1][1]))

	def handle_leaveattr(self, name, line, col):
		self._nesting.pop()

	def handle_leavestarttag(self, name, line, col):
		oldprefixes = self.prefixes

		newprefixes = {}
		for (attrname, xmlns) in self._attrs.iteritems():
			if attrname==u"xmlns" or attrname.startswith(u"xmlns:"):
				prefix = attrname[6:] or None
				newprefixes[prefix] = unicode(xmlns)

		if newprefixes:
			prefixes = oldprefixes.copy()
			prefixes.update(newprefixes)
			self.prefixes = newprefixes = prefixes
		else:
			newprefixes = oldprefixes

		(prefix, sep, name) = name.rpartition(u":")
		prefix = prefix or None

		try:
			xmlns = newprefixes[prefix]
		except KeyError:
			raise xsc.IllegalPrefixError(prefix)
		else:
			node = self.pool.element_xml(name, xmlns)

		for (attrname, attrvalue) in self._attrs.iteritems():
			if attrname != u"xmlns" and not attrname.startswith(u"xmlns:"):
				if u":" in attrname:
					(attrprefix, attrname) = attrname.split(u":", 1)
					if attrprefix == "xml":
						xmlns = xsc.xml_xmlns
					else:
						try:
							xmlns = newprefixes[attrprefix]
						except KeyError:
							raise xsc.IllegalPrefixError(attrprefix)
				else:
					xmlns = None
				if xmlns is not None:
					attrname = self.pool.attrclass_xml(attrname, xmlns)
				attrvalue = node.attrs.set_xml(attrname, attrvalue)
				node.attrs.set_xml(attrname, attrvalue.parsed(self))
		node.attrs = node.attrs.parsed(self)
		node = node.parsed(self, start=True)
		self.__appendNode(node, line, col)
		# push new innermost element onto the stack, together with the list of prefix mappings to which we have to return when we leave this element
		self._nesting.append((node, oldprefixes))
		self._attrs = None

	def handle_endtag(self, name, line, col):
		currentelement = self._nesting[-1][0]

		(prefix, sep, name) = name.rpartition(u":")
		xmlns = self.prefixes[prefix or None]
		element = self.pool.element_xml(name, xmlns) # Unfortunately this creates the element a second time.
		if  element.__class__ is not currentelement.__class__:
			raise xsc.ElementNestingError(currentelement.__class__, element.__class__)

		currentelement.parsed(self, start=False) # ignore return value

		if self.validate:
			currentelement.checkvalid()
		if self.loc:
			currentelement.endloc = xsc.Location(self.url, line, col)

		self.prefixes = self._nesting.pop()[1] # pop the innermost element off the stack and restore the old prefixes mapping (from outside this element)

	def handle_data(self, content, line, col):
		if content:
			node = self.pool.text(content)
			node = node.parsed(self)
			last = self._nesting[-1][0]
			if len(last) and isinstance(last[-1], xsc.Text):
				node = last[-1] + unicode(node) # join consecutive Text nodes
				node.startloc = last[-1].startloc # make sure the replacement node has the original location
				last[-1] = node # replace it
			else:
				self.__appendNode(node, line, col)

	handle_cdata = handle_data

	def handle_comment(self, content, line, col):
		node = self.pool.comment(content)
		node = node.parsed(self)
		self.__appendNode(node, line, col)

	def handle_proc(self, target, data, line, col):
		if target != "xml":
			node = self.pool.procinst_xml(target, data)
			node = node.parsed(self)
			self.__appendNode(node, line, col)

	def handle_entityref(self, name, line, col):
		try:
			c = {u"lt": u"<", u"gt": u">", u"amp": u"&", u"quot": u'"', u"apos": u"'"}[name]
		except KeyError:
			node = self.pool.entity_xml(name)
			if isinstance(node, xsc.CharRef):
				self.handle_data(unichr(node.codepoint), line, col)
			else:
				node = node.parsed(self)
				self.__appendNode(node, line, col)
		else:
			self.handle_data(c, line, col)

	def getLocation(self):
		return xsc.Location(self._locator)

	def __appendNode(self, node, line, col):
		if self.loc:
			node.startloc = xsc.Location(self.url, line, col)
		self._nesting[-1][0].append(node) # add the new node to the content of the innermost element/fragment/(attribute)


def parsestring(data, base=None, encoding=None, **builderargs):
	"""
	Parse the string <arg>data</arg> into an &xist; tree. For the arguments
	<arg>base</arg> and <arg>encoding</arg> see the method
	<pyref class="Builder" method="parsestring"><meth>parsestring</meth></pyref>
	in the <class>Builder</class> class. You can pass any other argument that the
	<pyref class="Builder" method="__init__"><class>Builder</class> constructor</pyref>
	takes as keyword arguments via <arg>builderargs</arg>.
	"""
	builder = Builder(**builderargs)
	return builder.parsestring(data, base=base, encoding=encoding)


def parseiter(iterable, base=None, encoding=None, **builderargs):
	"""
	Parse the input from the iterable <arg>iterable</arg> (which must produce the
	input in chunks of bytes) into an &xist; tree. For the arguments <arg>base</arg>
	and <arg>encoding</arg> see the method
	<pyref class="Builder" method="parsestring"><meth>parsestring</meth></pyref>
	in the <class>Builder</class> class. You can pass any other argument that the
	<pyref class="Builder" method="__init__"><class>Builder</class> constructor</pyref>
	takes as keyword arguments via <arg>builderargs</arg>.
	"""
	builder = Builder(**builderargs)
	return builder.parseiter(iterable, base=base, encoding=encoding)


def parsestream(stream, base=None, encoding=None, bufsize=8192, **builderargs):
	"""
	Parse &xml; from the stream <arg>stream</arg> into an &xist; tree.
	For the arguments <arg>base</arg>, <arg>encoding</arg> and <arg>bufzise</arg>
	see the method <pyref class="Builder" method="parse"><meth>parse</meth></pyref>
	in the <class>Parser</class> class. You can pass any other argument that the
	<pyref class="Builder" method="__init__"><class>Builder</class> constructor</pyref>
	takes as keyword arguments via <arg>builderargs</arg>.
	"""
	builder = Builder(**builderargs)
	return builder.parsestream(stream, base=base, encoding=encoding, bufsize=bufsize)


def parsefile(filename, base=None, encoding=None, bufsize=8192, **builderargs):
	"""
	Parse &xml; input from the file named <arg>filename</arg>. For the arguments
	<arg>base</arg>, <arg>encoding</arg> and <arg>bufsize</arg> see the method
	<pyref class="Builder" method="parsefile"><meth>parsefile</meth></pyref>
	in the <class>Builder</class> class. You can pass any other argument that the
	<pyref class="Builder" method="__init__"><class>Builder</class> constructor</pyref>
	takes as keyword arguments via <arg>builderargs</arg>.
	"""
	builder = Builder(**builderargs)
	return builder.parsefile(filename, base=base, encoding=encoding, bufsize=bufsize)


def parseurl(name, base=None, encoding=None, bufsize=8192, headers=None, data=None, **builderargs):
	"""
	Parse &xml; input from the &url; <arg>name</arg> into an &xist; tree.
	For the arguments <arg>base</arg>, <arg>encoding</arg>, <arg>bufsize</arg>,
	<arg>headers</arg> and <arg>data</arg> see the method
	<pyref class="Builder" method="parseurl"><meth>parseurl</meth></pyref>
	in the <class>Builder</class> class. You can pass any other argument that the
	<pyref class="Builder" method="__init__"><class>Builder</class> constructor</pyref>
	takes as keyword arguments via <arg>builderargs</arg>.
	"""
	builder = Builder(**builderargs)
	return builder.parseurl(name, base=base, encoding=encoding, headers=headers, data=data)


def parseetree(tree, base=None, **builderargs):
	"""
	Parse &xml; input from the object <arg>tree</arg> which must support the
	<a href="http://effbot.org/zone/element-index.htm">ElementTree</a>
	&api;. For the argument <arg>base</arg> see the method
	<pyref class="Builder" method="parseetree"><meth>parseetree</meth></pyref>
	in the <class>Builder</class> class. You can pass any other argument that the
	<pyref class="Builder" method="__init__"><class>Builder</class> constructor</pyref>
	takes as keyword arguments via <arg>builderargs</arg>.
	"""
	builder = Builder(**builderargs)
	return builder.parseetree(tree, base=base)
