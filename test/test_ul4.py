#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009-2012 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, os, re, datetime, io, json, contextlib, tempfile, collections, shutil, subprocess, pkg_resources

import pytest

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
			dir = os.path.expanduser("~/checkouts/LivingLogic.Javascript.ul4")
			proc = subprocess.Popen("d8 {dir}/ul4on.js {dir}/ul4.js {fn}".format(dir=dir, fn=f.name), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			(stdout, stderr) = proc.communicate()
		stdout = stdout.decode("utf-8")
		stderr = stderr.decode("utf-8")
		# Check if we have an exception
		if proc.returncode:
			print(stdout, file=sys.stdout)
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


all_renderers =  [
	("python", RenderPython),
	("python_dumps", RenderPythonDumpS),
	("python_dump", RenderPythonDump),
	("js", RenderJS),
	("java_interpreted_by_python", RenderJavaInterpretedTemplateByPython),
	("java_compiled_by_python", RenderJavaCompiledTemplateByPython),
	("java_interpreted_by_java", RenderJavaInterpretedTemplateByJava),
]


def pytest_generate_tests(metafunc):
	if "r" in metafunc.funcargnames:
		metafunc.parametrize("r", [r for (id, r) in all_renderers], ids=[id for (id, r) in all_renderers])


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
	"expected at least \\d+ arguments",
	# Javascript argument mismatch exception messages
	"requires (at least \\d+|\\d+(-\\d+)?) arguments?, \\d+ given",
	# Java compiler errors for argument mismatches
	"cannot find symbol",
	"cannot be applied",
	"The method .* is not applicable for the arguments",
	# Java exception messages for argument mismatches
	"expects (at least \\d+|exactly \\d+|\\d+-\\d+) arguments?, \\d+ given",
]
argumentmismatchmessage = "({})".format("|".join(argumentmismatchmessage))


def eq(expected, render):
	got = render.renders() # Put this on an extra line, so that pytest executes it only once
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
		pytest.fail("failed to raise exception")


@pytest.mark.ul4
def test_text(r):
	eq('gurk', r('gurk'))
	eq('g\xfcrk', r('g\xfcrk'))


@pytest.mark.ul4
def test_none(r):
	eq('', r('<?print None?>'))
	eq('no', r('<?if None?>yes<?else?>no<?end if?>'))


@pytest.mark.ul4
def test_false(r):
	eq('False', r('<?print False?>'))
	eq('no', r('<?if False?>yes<?else?>no<?end if?>'))


@pytest.mark.ul4
def test_true(r):
	eq('True', r('<?print True?>'))
	eq('yes', r('<?if True?>yes<?else?>no<?end if?>'))


@pytest.mark.ul4
def test_int(r):
	values = (0, 42, -42, 0x7ffffff, 0x8000000, -0x8000000, -0x8000001)
	if r is not RenderJS:
		# Since Javascript has no real integers the following would lead to rounding errors
		values += (0x7ffffffffffffff, 0x800000000000000, -0x800000000000000, -0x800000000000001, 9999999999, -9999999999, 99999999999999999999, -99999999999999999999)
	for value in values:
		eq(str(value), r('<?print {}?>'.format(value)))
	eq('255', r('<?print 0xff?>'))
	eq('255', r('<?print 0Xff?>'))
	eq('-255', r('<?print -0xff?>'))
	eq('-255', r('<?print -0Xff?>'))
	eq('63', r('<?print 0o77?>'))
	eq('63', r('<?print 0O77?>'))
	eq('-63', r('<?print -0o77?>'))
	eq('-63', r('<?print -0O77?>'))
	eq('7', r('<?print 0b111?>'))
	eq('7', r('<?print 0B111?>'))
	eq('-7', r('<?print -0b111?>'))
	eq('-7', r('<?print -0B111?>'))

	eq('no', r('<?if 0?>yes<?else?>no<?end if?>'))
	eq('yes', r('<?if 1?>yes<?else?>no<?end if?>'))
	eq('yes', r('<?if -1?>yes<?else?>no<?end if?>'))


@pytest.mark.ul4
def test_float(r):
	# str() output might differ slightly between Python and JS, so eval the output again for tests
	evaleq(0.0, r('<?print 0.?>'))
	evaleq(42.0, r('<?print 42.?>'))
	evaleq(-42.0, r('<?print -42.?>'))
	evaleq(-42.5, r('<?print -42.5?>'))
	evaleq(1e42, r('<?print 1E42?>'))
	evaleq(1e42, r('<?print 1e42?>'))
	evaleq(-1e42, r('<?print -1E42?>'))
	evaleq(-1e42, r('<?print -1e42?>'))

	eq('no', r('<?if 0.?>yes<?else?>no<?end if?>'))
	eq('yes', r('<?if 1.?>yes<?else?>no<?end if?>'))
	eq('yes', r('<?if -1.?>yes<?else?>no<?end if?>'))


@pytest.mark.ul4
def test_string(r):
	raises("Unterminated string|mismatched character|MismatchedTokenException", r('<?print "?>'))
	eq('foo', r('<?print "foo"?>'))
	eq('\n', r('<?print "\\n"?>'))
	eq('\r', r('<?print "\\r"?>'))
	eq('\t', r('<?print "\\t"?>'))
	eq('\f', r('<?print "\\f"?>'))
	eq('\b', r('<?print "\\b"?>'))
	eq('\a', r('<?print "\\a"?>'))
	eq('\x1b', r('<?print "\\e"?>'))
	eq('\x00', r('<?print "\\x00"?>'))
	eq('"', r('<?print "\\""?>'))
	eq("'", r('<?print "\\\'"?>'))
	eq('\u20ac', r('<?print "\u20ac"?>'))
	eq('\xff', r('<?print "\\xff"?>'))
	eq('\u20ac', r('''<?print "\\u20ac"?>'''))
	eq("a\nb", r('<?print "a\nb"?>'))
	for c in "\x00\x80\u0100\u3042\n\r\t\f\b\a\e\"":
		eq(c, r('<?print obj?>', obj=c)) # This tests :func:`misc.javaexpr` for Java and :func:`ul4c._asjson` for JS

	# Test literal control characters
	eq('gu\n\r\trk', r("<?print 'gu\n\r\trk'?>"))
	eq('gu\n\r\t\\rk', r(r"<?print 'gu\n\r\t\\rk'?>"))

	eq('no', r('<?if ""?>yes<?else?>no<?end if?>'))
	eq('yes', r('<?if "foo"?>yes<?else?>no<?end if?>'))


@pytest.mark.ul4
def test_date(r):
	eq('2000-02-29', r('<?print @(2000-02-29).isoformat()?>'))
	eq('2000-02-29', r('<?print @(2000-02-29T).isoformat()?>'))
	eq('2000-02-29T12:34:00', r('<?print @(2000-02-29T12:34).isoformat()?>'))
	eq('2000-02-29T12:34:56', r('<?print @(2000-02-29T12:34:56).isoformat()?>'))
	eq('2000-02-29T12:34:56.987000', r('<?print @(2000-02-29T12:34:56.987000).isoformat()?>')) # JS and Java only supports milliseconds
	eq('yes', r('<?if @(2000-02-29T12:34:56.987654)?>yes<?else?>no<?end if?>'))


@pytest.mark.ul4
def test_color(r):
	eq('255,255,255,255', r('<?code c = #fff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>'))
	eq('255,255,255,255', r('<?code c = #ffffff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>'))
	eq('18,52,86,255', r('<?code c = #123456?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>'))
	eq('17,34,51,68', r('<?code c = #1234?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>'))
	eq('18,52,86,120', r('<?code c = #12345678?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>'))
	eq('yes', r('<?if #fff?>yes<?else?>no<?end if?>'))


@pytest.mark.ul4
def test_list(r):
	eq('', r('<?for item in []?><?print item?>;<?end for?>'))
	eq('1;', r('<?for item in [1]?><?print item?>;<?end for?>'))
	eq('1;', r('<?for item in [1,]?><?print item?>;<?end for?>'))
	eq('1;2;', r('<?for item in [1, 2]?><?print item?>;<?end for?>'))
	eq('1;2;', r('<?for item in [1, 2,]?><?print item?>;<?end for?>'))
	eq('no', r('<?if []?>yes<?else?>no<?end if?>'))
	eq('yes', r('<?if [1]?>yes<?else?>no<?end if?>'))


@pytest.mark.ul4
def test_dict(r):
	eq('', r('<?for (key, value) in {}.items()?><?print key?>:<?print value?>\n<?end for?>'))
	eq('1:2\n', r('<?for (key, value) in {1:2}.items()?><?print key?>:<?print value?>\n<?end for?>'))
	eq('1:#fff\n', r('<?for (key, value) in {1:#fff}.items()?><?print key?>:<?print value?>\n<?end for?>'))
	eq('1:2\n', r('<?for (key, value) in {1:2,}.items()?><?print key?>:<?print value?>\n<?end for?>'))
	# With duplicate keys, later ones simply overwrite earlier ones
	eq('1:3\n', r('<?for (key, value) in {1:2, 1: 3}.items()?><?print key?>:<?print value?>\n<?end for?>'))
	# Test **
	eq('1:2\n', r('<?for (key, value) in {**{1:2}}.items()?><?print key?>:<?print value?>\n<?end for?>'))
	eq('1:4\n', r('<?for (key, value) in {1:1, **{1:2}, 1:3, **{1:4}}.items()?><?print key?>:<?print value?>\n<?end for?>'))
	eq('no', r('<?if {}?>yes<?else?>no<?end if?>'))
	eq('yes', r('<?if {1:2}?>yes<?else?>no<?end if?>'))


