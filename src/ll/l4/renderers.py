# -*- coding: utf-8 -*-

from __future__ import division

from ll import misc
from ll.l4 import compiler
from ll.xist import xsc


def annotate(template):
	stack = []

	def addjump():
		template.opcodes[stack[-1]].jump = i

	for (i, opcode) in enumerate(template):
		if opcode.code == "if":
			stack.append(i)
		elif opcode.code == "else":
			addjump()
			stack[-1] = i
		elif opcode.code == "endif":
			addjump()
			stack.pop()
		elif opcode.code == "for":
			stack.append(i)
		elif opcode.code == "endfor":
			addjump()
			stack.pop()


class Renderer(object):
	def __init__(self, template):
		if isinstance(template, basestring):
			template = compiler.Template.fromsrc(template)
		self.template = template


class PythonRunner(Renderer):
	def __init__(self, template):
		Renderer.__init__(self, template)
		annotate(self.template)
		self.pc = 0

	def func1_isnone(self, arg):
		return arg is None

	def func1_isstr(self, arg):
		return isinstance(arg, basestring)

	def func1_isint(self, arg):
		return isinstance(arg, (int, long)) and not isinstance(arg, bool)

	def func1_isfloat(self, arg):
		return isinstance(arg, float)

	def func1_isbool(self, arg):
		return isinstance(arg, bool)

	def func1_islist(self, arg):
		return isinstance(arg, (list, tuple))

	def func1_isdict(self, arg):
		return isinstance(arg, dict)

	def func1_str(self, arg):
		return unicode(arg) if arg is not None else u""

	def func1_repr(self, arg):
		return repr(arg)

	def func1_int(self, arg):
		return int(arg)

	def func1_len(self, arg):
		return len(arg)

	def func1_enumerate(self, arg):
		return enumerate(arg)

	def func1_xmlescape(self, arg):
		return xml.xmlescape(arg)

	def func1_chr(self, arg):
		return unichr(arg)

	def func1_ord(self, arg):
		return ord(arg)

	def func1_hex(self, arg):
		return hex(arg)

	def func1_oct(self, arg):
		return u"0o%s" % oct(arg)[2:]

	def func1_bin(self, arg):
		return "0b" + ("".join("1" if arg & 1<<i else "0" for i in xrange(100)).rstrip("0"))[::-1]

	def meth0_split(self, obj):
		return obj.split()

	def meth1_split(self, obj, arg1):
		return obj.split(arg1)

	def meth2_split(self, obj, arg1, arg2):
		return obj.split(arg1, arg2)

	def meth0_rsplit(self, obj):
		return obj.rsplit()

	def meth1_rsplit(self, obj, arg1):
		return obj.rsplit(arg1)

	def meth2_rsplit(self, obj, arg1, arg2):
		return obj.rsplit(arg1, arg2)

	def meth0_strip(self, obj):
		return obj.strip()

	def meth1_strip(self, obj, arg):
		return obj.strip(arg)

	def meth0_lstrip(self, obj):
		return obj.lstrip()

	def meth1_lstrip(self, obj, arg):
		return obj.lstrip(arg)

	def meth0_rstrip(self, obj):
		return obj.rstrip()

	def meth0_items(self, obj):
		return obj.iteritems()

	def meth1_rstrip(self, obj, arg):
		return obj.rstrip(arg)

	def meth1_startswith(self, obj, arg):
		return obj.startswith(arg)

	def meth1_endswith(self, obj, arg):
		return obj.endswith(arg)

	def meth0_upper(self, obj):
		return obj.upper()

	def meth0_lower(self, obj):
		return obj.lower()

	def meth1_find(self, obj, arg):
		return obj.find(arg)

	def meth2_find(self, obj, arg1, arg2):
		return obj.find(arg1, arg2)

	def meth3_find(self, obj, arg1, arg2, arg3):
		return obj.rsplit(arg1, arg2, arg3)

	def render(self, data):
		variables = dict(data=data)

		# All active iterators
		iterators = []

		# The registers for our virtual CPU
		reg = 10*[None]

		# Current program counter
		while self.pc < len(self.template.opcodes):
			opcode = self.template.opcodes[self.pc]
			try:
				code = opcode.code
				r1 = opcode.r1
				r2 = opcode.r2
				r3 = opcode.r3
				r3 = opcode.r3
				r4 = opcode.r4
				r5 = opcode.r5
				arg = opcode.arg
				jump = opcode.jump
				# for i in xrange(10):
				# 	print "      %d=%r" % (i, reg[i])
				# print "#%d code=%r, r1=%r, r2=%r, r3=%r, r4=%r, r5=%r, arg=%r" % (self.pc, code, r1, r2, r3, r4, r5, arg)
				# print
				if code is None:
					yield unicode(opcode.location.code)
				elif code == "print":
					if reg[r1] is not None:
						yield unicode(reg[r1])
				elif code == "loadstr":
					reg[r1] = arg
				elif code == "loadint":
					reg[r1] = int(arg)
				elif code == "loadfloat":
					reg[r1] = float(arg)
				elif code == "loadnone":
					reg[r1] = None
				elif code == "loadfalse":
					reg[r1] = False
				elif code == "loadtrue":
					reg[r1] = True
				elif code == "loadvar":
					reg[r1] = variables[arg]
				elif code == "storevar":
					variables[arg] = reg[r1]
				elif code == "addvar":
					variables[arg] += reg[r1]
				elif code == "subvar":
					variables[arg] -= reg[r1]
				elif code == "mulvar":
					variables[arg] *= reg[r1]
				elif code == "truedivvar":
					variables[arg] /= reg[r1]
				elif code == "floordivvar":
					variables[arg] //= reg[r1]
				elif code == "modvar":
					variables[arg] %= reg[r1]
				elif code == "delvar":
					del variables[arg]
				elif code == "getattr":
					reg[r1] = reg[r2][arg]
				elif code == "getitem":
					reg[r1] = reg[r2][reg[r3]]
				elif code == "getslice12":
					reg[r1] = reg[r2][reg[r3]:reg[r4]]
				elif code == "getslice1":
					reg[r1] = reg[r2][reg[r3]:]
				elif code == "getslice2":
					reg[r1] = reg[r2][:reg[r3]]
				elif code == "getslice":
					reg[r1] = reg[r2][:]
				elif code == "for":
					iterator = iter(reg[r2])
					try:
						reg[r1] = iterator.next()
					except StopIteration:
						self.pc = jump+1 # Skip loop
						continue
					iterators.append((r1, self.pc, iterator)) # Remember the loop register, where to restart the loop and the iterator
				elif code == "endfor":
					(r, loopstart, iterator) = iterators[-1]
					try:
						reg[r] = iterator.next()
					except StopIteration:
						iterators.pop()
					else:
						self.pc = loopstart+1
						continue
				elif code == "contains":
					try:
						reg[r1] = reg[r2] in reg[r3]
					except TypeError:
						reg[r1] = None # FIXME: exception
				elif code == "notcontains":
					try:
						reg[r1] = reg[r2] not in reg[r3]
					except TypeError:
						reg[r1] = None # FIXME: exception
				elif code == "not":
					reg[r1] = not reg[r2]
				elif code == "neg":
					reg[r1] = -reg[r2]
				elif code == "equals":
					reg[r1] = (reg[r2] == reg[r3])
				elif code == "notequals":
					reg[r1] = (reg[r2] != reg[r3])
				elif code == "add":
					reg[r1] = reg[r2] + reg[r3]
				elif code == "sub":
					reg[r1] = reg[r2] - reg[r3]
				elif code == "mul":
					reg[r1] = reg[r2] * reg[r3]
				elif code == "floordiv":
					reg[r1] = reg[r2] // reg[r3]
				elif code == "truediv":
					reg[r1] = reg[r2] / reg[r3]
				elif code == "and":
					reg[r1] = bool(reg[r2] and reg[r3])
				elif code == "or":
					reg[r1] = bool(reg[r2] or reg[r3])
				elif code == "mod":
					reg[r1] = reg[r2] % reg[r3]
				elif code == "callfunc0":
					try:
						func = getattr(self, "func0_%s" % arg)
					except AttributeError:
						raise compiler.UnknownFunctionError(arg)
					reg[r1] = func()
				elif code == "callfunc1":
					try:
						func = getattr(self, "func1_%s" % arg)
					except AttributeError:
						raise compiler.UnknownFunctionError(arg)
					reg[r1] = func(reg[r2])
				elif code == "callfunc2":
					try:
						func = getattr(self, "func2_%s" % arg)
					except AttributeError:
						raise compiler.UnknownFunctionError(arg)
					reg[r1] = func(reg[r2], reg[r3])
				elif code == "callmeth0":
					try:
						meth = getattr(self, "meth0_%s" % arg)
					except AttributeError:
						raise compiler.UnknownMethodError(arg)
					reg[r1] = meth(reg[r2])
				elif code == "callmeth1":
					try:
						meth = getattr(self, "meth1_%s" % arg)
					except AttributeError:
						raise compiler.UnknownMethodError(arg)
					reg[r1] = meth(reg[r2], reg[r3])
				elif code == "callmeth2":
					try:
						meth = getattr(self, "meth2_%s" % arg)
					except AttributeError:
						raise compiler.UnknownMethodError(arg)
					reg[r1] = meth(reg[r2], reg[r3], reg[r4])
				elif code == "if":
					if not reg[r1]:
						# jump to the first opcode after the ``else``.
						self.pc = jump+1
						continue
					# else continue with the next opcode
				elif code == "else":
					# If we run into an ``else``, jump after the ``endif``, as we have executed the ``if`` block.
					self.pc = jump+1
					continue
				elif code == "endif":
					pass
				else:
					raise compiler.UnknownOpcodeError(code)
				self.pc += 1
			except compiler.Error, exc:
				exc.decorate(opcode.location)
				raise
			except Exception, exc:
				raise compiler.Error(exc).decorate(opcode.location)


