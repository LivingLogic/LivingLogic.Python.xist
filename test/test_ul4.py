#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2009-2022 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2022 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import sys, os, re, io, tempfile, subprocess, codecs, datetime, math
from collections import abc

import pytest

from ll import ul4c, color, misc, ul4on
from ll.xist.ns import html, ul4


home = os.environ["HOME"]


def passbytes(exc):
	if isinstance(exc, UnicodeDecodeError):
		return (exc.object[exc.start:exc.end].decode("iso-8859-1"), exc.end)
	else:
		raise TypeError(f"don't know how to handle {exc!r}")


codecs.register_error("passbytes", passbytes)


class Point:
	ul4_attrs = {"x", "y"}

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def ul4_getattr(self, name):
		return getattr(self, name)

	def ul4_setattr(self, name, value):
		if name == "x":
			if isinstance(value, int):
				self.x = value
			else:
				raise TypeError("attribute x must be of type int!")
		elif name == "y":
			raise TypeError(r"readonly attribute {name!r}")
		else:
			raise AttributeError(name)


class PseudoDict(abc.Mapping):
	def __init__(self, dict):
		self.dict = dict

	def __getitem__(self, key):
		return self.dict[key]

	def __iter__(self):
		return iter(self.dict)

	def __len__(self):
		return len(self.dict)


class PseudoList(abc.Sequence):
	def __init__(self, list):
		self.list = list

	def __getitem__(self, index):
		return self.list[index]

	def __len__(self):
		return len(self.list)


class TemplatePython:
	def __init__(self, source, name=None, whitespace="keep", signature=None):
		self.source = source
		self.name = name
		self.whitespace = whitespace
		self.signature = signature
		self.template = self.maketemplate()

	def maketemplate(self):
		return ul4c.Template(self.source, name=self.name, whitespace=self.whitespace, signature=self.signature)

	def render(self, *args, **kwargs):
		return "".join(self.template.render(*args, **kwargs))

	def renders(self, *args, **kwargs):
		return self.template.renders(*args, **kwargs)

	def __call__(self, *args, **kwargs):
		return self.template(*args, **kwargs)

	def render_with_globals(self, args, kwargs, globals):
		return "".join(self.template.render_with_globals(args, kwargs, globals))

	def renders_with_globals(self, args, kwargs, globals):
		return self.template.renders_with_globals(args, kwargs, globals)

	def call_with_globals(self, args, kwargs, globals):
		return self.template.call_with_globals(args, kwargs, globals)


class TemplatePythonDumpS(TemplatePython):
	def maketemplate(self):
		template = ul4c.Template(self.source, name=self.name, whitespace=self.whitespace, signature=self.signature)
		template = ul4c.Template.loads(template.dumps()) # Recreate the template from the binary dump
		return template


class TemplatePythonDump(TemplatePython):
	def maketemplate(self):
		template = ul4c.Template(self.source, name=self.name, whitespace=self.whitespace, signature=self.signature)
		stream = io.StringIO()
		template.dump(stream)
		stream.seek(0)
		template = ul4c.Template.load(stream) # Recreate the template from the stream
		return template


class TemplateJava:
	def __init__(self, source, name=None, whitespace="keep", signature=None):
		self.source = source
		self.name = name
		self.whitespace = whitespace
		self.signature = signature

	def findexception(self, output):
		lines = output.splitlines()
		msg = None
		exc = None
		lastexc = None
		for line in lines:
			prefix1 = 'Exception in thread "main"'
			prefix2 = "Caused by:"
			prefix3 = "Suppressed:"
			if line.startswith(prefix1):
				msg = line[len(prefix1):].strip()
			elif line.startswith(prefix2):
				msg = line[len(prefix2):].strip()
			elif line.lstrip().startswith(prefix3):
				msg = line.lstrip()[len(prefix3):].strip()
			else:
				continue
			newexc = RuntimeError(msg)
			newexc.__cause__ = lastexc
			lastexc = newexc
			if exc is None:
				exc = newexc
		if exc is not None:
			print(output, file=sys.stderr)
			raise exc

	def run(self, data):
		dump = ul4on.dumps(data).encode("utf-8")
		result = subprocess.run("java com.livinglogic.ul4.Tester", input=dump, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		# Check if we have an exception
		self.findexception(result.stderr.decode("utf-8", "passbytes"))
		return result.stdout.decode("utf-8", "passbytes")

	def renders(self, *args, **kwargs):
		data = self._makedata("renders", args, kwargs)
		return self.run(data)

	def render(self, *args, **kwargs):
		data = self._makedata("render", args, kwargs)
		return self.run(data)

	def __call__(self, *args, **kwargs):
		data = self._makedata("call", args, kwargs)
		return ul4on.loads(self.run(data))

	def render_with_globals(self, args, kwargs, globals):
		data = self._makedata("render", args, kwargs, globals)
		return self.run(data)

	def renders_with_globals(self, args, kwargs, globals):
		data = self._makedata("renders", args, kwargs, globals)
		return self.run(data)

	def call_with_globals(self, args, kwargs, globals):
		data = self._makedata("call", args, kwargs, globals)
		return ul4on.loads(self.run(data))


class TemplateJavaCompiledByPython(TemplateJava):
	def template(self):
		return ul4c.Template(self.source, name=self.name, whitespace=self.whitespace, signature=self.signature)

	def _makedata(self, command, args, kwargs, globals=None):
		if args:
			raise ValueError("positional arguments not supported")
		return dict(
			command=command,
			template=self.template(),
			name=None,
			whitespace=None,
			signature=None,
			variables=kwargs,
			globalvariables=globals,
		)


class TemplateJavaCompiledByJava(TemplateJava):
	def _makedata(self, command, args, kwargs, globals=None):
		if args:
			raise ValueError("positional arguments not supported")
		return dict(
			command=command,
			template=self.source,
			name=self.name,
			whitespace=self.whitespace,
			signature=self.signature,
			variables=kwargs,
			globalvariables=globals,
		)


class TemplatePHP:
	def __init__(self, source, name=None, whitespace="keep", signature=None):
		self.source = source
		self.name = name
		self.whitespace = whitespace
		self.signature = signature
		self.template = self.maketemplate()

	def maketemplate(self):
		return ul4c.Template(self.source, name=self.name, whitespace=self.whitespace, signature=self.signature)

	def phpexpr(self, obj):
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
					c = f'\\x{ord(c):02x}'
				v.append(c)
			v.append('"')
			return "".join(v)
		elif isinstance(obj, datetime.datetime):
			return rf"\com\livinglogic\ul4\Utils::date({obj.year}, {obj.month}, {obj.day}, {obj.hour}, {obj.minute}, {obj.second}, {obj.microsecond})"
		elif isinstance(obj, datetime.date):
			return rf"\com\livinglogic\ul4\Utils::date({obj.year}, {obj.month}, {obj.day})"
		elif isinstance(obj, datetime.timedelta):
			return rf"new \com\livinglogic\ul4\TimeDelta({obj.days}, {obj.seconds}, {obj.microseconds})"
		elif isinstance(obj, misc.monthdelta):
			return rf"new \com\livinglogic\ul4\MonthDelta({obj.months})"
		elif isinstance(obj, color.Color):
			return rf"new \com\livinglogic\ul4\Color({obj.r()}, {obj.g()}, {obj.b()}, {obj.a()})"
		elif isinstance(obj, ul4c.Template):
			return rf"\com\livinglogic\ul4\Template::loads({self.phpexpr(obj.dumps())})"
		elif isinstance(obj, abc.Mapping):
			items = ", ".join(f"{self.phpexpr(key)} => {self.phpexpr(value)}" for (key, value) in obj.items())
			return f"array({items})"
		elif isinstance(obj, abc.Sequence):
			items = ", ".join(self.phpexpr(item) for item in obj)
			return f"array({items})"
		else:
			raise ValueError(f"Can't convert {obj!r} to PHP")

	def runcode(self, source):
		f = sys._getframe(2)
		print(f"Rendering UL4 template ({f.f_code.co_filename}, line {f.f_lineno:,}):")
		print(source)
		with tempfile.NamedTemporaryFile(mode="wb", suffix=".php") as f:
			f.write(source.encode("utf-8"))
			f.flush()
			dir = os.path.expanduser("~/checkouts/LivingLogic.PHP.ul4")
			result = subprocess.run(f"php -n -d include_path={dir} -d date.timezone=Europe/Berlin {f.name}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout = result.stdout.decode("utf-8", "passbytes")
		stderr = result.stderr.decode("utf-8", "passbytes")
		# Check if we have an exception
		if result.returncode:
			print(stdout, file=sys.stdout)
			print(stderr, file=sys.stderr)
			raise RuntimeError((stderr or stdout).strip().splitlines()[0])
		return stdout

	def renders(self, *args, **kwargs):
		if args:
			raise ValueError("*args not supported")

		source = f"""<?php
		include_once 'com/livinglogic/ul4/ul4.php';
		$template = \\com\\livinglogic\\ul4\\Template::loads({self.phpexpr(self.template.dumps())});
		$variables = {self.phpexpr(kwargs)};
		print $template->renders($variables);
		?>"""
		return self.runcode(source)

	def render(self, *args, **kwargs):
		return self.renders(*args, **kwargs)

	def __call__(self, *args, **kwargs):
		if args:
			raise ValueError("*args not supported")

		source = f"""<?php
		include_once 'com/livinglogic/ul4/ul4.php';
		$template = \\com\\livinglogic\\ul4\\Template::loads({self.phpexpr(self.template.dumps())});
		$variables = {self.phpexpr(kwargs)};
		print $template->call($variables);
		?>"""
		return self.runcode(source)


class TemplateJavascript:
	def __init__(self, source, name=None, whitespace="keep", signature=None):
		self.source = source
		self.name = name
		self.whitespace = whitespace
		self.signature = signature
		self.template = self.maketemplate()

	def maketemplate(self):
		return ul4c.Template(self.source, name=self.name, whitespace=self.whitespace, signature=self.signature)

	def runcode(self, command, source):
		f = sys._getframe(2)
		print(f"Rendering UL4 template ({f.f_code.co_filename}, line {f.f_lineno:,}):")
		print(source)
		with tempfile.NamedTemporaryFile(mode="wb", suffix=".js") as f:
			f.write(source.encode("utf-8"))
			f.flush()
			dir = os.path.expanduser("~/checkouts/LivingLogic.Javascript.ul4")
			cmd = command.format(cmd=command, dir=dir, fn=f.name)
			result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout = result.stdout.decode("utf-8", "passbytes")
		stderr = result.stderr.decode("utf-8", "passbytes")
		print(repr(stdout))
		print(repr(stderr))
		if stderr:
			raise RuntimeError(stderr)
		data = ul4on.loads(stdout)
		# Check if we had an exception
		if data["status"] == "error":
			raise RuntimeError(data["result"])
		else:
			return data["result"]


class TemplateJavascriptV8(TemplateJavascript):
	def _make_source(self, command, args, kwargs, globals={}):
		if args:
			raise ValueError("positional arguments not supported")

		return f"""
			var template = {self.template.jssource()};
			var vars = ul4._map2object(ul4.loads({ul4c._asjson(ul4on.dumps(kwargs))}));
			var globals = ul4._map2object(ul4.loads({ul4c._asjson(ul4on.dumps(globals))}));
			try
			{{
				print(ul4.dumps({{"status": "ok", "result": {command}}}));
			}}
			catch (exc)
			{{
				print(ul4.dumps({{"status": "error", "result": ul4._stacktrace(exc)}}));
			}}
		"""

	def renders(self, *args, **kwargs):
		source = self._make_source("template.renders(vars, {})", args, kwargs)
		return self.runcode("d8 --stack_size=100 {dir}/dist/umd/ul4.js {fn}", source)

	def render(self, *args, **kwargs):
		return self.renders(*args, **kwargs)

	def __call__(self, *args, **kwargs):
		source = self._make_source("template.call(vars, {})", args, kwargs)
		return self.runcode("d8 {dir}/dist/umd/ul4.js {fn}", source)

	def renders_with_globals(self, args, kwargs, globals):
		source = self._make_source("template.renders(vars, globals)", args, kwargs, globals)
		return self.runcode("d8 --stack_size=100 {dir}/dist/umd/ul4.js {fn}", source)

	def render_with_globals(self, args, kwargs, globals):
		return self.renders_with_globals(args, kwargs, globals)

	def call_with_globals(self, args, kwargs, globals):
		source = self._make_source("template.call(vars, globals)", args, kwargs, globals)
		return self.runcode("d8 {dir}/dist/umd/ul4.js {fn}", source)


class TemplateJavascriptNode(TemplateJavascript):
	def _make_source(self, command, args, kwargs, globals={}):
		if args:
			raise ValueError("positional arguments not supported")

		return f"""
			const ul4 = require('{home}/checkouts/LivingLogic.Javascript.ul4/dist/umd/ul4');

			var template = {self.template.jssource()};
			var vars = ul4._map2object(ul4.loads({ul4c._asjson(ul4on.dumps(kwargs))}));
			var globals = ul4._map2object(ul4.loads({ul4c._asjson(ul4on.dumps(globals))}));
			try
			{{
				console.log(ul4.dumps({{"status": "ok", "result": {command}}}));
			}}
			catch (exc)
			{{
				console.log(ul4.dumps({{"status": "error", "result": ul4._stacktrace(exc)}}));
			}}
		"""

	def renders(self, *args, **kwargs):
		source = self._make_source("template.renders(vars, {})", args, kwargs)
		return self.runcode("node {fn}", source)

	def render(self, *args, **kwargs):
		return self.renders(*args, **kwargs)

	def __call__(self, *args, **kwargs):
		source = self._make_source("template.call(vars, {})", args, kwargs)
		return self.runcode("node {fn}", source)

	def renders_with_globals(self, args, kwargs, globals):
		source = self._make_source("template.renders(vars, globals)", args, kwargs, globals)
		return self.runcode("node {fn}", source)

	def render_with_globals(self, args, kwargs, globals):
		return self.renders_with_globals(args, kwargs, globals)

	def call_with_globals(self, args, kwargs, globals):
		source = self._make_source("template.call(vars, globals)", args, kwargs, globals)
		return self.runcode("node {fn}", source)


template_params = [
	pytest.param("python", marks=pytest.mark.python),
	pytest.param("python_dumps", marks=pytest.mark.python),
	pytest.param("python_dump", marks=pytest.mark.python),
	pytest.param("java_compiled_by_python", marks=pytest.mark.java),
	pytest.param("java_compiled_by_java", marks=pytest.mark.java),
	pytest.param("js_v8", marks=pytest.mark.js),
	pytest.param("js_node", marks=pytest.mark.js),
	# pytest.param("php", marks=pytest.mark.php),
]

all_templates = dict(
	python=TemplatePython,
	python_dumps=TemplatePythonDumpS,
	python_dump=TemplatePythonDump,
	java_compiled_by_python=TemplateJavaCompiledByPython,
	java_compiled_by_java=TemplateJavaCompiledByJava,
	js_v8=TemplateJavascriptV8,
	js_node=TemplateJavascriptNode,
	php=TemplatePHP,
)

@pytest.fixture(scope="module", params=template_params)
def T(request):
	"""
	A parameterized fixture that returns each of the testing classes
	:class:`TemplatePython`, :class:`TemplatePythonDumpS`,
	:class:`TemplatePythonDump`, :class:`TemplateJavaCompiledByPython`,
	:class:`TemplateJavaCompiledByJava`, :class:`TemplateJavascriptV8`,
	:class:`TemplateJavascriptNode` and :class:`TemplatePHP`.

	Each of these classes has methods :meth:`render`, :meth:`renders` and
	:meth:`__call__` to render/call the template with the appropriate backend.
	"""
	return all_templates[request.param]


def pytest_generate_tests(metafunc):
	if "reprfunc" in metafunc.fixturenames:
		values = ["repr", "ascii"]
		metafunc.parametrize("reprfunc", values, ids=values)


def _make_exception_re(*args):
	return "({})".format("|".join(args))


argumentmismatchmessage = _make_exception_re(
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
	"takes no keyword arguments",
	"expected at least \\d+ arguments?",
	"expected at most \\d+ arguments?, got \\d+",
	"missing \\d+ required positional arguments?", # 3.3
	"missing required argument",
	"takes \\d+ positional arguments? but \\d+ (was|were) given", # 3.3
	"takes from \\d+ to \\d+ positional arguments but \\d+ (was|were) given", # 3.3
	"takes at least \\d+ positional arguments? \\(\\d+ given\\)",
	"missing a required argument: .\\w+.",
	# Javascript argument mismatch exception messages
	"\\w+\\(\\) takes at most \\d+ positional arguments?, \\d+ given",
	"requires (at least \\d+|\\d+(-\\d+)?) arguments?, \\d+ given",
	"[rR]equired \\w+\\(\\) argument \\w+ \\(position \\d+\\) missing",
	"[rR]equired \\w+\\(\\) argument missing",
	"doesn't support an argument named \\w+",
	"\\w+\\(\\) doesn't support an argument named .\\w+.",
	# Java exception classes for argument mismatches
	"com.livinglogic.ul4.TooManyArgumentsException",
	"com.livinglogic.ul4.MissingArgumentException",
	"com.livinglogic.ul4.ArgumentCountMismatchException",
	"com.livinglogic.ul4.UnsupportedArgumentNameException",
	"com.livinglogic.ul4.KeywordArgumentsNotSupportedException",
)

unorderabletypesmessage = _make_exception_re(
	# Python 3.6
	"not supported between instances of",
	# Python < 3.6 and Javascript
	"unorderable types",
	# Java
	"com.livinglogic.ul4.UnorderableTypesException",
)

duplicatekeywordargument = _make_exception_re(
	# Python
	"multiple values for keyword argument",
	"duplicate keyword argument",
	"keyword argument repeated",
	# Java
	"com.livinglogic.ul4.DuplicateArgumentException",
)

unknownkeywordargument = _make_exception_re(
	# Python
	"got an unexpected keyword argument",
	"[a-zA-Z_][a-zA-Z0-9_]*\\(\\) doesn't support an argument named '[a-zA-Z_][a-zA-Z0-9_]*'",
	"an argument named [a-zA-Z_][a-zA-Z0-9_]* isn't supported",
	"too many keyword arguments",
	"takes no keyword arguments",
	"got some positional-only arguments passed as keyword arguments",
	"'[a-zA-Z_][a-zA-Z0-9_]*' is an invalid keyword argument for [a-zA-Z_][a-zA-Z0-9_]*\\(\\)",
)

missingkeywordargument = _make_exception_re(
	# Python
	"required \\w+\\(\\) argument .\\w+. \\(position \\d+\\) missing",
	"missing a required argument",
	# Java
	"com.livinglogic.ul4.MissingArgumentException",
)

subscriptablemessage = _make_exception_re(
	# Python
	"object is not subscriptable",
	"object does not support item assignment",
	# Java
	"com.livinglogic.ul4.ArgumentTypeMismatchException: <[\\w\\d.]+>\\[<[\\w\\d.]+>\\] not supported"
)

indexmessage = _make_exception_re(
	# Python
	"index out of range",
	# Javascript
	"index -?\\d+ out of range",
	# Java
	"IndexOutOfBoundsException"
)


zerodivisionmessage = _make_exception_re(
	# Python
	"division or modulo by zero",
	# Python/Java/Javascript
	"division by zero",
	# Java
	"/ by zero",
)


class raises:
	def __init__(self, msg):
		self._msg = msg
		self.msg = re.compile(msg)

	def __enter__(self):
		pass

	def __exit__(self, type, value, traceback):
		if value is None:
			pytest.fail("failed to raise exception")
		# Check that any exception in the exception chain of the raised one matches a regexp
		exceptionmsgs = [misc.format_exception(exc) for exc in misc.exception_chain(value)]
		if not any(self.msg.search(msg) is not None for msg in exceptionmsgs):
			pytest.fail(f"failed to find expected exception message {self._msg!r} in exception {misc.format_exception(value)}")
		return True # Don't propagate exception


@pytest.mark.ul4
def test_text(T):
	assert 'gurk' == T('gurk').renders()
	assert 'g\xfcrk' ==  T('g\xfcrk').renders()
	assert 'gurk' == T('gurk', whitespace="strip").renders()
	assert 'g\tu rk' == T('g\t\n\t u \n  r\n\t\tk', whitespace="strip").renders()


@pytest.mark.ul4
def test_linefeed_in_code(T):
	assert "40" == T("<?print\na\n+\nb\n?>").renders(a=17, b=23)


@pytest.mark.ul4
def test_whitespace_before_tag(T):
	assert "42" == T("<? print 42 ?>").renders()


@pytest.mark.ul4
def test_undefined(T):
	assert '' == T('<?print Undefined?>').renders()
	assert 'no' == T('<?if Undefined?>yes<?else?>no<?end if?>').renders()


@pytest.mark.ul4
def test_none(T):
	assert '' == T('<?print None?>').renders()
	assert 'no' == T('<?if None?>yes<?else?>no<?end if?>').renders()


@pytest.mark.ul4
def test_false(T):
	assert 'False' == T('<?print False?>').renders()
	assert 'no' == T('<?if False?>yes<?else?>no<?end if?>').renders()


@pytest.mark.ul4
def test_true(T):
	assert 'True' == T('<?print True?>').renders()
	assert 'yes' == T('<?if True?>yes<?else?>no<?end if?>').renders()


@pytest.mark.ul4
def test_int(T):
	values = (0, 42, -42, 0x7ffffff, 0x8000000, -0x8000000, -0x8000001)
	if T not in (TemplateJavascriptV8, TemplateJavascriptNode, TemplatePHP):
		# Since Javascript has no real integers the following would lead to rounding errors
		# And PHP doesn't have any support for big integers (except for some GMP wrappers, that may not be installed)
		values += (0x7ffffffffffffff, 0x800000000000000, -0x800000000000000, -0x800000000000001, 9999999999, -9999999999, 99999999999999999999, -99999999999999999999)
	for value in values:
		assert str(value) == T(f'<?print {value}?>').renders()
	assert '255' == T('<?print 0xff?>').renders()
	assert '255' == T('<?print 0Xff?>').renders()
	assert '-255' == T('<?print -0xff?>').renders()
	assert '-255' == T('<?print -0Xff?>').renders()
	assert '63' == T('<?print 0o77?>').renders()
	assert '63' == T('<?print 0O77?>').renders()
	assert '-63' == T('<?print -0o77?>').renders()
	assert '-63' == T('<?print -0O77?>').renders()
	assert '7' == T('<?print 0b111?>').renders()
	assert '7' == T('<?print 0B111?>').renders()
	assert '-7' == T('<?print -0b111?>').renders()
	assert '-7' == T('<?print -0B111?>').renders()

	assert 'no' == T('<?if 0?>yes<?else?>no<?end if?>').renders()
	assert 'yes' == T('<?if 1?>yes<?else?>no<?end if?>').renders()
	assert 'yes' == T('<?if -1?>yes<?else?>no<?end if?>').renders()


@pytest.mark.ul4
def test_float(T):
	# str() output might differ slightly between Python and JS, so eval the output again for tests
	assert 0.0 == eval(T('<?print 0.?>').renders())
	assert 42.0 == eval(T('<?print 42.?>').renders())
	assert -42.0 == eval(T('<?print -42.?>').renders())
	assert -42.5 == eval(T('<?print -42.5?>').renders())
	assert 1e42 == eval(T('<?print 1E42?>').renders())
	assert 1e42 == eval(T('<?print 1e42?>').renders())
	assert -1e42 == eval(T('<?print -1E42?>').renders())
	assert -1e42 == eval(T('<?print -1e42?>').renders())

	assert 'no' == T('<?if 0.?>yes<?else?>no<?end if?>').renders()
	assert 'yes' == T('<?if 1.?>yes<?else?>no<?end if?>').renders()
	assert 'yes' == T('<?if -1.?>yes<?else?>no<?end if?>').renders()


@pytest.mark.ul4
def test_string(T):
	assert 'foo' == T('<?print "foo"?>').renders()
	assert '\n' == T('<?print "\\n"?>').renders()
	assert '\r' == T('<?print "\\r"?>').renders()
	assert '\t' == T('<?print "\\t"?>').renders()
	assert '\f' == T('<?print "\\f"?>').renders()
	assert '\b' == T('<?print "\\b"?>').renders()
	assert '\a' == T('<?print "\\a"?>').renders()
	assert '\x00' == T('<?print "\\x00"?>').renders()
	assert '"' == T('<?print "\\""?>').renders()
	assert "'" == T('<?print "\\\'"?>').renders()
	assert '\u20ac' == T('<?print "\u20ac"?>').renders()
	assert '\xff' == T('<?print "\\xff"?>').renders()
	assert '\u20ac' == T('''<?print "\\u20ac"?>''').renders()
	for c in "\x00\x80\u0100\u3042\n\r\t\f\b\a\"":
		assert c == T('<?print obj?>').renders(obj=c) # This tests :func:`misc.javaexpr` for Java and :func:`ul4c._asjson` for JS

	# Test literal control characters (but '\r' and '\n' are not allowed)
	assert 'gu\trk' == T("<?print 'gu\trk'?>").renders()
	assert 'gu\t\\rk' == T(r"<?print 'gu\t\\rk'?>").renders()

	# Test triple quoted strings
	assert 'gu\r\nrk' == T("<?print '''gu\r\nrk'''?>").renders()
	assert 'gu\r\nrk' == T('<?print """gu\r\nrk"""?>').renders()

	assert 'no' == T('<?if ""?>yes<?else?>no<?end if?>').renders()
	assert 'yes' == T('<?if "foo"?>yes<?else?>no<?end if?>').renders()

	with raises("Unterminated string|mismatched character|MismatchedTokenException|NoViableAltException|SyntaxException"):
		T('<?print "?>').renders()


@pytest.mark.ul4
def test_date(T):
	assert 'yes' == T('<?if @(2000-02-29)?>yes<?else?>no<?end if?>').renders()


@pytest.mark.ul4
def test_datetime(T):
	if issubclass(T, (TemplatePHP, TemplateJavascript)):
		assert '2000-02-29T12:34:56.987000' == T('<?print @(2000-02-29T12:34:56.987000).isoformat()?>').renders() # JS only supports milliseconds
	else:
		assert '2000-02-29T12:34:56.987654' == T('<?print @(2000-02-29T12:34:56.987654).isoformat()?>').renders()
	assert 'yes' == T('<?if @(2000-02-29T12:34:56.987654)?>yes<?else?>no<?end if?>').renders()


@pytest.mark.ul4
def test_color(T):
	assert '255,255,255,255' == T('<?code c = #fff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>').renders()
	assert '255,255,255,255' == T('<?code c = #ffffff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>').renders()
	assert '18,52,86,255' == T('<?code c = #123456?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>').renders()
	assert '17,34,51,68' == T('<?code c = #1234?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>').renders()
	assert '18,52,86,120' == T('<?code c = #12345678?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>').renders()
	assert 'yes' == T('<?if #fff?>yes<?else?>no<?end if?>').renders()


@pytest.mark.ul4
def test_slice(T):
	source = "<?print repr(obj.start)?>:<?print repr(obj.stop)?>"

	obj = slice(17, 42)
	assert "17:42" == T(source).renders(obj=obj)

	obj = slice(None, None)
	assert "None:None" == T(source).renders(obj=obj)

	with raises(subscriptablemessage):
		T("<?print repr(obj['start'])?>").renders(obj=obj)

	with raises(subscriptablemessage):
		T("<?print repr(obj['stop'])?>").renders(obj=obj)


@pytest.mark.ul4
def test_list(T):
	assert '' == T('<?for item in []?><?print item?>;<?end for?>').renders()
	assert '1;' == T('<?for item in [1]?><?print item?>;<?end for?>').renders()
	assert '1;' == T('<?for item in [1,]?><?print item?>;<?end for?>').renders()
	assert '1;2;' == T('<?for item in [1, 2]?><?print item?>;<?end for?>').renders()
	assert '1;2;' == T('<?for item in [1, 2,]?><?print item?>;<?end for?>').renders()
	assert 'no' == T('<?if []?>yes<?else?>no<?end if?>').renders()
	assert 'yes' == T('<?if [1]?>yes<?else?>no<?end if?>').renders()


@pytest.mark.ul4
def test_unpacklist(T):
	assert '[]' == T('<?print [*[]]?>').renders()
	assert '[0, 1, 2]' == T('<?print [*range(3)]?>').renders()
	assert '[0, 1, 2]' == T('<?print [*[0, 1, 2]]?>').renders()
	assert '[-1, 0, 1, 2, -2, 3, 4, 5]' == T('<?print [-1, *range(3), -2, *range(3, 6)]?>').renders()
	assert '[0]' == T('<?print [*{0: 1}]?>').renders()


@pytest.mark.ul4
def test_listcomp(T):
	assert "[2, 6]" == T("<?code d = [2*i for i in range(4) if i%2]?><?print d?>").renders()
	assert "[0, 2, 4, 6]" == T("<?code d = [2*i for i in range(4)]?><?print d?>").renders()

	# Make sure that the loop variables doesn't leak into the surrounding scope
	assert T("<?code d = [2*i for i in range(4)]?><?print type(i)?>").renders() in {"<type undefinedvariable>", "<type undefined>"}


@pytest.mark.ul4
def test_set(T):
	assert '' == T('<?for item in {/}?><?print item?>!<?end for?>').renders()
	assert 'gurk!' == T('<?for item in {"gurk"}?><?print item?>!<?end for?>').renders()
	assert 'no' == T('<?if {/}?>yes<?else?>no<?end if?>').renders()
	assert 'yes' == T('<?if {"gurk"}?>yes<?else?>no<?end if?>').renders()
	if T is not TemplateJavascriptV8:
		assert '<type int>' == T('<?for item in {1}?><?print type(item)?><?end for?>').renders()

	# Make sure that the loop variables doesn't leak into the surrounding scope
	assert T("<?code d = {str(2*i) for i in range(4)}?><?print type(i)?>").renders() in {"<type undefinedvariable>", "<type undefined>"}


@pytest.mark.ul4
def test_unpackset(T):
	assert '{/}' == T('<?print {*{/}}?>').renders()
	assert '{/}' == T('<?print {*[]}?>').renders()
	assert '[0, 1, 2]' == T('<?print sorted({*range(3)})?>').renders()
	assert '[0, 1, 2]' == T('<?print sorted({*{0, 1, 2}})?>').renders()
	assert '[-2, -1, 0, 1, 2, 3, 4, 5]' == T('<?print sorted({-1, *range(3), -2, *range(3, 6)})?>').renders()
	assert '{0}' == T('<?print {*{0: 1}}?>').renders()


@pytest.mark.ul4
def test_genexpr(T):
	assert "2, 6:" == T("<?code ge = (str(2*i) for i in range(4) if i%2)?><?print ', '.join(ge)?>:<?print ', '.join(ge)?>").renders()
	assert "2, 6" == T("<?print ', '.join(str(2*i) for i in range(4) if i%2)?>").renders()
	assert "0, 2, 4, 6" == T("<?print ', '.join(str(2*i) for i in range(4))?>").renders()
	assert "0, 2, 4, 6" == T("<?print ', '.join((str(2*i) for i in range(4)))?>").renders()
	assert "0:g; 1:r; 2:k" == T("<?for (i, c2) in enumerate(c for c in 'gurk' if c != 'u')?><?if i?>; <?end if?><?print i?>:<?print c2?><?end for?>").renders()

	# Make sure that the loop variables doesn't leak into the surrounding scope
	assert T("<?code d = (2*i for i in range(4))?><?print type(i)?>").renders() in {"<type undefinedvariable>", "<type undefined>"}


@pytest.mark.ul4
def test_dict(T):
	assert '{}' == T('<?print {}?>').renders()
	assert '' == T('<?for (key, value) in {}.items()?><?print key?>:<?print value?>\n<?end for?>').renders()
	assert '1:2\n' == T('<?for (key, value) in {1:2}.items()?><?print key?>:<?print value?>\n<?end for?>').renders()
	assert '1:#fff\n' == T('<?for (key, value) in {1:#fff}.items()?><?print key?>:<?print value?>\n<?end for?>').renders()
	assert '1:2\n' == T('<?for (key, value) in {1:2,}.items()?><?print key?>:<?print value?>\n<?end for?>').renders()
	# With duplicate keys, later ones simply overwrite earlier ones
	assert '1:3\n' == T('<?for (key, value) in {1:2, 1: 3}.items()?><?print key?>:<?print value?>\n<?end for?>').renders()
	assert 'no' == T('<?if {}?>yes<?else?>no<?end if?>').renders()
	assert 'yes' == T('<?if {1:2}?>yes<?else?>no<?end if?>').renders()
	if T is not TemplateJavascriptV8:
		assert '<type int>' == T('<?for (key, value) in {1:2}.items()?><?print type(key)?><?end for?>').renders()

	# Make sure that the loop variables doesn't leak into the surrounding scope
	assert T("<?code d = {i: 2*i for i in range(4)}?><?print type(i)?>").renders() in {"<type undefinedvariable>", "<type undefined>"}


@pytest.mark.ul4
def test_unpackdict(T):
	assert '{}' == T('<?print {**{}}?>').renders()
	assert '2:two;0:zero;1:one;' == T('<?code a = {0: "zero", 1: "one"}?><?code b = {2: "two", **a}?><?for (k, v) in b.items()?><?print k?>:<?print v?>;<?end for?>').renders()
	assert '3:three;0:zero;1:one;2:two;' == T('<?code a = {0: "zero", 1: "one"}?><?code b = {2: "two"}?><?code c = {3: "three", **a, **b.items()}?><?for (k, v) in c.items()?><?print k?>:<?print v?>;<?end for?>').renders()


@pytest.mark.ul4
def test_dictcomp(T):
	assert "" == T("<?code d = {str(i):2*i for i in range(10) if i%2}?><?if '2' in d?><?print d['2']?><?end if?>").renders()
	assert "6" == T("<?code d = {str(i):2*i for i in range(10) if i%2}?><?if '3' in d?><?print d['3']?><?end if?>").renders()
	assert "6" == T("<?code d = {str(i):2*i for i in range(10)}?><?print d['3']?>").renders()
	if T is not TemplateJavascriptV8:
		# V8 doesn't support Maps, so for dictionaries we're using plain objects (which only supports string keys)
		assert '45' == T('<?code d = {i:2*i for i in range(10)}?><?print sum(d)?>').renders()


@pytest.mark.ul4
def test_print(T):
	assert "" == T("<?print None?>").renders()
	assert "<foo>" == T("<?print '<foo>'?>").renders()


@pytest.mark.ul4
def test_printx(T):
	assert "" == T("<?printx None?>").renders()
	assert "&lt;foo&gt;" == T("<?printx '<foo>'?>").renders()


@pytest.mark.ul4
def test_setvar(T):
	assert '42' == T('<?code x = 42?><?print x?>').renders()
	assert 'xyzzy' == T('<?code x = "xyzzy"?><?print x?>').renders()
	assert 'x,y' == T('<?code (x, y) = "xy"?><?print x?>,<?print y?>').renders()
	assert '42' == T('<?code (x,) = [42]?><?print x?>').renders()
	assert '17,23' == T('<?code (x,y) = [17, 23]?><?print x?>,<?print y?>').renders()
	assert '17,23,37,42,105' == T('<?code ((v, w), (x,), (y,), z) = [[17, 23], [37], [42], 105]?><?print v?>,<?print w?>,<?print x?>,<?print y?>,<?print z?>').renders()


@pytest.mark.ul4
def test_setvar_iterator(T):
	assert 'g;k' == T("<?code (x,y) = (c for c in 'gurk' if c < 'r')?><?print x?>;<?print y?>").renders()


@pytest.mark.ul4
def test_addvar(T):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			assert x + y == eval(T(f'<?code x = {x}?><?code x += {y}?><?print x?>').renders())
	assert 'xyzzy' == T('<?code x = "xyz"?><?code x += "zy"?><?print x?>').renders()
	assert '[1, 2, 3, 4]' == T('<?code x = [1, 2]?><?code x += [3, 4]?><?print x?>').renders()


@pytest.mark.ul4
def test_subvar(T):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			assert x - y == eval(T(f'<?code x = {x}?><?code x -= {y}?><?print x?>').renders())


@pytest.mark.ul4
def test_mulvar(T):
	for x in (17, 17., False, True):
		for y in (23, 23., False, True):
			assert x * y == eval(T(f'<?code x = {x}?><?code x *= {y}?><?print x?>').renders())
	for x in (17, False, True):
		y = "xyzzy"
		assert x * y == T(f'<?code x = {x}?><?code x *= {y!r}?><?print x?>').renders()
	assert 17*"xyzzy" == T('<?code x = "xyzzy"?><?code x *= 17?><?print x?>').renders()


@pytest.mark.ul4
def test_floordivvar(T):
	for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
		for y in (2, -2, 2.0, -2.0, True):
			assert x // y == eval(T(f'<?code x = {x}?><?code x //= {y}?><?print x?>').renders())


@pytest.mark.ul4
def test_truedivvar(T):
	for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
		for y in (2, -2, 2.0, -2.0, True):
			assert x / y == eval(T(f'<?code x = {x}?><?code x /= {y}?><?print x?>').renders())


@pytest.mark.ul4
def test_modvar(T):
	for x in (1729, 1729.0, -1729, -1729.0, False, True):
		for y in (23, 23., -23, -23.0, True):
			assert x % y == eval(T(f'<?code x = {x}?><?code x %= {y}?><?print x?>').renders())


@pytest.mark.ul4
def test_shiftleftvar(T):
	t = T("<?code x <<= y?><?print x?>")

	assert "1" == t.renders(x=True, y=False)
	assert "2" == t.renders(x=True, y=True)
	assert "0" == t.renders(x=1, y=-1)
	assert "-256" == t.renders(x=-1, y=8)
	assert "2147483648" == t.renders(x=1, y=31)
	assert "4294967296" == t.renders(x=1, y=32)
	if T in (TemplateJavascriptV8, TemplateJavascriptNode):
		# Javascript numbers don't have enough precision
		assert "18014398509481984" == t.renders(x=1, y=54)
	else:
		assert "9223372036854775808" == t.renders(x=1, y=63)
		assert "18446744073709551616" == t.renders(x=1, y=64)
		assert "340282366920938463463374607431768211456" == t.renders(x=1, y=128)


@pytest.mark.ul4
def test_shiftrightvar(T):
	t = T("<?code x >>= y?><?print x?>")

	assert "1" == t.renders(x=True, y=False)
	assert "0" == t.renders(x=True, y=True)
	assert "2" == t.renders(x=1, y=-1)
	assert "2147483648" == t.renders(x=1, y=-31)
	assert "1" == t.renders(x=2147483648, y=31)
	assert "0" == t.renders(x=1, y=32)
	assert "-1" == t.renders(x=-1, y=10)
	assert "-1" == t.renders(x=-4, y=10)


@pytest.mark.ul4
def test_bitandvar(T):
	t = T("<?code x &= y?><?print x?>")

	assert "0" == t.renders(x=False, y=False)
	assert "0" == t.renders(x=False, y=True)
	assert "1" == t.renders(x=True, y=True)
	assert "1" == t.renders(x=3, y=True)
	assert "12" == t.renders(x=15, y=60)
	assert "0" == t.renders(x=255, y=256)
	assert "0" == t.renders(x=255, y=-256)
	assert "1" == t.renders(x=255, y=-255)


@pytest.mark.ul4
def test_bitxorvar(T):
	t = T("<?code x ^= y?><?print x?>")

	assert "0" == t.renders(x=False, y=False)
	assert "1" == t.renders(x=False, y=True)
	assert "0" == t.renders(x=True, y=True)
	assert "2" == t.renders(x=3, y=True)
	assert "51" == t.renders(x=15, y=60)
	assert "511" == t.renders(x=255, y=256)
	assert "-1" == t.renders(x=255, y=-256)
	assert "-2" == t.renders(x=255, y=-255)


@pytest.mark.ul4
def test_bitorvar(T):
	t = T("<?code x |= y?><?print x?>")

	assert "0" == t.renders(x=False, y=False)
	assert "1" == t.renders(x=False, y=True)
	assert "1" == t.renders(x=True, y=True)
	assert "3" == t.renders(x=3, y=True)
	assert "63" == t.renders(x=15, y=60)
	assert "511" == t.renders(x=255, y=256)
	assert "-1" == t.renders(x=255, y=-256)
	assert "-1" == t.renders(x=255, y=-255)


@pytest.mark.ul4
def test_for_string(T):
	assert '' == T('<?for c in data?>(<?print c?>)<?end for?>').renders(data="")
	assert '(g)(u)(r)(k)' == T('<?for c in data?>(<?print c?>)<?end for?>').renders(data="gurk")


@pytest.mark.ul4
def test_for_list(T):
	assert '' == T('<?for c in data?>(<?print c?>)<?end for?>').renders(data="")
	assert '(g)(u)(r)(k)' == T('<?for c in data?>(<?print c?>)<?end for?>').renders(data=["g", "u", "r", "k"])


@pytest.mark.ul4
def test_for_dict(T):
	assert '' == T('<?for c in data?>(<?print c?>)<?end for?>').renders(data={})
	assert '(a)(b)(c)' == T('<?for c in sorted(data)?>(<?print c?>)<?end for?>').renders(data=dict(a=1, b=2, c=3))


@pytest.mark.ul4
def test_for_nested_loop(T):
	assert '[(1)(2)][(3)(4)]' == T('<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>').renders(data=[[1, 2], [3, 4]])


@pytest.mark.ul4
def test_for_leak(T):
	# Both loop variables and variables assigned in the block leak into the surrounding scope.
	assert '4;4' == T('<?code x = 17?><?code y = 23?><?for x in range(5)?><?code y = x?><?end for?><?print x?>;<?print y?>').renders()


@pytest.mark.ul4
def test_for_unpacking(T):
	data = [
		("spam", "eggs", 17),
		("gurk", "hurz", 23),
		("hinz", "kunz", 42),
	]

	assert '(spam)(gurk)(hinz)' == T('<?for (a,) in data?>(<?print a?>)<?end for?>').renders(data=[item[:1] for item in data])
	assert '(spam,eggs)(gurk,hurz)(hinz,kunz)' == T('<?for (a, b) in data?>(<?print a?>,<?print b?>)<?end for?>').renders(data=[item[:2] for item in data])
	assert '(spam,eggs,17)(gurk,hurz,23)(hinz,kunz,42)' == T('<?for (a, b, c) in data?>(<?print a?>,<?print b?>,<?print c?>)<?end for?>').renders(data=data)


@pytest.mark.ul4
def test_for_nested_unpacking(T):
	data = [
		(("spam", "eggs"), (17,), None),
		(("gurk", "hurz"), (23,), False),
		(("hinz", "kunz"), (42,), True),
	]

	assert '(spam,eggs,17,)(gurk,hurz,23,False)(hinz,kunz,42,True)' == T('<?for ((a, b), (c,), d) in data?>(<?print a?>,<?print b?>,<?print c?>,<?print d?>)<?end for?>').renders(data=data)


@pytest.mark.ul4
def test_while(T):
	assert "0;1;2;" == T("<?code i = 0?><?while i < 3?><?print i?>;<?code i+=1?><?end while?>").renders()


@pytest.mark.ul4
def test_while_break(T):
	assert "0;1;2;" == T("<?code i = 0?><?while i < 30?><?print i?>;<?code i+=1?><?if i == 3?><?break?><?end if?><?end while?>").renders()


@pytest.mark.ul4
def test_for_break(T):
	assert '1, 2, ' == T('<?for i in [1,2,3]?><?print i?>, <?if i==2?><?break?><?end if?><?end for?>').renders()


@pytest.mark.ul4
def test_break_nested(T):
	assert '1, 1, 2, 1, 2, 3, ' == T('<?for i in [1,2,3,4]?><?for j in [1,2,3,4]?><?print j?>, <?if j>=i?><?break?><?end if?><?end for?><?if i>=3?><?break?><?end if?><?end for?>').renders()


@pytest.mark.ul4
def test_continue(T):
	assert '1, 3, ' == T('<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?print i?>, <?end for?>').renders()


@pytest.mark.ul4
def test_continue_nested(T):
	assert '1, 3, \n1, 3, \n' == T('<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?for j in [1,2,3]?><?if j==2?><?continue?><?end if?><?print j?>, <?end for?>\n<?end for?>').renders()


@pytest.mark.ul4
def test_if(T):
	assert '42' == T('<?if data?><?print data?><?end if?>').renders(data=42)


@pytest.mark.ul4
def test_else(T):
	t = T('<?if data?><?print data?><?else?>no<?end if?>')
	assert '42' == t.renders(data=42)
	assert 'no' == t.renders(data=0)


@pytest.mark.ul4
def test_block_errors(T):
	with raises("block unclosed"):
		T('<?for x in data?>').renders()

	with raises("<\\?for\\?> ended by <\\?end if\\?>|<\\?end if\\?> doesn't match any <\\?if\\?>"):
		T('<?for x in data?><?end if?>').renders()

	with raises("not in any block"):
		T('<?end?>').renders()

	with raises("not in any block"):
		T('<?end for?>').renders()

	with raises("not in any block"):
		T('<?end if?>').renders()

	with raises("<\\?else\\?> doesn't match any <\\?if\\?>"):
		T('<?else?>').renders()

	with raises("block unclosed"):
		T('<?if data?>').renders()

	with raises("block unclosed"):
		T('<?if data?><?else?>').renders()

	with raises("duplicate <\\?else\\?> in <\\?if\\?>/<\\?elif\\?>/<\\?else\\?> chain|<\\?else\\?> already seen in <\\?if\\?>"):
		T('<?if data?><?else?><?else?>').renders()

	with raises("<\\?elif\\?> can't follow <\\?else\\?> in <\\?if\\?>/<\\?elif\\?>/<\\?else\\?> chain|<\\?else\\?> already seen in <\\?if\\?>"):
		T('<?if data?><?else?><?elif data?>').renders()

	with raises("<\\?elif\\?> can't follow <\\?else\\?> in <\\?if\\?>/<\\?elif\\?>/<\\?else\\?> chain|<\\?else\\?> already seen in <\\?if\\?>"):
		T('<?if data?><?elif data?><?elif data?><?else?><?elif data?>').renders()

	with raises("<\\?ignore\\?> block unclosed"):
		T('<?ignore?><?ignore?>nix<?end ignore?>').renders()

	with raises("not in any block"):
		T('<?ignore?>nix<?end ignore?><?end ignore?>').renders()


@pytest.mark.ul4
def test_ignore(T):
	assert "" == T("<?ignore?>nix<?end ignore?>").renders()
	assert "" == T("<?ignore?><?if?>nix<?end ignore?>").renders()
	assert "" == T("<?ignore?><?if?>nix<?end?><?end for?><?end ignore?>").renders()
	assert "" == T("<?ignore?>nix<?ignore?>nix<?end ignore?>nix<?end ignore?>").renders()
	assert "doch" == T("<?ignore?>nix<?ignore?>nix<?end ignore?>nix<?end ignore?>doch<?ignore?>nix<?ignore?>nix<?end ignore?>nix<?end ignore?>").renders()


@pytest.mark.ul4
def test_empty():
	with raises("expression required"):
		TemplatePython('<?print?>').renders()

	with raises("expression required"):
		TemplatePython('<?if?>').renders()

	with raises("expression required"):
		TemplatePython('<<?if x?><?elif?><?end if?>').renders()

	with raises("loop expression required"):
		TemplatePython('<?for?>').renders()

	with raises("statement required"):
		TemplatePython('<?code?>').renders()


@pytest.mark.ul4
def test_add(T):
	t = T('<?print x + y?>')
	values = (17, 23, 1., -1.)

	for x in values:
		for y in values:
			assert x + y == eval(t.renders(x=x, y=y)) # Using ``eval`` avoids problem with the nonexistent int/float distinction in JS
	assert 'foobar' == T('<?code x="foo"?><?code y="bar"?><?print x+y?>').renders()
	assert '[1, 2, 3, 4]' == t.renders(x=[1, 2], y=[3, 4])
	assert '(f)(o)(o)(b)(a)(r)' == T('<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>').renders(data=dict(foo="foo", bar="bar"))
	assert "2012-10-18 00:00" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(1))
	assert "2013-10-17 00:00" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(365))
	assert "2012-10-17 12:00" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 12*60*60))
	assert "2012-10-17 00:00:01" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 1))
	if T is not TemplatePHP:
		assert "2012-10-17 00:00:00.500000" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 0, 500000))
		assert "2012-10-17 00:00:00.001000" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 0, 1000))
	assert "2 days, 0:00:00" == t.renders(x=datetime.timedelta(1), y=datetime.timedelta(1))
	assert "1 day, 0:00:01" == t.renders(x=datetime.timedelta(1), y=datetime.timedelta(0, 1))
	assert "1 day, 0:00:00.000001" == t.renders(x=datetime.timedelta(1), y=datetime.timedelta(0, 0, 1))
	assert "2 months" == t.renders(x=misc.monthdelta(1), y=misc.monthdelta(1))
	assert "2000-02-29" == t.renders(x=datetime.date(2000, 1, 31), y=misc.monthdelta(1))
	assert "2000-02-01 00:00" == t.renders(x=datetime.datetime(2000, 1, 1), y=misc.monthdelta(1))
	assert "1999-11-30 00:00" == t.renders(x=datetime.datetime(2000, 1, 31), y=misc.monthdelta(-2))
	assert "2000-03-29 00:00" == t.renders(x=datetime.datetime(2000, 2, 29), y=misc.monthdelta(1))
	assert "2001-02-28 00:00" == t.renders(x=datetime.datetime(2000, 2, 29), y=misc.monthdelta(12))
	assert "2001-02-28 00:00" == t.renders(x=misc.monthdelta(12), y=datetime.datetime(2000, 2, 29))


