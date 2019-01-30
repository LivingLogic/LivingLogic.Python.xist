#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2011-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2011-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import sys, io, os, json, datetime, math, tempfile, shutil, subprocess

import pytest

from ll import ul4on, ul4c, color, misc


home = os.environ["HOME"]

# For the Oracle tests to work the environment variable ``LL_ORASQL_TEST_CONNECT``
# must point to an Oracle schema where the packages ``UL4ON_PKG`` and
# ``UL4ONBUFFER_PKG`` from https://github.com/LivingLogic/LivingLogic.Oracle.ul4
# are installed


def oracle_ul4on(code):
	"""
	A test fixture that will execute the PL/SQL code passed in as a parameter.
	This PL/SQL code must output an UL4ON dump into the PL/SQL variable ``c_out``
	by using the ``UL4ON_PKG`` package. The package name is available as the
	function attribute ``pkg``.

	:func:`oracle_ul4on` returns the deserialized object dump as a Python object.

	For example::

		oracle('''
			{oracle.pkg}.begindict(c_out);
			{oracle.pkg}.enddict(c_out);
		''')

	should return a empty dictionary.
	"""
	connectstring = os.environ.get("LL_ORASQL_TEST_CONNECT")
	if connectstring:
		from ll import orasql
		db = orasql.connect(connectstring, readlobs=True)
		cursor = db.cursor()
		print(code)
		cursor.execute(f"""
			create or replace function ul4ontest
			return clob
			as
				c_out clob;
			begin
				{code}
				return c_out;
			end;
		""")
		cursor.execute("select ul4ontest from dual")
		dump = cursor.fetchone().ul4ontest
		return ul4on.loads(dump)
	else:
		return None

oracle_ul4on.pkg = "ul4on_pkg"


def oracle_ul4onbuffer(code):
	"""
	A test fixture that will execute the PL/SQL code passed in as a parameter.
	This PL/SQL code must output an UL4ON dump into the PL/SQL variable ``c_out``
	by using the ``UL4ONBUFFER_PKG`` package. The package name is available as
	the function attribute ``pkg``.

	:func:`oracle_ul4onbuffer` returns the deserialized object dump as a Python
	object.

	For example::

		oracle('''
			{oracle.pkg}.begindict(c_out);
			{oracle.pkg}.enddict(c_out);
		''')

	should return a empty dictionary.

	Note that call to ``UL4ONBUFFER_PKG.INIT()`` and ``UL4ONBUFFER_PKG.FLUSH()``
	are not required in the code passed in (this makes it possible to call
	:func:`oracle_ul4on` and :func:`oracle_ul4onbuffer` with the code).
	"""
	connectstring = os.environ.get("LL_ORASQL_TEST_CONNECT")
	if connectstring:
		from ll import orasql
		db = orasql.connect(connectstring, readlobs=True)
		cursor = db.cursor()
		cursor.execute(f"""
			create or replace function ul4ontest
			return clob
			as
				c_out clob;
			begin
				ul4onbuffer_pkg.init(c_out);
				{code}
				ul4onbuffer_pkg.flush(c_out);
				return c_out;
			end;
		""")
		cursor.execute("select ul4ontest from dual")
		dump = cursor.fetchone().ul4ontest
		return ul4on.loads(dump)
	else:
		return None

oracle_ul4onbuffer.pkg = "ul4onbuffer_pkg"


all_oracles = [
	("oracle_ul4on", oracle_ul4on),
	("oracle_ul4onbuffer", oracle_ul4onbuffer),
]


def _transport_python(obj, indent, registry):
	return ul4on.loads(ul4on.dumps(obj, indent=indent), registry=registry)


def transport_python(obj, registry=None):
	return _transport_python(obj, indent="", registry=registry)


def transport_python_pretty(obj, registry=None):
	return _transport_python(obj, indent="\t", registry=registry)


