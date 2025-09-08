import os, datetime

from ll import orasql

import pytest

from ll import vsql

dbname = os.environ.get("LL_ORASQL_TEST_CONNECT") # Need a connectstring as environment var


###
### Definition of vSQL records and tables
###

vsql_group = vsql.Group("vsql_test")
vsql_group.add_field("identifier", vsql.DataType.STR, "{a}.vs_identifier")
vsql_group.add_field("v_bool", vsql.DataType.BOOL, "{a}.vs_bool")
vsql_group.add_field("v_int", vsql.DataType.INT, "{a}.vs_int")
vsql_group.add_field("v_number", vsql.DataType.NUMBER, "{a}.vs_number")
vsql_group.add_field("v_str", vsql.DataType.STR, "{a}.vs_str")
vsql_group.add_field("v_clob", vsql.DataType.CLOB, "{a}.vs_clob")
vsql_group.add_field("v_date", vsql.DataType.DATE, "{a}.vs_date")
vsql_group.add_field("v_datetime", vsql.DataType.DATETIME, "{a}.vs_datetime")
vsql_group.add_field("v_datedelta", vsql.DataType.DATEDELTA, "{a}.vs_int")
vsql_group.add_field("v_datetimedelta", vsql.DataType.DATETIMEDELTA, "{a}.vs_number")
vsql_group.add_field("v_monthdelta", vsql.DataType.MONTHDELTA, "{a}.vs_int")


vsql_r = vsql.Field(
	"r",
	vsql.DataType.STR,
	"?",
	"1 = 1",
	vsql_group,
)


###
### Helder functions
###

def expr(db, vsqlexpr, *, where=None):
	query = vsql.Query(r=vsql_r)
	query.select_vsql(vsqlexpr)
	if where:
		query.where_vsql(where)
	rs = execute(db, query)
	assert len(rs) == 1
	result = rs[0][0]
	if isinstance(result, orasql.DbObject):
		result = result.aslist()
	return result


def execute(db, query):
	return db.cursor().execute(query.sqlsource()).fetchall()


def make_record(db, **kwargs):
	query = f"insert into vsql_test ({', '.join(kwargs)}) values ({', '.join(f':{k}' for k in kwargs)})"
	db.cursor().execute(query, **kwargs)


###
### ``pytest`` test fixtures
###

@pytest.fixture
def db():
	db = orasql.connect(dbname, readlobs=True)
	return db


def setup_vsql_data(db):
	c = db.cursor()
	try:
		c.execute("drop table vsql_test")
	except Exception:
		pass
	c.execute("""
		create table vsql_test
		(
			vs_identifier varchar2(100),
			vs_bool integer,
			vs_int integer,
			vs_number number,
			vs_str varchar2(4000),
			vs_clob clob,
			vs_date date,
			vs_datetime date
		)
	""")
	make_record(db, vs_identifier="none")
	make_record(db, vs_identifier="bool_false", vs_bool=0)
	make_record(db, vs_identifier="bool_true", vs_bool=1)
	make_record(db, vs_identifier="date", vs_date=datetime.date(2000, 2, 29))
	make_record(db, vs_identifier="datetime", vs_datetime=datetime.datetime(2000, 2, 29, 12, 34, 56))
	make_record(db, vs_identifier="str", vs_str="gurk")
	make_record(db, vs_identifier="int", vs_int=1776)
	make_record(db, vs_identifier="number", vs_number=42.5)
	make_record(db, vs_identifier="datedelta", vs_int=12)
	make_record(db, vs_identifier="datetimedelta", vs_number=1.0 + 12/24 + 34/24/60 + 56/24/60/60)
	make_record(db, vs_identifier="monthdelta", vs_int=3)
	db.commit()


@pytest.fixture
def vsql_data(db, tmp_path_factory, worker_id):
	"""
	A test fixture that sets up the database for testing vSQL
	"""

	# This uses the logic documented here:
	# https://pytest-xdist.readthedocs.io/en/latest/how-to.html#making-session-scoped-fixtures-execute-only-once
	# to support running under ``pytest-xdist``

	if worker_id == "master":
		setup_vsql_data(db)
		return db

	# get the temp directory shared by all workers
	root_tmp_dir = tmp_path_factory.getbasetemp().parent

	# File that signals that test data has been created in the database
	fn = root_tmp_dir / "init.dummy"

	# Lock file for prevention concurrent checks
	ln = root_tmp_dir / "init.lock"

	with filelock.FileLock(ln):
		if not fn.is_file():
			# Create test data
			setup_vsql_data(db)
			# Record that test data has been created
			fn.write_text("done")
	return db