@pytest.mark.ul4
def test_code_storevar(r):
	eq('42', r('<?code x = 42?><?print x?>'))
	eq('xyzzy', r('<?code x = "xyzzy"?><?print x?>'))
	eq('x,y', r('<?code (x, y) = "xy"?><?print x?>,<?print y?>'))
	eq('42', r('<?code (x,) = [42]?><?print x?>'))
	eq('17,23', r('<?code (x,y) = [17, 23]?><?print x?>,<?print y?>'))
	eq('17,23,37,42,105', r('<?code ((v, w), (x,), (y,), z) = [[17, 23], [37], [42], 105]?><?print v?>,<?print w?>,<?print x?>,<?print y?>,<?print z?>'))


@pytest.mark.ul4
def test_code_addvar(r):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			evaleq(x + y, r('<?code x = {}?><?code x += {}?><?print x?>'.format(x, y)))
	eq('xyzzy', r('<?code x = "xyz"?><?code x += "zy"?><?print x?>'))


@pytest.mark.ul4
def test_code_subvar(r):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			evaleq(x - y, r('<?code x = {}?><?code x -= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_code_mulvar(r):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			evaleq(x * y, r('<?code x = {}?><?code x *= {}?><?print x?>'.format(x, y)))
	for x in (17, False, True):
		y = "xyzzy"
		eq(x * y, r('<?code x = {}?><?code x *= {!r}?><?print x?>'.format(x, y)))
	eq(17*"xyzzy", r('<?code x = "xyzzy"?><?code x *= 17?><?print x?>'))


@pytest.mark.ul4
def test_code_floordivvar(r):
	for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
		for y in (2, -2, 2.0, -2.0, True):
			evaleq(x // y, r('<?code x = {}?><?code x //= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_code_truedivvar(r):
	for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
		for y in (2, -2, 2.0, -2.0, True):
			evaleq(x / y, r('<?code x = {}?><?code x /= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_code_modvar(r):
	for x in (1729, 1729.0, -1729, -1729.0, False, True):
		for y in (23, 23., -23, -23.0, True):
			evaleq(x % y, r('<?code x = {}?><?code x %= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_code_delvar(r):
	if r is not RenderJS:
		raises("(KeyError|not found)", r('<?code x = 1729?><?code del x?><?print x?>'))


@pytest.mark.ul4
def test_for_string(r):
	eq('', r('<?for c in data?>(<?print c?>)<?end for?>', data=""))
	eq('(g)(u)(r)(k)', r('<?for c in data?>(<?print c?>)<?end for?>', data="gurk"))


@pytest.mark.ul4
def test_for_list(r):
	eq('', r('<?for c in data?>(<?print c?>)<?end for?>', data=""))
	eq('(g)(u)(r)(k)', r('<?for c in data?>(<?print c?>)<?end for?>', data=["g", "u", "r", "k"]))


@pytest.mark.ul4
def test_for_dict(r):
	eq('', r('<?for c in data?>(<?print c?>)<?end for?>', data={}))
	eq('(a)(b)(c)', r('<?for c in sorted(data)?>(<?print c?>)<?end for?>', data=dict(a=1, b=2, c=3)))


@pytest.mark.ul4
def test_for_nested_loop(r):
	eq('[(1)(2)][(3)(4)]', r('<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>', data=[[1, 2], [3, 4]]))


@pytest.mark.ul4
def test_for_unpacking(r):
	data = [
		("spam", "eggs", 17),
		("gurk", "hurz", 23),
		("hinz", "kunz", 42),
	]

	eq('(spam)(gurk)(hinz)', r('<?for (a,) in data?>(<?print a?>)<?end for?>', data=[item[:1] for item in data]))
	eq('(spam,eggs)(gurk,hurz)(hinz,kunz)', r('<?for (a, b) in data?>(<?print a?>,<?print b?>)<?end for?>', data=[item[:2] for item in data]))
	eq('(spam,eggs,17)(gurk,hurz,23)(hinz,kunz,42)', r('<?for (a, b, c) in data?>(<?print a?>,<?print b?>,<?print c?>)<?end for?>', data=data))


@pytest.mark.ul4
def test_for_nested_unpacking(r):
	data = [
		(("spam", "eggs"), (17,), None),
		(("gurk", "hurz"), (23,), False),
		(("hinz", "kunz"), (42,), True),
	]

	eq('(spam,eggs,17,)(gurk,hurz,23,False)(hinz,kunz,42,True)', r('<?for ((a, b), (c,), d) in data?>(<?print a?>,<?print b?>,<?print c?>,<?print d?>)<?end for?>', data=data))


@pytest.mark.ul4
def test_break(r):
	eq('1, 2, ', r('<?for i in [1,2,3]?><?print i?>, <?if i==2?><?break?><?end if?><?end for?>'))


@pytest.mark.ul4
def test_break_nested(r):
	eq('1, 1, 2, 1, 2, 3, ', r('<?for i in [1,2,3,4]?><?for j in [1,2,3,4]?><?print j?>, <?if j>=i?><?break?><?end if?><?end for?><?if i>=3?><?break?><?end if?><?end for?>'))


@pytest.mark.ul4
def test_continue(r):
	eq('1, 3, ', r('<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?print i?>, <?end for?>'))


@pytest.mark.ul4
def test_continue_nested(r):
	eq('1, 3, \n1, 3, \n', r('<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?for j in [1,2,3]?><?if j==2?><?continue?><?end if?><?print j?>, <?end for?>\n<?end for?>'))


@pytest.mark.ul4
def test_if(r):
	eq('42', r('<?if data?><?print data?><?end if?>', data=42))


@pytest.mark.ul4
def test_else(r):
	eq('42', r('<?if data?><?print data?><?else?>no<?end if?>', data=42))
	eq('no', r('<?if data?><?print data?><?else?>no<?end if?>', data=0))


@pytest.mark.ul4
def test_block_errors():
	raises("BlockError: block unclosed", RenderPython('<?for x in data?>'))
	raises("BlockError: endif doesn't match any if", RenderPython('<?for x in data?><?end if?>'))
	raises("BlockError: not in any block", RenderPython('<?end?>'))
	raises("BlockError: not in any block", RenderPython('<?end for?>'))
	raises("BlockError: not in any block", RenderPython('<?end if?>'))
	raises("BlockError: else doesn't match any if", RenderPython('<?else?>'))
	raises("BlockError: block unclosed", RenderPython('<?if data?>'))
	raises("BlockError: block unclosed", RenderPython('<?if data?><?else?>'))
	raises("BlockError: else already seen in if", RenderPython('<?if data?><?else?><?else?>'))
	raises("BlockError: else already seen in if", RenderPython('<?if data?><?else?><?elif data?>'))
	raises("BlockError: else already seen in if", RenderPython('<?if data?><?elif data?><?elif data?><?else?><?elif data?>'))


@pytest.mark.ul4
def test_empty():
	raises("expression required", RenderPython('<?print?>'))
	raises("expression required", RenderPython('<?if?>'))
	raises("expression required", RenderPython('<<?if x?><?elif?><?end if?>'))
	raises("loop expression required", RenderPython('<?for?>'))
	raises("statement required", RenderPython('<?code?>'))
	raises("expression required", RenderPython('<?render?>'))


@pytest.mark.ul4
def test_add(r):
	values = (17, 23, 1., -1.)

	for x in values:
		for y in values:
			evaleq(x + y, r('<?print x + y?>', x=x, y=y)) # Using ``evaleq`` avoids problem with the nonexistant int/float distinction in JS
	eq('foobar', r('<?code x="foo"?><?code y="bar"?><?print x+y?>'))
	eq('(f)(o)(o)(b)(a)(r)', r('<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>', data=dict(foo="foo", bar="bar")))


@pytest.mark.ul4
def test_sub(r):
	values = (17, 23, 1., -1.)

	for x in values:
		for y in values:
			evaleq(x - y, r('<?print x - y?>', x=x, y=y))


@pytest.mark.ul4
def test_mul(r):
	values = (17, 23, 1., -1.)

	for x in values:
		for y in values:
			evaleq(x * y, r('<?print x * y?>', x=x, y=y))
	eq(17*"foo", r('<?print 17*"foo"?>'))
	eq(17*"foo", r('<?code x=17?><?code y="foo"?><?print x*y?>'))
	eq("foo"*17, r('<?code x="foo"?><?code y=17?><?print x*y?>'))
	eq("foo"*17, r('<?print "foo"*17?>'))
	eq("(foo)(bar)(foo)(bar)(foo)(bar)", r('<?for i in 3*data?>(<?print i?>)<?end for?>', data=["foo", "bar"]))


@pytest.mark.ul4
def test_truediv(r):
	eq("0.5", r('<?print 1/2?>'))
	eq("0.5", r('<?code x=1?><?code y=2?><?print x/y?>'))


@pytest.mark.ul4
def test_floordiv(r):
	eq("0", r('<?print 1//2?>'))
	eq("0", r('<?code x=1?><?code y=2?><?print x//y?>'))


@pytest.mark.ul4
def test_mod(r):
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			evaleq(x % y, r('<?print {} % {}?>'.format(x, y)))
			evaleq(x % y, r('<?print x % y?>', x=x, y=y))


@pytest.mark.ul4
def test_eq(r):
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			eq(str(x == y), r('<?print {} == {}?>'.format(x, y)))
			eq(str(x == y), r('<?print x == y?>', x=x, y=y))


@pytest.mark.ul4
def test_ne(r):
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			eq(str(x != y), r('<?print {} != {}?>'.format(x, y)))
			eq(str(x != y), r('<?print x != y?>', x=x, y=y))


@pytest.mark.ul4
def test_lt(r):
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			eq(str(x < y), r('<?print {} < {}?>'.format(x, y)))
			eq(str(x < y), r('<?print x < y?>', x=x, y=y))


@pytest.mark.ul4
def test_le(r):
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			eq(str(x <= y), r('<?print {} <= {}?>'.format(x, y)))
			eq(str(x <= y), r('<?print x <= y?>', x=x, y=y))


@pytest.mark.ul4
def test_gt(r):
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			eq(str(x > y), r('<?print {} > {}?>'.format(x, y)))
			eq(str(x > y), r('<?print x > y?>', x=x, y=y))


@pytest.mark.ul4
def test_ge(r):
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			eq(str(x >= y), r('<?print {} >= {}?>'.format(x, y)))
			eq(str(x >= y), r('<?print x >= y?>', x=x, y=y))


@pytest.mark.ul4
def test_contains(r):
	code = '<?print x in y?>'

	eq("True", r(code, x=2, y=[1, 2, 3]))
	eq("False", r(code, x=4, y=[1, 2, 3]))
	eq("True", r(code, x="ur", y="gurk"))
	eq("False", r(code, x="un", y="gurk"))
	eq("True", r(code, x="a", y={"a": 1, "b": 2}))
	eq("False", r(code, x="c", y={"a": 1, "b": 2}))
	eq("True", r(code, x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42)))
	eq("False", r(code, x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42)))


@pytest.mark.ul4
def test_notcontains(r):
	code = '<?print x not in y?>'

	eq("False", r(code, x=2, y=[1, 2, 3]))
	eq("True", r(code, x=4, y=[1, 2, 3]))
	eq("False", r(code, x="ur", y="gurk"))
	eq("True", r(code, x="un", y="gurk"))
	eq("False", r(code, x="a", y={"a": 1, "b": 2}))
	eq("True", r(code, x="c", y={"a": 1, "b": 2}))
	eq("False", r(code, x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42)))
	eq("True", r(code, x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42)))


@pytest.mark.ul4
def test_and(r):
	eq("False", r('<?print x and y?>', x=False, y=False))
	eq("False", r('<?print x and y?>', x=False, y=True))
	eq("0", r('<?print x and y?>', x=0, y=True))


@pytest.mark.ul4
def test_or(r):
	eq("False", r('<?print x or y?>', x=False, y=False))
	eq("True", r('<?print x or y?>', x=False, y=True))
	eq("42", r('<?print x or y?>', x=42, y=True))


@pytest.mark.ul4
def test_not(r):
	eq("True", r('<?print not x?>', x=False))
	eq("False", r('<?print not x?>', x=42))


@pytest.mark.ul4
def test_getitem(r):
	eq("u", r("<?print 'gurk'[1]?>"))
	eq("u", r("<?print x[1]?>", x="gurk"))
	eq("u", r("<?print 'gurk'[-3]?>"))
	eq("u", r("<?print x[-3]?>", x="gurk"))
	raises("index out of range|IndexError", r("<?print 'gurk'[4]?>"))
	raises("index (4 )?out of range", r("<?print x[4]?>", x="gurk"))
	raises("index out of range|IndexError", r("<?print 'gurk'[-5]?>"))
	raises("index (-5 )?out of range", r("<?print x[-5]?>", x="gurk"))


@pytest.mark.ul4
def test_getslice12(r):
	eq("ur", r("<?print 'gurk'[1:3]?>"))
	eq("ur", r("<?print x[1:3]?>", x="gurk"))
	eq("ur", r("<?print 'gurk'[-3:-1]?>"))
	eq("ur", r("<?print x[-3:-1]?>", x="gurk"))
	eq("", r("<?print 'gurk'[4:10]?>"))
	eq("", r("<?print x[4:10]?>", x="gurk"))
	eq("", r("<?print 'gurk'[-10:-5]?>"))
	eq("", r("<?print x[-10:-5]?>", x="gurk"))


@pytest.mark.ul4
def test_getslice1(r):
	eq("urk", r("<?print 'gurk'[1:]?>"))
	eq("urk", r("<?print x[1:]?>", x="gurk"))
	eq("urk", r("<?print 'gurk'[-3:]?>"))
	eq("urk", r("<?print x[-3:]?>", x="gurk"))
	eq("", r("<?print 'gurk'[4:]?>"))
	eq("", r("<?print x[4:]?>", x="gurk"))
	eq("gurk", r("<?print 'gurk'[-10:]?>"))
	eq("gurk", r("<?print x[-10:]?>", x="gurk"))


@pytest.mark.ul4
def test_getslice2(r):
	eq("gur", r("<?print 'gurk'[:3]?>"))
	eq("gur", r("<?print x[:3]?>", x="gurk"))
	eq("gur", r("<?print 'gurk'[:-1]?>"))
	eq("gur", r("<?print x[:-1]?>", x="gurk"))
	eq("gurk", r("<?print 'gurk'[:10]?>"))
	eq("gurk", r("<?print x[:10]?>", x="gurk"))
	eq("", r("<?print 'gurk'[:-5]?>"))
	eq("", r("<?print x[:-5]?>", x="gurk"))


@pytest.mark.ul4
def test_getslice(r):
	eq("gurk", r("<?print 'gurk'[:]?>"))
	eq("gurk", r("<?print x[:]?>", x="gurk"))
	eq("[1, 2]", r("<?print x[:]?>", x=[1, 2]))


@pytest.mark.ul4
def test_nested(r):
	sc = "4"
	sv = "x"
	n = 4
	# when using 8 Java will output "An irrecoverable stack overflow has occurred"
	depth = 7
	for i in range(depth):
		sc = "({})+({})".format(sc, sc)
		sv = "({})+({})".format(sv, sv)
		n = n + n

	eq(str(n), r('<?print {}?>'.format(sc)))
	eq(str(n), r('<?code x=4?><?print {}?>'.format(sv)))


@pytest.mark.ul4
def test_precedence(r):
	eq("14", r('<?print 2+3*4?>'))
	eq("20", r('<?print (2+3)*4?>'))
	eq("10", r('<?print -2+-3*-4?>'))
	eq("14", r('<?print --2+--3*--4?>'))
	eq("14", r('<?print (-(-2))+(-((-3)*-(-4)))?>'))
	eq("42", r('<?print 2*data.value?>', data=dict(value=21)))
	eq("42", r('<?print data.value[0]?>', data=dict(value=[42])))
	eq("42", r('<?print data[0].value?>', data=[dict(value=42)]))
	eq("42", r('<?print data[0][0][0]?>', data=[[[42]]]))
	eq("42", r('<?print data.value.value[0]?>', data=dict(value=dict(value=[42]))))
	eq("42", r('<?print data.value.value[0].value.value[0]?>', data=dict(value=dict(value=[dict(value=dict(value=[42]))]))))

@pytest.mark.ul4
def test_associativity(r):
	eq("9", r('<?print 2+3+4?>'))
	eq("-5", r('<?print 2-3-4?>'))
	eq("24", r('<?print 2*3*4?>'))
	if r is not RenderJS:
		eq("2.0", r('<?print 24/6/2?>'))
		eq("2", r('<?print 24//6//2?>'))
	else:
		evaleq(2.0, r('<?print 24/6/2?>'))
		evaleq(2, r('<?print 24//6//2?>'))

@pytest.mark.ul4
def test_bracket(r):
	sc = "4"
	sv = "x"
	for i in range(10):
		sc = "({})".format(sc)
		sv = "({})".format(sv)

	eq("4", r('<?print {}?>'.format(sc)))
	eq("4", r('<?code x=4?><?print {}?>'.format(sv)))


@pytest.mark.ul4
def test_function_now(r):
	now = str(datetime.datetime.now())

	raises(argumentmismatchmessage, r("<?print now(1)?>"))
	raises(argumentmismatchmessage, r("<?print now(1, 2)?>"))
	le(now, r("<?print now()?>"))


@pytest.mark.ul4
def test_function_utcnow(r):
	utcnow = str(datetime.datetime.utcnow())

	raises(argumentmismatchmessage, r("<?print utcnow(1)?>"))
	raises(argumentmismatchmessage, r("<?print utcnow(1, 2)?>"))
	utcnowfromtemplate = r("<?print utcnow()?>")
	# JS and Java only have milliseconds precision, but this shouldn't lead to problems here, as rendering the template takes longer than a millisecond
	le(utcnow, utcnowfromtemplate)


@pytest.mark.ul4
def test_function_vars(r):
	code = "<?if var in vars()?>yes<?else?>no<?end if?>"

	raises(argumentmismatchmessage, r("<?print vars(1)?>"))
	raises(argumentmismatchmessage, r("<?print vars(1, 2)?>"))
	eq("yes", r(code, var="spam", spam="eggs"))
	eq("no", r(code, var="nospam", spam="eggs"))


@pytest.mark.ul4
def test_function_random(r):
	raises(argumentmismatchmessage, r("<?print random(1)?>"))
	raises(argumentmismatchmessage, r("<?print random(1, 2)?>"))
	eq("ok", r("<?code r = random()?><?if r>=0 and r<1?>ok<?else?>fail<?end if?>"))


@pytest.mark.ul4
def test_function_randrange(r):
	raises(argumentmismatchmessage, r("<?print randrange()?>"))
	eq("ok", r("<?code r = randrange(4)?><?if r>=0 and r<4?>ok<?else?>fail<?end if?>"))
	eq("ok", r("<?code r = randrange(17, 23)?><?if r>=17 and r<23?>ok<?else?>fail<?end if?>"))
	eq("ok", r("<?code r = randrange(17, 23, 2)?><?if r>=17 and r<23 and r%2?>ok<?else?>fail<?end if?>"))


@pytest.mark.ul4
def test_function_randchoice(r):
	raises(argumentmismatchmessage, r("<?print randchoice()?>"))
	eq("ok", r("<?code r = randchoice('abc')?><?if r in 'abc'?>ok<?else?>fail<?end if?>"))
	eq("ok", r("<?code s = [17, 23, 42]?><?code r = randchoice(s)?><?if r in s?>ok<?else?>fail<?end if?>"))
	eq("ok", r("<?code s = #12345678?><?code sl = [0x12, 0x34, 0x56, 0x78]?><?code r = randchoice(s)?><?if r in sl?>ok<?else?>fail<?end if?>"))


@pytest.mark.ul4
def test_function_xmlescape(r):
	raises(argumentmismatchmessage, r("<?print xmlescape()?>"))
	raises(argumentmismatchmessage, r("<?print xmlescape(1, 2)?>"))
	eq("&lt;&lt;&gt;&gt;&amp;&#39;&quot;gurk", r("<?print xmlescape(data)?>", data='<<>>&\'"gurk'))


@pytest.mark.ul4
def test_function_csv(r):
	raises(argumentmismatchmessage, r("<?print csv()?>"))
	raises(argumentmismatchmessage, r("<?print csv(1, 2)?>"))
	eq("", r("<?print csv(data)?>", data=None))
	eq("False", r("<?print csv(data)?>", data=False))
	eq("True", r("<?print csv(data)?>", data=True))
	eq("42", r("<?print csv(data)?>", data=42))
	# no check for float
	eq("abc", r("<?print csv(data)?>", data="abc"))
	eq('"a,b,c"', r("<?print csv(data)?>", data="a,b,c"))
	eq('"a""b""c"', r("<?print csv(data)?>", data='a"b"c'))
	eq('"a\nb\nc"', r("<?print csv(data)?>", data="a\nb\nc"))


@pytest.mark.ul4
def test_function_asjson(r):
	raises(argumentmismatchmessage, r("<?print asjson()?>"))
	raises(argumentmismatchmessage, r("<?print asjson(1, 2)?>"))
	eq("null", r("<?print asjson(data)?>", data=None))
	eq("false", r("<?print asjson(data)?>", data=False))
	eq("true", r("<?print asjson(data)?>", data=True))
	eq("42", r("<?print asjson(data)?>", data=42))
	# no check for float
	eq('"abc"', r("<?print asjson(data)?>", data="abc"))
	eq('[1, 2, 3]', r("<?print asjson(data)?>", data=[1, 2, 3]))
	eq('[1, 2, 3]', r("<?print asjson(data)?>", data=PseudoList([1, 2, 3])))
	eq('{"one": 1}', r("<?print asjson(data)?>", data={"one": 1}))
	eq('{"one": 1}', r("<?print asjson(data)?>", data=PseudoDict({"one": 1})))


@pytest.mark.ul4
def test_function_fromjson(r):
	code = "<?print repr(fromjson(data))?>"
	raises(argumentmismatchmessage, r("<?print fromjson()?>"))
	raises(argumentmismatchmessage, r("<?print fromjson(1, 2)?>"))
	eq("None", r(code, data="null"))
	eq("False", r(code, data="false"))
	eq("True", r(code, data="true"))
	eq("42", r(code, data="42"))
	# no check for float
	contains(('"abc"', "'abc'"), r(code, data='"abc"'))
	eq('[1, 2, 3]', r(code, data="[1, 2, 3]"))
	contains(('{"one": 1}', "{'one': 1}"), r(code, data='{"one": 1}'))


@pytest.mark.ul4
def test_function_ul4on(r):
	code = "<?print repr(fromul4on(asul4on(data)))?>"

	raises(argumentmismatchmessage, r("<?print asul4on()?>"))
	raises(argumentmismatchmessage, r("<?print asul4on(1, 2)?>"))
	raises(argumentmismatchmessage, r("<?print fromul4on()?>"))
	raises(argumentmismatchmessage, r("<?print fromul4on(1, 2)?>"))
	eq("None", r(code, data=None))
	eq("False", r(code, data=False))
	eq("True", r(code, data=True))
	eq("42", r(code, data=42))
	# no check for float
	contains(('"abc"', "'abc'"), r(code, data="abc"))
	eq('[1, 2, 3]', r(code, data=[1, 2, 3]))
	contains(('{"one": 1}', "{'one': 1}"), r(code, data={'one': 1}))


@pytest.mark.ul4
def test_function_str(r):
	code = "<?print str(data)?>"

	raises(argumentmismatchmessage, r("<?print str(1, 2)?>"))
	eq("", r("<?print str()?>"))
	eq("", r(code, data=None))
	eq("True", r(code, data=True))
	eq("False", r(code, data=False))
	eq("42", r(code, data=42))
	eq("4.2", r(code, data=4.2))
	eq("foo", r(code, data="foo"))
	eq("2011-02-09", r(code, data=datetime.date(2011, 2, 9)))
	eq("2011-02-09 12:34:56", r(code, data=datetime.datetime(2011, 2, 9, 12, 34, 56)))
	eq("2011-02-09 12:34:56.987000", r(code, data=datetime.datetime(2011, 2, 9, 12, 34, 56, 987000)))


@pytest.mark.ul4
def test_function_int(r):
	raises(argumentmismatchmessage, RenderPython("<?print int(1, 2, 3)?>"))
	raises("int\\(\\) argument must be a string or a number|int\\(null\\) not supported", RenderPython("<?print int(data)?>", data=None))
	raises("invalid literal for int|NumberFormatException", RenderPython("<?print int(data)?>", data="foo"))
	eq("0", r("<?print int()?>"))
	eq("1", r("<?print int(data)?>", data=True))
	eq("0", r("<?print int(data)?>", data=False))
	eq("42", r("<?print int(data)?>", data=42))
	eq("4", r("<?print int(data)?>", data=4.2))
	eq("42", r("<?print int(data)?>", data="42"))
	eq("66", r("<?print int(data, 16)?>", data="42"))


@pytest.mark.ul4
def test_function_float(r):
	code = "<?print float(data)?>"

	raises(argumentmismatchmessage, r("<?print float(1, 2, 3)?>"))
	raises("float\\(\\) argument must be a string or a number|float\\(null\\) not supported", r(code, data=None))
	eq("4.2", r(code, data=4.2))
	if r is not RenderJS:
		eq("0.0", r("<?print float()?>"))
		eq("1.0", r(code, data=True))
		eq("0.0", r(code, data=False))
		eq("42.0", r(code, data=42))
		eq("42.0", r(code, data="42"))
	else:
		evaleq(0.0, r("<?print float()?>"))
		evaleq(1.0, r(code, data=True))
		evaleq(0.0, r(code, data=False))
		evaleq(42.0, r(code, data=42))
		evaleq(42.0, r(code, data="42"))


@pytest.mark.ul4
def test_function_len(r):
	code = "<?print len(data)?>"

	raises(argumentmismatchmessage, r("<?print len()?>"))
	raises(argumentmismatchmessage, r("<?print len(1, 2)?>"))
	raises("has no len\\(\\)|len\\(.*\\) not supported", r(code, data=None))
	raises("has no len\\(\\)|len\\(.*\\) not supported", r(code, data=True))
	raises("has no len\\(\\)|len\\(.*\\) not supported", r(code, data=False))
	raises("has no len\\(\\)|len\\(.*\\) not supported", r(code, data=42))
	raises("has no len\\(\\)|len\\(.*\\) not supported", r(code, data=4.2))
	eq("42", r(code, data=42*"?"))
	eq("42", r(code, data=42*[None]))
	eq("42", r(code, data=dict.fromkeys(range(42))))


@pytest.mark.ul4
def test_function_enumerate(r):
	code1 = "<?for (i, value) in enumerate(data)?>(<?print value?>=<?print i?>)<?end for?>"
	code2 = "<?for (i, value) in enumerate(data, 42)?>(<?print value?>=<?print i?>)<?end for?>"

	raises(argumentmismatchmessage, r("<?print enumerate()?>"))
	raises(argumentmismatchmessage, r("<?print enumerate(1, 2, 3)?>"))
	raises("is not iterable|iter\\(.*\\) not supported", r(code1, data=None))
	raises("is not iterable|iter\\(.*\\) not supported", r(code1, data=True))
	raises("is not iterable|iter\\(.*\\) not supported", r(code1, data=False))
	raises("is not iterable|iter\\(.*\\) not supported", r(code1, data=42))
	raises("is not iterable|iter\\(.*\\) not supported", r(code1, data=4.2))
	eq("(f=0)(o=1)(o=2)", r(code1, data="foo"))
	eq("(foo=0)(bar=1)", r(code1, data=["foo", "bar"]))
	eq("(foo=0)", r(code1, data=dict(foo=True)))
	eq("", r(code1, data=""))
	eq("(f=42)(o=43)(o=44)", r(code2, data="foo"))


@pytest.mark.ul4
def test_function_enumfl(r):
	code1 = "<?for (i, f, l, value) in enumfl(data)?><?if f?>[<?end if?>(<?print value?>=<?print i?>)<?if l?>]<?end if?><?end for?>"
	code2 = "<?for (i, f, l, value) in enumfl(data, 42)?><?if f?>[<?end if?>(<?print value?>=<?print i?>)<?if l?>]<?end if?><?end for?>"

	raises(argumentmismatchmessage, r("<?print enumfl()?>"))
	raises(argumentmismatchmessage, r("<?print enumfl(1, 2, 3)?>"))
	raises("is not iterable|iter\\(.*\\) not supported", r(code1, data=None))
	raises("is not iterable|iter\\(.*\\) not supported", r(code1, data=True))
	raises("is not iterable|iter\\(.*\\) not supported", r(code1, data=False))
	raises("is not iterable|iter\\(.*\\) not supported", r(code1, data=42))
	raises("is not iterable|iter\\(.*\\) not supported", r(code1, data=4.2))
	eq("[(f=0)(o=1)(o=2)]", r(code1, data="foo"))
	eq("[(foo=0)(bar=1)]", r(code1, data=["foo", "bar"]))
	eq("[(foo=0)]", r(code1, data=dict(foo=True)))
	eq("", r(code1, data=""))
	eq("[(f=42)(o=43)(o=44)]", r(code2, data="foo"))


@pytest.mark.ul4
def test_function_isfirstlast(r):
	code = "<?for (f, l, value) in isfirstlast(data)?><?if f?>[<?end if?>(<?print value?>)<?if l?>]<?end if?><?end for?>"

	raises(argumentmismatchmessage, r("<?print isfirstlast()?>"))
	raises(argumentmismatchmessage, r("<?print isfirstlast(1, 2)?>"))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=None))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=True))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=False))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=42))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=4.2))
	eq("[(f)(o)(o)]", r(code, data="foo"))
	eq("[(foo)(bar)]", r(code, data=["foo", "bar"]))
	eq("[(foo)]", r(code, data=dict(foo=True)))
	eq("", r(code, data=""))


