import os, datetime, decimal, filelock, aod

import psycopg
from psycopg import rows, sql

from ll import orasql, misc

import pytest

from ll import vsql

dbname_oracle = os.environ.get("LL_PYSQL_TEST_CONNECT_ORACLE") # Need a connectstring as environment var
dbname_postgres = os.environ.get("LL_PYSQL_TEST_CONNECT_POSTGRES") # Need a connectstring as environment var


###
### ``pytest`` test fixtures and helper classes
###

class VSQLDB:
	# Whether the database can store the character ``U+0000`` in string values
	supports_nul = True

	def query(self, comment=None, **vars):
		return self.queryclass(comment, **vars)

	def execute(self, query):
		sql = query.sqlsource()
		print(f"Executing query:\n{sql}")
		return self.db.cursor().execute(sql).fetchall()

	def expr(self, vsqlexpr, *, where=None):
		query = self.query(r=self.r)
		query.select_vsql(vsqlexpr)
		if where:
			query.where_vsql(where)
		rs = self.execute(query)
		assert len(rs) == 1
		return self.extract_result(rs[0][0])

	def extract_result(self, value):
		return value


class VSQLOracle(VSQLDB):
	dbtype = vsql.DBType.ORACLE
	queryclass = vsql.OracleQuery

	# Connect on first use, so that the tests for the other database can be run
	# (via ``-m 'not oracle'``) without an Oracle database being available
	db = aod.Attr[orasql.Connection]("connect")

	test_table = vsql.Group("vsql_test")
	test_table.add_field("identifier", vsql.DataType.STR, "{a}.vs_identifier", description="The identifier")
	test_table.add_field("v_bool", vsql.DataType.BOOL, "{a}.vs_bool", description="The bool attribute")
	test_table.add_field("v_int", vsql.DataType.INT, "{a}.vs_int", description="The int attribute")
	test_table.add_field("v_number", vsql.DataType.NUMBER, "{a}.vs_number", description="The number attribute")
	test_table.add_field("v_str", vsql.DataType.STR, "{a}.vs_str", description="The str attribute")
	test_table.add_field("v_clob", vsql.DataType.CLOB, "{a}.vs_clob", description="The clob attribute")
	test_table.add_field("v_date", vsql.DataType.DATE, "{a}.vs_date", description="The date attribute")
	test_table.add_field("v_datetime", vsql.DataType.DATETIME, "{a}.vs_datetime", description="The datetime attribute")
	test_table.add_field("v_datedelta", vsql.DataType.DATEDELTA, "{a}.vs_datedelta", description="The datedelta attribute")
	test_table.add_field("v_datetimedelta", vsql.DataType.DATETIMEDELTA, "{a}.vs_datetimedelta", description="The datetimedelta attribute")
	test_table.add_field("v_monthdelta", vsql.DataType.MONTHDELTA, "{a}.vs_monthdelta", description="The monthdelta attribute")
	test_table.add_field("v_color", vsql.DataType.COLOR, "{a}.vs_int", description="The color attribute")

	field_table = vsql.Group("vsql_field")
	field_table.add_field("id", vsql.DataType.STR, "{a}.fld_id")
	field_table.add_field("name", vsql.DataType.STR, "{a}.fld_name")
	field_table.add_field("parent", vsql.DataType.STR, "{a}.fld_id_super", "{m}.fld_id_super = {d}.fld_id", field_table)

	person_table = vsql.Group("vsql_person")
	person_table.add_field("id", vsql.DataType.STR, "{a}.per_id")
	person_table.add_field("firstname", vsql.DataType.STR, "{a}.per_firstname")
	person_table.add_field("lastname", vsql.DataType.STR, "{a}.per_lastname")
	person_table.add_field("gender", vsql.DataType.STR, "{a}.per_gender")
	person_table.add_field("field", vsql.DataType.STR, "{a}.fld_id", "{m}.fld_id = {d}.fld_id", field_table)
	person_table.add_field("date_of_birth", vsql.DataType.DATE, "{a}.per_date_of_birth")
	person_table.add_field("date_of_death", vsql.DataType.DATE, "{a}.per_date_of_death")
	person_table.add_field("country_of_birth", vsql.DataType.STR, "{a}.per_country_of_birth")
	person_table.add_field("grave", vsql.DataType.GEO, "{a}.per_grave")
	person_table.add_field("nobel_prize", vsql.DataType.BOOL, "{a}.per_nobel_prize")
	person_table.add_field("url", vsql.DataType.STR, "{a}.per_url")
	person_table.add_field("createdat", vsql.DataType.DATETIME, "{a}.per_createdat")

	p = vsql.Field("p", vsql.DataType.STR, "1 = 1", "2 = 2", refgroup=person_table)

	r = vsql.Field("r", vsql.DataType.STR, "?", "1 = 1", test_table, "Loop variable over all records")

	type_for_bool = int
	type_for_date = datetime.datetime
	type_for_datetime = datetime.datetime

	@staticmethod
	def type_for_datedelta(days=0):
		return days

	@staticmethod
	def type_for_datetimedelta(days=0, seconds=0):
		return days + seconds/86400

	@staticmethod
	def type_for_monthdelta(months=0):
		return months

	def connect(self):
		self.db = orasql.connect(dbname_oracle, readlobs=True)

	def extract_result(self, value):
		if isinstance(value, orasql.DbObject):
			value = [self.extract_result(item) for item in value.aslist()]
		elif isinstance(value, orasql.LOB):
			value = value.read()
		return value