@pytest.mark.ul4
def test_sub(T):
	t = T('<?print x - y?>')

	values = (17, 23, 1., -1.)

	for x in values:
		for y in values:
			assert x - y == eval(t.renders(x=x, y=y))

	assert "2012-10-16 00:00" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(1))
	assert "2011-10-17 00:00" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(366))
	assert "2012-10-16 12:00" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 12*60*60))
	assert "2012-10-16 23:59:59" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 1))
	if T is not TemplatePHP:
		assert "2012-10-16 23:59:59.500000" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 0, 500000))
		assert "2012-10-16 23:59:59.999000" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.timedelta(0, 0, 1000))
		assert "2 days, 0:00:00" == t.renders(x=datetime.datetime(2012, 10, 17), y=datetime.datetime(2012, 10, 15))
		assert "730 days, 0:00:00" == t.renders(x=datetime.datetime(1999, 1, 1), y=datetime.datetime(1997, 1, 1))
	assert "0:00:00" == t.renders(x=datetime.timedelta(1), y=datetime.timedelta(1))
	assert "1 day, 0:00:00" == t.renders(x=datetime.timedelta(2), y=datetime.timedelta(1))
	assert "23:59:59" == t.renders(x=datetime.timedelta(1), y=datetime.timedelta(0, 1))
	assert "23:59:59.999999" == t.renders(x=datetime.timedelta(1), y=datetime.timedelta(0, 0, 1))
	assert "-1 day, 23:59:59" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0, 1))
	assert "-1 day, 23:59:59.999999" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0, 0, 1))
	assert "2000-01-01 00:00" == t.renders(x=datetime.datetime(2000, 2, 1), y=misc.monthdelta(1))
	assert "2000-02-29 00:00" == t.renders(x=datetime.datetime(1999, 12, 31), y=misc.monthdelta(-2))
	assert "2000-02-29 00:00" == t.renders(x=datetime.datetime(2000, 3, 29), y=misc.monthdelta(1))
	assert "1999-02-28 00:00" == t.renders(x=datetime.datetime(2000, 2, 29), y=misc.monthdelta(12))
	assert "2000-02-29" == t.renders(x=datetime.date(2000, 3, 31), y=misc.monthdelta(1))
	assert "-1 month" == t.renders(x=misc.monthdelta(2), y=misc.monthdelta(3))
	assert "365 days, 0:00:00" == t.renders(x=datetime.datetime(2015, 1, 1), y=datetime.datetime(2014, 1, 1))
	assert "-365 days, 0:00:00" == t.renders(x=datetime.datetime(2014, 1, 1), y=datetime.datetime(2015, 1, 1))
	assert "135 days, 0:00:00" == t.renders(x=datetime.datetime(2015, 10, 10), y=datetime.datetime(2015, 5, 28))
	assert "1:00:00" == t.renders(x=datetime.datetime(2015, 1, 1, 13), y=datetime.datetime(2015, 1, 1, 12))

	base = datetime.datetime(2015, 1, 1, 1)
	dates = (
		datetime.datetime(2015, 1, 2, 1),
		datetime.datetime(2015, 1, 2, 2),
		datetime.datetime(2015, 1, 2, 2, 1),
		datetime.datetime(2015, 1, 2, 2, 1, 1),
		datetime.datetime(2015, 1, 2, 2, 1, 1, 1000),
	)
	assert "1 day, 0:00:00" == t.renders(x=dates[0], y=base)
	assert "1 day, 1:00:00" == t.renders(x=dates[1], y=base)
	assert "1 day, 1:01:00" == t.renders(x=dates[2], y=base)
	assert "1 day, 1:01:01" == t.renders(x=dates[3], y=base)
	assert "1 day, 1:01:01.001000" == t.renders(x=dates[4], y=base)
	assert "-1 day, 0:00:00" == t.renders(x=base, y=dates[0])
	assert "-2 days, 23:00:00" == t.renders(x=base, y=dates[1])
	assert "-2 days, 22:59:00" == t.renders(x=base, y=dates[2])
	assert "-2 days, 22:58:59" == t.renders(x=base, y=dates[3])
	assert "-2 days, 22:58:58.999000" == t.renders(x=base, y=dates[4])


@pytest.mark.ul4
def test_neg(T):
	t = T("<?print -x?>")

	assert "0" == t.renders(x=False)
	assert "-1" == t.renders(x=True)
	assert "-17" == t.renders(x=17)
	assert "-42.5" == t.renders(x=42.5)
	assert "0:00:00" == t.renders(x=datetime.timedelta())
	assert "-1 day, 0:00:00" == t.renders(x=datetime.timedelta(1))
	assert "-1 day, 23:59:59" == t.renders(x=datetime.timedelta(0, 1))
	assert "-1 day, 23:59:59.999999" == t.renders(x=datetime.timedelta(0, 0, 1))
	assert "0 months" == t.renders(x=misc.monthdelta())
	assert "-1 month" == t.renders(x=misc.monthdelta(1))
	# This checks constant folding
	assert "0" == T("<?print -False?>").renders()
	assert "-1" == T("<?print -True?>").renders()
	assert "-2" == T("<?print -2?>").renders()
	assert "-2.5" == T("<?print -2.5?>").renders()


@pytest.mark.ul4
def test_bitnot(T):
	t = T("<?print ~x?>")

	assert "-1" == t.renders(x=False)
	assert "-2" == t.renders(x=True)
	assert "-1" == t.renders(x=0)
	assert "-256" == t.renders(x=255)
	assert "-4294967297" == t.renders(x=1 << 32)
	if T in (TemplateJavascriptV8, TemplateJavascriptNode):
		# Javascript numbers don't have enough precision
		assert "-4503599627370497" == t.renders(x=1 << 52)
	else:
		assert "-18446744073709551617" == t.renders(x=1 << 64)


@pytest.mark.ul4
def test_mul(T):
	t = T('<?print x * y?>')
	values = (17, 23, 1., -1.)

	for x in values:
		for y in values:
			assert x * y == eval(t.renders(x=x, y=y))
	assert 17*"foo" == T('<?print 17*"foo"?>').renders()
	assert 17*"foo" == T('<?code x=17?><?code y="foo"?><?print x*y?>').renders()
	assert "foo"*17 == T('<?code x="foo"?><?code y=17?><?print x*y?>').renders()
	assert "foo"*17 == T('<?print "foo"*17?>').renders()
	assert "(foo)(bar)(foo)(bar)(foo)(bar)" == T('<?for i in 3*data?>(<?print i?>)<?end for?>').renders(data=["foo", "bar"])
	assert "0:00:00" == t.renders(x=4, y=datetime.timedelta())
	assert "4 days, 0:00:00" == t.renders(x=4, y=datetime.timedelta(1))
	assert "2 days, 0:00:00" == t.renders(x=4, y=datetime.timedelta(0, 12*60*60))
	assert "0:00:02" == t.renders(x=4, y=datetime.timedelta(0, 0, 500000))
	assert "12:00:00" == t.renders(x=0.5, y=datetime.timedelta(1))
	assert "0:00:00" == t.renders(x=datetime.timedelta(), y=4)
	assert "4 days, 0:00:00" == t.renders(x=datetime.timedelta(1), y=4)
	assert "2 days, 0:00:00" == t.renders(x=datetime.timedelta(0, 12*60*60), y=4)
	assert "0:00:02" == t.renders(x=datetime.timedelta(0, 0, 500000), y=4)
	assert "12:00:00" == t.renders(x=datetime.timedelta(1), y=0.5)
	assert "4 months" == t.renders(x=4, y=misc.monthdelta(1))
	assert "4 months" == t.renders(x=misc.monthdelta(1), y=4)


@pytest.mark.ul4
def test_truediv(T):
	t = T("<?print x / y?>")

	assert "0.5" == T('<?print 1/2?>').renders()
	assert "0.5" == T('<?code x=1?><?code y=2?><?print x/y?>').renders()
	assert "0:00:00" == t.renders(x=datetime.timedelta(), y=4)
	assert "2 days, 0:00:00" == t.renders(x=datetime.timedelta(8), y=4)
	assert "12:00:00" == t.renders(x=datetime.timedelta(4), y=8)
	assert "0:00:00.500000" == t.renders(x=datetime.timedelta(0, 4), y=8)
	assert "2 days, 0:00:00" == t.renders(x=datetime.timedelta(1), y=0.5)
	assert "9:36:00" == t.renders(x=datetime.timedelta(1), y=2.5)
	assert "0:00:00" == t.renders(x=datetime.timedelta(), y=4)
	assert "2 days, 0:00:00" == t.renders(x=datetime.timedelta(8), y=4)
	assert "12:00:00" == t.renders(x=datetime.timedelta(4), y=8)
	assert "0:00:00.500000" == t.renders(x=datetime.timedelta(0, 4), y=8)
	assert 2.0 == eval(t.renders(x=datetime.timedelta(4), y=datetime.timedelta(2)))
	assert 2.0 == eval(t.renders(x=misc.monthdelta(4), y=misc.monthdelta(2)))

	for x in (True, 42, 42.5, datetime.timedelta(7)):
		for y in (False, 0, 0.0):
			with raises(zerodivisionmessage):
				t.renders(x=x, y=y)


@pytest.mark.ul4
def test_floordiv(T):
	t = T("<?print x // y?>")

	assert "0" == T('<?print 1//2?>').renders()
	assert "0" == T('<?code x=1?><?code y=2?><?print x//y?>').renders()

	for x in (True, 2, 3.5):
		for y in (True, 2, 3.5):
			assert x//y == float(t.renders(x=x, y=y))

	assert "1 month" == t.renders(x=misc.monthdelta(3), y=2)
	assert "1" == t.renders(x=misc.monthdelta(3), y=misc.monthdelta(2))

	for x in (True, 42, 42.5):
		for y in (False, 0, 0.0):
			with raises(zerodivisionmessage):
				t.renders(x=x, y=y)

	for x in (datetime.timedelta(7), misc.monthdelta(3)):
		for y in (False, 0):
			with raises(zerodivisionmessage):
				t.renders(x=x, y=y)

	with raises(zerodivisionmessage):
		t.renders(x=datetime.timedelta(5), y=datetime.timedelta(0))

	with raises(zerodivisionmessage):
		t.renders(x=misc.monthdelta(5), y=misc.monthdelta(0))


@pytest.mark.ul4
def test_mod(T):
	values = (17, 23, 17., 23.)

	t = T('<?print x % y?>')

	for x in values:
		for y in values:
			assert x % y == eval(T(f'<?print {x} % {y}?>').renders())
			assert x % y == eval(t.renders(x=x, y=y))


@pytest.mark.ul4
def test_shiftleft(T):
	t = T("<?print x << y?>")

	assert "16" == T("<?print 1 << 4?>").renders()
	assert "2" == T("<?print True << True?>").renders()
	assert "1" == t.renders(x=True, y=False)
	assert "2" == t.renders(x=True, y=True)
	assert "0" == t.renders(x=1, y=-1)
	assert "-256" == t.renders(x=-1, y=8)
	assert "2147483648" == t.renders(x=1, y=31)
	assert "4294967296" == t.renders(x=1, y=32)
	if T in (TemplateJavascriptV8, TemplateJavascriptNode):
		# Javascript numbers don't have enough precision
		assert "9007199254740992" == t.renders(x=1, y=53)
	else:
		assert "9223372036854775808" == t.renders(x=1, y=63)
		assert "18446744073709551616" == t.renders(x=1, y=64)
		assert "340282366920938463463374607431768211456" == t.renders(x=1, y=128)


@pytest.mark.ul4
def test_shiftright(T):
	t = T("<?print x >> y?>")

	assert "1" == T("<?print 16 >> 4?>").renders()
	assert "0" == T("<?print True >> True?>").renders()
	assert "1" == t.renders(x=True, y=False)
	assert "0" == t.renders(x=True, y=True)
	assert "2" == t.renders(x=1, y=-1)
	assert "2147483648" == t.renders(x=1, y=-31)
	assert "1" == t.renders(x=2147483648, y=31)
	assert "0" == t.renders(x=1, y=32)
	assert "-1" == t.renders(x=-1, y=10)
	assert "-1" == t.renders(x=-4, y=10)


@pytest.mark.ul4
def test_bitand(T):
	t = T("<?print x & y?>")

	assert "2" == T("<?print 3 & 6?>").renders()
	assert "1" == T("<?print True & True?>").renders()
	assert "0" == t.renders(x=False, y=False)
	assert "0" == t.renders(x=False, y=True)
	assert "1" == t.renders(x=True, y=True)
	assert "1" == t.renders(x=3, y=True)
	assert "12" == t.renders(x=15, y=60)
	assert "0" == t.renders(x=255, y=256)
	assert "0" == t.renders(x=255, y=-256)
	assert "1" == t.renders(x=255, y=-255)


@pytest.mark.ul4
def test_bitxor(T):
	t = T("<?print x ^ y?>")

	assert "5" == T("<?print 3 ^ 6?>").renders()
	assert "0" == T("<?print True ^ True?>").renders()
	assert "0" == t.renders(x=False, y=False)
	assert "1" == t.renders(x=False, y=True)
	assert "0" == t.renders(x=True, y=True)
	assert "2" == t.renders(x=3, y=True)
	assert "51" == t.renders(x=15, y=60)
	assert "511" == t.renders(x=255, y=256)
	assert "-1" == t.renders(x=255, y=-256)
	assert "-2" == t.renders(x=255, y=-255)


@pytest.mark.ul4
def test_bitor(T):
	t = T("<?print x | y?>")

	assert "7" == T("<?print 3 | 6?>").renders()
	assert "1" == T("<?print False | True?>").renders()
	assert "0" == t.renders(x=False, y=False)
	assert "1" == t.renders(x=False, y=True)
	assert "1" == t.renders(x=True, y=True)
	assert "3" == t.renders(x=3, y=True)
	assert "63" == t.renders(x=15, y=60)
	assert "511" == t.renders(x=255, y=256)
	assert "-1" == t.renders(x=255, y=-256)
	assert "-1" == t.renders(x=255, y=-255)


@pytest.mark.ul4
def test_is(T):
	assert "True" == T("<?print None is None?>").renders()

	assert "False" == T("<?print 42 is None?>").renders()

	assert "True" == T("<?print x is None?>").renders(x=None)

	assert "False" == T("<?print x is None?>").renders(x=False)

	t = T('<?print x is y?>')

	assert "True" == t.renders(x=None, y=None)

	obj = 42
	assert "True" == t.renders(x=obj, y=obj)

	obj = [1, 2, 3]
	assert "True" == t.renders(x=obj, y=obj)

	assert "False" == t.renders(x=[1, 2, 3], y=[1, 2, 3])


@pytest.mark.ul4
def test_isnot(T):
	assert "False" == T("<?print None is not None?>").renders()

	assert "True" == T("<?print 42 is not None?>").renders()

	assert "False" == T("<?print x is not None?>").renders(x=None)

	assert "True" == T("<?print x is not None?>").renders(x=False)

	t = T('<?print x is not y?>')

	assert "False" == t.renders(x=None, y=None)

	obj = 42
	assert "False" == t.renders(x=obj, y=obj)

	obj = [1, 2, 3]
	assert "False" == t.renders(x=obj, y=obj)

	assert "True" == t.renders(x=[1, 2, 3], y=[1, 2, 3])


@pytest.mark.ul4
def test_eq(T):
	t = T('<?print x == y?>')
	numbervalues = (17, 23, 17., 23.)

	for x in numbervalues:
		for y in numbervalues:
			assert str(x == y) == T(f'<?print {x} == {y}?>').renders()
			assert str(x == y) == t.renders(x=x, y=y)

	assert "True" == t.renders(x=None, y=None)
	assert "True" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0))
	assert "False" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(1))
	assert "False" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0, 1))
	assert "False" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0, 0, 1))
	assert "True" == t.renders(x=misc.monthdelta(0), y=misc.monthdelta(0))
	assert "False" == t.renders(x=misc.monthdelta(0), y=misc.monthdelta(1))
	assert "True" == t.renders(x=True, y=True)
	assert "False" == t.renders(x=True, y=False)
	assert "True" == t.renders(x=True, y=1)
	assert "True" == t.renders(x=False, y=0)
	assert "False" == t.renders(x=False, y=1)
	assert "True" == t.renders(x=1, y=1.0)
	assert "False" == t.renders(x=1, y=-1.0)
	assert "True" == t.renders(x=True, y=1.0)
	assert "False" == t.renders(x=True, y=-1.0)
	assert "True" == t.renders(x="foo", y="foo")
	assert "False" == t.renders(x="foobar", y="foobaz")
	assert "True" == t.renders(x=datetime.date(2015, 11, 12), y=datetime.date(2015, 11, 12))
	assert "False" == t.renders(x=datetime.date(2015, 11, 12), y=datetime.date(2015, 11, 13))
	assert "True" == t.renders(x=color.Color(0x12, 0x34, 0x56, 0x78), y=color.Color(0x12, 0x34, 0x56, 0x78))
	assert "False" == t.renders(x=color.Color(0x12, 0x34, 0x56, 0x78), y=color.Color(0x11, 0x34, 0x56, 0x78))
	assert "False" == t.renders(x=color.Color(0x12, 0x34, 0x56, 0x78), y=color.Color(0x12, 0x33, 0x56, 0x78))
	assert "False" == t.renders(x=color.Color(0x12, 0x34, 0x56, 0x78), y=color.Color(0x12, 0x34, 0x55, 0x78))
	assert "False" == t.renders(x=color.Color(0x12, 0x34, 0x56, 0x78), y=color.Color(0x12, 0x34, 0x56, 0x77))
	assert "True" == t.renders(x=[], y=[])
	assert "True" == t.renders(x=[1, 2, 3], y=[1, 2, 3])
	assert "True" == t.renders(x=[1, [2, [3]]], y=[1, [2, [3]]])
	assert "False" == t.renders(x=[1, [2, [3]]], y=[1, [2, [4]]])
	assert "False" == t.renders(x=[1, 2, 3], y=[1, 2, 4])
	assert "False" == t.renders(x=[1, 2, 3], y=[1, 2, 3, 4])
	assert "True" == t.renders(x={}, y={})
	assert "True" == t.renders(x={1: 2, "foo": "bar"}, y={1: 2, "foo": "bar"})
	assert "False" == t.renders(x={1: 2, "foo": "bar"}, y={1: 2, "foo": "baz"})
	assert "False" == t.renders(x={1: 2, "foo": "bar", 3: 4}, y={1: 2, "foo": "bar", 5: 6})
	assert "True" == t.renders(x=set(), y=set())
	assert "True" == t.renders(x={1, "foo"}, y={1, "foo"})
	assert "False" == t.renders(x={1, "foo"}, y={1, "bar"})
	assert "False" == t.renders(x={1, 2}, y={1, 2, 3})

	# Mixed type comparisons
	assert "False" == t.renders(x=None, y=True)
	assert "False" == t.renders(x=None, y=42)
	assert "False" == t.renders(x=42, y="foo")
	assert "False" == t.renders(x="foo", y=[])
	assert "False" == t.renders(x=[], y={})
	assert "False" == t.renders(x={}, y=set())


@pytest.mark.ul4
def test_ne(T):
	t = T('<?print x != y?>')
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert str(x != y) == T(f'<?print {x} != {y}?>').renders()
			assert str(x != y) == t.renders(x=x, y=y)

	assert "False" == t.renders(x=None, y=None)
	assert "False" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0))
	assert "True" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(1))
	assert "True" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0, 1))
	assert "True" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0, 0, 1))
	assert "False" == t.renders(x=misc.monthdelta(0), y=misc.monthdelta(0))
	assert "True" == t.renders(x=misc.monthdelta(0), y=misc.monthdelta(1))
	assert "False" == t.renders(x=True, y=True)
	assert "True" == t.renders(x=True, y=False)
	assert "False" == t.renders(x=True, y=1)
	assert "False" == t.renders(x=False, y=0)
	assert "True" == t.renders(x=False, y=1)
	assert "False" == t.renders(x=1, y=1.0)
	assert "True" == t.renders(x=1, y=-1.0)
	assert "False" == t.renders(x=True, y=1.0)
	assert "True" == t.renders(x=True, y=-1.0)
	assert "False" == t.renders(x="foo", y="foo")
	assert "True" == t.renders(x="foobar", y="foobaz")
	assert "False" == t.renders(x=datetime.date(2015, 11, 12), y=datetime.date(2015, 11, 12))
	assert "True" == t.renders(x=datetime.date(2015, 11, 12), y=datetime.date(2015, 11, 13))
	assert "False" == t.renders(x=color.Color(0x12, 0x34, 0x56, 0x78), y=color.Color(0x12, 0x34, 0x56, 0x78))
	assert "True" == t.renders(x=color.Color(0x12, 0x34, 0x56, 0x78), y=color.Color(0x11, 0x34, 0x56, 0x78))
	assert "True" == t.renders(x=color.Color(0x12, 0x34, 0x56, 0x78), y=color.Color(0x12, 0x33, 0x56, 0x78))
	assert "True" == t.renders(x=color.Color(0x12, 0x34, 0x56, 0x78), y=color.Color(0x12, 0x34, 0x55, 0x78))
	assert "True" == t.renders(x=color.Color(0x12, 0x34, 0x56, 0x78), y=color.Color(0x12, 0x34, 0x56, 0x77))
	assert "False" == t.renders(x=[], y=[])
	assert "False" == t.renders(x=[1, 2, 3], y=[1, 2, 3])
	assert "False" == t.renders(x=[1, [2, [3]]], y=[1, [2, [3]]])
	assert "True" == t.renders(x=[1, [2, [3]]], y=[1, [2, [4]]])
	assert "True" == t.renders(x=[1, 2, 3], y=[1, 2, 4])
	assert "True" == t.renders(x=[1, 2, 3], y=[1, 2, 3, 4])
	assert "False" == t.renders(x={}, y={})
	assert "False" == t.renders(x={1: 2, "foo": "bar"}, y={1: 2, "foo": "bar"})
	assert "True" == t.renders(x={1: 2, "foo": "bar"}, y={1: 2, "foo": "baz"})
	assert "True" == t.renders(x={1: 2, "foo": "bar", 3: 4}, y={1: 2, "foo": "bar", 5: 6})
	assert "False" == t.renders(x=set(), y=set())
	assert "False" == t.renders(x={1, "foo"}, y={1, "foo"})
	assert "True" == t.renders(x={1, "foo"}, y={1, "bar"})
	assert "True" == t.renders(x={1, 2}, y={1, 2, 3})

	# Mixed type comparisons
	assert "True" == t.renders(x=None, y=True)
	assert "True" == t.renders(x=None, y=42)
	assert "True" == t.renders(x=42, y="foo")
	assert "True" == t.renders(x="foo", y=[])
	assert "True" == t.renders(x=[], y={})
	assert "True" == t.renders(x={}, y=set())


@pytest.mark.ul4
def test_lt(T):
	t = T('<?print x < y?>')
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert str(x < y) == T(f'<?print {x} < {y}?>').renders()
			assert str(x < y) == t.renders(x=x, y=y)

	assert "False" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0))
	assert "True" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(1))
	assert "True" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0, 1))
	assert "True" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0, 0, 1))
	assert "False" == t.renders(x=misc.monthdelta(0), y=misc.monthdelta(0))
	assert "True" == t.renders(x=misc.monthdelta(0), y=misc.monthdelta(1))
	assert "True" == t.renders(x=False, y=True)
	assert "False" == t.renders(x=True, y=False)
	assert "False" == t.renders(x=True, y=1)
	assert "True" == t.renders(x=False, y=1)
	assert "True" == t.renders(x=1, y=2.3)
	assert "False" == t.renders(x=1, y=-1.0)
	assert "True" == t.renders(x=True, y=2.0)
	assert "False" == t.renders(x=True, y=-1.0)
	assert "True" == t.renders(x="bar", y="foo")
	assert "False" == t.renders(x="foo", y="foo")
	assert "True" == t.renders(x="foobar", y="foobaz")
	assert "True" == t.renders(x=[1, 2], y=[1, 2, 3])
	assert "False" == t.renders(x=[1, 3], y=[1, 2])
	assert "True" == t.renders(x=[1, 2, "bar"], y=[1, 2, "foo"])
	assert "True" == t.renders(x=[1, 2, [3, "bar"]], y=[1, 2, [3, "foo"]])

	with raises(unorderabletypesmessage):
		t.renders(x=None, y=None)

	with raises(unorderabletypesmessage):
		t.renders(x=1, y="foo")

	with raises(unorderabletypesmessage):
		t.renders(x={}, y=[])


@pytest.mark.ul4
def test_le(T):
	t = T('<?print x <= y?>')
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert str(x <= y) == T(f'<?print {x} <= {y}?>').renders()
			assert str(x <= y) == t.renders(x=x, y=y)

	assert "True" == t.renders(x=datetime.timedelta(1), y=datetime.timedelta(1))
	assert "False" == t.renders(x=datetime.timedelta(1), y=datetime.timedelta(0))
	assert "False" == t.renders(x=datetime.timedelta(0, 1), y=datetime.timedelta(0))
	assert "False" == t.renders(x=datetime.timedelta(0, 0, 1), y=datetime.timedelta(0))
	assert "True" == t.renders(x=misc.monthdelta(1), y=misc.monthdelta(1))
	assert "False" == t.renders(x=misc.monthdelta(1), y=misc.monthdelta(0))
	assert "True" == t.renders(x=False, y=False)
	assert "False" == t.renders(x=True, y=False)
	assert "True" == t.renders(x=True, y=1)
	assert "True" == t.renders(x=False, y=1)
	assert "True" == t.renders(x=1, y=2.3)
	assert "False" == t.renders(x=1, y=-1.0)
	assert "True" == t.renders(x=True, y=2.0)
	assert "False" == t.renders(x=True, y=-1.0)
	assert "True" == t.renders(x="bar", y="foo")
	assert "True" == t.renders(x="foo", y="foo")
	assert "True" == t.renders(x="foobar", y="foobaz")
	assert "True" == t.renders(x=[1, 2], y=[1, 2])
	assert "True" == t.renders(x=[1, 2], y=[1, 2, 3])
	assert "False" == t.renders(x=[1, 3], y=[1, 2])
	assert "True" == t.renders(x=[1, 2, "foo"], y=[1, 2, "foo"])
	assert "True" == t.renders(x=[1, 2, "bar"], y=[1, 2, "foo"])
	assert "True" == t.renders(x=[1, 2, [3, "bar"]], y=[1, 2, [3, "foo"]])

	with raises(unorderabletypesmessage):
		t.renders(x=None, y=None)

	with raises(unorderabletypesmessage):
		t.renders(x=1, y="foo")

	with raises(unorderabletypesmessage):
		t.renders(x={}, y=[])


