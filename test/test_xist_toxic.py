#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2009-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


from ll import toxicc
from ll.xist import xsc
from ll.xist.ns import html, htmlspecials, toxic


def oraclecode():
	return xsc.Frag(
		toxic.args("search in varchar2"),
		toxic.vars("i integer;"),
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


def test_oracle_clobfunc():
	e = oraclecode()
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl)
	assert "dbms_lob.createtemporary" in sql
	assert "procedure write" in sql
	assert "return clob\n" in sql


def test_oracle_varcharfunc():
	e = xsc.Frag(
		toxic.type("varchar2(20000)"),
		oraclecode(),
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl)
	assert "dbms_lob.createtemporary" not in sql
	assert "procedure write" not in sql
	assert "c_out := c_out ||" in sql
	assert "return varchar2\n" in sql


def test_oracle_clobproc():
	e = xsc.Frag(
		toxic.proc(),
		toxic.args("c_out out clob"),
		oraclecode()
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl)
	print(sql)
	assert "dbms_lob.createtemporary" in sql
	assert "procedure write" in sql
	assert "c_out out clob" in sql


def test_oracle_varcharproc():
	e = xsc.Frag(
		toxic.proc(),
		toxic.type("varchar2(20000)"),
		toxic.args("c_out out varchar2(20000)"),
		oraclecode(),
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl)
	assert "dbms_lob.createtemporary" not in sql
	assert "procedure write" not in sql
	assert "c_out := c_out ||" in sql
	assert "c_out out varchar2(20000)" in sql


def sqlservercode():
	return xsc.Frag(
		toxic.args("@search varchar(100)"),
		toxic.vars("declare @i integer;"),
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


def test_sqlserver_clobfunc():
	e = sqlservercode()
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl, mode="sqlserver")
	assert "declare @c_out varchar(max)" in sql
	assert "returns varchar(max)\n" in sql
	assert "set @c_out = @c_out +" in sql


def test_sqlserver_varcharfunc():
	e = xsc.Frag(
		toxic.type("varchar(20000)"),
		sqlservercode(),
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl, mode="sqlserver")
	assert "declare @c_out varchar(20000)" in sql
	assert "returns varchar(20000)\n" in sql
	assert "set @c_out = @c_out +" in sql


def test_sqlserver_clobproc():
	e = xsc.Frag(
		toxic.proc(),
		toxic.args("@c_out varchar(max) output"),
		sqlservercode(),
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl, mode="sqlserver")
	assert "@c_out varchar(max) output" in sql
	assert "set @c_out = @c_out +" in sql


def test_sqlserver_varcharproc():
	e = xsc.Frag(
		toxic.proc(),
		toxic.type("varchar(20000)"),
		toxic.args("@c_out varchar(20000) output"),
		sqlservercode(),
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl, mode="sqlserver")
	assert "c_out varchar(20000) output" in sql
	assert "set @c_out = @c_out +" in sql