class VSQLPostgres(VSQLDB):
	dbtype = vsql.DBType.POSTGRES
	queryclass = vsql.PostgresQuery

	# Connect on first use, so that the tests for the other database can be run
	# (via ``-m 'not postgres'``) without a PostgreSQL database being available
	db = aod.Attr[psycopg.Connection]("connect")

	# PostgreSQL rejects ``U+0000`` in ``text`` values
	supports_nul = False

	test_table = vsql.Group("vsql_test.vsql_test")
	test_table.add_field("identifier", vsql.DataType.STR, "{a}.vs_identifier", description="The identifier")
	test_table.add_field("v_bool", vsql.DataType.BOOL, "{a}.vs_bool", description="The bool attribute")
	test_table.add_field("v_int", vsql.DataType.INT, "{a}.vs_int", description="The int attribute")
	test_table.add_field("v_number", vsql.DataType.NUMBER, "{a}.vs_number", description="The number attribute")
	test_table.add_field("v_str", vsql.DataType.STR, "{a}.vs_str", description="The str attribute")
	test_table.add_field("v_clob", vsql.DataType.CLOB, "{a}.vs_clob", description="The clob attribute")
	test_table.add_field("v_date", vsql.DataType.DATE, "{a}.vs_date", description="The date attribute")
	test_table.add_field("v_datetime", vsql.DataType.DATETIME, "{a}.vs_datetime", description="The datetime attribute")
	test_table.add_field("v_datedelta", vsql.DataType.DATEDELTA, "{a}.vs_datedelta", description="The datedelta attribute")
	test_table.add_field("v_datetimedelta", vsql.DataType.DATETIMEDELTA, "{a}.vs_datetimedelta", description="The datetimedelta attribute")
	test_table.add_field("v_monthdelta", vsql.DataType.MONTHDELTA, "{a}.vs_monthdelta", description="The monthdelta attribute")
	test_table.add_field("v_color", vsql.DataType.COLOR, "{a}.vs_int", description="The color attribute")

	field_table = vsql.Group("vsql_test.vsql_field")
	field_table.add_field("id", vsql.DataType.STR, "{a}.fld_id")
	field_table.add_field("name", vsql.DataType.STR, "{a}.fld_name")
	field_table.add_field("parent", vsql.DataType.STR, "{a}.fld_id_super", "{m}.fld_id_super = {d}.fld_id", field_table)

	person_table = vsql.Group("vsql_test.vsql_person")
	person_table.add_field("id", vsql.DataType.STR, "{a}.per_id")
	person_table.add_field("firstname", vsql.DataType.STR, "{a}.per_firstname")
	person_table.add_field("lastname", vsql.DataType.STR, "{a}.per_lastname")
	person_table.add_field("gender", vsql.DataType.STR, "{a}.per_gender")
	person_table.add_field("field", vsql.DataType.STR, "{a}.fld_id", "{m}.fld_id = {d}.fld_id", field_table)
	person_table.add_field("date_of_birth", vsql.DataType.DATE, "{a}.per_date_of_birth")
	person_table.add_field("date_of_death", vsql.DataType.DATE, "{a}.per_date_of_death")
	person_table.add_field("country_of_birth", vsql.DataType.STR, "{a}.per_country_of_birth")
	person_table.add_field("grave", vsql.DataType.GEO, "{a}.per_grave")
	person_table.add_field("nobel_prize", vsql.DataType.BOOL, "{a}.per_nobel_prize")
	person_table.add_field("url", vsql.DataType.STR, "{a}.per_url")
	person_table.add_field("createdat", vsql.DataType.DATETIME, "{a}.per_createdat")

	p = vsql.Field("p", vsql.DataType.STR, "1 = 1", "2 = 2", refgroup=person_table)

	r = vsql.Field("r", vsql.DataType.STR, "?", "1 = 1", test_table, "Loop variable over all records")

	type_for_bool = bool
	type_for_date = datetime.date
	type_for_datetime = datetime.datetime

	@staticmethod
	def type_for_datedelta(days=0):
		return datetime.timedelta(days=days)

	@staticmethod
	def type_for_datetimedelta(days=0, seconds=0):
		return datetime.timedelta(days=days, seconds=seconds)

	@staticmethod
	def type_for_monthdelta(months=0):
		# ``psycopg`` converts the year/month part of an ``interval`` into days
		# (using 365 days per year and 30 days per month)
		years = int(months/12)
		return datetime.timedelta(days=years * 365 + (months - 12 * years) * 30)

	def connect(self):
		self.db = psycopg.connect(dbname_postgres, row_factory=rows.namedtuple_row)

	def extract_result(self, value):
		# ``psycopg`` returns ``numeric`` values as ``decimal.Decimal``, but the
		# tests (and the Oracle implementation) use :class:`float`
		if isinstance(value, decimal.Decimal):
			value = float(value)
		elif isinstance(value, list):
			value = [self.extract_result(item) for item in value]
		return value

	def execute(self, query):
		self.db.rollback() # If the previous test failed, get rid of broken transaction
		return super().execute(query)


