#! /usr/bin/env python

"""
A XSC module that contains elements that are useful for incorparating
database content into XSC pages.
"""

__version__ = "$Revision$"
# $Source$

import xsc
import specials

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
xsc.registerElement("element",element)

class lookupcombobox(element):
	attr_handlers = xsc.appendDict(element.attr_handlers,{ "db" : xsc.TextAttr , "query" : xsc.TextAttr , "displayfield" : xsc.TextAttr , "valuefield" : xsc.TextAttr })

	def asHTML(self):
		e = select(name = self["name"])

		db = eval(str(self["db"]))
		query = db.query(str(self["query"]))
		displayfield = str(self["displayfield"].asHTML())
		valuefield = str(self["valuefield"].asHTML())
		for tuple in query.dictresult():
			value = str(tuple[valuefield])
			o = option(tuple[displayfield],value = value)
			if self.has_attr("value") and str(self["value"]) == value:
				o["selected"] = None
			e.append(o)
		return e.asHTML()
xsc.registerElement("lookupcombobox",lookupcombobox)

class edit(element):
	attr_handlers = xsc.appendDict(element.attr_handlers,{ "size" : xsc.TextAttr })

	def asHTML(self):
		e = input()
		for attr in self.attrs.keys():
			e[attr] = self[attr]

		return e.asHTML()
xsc.registerElement("edit",edit)

class static(element):
	def asHTML(self):
		if self.has_attr("value"):
			e = self["value"].content
		else:
			e = nbsp()

		return e.asHTML()
xsc.registerElement("static",static)

class hidden(element):
	def asHTML(self):
		e = input(type="hidden",name=self["name"])
		if self.has_attr("value"):
			e["value"] = self["value"]

		return e.asHTML()
xsc.registerElement("hidden",hidden)

class target(xsc.Element):
	empty = 0

	def asHTML(self):
		return self.content.asHTML()
xsc.registerElement("target",target)

class template(xsc.Element):
	empty = 0
	attr_handlers = { "db" : xsc.TextAttr , "query" : xsc.TextAttr }

	def asHTML(self):
		db = eval(str(self["db"]))
		query = db.query(str(self["query"]))

		content = self.content.clone()

		targets = content.allElementsNamed(target)

		targettemplate = targets[0].clone() # make a copy of the target before we remove its content
		del targets[0][:] # make the target empty (we'll put our date in there later)

		for record in query.dictresult():
			target = targettemplate.clone() # make a new target, because we'll put the date in there
			for field in target.allElementsDerivedFrom(element): # iterate over all database elements in the target
				field["value"] = str(record[str(field["name"])]) # put the field values in
			targets[0].append(target)

		return content.asHTML()
xsc.registerElement("template",template)

class table(xsc.Element):
	empty = 0
	attr_handlers = { "db" : xsc.TextAttr , "query" : xsc.TextAttr , "class" : xsc.TextAttr }

	def asHTML(self):
		db = eval(str(self["db"]))
		query = db.query(str(self["query"]))

		e = plaintable()
		if self.has_attr("class"):
			e["class"] = self["class"]

		fields = self.elementsNamed(field)

		headers = tr()
		for field in fields:
			headers.append(th(field["caption"],Class = field["name"]))
		e.append(headers)

		flipflop = "even"
		for tuple in query.dictresult():
			etuple = tr(Class=flipflop)
			for field in fields:
				name = field["name"]
				etuple.append(td(str(tuple[str(name)]),Class=name))
			e.append(etuple)
			if flipflop == "even":
				flipflop = "odd"
			else:
				flipflop = "even"

		return e.asHTML()
xsc.registerElement("table",table)

class edittable(xsc.Element):
	empty = 0
	attr_handlers = { "db" : xsc.TextAttr , "query" : xsc.TextAttr , "class" : xsc.TextAttr , "action" : xsc.URLAttr }

	def asHTML(self):
		db = eval(str(self["db"]))
		query = db.query(str(self["query"]))

		e = specials.plaintable()
		if self.has_attr("class"):
			e["class"] = self["class"]

		fields = self.elementsNamed(field)

		headers = tr()
		for field in fields:
			headers.append(th(field["caption"],Class = field["name"]))
		headers.append(th("Bearbeiten",colspan="2"))
		e.append(headers)

		flipflop = "even"
		for tuple in query.dictresult():
			etuple = tr(Class=flipflop)
			for field in fields:
				name = field["name"]
				control = self.__control(field,str(tuple[str(name)]))
				etuple.append(td(control,Class=name))
			button1 = input(type="submit",value="Übernehmen",name="save")
			etuple.append(td(button1))
			button2 = input(type="submit",value="Löschen",name="delete")
			etuple.append(td(button2))
			e.append(form(etuple,action = self["action"]))
			if flipflop == "even":
				flipflop = "odd"
			else:
				flipflop = "even"

		# row for new record
		etuple = tr(Class=flipflop)
		for field in fields:
			name = field["name"]
			control = self.__control(field)
			etuple.append(td(control,Class=name))
		button = input(type="submit",value="Anlegen",name="new")
		etuple.append(td(button,colspan="2"))

		e.append(form(etuple,action = self["action"]))

		return e.asHTML()

	def __control(self,field,value = None):
		fieldtype = str(field["type"])
		if fieldtype == "edit":
			control = edit(name = field["name"])
			if field.has_attr("size"):
				control["size"] = field["size"]
		elif fieldtype == "lookup":
			control = lookupcombobox(name = field["name"],query = field["lookupquery"],displayfield = field["lookupdisplayfield"],valuefield = field["lookupvaluefield"])
		elif fieldtype == "static":
			control = static(name = field["name"])
		elif fieldtype == "hidden":
			control = hidden(name = field["name"])
		if value is not None:
			control["value"] = value
		return control
		
xsc.registerElement("table",table)

class field(xsc.Element):
	empty = 1
	attr_handlers = { "name" : xsc.TextAttr , "caption" : xsc.TextAttr , "type" : xsc.TextAttr , "size" : xsc.TextAttr , "lookupquery" : xsc.TextAttr , "lookupdisplayfield" : xsc.TextAttr , "lookupvaluefield" : xsc.TextAttr }
xsc.registerElement("field",field)

if __name__ == "__main__":
	xsc.make()
