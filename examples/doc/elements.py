#! /usr/bin/env python

"""
This module contains all the elements used in creating HTML documentation out of docstrings.

Some of the elements are used by the <moduleref>doc</moduleref> module on it's own when
an XML documentation tree is created for an object (see the function
<functionref module="doc">explain</functionref> in the module <moduleref>doc</moduleref>).

Other elements can be used by the user in the docstrings themselves, e.g. to refer to
other modules, functions, classes or methods.
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import types
import string

from xist import xsc
from xist.ns import html, specials

class par(html.div):
	empty = 0
	attrHandlers = html.div.attrHandlers.copy()
	attrHandlers.update({"noindent": xsc.TextAttr})

	def convert(self, converter):
		e = html.div(self.content.clone())
		indent = 1
		for attr in self.attrs.keys():
			if attr == "noindent":
				indent = None
			else:
				e[attr] = self[attr]
		if indent is not None:
			e["class"] = "indent"
		return e.convert(converter)

class module(xsc.Element):
	"""
	is the top element of a module description it contains a name (as an attribute),
	a description and lists of functions and classes.
	"""
	empty = 0
	attrHandlers = {"name": xsc.TextAttr}
	
	def convert(self, converter):
		b = specials.plainbody(
			html.h1("Module ",html.code(self["name"],**{"class": "module"}))
		)
		b.extend(self.content)
		e = html.html(
			html.head(
				html.link(rel="stylesheet",href="doc.css")
			),
			b
		)
		return e.convert(converter)

class classes(xsc.Element):
	"""
	contains class elements
	"""
	empty = 0

	def convert(self, converter):
		e = xsc.Frag(html.h2("Classes"))
		e.extend(self.content.convert(converter))
		return e

class functions(xsc.Element):
	"""
	contains function elements
	"""
	empty = 0

	def convert(self, converter):
		e = xsc.Frag(html.h2("Functions"))
		e.extend(self.content.convert(converter))
		return e

class methods(xsc.Element):
	"""
	contains method elements
	"""
	empty = 0

	def convert(self, converter):
		e = xsc.Frag(html.h3("Methods"))
		e.extend(self.content.convert(converter))
		return e

class function(xsc.Element):
	"""
	contains the description of a function. This element
	has a <code>name</code> attribute, and contains a
	<code>signature</code> and a <code>desc</code> element.
	"""
	empty = 0
	attrHandlers = {"name": xsc.TextAttr}

	def convert(self, converter):
		e = xsc.Frag(html.h3(self["name"]))
		sig = self.find(type=signature)[0]
		e.append(html.div(html.code(self["name"], "(", sig.find(type=arg).withSeparator(", "), ")", class_="function"), class_="function"))
		descs = self.find(type=desc)
		if len(descs):
			e.append(html.div(descs[0]))
		return e.convert(converter)

class method(xsc.Element):
	empty = 0
	attrHandlers = {"name": xsc.TextAttr}

	def convert(self, converter):
		e = html.div(class_="method")
		sig = self.find(type=signature)[0]
		e.append(
			html.div(
				html.code(
					Self(),
					".",
					html.span(self["name"], class_="name"),
					"(",
					sig.find(type=arg)[1:].withSeparator(", "), # drop the self from the arguments
					"):",
					class_="method"
				),
				class_="name"
			)
		)
		descs = self.find(type=desc)
		if len(descs):
			e.append(descs[0])
		return e.convert(converter)

class Class(xsc.Element):
	empty = 0
	attrHandlers = {"name": xsc.TextAttr}

	def convert(self, converter):
		e = xsc.Frag(html.h3("Class ", html.code(self["name"], class_="class")))
		e.extend(self.content)
		return e.convert(converter)

class Self(xsc.Element):
	"""
	use this class when referring to the object for which a method has been
	called, e.g.:
	<pre>
		this function fooifies the object &lt;self/&gt;.
	</pre>
	"""
	empty = 0

	def convert(self, converter):
		return html.code("self", class_="self")

class signature(xsc.Element):
	empty = 0

class desc(xsc.Element):
	empty = 0

	def convert(self, converter):
		e = html.div(self.content.convert(converter), class_="description")

		return e

class arg(xsc.Element):
	empty = 1
	attrHandlers = {"name": xsc.TextAttr, "type": xsc.TextAttr, "default": xsc.TextAttr}

	def convert(self, converter):
		e = xsc.Frag()
		if self.hasAttr("type"):
			type = self["type"].convert(converter).asPlainString()
			if type=="positional":
				e.append("*")
			elif type=="keyword":
				e.append("**")
		e.append(html.code(self["name"].convert(converter),class_="arg"))
		if self.hasAttr("default"):
			e.append("=",self["default"].convert(converter))
		return e.convert(converter)

class attr(xsc.Element):
	empty = 0

	def convert(self, converter):
		return html.code(self.content, class_="attr").convert(converter)

# build a namespace with all the classes we've defined so far
namespace = xsc.Namespace("doc","http://www.livinglogic.de/DTDs/doc.dtd",vars())

