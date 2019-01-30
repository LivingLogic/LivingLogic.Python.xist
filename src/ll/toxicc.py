# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2004-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2004-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


'''
This module can be used for generating Oracle or SQL server functions that
return XML strings. This is done by embedding processing instructions containing
SQL code into XML files and transforming those files with XIST.

An Oracle example that generates an HTML table containing the result of a search
for names in a ``person`` table might look like this::

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

	print toxic.compile(search().conv().string(encoding"us-ascii")).encode("us-ascii")

The same example for SQL Server might look like this::

	from ll.xist import xsc
	from ll.xist.ns import html, htmlspecials
	from ll import toxic

	class search(xsc.Element):
		def convert(self, converter):
			e = xsc.Frag(
				toxic.args("@search varchar(100)"),
				toxic.vars("declare @i integer;"),
				toxic.type("varchar(max)"),
				htmlspecials.plaintable(
					toxic.code("""
						set @i = 1;

						declare @row_name varchar(100);
						declare person_cursor cursor for
							select name from person where name like @search

						open person_cursor

						while 1 = 1
						begin
							fetch next from person_cursor into @row_name;
							if (@@fetch_status != 0)
								break

							"""),
							html.tr(
								html.th(toxic.expr("@i"), align="right"),
								html.td(toxic.expr("schema.xmlescape(@row_name)"))
							),
							toxic.code("""
							set @i = @i+1;
						end

						close person_cursor
						deallocate person_cursor
					""")
				)
			)
			return e.convert(converter)

	print toxic.xml2sqs(search().conv().string(encoding"us-ascii")).encode("us-ascii")


Running the Oracle script will give the following output (the indentation will
be different though)::

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

	from ll.xist import parse
	from ll.xist.ns import html, htmlspecials
	from ll import toxic

	node = parse.tree(parse.File("search.sqlxsc"), parse.Expat(ns=True), parse.Node())
	node = node.conv()
	print toxic.xml2ora(node.string(encoding="us-ascii")).encode("us-ascii")
'''


from ll import misc


__docformat__ = "reStructuredText"


__all__ = ["compile", "prettify"]


def _stringifyoracle(string, nchar=False):
	"""
	Format :obj:`string` as multiple PL/SQL string constants or expressions.
	:obj:`nchar` specifies if a ``NVARCHAR`` constant should be generated or a
	``VARCHAR``. This is a generator.
	"""
	current = []

	for c in string:
		if ord(c) < 32:
			if current:
				current = "".join(current)
				if nchar:
					yield f"N'{current}'"
				else:
					yield f"'{current}'"
				current = []
			yield f"chr({ord(c)})"
		else:
			if c == "'":
				c = "''"
			current.append(c)
			if len(current) > 1000:
				current = "".join(current)
				if nchar:
					yield f"N'{current}'"
				else:
					yield f"'{current}'"
				current = []
	if current:
		current = "".join(current)
		if nchar:
			yield f"N'{current}'"
		else:
			yield f"'{current}'"