vsql_db_params = [
	pytest.param("oracle", marks=pytest.mark.oracle),
	pytest.param("postgres", marks=pytest.mark.postgres),
]


all_vsql_dbs = dict(
	oracle=VSQLOracle(),
	postgres=VSQLPostgres(),
)


@pytest.fixture(scope="module", params=vsql_db_params)
def vsql_db(request):
	return all_vsql_dbs[request.param]


def make_records(dbtype, db):
	def make_record(table, **kwargs):
		if dbtype is vsql.DBType.ORACLE:
			fields = t""
			values = t""
			for (i, (fieldname, fieldvalue)) in enumerate(kwargs.items()):
				if i:
					fields += t", "
					values += t", "
				fields += t"{fieldname:q}"
				if isinstance(fieldvalue, bool):
					fieldvalue = int(fieldvalue)
				elif isinstance(fieldvalue, misc.monthdelta):
					fieldvalue = fieldvalue.months()
				elif isinstance(fieldvalue, datetime.timedelta):
					if fieldvalue.seconds == 0 and fieldvalue.microseconds == 0:
						fieldvalue = fieldvalue.days
					else:
						fieldvalue = fieldvalue.days + fieldvalue.seconds/86400 + fieldvalue.microseconds/86400000000
				values += t"{fieldvalue}"

			query = t"insert into {table:q} ({fields:q}) values ({values:q})"
			db.cursor().execute(query)
		else:
			fields = t""
			values = t""
			for (i, (fieldname, fieldvalue)) in enumerate(kwargs.items()):
				if i:
					fields += t", "
					values += t", "
				fields += t"{sql.SQL(fieldname):q}"
				if isinstance(fieldvalue, misc.monthdelta):
					values += t"interval '{sql.SQL(str(fieldvalue.months())):q} months'"
				else:
					values += t"{fieldvalue}"

			query = t"insert into vsql_test.{sql.SQL(table):q} ({fields:q}) values ({values:q})"
			db.cursor().execute(query)

	make_record("vsql_test", vs_identifier="none")
	make_record("vsql_test", vs_identifier="bool_false", vs_bool=False)
	make_record("vsql_test", vs_identifier="bool_true", vs_bool=True)
	make_record("vsql_test", vs_identifier="date", vs_date=datetime.date(2000, 2, 29))
	make_record("vsql_test", vs_identifier="datetime", vs_datetime=datetime.datetime(2000, 2, 29, 12, 34, 56))
	make_record("vsql_test", vs_identifier="str", vs_str="gurk")
	make_record("vsql_test", vs_identifier="clob", vs_clob="gurk"*100000)
	make_record("vsql_test", vs_identifier="shortclob", vs_clob="gurk")
	make_record("vsql_test", vs_identifier="int", vs_int=1776)
	make_record("vsql_test", vs_identifier="number", vs_number=42.5)
	make_record("vsql_test", vs_identifier="datedelta", vs_datedelta=datetime.timedelta(12))
	make_record("vsql_test", vs_identifier="datetimedelta", vs_datetimedelta=datetime.timedelta(days=1, hours=12, minutes=34, seconds=56))
	make_record("vsql_test", vs_identifier="monthdelta", vs_monthdelta=misc.monthdelta(3))
	make_record("vsql_test", vs_identifier="color", vs_int=0x123456ff)

	make_record("vsql_field", fld_id="science", fld_name="Science")
	make_record("vsql_field", fld_id="mathematics", fld_name="Mathematics", fld_id_super="science")
	make_record("vsql_field", fld_id="physics", fld_name="Physics", fld_id_super="science")
	make_record("vsql_field", fld_id="computerscience", fld_name="Computer science", fld_id_super="science")
	make_record("vsql_field", fld_id="art", fld_name="Art")
	make_record("vsql_field", fld_id="film", fld_name="Film", fld_id_super="art")
	make_record("vsql_field", fld_id="music", fld_name="Music", fld_id_super="art")
	make_record("vsql_field", fld_id="literature", fld_name="Literature", fld_id_super="art")
	make_record("vsql_field", fld_id="politics", fld_name="Politics")
	make_record("vsql_field", fld_id="industry", fld_name="Industry")
	make_record("vsql_field", fld_id="sport", fld_name="Sport")

	make_record(
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
		per_nobel_prize=False,
		per_url="https://de.wikipedia.org/wiki/Albert_Einstein",
	)

	make_record(
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
		per_nobel_prize=True,
		per_url="https://de.wikipedia.org/wiki/Marie_Curie",
	)

	make_record(
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
		per_nobel_prize=False,
		per_url="https://de.wikipedia.org/wiki/Muhammad_Ali",
	)

	make_record(
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
		per_nobel_prize=False,
		per_url="https://de.wikipedia.org/wiki/Marilyn_Monroe",
	)

	make_record(
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
		per_nobel_prize=False,
		per_url="https://de.wikipedia.org/wiki/Elvis_Presley",
	)

	make_record(
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
		per_nobel_prize=False,
		per_url="https://de.wikipedia.org/wiki/Bernhard_Riemann",
	)

	make_record(
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
		per_nobel_prize=False,
		per_url="https://de.wikipedia.org/wiki/Carl_Friedrich_Gau%C3%9F",
	)

	make_record(
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
		per_nobel_prize=False,
		per_url="https://de.wikipedia.org/wiki/Ronald_Reagan",
	)

	make_record(
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
		per_nobel_prize=False,
		per_url="https://de.wikipedia.org/wiki/Angela_Merkel",
	)