def _transport_js_v8(obj, indent):
	"""
	Generate Javascript source that loads the dump done by Python, dumps it
	again, and outputs this dump which is again loaded by Python.

	(this requires an installed ``d8`` shell from V8 (http://code.google.com/p/v8/))
	"""
	dump = ul4on.dumps(obj, indent=indent)
	js = f"obj = ul4on.loads({ul4c._asjson(dump)});\nprint(ul4on.dumps(obj, {ul4c._asjson(indent)}));\n"
	f = sys._getframe(1)
	print(f"Testing UL4ON via V8 ({f.f_code.co_filename}, line {f.f_lineno:,}):")
	print(js)
	with tempfile.NamedTemporaryFile(mode="wb", suffix=".js") as f:
		f.write(js.encode("utf-8"))
		f.flush()
		dir = os.path.expanduser("~/checkouts/LivingLogic.Javascript.ul4")
		cmd = f"d8 {dir}/ul4.js {f.name}"
		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	stdout = result.stdout.decode("utf-8")
	stderr = result.stderr.decode("utf-8")
	# Check if we have an exception
	if result.returncode:
		print(stdout, file=sys.stdout)
		print(stderr, file=sys.stderr)
		raise RuntimeError((stderr or stdout).splitlines()[0])
	output = stdout[:-1] # Drop the "\n"
	print(f"Got result {output!r}")
	return ul4on.loads(output)


def transport_js_v8(obj):
	return _transport_js_v8(obj, indent="")


def transport_js_v8_pretty(obj):
	return _transport_js_v8(obj, indent="\t")


def _transport_js_node(obj, indent):
	"""
	Generate Javascript source that loads the dump done by Python, dumps it
	again, and outputs this dump which is again loaded by Python.

	(this requires an installed ``node`` command from Node
	"""
	dump = ul4on.dumps(obj, indent=indent)
	js = f"""
		const ll = require('{home}/checkouts/LivingLogic.Javascript.ul4/ul4.min');
		const ul4on = ll.ul4on;
		obj = ul4on.loads({ul4c._asjson(dump)});
		console.log(JSON.stringify(ul4on.dumps(obj, {ul4c._asjson(indent)})));
	"""
	f = sys._getframe(1)
	print(f"Testing UL4ON via Node ({f.f_code.co_filename}, line {f.f_lineno:,}):")
	print(js)
	with tempfile.NamedTemporaryFile(mode="wb", suffix=".js") as f:
		f.write(js.encode("utf-8"))
		f.flush()
		dir = os.path.expanduser("~/checkouts/LivingLogic.Javascript.ul4")
		cmd = f"node {f.name}"
		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	stdout = result.stdout.decode("utf-8")
	stderr = result.stderr.decode("utf-8")
	# Check if we have an exception
	if result.returncode:
		print(stdout, file=sys.stdout)
		print(stderr, file=sys.stderr)
		raise RuntimeError((stderr or stdout).splitlines()[0])
	print(f"Got result {stdout!r}")
	return ul4on.loads(json.loads(stdout))


def transport_js_node(obj):
	return _transport_js_node(obj, indent="")