@pytest.mark.ul4
def test_function_isfirst(r):
	code = "<?for (f, value) in isfirst(data)?><?if f?>[<?end if?>(<?print value?>)<?end for?>"

	raises(argumentmismatchmessage, r("<?print isfirst()?>"))
	raises(argumentmismatchmessage, r("<?print isfirst(1, 2)?>"))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=None))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=True))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=False))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=42))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=4.2))
	eq("[(f)(o)(o)", r(code, data="foo"))
	eq("[(foo)(bar)", r(code, data=["foo", "bar"]))
	eq("[(foo)", r(code, data=dict(foo=True)))
	eq("", r(code, data=""))


@pytest.mark.ul4
def test_function_islast(r):
	code = "<?for (l, value) in islast(data)?>(<?print value?>)<?if l?>]<?end if?><?end for?>"

	raises(argumentmismatchmessage, r("<?print islast()?>"))
	raises(argumentmismatchmessage, r("<?print islast(1, 2)?>"))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=None))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=True))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=False))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=42))
	raises("is not iterable|iter\\(.*\\) not supported", r(code, data=4.2))
	eq("(f)(o)(o)]", r(code, data="foo"))
	eq("(foo)(bar)]", r(code, data=["foo", "bar"]))
	eq("(foo)]", r(code, data=dict(foo=True)))
	eq("", r(code, data=""))