@pytest.mark.ul4
def test_gt(T):
	t = T('<?print x > y?>')
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert str(x > y) == T(f'<?print {x} > {y}?>').renders()
			assert str(x > y) == t.renders(x=x, y=y)

	assert "False" == t.renders(x=datetime.timedelta(1), y=datetime.timedelta(1))
	assert "True" == t.renders(x=datetime.timedelta(1), y=datetime.timedelta(0))
	assert "True" == t.renders(x=datetime.timedelta(0, 1), y=datetime.timedelta(0))
	assert "True" == t.renders(x=datetime.timedelta(0, 0, 1), y=datetime.timedelta(0))
	assert "False" == t.renders(x=misc.monthdelta(1), y=misc.monthdelta(1))
	assert "True" == t.renders(x=misc.monthdelta(1), y=misc.monthdelta(0))

	assert "True" == t.renders(x=True, y=False)
	assert "False" == t.renders(x=False, y=True)
	assert "False" == t.renders(x=1, y=True)
	assert "True" == t.renders(x=1, y=False)
	assert "True" == t.renders(x=2.3, y=1)
	assert "False" == t.renders(x=-1.0, y=1)
	assert "True" == t.renders(x=2.0, y=True)
	assert "False" == t.renders(x=-1.0, y=True)
	assert "True" == t.renders(x="foo", y="bar")
	assert "False" == t.renders(x="foo", y="foo")
	assert "True" == t.renders(x="foobaz", y="foobar")
	assert "True" == t.renders(x=[1, 2, 3], y=[1, 2])
	assert "False" == t.renders(x=[1, 2], y=[1, 3])
	assert "True" == t.renders(x=[1, 2, "foo"], y=[1, 2, "bar"])
	assert "True" == t.renders(x=[1, 2, [3, "foo"]], y=[1, 2, [3, "bar"]])

	with raises(unorderabletypesmessage):
		t.renders(x=None, y=None)

	with raises(unorderabletypesmessage):
		t.renders(x=1, y="foo")

	with raises(unorderabletypesmessage):
		t.renders(x={}, y=[])


@pytest.mark.ul4
def test_ge(T):
	t = T('<?print x >= y?>')
	values = (17, 23, 17., 23.)

	for x in values:
		for y in values:
			assert str(x >= y) == T(f'<?print {x} >= {y}?>').renders()
			assert str(x >= y) == t.renders(x=x, y=y)

	assert "True" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0))
	assert "False" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(1))
	assert "False" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0, 1))
	assert "False" == t.renders(x=datetime.timedelta(0), y=datetime.timedelta(0, 0, 1))
	assert "True" == t.renders(x=misc.monthdelta(0), y=misc.monthdelta(0))
	assert "False" == t.renders(x=misc.monthdelta(0), y=misc.monthdelta(1))
	assert "True" == t.renders(x=False, y=False)
	assert "False" == t.renders(x=False, y=True)
	assert "True" == t.renders(x=1, y=True)
	assert "True" == t.renders(x=1, y=False)
	assert "True" == t.renders(x=2.3, y=1)
	assert "False" == t.renders(x=False, y=1)
	assert "True" == t.renders(x=2.0, y=True)
	assert "False" == t.renders(x=-1.0, y=True)
	assert "True" == t.renders(x="foo", y="bar")
	assert "True" == t.renders(x="foo", y="foo")
	assert "True" == t.renders(x="foobaz", y="foobar")
	assert "True" == t.renders(x=[1, 2], y=[1, 2])
	assert "True" == t.renders(x=[1, 2, 3], y=[1, 2])
	assert "False" == t.renders(x=[1, 2], y=[1, 3])
	assert "True" == t.renders(x=[1, 2, "foo"], y=[1, 2, "foo"])
	assert "True" == t.renders(x=[1, 2, "foo"], y=[1, 2, "bar"])
	assert "True" == t.renders(x=[1, 2, [3, "foo"]], y=[1, 2, [3, "bar"]])

	with raises(unorderabletypesmessage):
		t.renders(x=None, y=None)

	with raises(unorderabletypesmessage):
		t.renders(x=1, y="foo")

	with raises(unorderabletypesmessage):
		t.renders(x={}, y=[])


@pytest.mark.ul4
def test_contains(T):
	t = T('<?print x in y?>')

	assert "True" == t.renders(x=2, y=[1, 2, 3])
	assert "False" == t.renders(x=4, y=[1, 2, 3])
	assert "True" == t.renders(x="ur", y="gurk")
	assert "False" == t.renders(x="un", y="gurk")
	assert "True" == t.renders(x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42))
	assert "False" == t.renders(x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42))
	assert "True" == t.renders(x="a", y={"a": 1, "b": 2})
	assert "False" == t.renders(x="c", y={"a": 1, "b": 2})
	if T is not TemplateJavascriptV8:
		assert "True" == t.renders(x=1, y={1: 2, 3: 4})


@pytest.mark.ul4
def test_notcontains(T):
	t = T('<?print x not in y?>')

	assert "False" == t.renders(x=2, y=[1, 2, 3])
	assert "True" == t.renders(x=4, y=[1, 2, 3])
	assert "False" == t.renders(x="ur", y="gurk")
	assert "True" == t.renders(x="un", y="gurk")
	assert "False" == t.renders(x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42))
	assert "True" == t.renders(x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42))
	assert "False" == t.renders(x="a", y={"a": 1, "b": 2})
	assert "True" == t.renders(x="c", y={"a": 1, "b": 2})
	if T is not TemplateJavascriptV8:
		assert "False" == t.renders(x=1, y={1: 2, 3: 4})


@pytest.mark.ul4
def test_and(T):
	t = T('<?print x and y?>')

	assert "False" == t.renders(x=False, y=False)
	assert "False" == t.renders(x=False, y=True)
	assert "0" == t.renders(x=0, y=True)


@pytest.mark.ul4
def test_or(T):
	t = T('<?print x or y?>')

	assert "False" == t.renders(x=False, y=False)
	assert "True" == t.renders(x=False, y=True)
	assert "42" == t.renders(x=42, y=True)


@pytest.mark.ul4
def test_not(T):
	t = T('<?print not x?>')

	assert "True" == t.renders(x=False)
	assert "False" == t.renders(x=42)


@pytest.mark.ul4
def test_ifexpr(T):
	t = T('<?print x if y else z?>')

	assert "17" == t.renders(x=17, y=True, z=23)
	assert "23" == t.renders(x=17, y=False, z=23)
	assert "17" == T('<?print 17 if True else 23?>').renders()
	assert "23" == T('<?print 17 if False else 23?>').renders()


@pytest.mark.ul4
def test_getitem(T):
	assert "u" == T("<?print 'gurk'[1]?>").renders()
	assert "u" == T("<?print x[1]?>").renders(x="gurk")
	assert "u" == T("<?print x[1]?>").renders(x=list("gurk"))
	assert "u" == T("<?print 'gurk'[-3]?>").renders()
	assert "u" == T("<?print x[-3]?>").renders(x="gurk")
	assert "u" == T("<?print x[-3]?>").renders(x=list("gurk"))

	with raises(indexmessage):
		T("<?print 'gurk'[4]?>").renders()

	with raises(indexmessage):
		T("<?print x[4]?>").renders(x="gurk")

	with raises(indexmessage):
		T("<?print x[4]?>").renders(x=list("gurk"))

	with raises(indexmessage):
		T("<?print 'gurk'[-5]?>").renders()

	with raises(indexmessage):
		T("<?print x[-5]?>").renders(x="gurk")

	with raises(indexmessage):
		T("<?print x[-5]?>").renders(x=list("gurk"))

	assert "z" == T("<?print x['y']?>").renders(x={"y": "z"})
	assert "z" == T("<?print x[None]?>").renders(x={None: "z"})


@pytest.mark.ul4
def test_setitem(T):
	assert "gark" == T("<?code x = list('gurk')?><?code x[1] = 'a'?><?print ''.join(x)?>").renders()
	assert "gark" == T("<?code x = list('gurk')?><?code x[-3] = 'a'?><?print ''.join(x)?>").renders()

	with raises(indexmessage):
		T("<?code x = list('gurk')?><?code x[4] = 'a'?><?print ''.join(x)?>").renders()

	with raises(indexmessage):
		T("<?code x = list('gurk')?><?code x[-5] = 'a'?><?print ''.join(x)?>").renders()


@pytest.mark.ul4
def test_getslice(T):
	assert "ur" == T("<?print 'gurk'[1:3]?>").renders()
	assert "ur" == T("<?print x[1:3]?>").renders(x="gurk")
	assert "ur" == T("<?print 'gurk'[-3:-1]?>").renders()
	assert "ur" == T("<?print x[-3:-1]?>").renders(x="gurk")
	assert "" == T("<?print 'gurk'[4:10]?>").renders()
	assert "" == T("<?print x[4:10]?>").renders(x="gurk")
	assert "" == T("<?print 'gurk'[-10:-5]?>").renders()
	assert "" == T("<?print x[-10:-5]?>").renders(x="gurk")
	assert "urk" == T("<?print 'gurk'[1:]?>").renders()
	assert "urk" == T("<?print x[1:]?>").renders(x="gurk")
	assert "urk" == T("<?print 'gurk'[-3:]?>").renders()
	assert "urk" == T("<?print x[-3:]?>").renders(x="gurk")
	assert "" == T("<?print 'gurk'[4:]?>").renders()
	assert "" == T("<?print x[4:]?>").renders(x="gurk")
	assert "gurk" == T("<?print 'gurk'[-10:]?>").renders()
	assert "gurk" == T("<?print x[-10:]?>").renders(x="gurk")
	assert "gur" == T("<?print 'gurk'[:3]?>").renders()
	assert "gur" == T("<?print x[:3]?>").renders(x="gurk")
	assert "gur" == T("<?print 'gurk'[:-1]?>").renders()
	assert "gur" == T("<?print x[:-1]?>").renders(x="gurk")
	assert "gurk" == T("<?print 'gurk'[:10]?>").renders()
	assert "gurk" == T("<?print x[:10]?>").renders(x="gurk")
	assert "" == T("<?print 'gurk'[:-5]?>").renders()
	assert "" == T("<?print x[:-5]?>").renders(x="gurk")
	assert "05" == T("<?print ('0' + str(x))[-2:]?>").renders(x=5)
	assert "15" == T("<?print ('0' + str(x))[-2:]?>").renders(x=15)
	assert "gurk" == T("<?print 'gurk'[:]?>").renders()
	assert "gurk" == T("<?print x[:]?>").renders(x="gurk")
	assert "[1, 2]" == T("<?print x[:]?>").renders(x=[1, 2])


@pytest.mark.ul4
def test_setslice(T):
	assert "[1, -2, -3, 4]" == T("<?code x = [1, 2, 3, 4]?><?code x[1:3] = [-2, -3]?><?print x?>").renders()
	assert "[1, -1, -4, -9, 4]" == T("<?code x = [1, 2, 3, 4]?><?code x[1:-1] = (-i*i for i in range(1, 4))?><?print x?>").renders()
	assert "[-1, -4, -9]" == T("<?code x = [1, 2, 3, 4]?><?code x[:] = (-i*i for i in range(1, 4))?><?print x?>").renders()


@pytest.mark.ul4
def test_nested(T):
	sc = "4"
	sv = "x"
	n = 4
	# when using 8, older Java version will output:
	# "An irrecoverable stack overflow has occurred"
	depth = 7
	for i in range(depth):
		sc = f"({sc})+({sc})"
		sv = f"({sv})+({sv})"
		n = n + n

	assert str(n) == T(f'<?print {sc}?>').renders()
	assert str(n) == T(f'<?code x=4?><?print {sv}?>').renders()


@pytest.mark.ul4
def test_precedence(T):
	assert "14" == T('<?print 2+3*4?>').renders()
	assert "20" == T('<?print (2+3)*4?>').renders()
	assert "10" == T('<?print -2+-3*-4?>').renders()
	assert "14" == T('<?print --2+--3*--4?>').renders()
	assert "14" == T('<?print (-(-2))+(-((-3)*-(-4)))?>').renders()
	assert "42" == T('<?print 2*data.value?>').renders(data=dict(value=21))
	assert "42" == T('<?print data.value[0]?>').renders(data=dict(value=[42]))
	assert "42" == T('<?print data[0].value?>').renders(data=[dict(value=42)])
	assert "42" == T('<?print data[0][0][0]?>').renders(data=[[[42]]])
	assert "42" == T('<?print data.value.value[0]?>').renders(data=dict(value=dict(value=[42])))
	assert "42" == T('<?print data.value.value[0].value.value[0]?>').renders(data=dict(value=dict(value=[dict(value=dict(value=[42]))])))


@pytest.mark.ul4
def test_associativity(T):
	assert "9" == T('<?print 2+3+4?>').renders()
	assert "-5" == T('<?print 2-3-4?>').renders()
	assert "24" == T('<?print 2*3*4?>').renders()
	if T not in (TemplateJavascriptV8, TemplateJavascriptNode):
		assert "2.0" == T('<?print 24/6/2?>').renders()
		assert "2" == T('<?print 24//6//2?>').renders()
	else:
		assert 2.0 == eval(T('<?print 24/6/2?>').renders())
		assert 2 == eval(T('<?print 24//6//2?>').renders())


@pytest.mark.ul4
def test_bracket(T):
	sc = "4"
	sv = "x"
	for i in range(10):
		sc = f"({sc})"
		sv = f"({sv})"

	assert "4" == T(f'<?print {sc}?>').renders()
	assert "4" == T(f'<?code x=4?><?print {sv}?>').renders()


@pytest.mark.ul4
def test_callfunc_args(T):
	assert "@(2013-01-07)" == T("<?print repr(date(2013, 1, 7))?>").renders()
	assert "@(2013-01-07)" == T("<?print repr(date(2013, 1, day=7))?>").renders()
	assert "@(2013-01-07)" == T("<?print repr(date(2013, month=1, day=7))?>").renders()
	assert "@(2013-01-07)" == T("<?print repr(date(year=2013, month=1, day=7))?>").renders()
	assert "@(2013-01-07)" == T("<?print repr(date(2013, *[1, 7]))?>").renders()
	assert "@(2013-01-07)" == T("<?print repr(date(*[2013, 1, 7]))?>").renders()
	assert "@(2013-01-07)" == T("<?print repr(date(year=2013, **{'month': 1, 'day': 7}))?>").renders()
	assert "@(2013-01-07)" == T("<?print repr(date(2013, *[1], **{'day': 7}))?>").renders()
	assert "@(2013-01-07)" == T("<?print repr(date(*[2013], *[1], *[7]))?>").renders()
	assert "@(2013-01-07)" == T("<?print repr(date(year=2013, **{'month': 1}, **{'day': 7}))?>").renders()

	with raises(duplicatekeywordargument):
		T("<?print repr(date(year=2013, year=2013))?>").renders()

	with raises(duplicatekeywordargument):
		T("<?print repr(date(year=2013, **{'year': 2013}))?>").renders()

	with raises(duplicatekeywordargument):
		T("<?print repr(date(**{'year': 2013}, **{'year': 2013}))?>").renders()


@pytest.mark.ul4
def test_function_now(T):
	now = str(datetime.datetime.now())

	assert now <= T("<?print now()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print now(1)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print now(1, 2)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print now(foo=1)?>").renders()


@pytest.mark.ul4
def test_function_today(T):
	today = str(datetime.date.today())
	result = T("<?print today()?>").renders()
	assert today <= result
	assert len(result) == 10

	with raises(argumentmismatchmessage):
		T("<?print today(1)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print today(foo=1)?>").renders()


@pytest.mark.ul4
def test_function_utcnow(T):
	utcnow = str(datetime.datetime.utcnow())

	# JS and Java only have milliseconds precision, but this shouldn't lead to problems here, as rendering the template takes longer than a millisecond
	assert utcnow <= T("<?print utcnow()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print utcnow(1)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print utcnow(foo=1)?>").renders()


@pytest.mark.ul4
def test_function_date(T):
	assert "@(2012-10-06)" == T("<?print repr(date(2012, 10, 6))?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "@(2012-10-06)" == T("<?print repr(date(year=2012, month=10, day=6))?>").renders()

	# Test mixed argument passing
	assert "@(2012-10-06)" == T("<?print repr(date(2012, *[10], **{'day': 6}))?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print date(2012, 10, 6, 12, 34, 56, 123456, 7890)?>").renders()


@pytest.mark.ul4
def test_function_datetime(T):
	assert "@(2012-10-06T)" == T("<?print repr(datetime(2012, 10, 6))?>").renders()
	assert "@(2012-10-06T12:00)" == T("<?print repr(datetime(2012, 10, 6, 12))?>").renders()
	assert "@(2012-10-06T12:34)" == T("<?print repr(datetime(2012, 10, 6, 12, 34))?>").renders()
	assert "@(2012-10-06T12:34:56)" == T("<?print repr(datetime(2012, 10, 6, 12, 34, 56))?>").renders()
	if T is not TemplatePHP:
		assert "@(2012-10-06T12:34:56.987000)" == T("<?print repr(datetime(2012, 10, 6, 12, 34, 56, 987000))?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "@(2012-10-06T12:34:56)" == T("<?print repr(datetime(year=2012, month=10, day=6, hour=12, minute=34, second=56, microsecond=0))?>").renders()

	# Test mixed argument passing
	assert "@(2012-10-06T12:34:56)" == T("<?print repr(datetime(2012, *[10], *[6], hour=12, **{'minute': 34}, **{'second': 56}))?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print datetime(2012, 10, 6, 12, 34, 56, 123456, 7890)?>").renders()


@pytest.mark.ul4
def test_function_timedelta(T):
	assert "1 day, 0:00:00" == T("<?print timedelta(1)?>").renders()
	assert "-1 day, 0:00:00" == T("<?print timedelta(-1)?>").renders()
	assert "2 days, 0:00:00" == T("<?print timedelta(2)?>").renders()
	assert "0:00:01" == T("<?print timedelta(0, 0, 1000000)?>").renders()
	assert "1 day, 0:00:00" == T("<?print timedelta(0, 0, 24*60*60*1000000)?>").renders()
	assert "1 day, 0:00:00" == T("<?print timedelta(0, 24*60*60)?>").renders()
	assert "12:00:00" == T("<?print timedelta(0.5)?>").renders()
	assert "0:00:00.500000" == T("<?print timedelta(0, 0.5)?>").renders()
	assert "0:00:00.500000" == T("<?print timedelta(0.5/(24*60*60))?>").renders()
	assert "-1 day, 12:00:00" == T("<?print timedelta(-0.5)?>").renders()
	assert "-1 day, 23:59:59.500000" == T("<?print timedelta(0, -0.5)?>").renders()
	assert "0:00:01" == T("<?print timedelta(0, 1)?>").renders()
	assert "0:01:00" == T("<?print timedelta(0, 60)?>").renders()
	assert "1:00:00" == T("<?print timedelta(0, 60*60)?>").renders()
	assert "1 day, 1:01:01.000001" == T("<?print timedelta(1, 60*60+60+1, 1)?>").renders()
	assert "0:00:00.000001" == T("<?print timedelta(0, 0, 1)?>").renders()
	assert "-1 day, 23:59:59" == T("<?print timedelta(0, -1)?>").renders()
	assert "-1 day, 23:59:59.999999" == T("<?print timedelta(0, 0, -1)?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "0:00:00.000001" == T("<?print timedelta(days=0, seconds=0, microseconds=1)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print timedelta(1, 2, 3, 4)?>").renders()


@pytest.mark.ul4
def test_function_monthdelta(T):
	assert "0 months" == T("<?print monthdelta()?>").renders()
	assert "2 months" == T("<?print monthdelta(2)?>").renders()
	assert "1 month" == T("<?print monthdelta(1)?>").renders()
	assert "-1 month" == T("<?print monthdelta(-1)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print monthdelta(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print monthdelta(months=1)?>").renders()


@pytest.mark.ul4
def test_function_random(T):
	assert "ok" == T("<?code r = random()?><?if r>=0 and r<1?>ok<?else?>fail<?end if?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print random(1)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print random(1, 2)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print random(foo=1)?>").renders()


@pytest.mark.ul4
def test_function_randrange(T):
	assert "ok" == T("<?code r = randrange(4)?><?if r>=0 and r<4?>ok<?else?>fail<?end if?>").renders()
	assert "ok" == T("<?code r = randrange(17, 23)?><?if r>=17 and r<23?>ok<?else?>fail<?end if?>").renders()
	assert "ok" == T("<?code r = randrange(17, 23, 2)?><?if r>=17 and r<23 and r%2?>ok<?else?>fail<?end if?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print randrange()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print randrange(stop=1)?>").renders()


@pytest.mark.ul4
def test_function_randchoice(T):
	assert "ok" == T("<?code r = randchoice('abc')?><?if r in 'abc'?>ok<?else?>fail<?end if?>").renders()
	assert "ok" == T("<?code s = [17, 23, 42]?><?code r = randchoice(s)?><?if r in s?>ok<?else?>fail<?end if?>").renders()
	assert "ok" == T("<?code s = #12345678?><?code sl = [0x12, 0x34, 0x56, 0x78]?><?code r = randchoice(s)?><?if r in sl?>ok<?else?>fail<?end if?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "ok" == T("<?code s = [17, 23, 42]?><?code r = randchoice(seq=s)?><?if r in s?>ok<?else?>fail<?end if?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print randchoice()?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "42" == T("<?print randchoice(seq=[42])?>").renders()


@pytest.mark.ul4
def test_function_xmlescape(T):
	assert "&lt;&lt;&gt;&gt;&amp;&#39;&quot;gurk" == T("<?print xmlescape(data)?>").renders(data='<<>>&\'"gurk')

	with raises(argumentmismatchmessage):
		T("<?print xmlescape()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print xmlescape(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print xmlescape(obj=data)?>").renders(data=42)


@pytest.mark.ul4
def test_function_csv(T):
	t = T("<?print csv(data)?>")

	assert "" == t.renders(data=None)
	assert "False" == t.renders(data=False)
	assert "True" == t.renders(data=True)
	assert "42" == t.renders(data=42)
	# no check for float
	assert "abc" == t.renders(data="abc")
	assert '"a,b,c"' == t.renders(data="a,b,c")
	assert '"a""b""c"' == t.renders(data='a"b"c')
	assert '"a\nb\nc"' == t.renders(data="a\nb\nc")

	with raises(argumentmismatchmessage):
		T("<?print csv()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print csv(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print csv(obj=data)?>").renders(data=42)


@pytest.mark.ul4
def test_function_asjson(T):
	t = T("<?print asjson(data)?>")

	assert "null" == t.renders(data=None)
	assert "false" == t.renders(data=False)
	assert "true" == t.renders(data=True)
	assert "42" == t.renders(data=42)
	# no check for float
	assert '"abc"' == t.renders(data="abc")
	assert '"\'"' == t.renders(data="'")
	assert '"\\\""' == t.renders(data='"')
	assert '[1, 2, 3]' == t.renders(data=[1, 2, 3])
	assert '[1, 2, 3]' == t.renders(data=PseudoList([1, 2, 3]))
	assert '{"one": 1}' == t.renders(data={"one": 1})
	assert '{"one": 1}' == t.renders(data=PseudoDict({"one": 1}))
	assert 'new ul4.Date_(2000, 2, 29)' == t.renders(data=datetime.date(2000, 2, 29))
	assert 'new Date(2000, 1, 29, 12, 34, 56, 987)' == t.renders(data=datetime.datetime(2000, 2, 29, 12, 34, 56, 987654))
	assert 'new ul4.TimeDelta(1, 1, 1)' == t.renders(data=datetime.timedelta(1, 1, 1))
	assert 'new ul4.MonthDelta(1)' == t.renders(data=misc.monthdelta(1))
	assert 'new ul4.Color(1, 2, 3, 4)' == t.renders(data=color.Color(1, 2, 3, 4))

	with raises(argumentmismatchmessage):
		T("<?print asjson()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print asjson(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print asjson(obj=data)?>").renders(data=42)


@pytest.mark.ul4
def test_function_fromjson(T):
	t = T("<?print repr(fromjson(data))?>")

	assert "None" == t.renders(data="null")
	assert "False" == t.renders(data="false")
	assert "True" == t.renders(data="true")
	assert "42" == t.renders(data="42")
	# no check for float
	assert t.renders(data='"abc"') in ('"abc"', "'abc'")
	assert '[1, 2, 3]' == t.renders(data="[1, 2, 3]")
	assert "{'one': 1}" == t.renders(data='{"one": 1}')

	with raises(argumentmismatchmessage):
		T("<?print fromjson()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print fromjson(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print fromjson(string=data)?>").renders(data="42")


@pytest.mark.ul4
def test_function_ul4on(T):
	t = T("<?print repr(fromul4on(asul4on(data)))?>")

	assert "None" == t.renders(data=None)
	assert "False" == t.renders(data=False)
	assert "True" == t.renders(data=True)
	assert "42" == t.renders(data=42)
	# no check for float
	assert t.renders(data="abc") in ('"abc"', "'abc'")
	assert '[1, 2, 3]' == t.renders(data=[1, 2, 3])
	assert t.renders(data={'one': 1}) in ('{"one": 1}', "{'one': 1}")

	# Explicitly check the real output for at least one example
	assert "i42" == T("<?print asul4on(42)?>").renders()

	# Test pretty printing
	expected = "L\n\ti1\n\ti2\n\ti3\n]\n"
	if issubclass(T, TemplateJavascript):
		expected = expected.lower()
	assert expected == T("<?print asul4on([1, 2, 3], '\\t')?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print asul4on()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print asul4on(1, 2, 3)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print fromul4on()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print fromul4on(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print asul4on(obj=42)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print fromul4on(dump='i42')?>").renders()


@pytest.mark.ul4
def test_function_str(T):
	t = T("<?print str(data)?>")

	assert "" == T("<?print str()?>").renders()
	assert "" == t.renders(data=None)
	assert "True" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "42" == t.renders(data=42)
	assert "4.2" == t.renders(data=4.2)
	assert "foo" == t.renders(data="foo")
	assert "2011-02-09 00:00" == t.renders(data=datetime.datetime(2011, 2, 9))
	assert "2011-02-09 12:34:56" == t.renders(data=datetime.datetime(2011, 2, 9, 12, 34, 56))
	if T is not TemplatePHP:
		assert "2011-02-09 12:34:56.987000" == t.renders(data=datetime.datetime(2011, 2, 9, 12, 34, 56, 987000))
	assert "0:00:00" == t.renders(data=datetime.timedelta())
	assert "1 day, 0:00:00" == t.renders(data=datetime.timedelta(1))
	assert "-1 day, 0:00:00" == t.renders(data=datetime.timedelta(-1))
	assert "2 days, 0:00:00" == t.renders(data=datetime.timedelta(2))
	assert "0:00:01" == t.renders(data=datetime.timedelta(0, 1))
	assert "0:01:00" == t.renders(data=datetime.timedelta(0, 60))
	assert "1:00:00" == t.renders(data=datetime.timedelta(0, 60*60))
	assert "1 day, 1:01:01.000001" == t.renders(data=datetime.timedelta(1, 60*60+60+1, 1))
	assert "0:00:00.000001" == t.renders(data=datetime.timedelta(0, 0, 1))
	assert "-1 day, 23:59:59" == t.renders(data=datetime.timedelta(0, -1))
	assert "-1 day, 23:59:59.999999" == t.renders(data=datetime.timedelta(0, 0, -1))

	assert "(x=17, y=@(2000-02-29))" == T("<?def f(x=17, y=@(2000-02-29))?><?return x+y?><?end def?><?print str(f.signature)?>").renders()
	# Javascript version doesn't have support for printing recursive data structures
	if T not in (TemplateJavascriptV8, TemplateJavascriptNode):
		assert "(bad=[...])" == T("<?code bad = []?><?code bad.append(bad)?><?def f(bad=bad)?><?end def?><?print str(f.signature)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print str(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print str(obj=data)?>").renders(data=42)


@pytest.mark.ul4
def test_function_bool(T):
	assert "False" == T("<?print bool()?>").renders()

	t = T("<?print bool(data)?>")
	assert "True" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=0)
	assert "True" == t.renders(data=42)
	assert "False" == t.renders(data=0.0)
	assert "True" == t.renders(data=42.5)
	assert "False" == t.renders(data="")
	assert "True" == t.renders(data="gurk")
	assert "False" == t.renders(data=[])
	assert "True" == t.renders(data=["gurk"])
	assert "False" == t.renders(data={})
	assert "True" == t.renders(data={"gurk": "hurz"})
	assert "True" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta())
	assert "True" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta())
	assert "True" == t.renders(data=misc.monthdelta(1))

	with raises(argumentmismatchmessage):
		T("<?print bool(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print bool(obj=data)?>").renders(data=42)


@pytest.mark.ul4
def test_function_list(T):
	with raises(argumentmismatchmessage):
		T("<?print list(1, 2)?>").renders()
	assert "[]" == T("<?print list()?>").renders()
	assert "[1, 2]" == T("<?print list(data)?>").renders(data=[1, 2])
	assert "g" == T("<?print list(data)[0]?>").renders(data="gurk")
	assert "gurk" == T("<?print list(data)[0]?>").renders(data={"gurk": "hurz"})
	if T is not TemplateJavascriptV8:
		assert "[1]" == T("<?print list(data)?>").renders(data={1: 2})
	assert "foo42" == T("<?code x = list(data.items())?><?print x[0][0]?><?print x[0][1]?>").renders(data={"foo": 42})
	assert "[0, 1, 2]" == T("<?print repr(list(range(3)))?>").renders()

	with raises(unknownkeywordargument):
		T("<?print list(iterable=data)[0]?>").renders(data="gurk")


@pytest.mark.ul4
def test_function_set(T):
	assert "{/}" == T("<?print set()?>").renders()
	assert T("<?print set(data)?>").renders(data=["1"]) in ("{'1'}", '{"1"}')
	if T is not TemplateJavascriptV8:
		assert "{1}" == T("<?print set(data)?>").renders(data={1: 2})
		assert "{1}" == T("<?print set(data)?>").renders(data=[1])
	assert T("<?print repr(set(str(i) for i in range(1)))?>").renders() in ("{'0'}", '{"0"}')

	with raises(argumentmismatchmessage):
		T("<?print set(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print set(iterable=data)?>").renders(data=["1"]) in ("{'1'}", '{"1"}')


@pytest.mark.ul4
def test_function_dict(T):
	assert "{}" == T("<?print dict()?>").renders()
	assert "{17: 23, 42: 73}" == T("<?print dict(data)?>").renders(data=[(17, 23), (42, 73)])
	assert "{'foo': 23, 'bar': 42}" == T("<?print dict({'foo': 17}, foo=23, bar=42)?>").renders()


@pytest.mark.ul4
def test_function_int(T):
	assert "0" == T("<?print int()?>").renders()
	assert "1" == T("<?print int(data)?>").renders(data=True)
	assert "0" == T("<?print int(data)?>").renders(data=False)
	assert "42" == T("<?print int(data)?>").renders(data=42)
	assert "4" == T("<?print int(data)?>").renders(data=4.2)
	assert "42" == T("<?print int(data)?>").renders(data="42")
	assert "66" == T("<?print int(data, 16)?>").renders(data="42")

	with raises(argumentmismatchmessage):
		T("<?print int(1, 2, 3)?>").renders()

	with raises("int\\(\\) argument must be a string, a bytes-like object or a (real )?number, not|int\\(\\) argument must be a string or a number|int\\(null\\) not supported|Can't convert null to int!"):
		T("<?print int(data)?>").renders(data=None)

	with raises("invalid literal for int|NumberFormatException"):
		T("<?print int(data)?>").renders(data="foo")

	with raises(unknownkeywordargument):
		T("<?print int(obj=data, base=None)?>").renders(data=42)


@pytest.mark.ul4
def test_function_float(T):
	t = T("<?print float(data)?>")

	assert "4.2" == t.renders(data=4.2)
	if T not in (TemplateJavascriptV8, TemplateJavascriptNode):
		assert "0.0" == T("<?print float()?>").renders()
		assert "1.0" == t.renders(data=True)
		assert "0.0" == t.renders(data=False)
		assert "42.0" == t.renders(data=42)
		assert "42.0" == t.renders(data="42")
	else:
		assert 0.0 == eval(T("<?print float()?>").renders())
		assert 1.0 == eval(t.renders(data=True))
		assert 0.0 == eval(t.renders(data=False))
		assert 42.0 == eval(t.renders(data=42))
		assert 42.0 == eval(t.renders(data="42"))

	with raises(argumentmismatchmessage):
		T("<?print float(1, 2, 3)?>").renders()

	with raises("float\\(\\) argument must be a string or a (real )?number|float\\(null\\) not supported|Can't convert null to float!"):
		t.renders(data=None)

	with raises(unknownkeywordargument):
		T("<?print float(x=data)?>").renders(data=42)


@pytest.mark.ul4
def test_module_color_function_Color(T):
	assert "#369" == T("<?print color.Color(51, 102, 153, 255)?>").renders()


@pytest.mark.ul4
def test_module_color_function_css(T):
	assert "#000" == T("<?print repr(color.css('black'))?>").renders()
	assert "#fff" == T("<?print repr(color.css('white'))?>").renders()
	assert "#123" == T("<?print repr(color.css('#123'))?>").renders()
	assert "#1234" == T("<?print repr(color.css('#1234'))?>").renders()
	assert "#123456" == T("<?print repr(color.css('#123456'))?>").renders()
	assert "#12345678" == T("<?print repr(color.css('#12345678'))?>").renders()
	assert "#136" == T("<?print repr(color.css('rgb(17, 20%, 40%)'))?>").renders()
	assert "#1369" == T("<?print repr(color.css('rgba(17, 20%, 40%, 0.6)'))?>").renders()
	assert "#1369" == T("<?print repr(color.css('rgba(17, 20%, 40%, 60%)'))?>").renders()
	assert "#123" == T("<?print repr(color.css('bad', #123))?>").renders()


@pytest.mark.ul4
def test_module_color_function_mix(T):
	assert "#aaa" == T("<?print repr(color.mix(#000, #fff, #fff))?>").renders()
	assert "#555" == T("<?print repr(color.mix(#000, #000, #fff))?>").renders()
	assert "#aaaa" == T("<?print repr(color.mix(#0000, #ffff, #ffff))?>").renders()
	assert "#aaa" == T("<?print repr(color.mix(#000, 2, #fff))?>").renders()
	assert "#12c" == T("<?print repr(color.mix(#f00, 2, #0f0, 12, #00f))?>").renders()


@pytest.mark.ul4
def test_function_len(T):
	t = T("<?print len(data)?>")

	assert "42" == t.renders(data=42*"?")
	assert "42" == t.renders(data=42*[None])
	assert "42" == t.renders(data=dict.fromkeys(range(42)))

	with raises(argumentmismatchmessage):
		T("<?print len()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print len(1, 2)?>").renders()

	with raises("has no len\\(\\)|len\\(.*\\) not supported"):
		t.renders(data=None)

	with raises("has no len\\(\\)|len\\(.*\\) not supported"):
		t.renders(data=True)

	with raises("has no len\\(\\)|len\\(.*\\) not supported"):
		t.renders(data=False)

	with raises("has no len\\(\\)|len\\(.*\\) not supported"):
		t.renders(data=42)

	with raises("has no len\\(\\)|len\\(.*\\) not supported"):
		t.renders(data=4.2)

	with raises(unknownkeywordargument):
		T("<?print len(sequence=data)?>").renders(data=42*"?")


@pytest.mark.ul4
def test_function_any(T):
	assert "False" == T("<?print any('')?>").renders()
	assert "True" == T("<?print any('foo')?>").renders()
	assert "True" == T("<?print any(i > 7 for i in range(10))?>").renders()
	assert "False" == T("<?print any(i > 17 for i in range(10))?>").renders()
	if T is not TemplateJavascriptV8:
		assert "False" == T("<?print any({None: 17, 0: 23})?>").renders()
		assert "True" == T("<?print any({None: 17, 0: 23, 42: 'foo'})?>").renders()
		assert "False" == T("<?print any({0: 17})?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print any()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print any(1, 2)?>").renders()

	with raises("is not iterable|any\\(.*\\) not supported"):
		T("<?print any(data)?>").renders(data=None)

	with raises(unknownkeywordargument):
		T("<?print any(iterable=(i > 17 for i in range(10)))?>").renders()


@pytest.mark.ul4
def test_function_all(T):
	assert "True" == T("<?print all('')?>").renders()
	assert "True" == T("<?print all('foo')?>").renders()
	assert "False" == T("<?print all(i < 7 for i in range(10))?>").renders()
	assert "True" == T("<?print all(i < 17 for i in range(10))?>").renders()
	if T is not TemplateJavascriptV8:
		assert "False" == T("<?print any({None: 17, 0: 23})?>").renders()
		assert "True" == T("<?print any({17: 23, 42: 'foo'})?>").renders()
		assert "False" == T("<?print any({0: 17})?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print all()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print all(1, 2)?>").renders()

	with raises("is not iterable|all\\(.*\\) not supported"):
		T("<?print all(data)?>").renders(data=None)

	with raises(unknownkeywordargument):
		T("<?print all(iterable=(i < 17 for i in range(10)))?>").renders()


@pytest.mark.ul4
def test_function_enumerate(T):
	t1 = T("<?for (i, value) in enumerate(data)?>(<?print value?>=<?print i?>)<?end for?>")
	t2 = T("<?for (i, value) in enumerate(data, 42)?>(<?print value?>=<?print i?>)<?end for?>")

	assert "(f=0)(o=1)(o=2)" == t1.renders(data="foo")
	assert "(foo=0)(bar=1)" == t1.renders(data=["foo", "bar"])
	assert "(foo=0)" == t1.renders(data=dict(foo=True))
	assert "" == t1.renders(data="")
	assert "(f=42)(o=43)(o=44)" == t2.renders(data="foo")

	# Make sure that the parameters have the same name in all implementations
	assert "(f=42)(o=43)(o=44)" == T("<?for (i, value) in enumerate(iterable=data, start=42)?>(<?print value?>=<?print i?>)<?end for?>").renders(data="foo")

	with raises(argumentmismatchmessage):
		T("<?print enumerate()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print enumerate(1, 2, 3)?>").renders()

	with raises("is not iterable|iter\\(.*\\) not supported"):
		t1.renders(data=None)

	with raises("is not iterable|iter\\(.*\\) not supported"):
		t1.renders(data=True)

	with raises("is not iterable|iter\\(.*\\) not supported"):
		t1.renders(data=False)

	with raises("is not iterable|iter\\(.*\\) not supported"):
		t1.renders(data=42)

	with raises("is not iterable|iter\\(.*\\) not supported"):
		t1.renders(data=4.2)


@pytest.mark.ul4
def test_function_enumfl(T):
	t1 = T("<?for (i, f, l, value) in enumfl(data)?><?if f?>[<?end if?>(<?print value?>=<?print i?>)<?if l?>]<?end if?><?end for?>")
	t2 = T("<?for (i, f, l, value) in enumfl(data, 42)?><?if f?>[<?end if?>(<?print value?>=<?print i?>)<?if l?>]<?end if?><?end for?>")
	assert "[(f=0)(o=1)(o=2)]" == t1.renders(data="foo")
	assert "[(foo=0)(bar=1)]" == t1.renders(data=["foo", "bar"])
	assert "[(foo=0)]" == t1.renders(data=dict(foo=True))
	assert "" == t1.renders(data="")
	assert "[(f=42)(o=43)(o=44)]" == t2.renders(data="foo")

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t1.renders(data=None)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t1.renders(data=True)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t1.renders(data=False)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t1.renders(data=42)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t1.renders(data=4.2)

	with raises(argumentmismatchmessage):
		T("<?print enumfl()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print enumfl(1, 2, 3)?>").renders()

	with raises(unknownkeywordargument):
		T("<?for (i, f, l, value) in enumfl(iterable=data, start=42)?><?if f?>[<?end if?>(<?print value?>=<?print i?>)<?if l?>]<?end if?><?end for?>").renders(data="foo")


@pytest.mark.ul4
def test_function_isfirstlast(T):
	t = T("<?for (f, l, value) in isfirstlast(data)?><?if f?>[<?end if?>(<?print value?>)<?if l?>]<?end if?><?end for?>")
	assert "[(f)(o)(o)]" == t.renders(data="foo")
	assert "[(foo)(bar)]" == t.renders(data=["foo", "bar"])
	assert "[(foo)]" == t.renders(data=dict(foo=True))
	assert "" == t.renders(data="")

	with raises(argumentmismatchmessage):
		T("<?print isfirstlast()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isfirstlast(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?for (f, l, value) in isfirstlast(iterable=data)?><?if f?>[<?end if?>(<?print value?>)<?if l?>]<?end if?><?end for?>").renders(data="foo")

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=None)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=True)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=False)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=42)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=4.2)


