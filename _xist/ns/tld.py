#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

## Copyright 1999-2003 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2003 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license

"""
<par>This is the &xist; namespace for the JavaServer Pages 1.1 Tag Library
descriptor (<lit>.tld</lit>) (&xml;) file format/syntax.</par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from ll.xist import xsc
from ll.xist.ns import xndl

class IdAttrs(xsc.Element.Attrs):
	class id(xsc.IDAttr): pass

class DocTypeTLD11(xsc.DocType):
	"""
	<par>document type for tag library descriptors version 1.1</par>
	"""
	def __init__(self):
		xsc.DocType.__init__(self, 'taglib PUBLIC "-//Sun Microsystems, Inc.//DTD JSP Tag Library 1.1//EN" "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd"')

class attribute(xsc.Element):
	"""
	<par>The attribute tag defines an attribute for the nesting tag</par>
	<par>An attribute definition is composed of:</par>
	<ulist>
		<item>the attributes name (required)</item>
		<item>if the attribute is required or optional (optional)</item>
		<item>if the attributes value may be dynamically calculated at
				runtime by a scriptlet expression (optional)
		</item>
	</ulist>
	"""
	empty = False
	class Attrs(IdAttrs): pass

	def convert(self, converter):
		e = xndl.attr(name=self.find(type=name)[0].content)
		isRequired = None
		l = self.find(type=required)
		if l:
			value = str(l[0].content)
			if value in ('true', 'yes'):
				isRequired = True
			elif value in ('false', 'no'):
				isRequired = None
			else:
				raise ValueError('value %s not allowed for tag <required>' % value)
		e['required'] = isRequired
		return e.convert(converter)

class bodycontent(xsc.Element):
	"""
	<par>Provides a hint as to the content of the body of this tag.
	Primarily intended for use by page composition tools.</par>

	<par>There are currently three values specified:</par>
	<ulist>
		<item><lit>tagdependent</lit>: The body of the tag is interpreted
			by the tag implementation itself, and is most likely in a
			different <z>language</z>, e.g embedded &sql; statements.
		</item>
		<item><lit>JSP</lit>: The body of the tag contains nested &jsp; syntax</item>
		<item><lit>empty</lit>: The body must be empty</item>
	</ulist>
	<par>The default (if not defined) is <lit>JSP</lit>.</par>
	<par>Valid values: <lit>tagdependent</lit>, <lit>JSP</lit>,
	<lit>empty</lit>.</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

class info(xsc.Element):
	"""
	<par>Defines an arbitrary text string describing the tag library.</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

	def convert(self, converter):
		e = xndl.doc(self.content)
		return e.convert(converter)

class jspversion(xsc.Element):
	"""
	<par>Describes the &jsp; version (number) this taglibrary requires in
	order to function (dewey decimal). The default is <lit>1.1</lit>.</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

class name(xsc.Element):
	"""
	<par>Defines the canonical name of a tag or attribute being defined.</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

class required(xsc.Element):
	"""
	<par>Defines if the nesting attribute is required or optional.</par>
	<par>Valid values: <lit>true</lit>, <lit>false</lit>, <lit>yes</lit>,
	<lit>no</lit>.</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

class rtexprvalue(xsc.Element):
	"""
	<par>Defines if the nesting attribute can have scriptlet expressions as
	a value, i.e the value of the attribute may be dynamically calculated
	at request time, as opposed to a static value determined at translation
	time.</par>
	<par>Valid values: <lit>true</lit>, <lit>false</lit>, <lit>yes</lit>,
	<lit>no</lit>.</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

class shortname(xsc.Element):
	"""
	<par>Defines a short (default) shortname to be used for tags and
	variable names used/created by this tag library.</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

class tag(xsc.Element):
	"""
	<par>The tag defines a unique tag in this tag library, defining:</par>
	<ulist>
		<item>the unique tag/element name</item>
		<item>the subclass of <class>javax.servlet.jsp.tagext.Tag</class> implementation class</item>
		<item>an optional subclass of <class>javax.servlet.jsp.tagext.TagExtraInfo</class></item>
		<item>the body content type (hint)</item>
		<item>optional tag-specific information</item>
		<item>any attributes</item>
	</ulist>
	"""
	empty = False
	class Attrs(IdAttrs): pass

	def convert(self, converter):
		e = xndl.element(name=self.find(type=name)[0].content)
		l = self.find(type=bodycontent)
		isEmpty = None
		if l:
			value = str(l[0].content)
			if value in ('tagdependent', 'JSP'):
				isEmpty = None
			elif value == 'empty':
				isEmpty = True
			else:
				raise ValueError("value %s is not allowed for tag <bodycontent>" % value)
		e['empty'] = isEmpty
		e.append(self.find(type=info))
		e.append(self.find(type=attribute))
		return e.convert(converter)
		

class tagclass(xsc.Element):
	"""
	<par>Defines the subclass of <class>javax.serlvet.jsp.tagext.Tag</class>
	that implements the request time semantics for this tag.</par>
	<par>The content has to be a fully qualified Java class name.</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

class taglib(xsc.Element):
	"""
	<par>The taglib tag is the document root, it defines:</par>
	<ulist>
		<item><lit>tlibversion</lit>: The version of the tag library implementation</item>
		<item><lit>jspversion</lit>: The version of JSP the tag library depends upon</item>
		<item><lit>shortname</lit>: A simple default short name that could be used by
					a &jsp; authoring tool to create names with a mnemonic
					value; for example, the it may be used as the prefered
					prefix value in taglib directives.
		</item>
		<item><lit>uri</lit>: A &url; uniquely identifying this taglib</item>
		<item><lit>info</lit>: A simple string describing the <z>use</z> of
				this taglib, should be user discernable
		</item>
	</ulist>
	"""
	empty = False
	class Attrs(IdAttrs): pass

	def convert(self, converter):
		e = xndl.xndl()
		e['name'] = str(self.find(type=shortname)[0].content)
		l = self.find(type=uri)
		if l:
			e["url"] = l[0].content
		e.append(self.find(type=info))
		e.append(self.find(type=tag))
		return e.convert(converter)

class teiclass(xsc.Element):
	"""
	<par>Defines the subclass of <class>javax.servlet.jsp.tagext.TagExtraInfo</class>
	for this tag. If this is not given, the class is not consulted at
	translation time.</par>
	<par>The content has to be a fully qualified Java class name.</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

class tlibversion(xsc.Element):
	"""
	<par>Describes this version (number) of the taglibrary (dewey decimal).</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

class uri(xsc.Element):
	"""
	<par>Defines a public URI that uniquely identifies this version of
	the taglibrary. Leave it empty if it does not apply.</par>
	"""
	empty = False
	class Attrs(IdAttrs): pass

class xmlns(xsc.Namespace):
	xmlname = "tld"
	xmlurl = "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd"
xmlns.makemod(vars())

