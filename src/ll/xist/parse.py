# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


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
	>>> source = "<a href='http://www.python.org/'>Python</a>"
	>>> doc = parse.tree(
	... 	parse.String(source)
	... 	parse.Expat()
	... 	parse.NS(html)
	... 	parse.Node(pool=xsc.Pool(html))
	... )
	>>> doc.bytes()
	'<a href="http://www.python.org/">Python</a>'

A source object is an iterable object that produces the input byte string for
the parser (possibly in multiple chunks) (and information about the URL of the
input)::

	>>> from ll.xist import parse
	>>> list(parse.String("<a href='http://www.python.org/'>Python</a>"))
	[('url', URL('STRING')),
	 ('bytes', "<a href='http://www.python.org/'>Python</a>")]

All subsequent objects in the pipeline are callable objects, get the input
iterator as an argument and return an iterator over events themselves. The
following code shows an example of an event stream::

	>>> from ll.xist import parse
	>>> source = "<a href='http://www.python.org/'>Python</a>"
	>>> list(parse.events(parse.String(source), parse.Expat()))
	[('url', URL('STRING')),
	 ('position', (0, 0)),
	 ('enterstarttag', u'a'),
	 ('enterattr', u'href'),
	 ('text', u'http://www.python.org/'),
	 ('leaveattr', u'href'),
	 ('leavestarttag', u'a'),
	 ('position', (0, 39)),
	 ('text', u'Python'),
	 ('endtag', u'a')]

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

	``"unicode"``
		The event data is a unicode string. This event is produced by
		:class:`Decoder` objects. Note that the only predefined pipeline objects
		that can handle ``"unicode"`` events are :class:`Encoder` objects.

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
objects or by :class:`Expat` objects when :var:`ns` is true (i.e. the expat
parser does the namespace resolution):

	``"enterstarttagns"``
		The beginning of an element start tag in namespace mode.
		The event data is an (element name, namespace name) tuple.

	``"leavestarttagns"``
		The end of an element start tag in namespace mode. The event data is an
		(element name, namespace name) tuple.

	``"enterattrns"``
		The beginning of an attribute in namespace mode. The event data is an
		(element name, namespace name) tuple.

	``"leaveattrns"``
		The end of an attribute in namespace mode. The event data is an
		(element name, namespace name) tuple.

	``"endtagns"``
		An element end tag in namespace mode. The event data is an
		(element name, namespace name) tuple.

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

	``"startelementnode"``
		The beginning of an element. The event data is an instance of
		:class:`ll.xist.xsc.Element` (or rather one of its subclasses). The
		attributes of the element object are set, but the element has no content.

	``"endelementnode"``
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
"""


import sys, os, os.path, warnings, cStringIO, codecs, contextlib, types

from xml.parsers import expat

from ll import url as url_, misc, xml_codec
from ll.xist import xsc, xfind
try:
	from ll.xist import sgmlop
except ImportError:
	pass
from ll.xist.ns import xml, html


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
		return "{0.pipe!r} can't handle event type {0.event[0]!r}".format(self)


###
### Sources: Classes that create on event stream
###

class String(object):
	"""
	Provides parser input from a string.
	"""
	def __init__(self, data, url=None):
		"""
		Create a :class:`String` object. :var:`data` must be a byte or
		unicode string. :var:`url` specifies the URL for the source (defaulting
		to ``"STRING"``).
		"""
		self.url = url_.URL(url if url is not None else "STRING")
		self.data = data

	def __iter__(self):
		"""
		Produces an event stream of one ``"url"`` event and one ``"bytes"`` or
		``"unicode"`` event for the data.
		"""
		yield (u"url", self.url)
		if isinstance(self.data, str):
			yield (u"bytes", self.data)
		elif isinstance(self.data, unicode):
			yield (u"unicode", self.data)
		else:
			raise TypeError("data must be str or unicode")


class Iter(object):
	"""
	Provides parser input from an iterator over strings.
	"""

	def __init__(self, iterable, url=None):
		"""
		Create a :class:`Iter` object. :var:`iterable` must be an iterable object
		producing byte or unicode strings. :var:`url` specifies the URL for the
		source (defaulting to ``"ITER"``).
		"""
		self.url = url_.URL(url if url is not None else "ITER")
		self.iterable = iterable

	def __iter__(self):
		"""
		Produces an event stream of one ``"url"`` event followed by the
		``"bytes"``/``"unicode"`` events for the data from the iterable.
		"""
		yield (u"url", self.url)
		for data in self.iterable:
			if isinstance(data, str):
				yield (u"bytes", data)
			elif isinstance(data, unicode):
				yield (u"unicode", data)
			else:
				raise TypeError("data must be str or unicode")


class Stream(object):
	"""
	Provides parser input from a stream (i.e. an object that provides a
	:meth:`read` method).
	"""

	def __init__(self, stream, url=None, bufsize=8192):
		"""
		Create a :class:`Stream` object. :var:`stream` must have a :meth:`read`
		method (with a ``size`` argument). :var:`url` specifies the URL for the
		source (defaulting to ``"STREAM"``). :var:`bufsize` specifies the
		chunksize for reads from the stream.
		"""
		self.url = url_.URL(url if url is not None else "STREAM")
		self.stream = stream
		self.bufsize = bufsize

	def __iter__(self):
		"""
		Produces an event stream of one ``"url"`` event followed by the
		``"bytes"``/``"unicode"`` events for the data from the stream.
		"""
		yield (u"url", self.url)
		while True:
			data = self.stream.read(self.bufsize)
			if data:
				if isinstance(data, str):
					yield (u"bytes", data)
				elif isinstance(data, unicode):
					yield (u"unicode", data)
				else:
					raise TypeError("data must be str or unicode")
			else:
				break


class File(object):
	"""
	Provides parser input from a file.
	"""

	def __init__(self, filename, bufsize=8192):
		"""
		Create a :class:`File` object. :var:`filename` is the name of the file
		and may start with ``~`` or ``~user`` for the home directory of the
		current or the specified user. :var:`bufsize` specifies the chunksize
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
		yield (u"url", self.url)
		with open(self._filename, "rb") as stream:
			while True:
				data = stream.read(self.bufsize)
				if data:
					yield (u"bytes", data)
				else:
					break