def _compile_oracle(string):
	"""
	TOXIC compile function for Oracle
	"""
	foundproc = False
	foundargs = []
	foundvars = []
	foundsql = []
	foundtype = "clob"

	for (t, s) in misc.tokenizepi(string):
		if t is None:
			foundsql.append((-1, s))
		elif t == "code":
			foundsql.append((0, s))
		elif t == "expr":
			foundsql.append((1, s))
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
			foundsql.append((-1, f"<?{t} {s}?>"))

	result = []
	if foundargs:
		foundargs = ",\n\t".join(foundargs)
		result.append(f"(\n\t{foundargs}\n)\n")
	plaintype = foundtype
	if "(" in plaintype:
		plaintype = plaintype[:plaintype.find("(")]
	isclob = plaintype.lower() in ("clob", "nclob")
	if not foundproc:
		result.append(f"return {plaintype}\n")
	result.append("as\n")
	if not foundproc:
		result.append(f"\tc_out {foundtype};\n")
	if foundvars:
		foundvars = "".join(foundvars)
		result.append("\t{foundvars}\n")
	nchar = foundtype.lower().startswith("n")
	if isclob:
		argtype = plaintype.rstrip("clob")
		for arg in ("clob", "varchar2"):
			result.append(f"\tprocedure write(p_text in {argtype}{arg})\n")
			result.append("\tas\n")
			result.append("\t\tbegin\n")
			if arg == "clob":
				result.append("\t\t\tif p_text is not null and length(p_text) != 0 then\n")
				result.append("\t\t\t\tdbms_lob.append(c_out, p_text);\n")
			else:
				result.append("\t\t\tif p_text is not null then\n")
				result.append("\t\t\t\tdbms_lob.writeappend(c_out, length(p_text), p_text);\n")
			result.append("\t\tend if;\n")
			result.append("\tend;\n")
	result.append("begin\n")
	if isclob:
		result.append("\tdbms_lob.createtemporary(c_out, true);\n")
	for (mode, string) in foundsql:
		if mode == -1:
			for s in _stringifyoracle(string, nchar):
				if isclob:
					result.append(f"\twrite({s});\n")
				else:
					result.append(f"\tc_out := c_out || {s};\n")
		elif mode == 0:
			result.append(string)
			result.append("\n")
		else: # mode == 1
			if isclob:
				result.append(f"\twrite({string});\n")
			else:
				result.append(f"\tc_out := c_out || {string};\n")
	if not foundproc:
		result.append("\treturn c_out;\n")
	result.append("end;\n")
	return "".join(result)


def _compile_sqlserver(string):
	"""
	TOXIC compile function for SQL Server
	"""
	foundproc = False
	foundargs = []
	foundvars = []
	foundsql = []
	foundtype = "varchar(max)"

	for (t, s) in misc.tokenizepi(string):
		if t is None:
			foundsql.append((-1, s))
		elif t == "code":
			foundsql.append((0, s))
		elif t == "expr":
			foundsql.append((1, s))
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
			foundsql.append((-1, f"<?{t} {s}?>"))

	result = []
	if foundargs:
		foundargs = ",\n\t".join(foundargs)
		result.append(f"(\n\t{foundargs}\n)\n")
	if not foundproc:
		result.append(f"returns {foundtype}\n")
	result.append("as\n")
	result.append("begin\n")
	if not foundproc:
		result.append(f"\tdeclare @c_out {foundtype};\n")
		result.append("\tset @c_out = '';\n")
	if foundvars:
		foundvars = "".join(foundvars)
		result.append(f"\t{foundvars}\n")
	for (mode, string) in foundsql:
		if mode == -1:
			string = string.replace("'", "''")
			string = f"'{string}'"
			result.append(f"\tset @c_out = @c_out + {string};\n")
		elif mode == 0:
			result.append(string)
			result.append("\n")
		else: # mode == 1
			result.append(f"\tset @c_out = @c_out + set @c_out = @c_out + convert(varchar, isnull({string}, ''));\n")
	if not foundproc:
		result.append("\treturn @c_out;\n")
	result.append("end;\n")
	return "".join(result)


def compile(string, mode="oracle"):
	"""
	The :class:`str` object :obj:`string` must be a string containing embedded
	TOXIC processing instructions. :func:`compile` creates the body of an Oracle
	or SQL Server function or procedure from it. :obj:`mode` can be either
	``"oracle"`` or ``"sqlserver".
	"""
	if mode == "oracle":
		return _compile_oracle(string)
	elif mode == "sqlserver":
		return _compile_sqlserver(string)
	raise ValueError(f"unknown mode {mode!r}")


def prettify(string, mode="oracle"):
	"""
	Try to fix the indentation of the PL/SQL snippet passed in. :obj:`mode` can
	be either ``"oracle"`` or ``"sqlserver"``.
	"""
	lines = [line.lstrip() for line in string.splitlines()]
	newlines = []
	if mode == "oracle":
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
	elif mode == "sqlserver":
		indents = {
			"(": (0, 1),
			");": (-1, 0),
			")": (-1, 0),
			"as": (0, 1),
			"begin": (0, 1),
			"end;": (-1, 0),
			"end": (-1, 0),
		}
	else:
		raise ValueError(f"unknown mode {mode!r}")
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
			newlines.append("\t"*indent + line)
			indent = max(0, indent+post)
			if prefix == "as":
				firstafteras = True
	return "\n".join(newlines)
