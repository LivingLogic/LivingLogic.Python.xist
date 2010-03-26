# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
This module contains everything you need to parse XIST objects from files,
strings, URLs etc.

Parsing XML is done with a pipelined approach. The first step in the pipeline
is a :class:`Source` object that provides the XML source (from strings, files,
URLs, etc.).

The next step is the XML parser. It turns the input source into an iterator over
parsing events (an "event stream"). Further steps in the pipeline might resolve
namespace prefixes (:class:`NS`), and instantiate XIST classes
(:class:`Instantiate`).

The final step in the pipeline is either building an XML tree via :func:`tree`
or an iterative parsing step (similar to ElementTrees :func:`iterparse`
function) via :func:`iterparse`.

Parsing a simple HTML string might e.g. look like this::

	>>> from ll.xist import xsc, parsers
	>>> from ll.xist.ns import html
	>>> source = "<a href='http://www.python.org/'>Python</a>"
	>>> doc = parsers.tree(
	...         parsers.StringSource(source)
	...       | parsers.Expat()
	...       | parsers.NS(prefixes={None: html})
	...       | parsers.Instantiate(pool=xsc.Pool(html))
	... )
	>>> doc.bytes()
	'<a href="http://www.python.org/">Python</a>'

Alternatively the parsing step can be done with a :class:`Tidy` object, which
parses (potentially ill-formed) HTML into an event stream.

It's also possible to turn an object that is compatible with the ElemenTree__
API into an event stream via an :class:`ETree` object.

	__ http://effbot.org/zone/element-index.htm

The following code shows an example of an event stream::

	>>> from ll.xist import parsers
	>>> source = "<a href='http://www.python.org/'>Python</a>"
	>>> list(parsers.StringSource(source) | parsers.Expat())
	[('location', (0, 0)),
	 ('enterstarttag', u'a'),
	 ('enterattr', u'href'),
	 ('text', u'http://www.python.org/'),
	 ('leaveattr', u'href'),
	 ('leavestarttag', u'a'),
	 ('location', (0, 39)),
	 ('text', u'Python'),
	 ('endtag', u'a')]

An event is a tuple consisting of the event type and the event data. The
following events are produced:

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
		A text. The event data is the text content. Parsers should try to avoid
		outputting multiple text events in sequence.

	``"cdata"``
		A CDATA section. The event data is the content of the CDATA section.
		Parsers may report CDATA sections as text events instead of cdata events.

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
		``"enterattr"`` and the ``"leaveattr"`` event. (In most cases this is
		one text event).

	``"endtag"``
		An element end tag. The event data is the element name.

	``"procinst"``
		A processing instruction. The event data is a tuple consisting of the
		pi target and the pi data.

	``"entity"``
		An entity reference. The event data is the entity name.

	``"location"``
		The event data is a tuple containing the line and column number in the
		source (both starting with 0). All the following events should use this
		location information until the next location event.
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

class PipelineMismatchError(TypeError):
	def __init__(self, pipein, pipeout):
		self.pipein = pipein
		self.pipeout = pipeout

	def __str__(self):
		return "{0.pipein!r} got wrong input from {0.pipeout!r}: need {0.pipein.intype}, got {0.pipeout.outtype}".format(self)


###
### pipeline
###

class PipelineObject(object):
	"""
	A :class:`PipelineObject` is the base class of all objects in a
	:class:`Pipeline`. It provides basic functionality for creating a pipeline
	via the or (``|``) operator.
	"""

	def __init__(self, input=None):
		self.input = input

	@property
	def url(self):
		return self.input.url if self.input is not None else None

	def __ror__(self, other):
		"""
		Set :var:`other` as :var:`self`\s input and return :var:`self`.
		"""
		if not isinstance(other, (Source, PipelineObject)):
			if isinstance(other, basestring):
				other = StringSource(other)
			elif isinstance(other, url_.URL):
				other = URLSource(other)
			elif hasattr(other, "__iter__"): # Test this last (as ``URL``\s have :meth:`__iter__` too)
				other = IterSource(other)
			else:
				raise TypeError("can't convert {0!r} to a source".format(other))
		if other.outtype != self.intype:
			raise PipelineMismatchError(self, other)
		self.input = other
		return self


###
### sources
###

