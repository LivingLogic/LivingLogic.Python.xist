#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009-2012 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, os, re, datetime, io, json, contextlib, tempfile, collections, shutil, subprocess, pkg_resources

import py.test

from ll import ul4c, color, misc
from ll.xist.ns import html, ul4


class PseudoDict(collections.Mapping):
	def __init__(self, dict):
		self.dict = dict

	def __getitem__(self, key):
		return self.dict[key]

	def __iter__(self):
		return iter(self.dict)

	def __len__(self):
		return len(self.dict)


class PseudoList(collections.Sequence):
	def __init__(self, list):
		self.list = list

	def __getitem__(self, index):
		return self.list[index]

	def __len__(self):
		return len(self.list)


class Render(object):
	def __init__(self, __, **variables):
		self.source = __
		self.variables = variables
		f = sys._getframe(1)
		self.filename = f.f_code.co_filename
		self.lineno = f.f_lineno

	def __repr__(self):
		return "{0.__class__.__name__}({0.source!r}, {0.variables!r})".format(self)


class RenderPython(Render):
	def renders(self):
		template = ul4c.Template(self.source)
		print("Testing Python template ({}, line {}):".format(self.filename, self.lineno))
		print(template.pythonsource())
		return template.renders(**self.variables)


class RenderPythonDumpS(Render):
	def renders(self):
		template = ul4c.Template(self.source)
		template = ul4c.Template.loads(template.dumps()) # Recreate the template from the binary dump
		print("Testing Python template loaded from string ({}, line {}):".format(self.filename, self.lineno))
		print(template.pythonsource())
		return template.renders(**self.variables)


class RenderPythonDump(Render):
	def renders(self):
		template = ul4c.Template(self.source)
		stream = io.StringIO()
		template.dump(stream)
		stream.seek(0)
		template = ul4c.Template.load(stream) # Recreate the template from the stream
		print("Testing Python template loaded from stream ({}, line {}):".format(self.filename, self.lineno))
		print(template.pythonsource())
		return template.renders(**self.variables)


