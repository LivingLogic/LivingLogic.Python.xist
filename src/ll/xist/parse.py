# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This module contains everything you need to create XIST objects by parsing
files, strings, URLs etc.

Parsing XML is done with a pipelined approach. The first step in the pipeline
is a source object that provides the input for the rest of the pipeline.
The next step is the XML parser. It turns the input source into an iterator over
parsing events (an "event stream"). Further steps in the pipeline might resolve
namespace prefixes (:class:`NS`), and instantiate XIST classes
(:class:`Node`). The final step in the pipeline is either building an
XML tree via :func:`tree` or an iterative parsing step (similar to ElementTrees
:func:`iterparse` function) via :func:`itertree`.

Parsing a simple HTML string might e.g. look like this::

	>>> from ll.xist import xsc, parse
	>>> from ll.xist.ns import html
	>>> source = b"<a href='http://www.python.org/'>Python</a>"
	>>> doc = parse.tree(
	... 	parse.String(source),
	... 	parse.Expat(),
	... 	parse.NS(html),
	... 	parse.Node(pool=xsc.Pool(html)),
	... )
	>>> doc.string()
	'<a href="http://www.python.org/">Python</a>'

A source object is an iterable object that produces the input byte string for
the parser (possibly in multiple chunks) (and information about the URL of the
input)::

	>>> from ll.xist import parse
	>>> list(parse.String(b"<a href='http://www.python.org/'>Python</a>"))
	[('url', URL('STRING')),
	 ('bytes', "<a href='http://www.python.org/'>Python</a>")]

All subsequent objects in the pipeline are callable objects, get the input
iterator as an argument and return an iterator over events themselves. The
following code shows an example of an event stream::

	>>> from ll.xist import parse
	>>> source = b"<a href='http://www.python.org/'>Python</a>"
	>>> list(parse.events(parse.String(source), parse.Expat()))
	[('url', URL('STRING')),
	 ('position', (0, 0)),
	 ('enterstarttag', 'a'),
	 ('enterattr', 'href'),
	 ('text', 'http://www.python.org/'),
	 ('leaveattr', 'href'),
	 ('leavestarttag', 'a'),
	 ('position', (0, 39)),
	 ('text', 'Python'),
	 ('endtag', 'a')]

An event is a tuple consisting of the event type and the event data. Different
stages in the pipeline produce different event types. The following event types
can be produced by source objects:

	``"url"``
		The event data is the URL of the source. Usually such an event is produced
		only once at the start of the event stream. For sources that have no
		natural URL (like strings or streams) the URL can be specified when
		creating the source object.

	``"bytes"``
		This event is produced by source objects  (and :class:`Transcoder` objects).
		The event data is a byte string.

	``"str"``
		The event data is a string. This event is produced by :class:`Decoder`
		or source objects. Note that the only predefined pipeline objects that can
		handle ``"str"`` events are :class:`Encoder` objects, i.e. normally a
		parser handles ``"bytes"`` events, but not ``"str"`` events.

The following type of events are produced by parsers (in addition to the
``"url"`` event from above):

	``"position"``
		The event data is a tuple containing the line and column number in the
		source (both starting with 0). All the following events should use this
		position information until the next position event.

	``"xmldecl"``
		The XML declaration. The event data is a dictionary containing the keys
		``"version"``, ``"encoding"`` and ``"standalone"``. Parsers may omit this
		event.

	``"begindoctype"``
		The begin of the doctype. The event data is a dictionary containing the
		keys ``"name"``, ``"publicid"`` and ``"systemid"``.  Parsers may omit this
		event.

	``"enddoctype"``
		The end of the doctype. The event data is :const:`None`. (If there is no
		internal subset, the ``"enddoctype"`` event immediately follows the
		``"begindoctype"`` event). Parsers may omit this event.

	``"comment"``
		A comment. The event data is the content of the comment.

	``"text"``
		Text data. The event data is the text content. Parsers should try to avoid
		outputting multiple text events in sequence.

	``"cdata"``
		A CDATA section. The event data is the content of the CDATA section.
		Parsers may report CDATA sections as ``"text"`` events instead of
		``"cdata"`` events.

	``"enterstarttag"``
		The beginning of an element start tag. The event data is the element name.

	``"leavestarttag"``
		The end of an element start tag. The event data is the element name.
		The parser will output events for the attributes between the
		``"enterstarttag"`` and the ``"leavestarttag"`` event.

	``"enterattr"``
		The beginning of an attribute. The event data is the attribute name.

	``"leaveattr"``
		The end of an attribute. The event data is the attribute name.
		The parser will output events for the attribute value between the
		``"enterattr"`` and the ``"leaveattr"`` event. (In almost all cases
		this is one text event).

	``"endtag"``
		An element end tag. The event data is the element name.

	``"procinst"``
		A processing instruction. The event data is a tuple consisting of the
		processing instruction target and the data.

	``"entity"``
		An entity reference. The event data is the entity name.

The following events are produced for elements and attributes in namespace mode
(instead of those without the ``ns`` suffix). They are produced by :class:`NS`
objects or by :class:`Expat` objects when the :obj:`ns` argument is true (i.e.
the expat parser performs the namespace resolution):

	``"enterstarttagns"``
		The beginning of an element start tag in namespace mode.
		The event data is an (namespace name, element name) tuple.

	``"leavestarttagns"``
		The end of an element start tag in namespace mode. The event data is an
		(namespace name, element name) tuple.

	``"enterattrns"``
		The beginning of an attribute in namespace mode. The event data is an
		(namespace name, element name) tuple.

	``"leaveattrns"``
		The end of an attribute in namespace mode. The event data is an
		(namespace name, element name) tuple.

	``"endtagns"``
		An element end tag in namespace mode. The event data is an
		(namespace name, element name) tuple.

