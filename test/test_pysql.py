#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2014-2020 by LivingLogic AG, Bayreuth/Germany
## Copyright 2014-2020 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import os, datetime, json, pathlib

import cx_Oracle

import pytest

from ll import orasql, pysql


basedir = pathlib.Path(__file__).parent

connectstring_oracle = os.environ["LL_ORASQL_TEST_CONNECT"] # Need a connectstring as environment var
connectstring_postgres = os.environ["LL_POSTSQL_TEST_CONNECT"] # Need a connectstring as environment var


def execute_commands(tmpdir):
	pysql.main([
		str(basedir/"pysql/main.pysql"),
		"-d", connectstring_oracle,
		"-D", f"connectstring_oracle={connectstring_oracle}",
		"-D", f"connectstring_postgres={connectstring_postgres}",
		"-vfull",
		"-z",
		"--tabsize=3",
		"--context=10",
		"--scpdirectory", f"{tmpdir}/",
		"--filedirectory", f"{tmpdir}/"
	])


@pytest.mark.db
def test_pysql(tmpdir):
	execute_commands(tmpdir)
	tmpdir = pathlib.Path(tmpdir)

	with orasql.connect(connectstring_oracle, readlobs=True) as db:
		c = db.cursor()
		c.execute("select * from pysql_test_table order by tt_cdate")
		rows = c.fetchall()

		for r in rows:
			if r.tt_identifier == "full":
				assert r.tt_int == 42
				assert r.tt_number == 42.5
				assert r.tt_str == "ä"*2000
				assert r.tt_clob == "ä"*100000
				assert r.tt_blob == b"\xff"*100000
				assert r.tt_datetime == datetime.datetime(2000, 2, 29, 12, 34, 56)
			elif r.tt_identifier == "outcheck":
				assert r.tt_int == 101
			elif r.tt_identifier == "empty":
				assert r.tt_int is None
				assert r.tt_number is None
				assert r.tt_str is None
				assert r.tt_clob is None
				assert r.tt_blob is None
				assert r.tt_datetime is None
			elif r.tt_identifier == "noparams":
				assert r.tt_int is None
				assert r.tt_number is None
				assert r.tt_str is None
				assert r.tt_clob is None
				assert r.tt_blob is None
				assert r.tt_datetime is None
			elif r.tt_identifier == "schemacheck":
				got = r.tt_str
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
			else:
				pytest.fail(f"tt_identifier {r.tt_identifier!r} unknown")

	f = tmpdir/"gurk_file.txt"
	assert f.read_text() == "gurk_file"
	stat = os.stat(str(f))
	assert stat.st_mode & 0o777 == 0o644

	f2 = tmpdir/"gurk_scp.txt"
	assert f2.read_text() == "gurk_scp"