@pytest.mark.ul4
def test_function_isnone(r):
	code = "<?print isnone(data)?>"

	raises(argumentmismatchmessage, r("<?print isnone()?>"))
	raises(argumentmismatchmessage, r("<?print isnone(1, 2)?>"))
	eq("True", r(code, data=None))
	eq("False", r(code, data=True))
	eq("False", r(code, data=False))
	eq("False", r(code, data=42))
	eq("False", r(code, data=4.2))
	eq("False", r(code, data="foo"))
	eq("False", r(code, data=datetime.datetime.now()))
	eq("False", r(code, data=()))
	eq("False", r(code, data=[]))
	eq("False", r(code, data={}))
	eq("False", r(code, data=ul4c.Template("")))
	eq("False", r(code, data=color.red))


@pytest.mark.ul4
def test_function_isbool(r):
	code = "<?print isbool(data)?>"

	raises(argumentmismatchmessage, r("<?print isbool()?>"))
	raises(argumentmismatchmessage, r("<?print isbool(1, 2)?>"))
	eq("False", r(code, data=None))
	eq("True", r(code, data=True))
	eq("True", r(code, data=False))
	eq("False", r(code, data=42))
	eq("False", r(code, data=4.2))
	eq("False", r(code, data="foo"))
	eq("False", r(code, data=datetime.datetime.now()))
	eq("False", r(code, data=()))
	eq("False", r(code, data=[]))
	eq("False", r(code, data={}))
	eq("False", r(code, data=ul4c.Template("")))
	eq("False", r(code, data=color.red))


