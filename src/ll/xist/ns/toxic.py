#! /usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2004-2008 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2004-2008 by Walter Dörwald
##
## All Rights Reserved
##
## See xist/__init__.py for the license


'''
This module is an XIST namespace. It can be used for generating Oracle database
functions that return XML strings. This is done by embedding processing
instructions containing PL/SQL code into XML files and transforming those
files with XIST.

An example that generates an HTML table containing the result of a search for
names in a ``person`` table might look like this::

	from ll.xist import xsc
	from ll.xist.ns import html, htmlspecials
	from ll import toxic

	class search(xsc.Element):
		def convert(self, converter):
			e = xsc.Frag(
				toxic.args("search varchar2"),
				toxic.vars("i integer;"),
				toxic.type("varchar2(32000);"),
				htmlspecials.plaintable(
					toxic.code("""
						i := 1;
						for row in (select name from person where name like search) loop
							"""),
							html.tr(
								html.th(toxic.expr("i"), align="right"),
								html.td(toxic.expr("xmlescape(row.name)"))
							),
							toxic.code("""
							i := i+1;
						end loop;
					""")
				)
			)
			return e.convert(converter)

	print toxic.xml2ora(search().conv().asstring(encoding"us-ascii")).encode("us-ascii")

Running this script will give the following output (the indentation will be
different though)::

	(
		search varchar2
	)
	return varchar2
	as
		c_out varchar2(32000);
		i integer;
	begin
		c_out := c_out || '<table cellpadding="0" border="0" cellspacing="0">';
		i := 1;
		for row in (select name from person where name like search) loop
			c_out := c_out || '<tr><th align="right">';
			c_out := c_out || i;
			c_out := c_out || '</th><td>';
			c_out := c_out || xmlescape(row.name);
			c_out := c_out || '</td></tr>';
			i := i+1;
		end loop;
		c_out := c_out || '</table>';
		return c_out;
	end;

Instead of generating the XML from a single XIST element, it's of course also
possible to use an XML file. One that generates the same function as the
one above looks like this::

	<?args
		search varchar2
	?>
	<?vars
		i integer;
	?>
	<plaintable class="search">
		<?code
			i := 1;
			for row in (select name from person where name like search) loop
				?>
				<tr>
					<th align="right"><?expr i?></th>
					<td><?expr xmlescape(row.name)?></td>
				</tr>
				<?code
				i := i + 1;
			end loop;
		?>
	</plaintable>

When the file is saved as :file:`search.sqlxsc` then parsing the file,
transforming it and printing the function body works like this::

	from ll.xist import parsers
	from ll.xist.ns import html, htmlspecials
	from ll import toxic

	node = parsers.parsefile("search.sqlxsc")
	node = node.conv()
	print toxic.xml2ora(node.asString(encoding="us-ascii")).encode("us-ascii")
'''


import cStringIO

from ll import misc
from ll.xist import xsc, publishers


__docformat__ = "reStructuredText"


xmlns = "http://xmlns.livinglogic.de/xist/ns/toxic"


def stringify(string, nchar=False):
	"""
	Format :var:`string` as multiple PL/SQL string constants or expressions.
	:var:`nchar` specifies if a ``NVARCHAR`` constant should be generated or a
	``VARCHAR``. This is a generator.
	"""
	current = []

	for c in string:
		if ord(c) < 32:
			if current:
				if nchar:
					yield u"N'%s'" % u"".join(current)
				else:
					yield u"'%s'" % u"".join(current)
				current = []
			yield u"chr(%d)" % ord(c)
		else:
			if c == u"'":
				c = u"''"
			current.append(c)
			if len(current) > 1000:
				if nchar:
					yield u"N'%s'" % u"".join(current)
				else:
					yield u"'%s'" % u"".join(current)
				current = []
	if current:
		if nchar:
			yield u"N'%s'" % u"".join(current)
		else:
			yield u"'%s'" % u"".join(current)


