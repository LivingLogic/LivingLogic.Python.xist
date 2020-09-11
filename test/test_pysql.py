#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2014-2020 by LivingLogic AG, Bayreuth/Germany
## Copyright 2014-2020 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import os, tempfile

import cx_Oracle

import pytest

from ll import orasql, pysql


connectstring_oracle = os.environ.get("LL_ORASQL_TEST_CONNECT") # Need a connectstring as environment var


commands = """

# Connect to the Oracle database

connect(connectstring_oracle)

# Create our test table which we will fill with test data.

create table pysql_test_table(
	tt_id integer,
	tt_int integer,
	tt_number number,
	tt_str varchar2(4000),
	tt_clob clob,
	tt_datetime date,
	tt_cdate timestamp
);

-- @@@@

# Disconnect again

disconnect()

-- @@@

# Connect again (this time using the ``oracle:`` "schema" prefix

connect("oracle:" + connectstring_oracle)

# Create test procedure which we'll use to populate the table
# (and test procedure calling)

create or replace procedure pysql_test_procedure(
	p_tt_id in out integer,
	p_tt_int integer := null,
	p_tt_number number := null,
	p_tt_str varchar2 := null,
	p_tt_clob clob := null,
	p_tt_datetime date := null
)
as
begin
	if p_tt_id is null then
		p_tt_id := 1;
	end if;
	insert into pysql_test_table
	(
		tt_id,
		tt_int,
		tt_number,
		tt_str,
		tt_clob,
		tt_datetime,
		tt_cdate
	)
	values
	(
		p_tt_id,
		p_tt_int,
		p_tt_number,
		p_tt_str,
		p_tt_clob,
		p_tt_datetime,
		systimestamp
	);
	p_tt_id := p_tt_id + 100;
end;
/

-- @@@

# Create sequence (but this time via the ``sql`` command
# specified via dictionary).

{
	"type": "sql",
	"sql":
		"create sequence pysql_test_sequence"
		"	minvalue 10"
		"	maxvalue 9999999999999999999999999999"
		"	start with 30"
		"	increment by 10"
		"	cache 20",
}

# Call ``pysql_test_procedure`` the first time (and remember the value of the
# OUT parameter).

procedure(
	"pysql_test_procedure",
	args=dict(
		p_tt_id=var("tt_1"),
	),
)

# Call ``pysql_test_procedure`` the second time (and pass the resulting value
# for ``p_tt_id`` from the last call).

procedure(
	"pysql_test_procedure",
	args=dict(
		p_tt_id=var("tt_1"),
	)
)

reset_sequence(
	"pysql_test_sequence",
	table="pysql_test_table",
	field="tt_id",
)

sql(
	"begin :filename_file := 'gurk_file.txt'; end;",
	args=dict(
		filename_file=var("filename_file", str),
	),
)

object_exists(
	"pysql_test_procedure"
)

constraint_exists(
	"doesnt_exist"
)

{
	"type": "sql",
	"sql": "begin :filename_scp := 'gurk_scp.txt'; end;",
	"args": {
		"filename_scp": var("filename_scp", str),
	}
}

{
	"type": "file",
	"name": "{filename_file}",
	"content": b"gurk_file",
	"mode": 0o644,
}

{
	"type": "scp",
	"name": "{filename_scp}",
	"content": b"gurk_scp",
}

procedure(
	"doesnt_exist",
	cond=False,
)

reset_sequence(
	"doesnt_exist",
	table="doesnt_exist",
	field="de_id",
	cond=False,
)

sql(
	"begin doesnt_exist; end;",
	cond=False,
)

file(
	name="doesnt_exist",
	content=b"nothing",
	cond=False,
)

scp(
	name="doesnt_exist",
	content=b"nothing",
	cond=False,
)

disconnect()
"""


def execute_commands(commands, tmpdir):
	with tempfile.NamedTemporaryFile(delete=False) as f:
		tempname = f.name
		f.write(commands.encode("utf-8"))

	try:
		pysql.main([
			tempname,
			"-d", connectstring_oracle,
			"-D", f"connectstring_oracle={connectstring_oracle}",
			"-vfull",
			"-z",
			"--tabsize=3",
			"--context=10",
			"--scpdirectory", tmpdir,
			"--filedirectory", tmpdir
		])
	finally:
		os.remove(tempname)


def cleanup():
	commands = [
		"drop table pysql_test_table",
		"drop sequence pysql_test_sequence",
		"drop procedure pysql_test_procedure",
	]
	with orasql.connect(connectstring_oracle) as db:
		c = db.cursor()
		for command in commands:
			try:
				c.execute(command)
			except cx_Oracle.DatabaseError:
				pass


@pytest.mark.db
def test_pysql(tmpdir):
	cleanup()

	execute_commands(commands, f"{tmpdir}/")

	with orasql.connect(connectstring_oracle) as db:
		c = db.cursor()
		c.execute("select tt_id from pysql_test_table order by tt_cdate")
		data = [int(r.tt_id) for r in c]
		assert data == [1, 101]
		c.execute("select pysql_test_sequence.nextval as nv from dual")
		data = c.fetchone().nv
		assert data == 111

	f = tmpdir.join("gurk_file.txt")
	assert f.read() == "gurk_file"
	stat = os.stat(str(f))
	assert stat.st_mode & 0o777 == 0o644

	f2 = tmpdir.join("gurk_scp.txt")
	assert f2.read() == "gurk_scp"

	cleanup()