@pytest.mark.ul4
def test_function_isint(r):
	code = "<?print isint(data)?>"

	raises(argumentmismatchmessage, r("<?print isint()?>"))
	raises(argumentmismatchmessage, r("<?print isint(1, 2)?>"))
	eq("False", r(code, data=None))
	eq("False", r(code, data=True))
	eq("False", r(code, data=False))
	eq("True", r(code, data=42))
	eq("False", r(code, data=4.2))
	eq("False", r(code, data="foo"))
	eq("False", r(code, data=datetime.datetime.now()))
	eq("False", r(code, data=()))
	eq("False", r(code, data=[]))
	eq("False", r(code, data={}))
	eq("False", r(code, data=ul4c.Template("")))
	eq("False", r(code, data=color.red))


@pytest.mark.ul4
def test_function_isfloat(r):
	code = "<?print isfloat(data)?>"

	raises(argumentmismatchmessage, r("<?print isfloat()?>"))
	raises(argumentmismatchmessage, r("<?print isfloat(1, 2)?>"))
	eq("False", r(code, data=None))
	eq("False", r(code, data=True))
	eq("False", r(code, data=False))
	eq("False", r(code, data=42))
	eq("True", r(code, data=4.2))
	eq("False", r(code, data="foo"))
	eq("False", r(code, data=datetime.datetime.now()))
	eq("False", r(code, data=()))
	eq("False", r(code, data=[]))
	eq("False", r(code, data={}))
	eq("False", r(code, data=ul4c.Template("")))
	eq("False", r(code, data=color.red))


@pytest.mark.ul4
def test_function_isstr(r):
	code = "<?print isstr(data)?>"

	raises(argumentmismatchmessage, r("<?print isstr()?>"))
	raises(argumentmismatchmessage, r("<?print isstr(1, 2)?>"))
	eq("False", r(code, data=None))
	eq("False", r(code, data=True))
	eq("False", r(code, data=False))
	eq("False", r(code, data=42))
	eq("False", r(code, data=4.2))
	eq("True", r(code, data="foo"))
	eq("False", r(code, data=datetime.datetime.now()))
	eq("False", r(code, data=()))
	eq("False", r(code, data=[]))
	eq("False", r(code, data={}))
	eq("False", r(code, data=ul4c.Template("")))
	eq("False", r(code, data=color.red))


@pytest.mark.ul4
def test_function_isdate(r):
	code = "<?print isdate(data)?>"

	raises(argumentmismatchmessage, r("<?print isdate()?>"))
	raises(argumentmismatchmessage, r("<?print isdate(1, 2)?>"))
	eq("False", r(code, data=None))
	eq("False", r(code, data=True))
	eq("False", r(code, data=False))
	eq("False", r(code, data=42))
	eq("False", r(code, data=4.2))
	eq("False", r(code, data="foo"))
	eq("True", r(code, data=datetime.datetime.now()))
	eq("False", r(code, data=()))
	eq("False", r(code, data=[]))
	eq("False", r(code, data={}))
	eq("False", r(code, data=ul4c.Template("")))
	eq("False", r(code, data=color.red))


@pytest.mark.ul4
def test_function_islist(r):
	code = "<?print islist(data)?>"

	raises(argumentmismatchmessage, r("<?print islist()?>"))
	raises(argumentmismatchmessage, r("<?print islist(1, 2)?>"))
	eq("False", r(code, data=None))
	eq("False", r(code, data=True))
	eq("False", r(code, data=False))
	eq("False", r(code, data=42))
	eq("False", r(code, data=4.2))
	eq("False", r(code, data="foo"))
	eq("False", r(code, data=datetime.datetime.now()))
	eq("True", r(code, data=()))
	eq("True", r(code, data=[]))
	eq("True", r(code, data=PseudoList([])))
	eq("False", r(code, data={}))
	eq("False", r(code, data=ul4c.Template("")))
	eq("False", r(code, data=color.red))


@pytest.mark.ul4
def test_function_isdict(r):
	code = "<?print isdict(data)?>"

	raises(argumentmismatchmessage, r("<?print isdict()?>"))
	raises(argumentmismatchmessage, r("<?print isdict(1, 2)?>"))
	eq("False", r(code, data=None))
	eq("False", r(code, data=True))
	eq("False", r(code, data=False))
	eq("False", r(code, data=42))
	eq("False", r(code, data=4.2))
	eq("False", r(code, data="foo"))
	eq("False", r(code, data=datetime.datetime.now()))
	eq("False", r(code, data=()))
	eq("False", r(code, data=[]))
	eq("True", r(code, data={}))
	eq("True", r(code, data=PseudoDict({})))
	eq("False", r(code, data=ul4c.Template("")))
	eq("False", r(code, data=color.red))


@pytest.mark.ul4
def test_function_istemplate(r):
	code = "<?print istemplate(data)?>"

	raises(argumentmismatchmessage, r("<?print istemplate()?>"))
	raises(argumentmismatchmessage, r("<?print istemplate(1, 2)?>"))
	eq("False", r(code, data=None))
	eq("False", r(code, data=True))
	eq("False", r(code, data=False))
	eq("False", r(code, data=42))
	eq("False", r(code, data=4.2))
	eq("False", r(code, data="foo"))
	eq("False", r(code, data=datetime.datetime.now()))
	eq("False", r(code, data=()))
	eq("False", r(code, data=[]))
	eq("False", r(code, data={}))
	eq("True", r(code, data=ul4c.Template("")))
	eq("False", r(code, data=color.red))


@pytest.mark.ul4
def test_function_iscolor(r):
	code = "<?print iscolor(data)?>"

	raises(argumentmismatchmessage, r("<?print iscolor()?>"))
	raises(argumentmismatchmessage, r("<?print iscolor(1, 2)?>"))
	eq("False", r(code, data=None))
	eq("False", r(code, data=True))
	eq("False", r(code, data=False))
	eq("False", r(code, data=42))
	eq("False", r(code, data=4.2))
	eq("False", r(code, data="foo"))
	eq("False", r(code, data=datetime.datetime.now()))
	eq("False", r(code, data=()))
	eq("False", r(code, data=[]))
	eq("False", r(code, data={}))
	eq("False", r(code, data=ul4c.Template("")))
	eq("True", r(code, data=color.red))


