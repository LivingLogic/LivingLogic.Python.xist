#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3

## Copyright 2009-2013 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2013 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import sys, os, re, datetime, io, json, contextlib, tempfile, collections, shutil, subprocess

import pytest

from ll import ul4c, color, misc, ul4on
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


def render_python(__, *, keepws=True, **variables):
	"""
	Compile the template from the source ``__`` and render it with the variables ``variables``.
	"""
	template = ul4c.Template(__, keepws=keepws)
	return template.renders(**variables)


def render_python_dumps(__, *, keepws=True, **variables):
	"""
	Compile the template from the source ``__``, create a string dump from it,
	recreate the template from the dump string and render it with the variables
	``variables``.
	"""
	template = ul4c.Template(__, keepws=keepws)
	template = ul4c.Template.loads(template.dumps()) # Recreate the template from the binary dump
	return template.renders(**variables)


def render_python_dump(__, *, keepws=True, **variables):
	"""
	Compile the template from the source ``__``, dump it to a stream, recreate
	the template from the dump and render it with the variables ``variables``.
	"""
	template = ul4c.Template(__, keepws=keepws)
	stream = io.StringIO()
	template.dump(stream)
	stream.seek(0)
	template = ul4c.Template.load(stream) # Recreate the template from the stream
	return template.renders(**variables)


def render_js(__, *, keepws=True, **variables):
	"""
	Compile the template from the source ``__``, and generate Javascript source
	from it that renders the template with the variables ``variables``.

	(this requires an installed ``d8`` shell from V8 (http://code.google.com/p/v8/))
	"""
	template = ul4c.Template(__, keepws=keepws)
	js = template.jssource()
	js = "template = {};\ndata = {};\nprint(template.renders(data));\n".format(js, ul4c._asjson(variables))
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


