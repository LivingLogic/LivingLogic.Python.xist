#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from __future__ import division

import sys, os, re, datetime, StringIO, json, contextlib, tempfile, collections, shutil, subprocess, pkg_resources

import py.test

from ll import ul4c, color, misc


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
		template = ul4c.compile(self.source)
		print "Testing Python template:".format(self.filename, self.lineno)
		print template.pythonsource()
		return template.renders(**self.variables)


class RenderPythonDumpS(Render):
	def renders(self):
		template = ul4c.compile(self.source)
		template = ul4c.loads(template.dumps()) # Recreate the template from the binary dump
		print "Testing Python template loaded from string ({}, line {}):".format(self.filename, self.lineno)
		print template.pythonsource()
		return template.renders(**self.variables)


class RenderPythonDump(Render):
	def renders(self):
		template = ul4c.compile(self.source)
		stream = StringIO.StringIO()
		template.dump(stream)
		stream.seek(0)
		template = ul4c.load(stream) # Recreate the template from the stream
		print "Testing Python template loaded from stream ({}, line {}):".format(self.filename, self.lineno)
		print template.pythonsource()
		return template.renders(**self.variables)


class RenderJS(Render):
	def renders(self):
		# Check the Javascript version (this requires an installed ``d8`` shell from V8 (http://code.google.com/p/v8/))
		template = ul4c.compile(self.source)
		js = template.jssource()
		js = u"template = {};\ndata = {};\nprint(template.renders(data));\n".format(js, ul4c._json(self.variables))
		print "Testing Javascript code compiled by Python ({}, line {}):".format(self.filename, self.lineno)
		print js.encode("utf-8")
		with tempfile.NamedTemporaryFile(mode="wb", suffix=".js") as f:
			f.write(js.encode("utf-8"))
			f.flush()
			result = os.popen("d8 {} {}".format(pkg_resources.resource_filename("ll.xist", "data/"), f.name), "rb").read()
		result = result.decode("utf-8")[:-1] # Drop the "\n"
		# Check if we have an exception
		if result.endswith("^"):
			raise RuntimeError(result.splitlines()[0])
		return result