def xml2ora(string):
	"""
	The :class:`unicode` object :var:`string` must be an XML string.
	:func:`xml2ora` extracts the relevant processing instructions and creates
	the body of an Oracle function from it.
	"""
	foundproc = False
	foundargs = []
	foundvars = []
	foundplsql = []
	foundtype = u"clob"

	for (t, s) in misc.tokenizepi(string):
		if t is None:
			foundplsql.append((-1, s))
		elif t == "code":
			foundplsql.append((0, s))
		elif t == "expr":
			foundplsql.append((1, s))
		elif t == "args":
			foundargs.append(s)
		elif t == "vars":
			foundvars.append(s)
		elif t == "type":
			foundtype = s
		elif t == "proc":
			foundproc = True
		else:
			# Treat unknown PIs as text
			foundplsql.append((-1, u"<?%s %s?>" % (t, s)))

	result = []
	if foundargs:
		result.append(u"(\n\t%s\n)\n" % u",\n\t".join(foundargs))
	plaintype = foundtype
	if u"(" in plaintype:
		plaintype = plaintype[:plaintype.find(u"(")]
	isclob = plaintype.lower() in ("clob", "nclob")
	if not foundproc:
		result.append(u"return %s\n" % plaintype)
	result.append(u"as\n")
	if not foundproc:
		result.append(u"\tc_out %s;\n" % foundtype)
	if foundvars:
		result.append(u"\t%s\n" % u"".join(foundvars))
	nchar = foundtype.lower().startswith(u"n")
	if isclob:
		for arg in (u"clob", u"varchar2"):
			result.append(u"\tprocedure write(p_text in %s%s)\n" % (plaintype.rstrip(u"clob"), arg))
			result.append(u"\tas\n")
			result.append(u"\t\tbegin\n")
			if arg == u"clob":
				result.append(u"\t\t\tif p_text is not null and length(p_text) != 0 then\n")
				result.append(u"\t\t\t\tdbms_lob.append(c_out, p_text);\n")
			else:
				result.append(u"\t\t\tif p_text is not null then\n")
				result.append(u"\t\t\t\tdbms_lob.writeappend(c_out, length(p_text), p_text);\n")
			result.append(u"\t\tend if;\n")
			result.append(u"\tend;\n")
	result.append(u"begin\n")
	if isclob:
		result.append(u"\tdbms_lob.createtemporary(c_out, true);\n")
	for (mode, string) in foundplsql:
		if mode == -1:
			for s in stringify(string, nchar):
				if isclob:
					result.append(u"\twrite(%s);\n" % s)
				else:
					result.append(u"\tc_out := c_out || %s;\n" % s)
		elif mode == 0:
			result.append(string)
			result.append(u"\n")
		else: # mode == 1
			if isclob:
				result.append(u"\twrite(%s);\n" % string)
			else:
				result.append(u"\tc_out := c_out || %s;\n" % string)
	if not foundproc:
		result.append(u"\treturn c_out;\n")
	result.append(u"end;\n")
	return u"".join(result)


def prettify(string):
	"""
	Try to fix the indentation of the PL/SQL snippet passed in.
	"""
	lines = [line.lstrip("\t") for line in string.split("\n")]
	newlines = []
	indents = {
		"(": (0, 1),
		");": (-1, 0),
		")": (-1, 0),
		"as": (0, 1),
		"begin": (0, 1),
		"loop": (0, 1),
		"end;": (-1, 0),
		"end": (-1, 0),
		"exception": (-1, 1),
		"if": (0, 1),
		"for": (0, 1),
		"while": (0, 1),
		"elsif": (-1, 1),
		"else": (-1, 1),
	}
	indent = 0
	firstafteras = False
	for line in lines:
		if not line:
			newlines.append("")
		else:
			prefix = line.split(None, 1)[0]
			(pre, post) = indents.get(prefix, (0, 0))
			if line.endswith("("):
				post = 1
			elif firstafteras and prefix == "begin":
				# as followed by begin has same indentation
				pre = -1
			indent = max(0, indent+pre)
			newlines.append("%s%s" % ("\t"*indent, line))
			indent = max(0, indent+post)
			if prefix == "as":
				firstafteras = True
	return "\n".join(newlines)


class args(xsc.ProcInst):
	"""
	Specifies the arguments to be used by the generated function. For example::

		<?args
			key in integer,
			lang in varchar2
		?>

	If :class:`args` is used multiple times, the contents will simple be
	concatenated.
	"""


class vars(xsc.ProcInst):
	"""
	Specifies the local variables to be used by the function. For example::

		<?vars
			buffer varchar2(200) := 'foo';
			counter integer;
		?>

	If :class:`vars` is used multiple times, the contents will simple be
	concatenated.
	"""


class code(xsc.ProcInst):
	"""
	A PL/SQL code fragment that will be embedded literally in the generated
	function. For example::

		<?code select user into v_user from dual;?>
	"""


class expr(xsc.ProcInst):
	"""
	The data of an :class:`expr` processing instruction must contain a PL/SQL
	expression whose value will be embedded in the string returned by the
	generated function. This value will not be escaped in any way, so you can
	generate XML tags with :class:`expr` PIs but you must make sure to generate
	the value in the encoding that the caller of the generated function expects.
	"""


class proc(xsc.ProcInst):
	"""
	When this processing instruction is found in the source :func:`xml2ora` will
	not generate a function as a result, but a procedure. This procedure must
	have ``c_out`` as an "out" variable (of the appropriate type (see
	:class:`type`) where the output will be written to.
	"""


class type(xsc.ProcInst):
	"""
	Can be used to specify the return type of the generated function. The default
	is ``clob``.
	"""
