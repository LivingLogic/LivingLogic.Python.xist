#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009-2012 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2012 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import sys, os, re, datetime, io, json, contextlib, tempfile, collections, shutil, subprocess

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


def render_python(__, **variables):
	"""
	Compile the template from the source ``__`` and render it with the variables ``variables``.
	"""
	template = ul4c.Template(__)
	f = sys._getframe(1)
	print("Testing Python template ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
	print(template.pythonsource())
	return template.renders(**variables)


def render_python_dumps(__, **variables):
	"""
	Compile the template from the source ``__``, create a string dump from it,
	recreate the template from the dump string and render it with the variables
	``variables``.
	"""
	template = ul4c.Template(__)
	template = ul4c.Template.loads(template.dumps()) # Recreate the template from the binary dump
	f = sys._getframe(1)
	print("Testing Python template loaded from string ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
	print(template.pythonsource())
	return template.renders(**variables)


def render_python_dump(__, **variables):
	"""
	Compile the template from the source ``__``, dump it to a stream, recreate
	the template from the dump and render it with the variables ``variables``.
	"""
	template = ul4c.Template(__)
	stream = io.StringIO()
	template.dump(stream)
	stream.seek(0)
	f = sys._getframe(1)
	template = ul4c.Template.load(stream) # Recreate the template from the stream
	print("Testing Python template loaded from stream ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
	print(template.pythonsource())
	return template.renders(**variables)


def render_js(__, **variables):
	"""
	Compile the template from the source ``__``, and generate Javascript source
	from it that renders the template with the variables ``variables``.

	(this requires an installed ``d8`` shell from V8 (http://code.google.com/p/v8/))
	"""
	template = ul4c.Template(__)
	js = template.jssource()
	js = "template = {};\ndata = {};\nprint(template.renders(data));\n".format(js, ul4c._asjson(variables))
	f = sys._getframe(1)
	print("Testing Javascript code compiled by Python ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
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


def java_findexception(output):
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


def java_formatsource(string):
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


def java_runsource(source):
	"""
	Compile the Java source :var:`source`, run it and return the output
	"""
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

	tempdir = tempfile.mkdtemp()
	try:
		source = maincodetemplate % dict(source=source)
		source = java_formatsource(source)
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
		java_findexception(stderr.decode("utf-8"))
	finally:
		shutil.rmtree(tempdir)
	if stderr:
		print(stderr, file=sys.stderr)
	return stdout.decode("utf-8")



def render_java_interpretedtemplate_by_python(__, **variables):
	"""
	Compile the template from the source ``__``, and generate Java source that
	recreates the template from the Python generated dump and renders the
	template with the variables ``variables``.

	(this requires an installed Java compiler and the Java UL4 jar)
	"""

	codetemplate = """
	com.livinglogic.ul4.InterpretedTemplate template = %(template)s;
	java.util.Map<String, Object> variables = %(variables)s;
	String output = template.renders(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	f = sys._getframe(1)
	print("Testing Java InterpretedTemplate (compiled by Python) ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
	templatesource = ul4c.Template(__).javasource(interpreted=True)
	java = codetemplate % dict(variables=misc.javaexpr(variables), template=templatesource)
	return java_runsource(java)


def render_java_compiledtemplate_by_python(__, **variables):
	"""
	Compile the template from the source ``__``, and generate Java source that
	contains the template in compiled form and renders the template with the
	variables ``variables``.

	(this requires an installed Java compiler and the Java UL4 jar)
	"""

	codetemplate = """
	com.livinglogic.ul4.Template template = %(template)s;
	java.util.Map<String, Object> variables = %(variables)s;
	String output = template.renders(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	f = sys._getframe(1)
	print("Testing Java CompiledTemplate (compiled by Python) ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
	template = ul4c.Template(__)
	java = template.javasource(interpreted=False)
	java = codetemplate % dict(variables=misc.javaexpr(variables), template=java)
	return java_runsource(java)


def render_java_interpretedtemplate_by_java(__, **variables):
	"""
	Generate Java source that compiles the template source ``__`` and renders the
	template with the variables ``variables``.

	(this requires an installed Java compiler and the Java UL4 jar)
	"""

	codetemplate = """
	com.livinglogic.ul4.InterpretedTemplate template = new com.livinglogic.ul4.InterpretedTemplate(%(source)s);
	java.util.Map<String, Object> variables = %(variables)s;
	String output = template.renders(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	f = sys._getframe(1)
	print("Testing Java InterpretedTemplate (compiled by Java) ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
	java = codetemplate % dict(source=misc.javaexpr(__), variables=misc.javaexpr(variables))
	return java_runsource(java)


all_renderers =  [
	("python", render_python),
	("python_dumps", render_python_dumps),
	("python_dump", render_python_dump),
	("js", render_js),
	("java_interpreted_by_python", render_java_interpretedtemplate_by_python),
	("java_compiled_by_python", render_java_compiledtemplate_by_python),
	("java_interpreted_by_java", render_java_interpretedtemplate_by_java),
]


def pytest_generate_tests(metafunc):
	if "r" in metafunc.funcargnames:
		metafunc.parametrize("r", [r for (id, r) in all_renderers], ids=[id for (id, r) in all_renderers])


argumentmismatchmessage = [
	# Python argument mismatch exception messages
	"takes exactly \\d+ (positional )?arguments?", # < 3.3
	"expected \\d+ arguments?",
	"Required argument .* not found",
	"takes exactly (one|\\d+) arguments?",
	"expected at least \\d+ arguments", # < 3.3
	"takes at most \\d+ (positional )?arguments?",
	"takes at least \\d+ argument", #  < 3.3
	"takes no arguments",
	"expected at least \\d+ arguments",
	"missing \\d+ required positional arguments?", # 3.3
	"takes \\d+ positional arguments? but \\d+ (was|were) given", # 3.3
	"takes from \\d+ to \\d+ positional arguments but \\d+ (was|were) given", # 3.3
	# Javascript argument mismatch exception messages
	"requires (at least \\d+|\\d+(-\\d+)?) arguments?, \\d+ given",
	# Java compiler errors for argument mismatches
	"cannot find symbol",
	"cannot be applied",
	"The method .* is not applicable for the arguments",
	"no suitable method found for",
	# Java exception messages for argument mismatches
	"expects (at least \\d+|exactly \\d+|\\d+-\\d+) arguments?, \\d+ given",
]
argumentmismatchmessage = "({})".format("|".join(argumentmismatchmessage))


class raises(object):
	def __init__(self, msg):
		self.msg = re.compile(msg)

	def exceptionchain(self, exc):
		while exc is not None:
			yield exc
			exc = exc.__cause__

	def __enter__(self):
		pass

	def __exit__(self, type, value, traceback):
		if value is None:
			pytest.fail("failed to raise exception")
		# Check that any exception in the ``__cause__`` chain of the raised one matches a regexp
		exceptionmsgs = [str(exc) for exc in self.exceptionchain(value)]
		assert any(self.msg.search(msg) is not None for msg in exceptionmsgs)
		return True # Don't propagate exception


@pytest.mark.ul4
def test_text(r):
	assert 'gurk' == r('gurk')
	assert 'g\xfcrk' ==  r('g\xfcrk')


@pytest.mark.ul4
def test_none(r):
	assert '' == r('<?print None?>')
	assert 'no' == r('<?if None?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_false(r):
	assert 'False' == r('<?print False?>')
	assert 'no' == r('<?if False?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_true(r):
	assert 'True' == r('<?print True?>')
	assert 'yes' == r('<?if True?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_int(r):
	values = (0, 42, -42, 0x7ffffff, 0x8000000, -0x8000000, -0x8000001)
	if r is not render_js:
		# Since Javascript has no real integers the following would lead to rounding errors
		values += (0x7ffffffffffffff, 0x800000000000000, -0x800000000000000, -0x800000000000001, 9999999999, -9999999999, 99999999999999999999, -99999999999999999999)
	for value in values:
		assert str(value) == r('<?print {}?>'.format(value))
	assert '255' == r('<?print 0xff?>')
	assert '255' == r('<?print 0Xff?>')
	assert '-255' == r('<?print -0xff?>')
	assert '-255' == r('<?print -0Xff?>')
	assert '63' == r('<?print 0o77?>')
	assert '63' == r('<?print 0O77?>')
	assert '-63' == r('<?print -0o77?>')
	assert '-63' == r('<?print -0O77?>')
	assert '7' == r('<?print 0b111?>')
	assert '7' == r('<?print 0B111?>')
	assert '-7' == r('<?print -0b111?>')
	assert '-7' == r('<?print -0B111?>')

	assert 'no' == r('<?if 0?>yes<?else?>no<?end if?>')
	assert 'yes' == r('<?if 1?>yes<?else?>no<?end if?>')
	assert 'yes' == r('<?if -1?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_float(r):
	# str() output might differ slightly between Python and JS, so eval the output again for tests
	assert 0.0 == eval(r('<?print 0.?>'))
	assert 42.0 == eval(r('<?print 42.?>'))
	assert -42.0 == eval(r('<?print -42.?>'))
	assert -42.5 == eval(r('<?print -42.5?>'))
	assert 1e42 == eval(r('<?print 1E42?>'))
	assert 1e42 == eval(r('<?print 1e42?>'))
	assert -1e42 == eval(r('<?print -1E42?>'))
	assert -1e42 == eval(r('<?print -1e42?>'))

	assert 'no' == r('<?if 0.?>yes<?else?>no<?end if?>')
	assert 'yes' == r('<?if 1.?>yes<?else?>no<?end if?>')
	assert 'yes' == r('<?if -1.?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_string(r):
	with raises("Unterminated string|mismatched character|MismatchedTokenException"):
		r('<?print "?>')
	assert 'foo' == r('<?print "foo"?>')
	assert '\n' == r('<?print "\\n"?>')
	assert '\r' == r('<?print "\\r"?>')
	assert '\t' == r('<?print "\\t"?>')
	assert '\f' == r('<?print "\\f"?>')
	assert '\b' == r('<?print "\\b"?>')
	assert '\a' == r('<?print "\\a"?>')
	assert '\x1b' == r('<?print "\\e"?>')
	assert '\x00' == r('<?print "\\x00"?>')
	assert '"' == r('<?print "\\""?>')
	assert "'" == r('<?print "\\\'"?>')
	assert '\u20ac' == r('<?print "\u20ac"?>')
	assert '\xff' == r('<?print "\\xff"?>')
	assert '\u20ac' == r('''<?print "\\u20ac"?>''')
	assert "a\nb" == r('<?print "a\nb"?>')
	for c in "\x00\x80\u0100\u3042\n\r\t\f\b\a\e\"":
		assert c == r('<?print obj?>', obj=c) # This tests :func:`misc.javaexpr` for Java and :func:`ul4c._asjson` for JS

	# Test literal control characters
	assert 'gu\n\r\trk' == r("<?print 'gu\n\r\trk'?>")
	assert 'gu\n\r\t\\rk' == r(r"<?print 'gu\n\r\t\\rk'?>")

	assert 'no' == r('<?if ""?>yes<?else?>no<?end if?>')
	assert 'yes' == r('<?if "foo"?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_date(r):
	assert '2000-02-29' == r('<?print @(2000-02-29).isoformat()?>')
	assert '2000-02-29' == r('<?print @(2000-02-29T).isoformat()?>')
	assert '2000-02-29T12:34:00' == r('<?print @(2000-02-29T12:34).isoformat()?>')
	assert '2000-02-29T12:34:56' == r('<?print @(2000-02-29T12:34:56).isoformat()?>')
	assert '2000-02-29T12:34:56.987000' == r('<?print @(2000-02-29T12:34:56.987000).isoformat()?>') # JS and Java only supports milliseconds
	assert 'yes' == r('<?if @(2000-02-29T12:34:56.987654)?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_color(r):
	assert '255,255,255,255' == r('<?code c = #fff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	assert '255,255,255,255' == r('<?code c = #ffffff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	assert '18,52,86,255' == r('<?code c = #123456?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	assert '17,34,51,68' == r('<?code c = #1234?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	assert '18,52,86,120' == r('<?code c = #12345678?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
	assert 'yes' == r('<?if #fff?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_list(r):
	assert '' == r('<?for item in []?><?print item?>;<?end for?>')
	assert '1;' == r('<?for item in [1]?><?print item?>;<?end for?>')
	assert '1;' == r('<?for item in [1,]?><?print item?>;<?end for?>')
	assert '1;2;' == r('<?for item in [1, 2]?><?print item?>;<?end for?>')
	assert '1;2;' == r('<?for item in [1, 2,]?><?print item?>;<?end for?>')
	assert 'no' == r('<?if []?>yes<?else?>no<?end if?>')
	assert 'yes' == r('<?if [1]?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_listcomp(r):
	assert "[2, 6]" == r("<?code d = [2*i for i in range(4) if i%2]?><?print d?>")
	assert "[0, 2, 4, 6]" == r("<?code d = [2*i for i in range(4)]?><?print d?>")


@pytest.mark.ul4
def test_genexpr(r):
	assert "2, 6:" == r("<?code ge = (str(2*i) for i in range(4) if i%2)?><?print ', '.join(ge)?>:<?print ', '.join(ge)?>")
	assert "2, 6" == r("<?print ', '.join(str(2*i) for i in range(4) if i%2)?>")
	assert "0, 2, 4, 6" == r("<?print ', '.join(str(2*i) for i in range(4))?>")
	assert "0, 2, 4, 6" == r("<?print ', '.join((str(2*i) for i in range(4)))?>")


@pytest.mark.ul4
def test_dict(r):
	assert '' == r('<?for (key, value) in {}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert '1:2\n' == r('<?for (key, value) in {1:2}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert '1:#fff\n' == r('<?for (key, value) in {1:#fff}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert '1:2\n' == r('<?for (key, value) in {1:2,}.items()?><?print key?>:<?print value?>\n<?end for?>')
	# With duplicate keys, later ones simply overwrite earlier ones
	assert '1:3\n' == r('<?for (key, value) in {1:2, 1: 3}.items()?><?print key?>:<?print value?>\n<?end for?>')
	# Test **
	assert '1:2\n' == r('<?for (key, value) in {**{1:2}}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert '1:4\n' == r('<?for (key, value) in {1:1, **{1:2}, 1:3, **{1:4}}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert 'no' == r('<?if {}?>yes<?else?>no<?end if?>')
	assert 'yes' == r('<?if {1:2}?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_dictcomp(r):
	# JS only supports string keys
	assert "" == r("<?code d = {str(i):2*i for i in range(10) if i%2}?><?if '2' in d?><?print d['2']?><?end if?>")
	assert "6" == r("<?code d = {str(i):2*i for i in range(10) if i%2}?><?if '3' in d?><?print d['3']?><?end if?>")
	assert "6" == r("<?code d = {str(i):2*i for i in range(10)}?><?print d['3']?>")


@pytest.mark.ul4
def test_code_storevar(r):
	assert '42' == r('<?code x = 42?><?print x?>')
	assert 'xyzzy' == r('<?code x = "xyzzy"?><?print x?>')
	assert 'x,y' == r('<?code (x, y) = "xy"?><?print x?>,<?print y?>')
	assert '42' == r('<?code (x,) = [42]?><?print x?>')
	assert '17,23' == r('<?code (x,y) = [17, 23]?><?print x?>,<?print y?>')
	assert '17,23,37,42,105' == r('<?code ((v, w), (x,), (y,), z) = [[17, 23], [37], [42], 105]?><?print v?>,<?print w?>,<?print x?>,<?print y?>,<?print z?>')


@pytest.mark.ul4
def test_code_addvar(r):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			assert x + y == eval(r('<?code x = {}?><?code x += {}?><?print x?>'.format(x, y)))
	assert 'xyzzy' == r('<?code x = "xyz"?><?code x += "zy"?><?print x?>')


@pytest.mark.ul4
def test_code_subvar(r):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			assert x - y == eval(r('<?code x = {}?><?code x -= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_code_mulvar(r):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			assert x * y == eval(r('<?code x = {}?><?code x *= {}?><?print x?>'.format(x, y)))
	for x in (17, False, True):
		y = "xyzzy"
		assert x * y == r('<?code x = {}?><?code x *= {!r}?><?print x?>'.format(x, y))
	assert 17*"xyzzy" == r('<?code x = "xyzzy"?><?code x *= 17?><?print x?>')


@pytest.mark.ul4
def test_code_floordivvar(r):
	for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
		for y in (2, -2, 2.0, -2.0, True):
			assert x // y == eval(r('<?code x = {}?><?code x //= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_code_truedivvar(r):
	for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
		for y in (2, -2, 2.0, -2.0, True):
			assert x / y == eval(r('<?code x = {}?><?code x /= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_code_modvar(r):
	for x in (1729, 1729.0, -1729, -1729.0, False, True):
		for y in (23, 23., -23, -23.0, True):
			assert x % y == eval(r('<?code x = {}?><?code x %= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_code_delvar(r):
	if r is not render_js:
		with raises("(x|not found)"):
			r('<?code x = 1729?><?code del x?><?print x?>')


@pytest.mark.ul4
def test_for_string(r):
	assert '' == r('<?for c in data?>(<?print c?>)<?end for?>', data="")
	assert '(g)(u)(r)(k)' == r('<?for c in data?>(<?print c?>)<?end for?>', data="gurk")


@pytest.mark.ul4
def test_for_list(r):
	assert '' == r('<?for c in data?>(<?print c?>)<?end for?>', data="")
	assert '(g)(u)(r)(k)' == r('<?for c in data?>(<?print c?>)<?end for?>', data=["g", "u", "r", "k"])


@pytest.mark.ul4
def test_for_dict(r):
	assert '' == r('<?for c in data?>(<?print c?>)<?end for?>', data={})
	assert '(a)(b)(c)' == r('<?for c in sorted(data)?>(<?print c?>)<?end for?>', data=dict(a=1, b=2, c=3))


@pytest.mark.ul4
def test_for_nested_loop(r):
	assert '[(1)(2)][(3)(4)]' == r('<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>', data=[[1, 2], [3, 4]])


@pytest.mark.ul4
def test_for_unpacking(r):
	data = [
		("spam", "eggs", 17),
		("gurk", "hurz", 23),
		("hinz", "kunz", 42),
	]

	assert '(spam)(gurk)(hinz)' == r('<?for (a,) in data?>(<?print a?>)<?end for?>', data=[item[:1] for item in data])
	assert '(spam,eggs)(gurk,hurz)(hinz,kunz)' == r('<?for (a, b) in data?>(<?print a?>,<?print b?>)<?end for?>', data=[item[:2] for item in data])
	assert '(spam,eggs,17)(gurk,hurz,23)(hinz,kunz,42)' == r('<?for (a, b, c) in data?>(<?print a?>,<?print b?>,<?print c?>)<?end for?>', data=data)


@pytest.mark.ul4
def test_for_nested_unpacking(r):
	data = [
		(("spam", "eggs"), (17,), None),
		(("gurk", "hurz"), (23,), False),
		(("hinz", "kunz"), (42,), True),
	]

	assert '(spam,eggs,17,)(gurk,hurz,23,False)(hinz,kunz,42,True)' == r('<?for ((a, b), (c,), d) in data?>(<?print a?>,<?print b?>,<?print c?>,<?print d?>)<?end for?>', data=data)


@pytest.mark.ul4
def test_break(r):
	assert '1, 2, ' == r('<?for i in [1,2,3]?><?print i?>, <?if i==2?><?break?><?end if?><?end for?>')


@pytest.mark.ul4
def test_break_nested(r):
	assert '1, 1, 2, 1, 2, 3, ' == r('<?for i in [1,2,3,4]?><?for j in [1,2,3,4]?><?print j?>, <?if j>=i?><?break?><?end if?><?end for?><?if i>=3?><?break?><?end if?><?end for?>')


@pytest.mark.ul4
def test_continue(r):
	assert '1, 3, ' == r('<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?print i?>, <?end for?>')


@pytest.mark.ul4
def test_continue_nested(r):
	assert '1, 3, \n1, 3, \n' == r('<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?for j in [1,2,3]?><?if j==2?><?continue?><?end if?><?print j?>, <?end for?>\n<?end for?>')


@pytest.mark.ul4
def test_if(r):
	assert '42' == r('<?if data?><?print data?><?end if?>', data=42)


@pytest.mark.ul4
def test_else(r):
	assert '42' == r('<?if data?><?print data?><?else?>no<?end if?>', data=42)
	assert 'no' == r('<?if data?><?print data?><?else?>no<?end if?>', data=0)


@pytest.mark.ul4
def test_block_errors(r):
	with raises("block unclosed"):
		r('<?for x in data?>')
	with raises("for ended by endif|endif doesn't match any if"):
		r('<?for x in data?><?end if?>')
	with raises("not in any block"):
		r('<?end?>')
	with raises("not in any block"):
		r('<?end for?>')
	with raises("not in any block"):
		r('<?end if?>')
	with raises("else doesn't match any if"):
		r('<?else?>')
	with raises("block unclosed"):
		r('<?if data?>')
	with raises("block unclosed"):
		r('<?if data?><?else?>')
	with raises("duplicate else in if/elif/else chain|else already seen in if"):
		r('<?if data?><?else?><?else?>')
	with raises("elif can't follow else in if/elif/else chain|else already seen in if"):
		r('<?if data?><?else?><?elif data?>')
	with raises("elif can't follow else in if/elif/else chain|else already seen in if"):
		r('<?if data?><?elif data?><?elif data?><?else?><?elif data?>')


@pytest.mark.ul4
def test_empty():
	with raises("expression required"):
		render_python('<?print?>')
	with raises("expression required"):
		render_python('<?if?>')
	with raises("expression required"):
		render_python('<<?if x?><?elif?><?end if?>')
	with raises("loop expression required"):
		render_python('<?for?>')
	with raises("statement required"):
		render_python('<?code?>')
	with raises("expression required"):
		render_python('<?render?>')


@pytest.mark.ul4
def test_add(r):
	code = '<?print x + y?>'
	values = (17, 23, 1., -1.)

	for x in values:
		for y in values:
			assert x + y == eval(r(code, x=x, y=y)) # Using ``evaleq`` avoids problem with the nonexistant int/float distinction in JS
	assert 'foobar' == r('<?code x="foo"?><?code y="bar"?><?print x+y?>')
	assert '(f)(o)(o)(b)(a)(r)' == r('<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>', data=dict(foo="foo", bar="bar"))
	assert "2012-10-18 00:00:00" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(1))
	assert "2013-10-17 00:00:00" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(365))
	assert "2012-10-17 12:00:00" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 12*60*60))
	assert "2012-10-17 00:00:01" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 1))
	assert "2012-10-17 00:00:00.500000" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 0, 500000))
	assert "2012-10-17 00:00:00.001000" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 0, 1000))
	assert "2 days, 0:00:00" == r(code, x=datetime.timedelta(1), y=datetime.timedelta(1))
	assert "1 day, 0:00:01" == r(code, x=datetime.timedelta(1), y=datetime.timedelta(0, 1))
	assert "1 day, 0:00:00.000001" == r(code, x=datetime.timedelta(1), y=datetime.timedelta(0, 0, 1))
	assert "2 months" == r(code, x=misc.monthdelta(1), y=misc.monthdelta(1))
	assert "2000-02-01 00:00:00" == r(code, x=datetime.datetime(2000, 1, 1), y=misc.monthdelta(1))
	assert "1999-11-30 00:00:00" == r(code, x=datetime.datetime(2000, 1, 31), y=misc.monthdelta(-2))
	assert "2000-03-29 00:00:00" == r(code, x=datetime.datetime(2000, 2, 29), y=misc.monthdelta(1))
	assert "2001-02-28 00:00:00" == r(code, x=datetime.datetime(2000, 2, 29), y=misc.monthdelta(12))
	assert "2001-02-28 00:00:00" == r(code, x=misc.monthdelta(12), y=datetime.datetime(2000, 2, 29))


@pytest.mark.ul4
def test_sub(r):
	code = '<?print x - y?>'
	values = (17, 23, 1., -1.)

	for x in values:
		for y in values:
			assert x - y == eval(r(code, x=x, y=y))

	assert "2012-10-16 00:00:00" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(1))
	assert "2011-10-17 00:00:00" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(366))
	assert "2012-10-16 12:00:00" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 12*60*60))
	assert "2012-10-16 23:59:59" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 1))
	assert "2012-10-16 23:59:59.500000" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 0, 500000))
	assert "2012-10-16 23:59:59.999000" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 0, 1000))
	assert "0:00:00" == r(code, x=datetime.timedelta(1), y=datetime.timedelta(1))
	assert "1 day, 0:00:00" == r(code, x=datetime.timedelta(2), y=datetime.timedelta(1))
	assert "23:59:59" == r(code, x=datetime.timedelta(1), y=datetime.timedelta(0, 1))
	assert "23:59:59.999999" == r(code, x=datetime.timedelta(1), y=datetime.timedelta(0, 0, 1))
	assert "-1 day, 23:59:59" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0, 1))
	assert "-1 day, 23:59:59.999999" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0, 0, 1))
	assert "2000-01-01 00:00:00" == r(code, x=datetime.datetime(2000, 2, 1), y=misc.monthdelta(1))
	assert "2000-02-29 00:00:00" == r(code, x=datetime.datetime(1999, 12, 31), y=misc.monthdelta(-2))
	assert "2000-02-29 00:00:00" == r(code, x=datetime.datetime(2000, 3, 29), y=misc.monthdelta(1))
	assert "1999-02-28 00:00:00" == r(code, x=datetime.datetime(2000, 2, 29), y=misc.monthdelta(12))
	assert "-1 month" == r(code, x=misc.monthdelta(2), y=misc.monthdelta(3))


@pytest.mark.ul4
def test_neg(r):
	code = "<?print -x?>"

	assert "0" == r(code, x=False)
	assert "-1" == r(code, x=True)
	assert "-17" == r(code, x=17)
	assert "-42.5" == r(code, x=42.5)
	assert "0:00:00" == r(code, x=datetime.timedelta())
	assert "-1 day, 0:00:00" == r(code, x=datetime.timedelta(1))
	assert "-1 day, 23:59:59" == r(code, x=datetime.timedelta(0, 1))
	assert "-1 day, 23:59:59.999999" == r(code, x=datetime.timedelta(0, 0, 1))
	assert "0 months" == r(code, x=misc.monthdelta())
	assert "-1 month" == r(code, x=misc.monthdelta(1))
	# This checks constant folding
	assert "0" == r("<?print -False?>")
	assert "-1" == r("<?print -True?>")
	assert "-2" == r("<?print -2?>")
	assert "-2.5" == r("<?print -2.5?>")

@pytest.mark.ul4
def test_mul(r):
	code = '<?print x * y?>'
	values = (17, 23, 1., -1.)

	for x in values:
		for y in values:
			assert x * y == eval(r(code, x=x, y=y))
	assert 17*"foo" == r('<?print 17*"foo"?>')
	assert 17*"foo" == r('<?code x=17?><?code y="foo"?><?print x*y?>')
	assert "foo"*17 == r('<?code x="foo"?><?code y=17?><?print x*y?>')
	assert "foo"*17 == r('<?print "foo"*17?>')
	assert "(foo)(bar)(foo)(bar)(foo)(bar)" == r('<?for i in 3*data?>(<?print i?>)<?end for?>', data=["foo", "bar"])
	assert "0:00:00" == r(code, x=4, y=datetime.timedelta())
	assert "4 days, 0:00:00" == r(code, x=4, y=datetime.timedelta(1))
	assert "2 days, 0:00:00" == r(code, x=4, y=datetime.timedelta(0, 12*60*60))
	assert "0:00:02" == r(code, x=4, y=datetime.timedelta(0, 0, 500000))
	assert "12:00:00" == r(code, x=0.5, y=datetime.timedelta(1))
	assert "0:00:00" == r(code, x=datetime.timedelta(), y=4)
	assert "4 days, 0:00:00" == r(code, x=datetime.timedelta(1), y=4)
	assert "2 days, 0:00:00" == r(code, x=datetime.timedelta(0, 12*60*60), y=4)
	assert "0:00:02" == r(code, x=datetime.timedelta(0, 0, 500000), y=4)
	assert "12:00:00" == r(code, x=datetime.timedelta(1), y=0.5)
	assert "4 months" == r(code, x=4, y=misc.monthdelta(1))
	assert "4 months" == r(code, x=misc.monthdelta(1), y=4)


@pytest.mark.ul4
def test_truediv(r):
	code = "<?print x / y?>"

	assert "0.5" == r('<?print 1/2?>')
	assert "0.5" == r('<?code x=1?><?code y=2?><?print x/y?>')
	assert "0:00:00" == r(code, x=datetime.timedelta(), y=4)
	assert "2 days, 0:00:00" == r(code, x=datetime.timedelta(8), y=4)
	assert "12:00:00" == r(code, x=datetime.timedelta(4), y=8)
	assert "0:00:00.500000" == r(code, x=datetime.timedelta(0, 4), y=8)
	assert "2 days, 0:00:00" == r(code, x=datetime.timedelta(1), y=0.5)
	assert "9:36:00" == r(code, x=datetime.timedelta(1), y=2.5)
	assert "0:00:00" == r(code, x=datetime.timedelta(), y=4)
	assert "2 days, 0:00:00" == r(code, x=datetime.timedelta(8), y=4)
	assert "12:00:00" == r(code, x=datetime.timedelta(4), y=8)
	assert "0:00:00.500000" == r(code, x=datetime.timedelta(0, 4), y=8)


@pytest.mark.ul4
def test_floordiv(r):
	assert "0" == r('<?print 1//2?>')
	assert "0" == r('<?code x=1?><?code y=2?><?print x//y?>')
	assert "1 month" == r('<?print x//y?>', x=misc.monthdelta(3), y=2)


@pytest.mark.ul4
def test_mod(r):
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert x % y == eval(r('<?print {} % {}?>'.format(x, y)))
			assert x % y == eval(r('<?print x % y?>', x=x, y=y))


@pytest.mark.ul4
def test_eq(r):
	code = '<?print x == y?>'
	numbervalues = (17, 23, 17., 23.)

	for x in numbervalues:
		for y in numbervalues:
			assert str(x == y) == r('<?print {} == {}?>'.format(x, y))
			assert str(x == y) == r(code, x=x, y=y)

	assert "True" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0))
	assert "False" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(1))
	assert "False" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0, 1))
	assert "False" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0, 0, 1))
	assert "True" == r(code, x=misc.monthdelta(0), y=misc.monthdelta(0))
	assert "False" == r(code, x=misc.monthdelta(0), y=misc.monthdelta(1))


@pytest.mark.ul4
def test_ne(r):
	code = '<?print x != y?>'
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert str(x != y) == r('<?print {} != {}?>'.format(x, y))
			assert str(x != y) == r(code, x=x, y=y)

	assert "False" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0))
	assert "True" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(1))
	assert "True" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0, 1))
	assert "True" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0, 0, 1))
	assert "False" == r(code, x=misc.monthdelta(0), y=misc.monthdelta(0))
	assert "True" == r(code, x=misc.monthdelta(0), y=misc.monthdelta(1))


@pytest.mark.ul4
def test_lt(r):
	code = '<?print x < y?>'
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert str(x < y) == r('<?print {} < {}?>'.format(x, y))
			assert str(x < y) == r(code, x=x, y=y)

	assert "False" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0))
	assert "True" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(1))
	assert "True" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0, 1))
	assert "True" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0, 0, 1))
	assert "False" == r(code, x=misc.monthdelta(0), y=misc.monthdelta(0))
	assert "True" == r(code, x=misc.monthdelta(0), y=misc.monthdelta(1))


@pytest.mark.ul4
def test_le(r):
	code = '<?print x <= y?>'
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert str(x <= y) == r('<?print {} <= {}?>'.format(x, y))
			assert str(x <= y) == r(code, x=x, y=y)

	assert "True" == r(code, x=datetime.timedelta(1), y=datetime.timedelta(1))
	assert "False" == r(code, x=datetime.timedelta(1), y=datetime.timedelta(0))
	assert "False" == r(code, x=datetime.timedelta(0, 1), y=datetime.timedelta(0))
	assert "False" == r(code, x=datetime.timedelta(0, 0, 1), y=datetime.timedelta(0))
	assert "True" == r(code, x=misc.monthdelta(1), y=misc.monthdelta(1))
	assert "False" == r(code, x=misc.monthdelta(1), y=misc.monthdelta(0))


@pytest.mark.ul4
def test_gt(r):
	code = '<?print x > y?>'
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert str(x > y) == r('<?print {} > {}?>'.format(x, y))
			assert str(x > y) == r(code, x=x, y=y)

	assert "False" == r(code, x=datetime.timedelta(1), y=datetime.timedelta(1))
	assert "True" == r(code, x=datetime.timedelta(1), y=datetime.timedelta(0))
	assert "True" == r(code, x=datetime.timedelta(0, 1), y=datetime.timedelta(0))
	assert "True" == r(code, x=datetime.timedelta(0, 0, 1), y=datetime.timedelta(0))
	assert "False" == r(code, x=misc.monthdelta(1), y=misc.monthdelta(1))
	assert "True" == r(code, x=misc.monthdelta(1), y=misc.monthdelta(0))


@pytest.mark.ul4
def test_ge(r):
	code = '<?print x >= y?>'
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert str(x >= y) == r('<?print {} >= {}?>'.format(x, y))
			assert str(x >= y) == r(code, x=x, y=y)

	assert "True" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0))
	assert "False" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(1))
	assert "False" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0, 1))
	assert "False" == r(code, x=datetime.timedelta(0), y=datetime.timedelta(0, 0, 1))
	assert "True" == r(code, x=misc.monthdelta(0), y=misc.monthdelta(0))
	assert "False" == r(code, x=misc.monthdelta(0), y=misc.monthdelta(1))


@pytest.mark.ul4
def test_contains(r):
	code = '<?print x in y?>'

	assert "True" == r(code, x=2, y=[1, 2, 3])
	assert "False" == r(code, x=4, y=[1, 2, 3])
	assert "True" == r(code, x="ur", y="gurk")
	assert "False" == r(code, x="un", y="gurk")
	assert "True" == r(code, x="a", y={"a": 1, "b": 2})
	assert "False" == r(code, x="c", y={"a": 1, "b": 2})
	assert "True" == r(code, x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42))
	assert "False" == r(code, x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42))


@pytest.mark.ul4
def test_notcontains(r):
	code = '<?print x not in y?>'

	assert "False" == r(code, x=2, y=[1, 2, 3])
	assert "True" == r(code, x=4, y=[1, 2, 3])
	assert "False" == r(code, x="ur", y="gurk")
	assert "True" == r(code, x="un", y="gurk")
	assert "False" == r(code, x="a", y={"a": 1, "b": 2})
	assert "True" == r(code, x="c", y={"a": 1, "b": 2})
	assert "False" == r(code, x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42))
	assert "True" == r(code, x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42))


@pytest.mark.ul4
def test_and(r):
	assert "False" == r('<?print x and y?>', x=False, y=False)
	assert "False" == r('<?print x and y?>', x=False, y=True)
	assert "0" == r('<?print x and y?>', x=0, y=True)


@pytest.mark.ul4
def test_or(r):
	assert "False" == r('<?print x or y?>', x=False, y=False)
	assert "True" == r('<?print x or y?>', x=False, y=True)
	assert "42" == r('<?print x or y?>', x=42, y=True)


@pytest.mark.ul4
def test_not(r):
	assert "True" == r('<?print not x?>', x=False)
	assert "False" == r('<?print not x?>', x=42)


@pytest.mark.ul4
def test_getitem(r):
	assert "u" == r("<?print 'gurk'[1]?>")
	assert "u" == r("<?print x[1]?>", x="gurk")
	assert "u" == r("<?print 'gurk'[-3]?>")
	assert "u" == r("<?print x[-3]?>", x="gurk")
	with raises("index out of range|IndexError"):
		r("<?print 'gurk'[4]?>")
	with raises("index (4 )?out of range"):
		r("<?print x[4]?>", x="gurk")
	with raises("index out of range|IndexError"):
		r("<?print 'gurk'[-5]?>")
	with raises("index (-5 )?out of range"):
		r("<?print x[-5]?>", x="gurk")


@pytest.mark.ul4
def test_getslice12(r):
	assert "ur" == r("<?print 'gurk'[1:3]?>")
	assert "ur" == r("<?print x[1:3]?>", x="gurk")
	assert "ur" == r("<?print 'gurk'[-3:-1]?>")
	assert "ur" == r("<?print x[-3:-1]?>", x="gurk")
	assert "" == r("<?print 'gurk'[4:10]?>")
	assert "" == r("<?print x[4:10]?>", x="gurk")
	assert "" == r("<?print 'gurk'[-10:-5]?>")
	assert "" == r("<?print x[-10:-5]?>", x="gurk")


@pytest.mark.ul4
def test_getslice1(r):
	assert "urk" == r("<?print 'gurk'[1:]?>")
	assert "urk" == r("<?print x[1:]?>", x="gurk")
	assert "urk" == r("<?print 'gurk'[-3:]?>")
	assert "urk" == r("<?print x[-3:]?>", x="gurk")
	assert "" == r("<?print 'gurk'[4:]?>")
	assert "" == r("<?print x[4:]?>", x="gurk")
	assert "gurk" == r("<?print 'gurk'[-10:]?>")
	assert "gurk" == r("<?print x[-10:]?>", x="gurk")


@pytest.mark.ul4
def test_getslice2(r):
	assert "gur" == r("<?print 'gurk'[:3]?>")
	assert "gur" == r("<?print x[:3]?>", x="gurk")
	assert "gur" == r("<?print 'gurk'[:-1]?>")
	assert "gur" == r("<?print x[:-1]?>", x="gurk")
	assert "gurk" == r("<?print 'gurk'[:10]?>")
	assert "gurk" == r("<?print x[:10]?>", x="gurk")
	assert "" == r("<?print 'gurk'[:-5]?>")
	assert "" == r("<?print x[:-5]?>", x="gurk")
	assert "05" == r("<?print ('0' + str(x))[-2:]?>", x=5)
	assert "15" == r("<?print ('0' + str(x))[-2:]?>", x=15)


@pytest.mark.ul4
def test_getslice(r):
	assert "gurk" == r("<?print 'gurk'[:]?>")
	assert "gurk" == r("<?print x[:]?>", x="gurk")
	assert "[1, 2]" == r("<?print x[:]?>", x=[1, 2])


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

	assert str(n) == r('<?print {}?>'.format(sc))
	assert str(n) == r('<?code x=4?><?print {}?>'.format(sv))


@pytest.mark.ul4
def test_precedence(r):
	assert "14" == r('<?print 2+3*4?>')
	assert "20" == r('<?print (2+3)*4?>')
	assert "10" == r('<?print -2+-3*-4?>')
	assert "14" == r('<?print --2+--3*--4?>')
	assert "14" == r('<?print (-(-2))+(-((-3)*-(-4)))?>')
	assert "42" == r('<?print 2*data.value?>', data=dict(value=21))
	assert "42" == r('<?print data.value[0]?>', data=dict(value=[42]))
	assert "42" == r('<?print data[0].value?>', data=[dict(value=42)])
	assert "42" == r('<?print data[0][0][0]?>', data=[[[42]]])
	assert "42" == r('<?print data.value.value[0]?>', data=dict(value=dict(value=[42])))
	assert "42" == r('<?print data.value.value[0].value.value[0]?>', data=dict(value=dict(value=[dict(value=dict(value=[42]))])))

@pytest.mark.ul4
def test_associativity(r):
	assert "9" == r('<?print 2+3+4?>')
	assert "-5" == r('<?print 2-3-4?>')
	assert "24" == r('<?print 2*3*4?>')
	if r is not render_js:
		assert "2.0" == r('<?print 24/6/2?>')
		assert "2" == r('<?print 24//6//2?>')
	else:
		assert 2.0 == eval(r('<?print 24/6/2?>'))
		assert 2 == eval(r('<?print 24//6//2?>'))

@pytest.mark.ul4
def test_bracket(r):
	sc = "4"
	sv = "x"
	for i in range(10):
		sc = "({})".format(sc)
		sv = "({})".format(sv)

	assert "4" == r('<?print {}?>'.format(sc))
	assert "4" == r('<?code x=4?><?print {}?>'.format(sv))


@pytest.mark.ul4
def test_function_now(r):
	now = str(datetime.datetime.now())

	with raises(argumentmismatchmessage):
		r("<?print now(1)?>")
	with raises(argumentmismatchmessage):
		r("<?print now(1, 2)?>")
	assert now <= r("<?print now()?>")


@pytest.mark.ul4
def test_function_utcnow(r):
	utcnow = str(datetime.datetime.utcnow())

	with raises(argumentmismatchmessage):
		r("<?print utcnow(1)?>")
	with raises(argumentmismatchmessage):
		r("<?print utcnow(1, 2)?>")
	# JS and Java only have milliseconds precision, but this shouldn't lead to problems here, as rendering the template takes longer than a millisecond
	assert utcnow <= r("<?print utcnow()?>")


@pytest.mark.ul4
def test_function_date(r):
	assert "@(2012-10-06)" == r("<?print repr(date(2012, 10, 6))?>")
	assert "@(2012-10-06T12:00:00)" == r("<?print repr(date(2012, 10, 6, 12))?>")
	assert "@(2012-10-06T12:34:00)" == r("<?print repr(date(2012, 10, 6, 12, 34))?>")
	assert "@(2012-10-06T12:34:56)" == r("<?print repr(date(2012, 10, 6, 12, 34, 56))?>")
	assert "@(2012-10-06T12:34:56.987000)" == r("<?print repr(date(2012, 10, 6, 12, 34, 56, 987000))?>")


@pytest.mark.ul4
def test_function_timedelta(r):
	with raises(argumentmismatchmessage):
		r("<?print timedelta(1, 2, 3, 4)?>")
	assert "0:00:01" == r("<?print timedelta(0, 0, 1000000)?>")
	assert "1 day, 0:00:00" == r("<?print timedelta(0, 0, 24*60*60*1000000)?>")
	assert "1 day, 0:00:00" == r("<?print timedelta(0, 24*60*60)?>")
	assert "12:00:00" == r("<?print timedelta(0.5)?>")
	assert "0:00:00.500000" == r("<?print timedelta(0, 0.5)?>")
	assert "0:00:00.500000" == r("<?print timedelta(0.5/(24*60*60))?>")
	assert "-1 day, 12:00:00" == r("<?print timedelta(-0.5)?>")
	assert "-1 day, 23:59:59.500000" == r("<?print timedelta(0, -0.5)?>")


@pytest.mark.ul4
def test_function_monthdelta(r):
	with raises(argumentmismatchmessage):
		r("<?print monthdelta(1, 2)?>")
	assert "0 months" == r("<?print monthdelta()?>")
	assert "2 months" == r("<?print monthdelta(2)?>")
	assert "1 month" == r("<?print monthdelta(1)?>")
	assert "-1 month" == r("<?print monthdelta(-1)?>")


@pytest.mark.ul4
def test_function_vars(r):
	code = "<?if var in vars()?>yes<?else?>no<?end if?>"

	with raises(argumentmismatchmessage):
		r("<?print vars(1)?>")
	with raises(argumentmismatchmessage):
		r("<?print vars(1, 2)?>")
	assert "yes" == r(code, var="spam", spam="eggs")
	assert "no" == r(code, var="nospam", spam="eggs")


@pytest.mark.ul4
def test_function_random(r):
	with raises(argumentmismatchmessage):
		r("<?print random(1)?>")
	with raises(argumentmismatchmessage):
		r("<?print random(1, 2)?>")
	assert "ok" == r("<?code r = random()?><?if r>=0 and r<1?>ok<?else?>fail<?end if?>")


@pytest.mark.ul4
def test_function_randrange(r):
	with raises(argumentmismatchmessage):
		r("<?print randrange()?>")
	assert "ok" == r("<?code r = randrange(4)?><?if r>=0 and r<4?>ok<?else?>fail<?end if?>")
	assert "ok" == r("<?code r = randrange(17, 23)?><?if r>=17 and r<23?>ok<?else?>fail<?end if?>")
	assert "ok" == r("<?code r = randrange(17, 23, 2)?><?if r>=17 and r<23 and r%2?>ok<?else?>fail<?end if?>")


@pytest.mark.ul4
def test_function_randchoice(r):
	with raises(argumentmismatchmessage):
		r("<?print randchoice()?>")
	assert "ok" == r("<?code r = randchoice('abc')?><?if r in 'abc'?>ok<?else?>fail<?end if?>")
	assert "ok" == r("<?code s = [17, 23, 42]?><?code r = randchoice(s)?><?if r in s?>ok<?else?>fail<?end if?>")
	assert "ok" == r("<?code s = #12345678?><?code sl = [0x12, 0x34, 0x56, 0x78]?><?code r = randchoice(s)?><?if r in sl?>ok<?else?>fail<?end if?>")


@pytest.mark.ul4
def test_function_xmlescape(r):
	with raises(argumentmismatchmessage):
		r("<?print xmlescape()?>")
	with raises(argumentmismatchmessage):
		r("<?print xmlescape(1, 2)?>")
	assert "&lt;&lt;&gt;&gt;&amp;&#39;&quot;gurk" == r("<?print xmlescape(data)?>", data='<<>>&\'"gurk')


@pytest.mark.ul4
def test_function_csv(r):
	with raises(argumentmismatchmessage):
		r("<?print csv()?>")
	with raises(argumentmismatchmessage):
		r("<?print csv(1, 2)?>")
	assert "" == r("<?print csv(data)?>", data=None)
	assert "False" == r("<?print csv(data)?>", data=False)
	assert "True" == r("<?print csv(data)?>", data=True)
	assert "42" == r("<?print csv(data)?>", data=42)
	# no check for float
	assert "abc" == r("<?print csv(data)?>", data="abc")
	assert '"a,b,c"' == r("<?print csv(data)?>", data="a,b,c")
	assert '"a""b""c"' == r("<?print csv(data)?>", data='a"b"c')
	assert '"a\nb\nc"' == r("<?print csv(data)?>", data="a\nb\nc")


@pytest.mark.ul4
def test_function_asjson(r):
	with raises(argumentmismatchmessage):
		r("<?print asjson()?>")
	with raises(argumentmismatchmessage):
		r("<?print asjson(1, 2)?>")
	assert "null" == r("<?print asjson(data)?>", data=None)
	assert "false" == r("<?print asjson(data)?>", data=False)
	assert "true" == r("<?print asjson(data)?>", data=True)
	assert "42" == r("<?print asjson(data)?>", data=42)
	# no check for float
	assert '"abc"' == r("<?print asjson(data)?>", data="abc")
	assert '[1, 2, 3]' == r("<?print asjson(data)?>", data=[1, 2, 3])
	assert '[1, 2, 3]' == r("<?print asjson(data)?>", data=PseudoList([1, 2, 3]))
	assert '{"one": 1}' == r("<?print asjson(data)?>", data={"one": 1})
	assert '{"one": 1}' == r("<?print asjson(data)?>", data=PseudoDict({"one": 1}))


@pytest.mark.ul4
def test_function_fromjson(r):
	code = "<?print repr(fromjson(data))?>"
	with raises(argumentmismatchmessage):
		r("<?print fromjson()?>")
	with raises(argumentmismatchmessage):
		r("<?print fromjson(1, 2)?>")
	assert "None" == r(code, data="null")
	assert "False" == r(code, data="false")
	assert "True" == r(code, data="true")
	assert "42" == r(code, data="42")
	# no check for float
	assert r(code, data='"abc"') in ('"abc"', "'abc'")
	assert '[1, 2, 3]' == r(code, data="[1, 2, 3]")
	assert r(code, data='{"one": 1}') in ('{"one": 1}', "{'one': 1}")


@pytest.mark.ul4
def test_function_ul4on(r):
	code = "<?print repr(fromul4on(asul4on(data)))?>"

	with raises(argumentmismatchmessage):
		r("<?print asul4on()?>")
	with raises(argumentmismatchmessage):
		r("<?print asul4on(1, 2)?>")
	with raises(argumentmismatchmessage):
		r("<?print fromul4on()?>")
	with raises(argumentmismatchmessage):
		r("<?print fromul4on(1, 2)?>")
	assert "None" == r(code, data=None)
	assert "False" == r(code, data=False)
	assert "True" == r(code, data=True)
	assert "42" == r(code, data=42)
	# no check for float
	assert r(code, data="abc") in ('"abc"', "'abc'")
	assert '[1, 2, 3]' == r(code, data=[1, 2, 3])
	assert r(code, data={'one': 1}) in ('{"one": 1}', "{'one': 1}")


@pytest.mark.ul4
def test_function_str(r):
	code = "<?print str(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print str(1, 2)?>")
	assert "" == r("<?print str()?>")
	assert "" == r(code, data=None)
	assert "True" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "42" == r(code, data=42)
	assert "4.2" == r(code, data=4.2)
	assert "foo" == r(code, data="foo")
	assert "2011-02-09 00:00:00" == r(code, data=datetime.datetime(2011, 2, 9))
	assert "2011-02-09 12:34:56" == r(code, data=datetime.datetime(2011, 2, 9, 12, 34, 56))
	assert "2011-02-09 12:34:56.987000" == r(code, data=datetime.datetime(2011, 2, 9, 12, 34, 56, 987000))
	assert "0:00:00" == r("<?print timedelta()?>")
	assert "1 day, 0:00:00" == r("<?print timedelta(1)?>")
	assert "-1 day, 0:00:00" == r("<?print timedelta(-1)?>")
	assert "2 days, 0:00:00" == r("<?print timedelta(2)?>")
	assert "0:00:01" == r("<?print timedelta(0, 1)?>")
	assert "0:01:00" == r("<?print timedelta(0, 60)?>")
	assert "1:00:00" == r("<?print timedelta(0, 60*60)?>")
	assert "1 day, 1:01:01.000001" == r("<?print timedelta(1, 60*60+60+1, 1)?>")
	assert "0:00:00.000001" == r("<?print timedelta(0, 0, 1)?>")
	assert "-1 day, 23:59:59" == r("<?print timedelta(0, -1)?>")
	assert "-1 day, 23:59:59.999999" == r("<?print timedelta(0, 0, -1)?>")


@pytest.mark.ul4
def test_function_bool(r):
	with raises(argumentmismatchmessage):
		r("<?print bool(1, 2)?>")
	assert "False" == r("<?print bool()?>")
	code = "<?print bool(data)?>"
	assert "True" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=0)
	assert "True" == r(code, data=42)
	assert "False" == r(code, data=0.0)
	assert "True" == r(code, data=42.5)
	assert "False" == r(code, data="")
	assert "True" == r(code, data="gurk")
	assert "False" == r(code, data=[])
	assert "True" == r(code, data=["gurk"])
	assert "False" == r(code, data={})
	assert "True" == r(code, data={"gurk": "hurz"})
	assert "True" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta())
	assert "True" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta())
	assert "True" == r(code, data=misc.monthdelta(1))


@pytest.mark.ul4
def test_function_int(r):
	with raises(argumentmismatchmessage):
		r("<?print int(1, 2, 3)?>")
	with raises("int\\(\\) argument must be a string or a number|int\\(null\\) not supported"):
		r("<?print int(data)?>", data=None)
	with raises("invalid literal for int|NumberFormatException"):
		r("<?print int(data)?>", data="foo")
	assert "0" == r("<?print int()?>")
	assert "1" == r("<?print int(data)?>", data=True)
	assert "0" == r("<?print int(data)?>", data=False)
	assert "42" == r("<?print int(data)?>", data=42)
	assert "4" == r("<?print int(data)?>", data=4.2)
	assert "42" == r("<?print int(data)?>", data="42")
	assert "66" == r("<?print int(data, 16)?>", data="42")


@pytest.mark.ul4
def test_function_float(r):
	code = "<?print float(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print float(1, 2, 3)?>")
	with raises("float\\(\\) argument must be a string or a number|float\\(null\\) not supported"):
		r(code, data=None)
	assert "4.2" == r(code, data=4.2)
	if r is not render_js:
		assert "0.0" == r("<?print float()?>")
		assert "1.0" == r(code, data=True)
		assert "0.0" == r(code, data=False)
		assert "42.0" == r(code, data=42)
		assert "42.0" == r(code, data="42")
	else:
		assert 0.0 == eval(r("<?print float()?>"))
		assert 1.0 == eval(r(code, data=True))
		assert 0.0 == eval(r(code, data=False))
		assert 42.0 == eval(r(code, data=42))
		assert 42.0 == eval(r(code, data="42"))


@pytest.mark.ul4
def test_function_len(r):
	code = "<?print len(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print len()?>")
	with raises(argumentmismatchmessage):
		r("<?print len(1, 2)?>")
	with raises("has no len\\(\\)|len\\(.*\\) not supported"):
		r(code, data=None)
	with raises("has no len\\(\\)|len\\(.*\\) not supported"):
		r(code, data=True)
	with raises("has no len\\(\\)|len\\(.*\\) not supported"):
		r(code, data=False)
	with raises("has no len\\(\\)|len\\(.*\\) not supported"):
		r(code, data=42)
	with raises("has no len\\(\\)|len\\(.*\\) not supported"):
		r(code, data=4.2)
	assert "42" == r(code, data=42*"?")
	assert "42" == r(code, data=42*[None])
	assert "42" == r(code, data=dict.fromkeys(range(42)))


@pytest.mark.ul4
def test_function_enumerate(r):
	code1 = "<?for (i, value) in enumerate(data)?>(<?print value?>=<?print i?>)<?end for?>"
	code2 = "<?for (i, value) in enumerate(data, 42)?>(<?print value?>=<?print i?>)<?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print enumerate()?>")
	with raises(argumentmismatchmessage):
		r("<?print enumerate(1, 2, 3)?>")
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code1, data=None)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code1, data=True)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code1, data=False)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code1, data=42)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code1, data=4.2)
	assert "(f=0)(o=1)(o=2)" == r(code1, data="foo")
	assert "(foo=0)(bar=1)" == r(code1, data=["foo", "bar"])
	assert "(foo=0)" == r(code1, data=dict(foo=True))
	assert "" == r(code1, data="")
	assert "(f=42)(o=43)(o=44)" == r(code2, data="foo")


@pytest.mark.ul4
def test_function_enumfl(r):
	code1 = "<?for (i, f, l, value) in enumfl(data)?><?if f?>[<?end if?>(<?print value?>=<?print i?>)<?if l?>]<?end if?><?end for?>"
	code2 = "<?for (i, f, l, value) in enumfl(data, 42)?><?if f?>[<?end if?>(<?print value?>=<?print i?>)<?if l?>]<?end if?><?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print enumfl()?>")
	with raises(argumentmismatchmessage):
		r("<?print enumfl(1, 2, 3)?>")
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code1, data=None)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code1, data=True)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code1, data=False)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code1, data=42)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code1, data=4.2)
	assert "[(f=0)(o=1)(o=2)]" == r(code1, data="foo")
	assert "[(foo=0)(bar=1)]" == r(code1, data=["foo", "bar"])
	assert "[(foo=0)]" == r(code1, data=dict(foo=True))
	assert "" == r(code1, data="")
	assert "[(f=42)(o=43)(o=44)]" == r(code2, data="foo")


@pytest.mark.ul4
def test_function_isfirstlast(r):
	code = "<?for (f, l, value) in isfirstlast(data)?><?if f?>[<?end if?>(<?print value?>)<?if l?>]<?end if?><?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print isfirstlast()?>")
	with raises(argumentmismatchmessage):
		r("<?print isfirstlast(1, 2)?>")
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=None)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=True)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=False)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=42)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=4.2)
	assert "[(f)(o)(o)]" == r(code, data="foo")
	assert "[(foo)(bar)]" == r(code, data=["foo", "bar"])
	assert "[(foo)]" == r(code, data=dict(foo=True))
	assert "" == r(code, data="")


@pytest.mark.ul4
def test_function_isfirst(r):
	code = "<?for (f, value) in isfirst(data)?><?if f?>[<?end if?>(<?print value?>)<?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print isfirst()?>")
	with raises(argumentmismatchmessage):
		r("<?print isfirst(1, 2)?>")
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=None)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=True)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=False)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=42)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=4.2)
	assert "[(f)(o)(o)" == r(code, data="foo")
	assert "[(foo)(bar)" == r(code, data=["foo", "bar"])
	assert "[(foo)" == r(code, data=dict(foo=True))
	assert "" == r(code, data="")


@pytest.mark.ul4
def test_function_islast(r):
	code = "<?for (l, value) in islast(data)?>(<?print value?>)<?if l?>]<?end if?><?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print islast()?>")
	with raises(argumentmismatchmessage):
		r("<?print islast(1, 2)?>")
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=None)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=True)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=False)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=42)
	with raises("is not iterable|iter\\(.*\\) not supported"):
		r(code, data=4.2)
	assert "(f)(o)(o)]" == r(code, data="foo")
	assert "(foo)(bar)]" == r(code, data=["foo", "bar"])
	assert "(foo)]" == r(code, data=dict(foo=True))
	assert "" == r(code, data="")


@pytest.mark.ul4
def test_function_isnone(r):
	code = "<?print isnone(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isnone()?>")
	with raises(argumentmismatchmessage):
		r("<?print isnone(1, 2)?>")
	assert "True" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_isbool(r):
	code = "<?print isbool(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isbool()?>")
	with raises(argumentmismatchmessage):
		r("<?print isbool(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "True" == r(code, data=True)
	assert "True" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_isint(r):
	code = "<?print isint(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isint()?>")
	with raises(argumentmismatchmessage):
		r("<?print isint(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "True" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_isfloat(r):
	code = "<?print isfloat(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isfloat()?>")
	with raises(argumentmismatchmessage):
		r("<?print isfloat(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "True" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_isstr(r):
	code = "<?print isstr(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isstr()?>")
	with raises(argumentmismatchmessage):
		r("<?print isstr(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "True" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_isdate(r):
	code = "<?print isdate(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isdate()?>")
	with raises(argumentmismatchmessage):
		r("<?print isdate(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "True" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_islist(r):
	code = "<?print islist(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print islist()?>")
	with raises(argumentmismatchmessage):
		r("<?print islist(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "True" == r(code, data=())
	assert "True" == r(code, data=[])
	assert "True" == r(code, data=PseudoList([]))
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_isdict(r):
	code = "<?print isdict(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isdict()?>")
	with raises(argumentmismatchmessage):
		r("<?print isdict(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "True" == r(code, data={})
	assert "True" == r(code, data=PseudoDict({}))
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_istemplate(r):
	code = "<?print istemplate(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print istemplate()?>")
	with raises(argumentmismatchmessage):
		r("<?print istemplate(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "True" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_iscolor(r):
	code = "<?print iscolor(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print iscolor()?>")
	with raises(argumentmismatchmessage):
		r("<?print iscolor(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "True" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_istimedelta(r):
	code = "<?print istimedelta(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print istimedelta()?>")
	with raises(argumentmismatchmessage):
		r("<?print istimedelta(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "True" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_ismonthdelta(r):
	code = "<?print ismonthdelta(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print ismonthdelta()?>")
	with raises(argumentmismatchmessage):
		r("<?print ismonthdelta(1, 2)?>")
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "True" == r(code, data=misc.monthdelta(1))
	assert "False" == r(code, data=())
	assert "False" == r(code, data=[])
	assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)


@pytest.mark.ul4
def test_function_get(r):
	with raises(argumentmismatchmessage):
		r("<?print get()?>")
	assert "" == r("<?print get('x')?>")
	assert "42" == r("<?print get('x')?>", x=42)
	assert "17" == r("<?print get('x', 17)?>")
	assert "42" == r("<?print get('x', 17)?>", x=42)


@pytest.mark.ul4
def test_function_repr(r):
	code = "<?print repr(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print repr()?>")
	with raises(argumentmismatchmessage):
		r("<?print repr(1, 2)?>")
	assert "None" == r(code, data=None)
	assert "True" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "42" == r(code, data=42)
	assert 42.5 == eval(r(code, data=42.5))
	assert r(code, data="foo") in ('"foo"', "'foo'")
	assert [1, 2, 3] == eval(r(code, data=[1, 2, 3]))
	if r is not render_js:
		assert [1, 2, 3] == eval(r(code, data=(1, 2, 3)))
	assert {"a": 1, "b": 2} == eval(r(code, data={"a": 1, "b": 2}))
	assert "@(2011-02-07T12:34:56.123000)" == r(code, data=datetime.datetime(2011, 2, 7, 12, 34, 56, 123000))
	assert "@(2011-02-07T12:34:56)" == r(code, data=datetime.datetime(2011, 2, 7, 12, 34, 56))
	assert "@(2011-02-07)" == r(code, data=datetime.datetime(2011, 2, 7))
	assert "@(2011-02-07)" == r(code, data=datetime.date(2011, 2, 7))
	assert "timedelta(1)" == r(code, data=datetime.timedelta(1))
	assert "timedelta(0, 1)" == r(code, data=datetime.timedelta(0, 1))
	assert "timedelta(0, 0, 1)" == r(code, data=datetime.timedelta(0, 0, 1))
	assert "timedelta(-1)" == r(code, data=datetime.timedelta(-1))
	assert "timedelta(-1, 86399)" == r(code, data=datetime.timedelta(0, -1))
	assert "timedelta(-1, 86399, 999999)" == r(code, data=datetime.timedelta(0, 0, -1))
	assert "timedelta(0, 43200)" == r(code, data=datetime.timedelta(0.5))
	assert "timedelta(0, 0, 500000)" == r(code, data=datetime.timedelta(0, 0.5))
	assert "timedelta(-1, 43200)" == r(code, data=datetime.timedelta(-0.5))
	assert "timedelta(-1, 86399, 500000)" == r(code, data=datetime.timedelta(0, -0.5))


@pytest.mark.ul4
def test_function_format(r):
	t = datetime.datetime(2011, 1, 25, 13, 34, 56, 987000)
	code2 = "<?print format(data, format)?>"
	code3 = "<?print format(data, format, lang)?>"

	assert "2011" == r(code2, format="%Y", data=t)
	assert "01" == r(code2, format="%m", data=t)
	assert "25" == r(code2, format="%d", data=t)
	assert "13" == r(code2, format="%H", data=t)
	assert "34" == r(code2, format="%M", data=t)
	assert "56" == r(code2, format="%S", data=t)
	assert "987000" == r(code2, format="%f", data=t)
	assert "Tue" == r(code2, format="%a", data=t)
	assert "Tue" == r(code3, format="%a", data=t, lang=None)
	assert "Tue" == r(code3, format="%a", data=t, lang="en")
	assert "Di" == r(code3, format="%a", data=t, lang="de")
	assert "Di" == r(code3, format="%a", data=t, lang="de_DE")
	assert "Tuesday" == r(code2, format="%A", data=t)
	assert "Tuesday" == r(code3, format="%A", data=t, lang=None)
	assert "Tuesday" == r(code3, format="%A", data=t, lang="en")
	assert "Dienstag" == r(code3, format="%A", data=t, lang="de")
	assert "Dienstag" == r(code3, format="%A", data=t, lang="de_DE")
	assert "Jan" == r(code2, format="%b", data=t)
	assert "Jan" == r(code3, format="%b", data=t, lang=None)
	assert "Jan" == r(code3, format="%b", data=t, lang="en")
	assert "Jan" == r(code3, format="%b", data=t, lang="de")
	assert "Jan" == r(code3, format="%b", data=t, lang="de_DE")
	assert "January" == r(code2, format="%B", data=t)
	assert "January" == r(code3, format="%B", data=t, lang=None)
	assert "January" == r(code3, format="%B", data=t, lang="en")
	assert "Januar" == r(code3, format="%B", data=t, lang="de")
	assert "Januar" == r(code3, format="%B", data=t, lang="de_DE")
	assert "01" == r(code2, format="%I", data=t)
	assert "025" == r(code2, format="%j", data=t)
	assert "PM" == r(code2, format="%p", data=t)
	assert "04" == r(code2, format="%U", data=t)
	assert "2" == r(code2, format="%w", data=t)
	assert "04" == r(code2, format="%W", data=t)
	assert "11" == r(code2, format="%y", data=t)
	assert r(code2, format="%c", data=t) in ("Tue Jan 25 13:34:56 2011", "Tue 25 Jan 2011 01:34:56 PM", "Tue 25 Jan 2011 01:34:56 PM ")
	assert "01/25/2011" == r(code2, format="%x", data=t)
	assert "01/25/2011" == r(code3, format="%x", data=t, lang=None)
	assert "01/25/2011" == r(code3, format="%x", data=t, lang="en")
	assert "25.01.2011" == r(code3, format="%x", data=t, lang="de")
	assert "25.01.2011" == r(code3, format="%x", data=t, lang="de_DE")
	assert r(code2, format="%X", data=t) in ("13:34:56", "01:34:56 PM")
	assert r(code3, format="%X", data=t, lang=None) in ("13:34:56", "01:34:56 PM")
	assert r(code3, format="%X", data=t, lang="en") in ("13:34:56", "01:34:56 PM")
	assert "13:34:56" == r(code3, format="%X", data=t, lang="de")
	assert "13:34:56" == r(code3, format="%X", data=t, lang="de_DE")
	assert "%" == r(code2, format="%%", data=t)


@pytest.mark.ul4
def test_function_chr(r):
	code = "<?print chr(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print chr()?>")
	with raises(argumentmismatchmessage):
		r("<?print chr(1, 2)?>")
	assert "\x00" == r(code, data=0)
	assert "a" == r(code, data=ord("a"))
	assert "\u20ac" == r(code, data=0x20ac)


@pytest.mark.ul4
def test_function_ord(r):
	code = "<?print ord(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print ord()?>")
	with raises(argumentmismatchmessage):
		r("<?print ord(1, 2)?>")
	assert "0" == r(code, data="\x00")
	assert str(ord("a")) == r(code, data="a")
	assert str(0x20ac) == r(code, data="\u20ac")


@pytest.mark.ul4
def test_function_hex(r):
	code = "<?print hex(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print hex()?>")
	with raises(argumentmismatchmessage):
		r("<?print hex(1, 2)?>")
	assert "0x0" == r(code, data=0)
	assert "0xff" == r(code, data=0xff)
	assert "0xffff" == r(code, data=0xffff)
	assert "-0xffff" == r(code, data=-0xffff)


@pytest.mark.ul4
def test_function_oct(r):
	code = "<?print oct(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print oct()?>")
	with raises(argumentmismatchmessage):
		r("<?print oct(1, 2)?>")
	assert "0o0" == r(code, data=0)
	assert "0o77" == r(code, data=0o77)
	assert "0o7777" == r(code, data=0o7777)
	assert "-0o7777" == r(code, data=-0o7777)


@pytest.mark.ul4
def test_function_bin(r):
	code = "<?print bin(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print bin()?>")
	with raises(argumentmismatchmessage):
		r("<?print bin(1, 2)?>")
	assert "0b0" == r(code, data=0b0)
	assert "0b11" == r(code, data=0b11)
	assert "-0b1111" == r(code, data=-0b1111)


@pytest.mark.ul4
def test_function_abs(r):
	code = "<?print abs(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print abs()?>")
	with raises(argumentmismatchmessage):
		r("<?print abs(1, 2)?>")
	assert "0" == r(code, data=0)
	assert "42" == r(code, data=42)
	assert "42" == r(code, data=-42)


@pytest.mark.ul4
def test_function_sorted(r):
	code = "<?for i in sorted(data)?><?print i?><?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print sorted()?>")
	assert "gkru" == r(code, data="gurk")
	assert "24679" == r(code, data="92746")
	assert "172342" == r(code, data=(42, 17, 23))
	assert "012" == r(code, data={0: "zero", 1: "one", 2: "two"})


@pytest.mark.ul4
def test_function_range(r):
	code1 = "<?for i in range(data)?><?print i?>;<?end for?>"
	code2 = "<?for i in range(data[0], data[1])?><?print i?>;<?end for?>"
	code3 = "<?for i in range(data[0], data[1], data[2])?><?print i?>;<?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print range()?>")
	assert "" == r(code1, data=-10)
	assert "" == r(code1, data=0)
	assert "0;" == r(code1, data=1)
	assert "0;1;2;3;4;" == r(code1, data=5)
	assert "" == r(code2, data=[0, -10])
	assert "" == r(code2, data=[0, 0])
	assert "0;1;2;3;4;" == r(code2, data=[0, 5])
	assert "-5;-4;-3;-2;-1;0;1;2;3;4;" == r(code2, data=[-5, 5])
	assert "" == r(code3, data=[0, -10, 1])
	assert "" == r(code3, data=[0, 0, 1])
	assert "0;2;4;6;8;" == r(code3, data=[0, 10, 2])
	assert "" == r(code3, data=[0, 10, -2])
	assert "10;8;6;4;2;" == r(code3, data=[10, 0, -2])
	assert "" == r(code3, data=[10, 0, 2])


@pytest.mark.ul4
def test_function_urlquote(r):
	assert "gurk" == r("<?print urlquote('gurk')?>")
	assert "%3C%3D%3E%2B%3F" == r("<?print urlquote('<=>+?')?>")
	assert "%7F%C3%BF%EF%BF%BF" == r("<?print urlquote('\u007f\u00ff\uffff')?>")


@pytest.mark.ul4
def test_function_urlunquote(r):
	assert "gurk" == r("<?print urlunquote('gurk')?>")
	assert "<=>+?" == r("<?print urlunquote('%3C%3D%3E%2B%3F')?>")
	assert "\u007f\u00ff\uffff" == r("<?print urlunquote('%7F%C3%BF%EF%BF%BF')?>")


@pytest.mark.ul4
def test_function_zip(r):
	code0 = "<?for i in zip()?><?print i?>;<?end for?>"
	code1 = "<?for (ix, ) in zip(x)?><?print ix?>;<?end for?>"
	code2 = "<?for (ix, iy) in zip(x, y)?><?print ix?>-<?print iy?>;<?end for?>"
	code3 = "<?for (ix, iy, iz) in zip(x, y, z)?><?print ix?>-<?print iy?>+<?print iz?>;<?end for?>"

	assert "" == r(code0)
	assert "1;2;" == r(code1, x=[1, 2])
	assert "" == r(code2, x=[], y=[])
	assert "1-3;2-4;" == r(code2, x=[1, 2], y=[3, 4])
	assert "1-4;2-5;" == r(code2, x=[1, 2, 3], y=[4, 5])
	assert "" == r(code3, x=[], y=[], z=[])
	assert "1-3+5;2-4+6;" == r(code3, x=[1, 2], y=[3, 4], z=[5, 6])
	assert "1-4+6;" == r(code3, x=[1, 2, 3], y=[4, 5], z=[6])


@pytest.mark.ul4
def test_function_type(r):
	code = "<?print type(x)?>"

	with raises(argumentmismatchmessage):
		r("<?print type()?>")
	with raises(argumentmismatchmessage):
		r("<?print type(1, 2)?>")
	assert "none" == r(code, x=None)
	assert "bool" == r(code, x=False)
	assert "bool" == r(code, x=True)
	assert "int" == r(code, x=42)
	assert "float" == r(code, x=4.2)
	assert "str" == r(code, x="foo")
	assert "date" == r(code, x=datetime.datetime.now())
	assert "date" == r(code, x=datetime.date.today())
	assert "timedelta" == r(code, x=datetime.timedelta())
	assert "monthdelta" == r(code, x=misc.monthdelta())
	assert "list" == r(code, x=(1, 2))
	assert "list" == r(code, x=[1, 2])
	assert "list" == r(code, x=PseudoList([1, 2]))
	assert "dict" == r(code, x={1: 2})
	assert "dict" == r(code, x=PseudoDict({1: 2}))
	assert "template" == r(code, x=ul4c.Template(""))
	assert "color" == r(code, x=color.red)


@pytest.mark.ul4
def test_function_reversed(r):
	code = "<?for i in reversed(x)?>(<?print i?>)<?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print reversed()?>")
	with raises(argumentmismatchmessage):
		r("<?print reversed(1, 2)?>")
	assert "(3)(2)(1)" == r(code, x="123")
	assert "(3)(2)(1)" == r(code, x=[1, 2, 3])
	assert "(3)(2)(1)" == r(code, x=(1, 2, 3))


@pytest.mark.ul4
def test_function_min(r):
	with raises(argumentmismatchmessage):
		r("<?print min()?>")
	with raises("empty sequence"):
		r("<?print min([])?>")
	assert "1" == r("<?print min('123')?>")
	assert "1" == r("<?print min(1, 2, 3)?>")
	assert "0" == r("<?print min(0, False, 1, True)?>")
	assert "False" == r("<?print min(False, 0, True, 1)?>")
	assert "False" == r("<?print min([False, 0, True, 1])?>")


@pytest.mark.ul4
def test_function_max(r):
	with raises(argumentmismatchmessage):
		r("<?print max()?>")
	with raises("empty sequence"):
		r("<?print max([])?>")
	assert "3" == r("<?print max('123')?>")
	assert "3" == r("<?print max(1, 2, 3)?>")
	assert "1" == r("<?print max(0, False, 1, True)?>")
	assert "True" == r("<?print max(False, 0, True, 1)?>")
	assert "True" == r("<?print max([False, 0, True, 1])?>")


@pytest.mark.ul4
def test_function_rgb(r):
	assert "#369" == r("<?print repr(rgb(0.2, 0.4, 0.6))?>")
	assert "#369c" == r("<?print repr(rgb(0.2, 0.4, 0.6, 0.8))?>")


@pytest.mark.ul4
def test_function_hls(r):
	assert "#fff" == r("<?print repr(hls(0, 1, 0))?>")
	assert "#fff0" == r("<?print repr(hls(0, 1, 0, 0))?>")


@pytest.mark.ul4
def test_function_hsv(r):
	assert "#fff" == r("<?print repr(hsv(0, 0, 1))?>")
	assert "#fff0" == r("<?print repr(hsv(0, 0, 1, 0))?>")


@pytest.mark.ul4
def test_method_upper(r):
	assert "GURK" == r("<?print 'gurk'.upper()?>")


@pytest.mark.ul4
def test_method_lower(r):
	assert "gurk" == r("<?print 'GURK'.lower()?>")


@pytest.mark.ul4
def test_method_capitalize(r):
	assert "Gurk" == r("<?print 'gURK'.capitalize()?>")


@pytest.mark.ul4
def test_method_startswith(r):
	assert "True" == r("<?print 'gurkhurz'.startswith('gurk')?>")
	assert "False" == r("<?print 'gurkhurz'.startswith('hurz')?>")


@pytest.mark.ul4
def test_method_endswith(r):
	assert "True" == r("<?print 'gurkhurz'.endswith('hurz')?>")
	assert "False" == r("<?print 'gurkhurz'.endswith('gurk')?>")


@pytest.mark.ul4
def test_method_strip(r):
	assert "gurk" == r(r"<?print obj.strip()?>", obj=' \t\r\ngurk \t\r\n')
	assert "gurk" == r(r"<?print obj.strip('xyz')?>", obj='xyzzygurkxyzzy')


@pytest.mark.ul4
def test_method_lstrip(r):
	assert "gurk \t\r\n" == r("<?print obj.lstrip()?>", obj=" \t\r\ngurk \t\r\n")
	assert "gurkxyzzy" == r("<?print obj.lstrip(arg)?>", obj="xyzzygurkxyzzy", arg="xyz")


@pytest.mark.ul4
def test_method_rstrip(r):
	assert " \t\r\ngurk" == r("<?print obj.rstrip()?>", obj=" \t\r\ngurk \t\r\n")
	assert "xyzzygurk" == r("<?print obj.rstrip(arg)?>", obj="xyzzygurkxyzzy", arg="xyz")


@pytest.mark.ul4
def test_method_split(r):
	assert "(f)(o)(o)" == r("<?for item in obj.split()?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "(f)(o \t\r\no \t\r\n)" == r("<?for item in obj.split(None, 1)?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "()(f)(o)(o)()" == r("<?for item in obj.split(arg)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")
	assert "()(f)(oxxoxx)" == r("<?for item in obj.split(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")


@pytest.mark.ul4
def test_method_rsplit(r):
	assert "(f)(o)(o)" == r("<?for item in obj.rsplit()?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "( \t\r\nf \t\r\no)(o)" == r("<?for item in obj.rsplit(None, 1)?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "()(f)(o)(o)()" == r("<?for item in obj.rsplit(arg)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")
	assert "(xxfxxo)(o)()" == r("<?for item in obj.rsplit(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")


@pytest.mark.ul4
def test_method_replace(r):
	assert 'goork' == r(r"<?print 'gurk'.replace('u', 'oo')?>")


@pytest.mark.ul4
def test_method_renders(r):
	t = ul4c.Template('(<?print data?>)')
	assert '(GURK)' == r("<?print t.renders(data='gurk').upper()?>", t=t)
	assert '(GURK)' == r("<?print t.renders(**{'data': 'gurk'}).upper()?>", t=t)

	t = ul4c.Template('(gurk)')
	assert '(GURK)' == r("<?print t.renders().upper()?>", t=t)


@pytest.mark.ul4
def test_method_mimeformat(r):
	t = datetime.datetime(2010, 2, 22, 12, 34, 56)

	assert 'Mon, 22 Feb 2010 12:34:56 GMT' == r(r"<?print data.mimeformat()?>", data=t)


@pytest.mark.ul4
def test_method_get(r):
	assert "42" == r("<?print {}.get('foo', 42)?>")
	assert "17" == r("<?print {'foo': 17}.get('foo', 42)?>")
	assert "" == r("<?print {}.get('foo')?>")
	assert "17" == r("<?print {'foo': 17}.get('foo')?>")


@pytest.mark.ul4
def test_method_r_g_b_a(r):
	assert '0x11' == r('<?code c = #123?><?print hex(c.r())?>')
	assert '0x22' == r('<?code c = #123?><?print hex(c.g())?>')
	assert '0x33' == r('<?code c = #123?><?print hex(c.b())?>')
	assert '0xff' == r('<?code c = #123?><?print hex(c.a())?>')


@pytest.mark.ul4
def test_method_hls(r):
	assert '0' == r('<?code c = #fff?><?print int(c.hls()[0])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hls()[1])?>')
	assert '0' == r('<?code c = #fff?><?print int(c.hls()[2])?>')


@pytest.mark.ul4
def test_method_hlsa(r):
	assert '0' == r('<?code c = #fff?><?print int(c.hlsa()[0])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hlsa()[1])?>')
	assert '0' == r('<?code c = #fff?><?print int(c.hlsa()[2])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hlsa()[3])?>')


@pytest.mark.ul4
def test_method_hsv(r):
	assert '0' == r('<?code c = #fff?><?print int(c.hsv()[0])?>')
	assert '0' == r('<?code c = #fff?><?print int(c.hsv()[1])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hsv()[2])?>')


@pytest.mark.ul4
def test_method_hsva(r):
	assert '0' == r('<?code c = #fff?><?print int(c.hsva()[0])?>')
	assert '0' == r('<?code c = #fff?><?print int(c.hsva()[1])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hsva()[2])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hsva()[3])?>')


@pytest.mark.ul4
def test_method_lum(r):
	assert 'True' == r('<?print #fff.lum() == 1?>')


@pytest.mark.ul4
def test_method_withlum(r):
	assert '#fff' == r('<?print #000.withlum(1)?>')


@pytest.mark.ul4
def test_method_witha(r):
	assert '#0063a82a' == r('<?print repr(#0063a8.witha(42))?>')


@pytest.mark.ul4
def test_method_join(r):
	assert '1,2,3,4' == r('<?print ",".join("1234")?>')
	assert '1,2,3,4' == r('<?print ",".join(["1", "2", "3", "4"])?>')


@pytest.mark.ul4
def test_method_find(r):
	s = "gurkgurk"
	assert '-1' == r('<?print s.find("ks")?>', s=s)
	assert '2' == r('<?print s.find("rk")?>', s=s)
	assert '2' == r('<?print s.find("rk", 2)?>', s=s)
	assert '6' == r('<?print s.find("rk", -3)?>', s=s)
	assert '2' == r('<?print s.find("rk", 2, 4)?>', s=s)
	assert '6' == r('<?print s.find("rk", 4, 8)?>', s=s)
	assert '5' == r('<?print s.find("ur", -4, -1)?>', s=s)
	assert '-1' == r('<?print s.find("rk", 2, 3)?>', s=s)
	assert '-1' == r('<?print s.find("rk", 7)?>', s=s)
	l = list("gurkgurk")
	assert '-1' == r('<?print l.find("x")?>', l=l)
	assert '2' == r('<?print l.find("r")?>', l=l)
	assert '2' == r('<?print l.find("r", 2)?>', l=l)
	assert '6' == r('<?print l.find("r", -3)?>', l=l)
	assert '2' == r('<?print l.find("r", 2, 4)?>', l=l)
	assert '6' == r('<?print l.find("r", 4, 8)?>', l=l)
	assert '6' == r('<?print l.find("r", -3, -1)?>', l=l)
	assert '-1' == r('<?print l.find("r", 2, 2)?>', l=l)
	assert '-1' == r('<?print l.find("r", 7)?>', l=l)
	assert '1' == r('<?print l.find(None)?>', l=[0, None, 1, None, 2, None, 3, None])


@pytest.mark.ul4
def test_method_rfind(r):
	s = "gurkgurk"
	assert '-1' == r('<?print s.rfind("ks")?>', s=s)
	assert '6' == r('<?print s.rfind("rk")?>', s=s)
	assert '6' == r('<?print s.rfind("rk", 2)?>', s=s)
	assert '6' == r('<?print s.rfind("rk", -3)?>', s=s)
	assert '2' == r('<?print s.rfind("rk", 2, 4)?>', s=s)
	assert '6' == r('<?print s.rfind("rk", 4, 8)?>', s=s)
	assert '5' == r('<?print s.rfind("ur", -4, -1)?>', s=s)
	assert '-1' == r('<?print s.rfind("rk", 2, 3)?>', s=s)
	assert '-1' == r('<?print s.rfind("rk", 7)?>', s=s)
	l = list("gurkgurk")
	assert '-1' == r('<?print l.rfind("x")?>', l=l)
	assert '6' == r('<?print l.rfind("r")?>', l=l)
	assert '6' == r('<?print l.rfind("r", 2)?>', l=l)
	assert '2' == r('<?print l.rfind("r", 2, 4)?>', l=l)
	assert '6' == r('<?print l.rfind("r", 4, 8)?>', l=l)
	assert '6' == r('<?print l.rfind("r", -3, -1)?>', l=l)
	assert '-1' == r('<?print l.rfind("r", 2, 2)?>', l=l)
	assert '-1' == r('<?print l.rfind("r", 7)?>', l=l)
	assert '7' == r('<?print l.rfind(None)?>', l=[0, None, 1, None, 2, None, 3, None])


@pytest.mark.ul4
def test_method_day(r):
	assert '12' == r('<?print @(2010-05-12).day()?>')
	assert '12' == r('<?print d.day()?>', d=datetime.date(2010, 5, 12))


@pytest.mark.ul4
def test_method_month(r):
	assert '5' == r('<?print @(2010-05-12).month()?>')
	assert '5' == r('<?print d.month()?>', d=datetime.date(2010, 5, 12))


@pytest.mark.ul4
def test_method_year(r):
	assert '5' == r('<?print @(2010-05-12).month()?>')
	assert '5' == r('<?print d.month()?>', d=datetime.date(2010, 5, 12))


@pytest.mark.ul4
def test_method_hour(r):
	assert '16' == r('<?print @(2010-05-12T16:47:56).hour()?>')
	assert '16' == r('<?print d.hour()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@pytest.mark.ul4
def test_method_minute(r):
	assert '47' == r('<?print @(2010-05-12T16:47:56).minute()?>')
	assert '47' == r('<?print d.minute()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@pytest.mark.ul4
def test_method_second(r):
	assert '56' == r('<?print @(2010-05-12T16:47:56).second()?>')
	assert '56' == r('<?print d.second()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@pytest.mark.ul4
def test_method_microsecond(r):
	assert '123000' == r('<?print @(2010-05-12T16:47:56.123000).microsecond()?>')
	assert '123000' == r('<?print d.microsecond()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56, 123000))


@pytest.mark.ul4
def test_method_weekday(r):
	assert '2' == r('<?print @(2010-05-12).weekday()?>')
	assert '2' == r('<?print d.weekday()?>', d=datetime.date(2010, 5, 12))


@pytest.mark.ul4
def test_method_week(r):
	assert '0' == r('<?print @(2012-01-01).week()?>')
	assert '0' == r('<?print @(2012-01-01).week(0)?>')
	assert '1' == r('<?print @(2012-01-01).week(6)?>')
	assert '1' == r('<?print @(2012-01-02).week()?>')
	assert '1' == r('<?print @(2012-01-02).week(0)?>')
	assert '1' == r('<?print @(2012-01-02).week(6)?>')


@pytest.mark.ul4
def test_method_yearday(r):
	assert '1' == r('<?print @(2010-01-01).yearday()?>')
	assert '366' == r('<?print @(2008-12-31).yearday()?>')
	assert '365' == r('<?print @(2010-12-31).yearday()?>')
	assert '132' == r('<?print @(2010-05-12).yearday()?>')
	assert '132' == r('<?print @(2010-05-12T16:47:56).yearday()?>')
	assert '132' == r('<?print d.yearday()?>', d=datetime.date(2010, 5, 12))
	assert '132' == r('<?print d.yearday()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


@pytest.mark.ul4
def test_render(r):
	t = ul4c.Template('<?print prefix?><?print data?><?print suffix?>')

	assert '(f)(o)(o)' == r('<?for c in data?><?render t.render(data=c, prefix="(", suffix=")")?><?end for?>', t=t, data='foo')
	assert '(f)(o)(o)' == r('<?for c in data?><?render t.render(data=c, **{"prefix": "(", "suffix": ")"})?><?end for?>', t=t, data='foo')


@pytest.mark.ul4
def test_render_var(r):
	t = ul4c.Template('<?code x += 1?><?print x?>')

	assert '42,43,42' == r('<?print x?>,<?render t.render(x=x)?>,<?print x?>', t=t, x=42)


@pytest.mark.ul4
def test_def(r):
	assert 'foo' == r('<?def lower?><?print x.lower()?><?end def?><?print lower.renders(x="FOO")?>')


@pytest.mark.ul4
def test_parse(r):
	assert '42' == r('<?print data.Noner?>', data=dict(Noner=42))


@pytest.mark.ul4
def test_nested_exceptions(r):
	tmpl1 = ul4c.Template("<?print 2*x?>", "tmpl1")
	tmpl2 = ul4c.Template("<?render tmpl1.render(x=x)?>", "tmpl2")
	tmpl3 = ul4c.Template("<?render tmpl2.render(tmpl1=tmpl1, x=x)?>", "tmpl3")

	with raises("unsupported operand type|not supported"):
		r("<?render tmpl3.render(tmpl1=tmpl1, tmpl2=tmpl2, x=x)?>", tmpl1=tmpl1, tmpl2=tmpl2, tmpl3=tmpl3, x=None)


@pytest.mark.ul4
def test_note(r):
	assert "foo" == r("f<?note This is?>o<?note a comment?>o")


@pytest.mark.ul4
def test_templateattributes(r):
	s1 = "<?print x?>"
	t1 = ul4c.Template(s1)

	s2 = "<?printx 42?>"
	t2 = ul4c.Template(s2)

	if r is not render_java_compiledtemplate_by_python:
		assert "<?" == r("<?print template.startdelim?>", template=t1)
		assert "?>" == r("<?print template.enddelim?>", template=t1)
		assert s1 == r("<?print template.source?>", template=t1)
		assert "1" == r("<?print len(template.content)?>", template=t1)
		assert "print" == r("<?print template.content[0].type?>", template=t1)
		assert s1 == r("<?print template.content[0].location.tag?>", template=t1)
		assert "x" == r("<?print template.content[0].location.code?>", template=t1)
		assert "var" == r("<?print template.content[0].obj.type?>", template=t1)
		assert "x" == r("<?print template.content[0].obj.name?>", template=t1)
		assert "printx" == r("<?print template.content[0].type?>", template=t2)
		assert "int" == r("<?print template.content[0].obj.type?>", template=t2)
		assert "42" == r("<?print template.content[0].obj.value?>", template=t2)


@pytest.mark.ul4
def test_templateattributes_localtemplate(r):
	source = "<?def lower?><?print t.lower()?><?end def?>"

	if r is not render_java_compiledtemplate_by_python:
		assert source + "<?print lower.source?>" == r(source + "<?print lower.source?>")
		assert source == r(source + "<?print lower.source[lower.location.starttag:lower.endlocation.endtag]?>")
		assert "<?print t.lower()?>" == r(source + "<?print lower.source[lower.location.endtag:lower.endlocation.starttag]?>")
		assert "lower" == r(source + "<?print lower.name?>")


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
	assert '<div></div>' == r(s, cond=False)
	assert '''<div class="gu'&quot;rk"></div>''' == r(s, cond=True)

	s = html.div(class_=(cond, "hurz")).conv().string()
	assert '<div class="hurz"></div>' == r(s, cond=False)
	assert '''<div class="gu'&quot;rkhurz"></div>''' == r(s, cond=True)

	s = cond.conv().string()
	assert '' == r(s, cond=False)
	assert '''<a>gu'"rk</a>''' == r(s, cond=True)

	s = html.ul(compact=ul4.attr_if(True, cond="cond")).conv().string()
	assert '<ul></ul>' == r(s, cond=False)
	assert '''<ul compact="compact"></ul>''' == r(s, cond=True)
