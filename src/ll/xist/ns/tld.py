# -*- coding: utf-8 -*-

## Copyright 1999-2008 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


"""
<p>This is the &xist; namespace for the JavaServer Pages 1.1 Tag Library
descriptor (<lit>.tld</lit>) (&xml;) file format/syntax.</p>
"""


from ll import misc
from ll.xist import xsc, sims, xnd, xfind


__docformat__ = "xist"


xmlns = "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd"


class IdAttrs(xsc.Attrs):
	class id(xsc.IDAttr): pass


class DocTypeTLD11(xsc.DocType):
	"""
	<p>document type for tag library descriptors version 1.1</p>
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'taglib PUBLIC "-//Sun Microsystems, Inc.//DTD JSP Tag Library 1.1//EN" "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd"')


class attribute(xsc.Element):
	"""
	<p>The attribute tag defines an attribute for the nesting tag</p>
	<p>An attribute definition is composed of:</p>
	<ul>
	<li>the attributes name (required)</li>
	<li>if the attribute is required or optional (optional)</li>
	<li>if the attributes value may be dynamically calculated at runtime by a
	scriptlet expression (optional)</li>
	</ul>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass

	def asxnd(self):
		e = xnd.Attr(unicode(self[name][0].content), u"xsc.TextAttr")
		isrequired = None
		node = misc.first(self[required], None)
		if node is not None:
			value = unicode(node[0].content)
			if value in (u"true", u"yes"):
				isrequired = True
			elif value in (u"false", u"no"):
				isrequired = None
			else:
				raise ValueError("value %s not allowed for tag <required>" % value)
		e.required = isrequired
		return e


class bodycontent(xsc.Element):
	"""
	<p>Provides a hint as to the content of the body of this tag.
	Primarily intended for use by page composition tools.</p>

	<p>There are currently three values specified:</p>
	<ul>
		<li><lit>tagdependent</lit>: The body of the tag is interpreted
			by the tag implementation itself, and is most likely in a
			different <z>language</z>, e.g embedded &sql; statements.
		</li>
		<li><lit>JSP</lit>: The body of the tag contains nested &jsp; syntax</li>
		<li><lit>empty</lit>: The body must be empty</li>
	</ul>
	<p>The default (if not defined) is <lit>JSP</lit>.</p>
	<p>Valid values: <lit>tagdependent</lit>, <lit>JSP</lit>,
	<lit>empty</lit>.</p>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class info(xsc.Element):
	"""
	<p>Defines an arbitrary text string describing the tag library.</p>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass

	def asxnd(self):
		return self.content.string()


class jspversion(xsc.Element):
	"""
	<p>Describes the &jsp; version (number) this taglibrary requires in
	order to function (dewey decimal). The default is <lit>1.1</lit>.</p>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class name(xsc.Element):
	"""
	<p>Defines the canonical name of a tag or attribute being defined.</p>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class required(xsc.Element):
	"""
	<p>Defines if the nesting attribute is required or optional.</p>
	<p>Valid values: <lit>true</lit>, <lit>false</lit>, <lit>yes</lit>,
	<lit>no</lit>.</p>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class rtexprvalue(xsc.Element):
	"""
	<p>Defines if the nesting attribute can have scriptlet expressions as
	a value, i.e the value of the attribute may be dynamically calculated
	at request time, as opposed to a static value determined at translation
	time.</p>
	<p>Valid values: <lit>true</lit>, <lit>false</lit>, <lit>yes</lit>,
	<lit>no</lit>.</p>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class shortname(xsc.Element):
	"""
	<p>Defines a short (default) shortname to be used for tags and
	variable names used/created by this tag library.</p>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class tag(xsc.Element):
	"""
	<p>The tag defines a unique tag in this tag library, defining:</p>
	<ul>
		<li>the unique tag/element name</li>
		<li>the subclass of <class>javax.servlet.jsp.tagext.Tag</class> implementation class</li>
		<li>an optional subclass of <class>javax.servlet.jsp.tagext.TagExtraInfo</class></li>
		<li>the body content type (hint)</li>
		<li>optional tag-specific information</li>
		<li>any attributes</li>
	</ul>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass

	def asxnd(self):
		e = xnd.Element(unicode(self[name][0].content))
		empty = None
		node = misc.first(self[bodycontent], None)
		if node is not None:
			value = unicode(node[0].content)
			if value in (u"tagdependent", u"JSP"):
				empty = False
			elif value == u"empty":
				empty = True
			else:
				raise ValueError("value %s is not allowed for tag <bodycontent>" % value)
		if empty:
			e.modeltype = "sims.Empty"
		else:
			e.modeltype = "sims.Any"
		node = misc.first(self[info], None)
		if node is not None:
			e.doc = node.asxnd()
		for attr in self[attribute]:
			e.attrs.append(attr.asxnd())
		return e


class tagclass(xsc.Element):
	"""
	<p>Defines the subclass of <class>javax.serlvet.jsp.tagext.Tag</class>
	that implements the request time semantics for this tag.</p>
	<p>The content has to be a fully qualified Java class name.</p>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class taglib(xsc.Element):
	"""
	<p>The taglib tag is the document root, it defines:</p>
	<ul>
		<li><lit>tlibversion</lit>: The version of the tag library implementation</li>
		<li><lit>jspversion</lit>: The version of JSP the tag library depends upon</li>
		<li><lit>shortname</lit>: A simple default short name that could be used by
					a &jsp; authoring tool to create names with a mnemonic
					value; for example, the it may be used as the prefered
					prefix value in taglib directives.
		</li>
		<li><lit>uri</lit>: A &url; uniquely identifying this taglib</li>
		<li><lit>info</lit>: A simple string describing the <z>use</z> of
				this taglib, should be user discernable
		</li>
	</ul>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass

	def asxnd(self):
		e = xnd.Module(unicode(self[shortname][0].content))
		node = misc.first(self[uri], None)
		xmlns = unicode(node[0].content) if node is not None else None
		node = misc.first(self[info], None)
		if node is not None:
			e.doc = node.asxnd()
		for node in self[tag]:
			e2 = node.asxnd()
			if xmlns is not None and isinstance(e2, xnd.Element):
				e2.xmlns = xmlns
			e.content.append(e2)
		return e


class teiclass(xsc.Element):
	"""
	<p>Defines the subclass of <class>javax.servlet.jsp.tagext.TagExtraInfo</class>
	for this tag. If this is not given, the class is not consulted at
	translation time.</p>
	<p>The content has to be a fully qualified Java class name.</p>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class tlibversion(xsc.Element):
	"""
	<p>Describes this version (number) of the taglibrary (dewey decimal).</p>
	"""
	xmlns = xmlns
	class Attrs(IdAttrs): pass


class uri(xsc.Element):
	"""
	<p>Defines a public URI that uniquely identifies this version of
	the taglibrary. Leave it empty if it does not apply.</p>
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