def transport_js_node_pretty(obj):
	return _transport_js_node(obj, indent="\t")


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
	source = f"""
	public class UL4ONTest
	{{
		@SuppressWarnings("unchecked")
		public static void main(String[] args) throws java.io.IOException, java.io.UnsupportedEncodingException, org.antlr.runtime.RecognitionException, ClassNotFoundException
		{{
			// Force the JVM to register the UL4 classes for UL4ON
			Class.forName("com.livinglogic.ul4.InterpretedTemplate");
			{source}
		}}
	}}
	"""

	tempdir = tempfile.mkdtemp()
	stderr = stdout = None
	try:
		source = java_formatsource(source)
		print(source)
		with open(os.path.join(tempdir, "UL4ONTest.java"), "wb") as f:
			f.write(source.encode("utf-8"))
		result = subprocess.run(f"cd {tempdir}; javac -encoding utf-8 UL4ONTest.java", stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		if result.returncode:
			stderr = result.stderr.decode("utf-8")
			print(stderr, file=sys.stderr)
			raise RuntimeError(stderr.splitlines()[0])
		result = subprocess.run(f"cd {tempdir}; java UL4ONTest", stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
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

	f = sys._getframe(1)
	print(f"Testing UL4ON via Java ({f.f_code.co_filename}, line {f.f_lineno}):")

	dump = ul4on.dumps(obj, indent=indent)
	code = f"""
	String input = {misc.javaexpr(dump)};
	Object object = com.livinglogic.ul4on.Utils.loads(input, null);
	String output = com.livinglogic.ul4on.Utils.dumps(object, {misc.javaexpr(indent)});
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	output = java_runsource(code)
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
	("js_node", transport_js_node),
	("js_node_pretty", transport_js_node_pretty),
	("java", transport_java),
	("java_pretty", transport_java_pretty),
]


def pytest_generate_tests(metafunc):
	if "t" in metafunc.funcargnames:
		metafunc.parametrize("t", [t for (id, t) in all_transports], ids=[id for (id, t) in all_transports])
	if "oracle" in metafunc.funcargnames:
		metafunc.parametrize("oracle", [oracle for (id, oracle) in all_oracles], ids=[id for (id, oracle) in all_oracles])


def test_none(t):
	assert None is t(None)


def test_bool(t):
	assert False is t(False)
	assert True is t(True)


def test_int(t):
	assert 42 == t(42)
	assert -42 == t(-42)


def test_float(t):
	assert -42.5 == t(-42.5)
	if t not in (transport_js_v8, transport_js_v8_pretty, transport_js_node, transport_js_node_pretty):
		assert 1e42 == t(1e42)
	assert math.pi == t(math.pi)


def test_string(t):
	assert "gurk" == t("gurk")

	# This should make sure that all characters roundtrip properly
	# (except maybe those outside the BMP, as JS and Java don't support them properly)
	chars = "".join(chr(c) for c in range(0x1000))
	assert chars == t(chars)


def test_color(t):
	c = color.Color(0x66, 0x99, 0xcc, 0xff)
	assert c == t(c)


def test_date(t):
	expected = datetime.date(2012, 10, 29)
	got = t(expected)
	assert isinstance(got, datetime.date) and not isinstance(got, datetime.datetime)
	assert expected == got


def test_datetime(t):
	expected = datetime.datetime(2012, 10, 29)
	got = t(expected)
	assert isinstance(got, datetime.datetime)
	assert expected == got

	expected = datetime.datetime(2012, 10, 29, 16, 44, 55, 987000)
	got = t(expected)
	assert isinstance(got, datetime.datetime)
	assert expected == got


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


def test_ordereddict(t):
	if t not in (transport_js_v8, transport_js_v8_pretty):
		d = {}
		assert d == t(d)

		assert isinstance(t(d), dict)

		d = {"gurk": "hurz"}
		assert d == t(d)

		d1 = {}
		d1[1] = 'one'
		d1[2] = 'two'
		assert d1 == t(d1)
		assert list(t(d1)) == [1, 2]

		d2 = {}
		d2[2] = 'two'
		d2[1] = 'one'
		assert t(d1) == t(d2)


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


def test_template_from_source():
	t = ul4on.loads("o s'de.livinglogic.ul4.template' n s'test' s'<?print x + y?>' s'x, y=23' s'keep' n n )")

	assert t.name == "test"
	assert t.source == "<?ul4 test(x, y=23)?><?print x + y?>"
	assert t.whitespace == "keep"
	assert t.startdelim == "<?"
	assert t.enddelim == "?>"
	assert t.renders(17) == "40"


def test_recursion(t):
	if t not in (transport_js_v8, transport_js_v8_pretty, transport_js_node, transport_js_node_pretty):
		l1 = []
		l1.append(l1)

		l2 = t(l1)
		assert len(l2) == 1
		assert l2[0] is l2


def test_custom_class(t):
	if t in (transport_python, transport_python_pretty):
		@ul4on.register("de.livinglogic.ul4.test.point")
		class Point:
			def __init__(self, x=None, y=None):
				self.x = x
				self.y = y

			def ul4ondump(self, encoder):
				encoder.dump(self.x)
				encoder.dump(self.y)

			def ul4onload(self, decoder):
				self.x = decoder.load()
				self.y = decoder.load()

		p = t(Point(17, 23))
		assert p.x == 17
		assert p.y == 23
		assert isinstance(p, Point)

		class Point2(Point):
			pass

		p = t(Point(17, 23), registry={"de.livinglogic.ul4.test.point": Point2})
		assert p.x == 17
		assert p.y == 23
		assert isinstance(p, Point2)

		@ul4on.register("de.livinglogic.ul4.test.pointcontent")
		class PointContent:
			def __init__(self, x=None, y=None):
				self.x = x
				self.y = y

			def ul4ondump(self, encoder):
				if self.x != 0:
					encoder.dump(self.x)
					if self.y != 0:
						encoder.dump(self.y)

			def ul4onload(self, decoder):
				i = -1
				for (i, item) in enumerate(decoder.loadcontent()):
					if i == 0:
						self.x = item
					elif i == 1:
						self.y = item
				if i < 1:
					self.y = 0
					if i < 0:
						self.x = 0

		p = t(PointContent(17, 23))
		assert p.x == 17
		assert p.y == 23
		assert isinstance(p, PointContent)

		p = t(PointContent(17, 0))
		assert p.x == 17
		assert p.y == 0
		assert isinstance(p, PointContent)

		p = t(PointContent(0, 0))
		assert p.x == 0
		assert p.y == 0
		assert isinstance(p, PointContent)


@pytest.mark.db
def test_oracle_none(oracle):
	if oracle:
		assert None is oracle(f"{oracle.pkg}.none(c_out);")


@pytest.mark.db
def test_oracle_bool(oracle):
	if oracle:
		assert None is oracle(f"{oracle.pkg}.bool(c_out, null);")
		assert False is oracle(f"{oracle.pkg}.bool(c_out, 0);")
		assert True is oracle(f"{oracle.pkg}.bool(c_out, 1);")


@pytest.mark.db
def test_oracle_int(oracle):
	if oracle:
		assert None is oracle(f"{oracle.pkg}.int(c_out, null);")
		assert 42 == oracle(f"{oracle.pkg}.int(c_out, 42);")
		assert 0 == oracle(f"{oracle.pkg}.int(c_out, 0);")
		assert -42 == oracle(f"{oracle.pkg}.int(c_out, -42);")


@pytest.mark.db
def test_oracle_float(oracle):
	if oracle:
		assert None is oracle(f"{oracle.pkg}.float(c_out, null);")
		assert 42.5 == oracle(f"{oracle.pkg}.float(c_out, 42.5);")
		assert 0.0 == oracle(f"{oracle.pkg}.float(c_out, 0);")
		assert -42.5 == oracle(f"{oracle.pkg}.float(c_out, -42.5);")


@pytest.mark.db
def test_oracle_str(oracle):
	if oracle:
		assert "foo" == oracle(f"{oracle.pkg}.str(c_out, 'foo');")
		assert "\x00\a\b\t\n\r\x1b" == oracle(f"{oracle.pkg}.str(c_out, chr(0) || chr(7) || chr(8) || chr(9) || chr(10) || chr(13) || chr(27));")
		assert "\xa0äöüÄÖÜß€" == oracle(f"{oracle.pkg}.str(c_out, '\xa0äöüÄÖÜß\u20ac');")
		assert "foo" == oracle(f"{oracle.pkg}.str(c_out, to_clob('foo'));")

		# Check every BMP character (in blocks of 64)
		size = 0x40
		for offset in range(0, 0x1000, size):
			chars = "".join(chr(c) for c in range(offset, offset + size))

			oraclechars = "".join(f"\\{ord(c):04x}" for c in chars)
			oraclechars = f"unistr('{oraclechars}')"

			assert chars == oracle(f"{oracle.pkg}.str(c_out, {oraclechars});")


@pytest.mark.db
def test_oracle_color(oracle):
	if oracle:
		expected = color.Color(0x66, 0x99, 0xcc, 0xff)
		got = oracle(f"{oracle.pkg}.color(c_out, 102, 153, 204, 255);")
		assert expected == got


@pytest.mark.db
def test_oracle_date(oracle):
	if oracle:
		expected = datetime.date(2014, 11, 6)
		got = oracle(f"{oracle.pkg}.date_(c_out, to_date('2014-11-06', 'YYYY-MM-DD'));")
		assert expected == got


@pytest.mark.db
def test_oracle_datetime(oracle):
	if oracle:
		expected = datetime.datetime(2014, 11, 6, 12, 34, 56)
		got = oracle(f"{oracle.pkg}.datetime(c_out, to_date('2014-11-06 12:34:56', 'YYYY-MM-DD HH24:MI:SS'));")
		assert expected == got

		expected = datetime.datetime(2014, 11, 6, 12, 34, 56, 987654)
		got = oracle(f"{oracle.pkg}.datetime(c_out, to_timestamp('2014-11-06 12:34:56,987654', 'YYYY-MM-DD HH24:MI:SS,FF6'));")
		assert expected == got


@pytest.mark.db
def test_oracle_timedelta(oracle):
	if oracle:
		expected = datetime.timedelta(days=42)
		got = oracle(f"{oracle.pkg}.timedelta(c_out, 42);")
		assert expected == got

		expected = datetime.timedelta(days=1, seconds=2, microseconds=3)
		got = oracle(f"{oracle.pkg}.timedelta(c_out, 1, 2, 3);")
		assert expected == got


@pytest.mark.db
def test_oracle_monthdelta(oracle):
	if oracle:
		expected = misc.monthdelta(42)
		got = oracle(f"{oracle.pkg}.monthdelta(c_out, 42);")
		assert expected == got

		expected = misc.monthdelta(-42)
		got = oracle(f"{oracle.pkg}.monthdelta(c_out, -42);")
		assert expected == got


@pytest.mark.db
def test_oracle_slice(oracle):
	if oracle:
		expected = slice(None, None)
		got = oracle(f"{oracle.pkg}.slice(c_out, null, null);")
		assert expected == got

		expected = slice(1, None)
		got = oracle(f"{oracle.pkg}.slice(c_out, 1, null);")
		assert expected == got

		expected = slice(None, 3)
		got = oracle(f"{oracle.pkg}.slice(c_out, null, 3);")
		assert expected == got

		expected = slice(1, 3)
		got = oracle(f"{oracle.pkg}.slice(c_out, 1, 3);")
		assert expected == got


@pytest.mark.db
def test_oracle_list(oracle):
	if oracle:
		expected = []
		got = oracle(f"""
			{oracle.pkg}.beginlist(c_out);
			{oracle.pkg}.endlist(c_out);
		""")
		assert expected == got

		expected = [None, 42, "foo"]
		got = oracle(f"""
			{oracle.pkg}.beginlist(c_out);
				{oracle.pkg}.none(c_out);
				{oracle.pkg}.int(c_out, 42);
				{oracle.pkg}.str(c_out, 'foo');
			{oracle.pkg}.endlist(c_out);
		""")
		assert expected == got


@pytest.mark.db
def test_oracle_set(oracle):
	if oracle:
		expected = set()
		got = oracle(f"""
			{oracle.pkg}.beginset(c_out);
			{oracle.pkg}.endset(c_out);
		""")
		assert expected == got

		expected = {None, 42, "foo"}
		got = oracle(f"""
			{oracle.pkg}.beginset(c_out);
				{oracle.pkg}.none(c_out);
				{oracle.pkg}.int(c_out, 42);
				{oracle.pkg}.str(c_out, 'foo');
			{oracle.pkg}.endset(c_out);
		""")
		assert expected == got


@pytest.mark.db
def test_oracle_dict(oracle):
	if oracle:
		expected = {}
		got = oracle(f"""
			{oracle.pkg}.begindict(c_out);
			{oracle.pkg}.enddict(c_out);
		""")
		assert expected == got

		expected = {"foo": None, "bar": 42, 42: [1, 2, 3]}
		got = oracle(f"""
			{oracle.pkg}.begindict(c_out);
				{oracle.pkg}.keynone(c_out, 'foo');
				{oracle.pkg}.keyint(c_out, 'bar', 42);
				{oracle.pkg}.int(c_out, 42);
				{oracle.pkg}.beginlist(c_out);
					{oracle.pkg}.int(c_out, 1);
					{oracle.pkg}.int(c_out, 2);
					{oracle.pkg}.int(c_out, 3);
				{oracle.pkg}.endlist(c_out);
			{oracle.pkg}.enddict(c_out);
		""")
		assert expected == got


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

		p = oracle(f"""
			{oracle.pkg}.beginobject(c_out, 'de.livinglogic.xist.ul4on.test.person');
				{oracle.pkg}.str(c_out, 'Otto');
				{oracle.pkg}.str(c_out, 'Normalverbraucher');
			{oracle.pkg}.endobject(c_out);
		""")

		assert isinstance(p, Person)
		assert p.firstname == "Otto"
		assert p.lastname == "Normalverbraucher"