Once XIST nodes have been instantiated (by :class:`Node` objects) the
following events are used:

	``"xmldeclnode"``
		The XML declaration. The event data is an instance of
		:class:`ll.xist.xml.XML`.

	``"doctypenode"``
		The doctype. The event data is an instance of :class:`ll.xist.xsc.DocType`.

	``"commentnode"``
		A comment. The event data is an instance of :class:`ll.xist.xsc.Comment`.

	``"textnode"``
		Text data. The event data is an instance of :class:`ll.xist.xsc.Text`.

	``"enterelementnode"``
		The beginning of an element. The event data is an instance of
		:class:`ll.xist.xsc.Element` (or one of its subclasses). The attributes
		of the element object are set, but the element has no content yet.

	``"leaveelementnode"``
		The end of an element. The event data is an instance of
		:class:`ll.xist.xsc.Element`.

	``"procinstnode"``
		A processing instruction. The event data is an instance of
		:class:`ll.xist.xsc.ProcInst`.

	``"entitynode"``
		An entity reference. The event data is an instance of
		:class:`ll.xist.xsc.Entity`.

For consuming event streams there are three functions:

	:func:`events`
		This generator simply outputs the events.

	:func:`tree`
		This function builds an XML tree from the events and returns it.

	:func:`itertree`
		This generator builds a tree like :func:`tree`, but returns events
		during certain steps in the parsing process.


Example
-------

The following example shows a custom generator in the pipeline that lowercases
all element and attribute names::

	from ll.xist import xsc, parse
	from ll.xist.ns import html

	def lowertag(input):
		for (event, data) in input:
			if event in {"enterstarttag", "leavestarttag", "endtag", "enterattr", "leaveattr"}:
				data = data.lower()
			yield (event, data)

	e = parse.tree(
		parse.String(b"<A HREF='gurk'><B>gurk</B></A>"),
		parse.Expat(),
		lowertag,
		parse.NS(html),
		parse.Node(pool=xsc.Pool(html))
	)

	print(e.string())

This scripts outputs::

	<a href="gurk"><b>gurk</b></a>
