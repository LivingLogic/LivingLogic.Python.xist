#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2014 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2014 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import io, os, tempfile

import cx_Oracle

import pytest

from ll import orasql, oradd


dbname = os.environ.get("LL_ORASQL_TEST_CONNECT") # Need a connectstring as environment var


def commands():
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

	with tempfile.NamedTemporaryFile(delete=False) as f:
		print(s.getvalue())
		f.write(s.getvalue().encode("utf-8"))
		tempname = f.name

	try:
		oradd.main([dbname, tempname, "-v3"])
	finally:
		os.remove(tempname)


def droptable():
	with orasql.connect(dbname) as db:
		c = db.cursor()
		try:
			c.execute("drop table oradd_test_table")
		except cx_Oracle.DatabaseError:
			pass


@pytest.mark.db
def test_oradd():
	droptable()

	execute_commands(commands())

	with orasql.connect(dbname) as db:
		c = db.cursor()
		c.execute("select odtt_id from oradd_test_table order by odtt_id")
		data = [int(r.odtt_id) for r in c]
		assert data == [1, 101]

	droptable()
