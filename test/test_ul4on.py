#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2011-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2011-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import sys, io, os, json, datetime, math, tempfile, shutil, subprocess

import pytest

from ll import ul4on, ul4c, color, misc


# For the Oracle tests to work the environment variable ``LL_ORASQL_TEST_CONNECT``
# must point to an Oracle schema where the UL4ON package from
# https://github.com/LivingLogic/LivingLogic.Oracle.ul4 is installed

@pytest.fixture(scope="module")
def oracle(request):
	connectstring = os.environ.get("LL_ORASQL_TEST_CONNECT")
	if connectstring:
		from ll import orasql
		db = orasql.connect(connectstring, readlobs=True)
		cursor = db.cursor()
		def run(code):
			cursor.execute("""
				create or replace function ul4ontest
				return clob
				as
					c_out clob;
				begin
					{}
					return c_out;
				end;
			""".format(code))
			cursor.execute("select ul4ontest from dual")
			dump = cursor.fetchone().ul4ontest
			return ul4on.loads(dump)
		return run
	else:
		return None


def _transport_python(obj, indent):
	return ul4on.loads(ul4on.dumps(obj, indent=indent))


def transport_python(obj):
	return _transport_python(obj, indent="")


def transport_python_pretty(obj):
	return _transport_python(obj, indent="\t")


