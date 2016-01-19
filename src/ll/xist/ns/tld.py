# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
This is the XIST namespace for the JavaServer Pages 1.1 Tag Library
descriptor (``.tld``) (XML) file format/syntax.
"""


from ll import misc
from ll.xist import xsc, sims, xnd, xfind


__docformat__ = "reStructuredText"


xmlns = "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd"


class IdAttrs(xsc.Attrs):
	class id(xsc.IDAttr): pass


class DocTypeTLD11(xsc.DocType):
	"""
	Document type for tag library descriptors version 1.1
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'taglib PUBLIC "-//Sun Microsystems, Inc.//DTD JSP Tag Library 1.1//EN" "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd"')


class attribute(xsc.Element):
	"""
	The attribute tag defines an attribute for the nesting tag. An attribute
	definition is composed of:

	*	the attributes name (required)

	*	if the attribute is required or optional (optional)

	*	if the attributes value may be dynamically calculated at runtime by a
		scriptlet expression (optional)
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass

	def asxnd(self, model="simple"):
		isrequired = False
		node = misc.first(self[required], None)
		if node is not None:
			value = str(node).strip()
			if value in ("true", "yes"):
				isrequired = True
			elif value not in ("false", "no"):
				raise ValueError("value {!r} not allowed for tag <required>".format(value))
		return xnd.Attr(str(self[name][0].content), "xsc.TextAttr", isrequired)


class bodycontent(xsc.Element):
	"""
	Provides a hint as to the content of the body of this tag. Primarily
	intended for use by page composition tools.

	There are currently three values specified:

	``tagdependent``
		The body of the tag is interpreted by the tag implementation itself,
		and is most likely in a different "language", e.g embedded SQL statements.

	``JSP``
		The body of the tag contains nested JSP syntax.

		``empty``
			The body must be empty.

	The default (if not defined) is ``JSP``.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class info(xsc.Element):
	"""
	Defines an arbitrary text string describing the tag library.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass

	def asxnd(self, model="simple"):
		return self.content.string()


class jspversion(xsc.Element):
	"""
	Describes the JSP version (number) this taglibrary requires in order to
	function (dewey decimal). The default is ``1.1``.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class name(xsc.Element):
	"""
	Defines the canonical name of a tag or attribute being defined.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class required(xsc.Element):
	"""
	Defines if the nesting attribute is required or optional. Valid value are
	``true``, ``false``, ``yes`` and ``no``.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class rtexprvalue(xsc.Element):
	"""
	Defines if the nesting attribute can have scriptlet expressions as a value,
	i.e the value of the attribute may be dynamically calculated at request
	time, as opposed to a static value determined at translation time. Valid
	value are ``true``, ``false``, ``yes`` and ``no``.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class shortname(xsc.Element):
	"""
	Defines a short (default) shortname to be used for tags and variable names
	used/created by this tag library.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class tag(xsc.Element):
	"""
	The tag defines a unique tag in this tag library, defining:

	*	the unique tag/element name

	*	the subclass of :class:`javax.servlet.jsp.tagext.Tag` implementation class

	*	an optional subclass of :class:`javax.servlet.jsp.tagext.TagExtraInfo`

	*	the body content type (hint)

	*	optional tag-specific information

	*	any attributes
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass

	def asxnd(self, model="simple"):
		e = xnd.Element(None, str(self[name][0].content))
		empty = None
		node = misc.first(self[bodycontent], None)
		if node is not None:
			value = str(node[0].content)
			if value in ("tagdependent", "JSP"):
				empty = False
			elif value == "empty":
				empty = True
			else:
				raise ValueError("value {!r} is not allowed for tag <bodycontent>".format(value))
		if model != "none":
			if model == "simple":
				e.modeltype = not empty
			else:
				e.modeltype = "sims.Empty" if empty else "sims.Any"
		node = misc.first(self[info], None)
		if node is not None:
			e.doc = node.asxnd(model=model)
		for attr in self[attribute]:
			e += attr.asxnd(model=model)
		return e


class tagclass(xsc.Element):
	"""
	Defines the subclass of :class:`javax.serlvet.jsp.tagext.Tag` that
	implements the request time semantics for this tag.

	The content has to be a fully qualified Java class name.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class taglib(xsc.Element):
	"""
	The taglib tag is the document root, it defines:

	``tlibversion``
		The version of the tag library implementation

	``jspversion``
		The version of JSP the tag library depends upon

	``shortname``
		A simple default short name that could be used by a JSP authoring tool
		to create names with a mnemonic value; for example, the it may be used
		as the prefered prefix value in taglib directives.

	``uri``
		A URL uniquely identifying this taglib

	``info``
		A simple string describing the "use" of this taglib, should be user
		discernable.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass

	def asxnd(self, model="simple"):
		ns = xnd.Module()
		node = misc.first(self[uri], None)
		xmlns = str(node[0].content) if node is not None else None
		node = misc.first(self[info], None)
		if node is not None:
			ns.doc = node.asxnd(model=model)
		for node in self[tag]:
			e = node.asxnd(model=model)
			if xmlns is not None and isinstance(e, xnd.Element):
				e.xmlns = xmlns
			ns += e
		return ns


class teiclass(xsc.Element):
	"""
	Defines the subclass of :class:`javax.servlet.jsp.tagext.TagExtraInfo` for
	this tag. If this is not given, the class is not consulted at translation
	time. The content has to be a fully qualified Java class name.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class tlibversion(xsc.Element):
	"""
	Describes this version (number) of the taglibrary (dewey decimal).
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class uri(xsc.Element):
	"""
	Defines a public URI that uniquely identifies this version of the taglibrary.
	Leave it empty if it does not apply.
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


taglib.model = sims.Elements(info, tag, jspversion, shortname, tlibversion, uri)
attribute.model = sims.Elements(rtexprvalue, required, name)
tag.model = sims.Elements(tagclass, info, name, bodycontent, attribute, teiclass)
bodycontent.model = \
info.model = \
jspversion.model = \
name.model = \
required.model = \
rtexprvalue.model = \
shortname.model = \
tagclass.model = \
teiclass.model = \
tlibversion.model = \
uri.model = sims.NoElements()
