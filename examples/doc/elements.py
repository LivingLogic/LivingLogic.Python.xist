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

from xist import xsc,html,specials

class par(html.div):
	empty = 0
	attrHandlers = xsc.appendDict(html.div.attrHandlers,{ "noindent" : xsc.TextAttr })

	def asHTML(self):
		e = html.div(self.content.clone())
		indent = 1
		for attr in self.attrs.keys():
			if attr == "noindent":
				indent = None
			else:
				e[attr] = self[attr]
		if indent is not None:
			e["class"] = "indent"
		return e.asHTML()

class module(xsc.Element):
	"""
	is the top element of a module description it contains a name (as an attribute),
	a description and lists of functions and classes.
	"""
	empty = 0
	attrHandlers = { "name" : xsc.TextAttr }
	
	def asHTML(self):
		b = specials.plainbody(
			html.h1("Module ",html.code(self["name"],Class="module"))
		)
		b.extend(self.content)
		e = html.html(
			html.head(
				html.link(rel="stylesheet",href="doc.css")
			),
			b
		)
		return e.asHTML()

class classes(xsc.Element):
	"""
	contains class elements
	"""
	empty = 0

	def asHTML(self):
		e = xsc.Frag(html.h2("Classes"))
		e.extend(self.content.asHTML())
		return e

class functions(xsc.Element):
	"""
	contains function elements
	"""
	empty = 0

	def asHTML(self):
		e = xsc.Frag(html.h2("Functions"))
		e.extend(self.content.asHTML())
		return e

class methods(xsc.Element):
	"""
	contains method elements
	"""
	empty = 0

	def asHTML(self):
		e = xsc.Frag(html.h3("Methods"))
		e.extend(self.content.asHTML())
		return e

class function(xsc.Element):
	"""
	contains the description of a function. This element
	has a <code>name</code> attribute, and contains a
	<code>signature</code> and a <code>desc</code> element.
	"""
	empty = 0
	attrHandlers = { "name" : xsc.TextAttr }

	def asHTML(self):
		e = xsc.Frag(html.h3(self["name"]))
		sig = self.findNodes(type = signature)[0]
		e.append(html.div(html.code(self["name"],"(",sig.findNodes(type = arg).withSeparator(", "),")",Class="function"),Class="function"))
		descs = self.findNodes(type = desc)
		if len(descs):
			e.append(html.div(descs[0]))
		return e.asHTML()

class method(xsc.Element):
	empty = 0
	attrHandlers = { "name" : xsc.TextAttr }

	def asHTML(self):
		e = html.div(Class="method")
		sig = self.findNodes(type = signature)[0]
		e.append(
			html.div(
				html.code(
					Self(),
					".",
					html.span(self["name"],Class="name"),
					"(",
					sig.findNodes(type = arg)[1:].withSeparator(", "), # drop the self from the arguments
					"):",
					Class="method"
				),
				Class="name"
			)
		)
		descs = self.findNodes(type = desc)
		if len(descs):
			e.append(descs[0])
		return e.asHTML()

class Class(xsc.Element):
	empty = 0
	attrHandlers = { "name" : xsc.TextAttr }

	def asHTML(self):
		e = xsc.Frag(html.h3("Class ",html.code(self["name"],Class="class")))
		e.append(self.content)
		return e.asHTML()

class Self(xsc.Element):
	"""
	use this class when referring to the object for which a method has been
	called, e.g.:
	<pre>
		this function fooifies the object &lt;self/&gt;.
	</pre>
	"""
	empty = 0

	def asHTML(self):
		return html.code("self",Class="self")

class signature(xsc.Element):
	empty = 0

class desc(xsc.Element):
	empty = 0

	def asHTML(self):
		e = html.div(self.content.asHTML(),Class = "description")

		return e

class arg(xsc.Element):
	empty = 1
	attrHandlers = { "name" : xsc.TextAttr , "type" : xsc.TextAttr , "default" : xsc.TextAttr }

	def asHTML(self):
		e = xsc.Frag()
		if self.hasAttr("type"):
			type = self["type"].asHTML().asPlainString()
			if type=="positional":
				e.append("*")
			elif type=="keyword":
				e.append("**")
		e.append(html.code(self["name"].asHTML(),Class="arg"))
		if self.hasAttr("default"):
			e.append("=",self["default"].asHTML())
		return e.asHTML()

class moduleref(xsc.Element):
	"""
	use this element to refer to another module, e.g.:
	<pre>
		see the module &lt;moduleref&gt;foo&lt;/moduleref&gt; for further details.
	</pre>
	"""
	empty = 0

	def asHTML(self):
		return html.code(self.content,Class = "module").asHTML()

class functionref(xsc.Element):
	"""
	use this element to refer to a function, e.g.:
	<pre>
		see the function &lt;moduleref&gt;foo&lt;/moduleref&gt; for further details.
	</pre>
	if the function referred to is in another module you can specify this module
	via the <attr>module</attr> attribute.
	"""
	empty = 0
	attrHandlers = { "module" : xsc.TextAttr }

	def asHTML(self):
		return html.code(self.content,Class = "function").asHTML()

class classref(xsc.Element):
	empty = 0
	attrHandlers = { "module" : xsc.TextAttr }

	def asHTML(self):
		return html.code(self.content,Class = "class").asHTML()

class methodref(xsc.Element):
	empty = 0
	attrHandlers = { "module" : xsc.TextAttr , "class" : xsc.TextAttr }

	def asHTML(self):
		return html.code(self.content,Class = "method").asHTML()

class argref(xsc.Element):
	empty = 0

	def asHTML(self):
		return html.code(self.content,Class = "arg").asHTML()

class argref(xsc.Element):
	empty = 0
	attrHandlers = { "type" : xsc.TextAttr }

	def asHTML(self):
		return html.code(self.content,Class = "arg").asHTML()

class argref(xsc.Element):
	empty = 0
	attrHandlers = { "type" : xsc.TextAttr }

	def asHTML(self):
		return html.code(self.content,Class = "arg").asHTML()

class attr(xsc.Element):
	empty = 0

	def asHTML(self):
		return html.code(self.content,Class = "attr").asHTML()

# register all the classes we've defined so far
xsc.registerAllElements(vars(),"doc")

