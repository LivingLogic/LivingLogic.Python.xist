# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
This file contains everything you need to parse XIST objects from files,
strings, URLs etc.
"""


import sys, os, os.path, warnings, cStringIO, codecs, pyexpat, contextlib

from xml.parsers import expat

from ll import url, xml_codec
from ll.xist import xsc
try:
	from ll.xist import sgmlop
except ImportError:
	pass
from ll.xist.ns import xml, html


__docformat__ = "reStructuredText"


class Parser(object):
	"""
	Basic parser interface.
	"""
	def __init__(self):
		self.application = None

	def begin(self, application):
		"""
		Start parsing. Events will be passed to :var:`application`, which must
		implement a handler for each event type.
		"""
		self.application = application

	def end(self):
		"""
		Finish parsing.
		"""
		self.application = None

	def feed(self, data, final):
		"""
		Feed :var:`data` (a byte string) to the parser. If :var:`final` is true
		this will be the last call to :meth:`feed`.
		"""


class SGMLOPParser(Parser):
	"""
	A parser based of :mod:`sgmlop`.
	"""
	def __init__(self, encoding=None):
		"""
		Create a new :class:`SGMLOPParser` object.
		"""
		Parser.__init__(self)
		self.encoding = encoding
		self._decoder = None
		self._parser = None

	def begin(self, application):
		Parser.begin(self, application)
		try:
			self._decoder = codecs.getincrementaldecoder("xml")(encoding=self.encoding)
			if self._parser is not None:
				self._parser.register(None)
			self._parser = sgmlop.XMLParser()
			self._parser.register(self)
		except Exception:
			if self._parser is not None:
				self._parser.register(None)
				self._parser = None
			self._decoder = None
			raise

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
	"""
	A parser using Pythons builtin :mod:`expat` XML parser.
	"""
	def __init__(self, encoding=None, transcode=False, xmldecl=False, doctype=False):
		Parser.__init__(self)
		self.encoding = encoding
		self._parser = None
		self._decoder = None
		self._encoder = None
		self._xmldecl = xmldecl
		self._doctype = doctype
		self._indoctype = False
		self._transcode = transcode

	def begin(self, application):
		Parser.begin(self, application)
		try:
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

			if self._xmldecl:
				self._parser.XmlDeclHandler = self.handle_xmldecl

			# Always required, as we want to recognize whether a comment or PI is in the internal DTD subset
			self._parser.StartDoctypeDeclHandler = self.handle_begindoctype
			self._parser.EndDoctypeDeclHandler = self.handle_enddoctype

			if self._transcode:
				self._decoder = codecs.getincrementaldecoder("xml")()
				self._encoder = codecs.getincrementalencoder("xml")(encoding="utf-8")
		except Exception:
			self._parser = None
			self._encoder = None
			self._decoder = None
			raise

	def end(self):
		Parser.end(self)
		self._parser = None
		self._encoder = None
		self._decoder = None

	def handle_xmldecl(self, version, encoding, standalone):
		standalone = (bool(standalone) if standalone != -1 else None)
		self.application.handle_xmldecl(version, encoding, standalone, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)

	def handle_begindoctype(self, doctypename, systemid, publicid, has_internal_subset):
		if publicid:
			content = u'%s PUBLIC "%s" "%s"' % (doctypename, publicid, systemid)
		elif systemid:
			content = u'%s SYSTEM "%s"' % (doctypename, systemid)
		else:
			content = doctypename
		self._indoctype = True
		if self._doctype:
			self.application.handle_doctype(content, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)

	def handle_enddoctype(self):
		self._indoctype = False

	def handle_default(self, data):
		if data.startswith("&") and data.endswith(";"):
			self.application.handle_entityref(data[1:-1], self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)

	def handle_comment(self, data):
		if not self._indoctype:
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
		if not self._indoctype:
			self.application.handle_proc(target, data, self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)

	def feed(self, data, final):
		if self._transcode:
			data = self._decoder.decode(data, final)
			data = self._encoder.encode(data, final)
		self._parser.Parse(data, final)


class Builder(object):
	"""
	It is the job of a :class:`Builder` to create the object tree from the
	events generated by the underlying parser.
	"""

	def __init__(self, parser=None, prefixes=None, tidy=False, loc=True, validate=True, encoding=None, pool=None):
		"""
		Create a new :class:`Builder` instance.

		Arguments have the following meaning:

		:var:`parser`
			an instance of the :class:`Parser` class (or any object that provides
			the appropriate interface).

		:var:`prefixes` : mapping
			a mapping that maps namespace prefixes to namespace names/modules
			(or lists of namespace names/modules). This is used to preinitialize
			the namespace prefix mapping.

		:var:`tidy` : bool
			If :var:`tidy` is true, libxml2__'s HTML parser will be used for
			parsing broken HTML.

			__ http://xmlsoft.org/

		:var:`loc` : bool
			Should location information be attached to the generated nodes?

		:var:`validate` : bool
			Should the parsed XML nodes be validated after parsing?

		:var:`encoding` : string or :const:`None`
			The default encoding to use when the source doesn't provide an
			encoding. The default :const:`None` results in the encoding being
			detected from the XML itself.

		:var:`pool` : :class:`ll.xist.xsc.Pool` object
			This pool will be used for creating all nodes during parsing.
		"""
		self.parser = parser

		self.pool = (pool if pool is not None else xsc.threadlocalpool.pool)

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
		Internal helper method for parsing HTML via :mod:`libxml2`.
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

		self.base = url.URL(base)

		if not data:
			node = xsc.Frag()
		else:
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
			parser = ExpatParser(encoding=encoding)
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
		Parse the string :var:`data` (:class:`str` or :class:`unicode`) into an
		XIST tree. :var:`base` is the base URL for the parsing process,
		:var:`encoding` can be used to force the parser to use the specified
		encoding.
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
		Parse the input from the iterable :var:`var` (which must produce the input
		in chunks of bytes) into an XIST tree. :var:`base` is the base URL for the
		parsing process, :var:`encoding` can be used to force the parser to use
		the specified encoding.
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
		Parse XML input from the stream :var:`stream`. :var:`base` is the base
		URL for the parsing process, :var:`encoding` can be used to force the
		parser to use the specified encoding. :var:`bufsize` is the buffer size
		used for reading the stream in blocks.
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
		Parse XML input from the file named :var:`filename`. :var:`base` is the
		base URL for the parsing process (defaulting to :var:`filename` if not
		specified), :var:`encoding` can be used to force the parser to use the
		specified encoding. :var:`bufsize` is the buffer size used for reading
		the file in blocks.
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
		Parse XML input from the URL :var:`name` (which might be a string
		or an :class:`ll.url.URL` object) into an XIST tree. :var:`base` is the
		base URL for the parsing process (defaulting to the final URL of the
		response (i.e. including redirects)). :var:`encoding` can be used to
		force the parser to use the specified encoding. :var:`bufsize` is the
		buffer size used for reading the response in blocks. :var:`args` and
		:var:`kwargs` will be passed on to the :meth:`open` call.
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
		Parse XML input from the object :var:`tree` which must support the
		ElementTree__ API. :var:`base` is the base URL for the parsing process
		(i.e. this URL will be prepended to all links in the tree).
		
		__ http://effbot.org/zone/element-index.htm
		"""
		def toxsc(node):
			name = type(node).__name__
			if "Element" in name:
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
			elif "ProcessingInstruction" in name:
				newnode = self.pool.procinst_xml(node.target, node.text)
				newnode = newnode.parsed(self)
				return newnode
			elif "Comment" in name:
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

	def handle_xmldecl(self, version, encoding, standalone, line, col):
		node = xml.XML(version=version, encoding=encoding, standalone=standalone)
		self.__appendNode(node, line, col)

	def handle_doctype(self, content, line, col):
		node = xsc.DocType(content)
		self.__appendNode(node, line, col)

	def handle_enterstarttag(self, name, line, col):
		self._attrs = {}

	def handle_enterattr(self, name, line, col):
		node = xsc.Frag()
		self._attrs[name] = node
		self._nesting.append((node, self._nesting[-1][1]))

	def handle_leaveattr(self, name, line, col):
		(node, prefixes) = self._nesting.pop()
		# if the attribute was empty, ``handle_data`` is newer called, so we have to add an empty text node, to prevent the attribute from disappearing
		if not node:
			node.append("")

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
	Parse the string :var:`data` into an XIST tree. For the arguments
	:var:`base` and :var:`encoding` see the method :meth:`parsestring` in the
	:class:`Builder` class. You can pass any other argument that the
	:class:`Builder` constructor takes as keyword arguments
	via :var:`builderargs`.
	"""
	builder = Builder(**builderargs)
	return builder.parsestring(data, base=base, encoding=encoding)


def parseiter(iterable, base=None, encoding=None, **builderargs):
	"""
	Parse the input from the iterable :var:`iterable` (which must produce the
	input in chunks of bytes) into an XIST tree. For the arguments :var:`base`
	and :var:`encoding` see the method :meth:`parsestring` in the
	:class:`Builder` class. You can pass any other argument that the
	:class:`Builder` constructor takes as keyword arguments via
	:var:`builderargs`.
	"""
	builder = Builder(**builderargs)
	return builder.parseiter(iterable, base=base, encoding=encoding)


def parsestream(stream, base=None, encoding=None, bufsize=8192, **builderargs):
	"""
	Parse XML from the stream :var:`stream` into an XIST tree. For the arguments
	:var:`base`, :var:`encoding` and :var:`bufzise` see the method
	:meth:`parsestream` in the :class:`Parser` class. You can pass any other
	argument that the :class:`Builder` constructor takes as keyword arguments via
	:var:`builderargs`.
	"""
	builder = Builder(**builderargs)
	return builder.parsestream(stream, base=base, encoding=encoding, bufsize=bufsize)


def parsefile(filename, base=None, encoding=None, bufsize=8192, **builderargs):
	"""
	Parse XML input from the file named :var:`filename`. For the arguments
	:var:`base`, :var:`encoding` and :var:`bufsize` see the method
	:meth:`parsefile` in the :class:`Builder` class. You can pass any other
	argument that the :class:`Builder` constructor takes as keyword arguments
	via :var:`builderargs`.
	"""
	builder = Builder(**builderargs)
	return builder.parsefile(filename, base=base, encoding=encoding, bufsize=bufsize)


def parseurl(name, base=None, encoding=None, bufsize=8192, headers=None, data=None, **builderargs):
	"""
	Parse XML input from the URL :var:`name` into an XIST tree. For the arguments
	:var:`base`, :var:`encoding`, :var:`bufsize`, :var:`headers` and :var:`data`
	see the method :meth:`parseurl` in the :class:`Builder` class. You can pass
	any other argument that the :class:`Builder` constructor takes as keyword
	arguments via :var:`builderargs`.
	"""
	builder = Builder(**builderargs)
	kwargs = dict(base=base, encoding=encoding)
	if headers is not None:
		kwargs["headers"] = headers
	if data is not None:
		kwargs["data"] = data
	return builder.parseurl(name, **kwargs)


def parseetree(tree, base=None, **builderargs):
	"""
	Parse XML input from the object :var:`tree` which must support the
	ElementTree__ API. For the argument :var:`base` see the method
	:meth:`parseetree` in the :class:`Builder` class. You can pass any other
	argument that the :class:`Builder` constructor takes as keyword arguments
	via :var:`builderargs`.

	__ http://effbot.org/zone/element-index.htm
	"""
	builder = Builder(**builderargs)
	return builder.parseetree(tree, base=base)
