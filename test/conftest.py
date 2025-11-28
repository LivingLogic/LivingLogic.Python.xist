import os, datetime, filelock

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
vsql_group.add_field("v_color", vsql.DataType.COLOR, "{a}.vs_int")


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

def extract_result(value):
	if isinstance(value, orasql.DbObject):
		value = [extract_result(item) for item in value.aslist()]
	elif isinstance(value, orasql.LOB):
		value = value.read()
	return value


def expr(db, vsqlexpr, *, where=None):
	query = vsql.Query(r=vsql_r)
	query.select_vsql(vsqlexpr)
	if where:
		query.where_vsql(where)
	rs = execute(db, query)
	assert len(rs) == 1
	return extract_result(rs[0][0])


def execute(db, query):
	sql = query.sqlsource()
	print(f"Executing query:\n{sql}")
	return db.cursor().execute(sql).fetchall()


def make_record(db, table, **kwargs):
	query = f"insert into {table} ({', '.join(kwargs)}) values ({', '.join(f':{k}' for k in kwargs)})"
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

	try:
		c.execute("drop table vsql_field")
	except Exception:
		pass

	try:
		c.execute("drop table vsql_person")
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

	c.execute("""
		create table vsql_field
		(
			fld_id varchar2(16),
			fld_name varchar2(200),
			fld_id_super varchar2(8)
		)
	""")

	c.execute("""
		create table vsql_person
		(
			per_id varchar2(16),
			per_firstname varchar2(200),
			per_lastname varchar2(200),
			per_gender varchar2(2),
			fld_id varchar2(16),
			per_date_of_birth date,
			per_date_of_death date,
			per_country_of_birth varchar2(200),
			per_grave varchar2(500),
			per_nobel_prize integer,
			per_url varchar2(200),
			per_createdat date
		)
	""")
	make_record(db, "vsql_test", vs_identifier="none")
	make_record(db, "vsql_test", vs_identifier="bool_false", vs_bool=0)
	make_record(db, "vsql_test", vs_identifier="bool_true", vs_bool=1)
	make_record(db, "vsql_test", vs_identifier="date", vs_date=datetime.date(2000, 2, 29))
	make_record(db, "vsql_test", vs_identifier="datetime", vs_datetime=datetime.datetime(2000, 2, 29, 12, 34, 56))
	make_record(db, "vsql_test", vs_identifier="str", vs_str="gurk")
	make_record(db, "vsql_test", vs_identifier="clob", vs_clob="gurk"*100000)
	make_record(db, "vsql_test", vs_identifier="shortclob", vs_clob="gurk")
	make_record(db, "vsql_test", vs_identifier="int", vs_int=1776)
	make_record(db, "vsql_test", vs_identifier="number", vs_number=42.5)
	make_record(db, "vsql_test", vs_identifier="datedelta", vs_int=12)
	make_record(db, "vsql_test", vs_identifier="datetimedelta", vs_number=1.0 + 12/24 + 34/24/60 + 56/24/60/60)
	make_record(db, "vsql_test", vs_identifier="monthdelta", vs_int=3)
	make_record(db, "vsql_test", vs_identifier="color", vs_int=0x123456ff)

	make_record(db, "vsql_field", fld_id="science", fld_name="Science")
	make_record(db, "vsql_field", fld_id="mathematics", fld_name="Mathematics", fld_id_super="science")
	make_record(db, "vsql_field", fld_id="physics", fld_name="Physics", fld_id_super="science")
	make_record(db, "vsql_field", fld_id="computerscience", fld_name="Computer science", fld_id_super="science")
	make_record(db, "vsql_field", fld_id="art", fld_name="Art")
	make_record(db, "vsql_field", fld_id="film", fld_name="Film", fld_id_super="art")
	make_record(db, "vsql_field", fld_id="music", fld_name="Music", fld_id_super="art")
	make_record(db, "vsql_field", fld_id="literature", fld_name="Literature", fld_id_super="art")
	make_record(db, "vsql_field", fld_id="politics", fld_name="Politics")
	make_record(db, "vsql_field", fld_id="industry", fld_name="Industry")
	make_record(db, "vsql_field", fld_id="sport", fld_name="Sport")

	make_record(
		db,
		"vsql_person",
		per_id="ae",
		per_firstname="Albert",
		per_lastname="Einstein",
		per_gender="m",
		fld_id="physics",
		per_country_of_birth="Germany",
		per_date_of_birth=datetime.date(1879, 3, 14),
		per_date_of_death=datetime.date(1955, 4, 15),
		per_grave="40.216085 -74.7917151 Grave of Albery Einstein",
		per_nobel_prize=0,
		per_url="https://de.wikipedia.org/wiki/Albert_Einstein",
	)

	make_record(
		db,
		"vsql_person",
		per_id="mc",
		per_firstname="Marie",
		per_lastname="Curie",
		per_gender="f",
		fld_id="physics",
		per_country_of_birth="Poland",
		per_date_of_birth=datetime.date(1867, 11, 7),
		per_date_of_death=datetime.date(1934, 7, 4),
		per_grave="48.84672 2.34631 Grave of Marie Curie",
		per_nobel_prize=1,
		per_url="https://de.wikipedia.org/wiki/Marie_Curie",
	)

	make_record(
		db,
		"vsql_person",
		per_id="ma",
		per_firstname="Muhammad",
		per_lastname="Ali",
		per_gender="m",
		fld_id="sport",
		per_country_of_birth="USA",
		per_date_of_birth=datetime.date(1942, 1, 17),
		per_date_of_death=datetime.date(2016, 6, 3),
		per_grave="38.2454051 -85.7170115 Grave of Muhammad Ali",
		per_nobel_prize=0,
		per_url="https://de.wikipedia.org/wiki/Muhammad_Ali",
	)

	make_record(
		db,
		"vsql_person",
		per_id="mm",
		per_firstname="Marilyn",
		per_lastname="Monroe",
		per_gender="f",
		fld_id="film",
		per_country_of_birth="USA",
		per_date_of_birth=datetime.date(1926, 6, 1),
		per_date_of_death=datetime.date(1962, 8, 4),
		per_grave="34.05827 -118.44096 Grave of Marilyn Monroe",
		per_nobel_prize=0,
		per_url="https://de.wikipedia.org/wiki/Marilyn_Monroe",
	)

	make_record(
		db,
		"vsql_person",
		per_id="ep",
		per_firstname="Elvis",
		per_lastname="Presley",
		per_gender="m",
		fld_id="music",
		per_country_of_birth="USA",
		per_date_of_birth=datetime.date(1935, 1, 8),
		per_date_of_death=datetime.date(1977, 8, 16),
		per_grave="35.04522870295311 -90.02283096313477 Grave of Elvis Presley",
		per_nobel_prize=0,
		per_url="https://de.wikipedia.org/wiki/Elvis_Presley",
	)

	make_record(
		db,
		"vsql_person",
		per_id="br",
		per_firstname="Bernhard",
		per_lastname="Riemann",
		per_gender="m",
		fld_id="mathematics",
		per_country_of_birth="Germany",
		per_date_of_birth=datetime.date(1826, 6, 17),
		per_date_of_death=datetime.date(1866, 6, 20),
		per_grave="45.942127 8.5870263, Grave of Bernhard Riemann",
		per_nobel_prize=0,
		per_url="https://de.wikipedia.org/wiki/Bernhard_Riemann",
	)

	make_record(
		db,
		"vsql_person",
		per_id="cfg",
		per_firstname="Carl Friedrich",
		per_lastname="Gauß",
		per_gender="m",
		fld_id="mathematics",
		per_country_of_birth="Germany",
		per_date_of_birth=datetime.date(1777, 4, 30),
		per_date_of_death=datetime.date(1855, 2, 23),
		per_grave="51.53157404627684 9.94189739227295 Grave of Carl Friedrich Gauß",
		per_nobel_prize=0,
		per_url="https://de.wikipedia.org/wiki/Carl_Friedrich_Gau%C3%9F",
	)

	make_record(
		db,
		"vsql_person",
		per_id="dk",
		per_firstname="Donald",
		per_lastname="Knuth",
		per_gender="m",
		fld_id="computerscience",
		per_country_of_birth="USA",
		per_date_of_birth=datetime.date(1938, 1, 10),
		per_url="https://de.wikipedia.org/wiki/Donald_E._Knuth",
	)

	make_record(
		db,
		"vsql_person",
		per_id="rr",
		per_firstname="Ronald",
		per_lastname="Reagan",
		per_gender="m",
		fld_id="politics",
		per_country_of_birth="USA",
		per_date_of_birth=datetime.date(1911, 2, 6),
		per_date_of_death=datetime.date(2004, 6, 5),
		per_grave="34.2590025 -118.8226249 Grave of Roland Reagan",
		per_nobel_prize=0,
		per_url="https://de.wikipedia.org/wiki/Ronald_Reagan",
	)

	make_record(
		db,
		"vsql_person",
		per_id="am",
		per_firstname="Angela",
		per_lastname="Merkel",
		per_gender="f",
		fld_id="politics",
		per_country_of_birth="Germany",
		per_date_of_birth=datetime.date(1954, 6, 17),
		per_date_of_death=None,
		per_grave=None,
		per_nobel_prize=0,
		per_url="https://de.wikipedia.org/wiki/Angela_Merkel",
	)

	db.commit()


@pytest.fixture(scope="session")
def vsql_data(tmp_path_factory, worker_id):
	"""
	A test fixture that sets up the database for testing vSQL
	"""

	# Don't use the fixture `db` becuase of different scopes.
	db = orasql.connect(dbname, readlobs=True)

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
