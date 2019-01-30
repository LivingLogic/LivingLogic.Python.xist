# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
A module that allows you to embed tags from Struts__ html custom tag library.

__ http://jakarta.apache.org/struts/
"""


from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://jakarta.apache.org/struts/tags-html"


class taglib(xsc.ProcInst):
	"""
	Creates a standard struts taglib header
	"""
	xmlns = xmlns

	def publish(self, publisher):
		yield publisher.encode('<%@ taglib uri="/WEB-INF/struts-html.tld" prefix="')
		yield publisher.encode(publisher.getobjectprefix(self))
		yield publisher.encode('" %>')


class Element(xsc.Element):
	"""
	Common base class for all the struts html elements
	"""
	register = False


class PartMouseElement(Element):
	xmlns = xmlns
	class Attrs(Element.Attrs):
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
		class alt(xsc.TextAttr): pass
		class altKey(xsc.TextAttr): pass
		class title(xsc.TextAttr): pass
		class titleKey(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class styleId(xsc.TextAttr): pass


class MouseElement(PartMouseElement):
	"""
	Common base class for all the struts elements which have mouse attributes
	"""
	xmlns = xmlns
	class Attrs(PartMouseElement.Attrs):
		class accesskey(xsc.TextAttr): pass
		class tabindex(xsc.TextAttr): pass
		class disabled(xsc.TextAttr): pass


class base(Element):
	"""
	Document base URI
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(Element.Attrs):
		class target(xsc.URLAttr): pass
		class server(xsc.TextAttr): pass


