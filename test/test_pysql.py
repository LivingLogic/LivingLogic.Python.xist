#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2014-2020 by LivingLogic AG, Bayreuth/Germany
## Copyright 2014-2020 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import os, tempfile, datetime, json

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
	tt_blob blob,
	tt_datetime date,
	tt_cdate timestamp
);

-- @@@@

alter table pysql_test_table add constraint pysql_test_table_pk primary key(tt_id);

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
	p_tt_blob blob := null,
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
		tt_blob,
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
		p_tt_blob,
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
		p_tt_id=var("tt_id_1"),
		p_tt_int=42,
		p_tt_number=42.5,
		p_tt_str="ä"*2000, # 4000 would lead to 8000 UTF-8 bytes, which doesn't work
		p_tt_clob="ä"*100000,
		p_tt_blob=b"\\xff"*100000,
		p_tt_datetime=datetime.datetime(2000, 2, 29, 12, 34, 56),
	),
)

# Call ``pysql_test_procedure`` the second time (and pass the resulting value
# for ``p_tt_id`` from the last call).

procedure(
	"pysql_test_procedure",
	args=dict(
		p_tt_id=var("tt_id_1"),
		p_tt_int=None,
		p_tt_number=None,
		p_tt_str=None,
		p_tt_clob=var(None, DB_TYPE_CLOB),
		p_tt_blob=var(None, DB_TYPE_BLOB),
		p_tt_datetime=None,
	)
)

# Reset sequence ``pysql_test_sequence`` to maximum ``tt_id``.

reset_sequence(
	"pysql_test_sequence",
	table="pysql_test_table",
	field="tt_id",
)

# Fetch next sequence value

sql(
	'''
		begin
			select pysql_test_sequence.nextval into :tt_id_seq from dual;
		end;
	''',
	args=dict(
		tt_id_seq=var("tt_id_seq"),
	),
)

# Call ``pysql_test_procedure`` a third time to record the result of the
# ``reset_sequence`` call.

procedure(
	"pysql_test_procedure",
	args=dict(
		p_tt_id=var("tt_id_seq"),
	)
)

sql(
	"begin :filename_file := 'gurk_file.txt'; end;",
	args=dict(
		filename_file=var("filename_file", str),
	),
)

sql(
	"begin :user_name := user; end;",
	args=dict(
		user_name=var("user_name", str),
	),
)

#>>>
import json
#<<<

# Call ``pysql_test_procedure`` again to record the results of various
# ``..._exists`` calls.

procedure(
	"pysql_test_procedure",
	args=dict(
		p_tt_id=var("tt_id_seq"),
		p_tt_str=json.dumps(
			{
				"PROCEDURE": object_exists("PYSQL_TEST_PROCEDURE"),
				"NOPROCEDURE": object_exists("DOESNT_EXIST"),
				"USER": user_exists(user_name),
				"NOUSER": user_exists("DOESNT_EXIST"),
				"SCHEMA": schema_exists(user_name),
				"NOSCHEMA": schema_exists("DOESNT_EXIST"),
				"PK": constraint_exists("PYSQL_TEST_TABLE_PK"),
				"NOPK": constraint_exists("DOESNT_EXIST"),
			}
		)
	)
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

	with orasql.connect(connectstring_oracle, readlobs=True) as db:
		c = db.cursor()
		c.execute("select * from pysql_test_table order by tt_cdate")
		data = c.fetchall()

		# Test first record
		assert data[0].tt_id == 1
		assert data[0].tt_int == 42
		assert data[0].tt_number == 42.5
		assert data[0].tt_str == "ä"*2000
		assert data[0].tt_clob == "ä"*100000
		assert data[0].tt_blob == b"\xff"*100000
		assert data[0].tt_datetime == datetime.datetime(2000, 2, 29, 12, 34, 56)

		# Test second record
		assert data[1].tt_id == 101
		assert data[1].tt_int is None
		assert data[1].tt_number is None
		assert data[1].tt_str is None
		assert data[1].tt_clob is None
		assert data[1].tt_blob is None
		assert data[1].tt_datetime is None

		# Test third record
		assert data[2].tt_id == 111
		assert data[2].tt_int is None
		assert data[2].tt_number is None
		assert data[2].tt_str is None
		assert data[2].tt_clob is None
		assert data[2].tt_blob is None
		assert data[2].tt_datetime is None

		# Test fourth record
		assert data[3].tt_id == 211
		got = data[3].tt_str
		got = json.loads(got)
		expect = dict(
			PROCEDURE=True,
			NOPROCEDURE=False,
			USER=True,
			NOUSER=False,
			SCHEMA=True,
			NOSCHEMA=False,
			PK=True,
			NOPK=False,
		)
		assert got == expect

	f = tmpdir.join("gurk_file.txt")
	assert f.read() == "gurk_file"
	stat = os.stat(str(f))
	assert stat.st_mode & 0o777 == 0o644

	f2 = tmpdir.join("gurk_scp.txt")
	assert f2.read() == "gurk_scp"

	cleanup()
