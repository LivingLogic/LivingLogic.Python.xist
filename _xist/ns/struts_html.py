#! /usr/bin/env python

"""
A module that allows you to embed struts html custom tag library.
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

from xist import xsc

class taglib(xsc.Element):
	empty = 1
	def publish(self, publisher):
		publisher.publish(u"<%@ taglib uri=\"/WEB-INF/struts-html.tld\" prefix=\"struts_html\" %>")

class Element(xsc.Element):
	"""
	common base class for all the struts html elements
	"""
	publishPrefix = 1

class base(Element):
	"""
	document base URI
	"""
	empty = 1
	attrHandlers = {"target": xsc.URLAttr}

class MouseElement(Element):
	"""
	common base class for all the struts elements which have mouse-attributes
	"""
	attrHandlers = {"accesskey": xsc.TextAttr, "onblur": xsc.TextAttr, "onchange": xsc.TextAttr, "onclick": xsc.TextAttr}
	attrHandlers.update({"ondblclick": xsc.TextAttr, "onfocus": xsc.TextAttr, "onkeydown": xsc.TextAttr, "onkeypress": xsc.TextAttr})
	attrHandlers.update({"onkeyup": xsc.TextAttr, "onmousedown": xsc.TextAttr, "onmousemove": xsc.TextAttr, "onmouseout": xsc.TextAttr})
	attrHandlers.update({"onmouseover": xsc.TextAttr, "onmouseup": xsc.TextAttr, "style": xsc.TextAttr, "styleClass": xsc.TextAttr, "tabindex": xsc.TextAttr})

class button(MouseElement):
	"""
	a button
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"property": xsc.TextAttr, "value": xsc.TextAttr})

class cancel(MouseElement):
	"""
	a cancel button
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"property": xsc.TextAttr, "value": xsc.TextAttr})

class checkbox(MouseElement):
	"""
	a html checkbox element
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"name": xsc.TextAttr, "property": xsc.TextAttr, "value": xsc.TextAttr})

class errors(Element):
	"""
	displays error messages which have been generated from an action or a validation method
	"""
	empty = 1
	attrHandlers = {"bundle": xsc.TextAttr, "locale": xsc.TextAttr, "name": xsc.TextAttr, "property": xsc.TextAttr}

class file(MouseElement):
	"""
	html input element of type file
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"accept": xsc.TextAttr, "maxlength": xsc.TextAttr, "name": xsc.TextAttr, "property": xsc.TextAttr, "value": xsc.TextAttr})

class form(Element):
	"""
	html form
	"""
	empty = 0
	attrHandlers = {"action": xsc.TextAttr, "enctype": xsc.TextAttr, "focus": xsc.TextAttr, "method": xsc.TextAttr, "name": xsc.TextAttr}
	attrHandlers.update({"onreset": xsc.TextAttr, "onsubmit": xsc.TextAttr, "scope": xsc.TextAttr, "style": xsc.TextAttr, "styleClass": xsc.TextAttr})
	attrHandlers.update({"target": xsc.TextAttr, "type": xsc.TextAttr})

class hidden(Element):
	"""
	hidden form field
	"""
	empty = 1
	attrHandlers = {"name": xsc.TextAttr, "property": xsc.TextAttr, "value": xsc.TextAttr}

class image(MouseElement):
	"""
	image input
	"""
	empty = 1
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"locale": xsc.TextAttr, "bundle": xsc.TextAttr, "property": xsc.TextAttr, "src": xsc.TextAttr, "style": xsc.TextAttr, "styleClass": xsc.TextAttr})
	attrHandlers.update({"value": xsc.TextAttr, "path": xsc.TextAttr, "isKey": xsc.BoolAttr})

class img(Element):
	"""
	html img tag
	"""
	empty = 0
	attrHandlers = {"accesskey": xsc.TextAttr, "align": xsc.TextAttr, "alt": xsc.TextAttr, "border": xsc.TextAttr}
	attrHandlers.update({"height": xsc.TextAttr, "hspace": xsc.TextAttr, "imageName": xsc.TextAttr, "ismap": xsc.TextAttr})
	attrHandlers.update({"lowsrc": xsc.TextAttr, "name": xsc.TextAttr, "onkeydown": xsc.TextAttr, "onkeypress": xsc.TextAttr})
	attrHandlers.update({"onkeyup": xsc.TextAttr, "paramId": xsc.TextAttr, "page": xsc.TextAttr, "paramName": xsc.TextAttr})
	attrHandlers.update({"paramProperty": xsc.TextAttr, "paramScope": xsc.TextAttr, "property": xsc.TextAttr, "scope": xsc.TextAttr})
	attrHandlers.update({"src": xsc.TextAttr, "style": xsc.TextAttr, "styleClass": xsc.TextAttr, "usemap": xsc.TextAttr})
	attrHandlers.update({"vspace": xsc.TextAttr, "width": xsc.TextAttr})
	
class link(MouseElement):
	"""
	html link
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"forward": xsc.TextAttr, "href": xsc.URLAttr, "linkName": xsc.TextAttr, "name": xsc.TextAttr})
	attrHandlers.update({"paramId": xsc.TextAttr, "page": xsc.TextAttr, "paramName": xsc.TextAttr})
	attrHandlers.update({"paramProperty": xsc.TextAttr, "paramScope": xsc.TextAttr, "property": xsc.TextAttr, "scope": xsc.TextAttr})
	attrHandlers.update({"target": xsc.TextAttr})