class URL(object):
	"""
	Provides parser input from a URL.
	"""

	def __init__(self, name, bufsize=8192, *args, **kwargs):
		"""
		Create a :class:`URL` object. :var:`name` is the URL. :var:`bufsize`
		specifies the chunksize for reads from the URL. :var:`args` and
		:var:`kwargs` will be passed on to the :meth:`open` method of the URL
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
		yield (u"url", stream.finalurl())
		with contextlib.closing(stream) as stream:
			while True:
				data = stream.read(self.bufsize)
				if data:
					yield (u"bytes", data)
				else:
					break


class ETree(object):
	"""
	Produces a (namespaced) event stream from an object that supports the
	ElementTree__ API.

	__ http://effbot.org/zone/element-index.htm
	"""

	def __init__(self, data, url=None, defaultxmlns=None):
		"""
		Create an :class:`ETree` object. Arguments have the following meaning:

		:var:`data`
			An object that supports the ElementTree API.

		:var:`url`
			The URL of the source. Defaults to ``"ETREE"``.

		:var:`defaultxmlns`
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
			yield (u"enterstarttagns", (elementname, elementxmlns))
			for (attrname, attrvalue) in node.items():
				if attrname.startswith("{"):
					(attrxmlns, sep, attrname) = attrname[1:].partition("}")
				else:
					attrxmlns = None
				yield (u"enterattrns", (attrname, attrxmlns))
				yield (u"text", attrvalue)
				yield (u"leaveattrns", (attrname, attrxmlns))
			yield (u"leavestarttagns", (elementname, elementxmlns))
			if node.text:
				yield (u"text", node.text)
			for child in node:
				for event in self._asxist(child):
					yield event
				if hasattr(child, "tail") and child.tail:
					yield (u"text", child.tail)
			yield (u"endtagns", (elementname, elementxmlns))
		elif "ProcessingInstruction" in name:
			yield (u"procinst", (node.target, node.text))
		elif "Comment" in name:
			yield (u"comment", node.text)

	def __iter__(self):
		"""
		Produces an event stream of namespaced parsing events for the ElementTree
		object passed as :var:`data` to the constructor.
		"""
		yield (u"url", self.url)
		for event in self._asxist(self.data):
			yield event


###
### Transformers: Classes that transform the event stream.
###