class PythonCode(Renderer):
	def __init__(self, template):
		Renderer.__init__(self, template)
		self.indent = 0

	def code(self, code):
		return "%s%s\n" % ("\t"*self.indent, code)

	def function(self):
		code = "".join(self.render("render"))
		ns = {}
		exec code.encode("ascii") in ns
		return ns["render"]

	def render(self, function=None):
		self.indent = 0
		if function is not None:
			yield self.code("def %s(data):" % function)
			self.indent += 1
		yield self.code("import sys")
		yield self.code("from ll.misc import xmlescape")
		yield self.code("from ll.l4 import compiler")
		yield self.code("variables = dict(data=data)")
		yield self.code("source = %r" % self.template.source)
		yield self.code("locations = %r" % (tuple((oc.location.type, oc.location.starttag, oc.location.endtag, oc.location.startcode, oc.location.endcode) for oc in self.template),))
		for i in xrange(10):
			yield self.code("reg%d = None" % i)

		yield self.code("try:")
		self.indent += 1
		yield self.code("startline = sys._getframe().f_lineno+1") # The source line of the first opcode
		try:
			for opcode in self.template:
				# The following code ensures that each opcode outputs exactly one source code line
				# This makes it possible in case of an error to find out which opcode produced the error
				if opcode.code is None:
					yield self.code("yield %r" % opcode.location.code)
				elif opcode.code == "loadstr":
					yield self.code("reg%d = %r" % (opcode.r1, opcode.arg))
				elif opcode.code == "loadint":
					yield self.code("reg%d = %s" % (opcode.r1, opcode.arg))
				elif opcode.code == "loadfloat":
					yield self.code("reg%d = %s" % (opcode.r1, opcode.arg))
				elif opcode.code == "loadnone":
					yield self.code("reg%d = None" % opcode.r1)
				elif opcode.code == "loadfalse":
					yield self.code("reg%d = False" % opcode.r1)
				elif opcode.code == "loadtrue":
					yield self.code("reg%d = True" % opcode.r1)
				elif opcode.code == "loadvar":
					yield self.code("reg%d = variables[%r]" % (opcode.r1, opcode.arg))
				elif opcode.code == "storevar":
					yield self.code("variables[%r] = reg%d" % (opcode.arg, opcode.r1))
				elif opcode.code == "addvar":
					yield self.code("variables[%r] += reg%d" % (opcode.arg, opcode.r1))
				elif opcode.code == "subvar":
					yield self.code("variables[%r] -= reg%d" % (opcode.arg, opcode.r1))
				elif opcode.code == "mulvar":
					yield self.code("variables[%r] *= reg%d" % (opcode.arg, opcode.r1))
				elif opcode.code == "truedivvar":
					yield self.code("variables[%r] /= reg%d" % (opcode.arg, opcode.r1))
				elif opcode.code == "floordivvar":
					yield self.code("variables[%r] //= reg%d" % (opcode.arg, opcode.r1))
				elif opcode.code == "modvar":
					yield self.code("variables[%r] %= reg%d" % (opcode.arg, opcode.r1))
				elif opcode.code == "delvar":
					yield self.code("del variables[%r]" % opcode.arg)
				elif opcode.code == "getattr":
					yield self.code("reg%d = reg%d[%r]" % (opcode.r1, opcode.r2, opcode.arg))
				elif opcode.code == "getitem":
					yield self.code("reg%d = reg%d[reg%d]" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "getslice12":
					yield self.code("reg%d = reg%d[reg%d:reg%d]" % (opcode.r1, opcode.r2, opcode.r3, opcode.r4))
				elif opcode.code == "getslice1":
					yield self.code("reg%d = reg%d[reg%d:]" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "getslice2":
					yield self.code("reg%d = reg%d[:reg%d]" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "getslice":
					yield self.code("reg%d = reg%d[:]" % (opcode.r1, opcode.r2))
				elif opcode.code == "print":
					yield self.code("if reg%d is not None: yield unicode(reg%d)" % (opcode.r1, opcode.r1))
				elif opcode.code == "for":
					yield self.code("for reg%d in reg%d:" % (opcode.r1, opcode.r2))
					self.indent += 1
				elif opcode.code == "endfor":
					self.indent -= 1
					yield self.code("# end for")
				elif opcode.code == "not":
					yield self.code("reg%d = not reg%d" % (opcode.r1, opcode.r2))
				elif opcode.code == "neg":
					yield self.code("reg%d = -reg%d" % (opcode.r1, opcode.r2))
				elif opcode.code == "contains":
					yield self.code("reg%d = reg%d in reg%d" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "notcontains":
					yield self.code("reg%d = reg%d not in reg%d" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "equals":
					yield self.code("reg%d = reg%d == reg%d" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "notequals":
					yield self.code("reg%d = reg%d != reg%d" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "add":
					yield self.code("reg%d = reg%d + reg%d" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "sub":
					yield self.code("reg%d = reg%d - reg%d" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "mul":
					yield self.code("reg%d = reg%d * reg%d" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "floordiv":
					yield self.code("reg%d = reg%d // reg%d" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "truediv":
					yield self.code("reg%d = reg%d / reg%d" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "and":
					yield self.code("reg%d = bool(reg%d and reg%d)" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "or":
					yield self.code("reg%d = bool(reg%d or reg%d)" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "mod":
					yield self.code("reg%d = reg%d %% reg%d" % (opcode.r1, opcode.r2, opcode.r3))
				elif opcode.code == "callfunc0":
					raise compiler.UnknownFunctionError(opcode.arg)
				elif opcode.code == "callfunc1":
					if opcode.arg == "xmlescape":
						yield self.code("reg%d = xmlescape(reg%d)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "str":
						yield self.code("reg%d = unicode(reg%d) if reg%d is not None else u''" % (opcode.r1, opcode.r2, opcode.r2))
					elif opcode.arg == "int":
						yield self.code("reg%d = int(reg%d)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "len":
						yield self.code("reg%d = len(reg%d)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "enumerate":
						yield self.code("reg%d = enumerate(reg%d)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "isnone":
						yield self.code("reg%d = reg%d is None" % (opcode.r1, opcode.r2))
					elif opcode.arg == "isstr":
						yield self.code("reg%d = isinstance(reg%d, basestring)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "isint":
						yield self.code("reg%d = isinstance(reg%d, (int, long)) and not isinstance(reg%d, bool)" % (opcode.r1, opcode.r2, opcode.r2))
					elif opcode.arg == "isfloat":
						yield self.code("reg%d = isinstance(reg%d, float)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "isbool":
						yield self.code("reg%d = isinstance(reg%d, bool)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "islist":
						yield self.code("reg%d = isinstance(reg%d, (list, tuple))" % (opcode.r1, opcode.r2))
					elif opcode.arg == "isdict":
						yield self.code("reg%d = isinstance(reg%d, dict)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "repr":
						yield self.code("reg%d = unicode(repr(reg%d))" % (opcode.r1, opcode.r2))
					elif opcode.arg == "chr":
						yield self.code("reg%d = unichr(reg%d)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "ord":
						yield self.code("reg%d = ord(reg%d)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "hex":
						yield self.code("reg%d = hex(reg%d)" % (opcode.r1, opcode.r2))
					elif opcode.arg == "oct":
						yield self.code('reg%d = "0o%%s" % oct(reg%d)[2:]' % (opcode.r1, opcode.r2))
					elif opcode.arg == "bin":
						yield self.code('reg%d = "0b" + ("".join("1" if reg%d & 1<<i else "0" for i in xrange(100)).rstrip("0"))[::-1]' % (opcode.r1, opcode.r2))
					else:
						raise compiler.UnknownFunctionError(opcode.arg)
				elif opcode.code == "callfunc2":
					raise compiler.UnknownFunctionError(opcode.arg)
				elif opcode.code == "callmeth0":
					if opcode.arg in ("split", "rsplit", "strip", "lstrip", "rstrip", "upper", "lower"):
						yield self.code("reg%d = reg%d.%s()" % (opcode.r1, opcode.r2, opcode.arg))
					elif opcode.arg == "items":
						yield self.code("reg%d = reg%d.iteritems()" % (opcode.r1, opcode.r2))
					else:
						raise compiler.UnknownMethodError(opcode.arg)
				elif opcode.code == "callmeth1":
					if opcode.arg in ("split", "rsplit", "strip", "lstrip", "rstrip", "startswith", "endswith", "find"):
						yield self.code("reg%d = reg%d.%s(reg%d)" % (opcode.r1, opcode.r2, opcode.arg, opcode.r3))
					else:
						raise compiler.UnknownMethodError(opcode.arg)
				elif opcode.code == "callmeth2":
					if opcode.arg in ("split", "rsplit", "find"):
						yield self.code("reg%d = reg%d.%s(reg%d, reg%d)" % (opcode.r1, opcode.r2, opcode.arg, opcode.r3, opcode.r4))
					else:
						raise compiler.UnknownMethodError(opcode.arg)
				elif opcode.code == "callmeth3":
					if opcode.arg == "find":
						yield self.code("reg%d = reg%d.%s(reg%d, reg%d, reg%d)" % (opcode.r1, opcode.r2, opcode.arg, opcode.r3, opcode.r4, opcode.r5))
					else:
						raise compiler.UnknownMethodError(opcode.arg)
				elif opcode.code == "if":
					yield self.code("if reg%d:" % opcode.r1)
					self.indent += 1
				elif opcode.code == "else":
					self.indent -= 1
					yield self.code("else:")
					self.indent += 1
				elif opcode.code == "endif":
					self.indent -= 1
					yield self.code("# end if")
				else:
					raise compiler.UnknownOpcodeError(opcode.code)
		except compiler.Error, exc:
			exc.decorate(opcode.location)
			raise
		except Exception, exc:
			raise compiler.Error(exc).decorate(opcode.location)
		self.indent -= 1
		buildloc = "compiler.Location(source, *locations[sys.exc_info()[2].tb_lineno-startline])"
		yield self.code("except compiler.Error, exc:")
		self.indent += 1
		yield self.code("exc.decorate(%s)" % buildloc)
		yield self.code("raise")
		self.indent -= 1
		yield self.code("except Exception, exc:")
		self.indent += 1
		yield self.code("raise compiler.Error(exc).decorate(%s)" % buildloc)