@pytest.mark.ul4
def test_function_isfirst(T):
	t = T("<?for (f, value) in isfirst(data)?><?if f?>[<?end if?>(<?print value?>)<?end for?>")
	assert "[(f)(o)(o)" == t.renders(data="foo")
	assert "[(foo)(bar)" == t.renders(data=["foo", "bar"])
	assert "[(foo)" == t.renders(data=dict(foo=True))
	assert "" == t.renders(data="")

	with raises(argumentmismatchmessage):
		T("<?print isfirst()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isfirst(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?for (f, value) in isfirst(iterable=data)?><?if f?>[<?end if?>(<?print value?>)<?end for?>").renders(data="foo")

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=None)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=True)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=False)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=42)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=4.2)


@pytest.mark.ul4
def test_function_islast(T):
	t = T("<?for (l, value) in islast(data)?>(<?print value?>)<?if l?>]<?end if?><?end for?>")

	assert "(f)(o)(o)]" == t.renders(data="foo")
	assert "(foo)(bar)]" == t.renders(data=["foo", "bar"])
	assert "(foo)]" == t.renders(data=dict(foo=True))
	assert "" == t.renders(data="")

	with raises(argumentmismatchmessage):
		T("<?print islast()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print islast(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?for (l, value) in islast(iterable=data)?>(<?print value?>)<?if l?>]<?end if?><?end for?>").renders(data="foo")

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=None)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=True)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=False)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=42)

	with raises("must be iterable|is not iterable|iter\\(.*\\) not supported"):
		t.renders(data=4.2)


