#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3

## Copyright 2014 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2014 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import io, os
from test import support

import pytest

from ll import orasql, oradd


dbname = os.environ.get("LL_ORASQL_TEST_CONNECT") # Need a connectstring as environment var


def commands():
	yield dict(
		type="sql",
		sql="""
		begin
			execute immediate 'drop table oradd_test_table';
		exception when others then
			if sqlcode != -0942 then
				raise;
			end if;
		end;
		"""
	)

	yield dict(
		type="sql",
		sql="""
		create table oradd_test_table(
			odtt_id integer
		)
		"""
	)

	yield dict(
		type="sql",
		sql="""
		create or replace procedure oradd_test_procedure(
			p_odtt_id in out integer
		)
		as
		begin
			if p_odtt_id is null then
				p_odtt_id := 1;
			end if;
			insert into oradd_test_table (odtt_id) values (p_odtt_id);
			p_odtt_id := p_odtt_id + 100;
		end;
		"""
	)

	yield dict(
		type="procedure",
		name="oradd_test_procedure",
		args=dict(
			p_odtt_id=oradd.var("odtt_1"),
		)
	)

	yield dict(
		type="procedure",
		name="oradd_test_procedure",
		args=dict(
			p_odtt_id=oradd.var("odtt_1"),
		)
	)


def execute_commands(commands):
	s = io.StringIO()

	for command in commands:
		print(repr(command), file=s)

	with support.captured_stdin() as stdin:
		print(s.getvalue())
		stdin.write(s.getvalue())
		oradd.main([dbname, "-v3"])


@pytest.mark.db
def test_oradd():
	execute_commands(commands())

	db = orasql.connect(dbname)
	c = db.cursor()
	c.execute("select odtt_id from oradd_test_table order by odtt_id")
	data = [int(r.odtt_id) for r in c]
	assert data == [1, 101]
