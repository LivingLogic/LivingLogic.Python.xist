#! /usr/bin/env python

"""
A XSC module that contains elements that are useful for incorparating
database content into XSC pages.
"""

__version__ = "$Revision$"
# $Source$

import sys
import xsc
import html
import specials

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

class element(xsc.Element):
	"""
	base element for all elements that display database content.
	the attribute name is the fieldname and value is the fieldvalue.

	This class in itself has no use, i.e. it should be considered abstract.
	"""
	emtpy = 1
	attr_handlers = { "name" : xsc.TextAttr , "value" : xsc.TextAttr }

	def asHTML(self):
		return None
xsc.registerElement(element)

class lookupcombobox(element):
	attr_handlers = xsc.appendDict(element.attr_handlers,{ "module" : xsc.TextAttr , "variable" : xsc.TextAttr , "query" : xsc.TextAttr , "displayfield" : xsc.TextAttr , "valuefield" : xsc.TextAttr })

	def asHTML(self):
		db = _getDB(self)
		query = db.query(str(self["query"]))

		e = select(name = self["name"])

		displayfield = str(self["displayfield"].asHTML())
		valuefield = str(self["valuefield"].asHTML())
		for tuple in query.dictresult():
			value = str(tuple[valuefield])
			o = option(tuple[displayfield],value = value)
			if self.has_attr("value") and str(self["value"]) == value:
				o["selected"] = None
			e.append(o)
		return e.asHTML()
xsc.registerElement(lookupcombobox)

class edit(element):
	attr_handlers = xsc.appendDict(element.attr_handlers,{ "size" : xsc.TextAttr })

	def asHTML(self):
		e = html.input()
		for attr in self.attrs.keys():
			e[attr] = self[attr]

		return e.asHTML()
xsc.registerElement(edit)

class memo(element):
	attr_handlers = xsc.appendDict(element.attr_handlers,html.textarea.attr_handlers }

	def asHTML(self):
		e = html.textarea()
		if self.has_attr("value"):
			e.append(self["value"])
		for attr in self.attrs.keys():
			if attr != "value":
				e[attr] = self[attr]

		return e.asHTML()
xsc.registerElement(memo)

class static(element):
	def asHTML(self):
		if self.has_attr("value"):
			e = self["value"].content
		else:
			e = specials.nbsp()

		return e.asHTML()
xsc.registerElement(static)

class hidden(element):
	def asHTML(self):
		e = html.input(type="hidden",name=self["name"])
		if self.has_attr("value"):
			e["value"] = self["value"]

		return e.asHTML()
xsc.registerElement(hidden)

class target(xsc.Element):
	empty = 0

	def asHTML(self):
		return self.content.asHTML()
xsc.registerElement(target)

class template(xsc.Element):
	empty = 0
	attr_handlers = xsc.appendDict(_connectionAttrs,{ "query" : xsc.TextAttr })

	def asHTML(self):
		db = _getDB(self)
		query = db.query(str(self["query"].asHTML()))

		content = self.content.clone()

		targets = content.elements(element = target,children = 1,attrs = 1)

		tt = targets[0].clone() # make a copy of the target before we remove its content
		del targets[0][:] # make the target empty (we'll put our data in there later)

		for record in query.dictresult():
			t = tt.clone() # make a new target, because we'll put the data in there
			for field in t.elements(element = element,subtype = 1,children = 1,attrs = 1): # iterate over all database elements in the target
				field["value"] = str(record[str(field["name"].asHTML())]) # put the field values in
			targets[0].append(t)

		return content.asHTML()
xsc.registerElement(template)

if __name__ == "__main__":
	xsc.make()