class RenderJS(Render):
	def renders(self):
		# Check the Javascript version (this requires an installed ``d8`` shell from V8 (http://code.google.com/p/v8/))
		template = ul4c.Template(self.source)
		js = template.jssource()
		js = "template = {};\ndata = {};\nprint(template.renders(data));\n".format(js, ul4c._asjson(self.variables))
		print("Testing Javascript code compiled by Python ({}, line {}):".format(self.filename, self.lineno))
		print(js)
		with tempfile.NamedTemporaryFile(mode="wb", suffix=".js") as f:
			f.write(js.encode("utf-8"))
			f.flush()
			dir = pkg_resources.resource_filename("ll.xist", "data/")
			proc = subprocess.Popen("d8 {dir}/js/ul4on.js {dir}/js/ul4.js {fn}".format(dir=dir, fn=f.name), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			(stdout, stderr) = proc.communicate()
		stdout = stdout.decode("utf-8")
		stderr = stderr.decode("utf-8")
		# Check if we have an exception
		if proc.returncode:
			print(stderr, file=sys.stderr)
			raise RuntimeError((stderr or stdout).splitlines()[0])
		return stdout[:-1] # Drop the "\n"


class RenderJava(Render):
	maincodetemplate = """
	public class UL4Test
	{
		@SuppressWarnings("unchecked")
		public static void main(String[] args) throws java.io.IOException, java.io.UnsupportedEncodingException, org.antlr.runtime.RecognitionException
		{
			%(source)s
		}
	}
	"""

	def findexception(self, output):
		lines = output.splitlines()
		msg = None
		for line in lines:
			prefix1 = 'Exception in thread "main"'
			prefix2 = "Caused by:"
			if line.startswith(prefix1):
				msg = line[len(prefix1):].strip()
			elif line.startswith(prefix2):
				msg = line[len(prefix2):].strip()
		if msg is not None:
			print(output, file=sys.stderr)
			raise RuntimeError(msg)

	def formatsource(self, string):
		"""
		Reindents the Java source.
		"""
		indent = 0
		newlines = []
		for line in string.strip().splitlines(False):
			line = line.strip()
			if line == "}" or line == "};":
				indent -= 1
			if line:
				newlines.append(indent*"\t" + line + "\n")
			if line == "{":
				indent += 1
		return "".join(newlines)

	def runsource(self, source):
		"""
		Compile the Java source :var:`source`, run it and return the output
		"""
		tempdir = tempfile.mkdtemp()
		try:
			source = self.maincodetemplate % dict(source=source)
			source = self.formatsource(source)
			print(source)
			with open(os.path.join(tempdir, "UL4Test.java"), "wb") as f:
				f.write(source.encode("utf-8"))
			proc = subprocess.Popen("cd {}; javac -encoding utf-8 UL4Test.java".format(tempdir), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			(stdout, stderr) = proc.communicate()
			if proc.returncode:
				stderr = stderr.decode("utf-8")
				print(stderr, file=sys.stderr)
				raise RuntimeError(stderr.splitlines()[0])
			proc = subprocess.Popen("cd {}; java UL4Test".format(tempdir), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			(stdout, stderr) = proc.communicate()
			# Check if we have an exception
			self.findexception(stderr.decode("utf-8"))
		finally:
			shutil.rmtree(tempdir)
		if stderr:
			print(stderr, file=sys.stderr)
		return stdout.decode("utf-8")


class RenderJavaInterpretedTemplateByPython(RenderJava):
	codetemplate = """
	com.livinglogic.ul4.InterpretedTemplate template = %(template)s;
	java.util.Map<String, Object> variables = %(variables)s;
	String output = template.renders(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	def renders(self):
		# Check the Java version
		print("Testing Java InterpretedTemplate (compiled by Python) ({}, line {}):".format(self.filename, self.lineno))
		templatesource = ul4c.Template(self.source).javasource(interpreted=True)
		java = self.codetemplate % dict(variables=misc.javaexpr(self.variables), template=templatesource)
		return self.runsource(java)


class RenderJavaCompiledTemplateByPython(RenderJava):
	codetemplate = """
	com.livinglogic.ul4.Template template = %(template)s;
	java.util.Map<String, Object> variables = %(variables)s;
	String output = template.renders(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	def renders(self):
		# Check the Java version
		print("Testing Java CompiledTemplate (compiled by Python) ({}, line {}):".format(self.filename, self.lineno))
		template = ul4c.Template(self.source)
		java = template.javasource(interpreted=False)
		java = self.codetemplate % dict(variables=misc.javaexpr(self.variables), template=java)
		return self.runsource(java)


class RenderJavaInterpretedTemplateByJava(RenderJava):
	codetemplate = """
	com.livinglogic.ul4.InterpretedTemplate template = new com.livinglogic.ul4.InterpretedTemplate(%(source)s);
	java.util.Map<String, Object> variables = %(variables)s;
	String output = template.renders(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	def renders(self):
		# Check the Java version
		print("Testing Java InterpretedTemplate (compiled by Java) ({}, line {}):".format(self.filename, self.lineno))
		java = self.codetemplate % dict(source=misc.javaexpr(self.source), variables=misc.javaexpr(self.variables))
		return self.runsource(java)


all_python_renderers = (RenderPython, RenderPythonDumpS, RenderPythonDump)
# FIXME: The following really takes a long time to run:
# all_renderers = (RenderPython, RenderPythonDumpS, RenderPythonDump, RenderJS, RenderJavaInterpretedTemplateByPython, RenderJavaCompiledTemplateByPython, RenderJavaInterpretedTemplateByJava)
all_renderers = all_python_renderers
all_renderers = (RenderJavaCompiledTemplateByPython,)


argumentmismatchmessage = [
	# Python argument mismatch exception messages
	"takes exactly \\d+ (positional )?arguments?",
	"expected \\d+ arguments?",
	"Required argument .* not found",
	"takes exactly one argument",
	"expected at least \\d+ arguments",
	"takes at most \\d+ (positional )?arguments?",
	"takes at least \\d+ argument",
	"takes no arguments",
	# Javascript argument mismatch exception messages
	"requires \\d+(-\\d+)? arguments?, \\d+ given",
	# Java compiler errors for argument mismatches
	"cannot find symbol",
	"cannot be applied",
]
argumentmismatchmessage = "({})".format("|".join(argumentmismatchmessage))


def eq(expected, render):
	got = render.renders() # Put this on an extra line, so that py.test executes it only once
	assert expected == got


def evaleq(expected, render):
	got = eval(render.renders())
	assert expected == got


def contains(expected, render):
	got = render.renders()
	assert got in expected


def le(expected, render):
	got = render.renders()
	assert expected <= got


def exceptionchain(exc):
	while exc is not None:
		yield exc
		exc = exc.__cause__


def raises(msg, render):
	# Check that executing ``render`` raises an exception that matches a regexp
	try:
		render.renders()
	except Exception as exc:
		exceptionmsgs = ["{0.__class__.__module__}.{0.__class__.__name__}: {0}".format(subexc) for subexc in exceptionchain(exc)]
		assert any(re.search(msg, exceptionmsg) is not None for exceptionmsg in exceptionmsgs)
	else:
		py.test.fail("failed to raise exception")


@py.test.mark.ul4
def test_text():
	for r in all_renderers:
		yield eq, 'gurk', r('gurk')
		yield eq, 'g\xfcrk', r('g\xfcrk')


@py.test.mark.ul4
def test_none():
	for r in all_renderers:
		yield eq, '', r('<?print None?>')
		yield eq, 'no', r('<?if None?>yes<?else?>no<?end if?>')


@py.test.mark.ul4
def test_false():
	for r in all_renderers:
		yield eq, 'False', r('<?print False?>')
		yield eq, 'no', r('<?if False?>yes<?else?>no<?end if?>')


@py.test.mark.ul4
def test_true():
	for r in all_renderers:
		yield eq, 'True', r('<?print True?>')
		yield eq, 'yes', r('<?if True?>yes<?else?>no<?end if?>')


@py.test.mark.ul4
def test_int():
	for r in all_renderers:
		values = (0, 42, -42, 0x7ffffff, 0x8000000, -0x8000000, -0x8000001)
		if r is not RenderJS:
			# Since Javascript has no real integers the following would lead to rounding errors
			values += (0x7ffffffffffffff, 0x800000000000000, -0x800000000000000, -0x800000000000001, 9999999999, -9999999999, 99999999999999999999, -99999999999999999999)
		for value in values:
			yield eq, str(value), r('<?print {}?>'.format(value))
		yield eq, '255', r('<?print 0xff?>')
		yield eq, '255', r('<?print 0Xff?>')
		yield eq, '-255', r('<?print -0xff?>')
		yield eq, '-255', r('<?print -0Xff?>')
		yield eq, '63', r('<?print 0o77?>')
		yield eq, '63', r('<?print 0O77?>')
		yield eq, '-63', r('<?print -0o77?>')
		yield eq, '-63', r('<?print -0O77?>')
		yield eq, '7', r('<?print 0b111?>')
		yield eq, '7', r('<?print 0B111?>')
		yield eq, '-7', r('<?print -0b111?>')
		yield eq, '-7', r('<?print -0B111?>')

		yield eq, 'no', r('<?if 0?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r('<?if 1?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r('<?if -1?>yes<?else?>no<?end if?>')


@py.test.mark.ul4
def test_float():
	for r in all_renderers:
		# str() output might differ slightly between Python and JS, so eval the output again for tests
		yield evaleq, 0.0, r('<?print 0.?>')
		yield evaleq, 42.0, r('<?print 42.?>')
		yield evaleq, -42.0, r('<?print -42.?>')
		yield evaleq, -42.5, r('<?print -42.5?>')
		yield evaleq, 1e42, r('<?print 1E42?>')
		yield evaleq, 1e42, r('<?print 1e42?>')
		yield evaleq, -1e42, r('<?print -1E42?>')
		yield evaleq, -1e42, r('<?print -1e42?>')

		yield eq, 'no', r('<?if 0.?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r('<?if 1.?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r('<?if -1.?>yes<?else?>no<?end if?>')


@py.test.mark.ul4
def test_string():
	for r in all_renderers:
		yield raises, "Unterminated string|mismatched character|MismatchedTokenException", r('<?print "?>')
		yield eq, 'foo', r('<?print "foo"?>')
		yield eq, '\n', r('<?print "\\n"?>')
		yield eq, '\r', r('<?print "\\r"?>')
		yield eq, '\t', r('<?print "\\t"?>')
		yield eq, '\f', r('<?print "\\f"?>')
		yield eq, '\b', r('<?print "\\b"?>')
		yield eq, '\a', r('<?print "\\a"?>')
		yield eq, '\x1b', r('<?print "\\e"?>')
		yield eq, '\x00', r('<?print "\\x00"?>')
		yield eq, '"', r('<?print "\\""?>')
		yield eq, "'", r('<?print "\\\'"?>')
		yield eq, '\u20ac', r('<?print "\u20ac"?>')
		yield eq, '\xff', r('<?print "\\xff"?>')
		yield eq, '\u20ac', r('''<?print "\\u20ac"?>''')
		yield eq, "a\nb", r('<?print "a\nb"?>')
		for c in "\x00\x80\u0100\u3042\n\r\t\f\b\a\e\"":
			yield eq, c, r('<?print obj?>', obj=c) # This tests :func:`misc.javaexpr` for Java and :func:`ul4c._asjson` for JS

		# Test literal control characters
		yield eq, 'gu\n\r\trk', r("<?print 'gu\n\r\trk'?>")
		yield eq, 'gu\n\r\t\\rk', r(r"<?print 'gu\n\r\t\\rk'?>")

		yield eq, 'no', r('<?if ""?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r('<?if "foo"?>yes<?else?>no<?end if?>')


@py.test.mark.ul4
def test_date():
	for r in all_renderers:
		yield eq, '2000-02-29', r('<?print @(2000-02-29).isoformat()?>')
		yield eq, '2000-02-29', r('<?print @(2000-02-29T).isoformat()?>')
		yield eq, '2000-02-29T12:34:00', r('<?print @(2000-02-29T12:34).isoformat()?>')
		yield eq, '2000-02-29T12:34:56', r('<?print @(2000-02-29T12:34:56).isoformat()?>')
		yield eq, '2000-02-29T12:34:56.987000', r('<?print @(2000-02-29T12:34:56.987000).isoformat()?>') # JS and Java only supports milliseconds
		yield eq, 'yes', r('<?if @(2000-02-29T12:34:56.987654)?>yes<?else?>no<?end if?>')


@py.test.mark.ul4
def test_color():
	for r in all_renderers:
		yield eq, '255,255,255,255', r('<?code c = #fff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
		yield eq, '255,255,255,255', r('<?code c = #ffffff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
		yield eq, '18,52,86,255', r('<?code c = #123456?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
		yield eq, '17,34,51,68', r('<?code c = #1234?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
		yield eq, '18,52,86,120', r('<?code c = #12345678?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
		yield eq, 'yes', r('<?if #fff?>yes<?else?>no<?end if?>')


@py.test.mark.ul4
def test_list():
	for r in all_renderers:
		yield eq, '', r('<?for item in []?><?print item?>;<?end for?>')
		yield eq, '1;', r('<?for item in [1]?><?print item?>;<?end for?>')
		yield eq, '1;', r('<?for item in [1,]?><?print item?>;<?end for?>')
		yield eq, '1;2;', r('<?for item in [1, 2]?><?print item?>;<?end for?>')
		yield eq, '1;2;', r('<?for item in [1, 2,]?><?print item?>;<?end for?>')
		yield eq, 'no', r('<?if []?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r('<?if [1]?>yes<?else?>no<?end if?>')


@py.test.mark.ul4
def test_dict():
	for r in all_renderers:
		yield eq, '', r('<?for (key, value) in {}.items()?><?print key?>:<?print value?>\n<?end for?>')
		yield eq, '1:2\n', r('<?for (key, value) in {1:2}.items()?><?print key?>:<?print value?>\n<?end for?>')
		yield eq, '1:#fff\n', r('<?for (key, value) in {1:#fff}.items()?><?print key?>:<?print value?>\n<?end for?>')
		yield eq, '1:2\n', r('<?for (key, value) in {1:2,}.items()?><?print key?>:<?print value?>\n<?end for?>')
		# With duplicate keys, later ones simply overwrite earlier ones
		yield eq, '1:3\n', r('<?for (key, value) in {1:2, 1: 3}.items()?><?print key?>:<?print value?>\n<?end for?>')
		# Test **
		yield eq, '1:2\n', r('<?for (key, value) in {**{1:2}}.items()?><?print key?>:<?print value?>\n<?end for?>')
		yield eq, '1:4\n', r('<?for (key, value) in {1:1, **{1:2}, 1:3, **{1:4}}.items()?><?print key?>:<?print value?>\n<?end for?>')
		yield eq, 'no', r('<?if {}?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r('<?if {1:2}?>yes<?else?>no<?end if?>')


@py.test.mark.ul4
def test_code_storevar():
	for r in all_renderers:
		yield eq, '42', r('<?code x = 42?><?print x?>')
		yield eq, 'xyzzy', r('<?code x = "xyzzy"?><?print x?>')


@py.test.mark.ul4
def test_code_addvar():
	for r in all_renderers:
		for x in (17, 17., False, True):
			for y in (23, 23., False, True):
				yield evaleq, x + y, r('<?code x = {}?><?code x += {}?><?print x?>'.format(x, y))
		yield eq, 'xyzzy', r('<?code x = "xyz"?><?code x += "zy"?><?print x?>')


@py.test.mark.ul4
def test_code_subvar():
	for r in all_renderers:
		for x in (17, 17., False, True):
			for y in (23, 23., False, True):
				yield evaleq, x - y, r('<?code x = {}?><?code x -= {}?><?print x?>'.format(x, y))


@py.test.mark.ul4
def test_code_mulvar():
	for r in all_renderers:
		for x in (17, 17., False, True):
			for y in (23, 23., False, True):
				yield evaleq, x * y, r('<?code x = {}?><?code x *= {}?><?print x?>'.format(x, y))
		for x in (17, False, True):
			y = "xyzzy"
			yield eq, x * y, r('<?code x = {}?><?code x *= {!r}?><?print x?>'.format(x, y))
		yield eq, 17*"xyzzy", r('<?code x = "xyzzy"?><?code x *= 17?><?print x?>')


@py.test.mark.ul4
def test_code_floordivvar():
	for r in all_renderers:
		for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
			for y in (2, -2, 2.0, -2.0, True):
				yield evaleq, x // y, r('<?code x = {}?><?code x //= {}?><?print x?>'.format(x, y))


@py.test.mark.ul4
def test_code_truedivvar():
	for r in all_renderers:
		for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
			for y in (2, -2, 2.0, -2.0, True):
				yield evaleq, x / y, r('<?code x = {}?><?code x /= {}?><?print x?>'.format(x, y))


@py.test.mark.ul4
def test_code_modvar():
	for r in all_renderers:
		for x in (1729, 1729.0, -1729, -1729.0, False, True):
			for y in (23, 23., -23, -23.0, True):
				yield evaleq, x % y, r('<?code x = {}?><?code x %= {}?><?print x?>'.format(x, y))


@py.test.mark.ul4
def test_code_delvar():
	for r in all_renderers:
		if r is not RenderJS:
			yield raises, "(KeyError|not found)", r('<?code x = 1729?><?code del x?><?print x?>')


@py.test.mark.ul4
def test_for_string():
	for r in all_renderers:
		yield eq, '', r('<?for c in data?>(<?print c?>)<?end for?>', data="")
		yield eq, '(g)(u)(r)(k)', r('<?for c in data?>(<?print c?>)<?end for?>', data="gurk")


@py.test.mark.ul4
def test_for_list():
	for r in all_renderers:
		yield eq, '', r('<?for c in data?>(<?print c?>)<?end for?>', data="")
		yield eq, '(g)(u)(r)(k)', r('<?for c in data?>(<?print c?>)<?end for?>', data=["g", "u", "r", "k"])


@py.test.mark.ul4
def test_for_dict():
	for r in all_renderers:
		yield eq, '', r('<?for c in data?>(<?print c?>)<?end for?>', data={})
		yield eq, '(a)(b)(c)', r('<?for c in sorted(data)?>(<?print c?>)<?end for?>', data=dict(a=1, b=2, c=3))


@py.test.mark.ul4
def test_for_nested():
	for r in all_renderers:
		yield eq, '[(1)(2)][(3)(4)]', r('<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>', data=[[1, 2], [3, 4]])


@py.test.mark.ul4
def test_for_unpacking():
	data = [
		("spam", "eggs", 17),
		("gurk", "hurz", 23),
		("hinz", "kunz", 42)
	]

	for r in all_renderers:
		yield eq, '(spam)(gurk)(hinz)', r('<?for (a,) in data?>(<?print a?>)<?end for?>', data=[item[:1] for item in data])
		yield eq, '(spam,eggs)(gurk,hurz)(hinz,kunz)', r('<?for (a, b) in data?>(<?print a?>,<?print b?>)<?end for?>', data=[item[:2] for item in data])
		yield eq, '(spam,eggs,17)(gurk,hurz,23)(hinz,kunz,42)', r('<?for (a, b, c) in data?>(<?print a?>,<?print b?>,<?print c?>)<?end for?>', data=data)


@py.test.mark.ul4
def test_break():
	for r in all_renderers:
		yield eq, '1, 2, ', r('<?for i in [1,2,3]?><?print i?>, <?if i==2?><?break?><?end if?><?end for?>')


@py.test.mark.ul4
def test_break_nested():
	for r in all_renderers:
		yield eq, '1, 1, 2, 1, 2, 3, ', r('<?for i in [1,2,3,4]?><?for j in [1,2,3,4]?><?print j?>, <?if j>=i?><?break?><?end if?><?end for?><?if i>=3?><?break?><?end if?><?end for?>')


@py.test.mark.ul4
def test_continue():
	for r in all_renderers:
		yield eq, '1, 3, ', r('<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?print i?>, <?end for?>')


@py.test.mark.ul4
def test_continue_nested():
	for r in all_renderers:
		yield eq, '1, 3, \n1, 3, \n', r('<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?for j in [1,2,3]?><?if j==2?><?continue?><?end if?><?print j?>, <?end for?>\n<?end for?>')


@py.test.mark.ul4
def test_if():
	for r in all_renderers:
		yield eq, '42', r('<?if data?><?print data?><?end if?>', data=42)


@py.test.mark.ul4
def test_else():
	for r in all_renderers:
		yield eq, '42', r('<?if data?><?print data?><?else?>no<?end if?>', data=42)
		yield eq, 'no', r('<?if data?><?print data?><?else?>no<?end if?>', data=0)


@py.test.mark.ul4
def test_block_errors():
	yield raises, "BlockError: block unclosed", RenderPython('<?for x in data?>')
	yield raises, "BlockError: endif doesn't match any if", RenderPython('<?for x in data?><?end if?>')
	yield raises, "BlockError: not in any block", RenderPython('<?end?>')
	yield raises, "BlockError: not in any block", RenderPython('<?end for?>')
	yield raises, "BlockError: not in any block", RenderPython('<?end if?>')
	yield raises, "BlockError: else doesn't match any if", RenderPython('<?else?>')
	yield raises, "BlockError: block unclosed", RenderPython('<?if data?>')
	yield raises, "BlockError: block unclosed", RenderPython('<?if data?><?else?>')
	yield raises, "BlockError: else already seen in if", RenderPython('<?if data?><?else?><?else?>')
	yield raises, "BlockError: else already seen in if", RenderPython('<?if data?><?else?><?elif data?>')
	yield raises, "BlockError: else already seen in if", RenderPython('<?if data?><?elif data?><?elif data?><?else?><?elif data?>')


@py.test.mark.ul4
def test_empty():
	yield raises, "expression required", RenderPython('<?print?>')
	yield raises, "expression required", RenderPython('<?if?>')
	yield raises, "expression required", RenderPython('<<?if x?><?elif?><?end if?>')
	yield raises, "loop expression required", RenderPython('<?for?>')
	yield raises, "statement required", RenderPython('<?code?>')
	yield raises, "expression required", RenderPython('<?render?>')


@py.test.mark.ul4
def test_add():
	values = (17, 23, 1., -1.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield evaleq, x + y, r('<?print x + y?>', x=x, y=y) # Using ``evaleq`` avoids problem with the nonexistant int/float distinction in JS
		yield eq, 'foobar', r('<?code x="foo"?><?code y="bar"?><?print x+y?>')
		yield eq, '(f)(o)(o)(b)(a)(r)', r('<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>', data=dict(foo="foo", bar="bar"))


@py.test.mark.ul4
def test_sub():
	values = (17, 23, 1., -1.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield evaleq, x - y, r('<?print x - y?>', x=x, y=y)


@py.test.mark.ul4
def test_mul():
	values = (17, 23, 1., -1.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield evaleq, x * y, r('<?print x * y?>', x=x, y=y)
		yield eq, 17*"foo", r('<?print 17*"foo"?>')
		yield eq, 17*"foo", r('<?code x=17?><?code y="foo"?><?print x*y?>')
		yield eq, "foo"*17, r('<?code x="foo"?><?code y=17?><?print x*y?>')
		yield eq, "foo"*17, r('<?print "foo"*17?>')
		yield eq, "(foo)(bar)(foo)(bar)(foo)(bar)", r('<?for i in 3*data?>(<?print i?>)<?end for?>', data=["foo", "bar"])


@py.test.mark.ul4
def test_truediv():
	for r in all_renderers:
		yield eq, "0.5", r('<?print 1/2?>')
		yield eq, "0.5", r('<?code x=1?><?code y=2?><?print x/y?>')


@py.test.mark.ul4
def test_floordiv():
	for r in all_renderers:
		yield eq, "0", r('<?print 1//2?>')
		yield eq, "0", r('<?code x=1?><?code y=2?><?print x//y?>')


@py.test.mark.ul4
def test_mod():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield evaleq, x % y, r('<?print {} % {}?>'.format(x, y))
				yield evaleq, x % y, r('<?print x % y?>', x=x, y=y)


@py.test.mark.ul4
def test_eq():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x == y), r('<?print {} == {}?>'.format(x, y))
				yield eq, str(x == y), r('<?print x == y?>', x=x, y=y)


@py.test.mark.ul4
def test_ne():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x != y), r('<?print {} != {}?>'.format(x, y))
				yield eq, str(x != y), r('<?print x != y?>', x=x, y=y)


@py.test.mark.ul4
def test_lt():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x < y), r('<?print {} < {}?>'.format(x, y))
				yield eq, str(x < y), r('<?print x < y?>', x=x, y=y)


@py.test.mark.ul4
def test_le():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x <= y), r('<?print {} <= {}?>'.format(x, y))
				yield eq, str(x <= y), r('<?print x <= y?>', x=x, y=y)


@py.test.mark.ul4
def test_gt():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x > y), r('<?print {} > {}?>'.format(x, y))
				yield eq, str(x > y), r('<?print x > y?>', x=x, y=y)


@py.test.mark.ul4
def test_ge():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x >= y), r('<?print {} >= {}?>'.format(x, y))
				yield eq, str(x >= y), r('<?print x >= y?>', x=x, y=y)


@py.test.mark.ul4
def test_contains():
	code = '<?print x in y?>'

	for r in all_renderers:
		yield eq, "True", r(code, x=2, y=[1, 2, 3])
		yield eq, "False", r(code, x=4, y=[1, 2, 3])
		yield eq, "True", r(code, x="ur", y="gurk")
		yield eq, "False", r(code, x="un", y="gurk")
		yield eq, "True", r(code, x="a", y={"a": 1, "b": 2})
		yield eq, "False", r(code, x="c", y={"a": 1, "b": 2})
		yield eq, "True", r(code, x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42))
		yield eq, "False", r(code, x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42))


@py.test.mark.ul4
def test_notcontains():
	code = '<?print x not in y?>'

	for r in all_renderers:
		yield eq, "False", r(code, x=2, y=[1, 2, 3])
		yield eq, "True", r(code, x=4, y=[1, 2, 3])
		yield eq, "False", r(code, x="ur", y="gurk")
		yield eq, "True", r(code, x="un", y="gurk")
		yield eq, "False", r(code, x="a", y={"a": 1, "b": 2})
		yield eq, "True", r(code, x="c", y={"a": 1, "b": 2})
		yield eq, "False", r(code, x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42))
		yield eq, "True", r(code, x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42))


@py.test.mark.ul4
def test_and():
	for r in all_renderers:
		yield eq, "False", r('<?print x and y?>', x=False, y=False)
		yield eq, "False", r('<?print x and y?>', x=False, y=True)
		yield eq, "0", r('<?print x and y?>', x=0, y=True)


@py.test.mark.ul4
def test_or():
	for r in all_renderers:
		yield eq, "False", r('<?print x or y?>', x=False, y=False)
		yield eq, "True", r('<?print x or y?>', x=False, y=True)
		yield eq, "42", r('<?print x or y?>', x=42, y=True)


@py.test.mark.ul4
def test_not():
	for r in all_renderers:
		yield eq, "True", r('<?print not x?>', x=False)
		yield eq, "False", r('<?print not x?>', x=42)


@py.test.mark.ul4
def test_getitem():
	for r in all_renderers:
		yield eq, "u", r("<?print 'gurk'[1]?>")
		yield eq, "u", r("<?print x[1]?>", x="gurk")
		yield eq, "u", r("<?print 'gurk'[-3]?>")
		yield eq, "u", r("<?print x[-3]?>", x="gurk")
		yield raises, "index out of range|IndexError", r("<?print 'gurk'[4]?>")
		yield raises, "index (4 )?out of range", r("<?print x[4]?>", x="gurk")
		yield raises, "index out of range|IndexError", r("<?print 'gurk'[-5]?>")
		yield raises, "index (-5 )?out of range", r("<?print x[-5]?>", x="gurk")


@py.test.mark.ul4
def test_getslice12():
	for r in all_renderers:
		yield eq, "ur", r("<?print 'gurk'[1:3]?>")
		yield eq, "ur", r("<?print x[1:3]?>", x="gurk")
		yield eq, "ur", r("<?print 'gurk'[-3:-1]?>")
		yield eq, "ur", r("<?print x[-3:-1]?>", x="gurk")
		yield eq, "", r("<?print 'gurk'[4:10]?>")
		yield eq, "", r("<?print x[4:10]?>", x="gurk")
		yield eq, "", r("<?print 'gurk'[-10:-5]?>")
		yield eq, "", r("<?print x[-10:-5]?>", x="gurk")


@py.test.mark.ul4
def test_getslice1():
	for r in all_renderers:
		yield eq, "urk", r("<?print 'gurk'[1:]?>")
		yield eq, "urk", r("<?print x[1:]?>", x="gurk")
		yield eq, "urk", r("<?print 'gurk'[-3:]?>")
		yield eq, "urk", r("<?print x[-3:]?>", x="gurk")
		yield eq, "", r("<?print 'gurk'[4:]?>")
		yield eq, "", r("<?print x[4:]?>", x="gurk")
		yield eq, "gurk", r("<?print 'gurk'[-10:]?>")
		yield eq, "gurk", r("<?print x[-10:]?>", x="gurk")


@py.test.mark.ul4
def test_getslice2():
	for r in all_renderers:
		yield eq, "gur", r("<?print 'gurk'[:3]?>")
		yield eq, "gur", r("<?print x[:3]?>", x="gurk")
		yield eq, "gur", r("<?print 'gurk'[:-1]?>")
		yield eq, "gur", r("<?print x[:-1]?>", x="gurk")
		yield eq, "gurk", r("<?print 'gurk'[:10]?>")
		yield eq, "gurk", r("<?print x[:10]?>", x="gurk")
		yield eq, "", r("<?print 'gurk'[:-5]?>")
		yield eq, "", r("<?print x[:-5]?>", x="gurk")


@py.test.mark.ul4
def test_getslice():
	for r in all_renderers:
		yield eq, "gurk", r("<?print 'gurk'[:]?>")
		yield eq, "gurk", r("<?print x[:]?>", x="gurk")
		yield eq, "[1, 2]", r("<?print x[:]?>", x=[1, 2])


@py.test.mark.ul4
def test_nested():
	sc = "4"
	sv = "x"
	n = 4
	# when using 10 compiling the variable will run out of registers
	# when using 8 Java will output "An irrecoverable stack overflow has occurred"
	depth = 7
	for i in range(depth):
		sc = "({})+({})".format(sc, sc)
		sv = "({})+({})".format(sv, sv)
		n = n + n

	for r in all_renderers:
		yield eq, str(n), r('<?print {}?>'.format(sc))
		yield eq, str(n), r('<?code x=4?><?print {}?>'.format(sv))


@py.test.mark.ul4
def test_precedence():
	for r in all_renderers:
		yield eq, "14", r('<?print 2+3*4?>')
		yield eq, "20", r('<?print (2+3)*4?>')
		yield eq, "10", r('<?print -2+-3*-4?>')
		yield eq, "14", r('<?print --2+--3*--4?>')
		yield eq, "14", r('<?print (-(-2))+(-((-3)*-(-4)))?>')
		yield eq, "42", r('<?print 2*data.value?>', data=dict(value=21))
		yield eq, "42", r('<?print data.value[0]?>', data=dict(value=[42]))
		yield eq, "42", r('<?print data[0].value?>', data=[dict(value=42)])
		yield eq, "42", r('<?print data[0][0][0]?>', data=[[[42]]])
		yield eq, "42", r('<?print data.value.value[0]?>', data=dict(value=dict(value=[42])))
		yield eq, "42", r('<?print data.value.value[0].value.value[0]?>', data=dict(value=dict(value=[dict(value=dict(value=[42]))])))

@py.test.mark.ul4
def test_associativity():
	for r in all_renderers:
		yield eq, "9", r('<?print 2+3+4?>')
		yield eq, "-5", r('<?print 2-3-4?>')
		yield eq, "24", r('<?print 2*3*4?>')
		if r is not RenderJS:
			yield eq, "2.0", r('<?print 24/6/2?>')
			yield eq, "2", r('<?print 24//6//2?>')
		else:
			yield evaleq, 2.0, r('<?print 24/6/2?>')
			yield evaleq, 2, r('<?print 24//6//2?>')

@py.test.mark.ul4
def test_bracket():
	sc = "4"
	sv = "x"
	for i in range(10):
		sc = "({})".format(sc)
		sv = "({})".format(sv)

	for r in all_renderers:
		yield eq, "4", r('<?print {}?>'.format(sc))
		yield eq, "4", r('<?code x=4?><?print {}?>'.format(sv))


@py.test.mark.ul4
def test_function_now():
	now = str(datetime.datetime.now())

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print now(1)?>")
		yield raises, argumentmismatchmessage, r("<?print now(1, 2)?>")
		yield le, now, r("<?print now()?>")


@py.test.mark.ul4
def test_function_utcnow():
	utcnow = str(datetime.datetime.utcnow())

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print utcnow(1)?>")
		yield raises, argumentmismatchmessage, r("<?print utcnow(1, 2)?>")
		utcnowfromtemplate = r("<?print utcnow()?>")
		# JS and Java only have milliseconds precision, but this shouldn't lead to problems here, as rendering the template takes longer than a millisecond
		yield le, utcnow, utcnowfromtemplate


@py.test.mark.ul4
def test_function_vars():
	code = "<?if var in vars()?>yes<?else?>no<?end if?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print vars(1)?>")
		yield raises, argumentmismatchmessage, r("<?print vars(1, 2)?>")
		yield eq, "yes", r(code, var="spam", spam="eggs")
		yield eq, "no", r(code, var="nospam", spam="eggs")


@py.test.mark.ul4
def test_function_random():
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print random(1)?>")
		yield raises, argumentmismatchmessage, r("<?print random(1, 2)?>")
		yield eq, "ok", r("<?code r = random()?><?if r>=0 and r<1?>ok<?else?>fail<?end if?>")


@py.test.mark.ul4
def test_function_randrange():
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print randrange()?>")
		yield eq, "ok", r("<?code r = randrange(4)?><?if r>=0 and r<4?>ok<?else?>fail<?end if?>")
		yield eq, "ok", r("<?code r = randrange(17, 23)?><?if r>=17 and r<23?>ok<?else?>fail<?end if?>")
		yield eq, "ok", r("<?code r = randrange(17, 23, 2)?><?if r>=17 and r<23 and r%2?>ok<?else?>fail<?end if?>")


@py.test.mark.ul4
def test_function_randchoice():
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print randchoice()?>")
		yield eq, "ok", r("<?code r = randchoice('abc')?><?if r in 'abc'?>ok<?else?>fail<?end if?>")
		yield eq, "ok", r("<?code s = [17, 23, 42]?><?code r = randchoice(s)?><?if r in s?>ok<?else?>fail<?end if?>")
		yield eq, "ok", r("<?code s = #12345678?><?code sl = [0x12, 0x34, 0x56, 0x78]?><?code r = randchoice(s)?><?if r in sl?>ok<?else?>fail<?end if?>")


@py.test.mark.ul4
def test_function_xmlescape():
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print xmlescape()?>")
		yield raises, argumentmismatchmessage, r("<?print xmlescape(1, 2)?>")
		yield eq, "&lt;&lt;&gt;&gt;&amp;&#39;&quot;gurk", r("<?print xmlescape(data)?>", data='<<>>&\'"gurk')


@py.test.mark.ul4
def test_function_csv():
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print csv()?>")
		yield raises, argumentmismatchmessage, r("<?print csv(1, 2)?>")
		yield eq, "", r("<?print csv(data)?>", data=None)
		yield eq, "False", r("<?print csv(data)?>", data=False)
		yield eq, "True", r("<?print csv(data)?>", data=True)
		yield eq, "42", r("<?print csv(data)?>", data=42)
		# no check for float
		yield eq, "abc", r("<?print csv(data)?>", data="abc")
		yield eq, '"a,b,c"', r("<?print csv(data)?>", data="a,b,c")
		yield eq, '"a""b""c"', r("<?print csv(data)?>", data='a"b"c')
		yield eq, '"a\nb\nc"', r("<?print csv(data)?>", data="a\nb\nc")


@py.test.mark.ul4
def test_function_asjson():
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print asjson()?>")
		yield raises, argumentmismatchmessage, r("<?print asjson(1, 2)?>")
		yield eq, "null", r("<?print asjson(data)?>", data=None)
		yield eq, "false", r("<?print asjson(data)?>", data=False)
		yield eq, "true", r("<?print asjson(data)?>", data=True)
		yield eq, "42", r("<?print asjson(data)?>", data=42)
		# no check for float
		yield eq, '"abc"', r("<?print asjson(data)?>", data="abc")
		yield eq, '[1, 2, 3]', r("<?print asjson(data)?>", data=[1, 2, 3])
		yield eq, '[1, 2, 3]', r("<?print asjson(data)?>", data=PseudoList([1, 2, 3]))
		yield eq, '{"one": 1}', r("<?print asjson(data)?>", data={"one": 1})
		yield eq, '{"one": 1}', r("<?print asjson(data)?>", data=PseudoDict({"one": 1}))


@py.test.mark.ul4
def test_function_fromjson():
	code = "<?print repr(fromjson(data))?>"
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print fromjson()?>")
		yield raises, argumentmismatchmessage, r("<?print fromjson(1, 2)?>")
		yield eq, "None", r(code, data="null")
		yield eq, "False", r(code, data="false")
		yield eq, "True", r(code, data="true")
		yield eq, "42", r(code, data="42")
		# no check for float
		yield contains, ('"abc"', "'abc'"), r(code, data='"abc"')
		yield eq, '[1, 2, 3]', r(code, data="[1, 2, 3]")
		yield contains, ('{"one": 1}', "{'one': 1}"), r(code, data='{"one": 1}')


@py.test.mark.ul4
def test_function_ul4on():
	code = "<?print repr(fromul4on(asul4on(data)))?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print asul4on()?>")
		yield raises, argumentmismatchmessage, r("<?print asul4on(1, 2)?>")
		yield raises, argumentmismatchmessage, r("<?print fromul4on()?>")
		yield raises, argumentmismatchmessage, r("<?print fromul4on(1, 2)?>")
		yield eq, "None", r(code, data=None)
		yield eq, "False", r(code, data=False)
		yield eq, "True", r(code, data=True)
		yield eq, "42", r(code, data=42)
		# no check for float
		yield contains, ('"abc"', "'abc'"), r(code, data="abc")
		yield eq, '[1, 2, 3]', r(code, data=[1, 2, 3])
		yield contains, ('{"one": 1}', "{'one': 1}"), r(code, data={'one': 1})


@py.test.mark.ul4
def test_function_str():
	code = "<?print str(data)?>"
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print str(1, 2)?>")
		yield eq, "", r("<?print str()?>")
		yield eq, "", r(code, data=None)
		yield eq, "True", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "42", r(code, data=42)
		yield eq, "4.2", r(code, data=4.2)
		yield eq, "foo", r(code, data="foo")
		yield eq, "2011-02-09", r(code, data=datetime.date(2011, 2, 9))
		yield eq, "2011-02-09 12:34:56", r(code, data=datetime.datetime(2011, 2, 9, 12, 34, 56))
		yield eq, "2011-02-09 12:34:56.987000", r(code, data=datetime.datetime(2011, 2, 9, 12, 34, 56, 987000))


@py.test.mark.ul4
def test_function_int():
	for r in all_renderers:
		yield raises, argumentmismatchmessage, RenderPython("<?print int(1, 2, 3)?>")
		yield raises, "int\\(\\) argument must be a string or a number|int\\(null\\) not supported", RenderPython("<?print int(data)?>", data=None)
		yield raises, "invalid literal for int|NumberFormatException", RenderPython("<?print int(data)?>", data="foo")
		yield eq, "0", r("<?print int()?>")
		yield eq, "1", r("<?print int(data)?>", data=True)
		yield eq, "0", r("<?print int(data)?>", data=False)
		yield eq, "42", r("<?print int(data)?>", data=42)
		yield eq, "4", r("<?print int(data)?>", data=4.2)
		yield eq, "42", r("<?print int(data)?>", data="42")
		yield eq, "66", r("<?print int(data, 16)?>", data="42")


@py.test.mark.ul4
def test_function_float():
	code = "<?print float(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print float(1, 2, 3)?>")
		yield raises, "float\\(\\) argument must be a string or a number|float\\(null\\) not supported", r(code, data=None)
		yield eq, "4.2", r(code, data=4.2)
		if r is not RenderJS:
			yield eq, "0.0", r("<?print float()?>")
			yield eq, "1.0", r(code, data=True)
			yield eq, "0.0", r(code, data=False)
			yield eq, "42.0", r(code, data=42)
			yield eq, "42.0", r(code, data="42")
		else:
			yield evaleq, 0.0, r("<?print float()?>")
			yield evaleq, 1.0, r(code, data=True)
			yield evaleq, 0.0, r(code, data=False)
			yield evaleq, 42.0, r(code, data=42)
			yield evaleq, 42.0, r(code, data="42")


@py.test.mark.ul4
def test_function_len():
	code = "<?print len(data)?>"
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print len()?>")
		yield raises, argumentmismatchmessage, r("<?print len(1, 2)?>")
		yield raises, "has no len\\(\\)|len\\(.*\\) not supported", r(code, data=None)
		yield raises, "has no len\\(\\)|len\\(.*\\) not supported", r(code, data=True)
		yield raises, "has no len\\(\\)|len\\(.*\\) not supported", r(code, data=False)
		yield raises, "has no len\\(\\)|len\\(.*\\) not supported", r(code, data=42)
		yield raises, "has no len\\(\\)|len\\(.*\\) not supported", r(code, data=4.2)
		yield eq, "42", r(code, data=42*"?")
		yield eq, "42", r(code, data=42*[None])
		yield eq, "42", r(code, data=dict.fromkeys(range(42)))


@py.test.mark.ul4
def test_function_enumerate():
	code1 = "<?for (i, value) in enumerate(data)?>(<?print value?>=<?print i?>)<?end for?>"
	code2 = "<?for (i, value) in enumerate(data, 42)?>(<?print value?>=<?print i?>)<?end for?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print enumerate()?>")
		yield raises, argumentmismatchmessage, r("<?print enumerate(1, 2, 3)?>")
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code1, data=None)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code1, data=True)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code1, data=False)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code1, data=42)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code1, data=4.2)
		yield eq, "(f=0)(o=1)(o=2)", r(code1, data="foo")
		yield eq, "(foo=0)(bar=1)", r(code1, data=["foo", "bar"])
		yield eq, "(foo=0)", r(code1, data=dict(foo=True))
		yield eq, "", r(code1, data="")
		yield eq, "(f=42)(o=43)(o=44)", r(code2, data="foo")


@py.test.mark.ul4
def test_function_enumfl():
	code1 = "<?for (i, f, l, value) in enumfl(data)?><?if f?>[<?end if?>(<?print value?>=<?print i?>)<?if l?>]<?end if?><?end for?>"
	code2 = "<?for (i, f, l, value) in enumfl(data, 42)?><?if f?>[<?end if?>(<?print value?>=<?print i?>)<?if l?>]<?end if?><?end for?>"
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print enumfl()?>")
		yield raises, argumentmismatchmessage, r("<?print enumfl(1, 2, 3)?>")
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code1, data=None)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code1, data=True)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code1, data=False)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code1, data=42)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code1, data=4.2)
		yield eq, "[(f=0)(o=1)(o=2)]", r(code1, data="foo")
		yield eq, "[(foo=0)(bar=1)]", r(code1, data=["foo", "bar"])
		yield eq, "[(foo=0)]", r(code1, data=dict(foo=True))
		yield eq, "", r(code1, data="")
		yield eq, "[(f=42)(o=43)(o=44)]", r(code2, data="foo")


@py.test.mark.ul4
def test_function_isfirstlast():
	code = "<?for (f, l, value) in isfirstlast(data)?><?if f?>[<?end if?>(<?print value?>)<?if l?>]<?end if?><?end for?>"
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print isfirstlast()?>")
		yield raises, argumentmismatchmessage, r("<?print isfirstlast(1, 2)?>")
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=None)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=True)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=False)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=42)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=4.2)
		yield eq, "[(f)(o)(o)]", r(code, data="foo")
		yield eq, "[(foo)(bar)]", r(code, data=["foo", "bar"])
		yield eq, "[(foo)]", r(code, data=dict(foo=True))
		yield eq, "", r(code, data="")


@py.test.mark.ul4
def test_function_isfirst():
	code = "<?for (f, value) in isfirst(data)?><?if f?>[<?end if?>(<?print value?>)<?end for?>"
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print isfirst()?>")
		yield raises, argumentmismatchmessage, r("<?print isfirst(1, 2)?>")
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=None)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=True)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=False)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=42)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=4.2)
		yield eq, "[(f)(o)(o)", r(code, data="foo")
		yield eq, "[(foo)(bar)", r(code, data=["foo", "bar"])
		yield eq, "[(foo)", r(code, data=dict(foo=True))
		yield eq, "", r(code, data="")


@py.test.mark.ul4
def test_function_islast():
	code = "<?for (l, value) in islast(data)?>(<?print value?>)<?if l?>]<?end if?><?end for?>"
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print islast()?>")
		yield raises, argumentmismatchmessage, r("<?print islast(1, 2)?>")
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=None)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=True)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=False)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=42)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=4.2)
		yield eq, "(f)(o)(o)]", r(code, data="foo")
		yield eq, "(foo)(bar)]", r(code, data=["foo", "bar"])
		yield eq, "(foo)]", r(code, data=dict(foo=True))
		yield eq, "", r(code, data="")


@py.test.mark.ul4
def test_function_isnone():
	code = "<?print isnone(data)?>"
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print isnone()?>")
		yield raises, argumentmismatchmessage, r("<?print isnone(1, 2)?>")
		yield eq, "True", r(code, data=None)
		yield eq, "False", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "False", r(code, data=42)
		yield eq, "False", r(code, data=4.2)
		yield eq, "False", r(code, data="foo")
		yield eq, "False", r(code, data=datetime.datetime.now())
		yield eq, "False", r(code, data=())
		yield eq, "False", r(code, data=[])
		yield eq, "False", r(code, data={})
		yield eq, "False", r(code, data=ul4c.Template(""))
		yield eq, "False", r(code, data=color.red)


@py.test.mark.ul4
def test_function_isbool():
	code = "<?print isbool(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print isbool()?>")
		yield raises, argumentmismatchmessage, r("<?print isbool(1, 2)?>")
		yield eq, "False", r(code, data=None)
		yield eq, "True", r(code, data=True)
		yield eq, "True", r(code, data=False)
		yield eq, "False", r(code, data=42)
		yield eq, "False", r(code, data=4.2)
		yield eq, "False", r(code, data="foo")
		yield eq, "False", r(code, data=datetime.datetime.now())
		yield eq, "False", r(code, data=())
		yield eq, "False", r(code, data=[])
		yield eq, "False", r(code, data={})
		yield eq, "False", r(code, data=ul4c.Template(""))
		yield eq, "False", r(code, data=color.red)


@py.test.mark.ul4
def test_function_isint():
	code = "<?print isint(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print isint()?>")
		yield raises, argumentmismatchmessage, r("<?print isint(1, 2)?>")
		yield eq, "False", r(code, data=None)
		yield eq, "False", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "True", r(code, data=42)
		yield eq, "False", r(code, data=4.2)
		yield eq, "False", r(code, data="foo")
		yield eq, "False", r(code, data=datetime.datetime.now())
		yield eq, "False", r(code, data=())
		yield eq, "False", r(code, data=[])
		yield eq, "False", r(code, data={})
		yield eq, "False", r(code, data=ul4c.Template(""))
		yield eq, "False", r(code, data=color.red)


@py.test.mark.ul4
def test_function_isfloat():
	code = "<?print isfloat(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print isfloat()?>")
		yield raises, argumentmismatchmessage, r("<?print isfloat(1, 2)?>")
		yield eq, "False", r(code, data=None)
		yield eq, "False", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "False", r(code, data=42)
		yield eq, "True", r(code, data=4.2)
		yield eq, "False", r(code, data="foo")
		yield eq, "False", r(code, data=datetime.datetime.now())
		yield eq, "False", r(code, data=())
		yield eq, "False", r(code, data=[])
		yield eq, "False", r(code, data={})
		yield eq, "False", r(code, data=ul4c.Template(""))
		yield eq, "False", r(code, data=color.red)


@py.test.mark.ul4
def test_function_isstr():
	code = "<?print isstr(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print isstr()?>")
		yield raises, argumentmismatchmessage, r("<?print isstr(1, 2)?>")
		yield eq, "False", r(code, data=None)
		yield eq, "False", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "False", r(code, data=42)
		yield eq, "False", r(code, data=4.2)
		yield eq, "True", r(code, data="foo")
		yield eq, "False", r(code, data=datetime.datetime.now())
		yield eq, "False", r(code, data=())
		yield eq, "False", r(code, data=[])
		yield eq, "False", r(code, data={})
		yield eq, "False", r(code, data=ul4c.Template(""))
		yield eq, "False", r(code, data=color.red)


@py.test.mark.ul4
def test_function_isdate():
	code = "<?print isdate(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print isdate()?>")
		yield raises, argumentmismatchmessage, r("<?print isdate(1, 2)?>")
		yield eq, "False", r(code, data=None)
		yield eq, "False", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "False", r(code, data=42)
		yield eq, "False", r(code, data=4.2)
		yield eq, "False", r(code, data="foo")
		yield eq, "True", r(code, data=datetime.datetime.now())
		yield eq, "False", r(code, data=())
		yield eq, "False", r(code, data=[])
		yield eq, "False", r(code, data={})
		yield eq, "False", r(code, data=ul4c.Template(""))
		yield eq, "False", r(code, data=color.red)


@py.test.mark.ul4
def test_function_islist():
	code = "<?print islist(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print islist()?>")
		yield raises, argumentmismatchmessage, r("<?print islist(1, 2)?>")
		yield eq, "False", r(code, data=None)
		yield eq, "False", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "False", r(code, data=42)
		yield eq, "False", r(code, data=4.2)
		yield eq, "False", r(code, data="foo")
		yield eq, "False", r(code, data=datetime.datetime.now())
		yield eq, "True", r(code, data=())
		yield eq, "True", r(code, data=[])
		yield eq, "True", r(code, data=PseudoList([]))
		yield eq, "False", r(code, data={})
		yield eq, "False", r(code, data=ul4c.Template(""))
		yield eq, "False", r(code, data=color.red)


@py.test.mark.ul4
def test_function_isdict():
	code = "<?print isdict(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print isdict()?>")
		yield raises, argumentmismatchmessage, r("<?print isdict(1, 2)?>")
		yield eq, "False", r(code, data=None)
		yield eq, "False", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "False", r(code, data=42)
		yield eq, "False", r(code, data=4.2)
		yield eq, "False", r(code, data="foo")
		yield eq, "False", r(code, data=datetime.datetime.now())
		yield eq, "False", r(code, data=())
		yield eq, "False", r(code, data=[])
		yield eq, "True", r(code, data={})
		yield eq, "True", r(code, data=PseudoDict({}))
		yield eq, "False", r(code, data=ul4c.Template(""))
		yield eq, "False", r(code, data=color.red)


@py.test.mark.ul4
def test_function_istemplate():
	code = "<?print istemplate(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print istemplate()?>")
		yield raises, argumentmismatchmessage, r("<?print istemplate(1, 2)?>")
		yield eq, "False", r(code, data=None)
		yield eq, "False", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "False", r(code, data=42)
		yield eq, "False", r(code, data=4.2)
		yield eq, "False", r(code, data="foo")
		yield eq, "False", r(code, data=datetime.datetime.now())
		yield eq, "False", r(code, data=())
		yield eq, "False", r(code, data=[])
		yield eq, "False", r(code, data={})
		yield eq, "True", r(code, data=ul4c.Template(""))
		yield eq, "False", r(code, data=color.red)


@py.test.mark.ul4
def test_function_iscolor():
	code = "<?print iscolor(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print iscolor()?>")
		yield raises, argumentmismatchmessage, r("<?print iscolor(1, 2)?>")
		yield eq, "False", r(code, data=None)
		yield eq, "False", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "False", r(code, data=42)
		yield eq, "False", r(code, data=4.2)
		yield eq, "False", r(code, data="foo")
		yield eq, "False", r(code, data=datetime.datetime.now())
		yield eq, "False", r(code, data=())
		yield eq, "False", r(code, data=[])
		yield eq, "False", r(code, data={})
		yield eq, "False", r(code, data=ul4c.Template(""))
		yield eq, "True", r(code, data=color.red)


@py.test.mark.ul4
def test_function_get():
	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print get()?>")
		yield eq, "", r("<?print get('x')?>")
		yield eq, "42", r("<?print get('x')?>", x=42)
		yield eq, "17", r("<?print get('x', 17)?>")
		yield eq, "42", r("<?print get('x', 17)?>", x=42)


@py.test.mark.ul4
def test_function_repr():
	code = "<?print repr(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print repr()?>")
		yield raises, argumentmismatchmessage, r("<?print repr(1, 2)?>")
		yield eq, "None", r(code, data=None)
		yield eq, "True", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "42", r(code, data=42)
		yield evaleq, 42.5, r(code, data=42.5)
		yield contains, ('"foo"', "'foo'"), r(code, data="foo")
		yield evaleq, [1, 2, 3], r(code, data=[1, 2, 3])
		if r is not RenderJS:
			yield evaleq, [1, 2, 3], r(code, data=(1, 2, 3))
		yield evaleq, {"a": 1, "b": 2}, r(code, data={"a": 1, "b": 2})
		yield eq, "@(2011-02-07T12:34:56.123000)", r(code, data=datetime.datetime(2011, 2, 7, 12, 34, 56, 123000))
		yield eq, "@(2011-02-07T12:34:56)", r(code, data=datetime.datetime(2011, 2, 7, 12, 34, 56))
		yield eq, "@(2011-02-07)", r(code, data=datetime.datetime(2011, 2, 7))
		yield eq, "@(2011-02-07)", r(code, data=datetime.date(2011, 2, 7))


@py.test.mark.ul4
def test_method_format():
	t = datetime.datetime(2011, 2, 6, 12, 34, 56, 987000)
	code = "<?print format(data, format)?>"
	for r in all_renderers:
		yield eq, "2011", r(code, format="%Y", data=t)
		yield eq, "02", r(code, format="%m", data=t)
		yield eq, "06", r(code, format="%d", data=t)
		yield eq, "12", r(code, format="%H", data=t)
		yield eq, "34", r(code, format="%M", data=t)
		yield eq, "56", r(code, format="%S", data=t)
		yield eq, "987000", r(code, format="%f", data=t)
		yield contains, ("Sun", "So"), r(code, format="%a", data=t)
		yield contains, ("Sunday", "Sonntag"), r(code, format="%A", data=t)
		yield eq, "Feb", r(code, format="%b", data=t)
		yield contains, ("February", "Februar"), r(code, format="%B", data=t)
		yield eq, "12", r(code, format="%I", data=t)
		yield eq, "037", r(code, format="%j", data=t)
		yield eq, "PM", r(code, format="%p", data=t)
		yield eq, "06", r(code, format="%U", data=t)
		yield eq, "0", r(code, format="%w", data=t)
		yield eq, "05", r(code, format="%W", data=t)
		yield eq, "11", r(code, format="%y", data=t)
		yield contains, ("Sun Feb  6 12:34:56 2011", "So Feb  6 12:34:56 2011"), r(code, format="%c", data=t)
		yield eq, "02/06/11", r(code, format="%x", data=t)
		yield eq, "12:34:56", r(code, format="%X", data=t)
		yield eq, "%", r(code, format="%%", data=t)


@py.test.mark.ul4
def test_function_chr():
	code = "<?print chr(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print chr()?>")
		yield raises, argumentmismatchmessage, r("<?print chr(1, 2)?>")
		yield eq, "\x00", r(code, data=0)
		yield eq, "a", r(code, data=ord("a"))
		yield eq, "\u20ac", r(code, data=0x20ac)


@py.test.mark.ul4
def test_function_ord():
	code = "<?print ord(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print ord()?>")
		yield raises, argumentmismatchmessage, r("<?print ord(1, 2)?>")
		yield eq, "0", r(code, data="\x00")
		yield eq, str(ord("a")), r(code, data="a")
		yield eq, str(0x20ac), r(code, data="\u20ac")


@py.test.mark.ul4
def test_function_hex():
	code = "<?print hex(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print hex()?>")
		yield raises, argumentmismatchmessage, r("<?print hex(1, 2)?>")
		yield eq, "0x0", r(code, data=0)
		yield eq, "0xff", r(code, data=0xff)
		yield eq, "0xffff", r(code, data=0xffff)
		yield eq, "-0xffff", r(code, data=-0xffff)


@py.test.mark.ul4
def test_function_oct():
	code = "<?print oct(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print oct()?>")
		yield raises, argumentmismatchmessage, r("<?print oct(1, 2)?>")
		yield eq, "0o0", r(code, data=0)
		yield eq, "0o77", r(code, data=0o77)
		yield eq, "0o7777", r(code, data=0o7777)
		yield eq, "-0o7777", r(code, data=-0o7777)


@py.test.mark.ul4
def test_function_bin():
	code = "<?print bin(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print bin()?>")
		yield raises, argumentmismatchmessage, r("<?print bin(1, 2)?>")
		yield eq, "0b0", r(code, data=0b0)
		yield eq, "0b11", r(code, data=0b11)
		yield eq, "-0b1111", r(code, data=-0b1111)


@py.test.mark.ul4
def test_function_abs():
	code = "<?print abs(data)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print abs()?>")
		yield raises, argumentmismatchmessage, r("<?print abs(1, 2)?>")
		yield eq, "0", r(code, data=0)
		yield eq, "42", r(code, data=42)
		yield eq, "42", r(code, data=-42)


@py.test.mark.ul4
def test_function_sorted():
	code = "<?for i in sorted(data)?><?print i?><?end for?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print sorted()?>")
		yield eq, "gkru", r(code, data="gurk")
		yield eq, "24679", r(code, data="92746")
		yield eq, "172342", r(code, data=(42, 17, 23))
		yield eq, "012", r(code, data={0: "zero", 1: "one", 2: "two"})


@py.test.mark.ul4
def test_function_range():
	code1 = "<?for i in range(data)?><?print i?>;<?end for?>"
	code2 = "<?for i in range(data[0], data[1])?><?print i?>;<?end for?>"
	code3 = "<?for i in range(data[0], data[1], data[2])?><?print i?>;<?end for?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print range()?>")
		yield eq, "", r(code1, data=-10)
		yield eq, "", r(code1, data=0)
		yield eq, "0;", r(code1, data=1)
		yield eq, "0;1;2;3;4;", r(code1, data=5)
		yield eq, "", r(code2, data=[0, -10])
		yield eq, "", r(code2, data=[0, 0])
		yield eq, "0;1;2;3;4;", r(code2, data=[0, 5])
		yield eq, "-5;-4;-3;-2;-1;0;1;2;3;4;", r(code2, data=[-5, 5])
		yield eq, "", r(code3, data=[0, -10, 1])
		yield eq, "", r(code3, data=[0, 0, 1])
		yield eq, "0;2;4;6;8;", r(code3, data=[0, 10, 2])
		yield eq, "", r(code3, data=[0, 10, -2])
		yield eq, "10;8;6;4;2;", r(code3, data=[10, 0, -2])
		yield eq, "", r(code3, data=[10, 0, 2])


@py.test.mark.ul4
def test_function_urlquote():
	for r in all_renderers:
		yield eq, "gurk", r("<?print urlquote('gurk')?>")
		yield eq, "%3C%3D%3E%2B%3F", r("<?print urlquote('<=>+?')?>")
		yield eq, "%7F%C3%BF%EF%BF%BF", r("<?print urlquote('\u007f\u00ff\uffff')?>")


@py.test.mark.ul4
def test_function_urlunquote():
	for r in all_renderers:
		yield eq, "gurk", r("<?print urlunquote('gurk')?>")
		yield eq, "<=>+?", r("<?print urlunquote('%3C%3D%3E%2B%3F')?>")
		yield eq, "\u007f\u00ff\uffff", r("<?print urlunquote('%7F%C3%BF%EF%BF%BF')?>")


@py.test.mark.ul4
def test_function_zip():
	code0 = "<?for i in zip()?><?print i?>;<?end for?>"
	code1 = "<?for (ix, ) in zip(x)?><?print ix?>;<?end for?>"
	code2 = "<?for (ix, iy) in zip(x, y)?><?print ix?>-<?print iy?>;<?end for?>"
	code3 = "<?for (ix, iy, iz) in zip(x, y, z)?><?print ix?>-<?print iy?>+<?print iz?>;<?end for?>"

	for r in all_renderers:
		yield eq, "", r(code0)
		yield eq, "1;2;", r(code1, x=[1, 2])
		yield eq, "", r(code2, x=[], y=[])
		yield eq, "1-3;2-4;", r(code2, x=[1, 2], y=[3, 4])
		yield eq, "1-4;2-5;", r(code2, x=[1, 2, 3], y=[4, 5])
		yield eq, "", r(code3, x=[], y=[], z=[])
		yield eq, "1-3+5;2-4+6;", r(code3, x=[1, 2], y=[3, 4], z=[5, 6])
		yield eq, "1-4+6;", r(code3, x=[1, 2, 3], y=[4, 5], z=[6])


@py.test.mark.ul4
def test_function_type():
	code = "<?print type(x)?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print type()?>")
		yield raises, argumentmismatchmessage, r("<?print type(1, 2)?>")
		yield eq, "none", r(code, x=None)
		yield eq, "bool", r(code, x=False)
		yield eq, "bool", r(code, x=True)
		yield eq, "int", r(code, x=42)
		yield eq, "float", r(code, x=4.2)
		yield eq, "str", r(code, x="foo")
		yield eq, "date", r(code, x=datetime.datetime.now())
		yield eq, "date", r(code, x=datetime.date.today())
		yield eq, "list", r(code, x=(1, 2))
		yield eq, "list", r(code, x=[1, 2])
		yield eq, "list", r(code, x=PseudoList([1, 2]))
		yield eq, "dict", r(code, x={1: 2})
		yield eq, "dict", r(code, x=PseudoDict({1: 2}))
		yield eq, "template", r(code, x=ul4c.Template(""))
		yield eq, "color", r(code, x=color.red)


@py.test.mark.ul4
def test_function_reversed():
	code = "<?for i in reversed(x)?>(<?print i?>)<?end for?>"

	for r in all_renderers:
		yield raises, argumentmismatchmessage, r("<?print reversed()?>")
		yield raises, argumentmismatchmessage, r("<?print reversed(1, 2)?>")
		yield eq, "(3)(2)(1)", r(code, x="123")
		yield eq, "(3)(2)(1)", r(code, x=[1, 2, 3])
		yield eq, "(3)(2)(1)", r(code, x=(1, 2, 3))


@py.test.mark.ul4
def test_function_rgb():
	for r in all_renderers:
		yield eq, "#369", r("<?print repr(rgb(0.2, 0.4, 0.6))?>")
		yield eq, "#369c", r("<?print repr(rgb(0.2, 0.4, 0.6, 0.8))?>")


@py.test.mark.ul4
def test_function_hls():
	for r in all_renderers:
		yield eq, "#fff", r("<?print repr(hls(0, 1, 0))?>")
		yield eq, "#fff0", r("<?print repr(hls(0, 1, 0, 0))?>")


@py.test.mark.ul4
def test_function_hsv():
	for r in all_renderers:
		yield eq, "#fff", r("<?print repr(hsv(0, 0, 1))?>")
		yield eq, "#fff0", r("<?print repr(hsv(0, 0, 1, 0))?>")


@py.test.mark.ul4
def test_method_upper():
	for r in all_renderers:
		yield eq, "GURK", r("<?print 'gurk'.upper()?>")


@py.test.mark.ul4
def test_method_lower():
	for r in all_renderers:
		yield eq, "gurk", r("<?print 'GURK'.lower()?>")


@py.test.mark.ul4
def test_method_capitalize():
	for r in all_renderers:
		yield eq, "Gurk", r("<?print 'gURK'.capitalize()?>")


@py.test.mark.ul4
def test_method_startswith():
	for r in all_renderers:
		yield eq, "True", r("<?print 'gurkhurz'.startswith('gurk')?>")
		yield eq, "False", r("<?print 'gurkhurz'.startswith('hurz')?>")


@py.test.mark.ul4
def test_method_endswith():
	for r in all_renderers:
		yield eq, "True", r("<?print 'gurkhurz'.endswith('hurz')?>")
		yield eq, "False", r("<?print 'gurkhurz'.endswith('gurk')?>")


@py.test.mark.ul4
def test_method_strip():
	for r in all_renderers:
		yield eq, "gurk", r(r"<?print obj.strip()?>", obj=' \t\r\ngurk \t\r\n')
		yield eq, "gurk", r(r"<?print obj.strip('xyz')?>", obj='xyzzygurkxyzzy')


@py.test.mark.ul4
def test_method_lstrip():
	for r in all_renderers:
		yield eq, "gurk \t\r\n", r("<?print obj.lstrip()?>", obj=" \t\r\ngurk \t\r\n")
		yield eq, "gurkxyzzy", r("<?print obj.lstrip(arg)?>", obj="xyzzygurkxyzzy", arg="xyz")


@py.test.mark.ul4
def test_method_rstrip():
	for r in all_renderers:
		yield eq, " \t\r\ngurk", r("<?print obj.rstrip()?>", obj=" \t\r\ngurk \t\r\n")
		yield eq, "xyzzygurk", r("<?print obj.rstrip(arg)?>", obj="xyzzygurkxyzzy", arg="xyz")


@py.test.mark.ul4
def test_method_split():
	for r in all_renderers:
		yield eq, "(f)(o)(o)", r("<?for item in obj.split()?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
		yield eq, "(f)(o \t\r\no \t\r\n)", r("<?for item in obj.split(None, 1)?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
		yield eq, "()(f)(o)(o)()", r("<?for item in obj.split(arg)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")
		yield eq, "()(f)(oxxoxx)", r("<?for item in obj.split(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")


@py.test.mark.ul4
def test_method_rsplit():
	for r in all_renderers:
		yield eq, "(f)(o)(o)", r("<?for item in obj.rsplit()?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
		yield eq, "( \t\r\nf \t\r\no)(o)", r("<?for item in obj.rsplit(None, 1)?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
		yield eq, "()(f)(o)(o)()", r("<?for item in obj.rsplit(arg)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")
		yield eq, "(xxfxxo)(o)()", r("<?for item in obj.rsplit(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")


@py.test.mark.ul4
def test_method_replace():
	for r in all_renderers:
		yield eq, 'goork', r(r"<?print 'gurk'.replace('u', 'oo')?>")


@py.test.mark.ul4
def test_method_renders():
	for r in all_renderers:
		t = ul4c.Template('(<?print data?>)')
		yield eq, '(GURK)', r("<?print t.renders(data='gurk').upper()?>", t=t)
		yield eq, '(GURK)', r("<?print t.renders(**{'data': 'gurk'}).upper()?>", t=t)

		t = ul4c.Template('(gurk)')
		yield eq, '(GURK)', r("<?print t.renders().upper()?>", t=t)


@py.test.mark.ul4
def test_method_mimeformat():
	t = datetime.datetime(2010, 2, 22, 12, 34, 56)
	for r in all_renderers:
		yield eq, 'Mon, 22 Feb 2010 12:34:56 GMT', r(r"<?print data.mimeformat()?>", data=t)


@py.test.mark.ul4
def test_method_get():
	for r in all_renderers:
		yield eq, "42", r("<?print {}.get('foo', 42)?>")
		yield eq, "17", r("<?print {'foo': 17}.get('foo', 42)?>")
		yield eq, "", r("<?print {}.get('foo')?>")
		yield eq, "17", r("<?print {'foo': 17}.get('foo')?>")


@py.test.mark.ul4
def test_method_r_g_b_a():
	for r in all_renderers:
		yield eq, '0x11', r('<?code c = #123?><?print hex(c.r())?>')
		yield eq, '0x22', r('<?code c = #123?><?print hex(c.g())?>')
		yield eq, '0x33', r('<?code c = #123?><?print hex(c.b())?>')
		yield eq, '0xff', r('<?code c = #123?><?print hex(c.a())?>')


@py.test.mark.ul4
def test_method_hls():
	for r in all_renderers:
		yield eq, '0', r('<?code c = #fff?><?print int(c.hls()[0])?>')
		yield eq, '1', r('<?code c = #fff?><?print int(c.hls()[1])?>')
		yield eq, '0', r('<?code c = #fff?><?print int(c.hls()[2])?>')


@py.test.mark.ul4
def test_method_hlsa():
	for r in all_renderers:
		yield eq, '0', r('<?code c = #fff?><?print int(c.hlsa()[0])?>')
		yield eq, '1', r('<?code c = #fff?><?print int(c.hlsa()[1])?>')
		yield eq, '0', r('<?code c = #fff?><?print int(c.hlsa()[2])?>')
		yield eq, '1', r('<?code c = #fff?><?print int(c.hlsa()[3])?>')


@py.test.mark.ul4
def test_method_hsv():
	for r in all_renderers:
		yield eq, '0', r('<?code c = #fff?><?print int(c.hsv()[0])?>')
		yield eq, '0', r('<?code c = #fff?><?print int(c.hsv()[1])?>')
		yield eq, '1', r('<?code c = #fff?><?print int(c.hsv()[2])?>')


@py.test.mark.ul4
def test_method_hsva():
	for r in all_renderers:
		yield eq, '0', r('<?code c = #fff?><?print int(c.hsva()[0])?>')
		yield eq, '0', r('<?code c = #fff?><?print int(c.hsva()[1])?>')
		yield eq, '1', r('<?code c = #fff?><?print int(c.hsva()[2])?>')
		yield eq, '1', r('<?code c = #fff?><?print int(c.hsva()[3])?>')


@py.test.mark.ul4
def test_method_lum():
	for r in all_renderers:
		yield eq, 'True', r('<?print #fff.lum() == 1?>')


@py.test.mark.ul4
def test_method_withlum():
	for r in all_renderers:
		yield eq, '#fff', r('<?print #000.withlum(1)?>')


@py.test.mark.ul4
def test_method_witha():
	for r in all_renderers:
		yield eq, '#0063a82a', r('<?print repr(#0063a8.witha(42))?>')


@py.test.mark.ul4
def test_method_join():
	for r in all_renderers:
		yield eq, '1,2,3,4', r('<?print ",".join("1234")?>')
		yield eq, '1,2,3,4', r('<?print ",".join([1, 2, 3, 4])?>')


@py.test.mark.ul4
def test_method_find():
	for r in all_renderers:
		yield eq, '-1', r('<?print s.find("ks")?>', s="gurkgurk")
		yield eq, '2', r('<?print s.find("rk")?>', s="gurkgurk")
		yield eq, '2', r('<?print s.find("rk", 2)?>', s="gurkgurk")
		yield eq, '2', r('<?print s.find("rk", 2, 4)?>', s="gurkgurk")
		yield eq, '6', r('<?print s.find("rk", 4, 8)?>', s="gurkgurk")
		yield eq, '-1', r('<?print s.find("rk", 2, 3)?>', s="gurkgurk")
		yield eq, '-1', r('<?print s.find("rk", 7)?>', s="gurkgurk")


@py.test.mark.ul4
def test_method_rfind():
	for r in all_renderers:
		yield eq, '-1', r('<?print s.rfind("ks")?>', s="gurkgurk")
		yield eq, '6', r('<?print s.rfind("rk")?>', s="gurkgurk")
		yield eq, '6', r('<?print s.rfind("rk", 2)?>', s="gurkgurk")
		yield eq, '2', r('<?print s.rfind("rk", 2, 4)?>', s="gurkgurk")
		yield eq, '6', r('<?print s.rfind("rk", 4, 8)?>', s="gurkgurk")
		yield eq, '-1', r('<?print s.rfind("rk", 2, 3)?>', s="gurkgurk")
		yield eq, '-1', r('<?print s.rfind("rk", 7)?>', s="gurkgurk")


@py.test.mark.ul4
def test_method_day():
	for r in all_renderers:
		yield eq, '12', r('<?print @(2010-05-12).day()?>')
		yield eq, '12', r('<?print d.day()?>', d=datetime.date(2010, 5, 12))


@py.test.mark.ul4
def test_method_month():
	for r in all_renderers:
		yield eq, '5', r('<?print @(2010-05-12).month()?>')
		yield eq, '5', r('<?print d.month()?>', d=datetime.date(2010, 5, 12))


@py.test.mark.ul4
def test_method_year():
	for r in all_renderers:
		yield eq, '5', r('<?print @(2010-05-12).month()?>')
		yield eq, '5', r('<?print d.month()?>', d=datetime.date(2010, 5, 12))


@py.test.mark.ul4
def test_method_hour():
	for r in all_renderers:
		yield eq, '16', r('<?print @(2010-05-12T16:47:56).hour()?>')
		yield eq, '16', r('<?print d.hour()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@py.test.mark.ul4
def test_method_minute():
	for r in all_renderers:
		yield eq, '47', r('<?print @(2010-05-12T16:47:56).minute()?>')
		yield eq, '47', r('<?print d.minute()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@py.test.mark.ul4
def test_method_second():
	for r in all_renderers:
		yield eq, '56', r('<?print @(2010-05-12T16:47:56).second()?>')
		yield eq, '56', r('<?print d.second()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@py.test.mark.ul4
def test_method_microsecond():
	for r in all_renderers:
		yield eq, '123000', r('<?print @(2010-05-12T16:47:56.123000).microsecond()?>')
		yield eq, '123000', r('<?print d.microsecond()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56, 123000))


@py.test.mark.ul4
def test_method_weekday():
	for r in all_renderers:
		yield eq, '2', r('<?print @(2010-05-12).weekday()?>')
		yield eq, '2', r('<?print d.weekday()?>', d=datetime.date(2010, 5, 12))


@py.test.mark.ul4
def test_method_yearday():
	for r in all_renderers:
		yield eq, '1', r('<?print @(2010-01-01).yearday()?>')
		yield eq, '366', r('<?print @(2008-12-31).yearday()?>')
		yield eq, '365', r('<?print @(2010-12-31).yearday()?>')
		yield eq, '132', r('<?print @(2010-05-12).yearday()?>')
		yield eq, '132', r('<?print @(2010-05-12T16:47:56).yearday()?>')
		yield eq, '132', r('<?print d.yearday()?>', d=datetime.date(2010, 5, 12))
		yield eq, '132', r('<?print d.yearday()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@py.test.mark.ul4
def test_render():
	t = ul4c.Template('<?print prefix?><?print data?><?print suffix?>')
	for r in all_renderers:
		yield eq, '(f)(o)(o)', r('<?for c in data?><?render t.render(data=c, prefix="(", suffix=")")?><?end for?>', t=t, data='foo')
		yield eq, '(f)(o)(o)', r('<?for c in data?><?render t.render(data=c, **{"prefix": "(", "suffix": ")"})?><?end for?>', t=t, data='foo')


@py.test.mark.ul4
def test_render_var():
	t = ul4c.Template('<?code x += 1?><?print x?>')
	for r in all_renderers:
		yield eq, '42,43,42', r('<?print x?>,<?render t.render(x=x)?>,<?print x?>', t=t, x=42)


@py.test.mark.ul4
def test_def():
	for r in all_renderers:
		yield eq, 'foo', r('<?def lower?><?print x.lower()?><?end def?><?print lower.renders(x="FOO")?>')


@py.test.mark.ul4
def test_parse():
	for r in all_renderers:
		yield eq, '42', r('<?print data.Noner?>', data=dict(Noner=42))


@py.test.mark.ul4
def test_nested_exceptions():
	tmpl1 = ul4c.Template("<?print 2*x?>", "tmpl1")
	tmpl2 = ul4c.Template("<?render tmpl1.render(x=x)?>", "tmpl2")
	tmpl3 = ul4c.Template("<?render tmpl2.render(tmpl1=tmpl1, x=x)?>", "tmpl3")

	for r in all_python_renderers:
		msg = "TypeError: unsupported operand type\\(s\\) for \\*: 'int' and 'NoneType'|.* \\* .* not supported"
		yield raises, msg, r("<?render tmpl3.render(tmpl1=tmpl1, tmpl2=tmpl2, x=x)?>", tmpl1=tmpl1, tmpl2=tmpl2, tmpl3=tmpl3, x=None)


@py.test.mark.ul4
def test_note():
	for r in all_renderers:
		yield eq, "foo", r("f<?note This is?>o<?note a comment?>o")


@py.test.mark.ul4
def test_templateattributes():
	s1 = "<?print x?>"
	t1 = ul4c.Template(s1)

	s2 = "<?printx 42?>"
	t2 = ul4c.Template(s2)

	for r in all_renderers:
		if r is not RenderJavaCompiledTemplateByPython:
			yield eq, "<?", r("<?print template.startdelim?>", template=t1)
			yield eq, "?>", r("<?print template.enddelim?>", template=t1)
			yield eq, s1, r("<?print template.source?>", template=t1)
			yield eq, "1", r("<?print len(template.content)?>", template=t1)
			yield eq, "print", r("<?print template.content[0].type?>", template=t1)
			yield eq, s1, r("<?print template.content[0].location.tag?>", template=t1)
			yield eq, "x", r("<?print template.content[0].location.code?>", template=t1)
			yield eq, "var", r("<?print template.content[0].obj.type?>", template=t1)
			yield eq, "x", r("<?print template.content[0].obj.name?>", template=t1)
			yield eq, "printx", r("<?print template.content[0].type?>", template=t2)
			yield eq, "int", r("<?print template.content[0].obj.type?>", template=t2)
			yield eq, "42", r("<?print template.content[0].obj.value?>", template=t2)


@py.test.mark.ul4
def test_templateattributes_localtemplate():
	source = "<?def lower?><?print t.lower()?><?end def?>"

	for r in all_renderers:
		if r is not RenderJavaCompiledTemplateByPython:
			yield eq, source + "<?print lower.source?>", r(source + "<?print lower.source?>")
			yield eq, source, r(source + "<?print lower.source[lower.location.starttag:lower.endlocation.endtag]?>")
			yield eq, "<?print t.lower()?>", r(source + "<?print lower.source[lower.location.endtag:lower.endlocation.starttag]?>")
			yield eq, "lower", r(source + "<?print lower.name?>")


def universaltemplate():
	return ul4c.Template("""
		text
		<?code x = 'gurk'?>
		<?code x = 42?>
		<?code x = 4.2?>
		<?code x = None?>
		<?code x = False?>
		<?code x = True?>
		<?code x = @(2009-01-04)?>
		<?code x = #0063a8?>
		<?code x = [42]?>
		<?code x = {"fortytwo": 42}?>
		<?code x = {**{"fortytwo": 42}}?>
		<?code x = y?>
		<?code x += 42?>
		<?code x -= 42?>
		<?code x *= 42?>
		<?code x /= 42?>
		<?code x //= 42?>
		<?code x %= 42?>
		<?code del x?>
		<?print x.gurk?>
		<?print x["gurk"]?>
		<?print x[1:2]?>
		<?print x[1:]?>
		<?print x[:2]?>
		<?print x[:]?>
		<?printx x?>
		<?for x in "12"?><?print x?><?break?><?continue?><?end for?>
		<?print not x?>
		<?print -x?>
		<?print x in y?>
		<?print x not in y?>
		<?print x==y?>
		<?print x!=y?>
		<?print x<y?>
		<?print x<=y?>
		<?print x>y?>
		<?print x>=y?>
		<?print x+y?>
		<?print x*y?>
		<?print x/y?>
		<?print x//y?>
		<?print x and y?>
		<?print x or y?>
		<?print x % y?>
		<?print now()?>
		<?print repr(1)?>
		<?print range(1, 2)?>
		<?print range(1, 2, 3)?>
		<?print rgb(1, 2, 3, 4)?>
		<?print x.r()?>
		<?print x.find(1)?>
		<?print x.find(1, 2)?>
		<?print x.find(1, 2, 3)?>
		<?if x?>gurk<?elif y?>hurz<?else?>hinz<?end if?>
		<?render x.render(a=1, b=2)?>
		<?def x?>foo<?end def?>
		<?render x.render()?>
	""")


@py.test.mark.ul4
def test_strtemplate():
	t = universaltemplate()
	str(t)


@py.test.mark.ul4
def test_pythonsource():
	t = universaltemplate()
	t.pythonsource()


@py.test.mark.ul4
def test_pythonfunction():
	t = universaltemplate()
	t.pythonfunction()


@py.test.mark.ul4
def test_jssource():
	t = universaltemplate()
	t.jssource()


@py.test.mark.ul4
def test_javasource():
	t = universaltemplate()
	t.javasource()


@py.test.mark.ul4
def test_attr_if():
	cond = ul4.attr_if(html.a("gu'\"rk"), cond="cond")

	s = html.div(class_=cond).conv().string()
	for r in all_renderers:
		yield eq, '<div></div>', r(s, cond=False)
		yield eq, '''<div class="gu'&quot;rk"></div>''', r(s, cond=True)

	s = html.div(class_=(cond, "hurz")).conv().string()
	for r in all_renderers:
		yield eq, '<div class="hurz"></div>', r(s, cond=False)
		yield eq, '''<div class="gu'&quot;rkhurz"></div>''', r(s, cond=True)

	s = cond.conv().string()
	for r in all_renderers:
		yield eq, '', r(s, cond=False)
		yield eq, '''<a>gu'"rk</a>''', r(s, cond=True)

	s = html.ul(compact=ul4.attr_if(True, cond="cond")).conv().string()
	for r in all_renderers:
		yield eq, '<ul></ul>', r(s, cond=False)
		yield eq, '''<ul compact="compact"></ul>''', r(s, cond=True)
