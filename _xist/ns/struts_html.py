#! /usr/bin/env python
# -*- coding: Latin-1 -*-

## Copyright 1999-2002 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2002 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
<doc:par>A module that allows you to embed tags from
the <a href="http://jakarta.apache.org/struts/">Struts</a>
html custom tag library.</doc:par>
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc

class taglib(xsc.ProcInst):
	"""
	creates a standard struts taglib header
	"""
	needsxmlnsdef = 0
	needsxmlnsuse = 1

	def publish(self, publisher):
		publisher.publish(u'<%%@ taglib uri="/WEB-INF/struts-html.tld" prefix="%s" %%>' % publisher.prefixes2use[self.xmlns])

class Element(xsc.Element):
	"""
	common base class for all the struts html elements
	"""
	needsxmlnsuse = 1

class base(Element):
	"""
	document base URI
	"""
	empty = True
	class Attrs(Element.Attrs):
		class target(xsc.URLAttr): pass

class MouseElement(Element):
	"""
	common base class for all the struts elements which have mouse attributes
	"""
	class Attrs(Element.Attrs):
		class accesskey(xsc.TextAttr): pass
		class onblur(xsc.TextAttr): pass
		class onchange(xsc.TextAttr): pass
		class onclick(xsc.TextAttr): pass
		class ondblclick(xsc.TextAttr): pass
		class onfocus(xsc.TextAttr): pass
		class onkeydown(xsc.TextAttr): pass
		class onkeypress(xsc.TextAttr): pass
		class onkeyup(xsc.TextAttr): pass
		class onmousedown(xsc.TextAttr): pass
		class onmousemove(xsc.TextAttr): pass
		class onmouseout(xsc.TextAttr): pass
		class onmouseover(xsc.TextAttr): pass
		class onmouseup(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass
		class tabindex(xsc.TextAttr): pass

class button(MouseElement):
	"""
	a button
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class property(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class cancel(MouseElement):
	"""
	a cancel button
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class property(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class checkbox(MouseElement):
	"""
	a html checkbox element
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class errors(Element):
	"""
	displays error messages which have been generated from an action or a validation method
	"""
	empty = True
	class Attrs(Element.Attrs):
		class bundle(xsc.TextAttr): pass
		class locale(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass

class file(MouseElement):
	"""
	html input element of type file
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class accept(xsc.TextAttr): pass
		class maxlength(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class form(Element):
	"""
	html form
	"""
	empty = False
	class Attrs(Element.Attrs):
		class action(xsc.TextAttr): pass
		class enctype(xsc.TextAttr): pass
		class focus(xsc.TextAttr): pass
		class method(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class onreset(xsc.TextAttr): pass
		class onsubmit(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass
		class target(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass

class hidden(Element):
	"""
	hidden form field
	"""
	empty = True
	class Attrs(Element.Attrs):
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class image(MouseElement):
	"""
	image input
	"""
	empty = True
	class Attrs(MouseElement.Attrs):
		class locale(xsc.TextAttr): pass
		class bundle(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class src(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass
		class path(xsc.TextAttr): pass
		class isKey(xsc.BoolAttr): pass

class img(Element):
	"""
	html img tag
	"""
	empty = False
	class Attrs(Element.Attrs):
		class accesskey(xsc.TextAttr): pass
		class align(xsc.TextAttr): pass
		class alt(xsc.TextAttr): pass
		class border(xsc.TextAttr): pass
		class height(xsc.TextAttr): pass
		class hspace(xsc.TextAttr): pass
		class imageName(xsc.TextAttr): pass
		class ismap(xsc.TextAttr): pass
		class lowsrc(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class onkeydown(xsc.TextAttr): pass
		class onkeypress(xsc.TextAttr): pass
		class onkeyup(xsc.TextAttr): pass
		class paramId(xsc.TextAttr): pass
		class page(xsc.TextAttr): pass
		class paramName(xsc.TextAttr): pass
		class paramProperty(xsc.TextAttr): pass
		class paramScope(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class src(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass
		class usemap(xsc.TextAttr): pass
		class vspace(xsc.TextAttr): pass
		class width(xsc.TextAttr): pass

class link(MouseElement):
	"""
	html link
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class forward(xsc.TextAttr): pass
		class href(xsc.URLAttr): pass
		class linkName(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class paramId(xsc.TextAttr): pass
		class page(xsc.TextAttr): pass
		class paramName(xsc.TextAttr): pass
		class paramProperty(xsc.TextAttr): pass
		class paramScope(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class target(xsc.TextAttr): pass

class multibox(MouseElement):
	"""
	multiple checkbox element
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class option(Element):
	"""
	option element
	"""
	empty = False
	class Attrs(Element.Attrs):
		class value(xsc.TextAttr): pass

class options(Element):
	"""
	struts html options element
	"""
	empty = True
	class Attrs(Element.Attrs):
		class collection(xsc.TextAttr): pass
		class labelName(xsc.TextAttr): pass
		class labelProperty(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass

class password(MouseElement):
	"""
	a password text input field
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class maxlength(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class size(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class radio(Element):
	"""
	html input radio
	"""
	class Attrs(Element.Attrs):
		class accesskey(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class onblur(xsc.TextAttr): pass
		class onchange(xsc.TextAttr): pass
		class onclick(xsc.TextAttr): pass
		class ondblclick(xsc.TextAttr): pass
		class onfocus(xsc.TextAttr): pass
		class onkeydown(xsc.TextAttr): pass
		class onkeypress(xsc.TextAttr): pass
		class onkeyup(xsc.TextAttr): pass
		class onmousedown(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class reset(MouseElement):
	"""
	a reset button
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass

class rewrite(Element):
	"""
	render a request uri like html link
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class forward(xsc.TextAttr): pass
		class href(xsc.URLAttr): pass
		class name(xsc.TextAttr): pass
		class page(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass

class select(MouseElement):
	"""
	a select element text input field
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class multiple(xsc.BoolAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class size(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class submit(MouseElement):
	"""
	a submit button
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class property(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class text(MouseElement):
	"""
	a text input field
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class maxlength(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class size(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

class textarea(MouseElement):
	"""
	a textarea
	"""
	empty = False
	class Attrs(MouseElement.Attrs):
		class cols(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class rows(xsc.TextAttr): pass
		class wrap(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass

# register all the classes we've defined so far
xmlns = xsc.Namespace("struts_html", "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd", vars())