def render_php(__, **variables):
	template = ul4c.Template(__)
	php = r"""<?php
	include_once 'com/livinglogic/ul4/ul4.php';
	$template = \com\livinglogic\ul4\InterpretedTemplate::loads({});
	$variables = {};
	print $template->renders($variables);
	?>""".format(phpexpr(template.dumps()), phpexpr(variables))
	with tempfile.NamedTemporaryFile(mode="wb", suffix=".php") as f:
		f.write(php.encode("utf-8"))
		f.flush()
		dir = os.path.expanduser("~/checkouts/LivingLogic.PHP.ul4")
		proc = subprocess.Popen("php -n -d include_path={dir} -d date.timezone=Europe/Berlin {fn}".format(dir=dir, fn=f.name), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		(stdout, stderr) = proc.communicate()
	stdout = stdout.decode("utf-8")
	stderr = stderr.decode("utf-8")
	# Check if we have an exception
	if proc.returncode:
		print(stdout, file=sys.stdout)
		print(stderr, file=sys.stderr)
		raise RuntimeError((stderr.strip() or stdout.strip()).splitlines()[0])
	return stdout


def phpexpr(obj):
	if obj is None:
		return "null"
	elif isinstance(obj, bool):
		return "true" if obj else "false"
	elif isinstance(obj, int):
		return str(obj)
	elif isinstance(obj, float):
		return str(obj)
	elif isinstance(obj, str):
		v = ['"']
		for c in obj:
			if c == '\n':
				c = '\\n'
			elif c == '\t':
				c = '\\t'
			elif c == '"':
				c = '\\"'
			elif ord(c) < 32:
				c = '\\x{:02x}'.format(ord(c))
			v.append(c)
		v.append('"')
		return "".join(v)
	elif isinstance(obj, datetime.datetime):
		return r"\com\livinglogic\ul4\Utils::date({}, {}, {}, {}, {}, {}, {})".format(obj.year, obj.month, obj.day, obj.hour, obj.minute, obj.second, obj.microsecond)
	elif isinstance(obj, datetime.date):
		return r"\com\livinglogic\ul4\Utils::date({}, {}, {})".format(obj.year, obj.month, obj.day)
	elif isinstance(obj, datetime.timedelta):
		return r"new \com\livinglogic\ul4\TimeDelta({}, {}, {})".format(obj.days, obj.seconds, obj.microseconds)
	elif isinstance(obj, misc.monthdelta):
		return r"new \com\livinglogic\ul4\MonthDelta({})".format(obj.months)
	elif isinstance(obj, color.Color):
		return r"new \com\livinglogic\ul4\Color({}, {}, {}, {})".format(obj.r(), obj.g(), obj.b(), obj.a())
	elif isinstance(obj, ul4c.Template):
		return r"\com\livinglogic\ul4\InterpretedTemplate::loads({})".format(phpexpr(obj.dumps()))
	elif isinstance(obj, collections.Mapping):
		return "array({})".format(", ".join("{} => {}".format(phpexpr(key), phpexpr(value)) for (key, value) in obj.items()))
	elif isinstance(obj, collections.Sequence):
		return "array({})".format(", ".join(phpexpr(item) for item in obj))
	else:
		raise ValueError("Can't convert {!r} to PHP".format(obj))


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
		if line in {"}", ")", "};", "},", ");", "),"}:
			indent -= 1
		if line:
			newlines.append(indent*"\t" + line + "\n")
		if line == "{" or line.endswith("("):
			indent += 1
	return "".join(newlines)


def java_runsource(source):
	"""
	Compile the Java source :obj:`source`, run it and return the output
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



def render_java_interpretedtemplate_by_python(__, *, keepws=True, **variables):
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

	templatesource = ul4c.Template(__, keepws=keepws).javasource()
	java = codetemplate % dict(variables=misc.javaexpr(variables), template=templatesource)
	return java_runsource(java)


def render_java_interpretedtemplate_by_java(__, keepws=True, **variables):
	"""
	Generate Java source that compiles the template source ``__`` and renders the
	template with the variables ``variables``.

	(this requires an installed Java compiler and the Java UL4 jar)
	"""

	codetemplate = """
	com.livinglogic.ul4.InterpretedTemplate template = new com.livinglogic.ul4.InterpretedTemplate(%(source)s, %(keepws)s);
	java.util.Map<String, Object> variables = %(variables)s;
	String output = template.renders(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	java = codetemplate % dict(source=misc.javaexpr(__), variables=misc.javaexpr(variables), keepws=misc.javaexpr(keepws))
	return java_runsource(java)


def call_python(__, *, keepws=True, **variables):
	"""
	Compile the template from the source ``__``, call it as a function with the variables ``variables`` and return the result.
	"""
	template = ul4c.Template(__, keepws=keepws)
	return template(**variables)


def call_python_dumps(__, *, keepws=True, **variables):
	"""
	Compile the template from the source ``__``, create a string dump from it,
	recreate the template from the dump string, call it as a function with the
	variables ``variables`` and return the result.
	"""
	template = ul4c.Template(__, keepws=keepws)
	template = ul4c.Template.loads(template.dumps()) # Recreate the template from the binary dump
	return template(**variables)


def call_python_dump(__, *, keepws=True, **variables):
	"""
	Compile the template from the source ``__``, dump it to a stream, recreate
	the template from the dump, call it as a function with the variables
	``variables`` and return the result.
	"""
	template = ul4c.Template(__, keepws=keepws)
	stream = io.StringIO()
	template.dump(stream)
	stream.seek(0)
	template = ul4c.Template.load(stream) # Recreate the template from the stream
	return template(**variables)


def call_js(__, *, keepws=True, **variables):
	"""
	Compile the template from the source ``__``, and generate Javascript source
	from it and call it as a function with the variables ``variables``.

	(this requires an installed ``d8`` shell from V8 (http://code.google.com/p/v8/))
	"""
	template = ul4c.Template(__, keepws=keepws)
	js = template.jssource()
	js = "template = {};\ndata = {};\nprint(ul4on.dumps(template.call(data)));\n".format(js, ul4c._asjson(variables))
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
	return ul4on.loads(stdout)


def call_java_interpretedtemplate_by_python(__, *, keepws=True, **variables):
	"""
	Compile the function from the source ``__``, and generate Java source that
	recreates the function from the Python generated dump and executes the
	function with the variables ``variables``.

	(this requires an installed Java compiler and the Java UL4 jar)
	"""

	codetemplate = """
	com.livinglogic.ul4.InterpretedTemplate template = %(template)s;
	java.util.Map<String, Object> variables = %(variables)s;
	Object output = template.call(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = com.livinglogic.ul4on.Utils.dumps(output).getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	templatesource = ul4c.Template(__, keepws=keepws).javasource()
	java = codetemplate % dict(variables=misc.javaexpr(variables), template=templatesource)
	return ul4on.loads(java_runsource(java))


def call_java_interpretedtemplate_by_java(__, keepws=True, **variables):
	"""
	Generate Java source that compiles the function source ``__`` and executes the
	function with the variables ``variables``.

	(this requires an installed Java compiler and the Java UL4 jar)
	"""

	codetemplate = """
	com.livinglogic.ul4.InterpretedTemplate template = new com.livinglogic.ul4.InterpretedTemplate(%(source)s, %(keepws)s);
	java.util.Map<String, Object> variables = %(variables)s;
	Object output = template.call(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = com.livinglogic.ul4on.Utils.dumps(output).getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	java = codetemplate % dict(source=misc.javaexpr(__), variables=misc.javaexpr(variables), keepws=misc.javaexpr(keepws))
	return ul4on.loads(java_runsource(java))


all_renderers = dict(
	python=render_python,
	python_dumps=render_python_dumps,
	python_dump=render_python_dump,
	js=render_js,
	# php=render_php,
	java_interpreted_by_python=render_java_interpretedtemplate_by_python,
	java_interpreted_by_java=render_java_interpretedtemplate_by_java,
)

all_callers = dict(
	python=call_python,
	python_dumps=call_python_dumps,
	python_dump=call_python_dump,
	js=call_js,
	# php=call_php,
	java_interpreted_by_python=call_java_interpretedtemplate_by_python,
	java_interpreted_by_java=call_java_interpretedtemplate_by_java,
)


@pytest.fixture(scope="module", params=all_renderers.keys())
def r(request):
	return all_renderers[request.param]


@pytest.fixture(scope="module", params=all_callers.keys())
def c(request):
	return all_callers[request.param]


argumentmismatchmessage = [
	# Python argument mismatch exception messages
	"takes exactly \\d+ (positional )?arguments?", # < 3.3
	"got an unexpected keyword argument",
	"expected \\d+ arguments?",
	"Required argument .* not found",
	"takes exactly (one|\\d+) arguments?",
	"expected at least \\d+ arguments", # < 3.3
	"takes at most \\d+ (positional )?arguments?",
	"takes at least \\d+ argument", #  < 3.3
	"takes no arguments",
	"expected at least \\d+ arguments?",
	"expected at most \\d+ arguments?, got \\d+",
	"missing \\d+ required positional arguments?", # 3.3
	"takes \\d+ positional arguments? but \\d+ (was|were) given", # 3.3
	"takes from \\d+ to \\d+ positional arguments but \\d+ (was|were) given", # 3.3
	# Javascript argument mismatch exception messages
	"requires (at least \\d+|\\d+(-\\d+)?) arguments?, \\d+ given",
	"required \\w+\\(\\) argument missing",
	# Java exception messages for argument mismatches
	"required \\w+\\(\\) argument \"\\w+\" \\(position \\d+\\) missing",
	"\\w+\\(\\) doesn't support an argument named \"\\w+\"",
	"\\w+\\(\\) doesn't support keyword arguments",
	"expects (at least \\d+|at most \\d+ positional|exactly \\d+|\\d+-\\d+) arguments?, \\d+ given",
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
	assert 'gurk' == r('gurk', keepws=False)
	assert 'g\tu rk' == r('g\t\n\t u \n  r\n\t\tk', keepws=False)


@pytest.mark.ul4
def test_whitespace(r):
	assert "40"  == r("<?print\na\n+\nb\n?>", a=17, b=23)


@pytest.mark.ul4
def test_undefined(r):
	assert '' == r('<?print Undefined?>')
	assert 'no' == r('<?if Undefined?>yes<?else?>no<?end if?>')


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
	if r is not render_js and r is not render_php:
		# Since Javascript has no real integers the following would lead to rounding errors
		# And PHP doesn't have any support for big integers (except for some GMP wrappers, that may not be installed)
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
	with raises("Unterminated string|mismatched character|MismatchedTokenException|NoViableAltException"):
		r('<?print "?>')
	assert 'foo' == r('<?print "foo"?>')
	assert '\n' == r('<?print "\\n"?>')
	assert '\r' == r('<?print "\\r"?>')
	assert '\t' == r('<?print "\\t"?>')
	assert '\f' == r('<?print "\\f"?>')
	assert '\b' == r('<?print "\\b"?>')
	assert '\a' == r('<?print "\\a"?>')
	assert '\x00' == r('<?print "\\x00"?>')
	assert '"' == r('<?print "\\""?>')
	assert "'" == r('<?print "\\\'"?>')
	assert '\u20ac' == r('<?print "\u20ac"?>')
	assert '\xff' == r('<?print "\\xff"?>')
	assert '\u20ac' == r('''<?print "\\u20ac"?>''')
	for c in "\x00\x80\u0100\u3042\n\r\t\f\b\a\"":
		assert c == r('<?print obj?>', obj=c) # This tests :func:`misc.javaexpr` for Java and :func:`ul4c._asjson` for JS

	# Test literal control characters (but '\r' and '\n' are not allowed)
	assert 'gu\trk' == r("<?print 'gu\trk'?>")
	assert 'gu\t\\rk' == r(r"<?print 'gu\t\\rk'?>")

	# Test triple quoted strings
	assert 'gu\r\nrk' == r("<?print '''gu\r\nrk'''?>")
	assert 'gu\r\nrk' == r('<?print """gu\r\nrk"""?>')

	assert 'no' == r('<?if ""?>yes<?else?>no<?end if?>')
	assert 'yes' == r('<?if "foo"?>yes<?else?>no<?end if?>')


@pytest.mark.ul4
def test_date(r):
	assert '2000-02-29' == r('<?print @(2000-02-29).isoformat()?>')
	assert '2000-02-29' == r('<?print @(2000-02-29T).isoformat()?>')
	assert '2000-02-29T12:34:00' == r('<?print @(2000-02-29T12:34).isoformat()?>')
	assert '2000-02-29T12:34:56' == r('<?print @(2000-02-29T12:34:56).isoformat()?>')
	if r is not render_php:
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

	# Make sure that the loop variables doesn't leak into the surrounding scope
	assert "undefined" == r("<?code d = [2*i for i in range(4)]?><?print type(i)?>")


@pytest.mark.ul4
def test_genexpr(r):
	assert "2, 6:" == r("<?code ge = (str(2*i) for i in range(4) if i%2)?><?print ', '.join(ge)?>:<?print ', '.join(ge)?>")
	assert "2, 6" == r("<?print ', '.join(str(2*i) for i in range(4) if i%2)?>")
	assert "0, 2, 4, 6" == r("<?print ', '.join(str(2*i) for i in range(4))?>")
	assert "0, 2, 4, 6" == r("<?print ', '.join((str(2*i) for i in range(4)))?>")
	assert "0:g; 1:r; 2:k" == r("<?for (i, c2) in enumerate(c for c in 'gurk' if c != 'u')?><?if i?>; <?end if?><?print i?>:<?print c2?><?end for?>")

	# Make sure that the loop variables doesn't leak into the surrounding scope
	assert "undefined" == r("<?code d = (2*i for i in range(4))?><?print type(i)?>")


@pytest.mark.ul4
def test_dict(r):
	assert '' == r('<?for (key, value) in {}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert '1:2\n' == r('<?for (key, value) in {1:2}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert '1:#fff\n' == r('<?for (key, value) in {1:#fff}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert '1:2\n' == r('<?for (key, value) in {1:2,}.items()?><?print key?>:<?print value?>\n<?end for?>')
	# With duplicate keys, later ones simply overwrite earlier ones
	assert '1:3\n' == r('<?for (key, value) in {1:2, 1: 3}.items()?><?print key?>:<?print value?>\n<?end for?>')
	assert 'no' == r('<?if {}?>yes<?else?>no<?end if?>')
	assert 'yes' == r('<?if {1:2}?>yes<?else?>no<?end if?>')

	# Make sure that the loop variables doesn't leak into the surrounding scope
	assert "undefined" == r("<?code d = {i: 2*i for i in range(4)}?><?print type(i)?>")


@pytest.mark.ul4
def test_dictcomp(r):
	# JS only supports string keys
	assert "" == r("<?code d = {str(i):2*i for i in range(10) if i%2}?><?if '2' in d?><?print d['2']?><?end if?>")
	assert "6" == r("<?code d = {str(i):2*i for i in range(10) if i%2}?><?if '3' in d?><?print d['3']?><?end if?>")
	assert "6" == r("<?code d = {str(i):2*i for i in range(10)}?><?print d['3']?>")


@pytest.mark.ul4
def test_print(r):
	assert "" == r("<?print None?>")
	assert "<foo>" == r("<?print '<foo>'?>")


@pytest.mark.ul4
def test_printx(r):
	assert "" == r("<?printx None?>")
	assert "&lt;foo&gt;" == r("<?printx '<foo>'?>")


@pytest.mark.ul4
def test_setvar(r):
	assert '42' == r('<?code x = 42?><?print x?>')
	assert 'xyzzy' == r('<?code x = "xyzzy"?><?print x?>')
	assert 'x,y' == r('<?code (x, y) = "xy"?><?print x?>,<?print y?>')
	assert '42' == r('<?code (x,) = [42]?><?print x?>')
	assert '17,23' == r('<?code (x,y) = [17, 23]?><?print x?>,<?print y?>')
	assert '17,23,37,42,105' == r('<?code ((v, w), (x,), (y,), z) = [[17, 23], [37], [42], 105]?><?print v?>,<?print w?>,<?print x?>,<?print y?>,<?print z?>')


@pytest.mark.ul4
def test_setvar_iterator(r):
	assert 'g;k' == r("<?code (x,y) = (c for c in 'gurk' if c < 'r')?><?print x?>;<?print y?>")


@pytest.mark.ul4
def test_addvar(r):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			assert x + y == eval(r('<?code x = {}?><?code x += {}?><?print x?>'.format(x, y)))
	assert 'xyzzy' == r('<?code x = "xyz"?><?code x += "zy"?><?print x?>')
	assert '[1, 2, 3, 4]' == r('<?code x = [1, 2]?><?code x += [3, 4]?><?print x?>')


@pytest.mark.ul4
def test_subvar(r):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			assert x - y == eval(r('<?code x = {}?><?code x -= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_mulvar(r):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			assert x * y == eval(r('<?code x = {}?><?code x *= {}?><?print x?>'.format(x, y)))
	for x in (17, False, True):
		y = "xyzzy"
		assert x * y == r('<?code x = {}?><?code x *= {!r}?><?print x?>'.format(x, y))
	assert 17*"xyzzy" == r('<?code x = "xyzzy"?><?code x *= 17?><?print x?>')


@pytest.mark.ul4
def test_floordivvar(r):
	for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
		for y in (2, -2, 2.0, -2.0, True):
			assert x // y == eval(r('<?code x = {}?><?code x //= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_truedivvar(r):
	for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
		for y in (2, -2, 2.0, -2.0, True):
			assert x / y == eval(r('<?code x = {}?><?code x /= {}?><?print x?>'.format(x, y)))


@pytest.mark.ul4
def test_modvar(r):
	for x in (1729, 1729.0, -1729, -1729.0, False, True):
		for y in (23, 23., -23, -23.0, True):
			assert x % y == eval(r('<?code x = {}?><?code x %= {}?><?print x?>'.format(x, y)))


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
def test_for_leak(r):
	# Both loop variables and variables assigned in the block leak in the surrounding scope.
	assert '4;4' == r('<?code x = 17?><?code y = 23?><?for x in range(5)?><?code y = x?><?end for?><?print x?>;<?print y?>')


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


@pytest.mark.ul4
def test_add(r):
	code = '<?print x + y?>'
	values = (17, 23, 1., -1.)

	for x in values:
		for y in values:
			assert x + y == eval(r(code, x=x, y=y)) # Using ``evaleq`` avoids problem with the nonexistant int/float distinction in JS
	assert 'foobar' == r('<?code x="foo"?><?code y="bar"?><?print x+y?>')
	assert '[1, 2, 3, 4]' == r('<?print x+y?>', x=[1, 2], y=[3, 4])
	assert '(f)(o)(o)(b)(a)(r)' == r('<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>', data=dict(foo="foo", bar="bar"))
	assert "2012-10-18 00:00:00" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(1))
	assert "2013-10-17 00:00:00" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(365))
	assert "2012-10-17 12:00:00" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 12*60*60))
	assert "2012-10-17 00:00:01" == r(code, x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 1))
	if r is not render_php:
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
	if r is not render_php:
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
	assert 2.0 == eval(r(code, x=datetime.timedelta(4), y=datetime.timedelta(2)))
	assert 2.0 == eval(r(code, x=misc.monthdelta(4), y=misc.monthdelta(2)))


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
	assert "" == r("<?print 'gurk'[4]?>")
	assert "" == r("<?print x[4]?>", x="gurk")
	assert "" == r("<?print 'gurk'[-5]?>")
	assert "" == r("<?print x[-5]?>", x="gurk")


@pytest.mark.ul4
def test_getslice(r):
	assert "ur" == r("<?print 'gurk'[1:3]?>")
	assert "ur" == r("<?print x[1:3]?>", x="gurk")
	assert "ur" == r("<?print 'gurk'[-3:-1]?>")
	assert "ur" == r("<?print x[-3:-1]?>", x="gurk")
	assert "" == r("<?print 'gurk'[4:10]?>")
	assert "" == r("<?print x[4:10]?>", x="gurk")
	assert "" == r("<?print 'gurk'[-10:-5]?>")
	assert "" == r("<?print x[-10:-5]?>", x="gurk")
	assert "urk" == r("<?print 'gurk'[1:]?>")
	assert "urk" == r("<?print x[1:]?>", x="gurk")
	assert "urk" == r("<?print 'gurk'[-3:]?>")
	assert "urk" == r("<?print x[-3:]?>", x="gurk")
	assert "" == r("<?print 'gurk'[4:]?>")
	assert "" == r("<?print x[4:]?>", x="gurk")
	assert "gurk" == r("<?print 'gurk'[-10:]?>")
	assert "gurk" == r("<?print x[-10:]?>", x="gurk")
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
	assert "gurk" == r("<?print 'gurk'[:]?>")
	assert "gurk" == r("<?print x[:]?>", x="gurk")
	assert "[1, 2]" == r("<?print x[:]?>", x=[1, 2])


@pytest.mark.ul4
def test_setslice(r):
	assert "[1, -2, -3, 4]" == r("<?code x = [1, 2, 3, 4]?><?code x[1:3] = [-2, -3]?><?print x?>")
	assert "[1, -1, -4, -9, 4]" == r("<?code x = [1, 2, 3, 4]?><?code x[1:-1] = (-i*i for i in range(1, 4))?><?print x?>")
	assert "[-1, -4, -9]" == r("<?code x = [1, 2, 3, 4]?><?code x[:] = (-i*i for i in range(1, 4))?><?print x?>")


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
def test_callfunc_args(r):
	assert "@(2013-01-07)" == r("<?print repr(date(2013, 1, 7))?>")
	assert "@(2013-01-07)" == r("<?print repr(date(2013, 1, day=7))?>")
	assert "@(2013-01-07)" == r("<?print repr(date(2013, month=1, day=7))?>")
	assert "@(2013-01-07)" == r("<?print repr(date(year=2013, month=1, day=7))?>")
	assert "@(2013-01-07)" == r("<?print repr(date(2013, *[1, 7]))?>")
	assert "@(2013-01-07)" == r("<?print repr(date(*[2013, 1, 7]))?>")
	assert "@(2013-01-07)" == r("<?print repr(date(year=2013, **{'month': 1, 'day': 7}))?>")
	assert "@(2013-01-07)" == r("<?print repr(date(2013, *[1], **{'day': 7}))?>")


@pytest.mark.ul4
def test_function_now(r):
	now = str(datetime.datetime.now())

	with raises(argumentmismatchmessage):
		r("<?print now(1)?>")
	with raises(argumentmismatchmessage):
		r("<?print now(1, 2)?>")
	with raises(argumentmismatchmessage):
		r("<?print now(foo=1)?>")
	assert now <= r("<?print now()?>")


@pytest.mark.ul4
def test_function_utcnow(r):
	utcnow = str(datetime.datetime.utcnow())

	with raises(argumentmismatchmessage):
		r("<?print utcnow(1)?>")
	with raises(argumentmismatchmessage):
		r("<?print utcnow(1, 2)?>")
	with raises(argumentmismatchmessage):
		r("<?print utcnow(foo=1)?>")
	# JS and Java only have milliseconds precision, but this shouldn't lead to problems here, as rendering the template takes longer than a millisecond
	assert utcnow <= r("<?print utcnow()?>")


@pytest.mark.ul4
def test_function_date(r):
	assert "@(2012-10-06)" == r("<?print repr(date(2012, 10, 6))?>")
	assert "@(2012-10-06T12:00:00)" == r("<?print repr(date(2012, 10, 6, 12))?>")
	assert "@(2012-10-06T12:34:00)" == r("<?print repr(date(2012, 10, 6, 12, 34))?>")
	assert "@(2012-10-06T12:34:56)" == r("<?print repr(date(2012, 10, 6, 12, 34, 56))?>")
	if r is not render_php:
		assert "@(2012-10-06T12:34:56.987000)" == r("<?print repr(date(2012, 10, 6, 12, 34, 56, 987000))?>")

	# Make sure that the parameters have the same name in all implementations
	assert "@(2012-10-06T12:34:56)" == r("<?print repr(date(year=2012, month=10, day=6, hour=12, minute=34, second=56, microsecond=0))?>")


@pytest.mark.ul4
def test_function_timedelta(r):
	with raises(argumentmismatchmessage):
		r("<?print timedelta(1, 2, 3, 4)?>")
	assert "1 day, 0:00:00" == r("<?print timedelta(1)?>")
	assert "-1 day, 0:00:00" == r("<?print timedelta(-1)?>")
	assert "2 days, 0:00:00" == r("<?print timedelta(2)?>")
	assert "0:00:01" == r("<?print timedelta(0, 0, 1000000)?>")
	assert "1 day, 0:00:00" == r("<?print timedelta(0, 0, 24*60*60*1000000)?>")
	assert "1 day, 0:00:00" == r("<?print timedelta(0, 24*60*60)?>")
	assert "12:00:00" == r("<?print timedelta(0.5)?>")
	assert "0:00:00.500000" == r("<?print timedelta(0, 0.5)?>")
	assert "0:00:00.500000" == r("<?print timedelta(0.5/(24*60*60))?>")
	assert "-1 day, 12:00:00" == r("<?print timedelta(-0.5)?>")
	assert "-1 day, 23:59:59.500000" == r("<?print timedelta(0, -0.5)?>")
	assert "0:00:01" == r("<?print timedelta(0, 1)?>")
	assert "0:01:00" == r("<?print timedelta(0, 60)?>")
	assert "1:00:00" == r("<?print timedelta(0, 60*60)?>")
	assert "1 day, 1:01:01.000001" == r("<?print timedelta(1, 60*60+60+1, 1)?>")
	assert "0:00:00.000001" == r("<?print timedelta(0, 0, 1)?>")
	assert "-1 day, 23:59:59" == r("<?print timedelta(0, -1)?>")
	assert "-1 day, 23:59:59.999999" == r("<?print timedelta(0, 0, -1)?>")

	# Make sure that the parameters have the same name in all implementations
	assert "0:00:00.000001" == r("<?print timedelta(days=0, seconds=0, microseconds=1)?>")


@pytest.mark.ul4
def test_function_monthdelta(r):
	with raises(argumentmismatchmessage):
		r("<?print monthdelta(1, 2)?>")
	assert "0 months" == r("<?print monthdelta()?>")
	assert "2 months" == r("<?print monthdelta(2)?>")
	assert "1 month" == r("<?print monthdelta(1)?>")
	assert "-1 month" == r("<?print monthdelta(-1)?>")

	# Make sure that the parameters have the same name in all implementations
	assert "1 month" == r("<?print monthdelta(months=1)?>")


@pytest.mark.ul4
def test_function_random(r):
	with raises(argumentmismatchmessage):
		r("<?print random(1)?>")
	with raises(argumentmismatchmessage):
		r("<?print random(1, 2)?>")
	with raises(argumentmismatchmessage):
		r("<?print random(foo=1)?>")
	assert "ok" == r("<?code r = random()?><?if r>=0 and r<1?>ok<?else?>fail<?end if?>")


@pytest.mark.ul4
def test_function_randrange(r):
	with raises(argumentmismatchmessage):
		r("<?print randrange()?>")
	with raises(argumentmismatchmessage):
		r("<?print randrange(foo=1)?>")
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

	# Make sure that the parameters have the same name in all implementations
	assert "ok" == r("<?code s = [17, 23, 42]?><?code r = randchoice(sequence=s)?><?if r in s?>ok<?else?>fail<?end if?>")


@pytest.mark.ul4
def test_function_xmlescape(r):
	with raises(argumentmismatchmessage):
		r("<?print xmlescape()?>")
	with raises(argumentmismatchmessage):
		r("<?print xmlescape(1, 2)?>")
	assert "&lt;&lt;&gt;&gt;&amp;&#39;&quot;gurk" == r("<?print xmlescape(data)?>", data='<<>>&\'"gurk')

	# Make sure that the parameters have the same name in all implementations
	assert "42" == r("<?print xmlescape(obj=data)?>", data=42)


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

	# Make sure that the parameters have the same name in all implementations
	assert "42" == r("<?print csv(obj=data)?>", data=42)


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

	# Make sure that the parameters have the same name in all implementations
	assert "42" == r("<?print asjson(obj=data)?>", data=42)


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

	# Make sure that the parameters have the same name in all implementations
	assert "42" == r("<?print fromjson(string=data)?>", data="42")


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

	# Make sure that the parameters have the same name in all implementations
	assert "42" == r("<?print repr(fromul4on(string=asul4on(obj=data)))?>", data=42)


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
	if r is not render_php:
		assert "2011-02-09 12:34:56.987000" == r(code, data=datetime.datetime(2011, 2, 9, 12, 34, 56, 987000))
	assert "0:00:00" == r(code, data=datetime.timedelta())
	assert "1 day, 0:00:00" == r(code, data=datetime.timedelta(1))
	assert "-1 day, 0:00:00" == r(code, data=datetime.timedelta(-1))
	assert "2 days, 0:00:00" == r(code, data=datetime.timedelta(2))
	assert "0:00:01" == r(code, data=datetime.timedelta(0, 1))
	assert "0:01:00" == r(code, data=datetime.timedelta(0, 60))
	assert "1:00:00" == r(code, data=datetime.timedelta(0, 60*60))
	assert "1 day, 1:01:01.000001" == r(code, data=datetime.timedelta(1, 60*60+60+1, 1))
	assert "0:00:00.000001" == r(code, data=datetime.timedelta(0, 0, 1))
	assert "-1 day, 23:59:59" == r(code, data=datetime.timedelta(0, -1))
	assert "-1 day, 23:59:59.999999" == r(code, data=datetime.timedelta(0, 0, -1))

	# Make sure that the parameters have the same name in all implementations
	assert "42" == r("<?print str(obj=data)?>", data=42)


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

	# Make sure that the parameters have the same name in all implementations
	assert "True" == r("<?print bool(obj=data)?>", data=42)


@pytest.mark.ul4
def test_function_list(r):
	with raises(argumentmismatchmessage):
		r("<?print list(1, 2)?>")
	assert "[]" == r("<?print list()?>")
	assert "[1, 2]" == r("<?print list(data)?>", data=[1, 2])
	assert "g" == r("<?print list(data)[0]?>", data="gurk")
	assert "foo42" == r("<?codex = list(data.items())?><?print x[0][0]?><?print x[0][1]?>", data={"foo": 42})
	assert "[0, 1, 2]" == r("<?print repr(list(range(3)))?>")

	# Make sure that the parameters have the same name in all implementations
	assert "g" == r("<?print list(iterable=data)[0]?>", data="gurk")


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

	# Make sure that the parameters have the same name in all implementations
	assert "42" == r("<?print int(obj=data, base=None)?>", data=42)


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

		# Make sure that the parameters have the same name in all implementations
		assert "42.0" == r("<?print float(obj=data)?>", data=42)
	else:
		assert 0.0 == eval(r("<?print float()?>"))
		assert 1.0 == eval(r(code, data=True))
		assert 0.0 == eval(r(code, data=False))
		assert 42.0 == eval(r(code, data=42))
		assert 42.0 == eval(r(code, data="42"))

		# Make sure that the parameters have the same name in all implementations
		assert 42.0 == eval(r("<?print float(obj=data)?>", data=42))


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

	# Make sure that the parameters have the same name in all implementations
	assert "42" == r("<?print len(sequence=data)?>", data=42*"?")


@pytest.mark.ul4
def test_function_any(r):
	with raises(argumentmismatchmessage):
		r("<?print any()?>")
	with raises(argumentmismatchmessage):
		r("<?print any(1, 2)?>")
	with raises("is not iterable|any\\(.*\\) not supported"):
		r("<?print any(data)?>", data=None)
	assert "False" == r("<?print any('')?>")
	assert "True" == r("<?print any('foo')?>")
	assert "True" == r("<?print any(i > 7 for i in range(10))?>")
	assert "False" == r("<?print any(i > 17 for i in range(10))?>")

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print any(iterable=(i > 17 for i in range(10)))?>")


@pytest.mark.ul4
def test_function_all(r):
	with raises(argumentmismatchmessage):
		r("<?print all()?>")
	with raises(argumentmismatchmessage):
		r("<?print all(1, 2)?>")
	with raises("is not iterable|all\\(.*\\) not supported"):
		r("<?print all(data)?>", data=None)
	assert "True" == r("<?print all('')?>")
	assert "True" == r("<?print all('foo')?>")
	assert "False" == r("<?print all(i < 7 for i in range(10))?>")
	assert "True" == r("<?print all(i < 17 for i in range(10))?>")

	# Make sure that the parameters have the same name in all implementations
	assert "True" == r("<?print all(iterable=(i < 17 for i in range(10)))?>")


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

	# Make sure that the parameters have the same name in all implementations
	assert "(f=42)(o=43)(o=44)" == r("<?for (i, value) in enumerate(iterable=data, start=42)?>(<?print value?>=<?print i?>)<?end for?>", data="foo")


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

	# Make sure that the parameters have the same name in all implementations
	assert "[(f=42)(o=43)(o=44)]" == r("<?for (i, f, l, value) in enumfl(iterable=data, start=42)?><?if f?>[<?end if?>(<?print value?>=<?print i?>)<?if l?>]<?end if?><?end for?>", data="foo")


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

	# Make sure that the parameters have the same name in all implementations
	assert "[(f)(o)(o)]" == r("<?for (f, l, value) in isfirstlast(iterable=data)?><?if f?>[<?end if?>(<?print value?>)<?if l?>]<?end if?><?end for?>", data="foo")


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

	# Make sure that the parameters have the same name in all implementations
	assert "[(f)(o)(o)" == r("<?for (f, value) in isfirst(iterable=data)?><?if f?>[<?end if?>(<?print value?>)<?end for?>", data="foo")


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

	# Make sure that the parameters have the same name in all implementations
	assert "(f)(o)(o)]" == r("<?for (l, value) in islast(iterable=data)?>(<?print value?>)<?if l?>]<?end if?><?end for?>", data="foo")


@pytest.mark.ul4
def test_function_isundefined(r):
	code = "<?print isundefined(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isundefined()?>")
	with raises(argumentmismatchmessage):
		r("<?print isundefined(1, 2)?>")
	assert "True" == r(code)
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
	assert "False" == r("<?print isundefined(repr)?>")
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print isundefined(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_isdefined(r):
	code = "<?print isdefined(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isdefined()?>")
	with raises(argumentmismatchmessage):
		r("<?print isdefined(1, 2)?>")
	assert "False" == r(code)
	assert "True" == r(code, data=None)
	assert "True" == r(code, data=True)
	assert "True" == r(code, data=False)
	assert "True" == r(code, data=42)
	assert "True" == r(code, data=4.2)
	assert "True" == r(code, data="foo")
	assert "True" == r(code, data=datetime.datetime.now())
	assert "True" == r(code, data=datetime.timedelta(1))
	assert "True" == r(code, data=misc.monthdelta(1))
	assert "True" == r(code, data=())
	assert "True" == r(code, data=[])
	assert "True" == r(code, data={})
	assert "True" == r(code, data=ul4c.Template(""))
	assert "True" == r("<?print isdefined(repr)?>")
	assert "True" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "True" == r("<?print isdefined(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_isnone(r):
	code = "<?print isnone(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isnone()?>")
	with raises(argumentmismatchmessage):
		r("<?print isnone(1, 2)?>")
	assert "False" == r(code)
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
	assert "False" == r("<?print isnone(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "True" == r("<?print isnone(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_isbool(r):
	code = "<?print isbool(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isbool()?>")
	with raises(argumentmismatchmessage):
		r("<?print isbool(1, 2)?>")
	assert "False" == r(code)
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
	assert "False" == r("<?print isbool(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print isbool(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_isint(r):
	code = "<?print isint(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isint()?>")
	with raises(argumentmismatchmessage):
		r("<?print isint(1, 2)?>")
	assert "False" == r(code)
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
	assert "False" == r("<?print isint(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print isint(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_isfloat(r):
	code = "<?print isfloat(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isfloat()?>")
	with raises(argumentmismatchmessage):
		r("<?print isfloat(1, 2)?>")
	assert "False" == r(code)
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
	assert "False" == r("<?print isfloat(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print isfloat(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_isstr(r):
	code = "<?print isstr(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isstr()?>")
	with raises(argumentmismatchmessage):
		r("<?print isstr(1, 2)?>")
	assert "False" == r(code)
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
	assert "False" == r("<?print isstr(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print isstr(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_isdate(r):
	code = "<?print isdate(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isdate()?>")
	with raises(argumentmismatchmessage):
		r("<?print isdate(1, 2)?>")
	assert "False" == r(code)
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
	assert "False" == r("<?print isdate(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print isdate(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_islist(r):
	code = "<?print islist(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print islist()?>")
	with raises(argumentmismatchmessage):
		r("<?print islist(1, 2)?>")
	assert "False" == r(code)
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
	if r is not render_php:
		assert "False" == r(code, data={})
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r("<?print islist(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print islist(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_isdict(r):
	code = "<?print isdict(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isdict()?>")
	with raises(argumentmismatchmessage):
		r("<?print isdict(1, 2)?>")
	assert "False" == r(code)
	assert "False" == r(code, data=None)
	assert "False" == r(code, data=True)
	assert "False" == r(code, data=False)
	assert "False" == r(code, data=42)
	assert "False" == r(code, data=4.2)
	assert "False" == r(code, data="foo")
	assert "False" == r(code, data=datetime.datetime.now())
	assert "False" == r(code, data=datetime.timedelta(1))
	assert "False" == r(code, data=misc.monthdelta(1))
	if r is not render_php:
		assert "False" == r(code, data=())
		assert "False" == r(code, data=[])
	assert "True" == r(code, data={})
	assert "True" == r(code, data=PseudoDict({}))
	assert "False" == r(code, data=ul4c.Template(""))
	assert "False" == r("<?print isdict(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print isdict(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_istemplate(r):
	code = "<?print istemplate(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print istemplate()?>")
	with raises(argumentmismatchmessage):
		r("<?print istemplate(1, 2)?>")
	assert "False" == r(code)
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
	assert "False" == r("<?print istemplate(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print istemplate(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_isfunction(r):
	code = "<?print isfunction(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print isfunction()?>")
	with raises(argumentmismatchmessage):
		r("<?print isfunction(1, 2)?>")
	assert "False" == r(code)
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
	assert "True" == r("<?print isfunction(repr)?>")
	assert "True" == r("<?def f?><?return 42?><?end def?><?print isfunction(f)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print istemplate(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_iscolor(r):
	code = "<?print iscolor(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print iscolor()?>")
	with raises(argumentmismatchmessage):
		r("<?print iscolor(1, 2)?>")
	assert "False" == r(code)
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
	assert "False" == r("<?print iscolor(repr)?>")
	assert "True" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print iscolor(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_istimedelta(r):
	code = "<?print istimedelta(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print istimedelta()?>")
	with raises(argumentmismatchmessage):
		r("<?print istimedelta(1, 2)?>")
	assert "False" == r(code)
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
	assert "False" == r("<?print istimedelta(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print istimedelta(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_ismonthdelta(r):
	code = "<?print ismonthdelta(data)?>"

	with raises(argumentmismatchmessage):
		r("<?print ismonthdelta()?>")
	with raises(argumentmismatchmessage):
		r("<?print ismonthdelta(1, 2)?>")
	assert "False" == r(code)
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
	assert "False" == r("<?print ismonthdelta(repr)?>")
	assert "False" == r(code, data=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "False" == r("<?print ismonthdelta(obj=data)?>", data=None)


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
	if r is not render_php:
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

	# Make sure that the parameters have the same name in all implementations
	assert "None" == r("<?print repr(obj=data)?>", data=None)


@pytest.mark.ul4
def test_function_print(r):
	assert "gurk hurz hinz kunz" == r("<?code print('gurk', 'hurz', 'hinz', 'kunz')?>")


@pytest.mark.ul4
def test_function_printx(r):
	assert "&lt;gurk&gt; &lt;hurz&gt; &lt;hinz&gt; &lt;kunz&gt;" == r("<?code printx('<gurk>', '<hurz>', '<hinz>', '<kunz>')?>")


@pytest.mark.ul4
def test_function_format_date(r):
	t = datetime.datetime(2011, 1, 25, 13, 34, 56, 987000)
	code2 = "<?print format(data, fmt)?>"
	code3 = "<?print format(data, fmt, lang)?>"

	assert "2011" == r(code2, fmt="%Y", data=t)
	assert "01" == r(code2, fmt="%m", data=t)
	assert "25" == r(code2, fmt="%d", data=t)
	assert "13" == r(code2, fmt="%H", data=t)
	assert "34" == r(code2, fmt="%M", data=t)
	assert "56" == r(code2, fmt="%S", data=t)
	assert "987000" == r(code2, fmt="%f", data=t)
	assert "Tue" == r(code2, fmt="%a", data=t)
	assert "Tue" == r(code3, fmt="%a", data=t, lang=None)
	assert "Tue" == r(code3, fmt="%a", data=t, lang="en")
	assert "Di" == r(code3, fmt="%a", data=t, lang="de")
	assert "Di" == r(code3, fmt="%a", data=t, lang="de_DE")
	assert "Tuesday" == r(code2, fmt="%A", data=t)
	assert "Tuesday" == r(code3, fmt="%A", data=t, lang=None)
	assert "Tuesday" == r(code3, fmt="%A", data=t, lang="en")
	assert "Dienstag" == r(code3, fmt="%A", data=t, lang="de")
	assert "Dienstag" == r(code3, fmt="%A", data=t, lang="de_DE")
	assert "Jan" == r(code2, fmt="%b", data=t)
	assert "Jan" == r(code3, fmt="%b", data=t, lang=None)
	assert "Jan" == r(code3, fmt="%b", data=t, lang="en")
	assert "Jan" == r(code3, fmt="%b", data=t, lang="de")
	assert "Jan" == r(code3, fmt="%b", data=t, lang="de_DE")
	assert "January" == r(code2, fmt="%B", data=t)
	assert "January" == r(code3, fmt="%B", data=t, lang=None)
	assert "January" == r(code3, fmt="%B", data=t, lang="en")
	assert "Januar" == r(code3, fmt="%B", data=t, lang="de")
	assert "Januar" == r(code3, fmt="%B", data=t, lang="de_DE")
	assert "01" == r(code2, fmt="%I", data=t)
	assert "025" == r(code2, fmt="%j", data=t)
	assert "PM" == r(code2, fmt="%p", data=t)
	assert "04" == r(code2, fmt="%U", data=t)
	assert "2" == r(code2, fmt="%w", data=t)
	assert "04" == r(code2, fmt="%W", data=t)
	assert "11" == r(code2, fmt="%y", data=t)
	assert r(code2, fmt="%c", data=t) in ("Tue Jan 25 13:34:56 2011", "Tue 25 Jan 2011 01:34:56 PM", "Tue 25 Jan 2011 01:34:56 PM ")
	assert "01/25/2011" == r(code2, fmt="%x", data=t)
	assert "01/25/2011" == r(code3, fmt="%x", data=t, lang=None)
	assert "01/25/2011" == r(code3, fmt="%x", data=t, lang="en")
	assert "25.01.2011" == r(code3, fmt="%x", data=t, lang="de")
	assert "25.01.2011" == r(code3, fmt="%x", data=t, lang="de_DE")
	assert r(code2, fmt="%X", data=t) in ("13:34:56", "01:34:56 PM")
	assert r(code3, fmt="%X", data=t, lang=None) in ("13:34:56", "01:34:56 PM")
	assert r(code3, fmt="%X", data=t, lang="en") in ("13:34:56", "01:34:56 PM")
	assert "13:34:56" == r(code3, fmt="%X", data=t, lang="de")
	assert "13:34:56" == r(code3, fmt="%X", data=t, lang="de_DE")
	assert "%" == r(code2, fmt="%%", data=t)


@pytest.mark.ul4
def test_function_format_int(r):
	code2 = "<?print format(data, fmt)?>"
	code3 = "<?print format(data, fmt, lang)?>"

	formatstrings = [
		"",
		"",
		"5",
		"05",
		"05",
		"+05",
		"+8b",
		"+#10b",
		"o",
		"+#x",
		"+#X",
		"<5",
		">5",
		"?>5",
		"^5",
		"?= 5",
		"?= #11b",
	]

	for f in formatstrings:
		assert format(42, f) == r(code2, data=42, fmt=f)
		if "c" not in f:
			assert format(-42, f) == r(code2, data=-42, fmt=f)
	assert format(True, "05") == r(code2, data=True, fmt="05")


@pytest.mark.ul4
def test_function_format_kwargs(r):
	assert "42" == r("<?print format(obj=data, fmt=fmt, lang=lang)?>", fmt="", data=42, lang="de")


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

	# Make sure that the parameters have the same name in all implementations
	assert "\x00" == r("<?print chr(i=data)?>", data=0)


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

	# Make sure that the parameters have the same name in all implementations
	assert "0" == r("<?print ord(c=data)?>", data="\x00")


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

	# Make sure that the parameters have the same name in all implementations
	assert "0x0" == r("<?print hex(number=data)?>", data=0)


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

	# Make sure that the parameters have the same name in all implementations
	assert "0o0" == r("<?print oct(number=data)?>", data=0)


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
def test_function_bin_kwargs(r):
	assert "0b0" == r("<?print bin(number=data)?>", data=0)


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
	assert "1 month" == r(code, data=misc.monthdelta(-1))
	assert "1 day, 0:00:01.000001" == r(code, data=datetime.timedelta(-1, -1, -1))

	# Make sure that the parameters have the same name in all implementations
	assert "0" == r("<?print abs(number=data)?>", data=0)


@pytest.mark.ul4
def test_function_sorted(r):
	code = "<?for i in sorted(data)?><?print i?><?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print sorted()?>")
	assert "gkru" == r(code, data="gurk")
	assert "24679" == r(code, data="92746")
	assert "172342" == r(code, data=(42, 17, 23))
	assert "012" == r(code, data={0: "zero", 1: "one", 2: "two"})

	# Make sure that the parameters have the same name in all implementations
	assert "123" == r("<?for i in sorted(iterable=data)?><?print i?><?end for?>", data="321")


@pytest.mark.ul4
def test_function_range(r):
	code1 = "<?for i in range(data)?><?print i?>;<?end for?>"
	code2 = "<?for i in range(data[0], data[1])?><?print i?>;<?end for?>"
	code3 = "<?for i in range(data[0], data[1], data[2])?><?print i?>;<?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print range()?>")
	with raises(argumentmismatchmessage):
		r("<?print range(1, 2, 3, 4)?>")
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
def test_function_slice(r):
	code2 = "<?for i in slice(data[0], data[1])?><?print i?>;<?end for?>"
	code3 = "<?for i in slice(data[0], data[1], data[2])?><?print i?>;<?end for?>"
	code4 = "<?for i in slice(data[0], data[1], data[2], data[3])?><?print i?>;<?end for?>"

	with raises(argumentmismatchmessage):
		r("<?print slice(1)?>")
	with raises(argumentmismatchmessage):
		r("<?print slice(1, 2, 3, 4, 5)?>")
	assert "g;u;r;k;" == r(code2, data=("gurk", None))
	assert "g;u;" == r(code2, data=("gurk", 2))
	assert "u;r;" == r(code3, data=("gurk", 1, 3))
	assert "u;r;k;" == r(code3, data=("gurk", 1, None))
	assert "g;u;" == r(code3, data=("gurk", None, 2))
	assert "u;u;" == r(code4, data=("gurkgurk", 1, 6, 4))


@pytest.mark.ul4
def test_function_urlquote(r):
	assert "gurk" == r("<?print urlquote('gurk')?>")
	assert "%3C%3D%3E%2B%3F" == r("<?print urlquote('<=>+?')?>")
	assert "%7F%C3%BF%EF%BF%BF" == r("<?print urlquote('\u007f\u00ff\uffff')?>")

	# Make sure that the parameters have the same name in all implementations
	assert "gurk" == r("<?print urlquote(string='gurk')?>")


@pytest.mark.ul4
def test_function_urlunquote(r):
	assert "gurk" == r("<?print urlunquote('gurk')?>")
	assert "<=>+?" == r("<?print urlunquote('%3C%3D%3E%2B%3F')?>")
	assert "\u007f\u00ff\uffff" == r("<?print urlunquote('%7F%C3%BF%EF%BF%BF')?>")

	# Make sure that the parameters have the same name in all implementations
	assert "gurk" == r("<?print urlunquote(string='gurk')?>")


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
	assert "undefined" == r(code)
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
	assert "template" == r("<?def t?><?end def?><?print type(t)?>")
	assert "function" == r("<?print type(repr)?>")
	assert "color" == r(code, x=color.red)

	# Make sure that the parameters have the same name in all implementations
	assert "none" == r("<?print type(obj=x)?>", x=None)


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

	# Make sure that the parameters have the same name in all implementations
	assert "(3)(2)(1)" == r("<?for i in reversed(sequence=x)?>(<?print i?>)<?end for?>", x=(1, 2, 3))


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
def test_function_sum(r):
	with raises(argumentmismatchmessage):
		r("<?print sum()?>")

	assert "0" == r("<?print sum([])?>")
	assert "6" == r("<?print sum([1, 2, 3])?>")
	assert "12" == r("<?print sum([1, 2, 3], 6)?>")
	assert "5050" == r("<?print sum(range(101))?>")

	assert "12" == r("<?print sum(iterable=[1, 2, 3], start=6)?>")


@pytest.mark.ul4
def test_function_first(r):
	assert "g" == r("<?print first('gurk')?>")
	assert "None" == r("<?print repr(first(''))?>")
	assert "x" == r("<?print first('', 'x')?>")

	assert "x" == r("<?print first(iterable='', default='x')?>")


@pytest.mark.ul4
def test_function_last(r):
	assert "k" == r("<?print last('gurk')?>")
	assert "None" == r("<?print repr(last(''))?>")
	assert "x" == r("<?print last('', 'x')?>")

	assert "x" == r("<?print last(iterable='', default='x')?>")


@pytest.mark.ul4
def test_function_rgb(r):
	assert "#369" == r("<?print repr(rgb(0.2, 0.4, 0.6))?>")
	assert "#369c" == r("<?print repr(rgb(0.2, 0.4, 0.6, 0.8))?>")

	# Make sure that the parameters have the same name in all implementations
	assert "#369c" == r("<?print repr(rgb(r=0.2, g=0.4, b=0.6, a=0.8))?>")


@pytest.mark.ul4
def test_function_hls(r):
	assert "#fff" == r("<?print repr(hls(0, 1, 0))?>")
	assert "#fff0" == r("<?print repr(hls(0, 1, 0, 0))?>")

	# Make sure that the parameters have the same name in all implementations
	assert "#fff0" == r("<?print repr(hls(h=0, l=1, s=0, a=0))?>")


@pytest.mark.ul4
def test_function_hsv(r):
	assert "#fff" == r("<?print repr(hsv(0, 0, 1))?>")
	assert "#fff0" == r("<?print repr(hsv(0, 0, 1, 0))?>")

	# Make sure that the parameters have the same name in all implementations
	assert "#fff0" == r("<?print repr(hsv(h=0, s=0, v=1, a=0))?>")


@pytest.mark.ul4
def test_method_upper(r):
	assert "GURK" == r("<?print 'gurk'.upper()?>")
	assert "GURK" == r("<?code m = 'gurk'.upper?><?print m()?>")


@pytest.mark.ul4
def test_method_lower(r):
	assert "gurk" == r("<?print 'GURK'.lower()?>")
	assert "gurk" == r("<?code m = 'GURK'.lower?><?print m()?>")


@pytest.mark.ul4
def test_method_capitalize(r):
	assert "Gurk" == r("<?print 'gURK'.capitalize()?>")
	assert "Gurk" == r("<?code m = 'gURK'.capitalize?><?print m()?>")


@pytest.mark.ul4
def test_method_startswith(r):
	assert "True" == r("<?print 'gurkhurz'.startswith('gurk')?>")
	assert "False" == r("<?print 'gurkhurz'.startswith('hurz')?>")
	assert "False" == r("<?code m = 'gurkhurz'.startswith?><?print m('hurz')?>")

	# Make sure that the parameters have the same name in all implementations
	assert "True" == r("<?print 'gurkhurz'.startswith(prefix='gurk')?>")


@pytest.mark.ul4
def test_method_endswith(r):
	assert "True" == r("<?print 'gurkhurz'.endswith('hurz')?>")
	assert "False" == r("<?print 'gurkhurz'.endswith('gurk')?>")
	assert "False" == r("<?code m = 'gurkhurz'.endswith?><?print m('gurk')?>")

	# Make sure that the parameters have the same name in all implementations
	assert "True" == r("<?print 'gurkhurz'.endswith(suffix='hurz')?>")


@pytest.mark.ul4
def test_method_strip(r):
	assert "gurk" == r(r"<?print obj.strip()?>", obj=' \t\r\ngurk \t\r\n')
	assert "gurk" == r(r"<?print obj.strip('xyz')?>", obj='xyzzygurkxyzzy')
	assert "gurk" == r(r"<?code m = obj.strip?><?print m('xyz')?>", obj='xyzzygurkxyzzy')

	# Make sure that the parameters have the same name in all implementations
	assert "gurk" == r(r"<?print obj.strip(chars='xyz')?>", obj='xyzzygurkxyzzy')


@pytest.mark.ul4
def test_method_lstrip(r):
	assert "gurk \t\r\n" == r("<?print obj.lstrip()?>", obj=" \t\r\ngurk \t\r\n")
	assert "gurkxyzzy" == r("<?print obj.lstrip(arg)?>", obj="xyzzygurkxyzzy", arg="xyz")
	assert "gurkxyzzy" == r("<?code m = obj.lstrip?><?print m(arg)?>", obj="xyzzygurkxyzzy", arg="xyz")

	# Make sure that the parameters have the same name in all implementations
	assert "gurkxyzzy" == r("<?print obj.lstrip(chars=arg)?>", obj="xyzzygurkxyzzy", arg="xyz")


@pytest.mark.ul4
def test_method_rstrip(r):
	assert " \t\r\ngurk" == r("<?print obj.rstrip()?>", obj=" \t\r\ngurk \t\r\n")
	assert "xyzzygurk" == r("<?print obj.rstrip(arg)?>", obj="xyzzygurkxyzzy", arg="xyz")
	assert "xyzzygurk" == r("<?code m = obj.rstrip?><?print m(arg)?>", obj="xyzzygurkxyzzy", arg="xyz")

	# Make sure that the parameters have the same name in all implementations
	assert "xyzzygurk" == r("<?print obj.rstrip(chars=arg)?>", obj="xyzzygurkxyzzy", arg="xyz")


@pytest.mark.ul4
def test_method_split(r):
	assert "(f)(o)(o)" == r("<?for item in obj.split()?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "(f)(o \t\r\no \t\r\n)" == r("<?for item in obj.split(None, 1)?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "()(f)(o)(o)()" == r("<?for item in obj.split(arg)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")
	assert "()(f)(oxxoxx)" == r("<?for item in obj.split(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")
	assert "()(f)(oxxoxx)" == r("<?code m = obj.split?><?for item in m(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")

	# Make sure that the parameters have the same name in all implementations
	assert "()(f)(oxxoxx)" == r("<?for item in obj.split(sep=arg, count=2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")


@pytest.mark.ul4
def test_method_rsplit(r):
	assert "(f)(o)(o)" == r("<?for item in obj.rsplit()?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "( \t\r\nf \t\r\no)(o)" == r("<?for item in obj.rsplit(None, 1)?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "()(f)(o)(o)()" == r("<?for item in obj.rsplit(arg)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")
	assert "(xxfxxo)(o)()" == r("<?for item in obj.rsplit(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")
	assert "(xxfxxo)(o)()" == r("<?code m = obj.rsplit?><?for item in m(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")

	# Make sure that the parameters have the same name in all implementations
	assert "(xxfxxo)(o)()" == r("<?for item in obj.rsplit(sep=arg, count=2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")


@pytest.mark.ul4
def test_method_replace(r):
	assert 'goork' == r("<?print 'gurk'.replace('u', 'oo')?>")
	assert 'fuuuu' == r("<?print 'foo'.replace('o', 'uu', None)?>")
	assert 'fuuo' == r("<?print 'foo'.replace('o', 'uu', 1)?>")
	assert 'fuuo' == r("<?code m = 'foo'.replace?><?print m('o', 'uu', 1)?>")

	# Make sure that the parameters have the same name in all implementations
	assert 'fuuo' == r("<?print 'foo'.replace(old='o', new='uu', count=1)?>")


@pytest.mark.ul4
def test_method_renders(r):
	t = ul4c.Template('(<?print data?>)')
	assert '(GURK)' == r("<?print t.renders(data='gurk').upper()?>", t=t)
	assert '(GURK)' == r("<?print t.renders(**{'data': 'gurk'}).upper()?>", t=t)
	assert '(GURK)' == r("<?code m = t.renders?><?print m(**{'data': 'gurk'}).upper()?>", t=t)

	t = ul4c.Template('(gurk)')
	assert '(GURK)' == r("<?print t.renders().upper()?>", t=t)


@pytest.mark.ul4
def test_method_mimeformat(r):
	t = datetime.datetime(2010, 2, 22, 12, 34, 56)

	assert 'Mon, 22 Feb 2010 12:34:56 GMT' == r("<?print data.mimeformat()?>", data=t)
	assert 'Mon, 22 Feb 2010 12:34:56 GMT' == r("<?code m = data.mimeformat?><?print m()?>", data=t)


@pytest.mark.ul4
def test_method_items(r):
	assert "a:42;b:17;c:23;" == r("<?for (key, value) in sorted(data.items())?><?print key?>:<?print value?>;<?end for?>", data=dict(a=42, b=17, c=23))
	assert "a:42;b:17;c:23;" == r("<?code m = data.items?><?for (key, value) in sorted(m())?><?print key?>:<?print value?>;<?end for?>", data=dict(a=42, b=17, c=23))


@pytest.mark.ul4
def test_method_values(r):
	assert "17;23;42;" == r("<?for value in sorted(data.values())?><?print value?>;<?end for?>", data=dict(a=42, b=17, c=23))
	assert "17;23;42;" == r("<?code m = data.values?><?for value in sorted(m())?><?print value?>;<?end for?>", data=dict(a=42, b=17, c=23))


@pytest.mark.ul4
def test_method_get(r):
	assert "42" == r("<?print {}.get('foo', 42)?>")
	assert "17" == r("<?print {'foo': 17}.get('foo', 42)?>")
	assert "" == r("<?print {}.get('foo')?>")
	assert "17" == r("<?print {'foo': 17}.get('foo')?>")
	assert "17" == r("<?code m = {'foo': 17}.get?><?print m('foo')?>")

	# Make sure that the parameters have the same name in all implementations
	assert "17" == r("<?print {'foo': 17}.get(key='foo', default=42)?>")


@pytest.mark.ul4
def test_method_r_g_b_a(r):
	assert '0x11' == r('<?code c = #123?><?print hex(c.r())?>')
	assert '0x11' == r('<?code c = #123?><?code m = c.r?><?print hex(m())?>')
	assert '0x22' == r('<?code c = #123?><?print hex(c.g())?>')
	assert '0x22' == r('<?code c = #123?><?code m = c.g?><?print hex(m())?>')
	assert '0x33' == r('<?code c = #123?><?print hex(c.b())?>')
	assert '0x33' == r('<?code c = #123?><?code m = c.b?><?print hex(m())?>')
	assert '0xff' == r('<?code c = #123?><?print hex(c.a())?>')
	assert '0xff' == r('<?code c = #123?><?code m = c.a?><?print hex(m())?>')


@pytest.mark.ul4
def test_method_hls(r):
	assert '0' == r('<?code c = #fff?><?print int(c.hls()[0])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hls()[1])?>')
	assert '0' == r('<?code c = #fff?><?print int(c.hls()[2])?>')
	assert '0' == r('<?code c = #fff?><?code m = c.hls?><?print int(m()[0])?>')


@pytest.mark.ul4
def test_method_hlsa(r):
	assert '0' == r('<?code c = #fff?><?print int(c.hlsa()[0])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hlsa()[1])?>')
	assert '0' == r('<?code c = #fff?><?print int(c.hlsa()[2])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hlsa()[3])?>')
	assert '0' == r('<?code c = #fff?><?code m = c.hlsa?><?print int(m()[0])?>')


@pytest.mark.ul4
def test_method_hsv(r):
	assert '0' == r('<?code c = #fff?><?print int(c.hsv()[0])?>')
	assert '0' == r('<?code c = #fff?><?print int(c.hsv()[1])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hsv()[2])?>')
	assert '0' == r('<?code c = #fff?><?code m = c.hsv?><?print int(m()[0])?>')


@pytest.mark.ul4
def test_method_hsva(r):
	assert '0' == r('<?code c = #fff?><?print int(c.hsva()[0])?>')
	assert '0' == r('<?code c = #fff?><?print int(c.hsva()[1])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hsva()[2])?>')
	assert '1' == r('<?code c = #fff?><?print int(c.hsva()[3])?>')
	assert '0' == r('<?code c = #fff?><?code m = c.hsva?><?print int(m()[0])?>')


@pytest.mark.ul4
def test_method_lum(r):
	assert 'True' == r('<?print #fff.lum() == 1?>')
	assert 'True' == r('<?code m = #fff.lum?><?print m() == 1?>')


@pytest.mark.ul4
def test_method_withlum(r):
	assert '#fff' == r('<?print #000.withlum(1)?>')
	assert '#fff' == r('<?code m = #000.withlum?><?print m(1)?>')

	# Make sure that the parameters have the same name in all implementations
	assert '#fff' == r('<?print #000.withlum(lum=1)?>')


@pytest.mark.ul4
def test_method_witha(r):
	assert '#0063a82a' == r('<?print repr(#0063a8.witha(42))?>')
	assert '#0063a82a' == r('<?code m = #0063a8.witha?><?print repr(m(42))?>')

	# Make sure that the parameters have the same name in all implementations
	assert '#0063a82a' == r('<?print repr(#0063a8.witha(a=42))?>')


@pytest.mark.ul4
def test_method_join(r):
	assert '1,2,3,4' == r('<?print ",".join("1234")?>')
	assert '1,2,3,4' == r('<?print ",".join(["1", "2", "3", "4"])?>')
	assert '1,2,3,4' == r('<?code m = ",".join?><?print m("1234")?>')

	# Make sure that the parameters have the same name in all implementations
	assert '1,2,3,4' == r('<?print ",".join(iterable="1234")?>')


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
	assert '-1' == r('<?code m = s.find?><?print m("rk", 7)?>', s=s)
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
	assert '-1' == r('<?code m = l.find?><?print m("r", 7)?>', l=l)

	# Make sure that the parameters have the same name in all implementations
	assert '2' == r('<?print s.find(sub="rk", start=2, end=4)?>', s=s)


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
	assert '-1' == r('<?code m = s.rfind?><?print m("rk", 7)?>', s=s)
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
	assert '-1' == r('<?code m = l.rfind?><?print m("r", 7)?>', l=l)

	# Make sure that the parameters have the same name in all implementations
	assert '2' == r('<?print s.rfind(sub="rk", start=2, end=4)?>', s=s)


@pytest.mark.ul4
def test_method_day(r):
	assert '12' == r('<?print @(2010-05-12).day()?>')
	assert '12' == r('<?print d.day()?>', d=datetime.date(2010, 5, 12))
	assert '12' == r('<?code m = @(2010-05-12).day?><?print m()?>')


@pytest.mark.ul4
def test_method_month(r):
	assert '5' == r('<?print @(2010-05-12).month()?>')
	assert '5' == r('<?print d.month()?>', d=datetime.date(2010, 5, 12))
	assert '5' == r('<?code m = @(2010-05-12).month?><?print m()?>')


@pytest.mark.ul4
def test_method_year(r):
	assert '5' == r('<?print @(2010-05-12).month()?>')
	assert '5' == r('<?print d.month()?>', d=datetime.date(2010, 5, 12))
	assert '5' == r('<?code m = @(2010-05-12).month?><?print m()?>')


@pytest.mark.ul4
def test_method_hour(r):
	assert '16' == r('<?print @(2010-05-12T16:47:56).hour()?>')
	assert '16' == r('<?print d.hour()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))
	assert '16' == r('<?code m = @(2010-05-12T16:47:56).hour?><?print m()?>')


@pytest.mark.ul4
def test_method_minute(r):
	assert '47' == r('<?print @(2010-05-12T16:47:56).minute()?>')
	assert '47' == r('<?print d.minute()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))
	assert '47' == r('<?code m = @(2010-05-12T16:47:56).minute?><?print m()?>')


@pytest.mark.ul4
def test_method_second(r):
	assert '56' == r('<?print @(2010-05-12T16:47:56).second()?>')
	assert '56' == r('<?print d.second()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))
	assert '56' == r('<?code m = @(2010-05-12T16:47:56).second?><?print m()?>')


@pytest.mark.ul4
def test_method_microsecond(r):
	if r is not render_php:
		assert '123000' == r('<?print @(2010-05-12T16:47:56.123000).microsecond()?>')
		assert '123000' == r('<?print d.microsecond()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56, 123000))
		assert '123000' == r('<?code m = @(2010-05-12T16:47:56.123000).microsecond?><?print m()?>')


@pytest.mark.ul4
def test_method_weekday(r):
	assert '2' == r('<?print @(2010-05-12).weekday()?>')
	assert '2' == r('<?print d.weekday()?>', d=datetime.date(2010, 5, 12))
	assert '2' == r('<?code m = @(2010-05-12).weekday?><?print m()?>')


@pytest.mark.ul4
def test_method_week(r):
	assert '0' == r('<?print @(2012-01-01).week()?>')
	assert '0' == r('<?print @(2012-01-01).week(0)?>')
	assert '1' == r('<?print @(2012-01-01).week(6)?>')
	assert '1' == r('<?print @(2012-01-02).week()?>')
	assert '1' == r('<?print @(2012-01-02).week(0)?>')
	assert '1' == r('<?print @(2012-01-02).week(6)?>')
	assert '0' == r('<?code m = @(2012-01-01).week?><?print m()?>')

	# Make sure that the parameters have the same name in all implementations
	assert '1' == r('<?print @(2012-01-02).week(firstweekday=0)?>')


@pytest.mark.ul4
def test_method_yearday(r):
	assert '1' == r('<?print @(2010-01-01).yearday()?>')
	assert '366' == r('<?print @(2008-12-31).yearday()?>')
	assert '365' == r('<?print @(2010-12-31).yearday()?>')
	assert '132' == r('<?print @(2010-05-12).yearday()?>')
	assert '132' == r('<?print @(2010-05-12T16:47:56).yearday()?>')
	assert '132' == r('<?print d.yearday()?>', d=datetime.date(2010, 5, 12))
	assert '132' == r('<?print d.yearday()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))
	assert '1' == r('<?code m = @(2010-01-01).yearday?><?print m()?>')


@pytest.mark.ul4
def test_method_days(r):
	assert '1' == r('<?print timedelta(1).days()?>')
	assert '1' == r('<?code m = timedelta(1).days?><?print m()?>')


@pytest.mark.ul4
def test_method_seconds(r):
	assert '42' == r('<?print timedelta(0, 42).seconds()?>')
	assert '42' == r('<?code m = timedelta(0, 42).seconds?><?print m()?>')


@pytest.mark.ul4
def test_method_microseconds(r):
	assert '123000' == r('<?print timedelta(0, 0, 123000).microseconds()?>')
	assert '123000' == r('<?code m = timedelta(0, 0, 123000).microseconds?><?print m()?>')


@pytest.mark.ul4
def test_method_months(r):
	assert '17' == r('<?print monthdelta(17).months()?>')
	assert '17' == r('<?code m = monthdelta(17).months?><?print m()?>')


@pytest.mark.ul4
def test_method_append(r):
	assert '[17, 23, 42]' == r('<?code l = [17]?><?code l.append(23, 42)?><?print l?>')
	assert '[17, 23, 42]' == r('<?code l = [17]?><?code m = l.append?><?code m(23, 42)?><?print l?>')


@pytest.mark.ul4
def test_method_insert(r):
	assert '[1, 2, 3, 4]' == r('<?code l = [1,4]?><?code l.insert(1, 2, 3)?><?print l?>')
	assert '[1, 2, 3, 4]' == r('<?code l = [1,4]?><?code m = l.insert?><?code m(1, 2, 3)?><?print l?>')


@pytest.mark.ul4
def test_method_pop(r):
	assert '42;17;23;' == r('<?code l = [17, 23, 42]?><?print l.pop()?>;<?print l.pop(-2)?>;<?print l.pop(0)?>;')
	assert '42;17;23;' == r('<?code l = [17, 23, 42]?><?code m = l.pop?><?print m()?>;<?print m(-2)?>;<?print m(0)?>;')


@pytest.mark.ul4
def test_method_update(r):
	assert '0' == r('<?code d = {}?><?code d.update()?><?print len(d)?>')
	assert '1' == r('<?code d = {}?><?code d.update([["one", 1]])?><?print d.one?>')
	assert '1' == r('<?code d = {}?><?code d.update({"one": 1})?><?print d.one?>')
	assert '1' == r('<?code d = {}?><?code d.update(one=1)?><?print d.one?>')
	assert '1' == r('<?code d = {}?><?code d.update([["one", 0]], {"one": 0}, one=1)?><?print d.one?>')
	assert '1' == r('<?code d = {}?><?code m = d.update?><?code m(one=1)?><?print d.one?>')


@pytest.mark.ul4
def test_method_render(r):
	t = ul4c.Template('<?print prefix?><?print data?><?print suffix?>')

	assert '(f)(o)(o)' == r('<?for c in data?><?code t.render(data=c, prefix="(", suffix=")")?><?end for?>', t=t, data='foo')
	assert '(f)(o)(o)' == r('<?for c in data?><?code t.render(data=c, **{"prefix": "(", "suffix": ")"})?><?end for?>', t=t, data='foo')
	assert '(f)(o)(o)' == r('<?code m = t.render?><?for c in data?><?code m(data=c, prefix="(", suffix=")")?><?end for?>', t=t, data='foo')


@pytest.mark.ul4
def test_def(r):
	assert 'foo' == r('<?def lower?><?print x.lower()?><?end def?><?print lower.renders(x="FOO")?>')


@pytest.mark.ul4
def test_pass_function(r):
	assert "&lt;" == r("<?def x?><?print xe('<')?><?end def?><?code x.render(xe=xmlescape)?>")
	assert "&lt;" == r("<?def xe?><?return xmlescape(s)?><?end def?><?def x?><?print xe(s='<')?><?end def?><?code x.render(xe=xe)?>")
	assert "&lt;" == r("<?def xe?><?return xmlescape(s)?><?end def?><?def x?><?print xe(s='<')?><?end def?><?code x.render()?>")


@pytest.mark.ul4
def test_parse(r):
	assert '42' == r('<?print data.Noner?>', data=dict(Noner=42))


@pytest.mark.ul4
def test_nested_exceptions(r):
	tmpl1 = ul4c.Template("<?print 2*x?>", "tmpl1")
	tmpl2 = ul4c.Template("<?code tmpl1.render(x=x)?>", "tmpl2")
	tmpl3 = ul4c.Template("<?code tmpl2.render(tmpl1=tmpl1, x=x)?>", "tmpl3")

	with raises("unsupported operand type|not supported"):
		r("<?code tmpl3.render(tmpl1=tmpl1, tmpl2=tmpl2, x=x)?>", tmpl1=tmpl1, tmpl2=tmpl2, tmpl3=tmpl3, x=None)


@pytest.mark.ul4
def test_note(r):
	assert "foo" == r("f<?note This is?>o<?note a comment?>o")


@pytest.mark.ul4
def test_templateattributes(r):
	s1 = "<?print x?>"
	t1 = ul4c.Template(s1)

	s2 = "<?printx 42?>"
	t2 = ul4c.Template(s2)

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
	assert "const" == r("<?print template.content[0].obj.type?>", template=t2)
	assert "42" == r("<?print template.content[0].obj.value?>", template=t2)


@pytest.mark.ul4
def test_templateattributes_localtemplate(r):
	# This checks that template attributes work on a closure
	source = "<?def lower?><?print t.lower()?><?end def?>"

	assert source + "<?print lower.source?>" == r(source + "<?print lower.source?>")
	assert source == r(source + "<?print lower.source[lower.location.starttag:lower.endlocation.endtag]?>")
	assert "<?print t.lower()?>" == r(source + "<?print lower.source[lower.location.endtag:lower.endlocation.starttag]?>")
	assert "lower" == r(source + "<?print lower.name?>")


@pytest.mark.ul4
def test_nestedscopes(r):
	# Subtemplates can see the local variables from their parents
	source = """
	<?for i in range(3)?>
		<?def x?>
			<?print i?>!
		<?end def?>
		<?code x.render()?>
	<?end for?>
	"""
	assert "0!1!2!" == r(source, keepws=False)

	# Subtemplates see the state of the variable at the point after the ``<?def?>`` tag,
	# so the following code will use ``i = 1`` instead of ``i = 2`` even if the subtemplate is called after the variable has been changed.
	source = """
	<?code i = 1?>
	<?def x?>
		<?print i?>
	<?end def?>
	<?code i = 2?>
	<?code x.render()?>
	"""
	assert "1" == r(source, keepws=False)


	# Subtemplates see themselves (i.e. the ``TemplateClosure`` object created for them), but no variables defined later
	source = """
	<?def x?>
		<?print type(x)?>;<?print type(y)?>
	<?end def?>
	<?code y = 42?>
	<?code x.render()?>
	"""
	assert "template;undefined" == r(source, keepws=False)

	# This shows the difference between local variables and variables from the parent.
	# ``x`` is passed to the subtemplate, so it will always be the current value instead of the one when it is defined
	# (Furthermore ``y += 1`` will load the variable from the parent but store it as a local variable)
	source = """
	<?def outer?>
		<?def inner?>
			<?code x += 1?>
			<?code y += 1?>
			<?print x?>!
			<?print y?>!
		<?end def?>
		<?code x += 1?>
		<?code y += 1?>
		<?code inner.render(x=x)?>
		<?print x?>!
		<?print y?>!
	<?end def?>
	<?code x += 1?>
	<?code y += 1?>
	<?code outer.render(x=x)?>
	<?print x?>!
	<?print y?>!
	"""

	assert "45!43!44!43!43!43!" == r(source, keepws=False, x=42, y=42)


def universaltemplate(keepws=True):
	return ul4c.Template("""
		text
		<?code x = 'gurk'?>
		<?code x = 42?>
		<?code x = 4.2?>
		<?code x = Undefined?>
		<?code x = ReallyUndefined?>
		<?code x = None?>
		<?code x = False?>
		<?code x = True?>
		<?code x = @(2009-01-04)?>
		<?code x = #0063a8?>
		<?code x = [42]?>
		<?code x = {"fortytwo": 42}?>
		<?code x = [x for x in range(10) if i % 2]?>
		<?code x = {x : x*x for x in range(10) if i % 2}?>
		<?code x = (x for x in range(10) if i % 2)?>
		<?code x = y?>
		<?code x += 42?>
		<?code x -= 42?>
		<?code x *= 42?>
		<?code x /= 42?>
		<?code x //= 42?>
		<?code x %= 42?>
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
		<?print repr(1, 2, x=17, y=23, *args, **kwargs)?>
		<?print x.r()?>
		<?print x.find(1)?>
		<?print x.find(1, 2)?>
		<?print x.find(1, 2, 3)?>
		<?print x.find(1, 2, x=17, y=23, *args, **kwargs)?>
		<?if x?>gurk<?elif y?>hurz<?else?>hinz<?end if?>
		<?code x.render(a=1, b=2)?>
		<?def x?>foo<?end def?>
		<?def x?><?return x?><?end def?>
		<?code x.render()?>
	""")


@pytest.mark.ul4
def test_strtemplate():
	t1 = universaltemplate(True)
	str(t1)

	t2 = universaltemplate(False)
	str(t2)


@pytest.mark.ul4
def test_keepws():
	s = """
		<?for i in range(10)?>
			<?print i?>
			;
		<?end for?>
	"""
	t = ul4c.Template(s, keepws=True)
	output1 = t.renders()
	t.keepws = False
	output2 = t.renders()
	assert output1 != output2
	assert "".join(output1.split()) == output2


@pytest.mark.ul4
def test_keepws_initialws(r):
	assert " foo" == r("<?if True?> foo<?end if?>", keepws=False)
	assert " foobar" == r("<?if True?> foo\n \tbar<?end if?>", keepws=False)


@pytest.mark.ul4
def test_keepws_nested(r):
	s1 = "<?def nested1?>1n\n<?code second.render()?><?end def?>1\n<?code nested1.render(second=second)?>"
	s2 = "<?def nested2?>2n\n<?end def?>2\n<?code nested2.render()?>"

	assert "1\n1n\n22n" == r(s1, keepws=True, second=ul4c.Template(s2, keepws=False))
	assert "11n2\n2n\n" == r(s1, keepws=False, second=ul4c.Template(s2, keepws=True))


@pytest.mark.ul4
def test_function(c):
	assert 42 == c("<?return 42?>")


@pytest.mark.ul4
def test_function_value(c):
	assert 84 == c("<?return 2*x?>", x=42)


@pytest.mark.ul4
def test_function_multiple_returnvalues(c):
	assert 84 == c("<?return 2*x?><?return 3*x?>", x=42)


@pytest.mark.ul4
def test_function_name(c):
	assert "f" == c("<?def f?><?return f.name?><?end def?><?return f(f=f)?>")


@pytest.mark.ul4
def test_function_closure(c):
	assert 24 == c("<?code y=3?><?def inner?><?return 2*x*y?><?end def?><?return inner(x=4)?>")
	assert 24 == c("<?def outer?><?code y=3?><?def inner?><?return 2*x*y?><?end def?><?return inner?><?end def?><?return outer()(x=4)?>")


@pytest.mark.ul4
def test_return_in_template(r):
	assert "gurk" == r("gurk<?return 42?>hurz")


@pytest.mark.ul4
def test_customattributes():
	class CustomAttributes:
		ul4attrs = {"foo", "+bar"}
		def __init__(self, foo, bar):
			self.foo = foo
			self.bar = bar

	o = CustomAttributes(foo=42, bar=23)
	assert "42" == render_python("<?print o.foo?>", o=o)
	assert "23" == render_python("<?print o.bar?>", o=o)
	assert "undefined" == render_python("<?print type(o.baz)?>", o=o)
	assert "42" == render_python("<?print o['foo']?>", o=o)
	assert "23" == render_python("<?print o['bar']?>", o=o)
	assert "undefined" == render_python("<?print type(o['baz'])?>", o=o)
	assert "True" == render_python("<?print 'foo' in o?>", o=o)
	assert "True" == render_python("<?print 'bar' in o?>", o=o)
	assert "False" == render_python("<?print 'baz' in o?>", o=o)
	assert "[['bar', 23], ['foo', 42]]" == render_python("<?print repr(sorted(list(o.items())))?>", o=o)
	assert "[23, 42]" == render_python("<?print repr(sorted(list(o.values())))?>", o=o)
	assert "foo" == render_python("<?for attr in o?><?if attr == 'foo'?><?print attr?><?end if?><?end for?>", o=o)
	assert "bar" == render_python("<?for attr in o?><?if attr == 'bar'?><?print attr?><?end if?><?end for?>", o=o)

	o = CustomAttributes(foo=42, bar=23)
	with raises("readonly"):
		render_python("<?code o.foo = 43?><?print o.foo?>", o=o)
	with raises("readonly"):
		render_python("<?code o['foo'] = 43?><?print o.foo?>", o=o)
	assert "17" == render_python("<?code o.bar = 17?><?print o.bar?>", o=o)
	assert "17" == render_python("<?code o['bar'] = 17?><?print o.bar?>", o=o)

	o = CustomAttributes(foo=42, bar=23)
	with raises("readonly"):
		render_python("<?code o.foo += 1?><?print o.foo?>", o=o)
	with raises("readonly"):
		render_python("<?code o['foo'] += 1?><?print o.foo?>", o=o)
	assert "24" == render_python("<?code o.bar += 1?><?print o.bar?>", o=o)
	assert "25" == render_python("<?code o['bar'] += 1?><?print o.bar?>", o=o)

	o = CustomAttributes(foo=42, bar=23)
	with raises("readonly"):
		render_python("<?code o.foo -= 1?><?print o.foo?>", o=o)
	with raises("readonly"):
		render_python("<?code o['foo'] -= 1?><?print o.foo?>", o=o)
	assert "22" == render_python("<?code o.bar -= 1?><?print o.bar?>", o=o)
	assert "21" == render_python("<?code o['bar'] -= 1?><?print o.bar?>", o=o)

	o = CustomAttributes(foo=42, bar=23)
	with raises("readonly"):
		render_python("<?code o.foo *= 2?><?print o.foo?>", o=o)
	with raises("readonly"):
		render_python("<?code o['foo'] *= 2?><?print o.foo?>", o=o)
	assert "46" == render_python("<?code o.bar *= 2?><?print o.bar?>", o=o)
	assert "92" == render_python("<?code o['bar'] *= 2?><?print o.bar?>", o=o)

	o = CustomAttributes(foo=42, bar=23)
	with raises("readonly"):
		render_python("<?code o.foo //= 2?><?print o.foo?>", o=o)
	with raises("readonly"):
		render_python("<?code o['foo'] //= 2?><?print o.foo?>", o=o)
	assert "11" == render_python("<?code o.bar //= 2?><?print o.bar?>", o=o)
	assert "5" == render_python("<?code o['bar'] //= 2?><?print o.bar?>", o=o)

	o = CustomAttributes(foo=42, bar=23)
	with raises("readonly"):
		render_python("<?code o.foo /= 2?><?print o.foo?>", o=o)
	with raises("readonly"):
		render_python("<?code o['foo'] /= 2?><?print o.foo?>", o=o)
	assert "11.5" == render_python("<?code o.bar /= 2?><?print o.bar?>", o=o)
	assert "5.75" == render_python("<?code o['bar'] /= 2?><?print o.bar?>", o=o)

	o = CustomAttributes(foo=42, bar=23)
	with raises("readonly"):
		render_python("<?code o.foo %= 2?><?print o.foo?>", o=o)
	with raises("readonly"):
		render_python("<?code o['foo'] %= 2?><?print o.foo?>", o=o)
	assert "3" == render_python("<?code o.bar %= 10?><?print o.bar?>", o=o)
	assert "1" == render_python("<?code o['bar'] %= 2?><?print o.bar?>", o=o)


@pytest.mark.ul4
def test_custommethods():
	class CustomMethod:
		ul4attrs = {"foo", "bar"}

		def foo(self):
			return 42

		@ul4c.generator
		def bar(self):
			yield "gurk"
			yield "hurz"
			return 42

		def baz(self):
			pass

	o = CustomMethod()
	assert "42" == render_python("<?print o.foo()?>", o=o)
	assert "gurkhurz42" == render_python("<?print o.bar()?>", o=o)
	with raises("baz"):
		render_python("<?print o.baz()?>", o=o)


@pytest.mark.ul4
def test_setlvalue(r):
	assert "bar" == r("<?code d = {}?><?code d.foo = 'bar'?><?print d.foo?>")
	assert "bar" == r("<?code d = {}?><?code d['foo'] = 'bar'?><?print d['foo']?>")
	assert "bar" == r("<?code d = ['bar']?><?code d[0] = 'bar'?><?print d[0]?>")
	assert "baz" == r("<?code d = {'foo': {}}?><?code d.foo.bar = 'baz'?><?print d.foo.bar?>")
	assert "baz" == r("<?code d = {'foo': {}}?><?code d.foo['bar'] = 'baz'?><?print d.foo['bar']?>")
	assert "baz" == r("<?code d = {'foo': ['bar']}?><?code d.foo[0] = 'baz'?><?print d.foo[0]?>")
	assert "baz" == r("<?code d = ['bar']?><?def f?><?return d?><?end def?><?code f()[0] = 'baz'?><?print d[0]?>")


@pytest.mark.ul4
def test_addlvalue(r):
	assert "barbaz" == r("<?code d = {'foo': 'bar'}?><?code d.foo += 'baz'?><?print d.foo?>")
	assert "barbaz" == r("<?code d = {'foo': 'bar'}?><?code d['foo'] += 'baz'?><?print d['foo']?>")
	assert "barbaz" == r("<?code d = ['bar']?><?code d[0] += 'baz'?><?print d[0]?>")
	assert "barbaz" == r("<?code d = {'foo': {'bar' : 'bar'}}?><?code d.foo.bar += 'baz'?><?print d.foo.bar?>")
	assert "barbaz" == r("<?code d = {'foo': {'bar' : 'bar'}}?><?code d.foo['bar'] += 'baz'?><?print d.foo['bar']?>")
	assert "barbaz" == r("<?code d = {'foo': ['bar']}?><?code d.foo[0] += 'baz'?><?print d.foo[0]?>")
	assert "barbaz" == r("<?code d = ['bar']?><?def f?><?return d?><?end def?><?code f()[0] += 'baz'?><?print d[0]?>")
	assert "[1, 2, 3, 4][1, 2, 3, 4]" == r("<?code d = {'foo': [1, 2]}?><?code l = d.foo?><?code d.foo += [3, 4]?><?print d.foo?><?print l?>")


@pytest.mark.ul4
def test_sublvalue(r):
	assert "6" == r("<?code d = {'foo': 23}?><?code d.foo -= 17?><?print d.foo?>")
	assert "6" == r("<?code d = {'foo': 23}?><?code d['foo'] -= 17?><?print d['foo']?>")
	assert "6" == r("<?code d = [23]?><?code d[0] -= 17?><?print d[0]?>")
	assert "6" == r("<?code d = {'foo': {'bar' : 23}}?><?code d.foo.bar -= 17?><?print d.foo.bar?>")
	assert "6" == r("<?code d = {'foo': {'bar' : 23}}?><?code d.foo['bar'] -= 17?><?print d.foo['bar']?>")
	assert "6" == r("<?code d = {'foo': [23]}?><?code d.foo[0] -= 17?><?print d.foo[0]?>")
	assert "6" == r("<?code d = [23]?><?def f?><?return d?><?end def?><?code f()[0] -= 17?><?print d[0]?>")


@pytest.mark.ul4
def test_mullvalue(r):
	assert "42" == r("<?code d = {'foo': 6}?><?code d.foo *= 7?><?print d.foo?>")
	assert "42" == r("<?code d = {'foo': 6}?><?code d['foo'] *= 7?><?print d['foo']?>")
	assert "42" == r("<?code d = [6]?><?code d[0] *= 7?><?print d[0]?>")
	assert "42" == r("<?code d = {'foo': {'bar' : 6}}?><?code d.foo.bar *= 7?><?print d.foo.bar?>")
	assert "42" == r("<?code d = {'foo': {'bar' : 6}}?><?code d.foo['bar'] *= 7?><?print d.foo['bar']?>")
	assert "42" == r("<?code d = {'foo': [6]}?><?code d.foo[0] *= 7?><?print d.foo[0]?>")
	assert "42" == r("<?code d = [6]?><?def f?><?return d?><?end def?><?code f()[0] *= 7?><?print d[0]?>")
	assert "[1, 2, 1, 2][1, 2, 1, 2]" == r("<?code d = {'foo': [1, 2]}?><?code l = d.foo?><?code d.foo *= 2?><?print d.foo?><?print l?>")


@pytest.mark.ul4
def test_floordivlvalue(r):
	assert "2" == r("<?code d = {'foo': 5}?><?code d.foo //= 2?><?print d.foo?>")
	assert "2" == r("<?code d = {'foo': 5}?><?code d['foo'] //= 2?><?print d['foo']?>")
	assert "2" == r("<?code d = [5]?><?code d[0] //= 2?><?print d[0]?>")
	assert "2" == r("<?code d = {'foo': {'bar' : 5}}?><?code d.foo.bar //= 2?><?print d.foo.bar?>")
	assert "2" == r("<?code d = {'foo': {'bar' : 5}}?><?code d.foo['bar'] //= 2?><?print d.foo['bar']?>")
	assert "2" == r("<?code d = {'foo': [5]}?><?code d.foo[0] //= 2?><?print d.foo[0]?>")
	assert "2" == r("<?code d = [5]?><?def f?><?return d?><?end def?><?code f()[0] //= 2?><?print d[0]?>")


@pytest.mark.ul4
def test_truedivlvalue(r):
	assert "2.5" == r("<?code d = {'foo': 5}?><?code d.foo /= 2?><?print d.foo?>")
	assert "2.5" == r("<?code d = {'foo': 5}?><?code d['foo'] /= 2?><?print d['foo']?>")
	assert "2.5" == r("<?code d = [5]?><?code d[0] /= 2?><?print d[0]?>")
	assert "2.5" == r("<?code d = {'foo': {'bar' : 5}}?><?code d.foo.bar /= 2?><?print d.foo.bar?>")
	assert "2.5" == r("<?code d = {'foo': {'bar' : 5}}?><?code d.foo['bar'] /= 2?><?print d.foo['bar']?>")
	assert "2.5" == r("<?code d = {'foo': [5]}?><?code d.foo[0] /= 2?><?print d.foo[0]?>")
	assert "2.5" == r("<?code d = [5]?><?def f?><?return d?><?end def?><?code f()[0] /= 2?><?print d[0]?>")


@pytest.mark.ul4
def test_truedivlvalue(r):
	assert "1" == r("<?code d = {'foo': 5}?><?code d.foo %= 2?><?print d.foo?>")
	assert "1" == r("<?code d = {'foo': 5}?><?code d['foo'] %= 2?><?print d['foo']?>")
	assert "1" == r("<?code d = [5]?><?code d[0] %= 2?><?print d[0]?>")
	assert "1" == r("<?code d = {'foo': {'bar' : 5}}?><?code d.foo.bar %= 2?><?print d.foo.bar?>")
	assert "1" == r("<?code d = {'foo': {'bar' : 5}}?><?code d.foo['bar'] %= 2?><?print d.foo['bar']?>")
	assert "1" == r("<?code d = {'foo': [5]}?><?code d.foo[0] %= 2?><?print d.foo[0]?>")
	assert "1" == r("<?code d = [5]?><?def f?><?return d?><?end def?><?code f()[0] %= 2?><?print d[0]?>")


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
