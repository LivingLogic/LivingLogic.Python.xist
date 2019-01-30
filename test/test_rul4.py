#! /usr/bin/env/python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2014-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2014-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import os

from ll import ul4c, orasql
from ll.scripts import rul4

import pytest


@pytest.fixture(scope="module")
def globals(request):
	"""
	Return a ``rul4.Globals`` object with one defined variable: ``connectstring``
	which will be the value of the environment variable ``LL_ORASQL_TEST_CONNECT``.

	This can be used to create a database connection like this::

		<?code db = globals.oracle(globals.vars.connectstring)?>

	If ``LL_ORASQL_TEST_CONNECT`` is not set ``None`` will be returned instead.
	"""
	connectstring = os.environ.get("LL_ORASQL_TEST_CONNECT")
	if connectstring:
		return rul4.Globals(vars={"connectstring": connectstring})
	else:
		return None


@pytest.mark.db
def test_oracle_query(globals):
	if globals:
		template = ul4c.Template("""
			<?code db = globals.oracle(globals.vars.connectstring)?>
			<?code db.execute('''
				create table ul4test(
					ul4_int integer,
					ul4_char varchar2(1000),
					ul4_clob clob)
			''')?>
			<?code db.execute('insert into ul4test values(1, ', 'first', ', ', 10000*'first', ')')?>
			<?code db.execute('insert into ul4test values(2, ', 'second', ', ', 10000*'second', ')')?>
			<?code db.execute('insert into ul4test values(3, ', 'third', ', ', 10000*'third', ')')?>
			<?code vin = db.int(2)?>
			<?for row in db.query('select * from ul4test where ul4_int <= ', vin, ' order by ul4_int')?>
				<?print row.ul4_int?>|
				<?print row.ul4_char?>|
				<?print row.ul4_clob?>|
			<?end for?>
			<?code db.execute('drop table ul4test')?>
			""",
			whitespace="strip"
		)
		assert template.renders(globals=globals) == f"1|first|{10000*'first'}|2|second|{10000*'second'}|"


@pytest.mark.db
def test_oracle_execute_function(globals):
	if globals:
		template = ul4c.Template("""
			<?code db = globals.oracle(globals.vars.connectstring)?>
			<?code db.execute('''
				create or replace function ul4test(p_arg integer)
				return integer
				as
				begin
					return 2*p_arg;
				end;
			''')?>
			<?code vin = db.int(42)?>
			<?code vout = db.int()?>
			<?code db.execute('begin ', vout, ' := ul4test(', vin, '); end;')?>
			<?print vout.value?>
			<?code db.execute('drop function ul4test')?>
			""",
			whitespace="strip"
		)
		assert template.renders(globals=globals) == "84"


@pytest.mark.db
def test_oracle_execute_procedure_out(globals):
	if globals:
		template = ul4c.Template("""
			<?code db = globals.oracle(globals.vars.connectstring)?>
			<?code db.execute('''
				create or replace procedure ul4test(p_intarg out integer, p_numberarg out number, p_strarg out varchar2, p_clobarg out clob, p_datearg out timestamp)
				as
				begin
					p_intarg := 42;
					p_numberarg := 42.5;
					p_strarg := 'foo';
					dbms_lob.createtemporary(p_clobarg, true);
					for i in 1..100000 loop
						dbms_lob.writeappend(p_clobarg, 3, 'foo');
					end loop;
					p_datearg := to_date('05.10.2014 16:17:18', 'DD.MM.YYYY HH24:MI:SS');
				end;
			''')?>
			<?code vint = db.int()?>
			<?code vnumber = db.number()?>
			<?code vstr = db.str()?>
			<?code vclob = db.clob()?>
			<?code vdate = db.date()?>
			<?code db.execute('call ul4test(', vint, ', ', vnumber, ', ', vstr, ', ', vclob, ', ', vdate, ')')?>
			<?print vint.value?>|<?print vnumber.value?>|<?print vstr.value?>|<?print vclob.value?>|<?print vdate.value?>
			<?code db.execute('drop procedure ul4test')?>
			""",
			whitespace="strip"
		)
		assert template.renders(globals=globals) == f"42|42.5|foo|{100000*'foo'}|2014-10-05 16:17:18"