def setup_vsql_data_oracle():
	dbo = orasql.connect(dbname_oracle, readlobs=True)

	co = dbo.cursor()
	try:
		co.execute("drop table vsql_test")
	except Exception:
		pass

	try:
		co.execute("drop table vsql_field")
	except Exception:
		pass

	try:
		co.execute("drop table vsql_person")
	except Exception:
		pass

	co.execute("""
		create table vsql_test
		(
			vs_identifier varchar2(100),
			vs_bool integer,
			vs_int integer,
			vs_number number,
			vs_str varchar2(4000),
			vs_clob clob,
			vs_date date,
			vs_datetime date,
			vs_datedelta integer,
			vs_datetimedelta number,
			vs_monthdelta integer
		)
	""")

	co.execute("""
		create table vsql_field
		(
			fld_id varchar2(16),
			fld_name varchar2(200),
			fld_id_super varchar2(8)
		)
	""")

	co.execute("""
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

	make_records(vsql.DBType.ORACLE, dbo)

	dbo.commit()


def setup_vsql_data_postgres():
	dbp = psycopg.connect(dbname_postgres, row_factory=rows.namedtuple_row)

	cp = dbp.cursor()
	cp.execute("drop schema if exists vsql_test cascade")

	cp.execute("create schema vsql_test")

	cp.execute("""
		create table vsql_test.vsql_test
		(
			vs_identifier text,
			vs_bool boolean,
			vs_int bigint,
			vs_number numeric,
			vs_str text,
			vs_clob text,
			vs_date date,
			vs_datetime timestamp,
			vs_datedelta interval,
			vs_datetimedelta interval,
			vs_monthdelta interval
		)
	""")

	cp.execute("""
		create table vsql_test.vsql_field
		(
			fld_id varchar(16),
			fld_name varchar(200),
			fld_id_super varchar(8)
		)
	""")

	cp.execute("""
		create table vsql_test.vsql_person
		(
			per_id varchar(16),
			per_firstname varchar(200),
			per_lastname varchar(200),
			per_gender varchar(2),
			fld_id varchar(16),
			per_date_of_birth date,
			per_date_of_death date,
			per_country_of_birth varchar(200),
			per_grave varchar(500),
			per_nobel_prize boolean,
			per_url varchar(200),
			per_createdat timestamp
		)
	""")

	make_records(vsql.DBType.POSTGRES, dbp)

	dbp.commit()


@pytest.fixture(scope="session")
def vsql_data(tmp_path_factory, worker_id):
	"""
	A test fixture that sets up the databases for testing vSQL
	"""

	# This uses the logic documented here:
	# https://pytest-xdist.readthedocs.io/en/latest/how-to.html#making-session-scoped-fixtures-execute-only-once
	# to support running under ``pytest-xdist``

	if worker_id == "master":
		# setup_vsql_data_oracle()
		setup_vsql_data_postgres()
		return

	# get the temp directory shared by all workers
	root_tmp_dir = tmp_path_factory.getbasetemp().parent

	# File that signals that test data has been created in the database
	fn = root_tmp_dir / "init.dummy"

	# Lock file to prevent concurrent checks
	ln = root_tmp_dir / "init.lock"

	with filelock.FileLock(ln):
		if not fn.is_file():
			# Create test data
			# setup_vsql_data_oracle()
			setup_vsql_data_postgres()
			# Record that test data has been created
			fn.write_text("done")
