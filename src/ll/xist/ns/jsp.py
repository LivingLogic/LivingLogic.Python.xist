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
					contentType=(contenttype, u"; ", u"; ".join("{}={}".format(*option) for option in options.items())),
					pageEncoding=encoding
				)
				return node.publish(publisher) # return a generator-iterator
		return super(directive_page, self).publish(publisher) # return a generator-iterator


def javastring(s):
	"""
	Return a Java string literal for the string :var:`s`.
	"""
	v = []
	specialchars = {u"\r": u"\\r", u"\n": u"\\n", u"\t": u"\\t", u'"': u'\\"'}
	for c in s:
		try:
			v.append(specialchars[c])
		except KeyError:
			oc = ord(c)
			v.append(u"\\u{:04x}".format(oc) if oc >= 128 else c)
	return u'"{}"'.format(u"".join(v))


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

	def make_literal(content):
		result.append(specials.literal(content))

	def make_scriptlet(content):
		if result and isinstance(result[-1], scriptlet):
			result[-1] += u"{}{}\n".format(u"\t"*indent, content)
		else:
			result.append(scriptlet(u"\n{}{}\n".format(u"\t"*indent, content)))

	varcounter = 0 # Used to number loop iterators and local templates
	result = xsc.Frag()

	make_scriptlet(u"//@@@ BEGIN template source")

	lines = template.source.splitlines(False)
	width = len(str(len(lines)+1))
	for (i, line) in enumerate(lines):
		make_scriptlet(u"// {1:{0}} {2}".format(width, i+1, line))

	make_scriptlet(u"//@@@ BEGIN template code")

	for i in xrange(10):
		make_scriptlet(u"Object r{} = null;".format(i))

	defs = []
	lastloc = None
	for opcode in template.opcodes:
		if opcode.code is not None and opcode.location is not lastloc:
			lastloc = opcode.location
			(line, col) = lastloc.pos()
			tag = lastloc.tag
			make_scriptlet(u"// Location {} (line {}, col {}): {}".format(lastloc.starttag+1, line, col, repr(tag)[1+isinstance(tag, unicode):-1]))
		if opcode.code is None:
			make_literal(opcode.location.code)
		elif opcode.code == "loadstr":
			make_scriptlet(u'r{op.r1} = {arg};'.format(op=opcode, arg=javastring(opcode.arg)))
		elif opcode.code == "loadint":
			make_scriptlet(u"r{op.r1} = new Integer({op.arg});".format(op=opcode))
		elif opcode.code == "loadfloat":
			make_scriptlet(u"r{op.r1} = new Double({op.arg});".format(op=opcode))
		elif opcode.code == "loadnone":
			make_scriptlet(u"r{op.r1} = null;".format(op=opcode))
		elif opcode.code == "loadfalse":
			make_scriptlet(u"r{op.r1} = Boolean.FALSE;".format(op=opcode))
		elif opcode.code == "loadtrue":
			make_scriptlet(u"r{op.r1} = Boolean.TRUE;".format(op=opcode))
		elif opcode.code == "loaddate":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.isoDateFormatter.parse({arg});".format(op=opcode, arg=javastring(opcode.arg)))
		elif opcode.code == "loadcolor":
			make_scriptlet(u"r{op.r1} = new com.livinglogic.ul4.Color(0x{r}, 0x{g}, 0x{b}, 0x{a})".format(op=opcode, r=opcode.arg[:2], g=opcode.arg[2:4], b=opcode.arg[4:6], a=opcode.arg[6:]))
		elif opcode.code == "buildlist":
			make_scriptlet(u"r{op.r1} = new java.util.ArrayList();".format(op=opcode))
		elif opcode.code == "builddict":
			make_scriptlet(u"r{op.r1} = new java.util.HashMap();".format(op=opcode))
		elif opcode.code == "addlist":
			make_scriptlet(u"((java.util.List)r{op.r1}).add(r{op.r2});".format(op=opcode))
		elif opcode.code == "adddict":
			make_scriptlet(u"((java.util.Map)r{op.r1}).put(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "updatedict":
			make_scriptlet(u"((java.util.Map)r{op.r1}).putAll((java.util.Map)r{op.r2});".format(op=opcode))
		elif opcode.code == "loadvar":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.getItem({var}, {arg});".format(op=opcode, var=variables, arg=javastring(opcode.arg)))
		elif opcode.code == "storevar":
			make_scriptlet(u"{var}.put({arg}, r{op.r1});".format(var=variables, arg=javastring(opcode.arg), op=opcode))
		elif opcode.code == "addvar":
			make_scriptlet(u"{var}.put({arg}, com.livinglogic.ul4.Utils.add({var}.get({arg}), r{op.r1}));".format(var=variables, arg=javastring(opcode.arg), op=opcode))
		elif opcode.code == "subvar":
			make_scriptlet(u"{var}.put({arg}, com.livinglogic.ul4.Utils.sub({var}.get({arg}), r{op.r1}));".format(var=variables, arg=javastring(opcode.arg), op=opcode))
		elif opcode.code == "mulvar":
			make_scriptlet(u"{var}.put({arg}, com.livinglogic.ul4.Utils.mul({var}.get({arg}), r{op.r1}));".format(var=variables, arg=javastring(opcode.arg), op=opcode))
		elif opcode.code == "truedivvar":
			make_scriptlet(u"{var}.put({arg}, com.livinglogic.ul4.Utils.truediv({var}.get({arg}), r{op.r1}));".format(var=variables, arg=javastring(opcode.arg), op=opcode))
		elif opcode.code == "floordivvar":
			name = javastring(opcode.arg)
			make_scriptlet(u"{var}.put({arg}, com.livinglogic.ul4.Utils.floordiv({var}.get({arg}), r{op.r1}));".format(var=variables, arg=javastring(opcode.arg), op=opcode))
		elif opcode.code == "modvar":
			make_scriptlet(u"{var}.put({arg}, com.livinglogic.ul4.Utils.mod({var}.get({arg}), r{op.r1}));".format(var=variables, arg=javastring(opcode.arg), op=opcode))
		elif opcode.code == "delvar":
			make_scriptlet(u"{var}.remove({arg});".format(var=variables, arg=javastring(opcode.arg)))
		elif opcode.code == "getattr":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.getItem(r{op.r2}, {arg});".format(op=opcode, arg=javastring(opcode.arg)))
		elif opcode.code == "getitem":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.getItem(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "getslice12":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.getSlice(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
		elif opcode.code == "getslice1":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.getSlice(r{op.r2}, r{op.r3}, null);".format(op=opcode))
		elif opcode.code == "getslice2":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.getSlice(r{op.r2}, null, r{op.r3});".format(op=opcode))
		elif opcode.code == "print":
			make_scriptlet(u"out.write(org.apache.commons.lang.ObjectUtils.toString(r{op.r1}));".format(op=opcode))
		elif opcode.code == "printx":
			make_scriptlet(u"out.write(com.livinglogic.ul4.Utils.xmlescape(r{op.r1}));".format(op=opcode))
		elif opcode.code == "for":
			varcounter += 1
			make_scriptlet(u"for (java.util.Iterator iterator{count} = com.livinglogic.ul4.Utils.iterator(r{op.r2}); iterator{count}.hasNext();)".format(op=opcode, count=varcounter))
			make_scriptlet(u"{")
			indent += 1
			make_scriptlet(u"r{op.r1} = iterator{count}.next();".format(op=opcode, count=varcounter))
		elif opcode.code == "endfor":
			indent -= 1
			make_scriptlet(u"}")
		elif opcode.code == "def":
			varcounter += 1
			make_scriptlet(u"com.livinglogic.ul4.JSPTemplate template{count} = new com.livinglogic.ul4.JSPTemplate()".format(count=varcounter))
			make_scriptlet(u"{")
			indent += 1
			make_scriptlet(u"public void execute(java.io.Writer out, Map variables) throws java.io.IOException")
			indent += 1
			make_scriptlet(u"{")
			indent += 1
			for i in xrange(10):
				make_scriptlet(u"Object r{} = null;".format(i))
			defs.append((opcode.arg, variables, varcounter))
			variables = "variables"
		elif opcode.code == "enddef":
			indent -= 1
			make_scriptlet(u"}")
			indent -= 1
			make_scriptlet(u"};")
			(arg, variables, oldcounter) = defs.pop()
			make_scriptlet(u"{var}.put({arg}, template{count});".format(var=variables, arg=javastring(arg), count=oldcounter))
		elif opcode.code == "break":
			make_scriptlet(u"break;")
		elif opcode.code == "continue":
			make_scriptlet(u"continue;")
		elif opcode.code == "not":
			make_scriptlet(u"r{op.r1} = !com.livinglogic.ul4.Utils.getBool(r{op.r2});".format(op=opcode))
		elif opcode.code == "neg":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.neg(r{op.r2});".format(op=opcode))
		elif opcode.code == "contains":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.contains(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "notcontains":
			make_scriptlet(u"r{op.r1} = !com.livinglogic.ul4.Utils.contains(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "eq":
			make_scriptlet(u"r{op.r1} = org.apache.commons.lang.ObjectUtils.equals(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "ne":
			make_scriptlet(u"r{op.r1} = !org.apache.commons.lang.ObjectUtils.equals(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "lt":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.lt(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "le":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.le(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "gt":
			make_scriptlet(u"r{op.r1} = !com.livinglogic.ul4.Utils.le(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "ge":
			make_scriptlet(u"r{op.r1} = !com.livinglogic.ul4.Utils.lt(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "add":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.add(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "sub":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.sub(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "mul":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.mul(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "floordiv":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.floordiv(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "truediv":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.truediv(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "and":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.getBool(r{op.r3}) ? r{op.r2} : r{op.r3};".format(op=opcode))
		elif opcode.code == "or":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.getBool(r{op.r2}) ? r{op.r2} : r{op.r3};".format(op=opcode))
		elif opcode.code == "mod":
			make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.mod(r{op.r2}, r{op.r3});".format(op=opcode))
		elif opcode.code == "callfunc0":
			if opcode.arg == "now":
				make_scriptlet(u"r{op.r1} = new java.util.Date();".format(op=opcode))
			elif opcode.arg in {"utcnow", "random"}:
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}();".format(op=opcode))
			elif opcode.arg == "vars":
				make_scriptlet(u"r{op.r1} = {var};".format(op=opcode, var=variables))
			else:
				raise ul4c.UnknownFunctionError(opcode.arg)
		elif opcode.code == "callfunc1":
			if opcode.arg in {"xmlescape", "csv", "repr", "enumerate", "chr", "ord", "hex", "oct", "bin", "sorted", "range", "type", "json", "reversed", "randrange"}:
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2});".format(op=opcode))
			elif opcode.arg == "str":
				make_scriptlet(u"r{op.r1} = org.apache.commons.lang.ObjectUtils.toString(r{op.r2});".format(op=opcode))
			elif opcode.arg == "int":
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.toInteger(r{op.r2});".format(op=opcode))
			elif opcode.arg == "float":
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.toFloat(r{op.r2});".format(op=opcode))
			elif opcode.arg == "bool":
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.getBool(r{op.r2});".format(op=opcode))
			elif opcode.arg == "len":
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.length(r{op.r2});".format(op=opcode))
			elif opcode.arg == "isnone":
				make_scriptlet(u"r{op.r1} = (r{op.r2} == null);".format(op=opcode))
			elif opcode.arg == "isstr":
				make_scriptlet(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof String));".format(op=opcode))
			elif opcode.arg == "isint":
				make_scriptlet(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof Integer));".format(op=opcode))
			elif opcode.arg == "isfloat":
				make_scriptlet(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof Double));".format(op=opcode))
			elif opcode.arg == "isbool":
				make_scriptlet(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof Boolean));".format(op=opcode))
			elif opcode.arg == "isdate":
				make_scriptlet(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof java.util.Date));".format(op=opcode))
			elif opcode.arg == "islist":
				make_scriptlet(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof java.util.List));".format(op=opcode))
			elif opcode.arg == "isdict":
				make_scriptlet(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof java.util.Map));".format(op=opcode))
			elif opcode.arg == "istemplate":
				make_scriptlet(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof com.livinglogic.ul4.Template));".format(op=opcode))
			elif opcode.arg == "iscolor":
				make_scriptlet(u"r{op.r1} = ((r{op.r2} != null) && (r{op.r2} instanceof com.livinglogic.ul4.Color));".format(op=opcode))
			elif opcode.arg == "get":
				make_scriptlet(u"r{op.r1} = {var}.get(r{op.r2});".format(op=opcode, var=variables))
			else:
				raise ul4c.UnknownFunctionError(opcode.arg)
		elif opcode.code == "callfunc2":
			if opcode.arg in {"range", "zip", "randrange"}:
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3});".format(op=opcode))
			elif opcode.arg == "get":
				make_scriptlet(u"r{op.r1} = {var}.containsKey(r{op.r2}) ? {var}.get(r{op.r2}) : r{op.r3};".format(op=opcode.r1, var=variables))
			else:
				raise ul4c.UnknownFunctionError(opcode.arg)
		elif opcode.code == "callfunc3":
			if opcode.arg in {"range", "zip", "rgb", "hls", "hsv", "randrange"}:
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
			else:
				raise ul4c.UnknownFunctionError(opcode.arg)
		elif opcode.code == "callfunc4":
			if opcode.arg in {"rgb", "hls", "hsv"}:
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4}, r{op.5});".format(op=opcode))
			else:
				raise ul4c.UnknownFunctionError(opcode.arg)
		elif opcode.code == "callmeth0":
			if opcode.arg in {"split", "strip", "lstrip", "rstrip", "upper", "lower", "capitalize", "items", "isoformat", "mimeformat", "day", "month", "year", "hour", "minute", "second", "microsecond", "weekday", "yearday"}:
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2});".format(op=opcode))
			elif opcode.arg in {"r", "g", "b", "a"}:
				make_scriptlet(u"r{op.r1} = ((com.livinglogic.ul4.Color)r{op.r2}).get{arg}();".format(op=opcode, arg=opcode.arg.upper()))
			elif opcode.arg in {"hls", "hlsa", "hsv", "hsva"}:
				make_scriptlet(u"r{op.r1} = ((com.livinglogic.ul4.Color)r{op.r2}).{op.arg}();".format(op=opcode))
			elif opcode.arg == "lum":
				make_scriptlet(u"r{op.r1} = new Double(((com.livinglogic.ul4.Color)r{op.r2}).lum());".format(op=opcode))
			else:
				raise ul4c.UnknownMethodError(opcode.arg)
		elif opcode.code == "callmeth1":
			if opcode.arg in {"split", "rsplit", "strip", "lstrip", "rstrip", "startswith", "endswith", "find", "rfind", "format", "withlum", "witha"}:
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3});".format(op=opcode))
			elif opcode.arg == "get":
				make_scriptlet(u"r{op.r1} = ((java.util.Map)r{op.r2}).get(r{op.r3});".format(op=opcode))
			else:
				raise ul4c.UnknownMethodError(opcode.arg)
		elif opcode.code == "callmeth2":
			if opcode.arg in {"split", "rsplit", "find", "replace"}:
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.{op.arg}(r{op.r2}, r{op.r3}, r{op.r4});".format(op=opcode))
			elif opcode.arg == "get":
				make_scriptlet(u"r{op.r1} = ((java.util.Map)r{op.r2}).containsKey(r{op.r3}) ? ((java.util.Map)r{op.r2}).get(r{op.r3}) : r{op.r4};".format(op=opcode))
			else:
				raise ul4c.UnknownMethodError(opcode.arg)
		elif opcode.code == "callmeth3":
			if opcode.arg == "find":
				make_scriptlet(u"r{op.r1} = com.livinglogic.ul4.Utils.find(r{op.r2}, r{op.r3}, r{op.r4}, r{op.5});".format(op=opcode))
			else:
				raise ul4c.UnknownMethodError(opcode.arg)
		elif opcode.code == "callmethkw":
			if opcode.arg == "render":
				make_scriptlet(u"r{op.r1} = ((com.livinglogic.ul4.Template)r{op.r2}).renders((java.util.Map)r{op.r3});".format(op=opcode))
			else:
				raise ul4c.UnknownMethodError(opcode.arg)
		elif opcode.code == "if":
			make_scriptlet(u"if (com.livinglogic.ul4.Utils.getBool(r{op.r1}))".format(op=opcode))
			make_scriptlet(u"{")
			indent += 1
		elif opcode.code == "else":
			indent -= 1
			make_scriptlet(u"}")
			make_scriptlet(u"else")
			make_scriptlet(u"{")
			indent += 1
		elif opcode.code == "endif":
			indent -= 1
			make_scriptlet(u"}")
		elif opcode.code == "render":
			make_scriptlet(u"((com.livinglogic.ul4.Template)r{op.r1}).renderjsp(out, (Map)r{op.r2});".format(op=opcode))
		else:
			raise ul4c.UnknownOpcodeError(opcode.code)
	make_scriptlet(u"//@@@ END template code")
	return result
