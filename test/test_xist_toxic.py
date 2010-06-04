#! /usr/bin/env/python
# -*- coding: utf-8 -*-

## Copyright 2009-2010 by LivingLogic AG, Bayreuth/Germany
## Copyright 2009-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


from ll import toxicc
from ll.xist import xsc
from ll.xist.ns import html, htmlspecials, toxic


def oraclecode():
	return xsc.Frag(
		toxic.args(u"search in varchar2"),
		toxic.vars(u"i integer;"),
		htmlspecials.plaintable(
			toxic.code(u"""
				i := 1;
				for row in (select name from person where name like search) loop
					"""),
					html.tr(
						html.th(toxic.expr(u"i"), align=u"right"),
						html.td(toxic.expr(u"xmlescape(row.name)"))
					),
					toxic.code(u"""
					i := i+1;
				end loop;
			""")
		)
	)


def test_oracle_clobfunc():
	e = oraclecode()
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl)
	assert u"dbms_lob.createtemporary" in sql
	assert u"procedure write" in sql
	assert u"return clob\n" in sql


def test_oracle_varcharfunc():
	e = xsc.Frag(
		toxic.type(u"varchar2(20000)"),
		oraclecode(),
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl)
	assert u"dbms_lob.createtemporary" not in sql
	assert u"procedure write" not in sql
	assert u"c_out := c_out ||" in sql
	assert u"return varchar2\n" in sql


def test_oracle_clobproc():
	e = xsc.Frag(
		toxic.proc(),
		toxic.args(u"c_out out clob"),
		oraclecode()
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl)
	print sql
	assert u"dbms_lob.createtemporary" in sql
	assert u"procedure write" in sql
	assert u"c_out out clob" in sql


def test_oracle_varcharproc():
	e = xsc.Frag(
		toxic.proc(),
		toxic.type(u"varchar2(20000)"),
		toxic.args(u"c_out out varchar2(20000)"),
		oraclecode(),
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl)
	assert u"dbms_lob.createtemporary" not in sql
	assert u"procedure write" not in sql
	assert u"c_out := c_out ||" in sql
	assert u"c_out out varchar2(20000)" in sql


def sqlservercode():
	return xsc.Frag(
		toxic.args(u"@search varchar(100)"),
		toxic.vars(u"declare @i integer;"),
		htmlspecials.plaintable(
			toxic.code(u"""
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
						html.th(toxic.expr(u"@i"), align=u"right"),
						html.td(toxic.expr(u"schema.xmlescape(@row_name)"))
					),
					toxic.code(u"""
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
	assert u"declare @c_out varchar(max)" in sql
	assert u"returns varchar(max)\n" in sql
	assert u"set @c_out = @c_out +" in sql


def test_sqlserver_varcharfunc():
	e = xsc.Frag(
		toxic.type(u"varchar(20000)"),
		sqlservercode(),
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl, mode="sqlserver")
	assert u"declare @c_out varchar(20000)" in sql
	assert u"returns varchar(20000)\n" in sql
	assert u"set @c_out = @c_out +" in sql


def test_sqlserver_clobproc():
	e = xsc.Frag(
		toxic.proc(),
		toxic.args(u"@c_out varchar(max) output"),
		sqlservercode(),
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl, mode="sqlserver")
	assert u"@c_out varchar(max) output" in sql
	assert u"set @c_out = @c_out +" in sql


def test_sqlserver_varcharproc():
	e = xsc.Frag(
		toxic.proc(),
		toxic.type(u"varchar(20000)"),
		toxic.args(u"@c_out varchar(20000) output"),
		sqlservercode(),
	)
	tmpl = e.conv().string(encoding="ascii")

	sql = toxicc.compile(tmpl, mode="sqlserver")
	assert u"c_out varchar(20000) output" in sql
	assert u"set @c_out = @c_out +" in sql