class multibox(MouseElement):
	"""
	multiple checkbox element
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"name": xsc.TextAttr, "property": xsc.TextAttr, "value": xsc.TextAttr})

class option(Element):
	"""
	option element
	"""
	empty = 1
	attrHandlers = {"value": xsc.TextAttr}

class options(Element):
	"""
	struts html options element
	"""
	empty = 1
	attrHandlers = {"collection": xsc.TextAttr, "labelName": xsc.TextAttr, "labelProperty": xsc.TextAttr, "name": xsc.TextAttr, "property": xsc.TextAttr}

class password(MouseElement):
	"""
	a password text input field
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"maxlength": xsc.TextAttr, "name": xsc.TextAttr, "property": xsc.TextAttr, "size": xsc.TextAttr, "value": xsc.TextAttr})

class radio(Element):
	"""
	html input radio
	"""
	attrHandlers = {"accesskey": xsc.TextAttr, "name": xsc.TextAttr, "onblur": xsc.TextAttr, "onchange": xsc.TextAttr, "onclick": xsc.TextAttr}
	attrHandlers.update({"ondblclick": xsc.TextAttr, "onfocus": xsc.TextAttr, "onkeydown": xsc.TextAttr, "onkeypress": xsc.TextAttr})
	attrHandlers.update({"onkeyup": xsc.TextAttr, "onmousedown": xsc.TextAttr, "property": xsc.TextAttr, "value": xsc.TextAttr})

class reset(MouseElement):
	"""
	a reset button
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"style": xsc.TextAttr, "styleClass": xsc.TextAttr})

class rewrite(Element):
	"""
	render a request uri like html link
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers = {"forward": xsc.TextAttr, "href": xsc.URLAttr, "name": xsc.TextAttr}
	attrHandlers.update({"page": xsc.TextAttr, "property": xsc.TextAttr, "scope": xsc.TextAttr})

class select(MouseElement):
	"""
	a select element text input field
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"multiple": xsc.BoolAttr, "name": xsc.TextAttr, "property": xsc.TextAttr, "size": xsc.TextAttr, "value": xsc.TextAttr})

class submit(MouseElement):
	"""
	a submit button
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"property": xsc.TextAttr, "value": xsc.TextAttr})

class text(MouseElement):
	"""
	a text input field
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"maxlength": xsc.TextAttr, "name": xsc.TextAttr, "property": xsc.TextAttr, "size": xsc.TextAttr, "value": xsc.TextAttr})

class textarea(MouseElement):
	"""
	a textarea
	"""
	empty = 0
	attrHandlers = MouseElement.attrHandlers.copy()
	attrHandlers.update({"cols": xsc.TextAttr, "name": xsc.TextAttr, "property": xsc.TextAttr, "rows": xsc.TextAttr, "value": xsc.TextAttr})



# register all the classes we've defined so far
namespace = xsc.Namespace("struts_html", "", vars())