@pytest.mark.ul4
def test_function_isundefined(T):
	t = T("<?print isundefined(data)?>")

	assert "True" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == T("<?print isundefined(repr)?>").renders()
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isundefined()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isundefined(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isundefined(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isdefined(T):
	t = T("<?print isdefined(data)?>")

	assert "False" == t.renders()
	assert "True" == t.renders(data=None)
	assert "True" == t.renders(data=True)
	assert "True" == t.renders(data=False)
	assert "True" == t.renders(data=42)
	assert "True" == t.renders(data=4.2)
	assert "True" == t.renders(data="foo")
	assert "True" == t.renders(data=datetime.date.today())
	assert "True" == t.renders(data=datetime.datetime.now())
	assert "True" == t.renders(data=datetime.timedelta(1))
	assert "True" == t.renders(data=misc.monthdelta(1))
	assert "True" == t.renders(data=())
	assert "True" == t.renders(data=[])
	assert "True" == t.renders(data=set())
	assert "True" == t.renders(data={})
	assert "True" == t.renders(data=ul4c.Template(""))
	assert "True" == T("<?print isdefined(repr)?>").renders()
	assert "True" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isdefined()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isdefined(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isdefined(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isnone(T):
	t = T("<?print isnone(data)?>")

	assert "False" == t.renders()
	assert "True" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print isnone(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isnone()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isnone(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isnone(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isbool(T):
	t = T("<?print isbool(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "True" == t.renders(data=True)
	assert "True" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print isbool(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isbool()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isbool(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isbool(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isint(T):
	t = T("<?print isint(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "True" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print isint(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isint()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isint(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isint(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isfloat(T):
	t = T("<?print isfloat(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "True" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print isfloat(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isfloat()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isfloat(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isfloat(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isstr(T):
	t = T("<?print isstr(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "True" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print isstr(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isstr()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isstr(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isstr(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isdate(T):
	t = T("<?print isdate(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "True" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print isdate(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isdate()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isdate(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isdate(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isdatetime(T):
	t = T("<?print isdatetime(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "True" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print isdate(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isdatetime()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isdatetime(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isdate(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_istimedelta(T):
	t = T("<?print istimedelta(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "True" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print istimedelta(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print istimedelta()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print istimedelta(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print istimedelta(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_ismonthdelta(T):
	t = T("<?print ismonthdelta(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "True" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print ismonthdelta(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print ismonthdelta()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print ismonthdelta(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print ismonthdelta(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_islist(T):
	t = T("<?print islist(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "True" == t.renders(data=())
	assert "True" == t.renders(data=[])
	assert "True" == t.renders(data=PseudoList([]))
	assert "False" == t.renders(data=set())
	if T is not TemplatePHP:
		assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print islist(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print islist()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print islist(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print islist(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isset(T):
	t = T("<?print isset(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "True" == t.renders(data=set())
	assert "False" == t.renders(data=PseudoList([]))
	if T is not TemplatePHP:
		assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print islist(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isset()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isset(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print islist(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isdict(T):
	t = T("<?print isdict(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	if T is not TemplatePHP:
		assert "False" == t.renders(data=())
		assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "True" == t.renders(data={})
	assert "True" == t.renders(data=PseudoDict({}))
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print isdict(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isdict()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isdict(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isdict(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_istemplate(T):
	t = T("<?print istemplate(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "True" == t.renders(data=ul4c.Template(""))
	assert "True" == T("<?def f?><?end def?><?print istemplate(f)?>").renders()
	assert "False" == T("<?print istemplate(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print istemplate()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print istemplate(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print istemplate(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isfunction(T):
	t = T("<?print isfunction(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "True" == t.renders(data=ul4c.Template(""))
	assert "True" == T("<?print isfunction(repr)?>").renders()
	assert "True" == T("<?def f?><?return 42?><?end def?><?print isfunction(f)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isfunction()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isfunction(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print istemplate(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_iscolor(T):
	t = T("<?print iscolor(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print iscolor(repr)?>").renders()
	assert "True" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print iscolor()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print iscolor(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print iscolor(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isexception(T):
	t = T("<?print isexception(data)?>")

	assert "False" == t.renders()
	assert "False" == t.renders(data=None)
	assert "False" == t.renders(data=True)
	assert "False" == t.renders(data=False)
	assert "False" == t.renders(data=42)
	assert "False" == t.renders(data=4.2)
	assert "False" == t.renders(data="foo")
	assert "False" == t.renders(data=datetime.date.today())
	assert "False" == t.renders(data=datetime.datetime.now())
	assert "False" == t.renders(data=datetime.timedelta(1))
	assert "False" == t.renders(data=misc.monthdelta(1))
	if t in (TemplatePython, TemplatePythonDump, TemplatePythonDumpS): # can't serialize exception in UL4ON
		assert "True" == t.renders(data=ValueError("broken"))
	assert "False" == t.renders(data=())
	assert "False" == t.renders(data=[])
	assert "False" == t.renders(data=set())
	assert "False" == t.renders(data={})
	assert "False" == t.renders(data=ul4c.Template(""))
	assert "False" == T("<?print isexception(repr)?>").renders()
	assert "False" == t.renders(data=color.red)

	with raises(argumentmismatchmessage):
		T("<?print isexception()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isexception(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isexception(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_isinstance(T):
	info = {
		"type(None)": [None],
		"bool": [True, False],
		"int": [42],
		"float": [42.5],
		"str": ["foo"],
		"date": [datetime.date.today()],
		"datetime": ["=now()"],
		"timedelta": [datetime.timedelta(1)],
		"monthdelta": [misc.monthdelta(1)],
		"list": [[]],
		"set": [set()],
		"dict": [{}],
		"ul4.Template": [ul4c.Template("<?print x?>")],
		"type(repr)": ["=repr"],
		"color.Color": [color.Color(0, 0, 0)]
	}

	for targettype in info:
		if targettype != "ul4.Template" or not issubclass(T, TemplateJavascript):
			for (checktype, values) in info.items():
				if checktype != "ul4.Template" or not issubclass(T, TemplateJavascript):
					output = str(checktype == targettype)

					for value in values:
						if isinstance(value, str) and value.startswith("="):
							source = f"<?print isinstance({value[1:]}, {targettype})?>"
							assert output == T(source).renders()
						else:
							source = f"<?print isinstance(value, {targettype})?>"
							assert output == T(source).renders(value=value)

	assert "True" == T("<?print isinstance('gurk', str)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isinstance()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isinstance(1)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print isinstance(1, 2, 3)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print isinstance(obj=42, cls=int)?>").renders()


@pytest.mark.ul4
def test_function_reprascii_none(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	assert "None" == t.renders(data=None)


@pytest.mark.ul4
def test_function_reprascii_bool(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	assert "True" == t.renders(data=True)
	assert "False" == t.renders(data=False)


@pytest.mark.ul4
def test_function_reprascii_int(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	assert "42" == t.renders(data=42)


@pytest.mark.ul4
def test_function_reprascii_float(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	assert 42.5 == eval(t.renders(data=42.5))


@pytest.mark.ul4
def test_function_reprascii_str(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	assert "'foo'" == t.renders(data="foo")
	assert "\"'\"" == t.renders(data="'")
	assert "'\"'" == t.renders(data="\"")
	assert "'\\'\"'" == t.renders(data="'\"")
	assert "'\\r'" == t.renders(data="\r")
	assert "'\\t'" == t.renders(data="\t")
	assert "'\\n'" == t.renders(data="\n")
	assert "'\\x00'" == t.renders(data="\x00") # category Cc
	assert "'\\x7f'" == t.renders(data="\x7f")
	assert "'\\x80'" == t.renders(data="\x80")
	assert "'\\x9f'" == t.renders(data="\x9f")
	assert "'\\xa0'" == t.renders(data="\xa0") # category Zs
	assert "'\\xad'" == t.renders(data="\xad") # category Cf
	if reprfunc == "ascii":
		assert "'\\xff'" == t.renders(data="\xff")
		assert "'\\u0100'" == t.renders(data="\u0100")
	else:
		assert "'\xff'" == t.renders(data="\xff")
		assert "'\u0100'" == t.renders(data="\u0100")
	assert "'\\u0378'" == t.renders(data="\u0378") # category Cn
	assert "'\\u2028'" == t.renders(data="\u2028") # category Zl
	assert "'\\u2029'" == t.renders(data="\u2029") # category Zp
	assert "'\\ud800'" == t.renders(data="\ud800") # category Cs
	assert "'\\ue000'" == t.renders(data="\ue000") # category Co
	if reprfunc == "ascii":
		assert "'\\u3042'" == t.renders(data="\u3042")
	else:
		assert "'\u3042'" == t.renders(data="\u3042")
	assert "'\\uffff'" == t.renders(data="\uffff")


@pytest.mark.ul4
def test_function_reprascii_list(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	assert [1, 2, 3] == eval(t.renders(data=[1, 2, 3]))
	if T is not TemplateJavascriptV8:
		assert [1, 2, 3] == eval(t.renders(data=(1, 2, 3)))


@pytest.mark.ul4
def test_function_reprascii_set(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	assert "{/}" == t.renders(data=set())
	assert "{'1'}" == t.renders(data={"1"})
	if T is not TemplateJavascriptV8:
		assert "{1}" == t.renders(data={1})


@pytest.mark.ul4
def test_function_reprascii_dict(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	assert "{}" == t.renders(data={})
	assert {"a": 1, "b": 2} == eval(t.renders(data={"a": 1, "b": 2}))


@pytest.mark.ul4
def test_function_reprascii_date(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	assert "@(2011-02-07)" == t.renders(data=datetime.date(2011, 2, 7))


@pytest.mark.ul4
def test_function_reprascii_datetime(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	if T is not TemplatePHP:
		assert "@(2011-02-07T12:34:56.123000)" == t.renders(data=datetime.datetime(2011, 2, 7, 12, 34, 56, 123000))
	assert "@(2011-02-07T12:34:56)" == t.renders(data=datetime.datetime(2011, 2, 7, 12, 34, 56))
	assert "@(2011-02-07T12:34)" == t.renders(data=datetime.datetime(2011, 2, 7, 12, 34))
	assert "@(2011-02-07T)" == t.renders(data=datetime.datetime(2011, 2, 7))


@pytest.mark.ul4
def test_function_reprascii_timedelta(T, reprfunc):
	t = T(f"<?print {reprfunc}(data)?>")

	assert t.renders(data=datetime.timedelta(1)) in {"timedelta(1)", "timedelta(days=1)"}
	assert t.renders(data=datetime.timedelta(0, 1)) in {"timedelta(0, 1)", "timedelta(seconds=1)"}
	assert t.renders(data=datetime.timedelta(0, 0, 1)) in {"timedelta(0, 0, 1)", "timedelta(microseconds=1)"}
	assert t.renders(data=datetime.timedelta(-1)) in {"timedelta(-1)", "timedelta(days=-1)"}
	assert t.renders(data=datetime.timedelta(0, -1)) in {"timedelta(-1, 86399)", "timedelta(days=-1, seconds=86399)"}
	assert t.renders(data=datetime.timedelta(0, 0, -1)) in {"timedelta(-1, 86399, 999999)", "timedelta(days=-1, seconds=86399, microseconds=999999)"}
	assert t.renders(data=datetime.timedelta(0.5)) in {"timedelta(0, 43200)", "timedelta(seconds=43200)"}
	assert t.renders(data=datetime.timedelta(0, 0.5)) in {"timedelta(0, 0, 500000)", "timedelta(microseconds=500000)"}
	assert t.renders(data=datetime.timedelta(-0.5)) in {"timedelta(-1, 43200)", "timedelta(days=-1, seconds=43200)"}
	assert t.renders(data=datetime.timedelta(0, -0.5)) in {"timedelta(-1, 86399, 500000)", "timedelta(days=-1, seconds=86399, microseconds=500000)"}


@pytest.mark.ul4
def test_function_reprascii_signature(T, reprfunc):
	output = T(f"<?def f(x=17, y=@(2000-02-29))?><?return x+y?><?end def?><?print {reprfunc}(f.signature)?>").renders()
	assert "(x=17, y=@(2000-02-29))" in output


@pytest.mark.ul4
def text_function_reprascii_badargs(T, reprfunc):
	with raises(argumentmismatchmessage):
		T(f"<?print {reprfunc}()?>").renders()

	with raises(argumentmismatchmessage):
		T(f"<?print {reprfunc}(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T(f"<?print {reprfunc}(obj=data)?>").renders(data=None)


@pytest.mark.ul4
def test_function_format_date(T):
	dt = datetime.date(2018, 9, 14)

	t2 = T("<?print format(data, fmt)?>")
	t3 = T("<?print format(data, fmt, lang)?>")

	assert "2018" == t2.renders(fmt="%Y", data=dt)
	assert "09" == t2.renders(fmt="%m", data=dt)
	assert "14" == t2.renders(fmt="%d", data=dt)
	assert "00" == t2.renders(fmt="%H", data=dt)
	assert "00" == t2.renders(fmt="%M", data=dt)
	assert "00" == t2.renders(fmt="%S", data=dt)
	assert "000000" == t2.renders(fmt="%f", data=dt)
	assert "Fri" == t2.renders(fmt="%a", data=dt)
	assert "Fri" == t3.renders(fmt="%a", data=dt, lang=None)
	assert "Fri" == t3.renders(fmt="%a", data=dt, lang="en")
	assert "Fr" == t3.renders(fmt="%a", data=dt, lang="de")
	assert "Fr" == t3.renders(fmt="%a", data=dt, lang="de_DE")
	assert "Friday" == t2.renders(fmt="%A", data=dt)
	assert "Friday" == t3.renders(fmt="%A", data=dt, lang=None)
	assert "Friday" == t3.renders(fmt="%A", data=dt, lang="en")
	assert "Freitag" == t3.renders(fmt="%A", data=dt, lang="de")
	assert "Freitag" == t3.renders(fmt="%A", data=dt, lang="de_DE")
	assert "Sep" == t2.renders(fmt="%b", data=dt)
	assert "Sep" == t3.renders(fmt="%b", data=dt, lang=None)
	assert "Sep" == t3.renders(fmt="%b", data=dt, lang="en")
	assert "Sep" == t3.renders(fmt="%b", data=dt, lang="de")
	assert "Sep" == t3.renders(fmt="%b", data=dt, lang="de_DE")
	assert "September" == t2.renders(fmt="%B", data=dt)
	assert "September" == t3.renders(fmt="%B", data=dt, lang=None)
	assert "September" == t3.renders(fmt="%B", data=dt, lang="en")
	assert "September" == t3.renders(fmt="%B", data=dt, lang="de")
	assert "September" == t3.renders(fmt="%B", data=dt, lang="de_DE")
	assert "257" == t2.renders(fmt="%j", data=dt)
	assert "36" == t2.renders(fmt="%U", data=dt)
	assert "5" == t2.renders(fmt="%w", data=dt)
	assert "37" == t2.renders(fmt="%W", data=dt)
	assert "18" == t2.renders(fmt="%y", data=dt)
	assert t2.renders(fmt="%c", data=dt) in {"Fri Sep 14 00:00:00 2018", "Fri 14 Sep 2018 00:00:00", "Fri Sep 14 00:00:00 AM 2018", "Fri 14 Sep 2018 00:00:00 AM"}
	assert "09/14/2018" == t2.renders(fmt="%x", data=dt)
	assert "09/14/2018" == t3.renders(fmt="%x", data=dt, lang=None)
	assert "09/14/2018" == t3.renders(fmt="%x", data=dt, lang="en")
	assert "14.09.2018" == t3.renders(fmt="%x", data=dt, lang="de")
	assert "14.09.2018" == t3.renders(fmt="%x", data=dt, lang="de_DE")
	assert t2.renders(fmt="%X", data=dt) in {"00:00:00", "00:00:00 AM"}
	assert t3.renders(fmt="%X", data=dt, lang=None) in {"00:00:00", "00:00:00 AM"}
	assert t3.renders(fmt="%X", data=dt, lang="en") in {"00:00:00", "00:00:00 AM"}
	assert "00:00:00" == t3.renders(fmt="%X", data=dt, lang="de")
	assert "00:00:00" == t3.renders(fmt="%X", data=dt, lang="de_DE")
	assert "%" == t2.renders(fmt="%%", data=dt)


@pytest.mark.ul4
def test_function_format_datetime(T):
	dt = datetime.datetime(2011, 1, 25, 13, 34, 56, 987000)

	t2 = T("<?print format(data, fmt)?>")
	t3 = T("<?print format(data, fmt, lang)?>")

	assert "2011" == t2.renders(fmt="%Y", data=dt)
	assert "01" == t2.renders(fmt="%m", data=dt)
	assert "25" == t2.renders(fmt="%d", data=dt)
	assert "13" == t2.renders(fmt="%H", data=dt)
	assert "34" == t2.renders(fmt="%M", data=dt)
	assert "56" == t2.renders(fmt="%S", data=dt)
	assert "987000" == t2.renders(fmt="%f", data=dt)
	assert "Tue" == t2.renders(fmt="%a", data=dt)
	assert "Tue" == t3.renders(fmt="%a", data=dt, lang=None)
	assert "Tue" == t3.renders(fmt="%a", data=dt, lang="en")
	assert "Di" == t3.renders(fmt="%a", data=dt, lang="de")
	assert "Di" == t3.renders(fmt="%a", data=dt, lang="de_DE")
	assert "Tuesday" == t2.renders(fmt="%A", data=dt)
	assert "Tuesday" == t3.renders(fmt="%A", data=dt, lang=None)
	assert "Tuesday" == t3.renders(fmt="%A", data=dt, lang="en")
	assert "Dienstag" == t3.renders(fmt="%A", data=dt, lang="de")
	assert "Dienstag" == t3.renders(fmt="%A", data=dt, lang="de_DE")
	assert "Jan" == t2.renders(fmt="%b", data=dt)
	assert "Jan" == t3.renders(fmt="%b", data=dt, lang=None)
	assert "Jan" == t3.renders(fmt="%b", data=dt, lang="en")
	assert "Jan" == t3.renders(fmt="%b", data=dt, lang="de")
	assert "Jan" == t3.renders(fmt="%b", data=dt, lang="de_DE")
	assert "January" == t2.renders(fmt="%B", data=dt)
	assert "January" == t3.renders(fmt="%B", data=dt, lang=None)
	assert "January" == t3.renders(fmt="%B", data=dt, lang="en")
	assert "Januar" == t3.renders(fmt="%B", data=dt, lang="de")
	assert "Januar" == t3.renders(fmt="%B", data=dt, lang="de_DE")
	assert "01" == t2.renders(fmt="%I", data=dt)
	assert "025" == t2.renders(fmt="%j", data=dt)
	assert "PM" == t2.renders(fmt="%p", data=dt)
	assert "04" == t2.renders(fmt="%U", data=dt)
	assert "2" == t2.renders(fmt="%w", data=dt)
	assert "04" == t2.renders(fmt="%W", data=dt)
	assert "11" == t2.renders(fmt="%y", data=dt)
	assert t2.renders(fmt="%c", data=dt) in {"Tue Jan 25 13:34:56 2011", "Tue 25 Jan 2011 13:34:56", "Tue Jan 25 01:34:56 PM 2011", "Tue 25 Jan 2011 01:34:56 PM"}
	assert "01/25/2011" == t2.renders(fmt="%x", data=dt)
	assert "01/25/2011" == t3.renders(fmt="%x", data=dt, lang=None)
	assert "01/25/2011" == t3.renders(fmt="%x", data=dt, lang="en")
	assert "25.01.2011" == t3.renders(fmt="%x", data=dt, lang="de")
	assert "25.01.2011" == t3.renders(fmt="%x", data=dt, lang="de_DE")
	assert t2.renders(fmt="%X", data=dt) in {"13:34:56", "01:34:56 PM"}
	assert t3.renders(fmt="%X", data=dt, lang=None) in {"13:34:56", "01:34:56 PM"}
	assert t3.renders(fmt="%X", data=dt, lang="en") in {"13:34:56", "01:34:56 PM"}
	assert "13:34:56" == t3.renders(fmt="%X", data=dt, lang="de")
	assert "13:34:56" == t3.renders(fmt="%X", data=dt, lang="de_DE")
	assert "%" == t2.renders(fmt="%%", data=dt)


@pytest.mark.ul4
def test_function_format_int(T):
	t = T("<?print format(data, fmt)?>")

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
		assert format(42, f) == t.renders(data=42, fmt=f)
		if "c" not in f:
			assert format(-42, f) == t.renders(data=-42, fmt=f)
	assert format(True, "05") == t.renders(data=True, fmt="05")


@pytest.mark.ul4
def test_function_format_kwargs(T):
	assert "42" == T("<?print format(obj=data, fmt=fmt, lang=lang)?>").renders(fmt="", data=42, lang="de")


@pytest.mark.ul4
def test_function_chr(T):
	t = T("<?print chr(data)?>")

	assert "\x00" == t.renders(data=0)
	assert "a" == t.renders(data=ord("a"))
	assert "\u20ac" == t.renders(data=0x20ac)

	with raises(argumentmismatchmessage):
		T("<?print chr()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print chr(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print chr(i=data)?>").renders(data=0)


@pytest.mark.ul4
def test_function_ord(T):
	t = T("<?print ord(data)?>")

	assert "0" == t.renders(data="\x00")
	assert str(ord("a")) == t.renders(data="a")
	assert str(0x20ac) == t.renders(data="\u20ac")

	with raises(argumentmismatchmessage):
		T("<?print ord()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print ord(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print ord(c=data)?>").renders(data="\x00")


@pytest.mark.ul4
def test_function_hex(T):
	t = T("<?print hex(data)?>")

	assert "0x0" == t.renders(data=0)
	assert "0xff" == t.renders(data=0xff)
	assert "0xffff" == t.renders(data=0xffff)
	assert "-0xffff" == t.renders(data=-0xffff)

	with raises(argumentmismatchmessage):
		T("<?print hex()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print hex(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print hex(number=data)?>").renders(data=0)


@pytest.mark.ul4
def test_function_oct(T):
	t = T("<?print oct(data)?>")

	assert "0o0" == t.renders(data=0)
	assert "0o77" == t.renders(data=0o77)
	assert "0o7777" == t.renders(data=0o7777)
	assert "-0o7777" == t.renders(data=-0o7777)

	with raises(argumentmismatchmessage):
		T("<?print oct()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print oct(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print oct(number=data)?>").renders(data=0)


@pytest.mark.ul4
def test_function_bin(T):
	t = T("<?print bin(data)?>")

	assert "0b0" == t.renders(data=0b0)
	assert "0b11" == t.renders(data=0b11)
	assert "-0b1111" == t.renders(data=-0b1111)

	with raises(argumentmismatchmessage):
		T("<?print bin()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print bin(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print bin(number=data)?>").renders(data=0)


@pytest.mark.ul4
def test_function_abs(T):
	t = T("<?print abs(data)?>")

	assert "0" == t.render(data=0)
	assert "42" == t.render(data=42)
	assert "42" == t.render(data=-42)
	assert "1 month" == t.render(data=misc.monthdelta(-1))
	assert "1 day, 0:00:01.000001" == t.render(data=datetime.timedelta(-1, -1, -1))

	with raises(argumentmismatchmessage):
		T("<?print abs()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print abs(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print abs(number=1)?>").renders()


@pytest.mark.ul4
def test_function_sorted(T):
	t = T("<?for i in sorted(data)?><?print i?><?end for?>")

	assert "gkru" == t.renders(data="gurk")
	assert "24679" == t.renders(data="92746")
	assert "172342" == t.renders(data=(42, 17, 23))
	assert "012" == t.renders(data={0: "zero", 1: "one", 2: "two"})

	# Test reverse argument
	assert "urkg" == T("<?for i in sorted(data, reverse=True)?><?print i?><?end for?>").renders(data="gurk")

	# Test key function
	assert "0;31;62;93;24;55;86;17;48;79;" == T("<?def key(v)?><?return v % 10?><?end def?><?for i in sorted(data, key)?><?print i?>;<?end for?>").renders(data=[0, 17, 24, 31, 48, 55, 62, 79, 86, 93])
	# Stability
	assert "20;10;0;31;41;51;72;62;82;" == T("<?def key(v)?><?return v % 10?><?end def?><?for i in sorted(data, key)?><?print i?>;<?end for?>").renders(data=[72, 31, 20, 62, 41, 10, 0, 82, 51])
	# reverse=True does not invert the runs of items that compare equal
	assert "72;62;82;31;41;51;20;10;0;" == T("<?def key(v)?><?return v % 10?><?end def?><?for i in sorted(data, key, True)?><?print i?>;<?end for?>").renders(data=[72, 31, 20, 62, 41, 10, 0, 82, 51])

	with raises(argumentmismatchmessage):
		T("<?print sorted()?>").renders()

	with raises(unknownkeywordargument):
		T("<?print sorted(iterable='123')?>").renders()

	with raises(unknownkeywordargument):
		T("<?print sorted(iterable='bca', reverse=True)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print sorted(iterable=data, key=str)?>").renders()


@pytest.mark.ul4
def test_function_range(T):
	t1 = T("<?for i in range(data)?><?print i?>;<?end for?>")
	t2 = T("<?for i in range(data[0], data[1])?><?print i?>;<?end for?>")
	t3 = T("<?for i in range(data[0], data[1], data[2])?><?print i?>;<?end for?>")

	assert "" == t1.renders(data=-10)
	assert "" == t1.renders(data=0)
	assert "0;" == t1.renders(data=1)
	assert "0;1;2;3;4;" == t1.renders(data=5)
	assert "" == t2.renders(data=[0, -10])
	assert "" == t2.renders(data=[0, 0])
	assert "0;1;2;3;4;" == t2.renders(data=[0, 5])
	assert "-5;-4;-3;-2;-1;0;1;2;3;4;" == t2.renders(data=[-5, 5])
	assert "" == t3.renders(data=[0, -10, 1])
	assert "" == t3.renders(data=[0, 0, 1])
	assert "0;2;4;6;8;" == t3.renders(data=[0, 10, 2])
	assert "" == t3.renders(data=[0, 10, -2])
	assert "10;8;6;4;2;" == t3.renders(data=[10, 0, -2])
	assert "" == t3.renders(data=[10, 0, 2])

	with raises(argumentmismatchmessage):
		T("<?print range()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print range(1, 2, 3, 4)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print range(stop=10)?>").renders()


@pytest.mark.ul4
def test_function_slice(T):
	t2 = T("<?for i in slice(data[0], data[1])?><?print i?>;<?end for?>")
	t3 = T("<?for i in slice(data[0], data[1], data[2])?><?print i?>;<?end for?>")
	t4 = T("<?for i in slice(data[0], data[1], data[2], data[3])?><?print i?>;<?end for?>")

	assert "g;u;r;k;" == t2.renders(data=("gurk", None))
	assert "g;u;" == t2.renders(data=("gurk", 2))
	assert "u;r;" == t3.renders(data=("gurk", 1, 3))
	assert "u;r;k;" == t3.renders(data=("gurk", 1, None))
	assert "g;u;" == t3.renders(data=("gurk", None, 2))
	assert "u;u;" == t4.renders(data=("gurkgurk", 1, 6, 4))
	assert "u;k;u;k;u;k;" == t4.renders(data=("gurkgurkgurk", 1, None, 2))

	with raises(argumentmismatchmessage):
		T("<?print slice(1)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print slice(1, 2, 3, 4, 5)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print slice('gurk', stop=10)?>").renders()


@pytest.mark.ul4
def test_function_urlquote(T):
	assert "gurk" == T("<?print urlquote('gurk')?>").renders()
	assert "%3C%3D%3E%20%2B%20%3F" == T("<?print urlquote('<=> + ?')?>").renders()
	assert "%7F%C3%BF%EF%BF%BF" == T("<?print urlquote('\u007f\u00ff\uffff')?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "gurk" == T("<?print urlquote(string='gurk')?>").renders()


@pytest.mark.ul4
def test_function_urlunquote(T):
	assert "gurk" == T("<?print urlunquote('gurk')?>").renders()
	assert "<=> + ?" == T("<?print urlunquote('%3C%3D%3E%20%2B%20%3F')?>").renders()
	assert "\u007f\u00ff\uffff" == T("<?print urlunquote('%7F%C3%BF%EF%BF%BF')?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "gurk" == T("<?print urlunquote(string='gurk')?>").renders()


@pytest.mark.ul4
def test_function_zip(T):
	t0 = T("<?for i in zip()?><?print i?>;<?end for?>")
	t1 = T("<?for (ix, ) in zip(x)?><?print ix?>;<?end for?>")
	t2 = T("<?for (ix, iy) in zip(x, y)?><?print ix?>-<?print iy?>;<?end for?>")
	t3 = T("<?for (ix, iy, iz) in zip(x, y, z)?><?print ix?>-<?print iy?>+<?print iz?>;<?end for?>")

	assert "" == t0.renders()
	assert "1;2;" == t1.renders(x=[1, 2])
	assert "" == t2.renders(x=[], y=[])
	assert "1-3;2-4;" == t2.renders(x=[1, 2], y=[3, 4])
	assert "1-4;2-5;" == t2.renders(x=[1, 2, 3], y=[4, 5])
	assert "" == t3.renders(x=[], y=[], z=[])
	assert "1-3+5;2-4+6;" == t3.renders(x=[1, 2], y=[3, 4], z=[5, 6])
	assert "1-4+6;" == t3.renders(x=[1, 2, 3], y=[4, 5], z=[6])

	with raises(unknownkeywordargument):
		T("<?print zip(iterables='gurk')?>").renders()


@pytest.mark.ul4
def test_function_type(T):
	t = T("<?print type(x)?>")

	assert t.renders() in {"<type undefinedvariable>", "<type undefined>"}
	assert "<type None>" == t.renders(x=None)
	assert "<type bool>" == t.renders(x=False)
	assert "<type bool>" == t.renders(x=True)
	assert "<type int>" == t.renders(x=42)
	assert "<type float>" == t.renders(x=4.2)
	assert "<type str>" == t.renders(x="foo")
	assert "<type date>" == t.renders(x=datetime.date.today())
	assert "<type datetime>" == t.renders(x=datetime.datetime.now())
	assert "<type timedelta>" == t.renders(x=datetime.timedelta())
	assert "<type monthdelta>" == t.renders(x=misc.monthdelta())
	assert "<type list>" == t.renders(x=(1, 2))
	assert "<type list>" == t.renders(x=[1, 2])
	assert "<type list>" == t.renders(x=PseudoList([1, 2]))
	assert "<type dict>" == t.renders(x={1: 2})
	assert "<type dict>" == t.renders(x=PseudoDict({1: 2}))
	assert "<type ul4.Template>" == t.renders(x=ul4c.Template(""))
	assert "<type ul4.TemplateClosure>" == T("<?def t?><?end def?><?print type(t)?>").renders()
	assert "<type function>" == T("<?print type(repr)?>").renders()
	assert "<type color.Color>" == T("<?print type(#000)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print type()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print type(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print type(obj=x)?>").renders(x=None)


@pytest.mark.ul4
def test_function_reversed(T):
	t = T("<?for i in reversed(x)?>(<?print i?>)<?end for?>")

	assert "(3)(2)(1)" == t.renders(x="123")
	assert "(3)(2)(1)" == t.renders(x=[1, 2, 3])
	assert "(3)(2)(1)" == t.renders(x=(1, 2, 3))

	with raises(argumentmismatchmessage):
		T("<?print reversed()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print reversed(1, 2)?>").renders()

	with raises(unknownkeywordargument):
		T("<?code reversed(sequence=x)?>").renders(x=(1, 2, 3))


@pytest.mark.ul4
def test_function_min(T):
	assert "1" == T("<?print min('123')?>").renders()
	assert "1" == T("<?print min(1, 2, 3)?>").renders()
	assert "0" == T("<?print min(0, False, 1, True)?>").renders()
	assert "False" == T("<?print min(False, 0, True, 1)?>").renders()
	assert "False" == T("<?print min([False, 0, True, 1])?>").renders()

	assert "42" == T("<?print min([], default=42)?>").renders()
	assert "hinz" == T("<?def key(s)?><?return s[1]?><?end def?><?print min(['gurk', 'hurz', 'hinz', 'kunz'], key=key)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print min()?>").renders()

	with raises(unknownkeywordargument):
		T("<?code min(args='gurk')?>").renders()

	with raises("empty sequence"):
		T("<?print min([])?>").renders()


@pytest.mark.ul4
def test_function_max(T):
	assert "3" == T("<?print max('123')?>").renders()
	assert "3" == T("<?print max(1, 2, 3)?>").renders()
	assert "1" == T("<?print max(0, False, 1, True)?>").renders()
	assert "True" == T("<?print max(False, 0, True, 1)?>").renders()
	assert "True" == T("<?print max([False, 0, True, 1])?>").renders()

	assert "42" == T("<?print max([], default=42)?>").renders()
	assert "hurz" == T("<?def key(s)?><?return s[2:]?><?end def?><?print max(['gurk', 'hurz', 'hinz', 'kunz'], key=key)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print max()?>").renders()

	with raises(unknownkeywordargument):
		T("<?code max(args='gurk')?>").renders()

	with raises("empty sequence"):
		T("<?print max([])?>").renders()


@pytest.mark.ul4
def test_function_sum(T):
	assert "0" == T("<?print sum([])?>").renders()
	assert "6" == T("<?print sum([1, 2, 3])?>").renders()
	assert "12" == T("<?print sum([1, 2, 3], 6)?>").renders()
	assert "5050" == T("<?print sum(range(101))?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print sum()?>").renders()

	msg = unknownkeywordargument[1:-1]
	msg = f"(sum\\(\\) takes at least 1 positional argument \\(0 given\\)|{msg})"

	with raises(msg):
		T("<?print sum(iterable=[1, 2, 3], start=6)?>").renders()


@pytest.mark.ul4
def test_function_first(T):
	assert "g" == T("<?print first('gurk')?>").renders()
	assert "None" == T("<?print repr(first(''))?>").renders()
	assert "x" == T("<?print first('', 'x')?>").renders()

	with raises(unknownkeywordargument):
		T("<?print first(iterable='', default='x')?>").renders()


@pytest.mark.ul4
def test_function_last(T):
	assert "k" == T("<?print last('gurk')?>").renders()
	assert "None" == T("<?print repr(last(''))?>").renders()
	assert "x" == T("<?print last('', 'x')?>").renders()

	with raises(unknownkeywordargument):
		T("<?print last(iterable='', default='x')?>").renders()


@pytest.mark.ul4
def test_function_rgb(T):
	assert "#369" == T("<?print repr(rgb(0.2, 0.4, 0.6))?>").renders()
	assert "#369c" == T("<?print repr(rgb(0.2, 0.4, 0.6, 0.8))?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "#369c" == T("<?print repr(rgb(r=0.2, g=0.4, b=0.6, a=0.8))?>").renders()


@pytest.mark.ul4
def test_function_hls(T):
	assert "#fff" == T("<?print repr(hls(0, 1, 0))?>").renders()
	assert "#fff0" == T("<?print repr(hls(0, 1, 0, 0))?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "#fff0" == T("<?print repr(hls(h=0, l=1, s=0, a=0))?>").renders()


@pytest.mark.ul4
def test_function_hsv(T):
	assert "#fff" == T("<?print repr(hsv(0, 0, 1))?>").renders()
	assert "#fff0" == T("<?print repr(hsv(0, 0, 1, 0))?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "#fff0" == T("<?print repr(hsv(h=0, s=0, v=1, a=0))?>").renders()


@pytest.mark.ul4
def test_function_md5(T):
	result = "acbd18db4cc2f85cedef654fccc4a4d8"
	assert result == T("<?print md5('foo')?>").renders()

	with raises(unknownkeywordargument):
		assert result == T("<?print md5(string='foo')?>").renders()


@pytest.mark.ul4
def test_function_scrypt(T):
	if not issubclass(T, TemplateJavascript):
		result = "468b5b132508a02f1868576247763abed96ac41db9287d21c8b5379ad71fbe2a2bf77fd3a738dda0572e0761938149f5b91b58d2ff87b9482680540606a710943d2a69f66fe89e2693361300c914b42c24abb29a80ef8840b6a0b67c96e5960292cc38cd959017931fe28e2a921107ade2f845e09a7590e9bf6755bd04ec51af"
		assert result == T("<?print scrypt('foo', 'bar')?>").renders()

		with raises(unknownkeywordargument):
			assert result == T("<?print scrypt(string='foo', salt='bar')?>").renders()


@pytest.mark.ul4
def test_function_round(T):
	assert "True" == T("<?print round(42) == 42?>").renders()
	assert "True" == T("<?print round(42, 1) == 42?>").renders()
	assert "True" == T("<?print round(42, -1) == 40?>").renders()

	assert "True" == T("<?print round(42.4) == 42?>").renders()
	assert "True" == T("<?print round(42.6) == 43?>").renders()
	assert "True" == T("<?print round(-42.4) == -42?>").renders()
	assert "True" == T("<?print round(-42.6) == -43?>").renders()
	assert "<type int>" == T("<?print type(round(42.5))?>").renders()

	assert "True" == T("<?print round(42.4, -1) == 40?>").renders()
	assert "True" == T("<?print round(46.2, -1) == 50?>").renders()
	assert "True" == T("<?print round(-42.4, -1) == -40?>").renders()
	assert "True" == T("<?print round(-46.2, -1) == -50?>").renders()
	assert "<type int>" == T("<?print type(round(42.5, -1))?>").renders()

	assert "True" == T("<?print round(42.987, 1) == 43.0?>").renders()
	assert "True" == T("<?print round(42.123, 1) == 42.1?>").renders()
	assert "True" == T("<?print round(-42.987, 1) == -43.0?>").renders()
	assert "True" == T("<?print round(-42.123, 1) == -42.1?>").renders()
	# assert "True" == T("<?print round(42.589, 2) == 42.59?>").renders()
	assert "True" == T("<?print round(42.123, 2) == 42.12?>").renders()
	# assert "True" == T("<?print round(-42.589, 2) == -42.59?>").renders()
	assert "True" == T("<?print round(-42.123, 2) == -42.12?>").renders()
	assert "<type float>" == T("<?print type(round(42.5, 1))?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "True" == T("<?print round(-42.123, digits=2) == -42.12?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print round()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print round(1, 2, 3)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print round(number=-42.123, digits=2)?>").renders()


@pytest.mark.ul4
def test_function_floor(T):
	assert "42" == T("<?print floor(x)?>").renders(x=42)
	# Javascript can't distinguish between int and float, so test the value not the output
	assert "True" == T("<?print floor(x, 1) == x?>").renders(x=42)
	assert "40" == T("<?print floor(x, -1)?>").renders(x=40)
	assert "40" == T("<?print floor(x, -1)?>").renders(x=49)
	assert "-50" == T("<?print floor(x, -1)?>").renders(x=-41)
	assert "-50" == T("<?print floor(x, -1)?>").renders(x=-50)
	assert "400" == T("<?print floor(x, -2)?>").renders(x=400)
	assert "400" == T("<?print floor(x, -2)?>").renders(x=499)
	assert "-500" == T("<?print floor(x, -2)?>").renders(x=-401)
	assert "-500" == T("<?print floor(x, -2)?>").renders(x=-500)
	assert "<type int>" == T("<?print type(floor(x))?>").renders(x=42)
	assert "<type int>" == T("<?print type(floor(x, 1))?>").renders(x=42)
	assert "<type int>" == T("<?print type(floor(x, -1))?>").renders(x=42)

	if not issubclass(T, TemplateJavascript):
		base = 10 ** 30
		assert str(base) == T(f"<?print floor(x, -30)?>").renders(x=base)
		assert str(base) == T(f"<?print floor(2*x-1, -30)?>").renders(x=base)
		assert str(2*base) == T(f"<?print floor(2*x, -30)?>").renders(x=base)
		assert str(-base) == T(f"<?print floor(-x, -30)?>").renders(x=base)
		assert str(-2*base) == T(f"<?print floor(-x-1, -30)?>").renders(x=base)
		assert str(-2*base) == T(f"<?print floor(-2*x, -30)?>").renders(x=base)
		assert str(-2*base) == T(f"<?print floor(-2*x+1, -30)?>").renders(x=base)
		# This checks integer overflow in the Java implementation
		assert "-10000000000" == T(f"<?print floor(x, -10)?>").renders(x=-2147483648)
		# This checks long overflow in the Java implementation
		assert "-10000000000000000000" == T(f"<?print floor(x, -19)?>").renders(x=-9223372036854775808)

	assert "True" == T("<?print floor(42.6) == 42?>").renders()
	assert "True" == T("<?print floor(-42.4) == -43?>").renders()
	assert "True" == T("<?print floor(-42.6) == -43?>").renders()
	assert "<type int>" == T("<?print type(floor(42.5))?>").renders()

	assert "True" == T("<?print floor(42.4, -1) == 40?>").renders()
	assert "True" == T("<?print floor(46.2, -1) == 40?>").renders()
	assert "True" == T("<?print floor(-42.4, -1) == -50?>").renders()
	assert "True" == T("<?print floor(-46.2, -1) == -50?>").renders()
	assert "<type int>" == T("<?print type(floor(42.5, -1))?>").renders()

	assert "True" == T("<?print floor(42.987, 1) == 42.9?>").renders()
	assert "True" == T("<?print floor(42.123, 1) == 42.1?>").renders()
	assert "True" == T("<?print floor(-42.987, 1) == -43.0?>").renders()
	assert "True" == T("<?print floor(-42.123, 1) == -42.2?>").renders()
	#
	assert "True" == T("<?print floor(42.589, 2) == 42.58?>").renders()
	assert "True" == T("<?print floor(42.123, 2) == 42.12?>").renders()
	#
	assert "True" == T("<?print math.isclose(floor(-42.589, 2), -42.59)?>").renders()
	assert "True" == T("<?print floor(-42.123, 2) == -42.13?>").renders()
	assert "<type float>" == T("<?print type(floor(42.5, 1))?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "True" == T("<?print floor(-42.123, digits=2) == -42.13?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print floor()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print floor(1, 2, 3)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print floor(number=-42.123, digits=2)?>").renders()


@pytest.mark.ul4
def test_function_ceil(T):
	assert "42" == T("<?print ceil(x)?>").renders(x=42)
	# Javascript can't distinguish between int and float, so test the value not the output
	assert "True" == T("<?print ceil(x, 1) == x?>").renders(x=42)
	assert "40" == T("<?print ceil(x, -1)?>").renders(x=40)
	assert "50" == T("<?print ceil(x, -1)?>").renders(x=41)
	assert "-40" == T("<?print ceil(x, -1)?>").renders(x=-49)
	assert "-50" == T("<?print ceil(x, -1)?>").renders(x=-50)
	assert "400" == T("<?print ceil(x, -2)?>").renders(x=400)
	assert "500" == T("<?print ceil(x, -2)?>").renders(x=499)
	assert "-400" == T("<?print ceil(x, -2)?>").renders(x=-401)
	assert "-500" == T("<?print ceil(x, -2)?>").renders(x=-500)
	assert "<type int>" == T("<?print type(ceil(x))?>").renders(x=42)
	assert "<type int>" == T("<?print type(ceil(x, 1))?>").renders(x=42)
	assert "<type int>" == T("<?print type(ceil(x, -1))?>").renders(x=42)

	if not issubclass(T, TemplateJavascript):
		base = 10 ** 30
		assert str(base) == T(f"<?print ceil(x, -30)?>").renders(x=base)
		assert str(2*base) == T(f"<?print ceil(x+1, -30)?>").renders(x=base)
		assert str(2*base) == T(f"<?print ceil(2*x, -30)?>").renders(x=base)
		assert str(-base) == T(f"<?print ceil(-x, -30)?>").renders(x=base)
		assert "0" == T(f"<?print ceil(-x+1, -30)?>").renders(x=base)
		assert str(-2*base) == T(f"<?print ceil(-2*x, -30)?>").renders(x=base)
		assert str(-base) == T(f"<?print ceil(-2*x+1, -30)?>").renders(x=base)
		# This checks integer overflow in the Java implementation
		assert "10000000000" == T(f"<?print ceil(x, -10)?>").renders(x=2147483647)
		# This checks long overflow in the Java implementation
		assert "10000000000000000000" == T(f"<?print ceil(x, -19)?>").renders(x=9223372036854775807)

	assert "43" == T("<?print ceil(42.6)?>").renders()
	assert "-42" == T("<?print ceil(-42.4)?>").renders()
	assert "<type int>" == T("<?print type(ceil(42.5))?>").renders()

	assert "50" == T("<?print ceil(42.4, -1)?>").renders()
	assert "50" == T("<?print ceil(46.2, -1)?>").renders()
	assert "-40" == T("<?print ceil(-42.4, -1)?>").renders()
	assert "-40" == T("<?print ceil(-46.2, -1)?>").renders()
	assert "<type int>" == T("<?print type(ceil(42.5, -1))?>").renders()

	assert "True" == T("<?print ceil(42.987, 1) == 43.0?>").renders()
	assert "42.2" == T("<?print ceil(42.123, 1)?>").renders()
	assert "-42.9" == T("<?print ceil(-42.987, 1)?>").renders()
	assert "-42.1" == T("<?print ceil(-42.123, 1)?>").renders()
	assert "True" == T("<?print math.isclose(ceil(42.589, 2), 42.59)?>").renders()
	assert "True" == T("<?print math.isclose(ceil(42.123, 2), 42.13)?>").renders()
	#
	assert "True" == T("<?print ceil(-42.589, 2) == -42.58?>").renders()
	assert "True" == T("<?print ceil(-42.123, 2) == -42.12?>").renders()
	assert "<type float>" == T("<?print type(ceil(42.5, 1))?>").renders()

	# Make sure that the parameters have the same name in all implementations
	assert "True" == T("<?print math.isclose(ceil(-42.123, digits=2), -42.12)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print ceil()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print ceil(1, 2, 3)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print ceil(number=-42.123, digits=2)?>").renders()


@pytest.mark.ul4
def test_function_getattr(T):
	assert "GURK" == T("<?print getattr('gurk', 'upper')()?>").renders()
	assert "a:42;b:17;c:23;" == T("<?for (key, value) in sorted(getattr(data, 'items')())?><?print key?>:<?print value?>;<?end for?>").renders(data={"a": 42, "b": 17, "c": 23})
	assert "{/}" == T("<?code getattr(data, 'clear')()?><?print data?>").renders(data={"a", "b", "c"})
	if T in (TemplatePython, TemplatePythonDump, TemplatePythonDumpS):
		assert "x=17, y=23" == T("x=<?print getattr(data, 'x')?>, y=<?print getattr(data, 'y')?>").renders(data=Point(17, 23))


@pytest.mark.ul4
def test_function_hasattr(T):
	assert "True" == T("<?print hasattr('gurk', 'upper')?>").renders()
	assert "False" == T("<?print hasattr('gurk', 'no')?>").renders()
	assert "TrueFalseFalse" == T("<?print hasattr(data, 'items')?><?print hasattr('data', 'a')?><?print hasattr('data', 'd')?>").renders(data={"a": 42, "b": 17, "c": 23})
	assert "TrueFalse" == T("<?print hasattr(data, 'clear')?><?print hasattr('data', 'a')?>").renders(data={"a", "b", "c"})
	if T in (TemplatePython, TemplatePythonDump, TemplatePythonDumpS):
		"TrueTrueFalse" == T("<?print hasattr(data, 'x')?><?print getattr(data, 'y')?><?print getattr(data, 'z')?>").renders(data=Point(17, 23))


@pytest.mark.ul4
def test_function_setattr(T):
	if T in (TemplatePython, TemplatePythonDump, TemplatePythonDumpS):
		assert "42" == T("<?code setattr(data, 'x', 42)?><?print data.x?>").renders(data=Point(17, 23))

		with raises("readonly attribute"):
			T("<?code setattr(data, 'y', 42)?>").renders(data=Point(17, 23))

		with raises("attribute x must be of type int"):
			T("<?code setattr(data, 'x', 'gurk')?>").renders(data=Point(17, 23))

		with raises("AttributeError: z"):
			T("<?code setattr(data, 'z', 42)?>").renders(data=Point(17, 23))


@pytest.mark.ul4
def test_function_dir(T):
	t = T("<?return dir(data)?>")

	set() == t(data=None)
	set() == t(data=True)
	set() == t(data=42)
	set() == t(data=42.5)
	assert {"calendar", "date", "day", "hour", "isoformat", "microsecond", "mimeformat", "minute", "month", "second", "week", "weekday", "year", "yearday"} == t(data=datetime.datetime.now())
	assert {"a", "abslight", "abslum", "b", "combine", "g", "hls", "hlsa", "hsv", "hsva", "hue", "invert", "light", "lum", "r", "rellight", "rellum", "sat", "witha", "withhue", "withlight", "withlum", "withsat"} == t(data=color.red)
	assert {"append", "count", "find", "insert", "pop", "rfind"} == t(data=[1, 2, 3])
	assert {"add", "clear"} == t(data={1, 2, 3})
	assert {"clear", "get", "items", "keys", "pop", "update", "values"} == t(data={"a": 17, "b": 23})
	if T in (TemplatePython, TemplatePythonDump, TemplatePythonDumpS):
		assert {'x', 'y'} == t(data=Point(17, 23))

	all = [
		None,
		True,
		42,
		42.5,
		datetime.datetime.now(),
		color.red,
		[1, 2, 3],
		{1, 2, 3},
		{"a": 17, "b": 23},
	]

	if T in (TemplatePython, TemplatePythonDump, TemplatePythonDumpS):
		all.append(Point(17, 23))

	# Check that ``getattr(x, ...)`` returns every attribute in ``dir(x)``
	assert "" == T("<?for obj in all?><?for an in dir(d)?><?if getattr(obj, an, None) is None?><?print repr(obj)?>.<?print an?>: FAIL<?end if?><?end for?><?end for?>").renders(all=all)

	with raises(unknownkeywordargument):
		T("<?print dir(obj=42)?>").renders()


@pytest.mark.ul4
def test_module_math(T):
	assert "math" == T("<?print math.__name__?>").renders()
	assert "Math related functions and constants" == T("<?print math.__doc__?>").renders()


@pytest.mark.ul4
def test_module_math_cos(T):
	t = T("<?code v = math.cos(x*math.pi)?><?print e-0.01 < v and v < e+0.01?>")

	for x in (0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2):
		assert "True" == t.renders(x=x, e=math.cos(x*math.pi))

	with raises(argumentmismatchmessage):
		T("<?print math.cos()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print math.cos(0, 0)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print math.cos(x=0)?>").renders()


@pytest.mark.ul4
def test_module_math_sin(T):
	t = T("<?code v = math.sin(x*math.pi)?><?print e-0.01 < v and v < e+0.01?>")

	for x in (0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2):
		assert "True" == t.renders(x=x, e=math.sin(x*math.pi))

	with raises(argumentmismatchmessage):
		T("<?print math.sin()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print math.sin(0, 0)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print math.sin(x=0)?>").renders()


@pytest.mark.ul4
def test_module_math_tan(T):
	t = T("<?code v = math.tan(x*math.pi)?><?print e-0.01 < v and v < e+0.01?>")

	for x in (0, 0.25, 0.75, 1, 1.25, 1.75, 2):
		assert "True" == t.renders(x=x, e=math.tan(x*math.pi))

	with raises(argumentmismatchmessage):
		T("<?print math.tan()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print math.tan(0, 0)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print math.tan(x=0)?>").renders()


@pytest.mark.ul4
def test_module_math_sqrt(T):
	t = T("<?code v = math.sqrt(x)?><?print e-0.01 < v and v < e+0.01?>")

	for x in range(10):
		assert "True" == t.renders(x=x, e=math.sqrt(x))

	with raises(argumentmismatchmessage):
		T("<?print math.sqrt()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print math.sqrt(0, 0)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print math.sqrt(x=0)?>").renders()


@pytest.mark.ul4
def test_module_math_isclose(T):
	t = T("<?print math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)?>")

	assert "True" == t.renders(a=10.0, b=12.5, rel_tol=0.25, abs_tol=0.0 )
	assert "True" == t.renders(a=1.0, b=1.25, rel_tol=0.0,  abs_tol=0.25)

	with raises(argumentmismatchmessage):
		T("<?print math.isclose()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print math.isclose(0, 0, 0, 0)?>").renders()


@pytest.mark.ul4
def test_method_upper(T):
	assert 'GURK' == T('<?print "gurk".upper()?>').renders()
	assert 'GURK' == T('<?code m = "gurk".upper?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.upper(42)?>").renders()


@pytest.mark.ul4
def test_method_lower(T):
	assert 'gurk' == T('<?print "GURK".lower()?>').renders()
	assert 'gurk' == T('<?code m = "GURK".lower?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.lower(42)?>").renders()


@pytest.mark.ul4
def test_method_capitalize(T):
	assert 'Gurk' == T('<?print "gURK".capitalize()?>').renders()
	assert 'Gurk' == T('<?code m = "gURK".capitalize?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.capitalize(42)?>").renders()


@pytest.mark.ul4
def test_method_startswith(T):
	assert "True" == T("<?print 'gurkhurz'.startswith('gurk')?>").renders()
	assert "False" == T("<?print 'gurkhurz'.startswith('hurz')?>").renders()
	assert "False" == T("<?code m = 'gurkhurz'.startswith?><?print m('hurz')?>").renders()
	assert "True" == T("<?print 'gurkhurz'.startswith(['gu', 'hu'])?>").renders()
	assert "False" == T("<?print 'gurkhurz'.startswith(['rk', 'rz'])?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.startswith()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.startswith('rk', 'rz')?>").renders()

	with raises(unknownkeywordargument):
		T("<?print 'gurkhurz'.startswith(prefix='gurk')?>").renders()


@pytest.mark.ul4
def test_method_endswith(T):
	assert "True" == T("<?print 'gurkhurz'.endswith('hurz')?>").renders()
	assert "False" == T("<?print 'gurkhurz'.endswith('gurk')?>").renders()
	assert "False" == T("<?code m = 'gurkhurz'.endswith?><?print m('gurk')?>").renders()
	assert "False" == T("<?print 'gurkhurz'.endswith(['gu', 'hu'])?>").renders()
	assert "True" == T("<?print 'gurkhurz'.endswith(['rk', 'rz'])?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.endswith()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.endswith('rk', 'rz')?>").renders()

	with raises(unknownkeywordargument):
		T("<?print 'gurkhurz'.endswith(suffix='hurz')?>").renders()


@pytest.mark.ul4
def test_method_strip(T):
	assert "gurk" == T(r"<?print obj.strip()?>").renders(obj=' \t\r\ngurk \t\r\n')
	assert "gurk" == T(r"<?print obj.strip('xyz')?>").renders(obj='xyzzygurkxyzzy')
	assert "gurk" == T(r"<?code m = obj.strip?><?print m('xyz')?>").renders(obj='xyzzygurkxyzzy')

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.strip('g', 'u')?>").renders()

	with raises(unknownkeywordargument):
		T(r"<?print obj.strip(chars='xyz')?>").renders(obj='xyzzygurkxyzzy')


@pytest.mark.ul4
def test_method_lstrip(T):
	assert "gurk \t\r\n" == T("<?print obj.lstrip()?>").renders(obj=" \t\r\ngurk \t\r\n")
	assert "gurkxyzzy" == T("<?print obj.lstrip(arg)?>").renders(obj="xyzzygurkxyzzy", arg="xyz")
	assert "gurkxyzzy" == T("<?code m = obj.lstrip?><?print m(arg)?>").renders(obj="xyzzygurkxyzzy", arg="xyz")

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.lstrip('g', 'u')?>").renders()

	with raises(unknownkeywordargument):
		T("<?print obj.lstrip(chars=arg)?>").renders(obj="xyzzygurkxyzzy", arg="xyz")


@pytest.mark.ul4
def test_method_rstrip(T):
	assert " \t\r\ngurk" == T("<?print obj.rstrip()?>").renders(obj=" \t\r\ngurk \t\r\n")
	assert "xyzzygurk" == T("<?print obj.rstrip(arg)?>").renders(obj="xyzzygurkxyzzy", arg="xyz")
	assert "xyzzygurk" == T("<?code m = obj.rstrip?><?print m(arg)?>").renders(obj="xyzzygurkxyzzy", arg="xyz")

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.rstrip('g', 'u')?>").renders()

	with raises(unknownkeywordargument):
		T("<?print obj.rstrip(chars=arg)?>").renders(obj="xyzzygurkxyzzy", arg="xyz")


@pytest.mark.ul4
def test_method_split(T):
	assert "(f)(o)(o)" == T("<?for item in obj.split()?>(<?print item?>)<?end for?>").renders(obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "(f)(o \t\r\no \t\r\n)" == T("<?for item in obj.split(None, 1)?>(<?print item?>)<?end for?>").renders(obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "()(f)(o)(o)()" == T("<?for item in obj.split(arg)?>(<?print item?>)<?end for?>").renders(obj="xxfxxoxxoxx", arg="xx")
	assert "()(f)(oxxoxx)" == T("<?for item in obj.split(arg, 2)?>(<?print item?>)<?end for?>").renders(obj="xxfxxoxxoxx", arg="xx")
	assert "()(f)(oxxoxx)" == T("<?code m = obj.split?><?for item in m(arg, 2)?>(<?print item?>)<?end for?>").renders(obj="xxfxxoxxoxx", arg="xx")

	# Make sure that the parameters have the same name in all implementations
	assert "()(f)(oxxoxx)" == T("<?for item in obj.split(sep=arg, maxsplit=2)?>(<?print item?>)<?end for?>").renders(obj="xxfxxoxxoxx", arg="xx")

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.split('u', 2, 42)?>").renders()


@pytest.mark.ul4
def test_method_rsplit(T):
	assert "(f)(o)(o)" == T("<?for item in obj.rsplit()?>(<?print item?>)<?end for?>").renders(obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "( \t\r\nf \t\r\no)(o)" == T("<?for item in obj.rsplit(None, 1)?>(<?print item?>)<?end for?>").renders(obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
	assert "()(f)(o)(o)()" == T("<?for item in obj.rsplit(arg)?>(<?print item?>)<?end for?>").renders(obj="xxfxxoxxoxx", arg="xx")
	assert "(xxfxxo)(o)()" == T("<?for item in obj.rsplit(arg, 2)?>(<?print item?>)<?end for?>").renders(obj="xxfxxoxxoxx", arg="xx")
	assert "(xxfxxo)(o)()" == T("<?code m = obj.rsplit?><?for item in m(arg, 2)?>(<?print item?>)<?end for?>").renders(obj="xxfxxoxxoxx", arg="xx")

	# Make sure that the parameters have the same name in all implementations
	assert "(xxfxxo)(o)()" == T("<?for item in obj.rsplit(sep=arg, maxsplit=2)?>(<?print item?>)<?end for?>").renders(obj="xxfxxoxxoxx", arg="xx")

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.rsplit('u', 2, 42)?>").renders()


@pytest.mark.ul4
def test_method_splitlines(T):
	lineends = (
		"\n",
		"\r",
		"\r\n",
		"\x0b",
		"\x0c",
		"\x1c",
		"\x1d",
		"\x1e",
		"\x85",
		"\u2028",
		"\u2029",
	)

	text = "".join(f"{chr(i)}{le}" for (i, le) in enumerate(lineends, ord('a')))

	source = "<?for item in obj.splitlines(keepends)?>(<?print repr(item)?>)<?end for?>"

	expected1 = "('a')('b')('c')('d')('e')('f')('g')('h')('i')('j')('k')"
	assert expected1 == T(source).renders(obj=text, keepends=False).replace('"', "'")

	expected2 = "".join(f"({chr(i)+le!r})" for (i, le) in enumerate(lineends, ord('a')))
	assert expected2 == T(source).renders(obj=text, keepends=True).replace('"', "'")

	# Make sure that the parameters have the same name in all implementations
	assert "['gurk']" == T("<?print 'gurk'.splitlines(keepends=False)?>").renders()


@pytest.mark.ul4
def test_method_replace(T):
	assert 'goork' == T("<?print 'gurk'.replace('u', 'oo')?>").renders()
	assert 'fuuuu' == T("<?print 'foo'.replace('o', 'uu', None)?>").renders()
	assert 'fuuo' == T("<?print 'foo'.replace('o', 'uu', 1)?>").renders()
	assert 'fuuo' == T("<?code m = 'foo'.replace?><?print m('o', 'uu', 1)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.replace()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print 'gurk'.replace('foo', 'bar', 2, 42)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print 'foo'.replace(old='o', new='uu', count=1)?>").renders()


@pytest.mark.ul4
def test_method_renders(T):
	t = ul4c.Template('(<?print data?>)')
	assert '(GURK)' == T("<?print t.renders(data='gurk').upper()?>").renders(t=t)
	assert '(GURK)' == T("<?print t.renders(**{'data': 'gurk'}).upper()?>").renders(t=t)
	assert '(GURK)' == T("<?code m = t.renders?><?print m(**{'data': 'gurk'}).upper()?>").renders(t=t)

	t = ul4c.Template('(gurk)')
	assert '(GURK)' == T("<?print t.renders().upper()?>").renders(t=t)


@pytest.mark.ul4
def test_method_isoformat_date(T):
	assert '2000-02-29' == T('<?print @(2000-02-29).isoformat()?>').renders()

	with raises(argumentmismatchmessage):
		T("<?print @(2000-02-29).isoformat(42)?>").renders()


@pytest.mark.ul4
def test_method_isoformat_datetime(T):
	assert '2000-02-29T00:00:00' == T('<?print @(2000-02-29T).isoformat()?>').renders()
	assert '2000-02-29T12:34:00' == T('<?print @(2000-02-29T12:34).isoformat()?>').renders()
	assert '2000-02-29T12:34:56' == T('<?print @(2000-02-29T12:34:56).isoformat()?>').renders()
	assert '2000-02-29T12:34:56.987000' == T('<?print @(2000-02-29T12:34:56.987000).isoformat()?>').renders()

	with raises(argumentmismatchmessage):
		T("<?print @(2000-02-29T12:34:56.987000).isoformat(42)?>").renders()


@pytest.mark.ul4
def test_method_mimeformat_date(T):
	t1 = datetime.date(2010, 2, 22)

	assert 'Mon, 22 Feb 2010' == T("<?print data.mimeformat()?>").renders(data=t1)
	assert 'Mon, 22 Feb 2010' == T("<?code m = data.mimeformat?><?print m()?>").renders(data=t1)

	with raises(argumentmismatchmessage):
		T("<?print @(2000-02-29).mimeformat(42)?>").renders()


@pytest.mark.ul4
def test_method_mimeformat_datetime(T):
	t2 = datetime.datetime(2010, 2, 22, 12, 34, 56)

	assert 'Mon, 22 Feb 2010 12:34:56 GMT' == T("<?print data.mimeformat()?>").renders(data=t2)
	assert 'Mon, 22 Feb 2010 12:34:56 GMT' == T("<?code m = data.mimeformat?><?print m()?>").renders(data=t2)

	with raises(argumentmismatchmessage):
		T("<?print @(2000-02-29T12:34:56.987000).mimeformat(42)?>").renders()


@pytest.mark.ul4
def test_method_date_date(T):
	assert '2000-02-29' == T('<?print @(2000-02-29).date()?>').renders()

	with raises(argumentmismatchmessage):
		T("<?print @(2000-02-29).date(42)?>").renders()


@pytest.mark.ul4
def test_method_date_datetime(T):
	assert '2000-02-29' == T('<?print @(2000-02-29T12:34:56.987654).date()?>').renders()

	with raises(argumentmismatchmessage):
		T("<?print @(2000-02-29T12:34:56.987000).date(42)?>").renders()


@pytest.mark.ul4
def test_method_keys(T):
	assert "a;b;c;" == T("<?code data = {'a': 42, 'b': 17, 'c': 23}?><?for key in data.keys()?><?print key?>;<?end for?>").renders()
	assert "a;b;c;" == T("<?code data = {'a': 42, 'b': 17, 'c': 23}?><?code m = data.keys?><?for key in m()?><?print key?>;<?end for?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print {}.keys(42)?>").renders()


@pytest.mark.ul4
def test_method_items(T):
	assert "a:42;b:17;c:23;" == T("<?code data = {'a': 42, 'b': 17, 'c': 23}?><?for (key, value) in data.items()?><?print key?>:<?print value?>;<?end for?>").renders()
	assert "a:42;b:17;c:23;" == T("<?code data = {'a': 42, 'b': 17, 'c': 23}?><?code m = data.items?><?for (key, value) in m()?><?print key?>:<?print value?>;<?end for?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print {}.items(42)?>").renders()


@pytest.mark.ul4
def test_method_values(T):
	assert "42;17;23;" == T("<?code data = {'a': 42, 'b': 17, 'c': 23}?><?for value in data.values()?><?print value?>;<?end for?>").renders()
	assert "42;17;23;" == T("<?code data = {'a': 42, 'b': 17, 'c': 23}?><?code m = data.values?><?for value in m()?><?print value?>;<?end for?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print {}.values(42)?>").renders()


@pytest.mark.ul4
def test_method_get(T):
	assert "42" == T("<?print {}.get('foo', 42)?>").renders()
	assert "17" == T("<?print {'foo': 17}.get('foo', 42)?>").renders()
	assert "" == T("<?print {}.get('foo')?>").renders()
	assert "17" == T("<?print {'foo': 17}.get('foo')?>").renders()
	assert "17" == T("<?code m = {'foo': 17}.get?><?print m('foo')?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print {}.get()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print {}.get('foo', 2, 42)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print {'foo': 17}.get(key='foo', default=42)?>").renders()


@pytest.mark.ul4
def test_color_method_r_g_b_a(T):
	assert '0x11' == T('<?code c = #123?><?print hex(c.r())?>').renders()
	assert '0x11' == T('<?code c = #123?><?code m = c.r?><?print hex(m())?>').renders()
	assert '0x22' == T('<?code c = #123?><?print hex(c.g())?>').renders()
	assert '0x22' == T('<?code c = #123?><?code m = c.g?><?print hex(m())?>').renders()
	assert '0x33' == T('<?code c = #123?><?print hex(c.b())?>').renders()
	assert '0x33' == T('<?code c = #123?><?code m = c.b?><?print hex(m())?>').renders()
	assert '0xff' == T('<?code c = #123?><?print hex(c.a())?>').renders()
	assert '0xff' == T('<?code c = #123?><?code m = c.a?><?print hex(m())?>').renders()


@pytest.mark.ul4
def test_color_method_hls(T):
	assert '0' == T('<?code c = #fff?><?print int(c.hls()[0])?>').renders()
	assert '1' == T('<?code c = #fff?><?print int(c.hls()[1])?>').renders()
	assert '0' == T('<?code c = #fff?><?print int(c.hls()[2])?>').renders()
	assert '0' == T('<?code c = #fff?><?code m = c.hls?><?print int(m()[0])?>').renders()


@pytest.mark.ul4
def test_color_method_hlsa(T):
	assert '0' == T('<?code c = #fff?><?print int(c.hlsa()[0])?>').renders()
	assert '1' == T('<?code c = #fff?><?print int(c.hlsa()[1])?>').renders()
	assert '0' == T('<?code c = #fff?><?print int(c.hlsa()[2])?>').renders()
	assert '1' == T('<?code c = #fff?><?print int(c.hlsa()[3])?>').renders()
	assert '0' == T('<?code c = #fff?><?code m = c.hlsa?><?print int(m()[0])?>').renders()


@pytest.mark.ul4
def test_color_method_hsv(T):
	assert '0' == T('<?code c = #fff?><?print int(c.hsv()[0])?>').renders()
	assert '0' == T('<?code c = #fff?><?print int(c.hsv()[1])?>').renders()
	assert '1' == T('<?code c = #fff?><?print int(c.hsv()[2])?>').renders()
	assert '0' == T('<?code c = #fff?><?code m = c.hsv?><?print int(m()[0])?>').renders()


@pytest.mark.ul4
def test_color_method_hsva(T):
	assert '0' == T('<?code c = #fff?><?print int(c.hsva()[0])?>').renders()
	assert '0' == T('<?code c = #fff?><?print int(c.hsva()[1])?>').renders()
	assert '1' == T('<?code c = #fff?><?print int(c.hsva()[2])?>').renders()
	assert '1' == T('<?code c = #fff?><?print int(c.hsva()[3])?>').renders()
	assert '0' == T('<?code c = #fff?><?code m = c.hsva?><?print int(m()[0])?>').renders()


@pytest.mark.ul4
def test_color_method_hue(T):
	assert 'True' == T('<?print #f00.hue() == 0?>').renders()
	assert 'True' == T('<?print #0f0.hue() == 120/360?>').renders()
	assert 'True' == T('<?print #00f.hue() == 240/360?>').renders()


@pytest.mark.ul4
def test_color_method_sat(T):
	assert 'True' == T('<?print #000.sat() == 0.0?>').renders()
	assert 'True' == T('<?print #fff.sat() == 0.0?>').renders()
	assert 'True' == T('<?print #f00.sat() == 1.0?>').renders()
	assert 'True' == T('<?print #0f0.sat() == 1.0?>').renders()
	assert 'True' == T('<?print #00f.sat() == 1.0?>').renders()


@pytest.mark.ul4
def test_color_method_light(T):
	assert 'True' == T('<?print #000.light() == 0?>').renders()
	assert 'True' == T('<?print #fff.light() == 1?>').renders()
	assert 'True' == T('<?print #f00.light() == 0.5?>').renders()
	assert 'True' == T('<?print #0f0.light() == 0.5?>').renders()
	assert 'True' == T('<?print #00f.light() == 0.5?>').renders()
	assert 'True' == T('<?code m = #fff.light?><?print m() == 1?>').renders()


@pytest.mark.ul4
def test_color_method_lum(T):
	assert math.isclose(1.0   , float(T("<?print #fff.lum()?>").renders()))
	assert math.isclose(0.0   , float(T("<?print #000.lum()?>").renders()))
	assert math.isclose(0.2126, float(T("<?print #f00.lum()?>").renders()))
	assert math.isclose(0.7152, float(T("<?print #0f0.lum()?>").renders()))
	assert math.isclose(0.0722, float(T("<?print #00f.lum()?>").renders()))


@pytest.mark.ul4
def test_color_method_withhue(T):
	assert '#f00' == T('<?code m = #0f0.withhue?><?print m(0/6)?>').renders()
	assert '#f00' == T('<?print #0f0.withhue(0/6)?>').renders()
	assert '#0f0' == T('<?print #f00.withhue(2/6)?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '#f00' == T('<?print #0f0.withhue(hue=0)?>').renders()


@pytest.mark.ul4
def test_color_method_withlight(T):
	assert '#fff' == T('<?code m = #000.withlight?><?print m(1.0)?>').renders()
	assert '#fff' == T('<?print #000.withlight(1.0)?>').renders()
	assert '#000' == T('<?print #000.withlight(0.0)?>').renders()
	assert '#fff' == T('<?print #fff.withlight(1.0)?>').renders()
	assert '#000' == T('<?print #fff.withlight(0.0)?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '#fff' == T('<?print #000.withlight(light=1.0)?>').renders()


@pytest.mark.ul4
def test_color_method_abslight(T):
	assert '#fff' == T('<?print #000.abslight(1.0)?>').renders()
	assert '#333' == T('<?print #000.abslight(0.2)?>').renders()
	assert '#000' == T('<?print #000.abslight(0.0)?>').renders()
	assert '#000' == T('<?print #000.abslight(-1.0)?>').renders()
	assert '#fff' == T('<?print #fff.abslight(1.0)?>').renders()
	assert '#fff' == T('<?print #fff.abslight(0.0)?>').renders()
	assert '#ccc' == T('<?print #fff.abslight(-0.2)?>').renders()
	assert '#000' == T('<?print #fff.abslight(-1.0)?>').renders()

	assert '#fff' == T('<?code m = #000.withlight?><?print m(1)?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '#fff' == T('<?print #000.abslight(f=1)?>').renders()

@pytest.mark.ul4
def test_color_method_rellight(T):
	assert '#fff' == T('<?print #000.rellight(1.0)?>').renders()
	assert '#333' == T('<?print #000.rellight(0.2)?>').renders()
	assert '#999' == T('<?print #333.rellight(0.5)?>').renders()
	assert '#000' == T('<?print #000.rellight(0.0)?>').renders()
	assert '#000' == T('<?print #000.rellight(-1.0)?>').renders()
	assert '#fff' == T('<?print #fff.rellight(1.0)?>').renders()
	assert '#fff' == T('<?print #fff.rellight(0.0)?>').renders()
	assert '#ccc' == T('<?print #fff.rellight(-0.2)?>').renders()
	assert '#666' == T('<?print #ccc.rellight(-0.5)?>').renders()
	assert '#000' == T('<?print #fff.rellight(-1.0)?>').renders()

	assert '#fff' == T('<?code m = #000.rellight?><?print m(1)?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '#fff' == T('<?print #000.rellight(f=1)?>').renders()


@pytest.mark.ul4
def test_color_method_withsat(T):
	# Javascript rounds differently (i.e. Python and Java return ``#7f7f7f``,
	# but Javascript returns ``#808080``).
	assert T('<?code m = #0f0.withsat?><?print m(0.0)?>').renders() in {'#7f7f7f', '#808080'}
	assert T('<?print #0f0.withsat(0.0)?>').renders() in {'#7f7f7f', '#808080'}
	assert '#0f0' == T('<?print #0f0.withsat(1.0)?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert T('<?print #0f0.withsat(sat=0)?>').renders() in {'#7f7f7f', '#808080'}


@pytest.mark.ul4
def test_color_method_witha(T):
	assert '#0063a82a' == T('<?print repr(#0063a8.witha(42))?>').renders()
	assert '#0063a82a' == T('<?code m = #0063a8.witha?><?print repr(m(42))?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '#0063a82a' == T('<?print repr(#0063a8.witha(a=42))?>').renders()


@pytest.mark.ul4
def test_color_method_withlum(T):
	assert '#fff' == T('<?print #000.withlum(1)?>').renders()
	assert '#fff' == T('<?code m = #000.withlum?><?print m(1)?>').renders()

	assert '#000' == T('<?print #fff.withlum(0)?>').renders()
	assert '#333' == T('<?print #fff.withlum(0.2)?>').renders()
	assert '#f00' == T('<?print #f00.withlum(0.2126)?>').renders()
	assert '#0f0' == T('<?print #0f0.withlum(0.7152)?>').renders()
	assert '#00f' == T('<?print #00f.withlum(0.0722)?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '#fff' == T('<?print #000.withlum(lum=1)?>').renders()


@pytest.mark.ul4
def test_color_method_abslum(T):
	assert '#fff' == T('<?print #000.abslum(1)?>').renders()
	assert '#fff' == T('<?code m = #000.abslum?><?print m(1)?>').renders()

	assert '#fff' == T('<?print #fff.abslum(0)?>').renders()
	assert '#000' == T('<?print #fff.abslum(-1)?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '#fff' == T('<?print #000.abslum(f=1)?>').renders()


@pytest.mark.ul4
def test_color_method_rellum(T):
	assert '#fff' == T('<?print #000.rellum(1)?>').renders()
	assert '#fff' == T('<?code m = #000.rellum?><?print m(1)?>').renders()

	assert '#fff' == T('<?print #fff.rellum(0)?>').renders()
	assert '#000' == T('<?print #fff.rellum(-1)?>').renders()
	assert '#888' == T('<?print #888.rellum(0)?>').renders()
	assert '#f33' == T('<?print #f00.rellum(0.2)?>').renders()
	assert '#3f3' == T('<?print #0f0.rellum(0.2)?>').renders()
	assert '#33f' == T('<?print #00f.rellum(0.2)?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '#fff' == T('<?print #000.rellum(f=1)?>').renders()


@pytest.mark.ul4
def test_color_method_invert(T):
	assert '#fff' == T('<?code m = #000.invert?><?print m(1)?>').renders()

	assert '#000' == T('<?print #000.invert(0)?>').renders()
	assert '#333' == T('<?print #000.invert(0.2)?>').renders()
	assert '#fff' == T('<?print #000.invert(1)?>').renders()
	assert '#fff' == T('<?print #000.invert()?>').renders()
	assert '#fff' == T('<?print #fff.invert(0)?>').renders()
	assert '#ccc' == T('<?print #fff.invert(0.2)?>').renders()
	assert '#000' == T('<?print #fff.invert(1)?>').renders()
	assert '#000' == T('<?print #fff.invert()?>').renders()
	assert '#0ff' == T('<?print #f00.invert()?>').renders()
	assert '#f0f' == T('<?print #0f0.invert()?>').renders()
	assert '#ff0' == T('<?print #00f.invert()?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '#fff' == T('<?print #000.invert(f=1)?>').renders()


@pytest.mark.ul4
def test_color_method_combine(T):
	assert "#783456" == T("<?print repr(color.Color(0x12, 0x34, 0x56).combine(r=0x78))?>").renders()
	assert "#127856" == T("<?print repr(color.Color(0x12, 0x34, 0x56).combine(g=0x78))?>").renders()
	assert "#123478" == T("<?print repr(color.Color(0x12, 0x34, 0x56).combine(b=0x78))?>").renders()
	assert "#12345678" == T("<?print repr(color.Color(0x12, 0x34, 0x56).combine(a=0x78))?>").renders()


@pytest.mark.ul4
def test_method_join(T):
	assert '1,2,3,4' == T('<?print ",".join("1234")?>').renders()
	assert '1,2,3,4' == T('<?print ",".join(["1", "2", "3", "4"])?>').renders()
	assert '1,2,3,4' == T('<?code m = ",".join?><?print m("1234")?>').renders()

	with raises(unknownkeywordargument):
		T('<?print ",".join(iterable="1234")?>').renders()


@pytest.mark.ul4
def test_method_count_string(T):
	source = "<?ul4 f(haystack, needle, start=None, end=None)?><?print haystack.count(needle, start, end)?>"

	assert '3' == T(source).renders(haystack='aaa', needle='a')
	assert '0' == T(source).renders(haystack='aaa', needle='b')
	assert '3' == T(source).renders(haystack='aaa', needle='a')
	assert '0' == T(source).renders(haystack='aaa', needle='b')
	assert '3' == T(source).renders(haystack='aaa', needle='a')
	assert '0' == T(source).renders(haystack='aaa', needle='b')
	assert '0' == T(source).renders(haystack='aaa', needle='b')
	assert '2' == T(source).renders(haystack='aaa', needle='a', start=1)
	assert '0' == T(source).renders(haystack='aaa', needle='a', start=10)
	assert '1' == T(source).renders(haystack='aaa', needle='a', start=-1)
	assert '3' == T(source).renders(haystack='aaa', needle='a', start=-10)
	assert '1' == T(source).renders(haystack='aaa', needle='a', start=0, end=1)
	assert '3' == T(source).renders(haystack='aaa', needle='a', start=0, end=10)
	assert '2' == T(source).renders(haystack='aaa', needle='a', start=0, end=-1)
	assert '0' == T(source).renders(haystack='aaa', needle='a', start=0, end=-10)
	assert '3' == T(source).renders(haystack='aaa', needle='', start=1)
	assert '1' == T(source).renders(haystack='aaa', needle='', start=3)
	assert '0' == T(source).renders(haystack='aaa', needle='', start=10)
	assert '2' == T(source).renders(haystack='aaa', needle='', start=-1)
	assert '4' == T(source).renders(haystack='aaa', needle='', start=-10)

	assert '1' == T(source).renders(haystack='',  needle='')
	assert '0' == T(source).renders(haystack='',  needle='', start=1, end=1)
	assert '0' == T(source).renders(haystack='',  needle='', start=0x7fffffff, end=0)

	assert '0' == T(source).renders(haystack='',  needle='xx')
	assert '0' == T(source).renders(haystack='',  needle='xx', start=1, end=1)
	assert '0' == T(source).renders(haystack='',  needle='xx', start=0x7fffffff, end=0)

	assert '1' == T(source).renders(haystack='aba', needle='ab', start=None, end=2)
	assert '0' == T(source).renders(haystack='aba', needle='ab', start=None, end=1)

	# Matches are non overlapping
	assert '1' == T(source).renders(haystack='aaa', needle='aa')

	with raises(argumentmismatchmessage):
		T('<?print "gurk".count()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print "gurk".count("u", 1, 2, 42)?>').renders()

	with raises(unknownkeywordargument):
		T('<?print "gurk".count(sub="u")?>').renders()


@pytest.mark.ul4
def test_method_count_list(T):
	source = "<?ul4 f(haystack, needle, start=None, end=None)?><?print haystack.count(needle, start, end)?>"

	assert '0' == T(source).renders(haystack=[1, 2, 3, 2, 3, 4, 1, 2, 3], needle='a')
	assert '3' == T(source).renders(haystack=[1, 2, 3, 2, 3, 4, 1, 2, 3], needle=2)
	assert '2' == T(source).renders(haystack=[1, 2, 3, 2, 3, 4, 1, 2, 3], needle=2, start=2)
	assert '1' == T(source).renders(haystack=[1, 2, 3, 2, 3, 4, 1, 2, 3], needle=2, start=2, end=7)

	with raises(argumentmismatchmessage):
		T('<?print [1, 2, 3].count()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print [1, 2, 3].count(1, 1, 2, 42)?>').renders()

	with raises(unknownkeywordargument):
		T('<?print [1, 2, 3].count(sub=1)?>').renders()


@pytest.mark.ul4
def test_method_find_string(T):
	s = "gurkgurk"
	assert '-1' == T('<?print s.find("ks")?>').renders(s=s)
	assert '2' == T('<?print s.find("rk")?>').renders(s=s)
	assert '2' == T('<?print s.find("rk", 2)?>').renders(s=s)
	assert '6' == T('<?print s.find("rk", -3)?>').renders(s=s)
	assert '2' == T('<?print s.find("rk", 2, 4)?>').renders(s=s)
	assert '6' == T('<?print s.find("rk", 4, 8)?>').renders(s=s)
	assert '5' == T('<?print s.find("ur", -4, -1)?>').renders(s=s)
	assert '-1' == T('<?print s.find("rk", 2, 3)?>').renders(s=s)
	assert '-1' == T('<?print s.find("rk", 7)?>').renders(s=s)
	assert '-1' == T('<?code m = s.find?><?print m("rk", 7)?>').renders(s=s)

	with raises(argumentmismatchmessage):
		T('<?print "gurk".find()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print "gurk".find("u", 1, 2, 42)?>').renders()

	with raises(unknownkeywordargument):
		T('<?print s.find(sub="rk", start=2, end=4)?>').renders(s=s)


@pytest.mark.ul4
def test_method_find_list(T):
	l = list("gurkgurk")
	assert '-1' == T('<?print l.find("x")?>').renders(l=l)
	assert '2' == T('<?print l.find("r")?>').renders(l=l)
	assert '2' == T('<?print l.find("r", 2)?>').renders(l=l)
	assert '6' == T('<?print l.find("r", -3)?>').renders(l=l)
	assert '2' == T('<?print l.find("r", 2, 4)?>').renders(l=l)
	assert '6' == T('<?print l.find("r", 4, 8)?>').renders(l=l)
	assert '6' == T('<?print l.find("r", -3, -1)?>').renders(l=l)
	assert '-1' == T('<?print l.find("r", 2, 2)?>').renders(l=l)
	assert '-1' == T('<?print l.find("r", 7)?>').renders(l=l)
	assert '1' == T('<?print l.find(None)?>').renders(l=[0, None, 1, None, 2, None, 3, None])
	assert '-1' == T('<?code m = l.find?><?print m("r", 7)?>').renders(l=l)

	with raises(argumentmismatchmessage):
		T('<?print [1, 2, 3].find()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print [1, 2, 3].find(1, 1, 2, 42)?>').renders()

	with raises(unknownkeywordargument):
		T('<?print l.find(sub="rk", start=2, end=4)?>').renders(l=l)


@pytest.mark.ul4
def test_method_rfind_string(T):
	s = "gurkgurk"
	assert '-1' == T('<?print s.rfind("ks")?>').renders(s=s)
	assert '6' == T('<?print s.rfind("rk")?>').renders(s=s)
	assert '6' == T('<?print s.rfind("rk", 2)?>').renders(s=s)
	assert '6' == T('<?print s.rfind("rk", -3)?>').renders(s=s)
	assert '2' == T('<?print s.rfind("rk", 2, 4)?>').renders(s=s)
	assert '6' == T('<?print s.rfind("rk", 4, 8)?>').renders(s=s)
	assert '5' == T('<?print s.rfind("ur", -4, -1)?>').renders(s=s)
	assert '-1' == T('<?print s.rfind("rk", 2, 3)?>').renders(s=s)
	assert '-1' == T('<?print s.rfind("rk", 7)?>').renders(s=s)
	assert '-1' == T('<?code m = s.rfind?><?print m("rk", 7)?>').renders(s=s)

	with raises(argumentmismatchmessage):
		T('<?print "gurk".find()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print "gurk".find("u", 1, 2, 42)?>').renders()

	with raises(unknownkeywordargument):
		T('<?print s.rfind(sub="rk", start=2, end=4)?>').renders(s=s)


@pytest.mark.ul4
def test_method_rfind_list(T):
	l = list("gurkgurk")
	assert '-1' == T('<?print l.rfind("x")?>').renders(l=l)
	assert '6' == T('<?print l.rfind("r")?>').renders(l=l)
	assert '6' == T('<?print l.rfind("r", 2)?>').renders(l=l)
	assert '2' == T('<?print l.rfind("r", 2, 4)?>').renders(l=l)
	assert '6' == T('<?print l.rfind("r", 4, 8)?>').renders(l=l)
	assert '6' == T('<?print l.rfind("r", -3, -1)?>').renders(l=l)
	assert '-1' == T('<?print l.rfind("r", 2, 2)?>').renders(l=l)
	assert '-1' == T('<?print l.rfind("r", 7)?>').renders(l=l)
	assert '7' == T('<?print l.rfind(None)?>').renders(l=[0, None, 1, None, 2, None, 3, None])
	assert '-1' == T('<?code m = l.rfind?><?print m("r", 7)?>').renders(l=l)

	with raises(argumentmismatchmessage):
		T('<?print [1, 2, 3].rfind()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print [1, 2, 3].rfind(1, 1, 2, 42)?>').renders()

	with raises(unknownkeywordargument):
		T('<?print l.rfind(sub="rk", start=2, end=4)?>').renders(l=l)


@pytest.mark.ul4
def test_method_day(T):
	assert '12' == T('<?print @(2010-05-12).day()?>').renders()
	assert '12' == T('<?print d.day()?>').renders(d=datetime.date(2010, 5, 12))
	assert '12' == T('<?code m = @(2010-05-12).day?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2010-05-12).day(42)?>').renders()


@pytest.mark.ul4
def test_method_month(T):
	assert '5' == T('<?print @(2010-05-12).month()?>').renders()
	assert '5' == T('<?print d.month()?>').renders(d=datetime.date(2010, 5, 12))
	assert '5' == T('<?code m = @(2010-05-12).month?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2010-05-12).month(42)?>').renders()


@pytest.mark.ul4
def test_method_year(T):
	assert '5' == T('<?print @(2010-05-12).month()?>').renders()
	assert '5' == T('<?print d.month()?>').renders(d=datetime.date(2010, 5, 12))
	assert '5' == T('<?code m = @(2010-05-12).month?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2010-05-12).year(42)?>').renders()


@pytest.mark.ul4
def test_method_hour(T):
	assert '16' == T('<?print @(2010-05-12T16:47:56).hour()?>').renders()
	assert '16' == T('<?print d.hour()?>').renders(d=datetime.datetime(2010, 5, 12, 16, 47, 56))
	assert '16' == T('<?code m = @(2010-05-12T16:47:56).hour?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2010-05-12T16:47:56).hour(42)?>').renders()


@pytest.mark.ul4
def test_method_minute(T):
	assert '47' == T('<?print @(2010-05-12T16:47:56).minute()?>').renders()
	assert '47' == T('<?print d.minute()?>').renders(d=datetime.datetime(2010, 5, 12, 16, 47, 56))
	assert '47' == T('<?code m = @(2010-05-12T16:47:56).minute?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2010-05-12T16:47:56).minute(42)?>').renders()


@pytest.mark.ul4
def test_method_second(T):
	assert '56' == T('<?print @(2010-05-12T16:47:56).second()?>').renders()
	assert '56' == T('<?print d.second()?>').renders(d=datetime.datetime(2010, 5, 12, 16, 47, 56))
	assert '56' == T('<?code m = @(2010-05-12T16:47:56).second?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2010-05-12T16:47:56).second(42)?>').renders()


@pytest.mark.ul4
def test_method_microsecond(T):
	if T is not TemplatePHP:
		assert '123000' == T('<?print @(2010-05-12T16:47:56.123000).microsecond()?>').renders()
		assert '123000' == T('<?print d.microsecond()?>').renders(d=datetime.datetime(2010, 5, 12, 16, 47, 56, 123000))
		assert '123000' == T('<?code m = @(2010-05-12T16:47:56.123000).microsecond?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2010-05-12T16:47:56).microsecond(42)?>').renders()


@pytest.mark.ul4
def test_method_weekday(T):
	assert '2' == T('<?print @(2010-05-12).weekday()?>').renders()
	assert '2' == T('<?print d.weekday()?>').renders(d=datetime.date(2010, 5, 12))
	assert '2' == T('<?code m = @(2010-05-12).weekday?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2010-05-12).weekday(42)?>').renders()


@pytest.mark.ul4
def test_method_calendar(T):
	# 1996: Non-leap year, starting on Monday
	assert '[1996, 1, 0]' == T('<?print repr(@(1996-01-01).calendar())?>').renders()
	assert '[1996, 1, 0]' == T('<?print repr(@(1996-01-01).calendar(6, 1))?>').renders()
	assert '[1996, 1, 0]' == T('<?print repr(@(1996-01-01).calendar(0, 7))?>').renders()
	assert '[1996, 1, 6]' == T('<?print repr(@(1996-01-07).calendar())?>').renders()
	assert '[1996, 2, 0]' == T('<?print repr(@(1996-01-08).calendar())?>').renders()
	assert '[1996, 52, 6]' == T('<?print repr(@(1996-12-29).calendar())?>').renders()
	assert '[1997, 1, 0]' == T('<?print repr(@(1996-12-30).calendar())?>').renders()

	# 2018: Leap year, starting on Monday
	assert '[2018, 1, 0]' == T('<?print repr(@(2018-01-01).calendar())?>').renders()
	assert '[2018, 1, 0]' == T('<?print repr(@(2018-01-01).calendar(6, 1))?>').renders()
	assert '[2018, 1, 0]' == T('<?print repr(@(2018-01-01).calendar(0, 7))?>').renders()
	assert '[2018, 1, 6]' == T('<?print repr(@(2018-01-07).calendar())?>').renders()
	assert '[2018, 2, 0]' == T('<?print repr(@(2018-01-08).calendar())?>').renders()
	assert '[2018, 22, 0]' == T('<?print repr(@(2018-05-28).calendar())?>').renders()
	assert '[2018, 52, 6]' == T('<?print repr(@(2018-12-30).calendar())?>').renders()
	assert '[2019, 1, 0]' == T('<?print repr(@(2018-12-31).calendar())?>').renders()

	# 2013: Non-leap year, starting on Tuesday
	assert '[2013, 1, 1]' == T('<?print repr(@(2013-01-01).calendar())?>').renders()
	assert '[2013, 1, 1]' == T('<?print repr(@(2013-01-01).calendar(6, 1))?>').renders()
	assert '[2012, 53, 1]' == T('<?print repr(@(2013-01-01).calendar(0, 7))?>').renders()
	assert '[2013, 1, 6]' == T('<?print repr(@(2013-01-06).calendar())?>').renders()
	assert '[2013, 2, 0]' == T('<?print repr(@(2013-01-07).calendar())?>').renders()
	assert '[2013, 52, 6]' == T('<?print repr(@(2013-12-29).calendar())?>').renders()
	assert '[2014, 1, 0]' == T('<?print repr(@(2013-12-30).calendar())?>').renders()

	# 2008: Leap year, starting on Tuesday
	assert '[2008, 1, 1]' == T('<?print repr(@(2008-01-01).calendar())?>').renders()
	assert '[2008, 1, 1]' == T('<?print repr(@(2008-01-01).calendar(6, 1))?>').renders()
	assert '[2007, 53, 1]' == T('<?print repr(@(2008-01-01).calendar(0, 7))?>').renders()
	assert '[2008, 1, 6]' == T('<?print repr(@(2008-01-06).calendar())?>').renders()
	assert '[2008, 2, 0]' == T('<?print repr(@(2008-01-07).calendar())?>').renders()
	assert '[2008, 52, 6]' == T('<?print repr(@(2008-12-28).calendar())?>').renders()
	assert '[2009, 1, 0]' == T('<?print repr(@(2008-12-29).calendar())?>').renders()

	# 2014: Non-leap year, starting on Wednesday
	assert '[2014, 1, 2]' == T('<?print repr(@(2014-01-01).calendar())?>').renders()
	assert '[2014, 1, 2]' == T('<?print repr(@(2014-01-01).calendar(6, 1))?>').renders()
	assert '[2013, 52, 2]' == T('<?print repr(@(2014-01-01).calendar(0, 7))?>').renders()
	assert '[2014, 1, 6]' == T('<?print repr(@(2014-01-05).calendar())?>').renders()
	assert '[2014, 2, 0]' == T('<?print repr(@(2014-01-06).calendar())?>').renders()
	assert '[2014, 52, 6]' == T('<?print repr(@(2014-12-28).calendar())?>').renders()
	assert '[2015, 1, 0]' == T('<?print repr(@(2014-12-29).calendar())?>').renders()

	# 1992: Leap year, starting on Wednesday
	assert '[1992, 1, 2]' == T('<?print repr(@(1992-01-01).calendar())?>').renders()
	assert '[1992, 1, 2]' == T('<?print repr(@(1992-01-01).calendar(6, 1))?>').renders()
	assert '[1991, 52, 2]' == T('<?print repr(@(1992-01-01).calendar(0, 7))?>').renders()
	assert '[1992, 1, 6]' == T('<?print repr(@(1992-01-05).calendar())?>').renders()
	assert '[1992, 2, 0]' == T('<?print repr(@(1992-01-06).calendar())?>').renders()
	assert '[1992, 52, 6]' == T('<?print repr(@(1992-12-27).calendar())?>').renders()
	assert '[1992, 53, 0]' == T('<?print repr(@(1992-12-28).calendar())?>').renders()

	# 2015: Non-leap year, starting on Thursday
	assert '[2015, 1, 3]' == T('<?print repr(@(2015-01-01).calendar())?>').renders()
	assert '[2015, 1, 3]' == T('<?print repr(@(2015-01-01).calendar(6, 1))?>').renders()
	assert '[2014, 52, 3]' == T('<?print repr(@(2015-01-01).calendar(0, 7))?>').renders()
	assert '[2015, 1, 6]' == T('<?print repr(@(2015-01-04).calendar())?>').renders()
	assert '[2015, 2, 0]' == T('<?print repr(@(2015-01-05).calendar())?>').renders()
	assert '[2015, 52, 6]' == T('<?print repr(@(2015-12-27).calendar())?>').renders()
	assert '[2015, 53, 0]' == T('<?print repr(@(2015-12-28).calendar())?>').renders()

	# 2004: Leap year, starting on Thursday
	assert '[2004, 1, 3]' == T('<?print repr(@(2004-01-01).calendar())?>').renders()
	assert '[2004, 1, 3]' == T('<?print repr(@(2004-01-01).calendar(6, 1))?>').renders()
	assert '[2003, 52, 3]' == T('<?print repr(@(2004-01-01).calendar(0, 7))?>').renders()
	assert '[2004, 1, 6]' == T('<?print repr(@(2004-01-04).calendar())?>').renders()
	assert '[2004, 2, 0]' == T('<?print repr(@(2004-01-05).calendar())?>').renders()
	assert '[2004, 52, 6]' == T('<?print repr(@(2004-12-26).calendar())?>').renders()
	assert '[2004, 53, 0]' == T('<?print repr(@(2004-12-27).calendar())?>').renders()

	# 2010: Non-leap year, starting on Friday
	assert '[2009, 53, 4]' == T('<?print repr(@(2010-01-01).calendar())?>').renders()
	assert '[2010, 1, 4]' == T('<?print repr(@(2010-01-01).calendar(6, 1))?>').renders()
	assert '[2009, 52, 4]' == T('<?print repr(@(2010-01-01).calendar(0, 7))?>').renders()
	assert '[2009, 53, 6]' == T('<?print repr(@(2010-01-03).calendar())?>').renders()
	assert '[2010, 1, 0]' == T('<?print repr(@(2010-01-04).calendar())?>').renders()
	assert '[2010, 51, 6]' == T('<?print repr(@(2010-12-26).calendar())?>').renders()
	assert '[2010, 52, 0]' == T('<?print repr(@(2010-12-27).calendar())?>').renders()

	# 2016: Leap year, starting on Friday
	assert '[2015, 53, 4]' == T('<?print repr(@(2016-01-01).calendar())?>').renders()
	assert '[2016, 1, 4]' == T('<?print repr(@(2016-01-01).calendar(6, 1))?>').renders()
	assert '[2015, 52, 4]' == T('<?print repr(@(2016-01-01).calendar(0, 7))?>').renders()
	assert '[2015, 53, 6]' == T('<?print repr(@(2016-01-03).calendar())?>').renders()
	assert '[2016, 1, 0]' == T('<?print repr(@(2016-01-04).calendar())?>').renders()
	assert '[2016, 51, 6]' == T('<?print repr(@(2016-12-25).calendar())?>').renders()
	assert '[2016, 52, 0]' == T('<?print repr(@(2016-12-26).calendar())?>').renders()

	# 2011: Non-leap year, starting on Saturday
	assert '[2010, 52, 5]' == T('<?print repr(@(2011-01-01).calendar())?>').renders()
	assert '[2011, 1, 5]' == T('<?print repr(@(2011-01-01).calendar(6, 1))?>').renders()
	assert '[2010, 52, 5]' == T('<?print repr(@(2011-01-01).calendar(0, 7))?>').renders()
	assert '[2010, 52, 6]' == T('<?print repr(@(2011-01-02).calendar())?>').renders()
	assert '[2011, 1, 0]' == T('<?print repr(@(2011-01-03).calendar())?>').renders()
	assert '[2011, 51, 6]' == T('<?print repr(@(2011-12-25).calendar())?>').renders()
	assert '[2011, 52, 0]' == T('<?print repr(@(2011-12-26).calendar())?>').renders()

	# 2000: Leap year, starting on Saturday
	assert '[1999, 52, 5]' == T('<?print repr(@(2000-01-01).calendar())?>').renders()
	assert '[2000, 1, 5]' == T('<?print repr(@(2000-01-01).calendar(6, 1))?>').renders()
	assert '[1999, 52, 5]' == T('<?print repr(@(2000-01-01).calendar(0, 7))?>').renders()
	assert '[1999, 52, 6]' == T('<?print repr(@(2000-01-02).calendar())?>').renders()
	assert '[2000, 1, 0]' == T('<?print repr(@(2000-01-03).calendar())?>').renders()
	assert '[2000, 51, 6]' == T('<?print repr(@(2000-12-24).calendar())?>').renders()
	assert '[2000, 52, 0]' == T('<?print repr(@(2000-12-25).calendar())?>').renders()

	# 2017: Non-leap year, starting on Sunday
	assert '[2016, 52, 6]' == T('<?print repr(@(2017-01-01).calendar())?>').renders()
	assert '[2017, 1, 6]' == T('<?print repr(@(2017-01-01).calendar(6, 1))?>').renders()
	assert '[2016, 52, 6]' == T('<?print repr(@(2017-01-01).calendar(0, 7))?>').renders()
	assert '[2017, 1, 0]' == T('<?print repr(@(2017-01-02).calendar())?>').renders()
	assert '[2017, 51, 6]' == T('<?print repr(@(2017-12-24).calendar())?>').renders()
	assert '[2017, 52, 0]' == T('<?print repr(@(2017-12-25).calendar())?>').renders()

	# 2012: Leap year, starting on Sunday
	assert '[2011, 52, 6]' == T('<?print repr(@(2012-01-01).calendar())?>').renders()
	assert '[2012, 1, 6]' == T('<?print repr(@(2012-01-01).calendar(6, 1))?>').renders()
	assert '[2011, 52, 6]' == T('<?print repr(@(2012-01-01).calendar(0, 7))?>').renders()
	assert '[2012, 1, 0]' == T('<?print repr(@(2012-01-02).calendar())?>').renders()
	assert '[2012, 52, 6]' == T('<?print repr(@(2012-12-30).calendar())?>').renders()
	assert '[2013, 1, 0]' == T('<?print repr(@(2012-12-31).calendar())?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '[2018, 1, 0]' == T('<?print @(2018-01-01).calendar(firstweekday=0, mindaysinfirstweek=4)?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2000-02-29).calendar(1, 2, 3)?>').renders()


@pytest.mark.ul4
def test_method_week(T):
	# 1996: Non-leap year, starting on Monday
	assert '1' == T('<?print repr(@(1996-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(1996-01-01).week(6, 1))?>').renders()
	assert '1' == T('<?print repr(@(1996-01-01).week(0, 7))?>').renders()
	assert '1' == T('<?print repr(@(1996-01-07).week())?>').renders()
	assert '2' == T('<?print repr(@(1996-01-08).week())?>').renders()
	assert '22' == T('<?print repr(@(1996-05-28).week())?>').renders()
	assert '1' == T('<?print repr(@(1996-12-30).week())?>').renders()
	assert '52' == T('<?print repr(@(1996-12-29).week())?>').renders()

	# 2018: Leap year, starting on Monday
	assert '1' == T('<?print repr(@(2018-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2018-01-01).week(6, 1))?>').renders()
	assert '1' == T('<?print repr(@(2018-01-01).week(0, 7))?>').renders()
	assert '1' == T('<?print repr(@(2018-01-07).week())?>').renders()
	assert '2' == T('<?print repr(@(2018-01-08).week())?>').renders()
	assert '52' == T('<?print repr(@(2018-12-30).week())?>').renders()
	assert '1' == T('<?print repr(@(2018-12-31).week())?>').renders()

	# 2013: Non-leap year, starting on Tuesday
	assert '1' == T('<?print repr(@(2013-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2013-01-01).week(6, 1))?>').renders()
	assert '53' == T('<?print repr(@(2013-01-01).week(0, 7))?>').renders()
	assert '1' == T('<?print repr(@(2013-01-06).week())?>').renders()
	assert '2' == T('<?print repr(@(2013-01-07).week())?>').renders()
	assert '52' == T('<?print repr(@(2013-12-29).week())?>').renders()
	assert '1' == T('<?print repr(@(2013-12-30).week())?>').renders()

	# 2008: Leap year, starting on Tuesday
	assert '1' == T('<?print repr(@(2008-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2008-01-01).week(6, 1))?>').renders()
	assert '53' == T('<?print repr(@(2008-01-01).week(0, 7))?>').renders()
	assert '1' == T('<?print repr(@(2008-01-06).week())?>').renders()
	assert '2' == T('<?print repr(@(2008-01-07).week())?>').renders()
	assert '52' == T('<?print repr(@(2008-12-28).week())?>').renders()
	assert '1' == T('<?print repr(@(2008-12-29).week())?>').renders()

	# 2014: Non-leap year, starting on Wednesday
	assert '1' == T('<?print repr(@(2014-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2014-01-01).week(6, 1))?>').renders()
	assert '52' == T('<?print repr(@(2014-01-01).week(0, 7))?>').renders()
	assert '1' == T('<?print repr(@(2014-01-05).week())?>').renders()
	assert '2' == T('<?print repr(@(2014-01-06).week())?>').renders()
	assert '52' == T('<?print repr(@(2014-12-28).week())?>').renders()
	assert '1' == T('<?print repr(@(2014-12-29).week())?>').renders()

	# 1992: Leap year, starting on Wednesday
	assert '1' == T('<?print repr(@(1992-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(1992-01-01).week(6, 1))?>').renders()
	assert '52' == T('<?print repr(@(1992-01-01).week(0, 7))?>').renders()
	assert '1' == T('<?print repr(@(1992-01-05).week())?>').renders()
	assert '2' == T('<?print repr(@(1992-01-06).week())?>').renders()
	assert '52' == T('<?print repr(@(1992-12-27).week())?>').renders()
	assert '53' == T('<?print repr(@(1992-12-28).week())?>').renders()

	# 2015: Non-leap year, starting on Thursday
	assert '1' == T('<?print repr(@(2015-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2015-01-01).week(6, 1))?>').renders()
	assert '52' == T('<?print repr(@(2015-01-01).week(0, 7))?>').renders()
	assert '1' == T('<?print repr(@(2015-01-04).week())?>').renders()
	assert '2' == T('<?print repr(@(2015-01-05).week())?>').renders()
	assert '52' == T('<?print repr(@(2015-12-27).week())?>').renders()
	assert '53' == T('<?print repr(@(2015-12-28).week())?>').renders()

	# 2004: Leap year, starting on Thursday
	assert '1' == T('<?print repr(@(2004-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2004-01-01).week(6, 1))?>').renders()
	assert '52' == T('<?print repr(@(2004-01-01).week(0, 7))?>').renders()
	assert '1' == T('<?print repr(@(2004-01-04).week())?>').renders()
	assert '2' == T('<?print repr(@(2004-01-05).week())?>').renders()
	assert '52' == T('<?print repr(@(2004-12-26).week())?>').renders()
	assert '53' == T('<?print repr(@(2004-12-27).week())?>').renders()

	# 2010: Non-leap year, starting on Friday
	assert '53' == T('<?print repr(@(2010-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2010-01-01).week(6, 1))?>').renders()
	assert '52' == T('<?print repr(@(2010-01-01).week(0, 7))?>').renders()
	assert '53' == T('<?print repr(@(2010-01-03).week())?>').renders()
	assert '1' == T('<?print repr(@(2010-01-04).week())?>').renders()
	assert '51' == T('<?print repr(@(2010-12-26).week())?>').renders()
	assert '52' == T('<?print repr(@(2010-12-27).week())?>').renders()

	# 2016: Leap year, starting on Friday
	assert '53' == T('<?print repr(@(2016-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2016-01-01).week(6, 1))?>').renders()
	assert '52' == T('<?print repr(@(2016-01-01).week(0, 7))?>').renders()
	assert '53' == T('<?print repr(@(2016-01-03).week())?>').renders()
	assert '1' == T('<?print repr(@(2016-01-04).week())?>').renders()
	assert '51' == T('<?print repr(@(2016-12-25).week())?>').renders()
	assert '52' == T('<?print repr(@(2016-12-26).week())?>').renders()

	# 2011: Non-leap year, starting on Saturday
	assert '52' == T('<?print repr(@(2011-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2011-01-01).week(6, 1))?>').renders()
	assert '52' == T('<?print repr(@(2011-01-01).week(0, 7))?>').renders()
	assert '52' == T('<?print repr(@(2011-01-02).week())?>').renders()
	assert '1' == T('<?print repr(@(2011-01-03).week())?>').renders()
	assert '51' == T('<?print repr(@(2011-12-25).week())?>').renders()
	assert '52' == T('<?print repr(@(2011-12-26).week())?>').renders()

	# 2000: Leap year, starting on Saturday
	assert '52' == T('<?print repr(@(2000-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2000-01-01).week(6, 1))?>').renders()
	assert '52' == T('<?print repr(@(2000-01-01).week(0, 7))?>').renders()
	assert '52' == T('<?print repr(@(2000-01-02).week())?>').renders()
	assert '1' == T('<?print repr(@(2000-01-03).week())?>').renders()
	assert '51' == T('<?print repr(@(2000-12-24).week())?>').renders()
	assert '52' == T('<?print repr(@(2000-12-25).week())?>').renders()

	# 2017: Non-leap year, starting on Sunday
	assert '52' == T('<?print repr(@(2017-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2017-01-01).week(6, 1))?>').renders()
	assert '52' == T('<?print repr(@(2017-01-01).week(0, 7))?>').renders()
	assert '1' == T('<?print repr(@(2017-01-02).week())?>').renders()
	assert '51' == T('<?print repr(@(2017-12-24).week())?>').renders()
	assert '52' == T('<?print repr(@(2017-12-25).week())?>').renders()

	# 2012: Leap year, starting on Sunday
	assert '52' == T('<?print repr(@(2012-01-01).week())?>').renders()
	assert '1' == T('<?print repr(@(2012-01-01).week(6, 1))?>').renders()
	assert '52' == T('<?print repr(@(2012-01-01).week(0, 7))?>').renders()
	assert '1' == T('<?print repr(@(2012-01-02).week())?>').renders()
	assert '52' == T('<?print repr(@(2012-12-30).week())?>').renders()
	assert '1' == T('<?print repr(@(2012-12-31).week())?>').renders()

	# Make sure that the parameters have the same name in all implementations
	assert '1' == T('<?print @(2018-01-01).week(firstweekday=0, mindaysinfirstweek=4)?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2000-02-29).week(1, 2, 3)?>').renders()


@pytest.mark.ul4
def test_method_yearday(T):
	assert '1' == T('<?print @(2010-01-01).yearday()?>').renders()
	assert '366' == T('<?print @(2008-12-31).yearday()?>').renders()
	assert '365' == T('<?print @(2010-12-31).yearday()?>').renders()
	assert '132' == T('<?print @(2010-05-12).yearday()?>').renders()
	assert '132' == T('<?print @(2010-05-12T16:47:56).yearday()?>').renders()
	assert '132' == T('<?print d.yearday()?>').renders(d=datetime.date(2010, 5, 12))
	assert '132' == T('<?print d.yearday()?>').renders(d=datetime.datetime(2010, 5, 12, 16, 47, 56))
	assert '1' == T('<?code m = @(2010-01-01).yearday?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print @(2000-02-29).yearday(42)?>').renders()


@pytest.mark.ul4
def test_method_days(T):
	assert '1' == T('<?print timedelta(1).days()?>').renders()
	assert '1' == T('<?code m = timedelta(1).days?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print timedelta(1).days(42)?>').renders()


@pytest.mark.ul4
def test_method_seconds(T):
	assert '42' == T('<?print timedelta(0, 42).seconds()?>').renders()
	assert '42' == T('<?code m = timedelta(0, 42).seconds?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print timedelta(1).seconds(42)?>').renders()


@pytest.mark.ul4
def test_method_microseconds(T):
	assert '123000' == T('<?print timedelta(0, 0, 123000).microseconds()?>').renders()
	assert '123000' == T('<?code m = timedelta(0, 0, 123000).microseconds?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print timedelta(1).microseconds(42)?>').renders()


@pytest.mark.ul4
def test_method_months(T):
	assert '17' == T('<?print monthdelta(17).months()?>').renders()
	assert '17' == T('<?code m = monthdelta(17).months?><?print m()?>').renders()

	with raises(argumentmismatchmessage):
		T('<?print monthdelta(1).months(42)?>').renders()


@pytest.mark.ul4
def test_method_append(T):
	assert '[17, 23, 42]' == T('<?code l = [17]?><?code l.append(23, 42)?><?print l?>').renders()
	assert '[17, 23, 42]' == T('<?code l = [17]?><?code m = l.append?><?code m(23, 42)?><?print l?>').renders()


@pytest.mark.ul4
def test_method_insert(T):
	assert '[1, 2, 3, 4]' == T('<?code l = [1,4]?><?code l.insert(1, 2, 3)?><?print l?>').renders()
	assert '[1, 2, 3, 4]' == T('<?code l = [1,4]?><?code m = l.insert?><?code m(1, 2, 3)?><?print l?>').renders()


@pytest.mark.ul4
def test_method_pop(T):
	assert '42;17;23;' == T('<?code l = [17, 23, 42]?><?print l.pop()?>;<?print l.pop(-2)?>;<?print l.pop(0)?>;').renders()
	assert '42;17;23;' == T('<?code l = [17, 23, 42]?><?code m = l.pop?><?print m()?>;<?print m(-2)?>;<?print m(0)?>;').renders()
	assert '23;73;{}' == T('<?code d = {17: 23, 42: 73}?><?print d.pop(17)?>;<?print d.pop(42)?>;<?print d?>').renders()
	assert '23;42;{42: 73}' == T('<?code d = {17: 23, 42: 73}?><?print d.pop(17)?>;<?print d.pop(43, 42)?>;<?print d?>').renders()


@pytest.mark.ul4
def test_method_update(T):
	assert '0' == T('<?code d = {}?><?code d.update()?><?print len(d)?>').renders()
	assert '1' == T('<?code d = {}?><?code d.update([["one", 1]])?><?print d.one?>').renders()
	assert '1' == T('<?code d = {}?><?code d.update({"one": 1})?><?print d.one?>').renders()
	assert '1' == T('<?code d = {}?><?code d.update(one=1)?><?print d.one?>').renders()
	assert '1' == T('<?code d = {}?><?code d.update([["one", 0]], {"one": 0}, one=1)?><?print d.one?>').renders()
	assert '1' == T('<?code d = {}?><?code m = d.update?><?code m(one=1)?><?print d.one?>').renders()


@pytest.mark.ul4
def test_method_clear(T):
	assert '0' == T('<?code d = {"foo": 17, "bar": 23}?><?code d.clear()?><?print len(d)?>').renders()
	assert '0' == T('<?code d = {"foo", "bar"}?><?code d.clear()?><?print len(d)?>').renders()


@pytest.mark.ul4
def test_def(T):
	assert 'foo' == T('<?def lower?><?print x.lower()?><?end def?><?print lower.renders(x="FOO")?>').renders()


@pytest.mark.ul4
def test_render(T):
	t = ul4c.Template('<?print prefix?><?print data?><?print suffix?>')

	assert '<f><o><o>' == T('<?for c in data?><?render t(data=c, prefix="<", suffix=">")?><?end for?>').renders(t=t, data='foo')
	assert '<f><o><o>' == T('<?for c in data?><?render t(data=c, **{"prefix": "<", "suffix": ">"})?><?end for?>').renders(t=t, data='foo')


@pytest.mark.ul4
def test_renderx(T):
	t = ul4c.Template("<?print prefix?><?print data?><?print suffix?>")

	assert "&lt;f&gt;&lt;&amp;&gt;&lt;o&gt;&lt;&amp;&gt;&lt;o&gt;" == T('<?for c in data?><?renderx t(data=c, prefix="<", suffix=">")?><?end for?>').renders(t=t, data='f&o&o')


@pytest.mark.ul4
def test_render_or_print(T):
	assert "<&><&>" == T("<?def x?><&><?end def?><?render_or_print x()?><?render_or_print '<&>'()?>").renders()


@pytest.mark.ul4
def test_render_or_printx(T):
	assert "<&>&lt;&amp;&gt;" == T("<?def x?><&><?end def?><?render_or_printx x()?><?render_or_printx '<&>'()?>").renders()


@pytest.mark.ul4
def test_renderx_or_print(T):
	assert "&lt;&amp;&gt;<&>" == T("<?def x?><&><?end def?><?renderx_or_print x()?><?renderx_or_print '<&>'()?>").renders()


@pytest.mark.ul4
def test_renderx_or_printx(T):
	assert "&lt;&amp;&gt;&lt;&amp;&gt;" == T("<?def x?><&><?end def?><?renderx_or_printx x()?><?renderx_or_printx '<&>'()?>").renders()


@pytest.mark.ul4
def test_renderblock(T):
	t1 = T("""
		<?whitespace strip?>
		<?def bracket(content, prefix="(", suffix=")")?>
			<?print prefix?><?render content()?><?print suffix?>
		<?end def?>
		<?renderblock bracket()?>
			gurk
		<?end renderblock?>
	""")

	assert '(gurk)' == t1.renders()

	# Check that the local template is named "content" and has no signature
	t2 = T("""
		<?whitespace strip?>
		<?def bracket(content)?>
			(<?print content.name?>|<?print repr(content.signature)?>)
		<?end def?>
		<?renderblock bracket()?>
			gurk
		<?end renderblock?>
	""")

	assert '(content|None)' == t2.renders()

	# Check that the call tests for a duplicate "content" argument
	t3 = T("""
		<?whitespace strip?>
		<?def bracket(content)?>
			gurk
		<?end def?>
		<?renderblock bracket(content=42)?>
			gurk
		<?end renderblock?>
	""")

	with raises(duplicatekeywordargument):
		t3.renders()

	# Check that the "content" template is added to the end of the keyword arguments
	t4 = T("""
		<?whitespace strip?>
		<?def bracket(**kwargs)?>
			<?print repr(list(kwargs))?>
		<?end def?>
		<?renderblock bracket(a=17, b=23)?>
			gurk
		<?end renderblock?>
	""")

	assert "['a', 'b', 'content']" == t4.renders()

	# Check that the content template doesn't leak into the surrounding scope
	t5 = T("""
		<?whitespace strip?>
		<?def bracket(content)?>
		<?end def?>
		<?renderblock bracket()?>
			gurk
		<?end renderblock?>
		<?print type(content)?>
	""")

	assert t5.renders() in {"<type undefinedvariable>", "<type undefined>"}


@pytest.mark.ul4
def test_renderblocks(T):
	t1 = T("""
		<?whitespace strip?>
		<?def bracket(content, prefix, suffix)?>
			<?if istemplate(prefix)?>
				<?render prefix()?>
			<?else?>
				<?print prefix?>
			<?end if?>
			<?if istemplate(content)?>
				<?render content()?>
			<?else?>
				<?print content?>
			<?end if?>
			<?if istemplate(suffix)?>
				<?render suffix()?>
			<?else?>
				<?print suffix?>
			<?end if?>
		<?end def?>
		<?renderblocks bracket()?>
			<?def prefix?>(<?end def?>
			<?def content?>gurk<?end def?>
			<?def suffix?>)<?end def?>
		<?end renderblocks?>
		<?renderblocks bracket(prefix="(", suffix=")")?>
			<?def content?>hurz<?end def?>
		<?end renderblocks?>
	""")

	assert '(gurk)(hurz)' == t1.renders()

	# <?renderblocks?> should complain about unknown arguments
	t2 = T("""
		<?whitespace strip?>
		<?def bracket(content, prefix, suffix)?>
		<?end def?>
		<?renderblocks bracket(wrong=42)?>
			<?def prefix?>(<?end def?>
			<?def content?>gurk<?end def?>
			<?def suffix?>)<?end def?>
		<?end renderblocks?>
	""")

	with raises(unknownkeywordargument):
		t2.renders()

	# Check that <?renderblocks?> complains about missing arguments
	t3 = T("""
		<?whitespace strip?>
		<?def bracket(content, prefix, suffix)?>
		<?end def?>
		<?renderblocks bracket()?>
		<?end renderblocks?>
	""")

	with raises(argumentmismatchmessage):
		t3.renders()

	# Check that <?renderblocks?> checks for duplicate arguments
	t4 = T("""
		<?whitespace strip?>
		<?def bracket(content, prefix, suffix)?>
		<?end def?>
		<?renderblocks bracket(prefix="(", suffix=")")?>
			<?def prefix?>(<?end def?>
			<?def content?>gurk<?end def?>
			<?def suffix?>)<?end def?>
		<?end renderblocks?>
	""")

	with raises(duplicatekeywordargument):
		t4.renders()

	# Check that the template arguments are added to the end of the call
	t5 = T("""
		<?whitespace strip?>
		<?def bracket(**kwargs)?>
			<?print repr(list(kwargs))?>
		<?end def?>
		<?renderblocks bracket(a=17, b=23, c=42)?>
			<?code prefix = "("?>
			<?def content?>gurk<?end def?>
			<?code suffix = ")"?>
		<?end renderblocks?>
	""")

	assert "['a', 'b', 'c', 'prefix', 'content', 'suffix']" == t5.renders()

	# Check that the template arguments don't leak into the surrounding scope
	t6 = T("""
		<?whitespace strip?>
		<?def bracket(**kwargs)?>
		<?end def?>
		<?renderblocks bracket()?>
			<?def prefix?>(<?end def?>
			<?def content?>gurk<?end def?>
			<?def suffix?>)<?end def?>
		<?end renderblocks?>
		<?print type(prefix)?>
		<?print type(content)?>
		<?print type(suffix)?>
	""")

	assert t6.renders() in {"<type undefinedvariable>" * 3, "<type undefined>" * 3}


@pytest.mark.ul4
def test_pass_function(T):
	assert "&lt;" == T("<?def x?><?print xe('<')?><?end def?><?render x(xe=xmlescape)?>").renders()
	assert "&lt;" == T("<?def xe?><?return xmlescape(s)?><?end def?><?def x?><?print xe(s='<')?><?end def?><?render x(xe=xe)?>").renders()
	assert "&lt;" == T("<?def xe?><?return xmlescape(s)?><?end def?><?def x?><?print xe(s='<')?><?end def?><?render x()?>").renders()


@pytest.mark.ul4
def test_parse(T):
	assert '42' == T('<?print data.Noner?>').renders(data=dict(Noner=42))


@pytest.mark.ul4
def test_nested_exceptions(T):
	tmpl1 = ul4c.Template("<?print 2*x?>", "tmpl1")
	tmpl2 = ul4c.Template("<?render tmpl1(x=x)?>", "tmpl2")
	tmpl3 = ul4c.Template("<?render tmpl2(tmpl1=tmpl1, x=x)?>", "tmpl3")

	with raises("unsupported operand type|not supported"):
		T("<?render tmpl3(tmpl1=tmpl1, tmpl2=tmpl2, x=x)?>").renders(tmpl1=tmpl1, tmpl2=tmpl2, tmpl3=tmpl3, x=None)


@pytest.mark.ul4
def test_note(T):
	assert "foo" == T("f<?note This is?>o<?note a comment?>o").renders()


@pytest.mark.ul4
def test_doc_attr():
	template = ul4c.Template("<?doc foo?><?def inner?><?doc innerfoo?><?doc innerbar?><?end def?><?doc bar?><?printx inner.doc?>")
	assert "foo" == template.doc


@pytest.mark.ul4
def test_doc(T):
	assert "innerfoo" == T("<?doc foo?><?def inner?><?doc innerfoo?><?doc innerbar?><?end def?><?doc bar?><?printx inner.doc?>").renders()


@pytest.mark.ul4
def test_exception(T):
	if T in (TemplatePython, TemplatePythonDumpS, TemplatePythonDump):
		assert "None" == T("<?print repr(exc.context)?>").renders(exc=ValueError("broken"))
		exc = ValueError("broken")
		exc.__cause__ = ValueError("because")
		assert "<type ValueError>" == T("<?print type(exc.context)?>").renders(exc=exc)
		assert "because" == T("<?print exc.context?>").renders(exc=exc)

		stacktrace = """
			<?ul4 stacktrace(exc)?>
			<?whitespace strip?>
			<?while exc is not None?>
				<?code texc = type(exc)?>
				<?if exc.location?>
					<?if texc.__module__?><?print texc.__module__?>.<?end if?><?print texc.__name__?>: <?print repr(exc.location.source)?>
				<?else?>
					<?if texc.__module__?><?print texc.__module__?>.<?end if?><?print texc.__name__?>: <?print exc?>
				<?end if?>
				<?print "\\n"?>
				<?code exc = exc.context?>
			<?end while?>
		"""

		expected = [
			"TypeError: unsupported operand type(s) for *: 'NoneType' and 'NoneType'",
			"ll.ul4c.LocationError: 'x*x'",
			"ll.ul4c.LocationError: 'inner(x)'",
			"ll.ul4c.LocationError: 'outer(x)'",
		]

		try:
			T("<?def outer(x)?>\n<?def inner(x)?>\n<?return x*x?>\n<?end def?>\n<?return inner(x)?>\n<?end def?>\n<?return outer(x)?>\n")(x=None)
		except Exception as exc:
			assert expected == T(stacktrace).renders(exc=exc).splitlines()


@pytest.mark.ul4
def test_astattributes(T):
	s1 = "<?print x?>"
	t1 = ul4c.Template(s1, name="t1")

	s2 = "<?printx 42?>"
	t2 = ul4c.Template(s2, name="t2")

	assert "t1" == T("<?print template.template.name?>").renders(template=t1)
	assert "None" == T("<?print repr(template.parenttemplate)?>").renders(template=t1)
	assert "2" == T("<?print len(template.content)?>").renders(template=t1) # The template AST always contains an :class:`Indent` node at the start
	assert "(indent) (print)" == T("<?print ' '.join('(' + ast.type + ')' for ast in template.content)?>").renders(template=t1)
	assert "t1" == T("<?print template.content[0].template.name?>").renders(template=t1)
	assert "t1" == T("<?print template.content[1].template.name?>").renders(template=t1)
	assert "<?print x?>" == T("<?print template.content[1].source?>").renders(template=t1)
	assert "x" == T("<?print template.content[1].obj.source?>").renders(template=t1)
	assert "var" == T("<?print template.content[1].obj.type?>").renders(template=t1)
	assert "x" == T("<?print template.content[1].obj.name?>").renders(template=t1)
	assert "printx" == T("<?print template.content[1].type?>").renders(template=t2)
	assert "const" == T("<?print template.content[1].obj.type?>").renders(template=t2)
	assert "42" == T("<?print template.content[1].obj.value?>").renders(template=t2)
	assert "inner" == T("<?def inner?><?end def?><?print inner.template.name?>", name="foo").renders()
	assert "foo" == T("<?def inner?><?end def?><?print inner.parenttemplate.name?>", name="foo").renders()


	s3 = "[<?print x?>]"
	t3 = ul4c.Template(s3, name="t")

	assert "slice(1, 12, None)" == T("<?print template.content[2].pos?>").renders(template=t3)
	assert "slice(9, 10, None)" == T("<?print template.content[2].obj.pos?>").renders(template=t3)
	assert "slice(9, 10, None)" == T("<?print template.content[2].obj.startpos?>").renders(template=t3)
	assert "1" == T("<?print template.content[2].obj.startline?>").renders(template=t3)
	assert "10" == T("<?print template.content[2].obj.startcol?>").renders(template=t3)
	assert "[<?print " == T("<?print template.content[2].obj.sourceprefix?>").renders(template=t3)
	assert "?>]" == T("<?print template.content[2].obj.sourcesuffix?>").renders(template=t3)
	assert "[<?print " == T("<?print template.content[2].obj.startsourceprefix?>").renders(template=t3)
	assert "?>]" == T("<?print template.content[2].obj.startsourcesuffix?>").renders(template=t3)
	assert "x" == T("<?print template.content[2].obj.startsource?>").renders(template=t3)
	assert "x" == T("<?print template.content[2].obj.source?>").renders(template=t3)


@pytest.mark.ul4
def test_astattribute_source_node(T):
	s = "<?print x?>"
	t = ul4c.Template(s, name="t")

	assert "slice(0, 11, None)" == T("<?print template.content[-1].startpos?>").renders(template=t)
	assert s == T("<?print template.content[-1].startsource?>").renders(template=t)
	assert s == T("<?print template.content[-1].source?>").renders(template=t)
	assert "x" == T("<?print template.content[-1].obj.source?>").renders(template=t)
	assert "x" == T("<?print template.content[-1].obj.startsource?>").renders(template=t)
	assert s == T("<?print template.content[-1].fullsource?>").renders(template=t)
	assert "<?print " == T("<?print template.content[-1].obj.sourceprefix?>").renders(template=t)
	assert "?>" == T("<?print template.content[-1].obj.sourcesuffix?>").renders(template=t)
	assert "<?print " == T("<?print template.content[-1].obj.startsourceprefix?>").renders(template=t)
	assert "?>" == T("<?print template.content[-1].obj.startsourcesuffix?>").renders(template=t)


@pytest.mark.ul4
def test_astattribute_source_template(T):
	s = "<?print x?>"
	t = ul4c.Template(s, name="t")

	assert "slice(0, 0, None)" == T("<?print template.startpos?>").renders(template=t)
	assert "slice(11, 11, None)" == T("<?print template.stoppos?>").renders(template=t)
	assert "" == T("<?print template.startsource?>").renders(template=t)
	assert s == T("<?print template.source?>").renders(template=t)
	assert "" == T("<?print template.stopsource?>").renders(template=t)
	assert s == T("<?print template.fullsource?>").renders(template=t)
	assert "" == T("<?print template.sourceprefix?>").renders(template=t)
	assert "" == T("<?print template.sourcesuffix?>").renders(template=t)
	assert "" == T("<?print template.startsourceprefix?>").renders(template=t)
	assert s == T("<?print template.startsourcesuffix?>").renders(template=t)
	assert s == T("<?print template.stopsourceprefix?>").renders(template=t)
	assert "" == T("<?print template.stopsourcesuffix?>").renders(template=t)


@pytest.mark.ul4
def test_astattribute_source_renderblock(T):
	s = "<?def b(content)?><b><?render content()?></b><?end def?><?renderblock b()?>foo<?end renderblock?>"
	t = ul4c.Template(s, name="t")

	assert "slice(56, 75, None)" == T("<?print template.content[-1].startpos?>", name="foo").renders(template=t)
	assert "slice(78, 97, None)" == T("<?print template.content[-1].stoppos?>", name="foo").renders(template=t)
	assert "<?renderblock b()?>" == T("<?print template.content[-1].startsource?>", name="foo").renders(template=t)
	assert "<?renderblock b()?>foo<?end renderblock?>" == T("<?print template.content[-1].source?>", name="foo").renders(template=t)
	assert "<?end renderblock?>" == T("<?print template.content[-1].stopsource?>", name="foo").renders(template=t)
	assert "slice(75, 75, None)" == T("<?print template.content[-1].content.startpos?>", name="foo").renders(template=t)
	assert "slice(78, 78, None)" == T("<?print template.content[-1].content.stoppos?>", name="foo").renders(template=t)
	assert "" == T("<?print template.content[-1].content.startsource?>", name="foo").renders(template=t)
	assert "foo" == T("<?print template.content[-1].content.source?>", name="foo").renders(template=t)
	assert "" == T("<?print template.content[-1].content.stopsource?>", name="foo").renders(template=t)
	assert s == T("<?print template.content[-1].content.fullsource?>", name="foo").renders(template=t)

	assert "\N{HORIZONTAL ELLIPSIS}?><b><?render content()?></b><?end def?>" == T("<?print template.content[-1].sourceprefix?>", name="foo").renders(template=t)
	assert "" == T("<?print template.content[-1].sourcesuffix?>", name="foo").renders(template=t)
	assert "\N{HORIZONTAL ELLIPSIS}?><b><?render content()?></b><?end def?>" == T("<?print template.content[-1].startsourceprefix?>", name="foo").renders(template=t)
	assert "foo<?end renderblock?>" == T("<?print template.content[-1].startsourcesuffix?>", name="foo").renders(template=t)
	assert "\N{HORIZONTAL ELLIPSIS})?></b><?end def?><?renderblock b()?>foo" == T("<?print template.content[-1].stopsourceprefix?>", name="foo").renders(template=t)
	assert "" == T("<?print template.content[-1].stopsourcesuffix?>", name="foo").renders(template=t)

	assert "\N{HORIZONTAL ELLIPSIS}nt()?></b><?end def?><?renderblock b()?>" == T("<?print template.content[-1].content.sourceprefix?>", name="foo").renders(template=t)
	assert "<?end renderblock?>" == T("<?print template.content[-1].content.sourcesuffix?>", name="foo").renders(template=t)
	assert "\N{HORIZONTAL ELLIPSIS}nt()?></b><?end def?><?renderblock b()?>" == T("<?print template.content[-1].content.startsourceprefix?>", name="foo").renders(template=t)
	assert "foo<?end renderblock?>" == T("<?print template.content[-1].content.startsourcesuffix?>", name="foo").renders(template=t)
	assert "\N{HORIZONTAL ELLIPSIS})?></b><?end def?><?renderblock b()?>foo" == T("<?print template.content[-1].content.stopsourceprefix?>", name="foo").renders(template=t)
	assert "<?end renderblock?>" == T("<?print template.content[-1].content.stopsourcesuffix?>", name="foo").renders(template=t)


@pytest.mark.ul4
def test_astattribute_source_renderblocks(T):
	s = "<?def b(content)?><b><?render content()?></b><?end def?><?renderblocks b()?><?def content?>foo<?end def?><?end renderblocks?>"
	t = ul4c.Template(s, name="t")

	assert "slice(56, 76, None)" == T("<?print template.content[-1].startpos?>", name="foo").renders(template=t)
	assert "slice(105, 125, None)" == T("<?print template.content[-1].stoppos?>", name="foo").renders(template=t)
	assert "<?renderblocks b()?>" == T("<?print template.content[-1].startsource?>", name="foo").renders(template=t)
	assert "<?renderblocks b()?><?def content?>foo<?end def?><?end renderblocks?>" == T("<?print template.content[-1].source?>", name="foo").renders(template=t)
	assert "<?end renderblocks?>" == T("<?print template.content[-1].stopsource?>", name="foo").renders(template=t)
	assert "<?def content?>foo<?end def?>" == T("<?print template.content[-1].content[0].source?>", name="foo").renders(template=t)
	assert s == T("<?print template.content[-1].content[0].fullsource?>", name="foo").renders(template=t)


@pytest.mark.ul4
def test_astattribute_source_for(T):
	s = "<?for i in range(10)?><?printx i?><?end for?>"
	t = ul4c.Template(s, name="t")

	assert "<?for i in range(10)?>" == T("<?print template.content[-1].startsource?>", name="foo").renders(template=t)
	assert s == T("<?print template.content[-1].source?>", name="foo").renders(template=t)
	assert "<?end for?>" == T("<?print template.content[-1].stopsource?>", name="foo").renders(template=t)
	assert s == T("<?print template.content[-1].fullsource?>", name="foo").renders(template=t)


@pytest.mark.ul4
def test_astattribute_source_while(T):
	s = "<?while now() < @(2020-02-02)?>wait<?end while?>"
	t = ul4c.Template(s, name="t")

	assert "<?while now() < @(2020-02-02)?>" == T("<?print template.content[-1].startsource?>", name="foo").renders(template=t)
	assert s == T("<?print template.content[-1].source?>", name="foo").renders(template=t)
	assert "<?end while?>" == T("<?print template.content[-1].stopsource?>", name="foo").renders(template=t)
	assert s == T("<?print template.content[-1].fullsource?>", name="foo").renders(template=t)


@pytest.mark.ul4
def test_astattribute_source_if(T):
	s = "<?if 1?>1<?elif 2?>2<?else?>3<?end if?>"
	t = ul4c.Template(s, name="t")

	assert "<?if 1?>" == T("<?print template.content[-1].startsource?>", name="foo").renders(template=t)
	assert s == T("<?print template.content[-1].source?>", name="foo").renders(template=t)
	assert "<?end if?>" == T("<?print template.content[-1].stopsource?>", name="foo").renders(template=t)
	assert "<?if 1?>" == T("<?print template.content[-1].content[0].startsource?>", name="foo").renders(template=t)
	assert "<?if 1?>1" == T("<?print template.content[-1].content[0].source?>", name="foo").renders(template=t)
	assert "" == T("<?print template.content[-1].content[0].stopsource?>", name="foo").renders(template=t)
	assert "<?elif 2?>" == T("<?print template.content[-1].content[1].startsource?>", name="foo").renders(template=t)
	assert "<?elif 2?>2" == T("<?print template.content[-1].content[1].source?>", name="foo").renders(template=t)
	assert "" == T("<?print template.content[-1].content[1].stopsource?>", name="foo").renders(template=t)
	assert "<?else?>" == T("<?print template.content[-1].content[2].startsource?>", name="foo").renders(template=t)
	assert "<?else?>3" == T("<?print template.content[-1].content[2].source?>", name="foo").renders(template=t)
	assert "" == T("<?print template.content[-1].content[2].stopsource?>", name="foo").renders(template=t)
	assert s == T("<?print template.content[-1].fullsource?>", name="foo").renders(template=t)


@pytest.mark.ul4
def test_templateattributes_localtemplate(T):
	# This checks that template attributes work on a closure
	source = "<?def lower?><?print t.lower()?><?end def?>"

	assert "<?def lower?>" == T(source + "<?print lower.startsource?>").renders()
	assert source == T(source + "<?print lower.source?>").renders()
	assert "<?end def?>" == T(source + "<?print lower.stopsource?>").renders()
	assert source == T(source + "<?print lower.template.source?>").renders()
	assert source + "<?print lower.parenttemplate.source?>" == T(source + "<?print lower.parenttemplate.source?>").renders()
	assert "<?print t.lower()?>" == T(source + "<?print lower.source[lower.content[0].startpos.start:lower.content[-1].startpos.stop]?>").renders()
	assert "lower" == T(source + "<?print lower.name?>").renders()


@pytest.mark.ul4
def test_nestedscopes(T):
	# Subtemplates can see the local variables from their parents
	source = """
	<?for i in range(3)?>
		<?def x?>
			<?print i?>!
		<?end def?>
		<?render x()?>
	<?end for?>
	"""
	assert "0!1!2!" == T(source, whitespace="strip").renders()

	# Subtemplates see the final state of the variable at the point were they are called,
	# so the following code will use ``i = 2`` as the call happens after the variable reassignment
	source = """
	<?code i = 1?>
	<?def x?>
		<?print i?>
	<?end def?>
	<?code i = 2?>
	<?render x()?>
	"""
	assert "2" == T(source, whitespace="strip").renders()


	# Subtemplates see themselves (i.e. the ``TemplateClosure`` object created for them)
	source = """
	<?def x?>
		<?print type(x)?>;<?print type(y)?>
	<?end def?>
	<?code y = 42?>
	<?render x()?>
	"""
	assert "<type ul4.TemplateClosure>;<type int>" == T(source, whitespace="strip").renders()

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
		<?render inner(x=x)?>
		<?print x?>!
		<?print y?>!
	<?end def?>
	<?code x += 1?>
	<?code y += 1?>
	<?render outer(x=x)?>
	<?print x?>!
	<?print y?>!
	"""

	assert "45!45!44!44!43!43!" == T(source, whitespace="strip").renders(x=42, y=42)


def universaltemplate(whitespace="keep"):
	return ul4c.Template(
		"""
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
			<?code x = {x*x for x in range(10) if i % 2}?>
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
			<?for x in "12"?>
				<?print x?>
				<?break?>
				<?continue?>
			<?end for?>
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
			<?if x?>
				gurk
			<?elif y?>
				hurz
			<?else?>
				hinz
			<?end if?>
			<?render x(a=1, b=2)?>
			<?def x?>
				foo
			<?end def?>
			<?def x(arg)?>
				foo
			<?end def?>
			<?def x?>
				<?return x?>
			<?end def?>
			<?def x(arg)?>
				<?return x?>
			<?end def?>
			<?render x()?>
		""",
		whitespace=whitespace
	)


@pytest.mark.ul4
def test_strtemplate():
	t1 = universaltemplate("keep")
	str(t1)

	t2 = universaltemplate("strip")
	str(t2)

	t3 = universaltemplate("smart")
	str(t3)


@pytest.mark.ul4
def test_whitespace():
	s = """
		<?for i in range(10)?>
			<?print i?>
			;
		<?end for?>
	"""
	t1 = ul4c.Template(s, whitespace="keep")
	output1 = t1.renders()
	t2 = ul4c.Template(s, whitespace="strip")
	output2 = t2.renders()
	assert output1 != output2
	assert "".join(output1.split()) == output2


@pytest.mark.ul4
def test_whitespace_initialws(T):
	assert " foo" == T("<?if True?> foo<?end if?>", whitespace="strip").renders()
	assert " foobar" == T("<?if True?> foo\n \tbar<?end if?>", whitespace="strip").renders()


@pytest.mark.ul4
def test_whitespace_nested(T):
	s1 = "<?def nested1?>1n\n<?render second()?><?end def?>1\n<?render nested1(second=second)?>"
	s2 = "<?def nested2?>2n\n<?end def?>2\n<?render nested2()?>"

	assert "1\n1n\n22n" == T(s1, whitespace="keep").renders(second=ul4c.Template(s2, whitespace="strip"))
	assert "11n2\n2n\n" == T(s1, whitespace="strip").renders(second=ul4c.Template(s2, whitespace="keep"))


@pytest.mark.ul4
def test_function(T):
	assert 42 == T("<?return 42?>")()


@pytest.mark.ul4
def test_function_value(T):
	assert 84 == T("<?return 2*x?>")(x=42)


@pytest.mark.ul4
def test_function_multiple_returnvalues(T):
	assert 84 == T("<?return 2*x?><?return 3*x?>")(x=42)


@pytest.mark.ul4
def test_function_name(T):
	assert "f" == T("<?def f?><?return f.name?><?end def?><?return f(f=f)?>")()


@pytest.mark.ul4
def test_function_closure(T):
	assert 24 == T("<?code y=3?><?def inner?><?return 2*x*y?><?end def?><?return inner(x=4)?>")()
	assert 24 == T("<?def outer?><?code y=3?><?def inner?><?return 2*x*y?><?end def?><?return inner?><?end def?><?return outer()(x=4)?>")()
	assert 42 == T("<?def inner?><?return x?><?end def?><?return inner()?>")(x=42)


@pytest.mark.ul4
def test_template_closure(T):
	assert "24" == T("<?code f = []?><?def outer()?><?code y=3?><?def inner(x)?><?print 2*x*y?><?end def?><?code f.append(inner)?><?end def?><?code outer()?><?render f[0](x=4)?>").renders()
	assert "42" == T("<?def inner?><?print x?><?end def?><?render inner()?>").render(x=42)


@pytest.mark.ul4
def test_renders_closure(T):
	assert "42" == T("<?def inner?><?print x?><?end def?><?print inner.renders()?>").render(x=42)


@pytest.mark.ul4
def test_return_in_template(T):
	assert "gurk" == T("gurk<?return 42?>hurz").renders()


@pytest.mark.ul4
def test_customattributes():
	class CustomAttributes:
		ul4_attrs = {"foo", "bar"}

		def __init__(self, foo, bar):
			self.foo = foo
			self.bar = bar

		def ul4_getattr(self, name):
			return getattr(self, name)

		def ul4_setattr(self, name, value):
			if name == "foo":
				self.foo = value
			elif name == "bar":
				raise TypeError(f"readonly attribute {name!r}")
			else:
				raise AttributeError(name)

	o = CustomAttributes(foo=42, bar=23)
	assert "42" == TemplatePython("<?print o.foo?>").renders(o=o)
	assert "23" == TemplatePython("<?print o.bar?>").renders(o=o)
	assert "undefinedkey" == TemplatePython("<?print type(o.baz).__name__?>").renders(o=o)

	readonlymessage = "readonly"

	o = CustomAttributes(foo=23, bar=42)
	assert "17" == TemplatePython("<?code o.foo = 17?><?print o.foo?>").renders(o=o)
	with raises(readonlymessage):
		TemplatePython("<?code o.bar = 43?>").renders(o=o)

	o = CustomAttributes(foo=23, bar=42)
	assert "24" == TemplatePython("<?code o.foo += 1?><?print o.foo?>").renders(o=o)
	with raises(readonlymessage):
		TemplatePython("<?code o.bar += 1?>").renders(o=o)

	o = CustomAttributes(foo=23, bar=42)
	assert "22" == TemplatePython("<?code o.foo -= 1?><?print o.foo?>").renders(o=o)
	with raises(readonlymessage):
		TemplatePython("<?code o.bar -= 1?>").renders(o=o)

	o = CustomAttributes(foo=23, bar=42)
	assert "46" == TemplatePython("<?code o.foo *= 2?><?print o.foo?>").renders(o=o)
	with raises(readonlymessage):
		TemplatePython("<?code o.bar *= 2?>").renders(o=o)

	o = CustomAttributes(foo=23, bar=42)
	assert "11" == TemplatePython("<?code o.foo //= 2?><?print o.foo?>").renders(o=o)
	with raises(readonlymessage):
		TemplatePython("<?code o.bar //= 2?>").renders(o=o)

	o = CustomAttributes(foo=23, bar=42)
	assert "11.5" == TemplatePython("<?code o.foo /= 2?><?print o.foo?>").renders(o=o)
	with raises(readonlymessage):
		TemplatePython("<?code o.bar /= 2?>").renders(o=o)

	o = CustomAttributes(foo=23, bar=42)
	assert "3" == TemplatePython("<?code o.foo %= 10?><?print o.foo?>").renders(o=o)
	with raises(readonlymessage):
		TemplatePython("<?code o.bar %= 2?>").renders(o=o)

	# UL4 no longer tries to support dict access to custom objects,
	# so all the following code should raise exceptions
	with raises("is not callable"):
		TemplatePython("<?print o.items()?>").renders(o=o)
	with raises("is not callable"):
		TemplatePython("<?print o.values()?>").renders(o=o)
	with raises("is not iterable"):
		TemplatePython("<?for attr in o?><?end for?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?print o['foo']?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?print o['bar']?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['foo'] = 17?><?print o.foo?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['foo'] += 1?><?print o.foo?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['foo'] -= 1?><?print o.foo?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['bar'] -= 1?><?print o.bar?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['foo'] *= 2?><?print o.foo?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['bar'] *= 2?><?print o.bar?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['foo'] //= 2?><?print o.foo?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['bar'] //= 2?><?print o.bar?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['foo'] /= 2?><?print o.foo?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['bar'] /= 2?><?print o.bar?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['foo'] %= 2?><?print o.foo?>").renders(o=o)
	with raises(subscriptablemessage):
		TemplatePython("<?code o['bar'] %= 2?><?print o.bar?>").renders(o=o)


@pytest.mark.ul4
def test_custommethods():
	class CustomMethod:
		def foo(self):
			return 42

		@ul4c.withcontext
		def bar(self, context):
			return len(context.vars.maps[0])

		def baz(self):
			pass

		def ul4_getattr(self, name):
			if name in {"foo", "bar"}:
				return getattr(self, name)
			raise AttributeError(name)

	o = CustomMethod()
	assert "42" == TemplatePython("<?print o.foo()?>").renders(o=o)
	assert "1" == TemplatePython("<?print o.bar()?>").renders(o=o)
	with raises("baz"):
		TemplatePython("<?print o.baz()?>").renders(o=o)


@pytest.mark.ul4
def test_customrender():
	class CustomRenderNoContext:

		def ul4_render(self, *args):
			yield "w/o context="
			for (i, arg) in enumerate(args):
				if i:
					yield ","
				yield arg

	class CustomRenderContext:
		@ul4c.withcontext
		def ul4_render(self, context, *args):
			yield "w/ context="
			for (i, arg) in enumerate(args):
				if i:
					yield ","
				yield arg

	assert "w/o context=foo,bar" == TemplatePython("<?render o('foo', 'bar')?>").renders(o=CustomRenderNoContext())
	assert "w/ context=foo,bar" == TemplatePython("<?render o('foo', 'bar')?>").renders(o=CustomRenderContext())


@pytest.mark.ul4
def test_keyword_evaluation_order():
	globalvar = 0
	def makevar(localvar):
		nonlocal globalvar
		result = globalvar + localvar
		globalvar = localvar
		return result

	globalvar = 0
	assert "1;3" == TemplatePython("<?def t?><?print x?>;<?print y?><?end def?><?render t(x=makevar(1), y=makevar(2))?>").renders(makevar=makevar)

	globalvar = 0
	assert "3;2" == TemplatePython("<?def t?><?print x?>;<?print y?><?end def?><?render t(y=makevar(2), x=makevar(1))?>").renders(makevar=makevar)


@pytest.mark.ul4
def test_setlvalue(T):
	assert "bar" == T("<?code d = {}?><?code d.foo = 'bar'?><?print d.foo?>").renders()
	assert "bar" == T("<?code d = {}?><?code d['foo'] = 'bar'?><?print d['foo']?>").renders()
	assert "bar" == T("<?code d = ['bar']?><?code d[0] = 'bar'?><?print d[0]?>").renders()
	assert "baz" == T("<?code d = {'foo': {}}?><?code d.foo.bar = 'baz'?><?print d.foo.bar?>").renders()
	assert "baz" == T("<?code d = {'foo': {}}?><?code d.foo['bar'] = 'baz'?><?print d.foo['bar']?>").renders()
	assert "baz" == T("<?code d = {'foo': ['bar']}?><?code d.foo[0] = 'baz'?><?print d.foo[0]?>").renders()
	assert "baz" == T("<?code d = ['bar']?><?def f?><?return d?><?end def?><?code f()[0] = 'baz'?><?print d[0]?>").renders()


@pytest.mark.ul4
def test_addlvalue(T):
	assert "barbaz" == T("<?code d = {'foo': 'bar'}?><?code d.foo += 'baz'?><?print d.foo?>").renders()
	assert "barbaz" == T("<?code d = {'foo': 'bar'}?><?code d['foo'] += 'baz'?><?print d['foo']?>").renders()
	assert "barbaz" == T("<?code d = ['bar']?><?code d[0] += 'baz'?><?print d[0]?>").renders()
	assert "barbaz" == T("<?code d = {'foo': {'bar' : 'bar'}}?><?code d.foo.bar += 'baz'?><?print d.foo.bar?>").renders()
	assert "barbaz" == T("<?code d = {'foo': {'bar' : 'bar'}}?><?code d.foo['bar'] += 'baz'?><?print d.foo['bar']?>").renders()
	assert "barbaz" == T("<?code d = {'foo': ['bar']}?><?code d.foo[0] += 'baz'?><?print d.foo[0]?>").renders()
	assert "barbaz" == T("<?code d = ['bar']?><?def f?><?return d?><?end def?><?code f()[0] += 'baz'?><?print d[0]?>").renders()
	assert "[1, 2, 3, 4][1, 2, 3, 4]" == T("<?code d = {'foo': [1, 2]}?><?code l = d.foo?><?code d.foo += [3, 4]?><?print d.foo?><?print l?>").renders()


@pytest.mark.ul4
def test_sublvalue(T):
	assert "6" == T("<?code d = {'foo': 23}?><?code d.foo -= 17?><?print d.foo?>").renders()
	assert "6" == T("<?code d = {'foo': 23}?><?code d['foo'] -= 17?><?print d['foo']?>").renders()
	assert "6" == T("<?code d = [23]?><?code d[0] -= 17?><?print d[0]?>").renders()
	assert "6" == T("<?code d = {'foo': {'bar' : 23}}?><?code d.foo.bar -= 17?><?print d.foo.bar?>").renders()
	assert "6" == T("<?code d = {'foo': {'bar' : 23}}?><?code d.foo['bar'] -= 17?><?print d.foo['bar']?>").renders()
	assert "6" == T("<?code d = {'foo': [23]}?><?code d.foo[0] -= 17?><?print d.foo[0]?>").renders()
	assert "6" == T("<?code d = [23]?><?def f?><?return d?><?end def?><?code f()[0] -= 17?><?print d[0]?>").renders()


@pytest.mark.ul4
def test_mullvalue(T):
	assert "42" == T("<?code d = {'foo': 6}?><?code d.foo *= 7?><?print d.foo?>").renders()
	assert "42" == T("<?code d = {'foo': 6}?><?code d['foo'] *= 7?><?print d['foo']?>").renders()
	assert "42" == T("<?code d = [6]?><?code d[0] *= 7?><?print d[0]?>").renders()
	assert "42" == T("<?code d = {'foo': {'bar' : 6}}?><?code d.foo.bar *= 7?><?print d.foo.bar?>").renders()
	assert "42" == T("<?code d = {'foo': {'bar' : 6}}?><?code d.foo['bar'] *= 7?><?print d.foo['bar']?>").renders()
	assert "42" == T("<?code d = {'foo': [6]}?><?code d.foo[0] *= 7?><?print d.foo[0]?>").renders()
	assert "42" == T("<?code d = [6]?><?def f?><?return d?><?end def?><?code f()[0] *= 7?><?print d[0]?>").renders()
	assert "[1, 2, 1, 2][1, 2, 1, 2]" == T("<?code d = {'foo': [1, 2]}?><?code l = d.foo?><?code d.foo *= 2?><?print d.foo?><?print l?>").renders()


@pytest.mark.ul4
def test_floordivlvalue(T):
	assert "2" == T("<?code d = {'foo': 5}?><?code d.foo //= 2?><?print d.foo?>").renders()
	assert "2" == T("<?code d = {'foo': 5}?><?code d['foo'] //= 2?><?print d['foo']?>").renders()
	assert "2" == T("<?code d = [5]?><?code d[0] //= 2?><?print d[0]?>").renders()
	assert "2" == T("<?code d = {'foo': {'bar' : 5}}?><?code d.foo.bar //= 2?><?print d.foo.bar?>").renders()
	assert "2" == T("<?code d = {'foo': {'bar' : 5}}?><?code d.foo['bar'] //= 2?><?print d.foo['bar']?>").renders()
	assert "2" == T("<?code d = {'foo': [5]}?><?code d.foo[0] //= 2?><?print d.foo[0]?>").renders()
	assert "2" == T("<?code d = [5]?><?def f?><?return d?><?end def?><?code f()[0] //= 2?><?print d[0]?>").renders()


@pytest.mark.ul4
def test_truedivlvalue(T):
	assert "2.5" == T("<?code d = {'foo': 5}?><?code d.foo /= 2?><?print d.foo?>").renders()
	assert "2.5" == T("<?code d = {'foo': 5}?><?code d['foo'] /= 2?><?print d['foo']?>").renders()
	assert "2.5" == T("<?code d = [5]?><?code d[0] /= 2?><?print d[0]?>").renders()
	assert "2.5" == T("<?code d = {'foo': {'bar' : 5}}?><?code d.foo.bar /= 2?><?print d.foo.bar?>").renders()
	assert "2.5" == T("<?code d = {'foo': {'bar' : 5}}?><?code d.foo['bar'] /= 2?><?print d.foo['bar']?>").renders()
	assert "2.5" == T("<?code d = {'foo': [5]}?><?code d.foo[0] /= 2?><?print d.foo[0]?>").renders()
	assert "2.5" == T("<?code d = [5]?><?def f?><?return d?><?end def?><?code f()[0] /= 2?><?print d[0]?>").renders()


@pytest.mark.ul4
def test_modlvalue(T):
	assert "1" == T("<?code d = {'foo': 5}?><?code d.foo %= 2?><?print d.foo?>").renders()
	assert "1" == T("<?code d = {'foo': 5}?><?code d['foo'] %= 2?><?print d['foo']?>").renders()
	assert "1" == T("<?code d = [5]?><?code d[0] %= 2?><?print d[0]?>").renders()
	assert "1" == T("<?code d = {'foo': {'bar' : 5}}?><?code d.foo.bar %= 2?><?print d.foo.bar?>").renders()
	assert "1" == T("<?code d = {'foo': {'bar' : 5}}?><?code d.foo['bar'] %= 2?><?print d.foo['bar']?>").renders()
	assert "1" == T("<?code d = {'foo': [5]}?><?code d.foo[0] %= 2?><?print d.foo[0]?>").renders()
	assert "1" == T("<?code d = [5]?><?def f?><?return d?><?end def?><?code f()[0] %= 2?><?print d[0]?>").renders()


@pytest.mark.ul4
def test_endless_recursion(T):
	with raises("maximum recursion depth exceeded|Maximum call stack size exceeded|too much recursion|StackOverflowError|Allocation failed - process out of memory"):
		T("""
			<?def f(container)?>
				<?for child in container?>
					<?code f(child)?>
				<?end for?>
			<?end def?>
			<?code x = []?>
			<?code x.append(x)?><?code f(x)?>
		""").renders()


@pytest.mark.ul4
def test_not_containment_precedence(T):
	assert "True" == T("<?print not 'x' in 'gurk'?>").renders()


@pytest.mark.ul4
def test_ul4_tag(T):
	assert "42" == T("<?ul4 template(foo=42)?><?print foo?>").renders()


@pytest.mark.ul4
def test_ul4_tag_python():

	t1 = ul4c.Template("<?ul4 foo?>")
	assert t1.name == "foo"
	assert t1.signature is None

	t2 = ul4c.Template("<?ul4 foo2(bar)?>")
	assert t2.name == "foo2"
	assert str(t2.signature) == "(bar)"

	t3 = ul4c.Template("<?ul4 foo3(bar=17, baz=23)?>")
	assert t3.name == "foo3"
	assert str(t3.signature) == "(bar=17, baz=23)"

	t4 = ul4c.Template("<?ul4 foo4(bar=baz)?>")
	assert t4.name == "foo4"
	assert str(t4.signature) == "(bar=UndefinedVariable('baz'))"

	t5 = ul4c.Template("<?ul4 ()?>")
	assert t5.name is None
	assert str(t5.signature) == "()"


@pytest.mark.ul4
def test_whitespace_tag():
	t1 = ul4c.Template("<?whitespace keep?>")
	assert t1.whitespace == "keep"

	t2 = ul4c.Template("<?whitespace strip?>")
	assert t2.whitespace == "strip"

	t3 = ul4c.Template("<?whitespace smart?>")
	assert t3.whitespace == "smart"


@pytest.mark.ul4
def test_smart_whitespace(T):
	# Without linefeeds the text will be output as-is.
	assert "\tTrue" == T("<?if True?>\tTrue<?end if?>", whitespace="smart").renders()

	# Line feeds will be removed from lines containing only a "control flow" tag.
	assert "True\n" == T("<?if True?>\nTrue\n<?end if?>\n", whitespace="smart").renders()

	# Indentation will also be removed from those lines.
	assert "True\n" == T("    <?if True?>\nTrue\n         <?end if?>\n", whitespace="smart").renders()

	# Additional text (before and after tag) will leave the line feeds intact.
	assert "x\nTrue\n" == T("x<?if True?>\nTrue\n<?end if?>\n", whitespace="smart").renders()
	assert " \nTrue\n" == T("<?if True?> \nTrue\n<?end if?>\n", whitespace="smart").renders()

	# Multiple tags will also leave the line feeds intact.
	assert "\nTrue\n\n" == T("<?if True?><?if True?>\nTrue\n<?end if?><?end if?>\n", whitespace="smart").renders()

	# For <?print?> and <?printx?> tags the indentation and line feed will not be stripped
	assert " 42\n" == T(" <?print 42?>\n", whitespace="smart").renders()
	assert " 42\n" == T(" <?printx 42?>\n", whitespace="smart").renders()

	# For <?render?> and <?renderx?> tags the line feed will be stripped, but the indentation will be reused for each line rendered by the call
	assert "   x\r\n" == T("<?def x?>\nx\r\n<?end def?>\n   <?render x()?>\n", whitespace="smart").renders()
	assert "\t&lt;\n\t&gt;\n" == T("<?def x?>\n<\n>\n<?end def?>\n\t<?renderx x()?>\n", whitespace="smart").renders()

	# But of course "common" indentation will be ignored
	assert "x\r\n" == T("<?if True?>\n   <?def x?>\n   x\r\n   <?end def?>\n   <?render x()?>\n<?end if?>\n", whitespace="smart").renders()
	assert "&amp;\r\n" == T("<?if True?>\n   <?def x?>\n   &\r\n   <?end def?>\n   <?renderx x()?>\n<?end if?>\n", whitespace="smart").renders()

	# But not on the outermost level, which leads to an esoteric corner case:
	# The indentation will be output twice (once by the text itself, and once by the render call).
	assert "      x\r\n" == T("   <?def x?>\n   x\r\n   <?end def?>\n   <?render x()?>\n", whitespace="smart").renders()
	assert "      &amp;\r\n" == T("   <?def x?>\n   &\r\n   <?end def?>\n   <?renderx x()?>\n", whitespace="smart").renders()

	# Additional indentation in the block will be removed.
	assert "True\n" == T("<?if True?>\n\tTrue\n<?end if?>\n", whitespace="smart").renders()

	# Outer indentation will be kept.
	assert " True\n" == T(" <?if True?>\n \tTrue\n <?end if?>\n", whitespace="smart").renders()

	# Mixed indentation will not be recognized as indentation.
	assert "\tTrue\n" == T(" <?if True?>\n\tTrue\n <?end if?>\n", whitespace="smart").renders()


@pytest.mark.ul4
def test_smart_whitespace_nesting(T):
	assert "<x>\n\t<y>\n\t\t<z>0</z>\n\t</y>\n\t<y>\n\t\t<z>1</z>\n\t</y>\n</x>" == T("<?whitespace smart?>\n<x>\n\t<?for i in range(2)?>\n\t\t<y>\n\t\t\t<z><?printx i?></z>\n\t\t</y>\n\t<?end for?>\n</x>").renders()


@pytest.mark.ul4
def test_smart_whitespace_empty_block(T):
	assert "" == T("<?whitespace smart?>\n<?if bug?>\n<?end if?>\n").renders()


@pytest.mark.ul4
def test_function_signature(T):
	assert 42 == T("<?return x?>", signature="x")(x=42)

	with raises(argumentmismatchmessage):
		T("<?return x?>", signature="x")()

	with raises(argumentmismatchmessage):
		T("<?return x?>", signature="x")(x=17, y=23)


@pytest.mark.ul4
def test_function_signature_default(T):
	assert 42 == T("<?return x?>", signature="x=42")()


@pytest.mark.ul4
def test_function_signature_args(T):
	# Calling a template with position arguments only works in Python (of course, inside a template this works in all implementations)
	if T in (TemplatePython, TemplatePythonDumpS, TemplatePythonDump):
		assert 40 == T("<?return sum(args)?>", signature="*args")(17, 23)


@pytest.mark.ul4
def test_function_signature_kwargs(T):
	assert 40 == T("<?return sum(kwargs.values())?>", signature="**kwargs")(x=17, y=23)


@pytest.mark.ul4
def test_template_signature(T):
	assert "42" == T("<?print x?>", name="template_signature_1", signature="x").renders(x=42)

	with raises(argumentmismatchmessage):
		T("<?print x?>", name="template_signature_2", signature="x").renders()

	with raises(argumentmismatchmessage):
		T("<?print x?>", name="template_signature_3", signature="x").renders(x=17, y=23)


@pytest.mark.ul4
def test_template_signature_default(T):
	assert "42" == T("<?print x?>", signature="x=42").renders()


@pytest.mark.ul4
def test_function_signature_default_from_parent(T):
	s = """
		<?code a = 42?>
		<?def f(x=2*a)?>
			<?return x?>
		<?end def?>
		<?code a = 17?>
		<?return f()?>
	"""
	assert 84 == T(s)()


@pytest.mark.ul4
def test_function_signature_mutable_default(T):
	s = """
		<?def f(x=[])?>
			<?code x.append(len(x))?>
			<?return x?>
		<?end def?>
		<?note This returns the same list twice, the addition is done after both function calls?>
		<?return f() + f()?>
	"""
	assert [0, 1, 0, 1] == T(s)()


@pytest.mark.ul4
def test_function_signature_mutable_default_copy(T):
	s = """
		<?def f(x=[])?>
			<?code x.append(len(x))?>
			<?return x?>
		<?end def?>
		<?return f()[:] + f()[:]?>
	"""
	assert [0, 0, 1] == T(s)()


@pytest.mark.ul4
def test_template_signature_default_in_loop(T):
	s = """
		<?code fs = []?>
		<?for i in range(10)?>
			<?def f(x=i)?>
				<?return x?>
			<?end def?>
			<?code fs.append(f)?>
		<?end for?>
		<?print ", ".join(str(f()) for f in fs)?>
	"""
	assert "0, 1, 2, 3, 4, 5, 6, 7, 8, 9" == T(s, whitespace="strip").renders()


@pytest.mark.ul4
def test_template_signature_loop_return_parent_variable(T):
	# The function sees the state of the variables at the point in time when it is called, not when it is defined.
	s = """
		<?code fs = []?>
		<?for i in range(10)?>
			<?def f()?>
				<?return i?>
			<?end def?>
			<?code fs.append(f)?>
		<?end for?>
		<?print ", ".join(str(f()) for f in fs)?>
	"""
	assert "9, 9, 9, 9, 9, 9, 9, 9, 9, 9" == T(s, whitespace="strip").renders()


@pytest.mark.ul4
def test_template_signature_loop_call_local_template(T):
	s = """
		<?code allis = []?>
		<?for i in range(10)?>
			<?def f()?>
				<?return i?>
			<?end def?>
			<?code allis.append(f())?>
		<?end for?>
		<?print ", ".join(str(i) for i in allis)?>
	"""
	assert "0, 1, 2, 3, 4, 5, 6, 7, 8, 9" == T(s, whitespace="strip").renders()


@pytest.mark.ul4
def test_render_in_renderblock(T):
	s = """
		<?def f(content=None)?>
		<?end def?>

		<?renderblock f()?>
			<?render f()?>
		<?end renderblock?>
	"""
	assert "\n\n\t" == T(s, whitespace="smart").renders()


@pytest.mark.ul4
def test_render_with_globals(T):
	t1 = ul4c.Template("<?print sum?>")
	t2 = T("<?render t1()?>")

	assert "42" == t2.render_with_globals([], {"t1": t1}, {"sum": 42})


@pytest.mark.ul4
def test_renders_with_globals(T):
	t1 = ul4c.Template("<?print sum?>")
	t2 = T("<?render t1()?>")

	assert "42" == t2.renders_with_globals([], {"t1": t1}, {"sum": 42})


@pytest.mark.ul4
def test_call_with_globals(T):
	t1 = ul4c.Template("<?return sum?>")
	t2 = T("<?return t1()?>")

	assert 42 == t2.call_with_globals([], {"t1": t1}, {"sum": 42})


@pytest.mark.ul4
def test_jssource():
	t = universaltemplate()
	t.jssource()


@pytest.mark.ul4
def test_javasource():
	t = universaltemplate()
	t.javasource()


@pytest.mark.ul4
def test_attr_if(T):
	cond = ul4.attr_if(html.a("gu'\"rk"), cond="cond")

	s = html.div(class_=cond).conv().string()
	assert '<div></div>' == T(s).renders(cond=False)
	assert '''<div class="gu'&quot;rk"></div>''' == T(s).renders(cond=True)

	s = html.div(class_=(cond, "hurz")).conv().string()
	assert '<div class="hurz"></div>' == T(s).renders(cond=False)
	assert '''<div class="gu'&quot;rkhurz"></div>''' == T(s).renders(cond=True)

	s = cond.conv().string()
	assert '' == T(s).renders(cond=False)
	assert '''<a>gu'"rk</a>''' == T(s).renders(cond=True)

	s = html.ul(compact=ul4.attr_if(True, cond="cond")).conv().string()
	assert '<ul></ul>' == T(s).renders(cond=False)
	assert '''<ul compact="compact"></ul>''' == T(s).renders(cond=True)


@pytest.mark.ul4
def test_module_ul4on(T):
	assert "ul4on" == T("<?print ul4on.__name__?>").renders()
	assert "Object serialization" == T("<?print ul4on.__doc__?>").renders()

	t = T("<?print repr(ul4on.loads(ul4on.dumps(data)))?>")
	assert "None" == t.renders(data=None)
	assert "False" == t.renders(data=False)
	assert "True" == t.renders(data=True)
	assert "42" == t.renders(data=42)
	# no check for float
	assert t.renders(data="abc") in ('"abc"', "'abc'")
	assert '[1, 2, 3]' == t.renders(data=[1, 2, 3])
	assert t.renders(data={'one': 1}) in ('{"one": 1}', "{'one': 1}")

	assert "True" == T("<?print isinstance(ul4on.Encoder(), ul4on.Encoder)?>").renders(data=None)
	assert "True" == T("<?print isinstance(ul4on.Decoder(), ul4on.Decoder)?>").renders(data=None)

	# Explicitly check the real output for at least one example
	assert "i42" == T("<?print ul4on.dumps(42)?>").renders()

	# Test pretty printing
	expected = "L\n\ti1\n\ti2\n\ti3\n]\n"
	if issubclass(T, TemplateJavascript):
		expected = expected.lower()
	assert expected == T("<?print ul4on.dumps([1, 2, 3], '\\t')?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print ul4on.dumps()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print ul4on.dumps(1, 2, 3)?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print ul4on.loads()?>").renders()

	with raises(argumentmismatchmessage):
		T("<?print ul4on.loads(1, 2, 3)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print ul4on.dumps(obj=42)?>").renders()

	with raises(unknownkeywordargument):
		T("<?print ul4on.loads(dump='i42')?>").renders()


@pytest.mark.ul4
def test_module_ul4on_chunked_encoder_calls(T):
	t = T("""
		<?whitespace strip?>
		<?code s1 = 'gurk'?>
		<?code s2 = 'hurz'?>
		<?code e = ul4on.Encoder()?>
		<?print e.dumps(s1)?>
		<?print e.dumps(s2)?>
		<?print e.dumps(obj=s1)?>
		<?print e.dumps(obj=s2)?>
	""")

	assert "S'gurk'S'hurz'^0^1" == t.renders()


@pytest.mark.ul4
def test_module_ul4on_chunked_decoder_calls(T):
	t = T("""
		<?whitespace strip?>
		<?code d = ul4on.Decoder()?>
		<?print d.loads("S'gurk'")?>
		<?print d.loads("S'hurz'")?>
		<?print d.loads("^0")?>
		<?print d.loads("^1")?>
	""")

	assert "gurkhurzgurkhurz" == t.renders()


@pytest.mark.ul4
def test_module_operator(T):
	assert "operator" == T("<?print operator.__name__?>").renders()
	assert "Various operators as functions" == T("<?print operator.__doc__?>").renders()

	assert "True" == T("<?print isinstance(operator.attrgetter('upper'), operator.attrgetter)?>").renders(data=None)

	t1 = T("<?print operator.attrgetter('upper')('foo')()?>")
	assert "FOO" == t1.renders()

	t2 = T("<?print operator.attrgetter('pos', 'pos.start', 'pos.stop')(t.content[-1])?>")
	assert "[slice(0, 11, None), 0, 11]" == t2.renders(t=ul4c.Template("<?print x?>"))


@pytest.mark.ul4
def test_module_ul4(T):
	assert "ul4" == T("<?print ul4.__name__?>").renders()
	assert "UL4 - A templating language" == T("<?print ul4.__doc__?>").renders()

	def saferepr(s):
		"""
		Escape tag delimiters
		"""
		s = repr(s)
		q = s[0]
		s = s.replace("<?", f"<{q} + {q}?")
		s = s.replace("?>", f"?{q} + {q}>")
		return s

	def ok(obj):
		if not isinstance(obj, type):
			return False
		elif not issubclass(obj, ul4c.AST):
			return False
		elif obj is ul4c.Tag:
			return False
		return True

	types = [ t for t in ul4c.__dict__.values() if ok(t) ]

	assert len(types) >= 82

	ul4c.Context.add_builtins()
	ul4 = ul4c.Context.builtins["ul4"]

	source_types = "".join(f"\t\t\t{t.__name__!r}: [ul4.{t.__name__}, {saferepr(getattr(ul4, t.__name__).__doc__)}],\n" for t in types)

	# Check that all the types we expect are there and correct
	source = f"""
		<?whitespace strip?>
		<?code types = {{
			{source_types}
		}}?>
		<?for (n, (t, d)) in types.items()?>
			<?if not t?>
				bad bool: <?print n?><?print "\\n"?>
			<?end if?>
			<?if t.__module__ != "ul4"?>
				bad module: <?print n?><?print "\\n"?>
			<?end if?>
			<?if t.__name__ != n?>
				bad name: <?print n?> != <?print t?><?print "\\n"?>
			<?end if?>
			<?if not t.__doc__?>
				empty doc: <?print n?><?print "\\n"?>
			<?elif t.__doc__ != d?>
				bad doc: <?print n?>; <?print repr(t.__doc__)?> != <?print repr(d)?><?print "\\n"?>
			<?end if?>
		<?end for?>
	"""
	assert "" == T(source).renders()

	# Javascript can't compile templates
	if not issubclass(T, TemplateJavascript):
		assert "gurk;hurz" == T("<?code t = ul4.Template('<?print x?' + '>', name='gurk', signature='x')?><?print t.name?>;<?render t('hurz')?>").renders()


def check_ast_types(T, source, obj, type):
	template = ul4c.Template(source)
	testsource = f"<?print type({obj}) is {type}?>;<?print isinstance({obj}, {type})?>;<?print repr(type({obj}))?>;<?print repr({type})?>"
	expected = f"True;True;<type {type}>;<type {type}>"
	output = T(testsource).renders(t=template)
	assert expected == output


@pytest.mark.ul4
def test_module_ul4_typecheck_indent(T):
	check_ast_types(T, "\t gurk\n", "t.content[0]", "ul4.IndentAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_text(T):
	check_ast_types(T, "\t gurk\n", "t.content[1]", "ul4.TextAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_lineend(T):
	check_ast_types(T, "\t gurk\n", "t.content[2]", "ul4.LineEndAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_const(T):
	check_ast_types(T, "<?print 42?>", "t.content[-1].obj", "ul4.ConstAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_seqitem(T):
	check_ast_types(T, "<?print [42]?>", "t.content[-1].obj.items[0]", "ul4.SeqItemAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_unpackseqitem(T):
	check_ast_types(T, "<?print [*x]?>", "t.content[-1].obj.items[0]", "ul4.UnpackSeqItemAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_list(T):
	check_ast_types(T, "<?print []?>", "t.content[-1].obj", "ul4.ListAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_listcomprehension(T):
	check_ast_types(T, "<?print [c for c in '123']?>", "t.content[-1].obj", "ul4.ListComprehensionAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_set(T):
	check_ast_types(T, "<?print {/}?>", "t.content[-1].obj", "ul4.SetAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_setcomprehension(T):
	check_ast_types(T, "<?print {c for c in '123'}?>", "t.content[-1].obj", "ul4.SetComprehensionAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_dictitem(T):
	check_ast_types(T, "<?print {'x': 42}?>", "t.content[-1].obj.items[0]", "ul4.DictItemAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_unpackdictitem(T):
	check_ast_types(T, "<?print {**x}?>", "t.content[-1].obj.items[0]", "ul4.UnpackDictItemAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_dict(T):
	check_ast_types(T, "<?print {}?>", "t.content[-1].obj", "ul4.DictAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_dictcomprehension(T):
	check_ast_types(T, "<?print {k: v for (k, v) in enumerate('123')}?>", "t.content[-1].obj", "ul4.DictComprehensionAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_generatorexpression(T):
	check_ast_types(T, "<?print (c for c in '123')?>", "t.content[-1].obj", "ul4.GeneratorExpressionAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_var(T):
	check_ast_types(T, "<?print x?>", "t.content[-1].obj", "ul4.VarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_conditionalblocks(T):
	check_ast_types(T, "<?if x?><?end if?>", "t.content[-1]", "ul4.ConditionalBlocksAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_ifblock(T):
	check_ast_types(T, "<?if x?><?end if?>", "t.content[-1].content[0]", "ul4.IfBlockAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_elifblock(T):
	check_ast_types(T, "<?if x?><?elif y?><?end if?>", "t.content[-1].content[1]", "ul4.ElIfBlockAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_elseblock(T):
	check_ast_types(T, "<?if x?><?else?><?end if?>", "t.content[-1].content[1]", "ul4.ElseBlockAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_forblock(T):
	check_ast_types(T, "<?for x in 'x123'?><?end for?>", "t.content[-1]", "ul4.ForBlockAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_whileblock(T):
	check_ast_types(T, "<?while x?><?end while?>", "t.content[-1]", "ul4.WhileBlockAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_break(T):
	check_ast_types(T, "<?for x in '123'?><?break?><?end for?>", "t.content[-1].content[0]", "ul4.BreakAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_continue(T):
	check_ast_types(T, "<?for x in '123'?><?continue?><?end for?>", "t.content[-1].content[0]", "ul4.ContinueAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_attr(T):
	check_ast_types(T, "<?print x.y?>", "t.content[-1].obj", "ul4.AttrAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_slice(T):
	check_ast_types(T, "<?print x[1:-1]?>", "t.content[-1].obj.obj2", "ul4.SliceAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_not(T):
	check_ast_types(T, "<?print not x?>", "t.content[-1].obj", "ul4.NotAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_if(T):
	check_ast_types(T, "<?print x if y else z?>", "t.content[-1].obj", "ul4.IfAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_neg(T):
	check_ast_types(T, "<?print -x?>", "t.content[-1].obj", "ul4.NegAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_bitnot(T):
	check_ast_types(T, "<?print ~x?>", "t.content[-1].obj", "ul4.BitNotAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_print(T):
	check_ast_types(T, "<?print x?>", "t.content[-1]", "ul4.PrintAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_printx(T):
	check_ast_types(T, "<?printx x?>", "t.content[-1]", "ul4.PrintXAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_return(T):
	check_ast_types(T, "<?return x?>", "t.content[-1]", "ul4.ReturnAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_item(T):
	check_ast_types(T, "<?return x[42]?>", "t.content[-1].obj", "ul4.ItemAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_shiftleft(T):
	check_ast_types(T, "<?return x << y?>", "t.content[-1].obj", "ul4.ShiftLeftAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_shiftright(T):
	check_ast_types(T, "<?return x >> y?>", "t.content[-1].obj", "ul4.ShiftRightAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_bitand(T):
	check_ast_types(T, "<?return x & y?>", "t.content[-1].obj", "ul4.BitAndAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_bitxor(T):
	check_ast_types(T, "<?return x ^ y?>", "t.content[-1].obj", "ul4.BitXOrAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_bitor(T):
	check_ast_types(T, "<?return x | y?>", "t.content[-1].obj", "ul4.BitOrAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_is(T):
	check_ast_types(T, "<?return x is y?>", "t.content[-1].obj", "ul4.IsAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_isnot(T):
	check_ast_types(T, "<?return x is not y?>", "t.content[-1].obj", "ul4.IsNotAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_eq(T):
	check_ast_types(T, "<?return x == y?>", "t.content[-1].obj", "ul4.EQAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_ne(T):
	check_ast_types(T, "<?return x != y?>", "t.content[-1].obj", "ul4.NEAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_lt(T):
	check_ast_types(T, "<?return x < y?>", "t.content[-1].obj", "ul4.LTAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_le(T):
	check_ast_types(T, "<?return x <= y?>", "t.content[-1].obj", "ul4.LEAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_gt(T):
	check_ast_types(T, "<?return x > y?>", "t.content[-1].obj", "ul4.GTAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_ge(T):
	check_ast_types(T, "<?return x >= y?>", "t.content[-1].obj", "ul4.GEAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_contains(T):
	check_ast_types(T, "<?return x in y?>", "t.content[-1].obj", "ul4.ContainsAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_notcontains(T):
	check_ast_types(T, "<?return x not in y?>", "t.content[-1].obj", "ul4.NotContainsAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_add(T):
	check_ast_types(T, "<?return x + y?>", "t.content[-1].obj", "ul4.AddAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_sub(T):
	check_ast_types(T, "<?return x - y?>", "t.content[-1].obj", "ul4.SubAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_mul(T):
	check_ast_types(T, "<?return x * y?>", "t.content[-1].obj", "ul4.MulAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_floordiv(T):
	check_ast_types(T, "<?return x // y?>", "t.content[-1].obj", "ul4.FloorDivAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_truediv(T):
	check_ast_types(T, "<?return x / y?>", "t.content[-1].obj", "ul4.TrueDivAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_or(T):
	check_ast_types(T, "<?return x or y?>", "t.content[-1].obj", "ul4.OrAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_and(T):
	check_ast_types(T, "<?return x and y?>", "t.content[-1].obj", "ul4.AndAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_mod(T):
	check_ast_types(T, "<?return x % y?>", "t.content[-1].obj", "ul4.ModAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_setvar(T):
	check_ast_types(T, "<?code x = y?>", "t.content[-1]", "ul4.SetVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_addvar(T):
	check_ast_types(T, "<?code x += y?>", "t.content[-1]", "ul4.AddVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_subvar(T):
	check_ast_types(T, "<?code x -= y?>", "t.content[-1]", "ul4.SubVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_mulvar(T):
	check_ast_types(T, "<?code x *= y?>", "t.content[-1]", "ul4.MulVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_floordivvar(T):
	check_ast_types(T, "<?code x //= y?>", "t.content[-1]", "ul4.FloorDivVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_truedivvar(T):
	check_ast_types(T, "<?code x /= y?>", "t.content[-1]", "ul4.TrueDivVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_modvar(T):
	check_ast_types(T, "<?code x %= y?>", "t.content[-1]", "ul4.ModVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_shiftleftvar(T):
	check_ast_types(T, "<?code x <<= y?>", "t.content[-1]", "ul4.ShiftLeftVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_shiftrightvar(T):
	check_ast_types(T, "<?code x >>= y?>", "t.content[-1]", "ul4.ShiftRightVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_bitandvar(T):
	check_ast_types(T, "<?code x &= y?>", "t.content[-1]", "ul4.BitAndVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_bitxorvar(T):
	check_ast_types(T, "<?code x ^= y?>", "t.content[-1]", "ul4.BitXOrVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_bitorvar(T):
	check_ast_types(T, "<?code x |= y?>", "t.content[-1]", "ul4.BitOrVarAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_positionalargument(T):
	check_ast_types(T, "<?print f(x)?>", "t.content[-1].obj.args[0]", "ul4.PositionalArgumentAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_keywordargument(T):
	check_ast_types(T, "<?print f(x=y)?>", "t.content[-1].obj.args[0]", "ul4.KeywordArgumentAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_unpacklistargument(T):
	check_ast_types(T, "<?print f(*x)?>", "t.content[-1].obj.args[0]", "ul4.UnpackListArgumentAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_unpackdictargument(T):
	check_ast_types(T, "<?print f(**x)?>", "t.content[-1].obj.args[0]", "ul4.UnpackDictArgumentAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_call(T):
	check_ast_types(T, "<?print f()?>", "t.content[-1].obj", "ul4.CallAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_render(T):
	check_ast_types(T, "<?render f()?>", "t.content[-1]", "ul4.RenderAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_renderx(T):
	check_ast_types(T, "<?renderx f()?>", "t.content[-1]", "ul4.RenderXAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_renderblock(T):
	check_ast_types(T, "<?renderblock f()?><?end renderblock?>", "t.content[-1]", "ul4.RenderBlockAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_renderblocks(T):
	check_ast_types(T, "<?renderblocks f()?><?end renderblocks?>", "t.content[-1]", "ul4.RenderBlocksAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_signature(T):
	check_ast_types(T, "<?def f(x)?><?end def?>", "t.content[-1].signature", "ul4.SignatureAST")


@pytest.mark.ul4
def test_module_ul4_typecheck_template(T):
	check_ast_types(T, "<?print 42?>", "t", "ul4.Template")


@pytest.mark.ul4
def test_module_ul4_typecheck_templateclosure(T):
	check_ast_types(T, "<?def f()?><?end def?><?return f?>", "t()", "ul4.TemplateClosure")
