# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
A module that allows you to embed JSP content as processing instructions.
"""


import cgi # for parse_header

from ll.xist import xsc, sims


__docformat__ = "reStructuredText"


xmlns = "http://java.sun.com/JSP/Page"


class directive(xsc.Element):
	model = sims.Empty()
	register = False # only serves as a base class

	def publish(self, publisher):
		yield publisher.encode(u"<%@ ")
		yield publisher.encode(self._publishname(publisher))
		for part in self.attrs.publish(publisher):
			yield part
		yield publisher.encode(u"%>")


class scriptlet(xsc.ProcInst):
	"""
	Will be published as ``<% content %>``.
	"""

	def publish(self, publisher):
		yield publisher.encode(u"<% ")
		yield publisher.encode(self.content)
		yield publisher.encode(u" %>")


class expression(xsc.ProcInst):
	"""
	Will be published as ``<%= content %>``.
	"""

	def publish(self, publisher):
		yield publisher.encode(u"<%= ")
		yield publisher.encode(self.content)
		yield publisher.encode(u" %>")


class declaration(xsc.ProcInst):
	"""
	Will be published as ``<%! content %>``.
	"""

	def publish(self, publisher):
		yield publisher.encode(u"<%! ")
		yield publisher.encode(self.content)
		yield publisher.encode(u" %>")


class If(scriptlet):
	xmlname = "if"

	def convert(self, converter):
		return scriptlet(u"if(", self.content, u"){")


class Else(scriptlet):
	xmlname = "else"

	def convert(self, converter):
		return scriptlet(u"}else{")


class ElIf(scriptlet):
	xmlname = "elif"

	def convert(self, converter):
		return scriptlet(u"}else if (", self.content, u"){")


class End(scriptlet):
	xmlname = "end"

	def convert(self, converter):
		return scriptlet(u"}")


class block(xsc.Element):
	"""
	This element embeds its content in ``{}`` brackets. Note that the content
	itself will not be turned into a scriptlet automatically but will be used
	as-is.
	"""
	model = sims.Any()

	def convert(self, converter):
		e = xsc.Frag(
			scriptlet(u"{"),
			self.content,
			scriptlet(u"}")
		)
		return e.convert(converter)


class directive_include(directive):
	xmlname = "include"
	class Attrs(directive.Attrs):
		class file(xsc.TextAttr): pass


class directive_taglib(directive):
	xmlname = "taglib"
	class Attrs(directive.Attrs):
		class uri(xsc.TextAttr): pass
		class prefix(xsc.TextAttr): pass


class directive_page(directive):
	xmlname = "page"
	class Attrs(directive.Attrs):
		class language(xsc.TextAttr):
			values = ("java",)
		class extends(xsc.TextAttr): pass
		class import_(xsc.TextAttr): xmlname = "import"
		class session(xsc.TextAttr): values = (u"true", u"false")
		class buffer(xsc.TextAttr): pass
		class autoFlush(xsc.TextAttr): values = (u"true", u"false")
		class isThreadSafe(xsc.TextAttr): values = (u"true", u"false")
		class info(xsc.TextAttr): pass
		class errorPage(xsc.URLAttr): pass
		class contentType(xsc.TextAttr): pass
		class isErrorPage(xsc.TextAttr): values = (u"true", u"false")
		class pageEncoding(xsc.TextAttr): pass

	def publish(self, publisher):
		# Only a contentType attribute triggers the special code
		if u"contentType" in self.attrs and not self.attrs.contentType.isfancy() and not self.attrs.pageEncoding.isfancy():
			(contenttype, options) = cgi.parse_header(unicode(self.attrs.contentType))
			pageencoding = unicode(self.attrs.pageEncoding)
			encoding = publisher.encoding
			if encoding is None:
				encoding = "utf-8"
			if u"charset" not in options or not (options[u"charset"] == pageencoding == encoding):
				options[u"charset"] = encoding
				node = self.__class__(
					self.attrs,
					contentType=(contenttype, u"; ", u"; ".join("%s=%s" % option for option in options.items())),
					pageEncoding=encoding
				)
				return node.publish(publisher) # return a generator-iterator
		return super(directive_page, self).publish(publisher) # return a generator-iterator


def fromul4(template, variables="variables", indent=0):
	"""
	Return the UL4 template :var:`template` as JSP source code. :var:`variables`
	is the variable name of the map object containing the top level variables.
	:var:`indent` is the initial indentation of the source code.

	The code produced requires the `UL4 Java package`__.

	__ http://hg.livinglogic.de/LivingLogic.Java.ul4
	"""
	from ll import ul4c
	from ll.xist.ns import specials

	# Turn a Python string into a Java string literal
	def _string(s):
		v = []
		specialchars = {"\r": "\\r", "\n": "\\n", "\t": "\\t", '"': '\\"'}
		for c in s:
			try:
				v.append(specialchars[c])
			except KeyError:
				oc = ord(c)
				v.append("\\u%04x" % oc if oc >= 128 else c)
		return '"%s"' % "".join(s)

	def make_literal(content):
		result.append(specials.literal(content))

	def make_scriptlet(content):
		line = "%s%s\n" % ("\t"*indent, content)
		if result and isinstance(result[-1], scriptlet):
			result[-1] += "%s%s\n" % ("\t"*indent, content)
		else:
			result.append(scriptlet("\n%s%s\n" % ("\t"*indent, content)))

	varcounter = 0 # Used to number loop iterators and local templates
	result = xsc.Frag()

	make_scriptlet("//@@@ BEGIN template source")

	lines = template.source.splitlines(False)
	width = len(str(len(lines)+1))
	for (i, line) in enumerate(lines):
		make_scriptlet("// %*d %s" % (width, i+1, line))

	make_scriptlet("//@@@ BEGIN template code")

	for i in xrange(10):
		make_scriptlet("Object r%d = null;" % i)

	defs = []
	lastloc = None
	for opcode in template.opcodes:
		if opcode.code is not None and opcode.location is not lastloc:
			lastloc = opcode.location
			(line, col) = lastloc.pos()
			tag = lastloc.tag
			make_scriptlet("// Location %d (line %d, col %d): %s" % (lastloc.starttag+1, line, col, repr(tag)[1+isinstance(tag, unicode):-1]))
		if opcode.code is None:
			make_literal(opcode.location.code)
		elif opcode.code == "loadstr":
			make_scriptlet('r%d = %s;' % (opcode.r1, _string(opcode.arg)))
		elif opcode.code == "loadint":
			make_scriptlet("r%d = new Integer(%s);" % (opcode.r1, opcode.arg))
		elif opcode.code == "loadfloat":
			make_scriptlet("r%d = new Double(%s);" % (opcode.r1, opcode.arg))
		elif opcode.code == "loadnone":
			make_scriptlet("r%d = null;" % opcode.r1)
		elif opcode.code == "loadfalse":
			make_scriptlet("r%d = Boolean.FALSE;" % opcode.r1)
		elif opcode.code == "loadtrue":
			make_scriptlet("r%d = Boolean.TRUE;" % opcode.r1)
		elif opcode.code == "loaddate":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.isoDateFormatter.parse(%s);" % (opcode.r1, _string(opcode.arg)))
		elif opcode.code == "loadcolor":
			make_scriptlet("r%d = new com.livinglogic.ul4.Color(0x%s, 0x%s, 0x%s, 0x%s)" % (opcode.r1, opcode.arg[:2], opcode.arg[2:4], opcode.arg[4:6], opcode.arg[6:]))
		elif opcode.code == "buildlist":
			make_scriptlet("r%d = new java.util.ArrayList();" % opcode.r1)
		elif opcode.code == "builddict":
			make_scriptlet("r%d = new java.util.HashMap();" % opcode.r1)
		elif opcode.code == "addlist":
			make_scriptlet("((java.util.List)r%d).add(r%d);" % (opcode.r1, opcode.r2))
		elif opcode.code == "adddict":
			make_scriptlet("((java.util.Map)r%d).put(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "updatedict":
			make_scriptlet("((java.util.Map)r%d).putAll((java.util.Map)r%d);" % (opcode.r1, opcode.r2))
		elif opcode.code == "loadvar":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.getItem(%s, %s);" % (opcode.r1, variables, _string(opcode.arg)))
		elif opcode.code == "storevar":
			make_scriptlet("%s.put(%s, r%d);" % (variables, _string(opcode.arg), opcode.r1))
		elif opcode.code == "addvar":
			name = _string(opcode.arg)
			make_scriptlet("%s.put(%s, com.livinglogic.ul4.Utils.add(%s.get(%s), r%d));" % (variables, name, variables, name, opcode.r1))
		elif opcode.code == "subvar":
			name = _string(opcode.arg)
			make_scriptlet("%s.put(%s, com.livinglogic.ul4.Utils.sub(%s.get(%s), r%d));" % (variables, name, variables, name, opcode.r1))
		elif opcode.code == "mulvar":
			name = _string(opcode.arg)
			make_scriptlet("%s.put(%s, com.livinglogic.ul4.Utils.mul(%s.get(%s), r%d));" % (variables, name, variables, name, opcode.r1))
		elif opcode.code == "truedivvar":
			name = _string(opcode.arg)
			make_scriptlet("%s.put(%s, com.livinglogic.ul4.Utils.truediv(%s.get(%s), r%d));" % (variables, name, variables, name, opcode.r1))
		elif opcode.code == "floordivvar":
			name = _string(opcode.arg)
			make_scriptlet("%s.put(%s, com.livinglogic.ul4.Utils.floordiv(%s.get(%s), r%d));" % (variables, name, variables, name, opcode.r1))
		elif opcode.code == "modvar":
			name = _string(opcode.arg)
			make_scriptlet("%s.put(%s, com.livinglogic.ul4.Utils.mod(%s.get(%s), r%d));" % (variables, name, variables, name, opcode.r1))
		elif opcode.code == "delvar":
			make_scriptlet("%s.remove(%s);" % (variables, _string(opcode.arg)))
		elif opcode.code == "getattr":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.getItem(r%d, %s);" % (opcode.r1, opcode.r2, _string(opcode.arg)))
		elif opcode.code == "getitem":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.getItem(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "getslice12":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.getSlice(r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
		elif opcode.code == "getslice1":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.getSlice(r%d, r%d, null);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "getslice2":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.getSlice(r%d, null, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "print":
			make_scriptlet("out.write(org.apache.commons.lang.ObjectUtils.toString(r%d));" % opcode.r1)
		elif opcode.code == "printx":
			make_scriptlet("out.write(com.livinglogic.ul4.Utils.xmlescape(org.apache.commons.lang.ObjectUtils.toString(r%d)));" % opcode.r1)
		elif opcode.code == "for":
			varcounter += 1
			make_scriptlet("for (java.util.Iterator iterator%d = com.livinglogic.ul4.Utils.iterator(r%d); iterator%d.hasNext();)" % (varcounter, opcode.r2, varcounter))
			make_scriptlet("{")
			indent += 1
			make_scriptlet("r%d = iterator%d.next();" % (opcode.r1, varcounter))
		elif opcode.code == "endfor":
			indent -= 1
			make_scriptlet("}")
		elif opcode.code == "def":
			varcounter += 1
			make_scriptlet("com.livinglogic.ul4.JSPTemplate template%d = new com.livinglogic.ul4.JSPTemplate()" % varcounter)
			make_scriptlet("{")
			indent += 1
			make_scriptlet("public void execute(java.io.Writer out, Map variables) throws java.io.IOException")
			indent += 1
			make_scriptlet("{")
			indent += 1
			for i in xrange(10):
				make_scriptlet("Object r%d = null;" % i)
			defs.append((opcode.arg, variables))
			variables = "variables"
		elif opcode.code == "enddef":
			indent -= 1
			make_scriptlet("}")
			indent -= 1
			make_scriptlet("};")
			(arg, variables) = defs.pop()
			make_scriptlet("%s.put(%s, template%d);" % (variables, _string(arg), varcounter))
		elif opcode.code == "break":
			make_scriptlet("break;")
		elif opcode.code == "continue":
			make_scriptlet("continue;")
		elif opcode.code == "not":
			make_scriptlet("r%d = !com.livinglogic.ul4.Utils.getBool(r%d);" % (opcode.r1, opcode.r2))
		elif opcode.code == "neg":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.neg(r%d);" % (opcode.r1, opcode.r2))
		elif opcode.code == "contains":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.contains(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "notcontains":
			make_scriptlet("r%d = !com.livinglogic.ul4.Utils.contains(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "eq":
			make_scriptlet("r%d = org.apache.commons.lang.ObjectUtils.equals(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "ne":
			make_scriptlet("r%d = !org.apache.commons.lang.ObjectUtils.equals(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "lt":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.lt(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "le":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.le(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "gt":
			make_scriptlet("r%d = !com.livinglogic.ul4.Utils.le(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "ge":
			make_scriptlet("r%d = !com.livinglogic.ul4.Utils.lt(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "add":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.add(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "sub":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.sub(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "mul":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.mul(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "floordiv":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.floordiv(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "truediv":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.truediv(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "and":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.getBool(r%d) ? r%d : r%d;" % (opcode.r1, opcode.r3, opcode.r2, opcode.r3))
		elif opcode.code == "or":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.getBool(r%d) ? r%d : r%d;" % (opcode.r1, opcode.r2, opcode.r2, opcode.r3))
		elif opcode.code == "mod":
			make_scriptlet("r%d = com.livinglogic.ul4.Utils.mod(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
		elif opcode.code == "callfunc0":
			if opcode.arg == "now":
				make_scriptlet("r%d = new java.util.Date();" % opcode.r1)
			elif opcode.arg == "vars":
				make_scriptlet("r%d = %s;" % (opcode.r1, variables))
			else:
				raise ul4c.UnknownFunctionError(opcode.arg)
		elif opcode.code == "callfunc1":
			if opcode.arg == "xmlescape":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.xmlescape(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "csv":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.csv(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "str":
				make_scriptlet("r%d = org.apache.commons.lang.ObjectUtils.toString(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "repr":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.repr(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "int":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.toInteger(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "float":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.toFloat(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "bool":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.getBool(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "len":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.length(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "enumerate":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.enumerate(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "isnone":
				make_scriptlet("r%d = (r%d == null);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "isstr":
				make_scriptlet("r%d = ((r%d != null) && (r%d instanceof String));" % (opcode.r1, opcode.r2, opcode.r2))
			elif opcode.arg == "isint":
				make_scriptlet("r%d = ((r%d != null) && (r%d instanceof Integer));" % (opcode.r1, opcode.r2, opcode.r2))
			elif opcode.arg == "isfloat":
				make_scriptlet("r%d = ((r%d != null) && (r%d instanceof Double));" % (opcode.r1, opcode.r2, opcode.r2))
			elif opcode.arg == "isbool":
				make_scriptlet("r%d = ((r%d != null) && (r%d instanceof Boolean));" % (opcode.r1, opcode.r2, opcode.r2))
			elif opcode.arg == "isdate":
				make_scriptlet("r%d = ((r%d != null) && (r%d instanceof java.util.Date));" % (opcode.r1, opcode.r2, opcode.r2))
			elif opcode.arg == "islist":
				make_scriptlet("r%d = ((r%d != null) && (r%d instanceof java.util.List));" % (opcode.r1, opcode.r2, opcode.r2))
			elif opcode.arg == "isdict":
				make_scriptlet("r%d = ((r%d != null) && (r%d instanceof java.util.Map));" % (opcode.r1, opcode.r2, opcode.r2))
			elif opcode.arg == "istemplate":
				make_scriptlet("r%d = ((r%d != null) && (r%d instanceof com.livinglogic.ul4.Template));" % (opcode.r1, opcode.r2, opcode.r2))
			elif opcode.arg == "iscolor":
				make_scriptlet("r%d = ((r%d != null) && (r%d instanceof com.livinglogic.ul4.Color));" % (opcode.r1, opcode.r2, opcode.r2))
			elif opcode.arg == "chr":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.chr(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "ord":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.ord(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "hex":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.hex(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "oct":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.oct(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "bin":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.bin(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "sorted":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.sorted(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "range":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.range(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "type":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.type(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "get":
				make_scriptlet("r%d = %s.get(r%d);" % (opcode.r1, variables, opcode.r2))
			elif opcode.arg == "json":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.json(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "reversed":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.reversed(r%d);" % (opcode.r1, opcode.r2))
			else:
				raise ul4c.UnknownFunctionError(opcode.arg)
		elif opcode.code == "callfunc2":
			if opcode.arg == "range":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.range(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "get":
				make_scriptlet("r%d = %s.containsKey(r%d) ? %s.get(r%d) : r%d;" % (opcode.r1, variables, opcode.r2, variables, opcode.r2, opcode.r3))
			elif opcode.arg == "zip":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.zip(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			else:
				raise ul4c.UnknownFunctionError(opcode.arg)
		elif opcode.code == "callfunc3":
			if opcode.arg == "range":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.range(r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
			elif opcode.arg == "zip":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.zip(r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
			elif opcode.arg == "rgb":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.rgb(r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
			elif opcode.arg == "hls":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.hls(r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
			elif opcode.arg == "hsv":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.hsv(r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
			else:
				raise ul4c.UnknownFunctionError(opcode.arg)
		elif opcode.code == "callfunc4":
			if opcode.arg == "rgb":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.rgb(r%d, r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4, opcode.r5))
			elif opcode.arg == "hls":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.hls(r%d, r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4, opcode.r5))
			elif opcode.arg == "hsv":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.hsv(r%d, r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4, opcode.r5))
			else:
				raise ul4c.UnknownFunctionError(opcode.arg)
		elif opcode.code == "callmeth0":
			if opcode.arg == "split":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.split(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "strip":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.strip(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "lstrip":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.lstrip(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "rstrip":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.rstrip(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "upper":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.upper(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "lower":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.lower(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "capitalize":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.capitalize(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "items":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.items(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "isoformat":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.isoformat(r%d);" % (opcode.r1, opcode.r2))
			elif opcode.arg == "r":
				make_scriptlet("r%d = ((com.livinglogic.ul4.Color)r%d).r();" % (opcode.r1, opcode.r2))
			elif opcode.arg == "g":
				make_scriptlet("r%d = ((com.livinglogic.ul4.Color)r%d).g();" % (opcode.r1, opcode.r2))
			elif opcode.arg == "b":
				make_scriptlet("r%d = ((com.livinglogic.ul4.Color)r%d).b();" % (opcode.r1, opcode.r2))
			elif opcode.arg == "a":
				make_scriptlet("r%d = ((com.livinglogic.ul4.Color)r%d).a();" % (opcode.r1, opcode.r2))
			elif opcode.arg == "hls":
				make_scriptlet("r%d = ((com.livinglogic.ul4.Color)r%d).hls();" % (opcode.r1, opcode.r2))
			elif opcode.arg == "hlsa":
				make_scriptlet("r%d = ((com.livinglogic.ul4.Color)r%d).hlsa();" % (opcode.r1, opcode.r2))
			elif opcode.arg == "hsv":
				make_scriptlet("r%d = ((com.livinglogic.ul4.Color)r%d).hsv();" % (opcode.r1, opcode.r2))
			elif opcode.arg == "hsva":
				make_scriptlet("r%d = ((com.livinglogic.ul4.Color)r%d).hsva();" % (opcode.r1, opcode.r2))
			elif opcode.arg == "lum":
				make_scriptlet("r%d = new Double(((com.livinglogic.ul4.Color)r%d).lum());" % (opcode.r1, opcode.r2))
			else:
				raise ul4c.UnknownMethodError(opcode.arg)
		elif opcode.code == "callmeth1":
			if opcode.arg == "split":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.split(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "rsplit":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.rsplit(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "strip":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.strip(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "lstrip":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.lstrip(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "rstrip":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.rstrip(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "startswith":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.startswith(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "endswith":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.endswith(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "find":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.find(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "rfind":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.rfind(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "format":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.format(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "get":
				make_scriptlet("r%d = ((java.util.Map)r%d).get(r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "withlum":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.withlum(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			elif opcode.arg == "witha":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.witha(r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			else:
				raise ul4c.UnknownMethodError(opcode.arg)
		elif opcode.code == "callmeth2":
			if opcode.arg == "split":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.split(r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
			elif opcode.arg == "rsplit":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.rsplit(r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
			elif opcode.arg == "find":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.find(r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
			elif opcode.arg == "replace":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.replace(r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
			elif opcode.arg == "get":
				make_scriptlet("r%d = ((java.util.Map)r%d).containsKey(r%d) ? ((java.util.Map)r%d).get(r%d) : r%d;" % (opcode.r1, opcode.r2, opcode.r3, opcode.r2, opcode.r3, opcode.r4))
			else:
				raise ul4c.UnknownMethodError(opcode.arg)
		elif opcode.code == "callmeth3":
			if opcode.arg == "find":
				make_scriptlet("r%d = com.livinglogic.ul4.Utils.find(r%d, r%d, r%d, r%d);" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4, opcode.r5))
			else:
				raise ul4c.UnknownMethodError(opcode.arg)
		elif opcode.code == "callmethkw":
			if opcode.arg == "render":
				make_scriptlet("r%d = ((com.livinglogic.ul4.Template)r%d).renders((java.util.Map)r%d);" % (opcode.r1, opcode.r2, opcode.r3))
			else:
				raise ul4c.UnknownMethodError(opcode.arg)
		elif opcode.code == "if":
			make_scriptlet("if (com.livinglogic.ul4.Utils.getBool(r%d))" % opcode.r1)
			make_scriptlet("{")
			indent += 1
		elif opcode.code == "else":
			indent -= 1
			make_scriptlet("}")
			make_scriptlet("else")
			make_scriptlet("{")
			indent += 1
		elif opcode.code == "endif":
			indent -= 1
			make_scriptlet("}")
		elif opcode.code == "render":
			make_scriptlet("((com.livinglogic.ul4.Template)r%d).renderjsp(out, (Map)r%d);" % (opcode.r1, opcode.r2))
		else:
			raise ul4c.UnknownOpcodeError(opcode.code)
	make_scriptlet("//@@@ END template code")
	return result