@pytest.mark.ul4
def test_function_get(r):
	raises(argumentmismatchmessage, r("<?print get()?>"))
	eq("", r("<?print get('x')?>"))
	eq("42", r("<?print get('x')?>", x=42))
	eq("17", r("<?print get('x', 17)?>"))
	eq("42", r("<?print get('x', 17)?>", x=42))


@pytest.mark.ul4
def test_function_repr(r):
	code = "<?print repr(data)?>"

	raises(argumentmismatchmessage, r("<?print repr()?>"))
	raises(argumentmismatchmessage, r("<?print repr(1, 2)?>"))
	eq("None", r(code, data=None))
	eq("True", r(code, data=True))
	eq("False", r(code, data=False))
	eq("42", r(code, data=42))
	evaleq(42.5, r(code, data=42.5))
	contains(('"foo"', "'foo'"), r(code, data="foo"))
	evaleq([1, 2, 3], r(code, data=[1, 2, 3]))
	if r is not RenderJS:
		evaleq([1, 2, 3], r(code, data=(1, 2, 3)))
	evaleq({"a": 1, "b": 2}, r(code, data={"a": 1, "b": 2}))
	eq("@(2011-02-07T12:34:56.123000)", r(code, data=datetime.datetime(2011, 2, 7, 12, 34, 56, 123000)))
	eq("@(2011-02-07T12:34:56)", r(code, data=datetime.datetime(2011, 2, 7, 12, 34, 56)))
	eq("@(2011-02-07)", r(code, data=datetime.datetime(2011, 2, 7)))
	eq("@(2011-02-07)", r(code, data=datetime.date(2011, 2, 7)))


@pytest.mark.ul4
def test_method_format(r):
	t = datetime.datetime(2011, 2, 6, 12, 34, 56, 987000)
	code = "<?print format(data, format)?>"

	eq("2011", r(code, format="%Y", data=t))
	eq("02", r(code, format="%m", data=t))
	eq("06", r(code, format="%d", data=t))
	eq("12", r(code, format="%H", data=t))
	eq("34", r(code, format="%M", data=t))
	eq("56", r(code, format="%S", data=t))
	eq("987000", r(code, format="%f", data=t))
	contains(("Sun", "So"), r(code, format="%a", data=t))
	contains(("Sunday", "Sonntag"), r(code, format="%A", data=t))
	eq("Feb", r(code, format="%b", data=t))
	contains(("February", "Februar"), r(code, format="%B", data=t))
	eq("12", r(code, format="%I", data=t))
	eq("037", r(code, format="%j", data=t))
	eq("PM", r(code, format="%p", data=t))
	eq("06", r(code, format="%U", data=t))
	eq("0", r(code, format="%w", data=t))
	eq("05", r(code, format="%W", data=t))
	eq("11", r(code, format="%y", data=t))
	contains(("Sun Feb  6 12:34:56 2011", "So Feb  6 12:34:56 2011"), r(code, format="%c", data=t))
	eq("02/06/11", r(code, format="%x", data=t))
	eq("12:34:56", r(code, format="%X", data=t))
	eq("%", r(code, format="%%", data=t))


@pytest.mark.ul4
def test_function_chr(r):
	code = "<?print chr(data)?>"

	raises(argumentmismatchmessage, r("<?print chr()?>"))
	raises(argumentmismatchmessage, r("<?print chr(1, 2)?>"))
	eq("\x00", r(code, data=0))
	eq("a", r(code, data=ord("a")))
	eq("\u20ac", r(code, data=0x20ac))


@pytest.mark.ul4
def test_function_ord(r):
	code = "<?print ord(data)?>"

	raises(argumentmismatchmessage, r("<?print ord()?>"))
	raises(argumentmismatchmessage, r("<?print ord(1, 2)?>"))
	eq("0", r(code, data="\x00"))
	eq(str(ord("a")), r(code, data="a"))
	eq(str(0x20ac), r(code, data="\u20ac"))


@pytest.mark.ul4
def test_function_hex(r):
	code = "<?print hex(data)?>"

	raises(argumentmismatchmessage, r("<?print hex()?>"))
	raises(argumentmismatchmessage, r("<?print hex(1, 2)?>"))
	eq("0x0", r(code, data=0))
	eq("0xff", r(code, data=0xff))
	eq("0xffff", r(code, data=0xffff))
	eq("-0xffff", r(code, data=-0xffff))


@pytest.mark.ul4
def test_function_oct(r):
	code = "<?print oct(data)?>"

	raises(argumentmismatchmessage, r("<?print oct()?>"))
	raises(argumentmismatchmessage, r("<?print oct(1, 2)?>"))
	eq("0o0", r(code, data=0))
	eq("0o77", r(code, data=0o77))
	eq("0o7777", r(code, data=0o7777))
	eq("-0o7777", r(code, data=-0o7777))


@pytest.mark.ul4
def test_function_bin(r):
	code = "<?print bin(data)?>"

	raises(argumentmismatchmessage, r("<?print bin()?>"))
	raises(argumentmismatchmessage, r("<?print bin(1, 2)?>"))
	eq("0b0", r(code, data=0b0))
	eq("0b11", r(code, data=0b11))
	eq("-0b1111", r(code, data=-0b1111))


@pytest.mark.ul4
def test_function_abs(r):
	code = "<?print abs(data)?>"

	raises(argumentmismatchmessage, r("<?print abs()?>"))
	raises(argumentmismatchmessage, r("<?print abs(1, 2)?>"))
	eq("0", r(code, data=0))
	eq("42", r(code, data=42))
	eq("42", r(code, data=-42))


@pytest.mark.ul4
def test_function_sorted(r):
	code = "<?for i in sorted(data)?><?print i?><?end for?>"

	raises(argumentmismatchmessage, r("<?print sorted()?>"))
	eq("gkru", r(code, data="gurk"))
	eq("24679", r(code, data="92746"))
	eq("172342", r(code, data=(42, 17, 23)))
	eq("012", r(code, data={0: "zero", 1: "one", 2: "two"}))


@pytest.mark.ul4
def test_function_range(r):
	code1 = "<?for i in range(data)?><?print i?>;<?end for?>"
	code2 = "<?for i in range(data[0], data[1])?><?print i?>;<?end for?>"
	code3 = "<?for i in range(data[0], data[1], data[2])?><?print i?>;<?end for?>"

	raises(argumentmismatchmessage, r("<?print range()?>"))
	eq("", r(code1, data=-10))
	eq("", r(code1, data=0))
	eq("0;", r(code1, data=1))
	eq("0;1;2;3;4;", r(code1, data=5))
	eq("", r(code2, data=[0, -10]))
	eq("", r(code2, data=[0, 0]))
	eq("0;1;2;3;4;", r(code2, data=[0, 5]))
	eq("-5;-4;-3;-2;-1;0;1;2;3;4;", r(code2, data=[-5, 5]))
	eq("", r(code3, data=[0, -10, 1]))
	eq("", r(code3, data=[0, 0, 1]))
	eq("0;2;4;6;8;", r(code3, data=[0, 10, 2]))
	eq("", r(code3, data=[0, 10, -2]))
	eq("10;8;6;4;2;", r(code3, data=[10, 0, -2]))
	eq("", r(code3, data=[10, 0, 2]))


@pytest.mark.ul4
def test_function_urlquote(r):
	eq("gurk", r("<?print urlquote('gurk')?>"))
	eq("%3C%3D%3E%2B%3F", r("<?print urlquote('<=>+?')?>"))
	eq("%7F%C3%BF%EF%BF%BF", r("<?print urlquote('\u007f\u00ff\uffff')?>"))


@pytest.mark.ul4
def test_function_urlunquote(r):
	eq("gurk", r("<?print urlunquote('gurk')?>"))
	eq("<=>+?", r("<?print urlunquote('%3C%3D%3E%2B%3F')?>"))
	eq("\u007f\u00ff\uffff", r("<?print urlunquote('%7F%C3%BF%EF%BF%BF')?>"))


@pytest.mark.ul4
def test_function_zip(r):
	code0 = "<?for i in zip()?><?print i?>;<?end for?>"
	code1 = "<?for (ix, ) in zip(x)?><?print ix?>;<?end for?>"
	code2 = "<?for (ix, iy) in zip(x, y)?><?print ix?>-<?print iy?>;<?end for?>"
	code3 = "<?for (ix, iy, iz) in zip(x, y, z)?><?print ix?>-<?print iy?>+<?print iz?>;<?end for?>"

	eq("", r(code0))
	eq("1;2;", r(code1, x=[1, 2]))
	eq("", r(code2, x=[], y=[]))
	eq("1-3;2-4;", r(code2, x=[1, 2], y=[3, 4]))
	eq("1-4;2-5;", r(code2, x=[1, 2, 3], y=[4, 5]))
	eq("", r(code3, x=[], y=[], z=[]))
	eq("1-3+5;2-4+6;", r(code3, x=[1, 2], y=[3, 4], z=[5, 6]))
	eq("1-4+6;", r(code3, x=[1, 2, 3], y=[4, 5], z=[6]))