def _transport_js_v8(obj, indent):
	"""
	Generate Javascript source that loads the dump done by Python, dumps it
	again, and outputs this dump which is again loaded by Python.

	(this requires an installed ``d8`` shell from V8 (http://code.google.com/p/v8/))
	"""
	dump = ul4on.dumps(obj, indent=indent)
	js = "obj = ul4on.loads({});\nprint(ul4on.dumps(obj, {}));\n".format(ul4c._asjson(dump), ul4c._asjson(indent))
	f = sys._getframe(1)
	print("Testing UL4ON via V8 ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
	print(js)
	with tempfile.NamedTemporaryFile(mode="wb", suffix=".js") as f:
		f.write(js.encode("utf-8"))
		f.flush()
		dir = os.path.expanduser("~/checkouts/LivingLogic.Javascript.ul4")
		fmt = "d8 {dir}/ul4.js {fn}"
		result = subprocess.run(fmt.format(dir=dir, fn=f.name), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	stdout = result.stdout.decode("utf-8")
	stderr = result.stderr.decode("utf-8")
	# Check if we have an exception
	if result.returncode:
		print(stdout, file=sys.stdout)
		print(stderr, file=sys.stderr)
		raise RuntimeError((stderr or stdout).splitlines()[0])
	output = stdout[:-1] # Drop the "\n"
	print("Got result {!r}".format(output))
	return ul4on.loads(output)


def transport_js_v8(obj):
	return _transport_js_v8(obj, indent="")


def transport_js_v8_pretty(obj):
	return _transport_js_v8(obj, indent="\t")


def _transport_js_spidermonkey(obj, indent):
	"""
	Generate Javascript source that loads the dump done by Python, dumps it
	again, and outputs this dump which is again loaded by Python.

	(this requires an installed ``js`` shell from Spidermonkey
	"""
	dump = ul4on.dumps(obj, indent=indent)
	js = "obj = ul4on.loads({});\nprint(JSON.stringify(ul4on.dumps(obj, {})));\n".format(ul4c._asjson(dump), ul4c._asjson(indent))
	f = sys._getframe(1)
	print("Testing UL4ON via Spidermonkey ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
	print(js)
	with tempfile.NamedTemporaryFile(mode="wb", suffix=".js") as f:
		f.write(js.encode("utf-8"))
		f.flush()
		dir = os.path.expanduser("~/checkouts/LivingLogic.Javascript.ul4")
		fmt = "js -f {dir}/ul4.js -f {fn}"
		result = subprocess.run(fmt.format(dir=dir, fn=f.name), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	stdout = result.stdout.decode("utf-8")
	stderr = result.stderr.decode("utf-8")
	# Check if we have an exception
	if result.returncode:
		print(stdout, file=sys.stdout)
		print(stderr, file=sys.stderr)
		raise RuntimeError((stderr or stdout).splitlines()[0])
	print("Got result {!r}".format(stdout))
	return ul4on.loads(json.loads(stdout))


def transport_js_spidermonkey(obj):
	return _transport_js_spidermonkey(obj, indent="")


def transport_js_spidermonkey_pretty(obj):
	return _transport_js_spidermonkey(obj, indent="\t")


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
	stderr = stdout = None
	try:
		source = maincodetemplate % dict(source=source)
		source = java_formatsource(source)
		print(source)
		with open(os.path.join(tempdir, "UL4ONTest.java"), "wb") as f:
			f.write(source.encode("utf-8"))
		result = subprocess.run("cd {}; javac -encoding utf-8 UL4ONTest.java".format(tempdir), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		if result.returncode:
			stderr = result.stderr.decode("utf-8")
			print(stderr, file=sys.stderr)
			raise RuntimeError(stderr.splitlines()[0])
		result = subprocess.run("cd {}; java UL4ONTest".format(tempdir), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout = result.stdout.decode("utf-8")
		# Check if we have an exception
		java_findexception(result.stderr.decode("utf-8"))
	finally:
		shutil.rmtree(tempdir)
	if stderr:
		print(stderr, file=sys.stderr)
	return stdout


def _transport_java(obj, indent):
	"""
	Generate Java source that loads the dump done by Python, dumps it again,
	and outputs this dump which is again loaded by Python.

	(this requires an installed Java compiler and the Java UL4 jar)
	"""

	codetemplate = """
	String input = %(dump)s;
	Object object = com.livinglogic.ul4on.Utils.loads(input);
	String output = com.livinglogic.ul4on.Utils.dumps(object, %(indent)s);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	dump = ul4on.dumps(obj, indent=indent)
	f = sys._getframe(1)
	print("Testing UL4ON via Java ({}, line {}):".format(f.f_code.co_filename, f.f_lineno))
	java = codetemplate % dict(dump=misc.javaexpr(dump), indent=misc.javaexpr(indent))
	output = java_runsource(java)
	return ul4on.loads(output)


def transport_java(obj):
	return _transport_java(obj, indent="")


def transport_java_pretty(obj):
	return _transport_java(obj, indent="\t")


all_transports = [
	("python", transport_python),
	("python_pretty", transport_python_pretty),
	("js_v8", transport_js_v8),
	("js_v8_pretty", transport_js_v8_pretty),
	("js_spidermonkey", transport_js_spidermonkey),
	("js_spidermonkey_pretty", transport_js_spidermonkey_pretty),
	("java", transport_java),
	("java_pretty", transport_java_pretty),
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
	assert -42 == t(-42)


def test_float(t):
	assert -42.5 == t(-42.5)
	if t not in (transport_js_v8, transport_js_v8_pretty, transport_js_spidermonkey, transport_js_spidermonkey_pretty):
		assert 1e42 == t(1e42)
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
	d = {}
	assert d == t(d)
	d = {"gurk": "hurz"}
	assert d == t(d)
	if t not in (transport_js_v8, transport_js_v8_pretty):
		d = {17: None, None: 23}
		assert d == t(d)


def test_set(t):
	if t not in (transport_js_v8, transport_js_v8_pretty):
		assert set() == t(set())
		assert {1, 2, 3} == t({1, 2, 3})


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


def test_recursion(t):
	if t not in (transport_js_v8, transport_js_v8_pretty, transport_js_spidermonkey, transport_js_spidermonkey_pretty):
		l1 = []
		l1.append(l1)

		l2 = t(l1)
		assert len(l2) == 1
		assert l2[0] is l2


@pytest.mark.db
def test_oracle_none(oracle):
	if oracle:
		assert None is oracle("ul4on_pkg.none(c_out);")


@pytest.mark.db
def test_oracle_bool(oracle):
	if oracle:
		assert None is oracle("ul4on_pkg.bool(c_out, null);")
		assert False is oracle("ul4on_pkg.bool(c_out, 0);")
		assert True is oracle("ul4on_pkg.bool(c_out, 1);")


@pytest.mark.db
def test_oracle_int(oracle):
	if oracle:
		assert None is oracle("ul4on_pkg.int(c_out, null);")
		assert 42 == oracle("ul4on_pkg.int(c_out, 42);")
		assert 0 == oracle("ul4on_pkg.int(c_out, 0);")
		assert -42 == oracle("ul4on_pkg.int(c_out, -42);")


@pytest.mark.db
def test_oracle_float(oracle):
	if oracle:
		assert None is oracle("ul4on_pkg.float(c_out, null);")
		assert 42.5 == oracle("ul4on_pkg.float(c_out, 42.5);")
		assert 0.0 == oracle("ul4on_pkg.float(c_out, 0);")
		assert -42.5 == oracle("ul4on_pkg.float(c_out, -42.5);")


@pytest.mark.db
def test_oracle_str(oracle):
	if oracle:
		assert "foo" == oracle("ul4on_pkg.str(c_out, 'foo');")
		assert "\x00\a\b\t\n\r\x1b" == oracle("ul4on_pkg.str(c_out, chr(0) || chr(7) || chr(8) || chr(9) || chr(10) || chr(13) || chr(27));")
		assert "\xa0äöüÄÖÜß€" == oracle("ul4on_pkg.str(c_out, '\xa0äöüÄÖÜß\u20ac');")
		assert "foo" == oracle("ul4on_pkg.str(c_out, to_clob('foo'));")


@pytest.mark.db
def test_oracle_color(oracle):
	if oracle:
		assert color.Color(0x66, 0x99, 0xcc, 0xff) == oracle("ul4on_pkg.color(c_out, 102, 153, 204, 255);")


@pytest.mark.db
def test_oracle_datetime(oracle):
	if oracle:
		assert datetime.datetime(2014, 11, 6, 12, 34, 56) == oracle("ul4on_pkg.datetime(c_out, to_date('2014-11-06 12:34:56', 'YYYY-MM-DD HH24:MI:SS'));")
		assert datetime.datetime(2014, 11, 6, 12, 34, 56, 987654) == oracle("ul4on_pkg.datetime(c_out, to_timestamp('2014-11-06 12:34:56,987654', 'YYYY-MM-DD HH24:MI:SS,FF6'));")


@pytest.mark.db
def test_oracle_timedelta(oracle):
	if oracle:
		assert datetime.timedelta(days=42) == oracle("ul4on_pkg.timedelta(c_out, 42);")
		assert datetime.timedelta(days=1, seconds=2, microseconds=3) == oracle("ul4on_pkg.timedelta(c_out, 1, 2, 3);")


@pytest.mark.db
def test_oracle_monthdelta(oracle):
	if oracle:
		assert misc.monthdelta(42) == oracle("ul4on_pkg.monthdelta(c_out, 42);")
		assert misc.monthdelta(-42) == oracle("ul4on_pkg.monthdelta(c_out, -42);")


@pytest.mark.db
def test_oracle_slice(oracle):
	if oracle:
		assert slice(None, None) == oracle("ul4on_pkg.slice(c_out, null, null);")
		assert slice(1, None) == oracle("ul4on_pkg.slice(c_out, 1, null);")
		assert slice(None, 3) == oracle("ul4on_pkg.slice(c_out, null, 3);")
		assert slice(1, 3) == oracle("ul4on_pkg.slice(c_out, 1, 3);")


@pytest.mark.db
def test_oracle_list(oracle):
	if oracle:
		assert [] == oracle("""
			ul4on_pkg.beginlist(c_out);
			ul4on_pkg.endlist(c_out);
		""")
		assert [None, 42, "foo"] == oracle("""
			ul4on_pkg.beginlist(c_out);
				ul4on_pkg.none(c_out);
				ul4on_pkg.int(c_out, 42);
				ul4on_pkg.str(c_out, 'foo');
			ul4on_pkg.endlist(c_out);
		""")


@pytest.mark.db
def test_oracle_set(oracle):
	if oracle:
		assert set() == oracle("""
			ul4on_pkg.beginset(c_out);
			ul4on_pkg.endset(c_out);
		""")
		assert {None, 42, "foo"} == oracle("""
			ul4on_pkg.beginset(c_out);
				ul4on_pkg.none(c_out);
				ul4on_pkg.int(c_out, 42);
				ul4on_pkg.str(c_out, 'foo');
			ul4on_pkg.endset(c_out);
		""")


@pytest.mark.db
def test_oracle_dict(oracle):
	if oracle:
		assert {} == oracle("""
			ul4on_pkg.begindict(c_out);
			ul4on_pkg.enddict(c_out);
		""")
		assert {"foo": None, "bar": 42, 42: [1, 2, 3]} == oracle("""
			ul4on_pkg.begindict(c_out);
				ul4on_pkg.keynone(c_out, 'foo');
				ul4on_pkg.keyint(c_out, 'bar', 42);
				ul4on_pkg.int(c_out, 42);
				ul4on_pkg.beginlist(c_out);
					ul4on_pkg.int(c_out, 1);
					ul4on_pkg.int(c_out, 2);
					ul4on_pkg.int(c_out, 3);
				ul4on_pkg.endlist(c_out);
			ul4on_pkg.enddict(c_out);
		""")


@pytest.mark.db
def test_oracle_object(oracle):
	if oracle:
		@ul4on.register("de.livinglogic.xist.ul4on.test.person")
		class Person:
			def __init__(self, firstname=None, lastname=None):
				self.firstname = firstname
				self.lastname = lastname

			def ul4ondump(self, encoder):
				encoder.dump(self.firstname)
				encoder.dump(self.lastname)

			def ul4onload(self, decoder):
				self.firstname = decoder.load()
				self.lastname = decoder.load()

		assert {} == oracle("""
			ul4on_pkg.begindict(c_out);
			ul4on_pkg.enddict(c_out);
		""")
		assert {"foo": None, "bar": 42, 42: [1, 2, 3]} == oracle("""
			ul4on_pkg.begindict(c_out);
				ul4on_pkg.keynone(c_out, 'foo');
				ul4on_pkg.keyint(c_out, 'bar', 42);
				ul4on_pkg.int(c_out, 42);
				ul4on_pkg.beginlist(c_out);
					ul4on_pkg.int(c_out, 1);
					ul4on_pkg.int(c_out, 2);
					ul4on_pkg.int(c_out, 3);
				ul4on_pkg.endlist(c_out);
			ul4on_pkg.enddict(c_out);
		""")
		p = oracle("""
			ul4on_pkg.beginobject(c_out, 'de.livinglogic.xist.ul4on.test.person');
				ul4on_pkg.str(c_out, 'Otto');
				ul4on_pkg.str(c_out, 'Normalverbraucher');
			ul4on_pkg.endobject(c_out);
		""")

		assert isinstance(p, Person)
		assert p.firstname == "Otto"
		assert p.lastname == "Normalverbraucher"