class RenderJava(Render):
	maincodetemplate = u"""
	public class UL4Test
	{
		@SuppressWarnings("unchecked")
		public static void main(String[] args) throws java.io.IOException, java.io.UnsupportedEncodingException
		{
			%(source)s
		}
	}
	"""

	def findexception(self, output):
		lines = output.splitlines()
		for line in lines:
			prefix = 'Exception in thread "main"'
			if line.startswith(prefix):
				msg = line[len(prefix):].strip()
				if msg == "Traceback (most recent call last):": # This is a Jython exception, the message is in the last line
					msg = lines[-1]
				print >>sys.stderr, output
				raise RuntimeError(msg)

	def formatsource(self, string):
		"""
		Reindents the Java source.
		"""
		indent = 0
		newlines = []
		for line in string.strip().splitlines(False):
			line = line.strip()
			if line == "}":
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
			print source.encode("utf-8")
			with open(os.path.join(tempdir, "UL4Test.java"), "wb") as f:
				f.write(source.encode("utf-8"))
			os.system("cd {}; javac -encoding utf-8 UL4Test.java".format(tempdir))
			pipe = subprocess.Popen("cd {}; java UL4Test".format(tempdir), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			(stdout, stderr) = pipe.communicate()
		finally:
			shutil.rmtree(tempdir)
		# Check if we have an exception
		self.findexception(stdout)
		self.findexception(stderr)
		if stderr:
			print >>sys.stderr, stderr
		return stdout.decode("utf-8")


class RenderJavaSourceCompiledByPython(RenderJava):
	codetemplate = u"""
	com.livinglogic.ul4.Template template = new com.livinglogic.ul4.JSPTemplate()
	{
		public void render(java.io.Writer out, java.util.Map<String, Object> variables) throws java.io.IOException
		{
			%(template)s
		}
	};
	java.util.Map<String, Object> variables = %(variables)s;
	String output = template.renders(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	def renders(self):
		# Check the Java version
		print "Testing Java code ({}, line {}):".format(self.filename, self.lineno)
		template = ul4c.compile(self.source)
		java = template.javasource(indent=4)
		java = self.codetemplate % dict(variables=misc.javaexpr(self.variables), template=java)
		return self.runsource(java)


class RenderJavaLoadByJava(RenderJava):
	codetemplate = u"""
	com.livinglogic.ul4.InterpretedTemplate template = com.livinglogic.ul4.InterpretedTemplate.load(%(dump)s);
	java.util.Map<String, Object> variables = %(variables)s;
	String output = template.renders(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	def renders(self):
		# Check the Java version
		print "Testing Java InterpretedTemplate (interpreted mode, compiled by Python) ({}, line {}):".format(self.filename, self.lineno)
		template = ul4c.compile(self.source)
		dump = template.dumps()
		java = self.codetemplate % dict(variables=misc.javaexpr(self.variables), dump=misc.javaexpr(dump))
		return self.runsource(java)


class RenderJavaSourceCompiledByJava(RenderJava):
	codetemplate = u"""
	com.livinglogic.ul4.InterpretedTemplate template = com.livinglogic.ul4.Compiler.compile(%(source)s);
	System.err.println("Generate Java code:");
	System.err.println(template.javaSource());
	com.livinglogic.ul4.JSPTemplate compiledTemplate = template.compileToJava();
	java.util.Map<String, Object> variables = %(variables)s;
	String output = compiledTemplate.renders(variables);
	// We can't use ``System.out.print`` here, because this gives us no control over the encoding
	// Use ``System.out.write`` to make sure the output is in UTF-8
	byte[] outputBytes = output.getBytes("utf-8");
	System.out.write(outputBytes, 0, outputBytes.length);
	"""

	def renders(self):
		# Check the Java version
		print "Testing Java InterpretedTemplate (compiled mode, compiled by Java) ({}, line {}):".format(self.filename, self.lineno)
		java = self.codetemplate % dict(source=misc.javaexpr(self.source), variables=misc.javaexpr(self.variables))
		return self.runsource(java)


all_python_renderers = (RenderPython, RenderPythonDumpS, RenderPythonDump)
all_renderers = (RenderPython, RenderPythonDumpS, RenderPythonDump, RenderJS, RenderJavaSourceCompiledByPython, RenderJavaLoadByJava, RenderJavaSourceCompiledByJava)


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


def raises(msg, render):
	# Check that executing ``render`` raises an exception that matches a regexp
	try:
		render.renders()
	except Exception, exc:
		assert re.search(msg, "{0.__class__.__module__}.{0.__class__.__name__}: {0}".format(exc)) is not None
	else:
		py.test.fail("failed to raise exception")


def test_text():
	for r in all_renderers:
		yield eq, u'gurk', r(u'gurk')
		yield eq, u'g\xfcrk', r(u'g\xfcrk')


def test_none():
	for r in all_renderers:
		yield eq, '', r(u'<?print None?>')
		yield eq, 'no', r(u'<?if None?>yes<?else?>no<?end if?>')


def test_false():
	for r in all_renderers:
		yield eq, 'False', r(u'<?print False?>')
		yield eq, 'no', r(u'<?if False?>yes<?else?>no<?end if?>')


def test_true():
	for r in all_renderers:
		yield eq, 'True', r(u'<?print True?>')
		yield eq, 'yes', r(u'<?if True?>yes<?else?>no<?end if?>')


def test_int():
	for r in all_renderers:
		yield eq, '0', r(u'<?print 0?>')
		yield eq, '42', r(u'<?print 42?>')
		yield eq, '-42', r(u'<?print -42?>')
		yield eq, '255', r(u'<?print 0xff?>')
		yield eq, '255', r(u'<?print 0Xff?>')
		yield eq, '-255', r(u'<?print -0xff?>')
		yield eq, '-255', r(u'<?print -0Xff?>')
		yield eq, '63', r(u'<?print 0o77?>')
		yield eq, '63', r(u'<?print 0O77?>')
		yield eq, '-63', r(u'<?print -0o77?>')
		yield eq, '-63', r(u'<?print -0O77?>')
		yield eq, '7', r(u'<?print 0b111?>')
		yield eq, '7', r(u'<?print 0B111?>')
		yield eq, '-7', r(u'<?print -0b111?>')
		yield eq, '-7', r(u'<?print -0B111?>')

		yield eq, 'no', r(u'<?if 0?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r(u'<?if 1?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r(u'<?if -1?>yes<?else?>no<?end if?>')


def test_float():
	for r in all_renderers:
		# str() output might differ slightly between Python and JS, so eval the output again for tests
		yield evaleq, 0.0, r(u'<?print 0.?>')
		yield evaleq, 42.0, r(u'<?print 42.?>')
		yield evaleq, -42.0, r(u'<?print -42.?>')
		yield evaleq, -42.5, r(u'<?print -42.5?>')
		yield evaleq, 1e42, r(u'<?print 1E42?>')
		yield evaleq, 1e42, r(u'<?print 1e42?>')
		yield evaleq, -1e42, r(u'<?print -1E42?>')
		yield evaleq, -1e42, r(u'<?print -1e42?>')

		yield eq, 'no', r(u'<?if 0.?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r(u'<?if 1.?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r(u'<?if -1.?>yes<?else?>no<?end if?>')


def test_string():
	for r in all_renderers:
		yield raises, "Unterminated string", r(u'<?print "?>')
		yield eq, 'foo', r(u'<?print "foo"?>')
		yield eq, '\n', r(u'<?print "\\n"?>')
		yield eq, '\r', r(u'<?print "\\r"?>')
		yield eq, '\t', r(u'<?print "\\t"?>')
		yield eq, '\f', r(u'<?print "\\f"?>')
		yield eq, '\b', r(u'<?print "\\b"?>')
		yield eq, '\a', r(u'<?print "\\a"?>')
		yield eq, '\x1b', r(u'<?print "\\e"?>')
		yield eq, '\x00', r(u'<?print "\\x00"?>')
		yield eq, '"', r(u'<?print "\\""?>')
		yield eq, "'", r(u'<?print "\\\'"?>')
		yield eq, u'\u20ac', r(u'<?print "\u20ac"?>')
		yield eq, u'\xff', r(u'<?print "\\xff"?>')
		yield eq, u'\u20ac', r(u'''<?print "\\u20ac"?>''')
		yield eq, "a\nb", r(u'<?print "a\nb"?>')
		for c in u"\x00\x80\u0100\u3042\n\r\t\f\b\a\e\"":
			yield eq, c, r(u'<?print obj?>', obj=c) # This tests :func:`misc.javaexpr` for Java and :func:`ul4c._json` for JS

		# Test literal control characters
		yield eq, u'gu\n\r\trk', r(u"<?print 'gu\n\r\trk'?>")
		yield eq, u'gu\n\r\t\\rk', r(ur"<?print 'gu\n\r\t\\rk'?>")

		yield eq, 'no', r(u'<?if ""?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r(u'<?if "foo"?>yes<?else?>no<?end if?>')


def test_date():
	for r in all_renderers:
		yield eq, '2000-02-29', r(u'<?print @2000-02-29T.isoformat()?>')
		yield eq, '2000-02-29T12:34:00', r(u'<?print @2000-02-29T12:34.isoformat()?>')
		yield eq, '2000-02-29T12:34:56', r(u'<?print @2000-02-29T12:34:56.isoformat()?>')
		yield eq, '2000-02-29T12:34:56.987000', r(u'<?print @2000-02-29T12:34:56.987000.isoformat()?>') # JS and Java only supports milliseconds
		yield eq, 'yes', r(u'<?if @2000-02-29T12:34:56.987654?>yes<?else?>no<?end if?>')


def test_color():
	for r in all_renderers:
		yield eq, '255,255,255,255', r(u'<?code c = #fff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
		yield eq, '255,255,255,255', r(u'<?code c = #ffffff?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
		yield eq, '18,52,86,255', r(u'<?code c = #123456?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
		yield eq, '17,34,51,68', r(u'<?code c = #1234?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
		yield eq, '18,52,86,120', r(u'<?code c = #12345678?><?print c[0]?>,<?print c[1]?>,<?print c[2]?>,<?print c[3]?>')
		yield eq, 'yes', r(u'<?if #fff?>yes<?else?>no<?end if?>')


def test_list():
	for r in all_renderers:
		yield eq, '', r(u'<?for item in []?><?print item?>;<?end for?>')
		yield eq, '1;', r(u'<?for item in [1]?><?print item?>;<?end for?>')
		yield eq, '1;', r(u'<?for item in [1,]?><?print item?>;<?end for?>')
		yield eq, '1;2;', r(u'<?for item in [1, 2]?><?print item?>;<?end for?>')
		yield eq, '1;2;', r(u'<?for item in [1, 2,]?><?print item?>;<?end for?>')
		yield eq, 'no', r(u'<?if []?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r(u'<?if [1]?>yes<?else?>no<?end if?>')


def test_dict():
	for r in all_renderers:
		yield eq, '', r(u'<?for (key, value) in {}.items()?><?print key?>:<?print value?>\n<?end for?>')
		yield eq, '1:2\n', r(u'<?for (key, value) in {1:2}.items()?><?print key?>:<?print value?>\n<?end for?>')
		yield eq, '1:2\n', r(u'<?for (key, value) in {1:2,}.items()?><?print key?>:<?print value?>\n<?end for?>')
		# With duplicate keys, later ones simply overwrite earlier ones
		yield eq, '1:3\n', r(u'<?for (key, value) in {1:2, 1: 3}.items()?><?print key?>:<?print value?>\n<?end for?>')
		# Test **
		yield eq, '1:2\n', r(u'<?for (key, value) in {**{1:2}}.items()?><?print key?>:<?print value?>\n<?end for?>')
		yield eq, '1:4\n', r(u'<?for (key, value) in {1:1, **{1:2}, 1:3, **{1:4}}.items()?><?print key?>:<?print value?>\n<?end for?>')
		yield eq, 'no', r(u'<?if {}?>yes<?else?>no<?end if?>')
		yield eq, 'yes', r(u'<?if {1:2}?>yes<?else?>no<?end if?>')


def test_code_storevar():
	for r in all_renderers:
		yield eq, '42', r(u'<?code x = 42?><?print x?>')
		yield eq, 'xyzzy', r(u'<?code x = "xyzzy"?><?print x?>')


def test_code_addvar():
	for r in all_renderers:
		for x in (17, 17., False, True):
			for y in (23, 23., False, True):
				yield evaleq, x + y, r(u'<?code x = {}?><?code x += {}?><?print x?>'.format(x, y))
		yield eq, 'xyzzy', r(u'<?code x = "xyz"?><?code x += "zy"?><?print x?>')


def test_code_subvar():
	for r in all_renderers:
		for x in (17, 17., False, True):
			for y in (23, 23., False, True):
				yield evaleq, x - y, r(u'<?code x = {}?><?code x -= {}?><?print x?>'.format(x, y))


def test_code_mulvar():
	for r in all_renderers:
		for x in (17, 17., False, True):
			for y in (23, 23., False, True):
				yield evaleq, x * y, r(u'<?code x = {}?><?code x *= {}?><?print x?>'.format(x, y))
		for x in (17, False, True):
			y = "xyzzy"
			yield eq, x * y, r(u'<?code x = {}?><?code x *= {!r}?><?print x?>'.format(x, y))
		yield eq, 17*"xyzzy", r(u'<?code x = "xyzzy"?><?code x *= 17?><?print x?>')


def test_code_floordivvar():
	for r in all_renderers:
		for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
			for y in (2, -2, 2.0, -2.0, True):
				yield evaleq, x // y, r(u'<?code x = {}?><?code x //= {}?><?print x?>'.format(x, y))


def test_code_truedivvar():
	for r in all_renderers:
		for x in (5, -5, 5.0, -5.0, 4, -4, 4.0, -4.0, False, True):
			for y in (2, -2, 2.0, -2.0, True):
				yield evaleq, x / y, r(u'<?code x = {}?><?code x /= {}?><?print x?>'.format(x, y))


def test_code_modvar():
	for r in all_renderers:
		for x in (1729, 1729.0, -1729, -1729.0, False, True):
			for y in (23, 23., -23, -23.0, True):
				yield evaleq, x % y, r(u'<?code x = {}?><?code x %= {}?><?print x?>'.format(x, y))


def test_code_delvar():
	for r in all_renderers:
		yield raises, "(KeyError|not found)", r(u'<?code x = 1729?><?code del x?><?print x?>')


def test_for_string():
	for r in all_renderers:
		yield eq, '', r(u'<?for c in data?>(<?print c?>)<?end for?>', data="")
		yield eq, '(g)(u)(r)(k)', r(u'<?for c in data?>(<?print c?>)<?end for?>', data="gurk")


def test_for_list():
	for r in all_renderers:
		yield eq, '', r(u'<?for c in data?>(<?print c?>)<?end for?>', data="")
		yield eq, '(g)(u)(r)(k)', r(u'<?for c in data?>(<?print c?>)<?end for?>', data=["g", "u", "r", "k"])


def test_for_dict():
	for r in all_renderers:
		yield eq, '', r(u'<?for c in data?>(<?print c?>)<?end for?>', data={})
		yield eq, '(a)(b)(c)', r(u'<?for c in sorted(data)?>(<?print c?>)<?end for?>', data=dict(a=1, b=2, c=3))


def test_for_nested():
	for r in all_renderers:
		yield eq, '[(1)(2)][(3)(4)]', r(u'<?for list in data?>[<?for n in list?>(<?print n?>)<?end for?>]<?end for?>', data=[[1, 2], [3, 4]])


def test_for_unpacking():
	data = [
		("spam", "eggs", 17),
		("gurk", "hurz", 23),
		("hinz", "kunz", 42)
	]

	for r in all_renderers:
		yield eq, '(spam)(gurk)(hinz)', r(u'<?for (a,) in data?>(<?print a?>)<?end for?>', data=data)
		yield eq, '(spam,eggs)(gurk,hurz)(hinz,kunz)', r(u'<?for (a, b) in data?>(<?print a?>,<?print b?>)<?end for?>', data=data)
		yield eq, '(spam,eggs,17)(gurk,hurz,23)(hinz,kunz,42)', r(u'<?for (a, b, c) in data?>(<?print a?>,<?print b?>,<?print c?>)<?end for?>', data=data)


def test_break():
	for r in all_renderers:
		yield eq, '1, 2, ', r(u'<?for i in [1,2,3]?><?print i?>, <?if i==2?><?break?><?end if?><?end for?>')


def test_break_nested():
	for r in all_renderers:
		yield eq, '1, 1, 2, 1, 2, 3, ', r(u'<?for i in [1,2,3,4]?><?for j in [1,2,3,4]?><?print j?>, <?if j>=i?><?break?><?end if?><?end for?><?if i>=3?><?break?><?end if?><?end for?>')


def test_continue():
	for r in all_renderers:
		yield eq, '1, 3, ', r(u'<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?print i?>, <?end for?>')


def test_continue_nested():
	for r in all_renderers:
		yield eq, '1, 3, \n1, 3, \n', r(u'<?for i in [1,2,3]?><?if i==2?><?continue?><?end if?><?for j in [1,2,3]?><?if j==2?><?continue?><?end if?><?print j?>, <?end for?>\n<?end for?>')


def test_if():
	for r in all_renderers:
		yield eq, '42', r(u'<?if data?><?print data?><?end if?>', data=42)


def test_else():
	for r in all_renderers:
		yield eq, '42', r(u'<?if data?><?print data?><?else?>no<?end if?>', data=42)
		yield eq, 'no', r(u'<?if data?><?print data?><?else?>no<?end if?>', data=0)


def test_block_errors():
	yield raises, "in u?.<.for x in data.>..*block unclosed", RenderPython(u'<?for x in data?>')
	yield raises, "endif doesn't match any if", RenderPython(u'<?for x in data?><?end if?>')
	yield raises, "not in any block", RenderPython(u'<?end?>')
	yield raises, "not in any block", RenderPython(u'<?end for?>')
	yield raises, "not in any block", RenderPython(u'<?end if?>')
	yield raises, "else doesn't match any if", RenderPython(u'<?else?>')
	yield raises, "in u?.<.if data.>..*block unclosed", RenderPython(u'<?if data?>')
	yield raises, "in u?.<.if data.>..*block unclosed", RenderPython(u'<?if data?><?else?>')
	yield raises, "duplicate else", RenderPython(u'<?if data?><?else?><?else?>')
	yield raises, "else already seen in elif", RenderPython(u'<?if data?><?else?><?elif data?>')
	yield raises, "else already seen in elif", RenderPython(u'<?if data?><?elif data?><?elif data?><?else?><?elif data?>')


def test_empty():
	yield raises, "expression required", RenderPython(u'<?print?>')
	yield raises, "expression required", RenderPython(u'<?if?>')
	yield raises, "expression required", RenderPython(u'<<?if x?><?elif?><?end if?>')
	yield raises, "loop expression required", RenderPython(u'<?for?>')
	yield raises, "statement required", RenderPython(u'<?code?>')
	yield raises, "render statement required", RenderPython(u'<?render?>')


def test_add():
	values = (17, 23, 1., -1.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield evaleq, x + y, r(u'<?print x + y?>', x=x, y=y) # Using ``evaleq`` avoids problem with the nonexistant int/float distinction in JS
		yield eq, 'foobar', r(u'<?code x="foo"?><?code y="bar"?><?print x+y?>')
		yield eq, '(f)(o)(o)(b)(a)(r)', r(u'<?for i in data.foo+data.bar?>(<?print i?>)<?end for?>', data=dict(foo="foo", bar="bar"))


def test_sub():
	values = (17, 23, 1., -1.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield evaleq, x - y, r(u'<?print x - y?>', x=x, y=y)


def test_mul():
	values = (17, 23, 1., -1.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield evaleq, x * y, r(u'<?print x * y?>', x=x, y=y)
		yield eq, 17*"foo", r(u'<?print 17*"foo"?>')
		yield eq, 17*"foo", r(u'<?code x=17?><?code y="foo"?><?print x*y?>')
		yield eq, "foo"*17, r(u'<?code x="foo"?><?code y=17?><?print x*y?>')
		yield eq, "foo"*17, r(u'<?print "foo"*17?>')
		yield eq, "(foo)(bar)(foo)(bar)(foo)(bar)", r(u'<?for i in 3*data?>(<?print i?>)<?end for?>', data=["foo", "bar"])


def test_truediv():
	for r in all_renderers:
		yield eq, "0.5", r(u'<?print 1/2?>')
		yield eq, "0.5", r(u'<?code x=1?><?code y=2?><?print x/y?>')


def test_floordiv():
	for r in all_renderers:
		yield eq, "0", r(u'<?print 1//2?>')
		yield eq, "0", r(u'<?code x=1?><?code y=2?><?print x//y?>')


def test_mod():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield evaleq, x % y, r(u'<?print {} % {}?>'.format(x, y))
				yield evaleq, x % y, r(u'<?print x % y?>', x=x, y=y)


def test_eq():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x == y), r(u'<?print {} == {}?>'.format(x, y))
				yield eq, str(x == y), r(u'<?print x == y?>', x=x, y=y)


def test_ne():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x != y), r(u'<?print {} != {}?>'.format(x, y))
				yield eq, str(x != y), r(u'<?print x != y?>', x=x, y=y)


def test_lt():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x < y), r(u'<?print {} < {}?>'.format(x, y))
				yield eq, str(x < y), r(u'<?print x < y?>', x=x, y=y)


def test_le():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x <= y), r(u'<?print {} <= {}?>'.format(x, y))
				yield eq, str(x <= y), r(u'<?print x <= y?>', x=x, y=y)


def test_gt():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x > y), r(u'<?print {} > {}?>'.format(x, y))
				yield eq, str(x > y), r(u'<?print x > y?>', x=x, y=y)


def test_ge():
	values = (17, 23, 17., 23.)
	for r in all_renderers:
		for x in values:
			for y in values:
				yield eq, str(x >= y), r(u'<?print {} >= {}?>'.format(x, y))
				yield eq, str(x >= y), r(u'<?print x >= y?>', x=x, y=y)


def test_contains():
	code = u'<?print x in y?>'

	for r in all_renderers:
		yield eq, "True", r(code, x=2, y=[1, 2, 3])
		yield eq, "False", r(code, x=4, y=[1, 2, 3])
		yield eq, "True", r(code, x="ur", y="gurk")
		yield eq, "False", r(code, x="un", y="gurk")
		yield eq, "True", r(code, x="a", y={"a": 1, "b": 2})
		yield eq, "False", r(code, x="c", y={"a": 1, "b": 2})
		yield eq, "True", r(code, x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42))
		yield eq, "False", r(code, x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42))


def test_notcontains():
	code = u'<?print x not in y?>'

	for r in all_renderers:
		yield eq, "False", r(code, x=2, y=[1, 2, 3])
		yield eq, "True", r(code, x=4, y=[1, 2, 3])
		yield eq, "False", r(code, x="ur", y="gurk")
		yield eq, "True", r(code, x="un", y="gurk")
		yield eq, "False", r(code, x="a", y={"a": 1, "b": 2})
		yield eq, "True", r(code, x="c", y={"a": 1, "b": 2})
		yield eq, "False", r(code, x=0xff, y=color.Color(0x00, 0x80, 0xff, 0x42))
		yield eq, "True", r(code, x=0x23, y=color.Color(0x00, 0x80, 0xff, 0x42))


def test_and():
	for r in all_renderers:
		yield eq, "False", r(u'<?print x and y?>', x=False, y=False)
		yield eq, "False", r(u'<?print x and y?>', x=False, y=True)
		yield eq, "0", r(u'<?print x and y?>', x=0, y=True)


def test_or():
	for r in all_renderers:
		yield eq, "False", r(u'<?print x or y?>', x=False, y=False)
		yield eq, "True", r(u'<?print x or y?>', x=False, y=True)
		yield eq, "42", r(u'<?print x or y?>', x=42, y=True)


def test_not():
	for r in all_renderers:
		yield eq, "True", r(u'<?print not x?>', x=False)
		yield eq, "False", r(u'<?print not x?>', x=42)


def test_getitem():
	for r in all_renderers:
		yield eq, "u", r(u"<?print 'gurk'[1]?>")
		yield eq, "u", r(u"<?print x[1]?>", x="gurk")
		yield eq, "u", r(u"<?print 'gurk'[-3]?>")
		yield eq, "u", r(u"<?print x[-3]?>", x="gurk")
		yield raises, "IndexError", r(u"<?print 'gurk'[4]?>")
		yield raises, "index (4 )?out of range", r(u"<?print x[4]?>", x="gurk")
		yield raises, "IndexError", r(u"<?print 'gurk'[-5]?>")
		yield raises, "index (-5 )?out of range", r(u"<?print x[-5]?>", x="gurk")


def test_getslice12():
	for r in all_renderers:
		yield eq, "ur", r(u"<?print 'gurk'[1:3]?>")
		yield eq, "ur", r(u"<?print x[1:3]?>", x="gurk")
		yield eq, "ur", r(u"<?print 'gurk'[-3:-1]?>")
		yield eq, "ur", r(u"<?print x[-3:-1]?>", x="gurk")
		yield eq, "", r(u"<?print 'gurk'[4:10]?>")
		yield eq, "", r(u"<?print x[4:10]?>", x="gurk")
		yield eq, "", r(u"<?print 'gurk'[-10:-5]?>")
		yield eq, "", r(u"<?print x[-10:-5]?>", x="gurk")


def test_getslice1():
	for r in all_renderers:
		yield eq, "urk", r(u"<?print 'gurk'[1:]?>")
		yield eq, "urk", r(u"<?print x[1:]?>", x="gurk")
		yield eq, "urk", r(u"<?print 'gurk'[-3:]?>")
		yield eq, "urk", r(u"<?print x[-3:]?>", x="gurk")
		yield eq, "", r(u"<?print 'gurk'[4:]?>")
		yield eq, "", r(u"<?print x[4:]?>", x="gurk")
		yield eq, "gurk", r(u"<?print 'gurk'[-10:]?>")
		yield eq, "gurk", r(u"<?print x[-10:]?>", x="gurk")


def test_getslice2():
	for r in all_renderers:
		yield eq, "gur", r(u"<?print 'gurk'[:3]?>")
		yield eq, "gur", r(u"<?print x[:3]?>", x="gurk")
		yield eq, "gur", r(u"<?print 'gurk'[:-1]?>")
		yield eq, "gur", r(u"<?print x[:-1]?>", x="gurk")
		yield eq, "gurk", r(u"<?print 'gurk'[:10]?>")
		yield eq, "gurk", r(u"<?print x[:10]?>", x="gurk")
		yield eq, "", r(u"<?print 'gurk'[:-5]?>")
		yield eq, "", r(u"<?print x[:-5]?>", x="gurk")


def test_nested():
	sc = u"4"
	sv = u"x"
	n = 4
	# when using 10 compiling the variable will run out of registers
	# when using 8 Java will output "An irrecoverable stack overflow has occurred"
	depth = 7
	for i in xrange(depth):
		sc = u"({})+({})".format(sc, sc)
		sv = u"({})+({})".format(sv, sv)
		n = n + n

	for r in all_renderers:
		yield eq, str(n), r(u'<?print {}?>'.format(sc))
		yield eq, str(n), r(u'<?code x=4?><?print {}?>'.format(sv))


def test_precedence():
	for r in all_renderers:
		yield eq, "14", r(u'<?print 2+3*4?>')
		yield eq, "20", r(u'<?print (2+3)*4?>')
		yield eq, "10", r(u'<?print -2+-3*-4?>')
		yield eq, "14", r(u'<?print --2+--3*--4?>')
		yield eq, "14", r(u'<?print (-(-2))+(-((-3)*-(-4)))?>')
		yield eq, "42", r(u'<?print 2*data.value?>', data=dict(value=21))
		yield eq, "42", r(u'<?print data.value[0]?>', data=dict(value=[42]))
		yield eq, "42", r(u'<?print data[0].value?>', data=[dict(value=42)])
		yield eq, "42", r(u'<?print data[0][0][0]?>', data=[[[42]]])
		yield eq, "42", r(u'<?print data.value.value[0]?>', data=dict(value=dict(value=[42])))
		yield eq, "42", r(u'<?print data.value.value[0].value.value[0]?>', data=dict(value=dict(value=[dict(value=dict(value=[42]))])))


def test_bracket():
	sc = u"4"
	sv = u"x"
	for i in xrange(10):
		sc = u"({})".format(sc)
		sv = u"({})".format(sv)

	for r in all_renderers:
		yield eq, "4", r(u'<?print {}?>'.format(sc))
		yield eq, "4", r(u'<?code x=4?><?print {}?>'.format(sv))


def test_function_now():
	now = unicode(datetime.datetime.now())

	for r in all_renderers:
		yield raises, "now.*unknown", r(u"<?print now(1)?>")
		yield raises, "now.*unknown", r(u"<?print now(1, 2)?>")
		yield le, now, r(u"<?print now()?>")


def test_function_utcnow():
	utcnow = unicode(datetime.datetime.utcnow())

	for r in all_renderers:
		yield raises, "utcnow.*unknown", r(u"<?print utcnow(1)?>")
		yield raises, "utcnow.*unknown", r(u"<?print utcnow(1, 2)?>")
		utcnowfromtemplate = r(u"<?print utcnow()?>")
		# JS and Java only have milliseconds precision, but this shouldn't lead to problems here, as rendering the template takes longer than a millisecond
		yield le, utcnow, utcnowfromtemplate


def test_function_vars():
	code = u"<?if var in vars()?>yes<?else?>no<?end if?>"

	for r in all_renderers:
		yield raises, "vars.*unknown", r("<?print vars(1)?>")
		yield raises, "vars.*unknown", r("<?print vars(1, 2)?>")
		yield eq, "yes", r(code, var="spam", spam="eggs")
		yield eq, "no", r(code, var="nospam", spam="eggs")


def test_function_random():
	for r in all_renderers:
		yield raises, "random.*unknown", r("<?print random(1)?>")
		yield raises, "random.*unknown", r("<?print random(1, 2)?>")
		yield eq, "ok", r(u"<?code r = random()?><?if r>=0 and r<1?>ok<?else?>fail<?end if?>")


def test_function_randrange():
	for r in all_renderers:
		yield raises, "randrange.*unknown", r("<?print randrange()?>")
		yield eq, "ok", r(u"<?code r = randrange(4)?><?if r>=0 and r<4?>ok<?else?>fail<?end if?>")
		yield eq, "ok", r(u"<?code r = randrange(17, 23)?><?if r>=17 and r<23?>ok<?else?>fail<?end if?>")
		yield eq, "ok", r(u"<?code r = randrange(17, 23, 2)?><?if r>=17 and r<23 and r%2?>ok<?else?>fail<?end if?>")


def test_function_randchoice():
	for r in all_renderers:
		yield raises, "randchoice.*unknown", r("<?print randchoice()?>")
		yield eq, "ok", r(u"<?code r = randchoice('abc')?><?if r in 'abc'?>ok<?else?>fail<?end if?>")
		yield eq, "ok", r(u"<?code s = [17, 23, 42]?><?code r = randchoice(s)?><?if r in s?>ok<?else?>fail<?end if?>")
		yield eq, "ok", r(u"<?code s = #12345678?><?code sl = [0x12, 0x34, 0x56, 0x78]?><?code r = randchoice(s)?><?if r in sl?>ok<?else?>fail<?end if?>")


def test_function_xmlescape():
	for r in all_renderers:
		yield raises, "xmlescape.*unknown", r(u"<?print xmlescape()?>")
		yield raises, "xmlescape.*unknown", r(u"<?print xmlescape(1, 2)?>")
		yield eq, "&lt;&lt;&gt;&gt;&amp;&#39;&quot;gurk", r(u"<?print xmlescape(data)?>", data='<<>>&\'"gurk')


def test_function_csv():
	for r in all_renderers:
		yield raises, "csv.*unknown", r(u"<?print csv()?>")
		yield raises, "csv.*unknown", r(u"<?print csv(1, 2)?>")
		yield eq, "", r(u"<?print csv(data)?>", data=None)
		yield eq, "False", r(u"<?print csv(data)?>", data=False)
		yield eq, "True", r(u"<?print csv(data)?>", data=True)
		yield eq, "42", r(u"<?print csv(data)?>", data=42)
		# no check for float
		yield eq, "abc", r(u"<?print csv(data)?>", data="abc")
		yield eq, '"a,b,c"', r(u"<?print csv(data)?>", data="a,b,c")
		yield eq, '"a""b""c"', r(u"<?print csv(data)?>", data='a"b"c')
		yield eq, '"a\nb\nc"', r(u"<?print csv(data)?>", data="a\nb\nc")


def test_function_json():
	for r in all_renderers:
		yield raises, "json.*unknown", r(u"<?print json()?>")
		yield raises, "json.*unknown", r(u"<?print json(1, 2)?>")
		yield eq, "null", r(u"<?print json(data)?>", data=None)
		yield eq, "false", r(u"<?print json(data)?>", data=False)
		yield eq, "true", r(u"<?print json(data)?>", data=True)
		yield eq, "42", r(u"<?print json(data)?>", data=42)
		# no check for float
		yield eq, '"abc"', r(u"<?print json(data)?>", data="abc")
		yield eq, '[1, 2, 3]', r(u"<?print json(data)?>", data=[1, 2, 3])
		yield eq, '[1, 2, 3]', r(u"<?print json(data)?>", data=PseudoList([1, 2, 3]))
		yield eq, '{"one": 1}', r(u"<?print json(data)?>", data={"one": 1})
		yield eq, '{"one": 1}', r(u"<?print json(data)?>", data=PseudoDict({"one": 1}))


def test_function_str():
	code = u"<?print str(data)?>"
	for r in all_renderers:
		yield raises, "str.*unknown", r(u"<?print str()?>")
		yield raises, "str.*unknown", r(u"<?print str(1, 2)?>")
		yield eq, "", r(code, data=None)
		yield eq, "True", r(code, data=True)
		yield eq, "False", r(code, data=False)
		yield eq, "42", r(code, data=42)
		yield eq, "4.2", r(code, data=4.2)
		yield eq, "foo", r(code, data="foo")
		yield eq, "2011-02-09", r(code, data=datetime.date(2011, 2, 9))
		yield eq, "2011-02-09 12:34:56", r(code, data=datetime.datetime(2011, 2, 9, 12, 34, 56))
		yield eq, "2011-02-09 12:34:56.987000", r(code, data=datetime.datetime(2011, 2, 9, 12, 34, 56, 987000))


def test_function_int():
	for r in all_renderers:
		yield raises, "int.*unknown", RenderPython(u"<?print int()?>")
		yield raises, "int.*unknown", RenderPython(u"<?print int(1, 2, 3)?>")
		yield raises, "int\\(\\) argument must be a string or a number|int\\(null\\) not supported", RenderPython(u"<?print int(data)?>", data=None)
		yield raises, "invalid literal for int|NumberFormatException", RenderPython(u"<?print int(data)?>", data="foo")
		yield eq, "1", r(u"<?print int(data)?>", data=True)
		yield eq, "0", r(u"<?print int(data)?>", data=False)
		yield eq, "42", r(u"<?print int(data)?>", data=42)
		yield eq, "4", r(u"<?print int(data)?>", data=4.2)
		yield eq, "42", r(u"<?print int(data)?>", data="42")
		yield eq, "66", r(u"<?print int(data, 16)?>", data="42")


def test_function_float():
	code = u"<?print float(data)?>"

	for r in all_renderers:
		yield raises, "float.*unknown", r(u"<?print float()?>")
		yield raises, "float.*unknown", r(u"<?print float(1, 2, 3)?>")
		yield raises, "float\\(\\) argument must be a string or a number|float\\(null\\) not supported", r(code, data=None)
		yield eq, "4.2", r(code, data=4.2)
		if r is not RenderJS:
			yield eq, "1.0", r(code, data=True)
			yield eq, "0.0", r(code, data=False)
			yield eq, "42.0", r(code, data=42)
			yield eq, "42.0", r(code, data="42")
		else:
			yield evaleq, 1.0, r(code, data=True)
			yield evaleq, 0.0, r(code, data=False)
			yield evaleq, 42.0, r(code, data=42)
			yield evaleq, 42.0, r(code, data="42")


def test_function_len():
	code = u"<?print len(data)?>"
	for r in all_renderers:
		yield raises, "len.*unknown", r(u"<?print len()?>")
		yield raises, "len.*unknown", r(u"<?print len(1, 2)?>")
		yield raises, "has no len\\(\\)|len\\(.*\\) not supported", r(code, data=None)
		yield raises, "has no len\\(\\)|len\\(.*\\) not supported", r(code, data=True)
		yield raises, "has no len\\(\\)|len\\(.*\\) not supported", r(code, data=False)
		yield raises, "has no len\\(\\)|len\\(.*\\) not supported", r(code, data=42)
		yield raises, "has no len\\(\\)|len\\(.*\\) not supported", r(code, data=4.2)
		yield eq, "42", r(code, data=42*"?")
		yield eq, "42", r(code, data=42*[None])
		yield eq, "42", r(code, data=dict.fromkeys(xrange(42)))


def test_function_enumerate():
	code = u"<?for (i, value) in enumerate(data)?><?print i?>:<?print value?>\n<?end for?>"
	for r in all_renderers:
		yield raises, "enumerate.*unknown", r(u"<?print enumerate()?>")
		yield raises, "enumerate.*unknown", r(u"<?print enumerate(1, 2)?>")
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=None)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=True)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=False)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=42)
		yield raises, "is not iterable|iter\\(.*\\) not supported", r(code, data=4.2)
		yield eq, "0:f\n1:o\n2:o\n", r(code, data="foo")
		yield eq, "0:foo\n1:bar\n", r(code, data=["foo", "bar"])
		yield eq, "0:foo\n", r(code, data=dict(foo=True))


def test_function_isnone():
	code = u"<?print isnone(data)?>"
	for r in all_renderers:
		yield raises, "isnone.*unknown", r(u"<?print isnone()?>")
		yield raises, "isnone.*unknown", r(u"<?print isnone(1, 2)?>")
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
		yield eq, "False", r(code, data=ul4c.compile(u""))
		yield eq, "False", r(code, data=color.red)


def test_function_isbool():
	code = u"<?print isbool(data)?>"

	for r in all_renderers:
		yield raises, "isbool.*unknown", r(u"<?print isbool()?>")
		yield raises, "isbool.*unknown", r(u"<?print isbool(1, 2)?>")
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
		yield eq, "False", r(code, data=ul4c.compile(u""))
		yield eq, "False", r(code, data=color.red)


def test_function_isint():
	code = u"<?print isint(data)?>"

	for r in all_renderers:
		yield raises, "isint.*unknown", r(u"<?print isint()?>")
		yield raises, "isint.*unknown", r(u"<?print isint(1, 2)?>")
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
		yield eq, "False", r(code, data=ul4c.compile(u""))
		yield eq, "False", r(code, data=color.red)


def test_function_isfloat():
	code = u"<?print isfloat(data)?>"

	for r in all_renderers:
		yield raises, "isfloat.*unknown", r(u"<?print isfloat()?>")
		yield raises, "isfloat.*unknown", r(u"<?print isfloat(1, 2)?>")
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
		yield eq, "False", r(code, data=ul4c.compile(u""))
		yield eq, "False", r(code, data=color.red)


def test_function_isstr():
	code = u"<?print isstr(data)?>"

	for r in all_renderers:
		yield raises, "isstr.*unknown", r(u"<?print isstr()?>")
		yield raises, "isstr.*unknown", r(u"<?print isstr(1, 2)?>")
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
		yield eq, "False", r(code, data=ul4c.compile(u""))
		yield eq, "False", r(code, data=color.red)


def test_function_isdate():
	code = u"<?print isdate(data)?>"

	for r in all_renderers:
		yield raises, "isdate.*unknown", r(u"<?print isdate()?>")
		yield raises, "isdate.*unknown", r(u"<?print isdate(1, 2)?>")
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
		yield eq, "False", r(code, data=ul4c.compile(u""))
		yield eq, "False", r(code, data=color.red)


def test_function_islist():
	code = u"<?print islist(data)?>"

	for r in all_renderers:
		yield raises, "islist.*unknown", r(u"<?print islist()?>")
		yield raises, "islist.*unknown", r(u"<?print islist(1, 2)?>")
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
		yield eq, "False", r(code, data=ul4c.compile(u""))
		yield eq, "False", r(code, data=color.red)


def test_function_isdict():
	code = u"<?print isdict(data)?>"

	for r in all_renderers:
		yield raises, "isdict.*unknown", r(u"<?print isdict()?>")
		yield raises, "isdict.*unknown", r(u"<?print isdict(1, 2)?>")
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
		yield eq, "False", r(code, data=ul4c.compile(u""))
		yield eq, "False", r(code, data=color.red)


def test_function_istemplate():
	code = u"<?print istemplate(data)?>"

	for r in all_renderers:
		yield raises, "istemplate.*unknown", r(u"<?print istemplate()?>")
		yield raises, "istemplate.*unknown", r(u"<?print istemplate(1, 2)?>")
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
		yield eq, "True", r(code, data=ul4c.compile(u""))
		yield eq, "False", r(code, data=color.red)


def test_function_iscolor():
	code = u"<?print iscolor(data)?>"

	for r in all_renderers:
		yield raises, "iscolor.*unknown", r(u"<?print iscolor()?>")
		yield raises, "iscolor.*unknown", r(u"<?print iscolor(1, 2)?>")
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
		yield eq, "False", r(code, data=ul4c.compile(u""))
		yield eq, "True", r(code, data=color.red)


def test_function_get():
	for r in all_renderers:
		yield raises, "get.*unknown", r(u"<?print get()?>")
		yield eq, "", r(u"<?print get('x')?>")
		yield eq, "42", r(u"<?print get('x')?>", x=42)
		yield eq, "17", r(u"<?print get('x', 17)?>")
		yield eq, "42", r(u"<?print get('x', 17)?>", x=42)


def test_function_repr():
	code = u"<?print repr(data)?>"

	for r in all_renderers:
		yield raises, "repr.*unknown", r(u"<?print repr()?>")
		yield raises, "repr.*unknown", r(u"<?print repr(1, 2)?>")
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
		yield eq, "@2011-02-07T12:34:56.123000", r(code, data=datetime.datetime(2011, 2, 7, 12, 34, 56, 123000))
		yield eq, "@2011-02-07T12:34:56", r(code, data=datetime.datetime(2011, 2, 7, 12, 34, 56))
		yield eq, "@2011-02-07T", r(code, data=datetime.datetime(2011, 2, 7))
		yield eq, "@2011-02-07T", r(code, data=datetime.date(2011, 2, 7))


def test_method_format():
	t = datetime.datetime(2011, 2, 6, 12, 34, 56, 987000)
	code = u"<?print format(data, format)?>"
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


def test_function_chr():
	code = u"<?print chr(data)?>"

	for r in all_renderers:
		yield raises, "chr.*unknown", r(u"<?print chr()?>")
		yield raises, "chr.*unknown", r(u"<?print chr(1, 2)?>")
		yield eq, "\x00", r(code, data=0)
		yield eq, "a", r(code, data=ord("a"))
		yield eq, u"\u20ac", r(code, data=0x20ac)


def test_function_ord():
	code = u"<?print ord(data)?>"

	for r in all_renderers:
		yield raises, "ord.*unknown", r(u"<?print ord()?>")
		yield raises, "ord.*unknown", r(u"<?print ord(1, 2)?>")
		yield eq, "0", r(code, data="\x00")
		yield eq, str(ord("a")), r(code, data="a")
		yield eq, str(0x20ac), r(code, data=u"\u20ac")


def test_function_hex():
	code = u"<?print hex(data)?>"

	for r in all_renderers:
		yield raises, "hex.*unknown", r(u"<?print hex()?>")
		yield raises, "hex.*unknown", r(u"<?print hex(1, 2)?>")
		yield eq, "0x0", r(code, data=0)
		yield eq, "0xff", r(code, data=0xff)
		yield eq, "0xffff", r(code, data=0xffff)
		yield eq, "-0xffff", r(code, data=-0xffff)


def test_function_oct():
	code = u"<?print oct(data)?>"

	for r in all_renderers:
		yield raises, "oct.*unknown", r(u"<?print oct()?>")
		yield raises, "oct.*unknown", r(u"<?print oct(1, 2)?>")
		yield eq, "0o0", r(code, data=0)
		yield eq, "0o77", r(code, data=077)
		yield eq, "0o7777", r(code, data=07777)
		yield eq, "-0o7777", r(code, data=-07777)


def test_function_bin():
	code = u"<?print bin(data)?>"

	for r in all_renderers:
		yield raises, "bin.*unknown", r(u"<?print bin()?>")
		yield raises, "bin.*unknown", r(u"<?print bin(1, 2)?>")
		yield eq, "0b0", r(code, data=0)
		yield eq, "0b11", r(code, data=3)
		yield eq, "-0b1111", r(code, data=-15)


def test_function_abs():
	code = u"<?print abs(data)?>"

	for r in all_renderers:
		yield raises, "abs.*unknown", r(u"<?print abs()?>")
		yield raises, "abs.*unknown", r(u"<?print abs(1, 2)?>")
		yield eq, "0", r(code, data=0)
		yield eq, "42", r(code, data=42)
		yield eq, "42", r(code, data=-42)


def test_function_sorted():
	code = u"<?for i in sorted(data)?><?print i?><?end for?>"

	for r in all_renderers:
		yield raises, "sorted.*unknown", r(u"<?print sorted()?>")
		yield raises, "sorted.*unknown", r(u"<?print sorted(1, 2)?>")
		yield eq, "gkru", r(code, data="gurk")
		yield eq, "24679", r(code, data="92746")
		yield eq, "012", r(code, data={0: "zero", 1: "one", 2: "two"})


def test_function_range():
	code1 = u"<?for i in range(data)?><?print i?><?end for?>"
	code2 = u"<?for i in range(data[0], data[1])?><?print i?><?end for?>"
	code3 = u"<?for i in range(data[0], data[1], data[2])?><?print i?><?end for?>"

	for r in all_renderers:
		yield raises, "range.*unknown", r(u"<?print range()?>")
		yield eq, "", r(code1, data=-10)
		yield eq, "", r(code1, data=0)
		yield eq, "0", r(code1, data=1)
		yield eq, "01234", r(code1, data=5)
		yield eq, "", r(code2, data=[0, -10])
		yield eq, "", r(code2, data=[0, 0])
		yield eq, "01234", r(code2, data=[0, 5])
		yield eq, "-5-4-3-2-101234", r(code2, data=[-5, 5])
		yield eq, "", r(code3, data=[0, -10, 1])
		yield eq, "", r(code3, data=[0, 0, 1])
		yield eq, "02468", r(code3, data=[0, 10, 2])
		yield eq, "", r(code3, data=[0, 10, -2])
		yield eq, "108642", r(code3, data=[10, 0, -2])
		yield eq, "", r(code3, data=[10, 0, 2])


def test_function_zip():
	code2 = u"<?for (ix, iy) in zip(x, y)?><?print ix?>-<?print iy?>;<?end for?>"
	code3 = u"<?for (ix, iy, iz) in zip(x, y, z)?><?print ix?>-<?print iy?>+<?print iz?>;<?end for?>"

	for r in all_renderers:
		yield raises, "zip.*unknown", r(u"<?print zip(1)?>")
		yield eq, "", r(code2, x=[], y=[])
		yield eq, "1-3;2-4;", r(code2, x=[1, 2], y=[3, 4])
		yield eq, "1-4;2-5;", r(code2, x=[1, 2, 3], y=[4, 5])
		yield eq, "", r(code3, x=[], y=[], z=[])
		yield eq, "1-3+5;2-4+6;", r(code3, x=[1, 2], y=[3, 4], z=[5, 6])
		yield eq, "1-4+6;", r(code3, x=[1, 2, 3], y=[4, 5], z=[6])


def test_function_type():
	code = u"<?print type(x)?>"

	for r in all_renderers:
		yield raises, "type.*unknown", r(u"<?print type()?>")
		yield raises, "type.*unknown", r(u"<?print type(1, 2)?>")
		yield eq, "none", r(code, x=None)
		yield eq, "bool", r(code, x=False)
		yield eq, "bool", r(code, x=True)
		yield eq, "int", r(code, x=42)
		yield eq, "int", r(code, x=42L)
		yield eq, "float", r(code, x=4.2)
		yield eq, "str", r(code, x="foo")
		yield eq, "str", r(code, x=u"foo")
		yield eq, "date", r(code, x=datetime.datetime.now())
		yield eq, "date", r(code, x=datetime.date.today())
		yield eq, "list", r(code, x=(1, 2))
		yield eq, "list", r(code, x=[1, 2])
		yield eq, "list", r(code, x=PseudoList([1, 2]))
		yield eq, "dict", r(code, x={1: 2})
		yield eq, "dict", r(code, x=PseudoDict({1: 2}))
		yield eq, "template", r(code, x=ul4c.compile(""))
		yield eq, "color", r(code, x=color.red)


def test_function_reversed():
	code = u"<?for i in reversed(x)?>(<?print i?>)<?end for?>"

	for r in all_renderers:
		yield raises, "reversed.*unknown", r(u"<?print reversed()?>")
		yield raises, "reversed.*unknown", r(u"<?print reversed(1, 2)?>")
		yield eq, "(3)(2)(1)", r(code, x="123")
		yield eq, "(3)(2)(1)", r(code, x=[1, 2, 3])
		yield eq, "(3)(2)(1)", r(code, x=(1, 2, 3))


def test_function_rgb():
	for r in all_renderers:
		yield eq, "#369", r("<?print repr(rgb(0.2, 0.4, 0.6))?>")
		yield eq, "#369c", r("<?print repr(rgb(0.2, 0.4, 0.6, 0.8))?>")


def test_function_hls():
	for r in all_renderers:
		yield eq, "#fff", r("<?print repr(hls(0, 1, 0))?>")
		yield eq, "#fff0", r("<?print repr(hls(0, 1, 0, 0))?>")


def test_function_hsv():
	for r in all_renderers:
		yield eq, "#fff", r("<?print repr(hsv(0, 0, 1))?>")
		yield eq, "#fff0", r("<?print repr(hsv(0, 0, 1, 0))?>")


def test_method_upper():
	for r in all_renderers:
		yield eq, "GURK", r(u"<?print 'gurk'.upper()?>")


def test_method_lower():
	for r in all_renderers:
		yield eq, "gurk", r(u"<?print 'GURK'.lower()?>")


def test_method_capitalize():
	for r in all_renderers:
		yield eq, "Gurk", r(u"<?print 'gURK'.capitalize()?>")


def test_method_startswith():
	for r in all_renderers:
		yield eq, "True", r(u"<?print 'gurkhurz'.startswith('gurk')?>")
		yield eq, "False", r(u"<?print 'gurkhurz'.startswith('hurz')?>")


def test_method_endswith():
	for r in all_renderers:
		yield eq, "True", r(u"<?print 'gurkhurz'.endswith('hurz')?>")
		yield eq, "False", r(u"<?print 'gurkhurz'.endswith('gurk')?>")


def test_method_strip():
	for r in all_renderers:
		yield eq, "gurk", r(r"<?print obj.strip()?>", obj=' \t\r\ngurk \t\r\n')
		yield eq, "gurk", r(r"<?print obj.strip('xyz')?>", obj='xyzzygurkxyzzy')


def test_method_lstrip():
	for r in all_renderers:
		yield eq, "gurk \t\r\n", r("<?print obj.lstrip()?>", obj=" \t\r\ngurk \t\r\n")
		yield eq, "gurkxyzzy", r("<?print obj.lstrip(arg)?>", obj="xyzzygurkxyzzy", arg="xyz")


def test_method_rstrip():
	for r in all_renderers:
		yield eq, " \t\r\ngurk", r("<?print obj.rstrip()?>", obj=" \t\r\ngurk \t\r\n")
		yield eq, "xyzzygurk", r("<?print obj.rstrip(arg)?>", obj="xyzzygurkxyzzy", arg="xyz")


def test_method_split():
	for r in all_renderers:
		yield eq, "(f)(o)(o)", r(u"<?for item in obj.split()?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
		yield eq, "(f)(o \t\r\no \t\r\n)", r(u"<?for item in obj.split(None, 1)?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
		yield eq, "()(f)(o)(o)()", r(u"<?for item in obj.split(arg)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")
		yield eq, "()(f)(oxxoxx)", r(u"<?for item in obj.split(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")


def test_method_rsplit():
	for r in all_renderers:
		yield eq, "(f)(o)(o)", r(u"<?for item in obj.rsplit()?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
		yield eq, "( \t\r\nf \t\r\no)(o)", r(u"<?for item in obj.rsplit(None, 1)?>(<?print item?>)<?end for?>", obj=" \t\r\nf \t\r\no \t\r\no \t\r\n")
		yield eq, "()(f)(o)(o)()", r(u"<?for item in obj.rsplit(arg)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")
		yield eq, "(xxfxxo)(o)()", r(u"<?for item in obj.rsplit(arg, 2)?>(<?print item?>)<?end for?>", obj="xxfxxoxxoxx", arg="xx")


def test_method_replace():
	for r in all_renderers:
		yield eq, 'goork', r(ur"<?print 'gurk'.replace('u', 'oo')?>")


def test_method_render():
	for r in all_renderers:
		t = ul4c.compile(u'(<?print data?>)')
		yield eq, '(GURK)', r(u"<?print t.render(data='gurk').upper()?>", t=t)
		yield eq, '(GURK)', r(u"<?print t.render(**{'data': 'gurk'}).upper()?>", t=t)

		t = ul4c.compile(u'(gurk)')
		yield eq, '(GURK)', r(u"<?print t.render().upper()?>", t=t)


def test_method_isoformat():
	t = datetime.datetime(2010, 02, 22, 12, 34, 56)
	for r in all_renderers:
		yield eq, 'Mon, 22 Feb 2010 12:34:56 GMT', r(ur"<?print data.mimeformat()?>", data=t)


def test_method_get():
	for r in all_renderers:
		yield eq, "42", r(u"<?print {}.get('foo', 42)?>")
		yield eq, "17", r(u"<?print {'foo': 17}.get('foo', 42)?>")
		yield eq, "", r(u"<?print {}.get('foo')?>")
		yield eq, "17", r(u"<?print {'foo': 17}.get('foo')?>")


def test_method_r_g_b_a():
	for r in all_renderers:
		yield eq, '0x11', r(u'<?code c = #123?><?print hex(c.r())?>')
		yield eq, '0x22', r(u'<?code c = #123?><?print hex(c.g())?>')
		yield eq, '0x33', r(u'<?code c = #123?><?print hex(c.b())?>')
		yield eq, '0xff', r(u'<?code c = #123?><?print hex(c.a())?>')


def test_method_hls():
	for r in all_renderers:
		yield eq, '0', r(u'<?code c = #fff?><?print int(c.hls()[0])?>')
		yield eq, '1', r(u'<?code c = #fff?><?print int(c.hls()[1])?>')
		yield eq, '0', r(u'<?code c = #fff?><?print int(c.hls()[2])?>')


def test_method_hlsa():
	for r in all_renderers:
		yield eq, '0', r(u'<?code c = #fff?><?print int(c.hlsa()[0])?>')
		yield eq, '1', r(u'<?code c = #fff?><?print int(c.hlsa()[1])?>')
		yield eq, '0', r(u'<?code c = #fff?><?print int(c.hlsa()[2])?>')
		yield eq, '1', r(u'<?code c = #fff?><?print int(c.hlsa()[3])?>')


def test_method_hsv():
	for r in all_renderers:
		yield eq, '0', r(u'<?code c = #fff?><?print int(c.hsv()[0])?>')
		yield eq, '0', r(u'<?code c = #fff?><?print int(c.hsv()[1])?>')
		yield eq, '1', r(u'<?code c = #fff?><?print int(c.hsv()[2])?>')


def test_method_hsva():
	for r in all_renderers:
		yield eq, '0', r(u'<?code c = #fff?><?print int(c.hsva()[0])?>')
		yield eq, '0', r(u'<?code c = #fff?><?print int(c.hsva()[1])?>')
		yield eq, '1', r(u'<?code c = #fff?><?print int(c.hsva()[2])?>')
		yield eq, '1', r(u'<?code c = #fff?><?print int(c.hsva()[3])?>')


def test_method_lum():
	for r in all_renderers:
		yield eq, 'True', r(u'<?print #fff.lum() == 1?>')


def test_method_withlum():
	for r in all_renderers:
		yield eq, '#fff', r(u'<?print #000.withlum(1)?>')


def test_method_witha():
	for r in all_renderers:
		yield eq, '#0063a82a', r(u'<?print repr(#0063a8.witha(42))?>')


def test_method_join():
	for r in all_renderers:
		yield eq, '1,2,3,4', r(u'<?print ",".join("1234")?>')
		yield eq, '1,2,3,4', r(u'<?print ",".join([1, 2, 3, 4])?>')


def test_method_find():
	for r in all_renderers:
		yield eq, '-1', r(u'<?print s.find("ks")?>', s="gurkgurk")
		yield eq, '2', r(u'<?print s.find("rk")?>', s="gurkgurk")
		yield eq, '2', r(u'<?print s.find("rk", 2)?>', s="gurkgurk")
		yield eq, '2', r(u'<?print s.find("rk", 2, 4)?>', s="gurkgurk")
		yield eq, '6', r(u'<?print s.find("rk", 4, 8)?>', s="gurkgurk")
		yield eq, '-1', r(u'<?print s.find("rk", 2, 3)?>', s="gurkgurk")
		yield eq, '-1', r(u'<?print s.find("rk", 7)?>', s="gurkgurk")


def test_method_rfind():
	for r in all_renderers:
		yield eq, '-1', r(u'<?print s.rfind("ks")?>', s="gurkgurk")
		yield eq, '6', r(u'<?print s.rfind("rk")?>', s="gurkgurk")
		yield eq, '6', r(u'<?print s.rfind("rk", 2)?>', s="gurkgurk")
		yield eq, '2', r(u'<?print s.rfind("rk", 2, 4)?>', s="gurkgurk")
		yield eq, '6', r(u'<?print s.rfind("rk", 4, 8)?>', s="gurkgurk")
		yield eq, '-1', r(u'<?print s.rfind("rk", 2, 3)?>', s="gurkgurk")
		yield eq, '-1', r(u'<?print s.rfind("rk", 7)?>', s="gurkgurk")


def test_method_day():
	for r in all_renderers:
		yield eq, '12', r(u'<?print @2010-05-12T.day()?>')
		yield eq, '12', r(u'<?print d.day()?>', d=datetime.date(2010, 5, 12))


def test_method_month():
	for r in all_renderers:
		yield eq, '5', r(u'<?print @2010-05-12T.month()?>')
		yield eq, '5', r(u'<?print d.month()?>', d=datetime.date(2010, 5, 12))


def test_method_year():
	for r in all_renderers:
		yield eq, '5', r(u'<?print @2010-05-12T.month()?>')
		yield eq, '5', r(u'<?print d.month()?>', d=datetime.date(2010, 5, 12))


def test_method_hour():
	for r in all_renderers:
		yield eq, '16', r(u'<?print @2010-05-12T16:47:56.hour()?>')
		yield eq, '16', r(u'<?print d.hour()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


def test_method_minute():
	for r in all_renderers:
		yield eq, '47', r(u'<?print @2010-05-12T16:47:56.minute()?>')
		yield eq, '47', r(u'<?print d.minute()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


def test_method_second():
	for r in all_renderers:
		yield eq, '56', r(u'<?print @2010-05-12T16:47:56.second()?>')
		yield eq, '56', r(u'<?print d.second()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


def test_method_microsecond():
	for r in all_renderers:
		yield eq, '123000', r(u'<?print @2010-05-12T16:47:56.123000.microsecond()?>')
		yield eq, '123000', r(u'<?print d.microsecond()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56, 123000))


def test_method_weekday():
	for r in all_renderers:
		yield eq, '2', r(u'<?print @2010-05-12T.weekday()?>')
		yield eq, '2', r(u'<?print d.weekday()?>', d=datetime.date(2010, 5, 12))


def test_method_yearday():
	for r in all_renderers:
		yield eq, '1', r(u'<?print @2010-01-01T.yearday()?>')
		yield eq, '366', r(u'<?print @2008-12-31T.yearday()?>')
		yield eq, '365', r(u'<?print @2010-12-31T.yearday()?>')
		yield eq, '132', r(u'<?print @2010-05-12T.yearday()?>')
		yield eq, '132', r(u'<?print @2010-05-12T16:47:56.yearday()?>')
		yield eq, '132', r(u'<?print d.yearday()?>', d=datetime.date(2010, 5, 12))
		yield eq, '132', r(u'<?print d.yearday()?>', d=datetime.datetime(2010, 5, 12, 16, 47, 56))


def test_render():
	t = ul4c.compile(u'<?print prefix?><?print data?><?print suffix?>')
	for r in all_renderers:
		yield eq, '(f)(o)(o)', r(u'<?for c in data?><?render t(data=c, prefix="(", suffix=")")?><?end for?>', t=t, data='foo')
		yield eq, '(f)(o)(o)', r(u'<?for c in data?><?render t(data=c, **{"prefix": "(", "suffix": ")"})?><?end for?>', t=t, data='foo')


def test_render_var():
	t = ul4c.compile(u'<?code x += 1?><?print x?>')
	for r in all_renderers:
		yield eq, '42,43,42', r(u'<?print x?>,<?render t(x=x)?>,<?print x?>', t=t, x=42)


def test_def():
	for r in all_renderers:
		yield eq, 'foo', r(u'<?def lower?><?print x.lower()?><?end def?><?print lower.render(x="FOO")?>')


def test_parse():
	for r in all_renderers:
		yield eq, '42', r(u'<?print data.Noner?>', data=dict(Noner=42))


def test_nested_exceptions():
	tmpl1 = ul4c.compile(u"<?print 2*x?>")
	tmpl2 = ul4c.compile(u"<?render tmpl1(x=x)?>")
	tmpl3 = ul4c.compile(u"<?render tmpl2(tmpl1=tmpl1, x=x)?>")

	for r in all_python_renderers:
		msg = "TypeError .*render tmpl3.*render tmpl2.*render tmpl1.*print 2.*unsupported operand type|.* \\* .* not supported"
		yield raises, msg, r(u"<?render tmpl3(tmpl1=tmpl1, tmpl2=tmpl2, x=x)?>", tmpl1=tmpl1, tmpl2=tmpl2, tmpl3=tmpl3, x=None)


def test_note():
	for r in all_renderers:
		yield eq, "foo", r(u"f<?note This is?>o<?note a comment?>o")


def test_templateattributes():
	s = "<?print x?>"
	t = ul4c.compile(s)

	for r in all_python_renderers:
		yield eq, "<?", r(u"<?print template.startdelim?>", template=t)
		yield eq, "?>", r(u"<?print template.enddelim?>", template=t)
		yield eq, s, r(u"<?print template.source?>", template=t)
		yield eq, "2", r(u"<?print len(template.opcodes)?>", template=t)
		yield eq, "loadvar", r(u"<?print template.opcodes[0].code?>", template=t)
		yield eq, "0", r(u"<?print template.opcodes[0].r1?>", template=t)
		yield eq, "", r(u"<?print template.opcodes[0].r2?>", template=t)
		yield eq, "x", r(u"<?print template.opcodes[0].arg?>", template=t)
		yield eq, s, r(u"<?code loc = template.opcodes[0].location?><?print template.source[loc.starttag:loc.endtag]?>", template=t)
		yield eq, "x", r(u"<?code loc = template.opcodes[0].location?><?print template.source[loc.startcode:loc.endcode]?>", template=t)


def universaltemplate():
	return ul4c.compile("""
		text
		<?code x = 'gurk'?>
		<?code x = 42?>
		<?code x = 4.2?>
		<?code x = None?>
		<?code x = False?>
		<?code x = True?>
		<?code x = @2009-01-04T?>
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
		<?render x(a=1, b=2)?>
		<?def x?>foo<?end def?>
		<?render x()?>
	""")


def test_strtemplate():
	t = universaltemplate()
	str(t)


def test_pythonsource():
	t = universaltemplate()
	t.pythonsource()
	t.pythonsource("template")


def test_pythonfunction():
	t = universaltemplate()
	t.pythonfunction()


def test_jssource():
	t = universaltemplate()
	t.jssource()


def test_javasource():
	t = universaltemplate()
	t.javasource()