"""


import os, os.path, warnings, io, codecs, contextlib

from xml.parsers import expat

from ll import url as url_, xml_codec
from ll.xist import xsc, xfind
try:
	from ll.xist import sgmlop
except ImportError:
	pass
from ll.xist.ns import xml


__docformat__ = "reStructuredText"


html_xmlns = "http://www.w3.org/1999/xhtml"


###
### exceptions
###

class UnknownEventError(TypeError):
	"""
	This exception is raised when a pipeline object doesn't know how to handle
	an event.
	"""
	def __init__(self, pipe, event):
		self.pipe = pipe
		self.event = event

	def __str__(self):
		return f"{self.pipe!r} can't handle event type {self.event[0]!r}"


###
### Sources: Classes that create on event stream
###

class String:
	"""
	Provides parser input from a string.
	"""
	def __init__(self, data, url=None):
		"""
		Create a :class:`String` object. :obj:`data` must be a :class:`bytes` or
		:class:`str` object. :obj:`url` specifies the URL for the source
		(defaulting to ``"STRING"``).
		"""
		self.url = url_.URL(url if url is not None else "STRING")
		self.data = data

	def __iter__(self):
		"""
		Produces an event stream of one ``"url"`` event and one ``"bytes"`` or
		``"str"`` event for the data.
		"""
		yield ("url", self.url)
		if isinstance(self.data, bytes):
			yield ("bytes", self.data)
		elif isinstance(self.data, str):
			yield ("str", self.data)
		else:
			raise TypeError("data must be str or bytes")


class Iter:
	"""
	Provides parser input from an iterator over strings.
	"""

	def __init__(self, iterable, url=None):
		"""
		Create a :class:`Iter` object. :obj:`iterable` must be an iterable object
		producing :class:`bytes` or :class:`str` objects. :obj:`url` specifies the
		URL for the source (defaulting to ``"ITER"``).
		"""
		self.url = url_.URL(url if url is not None else "ITER")
		self.iterable = iterable

	def __iter__(self):
		"""
		Produces an event stream of one ``"url"`` event followed by the
		``"bytes"``/``"str"`` events for the data from the iterable.
		"""
		yield ("url", self.url)
		for data in self.iterable:
			if isinstance(data, bytes):
				yield ("bytes", data)
			elif isinstance(data, int): # From iterating over a ``bytes`` object
				yield ("bytes", bytes([data]))
			elif isinstance(data, str):
				yield ("str", data)
			else:
				raise TypeError("data must be str or bytes")


class Stream:
	"""
	Provides parser input from a stream (i.e. an object that provides a
	:meth:`read` method).
	"""

	def __init__(self, stream, url=None, bufsize=8192):
		"""
		Create a :class:`Stream` object. :obj:`stream` must have a :meth:`read`
		method (with a ``size`` argument). :obj:`url` specifies the URL for the
		source (defaulting to ``"STREAM"``). :obj:`bufsize` specifies the
		chunksize for reads from the stream.
		"""
		self.url = url_.URL(url if url is not None else "STREAM")
		self.stream = stream
		self.bufsize = bufsize

	def __iter__(self):
		"""
		Produces an event stream of one ``"url"`` event followed by the
		``"bytes"``/``"str"`` events for the data from the stream.
		"""
		yield ("url", self.url)
		while True:
			data = self.stream.read(self.bufsize)
			if data:
				if isinstance(data, bytes):
					yield ("bytes", data)
				elif isinstance(data, str):
					yield ("str", data)
				else:
					raise TypeError("data must be str or bytes")
			else:
				break


class File:
	"""
	Provides parser input from a file.
	"""

	def __init__(self, filename, bufsize=8192):
		"""
		Create a :class:`File` object. :obj:`filename` is the name of the file
		and may start with ``~`` or ``~user`` for the home directory of the
		current or the specified user. :obj:`bufsize` specifies the chunksize
		for reads from the file.
		"""
		self.url = url_.File(filename)
		self._filename = os.path.expanduser(filename)
		self.bufsize = bufsize

	def __iter__(self):
		"""
		Produces an event stream of one ``"url"`` event followed by the
		``"bytes"`` events for the data from the file.
		"""
		yield ("url", self.url)
		with open(self._filename, "rb") as stream:
			while True:
				data = stream.read(self.bufsize)
				if data:
					yield ("bytes", data)
				else:
					break


class URL:
	"""
	Provides parser input from a URL.
	"""

	def __init__(self, name, bufsize=8192, *args, **kwargs):
		"""
		Create a :class:`URL` object. :obj:`name` is the URL. :obj:`bufsize`
		specifies the chunksize for reads from the URL. :obj:`args` and
		:obj:`kwargs` will be passed on to the :meth:`open` method of the URL
		object.

		The URL for the input will be the final URL for the resource (i.e. it will
		include redirects).
		"""
		self.url = url_.URL(name)
		self.bufsize = bufsize
		self.args = args
		self.kwargs = kwargs

	def __iter__(self):
		"""
		Produces an event stream of one ``"url"`` event followed by the
		``"bytes"`` events for the data from the URL.
		"""
		stream = self.url.open("rb", *self.args, **self.kwargs)
		yield ("url", stream.finalurl())
		with contextlib.closing(stream) as stream:
			while True:
				data = stream.read(self.bufsize)
				if data:
					yield ("bytes", data)
				else:
					break


class ETree:
	"""
	Produces a (namespaced) event stream from an object that supports the
	ElementTree__ API.

	__ http://effbot.org/zone/element-index.htm
	"""

	def __init__(self, data, url=None, defaultxmlns=None):
		"""
		Create an :class:`ETree` object. Arguments have the following meaning:

		:obj:`data`
			An object that supports the ElementTree API.

		:obj:`url`
			The URL of the source. Defaults to ``"ETREE"``.

		:obj:`defaultxmlns`
			The namespace name (or a namespace module containing a namespace name)
			that will be used for all elements that don't have a namespace.
		"""
		self.url = url_.URL(url if url is not None else "ETREE")
		self.data = data
		self.defaultxmlns = xsc.nsname(defaultxmlns)

	def _asxist(self, node):
		name = type(node).__name__
		if "Element" in name:
			elementname = node.tag
			if elementname.startswith("{"):
				(elementxmlns, sep, elementname) = elementname[1:].partition("}")
			else:
				elementxmlns = self.defaultxmlns
			yield ("enterstarttagns", (elementxmlns, elementname))
			for (attrname, attrvalue) in node.items():
				if attrname.startswith("{"):
					(attrxmlns, sep, attrname) = attrname[1:].partition("}")
				else:
					attrxmlns = None
				yield ("enterattrns", (attrxmlns, attrname))
				yield ("text", attrvalue)
				yield ("leaveattrns", (attrxmlns, attrname))
			yield ("leavestarttagns", (elementxmlns, elementname))
			if node.text:
				yield ("text", node.text)
			for child in node:
				yield from self._asxist(child)
				if hasattr(child, "tail") and child.tail:
					yield ("text", child.tail)
			yield ("endtagns", (elementxmlns, elementname))
		elif "ProcessingInstruction" in name:
			yield ("procinst", (node.target, node.text))
		elif "Comment" in name:
			yield ("comment", node.text)

	def __iter__(self):
		"""
		Produces an event stream of namespaced parsing events for the ElementTree
		object passed as :obj:`data` to the constructor.
		"""
		yield ("url", self.url)
		yield from self._asxist(self.data)


###
### Transformers: Classes that transform the event stream.
###

class Decoder:
	"""
	Decode the :class:`bytes` object produced by the previous object in the
	pipeline to :class:`str` object.

	This input object can be a source object or any other pipeline object that
	produces :class:`bytes` objects.
	"""

	def __init__(self, encoding=None):
		"""
		Create a :class:`Decoder` object. :obj:`encoding` is the encoding of the
		input. If :obj:`encoding` is :const:`None` it will be automatically
		detected from the XML data.
		"""
		self.encoding = encoding

	def __call__(self, input):
		decoder = codecs.getincrementaldecoder("xml")(encoding=self.encoding)
		for (evtype, data) in input:
			if evtype == "bytes":
				data = decoder.decode(data, False)
				if data:
					yield ("str", data)
			elif evtype == "str":
				if data:
					yield ("str", data)
			elif evtype == "url":
				yield ("url", data)
			else:
				raise UnknownEventError(self, (evtype, data))
		data = decoder.decode(b"", True)
		if data:
			yield ("str", data)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object encoding={self.encoding!r} at {id(self):#x}>"


class Encoder:
	"""
	Encode the :class:`str` objects produced by the previous object in the
	pipeline to :class:`bytes` objects.

	This input object must be a pipeline object that produces string output
	(e.g. a :class:`Decoder` object).

	This can e.g. be used to parse a :class:`str` object instead of a
	:class:`bytes` object like this::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import html
		>>> source = "<a href='http://www.python.org/'>Python</a>"
		>>> doc = parse.tree(
		... 	parse.String(source),
		... 	parse.Encoder(encoding="utf-8"),
		... 	parse.Expat(encoding="utf-8"),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(html)),
		... )
		>>> doc.string()
		'<a href="http://www.python.org/">Python</a>'
	"""

	def __init__(self, encoding=None):
		"""
		Create an :class:`Encoder` object. :obj:`encoding` will be the encoding of
		the output. If :obj:`encoding` is :const:`None` it will be automatically
		detected from the XML declaration in the data.
		"""
		self.encoding = encoding

	def __call__(self, input):
		encoder = codecs.getincrementalencoder("xml")(encoding=self.encoding)
		for (evtype, data) in input:
			if evtype == "str":
				data = encoder.encode(data, False)
				if data:
					yield ("bytes", data)
			elif evtype == "bytes":
				if data:
					yield ("bytes", data)
			elif evtype == "url":
				yield ("url", data)
			else:
				raise UnknownEventError(self, (evtype, data))
		data = encoder.encode("", True)
		if data:
			yield ("bytes", data)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object encoding={self.encoding!r} at {id(self):#x}>"


class Transcoder:
	"""
	Transcode the :class:`bytes` object of the input object into another encoding.

	This input object can be a source object or any other pipeline object that
	produces :class:`bytes` events.
	"""

	def __init__(self, fromencoding=None, toencoding=None):
		"""
		Create a :class:`Transcoder` object. :obj:`fromencoding` is the encoding
		of the input. :obj:`toencoding` is the encoding of the output. If any of
		them is :const:`None` the encoding will be detected from the data.
		"""
		self.fromencoding = fromencoding
		self.toencoding = toencoding

	def __call__(self, input):
		decoder = codecs.getincrementaldecoder("xml")(encoding=self.fromencoding)
		encoder = codecs.getincrementalencoder("xml")(encoding=self.toencoding)
		for (evtype, data) in input:
			if evtype == "bytes":
				data = encoder.encode(decoder.decode(data, False), False)
				if data:
					yield ("bytes", data)
			elif evtype == "url":
				yield ("url", data)
			else:
				raise UnknownEventError(self, (evtype, data))
		data = encoder.encode(decoder.decode(b"", True), True)
		if data:
			yield ("bytes", data)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object fromencoding={self.fromencoding!r} toencoding={self.toencoding!r} at {id(self):#x}>"


###
### Parsers
###

class Parser:
	"""
	Basic parser interface.
	"""
	evxmldecl = "xmldecl"
	evbegindoctype = "begindoctype"
	evenddoctype = "enddoctype"
	evcomment = "comment"
	evtext = "text"
	evcdata = "cdata"
	eventerstarttag = "enterstarttag"
	eventerstarttagns = "enterstarttagns"
	eventerattr = "enterattr"
	eventerattrns = "enterattrns"
	evleaveattr = "leaveattr"
	evleaveattrns = "leaveattrns"
	evleavestarttag = "leavestarttag"
	evleavestarttagns = "leavestarttagns"
	evendtag = "endtag"
	evendtagns = "endtagns"
	evprocinst = "procinst"
	eventity = "entity"
	evposition = "position"
	evurl = "url"


class Expat(Parser):
	"""
	A parser using Pythons builtin :mod:`expat` parser.
	"""

	def __init__(self, encoding=None, xmldecl=False, doctype=False, loc=True, cdata=False, ns=False):
		"""
		Create an :class:`Expat` parser. Arguments have the following meaning:

		:obj:`encoding` : string or :const:`None`
			Forces the parser to use the specified encoding. The default
			:const:`None` results in the encoding being detected from the XML itself.

		:obj:`xmldecl` : bool
			Should the parser produce events for the XML declaration?

		:obj:`doctype` : bool
			Should the parser produce events for the document type?

		:obj:`loc` : bool
			Should the parser produce ``"location"`` events?

		:obj:`cdata` : bool
			Should the parser output CDATA sections as ``"cdata"`` events? (If
			:obj:`cdata` is false ``"text"`` events are output instead.)

		:obj:`ns` : bool
			If :obj:`ns` is true, the parser performs namespace processing itself,
			i.e. it will emit ``"enterstarttagns"``, ``"leavestarttagns"``,
			``"endtagns"``, ``"enterattrns"`` and ``"leaveattrns"`` events instead
			of ``"enterstarttag"``, ``"leavestarttag"``, ``"endtag"``,
			``"enterattr"`` and ``"leaveattr"`` events.
		"""
		self.encoding = encoding
		self.xmldecl = xmldecl
		self.doctype = doctype
		self.loc = loc
		self.cdata = cdata
		self.ns = ns

	def __repr__(self):
		v = []
		if self.encoding is not None:
			v.append(f" encoding={self.encoding!r}")
		if self.xmldecl is not None:
			v.append(f" xmldecl={self.xmldecl!r}")
		if self.doctype is not None:
			v.append(f" doctype={self.doctype!r}")
		if self.loc is not None:
			v.append(f" loc={self.loc!r}")
		if self.cdata is not None:
			v.append(f" cdata={self.cdata!r}")
		if self.ns is not None:
			v.append(f" ns={self.ns!r}")
		attrs = "".join(v)
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object{attrs} at {id(self):#x}>"

	def __call__(self, input):
		"""
		Return an iterator over the events produced by :obj:`input`.
		"""
		self._parser = expat.ParserCreate(self.encoding, "\x01" if self.ns else None)
		self._parser.buffer_text = True
		self._parser.ordered_attributes = True
		self._parser.UseForeignDTD(True)
		self._parser.CharacterDataHandler = self._handle_text
		self._parser.StartElementHandler = self._handle_startelement
		self._parser.EndElementHandler = self._handle_endelement
		self._parser.ProcessingInstructionHandler = self._handle_procinst
		self._parser.CommentHandler = self._handle_comment
		self._parser.DefaultHandler = self._handle_default

		if self.cdata:
			self._parser.StartCdataSectionHandler = self._handle_startcdata
			self._parser.EndCdataSectionHandler = self._handle_endcdata

		if self.xmldecl:
			self._parser.XmlDeclHandler = self._handle_xmldecl

		# Always required, as we want to recognize whether a comment or PI is in the internal DTD subset
		self._parser.StartDoctypeDeclHandler = self._handle_begindoctype
		self._parser.EndDoctypeDeclHandler = self._handle_enddoctype

		self._indoctype = False
		self._incdata = False
		self._currentloc = None # Remember the last reported position

		# Buffers the events generated during one call to ``Parse``
		self._buffer = []

		try:
			for (evtype, data) in input:
				if evtype == "bytes":
					try:
						self._parser.Parse(data, False)
					except Exception as exc:
						# In case of an exception we want to output the events we have gathered so far, before reraising the exception
						yield from self._flush(True)
						raise exc
					else:
						yield from self._flush(False)
				elif evtype == "url":
					yield (self.evurl, data)
				else:
					raise UnknownEventError(self, (evtype, data))
			try:
				self._parser.Parse(b"", True)
			except Exception as exc:
				yield from self._flush(True)
				raise exc
			else:
				yield from self._flush(True)
		finally:
			del self._buffer
			del self._currentloc
			del self._incdata
			del self._indoctype
			del self._parser

	def _event(self, evtype, evdata):
		loc = None
		if self.loc:
			loc = (self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)
			if loc == self._currentloc:
				loc = None
		if self._buffer and evtype == self._buffer[-1][0] == self.evtext:
			self._buffer[-1] = (evtype, self._buffer[-1][1] + evdata)
		else:
			if loc:
				self._buffer.append((self.evposition, loc))
			self._buffer.append((evtype, evdata))
			if loc:
				self._currentloc = loc

	def _flush(self, force):
		# Flush ``self._buffer`` as far as possible
		if force or not self._buffer or self._buffer[-1][0] != self.evtext:
			yield from self._buffer
			del self._buffer[:]
		else:
			# hold back the last text event, because there might be more
			yield from self._buffer[:-1]
			del self._buffer[:-1]

	def _getname(self, name):
		if self.ns:
			if "\x01" in name:
				return tuple(name.split("\x01"))
			return (None, name)
		return name

	def _handle_startcdata(self):
		self._incdata = True

	def _handle_endcdata(self):
		self._incdata = False

	def _handle_xmldecl(self, version, encoding, standalone):
		standalone = (bool(standalone) if standalone != -1 else None)
		self._event(self.evxmldecl, {"version": version, "encoding": encoding, "standalone": standalone})

	def _handle_begindoctype(self, doctypename, systemid, publicid, has_internal_subset):
		if self.doctype:
			self._event(self.evbegindoctype, {"name": doctypename, "publicid": publicid, "systemid": systemid})

	def _handle_enddoctype(self):
		if self.doctype:
			self._event(self.evenddoctype, None)

	def _handle_default(self, data):
		if data.startswith("&") and data.endswith(";"):
			self._event(self.eventity, data[1:-1])

	def _handle_comment(self, data):
		if not self._indoctype:
			self._event(self.evcomment, data)

	def _handle_text(self, data):
		self._event(self.evcdata if self._incdata else self.evtext, data)

	def _handle_startelement(self, name, attrs):
		name = self._getname(name)
		self._event(self.eventerstarttagns if self.ns else self.eventerstarttag, name)
		for i in range(0, len(attrs), 2):
			key = self._getname(attrs[i])
			self._event(self.eventerattrns if self.ns else self.eventerattr, key)
			self._event(self.evtext, attrs[i+1])
			self._event(self.evleaveattrns if self.ns else self.evleaveattr, key)
		self._event(self.evleavestarttagns if self.ns else self.evleavestarttag, name)

	def _handle_endelement(self, name):
		name = self._getname(name)
		self._event(self.evendtagns if self.ns else self.evendtag, name)

	def _handle_procinst(self, target, data):
		if not self._indoctype:
			self._event(self.evprocinst, (target, data))


class SGMLOP(Parser):
	"""
	A parser based on :mod:`sgmlop`.
	"""

	def __init__(self, encoding=None, cdata=False):
		"""
		Create a :class:`SGMLOP` parser. Arguments have the following meaning:

		:obj:`encoding` : string or :const:`None`
			Forces the parser to use the specified encoding. The default
			:const:`None` results in the encoding being detected from the XML itself.

		:obj:`cdata` : bool
			Should the parser output CDATA sections as ``"cdata"`` events? (If
			:obj:`cdata` is false output ``"text"`` events instead.)
		"""
		self.encoding = encoding
		self.cdata = cdata

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object encoding={self.encoding!r} at {id(self):#x}>"

	def __call__(self, input):
		"""
		Return an iterator over the events produced by :obj:`input`.
		"""
		self._decoder = codecs.getincrementaldecoder("xml")(encoding=self.encoding)
		self._parser = sgmlop.XMLParser()
		self._parser.register(self)
		self._buffer = []
		self._hadtext = False

		try:
			for (evtype, data) in input:
				if evtype == "bytes":
					data = self._decoder.decode(data, False)
					evtype = "str"
				if evtype == "str":
					try:
						self._parser.feed(data)
					except Exception as exc:
						# In case of an exception we want to output the events we have gathered so far, before reraising the exception
						yield from self._flush(True)
						self._parser.close()
						raise exc
					else:
						yield from self._flush(False)
				elif evtype == "url":
					yield (self.evurl, data)
				else:
					raise UnknownEventError(self, (evtype, data))
			self._parser.close()
			yield from self._flush(True)
		finally:
			del self._hadtext
			del self._buffer
			self._parser.register(None)
			del self._parser
			del self._decoder

	def _event(self, evtype, evdata):
		if self._buffer and evtype == self._buffer[-1][0] == self.evtext:
			self._buffer[-1] = (evtype, self._buffer[-1][1] + evdata)
		else:
			self._buffer.append((evtype, evdata))

	def _flush(self, force):
		# Flush ``self._buffer`` as far as possible
		if force or not self._buffer or self._buffer[-1][0] != self.evtext:
			yield from self._buffer
			del self._buffer[:]
		else:
			# hold back the last text event, because there might be more
			yield from self._buffer[:-1]
			del self._buffer[:-1]

	def handle_comment(self, data):
		self._event(self.evcomment, data)

	def handle_data(self, data):
		self._event(self.evtext, data)

	def handle_cdata(self, data):
		self._event(self.evcdata if self.cdata else self.evtext, data)

	def handle_proc(self, target, data):
		if target.lower() != "xml":
			self._event(self.evprocinst, (target, data))

	def handle_entityref(self, name):
		self._event(self.eventity, name)

	def handle_enterstarttag(self, name):
		self._event(self.eventerstarttag, name)

	def handle_leavestarttag(self, name):
		self._event(self.evleavestarttag, name)

	def handle_enterattr(self, name):
		self._event(self.eventerattr, name)

	def handle_leaveattr(self, name):
		self._event(self.evleaveattr, name)

	def handle_endtag(self, name):
		self._event(self.evendtag, name)


class NS:
	"""
	An :class:`NS` object is used in a parsing pipeline to add support for XML
	namespaces. It replaces the ``"enterstarttag"``, ``"leavestarttag"``,
	``"endtag"``, ``"enterattr"`` and ``"leaveattr"`` events with the appropriate
	namespace version of the events (i.e. ``"enterstarttagns"`` etc.) where the
	event data is a ``(namespace, name)`` tuple.

	The output of an :class:`NS` object in the stream looks like this::

		>>> from ll.xist import parse
		>>> from ll.xist.ns import html
		>>> list(parse.events(
		... 	parse.String(b"<a href='http://www.python.org/'>Python</a>"),
		... 	parse.Expat(),
		... 	parse.NS(html)
		... ))
		[('url', URL('STRING')),
		 ('position', (0, 0)),
		 ('enterstarttagns', ('http://www.w3.org/1999/xhtml', 'a')),
		 ('enterattrns', (None, 'href')),
		 ('text', 'http://www.python.org/'),
		 ('leaveattrns', (None, 'href')),
		 ('leavestarttagns', ('http://www.w3.org/1999/xhtml', 'a')),
		 ('position', (0, 39)),
		 ('text', 'Python'),
		 ('endtagns', ('http://www.w3.org/1999/xhtml', 'a'))]
	"""

	def __init__(self, prefixes=None, **kwargs):
		"""
		Create an :class:`NS` object. :obj:`prefixes` (if not :const:`None`) can
		be a namespace name (or module), which will be used for the empty prefix,
		or a dictionary that maps prefixes to namespace names (or modules).
		:obj:`kwargs` maps prefixes to namespaces names too. If a prefix is in both
		:obj:`prefixes` and :obj:`kwargs`, :obj:`kwargs` wins.
		"""
		# the currently active prefix mapping (will be replaced once xmlns attributes are encountered)
		newprefixes = {}

		def make(prefix, xmlns):
			if prefix is not None and not isinstance(prefix, str):
				raise TypeError(f"prefix must be None or string, not {type(prefix)!r}")
			xmlns = xsc.nsname(xmlns)
			if not isinstance(xmlns, str):
				raise TypeError(f"xmlns must be string, not {type(xmlns)!r}")
			newprefixes[prefix] = xmlns

		if prefixes is not None:
			if isinstance(prefixes, dict):
				for (prefix, xmlns) in prefixes.items():
					make(prefix, xmlns)
			else:
				make(None, prefixes)

		for (prefix, xmlns) in kwargs.items():
			make(prefix, xmlns)
		self._newprefixes = self._attrs = self._attr = None
		# A stack entry is an ``((namespacename, elementname), prefixdict)`` tuple
		self._prefixstack = [(None, newprefixes)]

	def __call__(self, input):
		for (evtype, data) in input:
			try:
				handler = getattr(self, evtype)
			except AttributeError:
				raise UnknownEventError(self, (evtype, data))
			yield from handler(data)

	def url(self, data):
		yield ("url", data)

	def xmldecl(self, data):
		data = ("xmldecl", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def begindoctype(self, data):
		data = ("begindoctype", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def enddoctype(self, data):
		data = ("enddoctype", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def comment(self, data):
		data = ("comment", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def text(self, data):
		data = ("text", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def cdata(self, data):
		data = ("cdata", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def procinst(self, data):
		data = ("procinst", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def entity(self, data):
		data = ("entity", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def position(self, data):
		data = ("position", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def enterstarttag(self, data):
		self._newprefixes = {}
		self._attrs = {}
		self._attr = None
		if 0:
			yield False

	def enterattr(self, data):
		if data == "xmlns" or data.startswith("xmlns:"):
			prefix = data[6:] or None
			self._newprefixes[prefix] = self._attr = []
		else:
			self._attrs[data] = self._attr = []
		if 0:
			yield False

	def leaveattr(self, data):
		self._attr = None
		if 0:
			yield False

	def leavestarttag(self, data):
		oldprefixes = self._prefixstack[-1][1]

		if self._newprefixes:
			prefixes = oldprefixes.copy()
			newprefixes = {key: "".join(d for (t, d) in value if t == "text") or None for (key, value) in self._newprefixes.items()}
			prefixes.update(newprefixes)
		else:
			prefixes = oldprefixes

		(prefix, sep, name) = data.rpartition(":")
		prefix = prefix or None

		try:
			data = (prefixes[prefix], name)
		except KeyError:
			raise xsc.IllegalPrefixError(prefix)

		self._prefixstack.append((data, prefixes))

		yield ("enterstarttagns", data)
		for (attrname, attrvalue) in self._attrs.items():
			if ":" in attrname:
				(attrprefix, attrname) = attrname.split(":", 1)
				if attrprefix == "xml":
					xmlns = xsc.xml_xmlns
				else:
					try:
						xmlns = prefixes[attrprefix]
					except KeyError:
						raise xsc.IllegalPrefixError(attrprefix)
			else:
				xmlns = None
			yield ("enterattrns", (xmlns, attrname))
			yield from attrvalue
			yield ("leaveattrns", (xmlns, attrname))
		yield ("leavestarttagns", data)
		self._newprefixes = self._attrs = self._attr = None

	def endtag(self, data):
		(data, prefixes) = self._prefixstack.pop()
		yield ("endtagns", data)


class Node:
	"""
	A :class:`Node` object is used in a parsing pipeline to instantiate XIST
	nodes. It consumes a namespaced event stream::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import html
		>>> list(parse.events(
		... 	parse.String(b"<a href='http://www.python.org/'>Python</a>"),
		... 	parse.Expat(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(html))
		... ))
		[('enterelementnode',
		  <element ll.xist.ns.html.a xmlns='http://www.w3.org/1999/xhtml' (no children/1 attr) location='STRING:0:0' at 0x10a683550>),
		 ('textnode',
		  <ll.xist.xsc.Text content='Python' location='STRING:0:39' at 0x10a5e1170>),
		 ('leaveelementnode',
		  <element ll.xist.ns.html.a xmlns='http://www.w3.org/1999/xhtml' (no children/1 attr) location='STRING:0:0' at 0x10a683550>)
		]

	The event data of all events are XIST nodes. The element node from the
	``"enterelementnode"`` event already has all attributes set. There will be
	no events for attributes.
	"""
	def __init__(self, pool=None, base=None, loc=True):
		"""
		Create a :class:`Node` object.

		:obj:`pool` may be ``None`` or a :class:`xsc.Pool` object and specifies
		which classes used for creating element, entity and processsing
		instruction instances.

		:obj:`base` specifies the base URL for interpreting relative links in
		the input.

		:obj:`loc` specified whether location information should be attached to
		the nodes that get generated (the :obj:`startloc` attribute (and
		:obj:`endloc` attribute for elements))
		"""
		self.pool = (pool if pool is not None else xsc.threadlocalpool.pool)
		if base is not None:
			base = url_.URL(base)
		self._base = base
		self._url = url_.URL()
		self.loc = loc
		self._position = (None, None)
		self._stack = []
		self._inattr = False
		self._indoctype = False

	@property
	def base(self):
		if self._base is None:
			return self._url
		else:
			return self._base

	def __call__(self, input):
		for (evtype, data) in input:
			try:
				handler = getattr(self, evtype)
			except AttributeError:
				raise UnknownEventError(self, (evtype, data))
			event = handler(data)
			if event:
				yield event

	def url(self, data):
		self._url = data

	def xmldecl(self, data):
		node = xml.XML(version=data["version"], encoding=data["encoding"], standalone=data["standalone"])
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		return ("xmldeclnode", node)

	def begindoctype(self, data):
		if data["publicid"]:
			content = f'{data["name"]} PUBLIC "{data["publicid"]}" "{data["systemid"]}"'
		elif data["systemid"]:
			content = f'{data["name"]} SYSTEM "{data["systemid"]}"'
		else:
			content = data["name"]
		node = xsc.DocType(content)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		self.doctype = node
		self._indoctype = True

	def enddoctype(self, data):
		result = ("doctypenode", self.doctype)
		del self.doctype
		self._indoctype = False
		return result

	def entity(self, data):
		node = self.pool.entity(data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		node.parsed(self, "entity")
		if self._inattr:
			self._stack[-1].append(node)
		elif not self._indoctype:
			return ("entitynode", node)

	def comment(self, data):
		node = xsc.Comment(data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		node.parsed(self, "comment")
		if self._inattr:
			self._stack[-1].append(node)
		elif not self._indoctype:
			return ("commentnode", node)

	def cdata(self, data):
		node = xsc.Text(data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		node.parsed(self, "cdata")
		if self._inattr:
			self._stack[-1].append(node)
		elif not self._indoctype:
			return ("textnode", node)

	def text(self, data):
		node = xsc.Text(data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		node.parsed(self, "text")
		if self._inattr:
			self._stack[-1].append(node)
		elif not self._indoctype:
			return ("textnode", node)

	def enterstarttagns(self, data):
		node = self.pool.element(*data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		self._stack.append(node)
		node.parsed(self, "starttagns")

	def enterattrns(self, data):
		attrkey = self.pool.attrkey(*data)
		self._stack[-1].attrs[attrkey] = ()
		node = self._stack[-1].attrs[attrkey]
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		self._stack.append(node)
		self._inattr = True
		node.parsed(self, "enterattrns")

	def leaveattrns(self, data):
		node = self._stack.pop()
		self._inattr = False
		node.parsed(self, "leaveattrns")

	def leavestarttagns(self, data):
		node = self._stack[-1]
		node.parsed(self, "leavestarttagns")
		return ("enterelementnode", node)

	def endtagns(self, data):
		node = self._stack.pop()
		if self.loc:
			node.endloc = xsc.Location(self._url, *self._position)
		node.parsed(self, "endtagns")
		return ("leaveelementnode", node)

	def procinst(self, data):
		node = self.pool.procinst(*data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		node.parsed(self, "procinst")
		if self._inattr:
			self._stack[-1].append(node)
		elif not self._indoctype:
			return ("procinstnode", node)

	def position(self, data):
		self._position = data


class Tidy:
	"""
	A :class:`Tidy` object parses (potentially ill-formed) HTML from a source
	into a (non-namespaced) event stream by using lxml__'s HTML parser::

		>>> from ll.xist import parse
		>>> list(parse.events(parse.URL("http://www.yahoo.com/"), parse.Tidy()))
		[('url', URL('http://de.yahoo.com/?p=us')),
		 ('enterstarttag', 'html'),
		 ('enterattr', 'class'),
		 ('text', 'y-fp-bg y-fp-pg-grad  bkt708'),
		 ('leaveattr', 'class'),
		 ('enterattr', 'lang'),
		 ('text', 'de-DE'),
		 ('leaveattr', 'lang'),
		 ('enterattr', 'style'),
		 ('leaveattr', 'style'),
		 ('leavestarttag', 'html'),
		...

	__ http://lxml.de/
	"""

	def __init__(self, encoding=None, xmldecl=False, doctype=False):
		"""
		Create a new :class:`Tidy` object. Parameters have the following meaning:

		:obj:`encoding` : string or :const:`None`
			The encoding of the input. If :obj:`encoding` is :const:`None` it will
			be automatically detected by the HTML parser.

		:obj:`xmldecl` : bool
			Should the parser produce events for the XML declaration?

		:obj:`doctype` : bool
			Should the parser produce events for the document type?
		"""
		self.encoding = encoding
		self.xmldecl = xmldecl
		self.doctype = doctype

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object encoding={self.encoding!r} at {id(self):#x}>"

	def _asxist(self, node):
		name = type(node).__name__
		if "ElementTree" in name:
			if self.xmldecl:
				yield ("xmldecl", {"version": node.docinfo.xml_version or "1.0", "encoding": node.docinfo.encoding, "standalone": node.docinfo.standalone})
			if self.doctype:
				yield ("begindoctype", {"name": node.docinfo.root_name, "publicid": node.docinfo.public_id, "systemid": node.docinfo.system_url})
				yield ("enddoctype", None)
			yield from self._asxist(node.getroot())
		elif "Element" in name:
			elementname = node.tag
			yield ("enterstarttag", elementname)
			for (attrname, attrvalue) in sorted(node.items()):
				yield ("enterattr", attrname)
				if attrvalue:
					yield ("text", attrvalue)
				yield ("leaveattr", attrname)
			yield ("leavestarttag", elementname)
			if node.text:
				yield ("text", node.text)
			for child in node:
				yield from self._asxist(child)
				if hasattr(child, "tail") and child.tail:
					yield ("text", child.tail)
			yield ("endtag", elementname)
		elif "ProcessingInstruction" in name:
			yield ("procinst", (node.target, node.text))
		elif "Comment" in name:
			yield ("comment", node.text)
		# ignore all other types

	def __call__(self, input):
		from lxml import etree # This requires lxml (see http://lxml.de/)

		url = None
		collectdata = []
		for (evtype, data) in input:
			if evtype == "url":
				if url is None:
					url = data
				else:
					raise ValueError("got multiple url events")
			elif evtype == "bytes":
				collectdata.append(data)
			else:
				raise UnknownEventError(self, (evtype, data))
		data = b"".join(collectdata)
		if url is not None:
			yield ("url", url)
		if data:
			parser = etree.HTMLParser(encoding=self.encoding)
			doc = etree.parse(io.BytesIO(data), parser)
			yield from self._asxist(doc)


###
### Consumers: Functions that consume an event stream
###

def events(*pipeline):
	"""
	Return an iterator over the events produced by the pipeline objects in
	:obj:`pipeline`.
	"""
	source = pipeline[0]

	# Propagate first pipeline object to a source object (if unambiguous, else use it as it is)
	if isinstance(source, (bytes, str)):
		source = String(source)
	elif isinstance(source, url_.URL):
		source = URL(source)

	# Execute the pipeline, propagating pipeline objects in the process
	output = iter(source)
	for pipe in pipeline[1:]:
		if isinstance(pipe, xsc.Pool):
			pipe = Node(pool=pipe)
		output = pipe(output)
	return output


def tree(*pipeline, validate=False):
	"""
	Return a tree of XIST nodes from the event stream :obj:`pipeline`.

	:obj:`pipeline` must output only events that contain XIST nodes, i.e. the
	event types ``"xmldeclnode"``, ``"doctypenode"``, ``"commentnode"``,
	``"textnode"``, ``"enterelementnode"``, ``"leaveelementnode"``,
	``"procinstnode"`` and ``"entitynode"``.

	If :obj:`validate` is true, the tree is validated, i.e. it is checked if
	the structure of the tree is valid (according to the :obj:`model` attribute
	of each element node), if no undeclared elements or attributes have been
	encountered, all required attributes are specified and all
	attributes have allowed values.

	The node returned from :func:`tree` will always be a :class:`Frag` object.

	Example::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("http://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )

		>>> doc[0]
		<element ll.xist.ns.html.html
			xmlns='http://www.w3.org/1999/xhtml'
			(7 children/3 attrs)
			location='https://www.python.org/:?:?'
			at 0x110a4ecd0>
	"""
	path = [xsc.Frag()]
	for (evtype, node) in events(*pipeline):
		if evtype == "enterelementnode":
			path[-1].append(node)
			path.append(node)
		elif evtype == "leaveelementnode":
			if validate:
				for warning in node.validate(False, path):
					warnings.warn(warning)
			path.pop()
		else:
			path[-1].append(node)
			if validate:
				for warning in node.validate(False, path):
					warnings.warn(warning)
	return path[0]


def itertree(*pipeline, entercontent=True, enterattrs=False, enterattr=False, enterelementnode=False, leaveelementnode=True, enterattrnode=True, leaveattrnode=False, selector=None, validate=False):
	"""
	Parse the event stream :obj:`pipeline` iteratively.

	:func:`itertree` still builds a tree, but it returns an iterator of
	:class:`xsc.Cursor` objects that tracks changes to the tree as it is built.

	:obj:`validate` specifies whether each node should be validated after it has
	been fully parsed.

	The rest of the arguments can be used to control when :func:`itertree`
	returns to the calling code. For an explanation of their meaning see the
	class :class:`ll.xist.xsc.Cursor`.

	Example::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import xml, html, chars
		>>> for c in parse.itertree(
		... 	parse.URL("http://www.python.org/"),
		... 	parse.Tidy(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars)),
		... 	selector=html.a/html.img
		... ):
		...	print(c.path[-1].attrs.src, "-->", c.path[-2].attrs.href)

		https://www.python.org/static/img/python-logo.png --> https://www.python.org/
	"""
	selector = xfind.selector(selector)
	cursor = xsc.Cursor(xsc.Frag(), entercontent=entercontent, enterattrs=enterattrs, enterattr=enterattr, enterelementnode=enterelementnode, leaveelementnode=leaveelementnode, enterattrnode=enterattrnode, leaveattrnode=leaveattrnode)
	cursor.index.append(0)
	skipcontent = None # If this is not ``None``, we're currently skipping past the content of this element
	for (evtype, node) in events(*pipeline):
		cursor.event = evtype
		if evtype == "enterelementnode":
			cursor.path[-1].append(node)
			cursor.path.append(node)
			cursor.node = node
			enterattrs = cursor.enterattrs
			entercontent = cursor.entercontent
			if cursor.enterelementnode and cursor.path in selector and skipcontent is None:
				yield cursor
				enterattrs = cursor.enterattrs
				entercontent = cursor.entercontent
				cursor.restore()
			if enterattrs:
				yield from node.attrs._walk(cursor)
			cursor.index.append(0)
			if not entercontent and skipcontent is None:
				# Skip all events until we leave this element
				skipcontent = cursor.node
		elif evtype == "leaveelementnode":
			if validate:
				for warning in node.validate(False, cursor.path):
					warnings.warn(warning)
			cursor.index.pop()
			if skipcontent is cursor.node:
				skipcontent = None
			if cursor.leaveelementnode and cursor.path in selector and skipcontent is None:
				yield cursor
				cursor.restore()
			cursor.path.pop()
			cursor.node = cursor.path[-1]
			cursor.index[-1] += 1
		else:
			cursor.path[-1].append(node)
			cursor.path.append(node)
			cursor.node = node
			if validate:
				for warning in node.validate(False, cursor.path):
					warnings.warn(warning)
			if cursor.path in selector and skipcontent is None:
				yield cursor
				cursor.restore()
			cursor.path.pop()
			cursor.node = cursor.path[-1]
			cursor.index[-1] += 1
