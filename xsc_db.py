#! /usr/bin/env python

""""""

__version__ = "$Revision$"
# $Source$

class dbelement(XSCElement):
	"""
	base element for all elements that display database content.
	the attribute name is the fieldname and value is the fieldvalue.

	This class in itself has no use, i.e. it should be considered abstract.
	"""
	emtpy = 1
	attr_handlers = { "name" : XSCTextAttr , "value" : XSCTextAttr }

	def asHTML(self):
		return None
RegisterElement("dbelement",dbelement)

class dblookupcombobox(dbelement):
	attr_handlers = AppendDict(dbelement.attr_handlers,{ "query" : XSCTextAttr , "displayfield" : XSCTextAttr , "valuefield" : XSCTextAttr })

	def asHTML(self):
		e = select(name = self["name"])

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
RegisterElement("dblookupcombobox",dblookupcombobox)

class dbedit(dbelement):
	attr_handlers = AppendDict(dbelement.attr_handlers,{ "size" : XSCTextAttr })

	def asHTML(self):
		e = input()
		for attr in self.attrs.keys():
			e[attr] = self[attr]

		return e.asHTML()
RegisterElement("dbedit",dbedit)

class dbstatic(dbelement):
	def asHTML(self):
		if self.has_attr("value"):
			e = self["value"].content
		else:
			e = nbsp()

		return e.asHTML()
RegisterElement("dbstatic",dbstatic)

class dbhidden(dbelement):
	def asHTML(self):
		e = input(type="hidden",name=self["name"])
		if self.has_attr("value"):
			e["value"] = self["value"]

		return e.asHTML()
RegisterElement("dbhidden",dbhidden)

class dbtarget(XSCElement):
	empty = 0

	def asHTML(self):
		return self.content.asHTML()
RegisterElement("dbtarget",dbtarget)

class dbtemplate(XSCElement):
	empty = 0
	attr_handlers = { "query" : XSCTextAttr }

	def asHTML(self):
		query = db.query(str(self["query"]))

		content = self.content.clone()

		targets = content.allElementsNamed(dbtarget)

		targettemplate = targets[0].clone() # make a copy of the target before we remove its content
		del targets[0][:] # make the target empty (we'll put our date in there later)

		for record in query.dictresult():
			target = targettemplate.clone() # make a new target, because we'll put the date in there
			for field in target.allElementsDerivedFrom(dbelement): # iterate over all database elements in the target
				field["value"] = str(record[str(field["name"])]) # put the field values in
			targets[0].append(target)

		return content.asHTML()
RegisterElement("dbtemplate",dbtemplate)

class dbtable(XSCElement):
	empty = 0
	attr_handlers = { "query" : XSCTextAttr , "class" : XSCTextAttr }

	def asHTML(self):
		e = plaintable()
		if self.has_attr("class"):
			e["class"] = self["class"]

		query = db.query(str(self["query"]))
		fields = self.elementsNamed(dbfield)

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
RegisterElement("dbtable",dbtable)

class dbedittable(XSCElement):
	empty = 0
	attr_handlers = { "query" : XSCTextAttr , "class" : XSCTextAttr , "action" : XSCURLAttr }

	def asHTML(self):
		e = plaintable()
		if self.has_attr("class"):
			e["class"] = self["class"]

		query = db.query(str(self["query"]))
		fields = self.elementsNamed(dbfield)

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
			control = dbedit(name = field["name"])
			if field.has_attr("size"):
				control["size"] = field["size"]
		elif fieldtype == "lookup":
			control = dblookupcombobox(name = field["name"],query = field["lookupquery"],displayfield = field["lookupdisplayfield"],valuefield = field["lookupvaluefield"])
		elif fieldtype == "static":
			control = dbstatic(name = field["name"])
		elif fieldtype == "hidden":
			control = dbhidden(name = field["name"])
		if value is not None:
			control["value"] = value
		return control
		
RegisterElement("dbtable",dbtable)

class dbfield(XSCElement):
	empty = 1
	attr_handlers = { "name" : XSCTextAttr , "caption" : XSCTextAttr , "type" : XSCTextAttr , "size" : XSCTextAttr , "lookupquery" : XSCTextAttr , "lookupdisplayfield" : XSCTextAttr , "lookupvaluefield" : XSCTextAttr }
RegisterElement("dbfield",dbfield)