class Source(object):
	"""
	A source object provides the input for a parser.
	"""
	def __init__(self, url):
		self.url = url

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object url={0.url!r} at {1:#x}>".format(self, id(self))


class StringSource(Source):
	"""
	Provides parser input from a string.
	"""
	def __init__(self, data, url=None):
		"""
		Create a :class:`StringSource` object. :var:`data` must be an 8-bit string.
		:var:`url` specifies the url for the source (defaulting to ``"STRING"``).
		"""
		self.url = url_.URL(url if url is not None else "STRING")
		self.data = data
		self.outtype = "bytes" if isinstance(data, str) else "unicode"

	def __iter__(self):
		yield self.data


class IterSource(Source):
	"""
	Provides parser input from an iterator over strings.
	"""

	def __init__(self, iterable, url=None, outtype="bytes"):
		"""
		Create a :class:`IterSource` object. :var:`iterable` must be an iterable
		object producing 8-bit strings. :var:`url` specifies the url for the
		source (defaulting to ``"ITER"``).
		"""
		self.url = url_.URL(url if url is not None else "ITER")
		self.iterable = iterable
		self.outtype = outtype

	def __iter__(self):
		return iter(self.iterable)


class StreamSource(Source):
	"""
	Provides parser input from a stream (i.e. an object, that provides a
	:meth:`read` method).
	"""

	def __init__(self, stream, url=None, bufsize=8192, outtype="bytes"):
		"""
		Create a :class:`StreamSource` object. :var:`stream` must possess a
		:meth:`read` method (with a ``size`` argument). :var:`url` specifies the
		url for the source (defaulting to ``"STREAM"``). :var:`bufsize` specifies
		the chunksize for reads from the stream.
		"""
		self.url = url_.URL(url if url is not None else "STREAM")
		self.stream = stream
		self.bufsize = bufsize
		self.outtype = outtype

	def __iter__(self):
		while True:
			data = self.stream.read(self.bufsize)
			if data:
				yield data
			else:
				break


class FileSource(Source):
	"""
	Provides parser input from a file.
	"""

	def __init__(self, filename, bufsize=8192, outtype="bytes"):
		"""
		Create a :class:`FileSource` object. :var:`filename` is the name of the
		file and may start with ``~`` or ``~user`` for the home directory of the
		current or the specified user. :var:`bufsize` specify the chunksize for
		reads from the file.
		"""
		self.url = url_.File(filename)
		self._filename = os.path.expanduser(filename)
		self.outtype = outtype

	def __iter__(self):
		with open(self._filename, "rb") as stream:
			while True:
				data = stream.read(self.bufsize)
				if data:
					yield data
				else:
					break


class URLSource(Source):
	"""
	Provides parser input from a URL.
	"""

	outtype = "bytes"

	def __init__(self, name, bufsize=8192, *args, **kwargs):
		"""
		Create a :class:`URLSource` object. :var:`name` is the URL.
		:var:`bufsize` specify the chunksize for reads from the URL. :var:`args`
		and :var:`kwargs` will be passed on to the :meth:`open` method of the URL
		object.

		The URL for the input will be the final URL for the resource (i.e. it will
		include redirects).
		"""
		u = url_.URL(name)
		self.stream = u.open("rb", *args, **kwargs)
		self.url = self.stream.finalurl()
		self.bufsize = bufsize

	def __iter__(self):
		with contextlib.closing(self.stream) as stream:
			while True:
				data = stream.read(self.bufsize)
				if data:
					yield data
				else:
					break


class Decoder(PipelineObject):
	"""
	Decode the 8-bit output of the previous object in the pipeline to unicode.

	This previous object can be a source object or any other pipeline object that
	produces 8-bit strings.
	"""

	intype = "bytes"
	outtype = "unicode"

	def __init__(self, input=None, encoding=None):
		"""
		Create a :class:`Decoder` object. :var:`encoding` is encoding of the input.
		"""
		PipelineObject.__init__(self, input)
		self.encoding = encoding

	def _checkinput(self):
		if not isinstance(data, str):
			raise PipelineMismatchError(self, "bytes", data)

	def __iter__(self):
		decoder = codecs.getincrementaldecoder("xml")(encoding=self.encoding)
		for data in self.input:
			self._checkinput(data)
			data = decoder.decode(data, False)
			if data:
				yield data
		data = decoder.decode("", True)
		if data:
			yield data

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object encoding={0.encoding!r} at {1:#x}>".format(self, id(self))


class Encoder(PipelineObject):
	"""
	Encode the unicode output of the previous object in the pipeline to 8-bit
	strings.

	This previous object must be a pipeline object that produces unicode output
	(e.g. a :class:`Decoder` object).
	"""

	intype = "unicode"
	outtype = "bytes"

	def __init__(self, input=None, encoding=None):
		"""
		Create an :class:`Encoder` object. :var:`encoding` will be the encoding of
		the output.
		"""
		PipelineObject.__init__(self, input)
		self.encoding = encoding

	def _checkinput(self, data):
		if not isinstance(data, unicode):
			raise PipelineMismatchError(self, "unicode", data)

	def __iter__(self):
		encoder = codecs.getincrementalencoder("xml")(encoding=self.encoding)
		for data in self.input:
			self._checkinput(data)
			data = encoder.encode(data, False)
			if data:
				yield data
		data = encoder.encode(u"", True)
		if data:
			yield data

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object encoding={0.encoding!r} at {1:#x}>".format(self, id(self))


class Transcoder(PipelineObject):
	"""
	Transcode the 8-bit output of the previous object into another encoding.

	This previous object can be a source object or any other pipeline object that
	produces 8-bit strings.
	"""

	intype = "bytes"
	outtype = "bytes"

	def __init__(self, input=None, fromencoding=None, toencoding=None):
		"""
		Create a :class:`Transcoder` object. :var:`fromencoding` is the encoding
		of the input. :var:`toencoding` is the encoding of the output.
		"""
		PipelineObject.__init__(self, input)
		self.fromencoding = fromencoding
		self.toencoding = toencoding

	def _checkinput(self, data):
		if not isinstance(data, str):
			raise PipelineMismatchError(self, "bytes", data)

	def __iter__(self):
		decoder = codecs.getincrementaldecoder("xml")(encoding=self.fromencoding)
		encoder = codecs.getincrementalencoder("xml")(encoding=self.toencoding)
		for data in self.input:
			self._checkinput(data)
			data = encoder.encode(decoder.decode(data, False), False)
			if data:
				yield data
		data = encoder.encode(decoder.decode("", True), True)
		if data:
			yield data

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object fromencoding={0.fromencoding!r} toencoding={0.toencoding!r} at {1:#x}>".format(self, id(self))


###
### Parsers
###

class EventParser(PipelineObject):
	"""
	Basic parser interface.
	"""
	xmldecl = "xmldecl"
	begindoctype = "begindoctype"
	enddoctype = "enddoctype"
	comment = "comment"
	text = "text"
	cdata = "cdata"
	enterstarttag = "enterstarttag"
	enterattr = "enterattr"
	leaveattr = "leaveattr"
	leavestarttag = "leavestarttag"
	endtag = "endtag"
	procinst = "procinst"
	entity = "entity"
	location = "location"

	@misc.notimplemented
	def feed(self, data, final=False):
		"""
		Feed :var:`data` (a byte string) to the parser. If :var:`final` is true
		this will be the last call to :meth:`feed`.

		Return an iterator for the events.
		"""

	def _checkinput(self, data):
		if not isinstance(data, str):
			raise PipelineMismatchError(self, "bytes", data)

	def __iter__(self):
		"""
		Return an iterator over events.
		"""
		for data in self.input:
			self._checkinput(data)
			for event in self.feed(data):
				yield event
		for event in self.feed("", True):
			yield event


class Expat(EventParser):
	"""
	A parser using Pythons builtin :mod:`expat` parser.
	"""

	intype = "bytes"

	def __init__(self, input=None, encoding=None, xmldecl=False, doctype=False, loc=True, cdata=False, ns=False):
		"""
		Create an :class:`Expat` object. Arguments have the following meaning:

		:var:`encoding` : string or :const:`None`
			The default encoding to use when the source doesn't provide an
			encoding. The default :const:`None` results in the encoding being
			detected from the XML itself.

		:var:`xmldecl` : bool
			Should a node be output for the XML declaration?

		:var:`doctype` : bool
			Should a node be output for the document type?

		:var:`loc` : bool
			Should location information be attached to the generated nodes?

		:var:`cdata` : bool
			Output CDATA sections as ``"cdata"`` events? (If :var:`cdata` is false
			output ``"text"`` events instead.)

		:var:`ns` : bool
			If :var:`ns` is true, the parser does its own namespace processing.
			The data of ``"enterstarttag"``, ``"leavestarttag"``, ``"endtag"``,
			``"enterattr"`` and ``"leaveattr"`` events will already be
			``(name, namespace)`` tuples.
		"""
		EventParser.__init__(self, input)
		self._parser = expat.ParserCreate(encoding, "\x01" if ns else None)
		self._parser.buffer_text = True
		self._parser.ordered_attributes = True
		self._parser.UseForeignDTD(True)
		self._encoding = encoding
		self._xmldecl = xmldecl
		self._doctype = doctype
		self._loc = loc
		self._cdata = cdata
		self._ns = ns
		self._indoctype = False
		self._incdata = False
		self._location = None # Remember the last reported location

		self._parser.CharacterDataHandler = self._handle_text
		self._parser.StartElementHandler = self._handle_startelement
		self._parser.EndElementHandler = self._handle_endelement
		self._parser.ProcessingInstructionHandler = self._handle_procinst
		self._parser.CommentHandler = self._handle_comment
		self._parser.DefaultHandler = self._handle_default

		if cdata:
			self._parser.StartCdataSectionHandler = self._handle_startcdata
			self._parser.EndCdataSectionHandler = self._handle_endcdata

		if self._xmldecl:
			self._parser.XmlDeclHandler = self._handle_xmldecl

		# Always required, as we want to recognize whether a comment or PI is in the internal DTD subset
		self._parser.StartDoctypeDeclHandler = self._handle_begindoctype
		self._parser.EndDoctypeDeclHandler = self._handle_enddoctype

		# Buffers the events generated during one call to ``feed``
		self._buffer = []

		self.outtype = "nsevents" if ns else "events"

	def __repr__(self):
		v = []
		if self._encoding is not None:
			v.append(" encoding={0!r}".format(self._encoding))
		if self._xmldecl is not None:
			v.append(" xmldecl={0!r}".format(self._xmldecl))
		if self._doctype is not None:
			v.append(" doctype={0!r}".format(self._doctype))
		if self._loc is not None:
			v.append(" loc={0!r}".format(self._loc))
		if self._cdata is not None:
			v.append(" cdata={0!r}".format(self._cdata))
		if self._ns is not None:
			v.append(" ns={0!r}".format(self._ns))
		return "<{0.__class__.__module__}.{0.__class__.__name__} object{1} at {2:#x}>".format(self, "".join(v), id(self))

	def feed(self, data, final=False):
		self._parser.Parse(data, final)
		result = iter(self._buffer)
		self._buffer = []
		return result

	def _getname(self, name):
		if self._ns:
			if "\x01" in name:
				return tuple(name.split("\x01")[::-1])
			return (name, None)
		return name

	def _handle_location(self):
		if self._loc:
			loc = (self._parser.CurrentLineNumber-1, self._parser.CurrentColumnNumber)
			if loc != self._location:
				self._buffer.append((self.location, loc))
				self._location = loc

	def _handle_startcdata(self):
		self._incdata = True

	def _handle_endcdata(self):
		self._incdata = False

	def _handle_xmldecl(self, version, encoding, standalone):
		standalone = (bool(standalone) if standalone != -1 else None)
		self._handle_location()
		self._buffer.append((self.xmldecl, {"version": version, "encoding": encoding, "standalone": standalone}))

	def _handle_begindoctype(self, doctypename, systemid, publicid, has_internal_subset):
		if self._doctype:
			self._handle_location()
			self._buffer.append((self.begindoctype, {"name": doctypename, "publicid": publicid, "systemid": systemid}))

	def _handle_enddoctype(self):
		if self._doctype:
			self._handle_location()
			self._buffer.append((self.enddoctype, None))

	def _handle_default(self, data):
		if data.startswith("&") and data.endswith(";"):
			self._handle_location()
			self._buffer.append((self.entity, data[1:-1]))

	def _handle_comment(self, data):
		if not self._indoctype:
			self._handle_location()
			self._buffer.append((self.comment, data))

	def _handle_text(self, data):
		self._handle_location()
		self._buffer.append((self.cdata if self._incdata else self.text, data))

	def _handle_startelement(self, name, attrs):
		name = self._getname(name)
		self._handle_location()
		self._buffer.append((self.enterstarttag, name))
		for i in xrange(0, len(attrs), 2):
			key = self._getname(attrs[i])
			self._buffer.append((self.enterattr, key))
			self._buffer.append((self.text, attrs[i+1]))
			self._buffer.append((self.leaveattr, key))
		self._buffer.append((self.leavestarttag, name))

	def _handle_endelement(self, name):
		name = self._getname(name)
		self._handle_location()
		self._buffer.append((self.endtag, name))

	def _handle_procinst(self, target, data):
		if not self._indoctype:
			self._handle_location()
			self._buffer.append((self.procinst, (target, data)))


class SGMLOP(EventParser):
	"""
	A parser based of :mod:`sgmlop`.
	"""

	intype = "bytes"
	outtype = "events"

	def __init__(self, input=None, encoding=None):
		"""
		Create a new :class:`SGMLOP` object.
		"""
		EventParser.__init__(self, input)
		self.encoding = encoding
		self._decoder = codecs.getincrementaldecoder("xml")(encoding=encoding)
		self._parser = sgmlop.XMLParser()
		self._parser.register(self)
		self._buffer = []
		self._hadtext = False

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object encoding={0.encoding!r} at {1:#x}>".format(self, id(self))

	def feed(self, data, final=False):
		self._parser.feed(self._decoder.decode(data, final))
		result = iter(self._buffer)
		self._buffer = []
		return result

	def handle_comment(self, data):
		self._hadtext = False
		self._buffer.append((self.comment, data))

	def handle_data(self, data):
		if self._hadtext:
			self._buffer[-1] = (self.text, self._buffer[-1][1] + data)
		else:
			self._buffer.append((self.text, data))
		self._hadtext = True

	def handle_cdata(self, data):
		self._hadtext = False
		self._buffer.append((self.cdata, data))

	def handle_proc(self, target, data):
		self._hadtext = False
		self._buffer.append((self.procinst, (target, data)))

	def handle_entityref(self, name):
		self._hadtext = False
		self._buffer.append((self.entity, name))

	def handle_enterstarttag(self, name):
		self._hadtext = False
		self._buffer.append((self.enterstarttag, name))

	def handle_leavestarttag(self, name):
		self._hadtext = False
		self._buffer.append((self.leavestarttag, name))

	def handle_enterattr(self, name):
		self._hadtext = False
		self._buffer.append((self.enterattr, name))

	def handle_leaveattr(self, name):
		self._hadtext = False
		self._buffer.append((self.leaveattr, name))

	def handle_endtag(self, name):
		self._hadtext = False
		self._buffer.append((self.endtag, name))


class NS(PipelineObject):
	"""
	An :class:`NS` is used in a parsing pipeline to add support for XML namespaces.
	It replaces the element and attribute names in ``"enterstarttag"``,
	``"leavestarttag"``, ``"endtag"``, ``"enterattr"`` and ``"leaveattr"`` events
	with ``(name, namespace)`` tuples.

	The output of a :class:`NS` object in the stream looks like this::

		>>> from ll.xist import parsers
		>>> from ll.xist.ns import html
		>>> source = "<a href='http://www.python.org/'>Python</a>"
		>>> list(parsers.StringSource(source) | parsers.Expat() | parsers.NS(prefixes={None: html}))
		[('location', (0, 0)),
		 ('enterstarttag', (u'a', 'http://www.w3.org/1999/xhtml')),
		 ('enterattr', (u'href', None)),
		 u'http://www.python.org/',
		 ('leaveattr', (u'href', None)),
		 ('leavestarttag', (u'a', 'http://www.w3.org/1999/xhtml')),
		 ('location', (0, 39)),
		 ('text', u'Python'),
		 ('endtag', (u'a', 'http://www.w3.org/1999/xhtml'))]
	"""

	intype = "events"
	outtype = "nsevents"

	def __init__(self, input=None, prefixes=None, **kwargs):
		"""
		Create a :class:`NS` object. The namespace mapping is initialized from the
		dictionary :var:`prefixes` (if given) and from :var:`kwargs`.
		"""
		PipelineObject.__init__(self, input)
		# the currently active prefix mapping (will be replaced once xmlns attributes are encountered)
		newprefixes = {}
		args = (prefixes, kwargs) if prefixes is not None else (kwargs, )
		for arg in args:
			for (prefix, xmlns) in arg.iteritems():
				if prefix is not None and not isinstance(prefix, basestring):
					raise TypeError("prefix must be None or string, not {0!r}".format(prefix))
				xmlns = xsc.nsname(xmlns)
				if not isinstance(xmlns, basestring):
					raise TypeError("xmlns must be string, not {0!r}".format(xmlns))
				newprefixes[prefix] = xmlns
		self._newprefixes = self._attrs = self._attr = None
		# A stack entry is an ``((elementname, namespacename), prefixdict)`` tuple
		self._prefixstack = [(None, newprefixes)]

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

	def location(self, data):
		data = ("location", data)
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
			newprefixes = dict((key, "".join(d for (t, d) in value if t == "text")) for (key, value) in self._newprefixes.iteritems())
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

		yield ("enterstarttag", data)
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
			yield ("enterattr", (attrname, xmlns))
			for event in attrvalue:
				yield event
			yield ("leaveattr", (attrname, xmlns))
		yield ("leavestarttag", data)
		self._newprefixes = self._attrs = self._attr = None

	def endtag(self, data):
		(data, prefixes) = self._prefixstack.pop()
		yield ("endtag", data)

	def _checkinput(self, data):
		if not isinstance(data, tuple) or len(data) != 2:
			raise PipelineMismatchError(self, "event", data)
		# FIXME: More checks

	def __iter__(self):
		for event in self.input:
			# self._checkinput(event)
			for data in getattr(self, event[0])(event[1]):
				yield data


class Instantiate(PipelineObject):
	intype = "nsevents"
	outtype = "xist"

	def __init__(self, input=None, pool=None, base=None, loc=True):
		PipelineObject.__init__(self, input)
		self.pool = (pool if pool is not None else xsc.threadlocalpool.pool)
		if base is not None:
			base = url_.URL(base)
		self.base = base
		self.loc = loc
		self._location = (None, None)
		self._stack = []
		self._inattr = False

	def __iter__(self):
		if self.base is None:
			self.base = self.url
		for event in self.input:
			event = getattr(self, event[0])(event[1])
			if event is not None:
				yield event

	def xmldecl(self, data):
		node = xml.XML(version=data["version"], encoding=data["encoding"], standalone=data["standalone"])
		if self.loc:
			node.startloc = xsc.Location(self.url, *self._location)
		return ("xmldecl", node)

	def begindoctype(self, data):
		if data["publicid"]:
			fmt = u'{0[name]} PUBLIC "{0[publicid]}" "{0[systemid]}"'
		elif data["systemid"]:
			fmt = u'{0[name]} SYSTEM "{0[systemid]}"'
		else:
			fmt = u'{0[name]}'
		node = xsc.DocType(fmt.format(data))
		if self.loc:
			node.startloc = xsc.Location(self.url, *self._location)
		self.doctype = node
		return ("begindoctype", node)

	def enddoctype(self, data):
		result = ("enddoctype", self.doctype)
		del self.doctype
		return result

	def entity(self, data):
		node = self.pool.entity_xml(data)
		if self.loc:
			node.startloc = xsc.Location(self.url, *self._location)
		node.parsed(self, "entity")
		if self._inattr:
			self._stack[-1].append(node)
		else:
		 	return ("entity", node)

	def comment(self, data):
		node = xsc.Comment(data)
		if self.loc:
			node.startloc = xsc.Location(self.url, *self._location)
		node.parsed(self, "comment")
		if self._inattr:
			self._stack[-1].append(node)
		else:
			return ("comment", node)

	def cdata(self, data):
		node = xsc.Text(data)
		if self.loc:
			node.startloc = xsc.Location(self.url, *self._location)
		node.parsed(self, "cdata")
		if self._inattr:
			self._stack[-1].append(node)
		else:
			return ("cdata", node)

	def text(self, data):
		node = xsc.Text(data)
		if self.loc:
			node.startloc = xsc.Location(self.url, *self._location)
		node.parsed(self, "text")
		if self._inattr:
			self._stack[-1].append(node)
		else:
		 	return ("text", node)

	def enterstarttag(self, data):
		node = self.pool.element_xml(*data)
		if self.loc:
			node.startloc = xsc.Location(self.url, *self._location)
		self._stack.append(node)
		node.parsed(self, "enterstarttag")
		return ("enterstarttag", node)

	def enterattr(self, data):
		if data[1] is not None:
			node = self.pool.attrclass_xml(*data)
		else:
			node = self._stack[-1].attrs.allowedattr_xml(data[0])
		if self.loc:
			node.startloc = xsc.Location(self.url, *self._location)
		self._stack[-1].attrs[node] = ()
		node = self._stack[-1].attrs[node]
		self._stack.append(node)
		self._inattr = True
		node.parsed(self, "enterattr")

	def leaveattr(self, data):
		node = self._stack.pop()
		self._inattr = False
		node.parsed(self, "leaveattr")

	def leavestarttag(self, data):
		self._stack[-1].parsed(self, "leavestarttag")
		return ("leavestarttag", self._stack[-1])

	def endtag(self, data):
		node = self._stack.pop()
		if self.loc:
			node.endloc = xsc.Location(self.url, *self._location)
		node.parsed(self, "endtag")
		return ("endtag", node)

	def procinst(self, data):
		node = self.pool.procinst_xml(*data)
		if self.loc:
			node.startloc = xsc.Location(self.url, *self._location)
		node.parsed(self, "procinst")
		if self._inattr:
			self._stack[-1].append(node)
		else:
			return ("procinst", node)

	def location(self, data):
		self._location = data


class Tidy(PipelineObject):
	"""
	A :class:`Tidy` object parses (potentially ill-formed) HTML from a source
	into a event stream by using libxml2__'s HTML parser.

	__ http://xmlsoft.org/
	"""

	intype = "bytes"
	outtype = "events"

	def __init__(self, input=None, encoding=None, loc=True):
		PipelineObject.__init__(self, input)
		self.encoding = encoding
		self.loc = loc

	def __repr__(self):
		return "<{0.__class__.__module__}.{0.__class__.__name__} object encoding={0.encoding!r} loc={0.loc!r} at {1:#x}>".format(self, id(self))

	def __iter__(self):
		import libxml2 # This requires libxml2 (see http://www.xmlsoft.org/)

		def decode(s):
			try:
				return s.decode("utf-8")
			except UnicodeDecodeError:
				return s.decode("iso-8859-1")

		lastlineno = [None] # Have a mutable object to store to current line number

		def _handle_loc(node):
			if self.loc:
				lineno = node.lineNo()
				if lineno != lastlineno[0]:
					return ("location", (lineno, None))
					lastlineno[0] = lineno

		def toxsc(node):
			if node.type == "document_html":
				child = node.children
				while child is not None:
					for event in toxsc(child):
						yield event
					child = child.next
			elif node.type == "element":
				loc = _handle_loc(node)
				if loc is not None:
					yield loc
				elementname = decode(node.name).lower()
				yield ("enterstarttag", elementname)
				attr = node.properties
				while attr is not None:
					attrname = decode(attr.name).lower()
					content = decode(attr.content) if attr.content is not None else u""
					yield ("enterattr", attrname)
					yield ("text", content)
					yield ("leaveattr", attrname)
					attr = attr.next
				yield ("leavestarttag", elementname)
				child = node.children
				while child is not None:
					for event in toxsc(child):
						yield event
					child = child.next
				yield ("endtag", elementname)
			elif node.type == "text":
				loc = _handle_loc(node)
				if loc is not None:
					yield loc
				yield ("text", decode(node.content))
			elif node.type == "cdata":
				loc = _handle_loc(node)
				if loc is not None:
					yield loc
				yield ("cdata", decode(node.content))
			elif node.type == "comment":
				loc = _handle_loc(node)
				if loc is not None:
					yield loc
				yield ("comment", decode(node.content))
			# ignore all other types

		data = "".join(self.input)
		if data:
			try:
				olddefault = libxml2.lineNumbersDefault(1)
				doc = libxml2.htmlReadMemory(data, len(data), str(self.url), self.encoding, 0x160)
				try:
					for event in toxsc(doc):
						yield event
				finally:
					doc.freeDoc()
			finally:
				libxml2.lineNumbersDefault(olddefault)


class ETree(Source):
	"""
	Returns XML events from an object that supports the ElementTree__ API.

	__ http://effbot.org/zone/element-index.htm
	"""

	intype = "etree"
	outtype = "nsevents"

	def __init__(self, data, url=None, defaultxmlns=None):
		self.url = url_.URL(url if url is not None else "ETREE")
		self.data = data
		self.defaultxmlns = xsc.nsname(defaultxmlns)

	def __iter__(self):
		def toxsc(node):
			name = type(node).__name__
			if "Element" in name:
				elementname = node.tag
				if elementname.startswith("{"):
					(elementxmlns, sep, elementname) = elementname[1:].partition("}")
				else:
					elementxmlns = self.defaultxmlns
				yield ("enterstarttag", (elementname, elementxmlns))
				for (attrname, attrvalue) in node.items():
					if attrname.startswith("{"):
						(attrxmlns, sep, attrname) = attrname[1:].partition("}")
					else:
						attrxmlns = None
					yield ("enterattr", (attrname, attrxmlns))
					yield ("text", attrvalue)
					yield ("leaveattr", (attrname, attrxmlns))
				yield ("leavestarttag", (elementname, elementxmlns))
				if node.text:
					yield ("text", node.text)
				for child in node:
					for event in toxsc(child):
						yield event
					if hasattr(child, "tail") and child.tail:
						yield ("text", child.tail)
				yield ("endtag", (elementname, elementxmlns))
			elif "ProcessingInstruction" in name:
				yield ("procinst", (node.target, node.text))
			elif "Comment" in name:
				yield ("comment", (node.target, node.text))

		return toxsc(self.data)


def _fixpipeline(pipeline, parser=None, prefixes=None, pool=None, base=None, loc=True, tidy=False, encoding=None, **parserargs):
	needprefixes = False
	needinstantiate = False
	if tidy:
		pipeline |= Tidy(encoding=encoding)
		if prefixes is None:
			prefixes = {None: html_xmlns}
		needprefixes = True
	elif parser is not None or parserargs:
		if parser is None:
			parser = Expat
		pipeline |= parser(encoding=encoding, **parserargs)
		# If we're using an expat parser that does its own namespace handling, we don't need a prefix mapping
		if not isinstance(parser, Expat) or not parser.ns:
			needprefixes = True
	if needprefixes or prefixes is not None:
		pipeline |= NS(prefixes=prefixes)
		needinstantiate = True
	if needinstantiate or pool is not None or base is not None or not loc:
		pipeline |= Instantiate(pool=pool, base=base, loc=loc)
	return pipeline


def tree(pipeline, validate=True):
	stack = [xsc.Frag()]
	for event in pipeline:
		if event[0] == "enterstarttag":
			stack[-1].append(event[1])
			stack.append(event[1])
		elif event[0] == "endtag":
			if validate:
				event[1].checkvalid()
			stack.pop()
		elif event[0] != "leavestarttag":
			stack[-1].append(event[1])
	return stack[0]


def iterparse(input, events=("endtag",), validate=True, filter=None):
	filter = xfind.makewalkfilter(filter)
	path = [xsc.Frag()]
	for event in pipeline:
		if event in events and filter.matchpath(path):
			yield (event, path)
		if event == "enterstarttag":
			path[-1].append(node)
			path.append(node)
		elif event == "endtag":
			if validate:
				node.checkvalid()
			path.pop()
		elif event != "leavestarttag":
			path[-1].append(node)


class noBuilder(object):
	"""
	It is the job of a :class:`Builder` to create the object tree from the
	events generated by the underlying parser.
	"""

	def __init__(self, parser=Expat, prefixes=None, tidy=False, loc=True, validate=True, encoding=None, pool=None):
		"""
		Create a new :class:`Builder` instance.

		Arguments have the following meaning:

		:var:`parser`
			a subclass of the :class:`Parser` class (or any object that provides
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
					raise TypeError("Prefix must be None or string, not {0!r}".format(prefix))
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


	def _makeparser(self, iterable, encoding=None, base=None):
		# Internal helper: create a parser and initialize the stack
		parser = self.parser(iterable, encoding=encoding)
		self.base = url_.URL(base)
		# XIST nodes do not have a parent link, therefore we have to store the
		# active path through the tree in a stack (which we call ``_nesting``)
		# together with the namespace prefixes defined by each element.
		#
		# After we've finished parsing, the ``Frag`` that we put at the bottom of
		# the stack will be our document root.
		self._nesting = [ (xsc.Frag(), self.prefixes) ]
		parser.xmldecl = self.xmldecl
		parser.begindoctype = self.begindoctype
		parser.enddoctype = self.enddoctype
		parser.entity = self.entity
		parser.comment = self.comment
		parser.cdata = self.cdata
		parser.text = self.text
		parser.enterstarttag = self.enterstarttag
		parser.enterattr = self.enterattr
		parser.leaveattr = self.leaveattr
		parser.leavestarttag = self.leavestarttag
		parser.endtag = self.endtag
		parser.procinst = self.procinst
		if self.loc:
			parser.location = self.location
			self._location = (None, None)
		return parser

	def xmldecl(self, data):
		node = xml.XML(version=data["version"], encoding=data["encoding"], standalone=data["standalone"])
		self._appendNode(node)

	def begindoctype(self, data):
		if data["publicid"]:
			fmt = u'{0[name]} PUBLIC "{0[publicid]}" "{0[systemid]}"'
		elif data["systemid"]:
			fmt = u'{0[name]} SYSTEM "{0[systemid]}"'
		else:
			fmt = u'{0[name]}'
		node = xsc.DocType(fmt.format(data))
		self._appendNode(node)

	def enddoctype(self, data):
		pass

	def entity(self, data):
		try:
			c = {u"lt": u"<", u"gt": u">", u"amp": u"&", u"quot": u'"', u"apos": u"'"}[data]
		except KeyError:
			node = self.pool.entity_xml(data)
			if isinstance(node, xsc.CharRef):
				self.text(unichr(node.codepoint))
			else:
				node = node.parsed(self)
				self._appendNode(node)
		else:
			self.text(c)

	def comment(self, data):
		node = self.pool.comment(data)
		node = node.parsed(self)
		self._appendNode(node)

	def cdata(self, data):
		self.text(data)

	def text(self, data):
		if data:
			node = self.pool.text(data)
			node = node.parsed(self)
			last = self._nesting[-1][0]
			if len(last) and isinstance(last[-1], xsc.Text):
				node = last[-1] + unicode(node) # join consecutive Text nodes
				node.startloc = last[-1].startloc # make sure the replacement node has the original location
				last[-1] = node # replace it
			else:
				self._appendNode(node)

	def enterstarttag(self, data):
		self._attrs = {}

	def leavestarttag(self, data):
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

		(prefix, sep, name) = data.rpartition(u":")
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
		self._appendNode(node)
		# push new innermost element onto the stack, together with the list of prefix mappings to which we have to return when we leave this element
		self._nesting.append((node, oldprefixes))
		self._attrs = None

	def enterattr(self, data):
		node = xsc.Frag()
		self._attrs[data] = node
		self._nesting.append((node, self._nesting[-1][1]))

	def leaveattr(self, data):
		(node, prefixes) = self._nesting.pop()
		# if the attribute was empty, ``handle_data`` is newer called, so we have to add an empty text node, to prevent the attribute from disappearing
		if not node:
			node.append("")

	def endtag(self, data):
		currentelement = self._nesting[-1][0]

		(prefix, sep, name) = data.rpartition(u":")
		xmlns = self.prefixes[prefix or None]
		element = self.pool.element_xml(name, xmlns) # Unfortunately this creates the element a second time.
		if  element.__class__ is not currentelement.__class__:
			raise xsc.ElementNestingError(currentelement.__class__, element.__class__)

		currentelement.parsed(self, start=False) # ignore return value

		if self.validate:
			currentelement.checkvalid()
		if self.loc:
			currentelement.endloc = xsc.Location(*self._location)

		self.prefixes = self._nesting.pop()[1] # pop the innermost element off the stack and restore the old prefixes mapping (from outside this element)

	def procinst(self, data):
		(target, data) = data
		if target != "xml":
			node = self.pool.procinst_xml(target, data)
			node = node.parsed(self)
			self._appendNode(node)

	def location(self, data):
		self._location = data

	def _end(self):
		return self._nesting[0][0]

	def parsestring(self, data, base=None, encoding=None):
		"""
		Parse the string :var:`data` (:class:`str` or :class:`unicode`) into an
		XIST tree. :var:`base` is the base URL for the parsing process,
		:var:`encoding` can be used to force the parser to use the specified
		encoding.
		"""
		self.url = url_.URL(base if base is not None else "STRING")
		if isinstance(data, unicode):
			encoding = "utf-8"
			data = data.encode(encoding)
 		if self.tidy:
			return self._parseHTML(data, base=base, sysid=str(self.url), encoding=encoding)
		for (c, data) in self._makeparser([data], base=base, encoding=encoding):
			c(data)
 		return self._end()

	def parseiter(self, iterable, base=None, encoding=None):
		"""
		Parse the input from the iterable :var:`var` (which must produce the input
		in chunks of bytes) into an XIST tree. :var:`base` is the base URL for the
		parsing process, :var:`encoding` can be used to force the parser to use
		the specified encoding.
		"""
		parser = self._makeparser(base=base, encoding=encoding)
		self.url = url_.URL(base if base is not None else "ITER")
		if self.tidy:
			return self._parseHTML("".join(iterable), base=base, sysid=str(self.url), encoding=encoding)
		for (c, data) in self._makeparser(data, base=base, encoding=encoding):
			c(data)
 		return self._end()

	def parsestream(self, stream, base=None, encoding=None, bufsize=8192):
		"""
		Parse XML input from the stream :var:`stream`. :var:`base` is the base
		URL for the parsing process, :var:`encoding` can be used to force the
		parser to use the specified encoding. :var:`bufsize` is the buffer size
		used for reading the stream in blocks.
		"""
		self.url = url_.URL(base if base is not None else "STREAM")
		if self.tidy:
			return self._parseHTML(stream.read(), base=base, sysid=str(self.url), encoding=encoding)
		for (c, data) in self._makeparser(misc.iterstream(stream, bufsize), base=base, encoding=encoding):
			c(data)
 		return self._end()

	def parsefile(self, filename, base=None, encoding=None, bufsize=8192):
		"""
		Parse XML input from the file named :var:`filename`. :var:`base` is the
		base URL for the parsing process (defaulting to :var:`filename` if not
		specified), :var:`encoding` can be used to force the parser to use the
		specified encoding. :var:`bufsize` is the buffer size used for reading
		the file in blocks.
		"""
		self.url = url_.File(filename)
		if base is None:
			base = self.url
		filename = os.path.expanduser(filename)
		with contextlib.closing(open(filename, "rb")) as stream:
			if self.tidy:
				return self._parseHTML(stream.read(), base=base, sysid=str(self.url), encoding=encoding)
			for (c, data) in self._makeparser(misc.iterstream(stream, bufsize), base=base, encoding=encoding):
				c(data)
	 		return self._end()

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
		name = url_.URL(name)
		with contextlib.closing(name.open("rb", *args, **kwargs)) as stream:
			self.url = stream.finalurl()
			if base is None:
				base = self.url
			if self.tidy:
				return self._parseHTML(stream.read(), base=base, sysid=str(self.url), encoding=encoding)
			for (c, data) in self._makeparser(misc.iterstream(stream, bufsize), base=base, encoding=encoding):
				c(data)
	 		return self._end()

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
		self.base = url_.URL(base)

		defaultxmlns = None
		try:
			defaultxmlns = self.prefixes[None][0]
		except (KeyError, IndexError):
			pass

		return toxsc(tree)

	def _appendNode(self, node):
		if self.loc:
			node.startloc = xsc.Location(self.url, *self._location)
		self._nesting[-1][0].append(node) # add the new node to the content of the innermost element/fragment/(attribute)


def parsestring(data, url=None, **kwargs):
	"""
	Parse the string :var:`data` into an XIST tree. For the arguments
	:var:`base` and :var:`encoding` see the method :meth:`parsestring` in the
	:class:`Builder` class. You can pass any other argument that the
	:class:`Builder` constructor takes as keyword arguments
	via :var:`builderargs`.
	"""
	return tree(_fixpipeline(StringSource(data, url=url), **kwargs))


def parseiter(iterable, url=None, **kwargs):
	"""
	Parse the input from the iterable :var:`iterable` (which must produce the
	input in chunks of bytes) into an XIST tree. For the arguments :var:`base`
	and :var:`encoding` see the method :meth:`parsestring` in the
	:class:`Builder` class. You can pass any other argument that the
	:class:`Builder` constructor takes as keyword arguments via
	:var:`builderargs`.
	"""
	return tree(_fixpipeline(IterSource(iterable, url=url), **kwargs))


def parsestream(stream, base=None, bufsize=8192, **kwargs):
	"""
	Parse XML from the stream :var:`stream` into an XIST tree. For the arguments
	:var:`base`, :var:`encoding` and :var:`bufsize` see the method
	:meth:`parsestream` in the :class:`Parser` class. You can pass any other
	argument that the :class:`Builder` constructor takes as keyword arguments via
	:var:`builderargs`.
	"""
	return tree(_fixpipeline(StreamSource(stream, bufsize=bufsize), **kwargs))


def parsefile(filename, bufsize=8192, **kwargs):
	"""
	Parse XML input from the file named :var:`filename`. For the arguments
	:var:`base`, :var:`encoding` and :var:`bufsize` see the method
	:meth:`parsefile` in the :class:`Builder` class. You can pass any other
	argument that the :class:`Builder` constructor takes as keyword arguments
	via :var:`builderargs`.
	"""
	return tree(_fixpipeline(FileSource(filename, bufsize=bufsize), **kwargs))


def parseurl(name, bufsize=8192, headers=None, data=None, **kwargs):
	"""
	Parse XML input from the URL :var:`name` into an XIST tree. For the arguments
	:var:`base`, :var:`encoding`, :var:`bufsize`, :var:`headers` and :var:`data`
	see the method :meth:`parseurl` in the :class:`Builder` class. You can pass
	any other argument that the :class:`Builder` constructor takes as keyword
	arguments via :var:`builderargs`.
	"""
	return tree(_fixpipeline(URLSource(name, headers=headers, data=data), **kwargs))


def parseetree(node, defaultxmlns=None, **kwargs):
	"""
	Parse XML input from the object :var:`node` which must support the
	ElementTree__ API. For the argument :var:`base` see the method
	:meth:`parseetree` in the :class:`Builder` class. You can pass any other
	argument that the :class:`Builder` constructor takes as keyword arguments
	via :var:`builderargs`.

	__ http://effbot.org/zone/element-index.htm
	"""
	return tree(_fixpipeline(ETree(node, defaultxmlns=defaultxmlns), **kwargs))