class Decoder(object):
	"""
	Decode the byte strings produced by the previous object in the pipeline to
	unicode strings.

	This input object can be a source object or any other pipeline object that
	produces byte strings.
	"""

	def __init__(self, encoding=None):
		"""
		Create a :class:`Decoder` object. :var:`encoding` is the encoding of the
		input. If :var:`encoding` is ``None`` it will be automatically detected
		from the XML data.
		"""
		self.encoding = encoding

	def __call__(self, input):
		decoder = codecs.getincrementaldecoder("xml")(encoding=self.encoding)
		for (evtype, data) in input:
			if evtype == u"bytes":
				data = decoder.decode(data, False)
				if data:
					yield (u"unicode", data)
			elif evtype == u"unicode":
				if data:
					yield (u"unicode", data)
			elif evtype == u"url":
				yield (u"url", data)
			else:
				raise UnknownEventError(self, (evtype, data))
		data = decoder.decode("", True)
		if data:
			yield (u"unicode", data)

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object encoding={0.encoding!r} at {1:#x}>".format(self, id(self))


class Encoder(object):
	"""
	Encode the unicode strings produced by the previous object in the pipeline to
	byte strings.

	This input object must be a pipeline object that produces unicode output
	(e.g. a :class:`Decoder` object).
	"""

	def __init__(self, encoding=None):
		"""
		Create an :class:`Encoder` object. :var:`encoding` will be the encoding of
		the output. If :var:`encoding` is ``None`` it will be automatically
		detected from the XML declaration in the data.
		"""
		self.encoding = encoding

	def __call__(self, input):
		encoder = codecs.getincrementalencoder("xml")(encoding=self.encoding)
		for (evtype, data) in input:
			if evtype == u"unicode":
				data = encoder.encode(data, False)
				if data:
					yield (u"bytes", data)
			elif evtype == u"bytes":
				if data:
					yield (u"bytes", data)
			elif evtype == u"url":
				yield (u"url", data)
			else:
				raise UnknownEventError(self, (evtype, data))
		data = encoder.encode(u"", True)
		if data:
			yield (u"bytes", data)

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object encoding={0.encoding!r} at {1:#x}>".format(self, id(self))


class Transcoder(object):
	"""
	Transcode the byte strings of the input object into another encoding.

	This input object can be a source object or any other pipeline object that
	produces byte strings.
	"""

	def __init__(self, fromencoding=None, toencoding=None):
		"""
		Create a :class:`Transcoder` object. :var:`fromencoding` is the encoding
		of the input. :var:`toencoding` is the encoding of the output. If any of
		them is ``None`` the encoding will be detected from the data.
		"""
		self.fromencoding = fromencoding
		self.toencoding = toencoding

	def __call__(self, input):
		decoder = codecs.getincrementaldecoder("xml")(encoding=self.fromencoding)
		encoder = codecs.getincrementalencoder("xml")(encoding=self.toencoding)
		for (evtype, data) in input:
			if evtype == u"bytes":
				data = encoder.encode(decoder.decode(data, False), False)
				if data:
					yield (u"bytes", data)
			elif evtype == u"url":
				yield (u"url", data)
			else:
				raise UnknownEventError(self, (evtype, data))
		data = encoder.encode(decoder.decode("", True), True)
		if data:
			yield (u"bytes", data)

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object fromencoding={0.fromencoding!r} toencoding={0.toencoding!r} at {1:#x}>".format(self, id(self))


###
### Parsers
###

class Parser(object):
	"""
	Basic parser interface.
	"""
	evxmldecl = u"xmldecl"
	evbegindoctype = u"begindoctype"
	evenddoctype = u"enddoctype"
	evcomment = u"comment"
	evtext = u"text"
	evcdata = u"cdata"
	eventerstarttag = u"enterstarttag"
	eventerstarttagns = u"enterstarttagns"
	eventerattr = u"enterattr"
	eventerattrns = u"enterattrns"
	evleaveattr = u"leaveattr"
	evleaveattrns = u"leaveattrns"
	evleavestarttag = u"leavestarttag"
	evleavestarttagns = u"leavestarttagns"
	evendtag = u"endtag"
	evendtagns = u"endtagns"
	evprocinst = u"procinst"
	eventity = u"entity"
	evposition = u"position"
	evurl = u"url"


class Expat(Parser):
	"""
	A parser using Pythons builtin :mod:`expat` parser.
	"""

	def __init__(self, encoding=None, xmldecl=False, doctype=False, loc=True, cdata=False, ns=False):
		"""
		Create an :class:`Expat` parser. Arguments have the following meaning:

		:var:`encoding` : string or :const:`None`
			Forces the parser to use the specified encoding. The default
			:const:`None` results in the encoding being detected from the XML itself.

		:var:`xmldecl` : bool
			Should the parser produce events for the XML declaration?

		:var:`doctype` : bool
			Should the parser produce events for the document type?

		:var:`loc` : bool
			Should the parser produce ``"location"`` events?

		:var:`cdata` : bool
			Should the parser output CDATA sections as ``"cdata"`` events? (If
			:var:`cdata` is false output ``"text"`` events instead.)

		:var:`ns` : bool
			If :var:`ns` is true, the parser does its own namespace processing,
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
			v.append(" encoding={!r}".format(self.encoding))
		if self.xmldecl is not None:
			v.append(" xmldecl={!r}".format(self.xmldecl))
		if self.doctype is not None:
			v.append(" doctype={!r}".format(self.doctype))
		if self.loc is not None:
			v.append(" loc={!r}".format(self.loc))
		if self.cdata is not None:
			v.append(" cdata={!r}".format(self.cdata))
		if self.ns is not None:
			v.append(" ns={!r}".format(self.ns))
		return "<{0.__class__.__module__}.{0.__class__.__name__} object{1} at {2:#x}>".format(self, "".join(v), id(self))

	def __call__(self, input):
		"""
		Return an iterator over the events produced by :var:`input`.
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
				if evtype == u"bytes":
					try:
						self._parser.Parse(data, False)
					except Exception, exc:
						# In case of an exception we want to output the events we have gathered so far, before reraising the exception
						for event in self._flush(True):
							yield event
						raise exc
					else:
						for event in self._flush(False):
							yield event
				elif evtype == u"url":
					yield (self.evurl, data)
				else:
					raise UnknownEventError(self, (evtype, data))
			try:
				self._parser.Parse(b"", True)
			except Exception, exc:
				for event in self._flush(True):
					yield event
				raise exc
			else:
				for event in self._flush(True):
					yield event
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
			self._currentloc = loc

	def _flush(self, force):
		# Flush ``self._buffer`` as far as possible
		if force or not self._buffer or self._buffer[-1][0] != self.evtext:
			for event in self._buffer:
				yield event
			del self._buffer[:]
		else:
			# hold back the last text event, because there might be more
			for event in self._buffer[:-1]:
				yield event
			del self._buffer[:-1]

	def _getname(self, name):
		if self.ns:
			if "\x01" in name:
				return tuple(name.split("\x01")[::-1])
			return (name, None)
		return name

	def _handle_startcdata(self):
		self._incdata = True

	def _handle_endcdata(self):
		self._incdata = False

	def _handle_xmldecl(self, version, encoding, standalone):
		standalone = (bool(standalone) if standalone != -1 else None)
		self._event(self.evxmldecl, {u"version": version, u"encoding": encoding, u"standalone": standalone})

	def _handle_begindoctype(self, doctypename, systemid, publicid, has_internal_subset):
		if self.doctype:
			self._event(self.evbegindoctype, {u"name": doctypename, u"publicid": publicid, u"systemid": systemid})

	def _handle_enddoctype(self):
		if self.doctype:
			self._event(self.evenddoctype, None)

	def _handle_default(self, data):
		if data.startswith(u"&") and data.endswith(u";"):
			self._event(self.eventity, data[1:-1])

	def _handle_comment(self, data):
		if not self._indoctype:
			self._event(self.evcomment, data)

	def _handle_text(self, data):
		self._event(self.evcdata if self._incdata else self.evtext, data)

	def _handle_startelement(self, name, attrs):
		name = self._getname(name)
		self._event(self.eventerstarttagns if self.ns else self.eventerstarttag, name)
		for i in xrange(0, len(attrs), 2):
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

		:var:`encoding` : string or :const:`None`
			Forces the parser to use the specified encoding. The default
			:const:`None` results in the encoding being detected from the XML itself.

		:var:`cdata` : bool
			Should the parser output CDATA sections as ``"cdata"`` events? (If
			:var:`cdata` is false output ``"text"`` events instead.)
		"""
		self.encoding = encoding
		self.cdata = cdata

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object encoding={0.encoding!r} at {1:#x}>".format(self, id(self))

	def __call__(self, input):
		"""
		Return an iterator over the events produced by :var:`input`.
		"""
		self._decoder = codecs.getincrementaldecoder("xml")(encoding=self.encoding)
		self._parser = sgmlop.XMLParser()
		self._parser.register(self)
		self._buffer = []
		self._hadtext = False

		try:
			for (evtype, data) in input:
				if evtype == u"bytes":
					try:
						self._parser.feed(self._decoder.decode(data, False))
					except Exception, exc:
						# In case of an exception we want to output the events we have gathered so far, before reraising the exception
						for event in self._flush(True):
							yield event
						self._parser.close()
						raise exc
					else:
						for event in self._flush(False):
							yield event
				elif evtype == u"url":
					yield (self.evurl, data)
				else:
					raise UnknownEventError(self, (evtype, data))
			self._parser.close()
			for event in self._flush(True):
				yield event
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
			for event in self._buffer:
				yield event
			del self._buffer[:]
		else:
			# hold back the last text event, because there might be more
			for event in self._buffer[:-1]:
				yield event
			del self._buffer[:-1]

	def handle_comment(self, data):
		self._event(self.evcomment, data)

	def handle_data(self, data):
		self._event(self.evtext, data)

	def handle_cdata(self, data):
		self._event(self.evcdata if self.cdata else self.evtext, data)

	def handle_proc(self, target, data):
		if target.lower() != u"xml":
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


class NS(object):
	"""
	An :class:`NS` object is used in a parsing pipeline to add support for XML
	namespaces. It replaces the ``"enterstarttag"``, ``"leavestarttag"``,
	``"endtag"``, ``"enterattr"`` and ``"leaveattr"`` events with the appropriate
	namespace version of the events (i.e. ``"enterstarttagns"`` etc.) where the
	event data is a ``(name, namespace)`` tuple.

	The output of an :class:`NS` object in the stream looks like this::

		>>> from ll.xist import parse
		>>> from ll.xist.ns import html
		>>> list(parse.events(
		... 	parse.String("<a href='http://www.python.org/'>Python</a>"),
		... 	parse.Expat(),
		... 	parse.NS(html)
		... ))
		[('url', URL('STRING')),
		 ('position', (0, 0)),
		 ('enterstarttagns', (u'a', 'http://www.w3.org/1999/xhtml')),
		 ('enterattrns', (u'href', None)),
		 ('text', u'http://www.python.org/'),
		 ('leaveattrns', (u'href', None)),
		 ('leavestarttagns', (u'a', 'http://www.w3.org/1999/xhtml')),
		 ('position', (0, 39)),
		 ('text', u'Python'),
		 ('endtagns', (u'a', 'http://www.w3.org/1999/xhtml'))]
	"""

	def __init__(self, prefixes=None, **kwargs):
		"""
		Create an :class:`NS` object. :var:`prefixes` (if not ``None``) can be a
		namespace name (or module), which will be used for the empty prefix,
		or a dictionary that maps prefixes to namespace names (or modules).
		:var:`kwargs` maps prefixes to namespaces names too. If a prefix is in both
		:var:`prefixes` and :var:`kwargs`, :var:`kwargs` wins.
		"""
		# the currently active prefix mapping (will be replaced once xmlns attributes are encountered)
		newprefixes = {}

		def make(prefix, xmlns):
			if prefix is not None and not isinstance(prefix, basestring):
				raise TypeError("prefix must be None or string, not {!r}".format(prefix))
			xmlns = xsc.nsname(xmlns)
			if not isinstance(xmlns, basestring):
				raise TypeError("xmlns must be string, not {!r}".format(xmlns))
			newprefixes[prefix] = xmlns

		if prefixes is not None:
			if isinstance(prefixes, dict):
				for (prefix, xmlns) in prefixes.iteritems():
					make(prefix, xmlns)
			else:
				make(None, prefixes)

		for (prefix, xmlns) in kwargs.iteritems():
			make(prefix, xmlns)
		self._newprefixes = self._attrs = self._attr = None
		# A stack entry is an ``((elementname, namespacename), prefixdict)`` tuple
		self._prefixstack = [(None, newprefixes)]

	def __call__(self, input):
		for (evtype, data) in input:
			try:
				handler = getattr(self, evtype)
			except AttributeError:
				raise UnknownEventError(self, (evtype, data))
			for event in handler(data):
				yield event

	def url(self, data):
		yield (u"url", data)

	def xmldecl(self, data):
		data = (u"xmldecl", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def begindoctype(self, data):
		data = (u"begindoctype", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def enddoctype(self, data):
		data = (u"enddoctype", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def comment(self, data):
		data = (u"comment", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def text(self, data):
		data = (u"text", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def cdata(self, data):
		data = (u"cdata", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def procinst(self, data):
		data = (u"procinst", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def entity(self, data):
		data = (u"entity", data)
		if self._attr is not None:
			self._attr.append(data)
		else:
			yield data

	def position(self, data):
		data = (u"position", data)
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
		if data==u"xmlns" or data.startswith(u"xmlns:"):
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
			newprefixes = {key: u"".join(d for (t, d) in value if t == u"text") for (key, value) in self._newprefixes.iteritems()}
			prefixes.update(newprefixes)
		else:
			prefixes = oldprefixes

		(prefix, sep, name) = data.rpartition(u":")
		prefix = prefix or None

		try:
			data = (name, prefixes[prefix])
		except KeyError:
			raise xsc.IllegalPrefixError(prefix)

		self._prefixstack.append((data, prefixes))

		yield (u"enterstarttagns", data)
		for (attrname, attrvalue) in self._attrs.iteritems():
			if u":" in attrname:
				(attrprefix, attrname) = attrname.split(u":", 1)
				if attrprefix == "xml":
					xmlns = xsc.xml_xmlns
				else:
					try:
						xmlns = prefixes[attrprefix]
					except KeyError:
						raise xsc.IllegalPrefixError(attrprefix)
			else:
				xmlns = None
			yield (u"enterattrns", (attrname, xmlns))
			for event in attrvalue:
				yield event
			yield (u"leaveattrns", (attrname, xmlns))
		yield (u"leavestarttagns", data)
		self._newprefixes = self._attrs = self._attr = None

	def endtag(self, data):
		(data, prefixes) = self._prefixstack.pop()
		yield (u"endtagns", data)


class Node(object):
	"""
	A :class:`Node` object is used in a parsing pipeline to instantiate XIST
	nodes. It consumes a namespaced event stream::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import html
		>>> list(parse.events(
		... 	parse.String("<a href='http://www.python.org/'>Python</a>"),
		... 	parse.Expat(),
		... 	parse.NS(html),
		... 	parse.Node(pool=xsc.Pool(html))
		... ))
		[(u'startelementnode',
		  <ll.xist.ns.html.a element object (no children/1 attr) (from STRING:0:0) at 0x1026e6a10>),
		 (u'textnode',
		  <ll.xist.xsc.Text content=u'Python' (from STRING:0:39) at 0x102566b48>),
		 (u'endelementnode',
		  <ll.xist.ns.html.a element object (no children/1 attr) (from STRING:0:0) at 0x1026e6a10>)]

	The event data of all events are XIST nodes. The element node from the
	``"startelementnode"`` event already has all attributes set. There will be
	no events for attributes.
	"""
	def __init__(self, pool=None, base=None, loc=True):
		"""
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
		node = xml.XML(version=data[u"version"], encoding=data[u"encoding"], standalone=data[u"standalone"])
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		return (u"xmldeclnode", node)

	def begindoctype(self, data):
		if data[u"publicid"]:
			fmt = u'{0[name]} PUBLIC "{0[publicid]}" "{0[systemid]}"'
		elif data["systemid"]:
			fmt = u'{0[name]} SYSTEM "{0[systemid]}"'
		else:
			fmt = u'{0[name]}'
		node = xsc.DocType(fmt.format(data))
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		self.doctype = node
		self._indoctype = True

	def enddoctype(self, data):
		result = (u"doctypenode", self.doctype)
		del self.doctype
		self._indoctype = False
		return result

	def entity(self, data):
		node = self.pool.entity_xml(data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		node.parsed(self, u"entity")
		if self._inattr:
			self._stack[-1].append(node)
		elif not self._indoctype:
		 	return (u"entitynode", node)

	def comment(self, data):
		node = xsc.Comment(data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		node.parsed(self, u"comment")
		if self._inattr:
			self._stack[-1].append(node)
		elif not self._indoctype:
			return (u"commentnode", node)

	def cdata(self, data):
		node = xsc.Text(data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		node.parsed(self, u"cdata")
		if self._inattr:
			self._stack[-1].append(node)
		elif not self._indoctype:
			return (u"textnode", node)

	def text(self, data):
		node = xsc.Text(data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		node.parsed(self, u"text")
		if self._inattr:
			self._stack[-1].append(node)
		elif not self._indoctype:
		 	return (u"textnode", node)

	def enterstarttagns(self, data):
		node = self.pool.element_xml(*data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		self._stack.append(node)
		node.parsed(self, u"starttagns")

	def enterattrns(self, data):
		if data[1] is not None:
			node = self.pool.attrclass_xml(*data)
		else:
			node = self._stack[-1].attrs.allowedattr_xml(data[0])
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		self._stack[-1].attrs[node] = ()
		node = self._stack[-1].attrs[node]
		self._stack.append(node)
		self._inattr = True
		node.parsed(self, u"enterattrns")

	def leaveattrns(self, data):
		node = self._stack.pop()
		self._inattr = False
		node.parsed(self, u"leaveattrns")

	def leavestarttagns(self, data):
		node = self._stack[-1]
		node.parsed(self, u"leavestarttagns")
		return (u"startelementnode", node)

	def endtagns(self, data):
		node = self._stack.pop()
		if self.loc:
			node.endloc = xsc.Location(self._url, *self._position)
		node.parsed(self, u"endtagns")
		return (u"endelementnode", node)

	def procinst(self, data):
		node = self.pool.procinst_xml(*data)
		if self.loc:
			node.startloc = xsc.Location(self._url, *self._position)
		node.parsed(self, u"procinst")
		if self._inattr:
			self._stack[-1].append(node)
		elif not self._indoctype:
			return (u"procinstnode", node)

	def position(self, data):
		self._position = data


class Tidy(object):
	"""
	A :class:`Tidy` object parses (potentially ill-formed) HTML from a source
	into a (unnamespaced) event stream by using libxml2__'s HTML parser::

		>>> from ll.xist import parse
		>>> list(parse.events(parse.URL("http://www.yahoo.com/"), parse.Tidy()))
		[('url', URL('http://de.yahoo.com/?p=us')),
		 ('position', (3, None)),
		 ('enterstarttag', u'html'),
		 ('enterattr', u'lang'),
		 ('text', u'de-DE'),
		 ('leaveattr', u'lang'),
		 ('enterattr', u'class'),
		 ('text', u'y-fp-bg y-fp-pg-grad  bkt708'),
		 ('leaveattr', u'class'),
		 ('leavestarttag', u'html')
		...

	__ http://xmlsoft.org/
	"""

	def __init__(self, encoding=None, skipbad=False, loc=True):
		"""
		Create a new :class:`Tidy` object. Parameters have the following meaning:

		:var:`encoding` : string or ``None``
			The encoding of the input. If :var:`encoding` is ``None`` it will
			be automatically detected by the HTML parser.

		:var:`skipbad` : bool
			If :var:`skipbad` is true, unknown elements (i.e. those not in the
			:mod:`ll.xist.ns.html` namespace) will be skipped (i.e. instead of
			the element its content will be output). Unknown attributes will be
			skipped completely.

		:var:`loc` : bool
			If :var:`loc` is true, ``"position"`` events will be generated else
			they will be skipped.
		"""
		self.encoding = encoding
		self.skipbad = skipbad
		self.loc = loc

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object encoding={0.encoding!r} loc={0.loc!r} at {1:#x}>".format(self, id(self))

	def _handle_pos(self, node):
		if self.loc:
			lineno = node.lineNo()
			if lineno != self._lastlineno:
				result = (u"position", (lineno, None))
				self._lastlineno = lineno
				return result

	@staticmethod
	def decode(s):
		try:
			return s.decode("utf-8")
		except UnicodeDecodeError:
			return s.decode("iso-8859-1")

	def _asxist(self, node):
		decode = self.decode
		if node.type == "document_html":
			child = node.children
			while child is not None:
				for event in self._asxist(child):
					yield event
				child = child.next
		elif node.type == "element":
			pos = self._handle_pos(node)
			if pos is not None:
				yield pos
			elementname = decode(node.name).lower()
			if self.skipbad:
				el = getattr(html, elementname, None)
				elok = el is not None
			else:
				elok = True
			if elok:
				yield (u"enterstarttag", elementname)
				attr = node.properties
				while attr is not None:
					attrname = decode(attr.name).lower()
					if not self.skipbad or el.Attrs.isallowed_xml(attrname):
						content = decode(attr.content) if attr.content is not None else u""
						yield (u"enterattr", attrname)
						yield (u"text", content)
						yield (u"leaveattr", attrname)
					attr = attr.next
				yield (u"leavestarttag", elementname)
			child = node.children
			while child is not None:
				for event in self._asxist(child):
					yield event
				child = child.next
			if elok:
				yield (u"endtag", elementname)
		elif node.type == "text":
			pos = self._handle_pos(node)
			if pos is not None:
				yield pos
			yield (u"text", decode(node.content))
		elif node.type == "cdata":
			pos = self._handle_pos(node)
			if pos is not None:
				yield pos
			yield (u"cdata", decode(node.content))
		elif node.type == "comment":
			pos = self._handle_pos(node)
			if pos is not None:
				yield pos
			yield (u"comment", decode(node.content))
		# ignore all other types

	def __call__(self, input):
		import libxml2 # This requires libxml2 (see http://www.xmlsoft.org/)

		url = None
		collectdata = []
		for (evtype, data) in input:
			if evtype == u"url":
				if url is None:
					url = data
				else:
					raise ValueError("got multiple url events")
			elif evtype == u"bytes":
				collectdata.append(data)
			else:
				raise UnknownEventError(self, (evtype, data))
		data = "".join(collectdata)
		if url is not None:
			yield (u"url", url)
		if data:
			self._lastlineno = None
			try:
				olddefault = libxml2.lineNumbersDefault(1)
				doc = libxml2.htmlReadMemory(data, len(data), str(url), self.encoding, 0x160)
				try:
					for event in self._asxist(doc):
						yield event
				finally:
					doc.freeDoc()
			finally:
				libxml2.lineNumbersDefault(olddefault)


###
### Consumers: Functions that consume an event stream
###

def events(*pipeline):
	"""
	Return an iterator over the events produced by the pipeline objects in
	:var:`pipeline`.
	"""
	source = pipeline[0]

	# Propagate first pipeline object to a source object (if unambiguous, else use it as it is)
	if isinstance(source, basestring):
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


def tree(*pipeline, **kwargs):
	"""
	Return a tree of XIST nodes from the event stream :var:`pipeline`.

	:var:`pipeline` must output only events that contain XIST nodes, i.e. the
	event types ``"xmldeclnode"``, ``"doctypenode"``, ``"commentnode"``,
	``"textnode"``, ``"startelementnode"``, ``"endelementnode"``,
	``"procinstnode"`` and ``"entitynode"``.

	:var:`kwargs` supports one keyword argument: :var:`validate`.
	If :var:`validate` is true, the tree is validated, i.e. it is checked if
	the structure of the tree is valid (according to the :var:`model` attribute
	of each element node), if all required attributes are specified and all
	attributes have allowed values.

	The node returned from :func:`tree` will always be a :class:`Frag` object.

	Example::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import xml, html, chars
		>>> doc = parse.tree(
		... 	parse.URL("http://www.python.org/"),
		... 	parse.Expat(ns=True),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars))
		... )
		>>> doc[0]
		<ll.xist.ns.html.html element object (5 children/2 attrs) (from http://www.python.org/:3:0) at 0x1028eb3d0>
	"""
	stack = [xsc.Frag()]
	validate = kwargs.get("validate", True)
	for (evtype, node) in events(*pipeline):
		if evtype == u"startelementnode":
			stack[-1].append(node)
			stack.append(node)
		elif evtype == u"endelementnode":
			if validate:
				node.checkvalid()
			stack.pop()
		else:
			stack[-1].append(node)
	return stack[0]


def itertree(*pipeline, **kwargs):
	"""
	Parse the event stream :var:`pipeline` iteratively.

	:func:`itertree` still builds a tree, but it returns a iterator of
	``(event type, path)`` tuples that track changes to the tree as it is built.
	``path`` is a list containing the path from the root ``Frag`` object to the
	node being worked on.

	Which events and paths are produced depends on the keyword arguments
	:var:`events` and :var:`filter`. :var:`events`  specifies which events you
	want to see (possible event types are ``"xmldeclnode"``, ``"doctypenode"``,
	``"commentnode"``, ``"textnode"``, ``"startelementnode"``,
	``"endelementnode"``, ``"procinstnode"`` and ``"entitynode"``). The default
	is to only produce ``"endelementnode"`` events. (Note that for
	``"startelementnode"`` events, the attributes of the element have been set,
	but the element is still empty). :var:`filter` specifies an XIST walk filter
	(see the :mod:`ll.xist.xfind` module for more info on walk filters) to filter
	which paths are output. The default is to output all paths.

	Example::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import xml, html, chars
		>>> for (evtype, path) in parse.itertree(
		... 	parse.URL("http://www.python.org/"),
		... 	parse.Expat(ns=True),
		... 	parse.Node(pool=xsc.Pool(xml, html, chars)),
		... 	filter=html.a/html.img
		... ):
		... 	print path[-1].attrs.src, "-->", path[-2].attrs.href
		http://www.python.org/images/python-logo.gif --> http://www.python.org/
		http://www.python.org/images/trans.gif --> http://www.python.org/#left%2Dhand%2Dnavigation
		http://www.python.org/images/trans.gif --> http://www.python.org/#content%2Dbody
		http://www.python.org/images/donate.png --> http://www.python.org/psf/donations/
		http://www.python.org/images/worldmap.jpg --> http://wiki.python.org/moin/Languages
		http://www.python.org/images/success/tribon.jpg --> http://www.python.org/about/success/tribon/
	"""
	events_ = kwargs.get("events", ("endelementnode",))
	validate = kwargs.get("validate", True)
	filter = xfind.makewalkfilter(kwargs.get("filter", None))

	path = [xsc.Frag()]
	for (evtype, node) in events(*pipeline):
		if evtype == u"startelementnode":
			path[-1].append(node)
			path.append(node)
			if evtype in events_ and filter.matchpath(path): # FIXME: This requires that the ``WalkFilter`` is in fact a ``Selector``
				yield (evtype, path)
		elif evtype == u"endelementnode":
			if validate:
				node.checkvalid()
			if evtype in events_ and filter.matchpath(path): # FIXME: This requires that the ``WalkFilter`` is in fact a ``Selector``
				yield (evtype, path)
			path.pop()
		else:
			path[-1].append(node)
			path.append(node)
			if evtype in events_ and filter.matchpath(path): # FIXME: This requires that the ``WalkFilter`` is in fact a ``Selector``
				yield (evtype, path)
			path.pop()
