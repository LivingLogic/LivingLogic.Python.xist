#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3

## Copyright 2011-2014 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2011-2014 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import sys, io, os, datetime, math, tempfile, shutil, subprocess

from ll import ul4on, ul4c, color, misc


def transport_python(obj):
	return ul4on.loads(ul4on.dumps(obj))


def transport_js(obj):
	"""
	Generate Javascript source that loads the dump done by Python, dumps it
	again, and outputs this dump which is again loaded by Python.

	(this requires an installed ``d8`` shell from V8 (http://code.google.com/p/v8/))
	"""
	dump = ul4on.dumps(obj)
	js = "obj = ul4on.loads({});\nprint(ul4on.dumps(obj));\n".format(ul4c._asjson(dump))
	f = sys._getframe(1)
	print("Testing UL4ON via Javascript ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
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
	output = stdout[:-1] # Drop the "\n"
	return ul4on.loads(output)


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
	Compile the Java source :obj:`source`, run it and return the output
	"""
	maincodetemplate = """
	public class UL4ONTest
	{
		@SuppressWarnings("unchecked")
		public static void main(String[] args) throws java.io.IOException, java.io.UnsupportedEncodingException, org.antlr.runtime.RecognitionException, ClassNotFoundException
		{
			// Force the JVM to register the UL4 classes for UL4ON
			Class.forName("com.livinglogic.ul4.InterpretedTemplate");
			%(source)s
		}
	}
	"""

	tempdir = tempfile.mkdtemp()
	try:
		source = maincodetemplate % dict(source=source)
		source = java_formatsource(source)
		print(source)
		with open(os.path.join(tempdir, "UL4ONTest.java"), "wb") as f:
			f.write(source.encode("utf-8"))
		proc = subprocess.Popen("cd {}; javac -encoding utf-8 UL4ONTest.java".format(tempdir), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		(stdout, stderr) = proc.communicate()
		if proc.returncode:
			stderr = stderr.decode("utf-8")
			print(stderr, file=sys.stderr)
			raise RuntimeError(stderr.splitlines()[0])
		proc = subprocess.Popen("cd {}; java UL4ONTest".format(tempdir), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		(stdout, stderr) = proc.communicate()
		# Check if we have an exception
		java_findexception(stderr.decode("utf-8"))
	finally:
		shutil.rmtree(tempdir)
	if stderr:
		print(stderr, file=sys.stderr)
	return stdout.decode("utf-8")


def transport_java(obj):
	"""
	Generate Java source that loads the dump done by Python, dumps it again,
	and outputs this dump which is again loaded by Python.

	(this requires an installed Java compiler and the Java UL4 jar)
	"""

	codetemplate = """
	String input = %(dump)s;
	Object object = com.livinglogic.ul4on.Utils.loads(input);
	String output = com.livinglogic.ul4on.Utils.dumps(object);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	dump = ul4on.dumps(obj)
	f = sys._getframe(1)
	print("Testing UL4ON via Java ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
	java = codetemplate % dict(dump=misc.javaexpr(dump))
	output = java_runsource(java)
	return ul4on.loads(output)


all_transports =  [
	("python", transport_python),
	("js", transport_js),
	("java", transport_java),
]


def pytest_generate_tests(metafunc):
	if "t" in metafunc.funcargnames:
		metafunc.parametrize("t", [t for (id, t) in all_transports], ids=[id for (id, t) in all_transports])


def test_none(t):
	assert None is t(None)


def test_bool(t):
	assert False == t(False)
	assert True == t(True)


def test_int(t):
	assert 42 == t(42)


def test_float(t):
	assert -42.5 == t(-42.5)
	assert math.pi == t(math.pi)


def test_string(t):
	assert "gurk" == t("gurk")


def test_color(t):
	c = color.Color(0x66, 0x99, 0xcc, 0xff)
	assert c == t(c)


def test_datetime(t):
	d = datetime.datetime(2012, 10, 29, 16, 44, 55, 987000)
	assert d == t(d)


def test_timedelta(t):
	d = datetime.timedelta(1, 1, 1)
	assert d == t(d)


def test_monthdelta(t):
	d = misc.monthdelta(1)
	assert d == t(d)


def test_slice(t):
	d = slice(None, None)
	assert d == t(d)
	d = slice(1, None)
	assert d == t(d)
	d = slice(None, 3)
	assert d == t(d)
	d = slice(1, 3)
	assert d == t(d)


def test_list(t):
	assert [] == t([])
	assert [1, 2, 3] == t([1, 2, 3])


def test_dict(t):
	assert {} == t({})


def test_template(t):
	template = ul4c.Template("<?for i in range(10)?>(<?print i?>)<?end for?>")
	assert template.renders() == t(template).renders()


def test_nested(t):
	d = {
		"nix": None,
		"int": 42,
		"float": math.pi,
		"foo": "bar",
		"baz": datetime.datetime(2012, 10, 29, 16, 44, 55, 987000),
		"td": datetime.timedelta(-1, 1, 1),
		"md": misc.monthdelta(-1),
		"gurk": ["hurz"],
	}
	assert d == t(d)