class button(MouseElement):
	"""
	A button
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(MouseElement.Attrs):
		class indexed(xsc.TextAttr): pass


class cancel(MouseElement):
	"""
	A cancel button
	"""
	xmlns = xmlns
	model = sims.Any()


class checkbox(MouseElement):
	"""
	A html checkbox element
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(MouseElement.Attrs):
		class indexed(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass


class errors(Element):
	"""
	Displays error messages which have been generated from an action or a
	validation method
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(Element.Attrs):
		class bundle(xsc.TextAttr): pass
		class locale(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass


class file(MouseElement):
	"""
	HTML input element of type file
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(MouseElement.Attrs):
		class accept(xsc.TextAttr): pass
		class indexed(xsc.TextAttr): pass
		class maxlength(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class size(xsc.TextAttr): pass


class form(Element):
	"""
	HTML form
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(Element.Attrs):
		class action(xsc.TextAttr): pass
		class enctype(xsc.TextAttr): pass
		class focus(xsc.TextAttr): pass
		class focusIndex(xsc.TextAttr): pass
		class method(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class onreset(xsc.TextAttr): pass
		class onsubmit(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass
		class styleId(xsc.TextAttr): pass
		class target(xsc.TextAttr): pass
		class type(xsc.TextAttr): pass


class frame(Element):
	"""
	Render an HTML frame element
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(Element.Attrs):
		class action(xsc.TextAttr): pass
		class anchor(xsc.TextAttr): pass
		class forward(xsc.TextAttr): pass
		class frameborder(xsc.TextAttr): pass
		class frameName(xsc.TextAttr): pass
		class href(xsc.URLAttr): pass
		class longdesc(xsc.TextAttr): pass
		class marginheight(xsc.TextAttr): pass
		class marginwidth(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class noresize(xsc.TextAttr): pass
		class page(xsc.TextAttr): pass
		class paramId(xsc.TextAttr): pass
		class paramName(xsc.TextAttr): pass
		class paramProperty(xsc.TextAttr): pass
		class paramScope(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class scrolling(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass
		class styleId(xsc.TextAttr): pass
		class title(xsc.TextAttr): pass
		class titleKey(xsc.TextAttr): pass
		class transaction(xsc.TextAttr): pass


class hidden(PartMouseElement):
	"""
	hidden form field
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(PartMouseElement.Attrs):
		class accesskey(xsc.TextAttr): pass
		class indexed(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class write(xsc.TextAttr): pass


class html(Element):
	"""
	Render a HTML html element
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(Element.Attrs):
		class locale(xsc.TextAttr): pass
		class xhtml(xsc.TextAttr): pass


class image(MouseElement):
	"""
	image input
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(MouseElement.Attrs):
		class align(xsc.TextAttr): pass
		class border(xsc.TextAttr): pass
		class bundle(xsc.TextAttr): pass
		class indexed(xsc.TextAttr): pass
		class locale(xsc.TextAttr): pass
		class page(xsc.TextAttr): pass
		class pageKey(xsc.TextAttr): pass
		class src(xsc.TextAttr): pass
		class srcKey(xsc.TextAttr): pass


class img(Element):
	"""
	html img tag
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(Element.Attrs):
		class align(xsc.TextAttr): pass
		class alt(xsc.TextAttr): pass
		class altKey(xsc.TextAttr): pass
		class border(xsc.TextAttr): pass
		class bundle(xsc.TextAttr): pass
		class height(xsc.TextAttr): pass
		class hspace(xsc.TextAttr): pass
		class imageName(xsc.TextAttr): pass
		class ismap(xsc.TextAttr): pass
		class locale(xsc.TextAttr): pass
		class lowsrc(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class onclick(xsc.TextAttr): pass
		class ondblclick(xsc.TextAttr): pass
		class onkeydown(xsc.TextAttr): pass
		class onkeypress(xsc.TextAttr): pass
		class onkeyup(xsc.TextAttr): pass
		class onmousedown(xsc.TextAttr): pass
		class onmousemove(xsc.TextAttr): pass
		class onmouseout(xsc.TextAttr): pass
		class onmouseover(xsc.TextAttr): pass
		class onmouseup(xsc.TextAttr): pass
		class paramId(xsc.TextAttr): pass
		class page(xsc.TextAttr): pass
		class pageKey(xsc.TextAttr): pass
		class paramName(xsc.TextAttr): pass
		class paramProperty(xsc.TextAttr): pass
		class paramScope(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class src(xsc.TextAttr): pass
		class srcKey(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass
		class styleId(xsc.TextAttr): pass
		class title(xsc.TextAttr): pass
		class titleKey(xsc.TextAttr): pass
		class usemap(xsc.TextAttr): pass
		class vspace(xsc.TextAttr): pass
		class width(xsc.TextAttr): pass


class javascript(Element):
	"""
	Render JavaScript validation based on the validation rules loaded by the
	ValidatorPlugIn.
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(Element.Attrs):
		class cdata(xsc.TextAttr): pass
		class dynamicJavascript(xsc.TextAttr): pass
		class formName(xsc.TextAttr): pass
		class method(xsc.TextAttr): pass
		class page(xsc.TextAttr): pass
		class src(xsc.TextAttr): pass
		class staticJavascript(xsc.TextAttr): pass
		class htmlComment(xsc.TextAttr): pass


class link(Element):
	"""
	html link
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(Element.Attrs):
		class accesskey(xsc.TextAttr): pass
		class action(xsc.TextAttr): pass
		class anchor(xsc.TextAttr): pass
		class forward(xsc.TextAttr): pass
		class href(xsc.URLAttr): pass
		class indexed(xsc.TextAttr): pass
		class indexId(xsc.TextAttr): pass
		class linkName(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class onblur(xsc.TextAttr): pass
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
		class page(xsc.TextAttr): pass
		class paramId(xsc.TextAttr): pass
		class paramName(xsc.TextAttr): pass
		class paramProperty(xsc.TextAttr): pass
		class paramScope(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass
		class styleId(xsc.TextAttr): pass
		class tabindex(xsc.TextAttr): pass
		class target(xsc.TextAttr): pass
		class title(xsc.TextAttr): pass
		class titleKey(xsc.TextAttr): pass
		class transaction(xsc.TextAttr): pass


class messages(Element):
	"""
	Conditionally display a set of accumulated messages.
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(Element.Attrs):
		class id(xsc.TextAttr): pass
		class bundle(xsc.TextAttr): pass
		class locale(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class header(xsc.TextAttr): pass
		class footer(xsc.TextAttr): pass
		class message(xsc.TextAttr): pass


class multibox(MouseElement):
	"""
	multiple checkbox element
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(MouseElement.Attrs):
		class name(xsc.TextAttr): pass


class option(Element):
	"""
	option element
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(Element.Attrs):
		class bundle(xsc.TextAttr): pass
		class dir(xsc.TextAttr): pass
		class disabled(xsc.TextAttr): pass
		class filter(xsc.TextAttr): pass
		class lang(xsc.TextAttr): pass
		class key(xsc.TextAttr): pass
		class locale(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleId(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass


class options(Element):
	"""
	struts html options element
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(Element.Attrs):
		class collection(xsc.TextAttr): pass
		class filter(xsc.TextAttr): pass
		class labelName(xsc.TextAttr): pass
		class labelProperty(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass


class optionsCollection(Element):
	"""
	Render a collection of select options
	"""
	xmlns = xmlns
	model = sims.Empty()
	class Attrs(Element.Attrs):
		class filter(xsc.TextAttr): pass
		class label(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class style(xsc.TextAttr): pass
		class styleClass(xsc.TextAttr): pass
		class value(xsc.TextAttr): pass


class password(MouseElement):
	"""
	a password text input field
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(MouseElement.Attrs):
		class indexed(xsc.TextAttr): pass
		class maxlength(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class readonly(xsc.TextAttr): pass
		class redisplay(xsc.TextAttr): pass
		class size(xsc.TextAttr): pass


class radio(MouseElement):
	"""
	html input radio
	"""
	xmlns = xmlns
	class Attrs(MouseElement.Attrs):
		class indexed(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class idName(xsc.TextAttr): pass


class reset(MouseElement):
	"""
	a reset button
	"""
	xmlns = xmlns
	model = sims.Any()


class rewrite(Element):
	"""
	render a request uri like html link
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(Element.Attrs):
		class anchor(xsc.TextAttr): pass
		class forward(xsc.TextAttr): pass
		class href(xsc.URLAttr): pass
		class name(xsc.TextAttr): pass
		class page(xsc.TextAttr): pass
		class paramId(xsc.TextAttr): pass
		class paramName(xsc.TextAttr): pass
		class paramProperty(xsc.TextAttr): pass
		class paramScope(xsc.TextAttr): pass
		class property(xsc.TextAttr): pass
		class scope(xsc.TextAttr): pass
		class transaction(xsc.TextAttr): pass


class select(PartMouseElement):
	"""
	a select element text input field
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(PartMouseElement.Attrs):
		class disabled(xsc.TextAttr): pass
		class indexed(xsc.TextAttr): pass
		class multiple(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class tabindex(xsc.TextAttr): pass
		class size(xsc.TextAttr): pass


class submit(MouseElement):
	"""
	a submit button
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(MouseElement.Attrs):
		class indexed(xsc.TextAttr): pass


class text(MouseElement):
	"""
	a text input field
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(MouseElement.Attrs):
		class indexed(xsc.TextAttr): pass
		class maxlength(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class readonly(xsc.TextAttr): pass
		class size(xsc.TextAttr): pass


class textarea(MouseElement):
	"""
	a textarea
	"""
	xmlns = xmlns
	model = sims.Any()
	class Attrs(MouseElement.Attrs):
		class cols(xsc.TextAttr): pass
		class indexed(xsc.TextAttr): pass
		class name(xsc.TextAttr): pass
		class readonly(xsc.TextAttr): pass
		class rows(xsc.TextAttr): pass


class xhtml(Element):
	"""
	Render HTML tags as XHTML
	"""
	xmlns = xmlns
	model = sims.Empty()