@pytest.mark.ul4
def test_function_type(r):
	code = "<?print type(x)?>"

	raises(argumentmismatchmessage, r("<?print type()?>"))
	raises(argumentmismatchmessage, r("<?print type(1, 2)?>"))
	eq("none", r(code, x=None))
	eq("bool", r(code, x=False))
	eq("bool", r(code, x=True))
	eq("int", r(code, x=42))
	eq("float", r(code, x=4.2))
	eq("str", r(code, x="foo"))
	eq("date", r(code, x=datetime.datetime.now()))
	eq("date", r(code, x=datetime.date.today()))
	eq("list", r(code, x=(1, 2)))
	eq("list", r(code, x=[1, 2]))
	eq("list", r(code, x=PseudoList([1, 2])))
	eq("dict", r(code, x={1: 2}))
	eq("dict", r(code, x=PseudoDict({1: 2})))
	eq("template", r(code, x=ul4c.Template("")))
	eq("color", r(code, x=color.red))


@pytest.mark.ul4
def test_function_reversed(r):
	code = "<?for i in reversed(x)?>(<?print i?>)<?end for?>"

	raises(argumentmismatchmessage, r("<?print reversed()?>"))
	raises(argumentmismatchmessage, r("<?print reversed(1, 2)?>"))
	eq("(3)(2)(1)", r(code, x="123"))
	eq("(3)(2)(1)", r(code, x=[1, 2, 3]))
	eq("(3)(2)(1)", r(code, x=(1, 2, 3)))


@pytest.mark.ul4
def test_function_min(r):
	raises(argumentmismatchmessage, r("<?print min()?>"))
	raises("empty sequence", r("<?print min([])?>"))
	eq("1", r("<?print min('123')?>"))
	eq("1", r("<?print min(1, 2, 3)?>"))
	eq("0", r("<?print min(0, False, 1, True)?>"))
	eq("False", r("<?print min(False, 0, True, 1)?>"))
	eq("False", r("<?print min([False, 0, True, 1])?>"))


@pytest.mark.ul4
def test_function_max(r):
	raises(argumentmismatchmessage, r("<?print max()?>"))
	raises("empty sequence", r("<?print max([])?>"))
	eq("3", r("<?print max('123')?>"))
	eq("3", r("<?print max(1, 2, 3)?>"))
	eq("1", r("<?print max(0, False, 1, True)?>"))
	eq("True", r("<?print max(False, 0, True, 1)?>"))
	eq("True", r("<?print max([False, 0, True, 1])?>"))


@pytest.mark.ul4
def test_function_rgb(r):
	eq("#369", r("<?print repr(rgb(0.2, 0.4, 0.6))?>"))
	eq("#369c", r("<?print repr(rgb(0.2, 0.4, 0.6, 0.8))?>"))


@pytest.mark.ul4
def test_function_hls(r):
	eq("#fff", r("<?print repr(hls(0, 1, 0))?>"))
	eq("#fff0", r("<?print repr(hls(0, 1, 0, 0))?>"))


@pytest.mark.ul4
def test_function_hsv(r):
	eq("#fff", r("<?print repr(hsv(0, 0, 1))?>"))
	eq("#fff0", r("<?print repr(hsv(0, 0, 1, 0))?>"))


@pytest.mark.ul4
def test_method_upper(r):
	eq("GURK", r("<?print 'gurk'.upper()?>"))


@pytest.mark.ul4
def test_method_lower(r):
	eq("gurk", r("<?print 'GURK'.lower()?>"))


@pytest.mark.ul4
def test_method_capitalize(r):
	eq("Gurk", r("<?print 'gURK'.capitalize()?>"))


@pytest.mark.ul4
def test_method_startswith(r):
	eq("True", r("<?print 'gurkhurz'.startswith('gurk')?>"))
	eq("False", r("<?print 'gurkhurz'.startswith('hurz')?>"))


@pytest.mark.ul4
def test_method_endswith(r):
	eq("True", r("<?print 'gurkhurz'.endswith('hurz')?>"))
	eq("False", r("<?print 'gurkhurz'.endswith('gurk')?>"))


@pytest.mark.ul4
def test_method_strip(r):
	eq("gurk", r(r"<?print obj.strip()?>", obj=' \t\r\ngurk \t\r\n'))
	eq("gurk", r(r"<?print obj.strip('xyz')?>", obj='xyzzygurkxyzzy'))


@pytest.mark.ul4
def test_method_lstrip(r):
	eq("gurk \t\r\n", r("<?print obj.lstrip()?>", obj=" \t\r\ngurk \t\r\n"))
	eq("gurkxyzzy", r("<?print obj.lstrip(arg)?>", obj="xyzzygurkxyzzy", arg="xyz"))


@pytest.mark.ul4
def test_method_rstrip(r):
	eq(" \t\r\ngurk", r("<?print obj.rstrip()?>", obj=" \t\r\ngurk \t\r\n"))
	eq("xyzzygurk", r("<?print obj.rstrip(arg)?>", obj="xyzzygurkxyzzy", arg="xyz"))


@pytest.mark.ul4
def test_method_split(r):
	eq("(f)(o)(o)", r("<?for item in obj.split()?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n"))
	eq("(f)(o \t\r\no \t\r\n)", r("<?for item in obj.split(None, 1)?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n"))
	eq("()(f)(o)(o)()", r("<?for item in obj.split(arg)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx"))
	eq("()(f)(oxxoxx)", r("<?for item in obj.split(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx"))


@pytest.mark.ul4
def test_method_rsplit(r):
	eq("(f)(o)(o)", r("<?for item in obj.rsplit()?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n"))
	eq("( \t\r\nf \t\r\no)(o)", r("<?for item in obj.rsplit(None, 1)?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n"))
	eq("()(f)(o)(o)()", r("<?for item in obj.rsplit(arg)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx"))
	eq("(xxfxxo)(o)()", r("<?for item in obj.rsplit(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx"))


@pytest.mark.ul4
def test_method_replace(r):
	eq('goork', r(r"<?print 'gurk'.replace('u', 'oo')?>"))


@pytest.mark.ul4
def test_method_renders(r):
	t = ul4c.Template('(<?print data?>)')
	eq('(GURK)', r("<?print t.renders(data='gurk').upper()?>", t=t))
	eq('(GURK)', r("<?print t.renders(**{'data': 'gurk'}).upper()?>", t=t))

	t = ul4c.Template('(gurk)')
	eq('(GURK)', r("<?print t.renders().upper()?>", t=t))


@pytest.mark.ul4
def test_method_mimeformat(r):
	t = datetime.datetime(2010, 2, 22, 12, 34, 56)

	eq('Mon, 22 Feb 2010 12:34:56 GMT', r(r"<?print data.mimeformat()?>", data=t))


@pytest.mark.ul4
def test_method_get(r):
	eq("42", r("<?print {}.get('foo', 42)?>"))
	eq("17", r("<?print {'foo': 17}.get('foo', 42)?>"))
	eq("", r("<?print {}.get('foo')?>"))
	eq("17", r("<?print {'foo': 17}.get('foo')?>"))


@pytest.mark.ul4
def test_method_r_g_b_a(r):
	eq('0x11', r('<?code c = #123?><?print hex(c.r())?>'))
	eq('0x22', r('<?code c = #123?><?print hex(c.g())?>'))
	eq('0x33', r('<?code c = #123?><?print hex(c.b())?>'))
	eq('0xff', r('<?code c = #123?><?print hex(c.a())?>'))


@pytest.mark.ul4
def test_method_hls(r):
	eq('0', r('<?code c = #fff?><?print int(c.hls()[0])?>'))
	eq('1', r('<?code c = #fff?><?print int(c.hls()[1])?>'))
	eq('0', r('<?code c = #fff?><?print int(c.hls()[2])?>'))


@pytest.mark.ul4
def test_method_hlsa(r):
	eq('0', r('<?code c = #fff?><?print int(c.hlsa()[0])?>'))
	eq('1', r('<?code c = #fff?><?print int(c.hlsa()[1])?>'))
	eq('0', r('<?code c = #fff?><?print int(c.hlsa()[2])?>'))
	eq('1', r('<?code c = #fff?><?print int(c.hlsa()[3])?>'))


@pytest.mark.ul4
def test_method_hsv(r):
	eq('0', r('<?code c = #fff?><?print int(c.hsv()[0])?>'))
	eq('0', r('<?code c = #fff?><?print int(c.hsv()[1])?>'))
	eq('1', r('<?code c = #fff?><?print int(c.hsv()[2])?>'))


@pytest.mark.ul4
def test_method_hsva(r):
	eq('0', r('<?code c = #fff?><?print int(c.hsva()[0])?>'))
	eq('0', r('<?code c = #fff?><?print int(c.hsva()[1])?>'))
	eq('1', r('<?code c = #fff?><?print int(c.hsva()[2])?>'))
	eq('1', r('<?code c = #fff?><?print int(c.hsva()[3])?>'))


@pytest.mark.ul4
def test_method_lum(r):
	eq('True', r('<?print #fff.lum() == 1?>'))


@pytest.mark.ul4
def test_method_withlum(r):
	eq('#fff', r('<?print #000.withlum(1)?>'))


@pytest.mark.ul4
def test_method_witha(r):
	eq('#0063a82a', r('<?print repr(#0063a8.witha(42))?>'))


@pytest.mark.ul4
def test_method_join(r):
	eq('1,2,3,4', r('<?print ",".join("1234")?>'))
	eq('1,2,3,4', r('<?print ",".join([1, 2, 3, 4])?>'))


