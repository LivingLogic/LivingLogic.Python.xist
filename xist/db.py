#! /usr/bin/env python

"""
A XSC module that contains elements that are useful for incorparating
database content into XSC pages.
"""

__version__ = "$Revision$"
# $Source$

import sys
import string
import xsc
import html
import specials

retrievedb = 0 # should database content be retrieved?

def _getDB(element):
	if element.has_attr("module") and element.has_attr("variable"): # database connection via an existing one
		module = str(element["module"])
		variable = str(element["variable"])
		return sys.modules[module].__dict__[variable]
	else: # create our own connection
		api = str(element["api"])

		args = {}
		if element.has_attr("dbname"):
			args["dbname"] = str(element["dbname"])
		if element.has_attr("host"):
			args["host"] = str(element["host"])
		if element.has_attr("port"):
			args["port"] = eval(str(element["port"]))

		__import__(api)
		return apply(sys.modules[api].connect,(),args)

_connectionAttrs = { "module" : xsc.TextAttr , "variable" : xsc.TextAttr , "api" : xsc.TextAttr , "dbname" : xsc.TextAttr , "host" : xsc.TextAttr , "port" : xsc.TextAttr }

class control(xsc.Element):
	"""
	base element for all controls that display database content.
	the attribute name is the fieldname and value is the fieldvalue.

	This class in itself has no use, i.e. it should be considered abstract.

	control and all derived elements implement no asHTML(), but do their
	conversion to HTML in the __str__ function, because otherwise they
	would all have to be directly in the target element, an can't be embedded
	into other element, because then the template wouldn't be able to find
	them.

	With this version, the template can convert the target to HTML first,
	and then fill the controls with data.
	"""
	emtpy = 1
	attrHandlers = { "name" : xsc.TextAttr , "value" : xsc.TextAttr }

	def __str__(self):
		return ""
xsc.registerElement(control)

class lookupcombobox(control):
	attrHandlers = xsc.appendDict(control.attrHandlers,{ "module" : xsc.TextAttr , "variable" : xsc.TextAttr , "query" : xsc.TextAttr , "displayfield" : xsc.TextAttr , "valuefield" : xsc.TextAttr })

	def __str__(self):
		e = html.select(name = self["name"])

		if retrievedb:
			db = _getDB(self)
			query = db.query(str(self["query"]))
			displayfield = str(self["displayfield"].asHTML())
			valuefield = str(self["valuefield"].asHTML())
			for tuple in query.dictresult():
				value = str(tuple[valuefield])
				o = html.option(tuple[displayfield],value = value)
				if self.has_attr("value") and str(self["value"]) == value:
					o["selected"] = None
				e.append(o)
		else:
			e = html.select(name = self["name"])
			e.append(html.option("dummy"))
		return str(e.asHTML())
xsc.registerElement(lookupcombobox)

class checkbox(control):
	def __str__(self):
		e = html.input()
		for attr in self.attrs.keys():
			e[attr] = self[attr]
		e["type"] = "checkbox"
		if self.has_attr("value") and string.atoi(str(self["value"])) != 0:
			e["checked"] = None
		else:
			del e["checked"]
		return str(e.asHTML())


class edit(control):
	attrHandlers = xsc.appendDict(control.attrHandlers,{ "size" : xsc.TextAttr })

	def __str__(self):
		e = html.input()
		for attr in self.attrs.keys():
			e[attr] = self[attr]

		return str(e.asHTML())
xsc.registerElement(edit)

class memo(control):
	attrHandlers = xsc.appendDict(control.attrHandlers,html.textarea.attrHandlers)

	def __str__(self):
		e = html.textarea()
		if self.has_attr("value"):
			e.append(self["value"])
		for attr in self.attrs.keys():
			if attr != "value":
				e[attr] = self[attr]

		return str(e.asHTML())
xsc.registerElement(memo)

class static(control):
	def asPlainString(self):
		if self.has_attr("value"):
			return self["value"].asPlainString()
		else:
			return ""

	def __str__(self):
		if self.has_attr("value"):
			e = self["value"].content
		else:
			e = specials.nbsp()

		return str(e.asHTML())
xsc.registerElement(static)

class hidden(control):
	def __str__(self):
		e = html.input(type="hidden",name=self["name"])
		if self.has_attr("value"):
			e["value"] = self["value"]

		return str(e.asHTML())
xsc.registerElement(hidden)

class target(xsc.Element):
	empty = 0

	def asHTML(self):
		return self.content.asHTML()
xsc.registerElement(target)

class template(xsc.Element):
	empty = 0
	attrHandlers = xsc.appendDict(_connectionAttrs,{ "query" : xsc.TextAttr })

	def asHTML(self):
		content = self.content.clone()

		targets = content.elements(element = target,children = 1,attrs = 1)

		tt = targets[0].clone() # make a copy of the target before we remove its content
		del targets[0][:] # make the target empty (we'll put our data in there later)

		if retrievedb:
			db = _getDB(self)
			query = db.query(str(self["query"].asHTML()))

			for record in query.dictresult():
				t = tt.asHTML() # make a new target, because we'll put the data in there
				for field in t.elements(element = control,subtype = 1,children = 1,attrs = 1): # iterate over all database elements in the target
					field["value"] = str(record[str(field["name"].asHTML())]) # put the field values in
				targets[0].append(t)
		else:
			t = tt.asHTML() # make a new target, because we'll put the data in there
			for field in t.elements(element = control,subtype = 1,children = 1,attrs = 1): # iterate over all database elements in the target
				field["value"] = "dummy" # put dummy field values in
			targets[0].append(t)
		return content.asHTML()
xsc.registerElement(template)

if __name__ == "__main__":
	xsc.make()
