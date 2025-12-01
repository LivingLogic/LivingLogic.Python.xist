"""
Tests for :class:`ll.vsql.Query`

To run the tests, :mod:`pytest` is required.
"""

import math, datetime

from conftest import *

from ll import vsql


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


###
### Tests
###

def test_query_comment(db, vsql_data):
	q = vsql.Query("foo")
	assert "/* foo */" in q.sqlsource()


def test_query_badcomment(db, vsql_data):
	q = vsql.Query("/* foo */")
	assert q.sqlsource().count("*/") == 1


def test_query_simple(db, vsql_data):
	q = vsql.Query(p=p)
	q.from_vsql("p")
	q.select_vsql("p.firstname", alias="fn")
	q.where_vsql("p.lastname == 'Einstein'")
	rs = execute(db, q)

	assert rs[0].fn == "Albert"


def test_query_foreignkey(db, vsql_data):
	q = vsql.Query(p=p)
	q.from_vsql("p")
	q.select_vsql("p.field.parent.name", alias="fld")
	q.where_vsql("p.lastname == 'Einstein'")
	rs = execute(db, q)

	assert rs[0].fld == "Science"


def test_query_count_all(db, vsql_data):
	q = vsql.Query(p=p)
	q.from_vsql("p")
	q.aggregate_vsql("count()", "Number of persons", "c")
	rs = execute(db, q)

	assert rs[0].c == 10


def test_query_count_by_gender(db, vsql_data):
	q = vsql.Query(p=p)
	q.from_vsql("p")
	q.aggregate_vsql("group(p.gender)")
	q.aggregate_vsql("count()")
	rs = execute(db, q)

	assert {r[0]: r[1] for r in rs} == {"f": 3, "m": 7}


def test_query_oldest_by_gender(db, vsql_data):
	q = vsql.Query(p=p)
	q.from_vsql("p")
	q.aggregate_vsql("group(p.gender)")
	q.aggregate_vsql("max( int( ( (p.date_of_death or @(2000-02-29)) - p.date_of_birth ).days / 365.2425 ) )")
	rs = execute(db, q)

	assert {r[0]: int(r[1]) for r in rs} == {
		"f": 66, # Marie Curie
		"m": 93, # Ronald Reagan
	}


def test_query_count_by_field(db, vsql_data):
	q = vsql.Query(p=p)
	q.from_vsql("p")
	q.aggregate_vsql("group(p.field.id)")
	q.aggregate_vsql("count()")
	rs = execute(db, q)

	assert {r[0]: int(r[1]) for r in rs} == {
		"computerscience": 1, # Donald Kunth
		"film": 1, # Marilyn Monroe
		"mathematics": 2, # Bern Reieman, Carl Friedrich Gauß
		"music": 1, # Elvis Presley
		"physics": 2, # Albert Einstain, Marie Curie
		"politics": 2, # Ronald Reagan, Angela Merkel
		"sport": 1, # Muhammad Ali
	}


def test_query_first_last_by_century(db, vsql_data):
	q = vsql.Query(p=p)
	q.from_vsql("p")
	q.aggregate_vsql("group(p.date_of_birth.year//100)")
	q.aggregate_vsql("min(str(p.date_of_birth))")
	q.aggregate_vsql("max(str(p.date_of_birth))")
	q.aggregate_vsql("count()")
	rs = execute(db, q)

	assert {r[0]: (r[1], r[2], r[3]) for r in rs} == {
		17: (
			'1777-04-30',
			'1777-04-30',
			1,
		),
		18: (
			'1826-06-17',
			'1879-03-14',
			3,
		),
		19: (
			'1911-02-06',
			'1954-06-17',
			6,
		),
	}