@pytest.mark.ul4
def test_method_find(r):
	s = "gurkgurk"
	eq('-1', r('<?print s.find("ks")?>', s=s))
	eq('2', r('<?print s.find("rk")?>', s=s))
	eq('2', r('<?print s.find("rk", 2)?>', s=s))
	eq('6', r('<?print s.find("rk", -3)?>', s=s))
	eq('2', r('<?print s.find("rk", 2, 4)?>', s=s))
	eq('6', r('<?print s.find("rk", 4, 8)?>', s=s))
	eq('5', r('<?print s.find("ur", -4, -1)?>', s=s))
	eq('-1', r('<?print s.find("rk", 2, 3)?>', s=s))
	eq('-1', r('<?print s.find("rk", 7)?>', s=s))
	l = list("gurkgurk")
	eq('-1', r('<?print l.find("x")?>', l=l))
	eq('2', r('<?print l.find("r")?>', l=l))
	eq('2', r('<?print l.find("r", 2)?>', l=l))
	eq('6', r('<?print l.find("r", -3)?>', l=l))
	eq('2', r('<?print l.find("r", 2, 4)?>', l=l))
	eq('6', r('<?print l.find("r", 4, 8)?>', l=l))
	eq('6', r('<?print l.find("r", -3, -1)?>', l=l))
	eq('-1', r('<?print l.find("r", 2, 2)?>', l=l))
	eq('-1', r('<?print l.find("r", 7)?>', l=l))
	eq('1', r('<?print l.find(None)?>', l=[0, None, 1, None, 2, None, 3, None]))


@pytest.mark.ul4
def test_method_rfind(r):
	s = "gurkgurk"
	eq('-1', r('<?print s.rfind("ks")?>', s=s))
	eq('6', r('<?print s.rfind("rk")?>', s=s))
	eq('6', r('<?print s.rfind("rk", 2)?>', s=s))
	eq('6', r('<?print s.rfind("rk", -3)?>', s=s))
	eq('2', r('<?print s.rfind("rk", 2, 4)?>', s=s))
	eq('6', r('<?print s.rfind("rk", 4, 8)?>', s=s))
	eq('5', r('<?print s.rfind("ur", -4, -1)?>', s=s))
	eq('-1', r('<?print s.rfind("rk", 2, 3)?>', s=s))
	eq('-1', r('<?print s.rfind("rk", 7)?>', s=s))
	l = list("gurkgurk")
	eq('-1', r('<?print l.rfind("x")?>', l=l))
	eq('6', r('<?print l.rfind("r")?>', l=l))
	eq('6', r('<?print l.rfind("r", 2)?>', l=l))
	eq('2', r('<?print l.rfind("r", 2, 4)?>', l=l))
	eq('6', r('<?print l.rfind("r", 4, 8)?>', l=l))
	eq('6', r('<?print l.rfind("r", -3, -1)?>', l=l))
	eq('-1', r('<?print l.rfind("r", 2, 2)?>', l=l))
	eq('-1', r('<?print l.rfind("r", 7)?>', l=l))
	eq('7', r('<?print l.rfind(None)?>', l=[0, None, 1, None, 2, None, 3, None]))


@pytest.mark.ul4
def test_method_day(r):
	eq('12', r('<?print @(2010-05-12).day()?>'))
	eq('12', r('<?print d.day()?>', d=datetime.date(2010, 5, 12)))


@pytest.mark.ul4
def test_method_month(r):
	eq('5', r('<?print @(2010-05-12).month()?>'))
	eq('5', r('<?print d.month()?>', d=datetime.date(2010, 5, 12)))


@pytest.mark.ul4
def test_method_year(r):
	eq('5', r('<?print @(2010-05-12).month()?>'))
	eq('5', r('<?print d.month()?>', d=datetime.date(2010, 5, 12)))


@pytest.mark.ul4
def test_method_hour(r):
	eq('16', r('<?print @(2010-05-12T16:47:56).hour()?>'))
	eq('16', r('<?print d.hour()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56)))


@pytest.mark.ul4
def test_method_minute(r):
	eq('47', r('<?print @(2010-05-12T16:47:56).minute()?>'))
	eq('47', r('<?print d.minute()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56)))


@pytest.mark.ul4
def test_method_second(r):
	eq('56', r('<?print @(2010-05-12T16:47:56).second()?>'))
	eq('56', r('<?print d.second()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56)))


@pytest.mark.ul4
def test_method_microsecond(r):
	eq('123000', r('<?print @(2010-05-12T16:47:56.123000).microsecond()?>'))
	eq('123000', r('<?print d.microsecond()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56, 123000)))


@pytest.mark.ul4
def test_method_weekday(r):
	eq('2', r('<?print @(2010-05-12).weekday()?>'))
	eq('2', r('<?print d.weekday()?>', d=datetime.date(2010, 5, 12)))


@pytest.mark.ul4
def test_method_yearday(r):
	eq('1', r('<?print @(2010-01-01).yearday()?>'))
	eq('366', r('<?print @(2008-12-31).yearday()?>'))
	eq('365', r('<?print @(2010-12-31).yearday()?>'))
	eq('132', r('<?print @(2010-05-12).yearday()?>'))
	eq('132', r('<?print @(2010-05-12T16:47:56).yearday()?>'))
	eq('132', r('<?print d.yearday()?>', d=datetime.date(2010, 5, 12)))
	eq('132', r('<?print d.yearday()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56)))


@pytest.mark.ul4
def test_render(r):
	t = ul4c.Template('<?print prefix?><?print data?><?print suffix?>')

	eq('(f)(o)(o)', r('<?for c in data?><?render t.render(data=c, prefix="(", suffix=")")?><?end for?>', t=t, data='foo'))
	eq('(f)(o)(o)', r('<?for c in data?><?render t.render(data=c, **{"prefix": "(", "suffix": ")"})?><?end for?>', t=t, data='foo'))


@pytest.mark.ul4
def test_render_var(r):
	t = ul4c.Template('<?code x += 1?><?print x?>')

	eq('42,43,42', r('<?print x?>,<?render t.render(x=x)?>,<?print x?>', t=t, x=42))


@pytest.mark.ul4
def test_def(r):
	eq('foo', r('<?def lower?><?print x.lower()?><?end def?><?print lower.renders(x="FOO")?>'))


@pytest.mark.ul4
def test_parse(r):
	eq('42', r('<?print data.Noner?>', data=dict(Noner=42)))


@pytest.mark.ul4
def test_nested_exceptions(r):
	tmpl1 = ul4c.Template("<?print 2*x?>", "tmpl1")
	tmpl2 = ul4c.Template("<?render tmpl1.render(x=x)?>", "tmpl2")
	tmpl3 = ul4c.Template("<?render tmpl2.render(tmpl1=tmpl1, x=x)?>", "tmpl3")

	msg = "TypeError: unsupported operand type\\(s\\) for \\*: 'int' and 'NoneType'|.* \\* .* not supported"
	raises(msg, r("<?render tmpl3.render(tmpl1=tmpl1, tmpl2=tmpl2, x=x)?>", tmpl1=tmpl1, tmpl2=tmpl2, tmpl3=tmpl3, x=None))


@pytest.mark.ul4
def test_note(r):
	eq("foo", r("f<?note This is?>o<?note a comment?>o"))


@pytest.mark.ul4
def test_templateattributes(r):
	s1 = "<?print x?>"
	t1 = ul4c.Template(s1)

	s2 = "<?printx 42?>"
	t2 = ul4c.Template(s2)

	if r is not RenderJavaCompiledTemplateByPython:
		eq("<?", r("<?print template.startdelim?>", template=t1))
		eq("?>", r("<?print template.enddelim?>", template=t1))
		eq(s1, r("<?print template.source?>", template=t1))
		eq("1", r("<?print len(template.content)?>", template=t1))
		eq("print", r("<?print template.content[0].type?>", template=t1))
		eq(s1, r("<?print template.content[0].location.tag?>", template=t1))
		eq("x", r("<?print template.content[0].location.code?>", template=t1))
		eq("var", r("<?print template.content[0].obj.type?>", template=t1))
		eq("x", r("<?print template.content[0].obj.name?>", template=t1))
		eq("printx", r("<?print template.content[0].type?>", template=t2))
		eq("int", r("<?print template.content[0].obj.type?>", template=t2))
		eq("42", r("<?print template.content[0].obj.value?>", template=t2))


@pytest.mark.ul4
def test_templateattributes_localtemplate(r):
	source = "<?def lower?><?print t.lower()?><?end def?>"

	if r is not RenderJavaCompiledTemplateByPython:
		eq(source + "<?print lower.source?>", r(source + "<?print lower.source?>"))
		eq(source, r(source + "<?print lower.source[lower.location.starttag:lower.endlocation.endtag]?>"))
		eq("<?print t.lower()?>", r(source + "<?print lower.source[lower.location.endtag:lower.endlocation.starttag]?>"))
		eq("lower", r(source + "<?print lower.name?>"))


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


@pytest.mark.ul4
def test_strtemplate():
	t = universaltemplate()
	str(t)


@pytest.mark.ul4
def test_pythonsource():
	t = universaltemplate()
	t.pythonsource()


@pytest.mark.ul4
def test_pythonfunction():
	t = universaltemplate()
	t.pythonfunction()


@pytest.mark.ul4
def test_jssource():
	t = universaltemplate()
	t.jssource()


@pytest.mark.ul4
def test_javasource():
	t = universaltemplate()
	t.javasource()


@pytest.mark.ul4
def test_attr_if(r):
	cond = ul4.attr_if(html.a("gu'\"rk"), cond="cond")

	s = html.div(class_=cond).conv().string()
	eq('<div></div>', r(s, cond=False))
	eq('''<div class="gu'&quot;rk"></div>''', r(s, cond=True))

	s = html.div(class_=(cond, "hurz")).conv().string()
	eq('<div class="hurz"></div>', r(s, cond=False))
	eq('''<div class="gu'&quot;rkhurz"></div>''', r(s, cond=True))

	s = cond.conv().string()
	eq('', r(s, cond=False))
	eq('''<a>gu'"rk</a>''', r(s, cond=True))

	s = html.ul(compact=ul4.attr_if(True, cond="cond")).conv().string()
	eq('<ul></ul>', r(s, cond=False))
	eq('''<ul compact="compact"></ul>''', r(s, cond=True))
